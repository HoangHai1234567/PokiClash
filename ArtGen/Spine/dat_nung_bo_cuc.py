# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của chiến binh đất nung (dat_nung, tướng thứ 8 đảo Hỏa): khối từng part của rig monster_3625 ở khung 0 idle_01, tô phẳng
theo màu của THIẾT KẾ MÌNH. Mọi part của con gốc là mảnh CỨNG bám một xương (trừ kiếm hai xương, quầng lõi hai xương) nên hình bóng
từng mảnh của mình tự do; chỉ giữ chỗ đặt, cỡ, thứ tự chồng.

Giữ của con gốc: cách dựng (bộ giáp rỗng lơ lửng không chân, lõi tròn giữa ngực, hai giáp vai lớn, tay gần vắt ngang phía dưới nắm
kiếm dựng chéo bên trái, tay xa xoè ngón phía sau kiếm, chùm phiến đá xoè sau lưng). Đòn của con gốc đánh về bên PHẢI.
Đổi dáng ngay từ sơ đồ (vẽ bằng mã):
  - đầu thú hai sừng dài           → đầu TƯỢNG BINH đất nung: khối đầu tròn vuông, búi tóc lệch trên đỉnh, mặt quay sang PHẢI (phía địch)
  - kiếm mảnh hoa văn chữ triện      → kiếm BẢN RỘNG bằng đá dung nham đen, rãnh dung nham chạy giữa, chắn tay đất nung, chuôi có khâu tròn
  - chín phiến đá cong như sừng     → chín MẢNH ĐÁ DUNG NHAM thẳng, nhọn (như mảnh vỏ núi lửa vỡ), mỗi mảnh một khe dung nham
  - giáp vai khắc xoắn chữ triện     → giáp vai ĐẤT NUNG xếp vảy ngói (tả trong prompt)

    dat_nung_bo_cuc.py [tuong_binh|lo_gom]   → inbox/dat_nung_1/mau/bo_cuc_<hướng>.png (+ bo_cuc_hop_<hướng>.json)
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dat_nung as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
SC = 0.74                                        # đơn vị rig con gốc → pixel khung concept
INK = (43, 33, 24)
ATT = "att_idle0.json"
# bảng màu ĐỀ XUẤT của Claude (người dùng dặn: đất nung, đá dung nham, lõi dung nham), chờ duyệt concept
PALS = {
    # tượng binh: đất nung cam, đá dung nham nâu than
    "tuong_binh": dict(dat=(200, 104, 60), dat_trong=(150, 72, 44), nham=(74, 62, 60), lava=(238, 122, 34), loi=(255, 214, 74),
                       men=(200, 104, 60)),
    # lò gốm: gạch nung đỏ sẫm, vành men ngà, đá dung nham đen ánh tím
    "lo_gom": dict(dat=(168, 67, 47), dat_trong=(120, 48, 40), nham=(62, 58, 68), lava=(242, 140, 40), loi=(255, 224, 102),
                   men=(232, 216, 176)),
}
PAL = dict(PALS["tuong_binh"])

NHOM = {  # slot → nhóm màu
    "dat": ["P_jianjiaL1", "P_jianjiaR1", "P_dun01", "P_dun02", "P_dun03", "P_shouL2_1", "P_shouL2_2", "P_shouL4_1",
            "P_shouR2", "P_shouR4"],
    "dat_trong": ["P_jianjiaL2", "P_jianjiaR2", "P_jianjiaL3", "P_jianjiaR3", "P_jianjiaL4", "P_jianjiaL5", "P_jianjiaR4",
                  "P_jianjiaR5", "P_shouL3_1"],
    "nham": ["P_shenti1_1", "P_shenti1_2", "P_shenti1_3", "P_shouL1", "P_shouL3_2", "P_shouL3_3", "P_shouR3", "P_shouL4_2"],
    "lava": ["P_huoyan20"], "loi": ["P_huoyan17"],
}
MANH_DA = ["P_dun04", "P_dun05", "P_dun06", "P_dun07", "P_dun08", "P_dun09", "P_dun10", "P_dun11", "P_dun12"]
BO = {"P_tou2", "P_tou3", "wangge"}


def nhom_cua(slot):
    for k, v in NHOM.items():
        if slot in v:
            return k
    if slot.startswith("P_shouR4_"):
        return "nham"                             # mười đốt ngón tay xa
    return None


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def nap():
    _, imgs, atts = G.nap(ATT)
    return imgs, [a for a in atts if a["slot"] not in BO and a.get("alpha", 1) > 0.05]


def khung_T(atts):
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = (H + (y1 - y0) * SC) / 2 + y0 * SC
    return (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)), (ox, oy)


def bong(a, T, tron=4.0):
    """hình bóng KÍN của một part ở khung 0 idle trên khung concept (phóng S2), làm trơn: chỉ còn khối."""
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def truc(m):
    """trục chính của một khối: (tâm, vectơ dọc, vectơ ngang, [a0, a1] dọc, nửa bề ngang lớn nhất)."""
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    u, v = vt[0], vt[1]
    a = (P - c) @ u
    b = (P - c) @ v
    return c, u, v, (np.percentile(a, 1), np.percentile(a, 99)), float(np.percentile(np.abs(b), 97))


def da_ve(can, pts, mau, day=6):
    pts = np.array(pts, np.int32)
    cv2.fillPoly(can, [pts], mau, cv2.LINE_AA)
    cv2.polylines(can, [pts], True, INK, day * S2 // 2, cv2.LINE_AA)


def manh_da(can, m, tam_than, seed):
    """thay một phiến cong của con gốc bằng một MẢNH ĐÁ thẳng nhọn cùng chỗ, cùng dài, cùng bề ngang: gốc bè ở phía thân, mũi nhọn chĩa
    ra ngoài, một khe dung nham dọc giữa."""
    c, u, v, (a0, a1), hw = truc(m)
    if np.linalg.norm(c + u * a1 - tam_than) < np.linalg.norm(c + u * a0 - tam_than):
        u, a0, a1 = -u, -a1, -a0                  # a0 = đầu gần thân
    rng = np.random.default_rng(seed)
    L = a1 - a0
    hw = max(hw * 0.92, 26)
    k = rng.uniform(-0.25, 0.25)

    def P(t, s):
        return c + u * (a0 + L * t) + v * (hw * s)

    pts = [P(0.02, -0.72), P(0.30 + 0.1 * k, -1.0), P(0.72, -0.62), P(1.0, 0.10 * k * 4), P(0.66, 0.70), P(0.26 - 0.1 * k, 1.0),
           P(0.0, 0.62), P(0.06, 0.05)]
    da_ve(can, pts, PAL["nham"])
    khe = np.array([P(0.16, 0.05), P(0.36, -0.16), P(0.50, 0.12), P(0.70, -0.05)], np.int32)
    cv2.polylines(can, [khe], False, PAL["lava"], 7 * S2 // 2 * 2, cv2.LINE_AA)
    return pts


def kiem(can, T, bones):
    """kiếm bản rộng của mình trên trục xương bàn tay (bone11) → mũi (bone185) ở khung 0 idle."""
    b = {x["name"]: x for x in bones}
    g = T(np.array([b["bone11"]["x"], b["bone11"]["y"]])) * S2
    mu = T(np.array([b["bone185"]["x"], b["bone185"]["y"]])) * S2
    u = (mu - g) / np.linalg.norm(mu - g)
    v = np.array([-u[1], u[0]])
    L = np.linalg.norm(mu - g) * 1.0

    def P(t, s):
        return g + u * (L * t) + v * (L * s)

    # chuôi (từ dưới bàn tay tới chắn tay), khâu tròn cuối chuôi
    da_ve(can, [P(-0.15, -0.022), P(0.10, -0.022), P(0.10, 0.022), P(-0.15, 0.022)], PAL["nham"])
    cv2.circle(can, tuple(P(-0.185, 0).astype(int)), int(L * 0.048), INK, -1, cv2.LINE_AA)
    cv2.circle(can, tuple(P(-0.185, 0).astype(int)), int(L * 0.048) - 6 * S2 // 2 * 2, PAL["dat"], -1, cv2.LINE_AA)
    cv2.circle(can, tuple(P(-0.185, 0).astype(int)), int(L * 0.016), INK, -1, cv2.LINE_AA)
    # bản kiếm: rộng dần về phía mũi rồi vát nhọn
    ban = [P(0.14, -0.060), P(0.62, -0.082), P(0.84, -0.090), P(1.0, 0.0), P(0.84, 0.090), P(0.62, 0.082), P(0.14, 0.060)]
    da_ve(can, ban, PAL["nham"])
    ranh = [P(0.19, -0.020), P(0.80, -0.030), P(0.90, 0.0), P(0.80, 0.030), P(0.19, 0.020)]
    cv2.fillPoly(can, [np.array(ranh, np.int32)], PAL["lava"], cv2.LINE_AA)
    cv2.polylines(can, [np.array([P(0.22, 0.0), P(0.82, 0.0)], np.int32)], False, PAL["loi"], 5 * S2 // 2 * 2, cv2.LINE_AA)
    # chắn tay đất nung: khối thang, hai vai vểnh
    da_ve(can, [P(0.07, -0.105), P(0.11, -0.125), P(0.165, -0.07), P(0.165, 0.07), P(0.11, 0.125), P(0.07, 0.105)], PAL["dat"])
    return dict(goc=(g / S2).tolist(), mui=(mu / S2).tolist())


def dau(can, m, kieu="tuong_binh"):
    """đầu của mình thay đầu thú hai sừng. tuong_binh: khối đầu tượng binh đất nung, búi tóc lệch về sau (trái), mặt quay phải.
    lo_gom: mũ là chiếc VÒ gốm úp ngược: vòm tròn, vành men ở đáy, khe chữ T lộ dung nham, hai quai nhỏ."""
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.50, y0 + h * 0.66
    rx, ry = w * 0.34, h * 0.235
    if kieu == "lo_gom":
        cy -= ry * 0.15
        ry *= 1.18
        for sx in (-1, 1):                                               # hai quai vò
            c = (int(cx + sx * rx * 1.0), int(cy + ry * 0.05))
            cv2.ellipse(can, c, (int(rx * 0.22), int(ry * 0.30)), 0, 0, 360, INK, -1, cv2.LINE_AA)
            cv2.ellipse(can, c, (int(rx * 0.22) - 12, int(ry * 0.30) - 12), 0, 0, 360, PAL["dat_trong"], -1, cv2.LINE_AA)
        top = cv2.ellipse2Poly((int(cx), int(cy + ry * 0.55)), (int(rx), int(ry * 1.55)), 0, 180, 360, 6).astype(float)
        pts = np.concatenate([top, [[cx + rx * 1.08, cy + ry * 0.62], [cx + rx * 1.08, cy + ry], [cx - rx * 1.08, cy + ry],
                                    [cx - rx * 1.08, cy + ry * 0.62]]])
        da_ve(can, pts, PAL["dat"])
        vanh = np.array([[cx - rx * 1.08, cy + ry * 0.62], [cx + rx * 1.08, cy + ry * 0.62], [cx + rx * 1.08, cy + ry],
                         [cx - rx * 1.08, cy + ry]], np.int32)
        da_ve(can, vanh, PAL["men"])
        tx = cx + rx * 0.30                                              # khe chữ T lệch phải (mặt quay phải)
        T_ = np.array([[tx - rx * 0.55, cy - ry * 0.30], [tx + rx * 0.55, cy - ry * 0.30], [tx + rx * 0.55, cy - ry * 0.02],
                       [tx + rx * 0.13, cy - ry * 0.02], [tx + rx * 0.13, cy + ry * 0.50], [tx - rx * 0.13, cy + ry * 0.50],
                       [tx - rx * 0.13, cy - ry * 0.02], [tx - rx * 0.55, cy - ry * 0.02]], np.int32)
        cv2.fillPoly(can, [T_], PAL["loi"], cv2.LINE_AA)
        cv2.polylines(can, [T_], True, INK, 6, cv2.LINE_AA)
        return [int((cx - rx * 1.25) / S2), int((cy - ry) / S2), int((cx + rx * 1.25) / S2), int((cy + ry) / S2)]
    # búi tóc (đá dung nham) sau đỉnh đầu, có đai đất nung
    bx, by = cx - rx * 0.55, cy - ry * 1.25
    cv2.ellipse(can, (int(bx), int(by)), (int(rx * 0.50), int(ry * 0.52)), -25, 0, 360, INK, -1, cv2.LINE_AA)
    cv2.ellipse(can, (int(bx), int(by)), (int(rx * 0.50) - 12, int(ry * 0.52) - 12), -25, 0, 360, PAL["nham"], -1, cv2.LINE_AA)
    pts = cv2.ellipse2Poly((int(cx), int(cy)), (int(rx), int(ry)), 0, 0, 360, 6).astype(float)
    pts[:, 0] = cx + np.sign(pts[:, 0] - cx) * np.abs((pts[:, 0] - cx) / rx) ** 0.62 * rx
    pts[:, 1] = cy + np.sign(pts[:, 1] - cy) * np.abs((pts[:, 1] - cy) / ry) ** 0.62 * ry
    da_ve(can, pts, PAL["dat"])
    cv2.line(can, (int(cx - rx * 0.93), int(cy - ry * 0.42)), (int(cx + rx * 0.93), int(cy - ry * 0.42)), PAL["dat_trong"], 22, cv2.LINE_AA)
    for ex, ew in ((0.18, 0.21), (0.66, 0.17)):
        e = np.array([[cx + rx * (ex - ew), cy - ry * 0.02], [cx + rx * (ex + ew), cy - ry * 0.20], [cx + rx * (ex + ew * 0.8), cy + ry * 0.14],
                      [cx + rx * (ex - ew * 0.6), cy + ry * 0.20]], np.int32)
        cv2.fillPoly(can, [e], PAL["loi"], cv2.LINE_AA)
        cv2.polylines(can, [e], True, INK, 6, cv2.LINE_AA)
    return [int((bx - rx * 0.5) / S2), int((by - ry * 0.55) / S2), int((cx + rx) / S2), int((cy + ry) / S2)]


def bo_cuc(kieu="tuong_binh", luu=True):
    PAL.clear()
    PAL.update(PALS[kieu])
    imgs, atts = nap()
    T, goc = khung_T(atts)
    D = json.load(open(os.path.join(G.scan(), ATT), encoding="utf-8"))
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    lava = next(a for a in atts if a["slot"] == "P_huoyan20")
    tam_than = T(np.array(lava["xy"], float).reshape(-1, 2)).mean(0) * S2
    for i, a in enumerate(atts):
        s = a["slot"]
        if s == "shadow":
            continue
        if s == "P_wuqi":
            hop["kiem"] = kiem(can, T, D["bones"])
            continue
        nho = s.startswith("P_shouR4_") or s in ("P_huoyan17", "P_shouL4_2")
        m = bong(a, T, 2.0 if nho else 4.0)
        if not m.any():
            continue
        if s == "P_tou":
            hop[s] = dau(can, m, kieu)
            continue
        if s in MANH_DA:
            pts = np.array(manh_da(can, m, tam_than, 100 + i))
            hop[s] = [int(pts[:, 0].min() / S2), int(pts[:, 1].min() / S2), int(pts[:, 0].max() / S2), int(pts[:, 1].max() / S2)]
            continue
        nh = nhom_cua(s)
        if nh is None:
            print("chưa xếp nhóm:", s)
            nh = "dat"
        can[m] = PAL["men"] if s in ("P_jianjiaL3", "P_jianjiaR3") else PAL[nh]
        if nh == "lava":                                  # vài mảng vỏ nguội trôi trên mặt dung nham
            ys, xs = np.nonzero(m)
            cx, cy, r = xs.mean(), ys.mean(), (xs.max() - xs.min()) / 2
            for dx, dy, rr in ((-0.45, -0.35, 0.16), (0.30, -0.55, 0.12), (-0.10, 0.50, 0.14)):
                cv2.ellipse(can, (int(cx + dx * r), int(cy + dy * r)), (int(rr * r * 1.3), int(rr * r * 0.7)), 20, 0, 360, PAL["lava"], -1)
        can[vien(m, 3 if nho else 6)] = INK
        ys, xs = np.nonzero(m)
        hop[s] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(G.MAU, exist_ok=True)
        out.save(os.path.join(G.MAU, f"bo_cuc_{kieu}.png"))
        hop["_khung"] = dict(sc=SC, ox=float(goc[0]), oy=float(goc[1]))
        json.dump(hop, open(os.path.join(G.MAU, f"bo_cuc_hop_{kieu}.json"), "w"), indent=0)
        print(os.path.join(G.MAU, f"bo_cuc_{kieu}.png"))
        for k, v in hop.items():
            print(f"  {k:14s} {v}")
    return out


if __name__ == "__main__":
    for k_ in (sys.argv[1:] or list(PALS)):
        bo_cuc(k_)
