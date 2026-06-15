# ServeRest — Suíte de Testes API

Suite de testes automatizados (Pytest) para a API ServeRest, cobrindo recursos principais: `/usuarios`, `/login` e `/produtos`.

## Visão Geral

- **Objetivo**: validar fluxos de autenticação, operações CRUD e contratos de resposta (JSON Schema).
- **Status**: ✅ **25/25 testes passando** (tempo: 62.94s).
- **Cobertura de cenários**: 100% (25 cenários mapeados implementados e validados).

Para detalhes completos do plano de teste, veja [PLANO-DE-TESTES.md](PLANO-DE-TESTES.md).

## Requisitos

- Python 3.10+ (testado com Python 3.13.2)
- pip
- Recomendado: ambiente virtual

## Instalação

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar os testes

**Comando recomendado** (silencioso, sem warnings):

```bash
pytest -q --disable-warnings
```

**Com detalhes e verbose**:

```bash
pytest -vv
```

**Apenas um arquivo específico**:

```bash
pytest tests/test_login.py
pytest tests/test_produtos.py
pytest tests/test_usuarios.py
```

**Um teste específico**:

```bash
pytest tests/test_login.py::test_login_com_credenciais_validas_retorna_200_e_token
```

## Estrutura do Projeto

```
src/
  api/          # Clientes HTTP para chamar endpoints
  data/         # Geradores de payloads de teste
  helpers/      # Utilitários, normalizadores e validadores de JSON Schema
tests/
  conftest.py   # Fixtures e configurações
  test_login.py
  test_produtos.py
  test_usuarios.py
```

### Responsabilidades

- **`src/api/`**: encapsula chamadas HTTP (GET/POST/PUT/DELETE) para cada endpoint.
- **`src/data/`**: gera payloads reutilizáveis (ex.: dados de usuário, produto).
- **`src/helpers/`**: valida estruturas de resposta contra JSON Schema; normaliza tokens.
- **`tests/`**: casos de teste organizados por recurso; 25 cenários mapeados.

## Validação JSON Schema (Extra 1 implementado ✅)

A suíte valida a estrutura das respostas usando JSON Schema em **3+ endpoints**:

| Endpoint             | Teste                                                    | Schema                  |
| -------------------- | -------------------------------------------------------- | ----------------------- |
| `POST /login`        | `test_login_com_credenciais_validas_retorna_200_e_token` | `LOGIN_RESPONSE_SCHEMA` |
| `GET /produtos`      | `test_listar_produtos_retorna_200_e_lista`               | `PRODUTOS_LIST_SCHEMA`  |
| `GET /produtos/{id}` | `test_buscar_produto_por_id_valido_retorna_200`          | `PRODUTO_DETAIL_SCHEMA` |

**Localização dos schemas**: [src/helpers/schema_validators.py](src/helpers/schema_validators.py)

## Cobertura de Testes

- **Fórmula**: cobertura = `(cenários testados / cenários mapeados) × 100`.
- **Resultado**: `(25 / 25) × 100 = 100%` (cobertura de cenários).
- **Nota**: isso mede cobertura de cenários mapeados, não cobertura de linha/ramo do código.

Para medir cobertura de código (linhas/ramo), use `coverage.py`:

```bash
pip install coverage
coverage run -m pytest
coverage report -m
coverage html  # gera relatório em htmlcov/index.html
```

## Cenários fora do escopo

- Testes de performance/carga
- Testes de UI/browser
- Validação contratual OpenAPI completa (além da validação básica de schema)

## Configuração

- **Base URL padrão**: `https://compassuol.serverest.dev`
- **Credenciais de teste**: usadas via fixtures em `tests/conftest.py`
- Variáveis de ambiente: pode-se sobrescrever `BASE_URL` e credenciais conforme necessário.

## Executando na CI (GitHub Actions)

Exemplo mínimo de workflow:

```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: pytest -q --disable-warnings
```

## Observações

- O código foi simplificado e focado apenas no necessário para a suíte de testes.
- Todos os 25 testes estão implementados e passando.
- JSON Schema validation está implementado em múltiplos endpoints (Extra 1).
- Para adicionar novos testes, siga o padrão em `tests/` e atualize [PLANO-DE-TESTES.md](PLANO-DE-TESTES.md).
