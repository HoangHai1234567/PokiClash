# -*- coding: utf-8 -*-
"""Quái lính .atomik (1 dạng, không thu thập) vào game: khối `game`, chân dung, chép Resources, đổi lính trong heroes.json / cards.json.

    py -3 -I ArtGen/Spine/quai_npc_game.py game <ma>       quai_<..>/atom/export/<ma>.atomik -> quai_<..>/game/<ma>.atomik + chan_dung.png
    py -3 -I ArtGen/Spine/quai_npc_game.py vao <ma> [--kiem]  chép vào Resources/<ma>/ + sửa heroes.json, cards.json (lính bậc 1 và 2)

Cấu hình từng con: quai_<..>/game_cfg.json, ví dụ
    {"hit": {"attack": 0.41, "cast": 0.5, "skill": 0.98},        # khung trúng (bỏ thì lấy sự kiện cuối của clip)
     "lunge": ["skill"], "stay": [], "muzzle_bone": "cg_mui", "beam": 0.8,   # chỗ bắn tia mana (xương ở khung trúng cast)
     "impact": {"attack": [0.06, 0.3, 0.08, ""], "skill": [0.1, 0.8, 0.1, "#ffd08a55"]},   # dừng, rung, bật lùi, chớp
     "lv": {"linh_cua": ["Tôm Đấm", "Tôm tít đấm bốc"], "linh_cua2": ["Tôm Quyền", "Cú đấm nổ bọt"]},
     "the": {"linh_cua_skill": ["Đấm Thẳng", "fist"], ...}}
Bậc 1 và bậc 2 dùng chung hình (cỡ `size` của lính giữ nguyên). Sau đó trong Unity: "PokiClash/Nhập dữ liệu", rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng" (đã duyệt cả `minions` từ 2026-11-20). Chạy lại không đổi gì thêm.
"""
import json
import os
import re
import shutil
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
JSON = os.path.join(ROOT, "Assets", "02 Data", "Json")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
KIEM = "--kiem" in sys.argv


def cfg(ma):
    return json.load(open(os.path.join(HERE, ma, "game_cfg.json"), encoding="utf-8"))


def game(ma):
    C = cfg(ma)
    src = os.path.join(HERE, ma, "atom", "export", f"{ma}.atomik")
    J, img, ver = A.load(src)
    ci = A.clip(J, "idle")
    P = A.Pose(J).at(ci, 0.0)
    B = A.bounds(P)
    clips, times = [], []
    for c in ("attack", "cast", "skill"):
        try:
            k = A.clip(J, c)
        except StopIteration:
            continue
        t = (C.get("hit") or {}).get(c)
        if t is None:
            ev = J["anims"][k].get("ev") or []
            if not ev:
                continue
            t = ev[-1]["t"]
        clips.append(c)
        times.append(round(float(t), 3))
    # chỗ bắn tia mana của game (StageView.Beam, tia nhuộm màu hệ): xương `muzzle_bone` ở khung trúng của cast; không khai = trước ngực
    muzzle = []
    mb = C.get("muzzle_bone")
    if mb and "cast" in clips:
        Pc = A.Pose(J).at(A.clip(J, "cast"), times[clips.index("cast")])
        pt = Pc.bone_pt(A.bi(J)[mb])
        muzzle = [round(float(pt[0]), 1), round(float(pt[1]), 1)]
    imp = C.get("impact") or {}
    ic = [c for c in clips if c in imp]
    J["game"] = {
        "fps": 25, "height": round(float(B[3]), 2), "hitClips": clips, "hitTimes": times,
        "lunge": C.get("lunge", []), "stay": C.get("stay", []), "far": [], "muzzle": muzzle, "beam": float(C.get("beam", 0.8)), "beamStyle": "",
        "move": "move", "shadow": "shadow",
        "impactClips": ic, "impactStop": [imp[c][0] for c in ic], "impactShake": [imp[c][1] for c in ic],
        "impactPush": [imp[c][2] for c in ic], "impactFlash": [imp[c][3] for c in ic], "span": 0,
    }
    out = os.path.join(HERE, ma, "game")
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, f"{ma}.atomik")
    kq = A.save(p, J, img, max(ver, 3))
    # chân dung vuông 512, nền trong suốt: khung 0 idle, cắt vuông ôm cả con
    le = 0.06
    side = max(B[2] - B[0], B[3] - B[1]) * (1 + 2 * le)
    cx, cy = (B[0] + B[2]) / 2, (B[1] + B[3]) / 2
    box = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
    im = A.render(J, img, P, box, 512 / side, ss=2)
    im.save(os.path.join(out, "chan_dung.png"))
    print(f"{p}: {kq[0] // 1024} KB, cao {B[3]:.0f}, trúng {dict(zip(clips, times))}, lao {J['game']['lunge']}, chỗ bắn {muzzle or 'trước ngực'}; chân dung {im.size}")


def _khoi(t, key, val):
    k0 = t.index(f'"{key}": "{val}"')
    a = t.rindex("{", 0, k0)
    d, i = 0, a
    while True:
        if t[i] == "{":
            d += 1
        elif t[i] == "}":
            d -= 1
            if d == 0:
                return a, i + 1
        i += 1


def vao(ma):
    C = cfg(ma)
    d = os.path.join(RES, ma)
    src = os.path.join(HERE, ma, "game")
    if not KIEM:
        os.makedirs(d, exist_ok=True)
    for nguon, dich in ((f"{ma}.atomik", f"{ma}.atomik"), ("chan_dung.png", f"{ma}_portrait.png")):
        p, q = os.path.join(src, nguon), os.path.join(d, dich)
        giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
        if not giong and not KIEM:
            shutil.copyfile(p, q)
        print(f"  Resources/{ma}/{dich}: {'giữ' if giong else ('sẽ chép' if KIEM else 'chép')}")
    # heroes.json: lính bậc 1, 2 -> aola = ma, tên, danh hiệu
    path = os.path.join(JSON, "heroes.json")
    t = open(path, "rb").read().decode("utf-8")
    t0 = t
    for lid, (ten, dh) in C["lv"].items():
        a, b = _khoi(t, "id", lid)
        blk = t[a:b]
        blk = re.sub(r'"aola": "[^"]*"', f'"aola": "{ma}"', blk)
        blk = re.sub(r'(\r?\n   "name": )"[^"]*"', lambda m: f'{m.group(1)}"{ten}"', blk, count=1)
        blk = re.sub(r'(\r?\n     "name": )"[^"]*"', lambda m: f'{m.group(1)}"{ten}"', blk, count=1)
        blk = re.sub(r'"title": "[^"]*"', f'"title": "{dh}"', blk, count=1)
        t = t[:a] + blk + t[b:]
    print(f"  heroes.json: {'đổi' if t != t0 else 'đã đúng'}" + (" (chỉ kiểm)" if KIEM and t != t0 else ""))
    if t != t0 and not KIEM:
        open(path, "wb").write(t.encode("utf-8"))
    # cards.json: tên + biểu tượng thẻ của lính (hiệu ứng giữ nguyên)
    path = os.path.join(JSON, "cards.json")
    t = open(path, "rb").read().decode("utf-8")
    t0 = t
    for cid, (ten, icon) in (C.get("the") or {}).items():
        a, b = _khoi(t, "id", cid)
        blk = t[a:b]
        blk = re.sub(r'"name": "[^"]*"', f'"name": "{ten}"', blk, count=1)
        blk = re.sub(r'"icon": "[^"]*"', f'"icon": "{icon}"', blk, count=1)
        t = t[:a] + blk + t[b:]
    print(f"  cards.json: {'đổi' if t != t0 else 'đã đúng'}" + (" (chỉ kiểm)" if KIEM and t != t0 else ""))
    if t != t0 and not KIEM:
        open(path, "wb").write(t.encode("utf-8"))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) == 2 and a[0] == "game":
        game(a[1])
    elif len(a) == 2 and a[0] == "vao":
        vao(a[1])
    else:
        print(__doc__)
