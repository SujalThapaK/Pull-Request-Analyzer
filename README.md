<h1>Pull Request Analyzer</h1>
A Python API for analyzing the files and changes contained within a pull request using LLMs (Gemini 1.5).

Publicly accessible on: http://34.45.213.142:8000/
<br><br>
<hr>
<p float="left">
  <img src="https://github.com/user-attachments/assets/28a3c3be-d7ec-431b-9077-29824c03271b" width="30%" />
  <img src="https://github.com/user-attachments/assets/97535e71-8c5d-48c1-b61b-7e530e488a9e" width="40%" />
  <img src="https://github.com/user-attachments/assets/ae6866aa-13e9-4866-8327-3c2a8f59e315" width="20%" />
</p>
<b>POST, GET (Results) and GET (Status) screenshots shown above.</b>
<hr>
<b>POST /analyze-pr:</b><br>
Accepts GitHub PR details (repo, PR number) and specifies the operation mode. An example request is given below:

```
http://34.45.213.142:8000/analyze-pr?repo_url=https://github.com/caching-tools/next-shared-cache&pr_number=933&opMode=2
```

The request returns a ``"task_id"`` which can be used to check the status and result of the analysis.
<br><br>
<b>GET /status/<task_id></b>: 
<br>Checks the status of the given analysis ``task_id``. An example request is given below:

```
http://34.45.213.142:8000/status/1b8e182c-53a8-4e30-9925-d7b27e60dab1
```

The status values range from ``"success"``, ``"pending"`` and ``"failed"``.
<br><br>
<b>GET /results/<task_id></b>: 
<br>Returns the result for the given analysis ``task_id``. An example request is given below:

```
http://34.45.213.142:8000/results/1b8e182c-53a8-4e30-9925-d7b27e60dab1
```

The nature of the response will be dependent on the Operation Mode specified in the POST request. The different operation modes are:<br><br>
``0``: A balance between analysis and code, both lists out potential issues with the code and also provides the code to fix the issues.<br>
``1``: Less focus on theoretical analysis, it focuses on identifying issues and providing us with the code to solve them.<br>
``2``: More focus on theoretical analysis, providing detailed descriptions of the issues.<br>
<br>
<hr>
<b>Setup and run:</b>
<br>
1. Download the project, and open a terminal on the root folder.<br>
2. Install Docker and Docker-Compose (if not present alrady).<br>
3. Create a .env file with two parameters, similar to the one shown below:

```
Github_PAT={insert_GitHub_PersonalAccessToken_Here}
GOOGLE_API_KEY={insert_Google_API_Key_here}
```
4. Run the following command:

```
docker-compose --env-file .env up --build
```
<hr>

Built as an assignment for [PotPieAI](https://potpie.ai/) using:
- Python 3.11
- Langchain
- Celery
- Redis
- FastAPI

And deployed as a containerized VM using:
- Docker
- Google Compute Engine
