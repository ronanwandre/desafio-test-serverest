# ServeRest API Testes

Suite de testes em Python para a API ServeRest, cobrindo `/usuarios`, `/login` e `/produtos`.

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Executar

Execute a suíte completa (modo silencioso, sem warnings):

```bash
pytest -q --disable-warnings
```

## Projeto

- `src/api`: clientes HTTP
- `src/data`: geradores de payloads
- `src/helpers`: utilitários e validações de schema
- `tests`: casos de teste Pytest

## Execução por módulo

```bash
pytest tests/test_login.py
pytest tests/test_produtos.py
pytest tests/test_usuarios.py
```

## Cobertura de testes

- Método: cobertura medida como `cenários testados / cenários mapeados × 100`.
- Cenários implementados: 25
- Cenários mapeados: 25
- Cobertura total estimada: **100%**
- Resultado verificado: `25 passed` com `pytest -q --disable-warnings`

### Cenários fora do escopo

- Testes de performance/carga
- Testes de interface gráfica (UI/browser)
- Validação contratual OpenAPI completa além da validação básica de schema

## Observações

- Base URL: `https://compassuol.serverest.dev`
- O código foi simplificado para manter apenas o necessário para a suíte de testes.
