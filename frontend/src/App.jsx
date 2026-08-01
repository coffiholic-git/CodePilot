import { useState } from "react";

const apiUrl = import.meta.env.VITE_AI_API_URL || "http://localhost:8001";

const exampleCode = `public class UserService {
    public String findUser(String userId) {
        return "User: " + userId;
    }
}`;

function App() {
  const [filePath, setFilePath] = useState("src/main/java/com/example/UserService.java");
  const [code, setCode] = useState(exampleCode);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function analyzeCode(event) {
    event.preventDefault();
    setError("");
    setAnalysis(null);
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          files: [{ path: filePath, content: code }]
        })
      });

      if (!response.ok) {
        throw new Error("The AI service could not analyze the code.");
      }

      setAnalysis(await response.json());
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">AI CODE REVIEW</p>
        <h1>GitHub Analyzer</h1>
        <p className="intro">
          Paste a Java file and receive an AI-generated review with a score, summary, and practical improvements.
        </p>
      </section>

      <section className="workspace">
        <form className="editor-card" onSubmit={analyzeCode}>
          <div className="card-header">
            <h2>Java file</h2>
            <span className="language-badge">JAVA</span>
          </div>

          <label htmlFor="filePath">File path</label>
          <input
            id="filePath"
            value={filePath}
            onChange={(event) => setFilePath(event.target.value)}
            required
          />

          <label htmlFor="code">Source code</label>
          <textarea
            id="code"
            value={code}
            onChange={(event) => setCode(event.target.value)}
            spellCheck="false"
            required
          />

          <button type="submit" disabled={isLoading}>
            {isLoading ? "Analyzing..." : "Analyze code"}
          </button>
        </form>

        <section className="results-card" aria-live="polite">
          <div className="card-header">
            <h2>Analysis result</h2>
          </div>

          {!analysis && !error && (
            <p className="empty-state">Your AI review will appear here.</p>
          )}

          {error && <p className="error-message">{error}</p>}

          {analysis && <AnalysisResult analysis={analysis} />}
        </section>
      </section>
    </main>
  );
}

function AnalysisResult({ analysis }) {
  return (
    <div className="analysis">
      <div className="score-row">
        <div className="score-circle">{analysis.score ?? "-"}</div>
        <div>
          <p className="muted-label">QUALITY SCORE</p>
          <p className="summary">{analysis.summary}</p>
        </div>
      </div>

      <h3>Issues ({analysis.issues.length})</h3>
      {analysis.issues.length === 0 && <p className="empty-state">No issues were returned.</p>}

      <div className="issue-list">
        {analysis.issues.map((issue, index) => (
          <article className="issue" key={`${issue.filePath}-${issue.line}-${index}`}>
            <div className="issue-topline">
              <span className={`severity ${issue.severity.toLowerCase()}`}>{issue.severity}</span>
              <span>{issue.filePath}{issue.line ? ` : line ${issue.line}` : ""}</span>
            </div>
            <p>{issue.message}</p>
            {issue.suggestion && <p className="suggestion">Suggestion: {issue.suggestion}</p>}
          </article>
        ))}
      </div>
    </div>
  );
}

export default App;
