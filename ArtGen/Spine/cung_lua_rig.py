# -*- coding: utf-8 -*-
"""Quỷ lửa bắn cung (cung_lua, tướng thứ 3 đảo Hỏa): RESKIN đúng nghĩa trên rig con gốc monster_3357 (hiệp sĩ cung thủ).

Người dùng 2026-11-13: "xem con gốc tách như nào thì mình tách và gen như thế". →
- Xương: đủ mọi xương của họ, dáng gốc = khung 0 idle_01 (biến đổi riêng `l` đã áp ràng buộc, lấy mẫu bằng runtime Spine thật).
- Hình: MỖI hình của họ một hình của mình, NGUYÊN lưới của họ (đỉnh, tam giác, uv, trọng số; điểm gắn tính bằng ma trận dáng gốc đã áp ràng
  buộc trong att_goc.json), ảnh là mảnh reskin vẽ trên đúng khung ảnh vùng (cung_lua_da.py). Riêng vòm sau mũ `to_01` nới khung lên trên
  cho hai sừng (ô cứng trên xương đầu bone3b; lưới gốc bám bone3b 0,98).
- Thứ tự vẽ: của họ. Họ đổi thứ tự lúc giương cung (dây, cung, hai lớp bàn tay xa, mũi tên ra trước thân); .atomik không đổi thứ tự theo
  clip nên năm slot đó có thêm bản `_t` ở chỗ mới, bật theo thứ tự vẽ từng khung của họ.
- Clip: idle, walk, hit = của họ. attack = skill_01 của họ + mũi tên bay. cast, skill, appear, die: theo lời tả của người dùng, dựng trên
  chính bộ xương này (nền là dáng lấy mẫu của skill_01 / idle / hit).
- Mũi tên bay tới đối thủ: `bay_k` trên `ten_k` con của `fly_k` (game dời `far`, co quãng, xoay theo véc-tơ bay). Vệt lửa, tụ lửa, nổ: VFX.

    cung_lua_rig.py                          dựng, xuất inbox/cung_lua_1/rig/
    cung_lua_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    cung_lua_rig.py kiem                     góc nhảy lớn nhất giữa hai khung của từng clip
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, hoat, xuat, soi  # noqa: E402
from quai.khung import Sk, mat, goc_mat, Pose  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.luoi import Luoi  # noqa: E402
import cung_lua as G  # noqa: E402

DANG = os.environ.get("CL_DANG") or "lon"                # "lon" = dạng 2 (bám con gốc); "non" = dạng 1, cùng xương / lưới / clip, đổi tỉ lệ + da
TEN = os.environ.get("CL_TEN") or ("cung_lua_1" if DANG == "non" else "cung_lua_2")          # dạng 2 (dạng lớn, bám con gốc) của dòng; dạng 1 (non) làm sau trên cùng rig
RA = os.path.join(G.BASE, "non", "rig") if DANG == "non" else os.path.join(G.BASE, "rig")
MANH = os.environ.get("CL_MANH") or (os.path.join(G.BASE, "non", "manh") if DANG == "non" else os.path.join(G.BASE, "manh"))
if DANG == "non" and not os.path.isdir(MANH):
    MANH = os.path.join(G.BASE, "manh")                 # chưa có da dạng non: dựng bố cục bằng da dạng lớn
# DẠNG NON: tỉ lệ đổi ở xương GỐC của chuỗi (xương con thừa hưởng, mảnh co / phóng quanh khớp, gốc vẫn dính). Không đụng tay, chân,
# cung (tay kéo dây treo dưới xương dây cung; chân có điểm chạm đất).
TI_LE = {"bone3": 1.17, "bone4": 0.70} if DANG == "non" else {}     # bone3 = cổ → cả đầu + chùm lửa; bone4 = gốc chùm lửa trên mũ
RA = os.environ.get("CL_RA") or RA
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
SUNG_NOI = 0.62               # như cung_lua_da.py
DOI = ("gongjian_02", "gongjian_01", "youshou_01", "youshou_02", "jian")      # slot có bản _t (thứ tự vẽ lúc giương cung)
XOE = 9.0                     # độ xoè hai mũi tên phụ của chiêu mana
NANG_DAI = 1.45               # mũi tên lửa của chiêu cuối: dài gấp chừng này mũi tên thường (đuôi tì dây → mũi)
NANG_PX = 1.5                 # px atlas cho mỗi đơn vị
GIU_DICH = 0.4                # sau khi tới đích, xương mũi tên bay ở lại đích (đã ẩn) chừng này giây
TRE_TRUNG = 0.012             # khung "trúng" đặt SAU khung mũi tên tắt hẳn chừng này: game GIỮ dáng ở khung trúng (HoldOf ~0,3 s, khựng),
#                               trúng rơi vào giữa hai khoá thì mũi tên hiện mờ lơ lửng trước mặt (thấy trong game 2026-11-13). Vì vậy
#                               giờ buông và quãng bay đều là bội của 1 / FPS: khung tên tới đích trùng một khung mẫu.
N_LUA = 5                     # số cặp lưỡi lửa (trên / dưới) dọc thân mũi tên lửa
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung, đã áp ràng buộc)
def _cd():
    out = {}
    ix, ic, ij, iv = SL.index("xiong"), SL.index("gongjian_01"), SL.index("jian"), SL.index("zuojianjia")
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(I["bones"]):
            if b0["name"] == "root":
                continue
            z = L0[i]
            Am = np.array([[F["l"][i][2] - z[2], F["l"][i][0] - z[0], F["l"][i][1] - z[1],
                            F["l"][i][3] / (z[3] or 1.0), F["l"][i][4] / (z[4] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[b0["name"]] = Am
        truoc = [(F["o"].index(ic) > F["o"].index(ix), F["o"].index(ij) > F["o"].index(iv)) for F in fr]     # (cung trước ngực?, tên trước vai gần?)
        hien = [[(F["n"][k] is not None) * float(F["a"][k]) for k in range(len(SL))] for F in fr]
        out[clip] = (float(v["dur"]), res, truoc, hien)
    return out


CD = _cd()


def mau(clip, t, lap=False):
    dur, R, _, _ = CD[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    out = {}
    for b, arr in R.items():
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        out[b] = arr[i0] * (1 - w) + arr[i1] * w
    return out


def khung_ho(clip, t, lap=False):
    dur = CD[clip][0]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    return min(len(CD[clip][2]) - 1, int(round(x)))


def pha(a, b, w):
    out = {}
    for k in set(a) | set(b):
        va = a.get(k, np.array([0, 0, 0, 1, 1.0]))
        vb = b.get(k, np.array([0, 0, 0, 1, 1.0]))
        out[k] = va * (1 - w) + vb * w
    return out


def dat(P, d):
    for b, v in d.items():
        if abs(v[0]) > 1e-5:
            P.rot(b, float(v[0]))
        if abs(v[1]) > 1e-5 or abs(v[2]) > 1e-5:
            P.move(b, float(v[1]), float(v[2]))
        if abs(v[3] - 1) > 1e-6 or abs(v[4] - 1) > 1e-6:
            P.scale(b, float(v[3]), float(v[4]))


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def hien_theo_ho(P, clip, t, lap=False):
    """độ đậm mọi slot theo khung của họ; năm slot đổi thứ tự vẽ thì bật bản gốc hay bản _t theo thứ tự vẽ của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    _, _, truoc, hien = CD[clip]
    tc, tj = truoc[i]
    for k, sl in enumerate(SL):
        if sl == "shadow":
            continue
        a = 1.0 if hien[i][k] > 0.5 else 0.0
        if sl in DOI:
            tr = tj if sl == "jian" else tc
            P.alpha[sl] = 0.0 if tr else a
            P.alpha[sl + "_t"] = a if tr else 0.0
        else:
            P.alpha[sl] = a


# ---------------------------------------------------------------- dựng
def dung():
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    for i, b in enumerate(I["bones"]):
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        z = L0[i]
        k_ = TI_LE.get(b["name"], 1.0)
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1], goc=z[2], dai=b["len"], sx=z[3] * k_, sy=z[4] * k_)
    Wi = sk.the_gioi()                        # dáng gốc của mình = khung 0 idle của họ
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hien0 = {SL[k]: v > 0.5 for k, v in enumerate(CD["idle_01"][3][0])}
    by = {a["slot"]: a for a in AG["atts"]}
    IM = {}

    def anh_cua(r):
        if r not in IM:
            g = Image.open(os.path.join(MANH, r + ".png")).convert("RGBA")
            IM[r] = anh.loang_mau(g)
            sk.anh(r, IM[r])
        return IM[r]

    def hang(a, xy):
        """[(xương, x, y riêng, trọng số)...] mỗi đỉnh: điểm gắn theo ma trận DÁNG GỐC của họ (att_goc), như lưới gốc."""
        ws = a.get("w")
        rows, V0 = [], []
        for i, p in enumerate(xy):
            lst = [(NB[b], w) for b, w in ws[i] if w > 0] if ws else [(a["bone"], 1.0)]
            tong = sum(w for _, w in lst)
            row, v0 = [], np.zeros(2)
            for bn, w in lst:
                bn2 = "move" if bn == "root" else bn
                lp = np.linalg.solve(WG[bn], np.array([p[0], p[1], 1.0]))
                row.append((bn2, float(lp[0]), float(lp[1]), float(w / tong)))
                v0 += w / tong * (Wi[bn2] @ np.array([lp[0], lp[1], 1.0]))[:2]
            rows.append(row)
            V0.append(v0)
        return rows, np.array(V0)

    def gan(slot_ten, a, an, bien=None, ten_hinh=None):
        """hình của mình trong slot_ten = NGUYÊN lưới của hình a của họ + ảnh reskin cùng vùng. bien(xy) → xy: nắn đỉnh (thế giới dáng gốc)
        cho bản sao (mũi tên xoè, mũi tên nặng)."""
        r = a["region"]
        im = anh_cua(r)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        if r == "to_01":                       # vòm sau mũ + hai sừng: ô cứng cả khung đã nới, bám xương đầu
            noi = int(round(hr * SUNG_NOI))
            M, *_ = np.linalg.lstsq(np.c_[uv_px, np.ones(len(uv_px))], xy, rcond=None)
            uv_px = np.array([[0, -noi], [wr, -noi], [wr, hr], [0, hr]], float)
            xy = np.c_[uv_px, np.ones(4)] @ M
            tris = np.array([[0, 1, 2], [0, 2, 3]])
            a = dict(a, w=None, bone="bone3b")
            uv = (uv_px + np.array([0, noi])) / np.array([wr, hr + noi], float)
        else:
            uv = uv_px / np.array([wr, hr], float)
        if bien is not None:
            xy = bien(xy)
        rows, V0 = hang(a, xy)
        ten_hinh = ten_hinh or r
        sk.slot(slot_ten, rows[0][0][0], ten_hinh, an=an)
        sk.atts[slot_ten][ten_hinh] = {"type": "mesh", "path": r, "uv": uv, "tris": np.asarray(tris, int).reshape(-1, 3), "hull": len(uv),
                                       "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_hinh)] = Luoi(uv * np.array([im.width, im.height], float), np.asarray(tris, int).reshape(-1, 3), len(uv), len(uv),
                                             im.width, im.height, ten=slot_ten)
        return V0

    # mũi tên đang kéo trên dây (jian4): đuôi tên D4 (thế giới dáng gốc của họ) để xoè hai mũi phụ và phóng to mũi tên nặng
    a4 = by["jian4"]
    uv4, _ = G.luoi(a4)
    xy4 = np.array(a4["xy"], float).reshape(-1, 2)
    M4, *_ = np.linalg.lstsq(np.c_[uv4, np.ones(len(uv4))], xy4, rcond=None)
    al = np.asarray(imgs_ho["jian"].convert("RGBA"))[..., 3] > 100
    ys, xs = np.nonzero(al)
    duoi_px = np.array([xs.min(), ys[xs == xs.min()].mean()], float)
    mui_px = np.array([xs.max(), ys[xs == xs.max()].mean()], float)
    D4 = np.array([*duoi_px, 1.0]) @ M4
    T4 = np.array([*mui_px, 1.0]) @ M4

    info_nang = {}

    def quay_quanh(c, goc, k=1.0):
        c_, s_ = math.cos(math.radians(goc)), math.sin(math.radians(goc))
        Rm = np.array([[c_, -s_], [s_, c_]]) * k
        return lambda xy: (xy - c) @ Rm.T + c

    # ---- slot theo thứ tự vẽ của họ (sau → trước) + bản _t của năm slot đổi thứ tự lúc giương cung
    for a in sorted(AG["atts"], key=lambda q: q["order"]):
        s_ = a["slot"]
        if s_ == "jian4":
            continue                           # jian4 chỉ hiện lúc đã giương cung: đặt luôn ở chỗ mới (sau tấm vai gần)
        gan(s_, a, an=not hien0[s_])
        if s_ == "jian6":
            gan("gongjian_02_t", by["gongjian_02"], an=True)
        elif s_ == "jian3":
            gan("gongjian_01_t", by["gongjian_01"], an=True)
        elif s_ == "zuojianjia":
            lp = np.linalg.solve(WG[a4["bone"]], np.array([*D4, 1.0]))            # đuôi tên trong hệ xương mũi tên đang kéo
            for nm in ("xoe_a", "xoe_b"):
                sk.xuong(nm, a4["bone"], float(lp[0]), float(lp[1]))
                WG[nm] = WG[a4["bone"]] @ mat(float(lp[0]), float(lp[1]), 0.0)
            Wi = sk.the_gioi()
            for nm, g in (("xoe_a", XOE), ("xoe_b", -XOE)):
                gan("jian4" + nm[-1], dict(a4, bone=nm), an=True, bien=quay_quanh(D4, g))
            gan("jian4", a4, an=True)
            # MŨI TÊN LỬA NĂNG LƯỢNG của chiêu cuối (người dùng: "1 mũi tên lửa năng lực rực cháy, khác với mũi tên thường", rồi "nên làm
            # animation cho riêng nó, lửa cháy liên tục"): MỘT lưới 22 × 8 trên xương ten_3 (con của fly_3: lúc trên dây clip đặt nó theo đuôi
            # tên tì dây, lúc bay game lái tới đối thủ). Lõi thân bám cứng ten_3; mỗi lưỡi lửa trên / dưới thân bám một xương riêng gốc ở
            # thân tên (l_t*, l_d*), đuôi lửa bám l_duoi, đầu tên bám l_dau: clip cho các xương đó phập phồng, lay lệch pha → lửa cháy liên tục.
            sk.xuong("fly_3", "root", 0.0, 0.0)
            sk.xuong("ten_3", "fly_3", 0.0, 0.0)
            mt = json.load(open(os.path.join(MANH, "ten_lua.json")))
            g = Image.open(os.path.join(MANH, "ten_lua.png")).convert("RGBA")
            dai = NANG_DAI * float(np.hypot(*(T4 - D4)))                           # đuôi tì dây → mũi (đơn vị thế giới)
            k = dai / (mt["mui"][0] - mt["nock"][0])                                 # đơn vị cho mỗi px ảnh gen
            iml = anh.loang_mau(g.resize((max(2, round(g.width * k * NANG_PX)), max(2, round(g.height * k * NANG_PX))), Image.LANCZOS))
            sk.anh("ten_lua", iml)
            xt = mt["nock"][0] * k                                                   # bề dài phần đuôi lửa sau chỗ tì dây
            cao_l = g.height * k
            xs_seg = np.linspace(0.10 * dai, 0.70 * dai, N_LUA)
            x_dau = 0.82 * dai
            sk.xuong("l_duoi", "ten_3", 0.0, 0.0)
            for i_, x_ in enumerate(xs_seg):
                sk.xuong(f"l_t{i_}", "ten_3", float(x_), 0.0)
                sk.xuong(f"l_d{i_}", "ten_3", float(x_), 0.0)
            sk.xuong("l_dau", "ten_3", float(x_dau), 0.0)
            from quai.luoi import luoi_o
            Lf = luoi_o(iml.width, iml.height, 22, 8)
            Vf, Wf = [], []
            for q_ in Lf.pts:
                X = (q_[0] / iml.width * g.width - mt["nock"][0]) * k              # hệ riêng của mũi tên: gốc ở đuôi tì dây, +x về mũi, y lên
                Y = -(q_[1] / iml.height * g.height - mt["nock"][1]) * k
                Vf.append((X, Y))
                wc = math.exp(-(abs(Y) / (0.09 * cao_l)) ** 2)                       # lõi thân: cứng
                ph = "l_t" if Y >= 0 else "l_d"
                d = {}
                if X < 0:                                                            # đuôi lửa: cả mảng lay theo l_duoi (lõi cứng dần về chỗ tì dây)
                    f = min(1.0, -X / (0.45 * xt))
                    d["ten_3"] = wc * (1 - f)
                    d["l_duoi"] = 1 - wc * (1 - f)
                else:
                    d["ten_3"] = wc
                    r_ = 1 - wc
                    if X <= xs_seg[0]:
                        f = X / xs_seg[0]
                        d["l_duoi"] = r_ * (1 - f)
                        d[ph + "0"] = r_ * f
                    elif X >= xs_seg[-1]:
                        f = min(1.0, (X - xs_seg[-1]) / (x_dau - xs_seg[-1]))
                        d[f"{ph}{N_LUA - 1}"] = r_ * (1 - f)
                        d["l_dau"] = d.get("l_dau", 0.0) + r_ * f * 0.5              # đầu tên: nửa cứng, nửa phập phồng
                        d["ten_3"] += r_ * f * 0.5
                    else:
                        j_ = int(np.searchsorted(xs_seg, X)) - 1
                        f = (X - xs_seg[j_]) / (xs_seg[j_ + 1] - xs_seg[j_])
                        d[f"{ph}{j_}"] = r_ * (1 - f)
                        d[f"{ph}{j_ + 1}"] = r_ * f
                d = {b_: w_ for b_, w_ in d.items() if w_ > 0.01}
                tong = sum(d.values())
                Wf.append({b_: w_ / tong for b_, w_ in d.items()})
            sk.slot("ten_nang", "ten_3", "ten_lua", an=True)
            sk.luoi_gan("ten_nang", "ten_lua", Lf, Wf, the_gioi=np.array(Vf), ten="ten_lua")
            lp38 = np.linalg.solve(WG[a4["bone"]], np.array([*D4, 1.0]))[:2]          # đuôi tì dây và hướng mũi tên trong hệ xương mũi tên đang kéo
            u38 = np.linalg.solve(WG[a4["bone"]][:2, :2], (T4 - D4) / np.hypot(*(T4 - D4)))
            info_nang.update(dai=dai, lp=lp38, u=u38)
            gan("youshou_02_t", by["youshou_02"], an=True)
            gan("jian_t", by["jian"], an=True)
        elif s_ == "zuoshou_03":
            gan("youshou_01_t", by["youshou_01"], an=True)

    # ---- cung rơi (die): bản sao cây cung trên một xương con của root
    sk.xuong("cung_roi", "root", 0.0, 0.0)
    WG["cung_roi"] = np.linalg.inv(Wi["gongjian_01"]) @ np.eye(3)
    ac = by["gongjian_01"]
    r = "gongjian_01"
    im = anh_cua(r)
    uvc, trc = G.luoi(ac)
    Vc = sk.atts["gongjian_01"][r]["V"]                       # chỗ cây cung ở dáng gốc của mình
    sk.slot("cung_roi", "cung_roi", r, an=True)
    sk.atts["cung_roi"][r] = {"type": "mesh", "path": r, "uv": uvc / np.array(imgs_ho[r].size, float), "tris": np.asarray(trc, int).reshape(-1, 3),
                              "hull": len(uvc), "V": Vc, "verts": [[("cung_roi", float(v[0]), float(v[1]), 1.0)] for v in Vc],
                              "width": im.width, "height": im.height}
    tam_cung = Vc.mean(0)
    dau_cung = (Wi["bone31"][:2, 2].copy(), Wi["bone32"][:2, 2].copy())

    # ---- chiều cao game, far, mũi tên bay (ảnh mũi tên của mình, trục đuôi → mũi nằm theo +x)
    cao = float(sk.atts["to_02"]["to_02"]["V"][:, 1].max())
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    imj = anh_cua("jian")
    wr, hr = imgs_ho["jian"].size
    kj = float(np.hypot(*M4.T[:, 0]))                           # đơn vị thế giới cho mỗi px ảnh vùng
    u = (mui_px - duoi_px) / np.hypot(*(mui_px - duoi_px))
    n_ = np.array([-u[1], u[0]])
    giua = (mui_px + duoi_px) / 2
    goc_px = np.array([[0, 0], [wr, 0], [wr, hr], [0, hr]], float)
    for k in range(3):
        sk.xuong(f"fly_{k}", "root", 0.0, 0.0)
        sk.xuong(f"ten_{k}", f"fly_{k}", 0.0, 0.0)
        Vb = np.array([[np.dot(p - giua, u) * kj, -np.dot(p - giua, n_) * kj] for p in goc_px])
        sk.slot(f"bay_{k}", f"ten_{k}", "jian", an=True)
        sk.atts[f"bay_{k}"]["jian"] = {"type": "mesh", "path": "jian", "uv": goc_px / np.array([wr, hr], float), "tris": np.array([[0, 1, 2], [0, 2, 3]]),
                                       "hull": 4, "V": Vb, "verts": [[(f"ten_{k}", float(v[0]), float(v[1]), 1.0)] for v in Vb],
                                       "width": imj.width, "height": imj.height}
    for e, m in (("ban", "buông một mũi tên"), ("ban3", "buông ba mũi tên cùng lúc"), ("tu", "bắt đầu tụ lửa vào mũi tên nặng"),
                 ("ban_to", "buông mũi tên lửa nặng"), ("trung", "khung trúng"), ("dap_dat", "chạm đất"), ("roi_cung", "cung rơi khỏi tay"),
                 ("nga", "ngã nằm xuống")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(cao=cao, tam_cung=tam_cung, dau_cung=dau_cung, duoi_ten=a4["bone"], nang=info_nang)


# ---------------------------------------------------------------- clip
def bay_ten(sk, P, k, A, lech, q, slot=None, goc0=None):
    """mũi tên k ở quãng q (0..1) từ điểm A (thế giới, chỗ buông) tới far + lech. goc0: góc lúc còn trên dây (xoay dần sang hướng bay)."""
    far = sk.W0["far"][:2, 2]
    d = far + np.array(lech) - A
    an = not (0.0 <= q < 1.0 - 1e-6)         # 1e-6: khung tới đích tính ra 0,99999… vì sai số chia
    q = min(max(q, 0.0), 1.0)                # tới đích rồi thì xương Ở LẠI đích (đã ẩn), không chạy ngược về chỗ bắn
    Pd = A + q * d + np.array([0.0, 1.0]) * 18.0 * math.sin(math.pi * q)
    fly = q * far
    g = math.degrees(math.atan2(d[1], d[0]))
    if goc0 is not None:
        g = goc0 + (g - goc0) * em(q / 0.3)
    P.move(f"fly_{k}", float(fly[0]), float(fly[1]))
    P.move(f"ten_{k}", float(Pd[0] - fly[0]), float(Pd[1] - fly[1]))
    P.rot(f"ten_{k}", g)
    P.alpha[slot or f"bay_{k}"] = 0.0 if an else 1.0


def lua_chay(P, t, manh=1.0):
    """lửa của mũi tên lửa cháy liên tục: mỗi lưỡi lửa phập phồng dài ngắn, lay quanh gốc, sóng chạy từ mũi về đuôi; đuôi lửa quẫy; đầu tên đập."""
    w = 2 * math.pi * 4.5
    for i in range(N_LUA):
        for nm, dau, lech in ((f"l_t{i}", 1.0, 0.0), (f"l_d{i}", -1.0, 2.1)):
            ph = w * t + 1.15 * i + lech
            a, b = math.sin(ph), math.sin(1.7 * ph + 0.6)
            P.scale(nm, 1.0 + 0.07 * manh * b, 1.0 + manh * (0.22 * a + 0.09 * b))
            P.rot(nm, dau * manh * 8.0 * math.sin(ph + 1.2))
            P.move(nm, -5.0 * manh * (1.0 + a), 0.0)
    P.rot("l_duoi", 7.0 * manh * math.sin(0.8 * w * t))
    P.scale("l_duoi", 1.0 + 0.16 * manh * math.sin(w * t + 0.5), 1.0 + 0.10 * manh * math.sin(1.6 * w * t))
    P.scale("l_dau", 1.0 + 0.05 * manh * math.sin(1.3 * w * t), 1.0 + 0.08 * manh * math.sin(1.3 * w * t + 1.0))


def lam_clip(sk, info):
    out = []
    cao = info["cao"]

    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        hien_theo_ho(P, "idle_01", t, True)
    out.append(Clip("idle", CD["idle_01"][0], idle, loop=True))

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        hien_theo_ho(P, "run_01", t, True)
    out.append(Clip("walk", CD["run_01"][0], walk, loop=True))

    def hit(t, P):
        dat(P, mau("hit_01", t))
        hien_theo_ho(P, "hit_01", t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ---- đánh thường: skill_01 của họ (rút tên, giương, buông ở khung 12 = 0,40 s) + mũi tên bay tới đối thủ
    T_BAN, BAY = 12 / FPS, 5 / FPS

    def cho_buong(them_y=0.0):
        P0 = Pose()
        dat(P0, mau("skill_01", T_BAN - 1 / FPS))
        if them_y:
            P0.move("move", 0.0, them_y)
        return sk.the_gioi(P0)

    W_b = cho_buong()
    A0 = W_b[info["duoi_ten"]][:2, 2].copy()                      # chỗ mũi tên trên dây lúc buông

    def attack(t, P):
        dat(P, mau("skill_01", t))
        hien_theo_ho(P, "skill_01", t)
        if T_BAN <= t < T_BAN + BAY + GIU_DICH:
            bay_ten(sk, P, 0, A0, (0.0, 0.0), (t - T_BAN) / BAY)
    out.append(Clip("attack", CD["skill_01"][0], attack, ev=[(T_BAN, "ban", ""), (T_BAN + BAY + TRE_TRUNG, "trung", "")], trung=T_BAN + BAY + TRE_TRUNG))

    # ---- tiện ích chân: hạ hông, bàn chân giữ chỗ của dáng hiện tại
    def mut(W, b):
        bb = sk.bones[sk.bi[b]]
        return (W[b] @ np.array([bb["length"], 0.0, 1.0]))[:2]

    def ik_chan(P, W, dui, cang, dich):
        bd, bc = sk.bones[sk.bi[dui]], sk.bones[sk.bi[cang]]
        S_ = W[dui][:2, 2]
        L1, L2 = bd["length"], bc["length"]
        d = np.clip(np.hypot(*(dich - S_)), abs(L1 - L2) + 1e-3, L1 + L2 - 1e-3)
        g0 = math.atan2(dich[1] - S_[1], dich[0] - S_[0])
        a1 = g0 + math.acos(np.clip((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1))       # gối gập ra trước như dáng của họ
        E = S_ + L1 * np.array([math.cos(a1), math.sin(a1)])
        a2 = math.atan2(dich[1] - E[1], dich[0] - E[0])
        for b_, gw in ((dui, a1), (cang, a2)):
            bb = sk.bones[sk.bi[b_]]
            cur = bb["rot"] + P._g(b_)[2]
            r = math.degrees(gw) - goc_mat(W[bb["parent"]])
            P._g(b_)[2] = r - 360.0 * round((r - cur) / 360.0) - bb["rot"]
            W = sk.the_gioi(P)
        return W

    def nhun(P, d):
        if abs(d) < 1e-4:
            return
        W = sk.the_gioi(P)
        c13, c15 = mut(W, "bone13"), mut(W, "bone15")
        P.move("bone", 0.0, -d)
        W = sk.the_gioi(P)
        W = ik_chan(P, W, "bone12", "bone13", c13)
        ik_chan(P, W, "bone14", "bone15", c15)

    def dat_mat(P, b, M):
        P.move(b, float(M[0, 2]), float(M[1, 2]))
        P.rot(b, math.degrees(math.atan2(M[1, 0], M[0, 0])))

    # ---- CHIÊU MANA: ba mũi tên xoè, buông cùng lúc, ngắm NGANG (dáng giương của skill_01, giữ dây lâu hơn)
    TC = [(0.0, 0.0), (0.30, 0.20), (0.55, 0.30), (0.95, 0.38), (1.00, 0.40), (1.65, 1.0)]
    T_B3, BAY3 = 1.0, 5 / FPS
    LECH3 = [(0.0, 0.0), (0.0, 0.09 * cao), (0.0, -0.09 * cao)]
    A3 = [W_b[b_][:2, 2].copy() for b_ in (info["duoi_ten"], "xoe_a", "xoe_b")]

    def tq(t, bang):
        for (a_, x), (b_, y) in zip(bang, bang[1:]):
            if t <= b_:
                return x + (y - x) * (t - a_) / (b_ - a_)
        return bang[-1][1]

    def cast(t, P):
        u = tq(t, TC)
        dat(P, mau("skill_01", u))
        hien_theo_ho(P, "skill_01", u)
        g = em((t - 0.30) / 0.25) * (1 - em((t - 0.95) / 0.06))
        P.rot("bone2b", 1.6 * g * math.sin(2 * math.pi * 11 * t))       # gồng run lúc giữ dây
        if P.alpha.get("jian4", 0) > 0.5:
            P.alpha["jian4a"] = P.alpha["jian4b"] = 1.0
        nhun(P, 6.0 * g)
        if T_B3 <= t < T_B3 + BAY3 + GIU_DICH:
            for k in range(3):
                bay_ten(sk, P, k, A3[k], LECH3[k], (t - T_B3) / BAY3)
    out.append(Clip("cast", 1.65, cast, ev=[(T_B3, "ban3", ""), (T_B3 + BAY3 + TRE_TRUNG, "trung", "")], trung=T_B3 + BAY3 + TRE_TRUNG))

    # ---- CHIÊU CUỐI: ba phát nhanh → nhún, bật lên kéo mũi tên nặng → GIỮ tụ lửa → bắn, giật lùi → rơi, đáp đất
    SH = [(0.00, 9 / FPS), (9 / FPS, 17 / FPS), (17 / FPS, 25 / FPS)]          # buông đúng khung mẫu (xem TRE_TRUNG)
    T_NHUN, T_BAT, T_DINH, T_BAN2, T_DAT, D_SK = 0.98, 1.12, 1.36, 62 / FPS, 2.48, 3.05
    BAY_N, CAO_N = 5 / FPS, 0.62 * cao
    NG = info["nang"]

    def cho_ten_lua(W):
        """(đuôi tì dây, góc mũi tên) của mũi tên lửa trên dây ở tư thế W."""
        Wb = W[info["duoi_ten"]]
        d_ = Wb[:2, :2] @ NG["u"]
        return (Wb @ np.array([*NG["lp"], 1.0]))[:2], math.degrees(math.atan2(d_[1], d_[0]))

    A_N, G_N = cho_ten_lua(cho_buong(CAO_N))
    d_n = sk.W0["far"][:2, 2] - A_N
    LECH_N = tuple(-d_n / np.hypot(*d_n) * 0.6 * NG["dai"])                    # đuôi tên dừng trước đích 0,6 thân tên: mũi xuyên qua tâm đối thủ
    SC_BAY = (1.26, 1.38)
    T_CUOI = SH[-1][1] + 0.16

    def u_sk(t):
        for i, (a_, b_) in enumerate(SH):
            if t < b_:
                u0 = 0.0 if i == 0 else 0.20
                return u0 + (T_BAN - u0) * em((t - a_) / (b_ - a_)) ** 0.8, False
        if t < T_CUOI:
            return T_BAN + (t - SH[-1][1]) * 1.25, False
        if t < T_BAT:
            return (T_BAN + 0.2) if t < (T_CUOI + T_BAT) / 2 else 0.20, False
        if t < T_DINH:
            return 0.20 + 0.18 * em((t - T_BAT) / (T_DINH - T_BAT)), True
        if t < T_BAN2:
            return 0.38, True
        return T_BAN + (t - T_BAN2) * 0.9, False

    def skill(t, P):
        u, nang = u_sk(t)
        d_ = mau("skill_01", u)
        for i, (a_, b_) in enumerate(SH):
            if i > 0 and a_ <= t < a_ + 0.08:                    # hoà từ dáng vừa buông sang dáng rút tên mới
                d_ = pha(mau("skill_01", T_BAN + 0.04), d_, em((t - a_) / 0.08))
        if T_CUOI <= t < T_BAT:                                  # rút mũi tên nặng: hoà thẳng dáng sau buông → dáng rút
            d_ = pha(mau("skill_01", T_BAN + 0.2), mau("skill_01", 0.20), em((t - T_CUOI) / (T_BAT - T_CUOI)))
        dat(P, d_)
        hien_theo_ho(P, "skill_01", u)
        if nang:
            P.alpha["ten_nang"] = P.alpha.get("jian4", 0.0)
            P.alpha["jian4"] = 0.0
        y, d_nhun = 0.0, 0.0
        if T_NHUN <= t < T_BAT:
            d_nhun = 16.0 * math.sin(math.pi * (t - T_NHUN) / (T_BAT - T_NHUN))
        elif T_BAT <= t < T_DINH:
            y = CAO_N * (1 - (1 - (t - T_BAT) / (T_DINH - T_BAT)) ** 2)
        elif T_DINH <= t < T_BAN2:
            y = CAO_N + 6.0 * math.sin(2 * math.pi * (t - T_DINH) / 0.5)
        elif T_BAN2 <= t < T_DAT:
            q = (t - T_BAN2) / (T_DAT - T_BAN2)
            y = CAO_N * (1 - q * q)
        elif t >= T_DAT:
            q = t - T_DAT
            d_nhun = 20.0 * math.sin(math.pi * 0.5 * min(1.0, q / 0.07)) * (1 - em((q - 0.07) / 0.40))
        x = -38.0 * em((t - T_BAN2) / 0.12) * (1 - em((t - T_DAT - 0.1) / 0.4)) if t >= T_BAN2 else 0.0
        P.move("move", x, y)
        if y < 1.0:
            nhun(P, d_nhun)
        bay = em((t - T_BAT) / 0.12) * (1 - em((t - T_DAT + 0.06) / 0.08))          # co chân lúc ở trên không
        P.rot("bone12", -28.0 * bay)
        P.rot("bone13", 42.0 * bay)
        P.rot("bone14", -20.0 * bay)
        P.rot("bone15", 36.0 * bay)
        g = em((t - T_DINH) / 0.2) * (1 - em((t - T_BAN2) / 0.05))                  # gồng, run, chùm lửa bùng to lúc tụ lửa
        P.rot("bone2b", 2.5 * g * math.sin(2 * math.pi * 13 * t) * (0.6 + 0.8 * (t - T_DINH) / (T_BAN2 - T_DINH)))
        P.scale("bone4", 1.0 + 0.28 * g)
        for i, (a_, b_) in enumerate(SH):
            if b_ <= t < b_ + BAY + 2 / FPS:
                bay_ten(sk, P, i, A0, (0.0, (i - 1) * 0.06 * cao), (t - b_) / BAY)
        if T_BAN2 <= t < T_BAN2 + BAY_N + GIU_DICH:
            bay_ten(sk, P, 3, A_N, LECH_N, (t - T_BAN2) / BAY_N, slot="ten_nang", goc0=G_N)
            P.scale("ten_3", *SC_BAY)
            lua_chay(P, t, 1.3)
        if nang:                                                 # mũi tên lửa trên dây: đặt theo đuôi tên tì dây SAU khi thân đã vào dáng
            vt, gt = cho_ten_lua(sk.the_gioi(P))
            P.move("ten_3", float(vt[0]), float(vt[1]))
            P.rot("ten_3", gt)
            lon = 0.45 + 0.55 * em((t - T_BAT) / (T_DINH - T_BAT + 0.12))                       # nhen lên từ nhỏ
            tu = em((t - T_DINH) / (T_BAN2 - T_DINH))                                           # 0 → 1 suốt lúc giữ
            cuoi = 0.16 * em((t - (T_BAN2 - 0.14)) / 0.14)                                      # phình to ngay trước khi buông
            P.scale("ten_3", lon * (1.0 + 0.10 * tu + cuoi), lon * (1.0 + 0.22 * tu + cuoi))
            lua_chay(P, t, 0.7 + 0.6 * tu)                                                      # lửa cháy mạnh dần lúc tụ
    out.append(Clip("skill", D_SK, skill, ev=[(b_, "ban", "") for _, b_ in SH] + [(T_DINH, "tu", ""), (T_BAN2, "ban_to", ""),
                                                                                (T_BAN2 + BAY_N + TRE_TRUNG, "trung", ""), (T_DAT, "dap_dat", "")],
                    trung=T_BAN2 + BAY_N + TRE_TRUNG))

    # ---- APPEAR: nhảy từ trên - sau bên trái vào sàn, co chân, đáp thụp, đứng dậy vào thế
    T_CHAM, D_AP = 0.46, 1.35

    def appear(t, P):
        dat(P, mau("idle_01", 0.0))
        hien_theo_ho(P, "idle_01", 0.0)
        if t < T_CHAM:
            q = t / T_CHAM
            P.move("move", -0.95 * cao * (1 - q), 0.75 * cao * (1 - q * q) + 0.25 * cao * math.sin(math.pi * q) * (1 - q))
            P.rot("bone2", -10.0 * (1 - q))
            P.rot("bone12", -30.0)
            P.rot("bone13", 45.0)
            P.rot("bone14", -24.0)
            P.rot("bone15", 40.0)
            for b_ in ("bone4", "bone5", "bone6"):
                P.rot(b_, 14.0 * (1 - q))                         # chùm lửa bị kéo ngược lại khi lao xuống
        else:
            q = t - T_CHAM
            nhun(P, 24.0 * math.sin(math.pi * 0.5 * min(1.0, q / 0.08)) * (1 - em((q - 0.08) / 0.55)))
            P.rot("bone2b", -8.0 * (1 - em(q / 0.5)))
        a_ = min(1.0, t / 0.07)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(T_CHAM, "dap_dat", "")]))

    # ---- DIE: khựng, RỤNG CUNG (cung rơi nằm ngang trên đất), QUỴ GỐI, đổ sấp nằm xuống, mờ dần
    T_ROI, T_QUY, T_NGA, D_DIE = 0.22, 0.62, 1.12, 1.75
    NGA_X, NGA_NANG = 40.0, 15.0
    tam_c = info["tam_cung"]
    neoD = {}

    def die(t, P):
        th = min(t, 0.22)
        dat(P, mau("hit_01", th))
        hien_theo_ho(P, "hit_01", th)
        q = em((t - 0.18) / (T_QUY - 0.18))
        q3 = em((t - T_QUY) / (T_NGA - T_QUY)) ** 1.5 if t >= T_QUY else 0.0
        P.rot("bone2b", -10.0 * q)
        P.rot("bone3b", -8.0 * q + 6.0 * q3)
        nhun(P, 30.0 * q * (1 - 0.85 * q3))
        W = sk.the_gioi(P)
        if t < T_ROI:
            neoD.clear()
        else:
            if "M" not in neoD:
                neoD["M"] = W["gongjian_01"] @ np.linalg.inv(sk.W0["gongjian_01"])
                v_ = (neoD["M"] @ np.array([*info["dau_cung"][1], 1.0]))[:2] - (neoD["M"] @ np.array([*info["dau_cung"][0], 1.0]))[:2]
                g_ = -math.degrees(math.atan2(v_[1], v_[0]))
                neoD["g"] = g_ - 360.0 * round(g_ / 360.0)
            M = neoD["M"]
            q2 = t - T_ROI
            c0 = (M @ np.array([*tam_c, 1.0]))[:2]
            cao_roi = max(1.0, c0[1] - 30.0)
            tc = math.sqrt(2 * cao_roi / 2600.0)
            qq = min(1.0, q2 / tc)
            nay = 6.0 * math.exp(-(q2 - tc) / 0.06) * math.sin(math.pi * min(1.0, (q2 - tc) / 0.1)) if q2 > tc else 0.0
            R_ = mat(c0[0] + 34.0 * em(qq), c0[1] - cao_roi * qq * qq + nay, neoD["g"] * em(qq)) @ mat(-c0[0], -c0[1], 0.0)
            dat_mat(P, "cung_roi", R_ @ M)
            P.alpha["cung_roi"] = 1.0
            for sl in ("gongjian_01", "gongjian_01_t", "gongjian_02", "gongjian_02_t", "jian", "jian_t", "jian4"):
                P.alpha[sl] = 0.0
        if t >= T_QUY:                                           # đổ sấp: quay quanh mũi chân, nâng dần cho thân nằm sát đất
            nay = 5.0 * math.exp(-(t - T_NGA) / 0.08) * math.sin(math.pi * min(1.0, (t - T_NGA) / 0.12)) if t > T_NGA else 0.0
            dat_mat(P, "move", mat(NGA_X, NGA_NANG * q3 + nay, -84.0 * q3) @ mat(-NGA_X, 0.0, 0.0))
        P.scale("bone4", 1.0 - 0.35 * em((t - 0.5) / 1.1))        # lửa tàn dần
        fa = 1.0 - em((t - (D_DIE - 0.3)) / 0.3)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(T_ROI, "roi_cung", ""), (T_NGA, "nga", "")]))
    return out


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c)
            xau = {}
            for p, q in zip(fr, fr[1:]):
                for bn in set(p.t) | set(q.t):
                    d = abs(q.t.get(bn, [0, 0, 0, 1, 1])[2] - p.t.get(bn, [0, 0, 0, 1, 1])[2])
                    xau[bn] = max(xau.get(bn, 0), d)
            lon = sorted(((v, k) for k, v in xau.items() if v > 40), reverse=True)[:6]
            print(f"{c.ten:7s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°"))
        return
    if a and a[0] == "bo_cuc":                # hình bố cục: dáng nghỉ (khung 0 idle) trên nền trắng, làm ảnh mẫu tỉ lệ cho concept
        fr = hoat.nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.10)
        im = ve.ve(fr[0], Bx, float(a[2]) if len(a) > 2 else 2.0, bg=(255, 255, 255), ss=2).convert("RGB")
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        im.save(a[1])
        print(a[1], im.size)
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang_ = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    if a and a[0] == "nhe":                    # CL_DANG=lon: ghi bản để dạng 1 gộp tiến hóa (rig + khung 0 idle + chiều cao)
        import pickle
        idle_ = [c for c in clips if c.ten == "idle"][0]
        os.makedirs(RA, exist_ok=True)
        pickle.dump((sk, hoat.nuong(sk, idle_)[0], info["cao"]), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    M, noi = sk, {}
    if DANG == "non":
        # TIẾN HÓA nối liền (quai/tienhoa.py): gộp rig dạng 2 (dựng ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun).
        # Ý: quỷ con BẮT LỬA. Dạng 1 thụp xuống gồng, chùm lửa nhỏ trên mũ bùng to dần và giật theo nhịp tới cỡ chùm lửa dạng 2; đổi
        # dạng lúc lửa to nhất; dạng 2 hiện ra, ưỡn ngực gầm, chùm lửa bùng quá cỡ rồi lắng về dáng nghỉ.
        import pickle
        import subprocess
        from quai import tienhoa
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, CL_DANG="lon", CL_TEN="", CL_RA="", CL_MANH=""),
                       check=True)
        sk2, idle2, cao2 = pickle.load(open(os.path.join(G.BASE, "rig", "_nhe.pkl"), "rb"))
        ti = info["cao"] / cao2
        M = tienhoa.gop(sk, sk2)
        # ảnh dạng 2 trùng từng điểm với ảnh dạng 1 (mọi mảnh trừ năm mảnh đổi da) thì dùng chung: atlas khỏi phình gấp đôi
        chung = 0
        for nm in list(sk2.images):
            if nm in sk.images and sk.images[nm].size == sk2.images[nm].size and \
                    np.array_equal(np.asarray(sk.images[nm]), np.asarray(sk2.images[nm])):
                M.images.pop("n_" + nm, None)
                for sl in M.atts.values():
                    for sp in sl.values():
                        if sp.get("path") == "n_" + nm:
                            sp["path"] = nm
                chung += 1
        print(f"  gộp tiến hóa: {chung} / {len(sk2.images)} ảnh dùng chung với dạng 1")
        idle_c = [c for c in clips if c.ten == "idle"][0]
        K_LUA = 1.0 / TI_LE.get("bone4", 1.0)                      # chùm lửa dạng 1 phóng chừng này thì bằng chùm lửa dạng 2

        def gong(t, P):
            idle_c.fn(t % idle_c.dur, P)
            g = hoat.cv(t, [(0, 0), (0.28, -0.6), (0.55, 1, "out"), (1.3, 1.15)])        # thụp lấy hơi rồi gồng
            r = hoat.rung(t, 0.45, 1.35, moi=1)
            P.scale("move", 1 + 0.05 * max(g, 0) - 0.04 * min(g, 0), 1 - 0.07 * max(g, 0) * 0.6 + 0.05 * min(g, 0))
            P.move("move", 2.2 * r, 0.0)
            k = hoat.cv(t, [(0, 0), (0.3, 0.0), (0.7, 0.45, "out"), (0.85, 0.35), (1.25, 1.0, "out"), (1.4, 1.0)])   # lửa bùng hai nhịp
            lon = 1 + (K_LUA * 1.12 - 1) * k
            ph = 2 * math.pi * 9.0 * t
            P.scale("bone4", lon * (1 + 0.05 * k * math.sin(ph)), lon * (1 + 0.09 * k * math.sin(ph + 1.3)))
            P.rot("bone4", 5.0 * k * math.sin(0.6 * ph))
            P.rot("bone3", 3.0 * max(g, 0) * math.sin(2 * math.pi * 14 * t) * 0.4)              # đầu run lúc gồng

        def bung(t, P, fl):
            for b_, v in tienhoa.doi_ten_pose(idle2, "n_").t.items():
                P.t[b_] = list(v)
            ph = 2 * math.pi * 8.0 * t
            P.scale("n_move", 1 + 0.03 * fl, 1 + 0.07 * fl)                                     # ưỡn lên gầm
            P.scale("n_bone4", 1 + 0.26 * fl + 0.05 * fl * math.sin(ph), 1 + 0.34 * fl + 0.08 * fl * math.sin(ph + 1.1))
            P.rot("n_bone4", 6.0 * fl * math.sin(0.5 * ph))
            P.scale("n_bone3", 1 + 0.05 * fl)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=bung, mem=[])
        for e_, m_ in (("tu_luc", "tiến hóa: gồng, lửa trên mũ bùng to"), ("doi_dang", "tiến hóa: đổi dạng"), ("gam", "tiến hóa: dạng mới gầm")):
            M.su_kien(e_, m_)
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips, RA, TEN, f"Quỷ lửa bắn cung dạng {1 if DANG == 'non' else 2} ({TEN})", dang=1 if DANG == "non" else 2, so_dang=2, noi_them=noi, dung_yen=("attack", "cast", "skill"), lao=(),
                  far=("attack", "cast", "skill"), far_aim=("attack", "cast", "skill"), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  # cảm giác trúng: (khựng, rung, bật lùi[, chớp màn]); chiêu cuối "impact mạnh, shake cam" (người dùng)
                  impact={"attack": (0.05, 0.25, 0.07), "skill": (0.22, 1.0, 0.18, "#ffb04066")})


if __name__ == "__main__":
    main(sys.argv[1:])
