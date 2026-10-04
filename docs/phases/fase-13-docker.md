# Fase 13 — Docker

## Objetivo
Subir tudo com um comando.

## Conceitos para estudar
- Dockerfile multi-stage com uv
- docker compose: serviços, redes, volumes, healthchecks, `depends_on`
- MCP Server via Streamable HTTP entre containers (em vez de stdio)

## Tarefas
- [ ] Dockerfiles: backend, mcp-server, agent-api
- [ ] Compose: agent-api, mcp-server, backend, postgres (com pgvector), redis
- [ ] Migrations + seed + ingestão RAG automáticos na subida
- [ ] Healthchecks

## Desafio obrigatório
Trocar o transport do MCP para HTTP e o agente continuar funcionando só mudando configuração.

## Definição de pronto
Clone limpo + `.env` + `docker compose up` → todos os UCs do PRD funcionam.

## Prompt sugerido
> Fase 13. Leia @docs/phases/fase-13-docker.md. Me explique o Dockerfile com uv antes de escrevermos.
