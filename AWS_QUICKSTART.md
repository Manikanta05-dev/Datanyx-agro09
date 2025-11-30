# 🚀 AWS Deployment Quick Start

## 📋 What You Need

✅ AWS Account (free tier works)
✅ GitHub repository: https://github.com/Manikanta05-dev/Datanyx-agro09

---

## 🎯 Choose Your Deployment Method

### **Option 1: AWS Amplify (Easiest - Recommended)**
- ✅ Automatic builds from GitHub
- ✅ Free SSL certificate
- ✅ CDN included
- ✅ Best for React frontend

### **Option 2: AWS Elastic Beanstalk**
- ✅ Good for full-stack apps
- ✅ Auto-scaling
- ✅ Works with Streamlit

### **Option 3: AWS EC2**
- ✅ Full control
- ✅ Most flexible
- ✅ Manual setup required

---

## 🌟 OPTION 1: AWS Amplify (React Frontend)

### Step 1: Go to AWS Amplify Console
1. Open: https://console.aws.amazon.com/amplify/
2. Click **"New app"** → **"Host web app"**

### Step 2: Connect GitHub
1. Select **GitHub**
2. Authorize AWS Amplify
3. Choose repository: **Datanyx-agro09**
4. Choose branch: **main**

### Step 3: Configure Build Settings
```yaml
Build command: cd frontend && npm ci && npm run build
Build output directory: frontend/dist
Base directory: (leave empty)
```

Or use the `amplify.yml` file (already in your repo)

### Step 4: Add Environment Variables
```
VITE_API_URL = https://your-backend-url.com
```
(You'll get this after deploying the backend)

### Step 5: Deploy!
Click **"Save and deploy"**

⏱️ Wait 5-10 minutes for deployment

### Step 6: Get Your URL
You'll get a URL like: `https://main.d1234abcd.amplifyapp.com`

---

## 🖥️ Deploy Backend (Required for Amplify)

### Method A: AWS Elastic Beanstalk (Recommended)

#### Install EB CLI:
```bash
pip install awsebcli
```

#### Deploy:
```bash
cd v_pulse_app

# Initialize
eb init -p python-3.11 vois-backend --region us-east-1

# Create environment
eb create vois-backend-env

# Deploy
eb deploy
```

#### Get Backend URL:
```bash
eb status
```
Copy the CNAME URL (e.g., `vois-backend-env.us-east-1.elasticbeanstalk.com`)

#### Update Frontend:
Go back to Amplify → Environment variables → Update `VITE_API_URL`

---

## 🎯 OPTION 2: AWS Elastic Beanstalk (Full Stack)

### For Streamlit Frontend + Backend:

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 vois-app --region us-east-1

# Create environment
eb create vois-env

# Deploy
eb deploy

# Open app
eb open
```

Your app will be at: `http://vois-env.us-east-1.elasticbeanstalk.com`

---

## 💻 OPTION 3: AWS EC2 (Manual)

### Step 1: Launch EC2 Instance
1. Go to: https://console.aws.amazon.com/ec2/
2. Click **"Launch Instance"**
3. Choose: **Ubuntu Server 22.04 LTS**
4. Instance type: **t2.medium** (or t3.medium)
5. Create/select key pair
6. Security group: Allow ports **22, 5000, 8501**
7. Launch!

### Step 2: Connect to Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Setup Application
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/Manikanta05-dev/Datanyx-agro09.git
cd Datanyx-agro09

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 4: Start Services
```bash
# Start backend
nohup python backend/app.py > backend.log 2>&1 &

# Start frontend
nohup streamlit run frontend/dashboard.py --server.port=8501 --server.address=0.0.0.0 > frontend.log 2>&1 &
```

### Step 5: Access Application
- **Backend:** http://your-ec2-ip:5000
- **Frontend:** http://your-ec2-ip:8501

---

## 🔧 Quick Commands Reference

### Check AWS CLI Installation:
```bash
aws --version
```

### Install AWS CLI (if needed):
```bash
# Windows
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Mac
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Configure AWS CLI:
```bash
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: us-east-1
# - Default output format: json
```

---

## 📊 Deployment Summary

### For AWS Amplify (React):
```
✅ Build Command: cd frontend && npm ci && npm run build
✅ Build Output: frontend/dist
✅ Environment Variable: VITE_API_URL
```

### For Elastic Beanstalk (Streamlit):
```
✅ Platform: Python 3.11
✅ Entry Point: Procfile (already in repo)
✅ Port: Automatic (from $PORT)
```

### For EC2:
```
✅ Backend Port: 5000
✅ Frontend Port: 8501
✅ Security Group: Open both ports
```

---

## 🎬 Recommended Deployment Flow

### 1. Deploy Backend First (Elastic Beanstalk):
```bash
eb init -p python-3.11 vois-backend
eb create vois-backend-env
eb deploy
```

### 2. Get Backend URL:
```bash
eb status
# Copy the CNAME URL
```

### 3. Deploy Frontend (AWS Amplify):
- Go to Amplify Console
- Connect GitHub repo
- Add environment variable: `VITE_API_URL=<backend-url>`
- Deploy!

### 4. Done! 🎉
- Frontend: `https://main.xxxxx.amplifyapp.com`
- Backend: `http://vois-backend-env.elasticbeanstalk.com`

---

## 💰 Cost Estimate

### Free Tier (First 12 months):
- **Amplify:** 1000 build minutes/month free
- **Elastic Beanstalk:** Free (pay for EC2)
- **EC2 t2.micro:** 750 hours/month free

### After Free Tier:
- **Amplify:** ~$15/month
- **Elastic Beanstalk:** ~$30/month
- **Total:** ~$45/month

---

## 🆘 Need Help?

### Check Logs:

**Elastic Beanstalk:**
```bash
eb logs
```

**EC2:**
```bash
tail -f backend.log
tail -f frontend.log
```

**Amplify:**
- Go to Amplify Console → Your App → Build logs

---

## ✅ Verification Checklist

After deployment:
- [ ] Backend API responds at `/` endpoint
- [ ] Frontend loads successfully
- [ ] Can forecast demand
- [ ] Can check crop suitability
- [ ] Can optimize supply chain
- [ ] All 4 models working

---

## 🚀 Ready to Deploy!

**Easiest Path:**
1. Deploy backend with Elastic Beanstalk (5 minutes)
2. Deploy frontend with Amplify (10 minutes)
3. Total time: 15 minutes!

**Start here:** https://console.aws.amazon.com/amplify/

Good luck! 🌱
