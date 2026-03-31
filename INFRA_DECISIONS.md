# Decisões de Infraestrutura (Produção)

## Provedor final

- Frontend: Render (Static Site)
- Backend: Render (Web Service Docker)
- Banco gerenciado: Render PostgreSQL
- DNS/WAF/SSL: Cloudflare

## Recursos previstos

- Serviço backend: `boaforma-backend`
- Serviço frontend: `boaforma-frontend`
- Banco gerenciado: `boaforma-db`

## Configuração de produção no repositório

- `render.yaml` consolidado com Postgres gerenciado e variáveis de produção
- `deploy/render.production.yaml` e `deploy/render.staging.yaml` para ambientes separados
- Hardening de host e CORS por domínio final:
  - `TRUSTED_HOSTS`
  - `CORS_ALLOWED_ORIGINS`

## Validação pós-provisionamento

1. Deploy em ambiente real
2. Executar:
   - smoke (`scripts.smoke_production`)
   - segurança (`scripts.security_check_basic`)
   - CORS por domínio final (`scripts.validate_cors_domain`)
3. Confirmar métricas em `/ops/metrics`
