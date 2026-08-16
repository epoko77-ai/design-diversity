---
name: design-diversity
description: >-
  Claude가 산출하는 PPT·웹사이트 디자인의 천편일률 문제를 해결하는 '디자인 팩 카탈로그' 제작 오케스트레이터.
  공개 디자인 시스템·비주얼 스타일을 수집·증류해, Claude Code에 복붙하면 그 스타일이 재현되는 디자인 팩
  (prompt.md + tokens.json + preview.png + meta.yaml)을 만들고, baseline 대조로 다양성을 검증한 뒤
  GitHub 공개 레포 + 카탈로그 웹사이트로 발행한다. 7인 에이전트 팀(소싱·스키마·PPT집필·웹집필·렌더·다양성QA·발행)을
  파이프라인으로 조율한다. 트리거 — "디자인 다양성", "디자인 팩", "디자인 팩 카탈로그", "디자인 시스템 카탈로그",
  "PPT 디자인 다양화", "웹 디자인 팩", "프롬프트형 디자인 시스템", "Claude 디자인 천편일률", "디자인 팩 만들어줘".
  후속 작업 — "팩 추가", "PPT 팩 N개 더", "웹 팩 추가", "특정 팩만 다시", "다양성 검증 다시", "팩 재집필",
  "스키마 변경", "카탈로그 사이트 재배포", "레포 갱신", "재실행"도 모두 이 스킬로 처리한다.
  단순 PPT 1건 제작은 korean-premium-deck, 단순 웹사이트 1건은 frontend-design을 사용한다.
---

# Design Diversity — 디자인 팩 카탈로그 오케스트레이터

공개 디자인 시스템을 수집·증류해 Claude Code 복붙용 '디자인 팩' 카탈로그를 만들고, 다양성을 검증한 뒤 GitHub + 웹사이트로 발행하는 7인 에이전트 팀을 조율한다.

## 핵심 산출물 (확정 규격)

각 디자인 팩 = `design-packs/{slug}/` 안의 4개 파일:
- `prompt.md` — Claude Code에 복붙하는 자기완결적 디자인 지시문 (SSOT 사용처)
- `tokens.json` — 머신리더블 디자인 토큰 (color/type/spacing/motion)
- `preview.png` — 실제 샘플 렌더
- `meta.yaml` — 카테고리·스타일 계열·출처·라이선스

규격 정의는 `design-pack-schema` 스킬이 SSOT다. 1차 출범 규모 = PPT 20 + 웹 20 = 40팩.

## 실행 모드

**에이전트 팀** (단일 팀 11인, 작업 의존성으로 파이프라인 표현). 팀원은 `SendMessage`로 직접 조율, 산출물은 `_workspace/` 및 `design-packs/` 파일로 공유, 진행은 `TaskCreate`/`TaskUpdate`로 추적.

| 에이전트 | 역할 | 주 스킬 | 모델 |
|---|---|---|---|
| design-scout | 후보 소싱 + 원본 적격 게이트 | design-sourcing | sonnet |
| reference-analyst | 원본 전수 정독·visual spec·변환 계약 | reference-analysis | **fable** |
| pack-architect | 스키마 SSOT·인덱스·상태 머신 | design-pack-schema | sonnet |
| ppt-pack-curator | standard PPT 팩 집필 | ppt-design-idioms | sonnet |
| web-pack-curator | standard 웹 팩 집필 | web-design-idioms | sonnet |
| reference-pack-curator | premium 레퍼런스 팩 집필 (1회 1팩) | reference-analysis + 트랙 idioms | **fable** |
| sample-renderer | 블라인드 재생 + 렌더 매니페스트 | sample-rendering | sonnet |
| craft-qa | 기계 검사 + 광학 검수 | craft-scoring | sonnet |
| fidelity-qa | 원본 대조 + 이종 모델 교차검증 | fidelity-scoring | **opus** |
| diversity-qa | baseline·팩 간 차별성만 | diversity-scoring | sonnet |
| catalog-publisher | 레포·사이트 발행 | catalog-publishing | sonnet |

**모델 배분 원칙.** 전원 최고 티어는 낭비다. 판단의 난이도가 높은 곳에만 상위 티어를 쓴다 — 원본을 처음 해석하는 `reference-analyst`, 그 해석을 지시문으로 옮기는 `reference-pack-curator`, 그리고 통과·반려를 최종 판정하는 `fidelity-qa`. 나머지는 정해진 절차의 집행이므로 sonnet으로 충분하다. 결정적 검사(해시·종횡비·페이지 수·`spec_version` 일치)는 **모델이 아니라 스크립트**가 한다.

**교차검증.** `fidelity-qa`는 집필자(Claude)와 다른 계열 모델을 2차 검증자로 세운다 — `codex exec -m gpt-5.6-sol`. 같은 모델이 자기 산출물을 채점하면 가짜 합의가 생긴다. 두 판정의 총점 차이가 4점 이상이거나 합격선 경계(22~24점)면 평균 내지 말고 `needs_human`으로 올린다.

## Phase 0: 컨텍스트 확인

작업 시작 전 `_workspace/`와 `catalog.json` 존재를 확인해 실행 모드를 정한다.

- **초기 실행** — `catalog.json` 없음 → 전체 파이프라인 (Phase 1~5).
- **후속 — 팩 추가** — `catalog.json` 있음 + "팩 N개 추가" → Phase 1(빈 축만 소싱) → 2~5를 신규 슬러그에만 적용. 기존 팩 보존.
- **후속 — 부분 재실행** — "특정 팩만 다시", "다양성 검증 다시" → 해당 슬러그·해당 Phase만 재호출. 시작 전 기존 `_workspace/`를 `_workspace_prev/`로 백업.
- **후속 — 스키마/사이트만** — "스키마 변경"→ pack-architect 단독 + 마이그레이션 보고. "사이트 재배포"→ catalog-publisher 단독.

부분 재실행 시 어느 Phase부터 도는지 사용자에게 1줄로 알리고 진행한다.

## 트랙 분기 — 먼저 `reference_mode`를 정한다

팩마다 근거의 성격이 다르고, **근거가 다르면 파이프라인이 다르다.** 집필 전에 `reference-analysis` 스킬의 4모드 중 하나를 확정한다.

- `style_synthesis` → **표준 트랙** (Phase 1 → 2 → 3). 원본이 없으므로 fidelity 채점 대상이 아니다.
- `exact_document` · `official_system` · `historical_canon` → **근거 트랙** (Phase 1 → 1.5 → 2R → 3). 근거 인벤토리 확보가 선행 조건이며 fidelity 게이트를 통과해야 한다.

근거 트랙 안에서 무엇을 정독하는지가 모드별로 다르다 — `exact_document`는 원본 페이지 전수, `official_system`은 토큰·컴포넌트·상태·뷰포트, `historical_canon`은 1차 자료 기반 원리·모티프 인벤토리.

## Phase 1: 소싱 + 적격 게이트 (design-scout)

design-scout에 트랙·목표 수를 할당한다.
- 출력: `_workspace/{batch}/01_scout_candidates.json` (탈락분과 탈락 사유 포함).
- 후보는 목표치보다 ~40% 많게 — 적격 게이트에서 상당수가 탈락한다.
- **`exact_document` 후보는 원본을 실제로 내려받고 종횡비·페이지 수를 실측한 것만 통과시킨다.** 링크 존재만으로는 후보가 아니다. PPT 트랙 종횡비 기준은 ≥1.6.

이 게이트를 안 돌려 A4 세로 문서를 덱으로 오인한 탓에 2팩을 폐기하고 후보 6건을 뒤늦게 버린 이력이 있다. **비율을 먼저 재라.**

## Phase 1.5: 원본 정독 (reference-analyst) — 레퍼런스 트랙 전용

1. 원본 전 페이지를 렌더(`pages_src/{code}/p-NN.png`)하고 **전부 본다.** 표본 정독 금지.
2. 페이지별 관찰을 `visual_spec/{code}.json`에 남긴다 — `observed`와 `inferred`를 분리한다.
3. 시그니처 모티프 3~7개를 `evidence_pages`와 함께 추출한다. 근거 페이지가 없는 모티프는 삭제.
4. `transform_contract/{code}.json` — 원본 요소별 preserve / adapt / substitute / drop. 상표·독점 사진·유료 폰트·공식 문구는 `preserve` 불가.
5. `page_mirror_plan` — 원본 N장 → 팩 M장 매핑. 병합했으면 `compression: merged`로 정직하게 적고 "1:1 mirror"라 부르지 않는다.

**이 산출물 없이 레퍼런스 팩 집필을 시작하지 않는다.** v1이 실패한 이유가 원본 없이 메타 추론으로 쓴 것이었다.

## Phase 2: 표준 팩 집필 (pack-architect → 두 curator 병렬)

1. pack-architect가 스키마를 잠그고 후보를 다양성 매트릭스로 솎아 `02_architect_selected.json` + `catalog.json` 갱신.
2. ppt-pack-curator·web-pack-curator가 **병렬로** 집필 → `prompt.md` + `tokens.json` + `meta.yaml`.
3. pack-architect가 포맷·라이선스·중복·`spec_version` 3자 일치를 검수. 위반은 반려·재집필(최대 2회).

배치는 트랙별 5팩 단위 — 배치마다 Phase 3을 이어 돌려 피드백을 빨리 받는다.

## Phase 2R: 레퍼런스 팩 집필 (reference-pack-curator) — 한 번에 1팩

`visual_spec` + `transform_contract` + `page_mirror_plan`을 입력으로 받아 집필한다.

- **관찰에 없는 것을 쓰지 않는다.** 정보가 부족하면 일반 원리로 메우지 말고 reference-analyst에 재정독을 요청한다.
- **원본이 일반 규칙을 어기고 있으면 원본이 옳다.** 그 이탈이 그 덱의 정체성이다. (`ppt-design-idioms`의 "본문 24pt+" 같은 일반 권고가 원본의 14pt 카드 본문을 덮으면 안 된다 — 실제로 `ppt-mcst`가 이 충돌을 안은 채 발행됐다.)
- **curator 인스턴스 하나는 한 슬러그만 처리한다.** 한 인스턴스가 여러 팩을 동시에 쓰면 시그니처가 섞인다. 서로 다른 슬러그는 독립 인스턴스로 병렬 처리해도 된다 — 격리 단위는 팩이지 배치가 아니다.

## Phase 3: 블라인드 렌더 + 3게이트 (sample-renderer → craft / fidelity / diversity)

각 팩(또는 배치)에 대해:

1. **블라인드 재생** — sample-renderer는 `prompt.md`+`tokens.json`만 받는다. **원본 이미지·visual_spec·집필자의 HTML을 보지 않는다.** prompt.md만으로 스타일이 안 나오면 그것이 팩의 결함이다. 렌더 소스 해시를 `render-manifest.json`에 남긴다.
2. **craft 게이트** (craft-qa) — 결정적 검사(A군) 먼저, 통과 시 시각 검수(B군). A군 hard fail이면 시각 검수에 비용을 쓰지 않는다.
3. **fidelity 게이트** (fidelity-qa) — 레퍼런스 트랙만. 원본 페이지 ↔ 팩 렌더 대조 + Codex 교차검증.
4. **diversity 게이트** (diversity-qa) — baseline 대비 차별성, 팩 간 쌍둥이 검사.

**게이트는 합산하지 않는다.** 높은 다양성이 낮은 충실도를 상쇄할 수 없다. 어느 게이트가 필요한지와 `status`를 어떻게 도출하는지는 **`design-pack-schema`의 상태식 절이 SSOT**다 — 여기에 식을 복제하지 않는다(모드마다 필요한 게이트가 다르고, 식을 여러 곳에 두면 한쪽만 고쳐진다).

반려 시 담당 curator가 수정 → 재렌더 → 재검증(팩당 최대 2회). 2회 후에도 미달이면 `reject`를 유지하고 production에서 제외한다. 렌더 증거를 만들지 못하면 `needs_review` + `reason_code: render_failed`로 기록하고 역시 제외한다. 비통과 팩은 내부 검토 목록에만 남긴다.

> v2까지는 "2회 미달이면 draft 배지로 발행"이었다. 이 규칙은 폐기한다 — 검증에 실패한 팩을 내보내는 것이 카탈로그 신뢰도를 갉아먹는다.

전체 종료 시 diversity-qa가 팩 간 유사도 매트릭스(`04_qa_diversity-matrix.md`)를 작성, 쌍둥이 팩은 pack-architect가 통합·재정의.

## Phase 4: 발행 (catalog-publisher)

1. 통과 팩 + `catalog.json`으로 GitHub 레포 구조화: `README.md`, `CONTRIBUTING.md`, `LICENSE`, `design-packs/`.
2. `site/`에 Next.js 15 카탈로그 웹사이트 빌드 — 갤러리·필터·prompt.md 원클릭 복사.
3. 자체 QA(빌드·카드 렌더·복사 동작·모바일) 후 Vercel preview 배포.
4. **production 배포는 사용자 명시 승인 후.** preview URL을 먼저 보고한다.

## Phase 5: 피드백 (Phase 7 진화)

발행 후 사용자에게 개선점·팀 구성 피드백 기회를 제공한다. 피드백 유형별 반영 대상은 `harness:harness` Phase 7-2 표를 따르고, 변경은 프로젝트 `CLAUDE.md` 변경 이력에 기록한다.

## 데이터 전달 프로토콜

- **태스크 기반**(`TaskCreate`) — 파이프라인 의존성·진행 추적.
- **파일 기반** — 중간 산출물은 `_workspace/{phase}_{agent}_{artifact}`, 최종 팩은 `design-packs/{slug}/`, 인덱스는 루트 `catalog.json`. `_workspace/`는 감사용으로 보존.
- **메시지 기반**(`SendMessage`) — 반려 사유·재소싱 요청 등 실시간 조율.

## 에러 핸들링

- 에이전트 실패 → 1회 재시도. 재실패 시 해당 산출물 없이 진행하고 최종 보고에 누락을 명시.
- 후보 부족 → design-scout 재소싱 1회, 그래도 부족하면 가능한 수로 진행 + 빈 축 보고.
- 팩 2회 반려 후 미달 → `reject` 유지, production 제외(파일은 삭제하지 않음).
- 라이선스 모호 → 팩을 드롭하지 말고 `license: unclear`로 표시, pack-architect가 1차 출처 확인.
- 렌더 실패 → `needs_review` + `reason_code: render_failed`. production에서 제외하고 사람 판단에 올린다.

## 테스트 시나리오

**정상 흐름:** "디자인 팩 카탈로그 만들어줘" → Phase 0(초기) → 소싱 40+α 후보 → 스키마 락 + 40팩 병렬 집필 → 렌더·검증 루프(반려분 재집필) → 레포 + 사이트 발행 → preview URL 보고 → production 승인 대기.

**후속 흐름:** "PPT 레트로 팩 5개 더 추가해줘" → Phase 0(팩 추가) → scout가 레트로 축만 소싱 → ppt-curator만 5팩 집필 → 렌더·검증 → catalog.json·사이트에 5카드 증분 반영.

**에러 흐름:** diversity-qa가 어떤 팩을 2회 반려 → `reject` 유지 → production 카탈로그에서 제외 → 최종 보고에 비통과 목록과 사유 명시.
