# Khung bố cục thân máy casino (người dùng 2026-11-20: chọn casino_B.png "nhưng thêm 1 chút nhẹ kiểu tô chì").
# Như cabinet_ref của make_parts_refs.py (cùng cửa sổ đúng của bàn, cùng toạ độ px khối máy) nhưng vùng vẽ rộng hơn để có hai cột
# vàng đỏ hai bên vòm và bệ đỏ sau hàng nút như casino_B: vùng khối máy x [30, 1050], y [110, 1640] -> ảnh 1024 x 1536 (2:3).
# Ra refs/khung_than_may_casino.png, refs/cua_so_casino.png, refs/bo_cuc_casino.json (vùng vẽ, mốc cột, gờ đế, bệ).
# Chạy: py -3 -I ArtGen/Pachinko/v2/make_casino_refs.py
import importlib.util
import json
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mpr", os.path.join(HERE, "make_parts_refs.py"))
mpr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mpr)

OUT = mpr.OUT
INK = mpr.INK
BOARD, CAB = mpr.BOARD, mpr.CAB
CAN_W, CAN_H = 1024, 1536
REG = [30.0, 110.0, 1050.0, 1640.0]
SC = CAN_W / (REG[2] - REG[0])
RED = (200, 36, 52)
GOLD = (246, 190, 60)
CREAM = (255, 236, 170)
PLINTH = (150, 26, 44)


def C(x, y):
    return (x - REG[0]) * SC, (y - REG[1]) * SC


def main():
    win_face = np.array(Image.open(os.path.join(OUT, "cua_so_mat_ban.png"))) > 0
    im = Image.new("RGB", (CAN_W, CAN_H), (235, 232, 226))
    bx0, by0 = C(BOARD[0], BOARD[1])
    bx1, by1 = C(BOARD[2], BOARD[3])
    _, rail0 = C(0, CAB["rail"][0])
    _, rail1 = C(0, CAB["rail"][1])
    _, flags = C(0, CAB["flags"])
    wm = cv2.resize(win_face.astype(np.uint8), (int(round(bx1 - bx0)), int(round(by1 - by0))), interpolation=cv2.INTER_NEAREST)
    exact = np.zeros((CAN_H, CAN_W), np.uint8)
    ox, oy = int(round(bx0)), int(round(by0))
    exact[oy:oy + wm.shape[0], ox:ox + wm.shape[1]] = wm
    exact[int(by1) - 40:int(rail0) + 8, ox:ox + wm.shape[1]] = 1
    disk = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    x0c, _ = C(CAB["x0"], 0)
    frame_w = int(round(bx0 - x0c))
    outer = cv2.dilate(exact, disk(frame_w))
    outer[int(rail0) + 8:, :] = 0
    trim_o = cv2.dilate(exact, disk(frame_w + 6))
    trim_o[int(rail0) + 8:, :] = 0
    trim_i = cv2.dilate(exact, disk(14))
    shrunk = cv2.erode(exact, disk(10))
    arr = np.array(im)
    # vòm: viền vàng ngoài, dải đỏ, viền vàng trong (mép cửa sổ), cửa sổ trắng
    arr[trim_o > 0] = GOLD
    arr[outer > 0] = RED
    arr[(trim_i > 0) & (outer > 0)] = GOLD
    arr[shrunk > 0] = (255, 255, 255)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    for msk in (trim_o, shrunk):
        cnts, _ = cv2.findContours(msk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            d.line([tuple(p[0]) for p in c] + [tuple(c[0][0])], fill=INK, width=4)

    def bulb(x, y, r=10):
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM, outline=INK, width=3)
    # đèn trên đường giữa dải đỏ của vòm (tới chân cột)
    mid = cv2.dilate(exact, disk((frame_w + 14) // 2))
    mid[int(rail0) - 6:, :] = 0
    cnts, _ = cv2.findContours(mid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnts, key=len)[:, 0, :].astype(float)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(c, axis=0).T))]
    bulbs = []
    for t in np.arange(0, seg[-1], 34.0):
        i = int(np.searchsorted(seg, t))
        x, y = c[min(i, len(c) - 1)]
        if y < rail0 - 24:
            bulbs.append((x, y))
    for x, y in bulbs:
        bulb(x, y)
    # hai cột: ngoài dải vòm, từ chân vòm (chỗ mép cửa sổ thẳng đứng) xuống gờ đế; mũ cột vàng có quả cầu, thân đỏ có sao vàng,
    # chân cột vàng
    left_edge = np.array([np.argmax(outer[y] > 0) if outer[y].any() else CAN_W for y in range(CAN_H)])
    straight = int(np.argmax(left_edge <= left_edge[int(rail0) - 20] + 2))
    pw = 86
    cols = []
    for side in (0, 1):
        le = int(np.argmax(trim_o[int(rail0) - 20] > 0))
        xa = max(6, le - pw + 6) if side == 0 else CAN_W - max(6, le - pw + 6) - pw
        xb = xa + pw
        top = straight + 40
        cols.append([xa, top, xb, rail0])
        d.rectangle([xa, top + 70, xb, rail0 - 50], fill=RED, outline=INK, width=4)
        for sy in np.linspace(top + 120, rail0 - 100, 6):
            cx = (xa + xb) / 2
            pts = []
            for k in range(10):
                r = 26 if k % 2 == 0 else 11
                a = np.radians(-90 + 36 * k)
                pts.append((cx + r * np.cos(a), sy + r * np.sin(a)))
            d.polygon(pts, fill=GOLD, outline=INK)
        d.rounded_rectangle([xa - 12, top + 20, xb + 12, top + 76], 10, fill=GOLD, outline=INK, width=4)
        d.ellipse([(xa + xb) / 2 - 26, top - 32, (xa + xb) / 2 + 26, top + 22], fill=GOLD, outline=INK, width=4)
        d.rounded_rectangle([xa - 12, rail0 - 56, xb + 12, rail0 + 2], 8, fill=GOLD, outline=INK, width=4)
    # hoa văn vàng hai bên đỉnh vòm (nằm sau bảng số, chỉ ló mép)
    apex_y = float(np.where(trim_o.any(1))[0][0])
    sx = CAN_W / 2
    d.arc([sx - 230, apex_y + 10, sx - 40, apex_y + 90], 200, 340, fill=GOLD, width=18)
    d.arc([sx + 40, apex_y + 10, sx + 230, apex_y + 90], 200, 340, fill=GOLD, width=18)
    # gờ đế đỏ viền vàng có đèn, cờ đuôi nheo vàng đỏ, bệ đỏ sẫm viền vàng (sau hàng nút)
    lx, rx = max(4, cols[0][0] - 8), min(CAN_W - 4, cols[1][2] + 8)
    _, base_bot = C(0, 1640)
    d.rounded_rectangle([lx + 20, flags - 20, rx - 20, base_bot - 4], 24, fill=PLINTH, outline=INK, width=5)
    d.rounded_rectangle([lx + 20, flags - 20, rx - 20, flags + 6], 10, fill=GOLD, outline=INK, width=4)
    d.rounded_rectangle([lx, rail0 - 6, rx, rail1 + 6], 16, fill=GOLD, outline=INK, width=5)
    d.rounded_rectangle([lx + 12, rail0 + 4, rx - 12, rail1 - 4], 10, fill=RED, outline=INK, width=3)
    for x in np.linspace(lx + 40, rx - 40, 17):
        bulb(x, (rail0 + rail1) / 2, 10)
    n = 16
    w = (rx - lx - 20) / n
    for i in range(n):
        fx = lx + 10 + i * w
        col = GOLD if i % 2 == 0 else RED
        d.polygon([(fx + 3, rail1 + 4), (fx + w - 3, rail1 + 4), (fx + w / 2, flags + 30)], fill=col, outline=INK)
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2), "EMPTY WINDOW\n(plain white,\nno content)", fill=(150, 150, 150), font=mpr.font(30), anchor="mm", align="center")
    _, py = C(0, 1500)
    d.text((CAN_W / 2, py), "plain plinth panel (buttons go here later)", fill=(230, 180, 180), font=mpr.font(24), anchor="mm")
    im.save(os.path.join(OUT, "khung_than_may_casino.png"))
    Image.fromarray(exact * 255).save(os.path.join(OUT, "cua_so_casino.png"))
    to_m = lambda v: [round(v[0] / SC + REG[0], 1), round(v[1] / SC + REG[1], 1), round(v[2] / SC + REG[0], 1), round(v[3] / SC + REG[1], 1)]
    info = {"region": REG, "size": [CAN_W, CAN_H], "columns": [to_m(c) for c in cols], "rail": CAB["rail"], "bulbs_hint": len(bulbs) + 17}
    with open(os.path.join(OUT, "bo_cuc_casino.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    print("ok", info)


if __name__ == "__main__":
    main()
