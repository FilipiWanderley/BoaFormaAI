import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

type AuthState = {
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  status: 'nao_autenticado' | 'autenticando' | 'autenticado' | 'sessao_expirada' | 'erro_autenticacao'
  error: string | null
}

const authState: AuthState = {
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  status: 'nao_autenticado',
  error: null,
}

const setSessionExpiredMock = vi.fn(() => {
  authState.token = null
  authState.refreshToken = null
  authState.isAuthenticated = false
  authState.status = 'sessao_expirada'
  authState.error = 'Sessao expirada. Faca login novamente.'
})

vi.mock('../store/authStore', () => {
  return {
    useAuthStore: {
      getState: () => ({
        token: authState.token,
        refreshToken: authState.refreshToken,
        isAuthenticated: authState.isAuthenticated,
        status: authState.status,
        error: authState.error,
        setSessionExpired: setSessionExpiredMock,
      }),
      setState: (partial: Partial<AuthState>) => {
        Object.assign(authState, partial)
      },
    },
  }
})

const API_BASE_URL = 'http://localhost:8000'

function resetAuthState(): void {
  authState.token = 'expired-access'
  authState.refreshToken = 'valid-refresh'
  authState.isAuthenticated = true
  authState.status = 'autenticado'
  authState.error = null
}

describe('api interceptor refresh flow', () => {
  let apiMock: MockAdapter
  let axiosMock: MockAdapter

  beforeEach(async () => {
    vi.resetModules()
    setSessionExpiredMock.mockClear()
    resetAuthState()

    ;(globalThis as { window?: { location: { href: string } } }).window = {
      location: { href: '/dashboard' },
    }

    const { api } = await import('./api')
    apiMock = new MockAdapter(api)
    axiosMock = new MockAdapter(axios)
  })

  afterEach(() => {
    apiMock.restore()
    axiosMock.restore()
    delete (globalThis as { window?: unknown }).window
  })

  it('renova token e reexecuta request apos 401', async () => {
    apiMock.onGet('/protected').replyOnce(401)
    apiMock.onGet('/protected').replyOnce((config) => {
      return [200, { ok: true, auth: config.headers?.Authorization }]
    })

    axiosMock.onPost(`${API_BASE_URL}/auth/refresh`).reply(200, {
      access_token: 'new-access-token',
      refresh_token: 'new-refresh-token',
      token_type: 'bearer',
    })

    const { api } = await import('./api')
    const response = await api.get('/protected')

    expect(response.status).toBe(200)
    expect(response.data.ok).toBe(true)
    expect(response.data.auth).toBe('Bearer new-access-token')
    expect(axiosMock.history.post).toHaveLength(1)
    expect(authState.token).toBe('new-access-token')
    expect(authState.refreshToken).toBe('new-refresh-token')
    expect(setSessionExpiredMock).not.toHaveBeenCalled()
  })

  it('com requests concorrentes, faz apenas um refresh', async () => {
    apiMock.onGet('/resource-a').replyOnce(401)
    apiMock.onGet('/resource-a').replyOnce(200, { ok: 'a' })
    apiMock.onGet('/resource-b').replyOnce(401)
    apiMock.onGet('/resource-b').replyOnce(200, { ok: 'b' })

    axiosMock.onPost(`${API_BASE_URL}/auth/refresh`).reply(
      () => new Promise((resolve) => {
        setTimeout(() => {
          resolve([
            200,
            {
              access_token: 'shared-access-token',
              refresh_token: 'shared-refresh-token',
              token_type: 'bearer',
            },
          ])
        }, 20)
      }),
    )

    const { api } = await import('./api')
    const [a, b] = await Promise.all([api.get('/resource-a'), api.get('/resource-b')])

    expect(a.data.ok).toBe('a')
    expect(b.data.ok).toBe('b')
    expect(axiosMock.history.post).toHaveLength(1)
    expect(authState.token).toBe('shared-access-token')
    expect(authState.refreshToken).toBe('shared-refresh-token')
  })

  it('expira sessao quando refresh falha', async () => {
    apiMock.onGet('/protected').replyOnce(401)
    axiosMock.onPost(`${API_BASE_URL}/auth/refresh`).reply(401)

    const { api } = await import('./api')

    await expect(api.get('/protected')).rejects.toBeTruthy()

    const windowRef = (globalThis as { window?: { location: { href: string } } }).window

    expect(setSessionExpiredMock).toHaveBeenCalledTimes(1)
    expect(authState.status).toBe('sessao_expirada')
    expect(windowRef?.location.href).toBe('/login')
  })
})
