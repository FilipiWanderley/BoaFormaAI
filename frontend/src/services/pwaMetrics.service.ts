const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

type PwaEvent = 'install_prompt_shown' | 'install_accepted' | 'install_dismissed' | 'app_installed'

export async function trackPwaEvent(event: PwaEvent): Promise<void> {
  try {
    await fetch(`${API_BASE_URL}/ops/pwa-events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event }),
      keepalive: true,
    })
  } catch {
    return
  }
}
