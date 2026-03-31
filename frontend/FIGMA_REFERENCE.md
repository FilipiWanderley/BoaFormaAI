# Referências de Figma Aplicadas

## Objetivo

Documentar a tradução das referências visuais do produto para o código, mantendo consistência entre telas, componentes e tokens.

## Direções visuais aplicadas

- Estética dark premium com contraste alto.
- Hierarquia tipográfica enxuta para títulos, subtítulos e métricas.
- Cards de superfície com borda suave e elevação discreta.
- Chamadas primárias em azul (`accent`) e estados neutros em `surface`.
- Estados vazios e headers de página padronizados.

## Mapeamento Figma → Código

- Header de páginas: `src/components/ui/PageHeader.tsx`
- Empty state: `src/components/ui/EmptyState.tsx`
- Ações e CTA: `src/components/ui/Button.tsx`
- Inputs e campos de formulário: `src/components/ui/Input.tsx`
- Containers de conteúdo: `src/components/ui/Card.tsx`
- Sinalização de status: `src/components/ui/Badge.tsx`
- Tokens globais: `tailwind.config.js`

## Telas consolidadas

- Login / Register
- Dashboard
- Workout
- Chat
- History
- Profile

## Próximo refinamento visual

- Evoluir catálogo visual com variações de componente por densidade e breakpoints.
