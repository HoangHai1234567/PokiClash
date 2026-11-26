# Đưa hình lều Hội Máy Quả vào Unity (Assets/03 Art/Casino/Leu/sl_*, rig Assets/03 Art/Casino/MayQua/may_qua.bytes).
# - sl_nen.jpg: nền lều 1144 x 2048 (nen_leu_qua_2k.jpg; ArtPostprocessor nhập 2048 theo tên "/Casino/Leu/sl_nen").
# - sl_bt_0..8.png: 9 biểu tượng cuộn cắt từ bieu_tuong_1k.png (nền hồng), theo mã biểu tượng của Core/Casino/Slots.cs:
#   0..4 ngọc hệ (Elements.All = Kim, Mộc, Thủy, Hỏa, Thổ), 5 bi, 6 huy hiệu khách mời, 7 Sao, 8 Rương. 200 x 200 px (hiện ~90).
# - sl_bt_0..8_nhoe.png: cùng biểu tượng kéo nhoè dọc, 200 x 380 (cuộn chạy nhanh thì SlotReels đổi sang hình này).
# - may_qua.bytes: bản sao ../atom/export/may_qua.atomik (đuôi .bytes để AtomikImporter của tướng không nhận; nạp bằng AtomikFile.Load).
# - sl_leu.json: số đo cho menu dựng scene (px ảnh nền 2k).
# Chạy: py -3 -I dua_vao_unity.py
import json, os, shutil, sys
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LEU = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "Leu")
MQ = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "MayQua")
os.makedirs(LEU, exist_ok=True)
os.makedirs(MQ, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, "..", "rig"))

nen = Image.open(os.path.join(HERE, "nen_leu_qua_2k.jpg")).convert("RGB")
nen.save(os.path.join(LEU, "sl_nen.jpg"), quality=92)

a = np.asarray(Image.open(os.path.join(HERE, "bieu_tuong_1k.png")).convert("RGB")).astype(np.float32)
bg = np.median(a[:24, :24].reshape(-1, 3), axis=0)
d = np.sqrt(((a - bg) ** 2).sum(2))
al = np.clip((d - 70) / 50, 0, 1)
m = (al > 0.5).astype(np.uint8)
pad = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
cv2.floodFill(pad, None, (0, 0), 2)
al = np.maximum(al, (pad[1:-1, 1:-1] != 2).astype(np.float32))          # lòng kín (bi trắng, mảng kem) là đặc
n, lab, st, ce = cv2.connectedComponentsWithStats((al > 0.5).astype(np.uint8), 8)
items = sorted([i for i in range(1, n) if st[i, 4] > 4000], key=lambda i: (int(ce[i][1] // 341), ce[i][0]))
assert len(items) == 9, len(items)
solid = cv2.erode((al > 0.97).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
rgb = a.copy()
mm = solid.astype(np.float32)
for _ in range(6):                                                         # loang màu ra mép (hết ánh hồng)
    k = np.ones((3, 3), np.float32)
    num = cv2.filter2D(rgb * mm[..., None], -1, k)
    den = cv2.filter2D(mm, -1, k)
    new = (den > 0) & (mm == 0)
    rgb[new] = num[new] / den[new][:, None]
    mm[new] = 1
ORDER = [3, 2, 1, 0, 4, 5, 6, 7, 8]   # tờ vẽ: lửa, nước, lá, thỏi, đá, bi, vương miện, sao, rương; Elements.All = Kim, Mộc, Thủy, Hỏa, Thổ
for sym in range(9):
    i = items[ORDER[sym]]
    x, y, w, h = st[i, :4]
    x0, y0, x1, y1 = max(0, x - 3), max(0, y - 3), x + w + 3, y + h + 3
    part = np.dstack([rgb[y0:y1, x0:x1], (al * (lab == i))[y0:y1, x0:x1] * 255]).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(part)
    side = max(im.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))                      # ô vuông, biểu tượng ở giữa: mọi biểu tượng cùng tỉ lệ
    sq.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
    sq = sq.resize((200, 200), Image.LANCZOS)
    sq.save(os.path.join(LEU, f"sl_bt_{sym}.png"))
    # hình NHOÈ DỌC lúc cuộn chạy nhanh (SlotReels.BlurTall = 380 / 200): kéo vệt dọc 150 px trên khung 200 x 380, nhân alpha trước
    # khi làm nhoè (mép không lẫn màu nền), đậm lại một chút cho vệt còn rõ màu biểu tượng
    big = np.zeros((380, 200, 4), np.float32)
    big[90:290] = np.asarray(sq).astype(np.float32)
    pm = big.copy()
    pm[..., :3] *= pm[..., 3:4] / 255.0
    pm = cv2.blur(pm, (1, 150))
    pm = cv2.blur(pm, (1, 41))
    al_b = np.clip(pm[..., 3] * 1.9, 0, 255)
    col = np.where(pm[..., 3:4] > 0.5, pm[..., :3] / np.maximum(pm[..., 3:4], 0.5) * 255.0, 0)
    out = np.dstack([col.clip(0, 255), al_b]).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(LEU, f"sl_bt_{sym}_nhoe.png"))

shutil.copyfile(os.path.join(HERE, "..", "atom", "export", "may_qua.atomik"), os.path.join(MQ, "may_qua.bytes"))
geo = json.load(open(os.path.join(HERE, "..", "atom", "geo.json"), encoding="utf-8"))
json.dump({"nen": list(nen.size), "rig_origin": geo["origin"], "reel": geo["reel"]}, open(os.path.join(LEU, "sl_leu.json"), "w"), indent=1)
print("xong:", LEU, MQ)
