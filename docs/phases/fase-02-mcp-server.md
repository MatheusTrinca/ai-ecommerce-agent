# Fase 02 — MCP Server

## Objetivo
Expor as operações do backend como MCP Tools que uma IA pode descobrir e chamar.

## Conceitos para estudar
- O que é MCP e que problema resolve (vs. API REST comum)
- Primitivas: **tools**, **resources**, **prompts**
- JSON-RPC, lifecycle (initialize → operações → shutdown)
- Transports: **stdio** vs **Streamable HTTP**
- Como o schema da tool é gerado a partir dos type hints e da docstring
- SDK oficial `mcp` / FastMCP; MCP Inspector para testar

## Decisão de arquitetura (discutir antes de codar)
O MCP Server acessa os dados como?
- **A)** Importando os services do backend diretamente (mesmo processo/pacote)
- **B)** Chamando a API FastAPI via HTTP
Registre a escolha e o motivo no PROGRESS.md.

## Tarefas
- [ ] Servidor FastMCP em `mcp_server/server.py` (transport stdio primeiro)
- [ ] Tools de leitura do PRD §7 (exceto `search_knowledge_base`)
- [ ] Docstrings claras — elas viram a descrição que o LLM lê
- [ ] Retornos estruturados (Pydantic/dict), erros tratados (pedido inexistente etc.)
- [ ] `check_order_status` calcula `is_late`
- [ ] Um **resource** (ex.: `catalog://categories`) e um **prompt** simples, para conhecer as primitivas
- [ ] Testar tudo no MCP Inspector

## Desafio obrigatório
Implementar `search_products` sem tocar no banco dentro da função da tool:
`MCP Tool → Service → Repository → Database`.

## Definição de pronto
- `list_tools` no Inspector mostra todas as tools com schemas corretos
- Cada tool testada manualmente com sucesso e com erro
- Nenhum SQL dentro de `mcp_server/`

## Perguntas de checagem
1. Diferença entre tool, resource e prompt? Quando usar cada um?
2. Por que a docstring importa tanto numa tool MCP?
3. Quando usar stdio e quando usar HTTP?

## Fora de escopo
LLM, agentes, client próprio.

## Prompt sugerido
> Fase 02. Leia @docs/phases/fase-02-mcp-server.md. Antes de codar, me explique o protocolo MCP e vamos discutir a decisão A vs B.
