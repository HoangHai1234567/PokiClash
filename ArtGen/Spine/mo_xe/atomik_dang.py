# -*- coding: utf-8 -*-
"""Dựng DẠNG KHÁC thẳng trên một .atomik (cùng xương, lưới, clip): đổi tỉ lệ xương, tô màu lại, thay mảnh bằng ảnh cắt từ concept,
gộp clip tiến hóa, tính lại khối game, chân dung. Dùng khi máy không có dữ liệu quét con gốc (skill pokiclash-spine-rig, "DẠNG KHÁC
trên CÙNG rig gốc"). Tính tư thế chép đúng Game/Atomik/AtomikPose.cs (xoay, dời cộng; tỉ lệ nhân; noScale; bezier điểm điều khiển
tuyệt đối; sk đổi hình; sa độ đậm).
"""
import gzip
import io
import json
import math
import struct

import cv2
import numpy as np
from PIL import Image


# ---------------------------------------------------------------- đọc / ghi
def load(path):
    b = open(path, "rb").read()
    assert b[:4] == b"ATMK"
    ver = struct.unpack("<H", b[4:6])[0]
    d = gzip.decompress(b[6:])
    n = struct.unpack("<I", d[:4])[0]
    J = json.loads(d[4:4 + n].decode("utf-8"))
    m = struct.unpack("<I", d[4 + n:8 + n])[0]
    img = np.array(Image.open(io.BytesIO(d[8 + n:8 + n + m])).convert("RGBA"))
    return J, img, ver


def save(path, J, img, ver=3):
    bio = io.BytesIO()
    q = Image.fromarray(img, "RGBA").quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
    q.save(bio, "PNG", optimize=True)          # như xuat.ghi_spine: atlas bảng màu 256
    png = bio.getvalue()
    js = json.dumps(J, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    body = struct.pack("<I", len(js)) + js + struct.pack("<I", len(png)) + png
    out = b"ATMK" + struct.pack("<H", ver) + gzip.compress(body, 9)
    open(path, "wb").write(out)
    return len(out), len(js), len(png)


def bi(J):
    return {b["name"]: i for i, b in enumerate(J["bones"])}


def si(J):
    return {s["name"]: i for i, s in enumerate(J["slots"])}


def clip(J, name):
    return next(i for i, a in enumerate(J["anims"]) if a["name"] == name)


# ---------------------------------------------------------------- khoá
def _bez(t0, v0, cx1, cy1, cx2, cy2, t1, v1, t):
    lo, hi, s = 0.0, 1.0, 0.5
    for _ in range(22):
        s = (lo + hi) * 0.5
        u = 1 - s
        xs = u * u * u * t0 + 3 * u * u * s * cx1 + 3 * u * s * s * cx2 + s * s * s * t1
        if xs < t:
            lo = s
        else:
            hi = s
    m = 1 - s
    return m * m * m * v0 + 3 * m * m * s * cy1 + 3 * m * s * s * cy2 + s * s * s * v1


def s1(k, t):
    S = 7
    n = len(k) // S
    if n == 0:
        return 0.0
    if t <= k[0]:
        return k[1]
    if t >= k[(n - 1) * S]:
        return k[(n - 1) * S + 1]
    i = 0
    while i < n - 2 and t >= k[(i + 1) * S]:
        i += 1
    o, q = i * S, i * S + S
    t0, v0, t1, v1 = k[o], k[o + 1], k[q], k[q + 1]
    kind = int(k[o + 2])
    if kind == 1:
        return v0
    if kind == 2:
        return _bez(t0, v0, k[o + 3], k[o + 4], k[o + 5], k[o + 6], t1, v1, t)
    return v0 + (v1 - v0) * (t - t0) / max(1e-6, t1 - t0)


def s2(k, t):
    S = 12
    n = len(k) // S
    if n == 0:
        return 0.0, 0.0
    if t <= k[0]:
        return k[1], k[2]
    if t >= k[(n - 1) * S]:
        return k[(n - 1) * S + 1], k[(n - 1) * S + 2]
    i = 0
    while i < n - 2 and t >= k[(i + 1) * S]:
        i += 1
    o, q = i * S, i * S + S
    t0, t1 = k[o], k[q]
    kind = int(k[o + 3])
    if kind == 1:
        return k[o + 1], k[o + 2]
    if kind == 2:
        return (_bez(t0, k[o + 1], k[o + 4], k[o + 5], k[o + 6], k[o + 7], t1, k[q + 1], t),
                _bez(t0, k[o + 2], k[o + 8], k[o + 9], k[o + 10], k[o + 11], t1, k[q + 2], t))
    u = (t - t0) / max(1e-6, t1 - t0)
    return k[o + 1] + (k[q + 1] - k[o + 1]) * u, k[o + 2] + (k[q + 2] - k[o + 2]) * u


# ---------------------------------------------------------------- tư thế
class Pose:
    def __init__(self, J):
        self.J = J
        nb = len(J["bones"])
        self.l = np.zeros((nb, 5))          # x, y, rot, sx, sy
        self.w = np.zeros((nb, 6))          # a, b, c, d, x, y
        ns = len(J["slots"])
        self.att = np.full(ns, -1, int)
        self.alpha = np.ones(ns)

    def sample(self, ci, t):
        J = self.J
        for i, b in enumerate(J["bones"]):
            self.l[i] = (b["x"], b["y"], b["rot"], b["sx"], b["sy"])
        for s, sl in enumerate(J["slots"]):
            self.att[s] = sl.get("att", -1)
            self.alpha[s] = 1 - min(1.0, max(0.0, sl.get("fade", 0.0) or 0.0))
        if ci is None or ci < 0:
            return self
        c = J["anims"][ci]
        for tl in c.get("tls") or []:
            i = tl["bone"]
            if tl["type"] == 0:
                self.l[i, 2] += s1(tl["keys"], t)
            else:
                vx, vy = s2(tl["keys"], t)
                if tl["type"] == 1:
                    self.l[i, 0] += vx
                    self.l[i, 1] += vy
                else:
                    self.l[i, 3] *= vx
                    self.l[i, 4] *= vy
        for k in c.get("sk") or []:
            for tt, a in zip(k["times"], k["atts"]):
                if tt <= t + 1e-5:
                    self.att[k["slot"]] = a
        for k in c.get("sa") or []:
            self.alpha[k["slot"]] = min(1.0, max(0.0, s1(k["keys"], t)))
        return self

    def world(self):
        J = self.J
        for i, b in enumerate(J["bones"]):
            x, y, r, sx, sy = self.l[i]
            rad = math.radians(r)
            cs, sn = math.cos(rad), math.sin(rad)
            a, bb, c, d = cs * sx, -sn * sy, sn * sx, cs * sy
            p = b["parent"]
            if p < 0:
                self.w[i] = (a, bb, c, d, x, y)
                continue
            pa, pb, pc, pd, px, py = self.w[p]
            if b.get("noScale"):
                n0, n1 = math.hypot(pa, pc), math.hypot(pb, pd)
                if n0 > 1e-6:
                    pa, pc = pa / n0, pc / n0
                if n1 > 1e-6:
                    pb, pd = pb / n1, pd / n1
            self.w[i] = (pa * a + pb * c, pa * bb + pb * d, pc * a + pd * c, pc * bb + pd * d,
                         self.w[p][0] * x + self.w[p][1] * y + px, self.w[p][2] * x + self.w[p][3] * y + py)
        return self

    def at(self, ci, t):
        return self.sample(ci, t).world()

    def bone_pt(self, b, lx=0.0, ly=0.0):
        a, bb, c, d, x, y = self.w[b]
        return np.array([a * lx + bb * ly + x, c * lx + d * ly + y])

    def verts(self, ai):
        """đỉnh thế giới (N x 2) của hình ai ở tư thế hiện tại."""
        w = self.J["atts"][ai]["wInfo"]
        out, k = [], 0
        while k < len(w):
            n = int(w[k])
            k += 1
            px = py = 0.0
            for _ in range(n):
                b, x, y, wt = int(w[k]), w[k + 1], w[k + 2], w[k + 3]
                a_, b_, c_, d_, tx, ty = self.w[b]
                px += (a_ * x + b_ * y + tx) * wt
                py += (c_ * x + d_ * y + ty) * wt
                k += 4
            out.append((px, py))
        return np.array(out)

    def items(self):
        """(slot, att, đỉnh thế giới, độ đậm) theo thứ tự vẽ, chỉ hình đang hiện."""
        res = []
        for s in range(len(self.J["slots"])):
            a = self.att[s]
            if a < 0 or self.alpha[s] < 0.004:
                continue
            res.append((s, a, self.verts(a), self.alpha[s]))
        return res


def uv_px(J, img, ai):
    H, W = img.shape[:2]
    u = np.array(J["atts"][ai]["uvs"], float).reshape(-1, 2)
    return np.c_[u[:, 0] * W, (1 - u[:, 1]) * H]


def bounds(P):
    xs, ys = [], []
    for _, _, V, _ in P.items():
        xs += [V[:, 0].min(), V[:, 0].max()]
        ys += [V[:, 1].min(), V[:, 1].max()]
    return min(xs), min(ys), max(xs), max(ys)


def render(J, img, P, box, scale, bg=None, ss=2, only=None):
    """vẽ tư thế P trong khung box (x0, y0, x1, y1 đơn vị rig, y lên) với scale px / đơn vị; bg None = trong suốt. RGBA uint8."""
    x0, y0, x1, y1 = box
    k = scale * ss
    Wc, Hc = int(round((x1 - x0) * k)), int(round((y1 - y0) * k))
    acc = np.zeros((Hc, Wc, 4), np.float32)          # tiền nhân alpha
    tex = img.astype(np.float32) / 255.0
    tex[..., :3] *= tex[..., 3:4]
    for s, a, V, al in P.items():
        if only is not None and s not in only:
            continue
        uv = uv_px(J, img, a)
        dst = np.c_[(V[:, 0] - x0) * k, (y1 - V[:, 1]) * k]
        tris = np.array(J["atts"][a]["tris"]).reshape(-1, 3)
        for t in tris:
            src_t, dst_t = uv[t].astype(np.float32), dst[t].astype(np.float32)
            r = cv2.boundingRect(dst_t)
            if r[2] <= 0 or r[3] <= 0:
                continue
            rx, ry, rw, rh = r
            rx0, ry0, rx1, ry1 = max(rx, 0), max(ry, 0), min(rx + rw, Wc), min(ry + rh, Hc)
            if rx1 <= rx0 or ry1 <= ry0:
                continue
            M = cv2.getAffineTransform(src_t, dst_t - np.float32([rx, ry]))
            patch = cv2.warpAffine(tex, M, (rw, rh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            mask = np.zeros((rh, rw), np.float32)
            cv2.fillConvexPoly(mask, np.round((dst_t - np.float32([rx, ry])) * 16).astype(np.int32), 1.0, cv2.LINE_AA, 4)
            pm = patch * (mask[..., None] * al)
            sub = acc[ry0:ry1, rx0:rx1]
            pp = pm[ry0 - ry:ry1 - ry, rx0 - rx:rx1 - rx]
            sub[:] = pp + sub * (1 - pp[..., 3:4])
    if bg is not None:
        bgc = np.array(list(bg) + [255], np.float32) / 255.0
        acc = acc + bgc * (1 - acc[..., 3:4])
        acc[..., 3] = 1.0
    out = acc.copy()
    a = np.clip(out[..., 3:4], 1e-6, 1)
    out[..., :3] = np.where(out[..., 3:4] > 0, out[..., :3] / a, 0)
    im = Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")
    if ss > 1:
        im = im.resize((Wc // ss, Hc // ss), Image.LANCZOS)
    return im


# ---------------------------------------------------------------- sửa rig
def scale_bones(J, ti):
    """ti: {"xương": k | [kx, ky] | {"s": .., "dx": .., "dy": ..}} nhân tỉ lệ / dời dáng gốc (như atomik_bocuc.py)."""
    B = bi(J)
    for nm, k in ti.items():
        b = J["bones"][B[nm]]
        if isinstance(k, dict):
            b["x"] += k.get("dx", 0.0)
            b["y"] += k.get("dy", 0.0)
            k = k.get("s", 1.0)
        kx, ky = (k, k) if not isinstance(k, list) else k
        b["sx"] *= kx
        b["sy"] *= ky


def canvas_map(khung, W, H, pad=1.06):
    """phép đổi px canvas (của atomik_bocuc.py --khung) ↔ đơn vị rig."""
    x0, y0, x1, y1 = khung
    z = max((x1 - x0) * pad / W, (y1 - y0) * pad / H)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    to_rig = lambda p: np.c_[cx + (np.asarray(p, float)[:, 0] - W / 2) * z, cy - (np.asarray(p, float)[:, 1] - H / 2) * z]  # noqa: E731
    to_px = lambda q: np.c_[(np.asarray(q, float)[:, 0] - cx) / z + W / 2, H / 2 - (np.asarray(q, float)[:, 1] - cy) / z]  # noqa: E731
    return to_rig, to_px, z


def _cr(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


def atlas_density(J, img, P):
    """px atlas trên một đơn vị rig (trung vị trên các hình, ở tư thế P)."""
    r = []
    for s, a, V, _ in P.items():
        uv = uv_px(J, img, a)
        tris = np.array(J["atts"][a]["tris"]).reshape(-1, 3)
        for t in tris[:3]:
            A1 = abs(_cr(V[t[1]] - V[t[0]], V[t[2]] - V[t[0]]))
            A2 = abs(_cr(uv[t[1]] - uv[t[0]], uv[t[2]] - uv[t[0]]))
            if A1 > 1e-3:
                r.append(math.sqrt(A2 / A1))
    return float(np.median(r))


def add_regions(J, img, ims, gap=4):
    """thêm ảnh (RGBA PIL) vào dưới atlas; trả atlas mới và danh sách khung px (x, y, w, h). Cập nhật uvs mọi hình cũ."""
    H, W = img.shape[:2]
    x, y, rowh, boxes = gap, H + gap, 0, []
    W2 = W
    for im in ims:
        w, h = im.size
        if x + w + gap > W:
            x, y, rowh = gap, y + rowh + gap, 0
        boxes.append((x, y, w, h))
        W2 = max(W2, x + w + gap)
        x += w + gap
        rowh = max(rowh, h)
    H2 = y + rowh + gap
    H2 = (H2 + 3) // 4 * 4
    W2 = (W2 + 3) // 4 * 4
    out = np.zeros((H2, W2, 4), np.uint8)
    out[:H, :W] = img
    for im, (bx, by, w, h) in zip(ims, boxes):
        out[by:by + h, bx:bx + w] = np.asarray(im.convert("RGBA"))
    for a in J["atts"]:
        u = a["uvs"]
        for i in range(0, len(u), 2):
            px, py = u[i] * W, (1 - u[i + 1]) * H
            u[i], u[i + 1] = round(px / W2, 6), round(1 - py / H2, 6)
    return out, boxes


def set_quad(J, H2, W2, ai, box, bone, local_corners):
    """hình ai thành ô cứng 4 đỉnh trên xương bone: khung atlas box, góc TL, TR, BR, BL (toạ độ theo xương)."""
    bx, by, w, h = box
    uv = [(bx, by), (bx + w, by), (bx + w, by + h), (bx, by + h)]
    a = J["atts"][ai]
    a["uvs"] = [v for x, y in uv for v in (round(x / W2, 6), round(1 - y / H2, 6))]
    a["tris"] = [0, 1, 2, 0, 2, 3]
    a["wInfo"] = [v for (lx, ly) in local_corners for v in (1, bone, round(float(lx), 3), round(float(ly), 3), 1.0)]


def bone_local(P, b, pts):
    a, bb, c, d, x, y = P.w[b]
    M = np.array([[a, bb], [c, d]])
    return (np.linalg.inv(M) @ (np.asarray(pts, float) - [x, y]).T).T


# ---------------------------------------------------------------- màu
def _lab(rgb):
    return cv2.cvtColor(np.asarray(rgb, np.uint8).reshape(-1, 1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)


def hx(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def att_masks(J, img, ais):
    """mặt nạ px atlas phủ bởi tam giác của các hình ais."""
    H, W = img.shape[:2]
    m = np.zeros((H, W), np.uint8)
    for a in ais:
        uv = uv_px(J, img, a)
        for t in np.array(J["atts"][a]["tris"]).reshape(-1, 3):
            cv2.fillConvexPoly(m, np.round(uv[t]).astype(np.int32), 1)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    return m.astype(bool)


def recolor(img, mask, pairs, ink_l=38.0, sigma=14.0):
    """tô màu lại vùng mask: mỗi px dời màu (Lab) theo các cặp (cũ, mới), trọng số mềm theo khoảng cách tới màu cũ; px mực (L thấp)
    giữ nguyên. Giữ vân chì sáp (độ lệch quanh màu cũ được giữ)."""
    H, W = img.shape[:2]
    idx = np.flatnonzero(mask.reshape(-1) & (img[..., 3].reshape(-1) > 0))
    if len(idx) == 0:
        return img
    rgb = img[..., :3].reshape(-1, 3)[idx]
    L = _lab(rgb)
    old = _lab([hx(a) for a, _ in pairs])
    new = _lab([hx(b) for _, b in pairs])
    d2 = ((L[:, None, :] - old[None, :, :]) ** 2).sum(-1)
    near = d2.argmin(1)
    dmin = np.sqrt(d2[np.arange(len(L)), near])
    wgt = np.exp(-(np.maximum(dmin - sigma, 0) / (2 * sigma)) ** 2)
    shift = (new - old)[near] * wgt[:, None]
    ink = L[:, 0] < ink_l * 255 / 100
    shift[ink] = 0
    L2 = np.clip(L + shift, 0, 255).astype(np.uint8)
    rgb2 = cv2.cvtColor(L2.reshape(-1, 1, 3), cv2.COLOR_LAB2RGB).reshape(-1, 3)
    out = img.copy()
    flat = out[..., :3].reshape(-1, 3)
    flat[idx] = rgb2
    return out


def clusters(img, mask, k=14):
    """màu chủ đạo (hex, tỉ lệ) trong vùng mask, bỏ mực."""
    px = img[..., :3][mask & (img[..., 3] > 200)]
    L = _lab(px)
    px = px[L[:, 0] > 38 * 255 / 100]
    if len(px) > 60000:
        px = px[np.random.RandomState(1).choice(len(px), 60000, replace=False)]
    Z = _lab(px)
    _, lab_, C = cv2.kmeans(Z, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5), 3, cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab_.ravel(), minlength=k) / len(lab_)
    rgb = cv2.cvtColor(np.clip(C, 0, 255).astype(np.uint8).reshape(-1, 1, 3), cv2.COLOR_LAB2RGB).reshape(-1, 3)
    order = np.argsort(-cnt)
    return [("#%02X%02X%02X" % tuple(rgb[i]), round(float(cnt[i]), 3)) for i in order]


# ---------------------------------------------------------------- khoá tự viết
def rot_keys(times_vals):
    return [v for t, x in times_vals for v in (round(float(t), 4), round(float(x), 3), 0, 0, 0, 0, 0)]


def xy_keys(times_xy):
    return [v for t, x, y in times_xy for v in (round(float(t), 4), round(float(x), 4), round(float(y), 4), 0, 0, 0, 0, 0, 0, 0, 0, 0)]


def add_bone(J, name, parent, x=0.0, y=0.0, rot=0.0):
    J["bones"].append({"name": name, "parent": parent, "x": float(x), "y": float(y), "rot": float(rot), "sx": 1.0, "sy": 1.0,
                       "noScale": False})
    return len(J["bones"]) - 1


def sway(J, bone, amp=4.0, chu_ky=1.6, pha=0.0, fps=10):
    """thêm khoá xoay hình sin (đung đưa) cho xương bone vào MỌI clip; chu kỳ làm tròn để khép vòng đúng thời lượng clip."""
    for an in J["anims"]:
        d = an["dur"]
        n = max(1, round(d / chu_ky))
        T = d / n
        ts = np.linspace(0, d, max(2, int(round(d * fps)) + 1))
        an.setdefault("tls", []).append({"bone": bone, "type": 0,
                                         "keys": rot_keys([(t, amp * math.sin(2 * math.pi * (t / T + pha))) for t in ts])})


# ---------------------------------------------------------------- tiến hóa
def _shift_tl(keys, S, s, off, val_at, end):
    """giữ phần khoá từ giây s tới end, dời giờ thêm off; khoá đầu (ở s) tính bằng val_at(s), đoạn đầu nối thẳng."""
    n = len(keys) // S
    out = []
    first = val_at(s)
    head = [s + off] + list(first)
    out += head + [0] * (S - len(head))
    for i in range(n):
        o = i * S
        t = keys[o]
        if t <= s + 1e-6 or t > end + 1e-6:
            continue
        k = list(keys[o:o + S])
        k[0] = t + off
        kind_i = 2 if S == 7 else 3
        if int(k[kind_i]) == 2:                      # điểm điều khiển bezier: giờ tuyệt đối
            if S == 7:
                k[3] += off
                k[5] += off
            else:
                k[4] += off
                k[6] += off
                k[8] += off
                k[10] += off
        out += k
    # nếu khoá trước khoá đầu tiên được giữ là bezier thì đoạn s → khoá kế: nối thẳng (đã đặt kiểu 0 ở head)
    return out


def gop_tien_hoa(JA, imgA, JB, imgB, k_B, dur=3.0, tB0=1.1, nhe=0.5, than_A=None, ten="evolve"):
    """thêm dạng sau (JB) bản nhẹ vào rig dạng trước (JA) + clip tiến hóa. k_B: tỉ lệ dạng sau trong rig gộp
    (= size_B / size_A * height_A / height_B). than_A: xương thân của A để rung. Trả atlas mới."""
    nA_b, nA_s, nA_a = len(JA["bones"]), len(JA["slots"]), len(JA["atts"])
    HB, WB = imgB.shape[:2]
    small = Image.fromarray(imgB, "RGBA").resize((max(4, round(WB * nhe)), max(4, round(HB * nhe))), Image.LANCZOS)
    imgA2, boxes = add_regions(JA, imgA, [small])
    H2, W2 = imgA2.shape[:2]
    bx, by, bw, bh = boxes[0]
    root_A = bi(JA)["root"]
    for i, b in enumerate(JB["bones"]):
        nb = dict(b)
        nb["name"] = "n_" + b["name"]
        nb["parent"] = root_A if b["parent"] < 0 else b["parent"] + nA_b
        if b["parent"] < 0:
            nb["sx"], nb["sy"] = b["sx"] * k_B, b["sy"] * k_B
        JA["bones"].append(nb)
    for s in JB["slots"]:
        ns = dict(s)
        ns["name"] = "n_" + s["name"]
        ns["bone"] = s["bone"] + nA_b
        ns["att"] = s["att"] + nA_a if s.get("att", -1) >= 0 else -1
        ns["fade"] = 1.0
        JA["slots"].append(ns)
    for a in JB["atts"]:
        na = dict(a)
        na["slot"] = a["slot"] + nA_s
        u = a["uvs"]
        uv = []
        for i in range(0, len(u), 2):
            px, py = bx + u[i] * bw, by + (1 - u[i + 1]) * bh
            uv += [round(px / W2, 6), round(1 - py / H2, 6)]
        na["uvs"] = uv
        w, k, nw = a["wInfo"], 0, []
        while k < len(w):
            m = int(w[k])
            nw.append(m)
            k += 1
            for _ in range(m):
                nw += [int(w[k]) + nA_b, w[k + 1], w[k + 2], w[k + 3]]
                k += 4
        na["wInfo"] = nw
        JA["atts"].append(na)
    # ---- clip tiến hóa
    ia = clip(JA, "idle")
    ib = clip(JB, "idle")
    idA, idB = JA["anims"][ia], JB["anims"][ib]
    tls = []
    for tl in idA.get("tls") or []:                 # A: idle như thường cho tới lúc tan
        tls.append({"bone": tl["bone"], "type": tl["type"], "keys": list(tl["keys"])})
    dB = idB["dur"]
    s0 = max(0.0, dB - (dur - tB0))
    off = tB0 - s0
    for tl in idB.get("tls") or []:
        S = 7 if tl["type"] == 0 else 12
        kk = tl["keys"]
        f = (lambda t, kk=kk: (s1(kk, t),)) if S == 7 else (lambda t, kk=kk: s2(kk, t))
        tls.append({"bone": tl["bone"] + nA_b, "type": tl["type"], "keys": _shift_tl(kk, S, s0, off, f, dB)})
    if than_A is not None:                           # A gồng: rung xoay nhanh, phồng nhẹ
        ts = np.arange(0.0, tB0 + 0.3 + 1e-6, 1 / 30)
        amp = lambda t: 0.0 if t < 0.25 else min(1.0, (t - 0.25) / 0.5)  # noqa: E731
        tls.append({"bone": than_A, "type": 0, "keys": rot_keys([(t, 2.2 * amp(t) * math.sin(2 * math.pi * 11 * t)) for t in ts])})
        tls.append({"bone": than_A, "type": 2, "keys": xy_keys([(t, 1 + 0.05 * amp(t), 1 + 0.07 * amp(t)) for t in ts])})
    nroot = nA_b + next(i for i, b in enumerate(JB["bones"]) if b["parent"] < 0)
    tls.append({"bone": nroot, "type": 2, "keys": xy_keys([(0, 0.8, 0.8), (tB0, 0.8, 0.8), (tB0 + 0.35, 1.04, 1.04), (tB0 + 0.6, 1.0, 1.0)])})
    sa = []
    for s in range(nA_s):
        sa.append({"slot": s, "keys": rot_keys([(0, 1), (tB0 - 0.05, 1), (tB0 + 0.25, 0), (dur, 0)])})
    for s in range(len(JB["slots"])):
        sa.append({"slot": s + nA_s, "keys": rot_keys([(0, 0), (tB0 - 0.05, 0), (tB0 + 0.25, 1), (dur, 1)])})
    sk = [{"slot": k_["slot"] + nA_s, "times": [t + off for t in k_["times"]], "atts": [a + nA_a if a >= 0 else -1 for a in k_["atts"]]}
          for k_ in (idB.get("sk") or [])]
    JA["anims"].append({"name": ten, "dur": dur, "tls": tls, "sk": sk, "sa": sa, "ev": []})
    return imgA2


# ---------------------------------------------------------------- sửa chuyển động
def scale_rot(J, bone, f):
    """nhân biên độ khoá xoay của xương bone trong mọi clip (giá trị và tung độ điểm điều khiển bezier)."""
    for an in J["anims"]:
        for tl in an.get("tls") or []:
            if tl["bone"] != bone or tl["type"] != 0:
                continue
            k = tl["keys"]
            for o in range(0, len(k), 7):
                k[o + 1] *= f
                if int(k[o + 2]) == 2:
                    k[o + 4] *= f
                    k[o + 6] *= f


def clamp_legs(J, legs, du=1.06, fps=30, clips=None):
    """chân bám xương bàn TÁCH khỏi thân (con của xương gốc), clip kéo bàn ra xa thì lưới chân giãn dài. Mỗi chân (hông, bàn):
    nếu khoảng cách hông → bàn vượt du × lớn nhất ở idle thì kéo bàn về phía hông; ghi lại khoá dời của xương bàn (30 khung/giây) cho
    clip có vượt. Trả {clip: số khung đã kéo}."""
    B = bi(J)
    P = Pose(J)
    ii = clip(J, "idle")
    lim = {}
    for hip, foot in legs:
        m = 0.0
        for t in np.arange(0, J["anims"][ii]["dur"] + 1e-6, 1 / fps):
            P.at(ii, t)
            m = max(m, float(np.hypot(*(P.bone_pt(B[foot]) - P.bone_pt(B[hip])))))
        lim[foot] = m * du
    bao = {}
    for ci, an in enumerate(J["anims"]):
        if clips is not None and an["name"] not in clips:
            continue
        ts = np.arange(0, an["dur"] + 1e-6, 1 / fps)
        if ts[-1] < an["dur"] - 1e-6:
            ts = np.r_[ts, an["dur"]]
        new = {foot: [] for _, foot in legs}
        n_keo = 0
        for t in ts:
            P.at(ci, t)
            for hip, foot in legs:
                fb = B[foot]
                h, f = P.bone_pt(B[hip]), P.bone_pt(fb)
                L = float(np.hypot(*(f - h)))
                if L > lim[foot]:
                    f = h + (f - h) * lim[foot] / L
                    n_keo += 1
                par = J["bones"][fb]["parent"]
                a, b_, c, d, x, y = P.w[par]
                loc = np.linalg.solve(np.array([[a, b_], [c, d]]), f - [x, y])
                new[foot].append((t, loc[0] - J["bones"][fb]["x"], loc[1] - J["bones"][fb]["y"]))
        if n_keo == 0:
            continue
        bao[an["name"]] = n_keo
        feet = {B[foot] for _, foot in legs}
        an["tls"] = [tl for tl in an.get("tls") or [] if not (tl["bone"] in feet and tl["type"] == 1)]
        for _, foot in legs:
            an["tls"].append({"bone": B[foot], "type": 1, "keys": xy_keys(new[foot])})
    return bao
