import requests

def fetch_pr_details(repo_url, pr_number, token=None):
    print(f"{repo_url}/pull/{pr_number}/files")
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(f"{repo_url}/pull/{pr_number}/files", headers=headers)
    print(f"Rate limit remaining: {response.headers.get('X-RateLimit-Remaining')}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    if response.status_code != 200:
        return {"error": f"Request failed with status {response.status_code}: {response.text}"}
    else:
        print("Okay")
    return response.json()
