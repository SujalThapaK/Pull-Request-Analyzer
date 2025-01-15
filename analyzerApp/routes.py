from fastapi import APIRouter
from analyzerApp.tasks import analyze_pr
from celery.result import AsyncResult
from analyzerApp.db import get_task_result
import os

router = APIRouter()

@router.post("/analyze-pr")
async def analyze_pr_endpoint(repo_url: str, pr_number: int, opMode: int):
    task = analyze_pr.delay(repo_url, pr_number, opMode)
    return {"task_id": task.id}

@router.get("/status/{task_id}")
async def check_status(task_id: str):
    result = AsyncResult(task_id)
    if result.state == "PENDING":
        return {"task_id": task_id, "status": "Pending", "result": None}
    elif result.state == "SUCCESS":
        return {"task_id": task_id, "status": "Success"}
    elif result.state == "FAILURE":
        return {"task_id": task_id, "status": "Failed", "error": str(result.result)}
    else:
        return {"task_id": task_id, "status": result.state}

@router.get("/results/{task_id}")
async def get_results(task_id: str):
    result = get_task_result(task_id)
    if result:
        return result
    return {"error": "Result not found"}
