import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # GitHub API
    GITHUB_API_BASE_URL = "https://api.github.com"
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional: for higher rate limits
    
    # AI API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # App settings
    APP_NAME = "GitHub Repository Analyzer"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

settings = Settings()
