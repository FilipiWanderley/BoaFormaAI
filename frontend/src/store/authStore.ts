import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { AuthStatus, UserResponse } from '../types'

interface AuthState {
  token: string | null
  refreshToken: string | null
  user: UserResponse | null
  isAuthenticated: boolean
  status: AuthStatus
  error: string | null
  login: (accessToken: string, refreshToken: string, user: UserResponse) => void
  setUser: (user: UserResponse) => void
  setAuthenticating: () => void
  setAuthError: (message: string) => void
  setSessionExpired: () => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      status: 'nao_autenticado',
      error: null,
      login: (accessToken, refreshToken, user) => set({
        token: accessToken,
        refreshToken,
        user,
        isAuthenticated: true,
        status: 'autenticado',
        error: null,
      }),
      setUser: (user) => set({ user }),
      setAuthenticating: () => set({ status: 'autenticando', error: null }),
      setAuthError: (message) => set({ status: 'erro_autenticacao', error: message }),
      setSessionExpired: () => set({
        token: null,
        refreshToken: null,
        user: null,
        isAuthenticated: false,
        status: 'sessao_expirada',
        error: 'Sessão expirada. Faça login novamente.',
      }),
      logout: () => set({
        token: null,
        refreshToken: null,
        user: null,
        isAuthenticated: false,
        status: 'nao_autenticado',
        error: null,
      }),
    }),
    { name: 'boa-forma-auth' },
  ),
)
