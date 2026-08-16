#!/usr/bin/env python3
"""디자인 팩 결정적 검사 (design-pack-schema v3 / craft-scoring A군).

모델이 아니라 스크립트가 판정하는 항목만 담는다. 시각 판단은 하지 않는다.

    python3 scripts/validate_pack.py                 # 전 팩
    python3 scripts/validate_pack.py ppt-motie-...   # 특정 팩
    python3 scripts/validate_pack.py --v3-only       # reference_mode 있는 팩만
    python3 scripts/validate_pack.py --json          # 기계 판독 출력

종료 코드: 0 = hard fail 0건, 1 = hard fail 있음.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml 필요: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "design-packs"

# --- 지시 밀도 기준 (design-pack-schema v3) ---
ATOM_MIN_GENERAL = 14
ATOM_MIN_CHART = 18
NUMERIC_RATIO_MIN = 0.60

DIM = re.compile(r"\b\d+(?:\.\d+)?\s*(?:pt|px|in|%|em|rem|deg|ms)\b")
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
# "N pt 이하 ... 금지" 형태의 하한 선언
MIN_SIZE_BAN = re.compile(r"(\d+)\s*pt\s*이하[^\n]{0,40}(?:금지|안\s*됨|불가)")


def png_size(path: Path):
    """의존성 없이 PNG IHDR에서 크기를 읽는다."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def sha256_of(path: Path) -> str:
    import hashlib
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def count_atoms(text: str):
    """constraint atom 근사 = 검증 가능한 값을 낀 지시 줄."""
    atoms = numeric = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        has_num = bool(DIM.search(s) or HEX.search(s))
        # 지시로 볼 수 있는 줄: 불릿/번호 항목이거나 콜론 서술
        is_instruction = s.startswith(("-", "*", "•")) or re.match(r"^\d+[.)]", s) or "：" in s or ":" in s
        if is_instruction:
            atoms += 1
            if has_num:
                numeric += 1
    return atoms, numeric


def validate(slug: str) -> dict:
    d = PACKS / slug
    hard: list[str] = []
    warn: list[str] = []
    info: dict = {"slug": slug}

    prompt_p, tokens_p, meta_p = d / "prompt.md", d / "tokens.json", d / "meta.yaml"
    for p in (prompt_p, tokens_p, meta_p):
        if not p.exists():
            hard.append(f"필수 파일 없음: {p.name}")
    if hard:
        return {**info, "hard_fails": hard, "warnings": warn}

    prompt = prompt_p.read_text(encoding="utf-8")
    tokens = json.loads(tokens_p.read_text(encoding="utf-8"))
    meta = yaml.safe_load(meta_p.read_text(encoding="utf-8"))

    ref_mode = meta.get("reference_mode")
    info["reference_mode"] = ref_mode or "(미분류)"
    info["category"] = meta.get("category", "standard")

    # ── 1. spec_version 3자 동기화 ──────────────────────────────
    versions = {
        "prompt.md": (re.search(r"spec_version[:\s]+([\w.\-가-힣]+)", prompt) or [None, None])[1],
        "tokens.json": tokens.get("spec_version"),
        "meta.yaml": meta.get("spec_version"),
    }
    present = {k: v for k, v in versions.items() if v}
    if len(set(present.values())) > 1:
        hard.append(f"spec_version 불일치: {present}")
    elif not present:
        warn.append("spec_version 없음 (v3 필수)")
    info["spec_version"] = present

    # ── 2. reference_mode 계약 ─────────────────────────────────
    if ref_mode == "style_synthesis" and meta.get("source_depth") == "full":
        hard.append("style_synthesis 팩은 source_depth: full 불가 (2차 자료 기반)")
    if ref_mode == "exact_document":
        ref = meta.get("reference") or {}
        for k in ("canonical_url", "sha256", "page_count", "aspect_ratio"):
            if not ref.get(k):
                hard.append(f"exact_document인데 reference.{k} 누락")
        pmp = meta.get("page_mirror_plan") or {}
        if not pmp.get("map"):
            hard.append("exact_document인데 page_mirror_plan.map 누락")
        elif pmp.get("compression") == "merged" and re.search(r"1\s*:\s*1\s*mirror", prompt, re.I):
            hard.append("compression: merged인데 prompt가 '1:1 mirror'를 주장")
        for m in meta.get("signature_motifs") or []:
            if not m.get("evidence_pages"):
                hard.append(f"시그니처 '{m.get('name')}'에 evidence_pages 없음 (관찰 근거 부재)")

    # ── 3. 캔버스 계약 + 페이지 규격 ────────────────────────────
    pages_dir = d / "pages"
    if pages_dir.exists():
        sizes = {}
        for f in sorted(pages_dir.glob("*.png")):
            s = png_size(f)
            if s:
                sizes[f.name] = s
        info["page_count"] = len(sizes)
        # PPT는 고정 캔버스라 전 페이지가 같은 크기여야 한다.
        # 웹은 풀페이지 스크린샷이라 높이가 가변 — 폭만 통일되면 된다.
        track = meta.get("track")
        if track == "ppt":
            uniq = set(sizes.values())
            if len(uniq) > 1:
                hard.append(f"페이지 픽셀 크기 불균일: {len(uniq)}종 {sorted(uniq)}")
        else:
            widths = {w for w, _ in sizes.values()}
            if len(widths) > 1:
                hard.append(f"웹 렌더 폭 불균일: {sorted(widths)} (뷰포트 폭은 고정돼야 함)")

        if sizes:
            from collections import Counter
            (w, h), _ = Counter(sizes.values()).most_common(1)[0]  # 최빈 크기 기준
            ratio = w / h
            info["render_ratio"] = round(ratio, 4)
            if track == "ppt" and abs(ratio - 16 / 9) / (16 / 9) > 0.005:
                hard.append(f"PPT 렌더 종횡비 {ratio:.3f} — 16:9 오차 0.5% 초과")

        # meta.pages 와 실제 파일 정합
        declared = [p.get("id") for p in (meta.get("pages") or [])]
        if declared:
            actual = [re.sub(r"^\d+-", "", f).removesuffix(".png") for f in sorted(sizes)]
            if declared != actual:
                hard.append(f"pages 정합 실패: meta={declared} / 파일={actual}")

    # 선언된 캔버스 문자열 안의 자기모순 (16:9라면서 다른 비율 병기).
    # 스택 렌더 높이 등 오탐을 막기 위해 캔버스를 언급한 줄로 한정한다.
    for line in prompt.splitlines():
        if "16:9" not in line or not re.search(r"캔버스|canvas|슬라이드 크기|해상도", line, re.I):
            continue
        for m in re.finditer(r"(\d{3,4})\s*[x×]\s*(\d{3,4})", line):
            w, h = int(m.group(1)), int(m.group(2))
            if h and abs(w / h - 16 / 9) / (16 / 9) > 0.02:
                hard.append(f"캔버스 계약 모순: '16:9'와 {w}×{h}(={w/h:.3f}) 병기")
                break
        else:
            continue
        break

    # ── 4. 자기모순 지시 ───────────────────────────────────────
    for m in MIN_SIZE_BAN.finditer(prompt):
        floor = int(m.group(1))
        smaller = {int(x) for x in re.findall(r"(\d+)\s*pt", prompt) if int(x) < floor}
        # 본문/카드 텍스트 맥락에서 하한보다 작은 값을 지정했는지
        body_small = [
            int(g) for g in re.findall(r"(?:본문|카드 본문|body)[^\n]{0,60}?(\d+)\s*pt", prompt)
            if int(g) < floor
        ]
        if body_small:
            hard.append(f"자기모순: 본문을 {body_small}pt로 지정하고 '{floor}pt 이하 금지'를 동시 기재")
        elif smaller:
            warn.append(f"'{floor}pt 이하 금지'인데 더 작은 pt 값 {sorted(smaller)[:5]} 존재 (역할 구분 확인 필요)")

    # ── 5. 지시 밀도 ───────────────────────────────────────────
    atoms, numeric = count_atoms(prompt)
    pg = info.get("page_count") or len(meta.get("pages") or []) or 1
    per_page = atoms / pg
    ratio_num = numeric / atoms if atoms else 0
    info["atoms"] = atoms
    info["atoms_per_page"] = round(per_page, 1)
    info["numeric_ratio"] = round(ratio_num, 2)
    if meta.get("category") == "premium":
        if per_page < ATOM_MIN_GENERAL:
            warn.append(f"지시 밀도 낮음: 페이지당 atom {per_page:.1f} < {ATOM_MIN_GENERAL}")
        if ratio_num < NUMERIC_RATIO_MIN:
            warn.append(f"검증 가능 비율 {ratio_num:.0%} < {NUMERIC_RATIO_MIN:.0%}")

    # ── 6. 렌더 신선도 ─────────────────────────────────────────
    manifest = d / "render-manifest.json"
    if manifest.exists():
        mf = json.loads(manifest.read_text(encoding="utf-8"))
        for name, p in (("prompt.md", prompt_p), ("tokens.json", tokens_p)):
            rec = (mf.get("source_hash") or {}).get(name)
            if rec and rec != sha256_of(p):
                hard.append(f"stale render: {name} 해시가 매니페스트와 다름")
        info["render_manifest"] = "present"
    else:
        info["render_manifest"] = "missing"
        if meta.get("category") == "premium":
            warn.append("render-manifest.json 없음 — 렌더 신선도 검증 불가")

    # ── 7. 렌더 증거 (premium은 상세 페이지가 있어야 한다) ──────
    declared_pages = meta.get("pages") or []
    rendered = info.get("page_count", 0)
    if meta.get("category") == "premium":
        if rendered == 0:
            (hard if meta.get("status") == "pass" else warn).append(
                "premium인데 렌더된 상세 페이지 0장 — 렌더 증거 없음")
        elif declared_pages and rendered != len(declared_pages):
            hard.append(f"선언 페이지 {len(declared_pages)}장 ≠ 렌더 {rendered}장")

    # ── 8. status 정합 + publishable 산출 ──────────────────────
    # 필요한 게이트는 reference_mode에 따라 다르다 (design-pack-schema 상태식이 SSOT).
    qa = meta.get("qa") or {}
    fidelity_required = ref_mode in ("exact_document", "official_system", "historical_canon")
    need = ["craft", "diversity"] + (["fidelity"] if fidelity_required else [])
    gates = {k: (qa.get(k) or {}).get("verdict") for k in need}
    missing = [g for g in need if gates.get(g) != "pass"]
    info["gates"] = gates

    if meta.get("status") == "pass" and missing:
        warn.append(f"status: pass인데 게이트 근거 없음/미통과: {missing}")

    info["publishable"] = bool(
        not hard
        and not missing
        and meta.get("status") == "pass"
        and info.get("render_manifest") == "present"
        and (meta.get("category") != "premium" or rendered > 0)
    )

    return {**info, "hard_fails": hard, "warnings": warn}


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    slugs = args or sorted(p.name for p in PACKS.iterdir() if p.is_dir())

    results = []
    for slug in slugs:
        r = validate(slug)
        if "--v3-only" in flags and r.get("reference_mode") == "(미분류)":
            continue
        results.append(r)

    if "--json" in flags:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        failed = [r for r in results if r["hard_fails"]]
        warned = [r for r in results if r["warnings"] and not r["hard_fails"]]
        for r in failed:
            print(f"\n✗ {r['slug']}  [{r['reference_mode']}]")
            for h in r["hard_fails"]:
                print(f"    HARD  {h}")
            for w in r["warnings"]:
                print(f"    warn  {w}")
        for r in warned:
            print(f"\n△ {r['slug']}  [{r['reference_mode']}]")
            for w in r["warnings"]:
                print(f"    warn  {w}")
        clean = len(results) - len(failed) - len(warned)
        pub = sum(1 for r in results if r.get("publishable"))
        print(f"\n{'='*60}")
        print(f"검사 {len(results)}팩 — 통과 {clean} / 경고 {len(warned)} / HARD FAIL {len(failed)}")
        print(f"발행 가능(publishable) {pub}팩 — 나머지 {len(results)-pub}팩은 게이트 근거·렌더 증거 미비")

    if "--require-publishable" in flags:
        return 0 if all(r.get("publishable") for r in results) else 1
    return 1 if any(r["hard_fails"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
