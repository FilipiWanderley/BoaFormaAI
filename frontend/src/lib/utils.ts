export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ')
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

export function levelLabel(level: string): string {
  const map: Record<string, string> = {
    iniciante: 'Iniciante',
    intermediario: 'Intermediário',
    avancado: 'Avançado',
  }
  return map[level] ?? level
}

export function feedbackLabel(fb: string | null): string {
  const map: Record<string, string> = {
    facil: 'Fácil',
    ok: 'Ok',
    dificil: 'Difícil',
  }
  return fb ? (map[fb] ?? fb) : '—'
}
