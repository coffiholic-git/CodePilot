from models.schemas import SourceFile


def keep_java_files(files: list[SourceFile]) -> list[SourceFile]:
    return [file for file in files if file.path.endswith(".java")]
