# Biển đảo Casino nối liền biển sảnh / chuyến tàu (bản 2: lớp đất trong suốt chỗ nước + lớp biển riêng trong game) (người dùng 2026-11-25: "phần biển của 2 đảo phải nối nhau, tôi thấy có sự khác nhau
# về màu sắc"): thay phần nước của ảnh đảo trống bằng tấm vân biển dùng chung của chuyến tàu qua mây (Assets/03 Art/Ship/tau_bien.png,
# lát 512 px như ShipVoyage), giữ nét sóng trắng, bọt viền bờ, nét mực, đất đá. Ảnh nối dài thêm `add` px biển ở đáy (toàn tấm vân biển,
# không lật gương). Khung công trình giữ nguyên (gốc trên trái); casino_art.json đổi h. Thay cho noi_bien.py.
# py -3 -I doi_bien.py
import os, sys, json
from PIL import Image, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = r"C:\Atomik\PokiWar"
ART = os.path.join(PROJ, "Assets", "03 Art", "Casino")
TILE = os.path.join(PROJ, "Assets", "03 Art", "Ship", "tau_bien.png")
add = int(sys.argv[1]) if len(sys.argv) > 1 else 400

base = Image.open(os.path.join(HERE, "dao_trong_2k.png")).convert("RGB")
W, H = base.size
tile = Image.open(TILE).convert("RGB")
tw, th = tile.size
sea = Image.new("RGB", (W, H + add))
for y in range(0, H + add, th):
    for x in range(0, W, tw):
        sea.paste(tile, (x, y))

# mặt nạ nước: xanh lơ (lam trội đỏ, lục cao); nét sóng trắng, bọt (đỏ cao) và nét mực không phải nước
px = base.load()
mask = Image.new("L", (W, H), 0)
mp = mask.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if b > 150 and g > 140 and b - r > 45:
            # mép mềm theo độ "xanh": nét sáp sáng (đỏ cao hơn) vẫn là nước nhưng giảm dần
            k = min(1.0, (b - r - 45) / 40.0)
            mp[x, y] = int(255 * k)
mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
# lớp đất: nước trong suốt (biển là lớp riêng trong game: tấm vân biển lát lặp, DayNight làm tối về đêm như biển sảnh)
land = base.convert("RGBA")
land.putalpha(Image.eval(mask, lambda v: 255 - v))
land.save(os.path.join(ART, "casino_dao.png"))
meta = json.load(open(os.path.join(ART, "casino_art.json"), encoding="utf-8"))
meta["h"] = H
meta["h_dao"] = H
json.dump(meta, open(os.path.join(ART, "casino_art.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ảnh xem: đất trên biển lát
prev = Image.new("RGB", (W, H))
prev.paste(sea.crop((0, 0, W, H)), (0, 0))
prev.paste(land, (0, 0), land)
prev.save(os.path.join(HERE, "doi_bien_ghep.png"))
print("casino_dao.png (lop dat, nuoc trong suot)", land.size)
