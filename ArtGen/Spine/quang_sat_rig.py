# -*- coding: utf-8 -*-
"""Tinh linh quặng sắt (quang_sat; tướng 3 đảo Kim): hình của mình chạy trên ĐÚNG rig của con gốc monster_3371. Ghi chú:
inbox/quang_sat_ghichu.md. Cách làm như tinh_sat_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ (FK; hai transform nhỏ đã được runtime nướng vào biến đổi riêng `l` của mẫu khung), thêm
  `move` (cú lao, đường đào: game nắn quãng), `day` (đáy thân: tâm bẹp / phình, nhảy lên xuống), `tam` (tâm thân: lộn, nghiêng; cha của
  `all`), `far` + `fly_t`, `fly_p` + `bay_t`, `bay_p` (tay bay của chiêu mana: game co quãng tới đối thủ, AolaActor.FarAtomik, farAim),
  `ho` (hố đất), `go` (gò đất chạy ngầm), `cat_x` (mặt nạ cắt: thân chui xuống / trồi lên khỏi hố).
- MẢNH: ảnh của mình "đúng chỗ, đúng cỡ" (quang_sat_manh.py → inbox/quang_sat_1/manh/), đặt vào thế giới rig ở dáng idle 0; mảnh bám nhiều
  xương (thân, ba tinh thể đầu) là lưới phủ hình, mỗi đỉnh biến dạng ĐÚNG như điểm tương ứng trên lưới của họ (gan_goc: trọng số + điểm gắn
  riêng từng xương); mảnh một xương (tay, mắt) là ô 4 đỉnh. Mắt ba hình: mở, nhắm `> <` (đổi theo khung như họ), ngủ (appear).
  BỎ slot shadow và bản sao tinh thể đầu của skill_02 (không dùng).
- CHUYỂN ĐỘNG (người dùng 2026-11-16):
    idle   = idle_01 (chớp, nheo một mắt như họ) + trò riêng: hai tay quặng xoay một vòng như nam châm (Claude thêm, "sửa đi chút");
    walk   = run_01; hit = hit_01; die = die_01 + tan;
    appear = nằm bẹp dưới đất ngủ (mắt ngủ, thở), mở mắt (lờ đờ, chớp, mở to), bật bay lên rồi hạ về dáng đứng;
    attack = skill_01_1 (nheo mắt, ngả ra sau, bật chéo lên húc): LAO VÀO HÚC, quãng tới dồn vào `move`;
    cast   = PHÓNG HAI TAY: lấy đà, hai tay quặng bay tới đối thủ (bản sao trên `fly_*`, code co quãng + chĩa theo hướng bay), găm,
             rút về khớp đúng chỗ tay thật;
    skill  = CHUI ĐẤT: bật lên lộn ngược, cắm đầu xuống hố; gò đất (mũi tinh thể ló lên như vây cá) chạy tới đối thủ (`move`, khai
             lunge: game nắn tới 72 % quãng); TRỒI LÊN HÚC từ dưới (đoạn bật của skill_01_2); nhảy lùi về chỗ cũ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/quang_sat_rig.py        → inbox/quang_sat_1/rig/
    py -3 -I ArtGen/Spine/quang_sat_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]    → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, khung, hoat, xuat, soi, luoi, trongso  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import quang_sat as G  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

DANG = int(os.environ.get("QS_DANG", "1"))           # 1: tinh linh quặng sắt; 2: dạng cuối (đá bazan, năm gai hematit; cùng rig, đòn mạnh hơn)
TEN_RIG = f"quang_sat_{DANG}"
BASE_D = os.path.join(os.path.dirname(G.BASE), TEN_RIG)
D_PX = float(os.environ.get("QS_DPX", "1.2"))        # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~310 đơn vị)
MANH = os.path.join(G.BASE, "manh_goc") if os.environ.get("QS_GOC") == "1" else os.path.join(BASE_D, "manh")
RA = os.environ.get("QS_RA") or os.path.join(G.BASE, "rig_goc" if os.environ.get("QS_GOC") == "1" else os.path.join(BASE_D, "rig"))
TAN = 0.45
FPS = 30.0
IMPACT = ({"attack": (0.08, 0.45, 0.12), "cast": (0.08, 0.5, 0.10), "skill": (0.20, 1.1, 0.25, "#ffffff4d")} if DANG == 1 else
          {"attack": (0.10, 0.6, 0.15), "cast": (0.10, 0.6, 0.12), "skill": (0.26, 1.4, 0.32, "#ffffff66")})

# slot của họ dùng (thứ tự vẽ idle, sau → trước) và hình từng slot
SLOT_HO = ["longdan_6", "longdan_0", "longdan_9", "longdan_8", "longdan_7", "longdan_4", "longdan_3", "longdan_2", "longdan_1", "longdan_5"]
HINH = {"longdan_0": ["longdan_0"], "longdan_9": ["longdan_9"], "longdan_8": ["longdan_8", "longdan_6", "ngu_p"],
        "longdan_7": ["longdan_7", "longdan_5", "ngu_t"], "longdan_4": ["longdan_4"], "longdan_3": ["longdan_3"], "longdan_2": ["longdan_2"],
        "longdan_1": ["longdan_1"],
        "longdan_6": ["longdan_0"], "longdan_5": ["longdan_1"]}             # bản sao hai tay của die_01 (bám longdan_6 / longdan_4)
BAN_SAO = {"longdan_6": "longdan_0", "longdan_5": "longdan_1"}             # slot bản sao → slot tay thật cùng hình
TAY = {"t": ("longdan_1", "longdan_8"), "p": ("longdan_0", "longdan_0")}  # tay trái / phải: (slot = tên ảnh, xương)
GAN_THEO = {}                                                            # slot thêm (không có ở con gốc) → bám như lưới của slot này
if DANG == 2:                                    # hai gai ngoài của chùm năm gai: bám như lưới thân (vẽ trước thân như các tinh thể đầu)
    SLOT_HO = SLOT_HO[:SLOT_HO.index("longdan_2") + 1] + ["gai_t", "gai_p"] + SLOT_HO[SLOT_HO.index("longdan_2") + 1:]
    HINH.update({"gai_t": ["gai_t"], "gai_p": ["gai_p"]})
    GAN_THEO = {"gai_t": "longdan_9", "gai_p": "longdan_9"}
# mảnh bay của chiêu mana: khoá → (slot = tên ảnh, xương tham chiếu: mảnh bám theo xương này khi lắp lại)
BAY_MANH = dict(TAY)
if DANG == 2:                                    # dạng 2: hai tay + năm gai trên đầu cùng bay (gai bám lưới thân → tham chiếu longdan_9)
    BAY_MANH.update({"g3": ("longdan_3", "longdan_9"), "g2": ("longdan_2", "longdan_9"), "gt": ("gai_t", "longdan_9"),
                     "gp": ("gai_p", "longdan_9"), "g4": ("longdan_4", "longdan_9")})
TINH_THE_DAU = ("longdan_4", "longdan_3", "longdan_2")
MAT = ("longdan_7", "longdan_8")
THAN = ("longdan_9",)


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
    return s, to_rig


def anh_manh(ten):
    """ảnh mảnh của mình đã thu về D_PX px / đơn vị + hộp (px concept) + hệ số thu."""
    thu = MANH
    DATJ = json.load(open(os.path.join(thu, "dat.json")))
    if ten not in DATJ:                                  # chưa có mảnh của mình: tạm dùng bộ da gốc (chỉ để chạy thử)
        thu = os.path.join(G.BASE, "manh_goc")
        DATJ = json.load(open(os.path.join(thu, "dat.json")))
        print(f"  (tạm) {ten}: lấy từ manh_goc")
    s_px, _ = tf()
    g = Image.open(os.path.join(thu, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def trong_so_goc(V, a0, ten, Wi):
    """mỗi điểm V (thế giới idle 0) biến dạng như điểm tương ứng trên lưới của họ a0 (att_idle0): toạ độ trọng tâm trong tam giác chứa
    nó (ngoài lưới: điểm gần nhất trên cạnh + khoảng lệch), trọng số W_b = Σ β_k w_b(k), điểm gắn riêng q_b = Σ β_k w_b(k) v_k / W_b
    (xem rong_vay_rig.gan_goc). Trả hàng (xương, x, y, w) theo ma trận idle 0 Wi."""
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


def gan_manh(sk, slot, ten_anh, a0, ten, Wi, M=None, Wbind=None):
    """mảnh của mình (manh/<ten_anh>.png, hộp trên concept) thành lưới đặt đúng chỗ concept ở dáng idle 0. a0: hình của họ ở idle 0 (lưới
    nhiều xương → lưới phủ hình + gan_goc; một xương → ô 4 đỉnh bám xương đó). M (3×3, tuỳ chọn): đổi chỗ thế giới idle 0 → chỗ khác
    (bản sao tay của die nằm ở dáng gốc của xương khác), Wbind: ma trận dùng tính điểm gắn (mặc định Wi)."""
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig = tf()
    nhieu = bool(a0.get("w")) and M is None
    if nhieu:
        L = luoi.luoi_vung(im, buoc_vien=10.0, buoc_trong=16.0, vien=2, ten=slot, in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(Px)
    if M is not None:
        V = (M @ np.c_[V, np.ones(len(V))].T).T[:, :2]
    Wb = Wbind or Wi
    if nhieu:
        rows = trong_so_goc(V, a0, ten, Wb)
    else:
        b = ten[a0["bone"]] if isinstance(a0["bone"], int) else a0["bone"]
        rows = [[(b, *[float(v) for v in np.linalg.solve(Wb[b], np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


def anh_dat(ten):
    """đạo cụ đất (gò, hố) thu về D_PX px / đơn vị (cùng tỉ lệ concept)."""
    im, hop, kq = anh_manh(ten)
    return im


def tach_ho(im):
    """hố cả cái → (lớp sau: lòng + vành sau, lớp trước: vành dưới đường ngang qua tâm lòng hố), tâm lòng (px ảnh), bán trục lòng."""
    A = np.asarray(im).copy()
    rgb = A[..., :3].astype(int)
    al = A[..., 3] > 128
    long_ = al & (rgb.max(2) < 70)                     # lòng hố tô một màu nâu đen phẳng
    import cv2
    n, lab, st, _ = cv2.connectedComponentsWithStats(long_.astype(np.uint8), 8)
    k = 1 + int(np.argmax(st[1:, 4]))
    ys, xs = np.nonzero(lab == k)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    a, b = (xs.max() - xs.min()) / 2, (ys.max() - ys.min()) / 2
    yy = np.arange(A.shape[0])[:, None]
    sau, truoc = A.copy(), A.copy()
    duoi = np.broadcast_to(yy > cy, al.shape) & ~(lab == k)
    sau[..., 3] = np.where(duoi, 0, A[..., 3])
    truoc[..., 3] = np.where(duoi, A[..., 3], 0)
    return Image.fromarray(sau, "RGBA"), Image.fromarray(truoc, "RGBA"), (cx, cy), (a, b)


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wc, Wi = mats(D), mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    byg = {}
    for a in D["atts"]:
        byg.setdefault(a["slot"], []).append(a)
    Vb = np.array(by0["longdan_9"]["xy"], float).reshape(-1, 2)
    y_day = float(Vb[:, 1].min())
    tam = np.array([(Vb[:, 0].min() + Vb[:, 0].max()) / 2, (Vb[:, 1].min() + Vb[:, 1].max()) / 2])
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
        if cha == "root":                                  # all → con của tam (tâm thân), giữ nguyên chỗ thế giới
            sk.xuong(b["name"], "tam", g[0] - float(tam[0]), g[1] - float(tam[1]), goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        else:
            sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    # hố, gò đất, mặt nạ cắt (con của move: đi cùng chỗ con đứng)
    sk.xuong("ho", "move", float(tam[0]), 0.0)
    sk.xuong("go", "move", float(tam[0]), 0.0)
    sk.xuong("cat_x", "move", float(tam[0]), -CAT_SAU, sx=CAT_TI, sy=CAT_TI)

    # ---- slot
    im_ho = anh_dat("ho")
    sau, truoc, (hcx, hcy), (ha, hb) = tach_ho(im_ho)
    sk.anh("ho_sau", sau)
    sk.anh("ho_truoc", truoc)
    dat_ho = khung.Dat(float(tam[0]), 0.0, neo=(hcx, hcy), neo_px=True, ti=K_HO / D_PX)
    sk.slot("ho_sau", "ho", "ho_sau", an=True)
    sk.manh("ho_sau", "ho_sau", dat_ho)
    a_r, b_r = K_HO * ha / D_PX, K_HO * hb / D_PX       # bán trục lòng hố, đơn vị rig
    sk.slot("cat", "cat_x")
    tong = [0, 0]
    so_thu_tu = {}
    for s in SLOT_HO:
        if s in BAN_SAO:                                 # bản sao tay của die: ẩn sẵn, bám xương riêng ở dáng gốc
            goc = BAN_SAO[s]
            a_d = next(a for a in byg[s] if a["region"] == goc)
            a_t = by0[goc]
            M = doi_cho(a_t, a_d)
            sk.slot(s, "move", goc, an=True)
            L = gan_manh(sk, s, goc, a_d, ten, Wi, M=M, Wbind=Wc)
        else:
            sk.slot(s, "move", HINH[s][0])
            for h in HINH[s]:
                L = gan_manh(sk, s, h, by0[GAN_THEO.get(s, s)], ten, Wi)
                tong[0] += L.n
                tong[1] += len(L.tris)
        so_thu_tu[s] = len(sk.slots) - 1
    # tay phải ra TRƯỚC thân ở vài clip của họ (skill_01_2 đầu clip, skill_01_3, block): slot bản sao ngay sau mắt
    sk.slot("longdan_0~truoc", "move", "longdan_0", an=True, truoc="longdan_4")
    gan_manh(sk, "longdan_0~truoc", "longdan_0", by0["longdan_0"], ten, Wi)
    sk.cat("cat", "longdan_5", mat_na(a_r, b_r, float(tam[0])))
    sk.slot("ho_truoc", "ho", "ho_truoc", an=True)
    sk.manh("ho_truoc", "ho_truoc", dat_ho)
    im_go, _, _ = anh_manh("go_dat")
    sk.anh("go_dat", im_go)
    sk.slot("go_dat", "go", "go_dat", an=True)
    sk.manh("go_dat", "go_dat", khung.Dat(float(tam[0]), 0.0, neo=(0.5, 0.97), ti=K_GO / D_PX))
    for e, m in (("trung", "khung trúng"), ("phong", "cast: một tay quặng rời thân (chuỗi = t / p)"), ("ve", "cast: tay quặng lắp lại"),
                 ("dao", "skill: mũi tinh thể cắm đất, bụi đất toé (VFX)"), ("chay", "skill: gò đất bắt đầu chạy ngầm (VFX vệt đất)"),
                 ("troi", "skill: đất nổ tung, con trồi lên (VFX)"), ("cham_dat", "chạm đất (appear, skill)"), ("ngu", "appear: đang ngủ (Zzz)"),
                 ("huc1", "dạng 2: nhát húc thứ nhất (VFX; khung trúng của game ở nhát sau)"), ("troi2", "dạng 2: đất nổ lần hai")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy thân y = {y_day:.1f}, tâm thân "
          f"({tam[0]:.1f}, {tam[1]:.1f}); lòng hố {2 * a_r:.0f} × {2 * b_r:.0f}")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, S=S, Wi=Wi, ho=(a_r, b_r),
                    go_cao=K_GO * im_go.height / D_PX * 0.97)


CAT_TI, CAT_SAU = 12.0, 3000.0
CAO_GAME_2 = 285.0
K_HO, K_GO = 0.74, 0.68                                # GPT vẽ hố, gò to hơn dặn: thu cho lòng hố vừa thân chui lọt, gò rộng cỡ thân


def mat_na(a, b, x_tam):
    """đa giác LỒI của mặt nạ cắt (toạ độ thế giới dáng gốc khi xương cat_x ở tỉ lệ 1, gốc ở tâm miệng hố): giữ phần trên mặt đất + lòng
    hố. Đáy là đoạn giữa nửa dưới elip miệng hố (|x| ≤ 0,6 a), hai bên theo tiếp tuyến ra xa. Ở dáng gốc xương nằm sâu CAT_SAU và phóng
    CAT_TI lần (không cắt gì); clip đặt về đúng chỗ, cỡ khi cần."""
    pts = []
    for k in np.linspace(-0.6, 0.6, 9):
        x = k * a
        pts.append((x, -b * math.sqrt(max(0.0, 1 - k * k))))
    x0, y0 = pts[-1]
    m = 0.75 * b / a                                   # độ dốc tiếp tuyến ở |x| = 0,6 a
    R = 1400.0
    pts.append((x0 + R, y0 + m * R))
    pts.append((x0 + R, 2000.0))
    pts.append((-(x0 + R), 2000.0))
    pts.append((-(x0 + R), y0 + m * R))
    # chuẩn về hệ của xương cat_x ở dáng gốc: điểm gắn = (p − (0, −CAT_SAU)) / CAT_TI rồi khung.cat tự đổi qua W0 của cat_x;
    # truyền thẳng toạ độ thế giới dáng gốc tương ứng: tâm (tam_x, −CAT_SAU) + p × CAT_TI
    return [(x_tam + px * CAT_TI, -CAT_SAU + py * CAT_TI) for px, py in pts[::-1]]


def doi_cho(a_t, a_d):
    """ma trận affine (3×3) đưa hình a_t (tay thật ở idle 0) tới a_d (bản sao ở dáng gốc): khớp đỉnh theo uv."""
    U1, V1 = np.array(a_t["uv"]).reshape(-1, 2), np.array(a_t["xy"], float).reshape(-1, 2)
    U2, V2 = np.array(a_d["uv"]).reshape(-1, 2), np.array(a_d["xy"], float).reshape(-1, 2)
    idx = [int(np.argmin(np.hypot(*(U1 - u).T))) for u in U2]
    X = np.c_[V1[idx], np.ones(len(idx))]
    sol, *_ = np.linalg.lstsq(X, V2, rcond=None)
    M = np.eye(3)
    M[:2, :] = sol.T
    return M


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, IB, ten, goc0 = info["S"], info["IB"], info["ten"], info["goc0"]
    out = {}
    sl = info["slots"]
    i7, i8, i0, i9 = sl.index("longdan_7"), sl.index("longdan_8"), sl.index("longdan_0"), sl.index("longdan_9")
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
        mat = [(F["n"][i7] or "longdan_7", F["n"][i8] or "longdan_8") for F in fr]
        truoc = [F["o"].index(i0) > F["o"].index(i9) for F in fr]     # tay phải vẽ sau thân thì ra trước
        vis = [{sl[k]: bool(F["n"][k]) for k in range(len(sl))} for F in fr]
        out[clip] = (float(v["dur"]), res, len(fr), mat, truoc, vis)
    return out


# ---------------------------------------------------------------- mốc giờ
# attack: lấy đà (nheo mắt, ngả ra sau) chậm hơn chút, bật húc đúng lúc trúng, rơi về
T_HUC = 0.46
M_ATTACK = [(0.0, 0.0), (0.36, 0.36, "io"), (T_HUC, 0.48, "in"), (0.62, 0.62, "out"), (1.0, 1.067, "io")]
LAO = 0.62                                             # đỉnh lao (× chiều cao) ở khung húc; sân nắn tới 72 % quãng
# cast: phóng hai tay
T_DA = 0.36                                            # hết lấy đà
T_PHONG = {"t": 12 / 30.0, "p": 14 / 30.0}                       # tay rời thân (bội của 1/30 cho khớp khung mẫu)
BAY = 0.20                                             # thời gian bay tới
GIU = 0.24                                             # găm ở đích
VE = 0.30                                              # bay về
VONG_DI = {"t": 70.0, "p": 25.0}                       # vồng lên của đường bay đi / về (tay trái về vòng qua đầu, không quét ngang mặt)
VONG_VE = {"t": 250.0, "p": 70.0}
if DANG == 2:                                          # năm gai rời đầu nối nhau sau hai tay, gai giữa (to nhất) cuối cùng
    T_PHONG.update({"g3": 16 / 30.0, "g2": 17 / 30.0, "gt": 18 / 30.0, "gp": 19 / 30.0, "g4": 21 / 30.0})
    VONG_DI.update({k: 90.0 for k in ("g3", "g2", "gt", "gp", "g4")})
    VONG_VE.update({"g3": 150.0, "g2": 110.0, "gt": 190.0, "gp": 90.0, "g4": 130.0})
TV = max(T_PHONG.values()) + BAY + GIU + VE            # mảnh cuối lắp lại
D_CAST = TV + 0.41
# skill: chui đất → chạy ngầm → trồi lên húc → nhảy lùi về
T_LAT0, T_LAT1 = 0.30, 0.56                            # bật lên + lộn ngược
T_DAO = 0.62                                           # mũi tinh thể cắm đất (sự kiện dao)
T_KHUAT = 0.82                                         # thân khuất hẳn dưới đất (ẩn mọi mảnh)
T_DOI = 0.88                                           # đổi sang dáng đứng dưới đất (khung trước, sau đều ẩn)
T_GO = 0.88                                            # gò đất nhô lên ở miệng hố
T_CHAY0, T_CHAY1 = 1.02, 1.80                          # gò đất chạy ngầm (move 0 → D_DAO)
T_TROI = 1.92                                          # đất nổ, con trồi lên
T_SKILL_HUC = 2.08                                     # húc trúng (đỉnh vọt)
T_DAP = 2.40                                           # rơi chạm đất
T_LUI0, T_LUI1 = 2.56, 3.02                            # nhảy lùi về chỗ cũ
D_SKILL = 3.20
D_DAO = 0.90                                           # quãng chạy ngầm (× chiều cao) trong rig; game nắn lại
T_HUC1 = T_XUONG = T_TROI2 = None
if DANG == 2:                                          # trồi húc HAI lần: húc, rơi lại xuống hố, trồi lên húc lần hai cao hơn
    T_HUC1, T_XUONG, T_TROI2 = 2.08, 2.36, 2.46
    T_SKILL_HUC, T_DAP, T_LUI0, T_LUI1, D_SKILL = 2.66, 3.00, 3.16, 3.62, 3.82
    LAO2_DAP, D_ATTACK = 0.92, 1.45                    # đánh thường: húc (T_HUC) rồi lộn một vòng giáng xuống (LAO2_DAP)
else:
    D_ATTACK = 1.0
# appear
T_THUC = 1.10                                          # hết ngủ, bắt đầu mở mắt
T_BAT_LEN = 1.62                                       # bật bay lên
D_APPEAR = 2.36


def lam_clip(sk, info, cao=310.0):
    CD = chuyen_dong(info)
    tam = info["tam"]
    far = sk.W0["far"][:2, 2] if "far" in sk.bi else np.array([0.9 * cao + 140.0, 0.45 * cao])

    def dat(P, goc, tau, lap=False, mat=True, chi=None):
        dur, R, n, M, TR, _ = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if chi is not None and b not in chi:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        k = min(n - 1, int(round(x)))
        if mat:
            P.att["longdan_7"], P.att["longdan_8"] = M[k]
        tr = TR[k]
        P.alpha["longdan_0~truoc"] = 1.0 if tr else 0.0
        P.alpha["longdan_0"] = 0.0 if tr else P.alpha.get("longdan_0", 1.0)

    def dam(P, a, chi=None):
        if a < 0.999:
            for sl in sk.slots:
                if chi is None or sl["name"] in chi:
                    P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def mat_co(P, k):
        """nhắm / nheo / mở to hai mắt: tỉ lệ dọc (sx của xương cha hai mắt, xoay ~107°)."""
        P.scale("longdan_5", k, 1.0)

    def pha(Pa, Pb, w):
        Q = khung.Pose()
        for b in set(Pa.t) | set(Pb.t):
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            Q.t[b] = [a_[q] + (b_[q] - a_[q]) * w for q in range(5)]
        Q.alpha = dict(Pa.alpha if w < 0.5 else Pb.alpha)
        Q.att = dict(Pb.att if w > 0.5 else Pa.att)
        return Q

    def dat_tg(P, b, xy, goc_tg, k=1.0):
        """đặt xương b tới chỗ xy, góc goc_tg THẾ GIỚI (trong tư thế P); k = mức hoà 0..1."""
        if k <= 1e-4:
            return
        W = sk.the_gioi(P)
        cha = sk.bones[sk.bi[b]]["parent"]
        Wp = W[cha]
        lp = np.linalg.solve(Wp, np.array([xy[0], xy[1], 1.0]))
        b0 = sk.bones[sk.bi[b]]
        g = P._g(b)
        dx, dy = float(lp[0]) - b0["x"], float(lp[1]) - b0["y"]
        dr = goc_tg - _goc(Wp) - b0["rot"]
        cur = _goc(W[b]) - _goc(Wp) - b0["rot"]
        dr = cur + ((dr - cur + 180.0) % 360.0 - 180.0)
        g[0] += k * (dx - g[0])
        g[1] += k * (dy - g[1])
        g[2] += k * (dr - g[2])

    def tg(P, b):
        W = sk.the_gioi(P)
        return W[b][:2, 2].copy(), _goc(W[b])

    # tâm hình từng tay (thế giới dáng idle 0) để xoay quanh tâm thay vì quanh gốc xương
    def tam_tay(s):
        V = sk.atts[s][s]["V"]
        return V.mean(0)

    def xoay_quanh(P, b, c_tg, goc):
        """xoay xương b thêm `goc` độ quanh điểm thế giới c_tg (giữ chỗ điểm đó); góc cộng thẳng (quay trọn vòng được)."""
        if abs(goc) < 1e-4:
            return
        W = sk.the_gioi(P)
        p = W[b][:2, 2]
        ca, sa = math.cos(math.radians(goc)), math.sin(math.radians(goc))
        d = p - c_tg
        p2 = c_tg + np.array([ca * d[0] - sa * d[1], sa * d[0] + ca * d[1]])
        Wp = W[sk.bones[sk.bi[b]]["parent"]]
        dl = np.linalg.solve(Wp[:2, :2], p2 - p)
        P.move(b, float(dl[0]), float(dl[1]))
        P.rot(b, goc)

    # ------------------------------------------------ idle: idle_01 + hai tay xoay một vòng như nam châm (4,30 → 5,10)
    def f_idle(t, P):
        dat(P, "idle_01", t, True)
        u = (t - 4.30) / 0.80
        if u >= 1:                                       # giữ +360 tới hết vòng lặp (xoay 360 ≡ 0, khỏi nhảy góc ngược một vòng)
            P.rot(TAY["t"][1], 360.0)
            P.rot(TAY["p"][1], -360.0)
        elif u > 0:
            k = ease(u, "io")
            nh = math.sin(math.pi * u)
            P.move("day", 0.0, 10.0 * nh)
            for ben, dau in (("t", 1.0), ("p", -1.0)):
                s, b = TAY[ben]
                W = sk.the_gioi(P)
                c = (W[b] @ np.linalg.solve(sk.W0[b], np.array([*tam_tay(s), 1.0])))[:2]
                xoay_quanh(P, b, c, dau * 360.0 * k)
            if 0.1 < u < 0.9:
                mat_co(P, 0.62)

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", t)
        vis = CD["die_01"][5][min(CD["die_01"][2] - 1, int(round(min(t, d) * FPS)))]
        for s in ("longdan_6", "longdan_5", "longdan_0", "longdan_1"):
            if not vis.get(s, True):
                P.alpha[s] = 0.0
            elif s in BAN_SAO:
                P.alpha[s] = 1.0
        dam(P, float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0)))

    # ------------------------------------------------ attack: lao vào húc
    x0_than = CD["skill_01_1"][1].get("longdan_2", np.zeros((1, 5)))[0, 1]

    def f_attack(t, P):
        if DANG == 2:
            dat(P, "skill_01_1", tmap(t, [(0.0, 0.0), (0.36, 0.36, "io"), (T_HUC, 0.48, "in"), (0.62, 0.62, "out"), (0.98, 0.70, "lin"),
                                          (D_ATTACK, 1.067, "io")]))
        else:
            dat(P, "skill_01_1", tmap(t, M_ATTACK))
        g = P._g("longdan_2")
        dx = g[0] - x0_than
        g[0] -= max(0.0, dx)                            # quãng tới của thân dồn sang move
        t_ve = T_HUC + 0.12 if DANG == 1 else LAO2_DAP + 0.10
        if t < T_HUC - 0.12:
            lao = -0.05 * ease(t / (T_HUC - 0.12))
        elif t < T_HUC:
            lao = -0.05 + (LAO + 0.05) * ease((t - (T_HUC - 0.12)) / 0.12, "in")
        elif t < t_ve:
            lao = LAO
        else:
            lao = LAO * (1 - ease((t - t_ve) / max(0.05, D_ATTACK - 0.08 - t_ve)))
        P.move("move", cao * lao, 0.0)
        k = math.exp(-((t - (T_HUC + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 - 0.14 * k, 1 + 0.10 * k)          # bẹp theo chiều húc đúng khung chạm
        if DANG == 2 and t > T_HUC:                          # nhát hai: bật lên, lộn một vòng tới trước, giáng xuống (khung trúng của game)
            P.move("day", 0.0, hoat.cv(t, [(T_HUC + 0.04, 0.0), (0.70, 105.0, "out"), (0.80, 112.0), (LAO2_DAP, 0.0, "in")]))
            P.rot("tam", -360.0 * ease((t - 0.62) / (LAO2_DAP - 0.62), "io") if t > 0.62 else 0.0)
            if 0.60 < t < LAO2_DAP - 0.02:
                mat_co(P, 0.6)
            if t > LAO2_DAP:
                b = math.exp(-(t - LAO2_DAP) / 0.09) * math.cos((t - LAO2_DAP) * 2 * math.pi / 0.22)
                P.scale("day", 1 + 0.22 * b, 1 - 0.26 * b)

    # ------------------------------------------------ cast: phóng hai tay
    def than_cast(t, P):
        """dáng thân của cast (không kể tay bay): idle khung 0 làm nền; lấy đà ngả ra sau, tay kéo về sau; đẩy tới khi phóng; giữ; đón
        tay về; hoà về idle."""
        dat(P, "idle_01", 0.0, mat=False)
        lui = hoat.cv(t, [(0, 0), (T_DA, 1.0, "out"), (T_PHONG["t"], -0.6, "in"), (0.55, -0.8, "out"), (TV - 0.10, -0.8),
                          (TV + 0.03, -0.2, "out"), (TV + 0.19, 0.0, "io"), (D_CAST, 0)])
        P.rot("tam", 9.0 * lui)
        P.move("day", -10.0 * lui, 0.0)
        bep = hoat.cv(t, [(0, 0), (T_DA, 1.0, "out"), (T_PHONG["t"], -0.7, "in"), (0.58, 0.0, "io"), (TV - 0.09, 0.0), (TV - 0.03, 0.5, "out"),
                          (TV + 0.11, 0.0, "io"), (D_CAST, 0)])
        P.scale("longdan_9", 1 - 0.08 * bep, 1 + 0.08 * bep)        # bẹp trên xương thân (trục x dọc), tay không méo theo
        keo = hoat.cv(t, [(0, 0), (T_DA, 1.0, "out"), (T_PHONG["p"], 1.0), (TV + 0.03, 1.0), (TV + 0.29, 0.0, "io"), (D_CAST, 0)])
        P.rot("longdan_7", -30.0 * keo)                # hai tay kéo về sau, lên cao (xoay chuỗi tay quanh thân)
        P.rot("longdan_8", 35.0 * keo)
        P.rot("longdan_12", 22.0 * keo)
        P.rot("longdan_0", -30.0 * keo)
        m = hoat.cv(t, [(0, 1.0), (0.10, 0.58, "out"), (T_DA, 0.58), (T_PHONG["t"], 1.15, "out"), (0.70, 1.0, "io"), (TV - 0.13, 1.0),
                        (TV - 0.05, 0.58, "out"), (TV + 0.13, 1.0, "io"), (D_CAST, 1.0)])
        mat_co(P, m)

    def f_cast(t, P):
        than_cast(t, P)
        W = None
        for ben, (s, b) in BAY_MANH.items():
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
                P.alpha[s] = 0.0
                if s == "longdan_0":
                    P.alpha["longdan_0~truoc"] = 0.0
                P.alpha[bb] = 1.0
            else:                                           # đã lắp lại: bản sao ẩn, GIỮ dáng cuối (khỏi quay ngược một vòng giữa hai khung)
                P.alpha[bb] = 0.0
            A = sk.W0[fb][:2, 2].copy()                    # chỗ rời thân (= tâm mảnh lúc phóng)
            g0 = _goc(sk.W0[bb])
            d = ((GOC_BAY[ben] - GOC_TAY[ben] + 90.0) % 180.0) - 90.0      # mảnh hai đầu nhọn: quay ít nhất cho một mũi chĩa tới
            v = far - A
            n = np.array([-v[1], v[0]]) / (float(np.hypot(*v)) or 1.0)       # pháp tuyến (vồng lên)
            if tt < t_toi:
                f = ease((tt - t0) / BAY, "in")
                pos = A + f * v + n * VONG_DI[ben] * math.sin(math.pi * f)
                ang = g0 + d * ease(min(1.0, (tt - t0) / 0.10), "out")
            elif tt < t_ve0:
                pos = far.copy()
                ang = g0 + d + 7.0 * math.sin((tt - t_toi) * 70.0) * math.exp(-(tt - t_toi) / 0.09)
            else:                                           # bay về, đáp ĐÚNG chỗ mảnh thật đang ở (thân đang chuyển động)
                if W is None:
                    W = sk.the_gioi(P)
                rb, Wl = REF[ben]
                Mt = W[rb] @ np.linalg.inv(Wl) @ sk.W0[bb]
                R_, gr = Mt[:2, 2], _goc(Mt)
                u = (tt - t_ve0) / VE
                e = ease(u, "io")
                pos = far * (1 - e) + R_ * e + n * VONG_VE[ben] * math.sin(math.pi * u)
                quay = 360.0 if (ben == "t" or A[0] < tam[0]) else -360.0
                g1 = gr + ((g0 + d - gr + 180.0) % 360.0 - 180.0)            # góc mảnh thật, gần góc đang bay nhất
                ang = (g0 + d) * (1 - e) + (g1 + quay) * e
            P.move(fb, float(pos[0] - A[0]), float(pos[1] - A[1]))
            P.rot(bb, float(ang - g0))

    # ------------------------------------------------ skill: chui đất → chạy ngầm → trồi lên húc → nhảy lùi
    a_ho, b_ho = info["ho"]
    hien_than = tuple(x for x in ["longdan_0", "longdan_0~truoc"] + SLOT_HO if x not in ("longdan_4", "longdan_6", "longdan_5"))

    def ho_hien(P, k):
        P.alpha["ho_sau"] = P.alpha["ho_truoc"] = 1.0 if k > 0.02 else 0.0
        P.scale("ho", max(0.02, k), max(0.02, k))

    def cat_bat(P, bat, nang=0.0):
        if bat:                                          # mặt nạ về đúng chỗ, đúng cỡ (tâm miệng hố); nang: nâng đáy (chạy ngầm: đáy phẳng ở mặt đất)
            P.move("cat_x", 0.0, CAT_SAU + nang)
            P.scale("cat_x", 1.0 / CAT_TI, 1.0 / CAT_TI)

    S2 = CD["skill_01_2"]
    # độ cao: đỉnh tinh thể giữa ở dáng gốc, gò đất cao bao nhiêu
    top = float(sk.atts["longdan_4"]["longdan_4"]["V"][:, 1].max())
    y_day, tam_y = info["y_day"], float(tam[1])
    go_cao = info["go_cao"]
    Y_VAY = go_cao + 55.0 - top                        # chạy ngầm: mũi tinh thể ló lên khỏi đỉnh gò chừng 38 đơn vị
    SX_DAO, SY_DAO = 0.80, 1.18

    def y_cham(sy):
        """dời `day` để mũi tinh thể (đã lộn ngược) vừa chạm đất khi day co sy."""
        return -sy * ((tam_y - y_day) - (top - tam_y))

    def dy_than(tau):
        """độ nâng thân (longdan_2) của skill_01_2 ở giây tau so với dáng gốc."""
        R = S2[1].get("longdan_2")
        if R is None:
            return 0.0
        x = min(tau * FPS, len(R) - 1)
        i0 = int(x)
        i1 = min(i0 + 1, len(R) - 1)
        return float(R[i0, 2] * (1 - (x - i0)) + R[i1, 2] * (x - i0))

    def f_skill(t, P):
        x_move = D_DAO * cao * ease((t - T_CHAY0) / (T_CHAY1 - T_CHAY0), "io") if t > T_CHAY0 else 0.0
        if t < T_TROI - 0.02:
            # ---- pha 1: lấy đà (thu tay, nheo mắt của skill_01_2), bật lên lộn ngược, cắm đầu xuống hố; rồi chạy ngầm
            if t < T_DOI:
                dat(P, "skill_01_2", min(t, T_LAT0) * (0.30 / T_LAT0))
                if t >= T_KHUAT:
                    for s in hien_than + ("longdan_4",):
                        P.alpha[s] = 0.0
                if t < T_LAT0:
                    k = ease(t / T_LAT0)
                    P.scale("day", 1 + 0.12 * k, 1 - 0.16 * k)
                else:
                    lat = ease((t - T_LAT0) / (T_LAT1 - T_LAT0), "io")
                    P.rot("tam", -180.0 * lat)
                    sx = hoat.cv(t, [(T_LAT0, 1.12), (0.40, 0.90, "out"), (T_LAT1, 0.95), (T_DAO, SX_DAO, "in"), (T_KHUAT, 0.78)])
                    sy = hoat.cv(t, [(T_LAT0, 0.84), (0.40, 1.16, "out"), (T_LAT1, 1.08), (T_DAO, SY_DAO, "in"), (T_KHUAT, 1.20)])
                    P.scale("day", sx, sy)
                    # bay lên rồi cắm xuống: dời `day` theo y (không dùng move: game nắn move theo quãng tới đối thủ)
                    yc = y_cham(SY_DAO)
                    y = hoat.cv(t, [(T_LAT0, 0.0), (0.46, yc + 70.0, "out"), (T_LAT1, yc + 40.0), (T_DAO, yc, "in"),
                                    (T_KHUAT, yc - 420.0, "in"), (T_DOI, yc - 520.0)])
                    P.move("day", 0.0, y)
            else:
                # dưới đất: thẳng đứng, chỉ mũi tinh thể giữa ló lên khỏi gò đất lúc chạy
                dat(P, "idle_01", 0.0, mat=False)
                for s in hien_than:
                    P.alpha[s] = 0.0
                if not (T_CHAY0 - 0.08 <= t < T_TROI - 0.12):
                    P.alpha["longdan_4"] = 0.0
                ra = ease((t - (T_CHAY0 - 0.08)) / 0.10, "out")
                P.move("day", 0.0, Y_VAY - 60.0 * (1 - ra) + 4.0 * math.sin((t - T_GO) * 2 * math.pi / 0.18))
                P.rot("tam", -6.0)                         # vây cá ngả về phía chạy
            cat_bat(P, t >= T_LAT1, nang=b_ho if t >= T_CHAY0 - 0.1 else 0.0)
            # hố ở chỗ cũ: mở khi mũi chạm đất, khép khi gò đất rời đi
            k = hoat.cv(t, [(T_DAO - 0.03, 0.0), (T_DAO + 0.06, 1.15, "out"), (T_DAO + 0.14, 1.0, "io"), (T_GO + 0.04, 1.0),
                            (T_CHAY0 + 0.06, 0.0, "in")])
            ho_hien(P, k)
            # gò đất nhô lên ở miệng hố rồi chạy ngầm tới đối thủ
            if t >= T_GO:
                g = hoat.cv(t, [(T_GO, 0.0), (T_GO + 0.10, 1.12, "out"), (T_GO + 0.18, 1.0, "io")])
                nh = 0.06 * math.sin((t - T_GO) * 2 * math.pi / 0.18) * (1.0 if t > T_CHAY0 else 0.4)
                P.alpha["go_dat"] = 1.0
                sx, sy = g * (1 + nh), g * (1 - nh)
                if t >= T_TROI - 0.14:                    # gò phồng to, rung trước khi nổ
                    u = ease((t - (T_TROI - 0.14)) / 0.12)
                    sx, sy = sx * (1 + 0.22 * u), sy * (1 + 0.40 * u)
                    P.rot("go", 5.0 * hoat.rung(t, T_TROI - 0.14, T_TROI, 1))
                P.scale("go", max(0.02, sx), max(0.02, sy))
                P.rot("go", 3.0 * math.sin((t - T_GO) * 2 * math.pi / 0.27))
            P.move("move", x_move, 0.0)
            return
        # ---- pha 2: trồi lên húc từ dưới (đoạn bật của skill_01_2), rơi về; rồi nhảy lùi về chỗ cũ
        P.move("move", D_DAO * cao * (1 - ease((t - T_LUI0) / (T_LUI1 - T_LUI0), "io")) if t > T_LUI0 else D_DAO * cao, 0.0)
        if DANG == 2 and t < T_TROI2 - 0.02:               # dạng 2, lần 1: trồi húc rồi rơi lại xuống hố
            tau = tmap(t, [(T_TROI - 0.02, 0.40), (T_HUC1, 0.50, "out"), (T_XUONG, 0.70, "lin")])
            dat(P, "skill_01_2", tau)
            P._g("longdan_2")[1] -= dy_than(tau)
            P.move("day", 0.0, hoat.cv(t, [(T_TROI - 0.02, -1.18 * top + 14.0), (T_TROI + 0.06, -0.62 * top, "out"),
                                           (T_HUC1, dy_than(0.50), "out"), (T_XUONG, -1.3 * top, "in")]))
            st = hoat.cv(t, [(T_TROI - 0.02, 0.80), (T_HUC1, 0.88, "out"), (T_HUC1 + 0.08, 1.04, "io"), (T_XUONG, 0.86)])
            P.scale("day", st, 2.0 - st)
            cat_bat(P, True)
            ho_hien(P, hoat.cv(t, [(T_TROI - 0.04, 0.0), (T_TROI + 0.05, 1.2, "out"), (T_TROI + 0.12, 1.0, "io")]))
            return
        t_troi = T_TROI2 if DANG == 2 else T_TROI
        them = 70.0 if DANG == 2 else 0.0                    # lần cuối của dạng 2 vọt cao hơn
        tau0 = 0.40
        tau = tmap(t, [(t_troi - 0.02, tau0), (T_SKILL_HUC, 0.50, "out"), (T_SKILL_HUC + 0.14, 0.66, "lin"), (T_DAP, 0.86, "in"),
                       (D_SKILL, 1.067, "io")])
        dat(P, "skill_01_2", tau)
        # trồi từ dưới đất: bỏ độ nâng thân của nguồn (bật quá nhanh), tự lái độ cao: mũi tinh thể phá đất trước, nửa thân ra, rồi vọt tới
        # đúng độ cao của nguồn ở khung húc (từ đó trả lại cho nguồn: liền mạch)
        if t < T_SKILL_HUC:
            P._g("longdan_2")[1] -= dy_than(tau)
            V = hoat.cv(t, [(t_troi - 0.02, -1.18 * top + 14.0), (t_troi + 0.06, -0.62 * top, "out"),
                            (T_SKILL_HUC, dy_than(0.50) + them, "out")])
            P.move("day", 0.0, V)
        elif them:
            P.move("day", 0.0, them * (1 - ease((t - T_SKILL_HUC) / (T_DAP - T_SKILL_HUC), "in")))
        st = hoat.cv(t, [(t_troi - 0.02, 0.80), (T_SKILL_HUC, 0.88, "out"), (T_SKILL_HUC + 0.08, 1.05, "io"), (T_DAP, 1.0)])
        P.scale("day", st, 2.0 - st)
        cat_bat(P, t < T_SKILL_HUC + 0.06)
        k = hoat.cv(t, [(T_TROI - 0.04, 0.0), (T_TROI + 0.05, 1.2, "out"), (T_TROI + 0.12, 1.0, "io"), (T_DAP, 1.0),
                        (T_DAP + 0.14, 0.0, "in")])
        if DANG == 2:                                      # hố nảy lần hai lúc đất nổ lần hai
            k *= 1 + 0.25 * math.exp(-((t - (T_TROI2 + 0.04)) / 0.05) ** 2)
        ho_hien(P, k)
        if t > T_DAP:                                      # chạm đất: bẹp rồi nảy
            b = math.exp(-(t - T_DAP) / 0.08) * math.sin((t - T_DAP) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.12 * b, 1 - 0.14 * b)
        if T_LUI0 < t < T_LUI1:                            # nhảy lùi về: vồng lên (dời day, không dùng move), ngả ra sau
            u = (t - T_LUI0) / (T_LUI1 - T_LUI0)
            P.move("day", 0.0, 70.0 * math.sin(math.pi * u))
            P.rot("tam", 10.0 * math.sin(math.pi * u))
        if t > T_LUI1:
            b = math.exp(-(t - T_LUI1) / 0.07) * math.sin((t - T_LUI1) * 2 * math.pi / 0.18)
            P.scale("day", 1 + 0.08 * b, 1 - 0.1 * b)

    # ------------------------------------------------ appear: nằm ngủ → mở mắt → bật bay lên → hạ về dáng đứng
    def f_appear(t, P):
        dat(P, "idle_01", 0.0, mat=False)
        Pn = P.copy()
        # dáng ngủ: bẹp sát đất, ngả ra sau, hai tay nằm rạp
        tho = math.sin(2 * math.pi * t / 1.1)
        Pn.scale("day", 1.14 + 0.025 * tho, 0.78 - 0.03 * tho)
        Pn.rot("tam", 7.0)
        Pn.rot("longdan_7", 30.0)
        Pn.rot("longdan_8", 20.0)
        Pn.rot("longdan_12", -30.0)
        Pn.rot("longdan_0", -20.0)
        Pn.move("day", 0.0, -6.0)
        w = ease((t - T_BAT_LEN + 0.12) / 0.30, "io")
        Q = pha(Pn, P, w)
        P.t.update(Q.t)
        P.att["longdan_7"], P.att["longdan_8"] = ("ngu_t", "ngu_p") if t < T_THUC else ("longdan_7", "longdan_8")
        # mở mắt: lờ đờ → chớp → mở to giật mình → về thường
        if t >= T_THUC:
            m = hoat.cv(t, [(T_THUC, 0.12), (1.22, 0.45, "out"), (1.30, 0.45), (1.34, 0.10, "in"), (1.40, 0.50, "out"), (1.46, 0.10, "in"),
                            (1.54, 1.20, "out"), (1.80, 1.20), (2.00, 1.0, "io")])
            mat_co(P, m)
        # giật mình nhún rồi bật bay lên, hạ về đất
        if t >= 1.48:
            y = hoat.cv(t, [(1.48, 0.0), (T_BAT_LEN, -6.0, "io"), (1.84, 95.0, "out"), (1.98, 88.0), (2.18, 0.0, "in"), (D_APPEAR, 0.0)])
            P.move("day", 0.0, y)
            sx = hoat.cv(t, [(1.48, 1.0), (T_BAT_LEN, 1.12, "io"), (1.70, 0.90, "out"), (1.86, 1.0, "io"), (2.18, 0.96), (2.24, 1.10, "out"),
                             (D_APPEAR, 1.0, "io")])
            P.scale("day", sx, 2.0 - sx)

    ev_cast = [(round(T_PHONG[k], 4), "phong", k) for k in BAY_MANH] + [(round(T_PHONG["t"] + BAY + 0.012, 3), "trung", "")] +               [(round(T_PHONG[k] + BAY + GIU + VE, 3), "ve", k) for k in BAY_MANH]
    ev_skill = [(T_DAO, "dao", ""), (T_CHAY0, "chay", ""), (T_TROI, "troi", ""), (T_SKILL_HUC, "trung", ""), (T_DAP, "cham_dat", "")]
    if DANG == 2:
        ev_skill += [(T_HUC1, "huc1", ""), (T_TROI2, "troi2", "")]
    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(0.2, "ngu", ""), (2.18, "cham_dat", "")]),
        Clip("idle", CD["idle_01"][0], f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(T_HUC, "trung", "")] if DANG == 1 else [(T_HUC, "huc1", ""), (LAO2_DAP, "trung", "")],
             trung=T_HUC if DANG == 1 else LAO2_DAP),
        Clip("cast", D_CAST, f_cast, ev=ev_cast, trung=T_PHONG["t"] + BAY + 0.012),
        Clip("skill", D_SKILL, f_skill, ev=ev_skill, trung=T_SKILL_HUC),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
    ]
    return clips, than_cast


GOC_TAY = {}                                            # góc thế giới trục dài của tay lúc rời thân (đầu mũi chĩa ra ngoài)
GOC_BAY = {}                                            # góc hướng bay (rig) từ chỗ rời thân tới far


def truc_tay(V, c_than):
    c = V.mean(0)
    _, _, vt = np.linalg.svd(V - c)
    ax = vt[0]
    if np.dot(ax, c - c_than) < 0:
        ax = -ax
    return math.degrees(math.atan2(ax[1], ax[0]))


REF = {}                                                # mảnh bay → (xương tham chiếu, ma trận thế giới của nó lúc phóng)


def them_tay_bay(sk, info, than_cast, cao):
    """xương far + fly_<k> (tâm mảnh lúc rời thân) + bay_<k> (dáng mảnh lúc rời thân) và slot bản sao (ẩn) cho mọi mảnh bay của chiêu mana.
    Bản sao là mảnh cứng trên bay_<k>: đỉnh = chỗ thế giới của mảnh thật ở khung phóng."""
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    far = sk.W0["far"][:2, 2]
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
        GOC_TAY[ben] = truc_tay(V, info["tam"])
        GOC_BAY[ben] = math.degrees(math.atan2(far[1] - c[1], far[0] - c[0]))


def nuong_idle(sk, c):
    """nướng idle như hoat.nuong nhưng GIỮ +360 của hai tay ở các khung cuối: dong_vong hoà các khung cuối về khung 0 làm tay quay ngược
    trọn một vòng (360 ≡ 0 nên khung cuối vẫn trùng khung 0 về hình)."""
    fr = hoat.nuong(sk, c)
    n = len(fr)
    for j in range(max(0, n - 8), n):
        P = khung.Pose()
        c.fn(min(c.dur, j / FPS), P)
        for b in (TAY["t"][1], TAY["p"][1]):
            if b in P.t:
                fr[j].t[b] = list(P.t[b])
    return fr


def nuong(sk, c):
    return nuong_idle(sk, c) if c.ten == "idle" else hoat.nuong(sk, c)


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    if DANG == 2:                                    # chiều cao game KHÔNG tính chùm gai vượt lên (kẻo thân dạng 2 bị co nhỏ hơn dạng 1):
        cao = CAO_GAME_2                             # thân dạng 1 đo 305; khai 285 → trên sân dạng 2 to hơn dạng 1 ~7 %, chùm gai nhô thêm
    them_tay_bay(sk, info, than_cast, cao)
    ve0 = soi.Ve(sk)
    clips, _ = lam_clip(sk, info, cao)
    print(f"chiều cao {cao:.0f}; tay rời thân {GOC_TAY}, hướng bay {GOC_BAY}")
    if a and a[0] == "kiem":
        # đo giật: góc riêng từng xương giữa hai khung nướng liền nhau, bước dời thế giới của tay / thân / mắt (slot đang hiện)
        for c in clips:
            fr = nuong(sk, c)
            xau = []
            al = lambda P, s: P.alpha.get(s, sk.slots[sk.si[s]]["alpha"])
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 35.0:
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for s, b in (("longdan_1", "longdan_8"), ("longdan_0", "longdan_0"), ("longdan_9", "longdan_9"), ("longdan_7", "longdan_16"),
                         ("bay_t", "bay_t"), ("bay_p", "bay_p"), ("go_dat", "go")):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if al(fr[i], s) > 0.5 and al(fr[i - 1], s) > 0.5 and d > 0.22 * cao:
                        xau.append(f"{i / 30:.2f}s {s} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:14]) + (" ..." if len(xau) > 14 else "")))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = nuong(sk, c)
        if ":" in a[2]:
            t0, t1, n = a[2].split(":")
            ts = list(np.linspace(float(t0), float(t1), int(n)))
        elif a[2].startswith("n="):
            ts = list(np.linspace(0, c.dur, int(a[2][2:])))
        else:
            ts = [float(x) for x in a[2].split(",")]
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.6
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            d = ImageDraw.Draw(im)
            d.text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, frames={"idle": nuong_idle(sk, clips[1])},
                  tieu_de=f"Tinh linh quặng sắt dạng {DANG} ({TEN_RIG}): tướng 3 đảo Kim", dang=DANG, so_dang=2, dung_yen=("cast",),
                  khong_khop=("attack",) if DANG == 2 else (),
                  lao=("skill",), far=("cast",), far_aim=("cast",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.8 if DANG == 1 else 4.6)


if __name__ == "__main__":
    main(sys.argv[1:])
