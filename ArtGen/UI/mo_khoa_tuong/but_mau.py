# Bút chì màu cho màn mở khoá tướng (người dùng 2026-11-25: "làm nhiều bút chì màu khác nhau tô các phần cùng lúc cho thật hơn"):
# tách bút chì vàng của bản đồ đảo Cỏ (Assets/03 Art/Islands/Co/but_chi.png) thành hai lớp cùng cỡ, chồng khít nhau:
#   but_mau_vo.png   : vỏ: viền mực, gỗ vót, đầu tẩy, khâu kim loại, hai rãnh xám trên thân (thân vàng và ruột chì bỏ trống);
#   but_mau_than.png : thân vàng + ruột chì đổi sang xám (giữ vân chì sáp), game nhân màu vùng tô (Image.color).
# Chạy: py -3 -I but_mau.py [thư mục ra] (mặc định Assets/03 Art/Shop của project chứa script).
import colorsys, os, sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
proj = os.path.join(here, "..", "..", "..")
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(proj, "Assets", "03 Art", "Shop")
src = np.array(Image.open(os.path.join(proj, "Assets", "03 Art", "Islands", "Co", "but_chi.png")).convert("RGBA")).astype(np.float32) / 255

h, w = src.shape[:2]
hsv = np.zeros((h, w, 3), np.float32)
for y in range(h):
    for x in range(w):
        hsv[y, x] = colorsys.rgb_to_hsv(*src[y, x, :3])
hue, sat, val = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
a = src[..., 3]
body = (hue >= 28) & (hue <= 62) & (sat > 0.6) & (val > 0.35) & (a > 0.02)  # thân vàng (cả vân sáp sẫm hơn)
lead = (hue >= 140) & (hue <= 200) & (sat > 0.3) & (val > 0.25) & (a > 0.02)  # ruột chì xanh ngọc
paint = body | lead

shell = src.copy()
shell[paint, 3] = 0
gray = np.zeros_like(src)
g = np.where(body, np.clip(val / 0.92, 0, 1), np.clip(val / 0.6, 0, 1) * 0.82)  # ruột chì sẫm hơn thân một chút
gray[..., 0] = gray[..., 1] = gray[..., 2] = g
gray[..., 3] = np.where(paint, a, 0)

os.makedirs(out, exist_ok=True)
for name, arr in (("but_mau_vo.png", shell), ("but_mau_than.png", gray)):
    Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA").save(os.path.join(out, name))
    print("ghi", os.path.normpath(os.path.join(out, name)))
print("thân", int(body.sum()), "ruột", int(lead.sum()), "điểm ảnh")
