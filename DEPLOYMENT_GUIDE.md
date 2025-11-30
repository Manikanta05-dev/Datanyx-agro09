# 🚀 VOIS Deployment Guide

Complete guide for deploying VOIS (Vegan Orbital Intelligence System) to various platforms.

---

## 📋 Prerequisites

- Python 3.11+
- Git
- Docker (optional, for containerized deployment)
- Account on deployment platform (Heroku, AWS, Azure, or GCP)

---

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Build and run both backend and frontend
docker-compose up -d

# Access the application
# Backend: http://localhost:5000
# Frontend: http://localhost:8501
```

### Option 2: Docker (Backend Only)

```bash
# Build the Docker image
docker build -t vois-backend .

# Run the container
docker run -p 5000:5000 vois-backend

# Run frontend separately
pip install streamlit plotly requests pandas numpy
streamlit run frontend/dashboard.py
```

---

## 🌐 Heroku Deployment

### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create Heroku App
```bash
heroku create vois-app-name
```

### Step 4: Add Buildpack
```bash
heroku buildpacks:set heroku/python
```

### Step 5: Deploy
```bash
git push heroku main
```

### Step 6: Scale Dynos
```bash
heroku ps:scale web=1
```

### Step 7: Open App
```bash
heroku open
```

**Note:** For Heroku, you'll need to modify `backend/app.py` to use the PORT environment variable:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

---

## ☁️ AWS Deployment

### Option 1: AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize EB:**
```bash
eb init -p python-3.11 vois-app
```

3. **Create Environment:**
```bash
eb create vois-env
```

4. **Deploy:**
```bash
eb deploy
```

5. **Open App:**
```bash
eb open
```

### Option 2: AWS EC2

1. **Launch EC2 Instance** (Ubuntu 22.04)

2. **SSH into Instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv git -y
```

4. **Clone Repository:**
```bash
git clone https://github.com/Manikanta05-dev/Datanyx-agro09.git
cd Datanyx-agro09
```

5. **Setup Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Run Application:**
```bash
# Backend
python backend/app.py &

# Frontend
streamlit run frontend/dashboard.py --server.port 8501 --server.address 0.0.0.0 &
```

7. **Configure Security Group:**
- Open ports 5000 (backend) and 8501 (frontend)

---

## 🔷 Azure Deployment

### Option 1: Azure App Service

1. **Install Azure CLI:**
```bash
# Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

2. **Login:**
```bash
az login
```

3. **Create Resource Group:**
```bash
az group create --name vois-rg --location eastus
```

4. **Create App Service Plan:**
```bash
az appservice plan create --name vois-plan --resource-group vois-rg --sku B1 --is-linux
```

5. **Create Web App:**
```bash
az webapp create --resource-group vois-rg --plan vois-plan --name vois-app --runtime "PYTHON:3.11"
```

6. **Deploy:**
```bash
az webapp up --name vois-app --resource-group vois-rg
```

### Option 2: Azure Container Instances

1. **Build and Push Docker Image:**
```bash
az acr create --resource-group vois-rg --name voisregistry --sku Basic
az acr build --registry voisregistry --image vois:latest .
```

2. **Deploy Container:**
```bash
az container create --resource-group vois-rg --name vois-container --image voisregistry.azurecr.io/vois:latest --dns-name-label vois-app --ports 5000 8501
```

---

## 🔴 Google Cloud Platform (GCP) Deployment

### Option 1: Google App Engine

1. **Install gcloud CLI:**
```bash
# Download from: https://cloud.google.com/sdk/docs/install
```

2. **Initialize gcloud:**
```bash
gcloud init
```

3. **Create app.yaml:**
```yaml
runtime: python311
entrypoint: python backend/app.py

instance_class: F2

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

4. **Deploy:**
```bash
gcloud app deploy
```

5. **Open App:**
```bash
gcloud app browse
```

### Option 2: Google Cloud Run

1. **Build Container:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/vois
```

2. **Deploy:**
```bash
gcloud run deploy vois --image gcr.io/PROJECT_ID/vois --platform managed --region us-central1 --allow-unauthenticated
```

---

## 🔧 Environment Variables

Create a `.env` file for production:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_APP=backend/app.py
SECRET_KEY=your-secret-key-here

# API Configuration
API_URL=http://localhost:5000

# Database (if needed in future)
# DATABASE_URL=postgresql://user:pass@host:port/db

# CORS Settings
CORS_ORIGINS=*
```

---

## 📊 Production Checklist

### Before Deployment:

- [ ] Update `requirements.txt` with exact versions
- [ ] Set `debug=False` in Flask app
- [ ] Configure proper CORS origins
- [ ] Set up environment variables
- [ ] Test all API endpoints
- [ ] Verify model files are included
- [ ] Check data files are accessible
- [ ] Configure logging
- [ ] Set up monitoring

### After Deployment:

- [ ] Test all features in production
- [ ] Monitor application logs
- [ ] Set up SSL/HTTPS
- [ ] Configure custom domain (optional)
- [ ] Set up backup strategy
- [ ] Monitor resource usage
- [ ] Set up alerts

---

## 🔒 Security Best Practices

1. **Use HTTPS:** Always use SSL certificates in production
2. **Environment Variables:** Never commit secrets to git
3. **CORS:** Restrict CORS to specific domains
4. **Rate Limiting:** Implement API rate limiting
5. **Input Validation:** Validate all user inputs
6. **Authentication:** Add authentication for sensitive endpoints (future)

---

## 📈 Scaling Considerations

### Horizontal Scaling:
- Use load balancer (AWS ELB, Azure Load Balancer, GCP Load Balancer)
- Deploy multiple instances
- Use container orchestration (Kubernetes)

### Vertical Scaling:
- Increase instance size
- Add more CPU/RAM
- Optimize model loading

### Database Scaling (Future):
- Use managed database services
- Implement caching (Redis)
- Use CDN for static assets

---

## 🐛 Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Kill process (Linux/Mac)
kill -9 <PID>
```

### Issue: Models Not Loading
```bash
# Retrain models
python train_models.py

# Verify model files exist
ls -la models/
```

### Issue: CORS Errors
- Check CORS configuration in `backend/app.py`
- Ensure frontend URL is in allowed origins

### Issue: Memory Issues
- Reduce model size
- Use model compression
- Increase instance memory

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Review error messages
3. Verify all dependencies are installed
4. Ensure models are trained and accessible

---

## 🎯 Quick Deploy Commands

### Heroku:
```bash
heroku create vois-app
git push heroku main
heroku open
```

### Docker:
```bash
docker-compose up -d
```

### AWS EB:
```bash
eb init && eb create && eb deploy
```

### GCP:
```bash
gcloud app deploy
```

---

**🌱 VOIS is ready for production deployment!**
