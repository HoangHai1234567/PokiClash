# -*- coding: utf-8 -*-
"""Trang xem CHIÊU NƯỚC MỚI của 8 tướng Thủy (2026-11-25, HatNuocChieu.cs: đạn liên châu, bong bóng nảy, cầu nhốt, bom nước, cầu xoáy, mưa
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
    ("ti_tach", 2, "mana", "Tí Tách", "Liên châu thủy đạn", "há miệng bắn 5 viên đạn nước liên tiếp, viên cuối to toé lớn"),
    ("thach_giai", 2, "mana", "Thạch Giải", "Bong bóng nảy", "thổi 3 bong bóng bay vồng, nảy một lần trên đất rồi vỡ ở thân đối thủ"),
    ("thach_giai", 2, "ult", "Thạch Giải", "Cầu nhốt", "ợ cầu nước bọc lấy đối thủ thành bong bóng trong suốt, rung hai nhịp rồi vỡ"),
    ("ca_den", 2, "mana", "Hải Đăng", "Bom nước", "phụt cầu nặng bay vồng, vòng gợn báo chỗ rơi, nổ toé đất + cột nước"),
    ("giong_bao", 2, "mana", "Giông Bão", "Cầu xoáy", "cầu tụ theo đầu trượng, ba cầu nhỏ quay quanh, trúng: chớp, gai sắc, toé sao"),
    ("giong_bao", 2, "ult", "Giông Bão", "Mưa giông", "mây giông tụ, mưa xiên, ba cột thác dội (cột giữa sau lưng đối thủ), sét"),
    ("lien_kinh", 2, "ult", "Thôn Kình", "Cầu ma thủy", "triệu hồi cầu ma thủy xanh biển sẫm (prefab gốc của gói, tô dải + vân chì) ngay ở thân đối thủ: cuộn tụ, lõi sáng, dải nước bay vòng, nén rồi nổ"),
    ("uyen_xa", 2, "mana", "Uyên Xà", "Thủy xà", "rắn nước trườn uốn lượn từ hai sừng tới, hai hàm lưỡi liềm ngoạm"),
    ("uyen_xa", 2, "ult", "Uyên Xà", "Chém nước", "đuôi sừng quất: ba lưỡi chém nước cung lưỡi liềm + vệt sáng"),
    ("han_ngac", 2, "ult", "Hàn Ngạc", "Siêu bão xoáy", "phễu nước + vòng xoáy rộng ba tầng, mắt bão trên đỉnh, mảnh băng bạc bay vòng, gió mưa quất"),
    ("han_ngac", 1, "ult", "Hàn Ngạc (Ngạc Nhi)", "Bão xoáy (nhẹ)", "bản dạng 1: ít tầng, ít mảnh băng"),
    ("hai_long", 3, "mana", "Hải Long (Ngũ Đầu)", "Loạt thủy cầu", "mỗi đầu nhả một cầu nước đúng lúc vươn ra (5 đầu)"),
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
<title>Chiêu nước mới</title>
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
<div class="wrap"><h1>Chiêu nước mới — 8 tướng Thủy</h1>
<p>Dựng theo bộ nước gói mẫu (shader UIWaterFx, flipbook SrRubfish + NamuFX), mỗi chiêu bám động tác clip có sẵn của tướng. Chụp tour Unity, ~0,1 s một khung.
Sò Ngoạm, Bát Trảo giữ chiêu riêng. Mã: Assets/01 Script/Game/Battle/HatNuocChieu.cs.</p>
<div class="grid">{"".join(cards)}</div></div>"""
open(os.path.join(HERE, "xem.html"), "w", encoding="utf-8").write(page)
print("ok", len(cards), os.path.join(HERE, "xem.html"))
