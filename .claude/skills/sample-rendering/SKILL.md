---
name: sample-rendering
description: >-
  디자인 팩의 prompt.md로 실제 PPT 슬라이드/웹 페이지 샘플을 생성하고, 동일 콘텐츠의 baseline 출력도
  함께 만들어 preview.png를 렌더하는 방법론 스킬. sample-renderer 에이전트가 사용한다. 공정 대조용
  더미 콘텐츠(fixture), 트랙별 렌더 경로, 폰트 폴백 처리를 규정한다.
---

# Sample Rendering — 샘플 렌더링 방법론

sample-renderer가 팩 적용 샘플과 baseline을 공정하게 렌더할 때 따르는 방법.

## 블라인드 재생 원칙 (가장 중요)

렌더는 **팩이 실제로 작동하는지에 대한 실험**이다. 실험자가 정답을 보고 있으면 실험이 아니다.

sample-renderer가 **받는 것:** `prompt.md` · `tokens.json` · fixture.

sample-renderer가 **보지 않는 것:**
- 원본 레퍼런스 이미지 (`pages_src/`)
- `visual_spec` · `transform_contract`
- 집필자가 만든 HTML·목업
- 이전 회차의 렌더 결과

이유는 단순하다. 원본을 보면서 렌더하면 `prompt.md`에 없는 것을 원본에서 보충해 그리게 되고, 그러면 **결함 있는 팩이 통과한다.** 실제 사용자는 `prompt.md`만 복붙한다 — 그 조건을 그대로 재현해야 한다. prompt.md만으로 스타일이 안 나오면 그것이 팩의 결함이며, 검증자가 잡을 일이다.

## 렌더 매니페스트 (필수)

렌더할 때마다 무엇으로부터 만들어졌는지 기록한다. 이것이 없으면 **명세가 갱신됐는데 옛 렌더가 남아 있는 상태**를 아무도 못 잡는다.

```json
{ "slug": "ppt-...", "rendered_at": "2026-08-16T...",
  "source_hash": { "prompt.md": "sha256:...", "tokens.json": "sha256:..." },
  "spec_version": "v3-2026-08-16",
  "canvas": { "declared": "16:9", "actual_px": [2560, 1440], "ratio": 1.778 },
  "pages": [ { "id": "cover", "file": "pages/01-cover.png", "px": [2560,1440] } ],
  "font_fallbacks": [] }
```

발행 전 `source_hash`가 현재 파일 해시와 다르면 **stale render**이며 자동 반려한다.

실제 사고: `ppt-motie`는 `prompt.md`가 v4로 갱신된 뒤에도 v3 시절 PNG가 남아, `06-diagram.png`가 명세(딥네이비 반원 호 다이어그램)와 전혀 다른 슬라이드(한국지도 6핀)인 채 발행됐다. 같은 팩의 10장 중 5장만 2560×1440이고 나머지는 2752×1616·2752×1640·2736×1616으로 크기도 제각각이었다.

## 캔버스 규격

한 팩의 **전 페이지가 동일 픽셀 크기**여야 한다. 페이지별 padding이 캔버스 바깥에 더해지지 않게 `box-sizing`을 고정하고, 렌더 후 크기를 실측해 매니페스트에 적는다. 선언 종횡비와 실제 오차 0.5% 초과는 hard fail이다.

## 공정 대조 원칙

다양성을 측정하려면 **콘텐츠는 같고 디자인만 달라야** 한다. 팩 적용본과 baseline은 동일한 더미 콘텐츠(fixture)를 쓴다.

## 더미 콘텐츠 (fixture)

트랙별로 고정된 가짜 콘텐츠를 쓴다. 매 팩·baseline에 동일 적용.

**PPT fixture** — 가상 회사 "Northwind" 분기 보고:
- 표지: "2026 1분기 사업 리뷰 / Northwind / 4월 30일"
- 본문: "핵심 성과 3가지" — 매출 성장, 신규 고객, 비용 효율 (각 1줄 설명)
- 차트: 분기별 매출 막대 차트 (Q1 120, Q2 145, Q3 138, Q4 170)

**웹 fixture** — 가상 제품 "Northwind" 랜딩:
- 히어로: 제목 "팀의 일을 한곳에" + 부제 1줄 + CTA 버튼 2개
- 섹션: 기능 카드 3개 (제목 + 1문장)
- 푸터: 로고 + 링크 4개 + 카피라이트

**premium fixture** — 위 3종 fixture는 standard 팩용이다. premium 팩은 8~12종 페이지를 요구하므로 부족하다. 팩의 `pages[].kind`에 대응하는 콘텐츠를 배치 단위로 미리 만들어 `_workspace/{batch}/fixtures/` 에 두고, 그 배치의 모든 팩이 **같은 fixture를 공유**한다 — 팩마다 다른 내용을 쓰면 렌더 차이가 디자인 차이인지 콘텐츠 차이인지 구별되지 않는다.

fixture 경로와 해시를 `render-manifest.json`에 남긴다:

```json
"content_fixture": { "path": "_workspace/{batch}/fixtures/ppt-premium.json",
                     "sha256": "sha256:..." }
```

**실존 상표·제품명·인물을 fixture에 쓰지 않는다.** 가상 회사·가상 제품으로 채운다 — 렌더는 공개 카탈로그에 그대로 실린다.

## 렌더 경로

**웹 트랙:** prompt.md 지시대로 단일 HTML 파일(인라인 CSS 또는 Tailwind CDN) 작성 → `_workspace/03_render_{slug}.html` → Playwright 등 헤드리스 브라우저로 데스크탑 폭(1280px)에서 풀페이지 스크린샷 → `design-packs/{slug}/preview.png`.

**PPT 트랙:** 16:9 캔버스의 슬라이드 3종(표지·본문·차트)을 한 장에 세로로 배치한 HTML 목업으로 렌더하는 방식을 기본으로 한다(가장 안정적). HTML 한 장 → 스크린샷 → `preview.png`. 실제 .pptx가 필요하면 python-pptx로 생성 후 LibreOffice(`soffice --headless --convert-to png`)로 변환하되, 변환 도구가 없으면 HTML 목업으로 폴백한다.

**baseline:** 같은 fixture를 "PPT를 만들어줘" / "랜딩페이지를 만들어줘" 수준의 **팩 없는 기본 요청**으로 렌더 → `_workspace/03_render_baseline-{track}.png`. 트랙당 1회만 만들고 모든 팩 검증에 재사용한다.

## 폰트 폴백

지정 폰트가 시스템·웹폰트로 확보되지 않으면 같은 분류(sans/serif/mono/display)의 가용 폰트로 폴백하고, 렌더 메모에 폴백 사실을 남긴다. 한글 콘텐츠는 Pretendard/Noto Sans KR 계열을 확보한다 — 한글이 두부(口)로 깨지면 렌더 실패로 처리한다.

## 산출물

- `design-packs/{slug}/preview.png` — 팩 적용 샘플 (사이트 카탈로그에도 쓰임).
- `_workspace/03_render_baseline-{track}.png` — 트랙 baseline.
- `_workspace/03_render_{slug}.html`(또는 .pptx) — 렌더 소스, 감사·재현용 보존.

## 에러 처리

렌더 실패(폰트·변환 도구 부재 등)는 1회 재시도 후 `needs_review` + `reason_code: render_failed`로 기록하고 사유와 함께 craft-qa·pack-architect에 보고한다. 렌더 증거가 없으면 production에서 제외한다 — 증거 없이 발행하지 않는다.
