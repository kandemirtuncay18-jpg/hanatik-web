"""Logo tasarım sayfasından (JPG) sitede kullanılacak şeffaf PNG'leri üretir.

Kullanım: python make_logo.py <logo-sayfasi.jpg>
Üretilen dosyalar: assets/logo.png (yatay logo), assets/logo-mark.png (yalnız amblem),
assets/favicon-192.png, assets/og-image.png
"""
import pathlib
import sys

import numpy as np
from PIL import Image

root = pathlib.Path(__file__).parent
src = Image.open(sys.argv[1]).convert("RGB")
W, H = src.size
sx, sy = W / 2000, H / 1091   # koordinatlar 2000x1091 görsele göre


def box(x0, y0, x1, y1):
    return tuple(int(v) for v in (x0 * sx, y0 * sy, x1 * sx, y1 * sy))


def color_to_alpha(img, bg=(255, 255, 255)):
    """Beyaza yakın zemini şeffaflaştırır, kenarları yumuşak tutar."""
    a = np.asarray(img).astype(np.float32)
    alpha = np.clip((255 - a.min(axis=2)) / 255.0 * 1.6, 0, 1)      # beyaza uzaklık
    alpha[alpha < 0.04] = 0
    out = np.zeros((*a.shape[:2], 4), np.float32)
    safe = np.maximum(alpha, 1e-3)[..., None]
    out[..., :3] = np.clip((a - 255 * (1 - safe)) / safe, 0, 255)
    out[..., 3] = alpha * 255
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def trim(img, pad=6):
    bbox = img.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    l, t, r, b = bbox
    return img.crop((max(0, l - pad), max(0, t - pad), min(img.width, r + pad), min(img.height, b + pad)))


assets = root / "assets"
assets.mkdir(exist_ok=True)

# 1) yatay ana logo
main = trim(color_to_alpha(src.crop(box(330, 50, 1680, 520))))
main.thumbnail((1200, 400))
main.save(assets / "logo.png", optimize=True)

# 2) yalnız amblem (daire + H kale)
mark = trim(color_to_alpha(src.crop(box(350, 50, 850, 510))))
mark.thumbnail((512, 512))
mark.save(assets / "logo-mark.png", optimize=True)

# 3) favicon: amblem beyaz yuvarlak zemin üzerinde, kare
side = 192
fav = Image.new("RGBA", (side, side), (255, 255, 255, 255))
m = mark.copy()
m.thumbnail((int(side * 0.86), int(side * 0.86)))
fav.alpha_composite(m, ((side - m.width) // 2, (side - m.height) // 2))
fav.save(assets / "favicon-192.png", optimize=True)

# 4) sosyal paylaşım görseli (1200x630, beyaz zemin, ortada logo)
og = Image.new("RGB", (1200, 630), (255, 255, 255))
lg = main.copy()
lg.thumbnail((980, 360))
og.paste(lg, ((1200 - lg.width) // 2, (630 - lg.height) // 2), lg)
og.save(assets / "og-image.png", optimize=True)

print("logo.png", main.size, "| mark", mark.size)
