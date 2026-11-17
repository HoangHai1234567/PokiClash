# -*- coding: utf-8 -*-
"""Tatu mai đá (cong_da; tướng 1 đảo Thổ, ải 1): hình của mình chạy trên ĐÚNG rig của con gốc monster_3378 (game tham khảo). Ghi chú:
inbox/tho5_ghichu.md. Cách làm như quang_sat_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ, thêm `move` (cú lao), `day` (đáy thân: nhún, nhảy), `tam` (tâm thân: nghiêng, lật; cha của `all`).
- MẢNH: ảnh "đúng chỗ, đúng cỡ" (cong_da_manh.py → inbox/cong_da_1/manh/), đặt vào thế giới rig ở dáng idle 0 theo chỗ trên concept;
  mỗi đỉnh biến dạng như điểm tương ứng trên lưới của họ (gan_goc). Mảnh thêm: `tinh_the` (cụm pha lê, bám như mai `hair3`). Không có trên
  concept: `hair5` (dùng ảnh sỏi nhỏ hair1), `footr2` (dùng ảnh chân footl1, tối hơn) đặt ở chỗ part gốc. Sỏi phải `hair4` vẽ TRƯỚC mai
  (concept: sỏi bám mép mai), còn lại giữ thứ tự vẽ của họ.
- CHUYỂN ĐỘNG (đề xuất tho5_anim.py, người dùng "làm đi" 2026-11-17):
    appear = chỉ có cái mai rơi phịch, nảy một lần → chân, đuôi, mặt bật ra, rũ mình, cau mày;
    idle   = idle_01 + hít hít mõm rồi hắt xì (sự kiện hat_xi cho phụt bụi);
    walk   = run_01; hit = hit_01; die = die_01 + lật ngửa + mờ;
    attack = skill_01_1 (lấy đà, lao húc, sỏi văng tới rồi về), quãng tới dồn vào `move`;
    cast   = skill_02 (nhún, bật lên) + LẮC MAI ở đỉnh nhảy (sự kiện ban: VFX chùm sỏi bay tới đối thủ), đáp phịch;
    skill  = rụt vào mai, mai rung lạch cạch (gồng) → cụm pha lê bung (sự kiện ban_troi: VFX pha lê bắn lên trời) → đứng dậy chĩa mõm,
             sự kiện mua (mưa pha lê rơi xuống đối thủ), trung (mảnh to nhất cắm xuống).
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/cong_da_rig.py        → inbox/cong_da_1/rig/
    py -3 -I ArtGen/Spine/cong_da_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]    → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/cong_da_rig.py kiem                                               (đo góc nhảy, bước dời)
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, khung, hoat, xuat, soi, luoi, trongso  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import tho5  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = tho5.dat("cong_da")
TEN_RIG = "cong_da_1"
D_PX = float(os.environ.get("CD_DPX", "1.2"))          # pixel ảnh atlas cho mỗi đơn vị rig
MANH = os.path.join(G.BASE, "manh")
RA = os.environ.get("CD_RA") or os.path.join(G.BASE, "rig")
TAN = 0.45
FPS = 30.0
IMPACT = {"attack": (0.06, 0.35, 0.08), "cast": (0.06, 0.40, 0.08), "skill": (0.14, 0.70, 0.18, "#ffffff40")}   # ải 1: gọn

# thứ tự vẽ (sau → trước). Concept: lưng < mai < tai < MẶT; nên thân có HAI lớp cùng lưới: `body` (thân tròn đủ, sau mai) và
# `body_truoc` (chỉ phần thân lộ ra trên concept, có viền đỉnh đầu chạy trước chân tai; cắt ở y concept 790, mờ dần 30 px) vẽ sau tai.
# Chân giữa `footl1` lùi ra SAU THÂN (họ vẽ trước khối pha lê): concept cho chân chui ra từ dưới bụng, đùi GPT vẽ trọn phải khuất.
SLOT_HO = ["tail", "footr2", "footl2", "hair5", "footr1", "footl1", "body", "hair3", "tinh_the", "hair4", "hair2", "hair1", "mmr", "mml",
           "body_truoc", "mt1", "eyes", "yq1", "yp1", "yp2"]
HINH = {s: [s] for s in SLOT_HO}
HINH["hair3"] = ["hair3", "hair3_tron"]                 # mai khoét chỗ thân lộ ra / mai nguyên vẹn (appear: lúc rơi, thân còn ẩn)
GAN_THEO = {"tinh_the": "hair3", "body_truoc": "body"}  # slot thêm → bám như lưới của slot này
CAT_TRUOC = (690.0, 722.0)                              # body_truoc + chỗ khoét mai: chỉ vùng đầu, x concept > 690 (mờ dần tới 722)
THAY = {"hair5": ("hair1", 0.85, 1.0), "footr2": ("footl1", 0.95, 0.80)}   # slot không có trên concept: (ảnh mượn, tỉ lệ, độ sáng)
SOI = ("hair2", "hair1", "hair4", "hair5")              # sỏi
MAT = ("eyes", "yq1", "yp1", "yp2", "mt1")
TAI = ("mml", "mmr")
CHAN = ("footl1", "footl2", "footr1", "footr2")


# ---------------------------------------------------------------- nạp
def nap():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(scan, "sample_goc.json"), encoding="utf-8"))
    return D, D0, I, S


def mats(Dj):
    return {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in Dj["bones"]}


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    W, H = 1536, 1024
    to_rig = lambda P: np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    to_px = lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
    return s, to_rig, to_px


_D0 = {}


def anh_manh(ten):
    """ảnh mảnh của mình đã thu về D_PX px / đơn vị + hộp (px concept) + hệ số thu. Slot không có trên concept (THAY): mượn ảnh khác,
    đặt tâm ở tâm part gốc khung 0 idle."""
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    s_px, _, to_px = tf()
    if ten in THAY and ten not in DATJ:
        nguon, ti, sang = THAY[ten]
        g = Image.open(os.path.join(MANH, nguon + ".png")).convert("RGBA")
        g = g.resize((max(2, round(g.width * ti)), max(2, round(g.height * ti))), Image.LANCZOS)
        if sang != 1.0:
            a = g.getchannel("A")
            g = ImageEnhance.Brightness(g.convert("RGB")).enhance(sang).convert("RGBA")
            g.putalpha(a)
        a0 = _D0[ten]
        c = to_px(np.array(a0["xy"], float).reshape(-1, 2)).mean(0)
        hop = [c[0] - g.width / 2, c[1] - g.height / 2, c[0] + g.width / 2, c[1] + g.height / 2]
    elif ten == "hair3_tron":
        g = Image.open(os.path.join(MANH, "hair3.png")).convert("RGBA")
        hop = DATJ["hair3"]["hop"]
    elif ten in ("body", "body_truoc", "hair3") and "body_truoc" in DATJ:
        g, hop = lop_than(ten, DATJ)
    else:
        g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
        hop = DATJ[ten]["hop"]
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), hop, kq


def _toan(ten, DATJ):
    """ảnh mảnh đặt lên khung concept 1536 × 1024 (mảng float RGBA 0..1)."""
    C = np.zeros((1024, 1536, 4), np.float32)
    g = np.asarray(Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA"), np.float32) / 255.0
    x0, y0 = int(DATJ[ten]["hop"][0]), int(DATJ[ten]["hop"][1])
    C[y0:y0 + g.shape[0], x0:x0 + g.shape[1]] = g[:1024 - y0, :1536 - x0]
    return C


def _cat_hop(C):
    al = C[..., 3] > 0.004
    ys, xs = np.nonzero(al)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    return Image.fromarray((np.clip(C[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8), "RGBA"), [float(x0), float(y0), float(x1), float(y1)]


def lop_than(ten, DATJ):
    """ba lớp quanh mặt (concept: lưng < mai < tai < mặt), dựng sao cho KHÔNG có vệt nối:
    - hair3 (mai): khoét vùng thân LỘ RA trên concept (M5, co 3 px để mai lót dưới viền của M5): ở đó mai vốn nằm sau thân;
    - body (thân tròn đủ, sau mai): M1, riêng vùng M5 (trên y 815) lấy đúng điểm ảnh của M5 → trùng từng điểm với lớp trước;
    - body_truoc (sau tai): M5 mờ dần ở bụng dưới (CAT_TRUOC), đè lên đúng các điểm ảnh y hệt của body."""
    import cv2
    M5 = _toan("body_truoc", DATJ)
    x = np.arange(1536, dtype=np.float32)[None, :]
    fx = np.broadcast_to(np.clip((x - CAT_TRUOC[0]) / (CAT_TRUOC[1] - CAT_TRUOC[0]), 0.0, 1.0), (1024, 1536))
    if ten == "hair3":                              # khoét mai ở MỌI chỗ thân lộ ra (GPT vẽ trọn mai xuống tới bụng)
        C = _toan("hair3", DATJ)
        m = cv2.erode((M5[..., 3] > 0.5).astype(np.uint8), np.ones((7, 7), np.uint8)).astype(np.float32)
        C[..., 3] *= 1.0 - m
        return _cat_hop(C)
    if ten == "body_truoc":
        C = M5.copy()
        C[..., 3] *= fx
        return _cat_hop(C)
    a5 = M5[..., 3:4]
    C = _toan("body", DATJ)
    # thân tròn đủ (M1) chỉ giữ ở chỗ nằm DƯỚI MAI (mai vẽ trọn, co 4 px) hoặc trong M5: phần M1 thò ra ngoài M5 ở bụng, mạn trái tạo
    # viền đôi + dải hở (người dùng: "đầu ghép bị lỗi, hở 1 chút ở dưới")
    mai = cv2.erode((_toan("hair3", DATJ)[..., 3] > 0.5).astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    C[..., 3] *= ((M5[..., 3] > 0.02) | mai).astype(np.float32)
    rgb = C[..., :3] * (1 - a5) + M5[..., :3] * a5
    al = np.maximum(C[..., 3:4], a5)
    return _cat_hop(np.concatenate([rgb, al], 2))


def trong_so_goc(V, a0, ten, Wi):
    """mỗi điểm V (thế giới idle 0) biến dạng như điểm tương ứng trên lưới của họ a0 (xem quang_sat_rig.trong_so_goc)."""
    Q = np.array(a0["xy"], float).reshape(-1, 2)
    tr = np.array(a0["tris"]).reshape(-1, 3)
    Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in a0["w"]]
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)

    def gan_canh(p, a, b):
        d = b - a
        t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T), t

    rows = []
    for p in V:
        v2 = p - A
        b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
        b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
        lech = np.zeros(2)
        if len(ok):
            i = int(ok[0])
            be = (float(b0[i]), float(b1[i]), float(b2[i]))
        else:
            best = None
            for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                dist, t = gan_canh(p, pa, pb)
                j = int(np.argmin(dist))
                if best is None or dist[j] < best[0]:
                    w3 = [0.0, 0.0, 0.0]
                    w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                    best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
            _, i, be, c = best
            lech = p - c
        acc = {}
        for vi, bw in zip(tr[i], be):
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Q[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5:
                continue
            g = q / w + lech
            lp = np.linalg.solve(Wi[n], np.array([g[0], g[1], 1.0]))
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    return rows


MEP_MAI = 70.0                                         # px concept: mép mai trong khoảng này quanh thân lộ ra biến dạng theo lưới thân


def _kc_than():
    """khoảng cách (px concept) tới vùng thân lộ ra (M5)."""
    import cv2
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    m = (_toan("body_truoc", DATJ)[..., 3] > 0.5).astype(np.uint8)
    return cv2.distanceTransform(1 - m, cv2.DIST_L2, 5)


def gan_manh(sk, slot, ten_anh, a0, ten, Wi, a_than=None, xuong=None):
    """mảnh của mình thành lưới đặt đúng chỗ concept ở dáng idle 0; mảnh to / nhiều xương: lưới phủ hình + gan_goc; nhỏ: ô 4 đỉnh.
    a_than (chỉ cho mai): mép mai sát thân lộ ra hoà dần sang biến dạng của lưới thân (mai bám xương đầu, thân bám nhiều xương: đầu xoay
    thì mép mai trượt khỏi thân, lộ viền)."""
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig, _ = tf()
    ws = {k for v in a0.get("w") or [] for k, _ in v}
    nhieu = len(ws) > 1
    if xuong is not None:                                # mảnh cứng trên xương riêng của mình (cụm pha lê)
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
        V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))
        inv = np.linalg.inv(sk.W0[xuong])
        rows = [[(xuong, *[float(q) for q in (inv @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=V)
        sk.atts[slot][ten_anh]["verts"] = rows
        return L
    if a_than is not None:
        L = luoi.luoi_vung(im, buoc_vien=10.0, buoc_trong=16.0, vien=2, ten=slot, in_tk=False)
        Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
        V = to_rig(Px)
        b = ten[next(iter(ws))]
        r_cung = [[(b, *[float(v) for v in np.linalg.solve(Wi[b], np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        r_than = trong_so_goc(V, a_than, ten, Wi)
        D = _kc_than()
        rows = []
        for p, rc, rt in zip(Px, r_cung, r_than):
            d = float(D[int(np.clip(p[1], 0, 1023)), int(np.clip(p[0], 0, 1535))])
            w = float(np.clip(1.0 - d / MEP_MAI, 0.0, 1.0)) ** 1.5
            gop = {}
            for (n, x, y, ww), k in [(e, 1 - w) for e in rc] + [(e, w) for e in rt]:
                if ww * k < 1e-5:
                    continue
                g = gop.setdefault(n, [0.0, 0.0, 0.0])
                g[0] += ww * k * x
                g[1] += ww * k * y
                g[2] += ww * k
            rows.append([(n, g[0] / g[2], g[1] / g[2], g[2]) for n, g in gop.items()])
        Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
        sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
        sk.atts[slot][ten_anh]["verts"] = rows
        return L
    if nhieu:
        L = luoi.luoi_vung(im, buoc_vien=10.0, buoc_trong=16.0, vien=2, ten=slot, in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(Px)
    if nhieu:
        rows = trong_so_goc(V, a0, ten, Wi)
    else:
        b = ten[next(iter(ws))] if ws else (ten[a0["bone"]] if isinstance(a0["bone"], int) else a0["bone"])
        rows = [[(b, *[float(v) for v in np.linalg.solve(Wi[b], np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    _D0.update(by0)
    _, to_rig, _ = tf()
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    hb = DATJ["body"]["hop"]
    Vb = to_rig(np.array([[hb[0], hb[1]], [hb[2], hb[3]]], float))
    y_day = float(min(Vb[:, 1]))
    tam = np.array([float(Vb[:, 0].mean()), float(Vb[:, 1].mean())])
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("day", "move", float(tam[0]), y_day)
    sk.xuong("tam", "day", 0.0, float(tam[1] - y_day))
    goc0 = {}
    for b in IB:
        if b["name"] in ("root", "shadow"):
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[b["name"]] = g
        if cha == "root":
            sk.xuong(b["name"], "tam", g[0] - float(tam[0]), g[1] - float(tam[1]), goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        else:
            sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    # xương cụm pha lê: con của `hair` (mai) ở chân cụm trên concept, trục x chĩa LÊN thế giới (vọt lên trời ở chiêu cuối rồi mọc lại)
    hp = DATJ["tinh_the"]["hop"]
    goc_pl = to_rig(np.array([[(hp[0] + hp[2]) / 2.0, hp[3] - 30.0]]))[0]
    sk.xuong("pha_le", "hair", float(goc_pl[0]), float(goc_pl[1]), goc=90.0, the_gioi=True)
    tong = [0, 0]
    for s in SLOT_HO:
        if s not in DATJ and s not in THAY:
            print(f"  (thiếu mảnh) bỏ slot {s}")
            continue
        sk.slot(s, "move", HINH[s][0])
        for h in HINH[s]:
            L = gan_manh(sk, s, h, by0[GAN_THEO.get(s, s)], ten, Wi, a_than=by0["body"] if s == "hair3" else None,
                         xuong="pha_le" if s == "tinh_the" else None)
            tong[0] += L.n
            tong[1] += len(L.tris)
    # xương mõm (điểm phát hắt xì / VFX): con của head ở chóp mõm trên concept
    _, to_rig, _ = tf()
    mui = to_rig(np.array([[1112.0, 735.0]]))[0]
    sk.xuong("mieng", "head", float(mui[0]), float(mui[1]), the_gioi=True)
    for e, m in (("trung", "khung trúng"), ("cham_dat", "chạm đất (appear, cast, skill)"), ("phong", "cast: một viên sỏi rời mai bay tới đối thủ (chuỗi = a / b / c)"),
                 ("ve", "cast: viên sỏi bay về lắp lại mai"),
                 ("ran", "cast: lắc mai, sỏi rung lạch cạch (VFX bụi)"), ("gong", "skill: rụt mai gồng, mai rung (VFX sỏi nảy)"),
                 ("ban_troi", "skill: cụm pha lê vọt lên trời (rig), VFX vệt"),
                 ("moc", "skill: cụm pha lê mọc lại trong hốc mai"), ("mua", "skill: mưa pha lê rơi xuống đối thủ (VFX)"),
                 ("bung", "appear: chân, mặt bật ra khỏi mai")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy thân y = {y_day:.1f}, tâm thân "
          f"({tam[0]:.1f}, {tam[1]:.1f})")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, S=S, Wi=Wi)


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        L = np.array([F["l"] for F in fr], float)
        res = {}
        for i, n in enumerate(ten):
            if n not in goc0:
                continue
            g = goc0[n]
            A = np.stack([L[:, i, 2] - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[n] = A
        out[clip] = (float(v["dur"]), res, len(fr))
    return out


# ---------------------------------------------------------------- mốc giờ
T_HUC = 0.40                                            # attack: đỉnh lao (skill_01_1 của họ: hông xa nhất ở 0,40)
LAO = 0.50                                              # quãng lao (× chiều cao) ở khung húc
D_ATTACK = 0.93
T_NHAY, T_DAP_C = 0.47, 0.66                            # cast: đỉnh nhảy, đáp (skill_02)
T_LAC0, T_LAC1 = 0.28, 0.56                             # cast: lắc mai
BAY_MANH = {"a": ("hair2", "hair3"), "b": ("hair1", "hair2"), "c": ("hair4", "hair4")}   # sỏi bay: khoá → (slot = ảnh, xương)
T_PHONG = {"a": 0.46, "b": 0.52, "c": 0.58}            # sỏi rời mai (nối nhau)
BAY, GIU, VE = 0.20, 0.14, 0.30                         # bay tới, găm ở đích, bay về
VONG_DI = {"a": 60.0, "b": 95.0, "c": 40.0}
VONG_VE = {"a": 150.0, "b": 210.0, "c": 110.0}
TV = max(T_PHONG.values()) + BAY + GIU + VE
D_CAST = round(TV + 0.30, 2)
T_RUT, T_GONG0, T_GONG1 = 0.22, 0.30, 0.80              # skill: rụt vào mai, mai rung
T_BAN_TROI, T_DUNG, T_MUA, T_SKILL_TRUNG = 0.86, 1.02, 1.20, 1.50
T_MOC = 1.66                                            # skill: cụm pha lê mọc lại
D_SKILL = 2.10
T_CHAM, T_BUNG = 0.34, 0.62                             # appear: mai chạm đất, chân / mặt bật ra
D_APPEAR = 1.60


def lam_clip(sk, info, cao=180.0):
    CD = chuyen_dong(info)

    def dat(P, goc, tau, lap=False, chi=None, bo=()):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if (chi is not None and b not in chi) or b in bo:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))

    def dam(P, a, chi=None):
        if a < 0.999:
            for sl in sk.slots:
                if chi is None or sl["name"] in chi:
                    P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def nheo(P, k):
        """nheo / nhắm hai mắt: co dọc nhóm mặt (head2: tròng, mày, miệng) quanh gốc; k = 1 thường, < 1 nheo."""
        P.scale("head2", 1.0, k)

    def _dich_cha(P, b, dx, dy):
        """dời thế giới (dx, dy) của xương b → dời trong hệ xương cha (tư thế P)."""
        W = sk.the_gioi(P)
        Wp = W[sk.bones[sk.bi[b]]["parent"]]
        d = np.linalg.solve(Wp[:2, :2], np.array([dx, dy]))
        return float(d[0]), float(d[1])

    # ------------------------------------------------ idle: sóng mềm lệch pha (người dùng: idle_01 + hắt xì "bị giật, không mềm mại")
    D_IDLE = 2.0
    w = 2 * math.pi / D_IDLE

    def song(t, tre, k=1.0):
        return math.sin(w * k * (t - tre))

    def f_idle(t, P):
        dat(P, "idle_01", 0.0)                                   # dáng gốc khung 0; mọi chuyển động là sóng tròn chu kỳ 2 s
        th = song(t, 0.0)
        P.scale("day", 1.0 + 0.016 * th, 1.0 - 0.020 * th)        # thở (giữ thể tích)
        P.move("day", 0.0, 1.6 * song(t, 0.05))
        P.rot("tam", 0.8 * song(t, 0.10))
        P.rot("head", 1.4 * song(t, 0.14))                       # đầu trễ thân
        P.move("head", 0.0, 1.2 * song(t, 0.16))
        P.rot("hair", -1.0 * song(t, 0.24))                      # mai trễ hơn, ngược chiều đầu chút
        for b, tre, a in (("hair3", 0.30, 4.0), ("hair2", 0.36, 5.0), ("hair4", 0.28, 4.0), ("hair5", 0.40, 3.0)):
            P.rot(b, a * song(t, tre))                           # sỏi lúc lắc trễ dần
        P.rot("all18", 7.0 * song(t, 0.32, 2.0))                  # đuôi vẫy hai nhịp mỗi vòng
        P.rot("mml", 2.5 * song(t, 0.22))
        P.rot("mmr", 2.5 * song(t, 0.27))
        # trò nhỏ: tai phải giật hai cái (1,10 → 1,40), mắt liếc về trước rồi về (1,45 → 1,85), mũi hít (0,55 → 0,85)
        P.rot("mmr", 10.0 * hoat.cv(t, [(1.10, 0.0), (1.16, 1.0, "out"), (1.24, 0.0, "io"), (1.30, 0.8, "out"), (1.40, 0.0, "io")]))
        lie = hoat.cv(t, [(1.45, 0.0), (1.56, 1.0, "io"), (1.74, 1.0), (1.86, 0.0, "io")])
        P.move("eyes", 2.5 * lie, -1.0 * lie)
        P.rot("head", 1.2 * hoat.cv(t, [(0.55, 0.0), (0.62, 1.0, "io"), (0.69, 0.0, "io"), (0.76, 1.0, "io"), (0.85, 0.0, "io")]))

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    # điểm thấp nhất của cả con (đỉnh lưới mai, thân, pha lê ở idle 0, quanh tâm `tam`) khi nghiêng góc a: để lật mà vẫn nằm trên đất
    Vt = np.concatenate([sk.atts[s_][s_]["V"] for s_ in ("hair3", "body", "tinh_the") if s_ in sk.atts]) - info["tam"]
    y_tam = float(info["tam"][1])

    def thap_nhat(a):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        return y_tam + float((Vt[:, 0] * sa + Vt[:, 1] * ca).min())

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", t)
        lat = ease((t - 0.42) / 0.36, "in") if t > 0.42 else 0.0
        P.rot("tam", 95.0 * lat)                                   # lật ngửa ra sau
        P.move("day", -0.10 * cao * lat, max(0.0, -thap_nhat(95.0 * lat)) + 0.06 * cao * math.sin(math.pi * min(1.0, lat)))
        if t > 0.78:                                               # chạm đất: nảy, sỏi rơi
            b = math.exp(-(t - 0.78) / 0.07) * math.sin((t - 0.78) * 2 * math.pi / 0.18)
            P.scale("day", 1 + 0.08 * b, 1 - 0.1 * b)
            for k, s in enumerate(("hair2", "hair3", "hair4", "hair5")):
                P.move(s, 0.0, -14.0 * ease(min(1.0, (t - 0.78 - 0.03 * k) / 0.2), "in") if t > 0.78 + 0.03 * k else 0.0)
        if t > 0.5:
            nheo(P, 0.25)
        dam(P, float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0)))

    # ------------------------------------------------ attack: lao húc
    def f_attack(t, P):
        dat(P, "skill_01_1", tmap(t, [(0.0, 0.0), (0.30, 0.30, "io"), (T_HUC, 0.40, "in"), (0.55, 0.55, "out"), (D_ATTACK, 0.93, "io")]))
        if t < T_HUC - 0.10:
            lao = -0.05 * ease(t / (T_HUC - 0.10))
        elif t < T_HUC:
            lao = -0.05 + (LAO + 0.05) * ease((t - (T_HUC - 0.10)) / 0.10, "in")
        elif t < T_HUC + 0.12:
            lao = LAO
        else:
            lao = LAO * (1 - ease((t - T_HUC - 0.12) / max(0.05, D_ATTACK - 0.10 - T_HUC - 0.12)))
        P.move("move", cao * lao, 0.0)
        k = math.exp(-((t - (T_HUC + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 - 0.10 * k, 1 + 0.09 * k)

    # ------------------------------------------------ cast: nhún, bật lên, lắc mai → ba viên sỏi bay găm vào đối thủ → bay về lắp lại mai
    far = sk.W0["far"][:2, 2] if "far" in sk.bi else np.array([0.9 * cao + 140.0, 0.45 * cao])
    BO_SOI = ("hair2", "hair3", "hair4", "hair5")

    def than_cast(t, P):
        """dáng thân của cast (không kể sỏi bay): skill_02 của họ cho thân + mai (sỏi giữ dáng gốc), lắc mai, đáp, đón sỏi về."""
        tau = tmap(t, [(0.0, 0.0), (T_NHAY, 0.47, "io"), (T_DAP_C, 0.62, "in"), (D_CAST, 1.20, "io")])
        dat(P, "skill_02", tau, bo=BO_SOI)
        if T_LAC0 < t < T_LAC1 + 0.06:                           # lắc mai thật mạnh như chó rũ nước
            e = math.sin(math.pi * min(1.0, (t - T_LAC0) / (T_LAC1 + 0.06 - T_LAC0)))
            r = 12.0 * e * math.sin((t - T_LAC0) * 2 * math.pi / 0.075)
            P.rot("hair", r)
            P.rot("body", 0.35 * r)
            for k, b in enumerate(BO_SOI):
                P.rot(b, 1.6 * r * (1 if k % 2 else -1))
            nheo(P, 0.65)
        if t > T_DAP_C:                                          # đáp phịch
            b = math.exp(-(t - T_DAP_C) / 0.08) * math.sin((t - T_DAP_C) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.10 * b, 1 - 0.12 * b)
        for k in BAY_MANH:                                       # mỗi viên về: mai nảy nhẹ đón
            tv = T_PHONG[k] + BAY + GIU + VE
            if t > tv:
                b = math.exp(-(t - tv) / 0.05) * math.sin((t - tv) * 2 * math.pi / 0.14)
                P.rot("hair", 3.0 * b)

    def f_cast(t, P):
        than_cast(t, P)
        W = None
        for ben, (s_, b_) in BAY_MANH.items():
            t0 = T_PHONG[ben]
            t_toi, t_ve0 = t0 + BAY, t0 + BAY + GIU
            t_ve1 = t_ve0 + VE
            fb, bb = f"fly_{ben}", f"bay_{ben}"
            if fb not in sk.bi:
                continue
            if t < t0:
                P.alpha[bb] = 0.0
                continue
            tt = min(t, t_ve1)
            if t < t_ve1:
                P.alpha[s_] = 0.0
                P.alpha[bb] = 1.0
            else:
                P.alpha[bb] = 0.0
            A = sk.W0[fb][:2, 2].copy()
            v = far - A
            n = np.array([-v[1], v[0]]) / (float(np.hypot(*v)) or 1.0)
            if tt < t_toi:
                f = ease((tt - t0) / BAY, "in")
                pos = A + f * v + n * VONG_DI[ben] * math.sin(math.pi * f)
                ang = -540.0 * f
            elif tt < t_ve0:
                pos = far.copy() + np.array([6.0, 0.0]) * math.sin((tt - t_toi) * 60.0) * math.exp(-(tt - t_toi) / 0.06)
                ang = -540.0
            else:                                                # bay về, đáp ĐÚNG chỗ viên sỏi thật đang ở trên mai
                if W is None:
                    W = sk.the_gioi(P)
                rb, Wl = REF[ben]
                Mt = W[rb] @ np.linalg.inv(Wl) @ sk.W0[bb]
                u = (tt - t_ve0) / VE
                e = ease(u, "io")
                pos = far * (1 - e) + Mt[:2, 2] * e + n * VONG_VE[ben] * math.sin(math.pi * u)
                g1 = _goc(Mt) - _goc(sk.W0[bb])
                ang = -540.0 * (1 - e) + (g1 - 720.0) * e
            P.move(fb, float(pos[0] - A[0]), float(pos[1] - A[1]))
            P.rot(bb, float(ang))

    # ------------------------------------------------ skill: rụt mai gồng → pha lê bung → đứng dậy chĩa mõm, mưa pha lê
    def f_skill(t, P):
        dat(P, "idle_01", 0.0)
        rut = hoat.cv(t, [(0.0, 0.0), (T_RUT, 1.0, "out"), (T_GONG1, 1.0), (T_BAN_TROI, -0.35, "out"), (T_DUNG, 0.0, "io"), (D_SKILL, 0.0)])
        r = max(rut, 0.0)
        # rụt vào mai: chân co lại dưới thân, cả con hạ sát đất, đầu rụt về sau; mai, pha lê GIỮ NGUYÊN HÌNH (không bóp `day`)
        for s_ in ("all5", "all8", "all11", "all14"):
            P.scale(s_, 1.0 - 0.6 * r, 1.0 - 0.6 * r)
        P.move("day", 0.0, -0.075 * cao * r + 9.0 * max(-rut, 0.0))           # bật lên lúc pha lê bung
        P.scale("day", 1.0 + 0.025 * r, 1.0 - 0.025 * r)
        P.move("head", -7.0 * r, -7.0 * r)
        if r > 0.2:
            nheo(P, 1.0 - 0.6 * min(1.0, r))
        if T_GONG0 < t < T_GONG1 + 0.04:                                       # mai rung lạch cạch, sỏi nảy
            e = min(1.0, (t - T_GONG0) / 0.2)
            r = 4.0 * e * math.sin((t - T_GONG0) * 2 * math.pi / 0.06)
            P.rot("hair", r)
            for k, s in enumerate(("hair2", "hair3", "hair4", "hair5")):
                P.move(s, 0.0, 5.0 * e * abs(math.sin((t - T_GONG0) * 2 * math.pi / (0.11 + 0.02 * k))))
        # cụm pha lê: nén một nhịp rồi VỌT lên trời (ra khỏi khung) → ẩn → mọc lại trong hốc mai (trục x của pha_le chĩa lên)
        if t < T_BAN_TROI:
            nen = hoat.cv(t, [(T_BAN_TROI - 0.12, 0.0), (T_BAN_TROI - 0.04, 1.0, "out"), (T_BAN_TROI, 0.0)])
            P.scale("pha_le", 1.0 - 0.10 * nen, 1.0 + 0.06 * nen)
        elif t < T_MOC:
            vot = ease((t - T_BAN_TROI) / 0.14, "in")
            P.move("pha_le", *_dich_cha(P, "pha_le", 0.0, 2.6 * cao * vot))
            P.scale("pha_le", 1.0 + 0.35 * vot, 1.0 - 0.15 * vot)            # kéo dài theo hướng bay
            if t > T_BAN_TROI + 0.14:
                P.alpha["tinh_the"] = 0.0
        else:
            k = hoat.cv(t, [(T_MOC, 0.1), (T_MOC + 0.12, 1.18, "out"), (T_MOC + 0.22, 0.94, "io"), (T_MOC + 0.30, 1.0, "io")])
            P.scale("pha_le", k, k)
        # đứng dậy, chĩa mõm về đối thủ, giữ tới khi mưa xong
        chi = hoat.cv(t, [(T_DUNG, 0.0), (T_DUNG + 0.14, 1.0, "out"), (1.70, 1.0), (D_SKILL - 0.05, 0.0, "io")])
        P.rot("head", -6.0 * chi)
        P.rot("tam", -4.0 * chi)
        if T_MUA < t < 1.72:                                                   # dáng giữ có trôi
            P.rot("body", 1.5 * math.sin((t - T_MUA) * 2 * math.pi / 0.16))
        if t > T_SKILL_TRUNG:
            b = math.exp(-(t - T_SKILL_TRUNG) / 0.09) * math.sin((t - T_SKILL_TRUNG) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.05 * b, 1 - 0.06 * b)

    # ------------------------------------------------ appear: mai rơi → chạm đất nảy → chân, mặt bật ra → rũ mình → cau mày
    than_an = ("body", "body_truoc", "tail", "hair5") + CHAN + MAT + TAI

    def f_appear(t, P):
        dat(P, "idle_01", 0.0)
        y = hoat.cv(t, [(0.0, 0.85 * cao), (T_CHAM, 0.0, "in"), (0.42, 0.10 * cao, "out"), (0.50, 0.0, "in")])
        P.move("day", 0.0, y)
        P.rot("tam", hoat.cv(t, [(0.0, -25.0), (T_CHAM, 0.0, "in"), (0.42, 4.0, "out"), (0.50, 0.0, "in")]))
        for x in (T_CHAM, 0.50):
            if t > x:
                b = math.exp(-(t - x) / 0.06) * math.sin((t - x) * 2 * math.pi / 0.16)
                P.scale("day", 1 + 0.12 * b, 1 - 0.14 * b)
        dam(P, min(1.0, t / 0.06))                                               # khung đầu trống
        hien = float(np.clip((t - (T_BUNG - 0.04)) / 0.06, 0.0, 1.0))
        dam(P, hien, chi=than_an)
        P.att["hair3"] = "hair3_tron" if hien < 0.5 else "hair3"
        if t < T_BUNG + 0.30:                                                    # chân bật ra (to dần, vượt, về)
            k = hoat.cv(t, [(T_BUNG - 0.04, 0.15), (T_BUNG + 0.08, 1.15, "out"), (T_BUNG + 0.18, 0.95, "io"), (T_BUNG + 0.28, 1.0, "io")])
            for s in ("all5", "all8", "all11", "all14", "all18"):
                P.scale(s, k, 1.0)
            P.move("head", -10.0 * (1 - min(1.0, k)), -8.0 * (1 - min(1.0, k)))
        if 0.95 < t < 1.28:                                                      # rũ mình
            e = math.sin(math.pi * (t - 0.95) / 0.33)
            r = 9.0 * e * math.sin((t - 0.95) * 2 * math.pi / 0.11)
            P.rot("body", r)
            P.rot("hair", -0.6 * r)
            nheo(P, 0.5)
        cau = hoat.cv(t, [(1.30, 0.0), (1.40, 1.0, "out"), (D_APPEAR, 1.0)])       # cau mày, nhìn đối thủ
        P.move("yp", 0.0, -2.5 * cau)

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_CHAM, "cham_dat", ""), (T_BUNG, "bung", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(T_HUC, "trung", "")], trung=T_HUC),
        Clip("cast", D_CAST, f_cast, ev=[(T_LAC0, "ran", "")] + [(round(T_PHONG[k], 3), "phong", k) for k in BAY_MANH] +
             [(round(T_PHONG["a"] + BAY, 3), "trung", ""), (T_DAP_C, "cham_dat", "")] +
             [(round(T_PHONG[k] + BAY + GIU + VE, 3), "ve", k) for k in BAY_MANH], trung=round(T_PHONG["a"] + BAY, 3)),
        Clip("skill", D_SKILL, f_skill, ev=[(T_GONG0, "gong", ""), (T_BAN_TROI, "ban_troi", ""), (T_MUA, "mua", ""),
                                             (T_SKILL_TRUNG, "trung", ""), (T_MOC, "moc", "")], trung=T_SKILL_TRUNG),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
    ]
    return clips, than_cast


REF = {}                                                # sỏi bay → (xương tham chiếu, ma trận thế giới của nó lúc phóng)


def them_soi_bay(sk, info, than_cast, cao, far_xy=None):
    """xương far + fly_<k> (tâm viên sỏi lúc rời mai) + bay_<k> và slot bản sao (ẩn) cho từng viên sỏi bay của cast (như
    quang_sat_rig.them_tay_bay). far_xy: đặt đích khác mặc định (bản xem trước có đối thủ)."""
    fx, fy = far_xy if far_xy is not None else (0.9 * cao + 140.0, 0.45 * cao)
    sk.xuong("far", "root", float(fx), float(fy))
    for ben, (s, rb) in BAY_MANH.items():
        P = khung.Pose()
        than_cast(T_PHONG[ben], P)
        W = sk.the_gioi(P)
        att = sk.atts[s][s]
        V = np.array([sum(w * (W[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in att["verts"]])
        c = V.mean(0)
        sk.xuong(f"fly_{ben}", "root", float(c[0]), float(c[1]))
        sk.xuong(f"bay_{ben}", f"fly_{ben}", float(c[0]), float(c[1]), goc=_goc(W[rb]), the_gioi=True)
        inv = np.linalg.inv(sk.W0[f"bay_{ben}"])
        rows = [[(f"bay_{ben}", *[float(q) for q in (inv @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        sk.slot(f"bay_{ben}", "move", s, an=True)
        sk.luoi_gan(f"bay_{ben}", s, sk.luoi[(s, s)], trongso.cung(len(rows), "move"), the_gioi=V)
        sk.atts[f"bay_{ben}"][s]["verts"] = rows
        REF[ben] = (rb, W[rb].copy())


def dung_het(far_xy=None):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    them_soi_bay(sk, info, than_cast, cao, far_xy)
    clips, _ = lam_clip(sk, info, cao)
    return sk, info, clips, cao


def main(a):
    sk, info, clips, cao = dung_het()
    ve0 = soi.Ve(sk)
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c)
            xau = []
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 35.0:
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for b in ("hip", "head", "hair", "hair2", "hair3", "hair4"):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.22 * cao:
                        xau.append(f"{i / 30:.2f}s {b} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:14]) + (" ..." if len(xau) > 14 else "")))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        if ":" in a[2]:
            t0, t1, n = a[2].split(":")
            ts = list(np.linspace(float(t0), float(t1), int(n)))
        elif a[2].startswith("n="):
            ts = list(np.linspace(0, c.dur, int(a[2][2:])))
        else:
            ts = [float(x) for x in a[2].split(",")]
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.9
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            ImageDraw.Draw(im).text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Tatu mai đá (cong_da_1): tướng 1 đảo Thổ", dang=1, so_dang=1, dung_yen=("cast", "skill"),
                  far=("cast",),
                  ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT, tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015},
                  dich_mb=0.3, tran_mb=0.5, span=3.6)


if __name__ == "__main__":
    main(sys.argv[1:])
