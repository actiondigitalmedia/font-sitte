const PAGE_SIZE = 48;
const PREVIEW_CONCURRENCY = 12;
const CATALOG_URL = "./catalog-lite.json";
const FAVORITES_KEY = "font-site-favorites";
const ALPHABET_SAMPLE = "Aa Bb Cc · 0123456789";
const PAIRING_TARGETS = {
  "sans-serif": ["serif", "display"],
  serif: ["sans-serif"],
  display: ["sans-serif", "serif"],
  monospace: ["sans-serif"],
  handwriting: ["sans-serif", "serif"],
  script: ["sans-serif"],
};

const state = {
  fonts: [],
  filtered: [],
  rendered: 0,
  loadedFaces: new Set(),
  loadingFaces: new Set(),
};

const els = {
  stats: document.getElementById("stats"),
  search: document.getElementById("search"),
  category: document.getElementById("category"),
  categoryNav: document.getElementById("category-nav"),
  source: document.getElementById("source"),
  style: document.getElementById("style"),
  featured: document.getElementById("featured"),
  variable: document.getElementById("variable"),
  favoritesOnly: document.getElementById("favorites-only"),
  sort: document.getElementById("sort"),
  reset: document.getElementById("reset"),
  resultCount: document.getElementById("result-count"),
  grid: document.getElementById("grid"),
  sentinel: document.getElementById("sentinel"),
  detail: document.getElementById("detail"),
  detailBody: document.getElementById("detail-body"),
  status: document.getElementById("status"),
};

function setStatus(message, type = "loading") {
  if (!els.status) return;
  els.status.hidden = false;
  els.status.className = `status ${type}`;
  els.status.textContent = message;
}

function clearStatus() {
  if (!els.status) return;
  els.status.hidden = true;
  els.status.textContent = "";
}

function previewFamilyId(font) {
  return `ff-${font.id}`;
}

function proxiedFontUrl(url) {
  return `/proxy-font?url=${encodeURIComponent(url)}`;
}

function resolveFontUrl(url) {
  const local = location.hostname === "localhost" || location.hostname === "127.0.0.1";
  return local ? proxiedFontUrl(url) : url;
}

function getFavorites() {
  try {
    return new Set(JSON.parse(localStorage.getItem(FAVORITES_KEY) || "[]"));
  } catch {
    return new Set();
  }
}

function toggleFavorite(id, event) {
  event?.stopPropagation();
  const favs = getFavorites();
  if (favs.has(id)) favs.delete(id);
  else favs.add(id);
  localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favs]));
  return favs.has(id);
}

function similarFonts(font, limit = 6) {
  return state.fonts.filter((f) => f.id !== font.id && f.category === font.category).slice(0, limit);
}

function suggestPairings(font, limit = 3) {
  const targets = PAIRING_TARGETS[font.category] || ["sans-serif"];
  return state.fonts
    .filter((f) => f.id !== font.id && targets.includes(f.category) && (f.featured || f.preview_woff2))
    .slice(0, limit);
}

function chipLinks(fonts) {
  return fonts.map((f) => `<a class="chip" href="/fonts/${f.id}/">${f.family_name}</a>`).join("");
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/"/g, "&quot;");
}

async function loadPreviewFont(font) {
  const family = previewFamilyId(font);
  if (state.loadedFaces.has(font.id)) return family;
  if (state.loadingFaces.has(font.id)) {
    await new Promise((r) => setTimeout(r, 80));
    return state.loadedFaces.has(font.id) ? family : null;
  }

  const woff2 = font.preview_woff2;
  if (!woff2) return null;

  state.loadingFaces.add(font.id);
  try {
    const src = resolveFontUrl(woff2);
    const weight = font.variants?.[0]?.weight || 400;
    const style = font.variants?.[0]?.style || "normal";
    const face = new FontFace(family, `url('${src}') format('woff2')`, {
      weight: String(weight),
      style,
      display: "swap",
    });
    await face.load();
    document.fonts.add(face);
    state.loadedFaces.add(font.id);
    return family;
  } catch (error) {
    console.warn(`Preview failed for ${font.family_name}:`, error);
    return null;
  } finally {
    state.loadingFaces.delete(font.id);
  }
}

function applyFontToCard(card, family) {
  if (!card || !family) return;
  card.classList.add("font-loaded");
  card.classList.remove("font-pending");
  for (const el of card.querySelectorAll("[data-font-sample]")) {
    el.style.fontFamily = `'${family}', Georgia, serif`;
  }
}

async function hydratePreviews(fonts) {
  const queue = fonts.filter((f) => f.preview_woff2);
  let index = 0;

  async function worker() {
    while (index < queue.length) {
      const i = index++;
      const font = queue[i];
      const family = await loadPreviewFont(font);
      const card = els.grid.querySelector(`.font-card[data-id="${font.id}"]`);
      if (family && card) applyFontToCard(card, family);
      else if (card) card.classList.add("font-no-preview");
    }
  }

  const workers = Array.from({ length: Math.min(PREVIEW_CONCURRENCY, queue.length || 1) }, () => worker());
  await Promise.all(workers);
}

function fillSelect(select, values) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value.replace(/-/g, " ");
    select.appendChild(option);
  }
}

function styleTagLabel(tagId) {
  return state.styleLabels?.[tagId] || tagId.replace(/-/g, " ");
}

function renderStats(info) {
  const previewNote = info.preview_enriched
    ? `<span class="stat"><strong>${info.preview_enriched.toLocaleString()}</strong> live previews</span>`
    : "";
  els.stats.innerHTML = `
    <span class="stat"><strong>${info.total_families.toLocaleString()}</strong> fonts</span>
    ${previewNote}
  `;
}

function syncCategoryPills() {
  const current = els.category.value;
  for (const pill of els.categoryNav.querySelectorAll(".cat-pill")) {
    pill.classList.toggle("active", pill.dataset.category === current);
  }
}

function buildCategoryNav(categories) {
  const sorted = ["", ...categories.sort()];
  const existing = new Set(
    [...els.categoryNav.querySelectorAll(".cat-pill")].map((p) => p.dataset.category)
  );
  for (const cat of sorted) {
    if (existing.has(cat)) continue;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `cat-pill${cat === "" ? " active" : ""}`;
    btn.dataset.category = cat;
    btn.textContent = cat ? cat.replace(/-/g, " ") : "All";
    btn.addEventListener("click", () => {
      els.category.value = cat;
      syncCategoryPills();
      applyFilters();
    });
    els.categoryNav.appendChild(btn);
    existing.add(cat);
  }
}

function applyFilters() {
  const q = els.search.value.trim().toLowerCase();
  const category = els.category.value;
  const source = els.source.value;
  const styleTag = els.style?.value;
  const featuredOnly = els.featured.checked;
  const variableOnly = els.variable.checked;
  const favoritesOnly = els.favoritesOnly?.checked;
  const favs = getFavorites();

  state.filtered = state.fonts.filter((font) => {
    if (category && font.category !== category) return false;
    if (source && font.source !== source) return false;
    if (styleTag && !(font.style_tags || []).includes(styleTag)) return false;
    if (featuredOnly && !font.featured) return false;
    if (variableOnly && !font.variable) return false;
    if (favoritesOnly && !favs.has(font.id)) return false;
    if (!q) return true;

    const haystack = [
      font.family_name,
      font.category,
      font.source,
      font.license_type,
      ...(font.designers || []),
      ...(font.tags || []),
      ...(font.style_tags || []),
      ...(font.featured_lists || []),
    ]
      .join(" ")
      .toLowerCase();

    return haystack.includes(q);
  });

  const sortBy = els.sort.value;
  state.filtered.sort((a, b) => {
    if (sortBy === "featured") {
      return Number(b.featured) - Number(a.featured) || a.family_name.localeCompare(b.family_name);
    }
    if (sortBy === "category") {
      return a.category.localeCompare(b.category) || a.family_name.localeCompare(b.family_name);
    }
    return a.family_name.localeCompare(b.family_name);
  });

  syncCategoryPills();
  state.rendered = 0;
  els.grid.innerHTML = "";
  els.resultCount.textContent = `${state.filtered.length.toLocaleString()} fonts ready to preview`;
  renderMore();
}

function cardHtml(font) {
  const favs = getFavorites();
  const isFav = favs.has(font.id);
  const name = escapeHtml(font.family_name);
  const pangram = escapeHtml(font.preview_text || "The quick brown fox jumps over the lazy dog");
  const styleCount = font.variant_count || font.variants?.length || 0;
  const hasPreview = Boolean(font.preview_woff2);
  const download = font.download_url
    ? `<a class="btn-download" href="${escapeHtml(font.download_url)}" target="_blank" rel="noopener" onclick="event.stopPropagation()">Download</a>`
    : font.source_url
      ? `<a class="btn-download" href="${escapeHtml(font.source_url)}" target="_blank" rel="noopener" onclick="event.stopPropagation()">Get font</a>`
      : "";

  return `
    <article class="font-card font-row ${hasPreview ? "font-pending" : "font-no-preview"}" data-id="${font.id}">
      <a href="/fonts/${font.id}/" class="font-card__preview-link" onclick="event.stopPropagation()">
        <div class="font-card__preview-pane">
          <p class="font-card__title-sample" data-font-sample title="${name}">${name}</p>
          <div class="font-card__samples">
            <p class="font-card__alphabet" data-font-sample>${ALPHABET_SAMPLE}</p>
            <p class="font-card__pangram" data-font-sample>${pangram}</p>
          </div>
          ${hasPreview ? "" : '<span class="font-card__no-face">Preview on download</span>'}
        </div>
      </a>
      <div class="font-card__footer">
        <div class="font-card__meta">
          <h2 class="font-card__name"><a href="/fonts/${font.id}/">${name}</a></h2>
          <p class="font-card__sub">${escapeHtml(font.license_type)} · ${styleCount} styles · ${escapeHtml(font.category)}</p>
        </div>
        <div class="font-card__actions">
          <button type="button" class="fav-btn ${isFav ? "active" : ""}" data-fav="${font.id}" aria-label="Favorite">${isFav ? "★" : "☆"}</button>
          ${download}
        </div>
      </div>
    </article>
  `;
}

function insertInFeedAd(container) {
  const ad = document.createElement("div");
  ad.className = "ad-slot ad-infeed";
  ad.dataset.adSlot = "in-feed-native";
  container.appendChild(ad);
  if (window.initAds) window.initAds();
}

async function renderMore() {
  const slice = state.filtered.slice(state.rendered, state.rendered + PAGE_SIZE);
  if (!slice.length) return;

  const fragment = document.createDocumentFragment();
  for (const font of slice) {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = cardHtml(font);
    const card = wrapper.firstElementChild;

    card.querySelector(".fav-btn")?.addEventListener("click", (e) => {
      const active = toggleFavorite(font.id, e);
      e.currentTarget.classList.toggle("active", active);
      e.currentTarget.textContent = active ? "★" : "☆";
    });
    card.addEventListener("click", (e) => {
      if (e.target.closest("a, button")) return;
      openDetail(font);
    });
    fragment.appendChild(card);

    if ((state.rendered + fragment.childElementCount) % 8 === 0) {
      insertInFeedAd(fragment);
    }
  }

  els.grid.appendChild(fragment);
  state.rendered += slice.length;
  await hydratePreviews(slice);
  observeSentinel();
}

function observeSentinel() {
  /* handled by global io in wireEvents */
}

async function openDetail(font) {
  const family = await loadPreviewFont(font);
  const previewFamily = family ? `'${family}', var(--font-ui)` : "var(--font-ui)";
  const isFav = getFavorites().has(font.id);

  const links = [
    `<a href="/fonts/${font.id}/">Specimen page</a>`,
    font.source_url ? `<a href="${font.source_url}" target="_blank" rel="noopener">Source</a>` : "",
    font.download_url ? `<a href="${font.download_url}" target="_blank" rel="noopener">Download</a>` : "",
    font.github_url ? `<a href="${font.github_url}" target="_blank" rel="noopener">GitHub</a>` : "",
    font.license_url ? `<a href="${font.license_url}" target="_blank" rel="noopener">License</a>` : "",
  ]
    .filter(Boolean)
    .join("");

  const styleCount = font.variant_count || font.variants?.length || 0;
  const similar = similarFonts(font);
  const pairings = suggestPairings(font);
  const styleBadges = (font.style_tags || [])
    .map((t) => `<span class="badge style">${styleTagLabel(t)}</span>`)
    .join(" ");

  els.detailBody.innerHTML = `
    <h2>${escapeHtml(font.family_name)} <button type="button" class="fav-btn ${isFav ? "active" : ""}" id="detail-fav">${isFav ? "★" : "☆"}</button></h2>
    ${styleBadges ? `<div class="badges">${styleBadges}</div>` : ""}
    <div class="detail-preview-pane">
      <p class="detail-preview" style="font-family:${previewFamily}">${escapeHtml(font.family_name)}</p>
      <p class="detail-preview-sub" style="font-family:${previewFamily}">${ALPHABET_SAMPLE}</p>
      <p class="detail-preview-sub" style="font-family:${previewFamily}">${escapeHtml(font.preview_text || "The quick brown fox jumps over the lazy dog 0123456789")}</p>
    </div>
    <dl class="detail-grid">
      <div><dt>Category</dt><dd>${escapeHtml(font.category)}</dd></div>
      <div><dt>Source</dt><dd>${escapeHtml(font.source)}</dd></div>
      <div><dt>License</dt><dd>${escapeHtml(font.license_type)}</dd></div>
      <div><dt>Styles</dt><dd>${styleCount}</dd></div>
    </dl>
    <div class="links">${links}</div>
    ${similar.length ? `<section><h3>Similar</h3><div class="chips">${chipLinks(similar)}</div></section>` : ""}
    ${pairings.length ? `<section><h3>Pairing picks</h3><div class="chips">${chipLinks(pairings)}</div></section>` : ""}
  `;

  document.getElementById("detail-fav")?.addEventListener("click", (e) => {
    const active = toggleFavorite(font.id, e);
    e.currentTarget.classList.toggle("active", active);
    e.currentTarget.textContent = active ? "★" : "☆";
  });

  els.detail.showModal();
}

function wireEvents() {
  for (const el of [els.search, els.category, els.source, els.style, els.featured, els.variable, els.favoritesOnly, els.sort]) {
    if (el) {
      el.addEventListener("input", applyFilters);
      el.addEventListener("change", () => {
        syncCategoryPills();
        applyFilters();
      });
    }
  }

  els.reset.addEventListener("click", () => {
    els.search.value = "";
    els.category.value = "";
    els.source.value = "";
    if (els.style) els.style.value = "";
    els.featured.checked = false;
    els.variable.checked = false;
    if (els.favoritesOnly) els.favoritesOnly.checked = false;
    els.sort.value = "name";
    syncCategoryPills();
    applyFilters();
  });

  const io = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) renderMore();
    },
    { rootMargin: "600px" }
  );
  io.observe(els.sentinel);
}

async function init() {
  wireEvents();

  if (window.location.protocol === "file:") {
    setStatus("Open via server: http://localhost:8080/", "error");
    els.resultCount.textContent = "Server required";
    return;
  }

  setStatus("Loading font catalog…");

  try {
    const response = await fetch(CATALOG_URL);
    if (!response.ok) throw new Error(`Catalog fetch failed (${response.status})`);

    const catalog = await response.json();
    state.fonts = catalog.fonts;
    state.styleLabels = catalog.catalog_info?.style_tag_labels || {};
    renderStats(catalog.catalog_info);

    const categories = [...new Set(state.fonts.map((f) => f.category))].sort();
    fillSelect(els.category, categories);
    buildCategoryNav(categories);
    fillSelect(els.source, [...new Set(state.fonts.map((f) => f.source))].sort());
    if (els.style) {
      const tagIds = [...new Set(state.fonts.flatMap((f) => f.style_tags || []))].sort();
      for (const id of tagIds) {
        const option = document.createElement("option");
        option.value = id;
        option.textContent = state.styleLabels[id] || styleTagLabel(id);
        els.style.appendChild(option);
      }
    }

    clearStatus();
    applyFilters();
  } catch (error) {
    setStatus(`Failed to load catalog: ${error.message}`, "error");
    els.resultCount.textContent = "Catalog unavailable";
    console.error(error);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
