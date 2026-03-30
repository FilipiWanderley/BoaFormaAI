import type { ReactNode } from 'react'

interface PageHeaderProps {
  eyebrow?: string
  title: string
  right?: ReactNode
}

export function PageHeader({ eyebrow, title, right }: PageHeaderProps) {
  return (
    <div className="flex items-end justify-between">
      <div>
        {eyebrow && <p className="text-[13px] text-white/40 mb-1">{eyebrow}</p>}
        <h1 className="text-[28px] font-semibold text-white tracking-tight">{title}</h1>
      </div>
      {right}
    </div>
  )
}
