import type { ReactNode } from 'react'

interface EmptyStateProps {
  icon: ReactNode
  title: string
  description: string
}

export function EmptyState({ icon, title, description }: EmptyStateProps) {
  return (
    <div className="bg-surface-2 border border-white/[0.07] rounded-2xl p-14 flex flex-col items-center gap-4 text-center">
      <div>{icon}</div>
      <div>
        <p className="text-[15px] font-medium text-white/60">{title}</p>
        <p className="text-[13px] text-white/30 mt-1">{description}</p>
      </div>
    </div>
  )
}
