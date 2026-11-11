# -*- coding: utf-8 -*-
"""Rồng vây: xoá vạch mực chỗ khúc trên đè khúc dưới cho các mảnh đã vá (manh/part_va), như rong_vay.py noi_part (2026-11-12).
Mỗi điểm ảnh của hai mảnh đặt vào thế giới ở dáng gốc qua lưới part của con gốc (toạ độ trọng tâm trong hệ uv, ngoài lưới thì kéo dài
tam giác gần nhất); nét mực của mảnh TRÊN mà nằm sâu trong hình bóng mảnh DƯỚI (hơn SAU đơn vị rig) thì tô lại màu thân gần nhất.
    py -3 -I ArtGen/Spine/rong_vay_va_noi.py <slot trên> <slot dưới> [sâu]      (ảnh vào/ra: manh/part_va/<slot trên>.png)"""
import json, os, sys
import numpy as np, cv2
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rong_vay as RV  # noqa: E402
import rong_vay_bo_cuc as BC  # noqa: E402

tren, duoi = sys.argv[1], sys.argv[2]
SAU = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
D = json.load(open(os.path.join(BC.sxs(), "scan", BC.MON, "att_goc.json"), encoding="utf-8"))
by = {a["slot"]: a for a in D["atts"]}


def anh(sl):
    for d in ("part_va", "part_noi", "part"):
        p = os.path.join(RV.MANH, d, sl + ".png")
        if os.path.exists(p):
            return p, np.array(Image.open(p).convert("RGBA"))


def the_gioi(sl, A):
    """(H, W, 2) toạ độ thế giới (đơn vị con gốc) của từng điểm ảnh có alpha"""
    a = by[sl]
    H, W = A.shape[:2]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([W, H])
    Q = np.array(a["xy"], float).reshape(-1, 2)
    tr = np.array(a["tris"]).reshape(-1, 3)
    out = np.full((H, W, 2), np.nan)
    ys, xs = np.nonzero(A[..., 3] > 0)
    P = np.stack([xs + 0.5, ys + 0.5], 1)
    Aa, Bb, Cc = U[tr[:, 0]], U[tr[:, 1]], U[tr[:, 2]]
    v0, v1 = Bb - Aa, Cc - Aa
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)
    tam = (Aa + Bb + Cc) / 3
    for s in range(0, len(P), 4000):
        p = P[s:s + 4000, None, :]
        v2 = p - Aa[None]
        b1 = (v2[..., 0] * v1[None, :, 1] - v2[..., 1] * v1[None, :, 0]) / den
        b2 = (v0[None, :, 0] * v2[..., 1] - v0[None, :, 1] * v2[..., 0]) / den
        b0 = 1 - b1 - b2
        inside = (b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4)
        near = np.argmin(np.hypot(*(tam[None] - p).transpose(2, 0, 1)), axis=1)
        i = np.where(inside.any(1), inside.argmax(1), near)
        r = np.arange(len(i))
        w = np.stack([b0[r, i], b1[r, i], b2[r, i]], 1)
        X = (w[:, :, None] * Q[tr[i]]).sum(1)
        out[ys[s:s + 4000], xs[s:s + 4000]] = X
    return out


pt, At = anh(tren)
pd, Ad = anh(duoi)
Xt, Xd = the_gioi(tren, At), the_gioi(duoi, Ad)
# hình bóng mảnh dưới trên lưới thế giới 0,5 đơn vị → khoảng cách vào trong
pts = Xd[Ad[..., 3] > 128]
lo = np.nanmin(np.r_[pts, Xt[At[..., 3] > 0]], 0) - 20
hi = np.nanmax(np.r_[pts, Xt[At[..., 3] > 0]], 0) + 20
st = 0.5
G = np.ceil((hi - lo) / st).astype(int) + 1
m = np.zeros((G[1], G[0]), np.uint8)
ij = np.round((pts - lo) / st).astype(int)
m[ij[:, 1], ij[:, 0]] = 1
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
sau = cv2.distanceTransform(m, cv2.DIST_L2, 5) * st
rgb = At[..., :3]
al = At[..., 3] > 128
dark = (rgb.max(axis=2) < 150) & (At[..., 3] > 0)
ok = ~np.isnan(Xt[..., 0])
ij2 = np.round((np.nan_to_num(Xt) - lo) / st).astype(int)
ij2[..., 0] = np.clip(ij2[..., 0], 0, G[0] - 1)
ij2[..., 1] = np.clip(ij2[..., 1], 0, G[1] - 1)
d_in = np.where(ok, sau[ij2[..., 1], ij2[..., 0]], 0)
xoa = dark & (d_in > SAU)
# KE: mép hai khúc KHÍT cạnh nhau (không chồng): nét mực của mảnh trên cách hình bóng mảnh dưới dưới KE đơn vị cũng là vạch nối
KE = float(os.environ.get("KE", "0"))
if KE > 0:
    ngoai = cv2.distanceTransform((1 - m).astype(np.uint8), cv2.DIST_L2, 5) * st
    d_out = np.where(ok, ngoai[ij2[..., 1], ij2[..., 0]], 1e9)
    xoa |= dark & (d_out < KE)
# GIU: nét mực nằm sát mép NGOÀI của hình ghép hai mảnh (dưới GIU đơn vị) là viền thật (vd vành bụng dưới khi mảnh dưới thò ra
# vài px so với mảnh trên): giữ, kẻo mảnh trên xoá viền mình mà thân mình lại che viền mảnh dưới → hở viền
GIU = float(os.environ.get("GIU", "0"))
PHU = float(os.environ.get("PHU", "0"))
d_h = np.zeros(At.shape[:2])
if GIU > 0 or PHU > 0:
    pt_t = Xt[At[..., 3] > 128]
    ij_t = np.round((pt_t - lo) / st).astype(int)
    ij_t[:, 0] = np.clip(ij_t[:, 0], 0, G[0] - 1); ij_t[:, 1] = np.clip(ij_t[:, 1], 0, G[1] - 1)
    mt_ = np.zeros_like(m); mt_[ij_t[:, 1], ij_t[:, 0]] = 1
    mt_ = cv2.morphologyEx(mt_, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    d_hop = cv2.distanceTransform((m | mt_).astype(np.uint8), cv2.DIST_L2, 5) * st
    d_h = np.where(ok, d_hop[ij2[..., 1], ij2[..., 0]], 0)
    if GIU > 0:
        xoa &= ~(d_h < GIU)
# chỉ nét mực VIỀN (gần mép mảnh trên), không đụng vạch bụng bên trong
dm = cv2.distanceTransform(np.pad(al.astype(np.uint8), 1), cv2.DIST_L2, 5)[1:-1, 1:-1]
xoa &= dm < 16
xoa = cv2.dilate(xoa.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & (At[..., 3] > 0)
VUNG = os.environ.get("VUNG")              # "x0,y0,x1,y1" (hệ ảnh mảnh trên): chỉ xoá mực trong hộp này (giữ viền ngoài ở chỗ khác)
if VUNG:
    x0, y0, x1, y1 = [int(v) for v in VUNG.split(",")]
    hop_ = np.zeros_like(xoa); hop_[y0:y1, x0:x1] = True
    xoa &= hop_
# điểm trắng giấy sót trong thân (GPT/cắt mảnh): tô lại màu kề bên, kẻo mờ mép chờm thành vệt sáng
trang = (At[..., :3].min(axis=2) > 232) & (At[..., 3] > 0)
xoa |= trang
thit = al & ~cv2.dilate(dark.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & ~cv2.dilate(trang.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
base = rgb.copy(); base[~thit] = 0
fill = cv2.inpaint(base, (~thit).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)   # chỉ loang từ thịt thân (điểm trong suốt không được làm màu nguồn)
out = At.copy()
out[..., :3][xoa] = fill[xoa]
out[..., 3][xoa] = 255
# mép cắt của mảnh trên nằm trong mảnh dưới (đường cắt khung part): mờ dần alpha từ mép đó vào MO px, chỉ ở chỗ có mảnh dưới
# phía sau (như nối các khúc khác: chờm đặc rồi mờ), để vân chì và vành bụng hai khúc hoà vào nhau thay vì một đường cắt thẳng
MO = float(os.environ.get("MO", "26"))
if MO > 0:
    a8 = (out[..., 3] > 0).astype(np.uint8)
    vien_ngoai = a8.astype(bool) & ~cv2.erode(np.pad(a8, 1), np.ones((3, 3), np.uint8))[1:-1, 1:-1].astype(bool)
    E = vien_ngoai & (d_in > 3.0)
    if E.any():
        dE = cv2.distanceTransform((~E).astype(np.uint8), cv2.DIST_L2, 5)
        k = np.clip(dE / MO, 0.0, 1.0)
        sau_lung = d_in > 0.5
        if GIU > 0:                                   # viền thật (sát mép ngoài hình ghép) không mờ
            sau_lung &= ~((d_h < GIU) & dark)
        al2 = out[..., 3].astype(float)
        al2[sau_lung] *= k[sau_lung] ** 1.2
        out[..., 3] = np.clip(al2, 0, 255).astype(np.uint8)
        print(f"  mờ mép cắt: {int(E.sum())} px mép nằm trong {duoi}, dải {MO:.0f} px")
# PHU: chỗ mảnh trên chồng lên mảnh dưới mà sát mép NGOÀI hình ghép (dưới PHU đơn vị): mảnh trên trong suốt hẳn (cả mực lẫn thân),
# để viền mảnh dưới lo trọn đoạn đó (viền mảnh trên ở đây thường đã bị xoá dở từ bước nối mảnh cũ → sọc, hở)
if PHU > 0:
    phu = (d_in > 0.5) & (d_h < PHU) & (out[..., 3] > 0)
    out[..., 3][phu] = 0
    print(f"  nhường viền cho {duoi}: {int(phu.sum())} px")
# CAT="x0,y0,x1,y1,d" (hệ ảnh mảnh trên): trong hộp, phần mảnh trên thò RA NGOÀI mảnh dưới dưới d đơn vị (dải mỏng mà viền đã bị
# bước nối mảnh cũ xoá thành màu sáng → riềm sáng ngoài viền mảnh dưới): gọt bỏ
CAT = os.environ.get("CAT")
if CAT:
    x0, y0, x1, y1, dd = [float(v) for v in CAT.split(",")]
    ngoai_ = cv2.distanceTransform((1 - m).astype(np.uint8), cv2.DIST_L2, 5) * st
    d_o = np.where(ok, ngoai_[ij2[..., 1], ij2[..., 0]], 1e9)
    hop2 = np.zeros(out.shape[:2], bool); hop2[int(y0):int(y1), int(x0):int(x1)] = True
    # chỉ dải sát mép NGOÀI hình ghép (d_h nhỏ), không gọt dọc đầu cuối của mảnh dưới nằm giữa thân (thành vết nứt khi chuyển động)
    cat = hop2 & (d_in <= 0.5) & (d_o < dd) & (d_h < dd) & (out[..., 3] > 0)
    out[..., 3][cat] = 0
    print(f"  gọt dải thò ra ngoài {duoi}: {int(cat.sum())} px")
# SANG="x0,y0,x1,y1" (hệ ảnh mảnh trên): điểm sáng màu sát mép trong suốt (riềm sáng ngoài nét viền, sót từ bước nối mảnh cũ)
# trong hộp: tô thành màu mực
SANG = os.environ.get("SANG")
if SANG:
    x0, y0, x1, y1 = [int(v) for v in SANG.split(",")]
    hop3 = np.zeros(out.shape[:2], bool); hop3[y0:y1, x0:x1] = True
    co = (out[..., 3] > 0).astype(np.uint8)
    sat_mep = cv2.distanceTransform(np.pad(co, 1), cv2.DIST_L2, 5)[1:-1, 1:-1] <= 3.0
    sang = hop3 & (out[..., 3] > 0) & sat_mep & (out[..., :3].min(axis=2) > 150)
    mm_ = np.median(At[..., :3][dark & (At[..., 3] > 200)], axis=0)
    out[..., :3][sang] = mm_.astype(np.uint8)
    print(f"  riềm sáng thành mực: {int(sang.sum())} px")
dst = os.path.join(RV.MANH, "part_va", tren + ".png")
os.makedirs(os.path.dirname(dst), exist_ok=True)
Image.fromarray(out, "RGBA").save(dst)
print(f"  điểm trắng giấy: {int(trang.sum())} px")
print(f"{tren} (từ {os.path.relpath(pt, RV.MANH)}) trên {duoi}: xoá {int(xoa.sum())} px mực sâu hơn {SAU} đơn vị -> {os.path.relpath(dst, RV.MANH)}")
