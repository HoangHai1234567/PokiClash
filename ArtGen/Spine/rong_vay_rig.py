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
CLIPS = [("idle", "idle_01", True, []), ("attack", "skill_01", False, [(0.55, "trung", "")]),
         ("cast", "skill_02", False, [(0.8, "phun", ""), (1.3, "het_phun", "")]),
         ("skill", "skill_03", False, [(0.7, "gam", ""), (1.5, "het_gam", "")]), ("hit", "hit_01", False, []),
         ("die", "die_01", False, [])]
TAN = 0.45                   # die: giữ dáng cuối rồi mờ dần chừng này giây
# người dùng 2026-11-11: "bỏ bớt vây ở thân đi để đỡ bị hiệu ứng vây lồng nhau": bỏ sáu vây nhỏ / khuất (lòng vòng cuộn, dưới thân,
# sau thân giữa), giữ năm vây buồm trên lưng và mép ngoài vòng cuộn (vay_07, 09, 10, 14, 15)
BO_VAY = ("vay_06", "vay_08", "vay_11", "vay_12", "vay_13", "vay_16")


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
    for b in giu:
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG, sx=b["sx"], sy=b["sy"])
    # kiểm: xương của mình trùng xương của họ ở dáng gốc
    lech = max(float(np.hypot(sk.goc_tg(b["name"])[0] - b["x"] * KG, sk.goc_tg(b["name"])[1] - b["y"] * KG)) for b in D["bones"] if b["name"] in sk.bi)
    print(f"{len(sk.bones)} xương; dáng gốc lệch xương của con gốc tối đa {lech:.3f} đơn vị rig")

    by_slot = {a["slot"]: a for a in D["atts"]}
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
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
            tong[0] += L.n
            tong[1] += len(L.tris)
            continue
        a = by_slot[BAM[t]]
        pg = os.path.join(RV.MANH, "part", BAM[t] + ".png")  # mảnh vẽ ĐÚNG KHUNG ảnh vùng của part (rong_vay.py cat_part): nguyên lưới của họ
        if os.path.exists(pg):
            # thu nhỏ ở dạng nhân sẵn alpha (RGBa): điểm trong suốt còn mang màu giấy trắng, thu nhỏ RGBA thường sẽ loang trắng
            # vào mép → vạch trắng ở chỗ nối đã xoá mực
            pn = lambda sl: os.path.join(RV.MANH, "part_noi", sl + ".png")          # noqa: E731  bản đã xoá vạch mực chỗ nối (noi_part)
            nap = lambda f: (lambda g: anh.loang_mau(g.resize((max(2, round(g.width / RV.PART_Z * 2 * SC * RES)),   # noqa: E731
                                                                 max(2, round(g.height / RV.PART_Z * 2 * SC * RES))), Image.LANCZOS).convert("RGBA")))(Image.open(f).convert("RGBA").convert("RGBa"))
            sk.anh(t, nap(pn(BAM[t]) if os.path.exists(pn(BAM[t])) else pg))
            L = gan_nguyen(sk, t, t, a, ten, Wc)
            tong[0] += L.n
            tong[1] += len(L.tris)
            ghi = f"  {t:12s} ← {BAM[t]:16s} mảnh vẽ đúng khung part, nguyên lưới của họ {L.n} đỉnh"
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
    for e, m in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả"), ("het_phun", "hết nhả"), ("gam", "chiêu cuối bung"),
                 ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]])


def chuyen_dong(sk, info):
    """clip của con gốc → {clip: (dài giây, {xương: mảng (số khung, 5) = xoay độ, dời x, y (đơn vị rig của mình), tỉ lệ x, y nhân}, mắt
    nhắm từng khung)}: lệch của biến đổi RIÊNG đã áp (runtime Spine) so với dáng gốc."""
    S = json.load(open(os.path.join(info["scan"], "sample_clips.json"), encoding="utf-8"))
    IB, ten = info["IB"], info["ten"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    i_nham = info["slots"].index("P_yanjing02")
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i in ids:
            b0 = IB[i]
            A = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
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
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=ev))
    return out


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
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
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN, "Rồng vây (rong_vay) dạng 1", dang=1, so_dang=1, dung_yen=("cast", "skill"), ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, dich_mb=0.9, tran_mb=1.1)


if __name__ == "__main__":
    main(sys.argv[1:])
