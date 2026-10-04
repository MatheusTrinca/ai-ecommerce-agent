# CLAUDE.md — AI E-commerce Agent (projeto de estudo)

## Contexto
Este é um projeto de ESTUDO. O objetivo principal não é entregar o produto rápido, e sim que o Matheus
aprenda MCP, agentes de IA e backend Python construindo tudo de forma incremental, fase por fase.

- PRD completo: @docs/PRD.md
- Fases: `docs/phases/fase-XX-*.md`
- Progresso: @PROGRESS.md

## Regras de trabalho (obrigatórias)
1. **Uma fase por vez.** Só trabalhe na fase indicada pelo usuário. Nunca implemente nada de fases futuras,
   mesmo que pareça "óbvio" ou "rápido".
2. **Comece sempre em plan mode.** Leia o arquivo da fase, explique os conceitos e proponha um plano de
   passos pequenos antes de escrever qualquer código.
3. **Ensine antes de codar.** Para cada conceito novo, explique o "porquê" em poucas linhas, com um exemplo
   mínimo. Relacione com o que já foi construído nas fases anteriores.
4. **Claude escreve o código, em passos pequenos e explicados.** Depois que o plano for aprovado, implemente
   um passo por vez (um arquivo ou uma responsabilidade por vez). Para cada passo:
   - explique o que o código faz e por que foi escrito assim (decisões, alternativas);
   - destaque as linhas mais importantes para o aprendizado;
   - pare e deixe o usuário rodar, testar e perguntar antes de seguir para o próximo passo.
   Exceção: no **desafio obrigatório** de cada fase, o usuário tenta primeiro; dê dicas progressivas e só
   mostre a solução completa se ele pedir.
5. **Revise como um sênior.** Quando o usuário escrever ou alterar código, revise: bugs, design,
   nomes, tipagem, testes. Seja honesto e direto.
6. **Feche a fase com verificação.** Antes de considerar a fase concluída:
   - confira cada item da "Definição de pronto";
   - faça as "Perguntas de checagem" da fase para o usuário responder;
   - atualize o PROGRESS.md (status + aprendizados + dúvidas em aberto).
7. **Sem frameworks de agente** (LangChain, LangGraph, CrewAI etc.) até a Fase 14. O agent loop, o MCP client
   e o tool calling são feitos "na mão" de propósito.
8. Se o usuário pedir para pular algo, avise o que ele perde de aprendizado, mas respeite a decisão.

## Stack
- Python 3.12+, gerenciado com `uv`
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (async) + Alembic + PostgreSQL
- MCP: SDK oficial `mcp` (Python), começando com FastMCP
- LLM: Anthropic SDK (`anthropic`) — pode ser trocado, mas mantenha o código desacoplado do provedor
- Redis (memória), pgvector (RAG; Qdrant opcional)
- pytest + pytest-asyncio, ruff, mypy (opcional)
- Docker / docker compose

## Convenções
- Arquitetura em camadas: `router → service → repository → model`. Nada de SQL em routers ou em tools MCP.
- Type hints em tudo; schemas Pydantic para entrada/saída.
- Configuração via variáveis de ambiente (`.env`, nunca commitado; manter `.env.example` atualizado).
- Commits pequenos, mensagem no formato `fase-XX: descrição`.
- Cada fase termina com testes passando para o que foi construído nela.

## Comandos (atualizar conforme o projeto evolui)
- Instalar deps: `uv sync`
- Rodar API: `uv run uvicorn backend.main:app --reload`
- Testes: `uv run pytest`
- Lint: `uv run ruff check .`
