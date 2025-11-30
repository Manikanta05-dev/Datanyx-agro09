import React, { useState } from 'react'
import apiService from '../services/api'

function ManufacturerDashboard() {
  const [activeTab, setActiveTab] = useState('demand')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Demand Forecasting State
  const [demandForm, setDemandForm] = useState({
    region: 'Hyderabad',
    product: 'Oat Milk',
    price: 200,
    genz_ratio: 0.5,
    google_trends_score: 70,
    month: 6,
  })
  const [demandResult, setDemandResult] = useState(null)

  // Supply Chain State
  const [supplyForm, setSupplyForm] = useState({
    destination_city: 'Hyderabad',
    product: 'Oat Milk',
    required_quantity: 100,
  })
  const [supplyResult, setSupplyResult] = useState(null)

  // Combined Intelligence State
  const [intelligenceForm, setIntelligenceForm] = useState({
    region: 'Hyderabad',
    product: 'Oat Milk',
    district: 'Anantapur',
    crop: 'Oats',
    price: 200,
    month: 6,
  })
  const [intelligenceResult, setIntelligenceResult] = useState(null)

  const handleDemandForecast = async () => {
    setLoading(true)
    setError(null)
    const quarter = Math.floor((demandForm.month - 1) / 3) + 1
    const payload = { ...demandForm, quarter }
    const result = await apiService.forecastVeganDemand(payload)
    setLoading(false)
    if (result.success) {
      setDemandResult(result.data)
    } else {
      setError(result.error)
    }
  }

  const handleSupplyOptimize = async () => {
    setLoading(true)
    setError(null)
    const result = await apiService.optimizeSupplyChain(supplyForm)
    setLoading(false)
    if (result.success) {
      setSupplyResult(result.data)
    } else {
      setError(result.error)
    }
  }

  const handleIntelligence = async () => {
    setLoading(true)
    setError(null)
    const result = await apiService.combinedIntelligence(intelligenceForm)
    setLoading(false)
    if (result.success) {
      setIntelligenceResult(result.data)
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
          📈 Demand Forecasting
        </button>
        <button
          className={`tab ${activeTab === 'supply' ? 'active' : ''}`}
          onClick={() => setActiveTab('supply')}
        >
          🔗 Supply Chain Optimizer
        </button>
        <button
          className={`tab ${activeTab === 'intelligence' ? 'active' : ''}`}
          onClick={() => setActiveTab('intelligence')}
        >
          📊 Combined Intelligence
        </button>
      </div>

      {activeTab === 'demand' && (
        <div className="card">
          <h2>📈 Enhanced Demand Forecasting</h2>
          <p>Forecast vegan product demand with time-series intelligence, GenZ adoption, and price elasticity.</p>
          
          <div className="form-row">
            <div className="form-group">
              <label>Region</label>
              <select
                value={demandForm.region}
                onChange={(e) => setDemandForm({ ...demandForm, region: e.target.value })}
              >
                {['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai', 'Pune', 'Kolkata'].map(r => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Product</label>
              <select
                value={demandForm.product}
                onChange={(e) => setDemandForm({ ...demandForm, product: e.target.value })}
              >
                {['Oat Milk', 'Vegan Meat', 'Soy Products', 'Chickpea Flour', 'Almond Milk', 'Coconut Milk', 'Quinoa', 'Tofu'].map(p => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Price (₹)</label>
              <input
                type="number"
                value={demandForm.price}
                onChange={(e) => setDemandForm({ ...demandForm, price: parseFloat(e.target.value) })}
                min="0"
                step="1"
              />
            </div>
            <div className="form-group">
              <label>GenZ Ratio: {demandForm.genz_ratio.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={demandForm.genz_ratio}
                onChange={(e) => setDemandForm({ ...demandForm, genz_ratio: parseFloat(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Google Trends Score: {demandForm.google_trends_score}</label>
              <input
                type="range"
                min="0"
                max="100"
                step="1"
                value={demandForm.google_trends_score}
                onChange={(e) => setDemandForm({ ...demandForm, google_trends_score: parseInt(e.target.value) })}
              />
            </div>
            <div className="form-group">
              <label>Month</label>
              <input
                type="number"
                value={demandForm.month}
                onChange={(e) => setDemandForm({ ...demandForm, month: parseInt(e.target.value) })}
                min="1"
                max="12"
              />
            </div>
          </div>

          <button className="button" onClick={handleDemandForecast} disabled={loading}>
            {loading ? 'Forecasting...' : '🔮 Forecast Demand'}
          </button>

          {error && <div className="error">❌ Error: {error}</div>}
          {demandResult && (
            <div className="result-box">
              <h3>📊 Forecast Result</h3>
              <div className="result-value">Predicted Consumption: {demandResult.predicted_consumption?.toFixed(0)} units</div>
              <p><strong>GenZ Adoption Index:</strong> {demandResult.genz_adoption_index?.toFixed(3)}</p>
              <p><strong>Price Elasticity Score:</strong> {demandResult.price_elasticity_score?.toFixed(3)}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'supply' && (
        <div className="card">
          <h2>🔗 VORTEX Supply Chain Optimizer</h2>
          <p>Optimize sourcing, reduce costs, and minimize waste.</p>
          
          <div className="form-row">
            <div className="form-group">
              <label>Destination City</label>
              <select
                value={supplyForm.destination_city}
                onChange={(e) => setSupplyForm({ ...supplyForm, destination_city: e.target.value })}
              >
                {['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai'].map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Product</label>
              <select
                value={supplyForm.product}
                onChange={(e) => setSupplyForm({ ...supplyForm, product: e.target.value })}
              >
                {['Oat Milk', 'Soy Products', 'Chickpea Flour'].map(p => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Required Quantity (tons)</label>
              <input
                type="number"
                value={supplyForm.required_quantity}
                onChange={(e) => setSupplyForm({ ...supplyForm, required_quantity: parseFloat(e.target.value) })}
                min="1"
                step="10"
              />
            </div>
          </div>

          <button className="button" onClick={handleSupplyOptimize} disabled={loading}>
            {loading ? 'Optimizing...' : '⚡ Optimize Supply Chain'}
          </button>

          {error && <div className="error">❌ Error: {error}</div>}
          {supplyResult && (
            <div className="result-box">
              <h3>⚡ Optimization Result</h3>
              <div className="result-value">Total Cost: ₹{supplyResult.total_cost?.toFixed(2)}</div>
              <p><strong>Waste Reduction:</strong> {supplyResult.waste_reduction_percentage?.toFixed(1)}%</p>
              <h4>Optimal Sources:</h4>
              <ul>
                {supplyResult.optimal_sources?.map((source, idx) => (
                  <li key={idx}>
                    {source.source_district}: {source.allocation_percentage?.toFixed(1)}% 
                    (Suitability: {source.suitability_score?.toFixed(3)})
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {activeTab === 'intelligence' && (
        <div className="card">
          <h2>📊 Combined AI Decision Engine</h2>
          <p>Get comprehensive intelligence combining all models.</p>
          
          <div className="form-row">
            <div className="form-group">
              <label>Region</label>
              <select
                value={intelligenceForm.region}
                onChange={(e) => setIntelligenceForm({ ...intelligenceForm, region: e.target.value })}
              >
                {['Hyderabad', 'Bengaluru', 'Mumbai'].map(r => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Product</label>
              <select
                value={intelligenceForm.product}
                onChange={(e) => setIntelligenceForm({ ...intelligenceForm, product: e.target.value })}
              >
                {['Oat Milk', 'Vegan Meat', 'Soy Products'].map(p => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>District</label>
              <select
                value={intelligenceForm.district}
                onChange={(e) => setIntelligenceForm({ ...intelligenceForm, district: e.target.value })}
              >
                {['Anantapur', 'Kurnool', 'Hindupur', 'Mahabubnagar'].map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Crop</label>
              <select
                value={intelligenceForm.crop}
                onChange={(e) => setIntelligenceForm({ ...intelligenceForm, crop: e.target.value })}
              >
                {['Oats', 'Chickpea', 'Soy', 'Quinoa'].map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Price (₹)</label>
              <input
                type="number"
                value={intelligenceForm.price}
                onChange={(e) => setIntelligenceForm({ ...intelligenceForm, price: parseFloat(e.target.value) })}
                min="0"
              />
            </div>
            <div className="form-group">
              <label>Month</label>
              <input
                type="number"
                value={intelligenceForm.month}
                onChange={(e) => setIntelligenceForm({ ...intelligenceForm, month: parseInt(e.target.value) })}
                min="1"
                max="12"
              />
            </div>
          </div>

          <button className="button" onClick={handleIntelligence} disabled={loading}>
            {loading ? 'Generating...' : '🧠 Generate Intelligence Report'}
          </button>

          {error && <div className="error">❌ Error: {error}</div>}
          {intelligenceResult && (
            <div className="result-box">
              <h3>🧠 Intelligence Report</h3>
              <div className="result-value">Priority Score: {intelligenceResult.priority_score?.toFixed(3)}</div>
              <p><strong>Recommendation:</strong> {intelligenceResult.recommendation}</p>
              <details>
                <summary>Full Report</summary>
                <pre>{JSON.stringify(intelligenceResult, null, 2)}</pre>
              </details>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ManufacturerDashboard

