# ai-commerce-agent

Projeto de estudo: agente de IA para operações de e-commerce, construído em fases incrementais
(Python + MCP + LLM). Ver `docs/PRD.md` e `docs/phases/` para o roteiro completo.

## Como rodar

Pré-requisitos: [uv](https://docs.astral.sh/uv/) instalado, Python 3.12+ (o `uv` resolve isso automaticamente).

1. Copie `.env.example` para `.env` e ajuste os valores:
   ```
   cp .env.example .env
   ```
2. Instale as dependências:
   ```
   uv sync
   ```
3. Rode os testes:
   ```
   uv run pytest
   ```
4. Rode o lint:
   ```
   uv run ruff check .
   ```
5. Rode o módulo `backend` (hoje, só imprime a `DATABASE_URL` lida do `.env`):
   ```
   uv run python -m backend
   ```

## Status

Ver `PROGRESS.md` para o progresso por fase.
