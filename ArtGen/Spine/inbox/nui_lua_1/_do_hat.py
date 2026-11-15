# -*- coding: utf-8 -*-
"""Đo cho HatNuiLua.cs: miệng từng ống lúc bắn (phần của chiều cao game, x về phía trước, y lên) + hướng ống (độ, 0 = phía trước, 90 = lên),
theo thứ tự bắn BAN; đầu (chỗ húc) lúc trúng của attack; miệng lúc tụ / nhả của cast. Chạy: NL_GOC=1 py -3 -I inbox/nui_lua_1/_do_hat.py"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
import nui_lua_rig as R
from quai import hoat
sk, info = R.dung()
clips = {c.ten: c for c in R.lam_clip(sk, info, 1015.0)}
ra = os.path.join(HERE, "..", R.MA_NON, "rig") if R.CHIBI else os.path.join(R.G.BASE, "rig_goc" if R.GOC else "rig")
H = json.load(open(os.path.join(ra, R.TEN_RIG + "_game.json"), encoding="utf-8"))["height"]
fr = hoat.nuong(sk, clips["skill"])
def w(P, b):
    M = sk.the_gioi(P)[b]
    return M[0, 2] / H, M[1, 2] / H, math.degrees(math.atan2(M[1, 0], M[0, 0]))
print("H", H)
ps, gs = [], []
for i, nn in enumerate(R.BAN):
    t = R.T_BAN0 + i * R.BAN_CACH
    x, y, g = w(fr[int(round(t * 30))], "ong_" + nn)
    ps.append(f"new Vector2({x:.3f}f, {y:.3f}f)"); gs.append(f"{g:.0f}f")
print("OngP = { " + ", ".join(ps) + " };")
print("OngG = { " + ", ".join(gs) + " };")
P0 = hoat.nuong(sk, clips["idle"])[0]
print("idle:", " ".join(f"{nn}=({w(P0, 'ong_' + nn)[0]:.3f},{w(P0, 'ong_' + nn)[1]:.3f})" for nn in R.KHOI))
fa = hoat.nuong(sk, clips["attack"])
print("attack mieng @trung:", ["%.3f" % v for v in w(fa[int(round(R.T_HUC * 30))], "mieng")])
fc = hoat.nuong(sk, clips["cast"])
for t in (R.T_TU, 0.6, R.T_NHA):
    print("cast mieng @%.2f:" % t, ["%.3f" % v for v in w(fc[int(round(t * 30))], "mieng")])
print("mốc: be", R.T_BE, "ban0", R.T_BAN0, "cach", R.BAN_CACH, "het", round(R.T_HET, 3), "dai", round(R.D_SKILL, 3), "tu", R.T_TU, "nha", R.T_NHA, "huc", R.T_HUC)
