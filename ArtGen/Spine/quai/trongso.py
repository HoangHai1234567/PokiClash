# -*- coding: utf-8 -*-
"""Trọng số đỉnh lưới cho thư viện quai. Mỗi bộ trọng số là list (một phần tử mỗi đỉnh) các dict {xương: w}.

- chuoi / chuoi_chieu / chuoi_geo: chuỗi xương (cổ, đuôi, râu, lưỡi, thân rắn): hàm cơ sở B-spline bậc hai theo vị trí dọc chuỗi
  (giữa đốt 0,75 đốt đó + 0,125 mỗi đốt kề; ở khớp 0,5 / 0,5). Không cột nào bám 100% một đốt (trừ ngọn), nên chuỗi xương gãy
  khúc bao nhiêu lưới vẫn cong trơn. cha=...: gốc chuỗi hoà vào xương cha như một đốt ảo (gốc đuôi mềm vào thân).
- vung: vùng (thân, bụng, đầu, vai...) hoà theo khoảng cách đi TRONG lưới (geodesic trên cạnh tam giác: không nhảy qua khe trắng),
  dải hoà cấu hình được.
- theo_truc: hai xương hoà theo một trục (hàm dưới hai xương: cổ họng / hàm).
- tron, nhan, chuan (tối đa 4 xương, chuẩn hoá), lam_tron (làm trơn trên lưới), cung (đồ cứng bám 100%), kiem (in số liệu).
"""
import heapq
import math

import numpy as np

from . import anh


def b2(t):
    """hàm cơ sở B-spline bậc hai, tâm ở 0, rộng 3."""
    t = abs(t)
    if t <= 0.5:
        return 0.75 - t * t
    if t < 1.5:
        return 0.5 * (1.5 - t) ** 2
    return 0.0


def _f_tu_s(s, dai):
    """độ dài dọc chuỗi -> vị trí theo đơn vị đốt (đốt có thể dài khác nhau)."""
    dai = np.atleast_1d(np.asarray(dai, float))
    if dai.size == 1:
        return np.asarray(s, float) / float(dai[0])
    cum = np.concatenate([[0], np.cumsum(dai)])
    s = np.asarray(s, float)
    j = np.clip(np.searchsorted(cum, s, side="right") - 1, 0, len(dai) - 1)
    return j + (s - cum[j]) / dai[j]


def chuoi_f(f, ten, cha=None, cha_hoa=1.0):
    """trọng số B-spline của các vị trí f (đơn vị đốt: 0 = gốc đốt 0, n = ngọn đốt cuối). ten: tên các đốt từ gốc ra ngọn."""
    n = len(ten)
    out = []
    for fv in np.atleast_1d(np.asarray(f, float)).tolist():
        d = {}
        for j in range(int(math.floor(fv - 1.5)), int(math.floor(fv + 1.5)) + 2):
            w = b2(fv - (j + 0.5))
            if w <= 1e-5:
                continue
            if j < 0:
                if cha:
                    d[cha] = d.get(cha, 0.0) + w * cha_hoa
                    d[ten[0]] = d.get(ten[0], 0.0) + w * (1 - cha_hoa)
                else:
                    d[ten[0]] = d.get(ten[0], 0.0) + w
            else:
                b = ten[min(n - 1, j)]
                d[b] = d.get(b, 0.0) + w
        out.append(d)
    return out


def chuoi(s, dai_dot, ten, cha=None, cha_hoa=1.0):
    """trọng số theo độ dài s dọc chuỗi (luoi_dai: luoi.s; đơn vị như dai_dot). dai_dot: một số hoặc danh sách độ dài từng đốt."""
    return chuoi_f(_f_tu_s(s, dai_dot), ten, cha, cha_hoa)


def _chieu_len_gay(Q, J):
    """chiếu điểm Q (N, 2) lên đường gấp khúc J (K, 2): trả độ dài dọc đường tới điểm chiếu (điểm ngoài hai đầu kéo dài theo
    hướng đoạn đầu / đoạn cuối, nên giá trị có thể < 0 hoặc > tổng dài)."""
    Q, J = np.asarray(Q, float), np.asarray(J, float)
    seg = J[1:] - J[:-1]
    ln = np.hypot(*seg.T)
    cum = np.concatenate([[0], np.cumsum(ln)])
    best_d = np.full(len(Q), np.inf)
    best_s = np.zeros(len(Q))
    for k in range(len(seg)):
        u = seg[k] / max(1e-9, ln[k])
        t = (Q - J[k]) @ u
        lo = -np.inf if k == 0 else 0.0
        hi = np.inf if k == len(seg) - 1 else ln[k]
        tc = np.clip(t, lo, hi)
        d = np.hypot(*(Q - (J[k] + tc[:, None] * u)).T)
        better = d < best_d - 1e-9
        best_d[better] = d[better]
        best_s[better] = cum[k] + tc[better]
    return best_s, cum


def chuoi_chieu(Q, J, ten, cha=None, cha_hoa=1.0):
    """trọng số chuỗi cho lưới bất kỳ: chiếu đỉnh Q (toạ độ thế giới rig, (N, 2)) lên đường các khớp J (n+1 điểm thế giới: gốc
    đốt 0 ... ngọn đốt cuối), rồi B-spline theo vị trí dọc đường. Hợp với chuỗi gần thẳng; chuỗi vẽ cong nhiều thì dùng chuoi_geo."""
    s, cum = _chieu_len_gay(Q, J)
    return chuoi(s, np.diff(cum), ten, cha, cha_hoa)


def dijkstra(L, nguon, gioi_han=np.inf):
    """khoảng cách đi trong lưới L (theo cạnh tam giác) từ tập đỉnh nguồn (list chỉ số, hoặc dict {đỉnh: khoảng cách đầu})."""
    adj = L.ke()
    d = np.full(L.n, np.inf)
    h = []
    items = nguon.items() if isinstance(nguon, dict) else ((i, 0.0) for i in nguon)
    for i, d0 in items:
        if d0 < d[i]:
            d[i] = d0
            heapq.heappush(h, (d0, i))
    while h:
        dv, v = heapq.heappop(h)
        if dv > d[v] or dv > gioi_han:
            continue
        for u, l in adj[v]:
            nd = dv + l
            if nd < d[u]:
                d[u] = nd
                heapq.heappush(h, (nd, u))
    return d


def _gan_nhat(L, p):
    return int(np.argmin(np.hypot(*(L.pts - np.asarray(p, float)).T)))


def chuoi_geo(L, J_anh, ten, cha=None, cha_hoa=1.0):
    """trọng số chuỗi theo khoảng cách đi trong lưới từ khớp gốc (chuỗi vẽ cong: đuôi cuộn, râu xoắn). J_anh: các khớp trên ẢNH
    mảnh (toạ độ như L.pts), gốc trước. Vị trí dọc chuỗi của mỗi đỉnh = khoảng cách geodesic từ khớp gốc, đổi sang đơn vị đốt
    theo khoảng cách geodesic của chính các khớp (nên khớp nằm đúng chỗ kẻ)."""
    J = np.asarray(J_anh, float)
    d = dijkstra(L, [_gan_nhat(L, J[0])])
    dj = np.array([d[_gan_nhat(L, p)] for p in J])
    dj[0] = 0.0
    for k in range(1, len(dj)):  # khớp phải tăng dần
        dj[k] = max(dj[k], dj[k - 1] + 1e-3)
    f = np.interp(d, dj, np.arange(len(dj), dtype=float), left=0.0, right=float(len(dj) - 1))
    over = d > dj[-1]
    f[over] = len(dj) - 1 + (d[over] - dj[-1]) / max(1e-6, dj[-1] - dj[-2])
    return chuoi_f(f, ten, cha, cha_hoa)


def _thuoc(L, vung):
    """đỉnh thuộc vùng: đa giác [(x, y)...] toạ độ ảnh mảnh, list đa giác, mặt nạ bool (H, W) cỡ ảnh, hoặc ("diem", [(x, y)...])
    (các đỉnh gần nhất), hoặc mảng chỉ số đỉnh."""
    from .luoi import _trong
    P = L.pts
    if isinstance(vung, tuple) and len(vung) == 2 and vung[0] == "diem":
        return np.unique([_gan_nhat(L, p) for p in vung[1]])
    if isinstance(vung, np.ndarray):
        if vung.dtype == bool and vung.ndim == 2:
            x = np.clip(P[:, 0].astype(int), 0, vung.shape[1] - 1)
            y = np.clip(P[:, 1].astype(int), 0, vung.shape[0] - 1)
            return np.flatnonzero(vung[y, x])
        if vung.ndim == 1:
            return vung.astype(int)
        polys = [vung]
    elif np.isscalar(vung[0][0]):
        polys = [vung]          # một đa giác
    else:
        polys = list(vung)      # nhiều đa giác
    ins = np.zeros(L.n, bool)
    for pg in polys:
        ins |= _trong(P, [np.asarray(pg, float)])
    return np.flatnonzero(ins)


def vung(L, cac_vung, dai_hoa=20.0, mac_dinh=None):
    """trọng số vùng hoà theo khoảng cách đi trong lưới. cac_vung: list [(xương, vùng)] theo thứ tự ưu tiên (vùng trước giành đỉnh
    trước); vùng như _thuoc. Đỉnh trong vùng b có khoảng cách 0 tới b; trọng số w_b ∝ exp(-(d_b / dai_hoa)²) nên ở ranh hai vùng
    0,5 / 0,5, sâu vào trong vùng thì về 1, chuyển trơn (đạo hàm 0 ở ranh). Đỉnh không thuộc vùng nào hoà theo vùng gần nhất.
    mac_dinh: xương cho lưới không có vùng nào chạm tới."""
    lab = -np.ones(L.n, int)
    names = []
    for k, (b, vg) in enumerate(cac_vung):
        names.append(b)
        ids = _thuoc(L, vg)
        ids = ids[lab[ids] < 0]
        if not len(ids):  # vùng không trúng đỉnh nào: lấy đỉnh gần tâm vùng nhất
            try:
                pg = np.asarray(vg[1] if isinstance(vg, tuple) else vg, float).reshape(-1, 2)
                i = _gan_nhat(L, pg.mean(0))
                if lab[i] < 0:
                    ids = np.array([i])
            except Exception:
                pass
        lab[ids] = k
    D = np.full((len(names), L.n), np.inf)
    for k in range(len(names)):
        src = np.flatnonzero(lab == k)
        if len(src):
            D[k] = dijkstra(L, src.tolist())
    out = []
    for i in range(L.n):
        d = D[:, i]
        if not np.isfinite(d).any():
            out.append({mac_dinh or names[0]: 1.0})
            continue
        dm = d[np.isfinite(d)].min()
        e = np.where(np.isfinite(d), np.exp(-(d * d - dm * dm) / (dai_hoa * dai_hoa)), 0.0)
        e /= e.sum()
        w = {}
        for k in np.flatnonzero(e > 1e-4):
            w[names[k]] = w.get(names[k], 0.0) + float(e[k])
        out.append(w)
    return out


def theo_truc(Q, p0, p1, a, b, u0=0.35, u1=0.65):
    """hai xương hoà dọc trục p0 → p1 (toạ độ như Q): u = vị trí chiếu (0 ở p0, 1 ở p1); u < u0 bám a, u > u1 bám b, giữa
    hoà smoothstep. Hàm dưới hai xương: a = xương cổ/đầu (cổ họng), b = xương hàm, trục từ sau bản lề ra mõm."""
    Q, p0, p1 = np.asarray(Q, float), np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    u = (Q - p0) @ d / max(1e-9, float(d @ d))
    x = np.clip((u - u0) / max(1e-6, u1 - u0), 0, 1)
    wb = x * x * (3 - 2 * x)
    return [{a: float(1 - v), b: float(v)} if 0 < v < 1 else ({b: 1.0} if v >= 1 else {a: 1.0}) for v in wb]


def cung(n, xuong):
    """đồ cứng thật (vỏ, sừng, đá, giáp): mọi đỉnh bám 100% một xương."""
    return [{xuong: 1.0} for _ in range(n)]


def nhan(W, he_so):
    he_so = np.broadcast_to(np.asarray(he_so, float), (len(W),))
    return [{b: w * float(k) for b, w in d.items()} for d, k in zip(W, he_so)]


def tron(*nguon):
    """cộng nhiều bộ trọng số có hệ số: tron((hệ_số_1, W1), (hệ_số_2, W2), ...); hệ số là số hoặc mảng theo đỉnh."""
    n = len(nguon[0][1])
    out = [dict() for _ in range(n)]
    for k, W in nguon:
        for i, d in enumerate(nhan(W, k)):
            o = out[i]
            for b, w in d.items():
                o[b] = o.get(b, 0.0) + w
    return out


def chuan(W, toi_da=4, bo=0.004):
    """giữ tối đa toi_da xương nặng nhất mỗi đỉnh, bỏ trọng số < bo, chuẩn hoá tổng 1."""
    out = []
    for d in W:
        it = sorted(((w, b) for b, w in d.items() if w > 0), reverse=True)[:toi_da]
        it = [(w, b) for w, b in it if w >= bo] or it[:1]
        s = sum(w for w, _ in it) or 1.0
        out.append({b: w / s for w, b in it})
    return out


def lam_tron(L, W, lan=2, giu=None, he=0.5):
    """làm trơn trọng số trên lưới (trung bình với đỉnh kề, lan vòng); giu: chỉ số đỉnh giữ nguyên (đồ cứng, hàng bám hàm)."""
    adj = L.ke()
    keep = set(np.asarray(giu, int).tolist()) if giu is not None else set()
    cur = [dict(d) for d in W]
    for _ in range(lan):
        nxt = []
        for i, d in enumerate(cur):
            if i in keep or not adj[i]:
                nxt.append(d)
                continue
            acc = {b: (1 - he) * w for b, w in d.items()}
            k = he / len(adj[i])
            for j, _l in adj[i]:
                for b, w in cur[j].items():
                    acc[b] = acc.get(b, 0.0) + k * w
            nxt.append(acc)
        cur = nxt
    return chuan(cur)


def kiem(W, ten="", cho_cung=(), in_ra=True):
    """số liệu trọng số: số xương tối đa mỗi đỉnh, số đỉnh bám cứng (≥ 99,5%) một xương theo từng xương. Đồ cứng thật khai trong
    cho_cung để khỏi bị nhắc."""
    mx = max((len(d) for d in W), default=0)
    hard = {}
    for d in W:
        b, w = max(d.items(), key=lambda kv: kv[1])
        if w >= 0.995:
            hard[b] = hard.get(b, 0) + 1
    bad = {b: c for b, c in hard.items() if b not in cho_cung}
    if in_ra:
        s = ", ".join(f"{b} {c}" for b, c in sorted(bad.items(), key=lambda kv: -kv[1])[:6])
        print(f"  trọng số {ten}: {len(W)} đỉnh, tối đa {mx} xương/đỉnh; bám cứng 100%: {sum(bad.values())} đỉnh" + (f" ({s})" if s else ""))
    return {"toi_da": mx, "cung": bad}
