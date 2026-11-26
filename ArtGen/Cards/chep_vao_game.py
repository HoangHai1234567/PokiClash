# -*- coding: utf-8 -*-
"""Chép tranh thẻ chung đã cắt (ArtGen/Cards/cat/<id>.png, 448 x 280 RGBA) vào Assets/03 Art/Cards/tranh_<id>.png (GD_Claude/36).

    py -3 -I ArtGen/Cards/chep_vao_game.py           # chép (ghi đè tranh_<id>.png cũ nếu có)
    py -3 -I ArtGen/Cards/chep_vao_game.py --kiem    # chỉ liệt kê, không chép

Tên "tranh_" (không dùng "card_": ArtImporter cắt 9 mảnh mọi ảnh card_*). Sau khi chép: Unity nhập ảnh (ASTC 6x6, sprite), rồi menu
"PokiClash/Dựng lại danh mục ảnh" để ArtLibrary thấy, và "PokiClash/Thẻ: thêm ô tranh" (một lần) cho prefab thẻ có ô tranh.
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "cat")
DST = os.path.join(ROOT, "Assets", "03 Art", "Cards")


def main(argv):
    kiem = "--kiem" in argv
    unknown = [a for a in argv if a != "--kiem"]
    if unknown:
        print(f"đối số lạ {unknown}: chỉ có --kiem; không làm gì")
        return 2
    pool = [c["id"] for c in json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "cards.json"), encoding="utf-8"))["pool"]]
    thieu = [i for i in pool if not os.path.exists(os.path.join(SRC, i + ".png"))]
    if thieu:
        print(f"thiếu {len(thieu)} tranh trong cat/: {', '.join(thieu)}")
    if not kiem:
        os.makedirs(DST, exist_ok=True)
    n = 0
    for i in pool:
        s = os.path.join(SRC, i + ".png")
        if not os.path.exists(s):
            continue
        if not kiem:
            shutil.copyfile(s, os.path.join(DST, f"tranh_{i}.png"))
        n += 1
    print(f"{'sẽ chép' if kiem else 'đã chép'} {n} tranh → {DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
