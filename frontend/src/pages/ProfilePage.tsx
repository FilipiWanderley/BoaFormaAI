import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { CheckCircle } from 'lucide-react'
import { authService } from '../services/auth.service'
import { PageHeader } from '../components/ui/PageHeader'
import { useAuthStore } from '../store/authStore'
import { Spinner } from '../components/ui/Spinner'
import { levelLabel } from '../lib/utils'

const schema = z.object({
  weight_kg:    z.coerce.number().min(20).max(300),
  height_cm:    z.coerce.number().min(100).max(250),
  goal:         z.string().min(3, 'Mínimo 3 caracteres'),
  restrictions: z.string().optional(),
})
type FormData = z.infer<typeof schema>

const inputCls = "w-full bg-surface-3 border border-white/[0.08] rounded-xl px-4 py-2.5 text-[14px] text-white placeholder-white/25 focus:outline-none focus:border-white/[0.18] transition-colors"

const LEVEL_BADGE: Record<string, string> = {
  iniciante:     'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  intermediario: 'text-amber-400  bg-amber-400/10  border-amber-400/20',
  avancado:      'text-blue-400   bg-blue-400/10   border-blue-400/20',
}

export function ProfilePage() {
  const { user, setUser } = useAuthStore()
  const qc = useQueryClient()

  const { register, handleSubmit, formState: { errors, isDirty } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      weight_kg:    user?.weight_kg,
      height_cm:    user?.height_cm,
      goal:         user?.goal,
      restrictions: user?.restrictions ?? '',
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FormData) => authService.updateMe(data),
    onSuccess: (updated) => {
      setUser(updated)
      qc.invalidateQueries({ queryKey: ['dashboard'] })
    },
  })

  if (!user) return null

  const firstName  = user.name.split(' ')[0]
  const badgeCls   = LEVEL_BADGE[user.level] ?? LEVEL_BADGE.avancado

  return (
    <div className="flex flex-col gap-7 pb-6">

      <PageHeader eyebrow="Configurações" title="Perfil" />

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_1.8fr] gap-6 items-start">

        {/* Identity */}
        <div className="flex flex-col gap-4">
          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-6 flex flex-col items-center text-center gap-4">
            <div className="w-16 h-16 rounded-full bg-surface-3 border border-white/[0.08] flex items-center justify-center text-[24px] font-semibold text-white/60">
              {firstName.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="text-[15px] font-semibold text-white">{user.name}</p>
              <p className="text-[12px] text-white/35 mt-0.5">{user.email}</p>
            </div>
            <span className={`text-[11px] font-medium px-2.5 py-1 rounded-full border ${badgeCls}`}>
              {levelLabel(user.level)}
            </span>
          </div>

          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5">
            <p className="text-[11px] font-medium text-white/30 uppercase tracking-wider mb-4">Dados atuais</p>
            <div className="flex flex-col gap-3">
              {[
                { label: 'Idade',   value: `${user.age} anos` },
                { label: 'Peso',    value: `${user.weight_kg} kg` },
                { label: 'Altura',  value: `${user.height_cm} cm` },
              ].map(({ label, value }) => (
                <div key={label} className="flex items-center justify-between">
                  <span className="text-[12px] text-white/35">{label}</span>
                  <span className="text-[13px] font-medium text-white/70">{value}</span>
                </div>
              ))}
              {user.goal && (
                <div className="pt-2 border-t border-white/[0.05]">
                  <p className="text-[11px] text-white/30 mb-1">Objetivo</p>
                  <p className="text-[13px] text-white/60">{user.goal}</p>
                </div>
              )}
              {user.restrictions && (
                <div className="pt-2 border-t border-white/[0.05]">
                  <p className="text-[11px] text-white/30 mb-1">Restrições</p>
                  <p className="text-[13px] text-white/50">{user.restrictions}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Form */}
        <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5 md:p-7">
          <p className="text-[11px] font-medium text-white/30 uppercase tracking-wider mb-6">Atualizar dados</p>

          <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="flex flex-col gap-5">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-[12px] text-white/40">Peso (kg)</label>
                <input {...register('weight_kg')} type="number" step="0.1" className={inputCls} />
                {errors.weight_kg && <p className="text-[11px] text-red-400/70">{errors.weight_kg.message}</p>}
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-[12px] text-white/40">Altura (cm)</label>
                <input {...register('height_cm')} type="number" className={inputCls} />
                {errors.height_cm && <p className="text-[11px] text-red-400/70">{errors.height_cm.message}</p>}
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] text-white/40">Objetivo</label>
              <input {...register('goal')} placeholder="Ex: hipertrofia, emagrecimento" className={inputCls} />
              {errors.goal && <p className="text-[11px] text-red-400/70">{errors.goal.message}</p>}
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] text-white/40">Restrições físicas <span className="text-white/20">(opcional)</span></label>
              <input {...register('restrictions')} placeholder="Ex: dor no joelho, lombar" className={inputCls} />
            </div>

            <div className="h-px bg-white/[0.05]" />

            {mutation.isSuccess && (
              <div className="flex items-center gap-2 text-[13px] text-emerald-400/80 bg-emerald-400/[0.07] border border-emerald-400/20 rounded-xl px-4 py-3">
                <CheckCircle className="w-4 h-4 shrink-0" />
                Perfil atualizado.
              </div>
            )}
            {mutation.isError && (
              <p className="text-[13px] text-red-400/70 bg-red-400/[0.07] border border-red-400/20 rounded-xl px-4 py-3">
                Erro ao salvar. Tente novamente.
              </p>
            )}

            <button
              type="submit"
              disabled={mutation.isPending || !isDirty}
              className="w-full h-[44px] bg-accent hover:bg-accent-hover rounded-xl flex items-center justify-center text-[14px] font-medium text-white disabled:opacity-40 transition-colors"
            >
              {mutation.isPending ? <Spinner /> : 'Salvar alterações'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
