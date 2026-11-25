# -*- coding: utf-8 -*-
"""Trang xem TIA NĂNG LƯỢNG kiểu Water Laser (2026-11-25, HatTiaLaser.ELaser): Lộc Phong (mana), Giác Mộc (mana + chiêu cuối), Thổ Tinh
(tia nhiệt trong chiêu cuối), kèm tia nước Water Laser gốc (Giông Bão) để so. Ảnh từ tour Unity:
    "PokiClash/Thử/Tướng/tia năng lượng kiểu Water Laser (...)"            → thư mục tốc thường
    "PokiClash/Thử/Tướng/tia năng lượng kiểu Water Laser, chạy chậm 0,4×"   → thư mục chậm
    "PokiClash/Thử/Tướng/Đảo Thủy/nước shader: soát tia Water Laser Giông Bão" → thư mục tia nước gốc
(mỗi tour xoá Temp/PokiShots/thuy_fx, nên chép từng lần ra chỗ khác rồi truyền vào đây).
    py -3 -I ghep.py <thư_mục_thường> <thư_mục_chậm> [thư_mục_tia_nước]
Ra gif/*.gif + xem.html cạnh file này (mở thẳng bằng trình duyệt, không đăng artifact: hình tướng aola).
"""
import glob
import html
import os
import re
import sys
from collections import defaultdict

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "gif")
os.makedirs(OUT, exist_ok=True)
TEN = {"bom_la": "Lộc Phong", "moc_tinh": "Giác Mộc", "giap_nham": "Thổ Tinh", "giong_bao": "Giông Bão"}
CLIP = {"mana": "Chiêu mana", "ult": "Chiêu cuối"}
# chiêu có tia: (tướng, đòn); Thổ Tinh: tia nhiệt nằm trong chiêu cuối
CO_TIA = {("bom_la", "mana"), ("moc_tinh", "mana"), ("moc_tinh", "ult"), ("giap_nham", "ult"), ("giong_bao", "mana")}
GHI = {
    ("bom_la", "mana"): "bảng lục ngọc, cầu cau_moc, lá phong cuốn theo",
    ("moc_tinh", "mana"): "bảng hổ phách, cầu cau_vang ở đỉnh sừng",
    ("moc_tinh", "ult"): "tia dày từ tim, nổ cầu cuối",
    ("giap_nham", "ult"): "Mặt Trời to ×2, thẳng trên vỏ đá; tia nhiệt dày gần bằng Mặt Trời, giữ qua vụ nổ",
    ("giong_bao", "mana"): "tia nước Water Laser gốc (bảng 0, không đổi)",
}


# bản chạy chậm: chỉ giữ đoạn có tia (tỉ lệ trong clip; cả clip chậm 10–14 MB mỗi GIF)
CAT = {("bom_la", "mana"): (0.08, 0.72), ("moc_tinh", "mana"): (0.28, 0.76), ("moc_tinh", "ult"): (0.38, 0.82), ("giap_nham", "ult"): (0.62, 0.92)}


def nhom(src):
    g = defaultdict(list)
    if not src or not os.path.isdir(src):
        return g
    for f in sorted(glob.glob(os.path.join(src, "*.jpg"))):
        m = re.match(r"(.+)_(\d+)_(mana|ult)_(\d+)\.jpg$", os.path.basename(f))
        if m and (m.group(1), m.group(3)) in CO_TIA:
            g[(m.group(1), int(m.group(2)), m.group(3))].append(f)
    return g


def gif(fs, name, dur):
    ims = []
    for f in fs:
        im = Image.open(f).convert("RGB")
        im = im.crop((0, int(0.04 * im.height), im.width, int(0.56 * im.height)))   # vùng sân (bỏ bảng thẻ phía dưới)
        w = 480
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        ims.append(im.quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    ims[0].save(os.path.join(OUT, name), save_all=True, append_images=ims[1:], duration=dur, loop=0, optimize=False)
    return len(ims)


def phan(tieu, mo, src, tag, dur):
    rows = []
    for (hero, form, clip), fs in sorted(nhom(src).items(), key=lambda kv: (kv[0][0] != "giong_bao", kv[0])):
        if tag == "cham" and (hero, clip) in CAT:
            a, b = CAT[(hero, clip)]
            fs = fs[int(a * len(fs)):int(b * len(fs)) + 1]
        name = f"{tag}_{hero}_{form}_{clip}.gif"
        k = gif(fs, name, dur)
        rows.append(f'<figure><img src="gif/{html.escape(name)}" loading="lazy" alt=""><figcaption>{html.escape(TEN.get(hero, hero))} · dạng {form} · '
                    f'{CLIP[clip]} <span>{k} khung · {html.escape(GHI.get((hero, clip), ""))}</span></figcaption></figure>')
    if not rows:
        return ""
    return f'<h2>{html.escape(tieu)}</h2><p>{html.escape(mo)}</p><div class="grid">{"".join(rows)}</div>'


thuong = sys.argv[1] if len(sys.argv) > 1 else None
cham = sys.argv[2] if len(sys.argv) > 2 else None
nuoc = sys.argv[3] if len(sys.argv) > 3 else None
body = (phan("Tốc thường", "Như trong trận (ảnh ~0,1 s một khung).", thuong, "thuong", 110)
        + phan("Chạy chậm 0,4×", "Đồng hồ sân và clip tướng cùng chậm: soi từng pha tụ → phóng mảnh → phình → dội → tắt.", cham, "cham", 110)
        + phan("Tia nước gốc để so", "Tia Water Laser của bộ nước (Giông Bão), chụp lại sau khi shader có bảng màu.", nuoc, "nuoc", 110))
page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tia năng lượng Water Laser</title>
<style>
:root{{--bg:#f4efe2;--fg:#2b2118;--muted:#6b5d4f;--card:#fffaf0;--line:#e3d8c3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1a17;--fg:#efe7d8;--muted:#b5a993;--card:#25231f;--line:#3a362f}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 "Segoe UI",system-ui,sans-serif;margin:0}}
.wrap{{max-width:1320px;margin:0 auto;padding:18px 16px 40px}}
h1{{font-size:1.5rem;margin:0 0 4px}} h2{{font-size:1.15rem;margin:22px 0 2px}} p{{color:var(--muted);margin:0 0 12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
img{{display:block;width:100%;height:auto}} figcaption{{padding:8px 10px;font-weight:600}} figcaption span{{color:var(--muted);font-weight:400}}
</style>
<div class="wrap"><h1>Tia năng lượng kiểu Water Laser — Mộc / Thổ</h1>
<p>Khung tia nước Water Laser (ống 4 lớp thở nhịp, phóng mảnh rồi phình, lưỡi liềm ôm thân, xoắn dọc thân, chỗ trúng lặp 0,2 s: chớp, gai sắc,
toé sao) tô bằng bảng màu theo hệ; hạt nước (giọt, bong bóng, mưa) thay bằng tia vụn, lá, than lửa. Shader PokiClash/UIWaterFx, mã HatTiaLaser.cs.</p>
{body}</div>"""
open(os.path.join(HERE, "xem.html"), "w", encoding="utf-8").write(page)
print("ok", os.path.join(HERE, "xem.html"))
