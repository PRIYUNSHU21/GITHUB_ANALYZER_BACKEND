from fastapi import APIRouter, HTTPException
from models.schemas import GitHubRepoRequest, GitHubRepoResponse, ErrorResponse
from services.github_service import GitHubService
from services.ai_service import AIService
from datetime import datetime
import asyncio

router = APIRouter(prefix="/api/v1", tags=["GitHub Analysis"])

github_service = GitHubService()
ai_service = AIService()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_available": ai_service.is_available()
    }

@router.post("/analyze", response_model=GitHubRepoResponse)
async def analyze_repository(request: GitHubRepoRequest):
    """Analyze a GitHub repository and return comprehensive data"""
    try:
        # Fetch all GitHub data concurrently
        repo_info_task = github_service.get_repo_info(request.owner, request.repo)
        languages_task = github_service.get_repo_languages(request.owner, request.repo)
        commits_task = github_service.get_commit_activity(request.owner, request.repo)
        readme_task = github_service.get_repo_readme(request.owner, request.repo)
        contributors_task = github_service.get_contributors(request.owner, request.repo)
        
        # Wait for all tasks to complete
        repo_info, languages_raw, commit_data, readme_content, contributor_data = await asyncio.gather(
            repo_info_task, languages_task, commits_task, readme_task, contributors_task,
            return_exceptions=True
        )
        
        # Handle errors
        if isinstance(repo_info, Exception):
            raise HTTPException(status_code=404, detail="Repository not found")
        
        # Process language data
        if isinstance(languages_raw, Exception):
            languages_raw = {}
            
        total_bytes = sum(languages_raw.values()) if languages_raw else 1
        language_percentages = {
            lang: round((bytes_count / total_bytes) * 100, 2)
            for lang, bytes_count in languages_raw.items()
        } if languages_raw else {"Unknown": 100.0}
        
        # Process commit data
        if isinstance(commit_data, Exception):
            commit_data = {
                "total_commits": 0, 
                "last_30_days": 0,
                "weekly_data": []
            }
        
        # Process contributor data
        if isinstance(contributor_data, Exception):
            contributor_data = {
                "total_contributors": 0,
                "active_contributors": 0,
                "top_contributors": []
            }
        
        # Process README
        if isinstance(readme_content, Exception):
            readme_content = "README not available"
        
        # Generate enhanced AI insights
        ai_insights = await ai_service.generate_three_insights(
            repo_info, readme_content, {"languages": language_percentages}, contributor_data
        )
        
        # Build response with enhanced structure
        response = GitHubRepoResponse(
            owner=request.owner,
            repo=request.repo,
            stats={
                "stars": repo_info.get("stargazers_count", 0),
                "forks": repo_info.get("forks_count", 0),
                "open_issues": repo_info.get("open_issues_count", 0),
                "license": repo_info.get("license", {}).get("name") if repo_info.get("license") else None
            },
            languages={
                "languages": language_percentages
            },
            commit_activity={
                "total_commits": commit_data.get("total_commits", 0),
                "last_30_days": commit_data.get("last_30_days", 0),
                "weekly_data": [
                    {"week": week["week"], "commits": week["commits"]}
                    for week in commit_data.get("weekly_data", [])
                ]
            },
            contributors={
                "total_contributors": contributor_data.get("total_contributors", 0),
                "active_contributors": contributor_data.get("active_contributors", 0),
                "top_contributors": [
                    {
                        "username": contrib["username"],
                        "commits": contrib["commits"],
                        "avatar_url": contrib["avatar_url"]
                    }
                    for contrib in contributor_data.get("top_contributors", [])
                ]
            },
            links={
                "repo_url": repo_info.get("html_url", f"https://github.com/{request.owner}/{request.repo}"),
                "owner_url": repo_info.get("owner", {}).get("html_url", f"https://github.com/{request.owner}")
            },
            ai_insights=ai_insights
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/repo/{owner}/{repo}/stats")
async def get_basic_stats(owner: str, repo: str):
    """Get basic repository statistics only"""
    try:
        repo_info = await github_service.get_repo_info(owner, repo)
        return {
            "stars": repo_info.get("stargazers_count", 0),
            "forks": repo_info.get("forks_count", 0),
            "open_issues": repo_info.get("open_issues_count", 0),
            "license": repo_info.get("license", {}).get("name") if repo_info.get("license") else None,
            "created_at": repo_info.get("created_at"),
            "updated_at": repo_info.get("updated_at")
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Repository not found")

@router.get("/repo/{owner}/{repo}/contributors")
async def get_contributors(owner: str, repo: str):
    """Get repository contributor information"""
    try:
        contributor_data = await github_service.get_contributors(owner, repo)
        return contributor_data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Repository not found")

@router.get("/repo/{owner}/{repo}/commits/activity")
async def get_commit_activity(owner: str, repo: str):
    """Get detailed commit activity with weekly breakdown"""
    try:
        commit_data = await github_service.get_commit_activity(owner, repo)
        return commit_data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Repository not found")
