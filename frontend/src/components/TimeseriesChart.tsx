import React, { useEffect, useMemo, useState } from 'react'
import Plot from 'react-plotly.js'
import { useFilters } from '../store/filters'
import { apiGet } from '../lib/api'

type SeriesResp = { series: { date: string; total_minutes: number; ma: number | null }[]; window: number }

export const TimeseriesChart: React.FC = () => {
  const { filters } = useFilters()
  const [data, setData] = useState<SeriesResp | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const run = async () => {
      try {
        setError(null)
        const q = new URLSearchParams({ from: filters.from, to: filters.to, window: String(filters.window) })
        const resp = await apiGet<SeriesResp>(`/analytics/v1/timeseries?${q.toString()}`)
        setData(resp)
      } catch (e: any) {
        setError(e.message)
      }
    }
    run()
  }, [filters.from, filters.to, filters.window])

  const plotData = useMemo(() => {
    if (!data) return [] as any[]
    const x = data.series.map(p => p.date)
    return [
      { x, y: data.series.map(p => p.total_minutes), type: 'scatter', mode: 'lines', name: '合計（分）', line: { color: '#0ea5e9' } },
      { x, y: data.series.map(p => p.ma), type: 'scatter', mode: 'lines', name: `${data.window}日移動平均`, line: { color: '#ef4444' } },
    ]
  }, [data])

  return (
    <div>
      {error && <div role="alert" style={{ color: 'crimson' }}>{error}</div>}
      <Plot data={plotData as any} layout={{ autosize: true, margin: { t: 24, r: 8, b: 40, l: 56 } }} style={{ width: '100%', height: 360 }} config={{ displayModeBar: false, responsive: true }} />
    </div>
  )
}
