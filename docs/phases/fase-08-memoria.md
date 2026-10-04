# Fase 08 — Memória

## Objetivo
Manter contexto entre mensagens e entre sessões.

## Conceitos para estudar
- Memória de curto prazo (histórico da sessão) vs longo prazo
- Session ID
- Redis: estruturas, TTL
- Janela de contexto: truncar, resumir
- Agent API com FastAPI (o agente sai do CLI)

## Tarefas
- [ ] Interface `MemoryStore` com implementação em memória e em Redis
- [ ] Agent API: `POST /sessions`, `POST /sessions/{id}/messages`, `GET /sessions/{id}`
- [ ] Persistir histórico (incluindo tool calls/results) por sessão
- [ ] Estratégia para conversas longas (truncar ou resumir)

## Desafio obrigatório
UC7: "Procure notebooks Lenovo." → "Somente abaixo de $1000." deve refinar a busca anterior,
inclusive depois de reiniciar a API (Redis).

## Definição de pronto
Sessões isoladas, persistentes e com limite de contexto tratado.

## Perguntas de checagem
1. O que exatamente precisa ser salvo para retomar uma conversa com tools?
2. Trade-offs entre truncar e resumir histórico?

## Prompt sugerido
> Fase 08. Leia @docs/phases/fase-08-memoria.md. Me explique as opções de memória e vamos desenhar a interface MemoryStore.
