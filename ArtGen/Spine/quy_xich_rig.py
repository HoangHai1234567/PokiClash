# -*- coding: utf-8 -*-
"""Quỷ xích (quy_xich, tướng 5 đảo Kim): RESKIN trên rig con gốc monster_3408 (quỷ béo cánh dơi, móc nối xích).

- Xương: đủ mọi xương của họ + `move`; dáng gốc = khung 0 idle_01 (biến đổi riêng `l` đã áp IK + path, lấy mẫu bằng runtime Spine thật).
- Hình: mỗi hình của họ một hình của mình, NGUYÊN lưới của họ (điểm gắn theo ma trận dáng gốc trong att_goc.json). Mảnh ĐỔI DÁNG (đỉnh mũ,
  má mũ, sừng, vây lưng, giáp vai to, ổ khoá, móc) là mảnh cứng một xương thay đúng slot của họ (quy_xich_manh.py, manh/moi.json).
- Thứ tự vẽ: của họ. skill_01 (quay xích) vẽ móc thứ hai + xích dài SAU tay xa (khung 0–21), die_01 / hit_02 vẽ TRƯỚC tay: các slot đó có
  bản `_sau` (trước P_shouL1), bật bản nào theo thứ tự vẽ của họ ở từng khung.
- Xích bay (cast, skill): móc bay `moc_bay` trên `moc_t` con của `fly_m`; XICH_N mắt xích, mắt k trên `xich_k` con của `fly_k`. Xương fly
  mang phần quãng w × far, xương con mang (1 − w) × điểm xuất phát (tay) → game (AolaActor.FarAtomik, far + farAim) co quãng tới đối thủ
  thật và xoay mắt xích theo hướng thật; mắt k luôn nằm trên đoạn tay → móc.
- Clip: idle, walk, hit, die = của họ (die mờ dần). attack = skill_02 (thu người, bay vọt, giơ móc, BỔ xuống) + lao tới, độ cao bay hạ
  còn BAY_ATK, cú rơi làm trơn (clip của họ rơi 460 đơn vị trong một khung). appear = bay từ ngoài trên trái vào (dáng bay của skill_02,
  cánh vỗ theo run_01), khựng, rơi thẳng xuống đáp nặng (đoạn đáp của skill_02). cast = skill_01 (quay xích qua đầu, ném): móc + xích bay tới
  `far`, găm, giật về, móc lắp lại trong tay. skill = xích bốc lửa (sự kiện), quay xích nhiều vòng nhanh dần (đoạn vòng của skill_01 lặp),
  ném, móc quấn TRÓI đối thủ, giữ xích căng giật giật, CỘT LỬA (sự kiện cho VFX), thả, giật móc về.

    quy_xich_rig.py                         dựng, xuất inbox/quy_xich_1/rig/
    quy_xich_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    quy_xich_rig.py kiem                    bước xoay lớn nhất giữa hai khung của từng clip
    QX_GOC=1 quy_xich_rig.py ...            dựng bằng DA GỐC (manh_goc/) ra rig_goc/: chỉ để soi clip trong máy, không đưa vào game
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
import quy_xich as G  # noqa: E402

GOC = os.environ.get("QX_GOC") == "1"
# DẠNG: "2" = dạng cuối đã duyệt (quỷ giáp kín, inbox/quy_xich_1); "non" = dạng 1 non trên CÙNG xương / lưới / clip (inbox/quy_xich_non):
# đổi tỉ lệ ở xương gốc từng bộ phận (đầu to, cánh nhỏ, móc nhỏ) rồi chuyển da (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc")
NON = os.environ.get("QX_DANG") == "non"
BASE = os.path.join(os.path.dirname(G.BASE), "quy_xich_non") if NON else G.BASE
TEN = "quy_xich_non" if NON else "quy_xich"
RA = os.environ.get("QX_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("QX_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
if NON and not GOC and not os.path.isdir(MANH):
    MANH = os.path.join(G.BASE, "manh")                 # chưa có da dạng non: dựng bố cục bằng da dạng 2
# dạng non có da riêng (manh/moi.json vẽ ở dáng gốc non): bỏ các slot dạng non không có (má mũ, ba vây, giáp vai nhỏ, hai giáp cổ)
DA_NON = NON and not GOC and os.path.normpath(MANH) == os.path.normpath(os.path.join(BASE, "manh"))
AN_NON = ("P_toukui1", "P_toukui3", "P_jiejing1", "P_jiejing2", "P_jiejing3", "P_jianjiaL", "P_xiongjiaL1", "P_xiongjiaR1")
BO_SLOT = AN_NON if DA_NON else ()
TI_LE = {} if not NON else {"bone11": float(os.environ.get("QX_DAU") or 1.25),        # đầu (mặt, sừng, mũ là con của bone11)
                            "bone27": float(os.environ.get("QX_CANH") or 0.72), "bone33": float(os.environ.get("QX_CANH") or 0.72),
                            "bone14b2": float(os.environ.get("QX_MOC") or 0.8)}       # móc tay (+ xích treo dưới cán)
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
SAU = ("W_wuqi2", "W_sB05", "W_sB06", "W_sB07", "W_sA05", "W_sA08", "W_sA09", "W_sA07")   # có bản _sau (sau tay xa)
XICH_DAI = SAU                    # móc thứ hai + xích dài của họ (skill_01 quay xích, die, hit_02)
XICH_TAY = ("W_sB02", "W_sB03", "W_sB04", "W_sA02", "W_sA03", "W_sA04", "W_sA06")       # 7 mắt xích treo dưới cán móc cầm tay
CANH = tuple(f"bone{i}" for i in range(27, 39))                                           # hai chuỗi xương cánh
XICH_N = 18                       # số mắt xích bay
TRE_TRUNG = 0.012
T_GO_ATK = 0.775                # lưỡi móc tới đỉnh đầu đối thủ (đo: 0,733 trên đầu bên trái, 0,767 đỉnh đầu, 0,80 đập xuống)


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung, đã áp ràng buộc)
def _cd():
    out = {}
    ia = SL.index("P_shouL1")
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
        sau = [{s: F["o"].index(SL.index(s)) < F["o"].index(ia) for s in SAU} for F in fr]
        hien = [[(F["n"][k] is not None) * float(F["a"][k]) for k in range(len(SL))] for F in fr]
        out[clip] = (float(v["dur"]), res, sau, hien)
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
        vb = np.array(b.get(k, np.array([0, 0, 0, 1, 1.0])), float)
        vb[0] -= 360.0 * round((vb[0] - va[0]) / 360.0)          # góc cùng vòng: trộn theo đường ngắn
        out[k] = va * (1 - w) + vb * w
    return out


def nuong(sk, clip):
    """như hoat.nuong nhưng góc LIỀN MẠCH (mỗi khung chọn bội 360° gần khung trước nhất: mẫu của họ có chỗ quấn góc, trộn hai dáng có thể
    lệch một vòng) và khép vòng clip lặp hoà về khung 0 + 360°k gần nhất (hoat.dong_vong hoà thẳng về khung 0 làm đuôi walk quay ngược 245°)."""
    n = int(round(clip.dur * FPS)) + 1
    ts = [min(clip.dur, i / FPS) for i in range(n)]
    frames = []
    for t in ts:
        P = Pose()
        clip.fn(t, P)
        frames.append(P)
    for i in range(1, n):
        Pp, Q = frames[i - 1], frames[i]
        for b, g in Q.t.items():
            a0 = Pp.t.get(b, [0, 0, 0, 1, 1])[2]
            g[2] -= 360.0 * round((g[2] - a0) / 360.0)
    # clip lặp: fn lấy mẫu t % dur nên khung cuối CHÍNH LÀ khung 0 (góc đã đưa về bội 360° liền với khung trước ở trên): vòng tự khép,
    # không hoà (xương quay đều nhiều vòng như đuôi run_01, +75° / khung, mà hoà về khung 0 thì khựng rồi nhảy)
    return frames


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
    """độ đậm mọi slot theo khung của họ; slot có bản _sau bật bản nào theo thứ tự vẽ của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    _, _, sau, hien = CD[clip]
    for k, sl in enumerate(SL):
        if sl == "shadow" or sl in BO_SLOT:
            continue
        a = 1.0 if hien[i][k] > 0.5 else 0.0
        if sl in SAU:
            P.alpha[sl] = 0.0 if sau[i][sl] else a
            P.alpha[sl + "_sau"] = a if sau[i][sl] else 0.0
        else:
            P.alpha[sl] = a


# ---------------------------------------------------------------- dựng
def manh_goc():
    """da gốc (chỉ để soi clip): mỗi vùng ảnh cắt theo lưới, phóng RES."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_goc.json")
    os.makedirs(MANH, exist_ok=True)
    for a in atts:
        p = os.path.join(MANH, a["region"] + ".png")
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
    # thế giới dáng gốc KHÔNG đổi tỉ lệ: mảnh cứng (moi.json, toạ độ thế giới của dạng 2) gắn theo hệ này thì co / phóng cùng xương
    sk_c = Sk("_c")
    sk_c.xuong("root")
    sk_c.xuong("move", "root")
    for i, b in enumerate(I["bones"]):
        if b["name"] != "root":
            z = L0[i]
            sk_c.xuong(b["name"], "move" if NB[b["parent"]] == "root" else NB[b["parent"]], z[0], z[1], goc=z[2], dai=b["len"], sx=z[3], sy=z[4])
    Wc = sk_c.the_gioi()
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

    def gan(slot_ten, a, an, r=None):
        r = r or a["region"]
        im = anh_cua(r)
        wr, hr = imgs_ho[a["region"]].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        sk.slot(slot_ten, rows[0][0][0], r, an=an)
        sk.atts[slot_ten][r] = {"type": "mesh", "path": r, "uv": uv, "tris": np.asarray(tris, int).reshape(-1, 3), "hull": len(uv),
                                "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, r)] = Luoi(uv * np.array([im.width, im.height], float), np.asarray(tris, int).reshape(-1, 3), len(uv), len(uv),
                                      im.width, im.height, ten=slot_ten)
        return V0

    def gan_cung(slot_ten, ten_anh, bone, Vw, an, Wb=None):
        """mảnh cứng: ô 4 đỉnh (thế giới khung 0 idle, hoặc trong hệ Wb) bám trọn một xương."""
        im = anh_cua(ten_anh)
        Wb = (Wi if DA_NON else Wc)[bone] if Wb is None else Wb
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        rows = [[(bone, *map(float, np.linalg.solve(Wb, np.array([v[0], v[1], 1.0]))[:2]), 1.0)] for v in Vw]
        V0 = np.array([(Wi[bone] @ np.array([r_[0][1], r_[0][2], 1.0]))[:2] for r_ in rows])
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.slot(slot_ten, bone, ten_anh, an=an)
        sk.atts[slot_ten][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": tris, "hull": 4, "V": V0, "verts": rows,
                                      "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_anh)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)
        return V0

    # ---- mảnh đổi dáng (moi.json): slot của họ → (tên ảnh, xương, 4 góc thế giới khung 0 idle)
    MOI = {}
    if not GOC and os.path.exists(os.path.join(MANH, "moi.json")):
        for ten, d in json.load(open(os.path.join(MANH, "moi.json"))).items():
            MOI[d["slot"]] = (ten, d["xuong"], np.array(d["the_gioi"], float))
    # móc thứ hai (W_wuqi2, xương bone14b11, đầu xích dài): cùng ảnh móc, đặt như móc tay theo phép dời giữa hai bản móc của họ
    if "W_wuqi" in MOI:
        a1, a2 = by["W_wuqi"], by["W_wuqi2"]
        uv1, _ = G.luoi(a1)
        uv2, _ = G.luoi(a2)
        M1, *_ = np.linalg.lstsq(np.c_[uv1, np.ones(len(uv1))], np.array(a1["xy"], float).reshape(-1, 2), rcond=None)   # px → thế giới gốc
        M2, *_ = np.linalg.lstsq(np.c_[uv2, np.ones(len(uv2))], np.array(a2["xy"], float).reshape(-1, 2), rcond=None)
        # 4 góc móc mới (thế giới khung 0 idle) → hệ xương bone14b2 (Wi) → thế giới GỐC của họ (WG) → px vùng (M1⁻¹) → thế giới gốc bản 2 (M2)
        ten, bn, Vw = MOI["W_wuqi"]
        loc = [np.linalg.solve((Wi if DA_NON else Wc)[bn], np.array([v[0], v[1], 1.0])) for v in Vw]
        km = TI_LE.get(bn, 1.0)                           # móc tay thu km (dạng non): móc thứ hai (đầu xích dài, xương không thu) thu theo
        wg = np.array([(WG[bn] @ (np.array([km, km, 1.0]) * l_))[:2] for l_ in loc])
        A1 = np.c_[M1.T[:, :2], M1.T[:, 2]]
        px = np.array([np.linalg.solve(A1[:, :2], v - A1[:, 2]) for v in wg])
        wg2 = np.c_[px, np.ones(4)] @ M2
        MOI["W_wuqi2"] = (ten, "bone14b11", wg2, WG["bone14b11"])

    def gan_slot(slot_ten, a, an):
        sl0 = slot_ten.replace("_sau", "")
        if sl0 in MOI:
            m = MOI[sl0]
            return gan_cung(slot_ten, m[0], m[1], m[2], an, Wb=m[3] if len(m) > 3 else None)
        return gan(slot_ten, a, an)

    atts = sorted(AG["atts"], key=lambda q: q["order"])
    if DA_NON:                                            # dạng non: sừng trái cũng nằm SAU nồi (như sừng phải), nhô lên khỏi đỉnh nồi
        atts = [q for q in atts if q["slot"] != "P_jiaoR1"]
        i_ = [q["slot"] for q in atts].index("P_toukui2")
        atts.insert(i_, by["P_jiaoR1"])
    for a in atts:
        if a["slot"] in BO_SLOT:
            continue
        if a["slot"] == "P_shouL1":                       # bản _sau: móc thứ hai + xích dài vẽ sau tay xa (skill_01 lúc quay)
            for s_ in SAU:
                gan_slot(s_ + "_sau", by[s_], an=True)
        gan_slot(a["slot"], a, an=not hien0[a["slot"]])
        if a["slot"] == "P_shouL31":                      # xích bay + móc bay: lớp tay xa (sau thân, trước móc tay)
            them_xich_bay(sk, anh_cua, by, imgs_ho, Wi, MOI)

    for e, m in (("bay_len", "rời đất bay lên"), ("go", "móc bổ xuống"), ("trung", "khung trúng"), ("cham_dat", "chạm đất (bụi)"),
                 ("quay", "bắt đầu quay xích (VFX vệt theo móc quay: xương bone14b11)"), ("nem", "móc rời tay bay đi"),
                 ("rut", "giật xích về"), ("moc_ve", "móc lắp lại trong tay"), ("lua_xich", "xích bốc lửa (VFX lửa bám mắt xích)"),
                 ("troi", "móc quấn trói đối thủ (VFX vòng xích quanh đối thủ)"), ("cot_lua", "CỘT LỬA rất to dưới đối thủ (VFX)"),
                 ("chay", "nhịp thiêu đốt"), ("tha", "thả trói, xích hết lửa"), ("nga", "ngã")):
        sk.su_kien(e, m)
    cao = float(max(sp["V"][:, 1].max() for sn, sl in sk.atts.items() if hien0.get(sn) for sp in sl.values()))
    sk.xuong("far", "root", 1.6 * cao, 0.42 * cao)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(cao=cao)


def them_xich_bay(sk, anh_cua, by, imgs_ho, Wi, MOI):
    """móc bay + XICH_N mắt xích bay. Ảnh mắt xích: hai ảnh của họ / của mình (W_suolian1 nghiêng, W_suolian2 thẳng) xen kẽ; trục dài của
    mắt xích nằm theo trục x của xương con (dọc đường xích). Móc bay: ảnh móc, gốc xương con ở VÒNG CUỐI cán (chỗ xích nối), lưỡi chĩa +x."""
    for k in range(XICH_N):
        sk.xuong(f"fly_{k}", "root", 0.0, 0.0)
        sk.xuong(f"xich_{k}", f"fly_{k}", 0.0, 0.0)
        r = "W_suolian2" if k % 2 == 0 else "W_suolian1"
        im = anh_cua(r)
        wr, hr = imgs_ho[r].size
        km = TI_LE.get("bone14b2", 1.0)                    # dạng non: mắt xích bay thu như xích treo dưới móc tay (con của bone14b2)
        dai, rong = hr * 2.0 * km, wr * 2.0 * km            # đơn vị rig (atlas họ 0,5 px / đơn vị); ảnh đứng → nằm theo +x
        V = np.array([[-dai / 2, rong / 2], [-dai / 2, -rong / 2], [dai / 2, -rong / 2], [dai / 2, rong / 2]])
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)          # mép trên ảnh (uv y=0) → đầu −x
        uv = np.array([[1, 0], [0, 0], [0, 1], [1, 1]], float)
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sl = f"xich_bay_{k}"
        sk.slot(sl, f"xich_{k}", r, an=True)
        sk.atts[sl][r] = {"type": "mesh", "path": r, "uv": uv, "tris": tris, "hull": 4, "V": V,
                          "verts": [[(f"xich_{k}", float(v[0]), float(v[1]), 1.0)] for v in V], "width": im.width, "height": im.height}
        sk.luoi[(sl, r)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=sl)
    # móc bay: lấy hình móc tay (slot W_wuqi) trong hệ xương bone14b2, dời gốc về vòng cuối cán, xoay cho cán → lưỡi theo +x
    sk.xuong("fly_m", "root", 0.0, 0.0)
    sk.xuong("moc_t", "fly_m", 0.0, 0.0)
    at = sk.atts["W_wuqi"]
    r = list(at)[0]
    sp = at[r]
    loc = np.array([[row[0][1], row[0][2]] for row in sp["verts"]]) if all(len(row) == 1 for row in sp["verts"]) else None
    if loc is None:                                       # lưới nhiều xương (da gốc): đổi thế giới khung 0 về hệ bone14b2
        loc = np.array([np.linalg.solve(Wi["bone14b2"], np.array([v[0], v[1], 1.0]))[:2] for v in sp["V"]])
    vong, luoi_ = MOC_TRUC
    d = np.array(luoi_) - np.array(vong)
    g = math.atan2(d[1], d[0])
    R = np.array([[math.cos(-g), -math.sin(-g)], [math.sin(-g), math.cos(-g)]])
    V = (loc - np.array(vong)) @ R.T * TI_LE.get("bone14b2", 1.0)      # dạng non: móc bay thu như móc tay
    sk.slot("moc_bay", "moc_t", r, an=True)
    sk.atts["moc_bay"][r] = dict(sp, V=V, verts=[[("moc_t", float(v[0]), float(v[1]), 1.0)] for v in V])
    sk.luoi[("moc_bay", r)] = sk.luoi[("W_wuqi", r)]


# trục móc trong hệ xương bone14b2 (vòng cuối cán, giữa lưỡi): đo một lần trên khung 0 idle (đặt trong main sau khi dựng)
MOC_TRUC = ((0.0, 0.0), (1.0, 0.0))


# ---------------------------------------------------------------- tiện ích
def bat_tat(P, ds, a):
    for s in ds:
        P.alpha[s] = a


def lam_clip(sk, info):
    out = []
    cao = info["cao"]
    F = sk.W0["far"][:2, 2]

    def tg(P, b):
        return sk.the_gioi(P)[b]

    # ---- idle / walk / hit / die: của họ
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

    D_DIE = CD["die_01"][0] + 0.45

    def die(t, P):
        dat(P, mau("die_01", t))
        hien_theo_ho(P, "die_01", t)
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.55, "nga", "")]))

    # ---- ĐÁNH THƯỜNG: skill_02 của họ. Họ bay vọt 474 đơn vị (bone2) rồi RƠI cả quãng trong một khung (0,67 → 0,73) lúc móc bổ xuống.
    # Mình: độ cao bay × BAY_ATK, rơi trơn trong T_ROI; lao tới (move) lúc đang bay, móc bổ xuống đầu đối thủ ở đỉnh lao.
    BAY_ATK = 0.38
    # cú bổ của họ nằm gọn giữa hai khung nguồn (0,70 → 0,733): giãn ra 0,10 s (0,62 → 0,72) cho móc vung qua đầu thấy được
    U_ATK = [(0.0, 0.0), (0.22, 0.20), (0.50, 0.53), (0.62, 0.667), (0.76, 0.733), (0.83, 0.80), (1.10, 1.07), (1.42, 1.333)]
    D_ATK = 1.42
    T_GO = T_GO_ATK                      # lưỡi móc đi qua đỉnh đầu đối thủ (đo bằng do_go)
    LAO = 0.72 * 1.9 * cao               # ≈ quãng game nắn tới (72 % của ~1,9 chiều cao): khỏi bị phóng cả cú nảy về

    def tq(t, bang):
        for (a_, x), (b_, y) in zip(bang, bang[1:]):
            if t <= b_:
                return x + (y - x) * (t - a_) / (b_ - a_)
        return bang[-1][1]

    y_b2 = CD["skill_02"][1]["bone2"][:, 2]

    def cao_bay(u):
        """độ cao bone2 của họ ở giây u của skill_02 (đơn vị dời so với dáng gốc)."""
        x = min(max(u, 0.0), CD["skill_02"][0]) * FPS
        i0 = min(int(x), len(y_b2) - 1)
        i1 = min(i0 + 1, len(y_b2) - 1)
        return y_b2[i0] * (1 - (x - i0)) + y_b2[i1] * (x - i0)

    def attack(t, P):
        u = tq(t, U_ATK)
        d_ = mau("skill_02", u)
        hy = cao_bay(u)
        if 0.62 < t < 0.76:                              # rơi trơn: từ độ cao lúc 0,62 về 0 lúc 0,76 (họ cắt cảnh trong một khung)
            h0 = cao_bay(tq(0.62, U_ATK))
            hy = h0 * (1 - em((t - 0.62) / 0.14)) ** 1.6
        if "bone2" in d_:
            d_["bone2"] = d_["bone2"].copy()
            d_["bone2"][2] = hy * BAY_ATK
        dat(P, d_)
        hien_theo_ho(P, "skill_02", u)
        # đỉnh lao (game nắn tới 72 % quãng) rơi vào lúc đang bay tới; lúc bổ thân lùi về 85 % đỉnh: thân béo chúi tới chỉ chạm mép đối
        # thủ, lưỡi móc (vươn ~0,8 chiều cao trước thân) vẫn tới đỉnh đầu nó
        lao = LAO * em((t - 0.18) / 0.42) * (1 - 0.15 * em((t - 0.60) / 0.18)) * (1 - em((t - 0.94) / 0.40))
        nay = 0.10 * cao * math.sin(math.pi * min(1.0, max(0.0, (t - 0.94) / 0.40))) if t > 0.94 else 0.0
        P.move("move", lao, nay)
    out.append(Clip("attack", D_ATK, attack, ev=[(0.22, "bay_len", ""), (0.70, "go", ""), (T_GO, "trung", ""),
                                                 (0.76, "cham_dat", "")], trung=T_GO))

    # ---- APPEAR: bay từ ngoài trên trái vào (dáng bay skill_02 ~0,36 s, cánh vỗ theo run_01 nhanh), khựng, rơi thẳng xuống, đáp nặng
    # (đoạn 0,73–1,33 của skill_02 = rơi chúi + đáp + đứng dậy), về thế.
    D_AP = 1.75
    T_ROI0, T_CHAM = 0.78, 1.00

    def appear(t, P):
        if t < T_ROI0:
            d_ = mau("skill_02", 0.36)
            d_.pop("bone2", None)
            vo = mau("run_01", t * 1.6, True)
            for b_ in CANH:
                if b_ in vo:
                    d_[b_] = vo[b_]
            dat(P, d_)
            hien_theo_ho(P, "skill_02", 0.36)
            q = min(1.0, t / 0.62)
            x = -1.15 * cao * (1 - em(q)) ** 1.3
            y = 0.62 * cao + 0.42 * cao * (1 - em(q)) + 0.025 * cao * math.sin(2 * math.pi * 3.2 * t)
            P.move("move", x, y)
            P.rot("bone3", -10.0 * (1 - q) + 8.0 * em((t - 0.55) / 0.2))          # chúi tới khi bay, ngả ra sau khi phanh
        elif t < T_CHAM:                                  # rơi: dáng của họ đi liền 0,36 → 0,733 (giơ móc qua đầu rồi bắt đầu bổ)
            w = (t - T_ROI0) / (T_CHAM - T_ROI0)
            u = 0.36 + (0.733 - 0.36) * w ** 1.2
            d_ = mau("skill_02", u)
            d_.pop("bone2", None)
            if t < T_ROI0 + 0.15:                         # cánh: hoà từ nhịp vỗ sang dáng rơi (đổi thẳng thì cánh giật 76°)
                vo = mau("run_01", t * 1.6, True)
                k_ = em((t - T_ROI0) / 0.15)
                for b_ in CANH:
                    if b_ in vo or b_ in d_:
                        d_[b_] = pha({b_: vo.get(b_, np.array([0, 0, 0, 1, 1.0]))}, {b_: d_.get(b_, np.array([0, 0, 0, 1, 1.0]))}, k_)[b_]
            dat(P, d_)
            hien_theo_ho(P, "skill_02", u)
            P.move("move", 0.0, 0.62 * cao * (1 - w * w))
            P.rot("bone3", 8.0 * (1 - w))
        else:                                             # đáp: 0,733 → 0,80 trong 0,07 s (móc đập đất), rồi đứng dậy tới 1,333
            u = 0.733 + (t - T_CHAM) / 0.07 * 0.067 if t < T_CHAM + 0.07 else                 0.80 + (t - T_CHAM - 0.07) * (1.333 - 0.80) / (D_AP - T_CHAM - 0.07)
            d_ = mau("skill_02", u)
            if "bone2" in d_:
                d_["bone2"] = d_["bone2"].copy()
                d_["bone2"][2] = 0.0
            dat(P, d_)
            hien_theo_ho(P, "skill_02", u)
            dap = em((t - T_CHAM) / 0.05) * (1 - em((t - T_CHAM - 0.05) / 0.25))
            P.scale("bone2", 1.0 + 0.10 * dap, 1.0 - 0.14 * dap)
        a_ = min(1.0, t / 0.08)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(T_ROI0, "go", ""), (T_CHAM, "cham_dat", "")]))

    # ---- XÍCH BAY (cast, skill): A = điểm nắm (gốc xương móc tay bone14b2) của khung đó; q = phần quãng móc đã bay (0..1)
    vong = np.array(MOC_TRUC[0])

    def xich_bay(P, q, goc_ve=None, w_ve=0.0, an_het=False):
        W = sk.the_gioi(P)
        A = (W["bone14b2"] @ np.array([*vong, 1.0]))[:2]
        d = F - A
        g = math.degrees(math.atan2(d[1], d[0]))
        an = an_het or q <= 0.02
        for k in range(XICH_N):
            w = (k + 1) / XICH_N * q
            P.move(f"fly_{k}", float(w * F[0]), float(w * F[1]))
            c = (1 - w) * A
            P.move(f"xich_{k}", float(c[0]), float(c[1]))
            P.rot(f"xich_{k}", g + (90.0 if k % 2 else 0.0) * 0)
            P.alpha[f"xich_bay_{k}"] = 0.0 if an else 1.0
        P.move("fly_m", float(q * F[0]), float(q * F[1]))
        c = (1 - q) * A
        P.move("moc_t", float(c[0]), float(c[1]))
        gm = g
        if goc_ve is not None and w_ve > 0:
            gv = goc_ve - 360.0 * round((goc_ve - g) / 360.0)
            gm = g + (gv - g) * w_ve
        P.rot("moc_t", gm)
        P.alpha["moc_bay"] = 0.0 if an else 1.0

    def goc_moc_tay(P):
        """góc thế giới của trục vòng → lưỡi của móc tay ở tư thế P."""
        Wm = sk.the_gioi(P)["bone14b2"]
        d = Wm[:2, :2] @ (np.array(MOC_TRUC[1]) - vong)
        return math.degrees(math.atan2(d[1], d[0]))

    # ---- CHIÊU MANA: skill_01 của họ. Quay xích qua đầu 0–0,70 (móc thứ hai + xích dài của họ, sau tay); ném 0,733: móc + xích bay tới
    # far trong BAY_C, găm, giữ (tay duỗi giữ xích), giật về 1,07–1,25, móc tay hiện lại 1,267 (khung 38 của họ).
    T_NEM, BAY_C, T_RUT0, T_RUT1, T_VE = 22 / FPS, 0.15, 1.07, 1.25, 38 / FPS
    D_CAST = CD["skill_01"][0]

    def q_cast(t):
        if t < T_NEM:
            return 0.0
        if t < T_NEM + BAY_C:
            return em((t - T_NEM) / BAY_C) ** 0.7
        if t < T_RUT0:
            return 1.0
        return 1.0 - em((t - T_RUT0) / (T_RUT1 - T_RUT0))

    def cast(t, P):
        dat(P, mau("skill_01", t))
        hien_theo_ho(P, "skill_01", t)
        if t >= T_NEM:
            bat_tat(P, XICH_DAI + tuple(s + "_sau" for s in SAU), 0.0)     # xích dài của họ → xích bay của mình
            P_ve = Pose()
            dat(P_ve, mau("skill_01", T_VE))
            xich_bay(P, q_cast(t), goc_moc_tay(P_ve), em((t - (T_RUT0 + 0.6 * (T_RUT1 - T_RUT0))) / (0.4 * (T_RUT1 - T_RUT0))),
                     an_het=t >= T_VE)
        else:
            xich_bay(P, 0.0, an_het=True)
    out.append(Clip("cast", D_CAST, cast, ev=[(0.20, "quay", ""), (T_NEM, "nem", ""), (T_NEM + BAY_C + TRE_TRUNG, "trung", ""),
                                             (T_RUT0, "rut", ""), (T_VE, "moc_ve", "")], trung=T_NEM + BAY_C + TRE_TRUNG))

    # ---- CHIÊU CUỐI: xích bốc lửa, quay nhiều vòng nhanh dần (đoạn vòng [V0, V1] của skill_01 lặp), ném, trói, giữ, cột lửa, thả, giật về
    V0_, V1_ = VONG
    dv = V1_ - V0_
    N_VONG = 3
    toc = [1.0, 1.25, 1.55]                                # vòng sau nhanh hơn
    T_A = V0_                                              # đoạn đầu của họ (giơ móc) giữ nguyên
    lich = []
    tt = T_A
    for k in range(N_VONG):
        lich.append((tt, tt + dv / toc[k]))
        tt += dv / toc[k]
    T_NEM2 = tt + (T_NEM - V1_)                            # đoạn ném của họ (V1 → 0,733) giữ nguyên tốc
    BAY_S = 0.16
    T_TROI = T_NEM2 + BAY_S
    T_COT = T_TROI + 0.40
    T_THA = T_COT + 1.10
    T_RUT_S1 = T_THA + 0.20
    T_VE_S = T_RUT_S1 + (T_VE - T_RUT1)
    D_SK = T_VE_S + (D_CAST - T_VE) + 0.10

    def u_skill(t):
        """giây của skill_01 cho giây t của chiêu cuối (−1 = đang ở đoạn giữ / trói)."""
        if t < T_A:
            return t
        for a_, b_ in lich:
            if t < b_:
                return V0_ + (t - a_) / (b_ - a_) * dv
        if t < T_NEM2 + 0.12:
            return V1_ + (t - lich[-1][1])
        if t < T_THA:
            return -1.0
        if t < T_RUT_S1:
            return T_RUT0 + (t - T_THA) / (T_RUT_S1 - T_THA) * (T_RUT1 - T_RUT0)
        return T_RUT1 + (t - T_RUT_S1)

    T_GIU = T_NEM + 0.12 + (T_NEM2 + 0.12 - T_NEM - 0.12)  # placeholder (không dùng)

    def skill(t, P):
        u = u_skill(t)
        if u < 0:                                           # giữ xích căng: dáng tay duỗi của họ (0,87–1,0) lặp chậm + giật giật
            k_ = (t - (T_NEM2 + 0.12))
            ug = 0.87 + 0.10 * (0.5 - 0.5 * math.cos(2 * math.pi * k_ / 0.9))
            dat(P, mau("skill_01", ug))
            hien_theo_ho(P, "skill_01", ug)
            giat = em((t - T_COT + 0.08) / 0.06) * (1 - em((t - T_COT) / 0.3))
            P.rot("bone3", -6.0 * giat + 1.5 * math.sin(2 * math.pi * 7 * t) * em((t - T_TROI) / 0.1))
            P.move("move", -8.0 * giat, 0.0)
        else:
            dat(P, mau("skill_01", u))
            hien_theo_ho(P, "skill_01", u)
        if t >= T_NEM2:
            bat_tat(P, XICH_DAI + tuple(s + "_sau" for s in SAU), 0.0)
            if t < T_NEM2 + BAY_S:
                q = em((t - T_NEM2) / BAY_S) ** 0.7
            elif t < T_THA:
                q = 1.0
            else:
                q = 1.0 - em((t - T_THA) / (T_RUT_S1 - T_THA))
            P_ve = Pose()
            dat(P_ve, mau("skill_01", T_VE))
            xich_bay(P, q, goc_moc_tay(P_ve), em((t - (T_THA + 0.6 * (T_RUT_S1 - T_THA))) / (0.4 * (T_RUT_S1 - T_THA))),
                     an_het=t >= T_VE_S)
            if T_TROI <= t < T_THA:                          # móc đã quấn đối thủ: VFX vẽ vòng xích; móc bay ẩn, xích căng giữ nguyên
                P.alpha["moc_bay"] = 0.0
        else:
            xich_bay(P, 0.0, an_het=True)
    ev = [(0.10, "lua_xich", ""), (T_A, "quay", ""), (T_NEM2, "nem", ""), (T_TROI, "troi", ""), (T_TROI + TRE_TRUNG, "trung", ""),
          (T_COT, "cot_lua", "")] + [(T_COT + 0.15 + 0.25 * k, "chay", "") for k in range(4)] + [(T_THA, "tha", ""), (T_THA + 0.02, "rut", ""),
                                                                                          (T_VE_S, "moc_ve", "")]
    out.append(Clip("skill", D_SK, skill, ev=ev, trung=T_COT + 0.15))
    print(f"  chiêu cuối {D_SK:.2f} s: quay {T_A:.2f}–{lich[-1][1]:.2f}, ném {T_NEM2:.2f}, trói {T_TROI:.2f}, cột lửa {T_COT:.2f}, thả {T_THA:.2f}")
    return out


def tim_vong():
    """đoạn vòng của skill_01 lúc quay xích: hai khung i < j (cách 6–16 khung, trong 4–21) có dáng tay + xích dài gần nhau nhất."""
    R = CD["skill_01"][1]
    keys = [b for b in R if b.startswith("bone14") or b in ("bone13", "rotate_01", "bone3", "bone9")]
    X = np.concatenate([R[b][:, :3] for b in keys], 1)
    best = None
    for i in range(4, 16):
        for j in range(i + 6, min(22, i + 17)):
            d = float(np.abs(X[j] - X[i]).mean())
            if best is None or d < best[0]:
                best = (d, i, j)
    print(f"  đoạn vòng skill_01: khung {best[1]}–{best[2]} ({best[1] / FPS:.3f}–{best[2] / FPS:.3f} s), lệch TB {best[0]:.2f}")
    return best[1] / FPS, best[2] / FPS


VONG = tim_vong()


def do_truc_moc(sk):
    """vòng cuối cán và giữa lưỡi của móc tay (hệ xương bone14b2), đo trên ảnh móc: điểm thấp nhất / xa nhất theo trục cán."""
    global MOC_TRUC
    at = sk.atts["W_wuqi"]
    r = list(at)[0]
    sp = at[r]
    im = np.asarray(sk.images[sp["path"]].convert("RGBA"))[..., 3] > 100
    Wi = sk.the_gioi()
    loc = np.array([np.linalg.solve(Wi["bone14b2"], np.array([v[0], v[1], 1.0]))[:2] for v in sp["V"]])
    uv = np.asarray(sp["uv"], float) * np.array([im.shape[1], im.shape[0]])
    M, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], loc, rcond=None)              # px ảnh → hệ bone14b2
    ys, xs = np.nonzero(im)
    P = np.c_[xs, ys, np.ones(len(xs))] @ M
    c = P.mean(0)
    # trục chính: hướng trải dài nhất; vòng cuối = đầu mút phía xa tâm lưỡi (lưỡi to nằm một đầu)
    u, s, vt = np.linalg.svd(P - c, full_matrices=False)
    ax = vt[0]
    pr = (P - c) @ ax
    dau_a, dau_b = P[pr < np.percentile(pr, 6)].mean(0), P[pr > np.percentile(pr, 94)].mean(0)
    # đầu có nhiều điểm ảnh gần nó hơn là lưỡi
    na = ((P - dau_a) ** 2).sum(1) < (0.25 * (s[0] / np.sqrt(len(P))) * 3) ** 2
    nb = ((P - dau_b) ** 2).sum(1) < (0.25 * (s[0] / np.sqrt(len(P))) * 3) ** 2
    vong, luoi_ = (dau_a, dau_b) if na.sum() < nb.sum() else (dau_b, dau_a)
    MOC_TRUC = (tuple(map(float, vong)), tuple(map(float, luoi_)))
    print(f"  trục móc (hệ bone14b2): vòng {MOC_TRUC[0][0]:.0f},{MOC_TRUC[0][1]:.0f} → lưỡi {MOC_TRUC[1][0]:.0f},{MOC_TRUC[1][1]:.0f}")


def main(a):
    global MOC_TRUC
    sk0, _ = dung_tam()
    do_truc_moc(sk0)
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
        sc_ = float(a[2]) if len(a) > 2 else 1.2
        im = ve.ve(fr[0], Bx, sc_, bg=(255, 255, 255), ss=2).convert("RGB")
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        im.save(a[1])
        json.dump(dict(box=list(Bx), scale=sc_), open(a[1][:-4] + ".json", "w"), indent=1)     # px ảnh = ((X − x0)·sc, (y1 − Y)·sc)
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
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: nuong(sk, c) for c in clips}
    xuat.xuat_het(sk, clips, RA, TEN, ("Quỷ xích dạng 1 non (quy_xich_non)" if NON else "Quỷ xích (quy_xich)") + ": tướng 5 đảo Kim"
                  + (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=("cast", "skill"), lao=(), far=("cast", "skill"), far_aim=("cast", "skill"),
                  cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  impact={"attack": (0.06, 0.32, 0.08), "skill": (0.24, 1.1, 0.2, "#ffb04a66")})


def dung_tam():
    """dựng nhanh (chưa có xích bay) chỉ để đo trục móc tay."""
    global them_xich_bay
    goc_fn = them_xich_bay
    them_xich_bay = lambda *a, **k: None  # noqa: E731
    try:
        return dung()
    finally:
        them_xich_bay = goc_fn


if __name__ == "__main__":
    main(sys.argv[1:])
