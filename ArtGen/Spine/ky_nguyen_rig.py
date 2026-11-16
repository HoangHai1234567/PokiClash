# -*- coding: utf-8 -*-
"""Kỵ sĩ cổ đại bị nguyền (ky_nguyen, tướng 8 đảo Kim): RESKIN trên rig con gốc monster_3642 (hiệp sĩ giáp rỗng lơ lửng, kiếm).

- Xương: đủ mọi xương của họ + `move`, `mieng` (mũi kiếm: chỗ gọi hồn), `luoi_hon` (gốc lưỡi kiếm hồn ở chỗ gãy, trục x dọc lưỡi).
  Dáng gốc = khung 0 idle_01 (biến đổi riêng `l` lấy mẫu bằng runtime Spine thật).
- Hình: mỗi hình của họ một hình của mình, NGUYÊN lưới của họ. Mảnh cứng (manh/moi.json: mũ, kiếm, giáo / mũi tên thay gai, mảnh khiên thay
  đá, mắt) là ô 4 đỉnh bám một xương. Mắt `P_mat` là slot riêng ngay trên mũ (appear: mắt bật sáng; die: mắt tắt).
- Thứ tự vẽ của họ đổi gần như mọi khung: slot "di động" nhân bản theo CHỖ CHÈN (skill pokiclash-spine-rig mục 28, như quy_dao_rig).
- Clip: idle / walk / hit = của họ; die = die_01 (mắt tắt, giáp đổ sụp) + mờ; appear = die_01 CHẠY NGƯỢC (đống giáp dưới đất → mắt bật sáng →
  lơ lửng ráp lại); attack = skill_01 (vung kiếm qua đầu, bổ) + lao tới; cast = skill_03_2 (giơ kiếm thẳng lên trời, giữ: gọi hồn đồng đội);
  skill = đầu skill_03_1 (dựng kiếm trước mặt, tay kia vuốt lên, giữ lâu: kiếm hút hồn) → lưỡi hồn mọc dài từ chỗ gãy → giơ kiếm qua đầu
  (skill_03_2) → BỔ (khoảnh khắc bổ của skill_01), khựng, rung → thu.

    ky_nguyen_rig.py                         dựng, xuất inbox/ky_nguyen_1/rig/
    ky_nguyen_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    ky_nguyen_rig.py kiem                    bước xoay lớn nhất giữa hai khung của từng clip
    KN_GOC=1 ky_nguyen_rig.py ...            dựng bằng DA GỐC ra rig_goc/: chỉ để soi clip trong máy, không đưa vào game
    KN_DANG=non ky_nguyen_rig.py ...         DẠNG 1 (kỵ sĩ non): cùng xương / lưới / clip, đổi tỉ lệ xương (TI_LE), mảnh inbox/ky_nguyen_non/manh
                                             (chưa có thì mượn da dạng 2) → inbox/ky_nguyen_non/rig/ (ky_nguyen_non.atomik)
    ky_nguyen_rig.py bo_cuc <png> [tỉ lệ]    khung 0 idle nền trắng (ảnh mẫu tỉ lệ cho concept dạng khác)
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
from quai.khung import Sk, Pose  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.luoi import Luoi  # noqa: E402
import ky_nguyen as G  # noqa: E402

GOC = os.environ.get("KN_GOC") == "1"
# DẠNG 1 (KN_DANG=non; người dùng 2026-11-16 "làm dạng 1 của tướng này"): đổi tỉ lệ ở xương gốc từng bộ phận (xương con thừa hưởng): đầu to,
# tay ngắn, bàn tay to lại chút, giáp vai / kiếm / áo choàng nhỏ, ngọn lửa trên mũ nhỏ (lửa là con của xương đầu: thu lại sau khi đầu phóng)
NON = os.environ.get("KN_DANG") == "non" and not GOC
BASE = os.path.join(os.path.dirname(G.BASE), "ky_nguyen_non") if NON else G.BASE
TEN = "ky_nguyen_non" if NON else "ky_nguyen"
RA = os.environ.get("KN_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("KN_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
if NON and not os.path.isdir(MANH):
    MANH = os.path.join(G.BASE, "manh")                  # chưa có da dạng 1: dựng bố cục bằng da dạng 2
DA_NON = NON and os.path.normpath(MANH) == os.path.normpath(os.path.join(BASE, "manh"))


def _f(k, v):
    return float(os.environ.get(k) or v)


TI_LE = {} if not NON else {
    "bone5": _f("KN_DAU", 1.4),                                             # đầu (mũ, mắt, lửa trên mũ)
    **{b: _f("KN_LUA", 0.58) for b in ("bone26", "bone27", "bone28", "bone29", "bone30")},   # gốc năm chuỗi lửa trên mũ
    "bone7": _f("KN_TAY", 0.85), "bone43": _f("KN_TAY", 0.85),              # cánh tay trên hai bên (cả cẳng, bàn, kiếm, giáp vai theo)
    "bone9": _f("KN_BAN", 1.1), "bone45": _f("KN_BAN", 1.1),                # bàn tay
    "bone31": _f("KN_VAI", 0.8),                                             # giáp vai (con của cánh tay trên)
    "bone23": _f("KN_KIEM", 0.8),                                            # kiếm (con của bàn tay)
    "bone40": _f("KN_AO", 0.85), "bone67": _f("KN_AO", 0.85),               # vạt trước, áo choàng sau
}
RES = 2
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
_S120 = os.path.join(SCAN, "sample_120.json")                 # skill_01 lấy mẫu 120 khung/giây: nhát bổ của họ chỉ chĩa tới trước ở 0,36 s
if os.path.exists(_S120):
    S.update(json.load(open(_S120, encoding="utf-8")))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
ZERO5 = np.array([0, 0, 0, 1, 1.0])
USE = ["idle_01", "run_01", "skill_01", "skill_03_1", "skill_03_2", "skill_03_3", "die_01", "hit_01"]
BO_SLOT = {"shadow", "wangge", "effect_yanwu", "P_yanwu", "P_yanwu2", "P_yanwu3"}     # khói đen của họ: VFX của mình làm khói hồn
CANH_TAY = ("bone2", "bone3", "bone6", "bone7", "bone8", "bone9", "bone23")         # chuỗi thân → tay gần → kiếm


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
    """chỗ chèn của slot di động m trong thứ tự vẽ o: số slot đứng yên được vẽ trước nó."""
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
            Am = np.array([[F["l"][i][2] - z[2], F["l"][i][0] - z[0], F["l"][i][1] - z[1],
                            F["l"][i][3] / (z[3] or 1.0), F["l"][i][4] / (z[4] or 1.0)] for F in fr])
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


def mau(clip, t, lap=False, chi=None, tru=()):
    dur, R, fps = CD[clip][0], CD[clip][1], CD[clip][4]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * fps
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
    dur, fps = CD[clip][0], CD[clip][4]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * fps
    return min(len(CD[clip][2]) - 1, int(round(x)))


def pha_gan(a, b, w):
    """trộn hai dáng, góc của b quy về cùng vòng với a."""
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


def tq(t, bang):
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / max(1e-9, b_ - a_)
    return bang[-1][1]


def tat_dan(t, t0, bien, tan, giam):
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def hien_theo_ho(sk, P, clip, t, lap=False, mat=1.0, hon=0.0, cat=False):
    """độ đậm + hình của mọi slot theo khung của họ; slot di động bật đúng bản theo chỗ chèn; mắt theo mũ × mat; phần vá hồn theo kiếm × hon."""
    i = khung_ho(clip, t, lap)
    hinh, cho = CD[clip][2][i], CD[clip][3][i]
    for k, sl in enumerate(SL):
        if sl in BO_SLOT or sl not in sk.si:
            continue
        n, a = hinh[k]
        ten = [ten_ban(k, kk) for kk in BAN[k]] if k in NEO0 else [sl]
        for nm in ten:
            bat = n is not None and (k not in NEO0 or nm == ten_ban(k, cho[k]))
            P.alpha[nm] = a if bat else 0.0
            if bat and n in sk.atts.get(nm, {}) and len(sk.atts[nm]) > 1:
                P.att[nm] = n
            goc_ = nm.split("@")[0]
            duoi_ = nm[len(goc_):]
            if goc_ == "P_tou" and "P_mat" + duoi_ in sk.si:
                P.alpha["P_mat" + duoi_] = (a if bat else 0.0) * mat
            if goc_ == "P_jian" and "P_jian_hon" + duoi_ in sk.si:
                v_ = (a if bat else 0.0) * float(hon)
                P.alpha["P_jian_hon" + duoi_] = v_
                # mặt nạ cắt bật suốt đoạn chiêu cuối có phần vá (cat), TRƯỚC khi phần vá hiện: khoá đổi hình của mặt nạ có thể trễ một khung
                P.att["P_jian_cat" + duoi_] = "cat" if (cat and bat) else None


# ---------------------------------------------------------------- dựng
def manh_goc():
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    os.makedirs(MANH, exist_ok=True)
    tot = {}                                              # vùng dùng chung hai slot (P_jianjia / P_jianjia2): cắt theo lưới lớn nhất
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
        k_ = TI_LE.get(b["name"], 1.0)
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1], goc=z[2], dai=b["len"], sx=z[3] * k_, sy=z[4] * k_)
    Wi = sk.the_gioi()
    # thế giới dáng gốc KHÔNG đổi tỉ lệ (= dạng 2): mảnh cứng có toạ độ thế giới dạng 2 (da dạng 2, hoặc mảnh dạng 1 ghi "he": "lon") gắn
    # theo hệ này thì co / phóng cùng xương; mảnh vẽ ở dáng dạng 1 thì gắn theo Wi
    if TI_LE:
        sk_c = Sk("_c")
        sk_c.xuong("root")
        sk_c.xuong("move", "root")
        for i, b in enumerate(I["bones"]):
            if b["name"] != "root":
                z = L0[i]
                sk_c.xuong(b["name"], "move" if NB[b["parent"]] == "root" else NB[b["parent"]], z[0], z[1], goc=z[2], dai=b["len"], sx=z[3], sy=z[4])
        Wc = sk_c.the_gioi()
    else:
        Wc = Wi
    HE = {}

    def W_he(bone, ten_anh=None):
        return Wi[bone] if (DA_NON and HE.get(ten_anh) != "lon") else Wc[bone]
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hinh0 = CD["idle_01"][2][0]
    IM = {}

    def anh_cua(r, goc_a=None):
        if r not in IM:
            p = os.path.join(MANH, r + ".png")
            if os.path.exists(p):
                g = Image.open(p).convert("RGBA")
            elif r in ("P_yanse", "P_yanse01"):                    # ô màu sau khe mắt mũ của họ: tô tối
                g = Image.new("RGBA", (8, 8), (31, 35, 33, 255))
            elif goc_a is not None and os.environ.get("KN_THIEU") == "1":   # chưa có mảnh: tạm da gốc (chỉ để thử)
                im_ = G.part_goc(goc_a)
                g = im_.resize((im_.width * RES, im_.height * RES), Image.LANCZOS)
            else:
                raise SystemExit(f"thiếu mảnh {p}")
            k_ = float(os.environ.get("KN_PX") or 0.6)          # ảnh mảnh 1 px / đơn vị → KN_PX px / đơn vị (atlas nhỏ, .atomik dưới trần)
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
        """mảnh cứng: ô 4 đỉnh (thế giới khung 0 idle) bám trọn một xương."""
        im = anh_cua(ten_anh)
        ten_att = ten_att or ten_anh
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        Wb = W_he(bone, ten_anh)
        rows = [[(bone, *map(float, np.linalg.solve(Wb, np.array([v[0], v[1], 1.0]))[:2]), 1.0)] for v in Vw]
        V0 = np.array([(Wi[bone] @ np.array([r_[0][1], r_[0][2], 1.0]))[:2] for r_ in rows])
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.atts[slot_ten][ten_att] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": tris, "hull": 4, "V": V0, "verts": rows,
                                      "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_att)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)

    # ---- mảnh cứng (moi.json): slot của họ → [(tên ảnh, xương, 4 góc thế giới khung 0 idle)], bản đầu là hình mặc định
    MOI = {}
    pm = os.path.join(MANH, "moi.json")
    if not GOC and os.path.exists(pm):
        for ten, d in json.load(open(pm)).items():
            MOI.setdefault(d["slot"], []).append((ten, d["xuong"], np.array(d["the_gioi"], float)))
            HE[ten] = d.get("he")

    by_slot = {}
    for a in AG["atts"]:
        if a.get("region") in imgs_ho:
            by_slot.setdefault(a["slot"], []).append(a)

    # ---- phần vá hồn: MỘT ảnh bám cứng bone23 (cùng khung với ảnh kiếm gãy: khít từng răng vết gãy) + mặt nạ cắt bám xương hon_dau (con
    # hon_goc ở chỗ gãy, trục x dọc lưỡi về mũi): chỉ lộ phần vá nằm SAU mép hon_dau; clip dời hon_dau theo bàn tay → phần vá hiện dần theo tay
    VA = {}
    if "P_jian_hon" in MOI:
        d0 = next(d for d in json.load(open(pm)).values() if d["slot"] == "P_jian_hon")
        g_, m_ = np.array(d0["gay"], float), np.array(d0["mui"], float)
        Wk = W_he("bone23", MOI["P_jian_hon"][0][0])          # cùng hệ với ảnh vá: đơn vị dọc hon_goc = đơn vị thế giới của hệ đó
        lg = np.linalg.solve(Wk, np.array([*g_, 1.0]))[:2]
        lm = np.linalg.solve(Wk, np.array([*m_, 1.0]))[:2]
        sk.xuong("hon_goc", "bone23", float(lg[0]), float(lg[1]), goc=math.degrees(math.atan2(*(lm - lg)[::-1])))
        sk.xuong("hon_dau", "hon_goc", 0.0, 0.0)
        sk.xuong("mui_hon", "hon_goc", float(np.hypot(*(lm - lg))), 0.0)
        Wi = sk.the_gioi()
        VA = dict(anh=MOI["P_jian_hon"][0][0], Vw=MOI["P_jian_hon"][0][2], a0=float(d0["a0"]), dai=float(np.hypot(*(m_ - g_))))

    def them(slot_goc, ten, hien):
        ats = by_slot.get(slot_goc)
        if not ats:
            return
        if slot_goc in MOI:
            m0 = MOI[slot_goc][0]
            sk.slot(ten, m0[1], m0[0], an=not hien)
            for ten_anh, bn, Vw in MOI[slot_goc]:
                gan_cung(ten, ten_anh, bn, Vw)
        else:
            mac = next((a for a in ats if a["cur"]), ats[0])
            sk.slot(ten, "move", mac["att"], an=not hien)
            for a in ats:
                gan(ten, a)
            sk._slot(ten)["bone"] = sk.atts[ten][mac["att"]]["verts"][0][0][0]
        if slot_goc == "P_jian" and VA:                           # mặt nạ cắt + phần vá ngay trên kiếm, cùng chỗ chèn (chiêu cuối bật)
            tc_ = ten.replace("P_jian", "P_jian_cat", 1)
            th_ = ten.replace("P_jian", "P_jian_hon", 1)
            sk.slot(tc_, "hon_dau")
            sk.slot(th_, "bone23", VA["anh"], an=True)
            gan_cung(th_, VA["anh"], "bone23", VA["Vw"])
            Wd = Wi["hon_dau"]
            sk.cat(tc_, th_, [tuple((Wd @ np.array([x, y, 1.0]))[:2]) for x, y in ((-3000, -500), (0, -500), (0, 500), (-3000, 500))])
            sk._slot(tc_)["att"] = None                           # tắt mặc định: runtime khỏi cắt ở mọi clip khác
        if slot_goc == "P_tou" and "P_mat" in MOI:                # mắt ngay trên mũ, cùng chỗ chèn
            m_ = MOI["P_mat"][0]
            tm = ten.replace("P_tou", "P_mat", 1)
            sk.slot(tm, m_[1], m_[0], an=not hien)
            gan_cung(tm, m_[0], m_[1], m_[2])

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

    # ---- mũi kiếm (xương mieng, con của bone23): điểm đặc của ảnh kiếm xa gốc xương nhất
    if "P_jian" in MOI:
        ten_k, _, Vw = MOI["P_jian"][0]
        g = np.asarray(IM[ten_k])[..., 3] > 120
        ys, xs = np.nonzero(g)
        u, v = (xs + 0.5) / g.shape[1], (ys + 0.5) / g.shape[0]
        Pw = (Vw[0][None] * ((1 - u) * (1 - v))[:, None] + Vw[1][None] * (u * (1 - v))[:, None] + Vw[2][None] * (u * v)[:, None]
              + Vw[3][None] * ((1 - u) * v)[:, None])
        Wk = W_he("bone23", ten_k)
    else:
        a_ = by_slot["P_jian"][0]
        Pw = np.array(a_["xy"], float).reshape(-1, 2)
        Pw = np.array([(Wi["bone23"] @ np.linalg.solve(WG["bone23"], np.array([p[0], p[1], 1.0])))[:2] for p in Pw])
        Wk = Wi["bone23"]
    loc = np.array([np.linalg.solve(Wk, np.array([p[0], p[1], 1.0]))[:2] for p in Pw])
    d_ = np.hypot(loc[:, 0], loc[:, 1])
    mui = loc[int(np.argmax(d_))]
    sk.xuong("mieng", "bone23", float(mui[0]), float(mui[1]))
    for e, m in (("trung", "khung đòn trúng"), ("lao", "bắt đầu lao tới"), ("chem", "nhát chém (vệt chém theo bone23 → mieng)"),
                 ("goi", "giơ kiếm lên trời: gọi hồn đồng đội (VFX + code cho hồn bay tới đối thủ)"), ("hut", "tay bắt đầu vuốt dọc lưỡi: hồn xanh hút vào chỗ gãy, phần vá hiện dần theo tay (VFX bám xương hon_dau)"),
                 ("hat", "tay hất lên: đoạn vá còn lại phóng tới mũi"), ("hoi_phuc", "kiếm vá xong (chớp xanh dọc lưỡi)"), ("gong", "giơ kiếm qua đầu, aura bùng"),
                 ("tat", "phần vá hồn tan"), ("mat_sang", "mắt bật sáng xanh"), ("bay_len", "các mảnh giáp nhấc lên"), ("rap", "giáp ráp xong"),
                 ("hon_thoat", "hồn xanh thoát khỏi giáp"), ("nga", "giáp đổ sụp xuống đất")):
        sk.su_kien(e, m)
    hien0 = {s["name"] for s in sk.slots if s.get("alpha", 1) > 0 and not s.get("an")}
    cao = float(max(sp["V"][:, 1].max() for sn, sl in sk.atts.items() if sn in hien0 for sp in sl.values() if "V" in sp))
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao {cao:.0f}; slot di động: "
          + ", ".join(f"{SL[m]} {BAN[m]}" for m in DONG))
    return sk, dict(cao=cao, va=VA)


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    out = []
    cao = info["cao"]

    # idle_01 của họ dài 10 s = chu kỳ gốc 2,0 s (khung 60 gần trùng khung 0) + một đoạn biến tấu 2–8 s. Lấy chu kỳ 2,0 s (giữ .atomik dưới
    # trần dung lượng), 0,25 s cuối hoà về khung 0 cho khép vòng liền
    D_ID = 2.0

    def idle(t, P):
        u = t % D_ID if t < D_ID - 1e-6 else 0.0
        d_ = mau("idle_01", u)
        if u > D_ID - 0.25:
            d_ = pha_gan(d_, mau("idle_01", 0.0), em((u - (D_ID - 0.25)) / 0.25))
        dat(P, d_)
        hien_theo_ho(sk, P, "idle_01", u if u < D_ID - 0.05 else 0.0)
    out.append(Clip("idle", D_ID, idle, loop=True))

    def walk(t, P):
        u = t if t < CD["run_01"][0] - 1e-6 else 0.0
        dat(P, mau("run_01", u))
        hien_theo_ho(sk, P, "run_01", u)
    out.append(Clip("walk", CD["run_01"][0], walk, loop=True))

    def hit(t, P):
        dat(P, mau("hit_01", t))
        hien_theo_ho(sk, P, "hit_01", t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ---- DIE: die_01 (hồn thoát, giáp đổ sụp thành đống), mắt tắt dần 0,25–0,70, mờ 0,32 s cuối
    D_DIE0 = CD["die_01"][0]
    D_DIE = D_DIE0 + 0.45

    def die(t, P):
        dat(P, mau("die_01", t))
        hien_theo_ho(sk, P, "die_01", t, mat=1.0 - em((t - 0.25) / 0.45))
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.20, "hon_thoat", ""), (1.55, "nga", "")]))

    # ---- APPEAR: die_01 chạy NGƯỢC. Đống giáp nằm đất (khung cuối die), mắt tối → bật sáng xanh (nhấp nháy hai lần) → các mảnh nhấc lên
    # lơ lửng ráp lại (die 2,0 → 0, chậm lúc nhấc, nhanh dần, khựng nhẹ lúc ráp) → về khung 0 idle.
    T_MAT, T_BAY, T_RAP, D_AP = 0.40, 0.75, 2.30, 2.65

    def appear(t, P):
        if t < T_BAY:
            u = D_DIE0
        elif t < T_RAP:
            q = (t - T_BAY) / (T_RAP - T_BAY)
            u = D_DIE0 * (1.0 - (q * q * (3 - 2 * q)) ** 1.15)
        else:
            u = 0.0
        d_ = mau("die_01", u)
        VAT = ("bone40", "bone41", "bone41b", "bone41c", "bone41d")   # vạt trước quất nhanh khi tua ngược: trung bình ±0,08 s
        ls_ = [mau("die_01", min(D_DIE0, max(0.0, u + k * 0.04)), chi=VAT) for k in (-2, -1, 0, 1, 2)]
        for b_ in VAT:
            if b_ in d_:
                d_[b_] = np.mean([l_[b_] for l_ in ls_ if b_ in l_], axis=0)
        if t > T_RAP:                                     # ráp xong: hoà về idle 0, thân nảy nhẹ
            d_ = pha_gan(d_, mau("idle_01", 0.0), em((t - T_RAP) / (D_AP - T_RAP)))
        dat(P, d_)
        nay = 0.04 * cao * math.sin(math.pi * min(1.0, max(0.0, (t - T_RAP) / 0.25))) if t > T_RAP else 0.0
        P.move("move", 0.0, nay)
        mat = 0.0 if t < T_MAT else min(1.0, (t - T_MAT) / 0.05) * (0.35 if T_MAT + 0.10 < t < T_MAT + 0.16 else 1.0)
        hien_theo_ho(sk, P, "die_01", u, mat=mat)
        a_ = min(1.0, t / 0.10)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(T_MAT, "mat_sang", ""), (T_BAY, "bay_len", ""), (T_RAP, "rap", "")]))

    # ---- ĐÁNH THƯỜNG: skill_01 (vung kiếm qua đầu ra sau 0,15–0,30, bổ qua phía trước 0,30–0,40, lao người theo đà 0,40–0,65) + lao tới
    # nhát bổ của họ 0,33 → 0,375 (kiếm chĩa tới trước ở 0,36) giãn ra 0,10 s cho thấy cung chém
    U_ATK = [(0.0, 0.0), (0.36, 0.30), (0.40, 0.33), (0.50, 0.375), (0.56, 0.40), (0.78, 0.65), (1.12, 1.0)]
    D_ATK = 1.12
    T_CHEM = 0.467
    LAO = 0.72 * 1.9 * cao

    def attack(t, P):
        u = tq(t, U_ATK)
        dat(P, mau("skill_01", u))
        hien_theo_ho(sk, P, "skill_01", u)
        lao = LAO * em((t - 0.06) / 0.38) * (1 - em((t - 0.78) / 0.34))
        P.move("move", lao, 0.0)
    out.append(Clip("attack", D_ATK, attack, ev=[(0.06, "lao", ""), (0.40, "chem", ""), (T_CHEM, "trung", "")], trung=T_CHEM))

    # ---- CHIÊU MANA: skill_03_2, đoạn giơ kiếm thẳng lên trời (1,70 → 2,05), GIỮ trên trời lâu (gọi hồn), hạ kiếm về
    U_CAST = [(0.0, 1.70), (0.62, 2.05), (1.40, 2.30), (1.85, 2.73)]
    D_CAST = 1.85
    T_GOI = 0.70

    def cast(t, P):
        u = tq(t, U_CAST)
        d_ = mau("skill_03_2", u)
        if t < 0.30:                                      # vào: từ idle 0 sang dáng 1,70 của họ
            d_ = pha_gan(mau("idle_01", 0.0), d_, em(t / 0.30))
        dat(P, d_)
        run = 0.6 * math.sin(2 * math.pi * 9 * t) * (em((t - 0.62) / 0.1) * (1 - em((t - 1.30) / 0.1)))
        P.rot("bone8", run)
        hien_theo_ho(sk, P, "skill_03_2", u)
    out.append(Clip("cast", D_CAST, cast, ev=[(T_GOI, "goi", ""), (1.05, "trung", "")], trung=1.05))

    # ---- CHIÊU CUỐI (người dùng 2026-11-16: phần kiếm hồn hiện dần THEO TAY khi vuốt lên, ngắn, khít vết gãy như vá kiếm bằng vật liệu khác)
    # dựng kiếm trước mặt (skill_03_1 0 → 0,40), tay kia VUỐT CHẬM lên dọc lưỡi (0,40 → 1,16; cộng góc vai / khuỷu cho tay sát và cao hơn):
    # mép hiện của phần vá chạy dọc lưỡi theo độ cao bàn tay (đi trước tay một chút như tay kéo lưỡi ra); vá xong (hoi_phuc) giữ, giơ qua đầu
    # (skill_03_2 @ 2,0), vung ra sau rồi BỔ (skill_01 0,34 → 0,36), chúc xuống, khựng + rung; phần vá tan trong lúc khựng; thu theo đà.
    T_A0, T_A1, T_B0, T_B1, T_C0, T_C1, T_D0 = 0.50, 1.72, 2.00, 2.30, 2.55, 2.67, 3.15
    T_P, T_Q = 0.80, 1.55                                 # tay lên nhanh dọc lưỡi sắt tới chỗ gãy | vuốt chậm dọc phần vá | hất lên: phần còn lại phóng tới mũi
    U_A0, U_P, U_Q, U_A1 = 0.40, 0.63, 1.18, 1.22
    LEAD = 50.0                                           # mép hiện đi trước lòng bàn tay (đơn vị dọc lưỡi)
    T_TAN = 0.24
    T_TAT = T_D0 - T_TAN
    CHUC = -7.0
    D_SK = 3.75
    U_CHEM0, U_CHEM = 0.34, 0.36
    TAY_VAI, TAY_KHUYU = 22.0, 12.0                       # cộng thêm cho bàn tay xa vuốt sát mép, cao dọc lưỡi

    def dang(t, P):
        """đặt dáng xương của chiêu cuối ở giây t; trả (clip, giây nguồn) cho hien_theo_ho."""
        if t < T_A0:
            u, clip = t / T_A0 * U_A0, "skill_03_1"
            d_ = mau(clip, u)
        elif t < T_P:
            u, clip = U_A0 + (U_P - U_A0) * em((t - T_A0) / (T_P - T_A0)) ** 0.8, "skill_03_1"
            d_ = mau(clip, u)
        elif t < T_Q:
            u, clip = U_P + (U_Q - U_P) * (t - T_P) / (T_Q - T_P), "skill_03_1"
            d_ = mau(clip, u)
        elif t < T_A1:
            q = (t - T_Q) / (T_A1 - T_Q)
            u, clip = U_Q + (U_A1 - U_Q) * (1 - (1 - q) ** 2), "skill_03_1"
            d_ = mau(clip, u)
        elif t < T_B0:
            u, clip = U_A1, "skill_03_1"
            d_ = mau(clip, u)
        elif t < T_B1:
            u, clip = 2.0, "skill_03_2"
            d_ = pha_gan(mau("skill_03_1", 1.24), mau(clip, u), em((t - T_B0) / (T_B1 - T_B0)))
        elif t < T_C0:
            u, clip = 2.0, "skill_03_2"
            d_ = mau(clip, u)
        elif t < T_C1:
            q = (t - T_C0) / (T_C1 - T_C0)
            clip = "skill_01"
            if q < 0.5:
                u = U_CHEM0
                d_ = pha_gan(mau("skill_03_2", 2.0), mau(clip, u), em(q / 0.5))
            else:
                u = U_CHEM0 + (U_CHEM - U_CHEM0) * ((q - 0.5) / 0.5) ** 1.4
                d_ = mau(clip, u)
        elif t < T_D0:
            u, clip = U_CHEM, "skill_01"
            d_ = mau(clip, u)
        else:
            u, clip = U_CHEM + (t - T_D0) / (D_SK - T_D0) * (1.0 - U_CHEM), "skill_01"
            d_ = mau(clip, u)
        dat(P, d_)
        w = em((t - T_A0) / 0.40) * (1 - em((t - T_A1) / 0.30))
        if w > 0:
            P.rot("bone43", TAY_VAI * w)
            P.rot("bone44", TAY_KHUYU * w)
        if T_C0 + 0.06 <= t < T_D0 + 0.15:
            P.rot("bone23", CHUC * em((t - (T_C0 + 0.06)) / 0.06) * (1 - em((t - T_D0) / 0.15)))
        if T_C1 <= t < T_D0:
            P.move("move", tat_dan(t, T_C1, 0.012 * cao, 14.0, 0.10), 0.0)
        return clip, u

    # mép hiện r(t) (đơn vị dọc lưỡi từ chỗ gãy) theo độ cao bàn tay xa chiếu lên trục lưỡi: lấy cực đại dồn (chỉ tiến), ánh xạ đoạn tay đi
    # [P0, cao nhất] → [đầu lát 0, mũi]
    VA = info.get("va") or {}
    L_VA = VA.get("dai", 0.0)
    ts_ = np.arange(T_A0, T_A1 + 1e-6, 1.0 / 120)
    ps_ = []
    if VA:
        for t_ in ts_:
            Q = Pose()
            dang(t_, Q)
            Wq = sk.the_gioi(Q)
            h = 0.5 * (Wq["bone53"][:2, 2] + Wq["bone57"][:2, 2])
            g, ax = Wq["hon_goc"][:2, 2], Wq["hon_goc"][:2, 0]
            ps_.append(float((h - g) @ ax) / float(ax @ ax))          # đơn vị dọc hon_goc (dạng 1: xương kiếm thu, chia lại cho tỉ lệ)
        ps_ = np.maximum.accumulate(np.array(ps_))
        r0 = VA["a0"]
        print(f"  chiêu cuối: bàn tay xa chiếu lên lưỡi {ps_[0]:.0f} → {ps_[-1]:.0f} (chỗ gãy = 0; lúc T_P {np.interp(T_P, ts_, ps_):.0f}, "
              f"T_Q {np.interp(T_Q, ts_, ps_):.0f}), phần vá {r0:.0f} → {L_VA:.0f}")

    def mep(t):
        """mép hiện: bám lòng bàn tay (+LEAD) tới T_Q; T_Q → T_A1 tay hất lên, phần còn lại phóng tới mũi (chậm dần)."""
        if not VA or t < T_A0:
            return -1e9
        if t >= T_A1:
            return 1e9
        if t < T_Q:
            return float(np.interp(t, ts_, ps_)) + LEAD
        rq = float(np.interp(T_Q, ts_, ps_)) + LEAD
        q = (t - T_Q) / (T_A1 - T_Q)
        return rq + (L_VA + 30.0 - rq) * (1 - (1 - q) ** 2.2)

    def skill(t, P):
        clip, u = dang(t, P)
        r = mep(t)
        hon = 1.0 if (VA and r > r0 + 4.0 and t < T_D0 and t >= T_A0 + 0.10) else 0.0
        if t > T_TAT:
            hon *= 1.0 - em((t - T_TAT) / T_TAN)
        if "hon_dau" in sk.bi:
            P.move("hon_dau", float(min(max(r, r0 - 20.0), L_VA + 60.0)), 0.0)
        hien_theo_ho(sk, P, clip, u, hon=hon, cat=bool(VA) and T_A0 - 0.10 <= t < T_D0 + 0.05)
    out.append(Clip("skill", D_SK, skill, ev=[(T_A0, "hut", ""), (T_Q, "hat", ""), (T_A1, "hoi_phuc", ""), (T_B1, "gong", ""), (T_C0 + 0.05, "chem", ""),
                                             (T_C1, "trung", ""), (T_TAT, "tat", "")], trung=T_C1))
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


SPAN = 6.0


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
            print(f"{c.ten:7s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°"))
        return
    if a and a[0] == "bo_cuc":                # hình bố cục: khung 0 idle nền trắng (ảnh mẫu tỉ lệ cho concept dạng khác)
        fr = nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.10)
        sc_ = float(a[2]) if len(a) > 2 else 1.0
        im = ve.ve(fr[0], Bx, sc_, bg=(255, 255, 255), ss=2).convert("RGB")
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        im.save(a[1])
        json.dump(dict(box=list(Bx), scale=sc_, ti_le=TI_LE), open(a[1][:-4] + ".json", "w"), indent=1)   # px = ((X − x0)·sc, (y1 − Y)·sc)
        print(a[1], im.size)
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
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
    xuat.xuat_het(sk, clips, RA, TEN, ("Kỵ sĩ non dạng 1 (ky_nguyen_non)" if NON else "Kỵ sĩ cổ đại bị nguyền (ky_nguyen)") + ": tướng 8 đảo Kim"
                  + (" — DA GỐC, chỉ để soi clip" if GOC else "") + (" — DA TẠM DẠNG 2" if NON and not DA_NON else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=("cast", "skill"), lao=(), far=(), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.08, "translate": 0.2, "scale": 0.002}, khop_idle=0.2, span=SPAN,
                  impact={"attack": (0.05, 0.28, 0.07), "skill": (0.26, 1.2, 0.22, "#b6ff7a30")})


if __name__ == "__main__":
    main(sys.argv[1:])
