// Progressive enhancement: make all content tables click-to-sort.
// Degrades gracefully to plain (still searchable) tables if the CDN is unavailable.
//
// Bound to document$ rather than DOMContentLoaded. When `navigation.instant` engages the
// document is not reloaded between pages, so a DOMContentLoaded handler would not run
// again; document$ is Material's supported hook and fires in both cases. Binding is made
// idempotent so a table is never wired twice if the hook fires more than once.
function initTablesort() {
  if (typeof Tablesort === "undefined") return;
  document.querySelectorAll("article table").forEach(function (t) {
    if (t.dataset.tablesortBound === "1") return;
    try {
      new Tablesort(t);
      t.dataset.tablesortBound = "1";
    } catch (e) { /* no-op */ }
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(initTablesort);
} else {
  document.addEventListener("DOMContentLoaded", initTablesort);
}
