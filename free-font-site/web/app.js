const PAGE_SIZE = 48;
const CATALOG_URL = "./catalog-lite.json";

const state = {
  fonts: [],
  filtered: [],
  rendered: 0,
  loadedFaces: new Set(),
};

const els = {
  stats: document.getElementById("stats"),
  search: document.getElementById("search"),
  category: document.getElementById("category"),
  source: document.getElementById("source"),
  featured: document.getElementById("featured"),
  variable: document.getElementById("variable"),
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
  els.status.hidden = false;
  els.status.className = `status ${type}`;
  els.status.textContent = message;
}

function clearStatus() {
  els.status.hidden = true;
  els.status.textContent = "";
}
  const family = familyName.trim().replace(/\s+/g, "+");
  return `https://fonts.googleapis.com/css2?family=${encodeURIComponent(family).replace(/%20/g, "+")}&display=swap`;
}

function ensureStylesheet(id, href) {
  if (document.getElementById(id)) return;
  const link = document.createElement("link");
  link.id = id;
  link.rel = "stylesheet";
  link.href = href;
  document.head.appendChild(link);
}

function ensureWoff2Face(font) {
  const variant = font.variants?.find((v) => v.files?.woff2) || font.variants?.[0];
  const woff2 = variant?.files?.woff2;
  if (!woff2) {
    if (font.source === "google-fonts") {
      ensureStylesheet(`gf-${font.id}`, googleCssUrl(font.family_name));
    }
    return;
  }

  const key = `${font.id}-${variant.name}`;
  if (state.loadedFaces.has(key)) return;
  state.loadedFaces.add(key);

  const style = document.createElement("style");
  style.textContent = `
    @font-face {
      font-family: '${font.family_name.replace(/'/g, "\\'")}';
      src: url('${woff2}') format('woff2');
      font-weight: ${variant.weight || 400};
      font-style: ${variant.style || "normal"};
      font-display: swap;
    }
  `;
  document.head.appendChild(style);
}

function fillSelect(select, values, labelFn = (v) => v) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labelFn(value);
    select.appendChild(option);
  }
}

function renderStats(info) {
  els.stats.innerHTML = `
    <span class="stat"><strong>${info.total_families.toLocaleString()}</strong> families</span>
    <span class="stat"><strong>${info.total_variants.toLocaleString()}</strong> variants</span>
    <span class="stat">Updated ${new Date(info.generated_at).toLocaleDateString()}</span>
  `;
}

function applyFilters() {
  const q = els.search.value.trim().toLowerCase();
  const category = els.category.value;
  const source = els.source.value;
  const featuredOnly = els.featured.checked;
  const variableOnly = els.variable.checked;

  state.filtered = state.fonts.filter((font) => {
    if (category && font.category !== category) return false;
    if (source && font.source !== source) return false;
    if (featuredOnly && !font.featured) return false;
    if (variableOnly && !font.variable) return false;
    if (!q) return true;

    const haystack = [
      font.family_name,
      font.category,
      font.source,
      font.license_type,
      ...(font.designers || []),
      ...(font.tags || []),
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

  state.rendered = 0;
  els.grid.innerHTML = "";
  els.resultCount.textContent = `${state.filtered.length.toLocaleString()} families match your filters`;
  renderMore();
}

function cardHtml(font) {
  const badges = [
    font.featured ? `<span class="badge featured">Featured</span>` : "",
    `<span class="badge">${font.category}</span>`,
    `<span class="badge">${font.source}</span>`,
    font.variable ? `<span class="badge">Variable</span>` : "",
  ].join("");

  return `
    <article class="card" data-id="${font.id}">
      <div class="card-top">
        <h2>${font.family_name}</h2>
      </div>
      <div class="badges">${badges}</div>
      <p class="preview" style="font-family:'${font.family_name.replace(/'/g, "\\'")}', var(--font-ui)">
        ${font.preview_text || "The quick brown fox jumps over the lazy dog"}
      </p>
      <p class="meta">${font.license_type} · ${font.variants?.length || 0} styles</p>
    </article>
  `;
}

function renderMore() {
  const slice = state.filtered.slice(state.rendered, state.rendered + PAGE_SIZE);
  if (!slice.length) return;

  const fragment = document.createDocumentFragment();
  for (const font of slice) {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = cardHtml(font);
    const card = wrapper.firstElementChild;
    card.addEventListener("click", () => openDetail(font));
    fragment.appendChild(card);
  }

  els.grid.appendChild(fragment);
  state.rendered += slice.length;
  observeCards();
}

function observeCards() {
  const cards = els.grid.querySelectorAll(".card:not([data-loaded])");
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const card = entry.target;
        const font = state.filtered.find((f) => f.id === card.dataset.id);
        if (font) ensureWoff2Face(font);
        card.dataset.loaded = "true";
        observer.unobserve(card);
      }
    },
    { rootMargin: "200px" }
  );

  cards.forEach((card) => observer.observe(card));
}

function openDetail(font) {
  ensureWoff2Face(font);

  const links = [
    font.source_url ? `<a href="${font.source_url}" target="_blank" rel="noopener">Source page</a>` : "",
    font.download_url ? `<a href="${font.download_url}" target="_blank" rel="noopener">Download</a>` : "",
    font.github_url ? `<a href="${font.github_url}" target="_blank" rel="noopener">GitHub</a>` : "",
    font.license_url ? `<a href="${font.license_url}" target="_blank" rel="noopener">License</a>` : "",
  ]
    .filter(Boolean)
    .join("");

  els.detailBody.innerHTML = `
    <h2>${font.family_name}</h2>
    <p class="detail-preview" style="font-family:'${font.family_name.replace(/'/g, "\\'")}', var(--font-ui)">
      ${font.preview_text || "The quick brown fox jumps over the lazy dog 0123456789"}
    </p>
    <dl class="detail-grid">
      <div><dt>Category</dt><dd>${font.category}</dd></div>
      <div><dt>Source</dt><dd>${font.source}</dd></div>
      <div><dt>License</dt><dd>${font.license_type}</dd></div>
      <div><dt>Styles</dt><dd>${font.variants?.length || 0}</dd></div>
      <div><dt>Designers</dt><dd>${(font.designers || []).join(", ") || "—"}</dd></div>
      <div><dt>Featured lists</dt><dd>${(font.featured_lists || []).join(", ") || "—"}</dd></div>
    </dl>
    <div class="links">${links}</div>
  `;

  els.detail.showModal();
}

function wireEvents() {
  for (const el of [els.search, els.category, els.source, els.featured, els.variable, els.sort]) {
    el.addEventListener("input", applyFilters);
    el.addEventListener("change", applyFilters);
  }

  els.reset.addEventListener("click", () => {
    els.search.value = "";
    els.category.value = "";
    els.source.value = "";
    els.featured.checked = false;
    els.variable.checked = false;
    els.sort.value = "name";
    applyFilters();
  });

  const io = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) renderMore();
    },
    { rootMargin: "400px" }
  );
  io.observe(els.sentinel);
}

async function init() {
  wireEvents();

  if (window.location.protocol === "file:") {
    setStatus(
      "Open this UI through the local server: http://localhost:8080/web/ (not as a file:// URL).",
      "error"
    );
    els.resultCount.textContent = "Server required";
    return;
  }

  setStatus("Loading font catalog…");

  try {
    const response = await fetch(CATALOG_URL);
    if (!response.ok) {
      throw new Error(`Catalog fetch failed (${response.status})`);
    }

    const catalog = await response.json();
    state.fonts = catalog.fonts;
    renderStats(catalog.catalog_info);

    const categories = [...new Set(state.fonts.map((f) => f.category))].sort();
    const sources = [...new Set(state.fonts.map((f) => f.source))].sort();
    fillSelect(els.category, categories);
    fillSelect(els.source, sources);

    clearStatus();
    applyFilters();
  } catch (error) {
    setStatus(
      `Failed to load catalog: ${error.message}. Make sure the server is running: python3 -m http.server 8080 --bind 0.0.0.0 --directory free-font-site`,
      "error"
    );
    els.resultCount.textContent = "Catalog unavailable";
  }
}

init();
