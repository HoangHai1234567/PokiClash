# -*- coding: utf-8 -*-
"""Rồng Giọt (dạng 1 mới của dòng Giọt Sương, thay Giọt Nước aola thuy_7): cắt mảnh, khớp, dựng xương, animation trận,
hiệu ứng nước, xuất Spine 4.2 rồi .atomik (2026-11-08). Cách A của skill pokiclash-spine-rig.

    <venv>/Scripts/python -I ArtGen/Spine/rong_giot.py cut | place | build | all
venv cần opencv-python, numpy, Pillow (máy ổ D: D:/spine-venv). Ảnh vào ArtGen/Spine/inbox/rong_giot/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rig  # noqa: E402

CODE = "rong_giot"
BASE = os.path.join(HERE, "inbox", CODE)

SPEC = {
    "base": BASE,
    "sheets": {
        "L2a_head_pieces.png": [["head", "head_blink", "head_shout"], ["crest", "ear_l", "ear_r"]],
        "L2b_body_pieces.png": [["wing_l", "torso", "wing_r", "tail", "sword"], ["arm_l", "fist_l", "arm_r", "fist_r"],
                                ["thigh_l", "foot_l", "thigh_r", "foot_r"]],
    },
    "side": {"wing_l": "l", "wing_r": "r", "ear_l": "l", "ear_r": "r", "arm_l": "l", "fist_l": "l", "arm_r": "r",
             "fist_r": "r", "thigh_l": "l", "foot_l": "l", "thigh_r": "r", "foot_r": "r", "tail": "l", "sword": "r"},
    # vẽ từ sau ra trước (theo ảnh lượt 1: tay trái người xem đè lên mép thân)
    "draw": ["tail", "wing_l", "wing_r", "thigh_l", "foot_l", "thigh_r", "foot_r", "torso", "arm_l", "fist_l", "crest",
             "ear_l", "ear_r", "head", "arm_r", "sword", "fist_r"],
    "swap": {"head": ["head_blink", "head_shout"]},
}
rig.SPEC[CODE] = SPEC

# Mảnh xanh trơn giống nhau nên dò tự do trên cả ảnh hay lạc chỗ (lần đầu 8/17 mảnh sai): dò quanh tâm đọc trên ảnh kẻ lưới
# của L1_duyet.png (x, y, nửa ô dò), tỉ lệ trong khoảng của tờ.
HINT = {
    "head": (536, 638, 60), "crest": (430, 330, 90), "ear_l": (205, 605, 70), "ear_r": (805, 600, 70),
    "torso": (505, 1045, 60), "wing_l": (225, 885, 70), "wing_r": (705, 895, 70), "tail": (185, 1125, 80),
    "sword": (855, 1200, 50), "arm_l": (360, 985, 80), "fist_l": (290, 1095, 60), "arm_r": (670, 1000, 60),
    "fist_r": (712, 1085, 50), "thigh_l": (370, 1240, 60), "foot_l": (322, 1345, 50), "thigh_r": (595, 1250, 60),
    "foot_r": (632, 1342, 50),
}
SCALES = {"L2a_head_pieces.png": (0.75, 1.35), "L2b_body_pieces.png": (0.85, 1.65)}
# lần hai: tay trái bị xoay nằm ngang (dò góc rộng), nắm tay phải dò lệch lên trên chuôi kiếm (lỗ cầm khác chuôi có màu)
HINT.update({"arm_l": (352, 985, 45)})
ROT = {"arm_l": (0, 30)}
FIXED = {"fist_r": {"s": 0.844, "r": -1.0, "cx": 748.0, "cy": 1092.0}}
GRIP = (34, 74, 138)  # màu cán kiếm quấn xanh sẫm: tô vào lòng nắm tay phải (GPT vẽ lỗ rỗng, bộ cắt lấp thành trắng)


def fix_parts():
    """Lòng nắm tay phải: vùng trắng kín bên trong mảnh tô màu cán kiếm, nên kiếm cắm vào nắm không lộ lỗ trắng."""
    import cv2
    import numpy as np
    from PIL import Image
    p = os.path.join(rig.paths(CODE)["parts"], "fist_r.png")
    im = np.array(Image.open(p).convert("RGBA"))
    rgb, a = im[:, :, :3].astype(np.int16), im[:, :, 3]
    white = ((rgb.min(2) > 200) & (a > 128)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
    h, w = a.shape
    done = 0
    for i in range(1, n):
        x, y, bw, bh, area = st[i]
        if area < 150 or x == 0 or y == 0 or x + bw >= w or y + bh >= h:
            continue
        m = lab == i
        m = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        m &= rgb.min(2) > 150  # không lấn vào nét mực
        noise = np.random.default_rng(7).integers(-10, 11, (h, w, 1))
        im[:, :, :3][m] = np.clip(np.array(GRIP)[None, None, :] + noise, 0, 255)[m].astype(np.uint8)
        done += int(m.sum())
    Image.fromarray(im).save(p)
    print(f"  fist_r: tô lòng nắm {done} điểm ảnh màu cán kiếm")


def place(redo=None):
    """redo: tên mảnh dò lại; None = mảnh chưa có trong placed.json (lần đầu: mọi mảnh)."""
    import json
    import numpy as np
    from PIL import Image
    P = rig.paths(CODE)
    ref = np.array(Image.open(P["ref"]).convert("RGB"))
    H, W = ref.shape[:2]
    rfg = rig.fg_mask(ref)
    ref_lab = rig.lab_f(ref)
    pj = os.path.join(P["rig"], "placed.json")
    old = json.load(open(pj))["parts"] if os.path.exists(pj) else {}
    out = {}
    pdir = os.path.join(P["rig"], "placed")
    os.makedirs(pdir, exist_ok=True)
    extras = {e for v in SPEC["swap"].values() for e in v}
    for sheet, rows in SPEC["sheets"].items():
        lo, hi = SCALES[sheet]
        for name in [n for row in rows for n in row if n not in extras]:
            if name in FIXED:
                out[name] = dict(FIXED[name], err=0.0)
                print(f"  {name:10s} đặt tay: {FIXED[name]}")
                continue
            if name in old and (redo is None or name not in redo):
                out[name] = {k: old[name][k] for k in ("s", "r", "cx", "cy", "err")}
                continue
            part = np.array(Image.open(os.path.join(P["parts"], name + ".png")).convert("RGBA"))
            cx, cy, win = HINT[name]
            r0, r1 = ROT.get(name, (-36, 36))
            c = rig.match(ref_lab, part, np.arange(lo, hi + 1e-6, 0.04), range(r0, r1 + 1, 6), 0.25, None, (cx, cy), win)
            c = rig.match(ref_lab, part, np.arange(c[1] * 0.95, c[1] * 1.051, c[1] * 0.012), np.arange(c[2] - 6, c[2] + 6.1, 2),
                          0.5, None, (c[3], c[4]), 24)
            err, s, r, x, y = rig.match(ref_lab, part, np.arange(c[1] * 0.985, c[1] * 1.016, c[1] * 0.005),
                                        np.arange(c[2] - 2, c[2] + 2.1, 1), 1.0, None, (c[3], c[4]), 8)
            out[name] = {"s": round(float(s), 4), "r": round(float(r), 2), "cx": round(float(x), 1), "cy": round(float(y), 1),
                         "err": round(float(err), 1)}
            print(f"  {name:10s} s={s:.3f} r={r:+.0f} tâm=({x:.0f},{y:.0f}) gợi ý=({cx},{cy}) sai={err:.0f}", flush=True)
    for main_, exs in SPEC["swap"].items():  # đầu nhắm mắt, đầu hét: cùng chỗ, cùng cỡ với đầu (GPT vẽ trùng khung)
        for ex in exs:
            out[ex] = dict(out[main_], of=main_)
    comp = np.full((H, W, 3), 255, np.float32)
    for name, t in out.items():
        part = np.array(Image.open(os.path.join(P["parts"], name + ".png")).convert("RGBA"))
        wp = rig.warp(part, t["s"], t["r"])
        Image.fromarray(wp).save(os.path.join(pdir, name + ".png"))
        t["w"], t["h"] = int(wp.shape[1]), int(wp.shape[0])
        t["x0"], t["y0"] = int(round(t["cx"] - wp.shape[1] / 2)), int(round(t["cy"] - wp.shape[0] / 2))
    for name in SPEC["draw"]:
        t = out[name]
        rig.paste(comp, np.array(Image.open(os.path.join(pdir, name + ".png"))), t["x0"], t["y0"])
    comp = comp.astype(np.uint8)
    cfg = rig.fg_mask(comp)
    iou = float((cfg & rfg).sum() / max(1, (cfg | rfg).sum()))
    diff = np.zeros_like(ref)
    diff[(rfg > 0) & (cfg == 0)] = (230, 60, 60)
    diff[(rfg == 0) & (cfg > 0)] = (60, 110, 230)
    diff[(rfg > 0) & (cfg > 0)] = (205, 205, 205)
    Image.fromarray(np.concatenate([ref, comp, diff], 1)).save(os.path.join(P["rig"], "so_ghep.png"))
    json.dump({"ref_size": [W, H], "iou": round(iou, 4), "parts": out}, open(os.path.join(P["rig"], "placed.json"), "w"),
              indent=1)
    print(f"IoU bóng ghép/ảnh gốc = {iou:.3f}  ->  {os.path.join(P['rig'], 'so_ghep.png')}")


def main(argv):
    step = argv[0] if argv else "all"
    if step in ("cut", "all"):
        rig.cut(CODE)
        fix_parts()
    if step in ("place", "all"):
        place(argv[1:] or None)
    if step in ("build", "all"):
        import rong_giot_build
        rong_giot_build.build()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
