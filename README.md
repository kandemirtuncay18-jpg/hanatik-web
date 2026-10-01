# HAN ATIK A.Ş. Web Sitesi

HAN ATIK YÖNETİMİ ÇEVRE İNŞAAT SANAYİ VE TİCARET A.Ş. kurumsal sitesi (tehlikeli/tehlikesiz atık nakliyesi ve atık yönetimi). Türkçe (kök) + İngilizce (`/en/`).

## Düzenleme
Tüm sayfalar `build.py` ile üretilir. Dosyanın başındaki **CONFIG** alanını (telefon, e-posta, adres, kuruluş yılı, site adresi) doldurup çalıştırın:

```
python build.py
```

- `ADDRESS` dolduğunda iletişim sayfasında **Google Harita** otomatik görünür.
- Statik site: GitHub Pages ile yayınlanır, sunucu gerekmez.
- Formlar `mailto:` ile e-posta uygulamasını açar. Doğrudan gönderim için Formspree/Web3Forms gibi bir servis eklenebilir.
- `KVKK` metni şablondur; yayın öncesi hukuki incelemeden geçirin.
