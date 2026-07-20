/**
 * Ad configuration — replace ADSENSE_CLIENT / slot IDs after AdSense approval.
 * In-feed ads are native card-sized tiles in the font grid (same cell size).
 */
window.FONT_SITE_ADS = {
  enabled: false, // set true after AdSense approval
  adsenseClient: "ca-pub-XXXXXXXXXXXXXXXX",
  slots: {
    "in-feed-native": "", // native / in-article style unit, card-sized
    "footer-banner": "",
  },
};

function initAds() {
  const adsOn = Boolean(window.FONT_SITE_ADS?.enabled);
  const client = window.FONT_SITE_ADS.adsenseClient;

  document.querySelectorAll(".ad-slot, .ad-native-body").forEach((el) => {
    if (el.hasAttribute("hidden")) return;
    const slotKey = el.dataset.adSlot;
    const slotId = slotKey ? window.FONT_SITE_ADS.slots[slotKey] : "";

    if (!adsOn || !slotId) {
      // Keep native card placeholders visible in-grid; hide reserved footer until live
      if (el.classList.contains("ad-footer") || el.classList.contains("ad-slot")) {
        if (!el.closest(".card-ad")) el.setAttribute("hidden", "");
      }
      if (el.classList.contains("ad-native-body") && !el.querySelector(".ad-placeholder")) {
        el.innerHTML = '<span class="ad-placeholder">Ad space</span>';
      }
      return;
    }

    if (el.dataset.filled === "true") return;
    el.dataset.filled = "true";
    el.innerHTML = `<ins class="adsbygoogle"
      style="display:block;width:100%;min-height:90px"
      data-ad-client="${client}"
      data-ad-slot="${slotId}"
      data-ad-format="fluid"
      data-ad-layout-key="-fb+5w+4e-db+86"></ins>`;
  });

  if (!adsOn) return;

  if (!document.querySelector('script[src*="pagead2.googlesyndication.com"]')) {
    const s = document.createElement("script");
    s.async = true;
    s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${client}`;
    s.crossOrigin = "anonymous";
    document.head.appendChild(s);
  }

  document.querySelectorAll(".adsbygoogle").forEach(() => {
    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (_) {
      /* ignore duplicate push during infinite scroll */
    }
  });
}

function maybeShowCookieBanner() {
  if (!window.FONT_SITE_ADS.enabled) return;
  if (localStorage.getItem("font-site-cookie-ok")) return;
  const bar = document.createElement("div");
  bar.className = "cookie-bar";
  bar.innerHTML =
    'We use cookies for analytics and ads. <button id="cookie-accept" type="button">Accept</button> <a href="privacy.html">Privacy</a>';
  document.body.appendChild(bar);
  document.getElementById("cookie-accept")?.addEventListener("click", () => {
    localStorage.setItem("font-site-cookie-ok", "1");
    bar.remove();
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    initAds();
    maybeShowCookieBanner();
  });
} else {
  initAds();
  maybeShowCookieBanner();
}

window.initAds = initAds;
