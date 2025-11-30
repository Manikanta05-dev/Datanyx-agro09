# 🔧 VOIS Troubleshooting Guide

## Quick Fixes for Common Issues

---

## 🚨 CRITICAL ISSUES (Must Fix Before Demo)

### Issue 1: Backend Won't Start

#### Symptom:
```
Error: Address already in use
```

#### Solution:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Then restart
cd v_pulse_app
python backend/app.py
```

#### Alternative:
Change port in `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

---

### Issue 2: Frontend Can't Connect to Backend

#### Symptom:
Dashboard shows: "❌ Backend API is Offline"

#### Solution 1: Check Backend is Running
```bash
# Test backend directly
curl http://localhost:5000/

# Should return: "VOIS (V-Pulse) API is Online"
```

#### Solution 2: Check Firewall
```bash
# Windows: Allow Python through firewall
# Settings → Windows Security → Firewall → Allow an app
```

#### Solution 3: Update API URL
In `frontend/dashboard.py`, verify:
```python
API_URL = "http://localhost:5000"
```

---

### Issue 3: Models Not Found

#### Symptom:
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/crop_advisor.pkl'
```

#### Solution:
```bash
# Retrain all models
cd v_pulse_app
python train_models.py

# Verify models exist
ls models/
# Should show: crop_advisor.pkl, demand_radar.pkl, crop_suitability.pkl, vegan_demand_forecast.pkl
```

---

### Issue 4: Import Errors

#### Symptom:
```
ModuleNotFoundError: No module named 'flask'
```

#### Solution:
```bash
# Reinstall dependencies
cd v_pulse_app
pip install -r requirements.txt --force-reinstall

# If still fails, upgrade pip
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚠️ MODERATE ISSUES (Can Work Around)

### Issue 5: Streamlit Port Already in Use

#### Symptom:
```
Error: Port 8501 is already in use
```

#### Solution:
```bash
# Use different port
streamlit run frontend/dashboard.py --server.port 8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

### Issue 6: Slow Model Loading

#### Symptom:
Backend takes 30+ seconds to start

#### Solution:
This is normal for first load. Models are cached after first load.

To speed up:
```python
# In backend/app.py, add lazy loading
@app.before_first_request
def load_models_lazy():
    global crop_advisor_model, demand_radar_model
    # Load models here
```

---

### Issue 7: CORS Errors in Browser Console

#### Symptom:
```
Access to XMLHttpRequest blocked by CORS policy
```

#### Solution:
In `backend/app.py`, verify CORS is enabled:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This should be present
```

If still fails:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

---

### Issue 8: Predictions Return NaN or Infinity

#### Symptom:
API returns: `{"predicted_consumption": NaN}`

#### Solution:
Check input data ranges:
```python
# In backend/app.py, add validation
def validate_input(data):
    if data['price'] < 0 or data['price'] > 10000:
        raise ValueError("Price out of range")
    # Add more validations
```

---

## 🔍 DEBUGGING ISSUES

### Issue 9: Model Accuracy Too Low

#### Symptom:
Model R² score < 0.5

#### Solution:
1. Check data quality:
```python
import pandas as pd
df = pd.read_csv('data/vegan_consumption.csv')
print(df.describe())
print(df.isnull().sum())
```

2. Increase model complexity:
```python
model = RandomForestRegressor(
    n_estimators=200,  # Increase from 100
    max_depth=15,      # Increase from 10
    min_samples_split=3  # Decrease from 5
)
```

3. Add more features:
```python
# Add interaction features
df['price_genz_interaction'] = df['price'] * df['genz_ratio']
```

---

### Issue 10: API Response Too Slow

#### Symptom:
API takes > 5 seconds to respond

#### Solution:
1. Add caching:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def predict_cached(region, product, price):
    # Your prediction logic
    pass
```

2. Reduce model size:
```python
model = RandomForestRegressor(
    n_estimators=50,  # Reduce from 100
    max_depth=8       # Reduce from 10
)
```

3. Use model compression:
```python
import pickle
import gzip

# Save compressed
with gzip.open('models/model.pkl.gz', 'wb') as f:
    pickle.dump(model, f)

# Load compressed
with gzip.open('models/model.pkl.gz', 'rb') as f:
    model = pickle.load(f)
```

---

### Issue 11: Dashboard Looks Broken

#### Symptom:
Dashboard layout is messed up

#### Solution:
1. Clear Streamlit cache:
```bash
streamlit cache clear
```

2. Restart Streamlit:
```bash
# Ctrl+C to stop
streamlit run frontend/dashboard.py
```

3. Check browser zoom (should be 100-125%)

4. Try different browser (Chrome recommended)

---

### Issue 12: Data Files Not Found

#### Symptom:
```
FileNotFoundError: data/vegan_consumption.csv
```

#### Solution:
1. Check current directory:
```bash
pwd  # Should be in v_pulse_app/
ls data/  # Should show CSV files
```

2. If files missing, regenerate:
```bash
cd data
python generate_data.py
```

3. Check file paths in code:
```python
# Use absolute paths
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'vegan_consumption.csv')
```

---

## 🎯 DEMO-SPECIFIC ISSUES

### Issue 13: Demo Freezes During Presentation

#### Symptom:
Dashboard becomes unresponsive

#### Solution:
1. **Don't panic!** Judges understand technical issues

2. Refresh browser (F5)

3. If still frozen, restart Streamlit:
```bash
# Ctrl+C in terminal
streamlit run frontend/dashboard.py
```

4. While restarting, explain:
"This is a demo environment. Let me show you the architecture while it restarts..."

5. Show screenshots as backup

---

### Issue 14: Wrong Predictions During Demo

#### Symptom:
Predictions don't make sense (e.g., negative consumption)

#### Solution:
1. Check input values - might be out of range

2. Add validation in frontend:
```python
if price < 0:
    st.error("Price cannot be negative")
    return
```

3. Explain to judges:
"This is a synthetic dataset. With real data, we'd add more validation..."

---

### Issue 15: Internet Connection Lost

#### Symptom:
Can't access external resources

#### Solution:
1. **Good news:** VOIS runs entirely locally!

2. Backend and frontend don't need internet

3. Only issue: Can't show deployment or cloud features

4. Focus on local demo and explain:
"The system runs entirely offline, which is great for data privacy..."

---

## 💻 PLATFORM-SPECIFIC ISSUES

### Windows Issues

#### Issue 16: Python Not Found
```bash
# Add Python to PATH
# Settings → System → About → Advanced system settings → Environment Variables
# Add: C:\Python39\ and C:\Python39\Scripts\
```

#### Issue 17: Permission Denied
```bash
# Run as Administrator
# Right-click Command Prompt → Run as administrator
```

#### Issue 18: Long Path Names
```bash
# Enable long paths
# Run as admin:
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```

---

### Mac/Linux Issues

#### Issue 19: Permission Denied on Port 5000
```bash
# Use port > 1024
python backend/app.py --port 5001

# Or use sudo (not recommended)
sudo python backend/app.py
```

#### Issue 20: Python Version Mismatch
```bash
# Use python3 explicitly
python3 backend/app.py
python3 -m pip install -r requirements.txt
```

---

## 🔬 ADVANCED DEBUGGING

### Enable Debug Mode

#### Backend:
```python
# In backend/app.py
app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Frontend:
```bash
streamlit run frontend/dashboard.py --logger.level=debug
```

### Check Logs

#### Backend Logs:
```bash
# Redirect to file
python backend/app.py > backend.log 2>&1

# View logs
tail -f backend.log
```

#### Frontend Logs:
```bash
# Streamlit logs are in terminal
# Or check: ~/.streamlit/logs/
```

### Test API Manually

```bash
# Health check
curl http://localhost:5000/

# Test demand forecast
curl -X POST http://localhost:5000/forecast_vegan_demand \
  -H "Content-Type: application/json" \
  -d '{"region":"Hyderabad","product":"Oat Milk","price":200,"genz_ratio":0.5,"google_trends_score":70,"month":6,"quarter":2}'

# Test suitability
curl -X POST http://localhost:5000/predict_suitability \
  -H "Content-Type: application/json" \
  -d '{"district":"Anantapur","crop":"Oats","soil_ph":7.0,"soil_type":"Loamy","rainfall":600,"temperature":25,"irrigation":1,"distance_to_city":50}'
```

---

## 📊 PERFORMANCE ISSUES

### Issue 21: High Memory Usage

#### Solution:
```python
# Reduce model size
model = RandomForestRegressor(
    n_estimators=50,
    max_depth=8,
    max_features='sqrt'
)

# Clear unused variables
import gc
gc.collect()
```

### Issue 22: High CPU Usage

#### Solution:
```python
# Limit parallel jobs
model = RandomForestRegressor(
    n_jobs=2  # Instead of -1 (all cores)
)
```

---

## 🆘 EMERGENCY CONTACTS

### If All Else Fails:

1. **Stay Calm** - Technical issues happen

2. **Have Backup Plan**:
   - Screenshots of working system
   - Pre-recorded demo video
   - Architecture diagrams
   - Code walkthrough

3. **Explain to Judges**:
   "This is a demo environment. The code is production-ready and works in our development environment. Let me show you the architecture and code instead..."

4. **Focus on Value**:
   - Problem you're solving
   - Your approach and innovation
   - Business impact
   - Technical architecture

5. **Show Code**:
   - Open `backend/app.py` and explain endpoints
   - Open `train_models.py` and explain ML pipeline
   - Show data files and explain datasets

---

## ✅ PRE-DEMO TESTING CHECKLIST

Run this 30 minutes before demo:

```bash
# 1. Test backend
curl http://localhost:5000/
# Should return: "VOIS (V-Pulse) API is Online"

# 2. Test demand forecast
curl -X POST http://localhost:5000/forecast_vegan_demand \
  -H "Content-Type: application/json" \
  -d '{"region":"Hyderabad","product":"Oat Milk","price":200,"genz_ratio":0.5,"google_trends_score":70,"month":6,"quarter":2}'
# Should return JSON with predicted_consumption

# 3. Test suitability
curl -X POST http://localhost:5000/predict_suitability \
  -H "Content-Type: application/json" \
  -d '{"district":"Anantapur","crop":"Oats","soil_ph":7.0,"soil_type":"Loamy","rainfall":600,"temperature":25,"irrigation":1,"distance_to_city":50}'
# Should return JSON with suitability_score

# 4. Test frontend
# Open http://localhost:8501
# Check sidebar shows: "✅ Backend API is Online"

# 5. Test each dashboard tab
# Manufacturer → Demand Forecasting → Click "Forecast Demand"
# Farmer → Crop Suitability → Click "Analyze Suitability"
# Manufacturer → Supply Chain Optimizer → Click "Optimize Supply Chain"
```

If all tests pass: **You're ready! 🎉**

If any test fails: **Check this guide for solutions**

---

## 📞 QUICK REFERENCE

### Restart Everything:
```bash
# Stop all (Ctrl+C in both terminals)

# Terminal 1: Backend
cd v_pulse_app
python backend/app.py

# Terminal 2: Frontend
cd v_pulse_app
streamlit run frontend/dashboard.py
```

### Retrain Models:
```bash
cd v_pulse_app
python train_models.py
```

### Reinstall Dependencies:
```bash
cd v_pulse_app
pip install -r requirements.txt --force-reinstall
```

### Check Everything:
```bash
# Backend running?
curl http://localhost:5000/

# Frontend running?
# Open http://localhost:8501

# Models exist?
ls models/

# Data exists?
ls data/
```

---

**Remember: You've built something amazing. Technical issues are temporary. Your solution and approach are what matter most! 💪🌱🏆**
