# -*- coding: utf-8 -*-
"""Hàm dùng chung cho rig dòng tm01 (Tí Tách → Sóng Thần), viết riêng cho dòng, không sửa thư viện quai.

- Concept → rig: Doi(S, x0, y0) đổi toạ độ concept (px, y xuống) sang toạ độ rig (px atlas, y lên, gốc giữa hai chân).
- Mảnh vẽ duỗi thẳng (tay, chân, đuôi, dải băng đô, mào): dat_thang đặt trục mảnh từ khớp gốc theo một hướng, đúng một độ dài.
- noi_suy: trọng số của một điểm bất kỳ lấy theo lưới thân đã có (nội suy trọng tâm trong tam giác chứa nó): mắt, miệng, mí
  dán lên thân mềm nén giãn cùng thân, không trượt.
- the_dung: dáng đứng theo concept (gập khuỷu, vểnh đuôi, IK chân) gọi đầu mọi clip, nên khung 0 idle = concept.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from quai import anh, luoi, trongso  # noqa: E402
from quai.khung import Dat  # noqa: E402


class Doi:
    """concept (cx, cy px, y xuống) → rig (x, y, y lên): x = (cx - x0)·S, y = (y0 - cy)·S."""

    def __init__(self, S, x0, y0):
        self.S, self.x0, self.y0 = float(S), float(x0), float(y0)

    def __call__(self, cx, cy=None):
        if cy is None:
            cx, cy = cx
        return np.array([(cx - self.x0) * self.S, (self.y0 - cy) * self.S])

    def nhieu(self, pts):
        return np.array([self(p) for p in pts])

    def nguoc(self, x, y):
        return np.array([x / self.S + self.x0, self.y0 - y / self.S])


def goc(a, b):
    """góc thế giới (độ, ngược kim, y lên) của vector a → b."""
    d = np.asarray(b, float) - np.asarray(a, float)
    return math.degrees(math.atan2(d[1], d[0]))


def dat_thang(im, L, goc_tg, A, dai=None, ti=None, goc_anh=None):
    """đặt mảnh duỗi thẳng: trục của dải L (L.truc: điểm từ gốc tới ngọn, toạ độ ảnh) có gốc tới điểm thế giới A, chĩa theo góc
    thế giới goc_tg; tỉ lệ = dai / dài trục (hoặc ti). goc_anh: góc của trục trên ảnh (y xuống; mặc định đo từ L.truc).
    Trả Dat."""
    D = L.truc[0]
    p0, p1 = D[0], D[-1]
    Lt = float(L.truc[1][-1])
    k = ti if ti is not None else dai / Lt
    ga = goc_anh if goc_anh is not None else math.degrees(math.atan2(-(p1[1] - p0[1]), p1[0] - p0[0]))  # góc trên ảnh, y lên
    return Dat(A[0], A[1], goc=goc_tg - ga, ti=k, neo=(float(p0[0]), float(p0[1])), neo_px=True)


def khop_theo_ti(L, ti_le):
    """các khớp trên ảnh theo tỉ lệ dọc trục (vd [0, 0.48, 1.0]): trả (điểm ảnh, độ dài từng đốt theo đơn vị ảnh)."""
    D, cum = L.truc
    s = np.asarray(ti_le, float) * cum[-1]
    P = np.stack([np.interp(s, cum, D[:, 0]), np.interp(s, cum, D[:, 1])], 1)
    return P, np.diff(s)


def noi_suy(Lb, Wb, Vb, Q):
    """trọng số của điểm Q (thế giới) theo lưới thân (Lb.tris, đỉnh thế giới Vb, trọng số Wb): tam giác chứa điểm thì nội suy
    trọng tâm, ngoài lưới thì lấy tam giác gần nhất (toạ độ trọng tâm kẹp về trong)."""
    T = np.asarray(Lb.tris, int)
    A, B, C = Vb[T[:, 0]], Vb[T[:, 1]], Vb[T[:, 2]]
    v0, v1 = B - A, C - A
    d00, d01, d11 = (v0 * v0).sum(1), (v0 * v1).sum(1), (v1 * v1).sum(1)
    den = np.where(np.abs(d00 * d11 - d01 * d01) < 1e-12, 1e-12, d00 * d11 - d01 * d01)
    out = []
    for q in np.asarray(Q, float):
        v2 = q - A
        d20, d21 = (v2 * v0).sum(1), (v2 * v1).sum(1)
        b1 = (d11 * d20 - d01 * d21) / den
        b2 = (d00 * d21 - d01 * d20) / den
        b0 = 1 - b1 - b2
        bad = np.maximum(0, -np.minimum(np.minimum(b0, b1), b2))
        i = int(np.argmin(bad))
        bc = np.clip(np.array([b0[i], b1[i], b2[i]]), 0, None)
        bc /= max(1e-9, bc.sum())
        d = {}
        for k in range(3):
            for b, w in Wb[T[i, k]].items():
                d[b] = d.get(b, 0.0) + w * bc[k]
        out.append(d)
    return trongso.chuan(out)


def dan_len_than(sk, slot, ten_anh, Lb, Wb, Vb, dat, buoc=None):
    """dán một hình phẳng (mắt, miệng, mí) lên lưới thân: lưới nhỏ của hình, trọng số nội suy theo thân, nên hình nén giãn cùng
    thân. buoc: bước lưới của hình (mặc định theo cỡ)."""
    im = sk.images[ten_anh]
    b = min(buoc, max(2.5, min(im.width, im.height) / 4.0)) if buoc else max(6.0, min(im.width, im.height) / 3.0)
    L = bo_tg_det(luoi.luoi_vung(im, b, b * 1.33, ten=f"{slot}/{ten_anh}"), im)
    V = dat.ra(L.pts, im.width, im.height)
    W = noi_suy(Lb, Wb, Vb, V)
    sk.luoi_gan(slot, ten_anh, L, W, the_gioi=V, ten=ten_anh)
    return L


def ghep_concept(ve, P, concept, doi, ra, box=None, an_concept=0.45):
    """ảnh so ghép: concept (mờ) chồng hình rig ở tư thế P, cùng khung nhìn, để chỉnh chỗ đặt mảnh."""
    B = box or ve.bao(P)
    pad = 30
    B = (B[0] - pad, B[1] - pad, B[2] + pad, B[3] + pad)
    k = 1.0 / doi.S
    rig = ve.ve(P, B, k, ss=1)
    c = Image.open(concept).convert("RGBA")
    cx0, cy0 = doi.nguoc(B[0], B[3])
    cx1, cy1 = doi.nguoc(B[2], B[1])
    cc = c.crop((int(cx0), int(cy0), int(cx0) + rig.width, int(cy0) + rig.height))
    base = Image.new("RGBA", rig.size, (255, 255, 255, 255))
    a = np.asarray(cc).astype(np.float32)
    a[..., 3] *= an_concept
    base.alpha_composite(Image.fromarray(a.astype(np.uint8), "RGBA"))
    r = np.asarray(rig).astype(np.float32)
    r[..., 3] *= 0.6
    base.alpha_composite(Image.fromarray(r.astype(np.uint8), "RGBA"))
    both = Image.new("RGB", (rig.width * 3, rig.height), (255, 255, 255))
    both.paste(cc.convert("RGB"), (0, 0))
    both.paste(base.convert("RGB"), (rig.width, 0))
    bg = Image.new("RGBA", rig.size, (150, 150, 150, 255))
    bg.alpha_composite(rig)
    both.paste(bg.convert("RGB"), (2 * rig.width, 0))
    both.save(ra)
    return ra


def ke_luoi(src, ra, buoc=20, phong=2.0):
    """ảnh mảnh phóng to có kẻ lưới toạ độ (đọc khớp, hạt giống)."""
    im = Image.open(src).convert("RGBA") if isinstance(src, str) else src.convert("RGBA")
    bg = Image.new("RGBA", im.size, (200, 200, 200, 255))
    bg.alpha_composite(im)
    big = bg.resize((int(im.width * phong), int(im.height * phong)), Image.NEAREST).convert("RGB")
    d = ImageDraw.Draw(big)
    f = anh.font(11)
    for x in range(0, im.width + 1, buoc):
        d.line([(x * phong, 0), (x * phong, big.height)], fill=(255, 0, 0) if x % (buoc * 5) == 0 else (255, 170, 170))
        if x % (buoc * 5) == 0:
            d.text((x * phong + 2, 2), str(x), fill=(180, 0, 0), font=f)
    for y in range(0, im.height + 1, buoc):
        d.line([(0, y * phong), (big.width, y * phong)], fill=(0, 0, 255) if y % (buoc * 5) == 0 else (170, 170, 255))
        if y % (buoc * 5) == 0:
            d.text((2, y * phong + 2), str(y), fill=(0, 0, 180), font=f)
    big.save(ra)
    return ra


def mat_na_concept(concept):
    """mặt nạ con vật trên concept: mọi điểm không phải nền trắng nối mép (giấy trắng khép kín bên trong vẫn tính là hình)."""
    rgb = np.asarray(Image.open(concept).convert("RGB"))
    bg = anh.nen_tu_mep(rgb.min(axis=2) > 236)
    return ~bg


def iou_concept(ve, P, concept, doi, ra=None):
    """IoU giữa mặt nạ hình rig ở tư thế P (vẽ theo tỉ lệ concept) và mặt nạ concept; ghi ảnh màu (xanh: chỉ concept, đỏ: chỉ
    rig, xám: chung) nếu có ra. Trả (iou, chỉ_concept, chỉ_rig) theo số điểm."""
    cm = mat_na_concept(concept)
    H, Wd = cm.shape
    x0, y1 = doi.nguoc(0, 0)  # không dùng
    box_rig = (doi(0, H)[0], doi(0, H)[1], doi(Wd, 0)[0], doi(Wd, 0)[1])   # cả khung concept trong toạ độ rig
    img = ve.ve(P, box_rig, 1.0 / doi.S, ss=1)
    a = np.asarray(img)[..., 3] > 100
    h = min(H, a.shape[0]); w = min(Wd, a.shape[1])
    rm = np.zeros_like(cm)
    rm[:h, :w] = a[:h, :w]
    inter = int((rm & cm).sum()); uni = int((rm | cm).sum())
    iou = inter / max(1, uni)
    if ra:
        o = np.full((H, Wd, 3), 255, np.uint8)
        o[cm & rm] = (150, 150, 150)
        o[cm & ~rm] = (40, 110, 230)
        o[rm & ~cm] = (230, 60, 50)
        Image.fromarray(o).save(ra)
    return iou, int((cm & ~rm).sum()), int((rm & ~cm).sum())


def bo_tg_det(L, im, goc_min=1.0):
    """bỏ tam giác suy biến (góc nhỏ nhất < goc_min độ, diện tích gần 0: ba đỉnh gần thẳng hàng ở mép khe hẹp) khỏi lưới, đo lại
    phần hở. Tam giác diện tích ~0 không phủ điểm ảnh nào nên bỏ không làm hở."""
    P = L.pts
    T = np.asarray(L.tris, int)
    a, b, c = P[T[:, 0]], P[T[:, 1]], P[T[:, 2]]

    def ang(u, v):
        cs = (u * v).sum(1) / np.maximum(1e-9, np.hypot(*u.T) * np.hypot(*v.T))
        return np.degrees(np.arccos(np.clip(cs, -1, 1)))
    g = np.minimum(np.minimum(ang(b - a, c - a), ang(a - b, c - b)), ang(a - c, b - c))
    keep = g >= goc_min
    if keep.all():
        return L
    L.tris = T[keep]
    hard = np.asarray(im.convert("RGBA"))[..., 3] > 40
    L.ho = luoi._phu(hard, L.pts, L.tris)
    print(f"  {L.ten if hasattr(L, 'ten') else ''}: bỏ {int((~keep).sum())} tam giác suy biến; góc nhỏ nhất còn {g[keep].min():.1f}°, hở {L.ho} px")
    return L
