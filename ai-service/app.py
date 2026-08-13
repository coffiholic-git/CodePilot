import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import AnalyzeRequest, AnalyzeResponse, GitHubRepositoryRequest
from services.analyzer import analyze_repository
from services.github_service import get_java_files_from_github

app = FastAPI(title="GitHub Analyzer AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "http://127.0.0.1:5177",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    return await analyze_repository(request.files)

@app.post("/analyze/github", response_model=AnalyzeResponse)
async def analyze_github_repository(request: GitHubRepositoryRequest):
    try:
        files = await get_java_files_from_github(request.repository_url)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            detail = "Repository not found. Make sure the URL is public and correct."
        else:
            detail = "GitHub could not provide the repository files. Try again later."
        raise HTTPException(status_code=error.response.status_code, detail=detail) from error
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail="Could not connect to GitHub.") from error

    return await analyze_repository(files)
