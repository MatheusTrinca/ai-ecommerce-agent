# Fase 06 — Agent + MCP ⭐ (MVP)

## Objetivo
Substituir as tools locais pelas tools do MCP Server. Este é o coração do projeto.

## Conceitos para estudar
- Converter `list_tools()` do MCP no formato de tools do LLM
- Rotear `tool_use` do LLM para `mcp_client.call_tool()`
- Converter resultado MCP em `tool_result`
- Descoberta dinâmica: o agente não conhece as tools em tempo de compilação

## Tarefas
- [ ] `agent/agent.py`: classe `Agent` que recebe um `MCPClient` e um `LLM`
- [ ] Adaptador MCP tool → schema do LLM
- [ ] Executar tool calls via MCP e devolver resultado
- [ ] Erros de tool (`isError`) repassados ao LLM de forma que ele consiga se recuperar
- [ ] CLI de chat com o agente

## Desafio obrigatório
Adicionar uma tool nova no MCP Server e o agente passar a usá-la **sem mudar nenhuma linha do agente**.

## Definição de pronto
- UC1, UC2 e UC3 do PRD respondidos com dados reais do banco
- `LLM → MCP Client → MCP Server → Database → LLM` funcionando

## Perguntas de checagem
1. O que o MCP trouxe de vantagem em relação à Fase 05?
2. Onde está o acoplamento entre agente e tools agora?

## Prompt sugerido
> Fase 06. Leia @docs/phases/fase-06-agent-mcp.md. Vamos desenhar juntos a classe Agent antes de codar.
