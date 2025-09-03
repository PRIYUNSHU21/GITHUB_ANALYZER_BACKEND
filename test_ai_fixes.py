import asyncio
import httpx
import json

async def test_ai_service_fixes():
    """Test the fixed AI service with rate limiting"""
    base_url = "https://github-analyzer-backend-g300.onrender.com"
    
    print("🧪 Testing Fixed AI Service (Rate Limiting)")
    print("=" * 50)
    
    # Test with a repository that had issues
    test_repo = {"owner": "octocat", "repo": "Hello-World"}
    
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:  # Longer timeout for AI processing
            print(f"🔍 Testing: {test_repo['owner']}/{test_repo['repo']}")
            print("⏱️  This may take a moment due to rate limiting delays...")
            
            response = await client.post(
                f"{base_url}/api/v1/analyze",
                json=test_repo
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ API Response received!")
                
                # Check AI insights specifically
                ai_insights = data.get('ai_insights', {})
                
                print(f"\n🤖 AI Insights Results:")
                print("-" * 30)
                
                # Repository Summary
                repo_summary = ai_insights.get('repository_summary', {})
                content = repo_summary.get('content', 'No content')
                print(f"📝 Repository Summary:")
                print(f"   Content: {content[:100]}...")
                print(f"   Has Error: {'AI service error' in content}")
                print(f"   Generated: {repo_summary.get('generated_at', 'N/A')}")
                
                # Language Analysis
                lang_analysis = ai_insights.get('language_analysis', {})
                content = lang_analysis.get('content', 'No content')
                print(f"\n🔤 Language Analysis:")
                print(f"   Content: {content[:100]}...")
                print(f"   Has Error: {'AI service error' in content}")
                print(f"   Generated: {lang_analysis.get('generated_at', 'N/A')}")
                
                # Contribution Patterns
                contrib_patterns = ai_insights.get('contribution_patterns', {})
                content = contrib_patterns.get('content', 'No content')
                print(f"\n👥 Contribution Patterns:")
                print(f"   Content: {content[:100]}...")
                print(f"   Has Error: {'AI service error' in content}")
                print(f"   Generated: {contrib_patterns.get('generated_at', 'N/A')}")
                
                # Check if any still have errors
                errors = sum([
                    'AI service error' in repo_summary.get('content', ''),
                    'AI service error' in lang_analysis.get('content', ''),
                    'AI service error' in contrib_patterns.get('content', '')
                ])
                
                if errors == 0:
                    print(f"\n🎉 SUCCESS: All AI insights generated without errors!")
                else:
                    print(f"\n⚠️  {errors}/3 insights still have errors")
                
                # Save the response
                with open("test_fixed_ai_response.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Full response saved to: test_fixed_ai_response.json")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

async def test_multiple_repos():
    """Test multiple repos to ensure rate limiting works"""
    base_url = "https://github-analyzer-backend-g300.onrender.com"
    
    print(f"\n🔄 Testing Multiple Repositories (Rate Limiting)")
    print("=" * 50)
    
    test_repos = [
        {"owner": "octocat", "repo": "Hello-World"},
        {"owner": "microsoft", "repo": "vscode"},
    ]
    
    for i, repo in enumerate(test_repos):
        print(f"\n{i+1}. Testing: {repo['owner']}/{repo['repo']}")
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    f"{base_url}/api/v1/analyze",
                    json=repo
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_insights = data.get('ai_insights', {})
                    
                    # Quick check for errors
                    errors = sum([
                        'AI service error' in ai_insights.get('repository_summary', {}).get('content', ''),
                        'AI service error' in ai_insights.get('language_analysis', {}).get('content', ''),
                        'AI service error' in ai_insights.get('contribution_patterns', {}).get('content', '')
                    ])
                    
                    print(f"   ✅ Response received, Errors: {errors}/3")
                    
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
        
        # Add delay between tests
        if i < len(test_repos) - 1:
            print("   ⏱️  Waiting before next test...")
            await asyncio.sleep(2)

async def main():
    print("🚀 Testing AI Service Rate Limiting Fixes")
    print("=" * 50)
    
    await test_ai_service_fixes()
    await test_multiple_repos()
    
    print(f"\n🏁 Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
