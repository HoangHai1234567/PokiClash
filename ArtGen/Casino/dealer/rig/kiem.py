# Kiểm clip đã xuất của Lão Mực (đọc ../atom/export/lao_muc.atomik): (1) bước nhảy góc lớn giữa hai khoá kề (dấu hiệu quay 360 độ
# sai), (2) khung cuối mỗi clip một lần có trùng khung đầu idle không, (3) khung đầu / cuối của clip lặp.
# Chạy: py -3 -I kiem.py
import gzip, json, os, struct, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
b = open(os.path.join(HERE, "..", "atom", "export", "lao_muc.atomik"), "rb").read()
d = gzip.decompress(b[6:])
jl = struct.unpack("<I", d[:4])[0]
j = json.loads(d[4:4 + jl])
bones = [x["name"] for x in j["bones"]]
STRIDE = {0: 7, 1: 12, 2: 12}


def sample(tl, t):
    st = STRIDE[tl["type"]]
    k = tl["keys"]
    n = len(k) // st
    dim = 1 if tl["type"] == 0 else 2
    if t <= k[0]:
        return k[1:1 + dim]
    for i in range(n - 1):
        t0, t1 = k[i * st], k[(i + 1) * st]
        if t <= t1:
            f = (t - t0) / max(t1 - t0, 1e-9)
            return [k[i * st + 1 + c] + (k[(i + 1) * st + 1 + c] - k[i * st + 1 + c]) * f for c in range(dim)]
    return k[(n - 1) * st + 1:(n - 1) * st + 1 + dim]


def pose(a, t):
    out = {}
    for tl in a["tls"]:
        out[(bones[tl["bone"]], tl["type"])] = sample(tl, t)
    return out


anims = {a["name"]: a for a in j["anims"]}
idle0 = pose(anims["idle"], 0.0)
print("phiên bản", j["version"], "| xương", len(j["bones"]), "| clip", len(j["anims"]))
for name, a in anims.items():
    worst = (0, "")
    for tl in a["tls"]:
        if tl["type"] != 0:
            continue
        k = tl["keys"]
        for i in range(0, len(k) - 7, 7):
            dv = abs(k[i + 8] - k[i + 1])
            dt = max(k[i + 7] - k[i], 1e-6)
            per_frame = dv / (dt * 30)
            if per_frame > worst[0]:
                worst = (per_frame, f"{bones[tl['bone']]} t={k[i]:.2f}")
    end = pose(a, a["dur"])
    start = pose(a, 0.0)
    ref = start if name in ("idle", "talk") else idle0
    diff = 0.0
    who = ""
    for key in set(end) | set(ref):
        dflt = [1.0, 1.0] if key[1] == 2 else [0.0, 0.0]
        e, r = end.get(key, dflt), ref.get(key, dflt)
        m = max(abs((x - y + 180.0) % 360.0 - 180.0) if key[1] == 0 else abs(x - y) for x, y in zip(e, r))   # góc: so theo vòng
        if m > diff:
            diff, who = m, key[0]
    print(f"{name:16s} dur {a['dur']:.1f}  góc nhảy lớn nhất {worst[0]:6.1f} độ/khung ({worst[1]})  lệch cuối so với "
          f"{'đầu chính nó' if name in ('idle', 'talk') else 'idle giây 0'}: {diff:.2f} ({who})  sự kiện {[(round(e['t'], 2), e['name']) for e in a.get('ev', [])]}")
