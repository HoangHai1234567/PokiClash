# -*- coding: utf-8 -*-
"""Đo cho HatSat.cs (chiêu mana tinh linh tinh thể sắt, cả hai dạng): mỗi phát (thứ tự phóng) lấy tinh thể ở khung NGAY TRƯỚC lúc ẩn
(t_ban − 1/60 s): tâm (phần của chiều cao game, x về phía trước, y lên), bề rộng / cao ảnh (phần chiều cao game), góc trục x của ảnh và hướng
mũi (độ, 0 = phía trước, 90 = lên), tên ảnh (Resources/<dạng>/<dạng>_tt_<vùng>). In thẳng mảng C#.

    py -3 -I ArtGen/Spine/tinh_sat_do_hat.py 1      (dạng 1; mỗi dạng một lệnh)
    py -3 -I ArtGen/Spine/tinh_sat_do_hat.py 2
"""
import io
import contextlib
import json
import math
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import khung  # noqa: E402


class _Im(io.StringIO):
    """nuốt chữ in của bộ dựng rig (có reconfigure như sys.stdout)."""
    def reconfigure(self, **k):
        pass


def slot_cua_xuong(sk):
    out = {}
    for s in sk.slots:
        att = sk.atts[s["name"]].get(s["att"])
        if att and att.get("verts"):
            nang = {}
            for row in att["verts"]:
                for b, _, _, w in row:
                    nang[b] = nang.get(b, 0.0) + w
            out.setdefault(max(nang, key=nang.get), s["name"])
    return out


def do(R, ten_rig, phong, t_ban0, cach, dich, slot_of, att_of):
    with contextlib.redirect_stdout(_Im()):
        sk, info = R.dung()
        clips = {c.ten: c for c in R.lam_clip(sk, info)}
    H = json.load(open(os.path.join(R.G.BASE, "rig", ten_rig + "_game.json"), encoding="utf-8"))["height"]
    c = clips["cast"]
    rows = []
    for j, b in enumerate(phong):
        t = t_ban0 + j * cach
        P = khung.Pose()
        c.fn(t - 1.0 / 60.0, P)
        W = sk.the_gioi(P)
        s = slot_of(b)
        a = att_of(s)
        spec = sk.atts[s][a]
        V = []
        for row in spec["verts"]:
            q = np.zeros(2)
            for bb, lx, ly, w in row:
                q += w * (W[bb] @ np.array([lx, ly, 1.0]))[:2]
            V.append(q)
        V = np.array(V)                                   # trái dưới, trái trên, phải trên, phải dưới (ảnh)
        ex, ey = V[2] - V[1], V[1] - V[0]
        cen = V.mean(0)
        goc = math.degrees(math.atan2(ex[1], ex[0]))
        mui = math.degrees(math.atan2(dich[1] - cen[1], dich[0] - cen[0]))
        rows.append((t, cen / H, np.hypot(*ex) / H, np.hypot(*ey) / H, goc, mui, a))
    return rows, H


def in_cs(tien_to, rows, anh):
    print(f"// {tien_to}: {len(rows)} phát")
    print(f"static readonly float[] {tien_to}T = {{ " + ", ".join(f"{r[0]:.3f}f" for r in rows) + " };")
    print(f"static readonly Vector2[] {tien_to}P = {{ " + ", ".join(f"new Vector2({r[1][0]:.3f}f, {r[1][1]:.3f}f)" for r in rows) + " };")
    print(f"static readonly Vector2[] {tien_to}S = {{ " + ", ".join(f"new Vector2({r[2]:.3f}f, {r[3]:.3f}f)" for r in rows) + " };")
    print(f"static readonly float[] {tien_to}A = {{ " + ", ".join(f"{r[4]:.0f}f" for r in rows) + " };")
    print(f"static readonly float[] {tien_to}G = {{ " + ", ".join(f"{r[5]:.0f}f" for r in rows) + " };")
    print(f"static readonly int[] {tien_to}K = {{ " + ", ".join(str(anh.index(r[6])) for r in rows) + " };")
    print(f"static readonly string[] {tien_to}Anh = {{ " + ", ".join(f'"{x}"' for x in anh) + " };")


def main(dang):
    """mỗi dạng một tiến trình: tinh_sat.py và tinh_sat_2.py cùng vá biến toàn cục của hoa_ho (con gốc, bộ đệm atlas)."""
    import quai.doi_tinh_sat as DT
    if dang == "1":
        import tinh_sat_rig as R1
        with contextlib.redirect_stdout(_Im()):
            sk1, _ = R1.dung()
        sc1 = slot_cua_xuong(sk1)          # như tinh_sat_rig.lam_clip.slot_cua
        rows1, H1 = do(R1, "tinh_sat_1", R1.PHONG, R1.T_BAN0, R1.BAN_CACH, R1.DICH, lambda b: sc1[b],
                       lambda s: next(x["att"] for x in sk1.slots if x["name"] == s))
        print(f"// dạng 1 (tinh_sat_1, chiều cao khai {H1:.1f}): khung trúng cast = phát đầu {R1.T_BAN0:.2f} s")
        in_cs("Tt1", rows1, DT.TT_1)
    else:
        import tinh_sat_2_rig as R2
        sc2 = {b: v[1] for b, v in R2.TT.items()}
        sc2.update({nb: R2.TT[g][1] + "_b" for nb, g in R2.NHAN.items()})
        rows2, H2 = do(R2, "tinh_sat_2", R2.PHONG, R2.T_BAN0, R2.BAN_CACH, R2.DICH, lambda b: sc2[b], lambda s: s[:-2] if s.endswith("_b") else s)
        print(f"// dạng 2 (tinh_sat_2, chiều cao khai {H2:.1f}): khung trúng cast = phát đầu {R2.T_BAN0:.2f} s")
        in_cs("Tt2", rows2, DT.TT_2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2")
