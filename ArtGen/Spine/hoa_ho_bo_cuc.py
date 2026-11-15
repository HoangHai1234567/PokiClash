# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của hổ lửa đảo Hỏa (hoa_ho): khối từng part của rig monster_3645 ở khung 0 idle_01, tô phẳng theo nhóm màu của THIẾT KẾ
MÌNH. Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng; không mang nét, hoa văn, màu của con gốc.

Người dùng (2026-11-14): giữ kiểu style của con gốc; mây quanh thân đổi sang mây đỏ lửa; BỎ sừng, BỎ chuông ở dưới. Vì vậy sơ đồ bỏ:
sừng `P_jiao`, khuyên sắt `P_tiehuan`, chuông nhỏ `P_lingdang`; cái chuông đồng lớn ôm ngực nằm sẵn trong ảnh thân `P_shenti_01` nên sơ
đồ tô thân một màu lông (không còn chuông).

Ba hướng màu ĐỀ XUẤT của Claude, chờ người dùng chọn:
  bach  bạch hổ mây lửa: lông trắng kem, vằn than, mây lửa đỏ son + cam + xoáy vàng (gần con gốc nhất)
  cam   hổ cam vằn đen, mây lửa đỏ thẫm viền vàng
  than  hổ than: lông xám than, vằn cam than hồng, mây lửa cam vàng

    hoa_ho_bo_cuc.py [hướng|all]   → inbox/hoa_ho_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json khung từng nhóm, _luoi_<hướng>.png)
"""
import json
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hoa_ho as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"

HUONG = {
    "bach": dict(
        long=(242, 236, 222),        # lông trắng kem #F2ECDE
        ban_chan=(226, 214, 196),    # bàn chân kem sẫm hơn #E2D6C4
        may=(214, 64, 42),           # mây lửa đỏ son #D6402A
        may_nhat=(244, 150, 48),     # chỏm lửa cam #F49630
        vong=(226, 170, 62),         # vòng chân vàng đồng #E2AA3E
        nanh=(250, 246, 232),
        tai=(238, 170, 150),
        rau=(90, 60, 50),
        mat=(248, 196, 60)),
    "cam": dict(
        long=(238, 148, 60),         # lông cam hổ #EE943C
        ban_chan=(246, 226, 196),    # bàn chân kem #F6E2C4
        may=(170, 40, 36),           # mây lửa đỏ thẫm #AA2824
        may_nhat=(248, 196, 70),     # chỏm lửa vàng #F8C446
        vong=(70, 64, 70),           # vòng chân sắt đen #464046
        nanh=(250, 246, 232),
        tai=(246, 226, 196),
        rau=(60, 44, 40),
        mat=(250, 220, 90)),
    "than": dict(
        long=(84, 80, 88),           # lông xám than #545058
        ban_chan=(60, 56, 64),       # bàn chân than sẫm #3C3840
        may=(240, 120, 40),          # mây lửa cam #F07828
        may_nhat=(250, 204, 80),     # chỏm lửa vàng #FACC50
        vong=(196, 60, 44),          # vòng chân đỏ son #C43C2C
        nanh=(246, 238, 220),
        tai=(120, 100, 104),
        rau=(40, 34, 36),
        mat=(250, 190, 60)),
}

BO = ("P_jiao", "P_tiehuan", "P_lingdang", "shadow", "wangge", "P_biyan", "P_yanjing")


def vai(slot):
    """part của con gốc → vai trò trong thiết kế mình (None = bỏ khỏi sơ đồ)."""
    if slot in BO:
        return None
    if slot in ("P_maofa_03", "P_maofa_04"):
        return "may_nhat"                              # hai chỏm lông xoăn trên trán → chỏm lửa nhỏ
    if slot.startswith("P_maofa") or slot.startswith("P_meimao"):
        return "may"
    if slot.startswith("jiaphuan"):
        return "vong"
    if slot.startswith("liaoya") or slot.startswith("P_ya"):
        return "nanh"
    if "erduo" in slot:
        return "tai"
    if "huxu" in slot:
        return "rau"
    if re.search(r"jiao(zhang|zhi)?(_\d+)?$", slot) and slot != "P_jiao":
        return "ban_chan"
    return "long"


KHUNG_NHOM = {
    "dau": r"^P_tou$|^P_zui", "tai_gan": r"^P_R_erduo", "tai_xa": r"^P_L_erduo", "nanh": r"^liaoya",
    "chom_tran": r"^P_maofa_0[34]$", "may_bom": r"^P_maofa_(05|06|07|08|09|10|11|12|13|14|15|16)$",
    "may_nguc": r"^P_maofa_(20|21)$", "may_hong": r"^P_maofa_(01|17|22)$", "may_duoi": r"^P_maofa_(23|23_01|24)$",
    "may_chan": r"^P_maofa_(02|19)$", "duoi": r"^P_weiba", "than": r"^P_shenti|^P_tun",
    "chan_truoc_gan": r"^P_R_(datui|xiaotui|jiao)", "chan_sau_gan": r"^P_R_hou", "chan_truoc_xa": r"^P_L_(datui|xiaotui|jiao)",
    "chan_sau_xa": r"^P_L_hou", "vong": r"^jiaphuan",
}


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def atts_dung():
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    return [a for a in atts if vai(a["slot"])]


def khung_T():
    atts = atts_dung()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    SC = round(min((W - 90) / (x1 - x0), (H - 110) / (y1 - y0)), 3)
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 50 + y0 * SC
    return SC, ox, oy, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def bong(a, T, tron=4.0):
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2))
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V * S2, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def ve(huong):
    C = HUONG[huong]
    SC, ox, oy, T = khung_T()
    atts = atts_dung()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop, dau_m = {}, None
    for a in atts:
        v = vai(a["slot"])
        nho = v in ("rau", "nanh")
        m = bong(a, T, 2.0 if nho else 4.0)
        if not m.any():
            continue
        can[m] = C[v]
        can[vien(m, 2 * S2 if nho else 3 * S2)] = INK
        ys, xs = np.nonzero(m)
        for ten, rx in KHUNG_NHOM.items():
            if re.search(rx, a["slot"]):
                h = hop.get(ten)
                b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        if a["slot"] == "P_tou":
            dau_m = m
    # mắt: lấy chỗ con mắt thật của rig (P_yanjing), vẽ một hình hạnh nhân xếch
    G._C.pop("att", None)
    _, _, het = G.nap(ATT)
    mat = next((a for a in het if a["slot"] == "P_yanjing"), None)
    if mat is not None:
        c = T(np.array(mat["xy"], float).reshape(-1, 2)).mean(0) * S2
        ex, ey = int(c[0]), int(c[1])
        cv2.ellipse(can, (ex, ey), (13 * S2, 7 * S2), 18, 0, 360, INK, -1)
        cv2.ellipse(can, (ex, ey), (10 * S2, 4 * S2), 18, 0, 360, C["mat"], -1)
        hop["mat"] = [ex / S2, ey / S2]
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    hop = {k: [round(x) for x in v] for k, v in hop.items()}
    hop["_sc"], hop["_ox"], hop["_oy"] = SC, round(ox, 1), round(oy, 1)
    json.dump(hop, open(os.path.join(G.MAU, "bo_cuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(p, "tỉ lệ", SC, "gốc rig", round(ox, 1), round(oy, 1))
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
    g.save(os.path.join(G.MAU, f"_luoi_{huong}.png"))


if __name__ == "__main__":
    hs = sys.argv[1] if len(sys.argv) > 1 else "all"
    for h in (HUONG if hs == "all" else [hs]):
        ve(h)
