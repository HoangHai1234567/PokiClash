# -*- coding: utf-8 -*-
"""Tượng đá giữ rừng (tuong_da): rig trên bộ xương của con gốc monster_3423, mảnh của mình là MẢNH CỨNG một xương đặt đúng chỗ concept
đã duyệt; chuyển động lấy mẫu từ clip dựng ở tầng điều khiển (tuong_da_clip.py mau → <scan>/sample_moi.json).

- Đủ mọi xương của họ (cả bộ xương rời thứ hai dùng cho die / appear), đúng cha – con; bỏ xương bóng và bốn mục tiêu IK (không dùng).
- Mỗi mảnh có hai slot: slot chính bám xương bộ chính; slot "<tên>~2" (ẩn sẵn) bám xương rời của bộ hai, đặt cao hơn 811,4 đơn vị như
  của họ. Clip bật tắt hai bộ theo đúng mẫu khung (hình và độ đậm slot của họ).
- Lõi hai hình: `loi` (sáng) / `loi_tat` (tắt), đổi theo kênh `loi` của clip.
- Chiêu mana: thứ bay đi là CẢ TẢNG CẲNG TAY (tảng đá + đai rễ + lòng bàn tay + ngón; người dùng 2026-11-12: "bắn cả phần này nữa chứ
  không chỉ ngón tay"): bản sao trên xương `fly_g` / `fly_x` (con của root; game co quãng theo chỗ đối thủ, AolaActor.FarAtomik), tảng
  tay thật ẩn trong lúc bay. Xương `far` = chỗ đối thủ mặc định.
- Xương `cau`: chỗ và cỡ quả cầu năng lượng của chiêu cuối (VFX gắn vào; rig không vẽ cầu).

    tuong_da_rig.py                  dựng, xuất inbox/tuong_da_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    tuong_da_rig.py soi <clip> <giây,giây,...> [tỉ lệ]     khung lớn nền xám → rig/soi_<clip>.png
Chạy qua quai/khoa.py nang. Xương, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ."""
import json
import math
import os
import pickle
import subprocess
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi, tienhoa  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import tuong_da as TD  # noqa: E402
import tuong_da_manh as TM  # noqa: E402
import tuong_da_clip as TC  # noqa: E402

TEN = f"tuong_da_{TD.K}"
RA = os.path.join(TD.BASE, "rig")
KG = 0.46                    # đơn vị rig con gốc → đơn vị rig của mình
NHE = os.environ.get("TD_NHE") == "1"     # bản NHẸ (ảnh nhỏ) của dạng 2, chỉ để gộp vào dạng 1 cho clip tiến hóa
PXU = 0.44 if NHE else 0.72  # pixel ảnh atlas cho mỗi đơn vị rig con gốc
BO = ("root", "shadow", "SR1", "SR2", "SL1", "SL2")
CLIPS = [("appear", "td_appear", False), ("idle", "td_idle", True), ("walk", "td_walk", True), ("attack", "td_attack", False),
         ("cast", "td_cast", False), ("skill", "td_skill", False), ("hit", "td_hit", False), ("die", "td_die", False)]
TAN = 0.5                    # die: giữ đống đá rồi mờ dần chừng này giây
TIEU_DE = ("Gạc Đá dạng 1: Mầm Đá (tuong_da_1)" if TD.K == 1 else "Gạc Đá dạng 2: Gạc Đá (tuong_da_2)")
DINH_DAU = 0.25 if TD.K == 1 else 0.40      # đỉnh rêu trên đầu nằm ở phần này của ảnh đầu (trên nó là mầm / gạc)
# cặp (mảnh của mình, hình của họ) để khớp khung concept với hệ toạ độ rig gốc (tâm khung bao)
NEO = [("cau", "P_qiu"), ("khoa", "P_zhuangshi"), ("cang_g", "P_shoubiR01"), ("cang_x", "P_shoubiL01"), ("vai_g", "P_jianjiaR01"),
       ("ban_g", "P_shouR01"), ("ban_x", "P_shouL01"), ("loi", "P_shuijing")]
TAY_BAY = {"g": ("bone18", 0), "x": ("bone11", 1)}        # xương tảng cẳng tay (thứ bay đi: cả tảng + bàn tay), thứ tự trong kênh `ban`


def khop_khung(dat):
    """khung concept (px, y xuống) ↔ thế giới rig gốc (y lên): px = ox + s·X, py = oy − s·Y (bình phương tối thiểu trên các cặp NEO)."""
    by = {a["att"]: a for a in TC.A["atts"] if a["cur"]}
    R, b = [], []
    for m, h in NEO:
        P = np.array(by[h]["xy"], float).reshape(-1, 2)
        X, Y = (P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2
        gx, gy = dat[m]["goc"]
        w, hh = dat[m]["co"]
        R += [[X, 1, 0], [-Y, 0, 1]]
        b += [gx + w / 2, gy + hh / 2]
    (s, ox, oy), *_ = np.linalg.lstsq(np.array(R, float), np.array(b, float), rcond=None)
    lech = np.array(R) @ np.array([s, ox, oy]) - np.array(b)
    print(f"khớp khung concept: {s:.3f} px / đơn vị con gốc; lệch từng mốc (px): " +
          ", ".join(f"{m} {math.hypot(lech[2 * i], lech[2 * i + 1]):.0f}" for i, (m, _) in enumerate(NEO)))
    return float(s), float(ox), float(oy)


def dung():
    I, A = TC.I, TC.A
    IB = I["bones"]
    ten = TC.TEN
    dat = json.load(open(os.path.join(TM.MANH, "dat.json"), encoding="utf-8"))
    thu_tu = dat.pop("_thu_tu")
    s, ox, oy = khop_khung(dat)
    tg = lambda px, py: np.array([(px - ox) / s, (oy - py) / s])          # px concept → thế giới con gốc   # noqa: E731

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này (lao)
    for b in IB:
        if b["name"] in BO:
            continue
        cha = ten[b["parent"]]
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG, sx=b["sx"], sy=b["sy"])
    W0g = TC.fk(TC.B0)                                                    # ma trận dáng gốc của họ (đơn vị con gốc)
    bo_hai = {g["x1"]: n2 for n2, g in TC.G2.items()}                     # xương bộ chính → xương rời bộ hai
    slot_ho = {g["x1"]: (TC.SLOT.index(g["slots"][0][2]), TC.SLOT.index(g["slots"][0][0])) for g in TC.G2.values()}

    # ngón tay: bám xương ngón gần nhất của bàn tay đó
    for ben, ds in TM.NGON.items():
        for t in [k for k in dat if k.startswith(f"ng_{ben}")]:
            c = tg(*dat[t]["tam"])
            dat[t]["xuong"] = min(ds, key=lambda b_: np.hypot(*(W0g[TC.ix(b_)][:2, 2] - c)))

    manh, D0 = [], {}
    for t in thu_tu:
        g = Image.open(os.path.join(TM.MANH, t + ".png"))
        k = PXU / s
        im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))
        sk.anh(t, im)
        p0 = tg(*dat[t]["goc"]) * KG
        ti = (g.width / s * KG / im.width, g.height / s * KG / im.height)
        b1 = dat[t]["xuong"]
        b2 = bo_hai[b1]
        D0[t] = (p0, ti)
        an = t == "loi_tat"
        sk.slot(t, b1, t, an=an)
        sk.manh(t, t, Dat(p0[0], p0[1], neo=(0.0, 0.0), ti=ti))
        sk.slot(t + "~2", b2, t, an=True)
        sk.manh(t + "~2", t, Dat(p0[0], p0[1] + TC.DY2 * KG, neo=(0.0, 0.0), ti=ti))
        manh.append(t)

    # chiều cao game: đỉnh rêu trên đầu (không tính gạc cây, kẻo thân bị thu nhỏ so với tướng khác)
    dau_top = tg(0, dat["dau"]["goc"][1] + dat["dau"]["co"][1] * DINH_DAU)[1]
    cao = float(dau_top * KG)

    # chiêu mana: nắm tay bay trên xương fly_* (con của root), chỗ xuất phát = chỗ bàn tay ở khung rời tay
    S = json.load(open(os.path.join(TD.scan(), "sample_moi.json"), encoding="utf-8"))
    sk.xuong("far", "root", 0.9 * cao + 60.0, 0.45 * cao)
    bay = {}
    for ben, (xb, k) in TAY_BAY.items():
        f = S["td_cast"]["frames"][int(round(TC.C_BAN[k] * 30))]
        i = TC.ix(xb)
        x, y, rot = f["b"][i][0] * KG, f["b"][i][1] * KG, f["b"][i][2]
        sk.xuong(f"fly_{ben}", "root", x, y)
        sk.xuong(f"nam_{ben}", f"fly_{ben}", x, y, goc=rot, the_gioi=True)
        Wb = sk.W0[xb]
        M = sk.W0[f"nam_{ben}"] @ np.linalg.inv(Wb)                          # dáng gốc của tảng cẳng tay → chỗ rời vai
        dg = khung.goc_mat(sk.W0[f"nam_{ben}"]) - khung.goc_mat(Wb)
        ds = [f"ban_{ben}", f"cang_{ben}"] + [t for t in thu_tu if t.startswith(f"ng_{ben}")]      # cả tảng cẳng tay + bàn tay bay đi
        for t in ds:
            p0, ti = D0[t]
            q = M @ np.array([p0[0], p0[1], 1.0])
            sk.slot("bay_" + t, f"nam_{ben}", t, an=True)
            sk.manh("bay_" + t, t, Dat(q[0], q[1], goc=dg, neo=(0.0, 0.0), ti=ti))
        bay[ben] = dict(ds=ds, x0=x, y0=y)
    sk.xuong("cau", "root", 0.0, cao * 1.5)                                  # chỗ quả cầu năng lượng (VFX)
    for e, m in (("trung", "khung đòn trúng (đấm / nắm tay tới đích / cầu tới đích)"), ("tu", "bắt đầu gồng / tụ cầu (VFX gió, lá hút vào)"),
                 ("phun", "một tảng cẳng tay rời vai"), ("ve", "tảng cẳng tay lắp lại"), ("day", "cầu đầy"), ("nem", "cầu rời tay"),
                 ("loi", "lõi hiện ra"), ("ghep", "mảnh to khớp vào"), ("xong", "ráp xong"), ("tat", "lõi tắt"), ("roi", "bắt đầu rụng"),
                 ("cham_dat", "mảnh to chạm đất")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {len(manh)} mảnh; chiều cao game {cao:.0f}")
    return sk, dict(manh=manh, dat=dat, slot_ho=slot_ho, bay=bay, cao=cao, S=S)


def chuyen_dong(S):
    """{clip: (dài, {xương: mảng (số khung, 5) = lệch xoay độ, dời x, y (đơn vị rig mình), tỉ lệ x, y nhân})}: biến đổi RIÊNG đã áp
    (runtime Spine) so với dáng gốc."""
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(TC.I["bones"]):
            if b0["name"] in BO:
                continue
            Am = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                            F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[b0["name"]] = Am
        out[clip] = (float(v["dur"]), res, fr)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(info["S"])
    KR = json.load(open(os.path.join(TD.scan(), "kenh_rieng.json"), encoding="utf-8"))
    manh, dat, slot_ho, bay = info["manh"], info["dat"], info["slot_ho"], info["bay"]
    far = sk.W0["far"][:2, 2]

    def noi(arr, x):
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        return np.asarray(arr[i0], float) * (1 - w) + np.asarray(arr[i1], float) * w, i0

    def dat_dang(P, goc, tau, lap):
        dur, R, fr = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        for b, arr in R.items():
            v, _ = noi(arr, x)
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        i0 = min(int(round(x)), len(fr) - 1)
        F = fr[i0]
        kr = KR[goc]
        loi, _ = noi(kr["loi"], x)
        sang = float(loi) >= 0.5
        for t in manh:
            s1, s2 = slot_ho[dat[t]["xuong"]]
            a1 = 1.0 if F["n"][s1] else 0.0
            a2 = float(F["a"][s2]) if F["n"][s2] else 0.0
            if t == "loi":
                a1, a2 = a1 * sang, a2 * sang
            elif t == "loi_tat":
                a1, a2 = a1 * (not sang), a2 * (not sang)
            P.alpha[t] = float(a1)
            P.alpha[t + "~2"] = float(a2)
        bay_, _ = noi(kr["bay"], x)
        if abs(bay_[0]) > 1e-4 or abs(bay_[1]) > 1e-4:
            P.move("move", float(bay_[0]) * KG, float(bay_[1]) * KG)
        # nắm tay bay (chiêu mana)
        fb, _ = noi(kr["ban"], x)
        for ben, (xb, k) in TAY_BAY.items():
            nang, xoay, co, dang_bay = kr["ban_them"][i0][k]
            ds = bay[ben]["ds"]
            if dang_bay > 0.5:
                f_ = float(fb[k])
                nang_, _ = noi([q[k][0] for q in kr["ban_them"]], x)
                P.move(f"fly_{ben}", f_ * (far[0] - bay[ben]["x0"]), f_ * (far[1] - bay[ben]["y0"]) + float(nang_) * TC.C_NANG * KG)
                P.rot(f"nam_{ben}", float(xoay))
                P.scale(f"nam_{ben}", float(co))
                for t in ds:
                    P.alpha["bay_" + t] = 1.0
                    P.alpha[t] = 0.0
            else:
                for t in ds:
                    P.alpha["bay_" + t] = 0.0
        # quả cầu năng lượng: xương cau (VFX bám), tỉ lệ = cỡ cầu
        c, _ = noi(kr["cau"], x)
        if c[0] > 1e-3:
            P.move("cau", float(c[1]) * KG - sk.W0["cau"][0, 2], float(c[2]) * KG - sk.W0["cau"][1, 2])
            P.scale("cau", max(0.02, float(c[0])))

    out = []
    for ten_, goc, lap in CLIPS:
        dur = CD[goc][0]
        ev = [tuple(e) for e in KR[goc]["su_kien"]]
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in list(P.alpha):
                    P.alpha[sl] = a * P.alpha[sl]
            out.append(Clip(ten_, dur + TAN, fn, ev=ev))
        else:
            trung = TC.C_BAN[0] + TC.C_TOI if ten_ == "cast" else None
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=ev, trung=trung))
    info["dat_dang"] = dat_dang
    return out


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ]
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    cao = info["cao"]
    if a and a[0] == "nhe":                    # TD_DANG=2 TD_NHE=1: ghi bản nhẹ (rig + khung 0 idle + chiều cao) cho dạng 1 gộp tiến hóa
        idle = [c for c in clips if c.ten == "idle"][0]
        os.makedirs(RA, exist_ok=True)
        pickle.dump((sk, hoat.nuong(sk, idle)[0], cao), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    M, noi = sk, {}
    if TD.K == 1:
        # TIẾN HÓA nối liền: gộp bản nhẹ của dạng 2 (dựng ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun)
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, TD_DANG="2", TD_NHE="1"), check=True)
        sk2, idle2, cao2 = pickle.load(open(os.path.join(HERE, "inbox", "tuong_da_2", "rig", "_nhe.pkl"), "rb"))
        ti = cao / cao2
        M = tienhoa.gop(sk, sk2)
        end2 = tienhoa.doi_ten_pose(idle2, "n_")
        dat_dang = info["dat_dang"]

        def gong(t, P):                         # Mầm Đá: đứng dáng nghỉ, thụp xuống lấy hơi rồi gồng: thân nhô lên, hai tay bung, lõi phồng, rung
            dat_dang(P, "td_idle", 0.0, True)
            g = hoat.cv(t, [(0, 0), (0.3, -0.5), (0.6, 1, "out"), (1.3, 1.2)])
            r = hoat.rung(t, 0.5, 1.35, moi=1)
            P.move("bone2", 1.4 * r, 26.0 * KG * g)
            P.scale("bone27", 1 + 0.30 * max(g, 0))
            P.rot("bone17", -9.0 * max(g, 0) + 1.5 * r)
            P.rot("bone10", 9.0 * max(g, 0) - 1.5 * r)
            P.rot("bone6", 4.0 * g)

        def bung(t, P, fl):                     # Gạc Đá: hiện ở dáng nghỉ của nó, ưỡn lên, hai tay bung ra, lõi phồng rồi về
            for b, v in end2.t.items():
                P.t[b] = list(v)
            P.move("n_bone2", 0.0, 22.0 * KG * fl)
            P.rot("n_bone17", -14.0 * fl)
            P.rot("n_bone10", 14.0 * fl)
            P.rot("n_bone6", 6.0 * fl)
            P.scale("n_bone27", 1 + 0.25 * fl)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=bung, mem=[])
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips, RA, TEN, TIEU_DE, dang=TD.K, so_dang=2, dung_yen=("cast", "skill"), lao=(), far=("cast",),
                  cao=cao, ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=noi)


if __name__ == "__main__":
    main(sys.argv[1:])
