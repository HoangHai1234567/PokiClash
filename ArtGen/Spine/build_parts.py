# -*- coding: utf-8 -*-
"""Gen BỘ PHẬN phục vụ animation sau khi đã rig (người dùng dặn 2026-11-08: gen một con hoàn chỉnh, rig xương, rồi mới gen thêm bộ
phận). Thay cho việc tự loang màu (inpaint) phần bị che: GPT vẽ đủ phần bị che, đúng chỗ, đúng cỡ trên chính khung concept.

Theo lớp của rig (beasts_cfg.py), lớp có "body" là mốc:
- lớp dưới 1 (duoi1): xoá mọi phần ở các lớp TRƯỚC lớp thân (đầu, tai, sừng, bờm, chân gần, cánh gần, đạo cụ, chuông...), vẽ đủ
  thân và các phần sau nó -> lấp chỗ trống dưới đầu, dưới chân gần cho lớp thân;
- lớp dưới 2 (duoi2): xoá thêm cả lớp thân, chỉ còn các phần SAU thân (chân xa, đuôi, cánh xa) vẽ đủ -> lấp cho các lớp đó.
Mỗi file prompt đính concept + ảnh hướng dẫn (phần cần xoá tô hồng). beast.py căn ảnh trả về khớp concept (ECC affine) rồi chỉ
lấy vùng bị che.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/build_parts.py <id> <k> [1|2 ...]
    -> gui_gpt/<id>_<k>/duoi<n>.txt, gui_gpt/<id>_<k>/duoi<n>_huong_dan.png; lưu inbox/<id>_<k>/tai_ve/L2_duoi<n>.png
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, FLAT  # noqa: E402

NAMES = {"head": "the head with everything on it (ears, horns, antlers, mane, crest, hat, hair)", "ear": "the ear", "tuft": "the crest",
         "leg_bn": "the near back leg", "leg_fn": "the near front leg", "leg_ff": "the front leg in front", "wing_f": "the near wing",
         "arm_f": "the near arm / flipper", "prop": "the item held in the hand", "bell": "the bell", "pend": "the small hanging bell / pendant",
         "claw_b": "the claw in front", "body": "the body / torso", "wings": "the wings"}


def removal_sets(F):
    layers = F["layers"]
    ib = next(i for i, (n, ps, g) in enumerate(layers) if "body" in ps)
    front = [p for _, ps, _ in layers[ib + 1:] for p in ps]
    body = list(layers[ib][1])
    behind = [p for _, ps, _ in layers[:ib] for p in ps]
    return {1: (front, body + behind), 2: (front + body, behind)}


def describe(parts):
    out = []
    for p in parts:
        key = p if p in NAMES else p.split("_")[0]
        d = NAMES.get(key, "the " + p.replace("_", " "))
        if d not in out:
            out.append(d)
    return ", ".join(out)


def guide(rgb, lab, names, remove, path):
    a = rgb.astype(np.float32).copy()
    m = np.isin(lab, [names.index(p) for p in remove if p in names])
    a[m] = a[m] * 0.3 + np.array([255, 0, 200], np.float32) * 0.7
    Image.fromarray(a.astype(np.uint8)).save(path)
    return int(m.sum())


def main(argv):
    import beast as B
    import thuy_long_lien as Q
    hid, k = argv[0], int(argv[1])
    levels = [int(x) for x in argv[2:]] or [1, 2]
    F = B.cfg(hid)["forms"][k]
    B.setup_labels(hid, k, F)
    rgb, fg = B.load(hid, k, F)
    lab = Q.labels(k, rgb, fg)
    names = B.parts_of(F)
    code = B.code(hid, k)
    src = B.src(hid, k)
    out_dir = W(HERE, "gui_gpt", code)
    save_dir = W(HERE, "inbox", code, "tai_ve")
    os.makedirs(out_dir, exist_ok=True)
    sets = removal_sets(F)
    for n in levels:
        remove, keep = sets[n]
        if not keep or not remove:
            print(f"bỏ qua lớp dưới {n} (không có phần cần xoá hoặc giữ)")
            continue
        gp = W(out_dir, f"duoi{n}_huong_dan.png")
        px = guide(rgb, lab, names, remove, gp)
        save = W(save_dir, f"L2_duoi{n}.png")
        t = f"""IMAGES (attached in this order; open each from its path):
image 1 = {src}: the finished hero picture, 1536x1024, white background.
image 2 = {gp}: the same picture, 1536x1024, with the parts to ERASE painted over in pink/magenta.

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L2_duoi{n}_2.png, L2_duoi{n}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: this is an animation helper layer. Edit image 1: ERASE every part that is painted magenta in image 2 ({describe(remove)}), and redraw what was HIDDEN behind them, so that the remaining parts ({describe(keep)}) become complete, as if the erased parts had never been drawn on top.

VERY IMPORTANT, the result is laid exactly over image 1 by a program:
- Same canvas 1536x1024. Every remaining part stays at EXACTLY the same position, size, angle and shape as in image 1, with the same outline and the same colours; do not move, resize, re-pose or restyle anything.
- Only the hidden areas are new: continue the outlines, colours and markings of the remaining parts naturally into the areas that were covered (for example the neck and shoulders under the head, the back under the legs, the root of the tail, the top of the far legs, the base of the wings).
- Where nothing of the remaining parts would be behind the erased parts, leave pure white background.
- Same hand-drawn look as image 1: dark-brown ink outline of the same thickness, coloured-pencil and crayon hatching.
{FLAT}
No new parts, no text, no shadow, no ground line.
"""
        p = W(out_dir, f"duoi{n}.txt")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(t)
        print(p, f"({px} px tô hồng)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
