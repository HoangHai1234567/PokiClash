# -*- coding: utf-8 -*-
"""Nhím thép (quai_kim): thay 4 chi bằng ảnh gen lại đúng chỗ (người dùng 2026-11-21, comment Studio: "chân bị khuyết 1 mảnh",
"tay và chân đều lỗi, bị khuyết mảnh và nhem nhuốc", "lỗi gen thừa và khuyết mảnh").

Mảnh chân, tay cũ cắt từ concept rồi để code vá phần bị thân che: viền hở, chỏm tròn lạ, lộ ra khi chi vung. Ảnh mới
inbox/quai_kim/tai_ve/chi_L2.png (Magnific gpt-2-6, concept làm ảnh mẫu, cùng khung 1536x1024): mỗi chi một hình kín viền mực,
phần bị thân che vẽ tiếp vào trong. Vuốt tay gần vẫn là mảnh vuot_gan cũ.

    py -3 -I ArtGen/Spine/quai_kim_chi.py      # cắt -> quai_kim/atom/images/{chan_xa,chan_gan,tay_xa,tay_gan}.png + parts.json
    bash ArtGen/Spine/quai_kim/build.sh        # dựng lại project AtomSpine

Mảnh cũ chép vào quai_kim/_cu_1121/ (không xoá).
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "quai_kim")
SRC = os.path.join(HERE, "inbox", "quai_kim", "tai_ve", "chi_L2.png")
NAMES = ["chan_xa", "chan_gan", "tay_xa", "tay_gan"]
# concept tô chi phía xa tối hơn (chiều sâu); ảnh gen sáng hơn ~10-15 mức: kéo màu xanh về trung vị của concept
SHIFT = {"chan_xa": (-9, -9, -12), "tay_xa": (-11, -11, -15)}
PAD = 4


def main():
    pj = os.path.join(D, "parts.json")
    P = json.load(open(pj, encoding="utf-8"))
    parts = {p["name"]: p for p in P["parts"]}
    im = np.array(Image.open(SRC).convert("RGBA")).astype(np.int32)
    im[im[:, :, 3] < 40, 3] = 0  # viền mờ quá nhạt: bỏ
    n, lab, stats, cent = cv2.connectedComponentsWithStats((im[:, :, 3] > 0).astype(np.uint8), connectivity=8)
    comps = sorted(range(1, n), key=lambda i: -stats[i, cv2.CC_STAT_AREA])[:4]
    # gán mỗi hình cho chi có tâm (mảnh cũ) gần nhất
    want = {nm: (parts[nm]["at"][0] + parts[nm]["size"][0] / 2, parts[nm]["at"][1] + parts[nm]["size"][1] / 2) for nm in NAMES}
    got = {}
    for nm, (cx, cy) in want.items():
        best = min(comps, key=lambda i: (cent[i][0] - cx) ** 2 + (cent[i][1] - cy) ** 2)
        if best in got.values():
            raise SystemExit(f"hai chi trùng một hình: {nm}")
        got[nm] = best
    bak = os.path.join(D, "_cu_1121")
    os.makedirs(bak, exist_ok=True)
    for nm, ci in got.items():
        src_old = os.path.join(D, "atom", "images", f"{nm}.png")
        if os.path.exists(src_old) and not os.path.exists(os.path.join(bak, f"{nm}.png")):
            shutil.copyfile(src_old, os.path.join(bak, f"{nm}.png"))
        x, y, w, h = (int(v) for v in stats[ci, :4])
        x0, y0 = max(0, x - PAD), max(0, y - PAD)
        x1, y1 = min(im.shape[1], x + w + PAD), min(im.shape[0], y + h + PAD)
        cut = im[y0:y1, x0:x1].copy()
        cut[lab[y0:y1, x0:x1] != ci, 3] = 0  # chỉ giữ hình của chi này
        if nm in SHIFT:
            rgb = cut[:, :, :3]
            lum = rgb @ np.array([0.299, 0.587, 0.114])
            blue = (cut[:, :, 3] > 0) & (rgb[:, :, 2] - rgb[:, :, 0] > 15) & (lum > 50)
            rgb[blue] = np.clip(rgb[blue] + np.array(SHIFT[nm]), 0, 255)
        Image.fromarray(cut.astype(np.uint8), "RGBA").save(os.path.join(D, "atom", "images", f"{nm}.png"))
        old = (parts[nm]["at"], parts[nm]["size"])
        parts[nm]["at"] = [x0, y0]
        parts[nm]["size"] = [x1 - x0, y1 - y0]
        print(f"{nm}: {old[0]} {old[1]} -> {parts[nm]['at']} {parts[nm]['size']}")
    json.dump(P, open(pj, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
