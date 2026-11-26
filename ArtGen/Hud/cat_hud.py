# Cắt tờ icon thanh trên (hud_v1.png, gen Magnific GPT 2.6 nền trong, lưới 2 x 3, 2026-11-27) và dựng hình cho game:
# - bi, đồng hồ, bánh răng: ghi đè Assets/03 Art/Fallback/Icons/{ball,clock,gear}.png (giữ .meta, giữ guid: cả game đổi theo),
#   256 x 256, hình (cả viền sticker) đặt vào đúng khung chữ nhật mà icon cũ chiếm, khỏi lệch bố cục các màn;
# - huy hiệu cấp: khung tròn có sao (ô 6) + ruy băng (ô 5) ghép một hình, tâm vòng tròn nằm đúng giữa ảnh
#   -> Assets/03 Art/Hud/huy_hieu_cap.png;
# - cung EXP: lấy đúng vùng rãnh tím nhạt của khung, tô tím đậm giữ vân chì, bỏ chỗ ruy băng che, ảnh vuông tâm vòng tròn
#   -> Assets/03 Art/Hud/cung_exp_cap.png (Image Filled Radial 360 trong prefab App);
# - số đo (tâm, bán kính, dải chữ ruy băng, theo pixel ảnh) -> hud_geo.json để đặt prefab.
# Chạy: py -3 -I ArtGen/Hud/cat_hud.py
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ICONS = os.path.join(ROOT, "Assets", "03 Art", "Fallback", "Icons")
HUD = os.path.join(ROOT, "Assets", "03 Art", "Hud")
# chạy thử: CAT_HUD_OUT=<thư mục> thì ghi icon và huy hiệu vào đó (icon cũ vẫn đọc ở Assets để lấy khung)
DRY = os.environ.get("CAT_HUD_OUT")
CUT = os.path.join(HERE, "cut")
SHEET = "hud_v1.png"
NAMES = ["ball", "clock", "gear", "medal_a", "ribbon", "medal_b"]
PAD = 6
EXP_RGB = np.array([146, 84, 214], np.float32)  # tím đậm của cung EXP (rãnh khung là tím nhạt)


def cut_sheet():
    im = np.array(Image.open(os.path.join(HERE, SHEET)).convert("RGBA"))
    h, w = im.shape[:2]
    # nền GPT 2.6 rải điểm mờ: kéo giãn độ đục, chỉ giữ vùng liền lớn (hình + viền sticker)
    a = im[:, :, 3].astype(np.float32)
    a = np.clip((a - 70) * 255 / 185, 0, 255).astype(np.uint8)
    solid = (a >= 128).astype(np.uint8)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(solid, connectivity=8)
    cw, ch = w / 3, h / 2
    masks = [np.zeros((h, w), np.uint8) for _ in NAMES]
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < 0.03 * cw * ch:
            continue
        cx, cy = cent[i]
        k = min(1, int(cy / ch)) * 3 + min(2, int(cx / cw))
        masks[k][lab == i] = 1
    out = {}
    for k, name in enumerate(NAMES):
        m = cv2.dilate(masks[k], np.ones((5, 5), np.uint8))
        ys, xs = np.nonzero(masks[k])
        x0, x1 = max(0, xs.min() - PAD), min(w, xs.max() + 1 + PAD)
        y0, y1 = max(0, ys.min() - PAD), min(h, ys.max() + 1 + PAD)
        c = im[y0:y1, x0:x1].copy()
        c[:, :, 3] = (a[y0:y1, x0:x1] * m[y0:y1, x0:x1]).astype(np.uint8)
        c[c[:, :, 3] == 0, :3] = 255  # điểm trong suốt tô trắng: lọc ảnh không ra viền đen
        out[name] = c
        Image.fromarray(c, "RGBA").save(os.path.join(CUT, name + ".png"))
        print(f"{name}: {c.shape[1]}x{c.shape[0]}")
    return out


def bbox(alpha, thr=40):
    ys, xs = np.nonzero(alpha > thr)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def place_icon(name, rgba):
    """Hình mới vào khung chữ nhật icon cũ chiếm (giữ tỉ lệ, canh giữa khung), ảnh 256 x 256."""
    path = os.path.join(ICONS, name + ".png")
    old = np.array(Image.open(path).convert("RGBA"))
    ox0, oy0, ox1, oy1 = bbox(old[:, :, 3])
    nx0, ny0, nx1, ny1 = bbox(rgba[:, :, 3])
    src = Image.fromarray(rgba[ny0:ny1, nx0:nx1], "RGBA")
    # viền sticker trắng làm hình to ra: cho phép tràn khung cũ 6 px mỗi bên nhưng không quá ảnh
    bw, bh = ox1 - ox0 + 12, oy1 - oy0 + 12
    s = min(bw / src.width, bh / src.height, 250 / src.width, 250 / src.height)
    tw, th = max(1, round(src.width * s)), max(1, round(src.height * s))
    src = src.resize((tw, th), Image.LANCZOS)
    cx, cy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
    px = int(round(min(max(cx - tw / 2, 3), 256 - 3 - tw)))
    py = int(round(min(max(cy - th / 2, 3), 256 - 3 - th)))
    canvas = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
    canvas.alpha_composite(src, (px, py))
    arr = np.array(canvas)
    arr[arr[:, :, 3] == 0, :3] = 255
    Image.fromarray(arr, "RGBA").save(os.path.join(DRY, name + ".png") if DRY else path)
    print(f"{name}.png: khung cũ {ox1 - ox0}x{oy1 - oy0}, hình mới {tw}x{th} tại ({px},{py})")


def circle_of(medal):
    """Tâm và bán kính các vòng của khung tròn: đĩa kem giữa, rãnh tím nhạt, mép ngoài."""
    rgb = medal[:, :, :3].astype(np.int32)
    hsv = cv2.cvtColor(medal[:, :, :3], cv2.COLOR_RGB2HSV).astype(np.int32)
    al = medal[:, :, 3] > 128
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lav = al & (hsv[:, :, 0] >= 120) & (hsv[:, :, 0] <= 150) & (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 150)
    cream = al & (r > 225) & (g > 210) & (b > 165) & (r - b > 15) & (r - b < 70)
    # tâm: trọng tâm vùng tím nhạt (vành tròn đều nên trọng tâm là tâm), tinh lại bằng đĩa kem trong vành
    ys, xs = np.nonzero(lav)
    cx, cy = xs.mean(), ys.mean()
    rad = np.hypot(xs - cx, ys - cy)
    r_in, r_out = np.percentile(rad, 1.5), np.percentile(rad, 98.5)
    ys2, xs2 = np.nonzero(cream)
    keep = np.hypot(xs2 - cx, ys2 - cy) < r_in * 0.95
    cx, cy = xs2[keep].mean(), ys2[keep].mean()
    rad = np.hypot(xs - cx, ys - cy)
    r_in, r_out = np.percentile(rad, 1.5), np.percentile(rad, 98.5)
    # mép ngoài (cả viền sticker): bán kính lớn nhất của hình theo phương ngang (tránh sao trên đỉnh)
    row = al[int(round(cy))]
    xs3 = np.nonzero(row)[0]
    r_edge = max(cx - xs3.min(), xs3.max() + 1 - cx)
    disc = np.percentile(np.hypot(xs2[keep] - cx, ys2[keep] - cy), 99)
    return dict(cx=float(cx), cy=float(cy), r_in=float(r_in), r_out=float(r_out), r_edge=float(r_edge), r_disc=float(disc)), lav


def build_badge(medal, ribbon):
    geo, lav = circle_of(medal)
    cx, cy, r_edge = geo["cx"], geo["cy"], geo["r_edge"]
    mh, mw = medal.shape[:2]
    # ruy băng: rộng 1,18 lần đường kính ngoài, dải giữa vắt qua đáy vòng tròn (tâm dải ở 0,80 bán kính dưới tâm)
    rb = Image.fromarray(ribbon, "RGBA")
    rx0, ry0, rx1, ry1 = bbox(ribbon[:, :, 3])
    rb = rb.crop((rx0, ry0, rx1, ry1))
    s = 2 * r_edge * 1.18 / rb.width
    rb = rb.resize((round(rb.width * s), round(rb.height * s)), Image.LANCZOS)
    rbw, rbh = rb.size
    # tâm dải giữa của ruy băng: hàng có nhiều điểm tím nhất ở nửa giữa theo chiều ngang
    ra = np.array(rb)
    rhsv = cv2.cvtColor(ra[:, :, :3], cv2.COLOR_RGB2HSV).astype(np.int32)
    vio = (ra[:, :, 3] > 128) & (rhsv[:, :, 0] >= 125) & (rhsv[:, :, 0] <= 155) & (rhsv[:, :, 1] > 60)
    mid = vio[:, rbw // 4: 3 * rbw // 4]
    rows = np.nonzero(mid.sum(axis=1) > mid.shape[1] * 0.6)[0]
    band_top, band_bot = rows.min(), rows.max() + 1
    band_cy = (band_top + band_bot) / 2
    band_x0 = np.nonzero(vio[int(band_cy)])[0]
    # vị trí ruy băng trên khung (toạ độ ảnh khung)
    rib_x = cx - rbw / 2
    rib_y = cy + r_edge * 0.80 - band_cy
    # ảnh ghép: tâm vòng tròn đúng giữa; đủ chỗ cho sao (trên) và ruy băng (dưới), rộng đủ ruy băng
    top_need = cy  # từ tâm lên đỉnh sao
    bot_need = max(mh - cy, rib_y + rbh - cy)
    half_h = int(np.ceil(max(top_need, bot_need))) + 2
    half_w = int(np.ceil(max(cx, mw - cx, rbw / 2))) + 2
    W, H = 2 * half_w, 2 * half_h
    ox, oy = half_w - cx, half_h - cy  # dời khung vào ảnh ghép
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    mimg = Image.fromarray(medal, "RGBA")
    canvas.alpha_composite(mimg, (int(round(ox)), int(round(oy))))
    rib_pos = (int(round(rib_x + ox)), int(round(rib_y + oy)))
    rib_layer = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    rib_layer.alpha_composite(rb, rib_pos)
    # viền sticker trắng của ruy băng chỉ giữ ở mép ngoài: chỗ đè lên khung thì bỏ (khỏi dải trắng vắt ngang khung vàng)
    ra2 = np.array(rib_layer)
    mal = np.array(canvas)[:, :, 3]
    white = (ra2[:, :, :3].min(axis=2) > 200) & (ra2[:, :, 3] > 0)
    ra2[white & (mal > 128), 3] = 0
    rib_layer = Image.fromarray(ra2, "RGBA")
    canvas.alpha_composite(rib_layer)
    arr = np.array(canvas)
    arr[arr[:, :, 3] == 0, :3] = 255
    Image.fromarray(arr, "RGBA").save(os.path.join(DRY or HUD, "huy_hieu_cap.png"))
    ccx, ccy = cx + round(ox), cy + round(oy)

    # cung EXP: rãnh tím nhạt (giữa r_in và r_out, bỏ nét mực), tô tím đậm giữ vân chì; bỏ chỗ ruy băng che
    full = np.zeros((H, W, 4), np.uint8)
    full[int(round(oy)):int(round(oy)) + mh, int(round(ox)):int(round(ox)) + mw] = medal
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.hypot(xx - ccx, yy - ccy)
    hsv = cv2.cvtColor(full[:, :, :3], cv2.COLOR_RGB2HSV).astype(np.int32)
    lum = full[:, :, :3].astype(np.float32).mean(axis=2)
    ring = (rr >= geo["r_in"] - 3) & (rr <= geo["r_out"] + 3) & (full[:, :, 3] > 128)
    pale = ring & (hsv[:, :, 2] > 120) & (hsv[:, :, 1] < 150)
    # độ phủ mềm ở mép nét mực: sáng càng gần màu rãnh càng đục
    lav_l = np.median(lum[pale])
    k = np.clip((lum - 90) / max(1, lav_l - 90), 0, 1)
    alpha = (pale * k * 255).astype(np.float32)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    alpha[np.array(rib_layer)[:, :, 3] > 40] = 0
    shade = np.clip(lum / max(1, lav_l), 0.75, 1.15)[..., None]
    col = np.clip(EXP_RGB[None, None, :] * shade, 0, 255).astype(np.uint8)
    arc = np.dstack([col, alpha.astype(np.uint8)])
    arc[arc[:, :, 3] == 0, :3] = np.array(EXP_RGB, np.uint8)
    # ảnh vuông tâm vòng tròn (Radial 360 quay quanh giữa ảnh)
    R = int(np.ceil(geo["r_out"])) + 6
    sq = arc[int(round(ccy)) - R:int(round(ccy)) + R, int(round(ccx)) - R:int(round(ccx)) + R]
    Image.fromarray(sq, "RGBA").save(os.path.join(DRY or HUD, "cung_exp_cap.png"))

    out = dict(
        badge_w=W, badge_h=H,
        circle_cx=float(ccx), circle_cy=float(ccy),
        r_edge=r_edge, r_out=geo["r_out"], r_in=geo["r_in"], r_disc=geo["r_disc"],
        arc_size=2 * R,
        band_cx=float(rib_pos[0] + rbw / 2), band_cy=float(rib_pos[1] + band_cy),
        band_h=float(band_bot - band_top), band_w=float(band_x0.max() - band_x0.min() if len(band_x0) else rbw * 0.6),
    )
    print("huy hiệu:", json.dumps({k: round(v, 1) if isinstance(v, float) else v for k, v in out.items()}, ensure_ascii=False))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(CUT, exist_ok=True)
    os.makedirs(DRY or HUD, exist_ok=True)
    parts = cut_sheet()
    for name in ("ball", "clock", "gear"):
        place_icon(name, parts[name])
    geo = build_badge(parts["medal_b"], parts["ribbon"])
    with open(os.path.join(HERE, "hud_geo.json"), "w", encoding="utf-8") as f:
        json.dump(geo, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
