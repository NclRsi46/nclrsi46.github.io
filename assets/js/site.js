// Progressive enhancement only: DESIGN.md "JavaScript".
// Theme: "system" (no attribute) -> "light" -> "dark". Stored per viewer; works without storage.
(function () {
  var root = document.documentElement;
  var order = ["system", "light", "dark"];
  function get() { try { return localStorage.getItem("theme") || "system"; } catch (e) { return "system"; } }
  function set(t) {
    if (t === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
    try { localStorage.setItem("theme", t); } catch (e) {}
    var b = document.querySelector("[data-theme-toggle]");
    if (b) { b.textContent = "Theme: " + t; b.setAttribute("aria-label", "Color theme: " + t + ". Change theme"); }
  }
  set(get());
  document.addEventListener("DOMContentLoaded", function () {
    set(get());
    var b = document.querySelector("[data-theme-toggle]");
    if (b) b.hidden = false; // buttons ship hidden so the page has no dead controls with JS off
    document.querySelectorAll("[data-copy]").forEach(function (btn) { if (navigator.clipboard) btn.hidden = false; });
    if (b) b.addEventListener("click", function () {
      root.classList.add("theme-anim");
      set(order[(order.indexOf(get()) + 1) % order.length]);
      setTimeout(function () { root.classList.remove("theme-anim"); }, 300);
    });
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var status = btn.parentNode.querySelector("[data-copy-status]");
        navigator.clipboard.writeText(btn.getAttribute("data-copy")).then(function () {
          if (status) { status.textContent = "Copied"; setTimeout(function () { status.textContent = ""; }, 2000); }
        });
      });
    });
  });
})();
