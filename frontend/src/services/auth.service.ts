import { api } from './api'
import type { TokenResponse, UserCreate, UserResponse } from '../types'

export const authService = {
  login: async (email: string, password: string): Promise<TokenResponse> => {
    const { data } = await api.post<TokenResponse>('/auth/login', { email, password })
    return data
  },

  register: async (payload: UserCreate): Promise<UserResponse> => {
    const { data } = await api.post<UserResponse>('/users', payload)
    return data
  },

  me: async (token?: string): Promise<UserResponse> => {
    const { data } = await api.get<UserResponse>('/users/me', {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    })
    return data
  },

  updateMe: async (payload: Partial<UserCreate>): Promise<UserResponse> => {
    const { data } = await api.patch<UserResponse>('/users/me', payload)
    return data
  },
}
