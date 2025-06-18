import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_PRODUTOS = os.path.join(BASE_DIR, "data", "produtos.json")
CAMINHO_PEDIDOS = os.path.join(BASE_DIR, "data", "pedidos.json")
CAMINHO_POLITICAS = os.path.join(BASE_DIR, "data", "politicas.md")


def listar_produtos():
    with open(CAMINHO_PRODUTOS, "r", encoding="utf-8") as f:
        return json.load(f)


def buscar_produto_por_id(produto_id):
    produtos = listar_produtos()
    for produto in produtos:
        if produto["id"] == produto_id:
            return produto
    return None


def consultar_pedido(pedido_id):
    with open(CAMINHO_PEDIDOS, "r", encoding="utf-8") as f:
        pedidos = json.load(f)
        for pedido in pedidos:
            if pedido["pedido_id"] == pedido_id:
                return pedido
    return None


def ler_politicas():
    with open(CAMINHO_POLITICAS, "r", encoding="utf-8") as f:
        return f.read()
