import asyncio
import httpx
import json
from datetime import datetime

async def test_enhanced_api():
    """Test the enhanced GitHub Analyzer API with real data"""
    base_url = "https://github-analyzer-backend-g300.onrender.com"
    
    print("🧪 Testing Enhanced GitHub Repository Analyzer API\n")
    print("=" * 60)
    
    # Test repositories to analyze
    test_repos = [
        {"owner": "facebook", "repo": "react"},
        {"owner": "microsoft", "repo": "vscode"},
        {"owner": "octocat", "repo": "Hello-World"}
    ]
    
    for repo in test_repos:
        print(f"\n🔍 Testing: {repo['owner']}/{repo['repo']}")
        print("-" * 40)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # Test full analysis
                response = await client.post(
                    f"{base_url}/api/v1/analyze",
                    json=repo
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    print("✅ API Response Structure:")
                    print(f"   Owner: {data.get('owner')}")
                    print(f"   Repo: {data.get('repo')}")
                    
                    # Test Stats
                    stats = data.get('stats', {})
                    print(f"\n📊 Stats:")
                    print(f"   Stars: {stats.get('stars', 0):,}")
                    print(f"   Forks: {stats.get('forks', 0):,}")
                    print(f"   Issues: {stats.get('open_issues', 0):,}")
                    print(f"   License: {stats.get('license', 'N/A')}")
                    
                    # Test Languages
                    languages = data.get('languages', {}).get('languages', {})
                    print(f"\n🔤 Languages:")
                    for lang, percentage in list(languages.items())[:3]:
                        print(f"   {lang}: {percentage}%")
                    
                    # Test Commit Activity
                    commit_activity = data.get('commit_activity', {})
                    weekly_data = commit_activity.get('weekly_data', [])
                    print(f"\n📈 Commit Activity:")
                    print(f"   Total Commits: {commit_activity.get('total_commits', 0):,}")
                    print(f"   Last 30 Days: {commit_activity.get('last_30_days', 0)}")
                    print(f"   Weekly Data Points: {len(weekly_data)}")
                    if weekly_data:
                        print(f"   Sample Week: {weekly_data[0]}")
                        print(f"   Latest Week: {weekly_data[-1] if weekly_data else 'None'}")
                    
                    # Test Contributors
                    contributors = data.get('contributors', {})
                    top_contributors = contributors.get('top_contributors', [])
                    print(f"\n👥 Contributors:")
                    print(f"   Total Contributors: {contributors.get('total_contributors', 0)}")
                    print(f"   Active Contributors: {contributors.get('active_contributors', 0)}")
                    print(f"   Top Contributors: {len(top_contributors)}")
                    for i, contrib in enumerate(top_contributors[:3]):
                        print(f"   #{i+1}: {contrib.get('username')} ({contrib.get('commits')} commits)")
                    
                    # Test AI Insights
                    ai_insights = data.get('ai_insights', {})
                    print(f"\n🤖 AI Insights:")
                    
                    repo_summary = ai_insights.get('repository_summary', {})
                    print(f"   Repository Summary:")
                    print(f"     Content: {repo_summary.get('content', 'N/A')[:100]}...")
                    print(f"     Generated: {repo_summary.get('generated_at', 'N/A')}")
                    
                    lang_analysis = ai_insights.get('language_analysis', {})
                    print(f"   Language Analysis:")
                    print(f"     Content: {lang_analysis.get('content', 'N/A')[:100]}...")
                    print(f"     Generated: {lang_analysis.get('generated_at', 'N/A')}")
                    
                    contrib_patterns = ai_insights.get('contribution_patterns', {})
                    print(f"   Contribution Patterns:")
                    print(f"     Content: {contrib_patterns.get('content', 'N/A')[:100]}...")
                    print(f"     Generated: {contrib_patterns.get('generated_at', 'N/A')}")
                    
                    # Test Links
                    links = data.get('links', {})
                    print(f"\n🔗 Links:")
                    print(f"   Repository: {links.get('repo_url', 'N/A')}")
                    print(f"   Owner: {links.get('owner_url', 'N/A')}")
                    
                    # Save full response for inspection
                    filename = f"test_response_{repo['owner']}_{repo['repo']}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"\n💾 Full response saved to: {filename}")
                    
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60)

async def test_individual_endpoints():
    """Test individual endpoints separately"""
    base_url = "https://github-analyzer-backend-g300.onrender.com"
    owner, repo = "facebook", "react"
    
    print(f"\n🔬 Testing Individual Endpoints for {owner}/{repo}")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test health
        print("\n1. Health Check:")
        try:
            response = await client.get(f"{base_url}/api/v1/health")
            if response.status_code == 200:
                health = response.json()
                print(f"   ✅ Status: {health.get('status')}")
                print(f"   ✅ AI Available: {health.get('ai_available')}")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Test basic stats
        print("\n2. Basic Stats:")
        try:
            response = await client.get(f"{base_url}/api/v1/repo/{owner}/{repo}/stats")
            if response.status_code == 200:
                stats = response.json()
                print(f"   ✅ Stars: {stats.get('stars', 0):,}")
                print(f"   ✅ Created: {stats.get('created_at')}")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Test contributors
        print("\n3. Contributors:")
        try:
            response = await client.get(f"{base_url}/api/v1/repo/{owner}/{repo}/contributors")
            if response.status_code == 200:
                contributors = response.json()
                print(f"   ✅ Total: {contributors.get('total_contributors', 0)}")
                print(f"   ✅ Active: {contributors.get('active_contributors', 0)}")
                top = contributors.get('top_contributors', [])
                if top:
                    print(f"   ✅ Top Contributor: {top[0].get('username')} ({top[0].get('commits')} commits)")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Test commit activity
        print("\n4. Commit Activity:")
        try:
            response = await client.get(f"{base_url}/api/v1/repo/{owner}/{repo}/commits/activity")
            if response.status_code == 200:
                commits = response.json()
                weekly_data = commits.get('weekly_data', [])
                print(f"   ✅ Total Commits: {commits.get('total_commits', 0):,}")
                print(f"   ✅ Last 30 Days: {commits.get('last_30_days', 0)}")
                print(f"   ✅ Weekly Data Points: {len(weekly_data)}")
                if weekly_data:
                    recent_weeks = weekly_data[-3:]  # Last 3 weeks
                    print(f"   ✅ Recent weeks: {recent_weeks}")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

async def create_sample_response_structure():
    """Create a sample response structure for documentation"""
    print("\n📋 Creating Sample Response Structure")
    print("=" * 60)
    
    sample_response = {
        "owner": "facebook",
        "repo": "react", 
        "stats": {
            "stars": 228000,
            "forks": 46500,
            "open_issues": 600,
            "license": "MIT"
        },
        "languages": {
            "languages": {
                "JavaScript": 65.2,
                "TypeScript": 30.1,
                "CSS": 3.5,
                "HTML": 1.2
            }
        },
        "commit_activity": {
            "total_commits": 12000,
            "last_30_days": 45,
            "weekly_data": [
                {"week": "2024-07-01", "commits": 25},
                {"week": "2024-07-08", "commits": 30},
                {"week": "2024-07-15", "commits": 28},
                "# ... 49 more weeks"
            ]
        },
        "contributors": {
            "total_contributors": 1650,
            "active_contributors": 45,
            "top_contributors": [
                {
                    "username": "gaearon",
                    "commits": 1200,
                    "avatar_url": "https://avatars.githubusercontent.com/u/810438?v=4"
                },
                {
                    "username": "sebmarkbage", 
                    "commits": 980,
                    "avatar_url": "https://avatars.githubusercontent.com/u/63648?v=4"
                }
            ]
        },
        "links": {
            "repo_url": "https://github.com/facebook/react",
            "owner_url": "https://github.com/facebook"
        },
        "ai_insights": {
            "repository_summary": {
                "content": "React is a popular JavaScript library for building user interfaces, developed by Facebook. It enables developers to create interactive web applications using a component-based architecture with virtual DOM for optimal performance.",
                "generated_at": "2025-09-03T10:30:00.000000"
            },
            "language_analysis": {
                "content": "This is a modern JavaScript ecosystem project with TypeScript integration, representing a well-structured library with excellent type safety and contemporary web development practices.",
                "generated_at": "2025-09-03T10:30:00.000000"
            },
            "contribution_patterns": {
                "content": "This repository shows healthy collaboration with 1650 total contributors and 45 active maintainers, indicating strong community engagement and sustainable development practices typical of major open-source projects.",
                "generated_at": "2025-09-03T10:30:00.000000"
            }
        }
    }
    
    # Save sample structure
    with open("sample_response_structure.json", 'w', encoding='utf-8') as f:
        json.dump(sample_response, f, indent=2, ensure_ascii=False)
    
    print("✅ Sample response structure saved to: sample_response_structure.json")
    print("\n📋 Response Structure Summary:")
    print("   ✅ Stats: 4 fields (stars, forks, issues, license)")
    print("   ✅ Languages: Dictionary with percentages")
    print("   ✅ Commit Activity: Total + 30-day + weekly data array")
    print("   ✅ Contributors: Total, active, top 5 with avatars")
    print("   ✅ AI Insights: 3 separate insights with timestamps")
    print("   ✅ Links: Repository and owner URLs")

async def main():
    """Run all tests"""
    print("🚀 GitHub Analyzer Backend - Enhanced API Testing")
    print("=" * 60)
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test the enhanced API
    await test_enhanced_api()
    
    # Test individual endpoints
    await test_individual_endpoints()
    
    # Create sample structure
    await create_sample_response_structure()
    
    print(f"\n🏁 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
