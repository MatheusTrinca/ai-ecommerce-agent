# Fase 01 — Backend E-commerce

## Objetivo
Criar a API que, depois, será exposta via MCP. Arquitetura limpa em camadas.

## Pré-requisitos
Fase 00 concluída. PostgreSQL rodando (pode ser só `docker run postgres:16` por enquanto — imagem já
disponível localmente).

## Conceitos para estudar
- FastAPI: routers, dependências (`Depends`), schemas de resposta
- Pydantic v2: modelos, validação, `model_config`
- SQLAlchemy 2.0 async: `DeclarativeBase`, `Mapped`, relacionamentos, `AsyncSession`
- Alembic: migrations
- Repository pattern e service layer (por que separar?)

## Tarefas
- [ ] Models: Customer, Category, Product, Order, OrderItem (ver PRD §6)
- [ ] Primeira migration com Alembic
- [ ] Script de seed (`backend/seed.py`) com os dados obrigatórios do PRD
- [ ] Repositories por entidade
- [ ] Services por entidade
- [ ] Endpoints:
  - `GET /products` (filtros: `search`, `category`, `max_price`)
  - `GET /products/{id}`
  - `GET /orders`, `GET /orders/{id}`
  - `GET /customers/{id}`, `GET /customers/{id}/orders`
- [ ] Testes dos services (banco de teste ou fixtures)

## Desafio obrigatório
Implementar `GET /products?search=laptop&max_price=1000` (busca por nome/descrição/marca, case-insensitive)
**sem copiar implementação pronta**. Claude só dá dicas.

## Definição de pronto
- Fluxo `router → service → repository → SQLAlchemy → PostgreSQL` funcionando
- `/docs` (Swagger) mostra todos os endpoints
- Seed reproduzível
- Testes passando

## Perguntas de checagem
1. O que vai no service e o que vai no repository?
2. Por que o router não deve conhecer o SQLAlchemy?
3. O que acontece se dois requests usam a mesma `AsyncSession`?

## Prompt sugerido
> Fase 01. Leia @docs/phases/fase-01-backend.md. Plan mode: me explique a arquitetura em camadas e me dê os passos. Comece pelos models.
