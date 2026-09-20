// Progressive enhancement: add a text filter above the big register tables. Typing hides
// non-matching rows; clearing restores them. Degrades to plain, still-searchable tables if this
// script does not run.
//
// Bound to document$ (Material's supported hook) rather than DOMContentLoaded, because
// `navigation.instant` does not reload the document between pages. Binding is idempotent, and it
// is independent of the click-to-sort enhancement on the same tables: sorting reorders rows,
// filtering toggles their visibility.
//
// PLACEMENT MATTERS. Material wraps every `table:not([class])` at runtime in
// `div.md-typeset__scrollwrap > div.md-typeset__table`, and the scrollwrap is `overflow-x: auto`.
// The theme bundle loads before this file, so its wrapping has already happened and the table's
// parent is the INNER wrapper. Inserting relative to the table therefore put the filter box
// inside the horizontal scroll region, where it scrolled out of view on exactly the widest
// register tables. Anchoring on the scrollwrap keeps the box outside the scroll region, and works
// whether or not the wrapping has happened yet.
function initTableFilter() {
  document.querySelectorAll("article table").forEach(function (t) {
    if (t.dataset.tablefilterBound === "1") return;
    var body = t.tBodies && t.tBodies[0];
    if (!body) return;
    var rows = body.rows;

    // Every register page gets a filter regardless of size, because consistency across the
    // registers matters more than saving a control on a short one. Elsewhere, only tables big
    // enough to be worth filtering - a row count alone does not mean "register", and a low
    // threshold put filter boxes on small prose tables.
    var isRegister = /\/registers\//.test(window.location.pathname);
    if (!isRegister && rows.length < 12) return;
    t.dataset.tablefilterBound = "1";

    var input = document.createElement("input");
    input.type = "text";
    input.className = "table-filter";
    input.placeholder = "Filter " + rows.length + " rows…";
    input.setAttribute("aria-label", "Filter table rows");

    // Anchor outside Material's horizontal scroll container when it exists.
    var ref = t.closest(".md-typeset__scrollwrap") || t;
    ref.parentNode.insertBefore(input, ref);

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
