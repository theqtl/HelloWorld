// Progressive enhancement: add a text filter above the large content tables (the registers).
// Typing hides non-matching rows client-side; clearing restores them. Degrades gracefully to
// plain, still-searchable tables if this script does not run.
//
// Bound to document$ (Material's supported hook) rather than DOMContentLoaded, because
// `navigation.instant` does not reload the document between pages. Binding is idempotent so a
// table is never wired twice, and it is independent of the click-to-sort enhancement on the same
// tables: sorting reorders rows, filtering toggles their visibility, and the two do not conflict.
function initTableFilter() {
  document.querySelectorAll("article table").forEach(function (t) {
    if (t.dataset.tablefilterBound === "1") return;
    var body = t.tBodies && t.tBodies[0];
    if (!body) return;
    var rows = body.rows;
    if (rows.length < 6) return; // only worth a filter box on the big register tables
    t.dataset.tablefilterBound = "1";

    var input = document.createElement("input");
    input.type = "text";
    input.className = "table-filter";
    input.placeholder = "Filter " + rows.length + " rows…";
    input.setAttribute("aria-label", "Filter table rows");
    t.parentNode.insertBefore(input, t);

    input.addEventListener("input", function () {
      var q = input.value.toLowerCase();
      for (var i = 0; i < rows.length; i++) {
        var hit = rows[i].textContent.toLowerCase().indexOf(q) !== -1;
        rows[i].style.display = hit ? "" : "none";
      }
    });
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(initTableFilter);
} else {
  document.addEventListener("DOMContentLoaded", initTableFilter);
}
