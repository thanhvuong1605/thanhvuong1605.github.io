# 🚀 Deployment Guide

This guide explains how to deploy the Beer Sales Prediction system online.

## Architecture

The system consists of two components:
1. **FastAPI Backend** - ML model API server
2. **Streamlit Frontend** - Interactive web interface

## Option 1: Streamlit Cloud (Recommended for Frontend)

Streamlit Cloud offers free hosting for Streamlit apps.

### Prerequisites
- GitHub account
- Repository pushed to GitHub

### Steps

1. **Push your code to GitHub** (if not already done):
```bash
git add .
git commit -m "Add beer sales prediction project"
git push origin main
```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Sign in with GitHub
   - Click "New app"

3. **Configure the app**:
   - **Repository**: Select your repository
   - **Branch**: `main` (or your branch)
   - **Main file path**: `21092025/api_demo/streamlit_demo.py`
   - **Python version**: 3.8 or higher

4. **Set Environment Variables** (if API is hosted separately):
   - Click "Advanced settings"
   - Add environment variable:
     - Key: `API_URL`
     - Value: Your deployed API URL (e.g., `https://your-api.railway.app`)

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://your-app-name.streamlit.app`

### Limitations
- Streamlit Cloud only hosts the frontend
- You'll need to deploy the API separately (see Option 2)

---

## Option 2: Deploy API to Railway/Render

### Railway (Recommended)

1. **Sign up at [Railway](https://railway.app)**

2. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"

3. **Configure the service**:
   - Select your repository
   - Root directory: `21092025/api_demo`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`

4. **Set environment variables** (if needed):
   - `PORT` (Railway sets this automatically)
   - `MODEL_DIR` (if models are in a different location)

5. **Deploy**
   - Railway will automatically deploy
   - Get your API URL (e.g., `https://your-api.railway.app`)

### Render

1. **Sign up at [Render](https://render.com)**

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Settings:
     - **Name**: `beer-sales-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Root Directory**: `21092025/api_demo`

3. **Set environment variables**:
   - `PORT` (Render sets this automatically)

4. **Deploy**
   - Render will build and deploy automatically
   - Get your API URL

---

## Option 3: Deploy Both Together (Docker)

### Create Dockerfile for API

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy model files (adjust path as needed)
COPY ../model /app/model

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy to Railway/Render with Docker

1. Push Dockerfile to repository
2. Configure service to use Docker
3. Deploy

---

## Option 4: Deploy to Your Own Server

### Using systemd (Linux)

1. **Create service file** `/etc/systemd/system/beer-sales-api.service`:

```ini
[Unit]
Description=Beer Sales Prediction API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/21092025/api_demo
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

2. **Start the service**:
```bash
sudo systemctl enable beer-sales-api
sudo systemctl start beer-sales-api
```

3. **Set up reverse proxy** (Nginx):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Environment Variables

### API Server
- `API_HOST`: Host to bind to (default: `0.0.0.0`)
- `API_PORT`: Port to listen on (default: `8000`)
- `MODEL_DIR`: Path to model directory (default: `../model`)

### Streamlit App
- `API_URL`: URL of the API server (default: `http://localhost:8000`)

---

## Troubleshooting

### API won't start
- Check if model files exist in the correct location
- Verify all dependencies are installed
- Check logs for error messages

### Streamlit can't connect to API
- Verify API URL is correct
- Check if API is accessible (try `curl https://your-api-url/health`)
- Ensure CORS is enabled in API (already configured)

### Model files not found
- Ensure model files are in the repository or accessible
- For large files, consider using Git LFS or external storage
- Update `MODEL_DIR` environment variable if needed

---

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Model files accessible (in repo or external storage)
- [ ] API deployed and accessible
- [ ] API URL configured in Streamlit app
- [ ] Streamlit app deployed
- [ ] Test predictions work end-to-end

---

## Example Deployment URLs

After deployment, you'll have:
- **API**: `https://beer-sales-api.railway.app`
- **Streamlit**: `https://beer-sales-predictor.streamlit.app`

Update the Streamlit app's `API_URL` environment variable to point to your deployed API.

---

## Cost Estimates

- **Streamlit Cloud**: Free
- **Railway**: Free tier available, then ~$5-20/month
- **Render**: Free tier available, then ~$7-25/month
- **Your own server**: Varies (e.g., DigitalOcean $5-10/month)

---

**Need help?** Check the main README.md or open an issue.

