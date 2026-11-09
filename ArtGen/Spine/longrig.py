# -*- coding: utf-8 -*-
"""Bộ rig mảnh rời + lưới có trọng số theo chuỗi xương (Thủy Long, 2026-11-08). Dùng cho tướng GPT vẽ từng mảnh (cách A),
tay, chân, đuôi, áo choàng vẽ liền cả chi rồi uốn bằng lưới, không cắt khớp.

- Toạ độ rig: pixel, y lên, gốc giữa hai chân trên mặt đất, con nhìn sang phải. Xương dáng gốc không xoay, không co giãn.
- Mảnh chuỗi (chain): khoảng cách đi trong hình (geodesic) từ đầu khớp chia mảnh thành n đoạn bằng nhau; khớp = tâm lát cắt;
  trọng số đỉnh theo khoảng cách đó, hai xương kề nhau hoà dần quanh khớp (smoothstep), đoạn đầu hoà một nửa vào xương cha.
- Animation viết bằng hàm thời gian (khoá chính có đường cong êm), rồi nướng mỗi khung (FPS): chân giải IK hai đoạn (bàn chân
  bám đất), chuỗi mềm (đuôi, mào, vải, áo choàng) chạy lò xo đuổi theo dáng động học nên có độ trễ và dư lực; xuất khoá dày
  rồi lược (RDP) trước khi ghi Spine 4.2 và .atomik.
"""
import copy
import heapq
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import atomik
import mesh as meshlib
import rig as riglib
from spine_compat import _convert_timeline, pack

FPS = 30


# ---------------------------------------------------------------- đường cong
def ease(kind, u):
    u = min(1.0, max(0.0, u))
    if kind == "l":
        return u
    if kind == "i":
        return u * u * u
    if kind == "o":
        return 1 - (1 - u) ** 3
    if kind == "ob":  # ra nhanh, vượt nhẹ rồi về
        c = 1.70158 * 1.2
        return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    if kind == "s":  # sine io
        return 0.5 - 0.5 * math.cos(math.pi * u)
    if kind == "step":
        return 0.0 if u < 1 else 1.0
    return u * u * u * (u * (6 * u - 15) + 10)  # "io": smootherstep


def curve(t, keys):
    """keys: [(t, v), (t, v, kiểu), ...]; kiểu (mặc định io) là của đoạn KẾT THÚC ở khoá đó."""
    if t <= keys[0][0]:
        return keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            return a[1] + (b[1] - a[1]) * ease(b[2] if len(b) > 2 else "io", u)
    return keys[-1][1]


def wave(t, period, amp, phase=0.0):
    return amp * math.sin(2 * math.pi * (t / period - phase))


def smooth01(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- rig
class Rig:
    def __init__(self, name):
        self.name = name
        self.bones = []          # [{name, parent, wx, wy}]
        self.bi = {}
        self.slots = []          # [{name, bone, att}]
        self.atts = {}           # slot -> {att: spec}
        self.images = {}         # tên ảnh -> PIL RGBA
        self.chains = {}         # tên chuỗi -> [xương]
        self.points = {}         # điểm đặt tên (mũi vũ khí...) -> (xương, x, y theo xương)
        self.legs = {}           # bên -> (đùi, cẳng, bàn chân)
        self.ik_space = None
        self.fx_slots = set()

    def bone(self, name, parent, wx, wy):
        self.bi[name] = len(self.bones)
        self.bones.append({"name": name, "parent": parent, "wx": float(wx), "wy": float(wy)})

    def bw(self, name):
        b = self.bones[self.bi[name]]
        return b["wx"], b["wy"]

    def slot(self, name, bone, att=None, fx=False):
        self.slots.append({"name": name, "bone": bone, "att": att})
        self.atts.setdefault(name, {})
        if fx:
            self.fx_slots.add(name)

    def region(self, slot, att, img, bone, cx, cy, w=None, h=None, rot=0.0):
        im = self.images[img]
        bx, by = self.bw(bone)
        self.atts[slot][att] = {"type": "region", "path": img, "x": cx - bx, "y": cy - by,
                                "width": float(w if w is not None else im.width),
                                "height": float(h if h is not None else im.height), "bone": bone, "rot": float(rot)}

    def mesh(self, slot, att, img, vw, uv, tris, nh, weights):
        """vw: đỉnh toạ độ rig (N,2); uv chuẩn hoá theo ảnh (v xuống); weights: [[(xương, w)...] mỗi đỉnh]."""
        self.atts[slot][att] = {"type": "mesh", "path": img, "vw": np.asarray(vw, float), "uv": np.asarray(uv, float),
                                "tris": np.asarray(tris, int), "nh": int(nh), "weights": weights}

    def point(self, name, bone, wx, wy):
        bx, by = self.bw(bone)
        self.points[name] = (bone, wx - bx, wy - by)


# ---------------------------------------------------------------- mảnh
def geodesic(mask, seeds):
    """khoảng cách đi trong mặt nạ (8 hướng) từ các điểm hạt (x, y)."""
    H, W = mask.shape
    d = np.full((H, W), np.inf, np.float32)
    pq = []
    for x, y in seeds:
        x, y = int(round(min(W - 1, max(0, x)))), int(round(min(H - 1, max(0, y))))
        if not mask[y, x]:  # hạt lọt ngoài mặt nạ: lấy điểm trong mặt nạ gần nhất
            ys, xs = np.nonzero(mask)
            j = int(np.argmin((xs - x) ** 2 + (ys - y) ** 2))
            x, y = int(xs[j]), int(ys[j])
        d[y, x] = 0
        heapq.heappush(pq, (0.0, x, y))
    nb = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
    while pq:
        dd, x, y = heapq.heappop(pq)
        if dd > d[y, x]:
            continue
        for dx, dy, c in nb:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and mask[ny, nx] and dd + c < d[ny, nx]:
                d[ny, nx] = dd + c
                heapq.heappush(pq, (dd + c, nx, ny))
    return d


class Piece:
    """mảnh ở tỉ lệ rig: ảnh RGBA, góc trên trái (ox, oy) theo toạ độ rig (X = ox + u, Y = oy - v)."""

    def __init__(self, name, rgba, ox, oy):
        self.name, self.rgba, self.ox, self.oy = name, rgba, ox, oy
        self.mask = (rgba[:, :, 3] > 128).astype(np.uint8)

    def to_rig(self, u, v):
        return self.ox + u, self.oy - v

    def to_px(self, X, Y):
        return X - self.ox, self.oy - Y

    def chain(self, start, end=None, n=2, end_far=False):
        """khớp dọc mảnh: start, end theo toạ độ rig (end None hoặc end_far: điểm xa nhất). Trả (khớp rig, bản đồ s 0..1)."""
        sx, sy = self.to_px(*start)
        D = geodesic(self.mask > 0, [(sx, sy)])
        fin = np.where(np.isfinite(D), D, -1)
        if end is None or end_far:
            ey, ex = np.unravel_index(int(np.argmax(fin)), D.shape)
        else:
            ex, ey = self.to_px(*end)
            ex, ey = int(round(min(D.shape[1] - 1, max(0, ex)))), int(round(min(D.shape[0] - 1, max(0, ey))))
            if not np.isfinite(D[ey, ex]):
                ys, xs = np.nonzero(np.isfinite(D))
                j = int(np.argmin((xs - ex) ** 2 + (ys - ey) ** 2))
                ex, ey = int(xs[j]), int(ys[j])
        L = float(D[ey, ex])
        joints = [start]
        for k in range(1, n):
            lv = L * k / n
            band = np.isfinite(D) & (np.abs(D - lv) < 1.6)
            ys, xs = np.nonzero(band)
            joints.append(self.to_rig(float(xs.mean()), float(ys.mean())))
        joints.append(self.to_rig(float(ex), float(ey)))
        s = np.where(np.isfinite(D), D / max(L, 1e-6), np.nan)
        return joints, s

    def make_mesh(self, step_edge=9, step_in=16):
        pts, nh, tris = meshlib.mesh_mask(self.mask, step_edge, step_in, min_area=40)
        return pts, nh, tris


def sample_map(s, pts):
    """giá trị bản đồ s tại các đỉnh (đỉnh viền lọt ngoài: lấy điểm hợp lệ gần nhất)."""
    H, W = s.shape
    ok = np.isfinite(s)
    ys, xs = np.nonzero(ok)
    out = []
    for x, y in pts:
        xi, yi = int(round(min(W - 1, max(0, x)))), int(round(min(H - 1, max(0, y))))
        if ok[yi, xi]:
            out.append(float(s[yi, xi]))
        else:
            j = int(np.argmin((xs - x) ** 2 + (ys - y) ** 2))
            out.append(float(s[ys[j], xs[j]]))
    return np.array(out)


def chain_weights(svals, bones, parent=None, blend=0.16, parent_blend=0.12):
    n = len(bones)
    W = []
    for s in svals:
        s = min(1.0, max(0.0, s))
        k = min(n - 1, int(s * n))
        ws = {bones[k]: 1.0}
        for j in range(1, n):  # hoà quanh khớp j (s = j/n), nửa bề rộng blend (theo s)
            c = j / n
            if abs(s - c) < blend:
                t = smooth01((s - c + blend) / (2 * blend))
                ws = {bones[j - 1]: 1 - t, bones[j]: t}
        if parent and s < parent_blend:
            wp = 0.5 * (1 - smooth01(s / parent_blend))
            ws = {b: w * (1 - wp) for b, w in ws.items()}
            ws[parent] = ws.get(parent, 0) + wp
        ws = {b: w for b, w in ws.items() if w > 0.01}
        tot = sum(ws.values())
        W.append([(b, w / tot) for b, w in ws.items()])
    return W


def add_chain_piece(R, piece, slot, img, bones, parent, joints, s, step_edge=9, step_in=16, blend=0.16, parent_blend=0.12,
                    make_bones=True):
    """mảnh chuỗi thành lưới có trọng số; make_bones: tạo xương bones[k] tại joints[k] (cha: parent rồi xương trước)."""
    if make_bones:
        p = parent
        for b, j in zip(bones, joints):
            R.bone(b, p, j[0], j[1])
            p = b
    pts, nh, tris = piece.make_mesh(step_edge, step_in)
    sv = sample_map(s, pts)
    wts = chain_weights(sv, bones, parent, blend, parent_blend)
    vw = np.array([piece.to_rig(x, y) for x, y in pts])
    h, w = piece.mask.shape
    uv = np.stack([pts[:, 0] / w, pts[:, 1] / h], 1)
    R.images[img] = Image.fromarray(piece.rgba)
    R.mesh(slot, img, img, vw, uv, tris, nh, wts)
    return len(pts), len(tris)


def add_rigid_piece(R, piece, slot, img, bone, att=None):
    R.images[img] = Image.fromarray(piece.rgba)
    h, w = piece.mask.shape
    cx, cy = piece.to_rig(w / 2, h / 2)
    R.region(slot, att or img, img, bone, cx, cy)


# ---------------------------------------------------------------- tư thế
class Pose:
    def __init__(self):
        self.t = {}      # xương -> [dx, dy, rot, sx, sy]
        self.att = {}    # slot -> tên hình (None = trống)
        self.alpha = {}  # slot -> độ đậm
        self.feet = {}   # bên -> (x, y, góc) đích bàn chân trong ik_space
        self.chain_base = {}  # xương chuỗi -> góc nền (lò xo đuổi theo)

    def _g(self, b):
        return self.t.setdefault(b, [0.0, 0.0, 0.0, 1.0, 1.0])

    def rot(self, b, a):
        self._g(b)[2] += a

    def move(self, b, dx, dy):
        g = self._g(b)
        g[0] += dx
        g[1] += dy

    def scale(self, b, sx, sy=None):
        g = self._g(b)
        g[3] *= sx
        g[4] *= sx if sy is None else sy


def fk(R, P):
    """ma trận thế giới 3x3 (y lên) của từng xương."""
    world = {}
    for b in R.bones:
        name = b["name"]
        dx, dy, r, sx, sy = P.t.get(name, (0, 0, 0, 1, 1))
        if b["parent"] is None:
            lx, ly = b["wx"] + dx, b["wy"] + dy
            Pm = np.eye(3)
        else:
            px, py = R.bw(b["parent"])
            lx, ly = b["wx"] - px + dx, b["wy"] - py + dy
            Pm = world[b["parent"]]
        c, s = math.cos(math.radians(r)), math.sin(math.radians(r))
        M = np.array([[c * sx, -s * sy, lx], [s * sx, c * sy, ly], [0, 0, 1]])
        world[name] = Pm @ M
    return world


def wangle(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


def solve_legs(R, P, world):
    """IK hai đoạn: đùi, cẳng theo đích bàn chân P.feet (toạ độ trong ik_space), bàn chân giữ góc đích."""
    for side, leg in R.legs.items():
        if side not in P.feet:
            continue
        th, sh, ft = leg[:3]
        space = leg[3] if len(leg) > 3 else R.ik_space
        S = world[space] if space else np.eye(3)
        Si = np.linalg.inv(S)
        tx, ty, fa = P.feet[side]
        H0, K0, A0 = np.array(R.bw(th)), np.array(R.bw(sh)), np.array(R.bw(ft))
        L1, L2 = np.linalg.norm(K0 - H0), np.linalg.norm(A0 - K0)
        Hw = (Si @ world[th])[:2, 2]
        T = np.array([tx, ty])
        D = T - Hw
        d = min(L1 + L2 - 1e-3, max(abs(L1 - L2) + 1e-3, np.linalg.norm(D)))
        a = math.atan2(D[1], D[0])
        alpha = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
        cross = (A0 - H0)[0] * (K0 - H0)[1] - (A0 - H0)[1] * (K0 - H0)[0]
        sign = 1 if cross > 0 else -1
        phi1 = a + sign * alpha
        knee = Hw + L1 * np.array([math.cos(phi1), math.sin(phi1)])
        Tc = Hw + d * np.array([math.cos(a), math.sin(a)])
        phi2 = math.atan2(*(Tc - knee)[::-1])
        th0 = math.atan2(*(K0 - H0)[::-1])
        sh0 = math.atan2(*(A0 - K0)[::-1])
        parent_rot = wangle(Si @ world[R.bones[R.bi[th]]["parent"]])
        thigh_w = math.degrees(phi1 - th0)
        shin_w = math.degrees(phi2 - sh0)
        P._g(th)[2] = thigh_w - parent_rot
        P._g(sh)[2] = shin_w - thigh_w
        P._g(ft)[2] = fa - shin_w


class Springs:
    """chuỗi mềm: điểm khớp đuổi theo vị trí động học (dáng nền) bằng lò xo tắt dần, giữ độ dài đoạn."""

    def __init__(self, R, chains):
        self.R = R
        self.chains = chains  # tên -> {"bones": [...], "k": [...], "damp": d}
        self.state = {}

    def targets(self, world, bones, tipw):
        pts = [world[b][:2, 2].copy() for b in bones]
        pts.append((world[bones[-1]] @ np.array([tipw[0], tipw[1], 1]))[:2])
        return pts

    def step(self, P, dt):
        R = self.R
        world = fk(R, P)
        for name, c in self.chains.items():
            bones = c["bones"]
            tip = c["tip"]  # đầu chót theo xương cuối (toạ độ xương)
            tg = self.targets(world, bones, tip)
            st = self.state.get(name)
            if st is None:
                st = {"p": [p.copy() for p in tg], "v": [np.zeros(2) for _ in tg]}
                self.state[name] = st
            p, v = st["p"], st["v"]
            p[0] = tg[0]
            sub = 4
            for _ in range(sub):
                h = dt / sub
                for i in range(1, len(p)):
                    k = c["k"][min(i - 1, len(c["k"]) - 1)]
                    damp = c.get("damp", 0.55) * 2 * math.sqrt(k)
                    acc = k * (tg[i] - p[i]) - damp * v[i]
                    v[i] = v[i] + acc * h
                    p[i] = p[i] + v[i] * h
                for i in range(1, len(p)):  # giữ độ dài đoạn
                    L = np.linalg.norm(tg[i] - tg[i - 1])
                    dvec = p[i] - p[i - 1]
                    n_ = np.linalg.norm(dvec)
                    if n_ > 1e-6:
                        p[i] = p[i - 1] + dvec / n_ * L
            # góc xương từ điểm mô phỏng
            for i, b in enumerate(bones):
                Mt = world[b]
                ang_t = math.degrees(math.atan2(*(tg[i + 1] - tg[i])[::-1]))
                ang_s = math.degrees(math.atan2(*(p[i + 1] - p[i])[::-1]))
                dlt = (ang_s - ang_t + 180) % 360 - 180
                lim = c.get("maxang")  # chuỗi không được văng quá góc này so với dáng động học (bờm dài)
                if lim:
                    dlt = max(-lim, min(lim, dlt))
                P._g(b)[2] += dlt
                world = fk(R, P)  # xương sau đi theo góc mới của xương trước
                tg = self.targets(world, bones, tip)


def bake(R, clip, springs_cfg):
    """clip: {"dur", "loop", "fn": f(t, P)}; trả list Pose mỗi khung (FPS)."""
    dur, loop = clip["dur"], clip.get("loop", False)
    n = max(2, int(round(dur * FPS)) + (0 if loop else 1))
    dt = 1.0 / FPS
    sp = Springs(R, springs_cfg)

    def one(t):
        P = Pose()
        clip["fn"](t, P)
        world = fk(R, P)
        if R.legs and P.feet:
            solve_legs(R, P, world)
        return P

    if loop:  # chạy nóng 2 vòng để lò xo vào nhịp
        for i in range(2 * n):
            sp.step(one((i % n) * dt), dt)
    else:
        P0 = one(0)
        for _ in range(FPS):
            sp.step(copy.deepcopy(P0), dt)
    out = []
    for i in range(n):
        t = min(dur, i * dt)
        P = one(t)
        sp.step(P, dt)
        if clip.get("post"):  # hậu kỳ sau lò xo (tiến hóa: khung cuối khớp khung đầu clip đứng dạng sau)
            clip["post"](t, P)
        out.append(P)
    if loop:  # khép vòng: 6 khung cuối hoà dần về khung đầu (chuỗi mềm)
        m = min(6, n // 3)
        for j in range(m):
            w = (j + 1) / (m + 1)
            a, b = out[n - m + j], out[0]
            for bone in set(a.t) | set(b.t):
                ta, tb = a._g(bone), b._g(bone)
                for q in range(5):
                    ta[q] = ta[q] * (1 - w) + tb[q] * w
    return out


# ---------------------------------------------------------------- khoá
def rdp(ts, vs, tol):
    keep = [0, len(ts) - 1]

    def rec(i, j):
        if j <= i + 1:
            return
        t0, t1, v0, v1 = ts[i], ts[j], vs[i], vs[j]
        best, bk = -1, -1
        for k in range(i + 1, j):
            vi = v0 + (v1 - v0) * (ts[k] - t0) / max(1e-9, t1 - t0)
            e = abs(vs[k] - vi)
            if e > best:
                best, bk = e, k
        if best > tol:
            keep.append(bk)
            rec(i, bk)
            rec(bk, j)

    rec(0, len(ts) - 1)
    return sorted(set(keep))


def to_timelines(R, frames, dur):
    """khung đã nướng -> khoá Spine 4.2 (thẳng giữa các khoá giữ lại)."""
    ts = [min(dur, i / FPS) for i in range(len(frames))]
    bones = {}
    names = sorted({b for P in frames for b in P.t})
    for b in names:
        vals = np.array([P.t.get(b, [0, 0, 0, 1, 1]) for P in frames], float)
        tl = {}
        if np.abs(vals[:, 2]).max() > 0.01:
            r = vals[:, 2]
            keep = sorted(set(rdp(ts, r, 0.08)))
            tl["rotate"] = [{"time": round(ts[i], 4), "value": round(float(r[i]), 3)} for i in keep]
        if np.abs(vals[:, :2]).max() > 0.01:
            keep = sorted(set(rdp(ts, vals[:, 0], 0.08)) | set(rdp(ts, vals[:, 1], 0.08)))
            tl["translate"] = [{"time": round(ts[i], 4), "x": round(float(vals[i, 0]), 3), "y": round(float(vals[i, 1]), 3)}
                               for i in keep]
        if np.abs(vals[:, 3:] - 1).max() > 0.001:
            keep = sorted(set(rdp(ts, vals[:, 3], 0.002)) | set(rdp(ts, vals[:, 4], 0.002)))
            tl["scale"] = [{"time": round(ts[i], 4), "x": round(float(vals[i, 3]), 4), "y": round(float(vals[i, 4]), 4)}
                           for i in keep]
        if tl:
            bones[b] = tl
    slots = {}
    for s in R.slots:
        name = s["name"]
        atts = [P.att.get(name, "__d") for P in frames]
        if any(a != "__d" for a in atts):
            seq, last = [], object()
            for i, a in enumerate(atts):
                a = s["att"] if a == "__d" else a
                if a != last:
                    seq.append({"time": round(ts[i], 4), "name": a})
                    last = a
            slots.setdefault(name, {})["attachment"] = seq
        al = np.array([P.alpha.get(name, 1.0) for P in frames])
        if np.abs(al - 1).max() > 0.002:
            keep = rdp(ts, al, 0.006)
            slots.setdefault(name, {})["alpha"] = [{"time": round(ts[i], 4), "value": round(float(al[i]), 4)} for i in keep]
    return {"bones": bones, "slots": slots}


# ---------------------------------------------------------------- xuất
def bone_local(R):
    out = [{"name": "root"}]
    for b in R.bones:
        if b["name"] == "root":
            continue
        px, py = R.bw(b["parent"]) if b["parent"] else (0.0, 0.0)
        out.append({"name": b["name"], "parent": b["parent"] or "root", "x": round(b["wx"] - px, 3),
                    "y": round(b["wy"] - py, 3), "length": 12})
    return out


def spine_json(R, anims):
    bones = bone_local(R)
    bidx = {b["name"]: i for i, b in enumerate(bones)}
    skin = {}
    for s in R.slots:
        d = {}
        for an, a in R.atts[s["name"]].items():
            if a["type"] == "region":
                d[an] = {"path": a["path"], "x": round(a["x"], 3), "y": round(a["y"], 3), "width": round(a["width"], 2),
                         "height": round(a["height"], 2)}
                if abs(a.get("rot", 0)) > 1e-3:
                    d[an]["rotation"] = round(a["rot"], 3)
            else:
                verts = []
                for (X, Y), ws in zip(a["vw"], a["weights"]):
                    verts.append(len(ws))
                    for b, w in ws:
                        bx, by = R.bw(b)
                        verts += [bidx[b], round(float(X - bx), 3), round(float(Y - by), 3), round(float(w), 4)]
                im = R.images[a["path"]]
                d[an] = {"type": "mesh", "path": a["path"], "uvs": [round(float(x), 6) for x in a["uv"].flatten()],
                         "triangles": [int(i) for i in a["tris"].flatten()], "vertices": verts, "hull": a["nh"],
                         "width": im.width, "height": im.height}
        skin[s["name"]] = d
    slots = []
    for s in R.slots:
        e = {"name": s["name"], "bone": s["bone"]}
        if s["att"]:
            e["attachment"] = s["att"]
        slots.append(e)
    conv = copy.deepcopy(anims)
    for a in conv.values():
        for tls in a.get("bones", {}).values():
            for kind, frames in tls.items():
                _convert_timeline(kind, frames)
        for st in a.get("slots", {}).values():
            if "alpha" in st:
                _convert_timeline("alpha", st["alpha"])
    return {"skeleton": {"hash": R.name, "spine": "4.2.0", "x": -300, "y": -40, "width": 900, "height": 700,
                         "images": "./images/", "fps": FPS},
            "bones": bones, "slots": slots, "skins": [{"name": "default", "attachments": skin}], "animations": conv}


def write_atlas(R, out_dir):
    aw, ah, place = pack(R.images, padding=2)
    atlas = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
    lines = [f"{R.name}.png", f"size: {aw},{ah}", "format: RGBA8888", "filter: Linear,Linear", "repeat: none"]
    for n, (x, y, w, h) in place.items():
        atlas.paste(R.images[n], (x, y))
        lines += [n, "  rotate: false", f"  xy: {x}, {y}", f"  size: {w}, {h}", f"  orig: {w}, {h}", "  offset: 0, 0",
                  "  index: -1"]
    atlas.save(os.path.join(out_dir, R.name + ".png"))
    open(os.path.join(out_dir, R.name + ".atlas"), "w").write("\n".join(lines) + "\n")
    return aw, ah


# ---------------------------------------------------------------- dựng hình (soi)
def slot_world_verts(R, world, slot, an):
    a = R.atts[slot][an]
    if a["type"] == "region":
        M = world[a["bone"]] if "bone" in a else world[[s for s in R.slots if s["name"] == slot][0]["bone"]]
        hw, hh = a["width"] / 2, a["height"] / 2
        c, s_ = math.cos(math.radians(a.get("rot", 0))), math.sin(math.radians(a.get("rot", 0)))
        corners = [(-hw, hh), (hw, hh), (hw, -hh), (-hw, -hh)]
        loc = np.array([[a["x"] + x * c - y * s_, a["y"] + x * s_ + y * c, 1] for x, y in corners]).T
        return (M @ loc)[:2].T
    out = np.zeros((len(a["vw"]), 2))
    for v, ((X, Y), ws) in enumerate(zip(a["vw"], a["weights"])):
        for b, w in ws:
            bx, by = R.bw(b)
            out[v] += w * (world[b] @ np.array([X - bx, Y - by, 1]))[:2]
    return out


def render(R, P, k, box, bg=(250, 246, 236)):
    Wb, Hb, ox, oy = box
    canvas = np.full((Hb, Wb, 3), bg, np.float32)
    world = fk(R, P)
    for s in R.slots:
        an = P.att.get(s["name"], s["att"])
        al_s = P.alpha.get(s["name"], 1.0)
        if not an or al_s <= 0.003:
            continue
        a = R.atts[s["name"]][an]
        tex = np.array(R.images[a["path"]])
        vs = slot_world_verts(R, world, s["name"], an)
        X, Y = ox + vs[:, 0] * k, oy - vs[:, 1] * k
        h, w = tex.shape[:2]
        if a["type"] == "region":
            src = np.float32([[0, 0], [w, 0], [w, h]])
            dst = np.float32([[X[0], Y[0]], [X[1], Y[1]], [X[2], Y[2]]])
            M = cv2.getAffineTransform(src, dst)
            wp = cv2.warpAffine(tex, M, (Wb, Hb), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                                borderValue=(0, 0, 0, 0)).astype(np.float32)
            al = wp[:, :, 3:4] / 255.0 * al_s
            canvas = canvas * (1 - al) + wp[:, :, :3] * al
            continue
        uvp = a["uv"] * [w, h]
        for tri in a["tris"]:
            src = np.float32(uvp[tri])
            dst = np.float32(np.stack([X[tri], Y[tri]], 1))
            x0, y0 = np.floor(dst.min(0)).astype(int) - 1
            x1, y1 = np.ceil(dst.max(0)).astype(int) + 2
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, Wb), min(y1, Hb)
            if x1 <= x0 or y1 <= y0:
                continue
            M = cv2.getAffineTransform(src, dst - np.float32([x0, y0]))
            patch = cv2.warpAffine(tex, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(0, 0, 0, 0)).astype(np.float32)
            mk = np.zeros((y1 - y0, x1 - x0), np.float32)
            c = dst.mean(0)
            grown = c + (dst - c) * 1.04 + np.sign(dst - c) * 0.4
            cv2.fillConvexPoly(mk, np.round((grown - [x0, y0]) * 4).astype(np.int32), 1.0, cv2.LINE_AA, 2)
            al = (patch[:, :, 3] / 255.0 * mk * al_s)[:, :, None]
            canvas[y0:y1, x0:x1] = canvas[y0:y1, x0:x1] * (1 - al) + patch[:, :, :3] * al
    return canvas.astype(np.uint8)


def sheet(R, clips, baked, out_dir, H, fh=300, n=9, gif=True):
    k = fh / (1.8 * H)
    Wb = int(2.4 * H * k)
    box = (Wb, fh, int(0.62 * H * k), int(fh - 0.12 * H * k))
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    rows = []
    for name, frames in baked.items():
        dur = clips[name]["dur"]
        idx = [round(i * (len(frames) - 1) / (n - 1)) for i in range(n)]
        imgs = [render(R, frames[i], k, box) for i in idx]
        row = Image.fromarray(np.concatenate(imgs, 1))
        d = ImageDraw.Draw(row)
        d.text((6, 4), f"{name} ({dur:.2f}s)", fill=(43, 33, 24), font=font)
        for j, i in enumerate(idx):
            d.text((j * Wb + Wb - 40, fh - 16), f"{i / FPS:.2f}", fill=(120, 100, 80), font=font)
        rows.append(np.array(row))
        if gif:
            gk = k * 1.2
            gbox = (int(Wb * 1.2), int(fh * 1.2), int(box[2] * 1.2), int(box[3] * 1.2))
            g = [Image.fromarray(render(R, frames[i], gk, gbox)) for i in range(0, len(frames), 2)]
            g[0].save(os.path.join(out_dir, f"anim_{name}.gif"), save_all=True, append_images=g[1:],
                      duration=int(2000 / FPS), loop=0)
    Image.fromarray(np.concatenate(rows, 0)).save(os.path.join(out_dir, "khung.png"))


def mesh_debug(R, out_dir, scale=2.0):
    """ảnh soi lưới + màu trọng số theo xương ở dáng gốc."""
    P = Pose()
    world = fk(R, P)
    xs, ys = [], []
    for s in R.slots:
        if s["att"]:
            v = slot_world_verts(R, world, s["name"], s["att"])
            xs += list(v[:, 0])
            ys += list(v[:, 1])
    x0, x1, y0, y1 = min(xs) - 20, max(xs) + 20, min(ys) - 20, max(ys) + 20
    Wd, Hd = int((x1 - x0) * scale), int((y1 - y0) * scale)
    box = (Wd, Hd, int(-x0 * scale), int(y1 * scale))
    img = Image.fromarray(render(R, P, scale, box, bg=(200, 200, 200))).convert("RGB")
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(3)
    col = {b["name"]: tuple(int(c) for c in rng.integers(40, 230, 3)) for b in R.bones}
    for s in R.slots:
        if not s["att"]:
            continue
        a = R.atts[s["name"]][s["att"]]
        if a["type"] != "mesh":
            continue
        v = slot_world_verts(R, world, s["name"], s["att"])
        X, Y = box[2] + v[:, 0] * scale, box[3] - v[:, 1] * scale
        for tri in a["tris"]:
            d.polygon([(X[i], Y[i]) for i in tri], outline=(60, 60, 60))
        for i, ws in enumerate(a["weights"]):
            c = np.zeros(3)
            for b, w in ws:
                c += w * np.array(col[b])
            d.ellipse([X[i] - 2.5, Y[i] - 2.5, X[i] + 2.5, Y[i] + 2.5], fill=tuple(int(q) for q in c))
    for b in R.bones:
        if b["name"].startswith("fx") or b["parent"] is None:
            continue
        x, y = box[2] + b["wx"] * scale, box[3] - b["wy"] * scale
        px, py = R.bw(b["parent"])
        d.line([box[2] + px * scale, box[3] - py * scale, x, y], fill=(255, 0, 160), width=2)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(255, 0, 160), width=2)
    img.save(os.path.join(out_dir, "luoi.png"))


def idle_height(R, P):
    world = fk(R, P)
    top = 0.0
    for s in R.slots:
        an = P.att.get(s["name"], s["att"])
        if not an or s["name"] in R.fx_slots or s["name"].endswith("shadow"):
            continue
        top = max(top, float(slot_world_verts(R, world, s["name"], an)[:, 1].max()))
    return top


def point_world(R, P, name):
    b, x, y = R.points[name]
    return (fk(R, P)[b] @ np.array([x, y, 1]))[:2]


def merge_next(A, B, prefix="n_", parent="root", scale_bone="evo"):
    """gộp rig dạng sau B vào A (tiến hóa): xương B thêm tiền tố, gốc B treo dưới xương scale_bone; slot B vẽ sau slot A."""
    M = copy.deepcopy(A)
    M.name = A.name
    M.bone(scale_bone, parent, 0.0, 0.0)
    for b in B.bones:
        if b["name"] == "root":
            continue
        M.bone(prefix + b["name"], prefix + b["parent"] if b["parent"] and b["parent"] != "root" else scale_bone,
               b["wx"], b["wy"])
    for img, im in B.images.items():
        M.images[prefix + img] = im
    for s in B.slots:
        M.slot(prefix + s["name"], prefix + s["bone"], prefix + s["att"] if s["att"] else None, fx=s["name"] in B.fx_slots)
        for an, a in B.atts[s["name"]].items():
            a2 = copy.deepcopy(a)
            a2["path"] = prefix + a["path"]
            if "bone" in a2:
                a2["bone"] = prefix + a2["bone"]
            if a2["type"] == "mesh":
                a2["weights"] = [[(prefix + b, w) for b, w in ws] for ws in a2["weights"]]
            M.atts[prefix + s["name"]][prefix + an] = a2
    return M


def export(R, clips, baked, out_dir, res_dir, game, H, gif=True):
    os.makedirs(out_dir, exist_ok=True)
    anims = {name: to_timelines(R, frames, clips[name]["dur"]) for name, frames in baked.items()}
    for name in anims:  # khoá ở thời điểm cuối để độ dài clip đúng
        anims[name]["bones"].setdefault("root", {})["translate"] = [{"time": 0, "x": 0, "y": 0},
                                                                    {"time": round(clips[name]["dur"], 4), "x": 0, "y": 0}]
    sk = spine_json(R, anims)
    json.dump(sk, open(os.path.join(out_dir, R.name + ".json"), "w"))
    aw, ah = write_atlas(R, out_dir)
    json.dump(game, open(os.path.join(out_dir, R.name + "_game.json"), "w"), indent=1, ensure_ascii=False)
    os.makedirs(res_dir, exist_ok=True)
    atomik.convert(os.path.join(out_dir, R.name + ".json"), os.path.join(out_dir, R.name + ".atlas"),
                   os.path.join(res_dir, R.name + ".atomik"), R.name, game)
    sheet(R, clips, baked, out_dir, H, gif=gif)
    mesh_debug(R, out_dir)
    return aw, ah
