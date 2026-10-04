# Fase 03 — MCP Client próprio

## Objetivo
Entender MCP do lado de quem consome: conectar, descobrir e chamar tools — sem LLM.

## Conceitos para estudar
- `ClientSession`, `stdio_client` do SDK `mcp`
- Handshake `initialize`, capabilities
- `list_tools`, `call_tool`, `list_resources`, `read_resource`
- Async context managers e ciclo de vida da conexão
- Formato do resultado (`content`, `structuredContent`, `isError`)

## Tarefas
- [ ] Classe `MCPClient` em `agent/mcp_client.py` com `connect()`, `list_tools()`, `call_tool()`, `close()`
- [ ] CLI `uv run python -m agent.cli_client`:
  - lista tools com descrição
  - permite chamar uma tool digitando nome + argumentos (JSON)
- [ ] Tratamento de erros: tool inexistente, argumentos inválidos, servidor caído
- [ ] Testes do client (pode subir o server em subprocesso)

## Desafio obrigatório
Fazer o CLI validar os argumentos contra o `inputSchema` da tool **antes** de enviar.

## Definição de pronto
`Client → MCP → Server → Database → Result` funcionando pelo terminal, sem nenhum LLM.

## Perguntas de checagem
1. O que acontece, em mensagens JSON-RPC, quando você chama `call_tool`?
2. Quem é responsável por iniciar o processo do server no transport stdio?
3. Por que o client precisa do `inputSchema`?

## Prompt sugerido
> Fase 03. Leia @docs/phases/fase-03-mcp-client.md. Me explique o handshake MCP e me dê o esqueleto da classe MCPClient com TODOs.
