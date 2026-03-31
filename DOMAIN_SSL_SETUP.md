# Setup de Domínio, SSL e CORS (Produção)

## Domínios alvo

- Frontend: `app.academia.com`
- Backend: `api.academia.com`

## DNS e SSL (Cloudflare)

1. Criar registros DNS:
   - `app` → hosting frontend
   - `api` → hosting backend
2. Habilitar proxy/WAF no Cloudflare.
3. Habilitar SSL/TLS full strict.
4. Confirmar certificado ativo para ambos subdomínios.

## Backend (variáveis)

- `CORS_ALLOWED_ORIGINS=https://app.academia.com`
- `TRUSTED_HOSTS=api.academia.com`

## Frontend (variáveis)

- `VITE_API_BASE_URL=https://api.academia.com`

## Validação operacional

### Uptime/ready

```bash
cd backend
./.venv/bin/python -m scripts.smoke_production --base-url https://api.academia.com
```

### CORS final

```bash
cd backend
./.venv/bin/python -m scripts.validate_cors_domain --api-base-url https://api.academia.com --frontend-origin https://app.academia.com
```

### Segurança básica

```bash
cd backend
./.venv/bin/python -m scripts.security_check_basic --base-url https://api.academia.com
```
