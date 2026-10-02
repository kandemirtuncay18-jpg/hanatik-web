document.querySelector('.burger')?.addEventListener('click', () => {
  document.querySelector('nav').classList.toggle('open');
});

// Formlar: content/site.json içindeki form_key (Web3Forms) doluysa doğrudan e-postaya gönderilir,
// boşsa kullanıcının e-posta uygulaması (mailto) açılır.
const LANG = document.documentElement.lang;
const MSG = {
  tr: { ok: 'Talebiniz alındı. En kısa sürede dönüş yapacağız. Teşekkürler!', err: 'Gönderilemedi. Lütfen telefonla ulaşın veya daha sonra tekrar deneyin.', wait: 'Gönderiliyor…' },
  en: { ok: 'Your request has been received. We will get back to you shortly. Thank you!', err: 'Could not send. Please call us or try again later.', wait: 'Sending…' },
}[LANG] || {};

function wire(id, subject) {
  const form = document.getElementById(id);
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const ok = form.querySelector('.ok');
    const btn = form.querySelector('button[type=submit]');
    const title = subject + ' - ' + (d.get('Waste type') || d.get('Organisation') || '');

    if (window.HAN_FORM_KEY) {
      const label = btn.textContent;
      btn.disabled = true; btn.textContent = MSG.wait;
      try {
        const payload = Object.fromEntries(d.entries());
        payload.access_key = window.HAN_FORM_KEY;
        payload.subject = title;
        payload.from_name = 'HAN ATIK Web';
        const res = await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(payload),
        });
        const json = await res.json();
        if (!json.success) throw new Error(json.message);
        ok.textContent = MSG.ok; ok.className = 'ok'; ok.style.display = 'block';
        form.reset();
      } catch (err) {
        ok.textContent = MSG.err; ok.className = 'ok bad'; ok.style.display = 'block';
      } finally {
        btn.disabled = false; btn.textContent = label;
      }
      return;
    }

    const body = [...d.entries()].map(([k, v]) => `${k}: ${v}`).join('\n');
    location.href = 'mailto:' + (window.HAN_MAIL || '') +
      '?subject=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
    ok.style.display = 'block';
  });
}
wire('teklif', 'Teklif Talebi / Quote Request');
wire('sponsor', 'Sponsorluk Başvurusu / Sponsorship Request');
