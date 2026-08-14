# GitHub Analyzer

A Java code-review project with a React frontend and a FastAPI backend. It uses Groq to generate an AI review with a quality score, summary, and actionable issues.

## Features

<<<<<<< HEAD
1. Receives Java source files through the `/analyze` endpoint .
2. Keeps `.java` files only.
3. Creates a clear code-review prompt.
4. Sends the prompt to an AI model.
5. Returns a score, summary, and list of code issues.
=======
- Paste Java source code into the editor.
- Upload a local `.java` file.
- Analyze a public GitHub repository URL.
- Review up to 20 Java files from the repository's default branch.
- Receive issue severity, file path, line number, suggestion, and confidence.

## Project structure

```text
projectfinal/
├── ai-service/                 # FastAPI backend
│   ├── app.py                  # API routes and CORS configuration
│   ├── requirements.txt        # Python dependencies
│   ├── models/schemas.py       # Request and response models
│   └── services/
│       ├── analyzer.py         # Analysis workflow
│       ├── github_service.py   # Public GitHub repository downloader
│       ├── llm_service.py      # Groq API client
│       ├── parser.py           # Java-file filter
│       └── prompt_builder.py   # AI review prompt
└── frontend/                   # React + Vite frontend
    └── src/App.jsx             # Upload, paste, GitHub URL, and results UI
```

## Requirements

- Python 3.11 or newer
- Node.js 18 or newer
- A Groq API key

## Backend setup

```powershell
cd ai-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `ai-service/.env.example` to `ai-service/.env`, then add your Groq key:

```env
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile
```

Optional: add a GitHub token to raise GitHub API rate limits:

```env
GITHUB_TOKEN=your-github-token
```

Start the backend:

```powershell
uvicorn app:app --reload --port 8001
```

- API health check: [http://127.0.0.1:8001/health](http://127.0.0.1:8001/health)
- API documentation: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

The address `http://127.0.0.1:8001/` itself intentionally returns `{"detail":"Not Found"}` because the backend exposes API routes only.

## Frontend setup

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). Keep the backend running while using the frontend.

## Using the application

### Analyze a Java file

1. Choose **Paste or upload**.
2. Upload a `.java` file or paste code into the source-code box.
3. Select **Analyze code**.

### Analyze a GitHub repository

1. Choose **GitHub URL**.
2. Enter a public repository URL in this format:

   ```text
   https://github.com/owner/repository
   ```

3. Select **Analyze repository**.

Private repositories are not supported yet. The backend downloads at most 20 `.java` files and sends them to Groq for review.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check that the backend is running. |
| `POST` | `/analyze` | Analyze supplied Java files. |
| `POST` | `/analyze/github` | Download and analyze a public GitHub repository. |

Example GitHub request:

```json
{
  "repository_url": "https://github.com/owner/repository"
}
```

## Troubleshooting

- **“Failed to fetch”**: start the backend on port `8001`, then refresh the frontend. The frontend must use `http://127.0.0.1:5173` or `http://localhost:5173`.
- **“Could not connect to GitHub”**: check your internet connection and that the repository is public. Add `GITHUB_TOKEN` if you have reached GitHub's rate limit.
- **No AI review**: set a valid `GROQ_API_KEY` in `ai-service/.env`, then restart the backend.
