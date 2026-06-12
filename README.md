# 🧪 Testes Automatizados - ServeRest API (Usuários)

[![Python](https://img.shields.io/badge/Python-3.13-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4+-0a9edc?logo=pytest)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Suíte completa de testes automatizados em Python + Pytest para o endpoint `/usuarios` da [API ServeRest](https://compassuol.serverest.dev/). Este projeto demonstra boas práticas de testes de API, padrões de design e qualidade de código.

## 📋 Índice

- [Características](#características)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes Implementados](#testes-implementados)
- [Boas Práticas](#boas-práticas)
- [Arquitetura](#arquitetura)
- [Contribuição](#contribuição)

## ✨ Características

- ✅ **10 testes abrangentes** cobrindo cenários de sucesso e erro
- ✅ **Client abstrato** para isolamento de dependências HTTP
- ✅ **Fixtures reutilizáveis** com teardown automático
- ✅ **Geração dinâmica de dados** sem hardcoding
- ✅ **Padrão AAA** (Arrange, Act, Assert) em todos os testes
- ✅ **Sem sleep ou timeouts** desnecessários
- ✅ **Configuração limpa** via `pytest.ini`

## 🔧 Pré-requisitos

- **Python** 3.10+
- **pip** (gerenciador de pacotes)

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/testes-serverest.git
cd testes-serverest
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> **Nota Windows:** Se receber erro de execução de scripts, use: `py -m pytest` diretamente, sem ativar o ambiente.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### Rodar todos os testes

```bash
pytest
```

**Saída esperada:**

```
============================= test session starts ==============================
collected 10 items

tests/test_usuarios.py ..........                                        [100%]

============================== 10 passed in XX.XXs =============================
```

### Rodar com modo verbose

```bash
pytest -v
```

### Rodar um teste específico

```bash
pytest tests/test_usuarios.py::test_cadastrar_usuario_valido_retorna_201_e_dados -v
```

### Rodar com cobertura (se instalado)

```bash
pip install pytest-cov
pytest --cov=src
```

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── api/
│   │   └── usuarios_client.py      # Cliente HTTP para /usuarios
│   ├── helpers/
│   │   └── utils.py                # Funções utilitárias (emails, etc)
│   └── data/
│       └── usuarios_data.py        # Construtores de payloads
├── tests/
│   ├── conftest.py                 # Fixtures pytest
│   └── test_usuarios.py            # Suite de testes (10 cenários)
├── pytest.ini                      # Configuração pytest
├── requirements.txt                # Dependências
└── README.md                       # Este arquivo
```

## 🧬 Testes Implementados

| Teste                                                | Descição                         | Esperado                 |
| ---------------------------------------------------- | -------------------------------- | ------------------------ |
| `test_cadastrar_usuario_valido_retorna_201_e_dados`  | Cadastro com dados válidos       | 201 + dados retornados   |
| `test_listar_usuarios_retorna_200`                   | Listar todos os usuários         | 200 + array              |
| `test_listar_usuarios_com_filtro_retorna_200`        | Listar com filtro por nome       | 200 + resultado filtrado |
| `test_listar_usuario_por_id_retorna_200`             | Obter usuário por ID             | 200 + dados do usuário   |
| `test_listar_usuario_id_inexistente_retorna_400`     | ID inválido                      | 400 + mensagem erro      |
| `test_atualizar_usuario_valido_retorna_200`          | Atualizar dados do usuário       | 200 + confirmação        |
| `test_atualizar_usuario_inexistente_retorna_400`     | Atualizar usuário que não existe | 400                      |
| `test_deletar_usuario_retorna_200`                   | Deletar usuário                  | 200 + confirmação        |
| `test_deletar_usuario_inexistente_retorna_400`       | Deletar usuário inexistente      | 400                      |
| `test_cadastrar_usuario_email_duplicado_retorna_400` | Email já registrado              | 400                      |

## 🏆 Boas Práticas Implementadas

### Padrão AAA (Arrange, Act, Assert)

```python
def test_exemplo(api):
    # Arrange: Preparar dados
    usuario = criar_payload_usuario()

    # Act: Executar ação
    resposta = api.criar_usuario(usuario)

    # Assert: Validar resultado
    assert resposta.status_code == 201
```

### Fixtures com Teardown

```python
@pytest.fixture
def usuario_criado(api):
    usuario = criar_payload_usuario()
    resposta = api.criar_usuario(usuario)
    usuario_id = resposta.json()["_id"]

    yield usuario_id  # Teste usa o ID

    # Limpeza automática após o teste
    api.deletar_usuario(usuario_id)
```

### Dados Dinâmicos

```python
def gerar_email_unico() -> str:
    return f"user_{uuid4().hex[:8]}@serverest.dev"
```

## 🏗️ Arquitetura

### Client Abstrato (`usuarios_client.py`)

Encapsula toda a lógica HTTP, permitindo mudanças na API sem afetar os testes:

```python
class UsuariosClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def criar_usuario(self, dados: dict) -> requests.Response:
        return requests.post(f"{self.base_url}/usuarios", json=dados)

    def listar_usuarios(self, filtro: dict = None) -> requests.Response:
        return requests.get(f"{self.base_url}/usuarios", params=filtro)
```

### Dados de Teste (`usuarios_data.py`)

Centraliza a construção de payloads:

```python
def criar_payload_usuario(**kwargs) -> dict:
    return {
        "nome": "Usuario Teste",
        "email": gerar_email_unico(),
        "password": "123456",
        "administrador": "false",
        **kwargs
    }
```

## 💡 Padrões de Teste

- **Independência:** Cada teste cria seus próprios dados
- **Idempotência:** Testes podem rodar múltiplas vezes
- **Limpeza automática:** Fixtures fazem teardown com `yield`
- **Sem esperas:** Nenhum `time.sleep()` desnecessário
- **Nomes descritivos:** Claro o que cada teste valida

## 🔗 Links Úteis

- [API ServeRest](https://compassuol.serverest.dev/)
- [Documentação Pytest](https://docs.pytest.org/)
- [Documentação Requests](https://requests.readthedocs.io/)
- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)

---
