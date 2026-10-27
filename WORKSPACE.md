# Ku 연구 작업공간 규칙 (정본)

이 파일이 작업공간 규칙의 **정본**이다. 각 폴더의 `CLAUDE.md`는 이 파일을 가리키는
스텁이고, 내용은 여기만 고친다. git으로 버전이 남고 맥미니에도 같은 파일이 간다.

갱신: 이 파일을 고치고 `cd ku-cowork-pipeline && git add -A && git commit && git push`
(push는 Ku 승인 후. 절대 규칙 5)

- 파이프라인 절대 규칙: `pipeline/ABSOLUTE_RULES.md` (상시 로드)
- 파이프라인 전문: `pipeline/system_prompt.md` (연구 작업 시 로드)
- 변경 이력: `pipeline/RELEASE_NOTES.md`

---

## 작업 폴더

연구용 폴더가 **두 곳**이다. 둘 다 Ku의 작업공간이고 용도가 다르다.

| 폴더 | 경로 | 용도 |
|---|---|---|
| `claude_research` | `C:\Users\kkaan\Downloads\claude_research` | 파이프라인 clone, 대다수 프로젝트 |
| `## research` | `C:\Users\kkaan\OneDrive\Tài liệu\Claude\Projects\## research` | ARGUS 등 일부 프로젝트, 투고 패키지 |

새 프로젝트는 `claude_research` 아래에 만든다. 이미 다른 폴더에 있는 프로젝트는
옮기지 않고 그 자리에서 작업한다.

연구를 시작하면 **코드네임 폴더**를 만들어 정리한다. 코드네임은 짧은 소문자 한 단어.

```
<코드네임>/
├── data/      원데이터·중간 산출물
├── code/      분석 스크립트
├── figure/    Figure 원본·생성 코드
├── latex/     main.tex · myref.bib · SI.tex
└── upload/    투고 패키지
```

루트에 작업 파일을 흩뿌리지 않는다.

**WSL 주의**: `/mnt/c/` 아래는 I/O가 3~5배 느리다. 대용량 계산은 `~/`에서 돌리고
결과만 복사한다.

---

## 파이프라인

정본 clone은 **하나뿐**이다: `claude_research/ku-cowork-pipeline/`
ku-pipeline 스킬도 이 clone을 읽는다. 다른 위치에 clone을 만들지 않는다
(2026-10-03 스킬 내부 사본 제거).

최초 1회 설치:
```bash
cd ~/Downloads/claude_research
git clone https://github.com/bisu9082/ku-cowork-pipeline.git
```

갱신:
```bash
cd ku-cowork-pipeline && git pull --ff-only   # 최신 지침 받기
cd ku-cowork-pipeline && git push             # 지침 수정 후 (Ku 승인 후)
```

⚠️ 정본 경로는 `pipeline/` 아래다. 저장소 루트에 같은 이름 파일을 만들지 않는다.
루트/pipeline 혼동으로 구버전이 로드되는 사고가 세 번 있었다.

⚠️ 구버전 변종은 `archive/`에 있다. 정본 옆에 두지 않는다.

---

## 세컨드 브레인 볼트 (Obsidian)

정본: `C:\Users\kkaan\Desktop\my second brain` (맥미니는 `~/second-brain`)
GitHub: github.com/bisu9082/ku2ndbarin (private)

**세션 중 프로젝트 상태가 바뀌면 그 자리에서 볼트를 갱신한다.** 세션 끝까지 미루지
않는다. 파일 접근이 없으면 볼트 폴더 연결을 먼저 요청한다.

갱신 대상은 `01-Projects/<코드네임>.md` 하나다.

| 상황 | 할 것 |
|---|---|
| 투고·제출함 | `status: 심사중`, `updated` 오늘 날짜 |
| 리비전 받음 | `status: 리비전`, `deadline: YYYY-MM-DD` 기입 |
| 억셉·리젝 | `status: 게재확정` 또는 재타깃 상태, `journal` 갱신 |
| 새 할 일 생김 | 본문 "다음 할 일"에 `- [ ] 내용` 추가 |
| 중요한 판단·수치 확정 | 본문 "핵심 메모"에 한 줄 누적 (덮어쓰지 말 것) |

**새 프로젝트를 시작하면** 볼트 노트와 작업 폴더를 같은 코드네임으로 동시에 만든다.
노트는 `99-Templates/프로젝트 템플릿.md`를 복사해 쓴다.

### 볼트에서 건드리지 말 것

- ⚠️ `## 메모리 카드 (전문)` 섹션은 Claude 메모리 추출본이다. **지우지 않는다.**
- ⚠️ 대시보드(`90-Dashboards/`)는 Dataview가 자동 생성한다. **직접 고치지 않는다.**
- ⚠️ `build_vault.py`를 **재실행하지 않는다. 노트를 덮어쓴다.**
  예외: `90-Dashboards/전체 프로젝트.md`는 고정 목록이라 프로젝트가 늘거나 줄면
  갱신이 필요하다. 그때만 레지스트리를 고치고, "핵심 메모"가 쌓인 노트를 제외하도록
  손본 뒤, **Ku 승인을 받고** 돌린다. 기본은 재실행 금지다.
- **파일을 볼트로 옮기지 않는다.** 원본은 원래 폴더에 두고 경로만 적는다.

### 브리핑

브리핑 생성기는 `claude_research/Claude outputs/daily_brief.py`다.
"오늘 브리핑" 요청을 받으면 이것을 실행한다.

---

## 자기인용 DB

정본: `ku-cowork-pipeline/pipeline/metaclaw/ku_publications.json`
규칙은 `pipeline/ABSOLUTE_RULES.md` 2절에 있다. 요약: verified 필드 + DOI 리졸브 +
**저자 Kang 대조**. under_review 인용 금지. 국내지 미등록 DOI는 보존하고 인용 시 생략.

---

## 작업 습관

`pipeline/ABSOLUTE_RULES.md` 6절과 동일하다. 요약:
한 단계씩 · 수치는 재현 로그에서만 · ID는 API로 역검증 · 공저자 가정 금지 ·
파일 생성·수정 후 경로 알림.

---

## 프로젝트별 노트

| 작업 폴더 | 볼트 노트 | 상태 |
|---|---|---|
| `## research/ARGUS/` | `01-Projects/ARGUS.md` | Analytical Chemistry, 집필 |
| `claude_research/deltaE/` | `01-Projects/deltaE.md` | 어레이 본 프로젝트, ARGUS의 모체 |

### ARGUS (Analytical Chemistry, in progress)

ARGUS는 `## research/ARGUS/`에 있다. `claude_research`에는 없다.

타깃은 **Analytical Chemistry** 단독 1편이다 (2026-10-17, Ku 기록).
ACS Sensors 2편 분할안은 해당 저널 어레이 SI 21편을 조사한 뒤 폐기했다.
그 저널 자체 데이터로 만든 ACS Sensors 논문은 정직하게 쓸 수 없다는 결론이었다.
ARGUS를 "ACS Sensors manuscript"라고 적은 지침이 있으면 그건 구버전이다.

Before doing anything in `ARGUS/`, read `ARGUS/HANDOVER.md` in full. It carries
the standing constraints on this project, including which data may and may not
be used, and it explains a verification apparatus that must not be routed
around. The project is nine review rounds deep and its checks encode what those
rounds found.

First command, always:

    cd ARGUS && python3 20_code/acs_verify_all.py --prove

Twelve checks and thirteen fault injections. If it is not green, fix that
before reading the manuscript: a red build means the text and the deposited
results disagree.
