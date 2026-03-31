import { useMemo, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { PageHeader } from '../components/ui/PageHeader'
import { exercisesService } from '../services/exercises.service'
import { useAuthStore } from '../store/authStore'

export function AdminExercisesPage() {
  const user = useAuthStore((s) => s.user)
  const qc = useQueryClient()
  const [name, setName] = useState('')
  const [muscleGroup, setMuscleGroup] = useState('peito')
  const [equipment, setEquipment] = useState('barra')
  const [level, setLevel] = useState<'iniciante' | 'intermediario' | 'avancado'>('iniciante')

  const canAccess = !!user?.is_admin

  const query = useQuery({
    queryKey: ['admin-exercises'],
    queryFn: () => exercisesService.adminList(100, 0),
    enabled: canAccess,
  })

  const createMutation = useMutation({
    mutationFn: () => exercisesService.adminCreate({
      name,
      muscle_group: muscleGroup,
      equipment,
      level,
    }),
    onSuccess: () => {
      setName('')
      qc.invalidateQueries({ queryKey: ['admin-exercises'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (exerciseId: number) => exercisesService.adminDelete(exerciseId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin-exercises'] }),
  })

  const exercises = useMemo(() => query.data ?? [], [query.data])

  if (!canAccess) {
    return (
      <div className="flex flex-col gap-6">
        <PageHeader eyebrow="Admin" title="Curadoria de Exercícios" />
        <div className="rounded-2xl border border-red-400/20 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          Acesso restrito ao administrador.
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6 pb-6">
      <PageHeader eyebrow="Admin" title="Curadoria de Exercícios" />

      <div className="rounded-2xl border border-white/[0.08] bg-surface-2 p-4">
        <p className="mb-3 text-sm text-white/70">Cadastrar novo exercício</p>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
          <input
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Nome do exercício"
            className="rounded-xl border border-white/[0.1] bg-surface-3 px-3 py-2 text-sm text-white"
          />
          <input
            value={muscleGroup}
            onChange={(event) => setMuscleGroup(event.target.value)}
            placeholder="Grupo muscular"
            className="rounded-xl border border-white/[0.1] bg-surface-3 px-3 py-2 text-sm text-white"
          />
          <input
            value={equipment}
            onChange={(event) => setEquipment(event.target.value)}
            placeholder="Equipamento"
            className="rounded-xl border border-white/[0.1] bg-surface-3 px-3 py-2 text-sm text-white"
          />
          <select
            value={level}
            onChange={(event) => setLevel(event.target.value as 'iniciante' | 'intermediario' | 'avancado')}
            className="rounded-xl border border-white/[0.1] bg-surface-3 px-3 py-2 text-sm text-white"
          >
            <option value="iniciante">Iniciante</option>
            <option value="intermediario">Intermediário</option>
            <option value="avancado">Avançado</option>
          </select>
        </div>
        <button
          onClick={() => createMutation.mutate()}
          disabled={createMutation.isPending || name.trim().length < 2}
          className="mt-3 rounded-xl bg-accent px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {createMutation.isPending ? 'Salvando...' : 'Salvar exercício'}
        </button>
      </div>

      <div className="rounded-2xl border border-white/[0.08] bg-surface-2 p-4">
        <p className="mb-3 text-sm text-white/70">Biblioteca cadastrada ({exercises.length})</p>
        <div className="grid grid-cols-1 gap-2">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="flex items-center justify-between rounded-xl border border-white/[0.08] bg-surface-3 px-3 py-2">
              <div>
                <p className="text-sm font-medium text-white">{exercise.name}</p>
                <p className="text-xs text-white/50">{exercise.muscle_group} · {exercise.equipment} · {exercise.level}</p>
              </div>
              <button
                onClick={() => deleteMutation.mutate(exercise.id)}
                disabled={deleteMutation.isPending}
                className="rounded-lg border border-red-400/30 bg-red-500/10 px-2.5 py-1 text-xs text-red-300"
              >
                Excluir
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
