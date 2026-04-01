# Architecture Decisions (ADR-style)

## ADR-001 — FastAPI + SQLAlchemy no backend

- **Decisão:** adotar FastAPI com SQLAlchemy 2.x e Pydantic 2.
- **Motivo:** produtividade alta, tipagem forte, documentação OpenAPI nativa e ótimo suporte para APIs de produto.
- **Trade-off:** menor ecossistema corporativo que frameworks tradicionais em Java/.NET.

## ADR-002 — React + TypeScript + Vite no frontend

- **Decisão:** usar React com TypeScript e Vite.
- **Motivo:** DX rápida, build moderno, tipagem ponta a ponta e fácil evolução para PWA.
- **Trade-off:** maior disciplina necessária em organização de estado/cache.

## ADR-003 — JWT + Refresh Token com rotação

- **Decisão:** autenticação stateless via JWT com refresh token rotativo.
- **Motivo:** segurança melhor para sessões longas, invalidação seletiva e boa UX.
- **Trade-off:** fluxo mais complexo de sessão e persistência de tokens de refresh.

## ADR-004 — Resiliência para LLM (timeout/retry/fallback)

- **Decisão:** chamadas de IA com timeout, retry com backoff e fallback determinístico.
- **Motivo:** manter funcionalidade do produto mesmo com degradação do provedor de IA.
- **Trade-off:** fallback pode reduzir qualidade semântica comparado ao LLM em pleno funcionamento.

## ADR-005 — Segurança por camadas na API

- **Decisão:** combinar lockout, rate limiting, headers de segurança, CORS restrito e trusted hosts.
- **Motivo:** reduzir vetores de abuso e harden da API para ambiente público.
- **Trade-off:** risco de falso positivo em limites agressivos.

## ADR-006 — Operação orientada a runbooks

- **Decisão:** manter playbooks e checklists de deploy, rollback, backup e go-live no repositório.
- **Motivo:** reprodutibilidade operacional e redução de erro humano.
- **Trade-off:** exige disciplina contínua de atualização documental.

## ADR-007 — Banco local SQLite e produção PostgreSQL

- **Decisão:** SQLite no desenvolvimento local e PostgreSQL gerenciado em produção.
- **Motivo:** simplicidade local e robustez/escala em produção.
- **Trade-off:** pequenas diferenças de comportamento SQL entre ambientes.
