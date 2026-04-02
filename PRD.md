# PRD — Academia Boa Forma AI

## 1. Visão do Produto

**Descrição:** Plataforma interna para a Academia Boa Forma, utilizada pelos alunos para geração e acompanhamento de treinos personalizados com IA.

**Objetivos:**
- Personalizar treinos com IA
- Acompanhar evolução
- Centralizar experiência do aluno

---

## 2. Usuários

- **Aluno** (principal)
- (Futuro) Admin da academia

---

## 3. Funcionalidades

### 3.1 Cadastro e Autenticação

**Dados do usuário:** nome, idade, peso, altura, objetivo, nível, restrições

**Checklist:**
- [x] Criar tabela `users`
- [x] Implementar cadastro (`POST /users`)
- [x] Implementar login (`POST /auth/login`)
- [x] Hash de senha (bcrypt)
- [x] JWT
- [x] Middleware de autenticação

---

### 3.2 Geração de Treino com IA

**Checklist:**
- [x] Criar endpoint `POST /workout/generate`
- [x] Criar prompt base
- [x] Integrar Groq
- [x] Estruturar resposta (JSON)
- [x] Salvar treino no banco

---

### 3.3 Dashboard

**Checklist:**
- [x] Criar endpoint `GET /dashboard`
- [x] Retornar treino do dia
- [x] Retornar progresso
- [x] Criar tela frontend

---

### 3.4 Histórico

**Checklist:**
- [x] Criar tabela `history`
- [x] Criar endpoint `GET /history/{user_id}`
- [x] Criar endpoint `POST /history`
- [x] Conectar com treino

---

### 3.5 Chat com IA

**Checklist:**
- [x] Criar endpoint `POST /chat`
- [x] Criar memória básica
- [x] Integrar com LLM
- [x] Salvar histórico

---

### 3.6 Adaptação Inteligente

**Checklist:**
- [x] Criar lógica de feedback
- [x] Ajustar prompt com histórico
- [x] Regerar treino com base no feedback

---

## 4. Arquitetura

### Backend
```
backend/
├── routers/
├── services/
├── db/
├── schemas/
└── config/
```

### Frontend
```
frontend/
├── pages/
├── components/
├── services/
└── hooks/
```

**Checklist:**
- [x] Criar estrutura de pastas backend
- [x] Criar estrutura frontend
- [x] Definir padrões de código
- [x] Separar responsabilidades

---

## 5. API — Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/users` | Cadastro de aluno |
| POST | `/auth/login` | Login |
| POST | `/workout/generate` | Gerar treino com IA |
| GET | `/workout/{user_id}` | Buscar treino do aluno |
| POST | `/chat` | Chat com IA |
| GET | `/history/{user_id}` | Histórico do aluno |
| GET | `/exercises` | Listar exercícios (com filtros) |
| GET | `/exercises/{id}` | Detalhes de um exercício |

**Checklist:**
- [x] Definir schemas (Pydantic)
- [x] Implementar validação
- [x] Testar endpoints no Swagger
- [x] Criar tratamento de erro

---

## 6. IA (GenAI)

- **LLM:** Groq
- **Embeddings:** local
- **Arquivo principal:** `llm_service.py`

**Checklist:**
- [x] Criar `llm_service.py`
- [x] Criar prompt base
- [x] Criar prompt com contexto
- [x] Testar respostas
- [x] Ajustar qualidade
- [x] Evitar prompt injection básico

---

## 7. Banco de Dados

- **Engine:** SQLite
- **Tabelas:** `users`, `workouts`, `history`, `exercises`, `workout_exercises`

**Checklist:**
- [x] Criar SQLite
- [x] Criar models
- [x] Criar migrations (opcional)
- [x] Testar persistência

---

## 8. Segurança

- JWT
- Hash de senha (bcrypt)
- Validação de inputs

**Checklist:**
- [x] Implementar bcrypt
- [x] Implementar JWT
- [x] Proteger rotas
- [x] Validar dados de entrada
- [x] Evitar prompt injection básico

---

## 9. Frontend — Telas

- Login
- Dashboard
- Treino
- Chat
- Histórico
- Perfil

**Checklist:**
- [x] Criar layout base
- [x] Criar navegação
- [x] Integrar com API
- [x] Criar estados (loading/error)
- [x] Testar fluxo completo

---

## 10. UI (Figma)

**Checklist:**
- [x] Subir app funcional
- [x] Validar todas as telas
- [x] Importar referências do Figma
- [x] Ajustar layout
- [x] Criar design system
- [x] Padronizar componentes

---

## 11. Deploy (Opcional)

**Checklist:**
- [x] Dockerizar backend
- [x] Deploy simples (Render/Vercel)
- [x] Configurar variáveis de ambiente

---

## 12. Testes

**Checklist:**
- [x] Testar endpoints
- [x] Testar fluxo completo
- [x] Testar IA
- [x] Testar erros

---

## 13. Roadmap de Execução

### Fase 1 — Base
- [x] Estrutura backend
- [x] Banco de dados
- [x] Autenticação

### Fase 1.5 — Exercise Library
- [x] Escolher fonte de dados (API ou dataset)
- [x] Criar tabelas `exercises` e `workout_exercises`
- [x] Importar dados iniciais
- [x] Criar service de exercícios com filtros

### Fase 2 — IA
- [x] Geração de treino
- [x] Integração LLM (Groq)
- [x] IA seleciona da base, não inventa exercícios

### Fase 3 — Funcionalidade
- [x] Dashboard
- [x] Histórico
- [x] Chat

### Fase 4 — Frontend
- [x] Telas
- [x] Integração com API

### Fase 5 — UI
- [x] Aplicar Figma
- [x] Design system

---

---

## 14. Módulo de Exercícios (Exercise Library)

> **Regra crítica:** a IA **nunca** inventa exercícios. Ela recebe a lista filtrada do banco e monta o treino a partir dela.

### Estrutura de cada exercício

```json
{
  "id": "string",
  "name": "string",
  "muscle_group": "string",
  "equipment": "string",
  "difficulty": "string",
  "instructions": ["string"],
  "media_type": "image | gif | video",
  "media_url": "string"
}
```

### Fluxo de geração de treino

```
Perfil do usuário (objetivo + nível + restrições + equipamento)
        ↓
Sistema filtra exercícios válidos do banco
        ↓
IA recebe a lista filtrada
        ↓
IA monta séries, reps e descanso usando esses exercícios
```

### Fonte de dados (MVP)
- Dataset público ou API (ex: ExerciseDB, MuscleWiki, JSON interno)
- Priorizar exercícios com imagem ou GIF
- **Não** usar conteúdo sem licença

### Mídia
- MVP: imagem ou GIF (mais leve)
- Futuro: vídeo curto, vídeos próprios da academia

### Tabelas
- `exercises` — base de exercícios
- `workout_exercises` — relacionamento treino ↔ exercícios selecionados

**Checklist:**
- [x] Escolher fonte de dados (API ou dataset)
- [x] Criar tabela `exercises`
- [x] Criar tabela `workout_exercises`
- [x] Importar dados iniciais
- [x] Criar service com filtros por músculo, equipamento e nível
- [x] Integrar filtro com geração de treino
- [x] Garantir que IA usa apenas exercícios da base
- [x] Adicionar campo de mídia (URL de imagem/GIF)
- [x] Testar exibição no frontend

---

## 15. Módulo de Exercise Library (Base Completa de Exercícios)

### Descrição

O sistema deve possuir uma base robusta e escalável de exercícios físicos contendo centenas ou milhares de exercícios, utilizada como fonte única e confiável para geração de treinos. Este módulo garante consistência, qualidade e realismo nos treinos gerados pela IA.

### Objetivos

- Garantir que todos os treinos utilizem exercícios válidos e estruturados
- Evitar que a IA invente exercícios inexistentes
- Permitir exibição de mídia (imagem, GIF ou vídeo) por exercício
- Padronizar a experiência do usuário
- Permitir escalabilidade da base de dados

### Escopo de dados

| Fase | Volume |
|------|--------|
| MVP | 200–400 exercícios |
| Avançada | 1000+ exercícios |

### Fonte de dados

- Datasets públicos (JSON)
- APIs externas (opcional, ex: ExerciseDB)
- Base interna persistida no banco

### Regras obrigatórias

- ❌ NÃO baixar conteúdo sem licença
- ❌ NÃO usar mídia sem autorização
- ❌ NÃO permitir que a IA invente exercícios
- ✅ Usar apenas exercícios existentes na base
- ✅ Garantir consistência dos dados

### Estrutura de cada exercício

```json
{
  "id": "string",
  "name": "string",
  "muscle_group": "string",
  "secondary_muscles": ["string"],
  "equipment": "string",
  "difficulty": "beginner | intermediate | advanced",
  "instructions": ["string"],
  "media_type": "image | gif | video",
  "media_url": "string"
}
```

### Persistência

- Tabela principal: `exercises`
- Relacionamentos: `workout_exercises`, `user_history`

### Integração com IA

> 🚨 **Regra crítica:** a IA NÃO deve gerar exercícios do zero.

**Fluxo de geração de treino:**

```
Usuário → perfil
       ↓
Sistema filtra exercícios válidos
       ↓
IA recebe lista filtrada
       ↓
IA monta treino estruturado (séries, reps, descanso)
       ↓
Retorna resposta
```

### Filtros obrigatórios

- Grupo muscular
- Equipamento disponível
- Nível do usuário
- Restrições físicas

### Mídia

- **MVP:** imagens ou GIFs
- **Futuro:** vídeos curtos, conteúdo próprio da academia

### Estratégia de uso da IA

A IA deve:
- Selecionar exercícios da base
- Organizar ordem do treino
- Definir séries, repetições e descanso
- Adaptar treino com base em feedback

### Validação

O sistema deve validar que:
- Todos os exercícios existem na base
- Nenhum exercício inventado foi incluído
- Os dados retornados estão completos

### Checklist de implementação

- [x] Escolher dataset com 200+ exercícios
- [x] Criar tabela `exercises`
- [x] Criar tabela `workout_exercises`
- [x] Criar script de importação (`scripts/seed_exercises.py`)
- [x] Popular banco com dados iniciais (200 exercícios — base MVP)
- [x] Criar service de exercícios (`services/exercise.py`)
- [x] Implementar filtro por músculo
- [x] Implementar filtro por equipamento
- [x] Implementar filtro por nível (com progressão: avancado acessa todos)
- [x] Implementar filtro por restrições físicas (keyword matching)
- [x] Expandir base para 1000 exercícios
- [x] Expandir grupos musculares para 16 categorias
- [x] Integrar com geração de treino (Fase 2)
- [x] Atualizar prompt da IA para usar exercícios da base
- [x] Validar saída da IA (nenhum exercício inventado)
- [x] Adicionar campo de mídia (image_url já presente)
- [x] Testar exibição no frontend

### Evolução futura

- Adicionar vídeos próprios da academia
- Permitir upload de mídia pelo admin
- Criar recomendações baseadas em desempenho
- Integrar com sensores ou wearables

---

## Checklist Final (Nível Portfólio)

- [x] App funcionando ponta a ponta
- [x] IA integrada
- [x] Autenticação
- [x] Banco persistente
- [x] UI moderna
- [x] README profissional
- [x] Deploy (opcional)

---

## 16. Responsividade e Experiência Mobile Web

### Descrição

A plataforma deve ser desenvolvida com abordagem **responsive web**, garantindo funcionamento adequado em **desktop, tablet e smartphones**, sem necessidade inicial de publicação em lojas como App Store ou Google Play.

O produto deve oferecer uma experiência consistente e adaptada para diferentes tamanhos de tela, permitindo que o aluno utilize o sistema diretamente pelo navegador do celular com usabilidade, legibilidade e navegação adequadas.

### Objetivos

- Garantir acesso completo ao sistema em dispositivos móveis
- Adaptar todas as telas para diferentes resoluções
- Melhorar usabilidade em navegação por toque
- Permitir uso do sistema como mobile web
- Preparar base futura para possível evolução para PWA

### Regras obrigatórias

- ✅ Todas as telas devem ser totalmente responsivas
- ✅ O sistema deve funcionar em desktop, tablet e mobile
- ✅ Componentes devem se adaptar sem quebrar layout
- ✅ Botões, inputs e áreas clicáveis devem ser adequados para toque
- ✅ Textos devem manter legibilidade em telas menores
- ✅ Menus e navegação devem ser simplificados no mobile
- ❌ Não depender exclusivamente de interface desktop
- ❌ Não permitir overflow horizontal ou elementos fora da tela

### Escopo de responsividade

As seguintes telas devem obrigatoriamente possuir versão responsiva:

- Login
- Dashboard
- Treino
- Chat com IA
- Histórico
- Perfil

### Requisitos de UI/UX

- Layout com adaptação para múltiplos breakpoints
- Grid e espaçamentos fluidos
- Navegação otimizada para touch
- Sidebar convertida em menu mobile quando necessário
- Cards, tabelas e listas adaptados para telas pequenas
- Formulários com boa usabilidade em celular
- Prioridade para performance e carregamento leve no mobile

### Breakpoints sugeridos

- Mobile: até 767px
- Tablet: 768px até 1023px
- Desktop: 1024px ou mais

### Estratégia técnica

A interface frontend deve ser construída com princípios de responsividade desde a base, utilizando:

- Media queries
- Layout flexível
- Grid responsivo
- Componentes reutilizáveis adaptáveis
- Abordagem mobile-first sempre que possível

### Checklist de implementação

- [x] Definir estratégia responsiva do frontend
- [x] Adaptar layout global para mobile
- [x] Criar breakpoints padrão do projeto
- [x] Ajustar navbar/menu para telas pequenas
- [x] Validar telas de login, dashboard, treino, chat, histórico e perfil no mobile
- [x] Ajustar formulários para toque
- [x] Garantir legibilidade tipográfica em telas pequenas
- [x] Corrigir overflow horizontal
- [x] Testar responsividade em diferentes resoluções
- [x] Validar experiência mobile web completa

### Evolução futura

- Transformar a aplicação em PWA
- Permitir adicionar à tela inicial do celular
- Melhorar experiência semelhante a app nativo
- Avaliar publicação futura em lojas móveis

---

## 17. Arquitetura de Produção (Production Architecture)

### Descrição

Definição da arquitetura necessária para suportar uso real por alunos da academia, garantindo escalabilidade, segurança e disponibilidade.

### Objetivos

- Suportar múltiplos usuários simultâneos
- Garantir alta disponibilidade
- Separar responsabilidades (frontend, backend, banco)
- Preparar base para crescimento

### Arquitetura proposta

```text
Usuário (web/mobile browser)
        ↓
Cloudflare (CDN + WAF + DNS)
        ↓
Frontend (Cloudflare Pages / Vercel)
        ↓
Backend API (Render / Railway / Fly.io)
        ↓
Banco de Dados (PostgreSQL gerenciado)
        ↓
Serviço de IA (Groq)
```

### Componentes

- Frontend: aplicação web responsiva
- Backend: API REST com autenticação e lógica de negócio
- Banco: PostgreSQL (produção)
- CDN/WAF: Cloudflare
- LLM: Groq

### Regras obrigatórias

- ❌ Não usar SQLite em produção
- ✅ Separar frontend e backend
- ✅ Usar banco gerenciado (Postgres)
- ✅ Todas as comunicações via HTTPS

### Checklist de implementação

- [x] Definir provedor final de frontend e backend
- [x] Provisionar Cloudflare (DNS + WAF + SSL)
- [x] Provisionar Postgres gerenciado
- [x] Configurar variáveis de ambiente de produção
- [x] Validar arquitetura ponta a ponta em ambiente produtivo

---

## 18. Segurança (Production-Grade Security)

### Descrição

Requisitos para garantir segurança de dados e proteção contra ataques.

### Objetivos

- Proteger dados dos alunos
- Evitar acesso não autorizado
- Mitigar ataques comuns (brute force, injection, etc.)

### Autenticação

- JWT com expiração curta
- Refresh token
- Hash de senha com bcrypt
- Logout com invalidação de sessão

### Proteções obrigatórias

- Rate limit em:
  - login
  - chat
  - geração de treino
- Bloqueio após tentativas falhas
- Validação de input (backend)
- CORS restrito
- Headers de segurança

### Infra de segurança

- HTTPS obrigatório
- WAF (Cloudflare)
- Proteção contra brute force
- Logs de acesso e auditoria

### IA (segurança)

- Sanitizar input do usuário
- Limitar contexto
- Validar output do LLM
- Evitar prompt injection

### Checklist de implementação

- [x] Implementar refresh token com rotação/revogação
- [x] Implementar rate limit por endpoint crítico
- [x] Implementar lockout temporário por falhas de login
- [x] Restringir CORS por ambiente/domínio
- [x] Adicionar headers de segurança (CSP, X-Frame-Options, etc.)
- [x] Estruturar logs de auditoria para eventos sensíveis

---

## 19. Banco de Dados (Produção)

### Descrição

Estratégia de banco para ambiente real.

### Mudanças necessárias

- Migrar de SQLite → PostgreSQL

### Requisitos

- Backup automático diário
- Possibilidade de restore
- Índices nas tabelas principais
- Conexões seguras (SSL)

### Performance

Indexar:

- users
- workouts
- history

Boas práticas:

- Evitar queries pesadas sem filtro
- Paginação em endpoints

### Checklist de implementação

- [x] Configurar `DATABASE_URL` para Postgres em produção
- [x] Criar migration com índices estratégicos
- [x] Validar SSL no driver/conexão de banco
- [x] Configurar política de backup e restore testado
- [x] Revisar endpoints para paginação consistente

---

## 20. Escalabilidade e Performance

### Descrição

Garantir que o sistema suporte crescimento de usuários.

### Cenário inicial

- ~1000 alunos cadastrados
- uso simultâneo moderado

### Estratégias

- CDN para frontend
- Backend stateless
- Pool de conexões no banco
- Cache (futuro)

### Pontos críticos

- Chat com IA (latência)
- Geração de treino
- Queries no banco

### Regras

- Timeout nas requisições de IA
- Retry controlado
- Fallback em falha de IA

### Checklist de implementação

- [x] Configurar timeout e retry com política clara no serviço de IA
- [x] Configurar pool de conexões para produção
- [x] Definir fallback funcional para indisponibilidade do LLM
- [x] Medir latência por endpoint crítico

---

## 21. Observabilidade (Logs, Monitoramento e Alertas)

### Descrição

Sistema deve ser monitorado continuamente.

### Requisitos

Logs de:

- login
- geração de treino
- erros
- chat

Operação:

- Monitoramento de uptime
- Alertas em falhas

### Métricas importantes

- tempo de resposta da API
- erros por endpoint
- uso de IA
- número de usuários ativos

### Checklist de implementação

- [x] Padronizar logs estruturados (JSON) no backend
- [x] Integrar monitoramento de uptime
- [x] Definir alertas de erro/latência
- [x] Expor métricas mínimas de aplicação

---

## 22. Deploy e Ambientes

### Descrição

Estratégia de deploy e separação de ambientes.

### Ambientes

- Dev
- Staging
- Produção

### Regras

- ❌ Não deployar direto em produção
- ✅ Testar em staging antes
- ✅ Variáveis de ambiente separadas

### Deploy

- CI/CD automatizado
- Rollback possível
- Versionamento

### Checklist de implementação

- [x] Criar ambiente de staging completo
- [x] Configurar pipeline CI/CD com gates de qualidade
- [x] Definir estratégia de rollback
- [x] Separar segredos por ambiente (dev/staging/prod)

---

## 23. Domínio e Acesso Público

### Descrição

Como o sistema será acessado pelos alunos.

### Estrutura

- `app.academia.com` → frontend
- `api.academia.com` → backend

### Requisitos

- HTTPS obrigatório
- DNS configurado
- Certificado SSL ativo

### Acesso

- via navegador (mobile e desktop)
- sem necessidade de app store

### Checklist de implementação

- [x] Configurar subdomínios de frontend e backend
- [x] Configurar certificados SSL
- [x] Validar CORS e cookies/tokens com domínio final

---

## 24. PWA (Evolução futura opcional)

### Descrição

Transformar o sistema em app instalável sem loja.

### Benefícios

- adicionar à tela inicial
- experiência tipo app
- offline básico (futuro)

### Checklist de evolução

- [x] Base inicial de manifest e service worker
- [x] Estratégia de cache offline robusta
- [x] UX de instalação guiada (prompt install)

---

## 25. Testes de Produção

### Tipos

- testes de carga (simular usuários)
- testes de segurança
- testes de API
- testes de fluxo completo

### Checklist de implementação

- [x] Definir suíte de testes de carga
- [x] Definir suíte de segurança (OWASP básico)
- [x] Automatizar smoke tests de produção
- [x] Definir critérios de aceitação por ambiente

---

## 26. Backup e Recuperação

### Requisitos

- backup automático diário
- retenção de backups
- teste de restore

### Checklist de implementação

- [x] Configurar backup diário no banco gerenciado
- [x] Definir janela de retenção
- [x] Executar restore de teste e documentar procedimento

---

## 27. LGPD e Privacidade

### Dados tratados

- nome
- idade
- peso
- altura
- objetivo
- restrições físicas

### Requisitos

- consentimento do usuário
- política de privacidade
- opção de exclusão de conta
- proteção de dados sensíveis

### Checklist de implementação

- [x] Implementar fluxo de consentimento
- [x] Publicar política de privacidade
- [x] Implementar exclusão de conta/dados
- [x] Definir política de retenção e minimização de dados

---

## 28. Custos e Infraestrutura

### Descrição

Planejamento mínimo de custos.

### Observação crítica

- ❌ Free tier não é confiável para produção
- ✅ Usar planos básicos pagos

### Componentes com custo

- backend
- banco
- domínio
- IA (uso)

### Checklist de implementação

- [x] Estimar custo mensal por ambiente
- [x] Definir orçamento e limites de consumo
- [x] Configurar alertas de custo (quando disponível)

---

## 29. Roadmap Pós-Produção

- versão PWA
- vídeos próprios da academia
- painel admin
- recomendação inteligente
- integração com wearables

---

## 30. Autenticação Social (Login com Google)

### Descrição

Implementação de login social utilizando Google como provedor de autenticação, permitindo que usuários acessem o sistema sem necessidade de criação de senha.

O login social deve ser integrado ao sistema atual de autenticação, garantindo consistência, segurança e evitando duplicação de contas.

### Objetivos

- Reduzir fricção no cadastro/login
- Melhorar experiência do usuário
- Aumentar taxa de conversão no onboarding
- Permitir login rápido via conta Google
- Manter compatibilidade com login tradicional (email + senha)

### Provedores suportados (MVP)

- ✅ Google
- ❌ Facebook (fora do escopo inicial)
- ❌ Microsoft (futuro)

### Fluxo de autenticação

```text
Usuário clica em "Continuar com Google"
        ↓
Frontend inicia autenticação com Google
        ↓
Usuário autoriza acesso
        ↓
Google retorna token (credential)
        ↓
Frontend envia token para backend
        ↓
Backend valida token com Google
        ↓
Backend extrai dados do usuário (email, nome, provider_id)
        ↓
Sistema verifica existência do usuário:
    - Se NÃO existir → cria novo usuário
    - Se existir → vincula conta Google
        ↓
Backend gera JWT da aplicação
        ↓
Usuário autenticado no sistema
```

### Estrutura de dados (User)

A tabela `users` deve suportar autenticação por múltiplos provedores.

Campos adicionais:

- `provider` → `"email"` | `"google"`
- `provider_id` → identificador único do Google
- `password` → opcional (`null` para login social)

### Regras de negócio

- ✅ Email é a identidade única do usuário
- ❌ Não permitir múltiplas contas com o mesmo email
- ✅ Se usuário já existir com email + senha: vincular login Google à mesma conta
- ❌ Não criar duplicidade de usuários
- ✅ Usuários Google não precisam de senha
- ✅ Usuários podem continuar usando login tradicional

### Endpoint

- `POST /auth/google`

Entrada:

```json
{
  "token": "google_credential_token"
}
```

Processamento:

- Validar token com Google
- Extrair dados do usuário
- Criar ou vincular conta
- Gerar JWT

Saída:

```json
{
  "access_token": "jwt_token",
  "user": {}
}
```

### Segurança

- ✅ Validar token do Google no backend (obrigatório)
- ❌ Nunca confiar apenas no frontend
- ✅ Utilizar HTTPS em todas as requisições
- ✅ Validar expiração do token
- ✅ Verificar issuer (Google)
- ✅ Sanitizar dados recebidos
- ✅ Logs de autenticação

### Frontend

Adicionar botão de login:

- "Continuar com Google"

Fluxo:

- abrir popup de autenticação
- receber token (credential)
- enviar para backend
- armazenar JWT retornado

### UX (Experiência do Usuário)

- Login com Google deve ser rápido e sem fricção
- Não solicitar dados duplicados após login
- Redirecionar diretamente para dashboard após autenticação
- Manter consistência com login tradicional

### Checklist de implementação

- [x] Criar credenciais no Google Cloud Console
- [x] Configurar OAuth Client ID
- [x] Implementar botão no frontend
- [x] Integrar Google Identity Services
- [x] Criar endpoint `/auth/google`
- [x] Validar token no backend
- [x] Implementar lógica de criação/vinculação de usuário
- [x] Gerar JWT após autenticação
- [x] Testar fluxo completo
- [x] Testar casos de usuário existente
- [x] Garantir ausência de duplicação de contas

### Evolução futura

- Adicionar login com Microsoft
- Adicionar login sem senha (magic link / OTP)
- Permitir vinculação de múltiplos provedores
- Dashboard de gerenciamento de contas vinculadas

### Observação crítica

O login social deve ser tratado como extensão do sistema atual de autenticação, não como um sistema separado.

A consistência da identidade do usuário (email único) é essencial para evitar problemas de duplicação e inconsistência de dados.

---

## 31. Fluxo de Autenticação e Estados da Aplicação

### Descrição

Definição completa dos fluxos de autenticação e dos estados da aplicação relacionados ao login, logout e sessão do usuário.

Esta seção garante consistência entre login tradicional (email + senha) e login social (Google), além de definir o comportamento do sistema em cenários de erro, expiração de sessão e navegação.

### Objetivos

- Garantir experiência consistente de login
- Evitar estados inválidos de autenticação
- Definir comportamento em todos os cenários possíveis
- Reduzir erros de UX
- Padronizar fluxos entre frontend e backend

### Estados da Aplicação

O sistema deve operar com os seguintes estados:

- Não autenticado
- Autenticando
- Autenticado
- Sessão expirada
- Erro de autenticação

### Fluxo de Login (Email + Senha)

```text
Usuário insere email e senha
        ↓
Frontend envia para /auth/login
        ↓
Backend valida credenciais
        ↓
Se válido:
    - retorna JWT
    - frontend salva token
    - redireciona para dashboard
Se inválido:
    - exibir erro ao usuário
```

### Fluxo de Login (Google)

```text
Usuário clica "Continuar com Google"
        ↓
Popup de autenticação Google
        ↓
Usuário autoriza
        ↓
Frontend recebe credential
        ↓
Envia para /auth/google
        ↓
Backend valida token
        ↓
Cria ou autentica usuário
        ↓
Retorna JWT
        ↓
Frontend salva token
        ↓
Redireciona para dashboard
```

### Fluxo de Sessão

Sessão ativa:

- JWT válido armazenado no frontend
- Usuário acessa rotas protegidas normalmente

Sessão expirada:

```text
Frontend faz requisição
        ↓
Backend retorna 401 (token expirado)
        ↓
Frontend:
    - limpa sessão
    - redireciona para login
    - exibe mensagem opcional
```

### Fluxo de Logout

- Remover token do frontend
- Limpar estado global do usuário
- Redirecionar para tela de login

### Persistência de sessão

- Token armazenado em memory (preferencial) ou localStorage (com cuidado)
- Validar token ao iniciar aplicação
- Caso inválido: forçar logout

### Tratamento de erros

Login inválido:

- Mensagem genérica: "Email ou senha inválidos"

Erro no Google login:

- Falha na autenticação → mostrar erro amigável
- Token inválido → rejeitar login

Falha de rede:

- Exibir mensagem: "Erro de conexão. Tente novamente."

API fora do ar:

- Mostrar fallback amigável
- Evitar travamento da UI

### Vinculação de contas

Cenário crítico:

Usuário já possui conta com email + senha e tenta login com Google.

Regra:

- Identificar por email
- Vincular conta Google à conta existente
- NÃO criar nova conta

### Regras globais

- Email é identificador único
- Não permitir duplicação de usuários
- Usuário autenticado não deve ver tela de login
- Rotas protegidas exigem autenticação

### Rotas protegidas

- Dashboard
- Treino
- Chat
- Histórico
- Perfil

Comportamento:

- Se não autenticado: redirecionar para login

### Redirecionamentos

- Login bem-sucedido → Dashboard
- Logout → Login
- Sessão expirada → Login
- Usuário já autenticado acessa `/login` → redirecionar para dashboard

### UX esperada

- Login rápido e sem fricção
- Feedback visual durante autenticação (loading)
- Erros claros e não técnicos
- Não exigir ações duplicadas
- Navegação fluida após login

### Cenários obrigatórios de teste

- Login com email válido
- Login com senha inválida
- Login com Google (novo usuário)
- Login com Google (usuário existente)
- Logout
- Token expirado
- API offline
- Requisição com token inválido

### Checklist de implementação

- [x] Definir estados globais de autenticação
- [x] Implementar controle de sessão no frontend
- [x] Criar interceptador para respostas 401
- [x] Implementar redirecionamentos automáticos
- [x] Garantir persistência de sessão
- [x] Tratar erros de login
- [x] Testar fluxo completo
- [x] Validar UX em mobile

### Evolução futura

- Refresh token automático
- Sessões simultâneas controladas
- Logout global (todos dispositivos)
- Autenticação multifator (MFA)

### Observação crítica

Autenticação não é apenas login — é o controle completo do estado do usuário dentro da aplicação.

Um fluxo mal definido pode gerar bugs críticos, problemas de segurança e má experiência do usuário.

---

## 32. Checklist de Go-Live em Produção

### Descrição

Checklist final obrigatório para validação antes da liberação do sistema para uso real pelos alunos da academia.

Esta seção garante que o sistema não apenas foi desenvolvido, mas também está operacional, seguro e estável em ambiente de produção.

### Objetivos

- Validar ambiente real de produção
- Reduzir risco de falhas após lançamento
- Garantir estabilidade para usuários reais
- Confirmar que todos os sistemas críticos estão funcionando

Status atual: execução iniciada com validações técnicas e evidências em ambiente local/staging-ready. Itens que dependem de operação real em produção permanecem pendentes.

### 🌐 1. Infraestrutura e Deploy

- [ ] Domínio configurado (`app.academia.com`)
- [ ] API publicada (`api.academia.com`)
- [ ] HTTPS ativo e válido
- [ ] DNS configurado corretamente
- [ ] Frontend acessível publicamente
- [ ] Backend acessível publicamente
- [x] Variáveis de ambiente configuradas
- [x] CORS configurado para domínio final
- [ ] WAF ativo (Cloudflare)

### 🗄️ 2. Banco de Dados

- [x] Banco em produção utilizando PostgreSQL
- [x] Conexão segura (SSL)
- [ ] Dados persistindo corretamente
- [x] Índices aplicados
- [ ] Teste de leitura e escrita validado
- [x] Nenhuma dependência de SQLite em produção

### 🔐 3. Segurança

- [x] Login protegido contra brute force
- [x] Rate limit ativo (login, chat, geração de treino)
- [x] JWT com expiração configurada
- [x] Refresh token implementado (se aplicável)
- [x] Senhas com hash bcrypt
- [x] CORS restrito corretamente
- [x] Headers de segurança aplicados
- [x] Tokens e secrets protegidos (env vars)
- [x] Validação de input em todos endpoints
- [x] Teste de acesso não autorizado (rotas protegidas)

### 🔑 4. Autenticação (Email + Google)

- [x] Login com email + senha funcionando
- [x] Login com Google funcionando
- [x] Token do Google validado no backend
- [x] Não há duplicação de contas por email
- [x] Vinculação de contas funcionando
- [x] Fluxo completo testado (login → dashboard)

### 🤖 5. IA (Treino e Chat)

- [x] Geração de treino funcionando
- [x] IA utilizando apenas exercícios da base
- [x] Estrutura JSON validada antes de salvar
- [x] Chat funcionando com memória básica
- [x] Timeout configurado para chamadas IA
- [x] Tratamento de erro da IA implementado
- [x] Sistema funcional mesmo com falha da IA (fallback)

### 📊 6. Observabilidade

- [x] Logs de autenticação funcionando
- [x] Logs de erro funcionando
- [x] Logs de geração de treino
- [ ] Monitoramento de uptime ativo
- [ ] Alertas configurados (falhas críticas)
- [x] Métricas básicas disponíveis

### 💾 7. Backup e Recuperação

- [ ] Backup automático configurado
- [x] Retenção de backups definida
- [ ] Teste de backup realizado
- [ ] Teste de restore realizado (obrigatório)

### ⚙️ 8. Performance e Carga

Evidência técnica: script dedicado `backend/scripts/load_test_critical_flows.py` implementado para carga concorrente de login, chat e geração de treino com métricas de latência/erro.

- [ ] Teste com múltiplos logins simultâneos
- [ ] Teste de geração de treino em carga
- [ ] Teste do chat com múltiplos usuários
- [ ] Tempo de resposta aceitável (< 2–3s)
- [ ] Backend sem erros sob carga moderada

### 📱 9. UX e Responsividade

- [ ] Login funcional no mobile
- [ ] Dashboard funcional no mobile
- [ ] Treino funcional no mobile
- [ ] Chat funcional no mobile
- [ ] Sem quebra de layout
- [ ] Navegação fluida
- [ ] Loading states implementados
- [ ] Mensagens de erro amigáveis

### 🔄 10. Fluxos Críticos

- [x] Cadastro → login → dashboard
- [x] Geração de treino completa
- [x] Histórico funcionando
- [x] Chat funcionando
- [x] Logout funcionando
- [x] Sessão expirada sendo tratada corretamente

### ⚖️ 11. LGPD e Privacidade

- [x] Política de privacidade publicada
- [x] Consentimento do usuário implementado
- [x] Opção de exclusão de conta funcional
- [x] Dados sensíveis protegidos
- [x] Fluxo de remoção de dados validado

### 🧪 12. Testes Finais

- [x] Teste completo do sistema ponta a ponta
- [ ] Teste com usuários reais (piloto)
- [ ] Teste em diferentes dispositivos
- [ ] Teste em diferentes navegadores
- [ ] Teste de falha de rede
- [ ] Teste de API fora do ar

### 🚀 13. Estratégia de Go-Live

Lançamento controlado:

- [ ] Liberar para grupo piloto (20–50 alunos)
- [ ] Coletar feedback
- [ ] Corrigir problemas críticos
- [ ] Expandir para 100 usuários
- [ ] Monitorar estabilidade
- [ ] Liberar para todos os alunos

### 🔥 Critério de aprovação

O sistema só deve ser liberado para produção completa quando:

- Todos os itens críticos estiverem validados
- Nenhum erro bloqueante estiver presente
- O sistema estiver estável sob uso real
- Logs, monitoramento e backup estiverem funcionando

### ⚠️ Observação crítica

Um sistema só está pronto para produção quando:

- Funciona corretamente
- É seguro
- É monitorável
- É recuperável em caso de falha

Desenvolvimento concluído não garante produção segura.

### 🧠 Definição de pronto para produção

“O sistema está pronto para produção quando pode falhar sem causar perda de dados, pode ser monitorado em tempo real e pode ser recuperado rapidamente.”

---

## 33. AI Orchestration Layer (Camada de Orquestração de IA)

### Descrição

Camada responsável por centralizar, controlar e padronizar todas as interações com o modelo de linguagem (LLM), garantindo consistência, segurança, rastreabilidade e controle de comportamento da IA.

Esta camada separa a lógica de negócio da lógica de IA, permitindo maior controle sobre prompts, contexto, parâmetros e respostas.

### Objetivos

- Centralizar chamadas para o LLM
- Controlar contexto enviado ao modelo
- Padronizar prompts
- Permitir ajustes sem impacto no restante do sistema
- Preparar o sistema para múltiplos modelos (futuro)
- Garantir previsibilidade das respostas

### Arquitetura

Controller / Endpoint  
        ↓  
AI Orchestration Layer  
        ↓  
Prompt Builder  
        ↓  
LLM Service (Groq)  
        ↓  
Response Handler  
        ↓  
Validation Layer  
        ↓  
Resposta final

### Componentes

#### 1. Prompt Builder

Responsável por:

- montar prompt base
- inserir contexto do usuário
- adicionar restrições
- incluir lista de exercícios filtrados

#### 2. Context Manager

Gerencia:

- dados do usuário
- histórico relevante
- restrições físicas
- objetivo do treino

#### 3. LLM Service

- integração com Groq
- envio de prompt
- recebimento de resposta

#### 4. Response Handler

Responsável por:

- parse da resposta (JSON)
- normalização de dados
- tratamento de erros

#### 5. Validation Layer

- validar estrutura da resposta
- garantir que exercícios existem na base
- bloquear dados inválidos
- evitar alucinação

### Regras obrigatórias

- ❌ Nenhum endpoint chama o LLM diretamente
- ✅ Toda chamada deve passar pela orchestration layer
- ✅ Respostas devem ser validadas antes de persistir
- ❌ Não confiar no output do modelo sem validação
- ✅ Contexto deve ser controlado e limitado

### Parâmetros controlados

A camada deve permitir controle de:

- temperatura
- max tokens
- modelo utilizado
- timeout
- retries

### Logs obrigatórios (IA)

- prompt enviado
- resposta recebida
- tempo de execução
- erro (se houver)

### Checklist de implementação

- [x] Criar service `ai_orchestrator.py`
- [x] Refatorar chamadas diretas ao LLM
- [x] Implementar Prompt Builder
- [x] Implementar Context Manager
- [x] Implementar Response Handler
- [x] Integrar com Validation Layer existente
- [x] Adicionar logs de IA
- [x] Testar fluxo completo

### Evolução futura

- suporte a múltiplos modelos (fallback)
- roteamento inteligente de chamadas
- otimização de custo por tipo de requisição
- cache de respostas
- A/B testing de prompts

---

## 34. Response Evaluation & Validation Engine

### Descrição

Mecanismo responsável por avaliar, validar e garantir a qualidade das respostas geradas pelo LLM antes de serem persistidas ou exibidas ao usuário.

Essa camada reduz riscos de alucinação, inconsistência e respostas inválidas.

### Objetivos

- Garantir integridade dos dados gerados pela IA
- Evitar respostas inválidas ou incoerentes
- Validar estrutura e conteúdo
- Implementar fallback automático
- Aumentar confiabilidade do sistema

### Arquitetura

LLM Response  
     ↓  
Parser (JSON)  
     ↓  
Schema Validation  
     ↓  
Business Validation  
     ↓  
Evaluation Score  
     ↓  
(Aprovado | Rejeitado | Retry)

### Tipos de validação

#### 1. Validação estrutural

- resposta deve estar em JSON válido
- campos obrigatórios presentes
- tipos corretos

#### 2. Validação de domínio

- exercícios devem existir na base
- respeitar restrições do usuário
- respeitar nível do usuário

#### 3. Validação semântica

- coerência do treino
- equilíbrio muscular
- lógica de séries e reps

### Estratégia de fallback

- resposta inválida → retry automático (até N vezes)
- fallback para prompt simplificado
- fallback para resposta padrão

### Score de qualidade (opcional avançado)

Cada resposta pode receber score baseado em:

- completude
- consistência
- aderência às regras

### Regras obrigatórias

- ❌ Nunca persistir resposta não validada
- ✅ Toda resposta deve passar por validação
- ✅ Sistema deve suportar retry automático
- ✅ Logs de validação devem ser registrados

### Checklist

- [x] Criar `response_evaluator.py`
- [x] Implementar validação estrutural
- [x] Implementar validação de domínio
- [x] Implementar retry automático
- [x] Integrar com orchestration layer
- [x] Criar logs de avaliação

---

## 35. Prompt Management & Versioning System

### Descrição

Sistema responsável por gerenciar, versionar e evoluir prompts utilizados pelo LLM, permitindo controle, rastreabilidade e melhoria contínua.

### Objetivos

- Controlar versões de prompts
- Permitir rollback
- Testar melhorias
- Garantir consistência entre versões

### Estrutura

```json
{
  "id": "string",
  "name": "generate_workout",
  "version": "v1",
  "content": "string",
  "created_at": "timestamp"
}
```

### Funcionalidades

- versionamento de prompt
- histórico de alterações
- rollback para versões anteriores
- associação de resposta com versão do prompt

### Uso no sistema

Cada chamada ao LLM deve registrar:

- versão do prompt utilizada
- contexto enviado
- resposta gerada

### Regras

- ❌ Não alterar prompt diretamente em código
- ✅ Prompts devem ser versionados
- ✅ Mudanças devem ser rastreáveis

### Checklist

- [x] Criar tabela `prompts`
- [x] Criar service `prompt_manager.py`
- [x] Implementar versionamento
- [x] Registrar versão em cada chamada
- [x] Permitir rollback

---

## 36. AI Observability & Monitoring

### Descrição

Camada de observabilidade focada especificamente em IA, permitindo monitorar comportamento, performance e qualidade das interações com o LLM.

### Objetivos

- Monitorar uso da IA
- Detectar falhas e inconsistências
- Medir performance
- Acompanhar custo

### Métricas obrigatórias

- tempo de resposta da IA
- número de chamadas
- taxa de erro
- taxa de retry
- custo estimado

### Logs obrigatórios

- prompt enviado
- resposta recebida
- tempo de execução
- erro (se houver)

### Alertas

- alta taxa de erro
- aumento de latência
- falha no LLM

### Regras

- ✅ Toda chamada de IA deve ser logada
- ✅ Logs devem ser estruturados
- ✅ Métricas devem ser monitoradas

### Checklist

- [x] Integrar logs de IA
- [x] Criar métricas específicas
- [x] Configurar alertas
- [x] Monitorar latência

---

## 37. Adaptive Learning & Feedback Intelligence

### Descrição

Sistema responsável por aprender com o comportamento e feedback do usuário, ajustando respostas da IA ao longo do tempo.

### Objetivos

- Personalizar experiência
- Adaptar treinos automaticamente
- Evoluir comportamento da IA

### Funcionalidades

- armazenar feedback do usuário
- ajustar contexto com base no histórico
- criar perfil comportamental

### Exemplo

Usuário prefere treino leve  
→ IA passa a priorizar isso automaticamente

### Regras

- ✅ Feedback deve influenciar geração futura
- ✅ Histórico deve ser considerado no contexto
- ❌ Não ignorar comportamento do usuário

### Checklist

- [x] Criar tabela de feedback
- [x] Integrar feedback no contexto
- [x] Ajustar prompt dinamicamente
- [x] Testar adaptação

---

## 38. Multi-step AI Pipeline (Pipeline de IA em Etapas)

### Descrição

Implementação de pipeline onde múltiplas chamadas ao LLM são feitas em etapas, aumentando qualidade e controle das respostas.

### Fluxo

1. Seleção de exercícios
2. Montagem do treino
3. Validação do treino

### Benefícios

- maior controle
- melhor qualidade
- menos erro

### Regras

- ❌ Não depender de única chamada para tarefas complexas
- ✅ Dividir problemas em etapas
- ✅ Validar cada etapa

### Checklist

- [x] Implementar pipeline multi-step
- [x] Separar responsabilidades por etapa
- [x] Integrar com validation engine
- [x] Testar fluxo completo

---

## 39. Resumo Executivo (Status 32 → 38)

### Entregas técnicas concluídas

- Seção 32: base de validação operacional reforçada com scripts de smoke e carga para fluxos críticos.
- Seção 33: orchestration layer implementada com separação de contexto, prompt, handler e validação.
- Seção 34: response evaluation engine ativa com validação estrutural e de domínio antes de persistência.
- Seção 35: prompt management versionado com registro de versões e trilha de execução.
- Seção 36: observabilidade de IA com métricas, latência, retries e alertas operacionais.
- Seção 37: adaptive learning com perfil comportamental baseado em feedback do usuário.
- Seção 38: pipeline multi-step em produção (seleção → montagem → validação).

### Benefícios já obtidos

- Maior previsibilidade e segurança nas respostas de IA.
- Redução de risco de alucinação por validação em múltiplas camadas.
- Rastreabilidade de prompts e execuções para auditoria e melhoria contínua.
- Base pronta para evolução com múltiplos modelos, fallback inteligente e otimização de custo.

### Pendências principais (fora do escopo puramente de código)

- Go-live operacional em ambiente público (domínio, DNS, HTTPS, WAF).
- Evidências finais de piloto com usuários reais e validações multi-dispositivo/multi-browser.
- Expansão controlada de rollout conforme checklist de produção.
