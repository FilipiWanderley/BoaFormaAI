# Academia Boa Forma AI

Plataforma full stack para geração e acompanhamento de treinos personalizados com IA, com autenticação de alunos, dashboard de progresso, histórico de treinos e chat com assistente virtual.

## Visão Geral do Projeto

Este projeto foi estruturado em duas aplicações:

- **Backend** em FastAPI (Python), responsável por autenticação, regras de negócio, integração com IA e persistência.
- **Frontend** em React + TypeScript + Vite, responsável pela experiência do aluno nas telas de login, dashboard, treino, chat, histórico e perfil.

O escopo funcional está alinhado ao PRD em `PRD.md`, com boa parte das funcionalidades centrais já implementadas em versão funcional de MVP avançado.

## O que já foi implementado até agora

### Backend (API + domínio)

- Estrutura modular por camadas (`routers`, `services`, `schemas`, `models`).
- Banco versionado com Alembic (migration inicial + upgrade automático no startup da API).
- Índices compostos de produção em `workouts(user_id, created_at)` e `history(user_id, completed_at)`.
- Banco SQLite com entidades principais:
  - `users`
  - `workouts`
  - `history`
  - `exercises`
  - `workout_exercises`
  - `chat_messages`
- Autenticação completa:
  - Cadastro de usuário
  - Login com JWT
  - Login social com Google (`/auth/google`)
  - Refresh token com rotação e revogação
  - Bloqueio temporário após tentativas inválidas consecutivas
  - Hash de senha com bcrypt
  - Middleware de proteção de rotas com bearer token
  - Logout com invalidação de sessão de refresh token
- Geração de treino com IA:
  - Integração com Groq
  - Prompt estruturado com regras de segurança
  - Timeout e retry com backoff para resiliência
  - Fallback automático de treino quando o LLM está indisponível
  - Uso obrigatório de exercícios da base (sem invenção)
  - Validação de IDs retornados pela IA
  - Persistência do treino e seus exercícios selecionados
- Feedback de treino:
  - Endpoint para marcar treino como `facil`, `ok` ou `dificil`
  - Feedback usado como pista de intensidade em gerações futuras
- Dashboard:
  - Retorno de dados do usuário
  - Treino do dia (`today_workout`)
  - Último treino gerado
  - Estatísticas de treinos gerados/concluídos
  - Cálculo de streak
- Histórico:
  - Marcação de treino concluído
  - Listagem paginada de histórico do usuário autenticado
- Chat com IA:
  - Histórico por usuário
  - Memória conversacional (janela de mensagens)
  - Persistência dos turnos usuário/assistente
  - Endpoint para limpar histórico
  - Métrica de uso de IA em endpoint operacional
- Exercícios:
  - Base expandida para 1000 exercícios
  - 16 grupos musculares suportados
  - Listagem geral com filtros
  - Listagem de exercícios compatíveis com nível/restrições
  - Busca por ID
- Histórico por usuário:
  - Endpoint `GET /history/{user_id}` com controle de acesso (somente o próprio usuário)
- Health check (`/health`) para monitoramento básico.
- Rate limit em endpoints críticos (`/auth/login`, `/chat`, `/workout/generate`).
- Headers de segurança HTTP habilitados (CSP, X-Frame-Options, HSTS, etc.).
- Logs estruturados de auditoria para eventos críticos (auth/chat/workout).

### Frontend (Web App)

- Aplicação React com roteamento protegido.
- Gerenciamento de autenticação com Zustand.
- Camada de API centralizada com Axios e interceptors:
  - Injeção automática do token
  - Tratamento de 401 com logout e redirecionamento
- Estado assíncrono com TanStack Query (queries/mutations/cache invalidation).
- Telas implementadas:
  - Login
  - Cadastro
  - Dashboard
  - Treino (gerar, listar, visualizar e feedback)
  - Chat
  - Histórico
  - Perfil
- Layout base com sidebar e componentes reutilizáveis de UI.
- Biblioteca compatível de exercícios integrada na tela de treino (com imagem/fallback e filtros ativos).
- Base URL da API configurável por ambiente (`VITE_API_BASE_URL`).
- PWA com cache offline robusto (app shell + runtime cache) e prompt de instalação guiado.
- Responsividade mobile-first aplicada (menu mobile, grids adaptáveis e ajuste de touch targets).
- Estilização com Tailwind CSS + design escuro moderno.
- Build de produção funcional com Vite.

## Ferramentas, frameworks e bibliotecas em uso

### Backend

- **Linguagem:** Python 3.9
- **Framework API:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM:** SQLAlchemy 2.x
- **Validação/config:** Pydantic 2 + pydantic-settings
- **Auth/JWT:** python-jose
- **Hash de senha:** passlib + bcrypt
- **Upload/form-data:** python-multipart
- **Integração LLM:** Groq SDK
- **Variáveis de ambiente:** python-dotenv
- **Banco de dados:** SQLite
- **Migrations:** Alembic

Dependências principais (arquivo `backend/requirements.txt`):

- fastapi==0.115.6
- uvicorn[standard]==0.32.1
- sqlalchemy==2.0.36
- pydantic[email]==2.10.3
- pydantic-settings==2.7.0
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-multipart==0.0.20
- groq==0.13.1
- python-dotenv==1.0.1
- alembic==1.14.1

### Frontend

- **Framework UI:** React 19
- **Linguagem:** TypeScript
- **Build tool/dev server:** Vite 8
- **Roteamento:** React Router DOM
- **HTTP client:** Axios
- **Data fetching/cache:** TanStack React Query
- **Forms:** React Hook Form
- **Validação:** Zod + @hookform/resolvers
- **Estado global:** Zustand
- **Ícones:** lucide-react
- **Estilo:** Tailwind CSS + PostCSS + Autoprefixer

Dependências principais (arquivo `frontend/package.json`):

- react / react-dom
- typescript
- vite
- react-router-dom
- axios
- @tanstack/react-query
- react-hook-form
- zod
- zustand
- tailwindcss

## Estrutura de Pastas

```text
.
├── PRD.md
├── README.md
├── docker-compose.yml
├── render.yaml
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── scripts/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── migrations/
│   ├── Dockerfile
│   └── .dockerignore
│   └── .env.example
└── frontend/
    ├── DESIGN_SYSTEM.md
    ├── FIGMA_REFERENCE.md
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── store/
    │   ├── types/
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

## Endpoints principais já disponíveis

### Auth e Usuário

- `POST /users` — cadastro
- `POST /auth/login` — login
- `POST /auth/google` — login social com Google
- `POST /auth/refresh` — renovar sessão com refresh token
- `POST /auth/logout` — invalidar refresh token
- `GET /users/me` — dados do usuário autenticado
- `PATCH /users/me` — atualização de perfil
- `DELETE /users/me` — exclusão de conta e dados

### Treinos

- `POST /workout/generate` — geração de treino com IA
- `GET /workout/me` — lista de treinos do usuário
- `GET /workout/{workout_id}` — detalhe de treino
- `PATCH /workout/{workout_id}/feedback` — feedback do treino

### Exercícios

- `GET /exercises` — lista com filtros e paginação (`limit`, `offset`)
- `GET /exercises/compatible` — exercícios compatíveis com paginação (`limit`, `offset`)
- `GET /exercises/{exercise_id}` — detalhe do exercício
- `GET /admin/exercises` — curadoria (admin)
- `POST /admin/exercises` — criar exercício (admin)
- `PATCH /admin/exercises/{exercise_id}` — editar exercício (admin)
- `DELETE /admin/exercises/{exercise_id}` — remover exercício (admin)

Observação de domínio: a biblioteca atual contém **1000 exercícios** com **16 grupos musculares**.

### Histórico e Dashboard

- `POST /history` — marcar treino como concluído
- `GET /history/me` — histórico do usuário
- `GET /history/{user_id}` — histórico por usuário autenticado (com autorização)
- `GET /dashboard` — visão consolidada

### Chat IA

- `POST /chat` — enviar mensagem
- `GET /chat/history` — histórico do chat
- `DELETE /chat/history` — limpar histórico

### Saúde da API

- `GET /health`
- `GET /ready`
- `GET /ops/metrics` — métricas operacionais (uptime, contagem de requests, erros e uso de IA)

## Como rodar localmente

### 1) Backend

```bash
cd backend
./.venv/bin/pip install -r requirements.txt
./.venv/bin/alembic upgrade head
./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Criar `.env` baseado no `.env.example` com:

- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL`
- `DB_POOL_SIZE`
- `DB_MAX_OVERFLOW`
- `DB_SSL_MODE` (ex.: `require` em Postgres gerenciado)
- `CORS_ALLOWED_ORIGINS`
- `CORS_ALLOWED_ORIGIN_REGEX`
- `LOGIN_RATE_LIMIT`
- `LOGIN_RATE_WINDOW_SECONDS`
- `CHAT_RATE_LIMIT`
- `CHAT_RATE_WINDOW_SECONDS`
- `WORKOUT_RATE_LIMIT`
- `WORKOUT_RATE_WINDOW_SECONDS`
- `LLM_TIMEOUT_SECONDS`
- `LLM_MAX_RETRIES`
- `LLM_RETRY_BACKOFF_SECONDS`
- `LLM_ENABLE_FALLBACK`
- `GOOGLE_OAUTH_CLIENT_ID`
- `SOCIAL_DEFAULT_AGE`
- `SOCIAL_DEFAULT_WEIGHT_KG`
- `SOCIAL_DEFAULT_HEIGHT_CM`
- `SOCIAL_DEFAULT_GOAL`
- `SOCIAL_DEFAULT_LEVEL`
- `GROQ_API_KEY`
- `GROQ_MODEL`

Frontend (`frontend/.env`), com base em `frontend/.env.example`:

- `VITE_API_BASE_URL`
- `VITE_GOOGLE_CLIENT_ID`

Guia de configuração Google OAuth:

- `GOOGLE_OAUTH_SETUP.md`

Templates adicionais por ambiente:

- `backend/.env.staging.example`
- `backend/.env.production.example`

### 2) Frontend

```bash
cd frontend
npm ci
npm run dev -- --host 0.0.0.0 --port 3000
```

App web: `http://localhost:3000`  
API: `http://localhost:8000`  
Docs Swagger: `http://localhost:8000/docs`

## Deploy e execução com containers

### Backend com Docker

```bash
docker build -t boaforma-backend:local ./backend
docker run --rm -p 8000:8000 --env-file backend/.env boaforma-backend:local
```

### Execução com Docker Compose

```bash
docker compose up --build
```

Arquivo de configuração:

- `docker-compose.yml` (execução local)
- `render.yaml` (deploy simples em Render: backend + frontend)
- `deploy/render.staging.yaml` (template staging em Render)
- `deploy/render.production.yaml` (template produção em Render)
- `DEPLOYMENT_RUNBOOK.md` (sequência de release, smoke e rollback)
- `OBSERVABILITY_ALERTING.md` (monitoramento de uptime e alertas de latência/erro)
- `BACKUP_POLICY.md` (política de backup/restore e retenção)
- `PRIVACY_POLICY.md` (política de privacidade e minimização de dados)
- `ACCEPTANCE_CRITERIA.md` (critérios de aceitação por ambiente)
- `COST_PLAN.md` (estimativa mensal, orçamento e limites por ambiente)
- `DOMAIN_SSL_SETUP.md` (procedimento de subdomínio, SSL e CORS final)
- `INFRA_DECISIONS.md` (provedor final e recursos de produção)
- `CLOUDFLARE_PROVISIONING.md` (checklist DNS/WAF/SSL em Cloudflare)
- `GOOGLE_CLOUD_OAUTH_SETUP.md` (checklist OAuth oficial Google Cloud)
- `GO_LIVE_CHECKLIST.md` (sequência final de publicação em produção)
- `GO_LIVE_RUNBOOK.md` (runbook por fase com critérios de saída)
- `GO_LIVE_EXECUTION_LOG.md` (template de registro da execução real)
- `GO_LIVE_EXECUTION_LOG_EXAMPLE.md` (exemplo preenchido para usar no dia do go-live)
- `GO_LIVE_EXECUTION_LOG_TEMPLATE.md` (template com placeholders para preenchimento rápido)
- `.github/workflows/ci.yml` (pipeline CI para backend e frontend)

## Operação de banco (SQLite local)

Script utilitário para backup/restore local:

```bash
cd backend
./.venv/bin/python -m scripts.db_maintenance backup --output ./backups/boaforma.sqlite3.bak
./.venv/bin/python -m scripts.db_maintenance restore --input ./backups/boaforma.sqlite3.bak
```

## Alertas de métricas

Avaliação automática de métricas via `/ops/metrics`:

```bash
cd backend
./.venv/bin/python -m scripts.evaluate_metrics_alerts --base-url https://api.academia.com
```

## Testes de produção (automação base)

Carga:

```bash
cd backend
./.venv/bin/python -m scripts.load_test_api --base-url https://api.academia.com --requests 100 --concurrency 10
```

Segurança OWASP básico:

```bash
cd backend
./.venv/bin/python -m scripts.security_check_basic --base-url https://api.academia.com
```

Validação de CORS por domínio final:

```bash
cd backend
./.venv/bin/python -m scripts.validate_cors_domain --api-base-url https://api.academia.com --frontend-origin https://app.academia.com
```

Validação ponta a ponta de arquitetura:

```bash
cd backend
./.venv/bin/python -m scripts.validate_production_architecture --frontend-url https://app.academia.com --backend-url https://api.academia.com
```

## LGPD (base implementada)

- Consentimento explícito no cadastro
- Política publicada em `PRIVACY_POLICY.md` e `/privacy-policy.html`
- Exclusão de conta disponível no perfil
- Retenção/minimização documentadas em `PRIVACY_POLICY.md`

## PWA (métricas de engajamento)

- Eventos rastreados em `/ops/pwa-events`:
  - `install_prompt_shown`
  - `install_accepted`
  - `install_dismissed`
  - `app_installed`
- Métricas consolidadas em `/ops/metrics` no campo `pwa_events`

## Custos (guardrails)

Validação de orçamento mensal:

```bash
cd backend
./.venv/bin/python -m scripts.check_cost_guardrail --current-cost 180 --budget-limit 650
```

## Qualidade e validações já executadas

- Instalação de dependências frontend concluída com sucesso.
- Instalação de dependências backend concluída com sucesso.
- Build do frontend validado (`npm run build`).
- Validação de sintaxe Python backend (`python -m compileall app`).
- Suíte de testes backend validada (`python -m unittest discover -s tests -v`) com cenários de auth, treino, histórico, chat, erros de API e camada LLM.
- Health check da API validado com retorno `{"status":"ok"}`.
- Build e execução do backend em container Docker validados.

## Commits já realizados no repositório

- `753fc59` — docs: adiciona PRD do projeto
- `96a1aea` — feat(backend): implementa API FastAPI com auth, treino IA, chat e dashboard
- `9d3e7f2` — feat(frontend): adiciona app React com telas e integração da API
- `e551445` — chore(db): adiciona alembic e migration inicial
- `24ee327` — feat(history): adiciona endpoint /history/{user_id} com controle de acesso
- `99cb5d7` — feat(deploy): prepara render e baseURL configurável no frontend
- `f74a6be` — refactor(db): executa migrations no startup da API
- `92c9d74` — feat(frontend): exibe biblioteca de exercícios compatíveis na tela de treino
- `a7eadc6` — refactor(frontend): padroniza header e estado vazio em páginas
- `8e69c44` — docs(prd): marca validação de telas e fluxo frontend
- `6e719f5` — feat(mobile): implementa base responsiva e navegação mobile
- `64629b8` — feat(pwa): adiciona base mobile web instalável
- `1cdd192` — feat(exercises): expande para 1000 itens e 16 grupos musculares
- `9a234cc` — feat(frontend): aplica logo branca no login e favicon azul
- `79723b5` — style(login): amplia escala da logo para melhor presença visual

## Pendências principais (próximos passos)

- Evoluir painel/admin com busca avançada, edição em lote e trilha de auditoria.
