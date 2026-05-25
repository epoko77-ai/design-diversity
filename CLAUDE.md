# Design Diversity

## 하네스: Design Diversity

**목표:** Claude가 산출하는 PPT·웹사이트 디자인의 천편일률 문제를 해결한다. 공개된 디자인 시스템·비주얼 스타일을 수집·증류해, Claude Code에 복붙하면 그 스타일이 재현되는 '디자인 팩' 카탈로그(1차 출범 40팩 = PPT 20 + 웹 20)를 만들고, baseline 대조로 다양성을 검증한 뒤 GitHub 공개 레포 + 카탈로그 웹사이트로 발행한다.

**트리거:** 디자인 팩 카탈로그 제작·확장·검증·발행 작업 요청 시 `design-diversity` 스킬을 사용하라. "디자인 팩 추가", "특정 팩만 다시", "다양성 검증 다시", "스키마 변경", "카탈로그 사이트 재배포" 등 후속 요청도 동일 스킬. 단순 질문은 직접 응답 가능.

**산출물 형식 (확정):** 각 팩 = `design-packs/{slug}/` 안의 `prompt.md` + `tokens.json` + `preview.png` + `meta.yaml`. 규격 SSOT는 `design-pack-schema` 스킬.

**팀 구성:** 에이전트 팀(7인) — design-scout · pack-architect · ppt-pack-curator · web-pack-curator · sample-renderer · diversity-qa · catalog-publisher. 스킬 8개(오케스트레이터 `design-diversity` + 컴포넌트 7). 상세는 `.claude/agents/`·`.claude/skills/`가 SSOT.

**발행:**
- GitHub: https://github.com/epoko77-ai/design-diversity (공개)
- 사이트(production): https://design-diversity.vercel.app — Vercel 프로젝트 `site` (team epoko77-9135), Deployment Protection 해제됨
- 카탈로그: 100팩 (PPT 50 + 웹 50), 전부 status pass. 표준 80 + 프리미엄 20. 프리미엄 팩은 팩당 5~7 상세페이지(catalog.json schema v2: category + pages). PPT는 차트 + 다이어그램·컴포넌트 키트 포함

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-05-20 | 초기 구성 (7 에이전트 + 8 스킬) | 전체 | - |
| 2026-05-20 | 1차 풀빌드 — 40팩 + 레포 + 사이트 발행 | catalog | - |
| 2026-05-20 | ppt-design-idioms에 전문 차트 기준 추가 | skills/ppt-design-idioms | PPT 차트 허접 피드백 |
| 2026-05-20 | 프리미엄 브랜드 스타일 20팩 추가 (40→60), PPT 20팩 차트 재작업·재렌더 | catalog | 전문성·고급화 피드백 |
| 2026-05-21 | ppt-design-idioms에 다이어그램·컴포넌트 키트 기준 추가 | skills/ppt-design-idioms | PPT가 색·분위기만 있고 다이어그램 양식 부재 피드백 |
| 2026-05-21 | 신규 20팩 추가 (60→80), 기존 30 PPT 다이어그램 키트 보완·재렌더, 사이트 PPT/웹 구분 강화 + 사용법 안내 추가 | catalog, site | 다이어그램 보강·사용법 피드백 |
| 2026-05-21 | 스키마 v2 (category + 상세페이지 pages) 도입, 프리미엄 20팩 추가 (80→100, PPT 50 + 웹 50), 팩당 5~7 상세페이지 렌더, 사이트 프리미엄 필터·상세페이지 갤러리·라이트박스 | skills/design-pack-schema, catalog, site | 프리미엄 등급·다활용 상세페이지 피드백 |
| 2026-05-24 | 프리미엄 10팩 추가 (100→110, PPT 50→60, 프리미엄 20→30) — 한국 대표 발표자료 10개 레퍼런스(삼성/SKT/현대차/네이버 통합보고서/카카오 + 산업통상부/과기정통부/기재부/국토부/고용부) 각각 10페이지 샘플 | catalog, site | 프리미엄 카탈로그 확장 |
| 2026-05-24 | 프리미엄 10팩 v2 재빌드 — 원본 PDF 다운로드 → design-analyst 페이지별 분석 → 재집필 → 재렌더로 충실도 100% 확보 (v1 메타 추론 폐기). 카탈로그 110팩 유지, 10팩 prompt.md/tokens.json/meta.yaml/preview·pages PNG 전부 교체 | catalog, site | 사용자 피드백 — v1이 실제 원본과 다름 |
| 2026-05-24 | 프리미엄 v3 — molit·moel(일반 문서) 탈락 + 문체부·통일부 신규 + 기존 8팩 페이지 1:1 mirror 재빌드. design-analyst 페이지별 정독 → page_mirror_plan → 재집필 → 페이지 mirror 렌더 → fidelity QA. 카탈로그 110팩 유지 | catalog, site | 사용자 피드백 — v2가 일반 문서 포함·디테일 부족 |
