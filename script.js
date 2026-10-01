document.querySelector('.burger')?.addEventListener('click', () => {
  document.querySelector('nav').classList.toggle('open');
});

// Formlar mailto ile e-posta uygulamasını açar (sunucu gerektirmez).
// Alıcı adres build.py içindeki EMAIL alanından gelir (window.HAN_MAIL).
function wire(id, subject) {
  const form = document.getElementById(id);
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const body = [...d.entries()].map(([k, v]) => `${k}: ${v}`).join('\n');
    location.href = 'mailto:' + (window.HAN_MAIL || '') +
      '?subject=' + encodeURIComponent(subject + ' - ' + (d.get('Waste type') || d.get('Organisation') || '')) +
      '&body=' + encodeURIComponent(body);
    form.querySelector('.ok').style.display = 'block';
  });
}
wire('teklif', 'Teklif Talebi / Quote Request');
wire('sponsor', 'Sponsorluk Başvurusu / Sponsorship Request');
