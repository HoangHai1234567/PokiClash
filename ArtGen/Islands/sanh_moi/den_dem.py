# Đèn đêm các đảo trên bản đồ sảnh (người dùng 2026-11-20: "buổi đêm các đảo sáng lên và người chơi cần phải biết là click được vào đảo,
# ban ngày thì không cần sáng, chiều tối thì cần; không dùng mũi tên"; chọn cách 3 + 4: mặt nạ phát sáng + đuốc thắp).
# Đọc ảnh đảo đã tách (Assets/03 Art/Islands/sanh_dao_<hệ>.png, build_sanh.py), ghi:
#   sanh_phat_<hệ>.png : chỗ vốn là nguồn sáng của đảo (dung nham, mặt trời vàng, chuông, xoáy nước, đèn hải đăng...) giữ màu gốc, alpha
#                        theo mặt nạ; game vẽ trên lớp nhuộm đêm (shader PokiClash/UIIslandEmit) nên chỗ này không bị nhuộm tối, chập chờn
#   hub_night.json     : khung ảnh phát sáng và chỗ đặt đuốc (tỉ lệ ảnh đảo, y từ trên), menu "PokiClash/Prefab/Sảnh: đèn đêm các đảo"
# Chạy: py -3 -I ArtGen/Islands/sanh_moi/den_dem.py   (thêm --xem: ghi ảnh soi mặt nạ vào thư mục này, không ghi Assets)
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Islands")

# vùng phát sáng: (khung x0, y0, x1, y1 theo tỉ lệ ảnh đảo, bộ lọc màu); chỉ điểm ảnh lọt cả khung lẫn màu mới sáng
EMIT = {
    "hoa": [((0.10, 0.12, 0.84, 1.00), "lava")],                      # dung nham, miệng núi lửa, hai đám lửa trên sườn
    "kim": [((0.52, 0.17, 0.71, 0.41), "gold"),                      # ông mặt trời trên tháp chuông
            ((0.57, 0.44, 0.67, 0.59), "gold")],                     # chuông vàng
    "tho": [((0.40, 0.05, 0.74, 0.27), "gold")],                     # mặt trời, mái vàng của đền
    "moc": [((0.20, 0.36, 0.72, 0.62), "glowwood")],                 # vân xoáy, sáng trên thân cây thần
    # xoáy nước không lấy: phần động "swirl" (IslandAnim) quay trên đó, ảnh tĩnh phủ lên thành chồng hình
    "thuy": [((0.40, 0.17, 0.62, 0.47), "stone"),                    # cổng rồng, cột đá trắng
             ((0.245, 0.425, 0.29, 0.50), "lamp"),                   # buồng đèn hải đăng
             ((0.895, 0.705, 0.935, 0.76), "lamp")],                 # đèn cột đầu cầu tàu
}

# đuốc: (x, y chân đuốc theo tỉ lệ ảnh đảo, kiểu): torch = cột + chậu + lửa; lamp = chỉ ánh lửa trong đèn có sẵn trong tranh
TORCHES = {
    "hoa": [(0.540, 0.690, "torch"), (0.645, 0.690, "torch"), (0.874, 0.140, "lamp")],
    "kim": [(0.530, 0.680, "torch"), (0.710, 0.680, "torch")],
    "tho": [(0.500, 0.370, "torch"), (0.645, 0.370, "torch")],
    "moc": [(0.385, 0.610, "torch"), (0.500, 0.610, "torch")],
    "thuy": [(0.430, 0.490, "torch"), (0.585, 0.490, "torch"), (0.265, 0.462, "lamp"), (0.915, 0.728, "lamp")],
}


def color_mask(rgb, kind):
    r, g, b = (rgb[..., i].astype(np.int16) for i in range(3))
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    # đỏ phải trội hơn lục: không lấy cỏ, lá vàng xanh
    if kind == "lava":  # cam, vàng rực: đỏ cao, lam thấp
        return (r > 205) & (g > 70) & (b < 120) & (r - b > 130) & (sat > 0.55) & (r >= g - 2)
    if kind == "gold":  # vàng kim (không lấy cát vàng nhạt: lam thấp, bão hoà cao)
        return (r > 200) & (g > 140) & (b < 95) & (sat > 0.6) & (r >= g - 2)
    if kind == "glowwood":  # vệt sáng cam nhạt trên thân cây (không lấy nâu sẫm, lá xanh)
        return (r > 215) & (g > 140) & (g < 215) & (b < 140) & (r - g > 25) & (r - b > 90)
    if kind == "stone":  # đá trắng (cổng rồng): sáng, gần như không màu
        return (r > 200) & (g > 200) & (b > 190) & (sat < 0.14)
    if kind == "lamp":  # chỗ sáng (trắng, vàng) trong đèn
        return (r > 215) & (g > 190) & (r >= g - 4)
    raise ValueError(kind)


def build(zone, preview):
    src = Image.open(os.path.join(ART, f"sanh_dao_{zone}.png")).convert("RGBA")
    a = np.asarray(src)
    H, W = a.shape[:2]
    rgb, alpha = a[..., :3], a[..., 3]
    mask = np.zeros((H, W), bool)
    for (x0, y0, x1, y1), kind in EMIT[zone]:
        box = np.zeros((H, W), bool)
        box[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True
        mask |= box & color_mask(rgb, kind) & (alpha > 200)
    # bỏ hạt lẻ (co rồi nở 1 px), mép mềm 1 px; chỉ dùng PIL, numpy (máy không có scipy)
    m = Image.fromarray((mask * 255).astype(np.uint8), "L").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    mask = np.asarray(m) > 127
    soft = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255.0
    soft = np.clip(soft * 1.4, 0, 1) * (alpha / 255.0)
    ys, xs = np.nonzero(soft > 0.02)
    if len(xs) == 0:
        return None
    pad = 4
    x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + 1 + pad)
    y0, y1 = max(0, ys.min() - pad), min(H, ys.max() + 1 + pad)
    out = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    out[..., :3] = rgb[y0:y1, x0:x1]
    out[..., 3] = (soft[y0:y1, x0:x1] * 255).astype(np.uint8)
    out[out[..., 3] == 0, :3] = 0  # chỗ trong suốt để đen cho file nhẹ
    img = Image.fromarray(out, "RGBA")
    if preview:
        # soi: đảo tối như đêm, chỗ phát sáng giữ màu
        night = (rgb * np.array([0.66, 0.72, 0.93])).astype(np.uint8)
        k = soft[..., None]
        view = (night * (1 - k) + rgb * k).astype(np.uint8)
        v = Image.fromarray(np.dstack([view, alpha]), "RGBA")
        bg = Image.new("RGBA", v.size, (40, 60, 120, 255))
        bg.alpha_composite(v)
        s = 900 / max(bg.size)
        bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS).convert("RGB").save(os.path.join(HERE, f"_soi_phat_{zone}.jpg"), quality=85)
    else:
        img.save(os.path.join(ART, f"sanh_phat_{zone}.png"), optimize=True)
    return {"zone": zone, "emit": f"sanh_phat_{zone}",
            "emitRect": [round(float(x0) / W, 5), round(float(y0) / H, 5), round(float(x1) / W, 5), round(float(y1) / H, 5)],
            "torches": [{"x": x, "y": y, "k": k} for x, y, k in TORCHES[zone]], "px": int(mask.sum())}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    preview = "--xem" in sys.argv
    items = []
    for z in ["thuy", "hoa", "kim", "moc", "tho"]:
        it = build(z, preview)
        if it:
            print(z, it["emitRect"], "điểm sáng", it.pop("px"))
            items.append(it)
    if not preview:
        with open(os.path.join(ART, "hub_night.json"), "w", encoding="utf-8") as f:
            json.dump({"islands": items}, f, ensure_ascii=False, indent=1)
        print("đã ghi", os.path.join(ART, "hub_night.json"))


if __name__ == "__main__":
    main()
