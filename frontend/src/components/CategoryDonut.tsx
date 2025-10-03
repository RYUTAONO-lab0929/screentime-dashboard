import React, { useEffect, useMemo, useState } from 'react'
import Plot from 'react-plotly.js'
import { useFilters } from '../store/filters'
import { apiGet } from '../lib/api'

export const CategoryDonut: React.FC = () => {
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

  const plotData = useMemo(() => {
    if (!data?.category_ratio) return [] as any[]
    const labels = Object.keys(data.category_ratio)
    const values = labels.map(l => data.category_ratio[l])
    return [{
      type: 'pie', hole: .5, labels, values, textinfo: 'label+percent', hoverinfo:'label+percent+value'
    }]
  }, [data])

  return (
    <div>
      {error && <div role="alert" className="text-red-500">{error}</div>}
      <Plot data={plotData as any} layout={{ showlegend: true, margin: { t: 16, b: 16, l: 16, r: 16 } }} style={{ width: '100%', height: 320 }} config={{ displayModeBar: false, responsive: true }} />
    </div>
  )
}
