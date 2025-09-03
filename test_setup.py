import asyncio
import httpx
from services.github_service import GitHubService
from services.ai_service import AIService

async def test_setup():
    print("🧪 Testing GitHub Analyzer Backend Setup...")
    
    # Test 1: GitHub Service
    print("\n1. Testing GitHub Service...")
    github_service = GitHubService()
    try:
        repo_info = await github_service.get_repo_info("octocat", "Hello-World")
        print(f"✅ GitHub API: {repo_info['name']} - {repo_info['stargazers_count']} stars")
    except Exception as e:
        print(f"❌ GitHub service failed: {e}")
        return
    
    # Test 2: AI Service
    print("\n2. Testing AI Service...")
    ai_service = AIService()
    if ai_service.is_available():
        try:
            test_repo = {"name": "Test", "description": "A test repository", "language": "Python", "stargazers_count": 100}
            summary = await ai_service.generate_repo_summary(test_repo, "This is a test README file for a Python project.")
            print(f"✅ AI Service: Generated {len(summary)} character summary")
            print(f"📝 Sample: {summary[:100]}...")
        except Exception as e:
            print(f"❌ AI service failed: {e}")
    else:
        print("❌ AI service not configured")
    
    print("\n✅ Setup test completed! Now starting the server...")

if __name__ == "__main__":
    asyncio.run(test_setup())
