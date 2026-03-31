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
- [ ] Importar referências do Figma
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
- [ ] Aplicar Figma
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
| Avançada | 500–1500+ exercícios |

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
- [x] Expandir base para 200+ exercícios
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
- [ ] Deploy (opcional)
