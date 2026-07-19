/** Load font preview on static specimen pages */
(async function () {
  const el = document.getElementById("specimen-preview");
  if (!el) return;

  const fontId = el.dataset.fontId;
  const res = await fetch("/catalog-lite.json");
  const catalog = await res.json();
  const font = catalog.fonts.find((f) => f.id === fontId);
  if (!font?.preview_woff2) return;

  const useProxy = location.hostname === "localhost" || location.hostname === "127.0.0.1";
  const src = useProxy
    ? `/proxy-font?url=${encodeURIComponent(font.preview_woff2)}`
    : font.preview_woff2;
  const family = `ff-${font.id}`;

  try {
    const face = new FontFace(family, `url('${src}') format('woff2')`, { display: "swap" });
    await face.load();
    document.fonts.add(face);
    el.style.fontFamily = `'${family}', system-ui, sans-serif`;
    el.style.fontSize = "clamp(2rem, 6vw, 4rem)";
  } catch (e) {
    console.warn(e);
  }
})();
