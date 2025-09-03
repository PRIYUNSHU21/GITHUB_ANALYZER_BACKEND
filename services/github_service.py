import httpx
from typing import Dict, Any, Optional
from config.settings import settings

class GitHubService:
    def __init__(self):
        self.base_url = settings.GITHUB_API_BASE_URL
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Analyzer/1.0"
        }
        
        # Add GitHub token if available (for higher rate limits)
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"
    
    async def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get basic repository information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get repository language breakdown"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/languages",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_commit_activity(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository commit activity (last 30 days)"""
        async with httpx.AsyncClient() as client:
            try:
                # Get commits from last 30 days
                from datetime import datetime, timedelta
                since_date = (datetime.now() - timedelta(days=30)).isoformat()
                
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/commits",
                    headers=self.headers,
                    params={"since": since_date, "per_page": 100}
                )
                
                recent_commits = 0
                if response.status_code == 200:
                    commits = response.json()
                    recent_commits = len(commits)
                
                # Try to get total commit count
                total_commits = 0
                try:
                    stats_response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}/stats/participation",
                        headers=self.headers
                    )
                    
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        total_commits = sum(stats.get("all", []))
                except:
                    # If stats API fails, estimate from recent commits
                    total_commits = recent_commits * 10  # rough estimate
                
                return {
                    "total_commits": total_commits,
                    "recent_commits": recent_commits
                }
            except Exception:
                return {
                    "total_commits": 0,
                    "recent_commits": 0
                }
    
    async def get_repo_readme(self, owner: str, repo: str) -> str:
        """Get repository README content"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/readme",
                    headers=self.headers
                )
                if response.status_code == 200:
                    readme_data = response.json()
                    # Get the actual content from download_url
                    content_response = await client.get(readme_data["download_url"])
                    if content_response.status_code == 200:
                        return content_response.text
                return "README not available"
            except Exception:
                return "README not available"
