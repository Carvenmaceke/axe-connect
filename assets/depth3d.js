// 3D depth across the site: cards lean towards the pointer with a soft glare,
// and "tilt" reveals turn up out of the page in 3D (their parents get perspective).
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-anim="tilt"]').forEach(function (el) {
    var p = el.parentElement; if (p && !p.style.perspective) p.style.perspective = '1200px';
  });
  if (reduce || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('.b-card, .proj, .step, .pr-item, .tw-card').forEach(function (el) {
    el.classList.add('tilt3d');
    var glare = document.createElement('span'); glare.className = 'tilt3d-glare'; glare.setAttribute('aria-hidden', 'true'); el.appendChild(glare);
    var raf = 0, max = el.classList.contains('big') ? 5 : 8;
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () {
        el.style.transform = 'perspective(1000px) rotateX(' + ((0.5 - y) * max).toFixed(2) + 'deg) rotateY(' + ((x - 0.5) * max).toFixed(2) + 'deg) translateY(-4px)';
        el.style.setProperty('--gx', (x * 100).toFixed(1) + '%'); el.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
      });
    });
    el.addEventListener('pointerleave', function () { cancelAnimationFrame(raf); el.style.transform = ''; });
  });
})();
