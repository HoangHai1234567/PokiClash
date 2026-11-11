"""Khớp mảnh vào concept (dòng Hải Long dạng 1, 2) bằng dò tự động, và đo IoU mặt nạ khung 0 idle với concept (DAC_TA mục 5, bài học
dòng 9: không đoán hệ số tay).

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm10_khop.py khop 2     dò đầu (tỉ lệ, góc, vị trí) + mặt nước + chỗ cổ mọc trên
                                                                        concept -> inbox/tm10_2/rig/khop.json (tm10.patch đọc)
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm10_khop.py iou 2      IoU mặt nạ thân (bỏ nước) khung 0 idle vs concept, ghi lên
                                                                        so_concept.png và khop.json
Dò: SQDIFF có mặt nạ trên Lab (như rig.place), tỉ lệ 0,45–1,2, góc −32…32°, 3 tầng thô → tinh. Hệ rig: 1 đơn vị = 1 px concept, gốc x =
tâm vùng nước, mặt nước concept = CLIPY của rig.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import hai_long as HL  # noqa: E402
import hai_long_soi as S  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
WATER_SLOTS = ("w", "band", "ripple", "mound", "cr", "dr", "rg", "cat", "n_", "song", "nuoc")


def paths(k):
    inbox = os.path.join(HERE, "inbox", f"tm10_{k}")
    return inbox, os.path.join(inbox, "tai_ve", "L1_duyet.png"), os.path.join(inbox, "manh"), os.path.join(inbox, "rig", "khop.json")


def concept_masks(con):
    """mặt nạ (thân, nước) trên concept: nền trắng > 236; nước = khối lam lớn (đóng lỗ bọt trắng), bỏ giọt nhỏ và vệt lam lẻ trên thân."""
    a = np.asarray(con.convert("RGB")).astype(int)
    fg = a.min(axis=2) < 236
    blue = ((a[..., 2] > a[..., 0] + 40) & (a[..., 2] > a[..., 1] + 10)).astype(np.uint8)
    blue = cv2.morphologyEx(blue, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(blue, 8)
    big = np.zeros_like(blue)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 4000:
            big[lab == i] = 1
    water = cv2.morphologyEx(big, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))).astype(bool)
    water &= fg | (cv2.dilate(big, np.ones((5, 5), np.uint8)) > 0)
    foam = fg & (a.min(axis=2) > 196) & (cv2.dilate(big, np.ones((61, 61), np.uint8)) > 0)   # bọt trắng ngà kề nước = nước
    water |= foam
    body = fg & ~water & ~(cv2.dilate(blue, np.ones((3, 3), np.uint8)) > 0)
    body = cv2.morphologyEx(body.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(body, 8)
    body2 = np.zeros_like(body)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500:   # bỏ giọt nước, mẩu lẻ
            body2[lab == i] = 1
    return body2.astype(bool), water


def lab(im):
    """bản đồ lớp màu (H, W, 5) float32: ngọc, san hô, kem, mực, vàng (sừng). Dò theo lớp màu chứ không theo Lab thô: SQDIFF chia
    số điểm thiên về mảnh nhỏ, tương quan chuẩn hoá bị nền sáng át -> cả hai dò nhầm đầu phụ thành thủ lĩnh (lỗi đã gặp)."""
    rgb = np.asarray(im.convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(int)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    ink = v < 95
    jade = (h >= 60) & (h <= 100) & (s > 60) & ~ink
    coral = ((h <= 12) | (h >= 170)) & (s > 90) & (v > 150)
    cream = (h >= 14) & (h <= 40) & (s >= 30) & (s <= 120) & (v > 190)
    gold = (h >= 18) & (h <= 40) & (s > 120) & (v > 170)
    return np.stack([jade, coral, cream, ink, gold], axis=2).astype(np.float32)


def match_piece(con_cls, piece, scales, angles, exclude=None):
    """dò mảnh (RGBA) trên concept: trả (score, cx, cy, góc, tỉ lệ) tốt nhất. Điểm = (tổng trùng lớp màu − phần mảnh rơi lên nền
    trắng) / diện tích mảnh (bất biến theo tỉ lệ). exclude: mặt nạ vùng đã có mảnh khác (bool), tâm rơi vào đó thì bỏ."""
    best = None
    pcls = lab(piece)
    pa = (np.asarray(piece)[..., 3] > 128)
    pcls *= pa[..., None]
    pa = pa.astype(np.float32)
    H_, W_ = con_cls.shape[:2]
    con_bg = (con_cls.sum(axis=2) < 0.5).astype(np.float32)
    nc = con_cls.shape[2]
    for sc in scales:
        for ang in angles:
            M = cv2.getRotationMatrix2D((piece.width / 2, piece.height / 2), ang, sc)
            bw, bh = int(piece.width * sc * 1.4) + 4, int(piece.height * sc * 1.4) + 4
            M[0, 2] += bw / 2 - piece.width / 2
            M[1, 2] += bh / 2 - piece.height / 2
            tm = cv2.warpAffine(pa, M, (bw, bh), flags=cv2.INTER_NEAREST)
            area = float(tm.sum())
            if bw >= W_ or bh >= H_ or area < 200:
                continue
            bg = cv2.matchTemplate(con_bg, tm, cv2.TM_CCORR)
            cover = cv2.matchTemplate(1.0 - con_bg, tm, cv2.TM_CCORR)      # mảnh rơi lên hình concept (lớp nào cũng được)
            hit = np.zeros_like(bg)
            for c in range(nc):
                tc = cv2.warpAffine(pcls[..., c], M, (bw, bh), flags=cv2.INTER_NEAREST)
                if tc.sum() < 1:
                    continue
                hit += cv2.matchTemplate(np.ascontiguousarray(con_cls[..., c]), tc, cv2.TM_CCORR)
            # trùng lớp − 0,8 × sai lớp (mảnh nhỏ lọt vào mảng ngọc phẳng thì viền mực, bờm của nó sai lớp hết) − lên nền
            r = (hit - 0.8 * (cover - hit) - bg) / area
            if exclude is not None:
                ex = exclude[bh // 2: bh // 2 + r.shape[0], bw // 2: bw // 2 + r.shape[1]]
                r = np.where(ex[:r.shape[0], :r.shape[1]], -9.0, r)
            _, mx, _, loc = cv2.minMaxLoc(r)
            if best is None or mx > best[0]:
                best = (float(mx), loc[0] + bw / 2, loc[1] + bh / 2, float(ang), float(sc))
    return best


def refine(con_lab, piece, b, exclude=None):
    s0, a0 = b[4], b[3]
    b2 = match_piece(con_lab, piece, np.arange(s0 - 0.08, s0 + 0.081, 0.02), np.arange(a0 - 6, a0 + 6.1, 2), exclude)
    return b2 if b2 and b2[0] >= b[0] else b


def trace_neck(dtm, body, gay, head_c, y_water, others, step=4):
    """đường tâm cổ từ gáy xuống mặt nước = đường đi rẻ nhất (Dijkstra trên lưới thu 1/step) trong mặt nạ thân, giá mỗi bước =
    1 / (độ sâu vào trong thân + 1): đường bám giữa thân, không lượn vòng (cách lần tham lam theo đỉnh biến đổi khoảng cách bị kẹt,
    xoắn vòng trong thân rộng: lỗi đã gặp). Đích: điểm thân đầu tiên chạm mặt nước. Không vào vùng đầu khác; không quay lên khối đầu mình."""
    import heapq
    H_, W_ = body.shape
    hs, ws = H_ // step, W_ // step
    bs = body[:hs * step, :ws * step].reshape(hs, step, ws, step).mean(axis=(1, 3)) > 0.5
    ds = dtm[:hs * step:step, :ws * step:step]
    hc = np.array(head_c, float)
    own_r = float(np.hypot(gay[0] - hc[0], gay[1] - hc[1])) * 0.9
    yy, xx = np.mgrid[0:hs, 0:ws]
    cx_, cy_ = xx * step, yy * step
    block = ~bs
    for ox, oy, w in others:
        block |= np.hypot(cx_ - ox, cy_ - oy) < w * 0.45
    block |= (np.hypot(cx_ - hc[0], cy_ - hc[1]) < own_r) & (cy_ < gay[1] - 2 * step)
    gy_ = int(y_water) // step
    sx, sy = int(gay[0]) // step, int(gay[1]) // step
    # gáy có thể rơi ngoài mặt nạ vài px: lấy điểm thân gần nhất
    if block[sy, sx] or not bs[sy, sx]:
        cand = np.argwhere(bs & ~block)
        if not len(cand):
            return None
        j = np.argmin((cand[:, 0] - sy) ** 2 + (cand[:, 1] - sx) ** 2)
        sy, sx = cand[j]
    cost = 1.0 / (ds + 1.0)
    dist = np.full((hs, ws), np.inf)
    prev = {}
    dist[sy, sx] = 0.0
    pq = [(0.0, sy, sx)]
    goal = None
    while pq:
        dcur, y, x = heapq.heappop(pq)
        if dcur > dist[y, x]:
            continue
        if y * step >= y_water - 2 * step:
            goal = (y, x)
            break
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < hs and 0 <= nx < ws) or block[ny, nx]:
                continue
            nd = dcur + cost[ny, nx] * (1.414 if dy and dx else 1.0)
            if nd < dist[ny, nx]:
                dist[ny, nx] = nd
                prev[(ny, nx)] = (y, x)
                heapq.heappush(pq, (nd, ny, nx))
    if goal is None:
        return None
    path = [goal]
    while path[-1] in prev:
        path.append(prev[path[-1]])
    path = path[::-1]
    pts = np.array([(x * step + step / 2, y * step + step / 2) for y, x in path], float)
    pts[0] = gay
    if len(pts) > 6:   # làm trơn (trung bình 7 điểm, giữ hai mút) rồi lấy thưa mỗi ~12 px
        k_ = 7
        sm = pts.copy()
        for i in range(1, len(pts) - 1):
            a, b = max(0, i - k_ // 2), min(len(pts), i + k_ // 2 + 1)
            sm[i] = pts[a:b].mean(axis=0)
        pts = sm
    keep = [0] + [i for i in range(1, len(pts) - 1) if i % 3 == 0] + [len(pts) - 1]
    return [tuple(pts[i]) for i in keep]


def khop(k):
    inbox, con_p, manh, out = paths(k)
    con = Image.open(con_p)
    cl = lab(con)
    body, water = concept_masks(con)
    ys, xs = np.nonzero(water)
    X0 = float(xs.mean())
    # mặt nước: trung vị mép trên của khối nước trong 80% bề rộng giữa
    x0w, x1w = np.percentile(xs, 10), np.percentile(xs, 90)
    tops = [np.nonzero(water[:, x])[0].min() for x in range(int(x0w), int(x1w), 6) if water[:, x].any()]
    y_water = float(np.percentile(tops, 30))
    # đầu: dò mảnh đầu thủ lĩnh n lần (loại vùng đã có), rồi gán: thủ lĩnh = to nhất; còn lại trái -> a, phải -> d
    nheads = 3 if k == 2 else 1
    pk_ = Image.open(os.path.join(manh, "head_k.png")).convert("RGBA")
    pk_ = pk_.crop(pk_.getbbox())
    pn_ = Image.open(os.path.join(manh, "head_n.png")).convert("RGBA").crop(Image.open(os.path.join(manh, "head_n.png")).getbbox()) if k == 2 else None
    cands = []
    exclude = np.zeros(body.shape, bool)
    for i in range(nheads):
        ex = exclude if exclude.any() else None
        b = match_piece(cl, pk_, np.arange(0.45, 1.31, 0.1), np.arange(-32, 33, 8), ex)
        b = refine(cl, pk_, b, ex)
        cands.append(b)
        r = int(pk_.width * b[4] * 0.45)
        cv2.circle(exclude.view(np.uint8), (int(b[1]), int(b[2])), r, 1, -1)
    cands.sort(key=lambda b: -b[4])
    order = [("k", cands[0])]
    if k == 2:
        rest = sorted(cands[1:], key=lambda b: b[1])
        order += [("a", rest[0]), ("d", rest[1])]
    heads = {}
    for hid, b in order:
        pname = "head_k" if hid == "k" else "head_n"
        piece = pk_ if hid == "k" else pn_
        if hid != "k":   # tinh lại bằng đúng mảnh đầu phụ quanh chỗ đã dò
            ex2 = np.zeros(body.shape, bool)
            for h2, b2 in order:
                if h2 != hid:
                    cv2.circle(ex2.view(np.uint8), (int(b2[1]), int(b2[2])), int(pk_.width * b2[4] * 0.45), 1, -1)
            b0 = (b[0], b[1], b[2], b[3], b[4] * pk_.width / piece.width)
            b = refine(cl, piece, b0, ex2)
        score, cx, cy, ang, sc = b
        ax, ay = HL.ANCHOR[pname]
        M = cv2.getRotationMatrix2D((piece.width / 2, piece.height / 2), ang, sc)
        g = M @ np.array([ax * piece.width, ay * piece.height, 1.0])
        gx, gy = g[0] - piece.width / 2 + cx, g[1] - piece.height / 2 + cy   # gáy (điểm neo cổ) trên concept
        heads[hid] = dict(piece=pname, score=round(score, 1), cx=round(cx, 1), cy=round(cy, 1), ang=round(ang, 1), sc=round(sc, 4),
                          w_px=round(piece.width * sc, 1), gx=round(float(gx), 1), gy=round(float(gy), 1), w_piece=piece.width)
        print(f"đầu {hid} ({pname}): tâm ({cx:.0f}, {cy:.0f}) gáy ({gx:.0f}, {gy:.0f}) góc {ang:.0f}° tỉ lệ {sc:.2f} (rộng {piece.width * sc:.0f} px), tương quan {score:.3f}")
    # chỗ cổ mọc: cột thân (không nước) ở hai dải trên mặt nước (cao, thấp) -> vị trí chân cổ và hướng mọc
    def runs_at(dy0, dy1):
        band = body[int(y_water) - dy0:int(y_water) - dy1, :]
        cols = band.mean(axis=0) > 0.5
        runs, x = [], 0
        while x < len(cols):
            if cols[x]:
                x1 = x
                while x1 < len(cols) and cols[x1]:
                    x1 += 1
                if x1 - x > 25:
                    runs.append(((x + x1) / 2, x1 - x))
                x = x1
            else:
                x += 1
        return runs
    necks = runs_at(150, 90)
    low = runs_at(60, 15)
    print("chân thân dải cao 150-90 (x, rộng):", [(round(a), b) for a, b in necks])
    print("chân thân dải thấp 60-15 (x, rộng):", [(round(a), b) for a, b in low])
    # đổi sang tham số rig (hai_long.HEADS): 1 đơn vị rig = 1 px atlas (SC × px tờ); f = đơn vị rig / px concept, thủ lĩnh size 1
    hk = heads["k"]
    f = hk["w_piece"] * HL.SC / hk["w_px"]
    runs = [r for r in necks if r[1] >= 100]
    used = set()
    rig_heads = {}
    for hid, h in sorted(heads.items(), key=lambda kv: -kv[1]["w_px"]):   # thủ lĩnh chọn chân cổ trước
        size = round(h["w_px"] * f / (h["w_piece"] * HL.SC), 3)
        Hx, Hy = (h["gx"] - X0) * f, HL.CLIPY + (y_water - h["gy"]) * f
        ex, dirE = None, None
        cand = [r for r in runs if r[0] not in used and abs(r[0] - h["gx"]) < 420]
        if cand:
            r = min(cand, key=lambda r: abs(r[0] - h["gx"]))
            used.add(r[0])
            lo = [q for q in low if q[1] >= 60 and abs(q[0] - r[0]) < 140]
            xl = min(lo, key=lambda q: abs(q[0] - r[0]))[0] if lo else r[0]
            ex = (xl - X0) * f
            dirE = math.degrees(math.atan2(82.0, r[0] - xl))        # hướng cổ mọc: từ dải thấp (−37 px) lên dải cao (−120 px)
            dirE = max(55.0, min(125.0, dirE))
        if ex is None:
            ex = Hx * 0.5
            dirE = 90 + 0.6 * (math.degrees(math.atan2(Hy - HL.CLIPY, Hx - ex)) - 90)
        rig_heads[hid] = dict(size=size, H=[round(Hx, 1), round(Hy, 1)], psi=round(h["ang"], 1), ex=round(ex, 1), dirE=round(dirE, 1))
        print(f"  -> rig {hid}: size {size}, H ({Hx:.0f}, {Hy:.0f}), psi {h['ang']:.0f}, ex {ex:.0f}, dirE {dirE:.0f}")
    # cổ: dò hướng mọc, góc vào gáy, hai hệ số Bezier (ka, kb) cho dải cổ phủ đúng thân trên concept (điểm = trùng thân − rơi lên nền)
    fgm = (np.asarray(con.convert("RGB")).min(axis=2) < 236)
    Tc = lambda p: (p[0] / f + X0, y_water - (p[1] - HL.CLIPY) / f)
    for hid, rh in rig_heads.items():
        kind = "k" if hid == "k" else "n"
        nim = Image.open(os.path.join(manh, f"neck_{kind}.png")).convert("RGBA")
        nim = nim.crop(nim.getbbox())
        seg = nim.width * HL.SC / HL.NB * rh["size"]
        thick = int(round(nim.height * HL.SC * HL.NECK_THICK.get(kind, 1.0) * rh["size"] / f))
        E = (rh["ex"], HL.CLIPY - 14)
        best = None
        for dirE in np.arange(rh["dirE"] - 25, rh["dirE"] + 26, 5):
            for arr in range(20, 111, 10):
                for ka in (0.3, 0.4, 0.52, 0.65, 0.8):
                    for kb in (0.25, 0.35, 0.42, 0.55, 0.7):
                        J = HL.neck_joints(E, float(dirE), rh["H"], rh["psi"] + arr, seg, HL.NB, ka=ka, kb=kb)
                        pts = np.int32([Tc(p) for p in J if p[1] > HL.CLIPY - 6])
                        if len(pts) < 2:
                            continue
                        m = np.zeros(body.shape, np.uint8)
                        cv2.polylines(m, [pts.reshape(-1, 1, 2)], False, 1, thickness=max(4, thick))
                        m = m.astype(bool)
                        sc_ = int((m & body).sum()) - int((m & ~fgm).sum())
                        if best is None or sc_ > best[0]:
                            best = (sc_, float(dirE), arr, ka, kb)
        if best:
            rh.update(dirE=round(best[1], 1), arr=best[2], ka=best[3], kb=best[4])
            print(f"  -> cổ {hid}: dirE {best[1]:.0f}, arr {best[2]}, ka {best[3]}, kb {best[4]} (điểm {best[0]})")
    # VÒNG 2: đường tâm từng cổ trích từ mặt nạ concept (lần theo đỉnh biến đổi khoảng cách từ gáy xuống mặt nước) thay cho Bezier;
    # bề dày cổ đo trên mặt nạ; hàm dưới, vòng thân, đuôi dò như đầu
    dtm = cv2.distanceTransform(body.astype(np.uint8), cv2.DIST_L2, 5)
    heads_c = {hid: (h["cx"], h["cy"], h["w_px"]) for hid, h in heads.items()}
    for hid, rh in rig_heads.items():
        h = heads[hid]
        trace = trace_neck(dtm, body, (h["gx"], h["gy"]), (h["cx"], h["cy"]), y_water, [v for k2, v in heads_c.items() if k2 != hid])
        if trace is None or len(trace) < 3:
            print(f"  !! cổ {hid}: không lần được đường tâm, giữ Bezier")
            continue
        rest = [[round((x - X0) * f, 1), round(HL.CLIPY + (y_water - y) * f, 1)] for x, y in trace[::-1]]   # E -> gáy, hệ rig
        rest[0][1] = HL.CLIPY - 14.0
        rh["rest"] = rest
        rh["ex"] = rest[0][0]
        mid = trace[len(trace) // 4: 3 * len(trace) // 4]
        # bề dày = 2 × độ sâu lớn nhất quanh mỗi điểm đường tâm (đường tâm lệch tâm vài px thì dt tại điểm bị thấp)
        th_px = float(np.median([2 * dtm[max(0, int(y) - 30):int(y) + 31, max(0, int(x) - 30):int(x) + 31].max() for x, y in mid])) if len(mid) else 0
        rh["_trace"] = [[float(x), float(y)] for x, y in trace]
        rh["_th_px"] = th_px
        kind = "k" if hid == "k" else "n"
        nim = Image.open(os.path.join(manh, f"neck_{kind}.png")).convert("RGBA")
        nim = nim.crop(nim.getbbox())
        th_rig = nim.height * HL.SC * HL.NECK_THICK.get(kind, 1.0) * rh["size"]
        if th_px > 0:
            rh["thick"] = round(min(1.3, max(0.7, th_px * f / th_rig)), 3)
        print(f"  -> cổ {hid}: đường tâm {len(trace)} điểm, dày {th_px:.0f} px concept -> hệ số dày {rh.get('thick', 1.0)}, ex {rh['ex']}")
    # hàm dưới: dò mảnh hàm quanh nửa dưới đầu -> tỉ lệ (so với đầu) và bản lề (so với gáy, hệ xương đầu)
    jaws = {}
    for hid, h in heads.items():
        kind = "k" if hid == "k" else "n"
        jp = Image.open(os.path.join(manh, f"jaw_{kind}.png")).convert("RGBA")
        jp = jp.crop(jp.getbbox())
        hw_px = h["w_px"]
        win = np.zeros(body.shape, bool)
        x0, x1 = int(h["cx"] - 0.7 * hw_px), int(h["cx"] + 0.9 * hw_px)
        y0, y1 = int(h["cy"] - 0.2 * hw_px), int(h["cy"] + 0.8 * hw_px)
        win[max(0, y0):y1, max(0, x0):x1] = True
        sc0 = h["sc"]
        b = match_piece(cl, jp, np.arange(sc0 * 0.5, sc0 * 1.15, 0.06), np.arange(h["ang"] - 16, h["ang"] + 17, 8), ~win)
        if b is None:
            continue
        b = refine(cl, jp, b, ~win)
        score, cx, cy, ang, sc = b
        ax, ay = HL.ANCHOR[f"jaw_{kind}"]
        M = cv2.getRotationMatrix2D((jp.width / 2, jp.height / 2), ang, sc)
        g = M @ np.array([ax * jp.width, ay * jp.height, 1.0])
        hx, hy = g[0] - jp.width / 2 + cx, g[1] - jp.height / 2 + cy       # bản lề trên concept
        rh = rig_heads[hid]
        jaw_sc = round(sc * f / (HL.SC * rh["size"]), 3)
        dx, dy = (hx - h["gx"]) * f / rh["size"], -(hy - h["gy"]) * f / rh["size"]   # hệ rig, chưa xoay
        r = math.radians(-rh["psi"])
        lx, ly = dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)
        hw = h["w_piece"] * HL.SC
        jaws[kind] = dict(sc=jaw_sc, jaw=[round(lx / hw, 4), round(ly / hw, 4)], score=round(score, 3), cx=round(cx, 1), cy=round(cy, 1), ang=round(ang, 1))
        print(f"  -> hàm {hid} ({kind}): tâm ({cx:.0f}, {cy:.0f}) tỉ lệ {sc:.2f} (JAW_SC {jaw_sc}), bản lề/gáy ({lx / hw:.3f}, {ly / hw:.3f}) hw, điểm {score:.3f}")
    # vòng thân = chân thân còn lại (dải cao, rộng ≥ 100); đuôi = mép phải của thân trên mặt nước
    extra = dict()
    rest = [r for r in runs if r[0] not in used]
    if rest:
        c = max(rest, key=lambda r: r[1])
        extra["coil_x"] = round((c[0] - X0) * f, 1)
    ys_b, xs_b = np.nonzero(body[int(y_water) - 420:int(y_water), :])
    if len(xs_b):
        xr = float(np.percentile(xs_b, 99.5))
        extra["tail_x"] = round((xr - X0) * f - 150.0, 1)   # vây đuôi vẽ ra ~150 đơn vị bên phải gốc đuôi
    print("  -> vòng thân / đuôi:", extra)
    # vòng thân, đuôi: dò mảnh (loại vùng đầu)
    exh = np.zeros(body.shape, bool)
    for hid, (cx_, cy_, w_) in heads_c.items():
        cv2.circle(exh.view(np.uint8), (int(cx_), int(cy_)), int(w_ * 0.5), 1, -1)
    parts = {}
    for pname, angs in (("coil", np.arange(-16, 17, 8)), ("tail", np.arange(-10, 81, 10))):
        pth = os.path.join(manh, pname + ".png")
        if not os.path.exists(pth) or (pname == "coil" and k == 1):
            continue
        pim = Image.open(pth).convert("RGBA")
        pim = pim.crop(pim.getbbox())
        ex2 = exh.copy()                      # cửa sổ: vòng thân bên trái tâm nước, đuôi bên phải; cả hai sát mặt nước
        if pname == "coil":
            ex2[:, int(X0 - 40):] = True
        else:
            ex2[:, :int(X0 + 90)] = True
        ex2[:int(y_water - 420), :] = True
        for rh in rig_heads.values():   # không dò lên cổ đã lần
            if "_trace" in rh:
                pts = np.int32(rh["_trace"]).reshape(-1, 1, 2)
                cv2.polylines(ex2.view(np.uint8), [pts], False, 1, thickness=int(max(20, rh.get("_th_px", 60) * 0.9)))
        tmpl, dx_full = pim, 0.0
        if pname == "tail":   # concept chỉ lộ vây + mẩu gốc: dò bằng nửa phải (vây) rồi suy ra tâm cả mảnh
            cut = int(pim.width * 0.55)
            tmpl = pim.crop((cut, 0, pim.width, pim.height))
            dx_full = -(cut / 2)   # tâm cả mảnh so với tâm phần vây, theo trục mảnh (px tờ)
        b = match_piece(cl, tmpl, np.arange(0.3, 1.05, 0.1), angs, ex2)
        if b is None:
            continue
        b = refine(cl, tmpl, b, ex2)
        if dx_full:
            r_ = math.radians(b[3])
            b = (b[0], b[1] + math.cos(r_) * dx_full * b[4], b[2] - math.sin(r_) * dx_full * b[4], b[3], b[4])
        score, cx, cy, ang, sc = b
        parts[pname] = dict(cx=round(cx, 1), cy=round(cy, 1), ang=round(ang, 1), sc=round(sc, 4), score=round(score, 3),
                            X=round((cx - X0) * f, 1), Y=round(HL.CLIPY + (y_water - cy) * f, 1), w_piece=pim.width, h_piece=pim.height)
        print(f"  -> {pname}: tâm ({cx:.0f}, {cy:.0f}) góc {ang:.0f}° tỉ lệ {sc:.2f}, điểm {score:.3f}")
    for rh in rig_heads.values():
        rh.pop("_trace", None)
        rh["th_px"] = round(rh.pop("_th_px", 0), 1)
    res = dict(X0=round(X0, 1), y_water=round(y_water, 1), f=round(f, 5), heads=heads, necks=[[round(a, 1), b] for a, b in necks],
               rig_heads=rig_heads, extra=extra, jaws=jaws, parts=parts, concept=os.path.relpath(con_p, HERE))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(out, f"X0 {X0:.0f}, mặt nước y {y_water:.0f}")
    return res


# ---------------------------------------------------------------- IoU
def rig_mask_concept(k, J, kh, setup=False):
    """mặt nạ thân của rig ở khung 0 idle (+ aura 0) vẽ vào hệ concept; bỏ slot nước, bỏ phần dưới mặt nước (mặt nạ cắt).
    setup=True: dáng gốc (không animation) để tách lỗi cắt/lưới khỏi lệch do idle giây 0."""
    con = Image.open(paths(k)[1])
    W_, H_ = con.size
    bones = J["bones"]
    atts = J["skins"][0]["attachments"]
    anims = [] if setup else [("idle", 0.0)] + ([("aura", 0.0)] if "aura" in J["animations"] else [])
    Wb = S._pose_bones(J, anims, bones)
    X0, yw, f = kh["X0"], kh["y_water"], kh.get("f", 1.0)
    T = lambda p: (p[0] / f + X0, yw - (p[1] - HL.CLIPY) / f)
    # vẽ ĐỘ TRONG thật của ảnh mảnh qua từng tam giác (lưới là ô chữ nhật phủ cả vùng trong suốt: tô đa giác thì mặt nạ phình to)
    manh = paths(k)[2]
    BODYP = ("head_k", "jaw_k", "mouth", "head_n", "jaw_n", "whisker", "lid_k", "lid_n", "tongue_k", "tongue_n", "neck_k", "neck_n", "coil", "tail")
    alpha_cache = {}

    def alpha_of(path):
        if path not in alpha_cache:
            p = os.path.join(os.path.dirname(manh), "manh_lai", path + ".png") if path.startswith("lai_") else os.path.join(manh if path in BODYP else HL.MANH, path + ".png")
            im = Image.open(p).convert("RGBA")
            im = im.crop(im.getbbox())
            alpha_cache[path] = (np.asarray(im)[..., 3] > 100).astype(np.uint8) * 255
        return alpha_cache[path]

    acc = np.zeros((H_, W_), np.uint8)
    for s in J["slots"]:
        nm = s["name"]
        if nm.startswith(WATER_SLOTS) or not s.get("attachment") or S._slot_alpha(J, "idle", 0.0, s) < 0.05:
            continue
        for an, a in atts.get(nm, {}).items():
            path = a.get("path", an)
            try:
                al = alpha_of(path)
            except Exception:
                continue
            ah_, aw_ = al.shape
            if a.get("type") == "mesh":
                P, _ = S.mesh_world(a, bones, Wb)
                uv = a["uvs"]
                tr = a["triangles"]
                for i in range(0, len(tr), 3):
                    idx = (tr[i], tr[i + 1], tr[i + 2])
                    src = np.float32([[uv[2 * j] * aw_, uv[2 * j + 1] * ah_] for j in idx])
                    dst = np.float32([T(P[j]) for j in idx])
                    x0, y0 = dst.min(axis=0)
                    x1, y1 = dst.max(axis=0)
                    x0, y0, x1, y1 = int(max(0, x0)), int(max(0, y0)), int(min(W_, x1 + 1)), int(min(H_, y1 + 1))
                    if x1 <= x0 or y1 <= y0:
                        continue
                    M = cv2.getAffineTransform(src, dst - np.float32([x0, y0]))
                    w = cv2.warpAffine(al, M, (x1 - x0, y1 - y0), flags=cv2.INTER_NEAREST, borderValue=0)
                    tm = np.zeros((y1 - y0, x1 - x0), np.uint8)
                    cv2.fillConvexPoly(tm, np.int32(np.round(dst - np.float32([x0, y0]))), 255)
                    acc[y0:y1, x0:x1] |= (w & tm)
            elif a.get("type", "region") == "region":
                wx, wy, ma, mb, mc, md = Wb[s["bone"]]
                ax, ay, aw, ah = a.get("x", 0), a.get("y", 0), a["width"] * a.get("scaleX", 1), a["height"] * a.get("scaleY", 1)
                rr = math.radians(a.get("rotation", 0))
                cs, sn = math.cos(rr), math.sin(rr)
                dst = []
                for qx, qy in ((-aw / 2, ah / 2), (aw / 2, ah / 2), (aw / 2, -ah / 2)):
                    lx, ly = ax + qx * cs - qy * sn, ay + qx * sn + qy * cs
                    dst.append(T((ma * lx + mb * ly + wx, mc * lx + md * ly + wy)))
                src = np.float32([[0, 0], [aw_, 0], [aw_, ah_]])
                M = cv2.getAffineTransform(src, np.float32(dst))
                acc |= cv2.warpAffine(al, M, (W_, H_), flags=cv2.INTER_NEAREST, borderValue=0)
    m = acc > 0
    m[int(yw):, :] = False   # dưới mặt nước: mặt nạ cắt che
    return m


def iou(k):
    inbox, con_p, manh, kp = paths(k)
    kh = json.load(open(kp, encoding="utf-8"))
    name = f"tm10_{k}"
    J = json.load(open(os.path.join(inbox, "rig", name + ".json"), encoding="utf-8"))
    con = Image.open(con_p)
    body, water = concept_masks(con)
    body = body.copy()
    body[int(kh["y_water"]):, :] = False   # concept: phần thân dưới mặt nước cũng bỏ (đuôi, vòng thân lộ trên nước vẫn tính)
    rm = rig_mask_concept(k, J, kh)
    inter, uni = (rm & body).sum(), (rm | body).sum()
    v = inter / max(1, uni)
    rs = rig_mask_concept(k, J, kh, setup=True)
    v_setup = (rs & body).sum() / max(1, (rs | body).sum())
    print(f"IoU dáng gốc (không animation) = {v_setup:.3f}")
    # ảnh chồng: concept thân (xám), rig (xanh), giao (đậm)
    ov = np.full(body.shape + (3,), 236, np.uint8)
    ov[body] = (170, 170, 170)
    ov[rm] = (90, 160, 230)
    ov[rm & body] = (40, 90, 170)
    ov[water & ~rm] = (215, 225, 240)
    oi = Image.fromarray(ov)
    dr = ImageDraw.Draw(oi)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    except Exception:
        f = None
    dr.text((20, 16), f"IoU thân (bỏ nước, bỏ dưới mặt nước) = {v:.3f} khung 0 idle, {v_setup:.3f} dáng gốc (đích >= 0,9); xám = concept, xanh = rig, đậm = giao",
            fill=(20, 20, 20), font=f)
    p = os.path.join(inbox, "rig", "so_concept_iou.png")
    oi.save(p, optimize=True)
    kh["iou"] = round(float(v), 4)
    kh["iou_setup"] = round(float(v_setup), 4)
    json.dump(kh, open(kp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ghi lên so_concept.png nếu có
    sp = os.path.join(inbox, "rig", "so_concept.png")
    if os.path.exists(sp):
        si = Image.open(sp).convert("RGB")
        d2 = ImageDraw.Draw(si)
        d2.text((si.width // 2 - 160, si.height - 24), f"IoU thân khung 0 idle vs concept = {v:.3f} (nước loại khỏi phép đo)", fill=(150, 20, 20), font=f)
        si.save(sp, optimize=True)
    print(f"IoU = {v:.3f} -> {p}")
    return v


if __name__ == "__main__":
    cmd, k = sys.argv[1], int(sys.argv[2])
    if cmd == "khop":
        khop(k)
    elif cmd == "iou":
        iou(k)
