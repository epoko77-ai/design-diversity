# Design Diversity

## 하네스: Design Diversity

**목표:** Claude가 산출하는 PPT·웹사이트 디자인의 천편일률 문제를 해결한다. 공개된 디자인 시스템·비주얼 스타일을 수집·증류해, Claude Code에 복붙하면 그 스타일이 재현되는 '디자인 팩' 카탈로그(1차 출범 40팩 = PPT 20 + 웹 20)를 만들고, baseline 대조로 다양성을 검증한 뒤 GitHub 공개 레포 + 카탈로그 웹사이트로 발행한다.

**트리거:** 디자인 팩 카탈로그 제작·확장·검증·발행 작업 요청 시 `design-diversity` 스킬을 사용하라. "디자인 팩 추가", "특정 팩만 다시", "다양성 검증 다시", "스키마 변경", "카탈로그 사이트 재배포" 등 후속 요청도 동일 스킬. 단순 질문은 직접 응답 가능.

**산출물 형식 (확정):** 각 팩 = `design-packs/{slug}/` 안의 `prompt.md` + `tokens.json` + `preview.png` + `meta.yaml`. 규격 SSOT는 `design-pack-schema` 스킬.

**팀 구성:** 에이전트 팀(11인) — design-scout · **reference-analyst** · pack-architect · ppt-pack-curator · web-pack-curator · **reference-pack-curator** · sample-renderer · **craft-qa** · **fidelity-qa** · diversity-qa · catalog-publisher. 스킬 11개(오케스트레이터 `design-diversity` + 컴포넌트 10). 상세는 `.claude/agents/`·`.claude/skills/`가 SSOT.

**모델 배분:** reference-analyst·reference-pack-curator = Fable 5 / fidelity-qa = Opus 5 (+ Codex `gpt-5.6-sol` 이종 교차검증) / 나머지 = Sonnet 5. 결정적 검사는 모델이 아니라 `scripts/validate_pack.py`가 수행.

**3게이트:** 발행 조건은 `fidelity_pass AND craft_pass AND diversity_pass`. 합산하지 않으며, 다양성이 충실도를 상쇄할 수 없다. 검증 실패 팩은 draft로 발행하지 않는다.

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
| 2026-08-17 | **프리미엄 35팩 prompt.md 밀도 고도화** — 페이지당 지시(constraint atom)를 전 팩 ≥14로 상향(작업 전 28/35 미달, 최저 7.0 → 작업 후 미달 0, 최저 15.4·중앙 19.0). 수치·hex 검증 가능 비율 중앙 75%. 자기모순 지시·캔버스 계약 오류·`spec_version` 불일치·`pages` 정합 실패 동반 수정으로 HARD FAIL 12팩 → 6팩. 웹 팩은 브레이크포인트별 값·`focus-visible` 상태·`prefers-reduced-motion`·대비 실측 추가, 역사 양식 팩은 정전 원리를 수치화. `style_synthesis` 팩의 `source_depth`를 `full`→`partial`로 정정(2차 자료 기반) | design-packs | 사용자 요청 — 팩 프롬프트가 얇아 Claude가 빈칸을 기본값으로 메우는 문제 |
| 2026-08-16 | **신규 프리미엄 5팩 — 집필·렌더 완료, fidelity 미통과로 중단** (krafton·shinhan·posco·samsungbio·hdhyundai). 전부 `status: needs_review`이며 `catalog.json`·사이트 미반영 = 카탈로그는 110팩 유지. 재개 절차·수리 백로그 36건은 `_workspace/premium_v4/00_HANDOVER.md` | design-packs | fidelity 게이트 3팩 반려(15·19·21 / 합격선 23) |
| 2026-08-16 | **하네스 고도화 v4** — v3의 mirror 절차가 어느 스킬에도 문서화되지 않아 매 회차 재발명되던 문제를 해결. 신규 스킬 3(`reference-analysis`·`fidelity-scoring`·`craft-scoring`) + 신규 에이전트 4(reference-analyst·reference-pack-curator·fidelity-qa·craft-qa) + 기존 8스킬·7에이전트 개정 + 결정적 검사 스크립트 `scripts/validate_pack.py`. 스키마 v3(reference_mode 4종·필드 정본화·밀도 기준·status 생성 규칙). 모델 티어 분화(전원 opus → fable 2 / opus 1 / sonnet 8). Codex `gpt-5.6-sol`(effort ultra) 이종 교차검증 도입 | skills, agents, scripts | 사용자 요청 — "더 정확하고 더 세련되고 더 원문과 닮게" |
