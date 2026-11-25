# -*- coding: utf-8 -*-
"""Dựng dự án AtomSpine từ khung của gen_khung.py: mỗi hiệu ứng một slot tờ khung (att.seq), mỗi đòn một clip.

    py -3 -I build_atom.py            # chép ảnh, viết atom/build.ops, chạy atom init + atom do
Sau đó: atom sheet / atom export atomik / atom studio (xem cuối file).
"""
import json
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

# vị trí trong cảnh (y lên, gốc ở đất giữa sân)
MIENG = (-300, 130)   # miệng người phun
DICH = (290, 95)      # chỗ trúng trên thân đối thủ
NAM = (290, 0)        # nổ nấm dưới chân đối thủ


def region_offset(fx):
    """Tâm ảnh so với điểm neo (px, y lên)."""
    m = MAN[fx]
    ax, ay = m["anchor"]
    return m["w"] / 2 - ax, ay - m["h"] / 2


def main():
    if not os.path.exists(os.path.join(PROJ, "atomspine.json")):
        subprocess.run(ATOM + ["init", PROJ, "--name", "lua_toon"], check=True)
    img_dir = os.path.join(PROJ, "images")
    os.makedirs(img_dir, exist_ok=True)
    ops = ["project.set name=lua_toon fps=24"]
    for fx, m in MAN.items():
        for i in range(m["count"]):
            nm = f"{fx}_{i:02d}"
            shutil.copyfile(os.path.join(FR, fx, nm + ".png"), os.path.join(img_dir, nm + ".png"))
            ops.append(f"image.add {nm} path=images/{nm}.png")
    ops += [
        f"bone.add mieng parent=root x={MIENG[0]} y={MIENG[1]}",
        f"bone.add dan parent=root x={MIENG[0]} y={MIENG[1]}",
        f"bone.add dich parent=root x={DICH[0]} y={DICH[1]}",
        f"bone.add nam parent=root x={NAM[0]} y={NAM[1]}",
        # tia than bắn theo hướng phun: vfx.burst toả quanh trục "lên" của xương, xoay -90 cho chĩa sang phải
        f"bone.add mieng_tia parent=mieng x=60 y=0 rot=-90",
        "vfx.art than kind=spark palette=fire size=22 seed=3",
    ]
    slots = [("phun", "mieng", "phun_lua"), ("nho", "mieng", "phun_nho"), ("cau", "dan", "cau_lua"),
             ("ten", "dan", "muiten"), ("no", "dich", "no_trung"), ("nam", "nam", "no_nam")]
    for slot, bone, fx in slots:
        ox, oy = region_offset(fx)
        ops += [
            f"slot.add {slot} bone={bone}",
            f"att.region {slot} {fx} image={fx}_00 x={ox:.1f} y={oy:.1f} use=false",
            f"att.seq {slot} {fx} prefix={fx}_ count={MAN[fx]['count']} setup=0",
        ]

    def show(anim, slot, fx, t0, mode, t1=None):
        ops.append(f"key {anim} {slot}.attachment {t0:.3f}:{fx}" + (f" {t1:.3f}:-" if t1 is not None else ""))
        ops.append(f"key {anim} {slot}.seq {t0:.3f}:{mode},0,{DT:.5f}")

    dx, dy = DICH[0] - MIENG[0], DICH[1] - MIENG[1]

    # 1. phun lửa lớn
    d = MAN["phun_lua"]["count"] * DT
    ops.append(f"anim.add phun_lua dur={d + 0.1:.3f}")
    show("phun_lua", "phun", "phun_lua", 0, "once", d)
    ops.append("vfx.burst phun_lua image=than bone=mieng_tia count=14 t=0.08 dur=0.7 speed=520 spread=40 "
               "gravity=-60 spin=180 seed=5")

    # 2. luồng nhỏ lặp (đòn thường / giữ tia)
    ops.append("anim.add phun_nho dur=1.0 loop=true")
    show("phun_nho", "nho", "phun_nho", 0, "loop")

    # 3. cầu lửa: bay 0.55 s rồi nổ trúng
    fly = 0.55
    dn = MAN["no_trung"]["count"] * DT
    ops.append(f"anim.add cau_lua dur={fly + dn + 0.05:.3f}")
    show("cau_lua", "cau", "cau_lua", 0, "loop", fly)
    ops.append(f"key cau_lua dan.translate 0:0,0:easeIn {fly:.3f}:{dx},{dy}")
    ops.append(f"key cau_lua dan.scale 0:0.35,0.35:backOut 0.12:1,1 {fly:.3f}:1.1,1.1")
    show("cau_lua", "no", "no_trung", fly, "once", fly + dn)
    ops.append(f"vfx.shake cau_lua bone=dich t={fly:.3f} dur=0.25 amp=5 freq=30 seed=2")

    # 4. mũi tên lửa: bay nhanh 0.32 s, nổ nhỏ hơn
    fly2 = 0.32
    ops.append(f"anim.add mui_ten dur={fly2 + dn + 0.05:.3f}")
    show("mui_ten", "ten", "muiten", 0, "loop", fly2)
    ops.append(f"key mui_ten dan.translate 0:-40,0:easeIn {fly2:.3f}:{dx},{dy}")
    ops.append(f"key mui_ten dan.scale 0:0.6,0.6:easeOut 0.06:1,1")
    show("mui_ten", "no", "no_trung", fly2, "once", fly2 + dn)
    ops.append(f"key mui_ten dich.scale 0:1,1 {fly2:.3f}:0.7,0.7 {fly2 + dn:.3f}:0.7,0.7")

    # 5. nổ trúng một mình
    ops.append(f"anim.add no_trung dur={dn + 0.1:.3f}")
    show("no_trung", "no", "no_trung", 0, "once", dn)

    # 6. nổ nấm (chiêu cuối)
    dm = MAN["no_nam"]["count"] * DT
    ops.append(f"anim.add no_nam dur={dm + 0.1:.3f}")
    show("no_nam", "nam", "no_nam", 0, "once", dm)
    ops.append("vfx.shake no_nam bone=root t=0.04 dur=0.5 amp=8 freq=28 seed=4")

    path = os.path.join(PROJ, "build.ops")
    open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
    print("ops:", len(ops), "->", path)
    r = subprocess.run(ATOM + ["do", "-p", PROJ, "-f", path], capture_output=True, text=True, encoding="utf-8")
    print((r.stdout + r.stderr)[-1500:])
    sys.exit(r.returncode)


def add_fx(names):
    """Thêm bản phun lửa khác (gen GPT / video) vào dự án đang có: ảnh + slot ở miệng + clip cùng tên."""
    img_dir = os.path.join(PROJ, "images")
    ops = []
    for fx in names:
        m = MAN[fx]
        for i in range(m["count"]):
            nm = f"{fx}_{i:02d}"
            shutil.copyfile(os.path.join(FR, fx, nm + ".png"), os.path.join(img_dir, nm + ".png"))
            ops.append(f"image.add {nm} path=images/{nm}.png")
        ox, oy = region_offset(fx)
        d = m["count"] * DT
        ops += [
            f"slot.add {fx} bone=mieng",
            f"att.region {fx} {fx} image={fx}_00 x={ox:.1f} y={oy:.1f} use=false",
            f"att.seq {fx} {fx} prefix={fx}_ count={m['count']} setup=0",
            f"anim.add {fx} dur={d + 0.1:.3f}",
            f"key {fx} {fx}.attachment 0:{fx} {d:.3f}:-",
            f"key {fx} {fx}.seq 0:once,0,{DT:.5f}",
        ]
        if fx.startswith("phun_video"):  # video bắt đầu lúc lửa đã phồng: phóng to từ nòng cho có đoạn mở đầu
            ops.append(f"key {fx} mieng.scale 0:0.12,0.12:easeOut 0.17:1,1")
    path = os.path.join(PROJ, "them_" + "_".join(names) + ".ops")
    open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
    r = subprocess.run(ATOM + ["do", "-p", PROJ, "-f", path], capture_output=True, text=True, encoding="utf-8")
    print((r.stdout + r.stderr)[-800:])
    sys.exit(r.returncode)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "them":
        add_fx(sys.argv[2].split(","))
    else:
        main()
