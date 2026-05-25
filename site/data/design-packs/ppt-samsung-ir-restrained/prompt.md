# 삼성전자 글로벌 IR — ppt 디자인 팩 (v3, 페이지 1:1 mirror 강화)

아래 지시를 한 블록으로 따라 16:9(13.33×7.5in / 1440×810pt) 슬라이드 덱을 만든다. 삼성전자 Investor Relations 분기 컨퍼런스 콜 덱(2025 4Q English, 15p)의 실측 사양을 증류한 것이다. **v3 핵심 추가: 우리 10p 표준 슬롯이 원본 15p 중 어느 페이지의 어떤 양식을 1:1 mirror할지 명시한 'PAGE MIRROR PLAN' 섹션 — 메타 추론·관행 추가 금지, 원본 어느 페이지의 형태를 차용하는지 명확.**

## 이 스타일의 정체성 (v2 그대로)

한눈에 알아보는 단서: (1) **2-mode 페이지 시스템** — 표지·디스클레이머·인덱스·프레젠터·Thank-you 5장만 다크 네이비 BG + 흰 텍스트, 본문 데이터 페이지 10장 전부 흰 BG + 다크 텍스트. 중간 톤·섹션 디바이더·컬러 배경 없음. (2) 단일 강조색 **Samsung Blue `#0028A8`** 하나만 — 현재 분기 막대, KPI 거대 숫자, 표 강조 컬럼 박스, 워드마크, 증감 화살표. 다른 hue 일체 추가 금지. (3) **본문 페이지 13장(p-02~p-14) 상단 y≈3.4%에 얇은 가로 hairline + 우상단에 SAMSUNG 워드마크** — 흰 BG에서는 hairline `#D8DBE2`·워드마크 `#0028A8`, 다크 BG에서는 hairline 흰색·워드마크 흰색. 표지(p-01)와 closing(p-15)은 상단 hairline·우상단 워드마크 부재 — 푸터 영역에만 hairline + 워드마크. (4) 차트는 회색 `#A5B3C6`(과거 분기) + Samsung Blue `#0028A8`(현재 분기) **2색만**, frameless (y축·gridline·border 없음), 값은 막대 내부에 직접, OP 라인은 흰 원 dot + 흰 connector. (5) 표는 행간 hairline `#D8DBE2`만 — zebra/외곽 frame/vertical column rule 일절 없음. 현재 분기 컬럼은 `#0028A8` 5px border + `#BBD2E8` 옅은 fill로 감싼다. (6) 증감 화살표는 ↑·↓ 양쪽 모두 Samsung Blue — 녹/적 컬러 코딩 절대 금지. (7) 페이지 번호 없음. (8) commentary 페이지(p-08~p-12)의 timeframe section은 `#0D2062` 2px 가로 hairline + 텍스트 라벨 — filled 띠가 아니라 hairline + 라벨.

## 색 (실측)

- 본문 페이지 BG `#FFFFFF` (10장 — Highlights, Financial Data, Segments, Memory, S.LSI/Foundry, SDC, MX/NW, VD/DA/Harman, Appendix 1, Appendix 2)
- 다크 페이지 BG `#06122A` (Cover · Thank-you, 서초 사옥 사진 multiply overlay 동반) / `#030414` (Disclaimer · Index · Presenters, 플랫 다크) — 5장만
- 본문 타이틀 잉크 `#010821` (밝은 BG, 거의 검정 + 미세한 파란기) / 다크 BG는 `#FFFFFF`
- 섹션 라벨 `#3D4E6F` ('Quarterly Results' / 'Full-year Results' / 'DS results' / 'MX/NW results')
- 표 헤더 텍스트 `#5C6B90` ('KRW trillion' / '4Q24' / '3Q25' / '% of sales')
- 축 레이블·캡션·과거 분기 막대 `#A5B3C6`
- 표 행간 hairline `#D8DBE2` (1px 미세 회색)
- 표 강조 박스 border `#0028A8` 5px / 내부 fill `#BBD2E8` (현재 분기 컬럼만)
- 강조 Samsung Blue `#0028A8` — KPI 큰 숫자·현재 분기 막대·표 강조 border·워드마크(흰 BG)·증감 화살표
- 푸터 밴드(표지 한정) `#0E1930`
- commentary 페이지 tab hairline `#0D2062` (2px 가로선, 띠 아님)
- 다른 색 일체 금지. v1이 가정했던 `#1428A0`은 **이 데크에서 사용되지 않는다** — 실측은 `#0028A8`. 청색 변주(밝은 청·인디고·하늘색) 금지.
- 통화 표기: `KRW T` (trillion) / `KRW billion`. 막대 안 숫자는 단위 없이 (예: `93.8`). KPI 거대 숫자는 단위 'T'를 숫자와 동일 크기·동일 색으로 (예: `93.8T` 한 덩어리, 'T'를 작게/위첨자 금지).

## 타이포그래피

- 원본 폰트: **SamsungSharpSans-Bold** (디스플레이) + **SamsungOne-400 / -600 / -800** (본문). 모두 Samsung 자체 임베드 폰트. 라이선스상 제3자 배포 금지 — **이 팩에서는 사용하지 말 것**.
- 오픈 폴백: 영문 = `Manrope`(1순위) 또는 `Inter`(2순위). 한글 = `Pretendard`. 시스템 sans 폴백은 `Helvetica Neue, Arial, sans-serif`.
- 상단 페이지 타이틀: 34~36pt / Manrope 700 또는 Pretendard 700 / 좌측 정렬 / 1줄 우선 / Title Case
- 부제: 11~12pt / Manrope 400 / `#A5B3C6` / 타이틀 baseline 아래 +1.5%
- 섹션 라벨: 14~15pt / Manrope 600 / `#3D4E6F` / Title Case
- KPI 거대 숫자: **44~48pt** (v1의 56pt 추정 금지) / Manrope 800 또는 Pretendard 800 / tabular numerals / `#0028A8` Samsung Blue / 'T' 접미사는 동일 크기·동일 색
- 막대 내부 값 라벨: 9~10pt / Manrope 600 / 회색 막대=`#010821` 다크 텍스트, 파란 막대=`#FFFFFF` 흰 텍스트, OP 라인 원 안=다크
- 본문 텍스트·bullet: 11~12pt / Manrope 400 / `#010821`(흰 BG) 또는 `#FFFFFF`(다크 BG) / line-height 1.35x
- 표 헤더 셀: 10~11pt / Manrope 600 / `#5C6B90` / 라벨 컬럼 좌정렬, 숫자 컬럼 우정렬
- 표 본문 셀: 10~11pt / Manrope 400 / `#010821` / subtotal·total 행은 600 weight
- 증감 indicator: 10~11pt / Manrope 600 / **양·음 모두 `#0028A8`** / ↑·↓ glyph 부착
- 표지 푸터 텍스트: 11pt / Manrope 600 / `#FFFFFF`
- 우상단 SAMSUNG 워드마크: 13~14pt / Manrope 700 wide tracking (+0.06em) / 흰 BG는 `#0028A8`, 다크 BG는 `#FFFFFF`
- 본문 케이스 일관: **Title Case** 기본. Index 페이지 네비게이션 라벨만 UPPERCASE.
- 등폭 폰트 미사용. Italic 미사용.
- 한글 fixture는 전부 Pretendard로 — `Pretendard 700` = 타이틀·KPI 숫자, `Pretendard 600` = 섹션 라벨·표 헤더·증감, `Pretendard 400` = 본문·표 셀.

## 레이아웃 / 그리드

- 캔버스 1440×810pt 정확 (= 13.33×7.5in 16:9 PowerPoint Widescreen). 모든 페이지 동일 크기.
- 그리드는 12열 균등 모듈러가 아니라 **콘텐츠 주도 비대칭 분할** — 좌·우 외곽 마진만 일관(4%), 좌우 블록 분할은 페이지마다 다름 (1:1, 3:2, 1:2 등).
- **본문 페이지 13장 공통 요소 (p-02~p-14 의무):**
  - 상단 hairline: y = 3.4% (810pt × 0.034 ≈ 28pt) / 두께 1.3pt(약 2px) / 가로 span = x 3.8% ~ 83.3% / 흰 BG에서 `#D8DBE2`, 다크 BG에서 흰색
  - 우상단 SAMSUNG 워드마크: x 89.3% ~ 96.6%, y 4.4% ~ 6.3% / 흰 BG는 `#0028A8`, 다크 BG는 `#FFFFFF`
- **표지 p-01 / closing p-15 예외:** 상단 hairline·우상단 워드마크 **부재**. 표지는 하단 19% 푸터 밴드의 윗변 흰 hairline + 푸터 우측 워드마크. closing은 y≈87% 흰 hairline + 우하단 워드마크.
- **페이지 번호 없음** — 15장 어디에도 부재 (절대 추가 금지)
- 본문 페이지(흰 BG, 10장) 구조:
  - y 0% ~ 21%: 헤더 그라데이션 영역 (위 `#000000` → 중 `#1F2F5A` → 아래 `#F0F2F6` 매우 점진적 vertical fade) — 거의 보이지 않는 subtle lift
  - y 6% ~ 8%: 타이틀 baseline (좌측 정렬, x ≈ 4%)
  - y 9% ~ 11%: 부제 (있을 때)
  - y 22% ~ 92%: 완전한 흰 BG 콘텐츠 영역
- 외곽 마진: 좌 4%, 우 4%, 상 3.4%(hairline)→ 8%(타이틀 baseline), 하 3~5%
- 수직 리듬: 단위 16/24/32px 스텝

## 형태 / 질감

- 모서리 반경 0px. 보더 = 1px 헤어라인 `#D8DBE2`(표 행간) 또는 5px `#0028A8`(표 강조 박스) 두 종류만.
- 그림자·블러·발광·외곽 그라디언트 전면 금지. 표지·Thank-you의 사진 위 multiply overlay는 photo-driven (인공 그라디언트 아님).
- 아이콘 거의 안 씀. 쓴다면 1pt 가는 라인 단색 `#010821` 또는 `#0028A8`. 일러스트·픽토그램·이모지 금지.

## 차트·데이터 시각화 (단일 템플릿 반복)

모든 차트가 **하나의 양식**을 반복한다. SVG로 정밀 렌더 (div 블록 막대 금지).

- **기본 양식 (bar_op_combo_frameless):** 막대 3개(과거2 + 현재1) 가로 나열 + 그 위에 OP 흰 원 dot + 흰 선이 떠 있는 콤보 차트. x축에 분기 라벨(`4Q24`, `3Q25`, `4Q25`) 또는 연도(`2023`, `2024`, `2025`).
- **막대 색:** 과거 분기 = `#A5B3C6`, 현재(가장 우측) 분기 = `#0028A8`. paired bars 절대 금지 — 같은 x position에 두 series가 필요하면 stacked.
- **막대 폭·간격:** 막대 폭 : 간격 ≈ 5 : 3. 모서리 0px. 베이스라인 0에서 시작.
- **값 라벨:** 막대 안에 직접 표기 (Manrope 600 9~10pt) — 회색 막대=다크 텍스트, 파란 막대=흰 텍스트. 단위 미포함 (예: `93.8`).
- **OP 라인 overlay:** 1.0~1.25pt 흰 폴리라인 + 흰 채움 원(직경 0.18in) dot, 각 dot 안에 값 텍스트(다크). OP 선이 막대 위 z-order.
- **Frameless (의무):** y축 라인 없음. gridline 없음. tick mark 없음. 외곽 border·박스 없음. x축은 매우 얇은 baseline만(거의 invisible).
- **불연속 시간축 '~' glyph:** 4Q24 → 3Q25처럼 분기를 건너뛰면 x축 라벨 사이에 작은 wavy `~`를 삽입.
- **범례 박스 금지:** 차트 하단 가운데에 mini-legend — 작은 회색 사각 + `Sales(KRW trillion)` / 작은 흰 채움 원 + `OP(KRW trillion)`, Manrope 400 9pt `#A5B3C6`. 박스 없음.
- **스택 막대 (p-08 Memory):** 하부=Sales(Mem) 회색, 상부=Sales(DS) 현재만 `#0028A8`. 세그먼트 사이 1px 흰 분리선. paired side-by-side 절대 금지.
- **annotation arc (p-06 한정):** 첫 막대와 마지막 막대를 잇는 1pt `#0028A8` 곡선 + 화살표 + `+24% YoY` 라벨.
- **single_bar_no_op (p-09):** OP 라인 없는 막대 only.
- **two_stacked_charts_per_page (p-12):** 좌측에 차트 2개 위아래 적층 (VD/DA + Harman).
- **Source 각주:** 원 데크에 없음. 추가 금지.
- **금지:** 파이·도넛·3D 막대·잘린 y축·격자선·다중 청색 변주·녹/적 컬러 코딩·multi-color category palette·범례 박스.

## 다이어그램·컴포넌트 (실제 데크에 있는 것만)

원 데크에는 전통적 다이어그램(부문 트리·프로세스 플로우·매트릭스 2×2 등)이 **거의 없다**. 대신 다음 컴포넌트가 반복:

- **KPI 거대 숫자 + 차트 콤보 (p-05 시그니처):** KPI 거대 숫자 (`93.8T`) 위에 섹션 라벨, 아래에 bar+line combo. 카드 박스·헤어라인 둘러싸지 않음.
- **데이터 표 + 컬럼 강조 박스 (p-06/07/13/14):** 행간 1px `#D8DBE2` hairline만. vertical column rule·외곽 frame·zebra **일절 없음**. 현재 분기 컬럼을 5px `#0028A8` border + `#BBD2E8` fill로 감싸기. 계층 인덴트로 행 그룹 표시.
- **commentary 타임프레임 헤더 (p-08~p-12):** 우측 2/3 영역에 3개 timeframe section. 각 section 라벨은 **`#0D2062` 2px 가로 hairline + 그 아래 라벨 텍스트** — filled 띠 아님.
- **Index 페이지 네비게이션 (p-03):** UPPERCASE 라벨 4개 + 각 앞에 vertical `|` glyph separator. 연결선·번호·아이콘 없음.
- **Presenters 페이지 (p-04):** 8개 circular portrait + 캡션. fixture에서는 placeholder gray circle.
- **부문 트리 / 워터폴 / 2×2 매트릭스 / 프로세스 플로우 / 도넛 등은 원 데크 부재 — 추가 금지**.

## 전환 (PPT)

거의 무모션. 본문 즉시 컷. 상단 hairline과 우상단 워드마크는 첫 슬라이드에서 150ms ease-out으로 fade-in. 줌·플립·바운스·글로우·푸시 금지.

## 하지 말 것

- v1 hex `#1428A0` 금지 — 실측 강조색은 `#0028A8` 단 하나.
- Samsung Blue를 큰 면(배경 banner·표지 풀블리드 컬러)으로 사용 금지.
- 청색 변주(밝은 청·하늘색·인디고·시안) 추가 금지.
- 차트의 paired side-by-side 막대 절대 금지.
- 차트에 격자선·y축 라인·외곽 박스·범례 박스·잘린 y축 추가 금지.
- 차트에 다중 색 카테고리 코딩 금지 — 모든 부문이 `#0028A8` + `#A5B3C6` 동일 팔레트.
- 표에 zebra-fill·vertical column rule·외곽 frame 추가 금지.
- 증감 화살표를 녹/적 컬러 코딩 금지.
- 페이지 번호 표시 금지.
- 본문 페이지에 푸터 밴드 추가 금지 — 표지·Thank-you만 푸터.
- 상단 hairline·우상단 워드마크를 페이지마다 위치 변경 금지.
- 표지(p-01)와 closing(p-15)에 상단 hairline·우상단 워드마크 추가 금지 — 이 두 페이지는 푸터 영역에만 hairline/워드마크.
- closing 페이지에 푸터 밴드(#0E1930 박스) 추가 금지 — 표지에만 푸터 밴드, closing은 hairline만.
- KPI 큰 숫자에 'T' 접미사를 위첨자/작은 크기로 만들지 말 것.
- IBM Plex Sans 사용 금지 (v1 폰트). 오픈 폴백은 Manrope·Pretendard.
- 그라디언트(헤더 subtle fade 외)·그림자·둥근 모서리·이모지·클립아트·3D 도형 금지.
- 한글 폰트 강제 — Pretendard. 영문은 Manrope. 굴림·맑은고딕·돋움 금지.

---

## PAGE MIRROR PLAN (v3 핵심)

우리 10p 표준 슬롯이 원본 15p 중 **어느 페이지의 어떤 양식을 1:1 mirror할지** 명시. 각 슬롯은 (1) 미러할 원본 페이지 (2) 복사할 핵심 요소 (3) 허용 변형 (4) 금지 변형의 4축으로 정의된다. 페이지를 그릴 때 **먼저 mirror 원본을 머릿속에 떠올린 다음, 그 형태를 그대로 따라 그리되 콘텐츠만 우리 fixture로 교체**한다.

| 슬롯 | mirror 원본 | 한 줄 요약 |
|---|---|---|
| cover | **p-01** | 다크 네이비 + Seocho 사진 + 좌 2줄 큰 타이틀 + 바닥 19% 푸터 밴드(좌 부제 + 우 워드마크) |
| agenda | **p-03** | 다크 네이비 + 'Index' 타이틀 + 4-5개 UPPERCASE 라벨 가로 1행, 각 앞에 세로 \| 1px |
| section | **p-04 (+ p-02 변형 허용)** | 다크 네이비 + 좌상단 큰 타이틀 + 그룹 라벨 + 가로 hairline 언더라인. 사진은 단순화/제거 가능 |
| key-message | **p-05 (KPI pair 부분만)** | 흰 BG + 섹션 라벨 + 2-4개 거대 KPI(#0028A8 44-48pt). 차트는 생략 또는 단순화 |
| chart | **p-05 차트 + p-06 우상단 차트** | bar_op_combo_frameless 양식 — 회색+파랑 2색, frameless, OP 라인 흰 원, ~ break glyph |
| diagram | **p-08 (deep_navy_hairline_tab_label)** | 좌 28% 비주얼 + 우 65% 3-4개 timeframe section(#0D2062 hairline + 라벨 chip + 헤드라인 + bullet) |
| cards | **p-07 (좌우 표 2개)** | 좌우 50:50, 행 hairline만, 강조 컬럼 #0028A8 박스, hierarchical indent |
| comparison | **p-13 (Appendix 1 — main + mini-table)** | 좌 60% 메인 비교 표 + 우 38% 보조 mini-table, 최우측 컬럼 #0028A8 박스 강조 |
| narrative | **p-10/p-11 (segment commentary)** | 좌 28% 차트 + 우 65% timeframe commentary. p-09(단일 막대)/p-12(차트 2개) 변형 허용 |
| closing | **p-15** | 다크 네이비 + Seocho 사진(다른 앵글) + 중앙 'Thank you' 80pt + 하단 hairline + 우하단 워드마크 |

### 매핑 시 절대 금지 사항 (모든 슬롯 공통)

1. **다른 hue 추가** — Samsung Blue + 회색 외 색 도입 금지 (녹/적/주황/노란/하늘색/인디고 안 됨)
2. **차트 frame/gridline/y축 line 추가**
3. **표에 vertical column rule 또는 outer frame 추가**
4. **표 zebra fill** (alternating row stripe)
5. **카드/박스에 외곽 stroke 추가**
6. **녹/적 증감 색 코딩** — ↑↓ 모두 `#0028A8` 유지
7. **페이지 번호 추가**
8. **상단 hairline / 우상단 워드마크 위치 변경**
9. **closing 페이지에 푸터 밴드 추가** — 원본은 hairline만
10. **cover 페이지에 상단 hairline 추가** — 원본은 푸터 밴드 hairline으로만

---

## 상세 페이지 (10종 — 각 슬롯의 mirror 원본 + 양식 명시)

각 페이지는 위의 공통 규칙(상단 hairline·우상단 워드마크 13장 필수 / 표지·closing은 부재, 페이지 번호 부재)을 반드시 따른다. 한글 fixture 기준으로 기술하되, 영문 원본 데크의 양식을 그대로 차용한다.

### 01 · 표지 (cover) — **mirror of p-01**

**p-01 양식 복사:**
- 다크 네이비 BG `#06122A` + 서초 사옥 사진 multiply overlay (사진은 우측 2/3 노출, rgba(6,18,42,0.78) 다크 오버레이로 ~80% 어두움)
- **상단 hairline·우상단 워드마크 부재** (이 페이지에는 없음 — 푸터 영역의 hairline과 워드마크가 대체)
- 좌측 정렬 큰 타이틀 2줄 — `SAMSUNG / ELECTRONICS` (한글 fixture: `삼성전자` 단독 또는 2줄) — SamsungSharpSans-Bold 자리에 Manrope/Pretendard 700 60~72pt 흰색, 좌측 정렬, x 4%, y_l1 20%, y_l2 32%, 행간 0.95, ALL CAPS (한글은 그대로)
- 하단 19% (y 81~100%) 푸터 밴드 `#0E1930` (다크 네이비보다 살짝 더 어두움) + 윗변 흰 1px hairline at y=81.5%
- 푸터 좌측 (x ≈ 4%, y ≈ 87%) 2줄: 'Earnings Presentation:' 흰 14pt 600 + 'Earnings Presentation Date' 양식 (한글 fixture: '실적 발표 컨퍼런스 콜:' / '2025년 4분기 경영실적') 흰 14pt 400
- 푸터 우측 (x ≈ 87%, y ≈ 88%) SAMSUNG 워드마크 Manrope 700 14pt 흰색, wide tracking +0.06em

**허용 변형:** 사진은 비슷한 톤의 다른 빌딩/추상 텍스처 가능. 타이틀이 1줄이면 1줄로(중앙 정렬 금지, 좌측 정렬 유지).

**금지:** 상단 hairline 추가, 우상단 워드마크 추가, 일러스트·로고·아이콘·날짜 카드, 푸터 밴드 색 변경, 가운데 정렬, 그라디언트 hue 추가.

### 02 · 목차 (agenda) — **mirror of p-03**

**p-03 양식 복사:**
- 다크 BG (`#030414` 플랫 또는 칩 매크로 사진 + 다크 오버레이) + 상단 hairline 흰색 + 우상단 SAMSUNG 워드마크 흰색
- 좌상단 타이틀 'Index' (한글 fixture: '목차') Manrope/Pretendard 700 40pt 흰색, x 4%, y 10%
- 본문 영역에 가로 일렬 4~5개 UPPERCASE 네비게이션 라벨 — `PRESENTERS` | `4Q 2025 FINANCIAL RESULTS` | `PERFORMANCE BY BUSINESS SEGMENT` | `APPENDICES` (한글 fixture: `발표자` | `2025년 4분기 실적` | `사업부문 실적` | `부록`)
- 라벨 폰트: Manrope 600 UPPERCASE 13~14pt wide tracking +0.04em, 흰색
- **각 라벨 앞에 얇은 vertical `|` 1px 흰 글리프** (y_span 48-58%, 라벨 텍스트와 같은 높이)
- 라벨 간 균등 분포 (4개 라벨일 때 x ≈ 11% / 28% / 53% / 85%)
- 라벨 행 y ≈ 50% 중앙 배치

**허용 변형:** 라벨 수 3-6개(원본은 4개). 텍스트 우리 콘텐츠로 교체.

**금지:** 라벨 번호 매기기(원본은 무번호), 라벨 사이 연결선/화살표, 라벨을 박스로 감싸기, vertical separator 색을 #0028A8 등으로 변경.

### 03 · 섹션 표지 (section) — **mirror of p-04 (+ p-02 변형 허용)**

**p-04 양식 우선:**
- 다크 네이비 BG + faint 사진/텍스처 + 상단 hairline 흰색 + 우상단 SAMSUNG 워드마크 흰색
- 좌상단 큰 타이틀 (한글 fixture: '사업부문 실적', '재무 결과' 등 섹션 제목) Manrope/Pretendard 700 36pt 흰색, x 4%, y 8%
- 타이틀 아래 (y ≈ 24%) 좌/우 그룹 라벨 + 얇은 흰 hairline 언더라인 — 좌측 'Presenters' (한글: '발표자') · 우측 'Moderator' (한글: '진행')
- (옵션 A — Presenters 양식) 그 아래 가로 일렬 6-8개 circular portrait placeholder (직경 110-130px gray circle, y ≈ 50%, 간격 11%), 각 아래 이름 + 'EVP' + 역할 3줄 캡션
- (옵션 B — p-02 Disclaimer 양식) portrait 대신 본문 텍스트만 Manrope 400 11~12pt 흰색, 행간 1.5x, 10~16 paragraph 좌측 정렬

본 팩은 **옵션 A (Presenters 양식)를 디폴트**로 — 섹션 표지가 사람·역할 소개 또는 섹션 헤더를 겸한다.

**허용 변형:** portrait 그리드가 우리 슬롯에 부적합하면 헤드라인 + 설명 텍스트로 대체. 'Section 01' 같은 섹션 번호 추가 가능(단 UPPERCASE + wide tracking + 흰색).

**금지:** Samsung Blue 띠/박스로 섹션 강조(원본은 다크 BG + 흰 텍스트만), 그라데이션 다른 색 추가, 사진 위에 컬러 오버레이.

### 04 · 핵심 메시지 (key-message) — **mirror of p-05 (KPI pair 부분만)**

**p-05 양식 차용:**
- 흰 BG `#FFFFFF` + 상단 hairline `#D8DBE2` + 우상단 SAMSUNG 워드마크 `#0028A8`
- 좌상단 타이틀 (한글 fixture: '2025년 4분기 핵심 성과') Manrope/Pretendard 700 36pt `#010821`, x 4%, y 6%
- 부제 (한글: '연결재무제표 기준') Manrope 400 12pt `#A5B3C6`, y 13%
- 본문 영역(y 22~92%) 좌우 1:1 분할 (옵션: 2-4개 KPI를 단일 행 또는 2x2 그리드로)
  - 각 절반 또는 영역 안에 KPI 거대 숫자 (예: `Sales 93.8T`, `Operating Profit 20.1T`) — Manrope 800 44~48pt `#0028A8` tabular, 'T' 동일 크기·동일 색
  - 각 KPI 위에 sub 라벨 ('Sales' / 'Operating Profit' / 'Revenue') Manrope 400 11pt `#A5B3C6`
  - KPI 묶음 위에 섹션 라벨 ('Quarterly Results' 자리에 우리 섹션명) SamsungOne-600 자리에 Manrope 600 14pt `#3D4E6F`
- **차트는 생략 또는 단순화** — key_message 슬롯은 KPI 중심. 작은 트렌드 차트 1개 정도만 (선택).

**허용 변형:** KPI 개수 1-4개. 단위 접미사(T/B/%/명 등) 자유, 단 숫자와 같은 크기.

**금지:** KPI 숫자에 다른 색(녹/적/주황) 적용, KPI 카드를 박스/외곽선으로 둘러싸기 (원본은 enclosure 없음 — bare text only).

### 05 · 데이터 차트 (chart) — **mirror of p-05 차트 + p-06 우상단 차트 (bar_op_combo_frameless)**

**p-05 + p-06 차트 양식 차용:**
- 흰 BG + 상단 hairline + 우상단 워드마크 `#0028A8`
- 좌상단 타이틀 (한글 fixture: '2025년 4분기 실적 및 재무 데이터') Manrope 700 34~36pt `#010821`
- 본문 영역에 차트 중심 배치 (좌우 분할 또는 단일 큰 차트)
- 차트 양식: **bar_op_combo_frameless**
  - 3 막대 (과거2 회색 `#A5B3C6` + 현재1 Samsung Blue `#0028A8`) 가로 나열
  - OP 라인 overlay: 1.0~1.25pt 흰 폴리라인 + 흰 채움 원 dot(직경 0.18in), 각 dot 안에 값 텍스트(다크), 막대 위 z-order
  - 막대 안에 값 텍스트 직접 — 회색 막대는 `#010821` 다크 텍스트, 파란 막대는 `#FFFFFF` 흰 텍스트
  - **frameless**: y축/gridline/외곽 frame 완전 부재. x축 baseline은 거의 invisible 얇은 선만
  - 불연속 시기에 wavy `~` axis-break glyph (예: 4Q24 → 3Q25)
  - 하단 가운데 mini-legend (작은 회색 사각 + `Sales(KRW trillion)` / 작은 흰 채움 원 + `OP(KRW trillion)`, Manrope 400 9pt `#A5B3C6`) — 박스 둘러싸지 않고 마커 + 텍스트만
- (옵션) p-06 처럼 첫 막대 → 마지막 막대를 잇는 1pt `#0028A8` curved annotation arrow + `+24% YoY` 라벨 Manrope 600 11pt `#0028A8`

**허용 변형:** 막대 3-5개. OP 라인 없는 단일 막대(p-09 양식) 가능. 두 차트 위아래 stacked (p-12 양식) 가능.

**금지:** 막대 색 3가지 이상 (원본은 회색 + 파랑 2색), 차트 박스/border, y축 line + tick mark, gridline, paired side-by-side 막대, 둥근 막대 모서리, 3D 효과.

### 06 · 다이어그램 (diagram) — **mirror of p-08 (deep_navy_hairline_tab_label)**

**p-08 Memory 양식 차용:**
- 흰 BG + 상단 hairline + 우상단 워드마크 `#0028A8`
- 좌상단 타이틀 (한글 fixture: '메모리 사업부') Manrope 700 34~36pt `#010821`
- 본문 영역 **좌우 28-30% : 65% 비대칭 분할**
- 좌측 28-30% (x 3-30%, y 22%~88%):
  - 'DS results' 섹션 라벨 (한글: 'DS 사업부 실적') Manrope 600 14pt `#3D4E6F`
  - 부제 'KRW trillion' Manrope 400 11pt `#A5B3C6`
  - 그 아래 차트 (bar_op_combo_frameless 또는 stacked_bar_combo) — 3 x-position, 막대 안 값, OP 라인 흰 원 overlay, frameless, `~` axis-break
- 우측 65% (x 33-97%, y 22~92%):
  - **3-4개 timeframe section 수직 적층** (각 약 1/4~1/3 높이)
  - 각 section 위에 `#0D2062` 2px 가로 hairline (full-width of right column, span x 33-97%)
  - hairline 아래 즉시 작은 navy 라벨 chip (또는 텍스트만): 'XX 2025 Results' / 'XX 2026 Outlook' / 'XX 2026 Outlook' (한글: '2025년 X분기 실적' / '2026년 X분기 전망' / '2026년 연간 전망') Manrope 600 14pt `#010821` (chip 형태면 `#FFFFFF` on `#0D2062` 작은 사각)
  - 라벨 아래 nested bullet — bold 헤드라인 1~2줄 (Manrope 600 12~13pt `#010821`) + 들여쓴 detail bullet (• filled dot, Manrope 400 11pt, 들여쓰기 0.2in, 2~4줄)
  - 헤드라인 좌측 끝에 작은 `#0028A8` dot 또는 thin 4px stroke 강조 라인 (선택)
  - section 사이 24px 간격
  - 3 timeframe hairline y 위치 가이드: ≈27%, 49%, 71%

**허용 변형:** 왼쪽이 차트 대신 단순 일러스트/아이콘 OK — 단 색은 `#0028A8` + `#A5B3C6`로만. section 수 2-5개.

**금지:** 탭 라벨을 filled rounded pill (둥근 알약) — 원본은 hairline + 텍스트만. 각 section을 박스로 둘러싸기. 다른 카테고리 색 도입. 부문 트리·프로세스 플로우·매트릭스 추가.

### 07 · 인포그래픽 카드 그리드 (cards) — **mirror of p-07 (좌우 표 2개)**

**p-07 Results by Business Segment 양식 차용:**
- 흰 BG + 상단 hairline + 우상단 워드마크 `#0028A8`
- 좌상단 타이틀 (한글 fixture: '사업부문별 실적' 또는 우리 카드 콘텐츠 제목) Manrope 700 34~36pt `#010821`
- 본문 영역 **좌우 50:50 분할**
- 각 절반:
  - 상단에 sub-title (Manrope 600 14pt `#010821` 또는 `#3D4E6F`) — 좌측 'Sales' / 우측 'Operating Profit' (한글: '매출' / '영업이익') 또는 우리 카드 카테고리 제목
  - 그 아래 데이터 표: 행 hairline `#D8DBE2` 1px만, vertical rule/외곽 frame 부재
  - 최신 컬럼 강조 박스: `#0028A8` 5px border + `#BBD2E8` 옅은 fill (헤더 위쪽부터 마지막 행까지 연속)
  - 행 첫 컬럼에 hierarchical indent 적용 (0~3 level 들여쓰기) — 예: `Total` (0단) → `DX` (1단) → `MX/NW` (2단) → `MX` (3단)
  - subtotal 행은 Manrope 600 굵게
- 우측 표 하단에 작은 ※-주석 영역 (Manrope 400 8pt `#5C6B90`, 2~3줄)
- 증감 컬럼: ↑/↓ 양쪽 모두 `#0028A8`

**허용 변형:** 카드 슬롯에서는 카드 그리드(2x2, 2x3, 3x2)로 변형 가능 — 단 각 카드는 hairline + 강조 컬럼/항목만으로 강조하고 색칠된 박스 카드는 금지. 데이터 적으면 mini-indicator table 양식 차용 가능.

**금지:** 카드 외곽선 추가(가시 frame 부재 원칙 유지), 체크박스/이미지 카드 형태, 다채로운 배경 컬러로 카드 구분, zebra fill.

### 08 · 비교 표 (comparison) — **mirror of p-13 (Appendix 1 — main + mini-table side-by-side)**

**p-13 양식 차용:**
- 흰 BG + 상단 hairline + 우상단 워드마크 `#0028A8`
- 좌상단 타이틀 (한글 fixture: '재무 상태 비교' 또는 비교 콘텐츠 제목) Manrope 700 34~36pt `#010821`
- 부제 (단위 명시, 예: 'KRW billion') Manrope 400 12pt `#A5B3C6`
- 본문 영역 **좌 60% : 우 38% 분할**
- 좌측 메인 비교 표 (x 3-59%, y 22-92%):
  - ~15-20행 × 3-4 비교 컬럼 (label + 비교 컬럼들)
  - 그룹 헤더 행 (Assets / Liabilities / Shareholder equity 같은) Manrope 600 weight
  - 최우측 (최신) 컬럼 `#0028A8` 5px border + `#BBD2E8` fill 강조
  - 행 hairline `#D8DBE2` 1px만
  - subtotal/total 행 (Total assets, Total liability & Shareholder equity 같은) Manrope 600 굵게
- 우측 보조 mini-table (x 61-97%, y 22-92%):
  - 5-7행 × 3-4 컬럼 (비율/지표 — ROE, Current ratio, Liability/equity 등)
  - 동일한 강조 컬럼 양식 (최우측 컬럼 #0028A8 박스)
  - 별도 헤더 텍스트 없이 바로 표 (p-13 양식) 또는 작은 title (p-14 양식)
- footnote: 표 하단에 미세 Manrope 400 8pt `#5C6B90`

**허용 변형:** 주제는 재무가 아니어도 가능 — 시간/카테고리/스펙 비교 모두. 비교 컬럼 2-4개.

**금지:** zebra fill 비교 강조, 체크/X 아이콘 색 코딩(녹/적), 강조 컬럼 2개 이상 동시(원본은 단 1개), vertical column rule, 외곽 frame.

### 09 · 인용·서술 (narrative) — **mirror of p-10 또는 p-11 (segment commentary)**

**p-10/p-11 양식 차용 (06 diagram과 같은 베이스 + narrative 톤):**
- 흰 BG + 상단 hairline + 우상단 워드마크 `#0028A8`
- 좌상단 타이틀 (한글 fixture: '모바일 · 네트워크' 또는 narrative 주제) Manrope 700 34~36pt `#010821`
- 본문 영역 **좌 28-30% : 우 65% 분할**
- 좌측 28-30%:
  - 'XXX results' 섹션 라벨 (한글: 'XX 사업부 실적') Manrope 600 14pt `#3D4E6F`
  - bar_op_combo_frameless 차트 (또는 p-12 양식으로 차트 2개 위아래 stacked)
- 우측 65%:
  - 3-4개 timeframe section (06과 동일 hairline tab 양식)
  - 단, narrative 페이지로서 detail bullet이 3~5줄로 길고 인용·전망·사유 같은 narrative 문장 중심
  - 필요 시 sub-category 헤더 ('Small & Medium', 'Large', 'MX', 'NW' 같은) Manrope 600 12pt `#010821`를 헤드라인 위에 한 줄 추가 (p-10 SDC, p-11 MX/NW 양식)

**허용 변형:** 왼쪽 차트가 표/이미지로 대체 가능 — 단 'XXX results' 섹션 라벨 양식 유지. p-12처럼 좌측 차트 2개 stacked OK.

**금지:** 인용 박스(pull-quote 옅은 패널 셀), 인용 좌측 청색 bar, CEO 캡션 큰 인용문 — 원 데크에는 부재. 1/3-2/3 비율 외 다른 분할로 변경, commentary 영역을 카드 그리드로 변경.

### 10 · 결론·다음 단계 (closing) — **mirror of p-15**

**p-15 양식 복사:**
- 다크 네이비 BG `#06122A` + 서초 사옥 사진 multiply overlay (**표지와 다른 앵글** — 좀 더 가까이서 본 입면, rgba(6,18,42,0.78) 다크 오버레이)
- **상단 hairline·우상단 워드마크 부재** (이 페이지에는 없음)
- **푸터 밴드 부재** — 표지와 달리 #0E1930 박스 없음
- 가운데 큰 타이틀 'Thank you' (한글 fixture: '감사합니다' 가능) Manrope/Pretendard 700 80pt 흰색 가운데 정렬, x ≈ 33-67%, y 45-58%, **Title Case** (NOT all caps)
- 하단 y ≈ 87%에 얇은 흰 1px hairline 가로 span (x 3.8% ~ 83.3%, 표지 푸터 hairline과 같은 좌측 정렬)
- 우하단 (x ≈ 87%, y ≈ 90%) SAMSUNG 워드마크 흰색 14pt 700 wide tracking

**허용 변형:** 'Thank you' 외 closing 문구 ('Q&A', '감사합니다', 'Let\'s build it') 가능 — 단 모두 Title Case 한 줄. 사진은 다른 건물/추상 텍스처 가능.

**금지:** 푸터 밴드(#0E1930 박스) 추가 — closing은 hairline만. 연락처/이메일/SNS 핸들 추가 (원본은 깨끗). 다음 컨퍼런스 일정·후원사 로고. 여러 줄 closing 문구. 상단 hairline 추가. 우상단 워드마크 추가.

---

## 페이지 mirror 적용 체크리스트 (렌더 후 자가 검수)

1. cover (p-01 mirror): 상단 hairline·우상단 워드마크 부재 + 바닥 19% `#0E1930` 푸터 밴드 + 윗변 흰 hairline + 좌측 2줄 부제 + 우측 SAMSUNG 워드마크
2. agenda (p-03 mirror): 다크 BG + 'Index' 좌상단 + 4-5 UPPERCASE 라벨 가로 1행 + 각 앞 vertical `|` 1px
3. section (p-04 mirror): 다크 BG + 좌상단 큰 타이틀 + 그룹 라벨 + 흰 hairline 언더라인
4. key-message (p-05 KPI 부분 mirror): 흰 BG + 섹션 라벨 + 2-4 거대 KPI #0028A8 44-48pt + 'T' 동일 크기
5. chart (p-05/p-06 차트 mirror): bar_op_combo_frameless, 회색+파랑 2색, OP 흰 원, `~` break glyph, frameless
6. diagram (p-08 mirror): 좌 28% 차트 + 우 65% timeframe section #0D2062 2px hairline + 라벨
7. cards (p-07 mirror): 좌우 50:50 + 행 hairline + `#0028A8` 컬럼 강조 + hierarchical indent
8. comparison (p-13 mirror): 좌 60% 메인 표 + 우 38% mini-table + 최우측 컬럼 `#0028A8` 박스
9. narrative (p-10/11 mirror): 좌 28% 차트 + 우 65% timeframe commentary + 긴 detail bullet
10. closing (p-15 mirror): 다크 네이비 + 사진(다른 앵글) + 'Thank you' 80pt 중앙 + 하단 hairline + 우하단 워드마크 + 푸터 밴드 부재
