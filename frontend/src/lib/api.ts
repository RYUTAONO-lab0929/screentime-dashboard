export function apiBase(): string {
  return (import.meta.env.VITE_API_BASE as string) || '/api'
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const base = apiBase()
  const res = await fetch(`${base}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    credentials: 'omit',
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json() as Promise<T>
}

export async function apiGetAuth<T>(path: string, init?: RequestInit): Promise<T> {
  const token = (import.meta.env.VITE_RESEARCHER_TOKEN as string) || ''
  return apiGet<T>(path, {
    ...init,
    headers: {
      ...(init?.headers || {}),
      Authorization: token ? `Bearer ${token}` : '',
    },
  })
}
