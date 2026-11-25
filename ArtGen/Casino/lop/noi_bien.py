# Nối dài biển dưới đáy ảnh đảo trống để màn đảo không lộ ranh ảnh với nền biển phẳng: lát lặp (lật gương) một mảng thuần biển ở góc
# dưới trái ảnh, trộn mềm 70 px giáp đáy ảnh gốc. Khung công trình giữ nguyên (gốc trên trái); casino_art.json đổi h.
# py -3 -I noi_bien.py [px thêm, mặc định 400]
import os, sys, json
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(r"C:\Atomik\PokiWar", "Assets", "03 Art", "Casino")
add = int(sys.argv[1]) if len(sys.argv) > 1 else 400
PATCH = (1712, 1172, 2044, 1356)  # mảng thuần biển (góc dưới phải bản 2k, dò bằng tỉ lệ điểm màu nước)
base = Image.open(os.path.join(HERE, "dao_trong_2k.png")).convert("RGB")
W, H = base.size
patch = base.crop(PATCH)
pw, ph = patch.size
strip = Image.new("RGB", (W, add))
for j in range(0, add, ph):
    for i in range(0, W, pw):
        p = patch
        if (i // pw) % 2: p = ImageOps.mirror(p)
        if (j // ph) % 2 == 0: p = ImageOps.flip(p)
        strip.paste(p, (i, j))
# trộn mềm: đầu dải lấy dần từ ảnh gốc lật gương (liền với hàng đáy)
blend = 70
top = ImageOps.flip(base.crop((0, H - blend, W, H)))
mask = Image.linear_gradient("L").resize((W, blend))  # 0 trên → 255 dưới
strip.paste(Image.composite(strip.crop((0, 0, W, blend)), top, mask), (0, 0))
out = Image.new("RGB", (W, H + add))
out.paste(base, (0, 0))
out.paste(strip, (0, H))
out.save(os.path.join(ART, "casino_dao.png"))
meta = json.load(open(os.path.join(ART, "casino_art.json"), encoding="utf-8"))
meta["h"] = H + add
meta["h_dao"] = H
json.dump(meta, open(os.path.join(ART, "casino_art.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("casino_dao.png", out.size)
