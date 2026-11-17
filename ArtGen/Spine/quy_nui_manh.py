# -*- coding: utf-8 -*-
"""Vượn núi đá bốn tay (quy_nui, tướng 5 đảo Thổ, rig monster_3612): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png
= hướng C, người dùng chọn 2026-11-17: vượn núi bằng đá bốn tay, mặt khỉ đột hai mắt hổ phách, vương miện ba gai đá, thân tảng đá tròn hoa
cương, mạch pha lê hổ phách chéo ngực, nắm đấm to, tay phụ vuốt đá, khố da). Concept TO HƠN rig ~17 % (vai, nắm đấm): căn bằng phép co
k + dời (mau/can.json, tìm theo IoU hình bóng với con gốc) rồi mỗi mảnh đặt theo chỗ của nó trên concept đã căn và gắn vào NHÓM lưới gốc
tương ứng (quy_nui_rig.py: gan_goc trên lưới gộp của các slot gốc).

Mảnh (bên = theo NGƯỜI XEM: _R là nửa trái tranh = slot *R* của họ, _L là nửa phải = slot *L*):
    than               thân (ngực, bụng, mạch hổ phách)            Q1   ← shenti2, bozi1, bozi2, xiongjia1, xiongjia2, shenti3
    dau                đầu vượn + vương miện gai                   Q2   ← tou
    dam_R / dam_L      nắm đấm trước trái / phải                    Q2   ← shouR3_1 / shouL3_1
    kho                khố da                                      Q2   ← weiqun
    vai_R / vai_L      tảng vai trước                              Q3   ← shouR1_2 + shouR1_1 / shouL1_2 + shouL1_1
    chan_R / chan_L    chân ngắn                                   Q3   ← tuiR1..3 / tuiL1..3
    canh_R / canh_L    cẳng tay trước                              Q4   ← shouR2 + shouR3_2 / shouL2 + shouL3_2 + shouL1_3
    tren_R / tren_L    bắp tay phụ (sau lưng, giơ lên)             Q4   ← jixieshouR1 / jixieshouL1
    duoi_R / duoi_L    cẳng tay phụ + lòng bàn tay                 Q5   ← jixieshouR2 / jixieshouL2
    ngon_R1..3 / ngon_L1..3  ngón vuốt tay phụ (trên → dưới)       Q6   ← shouzhiR1_* .. R3_* / shouzhiL1_* .. L3_*
    BỎ: đuôi weiba1/2 + jiapian (vượn không đuôi), bốn dải piaodai* (concept chỉ có khố trơn).

    quy_nui_manh.py can          căn concept lên hình con gốc (co + dời, IoU) → mau/can.json
    quy_nui_manh.py prompt       file prompt từng nhóm → gui_gpt/quy_nui_1/luot_2_<nhóm>.txt (+ nối HUONG_DAN.md)
    quy_nui_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    quy_nui_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402

G = tho5.dat("quy_nui")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "quy_nui_1")

# tâm dự kiến (px concept) của từng mảnh, để gán cụm cắt ra cho đúng tên
TAM = {"than": (790, 540), "dau": (845, 290), "dam_R": (400, 885), "dam_L": (1150, 885), "kho": (735, 800),
       "vai_R": (455, 480), "vai_L": (1095, 480), "chan_R": (585, 815), "chan_L": (895, 815),
       "canh_R": (385, 690), "canh_L": (1150, 690), "tren_R": (570, 200), "tren_L": (985, 195),
       "duoi_R": (360, 225), "duoi_L": (1185, 215)}

NHOM = {
    "Q1": [("than", "the TORSO: the big rounded rock chest and belly made of granite boulders, with the diagonal vein of flat amber crystals "
            "across it",
            "draw it as ONE complete rounded stone torso: the parts hidden behind the head, the two big shoulder boulders, the arms, the "
            "legs and the loincloth continue as the same granite boulders (its top reaches up behind the head to the neck, its sides "
            "continue under the shoulders, its bottom is a rounded stone belly/hip just above where the legs and the loincloth start); the "
            "amber vein continues straight across under the head. NO head, NO shoulders, NO arms, NO legs, NO loincloth")],
    "Q2": [("dau", "the HEAD: the broad ape face with the heavy brow, the two amber eyes, the wide nose, the jaw with the two upward tusks, "
            "and the crown of three jagged rock spikes on top", "complete its back and bottom (hidden by nothing) as a rounded rock head; "
            "keep the face exactly"),
           ("dam_R", "the huge front FIST at the lower LEFT (with its big knuckles)", "complete its top, hidden under the forearm, as a "
            "rounded wrist boulder"),
           ("dam_L", "the huge front FIST at the lower RIGHT (with its big knuckles)", "complete its top, hidden under the forearm, as a "
            "rounded wrist boulder"),
           ("kho", "the brown hide LOINCLOTH hanging between the legs", "complete its top, hidden behind the stone belly, as a straight "
            "waist edge")],
    "Q3": [("vai_R", "the big front SHOULDER boulder on the LEFT (the upper arm of the left front arm)", "complete it into ONE closed "
            "rounded boulder: the parts hidden by the forearm below it and by the back arm behind it continue as the same stone"),
           ("vai_L", "the big front SHOULDER boulder on the RIGHT (the upper arm of the right front arm)", "complete it into ONE closed "
            "rounded boulder: the parts hidden by the forearm below it and by the back arm behind it continue as the same stone"),
           ("chan_R", "the short LEFT LEG (between the left fist and the loincloth) with its foot", "complete its top, hidden under the "
            "belly, as a rounded thigh"),
           ("chan_L", "the short RIGHT LEG (between the loincloth and the right fist) with its foot", "complete its top, hidden under the "
            "belly, as a rounded thigh")],
    "Q4": [("canh_R", "the front FOREARM boulders of the LEFT front arm (between the left shoulder and the left fist)", "complete it into "
            "one closed shape: its top under the shoulder and its bottom inside the fist continue as the same stone"),
           ("canh_L", "the front FOREARM boulders of the RIGHT front arm (between the right shoulder and the right fist)", "complete it into "
            "one closed shape: its top under the shoulder and its bottom inside the fist continue as the same stone"),
           ("tren_R", "the UPPER ARM boulder of the LEFT BACK ARM (the raised arm rising from behind the left shoulder, at the top left of "
            "the head)", "complete its root, hidden behind the shoulder, as a rounded end"),
           ("tren_L", "the UPPER ARM boulder of the RIGHT BACK ARM (the raised arm rising from behind the right shoulder, at the top right "
            "of the head)", "complete its root, hidden behind the shoulder, as a rounded end")],
    "Q5": [("duoi_R", "the FOREARM and the PALM of the LEFT BACK ARM (going down to the left to the dark claw), WITHOUT the fingers",
            "complete its elbow end, hidden behind the upper arm, as a rounded end; the palm ends as a rounded dark-brown back of the hand "
            "where the fingers would start (do not draw the fingers)"),
           ("duoi_L", "the FOREARM and the PALM of the RIGHT BACK ARM (going down to the right to the dark claw), WITHOUT the fingers",
            "complete its elbow end, hidden behind the upper arm, as a rounded end; the palm ends as a rounded dark-brown back of the hand "
            "where the fingers would start (do not draw the fingers)")],
    "Q6": [("ngon", "the curved dark-brown FINGERS of the two back claws (three or four separate fingers on each claw, each a thick curved "
            "stone claw finger)", "draw EACH finger as its own closed shape with a short rounded base where it joins the palm (the palm "
            "itself is NOT drawn), keep a thin white gap between neighbouring fingers")],
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a huge four-armed MOUNTAIN APE made of rock, seen from the "
        "front, leaning on two huge stone fists: a broad ape face with two small amber eyes, a wide nose and two upward tusks, a crown of "
        "three jagged rock spikes; a body of big rounded granite boulders with a diagonal vein of amber crystals across the chest; two "
        "back arms raised at the top with dark three-fingered stone claws; short legs and a brown hide loincloth. Hand-drawn: wobbly "
        "dark-brown ink line, crayon hatching, flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


# ---------------------------------------------------------------- căn concept lên con gốc
def _mask(p):
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H)), np.int16)
    m = ((255 - a).max(2) > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k


def can():
    """phép co k + dời (tx, ty): px concept → px khung ca_con của con gốc; tìm k, dời quanh neo (tâm ngang + đáy) theo IoU hình bóng."""
    g, c = _mask(os.path.join(G.MAU, "goc_ca_con.png")), _mask(CONCEPT)
    ys, xs = np.nonzero(g)
    ys2, xs2 = np.nonzero(c)
    S = 4
    gs = cv2.resize(g, (W // S, H // S), interpolation=cv2.INTER_AREA) > 0
    best = None
    for k in np.arange(0.78, 1.0, 0.005):
        for dy in range(-60, 61, 4):
            for dx in range(-40, 41, 4):
                tx = (xs.min() + xs.max()) / 2 - k * (xs2.min() + xs2.max()) / 2 + dx
                ty = ys.max() - k * ys2.max() + dy
                w = cv2.warpAffine(c, np.float32([[k / S, 0, tx / S], [0, k / S, ty / S]]), (W // S, H // S)) > 0
                iou = (w & gs).sum() / max(1, (w | gs).sum())
                if best is None or iou > best[0]:
                    best = (float(iou), float(k), float(tx), float(ty))
    json.dump(dict(iou=best[0], k=best[1], tx=best[2], ty=best[3]), open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print("can", best)


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-17; người dùng chọn C = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): vượn núi đá bốn tay mặt khỉ đột, vương miện "
          "gai đá, mạch pha lê hổ phách chéo ngực, nắm đấm to, tay phụ vuốt đá, khố da. Mỗi nhóm chỉ giữ vài mảnh không chồng nhau, đúng chỗ, "
          "đúng cỡ, vẽ đủ phần bị che.", ""]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap between the "
             "kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `quy_nui_manh.py ghep`); phần bị che vẽ đủ, viền kín; nền "
           "trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
def nen(A):
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H:
            bg |= lab == i
    return bg


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def khu_vien(rgb, mm, r=2):
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def luu_manh(A, m, ten, DATJ, nguon):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=nguon)
    return x0, y0, x1, y1


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd)) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    os.makedirs(MANH, exist_ok=True)
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w"), indent=1)


def _cum(src, min_px=40):
    A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = ~nen(A)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    return A, lab, [(i, int(st[i, 4]), (float(cen[i][0]), float(cen[i][1])), st[i]) for i in range(1, n) if st[i, 4] > min_px]


def cat(chi=None):
    DATJ = nap_dat()
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A, lab, cum = _cum(src)
        print(f"{nh} ({os.path.basename(src)}): {len(cum)} cụm")
        if nh == "Q6":                                         # ngón: mỗi cụm đủ lớn là một ngón; chia trái / phải tranh, xếp trên → dưới
            lon = [c for c in cum if c[1] > 600]
            vun = [c for c in cum if c[1] <= 600]
            for ben, chon in (("R", [c for c in lon if c[2][0] < W / 2]), ("L", [c for c in lon if c[2][0] >= W / 2])):
                chon.sort(key=lambda c: c[2][1])
                for k, c in enumerate(chon, 1):
                    ids = [c[0]] + [v[0] for v in vun if np.hypot(v[2][0] - c[2][0], v[2][1] - c[2][1]) < 40]
                    ten = f"ngon_{ben}{k}"
                    b = luu_manh(A, np.isin(lab, ids), ten, DATJ, os.path.basename(src))
                    print(f"  {ten:9s} hộp {b}, {c[1]} px")
            continue
        slots = [s for s, _, _ in ds]
        gan = {s: [] for s in slots}
        for i, a, c, _ in cum:
            best = min(slots, key=lambda s: np.hypot(c[0] - TAM[s][0], c[1] - TAM[s][1]))
            d = np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1])
            if d < 300 or a > 20000:
                gan[best].append(i)
            else:
                print(f"  bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {a} px")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:9s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            print(f"  {s:9s} hộp {b}, {len(ids)} cụm")
    ghi_dat(DATJ)


def cat_canh(vao=22, sau=0.45, day_vien=6):
    """cẳng tay trước GPT vẽ bù dài xuống tận đất (chồng chỗ nắm đấm; bám xương cẳng nên lòi ra khi cổ tay xoay). Cho cẳng tay một ĐẦU
    TRÒN KHÉP KÍN ngay dưới mép trên nắm đấm: giữ phần trên đường ngang y_top + vao (y_top = mép trên nắm đấm ở cột giữa) cộng nửa elip
    phồng xuống (bán trục ngang = nửa bề ngang cẳng tay ở đường đó, sâu = sau × bán trục), rồi KẺ VIỀN MỰC dọc mép mới (màu mực lấy từ
    chính mảnh). Lộ ra khi cổ tay xoay thì là đầu tảng đá tròn một đường viền, không mép cắt, không quạt mờ (người dùng chê ở tatu)."""
    DATJ = nap_dat()
    for c, d in (("canh_R", "dam_R"), ("canh_L", "dam_L")):
        if c not in DATJ or d not in DATJ:
            continue
        x0, y0, x1, y1 = DATJ[c]["hop"]
        im = np.asarray(Image.open(os.path.join(MANH, c + ".png")).convert("RGBA")).copy()
        M = im[..., 3] > 128
        dm = np.asarray(Image.open(os.path.join(MANH, d + ".png")).convert("RGBA"))[..., 3] > 128
        dx0, dy0 = DATJ[d]["hop"][:2]
        y_top = dy0 + int(np.argmax(dm[:, dm.shape[1] // 2]))
        yl = int(y_top + vao - y0)                                       # đường cắt (px mảnh)
        yl = max(10, min(im.shape[0] - 2, yl))
        xs = np.nonzero(M[yl])[0]
        if len(xs) < 4:
            continue
        xa, xb = xs.min(), xs.max()
        xc, hw = (xa + xb) / 2.0, (xb - xa) / 2.0
        dd = sau * hw
        Y, X = np.mgrid[0:im.shape[0], 0:im.shape[1]]
        elip = ((X - xc) / max(1.0, hw)) ** 2 + ((Y - yl) / max(1.0, dd)) ** 2 <= 1.0
        M2 = M & ((Y < yl) | elip)
        # mực: màu tối nhất phổ biến trong mảnh
        rgb = im[..., :3].astype(int)
        lum = rgb.mean(2)
        muc = np.median(rgb[M & (lum < np.percentile(lum[M], 6))], axis=0).astype(np.uint8)
        dist = cv2.distanceTransform(M2.astype(np.uint8), cv2.DIST_L2, 5)
        moi = M2 & (Y >= yl - 2) & (dist <= day_vien)                    # chỉ kẻ dọc phần mép MỚI (phía dưới đường cắt)
        out = im.copy()
        out[moi, :3] = muc
        a = np.where(M2, im[..., 3], 0).astype(np.float32)
        a = cv2.GaussianBlur((M2 * 255).astype(np.float32), (0, 0), 0.7) * (a > 0) + (a == 0) * 0
        out[..., 3] = np.clip(np.where(M2, np.maximum(a, 0), 0), 0, 255).astype(np.uint8)
        out[..., 3] = np.where(M2, np.maximum(out[..., 3], (im[..., 3] * (dist > 1.5)).astype(np.uint8)), 0)
        Image.fromarray(out, "RGBA").save(os.path.join(MANH, c + ".png"))
        print(c, f"đầu tròn khép kín dưới mép trên {d} + {vao} px, sâu {dd:.0f} px, viền {day_vien} px")


THU_TU = (["ngon_L1", "ngon_L2", "ngon_L3", "duoi_L", "tren_L"] + ["ngon_R1", "ngon_R2", "ngon_R3", "duoi_R", "tren_R"] +
          ["vai_L", "canh_L", "dam_L", "chan_L", "chan_R", "kho", "than", "vai_R", "canh_R", "dau", "dam_R"])


def ghep():
    DATJ = nap_dat()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in THU_TU:
        if s not in DATJ:
            thieu.append(s)
            continue
        x0, y0, _, _ = DATJ[s]["hop"]
        can_.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can_.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can_.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    print(p, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "cat_canh":
        cat_canh()
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
