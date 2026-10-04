# Fase 04 — Primeiro LLM

## Objetivo
Entender a mecânica básica de conversa com um LLM. Esqueça o MCP nesta fase.

## Conceitos para estudar
- API de mensagens: `system`, `user`, `assistant`
- Histórico: o LLM não tem estado; você reenvia a conversa
- Parâmetros: `max_tokens`, `temperature`, modelo
- Tokens, contexto, custo
- Structured output (pedir JSON e validar com Pydantic)
- Streaming (opcional)

## Tarefas
- [ ] `agent/llm.py`: wrapper fino sobre o SDK (interface própria, para trocar provedor depois)
- [ ] Chat CLI com histórico em memória
- [ ] System prompt definindo o papel do assistente de e-commerce
- [ ] Exemplo de structured output: extrair `{intent, entities}` de uma frase do usuário
- [ ] Log de tokens usados por chamada

## Desafio obrigatório
Classificar a intenção do usuário (`buscar_produto`, `status_pedido`, `pedidos_cliente`, `outro`)
retornando JSON validado por Pydantic, com retry se o JSON vier inválido.

## Definição de pronto
Chat funcionando com histórico + extração estruturada validada.

## Perguntas de checagem
Explique com suas palavras a diferença entre **LLM**, **Tool**, **Agent** e **MCP**.

## Prompt sugerido
> Fase 04. Leia @docs/phases/fase-04-llm.md. Me explique como funciona a API de mensagens e por que o LLM é stateless.
