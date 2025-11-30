import React, { useState } from 'react'

function ConsumerDashboard() {
  const [activeTab, setActiveTab] = useState('trending')

  return (
    <div>
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'trending' ? 'active' : ''}`}
          onClick={() => setActiveTab('trending')}
        >
          📊 Trending Products
        </button>
        <button
          className={`tab ${activeTab === 'sustainability' ? 'active' : ''}`}
          onClick={() => setActiveTab('sustainability')}
        >
          🌱 Sustainability Score
        </button>
      </div>

      {activeTab === 'trending' && (
        <div className="card">
          <h2>📊 Trending Vegan Products</h2>
          <div className="info">
            <p>Discover trending vegan products in your region with GenZ adoption metrics.</p>
            <p>Use the Manufacturer dashboard's Demand Forecasting to see trending products.</p>
          </div>
        </div>
      )}

      {activeTab === 'sustainability' && (
        <div className="card">
          <h2>🌱 Sustainability Score</h2>
          <div className="info">
            <p>View sustainability metrics and environmental impact scores.</p>
            <p>Sustainability features coming soon!</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ConsumerDashboard

