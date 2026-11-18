# -*- coding: utf-8 -*-
"""Đo trên rig Thiên Thạch Thú các điểm mà lớp hạt Assets/01 Script/Game/Battle/HatThach.cs bám (đơn vị = chiều cao tướng game.height; x về
phía đối thủ, y lên; gốc = chân), in ra mảng C# để chép vào HatThach.cs. Hai dạng là hai rig (dạng 1 tinh_hach_non, dạng 2 tinh_hach_1).

    py -3 -I ArtGen/Spine/tinh_hach_do_hat.py           dạng 2 (đối chiếu bảng đang có trong HatThach.cs)
    TH_DANG=non py -3 -I ArtGen/Spine/tinh_hach_do_hat.py   dạng 1

Đo: Tay = giữa hai bàn tay đang xoa (cast, T_XOA1 − 0,05; như TAY_F của rig); Tu = điểm thiên thạch xoáy về (F_TU); S0[j] = chỗ bản sao j
rời đi (cho_phong lúc phóng); Cau[i] (giờ 0,05 i của skill) = (phần cú lao của move, tâm quả cầu − move theo x, theo y): phần cú lao chia
theo cùng hệ số với bảng dạng 2 (move.x lúc nổ ↔ 1,154; clip skill hai dạng cùng đường cong, chỉ nhân chiều cao); RCau = bán kính quả cầu.
"""
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tinh_hach_rig as R  # noqa: E402
from quai import hoat  # noqa: E402

X_NO_D2 = 1.154                      # phần cú lao lúc nổ trong bảng ThtCau của dạng 2


def main():
    sk, info, clips, cao = R.dung_het()
    _, than_cast, cho_phong = R.lam_clip(sk, info, cao)
    from quai import khung
    Qf = khung.Pose()
    than_cast(R.T_XOA1 - 0.05, Qf)
    Wf = sk.the_gioi(Qf)
    tay = 0.5 * ((Wf["xiaobi_r2"] @ np.array([120.0, 0.0, 1.0]))[:2] + (Wf["shouzhang_l"] @ np.array([90.0, 0.0, 1.0]))[:2])
    tu = tay + np.array([0.20 * cao, 0.04 * cao])
    nq = len(sk.info["quy"])
    s0 = [cho_phong(R.T_PHONG[j], j) / cao for j in range(nq)]
    c = [x for x in clips if x.ten == "skill"][0]
    fr = hoat.nuong(sk, c)
    Wl = [sk.the_gioi(P) for P in fr]
    mx = lambda i: float(Wl[i]["move"][0, 2])  # noqa: E731
    k_lao = mx(int(round(R.T_NO * 30))) / X_NO_D2
    rows = []
    for i in range(int(round(R.T_VE / 0.05)) + 1):
        f = min(len(fr) - 1, int(round(i * 0.05 * 30)))
        b = Wl[f]["bong_q"][:2, 2] - Wl[f]["move"][:2, 2]
        rows.append((mx(f) / k_lao, b[0] / cao, b[1] / cao))
    D = sk.info.get("D_BONG", 0.0)
    v2 = lambda v: f"new Vector2({v[0]:.3f}f, {v[1]:.3f}f)"  # noqa: E731
    print(f"// {R.TEN_RIG}: cao {cao:.1f}, {nq} thiên thạch, quả cầu Ø {D:.0f}")
    print(f"Tay = {v2(tay / cao)}; Tu = {v2(tu / cao)}; RCau = {D / 2 / cao:.3f}f")
    print("S0 = { " + ", ".join(v2(v) for v in s0) + " }")
    print("Cau = {")
    for i in range(0, len(rows), 4):
        print("    " + ", ".join(f"new Vector3({a:.3f}f, {b:.3f}f, {z:.3f}f)" for a, b, z in rows[i:i + 4]) + ",")
    print("}")


if __name__ == "__main__":
    main()
