import axios from 'axios'

const API_URL = 'http://localhost:5000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/')
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Basic demand prediction
  predictDemand: async (data) => {
    try {
      const response = await api.post('/predict_demand', data)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message }
    }
  },

  // Crop recommendation
  recommendCrop: async (data) => {
    try {
      const response = await api.post('/recommend_crop', data)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message }
    }
  },

  // Crop suitability
  predictSuitability: async (data) => {
    try {
      const response = await api.post('/predict_suitability', data)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message }
    }
  },

  // Enhanced vegan demand forecast
  forecastVeganDemand: async (data) => {
    try {
      const response = await api.post('/forecast_vegan_demand', data)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message }
    }
  },

  // Supply chain optimization
  optimizeSupplyChain: async (data) => {
    try {
      const response = await api.post('/optimize_supply_chain', data)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message }
    }
  },

  // Combined intelligence
  combinedIntelligence: async (data) => {
    try {
      const response = await api.post('/combined_intelligence', data)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message }
    }
  },
}

export default apiService

