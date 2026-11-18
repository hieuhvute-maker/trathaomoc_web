(function () {
  if (typeof window.ENABLE_ONLINE_SHOPPING !== "undefined" && !window.ENABLE_ONLINE_SHOPPING) {
    return;
  }
  var KEY = "bachphuc_cart";

  function read() {
    try {
      var items = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(items) ? items : [];
    } catch (e) {
      return [];
    }
  }

  function write(items) {
    localStorage.setItem(KEY, JSON.stringify(items));
    refreshBadges();
    window.dispatchEvent(new CustomEvent("bpcart:change", { detail: items }));
  }

  function count() {
    return read().reduce(function (sum, it) { return sum + it.qty; }, 0);
  }

  function add(id, qty) {
    qty = qty || 1;
    var items = read();
    var found = items.find(function (it) { return it.id === id; });
    if (found) {
      found.qty = Math.min(found.qty + qty, 50);
    } else {
      items.push({ id: id, qty: qty });
    }
    write(items);
  }

  function setQty(id, qty) {
    var items = read();
    if (qty <= 0) {
      items = items.filter(function (it) { return it.id !== id; });
    } else {
      items.forEach(function (it) { if (it.id === id) it.qty = Math.min(qty, 50); });
    }
    write(items);
  }

  function clear() {
    write([]);
  }

  function refreshBadges() {
    var n = count();
    document.querySelectorAll(".bp-cart-count").forEach(function (el) {
      el.textContent = n;
      el.hidden = n === 0;
    });
  }

  function isEnglish() {
    return localStorage.getItem("bachphuc_lang") === "en";
  }

  function toast(msg) {
    var el = document.createElement("div");
    el.className = "bp-cart-toast";
    el.textContent = msg;
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add("show"); });
    setTimeout(function () {
      el.classList.remove("show");
      setTimeout(function () { el.remove(); }, 300);
    }, 1800);
  }

  function injectStyles() {
    var css =
      ".bp-cart-link{position:relative;display:inline-flex;align-items:center;justify-content:center;" +
      "width:40px;height:40px;border-radius:50%;text-decoration:none;font-size:20px;margin-left:8px;" +
      "background:rgba(255,255,255,.12);color:inherit;flex-shrink:0}" +
      ".bp-cart-link:hover{background:rgba(255,255,255,.22)}" +
      ".bp-cart-count{position:absolute;top:-4px;right:-4px;min-width:20px;height:20px;padding:0 5px;" +
      "border-radius:10px;background:#c0392b;color:#fff;font-size:12px;font-weight:700;line-height:20px;text-align:center}" +
      ".bp-cart-count[hidden]{display:none}" +
      ".bp-cart-toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,20px);opacity:0;" +
      "background:#2d4a2b;color:#fff;padding:12px 20px;border-radius:8px;font-size:15px;z-index:9999;" +
      "transition:all .3s;box-shadow:0 4px 14px rgba(0,0,0,.25)}" +
      ".bp-cart-toast.show{opacity:1;transform:translate(-50%,0)}" +
      ".bp-add-cart-btn{cursor:pointer;border:none;font:inherit}";
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
  }

  function injectCartIcon() {
    document.querySelectorAll(".top-nav-inner").forEach(function (nav) {
      if (nav.querySelector(".bp-cart-link")) return;
      var a = document.createElement("a");
      a.href = "/giohang";
      a.className = "bp-cart-link";
      a.setAttribute("aria-label", "Giỏ hàng");
      a.title = isEnglish() ? "Cart" : "Giỏ hàng";
      a.innerHTML = '🛒<span class="bp-cart-count" hidden>0</span>';
      nav.appendChild(a);
    });
  }

  function bindAddButtons() {
    document.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-add-to-cart]");
      if (!btn) return;
      e.preventDefault();
      add(btn.getAttribute("data-add-to-cart"), 1);
      toast(isEnglish() ? "Added to cart" : "Đã thêm vào giỏ hàng");
    });
  }

  injectStyles();
  injectCartIcon();
  bindAddButtons();
  refreshBadges();

  window.BPCart = {
    get: read,
    count: count,
    add: add,
    setQty: setQty,
    clear: clear,
  };
})();
