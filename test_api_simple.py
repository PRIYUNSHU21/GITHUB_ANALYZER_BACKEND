import requests
import json

def test_api():
    print("🧪 Testing GitHub Analyzer API...\n")
    
    try:
        # Test health endpoint
        print("1. Testing Health Check...")
        response = requests.get("http://localhost:8000/api/v1/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        # Test basic stats
        print("2. Testing Basic Stats...")
        response = requests.get("http://localhost:8000/api/v1/repo/microsoft/vscode/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"VS Code Stats:")
            print(f"  Stars: {data['stars']}")
            print(f"  Forks: {data['forks']}")
            print(f"  Issues: {data['open_issues']}")
            print(f"  License: {data['license']}\n")
        
        # Test full analysis
        print("3. Testing Full Analysis...")
        response = requests.post(
            "http://localhost:8000/api/v1/analyze",
            json={"owner": "octocat", "repo": "Hello-World"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Analysis Results:")
            print(f"  Repository: {data['owner']}/{data['repo']}")
            print(f"  Stars: {data['stats']['stars']}")
            print(f"  Languages: {list(data['languages']['languages'].keys())}")
            print(f"  AI Summary: {data['ai_insight']['summary'][:150]}...")
            print(f"  Repository URL: {data['links']['repo_url']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
