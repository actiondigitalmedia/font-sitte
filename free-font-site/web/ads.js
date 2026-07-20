/**
 * Ad configuration — replace ADSENSE_CLIENT with your publisher ID before going live.
 * Header / sidebar / in-feed slots removed from UI for now (footer reserved, hidden until enabled).
 */
window.FONT_SITE_ADS = {
  enabled: false, // set true after AdSense approval
  adsenseClient: "ca-pub-XXXXXXXXXXXXXXXX",
  slots: {
    "footer-banner": "",
  },
};

function initAds() {
  // Skip hidden slots and removed placements
  document.querySelectorAll(".ad-slot").forEach((el) => {
    if (el.hasAttribute("hidden")) return;
    if (!window.FONT_SITE_ADS.enabled) {
      // Keep layout clean until ads are intentionally turned on
      el.setAttribute("hidden", "");
      return;
    }
    const slotId = window.FONT_SITE_ADS.slots[el.dataset.adSlot];
    if (!slotId) {
      el.setAttribute("hidden", "");
      return;
    }
  });

  if (!window.FONT_SITE_ADS.enabled) return;

  const client = window.FONT_SITE_ADS.adsenseClient;
  if (!document.querySelector('script[src*="pagead2.googlesyndication.com"]')) {
    const s = document.createElement("script");
    s.async = true;
    s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${client}`;
    s.crossOrigin = "anonymous";
    document.head.appendChild(s);
  }

  document.querySelectorAll(".ad-slot[data-ad-slot]:not([hidden])").forEach((el) => {
    const slotId = window.FONT_SITE_ADS.slots[el.dataset.adSlot];
    if (!slotId) return;
    el.innerHTML = `<ins class="adsbygoogle" style="display:block" data-ad-client="${client}" data-ad-slot="${slotId}"></ins>`;
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  });
}

function maybeShowCookieBanner() {
  // No cookie bar until ads/analytics are actually enabled
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
