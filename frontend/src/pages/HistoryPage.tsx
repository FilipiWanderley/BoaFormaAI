import { useQuery } from '@tanstack/react-query'
import { CheckCircle, Calendar } from 'lucide-react'
import { historyService } from '../services/history.service'
import { Spinner } from '../components/ui/Spinner'
import { formatDate, formatDateTime } from '../lib/utils'

export function HistoryPage() {
  const { data: history = [], isLoading } = useQuery({
    queryKey: ['history'],
    queryFn: historyService.listMine,
  })

  const grouped = history.reduce<Record<string, typeof history>>((acc, item) => {
    const day = formatDate(item.completed_at)
    if (!acc[day]) acc[day] = []
    acc[day].push(item)
    return acc
  }, {})

  return (
    <div className="flex flex-col gap-7 pb-6">

      {/* Header */}
      <div className="flex items-end justify-between">
        <div>
          <p className="text-[13px] text-white/40 mb-1">Seu progresso</p>
          <h1 className="text-[28px] font-semibold text-white tracking-tight">Histórico</h1>
        </div>
        {history.length > 0 && (
          <p className="text-[13px] text-white/30">
            <span className="text-white/60">{history.length}</span> treino{history.length !== 1 ? 's' : ''}
          </p>
        )}
      </div>

      {isLoading && (
        <div className="flex h-48 items-center justify-center">
          <Spinner label="Carregando..." />
        </div>
      )}

      {!isLoading && history.length === 0 && (
        <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-14 flex flex-col items-center gap-4 text-center">
          <Calendar className="w-8 h-8 text-white/15" />
          <div>
            <p className="text-[15px] font-medium text-white/60">Nenhum treino concluído</p>
            <p className="text-[13px] text-white/30 mt-1">Complete um treino para ver seu histórico aqui.</p>
          </div>
        </div>
      )}

      {/* Stats row */}
      {history.length > 0 && (
        <div className="grid grid-cols-3 gap-4">
          {[
            { value: history.length,              label: 'Treinos concluídos' },
            { value: Object.keys(grouped).length, label: 'Dias ativos' },
            { value: `${history.length * 45}`,    label: 'Minutos totais' },
          ].map(({ value, label }) => (
            <div key={label} className="bg-surface-2 border border-white/[0.07] rounded-2xl p-5">
              <p className="text-[28px] font-semibold text-white tracking-tight leading-none">{value}</p>
              <p className="text-[12px] text-white/35 mt-2">{label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Grouped list */}
      {Object.entries(grouped).map(([day, items]) => (
        <div key={day}>
          <div className="flex items-center gap-4 mb-3">
            <p className="text-[11px] font-medium text-white/30 uppercase tracking-wider shrink-0">{day}</p>
            <div className="flex-1 h-px bg-white/[0.05]" />
          </div>
          <div className="flex flex-col gap-2">
            {items.map((item) => (
              <div key={item.id} className="bg-surface-2 border border-white/[0.07] hover:border-white/[0.11] rounded-2xl px-5 py-4 flex items-center gap-4 transition-colors">
                <CheckCircle className="w-4 h-4 text-white/25 shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-[14px] font-medium text-white capitalize">{item.workout_name}</p>
                  <p className="text-[12px] text-white/35 mt-0.5">{formatDateTime(item.completed_at)}</p>
                </div>
                {item.notes && (
                  <p className="text-[12px] text-white/30 italic max-w-[180px] truncate">{item.notes}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
