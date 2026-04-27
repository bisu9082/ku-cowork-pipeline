# AutoMetaNet — Drug Metabolite Discovery Pipeline

## 프로젝트 개요
공개 LC-MS/MS 데이터(MassIVE/MetaboLights)를 GNPS2 플랫폼으로 분석하여
약물 대사체를 자동 발굴하고 MASST 리포지터리 검색으로 재현성을 검증하는 파이프라인.

## 폴더 구조
```
pipeline/
├── figure/          # 논문 Figure (PNG, 300 dpi 이상)
├── latex/           # 논문 LaTeX 소스 (main.tex, si.tex, myref.bib)
└── upload/          # GitHub 업로드 대상 파일
    ├── analysis_main.py     # Step 4 완성 후 추가
    ├── requirements.txt     # Step 4 완성 후 추가
    └── README_pipeline.md   # 이 파일
```

## 공개 데이터셋
| ID | 약물 | 내용 |
|----|------|------|
| MSV000085161 | Sildenafil | In vivo 마우스 혈장 (0-48h) |
| MSV000085495 | Sildenafil | Human liver microsome (0-4h) |
| MSV000085496 | Sildenafil | 5종 간 microsome (4h) |
| MTBLS2746    | Amitriptyline | Human plasma (EBI) |
| MSV000096967 | KF1601 | 신약후보물질 대사 |

## 투고 저널
Analytical Chemistry (ACS) — `\documentclass[journal=jacsat,manuscript=article]{achemso}`

## 저자
- Ku Kang (CBDRI)
- Jeongyun Kim (SNU CBE)
- Jin Yoo (CBDRI)
- Dongyoul Lee (Korea Military Academy) — Corresponding author
