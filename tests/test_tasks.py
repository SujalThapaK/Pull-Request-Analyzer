import pytest
from app.tasks import analyze_pr  # Replace with the actual import path of your Celery task

@pytest.fixture
def mock_pr_payload():
    return {
        "repo_url": "https://github.com/user/repo",
        "pr_number": 123,
        "github_token": "optional_token",
    }

def test_analyze_pr_task(mock_pr_payload):
    # Call the task synchronously for testing
    result = analyze_pr(mock_pr_payload)
    assert "files" in result
    assert "summary" in result
    assert isinstance(result["summary"]["total_files"], int)
    assert isinstance(result["summary"]["total_issues"], int)