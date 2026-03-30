import { api } from './api'
import type { ExerciseResponse } from '../types'

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
}
