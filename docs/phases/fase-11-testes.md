# Fase 11 — Testes

## Objetivo
Consolidar a suíte de testes de todas as camadas (cada fase já deixou testes; aqui organizamos e cobrimos lacunas).

## Conceitos para estudar
- Pirâmide de testes: unit, integração, e2e
- Fixtures e banco de teste
- Mock do LLM (respostas determinísticas) vs testes reais com LLM (evals)
- Testes de falha: MCP fora, banco fora, timeout
- Cobertura (`pytest-cov`)

## Tarefas
- [ ] Organizar `tests/backend`, `tests/mcp`, `tests/agent`, `tests/rag`, `tests/integration`
- [ ] Fake LLM para testar o agent loop sem chamadas reais
- [ ] Testes de seleção de tool (evals pequenas com LLM real, marcadas para rodar separado)
- [ ] Testes de falha

## Desafio obrigatório
Simular MCP Server indisponível e o agente responder de forma controlada ao usuário em vez de quebrar.

## Definição de pronto
`uv run pytest` verde; evals de tool selection com taxa de acerto registrada.

## Perguntas de checagem
1. Como testar algo não determinístico como um LLM?

## Prompt sugerido
> Fase 11. Leia @docs/phases/fase-11-testes.md. Analise os testes existentes e me aponte as lacunas.
