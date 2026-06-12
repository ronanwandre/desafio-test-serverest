import uuid


def criar_payload_usuario(nome: str | None = None,
                          email: str | None = None,
                          password: str = "Senha123!",
                          administrador: str = "true") -> dict:
    """Gera um payload de usuário. Se `email` não for fornecido, gera um único."""
    if not email:
        email = f"usuario_{uuid.uuid4().hex}@serverest.dev"
    if not nome:
        nome = f"Usuario {uuid.uuid4().hex[:6]}"
    return {
        "nome": nome,
        "email": email,
        "password": password,
        "administrador": administrador,
    }
