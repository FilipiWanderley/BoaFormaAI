import { api } from './api'
import type { ExerciseResponse } from '../types'

type AdminExercisePayload = {
  name: string
  muscle_group: string
  secondary_muscles?: string | null
  equipment: string
  level: 'iniciante' | 'intermediario' | 'avancado'
  instructions?: string | null
  image_url?: string | null
  contraindications?: string | null
}

export const exercisesService = {
  listCompatible: async (): Promise<ExerciseResponse[]> => {
    const { data } = await api.get<ExerciseResponse[]>('/exercises/compatible')
    return data
  },

  list: async (params?: {
    muscle_group?: string[]
    equipment?: string[]
    level?: string
  }): Promise<ExerciseResponse[]> => {
    const { data } = await api.get<ExerciseResponse[]>('/exercises', { params })
    return data
  },

  adminList: async (limit = 100, offset = 0): Promise<ExerciseResponse[]> => {
    const { data } = await api.get<ExerciseResponse[]>('/admin/exercises', { params: { limit, offset } })
    return data
  },

  adminCreate: async (payload: AdminExercisePayload): Promise<ExerciseResponse> => {
    const { data } = await api.post<ExerciseResponse>('/admin/exercises', payload)
    return data
  },

  adminUpdate: async (exerciseId: number, payload: Partial<AdminExercisePayload>): Promise<ExerciseResponse> => {
    const { data } = await api.patch<ExerciseResponse>(`/admin/exercises/${exerciseId}`, payload)
    return data
  },

  adminDelete: async (exerciseId: number): Promise<void> => {
    await api.delete(`/admin/exercises/${exerciseId}`)
  },
}
