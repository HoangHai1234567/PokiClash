# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của khủng long núi lửa đảo Hỏa (nui_lua): khối từng part của rig monster_3654 ở khung 0 idle_01, tô phẳng theo nhóm màu
của THIẾT KẾ MÌNH. Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng; không mang nét, hoa văn, màu của con gốc.

Mỗi ống núi lửa: thân màu đá, một dải dung nham ở miệng ống và một elip lõi (miệng núi lửa) ở đỉnh, đặt theo trục chính của part.
Mắt đặt ở chỗ con mắt của rig (P_yanjing_02, họ không bật) trên hàm trên.

Ba hướng màu ĐỀ XUẤT của Claude, chờ người dùng chọn:
  den   đá bazan đen than, dung nham cam lõi vàng, hàm và móng ngà (kinh điển)
  do    đá xỉ đỏ gạch, lưng nâu sẫm, dung nham vàng lõi kem, móng than
  lam   đá phiến xám lam, dung nham đỏ cam lõi vàng, hàm và móng ngà (đá lạnh, lửa nóng)

    nui_lua_bo_cuc.py [hướng|all]   → inbox/nui_lua_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json: khung từng nhóm, từng ống; _luoi_<hướng>.png)
"""
import json
import math
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nui_lua as G  # noqa: E402  (đổi con của hoa_ho sang monster_3654 trước khi nạp hoa_ho_bo_cuc)
import hoa_ho_bo_cuc as B  # noqa: E402

W, H, S2, INK = B.W, B.H, B.S2, B.INK
ATT = "att_idle0.json"

HUONG = {
    "den": dict(da=(86, 80, 92), da_dam=(54, 50, 60), nham=(240, 120, 40), loi=(250, 204, 80), xuong=(222, 196, 150), mat=(250, 214, 70)),
    "do": dict(da=(164, 78, 58), da_dam=(98, 46, 42), nham=(248, 176, 50), loi=(252, 232, 150), xuong=(60, 50, 54), mat=(252, 232, 150)),
    "lam": dict(da=(98, 112, 136), da_dam=(60, 68, 90), nham=(236, 92, 44), loi=(250, 200, 70), xuong=(226, 208, 170), mat=(250, 200, 70)),
    # Lượt 2 (2026-11-14, người dùng: "A đẹp nhưng nhìn hơi giống con gốc, sáng tạo hơn chút"): giữ bảng màu A, đổi thiết kế.
    #   giap  khủng long giáp: mũ xương ngà, đai vảy xương ở sườn, ĐUÔI CHUỲ (mảnh thêm), đỉnh lưng là miệng núi lửa chính
    #   sung  khủng long sừng: HAI SỪNG HÚC ngà (mảnh thêm) chĩa ra trước từ gờ mày, đỉnh lưng là miệng núi lửa chính
    #   cot   cả con dựng bằng cột bazan lục giác
    "giap": dict(da=(86, 80, 92), da_dam=(54, 50, 60), nham=(240, 120, 40), loi=(250, 204, 80), xuong=(228, 206, 164), mat=(250, 214, 70),
                 vai={r"^P_houtuiR5$|^P_qiantuiR3$|^P_duzi_0[12]$": "xuong", r"^P_shagne": "xuong", r"^P_xiae": "da"}, ong_mau={"11": "xuong", "12": "xuong", "16": "xuong"},
                 mieng_chinh=True, duoi=True),
    "sung": dict(da=(86, 80, 92), da_dam=(54, 50, 60), nham=(240, 120, 40), loi=(250, 204, 80), xuong=(228, 206, 164), mat=(250, 214, 70),
                 mieng_chinh=True, sung=True),
    "cot": dict(da=(74, 78, 94), da_dam=(46, 48, 62), nham=(244, 112, 36), loi=(252, 208, 84), xuong=(226, 208, 170), mat=(252, 208, 84)),
}
# mảnh thêm vẽ trên sơ đồ (toạ độ khung 1536x1024)
DUOI = [(380, 640), (300, 612), (225, 585), (180, 560), (185, 610), (235, 640), (300, 672), (380, 700)]
CHUY = ((150, 572), (62, 50), -20)
SUNG_XA = [(1120, 600), (1190, 585), (1250, 545), (1285, 495), (1295, 450), (1262, 490), (1228, 525), (1180, 548), (1120, 555)]
SUNG_GAN = [(1165, 690), (1235, 680), (1300, 640), (1338, 580), (1350, 515), (1318, 560), (1285, 600), (1240, 625), (1185, 628)]
MIENG_CHINH = ((772, 160), (66, 20))

BO = ("shadow", "P_yanjing_02")


def vai(slot):
    if slot in BO or slot.startswith("P_yan_"):
        return None
    if re.match(r"P_jiao_\d+$", slot):
        return "ong"
    if slot == "P_duzi" or slot == "P_houlong":
        return "nham"                                  # bụng dung nham lộ giữa các tảng đá; họng
    if slot.startswith("P_beijia"):
        return "da_dam"
    if slot.startswith("P_jiaozhi") or slot in ("P_xiae_1", "P_xiae_2"):
        return "xuong"                                 # móng; hàm dưới
    return "da"


KHUNG_NHOM = {
    "dau": r"^P_shagne|^P_xiae|^P_houlong|^P_jiao_(11|12|16)$", "ham_tren": r"^P_shagne", "ham_duoi": r"^P_xiae",
    "lung": r"^P_beijia", "bung": r"^P_duzi$", "da_suon": r"^P_duzi_0", "ong_lung_sau": r"^P_jiao_(09|10)$",
    "ong_lung_xa": r"^P_jiao_(13|14|15)$", "ong_giua": r"^P_jiao_(01|02)$", "ong_mong": r"^P_jiao_(03|04|06|07|08)$",
    "chan_truoc_gan": r"^P_qiantuiR|^P_jiaozhi_01", "chan_sau_gan": r"^P_houtuiR", "chan_truoc_xa": r"^P_qiantuiL|^P_jiaozhi_02",
    "chan_sau_xa": r"^P_houtuiL", "mong_truoc_gan": r"^P_jiaozhi_01", "mong_truoc_xa": r"^P_jiaozhi_02",
}
# part chân có vẽ sẵn một ống núi lửa (đầu ống ở phía xa tâm thân): cũng tô dải dung nham + lõi
ONG_TREN_CHAN = ("P_qiantuiR5", "P_qiantuiR1", "P_qiantuiL_01")


def truc_ong(V, tam=(-60.0, 380.0), len_tren=False):
    c = V.mean(0)
    _, _, vt = np.linalg.svd(V - c)
    ax = vt[0] if np.dot(vt[0], c - np.array(tam)) >= 0 else -vt[0]
    if len_tren and ax[1] < 0:
        ax = -ax
    pr = (V - c) @ ax
    return c, ax, pr


def atts_dung():
    G.H._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    return [a for a in atts if vai(a["slot"])]


def khung_T():
    atts = atts_dung()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    SC = round(min((W - 110) / (x1 - x0), (H - 120) / (y1 - y0)), 3)
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 55 + y0 * SC
    return SC, ox, oy, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def cho_mat(T):
    """chỗ con mắt: P_yanjing_02 ở dáng gốc, đưa sang khung 0 idle bằng phép biến đổi của hàm trên (cùng xương)."""
    scan = G.scan()
    Dg = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, ATT), encoding="utf-8"))
    g = {a["slot"]: a for a in Dg["atts"]}
    i0 = {a["slot"]: a for a in D0["atts"]}
    A = np.array(g["P_shagne_1"]["xy"], float).reshape(-1, 2)
    Bq = np.array(i0["P_shagne_1"]["xy"], float).reshape(-1, 2)
    X = np.hstack([A, np.ones((len(A), 1))])
    M, *_ = np.linalg.lstsq(X, Bq, rcond=None)
    e = np.array(g["P_yanjing_02"]["xy"], float).reshape(-1, 2).mean(0)
    return T(np.array([e[0], e[1], 1.0]) @ M)


def da_giac(can, pts, mau):
    q = (np.array(pts, float) * S2).astype(np.int32)
    cv2.fillPoly(can, [q], mau)
    cv2.polylines(can, [q], True, INK, 3 * S2)


def elip(can, tam, ban, goc, mau):
    cv2.ellipse(can, (tam[0] * S2, tam[1] * S2), (ban[0] * S2, ban[1] * S2), goc, 0, 360, INK, -1)
    cv2.ellipse(can, (tam[0] * S2, tam[1] * S2), (ban[0] * S2 - 3 * S2, ban[1] * S2 - 3 * S2), goc, 0, 360, mau, -1)


def ve(huong):
    C = HUONG[huong]
    SC, ox, oy, T = khung_T()
    atts = atts_dung()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop, ong = {}, {}
    if C.get("duoi"):                                  # đuôi chuỳ: sau mọi mảnh
        da_giac(can, DUOI, C["da"])
        elip(can, CHUY[0], CHUY[1], CHUY[2], C["xuong"])
    if C.get("sung"):                                  # sừng phía xa: sau các mảnh đầu
        da_giac(can, SUNG_XA, C["xuong"])
    for a in atts:
        s = a["slot"]
        v = vai(s)
        for rx_, v_ in C.get("vai", {}).items():
            if re.search(rx_, s):
                v = v_
        m = B.bong(a, T, 3.0)
        if not m.any():
            continue
        la_ong = v == "ong" or s in ONG_TREN_CHAN
        nn = s[-2:] if v == "ong" else s
        can[m] = C[C.get("ong_mau", {}).get(nn, "da") if v == "ong" else v]
        if la_ong:
            Vw = np.array(a["xy"], float).reshape(-1, 2)
            c, ax, pr = truc_ong(Vw, len_tren=nn in ("13", "14", "15", "09", "10", "02", "03", "04", "06"))
            if s == "P_qiantuiL_01" or s == "P_qiantuiR1":
                ax, pr = (-ax, -pr) if ax[1] < 0 else (ax, pr)     # ống trên bắp chân: miệng ở phía trên
            dai = pr.max() - pr.min()
            ys, xs = np.nonzero(m)
            # toạ độ rig của từng pixel mặt nạ → chiếu lên trục: dải dung nham ở 20% phía miệng ống
            rx = (xs / S2 - ox) / SC
            ry = (oy - ys / S2) / SC
            p = (rx - c[0]) * ax[0] + (ry - c[1]) * ax[1]
            band = p > pr.max() - 0.20 * dai
            can[ys[band], xs[band]] = C["nham"]
            dinh = c + ax * (pr.max() - 0.07 * dai)
            ngang = float(np.abs((Vw - c) @ np.array([-ax[1], ax[0]]))[pr > pr.max() - 0.25 * dai].max())
            d2 = T(dinh) * S2
            g = math.degrees(math.atan2(-ax[1], ax[0]))
            cv2.ellipse(can, (int(d2[0]), int(d2[1])), (max(3, int(0.20 * dai * SC * S2 * 0.35)), max(4, int(ngang * SC * S2 * 0.62))),
                        g, 0, 360, INK, -1)
            cv2.ellipse(can, (int(d2[0]), int(d2[1])), (max(2, int(0.20 * dai * SC * S2 * 0.35) - 5), max(3, int(ngang * SC * S2 * 0.62) - 5)),
                        g, 0, 360, C["loi"], -1)
            day = T(c + ax * pr.min())
            ong[nn] = dict(mieng=[round(float(d2[0] / S2)), round(float(d2[1] / S2))], day=[round(float(day[0])), round(float(day[1]))],
                           rong=round(2 * ngang * SC), dai=round(dai * SC))
        can[B.vien(m, 3 * S2)] = INK
        ys, xs = np.nonzero(m)
        for ten, rx_ in KHUNG_NHOM.items():
            if re.search(rx_, s):
                h = hop.get(ten)
                b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        hop.setdefault("_tat_ca", [1e9, 1e9, 0, 0])
        t = hop["_tat_ca"]
        hop["_tat_ca"] = [min(t[0], xs.min() / S2), min(t[1], ys.min() / S2), max(t[2], xs.max() / S2), max(t[3], ys.max() / S2)]
    if C.get("mieng_chinh"):
        elip(can, MIENG_CHINH[0], MIENG_CHINH[1], 0, C["loi"])
    if C.get("sung"):                                  # sừng phía gần: trước sọ
        da_giac(can, SUNG_GAN, C["xuong"])
    e = cho_mat(T) * S2
    ex, ey = int(e[0]), int(e[1])
    cv2.ellipse(can, (ex, ey), (15 * S2, 9 * S2), 30, 0, 360, INK, -1)
    cv2.ellipse(can, (ex, ey), (11 * S2, 5 * S2), 30, 0, 360, C["mat"], -1)
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    hop = {k: [round(x) for x in v] for k, v in hop.items()}
    hop["mat"] = [round(ex / S2), round(ey / S2)]
    hop["ong"] = ong
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
    for k, o in ong.items():
        d.text((o["mieng"][0] + 4, o["mieng"][1] - 6), k[-4:], fill=(0, 90, 255), font=F)
    g.save(os.path.join(G.MAU, f"_luoi_{huong}.png"))


if __name__ == "__main__":
    hs = sys.argv[1] if len(sys.argv) > 1 else "all"
    for h in (HUONG if hs == "all" else [hs]):
        ve(h)
