from models.schemas import SourceFile


def read_repository_files(files: list[SourceFile]) -> list[SourceFile]:
    """This keeps the file-reading step separate for future GitHub API support."""
    return files
