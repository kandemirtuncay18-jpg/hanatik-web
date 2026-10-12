// Ana sayfa sahnesi: hero.mp4 kendiliğinden oynar, videonun aşamasına göre ilgili yazı görünür.
(function () {
  const sec = document.getElementById('sahne');
  if (!sec) return;
  const video = sec.querySelector('.sc-video');
  const steps = sec.querySelectorAll('.sc-step');
  const bar = sec.querySelector('.sc-bar i');
  // her aşamanın başladığı video oranları (hero.mp4 sahne sınırları)
  const B = [0, 0.18, 0.41, 0.59, 0.75, 0.89, 1];
  let cur = -1;

  function update() {
    const q = video.duration ? video.currentTime / video.duration : 0;
    let idx = 0;
    while (idx < steps.length - 1 && q >= B[idx + 1]) idx++;
    if (idx !== cur) { cur = idx; steps.forEach((el, k) => el.classList.toggle('on', k === idx)); }
    if (bar) bar.style.width = (q * 100).toFixed(1) + '%';
  }

  video.addEventListener('timeupdate', update);
  (function tick() { update(); requestAnimationFrame(tick); })();
  update();
})();
