import argparse
from engine.scanner import scan_project
from engine.reporter import generate_report
from utils.path import normalize_path

def main():

    parser = argparse.ArgumentParser(
        prog="code_parser",
        description="ISO26262 Static Code Parser"
    )

    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help="Source code directory"
    )

    parser.add_argument(
        "-m",
        "--module",
        default="ALL",
        help="Target module name"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="log",
        help="Output directory"
    )

    parser.add_argument(
        "-r",
        "--rules",
        default="config/rules.json",
        help="Rule configuration file"
    )

    args = parser.parse_args()
    args.path = normalize_path(args.path)
    args.output = normalize_path(args.output)
    args.rules = normalize_path(args.rules)

    violations, rules = scan_project(
        source_path=args.path,
        module=args.module,
        rules_path=args.rules
    )

    generate_report(
        violations=violations,
        rules=rules,
        output_dir=args.output
    )
