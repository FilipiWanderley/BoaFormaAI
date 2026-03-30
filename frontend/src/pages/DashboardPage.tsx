import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, Flame, Zap, Dumbbell, Clock } from 'lucide-react'
import { dashboardService } from '../services/dashboard.service'
import { RingProgress } from '../components/ui/RingProgress'
import { Spinner } from '../components/ui/Spinner'
import { formatDate } from '../lib/utils'

// ── Helpers ──────────────────────────────────────────────

function getWeekDays() {
  const days   = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
  const today  = new Date()
  const dow    = today.getDay()
  const monday = new Date(today)
  monday.setDate(today.getDate() - ((dow + 6) % 7))

  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday)
    d.setDate(monday.getDate() + i)
    return {
      label:   days[d.getDay()],
      date:    d.getDate(),
      isToday: d.toDateString() === today.toDateString(),
    }
  })
}

// ── Main ─────────────────────────────────────────────────

export function DashboardPage() {
  const navigate = useNavigate()

  const { data, isLoading, isError } = useQuery({
    queryKey: ['dashboard'],
    queryFn:  dashboardService.get,
  })

  if (isLoading) return (
    <div className="flex h-64 items-center justify-center">
      <Spinner label="Carregando..." />
    </div>
  )
  if (isError || !data) return <p className="text-white/40">Erro ao carregar dashboard.</p>

  const { user, stats, last_workout, today_workout } = data
  const workoutOfDay = today_workout ?? last_workout
  const days    = getWeekDays()
  const kcal    = stats.total_workouts_completed * 280
  const km      = (stats.total_workouts_completed * 1.8).toFixed(1)
  const minutes = stats.total_workouts_completed * 45
  const pct     = Math.min(Math.round((stats.total_workouts_completed / 10) * 100), 100)

  return (
    <div className="flex flex-col gap-8">

      {/* ── Greeting ───────────────────────────────────── */}
      <div className="flex items-end justify-between">
        <div>
          <p className="text-[13px] text-white/40 mb-1">
            {new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' })}
          </p>
          <h1 className="text-[28px] font-semibold text-white tracking-tight">
            Olá, {user.name.split(' ')[0]}
          </h1>
        </div>
        {stats.current_streak_days > 0 && (
          <div className="flex items-center gap-1.5 text-[13px] text-white/50 bg-white/[0.05] border border-white/[0.08] rounded-full px-3 py-1.5">
            <Flame className="w-3.5 h-3.5 text-orange-400" />
            {stats.current_streak_days} dia{stats.current_streak_days !== 1 ? 's' : ''} de sequência
          </div>
        )}
      </div>

      {/* ── Calendar strip ─────────────────────────────── */}
      <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5">
        <div className="flex items-center justify-between mb-5">
          <p className="text-[13px] font-medium text-white/50 uppercase tracking-wider">
            {new Date().toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' }).replace(/^\w/, c => c.toUpperCase())}
          </p>
        </div>
        <div className="flex justify-between">
          {days.map(({ label, date, isToday }) => (
            <div key={date} className="flex flex-col items-center gap-2">
              <span className="text-[11px] text-white/30 font-medium">{label}</span>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-[13px] font-medium transition-colors ${
                isToday
                  ? 'bg-accent text-white'
                  : 'text-white/50 hover:text-white hover:bg-white/[0.06]'
              }`}>
                {date}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Main grid ──────────────────────────────────── */}
      <div className="grid grid-cols-3 gap-5">

        {/* Activity ring — spans 1 col */}
        <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-6 flex flex-col justify-between">
          <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider mb-5">Atividade</p>
          <div className="flex flex-col items-center gap-4">
            <RingProgress value={pct} size={100} strokeWidth={7} color="#2563eb" bg="rgba(255,255,255,0.05)">
              <span className="text-[20px] font-semibold text-white">{stats.total_workouts_completed}</span>
            </RingProgress>
            <p className="text-[12px] text-white/40 text-center">treinos concluídos</p>
          </div>
        </div>

        {/* Stats — spans 2 cols */}
        <div className="col-span-2 grid grid-cols-2 gap-4">
          {[
            { icon: Dumbbell, value: stats.total_workouts_generated, label: 'Total Gerados',  sub: 'treinos' },
            { icon: Clock,    value: minutes > 0 ? minutes : '—',    label: 'Tempo Total',    sub: 'minutos' },
            { icon: Flame,    value: kcal > 0 ? kcal : '—',          label: 'Calorias',       sub: 'kcal estimado' },
            { icon: Zap,      value: `${stats.total_workouts_completed * 120}`, label: 'Pontos',  sub: 'acumulados' },
          ].map(({ icon: Icon, value, label, sub }) => (
            <div key={label} className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5">
              <Icon className="w-4 h-4 text-white/25 mb-3" />
              <p className="text-[26px] font-semibold text-white tracking-tight leading-none">{value}</p>
              <p className="text-[12px] text-white/40 mt-1.5">{label}</p>
              <p className="text-[11px] text-white/25 mt-0.5">{sub}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ── Distance + best workout row ───────────────── */}
      <div className="grid grid-cols-[1fr_1.8fr] gap-5">

        {/* Distance */}
        <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-6 flex flex-col justify-between">
          <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider">Distância</p>
          <div>
            <p className="text-[38px] font-semibold text-white tracking-tight leading-none mt-6">{km}</p>
            <p className="text-[13px] text-white/40 mt-1">km estimado</p>
          </div>
          <p className="text-[11px] text-white/25 mt-4">{formatDate(new Date().toISOString())}</p>
        </div>

        {/* Last workout */}
        <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider">Treino do Dia</p>
            <button
              onClick={() => navigate('/workout')}
              className="flex items-center gap-1 text-[12px] text-white/40 hover:text-white transition-colors"
            >
              Ver todos <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {workoutOfDay ? (
            <button
              onClick={() => navigate('/workout')}
              className="flex items-start gap-4 text-left group mt-4"
            >
              <div className="w-14 h-14 rounded-xl bg-surface-3 border border-white/[0.06] flex items-center justify-center shrink-0">
                <Dumbbell className="w-6 h-6 text-white/20" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[15px] font-medium text-white capitalize group-hover:text-white/80 transition-colors truncate">
                  {workoutOfDay.workout_name}
                </p>
                <p className="text-[12px] text-white/40 mt-1">
                  {workoutOfDay.estimated_duration_minutes} min
                </p>
                <p className="text-[12px] text-white/30 mt-0.5 line-clamp-1">
                  {workoutOfDay.focus}
                </p>
              </div>
              <ArrowRight className="w-4 h-4 text-white/20 group-hover:text-white/50 transition-colors mt-0.5 shrink-0" />
            </button>
          ) : (
            <button
              onClick={() => navigate('/workout')}
              className="flex flex-col items-start gap-2 mt-4 group"
            >
              <p className="text-[15px] font-medium text-white/50 group-hover:text-white transition-colors">
                Gerar primeiro treino
              </p>
              <p className="text-[12px] text-white/30">
                A IA monta um treino personalizado para você
              </p>
              <div className="flex items-center gap-1.5 text-[12px] text-accent mt-1 group-hover:gap-2.5 transition-all">
                Começar <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
