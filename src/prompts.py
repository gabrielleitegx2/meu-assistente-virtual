
def construir_prompt_sistema() -> str:
    return "Você é um atendente educado e direto."

def construir_prompt_usuario(pergunta: str, produtos: list, politicas: str, pedidos: dict) -> str:
    return f"""Você é um assistente virtual de uma loja. Use os dados abaixo para responder perguntas.

### Produtos disponíveis:
{produtos}

### Políticas da loja:
{politicas}

### Pedidos (exemplo):
{pedidos}

### Agora responda a seguinte pergunta do cliente:
"{pergunta}"
"""
