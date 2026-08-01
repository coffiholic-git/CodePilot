from models.schemas import SourceFile


def build_prompt(files: list[SourceFile]) -> str:
    code = "\n\n".join(f"--- {file.path} ---\n{file.content}" for file in files)
    return (
        "You are a helpful Java code reviewer. Return only JSON with score, summary, and issues. "
        "Each issue needs filePath, severity, line, message, suggestion, and confidence. "
        "Check security, readability, bugs, and Spring Boot best practices.\n\n" + code
    )
