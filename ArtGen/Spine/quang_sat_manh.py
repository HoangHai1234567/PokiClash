# -*- coding: utf-8 -*-
"""Tinh linh quặng sắt (quang_sat): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png = L1_C, người dùng chọn
2026-11-16: vỏ đá xám lam, dải mặt tối, mắt xanh lơ, năm tinh thể bát diện sắt đen gờ bạc). Concept vẽ đúng khung hình cả con gốc ở khung 0
idle (mau/goc_ca_con.json: tỉ lệ s px / đơn vị, tâm cx, cy), nên mỗi mảnh cắt ra đặt thẳng vào thế giới rig ở dáng idle 0.

Mảnh (tên ảnh = tên vùng atlas của họ để rig tra theo slot):
    longdan_9  thân (vỏ đá + dải mặt tối, KHÔNG mắt)          M1
    longdan_4 / 3 / 2  tinh thể trên đầu giữa / trái / phải   M2
    longdan_1 / 0  tay trái (dài) / tay phải                  M2
    longdan_7 / 8  mắt mở trái / phải                         cắt thẳng từ concept (vùng xanh lơ + vành mực)
    longdan_5 / 6  mắt nhắm `>` / `<`                          F2
    ngu_t / ngu_p  mắt ngủ (cung cong) trái / phải            F3 (appear)
    go_dat, ho     gò đất chạy ngầm, hố đất (chiêu cuối)      D1 (đặt riêng, không theo chỗ concept)

    quang_sat_manh.py khung        viền mọi part gốc (khung 0 idle) chồng lên concept → mau/_goc_tren_concept.png
    quang_sat_manh.py prompt       file prompt từng nhóm → gui_gpt/quang_sat_1/luot_2_<nhóm>.txt (+ nối HUONG_DAN.md)
    quang_sat_manh.py mat          cắt hai mắt mở thẳng từ concept → manh/longdan_7.png, longdan_8.png
    quang_sat_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    quang_sat_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quang_sat as G  # noqa: E402
import quang_sat_da as DA  # noqa: E402

W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = DA.GUI
MUC = "#2B2118"

# nhóm gen: các mảnh trong một nhóm KHÔNG chồng nhau trên concept. Mỗi mảnh: (tên ảnh, mô tả tiếng Anh, cách vẽ phần khuất)
NHOM = {
    "M1": [("longdan_9", "the round stone SHELL (the whole body) with its dark face band and the two small silver studs",
            "the parts of the shell covered by the five black crystals must be drawn: a complete smooth round dome with its full outline "
            "(the top of the dome under the big crystal, the upper left and upper right edges under the side crystals, the lower left edge "
            "under the long left crystal, the lower right edge under the right crystal), plain blue-grey stone with the same three small "
            "dark speckles and the same two thin seam lines; the dark face band keeps exactly its shape (V dip on top, wavy zigzag bottom) "
            "but WITHOUT the two eyes: where the eyes were, the band is plain flat dark charcoal like the rest of the band")],
    "M2": [("longdan_4", "the BIG black crystal standing on top of the head (the tallest)",
            "complete it into ONE closed double-pointed octahedron: its lower tip ends where it meets the shell, as in image 1"),
           ("longdan_3", "the black crystal on the upper LEFT of the head", "complete it into one closed shape"),
           ("longdan_2", "the small black crystal on the upper RIGHT of the head", "complete it into one closed shape"),
           ("longdan_1", "the LONG black crystal floating at the lower LEFT (a hand)", "complete it into one closed double-pointed shape"),
           ("longdan_0", "the black crystal floating at the lower RIGHT (a hand)", "complete it into one closed double-pointed shape")],
}
# hình mắt phụ: vẽ đúng chỗ hai mắt của concept (chỉ hai dấu, nền trắng)
PHU = {
    "F2": (("longdan_5", "longdan_6"),
           "the two eyes TIGHTLY CLOSED (squeezed shut): the LEFT eye becomes a bold '>' mark and the RIGHT eye a bold '<' mark, each mark "
           "a thick stroke in flat bright cyan #5FD8EE with a thin dark-brown ink outline, each in the same place and about the same size "
           "as the eye it replaces (the '>' about 70 px wide and 80 px tall, the '<' a little smaller)"),
    "F3": (("ngu_t", "ngu_p"),
           "the two eyes CALMLY CLOSED, ASLEEP: each eye becomes a short gently curved arc that bows DOWNWARD (like a relaxed sleeping eye "
           "'u'), a thick stroke in flat bright cyan #5FD8EE with a thin dark-brown ink outline, about as wide as the eye it replaces "
           "(about 70 px for the left, 60 px for the right) and centred a little below the middle of that eye"),
}
DAT = {
    "D1": (("go_dat", "ho"),
           ["a DIRT MOUND, alone in the UPPER half of the canvas (centre about x = 768, y = 260): a long low rounded hump of loose brown "
            "earth pushed up from below by something digging underneath, about 620 px wide and 200 px tall, its bottom edge a flat "
            "horizontal ground line; flat earth brown #8B6542 with the side turned away darker #6E4E33, three short dark cracks on its top, "
            "four or five small round clods and two little pebbles sitting on it. Nothing comes out of it.",
            "a HOLE in the ground, alone in the LOWER half of the canvas (centre about x = 768, y = 760), seen from a low three-quarter "
            "view: a wide flat ELLIPSE opening about 640 px wide and 150 px tall, its inside ONE flat very dark brown #2A1E16 (no detail "
            "inside), surrounded by a ring of loose brown earth #8B6542 piled up round the rim, the ring thicker and higher at the FRONT "
            "(bottom) edge (about 60 px) than at the back (about 30 px), with a few small clods on the ring."]),
}
TEN_DAT = {"go_dat": "the dirt mound", "ho": "the hole"}


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def khu_vien(rgb, mm, r=2):
    """dải mép r px của mảnh lấy màu TỐI NHẤT quanh nó (điểm khử răng cưa pha giấy trắng để lại viền sáng quanh mảnh sẫm)."""
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    to_px = lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
    to_rig = lambda P: np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    return s, to_px, to_rig


def hop_goc():
    """hộp (concept px) của từng part gốc ở khung 0 idle, theo tên vùng (region)."""
    _, imgs, atts = G.nap("att_idle0.json")
    _, to_px, _ = tf()
    out = {}
    for a in atts:
        P = to_px(np.array(a["xy"], float).reshape(-1, 2))
        out[a["region"]] = [float(P[:, 0].min()), float(P[:, 1].min()), float(P[:, 0].max()), float(P[:, 1].max())]
    out["longdan_5"], out["longdan_6"] = out["longdan_7"], out["longdan_8"]      # mắt nhắm: chỗ mắt mở
    out["ngu_t"], out["ngu_p"] = out["longdan_7"], out["longdan_8"]
    return out


def khung():
    im = Image.open(CONCEPT).convert("RGB")
    d = ImageDraw.Draw(im)
    _, imgs, atts = G.nap("att_idle0.json")
    _, to_px, _ = tf()
    for a in atts:
        P = to_px(np.array(a["xy"], float).reshape(-1, 2))
        h = cv2.convexHull(P.astype(np.float32)).reshape(-1, 2)
        d.line([tuple(p) for p in h] + [tuple(h[0])], fill=(230, 40, 40), width=2)
        c = P.mean(0)
        d.text((c[0] - 10, c[1] - 6), a["region"], fill=(200, 0, 0))
    p = os.path.join(G.MAU, "_goc_tren_concept.png")
    im.save(p)
    print(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a chubby round blue-grey STONE dome spirit with a dark face "
        "band and two upright cyan oval eyes, two small silver studs above the band, three black-iron double-pointed octahedron crystals "
        "with silver ridge lines standing on its head (a big one in the middle, a smaller one on each side) and two floating black "
        "crystals as its hands (a long one at the lower left, a shorter one at the lower right). Hand-drawn: wobbly dark-brown ink line, "
        "crayon hatching, flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-16; người dùng chọn C = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): vỏ đá xám lam, dải mặt tối, hai mắt "
          "bầu dục xanh lơ, ba tinh thể bát diện sắt đen trên đầu + hai tinh thể làm tay. M1, M2 chỉ giữ vài mảnh, đúng chỗ, đúng cỡ, vẽ đủ "
          "phần bị che; F2, F3 vẽ mắt nhắm, mắt ngủ đúng chỗ hai mắt; D1 vẽ gò đất và hố đất cùng nét (cho chiêu cuối).", ""]
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
    for nh, (ten, mt) in PHU.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: draw ONLY the character's two eyes, in exactly the SAME POSITION and at the SAME SIZE as in image 1, but CHANGED as "
             f"follows: {mt}. REMOVE everything else (the shell, the dark face band, the studs, the crystals: pure white): only the two eye "
             "marks on white. " + STYLE, "", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(ten)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    for nh, (ten, ds) in DAT.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: {ANH1} Use it ONLY for the drawing style; do NOT draw the character.", ""] + save + ["",
             "TASK: draw TWO separate props for a battle effect of this character, in exactly the hand-drawn style of image 1 (wobbly dark-"
             "brown ink outline about 7 px all the way round each prop, flat colours with visible coloured-pencil / wax-crayon hatching, no "
             "shading, no highlights, no shadows, no glow). VERY SIMPLE, FEW DETAILS. Keep a wide white gap between the two props.", ""]
        t += [f"{i}. {d}" for i, d in enumerate(ds, 1)]
        t += ["", "Do not draw the character, no grass, no plants, no sky, no ground plane outside the props.",
              "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no frame."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(ten)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `quang_sat_manh.py ghep`); phần bị che vẽ đủ, viền kín; thân "
           "không còn mắt; mắt nhắm / ngủ màu xanh lơ (dải mặt tối đen, nét đen sẽ không thấy); nền trắng tinh."]
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


def luu_manh(A, m, ten, DATJ, nguon):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8)
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=nguon)
    return x0, y0, x1, y1


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd)) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w"), indent=1)


def mat():
    """hai mắt mở cắt thẳng từ concept: vùng xanh lơ trong hộp mắt gốc (nới 24 px), lấp lỗ (chấm sáng), nới 5 px lấy vành mực."""
    os.makedirs(MANH, exist_ok=True)
    DATJ = nap_dat()
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    HG = hop_goc()
    for ten in ("longdan_7", "longdan_8"):
        x0, y0, x1, y1 = [int(round(v)) for v in HG[ten]]
        x0, y0, x1, y1 = x0 - 24, y0 - 24, x1 + 24, y1 + 24
        sub = A[y0:y1, x0:x1]
        xanh = (sub[..., 2] > 170) & (sub[..., 1] > 150) & (sub[..., 0] < 170)
        n, lab, st, _ = cv2.connectedComponentsWithStats(xanh.astype(np.uint8), 8)
        k = 1 + int(np.argmax(st[1:, 4]))
        m = (lab == k).astype(np.uint8)
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        m = cv2.drawContours(np.zeros_like(m), cs, -1, 1, -1)              # lấp chấm sáng trắng bên trong
        m = cv2.dilate(m, el(5)).astype(bool)
        full = np.zeros((H, W), bool)
        full[y0:y1, x0:x1] = m
        b = luu_manh(A, full, ten, DATJ, "L1_duyet.png (cắt thẳng)")
        print(ten, "hộp", b, "| mắt gốc", [round(v) for v in HG[ten]])
    ghi_dat(DATJ)


def cat(chi=None):
    os.makedirs(MANH, exist_ok=True)
    DATJ = nap_dat()
    HG = hop_goc()
    viec = {nh: [s for s, _, _ in ds] for nh, ds in NHOM.items()}
    viec.update({nh: list(ten) for nh, (ten, _) in PHU.items()})
    for nh, slots in viec.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = [i for i in range(1, n) if st[i, 4] > 30]
        gan = {s: [] for s in slots}
        for i in cum:
            x, y, w, h, a = st[i]
            c = (x + w / 2, y + h / 2)
            best, bd = None, 1e9
            for s in slots:
                hb = HG[s]
                cx_, cy_ = (hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2
                dx = max(hb[0] - c[0], 0, c[0] - hb[2])
                dy = max(hb[1] - c[1], 0, c[1] - hb[3])
                dd = np.hypot(dx, dy) + 0.15 * np.hypot(c[0] - cx_, c[1] - cy_)
                if dd < bd:
                    best, bd = s, dd
            if bd < 160:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {a} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:10s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            hb = HG[s]
            print(f"  {s:10s} hộp {b} | part gốc ({hb[0]:.0f}, {hb[1]:.0f}, {hb[2]:.0f}, {hb[3]:.0f}), {len(ids)} cụm")
    # đạo cụ đất: mỗi đạo cụ là cụm lớn nhất ở nửa trên (gò) / nửa dưới (hố) của tờ
    for nh, (ten, _) in DAT.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        print(f"{nh} ({os.path.basename(src)}):")
        for s, tren in zip(ten, (True, False)):
            ids = [i for i in range(1, n) if st[i, 4] > 30 and ((cen[i][1] < H / 2) == tren)]
            if not ids:
                print(f"  {s:10s} KHÔNG THẤY")
                continue
            lon = max(ids, key=lambda i: st[i, 4])
            x, y, w, h, _ = st[lon]
            ids = [i for i in ids if x - 40 <= cen[i][0] <= x + w + 40 and y - 40 <= cen[i][1] <= y + h + 40]   # cục đất rời sát bên
            b = luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            print(f"  {s:10s} hộp {b}, {len(ids)} cụm")
    ghi_dat(DATJ)


THU_TU = ["longdan_0", "longdan_9", "longdan_8", "longdan_7", "longdan_4", "longdan_3", "longdan_2", "longdan_1"]


def ghep():
    """ghép mảnh theo thứ tự vẽ idle của rig (mắt mở) lên nền trắng; đặt cạnh concept; IoU hình bóng."""
    DATJ = nap_dat()
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in THU_TU:
        if s not in DATJ:
            thieu.append(s)
            continue
        x0, y0, _, _ = DATJ[s]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    print(p, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


def goc():
    """bộ mảnh TẠM bằng da gốc (chỉ để chạy thử rig trong máy khi chưa có mảnh của mình): mỗi part của họ vẽ đúng chỗ khung 0 idle
    trên khung concept → manh_goc/<tên>.png + dat.json; mắt nhắm lấy hình phụ của họ (dáng gốc); mắt ngủ = mắt nhắm; gò, hố vẽ phẳng."""
    from quai.soi import _tris
    ra = os.path.join(G.BASE, "manh_goc")
    os.makedirs(ra, exist_ok=True)
    _, to_px, _ = tf()
    DATJ = {}

    def ve(a, ten):
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), to_px(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        lay = lay.convert("RGBA")
        bb = lay.getbbox()
        lay.crop(bb).save(os.path.join(ra, ten + ".png"))
        DATJ[ten] = dict(hop=[bb[0], bb[1], bb[2], bb[3]], nguon="da gốc")

    _, imgs, atts = G.nap("att_idle0.json")
    for a in atts:
        ve(a, a["region"])
    for a in json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))["atts"]:
        if a.get("region") in ("longdan_5", "longdan_6") and a["slot"] in ("longdan_7", "longdan_8"):
            ve(a, a["region"])
    for s, d in (("ngu_t", "longdan_5"), ("ngu_p", "longdan_6")):
        Image.open(os.path.join(ra, d + ".png")).save(os.path.join(ra, s + ".png"))
        DATJ[s] = dict(DATJ[d])
    g = Image.new("RGBA", (620, 200), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([0, 10, 619, 390], fill=(139, 101, 66, 255), outline=(43, 33, 24, 255), width=7)
    g.save(os.path.join(ra, "go_dat.png"))
    DATJ["go_dat"] = dict(hop=[458, 160, 1078, 360], nguon="vẽ tạm")
    h = Image.new("RGBA", (660, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(h)
    d.ellipse([0, 20, 659, 219], fill=(139, 101, 66, 255), outline=(43, 33, 24, 255), width=7)
    d.ellipse([20, 40, 639, 180], fill=(42, 30, 22, 255))
    h.save(os.path.join(ra, "ho.png"))
    DATJ["ho"] = dict(hop=[438, 650, 1098, 870], nguon="vẽ tạm")
    json.dump(DATJ, open(os.path.join(ra, "dat.json"), "w"), indent=1)
    print(ra, sorted(DATJ))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "goc":
        goc()
    elif cmd == "khung":
        khung()
    elif cmd == "prompt":
        prompt()
    elif cmd == "mat":
        mat()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
