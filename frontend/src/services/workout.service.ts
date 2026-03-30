import { api } from './api'
import type {
  FeedbackValue,
  WorkoutGenerateRequest,
  WorkoutResponse,
  WorkoutSummary,
} from '../types'

export const workoutService = {
  generate: async (payload: WorkoutGenerateRequest): Promise<WorkoutResponse> => {
    const { data } = await api.post<WorkoutResponse>('/workout/generate', payload)
    return data
  },

  listMine: async (): Promise<WorkoutSummary[]> => {
    const { data } = await api.get<WorkoutSummary[]>('/workout/me')
    return data
  },

  getOne: async (id: number): Promise<WorkoutResponse> => {
    const { data } = await api.get<WorkoutResponse>(`/workout/${id}`)
    return data
  },

  submitFeedback: async (id: number, feedback: FeedbackValue): Promise<WorkoutSummary> => {
    const { data } = await api.patch<WorkoutSummary>(`/workout/${id}/feedback`, { feedback })
    return data
  },
}
