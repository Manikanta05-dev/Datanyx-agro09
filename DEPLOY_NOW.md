# 🚀 Deploy to AWS RIGHT NOW - Step by Step

## Step 1: Get AWS Credentials

### Option A: If you have AWS Access Keys
1. Go to: https://console.aws.amazon.com/iam/home#/security_credentials
2. Click "Create access key"
3. Copy:
   - Access Key ID
   - Secret Access Key

### Option B: Configure AWS CLI
Run this command and enter your credentials:
```bash
aws configure
```

Enter:
- AWS Access Key ID: [your-key]
- AWS Secret Access Key: [your-secret]
- Default region: us-east-1
- Default output format: json

---

## Step 2: Initialize Elastic Beanstalk

```bash
cd v_pulse_app
eb init
```

**Answer the prompts:**
1. Select region: **10) us-east-1** (or your preferred region)
2. Application name: **vois-app** (press Enter)
3. Platform: **Python**
4. Platform version: **Python 3.11** (or latest)
5. SSH: **No** (or Yes if you want SSH access)

---

## Step 3: Create Environment and Deploy

```bash
eb create vois-env
```

This will:
- Create the environment (5-10 minutes)
- Deploy your application
- Give you a URL

---

## Step 4: Open Your App

```bash
eb open
```

Your app will open in browser at:
`http://vois-env.us-east-1.elasticbeanstalk.com`

---

## 🎯 Quick Commands

```bash
# Check status
eb status

# View logs
eb logs

# Deploy updates
git add .
git commit -m "Update"
eb deploy

# Terminate (when done)
eb terminate vois-env
```

---

## ⚠️ Important Notes

1. **Port Configuration:** The app automatically uses $PORT from environment
2. **Models:** All model files will be uploaded (may take a few minutes)
3. **Cost:** Free tier covers 750 hours/month for 12 months

---

## 🆘 Troubleshooting

### If deployment fails:
```bash
eb logs
```

### If models not loading:
Check that `models/` folder is included in deployment

### If port error:
The backend is already configured to use `os.environ.get('PORT', 5000)`

---

## ✅ Success Checklist

After deployment:
- [ ] Visit the URL from `eb open`
- [ ] Backend API responds at `/`
- [ ] Can access Streamlit dashboard
- [ ] All features working

---

**Ready? Run these commands now:**

```bash
cd v_pulse_app
eb init
eb create vois-env
eb open
```

🎉 Your app will be live in 10 minutes!
