self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("workout-tracker-v1").then((cache) => {
      return cache.addAll([
        "/",
        "/add",
        "/static/style.css",
        "/static/icon-192.png",
        "/static/icon-512.png",
        "/manifest.json"
      ]);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
