# -*- coding: utf-8 -*-
"""Rùa golem lửa DẠNG 1 (rùa non; người dùng 2026-11-13: "con này 2 dạng thôi, làm dạng 1 nữa nhưng hình như gpt hết token rồi").

Cùng rig, cùng clip với dạng 2 (rua_lua_1). Codex hết hạn mức tới 18:30 nên dạng 1 dựng KHÔNG cần gen: xếp lại MẢNH dạng 2 đã cắt
(inbox/rua_lua_1/manh, toạ độ khung concept) ở tỉ lệ rùa non: đầu phóng quanh chỗ nối cổ, hai sừng co về gốc sừng (mầm sừng), cụm cột đá
co về chân cột, ngọn lửa co quanh gốc lửa, bỏ bớt ngọn lửa / cột đá. Mỗi hướng ra một thư mục mảnh riêng, rig dựng bằng chính
rua_lua_rig.py (biến môi trường RL_NON=<hướng>). Các hướng là ĐỀ XUẤT của Claude, chờ người dùng chọn.

    rua_lua_non.py manh [hướng|all]   → inbox/rua_lua_non/manh_<hướng>/ (ảnh mảnh + dat.json)
    rua_lua_non.py so                 → inbox/rua_lua_non/so_dang.jpg (dáng đứng từng hướng cạnh dạng 2, cùng tỉ lệ cỡ trong game)
"""
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NGUON = os.path.join(HERE, "inbox", "rua_lua_1", "manh")
RA = os.path.join(HERE, "inbox", "rua_lua_non")
DAU = ["hong", "ham", "mat_so", "mat_tat", "sung_gan", "sung_xa"]
TAM_DAU = (935, 715)          # chỗ đầu nối vào cổ trên khung concept: tâm phóng của cả đầu
MIENG = (1088, 812)           # như rua_lua_rig.MIENG (dạng 2)
LUA = ["lua_sung", "lua_duoi", "lua_trai", "lua_giua_trai", "lua_cao", "lua_phai", "lua_nho"]
# neo co của từng mảnh (phần của khung mảnh): gốc sừng, chân cột
NEO = {"sung_gan": (0.30, 0.80), "sung_xa": (0.22, 0.90), "cot_gan": (0.50, 0.86), "cot_xa": (0.5, 1.0)}

HUONG = {
    # A: rùa non mới nhú lửa: sừng là hai mầm ngắn, ba ngọn lửa nhỏ, cụm cột đá thấp, không có cột đá xa
    "mam_lua": dict(ten="A · mầm lửa: sừng mầm ngắn, ba ngọn lửa nhỏ, cột đá thấp", dau=1.10, sung=0.52, cot=0.72,
                    bo=["cot_xa", "lua_sung", "lua_duoi", "lua_giua_trai", "lua_nho"], lua={"lua_cao": 0.55, "lua_trai": 0.50, "lua_phai": 0.55}),
    # B: đủ bảy ngọn lửa nhưng nhỏ, sừng dài hơn A một chút
    "du_lua": dict(ten="B · đủ lửa nhỏ: sừng ngắn, đủ bảy ngọn lửa nhỏ", dau=1.10, sung=0.62, cot=0.80, bo=["cot_xa"],
                   lua={k: 0.58 for k in LUA}),
    # C: đầu to hẳn (non nhất), sừng mầm, chỉ một ngọn lửa giữa lưng
    "dau_to": dict(ten="C · đầu to: đầu to hơn hẳn, sừng mầm, một ngọn lửa giữa lưng", dau=1.20, sung=0.45, cot=0.66,
                   bo=["cot_xa", "lua_sung", "lua_duoi", "lua_giua_trai", "lua_nho", "lua_trai", "lua_phai"], lua={"lua_cao": 0.62}),
    # người dùng xem A, B, C (2026-11-13): "tôi muốn chi bi hơn, nhỏ hơn nữa" → đầu to hẳn so với thân (phóng quanh điểm thấp gần mõm để
    # đầu nở lên trên, hàm không chạm đất), sừng chỉ còn mầm, cả con nhỏ hơn trong game (cỡ 0,78 thay 0,92)
    "chibi": dict(ten="D · chibi: đầu rất to, sừng mầm, ba ngọn lửa nhỏ, cả con nhỏ hơn", dau=1.38, tam_dau=(950, 800), sung=0.40, cot=0.60,
                  bo=["cot_xa", "lua_sung", "lua_duoi", "lua_giua_trai", "lua_nho"], lua={"lua_cao": 0.50, "lua_trai": 0.44, "lua_phai": 0.48},
                  co=0.78),
    "chibi_1": dict(ten="E · chibi một lửa: đầu rất to, sừng mầm, một ngọn lửa, cả con nhỏ hơn", dau=1.38, tam_dau=(950, 800), sung=0.40,
                    cot=0.60, bo=["cot_xa", "lua_sung", "lua_duoi", "lua_giua_trai", "lua_nho", "lua_trai", "lua_phai"], lua={"lua_cao": 0.58},
                    co=0.78),
}
CO = 0.92                     # cỡ dạng 1 trong game khi hướng không ghi `co`


def co(im, goc, s, tam):
    """co / phóng ảnh mảnh quanh điểm tam (khung concept)."""
    if abs(s - 1) < 1e-6:
        return im, goc
    w, h = max(2, round(im.width * s)), max(2, round(im.height * s))
    im2 = im.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")
    return im2, (int(round(tam[0] + (goc[0] - tam[0]) * s)), int(round(tam[1] + (goc[1] - tam[1]) * s)))


def manh(huong):
    C = HUONG[huong]
    tam_dau = C.get("tam_dau", TAM_DAU)
    D = json.load(open(os.path.join(NGUON, "dat.json"), encoding="utf-8"))
    ra = os.path.join(RA, f"manh_{huong}")
    if os.path.isdir(ra):
        shutil.rmtree(ra)
    os.makedirs(ra)
    out = {}
    thu_tu = [t for t in D["_thu_tu"] if t not in C["bo"]]
    for t in thu_tu:
        d = dict(D[t])
        im = Image.open(os.path.join(NGUON, t + ".png")).convert("RGBA")
        goc = tuple(d["goc"])
        if t in DAU:
            im, goc = co(im, goc, C["dau"], tam_dau)
        if t in ("sung_gan", "sung_xa"):
            nx, ny = NEO[t]
            im, goc = co(im, goc, C["sung"], (goc[0] + nx * im.width, goc[1] + ny * im.height))
        if t == "cot_gan":
            nx, ny = NEO[t]
            im, goc = co(im, goc, C["cot"], (goc[0] + nx * im.width, goc[1] + ny * im.height))
        if t in C["lua"]:
            im, goc = co(im, goc, C["lua"][t], tuple(d["goc_lua"]))
        im.save(os.path.join(ra, t + ".png"))
        d["goc"], d["co"] = [int(goc[0]), int(goc[1])], [im.width, im.height]
        out[t] = d
        if t == "sung_gan":                      # mũi sừng mới: điểm cao nhất của mảnh sừng gần (chỗ tụ cầu lửa của chiêu cuối)
            a = np.asarray(im)[..., 3] > 128
            ys, xs = np.nonzero(a)
            k = int(np.argmin(ys))
            out["_sung_mui"] = [int(goc[0] + xs[ys == ys[k]].mean()), int(goc[1] + ys[k] + 6)]
    out["_mieng"] = [int(round(tam_dau[0] + (MIENG[0] - tam_dau[0]) * C["dau"])), int(round(tam_dau[1] + (MIENG[1] - tam_dau[1]) * C["dau"]))]
    out["_thu_tu"] = thu_tu
    json.dump(out, open(os.path.join(ra, "dat.json"), "w", encoding="utf-8"), indent=1)
    print(huong, len(thu_tu), "mảnh ->", ra, "mũi sừng", out["_sung_mui"], "mõm", out["_mieng"])


def so():
    """dáng đứng (khung 0 idle) từng hướng cạnh dạng 2, theo cỡ trong game của dòng hai dạng (0,92 / 1,1)."""
    import io
    import contextlib
    import importlib
    from quai import soi
    ims = []
    for h in [None] + (sys.argv[2].split(",") if len(sys.argv) > 2 else list(HUONG)):
        if h:
            os.environ["RL_NON"] = h
        else:
            os.environ.pop("RL_NON", None)
        import rua_lua_rig as R
        R = importlib.reload(R)
        with contextlib.redirect_stdout(io.StringIO()):
            sk, info = R.dung()
            clips = R.lam_clip(sk, info)
        from quai import hoat
        fr = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.03)
        ti = (1.1 if h is None else HUONG[h].get("co", CO)) / info["cao"] * 420       # cùng thước: 420 px = chiều cao game × cỡ 1
        ims.append((HUONG[h]["ten"].split(":")[0] if h else "Dạng 2 (đã có)", ve.ve(fr[0], Bx, ti, bg=(250, 247, 240), ss=2).convert("RGB")))
    from PIL import ImageDraw, ImageFont
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    Hm = max(i.height for _, i in ims)
    W = sum(i.width for _, i in ims) + 20 * (len(ims) + 1)
    o = Image.new("RGB", (W, Hm + 60), (250, 247, 240))
    d = ImageDraw.Draw(o)
    x = 20
    for ten, im in ims:
        o.paste(im, (x, 50 + Hm - im.height))
        d.text((x, 12), ten, fill=(43, 33, 24), font=F)
        x += im.width + 20
    p = os.path.join(RA, "so_dang.jpg")
    o.save(p, quality=90)
    print(p, o.size)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "manh":
        hs = sys.argv[2] if len(sys.argv) > 2 else "all"
        for h in (HUONG if hs == "all" else [hs]):
            manh(h)
    elif cmd == "so":
        so()
    else:
        print(__doc__)
