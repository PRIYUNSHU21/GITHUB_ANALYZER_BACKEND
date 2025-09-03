import httpx
from config.settings import settings
from typing import Optional

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return bool(self.api_key and self.api_key != "your_gemini_api_key_here")
    
    async def generate_repo_summary(self, repo_data: dict, readme_content: Optional[str] = None) -> str:
        """Generate AI summary of the repository"""
        if not self.is_available():
            return "AI service not configured. Please add GEMINI_API_KEY to .env file."
        
        try:
            # Create prompt for Gemini
            prompt = self._create_summary_prompt(repo_data, readme_content)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/models/gemini-1.5-flash:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    return f"AI service error: {response.status_code} - {response.text}"
                    
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
    
    def _create_summary_prompt(self, repo_data: dict, readme_content: Optional[str]) -> str:
        """Create a prompt for repository summary"""
        repo_name = repo_data.get("name", "Unknown")
        description = repo_data.get("description", "No description available")
        language = repo_data.get("language", "Unknown")
        stars = repo_data.get("stargazers_count", 0)
        
        # Truncate README if too long
        readme_snippet = ""
        if readme_content and readme_content != "README not available":
            readme_snippet = readme_content[:1000] + "..." if len(readme_content) > 1000 else readme_content
        
        prompt = f"""
Analyze this GitHub repository and provide a concise, informative summary in 2-3 sentences:

Repository: {repo_name}
Description: {description}
Primary Language: {language}
Stars: {stars}

{f"README Content: {readme_snippet}" if readme_snippet else ""}

Please provide a clear, professional summary that explains what this repository does, its main purpose, and key features. Keep it under 100 words.
"""
        return prompt
