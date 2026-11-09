# -*- coding: utf-8 -*-
"""Thú huyền thoại .atomik của đảo Thủy (2026-11-08): rig ĐƠN GIẢN kiểu Clash of Critters dựng từ MỘT ảnh liền.

Người dùng dặn: animation đơn giản, không chia nhiều khớp, học Clash of Critters (thú như họ), hiệu ứng bù vào là chính.
Số đo Critters (9 con): đòn 0,9-1,2 s, lấy đà 30-45%, ra đòn 2-3 khung, trúng ở 0,3-0,57 s, đầu xoay gấp 2-3 lần thân,
thân nén giãn tới ±15%, idle 2 s nhún 1-7%H, đuôi trễ 1/3 vòng, tai ngược pha, chân không IK (kéo dài, co lại), thân là một
khối. Hiệu ứng theo cách pixelfx: đà ngược chiều cú đánh, khựng 0,1 s lúc trúng, hạt văng có biến thiên, nhanh vào chậm ra,
tan dần; nhưng hình là ảnh vẽ tay tô phẳng (luật game: không glow, không additive).

Xương: root, move (lao, nhảy), shadow, ground (bàn chân bám), base (gốc ở đất: nghiêng, nén giãn), body (thân một khối),
head (đầu cứng), phụ kiện cứng (tai, sừng, vây, cánh, càng, đạo cụ: mỗi cái một xương), đuôi một chuỗi 2-4 đốt (lắc khoá
tay lệch pha, không lò xo). Chân: lưới nửa trên theo thân, bàn chân theo ground.

Cấu hình từng dạng ở beasts_cfg.py (vùng, khớp, lớp, kiểu đòn, hiệu ứng).

    D:/spine-venv/Scripts/python -I ArtGen/Spine/beast.py <id> nhan <k> | rig <k> | all | show <k> <clip> t1,t2 | grid <k>
"""
import json
import math
import os
import pickle
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import longrig as L  # noqa: E402
import rig as riglib  # noqa: E402
import thuy_long as T  # noqa: E402
import thuy_long_lien as Q  # noqa: E402
from longrig import curve  # noqa: E402

H = T.H
FXD = os.path.join(HERE, "inbox", "fx")  # ảnh hiệu ứng riêng (cắt từ tờ GPT), tên.png

# 2026-11-09: người dùng chê ghép lớp (cắt bộ phận + vá phần bị che) lệch, hở. Từ nay cả con là MỘT lưới liền: không cắt lớp,
# không vá; trọng số hoà mềm giữa các vùng (đầu, đuôi, chân uốn, không bao giờ hở). Chỉ phần ghi trong "sep" của dạng (vũ khí,
# cánh che thân... khi thật cần) mới thành lớp riêng.
ONE = True
HEADK = 0.55   # một lưới: đầu xoay ít (cổ uốn mềm), nghiêng cả người bù vào
BLEND = 26     # px: bề rộng dải hoà trọng số giữa hai vùng
NFLY, NFAR = 5, 8
RANGED = {"song", "breath", "roar", "throw"}                       # đòn đánh từ xa: đạn bay tới đối thủ
FAR_SKILL = {"erupt", "storm", "barrage", "summon_prop", "shockwave"}  # chiêu cuối đứng tại chỗ, hiệu ứng ở chỗ đối thủ
LUNGE_SKILL = {"charge", "slide", "spin_dash", "combo"}               # chiêu cuối lao tới (trận kéo tới đối thủ)


# ---------------------------------------------------------------- cấu hình
def cfg(hid):
    import beasts_cfg
    return beasts_cfg.HEROES[hid]


def code(hid, k):
    return f"{hid}_{k}"


def base(hid, k):
    return os.path.join(HERE, "inbox", code(hid, k))


def src(hid, k):
    """L1_duyet.png (Claude chọn) nếu có, không thì ảnh L1_lien*.png mới nhất (gen lại thì Codex lưu L1_lien_2.png...)."""
    p = os.path.join(base(hid, k), "L1_duyet.png")
    if os.path.isfile(p):
        return p
    d = os.path.join(base(hid, k), "tai_ve")
    c = sorted([f for f in os.listdir(d) if f.startswith("L1_lien") and f.endswith(".png")],
               key=lambda f: os.path.getmtime(os.path.join(d, f))) if os.path.isdir(d) else []
    if c:
        return os.path.join(d, c[-1])
    raise SystemExit("chưa có concept: " + code(hid, k))


def out_dir(hid, k):
    return os.path.join(base(hid, k), "rig")


def setup_labels(hid, k, F):
    Q.CFG["src"] = lambda kk: src(hid, k)
    Q.LAYERS[k] = F["layers"]
    Q.MARKD[k] = F["marks"]
    Q.OVERRIDE[k] = F.get("override", {})
    Q.CLAMP[k] = F.get("clamp", {})
    Q.LINEAR_Y.clear()
    Q.FULL_SHEET.clear()
    Q.WARM_FIX.clear()


def load(hid, k, F):
    """ảnh + mặt nạ hình như Q.load; mảng trắng khép kín lớn bị Q.load coi là khe nền (giữa chân, giữa tay) nhưng tròng mắt, ngọc
    trai cũng là mảng trắng khép kín: điểm "keep" của dạng trả mảng chứa nó về hình."""
    rgb, fg = Q.load(k)
    # lỗ trong hình (vùng khép kín không thuộc hình, không bao giờ là nền ngoài): giấy trắng thật đều tăm tắp (~254, không vân)
    # thì là khe; có vân sáp hoặc ngả màu (lông kem, tròng mắt, bọt) thì trả về hình; "keep"/"drop" của dạng ép tay
    holes = (fill_holes(fg) > 0) & (fg == 0)
    n, cl, st, _ = cv2.connectedComponentsWithStats(holes.astype(np.uint8), connectivity=8)
    gray = rgb.mean(2)
    mn = rgb.min(2).astype(np.float32)
    add = np.zeros_like(fg)
    keep_ids = {cl[int(y), int(x)] for (x, y) in F.get("keep", [])}
    drop_ids = {cl[int(y), int(x)] for (x, y) in F.get("drop", [])}
    for c in range(1, n):
        if c in drop_ids:
            continue
        m = cl == c
        core = cv2.erode(m.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
        if core.sum() < 30:
            core = m
        painted = float(mn[core].mean()) < 247 or float(gray[core].std()) > 3.5
        if c in keep_ids or painted:
            add |= m.astype(np.uint8)
    if add.any():
        add = cv2.dilate(add, np.ones((5, 5), np.uint8)) & fill_holes(fg)
        fg = ((fg > 0) | (add > 0)).astype(np.uint8)
    # "close_fill": khung (x0, y0, x1, y1) có hình viền hở một khe (lòng mây, sợi râu trắng): khép nét viền rồi lấp lòng
    for box in F.get("close_fill", []):
        x0, y0, x1, y1 = box[:4]
        sub = (rgb[y0:y1, x0:x1].min(2) < 235).astype(np.uint8)
        cl = cv2.morphologyEx(sub, cv2.MORPH_CLOSE, disk(box[4] if len(box) > 4 else 6))
        filled = fill_holes(cl)
        fg[y0:y1, x0:x1] = np.maximum(fg[y0:y1, x0:x1], filled)
    return rgb, fg


def under_image(hid, k, lv, rgb, fg, lab, names, F):
    """ảnh lớp dưới lv do GPT vẽ (inbox/<mã>/tai_ve/L2_duoi<lv>.png, mới nhất), căn khớp concept bằng ECC affine trên phần
    vẫn còn và nhìn thấy ở cả hai ảnh; trả (ảnh RGB đã căn, mặt nạ hình) hoặc None. Lưu bản căn rig/duoi<lv>_khop.png để soi."""
    d = os.path.join(base(hid, k), "tai_ve")
    cands = sorted([f for f in os.listdir(d) if f.startswith(f"L2_duoi{lv}") and f.endswith(".png")],
                   key=lambda f: os.path.getmtime(os.path.join(d, f))) if os.path.isdir(d) else []
    if not cands:
        return None
    im = np.array(Image.open(os.path.join(d, cands[-1])).convert("RGB"))
    if im.shape[:2] != rgb.shape[:2]:
        im = cv2.resize(im, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_AREA)
    import build_parts as BP
    remove, keep = BP.removal_sets(F)[lv]
    vis = np.isin(lab, [names.index(p) for p in keep if p in names]) & (fg > 0)
    vis = cv2.erode(vis.astype(np.uint8), disk(6))
    g1 = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    g2 = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    sc = 0.5
    a1, a2 = cv2.resize(g1, None, fx=sc, fy=sc), cv2.resize(g2, None, fx=sc, fy=sc)
    mk = cv2.resize(vis, None, fx=sc, fy=sc, interpolation=cv2.INTER_NEAREST)
    def ncc(w):  # tương quan trên vùng còn lại sau khi dời ảnh GPT theo w
        b = cv2.warpAffine(a2, w, (a1.shape[1], a1.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=1.0)
        m = mk > 0
        x, y = a1[m] - a1[m].mean(), b[m] - b[m].mean()
        return float((x * y).sum() / max(1e-6, np.sqrt((x * x).sum() * (y * y).sum())))
    ident = np.eye(2, 3, dtype=np.float32)
    c0 = ncc(ident)
    warp = ident.copy()
    try:
        cc, warp = cv2.findTransformECC(a1, a2, warp, cv2.MOTION_AFFINE,
                                        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-5), mk, 5)
    except cv2.error:
        cc, warp = -1.0, ident.copy()
    # GPT thường giữ đúng chỗ: chỉ nhận phép căn khi tốt hơn hẳn "không dời" và dời ít (ECC hay trôi khi vùng còn lại ít)
    if cc < c0 + 0.03 or abs(warp[0, 2]) > 8 or abs(warp[1, 2]) > 8:
        cc, warp = c0, ident.copy()
    warp[:, 2] /= sc
    al = cv2.warpAffine(im, warp, (rgb.shape[1], rgb.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                        borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    m = riglib.fg_mask(al) > 0
    print(f"  lớp dưới {lv}: {cands[-1]}, tương quan {cc:.3f}, dời ({warp[0, 2]:.1f}, {warp[1, 2]:.1f})")
    os.makedirs(out_dir(hid, k), exist_ok=True)
    Image.fromarray(al).save(os.path.join(out_dir(hid, k), f"duoi{lv}_khop.png"))
    if cc < 0.4:
        print(f"  lớp dưới {lv}: tương quan thấp, bỏ")
        return None
    return al, m


def drop_gaps(rgb, fg, lab):
    """khe giấy trắng nhỏ còn lẫn trong hình (Q.load chỉ bỏ khe > 3000 px) nằm GIỮA hai bộ phận (giữa gai bờm và cánh, giữa
    chân và bụng): bỏ khỏi hình, kẻo dính vào một lớp rồi thành vệt trắng khi lớp đó cử động. Lòng trắng mắt, răng, ngọc trai
    chỉ giáp một bộ phận nên giữ."""
    mn, mx = rgb.min(2).astype(np.int16), rgb.max(2).astype(np.int16)
    white = ((mn > 244) & (mx - mn < 12) & (fg > 0)).astype(np.uint8)
    n, cl, st, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
    k = np.ones((7, 7), np.uint8)
    dropped = 0
    gaps = np.zeros(fg.shape, np.uint8)
    for c in range(1, n):
        if st[c, cv2.CC_STAT_AREA] < 40:
            continue
        x, y, w, h = st[c, 0], st[c, 1], st[c, 2], st[c, 3]
        x0, y0, x1, y1 = max(0, x - 6), max(0, y - 6), min(fg.shape[1], x + w + 6), min(fg.shape[0], y + h + 6)
        m = cl[y0:y1, x0:x1] == c
        ring = (cv2.dilate(m.astype(np.uint8), k) > 0) & ~m
        labs = np.unique(lab[y0:y1, x0:x1][ring])
        labs = labs[labs >= 0]
        if len(labs) >= 2:
            fg[y0:y1, x0:x1][m] = 0
            lab[y0:y1, x0:x1][m] = -1
            gaps[y0:y1, x0:x1][m] = 1
            dropped += int(m.sum())
    if dropped:
        print(f"  bỏ {dropped} px khe trắng giữa các bộ phận")
    return fg, lab, gaps


def style_of(C, k, key, default=None):
    """kiểu của dạng k: khoá trong forms[k] trước, rồi của tướng (dict theo số dạng hoặc một giá trị chung)."""
    F = C["forms"].get(k, {})
    if key in F:
        return F[key]
    v = C.get(key, default)
    if isinstance(v, dict) and v and all(isinstance(x, int) for x in v):
        return v.get(k, default)
    return v


def one_layers(F):
    """một lưới: mọi phần chung lớp "main" (giữ thứ tự sau -> trước để vẽ tam giác), trừ phần "sep" (vũ khí, cánh che thân khi
    thật cần) thành lớp riêng sau hoặc trước."""
    sep = F.get("sep", {})
    allp = [p for _, ps, _ in F["layers"] for p in ps]
    back = [p for p in allp if sep.get(p) == "back"]
    front = [p for p in allp if sep.get(p) == "front"]
    main = [p for p in allp if p not in sep]
    return ([("sep_b", back, 14)] if back else []) + [("main", main, 0)] + ([("sep_f", front, 0)] if front else [])


def membership(lab, dom, ids, px):
    """độ thuộc vùng của từng pixel (nửa độ phân giải): lan đều 3x3 chỉ trong hình (không nhảy qua khe trắng), dải hoà rộng ~px
    quanh ranh giới hai vùng; trong lòng vùng vẫn 1. Trả mảng (số vùng, h/2, w/2), tổng mỗi pixel trong hình = 1."""
    L2 = lab[::2, ::2]
    D2 = (dom[::2, ::2] > 0).astype(np.float32)
    n = max(1, int(math.ceil(1.5 * (px / 4.0) ** 2)))
    den = cv2.blur(D2, (3, 3)) + 1e-6
    M = np.stack([((L2 == i) & (D2 > 0)).astype(np.float32) for i in ids])
    for _ in range(n):
        for j in range(len(ids)):
            M[j] = cv2.blur(M[j], (3, 3)) / den * D2
    return M


def spread_finite(D, n):
    """bản đồ quãng D (vô cực ngoài vùng) loang giá trị gần nhất ra ngoài n px."""
    big = np.float32(1e9)
    E = np.where(np.isfinite(D), D, big).astype(np.float32)
    k = np.ones((3, 3), np.uint8)
    for _ in range(n):
        m = E >= big
        if not m.any():
            break
        e = cv2.erode(E, k)
        E[m] = e[m]
    return np.where(E >= big, np.inf, E)


def paw_part(C, F, k, names):
    """chân dùng để vồ, đá (xương paw): khai "paw" hoặc chân gần phía trước."""
    p = style_of(C, k, "paw")
    if p:
        return p if p in names else None
    for cand in ("leg_fn", "leg_f", "leg_ff", "leg_d"):
        if cand in names and kind_of(F, cand) == "leg":
            return cand
    return None


def cut_gaps(tris, wts, XY, fg, sim_min=0.5):
    """một lưới: bỏ tam giác vắt qua khe (chỗ trong suốt) mà các đỉnh thuộc hai bộ phận cử động khác nhau (chóp đuôi sát móng,
    tai sát cánh): giữ thì phần này kéo phần kia thành vệt sọc. Chỗ hoà (gốc đuôi, cổ) đỉnh có trọng số gần nhau nên giữ."""
    names = sorted({b for w in wts for b, _ in w})
    ix = {b: i for i, b in enumerate(names)}
    Wm = np.zeros((len(wts), len(names)), np.float32)
    for i, w in enumerate(wts):
        for b, x in w:
            Wm[i, ix[b]] = x
    Wn = Wm / np.clip(np.linalg.norm(Wm, axis=1, keepdims=True), 1e-6, None)
    hole = fg == 0
    hh, ww = hole.shape
    keep = np.ones(len(tris), bool)
    for j, (a, b, c) in enumerate(tris):
        if min(Wn[a] @ Wn[b], Wn[b] @ Wn[c], Wn[a] @ Wn[c]) >= sim_min:
            continue
        P3 = XY[[a, b, c]]
        for x, y in (P3.mean(0), (P3[0] + P3[1]) / 2, (P3[1] + P3[2]) / 2, (P3[0] + P3[2]) / 2):
            if hole[min(hh - 1, max(0, int(round(y)))), min(ww - 1, max(0, int(round(x))))]:
                keep[j] = False
                break
    if (~keep).any():
        print(f"  cắt {int((~keep).sum())} tam giác vắt qua khe giữa hai bộ phận")
    return tris[keep]


def fill_small_holes(m, max_area):
    """lấp các lỗ (vùng không thuộc hình, khép kín) có diện tích dưới max_area."""
    m = (m > 0).astype(np.uint8)
    full = fill_holes(m)
    holes = (full > 0) & (m == 0)
    n, cl, st, _ = cv2.connectedComponentsWithStats(holes.astype(np.uint8), connectivity=4)
    out = m.copy()
    for c in range(1, n):
        if st[c, cv2.CC_STAT_AREA] < max_area:
            out[cl == c] = 1
    return out


def fill_holes(m):
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(m, dtype=np.uint8)
    cv2.drawContours(out, cs, -1, 1, -1)
    return out


def parts_of(F):
    return [p for _, ps, _ in F["layers"] for p in ps]


def kind_of(F, p):
    """chân: 'leg'; đuôi, rắn: ('chain', tên); còn lại cứng theo xương: tên phần là tên xương nếu có, không thì body."""
    kd = F.get("kinds", {})
    if p in kd:
        return kd[p]
    if p.startswith("leg"):
        return "leg"
    if p in F.get("chains", {}):
        return ("chain", p)
    if p in F["bones"]:
        return ("rigid", p)
    return ("rigid", "body")


def parent_of(F, b):
    pm = F.get("parent", {})
    if b in pm:
        return pm[b]
    for ch, (bones, par, _tip) in F.get("chains", {}).items():
        if b in bones:
            i = bones.index(b)
            return par if i == 0 else bones[i - 1]
    if b.startswith(("ear", "horn", "tuft", "mane", "whisk", "fin_h", "jaw")):
        return "head"
    return "body"


# ---------------------------------------------------------------- dựng rig
class Ctx:
    pass


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def build_rig(hid, k):
    C = cfg(hid)
    F = C["forms"][k]
    setup_labels(hid, k, F)
    rgb, fg = load(hid, k, F)
    names = parts_of(F)
    lab = Q.labels(k, rgb, fg)
    # khe giấy trắng giữa hai bộ phận: bỏ khỏi hình (trong suốt) và lưới không nối qua khe; giữ thì khe bị kéo giãn thành vệt
    # trắng khi đuôi, chân cử động
    fg, lab, gaps = drop_gaps(rgb, fg, lab)
    J = dict(F["bones"])
    rows = np.where(fg.any(1))[0]
    ground = float(F.get("ground", rows.max() - 6))
    top = float(F.get("top", rows.min()))
    ks = H / (ground - top)
    feet_x = float(J["base"][0])

    def S(p):
        return ((p[0] - feet_x) * ks, (ground - p[1]) * ks)

    R = L.Rig(code(hid, k))
    R.bone("root", None, 0, 0)
    R.bone("move", "root", 0, 0)
    R.bone("shadow", "root", 0, 0)
    # spin: xoay, lật cả con quanh giữa thân (lăn, quay quất đuôi, trượt bụng), chân bám đất (ground) cũng theo; base: gốc ở đất
    # (nghiêng, nén giãn)
    R.bone("spin", "move", S(J["base"])[0], 0.42 * H)
    R.bone("ground", "spin", 0, 0)
    R.bone("base", "spin", S(J["base"])[0], 0.0)
    made = {"root", "move", "shadow", "ground", "spin", "base"}
    # đồ bay ném được (bùa, hạt cánh quạt, bàn tay gỗ): xương flyp_<x> con của move (theo con lao tới; game kéo tới đối thủ
    # khi ném)
    throw = style_of(C, k, "throw") or []
    for b in throw:
        if b in J:
            R.bone("flyp_" + b, "move", *S(J[b]))
            made.add("flyp_" + b)
    todo = [b for b in J if b not in made]
    while todo:
        prog = False
        for b in list(todo):
            par = "base" if b == "body" else ("flyp_" + b if b in throw else parent_of(F, b))
            if par in made:
                R.bone(b, par, *S(J[b]))
                made.add(b)
                todo.remove(b)
                prog = True
        if not prog:
            raise SystemExit(f"xương thiếu cha: {todo}")
    mouth = S(F["mouth"])
    R.point("tip", F.get("mouth_bone", "head"), *mouth)

    # khung hình (toạ độ rig) để đặt hiệu ứng
    ys, xs = np.nonzero(fg)
    front = (xs.max() - feet_x) * ks
    back = (xs.min() - feet_x) * ks
    info = {"front": float(front), "back": float(back), "mouth": mouth, "len": float(front - back)}

    # bàn chân đánh (vồ, đá): xương "paw" con của ground ở đỉnh chân; nửa dưới chân theo paw thay vì bám đất
    paw = paw_part(C, F, k, names)
    if paw:
        pm_ = (lab == names.index(paw)) & (fg > 0)
        if pm_.any():
            yy_, xx_ = np.nonzero(pm_)
            ytop = yy_.min()
            sel = yy_ < ytop + 0.18 * (yy_.max() - ytop + 1)
            R.bone("paw", "ground", *S((float(xx_[sel].mean()), float(ytop))))
        else:
            paw = None
    info["paw"] = paw

    # lớp: miền = phần của lớp + dải mọc thêm dưới các lớp trên
    layers = one_layers(F) if ONE else F["layers"]
    above = set()
    specs = []
    for name, ps, grow in reversed(layers):
        specs.append((name, ps, grow, set(above)))
        above |= set(ps)
    specs.reverse()
    R.slot("shadow", "shadow", "shadow")
    R.images["shadow"] = T.shadow_image(0.8 * (front - back))
    R.region("shadow", "shadow", "shadow", "shadow", (front + back) * 0.5, 0)
    fx_setup(R, C, info, k)
    for s_ in FX_BACK:
        fx_slot(R, s_)
    lay_dbg, stats = [], []
    legtop = {}
    for p in names:
        if kind_of(F, p) == "leg":
            m = lab == names.index(p)
            if m.any():
                legtop[p] = float(np.nonzero(m)[0].min())
    ib = next(i for i, (n_, ps_, g_) in enumerate(layers) if "body" in ps_)
    unders = {} if ONE else {lv: under_image(hid, k, lv, rgb, fg, lab, names, F) for lv in (1, 2)}
    for li_, (name, ps, grow, abv) in enumerate(specs):
        ids = [names.index(p) for p in ps]
        own = np.isin(lab, ids) & (fg > 0)
        if not own.any():
            print("  lớp trống:", name)
            continue
        # lớp có ảnh bộ phận GPT vẽ đủ phần bị che (build_parts.py): lớp thân dùng lớp dưới 1, lớp sau thân dùng lớp dưới 2
        und = unders.get(1 if li_ == ib else 2 if li_ < ib else 0)
        ring = np.zeros_like(own)   # dải mọc thêm loang màu (cách cũ)
        ring_u = np.zeros_like(own)  # dải mọc thêm lấy từ hình GPT vẽ phần bị che
        if grow and abv:
            into = np.isin(lab, [names.index(p) for p in abv]) & (fg > 0)
            ring = (cv2.dilate(own.astype(np.uint8), disk(grow)) > 0) & into & ~own
            if und is not None:  # có hình vẽ thật: mọc rộng gấp 3 nhưng chỉ chỗ GPT có vẽ
                ring_u = (cv2.dilate(own.astype(np.uint8), disk(grow * 3)) > 0) & into & ~own & und[1]
        dom = own | ring
        if ring.any():
            sm = cv2.morphologyEx(dom.astype(np.uint8), cv2.MORPH_CLOSE, disk(6))
            sm = cv2.morphologyEx(sm, cv2.MORPH_OPEN, disk(8))
            dom = ((sm > 0) & (fg > 0)) | own
        dom = cv2.morphologyEx((dom | ring_u).astype(np.uint8), cv2.MORPH_CLOSE, disk(2)) > 0
        dom &= fg > 0
        dom = riglib.biggest(dom, 150)
        tex = rgb.copy()
        fillm = dom & ~own & ~ring_u  # phần còn hở GPT không vẽ: loang màu, kẻ nét mực ở mép
        if fillm.any():
            work = rgb.copy()
            work[~own] = np.median(rgb[own], 0).astype(np.uint8)
            if ring_u.any():
                work[ring_u] = und[0][ring_u]
            tex = cv2.inpaint(work, fillm.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
            tex = np.where(fillm[..., None], cv2.GaussianBlur(tex, (0, 0), 2.0), tex)
            edge = dom & (cv2.erode(dom.astype(np.uint8), disk(3)) == 0)
            inside = cv2.erode(fg, disk(5)) > 0
            line_ = edge & inside & fillm
            soft = cv2.GaussianBlur(line_.astype(np.float32), (0, 0), 0.8)[..., None]
            soft = np.maximum(soft, line_[..., None].astype(np.float32))
            tex = (tex * (1 - soft) + np.array(Q.INK, np.float32) * soft).astype(np.uint8)
        if ring_u.any():  # hình GPT; mép tiếp giáp phần thật hoà 4 px cho khỏi lộ đường nối
            dd = cv2.distanceTransform((~own).astype(np.uint8), cv2.DIST_L2, 5)
            wgt = np.clip(dd / 4.0, 0, 1)[..., None]
            blend = (rgb * (1 - wgt) + und[0] * wgt).astype(np.uint8)
            tex[ring_u & dom] = blend[ring_u & dom]
        tex[own] = rgb[own]
        a = cv2.GaussianBlur(dom.astype(np.float32), (0, 0), 0.9)
        yy, xx = np.nonzero(a > 0.02)
        x0, y0 = max(0, xx.min() - 3), max(0, yy.min() - 3)
        x1, y1 = min(fg.shape[1], xx.max() + 4), min(fg.shape[0], yy.max() + 4)
        rgba = np.dstack([tex, np.clip(a * 255, 0, 255).astype(np.uint8)])[y0:y1, x0:x1]
        w2, h2 = max(1, round((x1 - x0) * ks)), max(1, round((y1 - y0) * ks))
        small = Q.premul_resize(rgba, w2, h2)
        fx_, fy_ = (x1 - x0) / w2, (y1 - y0) / h2
        ox, oy = S((x0, y0))
        pc = L.Piece(name, small, ox, oy)
        llab = np.where(own, lab, -1)
        for _ in range(grow * 3 + 4):
            miss = dom & (llab < 0)
            if not miss.any():
                break
            g = cv2.dilate(llab.astype(np.float32) + 1, np.ones((3, 3), np.uint8)).astype(np.int32) - 1
            llab[miss] = g[miss]
        smap = {}
        for p in ps:
            kd = kind_of(F, p)
            if not (isinstance(kd, tuple) and kd[0] == "chain"):
                continue
            pm = llab == names.index(p)
            if not pm.any():
                continue
            bones, par, tip = F["chains"][kd[1]]
            D = Q.geo(pm, J[bones[0]])
            Lc = max(1.0, Q.at(D, tip))
            cuts = [min(0.95, max(0.05, Q.at(D, J[b]) / Lc)) for b in bones[1:]]
            for i in range(1, len(cuts)):
                cuts[i] = max(cuts[i], cuts[i - 1] + 0.05)
            smap[p] = (D / Lc, cuts, bones, par)
        # lấp lỗ nhỏ (khe giấy, lòng chữ) cho lưới liền; lỗ lớn (khoảng trống giữa đuôi và thân, giữa chân) để trống: lưới phủ qua
        # thì đuôi lắc kéo tam giác thành vệt sọc. "mesh_fill": "all" (đàn có dây mảnh giữa các lỗ) lấp hết như cũ
        pc.mask = fill_holes(pc.mask) if style_of(C, k, "mesh_fill") == "all" else fill_small_holes(pc.mask, 0.006 * H * H)
        pts_, nh, tris = pc.make_mesh(8, 14)
        if ONE:  # chuỗi: giá trị quãng dọc chuỗi loang ra ngoài vùng một dải (đỉnh vùng bên cạnh hoà vào chuỗi)
            for p in smap:
                Dn, cuts, bones, par = smap[p]
                smap[p] = (spread_finite(Dn, BLEND + 8), cuts, bones, par)

        def part_w(p, X, Y, xi, yi):
            kd = kind_of(F, p)
            if kd == "leg":
                y_top = legtop.get(p, Y)
                s = (Y - y_top) / max(1.0, ground - y_top)
                # chân đánh (paw): cả chân xoay quanh vai (cứng gần hết, chỉ đầu chân hoà vào thân); chân khác: nửa dưới bám đất
                wg = L.smooth01((s - 0.02) / 0.22) if p == paw else L.smooth01((s - 0.3) / 0.5)
                top_b = F.get("leg_parent", {}).get(p, "body")
                ws = [(top_b, 1 - wg), ("paw" if p == paw else "ground", wg)]
                return [(b, w) for b, w in ws if w > 0.01] or [("ground", 1.0)]
            if isinstance(kd, tuple) and kd[0] == "chain" and p in smap:
                Dn, cuts, bones, par = smap[p]
                s = float(Dn[yi, xi]) if np.isfinite(Dn[yi, xi]) else 0.0
                return Q.chain_w(min(1.0, max(0.0, s)), bones, cuts, par, 0.12, F.get("chain_pb", 0.3 if ONE else 0.12))
            if isinstance(kd, tuple) and kd[0] == "chain":
                return [(F["chains"][kd[1]][0][0], 1.0)]
            if isinstance(kd, tuple) and kd[0] == "rigid":
                return [(kd[1], 1.0)]
            if isinstance(kd, tuple) and kd[0] == "soft":  # hoà dần xương a -> b dọc đoạn p0 -> p1 (đầu chim liền thân)
                a_, b_, p0, p1 = kd[1:]
                dx_, dy_ = p1[0] - p0[0], p1[1] - p0[1]
                s = ((X - p0[0]) * dx_ + (Y - p0[1]) * dy_) / max(1.0, dx_ * dx_ + dy_ * dy_)
                w = L.smooth01(s)
                return [(b, x) for b, x in ((a_, 1 - w), (b_, w)) if x > 0.01]
            if isinstance(kd, list):
                return list(kd)
            return [("body", 1.0)]

        ids_ = [names.index(p) for p in ps]
        memb = membership(llab, dom, ids_, F.get("blend", BLEND)) if ONE and len(ps) > 1 else None
        wts, plabs = [], []
        qy_, qx_ = None, None
        for u, v in pts_:
            X, Y = x0 + u * fx_, y0 + v * fy_
            xi, yi = int(min(fg.shape[1] - 1, max(0, round(X)))), int(min(fg.shape[0] - 1, max(0, round(Y))))
            li = llab[yi, xi]
            if li < 0:
                if qy_ is None:
                    qy_, qx_ = np.nonzero(llab >= 0)
                j = int(np.argmin((qx_ - X) ** 2 + (qy_ - Y) ** 2))
                xi, yi, li = int(qx_[j]), int(qy_[j]), int(llab[qy_[j], qx_[j]])
            p = names[li]
            # chân đánh (paw) vẽ trên cùng: đá, vồ thì quét qua trước vải, thân (lúc đứng không chồng lên gì nên không đổi hình)
            plabs.append(len(ps) if p == paw else (ps.index(p) if p in ps else 0))
            mv = None
            if memb is not None:
                mv = memb[:, min(memb.shape[1] - 1, yi // 2), min(memb.shape[2] - 1, xi // 2)]
                if mv.sum() < 0.5:
                    mv = None
            if mv is None:
                wts.append(part_w(p, X, Y, xi, yi))
                continue
            acc = {}
            for j, pj in enumerate(ps):
                m = float(mv[j])
                if m < 0.02:
                    continue
                for b, w in part_w(pj, X, Y, xi, yi):
                    acc[b] = acc.get(b, 0.0) + m * w
            top4 = [(b, w) for b, w in sorted(acc.items(), key=lambda kv: -kv[1])[:4] if w > 0.01]
            sw = sum(w for _, w in top4)
            wts.append([(b, w / sw) for b, w in top4] if sw > 0 else part_w(p, X, Y, xi, yi))
        plabs = np.array(plabs)
        if ONE and len(tris):
            tris = cut_gaps(tris, wts, np.stack([x0 + pts_[:, 0] * fx_, y0 + pts_[:, 1] * fy_], 1), fg)
        depth = np.array([plabs[t].max() for t in tris]) if len(tris) else np.zeros(0)
        tris = tris[np.argsort(depth, kind="stable")]
        vw = np.array([pc.to_rig(x, y) for x, y in pts_])
        uv = np.stack([pts_[:, 0] / w2, pts_[:, 1] / h2], 1)
        R.images[name] = Image.fromarray(small)
        R.slot(name, wts[0][0][0], name)
        R.mesh(name, name, name, vw, uv, tris, nh, wts)
        stats.append(f"{name}: {len(pts_)} đỉnh")
        lay_dbg.append((name, rgba, own[y0:y1, x0:x1], (x0, y0)))
        for s_ in FX_MID.get(name, []):  # hiệu ứng chen giữa lớp (vòng nước trước thân, sau chân trước...)
            fx_slot(R, s_)
    for s_ in FX_FRONT:
        fx_slot(R, s_)
    ctx = Ctx()
    ctx.hid, ctx.k, ctx.R, ctx.F, ctx.C, ctx.info = hid, k, R, F, C, info
    ctx.rgb, ctx.fg, ctx.lab, ctx.layers = rgb, fg, lab, lay_dbg
    ctx.tf = {"ks": ks, "feet_x": feet_x, "ground": ground, "top": top}
    ctx.J = J
    print(f"{code(hid, k)}: " + "; ".join(stats))
    return R, ctx


# ---------------------------------------------------------------- hiệu ứng
# slot hiệu ứng: tên -> (xương cha, ảnh, cỡ theo H, góc, dx, dy); toạ độ đặt trong fx_setup
FXSPEC = {}
FXGROUND = {}  # slot ở xa đặt theo đất: độ cao xương so với đất
FX_BACK = ["fx_ground", "fx_ring_b"]
FX_MID = {}
FX_FRONT = ["fx_ring_f", "fx_shield", "fx_charge", "fx_orb", "fx_hit", "fx_hit2", "fx_big", "fx_big2", "fx_wave", "fx_drops",
            "fx_spark"] + [f"fx_p{i}" for i in range(10)] + \
           ["ff_ground", "fl_wave", "ff_big", "ff_big2", "ff_hit"] + [f"fl{i}" for i in range(5)] + [f"fp{i}" for i in range(8)]
NPART = 10


def fx_img(name):
    """ảnh hiệu ứng: FXnn = bộ nước dùng chung (Giọt Sương), tên khác = ảnh riêng trong inbox/fx/<tên>.png."""
    if name in T.FX:
        return T.fx_image(name)
    p = os.path.join(FXD, name + ".png")
    im = Image.open(p).convert("RGBA")
    keep = 200
    s = keep / max(im.size)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS) if s < 1 else im


def fx_setup(R, C, info, k):
    """ảnh của từng slot hiệu ứng theo bộ hiệu ứng của tướng (beasts_cfg: "fx"), xương đặt ở chỗ đánh, miệng, dưới chân."""
    fx = dict(DEFAULT_FX)
    fx.update(C.get("fx", {}))
    for kk, v in C.get("fx_form", {}).get(k, {}).items():
        fx[kk] = v
    mx, my = info["mouth"]
    front = info["front"]
    cx = (info["front"] + info["back"]) / 2
    hitx = front + 0.18 * H  # chỗ vụ trúng trước mặt (đòn đánh: thân đã lao tới, trận kéo cho chạm đối thủ)
    bones = {"fx_ground": ("move", cx, 0.02 * H), "fx_ring": ("move", cx, 0.38 * H), "fx_orb": ("tip", mx, my),
             "fx_charge": ("tip", mx, my), "fx_hit": ("move", hitx, 0.42 * H), "fx_hit2": ("move", hitx, 0.42 * H),
             "fx_big": ("move", front + 0.35 * H, 0.0), "fx_big2": ("move", front + 0.35 * H, 0.45 * H),
             "fx_wave": ("move", front + 0.5 * H, 0.0), "fx_drops": ("move", cx, 0.5 * H),
             "fx_spark": ("tip", mx, my), "fx_shield": ("move", cx, 0.45 * H)}
    for b, (par, x, y) in bones.items():
        R.bone(b, "head" if par == "tip" else par, x, y)
    for i in range(NPART):
        R.bone(f"fx_p{i}", "move", hitx, 0.42 * H)
    # hiệu ứng ở chỗ đối thủ (đòn xa, chiêu đứng tại chỗ): xương far (game dời tới tâm thân đối thủ, cao 0,45 chiều cao), hạt fp*,
    # đạn fly* (bay từ miệng tới far), sóng đất flyw (chạy dọc đất tới far)
    farx, fary = front + 0.9 * H, 0.45 * H
    info["far"] = (farx, fary)
    R.bone("far", "root", farx, fary)
    for i in range(NFAR):
        R.bone(f"fp{i}", "far", farx, fary)
    for i in range(NFLY):
        R.bone(f"fly{i}", "root", mx, my)
    R.bone("flyw", "root", front + 0.05 * H, 0.0)
    FXGROUND.clear()
    farmap = {"ff_ground": ("far", fx.get("fx_ground")), "ff_big": ("far", fx.get("fx_big")),
              "ff_big2": ("far", fx.get("fx_big2")), "ff_hit": ("far", fx.get("fx_hit")), "fl_wave": ("flyw", fx.get("fx_wave"))}
    for i in range(NFLY):
        farmap[f"fl{i}"] = (f"fly{i}", fx.get("fx_fly") or fx.get("fx_orb"))
    for i in range(NFAR):
        farmap[f"fp{i}"] = (f"fp{i}", fx.get("fx_p"))
    FXGROUND.update({"ff_ground": fary, "ff_big": fary, "fl_wave": 0.0})
    used = {}
    FXSPEC.clear()
    for slot, (bone, spec) in farmap.items():
        if not spec or spec[0] is None:
            continue
        img, size, rot = spec
        if img not in used:
            R.images[img] = fx_img(img)
            used[img] = True
        FXSPEC[slot] = (bone, img, size * H * (0.9 if slot.startswith("fl") and slot != "fl_wave" else 1.0), rot)
    for slot, (img, size, rot) in fx.items():
        if img is None or slot == "fx_p":
            continue
        if img not in used:
            R.images[img] = fx_img(img)
            used[img] = True
        bone = "fx_ring" if slot.startswith("fx_ring") else slot
        bone = "fx_p%d" % int(slot[4:]) if slot.startswith("fx_p") else bone
        FXSPEC[slot] = (bone, img, size * H, rot)
    for i in range(NPART):
        if f"fx_p{i}" not in FXSPEC and fx.get("fx_p"):
            img, size, rot = fx["fx_p"]
            if img not in used:
                R.images[img] = fx_img(img)
                used[img] = True
            FXSPEC[f"fx_p{i}"] = (f"fx_p{i}", img, size * H, rot)


DEFAULT_FX = {"fx_ground": ("FX08", 0.95, 0), "fx_ring_b": ("FX01", 1.0, 0), "fx_ring_f": ("FX01", 1.0, 0),
              "fx_charge": ("FX05", 0.22, 0), "fx_orb": ("FX06", 0.2, 0), "fx_hit": ("FX03", 0.5, 0),
              "fx_hit2": ("FX02", 0.6, 0), "fx_big": ("FX09", 1.0, 90), "fx_big2": ("FX03", 0.6, 0),
              "fx_wave": ("FX07", 0.85, 0), "fx_drops": ("FX04", 0.3, 0), "fx_spark": ("FX05", 0.22, 0),
              "fx_p": ("FX05", 0.08, 0)}


def fx_slot(R, slot):
    if slot not in FXSPEC:
        return
    bone, img, size, rot = FXSPEC[slot]
    im = R.images[img]
    s = size / max(im.size)
    bx, by = R.bw(bone)
    dx, dy = 0.0, 0.0
    standing = rot in (90, "up")
    if rot == 90:  # cột (tia đứng): gốc ở đất
        dy = size * 0.5
    elif rot == "up":  # hình đứng sẵn (vòi rồng, gai pha lê): đáy ảnh ở đất
        rot = 0.0
        dy = im.height * s * 0.5
    if slot in FXGROUND and (standing or slot != "ff_big"):  # hiệu ứng ở xa đặt theo đất dưới chân đối thủ
        dy -= FXGROUND[slot]
        if slot == "fl_wave":
            dy = im.height * s * 0.42
    R.slot(slot, bone, None, fx=True)
    R.region(slot, slot, img, bone, bx + dx, by + dy, im.width * s, im.height * s, rot)


def fx_on(P, slot, t, t0, t1, rise=0.0, fade=None, amax=1.0):
    T.fx_on(P, slot, t, t0, t1, rise, fade, amax)


def burst(P, t, t0, n=NPART, life=0.5, speed=(0.5, 1.0), ang=(20, 160), grav=1.6, spin=200, seed=1, size=(0.7, 1.3),
          origin=(0.0, 0.0), prefix="fx_p"):
    """hạt văng kiểu pixelfx: mỗi hạt tốc, góc, cỡ, đời, xoay riêng (có hạt giống), rơi theo trọng lực, nhỏ dần, tan.
    prefix "fp": hạt ở chỗ đối thủ (xương far)."""
    rng = np.random.RandomState(seed)
    if prefix == "fp":
        n = min(n, NFAR)
    for i in range(n):
        s = f"{prefix}{i}"
        sp = rng.uniform(*speed) * H
        a = math.radians(rng.uniform(*ang))
        lf = life * rng.uniform(0.7, 1.15)
        dl = rng.uniform(0, 0.05)
        sz = rng.uniform(*size)
        rs = rng.uniform(-spin, spin)
        u = t - t0 - dl
        if u < 0 or u >= lf:
            P.att.setdefault(s, None)  # không tắt hạt của một đợt khác đang bay
            continue
        P.att[s] = s
        x = origin[0] + math.cos(a) * sp * u
        y = origin[1] + math.sin(a) * sp * u - 0.5 * grav * H * u * u
        P.move(s, x, y)
        k = u / lf
        P.scale(s, sz * (1 - 0.6 * k))
        P.rot(s, rs * u)
        P.alpha[s] = 1 - L.smooth01((k - 0.55) / 0.45)


# ---------------------------------------------------------------- chuyển động
def squash(P, s, b="base"):
    """nén (s < 1) / giãn (s > 1) giữ thể tích, gốc ở đất."""
    P.scale(b, 1 / math.sqrt(s), s)


def bones_like(R, *pre):
    return [b["name"] for b in R.bones if b["name"].startswith(pre)]


def tail_bones(ctx):
    out = []
    for ch, (bones, _p, _t) in ctx.F.get("chains", {}).items():
        out.append(bones)
    return out


def secondary(P, ctx, t, lean_fn, amp=1.0, idle_u=None):
    """chuyển động phụ khoá tay (Critters): đuôi theo độ nghiêng thân trễ dần từng đốt, tai, vây ngược chiều, cánh."""
    for bones in tail_bones(ctx):  # đuôi trễ dần từng đốt, ngược chiều thân (quán tính)
        for i, b in enumerate(bones):
            d = 0.05 * (i + 1)
            P.rot(b, -amp * 0.55 * (1 + 0.3 * i) * lean_fn(t - d))
    for b in bones_like(ctx.R, "ear", "fin_h", "tuft", "mane", "whisk"):  # tai trễ: ngược chiều cú xoay, nhỏ
        P.rot(b, -amp * 0.45 * lean_fn(t - 0.06))
    for b in bones_like(ctx.R, "bell", "pend"):  # chuông, mặt dây: con lắc trễ hơn, mạnh hơn
        P.rot(b, -amp * 1.1 * lean_fn(t - 0.1))
    for b in bones_like(ctx.R, "wing"):
        P.rot(b, -amp * 0.4 * lean_fn(t - 0.04))


def idle(ctx):
    """thở 2 s: nhún nén nhẹ, thân lắc, đầu gật trễ, đuôi lượn trễ 1/3 vòng từng đốt, tai ngược pha, cánh phất chậm; giữa vòng
    một cú giật tai hoặc vẫy đuôi (điểm phá nhịp như Critters)."""
    D = ctx.C.get("idle_dur", 2.0)
    amp = ctx.C.get("idle_amp", 1.0)

    def f(t, P):
        u = 2 * math.pi * t / D
        b = 0.5 - 0.5 * math.cos(u)
        squash(P, 1 - 0.03 * amp * b)
        if ctx.C.get("hover"):  # con bay lơ lửng: nhấp nhô, bóng dưới đất co theo
            P.move("move", 0, 0.035 * H * math.sin(u))  # 0 ở khung đầu: nối liền các clip khác
            P.scale("shadow", 0.9 + 0.1 * b)
        P.rot("body", 1.4 * amp * math.sin(u))
        hrot(P, 2.6 * amp * math.sin(u - 0.9) - 1.2 * amp * b)
        ta = 0.6 if ONE else 1.0  # một lưới: đuôi lắc nhẹ (đuôi cuộn sát thân thì kéo giãn thân)
        for bones in tail_bones(ctx):
            for i, bn in enumerate(bones):
                P.rot(bn, ta * amp * (5 + 2.5 * i) * math.sin(u - 1.0 - 0.75 * i))
        ears = bones_like(ctx.R, "ear", "fin_h", "tuft", "mane", "whisk")
        for j, bn in enumerate(ears):
            P.rot(bn, amp * 4.0 * math.sin(u - 1.2 + math.pi * (j % 2)))
        for j, bn in enumerate(bones_like(ctx.R, "wing")):
            P.rot(bn, amp * 5.0 * math.sin(u - 0.4 - 0.3 * j))
        for bn in bones_like(ctx.R, "arm", "claw", "fin_b", "prop"):
            P.rot(bn, amp * 2.5 * math.sin(u - 0.5))
        for bn in bones_like(ctx.R, "bell", "pend"):
            P.rot(bn, amp * 4.0 * math.sin(u - 1.4))
        # điểm phá nhịp: giật tai / vẫy chóp đuôi
        acc = curve(t, [(0, 0), (0.62 * D, 0), (0.65 * D, 1, "o"), (0.72 * D, 0, "io"), (D, 0)])
        if ears:
            P.rot(ears[0], 14 * acc)
        for bones in tail_bones(ctx)[:1]:
            P.rot(bones[-1], -12 * acc)
        idle_fx(P, ctx, t, D)
    return {"dur": D, "loop": True, "fn": f}


def idle_fx(P, ctx, t, D):
    """hiệu ứng thường trực nhẹ (beasts_cfg "aura"): vòng nước dưới chân chậm, lấp lánh."""
    aura = ctx.C.get("aura", {}).get(ctx.k)
    if not aura:
        return
    if "ring" in aura:
        P.att["fx_ground"] = "fx_ground"
        P.alpha["fx_ground"] = aura["ring"]
        P.scale("fx_ground", 0.75 + 0.05 * math.sin(2 * math.pi * t / D))
        P.rot("fx_ground", 0)


def hit(ctx):
    """trúng đòn 0,6 s: bật ngửa ra sau, nén, đầu giật, đuôi tai quất, giọt nước văng."""
    D = 0.6

    def lean(t):
        return curve(t, [(0, 0), (0.07, 8, "o"), (0.24, 4), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.08, -0.07 * H, "o"), (0.22, -0.08 * H), (D, 0)])
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.rot("base", 0.5 * lean(t))
        P.rot("body", 0.5 * lean(t))
        squash(P, c([(0, 1), (0.06, 0.9, "o"), (0.2, 1.04), (0.4, 0.99), (D, 1)]))
        hrot(P, c([(0, 0), (0.06, 10, "o"), (0.25, 4), (D, 0)]))
        secondary(P, ctx, t, lean, 1.2)
        fx_on(P, "fx_drops", t, 0.02, 0.42, fade=0.28)
        P.move("fx_drops", c([(0, 0), (0.42, -0.05 * H, "o")]), c([(0, 0), (0.42, 0.08 * H, "o")]))
        P.scale("fx_drops", c([(0, 0.6), (0.42, 1.15, "o")]))
    return {"dur": D, "fn": f}


# --- tiện ích chuyển động (một lưới)
def hrot(P, a):
    """đầu xoay: một lưới thì cổ uốn mềm nên xoay ít hơn (HEADK), nghiêng cả người bù vào."""
    P.rot("head", a * (HEADK if ONE else 1.0))


def has(ctx, b):
    return b in ctx.R.bi


def go(P, mx, my=0.0):
    """dời cả con (xương move), bóng dưới chân theo."""
    P.move("move", mx, my)
    P.move("shadow", mx, 0)


def lean_to(P, a):
    P.rot("base", 0.45 * a)
    P.rot("body", 0.55 * a)


def limb(ctx, *names):
    for n in names:
        if has(ctx, n):
            return n
    return None


def flash(P, slot, t, wins):
    """một slot hiện ở nhiều cửa sổ [(t0, t1, cỡ)...]: mỗi lần nở nhanh rồi tan."""
    for t0, t1, s in wins:
        if t0 <= t < t1:
            fx_on(P, slot, t, t0, t1, fade=(t1 - t0) * 0.6)
            u = (t - t0) / (t1 - t0)
            P.scale(slot, s * (0.5 + 0.7 * L.smooth01(u / 0.4)))
            return
    P.att[slot] = None


def fx_h(ctx, slot):
    """chiều cao (đơn vị rig) của ảnh hiệu ứng trong slot."""
    if slot not in FXSPEC:
        return 0.0
    bone, img, size, rot = FXSPEC[slot]
    im = ctx.R.images[img]
    return size * (im.height if rot != 90 else im.width) / max(im.size)


def far_of(ctx):
    return ctx.info["far"]


def shoot(P, ctx, t, i, t0, fly, arc=0.0, spin=0.0, s0=0.7, s1=1.0):
    """đạn fly<i> bay từ miệng (dáng gốc) tới far trong fly giây, cong arc (đơn vị H), xoay spin độ."""
    s = f"fl{i}"
    b = f"fly{i}"
    if not (t0 <= t < t0 + fly + 0.03):
        P.att[s] = None
        return
    u = min(1.0, (t - t0) / fly)
    bx, by = ctx.R.bw(b)
    fx_, fy_ = far_of(ctx)
    e = u * u * (3 - 2 * u) * 0.35 + u * 0.65
    P.move(b, (fx_ - bx) * e, (fy_ - by) * e + arc * H * math.sin(math.pi * u))
    P.att[s] = s
    P.alpha[s] = min(1.0, (t - t0) / 0.04)
    P.scale(s, s0 + (s1 - s0) * u)
    P.rot(s, spin * u)


def far_impact(P, ctx, t, h, s=1.0, big=True, seed=11, ground=True):
    """vụ nổ ở chỗ đối thủ: vòng loang dưới chân, hình lớn trồi lên, nổ, hạt văng."""
    c = lambda ks: curve(t, ks)  # noqa: E731
    if ground:
        fx_on(P, "ff_ground", t, h - 0.3, h + 0.62, rise=0.2, fade=0.3)
        P.scale("ff_ground", c([(0, 0.5), (h - 0.3, 0.5), (h, 0.85, "o"), (h + 0.4, 1.3 * s, "o"), (h + 1, 1.3 * s)]))
        P.alpha["ff_ground"] = P.alpha.get("ff_ground", 1.0) * (0.45 if t < h else 1.0)
    if big:
        fx_on(P, "ff_big", t, h, h + 0.62, fade=0.26)
        P.scale("ff_big", s * c([(0, 0.6), (h, 0.6), (h + 0.18, 1.12, "o"), (h + 0.45, 1.2), (h + 1, 1.2)]),
                s * c([(0, 0.15), (h, 0.15), (h + 0.2, 1.0, "o"), (h + 1, 1.05)]))
    fx_on(P, "ff_big2", t, h + 0.02, h + 0.4, fade=0.24)
    P.scale("ff_big2", s * c([(0, 0.5), (h, 0.5), (h + 0.28, 1.5, "o"), (h + 1, 1.5)]))
    burst(P, t, h + 0.02, life=0.6, speed=(0.6, 1.2), ang=(30, 150), grav=1.6, seed=seed, size=(0.8, 1.5),
          origin=(0.0, -0.1 * H), prefix="fp")


def windup(P, ctx, t, motion, t_up, h, D):
    """tư thế tụ lực rồi tung chiêu đứng tại chỗ; trả hàm nghiêng (cho chuyển động phụ).
    stomp: giơ chân trước rồi dậm; roar: ngửa đầu rồi gầm rung người; howl: ngửa tru dài; claws: giơ càng/tay rồi nện;
    wings: vỗ cánh dồn dập, bốc lên chút; rear: chồm lên rồi nện cả người."""
    c = lambda ks: curve(t, ks)  # noqa: E731
    if motion == "stomp":
        def lean(tt):
            return curve(tt, [(0, 0), (t_up, 12), (h - 0.04, 14), (h, -10, "o"), (h + 0.12, -10), (h + 0.45, -2), (D, 0)])
        squash(P, c([(0, 1), (t_up, 1.07), (h - 0.04, 1.08), (h, 0.86, "o"), (h + 0.12, 0.9), (h + 0.4, 1.02), (D, 1)]))
        hrot(P, c([(0, 0), (t_up, 12), (h, -10, "o"), (h + 0.3, -6), (D, 0)]))
        pw = limb(ctx, "paw", "arm_f", "claw_f")
        if pw:
            P.rot(pw, c([(0, 0), (t_up, 46), (h - 0.05, 52), (h, -6, "i"), (h + 0.3, 0), (D, 0)]))
    elif motion in ("roar", "howl"):
        up = 22 if motion == "roar" else 30
        def lean(tt):
            return curve(tt, [(0, 0), (t_up, 9), (h, -7, "o"), (h + 0.5, -5), (D, 0)])
        squash(P, c([(0, 1), (t_up, 0.94), (h, 1.07, "o"), (h + 0.5, 1.05), (D, 1)]))
        hrot(P, c([(0, 0), (t_up, up), (h, -6 if motion == "roar" else up + 2, "o"), (h + 0.5, -4 if motion == "roar" else up), (D, 0)]))
        if h <= t < h + 0.5:  # rung người lúc gầm
            P.rot("body", 1.6 * math.sin(70 * t) * (1 - (t - h) / 0.5))
    elif motion == "claws":
        def lean(tt):
            return curve(tt, [(0, 0), (t_up, 7), (h, -9, "o"), (h + 0.3, -3), (D, 0)])
        squash(P, c([(0, 1), (t_up, 1.05), (h, 0.88, "o"), (h + 0.3, 0.98), (D, 1)]))
        hrot(P, c([(0, 0), (t_up, 10), (h, -8, "o"), (D, 0)]))
        for bn in bones_like(ctx.R, "claw", "arm"):
            P.rot(bn, c([(0, 0), (t_up, 46), (h - 0.04, 52), (h, -18, "o"), (h + 0.3, 0), (D, 0)]))
    elif motion == "wings":
        def lean(tt):
            return curve(tt, [(0, 0), (t_up, 8), (h, -8, "o"), (h + 0.4, -2), (D, 0)])
        go(P, 0, c([(0, 0), (t_up, 0.06 * H, "o"), (h, 0.05 * H), (h + 0.4, 0.0), (D, 0)]))
        squash(P, c([(0, 1), (t_up, 1.04), (h, 0.92, "o"), (h + 0.3, 1.0), (D, 1)]))
        hrot(P, c([(0, 0), (t_up, 12), (h, -8, "o"), (D, 0)]))
        fl = math.sin(2 * math.pi * t / 0.22) if t < h + 0.3 else 0.0
        for j, bn in enumerate(bones_like(ctx.R, "wing")):
            P.rot(bn, 16 * fl * (1 if j % 2 == 0 else 0.8))
    else:  # rear
        def lean(tt):
            return curve(tt, [(0, 0), (t_up, 18), (h - 0.05, 20), (h, -12, "o"), (h + 0.15, -12), (h + 0.5, -2), (D, 0)])
        go(P, 0, c([(0, 0), (t_up, 0.03 * H), (h, 0, "i"), (D, 0)]))
        squash(P, c([(0, 1), (t_up, 1.06), (h, 0.88, "o"), (h + 0.3, 1.0), (D, 1)]))
        hrot(P, c([(0, 0), (t_up, 16), (h, -12, "o"), (h + 0.4, -4), (D, 0)]))
        pw = limb(ctx, "paw", "arm_f", "claw_f")
        if pw:
            P.rot(pw, c([(0, 0), (t_up, 40), (h, -8, "i"), (h + 0.3, 0), (D, 0)]))
    lean_to(P, lean(t))
    return lean


# --- đòn đánh: các kiểu (beasts_cfg "attack", theo dạng được)
def attack(ctx):
    kind = style_of(ctx.C, ctx.k, "attack", "bite")
    return {"pounce": attack_dash, "ram": attack_dash, "bite": attack_dash, "claw": attack_dash, "smack": attack_dash,
            "smash": attack_dash, "slam": attack_dash, "swipe": attack_limb, "punch": attack_limb, "kick": attack_limb,
            "tailwhip": attack_tailwhip, "spin": attack_spin, "song": attack_range, "breath": attack_range,
            "roar": attack_range, "throw": attack_throw}[kind](ctx, kind)


def attack_dash(ctx, kind):
    """lao tới đánh (trận kéo đỉnh lao tới 72% quãng tới đối thủ), không nhảy: lấy đà ngược chiều (ngửa/lùi, nén), lao 2-3 khung,
    khựng 0,1 s lúc chạm, vượt quá rồi trôi về. Kiểu: ram húc (cúi đầu), bite cắn (đầu chồm), claw càng đấm, smack/smash đập
    đạo cụ cầm tay."""
    kind = {"smash": "smack", "pounce": "bite", "slam": "ram"}.get(kind, kind)
    D, h, hold = 1.0, 0.42, 0.1
    head_k = {"ram": -24, "bite": -20, "claw": -8, "smack": -10}[kind]
    lean_k = {"ram": -16, "bite": -11, "claw": -6, "smack": -8}[kind]

    def lean(t):
        return curve(t, [(0, 0), (0.3, 10), (h, lean_k, "o"), (h + hold, lean_k), (0.72, 3), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.3, -0.06 * H), (h, 0.55 * H, "i"), (h + hold, 0.56 * H), (0.66, 0.5 * H, "o"), (D, 0)])
        go(P, mx)
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.3, 0.9), (h, 1.09, "o"), (h + hold, 1.08), (0.72, 0.97), (D, 1)]))
        hrot(P, c([(0, 0), (0.3, 12), (h, head_k, "o"), (h + hold, head_k), (0.76, 4), (D, 0)]))
        for bn in bones_like(ctx.R, "claw_f", "arm_f", "prop"):  # càng, tay cầm đạo cụ: giơ lên rồi giáng xuống / đấm tới
            sw = style_of(ctx.C, ctx.k, "swing") or {"claw": (-25, 40), "smack": (55, -18)}.get(kind, (10, -16))
            P.rot(bn, c([(0, 0), (0.3, sw[0]), (h, sw[1], "o"), (h + hold, sw[1]), (0.8, 0), (D, 0)]))
        for bn in bones_like(ctx.R, "claw_b", "arm_b"):
            P.rot(bn, c([(0, 0), (0.3, -12), (h, 16, "o"), (D, 0)]))
        secondary(P, ctx, t, lean)
        attack_fx(P, ctx, t, h, kind)
    return {"dur": D, "fn": f, "hit": h}


def attack_limb(ctx, kind):
    """vồ (swipe: giơ chân trước cao rồi cào xuống), đấm (punch: tay kéo về rồi thụi tới), đá (kick: chân sau kéo rồi tung lên
    trước, người ngả ra sau). Lao tới như đòn cận chiến."""
    D, h, hold = 1.0, 0.44, 0.1
    if kind == "kick":
        bone = limb(ctx, "paw", "arm_f")
    elif kind == "swipe":
        bone = limb(ctx, "paw", "arm_f", "claw_f")
    else:
        bone = limb(ctx, "arm_f", "claw_f", "paw")
    sw = style_of(ctx.C, ctx.k, "swing") or {"swipe": (52, -10), "punch": (-30, 62), "kick": (-26, 82)}[kind]
    lk = {"swipe": -10, "punch": -12, "kick": 14}[kind]

    def lean(t):
        return curve(t, [(0, 0), (0.3, 8 if kind != "kick" else -4), (h, lk, "o"), (h + hold, lk), (0.72, 2), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.3, -0.05 * H), (h, 0.52 * H, "i"), (h + hold, 0.53 * H), (0.68, 0.46 * H, "o"), (D, 0)]))
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.3, 0.93), (h, 1.06, "o"), (h + hold, 1.05), (0.75, 0.98), (D, 1)]))
        hrot(P, c([(0, 0), (0.3, 8), (h, -10 if kind != "kick" else 6, "o"), (h + hold, -10 if kind != "kick" else 6), (0.8, 2), (D, 0)]))
        if bone:
            P.rot(bone, c([(0, 0), (0.3, sw[0]), (h, sw[1], "o"), (h + hold, sw[1]), (0.78, 0), (D, 0)]))
        other = limb(ctx, "arm_b", "claw_b") if bone in ("arm_f", "claw_f") else None
        if other:
            P.rot(other, c([(0, 0), (0.3, 14), (h, -18, "o"), (0.8, 0), (D, 0)]))
        secondary(P, ctx, t, lean)
        attack_fx(P, ctx, t, h, kind)
    return {"dur": D, "fn": f, "hit": h}


def attack_tailwhip(ctx, kind):
    """xoay người quất đuôi: lao tới, lật cả con (đuôi ra phía đối thủ), đuôi quất mạnh lúc chạm, lật về."""
    D, h = 1.05, 0.5

    def lean(t):
        return curve(t, [(0, 0), (0.28, 6), (h, -8, "o"), (0.7, -2), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.28, -0.04 * H), (0.44, 0.46 * H, "i"), (0.66, 0.48 * H), (0.82, 0.4 * H, "o"), (D, 0)]))
        P.scale("spin", c([(0, 1), (0.3, 1), (0.42, -1, "io"), (0.64, -1), (0.8, 1, "io"), (D, 1)]), 1)
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.3, 0.92), (0.44, 1.05, "o"), (0.7, 1.0), (D, 1)]))
        for bones in tail_bones(ctx):
            for i, b in enumerate(bones):  # lật người đã quét đuôi; đuôi chỉ quất thêm vừa phải (tổng chóp < 50°)
                P.rot(b, c([(0, 0), (0.38, -6 * (1 + 0.3 * i)), (h, 12 * (1 + 0.3 * i), "o"), (0.68, 3), (D, 0)]))
        secondary(P, ctx, t, lean, 0.5)
        attack_fx(P, ctx, t, h, kind)
    return {"dur": D, "fn": f, "hit": h}


def attack_spin(ctx, kind):
    """cuộn tròn lăn tới (con tròn): ngả đà, lăn một vòng tới đối thủ, nảy nhẹ lúc chạm."""
    D, h = 1.0, 0.46

    def lean(t):
        return curve(t, [(0, 0), (0.22, 6), (h, -6, "o"), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.22, -0.05 * H), (h, 0.55 * H, "i"), (h + 0.08, 0.56 * H), (0.7, 0.48 * H, "o"), (D, 0)]))
        P.rot("spin", c([(0, 0), (0.22, 14), (h, -360, "i"), (h + 0.06, -372, "o"), (0.62, -360), (D, -360)]))
        squash(P, c([(0, 1), (0.22, 0.86), (0.3, 1.0), (h, 0.95), (h + 0.06, 0.88, "o"), (0.7, 1.03), (D, 1)]))
        secondary(P, ctx, t, lean)
        attack_fx(P, ctx, t, h, kind)
    return {"dur": D, "fn": f, "hit": h}


def attack_range(ctx, kind):
    """đánh từ xa tại chỗ: ngửa hít hơi, chồm tới nhả đạn (song: 3 nốt lượn, breath: một quả to, roar: 3 vòng sóng âm to dần) bay
    tới đối thủ (xương fly, game kéo tới chỗ đối thủ), nổ ở chỗ đối thủ."""
    D, h, hold, fly = 1.0, 0.4, 0.08, 0.26
    hit = h + fly + (0.08 if kind != "breath" else 0.0)

    def lean(t):
        return curve(t, [(0, 0), (0.3, 9), (h, -9, "o"), (h + hold, -9), (0.74, 2), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.3, -0.04 * H), (h, 0.06 * H, "o"), (h + hold, 0.06 * H), (D, 0)]))
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.3, 1.06), (h, 0.93, "o"), (h + hold, 0.94), (0.74, 1.02), (D, 1)]))
        hrot(P, c([(0, 0), (0.3, 16), (h, -14, "o"), (h + hold, -14), (0.8, 3), (D, 0)]))
        for bn in bones_like(ctx.R, "wing"):
            P.rot(bn, c([(0, 0), (0.3, 22), (h, -26, "o"), (h + hold, -24), (0.8, 4), (D, 0)]))
        for bn in bones_like(ctx.R, "arm", "claw"):
            P.rot(bn, c([(0, 0), (0.3, 14), (h, -12, "o"), (0.8, 0), (D, 0)]))
        secondary(P, ctx, t, lean)
        if kind == "breath":
            shoot(P, ctx, t, 0, h - 0.02, fly, arc=0.02, spin=-200, s0=0.6, s1=1.15)
        elif kind == "song":
            for i in range(3):
                shoot(P, ctx, t, i, h - 0.02 + 0.04 * i, fly, arc=(0.08, -0.06, 0.12)[i], spin=(30, -40, 20)[i], s0=0.6, s1=0.95)
        else:
            for i in range(3):
                shoot(P, ctx, t, i, h - 0.02 + 0.04 * i, fly, arc=0.0, s0=0.5 + 0.2 * i, s1=1.0 + 0.25 * i)
        fx_on(P, "fx_charge", t, 0.12, h + 0.02, rise=0.1, fade=0.08, amax=0.9)
        P.scale("fx_charge", c([(0, 0.4), (h - 0.05, 1.0, "o"), (h, 0.7)]))
        flash(P, "ff_hit", t, [(hit - 0.02, hit + 0.3, 1.0)])
        burst(P, t, hit, life=0.45, speed=(0.45, 0.95), ang=(-10, 190), grav=1.6, seed=3, prefix="fp")
    return {"dur": D, "fn": f, "hit": hit}


def attack_throw(ctx, kind):
    """ném đồ bay (bùa, hạt cánh quạt): ngả đà, vung, đồ xoay tít bay tới đối thủ (xương flyp, game kéo tới chỗ đối thủ), trúng
    rồi bay vòng về chỗ cũ."""
    props = [b for b in (style_of(ctx.C, ctx.k, "throw") or []) if has(ctx, "flyp_" + b)]
    D, h, fly = 1.15, 0.4, 0.28
    hit = h + fly

    def lean(t):
        return curve(t, [(0, 0), (0.3, 10), (h, -10, "o"), (h + 0.1, -10), (0.8, 0), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.3, -0.03 * H), (h, 0.04 * H, "o"), (D, 0)]))
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.3, 0.94), (h, 1.05, "o"), (0.8, 1.0), (D, 1)]))
        hrot(P, c([(0, 0), (0.3, 10), (h, -10, "o"), (0.8, 0), (D, 0)]))
        for bn in bones_like(ctx.R, "wing", "arm"):
            P.rot(bn, c([(0, 0), (0.3, 30), (h, -30, "o"), (0.85, 0), (D, 0)]))
        fx_, fy_ = far_of(ctx)
        for j, b in enumerate(props):
            t0 = h - 0.02 + 0.05 * j
            x0, y0 = ctx.R.bw("flyp_" + b)
            ta = t0 + fly
            P.move("flyp_" + b, c([(0, 0), (t0, 0), (ta, fx_ - x0, "i"), (ta + 0.06, fx_ - x0), (ta + 0.4, 0, "io")]),
                   c([(0, 0), (t0, 0), (t0 + fly * 0.5, (fy_ - y0) * 0.5 + 0.14 * H, "o"), (ta, fy_ - y0, "i"),
                      (ta + 0.06, fy_ - y0), (ta + 0.24, 0.12 * H, "o"), (ta + 0.4, 0, "i")]))
            P.rot(b, c([(0, 0), (t0, 0), (ta + 0.4, -1080, "l")]))
            P.scale(b, c([(0, 1), (t0, 1), (t0 + 0.12, 1.5, "o"), (ta + 0.06, 1.5), (ta + 0.4, 1, "io")]))
        secondary(P, ctx, t, lean)
        flash(P, "ff_hit", t, [(hit - 0.02, hit + 0.3, 1.0)])
        burst(P, t, hit, life=0.45, speed=(0.45, 0.95), ang=(-10, 190), grav=1.6, seed=5, prefix="fp")
    return {"dur": D, "fn": f, "hit": hit}


def attack_fx(P, ctx, t, h, kind):
    """hiệu ứng đòn cận chiến: ảnh trúng chính (fx_hit) nở nhanh rồi tan, ảnh phụ (fx_hit2: vệt cào, vệt chém) lệch pha, hạt văng."""
    c = lambda ks: curve(t, ks)  # noqa: E731
    sp = ctx.C.get("attack_fx", {})
    P.move("fx_hit2", sp.get("dx", 0) * H, sp.get("dy", 0) * H)
    P.move("fx_hit", sp.get("dx", 0) * H, sp.get("dy", 0) * H)
    fx_on(P, "fx_hit2", t, h - 0.02, h + 0.24, fade=0.14)
    P.scale("fx_hit2", c([(0, 0.8), (h - 0.02, 0.8), (h + 0.14, sp.get("s2", 1.15), "o"), (h + 1, sp.get("s2", 1.15))]))
    P.rot("fx_hit2", sp.get("r2", -20) + (-35 if kind == "swipe" else 0))
    fx_on(P, "fx_hit", t, h, h + 0.32, fade=0.2)
    P.scale("fx_hit", c([(0, 0.4), (h, 0.4), (h + 0.2, sp.get("s1", 1.1), "o"), (h + 1, sp.get("s1", 1.1) * 1.05)]))
    burst(P, t, h, life=0.45, speed=(0.45, 0.95), ang=(-10, 150), grav=1.8, seed=3,
          origin=(sp.get("dx", 0) * H, sp.get("dy", 0) * H))


def cast(ctx):
    """chiêu mana 1 s: ngửa đầu tụ sức (quả cầu ở miệng to dần, lấp lánh xoay), nén người, rồi chồm tới nhả (trận bắn tia từ miệng
    ở khung trúng), giật ngược, về."""
    D, h = 1.0, 0.56

    def lean(t):
        return curve(t, [(0, 0), (0.34, 8), (h - 0.04, 9), (h, -8, "o"), (0.8, -4), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.34, 0.94), (h - 0.04, 0.92), (h, 1.06, "o"), (0.8, 1.0), (D, 1)]))
        hrot(P, c([(0, 0), (0.34, 14), (h - 0.04, 16), (h, -10, "o"), (0.82, -4), (D, 0)]))
        go(P, c([(0, 0), (h, 0), (h + 0.05, -0.04 * H, "o"), (0.85, -0.02 * H), (D, 0)]))
        for bn in bones_like(ctx.R, "wing"):
            P.rot(bn, c([(0, 0), (0.34, 20), (h, -20, "o"), (D, 0)]))
        for bn in bones_like(ctx.R, "claw", "arm", "prop"):
            P.rot(bn, c([(0, 0), (0.34, 18), (h, -10, "o"), (D, 0)]))
        secondary(P, ctx, t, lean)
        fx_on(P, "fx_orb", t, 0.12, h + 0.06, rise=0.16, fade=0.06, amax=0.95)
        P.scale("fx_orb", c([(0, 0.3), (0.12, 0.35), (h - 0.02, 1.25), (h + 0.06, 1.6, "o"), (D, 1.6)]))
        P.rot("fx_orb", c([(0, 0), (D, -220, "l")]))
        fx_on(P, "fx_charge", t, 0.2, h + 0.04, rise=0.1, fade=0.1)
        P.scale("fx_charge", c([(0, 0.4), (0.4, 1.1, "o"), (h, 0.7)]))
        P.rot("fx_charge", c([(0, 0), (D, 140, "l")]))
        fx_on(P, "fx_ring_b", t, 0.1, h + 0.1, rise=0.15, fade=0.12, amax=0.5)
        P.rot("fx_ring", c([(0, 0), (D, -300, "l")]))
        P.scale("fx_ring", c([(0, 0.5), (h, 0.9, "o"), (D, 1.0)]), c([(0, 0.25), (h, 0.4, "o"), (D, 0.45)]))
    return {"dur": D, "fn": f, "hit": h}


# --- chiêu cuối: các kiểu (beasts_cfg "skill"); không kiểu nào nhảy lên rồi ra chiêu (người dùng chê 2026-11-09)
def skill(ctx):
    kind = style_of(ctx.C, ctx.k, "skill", "erupt")
    return {"erupt": skill_erupt, "storm": skill_storm, "barrage": skill_barrage, "summon_prop": skill_summon_prop,
            "shockwave": skill_shockwave, "charge": skill_rush, "spin_dash": skill_rush, "slide": skill_slide,
            "combo": skill_combo, "leap": skill_leap, "dash": skill_leap, "summon": skill_summon}[kind](ctx, kind)


def motion_of(ctx, default):
    return style_of(ctx.C, ctx.k, "motion") or default


def skill_erupt(ctx, kind):
    """đứng tại chỗ tụ lực (dậm chân / gầm / giơ càng / vỗ cánh), vòng loang báo trước dưới chân đối thủ rồi hình lớn trồi lên ở
    đó (lốc nước, gai pha lê, dây leo, vòi rồng), nổ, hạt văng."""
    D, t_up, h = 1.6, 0.45, 0.78
    mo = motion_of(ctx, "stomp")

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        lean = windup(P, ctx, t, mo, t_up, h, D)
        secondary(P, ctx, t, lean, 1.1)
        skill_charge(P, t, c, h)
        far_impact(P, ctx, t, h, ctx.C.get("skill_fx", {}).get("scale", 1.0))
    return {"dur": D, "fn": f, "hit": h + 0.06}


def skill_storm(ctx, kind):
    """đứng tại chỗ ngửa gầm gọi trời: hình lớn (chuông, tảng băng, sét, lốc) rơi từ trên xuống đúng chỗ đối thủ, nảy, nổ."""
    D, t_up, h = 1.7, 0.5, 0.92
    mo = motion_of(ctx, "roar")
    land = 0.0 if FXSPEC.get("ff_big", (0, 0, 0, 0))[3] in (90, "up") else fx_h(ctx, "ff_big") * 0.5 - 0.45 * H

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        lean = windup(P, ctx, t, mo, t_up, h - 0.25, D)
        secondary(P, ctx, t, lean, 1.1)
        skill_charge(P, t, c, h - 0.2)
        fx_on(P, "fx_charge", t, 0.2, h - 0.2, rise=0.12, fade=0.12)
        P.scale("fx_charge", c([(0, 0.4), (0.5, 1.2, "o"), (h - 0.2, 0.8)]))
        P.rot("fx_charge", c([(0, 0), (D, 160, "l")]))
        fx_on(P, "ff_big", t, h - 0.32, h + 0.55, rise=0.06, fade=0.24)
        s = ctx.C.get("skill_fx", {}).get("scale", 1.0)
        P.move("ff_big", 0, c([(0, 1.8 * H), (h - 0.32, 1.8 * H), (h, land, "i"), (h + 0.06, land + 0.05 * H, "o"), (h + 0.15, land, "i")]))
        P.scale("ff_big", s * c([(0, 1.0), (h, 1.0), (h + 0.05, 1.12, "o"), (h + 0.16, 1.0), (h + 1, 1.0)]),
                s * c([(0, 1.0), (h, 1.0), (h + 0.05, 0.86, "o"), (h + 0.16, 1.0), (h + 1, 1.0)]))
        far_impact(P, ctx, t, h, s, big=False)
    return {"dur": D, "fn": f, "hit": h + 0.03}


def skill_barrage(ctx, kind):
    """đứng tại chỗ bắn liên hoàn: 5 đạn (lá, nốt, pha lê, gió) bay tới đối thủ nối nhau, người giật theo từng phát, nổ lớn cuối."""
    D, t0, gap, fly = 1.75, 0.5, 0.13, 0.26
    n = NFLY
    last = t0 + gap * (n - 1) + fly
    mo = motion_of(ctx, "wings")

    def lean(t):
        k = curve(t, [(0, 0), (0.4, 9), (t0, 4), (last, -2), (D, 0)])
        for i in range(n):
            ti = t0 + gap * i
            k -= 7 * math.exp(-((t - ti - 0.03) / 0.04) ** 2)
        return k

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.4, 0.93), (t0, 1.03, "o"), (last, 1.0), (D, 1)]))
        hrot(P, c([(0, 0), (0.4, 14), (t0, -8, "o"), (last, -6), (D, 0)]))
        fl = math.sin(2 * math.pi * (t - t0) / gap) if t0 <= t < last else 0.0
        for j, bn in enumerate(bones_like(ctx.R, "wing")):
            P.rot(bn, 14 * fl)
        for bn in bones_like(ctx.R, "arm", "claw"):
            P.rot(bn, 10 * fl)
        if mo == "stomp" and has(ctx, "paw"):
            P.rot("paw", 20 * max(0.0, fl))
        secondary(P, ctx, t, lean, 0.8)
        skill_charge(P, t, c, t0)
        for i in range(n):
            shoot(P, ctx, t, i, t0 + gap * i, fly, arc=(0.1, -0.08, 0.16, -0.04, 0.06)[i], spin=(180, -220, 160, -200, 240)[i],
                  s0=0.9, s1=1.3)
        flash(P, "ff_hit", t, [(t0 + gap * i + fly - 0.01, t0 + gap * i + fly + 0.16, 0.8) for i in range(n - 1)])
        far_impact(P, ctx, t, last, ctx.C.get("skill_fx", {}).get("scale", 1.0), big=False, seed=13)
    return {"dur": D, "fn": f, "hit": last}


def skill_summon_prop(ctx, kind):
    """gọi đồ khổng lồ (bàn tay gỗ): tay chỉ lên, đồ bốc lên to dần, xoay, bay tới trên đầu đối thủ rồi giáng xuống; đồ nhỏ khác
    (bùa) bay theo nện trước; đồ bay về chỗ cũ."""
    props = [b for b in (style_of(ctx.C, ctx.k, "throw") or []) if has(ctx, "flyp_" + b)]
    big = style_of(ctx.C, ctx.k, "big_prop") or (props[0] if props else None)
    small = [b for b in props if b != big]
    D, h = 1.85, 1.05
    fx_, fy_ = far_of(ctx)

    def lean(t):
        return curve(t, [(0, 0), (0.3, 10), (0.7, -6, "o"), (h, -10), (h + 0.3, -2), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.3, 1.05), (0.7, 0.95, "o"), (h, 0.92), (h + 0.3, 1.0), (D, 1)]))
        hrot(P, c([(0, 0), (0.3, 16), (0.7, -6, "o"), (h, -8), (D, 0)]))
        for bn in bones_like(ctx.R, "arm"):
            P.rot(bn, c([(0, 0), (0.3, 70), (0.7, 30, "o"), (h, 20), (h + 0.4, 0), (D, 0)]))
        secondary(P, ctx, t, lean)
        skill_charge(P, t, c, 0.7)
        if big:
            x0, y0 = ctx.R.bw("flyp_" + big)
            sc = style_of(ctx.C, ctx.k, "big_scale") or 2.0
            P.move("flyp_" + big, c([(0, 0), (0.35, (fx_ - x0) * 0.15), (0.75, (fx_ - x0) * 0.7, "io"), (h - 0.12, fx_ - x0, "o"),
                                     (h + 0.2, fx_ - x0), (D, 0, "io")]),
                   c([(0, 0), (0.35, 0.5 * H, "o"), (0.75, 0.75 * H), (h - 0.12, fy_ - y0 + 0.65 * H, "o"),
                      (h, fy_ - y0 + 0.05 * H, "i"), (h + 0.05, fy_ - y0 + 0.1 * H, "o"), (h + 0.2, fy_ - y0 + 0.05 * H),
                      (D, 0, "io")]))
            P.scale(big, c([(0, 1), (0.35, 1.3), (0.75, sc, "o"), (h, sc), (h + 0.05, sc * 1.08, "o"), (h + 0.2, sc),
                            (D, 1, "io")]))
            P.rot(big, c([(0, 0), (0.35, 20), (h - 0.12, 40), (h, -30, "i"), (h + 0.2, -25), (D, 0)]))
        for j, b in enumerate(small):
            t0 = 0.55 + 0.07 * j
            x0, y0 = ctx.R.bw("flyp_" + b)
            ta = t0 + 0.28
            P.move("flyp_" + b, c([(0, 0), (t0, 0), (ta, fx_ - x0, "i"), (ta + 0.05, fx_ - x0), (ta + 0.45, 0, "io")]),
                   c([(0, 0), (t0, 0), (t0 + 0.14, (fy_ - y0) * 0.5 + 0.2 * H, "o"), (ta, fy_ - y0, "i"), (ta + 0.05, fy_ - y0),
                      (ta + 0.45, 0, "io")]))
            P.rot(b, c([(0, 0), (t0, 0), (ta + 0.45, -900, "l")]))
        flash(P, "ff_hit", t, [(0.55 + 0.07 * j + 0.27, 0.55 + 0.07 * j + 0.45, 0.7) for j in range(len(small))])
        far_impact(P, ctx, t, h, ctx.C.get("skill_fx", {}).get("scale", 1.0), big=False, seed=17)
    return {"dur": D, "fn": f, "hit": h}


def skill_shockwave(ctx, kind):
    """dậm / gầm tại chỗ: sóng đất (ảnh sóng) chạy dọc mặt đất tới đối thủ, tới nơi thì hình lớn trồi lên, nổ."""
    D, t_up, h0, run = 1.7, 0.42, 0.72, 0.36
    h = h0 + run
    mo = motion_of(ctx, "stomp")

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        lean = windup(P, ctx, t, mo, t_up, h0, D)
        secondary(P, ctx, t, lean, 1.1)
        skill_charge(P, t, c, h0)
        x0, _ = ctx.R.bw("flyw")
        fx_, _ = far_of(ctx)
        fx_on(P, "fl_wave", t, h0, h + 0.12, rise=0.05, fade=0.1)
        P.move("flyw", c([(0, 0), (h0, 0), (h, fx_ - x0, "l"), (D, fx_ - x0)]), 0)
        P.scale("fl_wave", c([(0, 0.55), (h0, 0.55), (h, 1.05, "o"), (D, 1.1)]), c([(0, 0.4), (h0, 0.4), (h, 1.0, "o"), (D, 1.0)]))
        fx_on(P, "fx_ground", t, h0 - 0.02, h0 + 0.4, fade=0.25)
        P.scale("fx_ground", c([(0, 0.5), (h0, 0.5), (h0 + 0.3, 1.0, "o"), (D, 1.0)]))
        far_impact(P, ctx, t, h, ctx.C.get("skill_fx", {}).get("scale", 1.0), seed=19)
    return {"dur": D, "fn": f, "hit": h + 0.06}


def skill_rush(ctx, kind):
    """lao húc liên hồi (trận kéo tới đối thủ), không nhảy: cúi đầu cào chân lấy đà, lao thấp và nhanh (spin_dash: cuộn tròn lăn),
    húc, lùi nửa bước, húc cú nữa, hiệu ứng lớn ở chỗ va, lùi về."""
    D, h, h2 = 1.65, 0.85, 1.18

    def lean(t):
        return curve(t, [(0, 0), (0.45, -6), (h, -14, "o"), (h + 0.12, -8), (h2 - 0.08, 4), (h2, -14, "o"), (h2 + 0.15, -6), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.45, -0.07 * H), (h, 0.95 * H, "i"), (h + 0.1, 0.97 * H), (h2 - 0.1, 0.84 * H, "o"),
                 (h2, 0.97 * H, "i"), (h2 + 0.12, 0.97 * H), (D, 0, "io")]))
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.45, 0.9), (0.6, 1.06), (h, 1.08, "o"), (h + 0.1, 0.94), (h2, 1.08, "o"), (h2 + 0.15, 0.97), (D, 1)]))
        hrot(P, c([(0, 0), (0.45, -10), (h, -20, "o"), (h + 0.12, -8), (h2, -20, "o"), (h2 + 0.2, -4), (D, 0)]))
        if has(ctx, "paw"):  # cào chân lấy đà
            P.rot("paw", (14 * math.sin(2 * math.pi * t / 0.15) if 0.08 < t < 0.45 else 0.0))
        if kind == "spin_dash":
            P.rot("spin", c([(0, 0), (0.45, 10), (h, -720, "i"), (h + 0.1, -730, "o"), (h2, -720), (h2 + 0.1, -1080, "o"), (D, -1080)]))
        secondary(P, ctx, t, lean, 1.1)
        if 0.12 < t < 0.45:  # bụi cào chân
            fx_on(P, "fx_ground", t, 0.12, 0.45, rise=0.06, fade=0.15, amax=0.6)
            P.scale("fx_ground", 0.45)
            P.move("fx_ground", -0.1 * H, 0)
        else:
            P.att["fx_ground"] = None
        flash(P, "fx_hit", t, [(h, h + 0.3, 1.0), (h2, h2 + 0.3, 1.15)])
        fx_on(P, "fx_hit2", t, h - 0.02, h + 0.24, fade=0.14)
        P.scale("fx_hit2", c([(0, 0.8), (h - 0.02, 0.8), (h + 0.14, 1.15, "o"), (D, 1.15)]))
        skill_impact(P, ctx, t, c, h2)
    return {"dur": D, "fn": f, "hit": h}


def skill_slide(ctx, kind):
    """trượt bụng (chim cánh cụt): nhún, đổ người nằm sấp, trượt vèo tới đối thủ, va, tảng băng rơi; đứng dậy, lùi về."""
    D, h = 1.75, 0.95

    def lean(t):
        return curve(t, [(0, 0), (0.35, 6), (0.55, -4), (h, -8), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.35, -0.04 * H), (0.55, 0.15 * H, "o"), (h, 0.95 * H, "o"), (h + 0.08, 0.98 * H), (1.4, 0.9 * H),
                 (D, 0, "io")]),
           c([(0, 0), (0.35, 0), (0.55, -0.14 * H, "i"), (h + 0.1, -0.14 * H), (1.35, 0, "o"), (D, 0)]))
        P.rot("spin", c([(0, 0), (0.35, 12), (0.55, -78, "i"), (h, -78), (h + 0.06, -70, "o"), (1.35, 0, "io"), (D, 0)]))
        squash(P, c([(0, 1), (0.35, 0.86), (0.5, 1.08, "o"), (h, 1.0), (h + 0.06, 0.9, "o"), (1.4, 1.0), (D, 1)]))
        for bn in bones_like(ctx.R, "arm", "wing"):
            P.rot(bn, c([(0, 0), (0.35, 20), (0.55, 60, "o"), (h, 60), (1.35, 0), (D, 0)]))
        secondary(P, ctx, t, lean)
        burst(P, t, 0.58, life=0.4, speed=(0.3, 0.6), ang=(100, 170), grav=2.0, seed=23, origin=(-0.55 * H, -0.38 * H))
        skill_impact(P, ctx, t, c, h)
    return {"dur": D, "fn": f, "hit": h}


def skill_combo(ctx, kind):
    """liên hoàn (trận kéo tới đối thủ): lao vào, cào (hoặc đấm), cắn (hoặc húc), rồi xoay người quất đuôi (không đuôi thì húc
    mạnh), mỗi đòn một vệt trúng, đòn cuối nổ lớn."""
    D, b1, b2, b3 = 1.85, 0.42, 0.76, 1.12
    tail = bool(tail_bones(ctx))
    arm = limb(ctx, "paw", "arm_f", "claw_f")

    def lean(t):
        return curve(t, [(0, 0), (0.28, 8), (b1, -10, "o"), (b2 - 0.12, 6), (b2, -12, "o"), (b3 - 0.12, 4), (b3, -14, "o"),
                         (b3 + 0.2, -6), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        go(P, c([(0, 0), (0.28, -0.04 * H), (b1, 0.5 * H, "i"), (b2 - 0.1, 0.48 * H), (b2, 0.58 * H, "i"), (b3 - 0.12, 0.5 * H),
                 (b3, 0.62 * H, "i"), (b3 + 0.15, 0.62 * H), (1.5, 0.4 * H, "o"), (D, 0)]))
        lean_to(P, lean(t))
        squash(P, c([(0, 1), (0.28, 0.92), (b1, 1.06, "o"), (b2 - 0.1, 0.94), (b2, 1.07, "o"), (b3 - 0.1, 0.92), (b3, 1.08, "o"),
                     (b3 + 0.25, 0.98), (D, 1)]))
        hrot(P, c([(0, 0), (0.28, 8), (b1, -6, "o"), (b2 - 0.1, 10), (b2, -22, "o"), (b3 - 0.1, 4), (b3, -10, "o"), (D, 0)]))
        if arm:
            P.rot(arm, c([(0, 0), (0.28, 52), (b1, -10, "o"), (b1 + 0.15, 0), (D, 0)]))
        if tail:
            P.scale("spin", c([(0, 1), (b2 + 0.08, 1), (b3 - 0.06, -1, "io"), (b3 + 0.2, -1), (b3 + 0.36, 1, "io"), (D, 1)]), 1)
            for bones in tail_bones(ctx):
                for i, b in enumerate(bones):
                    P.rot(b, c([(0, 0), (b3 - 0.1, -6 * (1 + 0.3 * i)), (b3, 12 * (1 + 0.3 * i), "o"), (b3 + 0.25, 3), (D, 0)]))
        secondary(P, ctx, t, lean, 0.7)
        flash(P, "fx_hit", t, [(b1, b1 + 0.26, 0.9), (b2, b2 + 0.26, 1.0)])
        flash(P, "fx_hit2", t, [(b1 - 0.02, b1 + 0.22, 1.1), (b2 - 0.02, b2 + 0.22, 1.0)])
        P.rot("fx_hit2", -30 if t < b2 - 0.05 else 10)
        skill_impact(P, ctx, t, c, b3)
    return {"dur": D, "fn": f, "hit": b3}


def skill_leap(ctx, kind):
    """chiêu cuối lao tới (trận kéo tới đối thủ): tụ lực (lốc nước dưới chân, nén thấp), bật nhảy vòng cung / lướt thấp, giáng
    xuống trước đối thủ, khựng, hiệu ứng lớn (cột nước, nổ, sóng, hạt văng), lùi về."""
    D, h, hold = 1.7, 0.98, 0.12
    up = 0.42 * H if kind == "leap" else 0.06 * H

    def lean(t):
        return curve(t, [(0, 0), (0.42, 12), (0.7, -4), (h - 0.05, 6), (h, -16, "o"), (h + hold, -16), (1.3, -4), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.42, -0.08 * H), (0.7, 0.45 * H, "o"), (h, 0.9 * H, "i"), (h + hold, 0.91 * H), (1.28, 0.88 * H),
                (1.5, 0.3 * H, "io"), (D, 0)])
        my = c([(0, 0), (0.42, 0), (0.7, up, "o"), (h, 0, "i"), (1.36, 0), (1.44, 0.08 * H, "o"), (1.56, 0, "i"), (D, 0)])
        P.move("move", mx, my)
        P.move("shadow", mx, 0)
        P.scale("shadow", c([(0, 1), (0.7, 1 - 0.5 * up / (0.42 * H), "o"), (h, 1, "i"), (D, 1)]))
        P.rot("base", 0.45 * lean(t))
        P.rot("body", 0.55 * lean(t))
        squash(P, c([(0, 1), (0.42, 0.86), (0.5, 1.12, "o"), (0.8, 1.04), (h, 0.88, "i"), (h + hold, 0.9), (1.3, 1.03),
                     (1.5, 0.97), (D, 1)]))
        P.rot("head", c([(0, 0), (0.42, 16), (0.7, -6), (h, -20, "o"), (h + hold, -20), (1.36, 4), (D, 0)]))
        for bn in bones_like(ctx.R, "wing"):
            P.rot(bn, c([(0, 0), (0.42, 26), (0.56, -30, "o"), (0.7, 30), (0.84, -26), (h, 20), (h + 0.1, -10), (D, 0)]))
        for bn in bones_like(ctx.R, "claw_f", "arm_f", "prop"):
            P.rot(bn, c([(0, 0), (0.42, 40), (0.8, 60), (h, -60, "o"), (h + hold, -55), (1.4, 0), (D, 0)]))
        secondary(P, ctx, t, lean, 1.2)
        skill_charge(P, t, c, 0.66, True)
        skill_impact(P, ctx, t, c, h)
    return {"dur": D, "fn": f, "hit": h}


def skill_summon(ctx, kind):
    """chiêu cuối đứng tại chỗ gọi (rùa, chim, chuông): tụ lực lâu (lốc nước, vòng bùa), ngửa gầm / hát, rồi chồm tới: hiệu
    ứng lớn rơi / trồi lên trước mặt (trận không kéo lao)."""
    D, h, hold = 1.8, 1.04, 0.12

    def lean(t):
        return curve(t, [(0, 0), (0.5, 12), (h - 0.06, 14), (h, -10, "o"), (h + hold, -10), (1.4, 2), (D, 0)])

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        # lướt tới trước khi tung chiêu (trận kéo đỉnh lao tới đối thủ, hiệu ứng lớn rơi đúng chỗ đối thủ), rồi lùi về
        mx = c([(0, 0), (0.5, -0.04 * H), (h - 0.08, 0.7 * H, "io"), (h + hold, 0.72 * H), (1.42, 0.66 * H), (D, 0)])
        my = c([(0, 0), (0.5, 0), (0.7, 0.12 * H, "o"), (h - 0.08, 0, "i"), (D, 0)])
        P.move("move", mx, my)
        P.move("shadow", mx, 0)
        P.rot("base", 0.4 * lean(t))
        P.rot("body", 0.6 * lean(t))
        squash(P, c([(0, 1), (0.5, 1.07), (h - 0.06, 1.08), (h, 0.9, "o"), (h + hold, 0.92), (1.4, 1.02), (D, 1)]))
        P.rot("head", c([(0, 0), (0.5, 20), (h - 0.06, 22), (h, -14, "o"), (h + hold, -14), (1.45, 3), (D, 0)]))
        for bn in bones_like(ctx.R, "wing"):
            P.rot(bn, c([(0, 0), (0.25, 20), (0.4, -18), (0.55, 24), (0.7, -16), (0.85, 26), (h, -30, "o"), (D, 0)]))
        secondary(P, ctx, t, lean, 1.2)
        skill_charge(P, t, c, h - 0.02, True)
        skill_impact(P, ctx, t, c, h)
    return {"dur": D, "fn": f, "hit": h}


def skill_charge(P, t, c, t_end, shield=False):
    """tụ lực: lốc quanh người (vòng quay); shield: khiên (ảnh fx_shield) nở ra trước thân và vòng phía trước (chỉ kiểu chiêu cũ;
    kiểu mới chỉ vòng phía sau, nhạt, để thấy dáng tụ lực)."""
    if shield:
        fx_on(P, "fx_shield", t, 0.1, t_end, rise=0.15, fade=0.15, amax=0.8)
    else:
        P.att["fx_shield"] = None
    P.scale("fx_shield", c([(0, 0.6), (0.3, 1.05, "o"), (t_end, 1.0)]))
    fx_on(P, "fx_ring_b", t, 0.0, t_end, rise=0.25, fade=0.18, amax=0.85 if shield else 0.6)
    if shield:
        fx_on(P, "fx_ring_f", t, 0.0, t_end, rise=0.25, fade=0.18, amax=0.5)
    else:
        P.att["fx_ring_f"] = None
    P.rot("fx_ring", c([(0, 0), (t_end, -520, "l")]))
    P.scale("fx_ring", c([(0, 0.5), (0.3, 1.05, "o"), (t_end, 1.25)]))


def skill_impact(P, ctx, t, c, h):
    """hiệu ứng lớn của chiêu cuối (beasts_cfg "skill_fx"): fx_big (cột nước / vật rơi / pha lê trồi), fx_big2 (nổ), fx_wave
    (sóng sau đối thủ), fx_ground (vòng loang), hạt văng; rơi từ trên (drop) hay trồi lên (rise)."""
    sp = ctx.C.get("skill_fx", {})
    s = sp.get("scale", 1.0)
    fx_on(P, "fx_ground", t, h, h + 0.55, fade=0.3)
    P.scale("fx_ground", c([(0, 0.4), (h, 0.4), (h + 0.4, 1.35 * s, "o"), (h + 1, 1.35 * s)]))
    P.move("fx_ground", ctx.info["front"] + 0.35 * H - (ctx.info["front"] + ctx.info["back"]) / 2, 0)
    if sp.get("drop"):  # vật rơi từ trên xuống (chuông, băng) chạm đất ở h
        fx_on(P, "fx_big", t, h - 0.3, h + 0.5, rise=0.08, fade=0.25)
        P.move("fx_big", 0, c([(0, 1.6 * H), (h - 0.3, 1.6 * H), (h, 0, "i"), (h + 0.06, 0.05 * H, "o"), (h + 0.14, 0, "i")]))
        P.scale("fx_big", s * c([(0, 1.0), (h, 1.0), (h + 0.05, 1.12, "o"), (h + 0.16, 1.0), (h + 1, 1.0)]),
                s * c([(0, 1.0), (h, 1.0), (h + 0.05, 0.86, "o"), (h + 0.16, 1.0), (h + 1, 1.0)]))
    else:  # cột nước / pha lê trồi lên
        fx_on(P, "fx_big", t, h, h + 0.55, fade=0.25)
        P.scale("fx_big", s * c([(0, 0.6), (h, 0.6), (h + 0.18, 1.15, "o"), (h + 0.45, 1.25), (h + 1, 1.25)]),
                s * c([(0, 0.15), (h, 0.15), (h + 0.2, 1.0, "o"), (h + 1, 1.05)]))
    fx_on(P, "fx_big2", t, h, h + 0.36, fade=0.22)
    P.scale("fx_big2", s * c([(0, 0.5), (h, 0.5), (h + 0.26, 1.6, "o"), (h + 1, 1.6)]))
    if sp.get("wave", True):
        fx_on(P, "fx_wave", t, h + 0.05, h + 0.7, fade=0.28)
        P.scale("fx_wave", s * c([(0, 0.4), (h + 0.05, 0.4), (h + 0.27, 1.15, "o"), (h + 0.55, 1.25), (h + 1, 1.25)]),
                s * c([(0, 0.2), (h + 0.05, 0.2), (h + 0.27, 1.15, "o"), (h + 0.55, 1.3), (h + 1, 1.3)]))
    ox = ctx.info["front"] + 0.35 * H - (ctx.info["front"] + 0.18 * H)
    burst(P, t, h, life=0.6, speed=(0.6, 1.2), ang=(30, 150), grav=1.6, seed=7, size=(0.8, 1.5), origin=(ox, -0.42 * H))


# ---------------------------------------------------------------- tiến hóa
def evolve(ctxA, ctxB, M, idleB0, scaleB):
    """dạng A thành dạng B (xương n_): A gồng, nước dâng lốc quanh người, A tan dần, B hiện lớn dần trong lốc, nước vỡ tung,
    B gầm (ngửa đầu) rồi về đúng khung đầu clip đứng của B."""
    D = 2.8
    slotsA = [s["name"] for s in ctxA.R.slots]
    slotsB = ["n_" + s["name"] for s in ctxB.R.slots]
    endB = {"n_" + b: v for b, v in idleB0.t.items()}

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        squash(P, c([(0, 1), (0.3, 0.88), (0.45, 1.06, "o"), (1.2, 0.95), (D, 0.95)]))
        P.rot("head", c([(0, 0), (0.3, -6), (0.6, 14, "o"), (1.2, 18), (D, 18)]))
        aA = c([(0, 1), (1.0, 1), (1.3, 0, "io"), (D, 0)])
        for s_ in slotsA:
            if s_ not in ctxA.R.fx_slots:
                P.alpha[s_] = aA
        P.att["fx_ground"] = "fx_ground" if 0.4 <= t < 2.3 else None
        P.alpha["fx_ground"] = c([(0, 0), (0.4, 0), (0.6, 1), (1.8, 1), (2.3, 0)])
        P.scale("fx_ground", c([(0, 0.3), (0.4, 0.3), (0.9, 1.25, "o"), (2.0, 1.35), (D, 1.35)]))
        for s_ in ("fx_ring_b", "fx_ring_f"):
            P.att[s_] = s_ if 0.5 <= t < 1.95 else None
        P.alpha["fx_ring_b"] = c([(0, 0), (0.5, 0), (0.85, 0.9), (1.6, 0.9), (1.9, 0)])
        P.alpha["fx_ring_f"] = c([(0, 0), (0.5, 0), (0.85, 0.6), (1.0, 0.88), (1.45, 0.88), (1.65, 0.5), (1.9, 0)])
        P.rot("fx_ring", c([(0, 0), (1.95, -1000, "l"), (D, -1000)]))
        P.scale("fx_ring", c([(0, 0.4), (0.5, 0.4), (0.95, 1.1, "o"), (1.55, 1.2), (1.9, 1.6, "o"), (D, 1.6)]),
                c([(0, 0.3), (0.5, 0.3), (0.95, 0.9, "o"), (1.55, 1.0), (1.9, 1.3, "o"), (D, 1.3)]))
        P.att["fx_big2"] = "fx_big2" if 1.55 <= t < 2.2 else None
        P.alpha["fx_big2"] = c([(0, 1), (1.8, 1), (2.2, 0)])
        P.scale("fx_big2", c([(0, 0.5), (1.55, 0.5), (1.95, 2.0, "o"), (D, 2.0)]))
        cx = (ctxA.info["front"] + ctxA.info["back"]) / 2
        P.move("fx_big2", cx - (ctxA.info["front"] + 0.35 * H), 0.0)
        fx_on(P, "fx_drops", t, 1.65, 2.35, fade=0.35)
        P.scale("fx_drops", c([(0, 0.8), (1.65, 0.8), (2.35, 2.2, "o")]))
        P.move("fx_drops", c([(0, 0), (1.65, 0), (2.35, 0.1 * H, "o")]), c([(0, 0), (1.65, 0), (2.35, 0.3 * H, "o")]))
        aB = c([(0, 0), (1.08, 0), (1.4, 1, "io"), (D, 1)])
        for s_ in slotsB:
            if s_.replace("n_", "", 1) not in ctxB.R.fx_slots:
                P.alpha[s_] = aB
        P.scale("evo", scaleB * c([(0, 0.86), (1.0, 0.86), (1.95, 1.0, "o"), (D, 1.0)]))
        P.move("evo", 0, c([(0, -10), (1.0, -10), (1.85, 0, "o"), (D, 0)]))
        fl = c([(0, 0), (1.55, 0), (2.0, 1, "o"), (2.4, 1), (2.75, 0, "io"), (D, 0)])
        P.rot("n_head", 18 * fl)
        squash(P, 1 + 0.08 * fl, "n_base")
        for b in bones_like(ctxB.R, "wing"):
            P.rot("n_" + b, 26 * fl)
        P.alpha["shadow"] = aA
        P.alpha["n_shadow"] = aB

    def post(t, P):
        w = L.smooth01((t - (D - 0.35)) / 0.35)
        if w <= 0:
            return
        for b in set(endB) | {b for b in P.t if b.startswith("n_")}:
            tb = endB.get(b, [0, 0, 0, 1, 1])
            ta = P._g(b)
            for q in range(5):
                ta[q] = ta[q] * (1 - w) + tb[q] * w
    return {"dur": D, "fn": f, "post": post}


def clips_of(ctx):
    return {"idle": idle(ctx), "hit": hit(ctx), "attack": attack(ctx), "cast": cast(ctx), "skill": skill(ctx)}


# ---------------------------------------------------------------- xuất
def portrait(ctx, out, res):
    """chân dung vuông 512 cắt thẳng từ concept: khung vuông ôm cả con (đầu lệch giữa một chút), không bóng."""
    rgb, fg = ctx.rgb, ctx.fg
    ys, xs = np.nonzero(fg)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    side = int(max(x1 - x0, y1 - y0) * 1.06)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8) * 255
    rgba = np.dstack([rgb, a.astype(np.uint8)])
    canvas = np.zeros((side, side, 4), np.uint8)
    ax0, ay0 = int(round(cx - side / 2)), int(round(cy - side / 2))
    sx0, sy0 = max(0, ax0), max(0, ay0)
    sx1, sy1 = min(rgb.shape[1], ax0 + side), min(rgb.shape[0], ay0 + side)
    canvas[sy0 - ay0:sy1 - ay0, sx0 - ax0:sx1 - ax0] = rgba[sy0:sy1, sx0:sx1]
    im = Image.fromarray(canvas)
    im.save(os.path.join(out, "chan_dung.png"))
    im.resize((512, 512), Image.LANCZOS).save(os.path.join(res, code(ctx.hid, ctx.k) + "_portrait.png"))


def game_info(R, clips, baked, C, k):
    g = T.game_info(R, clips, baked)
    g["beam"] = C.get("beam", {}).get(k, 1.0)
    atk, sk = style_of(C, k, "attack", "bite"), style_of(C, k, "skill", "erupt")
    g["lunge"] = ["skill"] if sk in LUNGE_SKILL or sk in ("leap", "dash", "summon") else []
    # clip có hiệu ứng ở chỗ đối thủ (xương far, fly*): game dời tới đối thủ (AolaActor.FarAtomik)
    g["far"] = (["attack"] if atk in RANGED else []) + (["skill"] if sk in FAR_SKILL else [])
    if C.get("beamStyle"):
        g["beamStyle"] = C["beamStyle"]
    return g


def build_form(hid, k, nxt=None, gif=True):
    C = cfg(hid)
    R, ctx = build_rig(hid, k)
    od = out_dir(hid, k)
    os.makedirs(od, exist_ok=True)
    Q.debug_layers(ctx, os.path.join(od, "lop.png"))
    Q.LAYERS[k] = ctx.F["layers"]
    Q.label_sheet(k, ctx.rgb, ctx.lab, os.path.join(od, "nhan.png"), extra=list(ctx.J.values()) + [ctx.F["mouth"]])
    clips = clips_of(ctx)
    baked = Q.clean({n: L.bake(R, c, {}) for n, c in clips.items()}, R)
    hgt = L.idle_height(R, baked["idle"][0])
    res_dir = os.path.join(T.RES, code(hid, k))
    Rx = R
    if nxt:
        ctxB, RB, idleB0, hB = nxt
        M = L.merge_next(R, RB)
        M.chain_tips, M.legs = {}, {}
        M.points = dict(R.points)
        M.weapon_ang = 0.0
        ev = evolve(ctx, ctxB, M, idleB0, hgt / hB)
        hide = {"n_" + s["name"] for s in RB.slots}
        clipsM = {}
        for n, c in clips.items():
            def fn(t, P, f0=c["fn"]):
                f0(t, P)
                for s_ in hide:
                    P.att[s_] = None
            clipsM[n] = dict(c, fn=fn)
        clipsM["evolve"] = ev
        bakedM = Q.clean({n: L.bake(M, c, {}) for n, c in clipsM.items()}, M)
        Rx, clips, baked = M, clipsM, bakedM
    game = game_info(Rx, clips, baked, C, k)
    game["height"] = round(hgt, 2)
    print(f"  {code(hid, k)}: {len(Rx.bones)} xương, {len(Rx.slots)} slot, cao {hgt:.0f}, trận {json.dumps(game, ensure_ascii=False)}")
    aw, ah = L.export(Rx, clips, baked, od, res_dir, game, H, gif=gif)
    print(f"  atlas {aw}x{ah}, ra {od}")
    portrait(ctx, od, res_dir)
    with open(os.path.join(od, "baked.pkl"), "wb") as fh:
        pickle.dump((Rx, {n: c["dur"] for n, c in clips.items()}, baked), fh)
    return ctx, R, baked["idle"][0], hgt


def build_line(hid, gif=True):
    C = cfg(hid)
    ks = sorted(C["forms"])
    nxt = None
    for k in reversed(ks):
        nxt = build_form(hid, k, nxt, gif=gif)


def show(hid, k, clip, times, fh=420):
    with open(os.path.join(out_dir(hid, k), "baked.pkl"), "rb") as f_:
        R, durs, baked = pickle.load(f_)
    frames = baked[clip]
    kk = fh / (1.6 * H)
    Wb = int(3.4 * H * kk)
    imgs = []
    for t in times:
        i = min(len(frames) - 1, round(t * L.FPS))
        box = (Wb, fh, int(0.9 * H * kk), int(fh - 0.1 * H * kk))
        im = Image.fromarray(L.render(R, frames[i], kk, box))
        ImageDraw.Draw(im).text((6, 6), f"{clip} {t:.2f}s", fill=(43, 33, 24))
        imgs.append(np.array(im))
    p = os.path.join(out_dir(hid, k), f"xem_{clip}.png")
    Image.fromarray(np.concatenate(imgs, 0) if len(imgs) > 3 else np.concatenate(imgs, 1)).save(p)
    print(p)


def grid(hid, k):
    """ảnh concept kẻ lưới 50 px (số mỗi 100) để đọc toạ độ khớp, vùng."""
    p = src(hid, k)
    im = Image.open(p).convert("RGB")
    d = ImageDraw.Draw(im)
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    for x in range(0, im.width, 50):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if x % 100 == 0 else (255, 170, 170), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=F)
    for y in range(0, im.height, 50):
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255) if y % 100 == 0 else (170, 170, 255), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(0, 0, 200), font=F)
    o = os.path.join(base(hid, k), "luoi.png")
    os.makedirs(base(hid, k), exist_ok=True)
    im.save(o)
    print(o)


def main(argv):
    hid, step = argv[0], argv[1]
    if step == "grid":
        grid(hid, int(argv[2]))
    elif step == "nhan":
        k = int(argv[2])
        F = cfg(hid)["forms"][k]
        setup_labels(hid, k, F)
        rgb, fg = load(hid, k, F)
        lab = Q.labels(k, rgb, fg)
        os.makedirs(out_dir(hid, k), exist_ok=True)
        p = os.path.join(out_dir(hid, k), "nhan.png")
        Q.label_sheet(k, rgb, lab, p, extra=list(F["bones"].values()) + [F["mouth"]])
        print(p)
    elif step == "rig":
        build_form(hid, int(argv[2]), gif="--gif" in argv)
    elif step == "all":
        build_line(hid)
    elif step == "show":
        show(hid, int(argv[2]), argv[3], [float(x) for x in argv[4].split(",")])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
