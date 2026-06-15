import uuid


def gerar_email_unico(domain: str = "example.com") -> str:
    """Gera um email único usando uuid4 para evitar duplicidade nos testes."""
    return f"test_{uuid.uuid4().hex}@{domain}"


def normalize_bearer_token(token):
    if not isinstance(token, str):
        return None
    token = token.strip()
    return token.split(" ", 1)[1] if token.lower().startswith("bearer ") else token


def is_error_response(body) -> bool:
    if not isinstance(body, dict):
        return False
    if any(key in body for key in ("error", "message", "erro")):
        return True
    return any(isinstance(value, str) and value.strip() for value in body.values())


def extract_resource_id(data):
    if not isinstance(data, dict):
        return None

    if data.get("_id") or data.get("id"):
        return data.get("_id") or data.get("id")

    for key in ("usuario", "produto", "user", "item"):
        nested = data.get(key)
        if isinstance(nested, dict) and (nested.get("_id") or nested.get("id")):
            return nested.get("_id") or nested.get("id")

    return None
