import os
import sys

import pytest

# Garantir que o diretório src esteja no PYTHONPATH para importar os clientes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from api.login_client import LoginClient
from api.produtos_client import ProdutosClient
from api.usuarios_client import UsuariosClient
from data.login_data import criar_payload_login
from data.usuarios_data import criar_payload_usuario
from helpers.utils import gerar_email_unico, normalize_bearer_token


@pytest.fixture
def api():
    return UsuariosClient()


@pytest.fixture
def usuario_criado(api):
    payload = criar_payload_usuario(
        nome="Usuario Fixture",
        email=gerar_email_unico("serverest.dev"),
        administrador="true",
    )
    resposta = api.post_usuarios(payload)
    assert resposta.status_code == 201
    user_id = resposta.json().get("_id") or resposta.json().get("id") or (resposta.json().get("usuario") or {}).get("_id")
    yield {"id": user_id, "payload": payload, "response": resposta}

    if user_id:
        try:
            api.delete_usuario_by_id(user_id)
        except Exception:
            pass


@pytest.fixture
def login_client():
    return LoginClient()


@pytest.fixture
def produtos_client():
    return ProdutosClient()


@pytest.fixture
def token_admin(api, login_client):
    payload_usuario = criar_payload_usuario(
        nome="Admin Fixture",
        email=gerar_email_unico("serverest.dev"),
        administrador="true",
    )
    resposta_cadastro = api.post_usuarios(payload_usuario)
    assert resposta_cadastro.status_code == 201

    payload_login = criar_payload_login(payload_usuario["email"], payload_usuario["password"])
    resposta_login = login_client.post_login(payload_login)
    assert resposta_login.status_code == 200
    body_login = resposta_login.json()
    token = normalize_bearer_token(body_login.get("authorization") or body_login.get("token"))
    assert token, "Token de autenticação não encontrado na resposta de login"

    yield token

    # Teardown: deletar usuário admin criado para o token
    user_id = resposta_cadastro.json().get("_id") or resposta_cadastro.json().get("id")
    if user_id:
        try:
            api.delete_usuario_by_id(user_id)
        except Exception:
            pass


