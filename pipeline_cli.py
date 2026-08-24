#!/usr/bin/env python3
"""Small local adapter for the AutoResearchClaw/MetaClaw pipeline assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "pipeline_config.json"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def config() -> dict[str, Any]:
    return load_json(CONFIG_PATH)


def data_path(cfg: dict[str, Any], key: str) -> Path:
    return ROOT / cfg["paths"][key]


def cmd_status(_args: argparse.Namespace) -> None:
    cfg = config()
    print(f"Pipeline: {cfg['pipeline_version']}")
    print(f"Project: {cfg['project_name']}")
    print(f"Target journal: {cfg.get('target_journal') or '[not set]'}")
    print(f"Current step: Step {cfg['current_step']}")
    print(f"Completed steps: {cfg.get('completed_steps') or []}")
    print(f"Save root: {rel(ROOT / cfg['save_root'])}")
    print("\nAssets:")
    for key, value in cfg["paths"].items():
        path = ROOT / value
        status = "ok" if path.exists() else "missing"
        print(f"- {key}: {rel(path)} [{status}]")


def cmd_init(args: argparse.Namespace) -> None:
    cfg = config()
    if args.name:
        cfg["project_name"] = args.name
    if args.journal:
        cfg["target_journal"] = args.journal
    save_root = ROOT / cfg["save_root"]
    save_root.mkdir(exist_ok=True)
    for step in range(0, 9):
        (save_root / f"Step{step}").mkdir(exist_ok=True)
    save_json(CONFIG_PATH, cfg)
    print(f"Initialized {cfg['project_name']} under {rel(save_root)}")
    print(f"Target journal: {cfg.get('target_journal') or '[not set]'}")


def cmd_step(args: argparse.Namespace) -> None:
    cfg = config()
    if args.set is not None:
        if args.set < 0 or args.set > 8:
            raise SystemExit("Step must be between 0 and 8.")
        cfg["current_step"] = args.set
    if args.complete is not None:
        completed = list(dict.fromkeys(cfg.get("completed_steps", []) + [args.complete]))
        cfg["completed_steps"] = sorted(completed)
        cfg["current_step"] = max(cfg.get("current_step", 0), min(args.complete + 1, 8))
    save_json(CONFIG_PATH, cfg)
    print(f"Current step: Step {cfg['current_step']}")
    print(f"Completed steps: {cfg.get('completed_steps') or []}")


def normalize_terms(terms: list[str]) -> set[str]:
    out: set[str] = set()
    for term in terms:
        for chunk in term.replace(",", " ").split():
            if chunk.strip():
                out.add(chunk.strip().lower())
    return out


def cmd_self_cite(args: argparse.Namespace) -> None:
    cfg = config()
    db = load_json(data_path(cfg, "ku_publications"))
    query = normalize_terms(args.topics)
    min_overlap = args.min_overlap or db.get("self_citation_rules", {}).get("min_topic_overlap", 2)
    hits = []
    for paper in db.get("publications", []):
        if paper.get("status", "").lower().startswith("under review"):
            continue
        terms = normalize_terms(paper.get("topics", []) + paper.get("keywords", []))
        overlap = sorted(query & terms)
        if len(overlap) >= min_overlap:
            hits.append((len(overlap), overlap, paper))
    hits.sort(key=lambda item: (-item[0], item[2].get("year", 0), item[2].get("id", "")))
    if not hits:
        print("No self-citation candidates met the overlap threshold.")
        return
    for score, overlap, paper in hits[: args.limit]:
        doi = paper.get("doi") or "[DOI not available]"
        print(f"- {paper['bibtex_key']} ({paper.get('year')}), {paper.get('journal')}")
        print(f"  Title: {paper.get('title')}")
        print(f"  DOI: {doi}")
        print(f"  Overlap({score}): {', '.join(overlap)}")
        print(f"  Use when: {paper.get('citation_hint', '')}")


def find_journal_specs(db: dict[str, Any], journal: str) -> list[tuple[str, dict[str, Any]]]:
    journal_l = journal.lower()
    out = []
    for key, spec in db.get("journal_specs", {}).items():
        applies = [str(x).lower() for x in spec.get("applies_to", [])]
        if journal_l in key.lower() or any(journal_l in item or item in journal_l for item in applies):
            out.append((key, spec))
    return out


def cmd_figure(args: argparse.Namespace) -> None:
    cfg = config()
    db = load_json(data_path(cfg, "figure_patterns"))
    journal = args.journal or cfg.get("target_journal")
    if journal:
        specs = find_journal_specs(db, journal)
        if specs:
            print(f"Journal specs for {journal}:")
            for key, spec in specs:
                print(f"- {key}")
                for field in ("typography", "resolution_dpi", "file_formats", "color"):
                    if field in spec:
                        print(f"  {field}: {json.dumps(spec[field], ensure_ascii=False)}")
        else:
            print(f"No exact journal spec found for {journal}.")
    if args.chart:
        chart = db.get("chart_type_specs", {}).get(args.chart)
        if not chart:
            print(f"No chart spec found for {args.chart}.")
        else:
            print(f"\nChart spec: {args.chart}")
            for field in ("recommended_figsize", "color_rules", "axes", "legend", "common_errors"):
                if field in chart:
                    print(f"- {field}: {json.dumps(chart[field], ensure_ascii=False)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    status = sub.add_parser("status", help="Show pipeline state and asset paths.")
    status.set_defaults(func=cmd_status)

    init = sub.add_parser("init", help="Create workspace/Step0..Step8 folders and update metadata.")
    init.add_argument("--name", help="Project name to store in pipeline_config.json.")
    init.add_argument("--journal", help="Target journal to store in pipeline_config.json.")
    init.set_defaults(func=cmd_init)

    step = sub.add_parser("step", help="Set or mark research pipeline steps.")
    step.add_argument("--set", type=int, help="Set current step.")
    step.add_argument("--complete", type=int, help="Mark a step completed and move forward.")
    step.set_defaults(func=cmd_step)

    cite = sub.add_parser("self-cite", help="Find KU self-citation candidates by topic overlap.")
    cite.add_argument("topics", nargs="+", help="Topic or keyword terms.")
    cite.add_argument("--min-overlap", type=int, default=None, help="Minimum topic/keyword overlap.")
    cite.add_argument("--limit", type=int, default=5, help="Maximum results.")
    cite.set_defaults(func=cmd_self_cite)

    fig = sub.add_parser("figure", help="Show journal and chart figure rules.")
    fig.add_argument("--journal", help="Journal name. Defaults to target_journal.")
    fig.add_argument("--chart", help="Chart type key, e.g. bar_chart, heatmap, line_plot.")
    fig.set_defaults(func=cmd_figure)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
