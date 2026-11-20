# Khung bố cục cho các tờ mảnh màn máy bi bản 2 (GD_Claude/23, người dùng chọn concept 2 + cờ của concept 1, 2026-11-20).
# Toạ độ chung là "px khối máy" (khoi_may 1080 x 1530, gốc trên trái, y xuống). Bàn bi thu 0,92 (791,2 x 1169,6 -> 728 x 1076),
# đặt ở BOARD bên dưới; thân máy mới nằm SAU bàn, góc cam của mặt bàn tĩnh (may_tinh.png) làm trong suốt nên viền đỏ có đèn của thân
# máy hiện ra quanh vòm trời. Cửa sổ thân máy vẽ nhỏ hơn vòm trời một chút để mép cửa sổ luôn nằm dưới bàn.
# Ra (refs/): khung_than_may.png (2:3), khung_bang_so.png (3:2), khung_luoi_*.png (lưới ô cho tờ nhiều mảnh), cua_so.png (mặt nạ cửa
# sổ đúng của bàn trên khung thân máy, để cắt), bo_cuc_v2.json (mọi số đo).
# Chạy: py -3 -I ArtGen/Pachinko/v2/make_parts_refs.py
import json
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
FACE = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Machine", "may_tinh.png")
INK = (70, 50, 40)
ORANGE = (252, 116, 84)

# bố cục bản 2 (px khối máy)
BOARD_SCALE = 0.92
BOARD_W, BOARD_H = 791.2 * BOARD_SCALE, 1169.6 * BOARD_SCALE
BOARD = [540 - BOARD_W / 2, 215.0, 540 + BOARD_W / 2, 215.0 + BOARD_H]
CAB = {"x0": 112, "x1": 968, "apex": 150, "rail": [BOARD[3] - 4, BOARD[3] + 52], "flags": BOARD[3] + 104, "feet": BOARD[3] + 136}
SCORE = [220, 8, 860, 202]  # đáy bảng đè nhẹ lên sao huy hiệu vòm (đỉnh sao y 193, vòm đỏ y 200)
XPBAR = [40, -105, 1040, -15]
PUSH = [415, 1362, 665, 1578]
BET = [62, 1412, 292, 1528]
AUTO = [672, 1440, 792, 1560]
TRAY = [800, 1380, 1012, 1552]
COUNTER = [370, 1584, 710, 1644]
GIFT = [740, 1588, 1060, 1644]

# khung thân máy: vùng khối máy x [90, 990], y [110, 1460] -> ảnh 1024 x 1536
CAN_W, CAN_H = 1024, 1536
REG = [90.0, 110.0, 990.0, 1460.0]
SC = CAN_W / (REG[2] - REG[0])


def to_can(x, y):
    return (x - REG[0]) * SC, (y - REG[1]) * SC


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def window_mask():
    """Cửa sổ của bàn trên mặt bàn tĩnh: vòm trời đối xứng + phần dưới đủ bề ngang. Đo mép trái vòm theo từng hàng (bên trái sạch,
    không có làn), làm mượt, cho đơn điệu, lấy đối xứng. Ống làn chéo ở góc trên phải vẫn hiện vì mặt bàn nằm trên thân máy."""
    im = np.array(Image.open(FACE).convert("RGB")).astype(int)
    h, w = im.shape[:2]
    cam = (np.abs(im - np.array(ORANGE)).sum(2) < 60).astype(np.uint8)
    cam = cv2.morphologyEx(cam, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    left = np.zeros(h)
    for y in range(h):
        row = cam[y, : w // 2]
        z = np.where(row == 0)[0]
        left[y] = z[0] if len(z) else w // 2
    # mép trái giảm dần theo y tới khi chạm mép (vòm), sau đó 0
    top = int(np.argmax(left < w // 2 - 2))
    k = 31
    sm = np.convolve(np.pad(left, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k]
    sm = np.minimum.accumulate(sm)
    sm[sm < 6] = 0
    win = np.zeros((h, w), np.uint8)
    for y in range(top, h):
        l = int(round(sm[y]))
        win[y, l:w - l] = 1
    return win


def arch_path(d, x0, x1, apex, y_low, fill, width=4):
    """Vòm: nửa elip từ x0 tới x1, đỉnh apex, chân vòm ở y_low; kéo thẳng xuống."""
    rx = (x1 - x0) / 2
    ry = min(rx * 0.9, y_low - apex)
    cy = apex + ry
    pts = []
    for i in range(0, 181):
        a = np.radians(180 - i)
        pts.append((x0 + rx + rx * np.cos(a), cy - ry * np.sin(a)))
    pts = [(x0, y_low)] + pts + [(x1, y_low)]
    d.polygon(pts, fill=fill, outline=INK, width=width)
    return cy, rx, ry


def cabinet_ref(win_face):
    im = Image.new("RGB", (CAN_W, CAN_H), (235, 232, 226))
    d = ImageDraw.Draw(im)
    x0, y0 = to_can(CAB["x0"], CAB["apex"])
    x1, _ = to_can(CAB["x1"], CAB["apex"])
    _, rail0 = to_can(0, CAB["rail"][0])
    _, rail1 = to_can(0, CAB["rail"][1])
    _, flags = to_can(0, CAB["flags"])
    _, feet = to_can(0, CAB["feet"])
    # cửa sổ đúng của bàn trên khung
    bx0, by0 = to_can(BOARD[0], BOARD[1])
    bx1, by1 = to_can(BOARD[2], BOARD[3])
    wm = cv2.resize(win_face, (int(round(bx1 - bx0)), int(round(by1 - by0))), interpolation=cv2.INTER_NEAREST)
    exact = np.zeros((CAN_H, CAN_W), np.uint8)
    ox, oy = int(round(bx0)), int(round(by0))
    exact[oy:oy + wm.shape[0], ox:ox + wm.shape[1]] = wm
    # đáy cửa sổ kéo xuống tới gờ đế
    exact[int(by1) - 40:int(rail0) + 8, ox:ox + wm.shape[1]] = np.maximum(exact[int(by1) - 40:int(rail0) + 8, ox:ox + wm.shape[1]], 1)
    disk = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    frame_w = int(round((bx0 - x0)))  # dày khung = khoảng bàn tới mép tủ
    outer = cv2.dilate(exact, disk(frame_w))
    outer[int(rail0) + 8:, :] = 0
    shrunk = cv2.erode(exact, disk(10))
    arr = np.array(im)
    arr[outer > 0] = (232, 96, 74)
    arr[shrunk > 0] = (255, 255, 255)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    for msk in (outer, shrunk):
        cnts, _ = cv2.findContours(msk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            d.line([tuple(p[0]) for p in c] + [tuple(c[0][0])], fill=INK, width=5)
    # chân tủ (sau gờ đế)
    for fx in (x0 + 60, x1 - 170):
        d.rounded_rectangle([fx, rail1 - 10, fx + 110, feet], 14, fill=(214, 120, 70), outline=INK, width=4)

    def bulb(x, y, r=11):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 236, 170), outline=INK, width=3)
    # đèn: đường giữa khung, rải đều theo chiều dài (mật độ như máy tham khảo: vòm 87 bóng, cách ~0,3 u)
    mid = cv2.dilate(exact, disk(frame_w // 2))
    mid[int(rail0) - 6:, :] = 0
    cnts, _ = cv2.findContours(mid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnts, key=len)[:, 0, :].astype(float)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(c, axis=0).T))]
    step = 36.0
    bulbs = []
    for t in np.arange(0, seg[-1], step):
        i = int(np.searchsorted(seg, t))
        x, y = c[min(i, len(c) - 1)]
        if y < rail0 - 26:
            bulbs.append((x, y))
    for x, y in bulbs:
        bulb(x, y)
    # huy hiệu đỉnh vòm: sao + hai nét cuộn xanh
    apex_y = float(np.where(outer.any(1))[0][0])
    sx, sy = (x0 + x1) / 2, apex_y + frame_w * 0.5
    star = []
    for k in range(10):
        r = 34 if k % 2 == 0 else 15
        a = np.radians(-90 + 36 * k)
        star.append((sx + r * np.cos(a), sy + r * np.sin(a)))
    d.polygon(star, fill=(255, 210, 70), outline=INK, width=3)
    d.arc([sx - 200, sy - 10, sx - 50, sy + 50], 200, 340, fill=(90, 190, 180), width=12)
    d.arc([sx + 50, sy - 10, sx + 200, sy + 50], 200, 340, fill=(90, 190, 180), width=12)
    # gờ đế có đèn + cờ đuôi nheo (concept 1)
    d.rounded_rectangle([x0 - 16, rail0, x1 + 16, rail1], 16, fill=(214, 78, 60), outline=INK, width=5)
    for x in np.linspace(x0 + 30, x1 - 30, 15):
        bulb(x, (rail0 + rail1) / 2, 10)
    n = 14
    w = (x1 - x0 + 20) / n
    for i in range(n):
        fx = x0 - 10 + i * w
        col = (255, 214, 90) if i % 2 == 0 else (245, 150, 175)
        d.polygon([(fx + 3, rail1 - 2), (fx + w - 3, rail1 - 2), (fx + w / 2, flags)], fill=col, outline=INK)
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2), "EMPTY WINDOW\n(plain white,\nno content)", fill=(150, 150, 150), font=font(30), anchor="mm", align="center")
    im.save(os.path.join(OUT, "khung_than_may.png"))
    Image.fromarray(exact * 255).save(os.path.join(OUT, "cua_so.png"))
    return {"bulbs_hint": len(bulbs) + 15, "frame_w": frame_w, "apex": apex_y}


def score_ref():
    W, H = 1536, 1024
    im = Image.new("RGB", (W, H), (235, 232, 226))
    d = ImageDraw.Draw(im)
    bw = 1400
    bh = bw * (SCORE[3] - SCORE[1]) / (SCORE[2] - SCORE[0])
    x0, y0 = (W - bw) / 2, (H - bh) / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 70, fill=(250, 176, 60), outline=INK, width=6)
    m = 70
    d.rounded_rectangle([x0 + m, y0 + m, x0 + bw - m, y0 + bh - m], 36, fill=(78, 36, 66), outline=INK, width=5)

    def bulb(x, y, r=17):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 236, 170), outline=INK, width=3)
    # bảng số máy tham khảo: 26 bóng (9 trên, 9 dưới, 2 mỗi bên, 4 góc); bảng mình rộng hơn: 13 trên, 13 dưới, 2 mỗi bên
    for x in np.linspace(x0 + 50, x0 + bw - 50, 13):
        bulb(x, y0 + 34)
        bulb(x, y0 + bh - 34)
    for y in np.linspace(y0 + 150, y0 + bh - 150, 2):
        bulb(x0 + 34, y)
        bulb(x0 + bw - 34, y)
    d.text((W / 2, H / 2), "EMPTY DARK DISPLAY (no digits)", fill=(200, 170, 200), font=font(40), anchor="mm")
    im.save(os.path.join(OUT, "khung_bang_so.png"))
    return [x0, y0, x0 + bw, y0 + bh]


def grid_ref(name, W, H, cols, rows, labels, bg=(235, 232, 226), fg=INK):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    cw, ch = W / cols, H / rows
    for i, lab in enumerate(labels):
        c, r = i % cols, i // cols
        d.rectangle([c * cw + 8, r * ch + 8, (c + 1) * cw - 8, (r + 1) * ch - 8], outline=fg, width=2)
        d.text((c * cw + cw / 2, r * ch + ch / 2), lab, fill=fg, font=font(30), anchor="mm", align="center")
    im.save(os.path.join(OUT, name))


def main():
    win = window_mask()
    Image.fromarray(win * 255).save(os.path.join(OUT, "cua_so_mat_ban.png"))
    info = cabinet_ref(win)
    score_box = score_ref()
    grid_ref("khung_luoi_so.png", 1536, 1024, 6, 2, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "x"])
    grid_ref("khung_luoi_nut.png", 1024, 1024, 2, 2, ["A normal\ngold dome", "B pressed\n(same base)", "C empty\ngrey dome", "D big bet\npink dome"])
    grid_ref("khung_luoi_mon.png", 1536, 1024, 3, 2, ["1 bet pill", "2 bet pill\nlocked", "3 chest tray\nframe", "4 ball counter\npill", "5 auto button\noff", "6 auto button\non"])
    grid_ref("khung_luoi_fx.png", 1536, 1024, 4, 3, ["1 bulb\nyellow", "2 bulb\npink", "3 bulb\nwhite", "4 glow\nblob", "5 sparkle\n4-point", "6 star\nglint", "7 light\nrays", "8 coin", "9 confetti", "10 light\nstreak", "11 glow\nring", "12 star\nspark"],
             bg=(0, 0, 0), fg=(90, 90, 90))
    lay = {"board_scale": BOARD_SCALE, "board": BOARD, "cab": CAB, "score": SCORE, "xpbar": XPBAR, "push": PUSH, "bet": BET,
           "auto": AUTO, "tray": TRAY, "counter": COUNTER, "gift": GIFT, "cab_canvas": {"size": [CAN_W, CAN_H], "region": REG},
           "score_canvas_box": score_box}
    with open(os.path.join(OUT, "bo_cuc_v2.json"), "w", encoding="utf-8") as f:
        json.dump(lay, f, ensure_ascii=False, indent=1)
    print("ok", info)


if __name__ == "__main__":
    main()
