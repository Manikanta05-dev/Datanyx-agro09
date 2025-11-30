# 🚀 AWS Deployment Guide for VOIS

Complete guide for deploying VOIS to AWS with both backend and frontend.

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  AWS Cloud                          │
│                                                     │
│  ┌──────────────────┐      ┌──────────────────┐   │
│  │   S3 + CloudFront│      │   EC2/Beanstalk  │   │
│  │  (React Frontend)│◄────►│  (Flask Backend) │   │
│  │   Port: 80/443   │      │    Port: 5000    │   │
│  └──────────────────┘      └──────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Deployment Options

### Option 1: Streamlit Frontend (Current)
- **Backend:** AWS EC2 or Elastic Beanstalk
- **Frontend:** Same EC2 instance (Streamlit on port 8501)

### Option 2: React Frontend (Recommended for Production)
- **Backend:** AWS EC2 or Elastic Beanstalk
- **Frontend:** AWS S3 + CloudFront or Amplify

---

## 📦 OPTION 1: Streamlit Frontend Deployment

### Backend + Frontend on EC2

#### Step 1: Launch EC2 Instance
```bash
# Instance Type: t2.medium or t3.medium
# OS: Ubuntu 22.04 LTS
# Storage: 20GB
# Security Group: Open ports 22, 5000, 8501
```

#### Step 2: Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
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

#### Step 3: Start Services
```bash
# Start Backend (in background)
nohup python backend/app.py > backend.log 2>&1 &

# Start Frontend (in background)
nohup streamlit run frontend/dashboard.py --server.port=8501 --server.address=0.0.0.0 > frontend.log 2>&1 &
```

#### Step 4: Access Application
- **Backend API:** http://your-ec2-ip:5000
- **Frontend Dashboard:** http://your-ec2-ip:8501

### Using Elastic Beanstalk (Streamlit)

Create `Procfile`:
```
web: streamlit run frontend/dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

Deploy:
```bash
eb init -p python-3.11 vois-app
eb create vois-env
eb deploy
```

---

## 📦 OPTION 2: React Frontend Deployment (Production Ready)

### Frontend Build Configuration

#### Build Command:
```bash
cd frontend && npm install && npm run build
```

#### Build Output Directory:
```
frontend/dist
```

#### Environment Variables:
```env
VITE_API_URL=https://your-backend-api-url.com
```

---

## 🌐 Deploy React Frontend to AWS Amplify

### Step 1: Update vite.config.js for Production

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  },
  server: {
    port: 3000
  },
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:5000')
  }
})
```

### Step 2: Create Build Specification

Create `amplify.yml` in project root:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

### Step 3: Deploy to AWS Amplify

1. **Go to AWS Amplify Console**
2. **Connect Repository:**
   - Choose GitHub
   - Select repository: `Manikanta05-dev/Datanyx-agro09`
   - Branch: `main`

3. **Build Settings:**
   - Build command: `npm run build`
   - Build output directory: `frontend/dist`
   - Base directory: `frontend`

4. **Environment Variables:**
   ```
   VITE_API_URL = https://your-backend-url.com
   ```

5. **Deploy!**

### AWS Amplify CLI Method

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Configure Amplify
amplify configure

# Initialize Amplify in your project
cd frontend
amplify init

# Add hosting
amplify add hosting

# Choose: Amazon CloudFront and S3

# Publish
amplify publish
```

---

## 🗄️ Deploy React Frontend to S3 + CloudFront

### Step 1: Build the Frontend

```bash
cd frontend
npm install
npm run build
```

### Step 2: Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://vois-frontend

# Enable static website hosting
aws s3 website s3://vois-frontend --index-document index.html --error-document index.html
```

### Step 3: Upload Build Files

```bash
# Upload dist folder to S3
aws s3 sync dist/ s3://vois-frontend --acl public-read
```

### Step 4: Create CloudFront Distribution

```bash
# Create distribution (via AWS Console or CLI)
# Origin: vois-frontend.s3.amazonaws.com
# Default Root Object: index.html
# Error Pages: 404 -> /index.html (for React Router)
```

### Step 5: Update API URL

Update `frontend/src/services/api.js`:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'https://your-backend-api.com';
```

---

## 🖥️ Deploy Backend to AWS

### Option A: Elastic Beanstalk

#### Step 1: Install EB CLI
```bash
pip install awsebcli
```

#### Step 2: Initialize and Deploy
```bash
# Initialize
eb init -p python-3.11 vois-backend --region us-east-1

# Create environment
eb create vois-backend-env

# Deploy
eb deploy

# Get URL
eb status
```

#### Step 3: Configure Environment Variables
```bash
eb setenv FLASK_ENV=production DEBUG=False
```

### Option B: EC2 with Docker

#### Step 1: Build and Push Docker Image

```bash
# Build image
docker build -t vois-backend .

# Tag for ECR
docker tag vois-backend:latest YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/vois-backend:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/vois-backend:latest
```

#### Step 2: Deploy to EC2

```bash
# SSH to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Pull and run Docker image
docker pull YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/vois-backend:latest
docker run -d -p 5000:5000 YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/vois-backend:latest
```

---

## 🔧 Complete Deployment Commands

### For AWS Amplify (React Frontend):

**Build Command:**
```bash
cd frontend && npm ci && npm run build
```

**Build Output Directory:**
```
frontend/dist
```

**Base Directory:**
```
frontend
```

**Environment Variables:**
```
VITE_API_URL=https://your-backend-api-url.com
```

### For S3 Static Hosting (React Frontend):

```bash
# Build
cd frontend
npm install
npm run build

# Deploy
aws s3 sync dist/ s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### For EC2 (Streamlit Frontend):

```bash
# No build needed
streamlit run frontend/dashboard.py --server.port=8501 --server.address=0.0.0.0
```

---

## 📝 Build Specification Files

### amplify.yml (for AWS Amplify)

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

### buildspec.yml (for AWS CodeBuild)

```yaml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Installing dependencies...
      - cd frontend
      - npm install
  build:
    commands:
      - echo Build started on `date`
      - npm run build
  post_build:
    commands:
      - echo Build completed on `date`

artifacts:
  files:
    - '**/*'
  base-directory: frontend/dist
```

---

## 🔒 Security Configuration

### CORS Configuration (Backend)

Update `backend/app.py`:
```python
from flask_cors import CORS

# Production CORS
CORS(app, origins=[
    "https://your-cloudfront-domain.cloudfront.net",
    "https://your-amplify-domain.amplifyapp.com"
])
```

### Environment Variables

**Backend (.env):**
```env
FLASK_ENV=production
DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env.production):**
```env
VITE_API_URL=https://your-backend-api.com
```

---

## 📊 Cost Estimation

### Option 1: Streamlit on EC2
- **EC2 t3.medium:** ~$30/month
- **Total:** ~$30/month

### Option 2: React + S3 + CloudFront
- **S3:** ~$1/month
- **CloudFront:** ~$5/month
- **EC2 for Backend:** ~$30/month
- **Total:** ~$36/month

### Option 3: Amplify + Elastic Beanstalk
- **Amplify:** ~$15/month
- **Elastic Beanstalk:** ~$30/month
- **Total:** ~$45/month

---

## 🚀 Quick Deploy Script

Create `deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Deploying VOIS to AWS..."

# Build Frontend
echo "📦 Building React Frontend..."
cd frontend
npm install
npm run build

# Upload to S3
echo "☁️ Uploading to S3..."
aws s3 sync dist/ s3://vois-frontend --delete

# Invalidate CloudFront
echo "🔄 Invalidating CloudFront cache..."
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"

# Deploy Backend
echo "🖥️ Deploying Backend..."
cd ..
eb deploy

echo "✅ Deployment complete!"
echo "Frontend: https://your-cloudfront-domain.cloudfront.net"
echo "Backend: https://your-backend-url.com"
```

Make executable:
```bash
chmod +x deploy.sh
```

---

## 🎯 Recommended Setup

**For Production:**
1. **Frontend:** AWS Amplify (React) - Easiest
2. **Backend:** AWS Elastic Beanstalk - Scalable
3. **Database:** AWS RDS (if needed in future)
4. **Storage:** S3 for model files

**For Development/Demo:**
1. **Frontend + Backend:** Single EC2 instance (Streamlit)
2. **Cost-effective and simple**

---

## 📞 Support

**Common Issues:**

1. **CORS Errors:** Update CORS origins in backend
2. **Build Fails:** Check Node.js version (use v18+)
3. **API Connection:** Verify VITE_API_URL is set correctly
4. **Port Issues:** Ensure security groups allow traffic

---

**🌱 Ready to deploy VOIS to AWS!**
