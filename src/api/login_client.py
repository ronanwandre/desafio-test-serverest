import requests


class LoginClient:
    """Cliente simples para o endpoint /login da API ServeRest."""

    def __init__(self, base_url: str = "https://compassuol.serverest.dev"):
        self.base_url = base_url.rstrip("/")

    def post_login(self, payload: dict) -> requests.Response:
        return requests.post(f"{self.base_url}/login", json=payload)
