"""Bản thử hiệu ứng PHUN LỬA (2026-11-10): mô phỏng hạt rồi xuất GIF để soi trước khi đưa vào sân (StageView).

Chia như VFX Graph (skill unity-vfx-graph): Spawn (nhịp sinh) -> Initialize (vị trí, tốc, đời) -> Update (cản, nổi, rối, đổi lớp
màu theo tuổi) -> Output (vẽ). Phần Output làm theo luật tô phẳng (skill pokiclash-hero-fx): không glow, không additive, không
gradient. Mỗi hạt lửa vẽ thành nhiều lớp phẳng chồng nhau (mực > đỏ > cam > vàng > kem), lớp trong co nhanh hơn theo tuổi
nên lửa "nguội" dần từ lõi kem ra mép đỏ rồi thành khói. Mọi hạt cùng lớp hoà thành một khối, chỉ khối ngoài có viền mực.

Nhịp học từ Clash of Critters (đọc prefab FX trên máy, không lấy hình): lửa cháy đời 0,3-0,8 s, nón 25°, rối nhẹ, cản 0,3;
bụi/tia văng bắn 2 đợt cách 0,1 s, trọng lực 0,2-0,5; khói là cụm mây kem tô phẳng, tan bằng cách CO NHỎ (không mờ dần).

Toạ độ: khung sân 540 x 464 (y xuống), như StageView; ảnh ra nhân K.
Chạy: py -3 -I phun_lua_thu.py <thư mục ra>   (ra phun_lua.gif, phun_lua_soi.png)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

import fire

HERE = os.path.dirname(os.path.abspath(__file__))
ERODE = os.environ.get("ERODE", "0") == "1"  # ERODE=1: khói tan bằng ăn mòn (học từ Epic Toon FX); mặc định: co nhỏ như bản chuẩn mốc
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
K = 2
FPS = 30
DUR = 1.9
H = 150.0  # chiều cao tướng chuẩn (đơn vị sân)
ME, FOE = np.array([392.0, 418.0]), np.array([158.0, 236.0])  # chân phe mình, địch (StageView.Pos)
MOUTH = ME + np.array([-34.0, -0.62 * H * 1.15])
TARGET = FOE + np.array([0.0, -0.45 * H])

COL = {  # màu phẳng
    "ink": fire.INK, "red": (222, 86, 50), "orange": (240, 140, 50), "yellow": (247, 204, 72), "cream": (252, 241, 200),
    "smoke": (238, 230, 214), "smoke_old": (204, 194, 184),
}

# --- nhịp ---
T_CHARGE = 0.0, 0.28  # tụ lực ở miệng
T_BREATH = 0.28, 1.18  # phun
RATE = 72.0  # hạt lửa / giây lúc phun đều
CONE = math.radians(12)  # nửa góc nón lúc ra khỏi miệng
DRAG = 1.8  # cản lửa (1/s)
HIT_FRONT = 34.0  # lửa dừng ở mặt trước thân đối thủ (cách tâm thân), không trùm qua người


class P:
    __slots__ = ("kind", "pos", "vel", "age", "life", "r0", "r1", "seed", "col", "spin", "rot", "hit", "tg")

    def __init__(self, kind, pos, vel, life, r0, r1, seed, col=None):
        self.kind, self.pos, self.vel, self.age, self.life = kind, np.array(pos, float), np.array(vel, float), 0.0, life
        self.r0, self.r1, self.seed, self.col, self.spin, self.rot, self.hit, self.tg = r0, r1, seed, col, 0.0, 0.0, False, False


def ease_out(x):
    return 1 - (1 - min(1.0, max(0.0, x))) ** 3


class Sim:
    def __init__(self, seed=1):
        self.rng = np.random.RandomState(seed)
        self.ps = []
        self.acc = 0.0
        self.t = 0.0
        self.n = 0
        d = TARGET - MOUTH
        self.dist = float(np.hypot(*d))
        self.u = d / self.dist
        self.nrm = np.array([-self.u[1], self.u[0]])
        self.burst_done = set()

    # ---------- Spawn + Initialize ----------
    def spawn_flame(self, k_ramp):
        rng = self.rng
        a = rng.uniform(-1, 1) * CONE * (1.25 if k_ramp < 1 else 1)
        ca, sa = math.cos(a), math.sin(a)
        dirv = self.u * ca + self.nrm * sa
        sp = rng.uniform(1200, 1400)
        life = rng.uniform(0.40, 0.52)
        r1 = rng.uniform(32, 40) * (0.8 + 0.2 * k_ramp)
        p = P("flame", MOUTH + dirv * rng.uniform(0, 8), dirv * sp, life, rng.uniform(7, 10), r1, self.n % 4)
        p.spin = rng.uniform(0, 6.28)
        p.tg = rng.uniform() < 0.35  # lưỡi lửa liếm lên ở mép
        self.ps.append(p)
        self.n += 1

    def spawn_smoke(self, pos, big=1.0):
        rng = self.rng
        v = np.array([rng.uniform(-30, 30), rng.uniform(-70, -40)]) - self.u * rng.uniform(0, 30)
        p = P("smoke", pos + rng.uniform(-6, 6, 2), v, rng.uniform(0.6, 0.95), rng.uniform(6, 9) * big,
              rng.uniform(18, 26) * big, self.n % 4)
        p.spin = rng.uniform(0, 6.28)
        self.ps.append(p)
        self.n += 1

    def spawn_spark(self, pos, dirv, sp):
        rng = self.rng
        p = P("spark", pos, dirv * sp, rng.uniform(0.28, 0.48), 1, 1, self.n % 2)
        self.ps.append(p)
        self.n += 1

    def spawn_ember(self, pos):
        rng = self.rng
        p = P("ember", pos, np.array([rng.uniform(-40, 40), rng.uniform(-90, -50)]), rng.uniform(0.7, 1.1), 1, 1, self.n % 2)
        p.spin = rng.uniform(0, 6.28)
        self.ps.append(p)
        self.n += 1

    def spawn_charge(self):
        rng = self.rng
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(55, 80)
        pos = MOUTH + np.array([math.cos(a), math.sin(a)]) * d
        p = P("charge", pos, (MOUTH - pos) * 2.2, 0.24, 1, 1, self.n % 2)
        p.spin = rng.uniform(0, 6.28)
        self.ps.append(p)
        self.n += 1

    def spawn(self, dt):
        t, rng = self.t, self.rng
        # tụ lực: vệt bay vào miệng, cầu lửa nhỏ nở ở miệng
        if T_CHARGE[0] <= t < T_CHARGE[1] - 0.08 and rng.uniform() < dt * 40:
            self.spawn_charge()
        if T_CHARGE[0] + 0.06 <= t < T_BREATH[0] and rng.uniform() < dt * 30:
            ball = P("flame", MOUTH + rng.uniform(-4, 4, 2), self.u * 25 + rng.uniform(-15, 15, 2), 0.22, 4,
                     10 + 26 * (t - T_CHARGE[0]) / (T_BREATH[0] - T_CHARGE[0]), self.n % 4, col="ball")
            self.ps.append(ball)
            self.n += 1
        # phun: nhịp lên nhanh 0,08 s, đầu luồng to; tắt dần 0,16 s cuối
        if T_BREATH[0] <= t < T_BREATH[1]:
            x = t - T_BREATH[0]
            ramp = min(1.0, x / 0.08)
            tail = min(1.0, (T_BREATH[1] - t) / 0.16)
            self.acc += dt * RATE * (1.5 if x < 0.1 else 1.0) * tail
            while self.acc >= 1:
                self.acc -= 1
                self.spawn_flame(ramp)
            # khói bốc liên tục từ mép trên luồng (phía xa miệng), gộp thành đám mây kem
            if rng.uniform() < dt * 20 * tail and x > 0.12:
                s = rng.uniform(0.45, 0.95)
                up = self.nrm if self.nrm[1] < 0 else -self.nrm
                self.spawn_smoke(MOUTH + self.u * self.dist * s + up * rng.uniform(14, 26) * (0.6 + s), 0.8 + 0.5 * s)
            # tia văng dọc luồng, ra từ mép, bay ra ngoài
            if rng.uniform() < dt * 14 * tail:
                s = rng.uniform(0.25, 0.8)
                sd = rng.choice([-1, 1])
                pos = MOUTH + self.u * self.dist * s + self.nrm * sd * rng.uniform(18, 30) * (0.5 + s)
                side = self.nrm * sd
                dv = self.u * rng.uniform(0.5, 1.0) + side * rng.uniform(0.4, 0.9) + np.array([0, -0.3])
                self.spawn_spark(pos, dv / np.hypot(*dv), rng.uniform(260, 420))
        # hết phun: một đám khói đọng ở đầu luồng
        if t >= T_BREATH[1] - 0.05 and "tail" not in self.burst_done:
            self.burst_done.add("tail")
            for _ in range(6):
                self.spawn_smoke(MOUTH + self.u * self.dist * rng.uniform(0.55, 0.9) + rng.uniform(-18, 18, 2), 1.15)
        # trúng: 2 đợt tia văng cách 0,1 s (Clash of Critters), lúc đầu luồng tới đích
        t_hit = T_BREATH[0] + 0.24
        for i, tb in enumerate((t_hit, t_hit + 0.1, t_hit + 0.4)):
            if t >= tb and i not in self.burst_done:
                self.burst_done.add(i)
                for _ in range(5 if i < 2 else 3):
                    a = math.atan2(-self.u[1], -self.u[0]) + rng.uniform(-1.4, 1.4)
                    dv = np.array([math.cos(a), math.sin(a) - 0.5])
                    self.spawn_spark(TARGET + rng.uniform(-10, 10, 2), dv / np.hypot(*dv), rng.uniform(250, 460))

    # ---------- Update ----------
    def update(self, dt):
        self.spawn(dt)
        rng = self.rng
        alive = []
        for p in self.ps:
            p.age += dt
            k = p.age / p.life
            if k >= 1:
                if p.kind == "flame" and p.col != "ball":
                    if rng.uniform() < (0.3 if p.hit else 0.45):
                        self.spawn_smoke(p.pos, 0.75 if p.hit else 1.0)
                    if rng.uniform() < 0.15:
                        self.spawn_ember(p.pos)
                continue
            if p.kind == "flame":
                p.vel *= math.exp(-DRAG * dt)  # cản
                p.vel[1] -= 320 * dt * min(1, k * 2)  # lửa nổi lên dần
                # rối: lệch vuông góc theo sin (mượt, có hạt giống), mạnh dần theo tuổi
                w = math.sin(p.age * 17 + p.spin) * 260 * k
                p.vel += self.nrm * w * dt
                # chạm đích: toả ra hai bên và lên, không xuyên qua người
                along = float(np.dot(p.pos - MOUTH, self.u))
                if along > self.dist - HIT_FRONT and not p.hit:
                    p.hit = True
                    vu = float(np.dot(p.vel, self.u))
                    side = 1 if float(np.dot(p.pos - MOUTH, self.nrm)) >= 0 else -1
                    p.vel += -self.u * vu * 0.92 + self.nrm * side * abs(vu) * rng.uniform(0.15, 0.32)
                    p.life = min(p.life, p.age + rng.uniform(0.1, 0.16))
                    p.r1 = min(p.r1, flame_layers(p)[0] * 1.05)  # không nở thêm khi đã chạm
                    p.r0 = min(p.r0, p.r1)
                if p.hit:
                    p.vel[1] += 320 * dt * min(1, k * 2)  # bỏ lực nổi: tạt sát thân, không cuộn lên trời
            elif p.kind == "smoke":
                p.vel *= math.exp(-1.4 * dt)
                p.vel[0] += math.sin(p.age * 5 + p.spin) * 30 * dt
                p.vel[1] -= 30 * dt
            elif p.kind == "spark":
                p.vel *= math.exp(-2.2 * dt)
                p.vel[1] += 0.45 * 900 * dt
            elif p.kind == "ember":
                p.vel *= math.exp(-1.6 * dt)
                p.vel[0] += math.sin(p.age * 7 + p.spin) * 80 * dt
            elif p.kind == "charge":
                p.vel *= 1 + 3 * dt  # tốc nhân e^(3t)
            p.pos = p.pos + p.vel * dt
            alive.append(p)
        self.ps = alive
        self.t += dt


# ---------- Output ----------
class Art:
    def __init__(self):
        self.blob = [fire.blob(s)[0] for s in range(4)]
        self.solid = [fire.blob_solid(s)[0] for s in range(4)]
        self.tongue = [fire.tongue(s)[0] for s in range(4)]
        self.tongue_solid = [fire.tongue(s, solid=True)[0] for s in range(4)]
        self.streak = [fire.streak(s)[0] for s in range(2)]
        self.ember = [fire.ember(s)[0] for s in range(2)]
        self.erode = [fire.erode_frames(s) for s in range(4)] if ERODE else None
        self.cache = {}

    def tinted(self, key, im, col, size, ang=0.0, stretch=1.0):
        w = max(2, int(round(size * stretch)))
        h = max(2, int(round(size)))
        ck = (key, col, w, h, int(ang / 6))
        if ck not in self.cache:
            a = np.asarray(im.resize((w, h), Image.BILINEAR)).astype(np.float32)
            a[..., :3] *= np.array(col, np.float32) / 255.0
            t = Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")
            if ang:
                t = t.rotate(int(ang / 6) * 6, resample=Image.BILINEAR, expand=True)
            self.cache[ck] = t
        return self.cache[ck]


def lerp(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def flame_layers(p):
    """bán kính (đơn vị sân) từng lớp theo tuổi: lõi co trước, viền đỏ sau cùng; cuối đời cả hạt co lại."""
    k = p.age / p.life
    r = p.r0 + (p.r1 - p.r0) * ease_out(k / 0.75) ** 0.8  # nở đều theo quãng bay: luồng loe thành hình nón
    r *= 1 - 0.88 * max(0.0, (k - 0.66) / 0.34) ** 1.3
    cream = r * 0.55 * max(0.0, 1 - k / 0.4) ** 0.7
    yellow = r * 0.74 * max(0.0, 1 - k / 0.68) ** 0.7
    orange = r * 0.88 * max(0.0, 1 - k / 0.95) ** 0.6
    return r, orange, yellow, cream


def render(sim, art, bg):
    im = bg.copy()
    flames = [p for p in sim.ps if p.kind == "flame"]
    smokes = [p for p in sim.ps if p.kind == "smoke"]

    def put(t, pos):
        im.alpha_composite(t, (int(pos[0] * K - t.width / 2), int(pos[1] * K - t.height / 2)))

    # khói: viền mực rồi ruột; tan bằng co nhỏ, màu kem ngả xám theo tuổi
    smk = []
    for p in smokes:
        k = p.age / p.life
        r = p.r0 + (p.r1 - p.r0) * ease_out(k / 0.45)
        if ERODE:  # tan bằng bị "cắn" từ một phía (6 khung, nửa sau đời), chỉ co nhẹ
            # khung 0..3 (tới lưỡi liềm còn dày; cung mảnh hơn chỉ còn viền mực như nét gạch), 15% cuối co về 0
            fr = min(3, int(max(0.0, (k - 0.45) / 0.4) * 4))
            r *= 1 - max(0.0, (k - 0.85) / 0.15)
        else:
            r *= 1 - max(0.0, (k - 0.6) / 0.4) ** 0.85
            fr = -1
        smk.append((p, r, lerp(COL["smoke"], COL["smoke_old"], min(1, k * 0.9)), fr))
    for p, r, c, fr in smk:
        if r > 1.5:
            if fr >= 0:
                put(art.tinted(f"er{fr}", art.erode[p.seed][fr][1], COL["ink"], 2 * r * K * 1.06), p.pos)
            else:
                put(art.tinted("s", art.solid[p.seed], COL["ink"], (2 * r + 5) * K), p.pos)
    for p, r, c, fr in smk:
        if r > 1.5:
            if fr >= 0:
                put(art.tinted(f"ef{fr}", art.erode[p.seed][fr][0], c, 2 * r * K * 1.06), p.pos)
            else:
                put(art.tinted("b", art.blob[p.seed], c, 2 * r * K), p.pos)

    # lửa: kéo dài theo vận tốc (stretched billboard), xoay theo hướng bay
    def fl(p):
        sp = float(np.hypot(*p.vel))
        if p.tg and p.age / p.life > 0.3:  # lưỡi lửa: đầu nhọn chĩa lên, hơi ngả theo hướng bay
            v = p.vel / max(sp, 1) * 0.35 + np.array([0, -1.0])
            return math.degrees(math.atan2(v[0], -v[1])) * -1, 1.0, True
        ang = -math.degrees(math.atan2(p.vel[1], p.vel[0]))
        return ang, 1 + min(0.7, sp / 1100), False
    lay = [(p,) + flame_layers(p) + fl(p) for p in flames]
    for idx, (key, col, ext) in enumerate((("s", COL["ink"], 5), ("b", COL["red"], 0), ("b", COL["orange"], 0),
                                            ("b", COL["yellow"], 0), ("b", COL["cream"], 0))):
        for p, r, o, y, c, ang, st, tg in lay:
            rr = (r, r, o, y, c)[idx]
            if rr < 1.2:
                continue
            if tg:
                src = art.tongue_solid[p.seed] if key == "s" else art.tongue[p.seed]
                put(art.tinted("t" + key, src, col, (2.3 * rr * K + ext * K), ang, 1.0), p.pos)
            else:
                src = art.solid[p.seed] if key == "s" else art.blob[p.seed]
                put(art.tinted(key, src, col, (2 * rr * K + ext * K), ang, st), p.pos)

    for p in sim.ps:
        k = p.age / p.life
        if p.kind == "spark":
            sp = float(np.hypot(*p.vel))
            ang = -math.degrees(math.atan2(p.vel[1], p.vel[0]))
            s = 1 - k ** 2
            t = art.tinted("k", art.streak[p.seed], (255, 255, 255), 8.5 * K * s, ang, max(1.6, min(3.6, sp / 90)))
            put(t, p.pos)
        elif p.kind == "ember":
            put(art.tinted("e", art.ember[p.seed], (255, 255, 255), 9 * K * (1 - k ** 3)), p.pos)
        elif p.kind == "charge":  # than bay vào miệng, to dần khi tới gần
            put(art.tinted("e", art.ember[p.seed], (255, 255, 255), (5 + 6 * k) * K), p.pos)
    return im


def stage_bg():
    """nền sân Hỏa + hai hình nhân xám đứng chỗ hai phe (chỉ để đọc tỉ lệ)."""
    src = Image.open(os.path.join(ROOT, "Assets", "03 Art", "BattleBG", "battle_hoa_c01.png")).convert("RGBA")
    W, Hh = 540 * K, 464 * K
    src = src.resize((W, int(src.height * W / src.width)))
    top = max(0, (src.height - Hh) // 2 - 120)
    bg = src.crop((0, top, W, top + Hh))
    d = ImageDraw.Draw(bg)
    for foot, s in ((ME, 1.15), (FOE, 1.0)):
        w, hh = 0.62 * H * s * K, H * s * K
        x, y = foot[0] * K, foot[1] * K
        d.ellipse([x - w * 0.55, y - 10 * K, x + w * 0.55, y + 8 * K], fill=(60, 40, 30, 90))
        d.ellipse([x - w / 2, y - hh, x + w / 2, y], fill=(150, 146, 140, 255), outline=fire.INK + (255,), width=3 * K)
        hx = x + (-1 if foot is ME else 1) * w * 0.18
        d.ellipse([hx - w * 0.36, y - hh - w * 0.25, hx + w * 0.36, y - hh + w * 0.45], fill=(150, 146, 140, 255),
                  outline=fire.INK + (255,), width=3 * K)
    return bg


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    sim, art, bg = Sim(), Art(), stage_bg()
    frames = []
    n = int(DUR * FPS)
    sub = 4
    for i in range(n):
        for _ in range(sub):
            sim.update(1 / FPS / sub)
        frames.append(render(sim, art, bg))
        print(i, len(sim.ps), file=sys.stderr) if i % 10 == 0 else None
    small = [f.convert("RGB").resize((540, int(540 * f.height / f.width)), Image.LANCZOS) for f in frames]
    probe = [small[int(x * FPS)] for x in (0.3, 0.75, 1.1, 1.45)]  # bảng màu chung lấy từ khung tụ, lửa, khói; không rắc nhiễu
    strip = Image.new("RGB", (probe[0].width, probe[0].height * len(probe)))
    for j, f in enumerate(probe):
        strip.paste(f, (0, j * f.height))
    pal = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    gif = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in small]
    gif[0].save(os.path.join(out_dir, "phun_lua.gif"), save_all=True, append_images=gif[1:] + [gif[-1]] * 8,
                duration=int(1000 / FPS), loop=0, optimize=True)
    # tờ soi: 12 khung
    pick = [int(x) for x in np.linspace(4, n - 1, 12)]
    tw = 540
    th = int(tw * frames[0].height / frames[0].width)
    sheet = Image.new("RGB", (tw * 4, th * 3), (255, 255, 255))
    for j, fi in enumerate(pick):
        f = frames[fi].convert("RGB").resize((tw, th), Image.LANCZOS)
        ImageDraw.Draw(f).text((8, 8), f"t={fi / FPS:.2f}s", fill=(0, 0, 0))
        sheet.paste(f, ((j % 4) * tw, (j // 4) * th))
    sheet.save(os.path.join(out_dir, "phun_lua_soi.png"))
    frames[int(0.75 * FPS)].convert("RGB").save(os.path.join(out_dir, "phun_lua_khung.png"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_phun_lua"))
