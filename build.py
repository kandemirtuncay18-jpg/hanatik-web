#!/usr/bin/env python3
"""HAN ATIK A.Ş. site üretici (TR kökte, EN /en/ altında).

Çalıştır:  python build.py
Aşağıdaki CONFIG alanlarını gerçek bilgilerle doldurup tekrar çalıştırın.
"""
import json
import pathlib
import urllib.parse

# ===================== CONFIG (burayı doldurun) =====================
SITE_URL = "https://kandemirtuncay18-jpg.github.io/hanatik-web"      # yayın adresi (sonunda / yok); GitHub Pages ise onun adresi
PHONE = ""                               # örn. "+90 212 000 00 00"
EMAIL = ""                               # örn. "info@hanatik.com.tr"
ADDRESS = ""                             # örn. "Organize Sanayi Bölgesi, 1. Cadde No:5, Gebze/Kocaeli"
HOURS_TR = "Pzt–Cmt 08:30–18:00"
HOURS_EN = "Mon–Sat 08:30–18:00"
FOUNDED = ""                             # örn. "2015"
MAPS_QUERY = ""                          # boşsa ADDRESS kullanılır. Google Maps'te arattığınız ifade
# ====================================================================

OUT = pathlib.Path(__file__).parent
NAME = "HAN ATIK A.Ş."
FULL = "HAN ATIK YÖNETİMİ ÇEVRE İNŞAAT SANAYİ VE TİCARET ANONİM ŞİRKETİ"
FULL_EN = "HAN WASTE MANAGEMENT ENVIRONMENT CONSTRUCTION INDUSTRY AND TRADE INC."

PAGES = ["index", "hizmetler", "hakkimizda", "belgeler", "sponsorluk", "iletisim", "kvkk"]
EN_SLUG = {"index": "index", "hizmetler": "services", "hakkimizda": "about",
           "belgeler": "certificates", "sponsorluk": "sponsorship",
           "iletisim": "contact", "kvkk": "privacy"}
NAV_KEYS = ["index", "hizmetler", "hakkimizda", "belgeler", "sponsorluk", "iletisim"]


def slug(key, lang):
    return f"{EN_SLUG[key] if lang == 'en' else key}.html"


def asset(name):
    return (OUT / "assets" / name).exists()


def gallery_files():
    return sorted(f.name for f in (OUT / "assets").glob("gallery-*") if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"))


def build_lang(lang):
    en = lang == "en"
    T = lambda tr, e: e if en else tr
    root = "../" if en else ""
    PH = lambda tr, e=None: f'<span class="placeholder">[{T(tr, e or tr)}]</span>'

    phone = PHONE or PH("telefon", "phone")
    email = EMAIL or PH("e-posta", "e-mail")
    addr = ADDRESS or PH("adres", "address")
    hours = T(HOURS_TR, HOURS_EN)
    full = FULL_EN if en else FULL
    tel_href = "tel:" + "".join(c for c in PHONE if c.isdigit() or c == "+") if PHONE else slug("iletisim", lang)
    sub_to = EMAIL or "info@hanatik.com.tr"

    def link(k):
        return slug(k, lang)

    def card(ic, t, p="", cls=""):
        return f'<div class="card {cls}"><div class="ic">{ic}</div><h3>{t}</h3><p>{p}</p></div>'

    def hero(h1, p, badge=None):
        b = f'<span class="badge">{badge}</span>' if badge else ""
        return f'<div class="hero page-hero"><div class="wrap">{b}<h1>{h1}</h1><p>{p}</p></div></div>'

    band = f"""<section class="band"><div class="wrap">
<h2>{T("Atık probleminizi birlikte çözelim", "Let's solve your waste challenge together")}</h2>
<p>{T("Atık türünüzü ve miktarınızı bildirin, size uygun nakliye ve bertaraf çözümüyle dönelim.",
      "Tell us your waste type and volume and we will come back with the right transport and disposal solution.")}</p>
<a class="btn btn-primary" href="{link('iletisim')}#teklif">{T("Ücretsiz Teklif Alın", "Get a Free Quote")}</a></div></section>"""

    # ---------------- sayfa gövdeleri ----------------
    bodies = {}

    has_vid = asset("hero.mp4")
    poster = f' poster="{root}assets/hero.jpg"' if asset("hero.jpg") else ""
    vid = (f'<video class="hero-video" autoplay muted loop playsinline preload="metadata"{poster} aria-hidden="true">'
           f'<source src="{root}assets/hero.mp4" type="video/mp4"></video>') if has_vid else ""
    home_hero = f"""<div class="hero{' has-video' if has_vid else ''}">{vid}<div class="wrap">
<span class="badge">{T("Tehlikeli &amp; Tehlikesiz Atık Çözümleri", "Hazardous &amp; Non-Hazardous Waste Solutions")}</span>
<h1>{T("Atıklarınız güvenli ellerde: toplama, nakliye, bertaraf.", "Your waste in safe hands: collection, transport, disposal.")}</h1>
<p>{T(f"{NAME}, sanayi, sağlık ve inşaat sektörlerine mevzuata uygun atık nakliyesi ve atık yönetimi hizmeti sunar.",
      "HAN ATIK provides compliant waste transportation and waste management services to industry, healthcare and construction.")}</p>
<div class="btns"><a class="btn btn-primary" href="{link('iletisim')}#teklif">{T("Teklif Al", "Get a Quote")}</a>
<a class="btn btn-ghost" href="{link('hizmetler')}">{T("Hizmetlerimiz", "Our Services")}</a></div></div></div>
<div class="strip"><div class="wrap">
<div>🚛 {T("ADR Uyumlu Nakliye", "ADR-Compliant Transport")}<small>{T("Tehlikeli madde taşımacılığı", "Dangerous goods haulage")}</small></div>
<div>📋 {T("Mevzuata Uygun", "Regulation Compliant")}<small>{T("Atık takip ve raporlama", "Waste tracking and reporting")}</small></div>
<div>🛡️ {T("İş Sağlığı &amp; Güvenliği", "Health &amp; Safety")}<small>{T("Eğitimli ekip", "Trained crew")}</small></div>
<div>🌍 {T("Çevreye Duyarlı", "Eco-Conscious")}<small>{T("Geri kazanım odaklı", "Recovery-focused")}</small></div></div></div>"""

    steps = [(T("Talep", "Request"), T("Atık türü ve miktarı bildirilir.", "Waste type and volume are reported.")),
             (T("Analiz", "Analysis"), T("Atık sınıflandırılır, kod belirlenir.", "Waste is classified and coded.")),
             (T("Toplama", "Collection"), T("Uygun ambalaj ve araçla toplanır.", "Collected with suitable packaging and vehicles.")),
             (T("Nakliye", "Transport"), T("Güvenli taşıma ve takip.", "Safe transport with tracking.")),
             (T("Bertaraf", "Disposal"), T("Lisanslı tesiste bertaraf/geri kazanım ve raporlama.", "Disposal/recovery at a licensed facility, with reporting."))]
    steps_html = "".join(card("", a, b, "step") for a, b in steps)

    gl = gallery_files()
    gallery = (f'''<section><div class="wrap"><span class="eyebrow">{T("Galeri", "Gallery")}</span><h2>{T("Çalışmalarımızdan", "From our work")}</h2>
<div class="gallery">{"".join(f'<img src="{root}assets/{g}" alt="{NAME} - {T("atık yönetimi", "waste management")}" loading="lazy">' for g in gl)}</div></div></section>''') if gl else ""

    bodies["index"] = (home_hero, f"""
<section><div class="wrap">
<span class="eyebrow">{T("Hizmetlerimiz", "Our Services")}</span><h2>{T("Uçtan uca atık yönetimi", "End-to-end waste management")}</h2>
<p class="lead">{T("Atığın oluştuğu yerden nihai bertaraf veya geri kazanım tesisine kadar tüm süreci tek çatı altında yönetiyoruz.",
                   "We manage the whole chain, from the point where waste is generated to the final disposal or recovery facility.")}</p>
<div class="grid g3">
{card("☣️", T("Tehlikeli Atık Yönetimi", "Hazardous Waste Management"), T("Kimyasal, yağlı, boyalı ve diğer tehlikeli atıkların güvenli toplanması, ambalajlanması ve bertarafı.", "Safe collection, packaging and disposal of chemical, oily, paint-related and other hazardous waste."), "danger")}
{card("🗑️", T("Tehlikesiz Atık Yönetimi", "Non-Hazardous Waste Management"), T("Endüstriyel, ambalaj, inşaat-yıkıntı ve evsel nitelikli atıkların düzenli toplanması ve taşınması.", "Regular collection and transport of industrial, packaging, construction and household-type waste."), "safe")}
{card("🚛", T("Atık Nakliyesi (ADR)", "Waste Transport (ADR)"), T("Lisanslı araçlarla ve eğitimli sürücülerle tehlikeli ve tehlikesiz atık taşımacılığı.", "Hazardous and non-hazardous waste haulage with licensed vehicles and trained drivers."))}
{card("♻️", T("Geri Dönüşüm &amp; Geri Kazanım", "Recycling &amp; Recovery"), T("Kâğıt, plastik, metal, yağ ve diğer atıkların ekonomiye yeniden kazandırılması.", "Returning paper, plastic, metal, oil and other waste streams to the economy."))}
{card("🏗️", T("İnşaat &amp; Hafriyat Atıkları", "Construction &amp; Excavation Waste"), T("Şantiyelerden çıkan inşaat ve yıkıntı atıklarının yönetimi ve nakliyesi.", "Management and transport of construction and demolition waste from sites."))}
{card("📑", T("Danışmanlık &amp; Raporlama", "Consulting &amp; Reporting"), T("Atık envanteri, beyan sistemi, mevzuat uyumu ve denetim hazırlığı desteği.", "Waste inventory, declaration system, regulatory compliance and audit preparation."))}
</div></div></section>

<section class="alt"><div class="wrap">
<span class="eyebrow">{T("Çalışma Süreci", "How We Work")}</span><h2>{T("5 adımda güvenli atık yönetimi", "Safe waste management in 5 steps")}</h2>
<p class="lead">{T("Şeffaf ve izlenebilir bir süreç yürütüyoruz.", "A transparent and traceable process.")}</p>
<div class="grid steps" style="grid-template-columns:repeat(auto-fit,minmax(180px,1fr))">{steps_html}</div></div></section>

<section><div class="wrap">
<span class="eyebrow">{T("Sektörler", "Industries")}</span><h2>{T("Hizmet verdiğimiz alanlar", "Sectors we serve")}</h2>
<div class="grid g4" style="margin-top:24px">
{card("🏭", T("Sanayi", "Industry"), T("Fabrika ve üretim tesisleri", "Factories and production sites"))}
{card("🏥", T("Sağlık", "Healthcare"), T("Hastane ve klinikler", "Hospitals and clinics"))}
{card("🏗️", T("İnşaat", "Construction"), T("Şantiye ve altyapı projeleri", "Building sites and infrastructure"))}
{card("⚗️", T("Kimya &amp; Enerji", "Chemicals &amp; Energy"), T("Kimyasal ve enerji tesisleri", "Chemical and energy plants"))}
</div></div></section>

<section class="alt"><div class="wrap">
<span class="eyebrow">{T("SSS", "FAQ")}</span><h2>{T("Sık sorulan sorular", "Frequently asked questions")}</h2>
<details><summary>{T("Tehlikeli atık ile tehlikesiz atık arasındaki fark nedir?", "What is the difference between hazardous and non-hazardous waste?")}</summary><p>{T("Tehlikeli atıklar insan sağlığı ve çevre için risk taşıyan (zehirli, yanıcı, aşındırıcı vb.) özelliklere sahiptir ve özel izin, ambalaj ve taşıma koşulları gerektirir. Tehlikesiz atıklar bu özellikleri taşımaz.", "Hazardous waste has properties that endanger health or the environment (toxic, flammable, corrosive, etc.) and needs special permits, packaging and transport conditions. Non-hazardous waste does not.")}</p></details>
<details><summary>{T("Atığımın tehlikeli olup olmadığını nasıl öğrenirim?", "How do I know if my waste is hazardous?")}</summary><p>{T("Atık kodu (Atık Yönetimi Yönetmeliği listesi) ve gerekirse laboratuvar analizi ile belirlenir. Ekibimiz bu konuda size yardımcı olur.", "It is determined by the waste code (list in the Waste Management Regulation) and, where needed, laboratory analysis. Our team will help you with this.")}</p></details>
<details><summary>{T("Teklif nasıl alabilirim?", "How can I get a quote?")}</summary><p>{T("İletişim sayfasındaki formu doldurmanız veya bizi aramanız yeterlidir.", "Just fill in the form on the contact page or call us.")}</p></details>
</div></section>
{gallery}{band}""")

    bodies["hizmetler"] = (hero(T("Hizmetlerimiz", "Our Services"), T("Atığın oluştuğu yerden bertaraf tesisine kadar eksiksiz çözümler.", "Complete solutions from the point of generation to the disposal facility.")), f"""
<section><div class="wrap"><div class="grid g2">
<div class="card danger"><div class="ic">☣️</div><h3>{T("Tehlikeli Atık Hizmetleri", "Hazardous Waste Services")}</h3>
<p>{T("Risk taşıyan atıklar için güvenli ve izlenebilir çözümler.", "Safe and traceable solutions for waste that carries risk.")}</p>
<ul>{"".join(f"<li>{x}</li>" for x in T(
 ["Atık yağlar, solventler, boya ve vernik atıkları", "Kimyasal ve laboratuvar atıkları", "Kirli ambalaj, filtre, emici malzemeler", "Akü ve pil atıkları", "Tıbbi atık (ilgili izinler kapsamında)", "Etiketleme, ambalajlama ve geçici depolama danışmanlığı"],
 ["Waste oils, solvents, paint and varnish waste", "Chemical and laboratory waste", "Contaminated packaging, filters and absorbents", "Battery and accumulator waste", "Medical waste (within applicable permits)", "Labelling, packaging and temporary storage consulting"]))}</ul></div>
<div class="card safe"><div class="ic">🗑️</div><h3>{T("Tehlikesiz Atık Hizmetleri", "Non-Hazardous Waste Services")}</h3>
<p>{T("Düzenli toplama ve ekonomik taşıma çözümleri.", "Regular collection and economical transport solutions.")}</p>
<ul>{"".join(f"<li>{x}</li>" for x in T(
 ["Kâğıt, karton, plastik, cam, metal atıklar", "Ahşap ve palet atıkları", "İnşaat ve yıkıntı atıkları", "Endüstriyel proses atıkları", "Konteyner ve kompaktör kiralama", "Periyodik toplama programları"],
 ["Paper, cardboard, plastic, glass and metal waste", "Wood and pallet waste", "Construction and demolition waste", "Industrial process waste", "Container and compactor rental", "Scheduled collection programmes"]))}</ul></div>
<div class="card"><div class="ic">🚛</div><h3>{T("Atık Nakliyesi", "Waste Transport")}</h3>
<ul>{"".join(f"<li>{x}</li>" for x in T(
 ["ADR kapsamında tehlikeli madde taşımacılığı", "Eğitimli ve belgeli sürücüler", "Araç takip ve sevkiyat izleme", "Atık taşıma formu ve evrak yönetimi"],
 ["Dangerous goods transport under ADR", "Trained and certified drivers", "Vehicle tracking and shipment monitoring", "Waste transport forms and paperwork"]))}</ul></div>
<div class="card"><div class="ic">♻️</div><h3>{T("Geri Dönüşüm &amp; Bertaraf", "Recycling &amp; Disposal")}</h3>
<ul>{"".join(f"<li>{x}</li>" for x in T(
 ["Lisanslı geri kazanım ve bertaraf tesislerine sevkiyat", "Enerji geri kazanımı ve ara depolama çözümleri", "Bertaraf sertifikası ve raporlama"],
 ["Delivery to licensed recovery and disposal facilities", "Energy recovery and interim storage solutions", "Disposal certificates and reporting"]))}</ul></div>
<div class="card"><div class="ic">📑</div><h3>{T("Danışmanlık", "Consulting")}</h3>
<ul>{"".join(f"<li>{x}</li>" for x in T(
 ["Atık envanteri ve sınıflandırma", "Atık beyan sistemi desteği", "Mevzuat uyum ve denetim hazırlığı", "Personel farkındalık eğitimleri"],
 ["Waste inventory and classification", "Waste declaration system support", "Regulatory compliance and audit preparation", "Staff awareness training"]))}</ul></div>
<div class="card"><div class="ic">🚨</div><h3>{T("Acil Müdahale", "Emergency Response")}</h3>
<ul>{"".join(f"<li>{x}</li>" for x in T(
 ["Dökülme ve sızıntı müdahalesi", "Kontamine alan temizliği", "7/24 acil hat"],
 ["Spill and leak response", "Contaminated site clean-up", "24/7 emergency line"]))}</ul></div>
</div></div></section>{band}""")

    bodies["hakkimizda"] = (hero(T("Hakkımızda", "About Us"), T("Güvenli, şeffaf ve sürdürülebilir atık yönetimi.", "Safe, transparent and sustainable waste management.")), f"""
<section><div class="wrap"><div class="grid g2">
<div><span class="eyebrow">{T("Biz Kimiz", "Who We Are")}</span><h2>{NAME}</h2>
<p>{full}, {T("atık yönetimi, çevre ve inşaat alanlarında hizmet veren bir şirkettir.", "is a company operating in waste management, environment and construction.")}
{(T("Kuruluş yılı: ", "Founded: ") + FOUNDED) if FOUNDED else PH("kuruluş yılı", "founding year")}</p>
<p style="margin-top:12px">{T("Amacımız; müşterilerimizin atıklarını mevzuata uygun, güvenli ve çevreye zarar vermeden yönetmek ve mümkün olduğunca ekonomiye yeniden kazandırmaktır.", "Our aim is to manage our customers' waste in compliance with regulations, safely and without harming the environment, and to return as much of it as possible to the economy.")}</p></div>
<div class="grid" style="gap:14px">
{card("🎯", T("Misyonumuz", "Our Mission"), T("Sürdürülebilir, güvenli ve şeffaf atık yönetimi sunmak.", "To deliver sustainable, safe and transparent waste management."))}
{card("👁️", T("Vizyonumuz", "Our Vision"), T("Bölgemizin güvenilir ve tercih edilen çevre hizmetleri şirketi olmak.", "To be the trusted, preferred environmental services company in our region."))}
</div></div></div></section>
<section class="alt"><div class="wrap"><span class="eyebrow">{T("Değerlerimiz", "Our Values")}</span><h2>{T("Nasıl çalışıyoruz", "How we work")}</h2>
<div class="grid g4" style="margin-top:24px">
{card("🛡️", T("Güvenlik", "Safety"), T("İş sağlığı ve güvenliği her işin önünde gelir.", "Health and safety come before every job."))}
{card("📋", T("Uyumluluk", "Compliance"), T("Mevzuata tam uyum ve belgelendirme.", "Full regulatory compliance and documentation."))}
{card("🌍", T("Çevre", "Environment"), T("Önce azaltma, sonra geri kazanım.", "Reduce first, then recover."))}
{card("🤝", T("Güven", "Trust"), T("Şeffaf süreç, zamanında hizmet.", "Transparent process, on-time service."))}
</div></div></section>{band}""")

    docs = [("📜", T("Atık Toplama/Taşıma Lisansı", "Waste Collection/Transport Licence")), ("🏛️", T("Çevre İzin ve Lisans Belgesi", "Environmental Permit & Licence")),
            ("🚛", "ADR / SRC"), ("✅", "ISO 14001"), ("🦺", "ISO 45001"), ("⭐", "ISO 9001")]
    bodies["belgeler"] = (hero(T("Belgeler &amp; Lisanslar", "Certificates &amp; Licences"), T("Yetkili ve belgeli hizmet anlayışı.", "Authorised and documented service.")), f"""
<section><div class="wrap">
<span class="eyebrow">{T("Lisans &amp; Belgeler", "Licences &amp; Certificates")}</span><h2>{T("Yetkilerimiz ve belgelerimiz", "Our authorisations and certificates")}</h2>
<p class="lead">{T("Atık sektöründe güven, belgelerle başlar. Aşağıdaki alanlar şirket belgeleri hazır olduğunda doldurulacaktır.", "In the waste sector, trust starts with documents. The fields below will be completed once the company documents are ready.")}</p>
<div class="grid g3">{"".join(card(i, t, PH("belge no / geçerlilik tarihi", "document no. / validity")) for i, t in docs)}</div></div></section>{band}""")

    sp = [("⚽", T("Spor", "Sports"), T("Yerel spor kulüplerine ve amatör takımlara destek.", "Support for local sports clubs and amateur teams.")),
          ("🌳", T("Çevre &amp; Doğa", "Environment &amp; Nature"), T("Ağaçlandırma, kıyı/doğa temizliği ve sıfır atık projeleri.", "Tree planting, shoreline/nature clean-ups and zero-waste projects.")),
          ("🎓", T("Eğitim", "Education"), T("Okullarda atık ayrıştırma ve çevre bilinci eğitimleri.", "Waste-separation and environmental awareness training at schools.")),
          ("🤲", T("Toplum", "Community"), T("Yerel etkinlik, dernek ve sosyal sorumluluk projeleri.", "Local events, associations and social responsibility projects."))]
    bodies["sponsorluk"] = (hero(T("Sponsorluk &amp; Toplumsal Destek", "Sponsorship &amp; Community Support"), T("Çevreyi ve yaşadığımız toplumu destekliyoruz.", "We support the environment and the community we live in.")), f"""
<section><div class="wrap">
<span class="eyebrow">{T("Destek Alanlarımız", "Areas of Support")}</span><h2>{T("Sponsorluk anlayışımız", "Our sponsorship approach")}</h2>
<p class="lead">{T("Çevre odaklı, topluma fayda sağlayan etkinlik ve kuruluşlara sponsor olmayı hedefliyoruz.", "We aim to sponsor events and organisations that are environment-focused and benefit the community.")}</p>
<div class="grid g4">{"".join(card(*x) for x in sp)}</div></div></section>
<section class="alt"><div class="wrap"><div class="grid g2">
<div><span class="eyebrow">{T("Sponsorluk Başvurusu", "Sponsorship Request")}</span><h2>{T("Projenizi bize anlatın", "Tell us about your project")}</h2>
<p class="lead" style="margin-bottom:0">{T("Kulüp, dernek, okul veya etkinlik organizatörüyseniz başvuru formunu doldurun. Başvurular değerlendirilir ve size dönüş yapılır.", "If you are a club, association, school or event organiser, fill in the form. Requests are reviewed and we will get back to you.")}</p></div>
<form id="sponsor">
<label>{T("Kurum / Kulüp Adı", "Organisation")}<input name="Organisation" required></label>
<div class="row"><label>{T("Yetkili Kişi", "Contact person")}<input name="Contact" required></label>
<label>{T("Telefon / E-posta", "Phone / e-mail")}<input name="Contact info" required></label></div>
<label>{T("Etkinlik / Proje ve Talep", "Event / project and request")}<textarea name="Details" rows="4" required></textarea></label>
<button class="btn btn-green" type="submit">{T("Başvuru Gönder", "Send Request")}</button>
<div class="ok">{T("Başvurunuz e-posta uygulamanızda hazırlandı. Teşekkürler!", "Your request has been prepared in your e-mail app. Thank you!")}</div>
</form></div></div></section>
<section><div class="wrap"><span class="eyebrow">{T("İş Ortakları", "Partners")}</span><h2>{T("Referanslar ve iş ortakları", "References and partners")}</h2>
<p class="lead">{T("Çalıştığımız kurumların logoları izinleri alındıktan sonra burada yer alacaktır.", "Logos of the organisations we work with will appear here once permission is obtained.")} {PH("logolar", "logos")}</p></div></section>""")

    q = MAPS_QUERY or ADDRESS
    if q:
        mapbox = (f'<iframe class="map" title="Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
                  f'src="https://www.google.com/maps?q={urllib.parse.quote(q)}&amp;output=embed&amp;hl={lang}"></iframe>'
                  f'<p class="note"><a href="https://www.google.com/maps/search/?api=1&amp;query={urllib.parse.quote(q)}" target="_blank" rel="noopener">{T("Google Haritalar\'da aç / yol tarifi al", "Open in Google Maps / get directions")} ↗</a></p>')
    else:
        mapbox = f'<div class="map mapph">🗺️ {PH("Google Harita konumu: build.py içindeki ADDRESS alanını doldurun", "Google Map location: set ADDRESS in build.py")}</div>'

    opts = T(["Tehlikeli atık", "Tehlikesiz atık", "Tıbbi atık", "İnşaat/hafriyat", "Geri dönüşüm", "Diğer / emin değilim"],
             ["Hazardous waste", "Non-hazardous waste", "Medical waste", "Construction/excavation", "Recycling", "Other / not sure"])
    bodies["iletisim"] = (hero(T("İletişim", "Contact"), T("Teklif almak veya acil durum bildirmek için bize ulaşın.", "Reach us for a quote or to report an emergency.")), f"""
<section><div class="wrap"><div class="grid g2">
<div><span class="eyebrow">{T("Teklif Formu", "Quote Form")}</span><h2>{T("Ücretsiz teklif isteyin", "Request a free quote")}</h2>
<form id="teklif">
<div class="row"><label>{T("Ad Soyad", "Full name")}<input name="Name" required></label>
<label>{T("Firma", "Company")}<input name="Company"></label></div>
<div class="row"><label>{T("Telefon", "Phone")}<input name="Phone" type="tel" required></label>
<label>E-mail<input name="E-mail" type="email" required></label></div>
<div class="row"><label>{T("Atık Türü", "Waste type")}<select name="Waste type">{"".join(f"<option>{o}</option>" for o in opts)}</select></label>
<label>{T("Tahmini Miktar", "Estimated volume")}<input name="Volume" placeholder="{T("örn. 5 ton / ay", "e.g. 5 tonnes / month")}"></label></div>
<label>{T("Konum (il/ilçe)", "Location (city/district)")}<input name="Location"></label>
<label>{T("Mesajınız", "Your message")}<textarea name="Message" rows="4"></textarea></label>
<label class="check"><input type="checkbox" required> <span>{T("<a href='kvkk.html'>KVKK Aydınlatma Metni</a>'ni okudum.", f"I have read the <a href='{link('kvkk')}'>Privacy Notice</a>.")}</span></label>
<button class="btn btn-primary" type="submit">{T("Teklif Talebi Gönder", "Send Quote Request")}</button>
<div class="ok">{T("Talebiniz e-posta uygulamanızda hazırlandı. Teşekkürler!", "Your request has been prepared in your e-mail app. Thank you!")}</div>
</form></div>
<div><span class="eyebrow">{T("İletişim", "Contact")}</span><h2>{T("Bize ulaşın", "Get in touch")}</h2>
<div class="card" style="margin-bottom:16px"><h3>{NAME}</h3><p>{full}</p>
<p style="margin-top:10px">📍 {addr}<br>📞 {phone}<br>✉️ {email}<br>🕒 {hours}</p></div>
<div class="card danger" style="margin-bottom:16px"><h3>🚨 {T("7/24 Acil Durum Hattı", "24/7 Emergency Line")}</h3><p>{T("Dökülme, sızıntı veya acil atık müdahalesi için:", "For spills, leaks or urgent waste response:")} <b>{phone}</b></p></div>
{mapbox}</div></div></div></section>""")

    kvkk_tr = f"""<h2>KVKK Aydınlatma Metni</h2>
<p><b>Veri sorumlusu:</b> {FULL}</p>
<p>Bu web sitesindeki teklif ve sponsorluk formları aracılığıyla ilettiğiniz ad-soyad, firma, telefon, e-posta, konum ve mesaj bilgileri; talebinizi değerlendirmek, size teklif sunmak ve sizinle iletişime geçmek amacıyla, 6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında işlenir.</p>
<p>Verileriniz hukuki yükümlülükler dışında üçüncü kişilerle paylaşılmaz. Kanun'un 11. maddesi kapsamında verilerinize erişme, düzeltme, silme ve itiraz haklarınız saklıdır; taleplerinizi {EMAIL or PH("e-posta")} adresine iletebilirsiniz.</p>
<p>Bu site çerez veya izleme aracı kullanmamaktadır. Google Haritalar gömülü harita Google'a ait içerik yükleyebilir.</p>
<p class="note">Not: Bu metin genel bir şablondur; yayına almadan önce şirketin hukuk danışmanı tarafından gözden geçirilmelidir.</p>"""
    kvkk_en = f"""<h2>Privacy Notice</h2>
<p><b>Data controller:</b> {FULL_EN}</p>
<p>The name, company, phone, e-mail, location and message details you send via the quote and sponsorship forms on this website are processed to evaluate your request, provide a quote and contact you, in line with Turkish Law No. 6698 on the Protection of Personal Data.</p>
<p>Your data is not shared with third parties except where legally required. You may request access, correction, deletion or object to processing by writing to {EMAIL or PH("e-mail")}.</p>
<p>This site does not use cookies or tracking tools. The embedded Google Map may load content from Google.</p>
<p class="note">Note: this is a generic template and should be reviewed by the company's legal counsel before going live.</p>"""
    bodies["kvkk"] = (hero(T("KVKK &amp; Gizlilik", "Privacy"), T("Kişisel verilerinizin korunması bizim için önemlidir.", "Protecting your personal data matters to us.")),
                      f'<section><div class="wrap" style="max-width:800px">{kvkk_en if en else kvkk_tr}</div></section>')

    # ---------------- sayfa kabuğu ----------------
    other = "tr" if en else "en"

    def shell(key, title, desc):
        hero_html, body = bodies[key]
        nav = "".join(f'<li><a href="{link(k)}"{" class=active" if k == key else ""}>{bodies_title[k]}</a></li>' for k in NAV_KEYS)
        sw = f'{"../" if en else "en/"}{slug(key, other)}'
        url = f"{SITE_URL}/{'en/' if en else ''}{'' if key == 'index' else slug(key, lang)}"
        alt_tr = f"{SITE_URL}/{'' if key == 'index' else slug(key, 'tr')}"
        alt_en = f"{SITE_URL}/en/{'' if key == 'index' else slug(key, 'en')}"
        ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": NAME, "legalName": FULL,
              "url": SITE_URL, "description": T("Tehlikeli ve tehlikesiz atık nakliyesi ve atık yönetimi", "Hazardous and non-hazardous waste transport and waste management"),
              "areaServed": "TR", "knowsAbout": ["Hazardous waste", "Waste transport", "Recycling"]}
        if PHONE: ld["telephone"] = PHONE
        if EMAIL: ld["email"] = EMAIL
        if ADDRESS: ld["address"] = ADDRESS
        return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {NAME}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="tr" href="{alt_tr}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_tr}">
<meta property="og:title" content="{title} | {NAME}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{'en_US' if en else 'tr_TR'}">
<meta name="theme-color" content="#14532d">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="topbar"><div class="wrap">
  <span>♻️ {T("Tehlikeli &amp; tehlikesiz atık nakliyesi ve yönetimi", "Hazardous &amp; non-hazardous waste transport and management")}</span>
  <span>{T("7/24 Acil Hat", "24/7 Emergency")}: <b>{phone}</b> · <a class="lang" href="{sw}" hreflang="{other}">{'TR 🇹🇷' if en else 'EN 🇬🇧'}</a></span>
</div></div>
<header><div class="wrap">
  <a class="logo" href="{link('index')}"><span class="mark">H</span><span>HAN ATIK<small>{T("ATIK YÖNETİMİ · ÇEVRE", "WASTE MANAGEMENT · ENVIRONMENT")}</small></span></a>
  <button class="burger" aria-label="Menu">☰</button>
  <nav><ul>{nav}<li><a class="cta" href="{link('iletisim')}#teklif">{T("Teklif Al", "Get a Quote")}</a></li></ul></nav>
</div></header>
{hero_html}
{body}
<footer><div class="wrap">
  <div class="grid">
    <div><h4>{NAME}</h4><p style="font-size:.9rem">{full}</p>
      <p style="font-size:.9rem;margin-top:10px">{T("Atıklarınızı mevzuata uygun, güvenli ve çevreye duyarlı şekilde topluyor, taşıyor ve bertaraf/geri kazanım süreçlerini yönetiyoruz.", "We collect, transport and manage the disposal/recovery of your waste in a compliant, safe and eco-conscious way.")}</p></div>
    <div><h4>{T("Sayfalar", "Pages")}</h4><ul>{"".join(f'<li><a href="{link(k)}">{bodies_title[k]}</a></li>' for k in NAV_KEYS)}<li><a href="{link('kvkk')}">{T("KVKK &amp; Gizlilik", "Privacy")}</a></li></ul></div>
    <div><h4>{T("Hizmetler", "Services")}</h4><ul><li>{T("Tehlikeli atık", "Hazardous waste")}</li><li>{T("Tehlikesiz atık", "Non-hazardous waste")}</li><li>{T("ADR nakliye", "ADR transport")}</li><li>{T("Geri dönüşüm", "Recycling")}</li><li>{T("Danışmanlık", "Consulting")}</li></ul></div>
    <div><h4>{T("İletişim", "Contact")}</h4><ul><li>📍 {addr}</li><li>📞 {phone}</li><li>✉️ {email}</li></ul></div>
  </div>
  <div class="copy">© 2026 {full}. {T("Tüm hakları saklıdır.", "All rights reserved.")}</div>
</div></footer>
<a class="wa" href="{tel_href}">📞 {T("Acil Hat", "Emergency")}</a>
<script>window.HAN_MAIL="{sub_to}";</script>
<script src="{root}script.js"></script>
</body></html>"""

    bodies_title = {"index": T("Ana Sayfa", "Home"), "hizmetler": T("Hizmetler", "Services"), "hakkimizda": T("Hakkımızda", "About"),
                    "belgeler": T("Belgeler", "Certificates"), "sponsorluk": T("Sponsorluk", "Sponsorship"),
                    "iletisim": T("İletişim", "Contact"), "kvkk": T("KVKK", "Privacy")}
    metas = {
        "index": (T("Tehlikeli ve Tehlikesiz Atık Nakliyesi ve Yönetimi", "Hazardous & Non-Hazardous Waste Transport and Management"),
                  T("HAN ATIK A.Ş. tehlikeli ve tehlikesiz atık nakliyesi, atık yönetimi, geri dönüşüm ve danışmanlık hizmetleri.", "HAN ATIK Inc.: hazardous and non-hazardous waste transport, waste management, recycling and consulting.")),
        "hizmetler": (T("Hizmetlerimiz", "Services"), T("Tehlikeli atık, tehlikesiz atık, ADR nakliye, geri dönüşüm ve danışmanlık hizmetleri.", "Hazardous waste, non-hazardous waste, ADR transport, recycling and consulting services.")),
        "hakkimizda": (T("Hakkımızda", "About Us"), T("HAN ATIK Yönetimi Çevre İnşaat Sanayi ve Ticaret A.Ş. hakkında.", "About HAN Waste Management Environment Construction Industry and Trade Inc.")),
        "belgeler": (T("Belgeler ve Lisanslar", "Certificates and Licences"), T("HAN ATIK A.Ş. lisans ve belgeleri.", "HAN ATIK licences and certificates.")),
        "sponsorluk": (T("Sponsorluk ve Toplumsal Destek", "Sponsorship and Community Support"), T("Spor, çevre, eğitim ve toplum projelerine destek ve sponsorluk başvurusu.", "Support for sports, environment, education and community projects; sponsorship requests.")),
        "iletisim": (T("İletişim ve Teklif", "Contact and Quote"), T("HAN ATIK A.Ş. iletişim bilgileri, Google Harita konumu ve teklif formu.", "HAN ATIK contact details, Google Map location and quote form.")),
        "kvkk": (T("KVKK ve Gizlilik", "Privacy Notice"), T("Kişisel verilerin korunması aydınlatma metni.", "Personal data protection notice.")),
    }
    outdir = OUT / "en" if en else OUT
    outdir.mkdir(exist_ok=True)
    for k in PAGES:
        (outdir / slug(k, lang)).write_text(shell(k, *metas[k]), encoding="utf-8")


def extras():
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14532d"/>'
        '<text x="32" y="45" font-family="Arial,sans-serif" font-size="38" font-weight="800" text-anchor="middle" fill="#fff">H</text></svg>',
        encoding="utf-8")
    urls = []
    for k in PAGES:
        urls.append(f"{SITE_URL}/{'' if k == 'index' else slug(k, 'tr')}")
        urls.append(f"{SITE_URL}/en/{'' if k == 'index' else slug(k, 'en')}")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (OUT / "404.html").write_text(
        '<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>404 | HAN ATIK A.Ş.</title><link rel="stylesheet" href="' + SITE_URL + '/style.css"></head><body>'
        '<section><div class="wrap" style="text-align:center"><h2>404</h2><p class="lead" style="margin:0 auto 20px">Sayfa bulunamadı / Page not found</p>'
        '<a class="btn btn-green" href="' + SITE_URL + '/">Ana sayfa / Home</a></div></section></body></html>', encoding="utf-8")


if __name__ == "__main__":
    build_lang("tr")
    build_lang("en")
    extras()
    print("tamam: TR + EN + sitemap/robots/404/favicon")

