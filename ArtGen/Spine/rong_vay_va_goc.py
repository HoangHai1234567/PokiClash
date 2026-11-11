# -*- coding: utf-8 -*-
"""Rồng vây: bo tròn góc lõm ở chỗ hai khúc thân gặp nhau (2026-11-12, người dùng: "cạnh trên bị móp vào 1 chút").
Hình bóng mảnh TRÊN được đặt vào hệ ảnh của mảnh DƯỚI (qua thế giới dáng gốc, lưới part của con gốc); hợp hai hình bóng, đóng hình
thái bán kính R px: phần lấp nằm ở góc giữa hai mảnh thêm vào mảnh DƯỚI (tô màu thân, kẻ lại viền mực ở mép mới). Sau đó chạy lại
rong_vay_va_noi.py để xoá mực + mờ mép chờm của mảnh trên theo hình bóng mới.
    py -3 -I ArtGen/Spine/rong_vay_va_goc.py <slot dưới> <slot trên> [R] [soi]"""
import json, os, sys
import numpy as np, cv2
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rong_vay as RV  # noqa: E402
import rong_vay_bo_cuc as BC  # noqa: E402

duoi, tren = sys.argv[1], sys.argv[2]
R = int(sys.argv[3]) if len(sys.argv) > 3 else 41
SOI = len(sys.argv) > 4
D = json.load(open(os.path.join(BC.sxs(), "scan", BC.MON, "att_goc.json"), encoding="utf-8"))
by = {a["slot"]: a for a in D["atts"]}


def anh(sl):
    for d in ("part_va", "part_noi", "part"):
        p = os.path.join(RV.MANH, d, sl + ".png")
        if os.path.exists(p):
            return np.array(Image.open(p).convert("RGBA"))


def bary_map(Psrc, S_, T_, tr):
    """điểm Psrc trong hệ S_ (đỉnh tam giác) → hệ T_ cùng tam giác (toạ độ trọng tâm; ngoài lưới: tam giác có tâm gần nhất)"""
    A, B, C = S_[tr[:, 0]], S_[tr[:, 1]], S_[tr[:, 2]]
    v0, v1 = B - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)
    tam = (A + B + C) / 3
    out = np.zeros((len(Psrc), 2))
    for s in range(0, len(Psrc), 3000):
        p = Psrc[s:s + 3000, None, :]
        v2 = p - A[None]
        b1 = (v2[..., 0] * v1[None, :, 1] - v2[..., 1] * v1[None, :, 0]) / den
        b2 = (v0[None, :, 0] * v2[..., 1] - v0[None, :, 1] * v2[..., 0]) / den
        b0 = 1 - b1 - b2
        ins = (b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4)
        near = np.argmin(np.hypot(*(tam[None] - p).transpose(2, 0, 1)), axis=1)
        i = np.where(ins.any(1), ins.argmax(1), near)
        r = np.arange(len(i))
        w = np.stack([b0[r, i], b1[r, i], b2[r, i]], 1)
        out[s:s + 3000] = (w[:, :, None] * T_[tr[i]]).sum(1)
    return out


Ad, At = anh(duoi), anh(tren)
Hd, Wd = Ad.shape[:2]
Ht, Wt = At.shape[:2]
ad, at_ = by[duoi], by[tren]
Ud = np.array(ad["uv"], float).reshape(-1, 2) * np.array([Wd, Hd]); Qd = np.array(ad["xy"], float).reshape(-1, 2); trd = np.array(ad["tris"]).reshape(-1, 3)
Ut = np.array(at_["uv"], float).reshape(-1, 2) * np.array([Wt, Ht]); Qt = np.array(at_["xy"], float).reshape(-1, 2); trt = np.array(at_["tris"]).reshape(-1, 3)
ys, xs = np.nonzero(At[..., 3] > 40)
Pt = np.stack([xs + 0.5, ys + 0.5], 1)
W_ = bary_map(Pt, Ut, Qt, trt)            # ảnh trên → thế giới
Pd = bary_map(W_, Qd, Ud, trd)            # thế giới → ảnh dưới
PAD = 80
mt = np.zeros((Hd + 2 * PAD, Wd + 2 * PAD), np.uint8)
ij = np.round(Pd + PAD).astype(int)
ok = (ij[:, 0] >= 0) & (ij[:, 0] < Wd + 2 * PAD) & (ij[:, 1] >= 0) & (ij[:, 1] < Hd + 2 * PAD)
mt[ij[ok, 1], ij[ok, 0]] = 1
mt = cv2.morphologyEx(mt, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
md = np.zeros_like(mt); md[PAD:PAD + Hd, PAD:PAD + Wd] = (Ad[..., 3] > 128)
U = (md | mt).astype(np.uint8)
cl = cv2.morphologyEx(U, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (R, R)))
lap = cl.astype(bool) & ~U.astype(bool)
# chỉ mẩu lấp chạm cả hai hình bóng (góc giữa hai khúc)
n, lab, st, _ = cv2.connectedComponentsWithStats(lap.astype(np.uint8))
k3 = np.ones((5, 5), np.uint8)
gd, gt = cv2.dilate(md, k3).astype(bool), cv2.dilate(mt, k3).astype(bool)
keep = np.zeros_like(lap)
for i in range(1, n):
    c = lab == i
    if st[i, cv2.CC_STAT_AREA] >= 20 and (c & gd).any() and (c & gt).any():
        keep |= c
TRON = os.environ.get("TRON")              # "sigma,x0,y0,x1,y1" (hệ ảnh mảnh dưới): làm trơn viền HỢP hai mảnh trong hộp
cat_d = np.zeros((Hd, Wd), bool)
if TRON:
    sg, x0, y0, x1, y1 = [float(v) for v in TRON.split(",")]
    cs, _ = cv2.findContours(U, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
    r = int(sg * 3)
    kk = np.exp(-0.5 * (np.arange(-r, r + 1) / sg) ** 2); kk /= kk.sum()
    sm = np.stack([np.convolve(np.r_[c[-r:, i], c[:, i], c[:r, i]], kk, "valid") for i in (0, 1)], 1)
    smask = np.zeros_like(U); cv2.fillPoly(smask, [np.round(sm).astype(np.int32)], 1)
    roi = np.zeros(U.shape, bool); roi[int(y0) + PAD:int(y1) + PAD, int(x0) + PAD:int(x1) + PAD] = True
    keep = keep | (roi & smask.astype(bool) & ~U.astype(bool))
    cat = roi & ~smask.astype(bool) & md.astype(bool) & ~mt.astype(bool)
    cat_d = cat[PAD:PAD + Hd, PAD:PAD + Wd]
    print(f"làm trơn viền hợp sigma {sg:.0f}: thêm {int((roi & smask.astype(bool) & ~U.astype(bool)).sum())} px, gọt {int(cat_d.sum())} px")
lap_d = keep[PAD:PAD + Hd, PAD:PAD + Wd]
LOT = os.environ.get("LOT")                # "x0,y0,x1,y1" (hệ ảnh mảnh dưới): lót thân mảnh dưới NGAY DƯỚI mảnh trên quanh chỗ nối
if LOT:                                    # (lúc đứng thì bị che; lúc hai khúc lệch nhau thì lộ thân + viền liền thay vì khe xám)
    x0, y0, x1, y1 = [int(v) for v in LOT.split(",")]
    win = np.zeros((Hd, Wd), bool); win[y0:y1, x0:x1] = True
    lot = win & mt[PAD:PAD + Hd, PAD:PAD + Wd].astype(bool) & ~(Ad[..., 3] > 128)
    lap_d = lap_d | lot
    print(f"lót dưới {tren}: {int(lot.sum())} px")
ra_ngoai = int(keep.sum() - lap_d.sum())
print(f"góc lấp: {int(keep.sum())} px, trong khung ảnh {duoi}: {int(lap_d.sum())} px, ngoài khung: {ra_ngoai} px")
if SOI:
    v = np.full((Hd + 2 * PAD, Wd + 2 * PAD, 3), 150, np.uint8)
    v[mt.astype(bool)] = (230, 90, 90); v[md.astype(bool)] = (90, 200, 90); v[md.astype(bool) & mt.astype(bool)] = (230, 210, 60)
    v[keep] = (40, 40, 255)
    v[PAD:PAD + Hd, PAD:PAD + Wd][cat_d] = (255, 0, 255)
    cv2.rectangle(v, (PAD, PAD), (PAD + Wd - 1, PAD + Hd - 1), (0, 0, 0), 1)
    Image.fromarray(v).save(os.environ.get("RA", "soi_goc.png")); sys.exit()
if not lap_d.any() and not cat_d.any():
    sys.exit("không có gì để đổi trong khung")
# thêm vào mảnh dưới: tô màu thân, kẻ viền ở mép mới
Ad = Ad.copy(); Ad[..., 3][cat_d] = 0
rgb = Ad[..., :3].copy(); al = Ad[..., 3] > 128
dark = (rgb.max(axis=2) < 150) & (Ad[..., 3] > 0)
moi = al | lap_d
dt = cv2.distanceTransform(al.astype(np.uint8), cv2.DIST_L2, 5)
ink = float(np.clip(np.median(dt[dark & al & (dt > 0) & (dt < 15)]) * 2, 4, 10))
gan = cv2.dilate((lap_d | cat_d).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(ink * 5) | 1,) * 2)).astype(bool)
thit = al & ~cv2.dilate(dark.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
base = rgb.copy(); base[~thit] = 0
fill = cv2.inpaint(base, (~thit).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
out = Ad.copy()
to = moi & gan
out[..., :3][to] = fill[to]
# viền: mép của hình bóng HỢP (mảnh dưới mới + mảnh trên), chỉ phần thuộc mảnh dưới quanh chỗ lấp
hop = (moi | mt[PAD:PAD + Hd, PAD:PAD + Wd].astype(bool)).astype(np.uint8)
dm = cv2.distanceTransform(np.pad(hop, 1), cv2.DIST_L2, 5)[1:-1, 1:-1]
dm_moi = cv2.distanceTransform(np.pad(moi.astype(np.uint8), 1), cv2.DIST_L2, 5)[1:-1, 1:-1]
vien = moi & gan & (dm <= ink)
mm = np.median(rgb[dark & al & (dt <= ink)], axis=0)
out[..., :3][vien] = mm.astype(np.uint8)
out[..., 3][lap_d] = 255
# trong vùng sửa: đặc hẳn (mép mềm của lần vá trước giờ nằm trong thân thì thành vạch xám), chỉ mép ngoài cùng mềm 1,5 px
dac = moi & gan
out[..., 3][dac] = np.clip(dm_moi[dac] * 170, 0, 255).astype(np.uint8)
dst = os.path.join(RV.MANH, "part_va", duoi + ".png")
Image.fromarray(out, "RGBA").save(dst)
print(f"{duoi}: lấp góc {int(lap_d.sum())} px, viền {ink:.1f} px -> {os.path.relpath(dst, RV.MANH)}")
