import os
import sys
import pytest

# Garantir que o diretório src esteja no PYTHONPATH para importar o client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from api.usuarios_client import UsuariosClient
from helpers.utils import gerar_email_unico


@pytest.fixture
def api():
    """Instância do client para a API de usuários."""
    return UsuariosClient()


@pytest.fixture
def usuario_criado(api):
    """Cria um usuário antes do teste e garante remoção no teardown (yield fixture).

    Retorna um dicionário com `id`, `payload` e `response`.
    """
    payload = {
        "nome": "Usuario Fixture",
        "email": gerar_email_unico("serverest.dev"),
        "password": "Senha123!",
        "administrador": "true",
    }
    resp = api.post_usuarios(payload)
    user_id = None
    try:
        body = resp.json()
        # tentativas comuns de extrair id
        user_id = body.get("_id") or body.get("id") or (body.get("usuario") or {}).get("_id")
    except Exception:
        user_id = None

    # fallback: procurar pelo email na listagem
    if not user_id:
        list_resp = api.get_usuarios()
        try:
            data = list_resp.json()
            usuarios = data.get("usuarios", data if isinstance(data, list) else [])
            for u in usuarios:
                if u.get("email") == payload["email"]:
                    user_id = u.get("_id") or u.get("id")
                    break
        except Exception:
            user_id = None

    yield {"id": user_id, "payload": payload, "response": resp}

    # teardown: deletar se conseguiu capturar id
    if user_id:
        try:
            api.delete_usuario_by_id(user_id)
        except Exception:
            pass
