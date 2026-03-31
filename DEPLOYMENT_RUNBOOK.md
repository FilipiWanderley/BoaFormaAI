# Runbook de Deploy, Staging e Rollback

## Ambientes

- Staging:
  - Frontend: `https://staging.app.academia.com`
  - Backend: `https://staging.api.academia.com`
- Produção:
  - Frontend: `https://app.academia.com`
  - Backend: `https://api.academia.com`

## Provisionamento Render

- Staging: usar `deploy/render.staging.yaml`
- Produção: usar `deploy/render.production.yaml`

## Sequência de release

1. Merge em `main`.
2. Deploy em staging.
3. Executar smoke check:

```bash
cd backend
./.venv/bin/python -m scripts.smoke_production --base-url https://staging.api.academia.com
```

4. Validar login, treino, chat e histórico manualmente.
5. Promover o mesmo commit para produção.
6. Executar smoke check em produção:

```bash
cd backend
./.venv/bin/python -m scripts.smoke_production --base-url https://api.academia.com
```

## Rollback

1. Identificar último commit estável:

```bash
git log --oneline -n 20
```

2. No painel do provedor, reimplantar a revisão anterior estável.
3. Confirmar recuperação com smoke check.
4. Registrar incidente com:
   - versão revertida
   - causa
   - ação corretiva

## Monitoramento e alertas

- Uptime monitor:
  - `GET /health`
  - `GET /ready`
- Métricas operacionais:
  - `GET /ops/metrics`
- Alertas recomendados:
  - indisponibilidade por 2 checagens consecutivas
  - erro HTTP 5xx acima de limiar
  - latência média degradada em endpoints críticos
