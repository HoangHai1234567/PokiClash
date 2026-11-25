# -*- coding: utf-8 -*-
"""Ghép bộ lửa Blender thành đòn trong dự án AtomSpine (atom/): cầu lửa bay → nổ, kim lửa ×3, lốc xoáy, lửa cháy, thiên thạch.
Khung lấy từ frames/<fx>/ (cat_gen.save), điểm neo trong manifest.json.

    py -3 -I build_bl.py
"""
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "frames")
PROJ = os.path.join(HERE, "atom")
ATOM = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
DT = 1 / 24
MAN = json.load(open(os.path.join(FR, "manifest.json"), encoding="utf-8"))
MIENG, DICH, DAT = (-300, 130), (290, 95), (290, 0)
ops = []


def off(fx):
    m = MAN[fx]
    ax, ay = m["anchor"]
    return m["w"] / 2 - ax, ay - m["h"] / 2


def images(fx):
    for i in range(MAN[fx]["count"]):
        nm = f"{fx}_{i:02d}"
        shutil.copyfile(os.path.join(FR, fx, nm + ".png"), os.path.join(PROJ, "images", nm + ".png"))
        ops.append(f"image.add {nm} path=images/{nm}.png")


def slot(name, bone, fx):
    ox, oy = off(fx)
    ops.extend([f"slot.add {name} bone={bone}",
                f"att.region {name} {fx} image={fx}_00 x={ox:.1f} y={oy:.1f} use=false",
                f"att.seq {name} {fx} prefix={fx}_ count={MAN[fx]['count']} setup=0"])


def show(anim, name, fx, t0, mode, t1=None):
    ops.append(f"key {anim} {name}.attachment {t0:.3f}:{fx}" + (f" {t1:.3f}:-" if t1 is not None else ""))
    ops.append(f"key {anim} {name}.seq {t0:.3f}:{mode},0,{DT:.5f}")


def bone(name, x, y, s=1.0, rot=0.0):
    ops.append(f"bone.add {name} parent=root x={x} y={y} sx={s} sy={s} rot={rot}")


for fx in ("cau_bl", "no_bl", "kim_bl", "loc_bl", "lua_bl"):
    images(fx)
DN = MAN["no_bl"]["count"] * DT

# ---------------------------------------------------------------- 1. cầu lửa bay → nổ
bone("b_cau", *MIENG, s=0.45)
bone("b_no", *DICH, s=0.62)
slot("s_cau", "b_cau", "cau_bl")
slot("s_no", "b_no", "no_bl")
fly = 0.55
dx, dy = DICH[0] - MIENG[0], DICH[1] - MIENG[1]
ops.append(f"anim.add cau_lua_bl dur={fly + DN + 0.05:.3f}")
show("cau_lua_bl", "s_cau", "cau_bl", 0, "loop", fly)
ops.append(f"key cau_lua_bl b_cau.translate 0:0,0:easeIn {fly:.3f}:{dx},{dy}")
ops.append(f"key cau_lua_bl b_cau.scale 0:0.3,0.3:backOut 0.12:1,1")
show("cau_lua_bl", "s_no", "no_bl", fly, "once", fly + DN)
ops.append(f"vfx.shake cau_lua_bl bone=b_no t={fly:.3f} dur=0.25 amp=4 freq=30 seed=3")

# ---------------------------------------------------------------- 2. nổ đứng riêng
ops.append(f"anim.add no_lua_bl dur={DN + 0.1:.3f}")
show("no_lua_bl", "s_no", "no_bl", 0, "once", DN)
ops.append("key no_lua_bl b_no.scale 0:1.3,1.3")

# ---------------------------------------------------------------- 3. kim lửa ×3, so le, nổ nhỏ ở đích
fly_k = 0.28
ops.append(f"anim.add kim_lua_bl dur={0.2 + fly_k + DN + 0.05:.3f}")
for k, (oy, ty, t0) in enumerate([(22, 120, 0.0), (0, 92, 0.1), (-22, 66, 0.2)]):
    bk, nk = f"b_kim{k}", f"b_nk{k}"
    bone(bk, MIENG[0], MIENG[1] + oy, s=0.42, rot=math.degrees(math.atan2(ty - MIENG[1] - oy, DICH[0] - MIENG[0])))
    bone(nk, DICH[0] - 10 + 12 * k, ty, s=0.3)
    slot(f"s_kim{k}", bk, "kim_bl")
    slot(f"s_nk{k}", nk, "no_bl")
    ddx, ddy = DICH[0] - MIENG[0], ty - MIENG[1] - oy
    show("kim_lua_bl", f"s_kim{k}", "kim_bl", t0, "loop", t0 + fly_k)
    if t0 > 0:
        ops.append(f"key kim_lua_bl s_kim{k}.attachment 0:-")
    ops.append(f"key kim_lua_bl {bk}.translate {t0:.3f}:0,0:easeIn {t0 + fly_k:.3f}:{ddx},{ddy}")
    show("kim_lua_bl", f"s_nk{k}", "no_bl", t0 + fly_k, "once", t0 + fly_k + DN)
    ops.append(f"key kim_lua_bl s_nk{k}.attachment 0:- {t0 + fly_k:.3f}:no_bl {t0 + fly_k + DN:.3f}:-")

# ---------------------------------------------------------------- 4. lốc xoáy lửa: mọc lên, xoáy, thu lại
bone("b_loc", *DAT, s=0.75)
slot("s_loc", "b_loc", "loc_bl")
ops.append("anim.add loc_lua_bl dur=2.1")
show("loc_lua_bl", "s_loc", "loc_bl", 0, "loop", 2.05)
ops.append("key loc_lua_bl b_loc.scale 0:0.15,0.05:backOut 0.32:1,1 1.7:1.05,1.08:easeIn 2.05:0.2,1.25")
ops.append("key loc_lua_bl s_loc.alpha 0:1 1.8:1 2.05:0")

# ---------------------------------------------------------------- 5. lửa cháy (lặp)
bone("b_lua", *DAT, s=0.5)
slot("s_lua", "b_lua", "lua_bl")
ops.append(f"anim.add lua_chay_bl dur={2 * MAN['lua_bl']['count'] * DT:.3f} loop=true")
show("lua_chay_bl", "s_lua", "lua_bl", 0, "loop")

# ---------------------------------------------------------------- 6. thiên thạch: cầu lửa rơi chéo → nổ lớn
start = (DAT[0] - 330, DAT[1] + 560)
ang = math.degrees(math.atan2(DAT[1] + 30 - start[1], DAT[0] - start[0]))
bone("b_tt", *start, s=0.6, rot=ang)
bone("b_ntt", DAT[0], DAT[1] + 40, s=1.15)
slot("s_tt", "b_tt", "cau_bl")
slot("s_ntt", "b_ntt", "no_bl")
fall = 0.6
ops.append(f"anim.add thien_thach_bl dur={fall + DN + 0.05:.3f}")
show("thien_thach_bl", "s_tt", "cau_bl", 0, "loop", fall)
ops.append(f"key thien_thach_bl b_tt.translate 0:0,0:easeIn {fall:.3f}:{DAT[0] - start[0]},{DAT[1] + 30 - start[1]}")
show("thien_thach_bl", "s_ntt", "no_bl", fall, "once", fall + DN)
ops.append(f"vfx.shake thien_thach_bl bone=root t={fall:.3f} dur=0.45 amp=9 freq=26 seed=5")

path = os.path.join(PROJ, "bo_lua_bl.ops")
open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
r = subprocess.run(ATOM + ["do", "-p", PROJ, "-f", path], capture_output=True, text=True, encoding="utf-8")
print((r.stdout + r.stderr)[-1200:])
sys.exit(r.returncode)
