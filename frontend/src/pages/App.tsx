import React from 'react'
import { CohortChart } from '../components/CohortChart'
import { Filters } from '../components/Filters'
import { TimeseriesChart } from '../components/TimeseriesChart'
import { KpiCards } from '../components/KpiCards'
import { CategoryDonut } from '../components/CategoryDonut'
import { TopAppsTable } from '../components/TopAppsTable'

export const App: React.FC = () => {
  return (
    <div className="px-4 py-4 max-w-6xl mx-auto text-slate-900 dark:text-slate-100">
      <header className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Screentime Dashboard</h1>
        <div>
          <button aria-label="ダークモード切替" className="px-2 py-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800" onClick={() => {
            const el = document.documentElement
            const dark = el.classList.toggle('dark')
            try { localStorage.setItem('theme', dark ? 'dark' : 'light') } catch(e){}
          }}>🌓</button>
        </div>
      </header>

      <section className="mt-6">
        <h2 className="text-base font-medium mb-2">フィルタ</h2>
        <Filters />
      </section>

      <section className="mt-6 grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-4">
          <KpiCards />
        </div>
        <div className="lg:col-span-3">
          <h2 className="text-base font-medium mb-2">時系列（移動平均）</h2>
          <TimeseriesChart />
        </div>
        <div className="lg:col-span-1">
          <h2 className="text-base font-medium mb-2">カテゴリ比率</h2>
          <CategoryDonut />
        </div>
      </section>

      <section className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <h2 className="text-base font-medium mb-2">コホート比較（ダミーデータ）</h2>
          <CohortChart />
        </div>
        <div className="lg:col-span-1">
          <TopAppsTable />
        </div>
      </section>

      <section className="mt-6">
        <h2 className="text-base font-medium mb-2">エクスポート</h2>
        <div className="flex gap-2">
          <a className="px-3 py-1 rounded bg-slate-200 dark:bg-slate-800" href={(import.meta.env.VITE_API_BASE || '/api') + '/exports/v1/csv'} target="_blank" rel="noreferrer" aria-label="CSVエクスポート">CSV</a>
          <a className="px-3 py-1 rounded bg-slate-200 dark:bg-slate-800" href={(import.meta.env.VITE_API_BASE || '/api') + '/exports/v1/pdf'} target="_blank" rel="noreferrer" aria-label="PDFエクスポート">PDF</a>
        </div>
      </section>
    </div>
  )
}
