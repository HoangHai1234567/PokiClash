# -*- coding: utf-8 -*-
"""Trang xem CHIÊU ĐỔI MÀU từ bộ chiêu nước cho hệ Mộc, Hỏa (2026-11-25: cầu ma xanh lục / màu lửa, chém lửa, tia lửa năng lượng). Gốc: trang CHIÊU NƯỚC MỚI của 8 tướng Thủy (2026-11-25, HatNuocChieu.cs: đạn liên châu, bong bóng nảy, cầu nhốt, bom nước, cầu xoáy, mưa
giông, sóng thần, thủy xà, chém nước, siêu bão xoáy, loạt thủy cầu). Ảnh từ tour Unity "PokiClash/Thử/Tướng/Đảo Thủy/chiêu nước mới ..."
(mỗi tour xoá Temp/PokiShots/thuy_fx, nên chép ra chỗ khác rồi truyền vào; thư mục sau ghi đè ảnh trùng tên của thư mục trước).
    py -3 -I ghep.py <thư_mục_ảnh> [thư_mục_ảnh_2 ...]
Ra gif/*.gif + xem.html cạnh file này (mở thẳng bằng trình duyệt, không đăng artifact: hình tướng aola).
"""
import glob
import html
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "gif")
os.makedirs(OUT, exist_ok=True)
# (tướng, dạng, đòn, tên tướng, tên chiêu, mô tả) theo thứ tự ải
CHON = [
    ("gac_da", 2, "ult", "Gạc Đá (Mộc)", "Cầu ma xanh lục", "tụ cầu trên hai tay (gió lá hút vào), cầu thành hình: lõi sáng, dải lục bay vòng; ném, nổ lá"),
    ("bom_la", 2, "ult", "Lộc Phong (Mộc)", "Cầu ma xanh lục", "ngửa đầu há mồm tụ cầu to, thành hình rồi gật đầu nện vào đối thủ"),
    ("nguu_quyen", 2, "ult", "Hỏa Quy (Hỏa)", "Cầu ma màu lửa", "lửa trên lưng hút vào cầu đỏ cam đặc trên mũi sừng (to 1,8 lần cầu cũ), lưỡi lửa liếm quanh; hất sừng phóng cầu, cầu vỡ (quầng cam, vòng sóng, lưỡi liềm lửa) rồi nổ lửa"),
    ("giap_long", 2, "ult", "Viêm Đao (Hỏa)", "Chém lửa", "lao tới liên hoàn 7 nhát: mỗi nhát một lưỡi liềm lửa (Chém nước đổi bảng lửa); cú bổ cuối cung chém dọc + nổ lớn"),
    ("su_tu_lua", 3, "mana", "Tiểu Quỷ Lava (Hỏa)", "Tia lửa năng lượng", "chĩa giáo bắn tia lửa kiểu Water Laser từ mũi giáo (trước: cầu lửa, lệch clip)"),
    ("hoa_nhan", 2, "mana", "Hỏa Nhãn (Hỏa)", "Tia lửa năng lượng", "tia lửa kiểu Water Laser từ giữa con mắt, bông trúng toé ở thân đối thủ"),
]


def gom(srcs):
    files = {}
    for src in srcs:
        for f in glob.glob(os.path.join(src, "*.jpg")):
            files[os.path.basename(f)] = f
    return files


def gif(fs, name, dur=110):
    ims = []
    for f in fs:
        im = Image.open(f).convert("RGB")
        im = im.crop((0, int(0.04 * im.height), im.width, int(0.56 * im.height)))   # vùng sân (bỏ bảng thẻ phía dưới)
        w = 480
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        ims.append(im.quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    ims[0].save(os.path.join(OUT, name), save_all=True, append_images=ims[1:], duration=dur, loop=0, optimize=False)
    return len(ims)


files = gom(sys.argv[1:])
cards = []
for hero, form, clip, ten, chieu, mota in CHON:
    pat = re.compile(rf"^{re.escape(hero)}_{form}_{clip}_(\d+)\.jpg$")
    fs = sorted((v for k, v in files.items() if pat.match(k)), key=lambda p: int(pat.match(os.path.basename(p)).group(1)))
    if not fs:
        print("thiếu", hero, form, clip)
        continue
    name = f"{hero}_{form}_{clip}.gif"
    k = gif(fs, name)
    cards.append(f'<figure><img src="gif/{html.escape(name)}" loading="lazy" alt=""><figcaption>{html.escape(ten)} · '
                 f'{"Chiêu mana" if clip == "mana" else "Chiêu cuối"} <b>{html.escape(chieu)}</b><span>{html.escape(mota)} · {k} khung</span></figcaption></figure>')
page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chiêu đổi màu</title>
<style>
:root{{--bg:#f4efe2;--fg:#2b2118;--muted:#6b5d4f;--card:#fffaf0;--line:#e3d8c3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1a17;--fg:#efe7d8;--muted:#b5a993;--card:#25231f;--line:#3a362f}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 "Segoe UI",system-ui,sans-serif;margin:0}}
.wrap{{max-width:1320px;margin:0 auto;padding:18px 16px 40px}}
h1{{font-size:1.5rem;margin:0 0 4px}} p{{color:var(--muted);margin:0 0 14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
img{{display:block;width:100%;height:auto}} figcaption{{padding:8px 10px;font-weight:600}} figcaption span{{display:block;color:var(--muted);font-weight:400}}
</style>
<div class="wrap"><h1>Chiêu đổi màu — Mộc, Hỏa</h1>
<p>Dùng lại bộ chiêu nước ở hệ khác, chỉ chỗ hợp: cầu prefab gốc MagicWater_OrbLoop tô dải lục / đỏ cam (CauMaTheo), lưỡi chém nước đổi bảng lửa, tia Water Laser bảng lửa. Chụp tour Unity, ~0,1 s một khung. Mã: HatChieuDoiMau.cs, HatNuocChieu.cs (CauMaTheo), HatDa / HatLoc / HatRua / HatNhan.cs.</p>
<div class="grid">{"".join(cards)}</div></div>"""
open(os.path.join(HERE, "xem.html"), "w", encoding="utf-8").write(page)
print("ok", len(cards), os.path.join(HERE, "xem.html"))
