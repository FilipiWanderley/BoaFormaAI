# Google Cloud OAuth Setup (Produção)

## Objetivo

Configurar credenciais oficiais de login Google para o domínio final da aplicação.

## Passo a passo

1. Criar/selecionar projeto no Google Cloud Console.
2. Configurar consent screen OAuth com dados da aplicação.
3. Criar credencial OAuth 2.0 do tipo **Web application**.
4. Registrar origens autorizadas:
   - `https://app.academia.com`
   - `https://staging.app.academia.com`
   - `http://localhost:5173`
5. Registrar redirecionamentos autorizados (se necessário ao fluxo):
   - `https://app.academia.com`
   - `https://staging.app.academia.com`
6. Copiar `Client ID` e configurar:
   - Backend: `GOOGLE_OAUTH_CLIENT_ID`
   - Frontend: `VITE_GOOGLE_CLIENT_ID`

## Checklist de validação

- [ ] Login Google funciona para usuário novo
- [ ] Login Google vincula conta existente por email
- [ ] Token inválido é rejeitado no backend
- [ ] Fluxo mantém redirecionamento para dashboard

## Referências internas

- `GOOGLE_OAUTH_SETUP.md`
- `PRIVACY_POLICY.md`
