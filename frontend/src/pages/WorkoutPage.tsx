import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  Clock, Play, Flame, MapPin, Zap,
  CheckCircle, Dumbbell, ArrowLeft, ArrowRight, ChevronDown,
} from 'lucide-react'
import { workoutService } from '../services/workout.service'
import { historyService } from '../services/history.service'
import { RingProgress } from '../components/ui/RingProgress'
import { Spinner } from '../components/ui/Spinner'
import { formatDate } from '../lib/utils'
import type { FeedbackValue, WorkoutGenerateRequest, WorkoutResponse, WorkoutSummary } from '../types'

const MUSCLE_GROUPS = ['peito','costas','quadriceps','posterior','gluteos','ombros','biceps','triceps','abdomen','panturrilha']
const EQUIPMENT     = ['barra','haltere','maquina','cabo','peso_corporal','kettlebell','elastico']
const DURATIONS     = [30, 45, 60, 75, 90]

function toggle<T>(arr: T[], item: T): T[] {
  return arr.includes(item) ? arr.filter(x => x !== item) : [...arr, item]
}

const chipCls = (active: boolean) =>
  `rounded-lg border px-3 py-1.5 text-[12px] font-medium transition-colors cursor-pointer ${
    active
      ? 'border-accent/50 bg-accent-muted text-accent'
      : 'border-white/[0.08] text-white/40 hover:border-white/[0.15] hover:text-white/70'
  }`

// ── Workout detail ─────────────────────────────────────────

function WorkoutDetail({ workout, onBack }: { workout: WorkoutResponse; onBack: () => void }) {
  const qc = useQueryClient()
  const [feedback, setFeedback] = useState<FeedbackValue | null>(workout.feedback ?? null)

  const totalKcal = workout.exercises.length * 55
  const totalKm   = (workout.exercises.length * 0.3).toFixed(1)
  const totalPts  = workout.exercises.length * 25

  const completeMutation = useMutation({
    mutationFn: () => historyService.complete({ workout_id: workout.id }),
    onSuccess:  () => qc.invalidateQueries({ queryKey: ['dashboard'] }),
  })

  const feedbackMutation = useMutation({
    mutationFn: (fb: FeedbackValue) => workoutService.submitFeedback(workout.id, fb),
    onSuccess:  (data) => setFeedback(data.feedback),
  })

  return (
    <div className="flex flex-col gap-7 pb-6">

      {/* Header */}
      <div className="flex items-start gap-4">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-xl bg-surface-3 border border-white/[0.08] hover:border-white/[0.14] flex items-center justify-center transition-colors shrink-0 mt-0.5"
        >
          <ArrowLeft className="w-4 h-4 text-white/60" />
        </button>
        <div className="flex-1">
          <h1 className="text-[22px] font-semibold text-white capitalize tracking-tight">{workout.workout_name}</h1>
          <p className="text-[13px] text-white/40 mt-0.5">{formatDate(new Date().toISOString())}</p>
        </div>
        <div className="flex items-center gap-1.5 bg-surface-3 border border-white/[0.08] rounded-xl px-3 py-2 shrink-0">
          <Clock className="w-3.5 h-3.5 text-white/40" />
          <span className="text-[13px] text-white/60 font-medium">{workout.estimated_duration_minutes} min</span>
        </div>
      </div>

      {/* Two column */}
      <div className="grid grid-cols-[1fr_1.5fr] gap-6 items-start">

        {/* Left */}
        <div className="flex flex-col gap-4">

          {/* Hero */}
          <div className="relative rounded-2xl overflow-hidden bg-surface-2 border border-white/[0.07]" style={{ aspectRatio: '1/1' }}>
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3"
              style={{ background: 'radial-gradient(circle at center, rgba(37,99,235,0.08) 0%, transparent 70%)' }}
            >
              <div className="w-14 h-14 rounded-full bg-accent/10 border border-accent/20 flex items-center justify-center">
                <Play className="w-6 h-6 text-accent ml-0.5" />
              </div>
              <span className="text-[12px] text-white/25">em breve</span>
            </div>
          </div>

          {/* Metrics */}
          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl overflow-hidden">
            {[
              { icon: Flame,  label: 'Calorias',    value: `${totalKcal}`, unit: 'kcal', pct: 70,  color: '#f97316' },
              { icon: MapPin, label: 'Distância',   value: totalKm,         unit: 'km',   pct: 40,  color: '#60a5fa' },
              { icon: Zap,    label: 'Pontos',      value: `${totalPts}+`,  unit: '',     pct: 80,  color: '#a78bfa' },
            ].map(({ icon: Icon, label, value, unit, pct, color }, i) => (
              <div key={label} className={`flex items-center gap-4 px-5 py-4 ${i < 2 ? 'border-b border-white/[0.05]' : ''}`}>
                <Icon className="w-4 h-4 text-white/25 shrink-0" />
                <div className="flex-1">
                  <span className="text-[15px] font-semibold text-white">{value}</span>
                  {unit && <span className="text-[12px] text-white/40 ml-1">{unit}</span>}
                  <p className="text-[11px] text-white/30 mt-0.5">{label}</p>
                </div>
                <RingProgress value={pct} size={34} strokeWidth={3} color={color} bg="rgba(255,255,255,0.07)">
                  <span className="text-[7px] text-white/60">{pct}%</span>
                </RingProgress>
              </div>
            ))}
          </div>

          {/* Feedback */}
          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5">
            <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider mb-4">Como foi?</p>
            <div className="flex gap-2">
              {([
                ['facil',   'Fácil',   '#22c55e'],
                ['ok',      'Ok',      '#facc15'],
                ['dificil', 'Difícil', '#f87171'],
              ] as const).map(([val, label, col]) => (
                <button key={val}
                  onClick={() => feedbackMutation.mutate(val as FeedbackValue)}
                  className="flex-1 py-2 rounded-lg border text-[12px] font-medium transition-all"
                  style={feedback === val
                    ? { borderColor: col, backgroundColor: `${col}14`, color: col }
                    : { borderColor: 'rgba(255,255,255,0.08)', color: 'rgba(255,255,255,0.4)' }
                  }
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* CTA */}
          <button
            onClick={() => completeMutation.mutate()}
            disabled={completeMutation.isSuccess || completeMutation.isPending}
            className="w-full h-[44px] bg-accent hover:bg-accent-hover rounded-xl flex items-center justify-center gap-2 text-[14px] font-medium text-white disabled:opacity-50 transition-colors"
          >
            {completeMutation.isSuccess ? (
              <><CheckCircle className="w-4 h-4" /> Concluído!</>
            ) : completeMutation.isPending ? 'Salvando...' : 'Marcar como concluído'}
          </button>
        </div>

        {/* Right — exercises */}
        <div className="flex flex-col gap-3">
          <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider">
            Exercícios <span className="text-white/25 normal-case">({workout.exercises.length})</span>
          </p>

          {workout.exercises.map((ex, i) => (
            <div key={ex.exercise_id} className="bg-surface-2 border border-white/[0.07] hover:border-white/[0.11] rounded-2xl p-4 transition-colors">
              <div className="flex items-start gap-3">
                <span className="text-[11px] font-semibold text-white/25 w-5 shrink-0 mt-0.5">{i + 1}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-[14px] font-medium text-white capitalize">{ex.exercise_name}</p>
                  <p className="text-[11px] text-white/35 mt-0.5 capitalize">{ex.muscle_group} · {ex.equipment}</p>
                  <div className="flex gap-5 mt-3">
                    <div>
                      <p className="text-[15px] font-semibold text-white leading-none">{ex.sets}</p>
                      <p className="text-[10px] text-white/30 mt-0.5">séries</p>
                    </div>
                    <div>
                      <p className="text-[15px] font-semibold text-white leading-none">{ex.reps}</p>
                      <p className="text-[10px] text-white/30 mt-0.5">reps</p>
                    </div>
                    <div>
                      <p className="text-[15px] font-semibold text-white leading-none">{ex.rest_seconds}s</p>
                      <p className="text-[10px] text-white/30 mt-0.5">descanso</p>
                    </div>
                  </div>
                  {ex.notes && <p className="text-[11px] text-white/25 italic mt-2">{ex.notes}</p>}
                </div>
              </div>
            </div>
          ))}

          {/* Tips */}
          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5 mt-1">
            <p className="text-[11px] font-medium text-white/30 uppercase tracking-wider mb-2">Dicas gerais</p>
            <p className="text-[13px] text-white/60 leading-relaxed">{workout.general_tips}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Generate form ─────────────────────────────────────────

export function WorkoutPage() {
  const [activeId, setActiveId] = useState<number | null>(null)
  const [muscleGroups, setMuscleGroups] = useState<string[]>([])
  const [equipment, setEquipment] = useState<string[]>([])
  const [duration, setDuration] = useState(60)
  const [lastFeedback, setLastFeedback] = useState<FeedbackValue | null>(null)

  const { data: workouts = [] } = useQuery<WorkoutSummary[]>({
    queryKey: ['workouts'],
    queryFn:  workoutService.listMine,
  })

  const { data: activeWorkout, isLoading: loadingActive } = useQuery<WorkoutResponse>({
    queryKey: ['workout', activeId],
    queryFn:  () => workoutService.getOne(activeId!),
    enabled:  activeId !== null,
  })

  const qc = useQueryClient()
  const generateMutation = useMutation({
    mutationFn: (req: WorkoutGenerateRequest) => workoutService.generate(req),
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['workouts'] })
      qc.invalidateQueries({ queryKey: ['dashboard'] })
      setActiveId(data.id)
    },
  })

  if (activeId !== null) {
    if (loadingActive) return <div className="flex h-64 items-center justify-center"><Spinner label="Carregando treino..." /></div>
    if (activeWorkout) return <WorkoutDetail workout={activeWorkout} onBack={() => setActiveId(null)} />
  }

  return (
    <div className="flex flex-col gap-7 pb-6">

      <div>
        <p className="text-[13px] text-white/40 mb-1">Personalizado pela IA</p>
        <h1 className="text-[28px] font-semibold text-white tracking-tight">Novo Treino</h1>
      </div>

      <div className="grid grid-cols-[1.3fr_1fr] gap-6 items-start">

        {/* Config */}
        <div className="flex flex-col gap-5">
          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-6 flex flex-col gap-6">

            <div>
              <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider mb-3">Grupos musculares</p>
              <div className="flex flex-wrap gap-2">
                {MUSCLE_GROUPS.map(m => (
                  <button key={m} type="button" onClick={() => setMuscleGroups(toggle(muscleGroups, m))}
                    className={chipCls(muscleGroups.includes(m))}>
                    {m.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            <div className="h-px bg-white/[0.05]" />

            <div>
              <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider mb-3">Equipamentos</p>
              <div className="flex flex-wrap gap-2">
                {EQUIPMENT.map(e => (
                  <button key={e} type="button" onClick={() => setEquipment(toggle(equipment, e))}
                    className={chipCls(equipment.includes(e))}>
                    {e.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            <div className="h-px bg-white/[0.05]" />

            <div>
              <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider mb-3">Duração</p>
              <div className="flex gap-2">
                {DURATIONS.map(d => (
                  <button key={d} type="button" onClick={() => setDuration(d)}
                    className={`flex-1 py-2 rounded-lg border text-[12px] font-medium transition-colors ${
                      duration === d
                        ? 'border-accent/50 bg-accent-muted text-accent'
                        : 'border-white/[0.08] text-white/40 hover:border-white/[0.15] hover:text-white/60'
                    }`}>
                    {d}min
                  </button>
                ))}
              </div>
            </div>

            <div className="h-px bg-white/[0.05]" />

            <div>
              <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider mb-3">
                Último treino foi…
                <span className="normal-case font-normal ml-1 text-white/25">(opcional)</span>
              </p>
              <div className="flex gap-2">
                {([
                  ['facil',   'Fácil',   '#22c55e'],
                  ['ok',      'Ok',      '#facc15'],
                  ['dificil', 'Difícil', '#f87171'],
                ] as const).map(([val, label, col]) => (
                  <button key={val} type="button"
                    onClick={() => setLastFeedback(lastFeedback === val ? null : val as FeedbackValue)}
                    className="flex-1 py-2 rounded-lg border text-[12px] font-medium transition-all"
                    style={lastFeedback === val
                      ? { borderColor: col, backgroundColor: `${col}14`, color: col }
                      : { borderColor: 'rgba(255,255,255,0.08)', color: 'rgba(255,255,255,0.4)' }
                    }>
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {generateMutation.isError && (
            <p className="text-[13px] text-red-400/70 bg-red-400/[0.08] border border-red-400/20 rounded-xl px-4 py-3">
              Erro ao gerar treino. Tente novamente.
            </p>
          )}

          <button
            disabled={generateMutation.isPending}
            onClick={() => generateMutation.mutate({
              muscle_groups:       muscleGroups.length ? muscleGroups : undefined,
              equipment_available: equipment.length    ? equipment    : undefined,
              duration_minutes:    duration,
              feedback_on_last:    lastFeedback ?? undefined,
            })}
            className="w-full h-[44px] bg-accent hover:bg-accent-hover rounded-xl flex items-center justify-center gap-2 text-[14px] font-medium text-white disabled:opacity-50 transition-colors"
          >
            {generateMutation.isPending ? 'Gerando...' : (
              <>Gerar Treino com IA <ArrowRight className="w-4 h-4" /></>
            )}
          </button>
        </div>

        {/* Past workouts */}
        <div className="flex flex-col gap-3">
          <p className="text-[12px] font-medium text-white/40 uppercase tracking-wider">
            Anteriores
          </p>

          {workouts.length === 0 ? (
            <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-8 flex flex-col items-center gap-3 text-center">
              <Dumbbell className="w-7 h-7 text-white/15" />
              <p className="text-[13px] text-white/30">Nenhum treino gerado ainda.</p>
            </div>
          ) : (
            workouts.map((w) => (
              <button key={w.id} onClick={() => setActiveId(w.id)}
                className="bg-surface-2 border border-white/[0.07] hover:border-white/[0.12] rounded-2xl p-4 flex items-center justify-between text-left transition-colors group"
              >
                <div>
                  <p className="text-[14px] font-medium text-white capitalize">{w.workout_name}</p>
                  <p className="text-[11px] text-white/35 mt-0.5">{formatDate(w.created_at)}</p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className="text-[11px] text-white/35 bg-white/[0.05] border border-white/[0.07] rounded-full px-2 py-0.5">
                    {w.estimated_duration_minutes}min
                  </span>
                  <ChevronDown className="w-3.5 h-3.5 text-white/20 -rotate-90 group-hover:text-white/50 transition-colors" />
                </div>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
