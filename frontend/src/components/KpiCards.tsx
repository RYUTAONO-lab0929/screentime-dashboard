import React, { useEffect, useState } from 'react'
import { useFilters } from '../store/filters'
import { apiGet } from '../lib/api'

export const KpiCards: React.FC = () => {
  const { filters } = useFilters()
  const [data, setData] = useState<any>(null)
  const [error, setError] = useState<string|null>(null)

  useEffect(() => {
    const run = async () => {
      try {
        setError(null)
        const q = new URLSearchParams({ from: filters.from, to: filters.to })
        const resp = await apiGet(`/analytics/v1/kpi?${q.toString()}`)
        setData(resp)
      } catch (e:any) { setError(e.message) }
    }
    run()
  }, [filters.from, filters.to])

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {error && <div role="alert" className="text-red-500">{error}</div>}
      <div className="rounded bg-slate-100 dark:bg-slate-800 p-3">
        <div className="text-xs text-slate-500">総使用時間</div>
        <div className="text-xl font-semibold">{data?.total_minutes?.toLocaleString?.() ?? '-'}</div>
      </div>
      <div className="rounded bg-slate-100 dark:bg-slate-800 p-3">
        <div className="text-xs text-slate-500">ピックアップ</div>
        <div className="text-xl font-semibold">{data?.pickups?.toLocaleString?.() ?? '-'}</div>
      </div>
      <div className="rounded bg-slate-100 dark:bg-slate-800 p-3">
        <div className="text-xs text-slate-500">通知</div>
        <div className="text-xl font-semibold">{data?.notifications?.toLocaleString?.() ?? '-'}</div>
      </div>
      <div className="rounded bg-slate-100 dark:bg-slate-800 p-3">
        <div className="text-xs text-slate-500">上位アプリ</div>
        <div className="text-sm">{Array.isArray(data?.top_apps) ? data.top_apps.slice(0,3).map((t:any)=>t[0]).join(', ') : '-'}</div>
      </div>
    </div>
  )
}
