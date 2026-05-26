# =============================================================
# naming.py
# =============================================================

import re
import os

def add_violation(
    violations: dict,
    rule_id: str,
    source_root: str,
    file_path: str,
    line_no: int,
    code: str
):
    """
    Add detected violation into runtime violation database.

    Parameters
    ----------
    violations : dict
        Runtime violation container.

    rule_id : str
        Rule identifier.

    source_root : str
        Root source directory used to generate relative paths.

    file_path : str
        Absolute source file path.

    line_no : int
        Violated line number.

    code : str
        Violated source code line.

    Returns
    -------
    None

    Notes
    -----
    Violations are grouped by:
        1. Rule ID
        2. Relative file path
        3. Violated lines
    """


    # Convert absolute path to relative path
    relative_path = os.path.relpath(file_path, source_root)

    # Normalize slash style
    relative_path = relative_path.replace("\\", "/")

    # Create rule entry if not existing
    if rule_id not in violations:
        violations[rule_id] = {"files": {}}

    # Create file entry if not existing
    if relative_path not in violations[rule_id]["files"]:
        violations[rule_id]["files"][relative_path] = []

    # Append violated line information
    violations[rule_id]["files"][relative_path].append((line_no, code.strip()))

def check_name_var_001(
    source: dict,
    violations: dict
):
    """
    Check local variable naming convention.

    Rule
    ----
    Local variable shall follow naming convention:

        L + type prefix + PascalCase

    Example
    -------
    Valid:
        LucCounter

    Invalid:
        Temp
        GucResult

    Parameters
    ----------
    source : dict
        Parsed source file information.

        Example:
        {
            "root": source_root,
            "path": file_path,
            "relative_path": relative_path,
            "lines": lines
        }

    violations : dict
        Runtime violation container.

    Returns
    -------
    None
    """

    # Extract source information
    source_root = source["root"]
    file_path = source["path"]
    lines = source["lines"]

    # Variable declaration detection pattern
    pattern = re.compile(r"\b(?:uint8|uint16|uint32|boolean|sint8|sint16|sint32)\s+([A-Za-z_][A-Za-z0-9_]*)")

    # Valid local variable naming convention
    valid_pattern = re.compile(r"^L[a-z]{2}[A-Z][A-Za-z0-9]*$")

    # Scan source lines
    for line_no, line in enumerate(lines, start=1):

        match = pattern.search(line)

        if not match:
            continue

        var_name = match.group(1)

        # Check naming violation
        if not valid_pattern.match(var_name):

            add_violation(
                violations=violations,
                rule_id="Name_Var_001",
                source_root=source_root,
                file_path=file_path,
                line_no=line_no,
                code=line
            )
