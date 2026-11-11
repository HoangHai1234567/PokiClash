# -*- coding: utf-8 -*-
"""Miệng và mắt theo luật (skill-petclash 7.2, mo_xe_quai_nhieu_dau mục 3b, 9 "Lỗi đã gặp"):

- THỊT TRONG MIỆNG THUỘC HÀM DƯỚI, há theo hàm. Lòng miệng là lưới ô (mặc định 5×3): hàng dưới bám xương hàm 100%; hàng trên chỉ
  bám đầu ở sát bản lề (màng khoé miệng), ra phía mõm thì theo hàm luôn (0 / 0,35 / 0,8 / 1 / 1) và mỏng dần. Vẽ SAU đầu và hàm
  (slot đứng trước slot hàm, slot đầu): khép miệng thì nấp sau, há thì lộ dần. Không mảng thịt nào bám đầu mà thò khỏi hàm trên.
- Hàm dưới có thể là lưới hai xương: sau bản lề bám xương cổ/đầu (cổ họng), trước bản lề bám xương hàm, giữa hoà: há miệng thì da
  cổ họng giãn ra, không hở ở bản lề.
- Mí mắt: fit_lid dò góc, tỉ lệ, độ lệch cho mí PHỦ KÍN con mắt (cả vùng màu liền với điểm hạt, bao lồi, nới vài px cho hết viền
  mực), ít lòi ra ngoài đầu, tránh gờ mày; in "còn hở N px" (phải 0) rồi soi ảnh cận phóng 4 lần.
"""
import math

import numpy as np
from PIL import Image

from . import anh, luoi, trongso
from .khung import Dat


def long_mieng(sk, slot, ten_anh, dau, ham, ban_le, mui, cot=5, hang=3, tren=(-0.04, -0.06, -0.10, -0.14, -0.18), duoi=-0.31,
               doc=(-0.08, 1.0), q_tren=(0.0, 0.35, 0.8, 1.0, 1.0), uv=(0.10, 0.97, 0.03, 0.97), ten=None):
    """lòng miệng: lưới cot × hang trên ảnh lòng miệng, đặt trong hệ "bản lề → mõm" ở dáng gốc (thế giới rig).
    ban_le, mui: điểm thế giới (bản lề hàm, chóp mõm khi khép); dai = |mui - ban_le|. Cột c ở x = doc[0]..doc[1] (tỉ lệ dai, dọc
    trục bản lề → mõm); mép trên cột c lệch tren[c]·dai, mép dưới duoi·dai (âm = phía dưới trục, theo hướng mõm sang phải).
    q_tren[c]: phần hàm của đỉnh hàng trên cột c (hàng dưới luôn 1). uv: phần ảnh dùng (u0, u1, v0, v1): lấy cả viền mực."""
    im = sk.images[ten_anh]
    H = np.asarray(ban_le, float)
    d = np.asarray(mui, float) - H
    dai = float(np.hypot(*d))
    u = d / max(1e-9, dai)
    nrm = np.array([-u[1], u[0]])  # vuông góc trục, phía "trên" khi mõm chĩa sang phải
    tr = np.interp(np.linspace(0, 1, cot), np.linspace(0, 1, len(tren)), tren)
    qt = np.interp(np.linspace(0, 1, cot), np.linspace(0, 1, len(q_tren)), q_tren)
    L = luoi.luoi_o(im.width, im.height, cot, hang, *uv, ten=ten or slot)
    V, Wt = [], []
    for r in range(hang):
        k = r / (hang - 1)
        for c in range(cot):
            fu = c / (cot - 1)
            x = (doc[0] + (doc[1] - doc[0]) * fu) * dai
            y = (tr[c] + (duoi - tr[c]) * k) * dai
            V.append(H + u * x + nrm * y)
            wj = qt[c] + (1 - qt[c]) * k
            Wt.append({dau: 1 - wj, ham: wj} if 0 < wj < 1 else ({ham: 1.0} if wj >= 1 else {dau: 1.0}))
    sk.luoi_gan(slot, ten_anh, L, Wt, the_gioi=np.array(V), ten=ten)
    return L


def ham_hai_xuong(Q, ban_le, mui, xuong_co, xuong_ham, u0=-0.12, u1=0.15):
    """trọng số hàm dưới hai xương: Q đỉnh thế giới (N, 2); sau bản lề (u < u0, tỉ lệ dai bản lề → mõm) bám xương cổ/đầu, trước
    (u > u1) bám xương hàm, giữa hoà trơn."""
    return trongso.theo_truc(Q, ban_le, mui, xuong_co, xuong_ham, u0, u1)


def vung_mat(dau, hat, nguong=48, noi=5, hop=None):
    """mặt nạ con mắt trên ảnh đầu: vùng liền màu gần màu ở điểm hạt (x, y px), giới hạn trong hop (x0, y0, x1, y1) nếu có (không
    dính sừng cùng màu), lấy bao lồi (gồm đồng tử, chấm sáng bên trong), nới noi px cho hết viền mực."""
    a = np.asarray(dau.convert("RGBA")).astype(int)
    Hh, Ww = a.shape[:2]
    hx, hy = int(hat[0]), int(hat[1])
    c0 = a[hy, hx, :3]
    near = (np.abs(a[..., :3] - c0).sum(2) < nguong * 1.7) & (a[..., 3] > 128)
    if hop:
        box = np.zeros_like(near)
        x0, y0, x1, y1 = [int(v) for v in hop]
        box[max(0, y0):y1, max(0, x0):x1] = True
        near &= box
    lab, _ = anh.thanh_phan(near)
    if lab[hy, hx] == 0:
        raise ValueError(f"điểm hạt mắt ({hx}, {hy}) không nằm trong vùng màu nào")
    ys, xs = np.nonzero(lab == lab[hy, hx])
    hull = anh.bao_loi(np.stack([xs + 0.5, ys + 0.5], 1))
    eye = anh.to_da_giac((Hh, Ww), hull)
    return anh.gian(eye, noi, tron=True)


def fit_lid(dau, mi, hat=None, mat=None, tranh=None, nguong=48, noi=5, hop=None, goc=(-34, 10, 4), ti=(1.0, 2.8, 0.15), doi=12, ten=""):
    """dò chỗ đặt mí (ảnh mi) trên ảnh đầu (dau) cho phủ kín con mắt. hat: điểm trong mống mắt (px ảnh đầu); mat: mặt nạ con
    mắt nếu đã có (bỏ qua hat). tranh: mặt nạ vùng mí không nên đè (gờ mày). goc (từ, tới, bước) độ, dương ngược kim trên màn hình;
    ti (từ, tới, bước) theo bề rộng mắt / bề rộng mí; doi: dời tâm ±px. Trả (cx, cy, góc, tỉ lệ, còn hở) với cx, cy là tâm mí
    trên ảnh đầu. In "còn hở N px" (phải là 0)."""
    eye = mat if mat is not None else vung_mat(dau, hat, nguong, noi, hop)
    head = np.asarray(dau.convert("RGBA"))[..., 3] > 128
    la = anh.co(np.asarray(mi.convert("RGBA"))[..., 3] > 150, 1)
    lim = Image.fromarray((la * 255).astype(np.uint8))
    ys, xs = np.nonzero(eye)
    ex, ey = float(xs.mean()), float(ys.mean())
    ew = float(xs.max() - xs.min() + 1)
    need = int(eye.sum())
    R = int(max(mi.width, mi.height) * ti[1] * ew / mi.width / 2 + doi + 4)
    wx0, wy0 = int(max(0, ex - R)), int(max(0, ey - R))
    wx1, wy1 = int(min(dau.width, ex + R)), int(min(dau.height, ey + R))
    E = eye[wy0:wy1, wx0:wx1]
    Hd = head[wy0:wy1, wx0:wx1]
    Tr = tranh[wy0:wy1, wx0:wx1] if tranh is not None else None
    ww, hh = wx1 - wx0, wy1 - wy0
    lc = np.array([mi.width / 2, mi.height / 2])

    def cost(rot, sc, cx, cy):
        r = math.radians(rot)
        al, be = sc * math.cos(r), sc * math.sin(r)
        inv = np.array([[al, -be], [be, al]]) / (sc * sc)   # nghịch của [[al, be], [-be, al]] (cv2: dương = ngược kim)
        off = lc + inv @ (np.array([wx0, wy0], float) - np.array([cx, cy]))
        m = np.asarray(lim.transform((ww, hh), Image.AFFINE, (inv[0, 0], inv[0, 1], off[0], inv[1, 0], inv[1, 1], off[1]),
                                     resample=Image.NEAREST)) > 127
        miss = need - int((m & E).sum())
        out = int((m & ~Hd).sum())
        c = miss * 40 + out * 6 + int(m.sum()) * 0.05 + (int((m & Tr).sum()) * 1.5 if Tr is not None else 0)
        return c, miss, out

    best = None
    for rot in np.arange(goc[0], goc[1] + 1e-6, goc[2]):
        for sc in np.arange(ti[0], ti[1] + 1e-6, ti[2]) * ew / mi.width:
            for dx in range(-doi, doi + 1, 3):
                for dy in range(-doi, doi + 1, 3):
                    c, miss, out = cost(rot, sc, ex + dx, ey + dy)
                    if best is None or c < best[0]:
                        best = (c, ex + dx, ey + dy, float(rot), float(sc), miss, out)
    _, bx, by, br, bs, _, _ = best
    for rot in np.arange(br - 3, br + 3.01, 1.0):
        for sc in np.arange(bs * 0.94, bs * 1.061, bs * 0.02):
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    c, miss, out = cost(rot, sc, bx + dx, by + dy)
                    if c < best[0]:
                        best = (c, bx + dx, by + dy, float(rot), float(sc), miss, out)
    _, cx, cy, rot, sc, miss, out = best
    print(f"  mí {ten}: tâm ({cx:.0f}, {cy:.0f}) góc {rot:.0f}° tỉ lệ {sc:.2f}; còn hở {miss} px / {need}, lòi ngoài đầu {out} px")
    return cx, cy, rot, sc, miss


def dat_mi(dat_dau, dau, kq):
    """Dat cho ảnh mí từ kết quả fit_lid, theo cách đặt đầu (dat_dau) trong thế giới rig."""
    cx, cy, rot, sc = kq[:4]
    p = dat_dau.mot((cx, cy), dau.width, dau.height)
    return Dat(p[0], p[1], dat_dau.goc + (-rot if dat_dau.lat else rot), (dat_dau.sx * sc, dat_dau.sy * sc), lat=dat_dau.lat)
