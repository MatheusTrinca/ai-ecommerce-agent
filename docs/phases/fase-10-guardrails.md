# Fase 10 — Write tools + aprovação humana

## Objetivo
Permitir ações que alteram dados, com segurança.

## Conceitos para estudar
- Separação read vs write tools
- Human-in-the-loop: pausar o loop e aguardar confirmação
- Validação de regras de negócio no service (não no prompt!)
- Autorização: quem pode fazer o quê
- Prompt injection vindo de dados (ex.: descrição de produto maliciosa)
- Rate limiting

## Tarefas
- [ ] Tools `cancel_order`, `update_customer`, `create_order` (regras no service: não cancelar pedido enviado etc.)
- [ ] Marcar tools como "requer confirmação" (metadata/annotations)
- [ ] Agente pausa e retorna estado `awaiting_confirmation` na Agent API
- [ ] Endpoint para confirmar/rejeitar a ação pendente
- [ ] Teste com um produto cuja descrição tenta instruir o agente

## Desafio obrigatório
O agente **nunca** executa `cancel_order` sem confirmação explícita, mesmo que o usuário diga
"cancele sem me perguntar". Prove com teste automatizado.

## Definição de pronto
UC10 funciona com confirmação; regras de negócio bloqueiam ações inválidas mesmo se o LLM tentar.

## Perguntas de checagem
1. Por que a regra de segurança não pode viver só no system prompt?
2. Onde o fluxo de confirmação guarda o estado pendente?

## Prompt sugerido
> Fase 10. Leia @docs/phases/fase-10-guardrails.md. Vamos desenhar o fluxo de confirmação antes de codar.
