import os
import json
import re
import openai
from dotenv import load_dotenv
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from src.assistente import listar_produtos, consultar_pedido, ler_politicas
from src.prompts import construir_prompt_sistema

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inicialização do FAISS
EMBEDDING_MODEL = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

faiss_index = None

def extrair_numero_pedido(pergunta: str) -> str | None:
    match = re.search(r"#?(\d{4,})", pergunta)
    return match.group(1) if match else None

def extrair_preco_maximo(texto: str) -> float | None:
    texto = texto.replace(".", "").replace(",", ".")
    padrao = r"(?i)(?:até|no máximo)?\s*R?\$?\s?(\d{1,5}(?:[.,]\d{2})?)"
    match = re.search(padrao, texto)
    return float(match.group(1)) if match else None

def extrair_caracteristicas(texto: str) -> list:
    palavras_chave = [
        "notebook", "smartphone", "tela", "grande", "pequeno", "RAM", "memória",
        "SSD", "HD", "Intel", "AMD", "Android", "Apple", "iPhone", "bateria"
    ]
    return [palavra for palavra in palavras_chave if palavra.lower() in texto.lower()]

def criar_documentos(pergunta: str = "") -> List[Document]:
    documentos = []

    preco_max = extrair_preco_maximo(pergunta)
    caracteristicas = extrair_caracteristicas(pergunta)
    produtos = listar_produtos()

    produtos_filtrados = []
    for prod in produtos:
        condicoes = []

        if preco_max:
            condicoes.append(prod["preco"] <= preco_max)

        if caracteristicas:
            texto_produto = f"{prod['nome']} {prod['descricao']} {' '.join(prod['especificacoes'].values())}".lower()
            condicoes += [c.lower() in texto_produto for c in caracteristicas]

        if not condicoes or all(condicoes):
            produtos_filtrados.append(prod)

    for produto in produtos_filtrados:
        conteudo = f"Produto: {produto['nome']}\nDescrição: {produto['descricao']}\nPreço: R$ {produto['preco']}"
        documentos.append(Document(page_content=conteudo, metadata={"tipo": "produto"}))

    # Políticas
    politicas = ler_politicas()
    documentos.append(Document(page_content=politicas, metadata={"tipo": "politica"}))

    # Pedido dinâmico
    numero_pedido = extrair_numero_pedido(pergunta)
    if numero_pedido:
        pedido = consultar_pedido(numero_pedido)
        if pedido:
            conteudo = json.dumps(pedido, indent=2, ensure_ascii=False)
            documentos.append(Document(page_content=conteudo, metadata={"tipo": "pedido"}))

    # Recomendação personalizada
    palavras_chave_recomendacao = ["recomenda", "sugere", "sugestão", "presente", "indicação", "gosta de"]
    if any(p in pergunta.lower() for p in palavras_chave_recomendacao):
        recomendados = [
            produto for produto in produtos
            if any(palavra in produto["descricao"].lower() or palavra in produto["nome"].lower()
                   for palavra in pergunta.lower().split())
        ]
        for r in recomendados:
            conteudo = f"[Sugestão personalizada]\nProduto: {r['nome']}\nDescrição: {r['descricao']}\nPreço: R$ {r['preco']}"
            documentos.append(Document(page_content=conteudo, metadata={"tipo": "recomendacao"}))

    return documentos

def inicializar_faiss(pergunta: str = ""):
    global faiss_index
    docs = criar_documentos(pergunta)
    docs_chunked = text_splitter.split_documents(docs)
    faiss_index = FAISS.from_documents(docs_chunked, EMBEDDING_MODEL)

# Inicializa com dados genéricos (sem pedido específico)
inicializar_faiss()

def responder_com_ia(pergunta: str) -> str:
    inicializar_faiss(pergunta)

    if faiss_index is None:
        raise ValueError("O índice FAISS não foi inicializado.")

    documentos_relevantes = faiss_index.similarity_search(pergunta, k=4)
    contexto = "\n---\n".join([doc.page_content for doc in documentos_relevantes])

    prompt_sistema = construir_prompt_sistema()
    prompt_usuario = f"Você está conversando com um cliente da loja. Use as informações abaixo para ajudá-lo.\n{contexto}\n\nPergunta: {pergunta}"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        temperature=0.4
    )

    return resposta.choices[0].message.content
