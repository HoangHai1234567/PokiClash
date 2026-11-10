"""Phân tích cấu trúc rig từ info.json (mo_xe.html mode=info): cây xương, chuỗi của từng mảnh, quan hệ sóng - đầu, thống kê clip."""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "info.json", encoding="utf-8"))
B, S = d["bones"], d["slots"]
A = {a["slot"]: a for a in d["skins"][0]["atts"]}
kids = collections.defaultdict(list)
for b in B:
    kids[b["parent"]].append(b["i"])
nm = lambda i: B[i]["name"]


def anc(i):
    out = []
    while i >= 0:
        out.append(i)
        i = B[i]["parent"]
    return out[::-1]


def subtree(i):
    out, st = [], [i]
    while st:
        j = st.pop()
        out.append(j)
        st += kids[j]
    return out


part = lambda s: sys.argv[2] if len(sys.argv) > 2 else "all"
P = part(0)

if P in ("all", "tree"):
    print("== CÂY XƯƠNG (chuỗi một con gộp thành a>b>c; [n] = số xương trong nhánh)")

    def show(i, ind):
        chain = [i]
        while len(kids[chain[-1]]) == 1:
            chain.append(kids[chain[-1]][0])
        last = chain[-1]
        txt = ">".join(nm(j) for j in chain)
        b = B[i]
        print("  " * ind + f"{txt}  (len {b['len']:.0f}, x {b['x']:.0f}, y {b['y']:.0f}, rot {b['rot']:.0f}" + (f", inherit {b['inherit']}" if b["inherit"] else "") + f") [{len(subtree(i))}]")
        for k in kids[last]:
            show(k, ind + 1)
    show(0, 0)

if P in ("all", "heads"):
    print("\n== BẢY ĐẦU: xương của từng mảnh (theo slot)")
    for k in range(1, 8):
        print(f"-- đầu {k:02d}")
        for s in S:
            if not s["name"].endswith(f"_{k:02d}") and s["name"] not in (f"yp_{k - 1}",):
                continue
            a = A.get(s["i"])
            if not a or "bones" not in a:
                continue
            bs = a["bones"]
            print(f"   {s['name']:12s} v{a['verts']:3d} {a.get('rw')}x{a.get('rh')}: " + ", ".join(nm(j) for j in bs))
        # chuỗi cổ: tổ tiên của xương sâu nhất trong shenti
        sh = next((A[s["i"]] for s in S if s["name"] == f"shenti_{k:02d}"), None)
        if sh:
            deep = max(sh["bones"], key=lambda j: len(anc(j)))
            print("   tổ tiên của đốt cổ sâu nhất:", " > ".join(nm(j) for j in anc(deep)))
            hd = next((A[s["i"]] for s in S if s["name"] in (f"shagne_{k:02d}", f"shange_{k:02d}")), None)
            if hd:
                print("   tổ tiên của xương đầu:", " > ".join(nm(j) for j in anc(max(hd["bones"], key=lambda j: len(anc(j))))))

if P in ("all", "waves"):
    print("\n== SÓNG (slot l_*, langhua_*, sd_*): tổ tiên có đi qua xương cổ/đầu không")
    head_bones = set()
    for s in S:
        if s["name"].split("_")[0] in ("shenti", "shagne", "shange", "tou", "xiae", "shetou", "jiao", "kouqiang", "liaoya") and s["i"] in A and "bones" in A[s["i"]]:
            head_bones |= set(A[s["i"]]["bones"])
    rows = collections.Counter()
    for s in S:
        if not (s["name"].startswith("l_") or s["name"].startswith("langhua") or s["name"].startswith("sd_")):
            continue
        a = A.get(s["i"])
        bs = a["bones"]
        top = set()
        via = False
        for j in bs:
            an = anc(j)
            top.add(nm(an[1]) + (">" + nm(an[2]) if len(an) > 2 else ""))
            if any(x in head_bones for x in an[:-1]) or j in head_bones:
                via = True
        rows[(tuple(sorted(top)), via)] += 1
        if via:
            print("   CÓ QUA CỔ/ĐẦU:", s["name"], a["name"], [nm(j) for j in bs])
    for (top, via), n in rows.items():
        print(f"   {n:3d} slot sóng, gốc {top}, qua cổ/đầu: {via}")
    print("   ví dụ chuỗi sóng:")
    for name in ("l_51", "l_45", "l_19", "l_6", "langhua_14", "l_27", "sd_1"):
        s = next(x for x in S if x["name"] == name)
        a = A[s["i"]]
        print(f"   {name} ({a['name']} {a.get('rw')}x{a.get('rh')}, v{a['verts']}):")
        for j in a["bones"]:
            b = B[j]
            print(f"       {' > '.join(nm(x) for x in anc(j)[1:])}  len {b['len']:.0f}")

if P in ("all", "clip"):
    print("\n== MẶT NẠ CẮT và ràng buộc")
    s0 = S[0]
    print("   slot", s0["name"], "trên xương", nm(s0["bone"]), "tổ tiên", [nm(j) for j in anc(s0["bone"])], A[0])
    for c in d["transform"]:
        print("  ", c["name"], "xương", [nm(j) for j in c["bones"]], "theo", nm(c["target"]), {k: v for k, v in c.items() if k.startswith("mix") or k.startswith("off")})
    for j in (484, 485, 139):
        print("   ", nm(j), "tổ tiên:", " > ".join(nm(x) for x in anc(j)), "con:", [nm(x) for x in kids[j]])

if P in ("all", "anim"):
    print("\n== ANIMATION")
    for a in d["anims"]:
        c = collections.Counter(t["type"].lstrip("_") for t in a["tls"])
        keys = sum(t["frames"] for t in a["tls"])
        bones = {t["boneIndex"] for t in a["tls"] if "boneIndex" in t}
        slots = {t["slotIndex"] for t in a["tls"] if "slotIndex" in t}
        print(f"-- {a['name']} {a['dur']} s: {len(a['tls'])} timeline, {keys} khoá, {len(bones)} xương, {len(slots)} slot")
        print("   ", dict(c))
        for t in a["tls"]:
            ty = t["type"].lstrip("_")
            if ty == "AttachmentTimeline":
                print(f"    đổi hình slot {S[t['slotIndex']]['name']}: {t['frames']} khoá {t.get('names')}")
            if ty == "DrawOrderTimeline":
                print(f"    đổi thứ tự vẽ: {t['frames']} khoá")
            if ty == "EventTimeline":
                print("    event", t.get("ev"))
            if "Constraint" in ty:
                print(f"    {ty} {t['frames']} khoá")
        # xương gốc nào được khoá, biên độ
        for t in a["tls"]:
            if "boneIndex" in t and B[t["boneIndex"]]["parent"] in (-1, 0) or ("boneIndex" in t and nm(t["boneIndex"]) in ("bone129", "bone2", "bone")):
                print(f"    gốc {nm(t['boneIndex'])} {t['type'].lstrip('_')} {t['frames']} khoá {t.get('min', '')} {t.get('max', '')} {t.get('rng', '')}")
