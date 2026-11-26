# Clip của cậu thám hiểm câu cá (GD_Claude/32 mục 2), viết bằng ops AtomSpine.
# Bản 3 (người dùng 2026-11-26: "tay không cần cử động... gen 2 tay bình thường", "không cần animation phần tay"): tay vẽ
# liền dáng cầm cần, gắn cứng vào ngực. Bản 2 ("tay lỗi nhiều, không cần show tay cầm cần"): hai tay cầm cần ở phía trước người nên khuất sau áo
# choàng; cánh tay khép vào, chỉ lộ tay áo ở vai; cần câu gắn điểm cầm `cam` trước ngực. Mỗi khoá dáng khai bằng tham số:
#   cam = vị trí điểm cầm (world, px nửa cỡ; đặt sao cho cán bần, guồng luôn khuất sau đầu / áo choàng), can = góc cần (độ, 0 = sang phải, 90 = dựng đứng),
#   cong = độ cong ngọn cần (âm: ngọn rủ theo chiều kim đồng hồ), nghieng = xoay lưng, hong = dời hông (dx, dy), dau = xoay đầu,
#   nang = nâng khuỷu (độ, cần giơ cao thì vai nhô), chan_t / chan_p = dời đích IK chân.
# Script đổi ra khoá cục bộ (dời + xoay `cam` trong hệ ngực), lò xo cho áo choàng, chỏm tóc. Luật: animation-humanoid, animation-petclash.
# Chạy: py -3 -I hoat_anh.py (sau dung_rig.py). Ra atom/ops/02_clip.ops, chạy atom do, tờ khung soát vào atom/.atomspine/.
import os, sys, math

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dung_rig as R  # noqa: E402
from atom_cli import CLI, run  # noqa: E402

PROJ = R.PROJ


def setup_bones():
    B = {}

    def add(name, parent, pos, rot):
        B[name] = {"parent": parent, "wpos": pos, "wrot": rot}

    def seg(name, parent, a, b):
        x, y, r, l = R.seg(a, b)
        add(name, parent, (x, y), r)

    add("move", None, (0.0, 0.0), 0.0)
    seg("hip", "move", "hip", "bung")
    seg("bung", "hip", "bung", "nguc")
    seg("nguc", "bung", "nguc", "co")
    add("cam", "nguc", R.W("cam"), 90.0)
    for n, b in B.items():
        p = b["parent"]
        if p is None:
            b["lpos"], b["lrot"] = b["wpos"], b["wrot"]
            continue
        pp, pr = B[p]["wpos"], B[p]["wrot"]
        dx, dy = b["wpos"][0] - pp[0], b["wpos"][1] - pp[1]
        c, s_ = math.cos(math.radians(-pr)), math.sin(math.radians(-pr))
        b["lpos"] = (dx * c - dy * s_, dx * s_ + dy * c)
        b["lrot"] = b["wrot"] - pr
    return B


BONES = setup_bones()


def fk(deltas, trans):
    W = {}
    for n, b in BONES.items():
        lp = b["lpos"]
        t = trans.get(n, (0, 0))
        lp = (lp[0] + t[0], lp[1] + t[1])
        lr = b["lrot"] + deltas.get(n, 0.0)
        if b["parent"] is None:
            W[n] = (lp, lr)
            continue
        (px, py), pr = W[b["parent"]]
        c, s_ = math.cos(math.radians(pr)), math.sin(math.radians(pr))
        W[n] = ((px + lp[0] * c - lp[1] * s_, py + lp[0] * s_ + lp[1] * c), pr + lr)
    return W


def ang(a):
    while a > 180:
        a -= 360
    while a < -180:
        a += 360
    return a


# tay: không có xương, không animation (người dùng 2026-11-26 "không cần animation phần tay"); tham số `nang` cũ bỏ qua


def pose(p):
    deltas, trans = {}, {}
    hx, hy = p.get("hong", (0, 0))
    trans["hip"] = (hx, hy)
    lean = p.get("nghieng", 0.0)
    deltas["bung"] = lean * 0.45
    deltas["nguc"] = lean * 0.55
    deltas["co"] = -lean * 0.3 + p.get("dau", 0.0) * 0.35
    deltas["dau"] = p.get("dau", 0.0) * 0.65
    W = fk(deltas, trans)
    (nx, ny), nr = W["nguc"]
    px, py = p.get("cam", R.W("cam"))
    c, s_ = math.cos(math.radians(-nr)), math.sin(math.radians(-nr))
    lx, ly = (px - nx) * c - (py - ny) * s_, (px - nx) * s_ + (py - ny) * c
    cl = BONES["cam"]["lpos"]
    trans["cam"] = (lx - cl[0], ly - cl[1])
    deltas["cam"] = ang(p["can"] - nr - BONES["cam"]["lrot"])
    return deltas, trans


CAM = {"cam": (36, 330), "can": 64, "cong": -4}
CHO = {"cam": (36, 326), "can": 52, "cong": -5}
NGAM = {"cam": (6, 432), "can": 120, "cong": -8, "nghieng": 5, "hong": (-3, 2), "dau": 3, "nang": 25}
KEO = {"cam": (30, 334), "can": 82, "cong": -24, "nghieng": 6, "hong": (-4, 1), "nang": 12, "chan_t": (-8, 0), "chan_p": (8, 0)}
GIO = {"cam": (14, 445), "can": 104, "cong": -4, "nghieng": -3, "hong": (0, 1), "dau": 6, "nang": 28}  # giơ cần khoe cá

CLIPS = {
    # tên: (dài, lặp, [(t, dáng, curve)], sự kiện)
    "idle": (2.4, True, [
        (0.0, dict(CAM), "ease"),
        (1.2, dict(CAM, can=65.5, cong=-6.5, hong=(0, -3), nghieng=-1, dau=-1.5, cam=(36, 327)), "ease"),
        (2.4, dict(CAM), "ease"),
    ], []),
    "ngam": (0.8, True, [
        (0.0, dict(NGAM), "ease"),
        (0.4, dict(NGAM, can=122, cong=-9.5, hong=(-3, 1)), "ease"),
        (0.8, dict(NGAM), "ease"),
    ], []),
    "quang": (0.6, False, [
        (0.0, dict(NGAM), "easeOut"),
        (0.09, dict(NGAM, cam=(8, 442), can=130, cong=-12, nghieng=7, hong=(-5, 3), nang=30), "snap"),
        (0.22, {"cam": (52, 350), "can": 36, "cong": 14, "nghieng": -9, "hong": (7, -2), "dau": -3, "nang": 10}, "easeOut"),
        (0.32, {"cam": (50, 342), "can": 28, "cong": -12, "nghieng": -7, "hong": (6, -3), "dau": -2, "nang": 6}, "ease"),
        (0.6, dict(CHO), "ease"),
    ], [(0.22, "tha")]),
    "cho": (3.0, True, [
        (0.0, dict(CHO), "ease"),
        (0.9, dict(CHO, can=53.5, cong=-6.5, hong=(2, -2), dau=2), "ease"),
        (1.6, dict(CHO, dau=-5, hong=(3, -1)), "ease"),
        (2.2, dict(CHO, dau=-4, can=51, hong=(1, -2)), "ease"),
        (3.0, dict(CHO), "ease"),
    ], []),
    "giat": (0.45, False, [
        (0.0, dict(CHO), "easeIn"),
        (0.06, dict(CHO, can=46, cong=-9, cam=(36, 320)), "snap"),
        (0.15, {"cam": (24, 400), "can": 100, "cong": -20, "nghieng": 8, "hong": (-5, 3), "dau": 4, "nang": 20}, "easeOut"),
        (0.45, dict(KEO), "ease"),
    ], [(0.15, "giat")]),
    "keo": (0.9, True, [
        (0.0, dict(KEO), "ease"),
        (0.22, dict(KEO, can=86, cong=-30, hong=(-6, 2), cam=(31, 338)), "ease"),
        (0.45, dict(KEO, can=79, cong=-20, hong=(-3, 0)), "ease"),
        (0.68, dict(KEO, can=84, cong=-28, hong=(-5, 2), cam=(30, 337)), "ease"),
        (0.9, dict(KEO), "ease"),
    ], []),
    "nhip": (0.32, False, [  # mỗi lần chạm trúng vùng vàng: giật cần lên một nhịp rồi về dáng kéo
        (0.0, dict(KEO), "snap"),
        (0.07, dict(KEO, can=97, cong=-12, cam=(30, 354), nghieng=8, hong=(-6, 3), nang=20), "easeOut"),
        (0.32, dict(KEO), "ease"),
    ], []),
    "trung": (1.6, False, [  # giơ cần, quay mặt lại cười, nhảy cẫng một cái
        (0.0, dict(KEO), "easeIn"),
        (0.12, dict(GIO, cong=-8, nghieng=4, hong=(-2, 4), dau=0), "easeOut"),
        (0.3, dict(GIO), "ease"),
        (0.45, dict(GIO, hong=(0, 20), cam=(14, 457), chan_t=(0, 15), chan_p=(0, 15)), "easeIn"),
        (0.6, dict(GIO, hong=(0, -6), can=101, cong=-8, nang=24), "easeOut"),
        (0.85, dict(GIO, dau=7), "ease"),
        (1.2, dict(GIO, dau=5, can=105), "ease"),
        (1.6, dict(GIO, dau=6), "ease"),
    ], [(0.12, "ca_len")]),
    "hut": (1.3, False, [
        (0.0, dict(KEO), "snap"),
        (0.1, {"cam": (44, 345), "can": 70, "cong": 2, "nghieng": 10, "hong": (-7, 2), "dau": 3, "nang": 10}, "easeOut"),
        (0.45, {"cam": (34, 318), "can": 26, "cong": -6, "nghieng": -8, "hong": (0, -6), "dau": -9, "nang": -6}, "ease"),
        (0.9, {"cam": (34, 316), "can": 24, "cong": -6, "nghieng": -9, "hong": (0, -7), "dau": -10, "nang": -6}, "ease"),
        (1.3, {"cam": (34, 318), "can": 25, "cong": -6, "nghieng": -8, "hong": (0, -6), "dau": -9, "nang": -6}, "ease"),
    ], []),
}

ROT = ["bung", "nguc", "co", "dau", "cam"]


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".") if abs(v) >= 0.005 else "0"


def clip_ops(name, dur, loop, keys, events):
    ops = [f"anim.add {name} dur={dur} loop={'true' if loop else 'false'}"]
    rot = {b: [] for b in ROT + ["can2", "can3", "can4"]}
    tr = {b: [] for b in ("hip", "cam", "ik_chan_t", "ik_chan_p")}
    for t, p, cv in keys:
        d, trans = pose(p)
        for b in ROT:
            rot[b].append((t, d.get(b, 0.0), cv))
        bend = p.get("cong", 0.0)
        for i, b in enumerate(("can2", "can3", "can4")):
            rot[b].append((t, bend * (0.25, 0.33, 0.42)[i], cv))
        tr["hip"].append((t, trans["hip"], cv))
        tr["cam"].append((t, trans["cam"], cv))
        tr["ik_chan_t"].append((t, p.get("chan_t", (0, 0)), cv))
        tr["ik_chan_p"].append((t, p.get("chan_p", (0, 0)), cv))
    for b, ks in rot.items():
        ops.append(f"key {name} {b}.rotate " + " ".join(f"{t}:{fmt(v)}:{c}" for t, v, c in ks))
    for b, ks in tr.items():
        ops.append(f"key {name} {b}.translate " + " ".join(f"{t}:{fmt(v[0])},{fmt(v[1])}:{c}" for t, v, c in ks))
    for t, ev in events:
        ops.append(f"event {name} {t} {ev}")
    return ops


def main():
    ops = [f"event.add {ev}" for ev in ("tha", "giat", "ca_len")]
    for name, (dur, loop, keys, events) in CLIPS.items():
        ops += clip_ops(name, dur, loop, keys, events)
        if name in ("idle", "cho", "ngam"):
            ops.append(f"anim.wave {name} bones=ao1,ao2,ao3 amp=1.2 lag=0.15 growth=1.3")
            ops.append(f"anim.wave {name} bones=aot1,aot2 amp=1.5 lag=0.18 growth=1.3 phase=0.2")
            ops.append(f"anim.wave {name} bones=aop1,aop2 amp=1.5 lag=0.18 growth=1.3 phase=0.5")
            ops.append(f"anim.wave {name} bones=chom amp=3 lag=0.1")
        else:
            ops.append(f"anim.spring {name} bones=ao1,ao2,ao3 stiffness=0.22 damping=0.55")
            ops.append(f"anim.spring {name} bones=aot1,aot2 stiffness=0.2 damping=0.5")
            ops.append(f"anim.spring {name} bones=aop1,aop2 stiffness=0.2 damping=0.5")
            ops.append(f"anim.spring {name} bones=chom stiffness=0.3 damping=0.45")
        if loop:
            ops.append(f"anim.loopfix {name}")
    ops.append("key trung dau.attachment 0:dau 0.24:dau_quay__dau")
    path = os.path.join(PROJ, "ops", "02_clip.ops")
    open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
    print(run(CLI + ["-p", PROJ, "do", "-f", path]))
    print(run(CLI + ["-p", PROJ, "lint"], check=False))


if __name__ == "__main__":
    main()
