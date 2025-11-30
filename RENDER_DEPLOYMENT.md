# 🚀 Deploy VOIS to Render - Quick Guide

## Why Render?
- ✅ **FREE** tier available
- ✅ **Easiest** deployment (no CLI needed)
- ✅ **Auto-deploys** from GitHub
- ✅ **Free SSL** certificate
- ✅ Perfect for demos and hackathons

---

## 🎯 Deploy in 5 Minutes

### Step 1: Go to Render
1. Visit: https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with **GitHub** (easiest)

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: **Datanyx-agro09**
3. Click **"Connect"**

### Step 3: Configure Service

**Basic Settings:**
- **Name:** `vois-backend`
- **Region:** Oregon (US West) or closest to you
- **Branch:** `main`
- **Root Directory:** `v_pulse_app` (IMPORTANT!)
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  python backend/app.py
  ```

**Instance Type:**
- Select: **Free** (for testing/demo)
- Or: **Starter** ($7/month for better performance)

### Step 4: Add Environment Variables (Optional)
Click **"Advanced"** → **"Add Environment Variable"**

```
DEBUG = False
PYTHON_VERSION = 3.11.0
```

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. You'll get a URL like: `https://vois-backend.onrender.com`

---

## 🎨 Deploy Frontend (Streamlit)

### Option A: Same Service (Backend + Frontend)

Update **Start Command** to:
```bash
python backend/app.py & streamlit run frontend/dashboard.py --server.port=8501 --server.address=0.0.0.0
```

**Note:** This runs both on same service (uses more resources)

### Option B: Separate Service (Recommended)

1. Create another **New Web Service**
2. Same repository: **Datanyx-agro09**
3. Configure:
   - **Name:** `vois-frontend`
   - **Root Directory:** `v_pulse_app`
   - **Build Command:** `pip install streamlit plotly requests pandas numpy`
   - **Start Command:** `streamlit run frontend/dashboard.py --server.port=$PORT --server.address=0.0.0.0`

4. Add Environment Variable:
   ```
   API_URL = https://vois-backend.onrender.com
   ```

---

## 📋 Quick Configuration Summary

### Backend Service:
```yaml
Name: vois-backend
Root Directory: v_pulse_app
Build Command: pip install -r requirements.txt
Start Command: python backend/app.py
Port: Auto-detected
```

### Frontend Service (Optional):
```yaml
Name: vois-frontend
Root Directory: v_pulse_app
Build Command: pip install streamlit plotly requests pandas numpy
Start Command: streamlit run frontend/dashboard.py --server.port=$PORT --server.address=0.0.0.0
Port: Auto-detected
```

---

## 🔧 Using render.yaml (Automatic)

Your repo already has `render.yaml` configured!

1. Go to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Connect repository: **Datanyx-agro09**
4. Render will auto-detect `render.yaml`
5. Click **"Apply"**
6. Done! 🎉

---

## ✅ After Deployment

### Check Your Services:
1. **Backend:** `https://vois-backend.onrender.com`
2. Test API: `https://vois-backend.onrender.com/` (should return health check)

### Update Frontend API URL:
If you deployed frontend separately, update the API URL in your code or environment variables.

---

## 💰 Cost

### Free Tier:
- ✅ 750 hours/month free
- ✅ Spins down after 15 min of inactivity
- ✅ Cold start: ~30 seconds
- ✅ Perfect for demos!

### Paid Tier ($7/month):
- ✅ Always on (no spin down)
- ✅ Faster performance
- ✅ More resources

---

## 🐛 Troubleshooting

### Service won't start?
1. Check logs in Render dashboard
2. Verify `requirements.txt` is correct
3. Ensure `backend/app.py` uses `PORT` env variable

### Models not loading?
- Models are in the repo and will be deployed
- Check logs for any file path issues

### Port errors?
- Backend already configured to use `os.environ.get('PORT', 5000)`
- No changes needed!

---

## 🚀 Quick Deploy Commands

### If using Render CLI (optional):
```bash
# Install Render CLI
npm install -g @render/cli

# Login
render login

# Deploy
render deploy
```

---

## 📊 Deployment Checklist

- [ ] Sign up on Render.com
- [ ] Connect GitHub repository
- [ ] Create Web Service for backend
- [ ] Configure build and start commands
- [ ] Wait for deployment (5-10 min)
- [ ] Test backend URL
- [ ] (Optional) Deploy frontend separately
- [ ] Share your live URL! 🎉

---

## 🎯 Your URLs After Deployment

**Backend API:**
```
https://vois-backend.onrender.com
```

**Test Endpoints:**
- Health: `https://vois-backend.onrender.com/`
- Forecast: `https://vois-backend.onrender.com/forecast_vegan_demand` (POST)
- Suitability: `https://vois-backend.onrender.com/predict_suitability` (POST)

---

## 🌟 Pro Tips

1. **Free tier spins down** - First request takes 30s to wake up
2. **Keep it awake** - Use a service like UptimeRobot to ping every 14 minutes
3. **Logs** - Check Render dashboard for real-time logs
4. **Auto-deploy** - Push to GitHub = automatic deployment!

---

**Ready to deploy? Go to:** https://render.com

🎉 Your app will be live in 10 minutes!
