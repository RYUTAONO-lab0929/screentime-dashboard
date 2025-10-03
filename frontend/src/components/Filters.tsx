import React from 'react'
import { useFilters } from '../store/filters'

export const Filters: React.FC = () => {
  const { filters, setFilters } = useFilters()
  return (
    <form style={{ display: 'flex', gap: 12, alignItems: 'end', flexWrap: 'wrap' }} onSubmit={e => e.preventDefault()}>
      <label>
        <div>開始日</div>
        <input aria-label="開始日" type="date" value={filters.from} onChange={e => setFilters({ from: e.target.value })} />
      </label>
      <label>
        <div>終了日</div>
        <input aria-label="終了日" type="date" value={filters.to} onChange={e => setFilters({ to: e.target.value })} />
      </label>
      <label>
        <div>移動平均</div>
        <select aria-label="移動平均" value={filters.window} onChange={e => setFilters({ window: Number(e.target.value) })}>
          {[7, 14, 28].map(w => (
            <option key={w} value={w}>{w}日</option>
          ))}
        </select>
      </label>
    </form>
  )
}
