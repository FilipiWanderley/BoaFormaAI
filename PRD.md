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
- [ ] Criar tabela `users`
- [ ] Implementar cadastro (`POST /users`)
- [ ] Implementar login (`POST /auth/login`)
- [ ] Hash de senha (bcrypt)
- [ ] JWT
- [ ] Middleware de autenticação

---

### 3.2 Geração de Treino com IA

**Checklist:**
- [ ] Criar endpoint `POST /workout/generate`
- [ ] Criar prompt base
- [ ] Integrar Groq
- [ ] Estruturar resposta (JSON)
- [ ] Salvar treino no banco

---

### 3.3 Dashboard

**Checklist:**
- [ ] Criar endpoint `GET /dashboard`
- [ ] Retornar treino do dia
- [ ] Retornar progresso
- [ ] Criar tela frontend

---

### 3.4 Histórico

**Checklist:**
- [ ] Criar tabela `history`
- [ ] Criar endpoint `GET /history/{user_id}`
- [ ] Criar endpoint `POST /history`
- [ ] Conectar com treino

---

### 3.5 Chat com IA

**Checklist:**
- [ ] Criar endpoint `POST /chat`
- [ ] Criar memória básica
- [ ] Integrar com LLM
- [ ] Salvar histórico

---

### 3.6 Adaptação Inteligente

**Checklist:**
- [ ] Criar lógica de feedback
- [ ] Ajustar prompt com histórico
- [ ] Regerar treino com base no feedback

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
- [ ] Criar estrutura de pastas backend
- [ ] Criar estrutura frontend
- [ ] Definir padrões de código
- [ ] Separar responsabilidades

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
- [ ] Definir schemas (Pydantic)
- [ ] Implementar validação
- [ ] Testar endpoints no Swagger
- [ ] Criar tratamento de erro

---

## 6. IA (GenAI)

- **LLM:** Groq
- **Embeddings:** local
- **Arquivo principal:** `llm_service.py`

**Checklist:**
- [ ] Criar `llm_service.py`
- [ ] Criar prompt base
- [ ] Criar prompt com contexto
- [ ] Testar respostas
- [ ] Ajustar qualidade
- [ ] Evitar prompt injection básico

---

## 7. Banco de Dados

- **Engine:** SQLite
- **Tabelas:** `users`, `workouts`, `history`, `exercises`, `workout_exercises`

**Checklist:**
- [ ] Criar SQLite
- [ ] Criar models
- [ ] Criar migrations (opcional)
- [ ] Testar persistência

---

## 8. Segurança

- JWT
- Hash de senha (bcrypt)
- Validação de inputs

**Checklist:**
- [ ] Implementar bcrypt
- [ ] Implementar JWT
- [ ] Proteger rotas
- [ ] Validar dados de entrada
- [ ] Evitar prompt injection básico

---

## 9. Frontend — Telas

- Login
- Dashboard
- Treino
- Chat
- Histórico
- Perfil

**Checklist:**
- [ ] Criar layout base
- [ ] Criar navegação
- [ ] Integrar com API
- [ ] Criar estados (loading/error)
- [ ] Testar fluxo completo

---

## 10. UI (Figma)

**Checklist:**
- [ ] Subir app funcional
- [ ] Validar todas as telas
- [ ] Importar referências do Figma
- [ ] Ajustar layout
- [ ] Criar design system
- [ ] Padronizar componentes

---

## 11. Deploy (Opcional)

**Checklist:**
- [ ] Dockerizar backend
- [ ] Deploy simples (Render/Vercel)
- [ ] Configurar variáveis de ambiente

---

## 12. Testes

**Checklist:**
- [ ] Testar endpoints
- [ ] Testar fluxo completo
- [ ] Testar IA
- [ ] Testar erros

---

## 13. Roadmap de Execução

### Fase 1 — Base
- [ ] Estrutura backend
- [ ] Banco de dados
- [ ] Autenticação

### Fase 1.5 — Exercise Library
- [ ] Escolher fonte de dados (API ou dataset)
- [ ] Criar tabelas `exercises` e `workout_exercises`
- [ ] Importar dados iniciais
- [ ] Criar service de exercícios com filtros

### Fase 2 — IA
- [ ] Geração de treino
- [ ] Integração LLM (Groq)
- [ ] IA seleciona da base, não inventa exercícios

### Fase 3 — Funcionalidade
- [ ] Dashboard
- [ ] Histórico
- [ ] Chat

### Fase 4 — Frontend
- [ ] Telas
- [ ] Integração com API

### Fase 5 — UI
- [ ] Aplicar Figma
- [ ] Design system

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
- [ ] Escolher fonte de dados (API ou dataset)
- [ ] Criar tabela `exercises`
- [ ] Criar tabela `workout_exercises`
- [ ] Importar dados iniciais
- [ ] Criar service com filtros por músculo, equipamento e nível
- [ ] Integrar filtro com geração de treino
- [ ] Garantir que IA usa apenas exercícios da base
- [ ] Adicionar campo de mídia (URL de imagem/GIF)
- [ ] Testar exibição no frontend

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
- [x] Popular banco com dados iniciais (59 exercícios — base MVP)
- [x] Criar service de exercícios (`services/exercise.py`)
- [x] Implementar filtro por músculo
- [x] Implementar filtro por equipamento
- [x] Implementar filtro por nível (com progressão: avancado acessa todos)
- [x] Implementar filtro por restrições físicas (keyword matching)
- [ ] Expandir base para 200+ exercícios
- [ ] Integrar com geração de treino (Fase 2)
- [ ] Atualizar prompt da IA para usar exercícios da base
- [ ] Validar saída da IA (nenhum exercício inventado)
- [ ] Adicionar campo de mídia (image_url já presente)
- [ ] Testar exibição no frontend

### Evolução futura

- Adicionar vídeos próprios da academia
- Permitir upload de mídia pelo admin
- Criar recomendações baseadas em desempenho
- Integrar com sensores ou wearables

---

## Checklist Final (Nível Portfólio)

- [ ] App funcionando ponta a ponta
- [ ] IA integrada
- [ ] Autenticação
- [ ] Banco persistente
- [ ] UI moderna
- [ ] README profissional
- [ ] Deploy (opcional)
