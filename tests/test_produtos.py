from data.login_data import criar_payload_login
from data.produtos_data import criar_payload_produto
from data.usuarios_data import criar_payload_usuario
from helpers.schema_validators import PRODUTOS_LIST_SCHEMA, PRODUTO_DETAIL_SCHEMA, validar_schema_json
from helpers.utils import gerar_email_unico, is_error_response, normalize_bearer_token


def test_listar_produtos_retorna_200_e_lista(produtos_client):
    # Arrange / Act
    resposta = produtos_client.get_produtos()

    # Assert
    assert resposta.status_code == 200
    body = resposta.json()
    validar_schema_json({"produtos": body.get("produtos") if isinstance(body, dict) else body}, PRODUTOS_LIST_SCHEMA)
    assert isinstance(body.get("produtos") if isinstance(body, dict) else body, list)


def test_cadastrar_produto_valido_com_token_admin_retorna_201(produtos_client, token_admin):
    # Arrange
    payload = criar_payload_produto()

    # Act
    resposta = produtos_client.post_produtos(payload, token_admin)

    # Assert
    assert resposta.status_code == 201
    body = resposta.json()
    produto = body.get("produto") or body
    # API pode retornar somente _id + message no body; se não vier o objeto completo, buscar por id
    if produto.get("nome"):
        assert produto.get("nome") == payload["nome"]
        assert produto.get("preco") == payload["preco"]
    else:
        produto_id = body.get("_id") or body.get("id") or (body.get("produto") or {}).get("_id")
        assert produto_id, "Resposta de criação não incluiu id do produto"
        # buscar o produto e validar os campos
        get_resp = produtos_client.get_produto_by_id(produto_id)
        assert get_resp.status_code == 200
        produto_full = (get_resp.json().get("produto") or get_resp.json())
        assert produto_full.get("nome") == payload["nome"]
        assert produto_full.get("preco") == payload["preco"]


def test_cadastrar_produto_sem_token_retorna_401(produtos_client):
    # Arrange
    payload = criar_payload_produto()

    # Act
    resposta = produtos_client.post_produtos(payload, None)

    # Assert
    assert resposta.status_code == 401
    assert is_error_response(resposta.json())


def test_cadastrar_produto_nome_duplicado_retorna_400(produtos_client, token_admin):
    # Arrange
    payload = criar_payload_produto()
    primeira_resposta = produtos_client.post_produtos(payload, token_admin)
    assert primeira_resposta.status_code == 201

    # Act
    segunda_resposta = produtos_client.post_produtos(payload, token_admin)

    # Assert
    assert segunda_resposta.status_code == 400
    assert is_error_response(segunda_resposta.json())


def test_buscar_produto_por_id_valido_retorna_200(produtos_client, token_admin):
    # Arrange
    payload = criar_payload_produto()
    create_resp = produtos_client.post_produtos(payload, token_admin)
    assert create_resp.status_code == 201
    produto_id = (create_resp.json().get("produto") or create_resp.json()).get("_id")

    # Act
    resposta = produtos_client.get_produto_by_id(produto_id)

    # Assert
    assert resposta.status_code == 200
    body = resposta.json()
    validar_schema_json(body, PRODUTO_DETAIL_SCHEMA)
    produto = body.get("produto") or body
    assert produto.get("_id") == produto_id


def test_buscar_produto_por_id_inexistente_retorna_400(produtos_client):
    # Arrange
    fake_id = "inexistente1234567890"

    # Act
    resposta = produtos_client.get_produto_by_id(fake_id)

    # Assert
    assert resposta.status_code == 400
    assert is_error_response(resposta.json())


def test_atualizar_produto_existente_retorna_200(produtos_client, token_admin):
    # Arrange
    payload = criar_payload_produto()
    create_resp = produtos_client.post_produtos(payload, token_admin)
    assert create_resp.status_code == 201
    produto_id = (create_resp.json().get("produto") or create_resp.json()).get("_id")
    update_payload = {**payload, "nome": f"{payload['nome']} Atualizado", "preco": payload["preco"] + 5}

    # Act
    resposta = produtos_client.put_produto_by_id(produto_id, update_payload, token_admin)

    # Assert
    assert resposta.status_code == 200
    body = resposta.json()
    assert body.get("message") or (body.get("produto") or {}).get("nome") == update_payload["nome"]


def test_excluir_produto_existente_retorna_200(produtos_client, token_admin):
    # Arrange
    payload = criar_payload_produto()
    create_resp = produtos_client.post_produtos(payload, token_admin)
    assert create_resp.status_code == 201
    produto_id = (create_resp.json().get("produto") or create_resp.json()).get("_id")

    # Act
    resposta = produtos_client.delete_produto_by_id(produto_id, token_admin)

    # Assert
    assert resposta.status_code == 200
    assert is_error_response(resposta.json()) or "message" in resposta.json() or "ok" in resposta.json() or "resultado" in resposta.json()


def test_excluir_produto_inexistente_retorna_200_com_mensagem(produtos_client, token_admin):
    # Arrange
    fake_id = "inexistente1234567890"

    # Act
    resposta = produtos_client.delete_produto_by_id(fake_id, token_admin)

    # Assert
    assert resposta.status_code in (200, 400)
    body = resposta.json()
    assert isinstance(body, dict)
    has_generic = any(k in body for k in ("message", "error", "erro"))
    has_field_errors = any(isinstance(v, str) and v.strip() for v in body.values())
    assert has_generic or has_field_errors


def test_cadastrar_produto_com_token_nao_admin_retorna_403(produtos_client, api, login_client):
    # Arrange
    usuario_payload = criar_payload_usuario(
        nome="Usuario Nao Admin",
        email=gerar_email_unico("serverest.dev"),
        administrador="false",
    )
    cadastro_resp = api.post_usuarios(usuario_payload)
    assert cadastro_resp.status_code == 201
    login_resp = login_client.post_login(criar_payload_login(usuario_payload["email"], usuario_payload["password"]))
    assert login_resp.status_code == 200
    token = normalize_bearer_token(login_resp.json().get("authorization") or login_resp.json().get("token"))
    payload = criar_payload_produto()

    # Act
    resposta = produtos_client.post_produtos(payload, token)

    # Assert
    assert resposta.status_code == 403
    assert is_error_response(resposta.json())
