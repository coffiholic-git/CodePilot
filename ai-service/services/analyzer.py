from models.schemas import AnalyzeResponse, Issue, SourceFile
from services.llm_service import ask_llm
from services.parser import keep_java_files
from services.prompt_builder import build_prompt


async def analyze_repository(files: list[SourceFile]) -> AnalyzeResponse:
    java_files = keep_java_files(files)
    if not java_files:
        return AnalyzeResponse(summary="No Java files were found.", issues=[])
    result = await ask_llm(build_prompt(java_files))
    issues = [Issue(**issue) for issue in result.get("issues", [])]
    return AnalyzeResponse(score=result.get("score"), summary=result.get("summary", "Analysis completed."), issues=issues)
