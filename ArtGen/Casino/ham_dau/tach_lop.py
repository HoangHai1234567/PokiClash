# Tách lớp động từ nền Hầm đấu (nen_ham_dau_2k.jpg) cho "cổng sắt mở đóng, khán giả nhún" (người dùng 2026-11-26):
# - cổng: song sắt (hình sáng trong lòng vòm tối) thành cong_song.png; mặt nạ lòng vòm cong_mat_na.png (song trượt lên bị vòm che);
#   nền được vá: lòng vòm không còn song (nen_ham_dau_2k_dong.jpg là bản nền dùng trong game);
# - khán giả hàng đầu (mảng tối ở đáy): 5 mảnh theo cột, kg_duoi_<i>.png;
# - khán giả trên khán đài hai bên: 2 mảnh mỗi bên, kg_xa_<i>.png.
# Khán giả vẫn nằm nguyên trong nền: mảnh chỉ nhích LÊN vài px rồi về, chỗ hở bên dưới lộ đúng mảng tối của nền nên không thấy mép.
# Ra thư mục lop/ + lop.json (khung từng mảnh theo px ảnh 2k) + lop_xem.png (mọi mảnh dời hết cỡ, cổng mở) để soát.
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "lop")
os.makedirs(OUT, exist_ok=True)
src = Image.open(os.path.join(HERE, "nen_ham_dau_2k.jpg")).convert("RGB")
W, H = src.size
A = np.asarray(src).astype(np.int32)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
LUM = (R * 299 + G * 587 + B * 114) // 1000


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def save_piece(name, mask, box, info, soft=1.2):
    """mask: bool cả ảnh; box: khung tìm (x0, y0, x1, y1). Cắt theo khung bao của mask trong box, mép mềm."""
    x0, y0, x1, y1 = box
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys) == 0:
        raise SystemExit("mat na rong: " + name)
    bx0, bx1, by0, by1 = max(0, xs.min() - 3), min(W, xs.max() + 4), max(0, ys.min() - 3), min(H, ys.max() + 4)
    a = ndimage.gaussian_filter(m[by0:by1, bx0:bx1].astype(np.float32), soft)
    a = np.clip((a - 0.25) / 0.5, 0, 1)
    rgba = np.dstack([np.asarray(src)[by0:by1, bx0:bx1], (a * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, name + ".png"))
    info[name] = [int(bx0), int(by0), int(bx1), int(by1)]
    return m


info = {}

# ---------- cổng sắt ----------
GX0, GY0, GX1, GY1 = 396, 940, 740, 1072
dark = np.zeros((H, W), bool)
dark[GY0:GY1, GX0:GX1] = LUM[GY0:GY1, GX0:GX1] < 70
# mảng tối của lòng vòm: bào 3 px cho đứt khỏi các nét mực mảnh (viền vòm đá, viền cột), lấy các mảng có tâm trong lòng vòm
core = ndimage.binary_erosion(dark, disk(3))
lab, n = ndimage.label(core)
inner = np.zeros((H, W), bool)
for k, (cy, cx) in enumerate(ndimage.center_of_mass(core, lab, range(1, n + 1)), 1):
    if 962 <= cy <= 1062 and 416 <= cx <= 720 and (lab == k).sum() > 120:
        inner |= lab == k
assert inner.any(), "khong thay long vom toi"
inner = ndimage.binary_dilation(inner, disk(3)) & dark
# lòng vòm = mảng tối + song nằm giữa (đóng hình bán kính 10: lấp song rộng ~14 px, không ăn sang vòm đá dày hơn)
opening = ndimage.binary_closing(inner, disk(10), border_value=0)
opening = ndimage.binary_fill_holes(opening)
opening[:GY0] = False
# bỏ thứ có màu (mũ cột gỗ, dây thừng trước cổng): song và lòng vòm đều xám / tối
coloured = ndimage.binary_dilation((R - B > 100) & (LUM > 78), disk(3))   # song xám hồng có R - B ~ 60, gỗ / thừng trên 150
opening &= ~coloured
opening = ndimage.binary_opening(opening, disk(3))
# mẩu song sát vòm đá bị sót ngoài lòng vòm: mảng sáng NHỎ chạm lòng vòm (vòm đá, đá kê là mảng lớn nên không dính)
light = np.zeros((H, W), bool)
light[GY0:GY1, GX0:GX1] = ((LUM > 78) & ~coloured)[GY0:GY1, GX0:GX1]
lab, n = ndimage.label(light)
near = ndimage.binary_dilation(opening, disk(8))
for k in range(1, n + 1):
    comp = lab == k
    if comp.sum() < 900 and (comp & near).any():
        opening |= ndimage.binary_dilation(comp, disk(3))
bars = opening & (LUM > 78)
bars_soft = ndimage.binary_dilation(bars, disk(2))
# mặt nạ lòng vòm (trắng, alpha theo lòng vòm)
ys, xs = np.where(opening)
ox0, ox1, oy0, oy1 = xs.min() - 2, xs.max() + 3, ys.min() - 2, ys.max() + 3
m = np.zeros((oy1 - oy0, ox1 - ox0, 4), np.uint8)
m[..., :3] = 255
m[..., 3] = opening[oy0:oy1, ox0:ox1] * 255
Image.fromarray(m, "RGBA").save(os.path.join(OUT, "cong_mat_na.png"))
info["cong_mat_na"] = [int(ox0), int(oy0), int(ox1), int(oy1)]
# song sắt: cùng khung với mặt nạ, alpha mềm theo độ sáng
al = np.clip((LUM[oy0:oy1, ox0:ox1] - 62) / 34.0, 0, 1) * bars_soft[oy0:oy1, ox0:ox1]
song = np.dstack([np.asarray(src)[oy0:oy1, ox0:ox1], (al * 255).astype(np.uint8)])
Image.fromarray(song, "RGBA").save(os.path.join(OUT, "cong_song.png"))
info["cong_song"] = info["cong_mat_na"]
# vá nền: chỗ song lấy màu điểm tối gần nhất trong lòng vòm (giữ vân chì)
fix = np.asarray(src).copy()
hole = ndimage.binary_dilation(bars, disk(4)) & opening
keep = opening & ~hole
idx = ndimage.distance_transform_edt(~keep, return_distances=False, return_indices=True)
hy, hx = np.where(hole)
fix[hy, hx] = fix[idx[0][hy, hx], idx[1][hy, hx]]

# ---------- khán giả hàng đầu (đáy ảnh) ----------
bluish = (B * 100 >= R * 74) & (LUM < 215)                 # tím than, viền hồng, băng mũ
cream = (R > 215) & (G > 185) & (B > 120)                  # lá bài
ink = LUM < 52
fg = np.zeros((H, W), bool)
Y0 = 1700
fg[Y0:] = (bluish | cream | ink)[Y0:]
fg = ndimage.binary_opening(fg, disk(6))                   # bỏ nét kẻ ván gỗ, thừng
fg = ndimage.binary_closing(fg, disk(4))
lab, n = ndimage.label(fg)
bottom = set(np.unique(lab[H - 12])) - {0}   # sát mép ảnh bị phép đóng hình ăn mất vài hàng
fg = np.isin(lab, list(bottom))
fg = ndimage.binary_fill_holes(fg)
fg[H - 12:] = fg[H - 13]            # trả lại các hàng sát đáy
CUTS = [0, 262, 548, 858, 985, W]
crowd = np.zeros((H, W), bool)   # mọi mảnh khán giả: để xoá chi tiết sáng của khán giả trong nền (xem cuối file)
for i in range(len(CUTS) - 1):
    crowd |= save_piece("kg_duoi_%d" % i, fg, (CUTS[i], Y0, CUTS[i + 1], H), info)

# ---------- khán giả trên khán đài ----------
navy = (B >= R - 6) & (LUM < 92)
bright = (LUM > 165) & (G * 100 > R * 70) & (B < 215)      # mắt kem, mũ rơm, cờ vàng, lá bài
far = navy | bright
far = ndimage.binary_opening(far, disk(4))                 # bỏ nét kẻ đá trên tường, cán cờ
REG = [(0, 400, 190, 735), (190, 400, 345, 735), (800, 400, 955, 735), (955, 400, W, 735)]
for i, (x0, y0, x1, y1) in enumerate(REG):
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = far[y0:y1, x0:x1]
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, [k + 1 for k, s in enumerate(sizes) if s > 2500])
    m = ndimage.binary_fill_holes(ndimage.binary_closing(m, disk(3)))
    crowd |= save_piece("kg_xa_%d" % i, m, (x0, y0, x1, y1), info, soft=1.0)

# Khán giả trong nền: chi tiết sáng (viền hồng, băng mũ, mắt, lá bài) tô lại thành mảng tối, lấy màu điểm tối gần nhất. Mảnh rời nằm
# đè lên mang đủ chi tiết; lúc mảnh nhích lên, chỗ lộ ra bên dưới chỉ còn mảng tối trơn nên không thấy nét đôi.
inside = ndimage.binary_erosion(crowd, disk(2))
plain = inside & (LUM < 62)
detail = ndimage.binary_dilation(inside & (LUM >= 62), disk(2)) & inside
plain &= ~detail
idx = ndimage.distance_transform_edt(~plain, return_distances=False, return_indices=True)
hy, hx = np.where(detail)
fix[hy, hx] = fix[idx[0][hy, hx], idx[1][hy, hx]]
nen = Image.fromarray(fix, "RGB")
nen.save(os.path.join(HERE, "nen_ham_dau_2k_dong.jpg"), quality=93)

json.dump({"size": [W, H], "pieces": info}, open(os.path.join(OUT, "lop.json"), "w"), indent=1)

# ---------- xem: mọi mảnh nhích hết cỡ, cổng mở ----------
pv = nen.convert("RGBA")
for name, (x0, y0, x1, y1) in info.items():
    if name.startswith("cong"):
        continue
    im = Image.open(os.path.join(OUT, name + ".png"))
    pv.alpha_composite(im, (x0, y0 - (14 if "duoi" in name else 8)))
pv.convert("RGB").save(os.path.join(OUT, "lop_xem.jpg"), quality=88)
# xem riêng: các mảnh trên nền hồng (soát mặt nạ)
chk = Image.new("RGBA", (W, H), (255, 0, 255, 255))
for name, (x0, y0, x1, y1) in info.items():
    if name == "cong_mat_na":
        continue
    chk.alpha_composite(Image.open(os.path.join(OUT, name + ".png")), (x0, y0))
chk.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(OUT, "lop_mat_na.jpg"), quality=85)
print(json.dumps(info))
