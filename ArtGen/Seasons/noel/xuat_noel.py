# Xuất ảnh mùa Noel vào game (người dùng 2026-11-27):
# - lớp tuyết 4 đảo sảnh (out/tuyet_<hệ>.png của tach_tuyet.py) thu về cỡ gốc của ảnh GPT (không phóng to vô ích);
# - tờ ông già Noel (gen/noel_sheet.png, GPT 2.6, nền trắng): xoá nền trắng nối với mép, tách 3 mảnh theo vùng liền: xe trượt có ông già
#   Noel (trên), tuần lộc dáng duỗi chân (dưới trái), dáng co chân (dưới phải); thu nhỏ còn ~50 %.
# Ra Assets/03 Art/Seasons/Resources/Seasons/noel/ (ArtImporter đặt Sprite, nén ASTC; HubSeason nạp bằng Resources.Load).
# py -3 -I xuat_noel.py
import json, os, sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DST = os.path.join(PROJ, "Assets", "03 Art", "Seasons", "Resources", "Seasons", "noel")
os.makedirs(DST, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

# cỡ ảnh GPT / cỡ khung đã đệm của từng đảo
meta = json.load(open(os.path.join(HERE, "gen", "pad_meta.json")))
for k, m in meta.items():
    g = Image.open(os.path.join(HERE, "gen", f"tuyet_{k}.png"))
    s = min(1.0, g.width / m["W"])  # đảo nhỏ (Casino 760 px) thì giữ cỡ gốc, không phóng
    im = Image.open(os.path.join(HERE, "out", f"tuyet_{k}.png"))
    w, h = round(im.width * s), round(im.height * s)
    im.resize((w, h), Image.LANCZOS).save(os.path.join(DST, f"tuyet_{k}.png"), optimize=True)
    print(f"tuyet_{k}: {im.size} -> {(w, h)}")

# tờ ông già Noel: GPT trả sẵn nền trong suốt nhưng có quầng trắng mờ bán trong suốt quanh hình (không theo luật "không quầng sáng"):
# giữ phần alpha > 128, lấp lỗ bên trong, mép mềm 1 px
raw = np.array(Image.open(os.path.join(HERE, "gen", "noel_sheet.png")).convert("RGBA"))
src = raw[..., :3]
H, W = src.shape[:2]
solid = (raw[..., 3] > 128).astype(np.uint8)
inv = 1 - solid
n, lab, st, _ = cv2.connectedComponentsWithStats(inv, connectivity=4)
# chỉ lấp lỗ li ti (đốm bán trong suốt giữa nét); khe hở thật (dưới xe trượt, giữa chân tuần lộc) giữ trong suốt
tiny = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] < 40]
solid[np.isin(lab, tiny)] = 1
alpha = cv2.GaussianBlur(solid * 255, (3, 3), 0).astype(np.uint8)
rgba = np.dstack([src, alpha])
# tách mảnh theo vùng liền của phần giữ lại (gộp mảnh nhỏ vào mảnh to gần nhất)
fg = (alpha > 40).astype(np.uint8)
n, lab, st, cen = cv2.connectedComponentsWithStats(cv2.dilate(fg, np.ones((15, 15), np.uint8)), 8)
big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 20000]
print("mảnh lớn:", [(int(st[i, 0]), int(st[i, 1]), int(st[i, 2]), int(st[i, 3])) for i in big])
parts = {}
for i in big:
    x, y, w, h = st[i, :4]
    cx, cy = cen[i]
    name = "xe" if cy < H * 0.55 else ("tuan_loc_1" if cx < W / 2 else "tuan_loc_2")
    m = (lab == i)
    p = rgba.copy()
    p[..., 3] = np.where(m, p[..., 3], 0)
    crop = p[max(0, y - 4):y + h + 4, max(0, x - 4):x + w + 4]
    parts[name] = (crop, (x, y, w, h))
scale = 0.5
info = {}
for name, (crop, box) in parts.items():
    im = Image.fromarray(crop)
    out = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    out.save(os.path.join(DST, f"noel_{name}.png"), optimize=True)
    info[name] = {"sheet_box": [int(v) for v in box], "size": out.size}
    print(f"noel_{name}: {out.size}")
json.dump(info, open(os.path.join(HERE, "out", "noel_parts.json"), "w"), indent=1)

# tờ xem: các mảnh trên nền xanh trời
sheet = Image.new("RGBA", (W, H), (120, 170, 220, 255))
for name, (crop, box) in parts.items():
    sheet.alpha_composite(Image.fromarray(crop), (max(0, box[0] - 4), max(0, box[1] - 4)))
sheet.convert("RGB").save(os.path.join(HERE, "out", "xem_noel.jpg"), quality=88)
