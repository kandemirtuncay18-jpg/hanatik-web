"""Google Fonts (Outfit + Inter) latin/latin-ext dosyalarını indirip assets/fonts altına koyar ve fonts.css üretir."""
import pathlib
import re
import urllib.request

root = pathlib.Path(__file__).parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
css_url = "https://fonts.googleapis.com/css2?family=Outfit:wght@500..800&family=Inter:wght@400..700&display=swap"
src = urllib.request.urlopen(urllib.request.Request(css_url, headers={"User-Agent": UA})).read().decode()

out = []
fonts = root / "assets" / "fonts"
fonts.mkdir(parents=True, exist_ok=True)
for m in re.finditer(r"/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}", src, re.S):
    subset, body = m.group(1), m.group(2)
    if subset not in ("latin", "latin-ext"):
        continue
    family = re.search(r"font-family: '([^']+)'", body).group(1)
    url = re.search(r"url\((https://[^)]+)\)", body).group(1)
    name = f"{family.lower()}-{subset}.woff2"
    (fonts / name).write_bytes(urllib.request.urlopen(url).read())
    weight = re.search(r"font-weight: ([^;]+);", body).group(1)
    rng = re.search(r"unicode-range: ([^;]+);", body).group(1)
    out.append(
        f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;"
        f"src:url(assets/fonts/{name}) format('woff2');unicode-range:{rng}}}"
    )
(root / "fonts.css").write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(out), "font tanımı yazıldı")
