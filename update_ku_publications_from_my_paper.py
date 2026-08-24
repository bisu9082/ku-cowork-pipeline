#!/usr/bin/env python3
"""Update MetaClaw KU publication DB from the Desktop "my paper" folder."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path.home() / "Desktop" / "my paper"
DEFAULT_DB = ROOT / "pipeline" / "metaclaw" / "ku_publications.json"
DEFAULT_REPORT = ROOT / "workspace" / "Step8" / "ku_publications_update_report.json"


FIELD_RE = re.compile(r"(?im)^\s*([a-zA-Z][\w-]*)\s*=\s*")
DOI_PREFIX_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.I)
YEAR_PREFIX_RE = re.compile(r"^(20\d{2}|19\d{2})")


TOPIC_RULES = [
    ("colorimetric sensor", ("colorimetric", "sensor array", "optical sensor")),
    ("chemical warfare agent", ("chemical warfare", "nerve agent", "novichok", "cwa", "mustard")),
    ("CBRN", ("cbrn", "radiological", "chemical warfare", "biological warfare")),
    ("machine learning", ("machine learning", "deep learning", "random forest", "xgboost", "yolov8", "classification")),
    ("environmental hazard", ("environmental", "hazard", "fire", "contaminant", "ecotox")),
    ("radiation", ("radiation", "gamma", "neutron", "radionuclide", "dosimeter")),
    ("decontamination", ("decontamination", "degradation", "photocatalytic")),
    ("materials", ("alloy", "nitriding", "rubber", "composite", "tio2")),
    ("biomedical", ("urine", "prostate", "cochlear", "neurology", "theranostic")),
    ("field deployable", ("portable", "field", "uav", "flight", "offline")),
]


def clean_value(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if len(value) >= 2 and value[0] in "{\"" and value[-1] in "}\"":
        value = value[1:-1]
    value = value.replace("\\&lt;", "<").replace("\\&gt;", ">")
    value = value.replace("\\&", "&")
    return " ".join(value.split())


def extract_field(text: str, field: str) -> str | None:
    match = re.search(rf"(?im)^\s*{re.escape(field)}\s*=\s*", text)
    if not match:
        return None
    i = match.end()
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text):
        return None
    opener = text[i]
    if opener in "{\"":
        closer = "}" if opener == "{" else "\""
        i += 1
        start = i
        depth = 1 if opener == "{" else 0
        while i < len(text):
            ch = text[i]
            if opener == "{":
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return clean_value(text[start:i])
            elif ch == closer and text[i - 1] != "\\":
                return clean_value(text[start:i])
            i += 1
        return clean_value(text[start:])
    end = text.find(",", i)
    if end == -1:
        end = text.find("\n", i)
    if end == -1:
        end = len(text)
    return clean_value(text[i:end])


def parse_bibtex_file(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "@" not in text or not FIELD_RE.search(text):
        return None
    key_match = re.search(r"@\w+\s*\{\s*([^,\s]+)", text)
    fields = {
        name: extract_field(text, name)
        for name in ("title", "journal", "year", "doi", "author", "keywords", "volume", "pages")
    }
    if not fields["title"] and not fields["doi"]:
        return None
    doi = fields["doi"]
    if doi:
        doi = DOI_PREFIX_RE.sub("", doi).strip()
    year = None
    if fields["year"]:
        year_match = re.search(r"(19|20)\d{2}", fields["year"])
        if year_match:
            year = int(year_match.group(0))
    authors = []
    if fields["author"]:
        authors = [clean_value(a) for a in re.split(r"\s+and\s+|;", fields["author"]) if a.strip()]
    keywords = []
    if fields["keywords"]:
        keywords = [clean_value(k) for k in re.split(r",|;", fields["keywords"]) if k.strip()]
    return {
        "bibtex_key": key_match.group(1) if key_match else path.stem,
        "authors": authors,
        "year": year,
        "title": fields["title"],
        "journal": fields["journal"],
        "doi": doi,
        "keywords": keywords,
        "volume": fields["volume"],
        "pages": fields["pages"],
        "source_file": str(path),
    }


def normalize_doi(doi: str | None) -> str:
    return DOI_PREFIX_RE.sub("", doi or "").strip().lower()


def normalize_title(title: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def make_bibtex_key(entry: dict) -> str:
    if entry.get("bibtex_key") and not re.match(r"^10\.", str(entry["bibtex_key"]), re.I):
        return str(entry["bibtex_key"])
    first = "Ku"
    for author in entry.get("authors", []):
        parts = re.split(r"\s+|,", author.strip())
        if parts:
            first = re.sub(r"[^A-Za-z0-9]", "", parts[0]) or "Ku"
            break
    journal = re.sub(r"[^A-Za-z0-9]", "", entry.get("journal") or "Publication")[:12]
    return f"{first}{entry.get('year') or 'YYYY'}{journal}"


def infer_topics(entry: dict) -> list[str]:
    haystack = " ".join(
        str(x or "")
        for x in [entry.get("title"), entry.get("journal"), " ".join(entry.get("keywords") or [])]
    ).lower()
    topics = [topic for topic, needles in TOPIC_RULES if any(n in haystack for n in needles)]
    if not topics:
        topics = ["KU publication"]
    return topics


def citation_hint(entry: dict, topics: list[str]) -> str:
    title = entry.get("title") or "KU publication"
    core = ", ".join(topics[:3])
    return f"{core} 관련 논문시 인용: {title[:80]}"


def next_id(publications: list[dict], year: int | None) -> str:
    max_n = 0
    for pub in publications:
        match = re.match(r"J(\d+)-", str(pub.get("id", "")))
        if match:
            max_n = max(max_n, int(match.group(1)))
    return f"J{max_n + 1}-{year or 'YYYY'}"


def pdf_candidates(source: Path, known_titles: set[str]) -> list[dict]:
    items = []
    for path in sorted(source.glob("*.pdf")):
        stem = path.stem
        year = None
        match = YEAR_PREFIX_RE.match(stem)
        if match:
            year = int(match.group(1)[:4])
            stem = stem[6:].strip(" -_")
        title_norm = normalize_title(stem)
        if title_norm and title_norm not in known_titles:
            items.append(
                {
                    "year": year,
                    "title_from_filename": stem,
                    "source_file": str(path),
                    "note": "PDF-only candidate; not inserted into publications without BibTeX/DOI metadata.",
                }
            )
    return items


def merge(db: dict, imported: list[dict]) -> tuple[dict, dict]:
    publications = list(db.get("publications", []))
    doi_index = {normalize_doi(p.get("doi")): p for p in publications if normalize_doi(p.get("doi"))}
    title_index = {normalize_title(p.get("title")): p for p in publications if normalize_title(p.get("title"))}
    added = []
    updated = []
    skipped = []

    for raw in imported:
        if not raw.get("title") or not raw.get("doi"):
            skipped.append({"source_file": raw.get("source_file"), "reason": "missing title or DOI"})
            continue
        doi_key = normalize_doi(raw.get("doi"))
        title_key = normalize_title(raw.get("title"))
        existing = doi_index.get(doi_key) or title_index.get(title_key)
        topics = infer_topics(raw)
        payload = {
            "bibtex_key": make_bibtex_key(raw),
            "authors": raw.get("authors", []),
            "year": raw.get("year"),
            "title": raw.get("title"),
            "journal": raw.get("journal"),
            "doi": raw.get("doi"),
            "topics": topics,
            "keywords": raw.get("keywords", []),
            "citation_hint": citation_hint(raw, topics),
            "verified": f"local BibTeX import {date.today()}",
            "doi_status": "unverified_local_bibtex",
            "local_source": "Desktop/my paper",
            "local_source_file": raw.get("source_file"),
            "verification_note": "Imported from local BibTeX/PDF collection; DOI resolution not rechecked in this run.",
        }
        if raw.get("volume"):
            payload["volume"] = raw["volume"]
        if raw.get("pages"):
            payload["pages"] = raw["pages"]

        if existing:
            changed = {}
            protected = {
                "authors",
                "year",
                "title",
                "journal",
                "doi",
                "verified",
                "doi_status",
                "verification_note",
                "source",
                "source_file",
            }
            for key, value in payload.items():
                if value in (None, [], ""):
                    continue
                if key in protected:
                    continue
                if key == "topics" and existing.get("topics"):
                    merged_topics = list(dict.fromkeys([*existing.get("topics", []), *value]))
                    if merged_topics != existing.get("topics"):
                        existing[key] = merged_topics
                        changed[key] = merged_topics
                    continue
                if key == "keywords" and existing.get("keywords"):
                    merged_keywords = list(dict.fromkeys([*existing.get("keywords", []), *value]))
                    if merged_keywords != existing.get("keywords"):
                        existing[key] = merged_keywords
                        changed[key] = merged_keywords
                    continue
                if existing.get(key) != value:
                    existing[key] = value
                    changed[key] = value
            existing["local_source"] = "Desktop/my paper"
            existing["local_source_file"] = raw.get("source_file")
            existing["local_refresh_note"] = (
                "Matched local BibTeX during 2026-08-23 refresh; existing verified metadata preserved."
            )
            changed.setdefault("local_source_file", raw.get("source_file"))
            if changed:
                updated.append({"id": existing.get("id"), "doi": raw.get("doi"), "changed": sorted(changed)})
        else:
            payload["id"] = next_id(publications, raw.get("year"))
            publications.append(payload)
            doi_index[doi_key] = payload
            title_index[title_key] = payload
            added.append({"id": payload["id"], "doi": payload["doi"], "title": payload["title"]})

    db["publications"] = sorted(
        publications,
        key=lambda p: (-(p.get("year") or 0), str(p.get("journal") or ""), str(p.get("title") or "")),
    )
    meta = dict(db.get("_meta", {}))
    meta.update(
        {
            "version": "2.2",
            "last_updated": str(date.today()),
            "total_published": len(db["publications"]),
            "source_refresh": "Desktop/my paper BibTeX import",
            "doi_verification_status": "Local BibTeX DOI values imported; external DOI resolution not performed.",
        }
    )
    db["_meta"] = meta
    return db, {"added": added, "updated": updated, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--out", type=Path, default=DEFAULT_DB)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    data = json.loads(args.db.read_text(encoding="utf-8"))
    bib_files = list(args.source.glob("*.txt")) + list(args.source.glob("*.bib")) + list(args.source.glob("*.bibtex"))
    imported = [entry for path in sorted(bib_files) if (entry := parse_bibtex_file(path))]
    merged, report = merge(data, imported)
    known_titles = {normalize_title(p.get("title")) for p in merged.get("publications", [])}
    report.update(
        {
            "source": str(args.source),
            "source_files_scanned": len(bib_files),
            "structured_entries_found": len(imported),
            "pdf_only_candidates": pdf_candidates(args.source, known_titles),
            "output": str(args.out),
        }
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"updated publication DB: +{len(report['added'])}, "
        f"updated {len(report['updated'])}, skipped {len(report['skipped'])}, "
        f"pdf-only candidates {len(report['pdf_only_candidates'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
