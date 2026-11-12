# -*- coding: utf-8 -*-
"""Rồng vây (rong_vay, tướng thứ 8 đảo Thủy): hình của mình chạy trên ĐÚNG rig của con gốc monster_3458. Ghi chú: inbox/rong_vay_ghichu.md.

Người dùng 2026-11-11: "làm giống 100% cánh gốc", "sao không gen theo đó ghép lại rồi đổi pose là được", "gen theo y hệt đúng tỉ lệ,
đúng hướng". Cách làm (như dự án vẫn vẽ đè lên rig aola):
- XƯƠNG: đủ mọi xương của họ (trừ xương mây và điểm điều khiển đường cong), đúng cha – con, đúng biến đổi riêng ở dáng gốc; đơn vị rig
  của mình = đơn vị của họ × KG.
- MẢNH: mỗi mảnh của mình (rong_vay.py: đặt sẵn đúng chỗ trên khung concept, tức là đúng chỗ part tương ứng của họ ở dáng gốc) dựng lưới
  dày, rồi mỗi đỉnh gắn để biến dạng ĐÚNG như điểm tương ứng trên lưới thưa của part đó (`gan_goc`: trọng số theo toạ độ trọng tâm,
  mỗi xương một điểm gắn riêng; đỉnh nằm ngoài lưới của họ bám điểm gần nhất). Dải cạnh cánh dùng nguyên lưới của họ + thanh trơn màu.
- CHUYỂN ĐỘNG: lấy mẫu clip của họ 30 khung/giây (biến đổi riêng đã áp của runtime, kể cả xương chạy trên đường cong đã được nướng:
  scan/monster_3458/sample_clips.json) → lệch so với dáng gốc cho mọi xương. Nhắm mắt: theo timeline đổi hình mắt của họ.
Xương, lưới và chuyển động là của nhà phát hành game gốc; hình là của mình. Như phần aola: dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/rong_vay_rig.py        → inbox/rong_vay_1/rig/ (xem.html, khung_*.png)
    py -3 -I ArtGen/Spine/rong_vay_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [luoi]           → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import rong_vay as RV  # noqa: E402
import rong_vay_bo_cuc as BC  # noqa: E402

TEN = "rong_vay_1"
RA = os.path.join(RV.BASE, "rig")
TI = 0.55                    # pixel concept → đơn vị rig
RES = 0.8                    # pixel concept → pixel ảnh atlas
SC = BC.SC                   # đơn vị rig con gốc → pixel concept (như sơ đồ bố cục)
KG = SC * TI                 # đơn vị rig con gốc → đơn vị rig của mình
BO = ("yun", "quxian")       # xương mây (không clip nào dùng), điểm điều khiển đường cong thân (đã nướng vào khoá)
BO_TEN = ("shadow",)
# mảnh của mình ← slot (part) của con gốc mà nó bám theo
BAM = {t: s for s, t in RV.TEN.items()}
BAM["mat_nham"] = "P_yanjing02"
CANH = ("canh_g_mang", "canh_g_song", "canh_x_mang", "canh_x_song")
CANH_DAI = {"canh_g_canh": "P_chibangR08_2", "canh_x_canh": "P_chibangR08_3"}     # dải cạnh cánh: nguyên lưới của họ
# clip của mình ← clip của họ
# clip game ← clip nguồn. rv_*: clip RIÊNG của mình, dựng ở tầng điều khiển của rig gốc bằng rong_vay_clip.py (người dùng 2026-11-12:
# appear uốn lượn bay vào rồi gầm; đánh thường quật đuôi; chiêu mana ngả người lấy đà cánh rồi quạt một phát; chiêu cuối biến tấu),
# runtime Spine thật nướng ra scan/sample_moi.json. Sự kiện lấy từ rong_vay_clip.SU_KIEN.
import rong_vay_clip as RC  # noqa: E402
CLIPS = [("appear", "rv_appear", False, RC.SU_KIEN["rv_appear"]), ("idle", "idle_01", True, []),
         ("attack", "rv_attack", False, RC.SU_KIEN["rv_attack"]), ("cast", "rv_cast", False, RC.SU_KIEN["rv_cast"]),
         ("skill", "rv_skill", False, RC.SU_KIEN["rv_skill"]), ("hit", "hit_01", False, []), ("die", "die_01", False, [])]
HIEN = 0.20                  # appear: hiện dần chừng này giây đầu (khung đầu trống)

# DẠNG (người dùng 2026-11-12: "làm dạng 1 đi"). Hình đang có (rồng trưởng thành, bám con gốc) là dạng 2 trong game; dạng 1 là rồng
# NON trên CÙNG rig, cùng lưới, cùng clip: chỉ đổi tỉ lệ dáng gốc của vài xương (xương con thừa hưởng) và vẽ lại da trong cùng khung
# part. Chọn bằng biến môi trường RV_DANG=non. Tỉ lệ đặt ở gốc từng chuỗi: cánh co về phía thân mà gốc cánh vẫn dính thân.
DANG = os.environ.get("RV_DANG", "")
TI_LE = {}
# THÂN NGẮN (người dùng 2026-11-12: "mặt nhìn non hơn rồi nhưng thân bạn cũng phải làm ngắn hơn"): co thân DỌC CHIỀU DÀI, giữ bề dày.
# Xương thân (trục x chạy dọc thân): chuỗi thân trước Q_shenti*, 8 đốt thân sau H_shenti* (đã nướng thành anh em dưới zhixin), chuỗi
# đuôi weiba*. Hệ số K_THAN áp ba chỗ: (1) toạ độ x riêng của MỌI xương con của một xương thân (đốt kế, đầu, gốc cánh, gốc vây) ×
# K: các khớp dọc thân xích lại; (2) vị trí các đốt thân sau và gốc đuôi (anh em dưới zhixin) co về đốt đầu H_shenti × K: vòng cuộn
# nhỏ lại; (3) toạ độ x của điểm gắn lưới trong hệ xương thân × K: da co theo chiều dài, bề dày giữ nguyên. Áp cho cả dáng gốc lẫn
# khoá dời của mọi clip. Không đổi tỉ lệ xương (đổi tỉ lệ lệch trục trên chuỗi FK có khớp gập làm xương con bị xiên).
K_THAN = 1.0                 # thân trước (cổ, ngực): chuỗi Q_shenti*
K_SAU = 1.0                  # thân sau (vòng cuộn): 8 đốt H_shenti*, cũng là hệ số co vị trí các đốt về H_shenti
K_DUOI = 1.0                 # đuôi: chuỗi weiba*
DAY_SAU = float(os.environ.get("RV_DAY_SAU", "0.86"))        # bề dày thân sau và đuôi của dạng non so với dạng 2
THAN = tuple(["Q_shenti"] + [f"Q_shenti{i}" for i in range(2, 6)] + ["H_shenti"] + [f"H_shenti{i}" for i in range(2, 9)]
             + ["weiba"] + [f"weiba{i}" for i in range(2, 6)])
THAN_SAU = tuple(["H_shenti"] + [f"H_shenti{i}" for i in range(2, 9)] + ["weiba"])      # anh em dưới zhixin, co về H_shenti
SUNG_NU = 1.0                # dạng non: sừng thu về gốc sừng thành nụ (hệ số co hình sừng quanh gốc)
_MANH0, _MANH_RIG0, _RES0 = RV.MANH, RV.MANH_RIG, RES


def cau_hinh(dang, res=None):
    """đặt dạng sắp dựng ("" = dạng 2 trưởng thành, "non" = dạng 1) và độ nét ảnh atlas; gọi TRƯỚC dung(). Cần khi một lần chạy dựng
    cả hai dạng (clip evolve của dạng 1 gộp bản nhẹ của dạng 2)."""
    global DANG, TI_LE, K_THAN, K_SAU, K_DUOI, SUNG_NU, TEN, RA, RES
    DANG, RES = dang, (res or _RES0)
    TI_LE, K_THAN, K_SAU, K_DUOI, SUNG_NU = {}, 1.0, 1.0, 1.0, 1.0
    TEN, RA = "rong_vay_1", os.path.join(RV.BASE, "rig")
    RV.MANH, RV.MANH_RIG = _MANH0, _MANH_RIG0
    if dang != "non":
        return
    # da của dạng non: inbox/rong_vay_non/manh/{part, part_va, part_noi} + mat_nham.png, canh_g_song.png (rong_vay_non.py)
    TEN = "rong_vay_non"
    RA = os.path.join(HERE, "inbox", "rong_vay_non", "rig")
    RV.MANH = os.path.join(HERE, "inbox", "rong_vay_non", "manh")
    RV.MANH_RIG = RV.MANH
    SUNG_NU = 0.42
    # lượt 2 "thân phải ngắn hơn": cả ba 0,72. Lượt 4 "phần đuôi vẫn dài, thu ngắn các part thân/đuôi lại chút": thân sau 0,62, đuôi 0,54
    K_THAN = float(os.environ.get("RV_K_THAN", "0.70"))
    K_SAU = float(os.environ.get("RV_K_SAU", "0.62"))
    K_DUOI = float(os.environ.get("RV_K_DUOI", "0.54"))
    TI_LE = {"tou": 1.26,
             "R_chibang11": 0.60, "R_chibang15": 0.60, "R_chibang18": 0.60, "chibangR08_4": 0.75,
             "L_chibang": 0.60, "L_chibang4": 0.60, "L_chibang7": 0.60}
    # vây ngắn lại (người dùng 2026-11-12, sau concept lượt 2: "làm vây của nó ngắn hơn chút nữa"): tỉ lệ đặt ở xương GỐC của từng vây
    # (gốc vây nằm trên thân nên vây co về phía thân). Vây lưng 0,74; vây tai, vây má 0,80; hai thuỳ vây đuôi 0,82.
    TI_LE.update({b: 0.74 for b in ("bone71", "bone73", "bone75", "bone76", "bone78", "bone79", "bone80", "bone83", "bone86",
                                    "bone89", "bone91", "bone92")})
    TI_LE.update({b: 0.80 for b in ("bone42", "bone44", "bone12", "bone15")})
    TI_LE.update({b: 0.82 for b in ("bone30", "bone33")})


cau_hinh(DANG)
TAN = 0.45                   # die: giữ dáng cuối rồi mờ dần chừng này giây
# người dùng 2026-11-11: "bỏ bớt vây ở thân đi để đỡ bị hiệu ứng vây lồng nhau": bỏ sáu vây nhỏ / khuất (lòng vòng cuộn, dưới thân,
# sau thân giữa), giữ năm vây buồm trên lưng và mép ngoài vòng cuộn (vay_07, 09, 10, 14, 15)
BO_VAY = ("vay_06", "vay_08", "vay_11", "vay_12", "vay_13", "vay_16")
# người dùng 2026-11-12: "phần sừng không rig xương, để cứng": sừng của con gốc là chùm lông mềm bám chuỗi 3 xương (bone36–38,
# bone39–41) nên uốn; của mình là sừng: mọi đỉnh bám 100% một xương (đầu), đi theo đầu, không uốn
CUNG = {"sung_s": "tou", "sung_t": "tou"}


def _cho_than(name, cha, x, y, x0, y0, x0s, y0s):
    """toạ độ riêng (đơn vị con gốc) của một xương sau khi co thân: (x, y) đang xét; (x0, y0) vị trí đốt H_shenti cùng lúc; (x0s, y0s)
    không dùng ở đây (để gọi cho gọn). Xem K_THAN."""
    if name in THAN_SAU:
        return x0 + K_SAU * (x - x0), y0 + K_SAU * (y - y0)
    if cha in THAN:
        return x * k_than(cha), y
    return x, y


def k_than(b):
    """hệ số co dọc chiều dài của một xương thân."""
    return K_DUOI if b.startswith("weiba") else K_SAU if b.startswith("H_shenti") else K_THAN


def co_da(sk, Wc, IB, ten):
    """DA co theo thân ngắn. Bản đầu nhân x của điểm gắn trong hệ TỪNG xương thân với K: ở chỗ thân uốn, hai khúc kề (bám hai xương
    lệch góc nhau) bị kéo lệch một đoạn ~ (1 − K) × nửa bề dày × góc gập → phía ngoài khúc cua hở, vành bụng lệch bậc, nét viền đứt
    (người dùng 2026-11-12: "các khớp này nối không match, chỗ bị hở, chỗ mất nét"). Cách đúng: đổi DÁNG GẮN bằng một phép dời
    chỉ phụ thuộc VỊ TRÍ: mỗi điểm da dời đúng bằng độ dời của điểm GẦN NÓ NHẤT trên trục thân (trục = đoạn gốc → mút của từng
    xương thân; trục mới = trục đã co), rồi tính lại điểm gắn theo ma trận dáng gắn MỚI của xương (Wc2). Ở dáng gắn mọi phần đóng
    góp của một đỉnh trùng nhau, hai khúc kề trùng nhau ở chỗ nối; bề dày giữ nguyên vì độ lệch ngang trục không đổi."""
    cha = {b["name"]: (ten[b["parent"]] if b["parent"] >= 0 else None) for b in IB}
    dai = {b["name"]: b["len"] * KG for b in IB}
    P0 = Wc["H_shenti"][:2, 2].copy()
    Wc2 = {}
    for b in IB:
        n, p_ = b["name"], cha[b["name"]]
        if n not in Wc:
            continue
        M = Wc[n].copy()
        O = Wc[n][:2, 2]
        if n in THAN_SAU:
            O2 = P0 + K_SAU * (O - P0)
        elif p_ in THAN and p_ in Wc2:
            loc = np.linalg.inv(Wc[p_]) @ np.array([O[0], O[1], 1.0])
            loc[0] *= k_than(p_)
            O2 = (Wc2[p_] @ loc)[:2]
        elif p_ is not None and p_ in Wc2:
            O2 = Wc2[p_][:2, 2] + (O - Wc[p_][:2, 2])
        else:
            O2 = O
        M[:2, 2] = O2
        Wc2[n] = M
    doan = {}
    for n in THAN:
        a = Wc[n][:2, 2]
        ax = Wc[n][:2, 0] * dai[n]
        doan[n] = (a, ax, Wc2[n][:2, 2], ax * k_than(n))

    def ky(n):                          # bề dày: thân sau thon dần (lỗ vòng cuộn mở thành lỗ nhỏ như concept, không bị bóp thành khe)
        return {"H_shenti": 0.95, "H_shenti2": 0.90}.get(n, DAY_SAU if (n.startswith("H_shenti") or n.startswith("weiba")) else 1.0)

    def doi(n, v):                      # độ dời của v: theo điểm gần nhất trên trục xương n, độ lệch khỏi trục nhân bề dày
        a, ax, a2, ax2 = doan[n]
        t = float(np.clip(np.dot(v - a, ax) / max(1e-9, np.dot(ax, ax)), 0.0, 1.0))
        f = a + t * ax
        return (a2 + t * ax2) + ky(n) * (v - f) - v

    inv2 = {n: np.linalg.inv(Wc2[n]) for n in THAN}
    dem = 0
    for hinhs in sk.atts.values():
        for h_ in hinhs.values():
            rows = h_.get("verts")
            if not (isinstance(rows, list) and rows and isinstance(rows[0], list)):
                continue
            moi = []
            for row in rows:
                tb = [(n, w) for n, x, y, w in row if n in THAN]
                if not tb:
                    moi.append(row)
                    continue
                v = sum(w * (Wc[n] @ np.array([x, y, 1.0]))[:2] for n, x, y, w in row) / max(1e-9, sum(r[3] for r in row))
                d = sum(w * doi(n, v) for n, w in tb) / sum(w for _, w in tb)
                r2 = []
                for n, x, y, w in row:
                    if n in THAN:
                        pw = (Wc[n] @ np.array([x, y, 1.0]))[:2] + d
                        q = inv2[n] @ np.array([pw[0], pw[1], 1.0])
                        r2.append((n, float(q[0]), float(q[1]), w))
                    else:
                        r2.append((n, x, y, w))
                moi.append(r2)
                dem += 1
            h_["verts"] = moi
    print(f"  co da theo trục thân: {dem} đỉnh bám xương thân")


def nap_goc():
    root = BC.sxs()
    scan = os.path.join(root, "scan", BC.MON)
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    atts = [a for a in D["atts"] if a["cur"] and a["type"].endswith("MeshAttachment")]
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    ox = (BC.W - (x1 - x0) * SC) / 2 - x0 * SC
    oy = (BC.H + (y1 - y0) * SC) / 2 + y0 * SC
    T = lambda x, y: (x * SC + ox, oy - y * SC)                           # noqa: E731  thế giới con gốc → khung concept
    c2r = lambda p: np.array([(p[0] - ox) * TI, (oy - p[1]) * TI])        # noqa: E731  khung concept → rig (= thế giới con gốc × KG)
    return D, T, c2r, root, scan


def gan_goc(sk, slot, hinh, V, att, ten, Wc):
    """cho lưới của mình (đỉnh V, toạ độ rig) biến dạng ĐÚNG như lưới thưa của con gốc (att): mỗi đỉnh của mình là một điểm nằm trong
    một tam giác của họ (toạ độ trọng tâm β). Lưới thưa nội suy VỊ TRÍ ba góc:
    vị trí = Σ β_k · Σ_b w_b(k) M_b M_b0⁻¹ v_k = Σ_b M_b M_b0⁻¹ [Σ_k β_k w_b(k) v_k]. Nên mỗi đỉnh của mình bám xương b với trọng số
    W_b = Σ_k β_k w_b(k) và ĐIỂM GẮN RIÊNG cho từng xương q_b = Σ_k β_k w_b(k) v_k / W_b (định dạng lưới Spine cho phép mỗi xương
    một điểm gắn). Chỉ nội suy trọng số (một điểm gắn chung) thì bên trong tam giác gấp khác họ: màng cánh nhăn khi các chuỗi bắt chéo.
    Đỉnh nằm NGOÀI lưới của họ (hình mình rộng hơn): bám như điểm gần nhất c trên lưới, cộng nguyên khoảng lệch (p − c) vào điểm gắn
    của từng xương. Kéo dài mặt phẳng tam giác gần nhất thì tam giác mép dẹt phóng đại chuyển động: gốc sống cánh giật, chồi ra.
    Wc: ma trận thế giới của xương ở DÁNG GỐC CÓ RÀNG BUỘC của họ (đường cong thân đã áp). Lưới của họ gắn theo dáng đó, còn dáng
    gốc của rig mình là biến đổi riêng chưa áp ràng buộc (xương thân sau lệch tới 9 đơn vị): điểm gắn phải tính bằng Wc, không
    bằng sk.W0, thì khi clip đặt lại đúng biến đổi của họ lưới mới về đúng chỗ."""
    Q = np.array(att["xy"], float).reshape(-1, 2) * KG
    tr = np.array(att["tris"]).reshape(-1, 3)
    Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in att["w"]]
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)

    def gan_canh(p, a, b):
        d = b - a
        t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T), t

    inv = {}
    rows, ngoai, xa = [], 0, 0.0
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
        else:                                  # ngoài lưới: điểm gần nhất trên cạnh của một tam giác
            ngoai += 1
            best = None
            for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                dist, t = gan_canh(p, pa, pb)
                j = int(np.argmin(dist))
                if best is None or dist[j] < best[0]:
                    w3 = [0.0, 0.0, 0.0]
                    w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                    best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
            dmin, i, be, c = best
            lech = p - c
            xa = max(xa, dmin)
        acc = {}
        for vi, bw in zip(tr[i], be):
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Q[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5 or n not in sk.bi:
                continue
            if n not in inv:
                inv[n] = np.linalg.inv(Wc[n])
            g = q / w + lech
            lp = inv[n] @ np.array([g[0], g[1], 1.0])
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh]["verts"] = rows
    return ngoai, xa


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc):
    """slot dùng NGUYÊN lưới của con gốc (đỉnh, tam giác, uv, trọng số) với ảnh của mình đã nằm đúng khung ảnh vùng của part đó."""
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2) * KG
    sk.slot(slot, "move", anh_ten)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][anh_ten]["verts"] = rows
    return L


def gan_va(sk, slot, anh_ten, att, ten, Wc):
    """slot có bản vá (manh/part_va: mép lẹm chỗ con gốc khoét cắm vây đã làm trơn, 2026-11-12): ảnh vẫn đúng khung part nhưng hình
    bóng thò ra ngoài lưới của họ (lưới họ khoét theo vết lẹm, dùng nguyên thì phần vá bị xén). Dựng lưới của mình phủ đủ ảnh; mỗi
    đỉnh đặt vào thế giới qua lưới của họ trong hệ uv (toạ độ trọng tâm; ngoài lưới thì kéo dài mặt phẳng tam giác gần nhất, phần vá
    chỉ thò vài px), rồi bám xương bằng gan_goc như các mảnh tự vẽ."""
    im = sk.images[anh_ten]
    k_ = RES / TI
    L = luoi.luoi_vung(im, buoc_vien=7 * k_, buoc_trong=10 * k_, ten=slot, in_tk=False)
    U = np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    Q = np.array(att["xy"], float).reshape(-1, 2) * KG
    tr = np.array(att["tris"]).reshape(-1, 3)
    A, B_, C = U[tr[:, 0]], U[tr[:, 1]], U[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)
    tam = (A + B_ + C) / 3
    V = []
    for p in L.pts:
        v2 = p - A
        b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
        b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
        i = int(ok[0]) if len(ok) else int(np.argmin(np.hypot(*(tam - p).T)))
        V.append(b0[i] * Q[tr[i, 0]] + b1[i] * Q[tr[i, 1]] + b2[i] * Q[tr[i, 2]])
    V = np.array(V)
    sk.slot(slot, "move", anh_ten)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V)
    ng, xa = gan_goc(sk, slot, anh_ten, V, att, ten, Wc)
    return L, ng, xa


def dung():
    import cv2
    import to_manh
    D, T, c2r, root, scan = nap_goc()
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    giu = [b for b in IB if not b["name"].startswith(BO) and b["name"] not in BO_TEN]

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này; clip của họ dời xương riêng nên nó đứng yên
    p0s = next((b["x"], b["y"]) for b in IB if b["name"] == "H_shenti")
    for b in giu:
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        k_ = TI_LE.get(b["name"], 1.0)                 # tỉ lệ dáng gốc riêng của dạng (dạng non: đầu to, cánh nhỏ)
        bx, by = _cho_than(b["name"], cha, b["x"], b["y"], p0s[0], p0s[1], p0s[0], p0s[1])
        sk.xuong(b["name"], "move" if cha == "root" else cha, bx * KG, by * KG, goc=b["rot"], dai=b["len"] * KG,
                 sx=b["sx"] * k_, sy=b["sy"] * k_)
    # kiểm: xương của mình trùng xương của họ ở dáng gốc
    lech = max(float(np.hypot(sk.goc_tg(b["name"])[0] - b["x"] * KG, sk.goc_tg(b["name"])[1] - b["y"] * KG)) for b in D["bones"] if b["name"] in sk.bi)
    print(f"{len(sk.bones)} xương; dáng gốc lệch xương của con gốc tối đa {lech:.3f} đơn vị rig")

    by_slot = {a["slot"]: a for a in D["atts"]}
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    # xương miệng (2026-11-12, đưa vào game suất han_ngac): con gốc không có, mỏ là lưới bám nhiều xương. Đặt ở khe giữa hai mỏ, ngay
    # sau chóp (concept: chóp mỏ trên 1215,229, mỏ dưới 1214,225), theo hệ xương đầu ở DÁNG CÓ RÀNG BUỘC (Wc), như mọi điểm gắn
    # → game.muzzle (chỗ phun nước của chiêu mana) do xuat.thong_tin_tran lấy từ xương "mieng" ở khung trúng của clip cast
    lp = np.linalg.solve(Wc["tou"], np.array([*c2r((1200.0, 233.0)), 1.0]))
    sk.xuong("mieng", "tou", float(lp[0]), float(lp[1]))
    thu_tu = [t for _, t in RV.thu_tu() if t not in BO_VAY]
    thu_tu.insert(thu_tu.index("dau") + 1, "mat_nham")
    thu_tu.insert(thu_tu.index("canh_g_song"), "canh_g_canh")      # dải cạnh cánh: dưới lớp sẫm, trên màng (như slot của con gốc)
    thu_tu.insert(thu_tu.index("canh_x_song"), "canh_x_canh")
    if os.path.exists(os.path.join(RV.MANH, "part", "P_erduo.png")):       # mào trên đỉnh đầu: part riêng của rig, vẽ ngay DƯỚI đầu
        thu_tu.insert(thu_tu.index("dau"), "may")
        BAM["may"] = "P_erduo"
    if os.path.exists(os.path.join(RV.MANH, "part", "P_yuqi02.png")):      # vây tai nhỏ (concept không có; vẽ theo khung part của rig)
        thu_tu.insert(thu_tu.index("sung_t") + 1, "tai_nho")
        BAM["tai_nho"] = "P_yuqi02"
    # ảnh dải cạnh cánh: của họ là một thanh trơn một màu, không viền (lưới tự nắn thành hình); của mình: cùng hình bóng thanh đó,
    # tô màu sống cánh của mình (trung vị trên mảnh sống cánh) có vân nhẹ
    _, gimgs = to_manh.nap(os.path.join(root, "web", "assets", "Monster", BC.MON), BC.MON)
    bar_a = gimgs["P_chibangR08_2"].split()[3]
    bw, bh = max(8, round(bar_a.width * 2 * SC * RES)), max(4, round(bar_a.height * 2 * SC * RES))
    sp = np.asarray(Image.open(os.path.join(RV.MANH, "canh_g_song.png")).convert("RGBA"))
    thit = (sp[..., 3] > 200) & (sp[..., :3].max(axis=2) > 115)
    mau = np.median(sp[..., :3][thit], axis=0)
    rng = np.random.RandomState(3)
    bar = np.clip(mau[None, None] + rng.normal(0, 5, (bh, bw, 1)), 0, 255).astype(np.uint8)
    bar = np.dstack([np.broadcast_to(bar, (bh, bw, 3)), np.asarray(bar_a.resize((bw, bh), Image.LANCZOS))])
    sk.anh("canh_canh", anh.loang_mau(Image.fromarray(bar, "RGBA")))
    tong = [0, 0]
    k_ = RES / TI
    for t in thu_tu:
        if t in CANH_DAI:
            a = by_slot[CANH_DAI[t]]
            uv = np.array(a["uv"], float).reshape(-1, 2)
            L = luoi.Luoi(uv * np.array([bw, bh]), np.array(a["tris"]).reshape(-1, 3), a["hull"], a["hull"], bw, bh, ten=t)
            V = np.array(a["xy"], float).reshape(-1, 2) * KG
            W = trongso.chuan([{ten[k]: w for k, w in ws if w > 0.003} for ws in a["w"]], toi_da=4)
            sk.slot(t, "move", "canh_canh")
            sk.luoi_gan(t, "canh_canh", L, W, the_gioi=V)
            # điểm gắn tính bằng ma trận dáng gốc CỦA HỌ (Wc), không bằng dáng gốc của sk: dạng non đổi tỉ lệ xương cánh ở dáng gốc,
            # gắn theo sk.W0 thì dải cạnh giữ nguyên cỡ thế giới (thò dài khỏi cánh đã co)
            rows = []
            for p_, ws in zip(V, a["w"]):
                row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p_[0], p_[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.003]
                tot_ = sum(r[3] for r in row) or 1.0
                rows.append([(n, x, y, w / tot_) for n, x, y, w in row])
            sk.atts[t]["canh_canh"]["verts"] = rows
            tong[0] += L.n
            tong[1] += len(L.tris)
            continue
        if DANG == "non" and t == "mat_nham":
            # mắt nhắm của dạng non: mắt trên da mới to hơn và lệch chỗ so với mảnh mí của dạng 2 (mí chỉ che một phần, lòi viền hổ
            # phách). Dựng mí ngay từ ảnh đầu: vùng hổ phách + con ngươi nới 4 px tô màu da đầu, kẻ một nét mắt nhắm; slot dùng
            # nguyên lưới của ĐẦU nên mí luôn nằm đúng trên mắt.
            hd = np.asarray(sk.images["dau"].convert("RGBA")).copy()
            rr, gg, bb = (hd[..., i].astype(int) for i in range(3))
            hp = (hd[..., 3] > 127) & (rr > 190) & (gg > 110) & (bb < 110)
            if hp.sum() > 30:
                k5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
                vung = cv2.dilate(cv2.morphologyEx(hp.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))), k5).astype(bool)
                da = (hd[..., 3] > 127) & (bb > 170) & (bb - rr > 60)
                mau_da = np.median(hd[..., :3][da], axis=0) if da.any() else np.array([108, 134, 220])
                mi = np.zeros_like(hd)
                mi[vung, :3] = mau_da
                mi[vung, 3] = 255
                ys, xs = np.nonzero(vung)
                cx, cy, bw_ = xs.mean(), ys.mean(), xs.max() - xs.min()
                pts_ = np.array([[cx - 0.36 * bw_ + i * 0.72 * bw_ / 12, cy + 0.10 * bw_ * (1 - ((i - 6) / 6.0) ** 2)] for i in range(13)], np.int32)
                tam_ = np.ascontiguousarray(mi[..., :3])
                cv2.polylines(tam_, [pts_], False, (43, 33, 24), 3, cv2.LINE_AA)
                mi[..., :3] = tam_
                sk.anh(t, anh.loang_mau(Image.fromarray(mi, "RGBA")))
                L = gan_nguyen(sk, t, t, by_slot["P_tou"], ten, Wc)
                for sl_ in sk.slots:
                    if sl_["name"] == t:
                        sl_["alpha"] = 0.0
                tong[0] += L.n
                tong[1] += len(L.tris)
                print(f"  {t:12s} ← mí dựng từ ảnh đầu ({int(vung.sum())} px), lưới của P_tou")
                continue
        a = by_slot[BAM[t]]
        pg = os.path.join(RV.MANH, "part", BAM[t] + ".png")  # mảnh vẽ ĐÚNG KHUNG ảnh vùng của part (rong_vay.py cat_part): nguyên lưới của họ
        if os.path.exists(pg):
            # thu nhỏ ở dạng nhân sẵn alpha (RGBa): điểm trong suốt còn mang màu giấy trắng, thu nhỏ RGBA thường sẽ loang trắng
            # vào mép → vạch trắng ở chỗ nối đã xoá mực
            pn = lambda sl: os.path.join(RV.MANH, "part_noi", sl + ".png")          # noqa: E731  bản đã xoá vạch mực chỗ nối (noi_part)
            nap = lambda f: (lambda g: anh.loang_mau(g.resize((max(2, round(g.width / RV.PART_Z * 2 * SC * RES)),   # noqa: E731
                                                                 max(2, round(g.height / RV.PART_Z * 2 * SC * RES))), Image.LANCZOS).convert("RGBA")))(Image.open(f).convert("RGBA").convert("RGBa"))
            pv = os.path.join(RV.MANH, "part_va", BAM[t] + ".png")              # bản vá mép lẹm (gan_va)
            if os.path.exists(pv):
                sk.anh(t, nap(pv))
                L, ng, xa = gan_va(sk, t, t, a, ten, Wc)
                ghi = f"  {t:12s} ← {BAM[t]:16s} bản vá mép lẹm, lưới của mình {L.n} đỉnh ({ng} đỉnh ngoài lưới họ, xa nhất {xa:.1f})"
            else:
                sk.anh(t, nap(pn(BAM[t]) if os.path.exists(pn(BAM[t])) else pg))
                L = gan_nguyen(sk, t, t, a, ten, Wc)
                ghi = f"  {t:12s} ← {BAM[t]:16s} mảnh vẽ đúng khung part, nguyên lưới của họ {L.n} đỉnh"
                if t in CUNG:                                # mảnh cứng: bám trọn một xương (điểm gắn = vị trí dáng gốc trong hệ xương đó)
                    inv_ = np.linalg.inv(Wc[CUNG[t]])
                    Pq = np.array(a["xy"], float).reshape(-1, 2) * KG
                    if SUNG_NU != 1.0:                       # nụ sừng: co hình sừng về GỐC sừng (nhóm đỉnh gần tâm đầu nhất)
                        tam = (np.array(by_slot["P_tou"]["xy"], float).reshape(-1, 2) * KG).mean(axis=0)
                        d_ = np.hypot(*(Pq - tam).T)
                        goc_ = Pq[d_ <= np.quantile(d_, 0.3)].mean(axis=0)
                        Pq = goc_ + SUNG_NU * (Pq - goc_)
                    sk.atts[t][t]["verts"] = [[(CUNG[t], *[float(v) for v in (inv_ @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)]
                                              for p in Pq]
                    ghi += f", CỨNG theo xương {CUNG[t]}"
            tong[0] += L.n
            tong[1] += len(L.tris)
            if t == "than_6":                                # con gốc dùng lại ảnh khúc đuôi cho slot P_shenti07
                a7 = t
                if os.path.exists(pn("P_shenti07")):         # cùng ảnh nhưng chỗ nối khác → bản xoá vạch nối riêng
                    a7 = "than_7"
                    sk.anh(a7, nap(pn("P_shenti07")))
                L7 = gan_nguyen(sk, "than_7", a7, by_slot["P_shenti07"], ten, Wc)
                tong[0] += L7.n
                tong[1] += len(L7.tris)
                ghi += f"; than_7 ← P_shenti07 cùng ảnh, {L7.n} đỉnh"
            print(ghi)
            continue
        pm = os.path.join(RV.MANH_RIG, t + ".png")          # bản đã làm liền chỗ đầu đè lên cổ (rong_vay.py noi)
        full = Image.open(pm if os.path.exists(pm) else os.path.join(RV.MANH, t + ".png")).convert("RGBA")
        if t == "vay_duoi":                                  # cuống đuôi dài của mình nằm xa lưới vây đuôi của họ: bỏ (đã có khúc than_7)
            hull = np.array([T(x, y) for x, y in np.array(a["xy"], float).reshape(-1, 2)[:a["hull"]]], np.int32)
            hm = np.zeros((BC.H, BC.W), np.uint8)
            cv2.fillPoly(hm, [hull], 1)
            hm = cv2.dilate(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (71, 71))).astype(bool)
            F_ = np.asarray(full).copy()
            F_[..., 3][~hm] = 0
            full = Image.fromarray(F_, "RGBA")
        if t in CANH:                                        # phần khuất (GPT vẽ bù) thò xa khỏi lưới cánh của họ: bỏ, kẻo lúc vỗ chồi ra
            hull = np.array([T(x, y) for x, y in np.array(a["xy"], float).reshape(-1, 2)[:a["hull"]]], np.int32)
            hm = np.zeros((BC.H, BC.W), np.uint8)
            cv2.fillPoly(hm, [hull], 1)
            hm = cv2.dilate(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(bool)
            lo = cv2.dilate(RV.vung(t)[0].astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))).astype(bool)
            F_ = np.asarray(full).copy()
            bo = (F_[..., 3] > 0) & ~hm & ~lo
            if bo.any():
                F_[..., 3][bo] = 0
                full = Image.fromarray(F_, "RGBA")
        bb = full.getbbox()
        im = full.crop(bb)
        im = anh.loang_mau(im.resize((max(2, round(im.width * RES)), max(2, round(im.height * RES))), Image.LANCZOS))
        sk.anh(t, im)
        dat = Dat(*c2r((bb[0], bb[1])), neo=(0.0, 0.0), ti=TI / RES)
        nho = min(im.size) < 60 * k_
        bv, bt = (6, 8.5) if nho else (7, 10)
        L = luoi.luoi_vung(im, buoc_vien=bv * k_, buoc_trong=bt * k_, ten=t, in_tk=False)
        V = dat.ra(L.pts, im.width, im.height)
        sk.slot(t, "move", t, an=(t == "mat_nham"))
        sk.luoi_gan(t, t, L, trongso.cung(L.n, "move"), dat=dat)                # giữ chỗ; gan_goc ghi đè
        ng, xa = gan_goc(sk, t, t, V, a, ten, Wc)
        if t in CUNG:                                        # mảnh cứng: bám trọn một xương, điểm gắn = vị trí dáng gốc trong hệ xương đó
            inv_ = np.linalg.inv(Wc[CUNG[t]])
            sk.atts[t][t]["verts"] = [[(CUNG[t], *[float(v) for v in (inv_ @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        tong[0] += L.n
        tong[1] += len(L.tris)
        print(f"  {t:12s} ← {BAM[t]:16s} {L.n:4d} đỉnh, {ng:3d} đỉnh ngoài lưới của họ (xa nhất {xa:5.1f})" + (f", lưới hở {L.ho} px" if L.ho else ""))
        if t == "than_6":
            # con gốc dùng lại ảnh khúc đuôi cho slot P_shenti07 (khúc nối khúc đuôi với vây đuôi). Của mình: nướng mảnh than_6 vào
            # khung uv của P_shenti06 (mỗi tam giác lưới: chỗ đứng trên khung concept → chỗ trong ảnh vùng), rồi slot than_7 dùng
            # nguyên lưới P_shenti07 của họ (đỉnh, tam giác, uv, trọng số) với ảnh đó
            from quai.soi import _tris
            g6 = gimgs["P_shenti06"]
            w7, h7 = round(g6.width * 2 * SC * RES), round(g6.height * 2 * SC * RES)
            uv6 = np.array(a["uv"], float).reshape(-1, 2) * np.array([w7, h7])
            src = np.array([T(x, y) for x, y in np.array(a["xy"], float).reshape(-1, 2)])
            lay = Image.new("RGBa", (w7, h7), (0, 0, 0, 0))
            _tris(lay, full.convert("RGBa"), uv6, src, np.array(a["tris"]).reshape(-1, 3))
            sk.anh("than_7", anh.loang_mau(lay.convert("RGBA")))
            L7 = gan_nguyen(sk, "than_7", "than_7", by_slot["P_shenti07"], ten, Wc)
            tong[0] += L7.n
            tong[1] += len(L7.tris)
            print(f"  than_7       ← P_shenti07 (ảnh than_6 nướng vào khung uv P_shenti06, {w7} x {h7}), nguyên lưới của họ {L7.n} đỉnh")
    print(f"{len(thu_tu)} mảnh, {tong[0]} đỉnh, {tong[1]} tam giác")
    if min(K_THAN, K_SAU, K_DUOI) != 1.0:
        co_da(sk, Wc, IB, ten)
    for e, m in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả"), ("het_phun", "hết nhả"), ("gam", "chiêu cuối bung"),
                 ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]])


def chuyen_dong(sk, info):
    """clip của con gốc → {clip: (dài giây, {xương: mảng (số khung, 5) = xoay độ, dời x, y (đơn vị rig của mình), tỉ lệ x, y nhân}, mắt
    nhắm từng khung)}: lệch của biến đổi RIÊNG đã áp (runtime Spine) so với dáng gốc."""
    S = json.load(open(os.path.join(info["scan"], "sample_clips.json"), encoding="utf-8"))
    moi = os.path.join(info["scan"], "sample_moi.json")          # clip riêng của mình (rong_vay_clip.py mau)
    if os.path.exists(moi):
        S.update(json.load(open(moi, encoding="utf-8")))
    IB, ten = info["IB"], info["ten"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    i_nham = info["slots"].index("P_yanjing02")
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        i0 = ten.index("H_shenti")
        p0s = (IB[i0]["x"], IB[i0]["y"])
        for i in ids:
            b0 = IB[i]
            cha = ten[b0["parent"]] if b0["parent"] >= 0 else None
            sx_, sy_ = _cho_than(b0["name"], cha, b0["x"], b0["y"], p0s[0], p0s[1], 0, 0)
            A = np.array([[F["l"][i][2] - b0["rot"],
                           (_cho_than(b0["name"], cha, F["l"][i][0], F["l"][i][1], F["l"][i0][0], F["l"][i0][1], 0, 0)[0] - sx_) * KG,
                           (_cho_than(b0["name"], cha, F["l"][i][0], F["l"][i][1], F["l"][i0][0], F["l"][i0][1], 0, 0)[1] - sy_) * KG,
                           F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        out[clip] = (float(v["dur"]), res, [F["n"][i_nham] is not None for F in fr])
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)

    def dat_dang(P, goc, tau, lap):
        dur, R, nham = CD[goc]
        n = len(nham)
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
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
        P.alpha["mat_nham"] = 1.0 if nham[i0] else 0.0

    out = []
    for ten_, goc, lap, ev in CLIPS:
        dur = CD[goc][0]
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in sk.slots:
                    if sl["alpha"] > 0 or sl["name"] == "mat_nham":
                        P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], 1.0)
            out.append(Clip(ten_, dur + TAN, fn, ev=ev))
        elif ten_ == "appear":
            def fn(t, P, goc=goc):
                dat_dang(P, goc, t, False)
                a = float(np.clip(t / HIEN, 0.0, 1.0))
                if a < 1.0:
                    for sl in sk.slots:
                        if sl["alpha"] > 0:
                            P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], 1.0)
            out.append(Clip(ten_, dur, fn, ev=ev))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=ev))
    return out


def noi_lai(sk, clips, r=4, vanh=6):
    """DẠNG NON: thân co lại nên các khúc kề nhau chồng sâu hơn dáng của dạng 2; nét viền mà bước xoá vạch nối của dạng 2 để lại
    (đúng cho độ chồng cũ) nay nằm giữa thân. Làm lại việc của rong_vay.py noi_part ngay trên ảnh của rig, theo DÁNG THẬT của dạng
    này (khung 0 idle): nét mực ở vành mép một khúc mà rơi sâu trong khúc KỀ nó → thay bằng màu tô gần nhất. Mép mờ dần của bản vá
    (để hoà chỗ chờm ở dạng 2) làm cứng lại, kẻo chỗ không còn khúc dưới thì nhìn xuyên."""
    import cv2
    from quai.soi import _tris
    P0 = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
    Wd = sk.the_gioi(P0)
    ds = [f"than_{i}" for i in range(1, 8) if f"than_{i}" in sk.atts]
    thu_tu_ve = {sl["name"]: k for k, sl in enumerate(sk.slots)}
    IN_LAI = {("than_1", "than_2")}      # cặp (khúc trên, khúc dưới) cho in lại nét: mới thấy cần ở cổ; cặp khác in ra nét thừa
    CHOM = 999      # cắt vạt chờm sâu hơn chừng này px: ĐÃ THỬ 9 và BỎ (hết che nét khúc dưới nhưng lộ bậc lệch của ranh vành bụng và
    #                 mẩu kem thò ở đỉnh vòng cuộn: vạt chờm chính là thứ che bậc đó). Thay bằng IN LẠI nét của khúc dưới lên vạt.
    e = lambda q: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * q + 1, 2 * q + 1))  # noqa: E731
    sc = RES / TI
    G = {}
    for t in ds:
        hinh = next(iter(sk.atts[t]))
        sp = sk.atts[t][hinh]
        im = sk.images[sp["path"]]
        V = np.array([sum(w * (Wd[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in row) for row in sp["verts"]])
        G[t] = (sp["path"], np.asarray(sp["uv"], float) * np.array([im.width, im.height]), V, np.asarray(sp["tris"], int).reshape(-1, 3))
    Pq = np.concatenate([g[2] for g in G.values()])
    x0, y1 = Pq[:, 0].min() - 12, Pq[:, 1].max() + 12
    cw, ch = int((Pq[:, 0].max() - x0 + 12) * sc), int((y1 - Pq[:, 1].min() + 12) * sc)
    can = lambda v: np.stack([(v[:, 0] - x0) * sc, (y1 - v[:, 1]) * sc], 1)   # noqa: E731
    cung_anh = {}
    for t, (path, uv, V, tris) in G.items():                    # làm cứng mép mờ trước khi đo độ phủ
        if path not in cung_anh:
            a = np.asarray(sk.images[path].convert("RGBA")).copy()
            a[..., 3] = np.where(a[..., 3] > 96, 255, 0).astype(np.uint8)
            cung_anh[path] = a
    # VIỀN KÍN LẠI: da dạng non thừa hưởng "chỗ không có mực" của dạng 2 (đầu khúc đã xoá vạch nối), nhưng thân ngắn chồng khác đi nên
    # có đoạn đã xoá nay nằm ngay trên mép ngoài (viền đứt). Kẻ lại mực dọc toàn bộ mép từng khúc; bước dưới chỉ xoá phần mực rơi
    # sâu trong khúc kề THEO DÁNG NÀY.
    for path, a in cung_anh.items():
        al_ = a[..., 3] > 127
        dai_ = al_ & ~cv2.erode(al_.astype(np.uint8), e(3)).astype(bool)
        a[dai_, :3] = (43, 33, 24)
    phu = {}
    for t, (path, uv, V, tris) in G.items():
        lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
        _tris(lay, Image.fromarray(cung_anh[path], "RGBA").convert("RGBa"), can(V), uv, tris)
        phu[t] = np.asarray(lay)[..., 3] > 127
    muc_can = {}                                                 # mực BÊN TRONG (không phải viền mép) của từng khúc, trên khung chung
    for t, (path, uv, V, tris) in G.items():
        a_ = cung_anh[path]
        al_ = a_[..., 3] > 127
        dm_ = cv2.distanceTransform(al_.astype(np.uint8), cv2.DIST_L2, 5)
        mt = al_ & (a_[..., :3].max(axis=2) < 105) & (dm_ > vanh + 1)
        lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
        _tris(lay, Image.fromarray(np.dstack([mt * 255] * 4).astype(np.uint8), "RGBa"), can(V), uv, tris)
        muc_can[t] = np.asarray(lay)[..., 3] > 110
    for i, t in enumerate(ds):
        path, uv, V, tris = G[t]
        a = cung_anh[path]
        J = np.zeros((ch, cw), bool)
        for nb in (ds[i - 1] if i else None, ds[i + 1] if i + 1 < len(ds) else None):
            if nb:
                J |= cv2.erode(phu[nb].astype(np.uint8), e(r)).astype(bool)
        lay = Image.new("RGBa", (a.shape[1], a.shape[0]), (0, 0, 0, 0))
        _tris(lay, Image.fromarray(np.dstack([J * 255] * 4).astype(np.uint8), "RGBa"), uv, can(V), tris)
        Jt = np.asarray(lay)[..., 3] > 127
        # VẠT CHỜM của khúc nằm TRÊN: chỉ để chờm chừng CHOM px vào khúc kề nằm DƯỚI; phần chờm sâu hơn cắt bỏ (mờ dần 6 px). Vạt
        # chờm sâu che mất một đoạn nét của khúc dưới (người dùng 2026-11-12: "phần gần đầu vẫn bị mất 1 ít nét": vạt kem của khúc
        # cổ che nửa phải một vạch vảy bụng của khúc ngực).
        Js = np.zeros((ch, cw), bool)
        for nb in (ds[i - 1] if i else None, ds[i + 1] if i + 1 < len(ds) else None):
            if CHOM < 100 and nb and thu_tu_ve[nb] < thu_tu_ve[t]:
                Js |= cv2.erode(phu[nb].astype(np.uint8), e(r + CHOM)).astype(bool)
        cat_ = None
        if Js.any():
            lay = Image.new("RGBa", (a.shape[1], a.shape[0]), (0, 0, 0, 0))
            _tris(lay, Image.fromarray(np.dstack([Js * 255] * 4).astype(np.uint8), "RGBa"), uv, can(V), tris)
            cat_ = np.asarray(lay)[..., 3] > 127
        al = a[..., 3] > 127
        rgb = a[..., :3]
        muc = al & (rgb.max(axis=2) < 105)
        dm = cv2.distanceTransform(al.astype(np.uint8), cv2.DIST_L2, 5)
        # CHỈ xoá nét viền ĐẦU KHÚC (chạy dọc mép). Nét chạy NGANG qua mép (ranh vành bụng, vạch vảy bụng, nối với mực ở sâu bên
        # trong) giữ tới cách mép 3 px: bản trước xoá cả vành 10 px nên các nét đó cụt và nhoè ở chỗ nối (người dùng: "vẫn lỗi nhẹ").
        trong = muc & (dm > vanh)
        # nét ngang: điểm mực ở độ sâu dm có mực "bên trong" nằm gần như thẳng phía trong nó (cách ≤ vanh − dm + 2). Điểm của viền
        # đầu khúc nằm lệch ngang khỏi chỗ giao thì xa hơn → không giữ (bản trước giữ cả một mẩu viền dài ~8 px cạnh chỗ giao)
        d_in = cv2.distanceTransform((~trong).astype(np.uint8), cv2.DIST_L2, 5)
        giu = muc & (dm >= 3.0) & (d_in <= vanh - dm + 1.0)
        bo = muc & Jt & (dm <= vanh) & ~giu
        bo |= al & Jt & (dm <= 2.0)                            # hai điểm mép: tô lại theo thịt (hết viền sáng)
        bo = cv2.dilate(bo.astype(np.uint8), e(1)).astype(bool) & al & Jt & ~cv2.dilate(giu.astype(np.uint8), e(1)).astype(bool)   # cả điểm xám khử răng cưa quanh nét vừa xoá
        tot = (dm > 3.0) & ~cv2.dilate(muc.astype(np.uint8), e(2)).astype(bool) & (rgb.min(axis=2) < 222)
        if bo.any() and tot.any():
            _, lb = cv2.distanceTransformWithLabels((~tot).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
            tra[lb[tot]] = rgb[tot]
            rgb[bo] = tra[lb][bo]
        # mép ở chỗ nằm SÂU trong khúc kề mờ dần 6 px (dưới nó chắc chắn có khúc kề cùng màu); nét ngang đã giữ thì không mờ
        mo_ = al & Jt & (dm < 6.0) & ~giu
        a[..., 3][mo_] = np.clip(dm[mo_] / 6.0 * 255.0, 0, 255).astype(np.uint8)
        # IN LẠI nét của khúc DƯỚI lên vạt chờm của khúc này: vạt kem chờm sâu che mất một đoạn vạch vảy của khúc dưới ("phần gần đầu
        # vẫn bị mất 1 ít nét"). Chỉ in nét mà khúc này không có nét nào của mình ở gần (cách > 8 px), kẻo ranh vành bụng thành nét đôi.
        in_ = 0
        for nb in (ds[i - 1] if i else None, ds[i + 1] if i + 1 < len(ds) else None):
            if nb and thu_tu_ve[nb] < thu_tu_ve[t]:
                # chỉ nét của khúc dưới đang HIỆN DỞ DANG: lần theo nét từ phần còn lộ (ngoài khúc này) vào dưới vạt tối đa 40 px.
                # Nét nằm trọn dưới vạt là nét khúc này cố ý che (in ra thành nét thừa: đã thử). Chỉ in trên nền KEM (vạch vảy).
                lo = muc_can[nb] & ~phu[t]
                k3 = np.ones((3, 3), np.uint8)
                for _ in range(40):
                    lo = cv2.dilate(lo.astype(np.uint8), k3).astype(bool) & muc_can[nb]
                lay = Image.new("RGBa", (a.shape[1], a.shape[0]), (0, 0, 0, 0))
                _tris(lay, Image.fromarray(np.dstack([(lo & phu[t]) * 255] * 4).astype(np.uint8), "RGBa"), uv, can(V), tris)
                mn = np.asarray(lay)[..., 3] > 110
                cua_minh = (a[..., 3] > 127) & (rgb.max(axis=2) < 105)
                kem = (rgb[..., 0] > 215) & (rgb[..., 1] > 195) & (rgb[..., 2] > 150) & (rgb[..., 2] < 235)
                kem = cv2.dilate(kem.astype(np.uint8), e(2)).astype(bool)
                P_ = mn & al & Jt & kem & ~cv2.dilate(cua_minh.astype(np.uint8), e(8)).astype(bool)
                # chỉ giữ mẩu NỐI một nét đang lộ với nét sẵn có của khúc này (đầu kia chạm tới gần mực của mình, vd viền mép phải):
                # mẩu kết thúc lơ lửng giữa nền kem là nét khúc này cố ý không có → bỏ (đã thấy thành nét thừa ở đỉnh vòng cuộn)
                gan_minh = cv2.dilate(cua_minh.astype(np.uint8), e(11)).astype(bool)
                nc_, lb_, st_, _ = cv2.connectedComponentsWithStats(cv2.dilate(P_.astype(np.uint8), e(2)), connectivity=8)
                for k_ in range(1, nc_):
                    cc = lb_ == k_
                    if st_[k_, cv2.CC_STAT_AREA] < 60 or not (cc & gan_minh).any() or (t, nb) not in IN_LAI:
                        P_ &= ~cc
                rgb[P_] = (43, 33, 24)
                a[..., 3][cv2.dilate(P_.astype(np.uint8), e(1)).astype(bool) & al] = 255
                in_ += int(P_.sum())
        if cat_ is not None and cat_.any():
            dc = cv2.distanceTransform((~cat_).astype(np.uint8), cv2.DIST_L2, 5)      # 0 trong vùng cắt, tăng dần ra ngoài
            a[..., 3] = (a[..., 3].astype(np.float32) * np.clip(dc / 6.0, 0.0, 1.0)).astype(np.uint8)
        print(f"  nối lại {t}: xoá {int(bo.sum())} px viền đầu khúc, giữ {int((giu & Jt).sum())} px nét ngang, mờ mép {int(mo_.sum())} px"
              + (f", cắt vạt chờm {int(cat_.sum())} px" if cat_ is not None else "") + (f", in lại {in_} px nét khúc dưới" if in_ else ""))
    for path, a in cung_anh.items():
        sk.images[path] = anh.loang_mau(Image.fromarray(a, "RGBA"))


NHE = 0.44                   # độ nét ảnh của bản dạng 2 gộp vào file dạng 1 (dạng 2 thật là 0,8): chỉ hiện ~1,3 giây cuối clip evolve


def tien_hoa(skA, clipsA):
    """clip `evolve` của dạng non (người dùng 2026-11-12: "làm nốt những cái bạn chưa làm"): gộp bản NHẸ của dạng 2 vào rig dạng 1
    (quai/tienhoa.py: xương dạng 2 mang tiền tố n_, slot ẩn mặc định). Dạng non ở dáng nghỉ ngửa người gồng, rung, há mỏ; đổi dạng
    lúc ~1,2 s; dạng 2 hiện ra vươn người há mỏ gầm rồi hoà về đúng khung 0 idle của dạng 2."""
    from quai import tienhoa
    idleA = [c for c in clipsA if c.ten == "idle"][0]
    frA0 = hoat.nuong(skA, idleA)[0]
    hA = soi.chieu_cao(soi.Ve(skA), frA0)
    cau_hinh("", res=NHE)
    skB, infoB = dung()
    clipsB = lam_clip(skB, infoB)
    frB0 = hoat.nuong(skB, [c for c in clipsB if c.ten == "idle"][0])[0]
    hB = soi.chieu_cao(soi.Ve(skB), frB0)
    cau_hinh("non")
    M = tienhoa.gop(skA, skB)

    def gong(t, P):                             # dạng non: từ dáng nghỉ ngửa lưng, thu người, rung, há mỏ dần
        idleA.fn(0.0, P)
        g = hoat.cv(t, [(0, 0), (0.3, -0.3), (0.6, 1, "out"), (1.3, 1.15)])
        r = hoat.rung(t, 0.45, 1.35, moi=1)
        gp = max(g, 0.0)
        P.rot("zhixin", 8.0 * g + 0.8 * r)
        P.move("zhixin", -10.0 * g, -8.0 * gp)
        P.rot("tou", -12.0 * gp + 1.2 * r)
        P.rot("bone11", -20.0 * gp)
        P.rot("bone10", 3.0 * gp)

    def gam(t, P, fl):                          # dạng 2: vươn người, há mỏ gầm, đầu rung
        r = hoat.rung(t, 2.0, 2.4, moi=1)
        P.rot("n_zhixin", 7.0 * fl)
        P.rot("n_tou", -9.0 * fl + 1.5 * r * fl)
        P.rot("n_bone11", -26.0 * fl)
        P.rot("n_bone10", 4.0 * fl)

    ev = tienhoa.clip_tien_hoa(M, skA, skB, frB0, tiB=hA / hB, fnA=gong, fnB=gam, mem=[])
    print(f"  evolve: gộp dạng 2 bản nhẹ (ảnh {NHE}); cao dạng non {hA:.0f}, dạng 2 {hB:.0f} → dạng 2 co {hA / hB:.3f} trong rig gộp")
    return M, clipsA + [ev]


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if DANG == "non":
        noi_lai(sk, clips)
        if not a:
            sk, clips = tien_hoa(sk, clips)
    if a and a[0] == "bo_cuc":                 # hình bố cục 1536x1024 nền trắng (khung 0 idle) cho prompt concept của dạng → a[1]
        fr = hoat.nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.03)
        sc = min(1536 * 0.84 / (Bx[2] - Bx[0]), 1024 * 0.86 / (Bx[3] - Bx[1]))
        im = ve.ve(fr[0], Bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
        out = Image.new("RGB", (1536, 1024), (255, 255, 255))
        out.paste(im, ((1536 - im.width) // 2, (1024 - im.height) // 2))
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        out.save(a[1])
        print(a[1], im.size)
        return
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ] [luoi]: khung lớn nền xám → rig/soi_<clip>.png
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        kw = dict(luoi=True, mau_luoi=(10, 10, 10, 90)) if len(a) > 4 else {}
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2, **kw).convert("RGB") for P in Ps]
        cot = min(len(ims), 4)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        pth = os.path.join(RA, f"soi_{a[1]}{'_' + DANG if DANG else ''}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN, "Rồng vây non (dạng 1)" if DANG == "non" else "Rồng vây (dạng 2)", dang=1 if DANG == "non" else 2,
                  so_dang=2, dung_yen=("cast", "skill"), ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, dich_mb=0.9, tran_mb=1.1)


if __name__ == "__main__":
    main(sys.argv[1:])
