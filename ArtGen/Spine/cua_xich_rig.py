# -*- coding: utf-8 -*-
"""Tinh linh đuôi máy cưa (cua_xich, tướng 4 đảo Kim): RESKIN trên rig con gốc monster_3374.

- Xương: đủ mọi xương của họ + `move`, `far`, `vong` (vòng dây giật); dáng gốc = khung 0 idle_01 (biến đổi riêng `l` đã áp IK +
  transform, lấy mẫu bằng runtime Spine thật).
- Hình: mảnh K (cua_xich_manh.py: đuôi, đĩa, thân, chân, tay, mắt) dùng NGUYÊN lưới của họ. Mảnh đổi dáng (mai trước / sau, sừng, mặt,
  quặng) là lưới dày trên ảnh của mình, mỗi đỉnh gắn như điểm tương ứng trên lưới của part họ mà nó thay (gan_theo_goc). Vòng dây giật
  bám tay trái bằng một bộ trọng số đều (lấy ở tâm vòng); sợi dây là dải lưới, đầu lỗ bám thân, đầu vòng bám như vòng → kéo vòng ra là dây
  giãn theo.
- Thứ tự vẽ: của mình (quặng sau mặt, mặt sau hai tay như concept D3, mai trước trên cùng).
- Clip: idle, walk, hit, die = của họ.

    cua_xich_rig.py                         dựng, xuất inbox/cua_xich_1/rig/
    cua_xich_rig.py ghep                    khung 0 idle cạnh concept + chồng viền → rig/ghep.png
    cua_xich_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    CX_GOC=1 cua_xich_rig.py ...            dựng bằng DA GỐC (manh_goc/) ra rig_goc/: chỉ để soi clip trong máy
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
from quai.luoi import Luoi, luoi_vung  # noqa: E402
import cua_xich as G  # noqa: E402

GOC = os.environ.get("CX_GOC") == "1"
# DẠNG: "1" = dạng đã vào game (inbox/cua_xich_1); "2" = dạng tiến hóa trên CÙNG xương / lưới / clip (inbox/cua_xich_2): đổi tỉ lệ ở xương gốc
# từng bộ phận rồi chuyển da (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc"). Chưa có da dạng 2 thì dựng bằng da dạng 1 (bố cục).
DANG = os.environ.get("CX_DANG", "1")
BASE = os.path.join(os.path.dirname(G.BASE), "cua_xich_2") if DANG == "2" else G.BASE
TEN = "cua_xich_2" if DANG == "2" else "cua_xich"
RA = os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.path.join(BASE, "manh_goc" if GOC else "manh")
if DANG == "2" and not GOC and not os.path.isdir(MANH):
    MANH = os.path.join(G.BASE, "manh")


def _ti_le():
    """tỉ lệ nhân thêm vào xương (dạng 2). bone19 = thân (cha của đầu, tay, đuôi), bone7 = đầu, bone18 = gốc đuôi (cả chuỗi đuôi + đĩa),
    bone12 / bone15 = gốc tay. Đè bằng CX_TL="bone7=0.85,bone18=1.2"."""
    if DANG != "2":
        return {}
    # lần 2 (người dùng: "thích B hơn nhưng nhìn chưa đủ khác biệt, phải to hơn và chiến hơn"): thân 1,22, đuôi cưa 1,3, chân 1,25
    # (lần 1: thân 1,12, đầu 0,82, đuôi 1,12, tay 0,9, chân giữ nguyên)
    t = {"bone19": 1.22, "bone7": 0.8, "bone18": 1.3, "bone12": 0.88, "bone15": 0.88, "bone3": 1.25, "bone5": 1.25}
    for kv in filter(None, os.environ.get("CX_TL", "").split(",")):
        k, v = kv.split("=")
        t[k.strip()] = float(v)
    return t


TI_LE = _ti_le()
RES = 2
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
# part của họ không dùng: gai sau đầu (D3 không có), tinh thể loé (VFX ngoài rig), tay phía xa (người dùng 2026-11-16: "bỏ tay bên kia đi")
BO = ("jingkuai", "youshou")
# `youerduo` (mảng sẫm sau tinh thể = mặt XA của mũ) GIỮ: người dùng 2026-11-16 "ở giữa là giữa theo chiều ngang đầu, con gốc còn có 1 layer
# đầu sau nữa": quặng kẹp giữa lớp mai trước và lớp đầu sau; bỏ lớp sau thì quặng nằm ở mép xa của đầu, trông lệch hẳn sang bên kia.
# chỉnh chỗ mảnh đổi dáng (px concept, cộng vào 4 góc khung ảnh). Người dùng 2026-11-16: "quặng sắt phải ở giữa đầu, nhìn như này bị lệch
# sang bên kia quá": tâm cụm quặng (x 966) về tâm đầu (mặt tròn x 852)
# Lần 2 ("sửa lại cho chính giữa giống con gốc, xem lại con gốc đi"): dời ngang là sai. Tinh thể của họ xoè quạt ôm mép trên vòm mũ, chân
# nấp sau vòm, cái cao nhất ở đỉnh vòm; vòm mai của mình thấp hơn mũ họ ~90 px nên đặt như concept thì lộ cả thân cột, cụm treo lệch ra
# sau. Hạ 55 px + xoay 14° ngược kim quanh tâm đầu (900, 560): chân cột nấp sau mai, cột cao giữa đỉnh đầu (so 5 phương án cạnh con gốc).
# Lần 3 ("ở giữa là giữa theo chiều ngang đầu, con gốc còn có 1 layer đầu sau nữa"): cái thiếu là LỚP ĐẦU SAU (youerduo) chứ không phải
# chỗ đặt. Trả lớp sau về; cột quặng của mình mập hơn tinh thể của họ, che hết lớp sau → co 0,85 quanh (930, 480), hạ 30 px: quặng kẹp
# giữa mai trước và lớp sau, lớp sau lộ quanh như con gốc (so 4 phương án E–H cạnh con gốc).
CHINH_R = {"quang": (-10.0, 30.0, 0.0, 0.85, 930.0, 480.0),
           # tai xa (bản lật của đốt mai sau + sừng): nhích lên + ra ngoài 45 px cho sừng gỉ cam lộ sau quặng (so 3 phương án a–c)
           "tai_xa": (45.0, -45.0, 0.0, 1.0, 0.0, 0.0)}
# dạng đủ: (dx, dy, góc độ ngược kim trên màn hình, tỉ lệ, tâm xoay x, tâm xoay y) px concept; CX_QUANG="dx,dy,goc,s,cx,cy" để thử
if os.environ.get("CX_QUANG"):
    CHINH_R["quang"] = tuple(float(x) for x in os.environ["CX_QUANG"].split(","))
for _kv in filter(None, os.environ.get("CX_CHINH", "").split(";")):          # CX_CHINH="tai_xa=dx,dy,goc,s,cx,cy;quang=..."
    CHINH_R[_kv.split("=")[0]] = tuple(float(x) for x in _kv.split("=")[1].split(","))
# TAI XA (slot youerduo): bản đối xứng của tai gần (cua_xich_manh.tai_xa): "tai_xa" = đốt mai sau + sừng lật ngang, "tai_xa_s" = chỉ sừng,
# "" = tấm nhọn trơn K3 (người dùng 2026-11-16: "tai 2 bên không đồng bộ")
TAI = os.environ.get("CX_TAI", "tai_xa")
# mảnh đổi dáng: tên ảnh → slot của họ mà nó thay / bám theo lưới
DOI = {"quang": "tofa", "mat": "to_01", "mai_sau": "to_02", "sung": "zuoerduo", "mai_truoc": "to_02", "tay_trai": "zuoshou",
       "tay_phai": "youshou"}
# thứ tự vẽ của mình (sau → trước); tên slot của họ giữ nguyên, mảnh mới thêm tên riêng
# tay của D3 nhỏ, nằm TRƯỚC mặt, ôm đáy mặt: vẽ lại thành mảnh đổi dáng (R6) gắn theo lưới găng của họ (găng gốc to, mặt họ che nửa
# trên nên không dùng hình bóng găng). Vòng + dây sau mặt? Không: mặt vẽ trọn quả cầu, đáy che vòng → vòng, dây sau mặt nhưng trước tay.
THU_TU = ["weiba_04", "weiba_03", "juzi_04", "juzi_03", "weiba_02", "weiba_01", "youxiaotui2", "youdatui2", "shenti", "zuoxiaotui2",
          "zuodatui2", "zuodatui3", "youerduo", "tofa", "to_01", "day", "vong", "zuoshou", "yanjing_01", "yanjing_02", "mai_sau",
          "zuoerduo", "to_02"]
SLOT_DOI = {"tofa": "quang", "to_01": "mat", "mai_sau": "mai_sau", "zuoerduo": "sung", "to_02": "mai_truoc", "zuoshou": "tay_trai",
            "youshou": "tay_phai"}
if TAI and not GOC:
    SLOT_DOI["youerduo"] = TAI
    DOI[TAI] = "youerduo"


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
        hien = [[(F["n"][k] is not None) * float(F["a"][k]) for k in range(len(F["n"]))] for F in fr]
        ten = [list(F["n"]) for F in fr]
        out[clip] = (float(v["dur"]), res, hien, ten)
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


def nuong(sk, clip):
    """góc LIỀN MẠCH: mỗi khung chọn bội 360° gần khung trước nhất (đĩa cưa quay nhiều vòng)."""
    n = int(round(clip.dur * FPS)) + 1
    frames = []
    for i in range(n):
        P = Pose()
        clip.fn(min(clip.dur, i / FPS), P)
        frames.append(P)
    for i in range(1, n):
        Pp, Q = frames[i - 1], frames[i]
        for b, g in Q.t.items():
            a0 = Pp.t.get(b, [0, 0, 0, 1, 1])[2]
            g[2] -= 360.0 * round((g[2] - a0) / 360.0)
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
    """hình đang bật của từng slot theo khung của họ: mắt nhắm (yanjing_03), đùi đổi hình (skill_03)."""
    i = khung_ho(clip, t, lap)
    _, _, hien, ten = CD[clip]
    for k, sl in enumerate(SL):
        if sl in ("shadow",) + BO or k >= len(hien[i]):
            continue
        ds = sl if GOC else SLOT_DOI.get(sl, sl)
        a = 1.0 if hien[i][k] > 0.5 else 0.0
        P.alpha[ds] = a
        if ten[i][k] and sl in ("yanjing_02", "youdatui2", "zuodatui2", "zuodatui3"):
            P.att[sl] = ten[i][k]
    if not GOC:
        P.alpha["mai_sau"] = P.alpha.get("mai_truoc", 1.0)
        if clip.startswith("skill_03"):                      # quay người: bụng ra sau, vòng + dây lộ dưới mõm như khuyên mũi → ẩn
            u = (t % CD[clip][0]) if lap else t
            an = 0.05 < u < 0.55
            P.alpha["vong"] = 0.0 if an else 1.0
            P.alpha["day"] = 0.0 if an else 1.0


# ---------------------------------------------------------------- dựng
def manh_goc():
    """da gốc (chỉ để soi clip): mỗi vùng ảnh cắt theo lưới, phóng RES."""
    G._C.pop("att", None)
    G.nap("att_goc.json")
    os.makedirs(MANH, exist_ok=True)
    for a in AG["atts"]:
        p = os.path.join(MANH, a["region"] + ".png")
        if a.get("region") and not os.path.exists(p):
            im = G.part_goc(a)
            im.resize((im.width * RES, im.height * RES), Image.LANCZOS).save(p)


def dung():
    if GOC:
        manh_goc()
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    # sk_c: CÙNG xương nhưng KHÔNG đổi tỉ lệ (thế giới khung 0 idle của họ): toạ độ gắn của mảnh mới (moi.json, att_idle0) tính trong hệ
    # này thì mảnh co / phóng cùng xương ở dạng 2; V0 (dáng gắn) tính bằng Wi của bộ xương đã đổi tỉ lệ
    sk_c = Sk("_c")
    sk_c.xuong("root")
    sk_c.xuong("move", "root")
    for i, b in enumerate(I["bones"]):
        if b["name"] != "root":
            cha = NB[b["parent"]]
            z = L0[i]
            sk_c.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1], goc=z[2], dai=b["len"], sx=z[3], sy=z[4])
    Wc = sk_c.the_gioi()
    # chân dài ra (dạng 2: gốc đùi bone3 / bone5 nhân tỉ lệ) thì bàn chân tụt dưới đất: nâng tâm thân bone2 lên đúng phần chân dài thêm
    # (chiều cao hông so với đáy cẳng chân ở khung 0 idle × (k − 1)), đổi sang hệ của xương cha `bone`
    nang = np.zeros(2)
    kc = max(TI_LE.get("bone3", 1.0), TI_LE.get("bone5", 1.0))
    if kc != 1.0:
        day_chan = min(min(np.array(a["xy"], float).reshape(-1, 2)[:, 1]) for a in A0["atts"]
                       if a["slot"] in ("zuoxiaotui2", "youxiaotui2") and a.get("xy"))
        hong = (Wc["bone3"][1, 2] + Wc["bone5"][1, 2]) / 2
        nang = np.linalg.solve(Wc["bone"][:2, :2], np.array([0.0, (kc - 1.0) * (hong - day_chan)]))
        print(f"  chân ×{kc:.2f}: nâng thân {(kc - 1.0) * (hong - day_chan):.1f} đơn vị")
    for i, b in enumerate(I["bones"]):
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        z = L0[i]
        k_ = TI_LE.get(b["name"], 1.0)
        dx_, dy_ = (nang if b["name"] == "bone2" else (0.0, 0.0))
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0] + dx_, z[1] + dy_, goc=z[2], dai=b["len"], sx=z[3] * k_, sy=z[4] * k_)
    Wi = sk.the_gioi()
    sk.sk_c = sk_c
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hien0 = {SL[k]: v > 0.5 for k, v in enumerate(CD["idle_01"][2][0])}
    by_goc = {}
    for a in AG["atts"]:
        by_goc.setdefault(a["slot"], []).append(a)
    by0 = {a["slot"]: a for a in A0["atts"] if a.get("region")}
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

    def gan(slot_ten, a, an, them_slot=True):
        """nguyên lưới của họ (att_goc), ảnh của mình cùng tên vùng."""
        r = a["region"]
        im = anh_cua(r)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        if them_slot:
            sk.slot(slot_ten, rows[0][0][0], r, an=an)
        sk.atts[slot_ten][r] = {"type": "mesh", "path": r, "uv": uv, "tris": np.asarray(tris, int).reshape(-1, 3), "hull": len(uv),
                                "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, r)] = Luoi(uv * np.array([im.width, im.height], float), np.asarray(tris, int).reshape(-1, 3), len(uv), len(uv),
                                      im.width, im.height, ten=slot_ten)

    def ghi_luoi(slot, ten_anh, L, rows):
        im = sk.images[ten_anh]
        V0 = np.zeros((len(rows), 2))
        for i, row in enumerate(rows):
            for b, x, y, w in row:
                V0[i] += w * (Wi[b] @ np.array([x, y, 1.0]))[:2]
        uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
        sk.atts[slot][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V0,
                                  "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot, ten_anh)] = L

    def gan_theo_goc(slot, ten_anh, L, V, att):
        """mỗi đỉnh V (thế giới khung 0 idle) bám như điểm tương ứng trên lưới của họ (att ở khung 0 idle); ngoài lưới: như điểm gần nhất
        cộng nguyên độ lệch (skill mục 27, rua_lua_rig.gan_theo_goc)."""
        Q = np.array(att["xy"], float).reshape(-1, 2)
        tr = np.array(att["tris"]).reshape(-1, 3)
        Wg = [{NB[k]: w for k, w in ws if w > 0.002} for ws in att["w"]] if att.get("w") else [{att["bone"]: 1.0}] * len(Q)
        A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
        v0, v1 = B_ - A, C - A
        den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
        den = np.where(np.abs(den) < 1e-9, 1e-9, den)

        def gan_canh(p, a, b):
            d = b - a
            t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
            return np.hypot(*(p - (a + t[:, None] * d)).T), t
        inv, rows, ngoai, xa = {}, [], 0, 0.0
        for p in V:
            v2 = p - A
            b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
            b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
            b0 = 1 - b1 - b2
            ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
            lech = np.zeros(2)
            if len(ok):
                i = int(ok[0])
                be = (float(b0[i]), float(b1[i]), float(b2[i]))
            else:
                ngoai += 1
                best = None
                for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                    dist, t = gan_canh(p, pa, pb)
                    j = int(np.argmin(dist))
                    if best is None or dist[j] < best[0]:
                        w3 = [0.0, 0.0, 0.0]
                        w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                        best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
                dmin, i, be, c = best
                lech = p - c
                xa = max(xa, dmin)
            acc = {}
            for vi, bw in zip(tr[i], be):
                for n, w in Wg[vi].items():
                    e = acc.setdefault(n, [0.0, np.zeros(2)])
                    e[0] += bw * w
                    e[1] += bw * w * Q[vi]
            row = []
            for n, (w, q) in acc.items():
                if abs(w) < 1e-5:
                    continue
                n2 = "move" if n == "root" else n
                if n2 not in inv:
                    inv[n2] = np.linalg.inv(Wc[n2])          # toạ độ gắn trong hệ KHÔNG đổi tỉ lệ (dạng 2: mảnh co theo xương)
                g = q / w + lech
                lp = inv[n2] @ np.array([g[0], g[1], 1.0])
                row.append((n2, float(lp[0]), float(lp[1]), float(w)))
            tot = sum(r[3] for r in row) or 1.0
            rows.append([(n, x, y, w / tot) for n, x, y, w in row])
        ghi_luoi(slot, ten_anh, L, rows)
        return ngoai, xa

    def trong_so_tai(att, P):
        """bộ trọng số {xương: w} của lưới họ (att, khung 0 idle) tại điểm P."""
        Q = np.array(att["xy"], float).reshape(-1, 2)
        Wg = [{NB[k]: w for k, w in ws if w > 0.002} for ws in att["w"]] if att.get("w") else [{att["bone"]: 1.0}] * len(Q)
        d = np.hypot(*(Q - P).T)
        k = np.argsort(d)[:3]
        wk = 1.0 / np.maximum(d[k], 1e-3)
        acc = {}
        for j, w_ in zip(k, wk / wk.sum()):
            for n, w in Wg[j].items():
                acc[n] = acc.get(n, 0.0) + w * w_
        return {("move" if n == "root" else n): w / sum(acc.values()) for n, w in acc.items()}

    def gan_deu(slot, ten_anh, L, V, ts):
        inv, rows = {}, []
        for p in V:
            row = []
            for b, w in ts.items():
                if b not in inv:
                    inv[b] = np.linalg.inv(Wc[b])
                lp = inv[b] @ np.array([p[0], p[1], 1.0])
                row.append((b, float(lp[0]), float(lp[1]), float(w)))
            rows.append(row)
        ghi_luoi(slot, ten_anh, L, rows)

    MOI = {}
    if not GOC and os.path.exists(os.path.join(MANH, "moi.json")):
        MOI = json.load(open(os.path.join(MANH, "moi.json")))
    if "vong" in MOI:                                     # xương vòng dây: con của thân, ở tâm vòng
        tam = np.array(MOI["vong"]["the_gioi"], float).mean(0)
        lp = np.linalg.solve(Wc["bone19"], np.array([tam[0], tam[1], 1.0]))
        sk.xuong("vong_g", "bone19", float(lp[0]), float(lp[1]))
        sk_c.xuong("vong_g", "bone19", float(lp[0]), float(lp[1]))
        Wi = sk.the_gioi()
        Wc = sk_c.the_gioi()

    def hop_the_gioi(ten, im):
        """ảnh mảnh mới → hàm px ảnh → thế giới khung 0 idle (4 góc khung ảnh trong moi.json)."""
        c = np.array(MOI[ten]["the_gioi"], float)
        if ten in CHINH_R:                                 # px concept → đơn vị (trục y concept hướng xuống)
            import cua_xich_manh as M
            T_, Ti_, spx = M.phep_can()
            ch = tuple(CHINH_R[ten]) + (0.0, 1.0, 0.0, 0.0)[len(CHINH_R[ten]) - 2:] if len(CHINH_R[ten]) < 6 else tuple(CHINH_R[ten])
            dx, dy, goc_, s_, px_, py_ = ch
            P_ = T_(c)                                     # 4 góc trên khung concept (px, y xuống)
            if abs(goc_) > 1e-6 or abs(s_ - 1.0) > 1e-6:
                g_ = math.radians(-goc_)                   # y xuống: ngược kim trên màn hình = góc âm
                R_ = np.array([[math.cos(g_), -math.sin(g_)], [math.sin(g_), math.cos(g_)]])
                P_ = (P_ - np.array([px_, py_])) @ R_.T * s_ + np.array([px_, py_])
            c = Ti_(P_ + np.array([dx, dy]))
        ex = (c[1] - c[0]) / im.width
        ey = (c[3] - c[0]) / im.height
        return lambda p: c[0] + ex * p[0] + ey * p[1]

    for sl in THU_TU:
        if GOC:
            if sl in ("day", "vong", "mai_sau"):
                continue
            for a in by_goc.get(sl, []):
                if sl in sk.atts and a["region"] in sk.atts[sl]:
                    continue
                gan(sl, a, an=not hien0.get(sl, False), them_slot=sl not in sk.atts)
                if not a["cur"]:
                    continue
            continue
        if sl in SLOT_DOI:                                 # mảnh đổi dáng
            ten = SLOT_DOI[sl]
            if ten not in MOI:
                if sl in by_goc and os.path.exists(os.path.join(MANH, by_goc[sl][0]["region"] + ".png")):
                    print(f"  thiếu mảnh {ten}: dùng tạm mảnh K {by_goc[sl][0]['region']}")
                    gan(sl, by_goc[sl][0], an=False)
                else:
                    print(f"  thiếu mảnh {ten}")
                continue
            im = anh_cua(ten)
            f = hop_the_gioi(ten, im)
            L = luoi_vung(im, buoc_vien=8.0, buoc_trong=11.0, ten=ten, in_tk=False)
            V = np.array([f(p) for p in L.pts])
            sk.slot(ten, "move", ten)
            ng, xa = gan_theo_goc(ten, ten, L, V, by0[DOI[ten]])
            print(f"  {ten}: lưới {L.n} đỉnh theo {DOI[ten]}; {ng} đỉnh ngoài lưới gốc, xa nhất {xa:.0f}")
            continue
        if sl == "vong":
            if "vong" not in MOI:
                continue
            im = anh_cua("vong")
            f = hop_the_gioi("vong", im)
            L = luoi_vung(im, buoc_vien=8.0, buoc_trong=12.0, ten="vong", in_tk=False)
            V = np.array([f(p) for p in L.pts])
            # vòng treo ở BỤNG (xương vong_g, con của thân bone19); chỉ lúc giật dây mới dời cùng tay trái (keo). Bám tay qua trọng số thì
            # lúc quay người tay trái chạy lên cạnh sừng, dây kéo chéo ngang mặt.
            sk.slot("vong", "vong_g", "vong")
            gan_deu("vong", "vong", L, V, {"vong_g": 1.0})
            continue
        if sl == "day":
            if "day" not in MOI or "vong" not in MOI:
                continue
            them_day(sk, anh_cua, Wi, MOI, by0, trong_so_tai)
            continue
        if sl in by_goc:
            cur = [a for a in by_goc[sl] if a["cur"]] + [a for a in by_goc[sl] if not a["cur"]]
            for j, a in enumerate(cur):
                if not os.path.exists(os.path.join(MANH, a["region"] + ".png")):
                    print(f"  thiếu ảnh {a['region']} ({sl})")
                    continue
                gan(sl, a, an=not hien0.get(sl, False), them_slot=sl not in sk.atts)
    for e, m in (("trung", "khung trúng"), ("keo", "giật dây khởi động"), ("xi", "máy hắt hơi (khói nhỏ)"),
                 ("no", "máy cưa nổ máy (khói, rung)"), ("hut", "hút khí xung quanh (VFX)"), ("lao", "lao tới đối thủ"),
                 ("cua", "nhát cưa trúng (tia lửa)"), ("nga", "ngã")):
        sk.su_kien(e, m)
    cao = float(max(sp["V"][:, 1].max() for sn, sl_ in sk.atts.items() if sn not in ("day",) for sp in sl_.values()))
    sk.xuong("far", "root", 1.6 * cao, 0.42 * cao)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(cao=cao)


def them_day(sk, anh_cua, Wi, MOI, by0, trong_so_tai):
    """sợi dây giật: dải lưới trên MỘT xương riêng `day_g` (con của thân bone19, gốc ở LỖ bụng, trục x chĩa tới đáy vòng). Mỗi khung
    day_dat() xoay day_g hướng về vòng và giãn theo trục x tới đúng khoảng cách → bề ngang dây giữ nguyên dù dây đổi hướng (trọng số
    tuyến tính hai đầu thì bề ngang không xoay theo: kéo ngang là dải bẹp thành sợi chỉ). Ảnh: khúc GIỮA của sợi dây thẳng."""
    import cua_xich_manh as M
    T, Ti, spx = M.phep_can()
    lo = Ti(M.LO_DAY)[0]
    cv = np.array(MOI["vong"]["the_gioi"], float)
    day_vong = (cv[2] + cv[3]) / 2 * 0.6 + cv.mean(0) * 0.4          # gần đáy vòng (khuất sau móng tay)
    im = anh_cua("day")
    ts_v = {"vong_g": 1.0}                                         # đầu dây nối vào vòng (vòng treo ở bụng, giật thì theo tay)
    N = 8
    d = day_vong - lo
    L_ = float(np.hypot(*d))
    rong = 16.0 / spx                                              # bề ngang dây: 16 px concept → đơn vị
    # mọi toạ độ riêng tính trong bộ xương KHÔNG đổi tỉ lệ (sk.sk_c, cùng hệ với moi.json): dạng 2 thì dây, vòng co / phóng cùng thân
    sk_c = sk.sk_c
    Mb = sk_c.the_gioi()["bone19"]
    lp = np.linalg.solve(Mb, np.array([lo[0], lo[1], 1.0]))
    g_cha = math.degrees(math.atan2(Mb[1, 0], Mb[0, 0]))
    for s_ in (sk, sk_c):
        s_.xuong("day_g", "bone19", float(lp[0]), float(lp[1]), goc=math.degrees(math.atan2(d[1], d[0])) - g_cha, dai=L_)
    Wc2 = sk_c.the_gioi()
    Wd = Wc2["day_g"]
    # chiều dài trục x của day_g trong thế giới ứng với 1 đơn vị riêng (cha có tỉ lệ) → đặt đỉnh theo đơn vị riêng
    k_ = float(np.hypot(*(Wd[:2, :2] @ np.array([1.0, 0.0]))))
    Lr, rr = L_ / k_, rong / float(np.hypot(*(Wd[:2, :2] @ np.array([0.0, 1.0]))))
    vong_loc = {b: np.linalg.solve(Wc2[b], np.array([day_vong[0], day_vong[1], 1.0]))[:2] for b in ts_v}
    Wi2 = sk.the_gioi()
    sk.day_info = dict(L=Lr, w=ts_v, loc=vong_loc)
    V, uv, rows = [], [], []
    for k in range(N + 1):
        f = k / N
        for s in (-1, 1):
            x, y = Lr * f, s * rr / 2
            V.append((Wd @ np.array([x, y, 1.0]))[:2])
            uv.append([0.12 + 0.76 * f, 0.5 - s * 0.5])
            rows.append([("day_g", float(x), float(y), 1.0)])
    tris = []
    for k in range(N):
        a, b, c, e = 2 * k, 2 * k + 1, 2 * k + 2, 2 * k + 3
        tris += [[a, c, b], [b, c, e]]
    # hàng uv: ảnh dây nằm ngang, mép trên ảnh (uv y=0) ↔ phía −nrm; hull = vòng quanh dải
    uv = np.array(uv, float)
    hull = [2 * k for k in range(N + 1)] + [2 * k + 1 for k in range(N, -1, -1)]
    order = hull
    V = np.array(V)[order]
    uv = uv[order]
    rows = [rows[i] for i in order]
    remap = {o: i for i, o in enumerate(order)}
    tris = np.array([[remap[x] for x in t] for t in tris], int)
    V0 = np.zeros((len(rows), 2))
    for i, row in enumerate(rows):
        for b, x, y, w in row:
            V0[i] += w * (Wi2[b] @ np.array([x, y, 1.0]))[:2]
    sk.slot("day", "day_g", "day")
    sk.atts["day"]["day"] = {"type": "mesh", "path": "day", "uv": uv, "tris": tris, "hull": len(uv), "V": V0, "verts": rows,
                             "width": im.width, "height": im.height}
    sk.luoi[("day", "day")] = Luoi(uv * np.array([im.width, im.height], float), tris, len(uv), len(uv), im.width, im.height, ten="day")
    print(f"  day: dải {N} đốt, dài {L_:.1f} đơn vị lúc nghỉ")


# ---------------------------------------------------------------- clip
def goc_tich_phan(D, omega):
    """góc quay của đĩa = tích phân tốc độ omega(t) (độ / giây, âm = cùng chiều kim đồng hồ như con gốc)."""
    dt = 1.0 / 240
    ts = np.arange(0.0, D + dt, dt)
    g = np.concatenate([[0.0], np.cumsum(omega(ts[:-1]) * dt)])
    return lambda t: float(np.interp(t, ts, g))


def bump(t, a, b):
    """bướu êm 0 → 1 → 0 trên [a, b] (tích phân = (b − a) / 2)."""
    if t <= a or t >= b:
        return 0.0
    return 0.5 - 0.5 * math.cos(2 * math.pi * (t - a) / (b - a))


def tq(t, bang):
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / (b_ - a_)
    return bang[-1][1]


def lam_clip(sk, info):
    out = []
    cao = info["cao"]
    # hướng giật dây (thế giới): tới trước, hơi lên; tay trái (bone12..14, kéo cả vòng theo) dời chừng ấy lúc giật hết
    KEO = np.array([0.44, -0.16]) * cao                    # ra trước, chúc xuống: tay đi DƯỚI mõm (giật lên thì vòng lên ngang mồm)

    def keo(P, p):
        if abs(p) < 1e-4:
            return
        M = sk.the_gioi(P)["bone19"][:2, :2]
        l_ = np.linalg.solve(M, KEO * p)
        P.move("bone12", float(l_[0]), float(l_[1]))
        if "vong_g" in sk.bi:                               # vòng đi cùng tay (cả hai là con của thân bone19)
            P.move("vong_g", float(l_[0]), float(l_[1]))
        P.rot("bone2", 2.5 * p)                           # ngả người ra sau theo cú giật

    def day_dat(P):
        """xoay xương dây day_g hướng về điểm nối ở đáy vòng (vòng bám tay trái qua trọng số) và giãn trục x tới đúng khoảng cách."""
        di = getattr(sk, "day_info", None)
        if not di:
            return
        W_ = sk.the_gioi(P)
        Wd = W_["day_g"]
        h = Wd[:2, 2]
        r = sum(w * (W_[b] @ np.array([*di["loc"][b], 1.0]))[:2] for b, w in di["w"].items())
        d = r - h
        a = math.degrees(math.atan2(d[1], d[0]) - math.atan2(Wd[1, 0], Wd[0, 0]))
        a -= 360.0 * round(a / 360.0)
        Lw = float(np.hypot(*(Wd[:2, :2] @ np.array([di["L"], 0.0]))))
        P.rot("day_g", a)
        P.scale("day_g", max(0.05, float(np.hypot(*d)) / max(Lw, 1e-6)), 1.0)

    def dia(P, g, k=1.0):
        """đặt góc đĩa cưa (đè góc của clip nguồn) và cỡ đĩa."""
        P._g("bone25")[2] = g
        if abs(k - 1.0) > 1e-4:
            P.scale("bone25", k, k)

    def rung(P, v, t, f=27.0):
        """máy nổ: thân, đuôi rung nhanh."""
        if v <= 1e-4:
            return
        P.move("bone2", 2.2 * v * math.sin(2 * math.pi * f * t), 1.4 * v * math.cos(2 * math.pi * (f + 4) * t))
        P.rot("bone18", 2.5 * v * math.sin(2 * math.pi * (f - 3) * t))

    def nen(clip, u, lap=False):
        d_ = mau(clip, u, lap)
        d_.pop("bone25", None)
        return d_

    # ---- IDLE: của họ + trò riêng: giữa chu kỳ máy cưa rồ lên một nhịp (đĩa quay nhanh, đuôi rung) rồi êm lại
    D_ID = CD["idle_01"][0]
    g_id = goc_tich_phan(D_ID, lambda ts: -360.0 - 1440.0 * np.array([bump(x, 3.5, 4.5) for x in ts]))   # 7 vòng + 2 vòng rồ = khép vòng

    def idle(t, P):
        dat(P, nen("idle_01", t, True))
        hien_theo_ho(P, "idle_01", t, True)
        dia(P, g_id(t % D_ID))
        rung(P, 0.8 * bump(t % D_ID, 3.5, 4.5), t)
    out.append(Clip("idle", D_ID, idle, loop=True))

    # ---- WALK: của họ + đuôi lắc theo bước, đĩa quay nhanh hơn chút
    D_W = CD["run_01"][0]

    def walk(t, P):
        dat(P, nen("run_01", t, True))
        hien_theo_ho(P, "run_01", t, True)
        dia(P, -720.0 * ((t % D_W) / D_W))                  # 2 vòng / bước: khép vòng
        P.rot("bone18", 4.0 * math.sin(2 * math.pi * t / D_W))
    out.append(Clip("walk", D_W, walk, loop=True))

    # ---- APPEAR: đứng nghỉ, cưa tắt; giật dây lần 1 (máy hắt hơi, đĩa nhích), giật lần 2 mạnh hơn → máy nổ, đĩa quay vọt, thân rung, rồi êm
    D_AP = 2.10
    Y1, Y2 = 0.32, 0.92                                     # lúc giật

    def p_keo(t, y, a):
        if t < y - 0.12:
            return 0.0
        if t < y:
            return -0.08 * a * em((t - (y - 0.12)) / 0.12)   # lấy đà: tay thu về
        if t < y + 0.11:
            return a * (-0.08 + 1.08 * em((t - y) / 0.11) ** 0.7)
        if t < y + 0.17:
            return a
        return a * (1 - em((t - y - 0.17) / 0.33))          # dây rút về

    g_ap = goc_tich_phan(D_AP, lambda ts: np.where(ts < Y2 + 0.14, 0.0,
                                                   -1800.0 * np.clip((ts - Y2 - 0.14) / 0.12, 0, 1) * (1 - 0.8 * np.clip((ts - 1.30) / 0.6, 0, 1))))

    def appear(t, P):
        dat(P, nen("idle_01", t, True))
        hien_theo_ho(P, "idle_01", t, True)
        keo(P, p_keo(t, Y1, 0.75) + p_keo(t, Y2, 1.0))
        g = -150.0 * em((t - Y1 - 0.12) / 0.22) * (1 - 0.3 * em((t - Y1 - 0.34) / 0.2)) + g_ap(t)   # hắt hơi: nhích rồi lùi nhẹ
        dia(P, g)
        rung(P, em((t - Y2 - 0.14) / 0.05) * (1 - em((t - 1.25) / 0.55)), t)
        rung(P, 0.5 * bump(t, Y1 + 0.12, Y1 + 0.34), t, 19.0)
        P.alpha["juzi_03"] = 0.0 if t < Y2 + 0.14 else 1.0  # vệt quay chỉ hiện khi máy đã nổ
        a_ = min(1.0, t / 0.08)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, appear, ev=[(Y1, "keo", ""), (Y1 + 0.12, "xi", ""), (Y2, "keo", ""), (Y2 + 0.14, "no", "")]))

    # ---- ĐÁNH THƯỜNG: húc = skill_01 của họ (lấy đà, chồm đầu tới lúc 0,47–0,53) + lao tới (move), đỉnh lao đúng lúc húc
    D_ATK = CD["skill_01"][0]
    T_HUC = 0.50
    LAO = 1.2 * cao

    def attack(t, P):
        dat(P, nen("skill_01", t))
        hien_theo_ho(P, "skill_01", t)
        P.alpha["jingkuai"] = 0.0
        dia(P, -900.0 * t)
        lao = LAO * em((t - 0.26) / (T_HUC - 0.26)) ** 1.4 * (1 - em((t - 0.60) / 0.45))
        P.move("move", lao, 0.0)
    out.append(Clip("attack", D_ATK, attack, ev=[(T_HUC, "trung", "")], trung=T_HUC))

    # ---- CHIÊU MANA: lao tới, quay người quật đuôi cưa (skill_03_1 của họ; cú quay của họ 2 khung → giãn ra 0,15 s), đĩa quay nhanh,
    # giữ đuôi một nhịp, quay về, lùi về chỗ
    U_C = [(0.0, 0.0), (0.24, 0.0), (0.39, 0.07), (0.47, 0.16), (0.72, 0.40), (0.97, 0.733)]
    T_QUAT = 0.47
    D_CAST = 1.40
    LAO_C = 0.9 * cao
    g_c = goc_tich_phan(D_CAST, lambda ts: -360.0 - 2500.0 * np.array([bump(x, 0.15, 1.05) for x in ts]) * 1.6)

    def cast(t, P):
        if t < 0.24 or t > 0.97:
            dat(P, nen("idle_01", 0.0 if t < 0.24 else t - 0.97, True))
            hien_theo_ho(P, "idle_01", 0.0)
            if t < 0.24:                                     # lấy đà: nén người
                k = bump(t, 0.0, 0.48)
                P.scale("bone2", 1.0 + 0.05 * k, 1.0 - 0.08 * k)
        else:
            u = tq(t, U_C)
            dat(P, nen("skill_03_1", u))
            hien_theo_ho(P, "skill_03_1", u)
        dia(P, g_c(t))
        lao = LAO_C * em((t - 0.08) / 0.34) * (1 - em((t - 0.75) / 0.42))
        P.move("move", lao, 0.0)
        rung(P, 0.6 * bump(t, T_QUAT - 0.03, T_QUAT + 0.25), t)
    out.append(Clip("cast", D_CAST, cast, ev=[(T_QUAT, "trung", ""), (T_QUAT, "cua", "")], trung=T_QUAT))

    # ---- CHIÊU CUỐI: giật dây ba lần (nhanh dần, máy rồ dần, đĩa to ra 1,35 lần), hút khí quanh, lao tới, quay người, ghì đuôi cưa vào
    # đối thủ cưa liên hồi (đuôi đẩy tới lui, rung), tia lửa mỗi nhát; quay về, lùi về, đĩa nhỏ lại
    KS = [(0.30, 0.8), (0.66, 0.9), (0.98, 1.0)]
    T_LAO0, T_GHI, T_NHA = 1.45, 1.78, 3.02
    D_SK = 3.90
    LAO_S = 0.9 * cao
    N_CUA = 11

    def om_sk(ts):
        w = np.full_like(ts, 0.0)
        for (y, _), v in zip(KS, (-700.0, -1600.0, -3400.0)):
            w = np.where(ts >= y + 0.10, v, w)
        tat = np.clip((ts - T_NHA - 0.25) / 0.6, 0, 1)
        return w * (1 - tat) + (-360.0) * tat
    g_s = goc_tich_phan(D_SK, om_sk)

    def k_dia(t):
        return 1.0 + 0.35 * em((t - 0.98) / 0.35) * (1 - em((t - T_NHA) / 0.4))

    U_S = [(T_LAO0, 0.0), (T_LAO0 + 0.15, 0.0), (T_LAO0 + 0.27, 0.07), (T_GHI, 0.16)]

    def skill(t, P):
        if t < T_LAO0 + 0.15:
            dat(P, nen("idle_01", t, True))
            hien_theo_ho(P, "idle_01", t, True)
            p = sum(p_keo(t, y, a) for y, a in KS)
            keo(P, p)
            if t > T_LAO0:                                   # lấy đà
                P.scale("bone2", 1.0 + 0.05 * bump(t, T_LAO0, T_LAO0 + 0.3), 1.0 - 0.08 * bump(t, T_LAO0, T_LAO0 + 0.3))
        elif t < T_GHI:
            u = tq(t, U_S)
            dat(P, nen("skill_03_1", u))
            hien_theo_ho(P, "skill_03_1", u)
        elif t < T_NHA:                                      # ghì cưa: dáng đuôi duỗi của họ (0,20–0,36) đẩy tới lui 3 nhịp / giây
            u = 0.28 + 0.08 * math.sin(2 * math.pi * 3.0 * (t - T_GHI))
            dat(P, nen("skill_03_1", u))
            hien_theo_ho(P, "skill_03_1", u)
            P.rot("bone26", 3.5 * math.sin(2 * math.pi * 13.0 * t))
        else:
            u = min(0.733, 0.40 + (t - T_NHA) / 0.30 * 0.333)
            dat(P, nen("skill_03_1", u) if u < 0.733 else nen("idle_01", t - T_NHA - 0.30, True))
            hien_theo_ho(P, "skill_03_1", u)
        dia(P, g_s(t), k_dia(t))
        v = min(1.0, max(0.0, -om_sk(np.array([t]))[0] / 3400.0))
        rung(P, (0.4 + 1.0 * (t >= T_GHI) * (t < T_NHA)) * v, t)
        lao = LAO_S * em((t - T_LAO0) / (T_GHI - T_LAO0)) * (1 - em((t - T_NHA - 0.05) / 0.42))
        P.move("move", lao, 0.0)
    ev = [(y, "keo", "") for y, _ in KS] + [(KS[-1][0] + 0.10, "no", ""), (1.05, "hut", ""), (T_LAO0 + 0.15, "lao", ""),
                                            (T_GHI, "trung", "")]
    ev += [(T_GHI + k * (T_NHA - T_GHI - 0.08) / (N_CUA - 1), "cua", "") for k in range(N_CUA)]
    out.append(Clip("skill", D_SK, skill, ev=ev, trung=T_GHI))

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
    for c in out:                                             # dây giật theo vòng ở mọi khung của mọi clip
        c.fn = (lambda f0: lambda t, P: (f0(t, P), day_dat(P)))(c.fn)
    return out


# ---------------------------------------------------------------- soi
def ghep(sk, clips):
    """khung 0 idle (bộ vẽ Python) cạnh concept cùng khung (phép căn của cua_xich_manh) + viền chồng."""
    import cua_xich_manh as M
    import cv2
    T, Ti, spx = M.phep_can()
    fr = nuong(sk, [c for c in clips if c.ten == "idle"][0])
    ve = soi.Ve(sk)
    # khung nhìn = cả khung concept đổi ra thế giới
    a = Ti(np.array([[0, 0], [M.W, M.H]], float))
    Bx = (float(a[0, 0]), float(a[1, 1]), float(a[1, 0]), float(a[0, 1]))
    im = ve.ve(fr[0], Bx, spx, bg=(255, 255, 255), ss=2).convert("RGB").resize((M.W, M.H), Image.LANCZOS)
    con = Image.open(M.CON).convert("RGB").resize((M.W, M.H), Image.LANCZOS)
    mr = M.mat_na(np.asarray(im))
    mc = M.mat_na(np.asarray(con))
    iou = (mr & mc).sum() / max(1, (mr | mc).sum())
    ov = np.asarray(im).copy()
    e = cv2.Canny((mc * 255).astype(np.uint8), 50, 150) > 0
    e = cv2.dilate(e.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    ov[e] = (230, 30, 30)
    out = Image.new("RGB", (M.W * 3 // 2, M.H // 2), "white")
    out.paste(con.resize((M.W // 2, M.H // 2), Image.LANCZOS), (0, 0))
    out.paste(im.resize((M.W // 2, M.H // 2), Image.LANCZOS), (M.W // 2, 0))
    out.paste(Image.fromarray(ov).resize((M.W // 2, M.H // 2), Image.LANCZOS), (M.W, 0))
    os.makedirs(RA, exist_ok=True)
    p = os.path.join(RA, "ghep.png")
    out.save(p)
    im.save(os.path.join(RA, "ghep_to.png"))
    print(p, f"IoU hình bóng với concept {iou:.3f}")


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "ghep":
        ghep(sk, clips)
        return
    if a and a[0] == "bo_cuc":                # hình bố cục: khung 0 idle nền trắng (ảnh mẫu tỉ lệ cho concept dạng khác)
        fr = nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.10)
        sc_ = float(a[2]) if len(a) > 2 else 1.6
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
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: nuong(sk, c) for c in clips}
    # khung vẽ trên sân (span, số lần chiều cao khai; game mặc định 3,4 = ±1,7 chiều cao quanh chân): cú lao trong rig + đuôi cưa vươn ở
    # chiêu cuối đi xa ~1,8 chiều cao → bị cắt dọc trong trận (tour KimFxTour 2026-11-16). Đo phạm vi ngang xa nhất của mọi clip, nới 8 %.
    ve = soi.Ve(sk)
    xa = max(max(abs(b[0]), abs(b[2])) for fr in frames.values() for b in (ve.bao(P) for P in fr[::2]))
    span = max(3.4, round(2 * xa / info["cao"] * 1.08, 2))
    print(f"  phạm vi ngang xa nhất {xa:.0f} đơn vị = {xa / info['cao']:.2f} chiều cao → span {span}")
    xuat.xuat_het(sk, clips, RA, TEN, "Tinh linh đuôi máy cưa (cua_xich): tướng 4 đảo Kim" + (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=(), lao=("cast", "skill"), far=(), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  impact={"attack": (0.06, 0.30, 0.08), "cast": (0.06, 0.30, 0.08), "skill": (0.10, 0.8, 0.10, "#ffd08a55")}, span=span)


if __name__ == "__main__":
    main(sys.argv[1:])
