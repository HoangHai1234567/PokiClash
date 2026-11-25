# -*- coding: utf-8 -*-
"""Ghép khung chụp từng prefab của gói lốc "Game VFX - Tornado Collection" (Editor/VfxPackShots.cs, menu "VFX gói lốc: chụp mọi
prefab Tornado Collection" → Temp/PokiShots/vfx_loc/tor_*) thành GIF + tờ 12 khung + trang xem.
    py -3 -I ghep.py            → ArtGen/XemVfx/vfx_loc/{gif,to}/ + xem.html
Gói nhập 2026-11-25 (Assets/Game VFX - Tornado Collection): 8 loại lốc, mỗi loại một bản một lượt + một bản lặp."""
import glob
import html
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Temp", "PokiShots", "vfx_loc"))
GIF = os.path.join(HERE, "gif")
TO = os.path.join(HERE, "to")
os.makedirs(GIF, exist_ok=True)
os.makedirs(TO, exist_ok=True)

# tên Việt cho từng loại (theo tên prefab)
TEN = {"Air": "Khí", "Airflow": "Luồng khí", "Blood": "Máu", "Dark": "Tối", "Fire": "Lửa", "Light": "Sáng",
       "Lightning": "Sét", "Sand": "Cát", "Snow": "Tuyết"}

items = []
for d in sorted(glob.glob(os.path.join(SRC, "tor_*"))):
    fs = sorted(glob.glob(os.path.join(d, "f_*.png")))
    if not fs:
        continue
    name = os.path.basename(d)
    ims = [Image.open(f).convert("RGB") for f in fs]
    w, h = ims[0].size
    small = [im.resize((w * 3 // 4, h * 3 // 4), Image.LANCZOS) for im in ims]
    pal = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for im in small]
    pal[0].save(os.path.join(GIF, name + ".gif"), save_all=True, append_images=pal[1:], duration=42, loop=0, optimize=True)
    n = 12
    idx = [round(i * (len(ims) - 1) / (n - 1)) for i in range(n)]
    cw, ch = w // 2, h // 2
    sheet = Image.new("RGB", (cw * 6, (ch + 12) * 2), (30, 30, 30))
    dr = ImageDraw.Draw(sheet)
    for k, i in enumerate(idx):
        x, y = (k % 6) * cw, (k // 6) * (ch + 12)
        sheet.paste(ims[i].resize((cw, ch), Image.LANCZOS), (x, y))
        dr.text((x + 3, y + ch), f"f{i} {i / 24:.2f}s", fill=(240, 240, 240))
    sheet.save(os.path.join(TO, name + ".png"))
    items.append((name, len(ims)))
    print(name, len(ims))


def label(n):
    raw = n[len("tor_FX_"):] if n.startswith("tor_FX_") else n
    loop = raw.endswith("_Loop")
    key = raw.replace("_Loop", "").replace(" Tornado", "").replace("Tornado", "").strip()
    return f'{TEN.get(key, key)} <span>({"lặp" if loop else "một lượt"})</span>', key, loop


items.sort(key=lambda it: (label(it[0])[1], label(it[0])[2]))
cards = "\n".join(
    f'<figure><img src="gif/{html.escape(n)}.gif" loading="lazy"><figcaption><b>{label(n)[0]}</b>'
    f' <span>{html.escape(n[4:])} · {c} khung · {c / 24:.2f}s · <a href="to/{html.escape(n)}.png">tờ khung</a></span></figcaption></figure>'
    for n, c in items)
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gói lốc mẫu</title>
<style>
body{{margin:0;background:#202226;color:#e8e8e8;font:14px/1.4 system-ui,sans-serif;padding:16px}}
h1{{font-size:20px;margin:0 0 4px}} p{{margin:0 0 14px;color:#aab}} a{{color:#9cf}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}
figure{{margin:0;background:#2c2f35;border-radius:8px;overflow:hidden}}
img{{width:100%;display:block;background:#73767a}} figcaption{{padding:6px 8px}} span{{color:#99a;font-size:12px}}
</style></head><body><h1>Gói lốc mẫu: Game VFX - Tornado Collection</h1>
<p>{len(items)} prefab (8 loại × một lượt / lặp), chụp trong Unity 24 khung/giây, góc ngang chúc 18°. Prefab ở Assets/Game VFX - Tornado Collection/Prefab.</p>
<div class="g">{cards}</div></body></html>"""
open(os.path.join(HERE, "xem.html"), "w", encoding="utf-8").write(page)
print("ok", len(items))
