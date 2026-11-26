# Xem trước viên bi lăn trên ĐÚNG hình bánh xe của game (ra/rl_*.png), ngoài Unity: đọc out/track.json ("chay.py dump <ô> <hạt giống>"),
# ghép lòng chảo + mâm xoay ép dẹt + trục + bi + nửa vành gần đúng như RouletteScene.PlaceWheel. Ra ../xem_bi_lan.webp (30 khung/giây)
# và ../xem_bi_lan_to.jpg (tờ khung). py -3 -I xem_bi_that.py
import json, math, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
D4 = os.path.dirname(HERE)
RA = os.path.join(D4, "ra")
T = json.load(open(os.path.join(HERE, "out", "track.json")))
info = json.load(open(os.path.join(RA, "banh_xe.json")))
pts, dt = T["pts"], T["dt"]
S = 0.5                                   # cỡ hiện trên sân khấu = nửa cỡ ảnh
R, K, KZ, BALL_R = info["R"] * S, info["K"], info["KZ"], 0.040


def load(n):
    im = Image.open(os.path.join(RA, n)).convert("RGBA")
    return im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)


bowl, front, rotor, tur, ball = load("rl_chao.png"), load("rl_vanh_truoc.png"), load("rl_mam.png"), load("rl_truc.png"), load("rl_bi.png")
cx, cy = info["chao"]["center"][0] * S, info["chao"]["center"][1] * S
tb = (info["truc"]["base"][0] * S, info["truc"]["base"][1] * S)


def height(r):
    def lerp(a, b, t):
        return a + (b - a) * max(0.0, min(1.0, t))
    if r >= 0.905: return 0.085
    if r >= 0.80: return lerp(0.035, 0.07, (r - 0.80) / 0.105)
    if r >= 0.70: return lerp(0.0, 0.035, (r - 0.70) / 0.10)
    return 0.0


def frame(i):
    x, y, z, rot = pts[i]
    im = Image.new("RGBA", bowl.size, (38, 47, 96, 255))
    im.alpha_composite(bowl)
    m = rotor.rotate(math.degrees(rot), resample=Image.BICUBIC)
    m = m.resize((m.width, round(m.height * K)), Image.BILINEAR)
    im.alpha_composite(m, (round(cx - m.width / 2), round(cy - m.height / 2)))
    im.alpha_composite(tur, (round(cx - tb[0]), round(cy - tb[1])))
    r = math.hypot(x, y)
    bx, by = cx + R * x, cy - R * (K * y + KZ * (height(r) + z + BALL_R))
    im.alpha_composite(ball, (round(bx - ball.width / 2), round(by - ball.height / 2)))
    im.alpha_composite(front)
    return im.convert("RGB")


idx = list(range(0, len(pts), 4))
frames = [frame(i) for i in idx]
frames[0].save(os.path.join(D4, "xem_bi_lan.webp"), save_all=True, append_images=frames[1:], duration=33, loop=0, quality=70, method=4)
pick = frames[::6]                         # mỗi 0,2 giây
cols = 8
rows = (len(pick) + cols - 1) // cols
w, h = bowl.width // 2, bowl.height // 2
sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 30))
for n, f in enumerate(pick):
    sheet.paste(f.resize((w, h), Image.LANCZOS), ((n % cols) * w, (n // cols) * h))
sheet.save(os.path.join(D4, "xem_bi_lan_to.jpg"), quality=82)
print(len(frames), "khung;", sheet.size, "ô", T["pocket"], "vị trí", T["slot"], "dài", T["duration"])
