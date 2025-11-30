# 🚀 VOIS Deployment Guide

## Deploy Your Hackathon Project to Production

---

## Option 1: Docker Deployment (Recommended)

### Step 1: Create Dockerfile for Backend

Create `v_pulse_app/backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/backend
COPY ../models /app/models
COPY ../data /app/data

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "backend/app.py"]
```

### Step 2: Create Dockerfile for Frontend

Create `v_pulse_app/frontend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/frontend

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "frontend/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 3: Create docker-compose.yml

Create `v_pulse_app/docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - API_URL=http://backend:5000
    restart: unless-stopped
```

### Step 4: Build and Run

```bash
cd v_pulse_app

# Build images
docker-compose build

# Run containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

Access:
- Frontend: http://localhost:8501
- Backend: http://localhost:5000

---

## Option 2: Heroku Deployment

### Backend Deployment

1. **Create Procfile** (`v_pulse_app/Procfile`):
```
web: python backend/app.py
```

2. **Create runtime.txt** (`v_pulse_app/runtime.txt`):
```
python-3.9.16
```

3. **Deploy to Heroku**:
```bash
cd v_pulse_app

# Login to Heroku
heroku login

# Create app
heroku create vois-backend

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Open app
heroku open
```

### Frontend Deployment

1. **Create setup.sh** (`v_pulse_app/frontend/setup.sh`):
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

2. **Create Procfile** (`v_pulse_app/frontend/Procfile`):
```
web: sh setup.sh && streamlit run dashboard.py
```

3. **Deploy**:
```bash
cd v_pulse_app/frontend

heroku create vois-frontend
heroku buildpacks:set heroku/python
git push heroku main
```

---

## Option 3: AWS Deployment

### Backend on AWS EC2

1. **Launch EC2 Instance**:
   - AMI: Ubuntu 22.04
   - Instance Type: t2.micro (free tier)
   - Security Group: Allow ports 22, 5000

2. **SSH into instance**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Setup application**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone or upload your code
git clone your-repo-url
cd v_pulse_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train models
python train_models.py

# Run backend
python backend/app.py
```

4. **Setup as service** (`/etc/systemd/system/vois-backend.service`):
```ini
[Unit]
Description=VOIS Backend API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/v_pulse_app
Environment="PATH=/home/ubuntu/v_pulse_app/venv/bin"
ExecStart=/home/ubuntu/v_pulse_app/venv/bin/python backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vois-backend
sudo systemctl start vois-backend
sudo systemctl status vois-backend
```

### Frontend on AWS EC2

Similar process, but run Streamlit:
```bash
streamlit run frontend/dashboard.py --server.port 8501 --server.address 0.0.0.0
```

---

## Option 4: Azure Deployment

### Backend on Azure App Service

1. **Install Azure CLI**:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

2. **Login and deploy**:
```bash
az login

# Create resource group
az group create --name vois-rg --location eastus

# Create app service plan
az appservice plan create --name vois-plan --resource-group vois-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group vois-rg --plan vois-plan --name vois-backend --runtime "PYTHON:3.9"

# Deploy code
cd v_pulse_app
az webapp up --name vois-backend --resource-group vois-rg
```

### Frontend on Azure

Similar process for frontend:
```bash
az webapp create --resource-group vois-rg --plan vois-plan --name vois-frontend --runtime "PYTHON:3.9"
az webapp up --name vois-frontend --resource-group vois-rg
```

---

## Option 5: Google Cloud Platform (GCP)

### Backend on Cloud Run

1. **Install gcloud CLI**:
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

2. **Build and deploy**:
```bash
cd v_pulse_app/backend

# Build container
gcloud builds submit --tag gcr.io/your-project-id/vois-backend

# Deploy to Cloud Run
gcloud run deploy vois-backend \
  --image gcr.io/your-project-id/vois-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend on Cloud Run

```bash
cd v_pulse_app/frontend

gcloud builds submit --tag gcr.io/your-project-id/vois-frontend
gcloud run deploy vois-frontend \
  --image gcr.io/your-project-id/vois-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 6: Vercel (Frontend Only)

Perfect for Streamlit dashboards:

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Create vercel.json** (`v_pulse_app/frontend/vercel.json`):
```json
{
  "builds": [
    {
      "src": "dashboard.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "dashboard.py"
    }
  ]
}
```

3. **Deploy**:
```bash
cd v_pulse_app/frontend
vercel
```

---

## Option 7: Railway (Easiest)

### Backend

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Python and deploys
5. Get your backend URL

### Frontend

1. Create new project
2. Deploy from GitHub
3. Set start command: `streamlit run frontend/dashboard.py`
4. Get your frontend URL

---

## Environment Variables

### Backend (.env)
```bash
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
CORS_ORIGINS=https://your-frontend-url.com
```

### Frontend (.env)
```bash
API_URL=https://your-backend-url.com
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Using Cloudflare (Free)

1. Add your domain to Cloudflare
2. Update nameservers
3. Enable "Always Use HTTPS"
4. Enable "Automatic HTTPS Rewrites"

---

## Database Setup (Optional)

If you want to store predictions:

### PostgreSQL on Heroku
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### MongoDB Atlas (Free)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update backend to use MongoDB

---

## Monitoring & Logging

### Option 1: Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

Add to `backend/app.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Option 2: Datadog (Full Monitoring)

```bash
pip install ddtrace
```

Run with:
```bash
ddtrace-run python backend/app.py
```

### Option 3: CloudWatch (AWS)

Automatically enabled on AWS services.

---

## Performance Optimization

### 1. Model Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def predict_demand(region, product, price):
    # Your prediction logic
    pass
```

### 2. API Rate Limiting
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/predict')
@limiter.limit("10 per minute")
def predict():
    pass
```

### 3. Response Compression
```python
from flask_compress import Compress

Compress(app)
```

### 4. CDN for Static Assets
Use Cloudflare or AWS CloudFront.

---

## Security Best Practices

1. **API Keys**: Use environment variables
2. **CORS**: Restrict to your frontend domain
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize all inputs
5. **HTTPS**: Always use SSL
6. **Secrets**: Never commit to Git
7. **Updates**: Keep dependencies updated

---

## Cost Estimation

### Free Tier Options:
- **Heroku**: Free (with limitations)
- **Railway**: $5/month
- **Vercel**: Free for personal projects
- **AWS Free Tier**: 12 months free (t2.micro)
- **GCP Free Tier**: $300 credit
- **Azure Free Tier**: $200 credit

### Production Costs (Monthly):
- **Small Scale** (< 1000 users): $10-30
- **Medium Scale** (< 10,000 users): $50-100
- **Large Scale** (< 100,000 users): $200-500

---

## Backup & Recovery

### Automated Backups

```bash
# Backup models
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/

# Backup data
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Upload to S3
aws s3 cp models-backup-*.tar.gz s3://your-bucket/backups/
```

### Cron Job for Daily Backups

```bash
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * /path/to/backup-script.sh
```

---

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy VOIS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Train models
      run: |
        python train_models.py
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "vois-backend"
        heroku_email: "your-email@example.com"
```

---

## Domain Setup

### Buy Domain (Optional)
- Namecheap: $10-15/year
- GoDaddy: $12-20/year
- Google Domains: $12/year

### Point to Your App
1. Get your app's IP or URL
2. Add A record or CNAME in DNS settings
3. Wait for propagation (5-30 minutes)

Example:
- `api.vois.com` → Backend
- `app.vois.com` → Frontend
- `www.vois.com` → Landing page

---

## Post-Deployment Checklist

- [ ] Backend is accessible
- [ ] Frontend is accessible
- [ ] API endpoints work
- [ ] Models are loaded
- [ ] HTTPS is enabled
- [ ] CORS is configured
- [ ] Error tracking is setup
- [ ] Backups are automated
- [ ] Monitoring is active
- [ ] Domain is configured
- [ ] Documentation is updated

---

## Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Port already in use"
```bash
# Change port in app.py
app.run(port=5001)
```

### Issue: "Models not loading"
```bash
# Check file paths
ls -la models/
# Retrain if needed
python train_models.py
```

### Issue: "CORS errors"
```python
# Update CORS settings in app.py
CORS(app, origins=["https://your-frontend-url.com"])
```

---

## Support & Maintenance

### Weekly Tasks:
- Check error logs
- Monitor API usage
- Review performance metrics

### Monthly Tasks:
- Update dependencies
- Retrain models with new data
- Review security patches

### Quarterly Tasks:
- Full system audit
- Performance optimization
- Feature updates

---

**Your VOIS system is now production-ready! 🚀🌱**
