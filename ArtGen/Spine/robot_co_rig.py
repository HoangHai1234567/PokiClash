# -*- coding: utf-8 -*-
"""Robot hủy diệt cổ đại (robot_co, tướng 7 đảo Kim): RESKIN trên rig con gốc monster_3613 (golem robot cổ nhìn thẳng, hai nắm đấm chống đất).

- Xương: đủ mọi xương của họ + `move`; dáng gốc = khung 0 idle_01 (biến đổi riêng `l` đã áp IK hai chân, lấy mẫu bằng runtime Spine thật).
- Hình: mỗi hình của họ một hình của mình, NGUYÊN lưới của họ (điểm gắn theo ma trận dáng gốc trong att_goc.json). Mảnh đổi dáng (chỏm, mặt
  nạ, gai vai...) khai trong manh/dat_moi.json (ảnh của mình đặt đúng chỗ, lưới dày, mỗi đỉnh bám như điểm tương ứng trên lưới họ).
- Thứ tự vẽ: của họ. skill_01..04 đổi thứ tự (sừng vai trái hình ra sau thân; cẳng tay phải hình + ngón ra sau thân lúc giật về): slot di
  động nhân bản theo chỗ chèn (`<slot>@<chỗ>`), mỗi khung bật đúng bản.
- Lõi tên lửa: `P_wuqi1` (đủ đạn) / `P_wuqi2` (ống rỗng) của họ + 7 slot đầu đạn `dau_k` (cắt từ hiệu hai ảnh) trên `bone5` để tắt từng quả
  khi phóng; xương `ong_k` ở tâm từng ống cho VFX.
- Clip (người dùng dặn 2026-11-16):
    idle, walk  của họ (idle_01, run_01)
    appear      các bộ phận bay vào theo đường cong bezier lệch nhịp (chân, thân, lõi, vải, cẳng tay, sừng, giáp vai, giáp ngực, mặt nạ), khớp
                vào chỗ, mắt bật sáng, nhún nặng
    attack      skill_01: giơ tay phải hình ra, ổ nắm đấm tụ cầu năng lượng (xương `cau_tay`), bắn, tay + thân giật lùi như họ; đạn do code
    cast        skill_03: hai tay giơ lên trời, lòng bàn tay xoay liên tục, tụ cầu to trên đầu (xương `mieng`), ném xuống; cầu do code
    skill       skill_04: đứng lên, hai giáp ngực mở, lõi lục giác; phóng 7 tên lửa (sự kiện `phong` + số ống), mỗi quả thân giật nhẹ, đầu
                đạn tắt; khép ngực. Đường bay homing bezier, nổ: VFX + code
    hit, die    hit_01; die_01 (mặt nạ rơi, mắt tắt, lõi rỗng) + mờ dần

    robot_co_rig.py                         dựng, xuất inbox/robot_co_1/rig/
    robot_co_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    robot_co_rig.py kiem                    bước xoay lớn nhất giữa hai khung của từng clip
    RC_GOC=1 robot_co_rig.py ...            dựng bằng DA GỐC (ảnh part của họ) ra rig_goc/: chỉ để soi clip trong máy, không đưa vào game
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, hoat, xuat, soi  # noqa: E402,F401
from quai.khung import Sk, Pose, mat, goc_mat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.luoi import Luoi  # noqa: E402
import robot_co as G  # noqa: E402

GOC = os.environ.get("RC_GOC") == "1"
# DẠNG: mặc định = dạng 2 (dạng cuối đã duyệt, inbox/robot_co_1); RC_DANG=non = dạng 1 non trên CÙNG xương / lưới / clip (inbox/robot_co_non):
# đổi tỉ lệ ở xương gốc từng bộ phận (giáp vai, cẳng tay + nắm đấm nhỏ lại, ống xả ngắn lại) rồi chuyển da (skill "DẠNG KHÁC trên CÙNG rig gốc")
NON = os.environ.get("RC_DANG") == "non" and not GOC
BASE = os.path.join(os.path.dirname(G.BASE), "robot_co_non") if NON else G.BASE
TEN = os.environ.get("RC_TEN") or ("robot_co_non" if NON else "robot_co")
RA = os.environ.get("RC_RA") or os.path.join(BASE, "rig_goc" if GOC else "rig")
MANH = os.environ.get("RC_MANH") or os.path.join(BASE, "manh_goc" if GOC else "manh")
MANH2 = os.path.join(G.BASE, "manh")                  # da dạng 2: dạng non chưa có mảnh nào thì tạm lấy mảnh này
TI_LE = {} if not NON else {"bone26": float(os.environ.get("RC_VAI") or 0.82), "bone37": float(os.environ.get("RC_VAI") or 0.82),
                            "bone10": float(os.environ.get("RC_TAY") or 0.88), "bone29": float(os.environ.get("RC_TAY") or 0.88)}
TI_LE_ONG = float(os.environ.get("RC_ONG") or 0.72) if NON else 1.0       # ống xả (mảnh thêm trên xương vai) co quanh chân ống
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
USE = ["idle_01", "run_01", "skill_01", "skill_03", "skill_04", "hit_01", "die_01"]
BO_SLOT = {"shadow_normal"}
N_ONG = 7
TAY_P = ("rotate_01", "bone10", "bone24")         # tay PHẢI hình (bên đối thủ): sừng vai, cẳng tay, ổ nắm đấm
TAY_T = ("bone28", "bone29", "bone30")            # tay TRÁI hình


# ---------------------------------------------------------------- thứ tự vẽ của họ: slot đứng yên + slot di động (skill mục 28)
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


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung, đã áp ràng buộc)
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
        out[clip] = (float(v["dur"]), res, hinh, cho)
    return out


CD = _cd()
BAN = {m: sorted({c[m] for clip in USE for c, h in zip(CD[clip][3], CD[clip][2]) if h[m][0] is not None} | {NEO0[m]}) for m in DONG}


def mau(clip, t, lap=False, chi=None, tru=()):
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


def pha_gan(a, b, w):
    """trộn hai dáng; góc của b quy về cùng vòng với a."""
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


def bump(t, a, b, c, d):
    return em((t - a) / (b - a)) * (1 - em((t - c) / (d - c)))


def tq(t, bang):
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / max(1e-9, b_ - a_)
    return bang[-1][1]


def xoay_deu(t, tA, tB, tong, ram=0.15):
    """góc đã quay ở giây t khi quay `tong` độ trong [tA, tB], tốc độ hình thang (tăng / giảm đều trong `ram` giây): dừng đúng `tong`."""
    if t <= tA:
        return 0.0
    if t >= tB:
        return tong
    D = tB - tA
    r = min(ram, D / 2)
    v = tong / (D - r)                                    # tốc độ đỉnh
    s = t - tA
    if s < r:
        return 0.5 * v * s * s / r
    if s > D - r:
        q = D - s
        return tong - 0.5 * v * q * q / r
    return 0.5 * v * r + v * (s - r)


def tat_dan(t, t0, bien, tan, giam):
    """rung tắt dần sau t0."""
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def hien_theo_ho(sk, P, clip, t, lap=False):
    """độ đậm + hình của mọi slot theo khung của họ; slot di động bật đúng bản theo chỗ chèn của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    hinh, cho = CD[clip][2][i], CD[clip][3][i]
    for k, sl in enumerate(SL):
        if sl in BO_SLOT:
            continue
        n, a = hinh[k]
        if k in NEO0:
            for kk in BAN[k]:
                nm = ten_ban(k, kk)
                if nm not in sk.si:
                    continue
                P.alpha[nm] = a if (n is not None and kk == cho[k]) else 0.0
                if n is not None and len(sk.atts[nm]) > 1:
                    P.att[nm] = n
        elif sl in sk.si:
            P.alpha[sl] = a if n is not None else 0.0
            if n is not None and len(sk.atts[sl]) > 1:
                P.att[sl] = n


# ---------------------------------------------------------------- toạ độ trên ảnh vùng của họ
def _px_the_gioi(a):
    """phép affine px ảnh vùng (y xuống) → thế giới dáng gốc của một hình (lưới của họ)."""
    uv, _ = G.luoi(a)
    xy = np.array(a["xy"], float).reshape(-1, 2)
    M, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], xy, rcond=None)
    return M                                              # [x y 1] @ M


def _tam_do(im, nguong=None):
    """tâm các điểm đỏ (vòng đỏ ổ nắm đấm, mắt) trên ảnh RGBA."""
    A = np.asarray(im.convert("RGBA")).astype(int)
    m = (A[..., 0] > 150) & (A[..., 1] < 90) & (A[..., 2] < 90) & (A[..., 3] > 128)
    ys, xs = np.nonzero(m)
    return np.array([xs.mean(), ys.mean()]) if len(xs) else None


def manh_goc():
    """da gốc (chỉ để soi clip): mỗi vùng ảnh cắt theo lưới, phóng RES."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_goc.json")
    os.makedirs(MANH, exist_ok=True)
    for a in AG["atts"]:
        if a.get("region") not in imgs:
            continue
        p = os.path.join(MANH, a["region"] + ".png")
        if not os.path.exists(p):
            im = G.part_goc(a)
            im.resize((im.width * RES, im.height * RES), Image.LANCZOS).save(p)


# ---------------------------------------------------------------- dựng
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
    # thế giới dáng gốc KHÔNG đổi tỉ lệ: mảnh cứng (moi.json, toạ độ thế giới dạng 2) gắn theo hệ này thì co / phóng cùng xương (dạng non)
    sk_c = Sk("_c")
    sk_c.xuong("root")
    sk_c.xuong("move", "root")
    for i, b in enumerate(I["bones"]):
        if b["name"] != "root":
            z = L0[i]
            sk_c.xuong(b["name"], "move" if NB[b["parent"]] == "root" else NB[b["parent"]], z[0], z[1], goc=z[2], dai=b["len"], sx=z[3],
                       sy=z[4])
    Wc = sk_c.the_gioi()
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hinh0 = CD["idle_01"][2][0]
    IM = {}

    def anh_cua(r):
        if r not in IM:
            p = os.path.join(MANH, r + ".png")
            if NON and not os.path.exists(p):                # dạng non chưa có mảnh này: tạm da dạng 2
                p = os.path.join(MANH2, r + ".png")
            if not os.path.exists(p):
                raise SystemExit(f"thiếu mảnh {p}")
            g = Image.open(p).convert("RGBA")
            if not GOC:                                  # ảnh mảnh 1 px / đơn vị → PX px / đơn vị (giữ .atomik dưới trần 0,5 MB)
                k = float(os.environ.get("RC_PX") or 0.8)
                g = g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA")
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
        """NGUYÊN lưới của họ với ảnh cùng khung ảnh vùng (× RES)."""
        r = a["region"]
        im = anh_cua(r)
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

    def gan_cung(slot_ten, ten_anh, bone, Vw, im):
        """mảnh cứng: ô 4 đỉnh (thế giới dáng gốc) bám trọn một xương."""
        if ten_anh not in IM:
            IM[ten_anh] = im
            sk.anh(ten_anh, im)
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        rows = [[(bone, *map(float, np.linalg.solve(Wi[bone], np.array([v[0], v[1], 1.0]))[:2]), 1.0)] for v in Vw]
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.slot(slot_ten, bone, ten_anh, an=True)
        sk.atts[slot_ten][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": tris, "hull": 4, "V": np.array(Vw, float),
                                      "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_anh)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)

    by_slot = {}
    for a in AG["atts"]:
        if a.get("region") not in imgs_ho:
            continue
        by_slot.setdefault(a["slot"], []).append(a)

    # mảnh ĐỔI DÁNG (robot_co_manh.py cat R → manh/moi.json): slot của họ → ảnh của mình, mảnh cứng một xương, 4 góc thế giới dáng gốc
    MOI, THEM = {}, {}
    pm = os.path.join(MANH, "moi.json")
    if NON and not os.path.exists(pm):                       # dạng non chưa có mảnh đổi dáng riêng: dùng của dạng 2
        pm = os.path.join(MANH2, "moi.json")
    if not GOC and os.path.exists(pm):
        for ten_m, d in json.load(open(pm, encoding="utf-8")).items():
            if d.get("slot"):
                MOI[d["slot"]] = dict(d, ten=ten_m)
            else:                                            # mảnh THÊM (ống xả gắn xương vai): slot riêng, chèn ngay trước slot them_truoc
                THEM.setdefault(d["them_truoc"], []).append(dict(d, ten=ten_m, co=d.get("co", TI_LE_ONG)))

    def gan_moi(slot_ten, att_name, d, bn):
        """mảnh cứng: ảnh manh/<tên>.png, 4 góc (trên trái, trên phải, dưới phải, dưới trái của ảnh) ở thế giới dáng gốc, bám trọn xương bn."""
        im = anh_cua(d["ten"])
        Vw = np.array(d["the_gioi"], float)
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        if d.get("co", 1.0) != 1.0:                          # co quanh trung điểm cạnh dưới (ống xả dạng non ngắn lại, chân vẫn ở chỗ cũ)
            c_ = (Vw[2] + Vw[3]) / 2
            Vw = c_ + (Vw - c_) * float(d["co"])
        # toạ độ riêng tính theo thế giới KHÔNG đổi tỉ lệ (Wc): mảnh co / phóng cùng xương ở dạng non; dạng 2 thì Wc = Wi
        rows = [[(bn, *map(float, np.linalg.solve(Wc[bn], np.array([v[0], v[1], 1.0]))[:2]), 1.0)] for v in Vw]
        V0 = np.array([(Wi[bn] @ np.array([r_[0][1], r_[0][2], 1.0]))[:2] for r_ in rows])
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.atts[slot_ten][att_name] = {"type": "mesh", "path": d["ten"], "uv": uv, "tris": tris, "hull": 4, "V": V0, "verts": rows,
                                       "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, att_name)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=slot_ten)

    def anh_ong(ten, rong, dai, bang=(), tep=None):
        """ảnh một khúc ống: lấy manh/<tep>.png (GPT vẽ theo hình bóng tự dựng, robot_co_manh.py K6) nếu có, không thì tự vẽ tô phẳng
        (sắt sẫm hoặc thép), viền mực, đầu bo tròn; bang = các vạch đai (tỉ lệ dọc 0..1, màu)."""
        k_ = float(os.environ.get("RC_PX") or 0.8) if not GOC else 0.5
        w_px, h_px = max(8, int(round(rong * k_))), max(8, int(round(dai * k_)))
        p_ = os.path.join(MANH, (tep or "") + ".png")
        if NON and tep and not os.path.exists(p_):
            p_ = os.path.join(MANH2, tep + ".png")
        if tep and os.path.exists(p_):
            im = Image.open(p_).convert("RGBa").resize((w_px, h_px), Image.LANCZOS).convert("RGBA")
            IM[ten] = anh.loang_mau(im)
            sk.anh(ten, IM[ten])
            return IM[ten]
        ss = 4
        im = Image.new("RGBA", (w_px * ss, h_px * ss), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        v = max(4, int(3.4 * ss * k_ / 0.8))
        r_ = int(w_px * ss * 0.34)
        mau_ = bang[0] if bang else (59, 58, 61)
        dr.rounded_rectangle([v // 2, v // 2, w_px * ss - v // 2, h_px * ss - v // 2], radius=r_, fill=mau_ + (255,), outline=(43, 33, 24, 255),
                             width=v)
        for y_, c_ in bang[1:]:
            yy = int(y_ * h_px * ss)
            dr.rectangle([v, yy - int(9 * ss * k_), w_px * ss - v, yy + int(9 * ss * k_)], fill=c_ + (255,), outline=(43, 33, 24, 255),
                         width=max(2, v // 2))
        x_ = int(w_px * ss * 0.28)                                   # một vạch sáng dọc thân
        dr.line([x_, r_, x_, h_px * ss - r_], fill=(142, 145, 150, 255), width=max(2, v // 2))
        im = im.resize((w_px, h_px), Image.LANCZOS)
        IM[ten] = im
        sk.anh(ten, im)
        return im

    def dat_ong(ten, im, A_, B_, rong, b_tren, b_duoi, W_):
        """đặt ảnh ống dọc đoạn A_ → B_ (thế giới dáng gốc): hai đỉnh đầu A_ bám b_tren, hai đỉnh đầu B_ bám b_duoi."""
        d_ = (B_ - A_) / max(1e-6, np.linalg.norm(B_ - A_))
        n_ = np.array([-d_[1], d_[0]])
        Vw = np.array([A_ + n_ * rong / 2, A_ - n_ * rong / 2, B_ - n_ * rong / 2, B_ + n_ * rong / 2])
        bones = [b_tren, b_tren, b_duoi, b_duoi]
        rows = [[(b, *map(float, np.linalg.solve(W_[b], np.array([p[0], p[1], 1.0]))[:2]), 1.0)] for b, p in zip(bones, Vw)]
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        tris = np.array([[0, 1, 2], [0, 2, 3]])
        sk.slot(ten, b_tren, ten)
        sk.atts[ten][ten] = {"type": "mesh", "path": ten, "uv": uv, "tris": tris, "hull": 4, "V": Vw, "verts": rows,
                             "width": im.width, "height": im.height}
        sk.luoi[(ten, ten)] = Luoi(uv * np.array([im.width, im.height], float), tris, 4, 4, im.width, im.height, ten=ten)

    def them_tay_may(ten, b_vai, b_khuyu, b_pit):
        """BẮP TAY MÁY ống lồng từ gốc bắp tay (b_vai) tới khuỷu (b_khuyu). Người dùng 2026-11-16: "walk tay phải đung đưa bị lỗi", rồi "tay
        vẫn lỗi" với bản thanh nối bám thẳng cẳng tay (cẳng tay xoay lệch bắp tay ~90° ở walk → mép dưới thanh xoay theo, thanh xoắn bẹp thành
        que). Khuỷu chỉ TRƯỢT dọc trục bắp tay (walk cách vai 252–388) nên: ỐNG BỌC to cứng trên b_vai; CẦN PÍT-TÔNG trong ống: đầu trên bám
        b_vai, đầu dưới bám b_pit (con của b_vai đặt ở khuỷu, KHÔNG xoay, chỉ chép độ trượt của b_khuyu: xem nuong) → luôn là hình chữ nhật."""
        z = L0[NB.index(b_khuyu)]
        sk.xuong(b_pit, b_vai, z[0], z[1], goc=0.0)
        W_ = sk.the_gioi()
        S_, E_ = W_[b_vai][:2, 2], W_[b_khuyu][:2, 2]
        L_ = float(np.linalg.norm(E_ - S_))
        d_ = (E_ - S_) / max(1e-6, L_)
        # cần pít-tông (vẽ trước, nằm sau ống bọc): từ 0,40 L tới khuỷu + 34
        r_c = 96.0
        imc = anh_ong(ten + "_can", r_c, 0.60 * L_ + 34.0, bang=((84, 86, 92), (0.55, (142, 145, 150))), tep="tay_may_can")
        dat_ong(ten + "_can", imc, S_ + d_ * 0.40 * L_, E_ + d_ * 34.0, r_c, b_vai, b_pit, W_)
        # ống bọc: từ trước vai 40 tới 0,78 L (ngắn hơn khuỷu ngắn nhất của walk), to, thép sẫm + hai đai
        r_o = 150.0
        imo = anh_ong(ten + "_ong", r_o, 0.78 * L_ + 40.0, bang=((74, 76, 81), (0.30, (106, 109, 114)), (0.86, (106, 109, 114))),
                      tep="tay_may_ong")
        dat_ong(ten + "_ong", imo, S_ - d_ * 40.0, S_ + d_ * 0.78 * L_, r_o, b_vai, b_vai, W_)

    def them(slot_goc, ten, hien):
        ats = by_slot.get(slot_goc)
        if not ats:
            return
        if ten == slot_goc:
            for d in THEM.get(slot_goc, []):
                sk.slot(d["ten"], d["xuong"], d["ten"])
                gan_moi(d["ten"], d["ten"], d, d["xuong"])
            if slot_goc == "P_shouL1_1" and not GOC:         # bắp tay máy phải hình: trước thân + giáp ngực, sau giáp vai trước và cẳng tay
                them_tay_may("tay_may_phai", "rotate_01", "bone10", "pit_phai")
        mac = next((a for a in ats if a["cur"]), ats[0])
        sk.slot(ten, "move", mac["att"], an=not hien)
        for a in ats:
            if slot_goc == "P_shenti2" and not GOC:            # nắp mắt tắt: dựng sau, đúng chỗ mắt của thân mình
                continue
            if slot_goc in MOI:                                # cùng chỗ thế giới, xương theo hình của họ (mặt nạ rơi ở die: P_tou2 trên bone9)
                bn = NB[a["w"][0][0][0]] if a.get("w") else a["bone"]
                gan_moi(ten, a["att"], MOI[slot_goc], "move" if bn == "root" else bn)
            else:
                gan(ten, a)
        if mac["att"] in sk.atts[ten]:
            sk._slot(ten)["bone"] = sk.atts[ten][mac["att"]]["verts"][0][0][0]
        else:
            sk._slot(ten)["bone"] = "bone4"
        if slot_goc == "P_wuqi1" and ten == "P_wuqi1":
            them_dau_dan(by_slot["P_wuqi1"])

    def them_dau_dan(ats):
        """7 đầu đạn: hiệu giữa ảnh lõi đủ đạn (P_wuqi1) và ống rỗng (P_wuqi2) → 7 cụm; mỗi cụm một mảnh cứng trên bone5 + xương ong_k."""
        import cv2
        a1 = next(a for a in ats if a["att"] == "P_wuqi1")
        im1, im2 = anh_cua("P_wuqi1"), anh_cua("P_wuqi2")
        A1 = np.asarray(im1.convert("RGBA")).astype(int)
        A2 = np.asarray(im2.convert("RGBA").resize(im1.size, Image.LANCZOS)).astype(int)
        d = (np.abs(A1[..., :3] - A2[..., :3]).sum(2) > 60) & (A1[..., 3] > 100)
        d = cv2.morphologyEx(d.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(d)
        cum = sorted([k for k in range(1, n) if st[k, cv2.CC_STAT_AREA] > 20], key=lambda k: -st[k, cv2.CC_STAT_AREA])[:N_ONG]
        tam_anh = np.array([im1.width, im1.height]) / 2.0
        cum = sorted(cum, key=lambda k: (np.hypot(*(cen[k] - tam_anh)), math.atan2(cen[k][1] - tam_anh[1], cen[k][0] - tam_anh[0])))
        wr, hr = imgs_ho["P_wuqi1"].size
        M = _px_the_gioi(a1)                                          # px ảnh vùng → thế giới
        k_px = wr / im1.width                                         # px ảnh mảnh → px ảnh vùng
        for j, k in enumerate(cum):
            x, y, w, h = st[k, 0], st[k, 1], st[k, 2], st[k, 3]
            x0, y0, x1, y1 = max(0, x - 3), max(0, y - 3), min(im1.width, x + w + 3), min(im1.height, y + h + 3)
            vung = cv2.dilate((lab == k).astype(np.uint8), np.ones((5, 5), np.uint8))[y0:y1, x0:x1]
            B = A1[y0:y1, x0:x1].copy()
            B[..., 3] = (B[..., 3] * vung).astype(int)
            imk = Image.fromarray(B.astype(np.uint8), "RGBA")
            goc = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            Vw = [np.array([gx * k_px, gy * k_px, 1.0]) @ M for gx, gy in goc]
            gan_cung(f"dau_{j}", f"dau_{j}", "bone5", Vw, imk)
            c = np.array([cen[k][0] * k_px, cen[k][1] * k_px, 1.0]) @ M
            lp = np.linalg.solve(Wi["bone5"], np.array([c[0], c[1], 1.0]))
            sk.xuong(f"ong_{j}", "bone5", float(lp[0]), float(lp[1]))
        print(f"  lõi tên lửa: {len(cum)} đầu đạn")

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

    # ---- xương cho VFX
    def tam_tren(slot, att=None):
        a = next(q for q in by_slot[slot] if att is None or q["att"] == att)
        c = _tam_do(G.part_goc(a))
        return (np.array([c[0], c[1], 1.0]) @ _px_the_gioi(a)) if c is not None else None

    mat_ = tam_tren("P_shenti", "P_shenti")
    e_ = MOI.get("P_shenti", {}).get("mat")
    if not GOC:                                              # mắt của thân mình: nắp mắt tắt (P_shenti2) là đĩa sắt sẫm đúng chỗ, đúng cỡ
        if e_:
            mat_ = np.array(e_["the_gioi"], float)
        r_ = (float(e_["r"]) if e_ else 24.0) + 2.5
        n_ = int(math.ceil(2 * r_ + 8))
        dia = Image.new("RGBA", (n_ * 4, n_ * 4), (0, 0, 0, 0))
        dr_ = ImageDraw.Draw(dia)
        c_ = n_ * 2
        dr_.ellipse([c_ - r_ * 4, c_ - r_ * 4, c_ + r_ * 4, c_ + r_ * 4], fill=(47, 47, 53, 255), outline=(43, 33, 24, 255), width=8)
        dia = dia.resize((n_, n_), Image.LANCZOS)
        IM["mat_tat"] = dia
        sk.anh("mat_tat", dia)
        h_ = n_ / 2.0
        Vw = [mat_ + np.array([-h_, h_]), mat_ + np.array([h_, h_]), mat_ + np.array([h_, -h_]), mat_ + np.array([-h_, -h_])]
        gan_moi("P_shenti2", "P_shenti2", dict(ten="mat_tat", the_gioi=[list(v) for v in Vw]), "bone4")
    lp = np.linalg.solve(Wi["bone4"], np.array([mat_[0], mat_[1], 1.0]))
    sk.xuong("mat", "bone4", float(lp[0]), float(lp[1]))
    for ten, slot, cang in (("cau_tay", "P_shouL2_1", "bone10"), ("cau_tay_t", "P_shouR2_1", "bone29")):
        o = tam_tren(slot)                                   # tâm vòng đỏ ổ nắm đấm
        goc_c = Wi[cang][:2, 2]
        huong = (o - goc_c) / max(1e-6, np.linalg.norm(o - goc_c))
        p = o + huong * 70.0                                  # cầu năng lượng nằm ngay trước lòng ổ
        lp = np.linalg.solve(Wi[cang], np.array([p[0], p[1], 1.0]))
        sk.xuong(ten, cang, float(lp[0]), float(lp[1]))
    cao = float(max(sp["V"][:, 1].max() for sn, sl in sk.atts.items() if sk._slot(sn)["alpha"] > 0 for sp in sl.values()))
    sk.xuong("mieng", "move", float(Wi["bone4"][0, 2]), 1.25 * cao)        # cầu to trên đầu ở chiêu mana (clip cast dời theo hai tay)
    sk.xuong("far", "root", 1.6 * cao, 0.42 * cao)
    for e, m in (("tu", "bắt đầu tụ cầu năng lượng (VFX ở cau_tay / mieng)"), ("ban", "bắn cầu năng lượng từ cau_tay (code cho đạn bay)"),
                 ("giat", "tay + thân giật lùi"), ("trung", "khung trúng"), ("xoay", "lòng bàn tay xoay liên tục"),
                 ("nem", "ném cầu to xuống đầu đối thủ (code cho cầu rơi)"), ("mo_nguc", "hai giáp ngực mở, lộ lõi tên lửa"),
                 ("phong", "phóng một tên lửa từ ong_<số> (code: đường bezier ngẫu nhiên kiểu homing tới đối thủ, nổ lớn)"),
                 ("dong_nguc", "giáp ngực khép lại"), ("lap", "một bộ phận lắp vào chỗ (tia lửa nhỏ)"), ("mat_sang", "mắt bật sáng"),
                 ("cham_dat", "chạm đất nặng (bụi)"), ("nga", "đổ xuống")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}; slot di động: "
          + ", ".join(f"{SL[m]}×{len(BAN[m])}" for m in DONG))
    return sk, dict(cao=cao)


# ---------------------------------------------------------------- appear: bộ phận bay bezier vào
NHOM_BAY = [   # (xương gốc nhóm, hướng xuất phát (× chiều cao, so với chỗ đích), giờ bắt đầu, giờ tới, quay thêm (độ, giảm về 0), cong)
    ("bone40", (-1.35, 0.15), 0.00, 0.40, 220.0, 1),      # chân trái hình
    ("bone43", (1.35, 0.15), 0.04, 0.44, -220.0, -1),     # chân phải hình
    ("bone4", (0.10, 1.70), 0.10, 0.52, 25.0, 1),         # thân (đầu, cổ, thân dưới) rơi từ trên xuống
    ("bone5", (0.55, 1.45), 0.26, 0.60, 90.0, -1),        # lõi tên lửa (cha của giáp ngực + chân: quay ít, kẻo con lệch cung)
    ("bone11", (-0.80, -0.55), 0.30, 0.66, 120.0, 1),     # vải eo
    ("bone10", (1.55, -0.25), 0.36, 0.76, -330.0, 1),     # cẳng tay phải hình (+ ngón)
    ("bone29", (-1.55, -0.25), 0.39, 0.79, 330.0, -1),    # cẳng tay trái hình
    ("rotate_01", (1.30, 1.15), 0.44, 0.82, -300.0, -1),  # sừng vai phải hình
    ("bone28", (-1.30, 1.15), 0.47, 0.85, 300.0, 1),      # sừng vai trái hình
    ("bone26", (1.60, 0.55), 0.52, 0.88, -240.0, 1),      # giáp vai phải hình
    ("bone37", (-1.60, 0.55), 0.55, 0.91, 240.0, -1),     # giáp vai trái hình
    ("bone6", (0.95, 0.95), 0.64, 0.97, -200.0, 1),       # giáp ngực phải hình
    ("bone7", (-0.95, 0.95), 0.67, 1.00, 200.0, -1),      # giáp ngực trái hình
    ("bone39", (0.00, 1.35), 0.82, 1.12, 360.0, 1),       # mặt nạ, cuối cùng
]


def lam_clip(sk, info):
    out = []
    cao = info["cao"]
    W0 = sk.the_gioi()
    goc0 = {b["name"]: b for b in sk.bones}

    # ---- idle / walk / hit / die: của họ
    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        hien_theo_ho(sk, P, "idle_01", t, True)
    out.append(Clip("idle", CD["idle_01"][0], idle, loop=True))

    # walk: người dùng 2026-11-16 "tôi không muốn tay phải cứ quẹt đất như thế, làm nó đung đưa nhẹ nhàng như tay trái thôi". Tay phải hình
    # của họ ở run_01 quét rộng (bắp 43°, cẳng 97°, bàn 84°, cẳng trượt 136 đơn vị; nắm đấm đi 621 đơn vị sát đất) → chuỗi tay phải chép NHỊP
    # TAY TRÁI hình, lật gương (góc đổi dấu) và lệch nửa chu kỳ (hai tay so le): nắm đấm phải nhấc khỏi đất, đi ~66 đơn vị như tay trái.
    GUONG = {"bone8": "bone27", "rotate_01": "bone28", "bone10": "bone29", "bone24": "bone30", "bone26": "bone37", "rotate_02": "bone38",
             "bone18": "bone31", "bone19": "bone32", "bone20": "bone33", "bone21": "bone34", "bone22": "bone35", "bone23": "bone36"}
    D_WK = CD["run_01"][0]

    def walk(t, P):
        d_ = mau("run_01", t, True)
        dl = mau("run_01", t + 0.5 * D_WK, True)
        for r_, l_ in GUONG.items():
            v = np.array(dl.get(l_, ZERO5), float)
            d_[r_] = np.array([-v[0], 0.0, 0.0, v[3], v[4]])
        dat(P, d_)
        hien_theo_ho(sk, P, "run_01", t, True)
    out.append(Clip("walk", CD["run_01"][0], walk, loop=True))

    def hit(t, P):
        dat(P, mau("hit_01", t))
        hien_theo_ho(sk, P, "hit_01", t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    D_DIE = CD["die_01"][0] + 0.45

    def die(t, P):
        dat(P, mau("die_01", t))
        hien_theo_ho(sk, P, "die_01", t)
        fa = 1.0 - em((t - (D_DIE - 0.32)) / 0.32)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.45, "nga", "")]))

    # ---- ĐÁNH THƯỜNG: skill_01 của họ. Tay phải hình vươn ra 0–0,40 (giữ nguyên), giữ + ổ nắm đấm xoay (họ quay bone24 đều) = tụ cầu,
    # rút gọn 0,40–1,03 → 0,40–0,82; bắn ở khung giật của họ (1,03 → 1,10: thân lùi, cẳng tay giật ngược), về.
    U_ATK = [(0.0, 0.0), (0.40, 0.40), (0.82, 1.03), (0.89, 1.10), (1.20, 1.45), (1.55, 2.0)]
    D_ATK = 1.55
    T_BAN = 0.84

    TAY_ATK = ("bone8", "rotate_01", "bone10", "bone24") + tuple(f"bone{i}" for i in range(18, 24))
    U_DUOI = 1.0                                           # giây của họ ở dáng tay duỗi thẳng (trước cú phóng tay)

    def attack(t, P):
        u = tq(t, U_ATK)
        d_ = mau("skill_01", u)
        # skill_01 của họ là cú TAY TÊN LỬA: từ 1,03 cẳng tay bị ẩn (bay đi do code của họ), xương cẳng tay thụt ngược vào vai rồi lắp lại sau
        # thân. Mình giữ tay trên người: sau lúc bắn, cả chuỗi tay lấy dáng duỗi của họ + cú giật (bắp tay hất lên, cẳng tay thụt như pít-tông)
        # rồi hoà dần về dáng nghỉ; phần còn lại (thân lùi, giáp vai bật mở) vẫn theo họ.
        if t > T_BAN - 0.02:
            ext = mau("skill_01", U_DUOI, chi=TAY_ATK)
            s_ = t - (T_BAN - 0.02)
            kick = math.exp(-s_ / 0.09) * (1 - math.exp(-s_ / 0.015))
            ve_ = em((t - (T_BAN + 0.10)) / (D_ATK - 0.12 - T_BAN - 0.10))
            for b in TAY_ATK:
                v = np.array(ext.get(b, ZERO5), float)
                if b == "rotate_01":
                    v[0] += 9.0 * kick
                elif b == "bone10":
                    v[0] += 6.0 * kick
                    v[1] -= 75.0 * kick
                v = v * (1 - ve_) + ZERO5 * ve_
                d_[b] = v
        # ổ nắm đấm: họ quay bone24 đều cả clip (tới 117° / khung sau khi rút gọn, ba ngón cách 120° nhìn như đứng yên); mình quay đúng 2 vòng
        # trong lúc vươn + tụ, dừng ở lúc bắn
        q_ = np.array(d_.get("bone24", ZERO5), float)
        q_[0] = -xoay_deu(t, 0.08, T_BAN, 720.0, 0.18)     # sau lúc bắn giữ −720° (= dáng nghỉ)
        d_["bone24"] = q_
        dat(P, d_)
        hien_theo_ho(sk, P, "skill_01", u)
        for m in DONG:                                     # cẳng tay + ngón luôn hiện, đúng thứ tự vẽ lúc nghỉ
            if SL[m] in ("P_shouL2_1",) or SL[m].startswith("P_shouL3_"):
                for kk in BAN[m]:
                    P.alpha[ten_ban(m, kk)] = 1.0 if kk == NEO0[m] else 0.0
        for sl in ("P_shouL2_1",) + tuple(s for s in SL if s.startswith("P_shouL3_")):
            if sl in sk.si and sl not in [SL[m] for m in DONG]:
                P.alpha[sl] = 1.0
        # gồng nhẹ lúc tụ: thân rung nhỏ dần lên
        g = bump(t, 0.40, 0.55, 0.80, 0.84)
        P.rot("bone4", 0.8 * g * math.sin(2 * math.pi * 14 * t))
    out.append(Clip("attack", D_ATK, attack, ev=[(0.36, "tu", ""), (T_BAN, "ban", ""), (T_BAN + 0.03, "giat", ""),
                                                 (T_BAN + 0.30, "trung", "")], trung=T_BAN + 0.30))

    # ---- CHIÊU MANA: skill_03 của họ. Giơ hai tay lên trời 0–0,50 (họ cho lòng bàn tay quay một vòng: bone24, bone30), GIỮ lâu hơn và cho
    # lòng bàn tay XOAY LIÊN TỤC (cộng góc đều) + gồng rung; cầu to tụ ở `mieng` (giữa hai ổ nắm đấm, nhích lên); ném = cú đập xuống của họ
    # (1,0 → 1,1: thân dập 148 đơn vị), về.
    T_GIO, T_NEM = 0.50, 1.55
    # cú đập của họ là KHOÁ BẬC: 1,000 → 1,033 bắp tay quay 140°, cẳng tay 216° trong một khung nguồn (nội suy thẳng: bàn tay đi vòng xuống
    # → lên → xuống, 450 đơn vị / khung 60). Mình tự vung: dáng A (1,000) → dáng B (1,067), mỗi xương tay chọn vòng ±360° sao cho ổ nắm đấm
    # đi đường NGẮN NHẤT, nhanh dần (đập), trong T_DAP; rồi phần còn lại của họ từ 1,067.
    T_DAP = 0.15
    U_A, U_B = 1.0, 31.999 / FPS + 1.0 / FPS            # khung 30 → khung 32 (1,067)
    D_A, D_B = mau("skill_03", U_A), mau("skill_03", U_B)
    TAY_P_, TAY_T_ = ("rotate_01", "bone10"), ("bone28", "bone29")

    def dang_dap(w, kp, kt):
        out = {}
        for b in set(D_A) | set(D_B):
            a_, b_ = D_A.get(b, ZERO5), np.array(D_B.get(b, ZERO5), float)
            b_ = b_.copy()
            if b in TAY_P_:
                b_[0] += 360.0 * kp[TAY_P_.index(b)]
            elif b in TAY_T_:
                b_[0] += 360.0 * kt[TAY_T_.index(b)]
            out[b] = a_ * (1 - w) + b_ * w
        return out

    def duong(kp, kt):
        L = [0.0, 0.0]
        prev = None
        for w in np.linspace(0, 1, 16):
            P_ = Pose()
            dat(P_, dang_dap(w, kp, kt))
            Wd = sk.the_gioi(P_)
            q = [Wd["cau_tay"][:2, 2], Wd["cau_tay_t"][:2, 2]]
            if prev is not None:
                L[0] += float(np.linalg.norm(q[0] - prev[0]))
                L[1] += float(np.linalg.norm(q[1] - prev[1]))
            prev = q
        return L
    bien = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]
    KP = min(bien, key=lambda k: duong(k, (0, 0))[0])
    KT = min(bien, key=lambda k: duong((0, 0), k)[1])
    print(f"  cú đập chiêu mana: vòng tay phải hình {KP}, tay trái hình {KT}; đường ổ nắm đấm {duong(KP, KT)[0]:.0f} / {duong(KP, KT)[1]:.0f} "
          f"(nội suy thẳng {duong((0, 0), (0, 0))[0]:.0f} / {duong((0, 0), (0, 0))[1]:.0f})")
    U_CAST = [(0.0, 0.0), (T_GIO, 0.50), (T_NEM, 1.0), (T_NEM + T_DAP, U_B), (T_NEM + T_DAP + 0.08, 1.10), (T_NEM + T_DAP + 0.48, 1.55),
              (T_NEM + T_DAP + 0.78, 2.0)]
    D_CAST = T_NEM + T_DAP + 0.78
    QUAY = 900.0                                           # độ / giây khi xoay lòng bàn tay

    def cast(t, P):
        u = tq(t, U_CAST)
        if T_NEM <= t < T_NEM + T_DAP:                    # cú đập tự vung (nhanh dần)
            u = U_A
            d_ = dang_dap(((t - T_NEM) / T_DAP) ** 1.3, KP, KT)
        else:
            d_ = mau("skill_03", u)
        # lòng bàn tay xoay liên tục (thay vòng quay một lần của họ): 4 vòng từ lúc giơ tới lúc ném, dừng đúng bội 360°
        quay_ = xoay_deu(t, 0.05, T_NEM, 4 * 360.0, 0.25)
        d_["bone24"] = np.array([-quay_, 0.0, 0.0, 1.0, 1.0])
        d_["bone30"] = np.array([quay_, 0.0, 0.0, 1.0, 1.0])
        dat(P, d_)
        hien_theo_ho(sk, P, "skill_03", u)
        if T_GIO * 0.6 < t < T_NEM + 0.05:
            g = em((t - T_GIO) / 0.4) * (1 - em((t - (T_NEM - 0.06)) / 0.06))
            P.rot("bone4", 0.9 * g * math.sin(2 * math.pi * 16 * t))
            P.move("bone4", 0.0, 3.0 * g * math.sin(2 * math.pi * 11 * t))
        W = sk.the_gioi(P)
        a_, b_ = (W["cau_tay"] @ np.array([0, 0, 1.0]))[:2], (W["cau_tay_t"] @ np.array([0, 0, 1.0]))[:2]
        m_ = (a_ + b_) / 2 + np.array([0.0, 0.10 * cao])
        dm = W["move"]
        lp = np.linalg.solve(dm, np.array([m_[0], m_[1], 1.0]))
        b0 = goc0["mieng"]
        P.move("mieng", float(lp[0] - b0["x"]), float(lp[1] - b0["y"]))
    out.append(Clip("cast", D_CAST, cast, ev=[(0.30, "tu", ""), (T_GIO * 0.6, "xoay", ""), (T_NEM + 0.08, "nem", ""),
                                             (T_NEM + 0.08 + 0.45, "trung", "")], trung=T_NEM + 0.08 + 0.45))

    # ---- CHIÊU CUỐI: skill_04 của họ. Đứng lên + hai giáp ngực mở 0–0,45; giữ dáng mở (họ 0,55) mà phóng N_ONG tên lửa cách nhau DT_PH,
    # mỗi quả thân giật lùi nhẹ, đầu đạn đó tắt (lõi đổi sang ảnh ống rỗng, đầu đạn còn lại là slot dau_k); rồi đoạn khép + ngồi về của họ.
    T_MO, T_PH0, DT_PH = 0.45, 0.62, 0.12
    T_PH1 = T_PH0 + DT_PH * (N_ONG - 1)
    T_DONG = T_PH1 + 0.35
    # sau loạt phóng: hoà THẲNG từ dáng giữ (họ 0,55) sang dáng 1,35 của họ trong T_HOA (đoạn 0,62–1,35 của họ là cú giật lùi 177 đơn vị +
    # trả về mà mình không dùng; dồn nó vào 0,15 s thì tay nhảy 140 đơn vị / khung 60), rồi đoạn khép ngực + ngồi về 1,35–2,0 của họ
    T_HOA = 0.28
    U_SK = [(0.0, 0.0), (T_MO, 0.45), (T_PH0, 0.55)]
    D_SK = T_DONG + T_HOA + 0.65
    THU = [5, 2, 0, 4, 1, 6, 3]                            # thứ tự ống phóng (ong_0 = giữa)

    def skill(t, P):
        if t < T_DONG:
            u = tq(t, U_SK)
            dat(P, mau("skill_04", u))
        elif t < T_DONG + T_HOA:
            u = 0.55
            dat(P, pha_gan(mau("skill_04", 0.55), mau("skill_04", 1.35), em((t - T_DONG) / T_HOA)))
        else:
            u = 1.35 + (t - T_DONG - T_HOA) / (D_SK - T_DONG - T_HOA) * 0.65
            dat(P, mau("skill_04", u))
        hien_theo_ho(sk, P, "skill_04", u)
        mo = T_MO * 0.6 < t < T_DONG + T_HOA + 0.12
        if mo:
            P.att["P_wuqi1"] = "P_wuqi2"
        for j in range(N_ONG):
            tj = T_PH0 + DT_PH * THU.index(j)
            P.alpha[f"dau_{j}"] = 1.0 if (mo and t < tj) else 0.0
        kick = 0.0
        for k in range(N_ONG):
            tk = T_PH0 + DT_PH * k
            if t >= tk:
                s_ = t - tk
                kick += math.exp(-s_ / 0.05) * (1 - math.exp(-s_ / 0.012))
        P.move("bone4", -22.0 * kick, -6.0 * kick)
        P.rot("bone4", 1.8 * kick)
    ev = [(0.25, "mo_nguc", "")] + [(T_PH0 + DT_PH * k, "phong", str(THU[k])) for k in range(N_ONG)] + [
        (T_PH0 + 0.55, "trung", ""), (T_DONG + T_HOA + 0.08, "dong_nguc", "")]
    out.append(Clip("skill", D_SK, skill, ev=ev, trung=T_PH0 + 0.55))
    print(f"  chiêu cuối {D_SK:.2f} s: mở ngực {T_MO:.2f}, phóng {T_PH0:.2f}–{T_PH1:.2f}, khép {T_DONG:.2f}")

    # ---- APPEAR: các bộ phận bay vào theo đường cong bezier bậc hai, lệch nhịp; khớp vào chỗ; mắt bật; nhún nặng
    T_MAT, D_AP = 1.24, 1.75
    con_cua = {}
    for b in sk.bones:
        nm = b["name"]
        p = b["parent"]
        x = nm
        while x is not None and x not in [g[0] for g in NHOM_BAY]:
            x = goc0[x]["parent"] if x in goc0 else None
        con_cua[nm] = x
    thu_tu_nhom = [nm for nm in [b["name"] for b in sk.bones] if nm in [g[0] for g in NHOM_BAY]]
    NB_ = {g[0]: g for g in NHOM_BAY}

    def nhom_cua_slot(sl):
        at = sk.atts.get(sl["name"]) or {}
        if not at:
            return None
        sp = list(at.values())[0]
        b = sp["verts"][0][0][0]
        return con_cua.get(b)

    NHOM_SLOT = {sl["name"]: nhom_cua_slot(sl) for sl in sk.slots}

    def vi_tri_bay(g, t):
        """(độ dời thế giới, góc thêm, độ đậm) của nhóm g ở giây t."""
        _, (hx, hy), t0, t1, quay, cong = NB_[g]
        S_ = np.array([hx, hy]) * cao
        if t <= t0:
            return S_, quay, 0.0
        q = min(1.0, (t - t0) / (t1 - t0))
        u = 1.0 - (1.0 - q) ** 3
        n_ = np.array([-S_[1], S_[0]]) / max(1e-6, np.linalg.norm(S_))
        C = 0.5 * S_ + n_ * 0.32 * np.linalg.norm(S_) * cong
        p = (1 - u) ** 2 * S_ + 2 * (1 - u) * u * C
        # góc giảm theo smoothstep (đỉnh 1,5 × tốc trung bình), không theo u (đầu đường bay u quá nhanh: mặt nạ quay 200° / khung)
        return p, quay * (1 - em(q)), min(1.0, (t - t0) / 0.06)

    def appear(t, P):
        dat(P, mau("idle_01", 0.0))
        hien_theo_ho(sk, P, "idle_01", 0.0)
        for g in thu_tu_nhom:
            # MỌI nhóm, kể cả nhóm đã tới nơi: nhóm cha còn đang bay (chân là con của lõi) thì phải bù, không thì bị cha kéo đi
            off, quay, a_ = vi_tri_bay(g, t)
            W = sk.the_gioi(P)
            b = goc0[g]
            Wd = W0[g].copy()
            c, s = math.cos(math.radians(quay)), math.sin(math.radians(quay))
            Wd[:2, :2] = np.array([[c, -s], [s, c]]) @ Wd[:2, :2]
            Wd[:2, 2] += off
            Ld = np.linalg.solve(W[b["parent"]], Wd)
            dr = goc_mat(Ld) - b["rot"]
            # đúng vòng: góc riêng ≈ góc quay thêm của nhóm trừ góc quay thêm của nhóm cha (đừng quy về ±180: nướng sẽ nối lệch một vòng)
            gp = con_cua.get(b["parent"])
            mong = quay - (vi_tri_bay(gp, t)[1] if gp else 0.0)
            dr += 360.0 * round((mong - dr) / 360.0)
            cur = P.t.get(g, [0, 0, 0, 1, 1])
            P.move(g, float(Ld[0, 2] - b["x"] - cur[0]), float(Ld[1, 2] - b["y"] - cur[1]))
            P.rot(g, float(dr - cur[2]))
        for sl in sk.slots:
            gr = NHOM_SLOT.get(sl["name"])
            if gr is not None:
                _, _, a_ = vi_tri_bay(gr, t)
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
        # mắt tắt cho tới khi lắp xong rồi chớp sáng
        tat = t < T_MAT or (T_MAT + 0.05 < t < T_MAT + 0.10)
        if "P_shenti2" in sk.si:
            P.att["P_shenti2"] = "P_shenti2"
            P.alpha["P_shenti2"] = (1.0 if tat else 0.0) * vi_tri_bay("bone4", t)[2]
        # thân đáp: nhún nặng; mặt nạ lắp: giật nhẹ
        nhun = bump(t, 0.50, 0.55, 0.60, 0.80)
        P.scale("bone2", 1.0 + 0.06 * nhun, 1.0 - 0.09 * nhun)
        sap = bump(t, 1.10, 1.13, 1.16, 1.40)
        P.scale("bone2", 1.0 + 0.05 * sap, 1.0 - 0.07 * sap)
        P.move("bone4", 0.0, tat_dan(t, T_MAT, 6.0, 5.0, 0.12))
    ev = [(0.52, "cham_dat", "")] + [(g[3], "lap", g[0]) for g in NHOM_BAY if g[0] != "bone4"] + [(T_MAT, "mat_sang", "")]
    out.append(Clip("appear", D_AP, appear, ev=sorted(ev)))
    return out


def nuong(sk, clip):
    """nướng clip; góc liền mạch (mỗi khung chọn bội 360° gần khung trước nhất)."""
    n = int(round(clip.dur * FPS)) + 1
    frames = []
    for i in range(n):
        t = min(clip.dur, i / FPS)
        P = Pose()
        clip.fn(t, P)
        # cần pít-tông bắp tay máy: xương pit_phai chép độ TRƯỢT của khuỷu bone10 (cùng cha rotate_01, không xoay). Appear thì không: ở đó
        # cẳng tay bay riêng (dời lớn trong hệ bắp tay), chép thì cần kéo dài xuyên màn
        if clip.ten != "appear" and "pit_phai" in sk.bi:
            g = P.t.get("bone10")
            if g and (abs(g[0]) > 1e-6 or abs(g[1]) > 1e-6):
                P.move("pit_phai", g[0], g[1])
        frames.append(P)
    for i in range(1, n):
        Pp, Q = frames[i - 1], frames[i]
        for b, g in Q.t.items():
            a0 = Pp.t.get(b, [0, 0, 0, 1, 1])[2]
            g[2] -= 360.0 * round((g[2] - a0) / 360.0)
    return frames


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
        sc_ = float(a[2]) if len(a) > 2 else 0.9
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
        sc = float(a[3]) if len(a) > 3 else 0.5
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
    xuat.xuat_het(sk, clips, RA, TEN, "Robot hủy diệt cổ đại (robot_co): tướng 7 đảo Kim" + (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  frames=frames, dang=1, so_dang=1, dung_yen=("attack", "cast", "skill"), lao=(), far=(), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  impact={"attack": (0.04, 0.16, 0.05), "cast": (0.12, 0.7, 0.14, "#ffd27a55"), "skill": (0.14, 0.95, 0.16, "#ffb04a66")})


if __name__ == "__main__":
    main(sys.argv[1:])
