---
name: design-pack-schema
description: >-
  디자인 팩의 산출 형식(prompt.md + tokens.json + preview.png + meta.yaml)과 카탈로그 인덱스(catalog.json)를
  정의하는 단일 진실 원천(SSOT) 스킬. 팩을 집필·검수·발행하는 모든 에이전트(pack-architect, ppt/web curator,
  catalog-publisher)가 따른다. 팩 파일 구조·필드·토큰 키·슬러그 규칙·스키마 변경 절차를 규정한다.
---

# Design Pack Schema — 산출 형식 SSOT

디자인 팩의 파일 구조와 필드를 정의한다. 이 스킬이 규격의 SSOT다 — 규격을 바꾸려면 이 파일을 먼저 갱신하고 모든 curator에 통지한다.

## 폴더 구조

```
design-packs/{slug}/
  prompt.md      ← Claude Code 복붙용 디자인 지시문
  tokens.json    ← 머신리더블 디자인 토큰
  preview.png    ← 샘플 렌더 (sample-renderer가 생성)
  meta.yaml      ← 메타데이터·출처·라이선스
```

## 슬러그 규칙

`{track}-{family}` 형태의 kebab-case. 예: `ppt-swiss-editorial`, `web-neo-brutalism`. 트랙 prefix(`ppt-`/`web-`)는 필수. 전 카탈로그에서 유일해야 한다.

## prompt.md — 가장 중요한 산출물

Claude Code에 **한 블록으로 복붙**해 그 스타일을 재현하는 자기완결 지시문. 모호어("모던하게", "깔끔하게") 금지 — 검증 가능한 구체 지시만. 필수 섹션:

```markdown
# {Display Name} — {track} 디자인 팩

## 이 스타일의 정체성
(2~3문장. 무엇을 보고 이 스타일임을 알 수 있는가)

## 색
(구체적 hex 값과 역할: 배경/표면/텍스트/강조. 강조색 개수 제한 명시)

## 타이포그래피
(폰트 패밀리·대체 폰트, 위계별 크기·굵기·자간·행간)

## 레이아웃 / 그리드
(PPT: 슬라이드 그리드·여백·헤더 / 웹: 콘텐츠 폭·브레이크포인트·섹션 리듬)

## 형태 / 질감
(보더·모서리·그림자·아이콘·이미지 처리 방식)

## 모션 (웹) / 전환 (PPT)
(있다면 구체적 duration·easing·트리거)

## 하지 말 것
(이 스타일에서 금지: Claude 기본 미감으로 회귀하는 것을 차단하는 핵심 섹션)

## 적용 예
(PPT: 표지·본문·차트 슬라이드 / 웹: 히어로·카드·푸터 — 각 1~2문장 지시)
```

"하지 말 것" 섹션은 필수다. 다양성의 적은 Claude가 기본값(보라 그라디언트, 둥근 카드, 이모지, 균일한 그림자)으로 회귀하는 것이다.

## tokens.json

```json
{
  "slug": "web-neo-brutalism",
  "track": "web",
  "family": "neo-brutalism",
  "color": { "bg": "#ffffff", "surface": "#ffe14d", "text": "#0a0a0a",
             "accent": ["#ff5a36"], "border": "#0a0a0a" },
  "type": { "display": { "family": "Archivo Black", "fallback": "sans-serif",
                          "size": "clamp(2.5rem,6vw,5rem)", "weight": 900, "tracking": "-0.02em" },
            "body": { "family": "Inter", "size": "1.0625rem", "weight": 400, "leading": 1.6 } },
  "spacing": { "unit": 8, "section": 96, "content_max": "1100px" },
  "shape": { "radius": "0px", "border": "3px solid", "shadow": "6px 6px 0 #0a0a0a" },
  "motion": { "duration": "120ms", "easing": "steps(1)", "hover": "translate(-2px,-2px)" }
}
```

키는 트랙 공통(`color`·`type`·`spacing`·`shape`)이고, `motion`(웹)·`slide`(PPT 슬라이드 메타)는 트랙별. 두 curator는 공통 키 이름을 동일하게 쓴다 — 사이트가 일관 소비해야 하므로.

## meta.yaml

```yaml
slug: web-neo-brutalism
display_name: Neo-Brutalism
track: web            # ppt | web
family: neo-brutalism
summary: 거친 보더·하드 섀도·원색 블록의 반(反)미니멀 웹 스타일.
axes: { color: vivid-primary, type: heavy-display, layout: block-grid, space: dense, motion: snappy }
sources:
  - { title: "...", url: "https://...", type: official|article }
license: "원자산은 각 출처 라이선스를 따름. 본 팩이 배포하는 것은 디자인 명세·토큰이며 원자산 사본이 아님."
source_depth: full     # full | partial
status: pass           # pass | needs_review | reject  (게이트에서 생성 — 사람이 쓰지 않는다)
```

## catalog.json — 카탈로그 인덱스

루트의 머신리더블 인덱스. 사이트·도구가 소비한다.

```json
{ "version": 1, "updated": "2026-05-20",
  "packs": [
    { "slug": "web-neo-brutalism", "track": "web", "family": "neo-brutalism",
      "display_name": "Neo-Brutalism", "summary": "...", "axes": {...},
      "preview": "design-packs/web-neo-brutalism/preview.png", "status": "pass" }
  ] }
```

## 스타일 축 (다양성의 측정 단위)

모든 팩은 5축으로 분류한다 — pack-architect가 이 매트릭스로 후보를 솎고 중복을 막는다.

| 축 | 예시 값 |
|---|---|
| color | mono / vivid-primary / pastel / dark / gradient / earth |
| type | minimal-sans / heavy-display / serif-editorial / mono / mixed |
| layout | strict-grid / block-grid / asymmetric / centered / full-bleed |
| space | dense / balanced / airy |
| motion | none / subtle / snappy / playful |

두 팩이 5축 중 4축 이상 같으면 사실상 쌍둥이 — 합치거나 한쪽을 다른 축으로 재정의한다.

## 스키마 v2 — 카테고리 + 상세 페이지 (2026-05-21)

팩에 두 개념을 추가한다. 기존 v1 팩은 모두 `category: standard`로 자동 분류되며 마이그레이션 불필요(필드 부재 = standard, pages 부재 = 단일 preview).

### category — 팩 등급

- `standard` — 단일 preview.png를 가진 일반 팩. 기존 80팩 전부.
- `premium` — 한 팩이 **5~7개의 상세 페이지(detail page)**를 갖춰, 표지/본문/차트/다이어그램/비교 등 다양한 활용 장면을 모두 명세·렌더한 심화 팩.

`category`는 `meta.yaml`·`catalog.json` 양쪽에 기재한다.

### 상세 페이지 (premium 전용)

premium 팩은 `design-packs/{slug}/pages/` 폴더에 5~7개의 페이지 렌더를 둔다:

```
design-packs/{slug}/
  prompt.md
  tokens.json
  preview.png          ← 카드 썸네일용 대표 1컷 (보통 pages/01과 동일하거나 표지)
  meta.yaml
  pages/
    01-cover.png   02-agenda.png   03-body.png   04-chart.png
    05-diagram.png 06-comparison.png 07-closing.png
```

파일명은 `NN-{page-id}.png` (2자리 순번 + page-id). 5~7장 권장, 최소 5장.

**페이지 ID 택소노미** — 트랙별 표준 ID에서 5~7개를 고른다(팩 성격에 맞게 취사선택, 신규 ID 추가 가능):

- **PPT:** `cover`(표지) · `agenda`(목차) · `section-divider`(섹션 간지) · `body`(핵심 본문) · `chart`(데이터 차트) · `diagram`(프로세스/관계 다이어그램) · `comparison`(비교·매트릭스) · `timeline`(타임라인) · `kpi`(KPI 대시보드) · `closing`(클로징/Q&A)
- **웹:** `hero`(히어로) · `nav`(헤더·내비게이션) · `features`(기능 그리드·카드) · `pricing`(가격표) · `content`(콘텐츠 상세·아티클) · `gallery`(쇼케이스·갤러리) · `dashboard`(앱·대시보드 화면) · `testimonial`(후기·로고월) · `cta-footer`(CTA·푸터)

### prompt.md — premium 팩의 추가 섹션

premium 팩의 prompt.md는 기존 "적용 예" 섹션을 **"## 상세 페이지 (5~7종)"**로 확장한다. 각 페이지마다 소제목 + 검증 가능한 구체 레이아웃 지시(그리드 좌표·요소 배치·치수). "다양한 방법으로 활용"이 실제 지시로 존재해야 한다 — 한 줄 요약 금지.

### tokens.json — premium 팩의 pages 키

```json
{ "...": "...",
  "category": "premium",
  "pages": [
    { "id": "cover", "label": "표지" },
    { "id": "chart", "label": "데이터 차트" }
  ] }
```

### meta.yaml — v2 필드

```yaml
category: premium        # premium | standard (부재 시 standard)
pages:                   # premium 전용
  - { id: cover, label: 표지, kind: cover }
  - { id: chart, label: 데이터 차트, kind: chart }
```

### catalog.json — v2 pack 엔트리

```json
{ "slug": "...", "track": "ppt", "category": "premium",
  "display_name": "...", "summary": "...", "axes": {...},
  "preview": "design-packs/{slug}/preview.png",
  "pages": [
    { "id": "cover", "label": "표지", "img": "design-packs/{slug}/pages/01-cover.png" }
  ],
  "status": "pass" }
```

`category`는 전 팩 필수(기존 80팩도 일괄 `standard` 백필). `pages`는 premium 팩만.

### 렌더 규약 (sample-renderer)

premium 팩은 1개 HTML에 5~7개 패널을 세로로 쌓아 작성하되, **각 패널을 개별 스크린샷**해 `pages/NN-id.png`로 저장하고, 대표 1컷을 `preview.png`로 복사한다. baseline 대조는 기존과 동일(트랙 baseline 1컷 재사용).

## 스키마 v3 — 레퍼런스 계약 · 필드 정본화 · 밀도 기준 (2026-08-16)

v2까지의 팩은 "무슨 스타일인가"만 선언했다. v3는 **"무엇을 근거로 그렇게 주장하는가"**를 함께 요구한다.

### 왜 v3가 필요했나 (실측 진단)

프리미엄 10팩의 `meta.yaml`을 전수 조사한 결과, **키 40종 중 28종이 1~2개 팩에만 존재**했다. 같은 개념을 팩마다 다른 이름으로 발명한 결과다.

| 개념 | 실제로 쓰인 이름들 | v3 정본 |
|---|---|---|
| 원본→팩 페이지 매핑 | `page_mirror_plan` · `mirror_plan` · `v3_mirror_plan` · `v3_page_mirror_plan` · `page_mirror_plan_summary` · `v3_compression_plan` | **`page_mirror_plan`** |
| 시그니처 모티프 | `signature_motifs` · `signature_visual_motifs` · `signature_top5` · `signature_locks_v2_carried` · `visual_vocabulary_anchors` · `visual_lexicon_11` | **`signature_motifs`** |
| 버전 | `version` · `spec_version` · `pack_id` · `based_on` · `changelog` · `v1_to_v2_diff` · `v2_to_v3_diff` · `v3_additions` | **`spec_version`** + `changelog` |
| 차별성 서술 | `differentiation` · `v3_focus` · `chart_inventory` | **`differentiation`** |

원인은 이 파일(SSOT)이 mirror 관련 필드를 **한 번도 정의한 적이 없다는 것**이다. v3에서 필드가 필요해지자 각 팩이 즉석에서 만들어 썼다. 위 표에 없는 이름은 전부 폐기하며, 새 필드가 필요하면 **이 파일을 먼저 고친다.**

### `reference_mode` — 전 팩 필수

팩이 무엇을 근거로 삼는지 선언한다. 상세 정의는 `reference-analysis` 스킬이 SSOT다.

| 값 | 근거 | fidelity 채점 | `source_depth: full` 허용 |
|---|---|---|---|
| `exact_document` | 특정 공개 덱 원본 파일 | 7축 전부 | 원본 sha256 있을 때만 |
| `official_system` | 공식 디자인 시스템 문서 | F1·F3·F4·F6·F7 | 공식 문서 직접 인용 시 |
| `historical_canon` | 학술·박물관 1차 자료 | F2·F3·F4·F7 | 1차 자료 확보 시 |
| `style_synthesis` | 복수 2차 자료 합성 | **채점 안 함** | **불가 — 항상 `partial`** |

**엄수:** 2차 자료(슬라이드 판매 사이트·해설 영상·블로그)만 있는 팩은 `style_synthesis`이며, `source_depth: full`을 쓸 수 없고 "원본을 재현했다"고 표기할 수 없다.

### v3 필수 필드 (`meta.yaml`)

```yaml
spec_version: v3-2026-08-16          # prompt.md·tokens.json과 3자 일치 필수
reference_mode: exact_document
reference:                            # exact_document 필수
  canonical_url: "https://..."
  retrieved_at: "2026-08-16T09:00:00+09:00"
  sha256: "..."
  media_type: application/pdf
  page_count: 24
  aspect_ratio: 1.778
page_mirror_plan:                     # exact_document 필수
  original_pages: 24
  pack_pages: 10
  compression: merged                 # identity | selected | merged
  map:
    - { pack_page: 5, source_pages: [9, 10, 11], kind: chart, rationale: "..." }
signature_motifs:                     # 3~7개
  - { rank: 1, name: "...", evidence_pages: [1, 5, 12], where: "...",
      uniqueness: "...", must_preserve: true }
transform_contract: _workspace/{batch}/transform_contract/{code}.json
qa:                                   # 게이트 결과. 사람이 손으로 pass를 쓰지 않는다
  fidelity: { verdict: pass, total: 25, scored_at: "..." }
  craft:    { verdict: pass, total_B: 21 }
  diversity:{ verdict: pass, total: 17 }
status: pass                          # 아래 규칙으로 생성
```

`evidence_pages`가 빈 시그니처는 관찰이 아니라 창작이므로 삭제한다.

### `status` — 사람이 쓰지 않고 생성한다 (이 절이 상태식의 SSOT)

필요한 게이트가 **모드마다 다르다.** `style_synthesis`는 원본이 없으므로 fidelity 대상이 아니다 — 이 팩에 fidelity 통과를 요구하면 영원히 발행되지 않는다.

```
fidelity_required = reference_mode in [exact_document, official_system, historical_canon]
required_gates    = [craft, diversity] + ([fidelity] if fidelity_required else [])

status = reject       ⟸ 필요한 게이트 중 하나라도 verdict == reject
       = needs_review ⟸ 필요한 게이트가 없거나 verdict != pass
                        (unreviewed / unverifiable / evidence_missing 포함)
       = pass         ⟸ 필요한 게이트 전부 pass
                        AND spec_version 3자 일치
                        AND render-manifest 해시가 현재 파일과 일치
```

`style_synthesis` 팩의 `qa.fidelity`는 `pass`가 아니라 **`not_applicable`**로 기록한다. 통과시킨 것이 아니라 대상이 아님을 남긴다.

**다른 파일은 이 식을 복사하지 않는다.** 오케스트레이터·발행 스킬·에이전트는 "모드별 상태식은 `design-pack-schema`가 SSOT"라고만 쓴다. 식을 여러 곳에 복제하면 한쪽만 고쳐져 갈라진다 — 이 프로젝트가 이미 겪은 실패다.

### `status` enum

`pass` · `needs_review` · `reject` **셋만** 쓴다. v2의 `escalate` · `draft` · `render_failed`는 폐기했다. 렌더 증거를 만들지 못한 경우는 `needs_review` + `reason_code: render_failed`로 기록하고 production에서 제외한다.

`needs_review`를 `pass`로 승격하지 않는다. 이미지를 다 보지 못했거나 검증 입력이 없으면 그것이 `needs_review`의 정의다. 시간·한도 부족은 통과 사유가 아니다.

### 상세 페이지 수 — 모드별 (v2의 "5~7장" 고정 규칙을 대체)

v2는 premium을 5~7장으로 고정했으나 실제 한국 레퍼런스 팩은 10장이다. 규칙이 현실과 달랐다.

```
style_synthesis / historical_canon : 5~7종
official_system                    : 6~9종
exact_document                     : 8~12종 (must_preserve 시그니처를 전부 담는 최소 슬롯 수)
```

### prompt.md 필수 섹션 (v3)

```
## 이 스타일의 정체성
## 레퍼런스 범위와 모드          ← v3 신설. 원본·모드·비선택 페이지 명시
## 변환 계약                     ← v3 신설. preserve / adapt / substitute / drop
## 색
## 타이포그래피
## 레이아웃 / 그리드
## 형태 / 질감
## 차트·데이터 시각화            (PPT)
## 다이어그램·컴포넌트           (PPT)
## 컴포넌트·반응형·접근성        (웹)
## 모션 / 전환
## 하지 말 것
## 상세 페이지
## 렌더 합격 기준                ← v3 신설. 이 팩이 통과해야 할 구체 수치
## 출처·권리 경계
```

### 지시 밀도 — 줄 수로 재지 않는다

실측 결과 프리미엄 10팩의 줄 수는 145~523줄(3.6배)이었으나 문자 수는 14.9K~30.7K(2.1배)였다. **줄 수는 품질 지표가 아니다** — 긴 단일 행으로 쓰면 줄 수만 작아진다.

밀도는 **constraint atom** = `(대상, 속성, 검증 가능한 값 또는 token 참조)` 3요소를 갖춘 지시의 개수로 잰다.

```
일반 페이지          : atom ≥ 14
chart/diagram 페이지 : atom ≥ 18
페이지 고유 atom     : ≥ 8   (전역 규칙 상속분 제외)
수치·token으로 검증 가능한 atom 비율 : ≥ 60%
동일 규칙 자연어 중복률              : ≤ 15%
같은 대상·같은 속성의 상충 값        : 0건        ← hard fail
```

**상충 0건이 v3에서 가장 중요한 규칙이다.** 실제 위반 사례:
- `ppt-motie` — 표지 슬로건 크기를 `76~86pt`·`60~80pt`·`60~72pt`로 세 번 다르게 선언
- `ppt-motie` — 캔버스를 `16:9`와 `1285×910`(실제 1.412)로 동시 선언
- `ppt-mcst` — 카드 본문을 `14pt`로 지정하고 "하지 말 것"에 `24pt 이하 금지`를 동시 기재

전역 규칙을 페이지에서 다시 쓰지 말고 참조한다 — `inherits: [grid.body, type.body, card.base]`. 자연어를 복제하면 위와 같은 충돌이 생긴다.

### 3자 동기화

`prompt.md`·`tokens.json`·`meta.yaml`의 `spec_version`, 페이지 ID·순서·kind가 다르면 **자동 반려**한다. `ppt-motie`는 prompt v4 / meta v4 / tokens **v3**로 어긋난 채 발행됐다.

### v1·v2 팩의 처리

기존 110팩은 이 회차에서 자동 마이그레이션하지 않는다. 다만 다음을 기록한다:
- `reference_mode` 미기재 팩은 **미분류**이며, 그 팩의 `source_depth: full`은 검증된 값이 아니다.
- 기존 `status: pass`는 v3 게이트를 통과한 값이 아니다. v3 이전 팩과 이후 팩을 같은 근거로 취급하지 않는다.
- 마이그레이션은 별도 회차로 계획한다.

## 스키마 변경 절차

1. 이 파일을 갱신한다. 2. `spec_version`을 올리고 변경점을 기록한다. 3. 영향받는 기존 팩의 마이그레이션 필요 여부를 pack-architect가 보고한다. 4. 모든 curator에 통지한다.

**새 필드가 필요하면 팩에서 즉석으로 만들지 말고 이 파일을 먼저 고친다.** v3 진단의 28종 고아 필드가 그 규율을 어긴 결과다.
