from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.assistente import listar_produtos, buscar_produto_por_id, consultar_pedido, ler_politicas
from src.rag_system import responder_com_ia

app = FastAPI(title="Assistente Virtual da Loja")

# Atualizado: monta static e templates fora de src/
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def renderizar_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Modelo para requisição de pergunta
class Pergunta(BaseModel):
    mensagem: str

@app.get("/produtos")
def get_produtos():
    return listar_produtos()

@app.get("/produtos/{produto_id}")
def get_produto_por_id(produto_id: str):
    produto = buscar_produto_por_id(produto_id)
    if produto:
        return produto
    return {"erro": "Produto não encontrado."}

@app.get("/pedidos/{pedido_id}")
def get_pedido_por_id(pedido_id: str):
    pedido = consultar_pedido(pedido_id)
    if pedido:
        return pedido
    return {"erro": "Pedido não encontrado."}

@app.get("/politicas")
def get_politicas():
    return {"conteudo": ler_politicas()}

@app.post("/perguntar")
def perguntar(pergunta: Pergunta):
    resposta = responder_com_ia(pergunta.mensagem)
    return {"resposta": resposta}
