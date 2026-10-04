# Fase 07 — Multi-tool Agent

## Objetivo
Resolver perguntas que exigem várias chamadas encadeadas (agent loop de verdade).

## Conceitos para estudar
- Agent loop: repetir enquanto `stop_reason == tool_use`
- Tool chaining e chamadas paralelas na mesma rodada
- Limite de iterações, timeouts
- Retries com backoff para falhas transitórias
- Ambiguidade: quando o agente deve perguntar ao usuário ("qual João?")

## Tarefas
- [ ] Loop com `MAX_TOOL_CALLS = 10`
- [ ] Suporte a múltiplos `tool_use` na mesma resposta
- [ ] Retry para erros transitórios do MCP/LLM
- [ ] Mensagem controlada quando o limite é atingido
- [ ] Trace no terminal: sequência de tools chamadas

## Exercícios
- "O pedido do João está atrasado?" (UC5) — com 2 Joãos no seed!
- "Quais notebooks abaixo de $1000 têm estoque?" (UC6)
- "Quais pedidos do João ainda estão pendentes?"
- "Quais produtos da categoria X estão sem estoque?"

## Desafio obrigatório
Quando houver dois clientes "João", o agente deve pedir esclarecimento em vez de chutar.

## Definição de pronto
Todos os exercícios respondidos corretamente; loop nunca passa do limite.

## Perguntas de checagem
1. Como o agente "sabe" que terminou?
2. Por que o limite de iterações é obrigatório em produção?

## Prompt sugerido
> Fase 07. Leia @docs/phases/fase-07-multi-tool.md. Revise meu agent loop atual e me diga o que precisa mudar.
