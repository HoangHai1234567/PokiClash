# -*- coding: utf-8 -*-
"""Thú giáp pháo (thu_phao, tướng 9 đảo Kim): RESKIN trên rig con gốc monster_3629 (thú bốn chân giáp khối, đuôi cuộn lên lưng thành pháo).

- Xương: đủ mọi xương của họ + `move`, `mieng` (giữa họng pháo, con của bone97: chỗ đạn / cầu năng lượng ra, trục x của bone97 = hướng nòng),
  `loi` (lõi tròn ở đuôi pháo, con của bone30). Dáng gốc = khung 0 idle_01 (biến đổi riêng `l` lấy mẫu bằng runtime Spine thật).
- Hình: mỗi hình của họ một hình của mình, NGUYÊN lưới của họ. Mảnh đổi dáng (manh/moi.json) là ô 4 đỉnh bám một xương.
- Thứ tự vẽ của họ chỉ đổi ở die_01: slot "di động" nhân bản theo CHỖ CHÈN (skill pokiclash-spine-rig mục 28).
- Clip: idle (chu kỳ 2 s của idle_01) / walk (run_01) / hit (hit_01) = của họ; die = die_01 (giáp vỡ, đổ sụp) + mờ;
  attack = skill_01 (nâng nòng, bắn một quả đạn sắt, giật mạnh hơn họ); cast = skill_03 (nòng chĩa trời, bắn liền 5 quả, mỗi quả một cú giật;
  code cho đạn tách thành tên lửa nhỏ homing); skill = skill_04_1 kéo dài (thủ thế, nòng thò dài, GỒNG tụ cầu năng lượng lớn ở họng, rung
  dần, BẮN: giật lùi rất mạnh, khựng, rung, trượt về); appear (Claude tự đặt) = thả từ trên trời xuống, nòng chĩa trời, dộng đất, nhún, nòng
  hạ xuống khoá cạch (vượt nhẹ), nòng thụt thử một cái xì khói, lõi sáng.

    thu_phao_rig.py                         dựng, xuất inbox/thu_phao_1/rig/
    thu_phao_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    thu_phao_rig.py kiem                    bước xoay lớn nhất giữa hai khung của từng clip
    TP_GOC=1 thu_phao_rig.py ...            dựng bằng DA GỐC ra rig_goc/: chỉ để soi clip trong máy, không đưa vào game
    TP_DANG=non thu_phao_rig.py ...         DẠNG 1 (non): cùng xương / lưới / clip, đổi tỉ lệ (TI_LE), mảnh inbox/thu_phao_non/manh (chưa có
                                            thì mượn da dạng 2) → inbox/thu_phao_non/rig/ (thu_phao_non.atomik)
    thu_phao_rig.py bo_cuc <png> [tỉ lệ]    khung 0 idle nền trắng
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
from quai import anh, xuat, soi  # noqa: E402
from quai.khung import Sk, Pose  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.luoi import Luoi  # noqa: E402
import thu_phao as G  # noqa: E402

GOC = os.environ.get("TP_GOC") == "1"
# DẠNG 1 (TP_DANG=non; người dùng 2026-11-17 "ok làm dạng 1 cho tướng này"): CÙNG xương / lưới / clip, đổi tỉ lệ ở xương gốc từng bộ phận
# (xương con thừa hưởng): đầu to, tai ngắn lại (tương đối), pháo nhỏ, đuôi ngắn. Chân giữ (bàn chân là đích IK dưới bone2: thu chân là hở)
NON = os.environ.get("TP_DANG") == "non" and not GOC
BASE = os.path.join(os.path.dirname(G.BASE), "thu_phao_non") if NON else G.BASE
TEN = "thu_phao_non" if NON else "thu_phao"
RA = os.environ.get("TP_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("TP_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
if NON and not os.path.isdir(MANH):
    MANH = os.path.join(G.BASE, "manh")                  # chưa có da dạng 1: dựng bố cục bằng da dạng 2
DA_NON = NON and os.path.normpath(MANH) == os.path.normpath(os.path.join(BASE, "manh"))


def _f(k, v):
    return float(os.environ.get(k) or v)


TI_LE = {} if not NON else {
    "bone28": _f("TP_DAU", 1.45),                                            # đầu (mũ, mắt, hai tai theo)
    "bone36": _f("TP_TAI", 0.8), "bone37": _f("TP_TAI", 0.8),               # hai tai (con của đầu: tổng ≈ 1,16)
    "bone99": _f("TP_PHAO", 0.78),                                           # pháo (thân, họng, lõi, cánh theo)
    "bone24": _f("TP_DUOI", 0.85),                                           # chuỗi đuôi + bốn vảy đuôi
}
RES = 2
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
ZERO5 = np.array([0, 0, 0, 1, 1.0])
USE = ["idle_01", "run_01", "skill_01", "skill_03", "skill_04_1", "die_01", "hit_01"]
BO_SLOT = {"shadow", "wangge"}
if not GOC:
    BO_SLOT |= {"P_tou01"}                         # da mình: khối đỉnh đầu gộp vào mũ (P_tou00 → "mu")
# Pháo theo đúng khung part của họ (tờ K7, người dùng 2026-11-17 chê bản pháo phẳng 2D): thứ tự vẽ như họ, mặt bên khối họng tự giãn khi nòng
# vươn nên không cần ống nòng. DOI_SAU / "nong" giữ làm đường dời slot nếu sau này cần.
DOI_SAU = {}
HOAN = {s for v in DOI_SAU.values() for s in v}
MIENG_PX = (965.0, 255.0)        # giữa ô cửa vòm sáng của khối họng (ảnh mau/goc_ca_con.png): chỗ ra đạn khi chưa có mảnh mới


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


def cong(d, bone, rot=0.0, x=0.0, y=0.0):
    """cộng thêm góc / độ dời lên một xương của dáng d."""
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


def tat_dan(t, t0, bien, tan, giam):
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def giat(t, t0, sau=0.035, ve=0.16):
    """đường giật: 0 → 1 trong `sau` giây (bật), rồi về 0 chậm dần trong `ve` giây."""
    if t < t0:
        return 0.0
    s = t - t0
    if s < sau:
        return em(s / sau)
    return max(0.0, 1.0 - em((s - sau) / ve))


def hien_theo_ho(sk, P, clip, t, lap=False):
    """độ đậm + hình của mọi slot theo khung của họ; slot di động bật đúng bản theo chỗ chèn."""
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


# ---------------------------------------------------------------- dựng
def manh_goc():
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    os.makedirs(MANH, exist_ok=True)
    tot = {}                                              # vùng dùng chung hai slot: cắt theo lưới lớn nhất
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


def px_the_gioi(px, py):
    """điểm trên ảnh mau/goc_ca_con.png → toạ độ thế giới dáng gốc (khung 0 idle)."""
    J = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    return np.array([J["cx"] + (px - 768.0) / J["s"], J["cy"] - (py - 512.0) / J["s"]])


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
            elif goc_a is not None and os.environ.get("TP_THIEU") == "1":   # chưa có mảnh: tạm da gốc (chỉ để thử)
                im_ = G.part_goc(goc_a)
                g = im_.resize((im_.width * RES, im_.height * RES), Image.LANCZOS)
            else:
                raise SystemExit(f"thiếu mảnh {p}")
            k_ = float(os.environ.get("TP_PX") or 0.6)          # ảnh mảnh 1 px / đơn vị → TP_PX px / đơn vị (atlas nhỏ, .atomik dưới trần)
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
    MOI, MOI_D = {}, {}
    pm = os.path.join(MANH, "moi.json")
    if not GOC and os.path.exists(pm):
        MOI_D = json.load(open(pm))
        for ten, d in MOI_D.items():
            if "slot" in d:
                MOI.setdefault(d["slot"], []).append((ten, d["xuong"], np.array(d["the_gioi"], float)))
                HE[ten] = d.get("he")

    by_slot = {}
    for a in AG["atts"]:
        if a.get("region") in imgs_ho:
            by_slot.setdefault(a["slot"], []).append(a)

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
            if SL[s_] in HOAN:
                if SL[s_] == "P_pao01_2" and "nong" in MOI:      # ống nòng ở chỗ cũ của họng: sau thân pháo
                    ten_n, bn_n, Vw_n = MOI["nong"][0]
                    sk.slot("nong", bn_n, ten_n)
                    gan_cung("nong", ten_n, bn_n, Vw_n)
                continue
            them(SL[s_], SL[s_], hien=hinh0[s_][0] is not None)
            for s2 in DOI_SAU.get(SL[s_], []):
                them(s2, s2, hien=hinh0[SL.index(s2)][0] is not None)

    # ---- họng pháo (mieng, con của bone97, trục x theo nòng) + lõi (loi, con của bone30)
    mw = np.array(MOI_D["_mieng"]["the_gioi"], float) if "_mieng" in MOI_D else px_the_gioi(*MIENG_PX)
    lm = np.linalg.solve(Wc["bone97"], np.array([mw[0], mw[1], 1.0]))[:2]
    sk.xuong("mieng", "bone97", float(lm[0]), float(lm[1]))
    lw = np.array(MOI_D["_loi"]["the_gioi"], float) if "_loi" in MOI_D else px_the_gioi(457.0, 444.0)
    ll = np.linalg.solve(Wc["bone30"], np.array([lw[0], lw[1], 1.0]))[:2]
    sk.xuong("loi", "bone30", float(ll[0]), float(ll[1]))
    for e, m in (("trung", "khung đòn trúng"), ("ban", "một phát bắn (đạn / cầu ra từ xương mieng, hướng trục x của bone97)"),
                 ("nap", "nòng thò ra, nạp đạn (chiêu mana)"), ("gong", "bắt đầu gồng: năng lượng tụ về họng pháo"),
                 ("day", "cầu năng lượng tụ đầy, rung mạnh nhất"), ("cham_dat", "appear: dộng xuống đất (bụi, sóng đất, nứt)"),
                 ("khoa", "appear: nòng hạ xuống khoá cạch (tia lửa ở khớp nòng)"), ("xa_khoi", "appear: nòng thụt thử, họng xì khói"),
                 ("loi_sang", "appear: lõi tròn bật sáng"), ("vo", "die: giáp vỡ, mảnh bắn ra"), ("tat_loi", "die: lõi tắt"),
                 ("nga", "die: đổ sụp xuống đất")):
        sk.su_kien(e, m)
    hien0 = {s["name"] for s in sk.slots if s.get("alpha", 1) > 0 and not s.get("an")}
    cao = float(max(sp["V"][:, 1].max() for sn, sl in sk.atts.items() if sn in hien0 for sp in sl.values() if "V" in sp))
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao {cao:.0f}; slot di động: "
          + ", ".join(f"{SL[m]} {BAN[m]}" for m in DONG))
    return sk, dict(cao=cao)


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    out = []
    cao = info["cao"]

    # idle_01 của họ dài 6 s = chu kỳ 2,0 s lặp hai lần (khung 60, 120 gần trùng khung 0) + một đoạn biến tấu 4–6 s. Lấy chu kỳ 2,0 s,
    # 0,25 s cuối hoà về khung 0 cho khép vòng liền
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

    # ---- DIE: die_01 (nòng hất lên, giáp vỡ bắn mảnh, đổ sụp thành đống), giữ, mờ 0,32 s cuối
    D_DIE0 = CD["die_01"][0]
    D_DIE = D_DIE0 + 0.55

    def die(t, P):
        dat(P, mau("die_01", t))
        hien_theo_ho(sk, P, "die_01", t)
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.48, "vo", ""), (0.62, "tat_loi", ""), (0.86, "nga", "")]))

    # ---- ĐÁNH THƯỜNG: skill_01 (nâng nòng 0 → 0,33, bắn ~0,37, hạ nòng về). Của mình: nâng nòng, ngắm một nhịp, BẮN: nòng thụt mạnh
    # vào vỏ (bone97 lùi), nòng hất lên, thân lùi + nhún; đạn sắt do code bay từ `mieng` tới đối thủ
    U_ATK = [(0.0, 0.0), (0.34, 0.33), (0.46, 0.36), (1.15, 1.0)]
    D_ATK, T_BAN, T_TRUNG = 1.15, 0.44, 0.72

    def attack(t, P):
        u = tq(t, U_ATK)
        d_ = mau("skill_01", u)
        g = giat(t, T_BAN, 0.035, 0.22)
        cong(d_, "bone97", x=-75.0 * g)
        cong(d_, "bone30", rot=7.0 * g)
        cong(d_, "bone", x=-14.0 * g, y=-6.0 * g)
        dat(P, d_)
        hien_theo_ho(sk, P, "skill_01", u)
    out.append(Clip("attack", D_ATK, attack, ev=[(T_BAN, "ban", ""), (T_TRUNG, "trung", "")], trung=T_TRUNG))

    # ---- CHIÊU MANA: skill_03 (nòng chĩa trời 0 → 0,40 kèm cú thò nòng ra, giữ, hạ nòng 1,53 → 2,17). Của mình: nòng lên + nạp, rồi BẮN
    # LIỀN 5 QUẢ lên trời (mỗi quả một cú giật: nòng thụt, thân nhún), giữ một nhịp, hạ nòng; code cho mỗi quả vọt lên khỏi màn rồi tách
    # thành tên lửa nhỏ homing lao xuống đối thủ (quả đầu chạm ở `trung`)
    BAN_CAST = [0.62, 0.80, 0.98, 1.16, 1.34]
    U_CAST = [(0.0, 0.0), (0.42, 0.40), (0.55, 0.47), (1.55, 0.87), (2.25, 2.167)]
    D_CAST, T_TRUNG_C = 2.25, 2.00

    def cast(t, P):
        u = tq(t, U_CAST)
        if 1.55 < t:                                      # hạ nòng: lấy đoạn hạ của họ 1,60 → 2,17 (bỏ ba cú bơm nòng giữa clip)
            u = 1.60 + (t - 1.55) / (D_CAST - 1.55) * (2.167 - 1.60)
            d_ = mau("skill_03", u)
            if t < 1.70:
                d_ = pha_gan(mau("skill_03", 0.87), d_, em((t - 1.55) / 0.15))
        else:
            d_ = mau("skill_03", u)
        for tb in BAN_CAST:
            g = giat(t, tb, 0.03, 0.13)
            if g > 0:
                cong(d_, "bone97", x=-60.0 * g)
                cong(d_, "bone30", rot=-3.5 * g)
                cong(d_, "bone", y=-9.0 * g, x=-6.0 * g)
        dat(P, d_)
        hien_theo_ho(sk, P, "skill_03", u)
    out.append(Clip("cast", D_CAST, cast, ev=[(0.42, "nap", "")] + [(tb, "ban", str(i)) for i, tb in enumerate(BAN_CAST)]
                    + [(T_TRUNG_C, "trung", "")], trung=T_TRUNG_C))

    # ---- CHIÊU CUỐI: skill_04_1 kéo dài và dữ hơn. Thủ thế (0 → 0,27 của họ), nòng thò dài (0,27 → 0,73), GỒNG: giữ dáng nòng dài, thân
    # lún dần + rung tăng dần (cầu năng lượng lớn dần ở họng, VFX bám `mieng`), BẮN: nòng bật về (1,33 → 1,40 của họ) + cả con trượt lùi
    # (bone2 của họ) + nòng hất, khựng, rung tắt dần, giữ, trượt về (2,0 → 2,67 của họ)
    T_THU, T_DAI, T_GONG, T_DAY, T_BAN_S, T_GIU, D_SK = 0.32, 0.80, 0.85, 2.05, 2.25, 2.85, 3.55
    T_TRUNG_S = T_BAN_S + 0.22

    def skill(t, P):
        if t < T_THU:
            u = t / T_THU * 0.27
            d_ = mau("skill_04_1", u)
        elif t < T_DAI:
            u = 0.27 + (0.73 - 0.27) * em((t - T_THU) / (T_DAI - T_THU)) ** 0.9
            d_ = mau("skill_04_1", u)
        elif t < T_BAN_S:
            q = (t - T_DAI) / (T_BAN_S - T_DAI)
            u = 0.73 + (1.33 - 0.73) * q
            d_ = mau("skill_04_1", u)
            ga = em((t - T_GONG) / (T_DAY - T_GONG))                    # độ gồng 0 → 1
            run = ga * (0.6 + 0.4 * em((t - T_DAY) / 0.1))
            cong(d_, "bone", x=2.6 * run * math.sin(2 * math.pi * 23 * t), y=-10.0 * ga + 1.8 * run * math.sin(2 * math.pi * 31 * t + 1.3))
            cong(d_, "bone30", rot=0.9 * run * math.sin(2 * math.pi * 19 * t + 0.4))
            cong(d_, "bone97", x=22.0 * ga)                             # nòng vươn thêm khi tụ
        else:
            if t < T_BAN_S + 0.05:
                u = 1.33 + (1.40 - 1.33) * em((t - T_BAN_S) / 0.05)
            elif t < T_GIU:
                u = 1.40 + (2.0 - 1.40) * (t - T_BAN_S - 0.05) / (T_GIU - T_BAN_S - 0.05)
            else:
                u = 2.0 + (2.667 - 2.0) * em((t - T_GIU) / (D_SK - T_GIU))
            d_ = mau("skill_04_1", u)
            g = giat(t, T_BAN_S, 0.04, 0.45)
            cong(d_, "bone30", rot=9.0 * g)
            cong(d_, "bone", y=-12.0 * g)
            cong(d_, "bone2", x=tat_dan(t, T_BAN_S + 0.05, 0.035 * cao, 13.0, 0.14))
        dat(P, d_)
        hien_theo_ho(sk, P, "skill_04_1", u)
    out.append(Clip("skill", D_SK, skill, ev=[(T_GONG, "gong", ""), (T_DAY, "day", ""), (T_BAN_S, "ban", ""), (T_TRUNG_S, "trung", "")],
                    trung=T_TRUNG_S))

    # ---- APPEAR (Claude tự đặt: "thả quân" từ trên trời): khung đầu trống, rơi từ 0,8 chiều cao xuống, nòng chĩa trời (bone30 +44°), thân chúi
    # nhẹ; DỘNG đất (cham_dat): nhún sâu theo dáng thủ thế của skill_04_1, rung; đứng lên; nòng HẠ xuống, vượt quá dáng nghỉ rồi KHOÁ cạch
    # (khoa); nòng thụt thử một cái, họng xì khói (xa_khoi), lõi sáng (loi_sang); về khung 0 idle
    T_CHAM, T_DUNG, T_HA0, T_KHOA, T_XA, D_AP = 0.30, 0.62, 0.66, 0.98, 1.16, 1.75
    NONG = 44.0

    def appear(t, P):
        d0 = mau("idle_01", 0.0)
        dthu = mau("skill_04_1", 0.27)
        if t < T_CHAM:
            d_ = dict(d0)
            q = t / T_CHAM
            cong(d_, "move", y=0.8 * cao * (1 - q * q))
            cong(d_, "bone", rot=-4.0 * (1 - q))
            nong = NONG
        elif t < T_DUNG:
            q = (t - T_CHAM) / (T_DUNG - T_CHAM)
            w = em(q / 0.18) if q < 0.18 else 1.0 - em((q - 0.18) / 0.82)
            d_ = pha_gan(d0, dthu, w)
            cong(d_, "bone", y=-26.0 * w)
            cong(d_, "move", x=tat_dan(t, T_CHAM, 0.02 * cao, 15.0, 0.08))
            nong = NONG - 6.0 * w
        else:
            d_ = dict(d0)
            if t < T_KHOA:
                q = (t - T_HA0) / (T_KHOA - T_HA0)
                nong = NONG * (1 - em(q) ** 1.4) - 7.0 * math.sin(math.pi * min(1.0, max(0.0, (q - 0.7) / 0.3))) if t > T_HA0 else NONG - 3.0
            else:
                nong = tat_dan(t, T_KHOA, 3.0, 6.0, 0.10)
            g = giat(t, T_XA, 0.03, 0.18)
            cong(d_, "bone97", x=-45.0 * g)
            cong(d_, "bone", y=-5.0 * g - 4.0 * giat(t, T_KHOA, 0.03, 0.12))
        cong(d_, "bone30", rot=nong)
        dat(P, d_)
        hien_theo_ho(sk, P, "idle_01", 0.0)
        a_ = min(1.0, t / 0.08)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(T_CHAM, "cham_dat", ""), (T_KHOA, "khoa", ""), (T_XA, "xa_khoi", ""),
                                               (T_XA + 0.08, "loi_sang", "")]))
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
    if a and a[0] == "bo_cuc":
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
    xuat.xuat_het(sk, clips, RA, TEN, ("Thú giáp pháo non dạng 1 (thu_phao_non)" if NON else "Thú giáp pháo (thu_phao)") + ": tướng 9 đảo Kim"
                  + (" — DA GỐC, chỉ để soi clip" if GOC else "") + (" — DA TẠM DẠNG 2" if NON and not DA_NON else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=("attack", "cast", "skill"), lao=(), far=(), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.08, "translate": 0.2, "scale": 0.002}, khop_idle=0.2, span=SPAN,
                  impact={"attack": (0.06, 0.3, 0.08), "cast": (0.06, 0.35, 0.08), "skill": (0.28, 1.3, 0.25, "#9fe8ff38")})


if __name__ == "__main__":
    main(sys.argv[1:])
