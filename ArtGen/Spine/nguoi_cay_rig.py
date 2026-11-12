# -*- coding: utf-8 -*-
"""Người cây (nguoi_cay): rig trên bộ xương của con gốc monster_3491 (dáng người đấm bốc). Mảnh của mình là MẢNH CỨNG / lưới ô nhỏ đặt
theo concept đã duyệt; chuyển động nền lấy mẫu từ clip của họ (<scan>/sample_goc.json, runtime Spine thật đã giải IK chân), động tác
riêng (giơ tay triệu dây gai, chụm tay tụ cầu, giơ cầu, đập xuống, trồi lên) viết thêm trên các xương tay FK ngay tại đây.

- DÁNG GỐC của rig mình = khung 0 idle_01 của họ (thế thủ), vì concept vẽ theo dáng đó; mọi khoá là lệch so với dáng này.
- Đủ xương của họ (bỏ xương bóng, mục tiêu IK); thêm xương của mình (tiền tố x_): u rêu vai, từng lá mào / cổ áo / váy (lò xo), rêu rủ,
  cành khô, râu; chuỗi dây gai `gai*` trên xương `far` (chỗ đối thủ, game dời); xương `cau` (quả cầu dây leo).
- Dây gai (chiêu mana) và quả cầu dây leo (chiêu cuối) là MẢNH CỦA RIG (vật cứng phải uốn / cầm trên tay), ẩn sẵn; hạt, bụi, lá văng
  là việc của lớp VFX (sự kiện trong clip).

    nguoi_cay_rig.py                    dựng, xuất inbox/nguoi_cay_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    nguoi_cay_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [xuong]   khung lớn nền xám → rig/soi_<clip>.png
Chạy qua quai/khoa.py nang. Xương và chuyển động nền là của nhà phát hành game tham khảo: dùng nội bộ."""
import json
import math
import os
import pickle
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi, tienhoa  # noqa: E402
from quai import luoi as LU  # noqa: E402
from quai.khung import goc_mat  # noqa: E402
from quai.hoat import Clip, LoXo  # noqa: E402
import nguoi_cay as NC  # noqa: E402
import nguoi_cay_manh as NM  # noqa: E402

TEN = f"nguoi_cay_{NC.K}"
RA = os.path.join(NC.BASE, "rig")
SCAN = NC.scan()
KG = 0.60                    # đơn vị rig con gốc → đơn vị rig của mình
NHE = os.environ.get("NC_NHE") == "1"   # bản NHẸ (ảnh nhỏ) của dạng lớn, chỉ để gộp vào dạng 1 cho clip tiến hóa
PXU = 0.46 if NHE else 0.80  # pixel ảnh atlas cho mỗi đơn vị rig con gốc
BO = ("root", "shadow", "target", "target2", "target3", "target4")
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
IB = I["bones"]
TENX = [b["name"] for b in IB]
B0 = np.array([f[:5] for f in S["idle_01"]["frames"][0]["l"]], float)      # dáng gốc của mình = khung 0 idle của họ (x, y, góc, sx, sy)
TIEU_DE = ("Người cây dạng 1: con non (nguoi_cay_1), tướng thứ 7 đảo Mộc" if NC.K == 1 else
           "Người cây dạng 2: dạng lớn (nguoi_cay_2), tướng thứ 7 đảo Mộc")

# xương của họ
TAY = {"g": dict(don="bone31", bap="bone32", cang="bone33", nam="bone34"), "x": dict(don="bone35", bap="bone36", cang="bone37", nam="bone38")}
CHAN = {"g": dict(dui="bone43", ong="bone44", ban="bone46"), "x": dict(dui="bone47", ong="bone48", ban="bone50")}
# cặp (mảnh của mình, hình của họ) để khớp khung concept với hệ toạ độ rig gốc (tâm khung bao)
NEO = [("than", "P_shenti2"), ("nam_g", "P_shouR3"), ("nam_x", "P_shouL3"), ("ban_g", "P_jiaoR"), ("ban_x", "P_jiaoL"), ("cang_g", "P_shouR2"),
       ("cang_x", "P_shouL2"), ("ong_g", "P_tuiL2"), ("ong_x", "P_tuiR2")]
# mảnh chi: hai khớp đọc trên concept (px) → gốc xương của nó và gốc xương con (xoay + co đều + dời cả mảnh cho khớp nằm đúng trục quay)
HAI = {"bap_g": ((606, 492), (345, 502), "bone32", "bone33"), "cang_g": ((345, 502), (345, 680), "bone33", "bone34"),
       "bap_x": ((946, 488), (1106, 584), "bone36", "bone37"), "cang_x": ((1106, 584), (1196, 406), "bone37", "bone38"),
       "dui_g": ((645, 690), (528, 812), "bone43", "bone44"), "ong_g": ((528, 812), (520, 905), "bone44", "bone46"),
       "dui_x": ((850, 690), (958, 800), "bone47", "bone48"), "ong_x": ((958, 800), (965, 905), "bone48", "bone50")}
# mảnh mút: một khớp (px concept) → gốc xương; xoay / co theo mảnh chi nó nối vào (None: chỉ dời)
MOT = {"nam_g": ((345, 680), "bone34", "cang_g"), "nam_x": ((1196, 406), "bone38", "cang_x"), "ban_g": ((520, 905), "bone46", None),
       "ban_x": ((965, 905), "bone50", None)}
# mảnh đi theo phép chỉnh của mảnh khác
THEO = {"ru_g1": "bap_g", "ru_g2": "bap_g", "ru_g3": "bap_g", "ru_x1": "bap_x", "ru_x2": "bap_x", "ru_x3": "bap_x"}
# mảnh cứng → xương
XUONG = {"dau": "tou", "dai": "zhixin", "bap_g": "bone32", "cang_g": "bone33", "nam_g": "bone34", "bap_x": "bone36", "cang_x": "bone37",
         "nam_x": "bone38", "dui_g": "bone43", "ong_g": "bone44", "ban_g": "bone46", "dui_x": "bone47", "ong_x": "bone48", "ban_x": "bone50",
         "vai_g": "x_vai_g", "vai_x": "x_vai_x"}
# mảnh mềm của mình: tên → (xương cha, số đốt, độ cứng lò xo, giới hạn góc)
MEM = {"mao1": ("tou", 2, (260, 170), 16), "mao2": ("tou", 2, (260, 170), 16), "mao3": ("tou", 2, (260, 170), 16),
       "rau": ("tou", 2, (230, 150), 18),
       "co1": ("bone5", 1, (240,), 12), "co2": ("bone5", 1, (240,), 12), "co3": ("bone5", 1, (220,), 12), "co4": ("bone5", 1, (240,), 12),
       "vay_s1": ("bone51", 2, (200, 130), 20), "vay_s4": ("bone51", 2, (200, 130), 20), "vay_s2": ("zhixin", 2, (200, 130), 20),
       "vay_s5": ("bone54", 2, (200, 130), 20), "vay_s3": ("bone54", 2, (200, 130), 20),
       "vay1": ("bone51", 2, (210, 140), 22), "vay2": ("bone51", 2, (210, 140), 22), "vay3": ("bone51", 2, (190, 125), 22),
       "vay4": ("bone54", 2, (180, 120), 22), "vay6": ("bone54", 2, (210, 140), 22), "vay7": ("bone54", 2, (210, 140), 22),
       "ru_g1": ("bone32", 2, (190, 120), 26), "ru_g2": ("bone32", 2, (190, 120), 26), "ru_g3": ("bone32", 2, (200, 130), 26),
       "ru_x1": ("bone36", 2, (190, 120), 26), "ru_x2": ("bone36", 2, (190, 120), 26), "ru_x3": ("bone36", 2, (200, 130), 26),
       "la_vai_g": ("x_vai_g", 1, (260,), 10), "la_vai_x": ("x_vai_x", 1, (260,), 10),
       "canh_g1": ("x_vai_g", 1, (420,), 6), "canh_g2": ("x_vai_g", 1, (440,), 6), "canh_x": ("x_vai_x", 1, (420,), 6)}
ZERO5 = (0.0, 0.0, 0.0, 1.0, 1.0)
DK_CAU = 0.78                # đường kính quả cầu dây leo lúc đầy (× chiều cao)
if NC.K == 1:                # DẠNG 1 (con non): khớp đọc trên concept dạng 1; ít lớp mềm; chiêu nhẹ hơn (một dây gai, cầu nhỏ)
    HAI = {"bap_g": ((604, 492), (345, 506), "bone32", "bone33"), "cang_g": ((345, 506), (338, 694), "bone33", "bone34"),
           "bap_x": ((946, 490), (1106, 588), "bone36", "bone37"), "cang_x": ((1106, 588), (1165, 402), "bone37", "bone38"),
           "dui_g": ((640, 700), (535, 806), "bone43", "bone44"), "ong_g": ((535, 806), (528, 905), "bone44", "bone46"),
           "dui_x": ((850, 700), (955, 800), "bone47", "bone48"), "ong_x": ((955, 800), (962, 905), "bone48", "bone50")}
    MOT = {"nam_g": ((338, 694), "bone34", "cang_g"), "nam_x": ((1165, 402), "bone38", "cang_x"), "ban_g": ((528, 905), "bone46", None),
           "ban_x": ((962, 905), "bone50", None)}
    THEO = {"ru_g1": "bap_g", "ru_x1": "bap_x"}
    MEM = {"mam_than": ("tou", 1, (300,), 8), "mam1": ("x_mam_than_0", 2, (230, 150), 20), "mam2": ("x_mam_than_0", 2, (230, 150), 20),
           "co1": ("bone5", 1, (240,), 12), "co2": ("bone5", 1, (220,), 12), "co3": ("bone5", 1, (240,), 12),
           "vay1": ("bone51", 2, (210, 140), 22), "vay2": ("bone51", 2, (210, 140), 22), "vay3": ("bone51", 2, (190, 125), 22),
           "vay4": ("bone54", 2, (210, 140), 22), "vay5": ("bone54", 2, (210, 140), 22),
           "ru_g1": ("bone32", 2, (190, 120), 26), "ru_x1": ("bone36", 2, (190, 120), 26)}
    DK_CAU = 0.54
N_GAI = 10                   # số đốt dây gai
# ba dây gai của chiêu mana (người dùng 2026-11-12: "triệu hồi nhiều cây hơn cùng quật nhiều kiểu"), xếp sau → trước:
#   dx: gốc dây so với chỗ đối thủ (× chiều cao); dai: chiều dài (× chiều cao); day: bề dày so với ảnh; lat: lật ảnh; chieu: +1 = cong
#   sang TRÁI (ngược kim), −1 = cong sang phải; moc: giây nhú; quat: giây quật trúng; kieu: dap (vươn cao rồi bổ từ trên xuống thành vòm),
#   ngang (quét ngang tầm chân rồi móc ngược lên), quan (quật vòng qua đầu rồi quấn thành vòng)
GAI = [dict(ten="c", dx=0.28, dai=1.64, day=1.15, lat=-1.0, chieu=1.0, moc=0.84, quat=1.42, kieu="dap"),
       dict(ten="b", dx=0.46, dai=1.22, day=0.95, lat=-1.0, chieu=1.0, moc=0.74, quat=1.22, kieu="ngang"),
       dict(ten="a", dx=-0.24, dai=1.55, day=1.0, lat=1.0, chieu=-1.0, moc=0.62, quat=1.02, kieu="quan")]
if NC.K == 1:                # dạng 1: chỉ một dây gai nhỏ, quật vòng rồi quấn
    GAI = [dict(ten="a", dx=-0.20, dai=1.22, day=0.80, lat=1.0, chieu=-1.0, moc=0.62, quat=1.02, kieu="quan")]
GAI_SLOT = tuple("gai_" + g["ten"] for g in GAI)
DAT_Y = -3.0                 # mặt đất của mặt nạ (đơn vị rig mình; đáy bàn chân ở y = 0)


def khop_khung(dat):
    """khung concept (px, y xuống) ↔ thế giới rig gốc (y lên): px = ox + s·X, py = oy − s·Y (bình phương tối thiểu trên các cặp NEO)."""
    by = {a["att"]: a for a in A0["atts"] if a["cur"]}
    R, b = [], []
    for m, h in NEO:
        P = np.array(by[h]["xy"], float).reshape(-1, 2)
        X, Y = (P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2
        Aff = np.array(dat[m]["A"], float)
        w, hh = dat[m]["co"]
        c = Aff @ np.array([w / 2, hh / 2, 1.0])
        R += [[X, 1, 0], [-Y, 0, 1]]
        b += [c[0], c[1]]
    (s, ox, oy), *_ = np.linalg.lstsq(np.array(R, float), np.array(b, float), rcond=None)
    lech = np.array(R) @ np.array([s, ox, oy]) - np.array(b)
    print(f"khớp khung concept: {s:.3f} px / đơn vị con gốc; lệch từng mốc (px): " +
          ", ".join(f"{m} {math.hypot(lech[2 * i], lech[2 * i + 1]):.0f}" for i, (m, _) in enumerate(NEO)))
    return float(s), float(ox), float(oy)


def dung(nang=None):
    dat = json.load(open(os.path.join(NM.MANH, "dat.json"), encoding="utf-8"))
    thu_tu = dat.pop("_thu_tu")
    s, ox, oy = khop_khung(dat)
    tg = lambda p: np.stack([(np.asarray(p, float)[..., 0] - ox) / s, (oy - np.asarray(p, float)[..., 1]) / s], -1)   # noqa: E731

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này (lao, nhảy)
    for i, b in enumerate(IB):
        if b["name"] in BO:
            continue
        cha = TENX[b["parent"]]
        x, y, r, sx, sy = B0[i]
        sk.xuong(b["name"], "move" if cha == "root" else cha, x * KG, y * KG + ((nang or 0.0) if cha == "root" else 0.0), goc=r,
                 dai=b["len"] * KG, sx=sx, sy=sy)
    # kiểm: dáng gốc của mình phải trùng thế giới khung 0 idle của họ
    sai = max(np.hypot(sk.W0[b["name"]][0, 2] / KG - b["x"], (sk.W0[b["name"]][1, 2] - (nang or 0.0)) / KG - b["y"]) for b in A0["bones"]
              if b["name"] not in BO)
    print(f"dáng gốc so khung 0 idle của họ: lệch lớn nhất {sai:.2f} đơn vị")
    goc_x = lambda b: (sk.W0[b][:2, 2] - np.array([0.0, nang or 0.0])) / KG       # gốc xương, đơn vị con gốc   # noqa: E731

    # phép chỉnh từng mảnh (thế giới con gốc → thế giới con gốc): SUA[t] là HÀM trên mảng điểm (N, 2)
    SUA, lin = {}, {}

    def chi(P0, P1, Q0, Q1):
        """mảnh chi đặt theo hai khớp P0 → Q0, P1 → Q1: xoay theo trục xương; CHỈ đoạn giữa hai khớp co giãn theo độ dài xương, phần
        ngoài hai khớp (hai đầu tròn) và bề ngang giữ nguyên cỡ. (Bản đầu co giãn cả mảnh dọc trục: đùi dạng 1 phải kéo 1,59 lần nên
        đầu tròn ở gối dài ra, thòi khỏi khớp, ống chân trông như rời khỏi chân: người dùng "khớp cổ chân lỗi, không liên kết".)"""
        dp, dq = P1 - P0, Q1 - Q0
        L, Lb = float(np.hypot(*dp)), float(np.hypot(*dq))
        up, uq = dp / L, dq / Lb
        np_, nq = np.array([-up[1], up[0]]), np.array([-uq[1], uq[0]])

        def f(w):
            w = np.asarray(w, float).reshape(-1, 2)
            s_ = (w - P0) @ up
            n_ = (w - P0) @ np_
            S_ = np.where(s_ < 0, s_, np.where(s_ <= L, s_ * Lb / L, Lb + (s_ - L)))
            return Q0 + S_[:, None] * uq + n_[:, None] * nq
        return f, Lb / L, math.degrees(math.atan2(dq[1], dq[0]) - math.atan2(dp[1], dp[0]))

    for t, (p0, p1, b0, b1) in HAI.items():
        f, k, a = chi(tg(p0), tg(p1), goc_x(b0), goc_x(b1))
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        SUA[t], lin[t] = f, np.array([[ca, -sa], [sa, ca]])                  # mảnh mút (nắm tay) chỉ xoay theo, không co
        d0 = np.hypot(*(tg(p0) - goc_x(b0)))
        print(f"  {t:8s} đoạn giữa co {k:.2f}  xoay {a:+6.1f}°  khớp gốc lệch trước khi chỉnh {d0:.0f}")
    for t, (p0, b0, theo) in MOT.items():
        R_ = lin[theo] if theo else np.eye(2)
        d_ = goc_x(b0) - R_ @ tg(p0)
        SUA[t] = (lambda w, R_=R_, d_=d_: (R_ @ np.asarray(w, float).reshape(-1, 2).T).T + d_)
    for t, theo in THEO.items():
        SUA[t] = SUA[theo]

    def the_gioi(t, pts_anh):
        """điểm ảnh (px ảnh gốc của mảnh) → thế giới rig mình."""
        Aff = np.array(dat[t]["A"], float)
        P = np.asarray(pts_anh, float).reshape(-1, 2)
        c = (Aff[:, :2] @ P.T).T + Aff[:, 2]
        w = tg(c)
        if t in SUA:
            w = SUA[t](w)
        return w * KG + np.array([0.0, nang or 0.0])

    def px_tg(t, p):
        """điểm concept (px) thuộc mảnh t → thế giới rig mình (có phép chỉnh của mảnh)."""
        w = tg(np.array(p, float))
        if t in SUA:
            w = SUA[t](w)[0]
        return w * KG + np.array([0.0, nang or 0.0])

    # xương của mình
    for ben in "gx":
        x, y = sk.W0[TAY[ben]["bap"]][:2, 2]
        sk.xuong(f"x_vai_{ben}", TAY[ben]["don"], x, y, 0.0, the_gioi=True)
    mem_ds = []
    for t, (cha, n, k, mx) in MEM.items():
        g, m = px_tg(t, dat[t]["cuong"]), px_tg(t, dat[t]["mui"])
        if t.startswith("canh"):                 # cành: cuống = gốc cành (đáy ảnh)
            pass
        J = [g + (m - g) * q / n for q in range(n + 1)]
        ten = sk.chuoi("x_" + t + "_", cha, J)
        mem_ds.append(LoXo(ten, k=k, damp=0.5, maxang=mx))
    ti_anh = PXU / s                             # ảnh atlas = ảnh mảnh × ti_anh
    da_nap = set()

    def nap(a):
        if a not in da_nap:
            g = Image.open(os.path.join(NM.MANH, a + ".png"))
            im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * ti_anh)), max(2, round(g.height * ti_anh))), Image.LANCZOS).convert("RGBA"))
            sk.anh(a, im)
            da_nap.add(a)
        return sk.images[a]

    def gan(slot, t, cot, hang, ts, an=False, xuong_slot=None):
        """lưới ô cot × hang đỉnh phủ cả ảnh của mảnh t; ts(u, v) → {xương: w} (u, v ∈ [0, 1] theo ảnh)."""
        a = dat[t]["anh"]
        im = nap(a)
        w0, h0 = dat[t]["co"]
        L = LU.luoi_o(im.width, im.height, cot, hang)
        uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
        V = the_gioi(t, uv * np.array([w0, h0], float))
        W = [ts(float(u), float(v)) for u, v in uv]
        b0 = xuong_slot or max(W[0], key=W[0].get)
        sk.slot(slot, b0, t, an=an)
        sk.luoi_gan(slot, a, L, W, the_gioi=V, ten=t)

    def muot(x):
        x = min(1.0, max(0.0, x))
        return x * x * (3 - 2 * x)

    sk.xuong("dat", "root")                      # xương đứng yên ở mặt đất cho mặt nạ (không bám thẳng root: gộp tiến hóa thay root của dạng sau)
    sk.slot("cat", "dat")                        # mặt nạ mặt đất (đặt đa giác sau khi biết chiều cao): phần thân dưới đất bị giấu (appear trồi lên)
    for t in thu_tu:
        if t == "than":                          # thân: phần trên theo ngực, phần dưới theo eo (đai che chỗ nối với hông)
            def ts_than(u, v):
                q = muot((v - 0.42) / 0.4)
                return {"bone5": 1.0} if q <= 0 else ({"bone4": 1.0} if q >= 1 else {"bone5": 1 - q, "bone4": q})
            gan(t, t, 3, 6, ts_than)
        elif t in MEM:
            n = MEM[t][1]
            ten = [f"x_{t}_{q}" for q in range(n)]
            dao = t.startswith("canh")           # ảnh cành: gốc ở ĐÁY ảnh
            if n == 1:
                gan(t, t, 2, 2, lambda u, v, b=ten[0]: {b: 1.0})
            else:
                def ts(u, v, ten=ten, dao=dao):
                    q = muot(((1 - v if dao else v) - 0.32) / 0.36)
                    return {ten[0]: 1.0} if q <= 0 else ({ten[1]: 1.0} if q >= 1 else {ten[0]: 1 - q, ten[1]: q})
                gan(t, t, 2, 6, ts)
        else:
            o = 9 if t in HAI else 2             # mảnh chi: lưới 9 × 9 để theo được phép co riêng đoạn giữa
            gan(t, t, o, o, lambda u, v, b=XUONG[t]: {b: 1.0})

    if nang is None:                             # lượt đo: bàn chân của mình thấp hơn gốc rig bao nhiêu thì nâng cả con lên chừng ấy
        day = min(float(a_["V"][:, 1].min()) for sl_ in ("ban_g", "ban_x") for a_ in sk.atts[sl_].values())
        print(f"đáy bàn chân ở y = {day:.1f}: nâng cả con {-day:.1f}")
        return dung(nang=-day)
    # chiều cao game: đỉnh đầu (không tính mào lá, cành khô)
    cao = float(the_gioi("dau", [[0, 0]])[0][1])
    # mặt nạ mặt đất: chỉ còn phần trên mặt đất của mọi mảnh thân (dây gai, quả cầu nằm ngoài mặt nạ). Luôn bật; đủ rộng cho cú lao, cú nhảy
    sk.cat("cat", thu_tu[-1], [(-5.0 * cao, DAT_Y), (7.0 * cao, DAT_Y), (7.0 * cao, 9.0 * cao), (-5.0 * cao, 9.0 * cao)])
    # chỗ đối thủ + BA dây gai (chiêu mana), mỗi dây một chuỗi N_GAI đốt mọc thẳng đứng từ đất quanh chỗ đối thủ, dùng chung một ảnh
    sk.xuong("far", "root", 0.9 * cao + 60.0, 0.45 * cao)
    fx = sk.W0["far"][0, 2]
    img = Image.open(os.path.join(NM.MANH, "gai.png"))
    im = anh.loang_mau(img.convert("RGBa").resize((max(2, round(img.width * 0.62)), max(2, round(img.height * 0.62))), Image.LANCZOS).convert("RGBA"))
    sk.anh("gai", im)
    gai = []
    for g in GAI:                                # thứ tự trong GAI = thứ tự vẽ (sau → trước)
        k_ = g["ten"]
        dai_gai = g["dai"] * cao
        gx = fx + g["dx"] * cao
        goc_ = f"gai_{k_}_goc"
        sk.xuong(goc_, "far", gx, -0.04 * cao, 90.0, the_gioi=True)
        ten_gai = sk.chuoi(f"gai_{k_}_", goc_, [(gx, -0.04 * cao + dai_gai * q / N_GAI) for q in range(N_GAI + 1)])
        kg_ = dai_gai / (img.width - 2 * NM.PAD)  # đơn vị rig cho mỗi px ảnh dây gai
        L = LU.luoi_o(im.width, im.height, 3 * N_GAI + 1, 3)
        uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
        V = np.stack([gx + g["lat"] * (uv[:, 1] - 0.5) * img.height * kg_ * g["day"], -0.04 * cao + (uv[:, 0] * img.width - NM.PAD) * kg_], 1)
        Wg = []
        for u, v in uv:
            f = min(N_GAI - 1e-6, max(0.0, (u * img.width - NM.PAD) / (img.width - 2 * NM.PAD) * N_GAI))
            i0 = int(f)
            r = f - i0
            d = {ten_gai[i0]: 0.75 - abs(r - 0.5) * 0.5}
            if r < 0.5 and i0 > 0:
                d[ten_gai[i0 - 1]] = 0.5 - r
            elif r >= 0.5 and i0 < N_GAI - 1:
                d[ten_gai[i0 + 1]] = r - 0.5
            tong = sum(d.values())
            Wg.append({k: v_ / tong for k, v_ in d.items()})
        sl = f"gai_{k_}"
        sk.slot(sl, goc_, sl, an=True)
        sk.luoi_gan(sl, "gai", L, Wg, the_gioi=V, ten=sl)
        gai.append(dict(g, slot=sl, goc=goc_, dot=ten_gai))
    # quả cầu dây leo (chiêu cuối): xương cau (con của move), ẩn sẵn
    sk.xuong("cau", "move", 0.0, cao * 0.9)
    imc = Image.open(os.path.join(NM.MANH, "cau.png"))
    dk = DK_CAU * cao                            # đường kính quả cầu lúc đầy
    im = anh.loang_mau(imc.convert("RGBa").resize((round(imc.width * 0.55), round(imc.height * 0.55)), Image.LANCZOS).convert("RGBA"))
    sk.anh("cau", im)
    sk.slot("cau", "cau", "cau", an=True)
    sk.manh("cau", "cau", khung.Dat(0.0, cao * 0.9, ti=dk / max(im.width, im.height)))
    for e, m in (("trung", "khung đòn trúng (đấm / dây gai quật / cầu nện xuống)"), ("trieu", "tay giơ hết: gọi dây gai"),
                 ("moc", "một dây gai nhú khỏi đất ở chỗ đối thủ (chuỗi kèm: tên dây a / b / c)"), ("quat", "cú quật của dây thứ hai, thứ ba trúng"), ("troi", "dây gai quấn xong, siết"), ("nha", "dây gai nhả, rút xuống đất"),
                 ("tu", "bắt đầu tụ quả cầu (VFX lá, dây leo bị hút vào)"), ("day", "cầu đầy"), ("nhay", "rời đất"),
                 ("nhu", "chồi nhú khỏi đất"), ("troi_len", "cả người đội đất vọt lên (VFX đất, lá văng)"), ("gam", "gồng, gầm"), ("nga", "đổ sụp")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(dat=dat, thu_tu=thu_tu, cao=cao, mem=mem_ds, gai=gai)


# ================================================================ chuyển động
def chuyen_dong():
    """{clip: (dài, {xương: mảng (số khung, 5) = lệch xoay độ, dời x, y (đơn vị rig mình), tỉ lệ x, y nhân})} so với dáng gốc của mình."""
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i, b in enumerate(IB):
            if b["name"] in BO:
                continue
            x0, y0, r0, sx0, sy0 = B0[i]
            Am = np.array([[F["l"][i][2] - r0, (F["l"][i][0] - x0) * KG, (F["l"][i][1] - y0) * KG, F["l"][i][3] / (sx0 or 1.0),
                            F["l"][i][4] / (sy0 or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[b["name"]] = Am
        out[clip] = (float(v["dur"]), res)
    # LÀM TRƠN chỗ clip của họ bật tức thì trong một khung (hình của họ nhỏ, chân nấp dưới váy nên không lộ; hình của mình to, người
    # dùng thấy "giật mấy frame, chân tay bị giật"):
    # - skill_02 lúc rời đất (0,90–0,97 s): cả thân vọt lên ~200 đơn vị trong một khung, bàn chân quay 122°, ống chân IK rung ±60°;
    # - skill_01_1 lúc chồm tới (0,37–0,40 s): cả thân dời ~230 đơn vị trong một khung.
    # Lọc Gauss mọi kênh của mọi xương trong cửa sổ đó (ngoài cửa sổ giữ nguyên: chân trên mặt đất vẫn bám, cú chạm đất vẫn gọn).
    def lam_tron(clip, t0, t1, sigma, mep=0.08):
        dur, res = out[clip]
        n = len(S[clip]["frames"])
        ts = np.arange(n) / 30.0
        w_ = (np.clip((ts - t0) / mep, 0, 1) * np.clip((t1 - ts) / mep, 0, 1))[:, None]
        r = int(math.ceil(3 * sigma))
        ker = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
        ker /= ker.sum()
        for b, arr in res.items():
            tron = np.stack([np.convolve(np.pad(arr[:, q], r, mode="edge"), ker, mode="valid") for q in range(5)], 1)
            res[b] = arr * (1 - w_) + tron * w_

    lam_tron("skill_02", 0.78, 1.36, 2.2)
    lam_tron("skill_01_1", 0.26, 0.54, 1.3)
    return out


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.2):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.2):
    x = min(1.0, max(0.0, x))
    return x ** k


def moc(t, ks):
    """đường khoá: ks = [(t, v[, kiểu])]; kiểu của khoá áp cho đoạn KẾT THÚC ở khoá đó: em (mặc định), ra, vao, thang."""
    if t <= ks[0][0]:
        return float(ks[0][1])
    for a, b in zip(ks, ks[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            kieu = b[2] if len(b) > 2 else "em"
            u = {"em": em, "ra": ra, "vao": vao, "thang": lambda q: q}[kieu](u)
            return float(a[1] + (b[1] - a[1]) * u)
    return float(ks[-1][1])


def lam_clip(sk, info):
    CD = chuyen_dong()
    cao = info["cao"]
    REF = {b: goc_mat(sk.W0[b]) for ben in "gx" for b in TAY[ben].values()}
    REF.update({b: goc_mat(sk.W0[b]) for b in ("bone4", "bone5", "tou")})
    far0 = sk.W0["far"][:2, 2].copy()
    cau0 = sk.W0["cau"][:2, 2].copy()
    ds_gai = info["gai"]
    la_mem = [t for t in MEM if not t.startswith("canh")]

    # tay tự viết thì KHÔNG lấy tay của clip nền, kể cả xương đòn (ở các chiêu của họ xương đòn vung theo tay, u rêu vai sẽ văng theo)
    BO_TAY = tuple(TAY[ben][k] for ben in "gx" for k in ("don", "bap", "cang", "nam"))

    def nen(P, goc, tau, lap=False, w=1.0, bo=(), lech=None):
        """dáng nền lấy từ clip của họ ở giây tau, trọng số w (cộng dồn được để pha hai dáng). bo: xương không lấy; lech: {xương: độ}
        cộng vào góc (bội 360° cho dáng nền thứ hai nằm cùng vòng với dáng thứ nhất khi pha)."""
        dur, R = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        for b, arr in R.items():
            if b in bo:
                continue
            n = len(arr)
            i0 = min(int(x), n - 1)
            i1 = min(i0 + 1, n - 1)
            f = x - i0
            v = arr[i0] * (1 - f) + arr[i1] * f
            goc_b = float(v[0]) + (lech.get(b, 0.0) if lech else 0.0)
            if abs(goc_b) > 1e-4:
                P.rot(b, goc_b * w)
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]) * w, float(v[2]) * w)
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, 1 + (float(v[3]) - 1) * w, 1 + (float(v[4]) - 1) * w)

    CHUOI = {}                   # xương → chính nó và mọi xương tổ tiên (góc thế giới = tổng góc riêng dọc chuỗi này)

    def chuoi_cua(b):
        if b not in CHUOI:
            ds, x_ = [], b
            while x_:
                ds.append(x_)
                x_ = sk.bones[sk.bi[x_]]["parent"]
            CHUOI[b] = tuple(ds)
            REF.setdefault(b, goc_mat(sk.W0[b]))
        return CHUOI[b]

    def huong(P, b, goc, w=1.0):
        """xoay xương b cho trục x của nó về góc THẾ GIỚI goc (độ, liên tục quanh góc dáng gốc REF[b]), trọng số w.
        Góc hiện tại đọc từ ma trận chỉ biết tới bội 360°: chọn bội cho nó gần nhất với REF[b] + tổng độ xoay đã đặt lên nó và mọi xương
        tổ tiên (lỗi đã gặp: so thẳng với REF thì khi cẳng tay hay thân đã quay quá nửa vòng, góc nhảy 360° giữa hai khung → giật)."""
        if w <= 1e-4:
            return
        ch = chuoi_cua(b)
        cur = goc_mat(sk.the_gioi(P)[b])
        uoc = REF[b] + sum(P.t.get(x, ZERO5)[2] for x in ch)
        cur += 360.0 * round((uoc - cur) / 360.0)
        P.rot(b, (goc - cur) * w)

    def tay(P, ben, bap, cang, nam=None, w=1.0):
        """đặt tay theo góc thế giới: bắp, cẳng, nắm (None: nắm thẳng theo cẳng như dáng gốc)."""
        T = TAY[ben]
        huong(P, T["bap"], bap, w)
        huong(P, T["cang"], cang, w)
        huong(P, T["nam"], (cang + REF[T["nam"]] - REF[T["cang"]]) if nam is None else nam, w)

    DAI_TAY = {ben: (float(np.hypot(*(sk.W0[TAY[ben]["cang"]][:2, 2] - sk.W0[TAY[ben]["bap"]][:2, 2]))),
                     float(np.hypot(*(sk.W0[TAY[ben]["nam"]][:2, 2] - sk.W0[TAY[ben]["cang"]][:2, 2])))) for ben in "gx"}

    def giai_tay(W, ben, dich, gan):
        """giải hai khúc tay: góc thế giới (bắp, cẳng) cho cổ tay (gốc xương nắm) tới điểm dich; khuỷu chìa ra ngoài (tay gần: sang trái,
        tay xa: sang phải). gan = (bắp, cẳng) dáng mong muốn: trả góc cùng vòng với nó."""
        S_ = W[TAY[ben]["bap"]][:2, 2]
        L1, L2 = DAI_TAY[ben]
        v = np.asarray(dich, float) - S_
        d = min(max(float(np.hypot(*v)), abs(L1 - L2) + 1e-3), L1 + L2 - 1e-3)
        a = math.atan2(v[1], v[0])
        phi = math.acos(max(-1.0, min(1.0, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
        gb = a + (phi if ben == "g" else -phi)
        E = S_ + L1 * np.array([math.cos(gb), math.sin(gb)])
        T_ = S_ + v / max(1e-9, float(np.hypot(*v))) * d
        gc = math.atan2(T_[1] - E[1], T_[0] - E[0])
        gb, gc = math.degrees(gb), math.degrees(gc)
        return gb + 360.0 * round((gan[0] - gb) / 360.0), gc + 360.0 * round((gan[1] - gc) / 360.0)

    def gio(P, t, manh=1.0, chu_ky=2.0):
        """gió: lá, rêu, râu đung đưa lệch pha (lò xo chạy sau sẽ làm trễ thêm)."""
        for k, tn in enumerate(la_mem):
            n = MEM[tn][1]
            bien = (5.0 if tn.startswith(("ru", "vay")) else 3.0) * manh
            ph = k * 1.7
            for q in range(n):
                P.rot(f"x_{tn}_{q}", bien * (0.6 + 0.5 * q) * math.sin(2 * math.pi * t / chu_ky + ph - 0.7 * q))

    RU = [t_ for t_ in MEM if t_.startswith("ru_")]
    VAI_K = 46.0                 # u rêu vai nghiêng tối đa chừng này độ khi tay giơ thẳng lên
    C0 = {ben: math.cos(math.radians(REF[TAY[ben]["bap"]] - REF["bone5"])) for ben in "gx"}

    def sau(P):
        """sau khi đặt dáng: u rêu vai XOAY theo bắp tay. Góc nghiêng tính theo độ GIƠ của bắp tay so với trục ngực (cos góc giữa hai
        trục: −0,34 ở thế thủ, 1 khi tay giơ thẳng lên), nên tay lên đường nào (vòng ngoài hay vốc qua phía trước) u rêu cũng nghiêng
        êm, không quay theo cả vòng. Tay gần (bên trái) giơ thì đầu ngoài u rêu nhấc lên = xoay thuận kim; tay xa ngược lại."""
        W = sk.the_gioi(P)
        g5 = goc_mat(W["bone5"])
        for ben, chieu in (("g", -1.0), ("x", 1.0)):
            c = math.cos(math.radians(goc_mat(W[TAY[ben]["bap"]]) - g5))
            e = (c - C0[ben]) / (1.0 - C0[ben])
            P.rot(f"x_vai_{ben}", chieu * VAI_K * (e if e > 0 else 0.5 * e))
        # rêu rủ dưới bắp tay TREO theo trọng lực: gốc dải rêu giữ hướng thế giới của dáng gốc (cộng phần đung đưa gio() đã đặt), không quay
        # cứng theo bắp tay (quay cứng thì lúc tay vung nhanh lò xo lệch quá nửa vòng, dải rêu lật ±30° từng khung)
        for tn in RU:
            b = f"x_{tn}_0"
            lac = P.t[b][2] if b in P.t else 0.0
            if b in P.t:
                P.t[b][2] = 0.0
            chuoi_cua(b)
            huong(P, b, REF[b] + lac)

    def rung(t, t0, t1, hz=11.0):
        if t < t0 or t > t1:
            return 0.0
        return math.sin(2 * math.pi * hz * (t - t0)) * min(1.0, (t - t0) / 0.12) * min(1.0, (t1 - t) / 0.12)

    def an_chieu(P):
        for sl_ in GAI_SLOT:
            P.alpha[sl_] = 0.0
        P.alpha["cau"] = 0.0

    # ---------------------------------------------------------------- idle: thế thủ của họ + gió + một nhịp gầm gừ rung vai
    I_DUR = CD["idle_01"][0]

    def idle(t, P):
        nen(P, "idle_01", t, True)
        gio(P, t, 1.0, 2.0)
        g = moc(t, [(2.2, 0), (2.45, 1, "ra"), (3.05, 1), (3.4, 0)])          # gầm gừ: chúi đầu, rung vai, nắm tay siết
        r = rung(t, 2.4, 3.1, 9.0)
        P.rot("tou", -7.0 * g + 2.2 * r * g)
        P.rot("bone5", -2.5 * g)
        for ben, d in (("g", 1), ("x", -1)):
            P.rot(f"x_vai_{ben}", d * (4.0 * g + 1.6 * r))
            P.scale(TAY[ben]["nam"], 1 + 0.07 * g + 0.02 * r * g)
            P.rot(TAY[ben]["cang"], d * -5.0 * g)
        for tn in [c_ for c_ in ("canh_g1", "canh_g2", "canh_x") if c_ in MEM]:
            P.rot(f"x_{tn}_0", 3.0 * r * g)
        sau(P)
        an_chieu(P)

    # ---------------------------------------------------------------- walk: run_01 của họ chạy chậm lại
    W_DUR = 0.8

    def walk(t, P):
        nen(P, "run_01", t / W_DUR * CD["run_01"][0], True)
        gio(P, t, 0.6, 0.8)
        sau(P)
        an_chieu(P)

    def hit(t, P):
        nen(P, "hit_01", t)
        sau(P)
        an_chieu(P)

    # ---------------------------------------------------------------- attack: cú đấm skill_01_1 của họ + lao tới
    A_DUR = CD["skill_01_1"][0]
    A_TRUNG = 0.42               # nắm tay xa duỗi hết (thân họ chồm tới ở 0,40 s)
    A_XA = 0.62 * cao

    def attack(t, P):
        # thân và chân: cú vặn người lấy đà rồi chồm tới của skill_01_1 (ở con gốc là cú ĐỚP bằng đầu rương). Hai tay là của mình (không lấy
        # tay của clip đó: tay họ vung cả vòng lúc thu về): tay XA (tay đấm, bên phải hình) GIƠ nắm đấm lên cao ra sau đầu rồi giáng thẳng
        # tới trước; tay gần đưa ra trước lúc lấy đà rồi giật khuỷu về sau làm đối trọng.
        nen(P, "skill_01_1", t, bo=BO_TAY)
        w = moc(t, [(0, 0), (0.14, 1), (A_TRUNG + 0.22, 1), (A_DUR - 0.14, 0)])
        u = moc(t, [(0.30, 0), (A_TRUNG, 1, "vao")])
        gio_len = moc(t, [(0, 0), (0.26, 1, "ra")])
        tay(P, "x", (-37.0 + 150.0 * gio_len) + (-8.0 - 113.0) * u, (60.0 + 62.0 * gio_len) + (-4.0 - 122.0) * u, w=w)
        tay(P, "g", -150.0 - 52.0 * u, -70.0 - 62.0 * u, w=w)
        P.scale(TAY["x"]["nam"], 1 + 0.14 * moc(t, [(A_TRUNG - 0.06, 0), (A_TRUNG, 1), (A_TRUNG + 0.2, 1), (A_TRUNG + 0.4, 0)]))
        x = moc(t, [(0.0, 0), (0.22, -0.07 * cao), (A_TRUNG, A_XA, "vao"), (A_TRUNG + 0.2, A_XA), (A_DUR - 0.08, 0)])
        P.move("move", x, 0.0)
        sau(P)
        an_chieu(P)

    # ---------------------------------------------------------------- cast: giơ MỘT tay (tay xa, bên phải hình) triệu ba dây gai quật ba kiểu rồi trói
    C_TRIEU = 0.50               # tay giơ hết
    C_MOC = min(g["moc"] for g in GAI)       # dây đầu tiên nhú
    C_QUAT = min(g["quat"] for g in GAI)     # cú quật đầu tiên trúng (khung trúng của game)
    C_TROI = max(g["quat"] for g in GAI) + (0.24 if len(GAI) > 1 else 0.28)      # mọi dây đã quấn / chụp xong: siết
    C_NHA = C_TROI + 0.48        # nhả
    C_DUR = C_NHA + 0.86

    def day_gai(P, g, t):
        """một dây gai ở giây t của clip. Góc dương của mỗi kiểu = cong VỀ PHÍA đối thủ; nhân `chieu` ra chiều thật."""
        tau = t - g["moc"]
        sl, dot, ch = g["slot"], g["dot"], g["chieu"]
        tq, tn = g["quat"] - g["moc"], C_NHA - g["moc"]
        if tau < 0 or tau > tn + 0.46:
            P.alpha[sl] = 0.0
            return
        lon = moc(tau, [(0, 0.03), (0.26, 1.0, "ra"), (tn, 1.0), (tn + 0.42, 0.03, "vao")])
        P.alpha[sl] = moc(tau, [(0, 0), (0.05, 1), (tn + 0.34, 1), (tn + 0.44, 0)])
        P.scale(g["goc"], lon, 0.55 + 0.45 * lon)
        siet = math.sin(2 * math.pi * 3.2 * (t - C_TROI)) if C_TROI < t < C_NHA else 0.0
        song = math.sin(2 * math.pi * 2.6 * tau + 1.3 * ch) * moc(tau, [(0, 1), (tq - 0.1, 1), (tq, 0), (tn, 0), (tn + 0.2, 1)])
        R = [0.0] * N_GAI
        if g["kieu"] == "quan":
            # ba đốt gốc đứng thẳng làm thân, bảy đốt ngọn: ngả ra sau lấy đà, quật vòng qua đầu, quấn thành vòng quanh thân đối thủ
            c = moc(tau, [(0, -1.0), (0.22, -3.0), (tq - 0.12, -7.0), (tq, 24.0, "vao"), (tq + 0.28, 43.0, "ra"), (tn, 45.0), (tn + 0.3, 5.0)])
            HE = (0.0, 0.0, 0.15, 0.6, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
            R = [(c + 2.2 * siet) * HE[q] for q in range(N_GAI)]
            nghieng = moc(tau, [(0, 0), (tq - 0.12, -6.0), (tq, 3.0, "vao"), (tn, 3.0), (tn + 0.3, 0)])
        elif g["kieu"] == "ngang":
            # bốn đốt gốc gập hẳn xuống cho thân dây nằm ngang tầm chân rồi quét qua; năm đốt ngọn lúc quét bị kéo trễ lại, quét xong thì móc
            # ngược lên ôm lấy đối thủ từ phía bên kia
            b_ = moc(tau, [(0, 0.0), (0.2, -4.0), (tq - 0.12, -10.0), (tq, 30.0, "vao"), (tq + 0.1, 27.0), (tn, 29.0), (tn + 0.3, 3.0)])
            h_ = moc(tau, [(0, 0.0), (tq - 0.12, 4.0), (tq - 0.02, 12.0), (tq + 0.24, -30.0, "ra"), (tn, -32.0), (tn + 0.3, 0.0)])
            HB = (0.0, 0.5, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0)
            HH = (0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 1.0, 1.0, 1.0, 1.0)
            R = [b_ * HB[q] + (h_ - 2.0 * siet) * HH[q] for q in range(N_GAI)]
            nghieng = 0.0
        else:
            # dap: vươn thẳng thật cao, ngả ra sau, rồi gập ở khúc giữa bổ phần ngọn từ trên xuống: thành cái vòm chụp qua đầu đối thủ; ngọn
            # nảy lên một nhịp khi chạm đất
            m_ = moc(tau, [(0, 0.0), (0.3, -4.0), (tq - 0.14, -8.0), (tq, 38.0, "vao"), (tq + 0.07, 33.0), (tq + 0.16, 36.0), (tn, 36.0),
                           (tn + 0.3, 3.0)])
            n_ = moc(tau, [(0, 0.0), (tq, 0.0), (tq + 0.07, -9.0), (tq + 0.18, 4.0), (tn, 4.0), (tn + 0.3, 0.0)])
            HM = (0.0, 0.0, 0.3, 1.0, 1.0, 1.0, 0.7, 0.0, 0.0, 0.0)
            HN = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
            R = [(m_ + 1.5 * siet) * HM[q] + n_ * HN[q] for q in range(N_GAI)]
            nghieng = moc(tau, [(0, 0), (tq - 0.14, -7.0), (tq, 4.0, "vao"), (tn, 3.0), (tn + 0.3, 0)])
        for q, b in enumerate(dot):
            P.rot(b, ch * (R[q] + 3.0 * song * math.sin(0.9 * q) * (0.3 + 0.7 * q / (N_GAI - 1))))
        P.rot(g["goc"], ch * nghieng)

    def cast(t, P):
        nen(P, "idle_01", 0.0, True)
        w = moc(t, [(0, 0), (C_TRIEU, 1, "ra"), (C_NHA + 0.05, 1), (C_DUR - 0.2, 0)])
        # nhịp tay: gọi lên một lần, rồi mỗi cú quật của một dây là một lần tay chém xuống, bật lại
        kc = moc(t, [(0, 0), (C_TRIEU, 0), (C_MOC + 0.06, 0.8, "vao"), (C_MOC + 0.22, 0.1)])
        for g in GAI:
            kc += moc(t, [(g["quat"] - 0.12, 0), (g["quat"], 1.2, "vao"), (g["quat"] + 0.16, 0.0)])
        kc += moc(t, [(C_TROI - 0.1, 0), (C_TROI, 0.7), (C_NHA, 0.8), (C_NHA + 0.12, 0)])       # nắm tay kéo xuống giữ: siết
        r = rung(t, C_TROI, C_NHA, 10.0)
        tay(P, "x", 82.0 - 22.0 * kc, 104.0 - 34.0 * kc - 2.5 * r, w=w)          # CHỈ tay xa (bên phải hình) giơ lên; tay gần giữ thế thủ
        P.scale(TAY["x"]["nam"], 1 + 0.10 * w * (1 if t < C_TROI else 1 + 0.4 * r))
        tay(P, "g", REF["bone32"] - 10.0 * w, REF["bone33"] + 12.0 * w, w=w)     # tay gần ghì thấp sát hông
        # thân: ngả ra sau lấy đà rồi chúi tới theo từng cú quật
        ng = moc(t, [(0, 0), (0.22, 4.0), (C_TRIEU, 2.0)]) - 5.0 * kc * moc(t, [(C_TRIEU, 0), (C_MOC, 1)])
        ng *= moc(t, [(C_DUR - 0.5, 1), (C_DUR - 0.15, 0)])
        P.rot("bone4", 0.4 * ng)
        P.rot("bone5", 0.6 * ng)
        P.rot("tou", -0.5 * ng + 4.0 * w)
        gio(P, t, 0.7 + 0.8 * w, 1.1)
        sau(P)
        P.alpha["cau"] = 0.0
        for g in ds_gai:
            day_gai(P, g, t)

    # ---------------------------------------------------------------- skill: vốc hai tay lên quá đầu, tụ quả cầu dây leo → nhảy tới → đập xuống
    K_DUR = 3.2
    K_GIO = 0.46                 # hai tay giơ xong, gần nhau trên đầu: bắt đầu tụ
    K_DAY = 1.30                 # cầu đầy
    K_NHUN = 1.52                # nhún sâu nhất
    K_DAP = 2.02                 # nện xuống (trúng)
    K_GIU = 2.36                 # bắt đầu đứng dậy
    N0, N1, N2, N3 = 0.72, 1.44, 1.69, CD["skill_02"][0]                       # skill_02 của họ: nhún sâu, chạm đất, giữ, hết
    K_XA = 0.80 * cao

    def gio_nhay(t):
        """giờ trong skill_02 của họ ứng với giờ t của mình. Trước K_NHUN đứng yên ở dáng NHÚN SÂU (0,72 s) để pha dần từ thế thủ sang
        (đoạn 0–0,72 s của họ là chạy lấy đà: pha thẳng vào giữa chừng thì chân giật)."""
        if t < K_NHUN:
            return N0
        if t < K_DAP:
            return moc(t, [(K_NHUN, N0), (K_DAP, N1, "thang")])
        if t < K_GIU:
            return moc(t, [(K_DAP, N1), (K_GIU, N2, "thang")])
        return moc(t, [(K_GIU, N2), (K_DUR - 0.1, N3, "thang")])

    # dáng nhún của họ nằm cùng vòng với thế thủ: góc lệch quá nửa vòng thì bớt bội 360° (pha đi đường ngắn, không quay ngược cả vòng)
    LECH_N = {b: -360.0 * round(float(arr[int(round(N0 * 30))][0]) / 360.0) for b, arr in CD["skill_02"][1].items()}
    LECH_N = {b: v for b, v in LECH_N.items() if abs(v) > 1}
    if LECH_N:
        print("  skill: xương lệch vòng giữa thế thủ và dáng nhún:", LECH_N)

    # (bắp, cẳng) góc thế giới, LIÊN TỤC so với dáng gốc (bắp gần −161°, cẳng gần −108°; bắp xa −37°, cẳng xa 60°). Tay gần VỐC lên đi qua
    # phía dưới rồi phía trước thân (−161° → −90° → 0° → 96°), đập xuống quay ngược lại qua phía trước: không khoá nào lệch quá một vòng.
    GIO_ = {"g": (96.0, 80.0), "x": (84.0, 104.0)}                             # giơ quá đầu, hai nắm tay gần nhau
    DAP = {"g": (-62.0, -38.0), "x": (-58.0, -28.0)}                           # nện xuống phía trước

    def skill(t, P):
        tn = gio_nhay(t)
        wn = moc(t, [(K_DAY - 0.05, 0), (K_NHUN, 1)])                          # thế thủ → dáng nhún, pha êm suốt 0,27 s
        if wn < 1:
            nen(P, "idle_01", 0.0, True, w=1 - wn)
        if wn > 0:
            nen(P, "skill_02", tn, w=wn, bo=BO_TAY, lech=LECH_N)
        # tay: nền → giơ (vốc lên) → đập → về nền
        w_tay = moc(t, [(0, 0), (K_GIO, 1), (K_GIU + 0.1, 1), (K_GIU + 0.5, 0)])
        u_dap = moc(t, [(K_DAP - 0.2, 0), (K_DAP, 1, "vao")])
        r = rung(t, K_GIO, K_DAY + 0.1, 13.0) * moc(t, [(K_GIO, 0.2), (K_DAY, 1.0, "thang")])
        # lúc giơ: hai cổ tay nhắm hai điểm cố định phía trên ĐẦU (giải hai khúc tay), nên thân nhún, chúi hay nhảy thì hai nắm tay vẫn
        # ngang nhau cùng đỡ quả cầu (trước đây đặt góc cố định: thân chúi là một nắm tay tụt xuống, cầu như đỡ một tay)
        Wd = sk.the_gioi(P)
        dau_ = Wd["tou"][:2, 2]
        dang = (0.150 + 0.030 * moc(t, [(K_GIO, 0), (K_DAY, 1.0)])) * cao     # cầu lớn dần thì hai tay dang ra
        for ben, d in (("g", -1.0), ("x", 1.0)):
            gb, gc = giai_tay(Wd, ben, dau_ + np.array([d * dang + 0.03 * cao, 0.34 * cao]), GIO_[ben])
            b = gb + (DAP[ben][0] - gb) * u_dap
            c = gc + (DAP[ben][1] - gc) * u_dap
            tay(P, ben, b + 1.5 * r, c - 2.0 * r, w=w_tay)
        # gồng lúc tụ: lún xuống, ngả dần ra sau, rung
        ng = moc(t, [(0, 0), (0.2, -4.0), (K_GIO, 2.0), (K_DAY, 6.0), (K_NHUN, 0)])
        P.rot("bone4", 0.3 * ng)
        P.rot("bone5", 0.7 * ng + 0.8 * r)
        P.rot("tou", 0.9 * ng)
        # lao: bay tới trong lúc nhảy, ở lại tới khi đứng dậy rồi nhảy lùi về
        x = moc(t, [(K_NHUN, 0), (K_DAP, K_XA, "thang"), (K_GIU + 0.1, K_XA), (K_DUR - 0.12, 0)])
        y = 0.16 * cao * math.sin(math.pi * moc(t, [(K_GIU + 0.1, 0), (K_DUR - 0.12, 1, "thang")])) if t > K_GIU + 0.1 else 0.0
        P.move("move", x, y)
        gio(P, t, 0.8 + 1.4 * moc(t, [(K_GIO, 0), (K_DAY, 1)]) * (1 if t < K_DAP else 0.3), 0.9)
        sau(P)
        for sl_ in GAI_SLOT:
            P.alpha[sl_] = 0.0
        # quả cầu: nằm trên hai nắm tay, lớn dần; nện xuống thì bẹp rồi tan (nổ là việc của VFX)
        lon = moc(t, [(K_GIO, 0.0), (K_DAY, 1.0, "ra"), (K_DAP, 1.0), (K_DAP + 0.1, 1.25), (K_DAP + 0.2, 0.0)])
        P.alpha["cau"] = moc(t, [(K_GIO, 0), (K_GIO + 0.08, 1), (K_DAP + 0.08, 1), (K_DAP + 0.2, 0)])
        W = sk.the_gioi(P)
        Wm = W["move"]
        tam = np.zeros(2)
        for ben in "gx":
            Wb = W[TAY[ben]["nam"]]
            tam += (Wb @ np.array([sk.bones[sk.bi[TAY[ben]["nam"]]]["length"] * 0.7, 0.0, 1.0]))[:2] / 2
        nang = (0.06 + 0.30 * lon) * cao * (1 - 0.85 * u_dap)                   # cầu to thì nằm trên hai nắm tay
        dich = tam + np.array([0.10 * cao * u_dap, nang])
        loc = np.linalg.solve(Wm, np.array([dich[0], dich[1], 1.0]))[:2]
        P.move("cau", float(loc[0] - (cau0[0])), float(loc[1] - cau0[1]))
        bep = moc(t, [(K_DAP, 0), (K_DAP + 0.1, 1)])
        P.scale("cau", max(0.02, lon) * (1 + 0.25 * bep) * (1 + 0.03 * r), max(0.02, lon) * (1 - 0.35 * bep) * (1 - 0.03 * r))
        P.rot("cau", 200.0 * moc(t, [(K_GIO, 0), (K_DAY, 1.0, "vao")]) - 120.0 * moc(t, [(K_NHUN, 0), (K_DAP, 1, "vao")]))

    # ---------------------------------------------------------------- appear: mào lá nhú khỏi đất như chồi, ngọ nguậy, rồi cả người đội đất vọt lên, gồng gầm
    P_DUR = 2.1
    P_NHU = 0.30                 # hết đoạn chồi nhú, bắt đầu vọt lên
    P_LON = 0.72                 # lên hết
    P_GAM = 1.08                 # gồng hết cỡ
    P_SAU = 1.22 * cao           # lúc đầu cả người nằm dưới đất chừng này (mặt nạ mặt đất giấu đi)
    GONG = {"g": (-196.0, -288.0), "x": (16.0, 104.0)}                         # hai tay giương ngang, cẳng dựng lên

    def appear(t, P):
        nen(P, "idle_01", 0.0, True)
        y = moc(t, [(0, -P_SAU), (0.14, -P_SAU + 0.34 * cao, "ra"), (P_NHU, -P_SAU + 0.38 * cao), (P_LON - 0.1, 0.07 * cao, "ra"), (P_LON, -0.02 * cao),
                    (P_LON + 0.1, 0.0)])
        lac = math.sin(2 * math.pi * 5.0 * t) * moc(t, [(0, 0.3), (P_NHU, 1.0), (P_LON - 0.1, 1.0), (P_LON + 0.05, 0.0)])     # giãy thoát khỏi đất
        P.move("move", 2.5 * lac, y)
        P.rot("bone4", 2.2 * lac)
        P.rot("tou", -3.0 * lac)
        w = moc(t, [(0, 1), (P_NHU + 0.1, 1), (P_LON, 0.0)])                   # lúc còn dưới đất: hai tay khép sát thân
        tay(P, "g", -118.0, -84.0, w=w)
        tay(P, "x", -72.0, 96.0, w=w)
        g = moc(t, [(P_LON, 0), (P_GAM, 1, "ra"), (1.52, 1), (P_DUR - 0.15, 0)])
        r = rung(t, P_GAM - 0.05, 1.56, 12.0)
        for ben in "gx":
            tay(P, ben, GONG[ben][0] + 2.0 * r, GONG[ben][1] - 3.0 * r, w=g)
            P.scale(TAY[ben]["nam"], 1 + 0.10 * g)
        P.rot("bone5", 5.0 * g + 0.8 * r)
        P.rot("tou", 9.0 * g + 2.5 * r)
        gio(P, t, 1.0 + 2.2 * moc(t, [(0, 1), (P_NHU, 1), (P_LON, 0.5), (P_GAM, 1), (1.5, 1), (P_DUR, 0)]), 0.5)
        sau(P)
        an_chieu(P)
        a = moc(t, [(0, 0), (0.05, 1)])
        for sl in [s_["name"] for s_ in sk.slots if s_["name"] not in GAI_SLOT + ("cau", "cat")]:
            P.alpha[sl] = a

    # ---------------------------------------------------------------- die: ngã của họ, các lớp lá cụp xuống, rồi mờ dần
    D_DUR = CD["die_01"][0]
    TAN = 0.55

    def die(t, P):
        nen(P, "die_01", t)
        heo = moc(t, [(0, 0), (0.5, 1, "ra")])
        for tn in la_mem:
            n = MEM[tn][1]
            dau = -1.0 if tn.endswith(("1", "s1")) else 1.0
            for q in range(n):
                P.rot(f"x_{tn}_{q}", dau * (6.0 + 8.0 * q) * heo)
        sau(P)
        an_chieu(P)
        a = float(np.clip(1.0 - (t - D_DUR - 0.15) / (TAN - 0.2), 0.0, 1.0))
        for sl in [s_["name"] for s_ in sk.slots if s_["name"] not in GAI_SLOT + ("cau", "cat")]:
            P.alpha[sl] = a

    mem = info["mem"]
    return [Clip("appear", P_DUR, appear, ev=[(0.0, "nhu", ""), (P_NHU, "troi_len", ""), (P_GAM, "gam", "")], mem=mem),
            Clip("idle", I_DUR, idle, loop=True, mem=mem),
            Clip("walk", W_DUR, walk, loop=True, mem=mem),
            Clip("attack", A_DUR, attack, ev=[(A_TRUNG, "trung", "")], trung=A_TRUNG, mem=mem),
            Clip("cast", C_DUR, cast, ev=[(C_TRIEU, "trieu", "")] + [(g["moc"], "moc", g["ten"]) for g in GAI] +
                 [(g["quat"], "trung" if g["quat"] == C_QUAT else "quat", g["ten"]) for g in GAI] + [(C_TROI, "troi", ""), (C_NHA, "nha", "")],
                 trung=C_QUAT, mem=mem),
            Clip("skill", K_DUR, skill, ev=[(K_GIO, "tu", ""), (K_DAY, "day", ""), (K_NHUN + 0.12, "nhay", ""), (K_DAP, "trung", "")],
                 trung=K_DAP, mem=mem),
            Clip("hit", CD["hit_01"][0], hit, mem=mem),
            Clip("die", D_DUR + TAN, die, ev=[(0.55, "nga", "")], mem=mem)]


def ve_khung(sk, clips, ten, ts, sc=1.0, xuong=False):
    c = [x for x in clips if x.ten == ten][0]
    fr = hoat.nuong(sk, c)
    ve = soi.Ve(sk)
    Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
    Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
    ims = []
    for P in Ps:
        im = ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
        if xuong:
            W = sk.the_gioi(P)
            d = ImageDraw.Draw(im)
            x0, y0, x1, y1 = Bx
            for b in sk.bones:
                if b["name"].startswith(("bone3", "bone4", "tou", "zhixin", "x_vai")):
                    px = (W[b["name"]][0, 2] - x0) * sc
                    py = (y1 - W[b["name"]][1, 2]) * sc
                    d.ellipse([px - 4, py - 4, px + 4, py + 4], outline=(255, 0, 0), width=2)
        ims.append(im)
    cot = min(len(ims), 6)
    hang = (len(ims) + cot - 1) // cot
    out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, f"soi_{ten}.png")
    out.save(pth)
    print(pth, out.size)


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ] [xuong]
        ve_khung(sk, clips, a[1], [float(x) for x in a[2].split(",")], float(a[3]) if len(a) > 3 else 1.0, "xuong" in a)
        return
    cao = info["cao"]
    if a and a[0] == "nhe":                    # NC_DANG=2 NC_NHE=1: ghi bản nhẹ (rig + khung 0 idle + chiều cao) cho dạng 1 gộp tiến hóa
        idle = [c for c in clips if c.ten == "idle"][0]
        os.makedirs(RA, exist_ok=True)
        pickle.dump((sk, hoat.nuong(sk, idle)[0], cao), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    M, noi = sk, {}
    if NC.K == 1:
        # TIẾN HÓA nối liền: gộp bản nhẹ của dạng lớn (dựng ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun)
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, NC_DANG="2", NC_NHE="1"), check=True)
        sk2, idle2, cao2 = pickle.load(open(os.path.join(HERE, "inbox", f"{NC.CODE}_2", "rig", "_nhe.pkl"), "rb"))
        ti = cao / cao2
        M = tienhoa.gop(sk, sk2)
        end2 = tienhoa.doi_ten_pose(idle2, "n_")

        def gong(t, P):                         # con non: thụp xuống lấy hơi rồi gồng: ngực ưỡn, hai tay bung ra, đầu ngửa, rung
            g = hoat.cv(t, [(0, 0), (0.3, -0.5), (0.6, 1, "out"), (1.3, 1.2)])
            r = hoat.rung(t, 0.5, 1.35, moi=1)
            P.rot("bone5", 5.0 * g + 0.8 * r)
            P.rot("tou", 7.0 * g + 1.5 * r)
            P.rot("bone32", -12.0 * max(g, 0) + 1.5 * r)
            P.rot("bone36", 12.0 * max(g, 0) - 1.5 * r)
            for b_ in ("bone34", "bone38"):
                P.scale(b_, 1 + 0.10 * max(g, 0))
            for sl_ in GAI_SLOT + ("cau",):
                P.alpha[sl_] = 0.0

        def bung(t, P, fl):                     # dạng lớn: hiện ở dáng nghỉ của nó, ưỡn lên, hai tay bung ra, nắm tay phồng rồi về
            for b_, v in end2.t.items():
                P.t[b_] = list(v)
            P.rot("n_bone5", 5.0 * fl)
            P.rot("n_tou", 8.0 * fl)
            P.rot("n_bone32", -14.0 * fl)
            P.rot("n_bone36", 14.0 * fl)
            for b_ in ("n_bone34", "n_bone38"):
                P.scale(b_, 1 + 0.10 * fl)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=bung, mem=[])
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips, RA, TEN, TIEU_DE, dang=NC.K, so_dang=2, dung_yen=("cast",), lao=("skill",), far=("cast",), cao=cao,
                  ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=noi)


if __name__ == "__main__":
    main(sys.argv[1:])
