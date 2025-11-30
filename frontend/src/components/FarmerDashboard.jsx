import React, { useState } from 'react'
import apiService from '../services/api'

function FarmerDashboard() {
  const [activeTab, setActiveTab] = useState('suitability')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [suitabilityForm, setSuitabilityForm] = useState({
    district: 'Anantapur',
    crop: 'Oats',
    soil_ph: 7.0,
    soil_type: 'Loamy',
    rainfall: 600,
    temperature: 25,
    irrigation: 1,
    distance_to_city: 50,
  })
  const [suitabilityResult, setSuitabilityResult] = useState(null)

  const handleSuitability = async () => {
    setLoading(true)
    setError(null)
    const result = await apiService.predictSuitability(suitabilityForm)
    setLoading(false)
    if (result.success) {
      setSuitabilityResult(result.data)
    } else {
      setError(result.error)
    }
  }

  return (
    <div>
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'suitability' ? 'active' : ''}`}
          onClick={() => setActiveTab('suitability')}
        >
          🌾 Crop Suitability
        </button>
        <button
          className={`tab ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          📈 Market Insights
        </button>
      </div>

      {activeTab === 'suitability' && (
        <div className="card">
          <h2>🌾 Crop Suitability Analyzer</h2>
          <p>Get AI-powered suitability scores for your district and crop combinations.</p>
          
          <div className="form-row">
            <div className="form-group">
              <label>District</label>
              <select
                value={suitabilityForm.district}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, district: e.target.value })}
              >
                {['Anantapur', 'Kurnool', 'Hindupur', 'Mahabubnagar', 'Nalgonda', 'Warangal'].map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Crop</label>
              <select
                value={suitabilityForm.crop}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, crop: e.target.value })}
              >
                {['Oats', 'Chickpea', 'Soy', 'Quinoa', 'Lentils', 'Mungbean'].map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Soil Type</label>
              <select
                value={suitabilityForm.soil_type}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, soil_type: e.target.value })}
              >
                {['Loamy', 'Sandy', 'Clay', 'Sandy Loam', 'Clay Loam'].map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Soil pH: {suitabilityForm.soil_ph.toFixed(1)}</label>
              <input
                type="range"
                min="5.5"
                max="8.5"
                step="0.1"
                value={suitabilityForm.soil_ph}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, soil_ph: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Rainfall (mm): {suitabilityForm.rainfall}</label>
              <input
                type="range"
                min="300"
                max="1200"
                step="10"
                value={suitabilityForm.rainfall}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, rainfall: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Temperature (°C): {suitabilityForm.temperature}</label>
              <input
                type="range"
                min="15"
                max="35"
                step="0.5"
                value={suitabilityForm.temperature}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, temperature: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Irrigation</label>
              <select
                value={suitabilityForm.irrigation}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, irrigation: parseInt(e.target.value) })}
              >
                <option value={1}>Irrigated</option>
                <option value={0}>Rainfed</option>
              </select>
            </div>
            <div className="form-group">
              <label>Distance to City (km): {suitabilityForm.distance_to_city}</label>
              <input
                type="range"
                min="10"
                max="200"
                step="5"
                value={suitabilityForm.distance_to_city}
                onChange={(e) => setSuitabilityForm({ ...suitabilityForm, distance_to_city: parseFloat(e.target.value) })}
              />
            </div>
          </div>

          <button className="button" onClick={handleSuitability} disabled={loading}>
            {loading ? 'Analyzing...' : '🔍 Analyze Suitability'}
          </button>

          {error && <div className="error">❌ Error: {error}</div>}
          {suitabilityResult && (
            <div className="result-box">
              <h3>🌾 Suitability Analysis</h3>
              {suitabilityResult.suitability_score >= 0.8 ? (
                <div className="result-value" style={{ color: '#2E7D32' }}>
                  Suitability Score: {suitabilityResult.suitability_score?.toFixed(3)} - Highly Suitable! 🌟
                </div>
              ) : suitabilityResult.suitability_score >= 0.6 ? (
                <div className="result-value" style={{ color: '#2196F3' }}>
                  Suitability Score: {suitabilityResult.suitability_score?.toFixed(3)} - Moderately Suitable
                </div>
              ) : (
                <div className="result-value" style={{ color: '#ff9800' }}>
                  Suitability Score: {suitabilityResult.suitability_score?.toFixed(3)} - Low Suitability
                </div>
              )}
              <p><strong>Recommendation:</strong> {suitabilityResult.recommendation}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'insights' && (
        <div className="card">
          <h2>📈 Market Insights & Buyback Opportunities</h2>
          <div className="info">
            <p>Get demand forecasts and market trends for your crops.</p>
            <p>Use the Manufacturer dashboard's Demand Forecasting tool to see market demand for your crops.</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default FarmerDashboard

