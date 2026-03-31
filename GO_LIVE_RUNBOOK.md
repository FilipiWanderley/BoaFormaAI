# Go-live Runbook (pré / execução / pós)

## Pré-go-live

- [ ] Revisão final de configuração em `render.yaml`
- [ ] Variáveis sensíveis configuradas em produção
- [ ] Domínio e SSL validados (`DOMAIN_SSL_SETUP.md`)
- [ ] OAuth Google validado (`GOOGLE_CLOUD_OAUTH_SETUP.md`)
- [ ] Backup recente disponível
- [ ] Plano de rollback pronto (`DEPLOYMENT_RUNBOOK.md`)

## Execução do go-live

- [ ] Publicar backend em produção
- [ ] Publicar frontend em produção
- [ ] Validar health/ready:
  - [ ] `GET /health`
  - [ ] `GET /ready`
- [ ] Validar arquitetura ponta a ponta:

```bash
cd backend
./.venv/bin/python -m scripts.validate_production_architecture --frontend-url https://app.academia.com --backend-url https://api.academia.com
```

- [ ] Validar CORS por domínio final:

```bash
cd backend
./.venv/bin/python -m scripts.validate_cors_domain --api-base-url https://api.academia.com --frontend-origin https://app.academia.com
```

- [ ] Validar segurança básica:

```bash
cd backend
./.venv/bin/python -m scripts.security_check_basic --base-url https://api.academia.com
```

- [ ] Validar smoke completo:

```bash
cd backend
./.venv/bin/python -m scripts.smoke_production --base-url https://api.academia.com
```

## Pós-go-live

- [ ] Ativar e validar alertas (uptime, erro/latência, custo)
- [ ] Registrar evidências de validação
- [ ] Confirmar jornada crítica:
  - [ ] cadastro
  - [ ] login email
  - [ ] login Google
  - [ ] geração de treino
  - [ ] chat
- [ ] Comunicar liberação para stakeholders

## Critérios de saída

- [ ] Nenhum erro crítico em validações automáticas
- [ ] Nenhum bloqueio funcional em jornada crítica
- [ ] Monitoramento ativo e sem alertas críticos
