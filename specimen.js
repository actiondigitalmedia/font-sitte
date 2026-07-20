/** Load font preview on static specimen pages (base-path safe). */
(async function () {
  const el = document.getElementById("specimen-preview");
  if (!el) return;

  const fontId = el.dataset.fontId;
  const cssHref = el.dataset.previewCss;
  const woff2Direct = el.dataset.previewWoff2;

  // If build already injected a stylesheet, family name should resolve — still boost size.
  if (cssHref) {
    el.style.fontSize = "clamp(2.2rem, 7vw, 4.5rem)";
    el.style.lineHeight = "1.15";
  }

  const base = (window.__SITE_BASE__ || "").replace(/\/$/, "");
  const catalogUrl = `${base}/catalog-lite.json`;

  let font = null;
  try {
    const res = await fetch(catalogUrl);
    if (res.ok) {
      const catalog = await res.json();
      font = catalog.fonts.find((f) => f.id === fontId) || null;
    }
  } catch (e) {
    console.warn("catalog fetch failed", e);
  }

  const woff2 = woff2Direct || font?.preview_woff2;
  if (!woff2 && cssHref) return; // CSS path already handling render
  if (!woff2) return;

  const useProxy = location.hostname === "localhost" || location.hostname === "127.0.0.1";
  const src = useProxy ? `${base}/proxy-font?url=${encodeURIComponent(woff2)}` : woff2;
  const family = `ff-${fontId}`;

  try {
    const face = new FontFace(family, `url("${src}") format("woff2")`, { display: "swap" });
    await face.load();
    document.fonts.add(face);
    el.style.fontFamily = `"${family}", ${el.style.fontFamily || "system-ui, sans-serif"}`;
    el.style.fontSize = "clamp(2.2rem, 7vw, 4.5rem)";
    el.style.lineHeight = "1.15";
    el.classList.add("specimen-loaded");
  } catch (e) {
    console.warn(e);
  }
})();
