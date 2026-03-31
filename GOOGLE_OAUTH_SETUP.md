# Configuração Google OAuth (Produção e Staging)

## 1) Criar projeto e OAuth no Google Cloud

1. Acesse Google Cloud Console.
2. Crie (ou selecione) o projeto da aplicação.
3. Ative API: **Google Identity Services / OAuth**.
4. Vá em **APIs e Serviços > Credenciais**.
5. Crie **ID do cliente OAuth 2.0** (tipo Web application).

## 2) Configurar origens/autorização

Adicione nas origens JavaScript autorizadas:

- `http://localhost:5173`
- `https://staging.app.academia.com`
- `https://app.academia.com`

Adicione nos URIs autorizados (se aplicável ao seu fluxo):

- `https://staging.app.academia.com`
- `https://app.academia.com`

## 3) Configurar variáveis de ambiente

Backend:

- `GOOGLE_OAUTH_CLIENT_ID=<client_id_google>`

Frontend:

- `VITE_GOOGLE_CLIENT_ID=<client_id_google>`

## 4) Validar fluxo end-to-end

1. Abrir tela de login.
2. Clicar em **Continuar com Google**.
3. Autorizar conta.
4. Confirmar redirecionamento ao dashboard.
5. Confirmar que usuário existente por email foi vinculado (sem duplicar conta).
