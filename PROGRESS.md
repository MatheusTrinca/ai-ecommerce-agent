# Progresso

Legenda: ⬜ não iniciada · 🟨 em andamento · ✅ concluída

| Fase | Tema | Status |
|---|---|---|
| 00 | Setup | ✅ |
| 01 | Backend e-commerce | ⬜ |
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
