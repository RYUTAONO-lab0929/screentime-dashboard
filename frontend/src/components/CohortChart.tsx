import React from 'react'
import Plot from 'react-plotly.js'

const days = Array.from({ length: 30 }).map((_, i) => `2025-09-${(i + 1).toString().padStart(2, '0')}`)

function randomWalk(seed: number) {
  let v = seed
  return days.map(() => (v = Math.max(20, Math.min(300, v + Math.round((Math.random() - 0.5) * 30)))))
}

export const CohortChart: React.FC = () => {
  const a = randomWalk(120)
  const b = randomWalk(150)

  return (
    <Plot
      data={[
        { x: days, y: a, type: 'scatter', mode: 'lines', name: '実験群', line: { color: '#2563eb' } },
        { x: days, y: b, type: 'scatter', mode: 'lines', name: '対照群', line: { color: '#f59e0b' } },
      ]}
      layout={{
        autosize: true,
        legend: { orientation: 'h' },
        xaxis: { title: '日付' },
        yaxis: { title: '総使用時間（分）' },
        margin: { t: 24, r: 8, b: 40, l: 56 },
      }}
      style={{ width: '100%', height: 420 }}
      config={{ displayModeBar: false, responsive: true }}
    />
  )
}
