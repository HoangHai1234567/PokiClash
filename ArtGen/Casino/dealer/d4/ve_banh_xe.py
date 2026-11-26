# Vẽ bánh xe Vòng Xoay Ngũ Hành (GD_Claude/31 mốc D4) bằng mã, đúng hình học của mô phỏng viên bi
# (Assets/01 Script/Core/Casino/RouletteBall.cs, lớp RouletteWheel: bán kính các vòng, độ cao, 8 mấu chắn, 26 ô và cách xếp ô).
# Nét: viền mực nâu sẫm hơi rung, tô phẳng có vân chì (vân lấy từ nỉ của ảnh nền lều), không bóng, không điểm sáng.
# Ra (thư mục ra/, cỡ gấp đôi cỡ hiện trên sân khấu, R = 640 px):
#   rl_chao.png        lòng chảo đứng yên, đã chiếu nghiêng (x = R·x, y = R·(K·y + KZ·h)); chỗ mâm xoay tô màu nền mâm
#   rl_vanh_truoc.png  nửa gần của vành gỗ + thành ngoài, cùng khung với rl_chao: vẽ ĐÈ lên viên bi (bi chạy sau vành gần)
#   rl_mam.png         mâm xoay nhìn thẳng từ trên (vòng số, vòng ô có vách ngăn, nón giữa); game xoay rồi ép dẹt theo K
#   rl_truc.png        trục giữa (đứng yên, đã chiếu nghiêng)
#   rl_bi.png          viên bi
#   banh_xe.json       khung, tâm, tỉ lệ để menu dựng scene đặt đúng chỗ
#   xem_banh_xe.png    ghép thử (mâm xoay 20°, bi ở ba chỗ) để soi
# Chạy: py -3 -I ve_banh_xe.py
import json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(HERE, "ra")
os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(PROJECT, "Assets", "03 Art", "Fonts", "Baloo2-ExtraBold.ttf")

# ---- hình học: PHẢI khớp RouletteWheel (C#) ----
K, KZ = 0.6, 0.8
R_RIM_IN, R_SLOPE, R_ROTOR, R_RING, R_POCKET, R_CONE = 0.905, 0.80, 0.70, 0.61, 0.555, 0.50
H_RIM, H_TRACK_OUT, H_TRACK_IN, H_BASE = 0.085, 0.07, 0.035, -0.10
BALL_R = 0.040
N_DIAMOND, R_DIAMOND = 8, 0.765
SLOTS = 26
# Người dùng 2026-11-26: "để đỏ đen thôi, nhiều màu quá": ô trên mâm xen kẽ ĐỎ / ĐEN như roulette thật (vị trí chẵn đỏ, lẻ đen), Sao Vàng
# màu vàng; hệ của ô ghi bằng biểu tượng nhỏ màu kem trong lòng ô (không tô ô theo màu hệ nữa).
RED, BLACK, BLACK_POCKET = "#cf3b2e", "#2a2422", "#40383a"
ELEM_ICON = ["e_kim", "e_moc", "e_thuy", "e_hoa", "e_tho"]   # thứ tự Elements.All
STAR = "#f6cf3d"


def pocket_at(slot):
    if slot == SLOTS - 1:
        return 25
    e, q = slot % 5, slot // 5
    return e * 5 + (q + 2 * e) % 5


def height(r):
    def lerp(a, b, t):
        return a + (b - a) * max(0.0, min(1.0, t))
    if r >= R_RIM_IN: return H_RIM
    if r >= R_SLOPE: return lerp(H_TRACK_IN, H_TRACK_OUT, (r - R_SLOPE) / (R_RIM_IN - R_SLOPE))
    if r >= R_ROTOR: return lerp(0.0, H_TRACK_IN, (r - R_ROTOR) / (R_SLOPE - R_ROTOR))
    return 0.0


# ---- bút vẽ ----
SS = 2                    # vẽ gấp đôi rồi thu lại cho mịn
R = 640                   # bán kính vành ngoài ở ảnh ra
RS = R * SS
INK = (59, 36, 22, 255)
random.seed(7)


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def shade(c, k):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c[:3]) + (c[3],)


def mix(c, d, t):
    return tuple(int(round(c[i] + (d[i] - c[i]) * t)) for i in range(3)) + (255,)


def wobble(n, amp, seed):
    """dãy n số nhiễu tần số thấp, khép vòng (cho nét mực hơi rung)"""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 2 * math.pi) for _ in range(4)]
    am = [rnd.uniform(0.4, 1.0) for _ in range(4)]
    fr = [3, 5, 9, 14]
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        out.append(amp * sum(am[k] * math.sin(fr[k] * a + ph[k]) for k in range(4)) / 2.2)
    return out


_grain = None


def grain(size):
    """vân chì: lấy độ sáng của nỉ trong ảnh nền lều, chuẩn hoá quanh 1, lát gương cho đủ cỡ"""
    global _grain
    if _grain is None:
        src = Image.open(os.path.join(HERE, "nen_leu_xoay_2k.jpg")).convert("L").crop((120, 1100, 1020, 2000))
        a = np.asarray(src).astype(np.float32)
        a = a / a.mean()
        a = np.clip(1.0 + (a - 1.0) * 0.55, 0.86, 1.12)
        a = np.concatenate([a, a[:, ::-1]], axis=1)
        _grain = np.concatenate([a, a[::-1]], axis=0)
    w, h = size
    g = _grain
    reps = (h // g.shape[0] + 1, w // g.shape[1] + 1)
    return np.tile(g, reps)[:h, :w]


def apply_grain(img):
    a = np.asarray(img).astype(np.float32)
    g = grain(img.size)[..., None]
    ink = (a[..., :3].sum(axis=2, keepdims=True) < 200)          # nét mực không nhận vân
    rgb = np.where(ink, a[..., :3], np.clip(a[..., :3] * g, 0, 255))
    return Image.fromarray(np.dstack([rgb, a[..., 3:]]).astype(np.uint8), "RGBA")


def finish(img, name, crop=None):
    img = apply_grain(img)
    w, h = img.size
    img = img.resize((w // SS, h // SS), Image.LANCZOS)
    if crop:
        img = img.crop(crop)
    img.save(os.path.join(OUT, name))
    return img


# =====================================================================================================
# 1. lòng chảo (chiếu nghiêng)
PAD = 16
BW = (2 * R + 2 * PAD) * SS
TOP_Y = K * 1.0 + KZ * H_RIM            # điểm cao nhất (vành xa)
BOT_Y = -K * 1.0 + KZ * H_BASE          # điểm thấp nhất (chân thành ngoài, phía gần)
BH = int(((TOP_Y - BOT_Y) * R + 2 * PAD) * SS)
CX = BW / 2
CY = (PAD + TOP_Y * R) * SS             # hàng ảnh của tâm mặt phẳng ô (h = 0)


def P(x, y, h=0.0):
    return (CX + RS * x, CY - RS * (K * y + KZ * h))


def ell(r, h, n=240, wob=0.0, seed=0, a0=0.0, a1=2 * math.pi):
    w = wobble(n, wob, seed) if wob else [0.0] * n
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        rr = r * (1 + w[i % n])
        pts.append(P(rr * math.cos(a), rr * math.sin(a), h))
    return pts


def band(d, r1, h1, r2, h2, fill, a0=0.0, a1=2 * math.pi):
    d.polygon(ell(r1, h1, a0=a0, a1=a1) + ell(r2, h2, a0=a0, a1=a1)[::-1], fill=fill)


def ink_ring(d, r, h, width, seed, a0=0.0, a1=2 * math.pi):
    pts = ell(r, h, wob=0.0035, seed=seed, a0=a0, a1=a1)
    d.line(pts, fill=INK, width=width, joint="curve")


LW = 7 * SS        # nét viền chính
LW2 = 5 * SS       # nét phụ
WOOD_RIM, WOOD_WALL, WOOD_IN = hexc("#d59a57"), hexc("#b0713a"), hexc("#8f5a2d")
TRACK, SLOPE = hexc("#e6b873"), hexc("#c58a4c")
ROTOR_BASE = hexc("#3a2a20")


def draw_rim(d, front_only=False):
    """vành gỗ trên cùng + thành ngoài. front_only: chỉ nửa gần (để vẽ đè lên bi)"""
    a0, a1 = (math.pi, 2 * math.pi) if front_only else (0.0, 2 * math.pi)
    # thành ngoài (chỉ nửa gần thấy được)
    wall = ell(1.0, H_RIM, a0=math.pi, a1=2 * math.pi) + ell(1.0, H_BASE, a0=math.pi, a1=2 * math.pi)[::-1]
    d.polygon(wall, fill=WOOD_WALL)
    # vài nẹp dọc trên thành ngoài
    for i in range(1, 12):
        a = math.pi + math.pi * i / 12
        d.line([P(math.cos(a), math.sin(a), H_RIM), P(math.cos(a), math.sin(a), H_BASE)], fill=shade(WOOD_WALL, 0.82), width=3 * SS)
    d.line(ell(1.0, H_BASE, wob=0.003, seed=3, a0=math.pi, a1=2 * math.pi), fill=INK, width=LW, joint="curve")
    d.line([P(-1, 0, H_RIM), P(-1, 0, H_BASE)], fill=INK, width=LW)
    d.line([P(1, 0, H_RIM), P(1, 0, H_BASE)], fill=INK, width=LW)
    # mặt vành
    band(d, 1.0, H_RIM, R_RIM_IN, H_RIM, WOOD_RIM, a0, a1)
    ink_ring(d, 1.0, H_RIM, LW, 1, a0, a1)
    ink_ring(d, R_RIM_IN, H_RIM, LW2, 2, a0, a1)
    # đinh tán nhỏ trên mặt vành
    for i in range(16):
        a = (i + 0.5) * 2 * math.pi / 16
        if front_only and not (math.pi < a < 2 * math.pi):
            continue
        x, y = P(0.953 * math.cos(a), 0.953 * math.sin(a), H_RIM)
        d.ellipse([x - 7 * SS, y - 5 * SS, x + 7 * SS, y + 5 * SS], fill=hexc("#f2c94c"), outline=INK, width=2 * SS)


bowl = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
d = ImageDraw.Draw(bowl)
# vách trong của vành (thấy ở phía xa), rồi đường bi chạy, sườn dốc, nền mâm
d.polygon(ell(R_RIM_IN, H_RIM), fill=WOOD_IN)
band(d, R_RIM_IN, H_TRACK_OUT, R_SLOPE, H_TRACK_IN, TRACK)
band(d, R_SLOPE, H_TRACK_IN, R_ROTOR, 0.0, SLOPE)
d.polygon(ell(R_ROTOR, 0.0), fill=ROTOR_BASE)
ink_ring(d, R_RIM_IN, H_TRACK_OUT, LW2, 4)
ink_ring(d, R_SLOPE, H_TRACK_IN, 4 * SS, 5)
ink_ring(d, R_ROTOR, 0.0, LW2, 6)
# 8 mấu chắn hình thoi trên sườn dốc (xen kẽ dọc / ngang)
for i in range(N_DIAMOND):
    a = (i + 0.5) * 2 * math.pi / N_DIAMOND
    ca, sa = math.cos(a), math.sin(a)
    lr, lt = (0.040, 0.016) if i % 2 == 0 else (0.018, 0.044)       # nửa dài theo hướng tâm / tiếp tuyến
    hh = height(R_DIAMOND)
    c = (R_DIAMOND * ca, R_DIAMOND * sa)
    pts = [P(c[0] + ca * lr, c[1] + sa * lr, height(R_DIAMOND + lr)), P(c[0] - sa * lt, c[1] + ca * lt, hh + 0.012),
           P(c[0] - ca * lr, c[1] - sa * lr, height(R_DIAMOND - lr)), P(c[0] + sa * lt, c[1] - ca * lt, hh + 0.012)]
    d.polygon(pts, fill=hexc("#f2c94c"))
    d.line(pts + [pts[0]], fill=INK, width=4 * SS, joint="curve")
draw_rim(d)
bowl_img = finish(bowl, "rl_chao.png")

front = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
draw_rim(ImageDraw.Draw(front), front_only=True)
front_img = finish(front, "rl_vanh_truoc.png")

# =====================================================================================================
# 2. mâm xoay (nhìn thẳng từ trên, chưa ép dẹt)
MR = int(R_ROTOR * R)                 # bán kính mâm ở ảnh ra
MS = (MR * 2 + 8) * SS
mc = MS / 2
rot = Image.new("RGBA", (MS, MS), (0, 0, 0, 0))
d = ImageDraw.Draw(rot)


def MP(r, a):
    return (mc + RS * r * math.cos(a), mc - RS * r * math.sin(a))


def wedge(r1, r2, a0, a1, fill, n=10):
    pts = [MP(r2, a0 + (a1 - a0) * i / n) for i in range(n + 1)] + [MP(r1, a1 - (a1 - a0) * i / n) for i in range(n + 1)]
    d.polygon(pts, fill=fill)


step = 2 * math.pi / SLOTS
font = ImageFont.truetype(FONT, int(0.078 * RS))
for s in range(SLOTS):
    p = pocket_at(s)
    red = s % 2 == 0
    col = hexc(STAR) if p == 25 else hexc(RED if red else BLACK)
    a0, a1 = s * step, (s + 1) * step
    wedge(R_RING, R_ROTOR, a0, a1, col)
    wedge(R_CONE, R_RING, a0, a1, shade(col, 0.7) if p == 25 or red else hexc(BLACK_POCKET))
# nón giữa: 13 tia hai màu vàng
for i in range(26):
    wedge(0.105, R_CONE, i * step, (i + 1) * step, hexc("#ecc56a") if i % 2 == 0 else hexc("#dcae4e"))
d.ellipse([mc - 0.105 * RS, mc - 0.105 * RS, mc + 0.105 * RS, mc + 0.105 * RS], fill=hexc("#b5412f"))
# nét mực: các vòng, vạch ngăn vòng số, vách ngăn ô
for r, w, sd in ((R_ROTOR - 0.004, LW2, 11), (R_RING, 4 * SS, 12), (R_CONE, LW2, 13), (0.105, 4 * SS, 14), (0.30, 3 * SS, 15)):
    wb = wobble(240, 0.004, sd)
    d.line([MP(r * (1 + wb[i % 240]), 2 * math.pi * i / 240) for i in range(241)], fill=INK, width=w, joint="curve")
rnd = random.Random(5)
for s in range(SLOTS):
    a = s * step + rnd.uniform(-0.004, 0.004)
    d.line([MP(R_RING, a), MP(R_ROTOR - 0.004, a)], fill=INK, width=3 * SS)
    # vách ngăn ô: thanh kem viền mực
    half = 0.0085
    bar = [MP(R_CONE + 0.004, a - half / R_CONE), MP(R_RING - 0.002, a - half / R_RING), MP(R_RING - 0.002, a + half / R_RING),
           MP(R_CONE + 0.004, a + half / R_CONE)]
    d.polygon(bar, fill=hexc("#f3e4c4"))
    d.line(bar + [bar[0]], fill=INK, width=2 * SS, joint="curve")
# số trên vòng số (đỉnh số quay về tâm), sao ở ô Sao Vàng
for s in range(SLOTS):
    p = pocket_at(s)
    a = (s + 0.5) * step
    cx, cy = MP((R_RING + R_ROTOR) / 2 + 0.002, a)
    tile = Image.new("RGBA", (int(0.14 * RS), int(0.14 * RS)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    tc = tile.size[0] / 2
    if p == 25:
        pts = []
        for i in range(10):
            rr = (0.036 if i % 2 == 0 else 0.016) * RS
            an = math.pi / 2 + i * math.pi / 5
            pts.append((tc + rr * math.cos(an), tc - rr * math.sin(an)))
        td.polygon(pts, fill=hexc("#fff6d6"))
        td.line(pts + [pts[0]], fill=INK, width=3 * SS, joint="curve")
    else:
        td.text((tc, tc), str(p % 5 + 1), font=font, fill=(255, 250, 240, 255), anchor="mm", stroke_width=3 * SS, stroke_fill=INK)
    tile = tile.rotate(math.degrees(a) + 90, resample=Image.BICUBIC)   # đỉnh số quay về tâm: nửa gần người xem đọc xuôi
    rot.alpha_composite(tile, (int(cx - tc), int(cy - tc)))
# biểu tượng hệ trong lòng ô: hình bóng màu kem của icon hệ (Assets/03 Art/Fallback/Icons/e_*.png), đỉnh quay về tâm như chữ số
ICONS = os.path.join(PROJECT, "Assets", "03 Art", "Fallback", "Icons")
isz = int(0.074 * RS)
for s in range(SLOTS):
    p = pocket_at(s)
    if p == 25:
        continue
    a = (s + 0.5) * step
    ic = Image.open(os.path.join(ICONS, ELEM_ICON[p // 5] + ".png")).convert("RGBA")
    box = ic.getbbox()
    ic = ic.crop(box)
    k = isz / max(ic.size)
    ic = ic.resize((max(1, round(ic.width * k)), max(1, round(ic.height * k))), Image.LANCZOS)
    sil = Image.new("RGBA", ic.size, hexc("#f3e4c4"))
    sil.putalpha(ic.split()[3])
    tile = Image.new("RGBA", (isz * 2, isz * 2), (0, 0, 0, 0))
    tile.alpha_composite(sil, (isz - sil.width // 2, isz - sil.height // 2))
    tile = tile.rotate(math.degrees(a) + 90, resample=Image.BICUBIC)
    cx, cy = MP(R_POCKET, a)
    rot.alpha_composite(tile, (int(cx - isz), int(cy - isz)))
rotor_img = finish(rot, "rl_mam.png")

# =====================================================================================================
# 3. trục giữa (đứng yên, chiếu nghiêng): đế, cột, núm
TW, TH = int(0.30 * RS), int(0.34 * RS)
tur = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
d = ImageDraw.Draw(tur)
tcx, base_y = TW / 2, TH - 0.07 * RS


def TE(r, h, fill, w=4 * SS):
    y = base_y - KZ * h * RS
    d.ellipse([tcx - r * RS, y - K * r * RS, tcx + r * RS, y + K * r * RS], fill=fill, outline=INK, width=w)


def TC(r, h0, h1, fill):
    y0, y1 = base_y - KZ * h0 * RS, base_y - KZ * h1 * RS
    d.rectangle([tcx - r * RS, y1, tcx + r * RS, y0], fill=fill)
    d.line([tcx - r * RS, y1, tcx - r * RS, y0], fill=INK, width=4 * SS)
    d.line([tcx + r * RS, y1, tcx + r * RS, y0], fill=INK, width=4 * SS)


BRASS, BRASS_D, RED = hexc("#f0c24e"), hexc("#cf9c33"), hexc("#d2492f")
TE(0.085, 0.0, BRASS_D)
TC(0.085, 0.0, 0.03, BRASS_D)
TE(0.085, 0.03, BRASS)
TE(0.038, 0.03, BRASS_D)
TC(0.038, 0.03, 0.15, BRASS_D)
TE(0.038, 0.15, BRASS)
TE(0.052, 0.185, RED)
tur_img = finish(tur, "rl_truc.png")
TUR_BASE = (TW / 2 / SS, base_y / SS)      # điểm đế trục (tâm mâm, h = 0) trong ảnh rl_truc

# 4. viên bi
BR = int(BALL_R * R)
bs = (BR * 2 + 12) * SS
ball = Image.new("RGBA", (bs, bs), (0, 0, 0, 0))
d = ImageDraw.Draw(ball)
d.ellipse([6 * SS, 6 * SS, bs - 6 * SS, bs - 6 * SS], fill=hexc("#fbf3df"), outline=INK, width=4 * SS)
d.arc([14 * SS, 14 * SS, bs - 14 * SS, bs - 14 * SS], 20, 80, fill=hexc("#d9c9a3"), width=3 * SS)   # nét chì cong, không phải điểm sáng
ball_img = ball.resize((bs // SS, bs // SS), Image.LANCZOS)
ball_img.save(os.path.join(OUT, "rl_bi.png"))

info = {
    "R": R, "K": K, "KZ": KZ,
    "chao": {"size": list(bowl_img.size), "center": [CX / SS, CY / SS]},          # tâm mặt phẳng ô trong ảnh (x, y từ mép trên)
    "mam": {"size": list(rotor_img.size), "radius": MR},
    "truc": {"size": list(tur_img.size), "base": list(TUR_BASE)},
    "bi": {"size": list(ball_img.size), "radius": BR},
}
json.dump(info, open(os.path.join(OUT, "banh_xe.json"), "w"), indent=1)

# =====================================================================================================
# ghép thử để soi: mâm xoay 20 độ, ép dẹt, bi ở ba chỗ (đường chạy xa, đường chạy gần, trong ô)
pv = Image.new("RGBA", bowl_img.size, hexc("#262f60"))
pv.alpha_composite(bowl_img)
m = rotor_img.rotate(20, resample=Image.BICUBIC)
m = m.resize((m.width, int(m.height * K)), Image.LANCZOS)
c = (CX / SS, CY / SS)
pv.alpha_composite(m, (int(c[0] - m.width / 2), int(c[1] - m.height / 2)))
pv.alpha_composite(tur_img, (int(c[0] - TUR_BASE[0]), int(c[1] - TUR_BASE[1])))


def put_ball(r, a, z=0.0):
    x, y = r * math.cos(a), r * math.sin(a)
    px, py = c[0] + R * x, c[1] - R * (K * y + KZ * (height(r) + z + BALL_R))   # bi nằm TRÊN mặt: tâm cao hơn mặt một bán kính
    pv.alpha_composite(ball_img, (int(px - ball_img.width / 2), int(py - ball_img.height / 2)))


put_ball(0.868, math.radians(70))
put_ball(0.868, math.radians(250))
put_ball(0.868, math.radians(300))
pv.alpha_composite(front_img)
put_ball(R_POCKET, math.radians(20) + 3.5 * step)
put_ball(R_POCKET, math.radians(20) + 17.5 * step)
pv.convert("RGB").save(os.path.join(HERE, "xem_banh_xe.png"))
print(info)
