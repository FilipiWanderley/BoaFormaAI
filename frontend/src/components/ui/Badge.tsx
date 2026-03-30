import type { HTMLAttributes } from 'react'
import { cn } from '../../lib/utils'

const colors = {
  green: 'bg-green-500/10 text-green-400 border-green-500/20',
  blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  red: 'bg-red-500/10 text-red-400 border-red-500/20',
  gray: 'bg-gray-700/50 text-gray-300 border-gray-700',
  purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
}

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  color?: keyof typeof colors
}

export function Badge({ color = 'gray', className, children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium',
        colors[color],
        className,
      )}
      {...props}
    >
      {children}
    </span>
  )
}
