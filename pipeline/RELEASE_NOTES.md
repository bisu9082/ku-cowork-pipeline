# AutoResearchClaw Pipeline — Release Notes

---

## v7.3: 2026-10-27

Google Research가 2026-10-14 공개한 Deep Review를 검토했다. **서비스는 채택하지
않고 구조만 가져왔다.**

- **[PAT-REVIEW] 신설.** Jayaram et al. (2026) arXiv:2606.28277의 Paper Assistant
  Tool 구조를 Claude Code 서브에이전트로 구현했다. 의미 세그먼트 분할, 전문
  컨텍스트 + 단일 세그먼트 담당, 적응 예산, 병렬 실행, 근거 통합. SPOT 벤치마크
  Math/CS에서 같은 모델의 오류 검출률이 55.2%에서 89.7%로 오른 구조다.
  Step 4(REPRO-AUDIT 직후)와 Step 8(Phase 0 신설) 두 곳에 걸었다.
- **발견 형식 고정.** 발견 1건마다 원문 직접 인용, 신뢰도, 그리고 `내가 틀렸다면`
  (이 발견이 거짓이 되려면 무엇이 참이어야 하는가)을 요구한다. 인용이 없거나
  반증 칸이 빈 발견은 통합 단계에서 등급을 낮추지 않고 폐기한다.
- **환각 가드 3종.** PAT가 문서한 실패 양상을 금지 규칙으로 적었다. 확인 없이
  outdated 선언, 참고문헌 발명, 이해 실패를 오류로 선언.
- **Deep Review 호스팅 서비스 업로드 금지.** 미투고·심사중·공저자 원고를 외부
  리뷰 서비스에 올리지 않는다. Deep Review는 로컬 버전이 없고 Gemini API 키는
  요금 결제 수단일 뿐 실행 위치를 바꾸지 않는다. 구글은 최대 1년 보관을 명시한다.
  [외부 행위 승인] 절대 규칙에 포함시켰다.
- **REPRO-AUDIT A6 검증 원장 추가.** ajogalekar/claude-codex-loop의 원장 규율에서
  가져왔다. 입력·코드·산출물 해시, 결함 ID 이월, 이전 원장 해시 체인.
  "PASS 라벨로 완료를 추론하지 않는다", "리뷰 후 파일이 바뀌면 그 리뷰는 무효",
  "라운드 소진은 통과가 아니라 미완료 중단". 같은 저장소의 시간당 자율 루프는
  채택하지 않았다. Codex 인증 세션과 UI 조작을 요구하고, 검증이 시뮬레이션
  단계이며, README 스스로 "두 모델의 의견으로 진실을 확립할 수 없다"고 적는다.
- **중복 제거.** Step 4 Cross-Model Review에서 재현성·seed·누설·검정력 질문을
  빼고 REPRO-AUDIT A1·A5로 넘겼다. Claim Verification 3항목(Citation·Numerical·
  Claim grounding)은 삭제했다. Step 7 Layer 1·2·3이 원고 전수로 수행하고 수치
  대조는 A3가 담당하므로 같은 질문을 세 번 묻던 구조였다. Step 8 Phase 4 수치
  매트릭스는 Phase 0 S3 세그먼트 산출물을 받아 쓴다. Step 8 Phase 1 비판자
  관점은 Phase 0 발견 목록에서 고르고 새로 상상하지 않는다.
- **시점 경계 명시.** 수치 대조가 A3·Layer 2·Phase 0 S3 세 곳에 나오는 것은
  중복이 아니라 시점이 다르기 때문임을 표로 적었다. A3는 쓰기 전(수치 확정),
  Layer 2는 쓴 뒤(집필 드리프트), Phase 0 S3는 조판 뒤(원고 내부 일관성).
  Step 8 Phase 1의 재현성 질문도 남겼다. A1·A5는 실제 재현 여부를,
  Phase 1은 원고가 그 사실을 서술하는지를 본다.

개정 직후 독립 감사에서 잡아 고친 것:
- **Step 4 세그먼트 범위.** PAT-REVIEW를 Step 4에도 걸면서 S5(주장-근거)·
  S6(프레이밍)이 함께 딸려갔다. Step 4는 집필 전이라 검증할 문장이 없는데
  GATE 4가 "치명 0건"을 요구해 **원리상 충족 불가능한 조건**이 됐다.
  실행 시점 표를 넣어 Step 4는 S1~S4(산출물 축), Step 8은 S1~S6(원고 축)으로
  갈랐다. Step 4의 S3은 본문 수치가 아니라 산출물과 표·Figure 초안을 본다.
- **SmartPause 조건 6종 → 7종.** 7번(PAT-REVIEW 치명)을 추가하면서 규칙 강도
  해석 절의 "발동 조건 6종에만" 문구를 고치지 않았다.
- **세션 시작 카드 버전 스탬프** v7.2 → v7.3.
- **검증 원장의 라운드 상한.** "라운드 수 소진은 미완료 중단"이라고 썼으나
  상한이 정의된 적이 없고 PAT-REVIEW는 명시적 무제한이다. 상한을 두지 않고
  "열린 결함을 남긴 채 중단하면 미완료 중단으로 적는다"로 고쳤다.
- **치명 의심의 조용한 폐기.** 인용 미확보 발견을 폐기하는 규칙이 치명 의심까지
  삼킬 수 있었다. 폐기 사실을 한 줄 남기도록 했다. GATE는 막지 않는다.
- **SmartPause 수치 불일치 허용 오차.** 기존 ±5%가 REPRO-AUDIT A3의 ±0.01과
  어긋나 있었다. 더 엄격한 A3 기준으로 통일했다.

미처리 (기존 결함, Ku 판단 대기):
- GATE 0·2·3·5·6이 정의되지 않은 채 "GATE CLEARED"를 전 단계에 요구한다
- STEP 0 진입점 [A]·[C]가 중간 GATE를 건너뛰는데 예외 조항이 없다
- Figure 막대 상단 여유가 y_max*1.15(P1 절)와 data*1.2(그래프 유형별 절)로 다르다
- Humanize KR 적용 범위가 "논문 제외"와 "국문 논문 텍스트 포함"으로 상충한다
- Turnitin Low/Med/High를 0~100 점수로 대체했다면서 보고 양식에 등급이 남아 있다
- citecheck 도구 설명이 Layer 1~4 수행이라 적혀 있으나 Layer 3은 API로 불가능하다

---

## v7.2: 2026-10-03

Cowork 종료에 맞춰 Claude Code 기준으로 정리하고, prompt-audit(audits/2026-10-03_prompt_audit.md) 1~5항을 반영했다.

- **논문 텍스트 공통 규칙 신설.** em dash(—, LaTeX `---`)는 논문 텍스트에서 0회. 기존 EN-WQ-1(≤3회), Humanize KR(1~2회)을 대체한다. 논문 텍스트(본문·SI·캡션·커버레터·리뷰어 응답·공시문)를 한 문장이라도 쓰거나 고칠 때마다 Humanize 점검을 실행하고 결과 블록을 함께 보고한다.
- **규칙 강도 해석 신설.** 절대 규칙 6개(VerifiedRegistry, 자기인용 검증, 공시 진실성, GATE, 외부 행위 승인, 논문 텍스트 규칙)와 사유를 밝히면 벗어날 수 있는 기본값을 구분했다.
- **Claude Code 환경으로 전환.** [시작-1]을 GitHub API 로드에서 로컬 clone `git pull`로 바꿨다. metaclaw JSON은 로컬 파일로 읽고, 지식베이스 갱신은 즉시 PUT이 아니라 Ku 승인 후 commit·push로 바꿨다. 세션 상태는 메모리 대신 프로젝트 `pipeline_state.json`에 기록한다.
- **정본 단일화.** clone은 `claude_research/ku-cowork-pipeline` 하나. ku-pipeline 스킬도 이 clone을 읽는다.
- **저장 구조 일원화.** 바탕화면 `SAVE_ROOT/Step1~8`을 `claude_research/<코드네임>/{data,code,figure,latex,upload}`로 바꿨다.
- **도구 요건 명시.** pdflatex·bibtex·Node.js·citecheck·detex가 없을 때의 대체 경로를 적고, 도구가 없다는 이유로 GATE를 통과 처리하지 않도록 했다.
- **모순 수정.** 자기인용 DB 기준을 2.3으로 통일하고 버전을 숫자로 비교한다(문자열 비교는 2.10을 구버전으로 판정함). 인용 검증 "3층" 표기를 "5층(Layer 0~4)"으로 고쳤다. Figure 설정을 투고용 P1과 검토용 P2로 나눠 constrained_layout과 subplots_adjust 충돌을 없앴다. 리비전 대응을 Step 6이 아니라 STEP R로 고쳤다. Humanize EN의 S1-A 어휘 목록을 문맥 판단으로 바꾸고, Notably 규칙을 G-4와 맞췄다.
- **공시 표기.** 모델명 예시를 Claude Opus 5.5로 바꾸고, 실제 사용 모델을 `models_used`에 기록하도록 했다.
- **헤더 정리.** 지침 헤더의 v5.5~v7.1 변경 이력을 이 파일 하단으로 옮겼다. 지침 본문의 em dash 구분자도 콜론으로 바꿨다.

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

---

## 부록: v5.5~v7.1 지침 헤더 이력 (2026-10-03 system_prompt.md에서 이관)

```
# Claude Cowork × AutoResearchClaw 논문 자동화 파이프라인 v7.1
# 기반: github.com/aiming-lab/AutoResearchClaw v0.4.0
# 저장소: github.com/bisu9082/ku-cowork-pipeline
# 업데이트: 2026-09-19
# v5.5 추가: 에디터·독자 공감 설계 절대 지침 (Audience Profile 시스템)
# v5.6 추가: 탑티어 저널 Figure 규격화 DB (9개 저널 Guidelines 실측 기반)
# v5.7 추가: 그래프 유형별 세부 규격 완전판 (bar/line/scatter/heatmap/box/pie/SHAP/histogram 등)
# v5.8 추가: 한글 작성 AI 문체 제거 원칙 (Humanize KR v1.1, 60+ 패턴 10카테고리)
# v5.9 추가: AutoResearchClaw v0.4.0 통합: Step4 Cross-Model Review,
#            Step7 3층 인용 검증, Step8 3관점 채점 강화, SmartPause 시스템
# v6.0 추가: 저널 페르소나 시스템: 에디터·저명과학자 아키타입 기반
#            2층 페르소나(에디터/과학자) + 실시간 독해 시뮬레이션 + Step2~8 동행
# v6.1 추가: VerifiedRegistry 허구 방지 절대 규칙 (전 단계 공통)
#            Step7 4계층 인용 검증 강화 (arXiv→CrossRef→SemanticScholar→LLM)
#            Step8 Accept 확률 정량 평가 + Aims/Scope 적합도 + 데이터 일관성 검증
# v6.2 추가: Humanize KR v1.6.1 업데이트: 신규 패턴 9건(C-11/C-12/D-7/E-5/E-6/
#            F-4/G-3/H-3/I-4) + KatFish·LREAD 기반 정량 지표 8개 + Fast/Strict 모드
# v6.3 추가: SciencePlots/cnsplots 통합: Step6 저널별 matplotlib 스타일 자동 적용
#            AutoSurvey2 4단계 문헌 수집 강화: Step1 섹션별 retrieval-guided 계획
#            OUTLINEFORGE 계층 아웃라인: Step5 본문 작성 전 H1/H2/H3 선행 승인
# v6.4 추가: Humanize EN v1.0: 영문 논문 AI 탐지 방지 시스템
#            출처: github.com/Aboudjem/humanizer-skill (30패턴+perplexity/burstiness과학)
#            학술논문 특화 패턴 추가 + Step5 실시간 적용 + Step7 pre-submission 점검
#            MODEL ROUTING 섹션 제거: Cowork 단일모델 환경 반영 (2026-05-29)
# v6.5 추가: CiteCheck Layer 0: Step7 자동 인용 감사 (color4-alt/CiteCheck CLI 통합)
#            Humanize EN v2.0: Writing Quality Check 4종 추가
#            (em dash ≤3 / throat-clearing opener / synonym cycling / 구조 패턴)
#            Step2 저널 선정 우선순위: ACS→RSC→Elsevier→Springer Nature, MDPI 최소화
# v6.6 추가: Humanize EN v3.0: 2026 탐지 문헌 반영 (미묘·비탐지 방향 집중)
#   출처: AIScientists-Dev/academic-humanizer + harshaneel/humanize (50+ 문헌, ~2026-04)
#   핵심전환: 현대 학습형 탐지기는 perplexity가 아닌 RLHF·instruction-tuning 흔적을 잡음
#     → [Lever9] RLHF 보이스 제거 (EN-S1-D 신설): 최고 레버리지
#     → Claim↔Evidence 동사 보정 (데이터보다 강한 동사 금지)
#     → 학술 보이스 보호 목록 (과잉교정으로 엄밀성 훼손 방지 가드레일)
#     → 미수록 AI 텔 4종 (In recent years 오프너/구문텔/분사구 꼬리/필러전환)
#   정직한 전제: 순수 규칙은 학습형 분류기 완전무력화 불가 → 목표=리뷰어 자연스러움+품질
# v6.7 추가: IEEE 저널 티어1 격상 (ACS·RSC와 동급, 서열 없음)
#            Step2 티어 구조 재편 + IEEE 선택 가이드(TIM/Sens.J./TNS/TGRS/TNNLS/JBHI)
#            IEEE Figure 규격(3.5in/7.16in·(a)(b)(c)·DPI) + IEEEtran LaTeX 구조
#            IEEE 제출 패키지(Index Terms/ORCID/Biography) + 인용형식 검증
#            ※ IEEE Access는 메가저널: 티어1 제외, MDPI 준하는 조건부
# v6.8 추가: SELFCITE-AUDIT: ku_publications.json 무결성 감사 (필수)
#   계기: 2026-07-19 감사서 허구 DOI 13건 적발(타인 논문 연결/미등록)
#   verified 필드 없으면 self-cite 금지 · under_review 논문 인용 절대금지
#   트리거 3종: Step1 진입 시 / DB 추가 시 / 분기 1회 전수
#   CrossRef 저자 대조(Kang 포함 여부)로 판정 · 허구 1건도 SmartPause
# v6.8.1 추가: 배포 검증서 발견한 2개 함정 방어 (2026-07-19)
#   ① CDN 캐시: raw.githubusercontent 구버전 반환 (v6.8.2에서 API 전환으로 대체됨)
#   ② 경로 불일치: DB 정본은 pipeline/metaclaw/ 고정, 루트 사본 읽지 말 것
#      (루트에만 업데이트해 허구 DOI가 live로 남은 실제 사고 반영)
# v6.8.2 개정: raw.githubusercontent 사용 금지 → GitHub API contents 엔드포인트
#   v6.8.1의 ?t=[난수] 캐시우회가 실제로 작동하지 않음을 실측 확인(2026-07-19)
#   raw는 쿼리 변경·대기에도 구버전 반환, 동시각 API는 최신 반환
#   → 정본 로드·존재확인은 contents / git-trees API로 일원화
# v6.9 추가: AI-DISCLOSURE: AI 사용 공시 시스템 (필수, 투고 차단 리스크 해소)
#   배경: 2026-08-02~ Claude 전 제품 생성텍스트에 워터마크 삽입(EU AI Act 50조)
#         + 주요 출판사 전부 AI 사용 공시 의무화 → 파이프라인에 공시 기능 부재였음
#   핵심: 공시가 방패다. 공시되면 마크 검출은 진술과 일치하는 정상 상태.
#         ⛔ 워터마크 제거·회피 처리는 수행하지 않는다(무의미하며 은폐 정황)
#   출판사별 공시 위치·양식 5종 + 진실성 원칙(축소기재 금지)
#   Step2 요건감지 → Step6 문안생성 → GATE7 누락검증
#   Figure AI 정책 3분류: 데이터그림 허용 / 원자료 금지 / GA 범용genAI 금지
# v7.0 추가: 다각도 감사로 발견한 3개 갭 해소 (2026-08-15)
#   ① [STEP R] 리비전 트랙 신설: 파이프라인이 신규논문 전용이었음.
#      Ku 활성 프로젝트 절반이 리비전인데 워크플로우 부재.
#      R0 코멘트해체 → R1 전략 → R2 Response → R3 revblue → R4 GATE R → R5 제출
#      메모리에만 있던 확립 규칙(별도폴더·Response/Changes·0070C0·ML방어우선) 이식
#   ② Step7 Layer 4 철회 검증: CrossRef updated-by(무료). 철회 인용 0건 GATE 조건
#   ③ Step3 방법론 레지스트리: AL·GNINA·TSFM대조군·DFT보고항목 기본값 명시
# v7.1 추가: (2026-09-19) GitHub 조사 기반 3종
#   ① Humanize EN v4.0: matsuikentaro1/humanizer_academic v1.4.0 이식
#      EN-AC-1~6(LLM어휘·압축표현·환언반복·무내용평가문·장식부사·서식)
#      ★EN-AC-GUARD G-1~G-4 과잉교정 방지 = 교정이 글을 망치는 것 차단
#      근거가 실측: Matsui 2025 Perspect Med Educ(PubMed 어휘변화 정량)
#   ② EN-SCORE: Aboudjem CLI 0~100 결정론 점수로 주관 Low/Med/High 대체
#      Step7 임계 ≤40. 단 GUARD 미통과 시 점수 무관 불통과
#   ③ REPRO-AUDIT: Step4 계산 재현성 5축 감사(referee2/code-review 기반)
#      chelator2 하드코딩상수·원고수치 불일치 재발 방지, GATE4 조건 편입
```
