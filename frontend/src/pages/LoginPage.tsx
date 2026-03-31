import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, ArrowRight } from 'lucide-react'
import { authService } from '../services/auth.service'
import { useAuthStore } from '../store/authStore'

const schema = z.object({
  email:    z.string().email('Email inválido'),
  password: z.string().min(1, 'Informe a senha'),
})
type FormData = z.infer<typeof schema>

const inputCls = "w-full bg-surface-3 border border-white/[0.08] rounded-xl px-4 py-3 pl-11 text-[14px] text-white placeholder-white/25 focus:outline-none focus:border-accent/50 focus:ring-0 transition-colors"

export function LoginPage() {
  const navigate  = useNavigate()
  const login     = useAuthStore((s) => s.login)
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const status = useAuthStore((s) => s.status)
  const authError = useAuthStore((s) => s.error)
  const setAuthenticating = useAuthStore((s) => s.setAuthenticating)
  const setAuthError = useAuthStore((s) => s.setAuthError)
  const [showForm, setShowForm] = useState(false)
  const [googleReady, setGoogleReady] = useState(false)
  const [termsAccepted, setTermsAccepted] = useState(false)
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true })
    }
  }, [isAuthenticated, navigate])

  useEffect(() => {
    if (!googleClientId) return
    const scriptId = 'google-identity-services'
    const existing = document.getElementById(scriptId) as HTMLScriptElement | null
    if (existing) {
      setGoogleReady(true)
      return
    }
    const script = document.createElement('script')
    script.id = scriptId
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = () => setGoogleReady(true)
    document.head.appendChild(script)
  }, [googleClientId])

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const mutation = useMutation({
    mutationFn: async (data: FormData) => {
      setAuthenticating()
      const token = await authService.login(data.email, data.password)
      const user  = await authService.me(token.access_token)
      return { token, user }
    },
    onSuccess: ({ token, user }) => {
      login(token.access_token, token.refresh_token, user)
      navigate('/dashboard')
    },
    onError: () => {
      setAuthError('Email ou senha inválidos.')
    },
  })

  const handleGoogleLogin = () => {
    if (!termsAccepted) {
      setAuthError('Aceite a política de privacidade para continuar com Google.')
      return
    }
    if (!googleClientId || !googleReady || !(window as any).google?.accounts?.id) {
      setAuthError('Login Google indisponível no momento.')
      return
    }
    setAuthenticating()
    ;(window as any).google.accounts.id.initialize({
      client_id: googleClientId,
      callback: async (response: { credential?: string }) => {
        try {
          if (!response.credential) {
            setAuthError('Falha na autenticação com Google.')
            return
          }
          const result = await authService.googleLogin(response.credential, '2026-01')
          login(result.access_token, result.refresh_token, result.user)
          navigate('/dashboard')
        } catch {
          setAuthError('Falha na autenticação com Google.')
        }
      },
      ux_mode: 'popup',
    })
    ;(window as any).google.accounts.id.prompt()
  }

  return (
    <div className="min-h-screen flex bg-surface-0">

      {/* ── Left panel ───────────────────────────────────── */}
      <div className="hidden lg:flex w-[46%] flex-col justify-between p-14 relative overflow-hidden border-r border-white/[0.05]">

        {/* Very subtle radial on top-left */}
        <div className="pointer-events-none absolute top-0 left-0 w-[500px] h-[500px] rounded-full"
          style={{ background: 'radial-gradient(circle at top left, rgba(37,99,235,0.07) 0%, transparent 65%)' }}
        />

        {/* Logo */}
        <div className="relative flex items-center">
          <img
            src="/Logo_Branca.svg"
            alt="BoaForma AI"
            className="h-20 w-auto max-w-[380px] object-contain"
            loading="eager"
          />
        </div>

        {/* Headline */}
        <div className="relative">
          <h1 className="text-[52px] font-semibold text-white leading-[1.05] tracking-[-2px] mb-5">
            Treinos feitos<br />
            para você,<br />
            <span className="text-white/30">pela IA.</span>
          </h1>
          <p className="text-[15px] text-white/40 leading-relaxed max-w-[340px]">
            Cada sessão personalizada com base no seu perfil, nível e objetivos. Sem achismos.
          </p>
        </div>

        {/* Bottom testimonial/stat */}
        <div className="relative border-t border-white/[0.06] pt-6 flex items-center gap-8">
          <div>
            <p className="text-[28px] font-semibold text-white tracking-tight">200+</p>
            <p className="text-[12px] text-white/35 mt-0.5">exercícios disponíveis</p>
          </div>
          <div className="w-px h-8 bg-white/[0.06]" />
          <div>
            <p className="text-[28px] font-semibold text-white tracking-tight">IA</p>
            <p className="text-[12px] text-white/35 mt-0.5">treinos adaptativos</p>
          </div>
        </div>
      </div>

      {/* ── Right panel ──────────────────────────────────── */}
      <div className="flex-1 flex items-center justify-center p-10">
        <div className="w-full max-w-[380px]">

          {/* Mobile logo */}
          <div className="lg:hidden mb-8 flex justify-center">
            <img
              src="/Logo_Branca.svg"
              alt="BoaForma AI"
              className="h-16 w-auto max-w-[320px] object-contain"
              loading="eager"
            />
          </div>

          <h2 className="text-[22px] font-semibold text-white tracking-tight mb-1">
            Bem-vindo de volta
          </h2>
          <p className="text-[14px] text-white/40 mb-8">
            Entre na sua conta para continuar
          </p>

          {showForm ? (
            <div className="flex flex-col gap-3 mb-5">
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/25" />
                <input {...register('email')} type="email" placeholder="seu@email.com" className={inputCls} />
                {errors.email && <p className="text-[11px] text-red-400 mt-1">{errors.email.message}</p>}
              </div>

              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/25" />
                <input {...register('password')} type="password" placeholder="••••••••" className={inputCls} />
                {errors.password && <p className="text-[11px] text-red-400 mt-1">{errors.password.message}</p>}
              </div>

              {(mutation.isError || status === 'erro_autenticacao' || status === 'sessao_expirada') && (
                <p className="text-[13px] text-red-400/80 text-center pt-1">{authError || 'Falha na autenticação.'}</p>
              )}

              <button
                onClick={handleSubmit((d) => mutation.mutate(d))}
                disabled={mutation.isPending || status === 'autenticando'}
                className="mt-1 w-full h-[44px] bg-accent hover:bg-accent-hover rounded-xl flex items-center justify-center gap-2 text-[14px] font-medium text-white transition-colors disabled:opacity-50"
              >
                {mutation.isPending || status === 'autenticando' ? 'Entrando...' : (
                  <>Entrar <ArrowRight className="w-4 h-4" /></>
                )}
              </button>
            </div>
          ) : (
            <div className="flex flex-col gap-3 mb-5">
              <label className="flex items-start gap-2 rounded-xl border border-white/[0.08] bg-surface-3 px-3 py-2 text-[12px] text-white/70">
                <input
                  type="checkbox"
                  checked={termsAccepted}
                  onChange={(event) => setTermsAccepted(event.target.checked)}
                  className="mt-0.5"
                />
                <span>
                  Li e aceito a política de privacidade.
                  <a href="/privacy-policy.html" target="_blank" rel="noreferrer" className="ml-1 text-accent hover:text-accent-hover">
                    Ver política
                  </a>
                </span>
              </label>
              <button
                onClick={handleGoogleLogin}
                disabled={!googleClientId || status === 'autenticando' || !termsAccepted}
                className="w-full h-[44px] bg-white text-black rounded-xl flex items-center justify-center gap-2 text-[14px] font-medium transition-colors disabled:opacity-50"
              >
                Continuar com Google
              </button>
              <button
                onClick={() => setShowForm(true)}
                className="w-full h-[44px] bg-accent hover:bg-accent-hover rounded-xl flex items-center justify-center gap-2 text-[14px] font-medium text-white transition-colors"
              >
                <Mail className="w-4 h-4" />
                Entrar com Email
              </button>
            </div>
          )}

          <Link
            to="/register"
            className="flex w-full h-[44px] items-center justify-center bg-surface-3 border border-white/[0.08] hover:border-white/[0.14] rounded-xl text-[14px] font-medium text-white/70 hover:text-white transition-colors"
          >
            Criar nova conta
          </Link>

          <p className="text-center text-[13px] text-white/30 mt-7">
            Novo por aqui?{' '}
            <Link to="/register" className="text-white/60 hover:text-white transition-colors">
              Criar conta grátis
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
