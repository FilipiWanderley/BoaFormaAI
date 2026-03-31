# Design System — Boa Forma AI

## Princípios

- Interface escura premium com alto contraste para legibilidade.
- Componentes reutilizáveis com API simples e previsível.
- Hierarquia visual consistente entre páginas, cards e estados.

## Tokens de Cor (Tailwind)

Definidos em `tailwind.config.js`:

- `surface.0` a `surface.4` para planos de fundo e elevação.
- `border`, `border.hover`, `border.strong` para contornos.
- `text.primary`, `text.secondary`, `text.tertiary` para níveis de leitura.
- `accent`, `accent.hover`, `accent.muted`, `accent.border` para ações e foco.

## Tipografia

- Fonte principal: `Inter` (`fontFamily.sans`).
- Escala de títulos baseada em `text-[28px]` para headers principais.
- Corpo e labels em `text-[11px]` a `text-[15px]` com opacidade contextual.

## Componentes base

- `Button`: variantes `primary`, `secondary`, `ghost`, `danger` + tamanhos `sm`, `md`, `lg`.
- `Input`: label/erro integrados, foco consistente e estados de borda.
- `Card`: base visual única para contêineres de conteúdo.
- `Badge`: semântica visual para status/contexto.
- `PageHeader`: padrão de cabeçalho de página.
- `EmptyState`: padrão único para telas vazias.
- `Spinner` e `RingProgress`: feedback de carregamento e progresso.

## Regras de composição

- Usar `PageHeader` em páginas principais para título/subtítulo/ação à direita.
- Usar `EmptyState` em listas/áreas vazias em vez de markup ad-hoc.
- Evitar cores hardcoded (`gray-*`, `blue-*`) quando houver token equivalente.
- Priorizar `surface-*`, `border-*`, `text-*`, `accent-*` para consistência.

## Próxima evolução

- Mapear referências de Figma para tokens de espaçamento e tipografia avançada.
- Criar catálogo visual de componentes com variações por estado.
