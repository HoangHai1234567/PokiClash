# -*- coding: utf-8 -*-
"""Ghép khung chụp từng prefab của gói VFX nước (Editor/VfxPackShots.cs → Temp/PokiShots/vfx_goi) thành GIF + tờ 12 khung + trang xem.
    py -3 -I ghep.py            → ArtGen/XemVfx/vfx_goi/{gif,to}/ + xem.html
Gói: SrRubfish "Water - Assets for VFX 02" (rub_*) và NamuFX "Stylized Water Effect Pack" (namu_*); người dùng 2026-11-25 cho dùng làm mẫu."""
import glob
import html
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Temp", "PokiShots", "vfx_goi"))
GIF = os.path.join(HERE, "gif")
TO = os.path.join(HERE, "to")
os.makedirs(GIF, exist_ok=True)
os.makedirs(TO, exist_ok=True)

items = []
for d in sorted(glob.glob(os.path.join(SRC, "*"))):
    if not os.path.isdir(d):
        continue
    fs = sorted(glob.glob(os.path.join(d, "f_*.png")))
    if not fs:
        continue
    name = os.path.basename(d)
    ims = [Image.open(f).convert("RGB") for f in fs]
    w, h = ims[0].size
    small = [im.resize((w * 2 // 3, h * 2 // 3), Image.LANCZOS) for im in ims]
    pal = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for im in small]
    pal[0].save(os.path.join(GIF, name + ".gif"), save_all=True, append_images=pal[1:], duration=42, loop=0, optimize=True)
    # tờ 12 khung đều nhau, có số khung + giây
    n = 12
    idx = [round(i * (len(ims) - 1) / (n - 1)) for i in range(n)]
    cw, ch = w // 2, h // 2
    sheet = Image.new("RGB", (cw * 4, (ch + 12) * 3), (30, 30, 30))
    dr = ImageDraw.Draw(sheet)
    for k, i in enumerate(idx):
        x, y = (k % 4) * cw, (k // 4) * (ch + 12)
        sheet.paste(ims[i].resize((cw, ch), Image.LANCZOS), (x, y))
        dr.text((x + 3, y + ch), f"f{i} {i / 24:.2f}s", fill=(240, 240, 240))
    sheet.save(os.path.join(TO, name + ".png"))
    items.append((name, len(ims)))
    print(name, len(ims))

cards = "\n".join(
    f'<figure><img src="gif/{html.escape(n)}.gif" loading="lazy"><figcaption><b>{html.escape(n.split("_", 1)[1])}</b>'
    f' <span>{"Rubfish" if n.startswith("rub_") else "NamuFX"} · {c} khung · {c / 24:.2f}s</span></figcaption></figure>'
    for n, c in items)
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Gói nước mẫu</title>
<style>
body{{margin:0;background:#202226;color:#e8e8e8;font:14px/1.4 system-ui,sans-serif;padding:16px}}
h1{{font-size:20px;margin:0 0 4px}} p{{margin:0 0 14px;color:#aab}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}}
figure{{margin:0;background:#2c2f35;border-radius:8px;overflow:hidden}}
img{{width:100%;display:block;background:#73767a}} figcaption{{padding:6px 8px}} span{{color:#99a;font-size:12px}}
</style></head><body><h1>Gói nước mẫu: SrRubfish Water VFX 02 + NamuFX Stylized Water</h1>
<p>{len(items)} prefab, chụp trong Unity 24 khung/giây, góc ngang chúc 18°. Dùng làm mẫu để làm lại bộ nước trong trận.</p>
<div class="g">{cards}</div></body></html>"""
open(os.path.join(HERE, "xem.html"), "w", encoding="utf-8").write(page)
print("ok", len(items))
