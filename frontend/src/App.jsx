import React, { useState } from 'react'
import ManufacturerDashboard from './components/ManufacturerDashboard'
import FarmerDashboard from './components/FarmerDashboard'
import ConsumerDashboard from './components/ConsumerDashboard'
import LegacyTools from './components/LegacyTools'
import './App.css'

function App() {
  const [activeDashboard, setActiveDashboard] = useState('manufacturer')

  const dashboards = [
    { id: 'manufacturer', label: '🏭 Manufacturer', component: ManufacturerDashboard },
    { id: 'farmer', label: '👨‍🌾 Farmer', component: FarmerDashboard },
    { id: 'consumer', label: '🛒 Consumer', component: ConsumerDashboard },
    { id: 'legacy', label: '📊 Legacy Tools', component: LegacyTools },
  ]

  const ActiveComponent = dashboards.find(d => d.id === activeDashboard)?.component || ManufacturerDashboard

  return (
    <div className="app">
      <header className="header">
        <h1>🌱 VOIS - Vegan Orbital Intelligence System</h1>
      </header>
      
      <nav className="nav">
        {dashboards.map(dashboard => (
          <button
            key={dashboard.id}
            className={`nav-button ${activeDashboard === dashboard.id ? 'active' : ''}`}
            onClick={() => setActiveDashboard(dashboard.id)}
          >
            {dashboard.label}
          </button>
        ))}
      </nav>

      <main className="main-content">
        <ActiveComponent />
      </main>
    </div>
  )
}

export default App

