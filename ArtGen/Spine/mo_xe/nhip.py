"""Đọc NHỊP của một clip từ khoá thật (chay.py info + chay.py keys): người làm animation đặt dáng ở khung nào, từng đốt của một
chuỗi xương được khoá lệch nhau ra sao, dùng đường cong gì.

    nhip.py <info.json> <keys.json> <clip> [--root <xương>] [--chain a,b,c ...] [--fps 30] [--bone <xương> ...]

  --root   chỉ tính các xương trong cây con của xương này (vd nhóm thân, bỏ nhóm nước)
  --chain  in bảng khoá xoay của từng đốt trong chuỗi (hàng = khung có khoá, cột = đốt): thấy ngay khoá cùng khung (dáng → dáng)
           hay khoá lệch khung (chồng trễ), biên độ lớn dần hay nhỏ dần ra ngọn
  --bone   in mọi khoá (xoay, dời, co giãn) của một xương"""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
a = sys.argv[1:]
info = json.load(open(a[0], encoding="utf-8"))
K = json.load(open(a[1], encoding="utf-8"))[a[2]]
opt = collections.defaultdict(list)
i = 3
while i < len(a):
    opt[a[i]].append(a[i + 1])
    i += 2
FPS = float(opt["--fps"][0]) if opt["--fps"] else 30.0
B = info["bones"]
bi = {b["name"]: b["i"] for b in B}
kids = collections.defaultdict(list)
for b in B:
    kids[b["parent"]].append(b["i"])


def subtree(r):
    out, st = set(), [r]
    while st:
        j = st.pop()
        out.add(j)
        st += kids[j]
    return out


scope = subtree(bi[opt["--root"][0]]) if opt["--root"] else set(range(len(B)))
fr = lambda t: int(round(t * FPS))
D = K["dur"]
print(f"== {a[2]}: {D:.2f} s = {fr(D)} khung; {len(K['tls'])} timeline")

# 1. nhịp: khung nào có nhiều xương được khoá
hist = collections.Counter()
ctype = collections.Counter()
per_bone = collections.Counter()
nkeys = 0
for t in K["tls"]:
    if "boneIndex" not in t or t["boneIndex"] not in scope:
        continue
    n = t["n"]
    times = t["f"][::n]
    per_bone[t["boneIndex"]] += len(times)
    nkeys += len(times)
    for x in times:
        hist[fr(x)] += 1
    for c in t.get("c", [])[:-1]:
        ctype[c] += 1
tot = sum(ctype.values()) or 1
print(f"khoá xương trong phạm vi: {nkeys}; đường cong: thẳng {ctype[0] * 100 // tot}%, bậc {ctype[1] * 100 // tot}%, bezier {ctype[2] * 100 // tot}%")
mx = max(hist.values())
print("NHỊP (khung: số timeline có khoá; ▇ theo tỉ lệ). Khung nổi bật = dáng chính:")
for f in sorted(hist):
    if hist[f] >= mx * 0.12:
        print(f"  khung {f:3d} ({f / FPS:5.2f} s) {hist[f]:4d} {'▇' * max(1, hist[f] * 40 // mx)}")
print("xương nhiều khoá nhất:", ", ".join(f"{B[b]['name']}×{c}" for b, c in per_bone.most_common(12)))


def tl_of(bone, typ):
    for t in K["tls"]:
        if t.get("boneIndex") == bone and t["type"] == typ:
            return t
    return None


# 2. chuỗi: bảng khoá xoay từng đốt
for ch in opt["--chain"]:
    names = ch.split(",")
    tls = [tl_of(bi[n], "RotateTimeline") for n in names]
    frames = sorted({fr(x) for t in tls if t for x in t["f"][::2]})
    print(f"\nCHUỖI {ch}: khoá xoay (độ, so với dáng gốc); * = bezier, ^ = bậc; trống = đốt đó không có khoá ở khung này")
    print("  khung   s   " + "".join(f"{n[-8:]:>10}" for n in names))
    for f in frames:
        row = f"  {f:4d} {f / FPS:5.2f} "
        for t in tls:
            cell = ""
            if t:
                for k, x in enumerate(t["f"][::2]):
                    if fr(x) == f:
                        c = t.get("c", [0] * 999)[k] if k < len(t.get("c", [])) else 0
                        cell = f"{t['f'][k * 2 + 1]:.1f}" + ("*" if c == 2 else "^" if c == 1 else "")
            row += f"{cell:>10}"
        print(row)
    amp = []
    for t in tls:
        v = t["f"][1::2] if t else [0]
        amp.append(max(v) - min(v))
    print("  biên độ " + "     " + "".join(f"{x:10.1f}" for x in amp))
    print("  số khoá " + "     " + "".join(f"{(len(t['f']) // 2 if t else 0):10d}" for t in tls))

for bn in opt["--bone"]:
    print(f"\nXƯƠNG {bn}:")
    for t in K["tls"]:
        if t.get("boneIndex") == bi[bn]:
            n = t["n"]
            ks = [(fr(t["f"][k]), *t["f"][k + 1:k + n]) for k in range(0, len(t["f"]), n)]
            print(f"  {t['type']}: " + "  ".join(f"[{k[0]}] " + ",".join(f"{v:.1f}" for v in k[1:]) for k in ks))
