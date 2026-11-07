/**
 * Ad configuration — replace ADSENSE_CLIENT with your publisher ID before going live.
 * Slots are non-blocking placeholders until AdSense is approved.
 */
window.FONT_SITE_ADS = {
  enabled: false, // set true after AdSense approval
  adsenseClient: "ca-pub-XXXXXXXXXXXXXXXX",
  slots: {
    "header-leaderboard": "",
    "sidebar-sticky": "",
    "in-feed-native": "",
    "footer-banner": "",
    "specimen-top": "",
  },
};

function initAds() {
  if (!window.FONT_SITE_ADS.enabled) {
    document.querySelectorAll(".ad-slot").forEach((el) => {
      if (!el.dataset.placeholder) {
        el.dataset.placeholder = "true";
        el.innerHTML = '<span class="ad-placeholder">Ad space</span>';
      }
    });
    return;
  }

  const client = window.FONT_SITE_ADS.adsenseClient;
  if (!document.querySelector('script[src*="pagead2.googlesyndication.com"]')) {
    const s = document.createElement("script");
    s.async = true;
    s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${client}`;
    s.crossOrigin = "anonymous";
    document.head.appendChild(s);
  }

  document.querySelectorAll(".ad-slot[data-ad-slot]").forEach((el) => {
    const slotId = window.FONT_SITE_ADS.slots[el.dataset.adSlot];
    if (!slotId) return;
    el.innerHTML = `<ins class="adsbygoogle" style="display:block" data-ad-client="${client}" data-ad-slot="${slotId}"></ins>`;
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  });
}

function maybeShowCookieBanner() {
  if (localStorage.getItem("font-site-cookie-ok")) return;
  const bar = document.createElement("div");
  bar.className = "cookie-bar";
  bar.innerHTML = 'We use cookies for analytics and ads. <button id="cookie-accept">Accept</button> <a href="/privacy.html">Privacy</a>';
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
