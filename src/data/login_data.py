def criar_payload_login(email: str, password: str) -> dict:
    return {
        "email": email,
        "password": password,
    }
