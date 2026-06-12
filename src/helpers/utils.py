import uuid


def gerar_email_unico(domain: str = "example.com") -> str:
    """Gera um email único usando uuid4 para evitar duplicidade nos testes."""
    return f"test_{uuid.uuid4().hex}@{domain}"
