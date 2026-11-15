# đo số cho HatRua.cs (SungPNon, LuaNon): mũi sừng `cau` theo giây và giữa ngọn lửa lúc bắt đầu bị hút, phần của chiều cao game
import sys, os, io, contextlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import numpy as np
import rua_lua_rig as R
from quai import hoat
with contextlib.redirect_stdout(io.StringIO()):
    sk, info = R.dung()
    clips = R.lam_clip(sk, info)
cao = info["cao"]
fr = hoat.nuong(sk, [c for c in clips if c.ten == "skill"][0])
T = [0, 0.30, 1.37, 1.50, 1.57, 1.60, 1.63, 1.80]
out = []
for t in T:
    W = sk.the_gioi(fr[min(len(fr) - 1, round(t * 30))])
    p = W["cau"][:2, 2] / cao
    out.append(f"new Vector2({p[0]:.3f}f, {p[1]:.3f}f)")
print("RL_NON =", R.NON, "| cao", round(cao, 1))
print("SungPNon:", ", ".join(out))
W = sk.the_gioi(fr[round(0.32 * 30)])
for l in info["lua"]:
    g, n = W[l + "_g"][:2, 2] / cao, W[l + "_2"][:2, 2] / cao
    m = (g + n) / 2
    print(f"LuaNon {l}: gốc ({g[0]:.3f}, {g[1]:.3f}) ngọn-đốt-cuối ({n[0]:.3f}, {n[1]:.3f}) giữa new Vector2({m[0]:.2f}f, {m[1]:.2f}f)")
fc = hoat.nuong(sk, [c for c in clips if c.ten == "cast"][0])
W = sk.the_gioi(fc[round(0.90 * 30)])
p = W["mieng"][:2, 2] / cao
print(f"mõm lúc phun (cast 0,90 s): ({p[0]:.3f}, {p[1]:.3f})")
