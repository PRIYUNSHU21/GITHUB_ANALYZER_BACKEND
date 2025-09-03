# GitHub Repository Analyzer - Render Deployment

## Environment Variables Required on Render:

```
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
ENVIRONMENT=production
DEBUG=False
```

## Render Deployment Steps:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Create Render Account**:
   - Go to https://render.com
   - Sign up/Login with GitHub

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

4. **Configure Build Settings**:
   - **Name**: github-analyzer-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**:
   - Go to Environment tab
   - Add all variables from above

6. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

## Your API will be available at:
```
https://your-service-name.onrender.com
```

## Test Endpoints After Deployment:
- Health: https://your-service-name.onrender.com/api/v1/health
- Docs: https://your-service-name.onrender.com/docs
