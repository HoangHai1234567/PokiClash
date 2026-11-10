"""Thư viện dựng hiệu ứng hạt chồng lớp phẳng (chuẩn mốc phun lửa 2026-11-10, skill pokiclash-hero-fx mục 0b).

Chia như VFX Graph: Spawn (Sim.at / every / periodic) -> Initialize (hàm tạo hạt) -> Update (Sim.step: cản mũ, gia tốc,
hàm upd riêng, chạm đất, sinh hạt con khi chết) -> Output (mỗi hạt trả các "nét vẽ" (nhóm, lớp, ảnh, màu, cỡ...), gom lại,
xếp theo (nhóm, lớp) rồi chồng). Không glow, không additive, không gradient: chỉ màu phẳng nhân lên ảnh xám, alpha phẳng.

Nhóm vẽ: FLOOR (dưới đất: khe nứt, bóng, vũng, vòng sau), BACK (sau tướng), HERO (tướng), FRONT (trước tướng).
Lớp trong nhóm: khói (mực 10, ruột 11), lửa (mực 20, đỏ 21, cam 22, vàng 23, kem 24, trang trí 21.5), trên cùng 40+.

Toạ độ: khung sân 540 x 464 (y xuống) như StageView, ảnh ra nhân K, có lề M để rung màn không hở mép.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import fire

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
K = 2
M = 24  # lề (px) cho rung
FPS = 30
W, Hs = 540, 464
H = 150.0  # chiều cao tướng chuẩn (đơn vị sân)
ME, FOE = np.array([392.0, 418.0]), np.array([158.0, 236.0])  # chân phe mình, địch (StageView.Pos)
FLOOR, BACK, HERO, FRONT = 0, 100, 200, 300
INK = fire.INK

PAL = {  # màu phẳng: [viền, ngoài -> lõi]
    "lua": [(234, 80, 42), (248, 150, 48), (252, 210, 78), (254, 244, 206)],
    "xoan": [(206, 58, 38), (240, 128, 44), (249, 192, 68), (253, 236, 176)],
    "nham": [(186, 46, 30), (236, 104, 34), (250, 170, 50), (254, 230, 132)],
    "lam": [(52, 96, 196), (84, 160, 236), (160, 220, 250), (236, 250, 255)],
}
SMOKE_DARK = [(50, 42, 40), (98, 92, 90), (152, 148, 146), (198, 194, 190)]  # than đen -> xám -> xám nhạt
SMOKE_FIRE = [(240, 140, 50), (168, 86, 50), (112, 98, 94), (160, 156, 152), (204, 200, 196)]  # khói đuôi lửa (cam -> nâu -> than -> xám)
SMOKE_CREAM = [(238, 230, 214), (226, 216, 202), (210, 202, 192), (204, 194, 184)]


def lerp(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def ramp(stops, k):
    k = min(1.0, max(0.0, k)) * (len(stops) - 1)
    i = min(len(stops) - 2, int(k))
    return lerp(stops[i], stops[i + 1], k - i)


def ease_out(x):
    return 1 - (1 - min(1.0, max(0.0, x))) ** 3


def unit(v):
    n = float(np.hypot(*v))
    return v / n if n > 1e-6 else np.array([0.0, -1.0])


# ---------------- hạt ----------------
class P:
    def __init__(self, pos, vel=(0, 0), life=1.0, **kw):
        self.pos = np.array(pos, float)
        self.vel = np.array(vel, float)
        self.age, self.life = 0.0, float(life)
        self.drag = 0.0  # cản mũ (1/s)
        self.acc = np.zeros(2)  # gia tốc (trọng lực dương = rơi; nổi = âm)
        self.draw = None  # hàm(p, k) -> danh sách nét vẽ
        self.upd = None  # hàm(p, dt, sim) riêng
        self.on_death = None
        self.on_ground = None
        self.ground = None  # y mặt đất (đơn vị sân); None = không chạm
        self.bounce = 0.0
        self.bounced = False
        self.seed = 0
        self.ang = 0.0
        self.spin = 0.0
        self.spin_drag = 0.0
        self.group = FRONT
        self.dead = False
        self.__dict__.update(kw)


class Sim:
    def __init__(self, seed=1):
        self.rng = np.random.RandomState(seed)
        self.seed = seed
        self.ps = []
        self.t = 0.0
        self.events = []  # (t, fn)
        self.streams = []  # [t0, t1, rate, fn, acc]
        self.periodics = []  # [period, n, fn, next_j, t0, t1]
        self.trauma = 0.0
        self.flash = 0.0  # chớp kem cả màn (alpha)
        self.hero_fx = {}  # tên -> {"tint": màu, "amt": 0..1, "off": (dx, dy), "sq": (sx, sy)}

    def add(self, p):
        self.ps.append(p)
        return p

    def at(self, t, fn):
        self.events.append([t, fn])

    def every(self, t0, t1, rate, fn):
        """sinh liên tục rate hạt/giây trong [t0, t1); fn(sim, x) với x = tuổi luồng 0..1."""
        self.streams.append([t0, t1, rate, fn, 0.0])

    def periodic(self, period, n, fn, t0=0.0, t1=1e9):
        """sinh n lần mỗi chu kỳ, tham số lấy từ rng riêng theo (j mod n): sau một chu kỳ khởi động trạng thái lặp đúng
        chu kỳ -> clip lặp liền mạch (aura, nhiệt). fn(sim, rng_j, j)."""
        self.periodics.append([period, n, fn, 0, t0, t1])

    def shake(self, amt):
        self.trauma = min(1.0, self.trauma + amt)

    def step(self, dt):
        t = self.t
        for ev in self.events:
            if ev[0] is not None and t >= ev[0]:
                ev[0] = None
                ev[1](self)
        for st in self.streams:
            t0, t1, rate, fn, acc = st
            if t0 <= t < t1:
                st[4] += dt * (rate(self, (t - t0) / (t1 - t0)) if callable(rate) else rate)
                while st[4] >= 1:
                    st[4] -= 1
                    fn(self, (t - t0) / (t1 - t0))
        for pr in self.periodics:
            period, n, fn, j, t0, t1 = pr
            while t0 + j * period / n <= t and t0 + j * period / n < t1:
                fn(self, np.random.RandomState(self.seed * 7919 + (j % n)), j)
                j += 1
            pr[3] = j
        alive = []
        for p in self.ps:
            p.age += dt
            if p.age >= p.life or p.dead:
                if p.on_death:
                    p.on_death(p, self)
                continue
            if p.drag:
                p.vel *= math.exp(-p.drag * dt)
            p.vel += p.acc * dt
            if p.spin_drag:
                p.spin *= math.exp(-p.spin_drag * dt)
            p.ang += p.spin * dt
            if p.upd:
                p.upd(p, dt, self)
            p.pos = p.pos + p.vel * dt
            if p.ground is not None and p.pos[1] > p.ground and p.vel[1] > 0:
                p.pos[1] = p.ground
                if p.bounce and not p.bounced:
                    p.bounced = True
                    p.vel = np.array([p.vel[0] * 0.65, -p.vel[1] * p.bounce])
                    p.spin *= 0.5
                else:
                    if p.on_ground:
                        p.on_ground(p, self)
                    p.vel[:] = 0
                    p.acc = np.zeros(2)
            alive.append(p)
        self.ps = alive
        self.trauma = max(0.0, self.trauma - 1.4 * dt)
        self.flash = max(0.0, self.flash - 6 * dt)
        for h in self.hero_fx.values():
            if "decay" in h:
                h["amt"] = max(0.0, h["amt"] - h["decay"] * dt)
        self.t += dt


# ---------------- ảnh ----------------
class Art:
    def __init__(self):
        self.src = {}
        self.cache = {}

    # hình hạt GPT vẽ (build_hat.py --nhap -> hat_gpt/): tên trong fxlib -> (tên file, ảnh đặc cho lớp mực?)
    GPT = {"blob": ("blob", False), "solid": ("blob", True), "sblob": ("sblob", False), "ssolid": ("sblob", True),
           "hook": ("hook", False), "hook_s": ("hook", True), "xhook": ("xhook", False), "xhook_s": ("xhook", True),
           "ldrop": ("ldrop", False), "ldrop_s": ("ldrop", True), "rock": ("rock", False)}
    FALLBACK = {"xhook": "hook", "xhook_s": "hook_s", "ldrop": "blob", "ldrop_s": "solid"}
    EXTRA = {}  # hình thêm của từng bộ (bo_thuy.py...): tên -> hàm(seed) trả ảnh RGBA

    def _gpt(self, name, seed):
        if name not in self.GPT:
            return None
        base, solid = self.GPT[name]
        f = os.path.join(HERE, "hat_gpt", f"{base}_s_{seed % 4}.png" if solid else f"{base}_{seed % 4}.png")
        return Image.open(f).convert("RGBA") if os.path.exists(f) else None

    def get(self, name, seed=0):
        key = (name, seed)
        if key not in self.src:
            g = self._gpt(name, seed)
            if g is not None:
                self.src[key] = g
                return g
            if name in self.FALLBACK:
                self.src[key] = self.get(self.FALLBACK[name], seed)
                return self.src[key]
            if name in self.EXTRA:
                self.src[key] = self.EXTRA[name](seed)
                return self.src[key]
            f = {
                "blob": lambda s: fire.blob(s)[0], "solid": lambda s: fire.blob_solid(s)[0],
                "hook": lambda s: fire.hook(s)[0], "hook_s": lambda s: fire.hook(s, solid=True)[0],
                "lobe": lambda s: fire.flame_lobes(s)[0], "lobe_s": lambda s: fire.flame_lobes(s, solid=True)[0],
                "sblob": lambda s: fire.cloud(s)[0], "ssolid": lambda s: fire.cloud(s, solid=True)[0],
                "burst": lambda s: fire.burst(s)[0], "burst_s": lambda s: fire.burst(s, solid=True)[0],
                "tongue": lambda s: fire.tongue(s)[0], "tongue_s": lambda s: fire.tongue(s, solid=True)[0],
                "curl": lambda s: fire.curl(s)[0], "streak": lambda s: fire.streak(s)[0], "ember": lambda s: fire.ember(s)[0],
                "ring": lambda s: fire.ring(thick=(0.22, 0.14, 0.08)[s % 3])[0],
                "ring_s": lambda s: fire.ring(thick=(0.22, 0.14, 0.08)[s % 3], solid=True)[0],
                "crack": lambda s: fire.lava_crack(s)[0], "rock": lambda s: fire.lava_rock(s)[0],
                "star": lambda s: fire.star4(s)[0], "heat": lambda s: fire.heat_ribbon(s / 8)[0],
                "ash": lambda s: fire.ash(s)[0], "ell": lambda s: fire.ellipse_solid()[0],
                "needle": lambda s: fire.needle(s)[0], "needle_s": lambda s: fire.needle(s, solid=True)[0],
            }.get(name)
            if f is None and name.startswith("erode"):  # erode_f / erode_r: (seed, khung)
                fr = seed % 10
                base = seed // 10
                ef = fire.erode_frames(base, n=6)
                for i, (a, b) in enumerate(ef):
                    self.src[("erode_f", base * 10 + i)] = a
                    self.src[("erode_r", base * 10 + i)] = b
                return self.src[key]
            self.src[key] = f(seed)
        return self.src[key]

    def hatch(self, col, size):
        """nền vân chì nhuộm màu col, phủ cả khung (cho mảng đa giác)."""
        key = ("hatch", tuple(col), size)
        if key not in self.cache:
            if "hatch0" not in self.src:
                big = fire._hatch((size[0] * 2, size[1] * 2), fire.GRAY, fire.HATCH_LO, np.random.RandomState(77), gap=2, ang=-38, amt=0.85)
                self.src["hatch0"] = np.asarray(big.convert("RGB").resize(size, Image.LANCZOS)).astype(np.float32)
            a = self.src["hatch0"] * (np.array(col, np.float32) / 255.0)
            self.cache[key] = Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGB")
        return self.cache[key]

    def poly(self, im, pts, col, alpha=1.0, grow=0.0):
        """mảng đa giác tô phẳng có vân chì (thân vòi rồng, dải nước liền): pts theo toạ độ sân; grow: nở thêm (viền mực)."""
        P_ = [(x * K + M, y * K + M) for x, y in pts]
        pad = int(grow * K) + 2
        x0 = max(0, int(min(q[0] for q in P_)) - pad)
        y0 = max(0, int(min(q[1] for q in P_)) - pad)
        x1 = min(im.width, int(max(q[0] for q in P_)) + pad + 1)
        y1 = min(im.height, int(max(q[1] for q in P_)) + pad + 1)
        if x1 <= x0 or y1 <= y0:
            return
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        d = ImageDraw.Draw(m)
        q = [(x - x0, y - y0) for x, y in P_]
        d.polygon(q, fill=255)
        if grow > 0:
            d.line(q + [q[0]], fill=255, width=int(2 * grow * K), joint="curve")
        if alpha < 0.999:
            m = m.point(lambda v: int(v * alpha))
        layer = self.hatch(col, im.size).crop((x0, y0, x1, y1)).convert("RGBA")
        layer.putalpha(m)
        im.alpha_composite(layer, (x0, y0))

    def polys(self, im, shapes, alpha=1.0):
        """nhiều mảng đa giác vẽ ĐẶC chồng nhau, rồi cả cụm mới làm trong (alpha): thân nước trong mờ mà chỗ chồng không bị tối."""
        tmp = Image.new("RGBA", im.size, (0, 0, 0, 0))
        for pts, col, grow in shapes:
            self.poly(tmp, pts, col, 1.0, grow)
        if alpha < 0.999:
            tmp.putalpha(tmp.getchannel("A").point(lambda v: int(v * alpha)))
        im.alpha_composite(tmp)

    def render(self, name, seed, col, w, h, ang, alpha):
        w, h = max(2, int(round(w))), max(2, int(round(h)))
        if name == "haze":  # hơi nóng: nét lượn mảnh không viền, seed = pha (0..23), màu kem nhạt, thon hai đầu
            ck = (name, seed, col, w // 2, h // 2, int(alpha * 40))
            im = self.cache.get(ck)
            if im is None:
                im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                ph = seed / 24
                pts = []
                for i in range(33):
                    t = i / 32
                    x = 4 + w / 2 + (w / 2 - 3) * math.sin(2 * math.pi * (1.3 * t + ph)) * math.sin(math.pi * t) ** 0.6
                    pts.append((x, 4 + t * h, math.sin(math.pi * t) ** 0.7))
                base = 2.2 * K
                c = tuple(col) + (int(255 * int(alpha * 40) / 40),)
                for (x0, y0, a0), (x1, y1, a1) in zip(pts[:-1], pts[1:]):
                    wd = max(1.0, base * (a0 + a1) / 2)
                    d.line([(x0, y0), (x1, y1)], fill=c, width=int(round(wd)))
                    d.ellipse([x1 - wd / 2, y1 - wd / 2, x1 + wd / 2, y1 + wd / 2], fill=c)
                self.cache[ck] = im
            return im
        if name in ("arcpx", "arcpx0"):  # đoạn cung elip theo pixel: seed = góc đầu*1000 + độ dài cung (độ, kiểu PIL: 0 = 3 giờ, chiều kim)
            ck = (name, seed, col, w // 2, h // 2, int(alpha * 40))
            im = self.cache.get(ck)
            if im is None:
                a0, span = seed // 1000, seed % 1000
                ink = int(2.2 * K) if name == "arcpx" else 0
                bw = max(2, int(col[3])) if len(col) > 3 else 6
                pad = ink + bw
                im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                box = [pad, pad, pad + w, pad + h]
                if ink:
                    d.arc([box[0] - ink / 2, box[1] - ink / 2, box[2] + ink / 2, box[3] + ink / 2], a0, a0 + span,
                          fill=INK + (255,), width=bw + 2 * ink)
                d.arc(box, a0 + 1, a0 + span - 1, fill=tuple(col[:3]) + (255,), width=bw)
                if alpha < 0.999:
                    arr = np.asarray(im).astype(np.float32)
                    arr[..., 3] *= int(alpha * 40) / 40
                    im = Image.fromarray(arr.astype(np.uint8), "RGBA")
                self.cache[ck] = im
            return im
        if name in ("ringpx", "ringpx0"):  # vòng vẽ thẳng theo pixel (ringpx0: không viền mực, cho vòng mảnh, vòng nhỏ): dải màu seed px, viền mực cố định (không phóng to theo ảnh)
            ck = (name, seed, col, w // 2, h // 2, int(alpha * 20))
            im = self.cache.get(ck)
            if im is None:
                ink = int(2.5 * K) if name == "ringpx" else 0
                bw = max(1, seed)
                pad = ink + bw
                im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                box = [pad - bw / 2 - ink, pad - bw / 2 - ink, pad + w + bw / 2 + ink, pad + h + bw / 2 + ink]
                if ink:
                    d.ellipse(box, outline=INK + (255,), width=bw + 2 * ink)
                box2 = [box[0] + ink, box[1] + ink, box[2] - ink, box[3] - ink]
                d.ellipse(box2, outline=tuple(col) + (255,), width=bw)
                if alpha < 0.999:
                    a = np.asarray(im).astype(np.float32)
                    a[..., 3] *= int(alpha * 20) / 20
                    im = Image.fromarray(a.astype(np.uint8), "RGBA")
                self.cache[ck] = im
            return im
        aq = int(round(ang / 3)) * 3 % 360
        alq = int(alpha * 40)
        ck = (name, seed, col, w, h, aq, alq)
        im = self.cache.get(ck)
        if im is None:
            a = np.asarray(self.get(name, seed).resize((w, h), Image.BILINEAR)).astype(np.float32)
            if col is not None:
                a[..., :3] *= np.array(col, np.float32) / 255.0
            if alq < 40:
                a[..., 3] *= alq / 40
            im = Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")
            if aq:
                im = im.rotate(aq, resample=Image.BILINEAR, expand=True)
            if len(self.cache) > 20000:
                self.cache.clear()
            self.cache[ck] = im
        return im


def poly(group, layer, pts, col, alpha=1.0, grow=0.0):
    """nét vẽ mảng đa giác tô phẳng có vân chì; grow > 0: nở thêm (dùng cho lớp mực dưới)."""
    return (group, layer, "poly", tuple((float(x), float(y)) for x, y in pts), col, (0.0, 0.0), grow, 0, 0, alpha)


def polys(group, layer, shapes, alpha=1.0):
    """cả cụm mảng đa giác (đỉnh, màu, nở) vẽ đặc rồi làm trong một lần: dùng cho thân nước trong mờ nhiều lớp."""
    return (group, layer, "polys", tuple((tuple((float(x), float(y)) for x, y in pts), col, float(g)) for pts, col, g in shapes), None,
            (0.0, 0.0), 0, 0, 0, alpha)


def item(group, layer, name, seed, col, pos, size, stretch=1.0, ang=0.0, alpha=1.0):
    """một nét vẽ: size = cao (đơn vị sân), stretch = rộng/cao; ang độ (ngược chiều kim)."""
    return (group, layer, name, seed, col, (float(pos[0]), float(pos[1])), size * stretch, size, ang, alpha)


# ---------------- vật liệu (Output) ----------------
def tip_angle(d):
    """góc xoay (độ, PIL) để ảnh có ngọn chĩa LÊN quay ngọn theo vectơ d."""
    return -math.degrees(math.atan2(d[0], -d[1]))


def flame_radii(k, r, heat=1.0):
    """bán kính lớp theo tuổi (chuẩn mốc): lõi kem hết ở 40% đời, vàng 68%, cam 95%. heat > 1: nóng lâu hơn."""
    cream = r * 0.55 * max(0.0, 1 - k / (0.4 * heat)) ** 0.7
    yellow = r * 0.74 * max(0.0, 1 - k / (0.68 * heat)) ** 0.7
    orange = r * 0.88 * max(0.0, 1 - k / min(1.4, 0.95 * heat)) ** 0.6
    return [r, r, orange, yellow, cream]


def mat_flame(style="tron", pal="lua", heat=1.0, size_fn=None, stretch_k=1100.0, ink=5.0):
    """lửa chồng lớp. style: tron (cụm tròn, chuẩn mốc), nhon (lưỡi móc câu, lõi dồn về đáy), xoan (khối đỏ sẫm + lưỡi cam +
    vòng xoắn trang trí), nham (dung nham: kéo dài theo vận tốc, nguội về đá)."""
    cols = PAL[pal]

    def draw(p, k):
        r = size_fn(p, k) if size_fn else p.r0 + (p.r1 - p.r0) * ease_out(k / 0.75) ** 0.8
        if size_fn is None:
            r *= 1 - 0.88 * max(0.0, (k - 0.66) / 0.34) ** 1.3
        if r < 0.8:
            return []
        rr = flame_radii(k, r, getattr(p, "heat", heat))
        sp = float(np.hypot(*p.vel))
        out = []
        layer_cols = [INK] + cols
        if pal == "nham" and getattr(p, "cool", False):  # dung nham nguội (chỉ khi được đánh dấu): viền ngả nâu đá
            layer_cols[1] = lerp(cols[0], (96, 44, 40), max(0.0, (k - 0.5) / 0.5))
        st = getattr(p, "style", style)
        if st == "luoi":  # lưỡi lửa kiểu tranh tướng: ngọn ngả ngược hướng bay và lên (lửa bị kéo theo), sọc màu to theo dáng lưỡi
            d = unit(-unit(p.vel) * 0.5 + np.array([0.0, -1.0]) * 0.5) if sp > 30 else np.array([0.0, -1.0])
            ang = tip_angle(d)
            frl = [1.0, 1.0, 0.8, 0.6, 0.38]
            for i, c in enumerate(layer_cols):
                rad = rr[i] if i < 2 else min(rr[1] * frl[i], rr[i] * 1.3)
                if rad < 1.0:
                    continue
                shift = -d * (r - rad) * 0.45
                sz = 2.7 * rad + (ink if i == 0 else 0)
                out.append(item(p.group, 20 + i, "lobe_s" if i == 0 else "lobe", p.seed % 8, c, p.pos + shift, sz, 1.0, ang))
            return out
        if st == "nhon":
            d = unit(p.vel) * 0.55 + np.array([0.0, -1.0]) * 0.45 if sp > 30 else np.array([0.0, -1.0])
            d = unit(d)
            ang = tip_angle(d)
            fr = [1.0, 1.0, 0.9, 0.78, 0.6]  # lưỡi nhọn: lõi to hơn cụm tròn (hình mảnh, lõi nhỏ là thành giọt nâu)
            for i, c in enumerate(layer_cols):
                rad = rr[i] if i < 2 else min(rr[1] * fr[i], rr[i] * 1.25)
                if rad < 1.0:
                    continue
                shift = -d * (r - rad) * 0.4  # lõi dồn về đáy lưỡi
                sz = 2.8 * rad + (ink if i == 0 else 0)
                out.append(item(p.group, 20 + i, "hook_s" if i == 0 else "hook", p.seed % 4, c, p.pos + shift, sz, 1.0, ang))
            return out
        stretch = 1.0 + min(1.6 if st == "nham" else 0.7, sp / stretch_k)
        ang = -math.degrees(math.atan2(p.vel[1], p.vel[0])) if sp > 5 else p.ang
        for i, c in enumerate(layer_cols):
            rad = rr[i]
            if rad < 1.0:
                continue
            if st == "xoan" and i >= 2:  # lưỡi cam xoắn trên khối đỏ sẫm
                d = unit(np.array([math.cos(p.ang), -abs(math.sin(p.ang)) - 0.6]))
                out.append(item(p.group, 20 + i, "xhook", (p.seed + i) % 4, c, p.pos - d * (r - rad) * 0.25, 2.9 * rad, 1.0,
                                tip_angle(d)))
                continue
            sz = 2 * rad + (ink if i == 0 else 0)
            out.append(item(p.group, 20 + i, "solid" if i == 0 else "blob", p.seed % 4, c, p.pos, sz, stretch, ang))
        if st == "xoan" and p.seed % 2 == 0 and r > 6:  # vòng xoắn đỏ sẫm trên khối đỏ
            out.append(item(p.group, 21.5, "curl", p.seed % 3, (240, 128, 44), p.pos + np.array([r * 0.25, 0]), 1.3 * r, 1.0,
                            math.degrees(p.ang)))
        return out
    return draw


def smoothstep(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def mat_smoke(pal=SMOKE_DARK, erode=False, ink=4.0, grow=0.27):
    """khói: viền mực + ruột, màu theo tuổi (than đen -> xám -> xám nhạt). Tan DẦN, không vụt tắt (người dùng dặn 2026-11-10):
    cụm lớn bị ăn mòn tới lưỡi liềm dày, đồng thời co mượt còn ~25% cỡ và nhạt dần bằng alpha phẳng ở 30% cuối đời
    (viền mực nhạt trước, ruột nhạt sau, để mực không lộ qua ruột); cụm nhỏ co mượt và nhạt dần."""
    def draw(p, k):
        # nở nhanh tới đỉnh ở 27% đời rồi co mượt (smoothstep, dốc 0 ở cuối) như khói Epic Toon FX; mọi thứ đổi liên tục,
        # không đổi khung (đổi khung ăn mòn làm khói giật)
        if k < grow:
            r = p.r0 + (p.r1 - p.r0) * ease_out(k / grow)
        else:
            r = p.r1 * (1 - 0.85 * smoothstep(grow, 1.0, k))
        c = ramp(pal, k ** 0.8)
        g = p.group
        a_ink = 1 - smoothstep(0.45, 0.85, k)
        a_fill = 1 - smoothstep(0.6, 1.0, k)
        if a_fill < 0.03:
            return []
        if p.r1 > 14 and erode:
            fr = min(3, int(max(0.0, (k - 0.55) / 0.35) * 4))  # chỉ bị cắn khi đã ngả xám (đen bị cắn trông như trăng đen)
            r *= 1 - 0.75 * smoothstep(0.55, 1.0, k)
            sd = (p.seed % 4) * 10 + fr
            ang = math.degrees(p.ang)
            out = [item(g, 11, "erode_f", sd, c, p.pos, 2.12 * r, 1.0, ang, a_fill)]
            if a_ink > 0.03:
                out.insert(0, item(g, 10, "erode_r", sd, INK, p.pos, 2.12 * r, 1.0, ang, a_ink))
            return out
        if r < 0.8:
            return []
        ang = math.degrees(p.ang)
        out = [item(g, 11, "sblob", p.seed % 4, c, p.pos, 2 * r, 1.0, ang, a_fill)]
        if a_ink > 0.03:
            out.insert(0, item(g, 10, "ssolid", p.seed % 4, INK, p.pos, 2 * r + ink, 1.0, ang, a_ink))
        return out
    return draw


def mat_sprite(name, layer=40, col=None, size=10.0, size_fn=None, stretch_fn=None, align=False, alpha_fn=None):
    def draw(p, k):
        s = size_fn(p, k) if size_fn else size
        if s < 0.6:
            return []
        stc = stretch_fn(p, k) if stretch_fn else 1.0
        ang = -math.degrees(math.atan2(p.vel[1], p.vel[0])) if align and np.hypot(*p.vel) > 1 else math.degrees(p.ang)
        a = alpha_fn(p, k) if alpha_fn else 1.0
        return [item(p.group, layer, name, p.seed, getattr(p, "col", col), p.pos, s, stc, ang, a)]
    return draw


def mat_ring(pal_col=(240, 140, 50), squash=0.32, thick_seq=None, size_fn=None, layer=30, band=(7.0, 1.5), ink=True):
    """vòng sóng phẳng: dải màu (band px theo đơn vị sân: đầu -> cuối, mảnh dần) + viền mực cố định, bóp dẹt thành elip,
    nhạt dần ở 30% cuối."""
    def draw(p, k):
        R = size_fn(p, k)
        if R < 1:
            return []
        col = getattr(p, "col", pal_col)
        bw = int(round((band[0] + (band[1] - band[0]) * k) * K))
        a = 1 - max(0.0, (k - 0.7) / 0.3)
        return [item(p.group, layer, "ringpx" if ink else "ringpx0", bw, col, p.pos, 2 * R * squash, 1 / squash, 0, a)]
    return draw


# ---------------- hạt dựng sẵn (Initialize) ----------------
def spark(sim, pos, d, speed, life=None, size=8.0, grav=400.0, group=FRONT, drag=5.0, rng=None):
    rng = rng or sim.rng
    p = P(pos, unit(d) * speed, life or rng.uniform(0.3, 0.5), drag=drag, acc=np.array([0, grav]), seed=rng.randint(2),
          group=group, rng=rng)
    p.draw = mat_sprite("streak", 40, (255, 255, 255), align=True,
                        size_fn=lambda q, k: size * (1 - k ** 2), stretch_fn=lambda q, k: max(1.6, min(3.6, np.hypot(*q.vel) / 90)))
    return sim.add(p)


def ember(sim, pos, vel=None, life=None, size=9.0, group=FRONT, rng=None):
    rng = rng or sim.rng
    v = vel if vel is not None else np.array([rng.uniform(-40, 40), rng.uniform(-90, -50)])
    p = P(pos, v, life or rng.uniform(0.7, 1.2), drag=1.6, seed=rng.randint(2), spin=rng.uniform(0, 6.28), group=group)
    p.upd = lambda q, dt, s: q.vel.__setitem__(0, q.vel[0] + math.sin(q.age * 7 + q.spin) * 80 * dt)
    p.draw = mat_sprite("ember", 41, (255, 255, 255), size_fn=lambda q, k: size * (1 - k ** 3))
    return sim.add(p)


def ash(sim, pos, vel=None, life=None, group=FRONT, dark=None, rng=None):
    """tro: mảnh dẹt đen than hoặc xám, bay lên chậm, lượn ngang, lật (bóp cao theo cos) rồi rơi dần."""
    rng = rng or sim.rng
    v = vel if vel is not None else np.array([rng.uniform(-35, 35), rng.uniform(-70, -30)])
    dk = rng.uniform() < 0.55 if dark is None else dark
    col = lerp((34, 30, 30), (70, 64, 62), rng.uniform()) if dk else lerp((140, 136, 132), (196, 192, 188), rng.uniform())
    p = P(pos, v, life or rng.uniform(1.0, 1.8), drag=1.4, acc=np.array([0, 26.0]), seed=rng.randint(4),
          spin=rng.uniform(-5, 5), group=group, col=col, ph=rng.uniform(0, 6.28), sz=rng.uniform(4.5, 8))
    p.upd = lambda q, dt, s: q.vel.__setitem__(0, q.vel[0] + math.sin(q.age * 3.2 + q.ph) * 55 * dt)
    p.draw = lambda q, k: [item(q.group, 42, "ash", q.seed, q.col, q.pos, q.sz * (1 - k ** 4),
                                1.0 / max(0.25, abs(math.cos(q.age * 6 + q.ph))) * 0.5 + 0.5, math.degrees(q.ang))]
    return sim.add(p)


def smoke(sim, pos, vel=None, life=None, r0=8.0, r1=24.0, pal=SMOKE_DARK, group=FRONT, erode=False, rise=30.0, with_ash=0.35,
          rng=None):
    rng = rng or sim.rng
    v = vel if vel is not None else np.array([rng.uniform(-30, 30), rng.uniform(-70, -40)])
    p = P(pos, v, life or rng.uniform(1.0, 1.5), drag=1.4, acc=np.array([0, -rise]), seed=rng.randint(4),
          spin=rng.uniform(-0.8, 0.8), spin_drag=1.2, ang=rng.uniform(0, 6.28), r0=r0, r1=r1, group=group,
          ph=rng.uniform(0, 6.28), rng=rng)
    def upd(q, dt, s):  # lượn ngang, càng về cuối càng bay lên nhanh (khói nhẹ dần)
        q.vel[0] += math.sin(q.age * 5 + q.ph) * 30 * dt
        q.vel[1] -= 70 * (q.age / q.life) * dt
    p.upd = upd
    p.draw = mat_smoke(pal, erode)
    if with_ash and rng.uniform() < with_ash:  # tro tán ra từ khói khi khói tan
        p.on_death = lambda q, s: [ash(s, q.pos + q.rng.uniform(-q.r1 * 0.4, q.r1 * 0.4, 2), group=q.group, rng=q.rng)
                                   for _ in range(q.rng.randint(1, 3))]
    return sim.add(p)


def flame(sim, pos, vel, life, r0, r1, style="tron", pal="lua", group=FRONT, drag=1.8, acc=(0, -320), heat=1.0,
          smoke_p=0.25, smoke_pal=SMOKE_DARK, smoke_big=1.0, ember_p=0.12, rng=None):
    rng = rng or sim.rng
    p = P(pos, vel, life, drag=drag, acc=np.array(acc, float), seed=rng.randint(4), r0=r0, r1=r1, group=group,
          ang=rng.uniform(0, 6.28), spin=rng.uniform(-3, 3), heat=heat, style=style, rng=rng)
    p.draw = mat_flame(style, pal)

    def die(q, s):
        if q.rng.uniform() < smoke_p:
            smoke(s, q.pos, r0=q.r1 * 0.22 * smoke_big, r1=q.r1 * 0.55 * smoke_big, pal=smoke_pal,
                  group=getattr(q, "smoke_group", q.group), rng=q.rng)
        if q.rng.uniform() < ember_p:
            ember(s, q.pos, group=q.group, rng=q.rng)
    p.on_death = die
    return sim.add(p)


def heat(sim, pos, h=50.0, life=None, vy=None, n=2, group=FRONT, rng=None, col=(255, 238, 212)):
    """hơi nóng bốc lên: n nét lượn mảnh song song, uốn liên tục (pha chạy theo tuổi), hiện dần rồi nhạt dần."""
    rng = rng or sim.rng
    p = P(pos, (rng.uniform(-6, 6), -(vy or rng.uniform(45, 75))), life or rng.uniform(1.1, 1.5), drag=0.3, group=group,
          ph=rng.uniform(0, 24), hh=h, n=n, gap=rng.uniform(6, 9), col=col)

    def draw(q, k):
        a = min(1.0, k / 0.25, (1 - k) / 0.35) * 0.75
        if a < 0.03:
            return []
        out = []
        for i in range(q.n):
            seed = int(q.ph + q.age * 30 + i * 7) % 24
            off = np.array([(i - (q.n - 1) / 2) * q.gap, i * 5.0])
            out.append(item(q.group, 39, "haze", seed, q.col, q.pos + off, q.hh * (0.85 + 0.3 * k), 0.16, 0, a))
        return out
    p.draw = draw
    return sim.add(p)


def ring(sim, pos, life, R0, R1, col=(248, 178, 64), squash=0.32, group=FLOOR, layer=30, band=(7.0, 1.5), ink=True):
    p = P(pos, (0, 0), life, group=group, col=col)
    p.draw = mat_ring(col, squash, size_fn=lambda q, k: R0 + (R1 - R0) * ease_out(k), layer=layer, band=band, ink=ink)
    return sim.add(p)


# ---------------- tướng, nền, xuất ----------------
def load_hero(rel, height, flip=False):
    """tranh tướng GPT nền trắng -> cắt nền (loang từ mép), cắt sát, thu theo chiều cao (px)."""
    im = Image.open(os.path.join(HERE, rel)).convert("RGBA")
    w0, h0 = im.size
    work = im.convert("RGB").copy()
    for seed in ((0, 0), (w0 - 1, 0), (0, h0 - 1), (w0 - 1, h0 - 1), (w0 // 2, 0), (w0 // 2, h0 - 1)):
        ImageDraw.floodfill(work, seed, (255, 0, 255), thresh=40)
    a = np.asarray(im).copy()
    mask = np.all(np.asarray(work) == (255, 0, 255), axis=2)
    a[mask, 3] = 0
    im = Image.fromarray(a, "RGBA")
    im = im.crop(im.getbbox())
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    s = height / im.height
    return im.resize((max(1, int(im.width * s)), int(height)), Image.LANCZOS)


class Stage:
    def __init__(self, bg="battle_hoa_c01.png", heroes=True, plain=None, me="inbox/huyen_viem_2/tai_ve/L1_lien.png",
                 foe="inbox/hoa_tinh_1/tai_ve/L1_lien.png"):
        Wp, Hp = W * K + 2 * M, Hs * K + 2 * M
        if plain:
            self.bg = Image.new("RGBA", (Wp, Hp), plain + (255,))
        else:
            src = Image.open(os.path.join(ROOT, "Assets", "03 Art", "BattleBG", bg)).convert("RGBA")
            src = src.resize((Wp, int(src.height * Wp / src.width)))
            top = max(0, (src.height - Hp) // 2 - 120)
            self.bg = src.crop((0, top, Wp, top + Hp))
        self.heroes = {}
        if heroes:
            self.heroes["me"] = (load_hero(me, H * 1.15 * K, flip=True), ME)
            self.heroes["foe"] = (load_hero(foe, H * K), FOE)
        self.tint_cache = {}

    def hero_img(self, name, fx):
        im, _ = self.heroes[name]
        if not fx or fx.get("amt", 0) < 0.02:
            return im
        q = int(fx["amt"] * 12)
        key = (name, fx["tint"], q)
        if key not in self.tint_cache:
            a = np.asarray(im).astype(np.float32)
            amt = q / 12
            lum = a[..., :3].mean(axis=2, keepdims=True)
            wgt = np.clip((lum - 70) / 70, 0, 1) * amt  # giữ nét viền mực: chỉ nhuộm phần tô màu
            a[..., :3] = a[..., :3] * (1 - wgt) + np.array(fx["tint"], np.float32) * wgt
            self.tint_cache[key] = Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")
        return self.tint_cache[key]


def render(sim, art, stage):
    im = stage.bg.copy()
    items = []
    for p in sim.ps:
        if p.draw:
            items += p.draw(p, min(0.999, p.age / p.life))
    for name, (img, foot) in stage.heroes.items():
        items.append((HERO, 0, "@" + name, 0, None, (foot[0], foot[1]), 0, 0, 0, 1))
    items.sort(key=lambda it: (it[0], it[1]))
    for g, l, name, seed, col, pos, w, h, ang, alpha in items:
        if name.startswith("@"):
            hn = name[1:]
            fx = sim.hero_fx.get(hn, {})
            img = stage.hero_img(hn, fx)
            off = fx.get("off", (0, 0))
            sq = fx.get("sq", (1, 1))
            if sq != (1, 1):
                img = img.resize((int(img.width * sq[0]), int(img.height * sq[1])), Image.BILINEAR)
            x = pos[0] * K + M - img.width / 2 + off[0] * K
            y = pos[1] * K + M - img.height + off[1] * K
            sh = art.render("ell", 0, (40, 24, 20), img.width * 0.62, 18 * K, 0, 0.35)
            im.alpha_composite(sh, (int(pos[0] * K + M - sh.width / 2), int(pos[1] * K + M - sh.height / 2)))
            im.alpha_composite(img, (int(x), int(y)))
            continue
        if name == "polys":  # seed = ((đỉnh, màu, nở), ...)
            art.polys(im, seed, alpha)
            continue
        if name == "poly":  # seed = các đỉnh, w = phần nở thêm
            art.poly(im, seed, col, alpha, w)
            continue
        t = art.render(name, seed, col, w * K, h * K, ang, alpha)
        x, y = int(pos[0] * K + M - t.width / 2), int(pos[1] * K + M - t.height / 2)
        if x > im.width or y > im.height or x + t.width < 0 or y + t.height < 0:
            continue
        im.alpha_composite(t, (x, y))
    if sim.flash > 0.01:
        im = Image.blend(im, Image.new("RGBA", im.size, (255, 246, 214, 255)), min(0.55, sim.flash))
    tr = sim.trauma ** 2
    dx = 12 * K * tr * math.sin(sim.t * 2 * math.pi * 11.7)
    dy = 8 * K * tr * math.sin(sim.t * 2 * math.pi * 14.3 + 1)
    return im.crop((int(M + dx), int(M + dy), int(M + dx) + W * K, int(M + dy) + Hs * K))


def run(build, out_dir, name, dur, loop=None, seed=1, stage=None, label=None, sub=4):
    """build(sim) dựng lịch; loop = chu kỳ (giây) nếu clip lặp: mô phỏng 2 chu kỳ khởi động rồi lấy chu kỳ thứ 3."""
    os.makedirs(out_dir, exist_ok=True)
    sim, art = Sim(seed), Art()
    stage = stage or Stage()
    build(sim)
    frames = []
    t_start = 2 * loop if loop else 0.0
    n = int(round((loop or dur) * FPS))
    while sim.t < t_start - 1e-9:
        for _ in range(sub):
            sim.step(1 / FPS / sub)
    for i in range(n):
        frames.append(render(sim, art, stage))
        for _ in range(sub):
            sim.step(1 / FPS / sub)
    save(frames, out_dir, name, label, hold=0 if loop else 8)
    return frames


def _font(sz):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def save(frames, out_dir, name, label=None, hold=8):
    small = [f.convert("RGB").resize((540, int(540 * f.height / f.width)), Image.LANCZOS) for f in frames]
    if label:  # chuỗi (góc trên trái) hoặc [(x, y, chữ)] theo toạ độ sân
        fnt = _font(20)
        labs = [(12 / (540 / W) / 1, 10, label)] if isinstance(label, str) else label
        for f in small:
            d = ImageDraw.Draw(f)
            for x, y, tx in labs:
                xx = 12 if isinstance(label, str) else x * f.width / W - d.textlength(tx, font=fnt) / 2
                d.text((xx, y * f.height / Hs if not isinstance(label, str) else 10), tx, fill=(43, 33, 24), font=fnt,
                       stroke_width=3, stroke_fill=(255, 250, 236))
    idx = [int(x) for x in np.linspace(0, len(small) - 1, 6)]
    strip = Image.new("RGB", (small[0].width, small[0].height * len(idx)))
    for j, i in enumerate(idx):
        strip.paste(small[i], (0, j * small[0].height))
    pal = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    gif = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in small]
    gif[0].save(os.path.join(out_dir, name + ".gif"), save_all=True, append_images=gif[1:] + [gif[-1]] * hold,
                duration=int(1000 / FPS), loop=0, optimize=True)
    pick = [int(x) for x in np.linspace(min(3, len(frames) - 1), len(frames) - 1, 12)]
    tw = 540
    th = int(tw * frames[0].height / frames[0].width)
    sheet = Image.new("RGB", (tw * 4, th * 3), (255, 255, 255))
    fnt = _font(16)
    for j, fi in enumerate(pick):
        f = small[fi].copy()
        ImageDraw.Draw(f).text((tw - 90, 8), f"t={fi / FPS:.2f}s", fill=(0, 0, 0), font=fnt)
        sheet.paste(f, ((j % 4) * tw, (j // 4) * th))
    sheet.save(os.path.join(out_dir, name + "_soi.png"))
