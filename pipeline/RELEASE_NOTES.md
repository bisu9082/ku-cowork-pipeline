# AutoResearchClaw Pipeline — Release Notes

---

## v6.8.2 — 2026-07-19

v6.8.1이 도입한 `?t=[난수]` 캐시 우회가 실제로는 작동하지 않음을 확인해 방식을 바꾼다.

raw.githubusercontent.com은 쿼리스트링을 바꿔가며 3회 요청하고 20초를 기다려도 계속 구버전(108,680B)을 반환했다. 같은 시각 GitHub API contents 엔드포인트는 최신(109,238B)을 반환했다. 캐시 무효화 시점을 통제할 수 없으므로 raw는 정본 판단에서 배제한다.

- 모든 GitHub 파일 로드를 `api.github.com/repos/.../contents/[경로]?ref=main`으로 전환했다. CDN을 거치지 않아 커밋 직후 최신이 오고, 응답의 size 필드로 교차 확인도 된다.
- 파일 존재·목록 확인은 `git/trees/main?recursive=1`을 쓴다.
- web_fetch만 가능한 상황에서 버전이 낮게 나오더라도 미업로드로 단정하지 않고, API로 교차 확인한 뒤 판정하도록 했다.

---

## v6.8.1 — 2026-07-19

GitHub 배포 검증 중 드러난 함정 2개를 방어한다.

- **CDN 캐시 우회.** raw.githubusercontent.com이 업로드 후 최대 5분간 구버전을 반환한다. 실제로 v6.8 업로드 완료 상태에서 v6.5가 로드됐다. 모든 GitHub raw fetch URL에 `?t=[난수]`를 붙이고, 로드 후 버전 번호를 내장 지침과 대조하도록 했다.
- **DB 정본 경로 고정.** ku_publications.json 정본을 `pipeline/metaclaw/`로 못박았다. 정리된 v2.1을 루트에만 올려 파이프라인이 읽는 경로에는 허구 DOI가 그대로 남아 있던 사고를 반영했다. DB 로드 직후 version 필드 존재와 항목 수를 확인하고, 어긋나면 self-cite를 진행하지 않는다.

---

## v6.8 — 2026-07-19

SELFCITE-AUDIT 신설. 2026-07-19 감사에서 ku_publications.json의 DOI 13건이 Ku와 무관한 타인 논문으로 연결되는 것을 적발한 데 따른 조치다. 자기인용 DB는 오류 시 Ku 논문에 남의 DOI가 실리므로 외부 문헌보다 위험하다.

- verified 필드 없는 항목은 self-cite 후보에서 자동 제외. under_review(심사 중) 논문은 인용 절대 금지.
- 감사 트리거 3종: Step 1 진입 시(필수), DB 추가 시(필수), 분기 1회 전수(권장).
- 판정은 출처(provenance) 교차 기준. 가장 위험한 것은 "DOI는 리졸브되는데 저자에 Kang이 없는" 경우로, 적발된 13건이 전부 이 유형이었다. 저자 대조를 생략하면 놓친다.
- CrossRef 404만으로 허구 판정하지 않는다. 국내지(10.31066·10.37944·10.31818)는 미등록이 흔해, 원문 인쇄값이면 doi_status=unregistered로 보존하고 인용 시 DOI를 생략한다.
- DB 수정 시 백업·무결성 재확인·integrity_note 기록을 의무화했다.

부수 작업으로 ku_publications.json을 v2.1로 재구축했다. 허구 13편 삭제, J2·J6 DOI 정정, 신규 10편 추가(bib 3 + PDF 7), 최종 32편 전수 verified.

---

## v6.7 — 2026-07-19

IEEE 저널을 티어 1로 격상해 ACS·RSC와 동급으로 다룬다. 티어 내 서열은 두지 않고 논문 성격으로 선택한다.

- Step 2 우선순위를 티어 구조로 재편: [티어1] ACS·RSC·IEEE → [티어2] Elsevier·Springer Nature.
- IEEE 선택 가이드 추가: 계측·불확도 → TIM, 센서 시스템 → Sensors Journal, 핵계측 → TNS, 공간매핑 → TGRS, ML 아키텍처 → TNNLS, 보건 ML → JBHI. 화학 메커니즘·분자 설계가 핵심이면 ACS/RSC.
- IEEE Figure 규격: single 88.9mm(3.5in) / double 181.6mm(7.16in), 패널 라벨 (a)(b)(c), DPI 300/600/1000.
- IEEEtran LaTeX 구조 + 제출 패키지(Index Terms, ORCID, Biography) + 인용형식 검증 추가. RSC TOC entry도 함께 보완.
- IEEE Access는 메가저널이라 티어 1에서 제외, MDPI에 준하는 조건부 취급.

---

## v6.6 — 2026-07-18

Humanize EN v2.0 → v3.0. 2026 탐지 문헌(academic-humanizer, harshaneel/humanize, 50+ peer-reviewed)을 반영했다. 핵심은 프레이밍 갱신 — 현대 학습형 탐지기(GPTZero 2025, Pangram)가 실제 잡는 것은 perplexity가 아니라 RLHF·instruction-tuning 흔적이다(arXiv 2605.19516).

- EN-S1-D: RLHF 보이스 제거 (불필요 균형·과잉 구조화·공손 헤징·완충 오프너·무내용 마무리). 최고 레버리지, 기존 최대 공백.
- Claim↔Evidence 동사 보정: 데이터보다 강한 동사 금지(prove → show empirically), 근거 없는 크기 형용사는 실측 수치로 귀속. VerifiedRegistry 연동.
- 학술 보이스 보호 목록: 과잉교정 방지 가드레일. 근거 헤징·수동태·we·기호·인용은 불가침.
- EN-S1-E: 미수록 텔 4종 ("In recent years" 오프너, 과장 구문, 분사구 꼬리, 필러 전환어).
- Best-of-N (선택, 기본 비활성): 고위험 단락 3~5 변형 중 AI-tell 최저본 선택.

정직한 전제 명시: 순수 규칙은 학습형 분류기를 완전 무력화 못 한다. 목표는 탐지 회피가 아니라 리뷰어가 느끼는 자연스러움과 문장 품질.

---

## v6.5 — 2026-06-18

### 새 기능

**Step 2: 저널 선정 우선순위 원칙 추가**
타깃 저널 제안 시 ACS → RSC → Elsevier → Springer Nature 순서를 기본값으로 적용한다. MDPI는 Ku가 명시적 사유를 제시할 때만 허용하며, 조건 없이 1순위 제안하는 것을 금지한다.

**Step 7: CiteCheck Layer 0 자동 인용 감사 추가**
기존 3층 인용 검증이 4층으로 업그레이드됐다. Layer 0에서 `citecheck-cli`(color4-alt/CiteCheck, MIT)가 전체 인용을 자동 스캔(CrossRef → SemanticScholar → OpenAlex → PubMed → arXiv → dblp)하고, ❌ 항목만 Layer 1 수동 검증으로 넘긴다. GATE 7 통과 조건에 "Layer 0 오류 0건" 항목이 추가됐다.

**Humanize EN v1.0 → v2.0: Writing Quality Check 4종 추가**
Imbad0202/academic-research-skills v3.7.0의 Writing Quality Check를 통합했다. 기존 S1/S2 패턴 탐지와 독립 실행.
- WQ-1: em dash 전체 ≤3회
- WQ-2: throat-clearing opener 7패턴 금지 ("It is worth noting that..." 등)
- WQ-3: synonym cycling 탐지 (동일 개념 무의미 동의어 교체)
- WQ-4: Rule of Three 반복 / 단락 길이 균일 / "Future studies" 남발 경고

Step 5 실시간 점검 및 Step 7 pre-submission 체크리스트, 완료 보고 박스에 WQ-1~4 항목이 포함된다.

---

## v6.4 — 2026-05-29

Humanize EN v1.0 추가 (AI 탐지 방지 시스템, 30패턴 + perplexity/burstiness 과학 기반). MODEL ROUTING 섹션 제거 (Cowork 단일모델 환경 반영).

## v6.3 — 2026-05

SciencePlots/cnsplots 저널 스타일 통합 (Step 6). AutoSurvey2 4단계 문헌 수집 강화 (Step 1). OUTLINEFORGE 계층 아웃라인 선행 승인 절차 (Step 5).

## v6.2 — 2026-04

Humanize KR v1.6.1 업데이트 (신규 패턴 9건, KatFish/LREAD 기반 정량 지표 8개, Fast/Strict 모드).

## v6.1 — 2026-04

VerifiedRegistry 허구 방지 절대 규칙 전 단계 적용. Step 7 4계층 인용 검증 강화. Step 8 Accept 확률 정량 평가.

## v6.0 — 2026-04

저널 페르소나 시스템 도입 (에디터/과학자 2층 아키타입, 실시간 독해 시뮬레이션, Step 2~8 동행).

## v5.x — 2026-03~04

v5.5 에디터·독자 공감 설계 절대 지침 (Audience Profile). v5.6 탑티어 저널 Figure 규격화 DB. v5.7 그래프 유형별 세부 규격. v5.8 Humanize KR v1.1 (60+ 패턴). v5.9 AutoResearchClaw v0.4.0 통합 (SmartPause, 3층 인용 검증, 3관점 채점).
