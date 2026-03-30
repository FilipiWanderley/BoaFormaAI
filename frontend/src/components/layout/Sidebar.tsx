import { NavLink, useNavigate } from 'react-router-dom'
import { LayoutDashboard, Dumbbell, MessageCircle, History, User, LogOut } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'

const nav = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Home' },
  { to: '/workout',   icon: Dumbbell,         label: 'Treino' },
  { to: '/chat',      icon: MessageCircle,     label: 'Chat IA' },
  { to: '/history',   icon: History,           label: 'Histórico' },
  { to: '/profile',   icon: User,              label: 'Perfil' },
]

export function Sidebar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const firstName = user?.name.split(' ')[0] ?? ''

  return (
    <aside className="flex h-screen w-[200px] shrink-0 flex-col bg-surface-1 border-r border-white/[0.06]">

      {/* Logo */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-baseline gap-1">
          <span className="text-[15px] font-semibold text-white tracking-tight">BoaForma</span>
          <span className="text-[10px] font-medium text-accent px-1 py-0.5 rounded bg-accent-muted">AI</span>
        </div>
      </div>

      <div className="h-px bg-white/[0.05] mx-4" />

      {/* Nav */}
      <nav className="flex flex-1 flex-col gap-px px-3 pt-4">
        {nav.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to}
            className={({ isActive }) =>
              `flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] font-medium transition-colors ${
                isActive
                  ? 'bg-white/[0.07] text-white'
                  : 'text-white/40 hover:text-white/70 hover:bg-white/[0.04]'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <Icon className={`h-[15px] w-[15px] shrink-0 ${isActive ? 'text-white' : ''}`} />
                {label}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* User */}
      <div className="px-3 pb-4">
        <div className="h-px bg-white/[0.05] mb-3" />
        <div className="flex items-center gap-2.5 px-3 py-2 mb-1">
          <div className="w-6 h-6 rounded-full bg-white/[0.08] flex items-center justify-center text-[11px] font-semibold text-white/60 shrink-0">
            {firstName.charAt(0).toUpperCase()}
          </div>
          <span className="text-[13px] text-white/50 truncate flex-1">{firstName}</span>
        </div>
        <button
          onClick={() => { logout(); navigate('/login') }}
          className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] font-medium text-white/30 hover:text-white/60 hover:bg-white/[0.04] transition-colors"
        >
          <LogOut className="h-[15px] w-[15px] shrink-0" />
          Sair
        </button>
      </div>
    </aside>
  )
}
