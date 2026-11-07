"""Animation boss đảo Thủy lô 2 (2026-11-07 đêm): khuôn có tham số, ghi <aola>/reskin/thuy_<id>/anim_moi.json.

Người dùng dặn: boss đẹp hơn, nhiều hiệu ứng hơn; 3 boss cuối (Thương Lam, Huyền Vũ, Lam Quân) có tia mana riêng (cast.tia).
Toạ độ hiệu ứng tính từ rig (chân, mép trước, chiều cao con), nên khuôn dùng chung được cho 15 dạng.

    py -3 -I ArtGen/Heroes/tools/anim_lo2.py [mã ...]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
AOLA = next(p for p in ("D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper", "E:/ProjectAtomik/aola") if os.path.isdir(p))
sys.path.insert(0, os.path.join(AOLA, "tools"))
import ghep_nhom as gn  # noqa: E402
import portrait_png as pp  # noqa: E402


def R(*k):
    return [[f, v] for f, v in k]


# mỗi dạng: gốc, đầu, mảnh vung khi đánh, mảnh đung đưa, mảnh bay (cha null), cha ghim thêm, chỗ bắn (mảnh, phần khung bao:
# fx, fy), cỡ tia, kiểu tia riêng, kiểu chiêu cuối, hiệu ứng đòn đánh và chiêu cuối (bộ của dòng)
SPEC = {
    "vay_lam_1": dict(pid=546, root=5, head=5, swing=[], wob=[3], fly=[13, 14], cast=(5, 0.95, 0.6), beam=0.84, kind="spin", line="vl"),
    "vay_lam_2": dict(pid=547, root=8, head=5, swing=[10, 4], wob=[3, 7], fly=[12, 13, 2, 9], cast=(5, 0.98, 0.65), beam=1.2, kind="spin", line="vl",
                      top=[5]),  # đầu gộp các mảnh mặt cũ (vẽ trên thân) nhưng mảnh đầu gốc nằm dưới thân: đưa lên trên mọi clip
    "vay_lam_3": dict(pid=548, root=16, head=16, swing=[], wob=[], fly=[9, 24, 28, 31, 2, 6, 23, 26, 27, 11, 12], cast=(16, 0.98, 0.55), beam=1.68, kind="spin", line="vl"),
    "kuba_1": dict(pid=94, root=14, head=18, swing=[16, 9], wob=[51, 52, 53], fly=[57, 58, 59, 60, 61, 62], cast=(18, 0.75, 0.75), beam=0.84, kind="shell", shell=19, line="kb"),
    "kuba_2": dict(pid=95, root=10, head=17, swing=[3], wob=[26, 8], fly=[37], cast=(3, 0.95, 0.4), beam=1.2, kind="shell", shell=13, line="kb"),
    "kuba_3": dict(pid=96, root=26, head=15, swing=[], wob=[18, 7], fly=[28, 29], cast=(15, 0.8, 0.7), beam=1.68, kind="slam", line="kb"),
    "thuong_lam_1": dict(pid=805, root=6, head=13, swing=[17], wob=[17, 9], fly=[], cast=(13, 0.95, 0.65), beam=0.84, kind="spin", line="tl", tia="tia_bang"),
    "thuong_lam_2": dict(pid=806, root=6, head=9, swing=[10], wob=[10, 5], fly=[], cast=(9, 0.97, 0.75), beam=1.2, kind="spin", line="tl", tia="tia_bang"),
    "thuong_lam_3": dict(pid=807, root=16, head=26, swing=[15, 20], wob=[15, 20, 9], fly=[], cast=(26, 0.98, 0.7), beam=1.68, kind="spin", line="tl", tia="tia_bang",
                         # khớp tự dò gắn cánh 20 vào cánh 15 và đuôi vào cánh: ghim theo Rig_Numbered (cánh, đuôi, vây dưới vào thân;
                         # chùm lưỡi sao vào chóp đuôi 9; đầu vào cổ 18)
                         parent={"15": 16, "20": 16, "11": 16, "10": 11, "9": 10, "12": 9, "3": 9, "8": 9, "6": 8, "7": 8, "5": 8, "4": 8,
                                 "25": 16, "14": 25, "26": 18}),
    "huyen_vu_1": dict(pid=713, root=7, head=12, swing=[12], wob=[10], fly=[22], cast=(12, 0.95, 0.7), beam=0.84, kind="slam", line="hv", tia="tia_xoay"),
    "huyen_vu_2": dict(pid=714, root=13, head=17, swing=[2, 6], wob=[2, 10], fly=[], cast=(17, 0.98, 0.7), beam=1.2, kind="slam", line="hv", tia="tia_xoay"),
    # bắn từ miệng (trước mặt): đầu mái chèo nằm sau lưng, tia từ đó bay qua che kín đầu (soi tour 2026-11-07)
    "huyen_vu_3": dict(pid=715, root=5, head=12, swing=[8], wob=[36], fly=[], cast=(12, 0.95, 0.7), beam=1.68, kind="slam", line="hv", tia="tia_xoay",
                       parent={"14": 8}),
    "lam_quan_1": dict(pid=1831, root=6, head=14, swing=[17], wob=[14], fly=[7], cast=(17, 0.98, 0.5), beam=0.84, kind="bell", bell=7, line="lq", tia="tia_trieu"),
    # Lam Quân 2: khớp tự dò treo đầu và đinh ba vào chuông; ghim: đầu vào thân, cán đinh ba 10 xoay quanh bàn tay 19 (vung là đâm xuống)
    "lam_quan_2": dict(pid=1832, root=6, head=24, swing=[10], wob=[2], fly=[28, 2, 37], cast=(27, 0.95, 0.5), beam=1.2, kind="bell", bell=28, line="lq", tia="tia_trieu",
                       parent={"24": 6, "3": 6, "25": 24, "10": 19, "27": 10, "23": 10, "21": 9, "26": 30}),
    # Lam Quân 3: khớp tự dò treo cả thân trên vào áo choàng 4; ghim vào thân 11/13 theo Rig_Numbered
    "lam_quan_3": dict(pid=2955, root=13, head=9, swing=[22], wob=[4], fly=[28, 2, 1], cast=(9, 0.9, 0.6), beam=1.68, kind="bell", bell=28, line="lq", tia="tia_trieu",
                       parent={"11": 13, "3": 11, "5": 13, "6": 11, "8": 11, "9": 11, "10": 11, "14": 11, "22": 14, "17": 11, "18": 17, "27": 11,
                               "29": 9, "26": 13, "21": 13, "24": 13, "20": 26, "23": 24}),
}

# hiệu ứng theo dòng: (đánh: ảnh ở mép trước lúc trúng), (chiêu: ảnh lớn sau thân, ảnh nổ lúc trúng)
LINE_FX = {
    "vl": dict(hit="song", hit_move=1.2, big="than", burst="no", extra="giot"),
    "kb": dict(hit="vong", hit_move=0, big="xoay", burst="no", extra="lap"),
    "tl": dict(hit="thuy_boss_fx/FX14", hit_move=0.9, big="than", burst="thuy_boss_fx/FX14", extra="lap"),
    "hv": dict(hit="vong", hit_move=0, big="xoay", burst="no", extra="giot"),
    "lq": dict(hit="thuy_boss_fx/FX15", hit_move=0, big="than", burst="no", extra="lap"),
}


def geom(pid, fly):
    r = gn.Rig(os.path.join(AOLA, "reskin", f"pet{pid}_parts"), "1_1")
    body, foot = [], None
    for n, p in enumerate(r.first, 1):
        im = r.char_img(str(p["c"]))
        b = r.box(p)
        if im is None or not b:
            continue
        if pp.is_shadow(im) and foot is None:
            foot = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
            continue
        if n not in fly:
            body.append(b)
    x0, y0 = min(b[0] for b in body), min(b[1] for b in body)
    x1, y1 = max(b[2] for b in body), max(b[3] for b in body)
    if foot is None:
        foot = ((x0 + x1) / 2, y1)
    return r, dict(x0=x0, y0=y0, x1=x1, y1=y1, H=y1 - y0, W=x1 - x0, cy=(y0 + y1) / 2, foot=foot)


def part_pt(r, n, fx, fy):
    b = r.box(r.first[n - 1])
    return [round(b[0] + (b[2] - b[0]) * fx, 1), round(b[1] + (b[3] - b[1]) * fy, 1)]


def build(code, s):
    r, g = geom(s["pid"], s["fly"])
    H = g["H"]
    L = max(90.0, min(170.0, 0.6 * H))  # quãng lao (px clip): >60 để trận lấy đỉnh lao, không quá xa kẻo thành hình ở xa
    front = [g["x1"] + 0.05 * H, g["cy"]]
    lf = LINE_FX[s["line"]]
    root, head = s["root"], s["head"]
    parent = {str(n): None for n in s["fly"]}
    parent.update(s.get("parent", {}))
    sw = ",".join(str(n) for n in s["swing"]) or None
    wob = s["wob"]
    clips = {}
    # đứng: nhấp nhô, đầu gật nhẹ, mảnh đung đưa lệch nhịp, mảnh bay trôi
    k1 = {"root": R((0, {"dy": 0, "sy": 1}), (14, {"dy": -0.025 * H, "sy": 1.02}), (28, {"dy": 0, "sy": 1}))}
    if head != root:
        k1[str(head)] = R((0, {"rot": 0}), (14, {"rot": 3}), (28, {"rot": 0}))
    for i, n in enumerate(wob):
        a = 7 if i % 2 == 0 else -7
        k1[str(n)] = R((0, {"rot": 0}), (7 + 3 * i, {"rot": a}), (21 + 3 * i, {"rot": -a * 0.6}), (28, {"rot": 0}))
    for i, n in enumerate(s["fly"]):
        ph = (i * 5) % 14
        k1[str(n)] = R((0, {"dy": 0}), (ph + 7, {"dy": -0.05 * H}), (28, {"dy": 0}))
    clips["1_1"] = {"frames": 28, "keys": k1}
    # trúng đòn
    k2 = {"root": R((0, {"dx": 0, "sx": 1, "sy": 1}), (3, {"dx": -0.12 * H, "sx": 1.06, "sy": 0.94}), (9, {"dx": -0.06 * H, "sx": 1, "sy": 1}), (18, {"dx": 0}))}
    k2[str(root)] = R((0, {"rot": 0}), (3, {"rot": -9}), (10, {"rot": 2}), (18, {"rot": 0}))
    if head != root:
        k2[str(head)] = R((0, {"rot": 0}), (3, {"rot": -12}), (10, {"rot": 3}), (18, {"rot": 0}))
    clips["1_2"] = {"frames": 18, "keys": k2}
    # đánh: lấy đà, lao (đỉnh khung 18), vung, hiệu ứng trúng ở mép trước
    k4 = {"root": R((0, {"dx": 0, "sx": 1, "sy": 1}), (8, {"dx": -0.1 * H, "sx": 0.95, "sy": 1.06}), (15, {"dx": 0.85 * L, "sx": 1.05, "sy": 0.96}),
                    (18, {"dx": L}), (23, {"dx": 0.55 * L, "sx": 1, "sy": 1}), (32, {"dx": 0}))}
    k4[str(root)] = R((0, {"rot": 0}), (8, {"rot": -7}), (16, {"rot": 6}), (19, {"rot": 8}), (25, {"rot": 0}))
    if sw:
        k4[sw] = R((0, {"rot": 0}), (8, {"rot": -30}), (15, {"rot": 20}), (18, {"rot": 40}), (26, {"rot": 0}))
    hit = {"img": lf["hit"], "from": 16, "to": 26, "at": front, "follow": "root", "size": [0.35, 0.8], "a": [1, 1, 0],
           "move": [lf["hit_move"] * H, 0]}
    if lf["hit"] == "vong":  # vòng sóng loang mặt đất: nằm dưới chân, sau thân
        hit.update(at=[front[0], g["foot"][1]], size=[0.3, 1.0], back=True)
    fx4 = [hit,
           {"img": "no", "from": 17, "to": 25, "at": [front[0] + 0.1 * H, front[1]], "follow": "root", "size": [0.25, 0.6], "a": [1, 0]},
           {"img": lf["extra"], "from": 18, "to": 28, "at": [front[0], front[1] - 0.2 * H], "follow": "root", "size": 0.25,
            "move": [0.2 * H, 0.25 * H], "a": [1, 0]}]
    clips["1_4"] = {"frames": 32, "keys": k4, "fx": fx4}
    if sw:
        clips["1_4"]["top"] = {sw: [[12, 24]]}
    # bắn tia (mana): ngả ra sau, đẩy tới, bắn ở khung 12; tụ nước ở chỗ bắn
    cp, cfx, cfy = s["cast"]
    muzzle = part_pt(r, cp, cfx, cfy)
    k5 = {"root": R((0, {"dx": 0, "sy": 1}), (8, {"dx": -0.06 * H, "sy": 1.04}), (12, {"dx": 0.04 * H, "sy": 0.97}), (16, {"dx": 0.01 * H, "sy": 1}), (20, {"dx": 0}))}
    k5[str(root)] = R((0, {"rot": 0}), (8, {"rot": -6}), (12, {"rot": 4}), (20, {"rot": 0}))
    fx5 = [{"img": "xoay", "from": 2, "to": 13, "part": cp, "at": muzzle, "size": [0.1, 0.35], "spin": -30, "a": [0, 1, 0.6]},
           {"img": "lap", "from": 6, "to": 14, "part": cp, "at": muzzle, "size": [0.1, 0.25], "a": [0, 1, 0]}]
    clips["1_5"] = {"frames": 20, "keys": k5, "fx": fx5}
    # chiêu cuối (44 khung, trúng ở khung 24): theo kiểu, nhiều hiệu ứng (boss)
    n6 = 44
    big = {"img": lf["big"], "from": 8, "to": 32, "at": [g["foot"][0] - 0.1 * H, g["cy"]], "follow": "root", "size": [0.6, 1.4],
           "a": [0, 0.9, 0], "back": True, "spin": 12 if lf["big"] == "xoay" else 0}
    burst = [{"img": lf["burst"], "from": 22, "to": 32, "at": front, "follow": "root", "size": [0.4, 1.1], "a": [1, 1, 0]},
             {"img": "no", "from": 23, "to": 31, "at": [front[0] + 0.15 * H, front[1]], "follow": "root", "size": [0.3, 0.9], "a": [1, 0], "rot": [0, 40]},
             {"img": "vong", "from": 23, "to": 34, "at": [g["foot"][0] + 0.3 * H, g["foot"][1]], "follow": "root", "size": [0.4, 1.3], "a": [1, 0]},
             {"img": lf["extra"], "from": 20, "to": 34, "at": [g["x0"], g["y0"]], "follow": "root", "size": 0.3, "move": [0.6 * H, 0.2 * H], "a": [0, 1, 0]},
             {"img": "lap", "from": 4, "to": 16, "at": [g["x1"], g["y0"]], "follow": "root", "size": [0.15, 0.35], "a": [0, 1, 0]}]
    if s["kind"] == "spin":
        k6 = {"root": R((0, {"dx": 0, "dy": 0, "sx": 1, "sy": 1}), (6, {"dy": 0.03 * H, "sx": 1.06, "sy": 0.92}), (10, {"dy": -0.15 * H, "sx": 1, "sy": 1}),
                        (18, {"dy": -0.18 * H, "dx": -0.05 * H}), (24, {"dx": 1.25 * L, "dy": 0}), (29, {"dx": 1.15 * L}), (38, {"dx": 0.2 * L}), (44, {"dx": 0}))}
        k6[str(root)] = R((0, {"rot": 0}), (8, {"rot": 0}), (18, {"rot": 360}), (44, {"rot": 360}))
        fx6 = [big, {"img": "xoay", "from": 6, "to": 20, "at": [g["foot"][0], g["cy"]], "follow": "root", "size": [0.5, 1.0], "spin": 30, "a": [0, 1, 0], "back": True}] + burst
        lunge = True
    elif s["kind"] == "shell":
        sh = s["shell"]
        k6 = {"root": R((0, {"dx": 0, "dy": 0, "sx": 1, "sy": 1}), (6, {"sx": 1.08, "sy": 0.9}), (10, {"dy": -0.2 * H, "sx": 0.92, "sy": 1.08}),
                        (14, {"dy": 0, "sx": 1, "sy": 1}), (24, {"dx": 1.25 * L}), (29, {"dx": 1.1 * L}), (38, {"dx": 0.2 * L}), (44, {"dx": 0}))}
        k6[str(root)] = R((0, {"rot": 0}), (12, {"rot": 0}), (22, {"rot": 360}), (44, {"rot": 360}))
        k6[str(sh)] = R((0, {"sx": 1, "sy": 1}), (10, {"sx": 1.15, "sy": 1.15}), (24, {"sx": 1.1, "sy": 1.1}), (32, {"sx": 1, "sy": 1}))
        fx6 = [big] + burst
        lunge = True
    elif s["kind"] == "slam":
        k6 = {"root": R((0, {"dx": 0, "dy": 0, "sx": 1, "sy": 1}), (6, {"sx": 1.08, "sy": 0.9}), (14, {"dy": -0.45 * H, "dx": 0.4 * L, "sx": 0.95, "sy": 1.06}),
                        (20, {"dy": -0.5 * H, "dx": 0.9 * L}), (24, {"dy": 0, "dx": 1.25 * L, "sx": 1.12, "sy": 0.86}), (28, {"sx": 1, "sy": 1}),
                        (36, {"dx": 0.4 * L}), (44, {"dx": 0}))}
        k6[str(root)] = R((0, {"rot": 0}), (14, {"rot": -10}), (22, {"rot": 12}), (28, {"rot": 0}))
        if sw:
            k6[sw] = R((0, {"rot": 0}), (14, {"rot": -45}), (22, {"rot": 30}), (24, {"rot": 45}), (32, {"rot": 0}))
        fx6 = [big] + burst + [{"img": "than", "from": 22, "to": 36, "at": [g["foot"][0] + 0.8 * L, g["foot"][1] - 0.4 * H], "follow": "root",
                                 "size": [0.4, 1.2], "a": [1, 1, 0]}]
        lunge = True
    else:  # bell: gõ chuông ba nhịp bật vòng sóng âm, rồi lao đâm
        bell = s["bell"]
        bc = part_pt(r, bell, 0.5, 0.5)
        k6 = {"root": R((0, {"dx": 0, "dy": 0, "sx": 1, "sy": 1}), (4, {"dx": -0.06 * H}), (16, {"dx": -0.06 * H}), (24, {"dx": 1.25 * L}),
                        (29, {"dx": 1.15 * L}), (38, {"dx": 0.2 * L}), (44, {"dx": 0}))}
        k6[str(bell)] = R((0, {"rot": 0}), (4, {"rot": 10}), (6, {"rot": -8}), (8, {"rot": 9}), (10, {"rot": -7}), (12, {"rot": 6}),
                          (14, {"rot": -4}), (16, {"rot": 0}))
        if sw:
            k6[sw] = R((0, {"rot": 0}), (16, {"rot": -30}), (22, {"rot": 25}), (24, {"rot": 35}), (32, {"rot": 0}))
        rings = [{"img": "thuy_boss_fx/FX15", "from": f0, "to": f0 + 10, "at": bc, "follow": "root", "size": [0.3, 1.5], "a": [1, 0]}
                 for f0 in (4, 8, 12)]
        fx6 = [big] + rings + burst
        lunge = True
    clips["1_6"] = {"frames": n6, "keys": k6, "fx": fx6}
    if sw and s["kind"] in ("slam", "bell"):
        clips["1_6"]["top"] = {sw: [[14, 30]]}
    if s.get("top"):  # mảnh luôn nằm trên (khai trước để mảnh vung vẫn lên trên nó lúc vung)
        key = ",".join(str(n) for n in s["top"])
        for c in clips.values():
            c["top"] = {key: [[0, c["frames"]]], **c.get("top", {})}
    cfg = {"note": f"{code} (anim_lo2.py, 2026-11-07): boss đảo Thủy, khuôn {s['kind']}, hiệu ứng dòng {s['line']}",
           "root": root, "parent": parent, "clips": clips,
           "cast": {"part": cp, "at": muzzle, "frame": 12, "beam": s["beam"], **({"tia": s["tia"]} if s.get("tia") else {})}}
    if lunge:
        cfg["lunge"] = ["1_6"]
    path = os.path.join(AOLA, "reskin", f"thuy_{s['pid']}", "anim_moi.json")
    json.dump(cfg, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(code, f"H {H:.0f} L {L:.0f}", "tia" if s.get("tia") else "")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for code, s in SPEC.items():
        if not only or code in only:
            build(code, s)
