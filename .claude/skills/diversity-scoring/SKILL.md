---
name: diversity-scoring
description: >-
  팩 적용 샘플을 baseline과 시각 대조해 다양성 점수를 매기고 합격/반려를 판정하는 방법론 스킬.
  diversity-qa 에이전트가 사용한다. 5축 채점 루브릭, 정량 보조 지표(perceptual hash·색 히스토그램·
  엣지 밀도), 두 종류의 실패 정의, 팩 간 유사도 매트릭스 작성법을 규정한다.
---

# Diversity Scoring — 다양성 채점 방법론

diversity-qa가 팩이 "실제로 baseline과 다른 결과를 내는가"를 판정할 때 따르는 방법.

## 이 스킬의 경계 (먼저 읽는다)

**이 스킬은 원문 충실도(fidelity)와 세련미(craft)를 판정하지 않는다.**

- 원본 레퍼런스 대비 판정 → `fidelity-scoring`
- 렌더 품질·정렬·대비·규격 → `craft-scoring`
- 이 스킬 → **baseline 대비 차별성 + 팩 간 중복**만

세 점수는 **합산하지 않는다.** 다양성이 높다고 충실도 미달을 상쇄할 수 없고, 그 반대도 아니다. 어느 게이트가 필요한지와 `status` 도출 규칙은 `design-pack-schema`의 상태식 절이 SSOT다 — 여기에 복제하지 않는다.

여기서 쓰는 5축(color/type/layout/space/shape·motion)은 `meta.yaml`이 **표방한** 스타일과의 일치를 본다. 표방을 쓴 사람이 팩을 쓴 사람과 같으므로, 이 축만으로는 "원본을 닮았는가"를 판정할 수 없다.

## 판정 어휘

> `unreviewed` · `unverifiable` · `evidence_missing`은 `pass`로 변환하지 않는다.
> 필수 이미지를 직접 보지 못했으면 `needs_review`다.

정량 지표는 정성 판정을 **보조**하지 실행되지 않은 정성 판정을 **대체**하지 않는다. 시간·이미지 열람 한도 부족은 통과 사유가 아니다. 실제로 `_workspace/13_qa_premium.json`은 이 루브릭에 없는 축(`baseline_score`·`detail_pages_score`)을 쓰고, 일부 팩을 직접 보지 못했다고 명시하면서 20팩 전원을 통과시켰다. 그것은 검증이 아니다.

## `reference_mode`에 따라 반려의 의미가 다르다

이 조항이 없어서 실제로 사고가 났다. diversity-qa가 `exact_document` 팩(HD현대)을 반려하며 **"원본에 없는 색을 본문에 넣어라"**고 지시했고, 그것은 그 덱의 `must_preserve` 시그니처(그래픽=그린 / 데이터=네이비 역할 분리)와 정면 충돌했다. curator가 거부하고 에스컬레이션한 것이 옳았다.

| mode | 낮은 diversity 점수의 의미 | 올바른 조치 |
|---|---|---|
| `style_synthesis` | 팩이 스타일을 덜 밀어붙였다 | **재집필** — 축을 더 또렷하게 |
| `exact_document` · `official_system` · `historical_canon` | **원본 자체가 baseline과 비슷하다** | **후보 교체** 또는 카탈로그 차원 판단 |

**근거 트랙 팩에 "원본에 없는 것을 더해 점수를 올려라"라고 지시하지 않는다.** 그것은 fidelity F3(근거 정밀도)에서 반려될 지시이며, 이 프로젝트가 v1~v3에서 겪은 실패("원본과 다르다")를 반대 방향으로 반복하는 것이다.

근거 트랙 팩이 이 게이트에서 미달하면 diversity-qa는 재집필을 지시하지 말고 **pack-architect에 에스컬레이션**한다. 판단은 셋 중 하나다 — (a) 후보를 교체한다, (b) 카탈로그 차원에서 다른 팩과 충분히 구별되면 통과시킨다, (c) 팩을 유지하되 카탈로그에서 그 유사성을 명시한다.

또한 근거 트랙에서는 **baseline 대비 거리보다 팩 간 거리가 더 중요하다.** 원본이 흔한 기업 IR 톤이면 baseline과 닮는 것이 정상이고, 그때 물어야 할 것은 "카탈로그 안의 다른 팩과 구별되는가"다.

## 판정 어휘 — enum

`pass` · `needs_review` · `reject` 셋만 쓴다. `fail`·`escalate`·`draft`는 쓰지 않는다.

## 핵심: 두 종류의 실패를 모두 잡는다

1. **차별성 실패** — 팩 적용본이 baseline과 너무 비슷하다. 팩이 스타일을 충분히 밀어붙이지 못함.
2. **정체성 실패** — baseline과는 다르지만, 팩이 표방한 스타일(`meta.yaml`의 `family`·`axes`)과도 다르다. 엉뚱하게 다름.

합격하려면 baseline과 충분히 다르고 **동시에** 표방 스타일과 일치해야 한다.

## 5축 채점 루브릭

baseline.png와 팩 preview.png를 **함께 읽고**, 각 축을 0~4점으로 채점한다.

| 축 | 무엇을 보는가 | 0점 | 4점 |
|---|---|---|---|
| color | 팔레트·대비·강조 운용 | baseline과 사실상 동일 | 표방 스타일대로 또렷이 다름 |
| type | 폰트 성격·위계·스케일 | 동일 | 또렷이 다름 + 표방 일치 |
| layout | 그리드·정렬·구성 | 동일 | 또렷이 다름 + 표방 일치 |
| space | 밀도·여백 리듬 | 동일 | 또렷이 다름 + 표방 일치 |
| shape/motion | 보더·모서리·그림자·질감(웹은 모션 단서) | 동일 | 또렷이 다름 + 표방 일치 |

**판정:** 총점(0~20). `pass` = 총점 13 이상 **그리고** 0점 축 없음. 그 외 `reject`. 차별성·정체성 어느 쪽이든 0점 축이 있으면 총점과 무관하게 반려.

## 정량 보조 지표

정성 판정을 보강하되 대체하지 않는다. `scripts/`에 헬퍼가 있으면 사용하고, 없으면 정성 판정만으로 진행하며 scorecard에 `quantitative: unavailable`을 표시한다.
- **perceptual hash 거리** — baseline과 너무 가까우면 차별성 의심.
- **색 히스토그램 차이** — 팔레트 분포 변화 정량화.
- **엣지/잉크 밀도** — 레이아웃 밀도 차이의 대리 지표.
극단값(거의 동일/완전 무관)일 때 정성 재검토의 플래그로만 쓴다.

## 반려는 축을 정조준한다

"별로다"가 아니라 재집필 가능한 형태로 쓴다:
> `reject` — color 3 / type 3 / **layout 0** / space 2 / shape 1. 레이아웃 축 실패: 그리드·정렬이 baseline과 동일. prompt.md의 "레이아웃" 섹션에 비대칭 그리드를 절대값으로 명시 필요. shape 축 약함: 보더·그림자 지시가 모호.

사유에는 어느 prompt.md 섹션을 어떻게 고쳐야 하는지를 담아 담당 curator가 바로 작업하게 한다.

## 점진적 검증

전체 완성 후 1회가 아니라, 각 팩(또는 5팩 배치) 렌더 직후 즉시 검증한다 — curator가 빨리 재집필하도록.

## 팩 간 유사도 매트릭스

개별 팩이 baseline과 다른 것에 더해, **채택 팩끼리도** 서로 충분히 달라야 카탈로그의 다양성이 성립한다. 전체 검증 종료 시 트랙별로 팩 간 5축 유사도 매트릭스를 작성해 `_workspace/04_qa_diversity-matrix.md`에 저장한다. 두 팩이 5축 중 4축 이상 같으면 쌍둥이로 표시하고 pack-architect에 통합·재정의를 권고한다.

## 산출물

- `_workspace/04_qa_scorecard.json` — 슬러그별 `{axis_scores, total, verdict, reasons[]}`.
- `_workspace/04_qa_diversity-matrix.md` — 팩 간 유사도 매트릭스 + 쌍둥이 권고.

## 에스컬레이션

같은 팩이 2회 반려 후에도 미달이면 `pass`로 강제하지 않는다. 2회 후에도 게이트 미달이면 `reject`를 유지하고 production에서 제외한다. 렌더 증거를 만들지 못하면 `needs_review` + `reason_code: render_failed`로 기록하고 역시 제외한다. 비통과 팩은 내부 검토 목록에만 남긴다. 상태 enum은 `pass` · `needs_review` · `reject` 셋뿐이다 — v2의 `escalate`·`draft`는 폐기됐다.
