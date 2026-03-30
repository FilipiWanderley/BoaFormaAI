import { api } from './api'
import type { DashboardResponse } from '../types'

export const dashboardService = {
  get: async (): Promise<DashboardResponse> => {
    const { data } = await api.get<DashboardResponse>('/dashboard')
    return data
  },
}
