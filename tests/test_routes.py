import pytest
from fastapi.testclient import TestClient
from analyzerApp.main import app  # Replace with the actual import path of your FastAPI app

client = TestClient(app)

@pytest.fixture
def mock_pr_payload():
    return {
        "repo_url": "https://github.com/user/repo",
        "pr_number": 123,
        "github_token": "optional_token",
    }

def test_analyze_pr(mock_pr_payload):
    response = client.post("/analyze-pr", json=mock_pr_payload)
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_status_endpoint():
    task_id = "dummy-task-id"  # Replace with a valid task ID during integration tests
    response = client.get(f"/status/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] in ["pending", "processing", "completed", "failed"]

def test_results_endpoint():
    task_id = "dummy-task-id"  # Replace with a valid task ID during integration tests
    response = client.get(f"/results/{task_id}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "results" in response.json()