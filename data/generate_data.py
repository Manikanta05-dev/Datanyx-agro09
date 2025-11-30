"""
Synthetic Data Generation Script for V-Pulse / VOIS
Generates all required datasets for Vegan Orbital Intelligence System
"""

import numpy as np
import pandas as pd
import os

def generate_crop_data(n_samples=1000):
    """
    Generate synthetic crop data with agricultural features.
    
    Columns: N, P, K, temperature, humidity, ph, rainfall, label
    Labels: 'rice', 'maize', 'chickpea', 'kidneybeans', 'mungbean'
    """
    np.random.seed(42)
    
    labels = ['rice', 'maize', 'chickpea', 'kidneybeans', 'mungbean']
    data = []
    
    # Define realistic ranges for each crop type
    crop_ranges = {
        'rice': {
            'N': (80, 120), 'P': (40, 60), 'K': (30, 50),
            'temperature': (20, 30), 'humidity': (80, 100),
            'ph': (5.5, 7.0), 'rainfall': (150, 300)
        },
        'maize': {
            'N': (50, 100), 'P': (30, 50), 'K': (20, 40),
            'temperature': (18, 27), 'humidity': (60, 80),
            'ph': (6.0, 7.5), 'rainfall': (50, 150)
        },
        'chickpea': {
            'N': (20, 50), 'P': (20, 40), 'K': (20, 40),
            'temperature': (15, 25), 'humidity': (50, 70),
            'ph': (6.0, 8.0), 'rainfall': (30, 100)
        },
        'kidneybeans': {
            'N': (20, 60), 'P': (20, 50), 'K': (20, 50),
            'temperature': (20, 30), 'humidity': (50, 80),
            'ph': (6.0, 7.5), 'rainfall': (40, 120)
        },
        'mungbean': {
            'N': (20, 50), 'P': (20, 40), 'K': (20, 40),
            'temperature': (25, 35), 'humidity': (60, 85),
            'ph': (6.5, 8.0), 'rainfall': (50, 150)
        }
    }
    
    # Generate samples for each crop type
    samples_per_crop = n_samples // len(labels)
    remainder = n_samples % len(labels)
    
    for idx, label in enumerate(labels):
        n_crop_samples = samples_per_crop + (1 if idx < remainder else 0)
        ranges = crop_ranges[label]
        
        for _ in range(n_crop_samples):
            row = {
                'N': np.random.uniform(*ranges['N']),
                'P': np.random.uniform(*ranges['P']),
                'K': np.random.uniform(*ranges['K']),
                'temperature': np.random.uniform(*ranges['temperature']),
                'humidity': np.random.uniform(*ranges['humidity']),
                'ph': np.random.uniform(*ranges['ph']),
                'rainfall': np.random.uniform(*ranges['rainfall']),
                'label': label
            }
            data.append(row)
    
    # Shuffle the data
    np.random.shuffle(data)
    
    df = pd.DataFrame(data)
    return df

def generate_demand_data(n_samples=1000):
    """
    Generate synthetic food order demand data.
    
    Columns: base_price, checkout_price, center_id, meal_id, num_orders
    """
    np.random.seed(42)
    
    # Generate realistic food order data
    n_centers = 20  # Number of different centers
    n_meals = 50    # Number of different meal types
    
    data = []
    
    for _ in range(n_samples):
        center_id = np.random.randint(1, n_centers + 1)
        meal_id = np.random.randint(1, n_meals + 1)
        
        # Base price between $5 and $25
        base_price = np.random.uniform(5.0, 25.0)
        
        # Checkout price is base_price plus some markup (0-20%)
        markup = np.random.uniform(0, 0.20)
        checkout_price = base_price * (1 + markup)
        
        # Number of orders follows a Poisson-like distribution
        # More realistic: some meals are more popular
        num_orders = np.random.poisson(lam=15) + 1  # At least 1 order
        
        row = {
            'base_price': round(base_price, 2),
            'checkout_price': round(checkout_price, 2),
            'center_id': center_id,
            'meal_id': meal_id,
            'num_orders': num_orders
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

def generate_vegan_consumption_data(n_samples=1000):
    """
    Generate vegan consumption data with time-series patterns.
    
    Columns: date, region, product, consumption, price, genz_ratio, google_trends_score
    """
    np.random.seed(42)
    
    regions = ['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai', 'Pune', 'Kolkata']
    # Exact products from problem statement
    products = ['Vegan Meat', 'Vegan Paneer', 'Vegan Milk', 'Oat Milk', 'Tofu', 
                'Plant-Based Protein', 'Soy Products', 'Chickpea Flour', 'Almond Milk', 
                'Coconut Milk', 'Quinoa', 'Tempeh', 'Vegan Cheese']
    
    data = []
    base_date = pd.Timestamp('2023-01-01')
    
    for i in range(n_samples):
        # Generate date with some seasonality
        days_offset = i % 365
        date = base_date + pd.Timedelta(days=days_offset)
        
        region = np.random.choice(regions)
        product = np.random.choice(products)
        
        # Base consumption with seasonality
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * days_offset / 365)
        base_consumption = np.random.uniform(100, 1000)
        consumption = int(base_consumption * seasonal_factor)
        
        # Price with some correlation to consumption
        base_price = np.random.uniform(50, 500)
        price = round(base_price, 2)
        
        # GenZ ratio (0-1) - higher for trendy products
        trendy_products = ['Oat Milk', 'Vegan Meat', 'Almond Milk']
        if product in trendy_products:
            genz_ratio = np.random.uniform(0.4, 0.8)
        else:
            genz_ratio = np.random.uniform(0.1, 0.5)
        
        # Google Trends score (0-100)
        google_trends = np.random.uniform(20, 100)
        
        row = {
            'date': date.strftime('%Y-%m-%d'),
            'region': region,
            'product': product,
            'consumption': consumption,
            'price': price,
            'genz_ratio': round(genz_ratio, 3),
            'google_trends_score': round(google_trends, 1)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

def generate_crop_suitability_data(n_samples=1000):
    """
    Generate crop suitability data per district.
    
    Columns: district, crop, soil_ph, soil_type, rainfall, temperature, irrigation, 
             yield_per_acre, distance_to_city, suitability_score
    """
    np.random.seed(42)
    
    districts = ['Anantapur', 'Kurnool', 'Hindupur', 'Mahabubnagar', 'Nalgonda', 
                 'Warangal', 'Karimnagar', 'Adilabad', 'Nizamabad', 'Medak']
    # Exact crops from problem statement
    crops = ['Soy', 'Oats', 'Chickpea', 'Pea Protein', 'Millets', 'Quinoa', 
             'Lentils', 'Mungbean', 'Kidneybeans', 'Blackbeans']
    soil_types = ['Loamy', 'Sandy', 'Clay', 'Sandy Loam', 'Clay Loam']
    
    data = []
    
    for _ in range(n_samples):
        district = np.random.choice(districts)
        crop = np.random.choice(crops)
        soil_type = np.random.choice(soil_types)
        
        # Realistic ranges
        soil_ph = np.random.uniform(5.5, 8.5)
        rainfall = np.random.uniform(300, 1200)  # mm
        temperature = np.random.uniform(15, 35)  # Celsius
        irrigation = np.random.choice([0, 1])  # 0 = rainfed, 1 = irrigated
        yield_per_acre = np.random.uniform(500, 3000)  # kg
        distance_to_city = np.random.uniform(10, 200)  # km
        
        # Calculate suitability score (0-1) based on multiple factors
        ph_score = 1 - abs(soil_ph - 7.0) / 3.5  # Optimal around 7
        rainfall_score = min(rainfall / 800, 1.0)  # Optimal around 800mm
        temp_score = 1 - abs(temperature - 25) / 20  # Optimal around 25°C
        irrigation_bonus = 0.1 if irrigation == 1 else 0
        distance_penalty = max(0, 1 - distance_to_city / 200)
        
        suitability_score = (ph_score * 0.2 + rainfall_score * 0.3 + 
                            temp_score * 0.2 + irrigation_bonus + 
                            distance_penalty * 0.3)
        suitability_score = max(0, min(1, suitability_score))  # Clamp to [0, 1]
        
        row = {
            'district': district,
            'crop': crop,
            'soil_ph': round(soil_ph, 2),
            'soil_type': soil_type,
            'rainfall': round(rainfall, 1),
            'temperature': round(temperature, 1),
            'irrigation': irrigation,
            'yield_per_acre': round(yield_per_acre, 1),
            'distance_to_city': round(distance_to_city, 1),
            'suitability_score': round(suitability_score, 3)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

def generate_logistics_supply_data(n_samples=1000):
    """
    Generate logistics and supply chain data.
    
    Columns: source_district, destination_city, crop, transport_cost, distance, 
             processing_capacity, storage_cost, supply_quantity
    """
    np.random.seed(42)
    
    source_districts = ['Anantapur', 'Kurnool', 'Hindupur', 'Mahabubnagar', 'Nalgonda']
    destination_cities = ['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai']
    crops = ['Oats', 'Chickpea', 'Soy', 'Quinoa', 'Lentils']
    
    data = []
    
    for _ in range(n_samples):
        source = np.random.choice(source_districts)
        destination = np.random.choice(destination_cities)
        crop = np.random.choice(crops)
        
        # Distance between source and destination (km)
        base_distance = np.random.uniform(100, 800)
        distance = round(base_distance, 1)
        
        # Transport cost (per ton per km)
        transport_cost_per_km = np.random.uniform(0.5, 2.0)
        transport_cost = round(transport_cost_per_km * distance, 2)
        
        # Processing capacity (tons per month)
        processing_capacity = np.random.uniform(100, 5000)
        
        # Storage cost (per ton per month)
        storage_cost = np.random.uniform(10, 100)
        
        # Supply quantity available (tons)
        supply_quantity = np.random.uniform(50, 2000)
        
        row = {
            'source_district': source,
            'destination_city': destination,
            'crop': crop,
            'transport_cost': transport_cost,
            'distance': distance,
            'processing_capacity': round(processing_capacity, 1),
            'storage_cost': round(storage_cost, 2),
            'supply_quantity': round(supply_quantity, 1)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

def main():
    """Generate and save CSV files."""
    # Ensure data directory exists
    data_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(data_dir, exist_ok=True)
    
    print("Generating crop_data.csv...")
    crop_df = generate_crop_data(1000)
    crop_path = os.path.join(data_dir, 'crop_data.csv')
    crop_df.to_csv(crop_path, index=False)
    print(f"✓ Generated {len(crop_df)} rows in {crop_path}")
    print(f"  Columns: {list(crop_df.columns)}")
    print(f"  Labels: {crop_df['label'].unique()}")
    
    print("\nGenerating demand_data.csv...")
    demand_df = generate_demand_data(1000)
    demand_path = os.path.join(data_dir, 'demand_data.csv')
    demand_df.to_csv(demand_path, index=False)
    print(f"✓ Generated {len(demand_df)} rows in {demand_path}")
    print(f"  Columns: {list(demand_df.columns)}")
    print(f"  Price range: ${demand_df['base_price'].min():.2f} - ${demand_df['base_price'].max():.2f}")
    print(f"  Total orders: {demand_df['num_orders'].sum()}")
    
    print("\nGenerating vegan_consumption.csv...")
    vegan_df = generate_vegan_consumption_data(1000)
    vegan_path = os.path.join(data_dir, 'vegan_consumption.csv')
    vegan_df.to_csv(vegan_path, index=False)
    print(f"✓ Generated {len(vegan_df)} rows in {vegan_path}")
    print(f"  Columns: {list(vegan_df.columns)}")
    print(f"  Regions: {vegan_df['region'].nunique()}")
    print(f"  Products: {vegan_df['product'].nunique()}")
    
    print("\nGenerating crop_suitability.csv...")
    suitability_df = generate_crop_suitability_data(1000)
    suitability_path = os.path.join(data_dir, 'crop_suitability.csv')
    suitability_df.to_csv(suitability_path, index=False)
    print(f"✓ Generated {len(suitability_df)} rows in {suitability_path}")
    print(f"  Columns: {list(suitability_df.columns)}")
    print(f"  Districts: {suitability_df['district'].nunique()}")
    print(f"  Crops: {suitability_df['crop'].nunique()}")
    print(f"  Suitability score range: {suitability_df['suitability_score'].min():.3f} - {suitability_df['suitability_score'].max():.3f}")
    
    print("\nGenerating logistics_supply.csv...")
    logistics_df = generate_logistics_supply_data(1000)
    logistics_path = os.path.join(data_dir, 'logistics_supply.csv')
    logistics_df.to_csv(logistics_path, index=False)
    print(f"✓ Generated {len(logistics_df)} rows in {logistics_path}")
    print(f"  Columns: {list(logistics_df.columns)}")
    print(f"  Source districts: {logistics_df['source_district'].nunique()}")
    print(f"  Destination cities: {logistics_df['destination_city'].nunique()}")
    
    print("\n✓ Data generation complete!")

if __name__ == "__main__":
    main()

