#!/usr/bin/env python3
"""Audit manuscript assets for provenance/metadata signals.

This wrapper connects the KU paper pipeline to the external
guillaumemeyer/watermarks-remover checkout in audit-only mode. It deliberately
does not call any cleaning/removal entrypoint.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def default_watermarks_dir() -> Path:
    env = os.environ.get("WATERMARKS_REMOVER_DIR")
    if env:
        return Path(env)
    return ROOT / "watermarks-remover"


def resolve_audit_script(watermarks_dir: Path) -> Path:
    script = watermarks_dir / "service" / "scripts" / "audit_dir.py"
    if not script.is_file():
        raise SystemExit(
            "watermarks-remover audit script not found. "
            "Clone https://github.com/guillaumemeyer/watermarks-remover "
            f"or pass --watermarks-dir. Looked at: {script}"
        )
    return script


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Submission/workspace directory to audit")
    parser.add_argument(
        "--watermarks-dir",
        type=Path,
        default=default_watermarks_dir(),
        help="Local checkout of guillaumemeyer/watermarks-remover",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json", "sarif"),
        default="human",
        help="Report format",
    )
    parser.add_argument("--out", type=Path, help="Write report to this file")
    parser.add_argument("--jobs", type=int, default=1, help="Audit worker count")
    parser.add_argument(
        "--check-stylometry",
        action="store_true",
        help="Also score text cadence as a writing-quality review signal",
    )
    parser.add_argument(
        "--allow-actionable",
        action="store_true",
        help="Return 0 even when audit findings need review",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = args.path.resolve()
    if not target.is_dir():
        raise SystemExit(f"not a directory: {target}")

    audit_script = resolve_audit_script(args.watermarks_dir.resolve())
    cmd = [
        sys.executable,
        str(audit_script),
        str(target),
        "--format",
        args.format,
        "--jobs",
        str(args.jobs),
    ]
    if args.check_stylometry:
        cmd.append("--check-stylometry")

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(proc.stdout, encoding="utf-8")
    else:
        print(proc.stdout, end="")

    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")

    if args.allow_actionable and proc.returncode == 1:
        return 0
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
