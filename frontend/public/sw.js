const STATIC_CACHE = "boaforma-static-v2"
const API_CACHE = "boaforma-api-v2"
const APP_SHELL = ["/", "/index.html", "/manifest.webmanifest", "/favicon.svg"]

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(APP_SHELL)).then(() => self.skipWaiting()),
  )
})

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && key !== API_CACHE)
          .map((key) => caches.delete(key)),
      ),
    ).then(() => self.clients.claim()),
  )
})

self.addEventListener("fetch", (event) => {
  const { request } = event
  if (request.method !== "GET") {
    return
  }

  const url = new URL(request.url)
  const isSameOrigin = url.origin === self.location.origin
  const isApiRequest = isSameOrigin && url.pathname.startsWith("/api")

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const responseClone = response.clone()
          caches.open(STATIC_CACHE).then((cache) => cache.put("/index.html", responseClone))
          return response
        })
        .catch(() => caches.match("/index.html")),
    )
    return
  }

  if (isApiRequest) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const responseClone = response.clone()
            caches.open(API_CACHE).then((cache) => cache.put(request, responseClone))
          }
          return response
        })
        .catch(() => caches.match(request)),
    )
    return
  }

  if (!isSameOrigin) {
    return
  }

  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      const networkPromise = fetch(request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone()
          caches.open(STATIC_CACHE).then((cache) => cache.put(request, responseClone))
        }
        return networkResponse
      })
      return cachedResponse || networkPromise
    }).catch(() => caches.match("/index.html")),
  )
})
