# Đưa ảnh màn Hang Tiềm Năng (bản sân khấu 2026-11-27) vào Unity: Assets/03 Art/Cave/.
# - hang_nen.jpg: nền hang (nen_hang_2k.jpg = Magnific GPT 2.6 1k high 9:16, phóng classic 2k preset Art subtle), 1144 x 2048,
#   ArtImporter nhập 2048 (luật "/Cave/hang_nen");
# - hang_da_tiem_nang.png, hang_da_tinh.png, hang_da_tien_hoa.png: ba icon thưởng cắt từ icon_thuong_1k.png (nền xanh phẳng #00B140),
#   mỗi cái vuông 192 px, có viền sticker trắng;
# - hang.json: số đo trên ảnh 2k (px, gốc trên trái) cho menu dựng màn (Editor/CaveStageMenu.cs chép số vào hằng).
# Gen lại nền thì phải đo lại bảng đá, bệ đá, lòng vòm (bảng M) rồi sửa hằng trong CaveStageMenu.
# Chạy: py -3 -I dua_vao_unity.py
import json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(PROJECT, "Assets", "03 Art", "Cave")
os.makedirs(OUT, exist_ok=True)

M = {
    "size": [1144, 2048],
    "tablet": [265, 388, 868, 550],    # bảng đá trống trên vòm (x0, y0, x1, y1): ghi tên tầng + thưởng lần đầu
    "arch": [350, 610, 760, 1020],     # lòng vòm (cầu thang xuống): boss mới chạy từ đây ra
    "platform": [0, 1020, 1144, 1480], # mặt bệ đá (khung bao elip): tướng đứng
    "steps_bottom": 1660,              # đáy bậc thềm trước bệ
    "bottom_color": "#342a49",         # màu đáy ảnh: tô phần màn dài hơn ảnh
}

src = Image.open(os.path.join(HERE, "nen_hang_2k.jpg")).convert("RGB")
assert list(src.size) == M["size"], src.size
src.save(os.path.join(OUT, "hang_nen.jpg"), quality=92)

# ---------- icon: tách khỏi nền xanh ----------
ic = np.asarray(Image.open(os.path.join(HERE, "icon_thuong_1k.png")).convert("RGB")).astype(np.float32)
r, g, b = ic[..., 0], ic[..., 1], ic[..., 2]
green = g - np.maximum(r, b)              # nền ~ +170, viền trắng ~ 0, hình < 60
alpha = np.clip((120 - green) / 70, 0, 1)  # mềm ở mép
rgb = ic.copy()
semi = alpha < 1
rgb[..., 1] = np.where(semi, np.minimum(g, np.maximum(r, b) + 10), g)  # khử ám xanh ở mép
rgba = np.dstack([rgb, alpha * 255]).clip(0, 255).astype(np.uint8)

# ba cụm theo cột: cột nào có điểm đục
cols = (alpha > 0.5).sum(0) > 0
runs, x = [], 0
W = len(cols)
while x < W:
    if cols[x]:
        x0 = x
        while x < W and cols[x]:
            x += 1
        if x - x0 > 40:
            runs.append((x0, x))
    x += 1
assert len(runs) == 3, runs
names = ["hang_da_tiem_nang", "hang_da_tinh", "hang_da_tien_hoa"]
S = 192
for (x0, x1), name in zip(runs, names):
    rows = np.where((alpha[:, x0:x1] > 0.5).sum(1) > 0)[0]
    y0, y1 = rows.min(), rows.max() + 1
    crop = Image.fromarray(rgba[y0:y1, x0:x1], "RGBA")
    side = max(crop.size) + 8
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(crop, ((side - crop.size[0]) // 2, (side - crop.size[1]) // 2))
    sq.resize((S, S), Image.LANCZOS).save(os.path.join(OUT, name + ".png"))
    print(name, (x0, y0, x1, y1))

json.dump(M, open(os.path.join(OUT, "hang.json"), "w"), indent=1)
print("xong:", OUT, sorted(f for f in os.listdir(OUT) if not f.endswith(".meta")))
