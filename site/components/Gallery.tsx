"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import type { CatalogPack, Axes } from "@/lib/types";
import { AXIS_LABELS, TRACK_LABELS } from "@/lib/types";

const AXIS_ORDER: (keyof Axes)[] = [
  "color",
  "type",
  "layout",
  "space",
  "motion",
];

const STORAGE_KEY = "dd-gallery-state-v1";

function uniqSorted(values: (string | undefined)[]): string[] {
  return Array.from(new Set(values.filter(Boolean) as string[])).sort();
}

function saveScroll() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    const prev = raw ? JSON.parse(raw) : {};
    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ ...prev, scrollY: window.scrollY })
    );
  } catch {
    /* ignore */
  }
}

function PackCard({ p }: { p: CatalogPack }) {
  const isPremium = p.category === "premium";
  const pageCount = p.pages?.length ?? 0;
  return (
    <Link
      href={`/pack/${p.slug}/`}
      className={`card${isPremium ? " card-premium" : ""}`}
      prefetch={false}
      onClick={saveScroll}
    >
      <div className="card-thumb">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`/previews/${p.slug}.png`}
          alt={`${p.display_name} 미리보기`}
          loading="lazy"
        />
        {isPremium && <span className="premium-badge">PREMIUM</span>}
      </div>
      <div className="card-body">
        <div className="card-top">
          <span className={`badge badge-${p.track}`}>
            {TRACK_LABELS[p.track]}
          </span>
          {p.status !== "pass" && (
            <span className="badge badge-draft">{p.status}</span>
          )}
          <span className="card-title">{p.display_name}</span>
        </div>
        <p className="card-summary">{p.summary}</p>
        <div className="card-axes">
          {AXIS_ORDER.map(
            (axis) =>
              p.axes?.[axis] && (
                <span className="tag" key={axis}>
                  {p.axes[axis]}
                </span>
              )
          )}
          {isPremium && pageCount > 0 && (
            <span className="tag tag-pages">상세 {pageCount}면</span>
          )}
        </div>
      </div>
    </Link>
  );
}

export default function Gallery({ packs }: { packs: CatalogPack[] }) {
  const [track, setTrack] = useState<string>("all");
  const [premiumOnly, setPremiumOnly] = useState<boolean>(false);
  const [axisFilters, setAxisFilters] = useState<
    Partial<Record<keyof Axes, string>>
  >({});
  const [hydrated, setHydrated] = useState(false);
  const pendingScrollY = useRef<number | null>(null);

  // Restore filter state + scroll position on mount (returning from detail)
  useEffect(() => {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (raw) {
        const s = JSON.parse(raw);
        if (typeof s.track === "string") setTrack(s.track);
        if (typeof s.premiumOnly === "boolean") setPremiumOnly(s.premiumOnly);
        if (s.axisFilters && typeof s.axisFilters === "object")
          setAxisFilters(s.axisFilters);
        if (typeof s.scrollY === "number") pendingScrollY.current = s.scrollY;
      }
    } catch {
      /* ignore */
    }
    if ("scrollRestoration" in window.history) {
      window.history.scrollRestoration = "manual";
    }
    setHydrated(true);
  }, []);

  // Persist filter state on change
  useEffect(() => {
    if (!hydrated) return;
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      const prev = raw ? JSON.parse(raw) : {};
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ ...prev, track, premiumOnly, axisFilters })
      );
    } catch {
      /* ignore */
    }
  }, [hydrated, track, premiumOnly, axisFilters]);

  const axisOptions = useMemo(() => {
    const opts: Record<string, string[]> = {};
    for (const axis of AXIS_ORDER) {
      opts[axis] = uniqSorted(packs.map((p) => p.axes?.[axis]));
    }
    return opts;
  }, [packs]);

  const filtered = useMemo(() => {
    return packs.filter((p) => {
      if (track !== "all" && p.track !== track) return false;
      if (premiumOnly && p.category !== "premium") return false;
      for (const axis of AXIS_ORDER) {
        const want = axisFilters[axis];
        if (want && p.axes?.[axis] !== want) return false;
      }
      return true;
    });
  }, [packs, track, premiumOnly, axisFilters]);

  // After hydration and first filtered render, restore saved scroll position
  useEffect(() => {
    if (!hydrated) return;
    const y = pendingScrollY.current;
    if (y == null) return;
    pendingScrollY.current = null;
    // Wait two frames so the grid has laid out before scrolling
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        window.scrollTo(0, y);
        try {
          const raw = sessionStorage.getItem(STORAGE_KEY);
          if (raw) {
            const prev = JSON.parse(raw);
            delete prev.scrollY;
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(prev));
          }
        } catch {
          /* ignore */
        }
      });
    });
  }, [hydrated, filtered.length]);

  const pptPacks = filtered.filter((p) => p.track === "ppt");
  const webPacks = filtered.filter((p) => p.track === "web");

  function toggleAxis(axis: keyof Axes, value: string) {
    setAxisFilters((prev) => ({
      ...prev,
      [axis]: prev[axis] === value ? undefined : value,
    }));
  }

  const hasAxisFilter = Object.values(axisFilters).some(Boolean);
  const premiumCount = packs.filter((p) => p.category === "premium").length;

  const SEG: { id: string; label: string; sub: string }[] = [
    { id: "all", label: "전체", sub: `${packs.length}` },
    {
      id: "ppt",
      label: "프레젠테이션 · PPT",
      sub: `${packs.filter((p) => p.track === "ppt").length}`,
    },
    {
      id: "web",
      label: "웹사이트",
      sub: `${packs.filter((p) => p.track === "web").length}`,
    },
  ];

  return (
    <section className="catalog">
      <div className="wrap">
        {/* prominent PPT / Website separation */}
        <div className="seg" role="tablist" aria-label="트랙 선택">
          {SEG.map((s) => (
            <button
              key={s.id}
              role="tab"
              aria-selected={track === s.id}
              className="seg-btn"
              onClick={() => setTrack(s.id)}
            >
              {s.label}
              <span className="seg-count">{s.sub}</span>
            </button>
          ))}
        </div>

        {/* category toggle — premium */}
        <div className="cat-bar">
          <button
            className={`cat-toggle${premiumOnly ? " cat-toggle-on" : ""}`}
            aria-pressed={premiumOnly}
            onClick={() => setPremiumOnly((v) => !v)}
          >
            <span className="cat-toggle-star">★</span>
            프리미엄 팩만 보기
            <span className="cat-toggle-count">{premiumCount}</span>
          </button>
          <span className="cat-bar-note">
            프리미엄 팩은 표지·본문·차트·다이어그램 등 5~7개 상세 페이지를
            모두 명세·렌더한 심화 팩입니다.
          </span>
        </div>

        {/* axis filters */}
        <div className="filters-inline">
          {AXIS_ORDER.map((axis) => (
            <div className="filter-row" key={axis}>
              <span className="filter-label">{AXIS_LABELS[axis]}</span>
              {axisOptions[axis].map((value) => (
                <button
                  key={value}
                  className="chip"
                  aria-pressed={axisFilters[axis] === value}
                  onClick={() => toggleAxis(axis, value)}
                >
                  {value}
                </button>
              ))}
            </div>
          ))}
          {hasAxisFilter && (
            <button
              className="chip chip-reset"
              onClick={() => setAxisFilters({})}
            >
              축 필터 초기화
            </button>
          )}
        </div>

        {filtered.length === 0 && (
          <p style={{ padding: "48px 0", color: "var(--ink-faint)" }}>
            조건에 맞는 팩이 없습니다. 필터를 조정해 보세요.
          </p>
        )}

        {/* "전체" → grouped by track; specific track → single grid */}
        {track === "all" ? (
          <>
            {pptPacks.length > 0 && (
              <div className="track-group">
                <div className="track-head">
                  <span className="badge badge-ppt">프레젠테이션 · PPT</span>
                  <h2>발표자료 디자인 팩</h2>
                  <span className="track-count">{pptPacks.length}팩</span>
                </div>
                <p className="track-desc">
                  표지·본문·차트·다이어그램 양식까지 한 벌로 명세된 슬라이드 덱
                  스타일.
                </p>
                <div className="grid">
                  {pptPacks.map((p) => (
                    <PackCard p={p} key={p.slug} />
                  ))}
                </div>
              </div>
            )}
            {webPacks.length > 0 && (
              <div className="track-group">
                <div className="track-head">
                  <span className="badge badge-web">웹사이트</span>
                  <h2>웹사이트 디자인 팩</h2>
                  <span className="track-count">{webPacks.length}팩</span>
                </div>
                <p className="track-desc">
                  레이아웃·컴포넌트·타이포·모션까지 명세된 웹페이지 스타일.
                </p>
                <div className="grid">
                  {webPacks.map((p) => (
                    <PackCard p={p} key={p.slug} />
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="track-group">
            <p className="result-count">{filtered.length}개 팩</p>
            <div className="grid">
              {filtered.map((p) => (
                <PackCard p={p} key={p.slug} />
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
