# Cắt tờ phụ phu.png (Magnific trả nền trong suốt): đầu quay lại cười, cần câu, bàn tay nắm có lỗ, bàn tay xoè.
# Đưa về cùng tỉ lệ tờ gốc rig (đo bề ngang tóc: đầu quay phải rộng ngang đầu sau lưng), rồi nửa cỡ như chuan_bi.py.
# Ra: atom/images/dau_quay.png, can_cau.png, nam_lo.png, tay_xoe.png; ghi thêm vào geo.json mục "extra".
import os, sys, json
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "atom", "images")
SCALE = 0.5
HAND_W = {"nam_lo": 46, "tay_xoe": 66}


def main():
    im = Image.open(os.path.join(HERE, "phu.png")).convert("RGBA")
    a = np.asarray(im).copy()
    alpha = a[..., 3]
    print("alpha: >0", int((alpha > 0).sum()), " >128", int((alpha > 128).sum()), " 1..128", int(((alpha > 0) & (alpha <= 128)).sum()))
    solid = alpha > 160
    solid = cv2.morphologyEx(solid.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0
    n, lab, st, cen = cv2.connectedComponentsWithStats(solid.astype(np.uint8), connectivity=8)
    comps = sorted([i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 3000], key=lambda i: st[i, cv2.CC_STAT_LEFT])
    named = {}
    for i in comps:
        x, y, w, h = st[i, :4]
        if h > 900:
            named["can_cau"] = i
        elif y < 800:
            named["dau_quay"] = i
        elif x < 300:
            named["nam_lo"] = i
        else:
            named["tay_xoe"] = i
    # tỉ lệ: đầu sau lưng rộng 244..770 (526 px tờ gốc); đầu quay đo ở tờ phụ
    geo = json.load(open(os.path.join(HERE, "geo.json")))
    hx, hy, hw, hh = st[named["dau_quay"], :4]
    k = 526.0 / hw * 0.96  # đầu quay hơi hẹp hơn vì nghiêng
    print("tỉ lệ tờ phụ -> tờ gốc", round(k, 3))
    geo["extra"] = {"scale_from_phu": round(k, 4)}
    for name, i in named.items():
        x, y, w, h = st[i, :4]
        m = lab == i
        m = cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0
        crop = a[y:y + h, x:x + w].copy()
        crop[..., 3] = np.where(m[y:y + h, x:x + w], crop[..., 3], 0)
        crop[..., 3] = np.where(crop[..., 3] > 160, 255, crop[..., 3])
        s = k * SCALE
        # bàn tay tờ phụ vẽ to hơn nắm tay tờ gốc: đưa về bề ngang nắm tay gốc (~47 px nửa cỡ); tay xoè rộng hơn vì xoè ngón
        if name in HAND_W:
            s = HAND_W[name] / w
        out = Image.fromarray(crop, "RGBA").resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
        out.save(os.path.join(OUT, name + ".png"))
        geo["extra"][name] = {"w": out.width, "h": out.height, "phu_box": [int(x), int(y), int(w), int(h)]}
        print(f"{name:9s} box {x},{y} {w}x{h} -> {out.width}x{out.height}")
    json.dump(geo, open(os.path.join(HERE, "geo.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
