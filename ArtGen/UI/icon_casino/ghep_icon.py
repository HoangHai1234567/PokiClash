# Icon "casino" cho nút giữa hàng nút đáy (người dùng 2026-11-27: "icon này nên đổi sang icon kiểu khác để hiểu đây là đảo casino chứ
# không chỉ pachinko"). Ghép từ chính bộ icon chung (cùng nét): bánh xe wheel.png tô lại ô xen kẽ đỏ / đen như bàn roulette (luật "đỏ đen"
# của bàn Vòng Xoay), bài cards.png trái dưới, xúc xắc dice.png phải dưới. Ra Assets/03 Art/Fallback/Icons/casino.png (256 px).
#   py -3 -I ghep_icon.py   rồi menu "PokiClash/Dựng lại danh mục ảnh"
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Fallback", "Icons"))
S = 256

w = np.asarray(Image.open(os.path.join(ICONS, "wheel.png")).convert("RGBA")).astype(np.float32)
h, wd, _ = w.shape
yy, xx = np.mgrid[0:h, 0:wd]
cx, cy = (wd - 1) / 2, (h - 1) / 2
rgb, a = w[..., :3], w[..., 3]
light = (rgb[..., 0] > 200) & (rgb[..., 1] > 160) & (rgb[..., 2] < 190) & (a > 10)  # ô vàng nhạt giữa các nan
sec = np.floor(((np.degrees(np.arctan2(yy - cy, xx - cx)) + 360) % 360) / 45).astype(int)  # 8 ô, nan ở bội 45°
mix = np.where((sec % 2 == 0)[..., None], np.array([226, 72, 58]), np.array([84, 66, 86]))  # đỏ / đen tím (sáng hơn nét viền)
new = rgb.copy()
new[light] = mix[light]
wheel = Image.fromarray(np.dstack([new, a]).astype(np.uint8), "RGBA")


def put(base, im, scale, px, py, rot=0):
    ww = int(S * scale)
    t = im.resize((ww, ww), Image.LANCZOS)
    if rot:
        t = t.rotate(rot, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(t, (int(px - t.width / 2), int(py - t.height / 2)))


o = Image.new("RGBA", (S, S), (0, 0, 0, 0))
put(o, wheel, 0.80, 128, 104)
put(o, Image.open(os.path.join(ICONS, "cards.png")).convert("RGBA"), 0.50, 72, 186, 8)
put(o, Image.open(os.path.join(ICONS, "dice.png")).convert("RGBA"), 0.50, 188, 190, -12)
o.save(os.path.join(ICONS, "casino.png"))
print("ghi", os.path.join(ICONS, "casino.png"))
