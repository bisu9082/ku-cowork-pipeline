# Provenance Audit Policy

Purpose: connect `guillaumemeyer/watermarks-remover` to the KU paper pipeline as an audit-only pre-submission gate.

## Allowed Use

- Inspect manuscript assets for C2PA, Content Credentials, AI-generation metadata, invisible Unicode carriers, and high-probability AI-text cadence.
- Produce human, JSON, or SARIF reports under `workspace/Step7/` or `workspace/Step8/`.
- Use findings to decide whether the manuscript needs an AI-use disclosure, source attribution note, data provenance statement, or author confirmation.
- Remove only private or accidental local metadata when Ku confirms ownership and journal policy allows it, while preserving required provenance, copyright, authorship, and disclosure records.

## Disallowed Use

- Do not remove, hide, or bypass C2PA, Content Credentials, SynthID, AI provenance, copyright, authorship, or other provenance marks to misrepresent origin.
- Do not rewrite text to evade AI detectors or watermark detectors.
- Do not auto-clean submitted figures, PDFs, DOCX, HTML, Markdown, or images as part of the pipeline.
- Do not treat a clean audit as proof that content is human-authored; report only what the tool detected.

## Pipeline Gate

Run the audit in Step 7 before citation/final consistency signoff and again in Step 8 before accept-probability scoring when submission files changed.

GATE-PROV passes only when all are true:

- Audit report exists for the target submission directory.
- `files_skipped` is empty or each skipped file has a documented reason.
- C2PA/AI metadata findings are either disclosed, intentionally preserved, or cleared by Ku with a written reason.
- Suspicious Unicode or stylometry findings are reviewed as writing-quality signals, not detector-evasion targets.
- The final Step report includes: `PROV-AUDIT: [pass/review-needed] | report: [path] | disclosure: [none/needed/included]`.

## Recommended Command

```powershell
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\run_provenance_audit.py workspace\Step8 --watermarks-dir watermarks-remover --format json --out workspace\Step8\provenance_audit.json
```

Use `--format sarif` for GitHub code scanning style output. Use `--allow-actionable` only when the goal is to record findings without failing the gate.
