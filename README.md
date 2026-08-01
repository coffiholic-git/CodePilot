# GitHub Analyzer AI Service

This project contains only the AI analysis service. It is a beginner-friendly Python/FastAPI API that reviews Java files using an OpenAI-compatible AI provider.

## What it does

1. Receives Java source files through the `/analyze` endpoint.
2. Keeps `.java` files only.
3. Creates a clear code-review prompt.
4. Sends the prompt to an AI model.
5. Returns a score, summary, and list of code issues.

Each issue can include a file path, severity, line number, explanation, suggestion, and confidence score.

## Folder structure

```text
ai-service/
├── app.py                     # Starts the FastAPI application
├── requirements.txt           # Python dependencies
├── models/
│   └── schemas.py             # Request and response models
├── services/
│   ├── analyzer.py            # Runs the complete analysis workflow
│   ├── parser.py              # Keeps Java files only
│   ├── prompt_builder.py      # Builds the prompt sent to the AI
│   ├── llm_service.py         # Calls the AI provider
│   └── github_service.py      # Placeholder for future GitHub API support
└── utils/
    └── file_utils.py          # Small file helper functions
```

## Setup

Requirements: Python 3.11 or newer and an OpenAI-compatible API key.

```powershell
cd ai-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set your AI provider key:

```powershell
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_MODEL="gpt-4o-mini"
```

Start the service:

```powershell
uvicorn app:app --reload --port 8001
```

Open `http://127.0.0.1:8001/docs` to test the API in the browser.

## API

### Health check

```http
GET /health
```

### Analyze Java code

```http
POST /analyze
Content-Type: application/json
```

```json
{
  "files": [
    {
      "path": "src/main/java/com/example/UserService.java",
      "content": "public class UserService { }"
    }
  ]
}
```

## Future improvements

- Connect directly to the GitHub API using `github_service.py`.
- Support more languages such as Python, JavaScript, and TypeScript.
- Add static code checks before calling the AI.
- Save analysis history in a database.

## React frontend

The React frontend is in [`frontend/`](frontend/). It lets you paste a Java file, send it to the AI service, and see the review result.

Start the AI service first, then run the frontend in another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the address shown by Vite, normally `http://localhost:5173`.
