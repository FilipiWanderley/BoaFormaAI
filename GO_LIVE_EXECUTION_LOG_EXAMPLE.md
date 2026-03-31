# Go-live Execution Log — Exemplo preenchido

## Informações da janela

- Data: 2026-04-02
- Responsável: Time Plataforma
- Versão/commit: `347c01d`
- Ambiente: Produção

## Pré-go-live

- Status: concluído
- Evidências:
  - `render.yaml` aplicado
  - variáveis de ambiente revisadas
  - DNS e SSL validados para `app.academia.com` e `api.academia.com`
  - OAuth Google validado em staging

## Execução

- Hora de início: 20:00 UTC
- Hora de término: 20:35 UTC
- Resultado dos comandos:
  - smoke: `ok`  
    `./.venv/bin/python -m scripts.smoke_production --base-url https://api.academia.com`
  - security: `ok`  
    `./.venv/bin/python -m scripts.security_check_basic --base-url https://api.academia.com`
  - cors: `ok`  
    `./.venv/bin/python -m scripts.validate_cors_domain --api-base-url https://api.academia.com --frontend-origin https://app.academia.com`
  - e2e architecture: `ok`  
    `./.venv/bin/python -m scripts.validate_production_architecture --frontend-url https://app.academia.com --backend-url https://api.academia.com`

## Pós-go-live

- Alertas ativos:
  - uptime: ativo
  - erro/latência: ativo
  - custo: ativo
- Incidentes observados: nenhum
- Ações corretivas: não aplicável

## Aprovação final

- Responsável técnico: aprovado
- Produto/negócio: aprovado
- Observações: janela encerrada sem rollback
