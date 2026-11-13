# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của thú một sừng đảo Mộc (giac_moc): khối từng part của rig monster_3804, tô phẳng theo nhóm màu của THIẾT KẾ MÌNH, ở hai
dáng: `nghi` (khung 0 idle_01) và `mo` (open_02 giây 0,5: ngẩng cao, vỏ ngực trượt mở, lộ lòng ngực có quả tim). Chỉ để GPT lấy chỗ đặt,
cỡ, thứ tự chồng; không mang nét, hoa văn, màu của con gốc. Đầu (mảnh cứng một xương) vẽ to hơn con gốc 1,45 lần và có mắt.

Hai hướng ĐỀ XUẤT của Claude (2026-11-13), chờ người dùng chọn:
  co_thu    thú cổ thụ: thân vỏ cây nâu, rêu, lưng dương xỉ + dây leo + tinh thể hổ phách, vỏ ngực là các tấm vỏ cây, tim nhựa hổ phách
  bach_thu  bạch thú hoa: thú lông trắng kem, lưng lá to + dây leo + nụ sen hồng, vỏ ngực là một nụ hoa khổng lồ, tim vàng

    giac_moc_bo_cuc.py [hướng|all] [nghi|mo|all]   → inbox/giac_moc_1/mau/bo_cuc_<hướng>_<dáng>.png (+ .json khung từng nhóm)
"""
import json
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import giac_moc as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1024, 1536
S2 = 2
INK = (43, 33, 24)
DANG = {"nghi": "att_idle0.json", "mo": "att_open.json"}
DAU_TO = 1.45

HUONG = {
    "co_thu": dict(
        than=(122, 84, 56),          # vỏ cây nâu óc chó #7A5438
        bung=(214, 188, 140),        # gỗ nhạt mặt dưới #D6BC8C
        ban_chan=(84, 58, 40),       # rễ sẫm #543A28
        reu=(110, 150, 62),          # rêu #6E963E
        la=(62, 120, 70),            # dương xỉ #3E7846
        la_nhat=(130, 176, 80),      # lá non #82B050
        day=(90, 140, 60),           # dây leo #5A8C3C
        tinh_the=(232, 168, 56),     # tinh thể hổ phách #E8A838
        gai=(218, 196, 150),         # gai gỗ nhạt #DAC496
        cua=(84, 58, 40),
        vo=(92, 64, 44),             # tấm vỏ ngực (vỏ cây sẫm) #5C402C
        vo_nhat=(218, 196, 150),     # tấm sườn gỗ nhạt
        vanh=(62, 120, 70),          # vành vỏ ngực: dây leo
        khe=(232, 168, 56),          # khe sáng hổ phách
        long=(70, 44, 36),           # lòng ngực #462C24
        tim=(255, 214, 80),          # quả tim #FFD650
        dau=(150, 106, 70),          # đầu gỗ sáng hơn #966A46
        sung=(84, 58, 40),
        sung_ngon=(232, 168, 56),
        mat=(255, 214, 80)),
    "bach_thu": dict(
        than=(240, 232, 214),        # lông trắng kem #F0E8D6
        bung=(226, 214, 190),
        ban_chan=(120, 92, 66),      # bàn chân nâu #785C42
        reu=(104, 168, 72),          # bờm lá ở chân #68A848
        la=(46, 124, 84),            # lá to lục sẫm #2E7C54
        la_nhat=(140, 190, 96),
        day=(86, 150, 70),
        tinh_the=(232, 120, 150),    # nụ sen hồng #E87896
        gai=(150, 196, 110),         # đài hoa dựng lục nhạt #96C46E
        cua=(120, 92, 66),
        vo=(214, 88, 130),           # cánh nụ hoa hồng sẫm #D65882
        vo_nhat=(240, 160, 180),     # cánh hoa nhạt
        vanh=(46, 124, 84),          # đài hoa
        khe=(244, 196, 70),
        long=(120, 50, 80),          # lòng nụ hoa #783250
        tim=(255, 226, 110),
        dau=(240, 232, 214),
        sung=(150, 106, 70),         # sừng gỗ #966A46
        sung_ngon=(244, 196, 70),
        mat=(232, 150, 40)),
}


def vai(slot, region):
    """part của con gốc → vai trò trong thiết kế mình (None = bỏ khỏi sơ đồ)."""
    if region == "B_beimao_04":
        return "day"                                   # bốn sợi râu mảnh → tua dây leo
    if slot.startswith("P_beifa"):
        return "la_nhat"
    if slot.startswith("B_beimao"):
        return "la"
    if slot.startswith("S_shitou"):
        return "tinh_the"
    if slot.startswith("P_bei_"):
        return "gai"
    if re.match(r"^T[HQ]_tui[LR]_3", slot) or re.match(r"^T[HQ]_tui[LR]_2_", slot):
        return "ban_chan"
    if re.match(r"^T[HQ]_tui", slot):
        return "than"
    if slot.startswith("P_tuimao"):
        return "reu"
    if slot.startswith("P_tuijiao"):
        return "cua"
    if slot in ("P_shenti_02",):
        return "long"
    if slot in ("P_shenti_02_1", "P_shenti_02_2"):
        return None                                    # cụm lỗ tối: thay bằng quả tim
    if slot.startswith("P_shenti"):
        return "than"
    if slot == "B_bozi_1":
        return "than"
    if slot.startswith("P_bozi"):
        return "gai"                                   # ba tấm đốt cổ
    if slot in ("B_bozi_E_10", "B_bozi_E_11", "B_bozi_E_12"):
        return "bung"
    if slot.startswith("B_bozi_A"):
        return "reu"
    if slot.startswith("B_bozi_B"):
        return "vo_nhat"
    if slot.startswith("B_bozi_C"):
        return "vo"
    if slot.startswith("B_bozi_D"):
        return "vanh"
    if slot.startswith("B_bozi_E"):
        return "khe"
    if slot.startswith("B_bozi_F"):
        return "cua"
    if slot == "P_tou_jiao_1":
        return "sung"
    if slot == "P_tou_jiao_2":
        return None
    if slot in ("P_tou1", "P_tou2"):
        return "dau"
    if slot == "B_tou_B_01":
        return "la_nhat"
    if slot.startswith("P_toufa"):
        return "la"
    return None


# nhóm để ghi khung (toạ độ trên khung concept) vào prompt
KHUNG_NHOM = {
    "sung": r"^P_tou_jiao_1$", "dau": r"^P_tou[12]$", "la_dau": r"^P_toufa|^B_tou_B|^P_beifa", "co": r"^B_bozi_1$|^P_bozi",
    "la_lung": r"^B_beimao", "tinh_the": r"^S_shitou", "gai_lung": r"^P_bei_0[2-5]$", "mong": r"^P_shenti04$", "vai": r"^P_shenti_01$",
    "vo_nguc": r"^B_bozi_[CDF]", "suon": r"^B_bozi_B", "long_nguc": r"^P_shenti_02$", "reu_vai": r"^B_bozi_A|^P_tuimao_R0[12]$|^P_tuijiao_R01$",
    "chan_truoc_gan": r"^TQ_tuiR|^P_tuimao_R0[34]|^P_tuijiao_R02", "chan_sau_gan": r"^TH_tuiR", "chan_truoc_xa": r"^TQ_tuiL|^P_tuimao_L|^P_tuijiao_L",
    "chan_sau_xa": r"^TH_tuiL",
}


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def pham_vi(att):
    _, _, atts = G.nap(att)
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if vai(a["slot"], a["region"])])
    return P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()


def ti_le():
    s = 9
    for att in DANG.values():
        x0, y0, x1, y1 = pham_vi(att)
        s = min(s, (W - 70) / (x1 - x0), (H - 150) / (y1 - y0))
    return round(s, 3)


def khung_T(att, SC):
    x0, y0, x1, y1 = pham_vi(att)
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 70 + y0 * SC
    return lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


def bong(a, T, tron=4.0, quanh=None, phong=1.0):
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2))
    if quanh is not None:
        V = quanh + (V - quanh) * phong
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V * S2, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def ve(huong, dang):
    C = HUONG[huong]
    att = DANG[dang]
    SC = ti_le()
    G._C.pop("att", None)
    _, _, atts = G.nap(att)
    T = khung_T(att, SC)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    dau = next(a for a in atts if a["slot"] == "P_tou1")
    tam_dau = T(np.array(dau["xy"], float).reshape(-1, 2)).mean(0)
    hop, tim_cho, sung_m, dau_m = {}, None, None, None
    for a in atts:
        v = vai(a["slot"], a["region"])
        if not v:
            continue
        la_dau = a["slot"] in ("P_tou1", "P_tou2")
        m = bong(a, T, 2.2 if v in ("day", "khe") else 4.0, tam_dau if la_dau else None, DAU_TO if la_dau else 1.0)
        if not m.any():
            continue
        can[m] = C[v]
        can[vien(m, 2 * S2 if v in ("day", "khe") else 3 * S2)] = INK
        ys, xs = np.nonzero(m)
        for ten, rx in KHUNG_NHOM.items():
            if re.search(rx, a["slot"]):
                h = hop.get(ten)
                b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        if a["slot"] == "P_shenti_02":
            tim_cho = (m, xs, ys)
        if a["slot"] == "P_tou_jiao_1":
            sung_m = (m, a)
        if a["slot"] == "P_tou1":
            dau_m = m
        if a["slot"] == "P_shenti_02" and dang == "mo":
            # quả tim: hình tròn ở chỗ rộng nhất của lòng ngực (vẽ ngay trên lòng ngực, dưới các tấm vỏ)
            d = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
            cy, cx = np.unravel_index(d.argmax(), d.shape)
            r = int(d.max() * 0.80)
            cv2.circle(can, (int(cx), int(cy)), r, INK, -1)
            cv2.circle(can, (int(cx), int(cy)), r - 3 * S2, C["tim"], -1)
            hop["tim"] = [(cx - r) / S2, (cy - r) / S2, (cx + r) / S2, (cy + r) / S2]
        if a["slot"] == "P_tou_jiao_1":
            # một phần ba ngọn sừng tô màu ngọn (chiếu lên trục gốc → ngọn; ngọn là đầu xa tâm đầu nhất)
            pts = np.stack([xs, ys], 1).astype(float)
            c0 = tam_dau * S2
            far = pts[np.argmax(((pts - c0) ** 2).sum(1))]
            near = pts[np.argmin(((pts - c0) ** 2).sum(1))]
            ax = (far - near) / (np.linalg.norm(far - near) + 1e-6)
            t = (pts - near) @ ax / (np.linalg.norm(far - near) + 1e-6)
            sel = t > 0.62
            mm = np.zeros_like(m)
            mm[ys[sel], xs[sel]] = True
            can[mm & ~vien(m, 3 * S2)] = C["sung_ngon"]
            hop["sung_goc"] = [float(near[0] / S2), float(near[1] / S2)]
            hop["sung_ngon"] = [float(far[0] / S2), float(far[1] / S2)]
    # mắt: một chấm ở nửa trước của đầu (con nhìn sang phải)
    if dau_m is not None:
        ys, xs = np.nonzero(dau_m)
        ex, ey = int(xs.min() + (xs.max() - xs.min()) * 0.50), int(ys.min() + (ys.max() - ys.min()) * 0.40)
        cv2.ellipse(can, (ex, ey), (11 * S2, 7 * S2), -15, 0, 360, INK, -1)
        cv2.ellipse(can, (ex, ey), (8 * S2, 4 * S2), -15, 0, 360, C["mat"], -1)
        hop["mat"] = [ex / S2, ey / S2]
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}_{dang}.png")
    im.save(p)
    hop = {k: [round(x) for x in v] for k, v in hop.items()}
    hop["_sc"] = SC
    json.dump(hop, open(os.path.join(G.MAU, f"bo_cuc_{dang}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(p, "tỉ lệ", SC)
    # bản kẻ lưới để đọc toạ độ (nội bộ)
    g = im.copy()
    d = ImageDraw.Draw(g)
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(0, 0, 0) if x % 100 == 0 else (170, 170, 170), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=F)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(0, 0, 0) if y % 100 == 0 else (170, 170, 170), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(200, 0, 0), font=F)
    g.save(os.path.join(G.MAU, f"_luoi_{huong}_{dang}.png"))


if __name__ == "__main__":
    hs = sys.argv[1] if len(sys.argv) > 1 else "all"
    ds = sys.argv[2] if len(sys.argv) > 2 else "all"
    for h in (HUONG if hs == "all" else [hs]):
        for dg in (DANG if ds == "all" else [ds]):
            ve(h, dg)
