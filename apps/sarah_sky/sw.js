// Service worker: caches the app itself so it opens offline and installs as an app. Telescope image tiles come
// from CDS and are not cached here (they would fill school devices' storage).
const VERSION = "skymap-1.7.1";
const SHELL = ["./", "index.html", "ar.html", "css/app.css", "js/main.js", "js/content.js", "js/ar.js", "js/tarotart.js", "js/traditions.js", "js/readings.js", "js/nav.js", "js/night.js", "js/dark.js", "vendor/aladin.js", "vendor/astronomy.browser.min.js",
  "data/constellations.json", "data/stars.json", "data/messier.json", "data/aegis_flags.json", "data/aegis_coverage.json", "data/aegis_discoveries.json", "data/aegis_reviews.json",
  "icons/icon.svg", "icons/icon-192.png", "icons/icon-512.png", "manifest.webmanifest"];
self.addEventListener("install", (e) => e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", (e) => e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;           // third-party: straight to network
  if (/\/data\/aegis_[a-z]+\.json$/.test(url.pathname)) {
    e.respondWith(fetch(e.request).then((r) => { const c = r.clone(); caches.open(VERSION).then((ca) => ca.put(e.request, c)); return r; }).catch(() => caches.match(e.request)));
    return;                                                                            // survey data: network first
  }
  e.respondWith(caches.match(e.request).then((hit) => hit || fetch(e.request)));
});
