# -*- coding: utf-8 -*-
"""tm08 cách lai (DAC_TA mục 5 "Cách lai", Claude điều phối yêu cầu 2026-11-11): thân, vây lưng, vây đuôi, vây ngực gần, mào, đầu
CẮT THẲNG TỪ CONCEPT đã duyệt (vùng loang từ hạt giống, nét mực dày là tường, nhãn gần nhất cho phần còn lại); thân uốn bằng chuỗi
xương dọc ĐƯỜNG TÂM (Dijkstra ưu tiên giữa thân trên mặt nạ), trọng số B-spline chiếu lên đường khớp trên lưới vùng dày của chính
hình concept. Mảnh GPT chỉ còn: hàm dưới + lòng miệng + lưỡi, mí, hai râu đèn (dải GPT uốn theo đường râu đọc trên concept), vây ngực
xa (dạng 2). Đầu dạng 2 phóng 1,3× quanh gáy (ghi rõ khi đo IoU).

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm08_lai.py cat 2      -> inbox/tm08_2/manh_lai/ (lớp .png, lop.json, nhan.png)
    tm08.py rig k tự dùng dung_lai khi có manh_lai/lop.json.
"""
import heapq
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import tm08 as T  # noqa: E402
from quai import anh, khung, luoi, mieng, trongso  # noqa: E402
from quai.khung import Dat  # noqa: E402

CODE = "tm08"

# hạt giống (px concept) từng vùng; "bo_*" = vùng bỏ (thay bằng mảnh GPT)
SEEDS = {
    2: {"dau": [(1300, 160), (1250, 130), (1400, 200), (1350, 225), (1420, 215), (1200, 112), (1252, 92), (1310, 78), (1190, 140)],
        "bo_ham": [(1400, 262), (1450, 258), (1395, 245), (1430, 245)],
        "than": [(1170, 330), (1190, 450), (1215, 560), (1200, 680), (1100, 790), (990, 830), (870, 745), (760, 650), (640, 640),
                 (520, 700), (400, 780), (300, 830), (210, 870), (1262, 400), (1292, 600), (1050, 862), (800, 760), (560, 760),
                 (250, 905), (1235, 300), (1165, 390), (1150, 500), (1120, 760)],
        "vay_lung": [(1060, 330), (1030, 450), (1030, 560), (960, 640), (650, 470), (560, 520), (480, 580), (380, 680), (300, 760),
                     (230, 820), (760, 470), (870, 540), (1080, 260)],
        "duoi_vay": [(110, 660), (215, 700), (70, 780), (130, 820)],
        "vay_nguc": [(1240, 280), (1215, 255)],
        "bo_rau": [(1372, 510), (1440, 482), (1352, 340), (1425, 340)]},
    1: {"dau": [(1100, 400), (1250, 300), (1300, 450), (1000, 300), (980, 250), (1150, 540), (1300, 520)],
        "bo_ham": [(1200, 528), (1240, 520), (1225, 512)],
        "mao": [(900, 150), (750, 300), (1000, 100), (700, 420), (820, 250), (1100, 130)],
        "than": [(900, 650), (850, 800), (950, 750), (780, 900), (650, 935), (520, 920), (430, 860), (1000, 700), (1020, 800),
                 (560, 950), (720, 560), (730, 650), (740, 720), (890, 880), (1010, 870)],
        "vay_than": [(700, 500), (720, 560), (732, 650), (742, 720), (745, 760)],
        "vay_nguc": [(880, 665), (860, 640)],
        "vay_nguc2": [(890, 790), (870, 760)],
        "duoi_vay": [(320, 760), (330, 850), (290, 740)],
        "bo_rau": [(1145, 770), (1222, 760), (1135, 660), (1210, 650)]},
}
# thứ tự vẽ sau -> trước (vùng concept); vùng "bo_*" không ra lớp
ORDER = {2: ["vay_lung", "than", "duoi_vay", "vay_nguc", "dau"], 1: ["mao", "than", "duoi_vay", "vay_nguc2", "vay_nguc", "dau"]}
# lớp mọc thêm (px concept) dưới lớp nào: (lớp, [lớp đè lên], px, màu tô: None = trung vị vùng)
GROW = {2: [("vay_lung", ["than"], 36), ("than", ["dau", "bo_ham", "vay_nguc"], 45), ("vay_nguc", ["than"], 0), ("duoi_vay", ["than"], 22)],
        1: [("mao", ["dau"], 40), ("than", ["dau", "bo_ham", "vay_nguc", "vay_nguc2"], 45), ("duoi_vay", ["than"], 20)]}
# điểm đọc trên concept (px): gáy (đầu đường tâm, nằm trong đầu một chút), chóp đuôi, bản lề hàm trên đầu, chiều dài hàm, mắt, râu
DAC = {
    2: dict(nape=(1232, 262), tail=(150, 890), hinge=(1335, 255), ham_dai=165, eye=(1385, 185),
            rau=[[(1330, 272), (1340, 330), (1352, 395), (1368, 455), (1374, 505)], [(1398, 272), (1418, 330), (1437, 395), (1446, 450), (1440, 480)]],
            dau_box=(1130, 40, 1510, 300)),
    1: dict(nape=(1000, 545), tail=(415, 838), hinge=(1150, 520), ham_dai=125, eye=(1130, 420),
            rau=[[(1130, 615), (1137, 690), (1143, 765)], [(1205, 612), (1212, 690), (1216, 748)]],
            dau_box=(840, 200, 1380, 620)),
}
HK = {2: 1.3, 1: 1.0}


def paths(k):
    inbox = os.path.join(HERE, "inbox", f"{CODE}_{k}")
    return inbox, os.path.join(inbox, "tai_ve", "L1_duyet.png"), os.path.join(inbox, "manh"), os.path.join(inbox, "manh_lai")


# ---------------------------------------------------------------- cắt từ concept
def fg_mask(rgb, light=222, sat=32):
    mn, mx = rgb.min(2).astype(np.int16), rgb.max(2).astype(np.int16)
    lite = ((mn > light) & (mx - mn < sat)).astype(np.uint8)
    n, lab = cv2.connectedComponents(lite, connectivity=4)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) & (lite > 0)
    fg = (~bg).astype(np.uint8)
    return cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0


def flood(fg, wall, seeds, cho_phep=None):
    """loang 1 px mỗi bước từ hạt giống, tường chặn; cho_phep[tên] = mặt nạ pixel vùng đó được loang vào (theo màu: vây bạc hà không
    loang sang thân chàm và ngược lại, vì tia vây mảnh không chặn được); phần còn lại (nét mực, ô kín) lấy nhãn gần nhất."""
    H, W = fg.shape
    lab = np.zeros((H, W), np.int32)
    names = list(seeds)
    for i, n in enumerate(names, 1):
        for x, y in seeds[n]:
            cv2.circle(lab, (int(x), int(y)), 5, i, -1)
    lab[~fg] = 0
    free = fg & ~wall
    k = np.ones((3, 3), np.uint8)
    for _ in range(2500):
        changed = False
        for i in range(1, len(names) + 1):
            d = cv2.dilate((lab == i).astype(np.uint8), k) > 0
            new = d & free & (lab == 0)
            if cho_phep and names[i - 1] in cho_phep:
                new &= cho_phep[names[i - 1]]
            if new.any():
                lab[new] = i
                changed = True
        if not changed:
            break
    rest = fg & (lab == 0)
    if rest.any():
        src = lab > 0
        _, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys, xs = np.nonzero(src)
        srclab = lab[ys, xs]
        lab[rest] = srclab[li[rest] - 1]
    return lab, names


def duong_tam(mask, p0, p1, step=3):
    """đường tâm thân: Dijkstra trên lưới thu nhỏ `step`, giá mỗi bước = dài × (1 + 60 / (dt + 2)) (ưu tiên giữa thân), từ p0 tới p1.
    Trả danh sách điểm px concept (đã làm mượt)."""
    m = mask[::step, ::step]
    dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    H, W = m.shape

    def near(p):
        ys, xs = np.nonzero(m)
        j = int(np.argmin((xs - p[0] / step) ** 2 + (ys - p[1] / step) ** 2))
        return int(ys[j]), int(xs[j])
    s, e = near(p0), near(p1)
    cost = 1.0 + 60.0 / (dt + 2.0)
    dist = np.full((H, W), np.inf)
    prev = -np.ones((H, W, 2), np.int32)
    dist[s] = 0
    pq = [(0.0, s)]
    nb = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)]
    while pq:
        d, (y, x) = heapq.heappop(pq)
        if (y, x) == e:
            break
        if d > dist[y, x]:
            continue
        for dy, dx, ln in nb:
            yy, xx = y + dy, x + dx
            if 0 <= yy < H and 0 <= xx < W and m[yy, xx]:
                nd = d + ln * 0.5 * (cost[y, x] + cost[yy, xx])
                if nd < dist[yy, xx]:
                    dist[yy, xx] = nd
                    prev[yy, xx] = (y, x)
                    heapq.heappush(pq, (nd, (yy, xx)))
    pts = []
    cur = e
    while cur[0] >= 0:
        pts.append((cur[1] * step + step / 2, cur[0] * step + step / 2))
        cur = tuple(prev[cur])
        if cur == (-1, -1) or len(pts) > 100000:
            break
    pts = np.array(pts[::-1], float)
    for _ in range(12):
        pts[1:-1] = 0.25 * pts[:-2] + 0.5 * pts[1:-1] + 0.25 * pts[2:]
    return pts


def pca_truc(mask, goc):
    """trục chính của vùng từ điểm gốc (px concept) tới điểm xa nhất theo hướng PCA."""
    ys, xs = np.nonzero(mask)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(axis=0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    ax = vt[0]
    g = np.asarray(goc, float)
    if ((c - g) @ ax) < 0:
        ax = -ax
    proj = (P - g) @ ax
    tip = g + ax * proj.max()
    return g, tip


def cat(k):
    inbox, con_p, manh, out = paths(k)
    os.makedirs(out, exist_ok=True)
    ref = np.asarray(Image.open(con_p).convert("RGB"))
    H, W = ref.shape[:2]
    fg = fg_mask(ref)
    lum = ref.astype(np.int32).sum(2) / 3
    ink = (lum < 88) & fg
    dti = cv2.distanceTransform(ink.astype(np.uint8), cv2.DIST_L2, 3)
    wall = cv2.dilate((dti >= 2.2).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0   # nét mực dày (viền, ranh vùng); tia vây mảnh không chặn
    wall &= ink
    r_, g_, b_ = [ref[..., i].astype(int) for i in range(3)]
    mint = (g_ > r_ + 45) & (g_ > b_ + 8) & (lum < 215) & fg          # vây bạc hà (và chấm đèn, hạt đèn)
    allow = {}
    for n in SEEDS[k]:
        if n in ("vay_lung", "duoi_vay", "vay_nguc", "vay_nguc2", "mao", "vay_than"):
            allow[n] = mint | ink
        elif n in ("than",):
            allow[n] = ~mint | ink
    lab, names = flood(fg, wall, SEEDS[k], allow)
    idx = {n: i + 1 for i, n in enumerate(names)}
    rgba = np.dstack([ref, np.where(fg, 255, 0).astype(np.uint8)])
    info = {"ref_size": [W, H], "lop": {}, "dac": {kk: v for kk, v in DAC[k].items()}}
    k3 = np.ones((3, 3), np.uint8)
    grown = {}
    for n, under, px in GROW[k]:
        if px <= 0:
            continue
        m = lab == idx[n]
        hid = np.zeros((H, W), bool)
        for u in under:
            hid |= lab == idx[u]
        near = cv2.dilate(m.astype(np.uint8), k3, iterations=px) > 0
        grown[n] = hid & near
    if "vay_than" in idx:   # vây lưng thấp liền thân (dạng 1): nhập vào vùng thân
        lab[lab == idx["vay_than"]] = idx["than"]
    for n in ORDER[k]:
        m = lab == idx[n]
        layer = np.where(m[..., None], rgba, 0).astype(np.uint8)
        g = grown.get(n)
        if g is not None and g.any():
            px = ref[m]
            lm = px.astype(np.int32).sum(1) / 3
            keep = (lm > 90) & (lm < 235)
            col = np.median(px[keep], axis=0) if keep.any() else np.array([120, 120, 160])
            rng = np.random.default_rng(7)
            layer[..., :3][g] = np.clip(col[None, :] + rng.integers(-9, 10, (int(g.sum()), 1)), 0, 255).astype(np.uint8)
            layer[..., 3][g] = 255
            full = m | g
            edge = full & ~(cv2.erode(full.astype(np.uint8), k3, iterations=3) > 0) & g
            layer[..., :3][edge] = (43, 33, 24)
            print(f"  {n}: mọc thêm {int(g.sum())} px (mực mép {int(edge.sum())})")
        nlab, cc, st, _ = cv2.connectedComponentsWithStats((layer[..., 3] > 128).astype(np.uint8), connectivity=8)
        small = np.isin(cc, [i for i in range(1, nlab) if st[i, cv2.CC_STAT_AREA] < 300])
        if small.any():
            layer[small] = 0
        a = cv2.GaussianBlur(layer[..., 3].astype(np.float32) / 255, (3, 3), 0.8)
        layer[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
        ys, xs = np.nonzero(layer[..., 3] > 8)
        if not len(xs):
            print(f"  {n}: TRỐNG")
            continue
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        Image.fromarray(layer[y0:y1, x0:x1], "RGBA").save(os.path.join(out, n + ".png"))
        info["lop"][n] = {"x0": x0, "y0": y0, "w": x1 - x0, "h": y1 - y0, "px": int(m.sum())}
        print(f"  {n:9s} ({x0},{y0}) {x1 - x0}x{y1 - y0}, {int(m.sum())} px")
    # đường tâm thân (Dijkstra) từ gáy tới chóp đuôi trên vùng thân (+ vùng bị đầu che: thêm vùng đầu để đi vào gáy)
    than = (lab == idx["than"]) | grown.get("than", np.zeros((H, W), bool))
    dau_m = lab == idx["dau"]
    pts = duong_tam(than | dau_m, DAC[k]["nape"], DAC[k]["tail"])
    # cắt phần đường nằm trong đầu trừ 40 px cuối (đường bắt đầu ở gáy trong đầu)
    dt_than = cv2.distanceTransform(than.astype(np.uint8), cv2.DIST_L2, 5)
    thick = np.array([2 * dt_than[int(min(H - 1, max(0, p[1]))), int(min(W - 1, max(0, p[0])))] for p in pts])
    info["duong_tam"] = [[float(x), float(y)] for x, y in pts]
    info["day"] = [float(t) for t in thick]
    # trục vây đuôi, vây ngực, mào (gốc = điểm vùng gần đường tâm / gần tâm đầu nhất)
    def goc_gan(mask, target):
        ys, xs = np.nonzero(mask)
        P = np.stack([xs, ys], 1).astype(float)
        d = np.min(((P[:, None, :] - target[None, :, :]) ** 2).sum(2), axis=1)
        j = int(np.argmin(d))
        return (float(P[j, 0]), float(P[j, 1]))
    truc = {}
    for n in [q for q in ("duoi_vay", "vay_nguc", "vay_nguc2", "mao") if q in idx]:
        m = lab == idx[n]
        if not m.any():
            continue
        if n == "mao":
            hc = np.array([[DAC[k]["eye"][0] - 120, DAC[k]["eye"][1] + 10]], float)
            g0 = goc_gan(m, hc)
        else:
            g0 = goc_gan(m, pts[::4])
        g, tip = pca_truc(m, g0)
        truc[n] = {"goc": [float(g[0]), float(g[1])], "ngon": [float(tip[0]), float(tip[1])]}
    info["truc"] = truc
    json.dump(info, open(os.path.join(out, "lop.json"), "w", encoding="utf-8"), indent=1)
    # bản đồ vùng + đường tâm để soi
    pal = np.array([(255, 255, 255), (230, 80, 80), (80, 160, 230), (90, 200, 120), (240, 200, 60), (200, 120, 220), (120, 220, 220),
                    (250, 150, 90), (150, 150, 150), (60, 60, 60), (180, 90, 40)], np.uint8)
    vis = pal[np.clip(lab, 0, len(pal) - 1)].copy()
    vis[wall] = (40, 30, 20)
    cv2.polylines(vis, [np.int32(np.round(pts)).reshape(-1, 1, 2)], False, (0, 0, 0), 3)
    for n, ps in SEEDS[k].items():
        for x, y in ps:
            cv2.circle(vis, (int(x), int(y)), 7, (0, 0, 0), 2)
    for n, tr in truc.items():
        cv2.line(vis, tuple(int(v) for v in tr["goc"]), tuple(int(v) for v in tr["ngon"]), (255, 0, 255), 3)
    Image.fromarray(np.concatenate([ref, vis], 1)).save(os.path.join(out, "nhan.png"))
    print(f"  nhãn: {', '.join(f'{n}={idx[n]}' for n in names)}; đường tâm {len(pts)} điểm -> {os.path.join(out, 'nhan.png')}")


# ---------------------------------------------------------------- dựng rig
def dung_lai(k, ti=None):
    T.TI = ti or T.TI_K[k]
    TI = T.TI
    cfg = T.CFG[k]
    inbox, con_p, manh, out = paths(k)
    meta = json.load(open(os.path.join(out, "lop.json"), encoding="utf-8"))
    dac = meta["dac"]
    hk = HK[k]
    to_rig, to_concept = T.toa_do(cfg)
    Hcon = (cfg["ground"] - cfg["dinh"]) * TI
    T.B_VIEN, T.B_TRONG = round(0.015 * Hcon, 1), round(0.02 * Hcon, 1)
    concept = np.asarray(Image.open(con_p).convert("RGB"))
    print(f"  [lai] dạng {k}: TI {TI}, chiều cao {Hcon:.0f}, bước {T.B_VIEN}/{T.B_TRONG}")

    def nap_lop(n):
        im = Image.open(os.path.join(out, n + ".png")).convert("RGBA")
        im = im.resize((max(2, round(im.width * TI)), max(2, round(im.height * TI))), Image.LANCZOS)
        return anh.loang_mau(im)

    def P_lop(n):
        o = meta["lop"][n]
        return lambda pts: to_rig(np.asarray(pts, float).reshape(-1, 2) / TI + np.array([o["x0"], o["y0"]], float))
    lop = {n: nap_lop(n) for n in meta["lop"]}
    pc = anh.nap_manh(manh, T.GIU_CHO, ti_le=TI)        # mảnh GPT (hàm, lòng miệng, lưỡi, mí, râu, vây ngực xa)
    sk = khung.Sk(f"{CODE}_{k}")
    for n, im in lop.items():
        sk.anh("c_" + n, im)
    dung_gpt = {"ham", "mieng", "luoi", "mi", "rau"} | ({"vay_nguc"} if k == 2 else set())
    for n in dung_gpt:
        sk.anh(n, pc[n])
    # ---- đường tâm -> khớp
    Qc = np.array(meta["duong_tam"], float)
    day = np.array(meta["day"], float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(Qc, axis=0).T))]
    Ltot_c = float(d[-1])
    N = cfg["N"]
    Lr = Ltot_c * TI
    seg = Lr / N
    s_j = np.linspace(0, Ltot_c, N + 1)
    Jc = np.stack([np.interp(s_j, d, Qc[:, 0]), np.interp(s_j, d, Qc[:, 1])], 1)
    Tj = np.interp(s_j, d, day)
    J = to_rig(Jc)
    c = int(round(cfg["c_s"] * N))
    lo, hi = max(1, c - 2), min(N - 1, c + 2)
    c = int(lo + np.argmin(J[lo:hi + 1, 1]))
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("shadow", "root")
    sk.xuong("dat", "root")
    sk.xuong("than", "move", J[c, 0], J[c, 1], the_gioi=True, dai=20)
    fw = sk.chuoi("fw", "than", J[c::-1])
    bk = sk.chuoi("bk", "than", J[c:])
    names_s = fw[::-1] + bk
    # pháp tuyến lưng tại khớp (rig)
    tgJ = np.gradient(J, axis=0)
    tgJ /= np.maximum(1e-9, np.hypot(*tgJ.T))[:, None]
    ndJ = np.stack([tgJ[:, 1], -tgJ[:, 0]], 1)
    # ---- đầu (phóng hk quanh gáy)
    im_d = lop["dau"]
    o_d = meta["lop"]["dau"]
    nape_px = ((dac["nape"][0] - o_d["x0"]) * TI, (dac["nape"][1] - o_d["y0"]) * TI)
    dat_dau = Dat(J[0, 0], J[0, 1], goc=0.0, ti=hk, neo=nape_px, neo_px=True)
    sk.xuong("dau", fw[-1], J[0, 0], J[0, 1], goc=0.0, dai=100, the_gioi=True)
    a_d = np.asarray(im_d)[..., 3] > 60
    yy, xx = np.nonzero(a_d)
    i_r = np.argmax(xx)
    mui = dat_dau.mot((xx[i_r], yy[i_r]), im_d.width, im_d.height)
    mieng_pt = mui + np.array([-6.0, -4.0])
    sk.xuong("mieng", "dau", mieng_pt[0], mieng_pt[1], goc=0.0, dai=30, the_gioi=True)
    # ---- hàm GPT: bản lề đọc trên concept, dài hàm theo concept
    im_j = pc["ham"]
    hinge_px = ((dac["hinge"][0] - o_d["x0"]) * TI, (dac["hinge"][1] - o_d["y0"]) * TI)
    ban_le = dat_dau.mot(hinge_px, im_d.width, im_d.height)
    jw_sheet = im_j.width / TI
    s_j_ = dac["ham_dai"] / jw_sheet * hk
    r_j = cfg.get("ham_r", 0.0)
    ban_le_px = T.diem_mep(im_j, "trai", 0.12)
    dat_ham = Dat(ban_le[0], ban_le[1], goc=r_j, ti=s_j_, neo=ban_le_px, neo_px=True)
    mui_j_px = T.diem_mep(im_j, "phai", 0.08)
    mui_j = dat_ham.mot(mui_j_px, im_j.width, im_j.height)
    gj = math.degrees(math.atan2(*(mui_j - ban_le)[::-1]))
    sk.xuong("ham", "dau", ban_le[0], ban_le[1], goc=gj, dai=float(np.hypot(*(mui_j - ban_le))), the_gioi=True)
    im_l = pc["luoi"]
    uj = (mui_j - ban_le) / max(1e-9, np.hypot(*(mui_j - ban_le)))
    dat_luoi = Dat(*(ban_le + uj * 0.12 * np.hypot(*(mui_j - ban_le)) + np.array([-uj[1], uj[0]]) * 6), goc=gj, ti=hk * 0.5, neo=(0.0, 0.5))
    Ll = luoi.luoi_dai(im_l, 4, ten="luoi", buoc=12, hang=4)
    luoi_b = sk.chuoi("luoi", "ham", dat_luoi.ra(Ll.khop(4), *im_l.size))
    # ---- râu: dải GPT uốn theo đường râu đọc trên concept (con của hàm)
    im_r = pc["rau"]
    Lr_ = luoi.luoi_dai(im_r, cfg["rau_n"], ten="rau", buoc=12, hang=3)
    rau = {}
    rau_curve = {}
    for side, pts_c in zip(("s", "t"), dac["rau"]):
        pc_ = np.asarray(pts_c, float)
        pr = J[0] + hk * (to_rig(pc_) - J[0])                   # râu thuộc đầu: phóng cùng đầu quanh gáy
        dd = np.r_[0, np.cumsum(np.hypot(*np.diff(pr, axis=0).T))]
        Lc = float(dd[-1])
        ti_r = Lc / max(1.0, Lr_.truc[1][-1])                  # dải GPT co cho dài bằng râu concept
        sj = np.linspace(0, Lc, cfg["rau_n"] + 1)
        Jr = np.stack([np.interp(sj, dd, pr[:, 0]), np.interp(sj, dd, pr[:, 1])], 1)
        rau[side] = (sk.chuoi("rau" + side, "ham", Jr), None)
        rau_curve[side] = (pr, dd, ti_r)
    # ---- vây ngực: dạng 2 gần = concept, xa = GPT sau thân; dạng 1 hai vây concept
    vay = {}
    vay_lop = {}
    for n, side in (("vay_nguc", "t"), ("vay_nguc2", "s")):
        if n not in meta["lop"]:
            continue
        tr = meta["truc"][n]
        g, tip = to_rig(tr["goc"]), to_rig(tr["ngon"])
        Jv = np.array([g, 0.5 * (g + tip), tip])
        # xương cha: đốt thân gần gốc vây nhất
        dj = np.hypot(*(J[:-1] - g).T)
        par = names_s[int(np.argmin(dj))]
        vay[side] = (sk.chuoi("vay" + side, par, Jv), None)
        vay_lop[side] = (n, Jv, par)
    if k == 2:
        im_v = pc["vay_nguc"]
        Lv = luoi.luoi_dai(im_v, 2, ten="vay_nguc", buoc=16, hang=6)
        g = to_rig(meta["truc"]["vay_nguc"]["goc"]) + np.array([-8 * TI, -10 * TI])   # nấp sau vây gần, hơi thấp
        tip = to_rig(meta["truc"]["vay_nguc"]["ngon"])
        gv = math.degrees(math.atan2(*(tip - g)[::-1])) - 8
        d_v = Dat(g[0], g[1], goc=gv, ti=cfg["vay_ti"] * 0.72, neo=(0.0, 0.5))
        dj = np.hypot(*(J[:-1] - g).T)
        xv = names_s[int(np.argmin(dj))]
        vay["s"] = (sk.chuoi("vays", xv, d_v.ra(Lv.khop(2), *im_v.size)), d_v)
        vay_gpt = (Lv, d_v, xv)
    # ---- mào (dạng 1): 3 đốt từ gốc lên đỉnh, con của đầu
    mao = None
    if "mao" in meta["lop"]:
        tr = meta["truc"]["mao"]
        g, tip = to_rig(tr["goc"]), to_rig(tr["ngon"])
        Jm = np.array([g * (1 - u) + tip * u for u in (0, 0.35, 0.7, 1.0)])
        mao = sk.chuoi("mao", "dau", Jm)
    # ---- vây đuôi: 2 đốt từ chóp đuôi
    tr = meta["truc"]["duoi_vay"]
    g, tip = to_rig(tr["goc"]), to_rig(tr["ngon"])
    Jdv = np.array([J[N], 0.5 * (J[N] + tip), tip])
    dvb = sk.chuoi("dv", bk[-1], Jdv)
    # ---- vây lưng (dạng 2): xương vl_i ở mép lưng từng khớp, con của đốt thân
    vl = []
    Jvl = None
    if "vay_lung" in meta["lop"]:
        Jvl = J + ndJ * (Tj * TI / 2)[:, None]
        for i in range(N):
            sk.xuong(f"vl{i}", names_s[i], Jvl[i, 0], Jvl[i, 1], goc=math.degrees(math.atan2(tgJ[i][1], tgJ[i][0])), dai=seg, the_gioi=True)
            vl.append(f"vl{i}")
    # ---- slot: sau -> trước
    sk.slot("cat_dat", "dat")
    if vl:
        sk.slot("vay_lung", vl[0], "c_vay_lung")
    if k == 2:
        sk.slot("vay_s", vay["s"][0][0], "vay_nguc")
    if mao:
        sk.slot("mao", mao[0], "c_mao")
    sk.slot("rau_s", rau["s"][0][0], "rau")
    sk.slot("than", names_s[0], "c_than")
    sk.slot("duoi_vay", dvb[0], "c_duoi_vay")
    if "s" in vay_lop:
        sk.slot("vay_s", vay["s"][0][0], "c_vay_nguc2")
    sk.slot("vay_t", vay["t"][0][0], "c_vay_nguc")
    sk.slot("mieng", "ham", "mieng")
    sk.slot("ham", "ham", "ham")
    sk.slot("luoi", luoi_b[0], "luoi", an=True)
    sk.slot("dau", "dau", "c_dau")
    sk.slot("mi", "dau", "mi", an=True)
    sk.slot("rau_t", rau["t"][0][0], "rau")
    sk.cat("cat_dat", "rau_t", [(-4000, -80), (4000, -80), (4000, 6000), (-4000, 6000)])   # mặt đất cắt (trồi/chìm); đuôi idle không chạm
    # ---- lưới thân: lưới vùng dày của hình concept, trọng số chiếu lên đường khớp
    im_b = lop["than"]
    Lb = luoi.luoi_vung(im_b, ten="than", buoc_theo_cao=Hcon)
    Qb = P_lop("than")(Lb.pts)
    Wb = trongso.chuoi_chieu(Qb, J, names_s)
    Wb = trongso.lam_tron(Lb, Wb, 1)
    trongso.kiem(Wb, "than")
    sk.luoi_gan("than", "c_than", Lb, Wb, the_gioi=Qb)
    # ---- vây lưng
    if vl:
        im_f = lop["vay_lung"]
        Lf = luoi.luoi_vung(im_f, ten="vay_lung", buoc_theo_cao=Hcon)
        Qf = P_lop("vay_lung")(Lf.pts)
        Wf = trongso.chuoi_chieu(Qf, Jvl, vl)
        sk.luoi_gan("vay_lung", "c_vay_lung", Lf, Wf, the_gioi=Qf)
    # ---- đầu: lưới vùng, gáy hoà vào đốt cổ đầu
    Lh = luoi.luoi_vung(im_d, ten="dau", buoc_theo_cao=Hcon)
    Qh = dat_dau.ra(Lh.pts, im_d.width, im_d.height)
    rg = 0.22 * im_d.height
    Wh = trongso.vung(Lh, [(fw[-1], T.vung_tron(im_d, nape_px, rg)), ("dau", [(0, 0), (im_d.width, 0), (im_d.width, im_d.height), (0, im_d.height)])],
                      dai_hoa=0.12 * im_d.height)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "c_dau", Lh, Wh, the_gioi=Qh)
    # ---- hàm, lòng miệng, mí (GPT)
    Lj = luoi.luoi_vung(im_j, T.B_VIEN * 0.85, T.B_TRONG * 0.85, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *im_j.size), ban_le, mui_j, "dau", "ham", u0=-0.1, u1=0.16)
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    mieng.long_mieng(sk, "mieng", "mieng", "dau", "ham", ban_le, mui, duoi=-0.26, doc=(-0.06, 0.92))
    eye_px = (int((dac["eye"][0] - o_d["x0"]) * TI), int((dac["eye"][1] - o_d["y0"]) * TI))
    kq = mieng.fit_lid(im_d, pc["mi"], hat=eye_px, ten=f"dạng {k} (lai)")
    sk.manh("mi", "mi", mieng.dat_mi(dat_dau, im_d, kq))
    Wl = trongso.chuoi(Ll.s, Ll.truc[1][-1] / 4, luoi_b, cha="ham", cha_hoa=0.6)
    sk.luoi_gan("luoi", "luoi", Ll, Wl, dat=dat_luoi)
    # ---- râu: dải GPT uốn theo đường râu
    for side, (names, _) in rau.items():
        pr, dd, ti_r = rau_curve[side]
        s_v = np.clip(Lr_.s * ti_r, 0, dd[-1])
        P = np.stack([np.interp(s_v, dd, pr[:, 0]), np.interp(s_v, dd, pr[:, 1])], 1)
        P2 = np.stack([np.interp(np.clip(s_v + 3, 0, dd[-1]), dd, pr[:, 0]), np.interp(np.clip(s_v + 3, 0, dd[-1]), dd, pr[:, 1])], 1)
        tg = P2 - P
        tg /= np.maximum(1e-9, np.hypot(*tg.T))[:, None]
        nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
        yc = Lr_.truc[0][0][1]
        off = (Lr_.pts[:, 1] - yc) * ti_r
        V = P + nr * off[:, None] + tg * ((Lr_.s * ti_r - s_v))[:, None]
        Wr = trongso.chuoi(s_v, dd[-1] / cfg["rau_n"], names, cha="ham", cha_hoa=0.5)
        sk.luoi_gan("rau_" + side, "rau", Lr_, Wr, the_gioi=V)
    # ---- vây ngực concept, vây xa GPT
    for side, (n, Jv, par) in vay_lop.items():
        im_v = lop[n]
        Lv_ = luoi.luoi_vung(im_v, ten=n, buoc_theo_cao=Hcon)
        Qv = P_lop(n)(Lv_.pts)
        Wv = trongso.chuoi_chieu(Qv, Jv, vay[side][0], cha=par, cha_hoa=0.7)
        sk.luoi_gan("vay_" + side, "c_" + n, Lv_, Wv, the_gioi=Qv)
    if k == 2:
        Lv, d_v, xv = vay_gpt
        Wv = trongso.chuoi(Lv.s, Lv.truc[1][-1] / 2, vay["s"][0], cha=xv, cha_hoa=0.7)
        sk.luoi_gan("vay_s", "vay_nguc", Lv, Wv, dat=d_v)
    # ---- mào, vây đuôi
    if mao:
        im_m = lop["mao"]
        Lm = luoi.luoi_vung(im_m, ten="mao", buoc_theo_cao=Hcon)
        Qm = P_lop("mao")(Lm.pts)
        Wm = trongso.chuoi_chieu(Qm, Jm, mao, cha="dau", cha_hoa=0.6)
        sk.luoi_gan("mao", "c_mao", Lm, Wm, the_gioi=Qm)
    im_dv = lop["duoi_vay"]
    Ldv = luoi.luoi_vung(im_dv, ten="duoi_vay", buoc_theo_cao=Hcon)
    Qdv = P_lop("duoi_vay")(Ldv.pts)
    Wdv = trongso.chuoi_chieu(Qdv, Jdv, dvb, cha=bk[-1], cha_hoa=0.6)
    sk.luoi_gan("duoi_vay", "c_duoi_vay", Ldv, Wdv, the_gioi=Qdv)
    for e, m in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                 ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối"), ("troi", "trồi khỏi đất"), ("chim", "chìm xuống")):
        sk.su_kien(e, m)
    info = dict(fw=fw, bk=bk, vl=vl, c=c, N=N, seg=seg, luoi=luoi_b, rau=rau, vay=vay, mao=mao, dv=dvb, J=J, Lr=Lr, pc=pc, k=k,
                to_rig=to_rig, to_concept=to_concept, concept=concept, dat_dau=dat_dau, hk=hk, dau_box=dac["dau_box"], lai=True,
                buoc=(T.B_VIEN, T.B_TRONG))
    return sk, info


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "cat":
        cat(int(sys.argv[2]))
    else:
        print(__doc__)
