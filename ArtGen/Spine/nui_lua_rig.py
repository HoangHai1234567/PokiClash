# -*- coding: utf-8 -*-
"""Khủng long núi lửa đảo Hỏa (nui_lua; tướng thứ 10 đảo Hỏa, FINAL BOSS, suất lan_hoa): hình của mình chạy trên ĐÚNG rig của con gốc
monster_3654. Ghi chú: inbox/nui_lua_ghichu.md. Cách làm như hoa_ho_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ; thêm `move` (cha của mọi thứ), `mieng` (giữa hai hàm: chỗ tụ cầu lửa của chiêu mana), `ong_<nn>` (miệng
  từng ống núi lửa P_jiao_<nn>, trục x chĩa dọc ống ra ngoài: chỗ nhả khói và chỗ bắn đạn của chiêu cuối), `khoi_<nn>_<j>` (cụm khói).
- MẢNH: mỗi part của họ một ảnh lắp vào NGUYÊN lưới của họ. BỎ: `shadow`, 6 cụm khói `P_yan_*` và mắt `P_yanjing_02` (họ không bật ở
  clip nào). NL_GOC=1: ảnh part GỐC (chỉ để dựng và soi clip trong máy, KHÔNG đưa vào game); không đặt: ảnh của mình ở
  inbox/nui_lua_1/manh/part/<vùng>.png.
- CHUYỂN ĐỘNG: mẫu khung của họ (scan/sample.json, trường `l` đã áp IK chân) → lệch so với dáng gốc; clip của mình = co giãn giờ một
  clip nguồn + kênh riêng trên `move`, hai hàm, từng ống (các kênh này không làm chân rời đất):
    idle = idle_01, walk = run_01, hit = hit_01, die = die_01 (như họ);
    attack = skill_01_1 (lùi lấy đà rồi lao tới HÚC; sân tự kéo cả con lao tới đối thủ);
    cast   = skill_02 (ngả ra sau, ngẩng đầu) + HÁ MỒM tụ cầu lửa, rồi chồm tới nhả, giật lùi;
    skill  = skill_04: gồng hai nhịp, dộng xuống và BẺ các ống núi lửa mỗi ống một hướng, giữ dáng bắn loạt đạn (mỗi phát ống giật);
             đường bay của đạn do code game lo (sự kiện `ban` mang số ống);
    appear = rơi từ trên xuống, dộng đất (đoạn dộng của skill_03).
  aura   = khói nhả đều ở miệng các ống lớn (lặp chồng lên mọi clip).
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/nui_lua_rig.py        → inbox/nui_lua_1/rig/ (NL_GOC=1: rig_goc/)
    py -3 -I ArtGen/Spine/nui_lua_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → soi_<clip>.png (khung lớn nền xám)
"""
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import nui_lua as G  # noqa: E402
from hoa_ho_rig import gan_nguyen, ease, tmap, _goc  # noqa: E402

GOC = os.environ.get("NL_GOC") == "1"
TEN_RIG = "nui_lua_1"
D_PX = float(os.environ.get("NL_DPX", "0.5" if GOC else "0.6"))        # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~1000 đơn vị)
BO_SLOT = ("shadow", "P_yanjing_02")
MANH = os.path.join(G.BASE, "manh", "part")
TAN = 0.45
K_BUOC = float(os.environ.get("NL_BUOC", "0.5"))     # bản chibi: phần dao động thân của clip chạy giữ lại
FPS = 30.0
SPAN = 4.2
IMPACT = {"attack": (0.10, 0.6, 0.14), "cast": (0.14, 0.8, 0.18, "#ffd9a055"), "skill": (0.20, 1.0, 0.2, "#fff3c066")}

# ống nhả khói lúc đứng (số cụm khói, cỡ) và ống bắn ở chiêu cuối (thứ tự bắn); số = đuôi tên slot P_jiao_<nn>
KHOI = {"09": (3, 1.0), "10": (3, 0.95), "02": (3, 0.9), "14": (2, 0.85), "15": (2, 0.7), "13": (2, 0.8), "01": (1, 0.55), "03": (1, 0.6)}
KHOI["cc"] = (3, 1.3)                                # miệng núi lửa CHÍNH trên đỉnh lưng (P_beijia_03; thiết kế "sừng")
MIENG_CHINH = (772.0, 160.0)                         # tâm miệng núi lửa chính trên sơ đồ bố cục (nui_lua_bo_cuc.MIENG_CHINH)
KHOI_CK = 2.4                                        # chu kỳ aura (giây)
BAN = ["09", "14", "02", "10", "13", "15", "03", "09", "04", "02", "14", "10", "01", "13", "06", "09"]   # 16 phát
# bẻ thêm (độ) cho các ống nhỏ mà họ để yên ở skill_04: mỗi ống một hướng
BE_THEM = {"bone33": 34.0, "bone34": 46.0, "bone38": 26.0, "bone30": 22.0, "bone31": 30.0, "bone42": 14.0, "bone43": -16.0, "bone44": -30.0}


# DẠNG 1 chibi (NL_DANG=non; người dùng 2026-11-14: "Ok làm dạng 1 đi"). Như hổ con: đổi tỉ lệ ngay trên rig trước (đầu to và ngẩng lên,
# chân ngắn + cả thân hạ xuống, ít ống núi lửa và ống ngắn, núi lưng nhỏ) → hình bố cục → concept → người dùng chọn → mới làm mảnh.
# NL_DANG=chibi: dạng 1 VẼ RIÊNG (người dùng chọn concept A): xương, tỉ lệ, clip như `non`; mảnh là hình cắt từ concept chibi, lắp bằng
# nui_lua_chibi.lap (lưới riêng bám xương của họ; chân có ba xương riêng + IK như hổ con). Không vẽ mảnh nào của dạng lớn.
MA_NON = os.environ.get("NL_MA", "nui_lua_non")      # thư mục inbox của dạng đang dựng: nui_lua_non (dạng 1) hoặc nui_lua_2 (dạng 2)
CHIBI = os.environ.get("NL_DANG") == "chibi" and not GOC
NON = (os.environ.get("NL_DANG") == "non" or CHIBI) and not GOC
if CHIBI:                                             # tỉ lệ = đúng các số đã dựng hình bố cục (và concept) của dạng này
    _bc = json.load(open(os.path.join(HERE, "inbox", MA_NON, "mau", "bo_cuc_chibi.json")))["chibi"]
    for _k in ("NL_KDAU", "NL_CO", "NL_CHAN", "NL_KONG", "NL_KLUNG"):
        os.environ.setdefault(_k, str(_bc[_k]))
    import nui_lua_chibi as _NC                       # bảng của dạng đang dựng (theo NL_MA): ống giữ lại, khói, thứ tự bắn
    os.environ["NL_ONG"] = ",".join(_NC.ONG)
K_DAU = float(os.environ.get("NL_KDAU", "1.5"))      # phóng xương đầu bone7
G_CO = float(os.environ.get("NL_CO", "48"))          # ngẩng cổ (độ, xương bone6b): con gốc cúi gằm, con non phải lộ mặt
K_CHAN = float(os.environ.get("NL_CHAN", "0.8"))    # tỉ lệ chân (tính trên chân có hông thấp nhất; chân khác rút cùng một quãng)
K_ONG = float(os.environ.get("NL_KONG", "0.6"))      # các ống còn giữ: ngắn lại
K_LUNG = float(os.environ.get("NL_KLUNG", "0.82"))   # các phiến núi lưng
ONG_NON = ("09", "02", "14", "03")                   # dạng 1 chỉ còn bốn ống + miệng núi lửa chính
if os.environ.get("NL_ONG"):                          # dạng 2 (thiếu niên): danh sách ống giữ lại riêng, vd NL_ONG=09,10,02,14,13,03
    ONG_NON = tuple(os.environ["NL_ONG"].split(","))
XUONG_ONG = {"09": "bone40", "10": "bone41", "02": "bone39", "14": "bone43", "13": "bone44", "15": "bone42", "03": "bone30",
             "04": "bone31", "06": "bone33", "07": "bone34", "01": "bone38"}
ONG_XUONG_NON = tuple(XUONG_ONG[k] for k in ONG_NON if k in XUONG_ONG)
K_SUNG = float(os.environ.get("NL_SUNG", "0"))       # > 0: hình bố cục dạng non vẫn có hai sừng, thu nhỏ còn K_SUNG lần
CHAN_GOC = ("bone10", "bone14", "bone18", "bone22")  # gốc bốn chân
LUNG_XUONG = ("bone26", "bone27", "bone28", "bone29")
if NON:
    KHOI = {k: v for k, v in KHOI.items() if k in ONG_NON or k == "cc"}
    BAN = [k for k in BAN if k in ONG_NON][:12] or list(ONG_NON)
if CHIBI:
    TEN_RIG = MA_NON
    KHOI, BAN, IMPACT = dict(_NC.KHOI), list(_NC.BAN), dict(_NC.IMPACT)


# ---------------------------------------------------------------- nạp
def nap_goc():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, I, scan


def ti_le_atlas(D):
    """px ảnh vùng của họ cho mỗi đơn vị rig (đo trên lưới tảng đá lưng lớn nhất)."""
    _, imgs, _ = G.nap("att_goc.json")
    a = next(x for x in D["atts"] if x["slot"] == "P_duzi")
    im = imgs[a["region"]]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    V = np.array(a["xy"], float).reshape(-1, 2)
    T = np.array(a["tris"]).reshape(-1, 3)

    def dt(P):
        e1, e2 = P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]]
        return np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]).sum() / 2

    return float(math.sqrt(dt(U) / dt(V)))


def anh_part(a, a_tl):
    r = a["region"]
    pth = os.path.join(MANH, r + ".png")
    if GOC:
        g = G.part_goc(a)
        kq = D_PX / a_tl
    elif os.path.exists(pth):
        import nui_lua_manh as M
        g = Image.open(pth).convert("RGBA")
        kq = D_PX / (a_tl * M.zs()[r])
    else:
        raise SystemExit("thiếu ảnh part " + pth + " (NL_GOC=1: da gốc)")
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


def anh_khoi(k=0):
    """cụm khói thứ k: ghép từ chính ảnh hạt khói của game (Assets/03 Art/Fx/Hat: hat_ssolid_<i> làm viền mực, hat_sblob_<i> nhuộm xám) để
    khói trong rig cùng nét với khói của lớp hạt; thiếu ảnh thì vẽ cụm mây giữ chỗ. Ảnh riêng: inbox/nui_lua_1/manh/khoi_<k>.png."""
    w = int(230 * D_PX)
    pth = os.path.join(G.BASE, "manh", f"khoi_{k}.png")
    hat = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx", "Hat"))
    i = (0, 2, 1)[k % 3]
    if os.path.exists(pth):
        g = Image.open(pth).convert("RGBA")
        kq = w / max(g.size)
        return anh.loang_mau(g.convert("RGBa").resize((round(g.width * kq), round(g.height * kq)), Image.LANCZOS).convert("RGBA"))
    if os.path.exists(os.path.join(hat, f"hat_sblob_{i}.png")):
        mau = ((104, 98, 98), (132, 126, 124), (84, 78, 80))[k % 3]
        vien = Image.open(os.path.join(hat, f"hat_ssolid_{i}.png")).convert("RGBA").resize((w, w), Image.LANCZOS)
        ruot = Image.open(os.path.join(hat, f"hat_sblob_{i}.png")).convert("RGBA").resize((w - 8, w - 8), Image.LANCZOS)
        A = np.asarray(vien).astype(np.float32)
        out = np.zeros((w, w, 4), np.float32)
        out[..., :3] = (43, 33, 24)
        out[..., 3] = A[..., 3]
        R = np.zeros((w, w, 4), np.float32)
        Rr = np.asarray(ruot).astype(np.float32)
        R[4:w - 4, 4:w - 4, 3] = Rr[..., 3]
        R[4:w - 4, 4:w - 4, :3] = Rr[..., :3] / 255.0 * np.array(mau, np.float32)
        a = R[..., 3:4] / 255.0
        out[..., :3] = out[..., :3] * (1 - a) + R[..., :3] * a
        out[..., 3] = np.maximum(out[..., 3], R[..., 3])
        return anh.loang_mau(Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA"))
    S = 4
    im = Image.new("RGBA", (w * S, w * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cuc = [(0.50, 0.56, 0.30), (0.30, 0.60, 0.20), (0.70, 0.60, 0.21), (0.40, 0.36, 0.20), (0.62, 0.34, 0.19)]
    for dd, mau in ((0.035, (43, 33, 24, 255)), (0.0, (132, 128, 132, 255))):
        for x, y, r in cuc:
            d.ellipse([(x - r - dd) * w * S, (y - r - dd) * w * S, (x + r + dd) * w * S, (y + r + dd) * w * S], fill=mau)
    return anh.loang_mau(im.resize((w, w), Image.LANCZOS))


def dung():
    D, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    a_tl = ti_le_atlas(D)
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    goc0 = {}
    DAT0 = -21.4                                      # mặt đất (đáy móng) ở dáng gốc
    ha = (1 - K_CHAN) * min(Wc[n][1, 2] - DAT0 for n in CHAN_GOC) if NON else 0.0
    for b in IB:
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        if b["inherit"]:                              # không thừa hưởng xoay của cha: góc riêng tính từ ma trận thế giới
            g[2] = _goc(Wc[b["name"]]) - _goc(Wc[cha])
        goc0[b["name"]] = g
        kd, n = 1.0, b["name"]
        gx, gy, gg = g[0], g[1], g[2]
        if NON:
            if n in CHAN_GOC:                         # mọi chân rút cùng một quãng `ha`, cả thân hạ xuống đúng quãng đó: bàn chân vẫn chạm đất
                kd = 1 - ha / (Wc[n][1, 2] - DAT0)
            elif n == "bone3":
                d = np.linalg.solve(Wc[cha][:2, :2], np.array([0.0, -ha]))
                gx, gy = gx + float(d[0]), gy + float(d[1])
            elif n == "bone7":
                kd = K_DAU
            elif n == "bone6b":                       # bone6 còn mang hai phiến núi lưng (bone27, bone28): ngẩng ở bone6b
                gg += G_CO
            elif n in ONG_XUONG_NON:
                kd = K_ONG
            elif n == "bone26":                       # phiến sau gáy là con của xương đầu: bù lại phần phóng của đầu
                kd = K_LUNG / K_DAU
            elif n in LUNG_XUONG:
                kd = K_LUNG
        sk.xuong(n, "move" if cha == "root" else cha, gx, gy, goc=gg, dai=b["len"], sx=g[3] * kd, sy=g[4] * kd)
    WP = None
    if CHIBI:                                         # dáng nghỉ của bản chibi = concept, vẽ ở dáng khung 0 idle của rig với tỉ lệ này
        import nui_lua_chibi as NC
        P0 = hoat.nuong(sk, lam_clip(sk, dict(scan=scan, IB=IB, ten=ten, goc0=goc0, slots=[], dat_y=0.0, ong={}, khoi=[]))[1])[0]
        WP = sk.the_gioi(P0)
        bc = json.load(open(os.path.join(NC.BASE, "mau", "bo_cuc_chibi.json")))

        def cpx(q):                                   # px concept → thế giới rig
            return np.array([bc["box"][0] + q[0] / bc["sc"], bc["box"][3] - q[1] / bc["sc"]])

        NC.xuong_ong(sk, WP, cpx)                     # xương riêng ở chân từng tháp ống
        WP = sk.the_gioi(P0)
    by = {a["slot"]: a for a in D["atts"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_SLOT and not s["name"].startswith("P_yan_")
             and s["name"] in by and by[s["name"]].get("region")]
    if NON:
        slots = [s for s in slots if not (s.startswith("P_jiao_") and s[-2:] not in ONG_NON)]
    tong = [0, 0]

    def xuong_cua(slot):
        nang = {}
        for ws in by[slot].get("w") or []:
            for k, w in ws:
                nang[ten[k]] = nang.get(ten[k], 0.0) + w
        return max(nang, key=nang.get) if nang else ten[by[slot]["bone"]]

    def them(ten_x, xg, cho, goc_tg):
        M = WP[xg] if CHIBI else Wc[xg]               # chibi: điểm cho theo dáng khung 0 idle của rig mình; còn lại: dáng gốc của họ
        lp = np.linalg.solve(M, np.array([cho[0], cho[1], 1.0]))
        sk.xuong(ten_x, xg, float(lp[0]), float(lp[1]), goc=goc_tg - _goc(M))

    # miệng từng ống: trục chính (PCA) của lưới ống, chĩa ra xa tâm thân
    tam = np.array([-60.0, 380.0])
    ong = {}
    for s in slots:
        m = re.match(r"P_jiao_(\d+)$", s)
        if not m:
            continue
        V = np.array(by[s]["xy"], float).reshape(-1, 2)
        c = V.mean(0)
        _, _, vt = np.linalg.svd(V - c)
        ax = vt[0] if np.dot(vt[0], c - tam) >= 0 else -vt[0]
        if m.group(1) in ("13", "14", "15", "09", "10", "02", "03", "04", "06") and ax[1] < 0:
            ax = -ax                                  # ống trên lưng luôn chĩa lên
        pr = (V - c) @ ax
        dinh = V[pr > pr.max() - 0.18 * (pr.max() - pr.min())].mean(0)
        ong[m.group(1)] = (xuong_cua(s), dinh, math.degrees(math.atan2(ax[1], ax[0])), float(pr.max() - pr.min()))

    # dáng idle0 → dáng gốc (cho những thứ đặt theo sơ đồ bố cục, vốn dựng ở dáng idle0)
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    W0 = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D0["bones"]}
    Hh = json.load(open(os.path.join(G.MAU, "bo_cuc.json"), encoding="utf-8"))

    def ve_goc(xg, p_tg0):
        """điểm thế giới ở dáng idle0, bám xương xg → thế giới ở dáng gốc + góc xoay (độ) của phép đổi."""
        Tm = Wc[xg] @ np.linalg.inv(W0[xg])
        q = Tm @ np.array([p_tg0[0], p_tg0[1], 1.0])
        return q[:2], _goc(Tm)

    if CHIBI:                                         # miệng núi lửa và ba ống: đúng chỗ trên concept
        ong = {nn: (xg if nn == "cc" else "ong_p_" + nn, cpx(q), g, 200.0) for nn, (xg, q, g) in NC.MIENG_ONG.items()}
    else:
        xg_cc = xuong_cua("P_beijia_03")
        cc, g_cc = ve_goc(xg_cc, ((MIENG_CHINH[0] - Hh["_ox"]) / Hh["_sc"], (Hh["_oy"] - MIENG_CHINH[1]) / Hh["_sc"]))
        ong["cc"] = (xg_cc, cc, 90.0 + g_cc, 300.0)

    def them_sung(t):
        """sừng húc (mảnh THÊM của thiết kế mình): ảnh manh/part/<t>.png, cứng theo xương sọ."""
        import nui_lua_manh as Mm
        Sg = json.load(open(os.path.join(G.MAU, "sung.json"), encoding="utf-8"))[t]
        g = Image.open(os.path.join(MANH, t + ".png")).convert("RGBA")
        kq = D_PX / (Mm.A_TL * Mm.zs()[t])
        g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
        sk.anh(t, anh.loang_mau(g))
        x0, y0, x1, y1 = Sg["hop"]
        c, gq = ve_goc(Sg["xuong"], ((x0 + x1) / 2, (y0 + y1) / 2))
        sk.slot(t, Sg["xuong"], t)
        sk.manh(t, t, khung.Dat(float(c[0]), float(c[1]), goc=gq, ti=(K_SUNG if NON and K_SUNG > 0 else 1.0) / D_PX), xuong=Sg["xuong"])

    for k in range(3):
        sk.anh(f"khoi_{k}", anh_khoi(k))
    dem_k = 0
    khoi = []
    # khói vẽ SAU các ống (đặt slot trước): bốc lên từ sau miệng ống
    for nn, (so, co) in KHOI.items():
        xg, dinh, goc_tg, dai = ong[nn]
        them("ong_" + nn, xg, dinh, goc_tg)
        for j in range(so):
            b = f"khoi_{nn}_{j}"
            sk.xuong(b, "ong_" + nn, 0.0, 0.0)
            sk.slot(b, b, f"khoi_{dem_k % 3}")
            p0 = sk.W0[b][:2, 2]                      # chỗ xương thật (dạng 1 đổi tỉ lệ nên khác chỗ ở dáng gốc của họ)
            sk.manh(b, f"khoi_{dem_k % 3}", khung.Dat(float(p0[0]), float(p0[1])), xuong=b)
            dem_k += 1
            khoi.append((b, nn, j, so, co))
    if not GOC and (not NON or (K_SUNG > 0 and not CHIBI)):
        them_sung("sung_xa")                          # sừng xa: sau mọi mảnh
    for s in ([] if CHIBI else slots):
        a = by[s]
        r = a["region"]
        sk.slot(s, "move", r)
        if r not in sk.images:
            sk.anh(r, anh_part(a, a_tl))
        L = gan_nguyen(sk, s, r, a, ten, Wc)
        tong[0] += L.n
        tong[1] += len(L.tris)
        if s == "P_xiae_1" and not GOC and (not NON or (K_SUNG > 0 and not CHIBI)):
            them_sung("sung_gan")                     # sừng gần: ngay trước sọ và hàm
    for nn, (xg, dinh, goc_tg, dai) in ong.items():
        if "ong_" + nn not in sk.bi:
            them("ong_" + nn, xg, dinh, goc_tg)
    # miệng: giữa hai hàm, phía trước họng; bám xương đầu (cha của hai hàm) nên há mồm không làm nó lệch
    Vh = np.array(by["P_houlong"]["xy"], float).reshape(-1, 2)
    Vx = np.array(by["P_xiae_1"]["xy"], float).reshape(-1, 2)
    mui = Vx[np.argmax(Vx[:, 0] - Vx[:, 1])]            # mũi hàm dưới (xa nhất về phía phải – dưới)
    hong = Vh.mean(0)
    cho = hong + 0.55 * (mui - hong) + np.array([10.0, 45.0])
    if CHIBI:
        them("mieng", "bone7", cpx(NC.MIENG[0]), NC.MIENG[1])
        tong = NC.lap(sk, by, ten, Wc, P0, D_PX, luoi, anh, cpx)
    else:
        them("mieng", "bone7", cho, math.degrees(math.atan2(mui[1] - hong[1], mui[0] - hong[0])) + 22.0)
    dat_y = min(np.array(by[s]["xy"], float).reshape(-1, 2)[:, 1].min() for s in slots if "jiaozhi" in s)
    for e, m in (("trung", "khung trúng"), ("huc", "attack: đầu húc tới"), ("tu", "cast: há mồm, bắt đầu tụ cầu lửa"),
                 ("nha", "cast: nhả cầu lửa"), ("gong", "skill: bắt đầu gồng"), ("be", "skill: dộng xuống, bẻ các ống núi lửa"),
                 ("ban", "skill: một ống bắn (chuỗi = số ống, xương ong_<số>)"), ("het_ban", "skill: hết loạt bắn"),
                 ("dap_dat", "appear: dộng xuống sàn")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác" + ("" if CHIBI else " (lưới của họ)") + f"; atlas của họ {a_tl:.3f} px / đơn vị; "
          f"mặt đất y = {dat_y:.1f}; {len(ong)} ống: " + " ".join(f"{k}@{v[0]}" for k, v in sorted(ong.items())))
    return sk, dict(scan=scan, IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], dat_y=dat_y, ong=ong, khoi=khoi)


# ---------------------------------------------------------------- chuyển động
def chuyen_dong(sk, info):
    S = json.load(open(os.path.join(info["scan"], "sample.json"), encoding="utf-8"))
    IB, ten, goc0 = info["IB"], info["ten"], info["goc0"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    out = {}
    ref = None
    for clip in ["idle_01"] + [c for c in S if c != "idle_01"]:
        fr = S[clip]["frames"]
        L = np.array([F["l"] for F in fr], float)                     # (khung, xương, 7): x, y, xoay, tỉ lệ x, y, xô
        Wm = np.array([F["m"] for F in fr], float)                    # (khung, xương, 4): a, b, c, d thế giới
        res = {}
        for i in ids:
            g = goc0[ten[i]]
            rot = L[:, i, 2]
            if IB[i]["inherit"]:
                p = IB[i]["parent"]
                rot = np.degrees(np.arctan2(Wm[:, i, 2], Wm[:, i, 0]) - np.arctan2(Wm[:, p, 2], Wm[:, p, 0]))
            A = np.stack([rot - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            moc = ref[ten[i]][0, 0] if ref is not None and ten[i] in ref else 0.0
            A[:, 0] -= 360.0 * round((A[0, 0] - moc) / 360.0)
            res[ten[i]] = A
        if ref is None:
            ref = res
        out[clip] = (float(S[clip]["dur"]), res, len(fr))
    return out


# giờ của mình → giờ clip nguồn
M_ATTACK = [(0.0, 0.0), (0.16, 0.13, "out"), (0.40, 0.47, "lin"), (0.50, 0.60, "in"), (0.66, 0.70, "out"), (1.15, 1.333, "io")]
T_HUC = 0.50
# cast: ngả ra sau + ngẩng đầu (0,30 → 0,62 của skill_02) giữ trôi trong lúc tụ; chồm xuống (0,91) lúc nhả; về
T_TU, T_NHA = 0.30, 1.05
M_CAST = [(0.0, 0.0), (0.30, 0.34, "io"), (T_NHA - 0.07, 0.68, "lin"), (T_NHA + 0.05, 0.80, "in"), (1.32, 0.66, "out"), (1.85, 0.0, "io")]
# skill: 0 → 1,64 gồng hai nhịp như họ (nén giờ còn 1,45); dộng + bẻ ống 1,45 → 1,70; GIỮ dáng bẻ (1,91 → 2,55 của họ) trong lúc bắn; về
T_BE, T_BAN0 = 1.52, 1.62
BAN_CACH = 0.07
T_HET = T_BAN0 + len(BAN) * BAN_CACH + 0.10
M_SKILL = [(0.0, 0.0), (1.28, 1.64, "lin"), (T_BE, 1.92, "in"), (T_HET, 2.55, "lin"), (T_HET + 0.62, 3.0, "io")]
D_SKILL = M_SKILL[-1][0]
NGANG = (float(os.environ.get("NL_NG0", "14")), float(os.environ.get("NL_NG1", "30")))   # độ ngẩng đầu ở cast: xương cổ, xương đầu
M_APPEAR = [(0.0, 0.62), (0.32, 0.91, "in"), (0.90, 1.45, "out"), (1.30, 2.0, "io")]
T_DAP = 0.32


def lam_clip(sk, info, cao=1000.0):
    CD = chuyen_dong(sk, info)
    ong = info["ong"]

    def dat(P, goc, tau, lap=False):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))

    def dam(P, a):
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def rung(t, t0, t1, bien, ra=0.12):
        if t0 <= t <= t1:
            k = int((t - t0) * FPS) // 2
            return bien * (1 if k % 2 == 0 else -1) * min(1.0, (t1 - t) / ra)
        return 0.0

    def ha(P, k, lech=0.0):
        """há mồm: hàm trên ngửa lên, hàm dưới trễ xuống (k = 0..1), lech = độ rung."""
        P.rot("bone9", 20.0 * k + lech)
        P.rot("bone8", -24.0 * k - lech)

    def giat_ong(P, nn, u):
        """một ống giật lúc bắn: co dọc ống 2 khung rồi bật quá đà, về (u = giây sau phát bắn)."""
        xg = ong[nn][0]
        if u < 0 or u > 0.30 or not (re.match(r"bone(3[0-4]|3[89]|4[0-4])$", xg) or xg.startswith("ong_p_")):
            return
        k = -0.16 * (1 - u / 0.06) if u < 0.06 else 0.07 * math.sin(math.pi * (u - 0.06) / 0.24) * (1 - (u - 0.06) / 0.24)
        if u < 0.06:
            k = -0.16 * math.sin(math.pi * min(1.0, u / 0.045) * 0.5) if u < 0.045 else -0.16 * (1 - (u - 0.045) / 0.015)
        P.scale(xg, 1.0 + k, 1.0 - 0.5 * k)

    def f_idle(t, P):
        dat(P, "idle_01", t, True)

    nho_walk = {}

    def f_walk(t, P):
        dat(P, "run_01", t, True)
        if CHIBI:
            # như hổ con: thân nhún quanh DÁNG ĐỨNG idle (khung 0) với K_BUOC lần dao động của run_01; chân do IK lo (bước tự viết, bám đất)
            if not nho_walk:
                dur = CD["run_01"][0]
                n = int(round(dur * FPS))
                tong = {}
                for k in range(n):
                    Q = khung.Pose()
                    dat(Q, "run_01", k / FPS, True)
                    for b, g in Q.t.items():
                        s_ = tong.setdefault(b, [0.0] * 5)
                        for q in range(5):
                            s_[q] += g[q] / n
                    for b in tong:
                        if b not in Q.t:
                            tong[b][3] += 1.0 / n
                            tong[b][4] += 1.0 / n
                Q0 = khung.Pose()
                dat(Q0, "idle_01", 0.0, True)
                nho_walk["tb"], nho_walk["idle"] = tong, Q0.t
            tb, i0 = nho_walk["tb"], nho_walk["idle"]
            moi = {}
            for b in set(P.t) | set(tb) | set(i0):
                if b == "move":
                    continue
                g = P.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                m = tb.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                z = i0.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                moi[b] = [z[0] + K_BUOC * (g[0] - m[0]), z[1] + K_BUOC * (g[1] - m[1]), z[2] + K_BUOC * (g[2] - m[2]),
                          z[3] * (1 + K_BUOC * (g[3] / (m[3] or 1.0) - 1)), z[4] * (1 + K_BUOC * (g[4] / (m[4] or 1.0) - 1))]
            mv = P.t.get("move")
            P.t.clear()
            P.t.update(moi)
            if mv:
                P.t["move"] = mv

    def f_hit(t, P):
        dat(P, "hit_01", t)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", t)
        for b, *_ in info["khoi"]:
            P.alpha[b] = float(np.clip(1.0 - t / 0.25, 0.0, 1.0))      # núi lửa tắt: khói ngừng
        dam(P, float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0)))

    def f_attack(t, P):
        dat(P, "skill_01_1", tmap(t, M_ATTACK))
        k = math.exp(-((t - (T_HUC + 0.03)) / 0.05) ** 2)
        P.scale("move", 1 + 0.04 * k, 1 - 0.035 * k)                   # dồn theo chiều húc đúng khung chạm
        # LAO TỚI HÚC (người dùng: "tấn công thường lao vào húc đối thủ"): xương `move` lùi lấy đà rồi phóng tới, đỉnh ở đúng khung húc; sân
        # nắn đỉnh lao này tới 72 % quãng tới đối thủ (AolaSticker.Lunge; không có quãng lao trên `move` thì sân chỉ nhún 35 %).
        t_ve = T_HUC + 0.14
        if t < 0.40:
            lao = -0.07 * ease((t - 0.12) / 0.14)
        elif t < T_HUC:
            lao = -0.07 + 0.67 * ease((t - 0.40) / (T_HUC - 0.40), "in")
        elif t < t_ve:
            lao = 0.60
        else:
            lao = 0.60 * (1 - ease((t - t_ve) / max(0.05, M_ATTACK[-1][0] - 0.05 - t_ve)))
        P.move("move", cao * lao + rung(t, T_HUC + 0.02, T_HUC + 0.2, 6.0), 0.0)
        # đầu cúi ghìm lúc lấy đà, hất lên lúc húc
        P.rot("bone7", -9.0 * hoat.bao(t, 0.10, 0.44, 0.12, 0.05) + 16.0 * math.exp(-((t - (T_HUC + 0.02)) / 0.07) ** 2))

    def f_cast(t, P):
        dat(P, "skill_02", tmap(t, M_CAST))
        mo = hoat.bao(t, T_TU - 0.06, T_NHA + 0.16, 0.20, 0.12)        # há dần lúc tụ, ngậm lại sau khi nhả
        ng = hoat.bao(t, T_TU - 0.14, T_NHA + 0.30, 0.26, 0.30)        # NGẨNG đầu cho mồm chĩa về đối thủ (con gốc cúi gằm)
        giat = math.exp(-((t - (T_NHA + 0.03)) / 0.05) ** 2)
        kn = _NC.K_NGANG if CHIBI else 0.3 if NON else 1.0             # con non đã ngẩng sẵn: chỉ ngẩng thêm một ít
        P.rot("bone6b", NGANG[0] * kn * ng - 4.0 * giat)
        P.rot("bone7", NGANG[1] * kn * ng - 7.0 * giat)
        ha(P, mo + 0.25 * math.exp(-((t - T_NHA) / 0.04) ** 2), rung(t, T_TU + 0.15, T_NHA - 0.03, 1.4, ra=0.2))
        # giật lùi cả thân đúng lúc nhả
        k = math.exp(-((t - (T_NHA + 0.04)) / 0.06) ** 2)
        P.move("move", -34.0 * k + rung(t, T_TU + 0.2, T_NHA - 0.02, 2.5, ra=0.2), 0.0)
        P.scale("move", 1 - 0.03 * k, 1 + 0.03 * k)

    def f_skill(t, P):
        dat(P, "skill_04", tmap(t, M_SKILL))
        be = hoat.bao(t, T_BE - 0.10, T_HET + 0.05, 0.14, 0.45)
        for b, a in BE_THEM.items():
            P.rot(b, a * be)
        for i, nn in enumerate(BAN):
            giat_ong(P, nn, t - (T_BAN0 + i * BAN_CACH))
        P.move("move", rung(t, T_BE, T_HET, 3.0, ra=0.25), -6.0 * be)
        ha(P, 0.55 * hoat.bao(t, T_BE - 0.05, T_HET, 0.10, 0.3))        # gầm trong lúc bắn

    def f_appear(t, P):
        dat(P, "skill_03", tmap(t, M_APPEAR))
        u = min(1.0, t / T_DAP)
        P.move("move", 0.0, 1.15 * cao * (1 - u * u))
        k = math.exp(-((t - (T_DAP + 0.04)) / 0.06) ** 2)
        P.scale("move", 1 + 0.05 * k, 1 - 0.06 * k)
        dam(P, ease(t / 0.12))

    def f_aura(t, P):
        for b, nn, j, so, co in info["khoi"]:
            so_nn = int(nn) if nn.isdigit() else 5
            pha = (so_nn * 0.377) % 1.0
            u = (t / KHOI_CK + pha + j / so) % 1.0                    # tuổi cụm khói 0..1
            dai = 210.0 * co
            P.move(b, dai * (-0.06 + 1.25 * (1 - (1 - u) ** 1.7)), 26.0 * co * math.sin(u * 5.0 + so_nn) * u)
            s = co * (0.30 + 0.85 * u ** 0.7)
            P.scale(b, s, s)
            P.rot(b, 40.0 * u * (1 if so_nn % 2 else -1))
            P.alpha[b] = float(min(1.0, u / 0.10) * (1.0 - max(0.0, (u - 0.45) / 0.55)) ** 1.3)

    ev_skill = [(0.05, "gong", ""), (T_BE, "be", "")] + [(round(T_BAN0 + i * BAN_CACH, 3), "ban", nn) for i, nn in enumerate(BAN)] + \
               [(round(T_HET, 3), "het_ban", "")]
    clips = [
        Clip("appear", M_APPEAR[-1][0], f_appear, ev=[(T_DAP, "dap_dat", "")]),
        Clip("idle", CD["idle_01"][0], f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", M_ATTACK[-1][0], f_attack, ev=[(T_HUC, "huc", ""), (T_HUC, "trung", "")]),
        Clip("cast", M_CAST[-1][0], f_cast, ev=[(T_TU, "tu", ""), (T_NHA, "nha", "")], trung=T_NHA),
        Clip("skill", D_SKILL, f_skill, ev=ev_skill, trung=T_BAN0),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
        Clip("aura", KHOI_CK, f_aura, loop=True),
    ]
    if CHIBI and getattr(sk, "chan_nl", None):        # bản chibi: bốn trụ chân có xương riêng, đặt sau khi hàm clip đã đặt thân
        import nui_lua_chibi as NC

        def boc(f, ten_c, dur):
            def g(t, P):
                f(t, P)
                r8 = P.t["bone8"][2] if P.t.get("bone8") else 0.0     # hàm của mình quay quanh khớp hàm, theo góc xương hàm của họ;
                if r8 < -0.01:                                          # không nghiến quá dáng nghỉ
                    P.rot("ham_p", 0.85 * r8)
                for k_, xb in getattr(sk, "ong_nl", ()):                # tháp ống: góc và co giãn theo xương ống của họ, quanh chân tháp
                    g_ = P.t.get(xb)
                    if g_:
                        P.rot("ong_p_" + k_, g_[2])
                        P.scale("ong_p_" + k_, g_[3], g_[4])
                theo = 0.0                                              # chân đi theo thân lúc cả con rời đất / đổ nghiêng
                if ten_c == "die":
                    theo = ease(t / 0.18)
                elif ten_c == "appear":
                    theo = 1.0 - ease((t - (T_DAP - 0.04)) / 0.12)
                NC.ik(sk, P, t, ten_c, dur, theo)
            return g

        for c in clips[:-1]:
            c.fn = boc(c.fn, c.ten, c.dur)
    return clips


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    bo = tuple(b for b, *_ in info["khoi"])
    cao = soi.chieu_cao(ve0, idle0, bo) - info["dat_y"]
    clips = lam_clip(sk, info, cao)
    print(f"chiều cao (không tính khói) {cao:.0f}; cast nhả {T_NHA:.2f}; skill dài {D_SKILL:.2f} s, bẻ {T_BE:.2f}, bắn {T_BAN0:.2f} → {T_HET:.2f}")
    ra = os.environ.get("NL_RA") or (os.path.join(HERE, "inbox", MA_NON, "rig" if CHIBI else "rig_bo_cuc") if NON else
                                     os.path.join(G.BASE, "rig_goc" if GOC else "rig"))
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        aura = hoat.nuong(sk, clips[-1])
        if c.ten != "aura":
            fr = hoat.phu_aura(fr, aura, sk)
        if ":" in a[2]:
            t0, t1, n = a[2].split(":")
            ts = list(np.linspace(float(t0), float(t1), int(n)))
        elif a[2].startswith("n="):
            ts = list(np.linspace(0, c.dur, int(a[2][2:])))
        else:
            ts = [float(x) for x in a[2].split(",")]
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.3
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            d = ImageDraw.Draw(im)
            sach = os.environ.get("NL_SACH") == "1"          # NL_SACH=1: khung sạch, không đánh dấu miệng và các ống
            if not sach:
                d.text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            W = sk.the_gioi(P)
            for b, mau in ([] if sach else [("mieng", (60, 255, 90))] + [("ong_" + nn, (80, 200, 255)) for nn in info["ong"]]):
                M = W[b]
                x, y = (M[0, 2] - Bx[0]) * sc, (Bx[3] - M[1, 2]) * sc
                x2, y2 = x + M[0, 0] * 60 * sc, y - M[1, 0] * 60 * sc
                d.line([x, y, x2, y2], fill=mau, width=2)
                d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=mau)
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in ("appear", "attack", "cast", "skill", "hit"):
            frames[c.ten] = [P.copy() for P in frames[c.ten]]
            hoat.khop_cuoi(frames[c.ten], frames["idle"][0], 0.2)
    xuat.xuat_het(sk, clips, ra, TEN_RIG, "Khủng long núi lửa (nui_lua): tướng cuối đảo Hỏa" + (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=("cast", "skill"), ma_goc=None, khop_idle=0, cao=cao + info["dat_y"],
                  noi_them={}, impact=IMPACT, tol={"rotate": 0.08, "translate": 0.2, "scale": 0.0015}, dich_mb=0.6, tran_mb=1.0, span=SPAN)


if __name__ == "__main__":
    main(sys.argv[1:])
