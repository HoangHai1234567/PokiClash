# -*- coding: utf-8 -*-
"""Hỏa Quy dạng 1 (rùa non, rua_lua_non hướng mầm lửa; suất nguu_quyen) + clip `evolve`: gộp dạng 2 (rua_lua_1) vào rig dạng 1 bằng
mo_xe/atomik_dang.gop_tien_hoa (dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng khung 0 idle của nó). Chép từ golem_lua_non_th.py.

Slot ẩn sẵn của hai rig (mắt tắt, pha lê nguội: fade 1) phải ẩn suốt clip evolve: gop_tien_hoa đặt alpha 1 cho MỌI slot nên sửa lại khoá
alpha của các slot đó về 0.

    py -3 -I ArtGen/Spine/rua_lua_non_th.py          → inbox/rua_lua_non/rig_mam_lua/rua_lua_non_th.atomik + khung_evolve.png
    py -3 -I ArtGen/Spine/rua_lua_non_th.py chep     → thêm: chép vào Assets/03 Art/Heroes/Resources/rua_lua_non (+ chân dung)
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
RA = os.path.join(HERE, "inbox", "rua_lua_non", "rig_" + (os.environ.get("RL_NON") or "chibi"))
SRC_A = os.path.join(RA, "rua_lua_non.atomik")
SRC_B = os.path.join(HERE, "inbox", "rua_lua_1", "rig", "rua_lua_1.atomik")
SIZE_A, SIZE_B = float(os.environ.get("RL_CO") or 0.78), 1.1   # cỡ dạng 1 (theo hướng: rua_lua_non.HUONG[..]["co"]), dạng 2 trong heroes.json (khối nguu_quyen)


def main(a):
    J, img, ver = A.load(SRC_A)
    JB, imgB, _ = A.load(SRC_B)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = SIZE_B / SIZE_A * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["bone3"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RA, "rua_lua_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; dạng 2 trong rig gộp × {k_B:.3f}; {n} slot ẩn giữ ẩn trong evolve; {kq}")
    # tờ khung evolve
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    ims = [A.render(J, img, A.Pose(J).at(ci, t), box, 0.5, bg=(150, 150, 150)).convert("RGB") for t in ts]
    cot = 6
    out = Image.new("RGB", (cot * ims[0].width, ((len(ims) + cot - 1) // cot) * ims[0].height), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    out.save(os.path.join(RA, "khung_evolve.png"))
    print(os.path.join(RA, "khung_evolve.png"), out.size)
    if a and a[0] == "chep":
        d = os.path.join(RES, "rua_lua_non")
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(p, os.path.join(d, "rua_lua_non.atomik"))
        shutil.copyfile(os.path.join(RA, "chan_dung.png"), os.path.join(d, "rua_lua_non_portrait.png"))
        print("đã chép vào", d)


if __name__ == "__main__":
    main(sys.argv[1:])
