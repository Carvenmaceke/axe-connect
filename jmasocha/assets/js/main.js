(function () {
  var WHATSAPP = "27661322462";
  var EMAIL = "wanhloni@gmail.com";

  // Mobile menu
  var header = document.querySelector(".site-header");
  var menuBtn = document.querySelector(".menu-btn");
  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = header.classList.toggle("nav-open");
      menuBtn.setAttribute("aria-expanded", open);
    });
  }

  // Footer year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Reveal on scroll
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -60px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  // Gallery filters
  var gallery = document.querySelector(".gallery");
  var filters = document.querySelectorAll(".filter");
  var items = gallery ? Array.prototype.slice.call(gallery.querySelectorAll("figure")) : [];

  function visibleItems() { return items.filter(function (f) { return !f.hidden; }); }

  function applyFilter(cat) {
    var found = false;
    filters.forEach(function (b) {
      var on = b.dataset.filter === cat;
      if (on) found = true;
      b.setAttribute("aria-pressed", on);
    });
    if (!found) return applyFilter("all");
    items.forEach(function (f) {
      f.hidden = cat !== "all" && f.dataset.tags.split(" ").indexOf(cat) === -1;
    });
    var empty = document.querySelector(".gallery-empty");
    if (empty) empty.hidden = visibleItems().length > 0;
  }

  if (gallery && filters.length) {
    filters.forEach(function (b) {
      var cat = b.dataset.filter;
      var count = cat === "all" ? items.length : items.filter(function (f) {
        return f.dataset.tags.split(" ").indexOf(cat) !== -1;
      }).length;
      var small = b.querySelector("small");
      if (small) small.textContent = count;
      b.addEventListener("click", function () {
        applyFilter(cat);
        history.replaceState(null, "", cat === "all" ? location.pathname : "#" + cat);
      });
    });
    applyFilter(location.hash.slice(1) || "all");
  }

  // Lightbox
  var lb = document.querySelector(".lightbox");
  if (lb && gallery) {
    var lbImg = lb.querySelector("img");
    var lbCap = lb.querySelector(".lb-caption");
    var current = 0;
    var lastFocus = null;

    function show(i) {
      var list = visibleItems();
      current = (i + list.length) % list.length;
      var img = list[current].querySelector("img");
      lbImg.src = img.dataset.full;
      lbImg.alt = img.alt;
      lbCap.textContent = list[current].querySelector("figcaption").textContent + "  ·  " + (current + 1) + " / " + list.length;
    }
    function open(fig) {
      lastFocus = document.activeElement;
      show(visibleItems().indexOf(fig));
      lb.classList.add("open");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-close").focus();
    }
    function close() {
      lb.classList.remove("open");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    }

    items.forEach(function (f) {
      f.addEventListener("click", function () { open(f); });
      f.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(f); }
      });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
    var touchX = null;
    lb.addEventListener("touchstart", function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      touchX = null;
    });
  }

  // Booking links: prefill a WhatsApp message with the package name
  document.querySelectorAll("[data-book]").forEach(function (a) {
    var msg = "Hi J Masocha Photography, I'd like the packages and prices for: " + a.dataset.book;
    a.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(msg);
    a.target = "_blank";
    a.rel = "noopener";
  });

  // Contact form: the site is static, so send via WhatsApp or the visitor's email app
  var form = document.querySelector("#booking-form");
  if (form) {
    var shoot = new URLSearchParams(location.search).get("shoot");
    if (shoot) {
      var sel = form.querySelector("#shoot");
      Array.prototype.forEach.call(sel.options, function (o) { if (o.value === shoot) sel.value = shoot; });
    }
    function compose() {
      var d = new FormData(form);
      return [
        "Hi J Masocha Photography,",
        "",
        "Name: " + d.get("name"),
        "Phone: " + d.get("phone"),
        d.get("email") ? "Email: " + d.get("email") : null,
        "Shoot: " + d.get("shoot"),
        d.get("date") ? "Preferred date: " + d.get("date") : null,
        "",
        d.get("message")
      ].filter(function (l) { return l !== null; }).join("\n");
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var via = e.submitter && e.submitter.value === "email" ? "email" : "whatsapp";
      var text = compose();
      if (via === "email") {
        location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Booking enquiry: " + new FormData(form).get("shoot")) + "&body=" + encodeURIComponent(text);
      } else {
        window.open("https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text), "_blank", "noopener");
      }
    });
  }
})();
