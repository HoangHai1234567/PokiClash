# -*- coding: utf-8 -*-
"""Hổ lửa DẠNG 1 bản CHIBI (hổ con vẽ riêng; người dùng 2026-11-14 tối: "Hổ con xấu quá, gen lại chibi hơn" → chọn concept A,
inbox/hoa_ho_non/tai_ve/L1_duyet.png). Cùng xương, cùng clip với dạng 2 (hoa_ho_rig.py, HH_DANG=chibi); xương đầu phóng 2, chân 0,68,
đuôi 0,6 (hình bố cục dựng concept dùng đúng các số này: inbox/hoa_ho_non/mau/bo_cuc_chibi.json).

MẢNH: gen "đúng chỗ, đúng cỡ" từ concept (hoa_ho_non.py manh_prompt → tai_ve/C_THAN, C_CHAN, C_DUOI, C_DAU), cắt theo cụm liền:
    c_duoi   đuôi + ngọn lửa        uốn theo lưới đuôi của họ (P_weiba_*)
    c_chan2  chân thứ hai từ trái   (sau thân)   uốn theo chân TRƯỚC GẦN của họ
    c_than   thân                   uốn theo lưới thân của họ (P_tun, P_shenti_01)
    c_bom    bờm lửa sau gáy        uốn theo các cụm mây cổ của họ (P_maofa_07/11/12/17)
    c_chan1  chân trái cùng         uốn theo chân SAU GẦN
    c_chan3  chân thứ ba            uốn theo chân SAU XA
    c_chan4  chân phải cùng         uốn theo chân TRƯỚC XA (cái chân vả)
    c_dau    đầu (cả tai, chỏm lửa, mắt); vùng hàm dưới tô màu lòng miệng       cứng trên xương đầu bone5
    c_ham    hàm dưới + lông cằm (cắt từ ảnh đầu theo đường môi)                 cứng trên xương hàm bone57
    P_biyan  mắt nhắm (vẽ bằng mã, che mắt mở)                                   cứng trên bone5
Chỗ đứng: ảnh concept ↔ thế giới rig theo phép đặt của hình bố cục, ở DÁNG KHUNG 0 IDLE (concept vẽ theo dáng đó). Mỗi đỉnh lưới của mình
lấy trọng số xương của điểm tương ứng trên lưới của họ (cùng chỗ; chân, đuôi: dời cho đáy / tâm khung bao trùng nhau trước khi tra; bờm:
khung bao ↔ khung bao), rồi gắn cứng vào từng xương đúng chỗ nó đang đứng ở dáng đó (dáng nghỉ = concept).

    hoa_ho_chibi.py cat     cắt bốn tờ → inbox/hoa_ho_non/manh_chibi/*.png + dat.json + _ghep.png (ghép lại so concept)
  Rig: HH_DANG=chibi py -3 -I hoa_ho_rig.py → inbox/hoa_ho_non/rig_chibi/
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import glob
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import khung  # noqa: E402
BASE = os.path.join(HERE, "inbox", "hoa_ho_non")
TAI = os.path.join(BASE, "tai_ve")
MANH = os.path.join(BASE, "manh_chibi")
W, H = 1536, 1024
INK = (43, 33, 24)
KEM = (242, 236, 222)
MIENG = (104, 32, 30)
TI_LE = {"HH_KDAU": "2.0", "HH_CHAN": "0.68", "HH_DUOI": "0.6"}

# đường môi → đa giác HÀM DƯỚI trên concept (px): khoé miệng, dọc đường môi tới trước mõm, rồi vòng xuống quanh cằm
HAM = [(1042, 516), (1075, 533), (1112, 546), (1150, 550), (1185, 532), (1212, 500), (1228, 486), (1262, 486), (1262, 720), (985, 720), (1005, 640)]
NANH = [(1141, 528), (1180, 528), (1175, 562), (1159, 571), (1145, 558)]      # mũi nanh trên: ở lại với đầu
MAT = (1042, 410, 80, 76)                                                        # mắt: tâm x, y, bán trục ngang, dọc
MAY = ((972, 338), (1120, 390))                                                  # nét mí / mày đè trên mắt

# mảnh: (tờ, thứ tự vẽ, lưới nguồn của họ, kiểu tra điểm tương ứng)
NGUON = {
    "c_duoi": ("P_weiba_01", "P_weiba_02"),
    "c_chan2": ("P_R_datui", "P_R_xiaotui", "P_R_jiao", "P_R_jiaozhi_01", "P_R_jiaozhi_02", "P_R_jiaozhi_03", "P_R_jiaozhi_04"),
    "c_than": ("P_tun", "P_shenti_01"),
    "c_co": ("P_tun", "P_shenti_01"),
    "c_bom": ("P_maofa_07", "P_maofa_11", "P_maofa_12", "P_maofa_17"),
    "c_chan1": ("P_R_houdatui", "P_R_houxiaotui_02", "P_R_houxiaotui", "P_R_houjiaozhang"),
    "c_chan3": ("P_L_houdatui", "P_L_houxiaotui_02", "P_L_houxiaotui", "P_L_houjiao_01"),
    "c_chan4": ("P_L_datui", "P_L_xiaotui", "P_L_jiao"),
}
KIEU = {"c_duoi": "khung", "c_chan1": "day", "c_chan2": "day", "c_chan3": "day", "c_chan4": "day", "c_than": "dong", "c_co": "dong", "c_bom": "khung"}
# 2026-11-14 tối, người dùng xem bản đầu: "đầu bị hở" (gầm: đầu ngửa lên rời khỏi thân) → thêm mảnh CỔ c_co; "animation đánh thường layer bị
# lỗi, chân phải ở dưới body" → chân vả c_chan4 vẽ DƯỚI thân, bỏ bản sinh đôi vẽ trên đầu.
THU_TU = ["c_duoi", "c_chan2", "c_chan4", "c_than", "c_bom", "c_co", "c_chan1", "c_chan3", "c_dau", "c_ham", "P_biyan"]
# slot sinh đôi: cùng ảnh, cùng lưới với slot gốc nhưng vẽ TRÊN đầu, bình thường ẩn. Đòn vả giơ chân trước lên ngang mặt: đầu to che mất,
# nên trong quãng giơ – vả clip attack bật bản trên, tắt bản dưới (hoa_ho_rig.f_attack)
SINH_DOI = {}
# cổ: một miếng lông kem hình viên thuốc (tâm đáy, tâm đỉnh, bán kính; px concept), đáy nằm trong thân, đỉnh nằm trong đầu, vẽ sau đầu. Đáy
# bám như thân ở chỗ đó, đỉnh bám xương đầu: đầu ngửa lên thì miếng này dãn ra lấp chỗ hở
CO = ((895, 705), (990, 520), 96)
# đuôi: bám một chuỗi xương ngắn ở GỐC đuôi của họ theo độ cao (gốc → ngọn lửa). Tra theo lưới đuôi của họ thì ngọn đuôi ngắn của mình ăn
# theo các đốt chót (quật rất mạnh): ngọn lửa bị kéo dãn thành vệt
CHUOI = {"c_duoi": ["bone8", "bone9", "bone10", "bone11"]}
# chân: bám chuỗi xương đùi → ống → bàn của đúng cái chân đó theo ĐỘ CAO KHỚP ở dáng khung 0 idle (đỉnh trên khớp gối bám đùi, dưới cổ chân
# bám bàn, pha mềm quanh khớp). Tra theo lưới chân của họ (nhiều mảnh rời, lệch chỗ so với chân mập của mình) thì clip chạy vặn méo chân.
KHOP = {"c_chan1": ["bone18", "bone19", "bone20", "bone21"], "c_chan3": ["bone33", "bone34", "bone35", "bone36"],
        "c_chan2": ["bone26", "bone27", "bone28"], "c_chan4": ["bone43", "bone44", "bone45"]}    # bàn chân vả: bone45 (bone68 là đốt ngón, gập mạnh lúc vả làm bàn chân rách)
CUNG = {"c_dau": "bone5", "c_ham": "bone57", "P_biyan": "bone5"}
# làm mượt trọng số trên lưới của mình (số vòng): lưới nguồn là nhiều mảnh rời (đùi, ống, bàn, ngón) nên hai đỉnh kề nhau có thể tra ra hai
# mảnh khác xương hẳn → rách hình khi chuyển động. Bờm: pha thêm xương cổ (PHA) cho bớt trôi theo các cụm mây rời của họ.
MUOT = {"c_duoi": 10, "c_chan1": 10, "c_chan2": 10, "c_chan3": 10, "c_chan4": 10, "c_than": 5, "c_bom": 24}
PHA = {"c_bom": ("bone4", 0.55)}
# chân: chiều gập gối (+1: gối đẩy về phía trước mặt, chân sau; −1: khuỷu đẩy về phía đuôi, chân trước) và pha bước của clip walk (hai cặp
# chân chéo: trái cùng + phải cùng, hai chân giữa)
GOI = {"c_chan1": 1, "c_chan2": 1, "c_chan3": -1, "c_chan4": -1}
PHA_BUOC = {"c_chan1": 0.0, "c_chan4": 0.0, "c_chan2": 0.5, "c_chan3": 0.5}
PHA_CAO = {"c_co": "bone5"}                           # pha dần theo độ cao sang xương này (đáy 0 → đỉnh 1)


# ---------------------------------------------------------------- cắt tờ
def _moi(tien_to):
    ds = sorted(glob.glob(os.path.join(TAI, tien_to + "*.png")), key=os.path.getmtime)
    if not ds:
        raise SystemExit("chưa có " + tien_to)
    return ds[-1]


def _tach(p):
    """ảnh tờ → (rgb, mặt nạ hình): nền = trắng nối với mép ảnh."""
    g = Image.open(p).convert("RGB")
    if g.size != (W, H):
        g = g.resize((W, H), Image.LANCZOS)
    A = np.asarray(g)
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab = cv2.connectedComponents(trang, connectivity=4)
    mep = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    nen = np.isin(lab, [k for k in mep if k != 0])
    return A, ~nen


def _cum(m, n, min_dt=2500):
    """n cụm liền lớn nhất của mặt nạ, xếp trái → phải."""
    k, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    ds = sorted([i for i in range(1, k) if st[i, cv2.CC_STAT_AREA] >= min_dt], key=lambda i: -st[i, cv2.CC_STAT_AREA])[:n]
    ds.sort(key=lambda i: st[i, cv2.CC_STAT_LEFT])
    if len(ds) < n:                                   # các hình chạm nhau ở một chỗ mảnh: co mặt nạ cho tách ra, rồi chia điểm theo cụm gần nhất
        for r in range(3, 30, 2):
            e = cv2.erode(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
            k2, lab2, st2, _ = cv2.connectedComponentsWithStats(e, connectivity=8)
            d2 = sorted([i for i in range(1, k2) if st2[i, cv2.CC_STAT_AREA] >= min_dt // 4], key=lambda i: -st2[i, cv2.CC_STAT_AREA])[:n]
            if len(d2) >= n:
                d2.sort(key=lambda i: st2[i, cv2.CC_STAT_LEFT])
                kc = np.stack([cv2.distanceTransform((lab2 != i).astype(np.uint8), cv2.DIST_L2, 5) for i in d2])
                gan = kc.argmin(0)
                print(f"  (tách {n} hình chạm nhau: co {r} px)")
                return [m & (gan == j) for j in range(n)]
    return [lab == i for i in ds]


def _luu(A, m, ten, dat, pad=3):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W, xs.max() + 1 + pad), min(H, ys.max() + 1 + pad)
    al = cv2.GaussianBlur(m[y0:y1, x0:x1].astype(np.float32) * 255, (0, 0), 0.7)
    out = np.dstack([A[y0:y1, x0:x1], np.clip(al * 1.6 - 60, 0, 255).astype(np.uint8)])
    Image.fromarray(out, "RGBA").save(os.path.join(MANH, ten + ".png"))
    dat[ten] = [int(x0), int(y0)]
    print(f"  {ten}: {x1 - x0} x {y1 - y0} tại ({x0}, {y0})")


def cat():
    os.makedirs(MANH, exist_ok=True)
    dat = {}
    A, m = _tach(_moi("C_THAN"))
    than = _cum(m, 1)[0]
    _luu(A, than, "c_than", dat)
    A, m = _tach(_moi("C_CHAN"))
    cs = _cum(m, 4)
    if len(cs) != 4:
        raise SystemExit(f"tờ CHAN có {len(cs)} cụm, cần 4 chân rời nhau")
    # ba chân vẽ TRƯỚC thân (1, 3, 4): xoá nét viền ở phần đỉnh chân nằm trong thân (không thì đỉnh bo tròn in một cung mực lên thân như
    # khớp đồ chơi); chỗ đó lấy màu lông của chính chân
    A = A.copy()
    el = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    than_trong = cv2.erode(than.astype(np.uint8), el(10)) > 0
    for i in (0, 2):
        c = cs[i]
        ys, xs = np.nonzero(c)
        dai = c & ~(cv2.erode(c.astype(np.uint8), el(13)) > 0)
        R = dai & than_trong & (np.arange(H)[:, None] < ys.min() + 0.3 * (ys.max() - ys.min()))   # chỉ phần đỉnh (bám cứng theo thân): phần dưới dãn ra ngoài thân lúc chạy, phải còn viền
        sang = c & (A.min(2) > 190)
        A[R] = np.median(A[sang], axis=0).astype(np.uint8)
    for i, c in enumerate(cs):
        _luu(A, c, f"c_chan{i + 1}", dat)
    # cổ (vẽ bằng mã): viên thuốc màu lông của thân, viền mực hai bên
    (ax, ay), (bx, by), r = CO
    S = 2
    co = np.zeros((H * S, W * S), np.uint8)
    cv2.line(co, (ax * S, ay * S), (bx * S, by * S), 255, 2 * r * S, cv2.LINE_AA)
    trong = np.zeros((H * S, W * S), np.uint8)
    cv2.line(trong, (ax * S, ay * S), (bx * S, by * S), 255, 2 * (r - 7) * S, cv2.LINE_AA)
    co = cv2.resize(co, (W, H), interpolation=cv2.INTER_AREA) > 127
    trong = cv2.resize(trong, (W, H), interpolation=cv2.INTER_AREA) > 127
    At, mt = _tach(_moi("C_THAN"))
    long_ = np.median(At[mt & (At.min(2) > 190)], axis=0).astype(np.uint8)
    Ac = np.zeros((H, W, 3), np.uint8)
    Ac[:] = INK
    Ac[trong] = long_
    _luu(Ac, co, "c_co", dat)
    A, m = _tach(_moi("C_DUOI"))
    cs = _cum(m, 2)
    if len(cs) != 2:
        raise SystemExit(f"tờ DUOI có {len(cs)} cụm, cần 2 (đuôi, bờm)")
    _luu(A, cs[0], "c_duoi", dat)
    _luu(A, cs[1], "c_bom", dat)
    # đầu: tách hàm dưới theo đường môi; chỗ hàm trên ảnh đầu tô màu lòng miệng (hàm đậy lên lúc ngậm)
    A, m = _tach(_moi("C_DAU"))
    dau = _cum(m, 1)[0]
    ham_m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(ham_m, [np.array(HAM, np.int32)], 255)
    nanh = np.zeros((H, W), np.uint8)
    cv2.fillPoly(nanh, [np.array(NANH, np.int32)], 255)
    ham = dau & (ham_m > 0) & (nanh == 0)
    A_dau = A.copy()
    trong = cv2.erode(ham_m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))) > 0     # chừa nét môi + viền của ảnh đầu
    to = dau & trong & (nanh == 0)
    A_dau[to] = MIENG
    _luu(A_dau, dau, "c_dau", dat)
    _luu(A, ham, "c_ham", dat)
    # mắt nhắm: miếng kem che mắt mở, một cung mí cong xuống, kẻ lại nét mày
    S = 3
    cx, cy, rx, ry = MAT
    x0, y0, x1, y1 = cx - rx - 14, cy - ry - 14, cx + rx + 14, cy + ry + 14
    b = np.zeros(((y1 - y0) * S, (x1 - x0) * S, 4), np.uint8)
    c0 = ((cx - x0) * S, (cy - y0) * S)
    long_dau = tuple(int(x) for x in np.median(A[dau & (A.min(2) > 190)], axis=0))      # màu lông của chính ảnh đầu (KEM lệch tông, lộ thành miếng vá)
    cv2.ellipse(b, c0, ((rx + 5) * S, (ry + 5) * S), 0, 0, 360, long_dau + (255,), -1, cv2.LINE_AA)
    cv2.ellipse(b, (c0[0], c0[1] - int(ry * 0.25 * S)), (int(rx * 0.8 * S), int(ry * 0.55 * S)), 0, 15, 165, INK + (255,), 9 * S, cv2.LINE_AA)
    (ax, ay), (bx, by) = MAY
    cv2.line(b, ((ax - x0) * S, (ay - y0) * S), ((bx - x0) * S, (by - y0) * S), INK + (255,), 11 * S, cv2.LINE_AA)
    Image.fromarray(b, "RGBA").resize((x1 - x0, y1 - y0), Image.LANCZOS).save(os.path.join(MANH, "P_biyan.png"))
    dat["P_biyan"] = [int(x0), int(y0)]
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w"), indent=1)
    # ghép lại so concept
    out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for ten in THU_TU:
        if ten == "P_biyan":
            continue
        out.alpha_composite(Image.open(os.path.join(MANH, ten + ".png")), tuple(dat[ten]))
    con = Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB")
    canh = Image.new("RGB", (W * 2, H), (255, 255, 255))
    canh.paste(con, (0, 0))
    canh.paste(out.convert("RGB"), (W, 0))
    canh.save(os.path.join(MANH, "_ghep.png"))
    d = np.abs(np.asarray(con).astype(int) - np.asarray(out.convert("RGB")).astype(int)).max(2)
    print(f"  ghép so concept: {100 * (d > 60).mean():.1f} % điểm lệch màu rõ → {os.path.join(MANH, '_ghep.png')}")


# ---------------------------------------------------------------- lắp vào rig (gọi từ hoa_ho_rig.dung ở chế độ chibi)
def lap(sk, by, ten, Wc, P0, d_px, luoi, anh):
    """tạo slot + lưới của mọi mảnh. by: att của họ theo slot; Wc: ma trận thế giới dáng gốc của họ; P0: khung 0 idle của rig mình."""
    cfg = json.load(open(os.path.join(BASE, "mau", "bo_cuc_chibi.json")))
    sc, box = cfg["sc"], cfg["box"]
    dat = json.load(open(os.path.join(MANH, "dat.json")))
    WP = sk.the_gioi(P0)
    inv = {}

    def nghich(b):
        if b not in inv:
            inv[b] = np.linalg.inv(WP[b])
        return inv[b]

    def nguon(slots):
        """đỉnh (ở khung 0 idle của rig mình), tam giác, trọng số của hợp các lưới nguồn."""
        Vs, Ts, Ws, off = [], [], [], 0
        for s in slots:
            a = by[s]
            xy = np.array(a["xy"], float).reshape(-1, 2)
            ws = a.get("w") or [[[a["bone"] if isinstance(a["bone"], int) else ten.index(a["bone"]), 1.0]]] * len(xy)
            P = np.zeros_like(xy)
            for i, (p, w) in enumerate(zip(xy, ws)):
                for k, v in w:
                    b = ten[k]
                    P[i] += v * (WP[b] @ np.linalg.inv(Wc[b]) @ np.array([p[0], p[1], 1.0]))[:2]
            Vs.append(P)
            Ts.append(np.array(a["tris"]).reshape(-1, 3) + off)
            Ws += [{ten[k]: float(v) for k, v in w if v > 0.002} for w in ws]
            off += len(xy)
        return np.vstack(Vs), np.vstack(Ts), Ws

    def tra(Q, V, T, Wg):
        """trọng số xương cho từng điểm Q: tam giác nguồn chứa nó, không có thì tam giác gần nhất (toạ độ trọng tâm kẹp về trong)."""
        A, B, C = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
        v0, v1 = B - A, C - A
        den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
        den = np.where(np.abs(den) < 1e-9, 1e-9, den)
        tam = (A + B + C) / 3
        out = []
        for q in Q:
            v2 = q - A
            b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
            b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
            b0 = 1 - b1 - b2
            ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
            if len(ok):
                i = int(ok[0])
                be = np.array([b0[i], b1[i], b2[i]])
            else:
                i = int(np.argmin(((tam - q) ** 2).sum(1)))
                be = np.clip(np.array([b0[i], b1[i], b2[i]]), 0, None)
                be = be / be.sum() if be.sum() > 1e-9 else np.array([1 / 3, 1 / 3, 1 / 3])
            d = {}
            for k, bk in zip(T[i], be):
                for b, w in Wg[k].items():
                    d[b] = d.get(b, 0.0) + float(bk) * w
            top = sorted(d.items(), key=lambda x: -x[1])[:4]
            top = [(b, w) for b, w in top if w > 0.03] or top[:1]
            tot = sum(w for _, w in top)
            out.append({b: w / tot for b, w in top})
        return out

    def muot(ts, tris, lan, pha=None):
        ds = sorted({b for d in ts for b in d})
        ix = {b: i for i, b in enumerate(ds)}
        M = np.zeros((len(ts), len(ds)))
        for i, d in enumerate(ts):
            for b, w in d.items():
                M[i, ix[b]] = w
        ke = [set() for _ in ts]
        for a, b, c in np.asarray(tris):
            ke[a] |= {b, c}
            ke[b] |= {a, c}
            ke[c] |= {a, b}
        ke = [np.array(sorted(k), int) for k in ke]
        for _ in range(lan):
            M = np.stack([0.5 * M[i] + 0.5 * M[k].mean(0) if len(k) else M[i] for i, k in enumerate(ke)])
        out = []
        for r in M:
            top = np.argsort(-r)[:4]
            top = [j for j in top if r[j] > 0.04] or [int(np.argmax(r))]
            tot = float(r[top].sum())
            d = {ds[j]: float(r[j]) / tot for j in top}
            if pha:
                d = {b: w * (1 - pha[1]) for b, w in d.items()}
                d[pha[0]] = d.get(pha[0], 0.0) + pha[1]
            out.append(d)
        return out

    tong = [0, 0]
    kq = d_px / sc                                     # px atlas cho mỗi px concept
    nho = {}
    chan_ds = []
    sk.chan_chibi = chan_ds
    for slot in THU_TU:
        if slot in SINH_DOI:
            goc = SINH_DOI[slot]
            L, ts, V, hang = nho[goc]
            sk.slot(slot, "move", goc, an=True)
            sk.luoi_gan(slot, goc, L, ts, the_gioi=V)
            sk.atts[slot][goc]["verts"] = hang
            continue
        g = Image.open(os.path.join(MANH, slot + ".png")).convert("RGBA")
        gk = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
        sk.slot(slot, "move", slot, an=(slot == "P_biyan"))
        sk.anh(slot, anh.loang_mau(gk))
        im = sk.images[slot]
        cung = slot in CUNG                             # mảnh cứng: lưới thưa
        L = luoi.luoi_vung(im, buoc_vien=30.0 if cung else 9.0, buoc_trong=44.0 if cung else 13.0, ten=slot, in_tk=False)
        # đỉnh lưới: px atlas → px concept → thế giới rig
        cx = dat[slot][0] + L.pts[:, 0] * g.width / im.width
        cy = dat[slot][1] + L.pts[:, 1] * g.height / im.height
        V = np.stack([box[0] + cx / sc, box[3] - cy / sc], 1)
        if slot in CUNG:
            ts = [{CUNG[slot]: 1.0}] * L.n
        elif slot in KHOP:
            # XƯƠNG CHÂN RIÊNG (người dùng 2026-11-14: "cả chân trái trước và sau khi walk đều lỗi, rig lại xương"): mỗi chân ba xương của
            # mình: <slot>_a đùi (khớp háng H nằm trong thân, con của xương thân trội ở chỗ đó), <slot>_b ống (khớp gối K), <slot>_c bàn
            # (cổ chân A). Đỉnh chân vẫn bám như thân (nấp trong thân). Bàn chân đi theo đâu là việc của ik() bên dưới: clip của họ → cổ
            # chân bám chỗ xương bàn của họ; clip walk → bước chân tự viết. Độ dài xương cố định nên chân không còn bị kéo dãn.
            ban = KHOP[slot][-1]
            Vt, Tt, Wt = nguon(NGUON["c_than"])
            than_w = muot(tra(V, Vt, Tt, Wt), L.tris, 6)
            y0, cao = float(V[:, 1].min()), float(V[:, 1].max() - V[:, 1].min())
            u = (V[:, 1] - y0) / max(1e-6, cao)                           # 0 = đáy bàn chân, 1 = đỉnh
            tx = lambda a, b: float(V[(u >= a) & (u <= b), 0].mean())      # noqa: E731
            Hh = np.array([tx(0.70, 0.90), y0 + 0.80 * cao])
            Aa = np.array([tx(0.05, 0.30), y0 + 0.16 * cao])
            dd = Aa - Hh
            dai = float(np.hypot(*dd))
            nn = np.array([-dd[1], dd[0]]) / dai                           # vuông góc (quay +90°): chân chĩa xuống thì nn = +x (phía trước)
            dau = GOI[slot]
            Kk = (Hh + Aa) / 2 + nn * dau * 0.17 * dai
            L1, L2 = float(np.hypot(*(Kk - Hh))), float(np.hypot(*(Aa - Kk)))
            ga = math.degrees(math.atan2(Kk[1] - Hh[1], Kk[0] - Hh[0]))
            gb = math.degrees(math.atan2(Aa[1] - Kk[1], Aa[0] - Kk[0]))
            i_h = int(np.argmin(((V - Hh) ** 2).sum(1)))
            cha_x = max(than_w[i_h], key=than_w[i_h].get)
            gp = khung.goc_mat(WP[cha_x])
            lp = np.linalg.solve(WP[cha_x], np.array([Hh[0], Hh[1], 1.0]))
            nr, na, nb, nc = slot + "_r", slot + "_a", slot + "_b", slot + "_c"
            gr = math.degrees(math.atan2(dd[1], dd[0]))                    # trục chân: háng → cổ chân
            sk.xuong(nr, cha_x, float(lp[0]), float(lp[1]), goc=gr - gp, dai=dai)
            sk.xuong(na, nr, 0.0, 0.0, goc=ga - gr, dai=L1)
            sk.xuong(nb, na, L1, 0.0, goc=gb - ga, dai=L2)
            # xương BÀN chân là con của xương THÂN (không phải của ống chân): chân bị ép ngắn bằng tỉ lệ thì bàn chân không bẹp theo; ik()
            # dời nó tới đúng đầu ống chân từng khung
            lpa = np.linalg.solve(WP[cha_x], np.array([Aa[0], Aa[1], 1.0]))
            sk.xuong(nc, cha_x, float(lpa[0]), float(lpa[1]), goc=gb - gp, dai=0.3 * L2)
            WP[nr] = khung.mat(Hh[0], Hh[1], gr)
            WP[na], WP[nb], WP[nc] = khung.mat(Hh[0], Hh[1], ga), khung.mat(Kk[0], Kk[1], gb), khung.mat(Aa[0], Aa[1], gb)
            uK = float((Kk[1] - y0) / cao)
            sm = lambda x: float(np.clip(x, 0, 1)) ** 2 * (3 - 2 * float(np.clip(x, 0, 1)))  # noqa: E731
            ts = []
            for d, uu in zip(than_w, u):
                wt = sm((uu - 0.74) / 0.14)                                # đỉnh: theo thân
                s1 = sm((uu - (uK - 0.07)) / 0.14)                         # trên gối: đùi
                s2 = sm((uu - 0.21) / 0.10)                                # trên cổ chân: ống
                e = {b: w * wt for b, w in d.items() if w * wt > 0.02}
                for b, w in ((na, (1 - wt) * s1), (nb, (1 - wt) * (1 - s1) * s2), (nc, (1 - wt) * (1 - s1) * (1 - s2))):
                    if w > 0.02:
                        e[b] = w
                tot = sum(e.values())
                ts.append({b: w / tot for b, w in e.items()})
            mc = np.linalg.solve(WP[ban], np.array([Aa[0], Aa[1], 1.0]))
            chan_ds.append(dict(slot=slot, cha=cha_x, hip=(float(lp[0]), float(lp[1])), ban_dp=(float(lpa[0]), float(lpa[1])), r=nr, gr0=gr, D0=dai, a=na, b=nb, c=nc, L1=L1, L2=L2, dau=dau, ga0=ga, gb0=gb,
                                cha_goc0=gp, ban=ban, mat_ca=(float(mc[0]), float(mc[1])), ban_goc0=khung.goc_mat(WP[ban]),
                                A0=(float(Aa[0]), float(Aa[1])), H0=(float(Hh[0]), float(Hh[1])), pha=PHA_BUOC[slot]))
        elif slot in CHUOI:
            ch = CHUOI[slot]
            s = (V[:, 1] - V[:, 1].min()) / max(1e-6, V[:, 1].max() - V[:, 1].min()) * (len(ch) - 1)
            ts = []
            for x in s:
                i = min(int(x), len(ch) - 2)
                w = float(x - i)
                ts.append({ch[i]: 1 - w, ch[i + 1]: w} if 0.02 < w < 0.98 else {ch[i + (w >= 0.5)]: 1.0})
        else:
            Vn, Tn, Wn = nguon(NGUON[slot])
            k = KIEU[slot]
            a0, a1, b0, b1 = V.min(0), V.max(0), Vn.min(0), Vn.max(0)
            if k == "dong":
                Q = V
            elif k == "day":                           # đáy khung bao (bàn chân) trùng nhau
                Q = V - np.array([(a0[0] + a1[0]) / 2, a0[1]]) + np.array([(b0[0] + b1[0]) / 2, b0[1]])
            elif k == "tam":
                Q = V - (a0 + a1) / 2 + (b0 + b1) / 2
            else:                                      # khung bao ↔ khung bao
                Q = b0 + (V - a0) / np.maximum(a1 - a0, 1e-6) * (b1 - b0)
            ts = muot(tra(Q, Vn, Tn, Wn), L.tris, MUOT.get(slot, 6), PHA.get(slot))
            if slot in PHA_CAO:
                bx = PHA_CAO[slot]
                u = (V[:, 1] - V[:, 1].min()) / max(1e-6, V[:, 1].max() - V[:, 1].min())
                u = np.clip((u - 0.25) / 0.5, 0, 1)
                u = u * u * (3 - 2 * u)
                moi = []
                for d, k in zip(ts, u):
                    e = {b: w * (1 - float(k)) for b, w in d.items() if w * (1 - float(k)) > 0.02}
                    if k > 0.02:
                        e[bx] = e.get(bx, 0.0) + float(k)
                    tot = sum(e.values())
                    moi.append({b: w / tot for b, w in e.items()})
                ts = moi
        sk.luoi_gan(slot, slot, L, ts, the_gioi=V)
        hang = [[(b, *[float(x) for x in (nghich(b) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for b, w in d.items()] for p, d in zip(V, ts)]
        sk.atts[slot][slot]["verts"] = hang
        nho[slot] = (L, ts, V, hang)
        tong[0] += L.n
        tong[1] += len(L.tris)
    return tong


# ---------------------------------------------------------------- IK chân (gọi sau hàm clip của hoa_ho_rig ở chế độ chibi)
def _goi(a):
    return (a + 180.0) % 360.0 - 180.0


def ik(sk, P, t, ten, dur):
    """đặt góc ba xương riêng của từng chân cho khung này. Clip `walk`: bàn chân đi theo một vòng bước tự viết (hai nhịp mỗi vòng clip, hai
    cặp chân chéo lệch nửa nhịp; lúc chống thì nằm trên mặt đất, lúc đưa tới thì nhấc lên). Clip khác: cổ chân tới chỗ xương bàn chân của
    họ đang ở (bám đất như họ), với không tới thì duỗi thẳng về phía đó. Tính trong hệ chưa áp xương `move` (clip có lật, co cả con)."""
    ds = getattr(sk, "chan_chibi", None)
    if not ds:
        return
    Q = P.copy()
    Q.t.pop("move", None)
    W = sk.the_gioi(Q)
    nho = sk.__dict__.setdefault("_ik_truoc", {})
    for c in ds:
        Wp = W[c["cha"]]
        Hh = (Wp @ np.array([c["hip"][0], c["hip"][1], 1.0]))[:2]
        gp = khung.goc_mat(Wp)
        L1, L2 = c["L1"], c["L2"]
        if ten == "walk":
            ph = 2 * math.pi * (2 * t / dur + c["pha"])
            leg = L1 + L2
            T = np.array([Hh[0] + (c["A0"][0] - c["H0"][0]) - 0.26 * leg * math.cos(ph), c["A0"][1] + 0.20 * leg * max(0.0, math.sin(ph))])
            xoay = -16.0 * max(0.0, math.sin(ph)) * math.cos(ph)
        else:
            Wf = W[c["ban"]]
            T = (Wf @ np.array([c["mat_ca"][0], c["mat_ca"][1], 1.0]))[:2]
            xoay = 0.5 * _goi(khung.goc_mat(Wf) - c["ban_goc0"])
        d = T - Hh
        dist = float(np.hypot(*d))
        a0 = math.atan2(d[1], d[0]) if dist > 1e-6 else math.radians(c["gr0"])
        grd = math.degrees(a0)                                 # trục chân lúc này: háng → đích
        ep = 1.0
        if dist >= c["D0"]:                                    # đích xa hơn lúc nghỉ: duỗi gối ra (IK hai khúc), hết tầm thì duỗi thẳng
            dc = min(dist, L1 + L2 - 1e-3)
            A = math.acos(max(-1.0, min(1.0, (L1 * L1 + dc * dc - L2 * L2) / (2 * L1 * dc))))
            g1 = a0 + c["dau"] * A
            Kk = Hh + L1 * np.array([math.cos(g1), math.sin(g1)])
            Tc = Hh + dc * np.array([math.cos(a0), math.sin(a0)])
            g1d, g2d = math.degrees(g1), math.degrees(math.atan2(Tc[1] - Kk[1], Tc[0] - Kk[0]))
            Ac = Tc
        else:
            # đích GẦN hơn lúc nghỉ (thân nhún xuống, bàn chân nhấc lên): KHÔNG gập thêm gối (chân mập một khúc gập gối là lưới đè lên
            # nhau, méo: người dùng 2026-11-14 "khi nhún chân xuống 2 chân trước lỗi ... cho khớp ngắn lại chứ không đè khớp gây méo").
            # Giữ nguyên hình chân lúc nghỉ, ÉP NGẮN cả chân dọc trục háng → cổ chân bằng tỉ lệ của xương gốc chân; bàn chân nhân
            # ngược lại để không bị bẹp theo.
            g1d, g2d = grd + (c["ga0"] - c["gr0"]), grd + (c["gb0"] - c["gr0"])
            ep = max(0.08, dist / c["D0"])
            Ac = T
        if ep < 0.999:
            P.scale(c["r"], ep, 1.0)
        lpc = np.linalg.solve(Wp, np.array([Ac[0], Ac[1], 1.0]))        # bàn chân: dời tới đầu ống chân (trong hệ xương thân)
        P.move(c["c"], float(lpc[0]) - c["ban_dp"][0], float(lpc[1]) - c["ban_dp"][1])
        for b, v in ((c["r"], (grd - gp) - (c["gr0"] - c["cha_goc0"])), (c["a"], (g1d - grd) - (c["ga0"] - c["gr0"])),
                     (c["b"], (g2d - g1d) - (c["gb0"] - c["ga0"])), (c["c"], xoay - (gp - c["cha_goc0"]))):
            v = _goi(v)
            khoa = (ten, b)
            if t > 1e-6 and khoa in nho:                       # liền mạch với khung trước (khỏi nhảy 360°)
                v = nho[khoa] + _goi(v - nho[khoa])
            nho[khoa] = v
            P.rot(b, v)


if __name__ == "__main__":
    if sys.argv[1:2] == ["cat"]:
        cat()
    else:
        print(__doc__)
