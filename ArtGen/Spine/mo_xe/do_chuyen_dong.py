"""Đo chuyển động từ mau_<clip>.json (mo_xe.html mode=sample) + info.json."""
import json
import math
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
I = json.load(open("info.json", encoding="utf-8"))
B, S = I["bones"], I["slots"]
bi = {b["name"]: b["i"] for b in B}
si = {s["name"]: s["i"] for s in S}
HEADS = {1: "bone9", 2: "bone40", 3: "bone57", 4: "bone89", 5: "bone74", 6: "bone104", 7: "bone120"}
NECK = {1: ["bone3", "bone4", "bone5", "bone6", "bone7", "bone8", "bone9"], 2: ["bone27", "bone35", "bone36", "bone37", "bone38", "bone39", "bone40"],
        3: ["bone51", "bone52", "bone53", "bone54", "bone55", "bone56", "bone57"], 4: ["bone83", "bone84", "bone85", "bone86", "bone87", "bone88", "bone89"],
        5: ["bone68", "bone69", "bone70", "bone71", "bone72", "bone73", "bone74"], 6: ["bone98", "bone99", "bone100", "bone101", "bone102", "bone103", "bone104"],
        7: ["bone114", "bone115", "bone116", "bone117", "bone118", "bone119", "bone120"]}
JAW = {1: "bone10", 2: "bone41", 3: "bone58", 4: "bone90", 5: "bone75", 6: "bone105", 7: "bone121"}


def load(clip):
    d = json.load(open(f"mau_{clip}.json"))
    b = np.array([f["b"] for f in d["frames"]], float)  # (khung, xương, 5)
    a = np.array([f["a"] for f in d["frames"]], float)
    s = np.array([f["s"] for f in d["frames"]], float)
    return d["dur"], d["fps"], b, a, s


def ang(a):
    return (a + 180) % 360 - 180


def rel_rot(b, child, parent):
    return ang(b[:, bi[child], 2] - b[:, bi[parent], 2])


clip = sys.argv[1]
dur, fps, b, a, s = load(clip)
n = len(b)
print(f"== {clip}: {dur:.2f} s, {n} khung")
m = b[:, bi["bone"], :]
w = b[:, bi["bone129"], :]
print(f"xương chủ của thân 'bone': x {m[:,0].min():.0f}..{m[:,0].max():.0f}, y {m[:,1].min():.0f}..{m[:,1].max():.0f}, tỉ lệ x {m[:,3].min():.2f}..{m[:,3].max():.2f} y {m[:,4].min():.2f}..{m[:,4].max():.2f}")
print(f"xương chủ của nước 'bone129': x {w[:,0].min():.0f}..{w[:,0].max():.0f}, y {w[:,1].min():.0f}..{w[:,1].max():.0f}, tỉ lệ x {w[:,3].min():.2f}..{w[:,3].max():.2f} y {w[:,4].min():.2f}..{w[:,4].max():.2f}")
print("ĐẦU: biên độ đầu (đơn vị rig; cả con cao ~1650), lúc cao nhất, tốc độ lớn nhất và lúc đạt, hàm há tối đa và lúc há")
for k, hb in HEADS.items():
    p = b[:, bi[hb], :2]
    v = np.hypot(*np.diff(p, axis=0).T) * fps
    jaw = rel_rot(b, JAW[k], hb)
    jaw0 = jaw - jaw[0] if clip.startswith("idle") else jaw - np.median(jaw)
    root = b[:, bi[NECK[k][0]], :2]
    rootmv = np.hypot(*(root - root[0]).T).max()
    print(f"  đầu {k}: x {p[:,0].min():6.0f}..{p[:,0].max():6.0f} (Δ{np.ptp(p[:,0]):4.0f})  y {p[:,1].min():6.0f}..{p[:,1].max():6.0f} (Δ{np.ptp(p[:,1]):4.0f})  "
          f"vmax {v.max():5.0f}/s lúc {v.argmax()/fps:.2f}s  hàm {jaw.min():5.0f}..{jaw.max():4.0f}° (đỉnh lệch lúc {np.abs(jaw0).argmax()/fps:.2f}s)  gốc cổ dời {rootmv:.0f}")
# uốn cổ: biên độ góc tương đối từng đốt (đầu chuỗi -> ngọn)
print("CỔ: biên độ góc (độ) của từng đốt so với đốt cha, gốc -> ngọn")
for k, ch in NECK.items():
    amps = []
    for i in range(1, len(ch)):
        r = rel_rot(b, ch[i], ch[i - 1])
        amps.append(np.ptp(np.unwrap(np.radians(r)) * 180 / math.pi))
    r0 = b[:, bi[ch[0]], 2]
    amps0 = np.ptp(np.unwrap(np.radians(r0)) * 180 / math.pi)
    print(f"  đầu {k}: gốc {amps0:4.0f} | " + " ".join(f"{x:4.0f}" for x in amps))
# trễ pha dọc cổ đầu 1 trong idle: thời điểm cực đại của góc từng đốt
if clip.startswith("idle"):
    print("TRỄ PHA dọc cổ (lúc góc tương đối đạt cực đại, giây):")
    for k in (1, 2, 4):
        ch = NECK[k]
        ts = [rel_rot(b, ch[i], ch[i - 1]).argmax() / fps for i in range(1, len(ch))]
        print(f"  đầu {k}: " + " ".join(f"{t:.2f}" for t in ts))
    # chu kỳ: tự tương quan của y đầu
    for k in (1, 2, 4, 6):
        y = b[:-1, bi[HEADS[k]], 1]
        y = y - y.mean()
        ac = [float((y * np.roll(y, sh)).sum()) for sh in range(1, len(y))]
        best = int(np.argmax(ac[10:])) + 11
        print(f"  đầu {k}: chu kỳ lặp ước {best / fps:.2f} s; y cực đại lúc {y.argmax()/fps:.2f} s")
# SÓNG
print("SÓNG: alpha và vị trí của vài cặp slot dùng chung ảnh")
for pair in (("l_51", "l_52"), ("l_14", "l_24"), ("l_45", "l_83"), ("l_19", "l_62"), ("l_6", "l_73"), ("l_27", "l_69"), ("langhua_14", "langhua_15"), ("l_37", "l_38")):
    row = []
    for nm in pair:
        j = si[nm]
        al = a[:, j]
        bone = S[j]["bone"]
        p = b[:, bone, :2]
        vis = al > 0.02
        on = np.flatnonzero(np.diff(vis.astype(int)) == 1)
        off = np.flatnonzero(np.diff(vis.astype(int)) == -1)
        row.append(f"{nm}: alpha {al.min():.2f}..{al.max():.2f} hiện lúc {[round(x / fps, 2) for x in on[:4]]} tắt lúc {[round(x / fps, 2) for x in off[:4]]} "
                   f"Δx {np.ptp(p[:,0]):.0f} Δy {np.ptp(p[:,1]):.0f} tỉ lệ {b[:,bone,3].min():.2f}..{b[:,bone,3].max():.2f}")
    print("  " + " | ".join(row))
# giọt nước
for nm in ("sd_1", "sd_3", "sd_6"):
    j = si[nm]
    bone = S[j]["bone"]
    p = b[:, bone, :2]
    print(f"  giọt {nm}: alpha {a[:, j].min():.2f}..{a[:, j].max():.2f}, x {p[:,0].min():.0f}..{p[:,0].max():.0f}, y {p[:,1].min():.0f}..{p[:,1].max():.0f}")
# số slot đang hiện theo thời gian (clip xuất hiện / chết)
vis = ((a > 0.02) & (s > 0)).sum(axis=1)
print("số slot hiện theo thời gian (mỗi 0,25 s):", [int(vis[min(n - 1, int(t * fps))]) for t in np.arange(0, dur + 0.01, 0.25)])
