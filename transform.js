// Dönüşüm bölümü: kaydırmaya bağlı canvas animasyonu (atık -> ayrıştırma -> geri kazanım).
// assets/frames/ içine kare dizisi (AI video kareleri) konursa parçacıklar yerine o kareler oynatılır.
(function () {
  const sec = document.getElementById('donusum');
  if (!sec || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const canvas = sec.querySelector('.tf-canvas');
  const ctx = canvas.getContext('2d');
  const stages = sec.querySelectorAll('.tf-stage');
  const dots = sec.querySelectorAll('.tf-dots span');
  const smooth = (t) => { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); };
  const lerp = (a, b, t) => a + (b - a) * t;
  let W = 0, H = 0, parts = [], p = 0, visible = false;

  // --- kare dizisi modu ---
  const frames = (window.HAN_FRAMES || []).map((src) => { const im = new Image(); im.decoding = 'async'; im.dataset.src = src; return im; });
  let framesLoading = false;
  function loadFrames() {
    if (framesLoading) return;
    framesLoading = true;
    frames.forEach((im) => { im.src = im.dataset.src; });
  }

  // --- hedef şekil: halka + ok ucu + yaprak (alfa örnekleme) ---
  function shapePoints(n) {
    const S = 300, o = document.createElement('canvas');
    o.width = o.height = S;
    const c = o.getContext('2d');
    c.fillStyle = '#000'; c.strokeStyle = '#000'; c.lineWidth = 26; c.lineCap = 'round';
    c.beginPath(); c.arc(S / 2, S / 2, 118, 0.15 * Math.PI, 1.85 * Math.PI); c.stroke();
    const ex = S / 2 + 118 * Math.cos(1.85 * Math.PI), ey = S / 2 + 118 * Math.sin(1.85 * Math.PI);
    c.beginPath(); c.moveTo(ex - 14, ey - 24); c.lineTo(ex + 34, ey - 4); c.lineTo(ex - 6, ey + 34); c.fill();
    c.save(); c.translate(S / 2, S / 2 + 8); c.rotate(-0.6);
    c.beginPath(); c.ellipse(0, 0, 34, 78, 0, 0, Math.PI * 2); c.fill(); c.restore();
    const d = c.getImageData(0, 0, S, S).data, pts = [];
    for (let y = 0; y < S; y += 3) for (let x = 0; x < S; x += 3) if (d[(y * S + x) * 4 + 3] > 128) pts.push([x / S - 0.5, y / S - 0.5]);
    for (let i = pts.length - 1; i > 0; i--) { const j = (Math.random() * (i + 1)) | 0; [pts[i], pts[j]] = [pts[j], pts[i]]; }
    const out = [];
    for (let i = 0; i < n; i++) out.push(pts[i % pts.length]);
    return out;
  }

  const CATS = ['#7c6a58', '#8a8f94', '#b99a6b', '#5d7a6a'];
  const GREENS = ['#4ade80', '#65a30d', '#22c55e', '#a3e635'];
  const hexToRgb = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const FROM = CATS.map(hexToRgb), TO = GREENS.map(hexToRgb);

  function build() {
    const n = innerWidth < 700 ? 520 : 1100, target = shapePoints(n);
    const size = Math.min(W, H) * 0.62, cx = W / 2, cy = H * 0.47;
    parts = [];
    for (let i = 0; i < n; i++) {
      const cat = i % 4, k = (i / 4) | 0, cols = 10;
      parts.push({
        ax: Math.random() * W, ay: Math.random() * H, ph: Math.random() * 6.28, sp: 0.4 + Math.random() * 0.8,
        bx: W * (0.14 + cat * 0.24) + (k % cols) * 11 - cols * 5.5, by: H * 0.28 + ((k / cols) | 0) * 9,
        cx: cx + target[i][0] * size, cy: cy + target[i][1] * size,
        cat, rot: Math.random() * 6.28, w: 5 + Math.random() * 6, h: 3 + Math.random() * 4,
      });
    }
  }

  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!frames.length) build();
  }

  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    if (frames.length) {
      const im = frames[Math.min(frames.length - 1, Math.floor(p * frames.length))];
      if (im.complete && im.naturalWidth) {
        const r = Math.max(W / im.naturalWidth, H / im.naturalHeight), w = im.naturalWidth * r, h = im.naturalHeight * r;
        ctx.globalAlpha = 0.55; ctx.drawImage(im, (W - w) / 2, (H - h) / 2, w, h); ctx.globalAlpha = 1;
      }
      return;
    }
    const sort = smooth((p - 0.28) / 0.28), form = smooth((p - 0.62) / 0.28);
    for (const q of parts) {
      const fx = Math.sin(t * q.sp + q.ph) * 18 * (1 - sort), fy = Math.cos(t * q.sp + q.ph) * 14 * (1 - sort);
      let x = lerp(q.ax + fx, q.bx, sort), y = lerp(q.ay + fy, q.by, sort);
      x = lerp(x, q.cx, form); y = lerp(y, q.cy, form);
      const a = FROM[q.cat], b = TO[q.cat];
      ctx.fillStyle = `rgb(${lerp(a[0], b[0], form) | 0},${lerp(a[1], b[1], form) | 0},${lerp(a[2], b[2], form) | 0})`;
      if (form > 0.55) {
        ctx.beginPath(); ctx.arc(x, y, lerp(q.w * 0.5, 2.6, form), 0, 6.283); ctx.fill();
      } else {
        ctx.save(); ctx.translate(x, y); ctx.rotate(q.rot * (1 - sort) + t * 0.2 * (1 - sort));
        ctx.fillRect(-q.w / 2, -q.h / 2, q.w, q.h); ctx.restore();
      }
    }
  }

  function update() {
    const r = sec.getBoundingClientRect();
    p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight)));
    sec.style.setProperty('--p', p.toFixed(3));
    const idx = Math.min(stages.length - 1, Math.floor(p * stages.length));
    stages.forEach((el, i) => el.classList.toggle('on', i === idx));
    dots.forEach((el, i) => el.classList.toggle('on', i <= idx));
  }

  function loop(t) {
    if (!visible) return;
    update(); draw(t / 1000);
    requestAnimationFrame(loop);
  }

  new IntersectionObserver((e) => {
    visible = e[0].isIntersecting;
    if (visible) { if (frames.length) loadFrames(); requestAnimationFrame(loop); }
  }, { rootMargin: '200px' }).observe(sec);
  addEventListener('resize', resize);
  resize();
  update();
})();
