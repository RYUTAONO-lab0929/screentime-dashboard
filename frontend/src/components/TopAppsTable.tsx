import React, { useEffect, useState } from 'react'
import { useFilters } from '../store/filters'
import { apiGet } from '../lib/api'

export const TopAppsTable: React.FC = () => {
  const { filters } = useFilters()
  const [apps, setApps] = useState<[string, number][]>([])
  const [error, setError] = useState<string|null>(null)

  useEffect(() => {
    const run = async () => {
      try {
        setError(null)
        const q = new URLSearchParams({ from: filters.from, to: filters.to })
        const resp = await apiGet<{ top_apps: [string, number][] }>(`/analytics/v1/kpi?${q.toString()}`)
        setApps(resp.top_apps || [])
      } catch (e:any) { setError(e.message) }
    }
    run()
  }, [filters.from, filters.to])

  return (
    <div className="rounded bg-slate-100 dark:bg-slate-800 p-3">
      <div className="text-base font-medium mb-2">上位アプリ</div>
      {error && <div role="alert" className="text-red-500">{error}</div>}
      <div className="max-h-64 overflow-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500">
              <th className="py-1">アプリ</th>
              <th className="py-1">総分</th>
            </tr>
          </thead>
          <tbody>
            {apps.map(([bundle, minutes]) => (
              <tr key={bundle} className="border-t border-slate-200 dark:border-slate-700">
                <td className="py-1">{bundle || '(unknown)'}</td>
                <td className="py-1 tabular-nums">{minutes.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
