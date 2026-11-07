"""Animation tướng đảo Mộc (2026-11-07): khuôn có tham số, ghi <aola>/reskin/moc_<id>/anim_moi.json cho anim_moi.py của máy ổ E
(cây khớp khai theo tên mảnh sau ghép: N01_8...). Chạy SAU ghep_nhom.py (cần export/anim.json đã ghép), rồi chạy anim_moi.py.

Dữ liệu mỗi dạng: mục "anim" trong ArtGen/Heroes/forms_moc/<mã>.json (từ tools/moc_spec): root (thân), head, swing (vung khi
đánh), wob (đung đưa lúc đứng), fly (bay rời), cast (mảnh, fx, fy), parent {mảnh: cha}, ult ("spin" | "slam", mặc định: có
swing thì slam). Toạ độ hiệu ứng tính từ khung bao con ở dáng nghỉ (chân, mép trước, chiều cao), nên khuôn dùng chung.
  1_1 đứng 28 khung: nhấp nhô thở, đầu gật, mảnh đung đưa lệch nhịp, mảnh bay trôi.
  1_2 trúng đòn 18 khung: bật lùi ngửa, đầu hất.
  1_4 đánh 32 khung: lấy đà, lao (đỉnh khung 18), vung, lá nổ ở mép trước.
  1_5 bắn tia 20 khung: ngả ra sau, lá xoáy tụ ở chỗ bắn, bắn ở khung 12.
  1_6 chiêu cuối 44 khung (lao, trúng khung 24): spin = bật lên xoay một vòng trong lốc lá rồi lao tới; slam = nhảy vồ đập
      xuống; nổ lá, vòng cỏ loang mặt đất, lá bay.

    py -3 -I ArtGen/Heroes/tools/anim_moc.py <mã> [...] [--run]     --run: chạy luôn anim_moi.py
"""
import json
import math
import os
import subprocess
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
HEROES = os.path.normpath(os.path.join(HERE, ".."))
AOLA = next(p for p in ("E:/ProjectAtomik/aola", "D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper")
            if os.path.isdir(p))
FX_DIR = [os.path.join(HEROES, "inbox", "moc_fx", "tai_ve").replace("\\", "/") + "/"]
# ảnh gói moc_fx (build_fx.py): FX01 lốc lá (vòng rỗng), FX03 lá nổ, FX04 chùm lá bay, FX05 phấn hoa lấp lánh,
# FX07 dây gai quật (chiêu cuối), FX08 vòng cỏ loang mặt đất (vòng rỗng)
HOLLOW = ["FX01", "FX08"]


def mul(p, q):
    a, b, c, d, e, f = p
    A, B, C, D, E, F_ = q
    return [a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F_ + e, b * E + d * F_ + f]


def apply(m, x, y):
    return m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]


def rest_geometry(rdir):
    """tên mảnh, khung bao mỗi mảnh (toạ độ clip) ở dáng nghỉ, từ bản vừa ghép"""
    gp = os.path.join(rdir, "anim_ghep.json")
    ap = gp if os.path.exists(gp) else os.path.join(rdir, "export", "anim.json")
    anim = json.load(open(ap, encoding="utf-8"))
    sprites = anim["sprites"]
    boxes, order = {}, []
    for r in anim["clips"]["1_1"]["frames"][0]:
        sp = sprites[int(r[0])]
        name = os.path.splitext(os.path.basename(sp))[0]
        w, h = Image.open(os.path.normpath(os.path.join(rdir, sp))).size
        m = [float(v) for v in r[1:7]]
        pts = [apply(m, x, y) for x, y in ((0, 0), (w, 0), (w, h), (0, h))]
        boxes[name] = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        order.append(name)
    return order, boxes


def inv(m):
    a, b, c, d, e, f = m
    det = a * d - b * c
    return [d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det]


def idle_tracks(rdir):
    """khung clip đứng GỐC (bản vừa ghép giữ nguyên chuyển động aola, hình đã thay): mỗi khung {tên mảnh: ma trận}"""
    gp = os.path.join(rdir, "anim_ghep.json")
    anim = json.load(open(gp if os.path.exists(gp) else os.path.join(rdir, "export", "anim.json"), encoding="utf-8"))
    names = [os.path.splitext(os.path.basename(s))[0] for s in anim["sprites"]]
    out = []
    for fr in anim["clips"]["1_1"]["frames"]:
        d = {}
        for r in fr:
            d.setdefault(names[int(r[0])], [float(v) for v in r[1:7]])
        out.append(d)
    return out


def secondary_motion(tracks, n, p, box, H):
    """chuyển động phụ của mảnh n so với cha p trong clip đứng gốc (mây trôi, vòng quay, tai vẫy, đèn đung đưa...),
    tính trong toạ độ dáng nghỉ quanh tâm mảnh: [(góc, dx, dy)] mỗi khung gốc, thêm một khung cuối nối vòng; None nếu gần
    như đứng yên (góc dưới 4 độ, dời dưới 1,5% chiều cao)"""
    if n not in tracks[0] or p not in tracks[0]:
        return None
    Mp0 = tracks[0][p]
    R0i = inv(mul(inv(Mp0), tracks[0][n]))
    P = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
    seq, last = [], (0.0, 0.0, 0.0)
    for fr in tracks:
        if n in fr and p in fr:
            D = mul(mul(inv(fr[p]), fr[n]), R0i)
            Dc = mul(Mp0, mul(D, inv(Mp0)))
            th = math.degrees(math.atan2(Dc[1], Dc[0]))
            if seq:  # góc liền mạch (vòng quay đủ 360 độ)
                th += 360 * round((seq[-1][0] - th) / 360)
            px, py = apply(Dc, *P)
            last = (th, px - P[0], py - P[1])
        seq.append(last)
    if max(abs(s[0]) for s in seq) < 4 and max(math.hypot(s[1], s[2]) for s in seq) < 0.015 * H:
        return None
    th0 = seq[0][0]
    seq.append((th0 + 360 * round((seq[-1][0] - th0) / 360), seq[0][1], seq[0][2]))
    return seq


def cycle_keys(seq, frames, period=28, step=2):
    """khoá [khung, góc, dx, dy] lặp chuyển động phụ theo chu kỳ period khung suốt clip frames khung (vòng quay cộng dồn)"""
    no = len(seq) - 1
    turn = seq[-1][0] - seq[0][0]
    keys = []
    for f in list(range(0, frames, step)) + [frames]:
        k, r = divmod(f, period)
        x = r * no / period
        i = int(x)
        t = x - i
        a, b = seq[i], seq[min(i + 1, no)]
        v = [a[j] + (b[j] - a[j]) * t for j in range(3)]
        keys.append([f, round(v[0] + turn * k, 2), round(v[1], 2), round(v[2], 2)])
    return keys


def build(code, run=False):
    f = json.load(open(os.path.join(HEROES, "forms_moc", code + ".json"), encoding="utf-8"))
    a = f.get("anim") or {}
    pid = f["aola"]
    rdir = os.path.join(AOLA, "reskin", f"moc_{pid}")
    order, boxes = rest_geometry(rdir)
    # số mảnh -> tên sau ghép (Nxx_<số>)
    name = {}
    for nm in order:
        if nm.startswith("N") and "_" in nm:
            try:
                name[int(nm.split("_")[1])] = nm
            except ValueError:
                pass
    group_of = {int(nm.split("_")[1]): nm.split("_")[0] for nm in name.values()}
    # bóng: mảnh giữ đầu tiên (thường là mảnh 1)
    parts = json.load(open(os.path.join(AOLA, "reskin", f"pet{pid}_parts", "front_idle", "parts.json"), encoding="utf-8"))["parts"]
    shadow = None
    keep = json.load(open(os.path.join(rdir, "groups.json"), encoding="utf-8")).get("keep", [])
    if keep:
        c = next(p["character"] for p in parts if p["n"] == keep[0])
        shadow = f"c{c}" if f"c{c}" in boxes else None

    def nm(n):
        return name.get(int(n))

    root = nm(a.get("root")) or next(iter(name.values()))
    head = nm(a.get("head")) or root
    fly = {nm(n) for n in a.get("fly", []) if nm(n)}
    pover = {nm(k): (nm(v) if v is not None else None) for k, v in (a.get("parent") or {}).items() if nm(k)}
    head_group = group_of.get(int(head.split("_")[1]))
    rig = {}
    for n, pn in name.items():
        if pn == root:
            rig[pn] = {"parent": None}
        elif pn in fly:
            rig[pn] = {"parent": None}
        elif pn in pover:
            rig[pn] = {"parent": pover[pn] if pover[pn] in name.values() else root}
        elif pn == head:
            rig[pn] = {"parent": root}
        elif group_of[n] == head_group:
            rig[pn] = {"parent": head}
        else:
            rig[pn] = {"parent": root}
    # vòng cha (cha khai sai): cắt về gốc
    for pn in list(rig):
        seen, cur = set(), pn
        while rig.get(cur, {}).get("parent"):
            if cur in seen:
                rig[pn]["parent"] = root
                break
            seen.add(cur)
            cur = rig[cur]["parent"]

    body = [b for n, b in boxes.items() if n != shadow and n not in fly]
    x0, y0 = min(b[0] for b in body), min(b[1] for b in body)
    x1, y1 = max(b[2] for b in body), max(b[3] for b in body)
    H = y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    foot_y = (boxes[shadow][1] + boxes[shadow][3]) / 2 if shadow else y1
    L = max(90.0, min(170.0, 0.6 * H))  # quãng lao: > 60 để trận lấy đỉnh lao, không quá xa kẻo thành hình ở xa
    front = [round(x1 + 0.05 * H, 1), round(cy, 1)]
    swing = [nm(n) for n in a.get("swing", []) if nm(n)]
    wob = [nm(n) for n in a.get("wob", []) if nm(n)]
    cp, cfx, cfy = a.get("cast") or (a.get("head"), 0.8, 0.5)
    cpn = nm(cp) or head
    cb = boxes[cpn]
    muzzle = [round(cb[0] + (cb[2] - cb[0]) * cfx, 1), round(cb[1] + (cb[3] - cb[1]) * cfy, 1)]
    nforms, form = f["forms"], f["form"]
    beam = {1: [1.0], 2: [0.85, 1.25], 3: [0.7, 1.0, 1.4]}[nforms][form - 1]
    if f["hero"] == "Thanh Long":
        beam = round(beam * 1.2, 2)
    ult = a.get("ult") or ("slam" if swing else "spin")

    def S(v):
        return round(v, 2)

    clips = {}
    # 1_1 đứng
    k1 = {}
    if head != root:
        k1[head] = [[0, 0], [14, 3], [28, 0]]
    for i, n in enumerate(wob):
        s = 7 if i % 2 == 0 else -7
        k1[n] = [[0, 0], [7 + 3 * i, s], [21 + 3 * i if 21 + 3 * i < 28 else 26, -s * 0.6], [28, 0]]
    for i, n in enumerate(fly):
        ph = (i * 5) % 14
        k1[n] = [[0, 0, 0, 0], [ph + 7, 0, 0, S(-0.05 * H)], [28, 0, 0, 0]]
    clips["1_1"] = {"_": "đứng: nhấp nhô thở, đầu gật, mảnh đung đưa lệch nhịp", "frames": 28,
                    "root": [[0, 0, 0, 0, 1, 1], [14, 0, S(-0.025 * H), 0, 1, 1.02], [28, 0, 0, 0, 1, 1]], "keys": k1}
    # 1_2 trúng đòn
    k2 = {}
    if head != root:
        k2[head] = [[0, 0], [3, -12], [10, 3], [18, 0]]
    for i, n in enumerate(wob):
        k2[n] = [[0, 0], [3, -14 if i % 2 == 0 else 14], [10, 3], [18, 0]]
    clips["1_2"] = {"_": "trúng đòn: bật lùi ngửa, đầu hất, rồi về", "frames": 18,
                    "root": [[0, 0, 0, 0, 1, 1], [3, S(-0.12 * H), 0, -9, 1.06, 0.94], [9, S(-0.06 * H), 0, 2, 1, 1],
                             [18, 0, 0, 0, 1, 1]], "keys": k2}
    # 1_4 đánh
    k4 = {n: [[0, 0], [8, -30], [15, 20], [18, 40], [26, 0]] for n in swing}
    if head != root and head not in swing:
        k4[head] = [[0, 0], [8, -6], [17, 8], [26, 0]]
    fx4 = [{"img": "FX03", "pin": {"piece": root, "at": front, "frame": 18}, "at": [S(0.05 * H), 0], "size": S(0.7 * H),
            "keys": [[17, 0.35, 0, 1, 0, 0], [19, 1, 20, 1, 0, 0], [23, 1.25, 35, 0.6, 0, 0], [26, 1.35, 45, 0, 0, 0]]},
           {"img": "FX04", "pin": {"piece": root, "at": front, "frame": 18}, "at": [0, S(-0.15 * H)], "size": S(0.45 * H),
            "keys": [[18, 0.5, 0, 1, 0, 0], [21, 1, 30, 1, S(0.15 * H), S(-0.1 * H)], [27, 1, 60, 0, S(0.3 * H), S(0.1 * H)]]}]
    clips["1_4"] = {"_": "đánh: lấy đà, lao tới (đỉnh khung 18), vung, lá nổ ở mép trước", "frames": 32,
                    "root": [[0, 0, 0, 0, 1, 1], [8, S(-0.1 * H), 0, -7, 0.95, 1.06], [15, S(0.85 * L), 0, 6, 1.05, 0.96],
                             [18, S(L), 0, 8, 1, 1], [23, S(0.55 * L), 0, 0, 1, 1], [32, 0, 0, 0, 1, 1]],
                    "keys": k4, "fx": fx4}
    if swing:
        clips["1_4"]["top"] = [{"pieces": swing, "from": 12, "to": 24}]
    # 1_5 bắn tia
    clips["1_5"] = {"_": "bắn tia: ngả ra sau, lá xoáy tụ ở chỗ bắn, bắn ở khung 12", "frames": 20,
                    "root": [[0, 0, 0, 0, 1, 1], [8, S(-0.06 * H), 0, -6, 1, 1.04], [12, S(0.04 * H), 0, 4, 1, 0.97],
                             [16, S(0.01 * H), 0, 0, 1, 1], [20, 0, 0, 0, 1, 1]],
                    "keys": {n: [[0, 0], [8, -20], [12, 15], [20, 0]] for n in swing},
                    "fx": [{"img": "FX01", "anchor": cpn, "at": muzzle, "size": S(0.35 * H),
                            "keys": [[2, 0.3, 0, 0, 0, 0], [8, 1, -120, 1, 0, 0], [12, 0.8, -200, 0.8, 0, 0], [14, 0.5, -240, 0, 0, 0]]},
                           {"img": "FX05", "anchor": cpn, "at": muzzle, "size": S(0.25 * H),
                            "keys": [[6, 0.4, 0, 0, 0, 0], [10, 1, 40, 1, 0, 0], [14, 0.6, 80, 0, 0, 0]]}]}
    # 1_6 chiêu cuối (lao, trúng khung 24)
    burst = [{"img": "FX03", "pin": {"piece": root, "at": front, "frame": 24}, "at": [0, 0], "size": S(0.9 * H),
              "keys": [[22, 0.4, 0, 1, 0, 0], [25, 1, 20, 1, 0, 0], [29, 1.2, 40, 0.6, 0, 0], [32, 1.3, 50, 0, 0, 0]]},
             {"img": "FX08", "pin": {"piece": root, "at": [front[0], foot_y], "frame": 24}, "at": [0, 0], "size": S(1.3 * H),
              "z": "back", "keys": [[23, 0.3, 0, 1, 0, 0], [28, 1, 0, 0.8, 0, 0], [34, 1.2, 0, 0, 0, 0]]},
             {"img": "FX04", "anchor": None, "at": [S(x0), S(y0)], "size": S(0.35 * H),
              "keys": [[20, 0.6, 0, 0, 0, 0], [24, 1, 40, 1, S(0.4 * H), S(0.1 * H)], [34, 1, 90, 0, S(0.9 * H), S(0.3 * H)]]},
             {"img": "FX05", "anchor": None, "at": [S(x1), S(y0)], "size": S(0.3 * H),
              "keys": [[4, 0.4, 0, 0, 0, 0], [9, 1, 30, 1, 0, 0], [16, 0.7, 60, 0, 0, 0]]}]
    if ult == "spin":
        r6 = [[0, 0, 0, 0, 1, 1], [6, 0, S(0.03 * H), 0, 1.06, 0.92], [10, 0, S(-0.15 * H), 0, 1, 1],
              [18, S(-0.05 * H), S(-0.18 * H), 360, 1, 1], [24, S(1.25 * L), 0, 360, 1, 1], [29, S(1.15 * L), 0, 360, 1, 1],
              [38, S(0.2 * L), 0, 360, 1, 1], [44, 0, 0, 360, 1, 1]]
        k6 = {n: [[0, 0], [18, 0], [22, 35], [24, 45], [32, 0]] for n in swing}
        fx6 = [{"img": "FX01", "anchor": None, "at": [S(cx), S(cy)], "size": S(1.2 * H), "z": "back",
                "keys": [[6, 0.5, 0, 0, 0, 0], [10, 1, -180, 1, 0, 0], [18, 1.1, -520, 1, 0, 0], [21, 0.8, -620, 0, 0, 0]]}] + burst
        note = "chiêu cuối: bật lên xoay một vòng trong lốc lá, lao tới (trúng khung 24), nổ lá, vòng cỏ, lá bay"
    else:
        r6 = [[0, 0, 0, 0, 1, 1], [6, 0, 0, 0, 1.08, 0.9], [14, S(0.4 * L), S(-0.45 * H), -10, 0.95, 1.06],
              [20, S(0.9 * L), S(-0.5 * H), 12, 1, 1], [24, S(1.25 * L), 0, 0, 1.12, 0.86], [28, S(1.25 * L), 0, 0, 1, 1],
              [36, S(0.4 * L), 0, 0, 1, 1], [44, 0, 0, 0, 1, 1]]
        k6 = {n: [[0, 0], [14, -45], [22, 30], [24, 45], [32, 0]] for n in swing}
        fx6 = burst + [{"img": "FX07", "pin": {"piece": root, "at": [front[0], foot_y], "frame": 24}, "at": [S(0.3 * H), S(-0.4 * H)],
                        "size": S(1.2 * H), "keys": [[22, 0.4, 0, 1, 0, 0], [25, 1, 0, 1, 0, 0], [32, 1.05, 0, 0.7, 0, 0],
                                                     [36, 1.1, 0, 0, 0, 0]]}]
        note = "chiêu cuối: nhảy vồ, đập xuống trước mặt (trúng khung 24), dây gai quật lên, nổ lá, vòng cỏ, lá bay"
    if head != root and head not in swing:
        k6[head] = [[0, 0], [14, -8], [24, 10], [32, 0]]
    clips["1_6"] = {"_": note, "frames": 44, "lunge": True, "root": r6, "keys": k6, "fx": fx6}
    if swing:
        clips["1_6"]["top"] = [{"pieces": swing, "from": 14, "to": 30}]
    # chuyển động phụ (người dùng dặn 2026-11-07: mây, vòng, đồ bay quanh tướng phải động như bản gốc): mảnh bay, mảnh đung
    # đưa và nhóm đổi dáng (trừ nhóm đầu, mảnh vung) lấy chuyển động của chính nó so với cha trong clip đứng gốc, lặp ở mọi clip
    kinds = {g[0]: g[3] for g in f["groups"]}
    cand = set(fly) | set(wob) | {pn for n, pn in name.items() if kinds.get(group_of[n]) == "doi" and group_of[n] != head_group}
    cand -= {root, head} | set(swing)
    tracks = idle_tracks(rdir)
    phu = {}
    for pn in sorted(cand):
        par = rig[pn]["parent"] or root
        seq = secondary_motion(tracks, pn, par, boxes[pn], H)
        if seq:
            phu[pn] = seq
            rig[pn]["pivot"] = [round((boxes[pn][0] + boxes[pn][2]) / 2, 2), round((boxes[pn][1] + boxes[pn][3]) / 2, 2)]
    # bản gốc đứng yên (mây của Thanh Long...): chuyển động mặc định lệch nhịp; mảnh đung đưa lắc quanh khớp (khớp tự tìm),
    # mảnh khác (mây, vòng, đồ bay) trôi nhẹ ngang dọc
    gname = {g[0]: g[2].lower() for g in f["groups"]}
    TROI = ("cloud", "ring", "halo", "orb", "bubble", "slat", "panel", "aura", "swirl", "lightning", "bolt", "spark",
            "trail", "spinner", "samara", "bead", "pearl", "wind", "drop", "petal")
    LAC = ("ear", "antenna", "whisker", "tail", "wing", "leaf", "leaves", "fin", "crest", "mane", "frond",
           "feather", "hair", "ribbon", "tuft", "lantern", "sprout", "vine", "whip", "frill")
    mac = {}
    for i, pn in enumerate(sorted(cand - set(phu))):
        ph = 2 * math.pi * ((i * 0.37) % 1)
        gn = gname.get(pn.split("_")[0], "")
        if pn in fly or any(w in gn for w in TROI):  # mây, vòng, đồ bay: trôi nhẹ ngang dọc
            ax, ay = 0.02 * H, 0.015 * H
            seq = [(0, ax * math.sin(2 * math.pi * k / 28 + ph), ay * math.sin(4 * math.pi * k / 28 + ph)) for k in range(29)]
        elif pn in wob or any(w in gn for w in LAC):  # tai, sừng, đuôi, cánh, lá: lắc quanh khớp (khớp tự tìm)
            seq = [(5 * math.sin(2 * math.pi * k / 28 + ph), 0, 0) for k in range(29)]
        else:  # vương miện, mũ, giáp, huy hiệu: đứng yên theo cha
            continue
        mac[pn] = seq
    for c in clips.values():
        for pn, seq in list(phu.items()) + list(mac.items()):
            c.setdefault("keys", {})[pn] = cycle_keys(seq, c["frames"])
    if phu:
        print(f"  chuyển động phụ theo bản gốc: {', '.join(sorted(phu))}")
    if mac:
        print(f"  chuyển động phụ mặc định: {', '.join(sorted(mac))}")
    cfg = {"_ghi_chu": f"{code} (anim_moc.py, 2026-11-07): tướng đảo Mộc, chiêu cuối kiểu {ult}; H {H:.0f}, quãng lao {L:.0f}",
           "fx_dir": FX_DIR, "fx_hollow": HOLLOW, "rig": rig, "clips": clips,
           "cast": {"clip": "1_5", "piece": cpn, "at": muzzle, "frame": 12, "beam": beam}}
    if shadow:
        cfg["shadow"] = shadow
    old = os.path.join(rdir, "anim_moi.json")
    if os.path.exists(old):  # chỉnh tay lúc soi (behind, pivot) giữ khi chạy lại
        o = json.load(open(old, encoding="utf-8"))
        if o.get("behind"):
            cfg["behind"] = o["behind"]
        for n, d in o.get("rig", {}).items():
            if n in cfg["rig"] and d.get("pivot"):
                cfg["rig"][n]["pivot"] = d["pivot"]
    json.dump(cfg, open(old, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(code, f"H {H:.0f} L {L:.0f} gốc {root} đầu {head} chiêu {ult} tia {beam}")
    if run:
        p = subprocess.run([sys.executable, "-I", os.path.join(AOLA, "tools", "anim_moi.py"), rdir], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        print((p.stdout + p.stderr)[-1500:])
        return p.returncode
    return 0


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    for c in args:
        build(c, run="--run" in sys.argv)
