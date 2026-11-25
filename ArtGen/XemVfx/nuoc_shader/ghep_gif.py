# -*- coding: utf-8 -*-
"""Ghép ảnh tour chụp hiệu ứng nước (Temp/PokiShots/thuy_fx/<tướng>_<dạng>_<atk|mana|ult>_NN.jpg, menu "PokiClash/Thử/Tướng/Đảo Thủy/…")
thành ảnh động GIF + trang xem cục bộ ArtGen/XemVfx/nuoc_shader/xem.html (người dùng ở nhà mở thẳng file, không đưa artifact).
Bộ nước bằng shader (2026-11-24, người dùng chọn "c").
    py -3 -I ghep_gif.py [thư_mục_ảnh]
"""
import glob
import html
import os
import re
import sys
from collections import defaultdict

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(HERE, "..", "..", "..", "Temp", "PokiShots", "thuy_fx"))
OUT = os.path.join(HERE, "gif")
os.makedirs(OUT, exist_ok=True)
TEN = {"ti_tach": "Tí Tách", "thach_giai": "Thạch Giải", "ca_den": "Hải Đăng", "ha_ba": "Hà Bá", "so_ngoc": "Sò Ngọc", "giong_bao": "Giông Bão",
       "lien_kinh": "Liên Kình", "uyen_xa": "Uyên Xà", "han_ngac": "Hàn Ngạc", "hai_long": "Hải Long"}
CLIP = {"atk": "Đòn thường", "mana": "Chiêu mana", "ult": "Chiêu cuối"}

groups = defaultdict(list)
for f in sorted(glob.glob(os.path.join(SRC, "*.jpg"))):
    m = re.match(r"(.+)_(\d+)_(atk|mana|ult)_(\d+)\.jpg$", os.path.basename(f))
    if m:
        groups[(m.group(1), int(m.group(2)), m.group(3))].append(f)
rows = []
for (hero, form, clip), fs in sorted(groups.items()):
    ims = []
    for f in fs:
        im = Image.open(f).convert("RGB")
        w = 420
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        ims.append(im.quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    name = f"{hero}_{form}_{clip}.gif"
    ims[0].save(os.path.join(OUT, name), save_all=True, append_images=ims[1:], duration=110, loop=0, optimize=False)
    rows.append((hero, form, clip, name, len(ims)))
cards = "\n".join(
    f'<figure><img src="gif/{html.escape(n)}" loading="lazy" alt=""><figcaption>{html.escape(TEN.get(h, h))} · dạng {f} · '
    f'{CLIP[c]} <span>{k} khung</span></figcaption></figure>' for h, f, c, n, k in rows)
page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nước shader trong trận</title>
<style>
:root{{--bg:#f4efe2;--fg:#2b2118;--muted:#6b5d4f;--card:#fffaf0;--line:#e3d8c3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1a17;--fg:#efe7d8;--muted:#b5a993;--card:#25231f;--line:#3a362f}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 "Segoe UI",system-ui,sans-serif;margin:0}}
.wrap{{max-width:1320px;margin:0 auto;padding:18px 16px 40px}}
h1{{font-size:1.5rem;margin:0 0 4px}} p{{color:var(--muted);margin:0 0 14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
img{{display:block;width:100%;height:auto}} figcaption{{padding:8px 10px;font-weight:600}} figcaption span{{color:var(--muted);font-weight:400}}
</style>
<div class="wrap"><h1>Bộ nước bằng shader — trong trận</h1>
<p>Chụp từ tour Unity (khung ~0,1 s). Shader PokiClash/UIWaterFx: lam nhạt + bọt trắng, khối cel, mép lam sâu, tan theo ngưỡng × mặt nạ mềm.</p>
<div class="grid">{cards}</div></div>"""
open(os.path.join(HERE, "xem.html"), "w", encoding="utf-8").write(page)
print("ok", len(rows), "gif")
