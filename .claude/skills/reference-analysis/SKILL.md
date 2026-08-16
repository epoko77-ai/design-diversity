---
name: reference-analysis
description: >-
  원본 레퍼런스(공개 PDF 덱·공식 디자인 시스템·역사 양식)를 확보·적격 판정·전수 정독하여, 팩 집필이
  근거로 삼을 visual spec과 변환 계약(transform contract)을 만드는 방법론 스킬. reference-analyst
  에이전트가 사용한다. 레퍼런스 모드 4종 분류, 원본 적격 게이트, 페이지 전수 인벤토리, 시그니처 모티프
  추출, 상표·독점자산 치환 계약을 규정한다. 이 스킬의 산출물 없이는 premium 레퍼런스 팩을 집필할 수 없다.
---

# Reference Analysis — 원본 정독 · 변환 계약

reference-analyst가 "원문과 닮은" 팩의 근거를 만드는 방법. **관찰한 것만 기록하고, 추론한 것은 추론이라고 표시한다.**

## 왜 이 스킬이 존재하는가

이 프로젝트는 프리미엄 한국 레퍼런스 10팩을 v1→v2→v3로 세 번 갈아엎었다. 사유는 매번 같았다 — *원본과 다르다.* v3에서 실제로 통했던 절차(원본 확보 → 페이지 전수 정독 → mirror plan → 재집필 → 대조 검증)가 어느 스킬에도 문서화되지 않아, 매 회차 처음부터 다시 발명됐다. 이 스킬이 그 절차의 SSOT다.

## 레퍼런스 모드 (가장 먼저 확정한다)

팩마다 `reference_mode`를 하나 고른다. **모드가 판정 기준을 결정하므로 이것을 틀리면 뒤의 모든 검증이 무의미하다.**

| `reference_mode` | 대상 | 근거 요구 수준 | 판정 기준 |
|---|---|---|---|
| `exact_document` | 특정 공개 덱 1건 (예: 부처 업무보고 PPT, 기업 IR 덱) | 원본 파일 확보 필수 | 페이지·변환 계약 대비 **fidelity** |
| `official_system` | 공식 디자인 시스템 (Material·HIG·Carbon 등) | 공식 문서 + 컴포넌트 캡처 | 컴포넌트·토큰 **conformance** |
| `historical_canon` | 역사 양식 (바우하우스·데스틸·스위스 타이포 등) | 학술·박물관 1차 자료 | 원리·모티프 인벤토리 **conformance** |
| `style_synthesis` | 복수 2차 자료의 합성 (예: "컨설팅 덱 미감") | 2차 자료 허용 | `style_conformance`만. **원문 충실도를 주장하지 않는다** |

**엄수:** `style_synthesis` 팩은 `source_depth: full`을 쓸 수 없고, meta·사이트 어디에서도 "원본을 재현했다"고 말하지 않는다. 2차 자료(슬라이드 판매 사이트·유튜브 해설·블로그)만 있는데 `full`로 표기하는 것은 출처 위조다.

## 원본 적격 게이트 (`exact_document` 전용)

후보를 정독하기 **전에** 기계적으로 판정한다. 여기서 거른 것이 가장 싸다.

| 게이트 | 기준 | 판정 방법 |
|---|---|---|
| G-A 확보 | 원본 파일을 실제로 내려받았다 | `curl -sL -o` 후 파일 유효성 확인. 링크 존재만으로는 불가 |
| G-B 매체 형태 | **PPT 트랙은 종횡비 ≥ 1.6** (16:9 = 1.778) | 1페이지 mediabox 실측 |
| G-C 분량 | 페이지 ≥ 8 | 페이지 수 |
| G-D 디자인 밀도 | 앞 5장을 렌더해 **직접 보고** 시각 언어가 있는지 판정 | 사람/에이전트 육안 |
| G-E 권리 | 공개 배포물이며 출처가 1차 | 게시 주체·URL |

**G-B가 이 프로젝트에서 가장 많이 실패한 게이트다.** A4 세로 한글 문서(종횡비 ≈0.71)를 덱으로 착각해 국토부·고용부 2팩을 폐기했고, 농식품부·행정안전부·식약처·기후에너지부·한국은행 후보 6건을 다운로드 후에야 탈락시켰다. **비율을 먼저 재라.**

게이트 결과는 후보별로 남긴다 — 탈락 사유는 다음 회차의 자산이다.

```json
{ "code": "mois", "gate_16x9": "fail", "aspect_ratio": 0.707,
  "drop_reason": "A4 세로 한글 문서. 디자인 덱 아님." }
```

## 원본 확보 기록 (source manifest)

통과한 원본은 재현 가능하게 고정한다. 원본은 저장소에 커밋하지 않되, **식별자는 커밋한다.**

```yaml
reference:
  mode: exact_document
  canonical_url: "https://..."        # 실제 다운로드에 성공한 URL 원문
  retrieved_at: "2026-08-15T14:20:00+09:00"
  sha256: "..."                        # 원본 파일 해시
  media_type: application/pdf
  page_count: 22
  page_box: { width: 960, height: 540, unit: pt }
  aspect_ratio: 1.778
  local_path: "_workspace/{batch}/pdf/{code}.pdf"   # 로컬 전용
```

`sha256`가 같으면 이전 분석을 재사용한다 — 같은 원본을 두 번 정독하지 않는다.

## 페이지 전수 인벤토리

**원본 전 페이지를 렌더해 전부 본다.** 표본만 보고 쓰는 것이 v1 실패의 직접 원인이었다.

```bash
pdftoppm -png -r 110 원본.pdf _workspace/{batch}/pages_src/{code}/p
```

페이지마다 관찰 기록을 남긴다. **형용사가 아니라 관찰값으로.**

```json
{ "page": 13, "role": "policy-diagram",
  "observed": {
    "bg": "#001838→#0848A0 세로 그라데이션 풀스크린",
    "structure": "중앙 반원 호 + 3노드, 호 상단에 시안 글로우",
    "type": "캘리그래피 28pt 흰색 2행 + 노드 라벨 16pt",
    "chart": null,
    "notes": "이 덱에서 유일한 다크 배경 다이어그램 — 시그니처 후보" },
  "inferred": ["글로우는 외곽 blur 24px로 추정 (원본 벡터 확인 불가)"] }
```

`observed`와 `inferred`를 반드시 분리한다. 뒤의 fidelity 검증자는 `observed`만 근거로 인정한다.

## 시그니처 모티프 추출

"이 덱임을 알아보게 하는 것"을 순위와 함께 3~7개 뽑는다. 각 항목은 네 필드를 갖춘다.

```yaml
signature_motifs:
  - rank: 1
    name: 캘리그래피 손글씨 슬로건 풀스크린
    evidence_pages: [1, 5, 12, 20, 21]     # 실제 관찰된 페이지. 필수
    where: 표지·섹션 인트로·종결. 본문 페이지에는 없음
    uniqueness: 다른 부처 덱은 고딕 제목만 씀 — 손글씨가 이 덱의 유일 식별자
    must_preserve: true
```

`evidence_pages`가 비어 있으면 그 모티프는 **관찰이 아니라 창작**이므로 삭제한다. `must_preserve: true`인 모티프가 하나라도 재현되지 않으면 fidelity에서 점수와 무관하게 반려다 — 그러니 이 플래그는 정말 그 덱을 그 덱이게 하는 것에만 붙인다.

## 변환 계약 (transform contract)

원본을 그대로 베끼는 것은 목적이 아니다. 우리가 배포하는 것은 **시각 원리의 명세**다. 원본의 각 요소를 네 가지 중 하나로 처분하고, 그 결정을 기록한다.

| action | 의미 | 예 |
|---|---|---|
| `preserve` | 그대로 재현 | 그리드 비율, 색 관계, 타이포 위계, 다이어그램 문법 |
| `adapt` | 역할은 유지하되 값을 조정 | 유료 폰트 → metric 호환 공개 폰트 |
| `substitute` | 보호 자산을 역할만 남기고 치환 | 부처 엠블럼 → 같은 위치·크기의 중립 워드마크 자리 |
| `drop` | 재현하지 않음 | 특정 인물 사진, 원본 고유 일러스트 |

```json
{ "source_page": 1, "element_id": "ministry-emblem", "class": "trademark",
  "action": "substitute",
  "preserve": ["우하단 배치", "슬라이드 폭 대비 5%", "다크 위 흰색 대비"],
  "prohibit": ["기관명 문자열", "엠블럼 기하", "전용 서체"] }
```

**보호 자산 분류(`class`)** — `trademark`(로고·엠블럼·워드마크) · `proprietary_image`(원본 사진·일러스트) · `licensed_font`(유료 폰트) · `slogan`(정부·기업 공식 문구). 이 넷은 `preserve`가 불가능하다. `substitute` 또는 `drop`만 허용한다.

## 페이지 매핑과 정직한 명명

원본 N장을 팩 M장으로 옮길 때, 반드시 어느 원본에서 왔는지 적는다.

```yaml
page_mirror_plan:                  # ← 정본 필드명. 다른 이름을 쓰지 않는다
  original_pages: 22
  pack_pages: 10
  compression: merged              # identity | selected | merged
  map:
    - pack_page: 5
      source_pages: [9, 10, 11]
      kind: chart
      rationale: 3장이 같은 정책의 연속 화면 — 하나로 합쳐도 문법 손실 없음
```

**명명 규율.** `compression: merged`인데 "1:1 mirror"라고 부르지 않는다. 22장을 10장으로 합쳤으면 그것은 `transformed-principle fidelity`이지 픽셀 미러가 아니다. 과대 표기는 뒤의 검증자가 무엇을 기대해야 할지 혼란시킨다.

- `identity` — 원본 1장 = 팩 1장, 전 페이지 커버
- `selected` — 원본 일부만 선택 (선택 사유 + 비선택 페이지 목록 필수)
- `merged` — 복수 원본 → 팩 1장 (병합 사유 필수)

## 산출물

```
_workspace/{batch}/
  01_scout_candidates.json          # 게이트 판정 포함 (탈락분도 보존)
  pdf/{code}.pdf                    # 원본 (로컬 전용, 커밋 안 함)
  pages_src/{code}/p-NN.png         # 원본 전 페이지 렌더
  visual_spec/{code}.json           # 페이지 전수 인벤토리 + 시그니처 + reference manifest
  transform_contract/{code}.json    # 요소별 처분 계약
```

### 정본 키 (필수 — 이름을 바꾸지 않는다)

**이 절이 없어서 첫 배치 5팩의 산출물이 즉시 갈라졌다.** 인벤토리에 `inventory`/`page_inventory` 2종, 비선택 페이지에 `not_selected`/`unselected`/`unmapped_source_pages` 3종, 변환 계약 루트에 5종이 생겼다. 팩 `meta.yaml`에서 벌어졌던 고아 필드 28종 사태와 같은 병이다. 아래 이름만 쓴다.

`visual_spec/{code}.json` 최상위 키:

| 정본 | 필수 | 폐기된 별칭 |
|---|---|---|
| `schema_version` | ✓ | — |
| `code` | ✓ | — |
| `reference` | ✓ | `manifest` |
| `pages_unreadable` | ✓ (없으면 `[]`) | — |
| `page_inventory` | ✓ | `inventory` · `pages` |
| `signature_motifs` | ✓ | `signature_visual_motifs` · `signature_top5` |
| `page_mirror_plan` | ✓ | `mirror_plan` · `compression_plan` |
| `palette_measured` | 권장 | `palette` |
| `contrast_measured` | 권장 | `contrast` |

`page_mirror_plan` 하위: `original_pages` · `pack_pages` · `compression` · `map` · **`not_selected`**(← `unselected`·`unmapped_source_pages`·`excluded` 폐기).

`transform_contract/{code}.json` 최상위 키: `schema_version` · `code` · `reference_sha256` · **`elements`**(요소 배열. `protected_assets`·`preserved_principles`로 쪼개지 말고 각 원소의 `class`·`action`으로 구분한다).

`page_inventory` 각 원소: `page`(정수) · `role` · `observed`(객체) · `inferred`(배열).
페이지 번호는 **항상 정수 배열**로 쓴다 — `"1,2,13-16 등 전 페이지"` 같은 문자열 금지. 뒤의 검증자가 기계로 대조할 수 없다.

새 키가 필요하면 산출물에서 즉석으로 만들지 말고 **이 표를 먼저 고친다.**

## 하지 말 것

- 표본 몇 장만 보고 전체를 단정하는 것. 전 페이지를 봐라.
- `observed`에 추론을 섞는 것. 확인 못 한 것은 `inferred`에 두거나 비워라.
- 원본을 못 구했는데 `exact_document`로 선언하는 것. 그건 `style_synthesis`다.
- 일반 디자인 상식으로 관찰의 빈칸을 메우는 것 — 원본이 규칙을 어기고 있으면 **원본이 옳다**. 그 이탈이 곧 그 덱의 정체성이다.
- 보호 자산을 `preserve`로 처분하는 것.
