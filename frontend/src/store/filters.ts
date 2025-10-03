import { create } from 'zustand'

export type Filters = {
  from: string
  to: string
  window: number
  cohort?: string
}

const today = new Date()
const thirtyDaysAgo = new Date(today.getTime() - 29 * 24 * 60 * 60 * 1000)

function toISODate(d: Date): string {
  return d.toISOString().slice(0, 10)
}

export const useFilters = create<{
  filters: Filters
  setFilters: (f: Partial<Filters>) => void
}>(set => ({
  filters: { from: toISODate(thirtyDaysAgo), to: toISODate(today), window: 7 },
  setFilters: (f) => set(s => ({ filters: { ...s.filters, ...f } })),
}))
