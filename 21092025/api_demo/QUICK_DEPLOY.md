# ⚡ Quick Deploy Guide

## Deploy to Streamlit Cloud (5 minutes)

### Step 1: Push to GitHub
```bash
cd /Users/thanhvuong/Desktop/Hobbies/thanhvuong1605.github.io
git add .
git commit -m "Add beer sales prediction project"
git push origin main
```

### Step 2: Deploy Streamlit App

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository**: `thanhvuong1605/thanhvuong1605.github.io`
   - **Branch**: `main`
   - **Main file path**: `21092025/api_demo/streamlit_demo.py`
5. Click "Deploy"

Your app will be available at: `https://beer-sales-predictor.streamlit.app` (or similar)

### Step 3: Deploy API (Railway - Free tier)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add service:
   - **Root Directory**: `21092025/api_demo`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. Get your API URL (e.g., `https://beer-sales-api.railway.app`)

### Step 4: Connect Streamlit to API

1. Go back to Streamlit Cloud
2. Click on your app → "Settings" → "Secrets"
3. Add:
```toml
API_URL = "https://your-api-url.railway.app"
```
4. Save and redeploy

### Done! 🎉

Your app is now live and accessible from your website.

---

## Alternative: Deploy API to Render

1. Go to https://render.com
2. Sign up with GitHub
3. Create "New Web Service"
4. Connect repository
5. Settings:
   - **Name**: `beer-sales-api`
   - **Root Directory**: `21092025/api_demo`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy and get URL

Then update Streamlit secrets with the Render URL.

