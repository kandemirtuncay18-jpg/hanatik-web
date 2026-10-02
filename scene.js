// Ana sayfa sahnesi: video kareleri kaydırmaya bağlı oynar, her aşamada ilgili yazı görünür.
// Kareler assets/scene/ içindedir (build.py window.HAN_SCENE'e yazar).
(function () {
  const sec = document.getElementById('sahne');
  const files = window.HAN_SCENE || [];
  if (!sec || !files.length || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const canvas = sec.querySelector('.sc-canvas');
  const ctx = canvas.getContext('2d');
  const steps = sec.querySelectorAll('.sc-step');
  const intro = sec.querySelector('.sc-intro');
  const bar = sec.querySelector('.sc-bar i');
  const N = steps.length;
  const INTRO = 0.12;                              // ilk %12: başlık
  // her aşamanın karşılık geldiği kare oranları (videodaki sahne sınırları)
  const B = [0, 0.18, 0.41, 0.59, 0.75, 0.89, 1];
  let W = 0, H = 0, p = 0, visible = false;

  const imgs = files.map((src) => { const im = new Image(); im.decoding = 'async'; im.src = src; return im; });
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function drawFrame(im, alpha) {
    if (!im || !im.complete || !im.naturalWidth) return false;
    const r = Math.max(W / im.naturalWidth, H / im.naturalHeight);
    const w = im.naturalWidth * r, h = im.naturalHeight * r;
    ctx.globalAlpha = alpha;
    ctx.drawImage(im, (W - w) / 2, (H - h) / 2, w, h);
    ctx.globalAlpha = 1;
    return true;
  }

  // ilerleme (0..1) -> video konumu (0..1), aşama başına eşit kaydırma
  function videoPos(q) {
    const s = clamp(Math.floor(q * N), 0, N - 1), local = q * N - s;
    return B[s] + (B[s + 1] - B[s]) * clamp(local, 0, 1);
  }

  function render() {
    const r = sec.getBoundingClientRect();
    p = clamp(-r.top / (r.height - innerHeight), 0, 1);
    const q = clamp((p - INTRO) / (1 - INTRO), 0, 1);
    const pos = videoPos(q) * (imgs.length - 1);
    const i = Math.floor(pos), f = pos - i;
    ctx.clearRect(0, 0, W, H);
    // en yakın yüklü kareyi bul (yükleme sürerken boşluk kalmasın)
    let a = i; while (a > 0 && !(imgs[a].complete && imgs[a].naturalWidth)) a--;
    drawFrame(imgs[a], 1);
    if (f > 0.02 && i + 1 < imgs.length) drawFrame(imgs[i + 1], f);     // kareler arası yumuşak geçiş

    intro.style.opacity = String(clamp(1 - p / (INTRO * 0.8), 0, 1));
    intro.style.pointerEvents = p < INTRO * 0.8 ? 'auto' : 'none';
    const idx = p < INTRO ? -1 : clamp(Math.floor(q * N), 0, N - 1);
    steps.forEach((el, k) => el.classList.toggle('on', k === idx));
    if (bar) bar.style.width = (q * 100).toFixed(1) + '%';
  }

  function loop() {
    if (!visible) return;
    render();
    requestAnimationFrame(loop);
  }

  new IntersectionObserver((e) => {
    visible = e[0].isIntersecting;
    if (visible) requestAnimationFrame(loop);
  }, { rootMargin: '100px' }).observe(sec);
  addEventListener('resize', () => { resize(); render(); });
  resize();
  render();
})();
