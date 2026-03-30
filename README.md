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
- Criação automática de tabelas via SQLAlchemy (`Base.metadata.create_all`).
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
  - Hash de senha com bcrypt
  - Middleware de proteção de rotas com bearer token
- Geração de treino com IA:
  - Integração com Groq
  - Prompt estruturado com regras de segurança
  - Uso obrigatório de exercícios da base (sem invenção)
  - Validação de IDs retornados pela IA
  - Persistência do treino e seus exercícios selecionados
- Feedback de treino:
  - Endpoint para marcar treino como `facil`, `ok` ou `dificil`
  - Feedback usado como pista de intensidade em gerações futuras
- Dashboard:
  - Retorno de dados do usuário
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
- Exercícios:
  - Listagem geral com filtros
  - Listagem de exercícios compatíveis com nível/restrições
  - Busca por ID
- Health check (`/health`) para monitoramento básico.

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
│   └── .env.example
└── frontend/
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
- `GET /users/me` — dados do usuário autenticado
- `PATCH /users/me` — atualização de perfil

### Treinos

- `POST /workout/generate` — geração de treino com IA
- `GET /workout/me` — lista de treinos do usuário
- `GET /workout/{workout_id}` — detalhe de treino
- `PATCH /workout/{workout_id}/feedback` — feedback do treino

### Exercícios

- `GET /exercises` — lista com filtros
- `GET /exercises/compatible` — exercícios compatíveis
- `GET /exercises/{exercise_id}` — detalhe do exercício

### Histórico e Dashboard

- `POST /history` — marcar treino como concluído
- `GET /history/me` — histórico do usuário
- `GET /dashboard` — visão consolidada

### Chat IA

- `POST /chat` — enviar mensagem
- `GET /chat/history` — histórico do chat
- `DELETE /chat/history` — limpar histórico

### Saúde da API

- `GET /health`

## Como rodar localmente

### 1) Backend

```bash
cd backend
./.venv/bin/pip install -r requirements.txt
./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Criar `.env` baseado no `.env.example` com:

- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL`
- `GROQ_API_KEY`
- `GROQ_MODEL`

### 2) Frontend

```bash
cd frontend
npm ci
npm run dev -- --host 0.0.0.0 --port 3000
```

App web: `http://localhost:3000`  
API: `http://localhost:8000`  
Docs Swagger: `http://localhost:8000/docs`

## Qualidade e validações já executadas

- Instalação de dependências frontend concluída com sucesso.
- Instalação de dependências backend concluída com sucesso.
- Build do frontend validado (`npm run build`).
- Validação de sintaxe Python backend (`python -m compileall app`).
- Health check da API validado com retorno `{"status":"ok"}`.

## Commits já realizados no repositório

- `753fc59` — docs: adiciona PRD do projeto
- `96a1aea` — feat(backend): implementa API FastAPI com auth, treino IA, chat e dashboard
- `9d3e7f2` — feat(frontend): adiciona app React com telas e integração da API

## Pendências principais (próximos passos)

- Expandir base de exercícios para 200+ itens.
- Criar suíte de testes automatizados (backend e frontend).
- Adicionar migrações de banco (ex.: Alembic).
- Definir pipeline de lint/typecheck/test no CI.
- Hardening para produção (CORS por ambiente, deploy e observabilidade).

