/* Massar shell — the side menu and the sub-tab strip, injected once so every
   screen shares them. The structure mirrors the live app exactly: seven doors,
   each with its own ordered sub-destinations, the first of which is the door's
   own landing route. A door with one entry renders no tab strip at all.
   A screen sets `data-nav` (door) and `data-sub` (route) on <body>. */
(function () {
  /* Badge counts are written here by gen.py from the same records the screens
     render. They were typed by hand once, and the rail said six products while
     the products table listed eight. A count that is maintained in two places
     is a count that will disagree with itself. */
  var COUNTS = {"accounts": "16", "opps": "6", "products": "8"}; /* gen.py:COUNTS */
  var DOORS = [
    { id: "home",     l: "الرئيسية",  d: "M3 10.5 12 3l9 7.5M5.5 9.5V20h13V9.5" },
    { id: "opps",     l: "فرص البيع", d: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" },
    { id: "accounts", l: "العملاء",   d: "M16 20v-2a4 4 0 0 0-8 0v2M12 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7" },
    { id: "products", l: "المنتجات",  d: "M21 8 12 3 3 8l9 5 9-5ZM3 8v8l9 5 9-5V8" },
    { id: "kmon",     l: "الحملات",   d: "M4 11v3l14 5V6L4 11ZM4 11H3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1" },
    { id: "reports",  l: "التقارير",  d: "M4 20V10M10 20V4M16 20v-7M22 20H2" },
    { id: "settings", l: "الإعدادات", d: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1 2 2 0 1 1-4 0 1.6 1.6 0 0 0-2.7-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 4.6 15a2 2 0 1 1 0-4 1.6 1.6 0 0 0 1.1-2.7l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 11 4.6a2 2 0 1 1 4 0 1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7 2 2 0 1 1 0 4Z" }
  ];
  var SUBS = {
    opps:     [["opps","الفرص"],["board","لوحة المتابعة"],["triage","فرز الردود"],["pipeline","سجل الأحداث"]],
    accounts: [["accounts","العملاء"],["customers","المحادثات"],["indicators","مؤشرات الاستخدام"],["tasks","المهام"],["notes","الملاحظات"]],
    products: [["products","المنتجات"],["knowledge","معرفة المنتج"],["perf","المستهدفات والأداء"],["org","الهيكل التنظيمي"]],
    kmon:     [["kmon","متابعة الحملات"],["aimkt","إنشاء حملة"],["targets","جهات الاستهداف"],["partners","شركاء المبيعات"]],
    settings: [["settings","مراحل البيع"],["divisions","الأقسام"],["team","الفريق"],["users","المستخدمون والصلاحيات"],["audit","سجل التدقيق"]]
  };

  var door = document.body.getAttribute("data-nav") || "home";
  var sub  = document.body.getAttribute("data-sub") || door;

  var items = DOORS.map(function (i) {
    return '<a class="m-nav" href="' + i.id + '.html" data-t="' + i.l + '" title="' + i.l + '"' +
      (i.id === door ? ' aria-current="page"' : "") + '>' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + i.d + '"/></svg>' +
      "<span>" + i.l + "</span>" + (COUNTS[i.id] ? "<b>" + COUNTS[i.id] + "</b>" : "") + "</a>";
  }).join("");

  var side = document.createElement("nav");
  side.className = "m-side";
  side.setAttribute("aria-label", "التنقل");
  side.innerHTML =
    '<div class="m-side__b"><span class="m-side__logo">م</span>' +
      '<span class="m-side__w"><span class="m-side__n">مسار</span>' +
      '<span class="m-side__r">مدير النظام</span></span></div>' +
    '<div class="m-side__nav">' + items + "</div>" +
    '<div class="m-side__f"><button class="m-side__t" type="button" aria-expanded="true">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 7 5 5-5 5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      "<span>طيّ القائمة</span></button></div>";
  document.querySelector(".m-shell").prepend(side);

  // The sub-tab strip renders under the page title, so a door's destinations
  // are reachable in one click from anywhere inside that door.
  var host = document.querySelector("[data-subs]");
  if (host && SUBS[door]) {
    host.innerHTML = '<div class="m-tabs" role="tablist">' + SUBS[door].map(function (s) {
      return '<a class="m-tab" role="tab" href="' + s[0] + '.html"' +
        (s[0] === sub ? ' aria-selected="true"' : ' aria-selected="false"') + ">" + s[1] + "</a>";
    }).join("") + "</div>";
  }

  var KEY = "massar.side.collapsed";
  function read() { try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; } }
  function write(v) { try { localStorage.setItem(KEY, v ? "1" : "0"); } catch (e) {} }

  var btn = side.querySelector(".m-side__t");
  function apply(c, animate) {
    // The first paint must not animate, or the rail slides in on every load.
    if (!animate) side.style.transition = "none";
    if (c) side.setAttribute("data-collapsed", ""); else side.removeAttribute("data-collapsed");
    btn.setAttribute("aria-expanded", c ? "false" : "true");
    if (!animate) { void side.offsetWidth; side.style.transition = ""; }
  }
  apply(read(), false);
  function toggle() { var n = !side.hasAttribute("data-collapsed"); apply(n, true); write(n); }
  btn.addEventListener("click", toggle);
  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "b" || e.key === "B")) { e.preventDefault(); toggle(); }
  });

  /* ---- Dialogs. Any [data-open="id"] opens the <dialog id>. Escape and the
     backdrop close it. The panel enters from scale(.97), never scale(0) —
     nothing in the real world appears from nothing. ---- */
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-open]");
    if (t) { var dlg = document.getElementById(t.getAttribute("data-open"));
             if (dlg) { dlg.showModal(); } return; }
    var c = e.target.closest("[data-close]");
    if (c) { c.closest("dialog").close(); return; }
  });
  document.addEventListener("click", function (e) {
    if (e.target.tagName === "DIALOG") e.target.close();   // backdrop
  });
})();
