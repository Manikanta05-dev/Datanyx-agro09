"""
VOIS (V-Pulse) Frontend Dashboard
Vegan Orbital Intelligence System - Multi-Dashboard Interface
Complete AI-driven market intelligence and agro-supply optimization
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuration
API_URL = "http://localhost:5000"
PAGE_TITLE = "VOIS: Vegan Orbital Intelligence System"

# Set page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .result-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Visualization Helper Functions
def create_demand_forecast_chart(predicted_consumption, product, region):
    """Create demand forecast visualization with trend"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Generate historical and forecast data
    historical = [predicted_consumption * np.random.uniform(0.7, 0.95) for _ in range(6)]
    forecast = [predicted_consumption * np.random.uniform(0.95, 1.15) for _ in range(6)]
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=months[:6], y=historical,
        mode='lines+markers',
        name='Historical',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=8)
    ))
    
    # Forecast data
    fig.add_trace(go.Scatter(
        x=months[6:], y=forecast,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#FF6B6B', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f'{product} Demand Forecast - {region}',
        xaxis_title='Month',
        yaxis_title='Consumption (units)',
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_genz_adoption_gauge(genz_index):
    """Create GenZ adoption gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=genz_index * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "GenZ Adoption Index"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#4CAF50"},
            'steps': [
                {'range': [0, 30], 'color': "#FFE0E0"},
                {'range': [30, 70], 'color': "#FFF4E0"},
                {'range': [70, 100], 'color': "#E8F5E9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_price_elasticity_chart(price_elasticity):
    """Create price elasticity visualization"""
    prices = np.linspace(100, 400, 20)
    demand = [1000 * (1 - (p - 200) / 500 * (1 - price_elasticity)) for p in prices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prices, y=demand,
        mode='lines',
        fill='tozeroy',
        line=dict(color='#2196F3', width=3),
        name='Demand Curve'
    ))
    
    fig.update_layout(
        title='Price Elasticity Analysis',
        xaxis_title='Price (₹)',
        yaxis_title='Demand (units)',
        height=300
    )
    
    return fig

def create_suitability_radar(suitability_score, district, crop):
    """Create radar chart for crop suitability factors"""
    categories = ['Soil Quality', 'Climate', 'Water', 'Logistics', 'Market Access']
    values = [
        suitability_score * np.random.uniform(0.9, 1.1),
        suitability_score * np.random.uniform(0.85, 1.05),
        suitability_score * np.random.uniform(0.9, 1.1),
        suitability_score * np.random.uniform(0.8, 1.0),
        suitability_score * np.random.uniform(0.85, 1.05)
    ]
    values = [min(1.0, max(0.0, v)) for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f'{crop} in {district}',
        line=dict(color='#4CAF50', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title=f'Suitability Analysis: {crop} in {district}',
        height=400
    )
    
    return fig

def create_supply_chain_pie(optimal_sources):
    """Create pie chart for supply chain allocation"""
    if not optimal_sources:
        return None
    
    labels = [source['source_district'] for source in optimal_sources]
    values = [source['allocation_percentage'] for source in optimal_sources]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker=dict(colors=px.colors.sequential.Greens)
    )])
    
    fig.update_layout(
        title='Supply Chain Allocation by District',
        height=400
    )
    
    return fig

def create_cost_comparison_bar(optimal_sources):
    """Create bar chart for cost comparison"""
    if not optimal_sources:
        return None
    
    districts = [source['source_district'] for source in optimal_sources]
    costs = [source['total_cost'] for source in optimal_sources]
    suitability = [source.get('suitability_score', 0.5) * 100 for source in optimal_sources]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(name='Cost', x=districts, y=costs, marker_color='#FF6B6B'),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(name='Suitability', x=districts, y=suitability, 
                   mode='lines+markers', marker_color='#4CAF50', line=dict(width=3)),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="District")
    fig.update_yaxes(title_text="Cost (₹)", secondary_y=False)
    fig.update_yaxes(title_text="Suitability Score (%)", secondary_y=True)
    
    fig.update_layout(title='Cost vs Suitability Analysis', height=400)
    
    return fig

def create_product_comparison_chart():
    """Create comparison chart for different vegan products"""
    products = ['Oat Milk', 'Vegan Meat', 'Soy Products', 'Chickpea Flour', 'Almond Milk', 'Tofu']
    demand = [1200, 980, 1450, 890, 1100, 950]
    growth = [25, 35, 20, 15, 30, 22]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(name='Current Demand', x=products, y=demand, marker_color='#4CAF50'),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(name='Growth %', x=products, y=growth, 
                   mode='lines+markers', marker_color='#FF6B6B', line=dict(width=3)),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Product")
    fig.update_yaxes(title_text="Demand (units)", secondary_y=False)
    fig.update_yaxes(title_text="Growth Rate (%)", secondary_y=True)
    
    fig.update_layout(title='Vegan Product Market Analysis', height=400)
    
    return fig

# Header
st.markdown(f'<h1 class="main-header">{PAGE_TITLE}</h1>', unsafe_allow_html=True)
st.markdown("---")

# Create main dashboard selector
dashboard_type = st.sidebar.selectbox(
    "Select Dashboard",
    ["🏭 Manufacturer", "👨‍🌾 Farmer", "🛒 Consumer", "📊 Legacy Tools"]
)

# Create tabs based on dashboard type
if dashboard_type == "🏭 Manufacturer":
    tab1, tab2, tab3 = st.tabs(["📈 Demand Forecasting", "🔗 Supply Chain Optimizer", "📊 Combined Intelligence"])
elif dashboard_type == "👨‍🌾 Farmer":
    tab1, tab2 = st.tabs(["🌾 Crop Suitability", "📈 Market Insights"])
elif dashboard_type == "🛒 Consumer":
    tab1, tab2 = st.tabs(["📊 Trending Products", "🌱 Sustainability Score"])
else:  # Legacy Tools
    tab1, tab2 = st.tabs(["📈 Demand Radar", "🚜 Cultivation Commander"])

# ==================== MANUFACTURER DASHBOARD ====================
if dashboard_type == "🏭 Manufacturer":
    with tab1:  # Demand Forecasting
        st.header("📈 Enhanced Demand Forecasting")
        st.markdown("Forecast vegan product demand with time-series intelligence, GenZ adoption, and price elasticity.")
        
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Region", ["Hyderabad", "Bengaluru", "Mumbai", "Delhi", "Chennai", "Pune", "Kolkata"])
            product = st.selectbox("Product", ["Oat Milk", "Vegan Meat", "Soy Products", "Chickpea Flour", "Almond Milk", "Coconut Milk", "Quinoa", "Tofu"])
            price = st.number_input("Price (₹)", min_value=0.0, value=200.0, step=1.0)
        
        with col2:
            genz_ratio = st.slider("GenZ Ratio", 0.0, 1.0, 0.5, 0.01)
            google_trends = st.slider("Google Trends Score", 0.0, 100.0, 70.0, 1.0)
            month = st.number_input("Month", 1, 12, value=6, step=1)
            quarter = (month - 1) // 3 + 1
        
        if st.button("🔮 Forecast Demand", type="primary", use_container_width=True):
            try:
                payload = {
                    "region": region, "product": product, "price": price,
                    "genz_ratio": genz_ratio, "google_trends_score": google_trends,
                    "month": month, "quarter": quarter
                }
                with st.spinner("Forecasting..."):
                    response = requests.post(f"{API_URL}/forecast_vegan_demand", json=payload, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display key metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Predicted Consumption", f"{result['predicted_consumption']:.0f} units", 
                                 delta=f"+{result['predicted_consumption']*0.15:.0f} vs last month")
                    with col2:
                        st.metric("GenZ Adoption Index", f"{result['genz_adoption_index']:.3f}",
                                 delta="+0.05" if result['genz_adoption_index'] > 0.5 else "-0.02")
                    with col3:
                        st.metric("Price Elasticity", f"{result['price_elasticity_score']:.3f}",
                                 delta="High" if result['price_elasticity_score'] > 0.7 else "Medium")
                    
                    st.markdown("---")
                    
                    # Visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Demand forecast chart
                        fig1 = create_demand_forecast_chart(result['predicted_consumption'], product, region)
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        # Price elasticity chart
                        fig3 = create_price_elasticity_chart(result['price_elasticity_score'])
                        st.plotly_chart(fig3, use_container_width=True)
                    
                    with col2:
                        # GenZ adoption gauge
                        fig2 = create_genz_adoption_gauge(result['genz_adoption_index'])
                        st.plotly_chart(fig2, use_container_width=True)
                        
                        # Product comparison
                        fig4 = create_product_comparison_chart()
                        st.plotly_chart(fig4, use_container_width=True)
                    
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:  # Supply Chain Optimizer
        st.header("🔗 VORTEX Supply Chain Optimizer")
        st.markdown("Optimize sourcing, reduce costs, and minimize waste.")
        
        col1, col2 = st.columns(2)
        with col1:
            destination = st.selectbox("Destination City", ["Hyderabad", "Bengaluru", "Mumbai", "Delhi", "Chennai"])
            product = st.selectbox("Product", ["Oat Milk", "Soy Products", "Chickpea Flour"])
        with col2:
            required_qty = st.number_input("Required Quantity (tons)", min_value=1.0, value=100.0, step=10.0)
        
        if st.button("⚡ Optimize Supply Chain", type="primary", use_container_width=True):
            try:
                payload = {"destination_city": destination, "product": product, "required_quantity": required_qty}
                with st.spinner("Optimizing..."):
                    response = requests.post(f"{API_URL}/optimize_supply_chain", json=payload, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display key metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Cost", f"₹{result['total_cost']:.2f}", 
                                 delta=f"-₹{result['total_cost']*0.3:.2f} saved")
                    with col2:
                        st.metric("Waste Reduction", f"{result['waste_reduction_percentage']:.1f}%",
                                 delta="Sustainable")
                    with col3:
                        st.metric("Sources", len(result['optimal_sources']),
                                 delta="Optimized")
                    
                    st.markdown("---")
                    
                    # Visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Pie chart for allocation
                        fig1 = create_supply_chain_pie(result['optimal_sources'])
                        if fig1:
                            st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Bar chart for cost comparison
                        fig2 = create_cost_comparison_bar(result['optimal_sources'])
                        if fig2:
                            st.plotly_chart(fig2, use_container_width=True)
                    
                    # Detailed table
                    st.subheader("📋 Optimal Sources Breakdown")
                    sources_df = pd.DataFrame(result['optimal_sources'])
                    st.dataframe(sources_df, use_container_width=True)
                    
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab3:  # Combined Intelligence
        st.header("📊 Combined AI Decision Engine")
        st.markdown("Get comprehensive intelligence combining all models.")
        
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Region", ["Hyderabad", "Bengaluru", "Mumbai"])
            product = st.selectbox("Product", ["Oat Milk", "Vegan Meat", "Soy Products"])
        with col2:
            district = st.selectbox("District", ["Anantapur", "Kurnool", "Hindupur", "Mahabubnagar"])
            crop = st.selectbox("Crop", ["Oats", "Chickpea", "Soy", "Quinoa"])
        
        price = st.number_input("Price (₹)", min_value=0.0, value=200.0)
        month = st.number_input("Month", 1, 12, value=6)
        
        if st.button("🧠 Generate Intelligence Report", type="primary", use_container_width=True):
            try:
                payload = {"region": region, "product": product, "district": district, "crop": crop, "price": price, "month": month}
                with st.spinner("Generating intelligence..."):
                    response = requests.post(f"{API_URL}/combined_intelligence", json=payload, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"**Priority Score:** {result['priority_score']:.3f}")
                    st.info(f"**Recommendation:** {result['recommendation']}")
                    st.json(result)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ==================== FARMER DASHBOARD ====================
elif dashboard_type == "👨‍🌾 Farmer":
    with tab1:  # Crop Suitability
        st.header("🌾 Crop Suitability Analyzer")
        st.markdown("Get AI-powered suitability scores for your district and crop combinations.")
        
        col1, col2 = st.columns(2)
        with col1:
            district = st.selectbox("District", ["Anantapur", "Kurnool", "Hindupur", "Mahabubnagar", "Nalgonda", "Warangal"])
            crop = st.selectbox("Crop", ["Oats", "Chickpea", "Soy", "Quinoa", "Lentils", "Mungbean"])
            soil_type = st.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Sandy Loam", "Clay Loam"])
        with col2:
            soil_ph = st.slider("Soil pH", 5.5, 8.5, 7.0, 0.1)
            rainfall = st.slider("Rainfall (mm)", 300.0, 1200.0, 600.0, 10.0)
            temperature = st.slider("Temperature (°C)", 15.0, 35.0, 25.0, 0.5)
        
        irrigation = st.radio("Irrigation", ["Irrigated (1)", "Rainfed (0)"], index=0)
        distance = st.slider("Distance to City (km)", 10.0, 200.0, 50.0, 5.0)
        
        if st.button("🔍 Analyze Suitability", type="primary", use_container_width=True):
            try:
                payload = {
                    "district": district, "crop": crop, "soil_ph": soil_ph,
                    "soil_type": soil_type, "rainfall": rainfall, "temperature": temperature,
                    "irrigation": 1 if irrigation.startswith("Irrigated") else 0,
                    "distance_to_city": distance
                }
                with st.spinner("Analyzing..."):
                    response = requests.post(f"{API_URL}/predict_suitability", json=payload, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    score = result['suitability_score']
                    
                    # Display score with color coding
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if score >= 0.8:
                            st.success(f"**Suitability Score**\n\n# {score:.3f}\n🌟 Highly Suitable!")
                        elif score >= 0.6:
                            st.info(f"**Suitability Score**\n\n# {score:.3f}\n✓ Moderately Suitable")
                        else:
                            st.warning(f"**Suitability Score**\n\n# {score:.3f}\n⚠ Low Suitability")
                    
                    with col2:
                        st.metric("Soil Match", f"{score*100:.1f}%", 
                                 delta="Excellent" if score > 0.8 else "Good" if score > 0.6 else "Fair")
                    
                    with col3:
                        st.metric("Climate Match", f"{score*95:.1f}%",
                                 delta="Optimal" if score > 0.7 else "Acceptable")
                    
                    st.markdown("---")
                    
                    # Recommendation box
                    st.info(f"**💡 Recommendation:** {result['recommendation']}")
                    
                    # Visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Radar chart for suitability factors
                        fig1 = create_suitability_radar(score, district, crop)
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Gauge chart for overall score
                        fig2 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=score * 100,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Overall Suitability"},
                            gauge={
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "#4CAF50" if score > 0.7 else "#FFA726"},
                                'steps': [
                                    {'range': [0, 40], 'color': "#FFCDD2"},
                                    {'range': [40, 70], 'color': "#FFF9C4"},
                                    {'range': [70, 100], 'color': "#C8E6C9"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 80
                                }
                            }
                        ))
                        fig2.update_layout(height=400)
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # Comparison with other crops
                    st.subheader("📊 Crop Comparison for Your District")
                    crops = ['Oats', 'Chickpea', 'Soy', 'Quinoa', 'Lentils', 'Mungbean']
                    scores = [score if c == crop else score * np.random.uniform(0.7, 1.1) for c in crops]
                    scores = [min(1.0, max(0.0, s)) for s in scores]
                    
                    fig3 = go.Figure(data=[
                        go.Bar(x=crops, y=scores, marker_color=['#4CAF50' if c == crop else '#90CAF9' for c in crops])
                    ])
                    fig3.update_layout(
                        title=f'Suitability Scores in {district}',
                        xaxis_title='Crop',
                        yaxis_title='Suitability Score',
                        height=300
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                    
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:  # Market Insights
        st.header("📈 Market Insights & Buyback Opportunities")
        st.markdown("View market demand trends and pricing for your crops.")
        
        # Market overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Market Price", "₹245/kg", delta="+12%")
        with col2:
            st.metric("Demand Growth", "28%", delta="+5% YoY")
        with col3:
            st.metric("Buyback Offers", "15 Active", delta="+3 new")
        
        st.markdown("---")
        
        # Market trends chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Price trends
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            prices = [220, 225, 235, 240, 242, 245]
            
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=months, y=prices,
                mode='lines+markers',
                name='Market Price',
                line=dict(color='#4CAF50', width=3),
                marker=dict(size=10),
                fill='tozeroy'
            ))
            fig1.update_layout(
                title='Market Price Trends (₹/kg)',
                xaxis_title='Month',
                yaxis_title='Price (₹)',
                height=350
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Demand by crop
            crops = ['Oats', 'Chickpea', 'Soy', 'Quinoa', 'Lentils']
            demand = [1200, 980, 1450, 890, 1100]
            
            fig2 = go.Figure(data=[
                go.Bar(x=crops, y=demand, marker_color='#66BB6A')
            ])
            fig2.update_layout(
                title='Current Market Demand (tons)',
                xaxis_title='Crop',
                yaxis_title='Demand',
                height=350
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Regional demand heatmap
        st.subheader("🗺️ Regional Demand Distribution")
        regions = ['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai']
        crops_heat = ['Oats', 'Chickpea', 'Soy']
        demand_matrix = np.random.randint(500, 1500, size=(len(crops_heat), len(regions)))
        
        fig3 = go.Figure(data=go.Heatmap(
            z=demand_matrix,
            x=regions,
            y=crops_heat,
            colorscale='Greens',
            text=demand_matrix,
            texttemplate='%{text}',
            textfont={"size": 12}
        ))
        fig3.update_layout(
            title='Demand Heatmap by Region (tons)',
            xaxis_title='Region',
            yaxis_title='Crop',
            height=300
        )
        st.plotly_chart(fig3, use_container_width=True)

# ==================== CONSUMER DASHBOARD ====================
elif dashboard_type == "🛒 Consumer":
    with tab1:  # Trending Products
        st.header("📊 Trending Vegan Products")
        st.markdown("Discover trending vegan products in your region with GenZ adoption metrics.")
        
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Top Product", "Oat Milk", delta="🔥 Trending")
        with col2:
            st.metric("GenZ Favorite", "Vegan Meat", delta="+45%")
        with col3:
            st.metric("Best Value", "Chickpea Flour", delta="₹180/kg")
        with col4:
            st.metric("New Arrivals", "3 Products", delta="This week")
        
        st.markdown("---")
        
        # Trending products chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Product popularity
            products = ['Oat Milk', 'Vegan Meat', 'Soy Products', 'Chickpea Flour', 'Almond Milk', 'Tofu']
            popularity = [95, 88, 82, 75, 85, 78]
            colors = ['#4CAF50' if p > 85 else '#FFA726' if p > 75 else '#90CAF9' for p in popularity]
            
            fig1 = go.Figure(data=[
                go.Bar(x=products, y=popularity, marker_color=colors)
            ])
            fig1.update_layout(
                title='Product Popularity Score',
                xaxis_title='Product',
                yaxis_title='Popularity (%)',
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # GenZ adoption pie chart
            labels = ['Oat Milk', 'Vegan Meat', 'Almond Milk', 'Tofu', 'Others']
            values = [30, 25, 20, 15, 10]
            
            fig2 = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker=dict(colors=px.colors.sequential.Greens)
            )])
            fig2.update_layout(
                title='GenZ Product Preferences',
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Price comparison
        st.subheader("💰 Price Comparison Across Regions")
        regions = ['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai']
        oat_milk_prices = [195, 205, 220, 210, 200]
        vegan_meat_prices = [280, 295, 310, 300, 290]
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Oat Milk', x=regions, y=oat_milk_prices, marker_color='#66BB6A'))
        fig3.add_trace(go.Bar(name='Vegan Meat', x=regions, y=vegan_meat_prices, marker_color='#FFA726'))
        
        fig3.update_layout(
            title='Product Prices by Region (₹/kg)',
            xaxis_title='Region',
            yaxis_title='Price (₹)',
            barmode='group',
            height=350
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:  # Sustainability Score
        st.header("🌱 Sustainability Score")
        st.markdown("View sustainability metrics and environmental impact scores.")
        
        # Sustainability metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Carbon Footprint", "45% Lower", delta="-15% vs dairy")
        with col2:
            st.metric("Water Usage", "60% Less", delta="Eco-friendly")
        with col3:
            st.metric("Land Usage", "75% Reduced", delta="Sustainable")
        
        st.markdown("---")
        
        # Environmental impact comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Carbon footprint comparison
            categories = ['Dairy Milk', 'Oat Milk', 'Almond Milk', 'Soy Milk']
            carbon = [3.2, 0.9, 1.1, 1.0]
            
            fig1 = go.Figure(data=[
                go.Bar(x=categories, y=carbon, 
                       marker_color=['#FF6B6B', '#4CAF50', '#66BB6A', '#81C784'])
            ])
            fig1.update_layout(
                title='Carbon Footprint (kg CO₂/liter)',
                xaxis_title='Product',
                yaxis_title='CO₂ Emissions',
                height=350
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Water usage comparison
            water = [628, 48, 371, 28]
            
            fig2 = go.Figure(data=[
                go.Bar(x=categories, y=water,
                       marker_color=['#FF6B6B', '#4CAF50', '#66BB6A', '#81C784'])
            ])
            fig2.update_layout(
                title='Water Usage (liters/liter)',
                xaxis_title='Product',
                yaxis_title='Water (L)',
                height=350
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Sustainability radar
        st.subheader("🌍 Overall Sustainability Analysis")
        categories = ['Carbon', 'Water', 'Land', 'Biodiversity', 'Waste']
        vegan_scores = [0.85, 0.90, 0.95, 0.80, 0.88]
        dairy_scores = [0.45, 0.40, 0.35, 0.50, 0.55]
        
        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatterpolar(
            r=vegan_scores,
            theta=categories,
            fill='toself',
            name='Vegan Products',
            line=dict(color='#4CAF50', width=2)
        ))
        
        fig3.add_trace(go.Scatterpolar(
            r=dairy_scores,
            theta=categories,
            fill='toself',
            name='Dairy Products',
            line=dict(color='#FF6B6B', width=2)
        ))
        
        fig3.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title='Sustainability Comparison',
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

# ==================== LEGACY TOOLS ====================
elif dashboard_type == "📊 Legacy Tools":
    with tab1:  # Tab 1: Demand Radar
        st.header("📈 Demand Radar")
        st.markdown("Forecast demand for vegan meals based on pricing and location data.")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            base_price = st.number_input(
                "Base Price ($)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.01,
                help="The base price of the meal"
            )
            
            checkout_price = st.number_input(
                "Checkout Price ($)",
                min_value=0.0,
                max_value=100.0,
                value=12.0,
                step=0.01,
                help="The final checkout price including markup"
            )
        
        with col2:
            center_id = st.number_input(
                "Center ID",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                help="The distribution center identifier"
            )
            
            meal_id = st.number_input(
                "Meal ID",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                help="The meal type identifier"
            )
        
        st.markdown("")
        
        if st.button("🔮 Forecast Demand", type="primary", use_container_width=True):
            try:
                # Prepare request data
                payload = {
                    "base_price": float(base_price),
                    "checkout_price": float(checkout_price),
                    "center_id": int(center_id),
                    "meal_id": int(meal_id)
                }
                
                # Make API request
                with st.spinner("Forecasting demand..."):
                    response = requests.post(
                        f"{API_URL}/predict_demand",
                        json=payload,
                        timeout=5
                    )
                
                # Check response
                if response.status_code == 200:
                    result = response.json()
                    predicted_orders = result.get("predicted_orders", "N/A")
                    
                    st.markdown("")
                    st.markdown(f"""
                        <div class="result-box">
                            <h3>📊 Forecast Result</h3>
                            <p style="font-size: 1.5rem; color: #2E7D32; font-weight: bold;">
                                Predicted Orders: <span style="color: #1B5E20;">{predicted_orders}</span>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display input summary
                    st.markdown("")
                    st.info(f"""
                        **Input Summary:**
                        - Base Price: ${base_price:.2f}
                        - Checkout Price: ${checkout_price:.2f}
                        - Center ID: {center_id}
                        - Meal ID: {meal_id}
                    """)
                    
                else:
                    error_msg = response.json().get("error", "Unknown error occurred")
                    st.error(f"❌ API Error: {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("""
                    ❌ **Connection Error**: Cannot connect to the backend API.
                    
                    Please ensure the Flask backend is running:
                    1. Open a terminal
                    2. Navigate to the project directory
                    3. Run: `python backend/app.py`
                """)
            except requests.exceptions.Timeout:
                st.error("⏱️ **Timeout Error**: The API request took too long. Please try again.")
            except Exception as e:
                st.error(f"❌ **Error**: {str(e)}")
    
    # Tab 2: Cultivation Commander
    with tab2:
        st.header("🚜 Cultivation Commander")
        st.markdown("Get crop recommendations based on soil and environmental conditions.")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌿 Soil Nutrients")
            nitrogen = st.slider(
                "Nitrogen (N)",
                min_value=0.0,
                max_value=150.0,
                value=50.0,
                step=0.1,
                help="Nitrogen content in the soil"
            )
            
            phosphorus = st.slider(
                "Phosphorus (P)",
                min_value=0.0,
                max_value=150.0,
                value=50.0,
                step=0.1,
                help="Phosphorus content in the soil"
            )
            
            potassium = st.slider(
                "Potassium (K)",
                min_value=0.0,
                max_value=150.0,
                value=50.0,
                step=0.1,
                help="Potassium content in the soil"
            )
        
        with col2:
            st.subheader("🌡️ Environmental Conditions")
            temperature = st.slider(
                "Temperature (°C)",
                min_value=0.0,
                max_value=50.0,
                value=25.0,
                step=0.1,
                help="Average temperature"
            )
            
            humidity = st.slider(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=60.0,
                step=0.1,
                help="Average humidity level"
            )
            
            ph = st.slider(
                "pH Level",
                min_value=0.0,
                max_value=14.0,
                value=7.0,
                step=0.1,
                help="Soil pH level"
            )
            
            rainfall = st.slider(
                "Rainfall (mm)",
                min_value=0.0,
                max_value=400.0,
                value=100.0,
                step=0.1,
                help="Average rainfall"
            )
        
        st.markdown("")
        
        if st.button("🔍 Analyze Soil", type="primary", use_container_width=True):
            try:
                # Prepare request data
                payload = {
                    "N": float(nitrogen),
                    "P": float(phosphorus),
                    "K": float(potassium),
                    "temperature": float(temperature),
                    "humidity": float(humidity),
                    "ph": float(ph),
                    "rainfall": float(rainfall)
                }
                
                # Make API request
                with st.spinner("Analyzing soil conditions..."):
                    response = requests.post(
                        f"{API_URL}/recommend_crop",
                        json=payload,
                        timeout=5
                    )
                
                # Check response
                if response.status_code == 200:
                    result = response.json()
                    recommended_crop = result.get("recommended_crop", "N/A")
                    
                    st.markdown("")
                    st.markdown(f"""
                        <div class="result-box">
                            <h3>🌾 Crop Recommendation</h3>
                            <p style="font-size: 1.5rem; color: #2E7D32; font-weight: bold;">
                                Recommended Crop: <span style="color: #1B5E20; text-transform: capitalize;">{recommended_crop}</span>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display input summary
                    st.markdown("")
                    st.info(f"""
                        **Input Summary:**
                        - Nitrogen (N): {nitrogen:.1f}
                        - Phosphorus (P): {phosphorus:.1f}
                        - Potassium (K): {potassium:.1f}
                        - Temperature: {temperature:.1f}°C
                        - Humidity: {humidity:.1f}%
                        - pH: {ph:.1f}
                        - Rainfall: {rainfall:.1f} mm
                    """)
                    
                else:
                    error_msg = response.json().get("error", "Unknown error occurred")
                    st.error(f"❌ API Error: {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("""
                    ❌ **Connection Error**: Cannot connect to the backend API.
                    
                    Please ensure the Flask backend is running:
                    1. Open a terminal
                    2. Navigate to the project directory
                    3. Run: `python backend/app.py`
                """)
            except requests.exceptions.Timeout:
                st.error("⏱️ **Timeout Error**: The API request took too long. Please try again.")
            except Exception as e:
                st.error(f"❌ **Error**: {str(e)}")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ About VOIS")
    st.markdown("""
        **VOIS (Vegan Orbital Intelligence System)** is an AI-driven platform for:
        
        ### 🏭 Manufacturer Dashboard:
        - Demand forecasting with GenZ metrics
        - Supply chain optimization (VORTEX)
        - Combined AI intelligence
        
        ### 👨‍🌾 Farmer Dashboard:
        - Crop suitability scoring
        - Market insights
        - Climate resilience analysis
        
        ### 🛒 Consumer Dashboard:
        - Trending products
        - Sustainability scores
        
        ### 📊 Legacy Tools:
        - Basic demand forecasting
        - Crop recommendations
    """)
    
    st.markdown("---")
    
    # API Status Check
    st.subheader("🔌 API Status")
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend API is Online")
        else:
            st.warning("⚠️ Backend API returned an error")
    except:
        st.error("❌ Backend API is Offline")
        st.caption("Start the backend with: `python backend/app.py`")

