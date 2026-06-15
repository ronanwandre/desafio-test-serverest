import requests


class ProdutosClient:
    """Cliente simples para o endpoint /produtos da API ServeRest."""

    def __init__(self, base_url: str = "https://compassuol.serverest.dev"):
        self.base_url = base_url.rstrip("/")

    def get_produtos(self) -> requests.Response:
        return requests.get(f"{self.base_url}/produtos")

    def post_produtos(self, payload: dict, token: str | None = None) -> requests.Response:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return requests.post(f"{self.base_url}/produtos", json=payload, headers=headers)

    def get_produto_by_id(self, produto_id: str) -> requests.Response:
        return requests.get(f"{self.base_url}/produtos/{produto_id}")

    def put_produto_by_id(self, produto_id: str, payload: dict, token: str) -> requests.Response:
        headers = {"Authorization": f"Bearer {token}"}
        return requests.put(f"{self.base_url}/produtos/{produto_id}", json=payload, headers=headers)

    def delete_produto_by_id(self, produto_id: str, token: str) -> requests.Response:
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(f"{self.base_url}/produtos/{produto_id}", headers=headers)
