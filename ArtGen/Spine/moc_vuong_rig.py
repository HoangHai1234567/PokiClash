# -*- coding: utf-8 -*-
"""Boss cuối đảo Mộc (moc_vuong): hình của mình chạy trên ĐÚNG rig của con gốc monster_3709. Ghi chú: inbox/moc_vuong_ghichu.md.

- XƯƠNG: đủ mọi xương của họ (trừ shadow), đúng cha – con, đơn vị × KG. Sáu xương của họ không thừa hưởng xoay của cha (inherit 2: bốn
  gốc cánh all38 / all155 / all63 / all127 và all12, all18): rig của mình chỉ có kiểu thừa hưởng thường, nên biến đổi riêng của sáu xương
  này tính ngược từ ma trận thế giới từng khung.
- MẢNH: mỗi slot dùng NGUYÊN lưới của họ (đỉnh, tam giác, uv, trọng số) với ảnh của mình vẽ đúng khung part (moc_vuong.anh_part: bản
  Codex ở manh/part, chưa có thì da tạm tô phẳng). Hai sừng là ô cứng của mình (sừng măng) bám xương sừng của họ. Mắt nhắm dựng bằng mã.
- THỨ TỰ VẼ ĐỔI GIỮA CLIP (.atomik không có): mỗi slot đổi chỗ có thêm slot SINH ĐÔI ở chỗ mới (tên <slot>~k), clip bật hình ở bản
  đúng chỗ, tắt bản kia (dãy slot là dãy chung ngắn chứa mọi thứ tự vẽ gặp trong các clip đã lấy mẫu).
- CHUYỂN ĐỘNG: mẫu 30 khung/giây của runtime Spine (biến đổi riêng ĐÃ áp IK và transform constraint): clip của họ
  (scan/sample_dk.json) và clip riêng dựng ở tầng điều khiển (moc_vuong_clip.py → scan/sample_moi.json).
Xương, lưới và chuyển động là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/moc_vuong_rig.py        → inbox/moc_vuong_1/rig/
    py -3 -I ArtGen/Spine/moc_vuong_rig.py soi <clip> <giây,giây,...> [tỉ lệ]                 → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import moc_vuong as MV  # noqa: E402

TEN = "moc_vuong_1"
RA = os.path.join(MV.BASE, "rig")
KG = 0.30                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = float(os.environ.get("MV_PXU", "0.40"))      # pixel ảnh atlas cho mỗi đơn vị rig con gốc (atlas của họ: 0,5)
CAO_KHAI = 1.12              # chiều cao khai cho game = chiều cao đo × hệ số này (khai lớn hơn thì game vẽ nhỏ lại)
BO_XUONG = ("shadow",)
BO_SLOT = ("wangge2", "shadow")
# (tên clip game, clip nguồn trong mẫu, lặp)
CLIPS = [("appear", "mv_appear", False), ("idle", "idle_01", True), ("walk", "mv_walk", True), ("fly", "mv_fly", True),
         ("attack", "skill_04", False), ("cast", "skill_02_1", False), ("skill", "mv_skill", False), ("hit", "hit_01", False),
         ("die", "die_01", False)]
# clip nguồn tạm khi clip riêng chưa dựng (để soi rig sớm)
TAM = {"mv_walk": "run_01"}
# sự kiện theo clip NGUỒN: (giây, tên, chuỗi)
SU_KIEN = {"skill_04": [(0.52, "chom", ""), (0.93, "dam", ""), (1.15, "trung", ""), (1.3, "gam", "")],
           "skill_02_1": [(0.2, "hit_hoi", ""), (0.62, "gam", ""), (1.25, "het_gam", "")]}
# hai sừng măng: (ô, xương sừng của họ, lùi gốc vào trong sọ (đơn vị), xoay thêm (độ), co theo chiều dài, co theo bề ngang)
SUNG = {"longjiao_01": ("sung_1", "jiao", 30.0, -8.0, 0.66, 0.82), "longjiao_02": ("sung_2", "jiao2", 26.0, -18.0, 0.66, 0.82)}


def _local(M2):
    """ma trận riêng 2x2 (N, 2, 2) → (xoay độ, tỉ lệ x, tỉ lệ y có dấu); phần xiên còn lại bỏ (trả kèm để báo)."""
    a, b, c, d = M2[..., 0, 0], M2[..., 0, 1], M2[..., 1, 0], M2[..., 1, 1]
    sx = np.hypot(a, c)
    rot = np.degrees(np.arctan2(c, a))
    det = a * d - b * c
    sy = det / np.maximum(sx, 1e-9)
    xien = (a * b + c * d) / np.maximum(sx * np.maximum(np.abs(sy), 1e-9), 1e-9)      # cos góc giữa hai trục
    return rot, sx, sy, xien


def _mat_l(l):
    """ma trận riêng 2x2 của Spine từ (xoay, tỉ lệ x, y, xiên x, y) (độ): la = cos(r + shx) sx, lb = cos(r + 90 + shy) sy, ..."""
    r, sx, sy, shx, shy = [l[..., i] for i in (2, 3, 4, 5, 6)]
    rx, ry = np.radians(r + shx), np.radians(r + 90.0 + shy)
    return np.stack([np.stack([np.cos(rx) * sx, np.cos(ry) * sy], -1), np.stack([np.sin(rx) * sx, np.sin(ry) * sy], -1)], -2)


def day_chung(orders):
    """dãy chung chứa mọi thứ tự vẽ (mỗi thứ tự là dãy con): ghép dần bằng dãy con chung dài nhất; phần tử phải lặp lại thành bản
    sinh đôi. Trả [(tên bản, tên slot gốc)]."""
    S = [(x, x) for x in orders[0]]
    dem = {}
    for O in orders[1:]:
        n, m = len(S), len(O)
        T = np.zeros((n + 1, m + 1), np.int32)
        for i in range(n - 1, -1, -1):
            si = S[i][1]
            for j in range(m - 1, -1, -1):
                T[i, j] = T[i + 1, j + 1] + 1 if si == O[j] else max(T[i + 1, j], T[i, j + 1])
        i = j = 0
        out = []
        while i < n and j < m:
            if S[i][1] == O[j]:
                out.append(S[i])
                i += 1
                j += 1
            elif T[i + 1, j] >= T[i, j + 1]:
                out.append(S[i])
                i += 1
            else:
                dem[O[j]] = dem.get(O[j], 1) + 1
                out.append((f"{O[j]}~{dem[O[j]]}", O[j]))
                j += 1
        out += S[i:]
        for x in O[j:]:
            dem[x] = dem.get(x, 1) + 1
            out.append((f"{x}~{dem[x]}", x))
        S = out
    return S


def nhung(S, O):
    """bản nào của từng slot đang bật khi thứ tự vẽ là O: khớp tham trái nhất trên dãy chung S. Trả {slot gốc: tên bản}."""
    r, i = {}, 0
    for x in O:
        while S[i][1] != x:
            i += 1
        r[x] = S[i][0]
        i += 1
    return r


def nap_mau(scan):
    S = json.load(open(os.path.join(scan, "sample_dk.json"), encoding="utf-8"))
    p = os.path.join(scan, "sample_moi.json")
    if os.path.exists(p):
        S.update(json.load(open(p, encoding="utf-8")))
    return S


def dung():
    scan = MV.SCAN
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    slots_goc = [s["name"] for s in I["slots"]]
    S = nap_mau(scan)
    can = {g for _, g, _ in CLIPS} | set(TAM.values()) | {"run_01", "fly_01", "skill_05", "skill_03"}
    S = {k: v for k, v in S.items() if k in can}

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này
    # ma trận thế giới dáng gốc ĐÃ ÁP RÀNG BUỘC của họ: điểm gắn lưới tính theo đây
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    dac_biet = [b["name"] for b in IB if b["inherit"]]
    goc0 = {}                                    # dáng gốc riêng của từng xương trong rig của mình: (x, y, xoay, sx, sy) đơn vị của họ
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_XUONG:
            continue
        cha = ten[b["parent"]]
        if b["inherit"]:
            L = np.linalg.inv(Wc[cha][:2, :2]) @ Wc[b["name"]][:2, :2]
            r, sx, sy, _ = _local(L[None])
            g = (b["x"], b["y"], float(r[0]), float(sx[0]), float(sy[0]))
        else:
            g = (b["x"], b["y"], b["rot"], b["sx"], b["sy"])
        goc0[b["name"]] = g
        sk.xuong(b["name"], "move" if cha == "root" else cha, g[0] * KG, g[1] * KG, goc=g[2], dai=b["len"] * KG, sx=g[3], sy=g[4])

    by = {a["att"]: a for a in D["atts"]}
    hinh = [a for a in sorted(D["atts"], key=lambda a: a["order"]) if a["slot"] not in BO_SLOT]
    co = {a["slot"] for a in hinh}
    # dãy slot chung cho mọi thứ tự vẽ gặp trong các clip dùng
    goc_o = [a["slot"] for a in hinh]
    thu_tu, khoa = [goc_o], {tuple(goc_o): 0}
    for clip, v in S.items():
        for F in v["frames"]:
            O = tuple(slots_goc[i] for i in F["o"] if slots_goc[i] in co)
            if O not in khoa:
                khoa[O] = len(thu_tu)
                thu_tu.append(list(O))
    day = day_chung(thu_tu)
    ban = [nhung(day, O) for O in thu_tu]        # cấu hình k: {slot gốc: tên bản đang bật}
    tam, tong, than = [], [0, 0], []

    def anh_cua(slot):
        a = by[slot]
        if slot in SUNG:
            g, la_tam = MV.anh_part(SUNG[slot][0])
        elif slot == "biyan":
            g, la_tam = mat_nham(), False
        else:
            g, la_tam = MV.anh_part(slot)
        if la_tam:
            tam.append(slot)
        g = g.convert("RGBa").resize((max(2, round(g.width / MV.Z * 2 * PXU)), max(2, round(g.height / MV.Z * 2 * PXU))), Image.LANCZOS).convert("RGBA")
        sk.anh(slot, anh.loang_mau(g))
        del a

    def gan(ban_, slot, bat):
        """một bản của slot (tên ban_) dùng nguyên lưới của họ; bat: bật mặc định."""
        a = by[slot]
        if slot not in sk.images:
            anh_cua(slot)
        im = sk.images[slot]
        sk.slot(ban_, "move", slot if bat else None)
        if slot in SUNG:                         # sừng măng: ô cứng bám xương sừng của họ
            o, xuong_, lui, xoay, co_d, co_r = SUNG[slot]
            _, _, g0, g1 = MV.o_sung(o)
            V = np.array(a["xy"], float).reshape(-1, 2)
            B = Wc[xuong_][:2, 2] / KG
            ngon = V[np.argmax(np.hypot(*(V - B).T))]
            huong = math.degrees(math.atan2(ngon[1] - B[1], ngon[0] - B[0])) + xoay
            k = im.width / (MV.o_sung(o)[1].shape[1])                        # px atlas / px ô
            u = np.array([math.cos(math.radians(huong)), math.sin(math.radians(huong))])
            P0 = (B - u * lui) * KG
            dat = Dat(float(P0[0]), float(P0[1]), goc=huong, ti=(KG / PXU * co_d, KG / PXU * co_r), neo=(float(g0[0] * k), float(g0[1] * k)), neo_px=True)
            L = luoi.luoi_o(im.width, im.height, 2, 2)
            sk.luoi_gan(ban_, slot, L, [{xuong_: 1.0}] * L.n, dat=dat)
            # điểm gắn theo ma trận ĐÃ áp ràng buộc
            Vw = dat.ra(L.pts, im.width, im.height)
            sk.atts[ban_][slot]["verts"] = [[(xuong_, *[float(v) for v in (np.linalg.inv(Wc[xuong_]) @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in Vw]
            tong[0] += L.n
            tong[1] += len(L.tris)
            return
        L = luoi.Luoi(np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3),
                      a["hull"], a["hull"], im.width, im.height, ten=ban_)
        V = np.array(a["xy"], float).reshape(-1, 2) * KG
        sk.luoi_gan(ban_, slot, L, trongso.cung(L.n, "move"), the_gioi=V)
        rows = []
        W_ = a.get("w") or [[(ten.index(a["bone"]), 1.0)]] * len(V)      # lưới không trọng số: bám trọn xương của slot
        for p, ws in zip(V, W_):
            row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
            tot = sum(r[3] for r in row) or 1.0
            rows.append([(n, x, y, w / tot) for n, x, y, w in row])
        sk.atts[ban_][slot]["verts"] = rows
        tong[0] += L.n
        tong[1] += len(L.tris)

    cur = {a["slot"]: a["cur"] for a in hinh}
    for ban_, slot in day:
        gan(ban_, slot, ban[0][slot] == ban_ and cur[slot])
        than.append(ban_)
    print(f"{len(sk.bones)} xương, {len(day)} slot ({len(day) - len(goc_o)} bản sinh đôi cho {len(thu_tu)} thứ tự vẽ), {tong[0]} đỉnh, "
          f"{tong[1]} tam giác" + (f"; DA TẠM {len(tam)} part" if tam else ""))

    # xương bám cho VFX: miệng (sóng âm), hai bàn chân trước (địa chấn), đỉnh đầu
    mom = np.array(by["tou_01"]["xy"], float).reshape(-1, 2)
    mui = mom[np.argmax(mom[:, 0] - 0.4 * mom[:, 1])] * KG                    # mũi mõm: điểm xa nhất về phải – dưới
    lp = np.linalg.solve(Wc["all8"], np.array([mui[0] - 14.0 * KG, mui[1] - 6.0 * KG, 1.0]))
    sk.xuong("mieng", "all8", float(lp[0]), float(lp[1]), goc=-math.degrees(math.atan2(Wc["all8"][1, 0], Wc["all8"][0, 0])) - 18.0)
    for nm, tgt in (("chan_tg", "all43"), ("chan_tx", "all46")):
        sk.xuong(nm, tgt, 0.0, 0.0)
    sk.xuong("far", "root", 2100.0 * KG, 420.0 * KG)
    for e, m in (("dam", "hai chân trước dậm xuống đất"), ("trung", "khung trúng: sét giáng xuống đối thủ (attack), lá chém tới (skill)"), ("chom", "chồm dựng, hai chân trước rời đất"), ("gam", "bắt đầu gầm (sóng âm)"),
                 ("het_gam", "hết gầm"), ("hit_hoi", "lấy hơi"), ("cham_dat", "đáp đất bằng bốn chân"), ("vo_canh", "một nhịp vỗ cánh"),
                 ("buoc", "một bàn chân chạm đất"), ("treo", "treo trên không, giương cánh lấy đà rơi"), ("sap", "sấp xuống xoè cánh sát đất"),
                 ("ken", "khép cánh trùm thân thành kén"), ("bung", "kén bung, bốn cánh dựng đứng")):
        sk.su_kien(e, m)
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=slots_goc, than=than, tam=tam, mau=S, goc0=goc0, dac_biet=dac_biet, khoa=khoa, ban=ban,
                    co=co, day=day)


def mat_nham():
    """mắt nhắm (slot biyan của họ, ô 16 x 12 phủ lên con mắt): miếng lông mực than + một nét mí cong. Cỡ ảnh vùng × Z."""
    m, _ = MV.bong_part("biyan", MV.Z * 4)
    h, w = m.shape
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([1, 1, w - 2, h - 2], fill=MV.PAL["nga"] + (255,))
    d.arc([w * 0.08, -h * 0.55, w * 0.92, h * 0.72], 20, 160, fill=MV.INK + (255,), width=max(2, h // 7))
    return im.resize((max(2, w // 4), max(2, h // 4)), Image.LANCZOS)


def chuyen_dong(sk, info):
    """{clip nguồn: (dài giây, {xương: mảng (số khung, 5) = xoay độ, dời x, y (đơn vị rig của mình), tỉ lệ x, y nhân}, [cấu hình thứ tự
    vẽ từng khung], [tên hình từng slot từng khung], [độ đậm])}: lệch của biến đổi riêng đã áp so với dáng gốc của rig mình."""
    IB, ten, goc0 = info["IB"], info["ten"], info["goc0"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n not in ("root",)]
    par = [b["parent"] for b in IB]
    db = {ten.index(n) for n in info["dac_biet"]}
    out = {}
    for clip, v in info["mau"].items():
        fr = v["frames"]
        Lr = np.array([F["l"] for F in fr], float)                    # (khung, xương, 7)
        M = np.array([F["m"] for F in fr], float).reshape(len(fr), -1, 2, 2)
        r, sx, sy, xien = _local(_mat_l(Lr))
        for i in db:                                                   # xương không thừa hưởng xoay: tính từ ma trận thế giới
            L = np.linalg.inv(M[:, par[i]]) @ M[:, i]
            r[:, i], sx[:, i], sy[:, i], xien[:, i] = _local(L)
        xm = float(np.abs(xien[:, ids]).max())
        res = {}
        for i in ids:
            g = goc0[ten[i]]
            A = np.stack([r[:, i] - g[2], (Lr[:, i, 0] - g[0]) * KG, (Lr[:, i, 1] - g[1]) * KG, sx[:, i] / (g[3] or 1.0), sy[:, i] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        cau_hinh = [info["khoa"][tuple(info["slots"][i] for i in F["o"] if info["slots"][i] in info["co"])] for F in fr]
        hinh = [F["n"] for F in fr]
        dam = [F["a"] for F in fr]
        out[clip] = (float(v["dur"]), res, cau_hinh, hinh, dam)
        if xm > 0.02:
            print(f"  chú ý: {clip} có xương xiên (cos góc hai trục tới {xm:.2f}); phần xiên bị bỏ")
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    slots, ban, day = info["slots"], info["ban"], info["day"]
    si = {n: i for i, n in enumerate(slots)}
    nhieu = {}                                                         # slot gốc → mọi bản của nó (chỉ slot có sinh đôi)
    for b_, s_ in day:
        nhieu.setdefault(s_, []).append(b_)
    nhieu = {k: v for k, v in nhieu.items() if len(v) > 1}
    mac_dinh = {b_: sk.slots[sk.si[b_]]["att"] for b_, _ in day}
    don = [s_ for b_, s_ in day if s_ not in nhieu]
    than = info["than"]
    # mảng dày (khung, xương, 5) cho từng clip nguồn: pha dáng, đổi nhịp, khép vòng bằng phép tính mảng
    bl = [b["name"] for b in sk.bones if b["name"] not in ("root", "move")]
    bx = {n: i for i, n in enumerate(bl)}
    DD = {}
    for clip, (dur, R, cau_hinh, hinh, dam) in CD.items():
        A = np.zeros((len(cau_hinh), len(bl), 5))
        A[:, :, 3:] = 1.0
        for b, v in R.items():
            A[:, bx[b]] = v
        DD[clip] = A

    def lay(goc, tau, lap=False):
        """dáng của clip nguồn ở giây tau: (mảng (xương, 5), cấu hình thứ tự vẽ, hình từng slot, độ đậm từng slot)."""
        dur, _, cau_hinh, hinh, dam = CD[goc]
        n = len(cau_hinh)
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0 + 1e-6
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        A = DD[goc]
        return [A[i0] * (1 - w) + A[i1] * w, cau_hinh[i0], hinh[i0], dam[i0]]

    def tron(d1, d2, w):
        """pha hai dáng (xoay theo đường ngắn); thứ tự vẽ, hình, độ đậm lấy của dáng nặng hơn."""
        if w <= 0:
            return d1
        if w >= 1:
            return d2
        V = d1[0] + (d2[0] - d1[0]) * w
        V[:, 0] = d1[0][:, 0] + ((d2[0][:, 0] - d1[0][:, 0] + 180.0) % 360.0 - 180.0) * w
        return [V] + (d2[1:] if w >= 0.5 else d1[1:])

    def ap(P, d, hien=1.0):
        V, k, H, A_ = d
        for i in np.flatnonzero((np.abs(V[:, :3]).max(1) > 1e-4) | (np.abs(V[:, 3:] - 1).max(1) > 1e-5)):
            v = V[i]
            b = bl[i]
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        for s_, ds in nhieu.items():                                   # slot có sinh đôi: bật đúng bản, tắt bản kia
            for b_ in ds:
                h_ = s_ if (ban[k][s_] == b_ and H[si[s_]]) else None
                if h_ != mac_dinh[b_]:
                    P.att[b_] = h_
        for s_ in don:
            h_ = s_ if H[si[s_]] else None
            if h_ != mac_dinh[s_]:
                P.att[s_] = h_
        if H[si["biyan"]]:
            P.alpha[ban[k]["biyan"]] = float(A_[si["biyan"]]) * hien
        if hien < 1.0:
            for sl in than:
                if not sl.startswith("biyan"):
                    P.alpha[sl] = hien

    def dat_dang(P, goc, tau, lap):
        ap(P, lay(goc, tau, lap))

    em = lambda x: (lambda q: q * q * (3 - 2 * q))(min(1.0, max(0.0, x)))      # noqa: E731
    ra = lambda x, k=2.0: 1 - (1 - min(1.0, max(0.0, x))) ** k                 # noqa: E731
    vao = lambda x, k=2.0: min(1.0, max(0.0, x)) ** k                          # noqa: E731

    def moc(ds, t):
        """nội suy thẳng theo các mốc [(t, giá trị)]."""
        if t <= ds[0][0]:
            return ds[0][1]
        for (a_, x), (b_, y) in zip(ds, ds[1:]):
            if t <= b_:
                return x + (y - x) * (t - a_) / (b_ - a_)
        return ds[-1][1]

    # ---------------------------------------------------------------- APPEAR: bay vào → treo một nhịp → RƠI MẠNH đáp bốn chân
    # Nguồn: run_01 của họ (nhún – bật lên không – xoè cánh lượn – giương cánh – rơi – đáp cúi thấp – về). Lấy từ lúc đã rời đất, đổi
    # nhịp: lượn vào chậm dần, treo giương cánh (lấy đà), rơi nhanh; cả con dời thêm trên xương move theo đường bay từ trên – sau tới.
    AP_VAO, AP_TREO, AP_ROI = 0.58, 0.80, 0.91
    R_DAP = 0.80                                                       # giây chạm đất trong run_01
    AP_DUR = AP_ROI + (CD["run_01"][0] - R_DAP)
    AP_X, AP_Y = -1180.0 * KG, 560.0 * KG

    def appear(t, P):
        if t < AP_VAO:
            tau = 0.37 + (0.585 - 0.37) * ra(t / AP_VAO, 1.5)
        elif t < AP_TREO:
            tau = 0.585 + (0.675 - 0.585) * em((t - AP_VAO) / (AP_TREO - AP_VAO))
        elif t < AP_ROI:
            tau = 0.675 + (R_DAP - 0.675) * vao((t - AP_TREO) / (AP_ROI - AP_TREO), 1.7)
        else:
            tau = R_DAP + (t - AP_ROI)
        ap(P, lay("run_01", tau), hien=min(1.0, t / 0.14))
        u = ra(t / AP_VAO, 2.2)
        P.move("move", AP_X * (1 - u), AP_Y * (1 - u) ** 1.3)
        if t >= AP_ROI:                                                # bẹp lúc chạm đất rồi bật lại
            r = t - AP_ROI
            e = math.exp(-r * 11.0) * math.cos(r * 24.0)
            P.scale("move", 1.0 + 0.055 * e, 1.0 - 0.075 * e)

    # ---------------------------------------------------------------- FLY (lặp): vỗ cánh bay lượn tại chỗ
    # Nguồn: fly_01 của họ (lao chéo qua màn hình, một nhịp vỗ cánh ở 0,5 → 1,3 s). Bỏ đường bay (dời của all2 và bốn đích bàn chân),
    # khép vòng bằng cách trừ dần độ trôi giữa hai đầu đoạn, giữ thân ở một độ cao + nhấp nhô theo nhịp cánh.
    F0, F1 = 0.5, 1.3
    FLY_DUR = F1 - F0
    DICH = [bx[n] for n in ("all2", "all43", "all46", "target2", "target4")]
    FLY_CAO = 300.0 * KG
    f_a, f_b = lay("fly_01", F0)[0].copy(), lay("fly_01", F1)[0].copy()
    f_troi = f_b - f_a

    def bay(t, P):
        s = (t % FLY_DUR) / FLY_DUR
        d = lay("fly_01", F0 + s * FLY_DUR)
        V = d[0] - f_troi * s
        duong = (d[0][bx["all2"], 1:3] - f_troi[bx["all2"], 1:3] * s).copy()      # chỗ all2 sau khi khép vòng: trừ đi để đứng tại chỗ
        nhap = 16.0 * KG * math.sin(2 * math.pi * (s - 0.18))
        for i in DICH:
            V[i, 1:3] = V[i, 1:3] - duong + np.array([0.0, FLY_CAO + nhap])
        V[bx["all2"], 0] += 12.0 + 3.0 * math.sin(2 * math.pi * (s - 0.3))        # thân bớt chúi: bay ngang
        ap(P, [V] + d[1:])

    # ---------------------------------------------------------------- SKILL (chiêu cuối): VẠN DIỆP
    # A = skill_05 của họ 0 → 1,47: sấp xuống xoè cánh sát đất → vươn dậy dựng bốn cánh gầm → khép cánh trùm thân thành kén (tụ lực).
    # B = skill_03 của họ 0,82 → hết: kén BUNG, bốn cánh dựng đứng gầm → quạt cánh chém tới → sập cánh quét xuống → về.
    SA1, SB0, S_NOI = 1.47, 0.82, 0.13
    S_DUR = SA1 + S_NOI + (CD["skill_03"][0] - SB0)

    def gio_b(tb):
        return SA1 + S_NOI + (tb - SB0)

    def skill(t, P):
        if t <= SA1:
            d = lay("skill_05", t)
        elif t < SA1 + S_NOI:
            d = tron(lay("skill_05", SA1), lay("skill_03", SB0), em((t - SA1) / S_NOI))
        else:
            d = lay("skill_03", SB0 + (t - SA1 - S_NOI))
        ap(P, d)
        r = hoat.rung(t, 1.2, SA1, moi=1)                               # gồng trong kén: rung nhẹ tăng dần
        if r:
            P.rot("all3", 0.8 * r * (t - 1.2) / (SA1 - 1.2))

    ev_skill = [(0.37, "sap", ""), (0.74, "gam", ""), (1.2, "ken", ""), (SA1, "bung", ""), (round(gio_b(1.22), 3), "trung", "quat"),
                (round(gio_b(1.72), 3), "trung", "sap"), (round(gio_b(2.0), 3), "het_gam", "")]

    D_DUR = CD["die_01"][0]

    def chet(t, P):
        # như clip của họ: khuỵu, gượng dậy, bật lên, sập xuống rồi xác văng chéo ra khỏi màn; 0,14 s cuối mờ hẳn (khung cuối trống)
        ap(P, lay("die_01", t), hien=float(np.clip((D_DUR - t) / 0.14, 0.0, 1.0)))

    out = []
    for ten_, goc, lap in CLIPS:
        if ten_ == "appear" and goc not in CD:
            out.append(Clip(ten_, AP_DUR, appear, ev=[(AP_TREO, "treo", ""), (AP_ROI, "cham_dat", "")]))
        elif ten_ == "fly" and goc not in CD:
            out.append(Clip(ten_, FLY_DUR, bay, loop=True, ev=[(round(0.22 * FLY_DUR, 3), "vo_canh", "")]))
        elif ten_ == "skill" and goc not in CD:
            out.append(Clip(ten_, S_DUR, skill, ev=ev_skill, trung=gio_b(1.22)))
        elif ten_ == "die":
            out.append(Clip(ten_, CD[goc][0], chet))
        else:
            if goc not in CD:
                goc = TAM[goc]
            dur = CD[goc][0]
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=SU_KIEN.get(goc, [])))
    return out


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ]: khung lớn nền xám → rig/soi_<clip>.png
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 4)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    if a and a[0] == "can":                    # can <clip> <giây> <xương hoặc x,y> <bán kính> [phóng]: ảnh cận → rig/can_<clip>_<giây>.png
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        P = fr[min(len(fr) - 1, int(round(float(a[2]) * 30)))]
        tam = tuple(sk.the_gioi(P)[a[3]][:2, 2]) if a[3] in sk.bi else tuple(float(x) for x in a[3].split(","))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"can_{a[1]}_{a[2]}.png")
        soi.anh_can(soi.Ve(sk), P, tam, float(a[4]), pth, phong=float(a[5]) if len(a) > 5 else 3.0, luoi=False)
        print(pth)
        return
    # con này rộng ngang (rộng / cao ~1,3) và ba dạng của suất dùng chung rig với cỡ 0,95 / 1,1 / 1,16: ở cỡ 1,16 cánh chờm bảng tên và sát
    # bệ đối thủ (xem trong trận 2026-11-13). Khai chiều cao lớn hơn chiều cao đo để game vẽ nhỏ lại chừng 11 %
    fr0 = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
    cao = soi.chieu_cao(soi.Ve(sk), fr0, ()) * CAO_KHAI
    xuat.xuat_het(sk, clips, RA, TEN, "Boss cuối đảo Mộc: rồng trúc bốn cánh (moc_vuong)" + (" — DA TẠM" if info["tam"] else ""), dang=1,
                  so_dang=1, dung_yen=("attack", "cast", "skill"), ma_goc=None, tol={"rotate": 0.25, "translate": 0.2, "scale": 0.003},
                  khop_idle=0.2, dich_mb=1.6, tran_mb=2.4, luoi=False, cao=cao)


if __name__ == "__main__":
    main(sys.argv[1:])
