import os
import json
from rules.naming import check_name_var_001
from engine.models import SourceFile

def scan_project(source_path: str, module: str, rules_path: str):
    """
    Scan source code project for coding rule violations.

    Parameters
    ----------
    source_path : str
        Root directory containing source files to be scanned.

    module : str
        Target module name filter.

        Example:
        - "adc"
        - "gpio"
        - "ALL"

        If "ALL" is specified, all source files are scanned.

    rules_path : str
        Path to rule configuration JSON file.

    Returns
    -------
    tuple
        violations : dict
            Runtime violation database generated during scan.

        rules : dict
            Rule metadata database loaded from rules.json.

    Notes
    -----
    - Only '.c' and '.h' files are scanned.
    - Rule checking functions are executed sequentially.
    - Violations are collected dynamically during scanning.
    - Module filtering is based on filename matching.
    """

    # Load rule configuration database
    with open(rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    # Runtime violation container
    violations = {}

    # Traverse source directory recursively
    for root, _, files in os.walk(source_path):
        for file_name in files:
             # Scan only C source/header files
            if not file_name.endswith((".c", ".h")):
                continue

            file_path = os.path.join(root, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            source = SourceFile(
                root=source_path,
                path=file_path,
                lines=lines
            )

            # Apply module filter
            if module != "ALL":
                if module.lower() not in file_name.lower():
                    continue

            # Full source file path
            file_path = os.path.join(root, file_name)

            # Execute rule checkers
            check_name_var_001(source=source, violations=violations)

    return violations, rules