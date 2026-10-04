# Fase 05 — Tool calling (tools locais)

## Objetivo
Ensinar o LLM a pedir a execução de funções Python locais. Ainda sem MCP.

## Conceitos para estudar
- Definição de tools (nome, descrição, JSON Schema)
- Resposta do modelo com `tool_use` e `stop_reason`
- Devolver `tool_result` com o `tool_use_id` correto
- O ciclo: User → LLM → tool call → função → resultado → LLM → resposta
- Escolha de tool: `auto`, forçada, nenhuma

## Tarefas
- [ ] 2 tools locais fake (`search_products`, `get_order`) com dados em memória
- [ ] Gerar o schema da tool a partir de um modelo Pydantic
- [ ] Loop de uma rodada: executar tool, devolver resultado, obter resposta final
- [ ] Imprimir no terminal qual tool foi escolhida e com quais argumentos

## Desafio obrigatório
"Find Lenovo laptops under $1000." deve gerar
`search_products(query="Lenovo laptop", max_price=1000)` — e você deve conseguir explicar
**por que** o modelo escolheu esses argumentos (descrição + schema).

## Definição de pronto
O agente escolhe a tool certa para pelo menos 5 perguntas diferentes e responde sem tool quando não precisa.

## Perguntas de checagem
1. Quem executa a função: o LLM ou o seu código?
2. O que acontece se a descrição da tool for ruim?

## Prompt sugerido
> Fase 05. Leia @docs/phases/fase-05-tool-calling.md. Me mostre o formato das mensagens de tool_use/tool_result antes de eu implementar.
