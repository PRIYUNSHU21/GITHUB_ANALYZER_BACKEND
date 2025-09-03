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

class WeeklyCommitData(BaseModel):
    week: str
    commits: int

class CommitActivity(BaseModel):
    total_commits: int
    last_30_days: int
    weekly_data: List[WeeklyCommitData]

class TopContributor(BaseModel):
    username: str
    commits: int
    avatar_url: str

class ContributorData(BaseModel):
    total_contributors: int
    active_contributors: int
    top_contributors: List[TopContributor]
    
class RepoLinks(BaseModel):
    repo_url: str
    owner_url: str

class AIInsightItem(BaseModel):
    content: str
    generated_at: str

class AIInsights(BaseModel):
    repository_summary: AIInsightItem
    language_analysis: AIInsightItem
    contribution_patterns: AIInsightItem
    
class GitHubRepoResponse(BaseModel):
    owner: str
    repo: str
    stats: RepoStats
    languages: LanguageData
    commit_activity: CommitActivity
    contributors: ContributorData
    links: RepoLinks
    ai_insights: AIInsights
    
class ErrorResponse(BaseModel):
    error: str
    message: str
