import React from 'react'
import { CohortChart } from '../components/CohortChart'

export const App: React.FC = () => {
  return (
    <div style={{ padding: 16, maxWidth: 1200, margin: '0 auto' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: 20 }}>Screentime Dashboard</h1>
        <div>
          <button aria-label="ダークモード切替">🌓</button>
        </div>
      </header>

      <section>
        <h2 style={{ fontSize: 16 }}>コホート比較（ダミーデータ）</h2>
        <CohortChart />
      </section>
    </div>
  )
}
