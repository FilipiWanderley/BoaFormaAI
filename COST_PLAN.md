# Plano de Custos e Infraestrutura

## Premissas

- Produção com planos pagos básicos (sem free tier crítico).
- IA variável por uso, com monitoramento mensal.
- Valores estimados em USD/mês para facilitar comparação.

## Estimativa mensal por ambiente

| Componente | Dev | Staging | Produção |
|---|---:|---:|---:|
| Backend (Render) | 0–7 | 7–25 | 25–85 |
| Banco (Postgres gerenciado) | 0–7 | 7–25 | 25–100 |
| Frontend (Static hosting) | 0 | 0–7 | 0–20 |
| Domínio + DNS/SSL | 0 | 0 | 1–5 |
| IA (Groq / LLM) | 5–25 | 10–60 | 50–400 |
| **Total estimado** | **5–39** | **24–117** | **101–610** |

## Orçamento e limites (guardrails)

- Dev: alvo até **USD 40/mês**
- Staging: alvo até **USD 120/mês**
- Produção: alvo até **USD 650/mês**
- Alerta amarelo: 80% do limite
- Alerta vermelho: 100% do limite

## Estratégia de controle

- Revisão semanal de consumo por componente.
- Limitar endpoints caros via rate limit e timeout.
- Usar fallback de IA quando necessário para proteger custo.
- Revisar modelos LLM e tokens máximos mensalmente.

## Alertas de custo

- Provedor de infraestrutura: alertas nativos (quando disponível).
- IA: alerta por gasto acumulado mensal.
- Automação local: `backend/scripts/check_cost_guardrail.py`.

## Operação

- Responsável: owner técnico do projeto.
- Frequência de revisão: semanal em staging/prod.
- Ação corretiva padrão:
  1. identificar fonte de aumento;
  2. aplicar limite temporário;
  3. revisar capacidade/plano;
  4. documentar decisão.
