window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// `navigation.instant` is enabled in mkdocs.yml. When it engages, Material swaps page
// content without reloading the document, so DOMContentLoaded fires only once per browser
// load and a handler bound to it never runs again. document$ is Material's supported hook:
// it emits on the initial load and on every subsequent client-side navigation, so it is
// correct in both cases. (Note: the failure was not reproduced in a headless test here,
// where instant navigation did not engage and full page loads occurred instead. This is
// the documented pattern regardless, and it degrades to DOMContentLoaded if document$ is
// absent.)
if (typeof document$ !== "undefined") {
  document$.subscribe(function () {
    if (!window.MathJax || !window.MathJax.typesetPromise) return;
    if (window.MathJax.startup && window.MathJax.startup.output &&
        window.MathJax.startup.output.clearCache) {
      window.MathJax.startup.output.clearCache();
    }
    if (window.MathJax.typesetClear) window.MathJax.typesetClear();
    if (window.MathJax.texReset) window.MathJax.texReset();
    window.MathJax.typesetPromise();
  });
} else {
  document.addEventListener("DOMContentLoaded", function () {
    if (window.MathJax && window.MathJax.typesetPromise) window.MathJax.typesetPromise();
  });
}
