import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { User, Mail, Lock, ChevronRight, ChevronLeft, Dumbbell, TrendingUp, Zap } from 'lucide-react'
import { authService } from '../services/auth.service'
import { useAuthStore } from '../store/authStore'

const schema = z.object({
  name:         z.string().min(4, 'Informe nome e sobrenome'),
  email:        z.string().email('Email inválido'),
  password:     z.string().min(8, 'Mínimo 8 caracteres'),
  age:          z.coerce.number().int().min(10).max(100),
  weight_kg:    z.coerce.number().min(20).max(300),
  height_cm:    z.coerce.number().min(100).max(250),
  goal:         z.string().min(3, 'Descreva seu objetivo'),
  level:        z.enum(['iniciante', 'intermediario', 'avancado']),
  restrictions: z.string().optional(),
  accept_terms: z.literal(true, { errorMap: () => ({ message: 'Você precisa aceitar os termos.' }) }),
  privacy_policy_version: z.string().default('2026-01'),
})
type FormData = z.infer<typeof schema>

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-[12px] font-medium text-[#b3b3b3]">{label}</label>
      {children}
      {error && <p className="text-[11px] text-red-400">{error}</p>}
    </div>
  )
}

const inputCls = "w-full bg-[#252525] border border-[#333] rounded-[10px] px-4 py-2.5 text-[14px] text-white placeholder-[#555] focus:outline-none focus:border-[#1e3fb9] focus:ring-1 focus:ring-[#1e3fb9]/30 transition-colors"

const FEATURES = [
  { icon: Dumbbell,   label: 'Treinos gerados por IA' },
  { icon: TrendingUp, label: 'Progresso em tempo real' },
  { icon: Zap,        label: 'Resultados comprovados' },
]

export function RegisterPage() {
  const navigate  = useNavigate()
  const login     = useAuthStore((s) => s.login)
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const [step, setStep] = useState<1 | 2>(1)

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true })
    }
  }, [isAuthenticated, navigate])

  const { register, handleSubmit, formState: { errors }, trigger } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { level: 'iniciante', privacy_policy_version: '2026-01' },
  })

  const mutation = useMutation({
    mutationFn: async (data: FormData) => {
      await authService.register(data)
      const token = await authService.login(data.email, data.password)
      const user  = await authService.me()
      return { token, user }
    },
    onSuccess: ({ token, user }) => {
      login(token.access_token, token.refresh_token, user)
      navigate('/dashboard')
    },
  })

  const goNext = async () => {
    const valid = await trigger(['name', 'email', 'password'])
    if (valid) setStep(2)
  }

  return (
    <div className="min-h-screen flex bg-[#1a1a1a]">

      {/* ── Left panel ───────────────────────────────────── */}
      <div className="hidden lg:flex w-[42%] bg-[#111] flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute -top-32 -left-32 w-[450px] h-[450px] rounded-full border border-[#1e3fb9]/10" />
        <div className="absolute -bottom-40 -right-20 w-[400px] h-[400px] rounded-full border border-[#1e3fb9]/10" />

        <div>
          <span className="text-[24px] font-medium text-white tracking-[-0.5px]">
            Boa<span className="text-[#1e3fb9]">F</span>orma
          </span>
          <span className="ml-1 text-[11px] text-[#b3b3b3]">AI</span>
        </div>

        <div>
          <h1 className="text-[42px] font-medium text-white leading-[1.1] tracking-[-1.5px] mb-4">
            Comece sua<br />
            <span className="text-[#1e3fb9]">jornada.</span>
          </h1>
          <p className="text-[15px] text-[#b3b3b3] leading-relaxed mb-10 max-w-[280px]">
            Crie sua conta gratuitamente e tenha um personal trainer de IA disponível 24h.
          </p>
          <div className="flex flex-col gap-4">
            {FEATURES.map(({ icon: Icon, label }) => (
              <div key={label} className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-[#1e3fb9]/20 flex items-center justify-center shrink-0">
                  <Icon className="w-4 h-4 text-[#1e3fb9]" />
                </div>
                <span className="text-[14px] text-[#b3b3b3]">{label}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="text-[12px] text-[#555]">© 2026 BoaForma AI</p>
      </div>

      {/* ── Right panel ──────────────────────────────────── */}
      <div className="flex-1 flex items-center justify-center p-8 overflow-y-auto">
        <div className="w-full max-w-[420px] py-6">

          {/* Mobile logo */}
          <div className="lg:hidden mb-8">
            <span className="text-[24px] font-medium text-white tracking-[-0.5px]">
              Boa<span className="text-[#1e3fb9]">F</span>orma
            </span>
          </div>

          {/* Header */}
          <div className="flex items-center gap-2 mb-1">
            {step === 2 && (
              <button onClick={() => setStep(1)} className="w-7 h-7 flex items-center justify-center">
                <ChevronLeft className="w-4 h-4 text-[#b3b3b3]" />
              </button>
            )}
            <h2 className="text-[24px] font-medium text-white tracking-[-0.5px]">
              {step === 1 ? 'Criar conta' : 'Perfil de treino'}
            </h2>
          </div>
          <p className="text-[13px] text-[#b3b3b3] mb-6">
            {step === 1 ? 'Passo 1 de 2 — Seus dados de acesso' : 'Passo 2 de 2 — Configure seu perfil'}
          </p>

          {/* Step indicator */}
          <div className="flex gap-2 mb-7">
            <div className="h-1 flex-1 rounded-full bg-[#1e3fb9]" />
            <div className={`h-1 flex-1 rounded-full transition-colors ${step === 2 ? 'bg-[#1e3fb9]' : 'bg-[#333]'}`} />
          </div>

          <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="flex flex-col gap-4">

            {step === 1 && (
              <>
                <Field label="Nome completo" error={errors.name?.message}>
                  <div className="relative">
                    <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#555]" />
                    <input {...register('name')} placeholder="João Silva" className={`${inputCls} pl-10`} />
                  </div>
                </Field>
                <Field label="Email" error={errors.email?.message}>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#555]" />
                    <input {...register('email')} type="email" placeholder="seu@email.com" className={`${inputCls} pl-10`} />
                  </div>
                </Field>
                <Field label="Senha" error={errors.password?.message}>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#555]" />
                    <input {...register('password')} type="password" placeholder="Mínimo 8 caracteres" className={`${inputCls} pl-10`} />
                  </div>
                </Field>

                <button
                  type="button"
                  onClick={goNext}
                  className="w-full h-[46px] bg-[#1e3fb9] hover:bg-[#2548d4] rounded-[10px] flex items-center justify-center gap-2 text-[14px] font-medium text-white transition-colors mt-2"
                >
                  Continuar <ChevronRight className="w-4 h-4" />
                </button>
              </>
            )}

            {step === 2 && (
              <>
                <div className="grid grid-cols-3 gap-3">
                  <Field label="Idade" error={errors.age?.message}>
                    <input {...register('age')} type="number" placeholder="25" className={inputCls} />
                  </Field>
                  <Field label="Peso (kg)" error={errors.weight_kg?.message}>
                    <input {...register('weight_kg')} type="number" placeholder="75" className={inputCls} />
                  </Field>
                  <Field label="Altura (cm)" error={errors.height_cm?.message}>
                    <input {...register('height_cm')} type="number" placeholder="175" className={inputCls} />
                  </Field>
                </div>

                <Field label="Nível de experiência" error={errors.level?.message}>
                  <select {...register('level')} className={`${inputCls} appearance-none`}>
                    <option value="iniciante">Iniciante</option>
                    <option value="intermediario">Intermediário</option>
                    <option value="avancado">Avançado</option>
                  </select>
                </Field>

                <Field label="Objetivo" error={errors.goal?.message}>
                  <input {...register('goal')} placeholder="Ex: hipertrofia, emagrecimento, saúde" className={inputCls} />
                </Field>

                <Field label="Restrições físicas (opcional)">
                  <input {...register('restrictions')} placeholder="Ex: dor no joelho, lombar" className={inputCls} />
                </Field>

                <div className="rounded-[10px] border border-[#333] bg-[#252525] px-3 py-2.5">
                  <label className="flex items-start gap-2 text-[12px] text-[#c7c7c7]">
                    <input type="checkbox" {...register('accept_terms')} className="mt-0.5" />
                    <span>
                      Li e aceito a política de privacidade.
                      <a
                        href="/privacy-policy.html"
                        target="_blank"
                        rel="noreferrer"
                        className="ml-1 text-[#4d6fe0] hover:text-[#6b89ef]"
                      >
                        Ver política
                      </a>
                    </span>
                  </label>
                  {errors.accept_terms && <p className="mt-1 text-[11px] text-red-400">{errors.accept_terms.message}</p>}
                </div>

                {mutation.isError && (
                  <p className="text-[13px] text-red-400 text-center">Erro ao criar conta. Verifique os dados.</p>
                )}

                <button
                  type="submit"
                  disabled={mutation.isPending}
                  className="w-full h-[46px] bg-[#1e3fb9] hover:bg-[#2548d4] rounded-[10px] flex items-center justify-center gap-2 text-[14px] font-medium text-white disabled:opacity-60 transition-colors mt-2"
                >
                  {mutation.isPending ? 'Criando conta...' : (
                    <>Criar conta <ChevronRight className="w-4 h-4" /></>
                  )}
                </button>
              </>
            )}
          </form>

          <p className="text-center text-[13px] text-[#b3b3b3] mt-7">
            Já tem conta?{' '}
            <Link to="/login" className="text-[#1e3fb9] hover:text-[#4d6fe0] font-medium transition-colors">
              Entrar
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
