import requests


class UsuariosClient:
    """Cliente simples para o endpoint /usuarios da API ServeRest.

    Todos os métodos retornam o objeto `requests.Response` bruto.
    """

    def __init__(self, base_url: str = "https://compassuol.serverest.dev"):
        self.base_url = base_url.rstrip('/')

    def get_usuarios(self) -> requests.Response:
        return requests.get(f"{self.base_url}/usuarios")

    def post_usuarios(self, payload: dict) -> requests.Response:
        return requests.post(f"{self.base_url}/usuarios", json=payload)

    def get_usuario_by_id(self, user_id: str) -> requests.Response:
        return requests.get(f"{self.base_url}/usuarios/{user_id}")

    def put_usuario_by_id(self, user_id: str, payload: dict) -> requests.Response:
        return requests.put(f"{self.base_url}/usuarios/{user_id}", json=payload)

    def delete_usuario_by_id(self, user_id: str) -> requests.Response:
        return requests.delete(f"{self.base_url}/usuarios/{user_id}")
