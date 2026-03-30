import { useEffect, useRef, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Send, Trash2, Bot, ArrowUpRight } from 'lucide-react'
import { chatService } from '../services/chat.service'
import { EmptyState } from '../components/ui/EmptyState'
import { PageHeader } from '../components/ui/PageHeader'
import { Spinner } from '../components/ui/Spinner'
import { formatDateTime } from '../lib/utils'
import { useAuthStore } from '../store/authStore'
import type { ChatMessageResponse } from '../types'

function MessageBubble({ msg }: { msg: ChatMessageResponse }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-surface-3 border border-white/[0.08] flex items-center justify-center shrink-0 mt-0.5">
          <Bot className="w-3.5 h-3.5 text-white/40" />
        </div>
      )}
      <div className={`max-w-[72%] flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-2xl px-4 py-2.5 text-[13px] leading-relaxed ${
          isUser
            ? 'bg-accent text-white rounded-tr-sm'
            : 'bg-surface-3 border border-white/[0.07] text-white/80 rounded-tl-sm'
        }`}>
          <p className="whitespace-pre-wrap">{msg.content}</p>
        </div>
        <span className="text-[10px] text-white/20">{formatDateTime(msg.created_at)}</span>
      </div>
    </div>
  )
}

const QUICK_PROMPTS = [
  'Como melhorar meu peito?',
  'Quantas proteínas por dia?',
  'Treino para perder gordura?',
  'Dicas de recuperação muscular',
]

export function ChatPage() {
  const qc        = useQueryClient()
  const user      = useAuthStore((s) => s.user)
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  const { data: messages = [], isLoading } = useQuery({
    queryKey: ['chat-history'],
    queryFn:  chatService.getHistory,
  })

  const sendMutation = useMutation({
    mutationFn: (msg: string) => chatService.send(msg),
    onSuccess: (data) => qc.setQueryData<ChatMessageResponse[]>(['chat-history'], data.history),
  })

  const clearMutation = useMutation({
    mutationFn: chatService.clearHistory,
    onSuccess:  () => qc.setQueryData(['chat-history'], []),
  })

  const handleSend = (msg?: string) => {
    const text = (msg ?? input).trim()
    if (!text || sendMutation.isPending) return
    setInput('')
    sendMutation.mutate(text)
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, sendMutation.isPending])

  const firstName = user?.name.split(' ')[0] ?? ''

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)]">

      <div className="mb-6 shrink-0">
        <PageHeader
          eyebrow="Seu coach virtual"
          title="Chat IA"
          right={messages.length > 0 ? (
            <button
              onClick={() => clearMutation.mutate()}
              disabled={clearMutation.isPending}
              className="flex items-center gap-1.5 text-[12px] text-white/30 hover:text-white/60 transition-colors disabled:opacity-40"
            >
              <Trash2 className="w-3.5 h-3.5" />
              Limpar
            </button>
          ) : null}
        />
      </div>

      {/* Layout */}
      <div className="flex gap-5 flex-1 min-h-0">

        {/* Chat */}
        <div className="flex-1 flex flex-col bg-surface-2 border border-white/[0.07] rounded-2xl overflow-hidden">
          <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">

            {isLoading && <div className="flex h-32 items-center justify-center"><Spinner /></div>}

            {!isLoading && messages.length === 0 && (
              <EmptyState
                icon={<Bot className="w-8 h-8 text-white/15" />}
                title={`Olá${firstName ? `, ${firstName}` : ''}`}
                description="Pergunte sobre treinos, nutrição ou qualquer dúvida de fitness."
              />
            )}

            {messages.map((msg) => <MessageBubble key={msg.id} msg={msg} />)}

            {sendMutation.isPending && (
              <div className="flex gap-3">
                <div className="w-7 h-7 rounded-full bg-surface-3 border border-white/[0.08] flex items-center justify-center shrink-0">
                  <Bot className="w-3.5 h-3.5 text-white/40" />
                </div>
                <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm bg-surface-3 border border-white/[0.07] px-4 py-3">
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-white/30 [animation-delay:0ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-white/30 [animation-delay:150ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-white/30 [animation-delay:300ms]" />
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-white/[0.05] p-4">
            <div className="flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                placeholder="Pergunte sobre treino, nutrição..."
                className="flex-1 bg-surface-3 border border-white/[0.08] focus:border-white/[0.15] rounded-xl px-4 py-2.5 text-[13px] text-white placeholder-white/25 focus:outline-none transition-colors"
              />
              <button
                onClick={() => handleSend()}
                disabled={!input.trim() || sendMutation.isPending}
                className="w-10 h-10 bg-accent hover:bg-accent-hover rounded-xl flex items-center justify-center disabled:opacity-30 transition-colors shrink-0"
              >
                <Send className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-52 shrink-0 flex flex-col gap-4">
          <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-4">
            <p className="text-[11px] font-medium text-white/30 uppercase tracking-wider mb-3">Sugestões</p>
            <div className="flex flex-col gap-1.5">
              {QUICK_PROMPTS.map((prompt) => (
                <button
                  key={prompt}
                  onClick={() => handleSend(prompt)}
                  disabled={sendMutation.isPending}
                  className="flex items-center justify-between gap-2 text-left text-[12px] text-white/45 hover:text-white/80 py-2 px-3 rounded-lg hover:bg-white/[0.04] transition-colors disabled:opacity-40 group"
                >
                  <span>{prompt}</span>
                  <ArrowUpRight className="w-3 h-3 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
