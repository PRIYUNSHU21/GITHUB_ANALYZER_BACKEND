import httpx
import asyncio
from datetime import datetime
from config.settings import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.last_api_call = 0  # Track last API call time for rate limiting
        
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return bool(self.api_key and self.api_key != "your_gemini_api_key_here")
    
    async def generate_three_insights(self, repo_data: dict, readme_content: str, 
                                    language_data: dict, contributor_data: dict) -> dict:
        """Generate three distinct AI insights as required"""
        if not self.is_available():
            return {
                "repository_summary": {
                    "content": "AI service not configured. Please add GEMINI_API_KEY to .env file.",
                    "generated_at": datetime.now().isoformat()
                },
                "language_analysis": {
                    "content": "AI service not configured.",
                    "generated_at": datetime.now().isoformat()
                },
                "contribution_patterns": {
                    "content": "AI service not configured.",
                    "generated_at": datetime.now().isoformat()
                }
            }
        
        try:
            # Generate all three insights with delays to avoid rate limiting
            logger.info("Generating repository summary...")
            repository_summary = await self._generate_repository_summary(repo_data, readme_content)
            
            # Add delay between API calls
            await asyncio.sleep(1)
            
            logger.info("Generating language analysis...")
            language_analysis = await self._generate_language_analysis(repo_data, language_data)
            
            # Add delay between API calls
            await asyncio.sleep(1)
            
            logger.info("Generating contribution patterns...")
            contribution_patterns = await self._generate_contribution_patterns(repo_data, contributor_data)
            
            return {
                "repository_summary": {
                    "content": repository_summary,
                    "generated_at": datetime.now().isoformat()
                },
                "language_analysis": {
                    "content": language_analysis,
                    "generated_at": datetime.now().isoformat()
                },
                "contribution_patterns": {
                    "content": contribution_patterns,
                    "generated_at": datetime.now().isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Error generating AI insights: {str(e)}")
            # Return meaningful fallback responses instead of error messages
            return {
                "repository_summary": {
                    "content": f"Repository analysis: {repo_data.get('name', 'Unknown repository')} - {repo_data.get('description', 'A GitHub repository')[:100]}{'...' if len(repo_data.get('description', '')) > 100 else ''}",
                    "generated_at": datetime.now().isoformat()
                },
                "language_analysis": {
                    "content": f"Technology stack: Primary language is {repo_data.get('language', 'Unknown')}. Language breakdown shows a {list(language_data.get('languages', {}).keys())[0] if language_data.get('languages') else 'mixed'}-focused project.",
                    "generated_at": datetime.now().isoformat()
                },
                "contribution_patterns": {
                    "content": f"Collaboration: This repository has {contributor_data.get('total_contributors', 0)} contributors with {contributor_data.get('active_contributors', 0)} active members, indicating {'healthy' if contributor_data.get('active_contributors', 0) > 5 else 'moderate'} community engagement.",
                    "generated_at": datetime.now().isoformat()
                }
            }
    
    async def _generate_repository_summary(self, repo_data: dict, readme_content: str) -> str:
        """Generate AI Repository Summary based on README and description"""
        prompt = f"""
Analyze this GitHub repository and provide a concise summary of its purpose and key features:

Repository: {repo_data.get('name', 'Unknown')}
Description: {repo_data.get('description', 'No description')}
Stars: {repo_data.get('stargazers_count', 0)}
Language: {repo_data.get('language', 'Unknown')}

README Content: {readme_content[:1500] if readme_content != "README not available" else "No README available"}

Provide a 2-3 sentence summary explaining what this repository does and its main purpose.
"""
        return await self._call_gemini_api(prompt)
    
    async def _generate_language_analysis(self, repo_data: dict, language_data: dict) -> str:
        """Generate AI Language Analysis for technology stack insights"""
        languages = language_data.get('languages', {})
        main_language = repo_data.get('language', 'Unknown')
        
        prompt = f"""
Analyze the technology stack of this repository:

Primary Language: {main_language}
Language Breakdown: {languages}
Repository Type: {repo_data.get('description', 'Unknown')}

Provide insights about the technology stack. Is this a standard framework combination (like MERN, MEAN, etc.)? 
What does the language composition tell us about the project's architecture? Keep it to 2-3 sentences.
"""
        return await self._call_gemini_api(prompt)
    
    async def _generate_contribution_patterns(self, repo_data: dict, contributor_data: dict) -> str:
        """Generate AI Contribution Patterns analysis for collaboration health"""
        total_contributors = contributor_data.get('total_contributors', 0)
        active_contributors = contributor_data.get('active_contributors', 0)
        top_contributors = contributor_data.get('top_contributors', [])
        
        prompt = f"""
Analyze the collaboration health of this repository:

Total Contributors: {total_contributors}
Active Contributors (5+ commits): {active_contributors}
Repository Age: {repo_data.get('created_at', 'Unknown')}
Last Updated: {repo_data.get('updated_at', 'Unknown')}
Top Contributors: {[c['username'] + f" ({c['commits']} commits)" for c in top_contributors[:3]]}

Provide insights about the project's collaboration patterns. Is it maintained by a core team or community? 
What does the contributor activity suggest about the project's health? Keep it to 2-3 sentences.
"""
        return await self._call_gemini_api(prompt)
    
    async def _call_gemini_api(self, prompt: str, max_retries: int = 3) -> str:
        """Make API call to Gemini with retry logic for rate limiting"""
        # Rate limiting: ensure at least 1 second between API calls
        import time
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call
        if time_since_last_call < 1.0:
            sleep_time = 1.0 - time_since_last_call
            await asyncio.sleep(sleep_time)
        
        self.last_api_call = time.time()
        
        for attempt in range(max_retries):
            try:
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
                    elif response.status_code == 429:  # Rate limit
                        wait_time = (2 ** attempt) + 1  # Exponential backoff
                        logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"API error {response.status_code}: {response.text}")
                        return f"AI service error: {response.status_code}"
                        
            except httpx.TimeoutException:
                logger.error(f"API timeout on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    return "AI service timeout"
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"API call failed on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return f"AI service error: {str(e)}"
                await asyncio.sleep(2)
        
        return "AI service unavailable after retries"
    
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
