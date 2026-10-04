# Fase 00 — Setup

## Objetivo
Preparar um projeto Python moderno e organizado, ainda sem IA.

## Conceitos para estudar
- `uv`: projetos, `pyproject.toml`, lockfile, `uv add`, `uv run`
- Virtual environments (o que o uv faz por baixo)
- Estrutura de pacotes Python (`__init__.py`, imports absolutos)
- Variáveis de ambiente e `pydantic-settings`
- Git: `.gitignore`, commits pequenos

## Tarefas
- [ ] `uv init` e Python 3.12+
- [ ] Criar estrutura: `backend/ mcp_server/ agent/ tests/ docs/`
- [ ] `.gitignore` (incluindo `.env`), `.env.example`
- [ ] Módulo `backend/config.py` com `Settings` (pydantic-settings) lendo `DATABASE_URL`
- [ ] ruff + pytest configurados no `pyproject.toml`
- [ ] Um teste trivial passando
- [ ] README com "como rodar"

## Desafio obrigatório
Fazer `uv run python -m backend` imprimir a `DATABASE_URL` lida do `.env` — sem hardcode.

## Definição de pronto
- `uv sync && uv run pytest` funciona num clone limpo
- `.env` fora do Git
- README explica setup

## Perguntas de checagem
1. Qual a diferença entre `pyproject.toml` e `uv.lock`?
2. Por que configuração deve vir de variáveis de ambiente?

## Prompt sugerido
> Vamos começar a Fase 00. Leia @docs/phases/fase-00-setup.md, me explique os conceitos e proponha um plano. Depois de aprovarmos o plano, implemente passo a passo explicando cada parte.
