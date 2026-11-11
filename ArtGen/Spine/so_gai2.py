# -*- coding: utf-8 -*-
"""Dòng sò đột biến (so_gai), LÀM LẠI TỪ ĐẦU 2026-11-11: mảnh chia một – một theo con gốc, mỗi mảnh một hình kín do GPT vẽ.

Người dùng: "đập đi gen lại từ đầu", "lòi xòm nhiều quá, đọc lại skill ... dịch ngược file spine xem các mảnh của họ".
Con gốc (monster_3237, tờ mổ D:/Ripper/SwordxStaff/scan/monster_3237/manh_*.png) vẽ sau → trước:
    P_xiaba1 (vòm tối, bám hàm dưới) → lưỡi → P_xiaba (mặt trước hàm dưới) → nanh, gai → P_tou1 (vòm mai trên kín) → mắt (đổi ảnh).
Của mình: long → luoi / luoi_d → mai_duoi → [luoi_mep] → luoi_t → mai_tren → mat_g, mat_x → moi.
Ảnh: U01 (mai trên, đúng chỗ đúng cỡ concept, không mắt), D01 (mặt trước mai dưới), P01 (tờ: vòm tím, mắt mở, mắt nhắm, lưỡi nằm,
môi chu, lưỡi dài). Prompt: build_so_gai2.py. Mã ở đây CHỈ tách nền trắng, đặt chỗ, co giãn cả mảnh; không vá, không cắt theo màu.

    py -3 -I ArtGen/Spine/so_gai2.py cat [1|2]         tách mảnh -> inbox/so_gai_<k>/manh2/ (+ manh2.json, _soi2.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/so_gai2.py rig 1|2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/so_gai2.py all     dạng 2 rồi dạng 1 gộp dạng 2 (evolve)
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ti_tach as T  # noqa: E402
import so_gai as S   # noqa: E402  (d_inbox, concept, SC, CHAM, N_LUOI, REF_W, lo_kin, gif_nho)

sys.stdout.reconfigure(encoding="utf-8")
CODE = "so_gai"
SC, CHAM, REF_W = S.SC, S.CHAM, S.REF_W
N_LUOI = 22                    # số xương lưỡi dài (bản cũ 8: uốn gãy khúc)
INK = np.array([43, 33, 24], np.float32)
N_GIOT = 16                    # số giọt dãi văng cùng lúc tối đa ở chiêu cuối (slot dùng lại)
DAI_PHA0 = 0.25                # pha của vòng chảy dãi ở khung 0 idle
DAI_SY = [(0, .35), (55, 1.0), (62, 1.08), (66, .4), (100, .35)]      # độ dài sợi dãi theo pha (%): rủ dài dần, đứt giọt, co lại
DAI_SX = [(0, 1.0), (55, .88), (62, .8), (66, 1.06), (100, 1.0)]
DAI_SY0 = T.ln(100 * DAI_PHA0, DAI_SY)
DAI_SX0 = T.ln(100 * DAI_PHA0, DAI_SX)
DUNG_CHOP_LUOI = False         # mảnh chóp lưỡi vắt qua vành (T02, dạng 2): người dùng 2026-11-11 "thừa mảnh lưỡi ở giữa kìa" -> bỏ
DAI_LUOI = 1.62                # lưỡi dài: bề dài so với bề ngang thân
THON_LUOI = (1.0, 0.52)        # lưỡi dài: bề dày ở cuống và ở đầu lưỡi (nhân thêm, thon dần)
F_GOC = 0.17                   # cuống lưỡi dài ở bao nhiêu phần bề dài miệng tính từ bản lề (nhỏ = sâu trong họng)
DAY_LUOI = 1.9                 # lưỡi dài: bề dày nhân thêm (so với tỉ lệ theo bề dài)
GRAY = (150, 150, 150)


def doc(p):
    return np.array(Image.open(p).convert("RGB")).astype(np.float32)


def hong(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 165) & (G < 125) & (B > G + 10) & (B > 70)


def cam(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 200) & (G > 95) & (G < 175) & (B < 120) & (R - B > 90)


def vang(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 200) & (G > 175) & (B < 125)


def rgba(a, m, chi_muc=False):
    """ảnh RGBA của một mảnh: viền ngoài luôn là mực nên dải 2 px sát mép lấy màu mực, độ đậm theo độ tối (không viền sáng)."""
    mn = a.min(2)
    if chi_muc:                                                                        # mắt nhắm: chỉ nét mực, lòng trong suốt
        al = np.clip((225 - mn) / 110.0, 0, 1) * m
        rgb = np.broadcast_to(INK, a.shape).copy()
    else:
        band = m & T.gian(~m, 2)
        al = m.astype(np.float32)
        al[band] = np.clip((246 - mn[band]) / 120.0, 0, 1)
        rgb = a.copy()
        rgb[band] = INK
    return np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8)


def co_gian(im, w, h):
    """co giãn ảnh RGBA (nhân sẵn alpha để mép không ám màu nền)."""
    f = im.astype(np.float32)
    f[..., :3] *= f[..., 3:4] / 255.0
    f = cv2.resize(f, (int(w), int(h)), interpolation=cv2.INTER_AREA if w < im.shape[1] else cv2.INTER_CUBIC)
    al = np.clip(f[..., 3:4], 0, 255)
    f[..., :3] = np.where(al > 0.5, f[..., :3] * 255.0 / np.maximum(al, 0.5), 0)
    return np.clip(f, 0, 255).astype(np.uint8)


def thon(im, s0, s1):
    """bóp thon cả ảnh lưỡi duỗi ngang (cuống bên trái): bề dày mỗi cột nhân s0 ở cuống → s1 ở đầu lưỡi, quanh đường giữa của
    chính cột đó (giữ nét lượn của mép). Co giãn trơn cả mảnh, không cắt vá."""
    a = np.array(im.convert("RGBA")).astype(np.float32)
    a[..., :3] *= a[..., 3:4] / 255.0
    H, W = a.shape[:2]
    al = a[..., 3] > 40
    cy = np.array([np.nonzero(al[:, x])[0].mean() if al[:, x].any() else H / 2.0 for x in range(W)], np.float32)
    cy = cv2.GaussianBlur(cy[None, :], (0, 0), 25)[0]
    u = np.arange(W, dtype=np.float32) / max(1, W - 1)
    e = u * u * (3 - 2 * u)
    sc = s0 + (s1 - s0) * (0.35 * u + 0.65 * e)
    H2 = int(math.ceil(H * max(s0, s1))) + 4
    yy, xx = np.mgrid[0:H2, 0:W].astype(np.float32)
    my = (yy - H2 / 2.0) / sc[None, :] + cy[None, :]
    o = cv2.remap(a, xx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    al2 = np.clip(o[..., 3:4], 0, 255)
    o[..., :3] = np.where(al2 > 0.5, o[..., :3] * 255.0 / np.maximum(al2, 0.5), 0)
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8), "RGBA")


def xoay(im, goc):
    """xoay ảnh RGBA quanh tâm (độ, dương = ngược kim trên màn hình), nới khung."""
    return np.array(Image.fromarray(im, "RGBA").rotate(goc, resample=Image.BICUBIC, expand=True))


def manh_lon(p):
    a = doc(p)
    bg = T.nen_trang(a, 236)
    cs = T.cum(~bg, 400)
    big = max(cs, key=lambda c: c["dt"])
    if len(cs) > 1:
        print(f"  {os.path.basename(p)}: {len(cs)} cụm, lấy cụm lớn nhất ({big['dt']} px); cụm khác: {[c['dt'] for c in cs if c is not big]}")
    return a, T.lap_lo(big["m"])


def lech(ac, a, m, R=24):
    """độ lệch (dx, dy) của mảnh so với concept: khớp mẫu có mặt nạ trong ±R px."""
    x0, y0, x1, y1 = T.hop(m, 0)
    gc = cv2.cvtColor(ac.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    gp = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    res = cv2.matchTemplate(gc[y0 - R:y1 + R, x0 - R:x1 + R], gp[y0:y1, x0:x1], cv2.TM_SQDIFF, mask=m[y0:y1, x0:x1].astype(np.float32))
    _, _, loc, _ = cv2.minMaxLoc(res)
    n = float(m.sum())
    return loc[0] - R, loc[1] - R, math.sqrt(res[R, R] / n), math.sqrt(max(0.0, float(res.min())) / n)


def doc_to(p):
    """tờ mảnh P01: sáu ô -> dict tên -> (a, mặt nạ cụm)."""
    a = doc(p)
    bg = T.nen_trang(a, 236)
    cs = T.cum(~bg, 250)
    # gộp cụm sát nhau (mày + mí của mắt nhắm)
    cha = list(range(len(cs)))

    def goc(i):
        while cha[i] != i:
            i = cha[i]
        return i
    for i in range(len(cs)):
        for j in range(i):
            c, d = cs[i], cs[j]
            if max(c["x0"], d["x0"]) - min(c["x1"], d["x1"]) < 26 and max(c["y0"], d["y0"]) - min(c["y1"], d["y1"]) < 26:
                cha[goc(i)] = goc(j)
    nhom = {}
    for i, c in enumerate(cs):
        nhom.setdefault(goc(i), []).append(c)
    o = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": []}
    for g in nhom.values():
        m = np.zeros_like(bg)
        for c in g:
            m |= c["m"]
        x0, y0, x1, y1 = T.hop(m, 0)
        if (x1 - x0) * (y1 - y0) < 1500:
            continue
        cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        ten = "F" if cy >= 760 else (("A" if cy < 450 else "D") if cx < 860 else ("B" if cy < 250 else ("C" if cy < 450 else "E")))
        o[ten].append((x0, m))
    dem = {k: len(v) for k, v in o.items()}
    if dem != {"A": 1, "B": 2, "C": 2, "D": 1, "E": 1, "F": 1}:
        raise SystemExit(f"tờ mảnh {p}: số mảnh mỗi ô {dem}, cần A1 B2 C2 D1 E1 F1")
    for k in o:
        o[k] = [m for _, m in sorted(o[k], key=lambda t: t[0])]
    return a, o


def cat_manh(a, m, chi_muc=False, le=3):
    box = T.hop(m, le)
    x0, y0, x1, y1 = box
    return rgba(a, m, chi_muc)[y0:y1, x0:x1], box


def dan(canvas, im, x, y):
    """dán ảnh RGBA lên canvas RGBA float (alpha thường), góc trên trái (x, y)."""
    H, W = canvas.shape[:2]
    h, w = im.shape[:2]
    X0, Y0, X1, Y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    s = im[Y0 - y:Y1 - y, X0 - x:X1 - x].astype(np.float32)
    al = s[..., 3:4] / 255.0
    d = canvas[Y0:Y1, X0:X1]
    d[..., :3] = d[..., :3] * (1 - al) + s[..., :3] * al
    d[..., 3:4] = d[..., 3:4] * (1 - al) + 255.0 * al


def mat_na_tai(im, x, y, shape):
    m = np.zeros(shape, bool)
    c = np.zeros(shape + (4,), np.float32)
    dan(c, im, x, y)
    m[:] = c[..., 3] > 110
    return m


def cat(k):
    ac = doc(S.concept(k))
    Hc, Wc = ac.shape[:2]
    cu = json.load(open(os.path.join(S.d_inbox(k), "manh", "manh.json"), encoding="utf-8"))    # số đo concept (bản lề, thân, dây cung)
    thu = os.path.join(S.d_inbox(k), "tai_ve")
    ra = os.path.join(S.d_inbox(k), "manh2")
    os.makedirs(ra, exist_ok=True)
    for f in os.listdir(ra):
        os.remove(os.path.join(ra, f))
    hx, hy = cu["ban_le"]
    dc = cu["day_cung"]
    goc_dc = math.degrees(math.atan2(dc[1], dc[0]))                                    # ảnh y xuống: dương = dây cung chúc xuống phía trước
    info = {"concept": "L1_duyet.png", "manh": {}, "ban_le": [hx, hy], "day_cung": dc, "than": cu["than"], "moi_giua": cu["moi_giua"],
            "giua_mep": cu["giua_mep"], "day_vanh": cu["day_vanh"], "mep": cu["mep"]}

    # ---- hai mai: đúng chỗ đúng cỡ concept
    pcs = {}
    for ten, goc in (("mai_tren", "U01"), ("mai_duoi", "D01")):
        a, m = manh_lon(T.moi_nhat(thu, goc))
        dx, dy, e0, e1 = lech(ac, a, m)
        print(f"  {goc}: lệch concept ({dx}, {dy}) px; sai số tại chỗ {e0:.1f}, tốt nhất {e1:.1f}")
        if (dx or dy) and e1 < 0.9 * e0:
            a = np.roll(a, (dy, dx), axis=(0, 1))
            m = np.roll(m, (dy, dx), axis=(0, 1))
        im, box = cat_manh(a, m)
        Image.fromarray(im, "RGBA").save(os.path.join(ra, ten + ".png"))
        info["manh"][ten] = box
        pcs[ten] = (a, m, im, box)
    aU, Um = pcs["mai_tren"][:2]
    aD, Dm = pcs["mai_duoi"][:2]
    co_J = bool(T.moi_nhat(thu, "J01"))
    if co_J:
        # CẢ HÀM DƯỚI một ảnh (J01): lớp sau lưỡi = cả ảnh; lớp trước lưỡi (vách trước: vành gần, nanh, bát) = phần của CHÍNH ảnh đó
        # nằm dưới lòng bát. Hai lớp cùng nét vẽ, cùng xương: hai vành là một vòng liền, chỗ nối không thể lệch (người dùng trả bản
        # D01 + B01 rời: "mép nối đầu miệng không match bị lệch"). Đường tách chỉ quyết định lưỡi bị che từ đâu.
        aJ, mJ = manh_lon(T.moi_nhat(thu, "J01"))
        Rj, Bj = aJ[..., 0], aJ[..., 2]
        ins = mJ & (aJ.max(2) < 125) & (Bj > Rj + 10)                                  # lòng bát: màu tối của vỏ (lam lục / chàm sẫm)
        ins = cv2.morphologyEx(ins.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
        cs_i = T.cum(ins, 200)
        lon = max(c["dt"] for c in cs_i)
        ins = np.zeros_like(ins)
        for c in cs_i:
            if c["dt"] > 0.05 * lon:
                ins |= c["m"]
        xi = np.nonzero(ins.any(0))[0]
        x0i, x1i = int(xi.min()), int(xi.max())
        ycut = np.full(Wc, -1.0)
        for x in xi:
            ycut[x] = np.nonzero(ins[:, x])[0].max()
        co_ = np.nonzero(ycut >= 0)[0]
        ycut = np.interp(np.arange(Wc), co_, ycut[co_])
        truoc = np.zeros_like(mJ)
        for x in np.nonzero(mJ.any(0))[0]:
            if x < x0i or x > x1i:
                truoc[:, x] = mJ[:, x]                                                 # hai đầu, ngoài lòng bát: hai vành đã nhập làm một
            else:
                y = int(ycut[x]) + 1
                truoc[y:, x] = mJ[y:, x]
        truoc = max(T.cum(truoc, 300), key=lambda c: c["dt"])["m"]
        dx, dy, e0, e1 = lech(ac, aJ, truoc)
        print(f"  J01: lệch concept ({dx}, {dy}) px (đo trên vách trước); sai số tại chỗ {e0:.1f}, tốt nhất {e1:.1f}; lòng bát {int(ins.sum())} px, cột {x0i}..{x1i}")
        if (dx or dy) and e1 < 0.9 * e0 and abs(dx) < 12 and abs(dy) < 12:
            aJ = np.roll(aJ, (dy, dx), axis=(0, 1))
            mJ = np.roll(mJ, (dy, dx), axis=(0, 1))
            truoc = np.roll(truoc, (dy, dx), axis=(0, 1))
        imJ = rgba(aJ, mJ)
        bJ = T.hop(mJ, 3)
        Image.fromarray(imJ[bJ[1]:bJ[3], bJ[0]:bJ[2]], "RGBA").save(os.path.join(ra, "long.png"))
        info["manh"]["long"] = bJ
        imF = imJ.copy()
        imF[~truoc, 3] = 0                                                             # mép tách giữ nguyên màu, không tô mực (kẻo có vạch qua vành)
        bF = T.hop(truoc, 3)
        Image.fromarray(imF[bF[1]:bF[3], bF[0]:bF[2]], "RGBA").save(os.path.join(ra, "mai_duoi.png"))
        info["manh"]["mai_duoi"] = bF
        aD, Dm = aJ, truoc
    fgc = T.lap_lo(~T.nen_trang(ac))
    V = fgc & ~Um & ~Dm
    V = cv2.morphologyEx(V.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
    cs = T.cum(V, 600)
    V = np.zeros_like(V)
    for c in cs:
        V |= c["m"]
    Pc = hong(ac) & fgc
    Pc = cv2.morphologyEx(Pc.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
    vx0, vy0, vx1, vy1 = T.hop(V, 0)
    print(f"  khe miệng lúc nghỉ: {int(V.sum())} px, khung {vx0, vy0, vx1, vy1}")

    # ---- góc khép: xoay vành cam mai trên quanh bản lề tới khi chạm / đè vành cam mai dưới (đo ở khúc giữa miệng)
    cU, cD = (cam(aU) & Um).astype(np.uint8), cam(aD) & Dm
    L_m = vx1 - hx
    cot = np.arange(int(hx + 0.3 * L_m), int(hx + 0.8 * L_m))
    topD = np.array([np.nonzero(cD[:, x])[0].min() if cD[:, x].any() else -1 for x in cot])
    g_cham = g_khit = None
    for g in np.arange(1, 60, 0.5):
        M = cv2.getRotationMatrix2D((hx, hy), -g, 1.0)
        r = cv2.warpAffine(cU, M, (Wc, Hc), flags=cv2.INTER_NEAREST) > 0
        khe = np.array([topD[i] - np.nonzero(r[:, x])[0].max() for i, x in enumerate(cot) if r[:, x].any() and topD[i] >= 0])
        if len(khe) < 20:
            continue
        if g_cham is None and khe.min() <= 0:
            g_cham = float(g)
        if np.median(khe) <= -0.25 * cu["day_vanh"]:
            g_khit = float(g)
            break
    info["g_cham"], info["g_khit"] = g_cham or 10.0, g_khit or 22.0
    print(f"  góc chạm {info['g_cham']:.1f}°, góc khép khít {info['g_khit']:.1f}°")

    # ---- tờ mảnh
    ap, o = doc_to(T.moi_nhat(thu, "P01"))

    # mắt: cỡ và chỗ theo mắt vàng của concept
    yc = sorted(T.cum(vang(ac) & fgc, 250), key=lambda c: -c["dt"])[:2]
    yc = sorted(yc, key=lambda c: c["x0"])                                             # gần (trái), xa (phải)
    info["mat"] = []
    for i, ten in enumerate(("mat_g", "mat_x")):
        mo, nh = o["B"][i], o["C"][i]
        yp = vang(ap) & mo
        px0, py0, px1, py1 = T.hop(yp, 0)
        c = yc[i]
        s = math.sqrt(((c["x1"] - c["x0"]) / (px1 - px0)) * ((c["y1"] - c["y0"]) / (py1 - py0)))
        im, box = cat_manh(ap, mo)
        im2 = co_gian(im, round(im.shape[1] * s), round(im.shape[0] * s))
        # tâm vàng của mảnh trùng tâm vàng concept
        gx = (c["x0"] + c["x1"]) / 2.0 - ((px0 + px1) / 2.0 - box[0]) * s
        gy = (c["y0"] + c["y1"]) / 2.0 - ((py0 + py1) / 2.0 - box[1]) * s
        b1 = [int(round(gx)), int(round(gy)), int(round(gx)) + im2.shape[1], int(round(gy)) + im2.shape[0]]
        Image.fromarray(im2, "RGBA").save(os.path.join(ra, ten + "_mo.png"))
        info["manh"][ten + "_mo"] = b1
        # mắt nhắm: cùng tỉ lệ, mày trùng mày (góc trên trái của khung mảnh trùng nhau, vì GPT vẽ mày cùng chỗ cùng góc)
        imn, boxn = cat_manh(ap, nh, chi_muc=True)
        imn2 = co_gian(imn, round(imn.shape[1] * s), round(imn.shape[0] * s))
        # canh theo mày: mép trên và tâm ngang của nét mực trên cùng
        b2 = [b1[0] + round(((boxn[0] + boxn[2]) / 2.0 - (box[0] + box[2]) / 2.0 - (T.hop(nh, 0)[0] + T.hop(nh, 0)[2] - T.hop(mo, 0)[0] - T.hop(mo, 0)[2]) / 2.0) * s),
              b1[1]]
        b2[0] = int(round((b1[0] + b1[2]) / 2.0 - imn2.shape[1] / 2.0))
        b2 += [b2[0] + imn2.shape[1], b2[1] + imn2.shape[0]]
        Image.fromarray(imn2, "RGBA").save(os.path.join(ra, ten + "_nham.png"))
        info["manh"][ten + "_nham"] = b2
        info["mat"].append({"ti": s, "tam": [(c["x0"] + c["x1"]) / 2.0, (c["y0"] + c["y1"]) / 2.0]})
        print(f"  {ten}: tỉ lệ {s:.3f}, khung {b1}")

    cD_top = np.array([np.nonzero(cD[:, x])[0].min() if cD[:, x].any() else -1 for x in range(Wc)])
    yy, xx = np.mgrid[0:Hc, 0:Wc]
    de = Pc & Dm                                                                       # chóp lưỡi vắt trước mai dưới (dạng 2)
    de = cv2.morphologyEx(de.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
    info["luoi_mep"] = False

    def dung_cho(goc, ten_ra):
        """mảnh GPT vẽ đúng chỗ đúng cỡ concept: tách nền, chỉnh lệch vài px, lưu."""
        a, m = manh_lon(T.moi_nhat(thu, goc))
        dx, dy, e0, e1 = lech(ac, a, m)
        if (dx or dy) and e1 < 0.9 * e0 and abs(dx) < 12 and abs(dy) < 12:
            a = np.roll(a, (dy, dx), axis=(0, 1))
            m = np.roll(m, (dy, dx), axis=(0, 1))
        im, box = cat_manh(a, m)
        Image.fromarray(im, "RGBA").save(os.path.join(ra, ten_ra + ".png"))
        info["manh"][ten_ra] = box
        return a, m, box

    # ---- lưỡi nằm: có T01 (GPT vẽ đúng chỗ đúng cỡ) thì dùng thẳng; chóp vắt mép là mảnh riêng T02 vẽ trước mai dưới
    if T.moi_nhat(thu, "T01"):
        _, Tm, bT = dung_cho("T01", "luoi_nghi")
        lo = T.hop(Tm & (V | T.gian(de, 4)), 0)
        info["luoi_lo"] = lo
        print(f"  lưỡi nằm (T01): khung {bT}; phần thấy {lo}; hồng concept chưa phủ {int((V & Pc & ~Tm).sum())} px, lưỡi đè lên tím {int((Tm & V & ~T.gian(Pc, 6)).sum())} px")
        if DUNG_CHOP_LUOI and T.moi_nhat(thu, "T02"):
            _, m2, b2 = dung_cho("T02", "luoi_mep")
            info["luoi_mep"] = True
            info["luoi_mep_rieng"] = True
            print(f"  chóp lưỡi vắt mép (T02): khung {b2}; nằm ngoài chóp của concept {int((m2 & ~T.gian(de, 10)).sum())} px; chóp concept chưa phủ {int((de & ~m2).sum())} px")
    else:
        # ---- lưỡi nằm: co giãn đều + đặt chỗ, khớp phần hồng thấy trong khe miệng (và chóp vắt mép của dạng 2)
        imT, boxT = cat_manh(ap, o["D"][0])
        al0 = imT[..., 3] > 110
        day = np.array([np.nonzero(al0[:, x])[0].max() if al0[:, x].any() else -1 for x in range(al0.shape[1])])
        yb = float(np.median(day[int(0.1 * len(day)):int(0.6 * len(day))]))                 # đáy của thân lưỡi
        cols = np.nonzero(day > yb + 18)[0]
        cols = cols[cols > 0.5 * len(day)]
        chop = np.zeros(imT.shape, np.uint8)                                               # ảnh phụ: các cột của chóp rủ xuống
        if len(cols) > 12:
            chop[:, int(cols.min()):int(cols.max()) + 1] = 255
        if abs(goc_dc) > 1.5:
            imT = xoay(imT, -goc_dc)
            chop = xoay(chop, -goc_dc)
        mT = (imT[..., 3] > 110).astype(np.float32)
        cD_top = np.array([np.nonzero(cD[:, x])[0].min() if cD[:, x].any() else -1 for x in range(Wc)])
        yy, xx = np.mgrid[0:Hc, 0:Wc]
        Pd = T.gian(Pc, 6)
        de = Pc & Dm                                                                       # chóp lưỡi vắt trước mai dưới (dạng 2)
        de = cv2.morphologyEx(de.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
        cho_phep = Um | Dm | V | T.gian(de, 8)
        Wm = np.zeros((Hc, Wc), np.float32)
        Wm[V & Pd] = 2.0
        Wm[V & ~Pd] = -1.5
        Wm[de] = 2.0
        if de.sum() > 800:                                                                 # quanh chóp vắt mép: thân lưỡi nằm TRÊN vành, không chìm sau mai dưới
            dx0, _, dx1, _ = T.hop(de, 0)
            chim = Dm & ~T.gian(de, 8) & (xx > dx0 - 50) & (xx < dx1 + 30) & (cD_top[None, :] >= 0) & (yy > cD_top[None, :] + 2)
            Wm[chim] = -2.0
        Wm[~cho_phep] = -3.0
        best = None
        h2 = cv2.resize(Wm, (Wc // 2, Hc // 2), interpolation=cv2.INTER_AREA)
        for s in np.arange(0.55, 1.36, 0.025):
            t = cv2.resize(mT, (max(4, round(mT.shape[1] * s / 2)), max(4, round(mT.shape[0] * s / 2))), interpolation=cv2.INTER_AREA)
            if t.shape[0] >= h2.shape[0] or t.shape[1] >= h2.shape[1]:
                continue
            res = cv2.matchTemplate(h2, t, cv2.TM_CCORR)
            _, mx, _, loc = cv2.minMaxLoc(res)
            if best is None or mx > best[0]:
                best = (mx, s, loc[0] * 2, loc[1] * 2)
        _, sT, tx, ty = best
        imT2 = co_gian(imT, round(imT.shape[1] * sT), round(imT.shape[0] * sT))
        bT = [int(tx), int(ty), int(tx) + imT2.shape[1], int(ty) + imT2.shape[0]]
        Image.fromarray(imT2, "RGBA").save(os.path.join(ra, "luoi_nghi.png"))
        info["manh"]["luoi_nghi"] = bT
        Tm = mat_na_tai(imT2, bT[0], bT[1], (Hc, Wc))
        lo = T.hop(Tm & (V | T.gian(de, 4)), 0)
        info["luoi_lo"] = lo
        print(f"  lưỡi nằm: tỉ lệ {sT:.3f}, khung {bT}; phần thấy {lo}; hồng concept chưa phủ {int((V & Pc & ~Tm).sum())} px, lưỡi đè lên tím {int((Tm & V & ~Pd).sum())} px")
        if de.sum() > 800:                                                                 # dạng 2: chóp lưỡi vắt qua mép = CÙNG ảnh lưỡi, chỉ giữ chóp, vẽ trước mai dưới
            chop2 = co_gian(chop, imT2.shape[1], imT2.shape[0])[..., 3].astype(np.float32) / 255.0
            if chop2.max() > 0.5:
                tip = imT2.copy().astype(np.float32)
                giu = np.zeros(chop2.shape, np.float32)
                hang = np.arange(chop2.shape[0])
                for x in range(chop2.shape[1]):
                    if chop2[:, x].max() < 0.02:
                        continue
                    X = bT[0] + x
                    yv = cD_top[X] if 0 <= X < Wc and cD_top[X] >= 0 else -1
                    if yv < 0:
                        near = np.nonzero(cD_top >= 0)[0]
                        yv = cD_top[near[np.argmin(np.abs(near - X))]]
                    y_cut = yv - 7 - bT[1]                                                  # mép trên viền mực của vành gần
                    giu[:, x] = np.clip((hang - y_cut) / 4.0, 0, 1) * chop2[:, x]
                tip[..., 3] *= giu
                Image.fromarray(np.clip(tip, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(ra, "luoi_mep.png"))
                info["manh"]["luoi_mep"] = bT
                info["luoi_mep"] = True
                thua = int(((tip[..., 3] > 110) & ~T.gian(de, 10)[bT[1]:bT[3], bT[0]:bT[2]]).sum()) if bT[3] <= Hc and bT[2] <= Wc else -1
                print(f"  chóp lưỡi vắt mép: cùng ảnh lưỡi, chỉ giữ chóp, vẽ trước mai dưới; phần nằm ngoài chóp của concept {thua} px")

    # ---- lớp sau lưỡi = NỬA SAU CỦA HÀM DƯỚI (B01: mặt trong vỏ + vành xa; người dùng: "xóa mảng tím", con sò chỉ có hai hàm,
    # không có thịt). L01 (vòm tím) là bản cũ đã bị trả, chỉ dùng khi chưa có B01.
    goc_sau = "J01" if co_J else ("B01" if T.moi_nhat(thu, "B01") else ("L01" if T.moi_nhat(thu, "L01") else None))

    def do_nghi(Gm_, d1_):
        """dáng nghỉ: concept há miệng hơn con gốc nên giữa vành trên và vành xa có thể còn khe nhìn xuyên. Như con gốc (lúc nghỉ
        vành trên che vành xa), hạ mai trên một góc nhỏ nhất đủ để hết khe. Không tính 45 px cuối trước đầu miệng (khuyết tự nhiên)."""
        che_ = Gm_ | Dm | Tm
        xu_ = np.nonzero(cU.any(0))[0]
        cot_ = np.arange(int(hx + 40), int(min(d1_, float(xu_.max())) - 45))
        k0 = kq = 0
        info["nghi_tren"] = -16.0
        for g in np.arange(0, 16.01, 0.5):
            M = cv2.getRotationMatrix2D((hx, hy), -g, 1.0)
            r = cv2.warpAffine(cU, M, (Wc, Hc), flags=cv2.INTER_NEAREST) > 0
            kq = 0
            for x in cot_:
                ys = np.nonzero(r[:, x])[0]
                if not len(ys):
                    continue
                duoi = np.nonzero(che_[int(ys.max()) + 1:, x])[0]
                if len(duoi):
                    kq += int(duoi[0])
            if g == 0:
                k0 = kq
            if kq < 150:
                info["nghi_tren"] = -float(g)
                break
        print(f"  dáng nghỉ: khe nhìn xuyên giữa vành trên và vành xa ở dáng concept {k0} px; hạ mai trên {-info['nghi_tren']:.1f}° thì còn {kq} px")

    if goc_sau == "J01":
        Gm = mJ
        do_nghi(Gm, float(np.nonzero(cD.any(0))[0].max()) - 2)
        ho = V & ~Tm & ~Gm
        loi = Gm & ~T.gian(T.lap_lo(Um | Dm | V), 2)
        print(f"  hàm dưới (J01): khung {info['manh']['long']}; khe miệng lúc nghỉ không được che {int(ho.sum())} px; lòi khỏi bóng concept {int(loi.sum())} px")
    elif goc_sau == "B01":
        # mặt trong cái bát: co giãn NGANG cả mảnh cho hai đầu vành xa trùng hai đầu vành gần; phần bụng tràn ra ngoài bóng vách
        # trước (ở dưới vành gần, vốn phải khuất) thì bỏ: mép bỏ nằm dưới viền mực của vách trước nên không lộ
        aB, mB = manh_lon(T.moi_nhat(thu, "B01"))
        xs_d = np.nonzero(cD.any(0))[0]
        xs_b = np.nonzero(mB.any(0))[0]
        d0, d1, b0, b1 = float(xs_d.min()) + 9, float(xs_d.max()) - 2, float(xs_b.min()), float(xs_b.max())
        kx = (d1 - d0) / (b1 - b0)
        Mx = np.float32([[kx, 0, d0 - kx * b0], [0, 1, 0]])
        aB = cv2.warpAffine(aB, Mx, (Wc, Hc), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
        mB = cv2.warpAffine(mB.astype(np.uint8), Mx, (Wc, Hc), flags=cv2.INTER_NEAREST) > 0
        top = cD_top.astype(np.float32).copy()
        co_ = np.nonzero(top >= 0)[0]
        top = np.interp(np.arange(Wc), co_, top[co_])
        tran = mB & (yy > top[None, :] + 10) & ~T.co(T.lap_lo(Dm), 3)
        mB &= ~tran
        mB = max(T.cum(mB, 400), key=lambda c: c["dt"])["m"]
        im, bG = cat_manh(aB, mB)
        Image.fromarray(im, "RGBA").save(os.path.join(ra, "long.png"))
        info["manh"]["long"] = bG
        Gm = mB
        than_ = T.lap_lo(Um | Dm | V)
        loi = Gm & ~T.gian(than_, 2)
        ho = V & ~Tm & ~Gm
        # dáng nghỉ: concept há miệng hơn con gốc nên giữa vành trên và vành xa còn một khe nhìn xuyên ở phía đầu miệng. Như con
        # gốc (lúc nghỉ vành trên che vành xa), hạ mai trên một góc nhỏ nhất đủ để hết khe.
        che = Gm | Dm | Tm
        xu = np.nonzero(cU.any(0))[0]
        cot_n = np.arange(int(hx + 40), int(min(d1, float(xu.max())) - 45))
        info["nghi_tren"] = 0.0
        for g in np.arange(0, 16.01, 0.5):
            M = cv2.getRotationMatrix2D((hx, hy), -g, 1.0)
            r = cv2.warpAffine(cU, M, (Wc, Hc), flags=cv2.INTER_NEAREST) > 0
            khe = 0
            for x in cot_n:
                ys = np.nonzero(r[:, x])[0]
                if not len(ys):
                    continue
                yb = int(ys.max())
                duoi = np.nonzero(che[yb + 1:, x])[0]
                if len(duoi):
                    khe += int(duoi[0])
            if g == 0:
                khe0 = khe
            if khe < 150:
                info["nghi_tren"] = -float(g)
                break
        else:
            info["nghi_tren"] = -16.0
        print(f"  dáng nghỉ: khe nhìn xuyên giữa vành trên và vành xa ở dáng concept {khe0} px; hạ mai trên {-info['nghi_tren']:.1f}° thì còn {khe} px")
        print(f"  mặt trong hàm dưới (B01): co ngang {kx:.3f}, bỏ {int(tran.sum())} px bụng tràn khỏi vách trước; khung {bG}; "
              f"khe miệng lúc nghỉ không được che {int(ho.sum())} px; lòi khỏi thân {int(loi.sum())} px")
    elif goc_sau:
        _, Gm, bG = dung_cho(goc_sau, "long")
        than_ = T.lap_lo(Um | Dm | V)
        loi = Gm & ~T.gian(than_, 2)
        ho = V & ~Tm & ~Gm
        print(f"  nửa sau hàm dưới ({goc_sau}): khung {bG}; khe miệng chưa phủ {int(ho.sum())} px; lòi khỏi thân {int(loi.sum())} px")
        info["long_loi"] = int(loi.sum())
    else:
        # ---- vòm tím (lớp sau lưỡi): xoay theo dây cung, co giãn rộng / cao riêng, đặt sao cho phủ hết khe miệng mà không lòi khỏi thân
        imG, _ = cat_manh(ap, o["A"][0])
        if abs(goc_dc) > 1.5:
            imG = xoay(imG, -goc_dc)
        mG = (imG[..., 3] > 110).astype(np.float32)
        aGm = imG[..., :3].astype(np.float32)
        mGc = (cam(aGm) & (mG > 0)).astype(np.float32)                                      # dải cam ở dây cung
        pts = np.argwhere(Um | Dm)[:, ::-1].astype(np.int32)
        hull = np.zeros((Hc, Wc), np.uint8)
        cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
        yU_tip = int(np.nonzero(cU[:, min(Wc - 1, vx1 - 8)])[0].min()) if cU[:, min(Wc - 1, vx1 - 8)].any() else vy0
        cho2 = T.lap_lo(Um | Dm | V) | ((hull > 0) & (xx >= vx1 - 60) & (yy >= yU_tip - 10) & (yy <= vy1 + 10))
        cho2 = T.co(cho2, 3)
        Wd = np.zeros((Hc, Wc), np.float32)
        Wd[Um] = 0.02
        Wd[Dm & (cD_top[None, :] >= 0) & (yy > cD_top[None, :] + 60)] = -0.6             # dây cung nằm ngay sau vành gần, không chìm sâu trong bát
        Wd[V & ~Tm] = 1.0
        Wd[~cho2] = -3.0
        Wc_ = np.zeros((Hc, Wc), np.float32)
        Wc_[~(Um | Dm)] = -2.0
        Wd2 = cv2.resize(Wd, (Wc // 2, Hc // 2), interpolation=cv2.INTER_AREA)
        Wc2 = cv2.resize(Wc_, (Wc // 2, Hc // 2), interpolation=cv2.INTER_AREA)
        th = cu["than"]
        Hu = hy - th["y_top"]
        best = None
        for w in np.arange(0.86, 1.13, 0.02) * (vx1 - hx):
            for h in np.arange(0.45, 1.16, 0.05) * Hu:
                sz = (max(4, round(w / 2)), max(4, round(h / 2)))
                t = cv2.resize(mG, sz, interpolation=cv2.INTER_AREA)
                tc = cv2.resize(mGc, sz, interpolation=cv2.INTER_AREA)
                res = cv2.matchTemplate(Wd2, t, cv2.TM_CCORR) + cv2.matchTemplate(Wc2, tc, cv2.TM_CCORR)
                _, mx, _, loc = cv2.minMaxLoc(res)
                if best is None or mx > best[0]:
                    best = (mx, w, h, loc[0] * 2, loc[1] * 2)
        _, w, h, gx, gy = best
        imG2 = co_gian(imG, round(w), round(h))
        bG = [int(gx), int(gy), int(gx) + imG2.shape[1], int(gy) + imG2.shape[0]]
        Image.fromarray(imG2, "RGBA").save(os.path.join(ra, "long.png"))
        info["manh"]["long"] = bG
        Gm = mat_na_tai(imG2, bG[0], bG[1], (Hc, Wc))
        ho = V & ~Tm & ~Gm
        print(f"  vòm tím: {round(w)} x {round(h)} px (gốc {imG.shape[1]} x {imG.shape[0]}), khung {bG}; khe miệng chưa phủ {int(ho.sum())} px; "
              f"vòm lòi khỏi thân {int((Gm & ~T.gian(cho2, 3)).sum())} px")

    # ---- môi chu, lưỡi dài: giữ cỡ gốc, rig tự đặt tỉ lệ
    imM, _ = cat_manh(ap, o["E"][0])
    Image.fromarray(imM, "RGBA").save(os.path.join(ra, "moi.png"))
    imL, _ = cat_manh(ap, o["F"][0])
    Image.fromarray(imL, "RGBA").save(os.path.join(ra, "luoi_dai.png"))

    # ---- dãi (người dùng 2026-11-11: "cho nó chảy dãi, chiêu cuối cũng bắn dãi lung tung"): sợi dãi rủ từ vành gần, giọt văng
    info["dai"] = False
    pS = T.moi_nhat(os.path.join(S.d_inbox(1), "tai_ve"), "S01")
    if pS:
        aS = doc(pS)
        cS = sorted(T.cum(~T.nen_trang(aS, 236), 1500), key=lambda c: c["x0"])
        if len(cS) != 5:
            raise SystemExit(f"tờ dãi {pS}: cần 5 mảnh, thấy {len(cS)}")
        for ten, c, kk in zip(("dai_soi", "dai", "giot_1", "giot_2", "giot_3"), cS, (7, 7, 9, 9, 9)):
            # mảnh dãi vào rig sẽ thu rất nhỏ (0,15–0,25): làm đậm nét mực trước (lọc min cả mảnh), kẻo viền biến mất
            ad = cv2.erode(aS.astype(np.uint8), np.ones((kk, kk), np.uint8)).astype(np.float32)
            imd, _ = cat_manh(ad, T.gian(T.lap_lo(c["m"]), kk // 2))
            Image.fromarray(imd, "RGBA").save(os.path.join(ra, ten + ".png"))
        xq = int(info["mep"]["x"] + 0.38 * (info["mep"]["ix"][1] - info["mep"]["x"]))
        co_v = np.nonzero(cD_top >= 0)[0]
        yq = float(cD_top[co_v[np.argmin(np.abs(co_v - xq))]]) + 0.55 * info["day_vanh"]
        info["dai_goc"] = [xq, yq]                                                     # chỗ sợi dãi bám: giữa dải vành gần, phía đầu miệng
        info["dai"] = True

    # ---- soi: ghép dáng nghỉ từ mảnh, đặt cạnh concept; đo bóng
    cv = np.zeros((Hc, Wc, 4), np.float32)
    for ten in ["long", "luoi_nghi", "mai_duoi"] + (["luoi_mep"] if info["luoi_mep"] else []) + ["mai_tren", "mat_g_mo", "mat_x_mo"]:
        im = np.array(Image.open(os.path.join(ra, ten + ".png")).convert("RGBA"))
        b = info["manh"][ten]
        dan(cv, im, b[0], b[1])
    al = cv[..., 3] > 110
    thieu, thua = int((fgc & ~al).sum()), int((al & ~T.gian(fgc, 2)).sum())
    print(f"  dáng nghỉ ghép từ mảnh: concept có mà ghép trống {thieu} px; ghép thừa ra ngoài concept {thua} px")
    x0, y0, x1, y1 = T.hop(fgc | al, 30)
    nen = np.full((Hc, Wc, 3), GRAY, np.float32)
    ghep = nen * (1 - cv[..., 3:4] / 255.0) + cv[..., :3] * (cv[..., 3:4] / 255.0)
    goc_ = np.where(fgc[..., None], ac, nen)
    Image.fromarray(np.hstack([goc_[y0:y1, x0:x1], ghep[y0:y1, x0:x1]]).astype(np.uint8)).save(os.path.join(ra, "_soi2.png"))
    json.dump(info, open(os.path.join(ra, "manh2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=lambda v: v.item() if hasattr(v, "item") else list(v))
    print(f"dạng {k}: mảnh -> {ra}")
    return info


# ================================================================ rig
def dung(k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    Dat = khung.Dat
    dm = os.path.join(S.d_inbox(k), "manh2")
    mj = json.load(open(os.path.join(dm, "manh2.json"), encoding="utf-8"))
    th = mj["than"]
    ox, oy = (th["x0"] + th["x1"]) / 2.0, float(th["y_day"])

    def R(x, y):
        return ((x - ox) * SC, (oy - y) * SC)

    def tam(box):
        return R((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)

    def nap(path, ti=SC):
        im = Image.open(path).convert("RGBA")
        im = im.resize((max(2, round(im.width * ti)), max(2, round(im.height * ti))), Image.LANCZOS)
        return anh.loang_mau(im)

    Wb, Hb = (th["x1"] - th["x0"]) * SC, (th["y_day"] - th["y_top"]) * SC
    H = (th["y_day"] - th["y_dinh"]) * SC
    Hg = R(*mj["ban_le"])
    mep = mj["mep"]
    dc = mj["day_cung"]
    goc_dc = math.degrees(math.atan2(-dc[1], dc[0]))
    co_mep = bool(mj.get("luoi_mep"))

    sk = khung.Sk(f"{CODE}_{k}")
    cung_ = ["long", "mai_duoi", "mai_tren", "mat_g_mo", "mat_g_nham", "mat_x_mo", "mat_x_nham"]
    mep_rieng = bool(mj.get("luoi_mep_rieng"))
    for n in cung_ + ["luoi_nghi"] + (["luoi_mep"] if co_mep else []):
        sk.anh(n, nap(os.path.join(dm, n + ".png")))
    # lưỡi dài: dài hơn bề ngang thân; bản thứ hai (cùng cỡ, phần gốc trong suốt) vẽ TRƯỚC mai dưới cho khúc đã thò ra ngoài miệng
    L_luoi = DAI_LUOI * Wb
    im_l = thon(Image.open(os.path.join(dm, "luoi_dai.png")).convert("RGBA"), *THON_LUOI)
    ti_l = L_luoi / im_l.width
    co_l = (max(2, round(im_l.width * ti_l)), max(2, round(im_l.height * ti_l * DAY_LUOI)))
    sk.anh("luoi_dai", anh.loang_mau(im_l.resize(co_l, Image.LANCZOS)))
    Lm = (mep["ix"][1] - mj["ban_le"][0]) * SC                                         # bề dài miệng (bản lề → đầu miệng)
    f0 = min(0.7, (1.0 - F_GOC) * Lm / L_luoi + 0.03)                                  # tỉ lệ dọc lưỡi nơi nó vượt qua đầu vành dưới
    a_l = np.array(im_l).astype(np.float32)
    xs = np.arange(a_l.shape[1]) / float(a_l.shape[1])
    a_l[..., 3] *= np.clip((xs - f0) / 0.03, 0, 1)[None, :]
    im_t = Image.fromarray(a_l.astype(np.uint8), "RGBA").resize(sk.images["luoi_dai"].size, Image.LANCZOS)
    sk.anh("luoi_dai_t", anh.loang_mau(im_t))

    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("lac", "move", 0, 2.6 * Hb)
    sk.xuong("than", "lac", 0, 0.48 * Hb, the_gioi=True)
    sk.xuong("mai_duoi", "than", *Hg, the_gioi=True)
    sk.xuong("mai_tren", "than", *Hg, the_gioi=True)
    sk.xuong("long", "mai_duoi", *Hg, goc=goc_dc, the_gioi=True)                        # vòm tím: co nhẹ về bản lề khi ngậm
    cm = [(mj["mat"][0]["tam"][0] + mj["mat"][1]["tam"][0]) / 2.0, (mj["mat"][0]["tam"][1] + mj["mat"][1]["tam"][1]) / 2.0]
    sk.xuong("mat", "mai_tren", *R(*cm), the_gioi=True)                                 # hai mắt (như bone19 của gốc)
    lo = mj["luoi_lo"]
    yl = (lo[1] + lo[3]) / 2.0
    sk.xuong("ln0", "mai_duoi", *R(lo[0], yl), the_gioi=True)
    sk.xuong("ln1", "ln0", *R(lo[0] + 0.55 * (lo[2] - lo[0]), yl), the_gioi=True)
    goc_l = R(mj["ban_le"][0] + F_GOC * (mep["ix"][1] - mj["ban_le"][0]), mj["giua_mep"][1] + 6)
    im = sk.images["luoi_dai"]
    Ll = luoi.luoi_dai(im, N_LUOI, cot_moi_dot=2, mu=True, buoc=max(7.0, im.height / 5.0), ten=f"lưỡi dài {k}")
    dat_l = Dat(goc_l[0], goc_l[1], neo=(0.02, 0.5))
    lu = sk.chuoi("lu", "mai_duoi", dat_l.ra(Ll.khop(N_LUOI), im.width, im.height))
    # xương mieng: giữa khe miệng, phía đầu miệng (chỗ viên ngọc phụt ra; VFX bám vào), trục x chĩa hướng nhổ
    pm = R(mep["x"] + 0.45 * (mep["ix"][1] - mep["x"]), 0.5 * (mep["y0"] + mep["y1"]))
    sk.xuong("mieng", "mai_duoi", pm[0], pm[1], goc=0, dai=40, the_gioi=True)

    # thứ tự vẽ theo con gốc: vòm tối → lưỡi → mặt trước hàm dưới → mai trên → mắt
    sk.slot("long", "long", "long")
    sk.slot("luoi", "ln0", "luoi_nghi")
    sk.slot("luoi_d", lu[0], None)
    sk.slot("mai_duoi", "mai_duoi", "mai_duoi")
    if co_mep:
        sk.slot("luoi_mep", "ln1" if mep_rieng else "ln0", "luoi_mep")
    co_dai = bool(mj.get("dai"))
    if co_dai:
        pd = R(*mj["dai_goc"])
        sk.xuong("dai", "mai_duoi", pd[0], pd[1], goc=0, the_gioi=True)                 # sợi dãi rủ từ vành gần (kéo dài bằng tỉ lệ dọc)
        sk.xuong("giot_n", "mai_duoi", pd[0], pd[1], goc=0, the_gioi=True)              # giọt dãi nhỏ xuống lúc nghỉ
        sk.slot("dai", "dai", "dai")
        sk.slot("giot_n", "giot_n", "giot_n", an=True)
    sk.slot("luoi_t", lu[0], None)
    sk.slot("mai_tren", "mai_tren", "mai_tren")
    sk.slot("mat_g", "mat", "mat_g_mo")
    sk.slot("mat_x", "mat", "mat_x_mo")

    for n in ("long", "mai_duoi", "mai_tren"):
        sk.manh(n, n, Dat(*tam(mj["manh"][n])))
    for n in ("mat_g", "mat_x"):
        sk.manh(n, n + "_mo", Dat(*tam(mj["manh"][n + "_mo"])))
        sk.manh(n, n + "_nham", Dat(*tam(mj["manh"][n + "_nham"])), ten=n + "_nham")
    # lưỡi nằm: lưới nhỏ, gốc bám ln0, nửa ngoài bám ln1; chóp vắt mép (dạng 2) dùng chung lưới và trọng số
    im = sk.images["luoi_nghi"]
    Ln = luoi.luoi_vung(im, buoc_vien=0.02 * H, buoc_trong=0.03 * H, ten=f"lưỡi nằm {k}")
    dat_n = Dat(*tam(mj["manh"]["luoi_nghi"]))
    V = dat_n.ra(Ln.pts, im.width, im.height)
    x0n, x1n = R(lo[0], 0)[0], R(lo[2], 0)[0]
    Wn = []
    for x, y in V:
        u = min(1.0, max(0.0, (x - x0n) / max(1.0, x1n - x0n)))
        w1 = min(1.0, max(0.0, (u - 0.2) / 0.6))
        w1 = w1 * w1 * (3 - 2 * w1)
        Wn.append({"ln0": 1.0} if w1 < 0.004 else ({"ln1": 1.0} if w1 > 0.996 else {"ln0": 1 - w1, "ln1": w1}))
    sk.luoi_gan("luoi", "luoi_nghi", Ln, Wn, dat=dat_n)
    if co_mep and mep_rieng:
        sk.manh("luoi_mep", "luoi_mep", Dat(*tam(mj["manh"]["luoi_mep"])))
    elif co_mep:
        sk.luoi_gan("luoi_mep", "luoi_mep", Ln, Wn, dat=dat_n)
    Wl = trongso.chuoi(Ll.s, Ll.truc[1][-1] / N_LUOI, lu, cha="mai_duoi", cha_hoa=0.0)
    sk.luoi_gan("luoi_d", "luoi_dai", Ll, Wl, dat=dat_l)
    sk.luoi_gan("luoi_t", "luoi_dai_t", Ll, Wl, dat=dat_l)
    sk.luoi_gan("luoi_t", "luoi_dai", Ll, Wl, dat=dat_l)
    if co_dai:
        hA = pd[1]                                                                     # độ cao chỗ bám so với mặt đất
        L_dai = 0.86 * hA                                                               # sợi dãi dài nhất (tỉ lệ dọc 1)
        imd = Image.open(os.path.join(dm, "dai.png")).convert("RGBA")
        wd, hd = max(4, round(0.115 * Wb)), max(6, round(L_dai * DAI_SY0))             # dáng gốc = trạng thái khung 0 của idle
        sk.anh("dai", anh.loang_mau(imd.resize((wd, hd), Image.LANCZOS)))
        sk.manh("dai", "dai", Dat(pd[0], pd[1], neo=(0.5, 0.03)))
        cg = {}
        for n, ti in (("giot_1", 0.11), ("giot_2", 0.085), ("giot_3", 0.066)):
            ig = Image.open(os.path.join(dm, n + ".png")).convert("RGBA")
            wg = max(4, round(ti * Wb))
            sk.anh(n, anh.loang_mau(ig.resize((wg, max(4, round(ig.height * wg / ig.width))), Image.LANCZOS)))
            cg[n] = sk.images[n].size
        sk.manh("giot_n", "giot_2", Dat(pd[0], pd[1], neo=(0.5, 0.25)), ten="giot_n")
        gd = []
        for i in range(N_GIOT):                                                        # giọt dãi văng ở chiêu cuối: con của move (theo cú lao), bay theo quỹ đạo nướng sẵn
            b = sk.xuong(f"gd{i}", "move", 0, 0)
            sk.slot(f"gd{i}", f"gd{i}", f"gd{i}", an=True)
            sk.manh(f"gd{i}", ("giot_1", "giot_2", "giot_3", "giot_2")[i % 4], Dat(0, 0, neo=(0.5, 0.62)), ten=f"gd{i}")
            gd.append(f"gd{i}")
    for ev, mo in (("trung", "đòn đớp / nhát quật đầu chạm đối thủ"), ("quat", "nhát quật lưỡi kế tiếp"), ("phun", "nhổ ngọc trai (VFX bám xương mieng)")):
        sk.su_kien(ev, mo)
    info = {"k": k, "Wb": Wb, "Hb": Hb, "H": H, "lu": lu, "g_cham": mj["g_cham"], "g_khit": mj["g_khit"], "co_mep": co_mep, "dinh": Ln.n + Ll.n,
            "nghi": float(mj.get("nghi_tren", 0.0)), "co_dai": co_dai}
    if co_dai:
        info.update({"hA": hA, "L_dai": L_dai, "gd": gd})
    return sk, info


def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    Clip, rung = hoat.Clip, hoat.rung
    ln, spl = T.ln, T.spl
    Wb, Hb, H, lu = info["Wb"], info["Hb"], info["H"], info["lu"]
    K = Wb / REF_W
    ch = CHAM[k]
    F = 30.0 / ch
    gk = info["g_khit"]
    CU, CD = -0.75 * gk, 0.25 * gk                                                     # dáng khép khít: mai trên sập xuống, mai dưới nhích lên
    nhe = 0.4 if k == 2 else 1.0                                                       # dạng 2: lưỡi nằm có chóp rủ khuất sau vách trước, nhúc nhích ít kẻo chóp ló ra ngoài bát
    hien = [s["name"] for s in sk.slots if s["alpha"] > 0]

    nghi = info["nghi"]                                                                # dáng nghỉ của mai trên so với concept (âm = khép bớt)

    def mai(P, tren, duoi):
        """tren, duoi: góc so với DÁNG NGHỈ (0 = nghỉ). Há: cộng thẳng; khép: nội suy từ dáng nghỉ tới dáng khít CU."""
        tren = nghi + tren if tren >= 0 else CU + (tren - CU) * (nghi - CU) / (0 - CU)
        P.rot("mai_tren", tren)
        P.rot("mai_duoi", duoi)
        rel = tren - duoi
        if rel < 0:                                                                    # ngậm: vòm tím co về bản lề, kẻo lòi ở đầu miệng
            g = min(1.0, -rel / gk)
            P.scale("long", 1 - 0.07 * g, 1 - 0.3 * g)
            P.move("ln0", 0, -0.09 * Hb * g)

    def nham(P):
        P.att["mat_g"] = "mat_g_nham"
        P.att["mat_x"] = "mat_x_nham"

    def luoi_nghi(P, a, b, dai=1.0):
        P.rot("ln0", a * nhe)
        P.rot("ln1", b * nhe)
        if dai != 1.0:
            P.scale("ln0", 1 + (dai - 1) * nhe, 1)

    U_NGOAI = 3.1                                                                      # tới đâu (thang 0..7) lưỡi còn nằm trong miệng

    def luoi_dai(P, t, A, C, co, tre=0.021):
        """lưỡi dài: A(giây) góc gốc, C(giây) độ cuộn (độ, tính cho 8 đốt chuẩn: nhiều xương hơn thì chia đều); khúc xa đi trễ hơn
        (quất như roi) và gợn sóng nhẹ chạy từ gốc ra ngọn cho mềm. co: tỉ lệ cả lưỡi."""
        P.att["luoi_d"] = "luoi_dai"                                                   # cả lưỡi: giữa vòm tím và mặt trước mai dưới
        # lớp trước chỉ vẽ khúc đã ra ngoài miệng (từ chỗ lưỡi vượt đầu vành gần). Lúc lưỡi còn đang thè ra / thu vào (co nhỏ) thì
        # chưa có khúc nào ngoài miệng: tắt lớp trước, kẻo lưỡi "chui qua" vách trước
        P.att["luoi_t"] = "luoi_dai_t" if co > 0.82 else None
        P.att["luoi"] = None
        if info["co_mep"]:
            P.att["luoi_mep"] = None
        truoc = 0.0
        for i, b in enumerate(lu):
            u = i * 7.0 / (len(lu) - 1)                                                # vị trí dọc lưỡi theo thang 8 đốt chuẩn (0..7)
            ti = t - u * tre
            # cuống nằm sâu trong lòng bát: khúc trong miệng (u < U_NGOAI) gần như thẳng theo góc gốc, chạy trong lòng bát ra
            # đầu miệng; độ cuộn dồn cả vào khúc ngoài miệng (tổng độ cuộn ở ngọn vẫn là 7·C)
            ng = max(0.0, u - U_NGOAI) * 7.0 / (7.0 - U_NGOAI)
            w = A(ti) + ng * C(ti) + 0.25 * u * C(ti) * 0.0 + 1.5 * ng * math.sin(2 * math.pi * (2.2 * t * ch - 0.2 * u))
            P.rot(b, w - truoc)
            truoc = w
        P.scale(lu[0], co, co)

    def an_het(P, a):
        for s in hien:
            P.alpha[s] = a

    # ---------------- idle: lắc lư như lật đật (bone2 + bone4 của gốc), vòng giữa nhai nhai, có chớp mắt
    def idle_fn(t, P):
        f = (t * F) % 120
        th = 2 * math.pi * f / 40.0
        P.rot("lac", 3.4 * (math.cos(th) - 1))
        P.rot("than", 7.5 * math.sin(th))
        mai(P, ln(f, [(0, 0), (16, 1.7), (38, 0), (51, 2.6), (55, 0), (59, 4.2), (63, -0.3), (67, 5.6), (71, 0.5), (80, 0), (96, 1.7), (118, 0), (120, 0)]),
            ln(f, [(0, 0), (40, 0), (51, -6.5), (55, -2.8), (59, -6.2), (63, -2.8), (67, -5), (80, 0), (120, 0)]))
        luoi_nghi(P, 3 * math.sin(th + 0.5) - 3 * math.sin(0.5), 6 * math.sin(th - 0.6) + 6 * math.sin(0.6))
        if 100 <= f < 104:
            nham(P)

    # ---------------- appear: rơi xuống như quả bóng (miệng ngậm), bẹp, nảy, há ra đớp hai cái
    def appear_fn(t, P):
        f = t * F
        an_het(P, ln(f, [(0, 0), (2, 1)]))
        P.move("than", 0, 2.6 * Hb * (1 - min(1.0, f / 7.0) ** 2) + K * ln(f, [(0, 0), (8, 0), (11, 34), (14, 0), (16, 8), (18, 0)]))
        P.rot("than", ln(f, [(0, -40), (7, 0), (9, 5), (12, -3), (16, 0)]))
        P.scale("than", ln(f, [(0, .95), (7, .95), (8.5, 1.14), (11, .97), (14, 1.05), (17, 1), (24, 1)]),
                ln(f, [(0, 1.05), (7, 1.05), (8.5, .86), (11, 1.04), (14, .96), (17, 1), (24, 1)]))
        mai(P, ln(f, [(0, CU), (10, CU), (13, 14), (15, CU * .6), (17.5, 12), (19.5, CU * .5), (22, 0), (24, 0)]),
            ln(f, [(0, CD), (10, CD), (13, -6), (15, CD * .6), (17.5, -5), (19.5, CD * .5), (22, 0), (24, 0)]))
        if f < 10:
            nham(P)

    # ---------------- attack: há hai mai thật to rồi đớp mạnh (skill_01 của gốc); cú lao nằm trên move để sân kéo tới đối thủ
    def attack_fn(t, P):
        f = t * F
        P.rot("than", ln(f, [(0, 0), (3, 4.8), (13, 5.5), (15, -1.4), (16, -20), (17, -26), (19, -22), (21, 7.8), (25, 8), (30, 0)]))
        P.move("than", K * ln(f, [(0, 0), (3, -14), (13, -18), (16, 10), (17, 16), (21, -20), (25, -12), (30, 0)]),
               K * ln(f, [(0, 0), (3, 80), (13, 88), (15, 67), (16, 12), (17, 0), (21, 0), (25, 34), (29, 0)]))
        P.move("move", 0.45 * H * ln(f, [(0, 0), (13, 0), (15, .5), (16, 1), (20, 1), (23, .45), (27, 0)]), 0)
        P.scale("than", ln(f, [(0, 1), (3, .96), (13, .95), (16, .98), (17, 1.14), (19, 1.1), (21, .96), (25, 1.02), (30, 1)]),
                ln(f, [(0, 1), (3, 1.04), (13, 1.05), (16, 1.02), (17, .86), (19, .9), (21, 1.04), (25, .98), (30, 1)]))
        mai(P, ln(f, [(0, 0), (3, 43), (13, 56), (15, 44), (16, 60), (17, CU - 2), (19, CU), (21, CU), (25, -3), (28, 3), (32, 0)]),
            ln(f, [(0, 0), (3, -25), (13, -35), (15, -33), (16, -48), (17, CD + 1), (21, CD), (25, -5), (32, 0)]))
        luoi_nghi(P, ln(f, [(0, 0), (3, 4), (13, 6), (16, 8), (17, 0), (32, 0)]), ln(f, [(0, 0), (3, -8), (8, 4), (13, -6), (16, 8), (17, 0), (32, 0)]),
                  ln(f, [(0, 1), (3, 1.08), (15, 1.08), (17, 1), (32, 1)]))
        if 16.5 <= f < 23:
            nham(P)

    # ---------------- cast: lấy hơi, NGẬM miệng, nín hơi (phồng, run, ngả ra sau), môi chu dẩu ra rồi NHỔ viên ngọc qua lỗ môi,
    # giật lùi, mở miệng về dáng (người dùng 2026-11-11: "tưởng tượng ngậm mồm rồi nhổ ra ngọc")
    def cast_fn(t, P):
        f = t * F
        r = rung(t, 11 / F, 18.6 / F)
        # hít hơi (hé miệng) → ngậm chặt → PHỒNG to dần, run, ngả ra sau → bật miệng PHỤT viên ngọc (xẹp, chúi tới) → giật lùi → về
        mai(P, ln(f, [(0, 0), (5, 12), (8, CU - 1), (9.5, CU), (18.6, CU), (19.6, 20), (21, 26), (25, 11), (30, -2), (34, 1), (40, 0)]),
            ln(f, [(0, 0), (5, -6), (8, CD + 1), (9.5, CD), (18.6, CD), (19.6, -9), (21, -11), (25, -4), (30, 1), (40, 0)]))
        P.rot("than", ln(f, [(0, 0), (5, 4), (9.5, 6), (17, 12), (18.6, 14), (19.6, -12), (21.5, 9), (25, 5), (31, 0)]))
        P.scale("than", ln(f, [(0, 1), (5, .97), (9.5, 1.03), (14, 1.13), (17.5, 1.21), (18.6, 1.24), (19.6, .9), (21.5, 1.05), (26, 1), (40, 1)]) * (1 + 0.012 * r),
                ln(f, [(0, 1), (5, 1.04), (9.5, 1.02), (14, 1.10), (17.5, 1.17), (18.6, 1.2), (19.6, 1.02), (21.5, .96), (26, 1), (40, 1)]) * (1 - 0.012 * r))
        P.move("than", K * (ln(f, [(0, 0), (9.5, -5), (17.5, -16), (19.6, 14), (21.5, -28), (26, -9), (33, 0)]) + 1.5 * r),
               K * ln(f, [(0, 0), (9.5, 0), (17.5, 8), (19.6, 0), (21.5, 10), (24, 0), (40, 0)]))
        if 8.5 <= f < 19.3:
            nham(P)

    # ---------------- skill: há miệng, thè lưỡi dài, lao tới, quật ba phát (skill_02 của gốc), thu lưỡi, lùi về.
    # Lưỡi chỉ vung trong khoảng miệng mở (lên tối đa ~50°, mai trên há theo), không vắt ra sau lưng mai trên.
    def kf(keys):
        return lambda tt: spl(tt * F, keys)

    # góc gốc không xuống dưới ~-5° (lưỡi luôn đi trong lòng bát ra đầu miệng); cú quật xuống là do khúc ngoài miệng cuộn xuống
    # góc gốc thấp nhất ~+9°: đường từ cuống (sâu, dưới mép vành giữa) tới ngay TRÊN đầu vành phía trước; thấp hơn thì lưỡi chui qua vách bát
    A_ = kf([(3, 12), (7, 28), (9, 46), (11, 9), (13, 12), (15, 40), (18, 9), (20, 12), (23, 48), (26, 8), (29, 11), (33, 11), (36, 10)])
    C_ = kf([(3, 2), (7, 5), (9, 8), (11, -13), (13, -6), (15, 7), (18, -12), (20, -5), (23, 9), (26, -15), (29, -7), (33, -1), (36, 0)])

    def skill_fn(t, P):
        f = t * F
        P.move("move", 0.5 * H * ln(f, [(0, 0), (4, 0), (9, 1), (31, 1), (38, 0)]), 0)
        P.move("than", 0, K * ln(f, [(0, 0), (4, 0), (6.5, 42), (9, 0), (23, 0), (25, 20), (26, 0), (31, 0), (34.5, 30), (38, 0)]))
        P.rot("than", ln(f, [(0, 0), (4, 8), (9, 14), (11, -12), (13, -4), (15, 10), (18, -10), (20, -3), (23, 16), (26, -22), (29, -8), (35, 0)]))
        P.scale("than", ln(f, [(0, 1), (25, 1), (26, 1.1), (28, 1.06), (31, 1), (44, 1)]), ln(f, [(0, 1), (25, 1), (26, .9), (28, .95), (31, 1), (44, 1)]))
        mai(P, ln(f, [(0, 0), (4, 42), (9, 56), (11, 30), (15, 52), (18, 30), (23, 60), (26, 26), (30, 30), (35, 6), (38, 0)]),
            ln(f, [(0, 0), (4, -8), (11, -14), (15, -6), (18, -14), (23, -5), (26, -18), (30, -8), (36, 0)]))
        if 3 <= f < 36:
            luoi_dai(P, t, A_, C_, ln(f, [(3, .22), (7, 1), (31, 1), (36, .22)]))
        if 25.5 <= f < 29:
            nham(P)

    # ---------------- hit: bị đánh lăn ngửa ra sau, mắt nhắm, miệng bật ra rồi về (hit_01 của gốc, lùi 1 khung)
    def hit_fn(t, P):
        f = t * F
        P.rot("than", ln(f, [(0, 0), (1, 34), (4, 46), (6, 36), (9, 10), (12, -3), (16, 0)]))
        P.move("than", K * ln(f, [(0, 0), (1, -58), (3, -22), (5, -44), (7, -50), (10, -28), (13, -10), (16, 0)]),
               K * ln(f, [(0, 0), (4, 20), (8, 0), (11, 9), (14, 0), (16, 0)]))
        P.scale("than", ln(f, [(0, 1), (1, .9), (4, 1.04), (8, 1), (16, 1)]), ln(f, [(0, 1), (1, 1.1), (4, .96), (8, 1), (16, 1)]))
        mai(P, ln(f, [(0, 0), (1, CU), (5, CU * .8), (7, 10), (10, 34), (13, 8), (16, 0)]), ln(f, [(0, 0), (1, CD), (5, CD), (10, -10), (16, 0)]))
        luoi_nghi(P, ln(f, [(0, 0), (7, 10), (10, 16), (13, -6), (16, 0)]), ln(f, [(0, 0), (7, -10), (10, 20), (13, -8), (16, 0)]))
        if 0.5 <= f < 10.5:
            nham(P)

    # ---------------- die: bị hất tung ra sau, rơi xuống mai bật mở, lưỡi thè dài nằm vật, rồi tan (die_01 của gốc)
    A_d = kf([(13, 30), (16, 9), (19, 13), (23, 9), (46, 10)])
    C_d = kf([(13, 8), (16, -16), (19, -9), (23, -13), (46, -12)])

    def die_fn(t, P):
        f = t * F
        P.rot("than", ln(f, [(0, 0), (2, 17), (6, 44), (9, 56), (11, 40), (13, 6), (15, -24), (17, -20), (25, -19), (46, -19)]))
        P.move("than", K * ln(f, [(0, 0), (2, -20), (6, -70), (9, -120), (13, -104), (17, -100), (46, -100)]),
               K * ln(f, [(0, 0), (2, 110), (6, 140), (9, 70), (12, 0), (14, 18), (17, 0), (46, 0)]))
        P.scale("than", ln(f, [(0, 1), (11, 1), (12.5, 1.12), (15, .97), (18, 1), (46, 1)]), ln(f, [(0, 1), (11, 1), (12.5, .88), (15, 1.03), (18, 1), (46, 1)]))
        mai(P, ln(f, [(0, 0), (2, CU), (9, CU), (11, 20), (13, 84), (15, 44), (18, 58), (22, 34), (26, 40), (46, 38)]),
            ln(f, [(0, 0), (2, CD), (9, CD), (13, -14), (17, -6), (46, -6)]))
        if f >= 13:
            luoi_dai(P, t, A_d, C_d, ln(f, [(13, .25), (17, .78), (46, .78)]))
        nham(P)
        if f > 33:
            a = ln(f, [(33, 1), (45, 0), (46, 0)])
            an_het(P, a)
            P.alpha["luoi_d"] = a
            P.alpha["luoi_t"] = a

    # ---------------- dãi
    def kep(x):
        return max(0.0, min(1.0, x))

    def boc(fn, kieu, n):
        """bọc một clip: thêm sợi dãi. kieu: idle (chảy, nhỏ giọt theo vòng), vao (appear: cuối clip mới hiện), ra (die: tắt),
        giua (clip khác: tắt ở đầu, hiện lại ở cuối cho khớp khung 0 idle). Sợi dãi luôn rủ thẳng xuống (bù góc xoay của hàm)."""
        if not info["co_dai"]:
            return fn
        hA, Ld = info["hA"], info["L_dai"]

        def g(t, P):
            fn(t, P)
            f = t * F
            bu = -sum(P.t.get(b, (0, 0, 0))[2] for b in ("lac", "than", "mai_duoi"))
            P.rot("dai", bu)
            if kieu == "idle":
                ph = (f % 120) / 120.0
                pc = 100 * ((ph + DAI_PHA0) % 1.0)
                P.scale("dai", ln(pc, DAI_SX) / DAI_SX0, ln(pc, DAI_SY) / DAI_SY0)
                P.rot("dai", 5 * (math.sin(2 * math.pi * f / 40.0 - 1.0) - math.sin(-1.0)))                # đung đưa trễ theo nhịp lắc
                if pc >= 63:                                                           # giọt đứt ra, rơi, chạm đất thì bẹp rồi tan
                    tau = (pc - 63) / 100.0 * 120.0 / F
                    roi = Ld * 1.02 + 0.5 * 9.0 * Hb * tau * tau
                    day_ = hA - 4
                    if roi < day_:
                        P.move("giot_n", 0, -roi)
                        P.rot("giot_n", bu)
                        P.alpha["giot_n"] = 1.0
                        sq = 1 + min(0.25, 0.9 * tau)
                        P.scale("giot_n", 1 / sq, sq)
                    else:
                        tb = tau - math.sqrt(max(0.0, (day_ - Ld * 1.02) / (4.5 * Hb)))
                        a = kep(1 - tb / 0.12)
                        if a > 0:
                            P.move("giot_n", 0, -day_)
                            P.rot("giot_n", bu)
                            P.alpha["giot_n"] = a
                            P.scale("giot_n", 1.5 + 2 * tb, max(0.25, 0.5 - 2 * tb))
            else:
                e = {"vao": kep((f - (n - 5)) / 4.0), "ra": kep(1 - f / 3.0)}.get(kieu, max(kep(1 - f / 3.0), kep((f - (n - 4)) / 4.0)))
                P.scale("dai", 1, max(0.04, e))
                P.alpha["dai"] = e * P.alpha.get("dai", 1.0)
        return g

    # giọt dãi văng ở chiêu cuối: phát ở đầu lưỡi theo từng cú vung / quật, vận tốc lấy từ chính chuyển động đầu lưỡi (đã trừ cú lao
    # trên xương move), toả rộng, rơi theo trọng lực; slot dùng lại khi giọt trước đã tan
    skill_goc = skill_fn
    if info["co_dai"]:
        rng = np.random.default_rng(11 + k)
        DOI = 0.40 * ch

        def dau_luoi(t):
            P = khung.Pose()
            skill_goc(t, P)
            W = sk.the_gioi(P)
            mv = P.t.get("move", (0.0, 0.0))
            M = W[lu[-1]]
            return np.array([M[0, 2] - mv[0], M[1, 2] - mv[1]])

        phat = []                                                                      # (giây phát, p0, v0, cỡ, slot)
        ban = [0.0] * len(info["gd"])
        for fe, so in ((6.5, 1), (8.4, 3), (9.6, 3), (11, 5), (12, 3), (13.5, 2), (15, 3), (16.2, 2), (18, 5), (19, 3), (20.5, 2), (22.5, 3), (23.6, 3), (26, 6), (27, 4), (29, 2), (31, 1)):
            te = fe / F
            p0 = dau_luoi(te)
            v = (p0 - dau_luoi(te - 1 / 60.0)) * 60.0
            sp = float(np.hypot(*v))
            huong = math.atan2(v[1], v[0]) if sp > 1 else 0.5
            for _ in range(so):
                i = next((j for j in range(len(ban)) if ban[j] <= te), None)
                if i is None:
                    break
                goc = huong + math.radians(rng.uniform(-65, 65))
                nhanh = min(3.0 * H, max(1.1 * H, sp * rng.uniform(0.25, 0.5))) * rng.uniform(0.75, 1.15)
                te_i = te + rng.uniform(0, 0.07)                                         # lệch giờ và lệch chỗ phát, kẻo cả chùm chụm thành bông hoa
                phat.append((te_i, p0 + rng.uniform(-0.07, 0.07, 2) * H, np.array([math.cos(goc) * nhanh, math.sin(goc) * nhanh + 0.5 * H]), rng.uniform(0.85, 1.45), i))
                ban[i] = te_i + DOI + 0.02
        G_ROI = 6.5 * H

        def skill_fn(t, P):                                                            # noqa: F811
            skill_goc(t, P)
            for te, p0, v0, co_g, i in phat:
                tau = t - te
                if 0 <= tau < DOI:
                    b = info["gd"][i]
                    x = p0[0] + v0[0] * tau
                    y = p0[1] + v0[1] * tau - 0.5 * G_ROI * tau * tau
                    P.move(b, x, max(2.0, y))
                    P.rot(b, math.degrees(math.atan2(v0[1] - G_ROI * tau, v0[0])) + 90.0)   # bụng giọt đi trước, đuôi kéo theo
                    gi = 1 + min(0.5, 1.6 * tau)
                    P.scale(b, co_g / math.sqrt(gi), co_g * gi)
                    P.alpha[b] = kep((DOI - tau) / 0.1) if y > 2.0 else kep((DOI - tau) / 0.1) * 0.8

    appear_fn, idle_fn, attack_fn, cast_fn, skill_fn, hit_fn, die_fn = (boc(appear_fn, "vao", 24), boc(idle_fn, "idle", 120), boc(attack_fn, "giua", 32),
                                                                        boc(cast_fn, "giua", 40), boc(skill_fn, "giua", 44), boc(hit_fn, "giua", 16),
                                                                        boc(die_fn, "ra", 46))
    return [Clip("appear", 24 / F, appear_fn),
            Clip("idle", 120 / F, idle_fn, loop=True),
            Clip("attack", 32 / F, attack_fn, ev=[(17 / F, "trung", "")]),
            Clip("cast", 40 / F, cast_fn, ev=[(19.6 / F, "phun", "")]),
            Clip("skill", 44 / F, skill_fn, ev=[(11 / F, "trung", ""), (18 / F, "quat", ""), (26 / F, "quat", "")], trung=11 / F),
            Clip("hit", 16 / F, hit_fn),
            Clip("die", 46 / F, die_fn)]


def rig(k, tien_hoa=None):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    for c in cl:
        w, at = S.lo_kin(sk, fr[c.ten])
        print(f"  lỗ kín {c.ten}: lớn nhất {w:.0f} px2" + (f" (khung {at})" if w > 0 else ""))
    ra = os.path.join(S.d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    ten = f"{CODE}_{k}"
    noi = {}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        ve1, ve2 = soi.Ve(sk), soi.Ve(sk2)
        ti = soi.chieu_cao(ve1, fr["idle"][0]) / soi.chieu_cao(ve2, fr2["idle"][0])
        M = tienhoa.gop(sk, sk2)

        def gong(t, P):                                                       # dạng cũ ngậm chặt, mắt nhắm, rung, phồng dần
            g = hoat.cv(t, [(0, 0), (0.3, 1, "out"), (1.3, 1)])
            P.rot("mai_tren", info["nghi"] + (-0.75 * info["g_khit"] - info["nghi"]) * g)
            P.rot("mai_duoi", 0.25 * info["g_khit"] * g)
            P.scale("long", 1 - 0.07 * g, 1 - 0.3 * g)
            P.move("ln0", 0, -0.09 * info["Hb"] * g)
            s = hoat.cv(t, [(0, 1), (0.3, 0.94), (0.6, 1.08, "out"), (1.3, 1.3)])
            r = hoat.rung(t, 0.45, 1.3)
            P.scale("than", s * (1 + 0.02 * r), s * (1 - 0.02 * r))
            if t > 0.2:
                P.att["mat_g"] = "mat_g_nham"
                P.att["mat_x"] = "mat_x_nham"

        def bung(t, P, fl):                                                   # dạng sau hiện ra, há thật to rồi đớp một cái
            o = hoat.cv(t, [(0, 0), (1.5, 0), (1.85, 1, "out"), (2.05, 1), (2.15, -0.35, "in"), (2.35, 0.15, "io"), (2.5, 0, "io"), (2.8, 0)])
            P.rot("n_mai_tren", info2["nghi"] + 46 * o)
            P.rot("n_mai_duoi", -16 * o)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=bung)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
    tk = xuat.xuat_het(M, clM, ra, ten, f"Sò đột biến dạng {k}", frames=frM, dang=k, so_dang=2, dung_yen=("cast",), lao=("skill",),
                       khop_idle=0, noi_them=noi, tol={"rotate": 0.08, "translate": 0.15, "scale": 0.001},
                       can=[("can_dop", "attack", 17 / 30.0 * CHAM[k], "than", 0.7 * info["H"]),
                            ("can_ha", "attack", 13 / 30.0 * CHAM[k], "than", 0.8 * info["H"]),
                            ("can_phong", "cast", 18.4 / 30.0 * CHAM[k], "than", 0.8 * info["H"]),
                            ("can_phut", "cast", 20.2 / 30.0 * CHAM[k], "than", 0.8 * info["H"])])
    S.gif_nho(sk, fr["cast"], info, k, os.path.join(ra, "xem_nho_ngoc.gif"))
    print(f"dạng {k}: góc chạm {info['g_cham']:.0f}°, góc khép khít {info['g_khit']:.0f}°; {info['dinh']} đỉnh lưỡi; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg[:1] == ["cat"]:
        for k in ([int(arg[1])] if len(arg) > 1 else [1, 2]):
            cat(k)
    elif arg[:1] == ["rig"]:
        rig(int(arg[1]))
    elif arg[:1] == ["all"]:
        r2 = rig(2)
        rig(1, tien_hoa=r2)
    else:
        print(__doc__)
