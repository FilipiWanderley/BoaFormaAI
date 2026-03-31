import { useEffect, useState } from 'react'
import { trackPwaEvent } from '../../services/pwaMetrics.service'

type DeferredInstallPromptEvent = Event & {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>
}

export function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<DeferredInstallPromptEvent | null>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const handleBeforeInstallPrompt = (event: Event) => {
      event.preventDefault()
      setDeferredPrompt(event as DeferredInstallPromptEvent)
      setVisible(true)
      void trackPwaEvent('install_prompt_shown')
    }

    const handleInstalled = () => {
      setDeferredPrompt(null)
      setVisible(false)
      void trackPwaEvent('app_installed')
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    window.addEventListener('appinstalled', handleInstalled)

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
      window.removeEventListener('appinstalled', handleInstalled)
    }
  }, [])

  if (!visible || !deferredPrompt) {
    return null
  }

  const install = async () => {
    await deferredPrompt.prompt()
    const choice = await deferredPrompt.userChoice
    if (choice.outcome === 'accepted') {
      void trackPwaEvent('install_accepted')
    } else {
      void trackPwaEvent('install_dismissed')
    }
    setDeferredPrompt(null)
    setVisible(false)
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 z-50 mx-auto max-w-xl rounded-2xl border border-white/10 bg-bg-card p-4 shadow-lg">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-text-primary">Instalar Boa Forma AI</p>
          <p className="text-xs text-text-muted">Adicione à tela inicial para acesso mais rápido.</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              void trackPwaEvent('install_dismissed')
              setVisible(false)
            }}
            className="h-9 rounded-lg border border-white/10 px-3 text-xs text-text-muted"
          >
            Agora não
          </button>
          <button
            onClick={install}
            className="h-9 rounded-lg bg-accent px-3 text-xs font-semibold text-white"
          >
            Instalar
          </button>
        </div>
      </div>
    </div>
  )
}
