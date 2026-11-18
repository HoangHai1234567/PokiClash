# -*- coding: utf-8 -*-
"""Sói giáp sắt (soi_giap, tướng 6 đảo Kim): RESKIN trên rig con gốc monster_3428 (sói to cơ bắp, khiên lớn, búa).

- Xương: đủ mọi xương của họ + `move`; dáng gốc = khung 0 idle_01 (biến đổi riêng `l` đã áp ràng buộc, lấy mẫu bằng runtime Spine thật).
- Hình: mảnh lông / dây / mặt của mình vẽ trên đúng khung ảnh vùng của họ, NGUYÊN lưới của họ (soi_giap_manh.py). Mảnh ĐỔI DÁNG (mũ, tấm
  gáy, giáp vai ba gai, búa, khiên, hai tai dựng) là mảnh cứng một xương, đặt theo concept B (khop_concept: concept → thế giới khung 0
  idle) + CHINH. Khiên nhìn thẳng W_dunpai2 = khiên của mình lật ngang (con gốc cũng vậy); búa bay W_futou2 (die) = búa của mình.
  Bỏ (ẩn): mảnh đỉnh mũ P_toushi2, vành tấm gáy P_toushi4, gai nhỏ giáp vai P_jianjiaR03, lớp sau mặt dây P_diaozhui1b, bùa P_diaozhui2.
- Thứ tự vẽ: của họ (không clip nào đổi thứ tự).
- Clip: idle (idle_01), walk (run_01), hit (hit_01), die (die_01 + mờ dần) = của họ.
  appear: khiên nằm đất trước mặt (skill_02 đoạn khiên úp) → nhấc khiên lên (skill_02 phần sau) → ngẩng đầu GẦM (mặt há `mat_ha`).
  attack: lấy đà vung búa qua người lên cao (skill_01 0–0,30 s) + LAO tới (xương move, game nắn quãng: lunge) → quật búa xuống trước mặt.
  cast: ném búa: vung búa qua người (skill_01), búa rời tay ở đỉnh vung, `bua_bay` (xương ten_0 con của fly_0) xoay tròn bay tới `far`,
  trúng, bay về tay (game co quãng theo far).
  skill: vào thế che khiên (skill_05), giữ gồng (skill_03), LAO xé gió tới đối thủ (move, khai lunge), HÚC (khiên xoay mặt ra trước như
  hit_03), bật lại, đứng dậy (skill_04). VFX gió / nổ do code ở các sự kiện.

    soi_giap_rig.py                              dựng, xuất inbox/soi_giap_1/rig/
    soi_giap_rig.py soi <clip> <giây,..> [tỉ lệ]  khung lớn nền xám → rig/soi_<clip>.png
    soi_giap_rig.py kiem                         bước xoay lớn nhất giữa hai khung của từng clip
    SG_GOC=1 soi_giap_rig.py ...                 dựng bằng DA GỐC (manh_goc/) ra rig_goc/: chỉ để soi clip trong máy
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
import soi_giap as G  # noqa: E402
import soi_giap_don as DON  # noqa: E402

GOC = os.environ.get("SG_GOC") == "1"
# SG_DANG=non: DẠNG 1 (sói con chibi): cùng xương, lưới, clip; đổi tỉ lệ xương (TI_LE: đầu to, khiên, búa, giáp vai nhỏ), bỏ tấm gáy; mảnh tìm ở
# inbox/soi_giap_non/manh trước, thiếu thì lấy mảnh dạng 2 (inbox/soi_giap_1/manh).
NON = os.environ.get("SG_DANG") == "non" and not GOC
BASE = os.path.join(HERE, "inbox", "soi_giap_non") if NON else G.BASE
MANH2 = os.path.join(G.BASE, "manh")
TEN = "soi_giap_non" if NON else "soi_giap"
RA = os.environ.get("SG_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("SG_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
# tỉ lệ RIÊNG từng xương (con thừa hưởng): thân trên P_shenti2 0,85 (ngực, tay, đầu theo), đầu P_tou2 bù lên 1,45 / 0,85; chân P_tui*1 0,82 (hông
# hạ xuống cho bàn chân chạm đất: HA_HONG tự tính); khiên, búa, giáp vai nhỏ lại; bờm co.
TI_LE = {"P_shenti2": 0.85, "P_tou2": 1.45 / 0.85, "P_jianjiaR02": 0.72, "W_dunpai3": 0.95, "W_futou": 1.0, "W_futou2": 0.75,
         "P_shouR1": 0.88, "P_shouL1": 0.90, "P_shenti4": 0.62, "P_shenti6": 0.62, "P_tuiL1": 0.82, "P_tuiR1": 0.82} if NON else {}
RES = 2
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
DAU_NON = NON and os.path.exists(os.path.join(MANH, "dau.png"))     # dạng non có đầu mắt to riêng (gen từ concept): thay mặt + mắt rời của dạng 2
AN_HAN = () if GOC else ("P_toushi2", "P_toushi4", "P_jianjiaR03", "P_diaozhui1b", "P_diaozhui2") + (("P_toushi3",) if NON else ()) +     (("P_yanjin1", "P_yanjin2", "P_diaozhui1") if DAU_NON else ())
# mảnh đổi dáng: slot của họ → (ảnh của mình, xương bám)
THAY = {"P_toushi1": ("mu", "P_tou2"), "P_toushi3": ("gay", "P_toushi3"), "P_jianjiaR01": ("vai", "P_jianjiaR02"),
        "W_futou": ("bua", "W_futou"), "W_dunpai1": ("khien", "W_dunpai3"), "P_erduoR": ("tai_gan", "P_erduoR"),
        "P_erduoL": ("tai_xa", "P_erduoL")}
# chỉnh tay (đơn vị rig, thế giới khung 0 idle): dời / phóng từng mảnh đổi dáng sau khi đặt theo concept (soi chồng concept rồi sửa)
CHINH = {}


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung, đã áp ràng buộc)
def _cd():
    out = {}
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
        hien = [[(F["n"][k] is not None) * float(F["a"][k]) for k in range(len(SL))] for F in fr]
        out[clip] = (float(v["dur"]), res, hien)
    return out


CD = _cd()


def mau(clip, t, lap=False):
    dur, R, _ = CD[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    out = {}
    for b, arr in R.items():
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        out[b] = arr[i0] * (1 - w) + arr[i1] * w
    return out


# đoạn clip của họ có IK đổi nhánh (góc xương nhảy 100–180° trong một khung; runtime của họ giải IK mỗi khung nên mượt, rig FK nướng
# của mình nội suy ở 60 khung / giây sẽ lộ dáng lạ): bỏ qua các khung đó, pha mượt dáng hai đầu đoạn.
NHANH = {"skill_05": [(0.0, 0.27)], "skill_04": [(0.06, 0.27)], "die_01": [(0.38, 0.60)]}


def mau_muot(clip, t, lap=False):
    for a_, b_ in NHANH.get(clip, ()):
        if a_ < t < b_:
            return pha(mau(clip, a_), mau(clip, b_), em((t - a_) / (b_ - a_)))
    return mau(clip, t, lap)


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


NHAM_NON = DAU_NON and os.path.exists(os.path.join(MANH, "dau_nham.png"))   # dạng non: đầu nhắm mắt thay mắt nhắm rời của họ
I_NHAM = SL.index("P_yanjin2")


def hien_theo_ho(P, clip, t, lap=False):
    """độ đậm mọi slot theo khung của họ (đổi hình mắt, búa bay, khiên hai mặt); slot đã bỏ luôn tắt."""
    i = khung_ho(clip, t, lap)
    hien = CD[clip][2]
    if NHAM_NON:                                       # họ bật mắt nhắm → đầu nhắm mắt của mình thay đầu thường
        nh = hien[i][I_NHAM] > 0.5
        P.alpha["mat_nham"] = 1.0 if nh else 0.0
        P.alpha["P_tou1"] = 0.0 if nh else 1.0
    for k, sl in enumerate(SL):
        if sl == "shadow" or sl in AN_HAN or (NHAM_NON and sl == "P_tou1"):   # slot đã bỏ: không có trong rig
            continue
        P.alpha[sl] = 1.0 if hien[i][k] > 0.5 else 0.0


# ---------------------------------------------------------------- dựng
def manh_goc():
    """da gốc (chỉ để soi clip): mỗi vùng ảnh cắt theo lưới, phóng RES (cả hình ẩn ở idle)."""
    import soi_giap_manh as SM
    os.makedirs(MANH, exist_ok=True)
    for r, (a, im) in SM.goc_tat_ca().items():
        p = os.path.join(MANH, r + ".png")
        if not os.path.exists(p):
            im.resize((im.width * RES, im.height * RES), Image.LANCZOS).save(p)


def aff(a, imgs_ho):
    """phép affine: px ảnh vùng của part (họ) → toạ độ RIÊNG của xương nó bám (dáng gốc). Chỉ đúng cho part một xương."""
    uv_px, _ = G.luoi(a)
    xy = np.array(a["xy"], float).reshape(-1, 2)
    bn = a["bone"] if not a.get("w") else NB[a["w"][0][0][0]]
    loc = np.array([np.linalg.solve(WG[bn], np.array([p[0], p[1], 1.0]))[:2] for p in xy])
    M, *_ = np.linalg.lstsq(np.c_[uv_px, np.ones(len(uv_px))], loc, rcond=None)
    return M, bn


def dung():
    if GOC:
        manh_goc()
    def xuong_het(ten, ti, ha):
        k = Sk(ten)
        k.xuong("root")
        k.xuong("move", "root")
        for i, b in enumerate(I["bones"]):
            if b["name"] == "root":
                continue
            cha = NB[b["parent"]]
            z = L0[i]
            k_ = ti.get(b["name"], 1.0)
            k.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1] - (ha if b["name"] == "bone2" else 0.0), goc=z[2], dai=b["len"],
                    sx=z[3] * k_, sy=z[4] * k_)
        return k
    sk0 = xuong_het("_goc", {}, 0.0)                                   # dáng gốc CHƯA đổi tỉ lệ: điểm gắn mảnh cứng tính theo nó (mảnh co theo xương)
    Wi0 = sk0.the_gioi()
    ha = 0.0
    if TI_LE:                                                          # hạ hông cho bàn chân (đã ngắn) chạm đất như dáng gốc
        W1 = xuong_het("_thu", TI_LE, 0.0).the_gioi()
        ha = float(np.mean([W1[b][1, 2] - Wi0[b][1, 2] for b in ("P_tuiL4", "P_tuiR4")]))
    sk = xuong_het(TEN, TI_LE, ha)
    Wi = sk.the_gioi()
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hien0 = {SL[k]: v > 0.5 for k, v in enumerate(CD["idle_01"][2][0])}
    by = {a["slot"]: a for a in AG["atts"]}
    IM = {}

    def anh_cua(r, lat=False):
        key = r + ("_lat" if lat else "")
        if key not in IM:
            pth = os.path.join(MANH, r + ".png")
            if NON and not os.path.exists(pth):                        # dạng non chưa có mảnh này: tạm mảnh dạng 2
                pth = os.path.join(MANH2, r + ".png")
            g = Image.open(pth).convert("RGBA")
            if lat:
                g = g.transpose(Image.FLIP_LEFT_RIGHT)
            IM[key] = anh.loang_mau(g)
            sk.anh(key, IM[key])
        return key, IM[key]

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

    def gan(slot_ten, a, an):
        r = a["region"]
        key, im = anh_cua(r)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        sk.slot(slot_ten, rows[0][0][0], key, an=an)
        sk.atts[slot_ten][key] = {"type": "mesh", "path": key, "uv": uv, "tris": np.asarray(tris, int).reshape(-1, 3), "hull": len(uv),
                                  "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, key)] = Luoi(uv * np.array([im.width, im.height], float), np.asarray(tris, int).reshape(-1, 3), len(uv), len(uv),
                                        im.width, im.height, ten=slot_ten)
        return V0

    def gan_cung(slot_ten, ten_anh, bone, Vw, an, lat=False, the_gioi=True, goc=True):
        """mảnh cứng: ô 4 đỉnh bám trọn một xương. Vw: 4 góc (TL, TR, BR, BL của ảnh) ở thế giới khung 0 idle (the_gioi) hoặc toạ độ
        riêng của xương."""
        key, im = anh_cua(ten_anh, lat)
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        if the_gioi:
            loc = [np.linalg.solve((Wi0 if goc else Wi)[bone], np.array([v[0], v[1], 1.0]))[:2] for v in Vw]
        else:
            loc = [np.asarray(v, float) for v in Vw]
        V0 = np.array([(Wi[bone] @ np.array([l_[0], l_[1], 1.0]))[:2] for l_ in loc])
        rows = [[(bone, float(l_[0]), float(l_[1]), 1.0)] for l_ in loc]
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.slot(slot_ten, bone, key, an=an)
        sk.atts[slot_ten][key] = {"type": "mesh", "path": key, "uv": uv, "tris": tris, "hull": 4, "V": V0, "verts": rows,
                                  "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, key)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)
        return V0

    # ---- mảnh đổi dáng: khung trên concept → thế giới khung 0 idle
    MOI = {}
    THAY_ = THAY
    if not GOC:
        import soi_giap_manh as SM
        nguon = [(os.path.join(MANH2, "moi.json"), os.path.join(G.MAU, "khop_concept.json"))]
        if NON and os.path.exists(os.path.join(MANH, "moi.json")):        # mảnh đổi dáng của dạng non: khung trên concept non + phép khớp riêng
            nguon.append((os.path.join(MANH, "moi.json"), os.path.join(BASE, "mau", "khop_concept.json")))
        hop_moi = {}
        for j, (pm, pk) in enumerate(nguon):
            kc = json.load(open(pk))
            for ten, d_ in json.load(open(pm)).items():
                hop_moi[ten] = (d_["hop"], kc, j == 0)
        Q2 = {}
        for ten, (hp, kc, la2) in hop_moi.items():
            x_, y_, w_, h_ = hp
            goc_px = np.array([[x_, y_], [x_ + w_, y_], [x_ + w_, y_ + h_], [x_, y_ + h_]], float)
            dv = kc.get("doi", {}).get(ten) if not la2 else None
            if isinstance(dv, (list, tuple)):
                goc_px = goc_px + np.array(dv, float)
            Q = SM.concept_ra_the_gioi(goc_px, kc)
            c_ = CHINH.get(ten, {})
            if "k" in c_:
                Q = Q.mean(0) + (Q - Q.mean(0)) * c_["k"]
            if "d" in c_:
                Q = Q + np.array(c_["d"], float)
            MOI[ten] = (Q, la2)                                        # la2: toạ độ dáng gốc (mảnh dạng 2) hay dáng non (đã đổi tỉ lệ)
            if dv == "neo2":                                           # đặt tâm vào tâm mảnh cùng tên của dạng 2 (đổi sang dáng non qua xương bám)
                Q2[ten] = Q
        if Q2:
            kc2 = json.load(open(nguon[0][1]))
            for ten, Q in Q2.items():
                hp = json.load(open(nguon[0][0]))[ten]["hop"]
                x_, y_, w_, h_ = hp
                c2 = SM.concept_ra_the_gioi(np.array([[x_ + w_ / 2, y_ + h_ / 2]], float), kc2)[0]
                xb = [v[1] for k_, v in THAY.items() if v[0] == ten][0]
                c2n = (Wi[xb] @ np.linalg.solve(Wi0[xb], np.array([c2[0], c2[1], 1.0])))[:2]
                MOI[ten] = (Q - Q.mean(0) + c2n, False)
        if NON and "dau" in MOI:
            # dạng non: đầu mắt to thay mặt; tai gần vẽ TRƯỚC mũ (vành mũ che gốc tai như concept): slot mũ mang tai gần, slot tai gần mang mũ
            THAY_ = dict(THAY, P_tou1=("dau", "P_tou2"), P_toushi1=("tai_gan", "P_erduoR"), P_erduoR=("mu", "P_tou2"))
        else:
            THAY_ = THAY

    def copy_quad(Q, a1, a2, lat=False, goc=True):
        """4 góc (thế giới, xương của a1) → 4 góc trong toạ độ riêng xương của a2 qua px ảnh vùng (a2 có thể là bản lật ngang của a1)."""
        M1, b1 = aff(a1, imgs_ho)
        M2, b2 = aff(a2, imgs_ho)
        loc1 = np.array([np.linalg.solve((Wi0 if goc else Wi)[b1], np.array([v[0], v[1], 1.0]))[:2] for v in Q])
        A = np.c_[M1[:2].T, M1[2]]                                     # loc = A·[px, 1]
        px = np.linalg.solve(A[:, :2], (loc1 - A[:, 2]).T).T
        if lat:
            wr = imgs_ho[a2["region"]].size[0]
            px = np.array([[wr - p[0], p[1]] for p in px])
            px = px[[1, 0, 3, 2]]                                      # góc TL của ảnh lật = góc TR của ảnh thường
        return [np.array([*p, 1.0]) @ M2 for p in px], b2

    for a in sorted(AG["atts"], key=lambda q: q["order"]):
        s = a["slot"]
        if s in AN_HAN:                                                # mảnh của họ không có trong thiết kế: bỏ
            continue
        an = not hien0.get(s, False)
        if MOI and s in THAY_ and THAY_[s][0] in MOI:
            ten_a, xb = THAY_[s]
            gan_cung(s, ten_a, xb, MOI[ten_a][0], an=an, goc=MOI[ten_a][1])
        elif MOI and s == "W_futou2":                                  # búa bay của die: bản sao búa của mình trên xương W_futou2
            Lq, b2 = copy_quad(MOI["bua"][0], by["W_futou"], a, goc=MOI["bua"][1])
            gan_cung(s, "bua", b2, Lq, an=True, the_gioi=False)
        elif MOI and s == "W_dunpai2":                                 # khiên nhìn thẳng = khiên của mình lật ngang
            Lq, b2 = copy_quad(MOI["khien"][0], by["W_dunpai1"], a, lat=True, goc=MOI["khien"][1])
            gan_cung(s, "khien", b2, Lq, an=True, lat=True, the_gioi=False)
        else:
            gan(s, a, an=an)
        if s == "P_tou1" and NON and "dau" in MOI:                     # dạng non: đầu nhắm mắt + đầu há gầm, ô cứng trên xương đầu, khớp đầu thường
            Qd = MOI["dau"][0]
            for ten_b, slot_b in (("dau_nham", "mat_nham"), ("dau_ha", "mat_ha")):
                pj = os.path.join(MANH, ten_b + ".json")
                if not os.path.exists(pj):
                    continue
                J = json.load(open(pj))
                u_, v_ = (Qd[1] - Qd[0]) / J["w0"], (Qd[3] - Qd[0]) / J["h0"]
                tl = Qd[0] + J["dx"] * u_ + J["dy"] * v_
                Qb = np.array([tl, tl + J["w"] * u_, tl + J["w"] * u_ + J["h"] * v_, tl + J["h"] * v_])
                gan_cung(slot_b, ten_b, "P_tou2", Qb, an=True, goc=False)
        if s == "P_tou1":                                              # mặt há gầm (appear): ô cứng trên xương đầu, phần trên trùng mặt
            if MOI and not NON and os.path.exists(os.path.join(MANH, "mat_ha.png")):
                o = json.load(open(os.path.join(G.MAU, "goc_A.json"), encoding="utf-8"))
                h0, hc = o["MAT_HA"]["hop"], o["MAT_HA"].get("hop_cat", o["MAT_HA"]["hop"])
                z = o["MAT_HA"]["z"]
                mh = Image.open(os.path.join(MANH, "mat_ha.png"))
                off = np.array([(hc[0] - h0[0]) / z, (hc[1] - h0[1]) / z])
                corner = [np.array([0, 0]), np.array([mh.width, 0]), np.array([mh.width, mh.height]), np.array([0, mh.height])]
                Mf, bf = aff(a, imgs_ho)
                Lq = [np.array([*(c_ / RES + off), 1.0]) @ Mf for c_ in corner]
                gan_cung("mat_ha", "mat_ha", bf, Lq, an=True, the_gioi=False)

    # ---- xương phụ cho VFX và vật bay
    def tam_anh(slot_ten):
        sp = list(sk.atts[slot_ten].values())[0]
        return sp["V"].mean(0)
    Vb = list(sk.atts["W_futou"].values())[0]["V"]
    cao = float(max(list(sk.atts[nm].values())[0]["V"][:, 1].max() for nm in sk.atts
                    if nm in hien0 and hien0[nm] and nm not in AN_HAN and sk.atts[nm]))
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    sk.xuong("fly_0", "root", 0.0, 0.0)
    sk.xuong("ten_0", "fly_0", 0.0, 0.0)
    # đầu búa: phần ảnh búa xa nắm tay nhất (tâm đầu búa) → xương `dau_bua` con của W_futou
    tay = Wi["P_shouR31"][:2, 2]
    dmax = np.argmax(np.hypot(*(Vb - tay).T))
    Vc = Vb.mean(0) + 0.45 * (Vb[dmax] - Vb.mean(0))
    lb = np.linalg.solve(Wi["W_futou"], np.array([*Vc, 1.0]))[:2]
    sk.xuong("dau_bua", "W_futou", float(lb[0]), float(lb[1]))
    tk_ = tam_anh("W_dunpai1")
    lk = np.linalg.solve(Wi["W_dunpai3"], np.array([*tk_, 1.0]))[:2]
    sk.xuong("tam_khien", "W_dunpai3", float(lk[0]), float(lk[1]))
    mui = Wi["P_tou2"]
    # búa bay (cast): ảnh búa, tâm quay = tâm đầu búa
    key, imb = anh_cua("bua" if MOI else "W_futou")
    Vq = Vb                                                            # 4 góc ảnh búa ở dáng gốc (đã theo tỉ lệ xương)
    if not MOI:                                                        # da gốc: lấy 4 góc ảnh vùng của họ
        Mf, bf = aff(by["W_futou"], imgs_ho)
        wr, hr = imgs_ho["W_futou"].size
        Vq = np.array([(Wi[bf] @ np.array([*(np.array([x_, y_, 1.0]) @ Mf), 1.0]))[:2] for x_, y_ in ((0, 0), (wr, 0), (wr, hr), (0, hr))])
    Vf = Vq - Vc
    sk.slot("bua_bay", "ten_0", key, an=True)
    sk.atts["bua_bay"][key] = {"type": "mesh", "path": key, "uv": np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float),
                               "tris": np.array([[0, 1, 2], [0, 2, 3]]), "hull": 4, "V": Vf,
                               "verts": [[("ten_0", float(v[0]), float(v[1]), 1.0)] for v in Vf], "width": imb.width, "height": imb.height}
    for e, m in (("vung", "vung búa"), ("trung", "khung trúng"), ("nem", "búa rời tay (ném)"), ("bat_bua", "búa bay về tới tay"),
                 ("che_khien", "vào thế che khiên"), ("tu_luc", "gồng tụ lực sau khiên (VFX gió hút)"), ("lao", "lao xé gió (VFX vệt gió)"),
                 ("huc", "khiên húc trúng"), ("nhat_khien", "nhấc khiên lên"), ("gam", "gầm (VFX sóng âm)"), ("nga", "ngã gục")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(cao=cao, Vc=Vc)


# ---------------------------------------------------------------- clip
def bay(sk, P, A, q, quay=0.0, lech=(0.0, 0.0)):
    """búa bay ở quãng q (0..1) từ điểm A (thế giới) tới far + lech; quay: góc xoay tròn (độ)."""
    far = sk.W0["far"][:2, 2]
    d = far + np.array(lech) - A
    an = not (0.0 <= q <= 1.0)
    q = min(max(q, 0.0), 1.0)
    Pd = A + q * d + np.array([0.0, 1.0]) * 40.0 * math.sin(math.pi * q)
    fly = q * far
    P.move("fly_0", float(fly[0]), float(fly[1]))
    P.move("ten_0", float(Pd[0] - fly[0]), float(Pd[1] - fly[1]))
    P.rot("ten_0", quay)
    P.alpha["bua_bay"] = 0.0 if an else 1.0


def lam_clip(sk, info):
    out = []
    cao = info["cao"]

    D_ID = CD["idle_01"][0]

    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        hien_theo_ho(P, "idle_01", t, True)
    out.append(Clip("idle", D_ID, idle, loop=True))

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        hien_theo_ho(P, "run_01", t, True)
    out.append(Clip("walk", CD["run_01"][0], walk, loop=True))

    def hit(t, P):
        dat(P, mau("hit_01", t))
        hien_theo_ho(P, "hit_01", t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ================= BA CLIP TẤN CÔNG (làm lại 2026-11-16 sau khi người dùng chê "còn yếu và hơi xấu"): dáng khoá đặt bằng soi_giap_don.Bo
    # (chân IK bám đất, tay búa theo đích, lớp phụ trễ). Nhịp theo animation-petclash mục 2: lấy đà NGƯỢC chiều cú đánh, ra đòn 2 khung, quá đà,
    # giữ có trôi, về. Góc tay búa (ta) và góc búa (ba) ghi LIỀN vòng (âm dần = quay theo chiều kim đồng hồ: sau → trên → trước).
    B = DON.Bo(sk)
    KB = info["cao"] / 640.68 if NON else 1.0                 # dạng non nhỏ hơn: độ dời tuyệt đối trong dáng khoá co theo chiều cao
    DOI_K = ("hx", "hy", "my", "fRx", "fRy", "fLx", "fLy", "kx", "ky")

    def co_khoa(keys):
        if KB == 1.0:
            return keys
        return [(t_, {k: (v * KB if k in DOI_K and isinstance(v, (int, float)) else v) for k, v in q.items()}, e) for t_, q, e in keys]
    N = B.nghi()
    TA, TK, BA = N["ta"], N["tk"], N["ba"]

    def nhip(t, t0, dai):
        """bướu 0 → 1 → 0 trong [t0, t0 + dai]."""
        return math.sin(math.pi * min(1.0, max(0.0, (t - t0) / dai)))

    # ---- ĐÁNH THƯỜNG: nhún kéo búa ra sau → bật nhảy tới, búa vung vòng qua đầu → NỆN búa xuống trước mặt (chạm đất cùng lúc đáp) →
    # lún quá đà, búa nảy → kéo búa về.
    LAO = 0.5 * cao
    T_TR = 14 / FPS
    ATK = [
        (0.00, N, "em"),
        (0.17, dict(hx=-26, hy=-34, hr=8, nr=7, dr=-12, ta=TA - 30, tk=0.97, ba=BA - 64, kx=-12, ky=-14, kw=3), "out"),
        (0.33, dict(mx=0.55 * LAO, my=74, hx=4, hy=16, hr=9, nr=15, dr=-20, vr=8, ta=TA - 140, tk=0.93, ba=BA - 160, kx=4, ky=14, kw=9,
                    fRy=22, fLy=34, fRr=-28, fLr=-22, fRx=-10, fLx=10), "em"),
        (0.40, dict(mx=0.78 * LAO, my=80, nr=18, ta=TA - 150, ba=BA - 168, fRy=30, fLy=26, ky=20, kw=11), "lin"),
        (T_TR, dict(mx=LAO, my=0, hx=44, hy=-44, hr=-21, nr=-23, dr=34, vr=18, ta=TA - 274, tk=1.0, ba=BA - 368, kx=-62, ky=24, kw=-6,
                    fRy=0, fLy=0, fRr=0, fLr=0, fRx=-18, fLx=34), "in"),
        (T_TR + 0.05, dict(hy=-54, hr=-25, nr=-27, dr=40, ba=BA - 376, ky=16, kw=-9), "out"),
        (T_TR + 0.15, dict(hy=-44, hr=-21, nr=-22, dr=32, ba=BA - 364, ky=22, kw=-6), "em"),
        (T_TR + 0.24, dict(hy=-42, ba=BA - 366), "lin"),
        (0.92, dict(mx=0.30 * LAO, hx=6, hy=-14, hr=-5, nr=-4, dr=4, vr=0, ta=TA - 330, tk=0.95, ba=BA - 372, kx=-16, ky=6, kw=-2,
                    fRx=-6, fLx=10), "em"),
        (1.15, dict(N, ta=TA - 360, ba=BA - 360), "em"),
    ]
    ATK = co_khoa(ATK)
    D_ATK = ATK[-1][0]

    def attack(t, P):
        q = dict(DON.noi(ATK, t))
        q["bs"] = 1.0 + 0.30 * nhip(t, 0.40, T_TR - 0.40 + 0.02)              # búa giãn dọc trục lúc nện (smear)
        B.dat(P, q)
        hien_theo_ho(P, "idle_01", 0.0)
        if t > T_TR:                                                           # rung tay lúc búa nện đất, tắt dần
            k = max(0.0, 1 - (t - T_TR) / 0.22)
            P.rot("P_shouR2", 2.5 * k * math.sin(2 * math.pi * 16 * (t - T_TR)))
            P.move("bone2", 0.0, -3.0 * k * abs(math.sin(2 * math.pi * 12 * (t - T_TR))))
    out.append(Clip("attack", D_ATK, attack, ev=[(0.17, "vung", ""), (T_TR, "trung", "")], trung=T_TR))

    # ---- CHIÊU MANA: NÉM BÚA. Xoay người kéo búa ra sau vai (nhấc chân trước) → bước tới quăng cả người, búa rời tay ở đỉnh vung → tay
    # theo đà xuống thấp, giữ → búa xoay tròn bay tới đối thủ (code co quãng) rồi bay về → giơ tay bắt, bị búa kéo giật ra sau → hạ búa.
    T_NEM, BAY_DI, GIU, BAY_VE = 15 / FPS, 0.20, 0.08, 0.34
    T_VE = T_NEM + BAY_DI + GIU
    T_BAT = T_VE + BAY_VE
    CAS = [
        (0.00, N, "em"),
        (0.24, dict(hx=-30, hy=-20, hr=10, nr=15, dr=-18, vr=10, ta=TA - 100, tk=0.95, ba=BA - 150, kx=26, ky=22, kw=-7,
                    fLy=24, fLx=-14, fLr=-18), "out"),
        (0.40, dict(hx=-36, nr=19, ta=TA - 106, ba=BA - 157, fLy=30, ky=28), "lin"),
        (T_NEM, dict(hx=42, hy=-26, hr=-17, nr=-21, dr=26, vr=6, ta=TA - 212, tk=1.0, ba=BA - 300, kx=-50, ky=14, kw=5,
                     fLy=0, fLx=48, fLr=0), "in"),
        (T_NEM + 0.08, dict(hx=52, hy=-34, hr=-22, nr=-24, dr=40, vr=16, ta=TA - 290, tk=0.93, ba=BA - 370, kx=-62, ky=8, kw=8), "out"),
        (T_VE, dict(hx=46, hy=-28, hr=-19, nr=-20, dr=34, ta=TA - 282, kx=-56, ky=12, kw=6), "em"),
        (T_BAT - 0.06, dict(hx=22, hy=-10, hr=-5, nr=-3, dr=6, vr=4, ta=TA - 196, tk=0.90, ba=BA - 240, kx=-20, ky=8, kw=2), "em"),
        (T_BAT, dict(ta=TA - 198, tk=0.86), "lin"),
        (T_BAT + 0.10, dict(hx=-16, hy=-16, hr=9, nr=10, dr=-12, ta=TA - 128, tk=0.80, ba=BA - 178, kx=10, ky=-6, kw=-3, fLx=30), "out"),
        (T_BAT + 0.30, dict(hx=-6, hy=-6, hr=3, nr=3, dr=-3, vr=0, ta=TA - 40, tk=0.95, ba=BA - 60, kx=2, ky=-2, kw=0, fLx=12), "em"),
        (T_BAT + 0.56, N, "em"),
    ]
    CAS = co_khoa(CAS)
    D_CAST = CAS[-1][0]
    G0_BUA = math.degrees(math.atan2(sk.W0["W_futou"][1, 0], sk.W0["W_futou"][0, 0]))

    def bua_tg(t):
        """(tâm đầu búa, góc búa so với dáng nghỉ) của búa TRONG TAY ở giây t của cast."""
        P0 = Pose()
        B.dat(P0, DON.noi(CAS, t))
        W = sk.the_gioi(P0)
        return W["dau_bua"][:2, 2].copy(), math.degrees(math.atan2(W["W_futou"][1, 0], W["W_futou"][0, 0])) - G0_BUA

    A_N, g_n = bua_tg(T_NEM)
    A_B, g_b = bua_tg(T_BAT)
    g_b -= 360.0 * round((g_b - (g_n - 1080.0)) / 360.0)                        # về tay sau ~3 vòng, khớp góc búa trong tay

    def cast(t, P):
        B.dat(P, DON.noi(CAS, t))
        hien_theo_ho(P, "idle_01", 0.0)
        if t < T_NEM:
            P.rot("ten_0", g_n)
        elif t >= T_BAT:
            P.rot("ten_0", g_b)
            k = max(0.0, 1 - (t - T_BAT) / 0.2)                                 # búa đập vào tay: rung
            P.rot("P_shouR2", 3.0 * k * math.sin(2 * math.pi * 15 * (t - T_BAT)))
        else:
            P.alpha["W_futou"] = 0.0
            if t < T_NEM + BAY_DI:
                q = (t - T_NEM) / BAY_DI
                bay(sk, P, A_N, q, quay=g_n - 500.0 * q)
            elif t < T_VE:
                bay(sk, P, A_N, 1.0, quay=g_n - 500.0 - 60.0 * (t - T_NEM - BAY_DI) / GIU)
            else:
                q = (t - T_VE) / BAY_VE
                bay(sk, P, A_B, 1.0 - q * q * (3 - 2 * q), quay=g_n - 560.0 + (g_b - g_n + 560.0) * q)
    out.append(Clip("cast", D_CAST, cast, ev=[(0.24, "vung", ""), (T_NEM, "nem", ""), (T_NEM + BAY_DI, "trung", ""), (T_BAT, "bat_bua", "")],
                    trung=T_NEM + BAY_DI))

    # ---- CHIÊU CUỐI: vào thế che khiên (skill_05 → skill_03) → gồng, CÀO CHÂN xuống đất hai lần như bò tót → rút người ra sau, khiên
    # dựng lên trước mặt (dáng hit_03 của họ: khiên xoay mặt ra trước) → LAO xé gió (nhanh dần, chân chạy, người chúi, cả con giãn dài) →
    # HÚC: khựng, khiên thúc tới, cả con nén lại rồi dội trượt lùi → giữ, khiên rung → hạ khiên về thế che, đứng dậy (skill_04), lùi về chỗ.
    C1, CP, C2, C3 = 0.45, 0.93, 33 / FPS, 40 / FPS
    C4, C5 = C3 + 0.40, C3 + 0.56
    D_SK = C5 + 0.85
    LAO_SK = 1.2 * cao
    CHAN = [b for b in NB if b.startswith("P_tui")]
    SKL = [
        (0.00, {}, "em"),
        (CP, dict(hy=-6), "em"),
        (C2, dict(mx=-0.10 * cao, hx=-36, hy=-26, hr=9, nr=6), "out"),                             # rút ra sau lấy đà
        (C3, dict(mx=LAO_SK, hx=22, hy=-8, hr=-16, nr=-6), "in3"),                                  # lao
        (C3 + 0.04, dict(hx=52, hy=-16, hr=-23, nr=-10), "lin"),                                    # húc: người dồn vào khiên
        (C3 + 0.17, dict(mx=0.90 * LAO_SK, hx=-8, hy=0, hr=5, nr=4), "out"),                        # dội, trượt lùi
        (C4, dict(mx=0.89 * LAO_SK, hx=0, hy=-4, hr=0, nr=0), "em"),
        (C5, dict(hy=0), "em"),
        (C5 + 0.60, dict(mx=0.0), "em"),
        (D_SK, dict(mx=0.0), "em"),
    ]

    SKL = co_khoa(SKL)

    def pha_gan(a, b, w):
        """pha hai dáng nền, góc đi đường ngắn nhất."""
        out_ = {}
        for k in set(a) | set(b):
            va, vb = a.get(k, ZERO5), b.get(k, ZERO5).copy()
            vb[0] = va[0] + (vb[0] - va[0]) - 360.0 * round((vb[0] - va[0]) / 360.0)
            out_[k] = va * (1 - w) + vb * w
        return out_

    def skill(t, P):
        chay = em((t - C2 + 0.05) / 0.10) * (1 - em((t - C3 + 0.04) / 0.08))                       # 1 trong lúc lao
        ram = em((t - C2 + 0.12) / 0.16) * (1 - em((t - C4) / (C5 - C4)))                           # khiên dựng mặt ra trước (hit_03)
        if t < C1:
            d_, src = mau_muot("skill_05", t * 0.5 / C1), ("skill_05", t * 0.5 / C1)
        elif t < C5:
            d_, src = mau("skill_03", (t - C1) % 1.0, True), ("skill_03", (t - C1) % 1.0)
            if ram > 0:
                d_ = pha_gan(d_, mau("hit_03", 0.2), ram)
            if chay > 0:
                ch = mau("run_01", 2.0 * (t - C2) + 0.1, True)
                for b in CHAN:
                    va, vb = d_.get(b, ZERO5), ch.get(b, ZERO5).copy()
                    vb[0] = va[0] + (vb[0] - va[0]) - 360.0 * round((vb[0] - va[0]) / 360.0)      # góc chân: đường ngắn nhất
                    d_[b] = va * (1 - chay) + vb * chay
        else:
            u = (t - C5) / (D_SK - C5)
            d_, src = mau_muot("skill_04", u), ("skill_04", u)
            if t < C5 + 0.18:                                                                      # nối êm từ thế che sang đoạn đứng dậy
                d_ = pha_gan(mau("skill_03", (C5 - C1) % 1.0, True), d_, em((t - C5) / 0.18))
        dat(P, d_)
        hien_theo_ho(P, *src)
        q = dict(DON.noi(SKL, t))
        if C1 < t < CP:                                                                            # cào chân gần xuống đất hai lần
            u = (t - C1) / (CP - C1)
            ph = (u * 2.0) % 1.0
            q["fRx"] = 34.0 * (1 - ph / 0.35) if ph < 0.35 else -34.0 + 68.0 * em((ph - 0.35) / 0.65)   # quẹt nhanh ra sau, đưa chậm về trước
            q["fRy"] = 16.0 * nhip(ph, 0.35, 0.65)
            q["fRr"] = -18.0 * nhip(ph, 0.35, 0.65)
            q["hr"] = q.get("hr", 0.0) - 2.5 * nhip(ph, 0.0, 0.35)
        if 0.0 < chay < 1.0:                                                                       # chuyển chân đứng (IK) ↔ chân chạy (FK): pha góc từng xương chân
            Pa, Pb = P.copy(), P.copy()
            B.dat(Pa, q, chan="nen", tay=False)
            B.dat(Pb, q, chan=False, tay=False)
            P.t = Pb.t
            for b in CHAN:
                va, vb = Pa.t.get(b, [0, 0, 0, 1, 1]), P._g(b)
                d = (vb[2] - va[2]) - 360.0 * round((vb[2] - va[2]) / 360.0)
                vb[2] = va[2] + d * chay
        else:
            B.dat(P, q, chan=False if chay >= 1.0 else "nen", tay=False)
        gian = 0.10 * chay - 0.13 * nhip(t, C3 - 0.005, 0.10) + 0.04 * nhip(t, C3 + 0.10, 0.14)      # giãn lúc lao, nén lúc húc, nảy lại
        if abs(gian) > 1e-4:
            P.scale("bone", 1.0 + gian, 1.0 - 0.7 * gian)
        thuc = nhip(t, C3 - 0.03, 0.20)                                                           # khiên thúc tới lúc húc
        if thuc > 0:
            B.doi_tg(P, "W_dunpai3", 54.0 * thuc, 8.0 * thuc)
        g = em((t - C1) / 0.15) * (1 - em((t - C2 + 0.14) / 0.1))                                 # gồng: hai dáng lệch 2–3° đổi nhau mỗi 2 khung
        s2 = 1.0 if int(t * FPS / 2) % 2 == 0 else -1.0
        gm = g * (0.4 + 0.6 * min(1.0, (t - C1) / max(0.01, C2 - 0.14 - C1)))
        P.rot("P_shenti3", 1.4 * gm * s2)
        P.rot("P_shouL2", -1.2 * gm * s2)
        P.move("bone2", 1.5 * gm * s2, 0.0)
        if C3 <= t < C4:                                                                          # rung sau cú húc, tắt dần
            k = (1 - (t - C3) / (C4 - C3)) ** 2
            P.move("bone2", 4.0 * k * math.sin(2 * math.pi * 15 * (t - C3)), 0.0)
            P.rot("W_dunpai3", 3.0 * k * math.sin(2 * math.pi * 18 * (t - C3)))
            P.rot("P_shouR2", 14.0 * k * math.sin(2 * math.pi * 3.2 * (t - C3)))                   # búa văng theo đà rồi lắc về
    out.append(Clip("skill", D_SK, skill, ev=[(0.05, "che_khien", ""), (C1, "tu_luc", ""), (C2, "lao", ""), (C3, "huc", ""),
                                             (C3 + 0.01, "trung", "")], trung=C3 + 0.01))

    # ---- APPEAR: khiên nằm đất trước mặt (skill_02 ~0,55 s), nhấc khiên lên (skill_02 0,55 → 1,17 s), ngẩng đầu GẦM (mặt há), về thế
    T_UP0, T_UP1 = 0.55, 1.167
    E1, E2, E3, D_AP = 0.25, 0.95, 1.75, 2.15

    def appear(t, P):
        if t < E1:
            u = T_UP0
        elif t < E2:
            u = T_UP0 + (T_UP1 - T_UP0) * em((t - E1) / (E2 - E1))
        else:
            u = T_UP1
        d_ = mau("skill_02", u)
        for b in ("P_shenti9", "P_shouR1", "P_shouR2", "P_shouR31", "W_futou", "P_jianjiaR02"):   # tay búa thõng như idle lúc nhấc khiên
            d_.pop(b, None)
        dat(P, d_)
        hien_theo_ho(P, "skill_02", u)
        gam =em((t - E2) / 0.18) * (1 - em((t - E3) / 0.30))
        P.rot("P_shenti8", 14.0 * gam)
        P.rot("P_tou2", 10.0 * gam)
        P.rot("P_shenti3", 5.0 * gam + 1.2 * gam * math.sin(2 * math.pi * 14 * t))
        P.move("bone2", 0.0, 6.0 * gam)
        if "mat_ha" in sk.atts and gam > 0.35:
            P.alpha["mat_ha"] = 1.0
            P.alpha["P_tou1"] = 0.0
        a_ = min(1.0, t / 0.08)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(E1, "nhat_khien", ""), (E2 + 0.1, "gam", "")]))

    # ---- DIE: die_01 của họ (búa văng, đổ sập lên khiên) + mờ dần
    D_DIE = CD["die_01"][0] + 0.45

    def die(t, P):
        dat(P, mau_muot("die_01", t))
        hien_theo_ho(P, "die_01", t)
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.75, "nga", "")]))
    return out


def go_vong(fr):
    """góc xoay của mỗi xương liền mạch qua các khung (bước > 180° dời về cùng vòng với khung trước): nối hai clip nguồn của họ có góc
    lệch nhau một vòng (thế che khiên skill_05 → skill_03 → skill_04) thì không quay nhảy."""
    for p, q in zip(fr, fr[1:]):
        for bn, v in q.t.items():
            if bn in p.t:
                v[2] -= 360.0 * round((v[2] - p.t[bn][2]) / 360.0)
    return fr


def nuong_het(sk, clips):
    """nướng mọi clip: gỡ vòng góc; ba clip tấn công tự dựng thêm lớp phụ trễ theo thân (bờm, vạt, đuôi, tai, mặt dây)."""
    fr = {}
    for c in clips:
        f = go_vong(hoat.nuong(sk, c))
        if c.ten in ("attack", "cast", "skill"):
            DON.phu(sk, f, FPS)
        fr[c.ten] = f
    return fr


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "kiem":
        for c in clips:
            fr = nuong_het(sk, [c])[c.ten]
            xau = {}
            for p, q in zip(fr, fr[1:]):
                for bn in set(p.t) | set(q.t):
                    d = abs(q.t.get(bn, [0, 0, 0, 1, 1])[2] - p.t.get(bn, [0, 0, 0, 1, 1])[2])
                    xau[bn] = max(xau.get(bn, 0), d)
            lon = sorted(((v, k) for k, v in xau.items() if v > 40), reverse=True)[:6]
            print(f"{c.ten:7s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°"))
        return
    if a and a[0] == "bo_cuc":                # hình bố cục: khung 0 idle trên nền trắng (ảnh mẫu tỉ lệ cho concept dạng non)
        fr = nuong_het(sk, [x for x in clips if x.ten == "idle"])["idle"]
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.10)
        sc_ = float(a[2]) if len(a) > 2 else 1.4
        im = ve.ve(fr[0], Bx, sc_, bg=(255, 255, 255), ss=2).convert("RGB")
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        im.save(a[1])
        json.dump(dict(box=list(Bx), scale=sc_, cao=info["cao"]), open(a[1][:-4] + ".json", "w"), indent=1)  # px = ((X − x0)·sc, (y1 − Y)·sc)
        print(a[1], im.size, "cao", round(info["cao"]))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = nuong_het(sk, [c])[c.ten]
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
    if a and a[0] == "nhe":                   # dạng 2: ghi bản nhẹ để dạng non gộp tiến hóa (rig + khung 0 idle + chiều cao + đoạn gầm của appear)
        import pickle
        fr = nuong_het(sk, [c for c in clips if c.ten in ("idle", "appear")])
        os.makedirs(RA, exist_ok=True)
        pickle.dump((sk, fr["idle"][0], info["cao"], fr["appear"]), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    frames = nuong_het(sk, clips)
    M, noi = sk, {}
    if NON and os.environ.get("SG_TIENHOA", "1") == "1":
        # TIẾN HÓA nối liền (quai/tienhoa.py): gộp rig dạng 2 (dựng ở tiến trình riêng). Sói con vào thế che khiên (skill_05), gồng run mạnh
        # dần sau khiên; đổi dạng lúc gồng mạnh nhất (VFX game che); dạng 2 hiện ra đúng đoạn NGẨNG ĐẦU GẦM của appear (mặt há), rồi hoà về
        # khung 0 idle dạng 2.
        import pickle
        import subprocess
        from quai import tienhoa
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, SG_DANG="2", SG_RA="", SG_MANH=""),
                       check=True)
        sk2, idle2, cao2, appear2 = pickle.load(open(os.path.join(G.BASE, "rig", "_nhe.pkl"), "rb"))
        ti = info["cao"] / cao2
        M = tienhoa.gop(sk, sk2)
        chung = 0
        for nm in list(sk2.images):                       # ảnh trùng từng điểm ảnh giữa hai dạng thì dùng chung
            if nm in sk.images and sk.images[nm].size == sk2.images[nm].size and \
                    np.array_equal(np.asarray(sk.images[nm]), np.asarray(sk2.images[nm])):
                M.images.pop("n_" + nm, None)
                for sl in M.atts.values():
                    for sp in sl.values():
                        if sp.get("path") == "n_" + nm:
                            sp["path"] = nm
                chung += 1
        print(f"  gộp tiến hóa: {chung} / {len(sk2.images)} ảnh dùng chung với dạng 1")
        # ảnh dạng 2 trong rig gộp chỉ hiện lúc tiến hóa (cỡ ~0,79): thu còn THU2 cho .atomik dưới trần (lưới dùng uv chuẩn hoá nên hình không lệch)
        # ảnh dạng 1 thu THU1 (ra sân ở cỡ 0,8: vẫn dư điểm ảnh); cả hai cho .atomik dưới trần 0,5 MB
        THU2, THU1 = 0.55, 0.88
        for nm in list(M.images):
            k_ = THU2 if nm.startswith("n_") else THU1
            im_ = M.images[nm]
            M.images[nm] = im_.convert("RGBa").resize((max(1, round(im_.width * k_)), max(1, round(im_.height * k_))),
                                                      Image.LANCZOS).convert("RGBA")
        for sl in M.atts.values():
            for sp in sl.values():
                if "width" in sp and "path" in sp:
                    k_ = THU2 if str(sp["path"]).startswith("n_") else THU1
                    sp["width"] = max(1, round(sp["width"] * k_))
                    sp["height"] = max(1, round(sp["height"] * k_))
        M.luoi = {}
        skill_c = [c for c in clips if c.ten == "skill"][0]
        T_GAM0, T_GAM1 = 0.95, 1.75                       # đoạn gầm trong appear dạng 2 (E2 → E3)

        def gong(t, P):
            skill_c.fn(min(t * 0.9, 0.9), P)              # vào thế che khiên rồi giữ (gồng sẵn có trong skill)
            aA = 1 - hoat.ease((t - 1.05) / 0.30)          # khiên nhìn thẳng (ẩn mặc định) mờ theo dạng cũ như mọi slot khác
            for s_ in ("W_dunpai1", "W_dunpai2"):
                P.alpha[s_] = P.alpha.get(s_, 0.0) * aA
            g = em((t - 0.35) / 0.7)
            P.rot("P_shenti3", 2.2 * g * (1 if int(t * FPS / 2) % 2 == 0 else -1))
            P.move("bone2", 2.4 * g * math.sin(2 * math.pi * 11 * t), -5.0 * g)

        def bung(t, P, fl):
            tb = T_GAM0 - 0.25 + (T_GAM1 - T_GAM0 + 0.25) * min(1.0, max(0.0, (t - 1.15) / 1.3))
            Q = appear2[min(len(appear2) - 1, int(round(tb * 30)))]
            for b_, v in Q.t.items():
                P.t["n_" + b_] = list(v)
            for s_, v in Q.alpha.items():
                if s_ in ("mat_ha", "P_tou1"):
                    P.alpha["n_" + s_] = v * min(1.0, max(0.0, (t - 1.12) / 0.33))

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=bung,
                                   ev=[(0.3, "tu_luc", ""), (1.25, "doi_dang", ""), (1.62, "gam", "")])
        for e_, m_ in (("tu_luc", "tiến hóa: gồng sau khiên"), ("doi_dang", "tiến hóa: đổi dạng"), ("gam", "tiến hóa: dạng mới gầm")):
            M.su_kien(e_, m_)
        clips = clips + [ev]
        frames["evolve"] = go_vong(hoat.nuong(M, ev))
        _, _, s_ev = tienhoa.lech_cuoi(M, frames["evolve"], sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips, RA, TEN, ("Sói giáp sắt dạng 1 (soi_giap_non)" if NON else "Sói giáp sắt (soi_giap)") + ": tướng 6 đảo Kim" +
                  (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=1, so_dang=2 if NON else 1, noi_them=noi, dung_yen=("cast",), lao=("skill",), far=("cast",), cao=info["cao"],
                  ma_goc=None, tol={"rotate": 0.12, "translate": 0.25, "scale": 0.002} if NON else {"rotate": 0.05, "translate": 0.12, "scale": 0.001},
                  khop_idle=0.2,
                  impact={"attack": (0.05, 0.25, 0.07), "skill": (0.12, 0.9, 0.18, "#e8eef655")} if NON else
                  {"attack": (0.07, 0.35, 0.09), "skill": (0.16, 1.3, 0.24, "#e8eef666")})


if __name__ == "__main__":
    main(sys.argv[1:])
