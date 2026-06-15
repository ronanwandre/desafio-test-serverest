import uuid


def criar_payload_produto(nome: str | None = None,
                           preco: float = 10.0,
                           descricao: str = "Produto de teste",
                           quantidade: int = 10) -> dict:
    if not nome:
        nome = f"Produto Teste {uuid.uuid4().hex[:8]}"
    return {
        "nome": nome,
        "preco": preco,
        "descricao": descricao,
        "quantidade": quantidade,
    }
