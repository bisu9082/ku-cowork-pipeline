# ku-cowork-pipeline

Claude Cowork 기반 논문 자동화 파이프라인 (AutoResearchClaw v0.3.1 기반)

## 저장소 구조
- `pipeline/system_prompt.md` — Cowork 시스템 프롬프트 (메인)
- `pipeline/figure_rules.md` — matplotlib Nature급 스타일 규칙
- `metaclaw/research_patterns.json` — 연구 패턴 데이터베이스
- `journal_requirements/` — 저널별 제출 요건

## Cowork 사용법
세션 시작 시 아래 URL을 web_fetch로 로드:
https://raw.githubusercontent.com/bisu9082/ku-cowork-pipeline/main/pipeline/system_prompt.md
