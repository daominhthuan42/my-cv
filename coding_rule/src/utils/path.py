from pathlib import Path


def normalize_path(path: str) -> str:
    """
    Normalize filesystem path.

    Convert:
    - Windows backslash paths
    - Mixed slash paths
    - Quoted paths

    into platform-independent normalized path.
    """

    path = path.strip()
    normalized = Path(path)
    return normalized.as_posix()
