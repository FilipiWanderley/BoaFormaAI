interface RingProgressProps {
  value: number      // 0–100
  size?: number
  strokeWidth?: number
  color?: string
  bg?: string
  children?: React.ReactNode
}

export function RingProgress({
  value,
  size = 129,
  strokeWidth = 10,
  color = '#1e3fb9',
  bg = '#444',
  children,
}: RingProgressProps) {
  const r      = (size - strokeWidth) / 2
  const cx     = size / 2
  const cy     = size / 2
  const circ   = 2 * Math.PI * r
  const offset = circ - (Math.min(value, 100) / 100) * circ

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={bg} strokeWidth={strokeWidth} />
        <circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 0.6s ease' }}
        />
      </svg>
      {children && (
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          {children}
        </div>
      )}
    </div>
  )
}
