# 파이프라인 v7.1 prompt-audit (2026-10-03)

대상: `pipeline/system_prompt.md` (v7.1, 140,400B, 2,529행) · `claude_research/CLAUDE.md` · `~/.claude/skills/ku-pipeline/SKILL.md`
기준: Cowork → Claude Code 이전, 새 기본 모델(Opus 5.5), 문서 내부 모순
이 문서는 진단만 담는다. 원본 지침은 아직 수정하지 않았다.

우선순위: 🔴 지금 고칠 것 · 🟡 v7.2에 넣을 것 · ⚪ 선택

---

## A. 환경 (Cowork 전제가 남은 곳)

**🔴 A1. 정본 사본이 두 개다**
- `claude_research/ku-cowork-pipeline/` (CLAUDE.md가 import)
- `~/.claude/skills/ku-pipeline/repo/` (ku-pipeline 스킬이 읽음)

지금은 둘 다 `1fa91d0`이라 같다. 한쪽만 고치고 push하면 다른 쪽은 구버전으로 남는다. 루트/pipeline 혼동 사고(3회)와 같은 구조다.
→ 하나로 통일. 스킬이 `claude_research` 사본을 읽게 하고 스킬 안의 `repo/`는 삭제.

**🔴 A2. 로드 전략이 두 갈래로 충돌**
- CLAUDE.md: `@…/system_prompt.md`로 140KB 전문을 **매 세션** 자동 로드 [추정: 약 5만 토큰 내외]
- 스킬: "2,500행 전체를 매번 읽지 않는다, 필요한 섹션만"

지금은 둘 다 일어난다. 파이프라인과 무관한 세션(GitHub 조사, 메일 정리)에서도 5만 토큰이 먼저 깔린다.
→ CLAUDE.md는 import 줄을 빼고 "연구 작업이면 ku-pipeline 스킬로 시작" 한 줄로 바꾼다. 공통 절대 규칙(VerifiedRegistry 등)만 별도 파일로 떼어 import.

**🟡 A3. Cowork 전용 문구 (스킬이 매번 치환 중 → 정본에 흡수)**

| 위치 | 현재 | Code에서 |
|---|---|---|
| 정체성 | "Cowork 환경에 적용한 연구 파트너" | Claude Code |
| [시작-1] | GitHub API curl로 지침 로드 + 버전 대조 | `git pull --ff-only` + 2행 버전 보고 |
| [시작-4]·FPA·SELFCITE·REVISION | `web_fetch api.github.com/…` (5곳) | 로컬 `pipeline/metaclaw/*.json` 읽기 |
| FPA-2 | "GitHub API PUT으로 **즉시** 업데이트" | 로컬 수정 → **Ku 승인 후** commit·push (스킬 규칙과 정본이 지금 모순) |
| V-TEX | "Cowork 샌드박스에서 실행" | 로컬 실행 |
| Step 4 | "Cowork 채팅창에 직접 출력", GitHub 웹 업로드 가이드 | 직접 `git init`/push 실행 (승인 후) |
| 세션 종료 | "메모리 업데이트" | 프로젝트 `pipeline_state.json` 갱신 |

**🟡 A4. 저장 구조 규칙이 세 개**
- 정본 [시작-2]: 바탕화면 `SAVE_ROOT/Step1~8/`
- CLAUDE.md: `claude_research/<코드네임>/{data,code,figure,latex,upload}`
- 스킬: "기존 체계 유지, 새 프로젝트만 StepN/"

→ CLAUDE.md 방식으로 일원화 권장(실제 프로젝트들이 이미 이 구조). 단계 산출물 위치는 `pipeline_state.json`의 `outputs`에 기록.

**🔴 A5. GATE에 필요한 도구가 이 PC에 없다**

| 도구 | 쓰는 곳 | 상태 |
|---|---|---|
| pdflatex, bibtex | V-TEX 1~4 (LaTeX 코드 제공 전 필수) | 없음 |
| node / npx | EN-SCORE (Step 7 임계 ≤40) | 없음 |
| citecheck | Step 7 Layer 0 | 없음 |
| detex | EN-SCORE 본문 추출 | 없음 |
| python 3.13 | 전반 | 있음 |

지금 상태로는 GATE 7을 정본대로 통과시킬 수 없다. 설치하거나 대체 경로를 정본에 명시해야 한다.
(설치 명령 `pip install citecheck-cli`, `npx skills add …` 자체도 실재 확인 전)

---

## B. 문서 내부 모순

**🔴 B1. 자기인용 DB 버전 기준**
- 정본 1484행: `_meta.version ≥ 2.1` / CLAUDE.md: `≥ 2.3`
- 1490행 `assert m['version'] >= '2.1'` 는 **문자열 비교**다. DB가 2.10이 되면 `'2.10' >= '2.3'`이 False라 정상 DB를 구버전으로 판정한다.
→ 2.3으로 통일 + `tuple(map(int, v.split('.')))` 비교.

**🟡 B2. "3층" 인용 검증 (3곳)** — Step 7 헤더·GATE 8 조건이 "3층"인데 실제는 Layer 0~4, 5층. GATE 8이 3층만 확인하면 된다고 읽힐 수 있다.

**🟡 B3. Figure 설정 충돌**
- 1232행 `constrained_layout=True 필수` ↔ 1229행 `subplots_adjust(hspace=0.55, wspace=0.38)`: matplotlib에서 constrained layout을 켜면 subplots_adjust는 무시되고 경고가 난다. 둘 중 하나만.
- rcParams `font.size 8` (저널 인쇄 규격) ↔ `figsize=(20,10)`, `FS_LABEL=26`, 패널 레이블 28pt: 인쇄 크기 규격(3.5in 단일 칼럼)과 화면용 대형 설정이 한 블록에 섞여 있다. "작업용 미리보기"와 "투고용 최종"으로 프로파일을 나눠야 한다.

**🟡 B4. 1684행 "Step 6 (리비전·리뷰 대응)"** — v7.0부터 리비전은 STEP R. Step 6은 Figure·제출물.

**🟡 B5. Humanize EN 규칙끼리 충돌**
- EN-S1-A가 robust·comprehensive·highlights·ensures를 "1개만 있어도 제거" ↔ v4.0 GUARD/EN-AC는 문맥 판단. S1-A가 더 앞에 있어 기계적 일괄 삭제를 부른다.
- "Perplexity 향상 규칙" ↔ v6.6 스스로 "perplexity 프레임은 stale"이라고 결론.
- EN-S1-E `Notably,` 금지 ↔ G-4 허용(단서 조항으로 봉합만 됨).
→ v6.4~v7.1이 덧붙이기로 쌓여 있다. 한 목록으로 재편(우선 G-1~G-4 → 그다음 패턴).

**⚪ B6. 섹션 순서** — Step 4 섹션이 Step 5·6 뒤(약 640행 이후)에 있다. 단계 순서로 재배치하면 필요한 섹션만 읽기 쉬워진다(A2와 연동).

---

## C. 새 모델(Opus 5.5) 관점

**🟡 C1. 강조 표지 과다** — `금지` 94 · `필수` 42 · `절대` 23 · `⛔` 17회.
예전 모델용으로 세게 쓴 표현이다. 최신 모델은 지시를 글자 그대로 따르므로 과잉 적용 위험이 있다(사소한 일에도 SmartPause, 데이터 그림까지 AI 정책으로 막기 등). 진짜 절대 규칙(VerifiedRegistry, 공시 진실성, 자기인용 저자 대조, push 승인)만 강조를 남기고 나머지는 평서문으로.

**🟡 C2. 헤더 변경이력 45행** — 모델에게는 판단 근거가 아니라 소음. `RELEASE_NOTES.md`로 이동하고 헤더는 버전·날짜 3줄만.

**⚪ C3. 단계별 모델 선택 재도입 가능** — v6.4에서 "Cowork 단일 모델"이라 뺐지만 Code는 `/model` 전환이 된다. 예: 검증·포맷(Step 7 Layer 0~4, DB 감사) = Sonnet 5.5 / 설계·집필·채점(Step 1·3·5·8, STEP R1) = Opus 5.5.

**🟡 C4. 공시 도구 표기** — 예시를 실제 모델명 기준으로: `Claude (Anthropic, Claude Opus 5.5, accessed 2026-10)`. 세션에서 실제로 쓴 모델을 기록하도록 `pipeline_state.json`에 `models_used` 필드 추가.

---

## D. 사실 확인이 필요한 서술

**🟡 D1. v6.9 워터마크 서술** — "2026-08-02부터 Claude 전 제품 생성 텍스트에 SynthID-Text 방식 워터마크(EU AI Act 50조)". 정본에 출처가 없다. SynthID-Text는 Google DeepMind 기술명이라 Claude 제품 설명으로는 확인이 필요하다. 공시 의무 원칙 자체는 출판사 정책만으로 성립하므로, 근거를 확인할 때까지 이 문단은 "출판사 공시 의무"를 근거로 다시 쓰는 편이 안전하다.

**⚪ D2. 저장소 정리 후보** — `pipeline/system_prompt_v6.0.md`(구버전)가 정본 옆에 있다. 잘못 열릴 위험. 루트의 `figure_rules.md`, `cross_provenance_audit_smoke.json`, `ku_publications_update_report.json`, `download`도 역할 확인 필요.

---

## 권장 v7.2 범위

1. A1·A2: 정본 단일화 + 전문 import 제거(스킬 기반 필요 섹션 로드)
2. A3·A4: Cowork 문구 → Claude Code, 저장 구조 일원화
3. B1~B5: 모순 수정
4. C1·C2·C4: 강조 정리, 변경이력 분리, 공시 표기
5. A5: 도구 설치 또는 대체 경로 명시 (설치는 Ku 확인 후)
6. (선택) C3 모델 선택, D1 근거 확인, D2 저장소 정리
