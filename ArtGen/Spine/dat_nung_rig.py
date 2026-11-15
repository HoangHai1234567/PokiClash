# -*- coding: utf-8 -*-
"""Chiến binh đất nung (dat_nung, tướng thứ 8 đảo Hỏa): rig trên bộ xương của con gốc monster_3625 (FK thuần, mọi mảnh cứng một xương),
chuyển động lấy từ mẫu khung clip của họ (sample.json) + clip tự viết.

Người dùng (2026-11-14):
- appear: các bộ phận bay vào quanh lõi.            - idle: giống họ, sửa khác chút.        - walk: giống họ.
- đánh thường: giống skill_01_1, sửa lại chút.
- chiêu mana: giống skill_04_1 (đâm kiếm vào đối thủ rồi nhiều động tác chém).
- chiêu cuối: dang tay, ngửa lòng bàn tay, kiếm bay lơ lửng ở giữa mũi hướng lên; kiếm phân thân sang hai bên (5 thanh); tất cả kiếm
  hướng về địch rồi bay vào.
- chết: lõi tắt ngỏm, rụng rời từng bộ phận.

Cách dựng:
- Dáng gốc của rig mình = khung 0 idle_01 của họ. Đủ mọi xương của họ (cha – con, biến đổi riêng), thêm root, move, far.
- Slot: mọi slot của họ (kể cả bộ tay / kiếm nhân bản và bàn tay xoè gắn trên tay gần). Thứ tự vẽ đổi trong clip của họ → slot "di động"
  nhân bản theo chỗ chèn (`<slot>@<k>`) như quy_dao_rig.
- BỘ MẢNH RỜI (appear, die): mỗi mảnh đang hiện ở khung 0 idle có thêm một slot `<slot>~r` bám xương rời `r_<slot>` (con của move, gốc ở
  tâm mảnh): clip tự viết đặt từng mảnh trong hệ thế giới (bay vào quanh lõi, rụng xuống đất).
- KIẾM BAY (chiêu cuối): 5 thanh `kiem_k` trên xương `nam_k` (con của `fly_k`, con của root; game co quãng bay theo chỗ đối thủ).
- DN_GOC=1: dựng bằng DA GỐC của họ (thử rig và clip trước khi có da của mình; chỉ xem nội bộ) → inbox/dat_nung_1/rig_goc/.

    dat_nung_rig.py                       dựng, xuất (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    dat_nung_rig.py soi <clip> <giây,..> [tỉ lệ]     khung lớn nền xám → soi_<clip>.png
    dat_nung_rig.py kiem                  bước xoay lớn nhất mỗi khung của từng clip
Chạy qua quai/khoa.py nang. Xương, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ."""
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
from quai.khung import Sk, mat, goc_mat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.luoi import Luoi  # noqa: E402
import dat_nung as G  # noqa: E402

GOC = os.environ.get("DN_GOC") == "1"                      # da GỐC của họ (thử rig)
TU_DO = os.environ.get("DN_TU_DO") == "1" and not GOC      # bản TỰ CHẾ theo concept A (người dùng đã bỏ 2026-11-14): mảnh tự do trong manh/
PART = not GOC and not TU_DO                               # MẶC ĐỊNH: da của mình vẽ đúng khung từng part của họ (manh_part/), nguyên lưới của họ
# DN_NON=1: DẠNG 1 (Viêm Dũng Nhi, chibi; người dùng 2026-11-14: "cho vào game đi rồi làm dạng 1 của tướng này"): cùng xương, cùng lưới, cùng
# clip với dạng 2; khác: tỉ lệ dáng gốc của vài xương (TI_NON: đầu to, giáp, phiến, kiếm nhỏ lại), bớt bốn phiến sau lưng (AN_NON), mảnh đổi kiểu
# dáng riêng ở inbox/dat_nung_non/manh_part2 (thiếu mảnh nào thì lấy của dạng 2). Xuất ra inbox/dat_nung_non/rig/.
NON = os.environ.get("DN_NON") == "1" and os.environ.get("DN_GOC") != "1" and os.environ.get("DN_TU_DO") != "1"
BASE_NON = os.path.join(HERE, "inbox", "dat_nung_non")
TI_NON = {"tou": 1.5, "bone27": 1.2, "bone31": 0.82, "bone32": 0.82, "L_jianjia": 0.9, "R_jianjia": 0.9, "bone13": 0.75, "R_fujianjia1": 0.72,
          "R_fujianjia2": 0.72, "bone23": 0.72, "bone24": 0.72, "bone26": 0.72, "bone28": 0.72, "bone107": 0.88, "bone11": 0.58} if NON else {}
AN_NON = {"P_dun08", "P_dun05", "P_dun12", "P_dun11"} if NON else set()
TEN = "dat_nung_non" if NON else "dat_nung_1"
MANH = os.path.join(G.BASE, "manh")
MANH_PART = os.path.join(G.BASE, "manh_part")
MANH_MOI = os.path.join(G.BASE, "manh_part2")              # mảnh ĐỔI KIỂU DÁNG (đầu, giáp; người dùng 2026-11-14): khung part nới thêm lề, lưới 4 đỉnh
PX_PART = 1.15                                              # ảnh atlas so với ảnh vùng của họ (0,56 px / đơn vị rig) → 0,64 px / đơn vị; ảnh mảnh của mình = ảnh vùng × 2
# mảnh đổi kiểu dáng: (co quanh trọng tâm hình, dời x, dời y) theo đơn vị rig ở dáng gốc (x sang phải, y lên trên). Hình mới to hơn mảnh
# cũ 1,2–1,5 lần và đầu mới bè ngang nên che mất quầng dung nham + viên lõi: thu lại, dời đầu sang phải cho lõi lộ ra như concept.
CHINH = {"P_tou": (0.86, 48.0, 10.0), "P_jianjiaL2": (0.85, 10.0, 0.0), "P_jianjiaR2": (0.85, 0.0, 0.0),
         "P_jianjiaL1": (0.85, 0.0, 0.0), "P_jianjiaR1": (0.90, 0.0, 0.0)}
CHINH_NON = {"P_tou": (0.72, 20.0, 60.0)}                                              # như CHINH, cho mảnh vẽ riêng của dạng 1
MOI = PART and os.environ.get("DN_CU") != "1" and os.path.isdir(MANH_MOI)      # có mảnh đổi kiểu dáng: xuất ra rig_moi/ (DN_CU=1: bản cũ, rig_part/)
RA = os.path.join(BASE_NON, "rig") if NON else os.path.join(G.BASE, "rig_goc" if GOC else ("rig" if TU_DO else ("rig_moi" if MOI else "rig_part")))
MANH_NON = os.path.join(BASE_NON, "manh_part2")
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
ZERO5 = np.array([0, 0, 0, 1, 1.0])
USE = ["idle_01", "run_01", "skill_01_1", "skill_04_1", "hit_01"]
BO_SLOT = {"shadow", "wangge"} | (set() if GOC else {"P_tou2", "P_tou3"}) | AN_NON      # P_tou2/3: lớp chớp mắt của họ (cùng ảnh đầu), bỏ ở da mình
CAO = 800.0                                   # chiều cao game: đỉnh đầu / giáp vai (không tính mảnh đá sau lưng và kiếm)
DAT_Y = 0.0                                   # mặt đất (y thế giới)
N_KIEM = 5

MANH_DA = {"P_dun04": "bone107", "P_dun05": "bone14", "P_dun06": "bone28", "P_dun07": "bone26", "P_dun08": "bone25", "P_dun09": "bone24",
           "P_dun10": "bone23", "P_dun11": "bone90", "P_dun12": "bone94"}
NGON_XA = ["R_zhongzhi", "R_zhongzhi2", "R_shizhi", "R_shizhi2", "R_damuzhi2", "R_damuzhi3", "R_xiaomuzhi", "R_xiaomuzhi2", "R_wumingzhi",
           "R_wumingzhi2"]
NGON_GAN = ["bone116", "bone117", "bone176", "bone177", "bone179", "bone180", "bone181", "bone182", "bone183", "bone184"]
TAY_MO = ["P_shouR5", "P_shouR4_017", "P_shouR4_12", "P_shouR4_13", "P_shouR4_018", "P_shouR4_010", "P_shouR4_011", "P_shouR4_014",
          "P_shouR4_012", "P_shouR4_013", "P_shouR4_015", "P_shouR4_016"]          # bàn tay xoè gắn trên tay gần (bone115)
NAM_TAY = ["P_shouL4_1", "P_shouL4_2"]


def loai(slot):
    """nhóm của một mảnh (thứ tự bay vào / rụng xuống)."""
    if slot.startswith("P_huoyan"):
        return "loi"
    if slot == "P_tou":
        return "dau"
    if slot == "P_wuqi":
        return "kiem"
    if slot in MANH_DA:
        return "da"
    if slot.startswith("P_shenti"):
        return "duoi"
    if slot.startswith("P_shouR4_"):
        return "ngon"
    if slot in ("P_shouR4", "P_shouL4_1", "P_shouL4_2"):
        return "ban"
    if slot.startswith("P_shou"):
        return "tay"
    if slot[-1] in "245" and slot.startswith("P_jianjia"):
        return "co"
    return "vai"                                # P_jianjia?1, ?3, P_dun01..03


# ---------------------------------------------------------------- thứ tự vẽ của họ: slot đứng yên + slot di động (như quy_dao_rig)
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
    return [s for s in base if s in static], [s for s in base if s not in static]


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
            Am = np.array([[F["l"][i][2] - z[2], F["l"][i][0] - z[0], F["l"][i][1] - z[1],
                            F["l"][i][3] / (z[3] or 1.0), F["l"][i][4] / (z[4] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if b0["name"] == "bone27":
                Am[:, 0] = 0.0                       # lõi của họ quay 4 vòng mỗi vòng idle: góc cộng dồn không khép vòng được; lõi mình chỉ đập
            if b0["name"] in ("bone186", "bone187"):
                continue                             # xương kiếm rời của họ (die_01): không dùng
            if np.abs(Am - ZERO5).max() > 1e-4:
                res[b0["name"]] = Am
        hinh = [[(F["n"][k], float(F["a"][k])) for k in range(len(SL))] for F in fr]
        cho = [{m: neo(F["o"], m) for m in DONG} for F in fr]
        out[clip] = (float(v["dur"]), res, hinh, cho)
    return out


CD = _cd()
BAN = {m: sorted({c[m] for clip in USE for c, h in zip(CD[clip][3], CD[clip][2]) if h[m][0] is not None} | {NEO0[m]}) for m in DONG}


def mau(clip, t, lap=False, chi=None, tru=()):
    """độ lệch (xoay, dời x, y, tỉ lệ x, y) của mọi xương ở giây t của clip họ, so với dáng gốc (khung 0 idle)."""
    dur, R = CD[clip][0], CD[clip][1]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    out = {}
    for b, arr in R.items():
        if (chi is not None and b not in chi) or b in tru:
            continue
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
    return {k: a.get(k, ZERO5) * (1 - w) + b.get(k, ZERO5) * w for k in set(a) | set(b)}


def pha_gan(a, b, w):
    out = {}
    for k in set(a) | set(b):
        x, y = a.get(k, ZERO5), np.array(b.get(k, ZERO5), float)
        y[0] += 360.0 * round((x[0] - y[0]) / 360.0)
        out[k] = x * (1 - w) + y * w
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


def u_(t, a, b):
    return em((t - a) / (b - a))


def ra_(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao_(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return x ** k


def vot(x, s=1.70158):
    x = min(1.0, max(0.0, x)) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


def bump(t, a, b, c, d):
    return em((t - a) / (b - a)) * (1 - em((t - c) / (d - c)))


def tq(t, bang):
    if t <= bang[0][0]:
        return bang[0][1]
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / max(1e-9, b_ - a_)
    return bang[-1][1]


def tat_dan(t, t0, bien, tan, giam):
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def hien_theo_ho(sk, P, clip, t, lap=False):
    """độ đậm + hình của mọi slot theo khung của họ; slot di động bật đúng bản theo chỗ chèn (thứ tự vẽ) của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    hinh, cho = CD[clip][2][i], CD[clip][3][i]
    for k, sl in enumerate(SL):
        if sl in BO_SLOT or sl not in sk.si:
            continue
        n, a = hinh[k]
        if k in NEO0:
            for kk in BAN[k]:
                P.alpha[ten_ban(k, kk)] = a if (n is not None and kk == cho[k]) else 0.0
        else:
            P.alpha[sl] = a if n is not None else 0.0


def gan_goc_tg(a, moc):
    return a - 360.0 * round((a - moc) / 360.0)


# ---------------------------------------------------------------- dựng
def dung():
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("far", "root", 0.9 * CAO + 140.0, 0.45 * CAO)
    for i, b in enumerate(I["bones"]):
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        z = L0[i]
        k_ = TI_NON.get(b["name"], 1.0)
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1], goc=z[2], dai=b["len"], sx=z[3] * k_, sy=z[4] * k_)
    Wi = sk.the_gioi()
    G.Q._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hinh0 = CD["idle_01"][2][0]
    IM = {}

    TAT_ANH = {}
    LE = {}                                              # ảnh vùng → lề (px ảnh vùng) của mảnh đổi kiểu dáng
    TAM = {}
    RIENG_NON = set()                                    # ảnh vùng có mảnh vẽ riêng của dạng 1

    def anh_goc(a):
        r = a["region"]
        if r not in IM:
            if PART:                                     # da của mình đúng khung ảnh vùng (dat_nung_da.py cat): ảnh vùng × 2
                pm = os.path.join(MANH_PART, r + ".png")
                p2 = os.path.join(MANH_MOI, r + ".png")
                if NON and os.path.exists(os.path.join(MANH_NON, r + ".png")):
                    p2 = os.path.join(MANH_NON, r + ".png")
                    RIENG_NON.add(r)
                if os.path.exists(p2) and os.environ.get("DN_CU") != "1":      # DN_CU=1: bản giữ kiểu dáng con gốc
                    pm = p2
                    LE[r] = float(json.load(open(p2[:-4] + ".json"))["le"])
                    al_ = np.asarray(Image.open(p2).convert("RGBA"))[..., 3] > 60
                    ys_, xs_ = np.nonzero(al_)
                    TAM[r] = (float(xs_.mean()) / al_.shape[1], float(ys_.mean()) / al_.shape[0])     # trọng tâm hình (phần của ảnh)
                if not os.path.exists(pm):
                    raise SystemExit(f"thiếu mảnh {pm} (chạy dat_nung_da.py cat)")
                g = Image.open(pm).convert("RGBA")
                co = (max(2, round(g.width * PX_PART / 2)), max(2, round(g.height * PX_PART / 2)))
                IM[r] = anh.loang_mau(g.convert("RGBa").resize(co, Image.LANCZOS).convert("RGBA"))
                if r == "P_tou" and r in LE:             # đầu mới mắt to, miệng dung nham: lúc lõi tắt thì mắt và miệng tắt theo
                    TAT_ANH[r] = r + "_tat"
                    sk.anh(r + "_tat", anh.loang_mau(tat_lava(g).convert("RGBa").resize(co, Image.LANCZOS).convert("RGBA")))
                if r in ("P_huoyan17", "P_huoyan20"):    # hình TẮT (lõi tắt, dung nham nguội) cho clip chết
                    TAT_ANH[r] = r + "_tat"
                    sk.anh(r + "_tat", anh.loang_mau(nguoi(g, (128, 112, 104) if r == "P_huoyan17" else (92, 78, 74))
                                                     .convert("RGBa").resize(co, Image.LANCZOS).convert("RGBA")))
            else:
                IM[r] = anh.loang_mau(G.part_goc(a))
            sk.anh(r, IM[r])
        return IM[r]

    def hang(a, xy):
        """điểm thế giới dáng gốc CỦA HỌ → (xương, toạ độ theo xương, trọng số) và điểm thế giới ở dáng gốc của mình (khung 0 idle)."""
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
        """da gốc: NGUYÊN lưới của họ."""
        r = a["region"]
        im = anh_goc(a)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        if r in LE:                                      # mảnh đổi kiểu dáng: ảnh = khung ảnh vùng nới lề; lưới 4 đỉnh qua phép afin uv → thế giới
            if a.get("w") and len({b_ for v_ in a["w"] for b_, w_ in v_ if w_ > 0}) > 1 and r != "P_wuqi":      # kiếm: bone185 đứng yên so với bone11 trong mọi clip
                raise SystemExit(f"{r}: mảnh nhiều xương, không đổi kiểu dáng bằng lưới 4 đỉnh được")
            T, *_ = np.linalg.lstsq(np.hstack([uv_px, np.ones((len(uv_px), 1))]), xy, rcond=None)
            sai = float(np.abs(np.hstack([uv_px, np.ones((len(uv_px), 1))]) @ T - xy).max())
            if sai > 1.5:
                print(f"  {slot_ten}: lưới gốc không afin (lệch {sai:.1f})")
            le = LE[r]
            uv_px = np.array([[-le, -le], [wr + le, -le], [wr + le, hr + le], [-le, hr + le]], float)
            xy = np.hstack([uv_px, np.ones((4, 1))]) @ T
            ch_ = CHINH_NON if r in RIENG_NON else CHINH
            if r in ch_:
                k_, dx_, dy_ = ch_[r]
                tam = np.array([-le + TAM[r][0] * (wr + 2 * le), -le + TAM[r][1] * (hr + 2 * le), 1.0]) @ T
                xy = tam + k_ * (xy - tam) + np.array([dx_, dy_])
            tris = np.array([[0, 1, 2], [2, 3, 0]])
            uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        else:
            uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        tris = np.asarray(tris, int).reshape(-1, 3)
        sk.atts[slot_ten][a["att"]] = {"type": "mesh", "path": r, "uv": uv, "tris": tris, "hull": len(uv), "V": V0, "verts": rows,
                                       "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, a["att"])] = Luoi(uv * np.array([im.width, im.height], float), tris, len(uv), len(uv), im.width, im.height, ten=slot_ten)

    DA = da_cua_minh(sk, Wi) if TU_DO else None

    def gan_minh(slot_ten, a):
        """da của mình: ảnh mảnh cứng 4 đỉnh đặt theo dat.json (thế giới khung 0 idle của mảnh chính); slot nhân bản của cùng ảnh vùng thì
        chuyển qua phép afin (lưới bản chính → lưới bản sao) ở dáng gốc của họ."""
        d = DA.get(a["region"])
        if d is None:
            return False
        key, C0, bm, am = d["anh"], d["goc4"], d["xuong"], d["att"]
        im = sk.images[key]
        if a is am or a["bone"] == bm:
            rows = [[(bm, *map(float, np.linalg.solve(Wi[bm], np.array([p[0], p[1], 1.0]))[:2]), 1.0)] for p in C0]
        else:
            Pm = np.array(am["xy"], float).reshape(-1, 2)
            Pc = np.array(a["xy"], float).reshape(-1, 2)
            n = min(len(Pm), len(Pc))
            A_ = np.hstack([Pm[:n], np.ones((n, 1))])
            T, *_ = np.linalg.lstsq(A_, Pc[:n], rcond=None)                    # thế giới dáng gốc họ: bản chính → bản sao
            rows = []
            for p in C0:
                ps = WG[bm] @ np.linalg.solve(Wi[bm], np.array([p[0], p[1], 1.0]))
                pc = np.array([ps[0], ps[1], 1.0]) @ T
                bc = a["bone"]
                rows.append([(bc, *map(float, np.linalg.solve(WG[bc], np.array([pc[0], pc[1], 1.0]))[:2]), 1.0)])
        V0 = np.array([(Wi[r[0][0]] @ np.array([r[0][1], r[0][2], 1.0]))[:2] for r in rows])
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        tris = np.array([[0, 1, 2], [2, 3, 0]])
        sk.atts[slot_ten][a["att"]] = {"type": "mesh", "path": key, "uv": uv, "tris": tris, "hull": 4, "V": V0, "verts": rows,
                                       "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, a["att"])] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)
        return True

    by_slot = {}
    for a in AG["atts"]:
        by_slot.setdefault(a["slot"], []).append(a)
    ROI = {}                                             # slot chính → dict(xuong, tam, P (đỉnh quanh tâm), loai)

    def them(slot_goc, ten, hien, chinh):
        ats = by_slot.get(slot_goc)
        if not ats:
            return
        mac = next((a for a in ats if a["cur"]), ats[0])
        sk.slot(ten, "move", mac["att"], an=not hien)
        for a in ats:
            if not TU_DO:
                gan(ten, a)
            elif not gan_minh(ten, a):
                del sk.atts[ten]
                sk.slots.pop()
                sk.si = {q["name"]: i for i, q in enumerate(sk.slots)}
                return
        spec = sk.atts[ten][mac["att"]]
        sk._slot(ten)["bone"] = spec["verts"][0][0][0]
        if chinh and hien:                               # bản RỜI của mảnh: cứng trên xương riêng ở tâm mảnh (appear, die)
            V = np.asarray(spec["V"], float)
            c = (V.min(0) + V.max(0)) / 2
            rb = "r_" + slot_goc[2:]
            sk.xuong(rb, "move", float(c[0]), float(c[1]))
            t2 = slot_goc + "~r"
            sk.slot(t2, rb, mac["att"], an=True)
            sk.atts[t2][mac["att"]] = dict(spec, verts=[[(rb, float(p[0] - c[0]), float(p[1] - c[1]), 1.0)] for p in V])
            sk.luoi[(t2, mac["att"])] = sk.luoi[(ten, mac["att"])]
            ROI[slot_goc] = dict(xuong=rb, slot=t2, tam=c, P=V - c, loai=loai(slot_goc), r=float(np.hypot(*(V - c).T).max()))
            d_ = DA.get(mac["region"]) if DA else None
            tat_ = (d_ or {}).get("tat") or TAT_ANH.get(mac["region"])
            if tat_:                                    # hình TẮT (lõi tắt, dung nham nguội): cùng chỗ, bật lúc chết
                t3 = slot_goc + "~t"
                sk.slot(t3, rb, mac["att"], an=True)
                sk.atts[t3][mac["att"]] = dict(sk.atts[t2][mac["att"]], path=tat_)
                sk.luoi[(t3, mac["att"])] = sk.luoi[(ten, mac["att"])]

    cho_chen = {}
    for m in DONG:
        for kk in BAN[m]:
            hang_ = [list(F["o"]).index(m) for c in USE for F in S[c]["frames"] if neo(F["o"], m) == kk]
            cho_chen.setdefault(kk, []).append((float(np.mean(hang_)) if hang_ else 0.0, m))
    for k in range(len(STAT) + 1):
        for _, m in sorted(cho_chen.get(k, [])):
            if SL[m] not in BO_SLOT:
                them(SL[m], ten_ban(m, k), hien=(hinh0[m][0] is not None and k == NEO0[m]), chinh=(k == NEO0[m]))
        if k < len(STAT):
            s_ = STAT[k]
            if SL[s_] not in BO_SLOT:
                them(SL[s_], SL[s_], hien=hinh0[s_][0] is not None, chinh=True)

    if TU_DO:
        # bản tự chế: viên LÕI nằm TRƯỚC hai vành cổ (concept), không nấp sau như của họ → dời slot lõi (và bản rời, bản tắt) ra sau vành cổ gần
        moc = max(i for i, q in enumerate(sk.slots) if q["name"].split("~")[0].split("@")[0] in ("P_jianjiaL2", "P_jianjiaR2"))
        doi = [q for q in sk.slots if q["name"].split("~")[0] == "P_huoyan17"]
        con = [q for q in sk.slots[:moc + 1] if q not in doi]
        sk.slots = con + doi + [q for q in sk.slots[moc + 1:] if q not in doi]
        sk.si = {q["name"]: i for i, q in enumerate(sk.slots)}

    # ---- KIẾM: tâm, trục (chuôi → mũi) ở khung 0 idle; 5 thanh kiếm bay của chiêu cuối
    kslot = "P_wuqi"
    spec_k = sk.atts[kslot]["P_wuqi"]
    Vk = np.asarray(spec_k["V"], float)
    g_, m_ = Wi["bone11"][:2, 2], Wi["bone185"][:2, 2]
    ax = (m_ - g_) / np.linalg.norm(m_ - g_)
    a0 = math.degrees(math.atan2(ax[1], ax[0]))
    Pk = Vk
    if len(Vk) == 4:                                   # ô ảnh 4 đỉnh (bản tự chế, kiếm vẽ riêng của dạng 1): lấy các điểm có hình
        al = np.asarray(sk.images[spec_k["path"]])[..., 3] > 60
        ys, xs = np.nonzero(al)
        uu, vv = xs[::7] / al.shape[1], ys[::7] / al.shape[0]
        Pk = Vk[0] + uu[:, None] * (Vk[1] - Vk[0]) + vv[:, None] * (Vk[3] - Vk[0])
    du = (Pk - g_) @ ax
    tam_k = g_ + ax * (du.min() + du.max()) / 2                           # tâm thanh kiếm (giữa chuôi và mũi)
    dai_k = float(du.max() - du.min())
    loc_tam = np.linalg.solve(Wi["bone11"], np.array([tam_k[0], tam_k[1], 1.0]))[:2]
    c_, s_ = math.cos(math.radians(-a0)), math.sin(math.radians(-a0))
    Rm = np.array([[c_, -s_], [s_, c_]])
    Vn = (Vk - tam_k) @ Rm.T                                              # kiếm nằm ngang, mũi chĩa +x, tâm ở gốc
    # hình QUẠT kiếm trên đầu (chiêu cuối): tâm quạt ở ngực, chuôi cách tâm R_TRONG, kiếm thu còn KI_TI; chỗ từng thanh = chỗ phóng (fly_k)
    KI_TI, R_TRONG, GOC_MO = 0.72, 420.0, 24.0
    tam_q = np.array([Wi["bone27"][0, 2] + 10.0, Wi["bone27"][1, 2] - 40.0])
    kiem, goc_q = [], []
    for k in range(N_KIEM):
        th = 90.0 - (k - 2) * GOC_MO                                      # k = 0 ngoài cùng bên trái (138°) … k = 4 bên phải (42°)
        r = R_TRONG + 0.5 * dai_k * KI_TI
        c = tam_q + r * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))])
        sk.xuong(f"fly_{k}", "root", float(c[0]), float(c[1]))
        sk.xuong(f"nam_{k}", f"fly_{k}", 0.0, 0.0)
        sk.slot(f"kiem_{k}", f"nam_{k}", "P_wuqi", an=True)
        sk.atts[f"kiem_{k}"]["P_wuqi"] = dict(spec_k, verts=[[(f"nam_{k}", float(p[0]), float(p[1]), 1.0)] for p in Vn], V=Vn + c)
        sk.luoi[(f"kiem_{k}", "P_wuqi")] = sk.luoi[(kslot, "P_wuqi")]
        kiem.append((float(c[0]), float(c[1])))
        goc_q.append(th)
    sk.xuong("mui_kiem", "bone11", float(np.linalg.solve(Wi["bone11"], np.array([m_[0], m_[1], 1.0]))[0]), 0.0)
    sk.xuong("mieng", "move", float(Wi["bone27"][0, 2]), float(Wi["bone27"][1, 2]))      # lõi (chỗ VFX tụ lực)
    for e, m in (("trung", "khung đòn trúng"), ("chem", "một nhát chém"), ("dam", "cú đâm"), ("lao", "bắt đầu lao tới"), ("tu", "tụ lực, lõi bùng"),
                 ("tha", "kiếm rời tay bay lên"), ("phan", "kiếm phân thân"), ("xoay", "dàn kiếm quay về phía địch"), ("ban", "một thanh kiếm phóng đi"),
                 ("cham", "một thanh kiếm tới đích"), ("hien", "kiếm hiện lại trong tay"), ("loi", "lõi hiện ra"), ("ghep", "mảnh to khớp vào"),
                 ("xong", "ráp xong"), ("tat", "lõi tắt"), ("roi", "bắt đầu rụng"), ("cham_dat", "mảnh to chạm đất")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; {len(ROI)} mảnh rời; slot di động: "
          + ", ".join(f"{SL[m]} {BAN[m]}" for m in DONG))
    return sk, dict(cao=CAO, roi=ROI, kiem=dict(a0=a0, loc_tam=loc_tam, dai=dai_k, cho=kiem, goc=goc_q, ti=KI_TI),
                    loi=Wi["bone27"][:2, 2].copy(), far=sk.W0["far"][:2, 2].copy())


def tat_lava(im, mau=(84, 70, 66)):
    """bản TẮT của một mảnh có chi tiết dung nham (mắt vàng, miệng và khe cam): chỉ vùng màu dung nham đổi sang đá nguội, phần còn lại giữ."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    R, G_, B = rgb[..., 0:1], rgb[..., 1:2], rgb[..., 2:3]
    w = np.clip((R - 215.0) / 20.0, 0, 1) * np.clip((G_ - B - 55.0) / 25.0, 0, 1)
    k = 0.9 + 0.5 * np.clip((G_ - 120.0) / 100.0, 0, 1)           # vàng (mắt) nguội thành xám sáng hơn cam (miệng, khe)
    out = rgb * (1 - w) + np.array(mau, np.float32)[None, None, :] * k * w
    return Image.fromarray(np.dstack([np.clip(out, 0, 255), al]).astype(np.uint8), "RGBA")


def nguoi(im, mau):
    """bản TẮT / NGUỘI của một mảnh: mọi vùng màu (không phải nét mực) đổi sang màu đá nguội, giữ đậm nhạt tương đối và vân sáp."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    sang = rgb.mean(2, keepdims=True)
    muc = (rgb.max(2, keepdims=True) < 105)
    co = (al > 40) & ~muc
    med = float(np.median(sang[co])) if co.any() else 160.0
    k = np.clip(0.80 + 0.35 * (sang - med) / 90.0, 0.55, 1.2)
    out = np.where(muc, rgb, np.array(mau, np.float32)[None, None, :] * k)
    return Image.fromarray(np.dstack([np.clip(out, 0, 255), al]).astype(np.uint8), "RGBA")


def da_cua_minh(sk, Wi):
    """da của mình: inbox/dat_nung_1/manh/dat.json {tên ảnh vùng của họ: {"anh": file, "M": afin 2×3 px ảnh → thế giới khung 0 idle}},
    "_px" (px atlas / đơn vị rig), "_tat" {ảnh vùng: file hình TẮT} (lõi, quầng dung nham lúc chết)."""
    p = os.path.join(MANH, "dat.json")
    if not os.path.exists(p):
        raise SystemExit(f"chưa có da của mình ({p}); thử rig bằng da gốc: DN_GOC=1")
    D = json.load(open(p, encoding="utf-8"))
    px = float(D.pop("_px", 0.62))
    tat = D.pop("_tat", {})
    main = {}
    for a in sorted(AG["atts"], key=lambda a: (not a["cur"], a["order"])):
        main.setdefault(a["region"], a)
    out = {}
    for r, d in D.items():
        g = Image.open(os.path.join(MANH, d["anh"] + ".png")).convert("RGBA")
        M = np.array(d["M"], float)
        ti = float(np.sqrt(abs(np.linalg.det(M[:, :2]))))
        co = (max(2, round(g.width * ti * px)), max(2, round(g.height * ti * px)))
        key = d["anh"]
        if key not in sk.images:
            sk.anh(key, anh.loang_mau(g.convert("RGBa").resize(co, Image.LANCZOS).convert("RGBA")))
        C = np.array([[0, 0, 1], [g.width, 0, 1], [g.width, g.height, 1], [0, g.height, 1]], float) @ M.T
        out[r] = dict(anh=key, goc4=C, xuong=("move" if main[r]["bone"] == "root" else main[r]["bone"]), att=main[r])
        if r in tat:
            g2 = Image.open(os.path.join(MANH, tat[r] + ".png")).convert("RGBA")
            sk.anh(tat[r], anh.loang_mau(g2.convert("RGBa").resize(co, Image.LANCZOS).convert("RGBA")))
            out[r]["tat"] = tat[r]
    return out


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    out = []
    cao = info["cao"]
    ROI = info["roi"]
    KI = info["kiem"]
    LOI = info["loi"]
    FAR = info["far"]
    co = sk.si
    rng = np.random.default_rng(3625)
    da_x = [b for b in MANH_DA.values()]
    PHA = {b: float(rng.uniform(0, 6.283)) for b in da_x}
    W0 = sk.the_gioi()
    HUONG_DA = {}                                        # hướng toả ra của từng mảnh đá (từ lõi), trong hệ xương cha
    for s, b in MANH_DA.items():
        if s in ROI:
            d = ROI[s]["tam"] - LOI
            d = d / max(1e-6, np.linalg.norm(d))
            cha = sk.bones[sk.bi[b]]["parent"]
            HUONG_DA[b] = np.linalg.solve(W0[cha][:2, :2], d)

    UON_G, UON_X = (-1.0 if TU_DO else None), None                           # chiều gập khuỷu khi giải tay (None: giữ chiều đang gập). Tay gần: khuỷu chúc XUỐNG
    # (khuỷu vểnh lên thì bắp tay quay 138°, các khối bắp tay văng lên che giáp vai và đầu)
    GOC_TAY_G, GOC_TAY_X = 20.0, 160.0                  # góc thế giới của bàn tay gần / xa khi ngửa lòng bàn tay

    def a_(P, slot, v):
        if slot in co:
            P.alpha[slot] = v

    def ho(P, clip, u, lap=False, d=None):
        dat(P, d if d is not None else mau(clip, u, lap))
        hien_theo_ho(sk, P, clip, u, lap)
        if TU_DO:        # họ đổi nắm tay gần sang bàn tay xoè (mu bàn tay ôm chuôi) trong skill_04; da của mình: bàn tay xoè nhỏ, giữ NẮM TAY
            for s_ in NAM_TAY:
                a_(P, s_, 1.0)
            for s_ in TAY_MO:
                m = SL.index(s_)
                for kk in BAN.get(m, []):
                    a_(P, ten_ban(m, kk), 0.0)

    def nhip_loi(P, t, chu_ky=1.0, bien=0.10):
        """nhịp đập của lõi: hai nhịp 'thình thịch' mỗi chu kỳ; bằng 0 ở t = 0."""
        x = (t % chu_ky) / chu_ky
        v = math.exp(-((x - 0.30) / 0.05) ** 2) + 0.6 * math.exp(-((x - 0.47) / 0.05) ** 2)
        P.scale("bone27", 1 + bien * v)

    def da_xoe(P, k, rung_=0.0, t=0.0):
        """chùm mảnh đá sau lưng xoè ra (k > 0) / khép vào (k < 0): dời dọc hướng toả từ lõi, mảnh xa xoè nhiều hơn; rung_ độ."""
        for b, h in HUONG_DA.items():
            P.move(b, float(h[0] * 70.0 * k), float(h[1] * 70.0 * k))
            if rung_:
                P.rot(b, rung_ * math.sin(2 * math.pi * 12.0 * t + PHA[b]))

    def da_tho(P, t, D, bien=1.0):
        """mảnh đá 'thở': mỗi mảnh nhấp nhô dọc hướng toả + xoay nhẹ, lệch pha; số vòng nguyên trong D, bằng 0 ở t = 0."""
        for b, h in HUONG_DA.items():
            ph = PHA[b]
            v = math.sin(2 * math.pi * 2 * t / D + ph) - math.sin(ph)
            P.move(b, float(h[0] * 14.0 * v * bien), float(h[1] * 14.0 * v * bien))
            P.rot(b, 2.2 * bien * (math.sin(2 * math.pi * t / D * 3 + 1.7 * ph) - math.sin(1.7 * ph)))

    def nam_ngon(P, v, gan=False):
        """ngón tay xa (hoặc bàn tay xoè gắn ở tay gần) co lại v (0..1)."""
        for i, b in enumerate(NGON_GAN if gan else NGON_XA):
            P.rot(b, (-38.0 if i % 2 == 0 else -52.0) * v * (1 if "damuzhi" not in b else 0.5))

    def tay_mo(P, mo):
        """tay gần: nắm tay (mo = False) hay bàn tay xoè (mo = True)."""
        for s in NAM_TAY:
            for nm in [q["name"] for q in sk.slots if q["name"] == s or q["name"].startswith(s + "@")]:
                if mo:
                    P.alpha[nm] = 0.0
        for s in TAY_MO:                                    # bật bản vẽ TRƯỚC cẳng tay (chỗ chèn lớn nhất), tắt các bản khác
            m = SL.index(s)
            for kk in BAN.get(m, [NEO0.get(m, 0)]) if m in NEO0 else [None]:
                nm = s if kk is None else ten_ban(m, kk)
                a_(P, nm, 1.0 if (mo and (kk is None or kk == max(BAN[m]))) else 0.0)

    B115 = sk.bones[sk.bi["bone115"]]

    def ban_tay_gan(P, goc):
        """bàn tay XOÈ của tay gần (xương bone115, con của L_shou): đặt vào cổ tay như họ đặt (lật gương bàn tay xa), các ngón chĩa góc
        thế giới `goc` (gọi sau khi đã giải tay)."""
        W = sk.the_gioi(P)
        k = 1.45 if TU_DO else 1.0                         # da của mình: lòng bàn tay xa nhỏ hơn nắm tay gần nhiều → phóng bàn tay xoè
        P.t["bone115"] = [15.7 - B115["x"], -5.2 - B115["y"], gan_goc_tg(goc - goc_mat(W["L_shou"]), -73.2) - B115["rot"], k, -k]

    def kiem_tay(P, hien):
        for nm in [q["name"] for q in sk.slots if q["name"] == "P_wuqi" or q["name"].startswith("P_wuqi@")]:
            if not hien:
                P.alpha[nm] = 0.0

    def kiem_tg(P):
        """tâm và góc thế giới của thanh kiếm đang cầm ở tư thế P."""
        W = sk.the_gioi(P)
        Wb = W["bone11"]
        c = (Wb @ np.array([KI["loc_tam"][0], KI["loc_tam"][1], 1.0]))[:2]
        return c, goc_mat(Wb) + (KI["a0"] - goc_mat(W0["bone11"]))

    def dat_kiem(P, k, tam, goc, s=1.0, a=1.0, bay=0.0):
        """thanh kiếm bay k: tâm (thế giới), góc mũi kiếm, tỉ lệ, độ đậm; bay 0..1 = quãng đã phóng tới far (xương fly_k: game co quãng)."""
        x0, y0 = KI["cho"][k]
        fx, fy = x0 + bay * (FAR[0] - x0), y0 + bay * (FAR[1] - y0)
        if bay > 0:
            P.move(f"fly_{k}", fx - x0, fy - y0)
        P.move(f"nam_{k}", float(tam[0] - fx), float(tam[1] - fy))
        P.rot(f"nam_{k}", float(goc))
        if s != 1.0:
            P.scale(f"nam_{k}", s, s)
        P.alpha[f"kiem_{k}"] = float(a)

    def bo_roi(P, dat_):
        """bật bộ mảnh RỜI: dat_ = {slot: (dx, dy, góc, tỉ lệ, độ đậm)} so với chỗ ở khung 0 idle; mảnh chính ẩn hết."""
        for q in sk.slots:
            nm = q["name"]
            if not nm.endswith("~r") and not nm.startswith("kiem_"):
                P.alpha[nm] = 0.0
        for s, r in ROI.items():
            dx, dy, g, sc, al = dat_.get(s, (0.0, 0.0, 0.0, 1.0, 1.0))
            P.move(r["xuong"], float(dx), float(dy))
            if g:
                P.rot(r["xuong"], float(g))
            if sc != 1.0:
                P.scale(r["xuong"], float(sc), float(sc))
            P.alpha[r["slot"]] = float(al)

    # ---- IDLE (giống họ, sửa khác chút): idle_01 của họ; cú vung kiếm giữa vòng giảm còn 55 %, thay bằng một NHỊP BÙNG của lõi (lõi phồng,
    # chùm đá sau lưng xoè ra rồi khép, bàn tay xa nắm lại rồi xoè); lõi đập hai nhịp mỗi giây; chùm đá thở lệch pha
    D_ID = CD["idle_01"][0]
    B0, B1, B2, B3 = 1.55, 1.85, 2.10, 2.60

    def idle(t, P):
        d = mau("idle_01", t, True)
        w = bump(t, 1.35, 1.6, 2.1, 2.45)
        nen = mau("idle_01", 1.2, True)
        d = pha(d, pha(d, nen, 0.45), w)
        dat(P, d)
        hien_theo_ho(sk, P, "idle_01", 0.0)
        nhip_loi(P, t, 1.0)
        g = bump(t, B0, B1, B2, B3)
        P.scale("bone27", 1 + 0.22 * g)
        da_tho(P, t, D_ID)
        da_xoe(P, 0.55 * g - 0.18 * bump(t, B0 - 0.3, B0, B0, B0 + 0.12))
        nam_ngon(P, bump(t, B0 - 0.35, B0, B1, B2))
    out.append(Clip("idle", D_ID, idle, loop=True, ev=[(B0, "tu", "")]))

    D_W = CD["run_01"][0]

    def walk(t, P):
        ho(P, "run_01", t, True)
        nhip_loi(P, t, D_W / 2 if D_W < 1.2 else 1.0, 0.08)
        da_xoe(P, -0.12 + 0.10 * math.sin(4 * math.pi * t / D_W) - 0.10 * math.sin(0))
    out.append(Clip("walk", D_W, walk, loop=True))

    def hit(t, P):
        ho(P, "hit_01", t)
        da_xoe(P, 0.5 * bump(t, 0.0, 0.07, 0.12, 0.4), rung_=2.0 * bump(t, 0.0, 0.05, 0.1, 0.35), t=t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ---- ATTACK (giống skill_01_1, sửa chút): thu người kéo lùi (lâu hơn, chùm đá khép) → LAO vai tới (cú lao của họ là MỘT khung nhảy bậc:
    # giãn ra 0,09 s) → tới nơi BỔ thêm một nhát kiếm chéo xuống trước mặt (họ chỉ húc) → khựng, chùm đá xoè, lõi bùng → lùi về
    U_L0, U_L1 = 10 / 30, 11 / 30
    TA1, TA2, TA_CH, TA3, D_AT = 0.42, 0.51, 0.60, 0.92, 1.30
    X_AT = 0.42 * cao

    def attack(t, P):
        u = tq(t, [(0, 0.0), (TA1, U_L0), (TA2, U_L1), (TA3, 0.70), (D_AT, CD["skill_01_1"][0])])
        ho(P, "skill_01_1", u)
        thu = bump(t, 0.05, 0.30, TA1, TA2)
        ch = u_(t, TA2 - 0.02, TA_CH) * (1 - u_(t, TA3 - 0.04, D_AT - 0.1))
        P.rot("L_jianbang", 16.0 * thu - 30.0 * ch)                              # giơ kiếm lên lúc lấy đà, bổ xuống trước mặt
        P.rot("L_dabi", 10.0 * thu - 26.0 * ch)
        P.rot("L_shou", -24.0 * ch)
        nen = math.exp(-max(0.0, t - TA_CH) / 0.09) if t >= TA_CH else 0.0
        x = X_AT * u_(t, TA1 - 0.02, TA_CH) * (1 - u_(t, TA3, D_AT - 0.06))
        P.move("move", x - 26.0 * thu + tat_dan(t, TA_CH, 12.0, 14.0, 0.11), tat_dan(t, TA_CH, -9.0, 12.0, 0.10))
        P.scale("move", 1.0 + 0.05 * nen, 1.0 - 0.07 * nen)
        da_xoe(P, -0.35 * thu + 0.9 * nen + 0.25 * bump(t, TA_CH, TA_CH + 0.1, TA3, D_AT), rung_=2.0 * thu, t=t)
        P.scale("bone27", 1 + 0.12 * thu + 0.35 * nen)
    out.append(Clip("attack", D_AT, attack, ev=[(TA1, "lao", ""), (TA_CH, "chem", ""), (TA_CH, "trung", "")], trung=TA_CH))

    # ---- CAST = chiêu mana (giống skill_04_1): thu người → LAO TỚI ĐÂM kiếm → hất lên → chém ngược về → vung kiếm ra sau lấy đà → BỔ kết.
    # Ba cú của họ là khoá bậc một khung (11, 26, 50–51): mỗi cú giãn ra 0,07–0,09 s cho thấy đường kiếm
    TC = [(0.0, 0.0), (0.34, 10 / 30), (0.42, 11 / 30), (0.56, 16 / 30), (0.92, 25 / 30), (1.00, 26 / 30), (1.22, 33 / 30), (1.62, 49 / 30),
          (1.72, 51 / 30), (2.02, 56 / 30), (2.70, CD["skill_04_1"][0])]
    C_DAM, C_CH2, C_KET, D_CA = 0.42, 1.00, 1.72, 2.70
    X_CA = 0.50 * cao

    def cast(t, P):
        u = tq(t, TC)
        ho(P, "skill_04_1", u)
        x = X_CA * u_(t, 0.20, C_DAM) * (1 - u_(t, 2.10, D_CA - 0.08))
        n1 = math.exp(-max(0.0, t - C_DAM) / 0.07) if t >= C_DAM else 0.0
        n3 = math.exp(-max(0.0, t - C_KET) / 0.09) if t >= C_KET else 0.0
        P.move("move", x + tat_dan(t, C_DAM, 8.0, 15.0, 0.09) + tat_dan(t, C_KET, 14.0, 13.0, 0.13), tat_dan(t, C_KET, -11.0, 11.0, 0.11))
        P.scale("move", 1.0 + 0.04 * n1 + 0.07 * n3, 1.0 - 0.05 * n1 - 0.09 * n3)
        gong = bump(t, 1.22, 1.36, 1.56, 1.64)
        da_xoe(P, 0.5 * n1 + 1.0 * n3 - 0.3 * gong + 0.3 * bump(t, 0.0, 0.15, 0.25, 0.34) * -1, rung_=2.4 * gong, t=t)
        P.scale("bone27", 1 + 0.2 * gong + 0.4 * n3 + 0.2 * n1)
    out.append(Clip("cast", D_CA, cast, ev=[(0.20, "lao", ""), (C_DAM, "dam", ""), (0.74, "chem", "len"), (C_CH2, "chem", "nguoc"), (1.30, "tu", ""),
                                            (C_KET, "chem", "ket"), (C_KET, "trung", "")], trung=C_KET))

    # ---- SKILL = chiêu cuối (tự làm): dang hai tay, ngửa lòng bàn tay; kiếm rời tay bay lên lơ lửng ở giữa, mũi hướng lên; kiếm PHÂN THÂN
    # sang hai bên thành hình quạt (5 thanh); cả dàn kiếm quay mũi về phía địch; lần lượt phóng tới; kiếm hiện lại trong tay
    S_THA, S_GIUA, S_P1, S_P2, S_XOAY0, S_XOAY1, S_BAN, S_KC, S_BAY, D_SK = 0.14, 0.58, 0.78, 0.94, 1.50, 1.86, 2.02, 0.06, 0.17, 3.20
    THU_TU_BAN = [4, 3, 2, 1, 0]                                   # thanh gần địch nhất phóng trước
    S_TOI = [S_BAN + THU_TU_BAN.index(k) * S_KC + S_BAY for k in range(N_KIEM)]
    S_TRUNG = max(S_TOI) + 0.012
    S_HIEN0, S_HIEN1 = 2.62, 2.96
    tay_g0, tay_x0 = W0["L_shou"][:2, 2].copy(), W0["R_shou"][:2, 2].copy()
    TAY_G = np.array([LOI[0] + 740.0, 600.0]) if TU_DO else np.array([LOI[0] + 730.0, 430.0])                      # bàn tay gần dang sang phải (người xem), lòng bàn tay ngửa
    TAY_X = np.array([LOI[0] - 500.0, 780.0]) if TU_DO else np.array([LOI[0] - 480.0, 440.0])     # trên hai phiến nhọn, ngoài giáp vai xa (thấp hơn thì nấp sau phiến)                      # bàn tay xa dang sang trái
    QUAT = [np.array(c, float) for c in KI["cho"]]                 # chỗ từng thanh trong hình quạt (tâm kiếm) = chỗ phóng (xương fly_k)
    GOC_Q = KI["goc"]                                              # góc mũi kiếm trong hình quạt (thanh giữa 90°)
    KI_S = KI["ti"]

    def skill(t, P):
        ho(P, "idle_01", 0.0)
        dang = u_(t, S_THA - 0.04, S_GIUA) * (1 - u_(t, S_HIEN0 - 0.12, S_HIEN1))
        nga = bump(t, S_XOAY0, S_XOAY1, S_BAN, S_BAN + 0.10)          # ngả ra sau lấy đà
        day = bump(t, S_BAN - 0.02, S_BAN + 0.07, S_TRUNG + 0.08, S_HIEN0)   # đẩy hai tay về trước
        nho = dang * (1 - nga) * math.sin(2 * math.pi * (t - S_GIUA) / 1.0) if t > S_GIUA else 0.0
        P.move("zhixin", -34.0 * nga + 46.0 * day, 22.0 * dang + 9.0 * nho - 12.0 * nga)
        P.rot("zhixin", 5.0 * nga - 7.0 * day)
        P.rot("tou", -8.0 * dang * (1 - day) + 6.0 * day)
        # hai tay: giải hai khúc cho bàn tay tới chỗ dang; lúc phóng thì đẩy về trước
        tg = tay_g0 + (TAY_G - tay_g0) * dang + (np.array([-60.0, 40.0]) * nga + np.array([120.0, 60.0]) * day) * dang
        tx = tay_x0 + (TAY_X - tay_x0) * dang + (np.array([-40.0, 50.0]) * nga + np.array([330.0, 40.0]) * day) * dang
        if dang > 1e-3:
            hoat.ik_hai_doan(sk, P, "L_dabi", "L_xiaobi", tg, ngon=(247.8, 1.0), uon=UON_G)
            hoat.ik_hai_doan(sk, P, "R_dabi", "R_xiaobi", tx, ngon=(155.9, 0.0), uon=UON_X)
            # lòng bàn tay NGỬA: bàn tay nằm ngang, ngón chĩa ra ngoài hơi vểnh lên
            W = sk.the_gioi(P)
            hien_tai = goc_mat(W["R_shou"])
            P.rot("R_shou", dang * (gan_goc_tg(GOC_TAY_X - 110.0 * day, hien_tai) - hien_tai))
        mo = S_THA <= t < S_HIEN0 + 0.10
        tay_mo(P, mo)
        if mo:
            ban_tay_gan(P, GOC_TAY_G + 50.0 * day - 30.0 * nga)
        nam_ngon(P, 0.25 * nga - 0.2 * day)
        nam_ngon(P, 0.25 * nga - 0.2 * day, gan=True)
        # lõi + chùm đá
        tu = bump(t, S_GIUA - 0.05, S_P1, S_XOAY1, S_BAN)
        no = math.exp(-max(0.0, t - S_BAN) / 0.16) if t >= S_BAN else 0.0
        P.scale("bone27", 1 + 0.30 * tu * (0.6 + 0.4 * math.sin(2 * math.pi * 5 * t)) + 0.5 * no)
        da_xoe(P, 0.8 * tu + 1.2 * no - 0.3 * nga, rung_=2.2 * tu, t=t)
        P.move("move", 2.0 * math.sin(2 * math.pi * 13 * t) * nga + tat_dan(t, S_BAN, -10.0, 12.0, 0.12), 0.0)
        # ---- kiếm
        if t < S_THA:
            return
        ck, gk = kiem_tg(P)
        if t >= S_HIEN0:                                           # kiếm hiện lại trong tay: lớn dần từ chuôi (xương bone11), đậm dần
            w = u_(t, S_HIEN0, S_HIEN1)
            P.scale("bone11", 0.3 + 0.7 * vot(w, 1.4))
            for nm in [q["name"] for q in sk.slots if q["name"] == "P_wuqi" or q["name"].startswith("P_wuqi@")]:
                P.alpha[nm] = P.alpha.get(nm, 0.0) * min(1.0, w * 2.5)
        else:
            kiem_tay(P, False)
        for k in range(N_KIEM):
            j = k - 2                                              # −2 … 2 (k = 0 ngoài cùng bên trái, k = 4 gần địch nhất)
            cho = QUAT[k]
            tb = S_BAN + THU_TU_BAN.index(k) * S_KC
            if t >= tb + S_BAY - 1e-6:                             # đã tới đích: tắt hẳn, xương bay ở lại đích rồi về chỗ cũ lúc đã ẩn
                o = 1.0 - u_(t, tb + S_BAY + 0.42, tb + S_BAY + 0.50)
                dat_kiem(P, k, FAR * o + cho * (1 - o), GOC_Q[k], s=KI_S, a=0.0, bay=o)
                continue
            if j == 0:
                al, w_ra = 1.0, 1.0
            else:
                ts = S_P1 if abs(j) == 1 else S_P2
                if t < ts:
                    dat_kiem(P, k, cho, GOC_Q[k], s=KI_S, a=0.0)
                    continue
                w_ra = vot((t - ts) / 0.30, 1.2)
                al = min(1.0, (t - ts) / 0.10)
            tam = QUAT[2] + (cho - QUAT[2]) * w_ra                 # thanh phân thân trượt ra từ thanh giữa, xoay dần ra góc quạt
            goc = 90.0 + (GOC_Q[k] - 90.0) * w_ra
            sc = KI_S
            if j == 0 and t < S_GIUA:                              # thanh thật: từ bàn tay bay lên giữa, xoay cho mũi lên, nhỏ dần (bay ra xa)
                w = em((t - S_THA) / (S_GIUA - S_THA))
                tam = ck + (cho - ck) * w + np.array([-70.0 * math.sin(math.pi * w), 0.0])
                goc = gk + (gan_goc_tg(90.0, gk) - gk) * ra_(w, 2.0)
                sc = 1.0 + (KI_S - 1.0) * w
            xoay = u_(t, S_XOAY0, S_XOAY1)
            if t > S_GIUA:                                         # lơ lửng nhấp nhô lệch pha
                tam = tam + np.array([0.0, 14.0 * math.sin(2 * math.pi * (t - S_GIUA) / 0.9 - 0.8 * abs(j))]) * (1 - xoay)
            if j == 0:
                sc *= 1.0 + 0.12 * math.exp(-((t - (S_P1 - 0.05)) / 0.05) ** 2) + 0.10 * math.exp(-((t - (S_P2 - 0.05)) / 0.05) ** 2)
            # dàn kiếm quay mũi về phía địch (xoay tại chỗ, thuận kim, thanh gần địch xoay trước một chút)
            if t > S_XOAY0:
                huong = math.degrees(math.atan2(FAR[1] - cho[1], FAR[0] - cho[0]))
                wq = (t - S_XOAY0 - 0.03 * (4 - k)) / (S_XOAY1 - S_XOAY0 - 0.12)
                goc = goc + (huong - goc) * vot(wq, 1.1) if wq < 1 else huong
            # lấy đà: lùi dọc trục kiếm, rồi phóng
            lui = 80.0 * bump(t, S_XOAY1 - 0.04, tb - 0.04, tb, tb + 0.02)
            if lui:
                tam = tam - lui * np.array([math.cos(math.radians(goc)), math.sin(math.radians(goc))])
            bay = 0.0
            if t >= tb:
                q = (t - tb) / S_BAY
                bay = q ** 1.6
                tam = cho + bay * (FAR - cho)
                sc = KI_S * (1.0 + 0.25 * q)
            dat_kiem(P, k, tam, goc, s=sc, a=al, bay=bay)
    ev_sk = ([(S_THA, "tha", ""), (S_GIUA, "tu", ""), (S_P1, "phan", "1"), (S_P2, "phan", "2"), (S_XOAY0, "xoay", "")]
             + [(S_BAN + i * S_KC, "ban", str(k)) for i, k in enumerate(THU_TU_BAN)]
             + [(S_TOI[k], "cham", str(k)) for k in THU_TU_BAN] + [(S_TRUNG, "trung", ""), (S_HIEN0, "hien", "")])
    out.append(Clip("skill", D_SK, skill, ev=ev_sk, trung=S_TRUNG))

    # ---- bộ mảnh rời: thứ tự theo nhóm
    ds = list(ROI.items())

    def goc_cuc(s):
        v = ROI[s]["tam"] - LOI
        return math.atan2(v[1], v[0])

    # ---- APPEAR (tự làm): LÕI hiện ra trước (quầng dung nham + viên lõi lớn dần, đập); rồi từng nhóm mảnh BAY VÀO quanh lõi: vành cổ, mảnh
    # dưới, đầu, giáp vai, tay, bàn tay, ngón, chùm đá (lần lượt theo vòng), cuối cùng thanh kiếm xoay tít bay vào tay; ráp xong gồng một nhịp
    NHOM_P = dict(loi=(0.0, 0.0), co=(0.34, 0.10), duoi=(0.44, 0.10), dau=(0.56, 0.0), vai=(0.66, 0.16), tay=(0.86, 0.16), ban=(1.04, 0.08),
                  ngon=(1.10, 0.12), da=(1.14, 0.30), kiem=(1.46, 0.0))
    P_XONG, D_AP = 1.86, 2.50
    BAY_P = {}
    for nh, (t0, trai) in NHOM_P.items():
        ss = sorted([s for s, r in ds if r["loai"] == nh], key=goc_cuc)
        for i, s in enumerate(ss):
            r = ROI[s]
            v = r["tam"] - LOI
            d = np.linalg.norm(v)
            h = v / d if d > 30 else np.array([math.cos(1.7 * i + 1.0), math.sin(1.7 * i + 1.0)])
            xa = 620.0 + 0.5 * d + float(rng.uniform(-60, 60))
            td = 0.24 if nh in ("ngon", "ban") else (0.34 if nh == "kiem" else 0.28)
            g0 = float(rng.choice([-1, 1]) * rng.uniform(120, 260)) * (2.2 if nh == "kiem" else 1.0)
            if nh == "kiem":
                h = np.array([-0.55, 0.83])
                xa = 900.0
            BAY_P[s] = (t0 + trai * i / max(1, len(ss) - 1), td, h * xa, g0)

    def appear(t, P):
        ho(P, "idle_01", 0.0)
        dat_ = {}
        doi = sum(tat_dan(t, BAY_P[s][0] + BAY_P[s][1] * 0.85, 7.0, 7.0, 0.08) for s, r in ds if r["loai"] in ("dau", "vai", "kiem"))
        for s, r in ds:
            ts, td, (ox, oy), g0 = BAY_P[s]
            if r["loai"] == "loi":
                w = u_(t, 0.0, 0.30)
                dap = 0.10 * math.sin(2 * math.pi * 3.2 * t) * math.exp(-t / 0.5) if t > 0.25 else 0.0
                if s == "P_huoyan17":
                    dat_[s] = (0.0, 150.0 * (1 - w), 0.0, 0.25 + 0.75 * vot(u_(t, 0.0, 0.26), 2.2) + dap, min(1.0, t / 0.06))
                else:
                    w2 = u_(t, 0.10, 0.42)
                    dat_[s] = (0.0, 0.0, -120.0 * (1 - w2), 0.2 + 0.8 * vot(w2, 1.3) + 0.5 * dap, min(1.0, max(0.0, (t - 0.10) / 0.10)))
                continue
            if t < ts:
                dat_[s] = (ox, oy, g0, 0.6, 0.0)
                continue
            w = (t - ts) / td
            f = vot(w, 1.5)
            nay_ = tat_dan(t, ts + td * 0.85, 0.07, 9.0, 0.06) if w > 0.85 else 0.0
            dat_[s] = (ox * (1 - f), oy * (1 - f) - (doi if w >= 1.0 else 0.0), g0 * (1 - em(min(1.0, w * 1.06))),
                       (0.7 + 0.3 * min(1.0, w * 1.6)) * (1 + nay_), min(1.0, (t - ts) / 0.08))
        if t < P_XONG:
            bo_roi(P, dat_)
            for k in range(N_KIEM):
                P.alpha[f"kiem_{k}"] = 0.0
            return
        g = tq(t, [(P_XONG, 0.0), (P_XONG + 0.14, 1.0), (P_XONG + 0.30, 1.0), (D_AP - 0.05, 0.0)])
        g = em(g) if t > P_XONG + 0.3 else vot(g, 1.6)
        da_xoe(P, 1.0 * g, rung_=1.6 * g, t=t)
        P.scale("bone27", 1 + 0.45 * g)
        P.move("zhixin", 0.0, 22.0 * g)
        P.rot("L_jianbang", 10.0 * g)
        P.rot("R_dabi", -12.0 * g)
        P.rot("tou", -6.0 * g)
    out.append(Clip("appear", D_AP, appear, ev=[(0.0, "loi", ""), (NHOM_P["dau"][0] + 0.28, "ghep", "dau"), (NHOM_P["kiem"][0] + 0.34, "ghep", "kiem"),
                                                (P_XONG, "xong", "")]))

    # ---- DIE (tự làm): giật ngửa; lõi chập chờn rồi TẮT NGỎM (0,36 s), quầng dung nham nguội theo; các mảnh mất lực xệ xuống rồi RỤNG RỜI từng
    # bộ phận (ngón, chùm đá, bàn tay, tay, giáp vai, vành cổ, đầu, lõi lăn ra), chất thành đống; thanh kiếm rơi cắm xuống đất
    X_TAT, X_G, TAN = 0.36, 5200.0, 0.5
    NHOM_X = dict(ngon=(0.44, 0.10), da=(0.46, 0.22), ban=(0.56, 0.06), kiem=(0.60, 0.0), tay=(0.64, 0.14), duoi=(0.70, 0.06), vai=(0.78, 0.14),
                  co=(0.90, 0.06), dau=(0.98, 0.0), loi=(1.02, 0.04))
    D_DIE = 1.95
    ROI_X = {}
    for nh, (t0, trai) in NHOM_X.items():
        ss = sorted([s for s, r in ds if r["loai"] == nh], key=lambda s: -ROI[s]["tam"][1])
        for i, s in enumerate(ss):
            r = ROI[s]
            gf = float(rng.choice([-1, 1]) * rng.uniform(50, 130))
            dx = -0.22 * (r["tam"][0] - LOI[0]) + float(rng.uniform(-40, 40))
            nay = dict(ngon=0.7, da=0.35, ban=0.3, tay=0.15, duoi=0.3, vai=0.10, co=0.2, dau=0.12, loi=0.5, kiem=0.0)[nh]
            ke = dict(vai=24.0, dau=70.0, co=40.0, loi=20.0).get(nh, 0.0) * float(rng.uniform(0.6, 1.2))
            if s == "P_huoyan17":
                dx, gf, ke = 260.0, -540.0, 0.0                    # viên lõi tắt lăn ra phía trước
            if s == "P_huoyan20":
                gf, ke = 20.0, 0.0
            if nh == "kiem":
                gf = gan_goc_tg(-102.0, KI["a0"]) - KI["a0"]        # mũi cắm xuống đất, hơi nghiêng
                dx = -180.0 - (r["tam"][0] - LOI[0]) * 0.0
            ROI_X[s] = (t0 + trai * i / max(1, len(ss) - 1), dx, gf, ke, nay)

    def _nam(s, gf):
        """tâm mảnh cách đất bao nhiêu khi nằm ở góc gf."""
        r = ROI[s]
        a = math.radians(gf)
        y = r["P"][:, 0] * math.sin(a) + r["P"][:, 1] * math.cos(a)
        return -float(y.min())

    def _roi(s, t):
        ts, dxf, gf, ke, nay = ROI_X[s]
        r = ROI[s]
        y0 = r["tam"][1]
        nang = 1.0 if r["loai"] in ("vai", "dau", "tay", "kiem") else 0.5
        if r["loai"] == "kiem":
            yf = DAT_Y + _nam(s, gf) - 70.0                        # mũi kiếm cắm sâu 70
        else:
            yf = DAT_Y + _nam(s, gf) * (0.55 if r["loai"] in ("vai", "dau", "co", "loi") and s != "P_huoyan17" else 1.0) + ke
        xe0 = 10.0 + 18.0 * nang
        xe = -xe0 * em((t - 0.12) / (ts - 0.12)) if t > 0.12 else 0.0
        lac = 1.6 * math.sin(2 * math.pi * 15 * t + (hash(s) % 7)) * (1.0 if 0.14 < t < ts else 0.0)
        if t <= ts:
            return lac, xe, 0.0
        h = max(1.0, (y0 - xe0) - yf)
        tr = math.sqrt(2.0 * h / X_G)
        x = t - ts
        if x < tr:
            f = x / tr
            return dxf * f, -xe0 - 0.5 * X_G * x * x, gf * em(f)
        x2 = x - tr
        b = h * 0.14 * nay * abs(math.sin(math.pi * x2 / 0.17)) * math.exp(-x2 / 0.11)
        lan = (dxf * 0.15 * nay) * (1 - math.exp(-x2 / 0.12))
        rg = tat_dan(t, ts + tr, 6.0 * (0.4 + nay), 5.0, 0.10) if r["loai"] != "kiem" else tat_dan(t, ts + tr, 7.0, 9.0, 0.16)
        return dxf + lan, (yf - y0) + b, gf + rg

    def die(t, P):
        ho(P, "idle_01", 0.0)
        giat = tat_dan(t, 0.0, 1.0, 4.0, 0.09) if t > 0 else 0.0
        giat = math.exp(-t / 0.09) * math.cos(2 * math.pi * 4.0 * t) if t < 0.5 else 0.0
        sang = tq(t, [(0, 1.0), (0.08, 0.25), (0.13, 0.9), (0.19, 0.12), (0.26, 0.55), (X_TAT, 0.0)])
        dat_ = {}
        for s, r in ds:
            dx, dy, g = _roi(s, t)
            c = r["tam"]
            dx += -24.0 * giat * (0.4 + c[1] / 700.0)
            g += 4.0 * giat * (1.0 if c[0] < LOI[0] else -0.6)
            sc, al = 1.0, 1.0
            if s == "P_huoyan17":
                sc = (0.72 + 0.28 * sang) * (1.0 - 0.12 * math.exp(-((t - X_TAT) / 0.05) ** 2))
                al = 0.35 + 0.65 * sang if GOC else 1.0
            if s == "P_huoyan20":
                al = (0.30 + 0.70 * sang) if GOC else 1.0
                sc = 0.9 + 0.1 * sang
            dat_[s] = (dx, dy, g, sc, al)
        bo_roi(P, dat_)
        for k in range(N_KIEM):
            P.alpha[f"kiem_{k}"] = 0.0
        if not GOC:                                                # da của mình: lõi và quầng dung nham đổi sang hình TẮT (nguội)
            for s in [s_ for s_ in ROI if (s_ + "~t") in co]:
                if True:
                    tat = sang < 0.5
                    P.alpha[s + "~t"] = P.alpha[ROI[s]["slot"]] if tat else 0.0
                    if tat:
                        P.alpha[ROI[s]["slot"]] = 0.0
        a = float(np.clip(1.0 - (t - (D_DIE - TAN)) / (TAN - 0.08), 0.0, 1.0))
        if a < 1.0:
            for sl in list(P.alpha):
                P.alpha[sl] = a * P.alpha[sl]
    out.append(Clip("die", D_DIE, die, ev=[(X_TAT, "tat", ""), (0.46, "roi", ""), (1.02, "cham_dat", ""), (1.20, "cham_dat", "dau")]))
    for c in out:
        c.mem = list(c.mem) + [GoVong()]
    return out


class GoVong:
    """hậu kỳ: bước xoay > 180° giữa hai khung (góc đã nướng của họ cộng dồn vòng) thì dời phần sau về cùng vòng."""

    def chay(self, sk, frames, ts, loop, fps):
        lech = {}
        for p, q in zip(frames, frames[1:]):
            for b in set(q.t) | set(lech):
                v = q._g(b)
                v[2] += lech.get(b, 0.0)
                d = v[2] - p.t.get(b, [0, 0, 0, 1, 1])[2]
                if abs(d) > 180.0:
                    k = -360.0 * round(d / 360.0)
                    v[2] += k
                    lech[b] = lech.get(b, 0.0) + k


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
    if a and a[0] == "bo_cuc":                       # hình bố cục dáng đứng trên nền trắng 1536 × 1024 (ảnh mẫu cho lượt concept dạng 1)
        fr = hoat.nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.02)
        sc = min(1536 * 0.72 / (Bx[2] - Bx[0]), 1024 * 0.86 / (Bx[3] - Bx[1]))
        im = ve.ve(fr[0], Bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
        o = Image.new("RGB", (1536, 1024), (255, 255, 255))
        o.paste(im, ((1536 - im.width) // 2, (1024 - im.height) // 2))
        ra = os.path.join(BASE_NON if NON else G.BASE, "mau")
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, "bo_cuc_non.png" if NON else "bo_cuc_dang_2.png")
        o.save(pth)
        print(pth)
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.25
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), int(a[4]) if len(a) > 4 else 6)
        hang_ = (len(ims) + cot - 1) // cot
        o = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            o.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        o.save(pth)
        print(pth, o.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN, "Viêm Dũng Nhi, dạng 1 (dat_nung_non)" if NON else "Chiến binh đất nung (dat_nung_1)" + (" · DA GỐC (thử rig)" if GOC else (" · bản tự chế (đã bỏ)" if TU_DO else (" · mặt + giáp mới" if MOI else " · da theo khung part"))), dang=1, so_dang=2 if NON else 1,
                  dung_yen=("skill",), lao=("attack", "cast"), far=("skill",), far_aim=("skill",), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  impact={"attack": (0.08, 0.45, 0.12), "cast": (0.14, 0.7, 0.16), "skill": (0.20, 1.0, 0.18, "#ffb04066")})


if __name__ == "__main__":
    main(sys.argv[1:])
