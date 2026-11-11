# -*- coding: utf-8 -*-
"""Lưới tam giác cho thư viện quai (đơn vị: pixel ảnh mảnh, y xuống; ảnh đã co về cỡ atlas nên đây cũng là pixel atlas).

- luoi_vung: tam giác gần đều cạnh phủ một hình alpha bất kỳ (kể cả lỗ, nhiều cụm). Viền lấy mẫu đều theo bước cạnh (thêm điểm
  chỗ viền cong cho sai lệch < tol px), điểm trong theo lưới tam giác đều (lục giác), làm mịn Laplace vài vòng, Delaunay rồi lọc
  tam giác ra ngoài hình, chèn trung điểm cạnh viền còn thiếu (Delaunay khớp viền). Đích mặc định: bước viền 11, bước trong 15.
- luoi_dai: dải lưới dọc một trục (cổ, đuôi, râu, lưỡi, chân): mỗi cột vuông góc trục, ≥ 3 cột mỗi đốt, ≥ 5 hàng nếu thân dày.
- luoi_o: lưới ô chữ nhật đều (lòng miệng 5×3...).
Mọi lưới in: số đỉnh, tam giác, góc nhỏ nhất, tỉ lệ tam giác dưới 25°, chỗ hở (pixel có hình mà không tam giác nào phủ).
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from . import anh

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import shapely
except ImportError:
    shapely = None


class Luoi:
    """pts (N, 2) toạ độ ảnh mảnh; tris (T, 3); nh: số đỉnh vòng ngoài đầu tiên (hull của Spine, các đỉnh này đứng đầu);
    nb: số đỉnh viền (mọi vòng, đứng trước đỉnh trong); w, h: cỡ ảnh; s: tham số dọc trục (luoi_dai) cho trọng số chuỗi."""

    def __init__(self, pts, tris, nh, nb, w, h, ten="", s=None):
        self.pts = np.asarray(pts, float)
        self.tris = np.asarray(tris, int).reshape(-1, 3)
        self.nh, self.nb, self.w, self.h, self.ten, self.s = int(nh), int(nb), int(w), int(h), ten, s
        self.truc = None     # luoi_dai: (điểm trục dày (K, 2), độ dài tích luỹ (K,))
        self.hang = None     # luoi_dai: (số cột, số hàng, chỉ số đỉnh theo lưới [cột][hàng])
        self.ho = 0          # số pixel có hình chưa được phủ

    @property
    def n(self):
        return len(self.pts)

    def canh(self):
        t = self.tris
        e = np.vstack([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]])
        e.sort(axis=1)
        return np.unique(e, axis=0)

    def ke(self):
        """danh sách kề [(đỉnh, độ dài cạnh)] cho từng đỉnh (đo khoảng cách đi trong hình)."""
        e = self.canh()
        L = np.hypot(*(self.pts[e[:, 0]] - self.pts[e[:, 1]]).T)
        adj = [[] for _ in range(self.n)]
        for (a, b), l in zip(e.tolist(), L.tolist()):
            adj[a].append((b, l))
            adj[b].append((a, l))
        return adj

    def goc(self):
        """ba góc của mỗi tam giác (độ), (T, 3)."""
        P = self.pts[self.tris]
        out = []
        for i in range(3):
            a, b, c = P[:, i], P[:, (i + 1) % 3], P[:, (i + 2) % 3]
            u, v = b - a, c - a
            cs = (u * v).sum(1) / np.maximum(1e-9, np.hypot(*u.T) * np.hypot(*v.T))
            out.append(np.degrees(np.arccos(np.clip(cs, -1, 1))))
        return np.stack(out, 1)

    def thong_ke(self):
        g = self.goc()
        gm = g.min(1) if len(g) else np.zeros(0)
        e = self.canh()
        L = np.hypot(*(self.pts[e[:, 0]] - self.pts[e[:, 1]]).T) if len(e) else np.zeros(1)
        return {"dinh": self.n, "tam_giac": len(self.tris), "goc_min": float(gm.min()) if len(gm) else 0.0,
                "duoi25": float((gm < 25).mean()) if len(gm) else 0.0, "goc_tb": float(gm.mean()) if len(gm) else 0.0,
                "canh_tb": float(L.mean()), "ho": int(self.ho)}

    def in_tk(self, ten=None):
        k = self.thong_ke()
        print(f"  lưới {ten or self.ten}: {k['dinh']} đỉnh, {k['tam_giac']} tam giác, góc nhỏ nhất {k['goc_min']:.1f}° "
              f"(TB góc nhỏ {k['goc_tb']:.1f}°, {100 * k['duoi25']:.1f}% dưới 25°), cạnh TB {k['canh_tb']:.1f} px, hở {k['ho']} px")
        return k

    def diem_truc(self, s):
        """điểm trên trục (luoi_dai) ở độ dài s (px ảnh) tính từ đầu trục."""
        D, cum = self.truc
        s = np.clip(np.asarray(s, float), 0, cum[-1])
        return np.stack([np.interp(s, cum, D[:, 0]), np.interp(s, cum, D[:, 1])], -1)

    def khop(self, so_dot, s0=0.0, s1=None):
        """so_dot + 1 khớp chia đều trục (luoi_dai) từ s0 tới s1 (mặc định hết trục): toạ độ ảnh."""
        s1 = self.truc[1][-1] if s1 is None else s1
        return self.diem_truc(np.linspace(s0, s1, so_dot + 1))


# ---------------------------------------------------------------- viền
def vong_bien(mask):
    """các vòng viền theo cạnh pixel của mặt nạ bool (toạ độ góc pixel, ảnh y xuống). Vòng ngoài có diện tích dương, lỗ âm."""
    m = np.pad(np.asarray(mask, bool), 1)
    H, W = m.shape
    S, E = [], []
    a, b = m[:-1, :], m[1:, :]
    ys, xs = np.nonzero(a & ~b)
    S.append(np.stack([xs + 1, ys + 1], 1)); E.append(np.stack([xs, ys + 1], 1))
    ys, xs = np.nonzero(~a & b)
    S.append(np.stack([xs, ys + 1], 1)); E.append(np.stack([xs + 1, ys + 1], 1))
    l, r = m[:, :-1], m[:, 1:]
    ys, xs = np.nonzero(l & ~r)
    S.append(np.stack([xs + 1, ys], 1)); E.append(np.stack([xs + 1, ys + 1], 1))
    ys, xs = np.nonzero(~l & r)
    S.append(np.stack([xs + 1, ys + 1], 1)); E.append(np.stack([xs + 1, ys], 1))
    S, E = np.vstack(S), np.vstack(E)
    if not len(S):
        return []
    Wc = W + 1
    sk = (S[:, 1] * Wc + S[:, 0]).tolist()
    ek = (E[:, 1] * Wc + E[:, 0]).tolist()
    Sx, Sy, Ex, Ey = S[:, 0].tolist(), S[:, 1].tolist(), E[:, 0].tolist(), E[:, 1].tolist()
    out = {}
    for i, k in enumerate(sk):
        out.setdefault(k, []).append(i)
    used = bytearray(len(sk))
    order = [i for i in range(len(sk)) if len(out[sk[i]]) == 1] + [i for i in range(len(sk)) if len(out[sk[i]]) > 1]
    loops = []
    for i0 in order:
        if used[i0]:
            continue
        pts, i = [], i0
        while not used[i]:
            used[i] = 1
            pts.append((Sx[i], Sy[i]))
            nxt = [j for j in out.get(ek[i], ()) if not used[j]]
            if not nxt:
                break
            if len(nxt) > 1:  # chỗ hai pixel chéo nhau: rẽ phải (bám sát phần trong)
                rx, ry = -(Ey[i] - Sy[i]), Ex[i] - Sx[i]
                i = next((j for j in nxt if (Ex[j] - Sx[j], Ey[j] - Sy[j]) == (rx, ry)), nxt[0])
            else:
                i = nxt[0]
        if len(pts) >= 4:
            loops.append(np.array(pts, float) - 1.0)
    return loops


def dien_tich(L):
    x, y = L[:, 0], L[:, 1]
    return 0.5 * float((x * np.roll(y, -1) - np.roll(x, -1) * y).sum())


def lam_muot(L, lan=2):
    for _ in range(lan):
        L = (np.roll(L, 1, 0) + L + np.roll(L, -1, 0)) / 3.0
    return L


def lay_mau(L, h, tol=1.0):
    """lấy mẫu vòng kín L cách đều bước h, thêm điểm ở đoạn mà dây cung lệch khỏi viền quá tol px."""
    C = np.vstack([L, L[:1]])
    seg = np.hypot(*np.diff(C, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    P = float(cum[-1])
    n = max(4, int(round(P / h)))
    cumE = np.concatenate([cum[:-1], cum[:-1] + P])
    CE = np.vstack([C[:-1], C[:-1]])

    def at(s):
        s = np.asarray(s, float) % P
        return np.stack([np.interp(s, cum, C[:, 0]), np.interp(s, cum, C[:, 1])], -1)

    def refine(a, b, depth=0):
        idx = np.flatnonzero((cumE > a + 1e-6) & (cumE < b - 1e-6))
        if not len(idx) or depth > 12:
            return [a]
        pa, pb = at(a), at(b)
        q = CE[idx]
        d = pb - pa
        ll = max(1e-9, float(d @ d))
        t = np.clip(((q - pa) @ d) / ll, 0, 1)
        dist = np.hypot(*(q - (pa + t[:, None] * d)).T)
        k = int(dist.argmax())
        if dist[k] <= tol:
            return [a]
        s = float(cumE[idx[k]])
        return refine(a, s, depth + 1) + refine(s, b, depth + 1)

    ss = np.linspace(0, P, n, endpoint=False)
    params = []
    for k in range(n):
        params += refine(ss[k], ss[k + 1] if k + 1 < n else ss[0] + P)
    # điểm đều nằm sát điểm góc vừa thêm (chóp sừng, răng, đáy khe) thì bỏ: đoạn viền quá ngắn sinh tam giác dẹt
    base = set(np.round(ss, 6).tolist())
    params = sorted(p % P for p in params)
    corner = [p for p in params if round(p, 6) not in base]
    if corner:
        cs = np.array(corner)
        keep = []
        for p in params:
            if round(p, 6) in base:
                dd = np.abs(cs - p)
                dd = np.minimum(dd, P - dd)
                if dd.min() < 0.4 * h:
                    continue
            keep.append(p)
        params = keep
    return at(np.array(params))


def _trong(Q, polys):
    """điểm nằm trong tập vòng (chẵn lẻ: lỗ tự trừ)."""
    Q = np.asarray(Q, float)
    inside = np.zeros(len(Q), bool)
    for L in polys:
        x0, y0 = L[:, 0], L[:, 1]
        x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
        for c in range(0, len(Q), 2048):
            px, py = Q[c:c + 2048, 0:1], Q[c:c + 2048, 1:2]
            cond = (y0 > py) != (y1 > py)
            xi = (x1 - x0) * (py - y0) / np.where(np.abs(y1 - y0) < 1e-12, 1e-12, y1 - y0) + x0
            inside[c:c + 2048] ^= ((cond & (px < xi)).sum(1) % 2 == 1)
    return inside


def _kc_bien(Q, polys):
    """khoảng cách nhỏ nhất từ điểm tới các cạnh viền."""
    Q = np.asarray(Q, float)
    best = np.full(len(Q), np.inf)
    for L in polys:
        A, B = L, np.roll(L, -1, 0)
        d = B - A
        ll = np.maximum(1e-12, (d * d).sum(1))
        for c in range(0, len(Q), 1024):
            q = Q[c:c + 1024, None, :]
            t = np.clip(((q - A) * d).sum(2) / ll, 0, 1)
            pr = A + t[..., None] * d
            best[c:c + 1024] = np.minimum(best[c:c + 1024], np.hypot(*(q - pr).transpose(2, 0, 1)).min(1))
    return best


# ---------------------------------------------------------------- Delaunay
def _q(P):
    return np.round(np.asarray(P, float) * 16) / 16


def delaunay(P):
    """tam giác Delaunay của tập điểm (cv2 nếu có, không thì shapely, không nữa thì Bowyer-Watson thuần Python)."""
    P = _q(P)
    key = {(float(x), float(y)): i for i, (x, y) in enumerate(P.tolist())}
    if cv2 is not None:
        x0, y0 = P.min(0) - 8
        x1, y1 = P.max(0) + 8
        sub = cv2.Subdiv2D((int(math.floor(x0)), int(math.floor(y0)), int(x1 - x0) + 4, int(y1 - y0) + 4))
        for x, y in P.tolist():
            sub.insert((x, y))
        out = []
        for t in sub.getTriangleList():
            ids = [key.get((float(t[2 * k]), float(t[2 * k + 1]))) for k in range(3)]
            if None not in ids:
                out.append(ids)
        return np.array(out, int).reshape(-1, 3)
    if shapely is not None:
        g = shapely.delaunay_triangles(shapely.MultiPoint(P))
        C = shapely.get_coordinates(g).reshape(-1, 4, 2)[:, :3]
        out = []
        for tri in C.tolist():
            ids = [key.get((float(a), float(b))) for a, b in tri]
            if None not in ids:
                out.append(ids)
        return np.array(out, int).reshape(-1, 3)
    return _bowyer_watson(P)


def _bowyer_watson(P):
    n = len(P)
    lo, hi = P.min(0), P.max(0)
    c, s = (lo + hi) / 2, float((hi - lo).max()) * 20 + 10
    pts = np.vstack([P, [[c[0] - s, c[1] - s], [c[0] + s, c[1] - s], [c[0], c[1] + s]]])

    def cc(a, b, d):
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = pts[d]
        D = 2 * (ax * (by - dy) + bx * (dy - ay) + dx * (ay - by))
        if abs(D) < 1e-12:
            return (0, 0, -1)
        ux = ((ax * ax + ay * ay) * (by - dy) + (bx * bx + by * by) * (dy - ay) + (dx * dx + dy * dy) * (ay - by)) / D
        uy = ((ax * ax + ay * ay) * (dx - bx) + (bx * bx + by * by) * (ax - dx) + (dx * dx + dy * dy) * (bx - ax)) / D
        return (ux, uy, (ax - ux) ** 2 + (ay - uy) ** 2)

    tris = [(n, n + 1, n + 2) + cc(n, n + 1, n + 2)]
    for i in range(n):
        x, y = pts[i]
        bad = [t for t in tris if (x - t[3]) ** 2 + (y - t[4]) ** 2 < t[5]]
        cnt = {}
        for t in bad:
            for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                k = tuple(sorted(e))
                cnt[k] = cnt.get(k, 0) + 1
        bs = set(bad)
        tris = [t for t in tris if t not in bs]
        for (a, b), v in cnt.items():
            if v == 1:
                tris.append((a, b, i) + cc(a, b, i))
    return np.array([t[:3] for t in tris if max(t[:3]) < n], int).reshape(-1, 3)


def _tg_trong(P, polys):
    T = delaunay(P)
    if not len(T):
        return T
    cen = P[T].mean(1)
    return T[_trong(cen, polys)]


def _bo_det(P, T, nb=0, eps=0.02, goc=1.0):
    """bỏ tam giác diện tích ~0 và tam giác 'tai' cả ba đỉnh trên viền mà góc < goc độ (điểm viền gần thẳng hàng sau khi chèn trung
    điểm): hình phủ chỉ hụt vài phần px² nằm trong lề nới viền, bỏ được góc 0°."""
    if not len(T):
        return T
    A = P[T]
    u, v = A[:, 1] - A[:, 0], A[:, 2] - A[:, 0]
    keep = np.abs(u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]) > 2 * eps
    if nb:
        L = Luoi(P, T, 0, 0, 1, 1)
        keep &= ~((T < nb).all(1) & (L.goc().min(1) < goc))
    return T[keep]


def _relax(P, T, nb, polys, dmin, w=0.55):
    n = len(P)
    if not len(T):
        return P
    e = np.vstack([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]])
    S = np.zeros((n, 2))
    C = np.zeros(n)
    np.add.at(S, e[:, 0], P[e[:, 1]])
    np.add.at(S, e[:, 1], P[e[:, 0]])
    np.add.at(C, e[:, 0], 1)
    np.add.at(C, e[:, 1], 1)
    idx = np.arange(nb, n)
    idx = idx[C[idx] > 0]
    if not len(idx):
        return P
    newp = P[idx] + w * (S[idx] / C[idx, None] - P[idx])
    ok = _trong(newp, polys) & (_kc_bien(newp, polys) >= dmin)
    P = P.copy()
    P[idx[ok]] = newp[ok]
    return P


def _phu(alpha, pts, tris):
    """số pixel có hình (alpha) mà không tam giác nào phủ."""
    H, W = alpha.shape
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    for t in tris:
        d.polygon([tuple(p) for p in pts[t].tolist()], fill=255, outline=255)
    return int((alpha & (np.asarray(im) < 128)).sum())


def _alpha(src, nguong=8):
    if isinstance(src, Image.Image):
        a = np.asarray(src.convert("RGBA"))[..., 3]
        return a > nguong, a > 40
    a = np.asarray(src, bool)
    return a, a


def luoi_vung(src, buoc_vien=11.0, buoc_trong=15.0, vien=2, lap=4, tol=1.0, lo_min=None, ten="", in_tk=True, buoc_theo_cao=None):
    """lưới tam giác gần đều phủ hình (ảnh PIL RGBA hoặc mặt nạ bool). vien: nới viền ra ngoài hình (px) để lưới phủ hết nét mực
    mép; lo_min: lỗ nhỏ hơn số px này thì lấp (mặc định (0,8·bước trong)²: khe nhỏ hơn một ô không lưới được, độ trong của ảnh
    vẫn giữ khe); lap: số vòng làm mịn điểm trong. buoc_theo_cao=H (chiều cao con, px atlas): bước viền 1,5% H, bước trong 2% H
    (đè buoc_vien, buoc_trong)."""
    if buoc_theo_cao:
        buoc_vien, buoc_trong = 0.015 * buoc_theo_cao, 0.02 * buoc_theo_cao
    a, a_hard = _alpha(src)
    H, W = a.shape
    m = anh.gian(a, vien, tron=True) if vien else a.copy()
    m = anh.lap_lo(m, (0.8 * buoc_trong) ** 2 if lo_min is None else lo_min)
    loops = [L for L in vong_bien(m) if abs(dien_tich(L)) > 12]
    loops.sort(key=lambda L: -dien_tich(L))  # vòng ngoài lớn nhất trước, lỗ (âm) sau
    B = [lay_mau(lam_muot(L), buoc_vien, tol) for L in loops]
    # điểm trong: lưới tam giác đều
    x0, y0 = np.min([b.min(0) for b in B], 0)
    x1, y1 = np.max([b.max(0) for b in B], 0)
    dy = buoc_trong * math.sqrt(3) / 2
    ys = np.arange(y0 + 0.37 * dy, y1, dy)
    cand = []
    for r, y in enumerate(ys):
        xs = np.arange(x0 + 0.21 * buoc_trong + (r % 2) * buoc_trong / 2, x1, buoc_trong)
        cand.append(np.stack([xs, np.full(len(xs), y)], 1))
    I = np.vstack(cand) if cand else np.zeros((0, 2))
    dmin = max(0.6 * buoc_trong, 0.75 * buoc_vien)
    if len(I):
        I = I[_trong(I, B)]
        if len(I):
            I = I[_kc_bien(I, B) >= dmin]
    for _ in range(lap):
        nb = sum(len(b) for b in B)
        P = np.vstack(B + [I])
        T = _tg_trong(P, B)
        P = _relax(P, T, nb, B, 0.5 * buoc_vien)
        I = P[nb:]
    # Delaunay khớp viền: cạnh viền nào chưa là cạnh tam giác thì chèn trung điểm của nó vào viền
    for _ in range(12):
        nb = sum(len(b) for b in B)
        P = np.vstack(B + [I])
        T = _tg_trong(P, B)
        es = set()
        for t in T.tolist():
            for i in range(3):
                u, v = t[i], t[(i + 1) % 3]
                es.add((u, v) if u < v else (v, u))
        miss, off = False, 0
        newB = []
        for b in B:
            n_ = len(b)
            out = []
            for i in range(n_):
                u, v = off + i, off + (i + 1) % n_
                out.append(b[i])
                if ((u, v) if u < v else (v, u)) not in es:
                    out.append((b[i] + b[(i + 1) % n_]) / 2)
                    miss = True
            newB.append(np.array(out))
            off += n_
        if not miss:
            break
        B = newB
        if len(I):  # điểm trong sát điểm viền mới chèn thì bỏ (tránh tam giác dẹt)
            I = I[_kc_bien(I, B) >= 0.45 * buoc_vien]
    T = _bo_det(P, T, nb)
    # gọn: bỏ điểm không thuộc tam giác nào, viền đứng trước
    used = np.zeros(len(P), bool)
    used[T.ravel()] = True
    nb_raw = nb
    keep = np.flatnonzero(used)
    remap = -np.ones(len(P), int)
    remap[keep] = np.arange(len(keep))
    pts, tris = P[keep], remap[T]
    nb2 = int(used[:nb_raw].sum())
    nh = int(used[:len(B[0])].sum()) if B else 0
    L = Luoi(pts, tris, nh, nb2, W, H, ten)
    L.ho = _phu(a_hard, pts, tris)
    if in_tk:
        L.in_tk()
    return L


# ---------------------------------------------------------------- dải lưới
def _truc_ngang(m):
    cols = np.flatnonzero(m.any(axis=0))
    rows = np.flatnonzero(m.any(axis=1))
    ymid = float(np.median([np.mean(np.flatnonzero(m[:, x])) for x in cols[::max(1, len(cols) // 40)]]))
    return np.array([[cols[0], ymid], [cols[-1] + 1.0, ymid]]), rows


def _day(poly, step=1.0):
    poly = np.asarray(poly, float)
    seg = np.hypot(*np.diff(poly, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = np.linspace(0, cum[-1], max(2, int(cum[-1] / step) + 1))
    D = np.stack([np.interp(s, cum, poly[:, 0]), np.interp(s, cum, poly[:, 1])], 1)
    return D, s


def _lay_mau_mo(A, h, tol=1.0):
    """lấy mẫu đường hở A (giữ hai đầu) cách đều bước h, thêm điểm chỗ dây cung lệch viền quá tol px."""
    seg = np.hypot(*np.diff(A, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    if cum[-1] < 1e-6:
        return A[:1].copy()
    at = lambda s: np.stack([np.interp(s, cum, A[:, 0]), np.interp(s, cum, A[:, 1])], -1)  # noqa: E731

    def refine(a, b, depth=0):
        idx = np.flatnonzero((cum > a + 1e-6) & (cum < b - 1e-6))
        if not len(idx) or depth > 10:
            return [a]
        pa, pb = at(a), at(b)
        d = pb - pa
        ll = max(1e-9, float(d @ d))
        q = A[idx]
        t = np.clip(((q - pa) @ d) / ll, 0, 1)
        dist = np.hypot(*(q - (pa + t[:, None] * d)).T)
        k = int(dist.argmax())
        if dist[k] <= tol:
            return [a]
        sm = float(cum[idx[k]])
        return refine(a, sm, depth + 1) + refine(sm, b, depth + 1)

    n = max(1, int(round(cum[-1] / h)))
    ss = np.linspace(0, cum[-1], n + 1)
    params = []
    for k in range(n):
        params += refine(ss[k], ss[k + 1])
    params.append(float(cum[-1]))
    return at(np.array(params))


def _mu(m, Gc, p_c, t_c, dau, buoc_vien, buoc_trong, tol=1.0, lap=4):
    """mũ tròn một đầu dải: phần hình (mặt nạ m) lòi qua cột mút Gc (R đỉnh, trên → dưới), phía -t_c nếu dau, +t_c nếu không.
    Lưới vùng đều có R đỉnh đầu ĐÚNG là Gc (dùng chung với dải; cạnh cột mút giữ nguyên, không chèn điểm lên đó). Trả (P, T) hoặc
    None nếu hình không lòi qua cột."""
    loops = [L for L in vong_bien(m) if dien_tich(L) > 12]
    if not loops:
        return None
    Lo = lam_muot(max(loops, key=dien_tich))
    sgn = -1.0 if dau else 1.0
    sd = ((Lo - p_c) @ t_c) * sgn
    segs = np.hypot(*np.diff(Gc, axis=0).T)
    margin = max(0.5 * buoc_vien, 0.6 * float(segs.max()))
    beyond = sd > margin
    if not beyond.any() or beyond.all():
        return None
    n = len(Lo)
    st = int(np.flatnonzero(~beyond)[0])
    runs, cur = [], []
    for i in ((np.arange(n) + st) % n).tolist():
        if beyond[i]:
            cur.append(i)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    run = min(runs, key=lambda r: float(np.hypot(*(Lo[r] - p_c).T).min()))
    if len(run) < 3:
        return None
    arc = _lay_mau_mo(Lo[run], buoc_vien, tol)
    if np.hypot(*(arc[0] - Gc[-1])) > np.hypot(*(arc[-1] - Gc[-1])):
        arc = arc[::-1]
    R = len(Gc)
    fixed_c = (Gc[:-1] + Gc[1:]) / 2
    fixed_r = segs / 2 * 1.08
    dmin = max(0.6 * buoc_trong, 0.75 * buoc_vien)

    def ok_pts(Q, B):
        if not len(Q):
            return np.zeros(0, bool)
        good = _trong(Q, [B]) & (_kc_bien(Q, [B]) >= 0.5 * buoc_vien)
        for c, r in zip(fixed_c, fixed_r):
            good &= np.hypot(*(Q - c).T) > r
        return good

    B = np.vstack([Gc, arc])
    x0, y0 = B.min(0)
    x1, y1 = B.max(0)
    dy = buoc_trong * math.sqrt(3) / 2
    cand = []
    for r, y in enumerate(np.arange(y0 + 0.37 * dy, y1, dy)):
        xs = np.arange(x0 + 0.21 * buoc_trong + (r % 2) * buoc_trong / 2, x1, buoc_trong)
        cand.append(np.stack([xs, np.full(len(xs), y)], 1))
    I = np.vstack(cand) if cand else np.zeros((0, 2))
    if len(I):
        I = I[ok_pts(I, B) & (_kc_bien(I, [B]) >= dmin)]
    for _ in range(lap):
        if not len(I):
            break
        B = np.vstack([Gc, arc])
        P = np.vstack([B, I])
        T = _tg_trong(P, [B])
        newI = _relax(P, T, len(B), [B], 0.5 * buoc_vien)[len(B):]
        I = np.where(ok_pts(newI, B)[:, None], newI, I)
    for _ in range(12):
        B = np.vstack([Gc, arc])
        P = np.vstack([B, I]) if len(I) else B
        T = _tg_trong(P, [B])
        es = set()
        for t in T.tolist():
            for i in range(3):
                u, v = t[i], t[(i + 1) % 3]
                es.add((u, v) if u < v else (v, u))
        miss_fixed = [i for i in range(R - 1) if (i, i + 1) not in es]
        new_arc, miss = [], False
        if (R - 1, R) not in es:
            new_arc.append((Gc[-1] + arc[0]) / 2)
            miss = True
        for j in range(len(arc)):   # đỉnh vòng: R + j; cạnh (R+j, R+j+1) và cạnh khép (cuối, 0)
            new_arc.append(arc[j])
            u = R + j
            v = R + j + 1 if j + 1 < len(arc) else 0
            if ((u, v) if u < v else (v, u)) not in es:
                new_arc.append((arc[j] + (arc[j + 1] if j + 1 < len(arc) else Gc[0])) / 2)
                miss = True
        if miss_fixed and len(I):   # cạnh cột mút thiếu: bỏ điểm trong đứng trong đường tròn đường kính của nó
            for i in miss_fixed:
                I = I[np.hypot(*(I - fixed_c[i]).T) > fixed_r[i] * 1.6] if len(I) else I
        if not miss and not miss_fixed:
            break
        if miss:
            arc = np.array(new_arc)
            if len(I):
                I = I[_kc_bien(I, [np.vstack([Gc, arc])]) >= 0.45 * buoc_vien]
    T = _bo_det(P, T, len(Gc) + len(arc))
    used = np.zeros(len(P), bool)
    used[T.ravel()] = True
    used[:R] = True
    keep = np.flatnonzero(used)
    remap = -np.ones(len(P), int)
    remap[keep] = np.arange(len(keep))
    return P[keep], remap[T]


def _sap_vien(pts, tris):
    """xếp lại đỉnh: vòng viền dài nhất trước (hull của Spine), các vòng viền khác, rồi đỉnh trong. Trả (perm, nh, nb) với
    perm[mới] = cũ."""
    e = np.sort(np.vstack([tris[:, [0, 1]], tris[:, [1, 2]], tris[:, [2, 0]]]), 1)
    uq, cnt = np.unique(e, axis=0, return_counts=True)
    adj = {}
    for a, b in uq[cnt == 1].tolist():
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    for v0 in adj:
        if v0 in seen:
            continue
        loop, prev, v = [v0], None, v0
        seen.add(v0)
        while True:
            nx = [u for u in adj[v] if u != prev and u not in seen]
            if not nx:
                break
            prev, v = v, nx[0]
            seen.add(v)
            loop.append(v)
        loops.append(loop)
    loops.sort(key=len, reverse=True)
    order = [v for lp in loops for v in lp]
    rest = [v for v in range(len(pts)) if v not in seen]
    return np.array(order + rest, int), (len(loops[0]) if loops else 0), len(order)


def _minang(P):
    g = []
    for i in range(3):
        u, v = P[(i + 1) % 3] - P[i], P[(i + 2) % 3] - P[i]
        g.append(math.degrees(math.acos(max(-1, min(1, float(u @ v) / max(1e-9, math.hypot(*u) * math.hypot(*v)))))))
    return min(g)


def _dai_co_mu(G, sc, D, cumD, tg, m, a_hard, mus, buoc_vien, buoc_trong, W, H, ten, so_dot, in_tk):
    """ghép dải lưới G (C × R) với mũ tròn ở đầu (mus = (gốc, ngọn)); đỉnh mũ có s theo vị trí chiếu lên trục."""
    C, R = G.shape[:2]
    Ltot = float(cumD[-1])
    Pg = G.reshape(-1, 2)
    pts = [tuple(p) for p in Pg.tolist()]
    svals = [float(sc[c]) for c in range(C) for _ in range(R)]
    gid = lambda c, r: c * R + r  # noqa: E731
    tris = []
    for c in range(C - 1):
        for r in range(R - 1):
            a0, b0, c0, d0 = gid(c, r), gid(c + 1, r), gid(c + 1, r + 1), gid(c, r + 1)
            t1 = [(a0, b0, c0), (a0, c0, d0)]
            t2 = [(a0, b0, d0), (b0, c0, d0)]
            tris += t1 if min(_minang(Pg[list(t)]) for t in t1) >= min(_minang(Pg[list(t)]) for t in t2) else t2
    for on, ce, dau in ((mus[0], 0, True), (mus[1], C - 1, False)):
        if not on:
            continue
        p_c = np.array([np.interp(sc[ce], cumD, D[:, 0]), np.interp(sc[ce], cumD, D[:, 1])])
        t_c = np.array([np.interp(sc[ce], cumD, tg[:, 0]), np.interp(sc[ce], cumD, tg[:, 1])])
        t_c /= max(1e-9, float(np.hypot(*t_c)))
        res = _mu(m, G[ce], p_c, t_c, dau, buoc_vien, buoc_trong)
        if res is None:
            continue
        Pc, Tc = res
        mp = {i: gid(ce, i) for i in range(R)}
        for i in range(R, len(Pc)):
            mp[i] = len(pts)
            pts.append(tuple(Pc[i]))
            svals.append(float(np.clip(sc[ce] + (Pc[i] - p_c) @ t_c, 0, Ltot)))
        tris += [(mp[a], mp[b], mp[c]) for a, b, c in Tc.tolist()]
    pts = np.array(pts, float)
    tris = np.array(tris, int)
    perm, nh, nb = _sap_vien(pts, tris)
    inv = np.empty(len(perm), int)
    inv[perm] = np.arange(len(perm))
    L = Luoi(pts[perm], inv[tris], nh, nb, W, H, ten, s=np.array(svals)[perm])
    L.truc = (D, cumD)
    L.hang = (C, R, inv[np.arange(C * R).reshape(C, R)])
    L.ho = _phu(a_hard, L.pts, L.tris)
    if in_tk:
        L.in_tk(f"{ten} (dải {C} cột × {R} hàng + mũ, {so_dot} đốt)")
    return L


def luoi_dai(src, so_dot, cot_moi_dot=3, hang=None, truc=None, vien=2, buoc=14.0, buoc_ngang=None, ten="", in_tk=True, mu=False,
             buoc_theo_cao=None):
    """dải lưới dọc trục (cổ, đuôi, râu, lưỡi, chân). truc: đường giữa [(x, y)...] toạ độ ảnh từ gốc tới ngọn (mặc định: đường
    ngang qua giữa hình, từ mép trái tới mép phải: GPT vẽ duỗi thẳng nằm ngang, gốc bên trái). Số cột = max(cot_moi_dot·số đốt + 1,
    dài / buoc + 1), mỗi cột vuông góc trục, hai đầu cột bám mép hình (lấy mép xa nhất trong khoảng giữa hai cột nên không hở).
    Số hàng = hang hoặc theo bề dày (buoc_ngang, mặc định = buoc), ít nhất 3, ít nhất 5 khi thân dày hơn 4 bước.
    Trả Luoi có .s (độ dài dọc trục của từng đỉnh) và .truc, .khop(n) để đặt xương.
    mu: mũ tròn ở đầu dải (True hoặc "hai": cả hai đầu; "dau": chỉ gốc; "ngon": chỉ ngọn): cột mút lùi vào cỡ nửa bề dày, chỏm tròn
    lòi qua cột mút được phủ bằng lưới vùng đều dùng chung đỉnh với cột mút (không hở, không tam giác dẹt ở chỏm); đỉnh mũ có .s
    theo vị trí chiếu lên trục nên trọng số chuoi() tự theo đốt mút. Có mu thì số hàng tăng cho ô gần vuông.
    buoc_theo_cao=H (chiều cao con, px atlas): bước dọc và ngang 2% H, bước viền mũ 1,5% H (đè buoc, buoc_ngang)."""
    a, a_hard = _alpha(src)
    H, W = a.shape
    m = anh.gian(a, vien) if vien else a.copy()
    buoc_vien_mu = 0.75 * buoc
    if buoc_theo_cao:
        buoc, buoc_ngang, buoc_vien_mu = 0.02 * buoc_theo_cao, 0.02 * buoc_theo_cao, 0.015 * buoc_theo_cao
    buoc_ngang = buoc_ngang or buoc
    mu_dau, mu_ngon = mu in (True, "hai", "dau"), mu in (True, "hai", "ngon")
    straight = truc is None
    if straight:
        truc, _ = _truc_ngang(m)
    D, cumD = _day(truc, 0.5)
    Ltot = float(cumD[-1])
    tg = np.gradient(D, axis=0)
    tg /= np.maximum(1e-9, np.hypot(*tg.T))[:, None]
    nrm = np.stack([-tg[:, 1], tg[:, 0]], 1)   # ảnh y xuống: trục sang phải thì pháp tuyến chĩa xuống
    maxd = float(np.hypot(W, H))
    s0, s1 = 0.0, Ltot
    if mu_dau or mu_ngon:   # cột mút lùi vào cỡ nửa bề dày gần đầu đó (chỏm tròn bán kính bằng nửa bề dày)
        def day_o(s):
            p = np.array([np.interp(s, cumD, D[:, 0]), np.interp(s, cumD, D[:, 1])])
            nv = np.array([np.interp(s, cumD, nrm[:, 0]), np.interp(s, cumD, nrm[:, 1])])
            tot = 0.0
            for sg in (-1, 1):
                r_ = np.arange(0, maxd, 0.5)
                q = p + sg * r_[:, None] * nv
                x, y = q[:, 0].astype(int), q[:, 1].astype(int)
                ok = (x >= 0) & (y >= 0) & (x < W) & (y < H)
                ins = np.zeros(len(r_), bool)
                ins[ok] = m[y[ok], x[ok]]
                out = np.flatnonzero(~ins)
                tot += r_[out[0]] if len(out) else r_[-1]
            return tot
        if mu_dau:
            s0 = min(0.4 * Ltot, max(0.5 * buoc, 0.5 * max(day_o(s) for s in np.linspace(0, 0.35 * Ltot, 8))))
        if mu_ngon:
            s1 = Ltot - min(0.4 * Ltot, max(0.5 * buoc, 0.5 * max(day_o(s) for s in np.linspace(0.65 * Ltot, Ltot, 8))))
    C = max(cot_moi_dot * so_dot + 1, int(math.ceil((s1 - s0) / buoc)) + 1)
    sc = np.linspace(s0, s1, C)
    ds = (s1 - s0) / (C - 1)

    def at(arr, s):
        return np.stack([np.interp(s, cumD, arr[:, 0]), np.interp(s, cumD, arr[:, 1])], -1)

    def reach(p, d):
        """khoảng xa nhất còn trong hình đi từ p theo hướng d (cho phép khe ngắn < 4 px)."""
        r = np.arange(0, maxd, 0.5)
        q = p + r[:, None] * d
        x, y = q[:, 0].astype(int), q[:, 1].astype(int)
        ok = (x >= 0) & (y >= 0) & (x < W) & (y < H)
        ins = np.zeros(len(r), bool)
        ins[ok] = m[y[ok], x[ok]]
        last, gap = 0.0, 0
        for k in range(len(r)):
            if ins[k]:
                last, gap = r[k], 0
            else:
                gap += 1
                if gap > 8 and r[k] > 2:
                    break
        return last

    tops, bots = np.zeros(C), np.zeros(C)
    for c in range(C):
        subs = np.clip(sc[c] + np.linspace(-0.6, 0.6, 7) * ds, s0, s1)
        if straight:
            x0, x1 = int(max(0, at(D, subs[0])[0])), int(min(W, at(D, subs[-1])[0] + 1))
            rows = np.flatnonzero(m[:, x0:max(x1, x0 + 1)].any(axis=1))
            yc = float(D[0, 1])
            tops[c] = max(1.5, yc - rows[0]) if len(rows) else 1.5
            bots[c] = max(1.5, rows[-1] + 1 - yc) if len(rows) else 1.5
        else:
            tt, bb = 1.5, 1.5
            for s in subs:
                p, nv = at(D, s), at(nrm, s)
                tt = max(tt, reach(p, -nv))
                bb = max(bb, reach(p, nv))
            tops[c], bots[c] = tt, bb
    thick = float((tops + bots).max())
    R = hang or max(3, int(round(thick / buoc_ngang)) + 1)
    if hang is None and thick > 4 * buoc_ngang:
        R = max(R, 5)
    if hang is None and (mu_dau or mu_ngon):   # ô gần vuông
        R = max(R, min(int(round(thick / ds)) + 1, int(round(thick / (0.6 * buoc_ngang))) + 1))
    G = np.zeros((C, R, 2))
    for c in range(C):
        p, nv = at(D, sc[c]), at(nrm, sc[c])
        for r in range(R):
            G[c, r] = p + nv * (-tops[c] + (tops[c] + bots[c]) * r / (R - 1))
    if mu_dau or mu_ngon:
        return _dai_co_mu(G, sc, D, cumD, tg, m, a_hard, (mu_dau, mu_ngon), buoc_vien_mu, buoc_ngang, W, H, ten, so_dot, in_tk)
    # thứ tự: vòng viền (hàng trên trái→phải, cột cuối xuống, hàng dưới phải→trái, cột đầu lên) rồi điểm trong
    ring = [(c, 0) for c in range(C)] + [(C - 1, r) for r in range(1, R)] + [(c, R - 1) for c in range(C - 2, -1, -1)] + [(0, r) for r in range(R - 2, 0, -1)]
    inner = [(c, r) for c in range(1, C - 1) for r in range(1, R - 1)]
    idx = -np.ones((C, R), int)
    pts, svals = [], []
    for k, (c, r) in enumerate(ring + inner):
        idx[c, r] = k
        pts.append(G[c, r])
        svals.append(sc[c])
    pts = np.array(pts)

    def minang(tri):
        P = pts[list(tri)]
        g = []
        for i in range(3):
            u, v = P[(i + 1) % 3] - P[i], P[(i + 2) % 3] - P[i]
            g.append(math.degrees(math.acos(max(-1, min(1, float(u @ v) / max(1e-9, math.hypot(*u) * math.hypot(*v)))))))
        return min(g)

    tris = []
    for c in range(C - 1):
        for r in range(R - 1):
            a0, b0, c0, d0 = idx[c, r], idx[c + 1, r], idx[c + 1, r + 1], idx[c, r + 1]
            t1 = [(a0, b0, c0), (a0, c0, d0)]
            t2 = [(a0, b0, d0), (b0, c0, d0)]
            tris += t1 if min(map(minang, t1)) >= min(map(minang, t2)) else t2
    L = Luoi(pts, tris, len(ring), len(ring), W, H, ten, s=np.array(svals))
    L.truc = (D, cumD)
    L.hang = (C, R, idx)
    L.ho = _phu(a_hard, pts, np.array(tris))
    if in_tk:
        L.in_tk(f"{ten} (dải {C} cột × {R} hàng, {so_dot} đốt)")
    return L


def luoi_o(w, h, cot, hang, u0=0.0, u1=1.0, v0=0.0, v1=1.0, ten=""):
    """lưới ô chữ nhật đều trên ảnh w×h (phần [u0, u1]×[v0, v1] theo tỉ lệ ảnh): cot × hang đỉnh. Đỉnh xếp theo hàng (r·cot + c);
    nh = nb = 0 (vòng viền không đứng đầu). Dùng khi đỉnh đặt theo công thức (lòng miệng)."""
    pts = [((u0 + (u1 - u0) * c / (cot - 1)) * w, (v0 + (v1 - v0) * r / (hang - 1)) * h) for r in range(hang) for c in range(cot)]
    tris = []
    for r in range(hang - 1):
        for c in range(cot - 1):
            a = r * cot + c
            tris += [(a, a + 1, a + cot + 1), (a, a + cot + 1, a + cot)]
    return Luoi(pts, tris, 0, 0, w, h, ten)
