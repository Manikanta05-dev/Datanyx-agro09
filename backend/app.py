"""
VOIS Backend API
Smart Vegan Supply & Demand Tracker - Flask REST API

This API implements the complete hackathon solution:
- OUTPUT 1: Vegan consumption analysis
- OUTPUT 2: Future demand forecasting (vegan meat, paneer, milk, oat milk, tofu, plant-based protein)
- OUTPUT 3: Optimal cultivation area recommendations (soy, oats, chickpeas, peas, millets)
- OUTPUT 4: Complete supply-demand intelligence system

3-Model AI System:
- MODEL 1: Demand Forecasting AI
- MODEL 2: Crop Suitability AI  
- MODEL 3: VORTEX Supply Chain Optimizer
"""

import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables to store loaded models and data
crop_advisor_model = None
demand_radar_model = None
crop_suitability_model = None
vegan_demand_model = None
vegan_consumption_df = None
crop_suitability_df = None
logistics_supply_df = None

def load_models():
    """Load all trained models at application startup."""
    global crop_advisor_model, demand_radar_model, crop_suitability_model, vegan_demand_model
    
    try:
        # Get the base directory (parent of backend/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models')
        
        # Load Crop Advisor model
        crop_model_path = os.path.join(models_dir, 'crop_advisor.pkl')
        with open(crop_model_path, 'rb') as f:
            crop_advisor_model = pickle.load(f)
        print(f"✓ Loaded Crop Advisor model")
        
        # Load Demand Radar model
        demand_model_path = os.path.join(models_dir, 'demand_radar.pkl')
        with open(demand_model_path, 'rb') as f:
            demand_radar_model = pickle.load(f)
        print(f"✓ Loaded Demand Radar model")
        
        # Load Crop Suitability model
        suitability_model_path = os.path.join(models_dir, 'crop_suitability.pkl')
        with open(suitability_model_path, 'rb') as f:
            crop_suitability_model = pickle.load(f)
        print(f"✓ Loaded Crop Suitability model")
        
        # Load Vegan Demand Forecast model
        vegan_model_path = os.path.join(models_dir, 'vegan_demand_forecast.pkl')
        with open(vegan_model_path, 'rb') as f:
            vegan_demand_model = pickle.load(f)
        print(f"✓ Loaded Vegan Demand Forecast model")
        
    except FileNotFoundError as e:
        print(f"Error: Model file not found - {e}")
        raise
    except Exception as e:
        print(f"Error loading models: {e}")
        raise

def load_data():
    """Load CSV data files for supply chain optimization."""
    global vegan_consumption_df, crop_suitability_df, logistics_supply_df
    
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        
        # Load dataframes
        vegan_consumption_df = pd.read_csv(os.path.join(data_dir, 'vegan_consumption.csv'))
        crop_suitability_df = pd.read_csv(os.path.join(data_dir, 'crop_suitability.csv'))
        logistics_supply_df = pd.read_csv(os.path.join(data_dir, 'logistics_supply.csv'))
        
        print(f"✓ Loaded data files")
        
    except Exception as e:
        print(f"Warning: Could not load data files: {e}")

# Load models and data at module level
try:
    load_models()
    load_data()
except Exception as e:
    print(f"Warning: Could not load models/data at startup: {e}")

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return "VOIS (V-Pulse) API is Online", 200

# ==================== EXISTING ENDPOINTS ====================

@app.route('/predict_demand', methods=['POST'])
def predict_demand():
    """Predict number of orders based on pricing and location data."""
    if demand_radar_model is None:
        return jsonify({"error": "Demand model not loaded"}), 500
    
    try:
        data = request.get_json()
        required_fields = ['base_price', 'checkout_price', 'center_id', 'meal_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        features = np.array([[float(data['base_price']), float(data['checkout_price']), 
                             int(data['center_id']), int(data['meal_id'])]])
        prediction = demand_radar_model.predict(features)[0]
        
        return jsonify({"predicted_orders": round(float(prediction))}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    """Recommend crop based on environmental and soil conditions."""
    if crop_advisor_model is None:
        return jsonify({"error": "Crop model not loaded"}), 500
    
    try:
        data = request.get_json()
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        features = np.array([[float(data['N']), float(data['P']), float(data['K']),
                             float(data['temperature']), float(data['humidity']),
                             float(data['ph']), float(data['rainfall'])]])
        prediction = crop_advisor_model.predict(features)[0]
        
        return jsonify({"recommended_crop": str(prediction)}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== NEW VOIS ENDPOINTS ====================

@app.route('/predict_suitability', methods=['POST'])
def predict_suitability():
    """
    Predict crop suitability score (0-1) for a district-crop combination.
    
    Expected JSON:
    {
        "district": str,
        "crop": str,
        "soil_ph": float,
        "soil_type": str,
        "rainfall": float,
        "temperature": float,
        "irrigation": int (0 or 1),
        "distance_to_city": float
    }
    
    Returns:
    {
        "suitability_score": float (0-1),
        "recommendation": str
    }
    """
    if crop_suitability_model is None:
        return jsonify({"error": "Suitability model not loaded"}), 500
    
    try:
        data = request.get_json()
        model_data = crop_suitability_model
        
        # Encode categorical features
        soil_encoded = model_data['soil_encoder'].transform([data['soil_type']])[0]
        crop_encoded = model_data['crop_encoder'].transform([data['crop']])[0]
        district_encoded = model_data['district_encoder'].transform([data['district']])[0]
        
        # Prepare features
        features = np.array([[
            float(data['soil_ph']), soil_encoded, float(data['rainfall']),
            float(data['temperature']), int(data['irrigation']),
            float(data['distance_to_city']), crop_encoded, district_encoded
        ]])
        
        # Predict
        score = model_data['model'].predict(features)[0]
        score = max(0, min(1, score))  # Clamp to [0, 1]
        
        # Generate recommendation
        if score >= 0.8:
            recommendation = "Highly suitable - Excellent conditions for this crop"
        elif score >= 0.6:
            recommendation = "Moderately suitable - Good conditions with minor adjustments"
        elif score >= 0.4:
            recommendation = "Marginally suitable - Requires significant improvements"
        else:
            recommendation = "Not suitable - Consider alternative crops or locations"
        
        return jsonify({
            "suitability_score": round(float(score), 3),
            "recommendation": recommendation
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/forecast_vegan_demand', methods=['POST'])
def forecast_vegan_demand():
    """
    Forecast vegan product demand with time-series features.
    
    Expected JSON:
    {
        "region": str,
        "product": str,
        "price": float,
        "genz_ratio": float (0-1),
        "google_trends_score": float (0-100),
        "month": int (1-12),
        "quarter": int (1-4)
    }
    
    Returns:
    {
        "predicted_consumption": float,
        "genz_adoption_index": float,
        "price_elasticity_score": float
    }
    """
    if vegan_demand_model is None:
        return jsonify({"error": "Vegan demand model not loaded"}), 500
    
    try:
        data = request.get_json()
        model_data = vegan_demand_model
        
        # Encode categorical features
        region_encoded = model_data['region_encoder'].transform([data['region']])[0]
        product_encoded = model_data['product_encoder'].transform([data['product']])[0]
        
        # Prepare features
        features = np.array([[
            float(data['price']), float(data['genz_ratio']),
            float(data['google_trends_score']), region_encoded,
            product_encoded, int(data['month']), int(data['quarter'])
        ]])
        
        # Predict consumption
        consumption = model_data['model'].predict(features)[0]
        consumption = max(0, consumption)  # Ensure non-negative
        
        # Calculate GenZ Adoption Index
        genz_index = float(data['genz_ratio']) * float(data['google_trends_score']) / 100
        
        # Calculate Price Elasticity Score (simplified)
        # Higher price typically reduces demand
        base_price = float(data['price'])
        price_elasticity = max(0, 1 - (base_price - 100) / 500)  # Normalized
        
        return jsonify({
            "predicted_consumption": round(float(consumption), 2),
            "genz_adoption_index": round(genz_index, 3),
            "price_elasticity_score": round(price_elasticity, 3)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/optimize_supply_chain', methods=['POST'])
def optimize_supply_chain():
    """
    Optimize supply chain using VORTEX Engine.
    
    Expected JSON:
    {
        "destination_city": str,
        "product": str,
        "required_quantity": float
    }
    
    Returns:
    {
        "optimal_sources": [
            {
                "source_district": str,
                "allocation_percentage": float,
                "transport_cost": float,
                "total_cost": float
            }
        ],
        "total_cost": float,
        "waste_reduction": float
    }
    """
    if logistics_supply_df is None or crop_suitability_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    try:
        data = request.get_json()
        destination = data['destination_city']
        product = data['product']
        required_qty = float(data['required_quantity'])
        
        # Find matching crops (simplified mapping)
        crop_mapping = {
            'Oat Milk': 'Oats',
            'Soy Products': 'Soy',
            'Chickpea Flour': 'Chickpea'
        }
        crop = crop_mapping.get(product, product.split()[0] if ' ' in product else product)
        
        # Filter logistics data
        logistics = logistics_supply_df[
            (logistics_supply_df['destination_city'] == destination) &
            (logistics_supply_df['crop'] == crop)
        ].copy()
        
        if len(logistics) == 0:
            return jsonify({"error": "No supply routes found"}), 404
        
        # Get suitability scores
        suitability = crop_suitability_df[
            crop_suitability_df['crop'] == crop
        ].copy()
        
        # Merge and calculate priority scores
        merged = logistics.merge(
            suitability,
            left_on='source_district',
            right_on='district',
            how='left'
        )
        
        # Calculate priority: higher suitability, lower cost
        merged['priority_score'] = (
            merged['suitability_score'].fillna(0.5) * 0.6 +
            (1 - merged['transport_cost'] / merged['transport_cost'].max()) * 0.4
        )
        
        # Sort by priority
        merged = merged.sort_values('priority_score', ascending=False)
        
        # Allocate supply
        optimal_sources = []
        remaining_qty = required_qty
        total_cost = 0
        
        for _, row in merged.iterrows():
            if remaining_qty <= 0:
                break
            
            available = min(row['supply_quantity'], remaining_qty)
            allocation_pct = (available / required_qty) * 100
            
            cost = row['transport_cost'] * (available / 1000)  # Cost per ton
            
            optimal_sources.append({
                "source_district": row['source_district'],
                "allocation_percentage": round(allocation_pct, 2),
                "transport_cost": round(row['transport_cost'], 2),
                "total_cost": round(cost, 2),
                "suitability_score": round(row['suitability_score'], 3)
            })
            
            total_cost += cost
            remaining_qty -= available
        
        # Calculate waste reduction (simplified)
        waste_reduction = min(50, len(optimal_sources) * 10)  # Up to 50%
        
        return jsonify({
            "optimal_sources": optimal_sources,
            "total_cost": round(total_cost, 2),
            "waste_reduction_percentage": round(waste_reduction, 1)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/combined_intelligence', methods=['POST'])
def combined_intelligence():
    """
    Combined AI Decision Engine - integrates all models.
    
    Expected JSON:
    {
        "region": str,
        "product": str,
        "district": str,
        "crop": str,
        "price": float,
        "month": int
    }
    
    Returns comprehensive intelligence report.
    """
    try:
        data = request.get_json()
        
        # Get demand forecast - directly predict instead of calling endpoint
        if vegan_demand_model is not None:
            try:
                model_data = vegan_demand_model
                region_encoded = model_data['region_encoder'].transform([data['region']])[0]
                product_encoded = model_data['product_encoder'].transform([data['product']])[0]
                
                price = float(data.get('price', 200))
                genz_ratio = float(data.get('genz_ratio', 0.5))
                google_trends = float(data.get('google_trends_score', 70))
                month = int(data.get('month', datetime.now().month))
                quarter = (month - 1) // 3 + 1
                
                features = np.array([[
                    price, genz_ratio, google_trends, region_encoded,
                    product_encoded, month, quarter
                ]])
                
                consumption = max(0, model_data['model'].predict(features)[0])
                genz_index = genz_ratio * google_trends / 100
                price_elasticity = max(0, 1 - (price - 100) / 500)
                
                demand_result = {
                    "predicted_consumption": round(float(consumption), 2),
                    "genz_adoption_index": round(genz_index, 3),
                    "price_elasticity_score": round(price_elasticity, 3)
                }
            except Exception as e:
                demand_result = {"predicted_consumption": 0, "error": str(e)}
        else:
            demand_result = {"predicted_consumption": 0}
        
        # Get suitability - directly predict instead of calling endpoint
        if crop_suitability_model is not None:
            try:
                model_data = crop_suitability_model
                district_encoded = model_data['district_encoder'].transform([data['district']])[0]
                crop_encoded = model_data['crop_encoder'].transform([data['crop']])[0]
                soil_type_encoded = model_data['soil_type_encoder'].transform([data.get('soil_type', 'Loamy')])[0]
                
                features = np.array([[
                    district_encoded, crop_encoded,
                    float(data.get('soil_ph', 7.0)),
                    soil_type_encoded,
                    float(data.get('rainfall', 600)),
                    float(data.get('temperature', 25)),
                    int(data.get('irrigation', 1)),
                    float(data.get('distance_to_city', 50))
                ]])
                
                score = max(0, min(1, model_data['model'].predict(features)[0]))
                
                if score >= 0.8:
                    recommendation = "Highly suitable - Excellent conditions for this crop"
                elif score >= 0.6:
                    recommendation = "Moderately suitable - Good conditions with minor adjustments"
                elif score >= 0.4:
                    recommendation = "Marginally suitable - Requires significant improvements"
                else:
                    recommendation = "Not suitable - Consider alternative crops or locations"
                
                suitability_result = {
                    "suitability_score": round(float(score), 3),
                    "recommendation": recommendation
                }
            except Exception as e:
                suitability_result = {"suitability_score": 0.5, "error": str(e)}
        else:
            suitability_result = {"suitability_score": 0.5}
        
        # Calculate priority score
        consumption = demand_result.get('predicted_consumption', 0)
        suitability = suitability_result.get('suitability_score', 0.5)
        
        # Normalize consumption (assuming typical range 0-2000)
        consumption_normalized = min(consumption / 2000, 1) if consumption > 0 else 0
        
        # Weighted priority score
        priority_score = (suitability * 0.5 + consumption_normalized * 0.5)
        
        # Add debug info
        print(f"DEBUG - Combined Intelligence:")
        print(f"  Consumption: {consumption}, Normalized: {consumption_normalized}")
        print(f"  Suitability: {suitability}")
        print(f"  Priority Score: {priority_score}")
        if 'error' in demand_result:
            print(f"  Demand Error: {demand_result['error']}")
        if 'error' in suitability_result:
            print(f"  Suitability Error: {suitability_result['error']}")
        
        return jsonify({
            "demand_forecast": demand_result,
            "suitability_analysis": suitability_result,
            "priority_score": round(priority_score, 3),
            "recommendation": "Proceed with production" if priority_score > 0.6 else "Review conditions"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure models are loaded before starting server
    if crop_advisor_model is None or demand_radar_model is None:
        print("Loading models...")
        load_models()
        load_data()
    
    print("\n" + "=" * 60)
    print("VOIS (V-Pulse) API Server Starting...")
    print("=" * 60)
    print("Endpoints:")
    print("  GET  / - Health check")
    print("  POST /predict_demand - Basic demand forecasting")
    print("  POST /recommend_crop - Crop recommendation")
    print("  POST /predict_suitability - Crop suitability scoring")
    print("  POST /forecast_vegan_demand - Enhanced demand forecasting")
    print("  POST /optimize_supply_chain - Supply chain optimization")
    print("  POST /combined_intelligence - Combined AI decision engine")
    print("=" * 60)
    
    # Get port from environment variable (for Heroku, Cloud platforms)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"\nServer running on http://0.0.0.0:{port}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
