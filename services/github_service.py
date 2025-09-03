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
        """Get repository commit activity with weekly breakdown"""
        async with httpx.AsyncClient() as client:
            try:
                from datetime import datetime, timedelta
                
                # Get commit activity stats (52 weeks)
                stats_response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/stats/commit_activity",
                    headers=self.headers
                )
                
                weekly_data = []
                total_commits = 0
                
                if stats_response.status_code == 200:
                    commit_stats = stats_response.json()
                    
                    # Process weekly data (GitHub provides last 52 weeks)
                    for week_data in commit_stats:
                        week_timestamp = week_data.get("week", 0)
                        commits = week_data.get("total", 0)
                        
                        if week_timestamp:
                            week_date = datetime.fromtimestamp(week_timestamp)
                            weekly_data.append({
                                "week": week_date.strftime("%Y-%m-%d"),
                                "commits": commits
                            })
                            total_commits += commits
                
                # Get recent commits for last 30 days count
                since_date = (datetime.now() - timedelta(days=30)).isoformat()
                recent_response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/commits",
                    headers=self.headers,
                    params={"since": since_date, "per_page": 100}
                )
                
                recent_commits = 0
                if recent_response.status_code == 200:
                    recent_commits = len(recent_response.json())
                
                return {
                    "total_commits": total_commits or 0,
                    "last_30_days": recent_commits,
                    "weekly_data": weekly_data[-52:]  # Last 52 weeks
                }
                
            except Exception:
                return {
                    "total_commits": 0,
                    "last_30_days": 0,
                    "weekly_data": []
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
    
    async def get_contributors(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository contributor statistics"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contributors",
                    headers=self.headers,
                    params={"per_page": 100}
                )
                
                if response.status_code == 200:
                    contributors = response.json()
                    
                    total_contributors = len(contributors)
                    # Consider contributors with 5+ contributions as active
                    active_contributors = len([c for c in contributors if c.get("contributions", 0) >= 5])
                    
                    # Get top 5 contributors
                    top_contributors = [
                        {
                            "username": contrib.get("login", "Unknown"),
                            "commits": contrib.get("contributions", 0),
                            "avatar_url": contrib.get("avatar_url", "")
                        }
                        for contrib in contributors[:5]
                    ]
                    
                    return {
                        "total_contributors": total_contributors,
                        "active_contributors": active_contributors,
                        "top_contributors": top_contributors
                    }
                
                return {
                    "total_contributors": 0,
                    "active_contributors": 0,
                    "top_contributors": []
                }
            except Exception:
                return {
                    "total_contributors": 0,
                    "active_contributors": 0,
                    "top_contributors": []
                }
