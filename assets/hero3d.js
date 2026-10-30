// 3D hero. Web mode: a phone (customer side) sends bookings along a glowing line to a dashboard monitor (your side).
// IT mode: a laptop runs through a repair checklist with the IT services orbiting it.
// The HTML mockups stay in the page and show whenever WebGL isn't available.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const host = document.getElementById('hero3d');
const visual = host && host.closest('.hero-visual');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const RED = 0xE5372B;

function webglOK() { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } }
if (host && visual && webglOK()) (document.fonts ? document.fonts.ready : Promise.resolve()).then(start, start);

// small canvas helpers
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function tex(c) { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; }
function pill(label, dot, dark) {
  const c = document.createElement('canvas'), g = c.getContext('2d'), F = '700 46px Figtree, sans-serif';
  g.font = F; const w = Math.ceil(g.measureText(label).width) + 104; c.width = w; c.height = 96; g.font = F;
  g.fillStyle = dark ? 'rgba(15,17,21,.92)' : 'rgba(255,255,255,.97)'; rr(g, 3, 3, w - 6, 90, 45); g.fill();
  g.strokeStyle = dark ? 'rgba(255,255,255,.18)' : 'rgba(15,17,21,.12)'; g.lineWidth = 3; g.stroke();
  g.fillStyle = dot; g.beginPath(); g.arc(50, 48, 13, 0, 7); g.fill();
  g.fillStyle = dark ? '#F2F3F5' : '#0F1115'; g.textBaseline = 'middle'; g.fillText(label, 76, 51);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex(c), transparent: true, depthWrite: false }));
  const h = 0.3; s.scale.set(h * w / 96, h, 1); return s;
}

function start() {
  const canvas = host.querySelector('canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  camera.position.set(0, 0.7, 10); camera.lookAt(0, -0.12, 0);

  scene.add(new THREE.HemisphereLight(0xffffff, 0x2a1414, 1.25));
  const key = new THREE.DirectionalLight(0xffffff, 1.7); key.position.set(3, 6, 6); scene.add(key);
  const redLight = new THREE.PointLight(RED, 26, 12); redLight.position.set(0, -0.5, 3); scene.add(redLight);

  const metal = new THREE.MeshStandardMaterial({ color: 0x23262d, metalness: 0.7, roughness: 0.35 });
  const silver = new THREE.MeshStandardMaterial({ color: 0xc8ccd3, metalness: 0.75, roughness: 0.3 });

  const glowTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(229,55,43,.6)'); gr.addColorStop(1, 'rgba(229,55,43,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return tex(c); })();
  function floorGlow(w, d, y) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, depthWrite: false })); m.rotation.x = -Math.PI / 2; m.position.y = y; return m; }

  /* ───────── WEB: phone + dashboard ───────── */
  const web = new THREE.Group(); web.position.y = 0.4; scene.add(web);

  // Phone
  const phone = new THREE.Group(); phone.position.set(-2.15, -0.15, 0.6); phone.rotation.set(0.04, 0.42, -0.04); web.add(phone);
  phone.add(new THREE.Mesh(new RoundedBoxGeometry(1.32, 2.62, 0.14, 6, 0.16), metal));
  const pc = document.createElement('canvas'); pc.width = 360; pc.height = 720; const pg = pc.getContext('2d'); const pTex = tex(pc);
  const pScreen = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 2.5), new THREE.MeshBasicMaterial({ map: pTex, toneMapped: false }));
  pScreen.position.z = 0.072; phone.add(pScreen);
  const SLOTS = ['09:00', '10:30', '13:00', '15:30'];
  function drawPhone(t, sentAt) {
    const g = pg; g.fillStyle = '#ffffff'; rr(g, 0, 0, 360, 720, 44); g.fill();
    g.fillStyle = '#0F1115'; rr(g, 140, 18, 80, 22, 11); g.fill();
    g.fillStyle = '#0F1115'; g.font = '700 22px Figtree, sans-serif'; g.fillText('yourbusiness.co.za', 28, 82);
    g.fillStyle = '#E5372B'; rr(g, 24, 110, 312, 170, 24); g.fill();
    g.fillStyle = '#fff'; g.font = '800 40px "Bricolage Grotesque", Figtree, sans-serif'; g.fillText('Book online', 48, 180);
    g.globalAlpha = .85; g.font = '600 21px Figtree, sans-serif'; g.fillText('Pick a time that suits you', 48, 222); g.globalAlpha = 1;
    const on = Math.floor(t / 1.6) % 4;
    SLOTS.forEach((s, i) => { const x = 24 + (i % 2) * 160, y = 310 + Math.floor(i / 2) * 82; g.fillStyle = i === on ? '#E5372B' : '#F1F2F4'; rr(g, x, y, 152, 66, 16); g.fill(); g.fillStyle = i === on ? '#fff' : '#2B2F37'; g.font = '700 26px Figtree, sans-serif'; g.fillText(s, x + 42, y + 42); });
    const pulse = 1 + Math.max(0, Math.sin(t * 3)) * 0.03;
    g.save(); g.translate(180, 520); g.scale(pulse, pulse); g.fillStyle = '#0F1115'; rr(g, -156, -38, 312, 76, 22); g.fill(); g.fillStyle = '#fff'; g.font = '700 26px Figtree, sans-serif'; g.textAlign = 'center'; g.fillText('Confirm booking', 0, 9); g.restore(); g.textAlign = 'left';
    const since = t - sentAt;
    if (since >= 0 && since < 1.6) { const a = Math.min(1, since * 4, (1.6 - since) * 4); g.globalAlpha = a; g.fillStyle = '#16A06A'; rr(g, 40, 610, 280, 64, 32); g.fill(); g.fillStyle = '#fff'; g.font = '700 24px Figtree, sans-serif'; g.fillText('✓  Booking sent', 84, 650); g.globalAlpha = 1; }
    pTex.needsUpdate = true;
  }

  // Monitor with the dashboard
  const mon = new THREE.Group(); mon.position.set(1.25, 0.15, -0.5); mon.rotation.y = -0.32; web.add(mon);
  mon.add(new THREE.Mesh(new RoundedBoxGeometry(3.6, 2.36, 0.12, 4, 0.07), metal));
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.12, 0.85, 16), silver); neck.position.set(0, -1.55, -0.12); mon.add(neck);
  const foot = new THREE.Mesh(new RoundedBoxGeometry(1.5, 0.08, 0.8, 4, 0.04), silver); foot.position.set(0, -1.98, -0.05); mon.add(foot);
  const dc = document.createElement('canvas'); dc.width = 1024; dc.height = 660; const dg = dc.getContext('2d'); const dTex = tex(dc);
  const dScreen = new THREE.Mesh(new THREE.PlaneGeometry(3.44, 2.22), new THREE.MeshBasicMaterial({ map: dTex, toneMapped: false }));
  dScreen.position.z = 0.062; mon.add(dScreen);
  const feed = [['Order #1048 paid', 'R1,250', '#16A06A'], ['Invoice sent', 'INV-207', '#E5372B'], ['New client added', 'Lerato M.', '#5A616E']];
  const NAMES = ['Thandi N.', 'Sipho D.', 'Naledi K.', 'Ayanda M.', 'Kagiso P.'];
  let bookings = 18, orders = 42, revenue = 24.6, flashAt = -9;
  function drawDash(t) {
    const g = dg; g.fillStyle = '#0F1115'; g.fillRect(0, 0, 1024, 660);
    g.fillStyle = '#16181D'; g.fillRect(0, 0, 92, 660);
    for (let i = 0; i < 5; i++) { g.fillStyle = i === 0 ? '#E5372B' : '#2A2D35'; rr(g, 26, 34 + i * 70, 40, 40, 10); g.fill(); }
    g.fillStyle = '#F2F3F5'; g.font = '800 34px "Bricolage Grotesque", Figtree, sans-serif'; g.fillText('Dashboard', 124, 66);
    g.fillStyle = '#2BC48A'; g.beginPath(); g.arc(880, 56, 8, 0, 7); g.fill(); g.font = '600 22px "JetBrains Mono", monospace'; g.fillText('LIVE', 898, 64);
    const kp = [['Bookings today', String(bookings)], ['Orders', String(orders)], ['Revenue', 'R' + revenue.toFixed(1) + 'k']];
    kp.forEach(([l, v], i) => { const x = 124 + i * 290; g.fillStyle = '#1B1E24'; rr(g, x, 96, 270, 116, 16); g.fill(); g.fillStyle = '#9AA1AD'; g.font = '600 20px Figtree, sans-serif'; g.fillText(l, x + 22, 132); g.fillStyle = i === 0 && t - flashAt < 1 ? '#FF6B60' : '#F2F3F5'; g.font = '800 44px Figtree, sans-serif'; g.fillText(v, x + 22, 186); });
    // chart
    g.fillStyle = '#1B1E24'; rr(g, 124, 230, 390, 400, 16); g.fill(); g.fillStyle = '#9AA1AD'; g.font = '600 20px Figtree, sans-serif'; g.fillText('This week', 148, 266);
    const H = [.42, .6, .5, .74, .58, .86, .7];
    H.forEach((h, i) => { const hh = (h + Math.sin(t * 1.2 + i) * 0.05) * 290; g.fillStyle = i === 5 ? '#E5372B' : '#3A3E48'; rr(g, 152 + i * 50, 600 - hh, 32, hh, 8); g.fill(); });
    // feed
    g.fillStyle = '#1B1E24'; rr(g, 534, 230, 460, 400, 16); g.fill(); g.fillStyle = '#9AA1AD'; g.fillText('Latest activity', 558, 266);
    feed.slice(0, 4).forEach(([a, b, col], i) => {
      const y = 290 + i * 82, fresh = i === 0 && t - flashAt < 1.4;
      g.fillStyle = fresh ? 'rgba(229,55,43,.22)' : '#22252C'; rr(g, 552, y, 424, 68, 14); g.fill();
      g.fillStyle = col; g.beginPath(); g.arc(580, y + 34, 9, 0, 7); g.fill();
      g.fillStyle = '#F2F3F5'; g.font = '700 23px Figtree, sans-serif'; g.fillText(a, 602, y + 42);
      g.fillStyle = '#9AA1AD'; g.font = '600 19px "JetBrains Mono", monospace'; g.textAlign = 'right'; g.fillText(b, 960, y + 42); g.textAlign = 'left';
    });
    dTex.needsUpdate = true;
  }

  // The line between the two sides, and the bookings travelling along it
  // the link is rebuilt when the layout changes between wide and narrow screens
  let curve, tube;
  function buildLink() {
    const sx = phone.position.x + 0.7, ex = mon.position.x - (narrow ? 0.9 : 1.67);
    curve = new THREE.CatmullRomCurve3(narrow
      ? [new THREE.Vector3(sx, -0.55, 0.75), new THREE.Vector3(sx + 0.35, -1.2, 0.6), new THREE.Vector3(sx + 0.75, -0.75, 0.2), new THREE.Vector3(ex, -0.25, -0.3)]
      : [new THREE.Vector3(sx, -0.55, 0.75), new THREE.Vector3(sx + 0.85, -1.15, 0.5), new THREE.Vector3(sx + 1.55, -0.2, 0.1), new THREE.Vector3(ex, 0.25, -0.35)]);
    if (tube) { web.remove(tube); tube.geometry.dispose(); }
    tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 80, 0.022, 8, false), tubeMat); web.add(tube);
  }
  const tubeMat = new THREE.MeshBasicMaterial({ color: RED, transparent: true, opacity: 0.75 });
  let narrow = null;
  function layout(isNarrow) {
    if (isNarrow === narrow) return; narrow = isNarrow;
    phone.position.x = narrow ? -1.55 : -2.15; phone.position.z = narrow ? 1.1 : 0.6;
    mon.position.x = narrow ? 0.7 : 1.25;
    cTag.position.set(phone.position.x, 1.55, phone.position.z); yTag.position.set(mon.position.x + 0.3, 1.7, -0.4);
    buildLink();
  }
  const pkts = [0, 1, 2].map(() => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 16), new THREE.MeshBasicMaterial({ color: 0xff8a7a })); const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, transparent: true, depthWrite: false })); halo.scale.set(0.6, 0.6, 1); m.add(halo); web.add(m); return m; });
  const cTag = pill('Customer side', '#E5372B', false); cTag.position.set(-2.1, 1.55, 0.6); web.add(cTag);
  const yTag = pill('Your side', '#16A06A', true); yTag.position.set(1.5, 1.7, -0.4); web.add(yTag);
  web.add(floorGlow(7, 3, -1.95));
  layout(host.clientWidth > 0 && host.clientWidth / host.clientHeight < 1.15);

  /* ───────── IT: laptop running a repair checklist ───────── */
  const it = new THREE.Group(); it.position.y = 0.35; scene.add(it); it.visible = false;
  const lap = new THREE.Group(); lap.position.y = -1.05; lap.rotation.y = -0.4; it.add(lap);
  lap.add(new THREE.Mesh(new RoundedBoxGeometry(4, 0.17, 2.7, 4, 0.08), silver));
  const deck = new THREE.Mesh(new THREE.PlaneGeometry(3.5, 1.5), new THREE.MeshStandardMaterial({ color: 0x1b1e24, roughness: 0.8 })); deck.rotation.x = -Math.PI / 2; deck.position.set(0, 0.087, -0.3); lap.add(deck);
  const hinge = new THREE.Group(); hinge.position.set(0, 0.085, -1.35); hinge.rotation.x = -0.14; lap.add(hinge);
  const lid = new THREE.Mesh(new RoundedBoxGeometry(4, 2.6, 0.11, 4, 0.06), silver); lid.position.y = 1.3; hinge.add(lid);
  const lc = document.createElement('canvas'); lc.width = 1024; lc.height = 640; const lg = lc.getContext('2d'); const lTex = tex(lc);
  const lScreen = new THREE.Mesh(new THREE.PlaneGeometry(3.7, 2.3), new THREE.MeshBasicMaterial({ map: lTex, toneMapped: false })); lScreen.position.set(0, 1.3, 0.06); hinge.add(lScreen);
  const CHECK = ['Hardware check', 'Virus & malware scan', 'Software & driver updates', 'Speed optimisation'];
  function drawLaptop(t) {
    const g = lg, cyc = (t % 9) / 9, done = Math.min(4, Math.floor(cyc * 6)), ready = done >= 4;
    g.fillStyle = '#ffffff'; g.fillRect(0, 0, 1024, 640);
    g.fillStyle = '#0F1115'; g.font = '600 22px "JetBrains Mono", monospace'; g.fillText('REPAIR JOB', 56, 76);
    g.fillStyle = ready ? '#16A06A' : '#E5372B'; rr(g, 690, 44, 280, 50, 25); g.fill(); g.fillStyle = '#fff'; g.font = '700 22px Figtree, sans-serif'; g.fillText(ready ? '✓ Ready for collection' : 'Working on it…', ready ? 712 : 752, 77);
    g.fillStyle = '#0F1115'; g.font = '800 50px "Bricolage Grotesque", Figtree, sans-serif'; g.fillText('Laptop running slow', 56, 160);
    g.fillStyle = '#5A616E'; g.font = '500 24px Figtree, sans-serif'; g.fillText('Diagnosed, fixed and tested before hand-back.', 56, 200);
    CHECK.forEach((c, i) => { const y = 250 + i * 78, ok = i < done, now = i === done && !ready; g.fillStyle = '#F4F5F7'; rr(g, 56, y, 912, 62, 14); g.fill(); g.fillStyle = ok ? '#16A06A' : now ? '#E5372B' : '#C9CDD4'; g.beginPath(); g.arc(94, y + 31, 15, 0, 7); g.fill(); if (ok) { g.strokeStyle = '#fff'; g.lineWidth = 4; g.beginPath(); g.moveTo(86, y + 31); g.lineTo(92, y + 38); g.lineTo(103, y + 24); g.stroke(); } g.fillStyle = '#0F1115'; g.font = '700 26px Figtree, sans-serif'; g.fillText(c, 128, y + 40); g.fillStyle = ok ? '#16A06A' : '#9AA1AD'; g.font = '600 20px "JetBrains Mono", monospace'; g.textAlign = 'right'; g.fillText(ok ? 'done' : now ? 'running' : 'waiting', 940, y + 39); g.textAlign = 'left'; });
    g.fillStyle = '#EEF0F3'; rr(g, 56, 574, 912, 16, 8); g.fill(); g.fillStyle = ready ? '#16A06A' : '#E5372B'; rr(g, 56, 574, 912 * Math.min(1, cyc * 1.5), 16, 8); g.fill();
    lTex.needsUpdate = true;
  }
  const IT_CHIPS = [['Remote session', '#E5372B'], ['Virus removal', '#16A06A'], ['Windows · macOS', '#3B82F6'], ['Networks & Wi-Fi', '#F59E0B'], ['Printers & email', '#8B5CF6'], ['On-site in Pretoria', '#E5372B']];
  const itChips = IT_CHIPS.map(([l, c], i) => { const s = pill(l, c, i % 2 === 1); s.userData.a = (i / IT_CHIPS.length) * Math.PI * 2; s.userData.y = 0.2 + (i % 3) * 0.45; it.add(s); return s; });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(3, 0.012, 8, 160), new THREE.MeshBasicMaterial({ color: RED, transparent: true, opacity: 0.5 })); ring.rotation.x = 1.25; ring.position.y = -0.4; it.add(ring);
  it.add(floorGlow(7, 4, -1.0));

  // Dust in the air
  const N = 260, pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) pos.set([(Math.random() - .5) * 12, (Math.random() - .5) * 7, -2 - Math.random() * 5], i * 3);
  const dg2 = new THREE.BufferGeometry(); dg2.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const dust = new THREE.Points(dg2, new THREE.PointsMaterial({ color: 0xff8a7a, size: 0.035, transparent: true, opacity: 0.6 })); scene.add(dust);

  // Mode switching: the current scene shrinks away and the other grows in
  const modeOf = () => document.documentElement.getAttribute('data-mode') === 'it' ? 'it' : 'web';
  let mode = modeOf(), switchAt = -9, from = null;
  web.visible = mode === 'web'; it.visible = mode === 'it';
  new MutationObserver(() => { const m = modeOf(); if (m !== mode) { from = mode; mode = m; switchAt = clock; wake(); } }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode'] });

  const target = { x: 0, y: 0 }, cur = { x: 0, y: 0 };
  addEventListener('pointermove', e => { target.x = (e.clientX / innerWidth - .5) * 2; target.y = (e.clientY / innerHeight - .5) * 2; }, { passive: true });

  function resize() {
    const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); layout(w / h < 1.15);
  }
  new ResizeObserver(resize).observe(host); resize();

  const t0 = performance.now(); let clock = 0, lastSent = -9, lastArrive = 0;
  function frame(now) {
    clock = (now - t0) / 1000; const t = clock;
    // switching
    const sp = Math.min(1, (t - switchAt) / 0.9), ease = 1 - Math.pow(1 - sp, 3);
    const show = (grp, on) => { grp.visible = on || (sp < 0.5 && from && grp === (from === 'web' ? web : it)); };
    show(web, mode === 'web'); show(it, mode === 'it');
    const inG = mode === 'web' ? web : it, outG = mode === 'web' ? it : web;
    if (sp < 1 && from) { outG.scale.setScalar(Math.max(0.001, 1 - sp * 2)); inG.scale.setScalar(Math.max(0.001, sp < 0.4 ? 0.001 : (sp - 0.4) / 0.6 * ease + 0.001)); }
    else { inG.scale.setScalar(1); outG.visible = false; }

    // frame each scene so it fills the space: the web pair is wide, the laptop is compact
    const half = Math.tan(THREE.MathUtils.degToRad(17)) * camera.aspect, need = mode === 'web' ? (narrow ? 2.95 : 3.75) : (narrow ? 3.7 : 4.1);
    const zT = Math.min(15, Math.max(6.8, need / half));
    camera.position.z += (zT - camera.position.z) * (sp < 1 ? 0.08 : 0.2);
    cur.x += (target.x - cur.x) * 0.06; cur.y += (target.y - cur.y) * 0.06;
    const sc = Math.min(1, scrollY / 700);
    scene.rotation.y = cur.x * 0.22 + Math.sin(t * 0.25) * 0.05;
    scene.rotation.x = cur.y * 0.08 + sc * 0.22;

    if (web.visible) {
      phone.position.y = -0.15 + Math.sin(t * 1.3) * 0.07; mon.position.y = 0.15 + Math.sin(t * 1.1 + 1) * 0.05;
      // a new booking leaves the phone every 3 seconds and reaches the dashboard 1.4s later
      const period = 3, k = Math.floor(t / period), ph = t - k * period;
      if (k > lastSent) { lastSent = k; }
      pkts.forEach((p, i) => { const u = (ph - i * 0.12) / 1.4; p.visible = u > 0 && u < 1; if (p.visible) p.position.copy(curve.getPointAt(Math.min(1, u))); p.scale.setScalar(i === 0 ? 1 : 0.6); });
      if (ph >= 1.4 && k > lastArrive) { lastArrive = k; bookings++; revenue += 0.5 + Math.random(); if (k % 2) orders++; flashAt = t; feed.unshift(['New booking', NAMES[k % NAMES.length], '#E5372B']); feed.length = 4; }
      drawPhone(t, k * period); drawDash(t);
      tubeMat.opacity = 0.55 + Math.sin(t * 4) * 0.15;
    }
    if (it.visible) {
      lap.position.y = -1.05 + Math.sin(t * 1.2) * 0.07;
      itChips.forEach(s => { const a = s.userData.a + t * 0.32; s.position.set(Math.cos(a) * 3.1, s.userData.y + Math.sin(t * 1.4 + s.userData.a) * 0.1 - 0.3, Math.sin(a) * 1.9); s.material.opacity = 0.5 + 0.5 * (Math.sin(a) + 1) / 2; });
      ring.rotation.z = t * 0.1; drawLaptop(t);
    }
    dust.rotation.y = t * 0.015;
    renderer.render(scene, camera);
  }

  let visible = true, running = false;
  function wake() { if (running || reduceMotion) { if (reduceMotion) frame(performance.now() + 4000); return; } running = true; const tick = now => { if (!visible || document.hidden) { running = false; return; } frame(now); requestAnimationFrame(tick); }; requestAnimationFrame(tick); }
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) wake(); }).observe(host);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) wake(); });
  window.__hero3dFrame = frame;
  visual.classList.add('is-3d');
  if (reduceMotion) frame(t0 + 4000); else wake();
}
