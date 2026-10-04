# Fase 12 — Observabilidade

## Objetivo
Saber exatamente o que o agente fez, quanto custou e onde falhou.

## Conceitos para estudar
- Logging estruturado (JSON)
- Tracing: spans e propagação de request_id
- Métricas: latência, tokens, erros, tools mais usadas
- OpenTelemetry (opcional), Langfuse (opcional)

## Tarefas
- [ ] Logs estruturados com request_id e session_id em todas as camadas
- [ ] Span por chamada de LLM e por tool call (args, resultado resumido, latência)
- [ ] Contagem de tokens e custo estimado por request
- [ ] Endpoint ou comando para ver o trace de um request

## Desafio obrigatório
Dado um request_id, reconstruir toda a cadeia: pergunta → decisões → tools → argumentos → resultados → resposta.

## Definição de pronto
Qualquer resposta do agente é explicável pelo trace.

## Prompt sugerido
> Fase 12. Leia @docs/phases/fase-12-observabilidade.md. Proponha o formato dos logs e dos spans.
