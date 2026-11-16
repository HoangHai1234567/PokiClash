# -*- coding: utf-8 -*-
"""Chiến binh sắt (chien_sat, tướng 2 đảo Kim): RESKIN trên rig con gốc monster_3348 (hiệp sĩ băng khiên + giáo).

- Xương: đủ mọi xương của họ + `move`; dáng gốc = khung 0 idle_01 (biến đổi riêng `l` đã áp ràng buộc, lấy mẫu bằng runtime Spine thật).
- Hình: MỖI hình của họ một hình của mình, NGUYÊN lưới của họ (điểm gắn theo ma trận dáng gốc trong att_goc.json), ảnh là mảnh đổi da vẽ
  trên đúng khung ảnh vùng (chien_sat_da.py to / cat).
- Thứ tự vẽ: của họ. open_01 đưa bàn tay ra trước mặt nạ: bốn slot bàn tay có bản `_t` (sau mặt nạ, trước khiên).
- Giáo: slot `wuqi_01` trên xương gốc `wuqi_01` (con của `bone`, IK của họ đã nướng). Clip tự dựng đặt giáo THEO TAY (`giao_theo_tay`):
  điểm nắm trong hệ bàn tay ↔ điểm đó trong hệ giáo lấy ở khung nguồn, góc giáo đặt theo thế giới → giáo không tuột khỏi tay.
- Clip: idle (idle_01 + mào lông lay thêm), walk (run_01), hit (hit_01), die (die_01 + mờ dần) = của họ. attack = skill_01_1 + lao tới
  (đỉnh lao đúng khung đâm). cast = ném giáo: lấy đà, phóng; giáo bay `giao_bay` trên `ten_0` con của `fly_0` (game dời `far`, co quãng,
  xoay theo hướng bay); giáo mọc lại trong tay. skill = giơ giáo (skill_01_2) gọi kim sắt, dậm giáo xuống đất (skill_02); kim sắt do code.
  appear = nhảy từ ngoài vào sàn, lộn trên không (open_01), đáp.

    chien_sat_rig.py                         dựng, xuất inbox/chien_sat_1/rig/
    chien_sat_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    chien_sat_rig.py kiem                    bước xoay lớn nhất giữa hai khung của từng clip
    CS_GOC=1 chien_sat_rig.py ...            dựng bằng DA GỐC (manh_goc/) ra rig_goc/: chỉ để soi clip trong máy, không đưa vào game
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
import chien_sat as G  # noqa: E402

GOC = os.environ.get("CS_GOC") == "1"
DANG = int(os.environ.get("CS_DANG") or "1")          # 1 = dạng đã duyệt (bám con gốc); 2 = dạng tiến hóa: cùng xương / lưới / clip, đổi tỉ lệ + da
BASE = G.BASE if DANG == 1 else os.path.join(os.path.dirname(G.BASE), "chien_sat_2")
TEN = "chien_sat" if DANG == 1 else "chien_sat_2"
RA = os.environ.get("CS_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("CS_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
if DANG == 2 and not os.path.isdir(MANH):
    MANH = os.path.join(G.BASE, "manh")                 # chưa có da dạng 2: dựng bố cục bằng da dạng 1
# DẠNG 2: bớt chibi, nặng nề hơn. Tỉ lệ đặt ở xương GỐC của từng bộ phận (con thừa hưởng, mảnh co / phóng quanh khớp, gốc vẫn dính):
# mũ (hujing_01, gốc ở cổ) nhỏ lại; mào (guan_01, con của mũ) to ra; hai giáp vai to ra. Không đụng chân, tay, khiên, giáo (chân chạm
# đất, giáo dựng đất phải trùng giáo gắn tay ở khung 0 idle).
TI_LE = {} if DANG == 1 else {"hujing_01": float(os.environ.get("CS_DAU") or 0.82), "guan_01": float(os.environ.get("CS_MAO") or 1.32),
                              "hujian_l_01": float(os.environ.get("CS_VAI") or 1.60), "hujian_r_01": float(os.environ.get("CS_VAI") or 1.60)}
RES = 2
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
TAY = ("xiaobi_r_02", "xiaobi_r_01", "sizhi_01", "damz_01")      # slot bàn tay có bản _t (trước mặt nạ) cho open_01
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
GIU_DICH = 0.4                # sau khi tới đích, xương giáo bay ở lại đích (đã ẩn) chừng này giây
TRE_TRUNG = 0.012             # khung trúng đặt SAU khung giáo tắt hẳn (game giữ dáng ở khung trúng; xem cung_lua_rig.py)
NANG_VAI = 26.0              # dạng 2: đỉnh giáp vai gần nhô quá mép trên khiên chừng này đơn vị (như concept B)
NEO_BAY = 0.62                # giáo bay: điểm neo (đi tới tâm đối thủ) ở 62 % thân giáo tính từ chuôi → mũi cắm sâu qua tâm


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung, đã áp ràng buộc)
def _cd():
    out = {}
    ia, ib = SL.index("xiaobi_r_02"), SL.index("hujing_01")
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
        truoc = [F["o"].index(ia) > F["o"].index(ib) for F in fr]              # bàn tay trước mặt nạ?
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
    """độ đậm mọi slot theo khung của họ; bốn slot bàn tay bật bản gốc hay bản _t theo thứ tự vẽ của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    _, _, truoc, hien = CD[clip]
    tr = truoc[i]
    for k, sl in enumerate(SL):
        if sl == "shadow":
            continue
        a = 1.0 if hien[i][k] > 0.5 else 0.0
        if sl in TAY:
            P.alpha[sl] = 0.0 if tr else a
            P.alpha[sl + "_t"] = a if tr else 0.0
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

    def gan(slot_ten, a, an):
        r = a["region"]
        im = anh_cua(r)
        wr, hr = imgs_ho[r].size
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

    # ---- trục giáo (từ ảnh vùng): chuôi → mũi, trong hệ xương wuqi_03 (giáo GẮN TAY: slot wuqi_02; mọi clip đòn của họ dùng bản này,
    # chỉ idle / block / stun dùng giáo dựng đất wuqi_01)
    a_g = by["wuqi_02"]
    uvg, _ = G.luoi(a_g)
    xyg = np.array(a_g["xy"], float).reshape(-1, 2)
    Mg, *_ = np.linalg.lstsq(np.c_[uvg, np.ones(len(uvg))], xyg, rcond=None)          # px ảnh vùng → thế giới dáng gốc của họ
    al = np.asarray(imgs_ho["wuqi_01"].convert("RGBA"))[..., 3] > 100
    ys, xs = np.nonzero(al)
    mui_px = np.array([xs[ys == ys.min()].mean(), ys.min()], float)
    chuoi_px = np.array([xs[ys == ys.max()].mean(), ys.max()], float)
    mui_w = np.array([*mui_px, 1.0]) @ Mg
    chuoi_w = np.array([*chuoi_px, 1.0]) @ Mg
    lm = np.linalg.solve(WG["wuqi_03"], np.array([*mui_w, 1.0]))[:2]
    lc = np.linalg.solve(WG["wuqi_03"], np.array([*chuoi_w, 1.0]))[:2]


    # ---- DẠNG 2: mảnh đổi dáng / mảnh mới là MẢNH CỨNG một xương, gen "đúng chỗ, đúng cỡ" trên concept (chien_sat_da2.py); toạ độ concept
    # → thế giới khung 0 idle qua bố cục dạng 2 (ảnh mẫu của concept: mau/bo_cuc.png + .json). Giáo mới căn theo TRỤC và CHUÔI của giáo cũ.
    MOI = {}
    if DANG == 2 and not GOC:
        moi = json.load(open(os.path.join(MANH, "moi.json")))
        bc = json.load(open(os.path.join(BASE, "mau", "bo_cuc.json")))
        x0b, _, _, y1b = bc["box"]
        scb = bc["scale"]
        bw, bh = Image.open(os.path.join(BASE, "mau", "bo_cuc.png")).size
        kk = 1000.0 / bh
        ox, oy = (1536 - round(bw * kk)) // 2, (1024 - round(bh * kk)) // 2
        s_px = 1.0 / (scb * kk)                                                         # đơn vị rig cho mỗi px concept

        def px2w(p_):
            return np.array([((p_[0] - ox) / kk) / scb + x0b, y1b - ((p_[1] - oy) / kk) / scb])

        for ten, d_ in moi.items():
            x_, y_, w_, h_ = d_["hop"]
            MOI[ten] = np.array([px2w((x_, y_)), px2w((x_ + w_, y_)), px2w((x_ + w_, y_ + h_)), px2w((x_, y_ + h_))])
        # giáo: trục ảnh mới (chuôi → mũi) đặt trùng trục giáo cũ, chuôi trùng chuôi
        gi = np.asarray(Image.open(os.path.join(MANH, "giao.png")).convert("RGBA"))[..., 3] > 100
        ys2, xs2 = np.nonzero(gi)
        m2 = np.array([xs2[ys2 == ys2.min()].mean(), -ys2.min()])
        c2 = np.array([xs2[ys2 == ys2.max()].mean(), -ys2.max()])
        aq = (m2 - c2) / np.hypot(*(m2 - c2))
        nq = np.array([-aq[1], aq[0]])
        Cw = (Wi["wuqi_03"] @ np.array([*lc, 1.0]))[:2]
        Lw = (Wi["wuqi_03"] @ np.array([*lm, 1.0]))[:2]
        uw = (Lw - Cw) / np.hypot(*(Lw - Cw))
        nw = np.array([-uw[1], uw[0]])
        hg, wg = gi.shape

        def q2w(qx, qy):
            d_ = np.array([qx, -qy]) - c2
            return Cw + s_px * (np.dot(d_, aq) * uw + np.dot(d_, nq) * nw)
        MOI["giao"] = np.array([q2w(0, 0), q2w(wg, 0), q2w(wg, hg), q2w(0, hg)])
        MOI["_giao"] = dict(c2=c2, m2=m2, aq=aq, nq=nq, s=s_px, wh=(wg, hg), mui_w=q2w(m2[0], -m2[1]))

    def gan_cung(slot_ten, ten_anh, bone, Vw, an):
        """mảnh cứng: ô 4 đỉnh (thế giới khung 0 idle) bám trọn một xương."""
        im = anh_cua(ten_anh)
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        rows = [[(bone, *map(float, np.linalg.solve(Wi[bone], np.array([v[0], v[1], 1.0]))[:2]), 1.0)] for v in Vw]
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.slot(slot_ten, bone, ten_anh, an=an)
        sk.atts[slot_ten][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": tris, "hull": 4, "V": np.array(Vw), "verts": rows,
                                      "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_anh)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)

    if MOI:
        # concept vẽ giáp vai gần đè lên chỗ dải trên của khiên (dải đó thuộc ảnh khiên của rig, vẽ trước vai): nâng giáp vai cho đỉnh nhô
        # quá mép trên khiên NANG_VAI đơn vị như concept; phần dưới của nó vẫn phủ vai (vẽ đủ phần khuất)
        _, Vd = hang(by["dun_01"], np.array(by["dun_01"]["xy"], float).reshape(-1, 2))
        d_ = Vd[:, 1].max() + NANG_VAI - MOI["vai_gan"][:, 1].max()
        print(f"  giáp vai gần: nâng {max(d_, 0):.1f} đơn vị")
        if d_ > 0:
            MOI["vai_gan"] = MOI["vai_gan"] + np.array([0.0, d_])
    THAY = {"wuqi_01": ("giao", "wuqi_01"), "wuqi_02": ("giao", "wuqi_03"), "wuqi_03": ("giao", "wuqi_04"), "hujian_l_01": ("vai_gan", "hujian_l_01")}
    for a in sorted(AG["atts"], key=lambda q: q["order"]):
        if MOI and a["slot"] in THAY:
            ten_a, xb = THAY[a["slot"]]
            gan_cung(a["slot"], ten_a, xb, MOI[ten_a], an=not hien0[a["slot"]])
        else:
            gan(a["slot"], a, an=not hien0[a["slot"]])
        if MOI and a["slot"] == "tou_01":                  # cánh thép bên trái mũ (dạng 2): sau vòm sau mũ, trước mào; giáp vai gần đè lên
            gan_cung("canh_mu", "canh_mu", "hujing_02", MOI["canh_mu"], an=False)
        if a["slot"] == "hujing_01":                       # bản _t của bàn tay: trước mặt nạ (open_01)
            for s_ in TAY:
                gan(s_ + "_t", by[s_], an=True)
    if MOI:
        lm = np.linalg.solve(Wi["wuqi_03"], np.array([*MOI["_giao"]["mui_w"], 1.0]))[:2]       # mũi giáo mới (dài hơn)
    sk.xuong("mui_giao", "wuqi_03", float(lm[0]), float(lm[1]))                        # mũi giáo gắn tay: chỗ VFX bám (gọi kim, chỗ dậm)

    # ---- giáo bay (cast): ảnh giáo nằm theo +x (chuôi → mũi), neo ở NEO_BAY thân giáo
    cao = float(max(sk.atts["guan_01"]["guan_01"]["V"][:, 1].max(), sk.atts["hujing_01"]["hujing_01"]["V"][:, 1].max()))
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    sk.xuong("fly_0", "root", 0.0, 0.0)
    sk.xuong("ten_0", "fly_0", 0.0, 0.0)
    if MOI:                                                                             # dạng 2: ảnh giáo mới
        gq = MOI["_giao"]
        wr, hr = gq["wh"]
        imw = anh_cua("giao")
        goc_px = np.array([[0, 0], [wr, 0], [wr, hr], [0, hr]], float)
        neo_q = gq["c2"] + NEO_BAY * (gq["m2"] - gq["c2"])
        Vb = np.array([[np.dot(np.array([p[0], -p[1]]) - neo_q, gq["aq"]) * gq["s"], np.dot(np.array([p[0], -p[1]]) - neo_q, gq["nq"]) * gq["s"]]
                       for p in goc_px])
        ten_bay = "giao"
        kg = gq["s"]
        neo, chuoi_px, u = neo_q, gq["c2"], gq["aq"]
    else:
        imw = anh_cua("wuqi_01")
        wr, hr = imgs_ho["wuqi_01"].size
        kg = float(np.hypot(*Mg[0]))                                                    # đơn vị thế giới cho mỗi px ảnh vùng
        u = (mui_px - chuoi_px) / np.hypot(*(mui_px - chuoi_px))
        n_ = np.array([-u[1], u[0]])
        neo = chuoi_px + NEO_BAY * (mui_px - chuoi_px)
        goc_px = np.array([[0, 0], [wr, 0], [wr, hr], [0, hr]], float)
        Vb = np.array([[np.dot(p - neo, u) * kg, -np.dot(p - neo, n_) * kg] for p in goc_px])
        ten_bay = "wuqi_01"
    sk.slot("giao_bay", "ten_0", ten_bay, an=True)
    sk.atts["giao_bay"][ten_bay] = {"type": "mesh", "path": ten_bay, "uv": goc_px / np.array([wr, hr], float),
                                    "tris": np.array([[0, 1, 2], [0, 2, 3]]), "hull": 4, "V": Vb,
                                    "verts": [[("ten_0", float(v[0]), float(v[1]), 1.0)] for v in Vb], "width": imw.width, "height": imw.height}
    for e, m in (("dam", "mũi giáo đâm tới"), ("trung", "khung trúng"), ("nem", "giáo rời tay (ném)"), ("moc", "giáo mọc lại trong tay"),
                 ("giuong", "giơ giáo lên"), ("trieu_hoi", "bắt đầu gọi kim sắt (VFX sinh kim trên đầu)"), ("dam_dat", "giáo dậm xuống đất"),
                 ("phong_kim", "kim sắt lao vào đối thủ (code lái)"), ("dap_dat", "chạm đất"), ("nga", "ngã gục")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    dai_giao = float(np.hypot(*(lm - lc)))
    return sk, dict(cao=cao, lm=lm, lc=lc, dai=dai_giao, neo_s=float(np.dot(neo - chuoi_px, u) * kg), kg=kg)


# ---------------------------------------------------------------- tiện ích
def dat_tg(sk, P, b, Mdes, W=None):
    """đặt xương b theo ma trận THẾ GIỚI mong muốn (chỉ xoay + dời; tỉ lệ 1); góc chọn cùng vòng với góc đang có."""
    W = W if W is not None else sk.the_gioi(P)
    bb = sk.bones[sk.bi[b]]
    Lp = np.linalg.solve(W[bb["parent"]], Mdes)
    g = P._g(b)
    goc = math.degrees(math.atan2(Lp[1, 0], Lp[0, 0])) - bb["rot"]
    goc -= 360.0 * round((goc - g[2]) / 360.0)
    g[0], g[1], g[2] = float(Lp[0, 2] - bb["x"]), float(Lp[1, 2] - bb["y"]), goc


def bay(sk, P, A, lech, q, goc0=None):
    """giáo bay ở quãng q (0..1) từ điểm A (thế giới, chỗ rời tay) tới far + lech; goc0: góc lúc rời tay (xoay dần sang hướng bay)."""
    far = sk.W0["far"][:2, 2]
    d = far + np.array(lech) - A
    an = not (0.0 <= q < 1.0 - 1e-6)
    q = min(max(q, 0.0), 1.0)
    Pd = A + q * d + np.array([0.0, 1.0]) * 22.0 * math.sin(math.pi * q)
    fly = q * far
    g = math.degrees(math.atan2(d[1], d[0]))
    if goc0 is not None:
        g0 = goc0 - 360.0 * round((goc0 - g) / 360.0)
        g = g0 + (g - g0) * em(q / 0.35)
    P.move("fly_0", float(fly[0]), float(fly[1]))
    P.move("ten_0", float(Pd[0] - fly[0]), float(Pd[1] - fly[1]))
    P.rot("ten_0", g)
    P.alpha["giao_bay"] = 0.0 if an else 1.0


def lam_clip(sk, info):
    out = []
    cao = info["cao"]

    # điểm nắm: gốc xương sizhi_01 (nắm tay) ở khung nguồn, trong hệ giáo của chính khung đó → đặt giáo theo tay ở khung tự dựng
    def nguon(clip, t):
        P0 = Pose()
        dat(P0, mau(clip, t))
        W = sk.the_gioi(P0)
        Wg = W["wuqi_01"]
        q = np.linalg.solve(Wg, np.array([*W["sizhi_01"][:2, 2], 1.0]))[:2]
        return goc_mat(Wg), q

    def giao_theo_tay(P, goc, q, W=None):
        W = W if W is not None else sk.the_gioi(P)
        h = W["sizhi_01"][:2, 2]
        c, s = math.cos(math.radians(goc)), math.sin(math.radians(goc))
        R = np.array([[c, -s], [s, c]])
        Md = np.eye(3)
        Md[:2, :2] = R
        Md[:2, 2] = h - R @ q
        dat_tg(sk, P, "wuqi_01", Md, W)

    def xoay_giao(P, goc_tg, w):
        """xoay giáo gắn tay (xương wuqi_03, gốc ở nắm tay) về góc THẾ GIỚI goc_tg, trộn w (0..1)."""
        if w <= 1e-4:
            return
        Wg = sk.the_gioi(P)["wuqi_03"]
        d = Wg[:2, :2] @ (info["lm"] - info["lc"])
        lech = goc_tg - math.degrees(math.atan2(d[1], d[0]))
        lech -= 360.0 * round(lech / 360.0)
        P.rot("wuqi_03", w * lech)

    def pha_goc(a, b, w):
        b = b - 360.0 * round((b - a) / 360.0)
        return a + (b - a) * w

    # ---- idle: của họ + mào lông ngựa lay thêm (hai nhịp mỗi vòng, trễ pha so với nhún của thân)
    D_ID = CD["idle_01"][0]

    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        hien_theo_ho(P, "idle_01", t, True)
        w = 2 * math.pi * 2.0 / D_ID
        P.rot("guan_01", 3.2 * math.sin(w * t - 0.9) + 1.2 * math.sin(2 * w * t + 0.4))
    out.append(Clip("idle", D_ID, idle, loop=True))

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        hien_theo_ho(P, "run_01", t, True)
        P.rot("guan_01", 4.0 * math.sin(2 * math.pi * t / CD["run_01"][0] - 1.2))
    out.append(Clip("walk", CD["run_01"][0], walk, loop=True))

    def hit(t, P):
        dat(P, mau("hit_01", t))
        hien_theo_ho(P, "hit_01", t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ---- ĐÁNH THƯỜNG: skill_01_1 của họ (thu giáo, đâm ngang, rút về) + LAO TỚI: đỉnh lao đúng khung mũi giáo vươn xa nhất
    tx = []
    for i in range(len(CD["skill_01_1"][2])):
        P0 = Pose()
        dat(P0, mau("skill_01_1", i / FPS))
        tx.append(sk.the_gioi(P0)["mui_giao"][0, 2])
    T_DAM = int(np.argmax(tx)) / FPS
    LAO = 0.55 * cao

    def lao_x(t):
        if t < 0.06:
            return 0.0
        if t < T_DAM:
            return LAO * em((t - 0.06) / (T_DAM - 0.06)) ** 1.4
        if t < T_DAM + 0.12:
            return LAO
        return LAO * (1 - em((t - T_DAM - 0.12) / 0.42))

    def attack(t, P):
        dat(P, mau("skill_01_1", t))
        hien_theo_ho(P, "skill_01_1", t)
        P.move("move", lao_x(t), 0.0)
    out.append(Clip("attack", CD["skill_01_1"][0], attack, ev=[(T_DAM - 0.03, "dam", ""), (T_DAM, "trung", "")], trung=T_DAM))

    # ---- CHIÊU MANA: NÉM GIÁO. Lấy đà chậm (dáng thu giáo của skill_01_1, ngả ra sau, nâng giáo chĩa chếch lên), giữ, phóng nhanh,
    # giáo rời tay đúng lúc tay vươn tới; tay không theo đà rồi về; giáo mọc lại trong tay.
    T_NEM, BAY_N, T_MOC, D_CAST = 27 / FPS, 6 / FPS, 1.22, 1.6
    U = [(0.0, 0.0), (0.38, 0.11), (0.80, 0.13), (T_NEM, T_DAM), (1.05, 0.44), (1.40, 0.80), (D_CAST, 1.0)]

    def tq(t, bang):
        for (a_, x), (b_, y) in zip(bang, bang[1:]):
            if t <= b_:
                return x + (y - x) * (t - a_) / (b_ - a_)
        return bang[-1][1]

    def cast_than(t, P):
        u = tq(t, U)
        dat(P, mau("skill_01_1", u))
        hien_theo_ho(P, "skill_01_1", u)
        nga = em(t / 0.38) * (1 - em((t - 0.80) / (T_NEM - 0.80)))                  # ngả ra sau lúc lấy đà
        toi = em((t - 0.80) / (T_NEM - 0.80)) * (1 - em((t - 1.05) / 0.4))          # chúi tới lúc phóng
        P.rot("st_02", 12.0 * nga - 7.0 * toi)
        P.rot("dabi_r_01", 48.0 * nga - 6.0 * toi)                                 # tay nâng cao ra sau
        P.rot("xiaobi_r_02", 18.0 * nga)
        xoay_giao(P, 22.0, nga)                                                     # mũi giáo vẫn chĩa tới, chếch lên
        run = em((t - 0.42) / 0.15) * (1 - em((t - 0.78) / 0.04))
        P.rot("st_03", 1.2 * run * math.sin(2 * math.pi * 12 * t))
        P.move("move", -10.0 * nga + 14.0 * toi, 0.0)
        return u, nga

    def giao_tg(W):
        """(điểm neo giáo bay, góc giáo) của giáo gắn tay ở tư thế W."""
        Wg = W["wuqi_03"]
        A = (Wg @ np.array([*(info["lc"] + (info["lm"] - info["lc"]) * NEO_BAY), 1.0]))[:2]
        d = Wg[:2, :2] @ (info["lm"] - info["lc"])
        return A, math.degrees(math.atan2(d[1], d[0]))

    P_ = Pose()
    cast_than(T_NEM, P_)
    A_N, g_rel = giao_tg(sk.the_gioi(P_))

    def cast(t, P):
        u, nga = cast_than(t, P)
        if t >= T_NEM:                                                              # tay không sau khi ném; giáo mọc lại trong tay
            k = em((t - T_MOC) / 0.16)
            P.alpha["wuqi_02"] = 1.0 if k > 0 else 0.0
            if k > 0:
                P.scale("wuqi_03", k * (1 + 0.12 * math.sin(math.pi * k)))
        if T_NEM <= t < T_NEM + BAY_N + GIU_DICH:
            bay(sk, P, A_N, (0.0, 0.0), (t - T_NEM) / BAY_N, goc0=g_rel)
    out.append(Clip("cast", D_CAST, cast, ev=[(T_NEM, "nem", ""), (T_NEM + BAY_N + TRE_TRUNG, "trung", ""), (T_MOC, "moc", "")],
                    trung=T_NEM + BAY_N + TRE_TRUNG))

    # ---- CHIÊU CUỐI: giơ giáo lên trời (skill_01_2) gọi kim sắt, giữ, nhón lên lấy đà, DẬM giáo xuống đất (skill_02), giữ, về.
    T_GIO = 0.44                    # giây của skill_01_2 ở dáng giáo dựng cao
    T_DAMD = 0.45                   # giây của skill_02 ở dáng giáo cắm đất
    A1, A2, A3, A4, A5, D_SK = 0.42, 1.25, 1.42, 1.52, 2.0, 2.45
    KHIEN = ("dun_01", "dun_02", "dun_03", "dun_04", "hujian_l_01")

    def skill(t, P):
        if t < A1:                                                                  # giơ giáo
            d_ = mau("skill_01_2", T_GIO * em(t / A1) ** 0.9)
            src = ("skill_01_2", T_GIO * em(t / A1) ** 0.9)
        elif t < A3:                                                                # giữ (gọi kim), rồi nhón lấy đà
            d_ = mau("skill_01_2", T_GIO)
            src = ("skill_01_2", T_GIO)
        elif t < A4:                                                                # dậm xuống
            w = em((t - A3) / (A4 - A3))
            d_ = pha(mau("skill_01_2", T_GIO), mau("skill_02", T_DAMD), w)
            src = None
        elif t < A5:                                                                # giữ cắm đất
            d_ = mau("skill_02", T_DAMD + 0.08 * min(1.0, (t - A4) / 0.3))
            src = ("skill_02", T_DAMD + 0.08 * min(1.0, (t - A4) / 0.3))
        else:                                                                       # về
            w = em((t - A5) / (D_SK - A5))
            d_ = pha(mau("skill_02", T_DAMD + 0.08), mau("idle_01", 0.0), w)
            src = None
        if t >= A3:                                                                 # khiên giữ trước người (skill_02 giơ khiên lên đầu)
            w_k = em((t - A3) / (A4 - A3))
            for b_ in KHIEN:
                if b_ in d_:
                    d_[b_] = d_[b_] * (1 - w_k) + np.array([0, 0, 0, 1, 1.0]) * w_k
        dat(P, d_)
        hien_theo_ho(P, "skill_01_2", min(t, T_GIO))
        g_gio = em((t - A1) / 0.15) * (1 - em((t - A3) / 0.05))
        P.rot("st_03", 1.4 * g_gio * math.sin(2 * math.pi * 13 * t) * (0.5 + 0.5 * min(1.0, (t - A1) / (A2 - A1))))
        nhon = em((t - A2) / (A3 - A2)) * (1 - em((t - A3) / 0.06))
        P.move("bone", 0.0, 10.0 * nhon)
        P.rot("dabi_r_01", 8.0 * nhon)
        dam = em((t - A4) / 0.04) * (1 - em((t - A4 - 0.08) / 0.35))               # thụp người lúc dậm
        P.move("bone", 0.0, -9.0 * dam)
        P.rot("guan_01", 6.0 * dam * math.sin(2 * math.pi * 6 * (t - A4)) - 4.0 * g_gio * math.sin(2 * math.pi * 3 * t))
    out.append(Clip("skill", D_SK, skill, ev=[(0.05, "giuong", ""), (A1, "trieu_hoi", ""), (A4, "dam_dat", ""), (A4 + 0.06, "phong_kim", ""),
                                             (A4 + 0.30, "trung", "")], trung=A4 + 0.30))

    # ---- APPEAR: nhảy từ ngoài (sau, trái) vào sàn, lộn trên không theo open_01, đáp, đứng vào thế
    T0_OP, T_CHAM_OP = 0.42, 1.42           # đoạn bay của open_01 (rời đất → chạm đất)
    D_AP = 1.55

    def appear(t, P):
        u = T0_OP + (t / 0.95) * (T_CHAM_OP - T0_OP) if t < 0.95 else T_CHAM_OP + (t - 0.95) * (2.233 - T_CHAM_OP) / (D_AP - 0.95)
        dat(P, mau("open_01", u))
        hien_theo_ho(P, "open_01", u)
        P.alpha["wuqi_02"] = 1.0
        # open_01 của họ để tay KHÔNG cầm giáo tới giây 2,0 (góc xương giáo lúc đó vô nghĩa): giữ giáo theo góc thế giới (chếch lên lúc
        # bay, dựng thẳng khi đáp) tới khi clip của họ hiện giáo lại, rồi mới trả về góc của clip
        xoay_giao(P, 70.0 + 18.0 * em((t - 0.95) / 0.2), 1.0 - em((u - 1.97) / 0.15))
        if t < 0.95:
            q = t / 0.95
            P.move("move", -1.05 * cao * (1 - q) ** 1.2, 0.35 * cao * math.sin(math.pi * q) * (1 - q))
        a_ = min(1.0, t / 0.06)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(0.95, "dap_dat", "")]))

    # ---- DIE: die_01 của họ (lảo đảo, đổ sấp, khiên úp) + mờ dần
    D_DIE = CD["die_01"][0] + 0.45

    def die(t, P):
        dat(P, mau("die_01", t))
        hien_theo_ho(P, "die_01", t)
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.70, "nga", "")]))
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
    if a and a[0] == "bo_cuc":                # hình bố cục: khung 0 idle trên nền trắng (ảnh mẫu tỉ lệ cho concept dạng sau)
        fr = hoat.nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.10)
        sc_ = float(a[2]) if len(a) > 2 else 2.0
        im = ve.ve(fr[0], Bx, sc_, bg=(255, 255, 255), ss=2).convert("RGB")
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        im.save(a[1])
        json.dump(dict(box=list(Bx), scale=sc_), open(a[1][:-4] + ".json", "w"), indent=1)     # ảnh px = ((X − x0)·sc, (y1 − Y)·sc)
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
    if a and a[0] == "nhe":                   # CS_DANG=2: ghi bản để dạng 1 gộp tiến hóa (rig + khung 0 idle + chiều cao)
        import pickle
        idle_ = [c for c in clips if c.ten == "idle"][0]
        os.makedirs(RA, exist_ok=True)
        sk_c = [c for c in clips if c.ten == "skill"][0]
        pickle.dump((sk, hoat.nuong(sk, idle_)[0], info["cao"], hoat.nuong(sk, sk_c)), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    M, noi = sk, {}
    BASE2 = os.path.join(os.path.dirname(G.BASE), "chien_sat_2")
    if DANG == 1 and not GOC and os.path.exists(os.path.join(BASE2, "manh", "moi.json")) and os.environ.get("CS_TIENHOA", "1") == "1":
        # TIẾN HÓA nối liền (quai/tienhoa.py): gộp rig dạng 2 (dựng ở tiến trình riêng: cấu hình theo dạng đọc lúc nạp mô-đun).
        # Ý "rèn lại giáp": dạng 1 cắm giáo, thụp xuống gồng, run, mào giật; đổi dạng lúc gồng mạnh nhất; dạng 2 hiện ra ưỡn ngực đứng
        # vào thế, mào bung rồi lắng về dáng nghỉ của dạng 2.
        import pickle
        import subprocess
        from quai import tienhoa
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, CS_DANG="2", CS_RA="", CS_MANH=""),
                       check=True)
        sk2, idle2, cao2, skill2 = pickle.load(open(os.path.join(BASE2, "rig", "_nhe.pkl"), "rb"))
        ti = info["cao"] / cao2
        M = tienhoa.gop(sk, sk2)
        chung = 0
        for nm in list(sk2.images):                       # ảnh dạng 2 trùng từng điểm ảnh dạng 1 (áo lót đen, cẳng tay) thì dùng chung
            if nm in sk.images and sk.images[nm].size == sk2.images[nm].size and \
                    np.array_equal(np.asarray(sk.images[nm]), np.asarray(sk2.images[nm])):
                M.images.pop("n_" + nm, None)
                for sl in M.atts.values():
                    for sp in sl.values():
                        if sp.get("path") == "n_" + nm:
                            sp["path"] = nm
                chung += 1
        print(f"  gộp tiến hóa: {chung} / {len(sk2.images)} ảnh dùng chung với dạng 1")
        # Ý "giơ giáo, rèn lại giáp": dạng 1 giơ giáo lên trời (động tác giơ của chiêu cuối), gồng run mạnh dần, mào giật; đổi dạng ở đỉnh
        # (VFX lốc / chớp của game che chỗ đổi, sự kiện doi_dang); dạng 2 hiện ra ĐÚNG dáng giơ giáo của chiêu cuối dạng 2, nhón rồi DẬM
        # giáo xuống đất (sự kiện gam), giữ, rồi hoà về khung 0 idle dạng 2.
        skill_c = [c for c in clips if c.ten == "skill"][0]
        A1_, A2_, A4_, A5_ = 0.42, 1.25, 1.52, 2.0                  # mốc của clip skill (như lam_clip)
        T_DAM_EV = 1.86

        def gong(t, P):
            ts = A1_ * em(t / 0.45)
            skill_c.fn(ts, P)
            g = em((t - 0.40) / 0.7)
            P.rot("st_03", 1.8 * g * math.sin(2 * math.pi * 14 * t))
            P.move("bone", 1.8 * g * math.sin(2 * math.pi * 11 * t), 3.0 * g)
            P.rot("guan_01", 8.0 * g * math.sin(2 * math.pi * 9 * t))

        def bung(t, P, fl):
            if t < 1.55:
                tb = A1_
            elif t < T_DAM_EV:
                tb = A2_ + (A4_ - A2_) * (t - 1.55) / (T_DAM_EV - 1.55)
            else:
                tb = A4_ + (A5_ - A4_) * min(1.0, (t - T_DAM_EV) / 0.6)
            Q = skill2[min(len(skill2) - 1, int(round(tb * 30)))]
            for b_, v in Q.t.items():
                P.t["n_" + b_] = list(v)
            P.rot("n_guan_01", 6.0 * (1 - em((t - 1.3) / 0.4)) * math.sin(2 * math.pi * 7 * t))

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=bung, mem=[],
                                   ev=[(0.3, "tu_luc", ""), (1.2, "doi_dang", ""), (T_DAM_EV, "gam", "")])
        for e_, m_ in (("tu_luc", "tiến hóa: giơ giáo gồng"), ("doi_dang", "tiến hóa: đổi dạng"), ("gam", "tiến hóa: dạng mới dậm giáo")):
            M.su_kien(e_, m_)
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    # hoà 0,2 s cuối mỗi clip không lặp về khung 0 idle (như xuat.khop_cuoi) nhưng hai slot giáo ĐỔI BẬC ở khung cuối: clip đòn dùng
    # giáo gắn tay (wuqi_02), idle dùng giáo dựng đất (wuqi_01); hai cây trùng nhau ở khung 0 idle (lệch 0,2 px). Trộn độ đậm thì
    # 0,2 s cuối hiện hai cây giáo mờ chồng nhau.
    frames = {c.ten: hoat.nuong(M, c) for c in clips}
    idle0 = frames["idle"][0]
    GIAO = ("wuqi_01", "wuqi_02", "wuqi_03", "giao_bay")
    for c in clips:
        if c.loop or c.ten in ("die", "evolve"):
            continue
        fr = [P.copy() for P in frames[c.ten]]
        giu = [{s: P.alpha.get(s, 1.0 if s == "wuqi_01" else 0.0) for s in GIAO} for P in fr]
        hoat.khop_cuoi(fr, idle0, 0.2)
        for P, g in zip(fr[:-1], giu[:-1]):
            P.alpha.update(g)
        fr[-1].alpha.update({s: idle0.alpha.get(s, 1.0 if s == "wuqi_01" else 0.0) for s in GIAO})
        frames[c.ten] = fr
    if "evolve" in frames:
        fr = frames["evolve"]
        for i_, P in enumerate(fr):
            t_ = i_ / FPS
            aA = 1 - hoat.ease((t_ - 1.05) / 0.30)
            aB = hoat.ease((t_ - 1.12) / 0.33)
            cuoi = i_ == len(fr) - 1
            P.alpha.update({"wuqi_01": 0.0, "wuqi_02": aA if t_ > 0 else 0.0, "wuqi_03": 0.0, "giao_bay": 0.0,
                            "n_wuqi_01": 1.0 if cuoi else 0.0, "n_wuqi_02": 0.0 if cuoi else aB, "n_wuqi_03": 0.0, "n_giao_bay": 0.0})
        fr[0].alpha.update({"wuqi_01": 1.0, "wuqi_02": 0.0})                 # khung 0 = khung 0 idle dạng 1 (giáo dựng đất)
    xuat.xuat_het(M, clips, RA, TEN, f"Chiến binh sắt dạng {DANG} ({TEN}): tướng 2 đảo Kim" + (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=DANG, so_dang=2, noi_them=noi, dung_yen=("cast", "skill"), lao=(), far=("cast",), far_aim=("cast",),
                  cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0,
                  impact={"attack": (0.05, 0.25, 0.07), "skill": (0.22, 1.0, 0.18, "#e8eef666")} if DANG == 1 else
                  {"attack": (0.06, 0.32, 0.08), "skill": (0.26, 1.25, 0.2, "#f2f4f888")})


if __name__ == "__main__":
    main(sys.argv[1:])
