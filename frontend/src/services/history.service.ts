import { api } from './api'
import type { HistoryCreate, HistoryResponse } from '../types'

export const historyService = {
  complete: async (payload: HistoryCreate): Promise<HistoryResponse> => {
    const { data } = await api.post<HistoryResponse>('/history', payload)
    return data
  },

  listMine: async (): Promise<HistoryResponse[]> => {
    const { data } = await api.get<HistoryResponse[]>('/history/me')
    return data
  },
}
