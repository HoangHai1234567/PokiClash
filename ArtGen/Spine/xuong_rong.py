# -*- coding: utf-8 -*-
"""Xương rồng tròn (mã làm việc xuong_rong; con gốc của rig: monster_3229, game tham khảo). Tướng đầu tiên đảo Mộc, DẠNG 1.

Người dùng 2026-11-12: "concept quái vật xương rồng thân tròn không mặt"; dạng 2 to hơn, chiến hơn, cùng form.
Cách làm = "reskin theo khung part" (skill pokiclash-spine-rig mục 00, mẫu bach_tuoc.py / rong_vay.py): mỗi part của rig gốc một ô đúng
khung ảnh vùng, trong ô là hình bóng kín tô phẳng theo THIẾT KẾ CỦA MÌNH; Codex vẽ lại sạch; rig dùng nguyên xương, lưới của họ.
Con gốc đã nhìn sang PHẢI (tay sau chĩa sang phải, đấm sang phải) nên không lật.

    xuong_rong.py part_goc         ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3229/parts/ (chỉ để xem)
    xuong_rong.py bo_cuc           sơ đồ bố cục phẳng 1536 × 1024 (đính vào prompt concept) → inbox/xuong_rong_1/mau/bo_cuc.png
    xuong_rong.py nhom_part        ba tờ hướng dẫn theo khung part (A thân + môi + lòng miệng, B răng + hoa + tay chân, C gai + gai
                                   dài + ụ đất) → mau/part_<tờ>.png + .json
    xuong_rong.py cat_part <tờ>    cắt tờ N_<tờ> Codex vẽ → manh/part/<hình>.png, đo IoU (ghi _iou.json)
    xuong_rong.py moi              vành môi = da thân NƯỚNG vào khung vành môi + nét mực mép lỗ miệng của Codex → manh/part_moi/
    xuong_rong.py so_part          tờ so mảnh với hình bóng → mau/so_part.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "xuong_rong"
MON = "monster_3229"
K = int(os.environ.get("XR_DANG", "1"))     # dạng: 1 (mặc định) hoặc 2 (cùng rig, cùng khung part; XR_DANG=2)
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
MANH = os.environ.get("XR_MANH") or os.path.join(BASE, "manh")      # XR_MANH: thư mục mảnh thử (chạy thử rig)
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
SC = 2.45                                        # đơn vị rig con gốc → pixel khung concept
Z = 4                                            # ảnh vùng atlas (tỉ lệ 0,75) phóng 4 lần = 3 lần cỡ thế giới của họ
INK = (43, 33, 24)
# dáng của concept: dáng gốc của rig + A POSE (tay sau thõng xuống, người dùng dặn 2026-11-12) = clip xr_dang của xuong_rong_clip.py
#   chay.py att <scan>/lam_clip monster_3229 <scan>/att_dang.json "anim=xr_dang&t=0&extra=xr_extra.json"
ATT = "att_dang.json"
# bảng màu theo dạng: đo trung vị trên concept đã duyệt (tai_ve/L1_duyet.png của từng dạng, người dùng duyệt 2026-11-12)
PAL_K = {1: dict(than=(76, 180, 105), gan=(25, 84, 52), gai=(254, 236, 169), hoa=(239, 79, 145), mieng=(153, 26, 70),
                 dat=(150, 112, 74), dat_dam=(104, 74, 48)),
         2: dict(than=(37, 155, 81), gan=(3, 75, 38), gai=(254, 231, 155), hoa=(240, 37, 101), mieng=(148, 13, 54),
                 dat=(150, 112, 74), dat_dam=(104, 74, 48))}
PAL = PAL_K[K]
GAI_THAN = ["P_ci1", "P_ci3", "P_ci4", "P_ci11", "P_ci12"]
GAI_TAY = ["P_shouL31", "P_shouL32", "P_shouL33", "P_shouR31", "P_shouR32", "P_shouR33"]
CHI = ["P_shouL1", "P_shouR2", "P_shouR3", "P_shouR1", "P_shouL2", "P_tuiR1", "P_tuiL1", "P_tuiL2", "P_tuiR2"]
# tờ mảnh theo dạng: (tỉ lệ phóng ảnh vùng, [ô theo thứ tự xếp]). Ô không phải part của rig: gai_vua, gai_dai (ảnh gai lúc phóng dài,
# đổi hình thay vì kéo giãn ảnh gai ngắn), u_dat (ụ đất của appear).
# DẠNG 2 dùng lại nguyên bộ gai, gai dài, ụ đất của dạng 1 (gai kem trơn như nhau; dài hơn là do tỉ lệ xương): không có tờ gai.
TO_K = {1: {"A": (2.8, ["P_shenti", "P_zuichun", "P_kouqiang"]),
            "B": (4.0, ["P_shangya", "P_xiaya", "P_shouL1", "P_toufa", "P_shouR2", "P_shouR3", "P_shouR1", "P_shouL2", "P_tuiR1",
                        "P_tuiL1", "P_tuiL2", "P_tuiR2"]),
            "C": (6.0, GAI_THAN + GAI_TAY + ["gai_vua", "gai_dai", "u_dat"])},
        2: {"A": (2.8, ["P_shenti", "P_zuichun", "P_kouqiang"]),
            "B": (4.0, ["P_shangya", "P_xiaya", "P_toufa"]),
            "C": (4.0, CHI)}}
TO = TO_K[K]
THEM = {"gai_vua": (380, 150), "gai_dai": (640, 136), "u_dat": (410, 176)}        # cỡ ô (px trên tờ) của các ô thêm
# DẠNG 2: nanh dài hơn hình bóng răng của họ → ô răng NỚI thêm chừng này px (trên tờ) quanh khung ảnh vùng; răng là mảnh cứng một
# xương nên rig gắn cả ô nới thành một ô chữ nhật (không dùng lưới ôm hình bóng của họ)
# Vành hoa dạng 2 cũng nới khung: cánh dài, hai cánh ngoài cùng chạm mép khung ảnh vùng thì bị cắt cụt thành cạnh thẳng không viền
DEM_K = {1: {}, 2: {"P_shangya": 56, "P_xiaya": 56, "P_toufa": 52}}
DEM = DEM_K[K]
# ô vẽ tự do: không cắt sát hình bóng, không bù. Vành hoa dạng 2: Codex vẽ lại thành quạt cong cân đối, lệch hình bóng hướng dẫn
# (IoU 0,74); hoa dùng lưới riêng nên lấy nguyên hình Codex vẽ (cắt sát + bù sẽ trộn điểm ảnh của tờ hướng dẫn vào)
KHONG_SAT = ("gai_vua", "gai_dai", "u_dat") + tuple(DEM)


def manh_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "manh")


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


def rig_goc():
    return os.path.join(sxs(), "web", "assets", "Monster", MON)


def scan():
    return os.path.join(sxs(), "scan", MON)


def loai(ten):
    """nhóm thiết kế của một part (tên hình của con gốc)."""
    if ten == "P_shenti":
        return "than"
    if ten == "P_kouqiang":
        return "mieng"
    if ten == "P_zuichun":
        return "moi"
    if ten in ("P_shangya", "P_xiaya"):
        return "rang"
    if ten == "P_toufa":
        return "hoa"
    if ten in GAI_THAN or ten in GAI_TAY:
        return "gai"
    if ten in ("P_tuiL2", "P_tuiR2"):
        return "ban_chan"
    return "chi"                                 # khúc tay, nắm tay, đùi


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_C = {}


def nap(att=None):
    """(ảnh vùng đã gỡ xoay {tên: RGBA}, att {tên hình: att}, danh sách att theo thứ tự vẽ). att: tên file dáng (mặc định ATT)."""
    att = att or ATT
    if att not in _C:
        _, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), att), encoding="utf-8"))
        atts = [a for a in D["atts"] if a.get("region") in imgs]
        _C[att] = dict(imgs=imgs, by={a["att"]: a for a in atts}, atts=sorted(atts, key=lambda a: a["order"]), bones=D["bones"])
    c = _C[att]
    return c["imgs"], c["by"], c["atts"]


def co_o(ten, z):
    imgs, by, _ = nap()
    im = imgs[by[ten]["region"]]
    return int(round(im.width * z)), int(round(im.height * z))


def part_goc(ten, z=1):
    """ảnh một part của con gốc cắt đúng theo lưới của nó (ảnh vùng atlas là chữ nhật nên dính mảnh bên cạnh)."""
    imgs, by, _ = nap()
    a = by[ten]
    im = imgs[a["region"]].convert("RGBA")
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    m = Image.new("L", (im.width * 4, im.height * 4), 0)
    d = ImageDraw.Draw(m)
    for t in np.array(a["tris"]).reshape(-1, 3):
        d.polygon([tuple(uv[i] * 4) for i in t], fill=255, outline=255)
    A = np.asarray(im).copy()
    A[..., 3] = (A[..., 3].astype(np.float32) * np.asarray(m.resize(im.size, Image.LANCZOS)) / 255.0).astype(np.uint8)
    out = Image.fromarray(A, "RGBA")
    return out if z == 1 else out.resize(co_o(ten, z), Image.LANCZOS)


def bong(ten, z=Z):
    """hình bóng KÍN của part (làm trơn nhẹ, không mang nét vẽ của họ), cỡ ảnh vùng × z. Vành môi giữ lỗ miệng."""
    a = np.asarray(part_goc(ten, z))
    m = (a[..., 3] > 100).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(1.0 * z))
    m = cv2.GaussianBlur(m * 255, (0, 0), 0.8 * z) > 127
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 2:
        m = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return m, a


def truc_xuong(ten, z):
    """(gốc, trục đơn vị) của xương mà part CỨNG bám (đỉnh đầu tiên), tính trong khung ô của part (px, y xuống)."""
    _, by, _ = nap()
    a = by[ten]
    B = _C[ATT]["bones"]
    w, h = co_o(ten, z)
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    xy = np.array(a["xy"], float).reshape(-1, 2)
    M, *_ = np.linalg.lstsq(np.c_[xy, np.ones(len(xy))], uv, rcond=None)      # thế giới → ô
    b = B[a["w"][0][0][0]]
    o = np.array([b["x"], b["y"], 1.0]) @ M
    u = np.array([b["a"], b["c"], 0.0]) @ M
    return o, u / np.linalg.norm(u)


def hinh_gai(ten, z):
    """hình học GAI của mình trong khung ô của part gai (px ô): gốc xương o, trục u, pháp tuyến n; dọc trục: t0 (đáy gốc gai), tb (tâm
    nửa elip gốc), tip (mũi); hw nửa bề ngang, c_n lệch tâm bề ngang. Gốc và bề ngang lấy theo hình bóng gai tù của con gốc, mũi
    vươn tới sát mép khung."""
    m0, _ = bong(ten, z)
    h, w = m0.shape
    o, u = truc_xuong(ten, z)
    n = np.array([-u[1], u[0]])
    ys, xs = np.nonzero(m0)
    P = np.stack([xs, ys], 1) - o
    t, s_ = P @ u, P @ n
    t0, t1 = np.percentile(t, 1), np.percentile(t, 99)
    c_n = (np.percentile(s_, 3) + np.percentile(s_, 97)) / 2          # tâm bề ngang (trục xương có thể lệch tâm hình)
    hw = (np.percentile(s_, 97) - np.percentile(s_, 3)) / 2 * 0.95
    le = 3.0 * z / 4 + 4
    tip = t1 + (t1 - t0) * 0.22                                        # mũi vươn dài hơn gai tù của họ
    for _ in range(40):                                                # không vượt khung ô
        p = o + u * tip + n * c_n
        if le <= p[0] <= w - le and le <= p[1] <= h - le:
            break
        tip -= (t1 - t0) * 0.02
    return dict(o=o, u=u, n=n, t0=t0, tb=t0 + hw * 0.55, tip=tip, hw=hw, c_n=c_n, w=w, h=h)


def non_gai(ten, z):
    """hình bóng GAI của mình: nón mập gốc tròn, mũi nhọn (như concept đã duyệt), nằm dọc trục xương gai. Gai là mảnh cứng (một ô chữ
    nhật bám một xương) nên hình bóng tự do trong khung."""
    g = hinh_gai(ten, z)
    o, u, n, tb, tip, hw, c_n, w, h = (g[k] for k in ("o", "u", "n", "tb", "tip", "hw", "c_n", "w", "h"))
    pts = []
    for q in np.linspace(np.pi / 2, 3 * np.pi / 2, 24):                # nửa elip gốc gai
        pts.append(o + u * (tb + np.cos(q) * hw * 0.55) + n * (c_n + np.sin(q) * hw))
    for q in np.linspace(0, 1, 16):                                    # cạnh dưới → mũi (hơi phồng)
        pts.append(o + u * (tb + (tip - tb) * q) + n * (c_n - hw * (1 - q) ** 0.82))
    for q in np.linspace(1, 0, 16):
        pts.append(o + u * (tb + (tip - tb) * q) + n * (c_n + hw * (1 - q) ** 0.82))
    S = 4
    mm = np.zeros((h * S, w * S), np.uint8)
    cv2.fillPoly(mm, [np.round(np.array(pts) * S).astype(np.int32)], 1)
    return cv2.resize(mm, (w, h), interpolation=cv2.INTER_AREA) > 0


def gai_tg(ten, z=6.0):
    """gai trong THẾ GIỚI của dáng ATT: (điểm đáy gốc gai, điểm mũi, nửa bề ngang) theo đơn vị rig con gốc, và tên xương gai bám:
    để đặt ảnh "gai dài" trùng trục, trùng gốc với gai ngắn."""
    g = hinh_gai(ten, z)
    _, by, _ = nap()
    a = by[ten]
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([g["w"], g["h"]])
    xy = np.array(a["xy"], float).reshape(-1, 2)
    M, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], xy, rcond=None)      # ô → thế giới
    day = np.r_[g["o"] + g["u"] * g["t0"] + g["n"] * g["c_n"], 1.0] @ M
    mui = np.r_[g["o"] + g["u"] * g["tip"] + g["n"] * g["c_n"], 1.0] @ M
    return day, mui, float(g["hw"] / (0.75 * z)), _C[ATT]["bones"][a["w"][0][0][0]]["name"]


def canh_hoa(ten, z):
    """hình VÀNH HOA của mình trong khung ô part mào: bảy cánh nhọn xoè quạt (như concept) đứng dọc cung đáy của mào con gốc. Trả
    (RGB, mặt nạ). Hoa bám 4 xương của mào qua lưới riêng (hình bóng khác lưới của họ)."""
    m0, _ = bong(ten, z)
    if DEM.get(ten):                                                   # ô nới khung: vẽ trên khung rộng hơn, cánh ngoài cùng đủ hình
        m0 = np.pad(m0, DEM[ten])
    h, w = m0.shape
    s = z / 4.0
    xs = np.nonzero(m0.any(axis=0))[0]
    x0, x1 = xs[0], xs[-1]
    cols = np.arange(x0, x1 + 1)
    low = np.array([np.nonzero(m0[:, x])[0].max() for x in cols], float)
    up = np.array([np.nonzero(m0[:, x])[0].min() for x in cols], float)
    kf = max(5, int(40 * s)) | 1
    low = cv2.GaussianBlur(low.reshape(1, -1), (kf, 1), 0).ravel()
    S = 3
    pil = Image.new("RGB", (w * S, h * S), (255, 255, 255))
    d = ImageDraw.Draw(pil)
    N = 7
    rong = (x1 - x0) / (N - 0.6)
    thu_tu = [0, 6, 1, 5, 2, 4, 3]                                     # cánh giữa vẽ sau cùng (đè lên hai bên)
    day = [(x, low[int(x - x0)] + 2) for x in np.linspace(x0 + 6 * s, x1 - 6 * s, 30)]
    d.polygon([(x * S, (y - 34 * s) * S) for x, y in day] + [(x * S, y * S) for x, y in reversed(day)], fill=PAL["hoa"])
    for i in thu_tu:
        f = i / (N - 1)
        bx = x0 + rong * 0.5 + f * (x1 - x0 - rong)
        j = int(np.clip(bx - x0, 0, len(cols) - 1))
        by_ = low[j] - 4 * s
        h0 = h - 2 * DEM.get(ten, 0)
        cao = float(np.clip(low[j] - up[max(0, j - 8):j + 9].min(), (0.62 if K == 1 else 0.80) * h0, 0.93 * h0)) * (0.86 + 0.14 * np.sin(np.pi * f))
        cao = min(cao, by_ - 6 * s)
        goc = np.radians(-90 + (f - 0.5) * 62)                         # xoè quạt: cánh ngoài ngả ra hai bên
        u = np.array([np.cos(goc), np.sin(goc)])
        n = np.array([-u[1], u[0]])
        hw, mu = (rong * 0.60, 0.75) if K == 1 else (rong * 0.47, 0.55)       # dạng 2: cánh hẹp, nhọn như lưỡi dao
        pts = []
        for q in np.linspace(0, 1, 18):
            pts.append(np.array([bx, by_]) + u * cao * q + n * hw * np.sin(np.pi * q ** mu) * (1 - 0.22 * q))
        for q in np.linspace(1, 0, 18):
            pts.append(np.array([bx, by_]) + u * cao * q - n * hw * np.sin(np.pi * q ** mu) * (1 - 0.22 * q))
        pts = [(float(np.clip(p[0], 4, w - 4)) * S, float(np.clip(p[1], 4, h - 4)) * S) for p in pts]
        d.polygon(pts, fill=PAL["hoa"])
        d.line(pts + pts[:1], fill=INK, width=int(round(5 * s * S)), joint="curve")
        c0, c1 = np.array([bx, by_]) + u * cao * 0.30, np.array([bx, by_]) + u * cao * 0.62
        d.line([(c0[0] * S, c0[1] * S), (c1[0] * S, c1[1] * S)], fill=INK, width=int(round(4 * s * S)))
    # đáy vành hoa (khuất sau thân): dải hồng liền, viền mực dưới đáy
    d.line([(x * S, y * S) for x, y in day], fill=INK, width=int(round(5 * s * S)), joint="curve")
    im = np.asarray(pil.resize((w, h), Image.LANCZOS)).copy()
    return im, im.min(axis=2) < 236


def rang_noi(ten, z):
    """ô răng dạng sau: khung ảnh vùng nới DEM px mỗi phía, nền là chính dải răng dạng 1 đã vẽ (đúng chỗ trong khung), tô lại màu
    dạng này: Codex kéo dài, vót nhọn từng nanh vào khoảng trắng nới thêm, dải lợi giữ nguyên chỗ."""
    d = DEM[ten]
    w, h = co_o(ten, z)
    g = Image.open(os.path.join(manh_dir(1), "part", ten + ".png")).convert("RGBA").resize((w, h), Image.LANCZOS)
    im = np.full((h + 2 * d, w + 2 * d, 3), 255, np.uint8)
    a = np.asarray(g)
    co = a[..., 3] > 127
    sub = im[d:d + h, d:d + w]
    sub[co] = a[..., :3][co]
    m = np.zeros(im.shape[:2], bool)
    m[d:d + h, d:d + w] = co
    return im, m


def thiet_ke(ten, z=Z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Lấy của con gốc hình bóng thân, môi,
    lòng miệng, răng, tay chân (và chỗ mấy ngón chân); GAI và VÀNH HOA mang hình bóng của mình (non_gai, canh_hoa). Trả (RGB nền
    trắng, mặt nạ)."""
    k = loai(ten)
    if k == "hoa":
        return canh_hoa(ten, z)
    if ten in DEM:
        return rang_noi(ten, z)
    m, a = bong(ten, z)
    if k == "gai":
        m = non_gai(ten, z)
    h, w = m.shape
    im = np.full((h, w, 3), 255, np.uint8)
    s = z / 4.0
    vien = 5 * s
    if k == "than":
        im[m] = PAL["than"]
        ys, xs = np.nonzero(m)
        cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        rx, ry = (xs.max() - xs.min()) / 2 - vien, (ys.max() - ys.min()) / 2 - vien
        pil = Image.fromarray(im)
        d = ImageDraw.Draw(pil)
        lat = np.radians(np.linspace(-82, 82, 60))
        for lam in (-80, -46, -12, 22, 56, 86):                     # múi dọc của xương rồng tròn, mặt trước lệch sang phải
            L = np.radians(lam)
            pts = [(cx + rx * np.sin(L) * np.cos(t), cy - ry * np.sin(t)) for t in lat]
            d.line(pts, fill=PAL["gan"], width=int(round(5 * s)), joint="curve")
            for t in np.radians([-48, -8, 34, 62] if lam % 4 == 0 else [-30, 14, 50]):   # nốt gai nhỏ dọc múi
                x, y = cx + rx * np.sin(L) * np.cos(t), cy - ry * np.sin(t)
                r = 6 * s
                if K == 1:
                    d.ellipse([x - r, y - r, x + r, y + r], fill=PAL["gai"], outline=INK, width=int(round(2.5 * s)))
                else:                                           # dạng 2: gai nhỏ nhọn chĩa ra ngoài (theo hướng từ tâm quả cầu)
                    v = np.array([x - cx, y - cy - 0.25 * ry])
                    v = v / max(1e-6, np.hypot(*v))
                    nn = np.array([-v[1], v[0]])
                    q0 = np.array([x, y])
                    tam_giac = [tuple(q0 + nn * 7 * s), tuple(q0 - nn * 7 * s), tuple(q0 + v * 22 * s)]
                    d.polygon(tam_giac, fill=PAL["gai"], outline=INK)
                    d.line(tam_giac + tam_giac[:1], fill=INK, width=int(round(2.5 * s)), joint="curve")
        im = np.asarray(pil).copy()
    elif k == "mieng":
        im[m] = PAL["mieng"]
        vien = 0                                                    # lòng miệng nằm dưới vành môi: không cần viền
    elif k == "moi":
        im[m] = PAL["than"]
        # viền mực chỉ ở mép TRONG (lỗ miệng); mép ngoài hoà vào thân
        im[m & cv2.dilate(lo_mieng(m, s).astype(np.uint8), el(6 * s)).astype(bool)] = INK
        im[~m] = 255
        return im, m
    elif k == "rang":
        im[m] = PAL["gai"]
    elif k == "hoa":
        im[m] = PAL["hoa"]
    elif k == "gai":
        im[m] = PAL["gai"]
    elif k == "ban_chan":
        im[m] = PAL["than"]
        rgb = a[..., :3].astype(int)
        ngon = (a[..., 3] > 100) & (rgb.min(axis=2) > 150) & (np.abs(rgb[..., 0] - rgb[..., 1]) < 28)      # ngón chân màu kem của họ
        ngon = cv2.morphologyEx(ngon.astype(np.uint8), cv2.MORPH_OPEN, el(2 * s))
        ngon = cv2.dilate(ngon, el(3 * s)).astype(bool) & m
        im[ngon] = PAL["gai"]
        im[cv2.morphologyEx(ngon.astype(np.uint8), cv2.MORPH_GRADIENT, el(2 * s)).astype(bool) & m] = INK
    else:
        im[m] = PAL["than"]
    if vien:
        im[m & ~cv2.erode(m.astype(np.uint8), el(vien)).astype(bool)] = INK
    im[~m] = 255
    return im, m


def lo_mieng(m, s):
    """lỗ miệng của vành môi (mặt nạ m): vùng trống lớn nhất nằm KÍN trong vành (không thông ra mép khung)."""
    n, lab, st, _ = cv2.connectedComponentsWithStats((~m).astype(np.uint8), 4)
    mep = set(lab[0].tolist()) | set(lab[-1].tolist()) | set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    kin = [i for i in range(1, n) if i not in mep]
    if not kin:
        return np.zeros(m.shape, bool)
    return lab == max(kin, key=lambda i: st[i, cv2.CC_STAT_AREA])


def khung_T():
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["cur"]])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = (H + (y1 - y0) * SC) / 2 + y0 * SC
    return lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


def bo_cuc(luu=True, chi=None):
    """sơ đồ bố cục: các part (thiết kế của mình) đặt đúng chỗ dáng gốc, đúng thứ tự vẽ."""
    imgs, by, atts = nap()
    T = khung_T()
    S2 = 2
    can = Image.new("RGBA", (W * S2, H * S2), (255, 255, 255, 255))
    for a in atts:
        if not a["cur"] or (chi and a["att"] not in chi):
            continue
        im, m = thiet_ke(a["att"])
        src = Image.fromarray(np.dstack([im, m.astype(np.uint8) * 255]), "RGBA").convert("RGBa")
        uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([m.shape[1], m.shape[0]])
        V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
        lay = Image.new("RGBa", can.size, (0, 0, 0, 0))
        _tris(lay, src, V, uv, np.array(a["tris"]).reshape(-1, 3))
        can = Image.alpha_composite(can, lay.convert("RGBA"))
    out = can.convert("RGB").resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        out.save(os.path.join(MAU, "bo_cuc.png"))
        print(os.path.join(MAU, "bo_cuc.png"))
        for a in atts:                                               # in chỗ từng part trên khung (để viết prompt)
            if a["cur"]:
                V = T(np.array(a["xy"], float).reshape(-1, 2))
                print(f"  {a['order']:2d} {a['att']:12s} x {V[:, 0].min():5.0f}–{V[:, 0].max():5.0f}  y {V[:, 1].min():5.0f}–{V[:, 1].max():5.0f}")
    return out


def xuat_part_goc():
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    _, _, atts = nap()
    for a in atts:
        part_goc(a["att"]).save(os.path.join(ra, f"{a['order']:02d}_{a['att'].replace(' ', '')}.png"))
    print(ra, len(atts), "part")


# ---------------------------------------------------------------- tờ mảnh theo khung part
def o_them(ten):
    """ô không phải part của rig, vẽ phẳng bằng mã để Codex vẽ lại: gai vừa / gai dài chĩa sang PHẢI (gốc tròn bên trái), ụ đất."""
    w, h = THEM[ten]
    pil = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(pil)
    if ten.startswith("gai"):
        cy, r = h / 2, h / 2 - 12
        pts = [(14 + r * 0.45, cy - r), (w - 12, cy), (14 + r * 0.45, cy + r)]
        d.polygon(pts, fill=PAL["gai"], outline=INK)
        d.ellipse([12, cy - r, 12 + r * 0.9, cy + r], fill=PAL["gai"], outline=INK, width=8)
        d.polygon([(14 + r * 0.45, cy - r + 8), (w - 30, cy), (14 + r * 0.45, cy + r - 8)], fill=PAL["gai"])
        d.line(pts, fill=INK, width=8, joint="curve")
    else:
        for (cx, cy, rx, ry) in ((w * 0.5, h * 0.62, w * 0.44, h * 0.34), (w * 0.3, h * 0.5, w * 0.2, h * 0.3), (w * 0.62, h * 0.42, w * 0.22, h * 0.3)):
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=PAL["dat"], outline=INK, width=8)
        d.ellipse([w * 0.12, h * 0.36, w * 0.88, h * 0.9], fill=PAL["dat"])
        for (x0, y0, x1, y1) in ((0.3, 0.5, 0.42, 0.72), (0.42, 0.72, 0.36, 0.84), (0.6, 0.45, 0.66, 0.7), (0.5, 0.3, 0.52, 0.5)):
            d.line([(w * x0, h * y0), (w * x1, h * y1)], fill=PAL["dat_dam"], width=6)
    im = np.asarray(pil).copy()
    return im, im.min(axis=2) < 236


def nhom_part():
    """ba tờ hướng dẫn: mỗi part một ô ĐÚNG KHUNG ảnh vùng của nó (× tỉ lệ của tờ), trong ô là hình bóng kín tô phẳng theo thiết kế
    của mình (thiet_ke), viền sẫm đúng mép. Ghi mau/part_<tờ>.png và .json ({ô: x, y, w, h, z})."""
    os.makedirs(MAU, exist_ok=True)
    for to, (z, ds) in TO.items():
        im = np.full((H, W, 3), 255, np.uint8)
        khung = {}
        x, y, hh, le = 26, 26, 0, 26
        for ten in ds:
            cell, m = o_them(ten) if ten in THEM else thiet_ke(ten, z)
            h, w = m.shape
            if x + w + le > W:
                x, y, hh = le, y + hh + le, 0
            if y + h + le > H:
                raise SystemExit(f"tờ {to}: ô {ten} không vừa (y = {y}, cao {h})")
            im[y:y + h, x:x + w] = cell
            khung[ten] = {"x": x, "y": y, "w": w, "h": h, "z": z, "dem": DEM.get(ten, 0)}
            x += w + le
            hh = max(hh, h)
        Image.fromarray(im).save(os.path.join(MAU, f"part_{to}.png"))
        json.dump(khung, open(os.path.join(MAU, f"part_{to}.json"), "w", encoding="utf-8"), indent=1)
        print(f"{to} (x{z}):", ", ".join(f"{k} {v['w']}x{v['h']} @ {v['x'] + v['w'] // 2},{v['y'] + v['h'] // 2}" for k, v in khung.items()))


def cat_part(to, ep=False):
    """cắt tờ N_<tờ>: mỗi part lấy đúng Ô của nó trên tờ (Codex vẽ đúng chỗ, đúng cỡ nên ô đó chính là khung ảnh vùng của part), tách
    nền trắng → manh/part/<hình>.png (cỡ ô trên tờ; rig tự co). Đo IoU với hình bóng hướng dẫn; chỉ ghi đè khi bản mới khít hơn
    (ep=True: ghi đè). Dọn bằng mã (không vẽ): cắt sát hình bóng nới vài px; chỗ vẽ hụt lấy màu tô gần nhất của tờ hướng dẫn; kẻ nét
    mực dọc phía trong mép lưới (lưới của họ ôm sát hình bóng, xén vào viền của mình)."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, f"N_{to}")
    if not path:
        print(to, "chưa có ảnh")
        return
    khung = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, f"_N_{to}_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=300, gop_px=12)
    gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    _, by, _ = nap("att_goc.json")
    pso = os.path.join(ra, "_iou.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    ids = [i for m_ in tt.manh for i in m_["ids"]]
    print(os.path.basename(path))
    for ten, kv in khung.items():
        x, y, w, h, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + h, x:x + w].min(axis=2) < 236                       # hình bóng trên tờ hướng dẫn
        cell = tt.rgba[y:y + h, x:x + w].copy()
        lab = tt.lab[y:y + h, x:x + w]
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[g].ravel().tolist()) - {0}:
            if i in ids:
                giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & g).sum() / max(1, (a | g).sum())
        cu = SO.get(ten, [0, ""])
        if not ep and cu[1] and cu[0] >= iou:
            print(f"  {ten}: IoU {iou:.2f}, giữ bản cũ (IoU {cu[0]:.2f})")
            continue
        bu = 0
        if ten not in KHONG_SAT:
            sat = cv2.dilate(g.astype(np.uint8), el(0.75 * z)).astype(bool)
            cell[..., 3][~sat] = 0
            a &= sat
            ho = g & ~a
            bu = int(ho.sum())
            if ho.any():                                                  # vẽ hụt trong hình bóng: lấy màu tô gần nhất của tờ hướng dẫn
                gc = gd[y:y + h, x:x + w]
                to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105)
                if to_.any():
                    _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                    tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                    tra[lb[to_]] = gc[to_]
                    cell[ho, :3] = tra[lb][ho]
                    cell[ho, 3] = 255
            if ten in by and loai(ten) in ("than", "rang", "chi", "ban_chan"):      # hoa, gai mang hình bóng riêng: không kẻ theo lưới họ
                at = by[ten]
                hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
                hm = np.zeros(a.shape, np.uint8)
                cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
                dai = hm.astype(bool) & ~cv2.erode(hm, el(1.1 * z), borderValue=0).astype(bool)
                cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), os.path.basename(path)]
        Image.fromarray(cell, "RGBA").save(os.path.join(ra, ten + ".png"))
        print(f"  {ten}: {w} x {h} (x{z}), IoU {iou:.2f}" + (f", bù {bu} px" if bu else ""))
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)


def so_part():
    """tờ so từng part đã cắt với hình bóng hướng dẫn: ĐỎ = hình bóng mà mảnh không phủ, XANH LÁ = vẽ thừa → mau/so_part.png."""
    cells = []
    for to in TO:
        pj = os.path.join(MAU, f"part_{to}.json")
        if not os.path.exists(pj):
            continue
        Kh = json.load(open(pj, encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        for ten, v in Kh.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm):
                continue
            x, y, w, h = v["x"], v["y"], v["w"], v["h"]
            g = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a = c[..., 3] > 127
            im = np.full((h, w, 3), 255, np.uint8)
            im[a] = c[..., :3][a]
            im[g & ~a] = (255, 0, 0)
            im[a & ~g] = (im[a & ~g] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
            cv2.putText(im, f"{to} {ten}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cells.append(im)
    Wd, x, y, hh, pos = 1900, 0, 0, 0, []
    for im in cells:
        h, w = im.shape[:2]
        if x + w > Wd:
            x, y, hh = 0, y + hh + 10, 0
        pos.append((x, y))
        x += w + 10
        hh = max(hh, h)
    S = np.full((y + hh, Wd, 3), 230, np.uint8)
    for im, (x, y) in zip(cells, pos):
        S[y:y + im.shape[0], x:x + min(im.shape[1], Wd - x)] = im[:, :Wd - x]
    Image.fromarray(S).save(os.path.join(MAU, "so_part.png"))
    print(os.path.join(MAU, "so_part.png"), len(cells), "ô")


def moi():
    """VÀNH MÔI (người dùng 2026-11-12: "cảm giác như có phần môi ở trên, bỏ line vẽ môi đi"): vành môi của rig là một lưới riêng phủ lên
    thân quanh lỗ miệng. Để KHÔNG thấy môi: da của vành môi = chính da thân nằm dưới nó ở dáng gốc, NƯỚNG vào khung vành môi (thế giới
    dáng gốc → ảnh vùng qua lưới của hai part), nên múi dọc chạy liền qua mép vành; mép ngoài mờ dần; chỉ giữ của Codex nét mực dọc
    mép lỗ miệng. → manh/part_moi/P_zuichun.png (rig ưu tiên dùng)."""
    _, by, _ = nap("att_goc.json")
    pt = os.path.join(MANH, "part")
    than = Image.open(os.path.join(pt, "P_shenti.png")).convert("RGBA")
    mo = Image.open(os.path.join(pt, "P_zuichun.png")).convert("RGBA")
    at, am = by["P_shenti"], by["P_zuichun"]
    kq = 4.0                                                           # px bức vẽ thế giới mỗi đơn vị rig
    xy_t, xy_m = np.array(at["xy"], float).reshape(-1, 2), np.array(am["xy"], float).reshape(-1, 2)
    Pq = np.concatenate([xy_t, xy_m])
    x0, y1 = Pq[:, 0].min() - 8, Pq[:, 1].max() + 8
    cw, ch = int((Pq[:, 0].max() - x0 + 8) * kq), int((y1 - Pq[:, 1].min() + 8) * kq)
    can = lambda xy: np.stack([(xy[:, 0] - x0) * kq, (y1 - xy[:, 1]) * kq], 1)          # noqa: E731
    lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
    _tris(lay, than.convert("RGBa"), can(xy_t), np.array(at["uv"], float).reshape(-1, 2) * np.array(than.size), np.array(at["tris"]).reshape(-1, 3))
    out = Image.new("RGBa", mo.size, (0, 0, 0, 0))
    _tris(out, lay, np.array(am["uv"], float).reshape(-1, 2) * np.array(mo.size), can(xy_m), np.array(am["tris"]).reshape(-1, 3))
    nuong = np.asarray(out.convert("RGBA")).astype(np.float32)
    g = np.asarray(mo).astype(np.float32)
    al = g[..., 3] > 127
    z = TO["A"][0]
    s = z / 4.0
    lo = lo_mieng(al, s)
    gan_lo = cv2.dilate(lo.astype(np.uint8), el(13 * s)).astype(bool)
    toi = np.clip((150.0 - g[..., :3].max(axis=2)) / 70.0, 0, 1) * gan_lo * al        # nét mực mép lỗ miệng của Codex
    co = nuong[..., 3] > 200
    rgb = np.where(co[..., None], nuong[..., :3], g[..., :3])
    rgb = rgb * (1 - toi[..., None]) + g[..., :3] * toi[..., None]
    # mép ngoài mờ dần (không viền): alpha theo khoảng cách tới mép ngoài của vành; mép lỗ miệng giữ sắc
    kin = al | lo
    dt = cv2.distanceTransform(kin.astype(np.uint8), cv2.DIST_L2, 5)
    a = np.clip(dt / (7.0 * s), 0, 1) * al
    # vành môi KHÔNG phủ lên viền mực của thân: chỗ vành sát mép quả cầu mà mang theo bản sao viền thân thì lúc há miệng (vành
    # giãn) hiện hai đường viền. Vành dừng cách mép thân 9 px (viền thân ~4 px + dải mực mép lưới)
    trong_than = cv2.distanceTransform((nuong[..., 3] > 200).astype(np.uint8), cv2.DIST_L2, 5)
    a *= np.clip((trong_than - 9.0) / 3.0, 0, 1)
    res = np.dstack([rgb, a * 255]).astype(np.uint8)
    ra = os.path.join(MANH, "part_moi")
    os.makedirs(ra, exist_ok=True)
    Image.fromarray(res, "RGBA").save(os.path.join(ra, "P_zuichun.png"))
    # lòng miệng nằm dưới vành môi và rộng gần bằng vành: màu đỏ rượu lộ qua dải mép mờ của vành thành vệt trên thân. Gọt mép lòng
    # miệng vào trong 12 px (vẫn nằm dưới phần đặc của vành, vành hẹp nhất ~35 px)
    km = np.asarray(Image.open(os.path.join(pt, "P_kouqiang.png")).convert("RGBA")).copy()
    dac = cv2.erode((km[..., 3] > 127).astype(np.uint8), el(12 * s)).astype(np.float32)
    km[..., 3] = (cv2.GaussianBlur(dac, (0, 0), 1.0) * 255).astype(np.uint8)
    Image.fromarray(km, "RGBA").save(os.path.join(ra, "P_kouqiang.png"))
    print(os.path.join(ra, "P_zuichun.png"), f"da thân phủ {100 * (co & al).sum() // max(1, al.sum())}% vành, nét mực giữ {int((toi > 0.5).sum())} px")


def main(a):
    if a[:1] == ["part_goc"]:
        xuat_part_goc()
    elif a[:1] == ["bo_cuc"]:
        bo_cuc()
    elif a[:1] == ["nhom_part"]:
        nhom_part()
    elif a[:1] == ["cat_part"]:
        for to in a[1:] or list(TO):
            cat_part(to, ep="ep" in a)
    elif a[:1] == ["so_part"]:
        so_part()
    elif a[:1] == ["moi"]:
        moi()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
