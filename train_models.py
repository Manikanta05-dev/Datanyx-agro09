"""
VOIS Model Training Script
Smart Vegan Supply & Demand Tracker - AI Model Training

This script trains the 3-model AI system:
1. MODEL 1: Demand Forecasting AI (Random Forest with time-series features)
2. MODEL 2: Crop Suitability AI (Random Forest Regression for 0-1 scoring)
3. MODEL 3: VORTEX Optimizer (uses Models 1 & 2 + logistics data)

All models align with hackathon problem statement requirements.
"""

import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np

def train_crop_advisor():
    """
    Train RandomForestClassifier for crop recommendation.
    Features: N, P, K, temperature, humidity, ph, rainfall
    Target: label
    """
    print("=" * 60)
    print("Training Supply Model: Crop Advisor")
    print("=" * 60)
    
    # Load data
    data_path = os.path.join('data', 'crop_data.csv')
    df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} samples")
    print(f"Features: {list(df.columns[:-1])}")
    print(f"Target: {df.columns[-1]}")
    print(f"Classes: {df['label'].unique()}")
    
    # Prepare features and target
    feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_columns]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train model
    print("\nTraining RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"  Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join('models', 'crop_advisor.pkl')
    os.makedirs('models', exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\n✓ Model saved to {model_path}")
    
    return model

def train_demand_radar():
    """
    Train RandomForestRegressor for sales forecasting.
    Features: base_price, checkout_price, center_id, meal_id
    Target: num_orders
    """
    print("\n" + "=" * 60)
    print("Training Demand Model: Demand Radar")
    print("=" * 60)
    
    # Load data
    data_path = os.path.join('data', 'demand_data.csv')
    df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} samples")
    print(f"Features: {list(df.columns[:-1])}")
    print(f"Target: {df.columns[-1]}")
    
    # Prepare features and target
    feature_columns = ['base_price', 'checkout_price', 'center_id', 'meal_id']
    X = df[feature_columns]
    y = df['num_orders']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    print(f"Target range: {y.min()} - {y.max()} orders")
    
    # Train model
    print("\nTraining RandomForestRegressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"  Test RMSE: {rmse:.4f}")
    print(f"  Test R² Score: {r2:.4f} ({r2*100:.2f}%)")
    print(f"  Mean Actual Orders: {y_test.mean():.2f}")
    print(f"  Mean Predicted Orders: {y_pred.mean():.2f}")
    
    # Save model
    model_path = os.path.join('models', 'demand_radar.pkl')
    os.makedirs('models', exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\n✓ Model saved to {model_path}")
    
    return model

def train_crop_suitability():
    """
    Train RandomForestRegressor for crop suitability scoring.
    Features: soil_ph, soil_type, rainfall, temperature, irrigation, distance_to_city
    Target: suitability_score (0-1)
    """
    print("\n" + "=" * 60)
    print("Training Crop Suitability Model")
    print("=" * 60)
    
    # Load data
    data_path = os.path.join('data', 'crop_suitability.csv')
    df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} samples")
    print(f"Districts: {df['district'].nunique()}")
    print(f"Crops: {df['crop'].nunique()}")
    
    # Encode categorical features
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()
    le_district = LabelEncoder()
    
    df['soil_type_encoded'] = le_soil.fit_transform(df['soil_type'])
    df['crop_encoded'] = le_crop.fit_transform(df['crop'])
    df['district_encoded'] = le_district.fit_transform(df['district'])
    
    # Prepare features and target
    feature_columns = ['soil_ph', 'soil_type_encoded', 'rainfall', 'temperature', 
                      'irrigation', 'distance_to_city', 'crop_encoded', 'district_encoded']
    X = df[feature_columns]
    y = df['suitability_score']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    print(f"Target range: {y.min():.3f} - {y.max():.3f}")
    
    # Train model
    print("\nTraining RandomForestRegressor for Suitability...")
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"  Test RMSE: {rmse:.4f}")
    print(f"  Test R² Score: {r2:.4f} ({r2*100:.2f}%)")
    print(f"  Mean Actual Score: {y_test.mean():.3f}")
    print(f"  Mean Predicted Score: {y_pred.mean():.3f}")
    
    # Save model and encoders
    model_path = os.path.join('models', 'crop_suitability.pkl')
    os.makedirs('models', exist_ok=True)
    
    model_data = {
        'model': model,
        'soil_encoder': le_soil,
        'crop_encoder': le_crop,
        'district_encoder': le_district
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✓ Model saved to {model_path}")
    
    return model

def train_vegan_demand_forecast():
    """
    Train enhanced demand forecasting model with time-series features.
    Features: price, genz_ratio, google_trends_score, region, product, month, season
    Target: consumption
    """
    print("\n" + "=" * 60)
    print("Training Enhanced Vegan Demand Forecast Model")
    print("=" * 60)
    
    # Load data
    data_path = os.path.join('data', 'vegan_consumption.csv')
    df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} samples")
    print(f"Regions: {df['region'].nunique()}")
    print(f"Products: {df['product'].nunique()}")
    
    # Convert date to datetime and extract features
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Encode categorical features
    le_region = LabelEncoder()
    le_product = LabelEncoder()
    
    df['region_encoded'] = le_region.fit_transform(df['region'])
    df['product_encoded'] = le_product.fit_transform(df['product'])
    
    # Prepare features and target
    feature_columns = ['price', 'genz_ratio', 'google_trends_score', 
                      'region_encoded', 'product_encoded', 'month', 'quarter']
    X = df[feature_columns]
    y = df['consumption']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    print(f"Target range: {y.min()} - {y.max()}")
    
    # Train model
    print("\nTraining RandomForestRegressor for Demand Forecast...")
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=12,
        min_samples_split=5,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"  Test RMSE: {rmse:.2f}")
    print(f"  Test R² Score: {r2:.4f} ({r2*100:.2f}%)")
    print(f"  Mean Actual Consumption: {y_test.mean():.2f}")
    print(f"  Mean Predicted Consumption: {y_pred.mean():.2f}")
    
    # Save model and encoders
    model_path = os.path.join('models', 'vegan_demand_forecast.pkl')
    os.makedirs('models', exist_ok=True)
    
    model_data = {
        'model': model,
        'region_encoder': le_region,
        'product_encoder': le_product
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✓ Model saved to {model_path}")
    
    return model

def main():
    """Train both models."""
    print("\n" + "=" * 60)
    print("V-Pulse Model Training")
    print("=" * 60 + "\n")
    
    # Train Supply Model (Crop Advisor)
    crop_model = train_crop_advisor()
    
    # Train Demand Model (Demand Radar)
    demand_model = train_demand_radar()
    
    # Train Crop Suitability Model
    suitability_model = train_crop_suitability()
    
    # Train Enhanced Vegan Demand Forecast Model
    vegan_demand_model = train_vegan_demand_forecast()
    
    print("\n" + "=" * 60)
    print("✓ All models trained and saved successfully!")
    print("=" * 60)
    print("\nModels saved in 'models/' directory:")
    print("  - crop_advisor.pkl (Crop Recommendation)")
    print("  - demand_radar.pkl (Basic Demand Forecasting)")
    print("  - crop_suitability.pkl (Crop Suitability Scoring)")
    print("  - vegan_demand_forecast.pkl (Enhanced Demand Forecasting)")

if __name__ == "__main__":
    main()

