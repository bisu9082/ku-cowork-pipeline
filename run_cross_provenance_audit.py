#!/usr/bin/env python3
"""Run the KU cross-tool provenance audit gate.

The cross audit combines the executable watermarks-remover audit with a
registry-driven checklist for image watermark and visible-overlay review. It
does not call any watermark removal, cleaning, or rewrite entrypoint.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "pipeline" / "metaclaw" / "provenance_tools.json"
RUNNER = ROOT / "scripts" / "run_provenance_audit.py"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".heic", ".bmp", ".gif", ".tif", ".tiff"}


def load_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def image_inventory(root: Path) -> list[dict]:
    images = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES):
        images.append(
            {
                "path": str(path),
                "suffix": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "manual_review": [
                    "Check whether the image is AI-generated or AI-edited.",
                    "Check for visible platform overlays, logos, or stamps.",
                    "If AI-generated/edited, preserve required provenance or add journal-compliant disclosure.",
                    "Do not remove invisible or visible provenance marks to misrepresent origin.",
                ],
            }
        )
    return images


def command_status() -> dict:
    return {
        "noai-watermark": {
            "available_on_path": shutil.which("noai-watermark") is not None,
            "pipeline_mode": "manual_reference_only",
        },
        "watermarks-remover": {
            "available_by_checkout": (ROOT / "watermarks-remover" / "service" / "scripts" / "audit_dir.py").is_file(),
            "pipeline_mode": "audit_only",
        },
    }


def run_primary_audit(args: argparse.Namespace, report_path: Path) -> dict:
    cmd = [
        sys.executable,
        str(RUNNER),
        str(args.path),
        "--watermarks-dir",
        str(args.watermarks_dir),
        "--format",
        "json",
        "--out",
        str(report_path),
        "--jobs",
        str(args.jobs),
    ]
    if args.check_stylometry:
        cmd.append("--check-stylometry")
    if args.allow_actionable:
        cmd.append("--allow-actionable")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    payload = None
    if report_path.is_file():
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stderr": proc.stderr,
        "report_path": str(report_path),
        "summary": payload.get("summary") if isinstance(payload, dict) else None,
        "files_skipped": payload.get("files_skipped") if isinstance(payload, dict) else None,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Submission/workspace directory to audit")
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--watermarks-dir", type=Path, default=ROOT / "watermarks-remover")
    parser.add_argument("--out", type=Path, help="Cross-audit JSON output path")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--check-stylometry", action="store_true")
    parser.add_argument("--allow-actionable", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = args.path.resolve()
    if not target.is_dir():
        raise SystemExit(f"not a directory: {target}")
    out = args.out or target / "cross_provenance_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    primary_report = out.with_name(out.stem + "_watermarks_remover.json")

    registry = load_registry(args.registry)
    primary = run_primary_audit(args, primary_report)
    images = image_inventory(target)
    statuses = command_status()
    review_needed = []
    summary = primary.get("summary") or {}
    if primary["returncode"] not in (0,):
        review_needed.append("primary_audit_returned_nonzero")
    if summary.get("actionable_files", 0):
        review_needed.append("watermarks_remover_actionable_findings")
    if images:
        review_needed.append("manual_image_provenance_review")

    report = {
        "root": str(target),
        "registry": registry,
        "tool_status": statuses,
        "primary_audit": primary,
        "image_inventory": images,
        "gate": {
            "status": "review-needed" if review_needed else "pass",
            "review_needed": review_needed,
            "required_step_report_line": "PROV-CROSS: [pass/review-needed] | reports: [cross json, primary json] | disclosure: [none/needed/included]",
        },
    }
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cross audit: {report['gate']['status']} | report: {out}")
    return 1 if review_needed and not args.allow_actionable else 0


if __name__ == "__main__":
    raise SystemExit(main())
