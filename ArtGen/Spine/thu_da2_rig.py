# -*- coding: utf-8 -*-
"""Tê Thiềm DẠNG 2 (thu_da_2; tướng 3 đảo Thổ, ải 10): hình của mình chạy trên ĐÚNG rig con gốc monster_3526 (dạng tiến hoá của 3525 trong game
gốc). Ghi chú: inbox/thu_da_2_ghichu.md. Cách làm như thu_da_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ (hai chân sau có IK: mẫu khung `l` của runtime đã nướng IK, transform vào biến đổi riêng), thêm `move` (cú lao;
  game nắn quãng ở clip khai lao), `day` (đáy thân, ở mặt đất: bẹp / phình), `tam` (tâm thân, cha của `all`), `mieng` (chỗ nhả tảng đá của
  chiêu mana, con của đầu all6, trục x chĩa hướng phun).
- MẢNH: ảnh của mình "đúng chỗ, đúng cỡ" (thu_da2_manh.py → inbox/thu_da_2/manh/, px C0 = concept vẽ lại trên bố cục con gốc, qua phép căn
  C0 → con gốc); mỗi slot là lưới phủ hình, đỉnh biến dạng như điểm tương ứng trên lưới cùng slot của họ (trong_so_goc; nhóm cùng bề mặt dùng
  chung trường trọng số). Khối gai `wuqi_*` = cụm lăng trụ pha lê hổ phách (vung như vung khối pha lê). MẮT vẽ SAU đầu (họ vẽ đầu đè mắt, mắt
  lộ qua lỗ trên ảnh đầu; đầu của mình kín). Thêm slot `mat_nham` (mắt nhắm vẽ bằng mã) để chớp. Lòng miệng + lưỡi (slot shetou) vẽ bằng mã,
  nửa trên bám đầu, nửa dưới bám hàm. Bỏ (ẩn): shadow, wuqi_011, youdabi_02 (C0 không có), meimao, yanjing_01 (đã liền trong đầu / mắt),
  yaodai_01..03 (đai vẽ liền trên eo), shouji.
- CHUYỂN ĐỘNG (Claude chọn, dựa clip gốc; đòn giống ý dạng 1 nhưng mạnh hơn):
    idle   = idle_01 (6 s: thở, đặt khối pha lê nằm ngang sau lưng rồi vác lại ở 1,5–3,3 s) + chớp mắt hai lần + khịt mũi;
    walk   = run_01; hit = hit_01 (nhắm mắt);
    attack = skill_01 nén nhịp: hạ khối pha lê ngang, nhún, LAO tới ĐÂM mũi pha lê (trúng 0,50 s), giữ, rút về;
    cast   = evolution_01: đứng ngả ra sau, khối vắt sau lưng, HÁ HÀM tụ (VFX hút đá vào miệng), rung hai dáng → PHUN TẢNG ĐÁ (đầu giật tới,
             hàm sập nửa, thân giật lùi) → chồm về;
    skill  = skill_04 đầu (chồm, giơ khối lên cao) → GỒNG giữ trên đầu, rung → NHẢY tới (khai lao) BỔ khối pha lê xuống trước mặt (trúng),
             quá đà, nảy về chỗ cũ, gầm ngắn (skill_04 đoạn há miệng) → về. Chọn bổ khối thay cho cuộn tròn lăn của dạng 1: rig dạng 2 có
             sẵn khối gai to vung được, không cần ảnh quả cầu; cú bổ từ trên đầu xuống nặng và rõ lực hơn cú lăn;
    appear = rơi từ trên xuống, đáp (bụi), múa khối pha lê (skill_03) rồi về idle;
    die    = die_01 (khối văng ra sau, ngã sấp) + nhắm mắt → mờ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/thu_da2_rig.py        → inbox/thu_da_2/rig/
    py -3 -I ArtGen/Spine/thu_da2_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]    → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/thu_da2_rig.py kiem                                              đo góc nhảy, bước dời giữa hai khung
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, khung, hoat, xuat, soi, luoi, trongso  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import thu_da2_manh as MN  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = MN.G
TEN_RIG = "thu_da_2"
D_PX = float(os.environ.get("TD2_DPX", "0.62"))
MANH = MN.MANH
RA = os.environ.get("TD2_RA") or os.path.join(G.BASE, "rig")
TAN = 0.40
FPS = 30.0
IMPACT = {"attack": (0.09, 0.55, 0.13), "cast": (0.10, 0.6, 0.13), "skill": (0.20, 1.1, 0.26, "#fff6c94d")}   # mạnh hơn dạng 1 một bậc

BO = {"shadow", "wuqi_011", "youdabi_02", "meimao", "yanjing_01", "yaodai_01", "yaodai_02", "yaodai_03", "shouji", "xiaba_02",
      "wuqi_03", "wuqi_04", "wuqi_05", "wuqi_06", "shenti_02", "shenti_03"}      # wuqi_02 = lớp lấp dưới gai phụ
# vẽ ngay sau đầu: mắt (+ mắt nhắm) rồi hàm dưới có răng nhô lên (họ vẽ cả hai trước đầu: mắt lộ qua lỗ trên ảnh đầu, hàm nấp sau đầu; đầu
# của mình kín, răng của mình đứng trước môi trên)
SAU_DAU = ["yanjing_02", "xiaba_01"]
NHOM_TRON = [("bozi_01", "bozi_02", "shenti_01", "yao"),       # đầu (to_01) KHÔNG trong nhóm: sọ cứng theo xương đầu (khỏi nhòe má khi ngửa)
             ("youdabi_01", "youxiaobi", "shouzhang", "shouzhi_01", "shouzhitou_01", "shouzhi_02", "shouzhitou_02", "shouzhi_03", "shouzhitou_03"),
             ("youdatui", "youxiaotui"), ("zuodatui", "zuoxiaotui")]
PHA_LE = ("wuqi_01", "wuqi_02", "wuqi_03", "wuqi_04", "wuqi_05", "wuqi_06", "wuqi_010", "wuqi_11", "wuqi_012")
CHAN_SAU = {"gan": ("all27", "all28", "all29"), "xa": ("all30", "all31", "all32")}
GAI_PHU_XOAY = {"all45": 0.45, "all46": 0.45}      # gai phụ xoay riêng (tới 78° ở gốc): giảm còn 45 %, khỏi lộ chỗ chúng che trên cụm


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


def anh_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    T = MN.tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    kq = D_PX * T["a"] / T["s"]
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def trong_so_goc(V, a0, ten, Wi):
    """mỗi điểm V biến dạng như điểm tương ứng trên lưới a0 của họ (ngoài lưới: kéo theo cạnh gần nhất)."""
    Q = np.array(a0["xy"], float).reshape(-1, 2)
    tr = np.array(a0["tris"]).reshape(-1, 3) if a0.get("tris") else None
    if a0.get("w"):
        Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in a0["w"]]
    else:
        bn = ten[a0["bone"]] if isinstance(a0["bone"], int) else a0["bone"]
        Wg = [{bn: 1.0}] * len(Q)
    if tr is None:                                            # hình chữ nhật một xương
        bn = list(Wg[0])[0]
        return [[(bn, *[float(v) for v in np.linalg.solve(Wi[bn], np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
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


PHA_TRONG_SO = {}
THAN_DUOI_DAU = ("shenti_01", "yao", "bozi_01", "bozi_02")
BY0 = {}
DA_GIAC = {}
A0_NHOM = {}
SIGMA = 18.0


def truong_chung(V, nhom, ten, Wi):
    R = {k: trong_so_goc(V, A0_NHOM[k], ten, Wi) for k in nhom}
    poly = {k: DA_GIAC[k].reshape(-1, 1, 2).astype(np.float32) for k in nhom}
    out = []
    for i, p in enumerate(V):
        d = {k: max(0.0, -cv2.pointPolygonTest(poly[k], (float(p[0]), float(p[1])), True)) for k in nhom}
        ph = {k: math.exp(-(d[k] / SIGMA) ** 2) for k in nhom}
        tot_ph = sum(ph.values())
        if tot_ph < 1e-9:
            kmin = min(d, key=d.get)
            ph = {k: 1.0 if k == kmin else 0.0 for k in nhom}
            tot_ph = 1.0
        acc = {}
        for k in nhom:
            f = ph[k] / tot_ph
            if f < 1e-4:
                continue
            for n, x, y, w in R[k][i]:
                e = acc.setdefault(n, [0.0, 0.0, 0.0])
                e[0] += w * f
                e[1] += w * f * x
                e[2] += w * f * y
        tot = sum(e[0] for e in acc.values()) or 1.0
        out.append([(n, e[1] / e[0], e[2] / e[0], e[0] / tot) for n, e in acc.items() if e[0] > 1e-6])
    return out


def da_giac_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    x0, y0, _, _ = DATJ[ten]["hop"]
    al = np.asarray(Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA"))[..., 3] > 100
    cs, _ = cv2.findContours(al.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea).reshape(-1, 2).astype(float) + np.array([x0, y0])
    return MN.tf()["c2w"](c)


def pha_rows(rows, rows_k, f_list):
    out = []
    for r0, r1, f in zip(rows, rows_k, f_list):
        acc = {}
        for (n, x, y, w), k in [(q, 1 - f) for q in r0] + [(q, f) for q in r1]:
            if w * k <= 1e-6:
                continue
            e = acc.setdefault(n, [0.0, 0.0, 0.0])
            e[0] += w * k
            e[1] += w * k * x
            e[2] += w * k * y
        tot = sum(e[0] for e in acc.values()) or 1.0
        out.append([(n, e[1] / e[0], e[2] / e[0], e[0] / tot) for n, e in acc.items()])
    return out


def gan_manh(sk, slot, ten_anh, a0, ten, Wi, xuong_cung=None, dat_lai=None):
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    T = MN.tf()
    trong_nhom = any(slot in g for g in NHOM_TRON)           # mảnh một xương của họ nhưng thuộc nhóm cùng bề mặt: vẫn dùng trường chung
    nhieu = xuong_cung is None and (trong_nhom or (bool(a0.get("tris")) and bool(a0.get("w"))))   # (khớp uốn mềm, dải chồng không văng ra)
    L = luoi.luoi_vung(im, buoc_vien=9.0, buoc_trong=15.0, vien=2, ten=slot, in_tk=False) if nhieu else luoi.luoi_o(im.width, im.height, 2, 2,
                                                                                                                   ten=slot)
    if dat_lai is not None:
        c, rong = dat_lai[0], dat_lai[1]
        kx = rong / im.width
        ky = (dat_lai[2] / im.height) if len(dat_lai) > 2 else kx
        V = np.stack([c[0] + (L.pts[:, 0] - im.width / 2) * kx, c[1] - (L.pts[:, 1] - im.height / 2) * ky], 1)
    else:
        Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
        V = T["c2w"](Px)
    if nhieu:
        nhom = next((g for g in NHOM_TRON if slot in g and all(k in DA_GIAC and k in A0_NHOM for k in g)), None)
        rows = truong_chung(V, nhom, ten, Wi) if nhom else trong_so_goc(V, a0, ten, Wi)
        if slot in THAN_DUOI_DAU:                              # phần thân lấn dưới đầu / hàm đi theo hẳn đầu / hàm: luôn khuất, không lộ mép
            for k in ("to_01", "xiaba_01"):
                if k not in DA_GIAC or k not in BY0:
                    continue
                poly = DA_GIAC[k].reshape(-1, 1, 2).astype(np.float32)
                fl = [float(np.clip((cv2.pointPolygonTest(poly, (float(p[0]), float(p[1])), True) + 3.0) / 6.0, 0.0, 1.0)) for p in V]
                if max(fl) > 0:
                    rows = pha_rows(rows, trong_so_goc(V, BY0[k], ten, Wi), fl)
        if slot in PHA_TRONG_SO and PHA_TRONG_SO[slot][0] in DA_GIAC:
            khac, R, fmax, a_khac = PHA_TRONG_SO[slot]
            poly = DA_GIAC[khac].reshape(-1, 1, 2).astype(np.float32)
            rows_k = trong_so_goc(V, a_khac, ten, Wi)
            fl = []
            for p in V:
                d = cv2.pointPolygonTest(poly, (float(p[0]), float(p[1])), True)
                fl.append(fmax * float(np.clip(1.0 - (-d) / R, 0.0, 1.0)) if d < 0 else fmax)
            rows = pha_rows(rows, rows_k, fl)
    else:
        b = xuong_cung or (ten[a0["bone"]] if isinstance(a0.get("bone"), int) else a0.get("bone"))
        if b is None:                                          # lưới nhiều xương nhưng gắn cứng: lấy xương nặng nhất
            ws = {}
            for wl in a0["w"]:
                for k, w in wl:
                    ws[ten[k]] = ws.get(ten[k], 0) + w
            b = max(ws, key=ws.get)
        Mb = Wi[b]
        rows = [[(b, *[float(v) for v in np.linalg.solve(Mb, np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L, V


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    chan = np.concatenate([np.array(by0[s]["xy"], float).reshape(-1, 2) for s in ("youxiaotui", "zuoxiaotui", "shouzhang", "shouzhitou_01",
                                                                                   "shouzhitou_02", "shouzhitou_03") if s in by0])
    y_day = float(chan[:, 1].min())
    Vb = np.concatenate([np.array(by0[s]["xy"], float).reshape(-1, 2) for s in ("shenti_01", "yao", "to_01")])
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
        if cha == "root":
            sk.xuong(b["name"], "tam", g[0] - float(tam[0]), g[1] - float(tam[1]), goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        elif cha == "shadow":
            continue
        else:
            sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    for g in NHOM_TRON:
        for k in g:
            if k in DATJ:
                DA_GIAC[k] = da_giac_manh(k)
                A0_NHOM[k] = by0[k]
    BY0.update(by0)
    if "to_01" in DATJ:
        DA_GIAC["to_01"] = da_giac_manh("to_01")
    if "xiaba_01" in DATJ:                                      # cổ trước sát hàm đi theo hàm (khỏi hở khi há)
        DA_GIAC["xiaba_01"] = da_giac_manh("xiaba_01")
        PHA_TRONG_SO["bozi_01"] = ("xiaba_01", 40.0, 1.0, by0["xiaba_01"])
    thu_tu = [s["name"] for s in I["slots"]]
    tong = [0, 0]
    for s in thu_tu:
        if s in BO or s in SAU_DAU:
            continue
        if s not in DATJ and s != "shetou":
            print(f"  (thiếu mảnh) {s}: bỏ")
            continue
        a0 = by0.get(s)
        if a0 is None:
            print(f"  (không có hình idle0) {s}: bỏ")
            continue
        sk.slot(s, "move", s)
        if s == "shetou":                                        # lòng miệng + lưỡi: nửa trên bám đầu, nửa dưới bám hàm
            T = MN.tf()
            hx0, hy0, hx1, hy1 = DATJ["xiaba_01"]["hop"]
            Pj = T["c2w"](np.array([[hx0, hy0], [hx1, hy1]], float))
            jw, jh = float(Pj[1, 0] - Pj[0, 0]), float(Pj[0, 1] - Pj[1, 1])
            c = np.array([Pj[0, 0] + 0.53 * jw, Pj[0, 1] - 0.30 * jh])     # phủ hết khe miệng tới mép trước hàm (khe trước mõm lúc há thấy lòng
            L, V = gan_manh(sk, s, s, {}, ten, Wi, xuong_cung="all6", dat_lai=(c, 0.90 * jw, 0.50 * jh))   # miệng tối, không thấy thân)
            yt, yb = float(V[:, 1].max()), float(V[:, 1].min())
            r_dau = [[("all6", *[float(v) for v in np.linalg.solve(Wi["all6"], np.array([q[0], q[1], 1.0]))[:2]], 1.0)] for q in V]
            r_ham = trong_so_goc(V, by0["xiaba_01"], ten, Wi)
            fl = []
            for q in V:
                u = (yt - q[1]) / max(1e-6, yt - yb)
                f = float(np.clip((u - 0.30) / 0.45, 0.0, 1.0))
                fl.append(f * f * (3 - 2 * f))
            rows = pha_rows(r_dau, r_ham, fl)
            Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
            sk.luoi_gan(s, s, L, trongso.cung(L.n, "move"), the_gioi=Vs)
            sk.atts[s][s]["verts"] = rows
        else:
            L, V = gan_manh(sk, s, s, a0, ten, Wi)
        tong[0] += L.n
        tong[1] += len(L.tris)
        if s == "to_01":
            for them in SAU_DAU:
                if them not in DATJ:
                    continue
                sk.slot(them, "move", them)
                L, V = gan_manh(sk, them, them, by0[them], ten, Wi)
                tong[0] += L.n
                tong[1] += len(L.tris)
                if them == "yanjing_02" and "mat_nham" in DATJ:
                    sk.slot("mat_nham", "move", "mat_nham", an=True)
                    gan_manh(sk, "mat_nham", "mat_nham", by0["yanjing_02"], ten, Wi)
    # chỗ nhả tảng đá: giữa hai hàm phía mõm, con của đầu
    hm = np.array(sk.atts["xiaba_01"]["xiaba_01"]["V"])
    x_m = float(hm[:, 0].max()) - 0.12 * float(np.ptp(hm[:, 0]))
    y_m = float(hm[:, 1].max()) + 4.0
    sk.xuong("mieng", "all6", x_m, y_m, goc=8.0, the_gioi=True)
    for e, m in (("trung", "khung trúng"), ("tu", "cast: bắt đầu tụ tảng đá trong miệng (VFX hút đá, bụi)"),
                 ("phun", "cast: phun tảng đá (đạn do VFX từ xương mieng)"), ("gong", "skill: giơ khối pha lê gồng trên đầu"),
                 ("nhay", "skill: nhảy tới"), ("cham_dat", "chạm đất (bụi tròn)"), ("gam", "gầm (bụi rung)"), ("khit", "idle: khịt mũi"),
                 ("lao", "attack: lao tới")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}, tâm ({tam[0]:.1f}, "
          f"{tam[1]:.1f}); mieng ({x_m:.0f}, {y_m:.0f})")
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
D_IDLE = 6.0                                     # idle_01 nguyên vòng
T_CHOP = (0.95, 4.35)                            # idle: chớp mắt
T_KHIT = 5.2                                     # idle: khịt mũi
D_ATTACK, T_DAM = 1.10, 0.55                     # attack: mũi pha lê chạm (skill_01 0,80 nén về)
LAO_A = 0.32                                     # attack: lao (× chiều cao) ở khung đâm; game nắn quãng
D_CAST, T_TU, T_PHUN = 1.55, 0.30, 0.95          # cast: há tụ, phun
T_CHOM0, T_GONG0, T_GONG1, T_BO, D_SKILL = 0.10, 0.50, 0.92, 1.12, 2.50   # skill: chồm, gồng, bổ (trúng)
T_NHAY = 0.96                                    # skill: rời đất
T_VE, T_GAM0, T_GAM1 = 1.62, 1.86, 2.20          # skill: đáp về chỗ cũ, gầm (vung khối ra sau 1,62 → 1,86)
LAO_S = 0.85                                     # skill: quãng nhảy (× chiều cao) ở khung bổ
T_DAP, D_APPEAR = 0.34, 2.05                     # appear: chạm đất, hết
D_DIE = 1.0 + TAN


def lam_clip(sk, info, cao=760.0):
    CD = chuyen_dong(info)

    def delta(goc, tau, lap=False):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        return {b: A[i0] * (1 - w) + A[i1] * w for b, A in R.items()}

    def ap(P, dd, chi=None, bo=()):
        for b, v in dd.items():
            if (chi is not None and b not in chi) or b in bo:
                continue
            r = float(v[0]) * GAI_PHU_XOAY.get(b, 1.0)
            if abs(r) > 1e-4:
                P.rot(b, r)
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))

    def tron(a, b, w):
        """trộn hai bộ độ lệch (nội suy thẳng từng thành phần; góc đã unwrap trong từng clip)."""
        out = {}
        z = np.array([0.0, 0.0, 0.0, 1.0, 1.0])
        for k in set(a) | set(b):
            out[k] = a.get(k, z) * (1 - w) + b.get(k, z) * w
        return out

    def dat(P, goc, tau, lap=False):
        ap(P, delta(goc, tau, lap))

    def dam(P, a):
        if a < 0.999:
            for s in sk.slots:
                P.alpha[s["name"]] = a * P.alpha.get(s["name"], s["alpha"])

    def nham(P, on=True):
        if "mat_nham" in sk.si:
            P.alpha["mat_nham"] = 1.0 if on else 0.0

    IDLE0 = delta("idle_01", 0.0)

    # ------------------------------------------------ idle
    def f_idle(t, P):
        dat(P, "idle_01", t, True)
        for tc in T_CHOP:
            if tc - 0.04 < t < tc + 0.08:
                nham(P)
        kk = hoat.cv(t, [(T_KHIT - 0.25, 0.0), (T_KHIT, 1.0, "io"), (T_KHIT + 0.30, 0.0, "io")])
        P.rot("all6", 3.0 * kk)
        P.rot("bone", -4.0 * kk)
        if T_KHIT - 0.03 < t < T_KHIT + 0.07:
            nham(P)

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)
        if 0.03 < t < 0.30:
            nham(P)

    # ------------------------------------------------ attack: hạ khối, nhún, lao tới đâm
    def f_attack(t, P):
        tau = tmap(t, [(0.0, 0.0), (0.26, 0.32, "io"), (0.44, 0.62, "io"), (T_DAM, 0.80, "in"), (0.76, 0.86, "out"), (D_ATTACK, 1.0, "io")])
        dat(P, "skill_01", tau)
        lao = hoat.cv(t, [(0.0, 0.0), (0.34, -0.04, "io"), (T_DAM, LAO_A, "in"), (0.78, LAO_A), (D_ATTACK - 0.05, 0.0, "io")])
        nhay = 0.06 * math.sin(math.pi * float(np.clip((t - 0.36) / (T_DAM - 0.36), 0, 1)))
        P.move("move", cao * lao, cao * nhay)
        k = math.exp(-((t - (T_DAM + 0.03)) / 0.05) ** 2)
        P.scale("day", 1 + 0.10 * k, 1 - 0.09 * k)
        P.rot("all18", -6.0 * k)                                 # tay vung quá đà một chút lúc chạm
        if T_DAM - 0.02 < t < T_DAM + 0.10:
            nham(P)

    # ------------------------------------------------ cast: đứng ngả ra sau, há hàm tụ, phun
    def f_cast(t, P):
        if t < 0.35:                                             # idle → dáng đứng gầm (evolution 0,2), trộn êm
            w = ease(t / 0.35, "io")
            ap(P, tron(IDLE0, delta("evolution_01", 0.20), w))
        elif t < T_PHUN - 0.06:                                  # giữ há tụ (evolution 0,2 → 1,0 chậm), rung hai dáng
            u = (t - 0.35) / (T_PHUN - 0.06 - 0.35)
            dat(P, "evolution_01", 0.20 + 0.75 * u)
            P.rot("all6", 1.4 * hoat.rung(t, 0.40, T_PHUN - 0.06, 2))
            P.rot("bone", -6.0 * ease(min(1.0, (t - 0.35) / 0.2), "out"))      # há thêm
        elif t < 1.12:                                           # PHUN: đầu giật tới, hàm sập nửa, thân giật lùi
            u = (t - (T_PHUN - 0.06)) / (1.12 - (T_PHUN - 0.06))
            dat(P, "evolution_01", 0.95 + 0.30 * ease(u, "out"))
        else:                                                    # chồm về idle
            u = (t - 1.12) / (D_CAST - 1.12)
            a = delta("evolution_01", 1.25 + 0.42 * min(1.0, u * 1.3))
            ap(P, tron(a, IDLE0, ease(u, "io")))
        giat = hoat.cv(t, [(T_PHUN - 0.05, 0.0), (T_PHUN + 0.03, 1.0, "out"), (1.25, 0.0, "io")])
        P.rot("all6", -9.0 * giat)
        P.rot("bone", 14.0 * giat)
        P.move("move", -0.05 * cao * giat, 0.0)
        P.rot("tam", 2.5 * giat)
        k = math.exp(-((t - (T_PHUN + 0.03)) / 0.05) ** 2)
        P.scale("day", 1 - 0.06 * k, 1 + 0.06 * k)

    # ------------------------------------------------ skill: chồm, giơ khối gồng, nhảy tới bổ, nảy về, gầm
    S_BO = delta("skill_01", 0.80)                               # dáng mũi pha lê chĩa tới (đích của cú bổ)

    def f_skill(t, P):
        if t < T_GONG0:                                          # chồm + giơ khối lên (skill_04 0 → 0,5)
            dat(P, "skill_04", 0.5 * ease(t / T_GONG0, "io"))
        elif t < T_NHAY:                                         # gồng giữ trên đầu (skill_04 0,5 → 0,7), rung hai dáng
            u = (t - T_GONG0) / (T_NHAY - T_GONG0)
            dat(P, "skill_04", 0.5 + 0.2 * u)
            P.rot("all18", 1.8 * hoat.rung(t, T_GONG0 + 0.05, T_NHAY - 0.02, 2))
            P.rot("all6", 1.2 * hoat.rung(t, T_GONG0 + 0.05, T_NHAY - 0.02, 2))
        elif t < T_BO:                                           # BỔ: từ dáng giơ cao xuống dáng chĩa tới, thêm hạ thấp
            u = ease((t - T_NHAY) / (T_BO - T_NHAY), "in")
            ap(P, tron(delta("skill_04", 0.70), S_BO, u))
            P.rot("all18", -22.0 * u)
            P.rot("all2", -6.0 * u)
        elif t < T_VE:                                           # quá đà, giữ, nảy về
            u = (t - T_BO) / (T_VE - T_BO)
            ap(P, tron(S_BO, delta("skill_04", 0.80), ease(max(0.0, (u - 0.35) / 0.65), "io")))
            qd = math.exp(-(t - T_BO) / 0.08)
            P.rot("all18", -22.0 * (1 - ease(max(0.0, (u - 0.35) / 0.65))) - 6.0 * qd)
            P.rot("all2", -6.0 * (1 - u))
        elif t < T_GAM0:                                         # vung khối ra sau lưng (skill_04 0,8 → 0,95), đều, chậm hơn gốc một chút
            u = (t - T_VE) / (T_GAM0 - T_VE)
            dat(P, "skill_04", 0.80 + 0.15 * u)
        elif t < T_GAM1:                                         # gầm (skill_04 0,95 → 1,5)
            u = (t - T_GAM0) / (T_GAM1 - T_GAM0)
            dat(P, "skill_04", 0.95 + 0.55 * u)
        else:                                                    # về (skill_04 1,5 → 2,0, liền mạch với đoạn gầm)
            u = (t - T_GAM1) / (D_SKILL - T_GAM1)
            dat(P, "skill_04", 1.50 + 0.50 * ease(u, "io"))
        # quãng nhảy: rời đất T_NHAY, chạm T_BO (đỉnh lao), nảy về T_VE
        if t < T_NHAY:
            x, y = -0.03 * ease(min(1.0, t / T_GONG0), "io"), 0.0
        elif t < T_BO:
            u = (t - T_NHAY) / (T_BO - T_NHAY)
            x, y = -0.03 + (LAO_S + 0.03) * ease(u, "in"), 0.18 * math.sin(math.pi * u)
        elif t < T_VE:
            u = (t - T_BO) / (T_VE - T_BO)
            x = LAO_S * (1 - ease(max(0.0, (u - 0.2) / 0.8), "io"))
            y = 0.16 * math.sin(math.pi * max(0.0, (u - 0.2) / 0.8))
        else:
            x, y = 0.0, 0.0
        P.move("move", cao * x, cao * y)
        b = math.exp(-max(0.0, t - T_BO) / 0.05) if t >= T_BO else 0.0
        P.scale("day", 1 + 0.16 * b, 1 - 0.16 * b)
        if t >= T_VE:
            b2 = math.exp(-(t - T_VE) / 0.05)
            P.scale("day", 1 + 0.10 * b2, 1 - 0.10 * b2)
        if T_BO - 0.02 < t < T_BO + 0.12:
            nham(P)

    # ------------------------------------------------ appear: rơi xuống, đáp, múa khối
    def f_appear(t, P):
        if t < T_DAP:
            u = t / T_DAP
            ap(P, delta("skill_03", 0.10))
            P.move("move", 0.0, cao * 1.2 * (1 - ease(u, "in")))
            dam(P, min(1.0, t / 0.10))
        elif t < T_DAP + 0.22:
            u = (t - T_DAP) / 0.22
            ap(P, delta("skill_03", 0.10))
            b = math.exp(-(t - T_DAP) / 0.06) * math.cos((t - T_DAP) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.14 * b, 1 - 0.14 * b)
        else:
            u = (t - T_DAP - 0.22) / (D_APPEAR - T_DAP - 0.22)
            dat(P, "skill_03", 0.10 + 1.60 * u)

    # ------------------------------------------------ die
    def f_die(t, P):
        dat(P, "die_01", t)
        if t > 0.12:
            nham(P)
        dam(P, float(np.clip(1.0 - (t - (D_DIE - TAN)) / (TAN - 0.05), 0.0, 1.0)))

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_DAP, "cham_dat", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True, ev=[(T_KHIT, "khit", "")]),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(0.34, "lao", ""), (T_DAM, "trung", "")], trung=T_DAM),
        Clip("cast", D_CAST, f_cast, ev=[(T_TU, "tu", ""), (T_PHUN, "phun", "")], trung=T_PHUN),
        Clip("skill", D_SKILL, f_skill, ev=[(T_GONG0, "gong", ""), (T_NHAY, "nhay", ""), (T_BO, "trung", ""), (T_VE, "cham_dat", ""),
                                             (T_GAM0, "gam", "")], trung=T_BO),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", D_DIE, f_die, ev=[(0.62, "cham_dat", "")]),
    ]
    return clips


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    clips = lam_clip(sk, info, cao)
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
            for s, b in (("to_01", "all6"), ("shenti_01", "all4"), ("wuqi_01", "all19"), ("shouzhang", "all11"), ("youxiaotui", "all29")):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.22 * cao:
                        xau.append(f"{i / 30:.2f}s {s} dời {d / cao:.2f} cao/khung")
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
        sc = float(a[3]) if len(a) > 3 else 0.35
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
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Tê Thiềm dạng 2 (thu_da_2): tướng 3 đảo Thổ", dang=2, so_dang=2,
                  dung_yen=("cast",), lao=("skill",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.8)


if __name__ == "__main__":
    main(sys.argv[1:])
