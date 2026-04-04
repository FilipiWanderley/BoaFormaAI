import axios from 'axios'
import type { AxiosError, InternalAxiosRequestConfig } from 'axios'
import type { TokenResponse } from '../types'
import { useAuthStore } from '../store/authStore'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

type RetryableRequestConfig = InternalAxiosRequestConfig & { _retry?: boolean }

let refreshPromise: Promise<string | null> | null = null

function redirectToLogin(): void {
  if (typeof window !== 'undefined') {
    window.location.href = '/login'
  }
}

function expireSession(): void {
  useAuthStore.getState().setSessionExpired()
  redirectToLogin()
}

function isRefreshRequest(url?: string): boolean {
  return (url ?? '').includes('/auth/refresh')
}

async function requestTokenRefresh(): Promise<string | null> {
  const refreshToken = useAuthStore.getState().refreshToken
  if (!refreshToken) return null

  try {
    const { data } = await axios.post<TokenResponse>(`${API_BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    })

    useAuthStore.setState({
      token: data.access_token,
      refreshToken: data.refresh_token,
      isAuthenticated: true,
      status: 'autenticado',
      error: null,
    })

    return data.access_token
  } catch {
    return null
  }
}

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (err: AxiosError) => {
    const originalRequest = err.config as RetryableRequestConfig | undefined
    const statusCode = err.response?.status

    if (!originalRequest || statusCode !== 401) {
      return Promise.reject(err)
    }

    if (originalRequest._retry || isRefreshRequest(originalRequest.url)) {
      expireSession()
      return Promise.reject(err)
    }

    if (!useAuthStore.getState().refreshToken) {
      expireSession()
      return Promise.reject(err)
    }

    originalRequest._retry = true

    if (!refreshPromise) {
      refreshPromise = requestTokenRefresh().finally(() => {
        refreshPromise = null
      })
    }

    const newAccessToken = await refreshPromise

    if (!newAccessToken) {
      expireSession()
      return Promise.reject(err)
    }

    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
    return api(originalRequest)
  },
)
