# PLANO-DE-TESTES

## Objetivo da suíte

Validar a funcionalidade e a estabilidade dos principais recursos da API ServeRest para os endpoints `/usuarios`, `/login` e `/produtos`.
A suíte deve garantir que os fluxos de cadastro, autenticação, autorização e gestão de produtos funcionem conforme o esperado.

## Estratégia

- Tipo de teste: testes funcionais de API REST.
- Camada: camada de integração leve, focada em serviços HTTP expostos pela API.
- Ferramentas: Python, Pytest, Requests e JsonSchema para validação de payloads/respostas.
- Abordagem: usar clients para encapsular chamadas HTTP, geradores de payloads para dados dinâmicos e fixtures para isolamento e teardown.

## Escopo

### Coberto

- `/usuarios`: listagem, cadastro, busca por ID, atualização e exclusão.
- `/login`: autenticação com credenciais válidas, tratamento de credenciais inválidas e validação de campos obrigatórios.
- `/produtos`: listagem pública, criação com token de usuário admin, busca por ID, atualização, exclusão e controle de permissões.

### Fora do escopo

- Testes de UI ou browser.
- Testes de performance/carga.
- Testes de contrato OpenAPI completos além da validação de schema básica.
- Endpoints e recursos que não sejam `/usuarios`, `/login` ou `/produtos`.

## Cenários a implementar

### /usuarios

1. `test_listar_usuarios_retorna_200_e_lista`
2. `test_cadastrar_usuario_valido_retorna_201_e_dados`
3. `test_cadastrar_usuario_com_email_duplicado_retorna_400`
4. `test_cadastrar_sem_campo_obrigatorio_retorna_400`
5. `test_buscar_usuario_por_id_valido_retorna_200`
6. `test_buscar_usuario_por_id_inexistente_retorna_400`
7. `test_atualizar_usuario_existente_retorna_200`
8. `test_atualizar_usuario_inexistente_cria_novo_retorna_201`
9. `test_deletar_usuario_existente_retorna_200`
10. `test_deletar_usuario_inexistente_retorna_200_com_mensagem`

### /login

1. `test_login_com_credenciais_validas_retorna_200_e_token`
2. `test_login_com_senha_errada_retorna_401`
3. `test_login_com_email_inexistente_retorna_401`
4. `test_login_com_campos_vazios_retorna_400`
5. `test_login_retorna_bearer_token_no_body`

### /produtos

1. `test_listar_produtos_retorna_200_e_lista`
2. `test_cadastrar_produto_valido_com_token_admin_retorna_201`
3. `test_cadastrar_produto_sem_token_retorna_401`
4. `test_cadastrar_produto_nome_duplicado_retorna_400`
5. `test_buscar_produto_por_id_valido_retorna_200`
6. `test_buscar_produto_por_id_inexistente_retorna_400`
7. `test_atualizar_produto_existente_retorna_200`
8. `test_excluir_produto_existente_retorna_200`
9. `test_excluir_produto_inexistente_retorna_200_com_mensagem`
10. `test_cadastrar_produto_com_token_nao_admin_retorna_403`

## Critérios de qualidade

Um teste estará pronto quando:

- seguir o padrão AAA: Arrange, Act, Assert.
- ser independente e não depender de outros testes.
- usar dados dinâmicos para evitar valores hardcoded.
- possuir teardown automático via fixtures com `yield` quando criar dados persistentes.
- validar o `status_code` e ao menos um campo relevante do corpo da resposta.
- incluir validação de schema JSON em endpoints críticos quando aplicável.
- poder ser executado isoladamente por módulo.
- estar registrado e documentado no plano de testes.
