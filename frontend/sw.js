// Service worker mínimo: cachea el "cascarón" de la app (HTML/CSS/JS/íconos)
// para que abra rápido e instale como PWA, y funcione sin conexión. Las
// llamadas a /api/ NUNCA se cachean, porque el progreso del niño debe ser
// siempre información fresca.
//
// Estrategia "red primero, caché de respaldo" (no "caché primero"): mientras
// este piloto está en pruebas, el contenido cambia seguido de una versión a
// otra. Con caché-primero, un navegador que ya visitó la app se queda
// sirviendo el HTML/JS viejo indefinidamente aunque el servidor tenga uno
// nuevo (así se rompió el crucigrama: el navegador seguía usando JS de una
// versión anterior, incompatible con los datos que manda el servidor
// actualizado). Con red-primero, siempre se usa la versión más reciente
// cuando hay conexión, y el caché solo se usa si el teléfono está sin señal.
const CACHE = "catequesis-confirmacion-v1";
const ARCHIVOS = [
  "/", "/index.html", "/css/style.css", "/js/app.js", "/manifest.json",
  "/icons/icon-192.png", "/icons/icon-512.png",
  "/icons/portada-itinerario-fe.jpg", "/icons/san-charbel-header.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ARCHIVOS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith("/api/")) return; // nunca cachear la API

  event.respondWith(
    fetch(event.request)
      .then((res) => {
        const copia = res.clone();
        caches.open(CACHE).then((cache) => cache.put(event.request, copia));
        return res;
      })
      .catch(() => caches.match(event.request))
  );
});
