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
        
        # Wait for all tasks to complete
        repo_info, languages_raw, commit_data, readme_content = await asyncio.gather(
            repo_info_task, languages_task, commits_task, readme_task,
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
            commit_data = {"total_commits": 0, "recent_commits": 0}
        
        # Generate AI summary
        ai_summary = "AI summary not available"
        if not isinstance(readme_content, Exception):
            ai_summary = await ai_service.generate_repo_summary(repo_info, readme_content)
        
        # Build response
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
                "last_30_days": commit_data.get("recent_commits", 0)
            },
            links={
                "repo_url": repo_info.get("html_url", f"https://github.com/{request.owner}/{request.repo}"),
                "owner_url": repo_info.get("owner", {}).get("html_url", f"https://github.com/{request.owner}")
            },
            ai_insight={
                "summary": ai_summary,
                "generated_at": datetime.now()
            }
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
