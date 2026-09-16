// Progressive enhancement: make all content tables click-to-sort.
// Degrades gracefully to plain (still searchable) tables if the CDN is unavailable.
document.addEventListener("DOMContentLoaded", function () {
  if (typeof Tablesort === "undefined") return;
  document.querySelectorAll("article table").forEach(function (t) {
    try { new Tablesort(t); } catch (e) { /* no-op */ }
  });
});
