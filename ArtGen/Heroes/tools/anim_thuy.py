"""Đòn đánh (1_4) và chiêu cuối (1_6) viết lại cho các tướng đảo Thủy vẽ lại ngày 2026-11-06/07 (người dùng dặn 2026-11-07:
"animation các tướng đang hơi 1 kiểu (lộn xong đánh hoặc lao vào đánh), kết hợp bắn tia nước, gọi sóng thần, gọi cầu nước trên
đầu tướng địch rồi bắn nước xuống, đặc biệt 3 final boss phải thật đặc biệt và đẹp").

Dựng thẳng trên dạng ĐÃ NHẬP vào project (Assets/03 Art/Heroes/Resources/<dạng>/), không cần thư mục ghép của AolaRipper (lô Thủy
ghép ở máy ổ D). Gốc dựng lại luôn là bản ở commit BASE (anim_lo2 của máy D), nên chạy lại không cộng dồn:
- dáng nghỉ = khung đầu clip đứng; số mảnh theo idle_parts; cây khớp anim.json "anim_moi" (root, parent, pivot);
- giữ nguyên clip đứng 1_1, trúng đòn 1_2, bắn tia 1_5 (chỉ đổi số hình); viết lại 1_4 và 1_6 theo bảng CHOREO bên dưới;
- hình hiệu ứng: ảnh GPT trong inbox/<gói>/tai_ve (bảng FX), cắt nền trắng, thu về cỡ hiện lớn nhất (như AolaImport, kể cả
  OtherScale 0,7), xếp lại atlas (bỏ hình không clip nào dùng), ghi <dạng>_atlas.png, <dạng>.asset (sizes, uvs, shadow, source),
  <dạng>_anim.bytes. Unity tự nhập lại khi refresh.

Đòn ở xa (không lao): hình không có trong dáng đứng, tâm xa hơn 1,5 lần chiều cao về phía trước là hiệu ứng ở xa; trận kéo về thân
đối thủ sao cho "far_center" trùng thân (Body = chân − 0,45 chiều cao). Ở đây hình ở xa đặt theo toạ độ quanh thân đối thủ (đơn vị
chiều cao, x tới trước, y xuống), lệch trái tâm tối đa 1 lần chiều cao ("far_ramp"). Đòn không lao khai khung trúng ("hit") và
"stay" (AolaActor, 2026-11-07), nên thân bay nhảy được mà trận vẫn coi là đòn đứng tại chỗ; script in mô phỏng để kiểm.

Lưu ý máy ổ D: menu nhập tướng aola thường (không phải "nguồn mới hơn") sẽ nhập lại từ thư mục ghép bên đó và đè mất bản này;
nhập xong thì chạy lại script này.

    py -3 -I ArtGen/Heroes/tools/anim_thuy.py [mã dạng ...] [--sheet] [--dry]
      --sheet: tờ khung clip mới vào Temp/anim_thuy/<dạng>.png; --dry: không ghi vào Assets
"""
import gzip
import io
import json
import math
import os
import re
import sys
import time

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from aola_form import Form, PROJECT, RES  # noqa: E402

BASE = "4d7557b"  # lô Thủy nhập từ máy ổ D (anim_lo2.py)
# hình ở xa cách chân quá RAMP_END lần chiều cao được kéo trọn về đối thủ (anim.json "far_ramp", AolaActor.Render); giữa 1 và
# RAMP_END là đoạn kéo dần cho đạn bay. Tâm vùng xa F cách chân 2,8 lần nên hình quanh đối thủ đặt lệch trái tới 1 lần chiều cao.
RAMP_END = 1.8
HEROES = os.path.normpath(os.path.join(HERE, ".."))
CACHE = os.path.join(PROJECT, "Library", "anim_thuy_fx")
OUT_SHEET = os.path.join(PROJECT, "Temp", "anim_thuy")

# hình hiệu ứng: tên ngắn -> (gói, bước GPT, khoét lõi trắng)
FX = {
    "xoay": ("giot_suong_fx", "FX01", True), "song": ("giot_suong_fx", "FX02", False), "no": ("giot_suong_fx", "FX03", False),
    "giot": ("giot_suong_fx", "FX04", False), "lap": ("giot_suong_fx", "FX05", False), "than": ("giot_suong_fx", "FX07", False),
    "vong": ("giot_suong_fx", "FX08", True), "tia": ("giot_suong_fx", "FX09", False), "cau": ("tieu_y_fx", "FX10", False),
    "tia_bang": ("thuy_boss_fx", "FX11", False), "tia_xoay": ("thuy_boss_fx", "FX12", False),
    "tia_trieu": ("thuy_boss_fx", "FX13", False), "bang": ("thuy_boss_fx", "FX14", False), "am": ("thuy_boss_fx", "FX15", True),
    "cot": ("thuy_chieu_fx", "FX16", False), "giao": ("thuy_chieu_fx", "FX17", False), "ran": ("thuy_chieu_fx", "FX18", False),
    "xoay_dat": ("thuy_chieu_fx", "FX19", False),
}
# chưa có ảnh GPT thì dùng tạm ảnh khác (xoay, co giãn như nhau)
FX_FALLBACK = {"cot": "tia", "giao": "tia_bang", "ran": "than", "xoay_dat": "vong"}


# ---------------------------------------------------------------- ma trận (Flash: x' = a x + c y + tx, y' = b x + d y + ty)

def mul(p, q):
    a, b, c, d, tx, ty = p
    e, f, g, h, ux, uy = q
    return (a * e + c * f, b * e + d * f, a * g + c * h, b * g + d * h, a * ux + c * uy + tx, b * ux + d * uy + ty)


def T(x, y):
    return (1, 0, 0, 1, x, y)


def Rz(deg):
    r = math.radians(deg)
    cs, sn = math.cos(r), math.sin(r)
    return (cs, sn, -sn, cs, 0, 0)  # dương = theo chiều kim đồng hồ trên màn hình (y xuống)


def S(sx, sy):
    return (sx, 0, 0, sy, 0, 0)


def about(px, py, deg=0.0, sx=1.0, sy=1.0, dx=0.0, dy=0.0):
    """xoay, co giãn quanh (px, py) rồi dời (dx, dy)"""
    return mul(T(px + dx, py + dy), mul(Rz(deg), mul(S(sx, sy), T(-px, -py))))


def apply(m, x, y):
    return m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]


# ---------------------------------------------------------------- khoá và nội suy

def ease(e, t):
    if e == "lin":
        return t
    if e == "in":
        return t * t
    if e == "out":
        return 1 - (1 - t) * (1 - t)
    if e == "hold":
        return 0.0
    if e == "back":  # vọt quá rồi về
        s = 1.7
        t -= 1
        return t * t * ((s + 1) * t + s) + 1
    return t * t * (3 - 2 * t)


def val(keys, ch, f, default):
    """keys: [(khung, {kênh: giá trị, 'e': kiểu nội suy đoạn sau})]; kênh thiếu ở một khoá thì nội suy giữa các khoá có nó"""
    ks = [(k, d[ch], d.get("e", "smooth")) for k, d in keys if ch in d]
    if not ks:
        return default
    if f <= ks[0][0]:
        return ks[0][1]
    for (k0, v0, e0), (k1, v1, _) in zip(ks, ks[1:]):
        if k0 <= f <= k1:
            if k1 == k0:
                return v1
            return v0 + (v1 - v0) * ease(e0, (f - k0) / (k1 - k0))
    return ks[-1][1]


def K(*items):
    """K((0, x=0), ...) không viết được trong Python; dùng K((0, dict(x=0)), ...) hoặc k(0, x=0)"""
    return list(items)


def k(f, **ch):
    return (f, ch)


# ---------------------------------------------------------------- ảnh hiệu ứng

def fx_source(name):
    """ảnh GPT mới nhất của bước (theo mtime), đường dẫn; chưa có thì ảnh tạm theo FX_FALLBACK"""
    import glob
    pack, step, _ = FX[name]
    src = sorted(glob.glob(os.path.join(HEROES, "inbox", pack, "tai_ve", f"{step}*.png")), key=os.path.getmtime, reverse=True)
    if src:
        return name, src[0]
    if name in FX_FALLBACK:
        return fx_source(FX_FALLBACK[name])
    raise SystemExit(f"thiếu ảnh hiệu ứng {name} ({pack}/{step})")


def fx_image(name):
    """cắt nền trắng nối mép (khoét lõi nếu hình vòng), cắt sát, tối đa 1024; cache theo mtime ảnh nguồn"""
    real, src = fx_source(name)
    hollow = FX[real][2]
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"{real}_{int(os.path.getmtime(src))}.png")
    if os.path.exists(out):
        return Image.open(out).convert("RGBA")
    import cv2
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.uint8)
    near = (rgb.min(2) > 215).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(near, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, sorted(border))
    if hollow:
        inner = [i for i in range(1, n) if i not in border]
        if inner:
            bg |= lab == max(inner, key=lambda i: st[i, cv2.CC_STAT_AREA])
    alpha = cv2.GaussianBlur(np.where(bg, 0, 255).astype(np.uint8), (3, 3), 0)
    im = Image.fromarray(np.dstack([rgb, alpha]), "RGBA")
    im = im.crop(im.getbbox())
    im.save(out)
    return im


# ---------------------------------------------------------------- dạng

class Rig:
    def __init__(self, form):
        self.form = form
        self.f = f = Form(form, rev=BASE)
        rows = f.clips["1_1"]["frames"][0]
        ip = f.anim["idle_parts"]
        assert len(ip) == len(rows), form
        top = TOP_FIX.get(form, [])
        order = [p for p in ip if p not in top] + [p for p in ip if p in top]
        self.rest = {p: rows[i] for i, p in enumerate(order)}  # mảnh -> hàng dáng nghỉ
        self.draw = [order[i] for i in range(len(rows))]  # thứ tự vẽ dáng nghỉ (mảnh)
        am = f.anim["anim_moi"]
        self.root = int(am["root"])
        self.parent = {int(a): (int(b) if b is not None else None) for a, b in am["parent"].items()}
        self.pivot = {int(a): tuple(v) for a, v in am["pivot"].items()}
        self.shadow = next((p for p, r in self.rest.items() if r[0] == f.shadow), None)
        # chiều cao như AolaActor: tâm bóng (Anchor) trừ mép trên mọi hình khung đầu clip đứng
        top_y = min(f.bbox(r)[1] for r in rows)
        if self.shadow is not None:
            b = f.bbox(self.rest[self.shadow])
            self.foot = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        else:
            bs = [f.bbox(r) for r in rows]
            self.foot = ((min(b[0] for b in bs) + max(b[2] for b in bs)) / 2, max(b[3] for b in bs))
        self.H = self.foot[1] - top_y
        bs = [f.bbox(self.rest[p]) for p in self.rest if p != self.shadow]
        self.body = (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
        # điểm xa: tâm vùng xa (far_center) cách chân 2,8 lần chiều cao về trước, ngang giữa thân
        self.F = (self.foot[0] + 2.8 * self.H, self.foot[1] - 0.45 * self.H)
        # đơn vị quanh đối thủ: một chiều cao đối thủ chuẩn (150 đơn vị sân, StageView.Height phe địch) quy ra điểm clip. Dạng
        # cao 176 x cỡ dạng đơn vị sân (phe mình), nên dạng to vẫn đặt cầu nước, chuông vừa khoảng trống trên đầu đối thủ
        self.size = form_size(form)
        self.E = self.H * 150 / (176 * self.size)
        self.idle_sprites = {r[0] for fr in f.clips["1_1"]["frames"] for r in fr}
        # mảnh có trong cây khớp: thứ tự cha trước con
        self.chain = []
        seen = set()

        def visit(p):
            if p in seen or p not in self.rest:
                return
            q = self.parent.get(p)
            if q is not None:
                visit(q)
            seen.add(p)
            self.chain.append(p)
        for p in self.rest:
            if p in self.parent or p == self.root:
                visit(p)

    def pt(self, x, y):
        """điểm theo chân (đơn vị chiều cao, x tới trước, y xuống) -> toạ độ clip"""
        return self.foot[0] + x * self.H, self.foot[1] + y * self.H

    def far(self, x, y):
        """điểm quanh thân đối thủ (đơn vị E: chiều cao đối thủ chuẩn) -> toạ độ clip"""
        return self.F[0] + x * self.E, self.F[1] + y * self.E

    def part_pt(self, p, fx=0.5, fy=0.5):
        b = self.f.bbox(self.rest[p])
        return b[0] + (b[2] - b[0]) * fx, b[1] + (b[3] - b[1]) * fy

    def center(self, p):
        return self.part_pt(p)


def form_size(form):
    """cỡ của dạng trong heroes.json (forms[].size), mặc định 1"""
    d = json.load(open(os.path.join(PROJECT, "Assets", "02 Data", "Json", "heroes.json"), encoding="utf-8"))
    for h in d["heroes"]:
        for f in h.get("forms", []):
            if f.get("aola") == form:
                return float(f.get("size") or h.get("size") or 1)
    return 1.0


TOP_FIX = {"thuy_547": [5]}  # anim_lo2 SPEC "top": mảnh nằm cuối mọi khung (đầu Vây Lam 2)


class Clip:
    def __init__(self, rig, n, pivot="foot"):
        self.r = rig
        self.n = n
        self.rootk = []
        self.pk = {}  # mảnh -> khoá
        self.fxs = []
        self.tops = []  # (mảnh, f0, f1)
        self.far_used = False
        if pivot == "foot":
            self.rp = rig.foot
        elif pivot == "center":
            self.rp = (rig.foot[0], rig.foot[1] - 0.5 * rig.H)
        else:
            self.rp = pivot

    # thân
    def root(self, *keys):
        self.rootk += keys
        return self

    def piece(self, p, *keys):
        if p is None:
            return self
        if isinstance(p, (list, tuple)):
            for q in p:
                self.piece(q, *keys)
            return self
        self.pk.setdefault(p, []).extend(keys)
        return self

    def top(self, p, f0=0, f1=None):
        for q in (p if isinstance(p, (list, tuple)) else [p]):
            self.tops.append((q, f0, self.n if f1 is None else f1))
        return self

    # hiệu ứng: img tên trong FX hoặc ("copy", mảnh); keys kênh x, y (đơn vị H theo hệ của space), s, r, a, sx, sy;
    # size: bề ngang gốc (đơn vị H); space: "foot" (theo chân, không theo thân), "root" (đi theo thân), "far" (quanh đối
    # thủ), ("piece", p) (theo mảnh p, x y là điểm clip dáng nghỉ cộng thêm dời đơn vị H); pivot: điểm neo trong ảnh (0..1);
    # z: "under" (dưới bóng), "back" (sau thân), "front"; vis: (f0, f1) khung hiện (mặc định khoá đầu tới khoá cuối)
    def fx(self, img, keys, size=0.5, space="root", pivot=(0.5, 0.5), z="front", flip=False, tint=None, vis=None, flipy=False):
        if space == "far":
            self.far_used = True
        keys = sorted(keys, key=lambda t: t[0])
        # độ đậm giữ nguyên qua các khoá không ghi "a" (hiện lên, giữ, chỉ tan ở đoạn cuối), không nội suy mờ dần cả quãng
        held, last = [], None
        for f, d in keys:
            if "a" in d:
                last = d["a"]
            elif last is not None:
                d = dict(d, a=last)
            held.append((f, d))
        keys = held
        v0, v1 = vis or (keys[0][0], keys[-1][0])
        # khung 0 phải đúng dáng nghỉ, không hình thêm: trận lấy khung 0 làm điểm khớp (tâm bóng, dạng không bóng thì khung bao)
        self.fxs.append(dict(img=img, keys=keys, size=size, space=space, pivot=pivot, z=z, flip=flip, tint=tint,
                             vis=(max(1, v0), v1), flipy=flipy))
        return self

    # ------------------------------------------------ dựng khung
    def build(self, anim):
        r = self.r
        frames = []
        for fi in range(self.n):
            g = {c: val(self.rootk, c, fi, d) for c, d in (("x", 0), ("y", 0), ("r", 0), ("sx", 1), ("sy", 1))}
            G = about(self.rp[0], self.rp[1], g["r"], g["sx"], g["sy"], g["x"] * r.H, g["y"] * r.H)
            W = {}
            alpha = {}
            for p in r.chain:
                ks = self.pk.get(p, [])
                rot, dx, dy = val(ks, "r", fi, 0), val(ks, "x", fi, 0), val(ks, "y", fi, 0)
                sx, sy = val(ks, "sx", fi, 1), val(ks, "sy", fi, 1)
                alpha[p] = val(ks, "a", fi, 1)
                pv = r.pivot.get(p, r.center(p))
                L = about(pv[0], pv[1], rot, sx, sy, dx * r.H, dy * r.H)
                q = r.parent.get(p)
                W[p] = mul(W[q] if q in W else G, L)
            body = []
            for p in r.draw:
                row = r.rest[p]
                if p == r.shadow:
                    lift = max(0.0, -g["y"])
                    ss = max(0.55, 1 - 0.8 * lift)
                    sc = r.foot
                    M = mul(about(sc[0], sc[1], 0, ss * (1 if g["sx"] >= 0 else 1), ss, g["x"] * r.H, 0), tuple(row[1:7]))
                    body.append((p, [row[0], *M, row[7] if len(row) > 7 else 1]))
                    continue
                M = mul(W.get(p, G), tuple(row[1:7]))
                body.append((p, [row[0], *M, (row[7] if len(row) > 7 else 1) * alpha.get(p, 1)]))
            # mảnh đưa lên trên
            for p, f0, f1 in self.tops:
                if f0 <= fi < f1:
                    for i, (q, rw) in enumerate(body):
                        if q == p:
                            body.append(body.pop(i))
                            break
            under, back, front = [], [], []
            for e in self.fxs:
                if not (e["vis"][0] <= fi <= e["vis"][1]):
                    continue
                rows = self.fx_row(anim, e, fi, G, W)
                if rows:
                    {"under": under, "back": back, "front": front}[e["z"]].extend(rows)
            out = []
            si = next((i for i, (q, _) in enumerate(body) if q == r.shadow), None)
            if si is not None:
                out += [body[si][1]] if not under else under + [body[si][1]]
                rest = [rw for i, (_, rw) in enumerate(body) if i != si]
            else:
                out += under
                rest = [rw for _, rw in body]
            frames.append(out + back + rest + front)
        return frames

    def fx_row(self, anim, e, fi, G, W):
        r = self.r
        ks = e["keys"]
        a = val(ks, "a", fi, 1)
        if a <= 0.01:
            return None
        x, y = val(ks, "x", fi, 0), val(ks, "y", fi, 0)
        s = val(ks, "s", fi, 1)
        rot = val(ks, "r", fi, 0)
        sx, sy = val(ks, "sx", fi, 1), val(ks, "sy", fi, 1)
        img = e["img"]
        if isinstance(img, tuple) and img[0] == "copy":
            # bản sao một nhóm mảnh thân (hình khác số, không thuộc dáng đứng nên trận coi là hiệu ứng, kéo về đối thủ được);
            # x y: chỗ đặt tâm nhóm (theo space), s r: co giãn, xoay quanh tâm nhóm
            ps = [p for p in r.draw if p in img[1]]
            bs = [r.f.bbox(r.rest[p]) for p in ps]
            c0 = ((min(b[0] for b in bs) + max(b[2] for b in bs)) / 2, (min(b[1] for b in bs) + max(b[3] for b in bs)) / 2)
            sp = e["space"]
            if sp == "far":
                px, py = r.far(x, y)
            elif sp in ("foot", "root"):
                px, py = r.pt(x, y)
            else:
                px, py = c0[0] + x * r.H, c0[1] + y * r.H
            k1 = r.E / r.H if sp == "far" else 1.0  # quanh đối thủ: cỡ theo chiều cao đối thủ chuẩn
            A = about(c0[0], c0[1], rot, k1 * s * sx * (-1 if e["flip"] else 1), k1 * s * sy, px - c0[0], py - c0[1])
            if sp == "root":
                A = mul(G, A)
            out = []
            for p in ps:
                sid = anim.copy_sprite(r.rest[p][0])
                M = mul(A, tuple(r.rest[p][1:7]))
                out.append([sid, *M, a] + ([{"tint": e["tint"]}] if e["tint"] else []))
            return out
        sid, (w, h) = anim.fx_sprite(img)
        size_px = e["size"] * (r.E if e["space"] == "far" else r.H) * s
        k0 = size_px / w
        fl = -1 if e["flip"] else 1
        fy = -1 if e["flipy"] else 1
        piv = (e["pivot"][0] * w, e["pivot"][1] * h)
        sp = e["space"]
        if sp == "far":
            px, py = r.far(x, y)
            base = None
        elif sp == "foot":
            px, py = r.pt(x, y)
            base = None
        elif sp == "root":
            px, py = r.pt(x, y)
            base = G
        else:  # ("piece", p, (cx, cy)): điểm dáng nghỉ trên mảnh p
            _, p, c = sp
            px, py = c[0] + x * r.H, c[1] + y * r.H
            base = W.get(p, G)
        M = mul(T(px, py), mul(Rz(rot), mul(S(k0 * sx * fl, k0 * sy * fy), T(-piv[0], -piv[1]))))
        if base is not None:
            M = mul(base, M)
        return [[sid, *M, a] + ([{"tint": e["tint"]}] if e["tint"] else [])]


# ---------------------------------------------------------------- mô phỏng trận (AolaActor.MotionOf, FarPiece)

def motion(anim, frames, clip):
    r = anim.rig
    sizes = anim.sizes_out
    idle = anim.idle_out

    def corners(row):
        s, a, b, c, d, tx, ty = row[:7]
        w, h = sizes[s]
        return [(a * x + c * y + tx, b * x + d * y + ty) for x, y in ((0, 0), (w, 0), (w, h), (0, h))]
    anchor = None
    for row in frames[0]:
        if row[0] == anim.shadow_out:
            q = corners(row)
            anchor = ((q[0][0] + q[2][0]) / 2, (q[0][1] + q[2][1]) / 2)
    if anchor is None:
        anchor = r.foot
    hp = r.H
    raw = []
    for fr in frames:
        sx = sy = 0
        kk = 0
        for row in fr:
            if row[0] == anim.shadow_out:
                continue
            if row[0] not in idle:
                q = corners(row)
                cx = sum(p[0] for p in q) / 4 - anchor[0]
                if cx > 1.5 * hp:
                    continue
            sx += row[5]
            sy += row[6]
            kk += 1
        raw.append((sx / kk, sy / kk) if kk else None)
    bas = next(v for v in raw if v)
    d = []
    last = (0, 0)
    for v in raw:
        last = (v[0] - bas[0], v[1] - bas[1]) if v else last
        d.append(last)
    n = len(d)
    disp = []
    for i in range(n):
        js = range(max(0, i - 2), min(n - 1, i + 2) + 1)
        disp.append((sum(d[j][0] for j in js) / len(js), sum(d[j][1] for j in js) / len(js)))
    mags = [math.hypot(*v) for v in disp]
    bi = max(range(n), key=lambda i: mags[i])
    best = mags[bi]
    hit = bi if best > 60 else int(n * (0.55 if clip == "1_6" else 0.6))
    # cú lao của trận: đỉnh dời quy ra đơn vị sân (chiều cao dáng đứng 150..208 đơn vị); <= 30 là đòn đứng tại chỗ
    m_lo, m_hi = best * 150 / hp, best * 208 / hp
    return dict(hit=hit, peak=bi, best=best, lunge_lo=m_lo, lunge_hi=m_hi)


# ---------------------------------------------------------------- animation phụ (bù như bản gốc aola)

AOLA_DIR = next((p for p in ("E:/ProjectAtomik/aola", "D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper")
                 if os.path.isdir(p)), None)


def inv(m):
    a, b, c, d, tx, ty = m
    det = a * d - b * c
    ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    return (ia, ib, ic, id_, -(ia * tx + ic * ty), -(ib * tx + id_ * ty))


def goc_seq(pid, piece):
    """khung con của mảnh (số theo khung đầu clip đứng gốc) qua các khung clip đứng bản gốc aola: [(đường dẫn hình, ma trận, alpha)]"""
    root = os.path.join(AOLA_DIR, "reskin", f"goc_{pid}")
    d = json.load(open(os.path.join(root, "export", "anim.json"), encoding="utf-8"))
    sp = d["sprites"]
    fr = d["clips"]["1_1"]["frames"]

    def name(i):
        return os.path.basename(sp[i])[:-4]
    r0 = fr[0][piece - 1]
    base = name(r0[0]).split("_")[0]
    seq = []
    prev = r0
    for f in fr:
        cand = [q for q in f if name(q[0]).split("_")[0] == base]
        if not cand:
            seq.append(None)
            continue
        q = min(cand, key=lambda z: (z[5] - prev[5]) ** 2 + (z[6] - prev[6]) ** 2)
        prev = q
        seq.append((os.path.normpath(os.path.join(root, sp[q[0]])), tuple(q[1:7]), q[7] if len(q) > 7 else 1))
    return seq


def restyled(path, tint, line):
    """khung con gốc tô lại bằng to_nuoc (viền mực nâu, tô phẳng hai tông, bọt trắng), nhuộm thêm nếu có; trả (ảnh, lề)"""
    os.makedirs(os.path.join(CACHE, "sub"), exist_ok=True)
    tag = "" if not tint else "_" + "_".join(str(int(v)) for c in tint for v in c)
    key = os.path.basename(os.path.dirname(os.path.dirname(path))) + "_" + os.path.basename(path)[:-4] + f"_l{line}{tag}"
    out = os.path.join(CACHE, "sub", key + ".png")
    meta = out + ".margin"
    if not (os.path.exists(out) and os.path.exists(meta)):
        sys.path.insert(0, os.path.join(AOLA_DIR, "tools"))
        import to_nuoc
        tmp = os.path.join(CACHE, "sub", key + "_raw.png")
        margin = to_nuoc.restyle(path, tmp, line=line)
        im = Image.open(tmp).convert("RGBA")
        # giọt, bọt nhỏ (cụm nhỏ hơn khoảng 6 lần viền) bị viền mực phủ kín thành chấm đen: tô màu xanh đậm, chỉ giữ viền mảnh ngoài
        import cv2
        arr = np.asarray(im).astype(np.float32)
        a8 = (arr[..., 3] > 100).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(a8, connectivity=8)
        small = np.zeros(a8.shape, bool)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] < (6 * line) ** 2:
                small |= lab == i
        if small.any():
            core = cv2.erode(small.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
            arr[core, :3] = to_nuoc.MID * 0.92
            im = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")
        if tint:
            # đổi bảng màu: to_nuoc chỉ ra 4 màu (mực, xanh đậm, xanh nhạt, bọt) nhân vân chì; đổi đúng 3 tông nước, giữ viền mực
            arr = np.asarray(im).astype(np.float32)
            rgb = arr[..., :3]
            src = [to_nuoc.INK, to_nuoc.MID, to_nuoc.LIGHT, to_nuoc.FOAM]
            dst = [to_nuoc.INK] + [np.array(c, dtype=np.float32) for c in tint]
            dist = np.stack([np.linalg.norm(rgb / max(1, c.max()) - c / max(1, c.max()), axis=2) for c in src])
            near = dist.argmin(0)
            res = rgb.copy()
            for i in range(1, 4):
                m = near == i
                ratio = rgb[m] / np.maximum(src[i], 1)
                res[m] = np.clip(ratio.mean(1, keepdims=True) * dst[i], 0, 255)
            arr[..., :3] = res
            im = Image.fromarray(arr.astype(np.uint8), "RGBA")
        im.save(out)
        open(meta, "w").write(str(margin))
        os.remove(tmp)
    return Image.open(out).convert("RGBA"), float(open(meta).read())


def secondary(anim, clips, phu, sub):
    """phu: [(mảnh hoặc [mảnh], biên độ độ, số vòng mỗi clip, kiểu "sway" | "wave" | "spin")]: xoay thêm quanh khớp, lan xuống mảnh
    con, cộng vào mọi clip (clip đứng đủ biên độ, clip khác một nửa); khung 0 vẫn đúng dáng nghỉ.
    sub: [(mảnh, bảng màu [xanh đậm, xanh nhạt, bọt] hoặc None)]: mảnh nước tự chạy của bản gốc: thay hình mảnh bằng khung con gốc tô lại, chạy theo nhịp
    clip đứng gốc, đặt theo ma trận gốc rồi đi theo chuyển động mảnh."""
    if not phu and not sub:
        return
    r = anim.rig
    ident = (1, 0, 0, 1, 0, 0)
    restinv = {p: inv(tuple(r.rest[p][1:7])) for p in r.rest}
    by_sprite = {}
    for p in r.draw:
        by_sprite.setdefault(r.rest[p][0], []).append(p)
    pid = int(anim.form.split("_")[1])
    seqs = {}
    for p, tint in sub:
        frames = []
        for it in goc_seq(pid, p):
            if it is None:
                frames.append(None)
                continue
            path, M, al = it
            # viền bằng viền các mảnh GPT: khoảng 0,85% chiều cao con, quy ra điểm ảnh của hình gốc
            line = round(max(2.0, min(14.0, 0.0085 * r.H / max(1e-6, math.hypot(M[0], M[1])))), 1)
            im, margin = restyled(path, tint, line)
            sid = anim.image_sprite(("sub", path, str(tint), line), im)
            frames.append((sid, mul(M, T(-margin, -margin)), al))
        seqs[p] = frames
    for cname, frs in list(clips.items()):
        N = len(frs)
        amp_k = 1.0 if cname == "1_1" else 0.5
        out = []
        for fi, rows0 in enumerate(frs):
            rows = [list(rw) for rw in rows0]
            seen = {}
            piece_row = {}
            for i, rw in enumerate(rows):
                ps = by_sprite.get(rw[0])
                if not ps:
                    continue
                j = seen.get(rw[0], 0)
                seen[rw[0]] = j + 1
                if j < len(ps):
                    piece_row[ps[j]] = i
            W = {p: mul(tuple(rows[i][1:7]), restinv[p]) for p, i in piece_row.items()}
            extra = {}
            for spec in phu:
                ps, amp, cyc = spec[0], spec[1], spec[2]
                kind = spec[3] if len(spec) > 3 else "sway"
                ps = ps if isinstance(ps, (list, tuple)) else [ps]
                for k_, p in enumerate(ps):
                    if kind == "spin":
                        extra[p] = 360.0 * cyc * fi / N if cname == "1_1" else 0.0
                        continue
                    ph = 0.9 * k_ if kind == "wave" else 0.0
                    t = 2 * math.pi * cyc * fi / N
                    extra[p] = amp * amp_k * (math.sin(t + ph) - math.sin(ph))
            C = {}
            newW = {}
            for p in r.chain:
                if p not in W:
                    continue
                q = r.parent.get(p)
                Cp = C.get(q, ident) if q is not None else ident
                Wp = mul(Cp, W[p])
                if extra.get(p):
                    pv = r.pivot.get(p, r.center(p))
                    Wp = mul(Wp, about(pv[0], pv[1], extra[p]))
                newW[p] = Wp
                C[p] = mul(Wp, inv(W[p]))
            for p, i in piece_row.items():
                if p in newW and p != r.shadow:
                    rows[i][1:7] = list(mul(newW[p], tuple(r.rest[p][1:7])))
            for p, frames in seqs.items():
                if p not in piece_row:
                    continue
                n = len(frames)
                kidx = (round(fi * n / N) % n) if cname == "1_1" else fi % n
                it = frames[kidx] or next((x for x in frames if x), None)
                if it is None:
                    continue
                sid, M, al = it
                i = piece_row[p]
                Wp = newW.get(p, W[p])
                rows[i][0] = sid
                rows[i][1:7] = list(mul(Wp, M))
                rows[i][7] = (rows[i][7] if len(rows[i]) > 7 else 1) * al
            out.append(rows)
        clips[cname] = out


# ---------------------------------------------------------------- ghi dạng

class Anim:
    def __init__(self, form):
        self.rig = Rig(form)
        self.form = form
        self.f = self.rig.f
        self.clips = {}
        self.extra = {}
        self._fx = {}  # tên -> (chỉ số, ảnh)
        self._copies = {}  # hình thân -> chỉ số bản sao
        self.sizes_out = None

    # chỉ số hình tạm (đổi lại khi xếp atlas): hình gốc giữ số cũ, hình thêm đánh số từ 10000
    def fx_sprite(self, name):
        if name not in self._fx:
            im = fx_image(name)
            self._fx[name] = (10000 + len(self._fx) + len(self._copies), im)
        sid, im = self._fx[name]
        return sid, im.size

    def image_sprite(self, key, im):
        """ảnh thêm bất kỳ (khung con gốc đã tô lại), khoá theo key"""
        if key not in self._fx:
            self._fx[key] = (10000 + len(self._fx) + len(self._copies), im)
        return self._fx[key][0]

    def copy_sprite(self, s):
        if s not in self._copies:
            self._copies[s] = 10000 + len(self._fx) + len(self._copies)
        return self._copies[s]

    def size_of(self, s):
        if s >= 10000:
            for name, (sid, im) in self._fx.items():
                if sid == s:
                    return im.size
            for src, sid in self._copies.items():
                if sid == s:
                    return self.f.sizes[src]
        return self.f.sizes[s]

    def add(self, name, clip, lunge=False, hit=None):
        """lunge: chiêu lao tới đối thủ (trận kéo thân, khung trúng = đỉnh lao); không lao thì phải cho hit: khung trúng khai sẵn
        (anim.json "hit", clip vào "stay": trận không kéo lao, hình ở xa kéo về đối thủ)"""
        assert lunge or hit is not None, name
        self.clips[name] = (clip, lunge, hit)

    def finish(self):
        base = self.f.anim
        out_clips = {}
        for c in ("1_1", "1_2", "1_5"):
            out_clips[c] = base["clips"][c]["frames"]
        lunge, far, hits, stay, ramp = [], {}, {}, [], {}
        for name, (clip, lg, hit) in self.clips.items():
            out_clips[name] = clip.build(self)
            if lg:
                if name != "1_4":
                    lunge.append(name)
            else:
                hits[name] = hit
                stay.append(name)
            if clip.far_used and not lg:
                far[name] = [round(self.rig.F[0], 2), round(self.rig.F[1], 2)]
                ramp[name] = round(self.rig.foot[0] + RAMP_END * self.rig.H, 2)
        # animation phụ như bản gốc aola (người dùng dặn 2026-11-07): chuyển động phụ cộng thêm, nước tự chạy bằng khung gốc tô lại
        from anim_thuy_choreo import PHU, SUB
        secondary(self, out_clips, PHU.get(self.form, []), SUB.get(self.form, []))
        # đổi số hình: hình dùng tới, xếp lại
        used = []
        seen = set()
        for c in ("1_1", "1_2", "1_4", "1_5", "1_6"):
            for fr in out_clips.get(c, []):
                for row in fr:
                    if row[0] not in seen:
                        seen.add(row[0])
                        used.append(row[0])
        remap = {s: i for i, s in enumerate(used)}
        self.sizes_out = [self.size_of(s) for s in used]
        self.idle_out = {remap[r[0]] for fr in out_clips["1_1"] for r in fr}
        self.shadow_out = remap.get(self.f.shadow, -1)
        clips_json = {}
        for c in ("1_1", "1_2", "1_4", "1_5", "1_6"):
            frs = []
            for fr in out_clips[c]:
                rows = []
                for row in fr:
                    nr = [remap[row[0]]] + [round(float(v), 4) for v in row[1:8]]
                    if len(row) > 8:
                        nr += row[8:]
                    rows.append(nr)
                frs.append(rows)
            clips_json[c] = {"size": base["clips"][c].get("size"), "frames": frs}
        self.used = used
        self.remap = remap
        anim = {k: v for k, v in base.items() if k not in ("clips", "lunge", "far_center", "hit", "stay", "far_ramp")}
        anim["clips"] = clips_json
        if lunge:
            anim["lunge"] = lunge
        if far:
            anim["far_center"] = far
            anim["far_ramp"] = ramp
        if hits:
            anim["hit"] = hits
            anim["stay"] = stay
        anim["anim_thuy"] = time.strftime("%Y-%m-%d %H:%M") + " tools/anim_thuy.py (đòn đánh, chiêu cuối viết lại)"
        self.anim_out = anim
        return anim

    def report(self):
        rep = {}
        for name in ("1_4", "1_6"):
            frames = []
            for fr in self.anim_out["clips"][name]["frames"]:
                frames.append(fr)
            m = motion(self, frames, name)
            clip, lg, hit = self.clips[name]
            if lg:
                rep[name] = dict(m, kind="lao", ok=m["best"] > 60 and m["lunge_lo"] > 30)
            else:
                rep[name] = dict(m, kind="xa", ok=True, hit=hit)
        return rep

    def pack(self):
        """atlas mới: hình thân cắt từ atlas gốc (giữ độ nét đã thu), hình hiệu ứng thu về cỡ hiện lớn nhất x OtherScale"""
        f = self.f
        r = self.rig
        k = (1024 / 3.4) / max(1.0, r.H)
        need = {}
        shown = {}
        for c in ("1_1", "1_2", "1_4", "1_5", "1_6"):
            for fr in self.anim_out["clips"][c]["frames"]:
                for s in {row[0] for row in fr}:
                    shown[s] = shown.get(s, 0) + 1
                for row in fr:
                    s = row[0]
                    a, b, cc, d = row[1:5]
                    need[s] = max(need.get(s, 0), max(math.hypot(a, b), math.hypot(cc, d)) * k)

        def brief(n):  # AolaImport.BriefScale (luật 1): hình hiện 1-2 khung thu 0,65, 3-4 khung 0,85
            return 1 if n <= 0 else 0.65 if n <= 2 else 0.85 if n <= 4 else 1
        imgs = []
        for i, s in enumerate(self.used):
            if s < 10000:
                imgs.append(("cut", s))
            elif s in self._copies.values():
                src = next(a for a, b in self._copies.items() if b == s)
                imgs.append(("same", self.remap[src] if src in self.remap else None, src))
            else:
                name = next(n for n, (sid, _) in self._fx.items() if sid == s)
                im = self._fx[name][1]
                sc = min(1.0, need.get(i, 1) * 0.7 * brief(shown.get(i, 0)))
                if sc < 1:
                    im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))), Image.LANCZOS)
                imgs.append(("img", im))
        tiles = {}
        for i, it in enumerate(imgs):
            if it[0] == "cut":
                W0, H0 = f.atlas.size
                x, y, w, h = f.uvs[it[1]]
                box = (round(x * W0), round((1 - y - h) * H0), round((x + w) * W0), round((1 - y) * H0))
                tiles[i] = f.atlas.crop(box)
            elif it[0] == "img":
                tiles[i] = it[1]
        # bản sao: dùng chung chỗ với hình gốc; gốc không dùng ở clip nào thì xếp riêng
        for i, it in enumerate(imgs):
            if it[0] == "same" and it[1] is None:
                W0, H0 = f.atlas.size
                x, y, w, h = f.uvs[it[2]]
                tiles[i] = f.atlas.crop((round(x * W0), round((1 - y - h) * H0), round((x + w) * W0), round((1 - y) * H0)))
        place = shelf_pack({i: t.size for i, t in tiles.items()})
        AW = max(px + tiles[i].width for i, (px, py) in place.items()) + 4
        AH = max(py + tiles[i].height for i, (px, py) in place.items()) + 4
        atlas = Image.new("RGBA", (AW, AH), (0, 0, 0, 0))
        uvs = [None] * len(imgs)
        for i, (px, py) in place.items():
            t = tiles[i]
            atlas.paste(t, (px, py))
            uvs[i] = (px / AW, 1 - (py + t.height) / AH, t.width / AW, t.height / AH)
        for i, it in enumerate(imgs):
            if it[0] == "same" and it[1] is not None:
                uvs[i] = uvs[it[1]]
        self.atlas_out = atlas
        self.uvs_out = uvs
        return atlas

    def write(self):
        base = f"{RES}/{self.form}/{self.form}"
        root = PROJECT
        self.atlas_out.save(os.path.join(root, base + "_atlas.png"), optimize=True)
        text = json.dumps(self.anim_out, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        open(os.path.join(root, base + "_anim.bytes"), "wb").write(gzip.compress(text, 9))
        a = self.f.asset_text
        sizes = "".join(f"  - {{x: {fmt(w)}, y: {fmt(h)}}}\n" for w, h in self.sizes_out)
        uvs = "".join(f"  - serializedVersion: 2\n    x: {fmt(x)}\n    y: {fmt(y)}\n    width: {fmt(w)}\n    height: {fmt(h)}\n"
                      for x, y, w, h in self.uvs_out)
        a = re.sub(r"(  sizes:\n)(?:  - \{[^\n]*\}\n)*", lambda m: m.group(1) + sizes, a, count=1)
        a = re.sub(r"(  uvs:\n)(?:  - serializedVersion: 2\n(?:    [^\n]*\n){4})*", lambda m: m.group(1) + uvs, a, count=1)
        a = re.sub(r"^  shadow: -?\d+", f"  shadow: {self.shadow_out}", a, count=1, flags=re.M)
        a = re.sub(r"^  source: .*$", f"  source: anim_thuy-{int(time.time())}", a, count=1, flags=re.M)
        a = re.sub(r"^  brief: .*\n", "", a, flags=re.M)
        a = a.rstrip("\n") + "\n  brief: 1\n"  # luật thu hình ít khung đã áp (AolaImport.BriefRule), menu thu không thu lần nữa
        open(os.path.join(root, base + ".asset"), "w", encoding="utf-8", newline="\n").write(a)


def fmt(v):
    v = float(v)
    if v == int(v):
        return str(int(v))
    return f"{v:.8g}"


def shelf_pack(sizes, pad=4):
    """xếp kệ: cao trước, bề rộng atlas theo căn diện tích; trả {i: (x, y)}"""
    area = sum((w + pad) * (h + pad) for w, h in sizes.values())
    widest = max(w for w, h in sizes.values()) + 2 * pad
    W = max(widest, int(math.sqrt(area) * 1.15))
    order = sorted(sizes, key=lambda i: -sizes[i][1])
    x = y = pad
    shelf = 0
    out = {}
    for i in order:
        w, h = sizes[i]
        if x + w + pad > W:
            x = pad
            y += shelf + pad
            shelf = 0
        out[i] = (x, y)
        x += w + pad
        shelf = max(shelf, h)
    return out


# ---------------------------------------------------------------- tờ khung

def sheet(anim, path, clips=("1_4", "1_6"), step=3, enemy=(1.4, 1.4), cols=10, scale=0.95):
    """khung clip mới; hình ở xa kéo về một đối thủ giả định (enemy: thân đối thủ so với chân, đơn vị H, y lên) như trận"""
    from PIL import ImageDraw
    r = anim.rig
    H = r.H
    fx0, fy0 = r.foot
    view = (fx0 - 0.9 * H, fy0 - 3.25 * H, fx0 + 2.7 * H, fy0 + 0.35 * H)

    class _F:  # Form giả để vẽ bằng aola_form.Form.render
        pass
    tiles = []
    for c in clips:
        frames = anim.anim_out["clips"][c]["frames"]
        far = c in anim.anim_out.get("far_center", {})
        rep = anim.rep.get(c, {}) if hasattr(anim, "rep") else {}
        for i in list(range(0, len(frames), step)) + ([rep["hit"]] if rep.get("hit") is not None else []):
            rows = frames[i]
            box = None
            if far:
                rows = pull_far(anim, c, rows, enemy)
                tx, ty = fx0 + enemy[0] * H, fy0 - enemy[1] * H
                box = (tx - 0.3 * H, ty - 0.45 * H, tx + 0.3 * H, ty + 0.45 * H)
            im = render(anim, rows, view, scale, box)
            lab = f"{c}:{i}" + (" TRÚNG" if i == rep.get("hit") else "")
            tiles.append((lab, im))
    tw, th = tiles[0][1].size
    rows_n = (len(tiles) + cols - 1) // cols
    Sx = Image.new("RGB", (cols * tw, rows_n * (th + 14)), "white")
    d = ImageDraw.Draw(Sx)
    for kk, (lab, im) in enumerate(tiles):
        x, y = (kk % cols) * tw, (kk // cols) * (th + 14)
        Sx.paste(im.convert("RGB"), (x, y + 14))
        d.text((x + 3, y + 1), lab, fill=(200, 0, 0) if "TRÚNG" in lab else (0, 0, 0))
        d.line([(x, y), (x, y + th + 14)], fill=(210, 210, 210))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Sx.save(path)
    return path


def pull_far(anim, clip, rows, enemy):
    r = anim.rig
    H = r.H
    F = anim.anim_out["far_center"][clip]
    end = min(anim.anim_out["far_ramp"][clip], F[0]) - r.foot[0]
    target = (r.foot[0] + enemy[0] * H, r.foot[1] - enemy[1] * H)
    out = []
    r0 = 1.0 * H
    for row in rows:
        if row[0] in anim.idle_out:
            out.append(row)
            continue
        w, h = anim.sizes_out[row[0]]
        a, b, c, d, tx, ty = row[1:7]
        cx = a * w / 2 + c * h / 2 + tx
        dd = cx - r.foot[0]
        if dd > r0 and end > r0:
            wgt = min(1, max(0, (dd - r0) / (end - r0)))
            row = list(row)
            row[5] += wgt * (target[0] - F[0])
            row[6] += wgt * (target[1] - F[1])
        out.append(row)
    return out


def render(anim, rows, view, scale, box=None):
    """vẽ khung từ atlas mới (đã pack); box: khung xám (x0, y0, x1, y1 toạ độ clip) đánh dấu chỗ đối thủ"""
    x0, y0, x1, y1 = view
    Wd, Hd = int((x1 - x0) * scale), int((y1 - y0) * scale)
    out = Image.new("RGBA", (Wd, Hd), (255, 255, 255, 255))
    if box:
        from PIL import ImageDraw
        ImageDraw.Draw(out).rounded_rectangle([(box[0] - x0) * scale, (box[1] - y0) * scale, (box[2] - x0) * scale, (box[3] - y0) * scale],
                                              radius=12, fill=(225, 225, 225, 255), outline=(170, 170, 170, 255))
    A = anim.atlas_out
    AW, AH = A.size
    cache = anim.__dict__.setdefault("_spr", {})
    for row in rows:
        s = row[0]
        al = row[7]
        if al <= 0.01:
            continue
        if s not in cache:
            x, y, w, h = anim.uvs_out[s]
            im = A.crop((round(x * AW), round((1 - y - h) * AH), round((x + w) * AW), round((1 - y) * AH)))
            sw, sh = anim.sizes_out[s]
            cache[s] = im.resize((max(1, round(sw)), max(1, round(sh))), Image.BILINEAR)
        im = cache[s]
        tint = row[8].get("tint") if len(row) > 8 and isinstance(row[8], dict) else None
        if tint:
            arr = np.asarray(im).astype(np.float32)
            for c in range(3):
                arr[..., c] = np.clip(arr[..., c] * tint[c] + tint[3 + c], 0, 255)
            im = Image.fromarray(arr.astype(np.uint8), "RGBA")
        a, b, c, d, tx, ty = row[1:7]
        A2, B2, C2, D2 = a * scale, b * scale, c * scale, d * scale
        TX, TY = (tx - x0) * scale, (ty - y0) * scale
        det = A2 * D2 - B2 * C2
        if abs(det) < 1e-9:
            continue
        ia, ib, ic, idd = D2 / det, -C2 / det, -B2 / det, A2 / det
        layer = im.transform((Wd, Hd), Image.AFFINE, (ia, ib, -(ia * TX + ib * TY), ic, idd, -(ic * TX + idd * TY)),
                             resample=Image.BILINEAR)
        if al < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * al)))
        out.alpha_composite(layer)
    return out


# ================================================================ chạy

def run(form, do_sheet=False, dry=False):
    from anim_thuy_choreo import CHOREO
    anim = Anim(form)
    CHOREO[form](anim)
    anim.finish()
    anim.pack()
    anim.rep = anim.report()
    for c, m in anim.rep.items():
        flag = "OK" if m["ok"] else "LỆCH"
        print(f"  {form} {c}: {m['kind']} trúng khung {m['hit']}/{len(anim.anim_out['clips'][c]['frames'])} (đỉnh {m['peak']}, "
              f"dời {m['best']:.0f}px = {m['lunge_lo']:.0f}..{m['lunge_hi']:.0f} đv sân) {flag}")
    print(f"  atlas {anim.atlas_out.size[0]}x{anim.atlas_out.size[1]} ({anim.atlas_out.size[0] * anim.atlas_out.size[1] / 1e6:.2f} MP), "
          f"{len(anim.used)} hình (gốc {len(anim.f.sizes)})")
    if do_sheet:
        p = sheet(anim, os.path.join(OUT_SHEET, f"{form}.png"))
        print("  tờ khung:", p)
    if not dry:
        anim.write()
    return anim


def main(argv):
    from anim_thuy_choreo import CHOREO
    args = [x for x in argv if not x.startswith("--")]
    for fm in args or list(CHOREO):
        print(fm)
        run(fm, "--sheet" in argv, "--dry" in argv)


if __name__ == "__main__":
    import anim_thuy  # chạy bằng bản module (bộ đòn import anim_thuy), không phải __main__
    anim_thuy.main(sys.argv[1:])
