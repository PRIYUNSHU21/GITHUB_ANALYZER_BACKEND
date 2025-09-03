import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from groq import Groq
from config.settings import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model_name = "llama-3.1-8b-instant"
        self.max_retries = 3
        
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return bool(settings.GROQ_API_KEY and settings.GROQ_API_KEY != "your_groq_api_key_here")
        
    async def _call_groq_api(self, prompt: str) -> str:
        """Make API call to Groq with retries and error handling"""
        for attempt in range(self.max_retries):
            try:
                # Add delay between attempts to avoid rate limiting
                if attempt > 0:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1,
                    stream=False,
                    stop=None
                )
                
                return completion.choices[0].message.content
                
            except Exception as e:
                logger.warning(f"Groq API attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    logger.error(f"All Groq API attempts failed: {str(e)}")
                    return f"AI service unavailable after retries"
                    
        return "AI service temporarily unavailable"

    async def generate_three_insights(self, repo_data: dict, readme_content: str, 
                                    language_data: dict, contributor_data: dict) -> dict:
        """Generate three distinct AI insights as required"""
        if not self.is_available():
            return {
                "repository_summary": {
                    "content": "AI service not configured. Please add GROQ_API_KEY to environment variables.",
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
            # Return meaningful fallback responses based on actual data
            repo_name = repo_data.get('name', 'Unknown repository')
            repo_desc = repo_data.get('description', 'A GitHub repository')
            primary_lang = repo_data.get('language', 'Unknown')
            stars = repo_data.get('stargazers_count', 0)
            
            # Get primary language from language data
            languages = language_data.get('languages', {})
            if languages:
                main_lang = max(languages.keys(), key=lambda k: languages[k])
            else:
                main_lang = primary_lang
                
            total_contrib = contributor_data.get('total_contributors', 0)
            active_contrib = contributor_data.get('active_contributors', 0)
            
            return {
                "repository_summary": {
                    "content": f"• Repository: {repo_name} - {repo_desc[:100] if repo_desc else 'GitHub repository'}\n• Stars: {stars:,} | Language: {main_lang}\n• This appears to be a {main_lang} project with development focus",
                    "generated_at": datetime.now().isoformat()
                },
                "language_analysis": {
                    "content": f"• Primary Language: {main_lang}\n• Technology Focus: {'Web development' if main_lang in ['JavaScript', 'TypeScript'] else 'Software development'}\n• Language composition indicates modern development practices",
                    "generated_at": datetime.now().isoformat()
                },
                "contribution_patterns": {
                    "content": f"• Total Contributors: {total_contrib}\n• Active Contributors: {active_contrib}\n• Project Scale: {'Large open-source' if total_contrib > 50 else 'Medium-scale' if total_contrib > 10 else 'Small/Personal'} project",
                    "generated_at": datetime.now().isoformat()
                }
            }

    async def _generate_repository_summary(self, repo_data: dict, readme_content: str) -> str:
        """Generate detailed repository summary with bullet points"""
        repo_name = repo_data.get('name', 'Unknown')
        description = repo_data.get('description', '')
        stars = repo_data.get('stargazers_count', 0)
        language = repo_data.get('language', 'Unknown')
        topics = repo_data.get('topics', [])
        
        prompt = f"""
Analyze this GitHub repository and provide a detailed summary in bullet point format:

Repository: {repo_name}
Description: {description}
Primary Language: {language}
Stars: {stars:,}
Topics: {', '.join(topics[:5]) if topics else 'None'}
README snippet: {readme_content[:500] if readme_content else 'No README available'}

Provide a comprehensive repository summary with the following bullet points:
• What this repository is (purpose and functionality)
• Key features and capabilities 
• Target audience or use cases
• Notable achievements (if high stars/popularity)
• Overall assessment of the project

Keep each bullet point detailed but concise. Focus on technical aspects and project significance.
"""
        
        return await self._call_groq_api(prompt)

    async def _generate_language_analysis(self, repo_data: dict, language_data: dict) -> str:
        """Generate detailed language and technology analysis with bullet points"""
        languages = language_data.get('languages', {})
        primary_lang = repo_data.get('language', 'Unknown')
        
        prompt = f"""
Analyze the technology stack and programming languages used in this repository:

Primary Language: {primary_lang}
Language Breakdown: {dict(list(languages.items())[:10]) if languages else 'No data'}

Provide a detailed technical analysis with the following bullet points:
• Technology Stack Overview (what the language choices indicate)
• Development Focus (web, mobile, backend, data science, etc.)
• Architecture Implications (based on language mix)
• Modern Development Practices (type safety, frameworks, etc.)
• Ecosystem and Tooling (what this tech stack enables)

Focus on technical insights about the project's technological approach and development philosophy.
Keep each point informative and specific to the language composition.
"""
        
        return await self._call_groq_api(prompt)

    async def _generate_contribution_patterns(self, repo_data: dict, contributor_data: dict) -> str:
        """Generate detailed contribution and collaboration analysis with bullet points"""
        total_contributors = contributor_data.get('total_contributors', 0)
        active_contributors = contributor_data.get('active_contributors', 0)
        top_contributors = contributor_data.get('top_contributors', [])
        
        # Calculate collaboration metrics
        top_contrib_commits = sum([c.get('commits', 0) for c in top_contributors[:3]])
        avg_commits_per_top = top_contrib_commits / 3 if len(top_contributors) >= 3 else 0
        
        prompt = f"""
Analyze the collaboration and contribution patterns for this repository:

Total Contributors: {total_contributors}
Active Contributors: {active_contributors}
Top Contributors: {len(top_contributors)}
Top 3 Contributors Commits: {top_contrib_commits}
Average Commits (Top 3): {avg_commits_per_top:.0f}

Provide a detailed collaboration analysis with the following bullet points:
• Project Scale and Community Size (what the numbers indicate)
• Collaboration Health (active vs total contributor ratio)
• Development Leadership (concentration of contributions)
• Community Engagement Level (based on contributor patterns)
• Project Maturity Assessment (what this contribution pattern suggests)

Focus on insights about the development community, project governance, and collaboration dynamics.
Make each point specific to the contribution data provided.
"""
        
        return await self._call_groq_api(prompt)
