# Critérios de Aceitação por Ambiente

## Dev

- API sobe localmente sem erro.
- `/health` e `/ready` respondem 200.
- Testes backend passam.
- Build frontend passa.

## Staging

- Deploy concluído com sucesso.
- Smoke test automatizado sem falhas.
- Teste de carga básico sem erro (`failure_count == 0`).
- Security check básico aprovado.
- Fluxos críticos manuais aprovados:
  - login (email e Google)
  - geração de treino
  - chat
  - histórico

## Produção

- Mesma revisão validada em staging.
- Smoke test automatizado aprovado.
- Security check básico aprovado.
- Monitoramento de uptime ativo.
- Alertas de latência/erro ativos.
- Plano de rollback validado.

## Comandos de validação

### Smoke

```bash
cd backend
./.venv/bin/python -m scripts.smoke_production --base-url https://api.academia.com
```

### Carga

```bash
cd backend
./.venv/bin/python -m scripts.load_test_api --base-url https://api.academia.com --requests 100 --concurrency 10
```

### Segurança básica

```bash
cd backend
./.venv/bin/python -m scripts.security_check_basic --base-url https://api.academia.com
```
