import { api } from './api'
import type { ChatMessageResponse, ChatResponse } from '../types'

export const chatService = {
  send: async (message: string): Promise<ChatResponse> => {
    const { data } = await api.post<ChatResponse>('/chat', { message })
    return data
  },

  getHistory: async (): Promise<ChatMessageResponse[]> => {
    const { data } = await api.get<ChatMessageResponse[]>('/chat/history')
    return data
  },

  clearHistory: async (): Promise<void> => {
    await api.delete('/chat/history')
  },
}
