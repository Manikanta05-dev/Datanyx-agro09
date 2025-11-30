import React, { useState } from 'react'
import apiService from '../services/api'

function LegacyTools() {
  const [activeTab, setActiveTab] = useState('demand')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Demand Radar State
  const [demandForm, setDemandForm] = useState({
    base_price: 10.0,
    checkout_price: 12.0,
    center_id: 1,
    meal_id: 1,
  })
  const [demandResult, setDemandResult] = useState(null)

  // Cultivation Commander State
  const [cropForm, setCropForm] = useState({
    N: 50.0,
    P: 50.0,
    K: 50.0,
    temperature: 25.0,
    humidity: 60.0,
    ph: 7.0,
    rainfall: 100.0,
  })
  const [cropResult, setCropResult] = useState(null)

  const handleDemand = async () => {
    setLoading(true)
    setError(null)
    const result = await apiService.predictDemand(demandForm)
    setLoading(false)
    if (result.success) {
      setDemandResult(result.data)
    } else {
      setError(result.error)
    }
  }

  const handleCrop = async () => {
    setLoading(true)
    setError(null)
    const result = await apiService.recommendCrop(cropForm)
    setLoading(false)
    if (result.success) {
      setCropResult(result.data)
    } else {
      setError(result.error)
    }
  }

  return (
    <div>
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'demand' ? 'active' : ''}`}
          onClick={() => setActiveTab('demand')}
        >
          📈 Demand Radar
        </button>
        <button
          className={`tab ${activeTab === 'crop' ? 'active' : ''}`}
          onClick={() => setActiveTab('crop')}
        >
          🚜 Cultivation Commander
        </button>
      </div>

      {activeTab === 'demand' && (
        <div className="card">
          <h2>📈 Demand Radar</h2>
          <p>Forecast demand for vegan meals based on pricing and location data.</p>
          
          <div className="form-row">
            <div className="form-group">
              <label>Base Price ($)</label>
              <input
                type="number"
                value={demandForm.base_price}
                onChange={(e) => setDemandForm({ ...demandForm, base_price: parseFloat(e.target.value) })}
                min="0"
                max="100"
                step="0.01"
              />
            </div>
            <div className="form-group">
              <label>Checkout Price ($)</label>
              <input
                type="number"
                value={demandForm.checkout_price}
                onChange={(e) => setDemandForm({ ...demandForm, checkout_price: parseFloat(e.target.value) })}
                min="0"
                max="100"
                step="0.01"
              />
            </div>
            <div className="form-group">
              <label>Center ID</label>
              <input
                type="number"
                value={demandForm.center_id}
                onChange={(e) => setDemandForm({ ...demandForm, center_id: parseInt(e.target.value) })}
                min="1"
                max="100"
              />
            </div>
            <div className="form-group">
              <label>Meal ID</label>
              <input
                type="number"
                value={demandForm.meal_id}
                onChange={(e) => setDemandForm({ ...demandForm, meal_id: parseInt(e.target.value) })}
                min="1"
                max="100"
              />
            </div>
          </div>

          <button className="button" onClick={handleDemand} disabled={loading}>
            {loading ? 'Forecasting...' : '🔮 Forecast Demand'}
          </button>

          {error && <div className="error">❌ Error: {error}</div>}
          {demandResult && (
            <div className="result-box">
              <h3>📊 Forecast Result</h3>
              <div className="result-value">Predicted Orders: {demandResult.predicted_orders}</div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'crop' && (
        <div className="card">
          <h2>🚜 Cultivation Commander</h2>
          <p>Get crop recommendations based on soil and environmental conditions.</p>
          
          <div className="form-row">
            <div className="form-group">
              <label>Nitrogen (N): {cropForm.N.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="150"
                step="0.1"
                value={cropForm.N}
                onChange={(e) => setCropForm({ ...cropForm, N: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Phosphorus (P): {cropForm.P.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="150"
                step="0.1"
                value={cropForm.P}
                onChange={(e) => setCropForm({ ...cropForm, P: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Potassium (K): {cropForm.K.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="150"
                step="0.1"
                value={cropForm.K}
                onChange={(e) => setCropForm({ ...cropForm, K: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Temperature (°C): {cropForm.temperature.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="50"
                step="0.1"
                value={cropForm.temperature}
                onChange={(e) => setCropForm({ ...cropForm, temperature: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Humidity (%): {cropForm.humidity.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="100"
                step="0.1"
                value={cropForm.humidity}
                onChange={(e) => setCropForm({ ...cropForm, humidity: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>pH Level: {cropForm.ph.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="14"
                step="0.1"
                value={cropForm.ph}
                onChange={(e) => setCropForm({ ...cropForm, ph: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Rainfall (mm): {cropForm.rainfall.toFixed(1)}</label>
              <input
                type="range"
                min="0"
                max="400"
                step="0.1"
                value={cropForm.rainfall}
                onChange={(e) => setCropForm({ ...cropForm, rainfall: parseFloat(e.target.value) })}
              />
            </div>
          </div>

          <button className="button" onClick={handleCrop} disabled={loading}>
            {loading ? 'Analyzing...' : '🔍 Analyze Soil'}
          </button>

          {error && <div className="error">❌ Error: {error}</div>}
          {cropResult && (
            <div className="result-box">
              <h3>🌾 Crop Recommendation</h3>
              <div className="result-value">Recommended Crop: {cropResult.recommended_crop}</div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default LegacyTools

