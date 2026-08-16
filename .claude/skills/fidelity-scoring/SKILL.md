---
name: fidelity-scoring
description: >-
  팩 렌더를 원본 레퍼런스와 페이지 단위로 대조해 '원문 충실도'를 0~4점 7축으로 채점하고 합격·반려를
  판정하는 방법론 스킬. fidelity-qa 에이전트가 사용한다. diversity-scoring(baseline 대비 차별성)과
  역할이 다르며 서로를 대체할 수 없다. 변환 계약 이행률·시그니처 재현율·환각 요소 검출·관계 문법·
  주목 위계·데이터 무결성·권리 경계 7축과 이종 모델 교차검증 절차를 규정한다.
---

# Fidelity Scoring — 원문 충실도 채점

fidelity-qa가 "이 팩이 실제로 원본을 닮았는가"를 판정하는 방법.

## diversity와 fidelity는 다른 것을 잰다

```
B = baseline (팩 없는 기본 출력)
O = 원본 레퍼런스
T = 선언된 변환 계약 (preserve/adapt/substitute/drop + page_mirror_plan)
R = 팩 렌더

diversity = distance(R, B)        ← "밋밋하지 않은가"
fidelity  = correspondence(R, T(O))  ← "원본을 닮았는가"
```

**둘은 합산하지 않는다.** 높은 diversity가 낮은 fidelity를 상쇄하면 안 된다. 발행 조건은 `diversity_pass AND fidelity_pass`다.

diversity가 fidelity를 대체할 수 없는 이유 — diversity 루브릭의 만점 정의는 "baseline과 또렷이 다름 + **표방** 스타일 일치"인데, 그 '표방'(`meta.yaml`의 family·axes)을 쓴 사람이 팩을 쓴 사람과 같다. 자기가 선언한 기준으로 자기를 채점하는 구조라 원본이 입력에 없다. 반례:

1. 원본은 보수적 네이비 문서인데 결과가 네온 포스터 → diversity 만점, fidelity 0점.
2. 원본이 baseline과 원래 비슷하면, 정확히 재현한 결과가 diversity에서 반려된다.
3. 색·타이포·레이아웃 값이 같아도 시그니처 모티프·페이지 순서·차트 의미·반복 규칙이 틀릴 수 있다.
4. pHash·색 히스토그램·엣지 밀도는 "무엇이 어디에 왜 있는가"를 판정하지 못한다.

## 적용 대상

`reference_mode`에 따라 채점 방식이 다르다.

| mode | 채점 |
|---|---|
| `exact_document` | 아래 7축 전부 |
| `official_system` | F1·F3·F4·F6·F7 (F2 시그니처 → 컴포넌트 커버리지로 대체, F5 면제) |
| `historical_canon` | F2·F3·F4·F7 (원리 인벤토리 대비) |
| `style_synthesis` | **fidelity 채점하지 않는다.** diversity + craft만 통과하면 된다 |

## 입력 (검증자 방화벽)

fidelity-qa에게 주는 것과 주지 않는 것을 엄격히 나눈다.

**준다:** 원본 페이지 렌더(`pages_src/`), 팩 렌더(`pages/`), `transform_contract`, `page_mirror_plan`, 시그니처 목록, 이 루브릭.

**주지 않는다:** 팩을 쓴 curator의 추론·자기평가·`prompt.md` 원문. 검증자가 집필자의 의도 설명을 읽으면 렌더에 없는 것을 있다고 믿는다. **보이는 것만으로 판정한다.**

## 7축 루브릭 (각 0~4점, 총 28점)

**`must_preserve: true` 항목이 계약대로 재현되지 않으면, 점수와 무관하게 `reject`다.** 가중치로 에두르지 않고 이 한 줄로 처리한다 — 3배 가중·F2 만점 강제·누락 자동반려를 겹쳐 세 번 처벌할 필요가 없다.

| 축 | 무엇을 재는가 | 0점 | 2점 | 4점 |
|---|---|---|---|---|
| **F1 계약 이행** | `transform_contract`의 preserve/adapt/substitute/drop 의무 이행률, `page_mirror_plan` 매핑 완결성 | 매핑 없음 또는 40% 미만 | 60~79% | 95%+, 모든 원본 페이지가 매핑되었거나 비선택 사유 보유 |
| **F2 시그니처 재현** | `must_preserve` 모티프 재현율 | 핵심 모티프 대부분 누락 | 일부만 재현 | 95%+, 시그니처 페이지는 전부 재현 |
| **F3 근거 정밀도** | 렌더의 주요 요소 중 원본 `observed`에 근거가 있는 비율 (= 환각 억제) | 창작 요소가 지배 | 60~79%만 근거 있음 | 95%+, 원본에 없는 새 주요 모티프 0건 |
| **F4 관계 문법** | 카드 해부구조·반복 규칙·요소 동반 관계·등장 위치 | 관계 체계가 다름 | 개별 요소는 비슷하나 규칙이 불안정 | 규칙 95%+ 일치 |
| **F5 주목 위계** | 상위 3개 focal 요소와 읽기 순서, 상대 면적·강조비 | 주 focal 부재 또는 역전 | dominant만 일치 | top-3 순서 일치, 상대 면적 ±10% |
| **F6 의미 무결성** | 페이지 역할, 차트 유형, 값·단위·순서 | 조작·창작·오역 | 큰 오류는 없으나 minor 복수 | 100% 일치 |
| **F7 권리 경계** | 상표·로고·독점 사진·아이콘·공식 문구 치환 | 원자산 직접 복제 | 브랜드 유사성 잔존, 사람 판단 필요 | 보호 자산 전부 치환, 시각 역할만 보존 |

F3은 **역방향 검사**다 — 다른 축이 "원본의 것이 렌더에 있는가"(recall)를 보는 반면, F3은 "렌더의 것이 원본에 있었는가"(precision)를 본다. 그럴듯하지만 원본에 없는 요소를 지어내는 것이 이 프로젝트의 v1 실패 모드였다.

## 합격 조건 — 모드별

모드마다 활성 축 수가 다르므로 **합격선도 다르다.** 활성 축이 4개(최대 16점)인 `historical_canon`에 23/28을 적용하면 통과가 수학적으로 불가능하다.

```
exact_document   : F1~F7 전 7축, 총점 ≥ 23 / 28
official_system  : F1·F2(컴포넌트 커버리지로 대체)·F3·F4·F6·F7 6축, 총점 ≥ 20 / 24
historical_canon : F2·F3·F4·F7 4축, 총점 ≥ 13 / 16
style_synthesis  : 채점 대상 아님 (qa.fidelity = not_applicable)

공통 조건:
  모든 활성 축 ≥ 2
  AND 활성 축 중 F1·F2·F3·F7에 해당하는 것 ≥ 3
  AND page_mirror_plan 매핑률 ≥ 80% (exact_document 전용)
```

## 자동 반려 (점수와 무관하게 즉시 reject)

- 원본 `sha256`·페이지 수·`reference_mode` 중 하나라도 누락
- **직접 보지 않은 페이지가 있는데 `pass` 판정** — 가장 흔한 부정이다
- (아래 캔버스·`spec_version`·해시 항목은 craft-qa A군이 먼저 판정한다. 여기서는 그 결과가 fail이면 채점을 시작하지 않는 **선행 조건**으로만 쓰고, 중복 채점하지 않는다.)
- 보호 자산(로고·엠블럼·독점 사진·유료 폰트) 직접 복제
- 숫자·단위·차트 방향 오류 1건 이상
- 시그니처 페이지 누락
- `prompt.md`·`tokens.json`·`meta.yaml`의 `spec_version` 불일치
- 캔버스 종횡비 선언과 실제 렌더 오차 0.5% 초과
- `style_synthesis`인데 `source_depth: full` 또는 "원문 재현" 주장

## 판정 어휘 — pass로 승격하지 않는다

> `unreviewed` · `unverifiable` · `evidence_missing`은 `pass`로 변환하지 않는다.
> 필수 페이지를 직접 보지 못했거나 검증 입력이 누락되면 `needs_review`로 두고 발행을 차단한다.

정량 지표가 정성 판정을 **보조**할 수는 있어도 **대체**할 수 없다. 이미지 열람 한도·시간 부족은 통과 사유가 아니라 `needs_review` 사유다.

## 이종 모델 교차검증

집필자(Claude)와 다른 계열의 모델을 2차 검증자로 세운다. 같은 모델이 자기 산출물을 채점하면 가짜 합의가 생긴다.

**전수가 아니라 표본이다.** 이미지 재검수는 비싸므로 아래에 해당할 때만 돌린다:
- 배치의 **첫 팩** (그 배치의 채점 기준을 교정하는 앵커)
- 1차 총점이 **합격선 경계**(exact_document 기준 22~24점)
- **F7 ≤ 2** (권리 경계 의심)
- 그 외 **20% 표본**

돌리지 않은 팩은 `cross_check: {status: not_run, reason: policy}`로 기록한다 — 돌린 척하지 않는다.

```bash
codex exec -m gpt-5.6-sol -c model_reasoning_effort=high \
  --sandbox read-only -o _workspace/{batch}/fidelity_qa/{code}_cross.md \
  -i 원본페이지.png -i 팩렌더.png \
  "두 이미지를 대조하라. 첫째는 원본, 둘째는 재현본이다. 아래 7축 루브릭으로 채점하고,
   재현본에 있으나 원본에 없는 요소(환각)를 전부 지목하라. 관대하게 채점하지 마라."
```

**두 검증자 결과의 처리:**
- 총점 차이 ≤ 3점 → 낮은 쪽 채택
- 총점 차이 ≥ 4점 → 평균 내지 말고 `needs_human`
- 총점 22~24점(합격선 경계) → `needs_human`
- F7이 어느 한쪽이라도 2점 이하 → `needs_human`

## 비용 규율

- 결정적 검사(해시 일치·종횡비·페이지 수·`spec_version`)를 **먼저 스크립트로** 돌린다. 여기서 걸리면 시각 검증에 비용을 쓰지 않는다.
- 원본 전체 파악은 저해상도 contact sheet로. **단, 팩 렌더는 전 페이지를 원해상도로 직접 본다.**
- 고해상도 정밀 검수는 시그니처 페이지와 실패 의심 영역에만.
- 원본 `sha256`가 같으면 이전 분석을 재사용. `prompt`/`tokens`가 바뀌면 렌더 이후만 무효화, 원본이 바뀌면 전부 무효화.

## 산출물

`_workspace/{batch}/fidelity_qa/{slug}.json`

```json
{ "slug": "...", "reference_mode": "exact_document",
  "source_sha256": "...", "pages_reviewed": [1,2,3,4,5,6,7,8,9,10],
  "pages_not_reviewed": [],
  "axes": { "F1": 4, "F2": 4, "F3": 3, "F4": 3, "F5": 3, "F6": 4, "F7": 4 },
  "total": 25, "verdict": "pass",
  "hallucinated_elements": [],
  "missing_signatures": [],
  "cross_check": { "verifier": "gpt-5.6-sol", "total": 24, "delta": 1 },
  "repair_requests": [] }
```

## 검증자는 팩을 수정하지 않는다

fidelity-qa는 `repair_requests`만 쓴다. 수정은 담당 curator가 하고, 수정 후에는 렌더부터 다시 돌려 새 해시로 재검증한다. 검증자가 직접 고치면 검증이 아니라 공동집필이 된다.
