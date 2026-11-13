/* Bencepo addons – shared helpers. Only network call: a cookie-free page view count (GoatCounter). */
"use strict";
(function () {
  const B = window.BENCEPO = window.BENCEPO || {};

  // Which addon wrote this export? Returns "leveltrail", "vendorfloor" or null.
  B.detect = function (text) {
    text = String(text || "").trim();
    const a = text.indexOf("{"), b = text.lastIndexOf("}");
    if (a < 0 || b < a) return null;
    let d; try { d = JSON.parse(text.slice(a, b + 1)); } catch (e) { return null; }
    if (d && (d.levelTrail || d.bencepoExport) && d.char) return "leveltrail";
    if (d && d.vendorFloor && d.total) return "vendorfloor";
    return null;
  };

  // Hand an export over to its tool page (same site, sessionStorage only).
  const HANDOFF = "bencepo.handoff";
  B.handoff = function (kind, text, base) {
    try { sessionStorage.setItem(HANDOFF, JSON.stringify({ kind, text })); } catch (e) {}
    location.href = (base || "") + kind + "/#imported";
  };
  B.takeHandoff = function (kind) {
    try {
      const v = JSON.parse(sessionStorage.getItem(HANDOFF) || "null");
      if (v && v.kind === kind) { sessionStorage.removeItem(HANDOFF); return v.text; }
    } catch (e) {}
    return null;
  };

  B.toast = function (msg) {
    let t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(B._tt); B._tt = setTimeout(() => t.classList.remove("show"), 2400);
  };

  B.copy = async function (text, ok) {
    try { await navigator.clipboard.writeText(text); B.toast(ok || "Copied."); }
    catch (e) { B.toast("Copy failed. Select the text and press Ctrl+C."); }
  };

  // Fade sections in as they scroll into view.
  function reveal() {
    const els = document.querySelectorAll(".reveal:not(.in)");
    if (!("IntersectionObserver" in window)) { els.forEach(e => e.classList.add("in")); return; }
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -40px 0px" });
    els.forEach(e => io.observe(e));
  }
  B.reveal = reveal;

  // Highlight the section tab whose section is on screen.
  B.sectionTabs = function (nav) {
    if (!nav || !("IntersectionObserver" in window)) return;
    const links = [...nav.querySelectorAll("a[href^='#']")];
    const map = new Map(links.map(a => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver(es => {
      es.forEach(e => {
        if (!e.isIntersecting) return;
        links.forEach(a => a.classList.remove("on"));
        const a = map.get(e.target.id); if (a) { a.classList.add("on"); a.scrollIntoView({ block: "nearest", inline: "nearest" }); }
      });
    }, { rootMargin: "-130px 0px -60% 0px" });
    map.forEach((a, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  };

  document.addEventListener("DOMContentLoaded", reveal);

  /* Page view counter: one image request to GoatCounter, no cookies, no IDs, no third-party script. */
  const count = () => {
    const h = location.hostname;
    if (!/\.github\.io$/.test(h) || navigator.doNotTrack === "1") return;
    try {
      const q = new URLSearchParams({
        p: location.pathname,
        t: document.title,
        r: document.referrer,
        q: location.search,
        s: [screen.width, screen.height, devicePixelRatio || 1].join(","),
        rnd: Math.random().toString(36).slice(2)
      });
      new Image().src = "https://bencepo.goatcounter.com/count?" + q.toString();
    } catch (e) { /* counting is optional */ }
  };
  document.addEventListener("DOMContentLoaded", count);
})();
