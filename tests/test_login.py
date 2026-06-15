import uuid

from data.login_data import criar_payload_login
from data.usuarios_data import criar_payload_usuario
from helpers.schema_validators import LOGIN_RESPONSE_SCHEMA, validar_schema_json
from helpers.utils import normalize_bearer_token, is_error_response


def test_login_com_credenciais_validas_retorna_200_e_token(login_client, api):
    # Arrange
    usuario_payload = criar_payload_usuario(
        nome="Usuario Login",
        email=f"login_{uuid.uuid4().hex}@serverest.dev",
        administrador="true",
    )
    cadastro_response = api.post_usuarios(usuario_payload)
    assert cadastro_response.status_code == 201
    usuario_id = cadastro_response.json().get("_id") or cadastro_response.json().get("id")

    try:
        payload_login = criar_payload_login(usuario_payload["email"], usuario_payload["password"])

        # Act
        resposta = login_client.post_login(payload_login)

        # Assert
        assert resposta.status_code == 200
        body = resposta.json()
        validar_schema_json(body, LOGIN_RESPONSE_SCHEMA)
        assert body.get("authorization") or body.get("token")
    finally:
        if usuario_id:
            api.delete_usuario_by_id(usuario_id)


def test_login_com_senha_errada_retorna_401(login_client):
    # Arrange
    payload_login = criar_payload_login(f"nao.existe.{uuid.uuid4().hex}@serverest.dev", "SenhaIncorreta123")

    # Act
    resposta = login_client.post_login(payload_login)

    # Assert
    assert resposta.status_code == 401
    assert is_error_response(resposta.json())


def test_login_com_email_inexistente_retorna_401(login_client):
    # Arrange
    payload_login = criar_payload_login(f"usuario_inexistente.{uuid.uuid4().hex}@serverest.dev", "Senha123!")

    # Act
    resposta = login_client.post_login(payload_login)

    # Assert
    assert resposta.status_code == 401
    assert is_error_response(resposta.json())


def test_login_com_campos_vazios_retorna_400(login_client):
    # Arrange
    payload_login = criar_payload_login("", "")

    # Act
    resposta = login_client.post_login(payload_login)

    # Assert
    assert resposta.status_code == 400
    assert is_error_response(resposta.json())


def test_login_retorna_bearer_token_no_body(login_client, api):
    # Arrange
    usuario_payload = criar_payload_usuario(
        nome="Usuario Token",
        email=f"token_{uuid.uuid4().hex}@serverest.dev",
        administrador="true",
    )
    cadastro_response = api.post_usuarios(usuario_payload)
    assert cadastro_response.status_code == 201
    usuario_id = cadastro_response.json().get("_id") or cadastro_response.json().get("id")

    try:
        payload_login = criar_payload_login(usuario_payload["email"], usuario_payload["password"])

        # Act
        resposta = login_client.post_login(payload_login)

        # Assert
        assert resposta.status_code == 200
        body = resposta.json()
        token = normalize_bearer_token(body.get("authorization") or body.get("token"))
        assert token
    finally:
        if usuario_id:
            api.delete_usuario_by_id(usuario_id)
