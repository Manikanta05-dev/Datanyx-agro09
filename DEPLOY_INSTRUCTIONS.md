# 🚀 EXACT DEPLOYMENT STEPS - Click by Click

## 🎯 PART 1: Deploy Backend on Render (5 minutes)

### Step 1: Open Render
1. Go to: **https://render.com**
2. Click **"Get Started"** (top right)
3. Click **"Sign Up with GitHub"**
4. Authorize Render to access your GitHub

### Step 2: Create Backend Service
1. Click **"New +"** button (top right)
2. Click **"Web Service"**
3. Find repository: **Datanyx-agro09**
4. Click **"Connect"** button next to it

### Step 3: Fill in the Form

**Copy and paste these EXACT values:**

| Field | Value |
|-------|-------|
| **Name** | `vois-backend` |
| **Region** | Oregon (US West) |
| **Branch** | `main` |
| **Root Directory** | `v_pulse_app` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python backend/app.py` |

### Step 4: Select Plan
- Scroll down to **"Instance Type"**
- Select **"Free"**

### Step 5: Deploy!
1. Click **"Create Web Service"** (bottom)
2. Wait 5-10 minutes
3. Copy your URL (looks like: `https://vois-backend-xxxx.onrender.com`)

✅ **Backend is LIVE!**

---

## 🎨 PART 2: Deploy Frontend on Streamlit Cloud (3 minutes)

### Step 1: Open Streamlit Cloud
1. Go to: **https://share.streamlit.io**
2. Click **"Sign in"**
3. Click **"Continue with GitHub"**
4. Authorize Streamlit

### Step 2: Deploy New App
1. Click **"New app"** button
2. Fill in the form:

| Field | Value |
|-------|-------|
| **Repository** | `Manikanta05-dev/Datanyx-agro09` |
| **Branch** | `main` |
| **Main file path** | `v_pulse_app/frontend/dashboard.py` |

### Step 3: Advanced Settings (Optional)
1. Click **"Advanced settings"**
2. Add Python version: `3.11`

### Step 4: Deploy!
1. Click **"Deploy!"** button
2. Wait 3-5 minutes
3. Your app will open automatically!

✅ **Frontend is LIVE!**

---

## 🔗 Connect Frontend to Backend

### Option A: Update in Code (if needed)
If the frontend can't connect to backend, update the API URL:

1. Go to Streamlit Cloud dashboard
2. Click your app → **"Settings"** → **"Secrets"**
3. Add:
```toml
API_URL = "https://vois-backend-xxxx.onrender.com"
```

### Option B: It Should Work Automatically
The frontend is configured to use `http://localhost:5000` by default, which works for local development. For production, you may need to update this.

---

## 📋 Quick Checklist

### Backend (Render):
- [ ] Sign up on Render.com
- [ ] Create Web Service
- [ ] Repository: Datanyx-agro09
- [ ] Root Directory: `v_pulse_app`
- [ ] Start Command: `python backend/app.py`
- [ ] Deploy and copy URL

### Frontend (Streamlit Cloud):
- [ ] Sign up on share.streamlit.io
- [ ] Create New App
- [ ] Repository: Datanyx-agro09
- [ ] Main file: `v_pulse_app/frontend/dashboard.py`
- [ ] Deploy!

---

## 🎉 After Deployment

### Your Live URLs:
- **Backend API:** `https://vois-backend-xxxx.onrender.com`
- **Frontend Dashboard:** `https://your-app.streamlit.app`

### Test Your App:
1. Open frontend URL
2. Try Demand Forecasting
3. Try Crop Suitability
4. Try Combined Intelligence

---

## 🆘 Troubleshooting

### Backend won't start?
- Check Render logs (click "Logs" tab)
- Verify Root Directory is `v_pulse_app`
- Wait for models to load (may take 2-3 minutes)

### Frontend can't connect to backend?
- Update API_URL in Streamlit secrets
- Check backend is running (visit backend URL)

### Free tier limitations?
- Render: Spins down after 15 min inactivity
- First request takes ~30 seconds to wake up
- Streamlit: Always on, no spin down!

---

## 💰 Cost

**Total Cost: $0 (FREE!)**
- Render Free Tier: 750 hours/month
- Streamlit Cloud: Unlimited (free tier)

---

## 🚀 Ready to Deploy?

1. **Backend:** https://render.com
2. **Frontend:** https://share.streamlit.io

**Time needed:** 10 minutes total

**You'll get:** 2 live URLs to share!

---

## 📸 Screenshots Guide

### Render Configuration:
```
Name: vois-backend
Root Directory: v_pulse_app
Build Command: pip install -r requirements.txt
Start Command: python backend/app.py
Instance Type: Free
```

### Streamlit Configuration:
```
Repository: Manikanta05-dev/Datanyx-agro09
Branch: main
Main file path: v_pulse_app/frontend/dashboard.py
```

---

**Start deploying now! Both platforms are free and easy!** 🎉
