# -*- coding: utf-8 -*-
"""Thú một sừng đảo Mộc (giac_moc): clip theo ý người dùng (2026-11-13), dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3804 rồi để runtime
Spine thật nướng (43 ràng buộc đường cong, 8 IK, 8 physics của họ vẫn chạy; skill pokiclash-spine-rig mục 00 "CLIP MỚI trên rig gốc").

Người dùng:
- appear: "làm nó nhảy vào thôi".           - idle: giống họ (idle_01).       - run, die: giống họ (run_01, die_01).
- đánh thường: giống skill 1, dậm chân mạnh tạo vết nứt tới đối thủ (fx làm riêng) → skill_01_3 (co chân trước gần rồi dậm).
- chiêu mana: giống skill_02, ngẩng lên tụ cầu năng lượng trên đỉnh sừng rồi cúi xuống phóng tia từ cầu.
- chiêu cuối: open_01 mở phần bụng, open_02 giữ lúc mở; quả tim trong bụng phát sáng cực mạnh rồi bắn một tia chết chóc vào đối thủ.

Rig gốc (con nhìn sang PHẢI): root > bone (dời cả con; bốn đích IK chân là con của nó) > bone4 > bone2 (thân, không gồm bàn chân) >
bone5 (ngực) > bone25 > bone24 > bone65 (đầu) > bone66 (sừng, không bao giờ cử động so với đầu).

Kênh riêng (ghi <scan>/kenh_rieng.json, giac_moc_rig.py đọc): bay = (x, y) dời xương move (appear nhảy từ ngoài vào); cau = 0..1+ cỡ quả
cầu ở đỉnh sừng (chiêu mana); tim = tỉ lệ quả tim (chiêu cuối: đập, phình); hien = 0..1 độ đậm cả con (appear hiện dần).

    giac_moc_clip.py dung                 ghép, ghi <scan>/lam_clip/gm_extra.json + kenh_rieng.json
    giac_moc_clip.py xem [clip,..|het] [n] [view|het] [t0] [t1]   tờ khung trên rig gốc → <scan>/lam_clip/khung/<clip>.jpg
    giac_moc_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json
Chạy qua quai/khoa.py chrome (xem, mau mở Chrome ngầm)."""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MON = "monster_3804"
FPS = 30.0


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


SCAN = os.path.join(sxs(), "scan", MON)
RIG = os.path.join(sxs(), "web", "assets", "Monster", MON)
LAM = os.path.join(SCAN, "lam_clip")
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
TEN = [b["name"] for b in I["bones"]]
PA = [b["parent"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
IKS = [k["name"] for k in I["ik"]]
ix = TEN.index
_S = None


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k độ trộn IK; ex = kênh riêng."""

    def __init__(self, u, k, ex=None):
        self.u, self.k = u, k
        self.ex = ex or dict(cau=0.0, tim=1.0, hien=1.0)

    def tron(self, B, w):
        return Dang(self.u + (B.u - self.u) * float(w), self.k + (B.k - self.k) * float(w), dict(self.ex))

    def xoay(self, ten, do):
        self.u[ix(ten), 2] += do
        return self

    def doi(self, ten, dx, dy):
        self.u[ix(ten), 0] += dx
        self.u[ix(ten), 1] += dy
        return self


def nap():
    global _S
    if _S is None:
        S = json.load(open(os.path.join(SCAN, "sample_dk.json"), encoding="utf-8"))
        _S = {}
        for c, v in S.items():
            U = np.array([f["u"] for f in v["frames"]], float)
            U[:, :, 2] = np.degrees(np.unwrap(np.radians(U[:, :, 2]), axis=0))
            U[:, :, 2] += 360.0 * np.round((B0[None, :, 2] - U[:1, :, 2]) / 360.0)
            _S[c] = (float(v["dur"]), U, np.array([[q[0] for q in f["k"]] for f in v["frames"]], float))
    return _S


def dk(clip, t, lap=False):
    dur, U, Kk = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w)


def nghi():
    return dk("idle_01", 0.0)


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return x ** k


def cung(t, t0, t1, t2, t3):
    if t <= t0 or t >= t3:
        return 0.0
    if t < t1:
        return em((t - t0) / (t1 - t0))
    if t <= t2:
        return 1.0
    return 1.0 - em((t - t2) / (t3 - t2))


def cong(moc, t, kieu=None):
    if t <= moc[0][0]:
        return moc[0][1]
    for i in range(len(moc) - 1):
        (a, x), (b, y) = moc[i], moc[i + 1]
        if t <= b:
            w = (t - a) / (b - a)
            if kieu and kieu[i]:
                w = kieu[i](w)
            return x + (y - x) * w
    return moc[-1][1]


def rung(t, t0, bien, tan=6.0, hz=5.0, pha=0.0):
    r = t - t0
    return bien * math.exp(-r * tan) * math.sin(2 * math.pi * hz * r + pha) if r > 0 else 0.0


def giat(t, bien, hz=19.0, pha=0.0):
    return bien * (math.sin(2 * math.pi * hz * t + pha) * 0.6 + math.sin(2 * math.pi * hz * 1.73 * t + 1.3 + pha) * 0.4)


# ---------------------------------------------------------------- idle, walk, hit, die: nguyên của họ
def idle(t):
    return dk("idle_01", t, True)


def walk(t):
    return dk("run_01", t, True)


def hit(t):
    return dk("hit_01", t)


def die(t):
    return dk("die_01", t)


# ---------------------------------------------------------------- attack: co chân trước gần, DẬM mạnh (vết nứt chạy tới đối thủ là VFX)
A_DAM, A_TRUNG, A_DUR = 0.74, 0.92, 1.40


def attack(t):
    """ĐÒN THƯỜNG 1,40 s, đứng tại chỗ (skill_01_3 của họ): rướn người, co chân trước gần lên trước ngực 0,30 → 0,60 (giữ đỉnh một nhịp);
    DẬM xuống 0,74 (sự kiện dam: bụi, đất nứt); cả thân dộng theo, rung tắt dần; vết nứt chạy tới đối thủ (sự kiện trung 0,92); về nghỉ."""
    tau = cong([(0.0, 0.0), (0.60, 0.58), (0.66, 0.61), (A_DAM, 0.74), (1.33, 1.3333)], t, [None, None, lambda w: vao(w, 1.8), None])
    D = dk("skill_01_3", tau)
    D.doi("bone2", rung(t, A_DAM, 9.0, 8.0, 7.0), -rung(t, A_DAM, 16.0, 7.0, 6.0, 1.4))
    D.xoay("bone24", rung(t, A_DAM, 3.0, 7.0, 6.0, 0.6))
    return D.tron(nghi(), em((t - 1.26) / 0.14)) if t > 1.26 else D


# ---------------------------------------------------------------- cast: ngẩng lên tụ cầu ở đỉnh sừng, cúi xuống phóng tia từ cầu
C_TU, C_PHUN, C_HET, C_DUR = 0.40, 1.36, 2.30, 2.70


def cast(t):
    """CHIÊU MANA 2,70 s, đứng tại chỗ (skill_02 của họ, kéo dài đoạn giữ). Ngẩng cao dần 0 → 1,10, ngực hé mở cho năng lượng từ tim
    chảy lên; cầu năng lượng tụ ở ĐỈNH SỪNG từ 0,40 (lớn dần, đầu rung nhẹ mạnh dần); 1,11 → 1,33 CÚI gập đầu chĩa sừng về trước;
    1,36 PHÓNG tia từ quả cầu (sự kiện phun): thân giật lùi một nhịp, ghìm giữ tia tới 2,30 (rung nhỏ; tia của game chảy 0,88 s);
    cầu tắt, ngẩng lên về nghỉ."""
    tau = cong([(0.0, 0.0), (1.33, 1.33), (C_HET + 0.03, 1.78), (C_DUR - 0.08, 2.0)], t)
    D = dk("skill_02", tau)
    tu = cung(t, C_TU, 1.10, 1.10, 1.30)
    giu = cung(t, C_PHUN, C_PHUN + 0.05, C_HET - 0.08, C_HET + 0.05)
    D.xoay("bone24", giat(t, 0.9, 16.0) * (0.25 + 0.75 * tu) * (tu > 0) + giat(t, 0.7, 23.0, 0.8) * giu)
    lui = -34.0 * cung(t, C_PHUN - 0.01, C_PHUN + 0.05, C_PHUN + 0.12, C_PHUN + 0.55) - 10.0 * giu
    D.doi("bone2", lui + giat(t, 1.8, 21.0, 2.0) * giu, giat(t, 1.4, 19.0, 0.4) * giu)
    D.ex["cau"] = max(0.0, cong([(C_TU - 0.02, 0.0), (1.10, 0.95), (C_PHUN - 0.04, 1.0), (C_PHUN, 1.25), (C_PHUN + 0.10, 0.80), (C_HET - 0.06, 0.70),
                                 (C_HET + 0.06, 0.0)], t, [lambda w: ra(w, 1.5), None, None, None, None, em])
                      + 0.05 * giat(t, 1.0, 13.0) * (tu > 0 or giu > 0))
    return D.tron(nghi(), em((t - (C_DUR - 0.14)) / 0.14)) if t > C_DUR - 0.14 else D


# ---------------------------------------------------------------- skill: mở ngực (open_01), giữ (open_02), tim rực sáng, bắn tia lớn
S_MO, S_TU, S_PHUN, S_HET, S_DONG, S_DUR = 0.95, 1.00, 2.05, 3.05, 3.55, 3.75
CK2 = 1.0667                                       # chu kỳ open_02


def skill(t):
    """CHIÊU CUỐI 3,75 s, đứng tại chỗ. 0 → 0,95 rướn cao, cổ dựng thẳng, các tấm vỏ ngực trượt MỞ (open_01), lộ quả tim; 1,00 → 2,05
    giữ dáng mở (open_02): tim đập nhanh dần, phình to, rực sáng (VFX), cả người rung mạnh dần; 2,05 BẮN tia lớn từ tim (sự kiện phun,
    trung 2,13): thân giật lùi mạnh, ghìm tia tới 3,05; tim xẹp, 3,05 → 3,55 hạ người, vỏ ngực ĐÓNG lại (open_01 chạy ngược); về nghỉ."""
    if t < S_HET:
        A = dk("open_01", min(t, 2.1667))
        Bo = dk("open_02", t - S_MO, True)
        D = A.tron(Bo, em((t - (S_MO - 0.10)) / 0.30))
    else:
        tau = cong([(S_HET, 0.62), (S_DONG, 0.0)], t, [em])
        D = dk("open_02", S_HET - S_MO, True).tron(dk("open_01", tau), em((t - S_HET) / 0.16))
        D = D.tron(nghi(), em((t - (S_DONG - 0.06)) / (S_DUR - S_DONG + 0.06)))
    tu = cung(t, S_TU, S_PHUN - 0.05, S_PHUN - 0.05, S_PHUN)
    giu = cung(t, S_PHUN, S_PHUN + 0.05, S_HET - 0.10, S_HET + 0.05)
    lac = 0.2 + 0.8 * vao(tu, 1.6)
    D.doi("bone2", (giat(t, 2.4, 15.0, 2.0) * lac * (tu > 0)) + giat(t, 3.0, 22.0, 1.0) * giu
          - 52.0 * cung(t, S_PHUN - 0.01, S_PHUN + 0.05, S_PHUN + 0.14, S_PHUN + 0.7) - 14.0 * giu
          + 16.0 * cung(t, S_PHUN - 0.22, S_PHUN - 0.04, S_PHUN - 0.04, S_PHUN),             # rướn tới lấy đà trước khi bắn
          giat(t, 2.0, 18.0, 0.5) * lac * (tu > 0) + giat(t, 2.2, 20.0, 0.2) * giu)
    D.xoay("bone24", giat(t, 1.0, 14.0, 1.0) * lac * (tu > 0) + giat(t, 0.9, 21.0, 0.3) * giu + 4.0 * cung(t, S_PHUN - 0.02, S_PHUN + 0.06, S_PHUN + 0.2, S_PHUN + 0.6))
    # quả tim: đập nhanh dần lúc tụ (1,6 → 5 nhịp / giây), phình tới 1,35; lúc bắn bung 1,5 rồi giữ 1,2 rung; hết tia xẹp về 1
    f = 1.6 + 3.4 * vao(tu, 1.5)
    dap = 0.06 * (0.5 + 0.5 * math.sin(2 * math.pi * f * (t - S_TU))) ** 3 * (tu > 0)
    D.ex["tim"] = (1.0 + 0.30 * vao(tu, 1.3) * (t < S_PHUN) + dap
                   + cong([(S_PHUN - 0.02, 0.0), (S_PHUN + 0.05, 0.50), (S_PHUN + 0.20, 0.22), (S_HET - 0.05, 0.18), (S_HET + 0.12, 0.0)], t,
                          [None, em, None, em]) * (t >= S_PHUN - 0.02)
                   + 0.03 * giat(t, 1.0, 17.0) * giu)
    return D


# ---------------------------------------------------------------- appear: nhảy từ ngoài vào, đáp thụp, đứng dậy
P_ROI, P_DAP, P_DUR = 0.20, 0.56, 1.75
P_XA = 1050.0                                      # bắt đầu ở sau lưng chừng này (ngoài khung), bay vào theo cung


def appear_bay(t):
    w = cong([(0.0, 0.0), (P_DAP, 1.0)], t, [lambda w: ra(w, 1.25)])
    return -P_XA * (1.0 - w), 0.0


def appear(t):
    """APPEAR 1,75 s (generate_01 của họ, bỏ đoạn gầm): cả con đang co người trên không (lấy từ 0,24 s của họ), bay vào từ phía sau
    theo cung, hiện dần 0,2 s đầu; ĐÁP thụp sâu 0,56 (sự kiện dap_dat: bụi, lá), bốn chân choãi, đầu chúi; đứng dậy 0,9 → 1,4; về nghỉ."""
    tau = cong([(0.0, 0.26), (P_DAP, 0.62), (0.95, 0.95), (1.45, 1.30)], t, [None, None, em])
    D = dk("generate_01", tau)
    D.doi("bone2", rung(t, P_DAP, 8.0, 7.0, 6.0), -rung(t, P_DAP, 14.0, 6.0, 5.0, 1.2))
    D = D.tron(nghi(), em((t - 1.15) / 0.50)) if t > 1.15 else D
    D.ex["hien"] = em(t / 0.18)
    return D


CLIP = {"gm_idle": (4.0, idle), "gm_walk": (1.6667, walk), "gm_attack": (A_DUR, attack), "gm_cast": (C_DUR, cast),
        "gm_skill": (S_DUR, skill), "gm_appear": (P_DUR, appear), "gm_hit": (0.5, hit), "gm_die": (1.0, die)}
LAP = {"gm_idle", "gm_walk"}
BAY = {"gm_appear": appear_bay}
SU_KIEN = {"gm_attack": [(A_DAM, "dam", ""), (A_TRUNG, "trung", "")],
           "gm_cast": [(C_TU, "tu", ""), (C_PHUN, "phun", ""), (C_HET, "het_phun", "")],
           "gm_skill": [(0.15, "mo", ""), (S_TU, "tu", ""), (S_PHUN, "phun", ""), (S_PHUN + 0.08, "trung", ""), (S_HET, "het_phun", ""),
                        (S_HET + 0.10, "dong", "")],
           "gm_appear": [(P_DAP, "dap_dat", "")]}


def dung(xem=False):
    out = []
    rieng = {}
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        Kk = np.array([d.k for d in Ds])
        bay = [list(BAY[ten](t)) if ten in BAY else [0.0, 0.0] for t in ts]
        if xem and ten in BAY:                     # giả lập ngay trên rig gốc phần xương move của rig mình lo
            U[:, ix("bone"), :2] += np.array(bay)
        bones = {}
        for i, nm in enumerate(TEN):
            d = U[:, i] - B0[i]
            o = {}
            if np.abs(d[:, 2]).max() > 1e-3:
                o["rotate"] = [[round(t, 4), round(float(v), 3)] for t, v in zip(ts, d[:, 2])]
            if np.abs(d[:, :2]).max() > 1e-3:
                o["translate"] = [[round(t, 4), round(float(x), 3), round(float(y), 3)] for t, (x, y) in zip(ts, d[:, :2])]
            sc = U[:, i, 3:] / np.where(np.abs(B0[i, 3:]) < 1e-6, 1.0, B0[i, 3:])
            if np.abs(sc - 1).max() > 1e-4:
                o["scale"] = [[round(t, 4), round(float(x), 4), round(float(y), 4)] for t, (x, y) in zip(ts, sc)]
            if o:
                bones[nm] = o
        iks = {kn: [[round(t, 4), round(float(v), 4), int(I["ik"][j]["bend"])] for t, v in zip(ts, Kk[:, j])] for j, kn in enumerate(IKS)
               if np.abs(Kk[:, j] - 1).max() > 1e-4}
        out.append({"name": ten, "dur": dur, "bones": bones, "iks": iks, "slots": {}})
        rieng[ten] = {"dur": dur, "cau": [float(d.ex["cau"]) for d in Ds], "tim": [float(d.ex["tim"]) for d in Ds],
                      "hien": [float(d.ex["hien"]) for d in Ds], "bay": bay, "su_kien": SU_KIEN.get(ten, []), "lap": ten in LAP}
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, IK {list(iks)}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "gm_extra.json"), "w", encoding="utf-8"))
    if not xem:
        json.dump(rieng, open(os.path.join(SCAN, "kenh_rieng.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "gm_extra.json"))
    return rieng


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "0,760,2300,2000"
VIEW_RIENG = {"gm_appear": "-400,760,3000,2000", "gm_skill": "0,860,2300,2200", "gm_cast": "0,860,2300,2200"}


def main(a):
    sys.stdout.reconfigure(encoding="utf-8")
    lenh = a[0] if a else "dung"
    if lenh == "dung":
        dung()
    elif lenh == "xem":
        dung(xem=True)
        cl = a[1] if len(a) > 1 and a[1] not in ("", "het") else ",".join(CLIP)
        n = a[2] if len(a) > 2 else "16"
        tt = (f"&t0={a[4]}" if len(a) > 4 else "") + (f"&t1={a[5]}" if len(a) > 5 else "")
        for c in cl.split(","):
            view = a[3] if len(a) > 3 and a[3] not in ("", "het") else VIEW_RIENG.get(c, VIEW)
            vw, vh = [float(x) for x in view.split(",")[2:]]
            _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={c}&extra=gm_extra.json&n={n}&tw=300&th={int(round(300 * vh / vw))}&cols=8&view={view}{tt}")
        dung()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "gm_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
