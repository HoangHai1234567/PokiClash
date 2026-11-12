# -*- coding: utf-8 -*-
"""Tinh linh rừng mập, hướng "mầm hai lá" (người dùng chốt 2026-11-12): MẢNH cho rig, làm hết bằng mã từ concept đã duyệt
(inbox/tinh_linh_1/tai_ve/L1_duyet.png), không gen thêm. Nét của game tô phẳng nên:

- THÂN (bụng, đầu, hai tay): hình bóng KÍN của đúng part con gốc (để lắp nguyên lưới của họ), tô bằng VÂN SÁP LÁT lấy từ thân trên
  concept, lát theo toạ độ THẾ GIỚI (đầu chồng lên bụng không lộ đường nối), viền mực kẻ bằng mã (bề dày rung nhẹ). Đầu: mép dưới nằm
  trong bụng KHÔNG có mực (đầu và bụng liền một khối), chỉ hai nếp gấp ngắn màu lục; má hồng vẽ trên đầu.
- MẮT: sáu bộ (bq1..bq6) đúng khung part: lòng TRẮNG trơn, vành dày màu lục (kiểu Tí Tách), không con ngươi, không mực.
- TÓC (mầm hai lá + cuống + vòng lá con): cắt thẳng từ concept thành MỘT mảnh. TRONG BỤNG: cụm hạt giống (hạt + rễ + mầm) và ba bong
  bóng, cắt từ concept. Các mảnh này là của mình, rig gắn lên xương riêng.
- MỒM: bầu dục sẫm + mảng lưỡi nhạt, không viền mực (như Tí Tách); chỉ hiện lúc bắn chiêu.

    tinh_linh_manh.py lam      mọi mảnh → inbox/tinh_linh_1/manh/ (+ manh/dat.json: chỗ đặt mảnh riêng trong thế giới của rig gốc)
    tinh_linh_manh.py ghep     ghép các mảnh ở dáng gốc, đặt cạnh concept → inbox/tinh_linh_1/manh/_so_ghep.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tinh_linh as TL  # noqa: E402

MANH = os.path.join(TL.BASE, "manh")
Z = 4                                    # px mỗi px ảnh vùng của họ = 2 px mỗi đơn vị rig con gốc
PX = 2.0                                 # px mỗi đơn vị (mọi mảnh lưu cùng cỡ này)
THAN = np.array([199, 227, 129])         # màu thân đo trên concept
MUC = np.array([62, 33, 8])              # mực
VANH = (73, 116, 37)                     # vành mắt
NEP = (118, 158, 70)                     # nét nếp gấp
MA = (244, 159, 141)                     # má
DA = {"bung": "P_shentiB", "dau": "P_tou2B", "tay_gan": "P_shouRB", "tay_xa": "P_shouLB"}
VAI = {"tay_gan": (-176.9, 327.3)}       # gốc xương vai bone5 / bone8 ở dáng gốc (thế giới con gốc)
MAT = ["P_SL_bq1", "P_SL_bq2", "P_SL_bq3", "P_SL_bq4", "P_SL_bq5", "P_SL_bq6"]
MIENG = (906.0, 594.0)                   # tâm mồm trên khung concept (giữa hai mắt, thấp hơn đáy mắt)
MIENG_CO = (68.0, 80.0)                  # rộng, cao của mồm há hết (đơn vị rig con gốc)
MA_HA, MA_TO = 0.0, 1.0                   # má hồng: hạ thêm (đơn vị), phóng
TOC_MAU = dict(r=186, b=112, y=345)      # ngưỡng nhận màu lá khi cắt tóc (thân dạng 2: r ≈ 199, b ≈ 129); y: chỉ phía trên mức này (px concept)
if TL.K == 1:                            # DẠNG 1 (hạt mầm): thân nhạt hơn, mầm lục non; số đo trên concept dạng 1
    THAN = np.array([228, 242, 155])
    VANH, NEP, MA = (100, 142, 58), (150, 172, 84), (246, 174, 153)
    MA_HA, MA_TO = 15.0, 1.22            # mặt chibi: mắt to và thấp hơn (rig phóng xương mắt) nên má cũng hạ xuống, to ra
    TOC_MAU = dict(r=212, b=128, y=322)  # cuống (195, 218, 98), lá (128, 181, 77); thân r ≈ 228, b ≈ 155
if TL.K == 3:                            # DẠNG 3 (nở hoa): thân lục đậm (152, 205, 82); số đo trên concept dạng 3
    THAN = np.array([152, 205, 82])
    VANH, NEP, MA = (45, 104, 25), (92, 140, 50), (242, 150, 131)
    # tóc có hoa hồng san hô (247, 116, 97), nhuỵ vàng (252, 194, 43), lá đậm (58, 145, 64), vòng lá (166, 208, 57) rất gần màu thân:
    # nhận từng nhóm màu riêng
    TOC_MAU = dict(y=350, kieu="hoa")


def el(r):
    return TL.el(r)


_C = {}


def by():
    if "by" not in _C:
        _, _, atts = TL.nap()
        _C["by"] = {a["att"]: a for a in atts}
    return _C["by"]


def concept():
    if "con" not in _C:
        _C["con"] = np.asarray(Image.open(os.path.join(TL.TAI, "L1_duyet.png")).convert("RGB")).copy()
    return _C["con"]


def tg_khung():
    """(ox, oy): khung concept = (ox + x·SC, oy − y·SC)."""
    if "tg" not in _C:
        T = TL.khung_T()
        o = T(np.array([0.0, 0.0]))
        _C["tg"] = (float(o[0]), float(o[1]))
    return _C["tg"]


def khung_ra_tg(p):
    ox, oy = tg_khung()
    p = np.asarray(p, float)
    return np.stack([(p[..., 0] - ox) / TL.SC, (oy - p[..., 1]) / TL.SC], -1)


def aff(ten, z=Z):
    """affine pixel ô part (× z) → thế giới dáng gốc: world = [u, v, 1] @ M. In sai số (lưới dáng gốc gần như affine của ảnh vùng)."""
    a = by()[ten]
    uv, _ = TL.luoi(a)
    xy = np.array(a["xy"], float).reshape(-1, 2)
    M, *_ = np.linalg.lstsq(np.c_[uv * z, np.ones(len(uv))], xy, rcond=None)
    return M


def bong(ten, z=Z):
    """hình bóng KÍN của part (làm trơn, không mang nét vẽ của họ), cỡ ảnh vùng × z."""
    g = TL.part_goc(by()[ten])
    al = np.asarray(g.resize((g.width * z, g.height * z), Image.LANCZOS))[..., 3]
    m = (al > 100).astype(np.uint8)
    le = 12 * z
    m = cv2.copyMakeBorder(m, le, le, le, le, cv2.BORDER_CONSTANT, value=0)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2 * z))
    m = (cv2.GaussianBlur(m * 255, (0, 0), 1.6 * z) > 127)[le:-le, le:-le]
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 2:
        m = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    f = cv2.copyMakeBorder(m.astype(np.uint8), 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)      # lấp lỗ kín (lòng trong suốt của lớp thạch)
    cv2.floodFill(f, None, (0, 0), 2)
    return m | (f[1:-1, 1:-1] == 0)


def van():
    """ô vân sáp LÁT ĐƯỢC của thân: ô vuông sạch lớn nhất của màu thân trên concept, phóng về PX px mỗi đơn vị, hai mép hoà chéo."""
    if "van" in _C:
        return _C["van"]
    im = concept().astype(int)
    sach = (np.abs(im - THAN).sum(2) < 110).astype(np.uint8)          # vân chì sáp lệch màu thân tới ~35 mỗi kênh
    sach = cv2.morphologyEx(sach, cv2.MORPH_CLOSE, el(2))
    sach = cv2.erode(sach, el(6))
    dt = cv2.distanceTransform(sach, cv2.DIST_L2, 5)
    y, x = np.unravel_index(int(np.argmax(dt)), dt.shape)
    r = min(110, int(dt[y, x] * 0.70))
    o = concept()[y - r:y + r, x - r:x + r]
    k = PX / TL.SC
    o = cv2.resize(o, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC).astype(np.float32)
    # khử lệch sáng tần số thấp (ô lát lặp lại không thành mảng sáng tối), giữ vân
    o += THAN.astype(np.float32) - cv2.GaussianBlur(o, (0, 0), 22)
    B = max(8, o.shape[0] // 5)
    S = o.shape[0] - B
    ramp = np.linspace(0, 1, B, dtype=np.float32)
    o[:, :B] = o[:, S:S + B] * (1 - ramp)[None, :, None] + o[:, :B] * ramp[None, :, None]
    o = o[:, :S]
    o[:B] = o[S:S + B] * (1 - ramp)[:, None, None] + o[:B] * ramp[:, None, None]
    o = np.clip(o[:S], 0, 255).astype(np.uint8)
    _C["van"] = o
    print(f"ô vân: tâm ({x}, {y}) trên concept, bán kính sạch {dt[y, x]:.0f} px → ô lát {o.shape[1]} × {o.shape[0]} px, màu TB {o.reshape(-1, 3).mean(0).round().tolist()}")
    return o


def lat(wx, wy):
    """màu vân tại toạ độ thế giới (mảng)."""
    o = van()
    return o[np.mod(np.round(-wy * PX).astype(int), o.shape[0]), np.mod(np.round(wx * PX).astype(int), o.shape[1])]


def nhieu(wx, wy, buoc, seed):
    """nhiễu trơn theo toạ độ thế giới, −1..1 (bề dày nét mực rung nhẹ như bút thật)."""
    rs = np.random.RandomState(seed)
    out = 0.0
    for kx, ky in rs.uniform(0.6, 1.4, (4, 2)):
        ph = rs.uniform(0, 6.28, 2)
        out = out + np.sin(wx / buoc * kx * 6.28 + ph[0]) * np.sin(wy / buoc * ky * 6.28 + ph[1])
    return out / 4.0


def luoi_tg(ten, z=Z):
    """(wx, wy) thế giới của từng pixel ô part."""
    m = bong(ten, z)
    M = aff(ten, z)
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]].astype(np.float32)
    return xx * M[0, 0] + yy * M[1, 0] + M[2, 0], xx * M[0, 1] + yy * M[1, 1] + M[2, 1], m


def trong_part(ten, wx, wy, co=0.0, z=Z):
    """điểm thế giới (mảng) có nằm trong hình bóng part `ten` (co vào `co` đơn vị) không."""
    m = bong(ten, z).astype(np.uint8)
    if co > 0:
        m = cv2.erode(m, el(co * PX), borderValue=0)
    Mi = np.linalg.inv(np.c_[aff(ten, z), [0, 0, 1]])
    u = wx * Mi[0, 0] + wy * Mi[1, 0] + Mi[2, 0]
    v = wx * Mi[0, 1] + wy * Mi[1, 1] + Mi[2, 1]
    ui, vi = np.round(u).astype(int), np.round(v).astype(int)
    ok = (ui >= 0) & (vi >= 0) & (ui < m.shape[1]) & (vi < m.shape[0])
    out = np.zeros(wx.shape, bool)
    out[ok] = m[vi[ok], ui[ok]] > 0
    return out


def mat_o_tg():
    """hộp hai con mắt (bq1) trong thế giới: [(x0, y0, x1, y1)] trái → phải."""
    a = by()["P_SL_bq1"]
    g = np.asarray(TL.part_goc(a))[..., 3] > 100
    M = aff("P_SL_bq1", 1)
    n, lab, st, _ = cv2.connectedComponentsWithStats(g.astype(np.uint8), 8)
    hop = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 60:
            continue
        x, y, w, h = st[i, :4]
        P = np.array([[x, y, 1], [x + w, y + h, 1]], float) @ M
        hop.append((min(P[:, 0]), min(P[:, 1]), max(P[:, 0]), max(P[:, 1])))
    return sorted(hop)


def ve_da(ten_minh):
    """một part THÂN: hình bóng part của họ, tô vân lát theo thế giới, viền mực bằng mã. RGBA cỡ ảnh vùng × Z."""
    ten = DA[ten_minh]
    wx, wy, m = luoi_tg(ten)
    # lưới của họ ôm sát hình bóng, có chỗ xén vào trong: cắt hình theo đúng mép lưới rồi mới kẻ mực, không thì chỗ lưới xén mất viền
    at = by()[ten]
    uv, _ = TL.luoi(at)
    hm = np.zeros(m.shape, np.uint8)
    cv2.fillPoly(hm, [np.round(uv[:at.get("hull", len(uv))] * Z).astype(np.int32)], 1)
    if ten_minh == "bung":
        # hình bụng của họ KHUYẾT ba chỗ (hõm bên trái dưới tay trước, hõm trên chỗ đầu ngồi, khấc trên phải): hình họ trong mờ, có tay
        # và đầu che; hình mình đặc, tay vung đi là lộ một mảng lõm (người dùng 2026-11-12: "lõm mất 1 mảng người bên trái").
        # Lấy BAO LỒI của hình bóng (lưới của họ vẫn phủ tới đó) cho bụng tròn đầy
        pts = cv2.findNonZero(m.astype(np.uint8))
        loi = np.zeros(m.shape, np.uint8)
        cv2.fillConvexPoly(loi, cv2.convexHull(pts), 1)
        m = loi.astype(bool)
    m = m & cv2.erode(hm, el(1), borderValue=0).astype(bool)
    im = lat(wx, wy).astype(np.float32)
    dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    day = 13.0 + 2.6 * nhieu(wx, wy, 90.0, 7) + 1.2 * nhieu(wx, wy, 23.0, 11)          # bề dày nét mực (px; 2 px = 1 đơn vị)
    muc = m & (dt < day)
    if ten_minh == "dau":
        trong = trong_part(DA["bung"], wx, wy, co=11.0)                 # mép dưới của đầu nằm trong bụng: không mực
        muc &= ~trong
        # nếp gấp cổ: hai đoạn ngắn màu lục ở hai đầu của mép dưới đó
        nep = m & (dt < 5.0) & trong & ~trong_part(DA["bung"], wx, wy, co=30.0) | (m & (dt < 5.0) & trong)
        xs = wx[m & (dt < 5.0) & trong]
        if len(xs):
            x0, x1 = xs.min(), xs.max()
            nep &= (wx < x0 + 0.17 * (x1 - x0)) | (wx > x1 - 0.13 * (x1 - x0))
            im[nep] = NEP
        # má hồng dưới hai mắt
        hop = mat_o_tg()
        (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = hop[0], hop[-1]
        day_mat = min(ay0, by0)
        for cx, cy, rx, ry in ((ax0 + 0.26 * (ax1 - ax0), day_mat - 26.0 - MA_HA, 0.30 * (ax1 - ax0) * MA_TO, 13.0 * MA_TO),
                               (bx0 + 0.62 * (bx1 - bx0), day_mat - 22.0 - MA_HA, 0.42 * (bx1 - bx0) * MA_TO, 11.0 * MA_TO)):
            e = ((wx - cx) / rx) ** 2 + ((wy - cy) / ry) ** 2
            a_ = np.clip((1.0 - e) * 6.0, 0, 1)[..., None] * (m & ~muc)[..., None]
            im = im * (1 - a_) + (np.array(MA, np.float32) + 5.0 * nhieu(wx, wy, 5.0, 3)[..., None]) * a_
    if ten_minh in VAI:
        # đầu vai (chỗ tay mọc ra từ thân): không mực ở phần nằm trong thân, để lúc tay vung đi chỗ khác gốc tay hoà vào thân, không
        # để lại một mẩu viền lồi trên mép bụng
        vx, vy = VAI[ten_minh]
        trong = trong_part(DA["bung"], wx, wy, co=7.0) | trong_part(DA["dau"], wx, wy, co=7.0)
        muc &= ~(trong & (np.hypot(wx - vx, wy - vy) < 78.0))
    tm = MUC.astype(np.float32) + 7.0 * nhieu(wx, wy, 6.0, 5)[..., None]
    im[muc] = tm[muc]
    al = cv2.GaussianBlur(m.astype(np.float32) * 255, (0, 0), 0.9)
    return Image.fromarray(np.dstack([np.clip(im, 0, 255).astype(np.uint8), np.clip(al, 0, 255).astype(np.uint8)]), "RGBA")


def ve_mat(ten):
    """một bộ mắt đúng khung part: chỗ họ tô trắng → TRẮNG, phần còn lại của hình bóng (vành, nét) → màu vành lục. Không mực."""
    g = TL.part_goc(by()[ten])
    a = np.asarray(g.resize((g.width * Z, g.height * Z), Image.LANCZOS)).astype(int)
    al = cv2.GaussianBlur((a[..., 3] > 100).astype(np.float32), (0, 0), 0.6 * Z)
    m = al > 0.5
    trang = cv2.GaussianBlur(((a[..., :3].min(2) > 185) & (a[..., 3] > 150)).astype(np.float32), (0, 0), 0.6 * Z) > 0.5
    # vành của họ dày ~12 đơn vị; concept của mình vành mảnh hơn (~7): nới lòng trắng ra 2,5 đơn vị, vẫn chừa vành ≥ 6,5 đơn vị
    trang = cv2.dilate((trang & m).astype(np.uint8), el(2.5 * PX)).astype(bool) & cv2.erode(m.astype(np.uint8), el(6.5 * PX), borderValue=0).astype(bool)
    im = np.zeros(m.shape + (3,), np.float32)
    im[:] = VANH
    t = cv2.GaussianBlur(trang.astype(np.float32), (0, 0), 0.8)[..., None]
    im = im * (1 - t) + 255.0 * t
    return Image.fromarray(np.dstack([im.astype(np.uint8), (np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8), 0, 1) * 255).astype(np.uint8)]), "RGBA")


def _cat(mask, le=6):
    """cắt một mảnh khỏi concept theo mặt nạ (px concept): RGBA phóng về PX px mỗi đơn vị + chỗ góc trên trái trong thế giới."""
    ys, xs = np.nonzero(mask)
    x0, y0, x1, y1 = xs.min() - le, ys.min() - le, xs.max() + le + 1, ys.max() + le + 1
    rgb = concept()[y0:y1, x0:x1]
    al = cv2.GaussianBlur(mask[y0:y1, x0:x1].astype(np.float32) * 255, (0, 0), 0.8)
    k = PX / TL.SC
    im = Image.fromarray(np.dstack([rgb, al.astype(np.uint8)]), "RGBA").convert("RGBa")
    im = im.resize((int(round(im.width * k)), int(round(im.height * k))), Image.LANCZOS).convert("RGBA")
    goc = khung_ra_tg(np.array([x0, y0], float))
    return im, [float(goc[0]), float(goc[1])]


def cat_toc():
    """TÓC = mầm hai lá + cuống + vòng lá con: mọi vùng màu lá (lục đậm, lục non) phía trên đầu + nét mực bao quanh chúng."""
    im = concept().astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    muc = im.max(2) < 100
    yy = np.arange(im.shape[0])[:, None]
    if TOC_MAU.get("kieu") == "hoa":
        mau = (r < 112) | (r > 214) | ((b < 68) & (r > 156) & (g > 185))      # lá đậm | hoa, nhuỵ | cuống, vòng lá
        la = ~muc & (im.min(2) < 225) & mau & (yy < TOC_MAU["y"])
    else:
        la = ~muc & (im.min(2) < 225) & (r < TOC_MAU["r"]) & (b < TOC_MAU["b"]) & (g > 110) & (yy < TOC_MAU["y"])        # mọi màu lá, cuống
    la = cv2.morphologyEx(la.astype(np.uint8), cv2.MORPH_OPEN, el(2))
    n, lab, st, _ = cv2.connectedComponentsWithStats(la, 8)
    la = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 300])
    ke = cv2.dilate(la.astype(np.uint8), el(11)).astype(bool) & muc                       # nét mực sát các vùng lá
    m = cv2.morphologyEx((la | ke).astype(np.uint8), cv2.MORPH_CLOSE, el(4))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, el(2)).astype(bool)
    # lấp lỗ kín (gân lá sáng, khe nhỏ)
    f = m.astype(np.uint8).copy()
    cv2.floodFill(f, None, (0, 0), 2)
    m |= f == 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    m = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return _cat(m), m


def cat_trong():
    """thứ nằm TRONG bụng: cụm hạt giống (lớn nhất) và các bong bóng: điểm trong lòng bụng khác màu thân (nét lục, nâu, kem), lấp lòng."""
    im = concept().astype(int)
    muc = im.max(2) < 100
    than = np.abs(im - THAN).sum(2) < 60
    yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]]
    vung = (xx > 600) & (xx < 980) & (yy > 615) & (yy < 905)                # lòng bụng (đọc trên concept; không chạm tay, viền)
    khac = vung & ~than & ~muc & (im.min(2) < 235)
    khac = cv2.morphologyEx(khac.astype(np.uint8), cv2.MORPH_CLOSE, el(3))
    f = khac.copy()
    cv2.floodFill(f, None, (0, 0), 2)
    khac = (khac > 0) | (f == 0)
    khac = cv2.morphologyEx(khac.astype(np.uint8), cv2.MORPH_OPEN, el(2))
    n, lab, st, cen = cv2.connectedComponentsWithStats(khac, 8)
    ds = sorted([i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 250], key=lambda i: -st[i, cv2.CC_STAT_AREA])
    out = []
    for j, i in enumerate(ds[:4]):
        m = cv2.dilate((lab == i).astype(np.uint8), el(2)).astype(bool)
        out.append((("hat" if j == 0 else f"bong{j}"), _cat(m), m))
    return out


def ve_mieng():
    """mồm tròn kiểu Tí Tách: bầu dục sẫm, phía dưới một mảng lưỡi nhạt; không viền mực. RGBA, PX px mỗi đơn vị."""
    S = 4
    w, h = int(MIENG_CO[0] * PX), int(MIENG_CO[1] * PX)
    yy, xx = np.mgrid[0:h * S, 0:w * S].astype(np.float32) / S
    cx, cy = w / 2, h / 2
    e = ((xx - cx) / (w / 2 - 1.5)) ** 2 + ((yy - cy) / (h / 2 - 1.5)) ** 2
    trong = e < 1.0
    im = np.zeros((h * S, w * S, 3), np.float32)
    im[:] = (44, 72, 30)                                             # lòng mồm lục sẫm
    lx, ly, lr = cx + w * 0.04, cy + h * 0.30, w * 0.36              # lưỡi: mảng tròn nhạt ở đáy
    luoi_ = (((xx - lx) / lr) ** 2 + ((yy - ly) / (lr * 0.82)) ** 2 < 1.0) & trong
    im[luoi_] = (233, 142, 126)
    al = trong.astype(np.float32) * 255
    out = np.dstack([im, al]).astype(np.uint8)
    return Image.fromarray(out, "RGBA").convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")


def lam():
    os.makedirs(MANH, exist_ok=True)
    dat = {}
    for t in DA:
        g = ve_da(t)
        g.save(os.path.join(MANH, t + ".png"))
        M = aff(DA[t])
        r = np.abs(np.c_[TL.luoi(by()[DA[t]])[0] * Z, np.ones(len(TL.luoi(by()[DA[t]])[0]))] @ M - np.array(by()[DA[t]]["xy"], float).reshape(-1, 2)).max()
        print(f"  {t}: {g.size}, lưới dáng gốc lệch affine tối đa {r:.2f} đơn vị")
    for i, t in enumerate(MAT, 1):
        ve_mat(t).save(os.path.join(MANH, f"mat{i}.png"))
    (g, goc), _ = cat_toc()
    g.save(os.path.join(MANH, "toc.png"))
    dat["toc"] = {"goc": goc, "co": list(g.size)}
    print(f"  toc: {g.size}, góc trên trái ở thế giới {np.round(goc, 1).tolist()}")
    for ten, (g, goc), _ in cat_trong():
        g.save(os.path.join(MANH, ten + ".png"))
        dat[ten] = {"goc": goc, "co": list(g.size)}
        print(f"  {ten}: {g.size}, góc trên trái ở thế giới {np.round(goc, 1).tolist()}")
    g = ve_mieng()
    g.save(os.path.join(MANH, "mieng.png"))
    c = khung_ra_tg(np.array(MIENG))
    dat["mieng"] = {"tam": [float(c[0]), float(c[1])], "co": list(g.size)}
    dat["px"] = PX
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    print(os.path.join(MANH, "dat.json"))


def ghep():
    """ghép các mảnh ở dáng gốc (đúng thứ tự vẽ của rig mình) đặt cạnh concept → manh/_so_ghep.png."""
    dat = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    X0, X1, Y0, Y1 = -420.0, 420.0, -30.0, 830.0
    Wd, Hd = int((X1 - X0) * PX), int((Y1 - Y0) * PX)
    can = Image.new("RGBA", (Wd, Hd), (255, 255, 255, 255))

    def dan_part(file, ten):
        g = Image.open(os.path.join(MANH, file + ".png")).convert("RGBa")
        M = aff(ten)
        A = np.array([[M[0, 0] * PX, M[1, 0] * PX, (M[2, 0] - X0) * PX], [-M[0, 1] * PX, -M[1, 1] * PX, (Y1 - M[2, 1]) * PX]], np.float32)
        lay = cv2.warpAffine(np.asarray(g), A, (Wd, Hd), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        can.alpha_composite(Image.fromarray(lay, "RGBa").convert("RGBA"))

    def dan_rieng(ten, goc=None):
        g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
        gx, gy = goc or dat[ten]["goc"]
        can.alpha_composite(g, (int(round((gx - X0) * PX)), int(round((Y1 - gy) * PX))))

    dan_part("tay_xa", DA["tay_xa"])
    dan_part("bung", DA["bung"])
    for t in [k for k in dat if k == "hat" or k.startswith("bong")]:
        dan_rieng(t)
    dan_part("dau", DA["dau"])
    dan_part("mat1", "P_SL_bq1")
    dan_part("tay_gan", DA["tay_gan"])
    dan_rieng("toc")
    a = can.convert("RGB")
    b = can.copy()
    mg = Image.open(os.path.join(MANH, "mieng.png"))
    tx, ty = dat["mieng"]["tam"]
    b.alpha_composite(mg, (int(round((tx - X0) * PX - mg.width / 2)), int(round((Y1 - ty) * PX - mg.height / 2))))
    c = Image.fromarray(concept())
    k = Hd / c.height
    c = c.resize((int(c.width * k), Hd), Image.LANCZOS).crop((int(c.width * k * 0.2), 0, int(c.width * k * 0.8), Hd))
    out = Image.new("RGB", (Wd * 2 + c.width, Hd), "white")
    out.paste(c, (0, 0))
    out.paste(a, (c.width, 0))
    out.paste(b.convert("RGB"), (c.width + Wd, 0))
    out = out.resize((out.width // 2, out.height // 2), Image.LANCZOS)
    out.save(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_so_ghep.png"), out.size, "(concept | ghép dáng gốc | ghép có mồm)")
    # sáu bộ mắt cạnh nhau
    ms = [Image.open(os.path.join(MANH, f"mat{i}.png")) for i in range(1, 7)]
    sh = Image.new("RGB", (sum(m.width for m in ms) + 70, max(m.height for m in ms) + 20), tuple(int(v) for v in THAN))
    x = 10
    for m in ms:
        sh.paste(m, (x, 10), m)
        x += m.width + 10
    sh.save(os.path.join(MANH, "_mat.png"))
    print(os.path.join(MANH, "_mat.png"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["lam"]:
        lam()
        ghep()
    elif a[:1] == ["ghep"]:
        ghep()
    else:
        print(__doc__)
