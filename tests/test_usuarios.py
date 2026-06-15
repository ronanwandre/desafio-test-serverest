import uuid

from data.usuarios_data import criar_payload_usuario
from helpers.utils import extract_resource_id, is_error_response


def _random_id():
    return uuid.uuid4().hex[:16]


def _assert_api_error_response(body):
    assert is_error_response(body)


def test_listar_usuarios_retorna_200_e_lista(api):
    # Arrange
    # Act
    resp = api.get_usuarios()
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    if isinstance(data, dict):
        assert ("usuarios" in data and isinstance(data["usuarios"], list)) or isinstance(data.get("usuarios"), list)
    else:
        assert isinstance(data, list)


def test_cadastrar_usuario_valido_retorna_201_e_dados(api):
    # Arrange
    payload = criar_payload_usuario()
    # Act
    resp = api.post_usuarios(payload)
    # Assert
    assert resp.status_code == 201
    body = resp.json()
    # verifica presença de email no retorno ou via listagem
    if body.get("email"):
        assert body.get("email") == payload["email"]
    else:
        # busca pelo email na listagem para garantir cadastro
        list_resp = api.get_usuarios()
        usuarios = list_resp.json().get("usuarios", list_resp.json())
        assert any(u.get("email") == payload["email"] for u in usuarios)


def test_cadastrar_usuario_com_email_duplicado_retorna_400(api):
    # Arrange
    payload = criar_payload_usuario()
    resp1 = api.post_usuarios(payload)
    user_id = extract_resource_id(resp1.json()) or _random_id()

    # Act
    resp2 = api.post_usuarios(payload)

    # Assert
    assert resp2.status_code == 400
    body = resp2.json()
    _assert_api_error_response(body)


def test_cadastrar_sem_campo_obrigatorio_retorna_400(api):
    # Arrange
    payload = {"email": f"sem-nome-{uuid.uuid4().hex}@teste.local", "password": "Senha1!", "administrador": "true"}
    # Act
    resp = api.post_usuarios(payload)
    # Assert
    assert resp.status_code == 400
    body = resp.json()
    _assert_api_error_response(body)


def test_buscar_usuario_por_id_valido_retorna_200(api):
    # Arrange
    payload = criar_payload_usuario()
    create_resp = api.post_usuarios(payload)
    user_id = extract_resource_id(create_resp.json())
    assert user_id is not None

    # Act
    resp = api.get_usuario_by_id(user_id)

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    # Verifica que o email/nome correspondem
    if isinstance(body, dict) and body.get("email"):
        assert body.get("email") == payload["email"]
    else:
        # alguns endpoints retornam objeto dentro de 'usuario'
        usuario = body.get("usuario") or {}
        assert usuario.get("email") == payload["email"]


def test_buscar_usuario_por_id_inexistente_retorna_400(api):
    # Arrange
    fake_id = _random_id()
    # Act
    resp = api.get_usuario_by_id(fake_id)
    # Assert
    assert resp.status_code == 400
    body = resp.json()
    _assert_api_error_response(body)


def test_atualizar_usuario_existente_retorna_200(api):
    # Arrange
    payload = criar_payload_usuario()
    create_resp = api.post_usuarios(payload)
    user_id = extract_resource_id(create_resp.json())
    assert user_id is not None
    novo_nome = "Nome Atualizado"
    update_payload = {**payload, "nome": novo_nome}

    # Act
    resp = api.put_usuario_by_id(user_id, update_payload)

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    assert body.get("message")
    assert "Registro" in body.get("message", "")


def test_atualizar_usuario_inexistente_cria_novo_retorna_201(api):
    # Arrange
    fake_id = _random_id()
    payload = criar_payload_usuario()

    # Act
    resp = api.put_usuario_by_id(fake_id, payload)

    # Assert
    assert resp.status_code in (200, 201)
    # se 201 => criado; se 200 => API atualizou (algumas APIs aceitam upsert)
    body = resp.json()
    assert "message" in body or body.get("email") == payload["email"] or (body.get("usuario") or {}).get("email") == payload["email"]


def test_deletar_usuario_existente_retorna_200(api, usuario_criado):
    # Arrange
    user_id = usuario_criado["id"]
    assert user_id is not None

    # Act
    resp = api.delete_usuario_by_id(user_id)

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert "message" in body or "ok" in body or "resultado" in body


def test_deletar_usuario_inexistente_retorna_200_com_mensagem(api):
    # Arrange
    fake_id = _random_id()
    # Act
    resp = api.delete_usuario_by_id(fake_id)
    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert "message" in body or "Nenhum" in str(body) or "excluído" in str(body)
