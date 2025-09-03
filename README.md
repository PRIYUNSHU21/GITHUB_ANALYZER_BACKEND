# GitHub Repository Analyzer Backend

A FastAPI-based backend service that provides comprehensive analysis of GitHub repositories with AI-powered insights.

## Features

- **Repository Statistics**: Stars, forks, issues, license information
- **Language Analysis**: Programming language breakdown with percentages
- **Commit Activity**: Recent commit activity tracking
- **AI Insights**: AI-generated repository summaries using Google Gemini
- **Direct Links**: Repository and owner profile links

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional: for higher rate limits
DEBUG=True
```

### 3. Run the Server
```bash
python main.py
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Main Analysis Endpoint
```
POST /api/v1/analyze
```
**Body:**
```json
{
  "owner": "microsoft",
  "repo": "vscode"
}
```

**Response:** Complete repository analysis with AI insights

### Basic Stats Endpoint
```
GET /api/v1/repo/{owner}/{repo}/stats
```
**Response:** Basic repository statistics only

### Health Check
```
GET /api/v1/health
```
**Response:** Service health and AI availability status

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── settings.py        # Configuration management
├── models/
│   └── schemas.py         # Pydantic models for request/response
├── services/
│   ├── github_service.py  # GitHub API integration
│   └── ai_service.py      # AI/Gemini integration
└── routers/
    └── github_routes.py   # API route handlers
```

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key for AI insights
- `GITHUB_TOKEN`: GitHub personal access token (optional, for higher rate limits)
- `DEBUG`: Enable debug mode (True/False)

## Getting API Keys

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### GitHub Token (Optional)
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `public_repo` scope
3. Add it to your `.env` file

## Example Usage

```python
import httpx

# Analyze a repository
response = httpx.post("http://localhost:8000/api/v1/analyze", json={
    "owner": "facebook",
    "repo": "react"
})

data = response.json()
print(f"Stars: {data['stats']['stars']}")
print(f"AI Summary: {data['ai_insight']['summary']}")
```

## Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
The app can be deployed to:
- **Railway**: `railway up`
- **Render**: Connect GitHub repo
- **Vercel**: Add `vercel.json` for serverless deployment
- **Docker**: Use the provided Dockerfile

## Tech Stack

- **Framework**: FastAPI
- **HTTP Client**: httpx (async)
- **AI**: Google Gemini API
- **Validation**: Pydantic
- **Environment**: python-dotenv
