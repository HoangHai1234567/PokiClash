# -*- coding: utf-8 -*-
"""Đo trên rig Thổ Tinh các điểm mà lớp hạt Assets/01 Script/Game/Battle/HatThoTinh.cs bám (đơn vị = chiều cao tướng game.height; x về
phía đối thủ, y lên; gốc = gốc rig, trùng chân trên sân), in ra khối khởi tạo C# (TtDang) để chép vào HatThoTinh.cs.

    SXS="D:/Ripper/SwordxStaff" py -3 -I ArtGen/Spine/thach_de_do_hat.py                 dạng 2 Thổ Tinh (thach_de_1)
    TH_DANG=non SXS="D:/Ripper/SwordxStaff" py -3 -I ArtGen/Spine/thach_de_do_hat.py     dạng 1 Tiểu Thổ Tinh (thach_de_non)

Đo (rig như bản đã xuất: DICH_RIG = None):
- nam1 / nam2 (attack, giây 0,68): hai nắm đấm (bone96, bone102) so với xương move (sân nắn đỉnh cú lao vào 72 % quãng tới đối thủ);
- mieng (cast, giây 0,30 → 0,95 bước 0,05): bản lề hàm (xương ham) so với chân;
- mảnh bay của chiêu mana (lưỡi trăng / mảnh vỏ), theo THỨ TỰ PHÓNG: idx (số lưỡi i), tach (đế lúc bứt khỏi vành, giây 0,32 + 0,024 i),
  ban / goc / cao / rong: tâm, góc trục đáy → đỉnh ảnh (độ, ngược kim, y lên), cao, rộng của khung ảnh trên rig ngay trước lúc rig ẩn nó
  (T_BAN − 1/60; đo từ khung ảnh thật nên đã gồm tỉ lệ xương của dạng 1);
- hình mảnh bay chuẩn hoá theo khung ảnh (luoi_1 dạng 2, non_vo_1 dạng 1): u = ngang theo bề rộng ảnh (phải +, 0 ở giữa), v từ mép dưới (0)
  tới mép trên (1); mép trái, mép phải từ trên xuống.
"""
import math
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SXS", r"D:\Ripper\SwordxStaff")
import thach_de_rig as R  # noqa: E402
from quai import khung, soi  # noqa: E402


def f3(x):
    return f"{x:.3f}f"


def v2(v):
    return f"new Vector2({f3(v[0])}, {f3(v[1])})"


def vien(path, n=11):
    """đường viền ảnh: mỗi hàng (từ trên xuống) lấy mép trái, mép phải của vùng đặc; (u, v) chuẩn hoá theo khung ảnh."""
    im = np.asarray(Image.open(path).convert("RGBA"))
    a = im[..., 3] > 128
    Hi, Wi = a.shape
    ys = np.where(a.any(axis=1))[0]
    y0, y1 = ys[0], ys[-1]
    trai, phai = [], []
    for k in range(n + 1):
        y = int(round(y0 + (y1 - y0) * k / n))
        xs = np.where(a[y])[0]
        if len(xs) == 0:
            continue
        v = (Hi - 0.5 - y) / Hi
        trai.append(((xs[0] - Wi / 2) / Wi, v))
        phai.append(((xs[-1] + 1 - Wi / 2) / Wi, v))
    return trai, phai


def main():
    sk, info, clips, frames = R.dung_het()
    cao = info["cao"]
    cl = {c.ten: c for c in clips}
    ve0 = soi.Ve(sk)
    ten = "dạng 1 Tiểu Thổ Tinh (thach_de_non)" if R.NON else "dạng 2 Thổ Tinh (thach_de_1)"
    print(f"// {ten}: cao {cao:.1f}")

    def P_at(clip, t):
        P = khung.Pose()
        cl[clip].fn(t, P)
        return P

    def pt(W, b):
        return W[b][:2, 2]

    W = sk.the_gioi(P_at("attack", 0.68))
    mv = pt(W, "move")
    a, b = (pt(W, "bone96") - mv) / cao, (pt(W, "bone102") - mv) / cao
    rows = [pt(sk.the_gioi(P_at("cast", 0.30 + 0.05 * k)), "ham") / cao for k in range(14)]

    c = info["cast"]
    T_BAN = c["T_BAN"]
    thu = sorted(T_BAN, key=lambda i: T_BAN[i])
    gai = {g["i"]: g for g in sk.info["gai"]}
    idx, tach, ban, goc, hh, ww = [], [], [], [], [], []
    for i in thu:
        idx.append(i)
        tach.append(pt(sk.the_gioi(P_at("cast", 0.32 + 0.024 * i)), f"gai_{i}") / cao)
        P = P_at("cast", T_BAN[i] - 1.0 / 60)
        items, _ = ve0.skin(P)
        Vq = [x[2] for x in items if x[0] == gai[i]["slot"]]
        if not Vq:
            raise SystemExit(f"không thấy khung ảnh của lưỡi {i}")
        V = Vq[0]                                        # TL, TR, BR, BL
        top, bot = 0.5 * (V[0] + V[1]), 0.5 * (V[3] + V[2])
        up = top - bot
        ban.append(V.mean(axis=0) / cao)
        goc.append(math.degrees(math.atan2(up[1], up[0])))
        hh.append(float(np.hypot(*up)) / cao)
        ww.append(float(np.hypot(*(V[1] - V[0]))) / cao)
    print(f"// thứ tự phóng {thu}; T_BAN {[round(T_BAN[i], 3) for i in thu]}; bay {c['BAY']:.2f}")
    anh = R.p_anh("non_vo_1" if R.NON else "luoi_1")
    trai, phai = vien(anh, 20 if R.NON else 11)
    print("{")
    print(f"    nam1 = {v2(a)}, nam2 = {v2(b)},")
    print("    mieng = new[]")
    print("    {")
    for i in range(0, len(rows), 4):
        print("        " + ", ".join(v2(v) for v in rows[i:i + 4]) + ",")
    print("    },")
    print("    idx = new[] { " + ", ".join(str(i) for i in idx) + " },")
    print("    tach = new[] { " + ", ".join(v2(v) for v in tach) + " },")
    print("    ban = new[] { " + ", ".join(v2(v) for v in ban) + " },")
    print("    goc = new[] { " + ", ".join(f"{g:.1f}f" for g in goc) + " },")
    print("    cao = new[] { " + ", ".join(f3(x) for x in hh) + " },")
    print("    rong = new[] { " + ", ".join(f3(x) for x in ww) + " },")
    print(f"    // hình: {os.path.basename(anh)}")
    print("    trai = new[] { " + ", ".join(v2(p) for p in trai) + " },")
    print("    phai = new[] { " + ", ".join(v2(p) for p in phai) + " },")
    print("}")


if __name__ == "__main__":
    main()
