try:
    from jsonschema import ValidationError, validate
    _JSONSCHEMA_AVAILABLE = True
except ImportError:  # pragma: no cover - fallback for environments without jsonschema
    _JSONSCHEMA_AVAILABLE = False

    class ValidationError(Exception):
        pass

    def validate(instance, schema):
        raise AssertionError(
            "Dependência 'jsonschema' não encontrada. Instale as dependências: `pip install -r requirements.txt`"
        )


USUARIOS_LIST_SCHEMA = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "usuarios": {"type": "array"},
            },
            "required": ["usuarios"],
            "additionalProperties": True,
        },
        {
            "type": "array",
        },
    ]
}

LOGIN_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "authorization": {"type": "string"},
        "token": {"type": "string"},
    },
    "oneOf": [
        {"required": ["authorization"]},
        {"required": ["token"]},
    ],
    "additionalProperties": True,
}

PRODUTOS_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "produtos": {"type": "array"},
    },
    "required": ["produtos"],
    "additionalProperties": True,
}

PRODUTO_DETAIL_SCHEMA = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "produto": {
                    "type": "object",
                    "properties": {
                        "_id": {"type": "string"},
                        "nome": {"type": "string"},
                        "preco": {"type": ["number", "integer"]},
                        "descricao": {"type": "string"},
                        "quantidade": {"type": "integer"},
                    },
                    "required": ["_id", "nome", "preco", "descricao", "quantidade"],
                    "additionalProperties": True,
                }
            },
            "required": ["produto"],
            "additionalProperties": True,
        },
        {
            "type": "object",
            "properties": {
                "_id": {"type": "string"},
                "nome": {"type": "string"},
                "preco": {"type": ["number", "integer"]},
                "descricao": {"type": "string"},
                "quantidade": {"type": "integer"},
            },
            "required": ["_id", "nome", "preco", "descricao", "quantidade"],
            "additionalProperties": True,
        },
    ]
}


def validar_schema_json(dados: dict, schema: dict) -> None:
    try:
        validate(instance=dados, schema=schema)
    except ValidationError as exc:
        # jsonschema.ValidationError has .message on older versions; guard generically
        msg = getattr(exc, "message", str(exc))
        raise AssertionError(f"Validação de schema falhou: {msg}") from exc
