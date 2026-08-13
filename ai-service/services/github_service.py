import base64
import os
import re

import httpx

from models.schemas import SourceFile

GITHUB_URL_PATTERN = re.compile(
    r"^https?://github\.com/(?P<owner>[\w.-]+)/(?P<repository>[\w.-]+)/?$"
)
MAX_FILES = 20
MAX_FILE_SIZE = 20_000


def parse_repository_url(repository_url: str) -> tuple[str, str]:
    """Return the owner and repository name from a public GitHub URL."""
    match = GITHUB_URL_PATTERN.match(repository_url.strip())
    if not match:
        raise ValueError("Enter a public repository URL such as https://github.com/owner/repository.")

    return match.group("owner"), match.group("repository").removesuffix(".git")


async def get_java_files_from_github(repository_url: str) -> list[SourceFile]:
    owner, repository = parse_repository_url(repository_url)
    headers = {"Accept": "application/vnd.github+json"}
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    async with httpx.AsyncClient(timeout=30, headers=headers) as client:
        repository_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repository}"
        )
        repository_response.raise_for_status()
        default_branch = repository_response.json()["default_branch"]

        tree_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repository}/git/trees/{default_branch}",
            params={"recursive": "1"},
        )
        tree_response.raise_for_status()
        java_paths = [
            item["path"]
            for item in tree_response.json().get("tree", [])
            if item["type"] == "blob" and item["path"].endswith(".java")
        ][:MAX_FILES]

        files = []
        for path in java_paths:
            file_response = await client.get(
                f"https://api.github.com/repos/{owner}/{repository}/contents/{path}",
                params={"ref": default_branch},
            )
            file_response.raise_for_status()
            file_data = file_response.json()
            content = base64.b64decode(file_data["content"]).decode("utf-8", errors="replace")
            files.append(SourceFile(path=path, content=content[:MAX_FILE_SIZE]))

    return files


def read_repository_files(files: list[SourceFile]) -> list[SourceFile]:
    """Keep file-reading separate from the repository download step."""
    return files
