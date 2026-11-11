# -*- coding: utf-8 -*-
"""Khung xương, slot, hình (mảnh cứng, lưới có trọng số, mặt nạ cắt) cho thư viện quai.

Toạ độ rig: pixel atlas, x sang phải, y LÊN, gốc ở chân (giữa hai chân trên mặt đất: game lấy gốc này làm tâm bóng), con nhìn
sang PHẢI. Xương lưu như Spine (vị trí, góc, tỉ lệ so với cha); Sk tự tính ma trận thế giới dáng gốc nên:
  - đặt xương bằng toạ độ thế giới được (the_gioi=True), chuỗi xương từ danh sách khớp (chuoi);
  - gắn lưới: toạ độ gắn của mỗi đỉnh với mỗi xương = nghịch đảo ma trận thế giới của xương nhân toạ độ thế giới của đỉnh, đúng
    cả khi xương (hay cha của nó) có tỉ lệ khác 1, lật âm, xoay (lỗi đã gặp ở Hải Long: hàm tỉ lệ 0,86 phải chia toạ độ gắn).
Ảnh mảnh đặt vào thế giới bằng Dat (điểm neo trên ảnh -> điểm rig, góc, tỉ lệ, lật).
"""
import math

import numpy as np

ZERO = (0.0, 0.0, 0.0, 1.0, 1.0)


def mat(x, y, r, sx=1.0, sy=1.0):
    c, s = math.cos(math.radians(r)), math.sin(math.radians(r))
    return np.array([[c * sx, -s * sy, x], [s * sx, c * sy, y], [0.0, 0.0, 1.0]])


def goc_mat(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


class Pose:
    """tư thế một khung: lệch so với dáng gốc như khoá Spine (xoay cộng, dời cộng, tỉ lệ nhân), độ đậm slot, hình trong slot.
    Cùng cách gọi với longrig.Pose (rot, move, scale, alpha, att) để chép clip từ beast.py dễ."""
    __slots__ = ("t", "alpha", "att")

    def __init__(self):
        self.t = {}      # xương -> [dx, dy, dgóc, sx, sy]
        self.alpha = {}  # slot -> độ đậm 0..1
        self.att = {}    # slot -> tên hình (None = trống)

    def _g(self, b):
        g = self.t.get(b)
        if g is None:
            g = self.t[b] = [0.0, 0.0, 0.0, 1.0, 1.0]
        return g

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

    def copy(self):
        p = Pose()
        p.t = {k: list(v) for k, v in self.t.items()}
        p.alpha = dict(self.alpha)
        p.att = dict(self.att)
        return p


class Dat:
    """đặt ảnh mảnh (w×h px, y xuống) vào thế giới rig: điểm neo (tỉ lệ ảnh, hoặc px nếu neo_px) tới (x, y) rig; góc (độ, dương
    ngược kim); ti: tỉ lệ (số hoặc (sx, sy)); lat: lật ngang (dùng lại một hình cho hai bên)."""

    def __init__(self, x, y, goc=0.0, ti=1.0, neo=(0.5, 0.5), lat=False, neo_px=False):
        self.x, self.y, self.goc, self.lat, self.neo, self.neo_px = float(x), float(y), float(goc), bool(lat), neo, neo_px
        self.sx, self.sy = (ti, ti) if np.isscalar(ti) else ti

    def ra(self, pts, w, h):
        """toạ độ ảnh (N, 2) -> thế giới rig (N, 2)."""
        P = np.asarray(pts, float).reshape(-1, 2)
        ax, ay = (self.neo if self.neo_px else (self.neo[0] * w, self.neo[1] * h))
        lx = (P[:, 0] - ax) * self.sx * (-1 if self.lat else 1)
        ly = -(P[:, 1] - ay) * self.sy
        c, s = math.cos(math.radians(self.goc)), math.sin(math.radians(self.goc))
        return np.stack([self.x + c * lx - s * ly, self.y + s * lx + c * ly], 1)

    def mot(self, p, w, h):
        return self.ra([p], w, h)[0]


class Sk:
    def __init__(self, ten):
        self.ten = ten
        self.bones = []      # dict(name, parent, x, y, rot, sx, sy, length, noScale)
        self.bi = {}
        self.W0 = {}         # ma trận thế giới dáng gốc 3x3
        self.slots = []      # dict(name, bone, att, alpha)
        self.si = {}
        self.atts = {}       # slot -> {tên hình: spec}
        self.images = {}     # tên ảnh -> PIL RGBA (vào atlas)
        self.points = {}     # tên điểm -> (xương, x, y theo xương)
        self.events = {}     # tên sự kiện -> mô tả
        self.luoi = {}       # (slot, hình) -> Luoi (soi luoi.png)
        self.info = {}       # tuỳ dùng

    # ---------------------------------------------------------------- xương
    def _wp_eff(self, b, Wp):
        if not b.get("noScale"):
            return Wp
        A = Wp.copy()
        n0, n1 = math.hypot(A[0, 0], A[1, 0]), math.hypot(A[0, 1], A[1, 1])
        if n0 > 1e-9:
            A[0, 0] /= n0
            A[1, 0] /= n0
        if n1 > 1e-9:
            A[0, 1] /= n1
            A[1, 1] /= n1
        return A

    def _world(self, b, L, Wp):
        """như AtomikPose.World: noScale bỏ tỉ lệ của cha ở phần quay, vị trí vẫn theo cha đủ tỉ lệ."""
        if Wp is None:
            return L
        A = self._wp_eff(b, Wp)
        W = np.eye(3)
        W[:2, :2] = A[:2, :2] @ L[:2, :2]
        W[:2, 2] = (Wp @ np.array([L[0, 2], L[1, 2], 1.0]))[:2]
        return W

    def xuong(self, ten, cha=None, x=0.0, y=0.0, goc=0.0, dai=0.0, sx=1.0, sy=1.0, the_gioi=False, khong_ti_le=False):
        """thêm xương. the_gioi=True: (x, y) là toạ độ thế giới rig và goc là góc thế giới của trục x xương (tỉ lệ vẫn là tỉ lệ
        riêng). khong_ti_le: không nhận tỉ lệ của cha (như noScale; tránh dùng khi có clip co cả con)."""
        if ten in self.bi:
            raise ValueError(f"xương {ten} đã có")
        if cha is not None and cha not in self.bi:
            raise ValueError(f"xương {ten}: chưa có cha {cha}")
        b = {"name": ten, "parent": cha, "length": float(dai), "sx": float(sx), "sy": float(sy), "noScale": bool(khong_ti_le)}
        if the_gioi and cha is not None:
            Wp = self.W0[cha]
            A = self._wp_eff(b, Wp)
            lp = np.linalg.solve(Wp, np.array([x, y, 1.0]))
            d = np.linalg.solve(A[:2, :2], np.array([math.cos(math.radians(goc)), math.sin(math.radians(goc))]))
            b["x"], b["y"], b["rot"] = float(lp[0]), float(lp[1]), math.degrees(math.atan2(d[1], d[0]))
        else:
            b["x"], b["y"], b["rot"] = float(x), float(y), float(goc)
        self.bi[ten] = len(self.bones)
        self.bones.append(b)
        L = mat(b["x"], b["y"], b["rot"], b["sx"], b["sy"])
        self.W0[ten] = self._world(b, L, self.W0[cha] if cha else None)
        return ten

    def chuoi(self, ten, cha, diem, khong_ti_le=False, ten_rieng=None):
        """chuỗi xương qua các khớp thế giới diem = [J0, J1, ..., Jn] (gốc → ngọn): đốt i đặt ở Ji, trục x chĩa tới J(i+1), dài
        |J(i+1) - Ji|. Tên ten0..ten(n-1) (hoặc ten_rieng). Trả danh sách tên."""
        J = np.asarray(diem, float)
        names = ten_rieng or [f"{ten}{i}" for i in range(len(J) - 1)]
        prev = cha
        for i in range(len(J) - 1):
            d = J[i + 1] - J[i]
            self.xuong(names[i], prev, J[i][0], J[i][1], math.degrees(math.atan2(d[1], d[0])), float(np.hypot(*d)), the_gioi=True,
                       khong_ti_le=khong_ti_le and i == 0)
            prev = names[i]
        return names

    def goc_tg(self, b):
        """vị trí và góc thế giới dáng gốc của xương."""
        W = self.W0[b]
        return float(W[0, 2]), float(W[1, 2]), goc_mat(W)

    def the_gioi(self, P=None):
        """ma trận thế giới 3x3 của mọi xương ở tư thế P (None: dáng gốc)."""
        if P is None:
            return dict(self.W0)
        W = {}
        t = P.t
        for b in self.bones:
            nm = b["name"]
            dx, dy, dr, psx, psy = t.get(nm, ZERO)
            L = mat(b["x"] + dx, b["y"] + dy, b["rot"] + dr, b["sx"] * psx, b["sy"] * psy)
            W[nm] = self._world(b, L, W[b["parent"]] if b["parent"] else None)
        return W

    def cap_nhat(self, W, ten, P):
        """tính lại ma trận thế giới của các xương ten (theo thứ tự cha trước) ở tư thế P, dùng W của cha có sẵn."""
        for nm in ten:
            b = self.bones[self.bi[nm]]
            dx, dy, dr, psx, psy = P.t.get(nm, ZERO)
            L = mat(b["x"] + dx, b["y"] + dy, b["rot"] + dr, b["sx"] * psx, b["sy"] * psy)
            W[nm] = self._world(b, L, W[b["parent"]] if b["parent"] else None)
        return W

    # ---------------------------------------------------------------- slot, hình
    def slot(self, ten, xuong, hinh=None, an=False, truoc=None):
        """thêm slot (thứ tự gọi = thứ tự vẽ, sau → trước; truoc=tên slot: chèn ngay trước slot đó). an=True: ẩn mặc định (mí
        mắt, lưỡi, hình đổi): clip bật bằng độ đậm."""
        if xuong not in self.bi:
            raise ValueError(f"slot {ten}: chưa có xương {xuong}")
        s = {"name": ten, "bone": xuong, "att": hinh, "alpha": 0.0 if an else 1.0}
        if truoc is not None:
            self.slots.insert(next(i for i, q in enumerate(self.slots) if q["name"] == truoc), s)
        else:
            self.slots.append(s)
        self.si = {q["name"]: i for i, q in enumerate(self.slots)}
        self.atts.setdefault(ten, {})
        return ten

    def anh(self, ten, im):
        self.images[ten] = im.convert("RGBA")
        return ten

    def _slot(self, slot):
        return self.slots[self.si[slot]]

    def manh(self, slot, anh, dat, ten=None, xuong=None):
        """mảnh cứng (region) đặt bằng Dat, bám xương của slot (hoặc xuong). Xương có tỉ lệ lệch hay lật thì tự thành lưới 4 đỉnh."""
        im = self.images[anh]
        b = xuong or self._slot(slot)["bone"]
        W = self.W0[b]
        w, h = im.width, im.height
        C = dat.ra([[0, 0], [w, 0], [w, h], [0, h], [w / 2, h / 2]], w, h)
        A = W[:2, :2]
        n0, n1 = math.hypot(A[0, 0], A[1, 0]), math.hypot(A[0, 1], A[1, 1])
        shear = abs(A[0, 0] * A[0, 1] + A[1, 0] * A[1, 1]) / max(1e-9, n0 * n1)
        if abs(n0 - n1) < 1e-6 * max(1, n0) and shear < 1e-6 and np.linalg.det(A) > 0:
            lp = np.linalg.solve(W, np.array([C[4, 0], C[4, 1], 1.0]))
            ex = C[1] - C[0]
            rot = math.degrees(math.atan2(ex[1], ex[0])) - goc_mat(W)
            if dat.lat:  # lật: hướng cạnh trên đảo, dùng scaleX âm
                rot = math.degrees(math.atan2(-ex[1], -ex[0])) - goc_mat(W)
            spec = {"type": "region", "path": anh, "x": float(lp[0]), "y": float(lp[1]), "rotation": rot,
                    "scaleX": (-1 if dat.lat else 1) * dat.sx / n0, "scaleY": dat.sy / n0, "width": w, "height": h, "bone": b}
            self.atts[slot][ten or anh] = spec
        else:
            from .luoi import luoi_o
            L = luoi_o(w, h, 2, 2)
            self.luoi_gan(slot, anh, L, [{b: 1.0}] * 4, dat=dat, ten=ten)
        return ten or anh

    def luoi_gan(self, slot, anh, L, trongso, dat=None, the_gioi=None, ten=None):
        """lưới có trọng số: L (Luoi, toạ độ ảnh), trongso (list dict {xương: w} mỗi đỉnh), đặt bằng dat hoặc cho thẳng toạ độ
        thế giới từng đỉnh (the_gioi, (N, 2)). Toạ độ gắn tính bằng nghịch đảo ma trận thế giới dáng gốc của từng xương."""
        im = self.images[anh]
        V = np.asarray(the_gioi, float) if the_gioi is not None else dat.ra(L.pts, im.width, im.height)
        if len(trongso) != L.n:
            raise ValueError(f"{slot}/{ten or anh}: {len(trongso)} trọng số cho {L.n} đỉnh")
        inv = {}
        verts = []
        for i, d in enumerate(trongso):
            row = []
            for b, w in d.items():
                if b not in self.bi:
                    raise ValueError(f"{slot}: trọng số dùng xương lạ {b}")
                if b not in inv:
                    inv[b] = np.linalg.inv(self.W0[b])
                lp = inv[b] @ np.array([V[i, 0], V[i, 1], 1.0])
                row.append((b, float(lp[0]), float(lp[1]), float(w)))
            verts.append(row)
        uv = L.pts / np.array([im.width, im.height], float)
        spec = {"type": "mesh", "path": anh, "uv": uv, "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V, "verts": verts,
                "width": im.width, "height": im.height}
        self.atts[slot][ten or anh] = spec
        self.luoi[(slot, ten or anh)] = L
        return ten or anh

    def cat(self, slot, den_slot, da_giac_tg):
        """mặt nạ cắt (Spine clipping): mọi hình từ slot kế sau slot này tới den_slot chỉ còn phần trong đa giác (LỒI, thế giới
        rig, bám xương của slot). Runtime game cắt trên CPU: chỉ bật khi cần (trồi, chìm)."""
        b = self._slot(slot)["bone"]
        inv = np.linalg.inv(self.W0[b])
        loc = [(inv @ np.array([x, y, 1.0]))[:2] for x, y in da_giac_tg]
        self.atts[slot]["cat"] = {"type": "clipping", "end": den_slot, "verts": [float(v) for p in loc for v in p]}
        self._slot(slot)["att"] = "cat"

    def diem(self, ten, xuong, x, y):
        """điểm đặt tên (thế giới rig dáng gốc) gắn vào xương: chỗ bắn, chỗ toé..."""
        lp = np.linalg.solve(self.W0[xuong], np.array([x, y, 1.0]))
        self.points[ten] = (xuong, float(lp[0]), float(lp[1]))

    def diem_tg(self, ten, W):
        b, x, y = self.points[ten]
        return (W[b] @ np.array([x, y, 1.0]))[:2]

    def su_kien(self, ten, mo_ta=""):
        self.events[ten] = mo_ta

    def tom_tat(self):
        nv = sum(len(a["verts"]) if a["type"] == "mesh" else (4 if a["type"] == "region" else 0) for s in self.atts.values() for a in s.values())
        nt = sum(len(a["tris"]) if a["type"] == "mesh" else (2 if a["type"] == "region" else 0) for s in self.atts.values() for a in s.values())
        return {"xuong": len(self.bones), "slot": len(self.slots), "dinh": nv, "tam_giac": nt}
