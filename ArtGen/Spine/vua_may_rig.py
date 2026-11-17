# -*- coding: utf-8 -*-
"""Vua robot (vua_may, tướng 10 / final boss đảo Kim): RESKIN trên rig con gốc monster_3637 (vua robot vàng, bệ hai chân xích), thêm
hai CHÂN ROBOT và BỐN CÁNH lơ lửng tự dựng.

- Xương: đủ mọi xương của họ + `move`. Dáng gốc = khung 0 idle_01 (biến đổi riêng `l` lấy mẫu bằng runtime Spine thật), riêng khối hông
  `xiabanshen_02` (cha của cả thân) và ba mảnh đầu quyền trượng `fazhang_03/04/05` (con của all2, theo trượng bằng transform constraint
  đã nướng) NÂNG lên DY = 150 đơn vị để có chỗ cho chân. Hai chân xích của họ (`jiao_l_03`, `jiao_r_3`) bỏ hình, giữ xương: chỗ cổ chân
  bám theo xích (bước, nhún, trượt của họ).
- CHÂN (tự dựng): mỗi chân `dui_<s>` (đùi, con của khối hông) → `ong_<s>` (ống), `ban_<s>` (bàn, con của move). Mỗi khung giải IK hai đoạn
  cho cổ chân tới đích: dưới đất = điểm bám trên xương xích của họ; trên không = treo theo hông (gối co thêm, mũi chân chúc).
- CÁNH (tự dựng, theo khuôn cánh của các tướng có cánh trong game: gốc cánh → tay cánh → từng chiếc lông một mảnh trên xương riêng): bốn
  cánh `cw_<k>` (con của ngực xiabanshen_03, lơ lửng sau lưng) → `cw_<k>_tay` → `cw_<k>_l<j>` (j = 0 lông ngoài cùng). Vỗ cánh tự viết:
  hất lên chậm (60 % chu kỳ), đập xuống nhanh (40 %), lông xoè khi giơ, khép khi đập, trễ nhịp theo thứ tự từ trong ra ngoài.
- Hình: mỗi hình của họ một hình của mình, NGUYÊN lưới của họ. Chân, cánh: ô cứng 4 đỉnh bám một xương.

    vua_may_rig.py                         dựng, xuất inbox/vua_may_1/rig/
    vua_may_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    vua_may_rig.py kiem                    bước xoay lớn nhất giữa hai khung của từng clip
    VM_GOC=1 vua_may_rig.py ...            dựng bằng DA GỐC + chân, cánh GIỮ CHỖ ra rig_goc/: chỉ để soi clip trong máy, không đưa vào game
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, xuat, soi  # noqa: E402
from quai.khung import Sk, Pose  # noqa: E402
from quai.hoat import Clip, ik_hai_doan  # noqa: E402
from quai.luoi import Luoi  # noqa: E402
import vua_may as G  # noqa: E402
import vua_may_da as DA  # noqa: E402

GOC = os.environ.get("VM_GOC") == "1"
BASE = G.BASE
TEN = "vua_may"
RA = os.environ.get("VM_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("VM_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
RES = 2
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
INH = {i for i, b in enumerate(I["bones"]) if b.get("inherit")}   # xương không nhận xoay / tỉ lệ của cha (inherit 1, 2): runtime mình không có


def _wm(F, i):
    a, b, c, d = F["m"][i]
    return np.array([[a, b, F["b"][i][0]], [c, d, F["b"][i][1]], [0, 0, 1.0]])


def l_cua(F, i):
    """biến đổi riêng (x, y, góc, sx, sy) của xương i ở khung F; xương inherit khác thường tính từ ma trận thế giới của nó và của cha."""
    if i not in INH:
        return list(F["l"][i][:5])
    Lw = np.linalg.solve(_wm(F, I["bones"][i]["parent"]), _wm(F, i))
    sx = math.hypot(Lw[0, 0], Lw[1, 0])
    return [float(Lw[0, 2]), float(Lw[1, 2]), math.degrees(math.atan2(Lw[1, 0], Lw[0, 0])), sx,
            float((Lw[0, 0] * Lw[1, 1] - Lw[0, 1] * Lw[1, 0]) / max(1e-9, sx))]


L0 = [l_cua(S["idle_01"]["frames"][0], i) for i in range(len(I["bones"]))]
ZERO5 = np.array([0, 0, 0, 1, 1.0])
USE = ["idle_01", "run_01", "hit_01", "die_01", "skill_01_1", "skill_01_2", "skill_01_3", "skill_02", "skill_03", "skill_04"]
BO_SLOT = {"shadow", "jiao_l_03", "jiao_r_3"}
DY = DA.DY
NANG = {"xiabanshen_02", "fazhang_03", "fazhang_04", "fazhang_05"}
XICH = {"gan": "jiao_r_3", "xa": "jiao_l_03"}      # chân gần (trái hình) bám xích jiao_r_3, chân xa (phải hình) bám jiao_l_03
CHAN_KEO = 1.22                                  # đùi, ống dài hơn sơ đồ bố cục: dáng nghỉ gập gối rõ, thân nhô lên ~80 vẫn với tới đất


# ---------------------------------------------------------------- thứ tự vẽ của họ: slot đứng yên + slot di động
def _thu_tu():
    base = list(S["idle_01"]["frames"][0]["o"])
    pos0 = {s: i for i, s in enumerate(base)}
    orders = []
    for c in USE:
        for F in S[c]["frames"]:
            o = tuple(F["o"])
            if o not in orders:
                orders.append(o)
    static = set(base)
    while True:
        cnt = {}
        for o in orders:
            seq = [s for s in o if s in static]
            for i in range(len(seq)):
                for j in range(i + 1, len(seq)):
                    if pos0[seq[i]] > pos0[seq[j]]:
                        cnt[seq[i]] = cnt.get(seq[i], 0) + 1
                        cnt[seq[j]] = cnt.get(seq[j], 0) + 1
        if not cnt:
            break
        static.discard(max(cnt, key=lambda k: (cnt[k], -pos0[k])))
    stat = [s for s in base if s in static]
    return stat, [s for s in base if s not in static]


STAT, DONG = _thu_tu()
STAT_I = {s: i for i, s in enumerate(STAT)}


def neo(o, m):
    n = 0
    for s in o:
        if s == m:
            return n
        if s in STAT_I:
            n += 1
    return n


NEO0 = {m: neo(S["idle_01"]["frames"][0]["o"], m) for m in DONG}


def ten_ban(m, k):
    return SL[m] if k == NEO0[m] else f"{SL[m]}@{k}"


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung)
def _cd():
    out = {}
    for clip in USE:
        v = S[clip]
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(I["bones"]):
            if b0["name"] == "root":
                continue
            z = L0[i]
            Lf = [l_cua(F, i) for F in fr]
            Am = np.array([[l[2] - z[2], l[0] - z[0], l[1] - z[1], l[3] / (z[3] or 1.0), l[4] / (z[4] or 1.0)] for l in Lf])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - ZERO5).max() > 1e-4:
                res[b0["name"]] = Am
        hinh = [[(F["n"][k], float(F["a"][k])) for k in range(len(SL))] for F in fr]
        cho = [{m: neo(F["o"], m) for m in DONG} for F in fr]
        out[clip] = (float(v["dur"]), res, hinh, cho, (len(fr) - 1) / max(1e-6, float(v["dur"])))
    return out


CD = _cd()
BAN = {m: sorted({c[m] for clip in USE for c, h in zip(CD[clip][3], CD[clip][2]) if h[m][0] is not None} | {NEO0[m]}) for m in DONG}


def mau(clip, t, lap=False):
    dur, R, fps = CD[clip][0], CD[clip][1], CD[clip][4]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * fps
    out = {}
    for b, arr in R.items():
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        out[b] = arr[i0] * (1 - w) + arr[i1] * w
    return out


def khung_ho(clip, t, lap=False):
    dur, fps = CD[clip][0], CD[clip][4]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * fps
    return min(len(CD[clip][2]) - 1, int(round(x)))


def pha_gan(a, b, w):
    out = {}
    for k in set(a) | set(b):
        x, y = a.get(k, ZERO5), np.array(b.get(k, ZERO5), float)
        y[0] += 360.0 * round((x[0] - y[0]) / 360.0)
        out[k] = x * (1 - w) + y * w
    return out


def cong(d, bone, rot=0.0, x=0.0, y=0.0):
    v = np.array(d.get(bone, ZERO5), float)
    v[0] += rot
    v[1] += x
    v[2] += y
    d[bone] = v


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


def tq(t, bang):
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / max(1e-9, b_ - a_)
    return bang[-1][1]


def giat(t, t0, sau=0.035, ve=0.16):
    if t < t0:
        return 0.0
    s_ = t - t0
    if s_ < sau:
        return em(s_ / sau)
    return max(0.0, 1.0 - em((s_ - sau) / ve))


# ---------------------------------------------------------------- hiệu ứng trong rig (ba chiêu người dùng duyệt 2026-11-17)
CAO0 = 1130.0                                             # chiều cao dáng đứng (không cánh) ước trước để đặt far
FAR = np.array([1.6 * CAO0, 0.40 * CAO0])                 # far: tâm thân đối thủ ở dáng gốc (game dời tới đối thủ thật)
N_NUT, N_TIA = 6, 14                                      # số tia lửa nứt đất (đánh thường), số đoạn tia (chiêu mana)
HANH = (("thuy", "sao_thuy", 1.45), ("hoa", "sao_hoa", 1.40), ("dat", "trai_dat", 1.30))   # (mã, ảnh mảnh, tỉ lệ bản sao) theo thứ tự tia đi qua
W_TIA = (0.30, 0.48, 0.66)                                # (cũ) chỗ ba hành tinh trên đường Mặt Trời → đối thủ (phần quãng)
# người dùng 2026-11-17: "chiêu cast mana cho các tiểu hành tinh đứng thẳng hàng trên đầu của đối thủ rồi mặt trời lên trên cùng sau đó bắn tia
# sáng xuống" → cột thẳng đứng trên đầu đối thủ (hệ far = tâm đối thủ): Sao Thủy thấp nhất, Sao Hỏa, Trái Đất, Mặt Trời trên cùng (× CAO0)
Y_COT = (0.50, 0.73, 1.02)
Y_SUN = 1.42
K_SUN = 1.55                                              # bản sao Mặt Trời bay lên cột: to hơn Mặt Trời trên trượng
# người dùng 2026-11-17: "cải tiến thêm idle hay các animation khác, cho các hành tinh quay quanh mặt trời": quỹ đạo elip nghiêng quanh tâm Mặt
# Trời, (bán kính ngang, dẹt, số vòng mỗi 2,67 s, pha); nửa dưới elip = phía người xem (vẽ trước Mặt Trời, to hơn), nửa trên = phía sau
QUY = {"fazhang_03": (185.0, 0.36, 3, 0.00), "fazhang_05": (290.0, 0.34, 2, 0.40), "fazhang_04": (390.0, 0.32, 1, 0.72)}
CHU_QUY = 2.6667
NGHIENG = math.radians(-14.0)
DAY_TIA = (150.0, 220.0, 300.0, 400.0)                      # bề dày đoạn tia trước / sau từng hành tinh (đơn vị rig)
MAU_CHO = {"cung": (255, 201, 60), "an": (249, 184, 37), "cot": (255, 230, 150), "tia": (255, 201, 60), "nhat_thuc": (42, 43, 51),
           "duoi": (255, 154, 61)}


def fx_anh(ten):
    """ảnh hiệu ứng manh/fx_<ten>.png (tờ FX_1 của vua_may_fx.py); chưa có thì vẽ hình giữ chỗ (để dựng được trước khi tờ về)."""
    p = os.path.join(MANH, f"fx_{ten}.png")
    if not os.path.exists(p):
        im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if ten == "tia":
            im = Image.new("RGBA", (400, 120), (0, 0, 0, 0))
            ImageDraw.Draw(im).rectangle([0, 10, 399, 109], fill=MAU_CHO[ten] + (255,), outline=DA.MUC + (255,), width=6)
        else:
            d.ellipse([8, 8, 192, 192], fill=MAU_CHO[ten] + (255,), outline=DA.MUC + (255,), width=6)
        os.makedirs(MANH, exist_ok=True)
        im.save(p)
    return f"fx_{ten}"


def tat_dan(t, t0, bien, tan, giam):
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def hien_theo_ho(sk, P, clip, t, lap=False):
    i = khung_ho(clip, t, lap)
    hinh, cho = CD[clip][2][i], CD[clip][3][i]
    for k, sl in enumerate(SL):
        if sl in BO_SLOT:
            continue
        n, a = hinh[k]
        ten = [ten_ban(k, kk) for kk in BAN[k]] if k in NEO0 else [sl]
        for nm in ten:
            if nm not in sk.si:
                continue
            bat = n is not None and (k not in NEO0 or nm == ten_ban(k, cho[k]))
            P.alpha[nm] = a if bat else 0.0
            if bat and n in sk.atts.get(nm, {}) and len(sk.atts[nm]) > 1:
                P.att[nm] = n


# ---------------------------------------------------------------- chân, cánh: hình học (đơn vị rig, thế giới khung 0 idle đã nâng)
def chan_khop(s):
    """khớp háng, gối, cổ chân của chân s: háng, cổ chân theo sơ đồ bố cục; đùi, ống dài thêm CHAN_KEO, gối giải lại (gập ra ngoài như
    sơ đồ)."""
    c = DA.CHAN[s]
    A, Bk, C = np.array(c["hong"], float), np.array(c["goi"], float), np.array(c["co"], float)
    L1, L2 = np.linalg.norm(Bk - A) * CHAN_KEO, np.linalg.norm(C - Bk) * CHAN_KEO
    D = C - A
    d = float(np.linalg.norm(D))
    al = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
    cr = (C - A)[0] * (Bk - A)[1] - (C - A)[1] * (Bk - A)[0]
    uon = -1.0 if cr >= 0 else 1.0
    a = math.atan2(D[1], D[0]) - uon * al
    K = A + L1 * np.array([math.cos(a), math.sin(a)])
    return A, K, C, L1, L2, (-uon)


def chan_manh(s):
    """mảnh giữ chỗ của một chân: [(tên, xương, [(đa giác, màu)])] vẽ sau → trước."""
    A, K, C, L1, L2, _ = chan_khop(s)
    c = DA.CHAN[s]
    g, m, cao = c["ban"]
    dd, do = c["day"]
    vang, sam, khop = (233, 196, 112), (196, 150, 72), (92, 80, 60)
    return [("hong", "dui", [(DA._tron(A, 64), khop)]),
            ("dui", "dui", [(DA._doan(A, K, dd, dd * 0.8), vang)]),
            ("ong", "ong", [(DA._doan(K + (C - K) * 0.05, C, do * 0.95, do * 1.2), sam)]),
            ("co", "ban", [(DA._tron((C[0], C[1] + 6), 44), khop)]),
            ("ban", "ban", [([(g, 0), (g, cao * 0.7), (g + (m - g) * 0.22, cao), (g + (m - g) * 0.7, cao), (m, cao * 0.5), (m + 26, 0)],
                             vang)]),
            ("goi", "ong", [(DA._tron(K, 70), sam)])]


def canh_cau_truc(k):
    """cánh k: gốc, hướng tay cánh, cổ cánh, các lông [(chỗ treo, góc, dài, bề ngang)] (j = 0 lông ngoài cùng), chiều quạt."""
    c = DA.CANH[k]
    a0, L, q, n = math.radians(c["huong"]), c["dai"], c["quat"], c["luoi"]
    d = np.array([math.cos(a0), math.sin(a0)])
    G0 = np.array(c["goc"], float)
    co = G0 + d * L * 0.55
    longs = []
    for j in range(n):
        t = j / max(1, n - 1)
        longs.append((co + (G0 - co) * (t * 0.8), a0 + q * math.radians(8 + 104 * t), L * (0.78 - 0.40 * t), L * 0.15, t))
    return dict(G0=G0, a0=a0, L=L, q=q, co=co, longs=longs, la=[(f"cw_{k}_l{j}", lg[4]) for j, lg in enumerate(longs)])


# ---------------------------------------------------------------- mảnh thật (manh/moi.json do vua_may_manh.py cắt từ concept B3)
MOI = {} if GOC else (json.load(open(os.path.join(MANH, "moi.json"))) if os.path.exists(os.path.join(MANH, "moi.json")) else {})
# mảnh đổi dáng gộp nhiều part của họ: các slot bị gộp thì bỏ (vương miện gộp vành sau; râu gộp hai đầu ria + mảnh má; trượng gộp đầu tháp)
if not GOC:
    BO_SLOT |= {"touguan_1", "toufa_02", "toufa_03", "toufa_04", "fazhang_02", "yanjing"}
# chỉnh tay mảnh đổi dáng (đơn vị rig): vương miện GPT vẽ vành sau thấp hơn concept → che mắt (mắt y 842–885, đáy vương miện ~855): nâng 38
CHINH = {"vuong_mien": (0.0, 38.0)}
BAN_LEN = 25.0                                            # bàn chân nâng lên cho đỉnh ngón lọt dưới đáy khối giáp (hở 8–13 đơn vị)
TANG = (("ngoai", 1.0), ("giua", 0.6), ("phu", 0.25))     # ba tầng lông cánh, vẽ sau → trước; số = độ trễ / xoè
CO_CHAN = ("goi", "ban")                                  # chân ống lồng: khối giáp ống chân (goi) + bàn chân; pít-tông vẽ bằng mã


def _manh_tg(ten):
    """mảnh mới: mặt nạ alpha + hàm px ảnh → thế giới (từ 4 góc thế giới của moi.json)."""
    Vw = np.array(MOI[ten]["the_gioi"], float)
    A = np.asarray(Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA"))[..., 3] > 100
    h, w = A.shape

    def f(px, py):
        return Vw[0] + (px / w) * (Vw[1] - Vw[0]) + (py / h) * (Vw[3] - Vw[0])
    return A, f


def chan_that_khop(s):
    """CHÂN ỐNG LỒNG (concept B3: chân là một khối giáp ngắn trên bàn chân; ba tờ đùi / ống / gối đều ra cùng khối đó): khớp háng = giữa mép
    trên khối giáp (pít-tông thép sẫm gắn hông trượt ra vào trong khối), cổ chân = giữa mép dưới khối, mặt đất = đáy bàn chân; bề ngang
    khối (để vẽ pít-tông)."""
    A, f = _manh_tg(f"chan_{s}_goi")
    ys, xs = np.nonzero(A)
    hm = ys.max() - ys.min()
    top = ys < ys.min() + 0.15 * hm
    bot = ys > ys.max() - 0.15 * hm
    hong = f(xs[top].mean(), ys.min() + 0.12 * hm)
    co = f(xs[bot].mean(), ys.max() - 0.10 * hm)
    rong = float(np.linalg.norm(f(xs.max(), ys.mean()) - f(xs.min(), ys.mean())))
    A, f = _manh_tg(f"chan_{s}_ban")
    ys, xs = np.nonzero(A)
    day = f(xs.mean(), ys.max())[1]
    return hong, co, rong, day


def canh_that(k):
    """cánh k từ mảnh thật: trục tay cánh (PCA điểm alpha của mảnh tay cánh), gốc = đầu gần thân, chiều quạt theo hướng cánh."""
    A, f = _manh_tg(f"canh_{k}_tay")
    ys, xs = np.nonzero(A)
    P = np.array([f(x, y) for x, y in zip(xs[::7], ys[::7])])
    c = P.mean(0)
    u, s_, vt = np.linalg.svd(P - c, full_matrices=False)
    d = vt[0]
    t = (P - c) @ d
    e0, e1 = c + d * t.min(), c + d * t.max()
    than = np.array([0.0, 800.0])
    G0, tip = (e0, e1) if np.linalg.norm(e0 - than) < np.linalg.norm(e1 - than) else (e1, e0)
    a0 = math.atan2(*(tip - G0)[::-1])
    q = 1.0 if tip[0] < G0[0] else -1.0
    L = float(np.linalg.norm(tip - G0))
    d_ = (tip - G0) / max(1e-9, L)
    # người dùng 2026-11-17: "các khớp cánh và lông cánh không match nhau" (bốn mảnh cứng xoay lệch nhau) → mỗi cánh MỘT lưới liền (tay
    # cánh + ba tầng lông ghép sẵn), bám ba xương dọc tay cánh: tay (gốc), co (cổ cánh 45 %), ngon (80 %)
    return dict(G0=G0, a0=a0, L=L, q=q, d=d_, la=[], luoi=True, co=G0 + d_ * 0.45 * L, ngon=G0 + d_ * 0.80 * L)


def canh_lien(k):
    """ghép tầng ngoài, giữa, phủ, tay cánh (đúng chỗ thế giới, 1 px / đơn vị) thành manh/canh_<k>_lien.png; trả 4 góc thế giới."""
    ps = [f"canh_{k}_{t_}" for t_, _ in TANG] + [f"canh_{k}_tay"]
    Q = [np.array(MOI[p_]["the_gioi"], float) for p_ in ps]
    x0 = min(q_[:, 0].min() for q_ in Q)
    x1 = max(q_[:, 0].max() for q_ in Q)
    y0 = min(q_[:, 1].min() for q_ in Q)
    y1 = max(q_[:, 1].max() for q_ in Q)
    can_ = Image.new("RGBA", (int(math.ceil(x1 - x0)) + 2, int(math.ceil(y1 - y0)) + 2), (0, 0, 0, 0))
    for p_, q_ in zip(ps, Q):
        im = Image.open(os.path.join(MANH, p_ + ".png")).convert("RGBA")
        w_, h_ = q_[1, 0] - q_[0, 0], q_[0, 1] - q_[3, 1]
        im = im.resize((max(1, round(w_)), max(1, round(h_))), Image.LANCZOS)
        can_.alpha_composite(im, (int(round(q_[0, 0] - x0)), int(round(y1 - q_[0, 1]))))
    can_.save(os.path.join(MANH, f"canh_{k}_lien.png"))
    return np.array([[x0, y1], [x0 + can_.width, y1], [x0 + can_.width, y1 - can_.height], [x0, y1 - can_.height]], float)


def ts_canh(V, ct, k):
    """trọng số dọc tay cánh: chiếu lên trục gốc → ngọn; t < 0,30 bám tay, 0,30–0,52 hoà sang cổ cánh, 0,62–0,86 hoà sang ngọn."""
    t = (np.asarray(V, float) - ct["G0"]) @ ct["d"] / ct["L"]
    out = []

    def sm(x):
        x = min(1.0, max(0.0, x))
        return x * x * (3 - 2 * x)
    for v in t:
        a = sm((v - 0.30) / 0.22)
        b = sm((v - 0.62) / 0.24)
        w = {f"cw_{k}_tay": 1 - a, f"cw_{k}_co": a * (1 - b), f"cw_{k}_ngon": a * b}
        out.append({kk: vv for kk, vv in w.items() if vv > 1e-3})
    return out


def ve_da_giac(ten, polys, pad=10):
    """ảnh RGBA 1 px / đơn vị của các đa giác (thế giới rig) + 4 góc thế giới (trên trái, trên phải, dưới phải, dưới trái)."""
    P = np.concatenate([np.array(p, float) for p, _ in polys])
    x0, y0 = P.min(0) - pad
    x1, y1 = P.max(0) + pad
    w, h = int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))
    S2 = 2
    im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for poly, mau in polys:
        pts = [((x - x0) * S2, (y1 - y) * S2) for x, y in poly]
        d.polygon(pts, fill=tuple(mau) + (255,))
        d.line(pts + [pts[0]], fill=DA.MUC + (255,), width=12, joint="curve")
    im = im.resize((w, h), Image.LANCZOS)
    os.makedirs(MANH, exist_ok=True)
    im.save(os.path.join(MANH, ten + ".png"))
    return np.array([[x0, y1], [x0 + w, y1], [x0 + w, y1 - h], [x0, y1 - h]], float)


# ---------------------------------------------------------------- dựng
def manh_goc():
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    os.makedirs(MANH, exist_ok=True)
    tot = {}
    for a in AG["atts"]:
        if a.get("region") not in imgs:
            continue
        uv, tr = G.luoi(a)
        dt = sum(abs(float((uv[t_[1]][0] - uv[t_[0]][0]) * (uv[t_[2]][1] - uv[t_[0]][1]) - (uv[t_[1]][1] - uv[t_[0]][1]) * (uv[t_[2]][0] - uv[t_[0]][0]))) for t_ in np.asarray(tr).reshape(-1, 3))
        if dt > tot.get(a["region"], (0, None))[0]:
            tot[a["region"]] = (dt, a)
    for r, (_, a) in tot.items():
        p = os.path.join(MANH, r + ".png")
        if not os.path.exists(p):
            im = G.part_goc(a)
            im.resize((im.width * RES, im.height * RES), Image.LANCZOS).save(p)


def dung():
    if GOC:
        manh_goc()
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    for i, b in enumerate(I["bones"]):
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        z = L0[i]
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1] + (DY if b["name"] in NANG else 0.0), goc=z[2], dai=b["len"],
                 sx=z[3], sy=z[4])
    Wi = sk.the_gioi()
    Wh = {}                                              # ma trận thế giới của họ ở khung 0 idle (chưa nâng): để gắn đỉnh lưới
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hinh0 = CD["idle_01"][2][0]
    IM = {}

    # ---- xương chân
    info_chan = {}
    THAT_CHAN = (not GOC) and all(f"chan_{s}_{t}" in MOI for s in ("xa", "gan") for t in CO_CHAN)
    LECH_CHAN = np.zeros(2)
    if THAT_CHAN:                                         # chân thật: khớp đo trên mảnh; cả hai chân hạ / nâng cho đáy bàn chân chạm đất
        kh = {s: chan_that_khop(s) for s in ("xa", "gan")}
        LECH_CHAN = np.array([0.0, -min(kh["xa"][3], kh["gan"][3]) - BAN_LEN])
        print("chân ống lồng: dời", LECH_CHAN.round(1), {s: [np.round(v, 0).tolist() for v in kh[s][:2]] for s in kh})
    for s in ("xa", "gan"):
        if THAT_CHAN:
            A, C = (np.asarray(v, float) + LECH_CHAN for v in kh[s][:2])
            Lc = float(np.linalg.norm(C - A))
            aA = math.degrees(math.atan2(*(C - A)[::-1]))
            sk.xuong(f"dui_{s}", "xiabanshen_02", *A, goc=aA, dai=Lc, the_gioi=True)       # pít-tông: gốc ở hông, chĩa xuống cổ chân
            sk.xuong(f"ban_{s}", "move", *C, goc=0.0, the_gioi=True)
            sk.xuong(f"ong_{s}", f"ban_{s}", *C, goc=aA + 180.0, dai=Lc, the_gioi=True)     # khối giáp: gốc ở cổ chân, chĩa lên hông
            info_chan[s] = dict(uon=0, C=C, A=A, Lc=Lc, rong=kh[s][2], long=True)
            continue
        A, K, C, L1, L2, uon = chan_khop(s)
        aA = math.degrees(math.atan2(*(K - A)[::-1]))
        aK = math.degrees(math.atan2(*(C - K)[::-1]))
        sk.xuong(f"dui_{s}", "xiabanshen_02", *A, goc=aA, dai=L1, the_gioi=True)
        sk.xuong(f"ong_{s}", f"dui_{s}", *K, goc=aK, dai=L2, the_gioi=True)
        sk.xuong(f"ban_{s}", "move", *C, goc=0.0, the_gioi=True)
        info_chan[s] = dict(uon=uon, C=C)
    # ---- xương cánh
    info_canh = {}
    THAT_CANH = (not GOC) and all(f"canh_{k}_tay" in MOI for k in DA.CANH)
    for k in DA.CANH:
        ct = canh_that(k) if THAT_CANH else canh_cau_truc(k)
        a0 = math.degrees(ct["a0"])
        sk.xuong(f"cw_{k}", "xiabanshen_03", *ct["G0"], goc=a0, dai=ct["L"] * 0.2, the_gioi=True)
        sk.xuong(f"cw_{k}_tay", f"cw_{k}", *ct["G0"], goc=a0, dai=ct["L"] * 0.55, the_gioi=True)
        if THAT_CANH:
            sk.xuong(f"cw_{k}_co", f"cw_{k}_tay", *ct["co"], goc=a0, dai=ct["L"] * 0.35, the_gioi=True)
            sk.xuong(f"cw_{k}_ngon", f"cw_{k}_co", *ct["ngon"], goc=a0, dai=ct["L"] * 0.2, the_gioi=True)
        else:
            for j, (p, a, l, w, t) in enumerate(ct["longs"]):
                sk.xuong(f"cw_{k}_l{j}", f"cw_{k}_tay", *p, goc=math.degrees(a), dai=l, the_gioi=True)
        info_canh[k] = ct
    THAT_VONG = (not GOC) and "hao_quang" in MOI
    if THAT_VONG:                                         # vòng hào quang: xương ở tâm vòng, con của ngực (xoay chậm trong clip aura)
        tv = np.array(MOI["hao_quang"]["the_gioi"], float).mean(0)
        sk.xuong("hao_quang", "xiabanshen_03", *tv, goc=0.0, the_gioi=True)
    Wi = sk.the_gioi()

    def anh_cua(r, goc_a=None):
        if r not in IM:
            p = os.path.join(MANH, r + ".png")
            if not os.path.exists(p):
                raise SystemExit(f"thiếu mảnh {p}")
            g = Image.open(p).convert("RGBA")
            k_ = float(os.environ.get("VM_PX") or 0.6)
            if r.startswith(("canh_", "hao_quang")):          # cánh, vòng: mảng phẳng lớn, nét to → thu nhỏ hơn (.atomik dưới trần 0,5 MB)
                k_ *= 0.62
            if k_ != 1.0 and min(g.size) * k_ >= 4:
                g = g.convert("RGBa").resize((max(2, round(g.width * k_)), max(2, round(g.height * k_))), Image.LANCZOS).convert("RGBA")
            IM[r] = anh.loang_mau(g)
            sk.anh(r, IM[r])
        return IM[r]

    def hang(a, xy):
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

    def gan(slot_ten, a):
        r = a["region"]
        im = anh_cua(r, a)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        tris = np.asarray(tris, int).reshape(-1, 3)
        sk.atts[slot_ten][a["att"]] = {"type": "mesh", "path": r, "uv": uv, "tris": tris, "hull": len(uv), "V": V0, "verts": rows,
                                       "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, a["att"])] = Luoi(uv * np.array([im.width, im.height], float), tris, len(uv), len(uv), im.width, im.height,
                                             ten=slot_ten)

    def gan_cung(slot_ten, ten_anh, bone, Vw, ten_att=None):
        im = anh_cua(ten_anh)
        ten_att = ten_att or ten_anh
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        Wb = Wi[bone]
        rows = [[(bone, *map(float, np.linalg.solve(Wb, np.array([v[0], v[1], 1.0]))[:2]), 1.0)] for v in Vw]
        V0 = np.array([(Wi[bone] @ np.array([r_[0][1], r_[0][2], 1.0]))[:2] for r_ in rows])
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.atts[slot_ten][ten_att] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": tris, "hull": 4, "V": V0, "verts": rows,
                                      "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_att)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)

    def manh_moi(slot_ten, bone, polys, lech=(0.0, 0.0), force=False):
        """mảnh tự dựng: GIỮ CHỖ (VM_GOC) thì vẽ từ đa giác; da mình thì ảnh cắt từ concept (manh/<slot>.png + moi.json). force: luôn vẽ
        từ đa giác (pít-tông chân)."""
        if not GOC and slot_ten in MOI and not force:
            Vw = np.array(MOI[slot_ten]["the_gioi"], float) + np.asarray(lech, float)
        else:
            Vw = ve_da_giac(slot_ten, polys)
        sk.slot(slot_ten, bone, slot_ten)
        gan_cung(slot_ten, slot_ten, bone, Vw)

    def them_chan(s):
        if THAT_CHAN:
            c = info_chan[s]
            A, C, w_ = c["A"], c["C"], c["rong"] * 0.46
            d_ = (C - A) / c["Lc"]
            day = A + d_ * c["Lc"] * 0.92
            sat, vang = (89, 88, 93), (249, 184, 37)
            nhan = [(A + d_ * 18, A + d_ * 40)]
            polys = [(DA._doan(A - d_ * 10, day, w_, w_ * 0.9), sat)] + [(DA._doan(a_, b_, w_ * 1.12), vang) for a_, b_ in nhan]
            manh_moi(f"chan_{s}_pit", f"dui_{s}", polys, force=True)
            manh_moi(f"chan_{s}_ban", f"ban_{s}", None, lech=LECH_CHAN + np.array([0.0, BAN_LEN]))
            manh_moi(f"chan_{s}_goi", f"ong_{s}", None, lech=LECH_CHAN)
            return
        for ten, xb, polys in chan_manh(s):
            manh_moi(f"chan_{s}_{ten}", {"dui": f"dui_{s}", "ong": f"ong_{s}", "ban": f"ban_{s}"}[xb], polys)

    def them_canh(k):
        ct = info_canh[k]
        if THAT_CANH:
            from quai.luoi import luoi_vung
            Vq = canh_lien(k)
            ten_a = f"canh_{k}_lien"
            im = anh_cua(ten_a)
            L_ = luoi_vung(im, buoc_vien=9.0, buoc_trong=14.0, vien=2, ten=ten_a, in_tk=False)
            kx = (Vq[1, 0] - Vq[0, 0]) / im.width
            ky = (Vq[0, 1] - Vq[3, 1]) / im.height
            Vw = np.stack([Vq[0, 0] + L_.pts[:, 0] * kx, Vq[0, 1] - L_.pts[:, 1] * ky], 1)
            sk.slot(f"canh_{k}", f"cw_{k}_tay", ten_a)
            sk.luoi_gan(f"canh_{k}", ten_a, L_, ts_canh(Vw, ct, k), the_gioi=Vw)
            return
        for j in reversed(range(len(ct["longs"]))):
            p, a, l, w, t = ct["longs"][j]
            manh_moi(f"cw_{k}_l{j}", f"cw_{k}_l{j}", [(DA._long(p, a, l, w), (214, 219, 226))])
        L = ct["L"]
        manh_moi(f"cw_{k}_tay", f"cw_{k}_tay", [(DA._doan(ct["G0"], ct["co"], L * 0.12, L * 0.085), (170, 176, 186)),
                                               (DA._tron(ct["co"], L * 0.06), (150, 156, 168))])
        manh_moi(f"cw_{k}_loi", f"cw_{k}", [(DA._tron(ct["G0"], L * 0.085), (120, 160, 220))])

    by_slot = {}
    for a in AG["atts"]:
        if a.get("region") in imgs_ho:
            by_slot.setdefault(a["slot"], []).append(a)

    THAY = {d["slot"]: (t_, d) for t_, d in MOI.items() if isinstance(d, dict) and d.get("slot")}

    def them(slot_goc, ten, hien):
        ats = by_slot.get(slot_goc)
        if not ats:
            return
        if slot_goc == "xiabanshen_02":
            them_chan("xa")
        if slot_goc in THAY:                              # mảnh đổi dáng: ô cứng 4 đỉnh trên xương ghi trong moi.json
            t_, d = THAY[slot_goc]
            sk.slot(ten, d["xuong"], t_, an=not hien)
            gan_cung(ten, t_, d["xuong"], np.array(d["the_gioi"], float) + np.array(CHINH.get(t_, (0.0, 0.0))))
        else:
            mac = next((a for a in ats if a["cur"]), ats[0])
            sk.slot(ten, "move", mac["att"], an=not hien)
            for a in ats:
                gan(ten, a)
            sk._slot(ten)["bone"] = sk.atts[ten][mac["att"]]["verts"][0][0][0]
        if slot_goc == "xiabanshen_02":
            them_chan("gan")

    if THAT_VONG:                                          # vòng hào quang sau cùng
        manh_moi("hao_quang", "hao_quang", None)
    for k in (("tren_xa", "tren_gan", "duoi_xa", "duoi_gan") if THAT_CANH else DA.THU_TU_CANH):   # bốn cánh sau mọi thứ
        them_canh(k)
    cho_chen = {}
    for m in DONG:
        for kk in BAN[m]:
            hang_ = [list(F["o"]).index(m) for c in USE for F in S[c]["frames"] if neo(F["o"], m) == kk]
            cho_chen.setdefault(kk, []).append((float(np.mean(hang_)) if hang_ else 0.0, m))
    for k in range(len(STAT) + 1):
        for _, m in sorted(cho_chen.get(k, [])):
            if SL[m] in BO_SLOT:
                continue
            them(SL[m], ten_ban(m, k), hien=(hinh0[m][0] is not None and k == NEO0[m]))
        if k < len(STAT):
            s_ = STAT[k]
            if SL[s_] in BO_SLOT:
                continue
            them(SL[s_], SL[s_], hien=hinh0[s_][0] is not None)

    # ---- điểm bám cổ chân trên xương xích của họ (khung 0 idle)
    for s, xb in XICH.items():
        info_chan[s]["H0"] = np.linalg.solve(Wi["xiabanshen_02"], np.array([*info_chan[s].get("A", info_chan[s]["C"]), 1.0]))[:2]
        info_chan[s]["bam"] = np.linalg.solve(Wi[xb], np.array([*info_chan[s]["C"], 1.0]))[:2]
        info_chan[s]["ban0"] = np.linalg.solve(Wi["move"], np.array([*info_chan[s]["C"], 1.0]))[:2]
    # ---- đầu quyền trượng (chỗ bắn / tụ chiêu): giữa bánh răng fazhang_05
    # ---- quỹ đạo: mỗi hành tinh thêm một slot "phía sau" (sau_<xương>) chèn ngay trước slot Mặt Trời, cùng hình, cùng xương
    for b_ in QUY:
        goc_sl = next((sl["name"] for sl in sk.slots if sl["name"].split("@")[0] == b_), None)
        if goc_sl is None or "fazhang_06" not in sk.si:
            continue
        ten_h = list(sk.atts[goc_sl])[0]
        sk.slot(f"sau_{b_}", b_, ten_h, an=True, truoc="fazhang_06")
        sk.atts[f"sau_{b_}"][ten_h] = dict(sk.atts[goc_sl][ten_h])
        sk.luoi[(f"sau_{b_}", ten_h)] = sk.luoi[(goc_sl, ten_h)]
    sc = np.array(MOI["mat_troi"]["the_gioi"], float).mean(0) if "mat_troi" in MOI else Wi["fazhang_06"][:2, 2]
    sun_c = np.linalg.solve(Wi["fazhang_06"], np.array([sc[0], sc[1], 1.0]))[:2]
    pl_c = {}
    for b_, m_ in (("fazhang_03", "sao_thuy"), ("fazhang_04", "sao_hoa"), ("fazhang_05", "trai_dat")):
        c_ = np.array(MOI[m_]["the_gioi"], float).mean(0) if m_ in MOI else Wi[b_][:2, 2]
        pl_c[b_] = np.linalg.solve(Wi[b_], np.array([c_[0], c_[1], 1.0]))[:2]

    # ---- HIỆU ỨNG trong rig: slot ẩn mặc định, vẽ trên cùng. Hình chữ nhật 4 đỉnh trong hệ xương (V_loc: trên trái, trên phải, dưới phải,
    # dưới trái), ảnh đứng thẳng theo trục xương
    sk.xuong("mieng", "fazhang_06", float(sun_c[0]), float(sun_c[1]))            # tâm Mặt Trời: chỗ tụ / bắn
    sk.xuong("far", "root", *FAR)
    Wi = sk.the_gioi()

    def fx_slot(slot, bone, ten_anh, rong, cao_, neo=(0.5, 0.5)):
        im = anh_cua(ten_anh)
        x0, y1 = -rong * neo[0], cao_ * neo[1]              # neo: điểm trên ảnh (x phải, y XUỐNG từ mép trên) đặt vào gốc xương
        Vl = np.array([[x0, y1], [x0 + rong, y1], [x0 + rong, y1 - cao_], [x0, y1 - cao_]], float)
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.slot(slot, bone, ten_anh, an=True)
        if bone not in Wi:
            Wi.update(sk.the_gioi())
        Vw = np.array([(Wi[bone] @ np.array([v[0], v[1], 1.0]))[:2] for v in Vl])
        sk.atts[slot][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": tris, "hull": 4, "V": Vw,
                                  "verts": [[(bone, float(v[0]), float(v[1]), 1.0)] for v in Vl], "width": im.width, "height": im.height}
        sk.luoi[(slot, ten_anh)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot)

    def kich(ten):                                         # tỉ lệ rộng / cao của ảnh
        im = Image.open(os.path.join(MANH, ten + ".png"))
        return im.width / im.height
    for t_ in MAU_CHO:
        fx_anh(t_)
    # đánh thường: tia lửa nứt đất (fly_n*), ấn + cột sáng ở chân đối thủ (con của far, hạ xuống đất)
    for k in range(N_NUT):
        sk.xuong(f"fly_n{k}", "root", 0.0, 0.0)
        sk.xuong(f"nut{k}", f"fly_n{k}", 0.0, 0.0)
        h_ = 0.30 * CAO0 * (0.75 + 0.5 * k / max(1, N_NUT - 1))
        fx_slot(f"fx_nut{k}", f"nut{k}", "fx_cot", h_ * kich("fx_cot"), h_, neo=(0.5, 1.0))
    sk.xuong("ff_an", "far", 0.0, -FAR[1])
    fx_slot("fx_an", "ff_an", "fx_an", 0.95 * CAO0, 0.95 * CAO0 * 0.30)
    sk.xuong("ff_cot", "far", 0.0, -FAR[1])
    fx_slot("fx_cot", "ff_cot", "fx_cot", 1.5 * CAO0 * kich("fx_cot"), 1.5 * CAO0, neo=(0.5, 1.0))
    # chiêu mana: chuỗi đoạn tia + ba hành tinh thẳng hàng (fly_t*, fly_p*), nổ mặt trời ở đối thủ
    for j in range(N_TIA):
        sk.xuong(f"fly_t{j}", "root", 0.0, 0.0)
        sk.xuong(f"tia{j}", f"fly_t{j}", 0.0, 0.0)
        fx_slot(f"fx_tia{j}", f"tia{j}", "fx_tia", 1.0, 1.0)     # cỡ thật đặt bằng tỉ lệ trong clip (dài theo quãng, dày theo đoạn)
    for j, (ma, anh_p, k_) in enumerate(HANH):
        sk.xuong(f"fly_p{j}", "root", 0.0, 0.0)
        sk.xuong(f"p{j}", f"fly_p{j}", 0.0, 0.0)
        im_ = Image.open(os.path.join(MANH, anh_p + ".png"))
        fx_slot(f"fx_p{j}", f"p{j}", anh_p, im_.width * k_, im_.height * k_)
    sk.xuong("fly_s", "root", 0.0, 0.0)                    # bản sao Mặt Trời bay lên đỉnh cột (chiêu mana)
    sk.xuong("s_bay", "fly_s", 0.0, 0.0)
    im_ = Image.open(os.path.join(MANH, "mat_troi.png"))
    fx_slot("fx_s", "s_bay", "mat_troi", im_.width * K_SUN, im_.height * K_SUN)
    sk.xuong("ff_no", "far", 0.0, 0.0)
    fx_slot("fx_no", "ff_no", "mat_troi", im_.width * 3.2, im_.height * 3.2)
    # chiêu cuối: nhật thực trên Mặt Trời; ba thiên thạch (đuôi lửa + hành tinh to) rơi xuống far, mỗi cú một vết nổ
    fx_slot("fx_nhat_thuc", "mieng", "fx_nhat_thuc", 380.0, 380.0)
    for j, (ma, anh_p, k_) in enumerate(HANH):
        sk.xuong(f"ff_m{j}", "far", 0.0, 0.0)
        im_ = Image.open(os.path.join(MANH, anh_p + ".png"))
        r_ = max(im_.width, im_.height) * (2.4 if ma != "dat" else 2.6)
        fx_slot(f"fx_duoi{j}", f"ff_m{j}", "fx_duoi", r_ * 2.6, r_ * 2.6 / kich("fx_duoi"), neo=(0.86, 0.5))
        fx_slot(f"fx_m{j}", f"ff_m{j}", anh_p, r_ * im_.width / max(im_.width, im_.height), r_ * im_.height / max(im_.width, im_.height))
        sk.xuong(f"ff_no{j}", "far", 0.0, 0.0)
        fx_slot(f"fx_no{j}", f"ff_no{j}", "mat_troi", r_ * 1.5, r_ * 1.5)

    for e, m in (("trung", "khung đòn trúng"), ("vo_canh", "appear: bung cánh"), ("bay_len", "appear: đập cánh cất cánh (gió, bụi)"),
                 ("cham_dat", "appear: hạ cánh dộng đất (bụi, sóng đất)"), ("nga", "die: đổ xuống"), ("tu", "tụ năng lượng vào Mặt Trời"),
                 ("dap", "đánh thường: đầu trượng nện đất"), ("an", "đánh thường: Ấn Mặt Trời nở dưới chân đối thủ"),
                 ("thang_hang", "chiêu mana: ba hành tinh xếp thẳng hàng"),
                 ("len_dinh", "chiêu mana: Mặt Trời lên đỉnh cột trên đầu đối thủ"), ("ban", "chiêu mana: Mặt Trời phóng tia"),
                 ("bay", "chiêu cuối: vua bay lên, hào quang nở"), ("quy_dao", "chiêu cuối: hành tinh bay vòng"),
                 ("nhat_thuc", "chiêu cuối: nhật thực (màn tối)"), ("phong", "chiêu cuối: hành tinh vọt lên trời"),
                 ("no", "chiêu cuối: một thiên thạch nện (chuỗi: thứ tự)"), ("sang", "chiêu cuối: Mặt Trời sáng lại")):
        sk.su_kien(e, m)
    hien0 = {s["name"] for s in sk.slots if s.get("alpha", 1) > 0 and not s.get("an")}
    cao = float(max(sp["V"][:, 1].max() for sn, sl in sk.atts.items() if sn in hien0 and not sn.startswith(("cw_", "canh_", "hao_quang"))
                    for sp in sl.values() if "V" in sp))
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao (không tính cánh) {cao:.0f}; slot di động: "
          + ", ".join(f"{SL[m]} {BAN[m]}" for m in DONG))
    return sk, dict(cao=cao, chan=info_chan, canh=info_canh, Wi=Wi, sun_c=sun_c, pl_c=pl_c)


# ---------------------------------------------------------------- chân, cánh: mỗi khung
def dat_chan(sk, P, info, khong=0.0, chuc=0.0):
    """giải hai chân sau khi thân đã đặt dáng. khong: 0 = cổ chân bám điểm trên xích của họ (dưới đất), 1 = treo theo hông (trên không,
    gối co thêm 30, mũi chân chúc `chuc` độ)."""
    W = sk.the_gioi(P)
    Wi = info["Wi"]
    if any(c.get("long") for c in info["chan"].values()):
        for s, c in info["chan"].items():
            dat_ = (W[XICH[s]] @ np.array([*c["bam"], 1.0]))[:2]
            Hn = (W["xiabanshen_02"] @ np.array([*c["H0"], 1.0]))[:2]
            if khong > 0:                                   # trên không: cổ chân treo dưới hông đúng dáng nghỉ, ngắn lại 8 %
                v0 = c["C"] - c["A"]
                R = W["xiabanshen_02"][:2, :2] / max(1e-9, math.hypot(*W["xiabanshen_02"][:2, 0]))
                dat_ = dat_ * (1 - khong) + (Hn + (R @ v0) * 0.92) * khong
            lp = np.linalg.solve(W["move"], np.array([dat_[0], dat_[1], 1.0]))[:2]
            P.move(f"ban_{s}", float(lp[0] - c["ban0"][0]), float(lp[1] - c["ban0"][1]))
            P.rot(f"ban_{s}", -chuc * khong)
            W = sk.the_gioi(P)
            for b_, goc_ in ((f"dui_{s}", math.atan2(*(dat_ - Hn)[::-1])), (f"ong_{s}", math.atan2(*(Hn - dat_)[::-1]))):
                cur = math.atan2(W[b_][1, 0], W[b_][0, 0])
                P.rot(b_, ((math.degrees(goc_ - cur) + 180) % 360) - 180)
                W = sk.the_gioi(P)
        return
    for s, c in info["chan"].items():
        dat_ = (W[XICH[s]] @ np.array([*c["bam"], 1.0]))[:2]
        if khong > 0:
            rel = Wi["xiabanshen_02"]
            treo = (W["xiabanshen_02"] @ np.linalg.solve(rel, np.array([c["C"][0], c["C"][1] + 34.0, 1.0])))[:2]
            dat_ = dat_ * (1 - khong) + treo * khong
        ik_hai_doan(sk, P, f"dui_{s}", f"ong_{s}", dat_, uon=c["uon"])
        W = sk.the_gioi(P)
        L2 = sk.bones[sk.bi[f"ong_{s}"]]["length"]
        tip = (W[f"ong_{s}"] @ np.array([L2, 0.0, 1.0]))[:2]
        lp = np.linalg.solve(W["move"], np.array([tip[0], tip[1], 1.0]))[:2]
        P.move(f"ban_{s}", float(lp[0] - c["ban0"][0]), float(lp[1] - c["ban0"][1]))
        P.rot(f"ban_{s}", -chuc * khong)                 # mũi chân (bên phải) chúc xuống


def quanh_mat_troi(sk, P, info, t, w_=1.0):
    """ba hành tinh bay quanh Mặt Trời trên trượng theo elip nghiêng (QUY), đặt SAU khi clip đã đặt dáng: dời xương hành tinh (con all2) từ chỗ
    clip để tới chỗ trên quỹ đạo (trộn w_), nửa dưới elip vẽ trước Mặt Trời và to hơn, nửa trên dùng slot sau_<xương> (vẽ sau Mặt Trời)."""
    if w_ <= 0:
        return
    W = sk.the_gioi(P)
    S = (W["fazhang_06"] @ np.array([*info["sun_c"], 1.0]))[:2]
    c, s_ = math.cos(NGHIENG), math.sin(NGHIENG)
    for b_, (rx, kk, n, ph) in QUY.items():
        if b_ not in sk.bi:
            continue
        th = 2 * math.pi * (n * t / CHU_QUY + ph)
        x, y = rx * math.cos(th), rx * kk * math.sin(th)
        dich = S + np.array([c * x - s_ * y, s_ * x + c * y])
        Wp = W[sk.bones[sk.bi[b_]]["parent"]]
        lp = np.linalg.solve(Wp, np.array([dich[0], dich[1], 1.0]))[:2] - np.linalg.solve(Wp, np.array([*W[b_][:2, 2], 1.0]))[:2]
        P.move(b_, float(lp[0] * w_), float(lp[1] * w_))
        truoc = math.sin(th) < 0
        k_ = 1.0 + 0.12 * w_ * (-math.sin(th))
        P.scale(b_, k_, k_)
        hien = 0.0
        for sl in sk.slots:
            if sl["name"].split("@")[0] == b_:
                a_ = P.alpha.get(sl["name"], sl["alpha"])
                hien = max(hien, a_)
                if not truoc and w_ > 0.5:
                    P.alpha[sl["name"]] = 0.0
        if f"sau_{b_}" in sk.si:
            P.alpha[f"sau_{b_}"] = hien if (not truoc and w_ > 0.5) else 0.0


def song_vo(ph):
    """một chu kỳ vỗ cánh, ph ∈ [0, 1): +1 = cuối nhịp đập xuống, −1 = đỉnh nhịp hất lên. Hất lên 60 % (chậm), đập xuống 40 % (nhanh)."""
    ph %= 1.0
    if ph < 0.6:
        return math.cos(math.pi * ph / 0.6)
    return -math.cos(math.pi * (ph - 0.6) / 0.4)


LECH_PHA = {"tren_gan": 0.0, "tren_xa": 0.03, "duoi_gan": 0.10, "duoi_xa": 0.13}
TI_CANH = {"tren_gan": 1.0, "tren_xa": 0.9, "duoi_gan": 0.8, "duoi_xa": 0.75}


def vo_canh(P, info, t, chu_ky, bien, xoe=10.0, nhap=0.0, cao=1.0, them=0.0):
    """vỗ bốn cánh. bien: biên độ tay cánh (độ); xoe: (bản giữ chỗ) lông xoè khi cánh giơ; nhap: gốc cánh nhấp nhô (phần chiều cao); them: góc
    cộng thêm cho mọi cánh theo chiều quạt (+ = hạ, − = giơ).
    Cánh lưới liền (bản da mình, người dùng 2026-11-17 "chuyển động của cánh khi bay chưa đẹp"): như cánh chim: ĐẬP XUỐNG (40 %, nhanh) cánh
    duỗi thẳng, ngọn trễ (cong ngược lên) rồi bắt kịp; HẤT LÊN (60 %, chậm) cánh GẬP ở cổ cánh (nửa ngoài rủ xuống, cả cánh ngắn lại ~10 %)
    rồi duỗi ra ở đỉnh."""
    for k, ct in info["canh"].items():
        q = ct["q"]
        ph = t / chu_ky + LECH_PHA[k]
        w = song_vo(ph)
        b = bien * TI_CANH[k]
        P.rot(f"cw_{k}", q * (b * w + them))
        P.move(f"cw_{k}", 0.0, nhap * cao * math.sin(2 * math.pi * (ph + 0.15)))
        if ct.get("luoi"):
            u = ph % 1.0
            gap = math.sin(math.pi * u / 0.6) if u < 0.6 else 0.0          # gập nhiều nhất giữa nhịp hất lên
            muc = min(1.0, b / 28.0)
            w1, w2 = song_vo(ph - 0.07), song_vo(ph - 0.14)
            P.rot(f"cw_{k}_co", q * (0.38 * b * (w1 - w) + 24.0 * gap * muc))
            P.rot(f"cw_{k}_ngon", q * (0.38 * b * (w2 - w1) + 16.0 * gap * muc))
            P.scale(f"cw_{k}_tay", 1.0 - 0.10 * gap * muc, 1.0)
            continue
        for b_, tj in ct["la"]:
            tre = song_vo(ph - 0.05 - 0.05 * tj)
            P.rot(b_, q * (0.35 * b * (tre - w) + xoe * tj * (-w)))


def gap_canh(P, info, g):
    """khép bốn cánh (g = 0 xoè như dáng gốc, 1 = khép sát sau lưng: tay cánh hạ / dựng, nửa ngoài gập vào)."""
    if g <= 0:
        return
    for k, ct in info["canh"].items():
        q = ct["q"]
        P.rot(f"cw_{k}", q * (-32.0 if k.startswith("tren") else 44.0) * g)   # cánh trên dựng đứng sát nhau, cánh dưới rủ xuống
        P.scale(f"cw_{k}", 1.0 - 0.22 * g, 1.0 - 0.22 * g)
        if ct.get("luoi"):
            P.rot(f"cw_{k}_co", q * 26.0 * g)
            P.rot(f"cw_{k}_ngon", q * 20.0 * g)
            continue
        for b_, tj in ct["la"]:
            P.rot(b_, -q * (86.0 if b_[-2:-1].isdigit() or b_[-1].isdigit() else 30.0) * tj * g)


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    out = []
    cao = info["cao"]
    D_ID = CD["idle_01"][0]

    def nen(clip, t, P, lap=False):
        dat(P, mau(clip, t, lap))
        hien_theo_ho(sk, P, clip, t, lap)

    # ---- IDLE: idle_01 của họ (1,33 s); chân bám xích; cánh lơ lửng vỗ nhẹ một nhịp, gốc cánh nhấp nhô
    D_IDL = 2 * D_ID                                       # 2,67 s: idle_01 của họ hai vòng, đủ chỗ cho quỹ đạo 3 / 2 / 1 vòng khép kín

    def idle(t, P):
        u = t if t < D_IDL - 1e-6 else 0.0
        nen("idle_01", u % D_ID, P)
        vo_canh(P, info, u, D_ID, 5.0, 4.0, 0.010, cao)
        dat_chan(sk, P, info)
        quanh_mat_troi(sk, P, info, u)
    out.append(Clip("idle", D_IDL, idle, loop=True))

    # ---- WALK = BAY: thân của run_01 (chúi tới, trượng ngả), nâng 0,24 chiều cao, nhấp nhô ngược nhịp cánh (lên khi đập xuống); chân
    # treo; cánh vỗ mạnh một nhịp mỗi vòng
    # người dùng 2026-11-17 "chuyển động của cánh khi bay chưa đẹp": cánh to vỗ 0,67 s / nhịp quá vội → 1,33 s một nhịp vỗ lớn (thân run_01
    # chạy hai vòng), nhấp nhô thân theo nhịp cánh (đập xuống thì thân bốc lên, trễ 0,1 nhịp)
    D_R = CD["run_01"][0]
    D_W = 2 * D_R
    H_BAY = 0.24 * cao

    def walk(t, P):
        u = t if t < D_W - 1e-6 else 0.0
        nen("run_01", u % D_R, P)
        w = song_vo(u / D_W - 0.10)
        P.move("all", 0.0, H_BAY - 0.04 * cao * w)
        P.rot("all", 2.5 * w)
        vo_canh(P, info, u, D_W, 32.0, 12.0, 0.0, cao)
        dat_chan(sk, P, info, khong=1.0, chuc=5.0)
        quanh_mat_troi(sk, P, info, u)
    out.append(Clip("walk", D_W, walk, loop=True))

    # ---- HIT: hit_01 của họ; cánh giật trễ (khép nửa nhịp rồi bật lại)
    def hit(t, P):
        nen("hit_01", t, P)
        g = math.sin(math.pi * min(1.0, t / 0.3)) * 0.35
        gap_canh(P, info, g)
        vo_canh(P, info, t, D_ID, 5.0, 4.0, 0.010, cao)
        dat_chan(sk, P, info)
        quanh_mat_troi(sk, P, info, t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ---- DIE: die_01 của họ (gục, đầu quyền trượng rơi), cánh tắt dần: rủ xuống, rơi, mờ; cả con mờ 0,32 s cuối
    D_DIE0 = CD["die_01"][0]
    D_DIE = D_DIE0 + 0.55

    def die(t, P):
        nen("die_01", t, P)
        r = em((t - 0.25) / 0.9)
        for k, ct in info["canh"].items():
            P.rot(f"cw_{k}", ct["q"] * 70.0 * r)
            P.move(f"cw_{k}", 0.0, -0.25 * cao * r * r)
            for b_, tj in ct["la"]:
                P.rot(b_, ct["q"] * 25.0 * tj * r)
            if ct.get("luoi"):
                P.rot(f"cw_{k}_co", ct["q"] * 22.0 * r)
                P.rot(f"cw_{k}_ngon", ct["q"] * 18.0 * r)
        fc = 1.0 - em((t - 0.6) / 0.5)
        for sl in sk.slots:
            if sl["name"].startswith(("cw_", "canh_", "hao_quang")):
                P.alpha[sl["name"]] = fc
        dat_chan(sk, P, info)
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.86, "nga", "")]))

    # ---- APPEAR (người dùng: "bay lên rồi hạ cánh"): hiện dần ở đất, ngồi thụp, cánh khép → BUNG cánh (vo_canh) → ĐẬP cánh cất cánh
    # (bay_len) vọt lên 0,55 chiều cao → lượn hai nhịp → hạ xuống, giơ cánh hãm → DỘNG đất (cham_dat): khuỵu gối, cánh đập xuống → đứng dậy,
    # cánh về dáng lơ lửng
    T_BUNG, T_CAT, T_DINH, T_HA, T_CHAM, D_AP = 0.22, 0.42, 0.70, 1.30, 1.58, 2.25
    H_AP = 0.55 * cao

    def appear(t, P):
        nen("idle_01", 0.0, P)
        if t < T_CAT:                                         # ngồi thụp, cánh khép rồi bung
            ngoi = em(t / T_BUNG) * 0.6 + 0.4 * em((t - T_BUNG) / (T_CAT - T_BUNG))
            P.move("all", 0.0, -40.0 * ngoi)
            g = 1.0 - em((t - 0.06) / (T_BUNG - 0.06)) if t < T_BUNG else 0.0
            gap_canh(P, info, g)
            if t >= T_BUNG:
                vo_canh(P, info, 0.0, 1.0, 0.0, 0.0, 0.0, cao, them=-26.0 * em((t - T_BUNG) / 0.12))
            dat_chan(sk, P, info)
        elif t < T_HA:                                        # cất cánh + lượn
            q = em((t - T_CAT) / (T_DINH - T_CAT))
            y = -40.0 + (H_AP + 40.0) * (1 - (1 - q) ** 2)
            if t > T_DINH:
                y = H_AP + 0.03 * cao * math.sin(2 * math.pi * (t - T_DINH) / 0.48)
            P.move("all", 0.0, y)
            P.rot("all", 3.0 * math.sin(2 * math.pi * (t - T_CAT) / 0.6))
            ky = 0.48                                         # nhịp vỗ khi lượn (cánh to: chậm)
            vo_canh(P, info, (t - T_CAT) + 0.6 * ky, ky, 34.0, 14.0, 0.0, cao)
            dat_chan(sk, P, info, khong=em((t - T_CAT) / 0.15), chuc=5.0)
        elif t < T_CHAM:                                      # hạ xuống nhanh dần, cánh giơ cao hãm
            q = (t - T_HA) / (T_CHAM - T_HA)
            P.move("all", 0.0, H_AP * (1 - q * q) + 0.03 * cao * math.sin(2 * math.pi * (T_HA - T_DINH) / 0.48) * (1 - q))
            vo_canh(P, info, 0.0, 1.0, 0.0, 0.0, 0.0, cao, them=-30.0 * em(q / 0.4))
            dat_chan(sk, P, info, khong=1.0 - em((q - 0.55) / 0.45), chuc=5.0)
        else:                                                  # chạm đất: khuỵu, cánh đập xuống, đứng dậy
            s = t - T_CHAM
            khuy = (em(s / 0.06) if s < 0.06 else 1.0) * (1.0 - em((s - 0.10) / 0.45))
            P.move("all", tat_dan(t, T_CHAM, 0.012 * cao, 14.0, 0.08), -46.0 * khuy)
            dap = (em(s / 0.08) if s < 0.08 else 1.0) * (1.0 - em((s - 0.12) / 0.5))
            vo_canh(P, info, 0.0, 1.0, 0.0, 0.0, 0.0, cao, them=-30.0 * (1 - em(s / 0.07)) + 22.0 * dap)
            dat_chan(sk, P, info)
        quanh_mat_troi(sk, P, info, t)
        a_ = min(1.0, t / 0.10)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(T_BUNG, "vo_canh", ""), (T_CAT, "bay_len", ""), (T_CHAM, "cham_dat", "")]))

    # ---- các đòn của họ (bản thô để xem cánh, chân khi đánh; chưa phải bản cuối): attack = skill_01_1, cast = skill_02, skill = skill_04,
    # cùng skill_01_2, skill_01_3, skill_03 để người dùng xem đủ bốn skill
    # ================================================================ BA CHIÊU (người dùng duyệt đề xuất 2026-11-17 "làm đi")
    PL = ("fazhang_03", "fazhang_04", "fazhang_05")       # Sao Thủy, Sao Hỏa, Trái Đất thật (mảnh của họ đã thay)

    def an_hanh_tinh(P, a_):
        for sl in sk.slots:
            if sl["name"].split("@")[0] in PL:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])

    def mieng_tg(P):
        return sk.the_gioi(P)["mieng"][:2, 2].copy()

    def tu_sun(P, k_, quay=0.0):
        P.scale("fazhang_06", k_, k_)
        if quay:
            P.rot("fazhang_06", quay)

    # ---------------- ĐÁNH THƯỜNG "Nhật Ấn" (skill_01_1): lấy đà, Mặt Trời bừng to; vụt qua đầu (vệt cung lửa); nện đất; tia lửa nứt chạy tới
    # đối thủ; Ấn Mặt Trời nở dưới chân đối thủ + cột sáng
    U_ATK = [(0.0, 0.0), (0.40, 0.30), (0.52, 0.40), (0.90, 0.72), (1.30, 1.0)]
    D_ATK, T_DAP, T_AN = 1.30, 0.52, 0.76
    T_TR_A = T_AN + 0.04
    P0 = Pose()
    dat(P0, mau("skill_01_1", 0.40))
    A_DAP = np.array([mieng_tg(P0)[0], 0.0])               # đầu trượng chạm đất (chiếu xuống đất)
    # vệt cung lửa: ảnh fx_cung lật ngang phủ hộp đường bay của Mặt Trời trong cú vụt (u 0,29 → 0,40)
    duong = []
    for u_ in np.linspace(0.29, 0.40, 12):
        P_ = Pose()
        dat(P_, mau("skill_01_1", u_))
        duong.append(mieng_tg(P_))
    duong = np.array(duong)
    bx0, by0 = duong.min(0) - 90
    bx1, by1 = duong.max(0) + 90
    sk.xuong("fx_cung_b", "root", 0.0, 0.0)
    if "fx_cung" not in sk.images:
        g_ = Image.open(os.path.join(MANH, "fx_cung.png")).convert("RGBA")
        g_ = g_.convert("RGBa").resize((g_.width // 2, g_.height // 2), Image.LANCZOS).convert("RGBA")
        sk.anh("fx_cung", anh.loang_mau(g_))
    imc = sk.images["fx_cung"]
    Vl = np.array([[bx1, by1], [bx0, by1], [bx0, by0], [bx1, by0]], float)             # lật ngang: góc trên trái ảnh → trên phải hộp
    uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
    sk.slot("fx_cung", "fx_cung_b", "fx_cung", an=True)
    sk.atts["fx_cung"]["fx_cung"] = {"type": "mesh", "path": "fx_cung", "uv": uv, "tris": np.array([[0, 1, 2], [0, 2, 3]]), "hull": 4,
                                     "V": Vl, "verts": [[("fx_cung_b", float(v[0]), float(v[1]), 1.0)] for v in Vl],
                                     "width": imc.width, "height": imc.height}
    sk.luoi[("fx_cung", "fx_cung")] = Luoi(uv * np.array([imc.width, imc.height], float), np.array([[0, 1, 2], [0, 2, 3]]), 4, 4,
                                          imc.width, imc.height, ten="fx_cung")

    def attack(t, P):
        u = tq(t, U_ATK)
        nen("skill_01_1", u, P)
        tu = em((t - 0.08) / 0.32) * (1 - em((t - 0.58) / 0.30))
        tu_sun(P, 1.0 + 0.75 * tu, -360.0 * em(t / D_ATK))
        lay = em(t / 0.40) * (1 - em((t - 0.40) / 0.12))
        dap = em((t - 0.44) / 0.10) * (1 - em((t - 0.64) / 0.5))
        vo_canh(P, info, t, D_ID, 4.0, 3.0, 0.008, cao, them=-16.0 * lay + 22.0 * dap)
        P.move("all", tat_dan(t, T_DAP, 0.014 * cao, 15.0, 0.08), -12.0 * giat(t, T_DAP, 0.03, 0.22))
        P.alpha["fx_cung"] = em((t - 0.42) / 0.04) * (1 - em((t - 0.54) / 0.12))
        F = FAR
        for k in range(N_NUT):
            w = (k + 1) / (N_NUT + 1)
            P.move(f"fly_n{k}", float(w * F[0]), float(w * F[1]))
            c = (1 - w) * A_DAP + w * np.array([0.0, -F[1]])
            P.move(f"nut{k}", float(c[0]), float(c[1]))
            tk = T_DAP + 0.02 + 0.032 * k
            mo = em((t - tk) / 0.05) * (1 - em((t - tk - 0.12) / 0.09))
            P.alpha[f"fx_nut{k}"] = 1.0 if mo > 0.02 else 0.0
            P.scale(f"nut{k}", 0.6 + 0.4 * mo, max(0.02, mo))
        an_ = em((t - T_AN) / 0.08)
        tan = 1 - em((t - 1.06) / 0.18)
        P.alpha["fx_an"] = (1.0 if (T_AN <= t < 1.24) else 0.0) * (tan if t > 1.06 else 1.0)
        k_ = (0.3 + 0.78 * an_ - 0.08 * em((t - T_AN - 0.08) / 0.08)) * (1 - 0.25 * (1 - tan))
        P.scale("ff_an", k_, k_)
        cot = em((t - T_AN - 0.02) / 0.08)
        P.alpha["fx_cot"] = 1.0 if (T_AN + 0.02 <= t < 1.20) else 0.0
        P.scale("ff_cot", (0.5 + 0.5 * cot) * (1 - 0.7 * em((t - 1.0) / 0.18)), max(0.02, cot))
        dat_chan(sk, P, info)
        quanh_mat_troi(sk, P, info, t)
    out.append(Clip("attack", D_ATK, attack, ev=[(0.10, "tu", ""), (T_DAP, "dap", ""), (T_AN, "an", ""), (T_TR_A, "trung", "")],
                    trung=T_TR_A))

    # ---------------- CHIÊU MANA "Tam Tinh Quang Pháo" (skill_02; người dùng 2026-11-17: "cho các tiểu hành tinh đứng thẳng hàng trên đầu của đối
    # thủ rồi mặt trời lên trên cùng sau đó bắn tia sáng xuống"): giơ trượng lên trời, ba hành tinh rời quỹ đạo bay vòng cung tới XẾP THÀNH CỘT
    # trên đầu đối thủ (Sao Thủy thấp nhất, Sao Hỏa, Trái Đất); Mặt Trời rời trượng bay lên ĐỈNH cột; vua vụt trượng chĩa tới ra lệnh; Mặt Trời
    # phóng tia THẲNG XUỐNG xuyên Trái Đất, Sao Hỏa, Sao Thủy (mỗi lần qua một hành tinh tia to thêm), nổ trên người đối thủ; tất cả bay về trượng
    U_CAST = [(0.0, 0.0), (0.45, 0.30), (1.00, 0.55), (1.10, 0.72), (1.70, 1.10), (2.10, 1.367)]
    D_CAST, T_BAN = 2.10, 1.10
    T_RA = (0.18, 0.25, 0.32)                               # từng hành tinh rời quỹ đạo
    T_TOI = (0.62, 0.69, 0.76)                              # tới chỗ trong cột
    T_S0, T_S1 = 0.55, 0.95                                 # Mặt Trời rời trượng → tới đỉnh cột
    T_TR_C, T_TAT, T_VE0, T_VE1 = T_BAN + 0.14, 1.60, 1.62, 1.95
    F = FAR
    YS = Y_SUN * CAO0
    Y_DAY = -0.20 * CAO0                                    # tia đâm qua tâm đối thủ xuống thêm một đoạn
    L_SEG = (YS - Y_DAY) / N_TIA * 1.40
    PLB = ("fazhang_03", "fazhang_04", "fazhang_05")        # đúng thứ tự HANH (Thủy, Hỏa, Trái Đất)
    pl_c = info["pl_c"]

    def bay(fly, con, A, dich, q, vong):
        """bản sao đi từ A (thế giới, theo trượng) tới far + dich (q 0 → 1), vồng lên `vong`; fly = q · far để game co quãng."""
        X = (1 - q) * A + q * (F + dich) + np.array([0.0, vong * math.sin(math.pi * q)])
        P_ = bay.P
        P_.move(fly, float(q * F[0]), float(q * F[1]))
        c = X - q * F
        P_.move(con, float(c[0]), float(c[1]))

    def cast(t, P):
        u = tq(t, U_CAST)
        nen("skill_02", u, P)
        tu = em((t - 0.20) / 0.35) * (1 - em((t - T_S0) / 0.10))
        tu_sun(P, 1.0 + 0.6 * tu, -360.0 * em(t / D_CAST))
        g = giat(t, T_BAN, 0.04, 0.30)
        P.move("all", -0.025 * cao * g, 0.0)
        bung = em((t - 0.20) / 0.30) * (1 - em((t - 1.70) / 0.30))
        vo_canh(P, info, t, 0.40, 3.0 + 3.0 * bung, 2.0, 0.006, cao, them=-18.0 * bung + 16.0 * g)
        if "hao_quang" in sk.bi:
            k_ = 1.0 + 0.15 * bung
            P.scale("hao_quang", k_, k_)
        dat_chan(sk, P, info)
        quanh_mat_troi(sk, P, info, t)                      # hành tinh thật luôn đặt trên quỹ đạo (kể cả lúc ẩn): chỗ cất / đáp của bản sao
        W = sk.the_gioi(P)
        bay.P = P
        # ba hành tinh: rời quỹ đạo → cột → về quỹ đạo
        for j in range(3):
            b_ = PLB[j]
            A = (W[b_] @ np.array([*pl_c[b_], 1.0]))[:2]
            dich = np.array([0.0, Y_COT[j] * CAO0 + 0.02 * CAO0 * math.sin(2 * math.pi * 1.6 * t + j)])
            if T_RA[j] <= t < T_VE1 + 0.0:
                for sl in sk.slots:
                    if sl["name"].split("@")[0] == b_ or sl["name"] == f"sau_{b_}":
                        P.alpha[sl["name"]] = 0.0
                P.alpha[f"fx_p{j}"] = 1.0
                if t < T_VE0:
                    q = em((t - T_RA[j]) / (T_TOI[j] - T_RA[j]))
                else:
                    q = 1 - em((t - T_VE0) / (T_VE1 - T_VE0))
                bay(f"fly_p{j}", f"p{j}", A, dich, q, 0.30 * CAO0)
                qua = math.exp(-((t - (T_BAN + 0.12 * (1 - Y_COT[j] / Y_SUN))) / 0.05) ** 2)     # tia đi qua: nảy to
                k_ = 1.0 + 0.25 * qua
                P.scale(f"p{j}", k_, k_)
            else:
                P.alpha[f"fx_p{j}"] = 0.0
        # Mặt Trời: rời trượng → đỉnh cột → về trượng
        A = W["mieng"][:2, 2]
        if T_S0 <= t < T_VE1:
            for sl in sk.slots:
                if sl["name"].split("@")[0] == "fazhang_06":
                    P.alpha[sl["name"]] = 0.0
            P.alpha["fx_s"] = 1.0
            q = em((t - T_S0) / (T_S1 - T_S0)) if t < T_VE0 else 1 - em((t - T_VE0) / (T_VE1 - T_VE0))
            bay("fly_s", "s_bay", A, np.array([0.0, YS]), q, 0.25 * CAO0)
            sac = math.exp(-((t - (T_BAN - 0.06)) / 0.07) ** 2)                               # dồn sức trước khi bắn
            k_ = (0.65 + 0.35 * em((t - T_S0) / 0.15)) * (1.0 + 0.18 * sac)
            P.scale("s_bay", k_, k_)
            P.rot("s_bay", -240.0 * em((t - T_S0) / 1.4))
        else:
            P.alpha["fx_s"] = 0.0
        # tia thẳng xuống: mọc từ Mặt Trời xuống trong 0,12 s, dày dần sau mỗi hành tinh, rung dày, tắt mỏng dần
        lan = em((t - T_BAN) / 0.12) if t >= T_BAN else 0.0
        mong = 1.0 - em((t - T_TAT) / 0.10)
        for j in range(N_TIA):
            yc = YS - (j + 0.5) / N_TIA * (YS - Y_DAY)
            P.move(f"fly_t{j}", float(F[0]), float(F[1]))
            P.move(f"tia{j}", 0.0, float(yc))
            P.rot(f"tia{j}", -90.0)
            bat = t >= T_BAN and lan >= (j + 0.5) / N_TIA * 0.98 and mong > 0.02
            P.alpha[f"fx_tia{j}"] = 1.0 if bat else 0.0
            day = DAY_TIA[sum(1 for y_ in Y_COT if yc < y_ * CAO0)]
            P.scale(f"tia{j}", L_SEG, max(0.02, day * mong * (1.0 + 0.08 * math.sin(2 * math.pi * 18 * t + j))))
        no = em((t - T_TR_C) / 0.10)
        P.alpha["fx_no"] = (1.0 if (T_TR_C <= t < 1.80) else 0.0) * ((1 - em((t - 1.58) / 0.20)) if t > 1.58 else 1.0)
        P.scale("ff_no", 0.4 + 0.9 * no, 0.4 + 0.9 * no)
        P.rot("ff_no", -90.0 * em((t - T_TR_C) / 0.5))
    out.append(Clip("cast", D_CAST, cast, ev=[(0.25, "tu", ""), (T_TOI[2], "thang_hang", ""), (T_S1, "len_dinh", ""), (T_BAN, "ban", ""),
                                             (T_TR_C, "trung", "")], trung=T_TR_C))

    # ---------------- CHIÊU CUỐI "Nhật Thực Thiên Giáng" (skill_03 + skill_04): vỗ cánh bay lên, hào quang nở to quay nhanh; hành tinh bay vòng
    # quanh vua; giơ trượng lên trời: NHẬT THỰC; hành tinh vọt lên trời rồi rơi xuống đối thủ thành thiên thạch (Thủy, Hỏa, Trái Đất khổng lồ);
    # Mặt Trời sáng lại, hành tinh về trượng, vua đáp
    D_SK = 3.70
    T_B, T_C, T_D, T_E = 0.40, 1.60, 2.45, 3.10
    T_NT, T_SANG = 2.00, 2.98
    ROI = ((2.62, 2.82), (2.74, 2.96), (2.90, 3.20))       # (bắt đầu rơi, chạm) từng thiên thạch
    T_TR_S = ROI[2][1]
    H_LEN = 0.16 * cao
    S_M = np.array([-0.62 * CAO0, 2.1 * CAO0])

    def skill(t, P):
        if t < T_B:
            clip_, u = "skill_03", t / T_B * 0.40
            d_ = mau(clip_, u)
        elif t < T_C:
            clip_, u = "skill_03", 0.45 + (t - T_B) / (T_C - T_B) * (1.60 - 0.45)
            d_ = mau(clip_, u)
        elif t < T_E:                                     # giơ trượng lên trời, GIỮ giơ suốt lúc thiên thạch rơi (nhật thực trên đầu trượng)
            clip_ = "skill_04"
            u = 0.15 + (t - T_C) / (T_D - T_C) * (1.25 - 0.15) if t < T_D else 1.25 + (t - T_D) / (T_E - T_D) * 0.13
            d_ = mau(clip_, u)
            if t < T_C + 0.15:
                d_ = pha_gan(mau("skill_03", 1.60), d_, em((t - T_C) / 0.15))
        else:                                             # hạ trượng: clip của họ giật về trong một khung (1,40 → 1,50) → hoà 0,18 s
            clip_, u = "skill_04", 1.50 + (t - T_E) / (D_SK - T_E) * (2.167 - 1.50)
            d_ = pha_gan(mau("skill_04", 1.38), mau(clip_, u), em((t - T_E) / 0.18))
        dat(P, d_)
        hien_theo_ho(sk, P, clip_, u)
        len_ = em((t - 0.20) / 0.50) * (1 - em((t - 3.22) / 0.30))
        cham = giat(t, 3.50, 0.05, 0.18)
        P.move("all", 0.0, H_LEN * len_ + 0.02 * cao * math.sin(2 * math.pi * (t - 0.7) / 0.8) * len_ - 30.0 * cham)
        bung = em((t - 0.15) / 0.30) * (1 - em((t - 3.25) / 0.35))
        gio = em((t - T_NT) / 0.25) * (1 - em((t - T_D) / 0.10))
        dap = giat(t, T_D, 0.06, 0.40)
        vo_canh(P, info, t, 0.8, 4.0 + 14.0 * bung * (1 - gio), 4.0, 0.006, cao, them=-8.0 * bung - 22.0 * gio + 26.0 * dap)
        if "hao_quang" in sk.bi:
            k_ = 1.0 + 0.45 * em((t - 0.30) / 0.60) * (1 - em((t - 3.20) / 0.40))
            P.scale("hao_quang", k_, k_)
            P.rot("hao_quang", -360.0 * em((t - 0.40) / 2.30))
        tu_sun(P, 1.0 + 0.5 * em((t - 1.70) / 0.30) * (1 - em((t - T_SANG) / 0.25)))
        nt = em((t - T_NT) / 0.15) * (1 - em((t - T_SANG) / 0.10))        # nhật thực: đĩa đen + vành nhật hoa phủ Mặt Trời
        P.alpha["fx_nhat_thuc"] = nt
        k_ = 0.6 + 0.4 * em((t - T_NT) / 0.15)
        P.scale("mieng", k_, k_)
        if 2.52 <= t < 3.30:                               # hành tinh thật: ẩn sau cú vọt lên tới lúc về trượng (nảy to dần)
            an_hanh_tinh(P, 0.0)
        elif t >= 3.30:
            k_ = 0.2 + 0.8 * em((t - 3.30) / 0.14) + 0.12 * math.sin(math.pi * min(1.0, (t - 3.30) / 0.28))
            for b_ in PL:
                P.scale(b_, k_, k_)
        for j, (t0, t1) in enumerate(ROI):                 # thiên thạch rơi chéo từ trời xuống tâm đối thủ (nhanh dần), chạm thì nổ
            if t0 <= t < t1:
                q = (t - t0) / (t1 - t0)
                X = S_M * (1 - q * q)
                P.move(f"ff_m{j}", float(X[0]), float(X[1]))
                P.rot(f"ff_m{j}", math.degrees(math.atan2(-S_M[1], -S_M[0])))
                P.alpha[f"fx_m{j}"] = P.alpha[f"fx_duoi{j}"] = 1.0
            else:
                P.alpha[f"fx_m{j}"] = P.alpha[f"fx_duoi{j}"] = 0.0
            no = em((t - t1) / 0.12)
            P.alpha[f"fx_no{j}"] = (1.0 if (t1 <= t < t1 + 0.34) else 0.0) * ((1 - em((t - t1 - 0.16) / 0.18)) if t >= t1 else 1.0)
            P.scale(f"ff_no{j}", 0.3 + 0.9 * no, 0.3 + 0.9 * no)
            P.rot(f"ff_no{j}", -60.0 * em((t - t1) / 0.4))
        dat_chan(sk, P, info, khong=len_, chuc=5.0)
        quanh_mat_troi(sk, P, info, t, 1.0 - em(t / 0.30) if t < 0.5 else em((t - 3.40) / 0.25))
    out.append(Clip("skill", D_SK, skill, ev=[(0.30, "bay", ""), (0.50, "quy_dao", ""), (T_NT, "nhat_thuc", ""), (T_D, "phong", "")]
                    + [(t1, "no", str(j + 1)) for j, (_, t1) in enumerate(ROI)] + [(T_SANG, "sang", ""), (T_TR_S, "trung", "")],
                    trung=T_TR_S))
    if "hao_quang" in sk.bi:                               # vòng hào quang quay chậm một vòng / 16 s, liền qua mọi clip (game phủ clip aura)
        D_AU = 16.0

        def aura(t, P):
            P.rot("hao_quang", -360.0 * (t % D_AU) / D_AU)
        out.append(Clip("aura", D_AU, aura, loop=True))
    return out


# ---------------------------------------------------------------- nướng (góc liền mạch) + chạy
def nuong(sk, clip):
    n = int(round(clip.dur * FPS)) + 1
    frames = []
    for i in range(n):
        P = Pose()
        clip.fn(min(clip.dur, i / FPS), P)
        frames.append(P)
    for i in range(1, n):
        for b, g in frames[i].t.items():
            a0 = frames[i - 1].t.get(b, [0, 0, 0, 1, 1])[2]
            g[2] -= 360.0 * round((g[2] - a0) / 360.0)
    return frames


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "kiem":
        for c in clips:
            fr = nuong(sk, c)
            xau = {}
            for p, q in zip(fr, fr[1:]):
                for bn in set(p.t) | set(q.t):
                    d = abs(q.t.get(bn, [0, 0, 0, 1, 1])[2] - p.t.get(bn, [0, 0, 0, 1, 1])[2])
                    xau[bn] = max(xau.get(bn, 0), d)
            lon = sorted(((v, k) for k, v in xau.items() if v > 40), reverse=True)[:6]
            print(f"{c.ten:11s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°"))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.5
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang_ = (len(ims) + cot - 1) // cot
        o = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            o.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        o.save(pth)
        print(pth, o.size)
        return
    frames = {c.ten: nuong(sk, c) for c in clips}
    xuat.xuat_het(sk, clips, RA, TEN, "Vua robot (vua_may): final boss đảo Kim" + (" — DA GỐC + chân, cánh GIỮ CHỖ, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=("attack", "cast", "skill"), lao=(), far=("attack", "cast", "skill"),
                  far_aim=("cast",), plain=[sl["name"] for sl in sk.slots if sl["name"].startswith("fx_")], cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.08, "translate": 0.2, "scale": 0.002}, khop_idle=0.2, span=4.0)


if __name__ == "__main__":
    main(sys.argv[1:])
