# -*- coding: utf-8 -*-
"""Vua robot non (DẠNG 1, concept A đã duyệt: inbox/vua_may_non/tai_ve/L1_duyet.png): MẢNH.

Rig dạng 1 = rig dạng 2 dựng bằng da dạng 1 rồi đổi tỉ lệ xương (mau/ti_le.json, như hình bố cục). Mảnh nào giữ hình bóng thì nằm ĐÚNG
khung mảnh dạng 2 (inbox/vua_may_1/manh); mảnh đổi dáng (vương miện, mặt, bốn cánh, hào quang) gen đúng chỗ trên concept A rồi đổi toạ độ
về KHUNG DẠNG 2 (w2 = S2_xương · M1_xương⁻¹ · w1: M1 = ma trận thế giới của xương trong rig ĐÃ đổi tỉ lệ ở khung 0 idle, S2 = dáng gốc rig
dạng 2), để sau khi đổi tỉ lệ nó về đúng chỗ trên concept.

  - dùng lại nguyên mảnh dạng 2 (cùng màu theo concept A): giáp vai, dải lam, cẳng tay, bắp tay, bàn tay, ngón, bánh răng, chân, quyền
    trượng, Mặt Trời, ba hành tinh;
  - K1, K4 CHUYỂN DA (tờ = mảnh dạng 2 đặt đúng ô tờ K của dạng 2; GPT làm gọn theo concept A): áo choàng sau / trước bỏ huy hiệu bánh
    răng, ngực bỏ lưới thông gió; lưng, bụng, khối hông, eo gọn;
  - N1: vương miện hoàng tử + mặt (cả đầu); N2: vòng hào quang; N3: bốn cánh (mỗi cánh MỘT mảnh liền: tay cánh + lông). Râu bỏ.

    vua_may_non_manh.py kiem_map   kiểm phép đổi px bố cục ↔ đơn vị rig (vẽ rig đã đổi tỉ lệ bằng bộ vẽ Python, so hình bố cục)
    vua_may_non_manh.py can        căn concept A lên khung bố cục (đồng dạng không xoay, IoU vùng thân) → mau/can.json
    vua_may_non_manh.py to         tờ K1, K4 chuyển da + file prompt K, N → mau/da_K*.png, gui_gpt/vua_may_non/luot_2_*.txt
    vua_may_non_manh.py chep       chép mảnh dạng 2 dùng lại → manh/ + moi.json (bỏ râu)
    vua_may_non_manh.py cat [K1|K4|N1|N2|N3]   cắt ảnh về → manh/, moi.json, tờ so
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402
import vua_may_non as NN  # noqa: E402

W, H = 1536, 1024
BASE = NN.BASE
MAU, TAI, GUI = NN.MAU, NN.TAI, NN.GUI
MANH = os.path.join(BASE, "manh")
MANH2 = os.path.join(HERE, "inbox", "vua_may_1", "manh")
MAU2 = os.path.join(HERE, "inbox", "vua_may_1", "mau")
CON = os.path.join(TAI, "L1_duyet.png")
DANG2 = NN.DANG2
INK = (43, 33, 24)
MUC = "#2B2118"
BC_W, BC_H = 1480, 1040                        # cỡ canvas của mau/bo_cuc.png (atomik_bocuc.py --w --h)


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def mat_na(rgb, nguong=236):
    """hình bóng trên nền trắng: mọi px không trắng nối với hình, lấp lỗ."""
    k = rgb.min(2) < nguong
    k = cv2.morphologyEx(k.astype(np.uint8), cv2.MORPH_CLOSE, el(2)).astype(bool)
    from scipy import ndimage as nd
    return nd.binary_fill_holes(k)


# ================================================================ phép đổi toạ độ
def rig2():
    return A.load(NN.RIG2)


_R = {}


def he():
    """(J2 dạng 2, J1 đã đổi tỉ lệ, P2 dáng gốc dạng 2, P1 khung 0 idle dạng 1)."""
    if not _R:
        J2, img2, _ = rig2()
        J1 = json.loads(json.dumps(J2))
        A.scale_bones(J1, json.load(open(NN.TI_LE, encoding="utf-8")))
        P2 = A.Pose(J2).at(None, 0.0)
        P1 = A.Pose(J1).at(A.clip(J1, "idle"), 0.0)
        _R.update(J2=J2, J1=J1, img2=img2, P2=P2, P1=P1, B=A.bi(J2))
    return _R


def _m3(w):
    a, b, c, d, x, y = w
    return np.array([[a, b, x], [c, d, y], [0, 0, 1.0]])


def d1_ve_d2(V1, xuong):
    """đỉnh thế giới dạng 1 (khung 0 idle, đã đổi tỉ lệ) → thế giới dáng gốc rig dạng 2, gắn cứng theo xương."""
    R = he()
    i = R["B"][xuong]
    M = _m3(R["P2"].w[i]) @ np.linalg.inv(_m3(R["P1"].w[i]))
    V1 = np.asarray(V1, float).reshape(-1, 2)
    return (M @ np.c_[V1, np.ones(len(V1))].T).T[:, :2]


def bc_map():
    """(px bo_cuc_khung 1536 × 1024 → thế giới dạng 1, ngược lại)."""
    j = json.load(open(os.path.join(MAU, "bo_cuc_khung.json")))
    to_rig, to_px, z = A.canvas_map(NN.KHUNG, BC_W, BC_H)

    def f(P):
        P = (np.asarray(P, float).reshape(-1, 2) - [j["ox"], j["oy"]]) / j["k"]
        return to_rig(P)

    def g(V):
        return to_px(np.asarray(V, float).reshape(-1, 2)) * j["k"] + [j["ox"], j["oy"]]
    return f, g, z / j["k"]


def kiem_map():
    R = he()
    f, g, upx = bc_map()
    bc = np.asarray(Image.open(os.path.join(MAU, "bo_cuc_khung.png")).convert("RGB"))
    mb = mat_na(bc)
    x0, y0 = f([[0, 0]])[0]
    x1, y1 = f([[W, H]])[0]
    im = A.render(R["J1"], R["img2"], R["P1"], (x0, y1, x1, y0), 1.0 / upx, bg=None)
    im = im.resize((W, H))
    mr = np.asarray(im)[..., 3] > 100
    iou = (mb & mr).sum() / (mb | mr).sum()
    print(f"bộ vẽ Python (rig đổi tỉ lệ, khung 0 idle) so hình bố cục: IoU {iou:.3f}; {upx:.3f} đơn vị / px")
    o = np.full((H, W, 3), 255, np.uint8)
    o[mb & ~mr] = (230, 60, 60)
    o[mr & ~mb] = (60, 160, 230)
    o[mb & mr] = (200, 200, 200)
    Image.fromarray(o).save(os.path.join(MAU, "_kiem_map.png"))


# ================================================================ căn concept A lên khung bố cục
VUNG_THAN = (430, 470, 1000, 790)               # px khung bố cục: ngực, vai, tay, áo choàng (chỗ gắn đầu, cánh, hào quang; bỏ chân, đầu đổi dáng)


def can():
    bc = np.asarray(Image.open(os.path.join(MAU, "bo_cuc_khung.png")).convert("RGB"))
    co = np.asarray(Image.open(CON).convert("RGB").resize((W, H), Image.LANCZOS))
    mb, mc = mat_na(bc), mat_na(co)
    x0, y0, x1, y1 = VUNG_THAN
    vung = np.zeros((H, W), bool)
    vung[y0:y1, x0:x1] = True
    ys, xs = np.nonzero(mb & vung)
    pts = np.c_[xs, ys][::5].astype(np.float32)
    best = (0, 1.0, 0, 0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for a in np.arange(0.92, 1.081, 0.01):
        for dx in range(-40, 41, 4):
            for dy in range(-40, 41, 4):
                q = np.c_[cx + (pts[:, 0] - cx) * a + dx, cy + (pts[:, 1] - cy) * a + dy].round().astype(int)
                ok = (q[:, 0] >= 0) & (q[:, 0] < W) & (q[:, 1] >= 0) & (q[:, 1] < H)
                hit = mc[q[ok, 1], q[ok, 0]].mean()
                if hit > best[0]:
                    best = (hit, a, dx, dy)
    _, a, dx, dy = best
    # tinh chỉnh từng px quanh nghiệm thô, đo IoU thật
    M = lambda a_, dx_, dy_: np.float32([[a_, 0, cx * (1 - a_) + dx_], [0, a_, cy * (1 - a_) + dy_]])  # noqa: E731

    def iou_(a_, dx_, dy_):
        w_ = cv2.warpAffine(mb.astype(np.uint8), M(a_, dx_, dy_), (W, H), flags=cv2.INTER_NEAREST).astype(bool)
        v_ = cv2.warpAffine(vung.astype(np.uint8), M(a_, dx_, dy_), (W, H), flags=cv2.INTER_NEAREST).astype(bool)
        return ((w_ & mc) & v_).sum() / max(1, ((w_ | mc) & v_).sum())
    b2 = (iou_(a, dx, dy), a, dx, dy)
    for a_ in np.arange(a - 0.01, a + 0.0101, 0.005):
        for dx_ in range(dx - 4, dx + 5):
            for dy_ in range(dy - 4, dy + 5):
                v = iou_(a_, dx_, dy_)
                if v > b2[0]:
                    b2 = (v, a_, dx_, dy_)
    iou, a, dx, dy = b2
    out = dict(a=float(a), dx=float(dx), dy=float(dy), cx=cx, cy=cy, iou=float(iou))
    json.dump(out, open(os.path.join(MAU, "can.json"), "w"), indent=1)
    print(f"căn concept A ↔ khung bố cục (px bố cục → px concept): a {a:.3f}, dời {dx}, {dy}; IoU vùng thân {iou:.3f}")
    w_ = cv2.warpAffine(mb.astype(np.uint8), M(a, dx, dy), (W, H), flags=cv2.INTER_NEAREST).astype(bool)
    o = np.full((H, W, 3), 255, np.uint8)
    o[w_ & ~mc] = (230, 60, 60)
    o[mc & ~w_] = (60, 160, 230)
    o[w_ & mc] = (200, 200, 200)
    Image.fromarray(o).save(os.path.join(MAU, "_so_can.png"))


def phep_can():
    """(px concept A → thế giới dạng 1, thế giới dạng 1 → px concept A, đơn vị / px concept)."""
    j = json.load(open(os.path.join(MAU, "can.json")))
    f, g, upx = bc_map()
    a, dx, dy, cx, cy = j["a"], j["dx"], j["dy"], j["cx"], j["cy"]

    def c2w(P):
        P = np.asarray(P, float).reshape(-1, 2)
        return f(np.c_[(P[:, 0] - dx - cx * (1 - a)) / a, (P[:, 1] - dy - cy * (1 - a)) / a])

    def w2c(V):
        P = g(V)
        return np.c_[P[:, 0] * a + cx * (1 - a) + dx, P[:, 1] * a + cy * (1 - a) + dy]
    return c2w, w2c, upx / a


# ================================================================ K: chuyển da (tờ = mảnh dạng 2 của mình, phóng đều, mỗi mảnh một ô)
M = dict(do="#DC3328", long="#FBEED2", bac="#BDBCBF", bac_toi="#9A9AA0", vang="#F0B42C", vang_toi="#C98F1E", sat="#59585D",
         gang="#4D4C51", xanh="#1A60E8")
MO_TA_CON = ("a young robot PRINCE in three-quarter view: a round grey robot head with two big round yellow eyes and NO beard, a low gold "
             "prince crown with three small points and a red jewel, gold and silver armour with thin gold rims and very few rivets, a short "
             "plain red cape with a cream fur edge over the left shoulder (NO emblem on it), a blue sash with a small gold gear on the right "
             "shoulder, a plain silver chest, big silver forearms with gold bands, dark gloved hands, a sceptre with a little Sun and three "
             "small planets, two short robot legs with gold boots, four small white wings with gold tips and a thin gold halo ring")
TO_K = {"K1": (0.85, [["pifenghou_01", "pifengqian", "xiongqiong"], ["xiabanshen_02", "beibu", "fubu"]])}
_ = M
MO_TA_K = {
    "pifenghou_01": f"the long BACK part of the royal CAPE: flat red {_['do']}; KEEP its cream fur trim {_['long']} (round scalloped tufts) "
                    "exactly where it is (along its long left edge and its bottom edge); REMOVE the gold gear emblem: plain red there, "
                    "nothing else on the cape.",
    "pifengqian": f"the FRONT part of the cape over the shoulder: flat red {_['do']}; KEEP its cream fur trim {_['long']} along its lower "
                  "edge; REMOVE the gold gear emblem: plain red there; nothing else.",
    "xiongqiong": f"the barrel CHEST: flat silver {_['bac']} with ONE gold {_['vang']} trim along its outer rim; KEEP the dark oval neck "
                  f"opening at its top (very dark steel {_['sat']}); REMOVE the gold vent grille and the round rivet: plain silver there.",
    "xiabanshen_02": f"the wide HIP BLOCK (three boxes side by side): flat silver {_['bac']} (instead of dark steel), each box with a thin "
                     f"gold {_['vang']} rim line, the middle box with a slightly darker silver {_['bac_toi']} inset panel.",
    "beibu": f"the BACK PLATE: flat silver {_['bac']} with a gold {_['vang']} rim (as it is).",
    "fubu": f"the Y-shaped BELLY PLATE: a gold {_['vang']} outer frame with a plain silver {_['bac']} inset panel (as it is).",
}
VI_K = {"K1": "áo choàng sau + trước (bỏ huy hiệu bánh răng), ngực (bỏ lưới thông gió), khối hông (bạc viền vàng), lưng, bụng"}


def to_k(ten):
    z, hang = TO_K[ten]
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    o = {}
    rows = []
    for h_ in hang:
        cs = []
        for r in h_:
            im = Image.open(os.path.join(MANH2, r + ".png")).convert("RGBA")
            big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
            cs.append((r, big))
        rows.append((cs, max(c[1].height for c in cs)))
    ke_y = (H - sum(c[1] for c in rows)) // (len(rows) + 1)
    y = ke_y
    for cs, hh in rows:
        ke = (W - sum(c[1].width for c in cs)) // (len(cs) + 1)
        assert ke > 12 and ke_y > 12, (ten, ke, ke_y)
        x = ke
        for r, big in cs:
            y0 = y + (hh - big.height) // 2
            can_.alpha_composite(big, (x, y0))
            o[r] = dict(hop=[x, y0, big.width, big.height], z=z)
            x += big.width + ke
        y += hh + ke_y
    p = os.path.join(MAU, f"da_{ten}.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_k(ten, o):
    mau = os.path.join(MAU, f"da_{ten}.png")
    out = os.path.join(TAI, f"D_{ten}.png")
    p = os.path.join(GUI, f"luot_2_da_{ten}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: six parts of a 2D animation puppet (a robot king), each drawn "
         "alone at the exact size and place to keep: top row the long back part of a red cape, the front part of the cape, the barrel "
         "chest; bottom row the wide hip block, the back plate, the Y-shaped belly plate. They are already hand-drawn in the right style; "
         "some of them carry details that must go.",
         f"image 2 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: {MO_TA_CON}. Take from it the colours "
         "and how SIMPLE the parts are. The shapes come from image 1.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ten}_2.png, D_{ten}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: SIMPLIFY. Redraw the SAME sheet with every part repainted as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet (if "
         "the new picture were laid over image 1, every part must coincide with the old one). Do NOT merge parts, do NOT add parts, do NOT "
         "move parts. Pure white (#FFFFFF) between the parts.", "",
         f"STYLE: exactly the style of image 1 and image 2: a wobbly dark-brown ink outline ({MUC}, about 9 px) all the way round every part "
         "exactly on its silhouette, thin ink lines for the few inner lines, every area ONE flat colour with visible coloured-pencil / "
         "wax-crayon hatching. No shading, no highlights, no gradients, no glow, no shadows. SIMPLE: big plain areas, no emblems, no extra "
         "rivets, no engravings.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {MO_TA_K[r]}")
    t += ["", "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."]
    ghi(p, t)
    print(p)
    return p


def nen_trang(A_):
    trang = (A_.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def moi_nhat(thu_muc, goc):
    fs = [f for f in os.listdir(thu_muc) if f.startswith(goc) and f.endswith(".png") and
          (f[len(goc):-4] == "" or (f[len(goc)] == "_" and f[len(goc) + 1:-4].isdigit()))]
    return os.path.join(thu_muc, max(fs, key=lambda f: os.path.getmtime(os.path.join(thu_muc, f)))) if fs else None


def _to_so(ims, p):
    w_ = sum(i.width + 10 for i in ims) + 10
    h_ = max(i.height for i in ims) + 20
    o = Image.new("RGB", (w_, h_), (150, 150, 150))
    x = 10
    for i in ims:
        o.paste(i, (x, 10), i)
        x += i.width + 10
    o.save(p)
    print(p)


def cat_k(ten):
    """mỗi mảnh: lấy đúng ô của nó trên tờ, tách nền trắng, đưa về cỡ mảnh dạng 2, kẹp trong hình bóng mảnh dạng 2 (nới 3 px), chỗ GPT vẽ
    hụt lấy màu gần nhất."""
    path = moi_nhat(TAI, f"D_{ten}")
    if not path:
        print(f"{ten}: chưa gen")
        return
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    A_ = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    print(f"{ten}:", os.path.basename(path))
    o = json.load(open(os.path.join(MAU, f"da_{ten}.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(MAU, f"da_{ten}.png")).convert("RGB")).astype(np.int32)
    fg = ~nen_trang(A_)
    fgG = ~nen_trang(Gd)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    so = []
    for r, d in o.items():
        x, y, cw, ch = d["hop"]
        pad = 14
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
        gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
        sub = lab[y0:y1, x0:x1]
        ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 30]
        m = np.isin(lab, ids)
        m[:y0] = m[y1:] = False
        m[:, :x0] = m[:, x1:] = False
        rgb = A_[y:y + ch, x:x + cw].astype(np.uint8)
        mm = m[y:y + ch, x:x + cw]
        al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
        vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
        sang = rgb.min(2).astype(np.float32)
        al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
        im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
        goc = Image.open(os.path.join(MANH2, r + ".png")).convert("RGBA")
        tw, th = goc.size
        im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        a2 = np.asarray(im2).copy()
        ag = np.asarray(goc)[..., 3] > 60
        gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
        a2[..., 3] = np.where(gioi, a2[..., 3], 0)
        thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)
        if thieu.any() and (a2[..., 3] >= 128).any():
            co = (a2[..., 3] >= 128).astype(np.uint8)
            _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys_, xs_ = np.nonzero(co)
            bang = np.zeros((lbl.max() + 1, 3), np.uint8)
            bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
            a2[thieu, :3] = bang[lbl[thieu]]
            a2[thieu, 3] = 255
        Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
        b = fgG[y:y + ch, x:x + cw]
        iou = float((mm & b).sum()) / max(1, (mm | b).sum())
        ious[r] = round(iou, 3)
        so.append(Image.fromarray(a2, "RGBA"))
        print(f"  {r:14s} IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, f"_so_{ten}.png"))


# ================================================================ N: mảnh đổi dáng gen đúng chỗ, đúng cỡ trên concept A
# (tên, hộp gán px concept, slot của dạng 2 nó thay (None = mảnh mới), xương bám, tả tiếng Anh)
NTO = {
    "N1": [("mat", (600, 380, 960, 600), "bizi", "xiabanshen_04",
            "the HEAD of the young robot prince WITHOUT the crown: the round grey head with the two big round yellow eyes, the brows, the "
            "small nose, the mouth line and the round ear disc on its left side, complete as ONE closed rounded head shape (the top of the "
            "head hidden under the crown is drawn too, plain grey; its bottom edge round, as in image 1)"),
           ("canh_tren_gan_lien", (0, 0, 600, 470), None, "cw_tren_gan_tay",
            "the UPPER LEFT wing: its grey wing arm with the two gold joints and all its white feathers with gold tips, complete as ONE "
            "piece (the part of the arm hidden behind other things drawn too)"),
           ("canh_tren_xa_lien", (960, 0, 1536, 470), None, "cw_tren_xa_tay",
            "the UPPER RIGHT wing: the same, complete as ONE piece"),
           ("canh_duoi_gan_lien", (0, 470, 600, 800), None, "cw_duoi_gan_tay",
            "the LOWER LEFT wing: the same, complete as ONE piece (its root hidden behind the cape drawn too)"),
           ("canh_duoi_xa_lien", (960, 470, 1536, 800), None, "cw_duoi_xa_tay",
            "the LOWER RIGHT wing: the same, complete as ONE piece (its root hidden behind the arm drawn too)")],
    "N2": [("vuong_mien", (560, 250, 1000, 470), "touguan", "touguan",
            "the low gold PRINCE CROWN with its three small points topped by small gold balls and its red jewel in front, complete as ONE "
            "closed shape (its back rim and the parts hidden behind other things drawn too)")],
    "N3": [("hao_quang", (450, 150, 1100, 620), None, "hao_quang",
            "the thin round gold HALO RING with its small pearls, complete as a FULL CIRCLE (the parts of the ring hidden behind the crown, "
            "the head and the body are drawn too, with pearls spaced evenly all the way round)")],
}
VI_N = {"N1": "đầu (không vương miện) + bốn cánh liền", "N2": "vương miện hoàng tử", "N3": "vòng hào quang đủ vòng"}


def prompt_n():
    ps = []
    for ma, ds in NTO.items():
        out = os.path.join(TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: {MO_TA_CON}.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} piece{'s' if len(ds) > 1 else ''} listed below, each in the SAME POSITION, at "
             "the SAME SIZE and with the SAME colours as in image 1 (if your picture were laid over image 1, every piece must sit exactly "
             "on its old place). REMOVE everything else (the body, the other parts, everything not listed) and leave pure white there. "
             "COMPLETE every piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were hidden "
             "behind other things in image 1 are drawn too, continuing its shape naturally." +
             (" The pieces stay separate from each other (leave a little white gap between them, do not merge them)." if len(ds) > 1
              else ""), "", "THE PIECE" + ("S:" if len(ds) > 1 else ":")]
        t += [f"{i}. {mt}." for i, (_, _, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, "
              "no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p))
        print(p)
    return ps


def cat_n(ma):
    """tờ M_<ma>: mỗi cụm liền về mảnh có hộp gán chứa tâm cụm; ảnh 1 px / đơn vị dạng 1; moi.json ghi 4 góc ở KHUNG DẠNG 2 (đổi qua xương
    bám) để sau khi đổi tỉ lệ xương mảnh về đúng chỗ trên concept."""
    c2w, w2c, upc = phep_can()
    path = moi_nhat(TAI, f"M_{ma}")
    if not path:
        print(f"{ma}: chưa gen")
        return []
    print(f"{ma}:", os.path.basename(path))
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj))
    rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
    fg = (~nen_trang(rgb.astype(np.int32))).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg, 8)
    ds = NTO[ma]
    gan = {d[0]: [] for d in ds}
    for i in range(1, n):
        if st[i, 4] < 150:
            continue
        cx, cy = cen[i]
        ung = [d for d in ds if d[1][0] <= cx < d[1][2] and d[1][1] <= cy < d[1][3]]
        if not ung:
            print(f"  cụm {i} tâm ({cx:.0f},{cy:.0f}) {st[i, 4]} px: không thuộc mảnh nào, bỏ")
            continue
        gan[min(ung, key=lambda d: np.hypot(cx - (d[1][0] + d[1][2]) / 2, cy - (d[1][1] + d[1][3]) / 2))[0]].append(i)
    so = []
    for ten, hop, sl, bn, _ in ds:
        if not gan[ten]:
            print(f"  {ten}: KHÔNG thấy mảnh")
            continue
        mm0 = np.isin(lab, gan[ten])
        mm0 = cv2.morphologyEx(mm0.astype(np.uint8), cv2.MORPH_CLOSE, el(2)).astype(bool)
        if ten == "hao_quang":                                   # lòng vòng: giấy trắng khép kín lớn → trong suốt
            n2, l2, s2, _ = cv2.connectedComponentsWithStats((rgb.min(2) > 236).astype(np.uint8), 4)
            for j in range(1, n2):
                if s2[j, 4] > 2000:
                    mm0 &= ~(l2 == j)
        ys, xs = np.nonzero(mm0)
        pad = 4
        x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W - 1, xs.max() + pad), min(H - 1, ys.max() + pad)
        mm = mm0[y0:y1 + 1, x0:x1 + 1]
        al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
        rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], (al * 255).astype(np.uint8)])
        out = Image.fromarray(rgba, "RGBA").convert("RGBa")
        k = upc                                                  # px concept → 1 px / đơn vị dạng 1
        out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
        out.save(os.path.join(MANH, ten + ".png"))
        hop4 = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
        w1 = c2w(hop4)
        w2 = d1_ve_d2(w1, bn)
        e = w2[1] - w2[0]
        quay = float(np.degrees(np.arctan2(e[1], e[0])))
        moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=w2.tolist(), to=ma,
                        the_gioi_d1=w1.tolist())
        so.append(out)
        print(f"  {ten:20s} hộp {x0},{y0}–{x1},{y1} → {ten}.png {out.size}  (thay {sl}, xương {bn}; khung dạng 2 xoay {quay:+.2f}°, "
              f"rộng {np.linalg.norm(e):.0f} / {np.linalg.norm(w1[1] - w1[0]):.0f})")
    json.dump(moi, open(pj, "w"), indent=1)
    if so:
        _to_so(so, os.path.join(MANH, f"_so_{ma}.png"))
    return so


# ================================================================ chép mảnh dạng 2 dùng lại
BO_MOI = ("rau", "vuong_mien", "mat", "hao_quang")


def chep():
    os.makedirs(MANH, exist_ok=True)
    n = 0
    for f in os.listdir(MANH2):
        if f.endswith(".png") and not f.startswith("_") and not os.path.exists(os.path.join(MANH, f)):
            shutil.copy2(os.path.join(MANH2, f), os.path.join(MANH, f))
            n += 1
    moi = json.load(open(os.path.join(MANH2, "moi.json")))
    pj = os.path.join(MANH, "moi.json")
    cu = json.load(open(pj)) if os.path.exists(pj) else {}
    for k in BO_MOI:
        moi.pop(k, None)
    for k, v in cu.items():                                      # mảnh dạng 1 đã cắt (tờ N) giữ lại
        if isinstance(v, dict) and str(v.get("to", "")).startswith("N"):
            moi[k] = v
    json.dump(moi, open(pj, "w"), indent=1)
    for k in ("rau",):
        p = os.path.join(MANH, k + ".png")
        if os.path.exists(p):
            os.remove(p)
    print(f"chép {n} mảnh dạng 2 → {MANH}; moi.json {len(moi)} mục (bỏ {', '.join(BO_MOI)})")


def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh theo concept A đã duyệt (2026-11-17)", "",
          "Claude tự gen và tự cắt; người dùng không cần làm gì.", ""]
    for ten, p, vi in ps:
        gd += [f"- **{ten}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`."]
    gd += ["", "Cắt: `py -3 -I ArtGen/Spine/vua_may_non_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    ps = []
    for ten in TO_K:
        ps.append((ten, prompt_k(ten, to_k(ten)), VI_K[ten]))
    for ma, p in prompt_n():
        ps.append((ma, p, VI_N[ma]))
    huong_dan(ps)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "kiem_map":
        kiem_map()
    elif cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "chep":
        chep()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ten in TO_K:
            if chi in ("", "K", ten):
                cat_k(ten)
        for ma in NTO:
            if chi in ("", "N", ma):
                cat_n(ma)
    else:
        print(__doc__)
