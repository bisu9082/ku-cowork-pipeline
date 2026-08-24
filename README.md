# AutoResearchClaw Pipeline Adapter

This repository now contains the local AutoResearchClaw v6.2 / MetaClaw assets and a small command-line adapter for using them in this project.

## Layout

- `pipeline/system_prompt_gpt.md`: compact GPT-oriented pipeline prompt.
- `pipeline/system_prompt.md`: full original pipeline prompt.
- `pipeline/metaclaw/ku_publications.json`: KU publication and self-citation database.
- `pipeline/metaclaw/figure_patterns.json`: journal and chart-type figure rules.
- `pipeline/metaclaw/figure_revision_log.json`: figure revision log data.
- `pipeline/metaclaw/provenance_audit_policy.md`: audit-only provenance and disclosure gate.
- `pipeline/metaclaw/provenance_tools.json`: cross-tool provenance registry.
- `pipeline_config.json`: current project state and asset paths.
- `workspace/Step0` to `workspace/Step8`: generated research outputs.
- `scripts/pipeline_cli.py`: local helper for status, setup, citations, and figure rules.
- `scripts/run_provenance_audit.py`: wrapper for `guillaumemeyer/watermarks-remover` audit mode.
- `scripts/run_cross_provenance_audit.py`: cross-audit wrapper combining executable audit with image/visible watermark review cues.

## Quick Start

Use the bundled Codex Python runtime:

```powershell
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\pipeline_cli.py status
```

Initialize the project workspace:

```powershell
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\pipeline_cli.py init --name "My Research Project" --journal "ACS Sensors"
```

Find self-citation candidates:

```powershell
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\pipeline_cli.py self-cite "machine learning" "colorimetric sensor" "CWA detection"
```

Check figure rules:

```powershell
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\pipeline_cli.py figure --journal "ACS Sensors" --chart bar_chart
```

Run the provenance audit gate:

```powershell
git clone https://github.com/guillaumemeyer/watermarks-remover.git watermarks-remover
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\run_provenance_audit.py workspace\Step8 --watermarks-dir watermarks-remover --format json --out workspace\Step8\provenance_audit.json
```

The integration is audit-only. Use it to decide disclosure, provenance, and metadata-review actions; do not use it to remove or bypass provenance marks.

Run the cross-tool provenance gate:

```powershell
& "C:\Users\kkaan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\run_cross_provenance_audit.py workspace\Step8 --watermarks-dir watermarks-remover --out workspace\Step8\cross_provenance_audit.json
```

Cross-tool mode registers `watermarks-remover`, `noai-watermark`, visible watermark review tools, and MarkScrub as audit/reference channels. Only `watermarks-remover` is executed automatically; image watermark and visible overlay tools are manual review references.

## Operating Rule

The pipeline is stateful. Update `pipeline_config.json` through `scripts/pipeline_cli.py step` after a step is completed, and keep generated outputs under `workspace/StepN/`.
