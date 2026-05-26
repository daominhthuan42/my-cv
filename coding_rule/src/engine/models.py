# =============================================================
# models.py
# =============================================================

import os

class SourceFile:
    """
    Source file model used by rule checkers.
    """

    def __init__(
        self,
        root: str,
        path: str,
        lines: list[str]
    ):

        self.root = root
        self.path = path
        self.lines = lines
        self.relative_path = os.path.relpath(
            path,
            root
        ).replace("\\", "/")
