from celery_config import app
from github import Github
from analyzerApp.agent import analyze_code
from analyzerApp.db import store_result
import os


@app.task(bind=True)
def analyze_pr(self, repo_url, pr_number, opMode):
    try:
        print("Fetching GitHub data...")
        github_pat = os.environ['Github_PAT']  # Fetch the GitHub personal access token from environment variables
        g = Github(github_pat)

        # Extract repo owner and name from the repo_url
        repo_owner, repo_name = repo_url.split('/')[-2:]  # Assuming format is "https://github.com/owner/repo"
        repo = g.get_repo(f"{repo_owner}/{repo_name}")

        # Get the specific pull request by number
        pull_request = repo.get_pull(pr_number)
        print(f"Analyzing Pull Request #{pr_number} - {pull_request.title}")

        # Get files changed in the pull request
        files = pull_request.get_files()
        pr_files = []

        for file in files:
            print(f"File: {file.filename}")
            patch_content = file.patch
            patch_lines = patch_content.split('\n')

            # Extract added lines
            added_lines = [line[2:] for line in patch_lines if line.startswith('+') and not line.startswith('+++')]

            # Store each file's added lines as a dict for further processing
            pr_files.append({"filename": file.filename, "Patch File": {patch_content}, "added_lines": added_lines})
        # Analyze the code changes
        results = analyze_code(pr_files,opMode)
        store_result(self.request.id, results)
        print("\nEverything done accordingly well.")
        return results
    except Exception as e:
        return {"TrueError": str(e)}
