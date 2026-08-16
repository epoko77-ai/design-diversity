---
name: catalog-publishing
description: >-
  검증 통과한 디자인 팩을 GitHub 공개 레포로 구조화하고, 팩을 탐색·필터·복사할 수 있는 Next.js 카탈로그
  웹사이트로 빌드해 Vercel에 배포하는 방법론 스킬. catalog-publisher 에이전트가 사용한다. 레포 레이아웃,
  README/CONTRIBUTING/LICENSE 구성, 정적 사이트 사양, 배포 절차, 자체 QA 체크리스트를 규정한다.
---

# Catalog Publishing — 레포·카탈로그 사이트 발행

catalog-publisher가 디자인 팩 카탈로그를 GitHub + 웹사이트로 발행할 때 따르는 방법.

## 레포 레이아웃

```
design-diversity/
  README.md          ← 프로젝트 목적·사용법·카탈로그 개요
  CONTRIBUTING.md     ← 새 팩 추가 절차 + 스키마 링크
  LICENSE             ← 명세·토큰의 재배포 라이선스
  catalog.json        ← 머신리더블 인덱스
  design-packs/{slug}/ prompt.md · tokens.json · preview.png · meta.yaml
  site/               ← Next.js 카탈로그 앱
```

## README 구성

방문자가 30초 안에 "왜·무엇·어떻게"를 알게 한다:
1. **왜** — Claude가 산출하는 PPT·웹 디자인이 천편일률인 문제. 이 카탈로그가 그 다양성을 푼다.
2. **무엇** — 디자인 팩이란 무엇인가(prompt.md + tokens.json + preview.png + meta.yaml), 현재 팩 수(트랙별).
3. **어떻게 쓰나** — 팩 폴더에서 `prompt.md`를 복사해 Claude Code에 붙여넣고 "이 스타일로 만들어줘"라고 요청. 카탈로그 사이트 링크.
4. 기여 안내(`CONTRIBUTING.md`), 라이선스.

## 라이선스 / 저작권 위생

`LICENSE`는 **이 레포가 배포하는 것**(디자인 명세·토큰·문서)에 적용한다. 권장: MIT 또는 CC BY 4.0.
README·CONTRIBUTING에 명시할 경계: "각 팩은 공개 디자인 시스템·스타일에서 학습한 시각 원리의 명세이며, 특정 제품의 상표·로고·독점 자산을 재배포하지 않는다. 각 팩의 출처는 `meta.yaml`에 기재한다." 라이선스 모호 팩(`license: unclear`)은 발행 전 pack-architect와 함께 정리한다.

## 카탈로그 웹사이트 사양

- **스택:** Next.js 15 App Router + TypeScript. 데이터는 빌드 타임에 `catalog.json` + `design-packs/` 폴더에서 정적 생성(SSG). 런타임 DB 없음.
- **핵심 동선 = 복사.** 방문자가 (1) 팩 그리드 갤러리를 훑고 (2) 트랙(PPT/웹)·스타일 축으로 필터하고 (3) 팩 상세에서 `prompt.md`를 **원클릭 복사**한다. 복사 버튼이 가장 눈에 띄어야 한다.
- **팩 카드:** `preview.png` 썸네일 + display_name + 트랙 배지 + axes 태그. production 카탈로그의 입력은 `publishable` 팩으로 **필터링**한다 — 비통과 팩에 배지를 달아 노출하지 않는다.
- **팩 상세:** 큰 preview, prompt.md 전문(복사 버튼), tokens.json 토큰 시각화(색 스와치 등), meta.yaml 출처.
- **사이트 자신이 좋은 디자인이어야** 설득력이 있다. 절제된 타이포·명확한 그리드·일관 색. `frontend-design` 스킬의 미감 원칙을 참고하되 카탈로그는 중립적 톤으로(특정 팩 스타일에 치우치지 않게).
- 반응형(모바일~데스크탑), 다크모드는 선택.

## 배포 절차

1. `site/`에서 빌드 — `npm run build` 통과 확인.
2. Vercel **preview** 배포 → preview URL 확보.
3. 자체 QA(아래) 통과 후, preview URL을 사용자에게 보고.
4. **production 배포는 사용자 명시 승인 후에만.** 승인 전까지 preview에 머문다.
5. GitHub 공개는 사용자가 원격 레포를 지정·승인한 뒤 수행한다.

## 발행 게이트 — `status`를 사람이 쓰지 않는다

카탈로그에 나가는 `status`는 손으로 적는 문자열이 아니라 게이트 결과에서 **생성**된다.

`publishable`의 정의와 모드별 필요 게이트는 **`design-pack-schema`의 상태식 절이 SSOT**다. 여기에 식을 복제하지 않는다 — 복제하면 한쪽만 고쳐져 갈라진다.

- `status: pass`인 팩만 production 카탈로그에 포함한다.
- `needs_review` · `reject` 팩은 **draft 배지로 내보내지 않는다.** 검증에 실패한 팩을 공개하는 것이 카탈로그 신뢰도를 갉아먹는다. 내부 검토 목록으로 분리한다.
- 게이트 산출물(`fidelity_qa/` · `craft_qa/` · `render-manifest.json`)이 없으면 빌드를 **실패시킨다** — 조용히 통과시키지 않는다.

> v2까지는 "2회 반려 후 escalate → draft 배지로 발행"이었다. 이 규칙은 폐기한다.

## 자체 QA 체크리스트

배포 보고 전 직접 확인:
- [ ] `npm run build` 성공, 콘솔 에러 없음
- [ ] 모든 팩 카드가 렌더되고 `preview.png`가 깨지지 않음
- [ ] 트랙·축 필터가 동작
- [ ] 팩 상세의 prompt.md 복사 버튼이 실제로 클립보드에 복사
- [ ] 모바일 폭(375px)에서 레이아웃 깨짐 없음
- [ ] `catalog.json`의 팩 수 = `design-packs/` 폴더 수
- [ ] production 데이터에 `needs_review`·`reject` 팩이 **포함되지 않음** (내부 검토 목록에만 존재)

## 재실행

기존 `site/`·레포가 있으면 전면 재생성하지 않고 증분 반영(새 팩 카드 추가, `catalog.json` 갱신). "사이트 재배포"만 요청되면 빌드·배포만 수행한다.
