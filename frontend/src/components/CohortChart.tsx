import React, { useEffect, useMemo, useState } from 'react'
import Plot from 'react-plotly.js'
import { useFilters } from '../store/filters'
import { apiGet } from '../lib/api'

const days = Array.from({ length: 30 }).map((_, i) => `2025-09-${(i + 1).toString().padStart(2, '0')}`)

function randomWalk(seed: number) {
  let v = seed
  return days.map(() => (v = Math.max(20, Math.min(300, v + Math.round((Math.random() - 0.5) * 30)))))
}

export const CohortChart: React.FC = () => {
  const { filters } = useFilters()
  const [series, setSeries] = useState<{ date: string; total_minutes: number }[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const run = async () => {
      try {
        setError(null)
        const q = new URLSearchParams({ from: filters.from, to: filters.to })
        // 簡易的に全体の時系列で比較の代替（デモ）。将来: cohort別APIに差し替え。
        const resp = await apiGet<{ series: { date: string; total_minutes: number }[] }>(`/analytics/v1/timeseries?${q.toString()}`)
        setSeries(resp.series)
      } catch (e: any) {
        setError(e.message)
      }
    }
    run()
  }, [filters.from, filters.to])

  const plotData = useMemo(() => {
    if (!series) return [] as any[]
    const x = series.map(p => p.date)
    return [
      { x, y: series.map(p => p.total_minutes), type: 'scatter', mode: 'lines', name: '全体', line: { color: '#2563eb' } },
    ]
  }, [series])

  return (
    <div>
      {error && <div role="alert" style={{ color: 'crimson' }}>{error}</div>}
      <Plot
        data={plotData as any}
        layout={{ autosize: true, legend: { orientation: 'h' }, xaxis: { title: '日付' }, yaxis: { title: '総使用時間（分）' }, margin: { t: 24, r: 8, b: 40, l: 56 } }}
        style={{ width: '100%', height: 420 }}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  )
}
