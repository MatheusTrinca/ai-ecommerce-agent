# Fase 09 — RAG

## Objetivo
Adicionar base de conhecimento (políticas) consultável pelo agente.

## Conceitos para estudar
- Embeddings e similaridade
- Chunking (tamanho, overlap, por seção)
- pgvector (reaproveita o Postgres); Qdrant como alternativa
- Metadados e filtros
- Busca híbrida (vetorial + full-text)
- Citações: responder indicando a fonte

## Tarefas
- [ ] Escrever 4 políticas em Markdown em `knowledge/` (shipping, return, warranty, payment)
- [ ] Pipeline de ingestão: ler → chunk → embed → salvar
- [ ] Tool MCP `search_knowledge_base(query)` retornando trechos + fonte
- [ ] Ajustar system prompt para citar a política usada

## Desafio obrigatório
O agente escolhe corretamente entre tools de banco e RAG:
- UC8 → só RAG
- UC2 → só banco
- UC9 → os dois combinados

## Definição de pronto
Os três casos funcionam e a resposta cita a fonte.

## Perguntas de checagem
1. Por que RAG virou uma tool MCP e não um passo fixo antes do LLM?
2. Como o tamanho do chunk afeta a resposta?

## Prompt sugerido
> Fase 09. Leia @docs/phases/fase-09-rag.md. Me explique embeddings e chunking com um exemplo pequeno antes da ingestão.
