from pydantic import BaseModel, Field


class SourceFile(BaseModel):
    path: str
    content: str


class AnalyzeRequest(BaseModel):
    files: list[SourceFile] = Field(min_length=1)


class Issue(BaseModel):
    filePath: str
    severity: str
    line: int | None = None
    message: str
    suggestion: str | None = None
    confidence: int | None = None


class AnalyzeResponse(BaseModel):
    score: int | None = None
    summary: str
    issues: list[Issue]
