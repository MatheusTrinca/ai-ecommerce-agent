# PRD — AI E-commerce Agent + MCP (Python)

## 1. Visão
Um agente de IA que atua como assistente de operações de um e-commerce. Ele recebe perguntas em linguagem
natural e usa ferramentas expostas por um **MCP Server** para consultar (e depois alterar) produtos, pedidos
e clientes, além de consultar políticas da empresa via RAG.

## 2. Objetivo real (estudo)
Aprender, construindo do zero e em ordem:
Python backend → MCP Server → MCP Client → LLM → Tool calling → Agent loop → Multi-tool → Memória → RAG →
Guardrails → Testes → Observabilidade → Docker.

Critério de sucesso do estudo: ao final, o Matheus consegue explicar e reimplementar cada camada sem
framework, e depois comparar com uma versão em LangGraph.

## 3. Personas
- **Operador / cliente final**: faz perguntas ("Meu pedido 12345 já foi enviado?").
- **Desenvolvedor (Matheus)**: constrói e entende cada camada.

## 4. Casos de uso (exemplos que o sistema final deve responder)
| # | Pergunta | Tools esperadas |
|---|---|---|
| UC1 | "Procure notebooks Lenovo com pelo menos 16 GB de RAM." | search_products |
| UC2 | "Qual o status do pedido #12345?" | get_order / check_order_status |
| UC3 | "Quais produtos da categoria X estão abaixo de $1.000?" | search_products |
| UC4 | "Mostre os pedidos do cliente João feitos este mês." | search_customers → get_customer_orders |
| UC5 | "O pedido do João está atrasado?" | search_customers → get_customer_orders → check_order_status |
| UC6 | "Quais notebooks abaixo de $1000 têm estoque?" | search_products → get_product_stock |
| UC7 | "Somente abaixo de $1000." (follow-up) | memória + search_products |
| UC8 | "Posso devolver um produto depois de 20 dias?" | search_knowledge_base |
| UC9 | "Posso cancelar o pedido 12345?" | get_order + search_knowledge_base |
| UC10 | "Cancele o pedido 12345." | cancel_order **com confirmação humana** |

## 5. Arquitetura alvo
```
User → Agent API (FastAPI) → AI Agent (loop, memória, seleção de tools)
                                 ├── Redis (memória de sessão)
                                 ├── RAG (pgvector)
                                 └── MCP Client ──MCP──> MCP Server → services → repositories → PostgreSQL
```

## 6. Modelo de dados
- **Customer**: id, name, email, created_at
- **Category**: id, name
- **Product**: id, name, description, brand, category_id, price, specs (JSON: ram_gb, storage_gb…), stock
- **Order**: id, customer_id, status (PENDING, PAID, SHIPPED, DELIVERED, CANCELLED), created_at,
  shipped_at, estimated_delivery
- **OrderItem**: id, order_id, product_id, quantity, unit_price

Seed obrigatório: ao menos 2 clientes chamados "João" e "Matheus", pedido `12345` existente,
um pedido atrasado, produtos Lenovo com e sem estoque, acima e abaixo de $1000.

## 7. Catálogo de MCP Tools
**Leitura**
- `search_products(query, category?, max_price?, min_ram_gb?, in_stock?)`
- `get_product(product_id)`
- `get_product_stock(product_id)`
- `search_orders(status?, customer_id?, date_from?, date_to?)`
- `get_order(order_id)`
- `check_order_status(order_id)` → inclui flag `is_late`
- `get_customer(customer_id)`
- `search_customers(name?, email?)`
- `get_customer_orders(customer_id, date_from?, date_to?)`
- `search_knowledge_base(query)` (Fase 9)

**Escrita** (Fase 10, sempre com confirmação)
- `cancel_order(order_id)`, `update_customer(customer_id, ...)`, `create_order(...)`

## 8. Requisitos não funcionais
- Nenhuma tool MCP acessa o banco diretamente (sempre via service).
- Agent loop com limite de iterações (`MAX_TOOL_CALLS = 10`).
- Erros de tool/MCP/LLM tratados sem derrubar a conversa.
- Todo request rastreável (request_id, session_id, tools chamadas, latência, tokens).
- Segredos só via variáveis de ambiente.
- `docker compose up` sobe o ambiente inteiro.

## 9. Fora de escopo
Pagamentos reais, autenticação de usuários finais complexa (OAuth), frontend elaborado
(um frontend simples é opcional na Fase 14), deploy em cloud.

## 10. Roadmap
| Milestone | Fases | Entrega |
|---|---|---|
| 🟢 1 — Backend | 00–02 | API + banco + MCP Server |
| 🔵 2 — MCP | 03–05 | MCP Client próprio + LLM + tool calling |
| 🟣 3 — Agent | 06–09 | Agent + MCP, multi-tool, memória, RAG |
| 🔴 4 — Produção | 10–14 | Guardrails, testes, observabilidade, Docker, versão final |

Detalhes de cada fase: `docs/phases/`.
