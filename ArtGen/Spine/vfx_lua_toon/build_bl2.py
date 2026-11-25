# -*- coding: utf-8 -*-
"""Dự án AtomSpine sạch `atom_bl/` cho bộ lửa Blender CÓ KHÓI: phun lửa, cầu lửa → nổ, nổ, kim lửa ×3, lốc xoáy, lửa cháy,
thiên thạch. Khói = tờ khung khoi_bl (cụm nhiều múi nâu xám, tách cụm rồi tan), rải thành nhiều cụm sau lửa:
bốc từ thân lửa, vệt khói đuôi dọc đường bay (luật dự án: vật bay cháy kéo khói đuôi), cụm khói khi nổ, khói đỉnh lốc / lửa cháy.

    py -3 -I build_bl2.py        (tạo lại atom_bl từ đầu)
"""
import json
import math
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "frames")
PROJ = os.path.join(HERE, "atom_bl")
ATOM = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
DT = 1 / 24
MAN = json.load(open(os.path.join(FR, "manifest.json"), encoding="utf-8"))
MIENG, DICH, DAT = (-300, 130), (290, 95), (290, 0)
KL = MAN["khoi_bl"]["count"] * DT          # đời một cụm khói
rnd = random.Random(7)
ops = ["project.set name=lua_blender fps=24", "vfx.art than kind=spark palette=fire size=22 seed=3"]


def off(fx):
    m = MAN[fx]
    ax, ay = m["anchor"]
    return m["w"] / 2 - ax, ay - m["h"] / 2


def images(fx):
    for i in range(MAN[fx]["count"]):
        nm = f"{fx}_{i:02d}"
        shutil.copyfile(os.path.join(FR, fx, nm + ".png"), os.path.join(PROJ, "images", nm + ".png"))
        ops.append(f"image.add {nm} path=images/{nm}.png")


def bone(name, x, y, s=1.0, rot=0.0):
    ops.append(f"bone.add {name} parent=root x={x:.1f} y={y:.1f} sx={s:.3f} sy={s:.3f} rot={rot:.2f}")


def slot(name, b, fx, back=False):
    ox, oy = off(fx)
    ops.extend([f"slot.add {name} bone={b}" + (" at=back" if back else ""),
                f"att.region {name} {fx} image={fx}_00 x={ox:.1f} y={oy:.1f} use=false",
                f"att.seq {name} {fx} prefix={fx}_ count={MAN[fx]['count']} setup=0"])


def show(anim, name, fx, t0, mode, t1=None):
    pre = "0:- " if t0 > 0 else ""
    ops.append(f"key {anim} {name}.attachment {pre}{t0:.3f}:{fx}" + (f" {t1:.3f}:-" if t1 is not None else ""))
    ops.append(f"key {anim} {name}.seq {t0:.3f}:{mode},0,{DT:.5f}")


puffs = [0]


def puff(anim, x, y, t0, sc, rise, drift, dur=None):
    """Một cụm khói (vẽ sau mọi thứ) bắt đầu ở t0 tại (x, y), bay lên `rise`, trôi ngang `drift`.
    dur: độ dài clip lặp → cụm vượt quá cuối clip được quấn về đầu (lặp liền)."""
    puffs[0] += 1
    b, s = f"kb{puffs[0]}", f"ks{puffs[0]}"
    bone(b, x, y, s=sc)
    slot(s, b, "khoi_bl", back=True)
    t1 = t0 + KL
    if dur is None or t1 <= dur:
        show(anim, s, "khoi_bl", t0, "once", t1)
        ops.append(f"key {anim} {b}.translate {t0:.3f}:0,0:easeOut {t1:.3f}:{drift:.0f},{rise:.0f}")
        return
    k = int(round((dur - t0) / DT))                 # số khung đã chạy trước khi quấn
    tb = t1 - dur
    q = (dur - t0) / KL
    ops.append(f"key {anim} {s}.attachment 0:khoi_bl {tb:.3f}:- {t0:.3f}:khoi_bl")
    ops.append(f"key {anim} {s}.seq 0:once,{k},{DT:.5f} {t0:.3f}:once,0,{DT:.5f}")
    ops.append(f"key {anim} {b}.translate 0:{drift * q:.0f},{rise * q:.0f} {tb:.3f}:{drift:.0f},{rise:.0f} "
               f"{t0:.3f}:0,0:easeOut {dur:.3f}:{drift * q:.0f},{rise * q:.0f}")


def trail(anim, p0, p1, fly, n, sc, t_start=0.04):
    """Vệt khói đuôi: n cụm nhỏ rải dọc đường bay (vị trí theo easeIn ~ t²), bay lên ít, trôi ngược hướng bay."""
    for i in range(n):
        t = t_start + (fly - t_start) * i / max(n - 1, 1) * 0.92
        q = (t / fly) ** 2
        x = p0[0] + (p1[0] - p0[0]) * q
        y = p0[1] + (p1[1] - p0[1]) * q
        d = (-(p1[0] - p0[0]) * 0.06, 30 + rnd.uniform(0, 20))
        puff(anim, x + rnd.uniform(-6, 6), y + rnd.uniform(-6, 6), t, sc * rnd.uniform(0.85, 1.15), d[1], d[0])


def fly_keys(anim, b, p0, p1, fly, k=10):
    """Khoá bay tăng tốc dần (vị trí ~ (t/fly)²) bằng k đoạn thẳng: hạt đuôi đặt đúng chỗ quả cầu đi qua."""
    vals = []
    for i in range(k + 1):
        t = fly * i / k
        q = (t / fly) ** 2
        vals.append(f"{t:.3f}:{(p1[0] - p0[0]) * q:.1f},{(p1[1] - p0[1]) * q:.1f}")
    ops.append(f"key {anim} {b}.translate " + " ".join(vals))


def fire_trail(anim, p0, p1, fly, sc, step=16, start=10):
    """Vệt đuôi gắn vào cầu: mỗi `step` px quả cầu đi qua thả một hạt duoi_bl (lửa đậm → khói) ngay sau nó, vẽ sau cầu."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    d = start
    while d < L - 4:
        t = fly * math.sqrt(d / L)                      # vị trí ~ t² → quãng d đạt lúc t
        x, y = p0[0] + ux * (d - 8), p0[1] + uy * (d - 8)
        puffs[0] += 1
        b, s = f"kb{puffs[0]}", f"ks{puffs[0]}"
        bone(b, x + rnd.uniform(-3, 3), y + rnd.uniform(-4, 4), s=sc * rnd.uniform(0.9, 1.1))
        slot(s, b, "duoi_bl", back=True)
        t1 = t + MAN["duoi_bl"]["count"] * DT
        show(anim, s, "duoi_bl", t, "once", t1)
        ops.append(f"key {anim} {b}.translate {t:.3f}:0,0:easeOut {t1:.3f}:{-ux * 25:.0f},{30 + rnd.uniform(0, 25):.0f}")
        d += step


def boom_smoke(anim, x, y, t0, sc, n=4):
    for i in range(n):
        a = i / n * 2 * math.pi + rnd.uniform(-0.4, 0.4)
        puff(anim, x + math.cos(a) * 28 * sc, y + 20 * sc + math.sin(a) * 14 * sc, t0 + 0.06 * i + rnd.uniform(0, 0.04),
             sc * rnd.uniform(0.8, 1.15), 110 * sc + rnd.uniform(0, 30), math.cos(a) * 30 * sc)


# ---------------------------------------------------------------- dựng
if os.path.exists(os.path.join(PROJ, "atomspine.json")):
    subprocess.run(ATOM + ["init", PROJ, "--name", "lua_blender", "--force"], check=True)
else:
    subprocess.run(ATOM + ["init", PROJ, "--name", "lua_blender"], check=True)
os.makedirs(os.path.join(PROJ, "images"), exist_ok=True)
for fx in ("phun_bl2", "cau_bl", "no_bl", "kim_bl", "loc_bl", "lua_bl", "khoi_bl", "duoi_bl"):
    images(fx)
DN = MAN["no_bl"]["count"] * DT

# 1. phun lửa + đốm than + khói bốc từ thân lửa
bone("b_mieng", *MIENG)
bone("b_tia", MIENG[0] + 60, MIENG[1], rot=-90)
slot("s_phun", "b_mieng", "phun_bl2")
DP = MAN["phun_bl2"]["count"] * DT
ops.append(f"anim.add phun_lua dur={DP + 0.5:.3f}")
show("phun_lua", "s_phun", "phun_bl2", 0, "once", DP)
ops.append("vfx.burst phun_lua image=than prefix=tph bone=b_tia count=12 t=0.3 dur=1.0 speed=430 spread=55 gravity=-50 spin=140 seed=11")
# khói: chỉ vài cụm quanh đầu luồng lửa, hiện lúc lửa bắt đầu tan (người dùng 2026-11-24)
# khói ở vùng GẦN CUỐI luồng (~65–85 % chiều dài từ miệng, không phải chót), mép trên thân lửa, thấy rõ từ ~1,2 s (người dùng chỉ khung 29)
for t, dx, dy, sc_ in [(1.02, 310, 85, 0.55), (1.1, 360, 100, 0.65), (1.18, 335, 70, 0.6), (1.28, 395, 95, 0.62), (1.4, 350, 80, 0.55)]:
    puff("phun_lua", MIENG[0] + dx, MIENG[1] + dy, t, sc_, rnd.uniform(90, 130), rnd.uniform(10, 30))

# 2. cầu lửa bay (khói đuôi) → nổ (cụm khói)
bone("b_cau", *MIENG, s=0.42)
bone("b_no", *DICH, s=0.62)
slot("s_cau", "b_cau", "cau_bl")
slot("s_no", "b_no", "no_bl")
fly = 0.55
ops.append(f"anim.add cau_lua dur={fly + DN + 0.6:.3f}")
show("cau_lua", "s_cau", "cau_bl", 0, "loop", fly)
fly_keys("cau_lua", "b_cau", MIENG, DICH, fly)
ops.append("key cau_lua b_cau.scale 0:0.3,0.3:backOut 0.12:1,1")
show("cau_lua", "s_no", "no_bl", fly, "once", fly + DN)
ops.append(f"vfx.shake cau_lua bone=b_no t={fly:.3f} dur=0.25 amp=4 freq=30 seed=3")
fire_trail("cau_lua", MIENG, DICH, fly, 0.55)
boom_smoke("cau_lua", DICH[0], DICH[1], fly + 0.25, 0.62)

# 3. nổ đứng riêng
ops.append(f"anim.add no_lua dur={DN + 0.8:.3f}")
show("no_lua", "s_no", "no_bl", 0, "once", DN)
ops.append("key no_lua b_no.scale 0:1.3,1.3")
boom_smoke("no_lua", DICH[0], DICH[1], 0.25, 0.85, n=5)

# 4. kim lửa ×3 (khói đuôi nhỏ, khói nhỏ ở chỗ trúng)
fly_k = 0.3
ops.append(f"anim.add kim_lua dur={0.2 + fly_k + DN + 0.5:.3f}")
for k, (oy, ty, t0) in enumerate([(22, 120, 0.0), (0, 92, 0.1), (-22, 66, 0.2)]):
    p0, p1 = (MIENG[0], MIENG[1] + oy), (DICH[0], ty)
    bone(f"b_kim{k}", *p0, s=0.5, rot=math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0])))
    bone(f"b_nk{k}", DICH[0] - 10 + 12 * k, ty, s=0.3)
    slot(f"s_kim{k}", f"b_kim{k}", "kim_bl")
    slot(f"s_nk{k}", f"b_nk{k}", "no_bl")
    show("kim_lua", f"s_kim{k}", "kim_bl", t0, "loop", t0 + fly_k)
    ops.append(f"key kim_lua b_kim{k}.translate {t0:.3f}:0,0:easeIn {t0 + fly_k:.3f}:{p1[0] - p0[0]},{p1[1] - p0[1]}")
    ops.append(f"key kim_lua b_kim{k}.scale {t0:.3f}:0.4,1:easeOut {t0 + 0.08:.3f}:1,1")
    show("kim_lua", f"s_nk{k}", "no_bl", t0 + fly_k, "once", t0 + fly_k + DN)
    for i in range(5):
        t = t0 + 0.05 + 0.05 * i
        q = ((t - t0) / fly_k) ** 2
        puff("kim_lua", p0[0] + (p1[0] - p0[0]) * q + rnd.uniform(-15, 15), p0[1] + (p1[1] - p0[1]) * q + rnd.uniform(-5, 5),
             t, rnd.uniform(0.1, 0.14), rnd.uniform(18, 30), rnd.uniform(-30, -10))
    puff("kim_lua", p1[0], p1[1] + 10, t0 + fly_k + 0.2, 0.32, 70, 10)

# 5. lốc xoáy lửa: lấy thẳng từ file mẫu đã mua (Updated and Simplified Tornado), đổi màu rực cháy (vfx_blender/loc_tu_mau.py);
#    mọc từ đất lên bằng phóng to xương ở chân, khói bốc từ miệng phễu
bone("b_loc", *DAT, s=0.8)
slot("s_loc", "b_loc", "loc_bl")
DLOC = MAN["loc_bl"]["count"] * DT
ops.append(f"anim.add loc_lua dur={DLOC + 1.1:.3f}")
show("loc_lua", "s_loc", "loc_bl", 0, "once", DLOC)
ops.append("key loc_lua b_loc.scale 0:0.55,0.08:backOut 0.28:1,1")
for i, t in enumerate([0.3, 0.5, 0.7, 0.9, 1.1, 1.3]):
    puff("loc_lua", DAT[0] + rnd.uniform(-60, 60), DAT[1] + 240 + rnd.uniform(-10, 15), t, rnd.uniform(0.45, 0.65),
         rnd.uniform(100, 140), rnd.uniform(-30, 30))

# 6. lửa cháy (lặp, khói đỉnh quấn vòng)
bone("b_lua", *DAT, s=0.55)
slot("s_lua", "b_lua", "lua_bl")
DL = 2 * MAN["lua_bl"]["count"] * DT
ops.append(f"anim.add lua_chay dur={DL:.3f} loop=true")
show("lua_chay", "s_lua", "lua_bl", 0, "loop")
for i in range(4):
    puff("lua_chay", DAT[0] + (-10, 8, -3, 12)[i], DAT[1] + 120, i * DL / 4, 0.17, 95, (10, -8, 14, -5)[i], dur=DL)   # nhỏ, bốc từ ngọn vệt trắng (lửa cháy theo bài Blender Box)

# 7. thiên thạch (khói đuôi dày) → nổ lớn
start = (DAT[0] - 330, DAT[1] + 560)
end = (DAT[0], DAT[1] + 30)
bone("b_tt", *start, s=0.62)
bone("b_ntt", DAT[0], DAT[1] + 40, s=1.15)
slot("s_tt", "b_tt", "cau_bl")
slot("s_ntt", "b_ntt", "no_bl")
fall = 0.6
ops.append(f"anim.add thien_thach dur={fall + DN + 0.8:.3f}")
show("thien_thach", "s_tt", "cau_bl", 0, "loop", fall)
fly_keys("thien_thach", "b_tt", start, end, fall)
show("thien_thach", "s_ntt", "no_bl", fall, "once", fall + DN)
ops.append(f"vfx.shake thien_thach bone=root t={fall:.3f} dur=0.45 amp=9 freq=26 seed=5")
fire_trail("thien_thach", start, end, fall, 0.8, step=18)
boom_smoke("thien_thach", DAT[0], DAT[1] + 40, fall + 0.25, 1.05, n=6)

path = os.path.join(PROJ, "dung.ops")
open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
r = subprocess.run(ATOM + ["do", "-p", PROJ, "-f", path], capture_output=True, text=True, encoding="utf-8")
print((r.stdout + r.stderr)[-1500:])
sys.exit(r.returncode)
