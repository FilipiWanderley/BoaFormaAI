# Go-live Checklist (ordem de execução)

## 1) Infra

- Aplicar `render.yaml` em produção.
- Confirmar serviços ativos:
  - backend `boaforma-backend`
  - frontend `boaforma-frontend`
  - banco `boaforma-db`
- Confirmar variáveis obrigatórias:
  - `DATABASE_URL`
  - `DB_SSL_MODE=require`
  - `CORS_ALLOWED_ORIGINS=https://app.academia.com`
  - `TRUSTED_HOSTS=api.academia.com`
  - `GOOGLE_OAUTH_CLIENT_ID`
  - `VITE_GOOGLE_CLIENT_ID`
  - `GROQ_API_KEY`

## 2) Cloudflare e domínio

- Executar checklist de `CLOUDFLARE_PROVISIONING.md`.
- Validar DNS e SSL para:
  - `app.academia.com`
  - `api.academia.com`

## 3) OAuth Google

- Executar checklist de `GOOGLE_CLOUD_OAUTH_SETUP.md`.
- Validar login Google (novo usuário e usuário existente).

## 4) Validações técnicas

```bash
cd backend
./.venv/bin/python -m scripts.smoke_production --base-url https://api.academia.com
./.venv/bin/python -m scripts.security_check_basic --base-url https://api.academia.com
./.venv/bin/python -m scripts.validate_cors_domain --api-base-url https://api.academia.com --frontend-origin https://app.academia.com
./.venv/bin/python -m scripts.validate_production_architecture --frontend-url https://app.academia.com --backend-url https://api.academia.com
```

## 5) Custos e observabilidade

- Validar orçamento com `COST_PLAN.md`.
- Ativar alertas operacionais:
  - uptime
  - erro/latência
  - custo

## 6) Plano de contingência

- Confirmar rollback conforme `DEPLOYMENT_RUNBOOK.md`.
- Confirmar backup/restore conforme `BACKUP_POLICY.md`.
