# Provisionamento Cloudflare (DNS + WAF + SSL)

## Objetivo

Publicar frontend e backend com domínios finais, proteção básica e SSL ativo.

## Domínios

- Frontend: `app.academia.com`
- Backend: `api.academia.com`

## Passo a passo

1. Adicionar domínio raiz da academia no Cloudflare.
2. Criar registros DNS:
   - `app` apontando para o host do frontend
   - `api` apontando para o host do backend
3. Ativar proxy (nuvem laranja) para ambos registros.
4. SSL/TLS:
   - modo `Full (strict)`
   - habilitar `Always Use HTTPS`
5. WAF:
   - regra gerenciada padrão Cloudflare ativa
   - bloquear tráfego anômalo por país/IP quando necessário
6. Rate Limiting (opcional recomendado):
   - limitar bursts em `/auth/login` e `/chat`

## Checklist de validação

- [ ] `https://app.academia.com` abre sem aviso de certificado
- [ ] `https://api.academia.com/health` retorna 200
- [ ] `https://api.academia.com/ready` retorna 200
- [ ] Certificados válidos nos dois subdomínios
- [ ] CORS validado com domínio final

## Referências internas

- `DOMAIN_SSL_SETUP.md`
- `DEPLOYMENT_RUNBOOK.md`
