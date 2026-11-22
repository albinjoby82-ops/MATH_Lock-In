/* Rules pop-up: differentiation and integration rules.
   Drop-in: add <script src="rules-popup.js" defer></script> to any page.
   Open with the "Rules" button or press R. Close with Esc or the X.
   Side panel, no dark backdrop, so the question stays visible. */
(function () {
  "use strict";

  var KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css";
  var KATEX_JS = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js";

  /* ---------- DATA ---------- */
  /* section: {title, head:[colA,colB], plainA:bool, rows:[[a,b],...]}  a/b are LaTeX unless plainA */
  var TABS = [
    {
      id: "diff",
      name: "Derivatives",
      sections: [
        {
          title: "Basic functions",
          head: ["Function", "Derivative"],
          rows: [
            ["c", "0"],
            ["x^n", "n\\,x^{n-1}"],
            ["\\sqrt{x}", "\\dfrac{1}{2\\sqrt{x}}"],
            ["\\dfrac{1}{x}", "-\\dfrac{1}{x^2}"],
            ["e^{x}", "e^{x}"],
            ["e^{kx}", "k\\,e^{kx}"],
            ["a^{x}", "a^{x}\\ln a"],
            ["\\ln x", "\\dfrac{1}{x}"],
            ["\\log_a x", "\\dfrac{1}{x\\ln a}"]
          ]
        },
        {
          title: "Trig",
          head: ["Function", "Derivative"],
          rows: [
            ["\\sin x", "\\cos x"],
            ["\\cos x", "-\\sin x"],
            ["\\tan x", "\\sec^2 x"],
            ["\\sec x", "\\sec x\\tan x"],
            ["\\csc x", "-\\csc x\\cot x"],
            ["\\cot x", "-\\csc^2 x"]
          ]
        },
        {
          title: "Inverse trig",
          head: ["Function", "Derivative"],
          rows: [
            ["\\arcsin x", "\\dfrac{1}{\\sqrt{1-x^2}}"],
            ["\\arccos x", "-\\dfrac{1}{\\sqrt{1-x^2}}"],
            ["\\arctan x", "\\dfrac{1}{1+x^2}"]
          ]
        },
        {
          title: "Hyperbolic",
          head: ["Function", "Derivative"],
          rows: [
            ["\\sinh x", "\\cosh x"],
            ["\\cosh x", "\\sinh x"],
            ["\\tanh x", "\\operatorname{sech}^2 x"]
          ]
        },
        {
          title: "Combining rules",
          head: ["Rule", "Formula"],
          plainA: true,
          rows: [
            ["Constant multiple", "(c f)' = c f'"],
            ["Sum", "(f+g)' = f' + g'"],
            ["Product", "(fg)' = f'g + f g'"],
            ["Quotient", "\\left(\\dfrac{f}{g}\\right)' = \\dfrac{f'g - f g'}{g^2}"],
            ["Chain", "\\dfrac{d}{dx}f(g(x)) = f'(g(x))\\cdot g'(x)"],
            ["ln of anything", "\\dfrac{d}{dx}\\ln u = \\dfrac{u'}{u}"],
            ["Power of anything", "\\dfrac{d}{dx}u^n = n\\,u^{n-1}u'"]
          ]
        }
      ]
    },
    {
      id: "int",
      name: "Integrals",
      sections: [
        {
          title: "Basic functions (add + C)",
          head: ["Function", "Integral"],
          rows: [
            ["x^n \\;(n\\neq -1)", "\\dfrac{x^{n+1}}{n+1}"],
            ["\\dfrac{1}{x}", "\\ln|x|"],
            ["e^{x}", "e^{x}"],
            ["e^{kx}", "\\dfrac{e^{kx}}{k}"],
            ["a^{x}", "\\dfrac{a^{x}}{\\ln a}"],
            ["\\ln x", "x\\ln x - x"]
          ]
        },
        {
          title: "Trig (add + C)",
          head: ["Function", "Integral"],
          rows: [
            ["\\sin x", "-\\cos x"],
            ["\\cos x", "\\sin x"],
            ["\\sec^2 x", "\\tan x"],
            ["\\csc^2 x", "-\\cot x"],
            ["\\sec x\\tan x", "\\sec x"],
            ["\\csc x\\cot x", "-\\csc x"],
            ["\\tan x", "-\\ln|\\cos x|"],
            ["\\sec x", "\\ln|\\sec x + \\tan x|"],
            ["\\sin^2 x", "\\dfrac{x}{2} - \\dfrac{\\sin 2x}{4}"],
            ["\\cos^2 x", "\\dfrac{x}{2} + \\dfrac{\\sin 2x}{4}"]
          ]
        },
        {
          title: "Inverse trig forms (add + C)",
          head: ["Function", "Integral"],
          rows: [
            ["\\dfrac{1}{\\sqrt{1-x^2}}", "\\arcsin x"],
            ["\\dfrac{1}{1+x^2}", "\\arctan x"],
            ["\\dfrac{1}{\\sqrt{a^2-x^2}}", "\\arcsin\\dfrac{x}{a}"],
            ["\\dfrac{1}{a^2+x^2}", "\\dfrac{1}{a}\\arctan\\dfrac{x}{a}"]
          ]
        },
        {
          title: "Hyperbolic (add + C)",
          head: ["Function", "Integral"],
          rows: [
            ["\\sinh x", "\\cosh x"],
            ["\\cosh x", "\\sinh x"]
          ]
        }
      ]
    },
    {
      id: "methods",
      name: "Methods",
      sections: [
        {
          title: "Integration methods",
          head: ["Method", "Formula"],
          plainA: true,
          rows: [
            ["ln rule (top = derivative of bottom)", "\\displaystyle\\int \\dfrac{u'}{u}\\,dx = \\ln|u| + C"],
            ["Power of anything", "\\displaystyle\\int u^n\\,u'\\,dx = \\dfrac{u^{n+1}}{n+1} + C"],
            ["Substitution", "\\displaystyle\\int f(g(x))\\,g'(x)\\,dx = \\int f(u)\\,du"],
            ["By parts", "\\displaystyle\\int u\\,dv = uv - \\int v\\,du"],
            ["Definite integral", "\\displaystyle\\int_a^b f\\,dx = F(b) - F(a)"]
          ]
        },
        {
          title: "When to use which",
          head: ["You see", "Try"],
          plainA: true,
          rows: [
            ["Function and its derivative both present", "Substitution"],
            ["Top is derivative of bottom", "ln rule"],
            ["Product like x eˣ, x sin x, x ln x", "By parts (pick u: ln, then x-power, then trig or exponential)"],
            ["sin² or cos²", "Half-angle identity"]
          ]
        },
        {
          title: "Trig identities",
          head: ["Name", "Formula"],
          plainA: true,
          rows: [
            ["Pythagoras", "\\sin^2 x + \\cos^2 x = 1"],
            ["Double angle (sin)", "\\sin 2x = 2\\sin x\\cos x"],
            ["Double angle (cos)", "\\cos 2x = \\cos^2 x - \\sin^2 x"],
            ["Half angle (sin²)", "\\sin^2 x = \\dfrac{1-\\cos 2x}{2}"],
            ["Half angle (cos²)", "\\cos^2 x = \\dfrac{1+\\cos 2x}{2}"]
          ]
        }
      ]
    },
    {
      id: "multi",
      name: "Multivariable",
      sections: [
        {
          title: "Derivatives",
          head: ["Name", "Formula"],
          plainA: true,
          rows: [
            ["Partial derivative", "f_x:\\ \\text{differentiate in } x,\\ \\text{treat } y \\text{ as constant}"],
            ["Gradient", "\\nabla f = (f_x,\\ f_y)"],
            ["Linear approximation", "f(a+\\Delta x,\\, b+\\Delta y) \\approx f(a,b) + f_x\\,\\Delta x + f_y\\,\\Delta y"],
            ["Directional derivative", "D_{\\mathbf u}f = \\nabla f\\cdot\\mathbf u \\quad(\\mathbf u \\text{ a unit vector})"],
            ["Chain rule", "\\dfrac{df}{dt} = f_x\\dfrac{dx}{dt} + f_y\\dfrac{dy}{dt}"],
            ["Second derivative test", "D = f_{xx}f_{yy} - (f_{xy})^2"]
          ]
        },
        {
          title: "Second derivative test, how to read D",
          head: ["Result", "Meaning"],
          plainA: true,
          rows: [
            ["D > 0 and fₓₓ > 0", "local minimum"],
            ["D > 0 and fₓₓ < 0", "local maximum"],
            ["D < 0", "saddle point"],
            ["D = 0", "test fails"]
          ]
        },
        {
          title: "Double integrals",
          head: ["Name", "Formula"],
          plainA: true,
          rows: [
            ["Rectangle (either order)", "\\displaystyle\\iint_R f\\,dA = \\int_a^b\\!\\int_c^d f\\,dy\\,dx"],
            ["Polar coordinates", "x = r\\cos\\theta,\\quad y = r\\sin\\theta,\\quad dA = r\\,dr\\,d\\theta"]
          ]
        }
      ]
    }
  ];

  /* ---------- STYLE ---------- */
  var CSS = [
    ".rp-btn{position:fixed;right:16px;bottom:16px;z-index:9998;min-width:44px;min-height:44px;padding:0 16px;",
    "border:1px solid #1f4fbf;border-radius:0;background:#fff;color:#1f4fbf;font:600 17px/1 KaTeX_Main,Georgia,serif;cursor:pointer;",
    "box-shadow:0 2px 8px rgba(0,0,0,.18)}",
    ".rp-btn:hover{background:#eef3fd}",
    ".rp-panel{position:fixed;top:0;right:0;bottom:0;z-index:9999;width:min(440px,100vw);background:#fff;color:#1a1a1a;",
    "border-left:1px solid #d4d4d8;box-shadow:-4px 0 18px rgba(0,0,0,.15);display:none;flex-direction:column;font:16px/1.45 KaTeX_Main,Georgia,serif}",
    ".rp-panel.rp-open{display:flex}",
    ".rp-head{display:flex;align-items:center;justify-content:space-between;padding:10px 12px 6px 16px}",
    ".rp-head b{font-size:19px}",
    ".rp-x{min-width:44px;min-height:44px;border:0;background:none;font-size:26px;cursor:pointer;color:#444}",
    ".rp-tabs{display:flex;gap:6px;padding:0 12px 8px;flex-wrap:wrap;border-bottom:1px solid #e4e4e7}",
    ".rp-tab{min-height:44px;padding:0 12px;border:1px solid #c7c7cc;border-radius:0;background:#fff;color:#1a1a1a;font:600 15px KaTeX_Main,Georgia,serif;cursor:pointer}",
    ".rp-tab[aria-selected=true]{background:#1f4fbf;color:#fff;border-color:#1f4fbf}",
    ".rp-body{overflow:auto;padding:4px 16px 24px;flex:1}",
    ".rp-body h3{margin:18px 0 6px;font-size:15px;color:#1f4fbf}",
    ".rp-body table{width:100%;border-collapse:collapse}",
    ".rp-body th{text-align:left;font-size:12px;color:#666;font-weight:600;padding:2px 6px;border-bottom:1px solid #d4d4d8}",
    ".rp-body td{padding:7px 6px;border-bottom:1px solid #eee;vertical-align:middle}",
    ".rp-body td.rp-plain{font-weight:600;font-size:14px;width:36%}",
    ".rp-hint{font-size:12px;color:#777;padding:0 16px 8px}",
    "@media (max-width:640px){.rp-panel{top:auto;height:70vh;width:100vw;border-left:0;border-top:1px solid #d4d4d8}}"
  ].join("");

  /* ---------- BUILD ---------- */
  var panel, body, tabsEl, btn, current = "diff", ready = false;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function tex(node, src) {
    if (window.katex) {
      try { window.katex.render(src, node, { throwOnError: false }); return; } catch (e) {}
    }
    node.textContent = src;
  }

  function renderTab(id) {
    current = id;
    try { localStorage.setItem("rp-tab", id); } catch (e) {}
    var tab = TABS.filter(function (t) { return t.id === id; })[0] || TABS[0];
    Array.prototype.forEach.call(tabsEl.children, function (b) {
      b.setAttribute("aria-selected", b.dataset.id === tab.id ? "true" : "false");
    });
    body.textContent = "";
    tab.sections.forEach(function (s) {
      body.appendChild(el("h3", "", s.title));
      var table = el("table");
      var thead = el("tr");
      s.head.forEach(function (h) { thead.appendChild(el("th", "", h)); });
      table.appendChild(thead);
      s.rows.forEach(function (r) {
        var tr = el("tr");
        var a = el("td", s.plainA ? "rp-plain" : "");
        var b = el("td");
        if (s.plainA) a.textContent = r[0]; else tex(a, r[0]);
        var isTextRow = s.plainA && !/[\\=^_]/.test(r[1]);
        if (isTextRow) b.textContent = r[1]; else tex(b, r[1]);
        tr.appendChild(a); tr.appendChild(b); table.appendChild(tr);
      });
      body.appendChild(table);
    });
    body.scrollTop = 0;
  }

  function build() {
    var style = el("style"); style.textContent = CSS; document.head.appendChild(style);

    btn = el("button", "rp-btn", "∑ Rules");
    btn.type = "button"; btn.setAttribute("aria-label", "Open rules (press R)");
    btn.onclick = toggle;

    panel = el("div", "rp-panel");
    panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Differentiation and integration rules");

    var head = el("div", "rp-head");
    head.appendChild(el("b", "", "Rules"));
    var x = el("button", "rp-x", "×"); x.type = "button"; x.setAttribute("aria-label", "Close"); x.onclick = close;
    head.appendChild(x);

    tabsEl = el("div", "rp-tabs"); tabsEl.setAttribute("role", "tablist");
    TABS.forEach(function (t) {
      var b = el("button", "rp-tab", t.name);
      b.type = "button"; b.dataset.id = t.id; b.setAttribute("role", "tab");
      b.onclick = function () { renderTab(t.id); };
      tabsEl.appendChild(b);
    });

    body = el("div", "rp-body");
    var hint = el("div", "rp-hint", "Press R to open or close. Esc also closes.");

    panel.appendChild(head); panel.appendChild(tabsEl); panel.appendChild(hint); panel.appendChild(body);
    document.body.appendChild(btn); document.body.appendChild(panel);

    document.addEventListener("keydown", function (e) {
      var t = e.target, typing = t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable);
      if (e.key === "Escape" && panel.classList.contains("rp-open")) { close(); return; }
      if (!typing && !e.ctrlKey && !e.metaKey && !e.altKey && (e.key === "r" || e.key === "R")) toggle();
    });
  }

  function open() {
    panel.classList.add("rp-open");
    if (!ready) {
      var saved = "diff";
      try { saved = localStorage.getItem("rp-tab") || "diff"; } catch (e) {}
      ready = true; renderTab(saved);
    }
  }
  function close() { panel.classList.remove("rp-open"); }
  function toggle() { panel.classList.contains("rp-open") ? close() : open(); }

  function loadKatex(cb) {
    if (window.katex) { cb(); return; }
    var l = document.createElement("link"); l.rel = "stylesheet"; l.href = KATEX_CSS; document.head.appendChild(l);
    var s = document.createElement("script"); s.src = KATEX_JS; s.onload = cb; s.onerror = cb; document.head.appendChild(s);
  }

  function start() { loadKatex(build); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
