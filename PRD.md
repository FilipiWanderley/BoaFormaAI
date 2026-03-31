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

- [ ] Definir provedor final de frontend e backend
- [ ] Provisionar Cloudflare (DNS + WAF + SSL)
- [ ] Provisionar Postgres gerenciado
- [ ] Configurar variáveis de ambiente de produção
- [ ] Validar arquitetura ponta a ponta em ambiente produtivo

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
- [ ] Configurar política de backup e restore testado
- [ ] Revisar endpoints para paginação consistente

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

- [ ] Configurar timeout e retry com política clara no serviço de IA
- [ ] Configurar pool de conexões para produção
- [ ] Definir fallback funcional para indisponibilidade do LLM
- [ ] Medir latência por endpoint crítico

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
- [ ] Integrar monitoramento de uptime
- [ ] Definir alertas de erro/latência
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

- [ ] Criar ambiente de staging completo
- [x] Configurar pipeline CI/CD com gates de qualidade
- [ ] Definir estratégia de rollback
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

- [ ] Configurar subdomínios de frontend e backend
- [ ] Configurar certificados SSL
- [ ] Validar CORS e cookies/tokens com domínio final

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
- [ ] Estratégia de cache offline robusta
- [ ] UX de instalação guiada (prompt install)

---

## 25. Testes de Produção

### Tipos

- testes de carga (simular usuários)
- testes de segurança
- testes de API
- testes de fluxo completo

### Checklist de implementação

- [ ] Definir suíte de testes de carga
- [ ] Definir suíte de segurança (OWASP básico)
- [ ] Automatizar smoke tests de produção
- [ ] Definir critérios de aceitação por ambiente

---

## 26. Backup e Recuperação

### Requisitos

- backup automático diário
- retenção de backups
- teste de restore

### Checklist de implementação

- [ ] Configurar backup diário no banco gerenciado
- [ ] Definir janela de retenção
- [ ] Executar restore de teste e documentar procedimento

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

- [ ] Implementar fluxo de consentimento
- [ ] Publicar política de privacidade
- [ ] Implementar exclusão de conta/dados
- [ ] Definir política de retenção e minimização de dados

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

- [ ] Estimar custo mensal por ambiente
- [ ] Definir orçamento e limites de consumo
- [ ] Configurar alertas de custo (quando disponível)

---

## 29. Roadmap Pós-Produção

- versão PWA
- vídeos próprios da academia
- painel admin
- recomendação inteligente
- integração com wearables
