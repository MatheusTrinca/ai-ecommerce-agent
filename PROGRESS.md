# Progresso

Legenda: ⬜ não iniciada · 🟨 em andamento · ✅ concluída

| Fase | Tema | Status |
|---|---|---|
| 00 | Setup | ✅ |
| 01 | Backend e-commerce | ✅ |
| 02 | MCP Server | ⬜ |
| 03 | MCP Client | ⬜ |
| 04 | Primeiro LLM | ⬜ |
| 05 | Tool calling (local) | ⬜ |
| 06 | Agent + MCP ⭐ MVP | ⬜ |
| 07 | Multi-tool agent | ⬜ |
| 08 | Memória | ⬜ |
| 09 | RAG | ⬜ |
| 10 | Write tools + aprovação humana | ⬜ |
| 11 | Testes | ⬜ |
| 12 | Observabilidade | ⬜ |
| 13 | Docker | ⬜ |
| 14 | Projeto final + comparação com framework | ⬜ |

## Diário de aprendizado
<!-- Ao fim de cada fase, o Claude Code adiciona uma entrada aqui. -->

### Fase 00 — Setup (2026-10-03)
- **O que construí:** projeto `uv` inicializado (git + `pyproject.toml`), pacotes `backend/`, `mcp_server/`,
  `agent/`, `tests/`; `backend/config.py` com `Settings` (pydantic-settings) lendo `DATABASE_URL` do `.env`;
  `backend/__main__.py` (desafio obrigatório); `ruff` e `pytest` configurados no `pyproject.toml`
  (incluindo `pythonpath = ["."]`); primeiro teste real (`tests/test_config.py`); `.gitignore`, `.env.example`
  e `README.md`.
- **O que aprendi:**
  - Diferença `pyproject.toml` (intenção/ranges de versão) vs `uv.lock` (resolução exata, travada, com hash).
  - `uv add` vs `uv add --dev` — dependências de runtime vs de desenvolvimento.
  - `python -m pacote` adiciona o diretório atual ao `sys.path` automaticamente; `pytest` não — por isso
    precisou do `pythonpath = ["."]` no `[tool.pytest.ini_options]` pra `tests/` conseguir importar `backend`.
  - Por que config vem de variável de ambiente: segurança (segredo não vai pro histórico do git) +
    flexibilidade entre ambientes (mesmo código, `.env` diferente por ambiente) — princípio do 12-factor app.
- **Decisões tomadas e por quê:**
  - `pytest-asyncio` não foi adicionado ainda (não há código assíncrono nesta fase); entra quando for
    necessário (Fase 01+).
  - `.env.example`/`.env` já no formato `postgresql+asyncpg://...` (driver async), adiantando o formato que
    será usado na Fase 01.
- **Dúvidas em aberto:**
  - Postgres local via Docker (sem instalação nativa) — anotado como pré-requisito da Fase 01
    (`docs/phases/fase-01-backend.md`, imagem `postgres:16` já disponível localmente).

### Fase 01 — Backend e-commerce (2026-10-04)
- **O que construí:** `docker-compose.yml` (Postgres local); `backend/db/base.py` (`DeclarativeBase`) e
  `backend/db/session.py` (engine async, `AsyncSessionLocal`, `get_db()`); os 5 models (`Customer`,
  `Category`, `Product`, `Order`, `OrderItem`) com `Mapped`/`mapped_column` e `relationship()`s
  bidirecionais; Alembic inicializado (`-t async`) e primeira migration aplicada; `backend/seed.py`
  (reproduzível via `TRUNCATE ... RESTART IDENTITY CASCADE`) com os dados obrigatórios do PRD; 4
  repositories (`Customer`, `Category`, `Order`, `Product` — o `ProductRepository.search` foi o desafio
  obrigatório); 5 schemas Pydantic de leitura; 3 services (`Customer`, `Order`, `Product`) + exceção de
  domínio `NotFoundError`; 3 routers + `backend/main.py` (lifespan + exception handler global); banco de
  teste (`ai_commerce_agent_test`) + `tests/conftest.py` + 3 arquivos de teste (10 testes, todos passando).
- **O que aprendi:**
  - `Mapped`/`mapped_column` (SQLAlchemy 2.0) tipam a coluna tanto pro Python quanto pro banco, substituindo
    o `Column()` antigo sem tipagem.
  - `expire_on_commit=False` no `async_sessionmaker` evita que o SQLAlchemy tente relançar uma query
    síncrona (lazy load) depois de um commit, o que quebraria em contexto async.
  - `relationship()` entre models que se referenciam mutuamente precisa de `TYPE_CHECKING` + forward
    reference em string (`Mapped["Order"]`) pra evitar import circular — mas isso só funciona de verdade se
    *alguém* garantir que todos os models foram importados antes do primeiro uso. Resolvido fazendo
    `backend/models/__init__.py` importar todas as classes (importar qualquer submódulo do pacote já
    dispara isso).
  - `sqlalchemy.Enum(PyEnum, native_enum=False)` dá tipagem/validação Python num enum sem criar um tipo
    `ENUM` nativo do Postgres — meio-termo entre "string crua" e "enum nativo com `ALTER TYPE` chato".
  - `selectinload()` é obrigatório (não opcional) pra relacionamentos que vão ser lidos depois da query, em
    contexto async — acessar uma relação não carregada fora de um `await` quebra (`MissingGreenlet`).
  - Pydantic v2 `ConfigDict(from_attributes=True)` + schemas aninhados permite validar uma árvore de objetos
    SQLAlchemy inteira (`Order` → `items` → `product`) de uma vez, desde que os relacionamentos envolvidos já
    estejam carregados.
  - FastAPI usa `response_model=` pra converter o retorno da rota — o router pode devolver o objeto do
    SQLAlchemy direto, sem chamar `Schema.model_validate()` manualmente.
  - Erro de domínio (`NotFoundError`) + `@app.exception_handler(...)` centraliza a tradução "erro de negócio
    → HTTP 404" num único lugar, em vez de `try/except` repetido em cada rota.
  - **Bug real encontrado e corrigido:** `pytest-asyncio` cria um event loop novo por teste (escopo
    "function") por padrão; como o engine de teste é criado numa fixture de escopo "session", a conexão
    asyncpg nascia num loop e era reusada em outro, corrompendo a transação (`cannot rollback; the
    transaction is in error state`). Corrigido fixando `asyncio_default_fixture_loop_scope` e
    `asyncio_default_test_loop_scope` como `"session"` no `pyproject.toml`.
  - `ruff` com a regra `B008` (bugbear) marca `Depends(...)` em default de parâmetro como erro — é falso
    positivo pra código FastAPI (é o padrão oficial da lib). Ignorado via `[tool.ruff.lint] ignore = ["B008"]`.
- **Decisões tomadas e por quê:**
  - `Order.status` como `String` + `enum.Enum` Python (via `sqlalchemy.Enum(..., native_enum=False)`), não
    enum nativo do Postgres — evita `ALTER TYPE` em migrations futuras ao custo de constraint só em Python.
  - Testes async com `@pytest.mark.asyncio` explícito (não `asyncio_mode = "auto"`) — mais visível sobre o
    que roda em loop de eventos.
  - Filtro `category` em `/products` por **nome** (resolvido pra `id` no `ProductService`), não por id — API
    mais amigável; categoria inexistente devolve lista vazia, não erro (é tratado como "sem resultados").
  - `docker-compose.yml` criado já nesta fase (Postgres isolado) como atalho de infraestrutura, mesmo sendo
    tema formal da Fase 13 — decisão do usuário, avisado do trade-off de aprendizado antes de seguir.
  - Desafio obrigatório (`ProductRepository.search`) foi implementado pelo Claude a pedido explícito do
    usuário, pulando a prática hands-on — avisado antes de executar.
  - Perguntas de checagem da fase foram respondidas pelo Claude a pedido do usuário, não pelo usuário.
- **Dúvidas em aberto:**
  - `ProductRead` expõe só `category_id` (sem objeto `Category` aninhado) — considerar enriquecer se algum
    caso de uso futuro precisar do nome da categoria direto na resposta de produto.
  - Nenhum `ondelete` explícito nas foreign keys (comportamento padrão do Postgres = `NO ACTION`) — revisitar
    se alguma fase futura precisar de regras de cascata (ex.: cancelar cliente deveria afetar pedidos?).
