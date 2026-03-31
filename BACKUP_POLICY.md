# Política de Backup e Recuperação (Produção)

## Objetivo

Garantir recuperação confiável dos dados em incidentes operacionais.

## Escopo

- Banco de produção: PostgreSQL gerenciado
- Banco de staging: PostgreSQL gerenciado

## Frequência e retenção

- Backup automático: diário
- Janela recomendada: 02:00 UTC
- Retenção mínima: 7 dias
- Retenção recomendada: 30 dias

## Procedimento de backup manual

```bash
cd backend
DATABASE_URL="postgresql://user:pass@host:5432/db" \
./.venv/bin/python -m scripts.db_maintenance backup --output ./backups --retention-days 30
```

## Procedimento de restore (teste)

```bash
cd backend
DATABASE_URL="postgresql://user:pass@host:5432/db" \
./.venv/bin/python -m scripts.db_maintenance restore --input ./backups/boaforma_pg_YYYYMMDD_HHMMSS.dump --clean
```

## Teste de recuperação (obrigatório)

Frequência recomendada: mensal.

Passos:

1. Selecionar backup recente.
2. Restaurar em banco de homologação temporário.
3. Executar smoke checks:
   - `/health`
   - `/ready`
   - `/ops/metrics`
4. Validar fluxo funcional:
   - login
   - dashboard
   - geração de treino
5. Registrar evidência do teste (data, responsável, resultado).

## RTO e RPO de referência

- RPO alvo: até 24h
- RTO alvo: até 60min
