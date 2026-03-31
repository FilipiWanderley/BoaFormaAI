# Observabilidade e Alertas (Uptime + Latência)

## Objetivo

Padronizar monitoramento contínuo de disponibilidade e qualidade da API em staging e produção.

## Endpoints monitorados

- `GET /health` (liveness)
- `GET /ready` (readiness)
- `GET /ops/metrics` (telemetria operacional)

## Recomendação de provedores

- Uptime monitor: UptimeRobot ou Better Stack
- Alertas: Email + Slack/WhatsApp via webhook

## Configuração mínima de uptime

Criar monitores para:

- `https://staging.api.academia.com/health`
- `https://staging.api.academia.com/ready`
- `https://api.academia.com/health`
- `https://api.academia.com/ready`

Parâmetros sugeridos:

- Intervalo de checagem: 1 minuto
- Timeout de requisição: 10 segundos
- Falha confirmada: 2 checagens consecutivas
- Janela de alerta: imediata após confirmação

## Alertas de latência e erro (via /ops/metrics)

Executar o script `backend/scripts/evaluate_metrics_alerts.py` via cron/scheduler e alertar se:

- `error_rate_percent > 5`
- `avg_latency_ms > 1200` em endpoint crítico
- `request_count == 0` em janela de operação

## Endpoints críticos recomendados

- `/auth/login`
- `/auth/google`
- `/workout/generate`
- `/chat`
- `/dashboard`

## Fluxo operacional de incidente

1. Alerta recebido
2. Confirmar status em `/health` e `/ready`
3. Verificar `/ops/metrics` para taxa de erro e latência
4. Se necessário, aplicar rollback seguindo `DEPLOYMENT_RUNBOOK.md`
5. Registrar incidente (causa, impacto, ação corretiva)

## Checklist

- [ ] Monitores de uptime ativos em staging
- [ ] Monitores de uptime ativos em produção
- [ ] Alertas de indisponibilidade testados
- [ ] Avaliação automática de métricas ativa
- [ ] Alertas de latência/erro testados
