import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Menu } from 'lucide-react'
import { Sidebar } from './Sidebar'

export function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <div className="flex min-h-screen bg-surface-0">
      <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />
      <main className="flex-1 min-w-0 overflow-y-auto">
        <header className="sticky top-0 z-20 border-b border-white/[0.05] bg-surface-0/90 backdrop-blur md:hidden">
          <div className="flex h-14 items-center justify-between px-4">
            <button
              type="button"
              onClick={() => setMobileOpen(true)}
              className="h-10 w-10 rounded-xl border border-white/[0.08] bg-surface-2 text-white/70 flex items-center justify-center"
            >
              <Menu className="w-4 h-4" />
            </button>
            <div className="flex items-baseline gap-1">
              <span className="text-[14px] font-semibold text-white tracking-tight">BoaForma</span>
              <span className="text-[10px] font-medium text-accent px-1 py-0.5 rounded bg-accent-muted">AI</span>
            </div>
            <div className="w-10" />
          </div>
        </header>
        <div className="mx-auto max-w-5xl px-4 py-6 md:px-8 md:py-8 lg:px-10 lg:py-9">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
