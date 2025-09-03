from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class GitHubRepoRequest(BaseModel):
    owner: str
    repo: str

class RepoStats(BaseModel):
    stars: int
    forks: int
    open_issues: int
    license: Optional[str]
    
class LanguageData(BaseModel):
    languages: Dict[str, float]  # language: percentage
    
class CommitActivity(BaseModel):
    total_commits: int
    last_30_days: int
    
class RepoLinks(BaseModel):
    repo_url: str
    owner_url: str
    
class AIInsight(BaseModel):
    summary: str
    generated_at: datetime
    
class GitHubRepoResponse(BaseModel):
    owner: str
    repo: str
    stats: RepoStats
    languages: LanguageData
    commit_activity: CommitActivity
    links: RepoLinks
    ai_insight: AIInsight
    
class ErrorResponse(BaseModel):
    error: str
    message: str
