import httpx
import asyncio
import json

async def test_api():
    """Test the GitHub Analyzer API"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing GitHub Repository Analyzer API\n")
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/api/v1/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    
    # Test basic stats endpoint
    print("2. Testing basic stats endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/api/v1/repo/microsoft/vscode/stats")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Stars: {data.get('stars', 'N/A')}")
                print(f"   Forks: {data.get('forks', 'N/A')}")
                print(f"   Issues: {data.get('open_issues', 'N/A')}")
                print(f"   License: {data.get('license', 'N/A')}\n")
            else:
                print(f"   Error: {response.text}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    
    # Test full analysis endpoint
    print("3. Testing full analysis endpoint...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{base_url}/api/v1/analyze",
                json={"owner": "facebook", "repo": "react"}
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Repository: {data['owner']}/{data['repo']}")
                print(f"   Stars: {data['stats']['stars']}")
                print(f"   Languages: {list(data['languages']['languages'].keys())[:3]}")
                print(f"   AI Summary: {data['ai_insight']['summary'][:100]}...")
                print(f"   Repo URL: {data['links']['repo_url']}\n")
            else:
                print(f"   Error: {response.text}\n")
        except Exception as e:
            print(f"   Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_api())
