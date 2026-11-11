# -*- coding: utf-8 -*-
"""tm03, cách lai: cắt tờ GPT, dò mảnh GPT trên concept, dựng lớp thân cắt từ concept + vẽ bù. Gọi qua tm03_lai.py (cần cv2):

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm03_lai.py cat 1    cắt tờ M01, M02 -> inbox/tm03_1/manh/
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm03_lai.py dat 1    dò mảnh trên concept, khớp đuôi cuộn -> lai/dat.json, so_ghep.png
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm03_lai.py lai 1    lớp thân cắt từ concept + vẽ bù -> lai/than.png, lop.json

Mọi toạ độ ở đây là px concept (1536 x 1024, y xuống). tm03.py đổi sang toạ độ rig.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh as qanh  # noqa: E402

import tm03_lai as TL  # noqa: E402

CODE = "tm03"


def base(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


# ---------------------------------------------------------------- cắt tờ
def _gan_1(to_m01, to_m02):
    out = {}
    m = sorted(to_m01.manh, key=lambda c: -c["dt"])
    out["bong"] = m[0]
    rest = m[1:]
    for c in rest:
        cx, cy = (c["x0"] + c["x1"]) / 2, (c["y0"] + c["y1"]) / 2
        top = cy < to_m01.h * 0.48
        mid = cx < to_m01.w * 0.75
        nm = ("mi_n" if mid else "mi_x") if top else ("long_mieng" if mid else "luoi")
        if nm in out:
            print("  trùng ô:", nm)
        out[nm] = c
    m2 = sorted(to_m02.manh, key=lambda c: -(c["x1"] - c["x0"]))
    out2 = {"duoi": m2[0]}
    legs = sorted(m2[1:], key=lambda c: (c["x0"] + c["x1"]) / 2)
    for nm, c in zip(("chan_sau", "chan_truoc", "chan_truoc_xa"), legs):
        out2[nm] = c
    return out, out2


def cat(k):
    td = os.path.join(base(k), "tai_ve")
    md = os.path.join(base(k), "manh")
    t1 = qanh.doc_to(qanh.to_moi_nhat(td, "M01"))
    t2 = qanh.doc_to(qanh.to_moi_nhat(td, "M02"))
    if k == 1:
        g1, g2 = _gan_1(t1, t2)
    else:
        m = sorted(t1.manh, key=lambda c: -c["dt"])
        g1 = {"bong": m[0]}
        for nm, c in zip(("long_mieng", "luoi", "mi_n", "mi_x"), sorted(m[1:], key=lambda c: (c["y0"] + c["y1"]) / 2)):
            g1[nm] = c
        legs = sorted(t2.manh, key=lambda c: -c["dt"])[:2]
        g2 = dict(zip(("chan_sau_xa", "chan_truoc_xa"), sorted(legs, key=lambda c: (c["x0"] + c["x1"]) / 2)))
    qanh.luu_manh(t1, g1, md)
    qanh.luu_manh(t2, g2, md)
    names = list(g1) + list(g2)
    print("  soi:", qanh.to_soi(md, names))


# ---------------------------------------------------------------- dò mảnh
def nap(k, n):
    return np.array(Image.open(os.path.join(base(k), "manh", n + ".png")).convert("RGBA"))


def doc_nhan(k):
    lab = np.load(os.path.join(base(k), "lai", "nhan.npy")).astype(np.int32)
    names = json.load(open(os.path.join(base(k), "lai", "nhan.json")))["names"]
    return lab, names


def mask_of(lab, names, *ns):
    m = np.zeros(lab.shape, bool)
    for n in ns:
        m |= lab == names.index(n) + 1
    return m


def hull_mask(m):
    ys, xs = np.nonzero(m)
    pts = np.stack([xs, ys], 1).astype(np.int32)
    h = cv2.convexHull(pts)
    out = np.zeros(m.shape, np.uint8)
    cv2.fillConvexPoly(out, h, 1)
    return out > 0


def warp_mask(part, sx, sy, r, lat=False, nguong=128):
    wp = TL.warp(part, sx, sy, r, lat)
    return wp, wp[:, :, 3] > nguong


def place_mask(H, W, wp_mask, cx, cy):
    out = np.zeros((H, W), bool)
    h, w = wp_mask.shape
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if ax1 > ax0 and ay1 > ay0:
        out[ay0:ay1, ax0:ax1] = wp_mask[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0]
    return out


def fit_cover(part, need, allow, s_rng, r_rng, around, win, sy_rng=None, w_miss=40.0, w_out=6.0, w_area=0.05):
    """dò (sx, sy, r, cx, cy) cho mặt nạ mảnh phủ kín `need`, ít lòi ra ngoài `allow`, nhỏ nhất. Trả kết quả và số px còn hở."""
    H, W = need.shape
    best = None
    nsum = int(need.sum())
    for sx in s_rng:
        for sy in (sy_rng if sy_rng is not None else [None]):
            syy = sx if sy is None else sy
            for r in r_rng:
                _, m = warp_mask(part, sx, syy, r)
                for dx in range(-win, win + 1, 3):
                    for dy in range(-win, win + 1, 3):
                        pm = place_mask(H, W, m, around[0] + dx, around[1] + dy)
                        miss = nsum - int((pm & need).sum())
                        out = int((pm & ~allow).sum())
                        c = miss * w_miss + out * w_out + int(pm.sum()) * w_area
                        if best is None or c < best[0]:
                            best = (c, sx, syy, r, around[0] + dx, around[1] + dy, miss, out)
    # tinh
    _, sx0, sy0, r0, cx0, cy0, _, _ = best
    for sx in np.linspace(sx0 * 0.97, sx0 * 1.03, 4):
        for sy in np.linspace(sy0 * 0.97, sy0 * 1.03, 4):
            for r in (r0 - 1, r0, r0 + 1):
                _, m = warp_mask(part, sx, sy, r)
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        pm = place_mask(H, W, m, cx0 + dx, cy0 + dy)
                        miss = nsum - int((pm & need).sum())
                        out = int((pm & ~allow).sum())
                        c = miss * w_miss + out * w_out + int(pm.sum()) * w_area
                        if c < best[0]:
                            best = (c, sx, sy, r, cx0 + dx, cy0 + dy, miss, out)
    return {"sx": float(best[1]), "sy": float(best[2]), "r": float(best[3]), "cx": float(best[4]), "cy": float(best[5])}, best[6], best[7]


# ---------------------------------------------------------------- đuôi cuộn: khớp đường xoắn vào concept
def tail_profile(part):
    """bề dày nửa trên / nửa dưới so với trục ngang qua giữa gốc, theo cột x của ảnh đuôi duỗi."""
    a = part[:, :, 3] > 128
    H, W = a.shape
    ys, xs = np.nonzero(a)
    x0, x1 = xs.min(), xs.max()
    cols = range(x0, x1 + 1)
    top, bot = [], []
    for x in cols:
        yy = np.nonzero(a[:, x])[0]
        top.append(yy.min() if len(yy) else np.nan)
        bot.append(yy.max() if len(yy) else np.nan)
    top, bot = np.array(top, float), np.array(bot, float)
    yc = float(np.nanmean((top[:max(5, len(top) // 12)] + bot[:max(5, len(bot) // 12)]) / 2))
    return {"x0": int(x0), "x1": int(x1), "yc": yc, "up": (yc - top).tolist(), "dn": (bot - yc).tolist()}


def centerline(p, Lp, n=240):
    """đường giữa đuôi (px concept, y xuống): gốc (x0, y0), hướng h0 (độ, màn hình), đoạn dẫn s_lead (tỉ lệ), bán kính r0 giảm
    tuyến tính theo q; quay theo chiều kim đồng hồ trên màn hình. Trả (pts (n, 2), theta (n,), s (n,))."""
    x0, y0, h0, s_lead, r0, q = p
    s = np.linspace(0, Lp, n)
    ds = s[1] - s[0]
    u = s / Lp
    w = np.clip(u / max(1e-3, s_lead), 0, 1)
    w = w * w * (3 - 2 * w)
    r = r0 * (1 - q * u)
    kap = w / np.maximum(r, 4.0)
    th = math.radians(h0) + np.concatenate([[0], np.cumsum((kap[1:] + kap[:-1]) / 2 * ds)])
    pts = np.zeros((n, 2))
    pts[0] = (x0, y0)
    for i in range(1, n):
        a = (th[i] + th[i - 1]) / 2
        pts[i] = pts[i - 1] + ds * np.array([math.cos(a), math.sin(a)])
    return pts, th, s


def ribbon_mask(shape, pts, th, s, prof, lam_t, lam_len, f=0.5):
    """vẽ dải đuôi theo đường giữa (mặt nạ ở độ phân giải f)."""
    H, W = shape
    out = np.zeros((int(H * f), int(W * f)), np.uint8)
    up, dn = np.array(prof["up"]), np.array(prof["dn"])
    L = len(up)
    xi = np.clip((s / lam_len).astype(int), 0, L - 1)
    a, b = np.nan_to_num(up[xi]) * lam_t, np.nan_to_num(dn[xi]) * lam_t
    nx, ny = -np.sin(th), np.cos(th)
    P1 = np.stack([pts[:, 0] - nx * a, pts[:, 1] - ny * a], 1) * f
    P2 = np.stack([pts[:, 0] + nx * b, pts[:, 1] + ny * b], 1) * f
    for i in range(len(pts) - 1):
        q = np.array([P1[i], P1[i + 1], P2[i + 1], P2[i]], np.int32)
        cv2.fillConvexPoly(out, q, 1)
    return out > 0


def fit_tail(T, care, prof, p0, rng, lam_t0, seed=1):
    """dò tham số đường xoắn cho dải đuôi trùng mặt nạ đuôi concept T (chỉ tính trong vùng care)."""
    f = 0.5
    Tf = cv2.resize(T.astype(np.uint8), None, fx=f, fy=f, interpolation=cv2.INTER_NEAREST) > 0
    Cf = cv2.resize(care.astype(np.uint8), None, fx=f, fy=f, interpolation=cv2.INTER_NEAREST) > 0
    Limg = len(prof["up"])

    def score(p):
        x0, y0, h0, s_lead, r0, q, lam_t, rho = p
        lam_len = lam_t * rho
        Lp = Limg * lam_len
        pts, th, s = centerline((x0, y0, h0, s_lead, r0, q), Lp)
        M = ribbon_mask(T.shape, pts, th, s, prof, lam_t, lam_len, f)
        a = M & Cf
        inter = (a & Tf).sum()
        uni = (a | Tf).sum()
        # khe giữa các vòng (lỗ kín bên trong dải cuộn) bị phạt nặng: các vòng phải chồng lên nhau như concept
        Mu = M.astype(np.uint8).copy()
        ff = np.zeros((Mu.shape[0] + 2, Mu.shape[1] + 2), np.uint8)
        cv2.floodFill(Mu, ff, (0, 0), 2)
        holes = int((Mu == 0).sum())
        return inter / max(1, uni) - 3.0 * holes / max(1, int(M.sum()))

    rs = np.random.RandomState(seed)
    best = (score(p0), np.array(p0, float))
    print(f"  đuôi: IoU khởi đầu {best[0]:.3f}")
    for it in range(1600):
        sc = 1.0 if it < 700 else (0.45 if it < 1200 else 0.2)
        p = best[1] + rs.uniform(-1, 1, len(p0)) * np.array(rng) * sc
        p[3] = np.clip(p[3], 0.02, 0.5)
        p[5] = np.clip(p[5], 0.2, 0.86)
        p[6] = np.clip(p[6], lam_t0 * 0.75, lam_t0 * 1.8)
        p[7] = np.clip(p[7], 1.0, 1.7)
        v = score(p)
        if v > best[0]:
            best = (v, p)
    print(f"  đuôi: IoU khớp {best[0]:.3f}, tham số {np.round(best[1], 3).tolist()}")
    return best


# ---------------------------------------------------------------- cấu hình dò dạng 1
DAT1 = {
    "bong": {"s": (0.72, 0.86), "r": (-6, 6), "around": (855, 610), "win": 45},
    "ground": 883,
    # chân: tỉ lệ, lấy x chân theo vùng chân concept, đáy bàn chân ở y
    "legs": {"chan_sn": ("chan_sau", 0.52, 883, 0), "chan_tn": ("chan_truoc", 0.52, 883, 0),
             # chân sau xa dời phải 70 px: hông nấp sau thân (đuôi nhấc lên thì không lộ cục hông lơ lửng)
             "chan_sx": ("chan_sau", 0.48, 870, 70), "chan_tx": ("chan_truoc_xa", 0.52, 872, 0)},
    # đuôi: (x0, y0, h0, s_lead, r0, q, lam_t, rho) khởi đầu và biên dò
    "duoi0": (656, 648, 176, 0.055, 185, 0.84, 0.75, 1.35),
    "duoi_rng": (18, 14, 14, 0.05, 25, 0.08, 0.08, 0.15),
}


def dat(k):
    if k == 2:
        return dat2()
    C = DAT1
    B = base(k)
    out_dir = os.path.join(B, "lai")
    _, ref, fg, ink = TL.doc_concept(k)
    H, W = fg.shape
    lab, names = doc_nhan(k)
    ref_lab = TL.lab_f(ref)
    res = {"ref_size": [W, H], "ground": C["ground"], "parts": {}}
    # 1) quả bóng GPT (nguồn vẽ bù) bằng SQDIFF
    bong = nap(k, "bong")
    c = C["bong"]
    b = TL.match(ref_lab, bong, np.linspace(c["s"][0], c["s"][1], 8), [None], range(c["r"][0], c["r"][1] + 1, 3), 0.5,
                 c["around"], c["win"])
    _, sx, _, r, cx, cy = b
    b = TL.match(ref_lab, bong, np.linspace(sx * 0.98, sx * 1.02, 5), [None], [r - 1, r, r + 1], 1.0, (cx, cy), 8)
    err, sx, sy, r, cx, cy = b
    res["parts"]["bong"] = {"sx": sx, "sy": sy, "r": r, "cx": cx, "cy": cy, "err": round(float(err), 1)}
    print(f"  bong: s={sx:.3f} r={r:+.0f} tâm=({cx:.0f},{cy:.0f}) sai={err:.0f}")
    ball_allow = mask_of(lab, names, "than", "mat_n", "mat_x", "mieng") | mask_of(lab, names, "chan_sn", "chan_tn")
    # 2) lòng miệng phủ kín lỗ miệng (nới 6 px)
    hole = cv2.dilate(mask_of(lab, names, "mieng").astype(np.uint8), np.ones((3, 3), np.uint8), iterations=6) > 0
    ys, xs = np.nonzero(hole)
    # nới lên trên 45 px sau môi trên: há miệng (lòng miệng theo hàm đi xuống) vẫn kín tới môi trên
    up = np.zeros_like(hole)
    for x in range(xs.min(), xs.max() + 1):
        col = np.nonzero(hole[:, x])[0]
        if len(col):
            up[max(0, col.min() - 45):col.min(), x] = True
    hole = hole | (up & ball_allow)
    ys, xs = np.nonzero(hole)
    lm = nap(k, "long_mieng")
    sc0 = (xs.max() - xs.min()) / max(1, (lm[:, :, 3] > 128).any(0).sum())
    p, miss, out = fit_cover(lm, hole, ball_allow, np.linspace(sc0 * 0.9, sc0 * 1.35, 8), range(-12, 13, 4),
                             (xs.mean(), ys.mean()), 9, sy_rng=np.linspace(sc0 * 0.9, sc0 * 1.4, 6), w_out=3.0)
    res["parts"]["long_mieng"] = p
    print(f"  long_mieng: s=({p['sx']:.2f},{p['sy']:.2f}) r={p['r']:+.0f} tâm=({p['cx']:.0f},{p['cy']:.0f}); hở {miss} px, lòi {out} px")
    # 3) mắt nhắm phủ kín đĩa mắt (bao lồi vùng mắt, nới 3 px)
    for mi, mat in (("mi_n", "mat_n"), ("mi_x", "mat_x")):
        eye = cv2.dilate(hull_mask(mask_of(lab, names, mat)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=3) > 0
        if mi == "mi_x":     # mắt xa: phần bị mắt gần che thì khỏi phủ
            eye &= ~hull_mask(mask_of(lab, names, "mat_n"))
        ys, xs = np.nonzero(eye)
        part = nap(k, mi)
        pa = part[:, :, 3] > 128
        sxe = (xs.max() - xs.min()) / max(1, pa.any(0).sum())
        sye = (ys.max() - ys.min()) / max(1, pa.any(1).sum())
        p, miss, out = fit_cover(part, eye, ball_allow, np.linspace(sxe * 0.95, sxe * 1.2, 6), range(-16, 9, 4),
                                 (xs.mean(), ys.mean()), 9, sy_rng=np.linspace(sye * 0.95, sye * 1.3, 6))
        res["parts"][mi] = p
        print(f"  {mi}: s=({p['sx']:.2f},{p['sy']:.2f}) r={p['r']:+.0f} tâm=({p['cx']:.0f},{p['cy']:.0f}); còn hở {miss} px, lòi {out} px")
    # 4) chân: đặt theo x bàn chân concept, đáy ở mặt đất
    for nm, (img, s, yb, dxl) in C["legs"].items():
        m = mask_of(lab, names, nm)
        ys, xs = np.nonzero(m)
        foot = xs[ys > ys.max() - 30]
        part = nap(k, img)
        wp, pm = warp_mask(part, s, s, 0)
        yy, xx = np.nonzero(pm)
        cx = float(foot.mean()) + dxl
        cy = yb - (yy.max() - wp.shape[0] / 2)
        res["parts"][nm] = {"img": img, "sx": s, "sy": s, "r": 0.0, "cx": cx, "cy": float(cy)}
        print(f"  {nm}: {img} s={s} tâm=({cx:.0f},{cy:.0f}), đỉnh hông y={cy - wp.shape[0] / 2:.0f}")
    # 5) lưỡi (clip chết): gốc trong lòng miệng
    lp = res["parts"]["long_mieng"]
    res["parts"]["luoi"] = {"sx": lp["sx"], "sy": lp["sx"], "r": -25.0, "goc": (lp["cx"] - 10, lp["cy"] + 8)}
    # 6) đuôi cuộn
    duoi = nap(k, "duoi")
    prof = tail_profile(duoi)
    T = mask_of(lab, names, "duoi")
    care = ~(mask_of(lab, names, "than", "mat_n", "mat_x", "mieng", "chan_sn", "chan_tn", "chan_sx"))
    best = fit_tail(T, care, prof, C["duoi0"], C["duoi_rng"], C["duoi0"][6])
    res["duoi"] = {"p": [float(v) for v in best[1]], "iou": float(best[0]), "prof": prof}
    json.dump(res, open(os.path.join(out_dir, "dat.json"), "w"), indent=1)
    so_ghep(k, res)


def so_ghep(k, res):
    """ghép thử mảnh GPT lên concept (đuôi theo đường xoắn đã khớp): concept | ghép | sai khác."""
    B = base(k)
    _, ref, fg, _ = TL.doc_concept(k)
    H, W = fg.shape
    lab, names = doc_nhan(k)
    comp = np.zeros((H, W, 4), np.uint8)
    P = res["parts"]
    # đuôi
    x0, y0, h0, sl, r0, q, lam_t, rho = res["duoi"]["p"]
    prof = res["duoi"]["prof"]
    lam_len = lam_t * rho
    Lp = len(prof["up"]) * lam_len
    pts, th, s = centerline((x0, y0, h0, sl, r0, q), Lp, 400)
    tm = ribbon_mask((H, W), pts, th, s, prof, lam_t, lam_len, 1.0)
    comp[tm] = (90, 170, 230, 255)
    for nm in ("chan_sx", "chan_tx"):
        t = P[nm]
        wp = TL.warp(nap(k, t["img"]), t["sx"], t["sy"], 0)
        TL.paste(comp, wp, t["cx"], t["cy"])
    than = np.dstack([ref, np.where(mask_of(lab, names, "than", "mat_n", "mat_x", "mieng"), 255, 0).astype(np.uint8)])
    comp = np.where(than[:, :, 3:4] > 0, than, comp).astype(np.uint8)
    for nm in ("chan_sn", "chan_tn"):
        t = P[nm]
        wp = TL.warp(nap(k, t["img"]), t["sx"], t["sy"], 0)
        TL.paste(comp, wp, t["cx"], t["cy"])
    cfg = comp[:, :, 3] > 128
    iou = float((cfg & fg).sum() / max(1, (cfg | fg).sum()))
    rgb = np.where(cfg[..., None], comp[:, :, :3], 255).astype(np.uint8)
    diff = np.full_like(ref, 255)
    diff[fg & ~cfg] = (230, 60, 60)
    diff[~fg & cfg] = (60, 110, 230)
    diff[fg & cfg] = (205, 205, 205)
    Image.fromarray(np.concatenate([ref, rgb, diff], 1)).save(os.path.join(B, "lai", "so_ghep.png"))
    print(f"  IoU ghép (thân concept + chân GPT + đuôi khớp) / concept = {iou:.3f}")
    res["iou_ghep"] = iou
    json.dump(res, open(os.path.join(B, "lai", "dat.json"), "w"), indent=1)


# ---------------------------------------------------------------- lớp thân cắt từ concept + vẽ bù
def lai(k):
    if k == 2:
        return lai2()
    B = base(k)
    out_dir = os.path.join(B, "lai")
    _, ref, fg, ink = TL.doc_concept(k)
    H, W = fg.shape
    lab, names = doc_nhan(k)
    res = json.load(open(os.path.join(out_dir, "dat.json")))
    P = res["parts"]
    lop = {"ref_size": [W, H], "ground": res["ground"], "lop": {}}
    if k == 1:
        k3 = np.ones((3, 3), np.uint8)
        body = mask_of(lab, names, "than", "mat_n", "mat_x")
        # nét mực giáp thân (viền thân đè lên đuôi, chân xa) thuộc về thân: thân đứng trước nên viền phải liền
        edge = ink & (cv2.dilate(body.astype(np.uint8), k3, iterations=5) > 0) & mask_of(lab, names, "duoi", "chan_sx", "chan_tx")
        body |= edge
        # lỗ miệng: vùng miệng + phần đỏ hồng sót trong bao lồi miệng (chóp lưỡi), trừ nét mực môi
        mh = hull_mask(mask_of(lab, names, "mieng"))
        rr, gg, bb_ = ref[..., 0].astype(int), ref[..., 1].astype(int), ref[..., 2].astype(int)
        reddish = (rr > gg + 40) & (rr > bb_ + 10)
        hole0 = mask_of(lab, names, "mieng") | (mh & reddish & ~ink)
        hole = cv2.erode(hole0.astype(np.uint8), k3, iterations=1) > 0
        body |= mask_of(lab, names, "mieng") & ~hole                 # viền môi phía trong: giữ với thân
        body &= ~hole
        rgba = np.dstack([ref, np.where(body, 255, 0).astype(np.uint8)])
        # vẽ bù chỗ bốn chân che (nới 5 px để lấy cả nét viền chân) từ quả bóng GPT đã đặt; chỗ GPT không phủ thì trong suốt
        # quả bóng GPT khớp lại theo bóng dáng nửa dưới (sx, sy riêng) để viền đáy trùng viền concept
        bong = nap(k, "bong")
        t = P["bong"]
        legs = mask_of(lab, names, "chan_sn", "chan_tn", "chan_tx")
        ball_full = body | legs
        yb0 = 640
        lower = np.zeros((H, W), bool)
        lower[yb0:] = True
        seen = body & lower & ~(cv2.dilate(legs.astype(np.uint8), k3, iterations=6) > 0)   # viền đáy concept thấy được
        best = None
        for sx in np.linspace(t["sx"] * 0.96, t["sx"] * 1.04, 9):
            for sy in np.linspace(t["sy"] * 0.96, t["sy"] * 1.04, 9):
                _, m = warp_mask(bong, sx, sy, t["r"])
                for dx in range(-8, 9, 2):
                    for dy in range(-8, 9, 2):
                        pm = place_mask(H, W, m, t["cx"] + dx, t["cy"] + dy) & lower
                        # khớp phần thấy được, phần chân che thì không tính
                        okm = ~(cv2.dilate(legs.astype(np.uint8), k3, iterations=6) > 0)
                        a, b = pm & okm, seen
                        v = (a & b).sum() / max(1, (a | b).sum())
                        if best is None or v > best[0]:
                            best = (v, sx, sy, t["cx"] + dx, t["cy"] + dy)
        _, sx, sy, cx, cy = best
        print(f"  bóng GPT khớp nửa dưới: IoU {best[0]:.3f} s=({sx:.3f},{sy:.3f}) tâm=({cx:.0f},{cy:.0f})")
        canvas = np.zeros((H, W, 4), np.uint8)
        TL.paste(canvas, TL.warp(bong, sx, sy, t["r"]), cx, cy)
        # dải dưới (y > yband) lấy cả từ bóng GPT, hoà dần 14 px trong vùng bụng vàng; trên dải: chỗ chân che vẫn vá
        yband = 742
        ramp = np.clip((np.arange(H) - yband) / 14.0, 0, 1)[:, None] * np.ones((1, W))
        region = (ball_full | (canvas[:, :, 3] > 40)) & (np.arange(H)[:, None] >= yband)
        gpt_a = canvas[:, :, 3].astype(np.float32) / 255
        cur_a = rgba[:, :, 3].astype(np.float32) / 255
        wgt = np.where(region, ramp, 0.0)
        wgt[region & (cur_a < 0.5)] = 1.0          # chỗ chân concept đã bỏ: lấy hẳn bóng GPT, không hoà với trong suốt
        hid = (cv2.dilate(legs.astype(np.uint8), k3, iterations=5) > 0) & ball_full & ~region
        take = hid & (canvas[:, :, 3] > 160)
        wgt[take] = 1.0
        new_rgb = rgba[:, :, :3] * (1 - wgt[..., None]) + canvas[:, :, :3] * wgt[..., None]
        new_a = cur_a * (1 - wgt) + gpt_a * wgt
        new_a[hid & ~take] = 0
        rgba = np.dstack([new_rgb, new_a * 255]).clip(0, 255).astype(np.uint8)
        print(f"  thân: dải đáy y>{yband} từ bóng GPT, vá {int(take.sum())} px chỗ chân che; nối viền {int(edge.sum())} px; "
              f"lỗ miệng {int(hole.sum())} px")
        a = rgba[:, :, 3].astype(np.float32) / 255
        a = cv2.GaussianBlur(a, (3, 3), 0.8)
        rgba[:, :, 3] = (np.clip(a * 1.15, 0, 1) * 255).astype(np.uint8)
        rgba[hole, 3] = 0
        ys, xs = np.nonzero(rgba[:, :, 3] > 8)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        Image.fromarray(rgba[y0:y1, x0:x1], "RGBA").save(os.path.join(out_dir, "than.png"))
        lop["lop"]["than"] = {"x0": x0, "y0": y0, "w": x1 - x0, "h": y1 - y0}
        # mí nhắm: vân mí GPT co về khung đĩa mắt concept, cắt theo đĩa, giữ vòng nét mực của concept (phủ kín, hở 0 px)
        near_disc = hull_mask(mask_of(lab, names, "mat_n"))
        for mi, mat in (("mi_n", "mat_n"), ("mi_x", "mat_x")):
            disc = cv2.dilate(hull_mask(mask_of(lab, names, mat)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2) > 0
            if mi == "mi_x":
                disc &= ~cv2.dilate(near_disc.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1).astype(bool)
            ys, xs = np.nonzero(disc)
            dx0, dy0, dx1, dy1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            part = nap(k, mi)
            bb = np.nonzero(part[:, :, 3] > 128)
            part = part[bb[0].min():bb[0].max() + 1, bb[1].min():bb[1].max() + 1]
            # mí GPT là nửa vòm: co cho bề ngang = đĩa, bề cao = 1,12 đĩa, đáy mí trùng đáy đĩa
            pw, ph = dx1 - dx0, int((dy1 - dy0) * 1.12)
            wp = cv2.resize(part, (int(pw), int(ph)), interpolation=cv2.INTER_AREA)
            canvas = np.zeros((H, W, 4), np.uint8)
            canvas[dy1 - ph:dy1, dx0:dx1] = wp[-min(ph, dy1):]
            blue = np.median(wp[(wp[:, :, 3] > 200) & (wp[:, :, :3].sum(2) > 200)][:, :3], 0).astype(np.uint8)
            layer = np.zeros((H, W, 4), np.uint8)
            got = disc & (canvas[:, :, 3] > 128)
            layer[got] = canvas[got]
            rest = disc & ~got
            layer[rest, :3] = blue
            layer[disc, 3] = 255
            ring = disc & ~cv2.erode(disc.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=6).astype(bool) & ink
            layer[ring, :3] = ref[ring]
            miss = int((disc & (layer[:, :, 3] < 128)).sum())
            a = layer[:, :, 3].astype(np.float32) / 255
            layer[:, :, 3] = (np.clip(cv2.GaussianBlur(a, (3, 3), 0.7) * 1.2, 0, 1) * 255).astype(np.uint8)
            Image.fromarray(layer[dy0:dy1, dx0:dx1], "RGBA").save(os.path.join(out_dir, mi + ".png"))
            lop["lop"][mi] = {"x0": int(dx0), "y0": int(dy0), "w": int(dx1 - dx0), "h": int(dy1 - dy0)}
            print(f"  {mi}: đĩa mắt ({dx0},{dy0}) {dx1 - dx0}x{dy1 - dy0}; vá {int(rest.sum())} px màu mí; còn hở {miss} px")
        # mặt nạ vùng (toạ độ concept) cho trọng số: hàm dưới, mắt, bụng, miệng
        for nm in ("mat_n", "mat_x", "mieng"):
            m = hull_mask(mask_of(lab, names, nm))
            ys, xs = np.nonzero(m)
            lop["lop"]["vung_" + nm] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        print(f"  than ({x0},{y0}) {x1 - x0}x{y1 - y0}")
    json.dump(lop, open(os.path.join(out_dir, "lop.json"), "w"), indent=1)


# ---------------------------------------------------------------- dạng 2
def mouth_hole2(ref, lab, names, ink):
    """lỗ miệng dạng 2: phần đỏ hồng (lòng miệng + lưỡi) trong vùng miệng, trừ răng (sáng) và nét mực."""
    mh = hull_mask(mask_of(lab, names, "mieng"))
    r, g, b = ref[..., 0].astype(int), ref[..., 1].astype(int), ref[..., 2].astype(int)
    reddish = (r > g + 35) & (r > b + 5)
    m = (mask_of(lab, names, "mieng") | mh) & reddish & ~ink
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
    return m


def dat2():
    k = 2
    B = base(k)
    out_dir = os.path.join(B, "lai")
    _, ref, fg, ink = TL.doc_concept(k)
    H, W = fg.shape
    lab, names = doc_nhan(k)
    ref_lab = TL.lab_f(ref)
    ys, xs = np.nonzero(fg)
    res = {"ref_size": [W, H], "ground": int(ys.max()), "parts": {}}
    bong = nap(k, "bong")
    b = TL.match(ref_lab, bong, np.linspace(0.80, 0.98, 8), [None], range(-4, 5, 2), 0.5, (770, 430), 50)
    _, sx, _, r, cx, cy = b
    b = TL.match(ref_lab, bong, np.linspace(sx * 0.98, sx * 1.02, 5), [None], [r - 1, r, r + 1], 1.0, (cx, cy), 8)
    err, sx, sy, r, cx, cy = b
    res["parts"]["bong"] = {"sx": sx, "sy": sy, "r": r, "cx": cx, "cy": cy, "err": round(float(err), 1)}
    print(f"  bong: s={sx:.3f} r={r:+.0f} tâm=({cx:.0f},{cy:.0f}) sai={err:.0f}")
    allow = mask_of(lab, names, "than", "tui", "la", "sung_n", "sung_x", "mat_n", "mat_x", "mieng")
    hole = cv2.dilate(mouth_hole2(ref, lab, names, ink).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=5) > 0
    ys, xs = np.nonzero(hole)
    up = np.zeros_like(hole)
    for x in range(xs.min(), xs.max() + 1):
        col = np.nonzero(hole[:, x])[0]
        if len(col):
            up[max(0, col.min() - 28):col.min(), x] = True
    need = hole | (up & allow)
    ys, xs = np.nonzero(need)
    lm = nap(k, "long_mieng")
    sc0 = (xs.max() - xs.min()) / max(1, (lm[:, :, 3] > 128).any(0).sum())
    p, miss, out = fit_cover(lm, need, allow, np.linspace(sc0 * 0.95, sc0 * 1.25, 7), range(-8, 9, 4), (xs.mean(), ys.mean()), 9,
                             sy_rng=np.linspace(sc0 * 0.9, sc0 * 1.8, 7), w_out=14.0)
    res["parts"]["long_mieng"] = p
    print(f"  long_mieng: s=({p['sx']:.2f},{p['sy']:.2f}) r={p['r']:+.0f} tâm=({p['cx']:.0f},{p['cy']:.0f}); hở {miss} px, lòi {out} px")
    # chân xa: đáy bàn chân ở đáy vùng chân concept, mép ngoài trùng mép ngoài vùng chân
    for nm, img, side in (("chan_sx", "chan_sau_xa", "trai"), ("chan_tx", "chan_truoc_xa", "phai")):
        m = mask_of(lab, names, nm)
        ys, xs = np.nonzero(m)
        part = nap(k, img)
        if nm == "chan_sx":
            # chân sau xa: đùi phải nấp sau đùi gần -> tâm đĩa đùi (dải 5–30 % trên của hình) tới (400, 488), đáy bàn chân ở đáy
            # vùng chân concept; tỉ lệ theo khoảng hông -> đáy
            pa = part[:, :, 3] > 128
            py_, px_ = np.nonzero(pa)
            top, bot = py_.min(), py_.max()
            band = (py_ > top + 0.05 * (bot - top)) & (py_ < top + 0.30 * (bot - top))
            hx, hy = float(px_[band].mean()), float(py_[band].mean())
            s = (ys.max() - 488) / max(1.0, bot - hy)
            c_img = np.array([part.shape[1] / 2, part.shape[0] / 2])
            cx = 400 - (hx - c_img[0]) * s
            cy = 488 - (hy - c_img[1]) * s
            wp, _ = warp_mask(part, s, s, 0)
        else:
            s = 0.53
            wp, pm = warp_mask(part, s, s, 0)
            yy, xx = np.nonzero(pm)
            cy = ys.max() - (yy.max() - wp.shape[0] / 2)
            cx = (xs.min() - (xx.min() - wp.shape[1] / 2)) if side == "trai" else (xs.max() - (xx.max() - wp.shape[1] / 2))
        res["parts"][nm] = {"img": img, "sx": s, "sy": s, "r": 0.0, "cx": float(cx), "cy": float(cy)}
        print(f"  {nm}: {img} s={s} tâm=({cx:.0f},{cy:.0f}) đỉnh y={cy - wp.shape[0] / 2:.0f}")
    lp = res["parts"]["long_mieng"]
    res["parts"]["luoi"] = {"sx": lp["sx"], "sy": lp["sx"], "r": -18.0, "goc": (lp["cx"] - 40, lp["cy"] + 6)}
    json.dump(res, open(os.path.join(out_dir, "dat.json"), "w"), indent=1)


def lai2():
    k = 2
    B = base(k)
    out_dir = os.path.join(B, "lai")
    _, ref, fg, ink = TL.doc_concept(k)
    H, W = fg.shape
    lab, names = doc_nhan(k)
    res = json.load(open(os.path.join(out_dir, "dat.json")))
    P = res["parts"]
    k3 = np.ones((3, 3), np.uint8)
    lop = {"ref_size": [W, H], "ground": res["ground"], "lop": {}}
    body = mask_of(lab, names, "than", "tui", "la", "sung_n", "sung_x", "mat_n", "mat_x", "mieng")
    near = mask_of(lab, names, "chan_sn", "chan_tn")
    far = mask_of(lab, names, "chan_sx", "chan_tx")
    edge = ink & (cv2.dilate(body.astype(np.uint8), k3, iterations=5) > 0) & far       # viền thân đè lên chân xa
    body |= edge
    hole = mouth_hole2(ref, lab, names, ink)
    hole = cv2.erode(hole.astype(np.uint8), k3, iterations=1) > 0
    body &= ~hole
    rgba = np.dstack([ref, np.where(body, 255, 0).astype(np.uint8)])
    # vẽ bù thân chỗ bốn chân che (nới 4 px) từ thân GPT không chân đã đặt; chỗ GPT không phủ thì trong suốt
    t = P["bong"]
    canvas = np.zeros((H, W, 4), np.uint8)
    TL.paste(canvas, TL.warp(nap(k, "bong"), t["sx"], t["sy"], t["r"]), t["cx"], t["cy"])
    hid = (near | far) & ~edge                       # chỉ đúng chỗ chân che, không nới (nới thì lộ viền bụng GPT quanh chân)
    # riêng sau chân trước gần (chân nhấc lên khi chưởng, chồm): thay cả vùng nới 10 px dưới ngực bằng thân GPT cho liền, bỏ mẩu
    # vụn của concept (vệt cánh tay, nét viền) còn sót ở đó
    # lớp chân gần giữ cả nét viền (mực trong 4 px quanh vùng chân); thân được thay bằng thân GPT đúng phần lớp chân che
    near_ink = ink & (cv2.dilate(near.astype(np.uint8), k3, iterations=4) > 0)
    nf = cv2.morphologyEx((near | near_ink).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ff = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(nf, ff, (0, 0), 2)
    hid |= (nf != 2) & fg & ~edge
    take = hid & (canvas[:, :, 3] > 160)
    rgba[take, :3] = canvas[take, :3]
    rgba[take, 3] = 255
    rgba[hid & ~take, 3] = 0
    rgba[hole, 3] = 0
    print(f"  thân: vẽ bù {int(take.sum())} px chỗ chân che từ thân GPT, bỏ {int((hid & ~take).sum())} px; lỗ miệng {int(hole.sum())} px")

    def save(nm, layer):
        a = layer[:, :, 3].astype(np.float32) / 255
        layer[:, :, 3] = (np.clip(cv2.GaussianBlur(a, (3, 3), 0.8) * 1.15, 0, 1) * 255).astype(np.uint8)
        ys, xs = np.nonzero(layer[:, :, 3] > 8)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        Image.fromarray(layer[y0:y1, x0:x1], "RGBA").save(os.path.join(out_dir, nm + ".png"))
        lop["lop"][nm] = {"x0": x0, "y0": y0, "w": x1 - x0, "h": y1 - y0}
        print(f"  {nm} ({x0},{y0}) {x1 - x0}x{y1 - y0}")

    save("than", rgba)
    hole_l = cv2.dilate(hole.astype(np.uint8), k3, iterations=0) > 0
    rgba2 = np.array(Image.open(os.path.join(out_dir, "than.png")))
    # hai chân gần cắt từ concept (gồm nét viền chân)
    for nm in ("chan_sn", "chan_tn"):
        m = mask_of(lab, names, nm)
        m |= ink & (cv2.dilate(m.astype(np.uint8), k3, iterations=4) > 0)
        # lấp khe vụn bên trong chân (mẩu nhãn thân sót trong cánh tay): đóng 5x5 rồi lấp lỗ kín
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
        mm = m.astype(np.uint8).copy()
        ff = np.zeros((H + 2, W + 2), np.uint8)
        cv2.floodFill(mm, ff, (0, 0), 2)
        m = (mm != 2) & fg
        m = (cv2.dilate(m.astype(np.uint8), k3, iterations=2) > 0) & fg          # mép mềm không hở xuống lớp thân
        save(nm, np.dstack([ref, np.where(m, 255, 0).astype(np.uint8)]))
    # mí nhắm: thuỳ dưới (con mắt) của mí GPT co về khung đĩa mắt concept, cắt theo đĩa, giữ vòng mực concept
    for mi, mat in (("mi_n", "mat_n"), ("mi_x", "mat_x")):
        disc = cv2.dilate(hull_mask(mask_of(lab, names, mat)).astype(np.uint8), k3, iterations=3) > 0
        ys, xs = np.nonzero(disc)
        dx0, dy0, dx1, dy1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        part = nap(k, mi)
        a = part[:, :, 3] > 128
        yy, xx = np.nonzero(a)
        lobe = part[yy.min() + int(0.42 * (yy.max() - yy.min())):yy.max() + 1, xx.min():xx.max() + 1]   # bỏ sừng, mày phía trên
        wp = cv2.resize(lobe, (int(dx1 - dx0), int(dy1 - dy0)), interpolation=cv2.INTER_AREA)
        layer = np.zeros((H, W, 4), np.uint8)
        sub = layer[dy0:dy1, dx0:dx1]
        dsub = disc[dy0:dy1, dx0:dx1]
        got = dsub & (wp[:, :, 3] > 100)
        sub[got] = wp[got]
        sel = (wp[:, :, 3] > 200) & (wp[:, :, :3].astype(int).sum(2) > 150)
        cob = np.median(wp[sel][:, :3], 0).astype(np.uint8) if sel.any() else np.array([36, 87, 197], np.uint8)
        rest = dsub & ~got
        sub[rest, :3] = cob
        sub[dsub, 3] = 255
        ring = disc & ~(cv2.erode(disc.astype(np.uint8), k3, iterations=4) > 0) & ink
        layer[ring, :3] = ref[ring]
        miss = int((hull_mask(mask_of(lab, names, mat)) & (layer[:, :, 3] < 128)).sum())
        a2 = layer[:, :, 3].astype(np.float32) / 255
        layer[:, :, 3] = (np.clip(cv2.GaussianBlur(a2, (3, 3), 0.7) * 1.2, 0, 1) * 255).astype(np.uint8)
        Image.fromarray(layer[dy0:dy1, dx0:dx1], "RGBA").save(os.path.join(out_dir, mi + ".png"))
        lop["lop"][mi] = {"x0": int(dx0), "y0": int(dy0), "w": int(dx1 - dx0), "h": int(dy1 - dy0)}
        print(f"  {mi}: đĩa mắt ({dx0},{dy0}) {dx1 - dx0}x{dy1 - dy0}; vá {int(rest.sum())} px; còn hở {miss} px")
    for nm in ("tui", "la", "sung_n", "sung_x", "mat_n", "mat_x", "mieng", "chan_sn", "chan_tn"):
        m = mask_of(lab, names, nm)
        ys, xs = np.nonzero(m)
        lop["lop"]["vung_" + nm] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    for nm in ("tui", "la"):
        m = mask_of(lab, names, nm)
        pts = np.stack(np.nonzero(m)[::-1], 1).astype(np.int32)
        h = cv2.convexHull(pts)[:, 0, :]
        lop["lop"]["da_giac_" + nm] = h.tolist()
    json.dump(lop, open(os.path.join(out_dir, "lop.json"), "w"), indent=1)
