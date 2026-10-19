// Renders the live Vega charts for <figure class="jelly-chart"> fragments.
// Without JS the static SVG in each figure stays visible.
(function () {
  const CDN = ["https://cdn.jsdelivr.net/npm/vega@6.2.0", "https://cdn.jsdelivr.net/npm/vega-lite@6.4.1", "https://cdn.jsdelivr.net/npm/vega-embed@7.0.2"];
  const DARK_SWAP = {"#009485": "#2fc2b2", "#80868f": "#9ba1aa", "#b4b9c0": "#5d636c", "#1f2328": "#e3e6ea", "#5c636e": "#a6adb7", "#e4e7eb": "#343944", "#9aa1ab": "#5f6672", "#c2504a": "#e0716b", "#f2f5f5": "#262a33", "#7fc4bc": "#2a7d74", "#00453e": "#6fe3d4", "#ffffff": "#10141a", "#fffffe": "#1e2029"};
  let loading = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = () => reject(new Error("could not load " + src));
      document.head.appendChild(s);
    });
  }

  function loadVega() {
    if (window.vegaEmbed) return Promise.resolve();
    if (!loading) loading = CDN.reduce((p, src) => p.then(() => loadScript(src)), Promise.resolve());
    return loading;
  }

  // MkDocs Material sets data-md-color-scheme on <body>; otherwise follow the OS setting.
  function isDark() {
    const scheme = document.body.getAttribute("data-md-color-scheme");
    if (scheme) return scheme === "slate";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  // The panels sit side by side (Jena | RDF4J). When the page is narrower than that, put every
  // panel under the previous one instead. The static SVG has the side-by-side width.
  function shouldStack(fig) {
    const svg = fig.querySelector(".jc-static svg");
    const wide = svg ? parseFloat(svg.getAttribute("width")) : 0;
    return wide > fig.clientWidth + 1;
  }

  function stackPanels(spec) {
    if (spec.vconcat && spec.vconcat.every((row) => row.hconcat)) {
      spec.vconcat = spec.vconcat.flatMap((row) => row.hconcat);
    } else if (spec.hconcat) {
      spec.vconcat = spec.hconcat;
      delete spec.hconcat;
    }
    // a panel that left its labels to its left-hand neighbour needs them back when on its own;
    // the heatmap's long dataset names get a little less room (only axes in the panels, not config)
    (function walk(o) {
      if (!o || typeof o !== "object") return;
      if (o.axis && o.axis.labels === false) o.axis.labels = true;
      if (o.axis && o.axis.labelLimit === 118) o.axis.labelLimit = 100;
      for (const k in o) if (k !== "config") walk(o[k]);
    })(spec);
    return spec;
  }

  function buildSpec(fig, dark, stack) {
    const spec0 = window.jellyCharts && window.jellyCharts[fig.id];
    if (!spec0) throw new Error("no chart spec for " + fig.id);
    let text = JSON.stringify(spec0);
    if (dark) for (const [light, dk] of Object.entries(DARK_SWAP)) text = text.split(light).join(dk);
    const spec = JSON.parse(text);
    return stack ? stackPanels(spec) : spec;
  }

  async function draw(fig, token) {
    const dark = isDark();
    const stack = shouldStack(fig);
    const live = fig.querySelector(".jc-live");
    try {
      await loadVega();
      if (token !== fig._jcToken) return; // a newer render was asked for in the meantime
      if (fig._jcView) fig._jcView.finalize();
      fig._jcView = null;
      const result = await window.vegaEmbed(live, buildSpec(fig, dark, stack), {
        renderer: "svg",
        // no "..." menu: MkDocs Material styles its <details> as a box that overflows the chart
        actions: false,
        tooltip: { theme: dark ? "dark" : "light" },
      });
      fig._jcView = result.view;
      fig._jcDark = dark;
      fig._jcStack = stack;
      fig.classList.add("jc-ready");
    } catch (e) {
      console.warn("jelly-charts:", e);
    }
  }

  // Renders of one figure run one after another, and only the latest one asked for is drawn.
  // Two at once (e.g. the first render still waiting for Vega to download when the page sets
  // its color scheme) would both write into the same element and leave a dead chart behind.
  function render(fig) {
    const token = (fig._jcToken = (fig._jcToken || 0) + 1);
    fig._jcQueue = (fig._jcQueue || Promise.resolve()).then(() => draw(fig, token));
  }

  function renderAll(onlyIfChanged) {
    const dark = isDark();
    document.querySelectorAll("figure.jelly-chart").forEach((fig) => {
      if (onlyIfChanged && fig._jcDark === dark && fig._jcStack === shouldStack(fig)) return;
      render(fig);
    });
  }

  function init() {
    // Vega's tooltip <div> hangs off <body>, so it outlives instant navigation, while its <style>
    // in <head> does not; on the next page it would show up unstyled at the bottom. Drop it here,
    // the next chart makes a new one.
    document.getElementById("vg-tooltip-element")?.remove();
    renderAll(false);
  }

  new MutationObserver(() => renderAll(true)).observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"],
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => renderAll(true));
  let resizeTimer = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => renderAll(true), 200);
  });

  // MkDocs Material's instant navigation swaps pages without a reload
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
