# -*- coding: utf-8 -*-
"""Dự án AtomSpine `atom_nuoc/` xem tia nước Blender (vfx_blender/nuoc_blender.py --phan tia | trung).
Người dùng 2026-11-24: "phần va chạm nên tách riêng ra" → hai bộ khung cùng nhịp, cùng tỉ lệ px:
  frames/nuoc_tia   (tia + bông toé ở miệng, neo MIỆNG)
  frames/nuoc_trung (bông va chạm ở đích, neo ĐIỂM CHẠM)
Clip: tia_nuoc (ghép: va chạm đặt ở miệng + 488 px = điểm chạm của khung tia), tia_rieng, va_cham, và mỗi hiệu ứng nước khác một clip
(cau_nuoc, no_nuoc, thuong_nuoc, song_nuoc, song_cuon, toe_nuoc, vung_nuoc, cau_vo, loc_nuoc, mach_phun).
Studio đang mở dự án này có thể ghi đè lúc dựng lại → dừng Studio trước khi chạy.
    py -3 -I build_nuoc.py
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "frames")
PROJ = os.path.join(HERE, "atom_nuoc")
ATOM = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
DT = 1 / 24
MAN = json.load(open(os.path.join(FR, "manifest.json"), encoding="utf-8"))
UPP, HX = 15.2 / 750, 10.0 - 0.12        # đơn vị Blender / px; điểm chạm trên trục tia (nuoc_blender.py)
DX = round(HX / UPP)                      # 488 px từ miệng tới điểm chạm
MIENG = (-320, 120)

args = ["init", PROJ, "--name", "tia_nuoc"] + (["--force"] if os.path.exists(os.path.join(PROJ, "atomspine.json")) else [])
subprocess.run(ATOM + args, check=True)
os.makedirs(os.path.join(PROJ, "images"), exist_ok=True)
ops = ["project.set name=tia_nuoc fps=24"]


def images(fx):
    for i in range(MAN[fx]["count"]):
        nm = f"{fx}_{i:02d}"
        shutil.copyfile(os.path.join(FR, fx, nm + ".png"), os.path.join(PROJ, "images", nm + ".png"))
        ops.append(f"image.add {nm} path=images/{nm}.png")


def slot(name, bone, fx):
    m = MAN[fx]
    ax, ay = m["anchor"]
    ops.extend([f"slot.add {name} bone={bone}",
                f"att.region {name} {fx} image={fx}_00 x={m['w'] / 2 - ax:.1f} y={ay - m['h'] / 2:.1f} use=false",
                f"att.seq {name} {fx} prefix={fx}_ count={m['count']} setup=0"])


def show(anim, name, fx):
    D = MAN[fx]["count"] * DT
    ops.extend([f"key {anim} {name}.attachment 0:{fx} {D:.3f}:-", f"key {anim} {name}.seq 0:once,0,{DT:.5f}"])


for fx in ("nuoc_tia", "nuoc_trung"):
    images(fx)
ops += [f"bone.add b_mieng parent=root x={MIENG[0]} y={MIENG[1]}", f"bone.add b_cham parent=root x={MIENG[0] + DX} y={MIENG[1]}",
        "bone.add b_cham_rieng parent=root x=0 y=120"]
slot("s_tia", "b_mieng", "nuoc_tia")
slot("s_cham", "b_cham", "nuoc_trung")
slot("s_cham_rieng", "b_cham_rieng", "nuoc_trung")
D = MAN["nuoc_tia"]["count"] * DT
ops.append(f"anim.add tia_nuoc dur={D + 0.4:.3f} loop=true")
show("tia_nuoc", "s_tia", "nuoc_tia")
show("tia_nuoc", "s_cham", "nuoc_trung")
ops.append(f"anim.add tia_rieng dur={D + 0.4:.3f} loop=true")
show("tia_rieng", "s_tia", "nuoc_tia")
ops.append(f"anim.add va_cham dur={D + 0.4:.3f} loop=true")
show("va_cham", "s_cham_rieng", "nuoc_trung")
# bộ nước khác (2026-11-24, người dùng: "làm thêm các fx khác hệ nước"): mỗi hiệu ứng một clip, slot riêng ở giữa khung
KHAC = [("cau_nuoc", (0, 120)), ("no_nuoc", (0, 120)), ("thuong_nuoc", (0, 120)), ("song_nuoc", (-200, 0)), ("song_cuon", (-120, -40)), ("toe_nuoc", (0, 120)), ("vung_nuoc", (0, -60)), ("cau_vo", (0, 120)), ("cau_nem", (0, 160)), ("toe_dat", (0, -80)), ("tia_ong", (-320, 60)), ("roi_nuoc", (-320, 60)), ("tia_nuoc2", (-320, 120)), ("thuong_nuoc2", (0, 120)), ("mach_phun2", (0, -100)), ("toe_nuoc2", (0, 120)), ("cau_vo2", (0, 120)), ("loc_nuoc", (0, 0)),
        ("mach_phun", (0, 0))]
for fx, (bx, by) in KHAC:
    images(fx)
    ops.append(f"bone.add b_{fx} parent=root x={bx} y={by}")
    slot(f"s_{fx}", f"b_{fx}", fx)
    d_ = MAN[fx]["count"] * DT
    if MAN[fx]["loop"]:
        ops += [f"anim.add {fx} dur={2 * d_:.3f} loop=true", f"key {fx} s_{fx}.attachment 0:{fx}", f"key {fx} s_{fx}.seq 0:loop,0,{DT:.5f}"]
    else:
        ops.append(f"anim.add {fx} dur={d_ + 0.4:.3f} loop=true")
        show(fx, f"s_{fx}", fx)
path = os.path.join(PROJ, "dung.ops")
open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
r = subprocess.run(ATOM + ["do", "-p", PROJ, "-f", path], capture_output=True, text=True, encoding="utf-8")
print((r.stdout + r.stderr)[-600:])
sys.exit(r.returncode)
