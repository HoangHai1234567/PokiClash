# -*- coding: utf-8 -*-
"""Tatu mai đá (cong_da, tướng 1 đảo Thổ, rig monster_3378): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png = L1_C,
người dùng chọn 2026-11-17: tatu con lông vàng đất, mai đá bốn tấm, cụm pha lê hổ phách trên đỉnh, sỏi bám mép mai). Concept vẽ cùng khung
với hình cả con gốc ở khung 0 idle (mau/goc_ca_con.json: s px / đơn vị, tâm cx, cy) nhưng tỉ lệ khác con gốc (concept "gần giống"), nên mỗi
mảnh đặt theo chỗ của nó trên concept rồi gắn vào xương / lưới gần nhất của họ (cong_da_rig.py, cách của quang_sat_rig.py).

Mảnh (tên ảnh = tên slot của họ để rig tra; mảnh thêm có tên riêng):
    body              thân + mõm + mặt (KHÔNG mắt, mày, miệng, tai)          M1
    hair3             mai đá bốn tấm (bám xương hair)                         M2
    tinh_the          cụm pha lê hổ phách trên đỉnh mai (mảnh thêm, bám hair) M3
    hair2 / hair1     viên sỏi to / nhỏ ở mép trái mai                        M3
    hair4             viên sỏi ở mép phải trên mai                            M3
    mml / mmr         tai trái / tai phải (thay hai tấm mày của họ)           M3
    tail              đuôi                                                    M3
    footl2 / footl1 / footr1   chân sau xa / chân giữa gần / chân trước gần  M4
    eyes, yq1, yp1, yp2, mt1  tròng trắng hai mắt / hai con ngươi / mày trái / mày phải / miệng: cắt thẳng từ concept (mat)
    hair5, footr2     không có trên concept: dùng lại ảnh hair1 / footl1 (rig đặt ở chỗ part gốc)

    cong_da_manh.py prompt       file prompt từng nhóm → gui_gpt/cong_da_1/luot_2_<nhóm>.txt (+ nối HUONG_DAN.md)
    cong_da_manh.py mat          cắt mắt, con ngươi, mày, miệng thẳng từ concept → manh/*.png
    cong_da_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    cong_da_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
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

G = tho5.dat("cong_da")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "cong_da_1")

# tâm dự kiến (px concept) của từng mảnh: để gán cụm cắt ra cho đúng tên (đọc trên mau/_goc_tren_concept.png)
TAM = {"body": (780, 760), "hair3": (740, 500), "tinh_the": (775, 190), "hair2": (395, 632), "hair1": (440, 680), "hair4": (1028, 390),
       "mml": (775, 575), "mmr": (1027, 555), "tail": (470, 795), "footl2": (560, 880), "footl1": (770, 900), "footr1": (1003, 890),
       "body_truoc": (850, 740), "eyes": [(875, 700), (1035, 680)], "mt1": (980, 782), "yq1": [(905, 700), (1043, 682)], "yp1": (880, 648), "yp2": (1030, 640)}

NHOM = {
    "M1": [("body", "the BODY: the round sandy-ochre furry body with the cream belly, the cream face patch round the snout and the short "
            "pointed SNOUT with its round dark-brown nose",
            "draw it WITHOUT the eyes, WITHOUT the angry brows, WITHOUT the mouth line and WITHOUT the two ears: where they were, plain fur in "
            "the same flat colours (ochre on the upper face, cream on the lower face round the snout). Its top, hidden under the stone shell "
            "in image 1, continues as a plain rounded furry back (a complete round bun-shaped body). Its lower edge, hidden behind the legs "
            "and the tail, continues as a plain rounded cream belly. No legs, no tail, no shell")],
    "M2": [("hair3", "the big STONE SHELL made of four overlapping curved grey-beige plates (the armadillo shell on the back)",
            "complete it into ONE closed shape: the places covered by the amber crystals on top, by the two ears, by the three round pebbles "
            "and by the body's face must be drawn as the shell continues (plain grey-beige plates with the same plate lines); on top of the "
            "shell, where the crystals stand, a small dark broken-open HOLE (a flat dark brown opening, the crystals are NOT drawn)")],
    "M3": [("tinh_the", "the cluster of FOUR AMBER CRYSTALS standing on top of the shell", "complete their bottoms: the four crystals stand on "
            "a short common base that would sit inside the hole of the shell (draw that base as the crystals continue, amber)"),
           ("hair2", "the BIGGER round grey PEBBLE stuck to the lower LEFT edge of the shell", "complete it into one closed round pebble"),
           ("hair1", "the SMALLER round grey PEBBLE just below it, at the lower left edge of the shell", "complete it into one closed round "
            "pebble"),
           ("hair4", "the round grey PEBBLE on the upper RIGHT edge of the shell", "complete it into one closed round pebble"),
           ("mml", "the LEFT EAR (round, ochre with a pink inside)", "complete its bottom, hidden in the fur, as a rounded base"),
           ("mmr", "the RIGHT EAR (round, ochre with a pink inside)", "complete its bottom, hidden in the fur, as a rounded base"),
           ("tail", "the short TAIL at the lower left with its two dark rings", "complete its root, hidden behind the body, as a rounded end")],
    "M4": [("footl2", "the BACK LEFT LEG (lower left) with its foot and three small cream claws", "complete its top, hidden under the body, as "
            "a rounded thigh"),
           ("footl1", "the MIDDLE LEG (bottom middle) with its foot and four small cream claws", "complete its top, hidden under the body, "
            "as a rounded thigh"),
           ("footr1", "the FRONT RIGHT LEG (lower right) with its foot and three small cream claws", "complete its top, hidden under the "
            "body, as a rounded thigh")],
    "M5": [("body_truoc", "ONLY the VISIBLE part of the furry body as it appears in image 1: the head and face with the short pointed snout "
            "and its round dark nose, the cream face patch, the side of the body and the cream belly below the stone shell",
            "do NOT complete anything hidden: its outline runs exactly along its visible boundary in image 1 (the dark line where the head "
            "meets the stone shell, the dark head-top line that passes IN FRONT of the bottoms of the two ears, and the outer outline). Draw "
            "it WITHOUT the eyes, WITHOUT the angry brows, WITHOUT the mouth line (plain fur in the same flat colours there), without the "
            "ears, legs, tail, shell, crystals and pebbles")],
    "F1": [("eyes", "the WHITES of the TWO EYES with their dark-brown ink outline rings (the big near eye on the left and the narrow far eye "
            "peeking at the right edge of the face)", "draw each eye white as a complete closed shape: the dark pupils are NOT drawn (where "
            "they were, plain white inside the outline) and the angry brows are NOT drawn (the outline ring of each eye stays complete and "
            "thin where the brow was)"),
           ("mt1", "the small frowning MOUTH line under the eyes", "just the curved ink stroke")],
    "F2": [("yq1", "the TWO dark-brown PUPILS (each with its small white highlight dot)", "each pupil a complete round dark disc in the same "
            "place and size as in image 1 (complete the part that touches the eye outline as a round disc); no eye white, no outline ring"),
           ("yp1", "the thick angry BROW stroke over the LEFT (big) eye", "just the brow stroke, a little apart from the pupil"),
           ("yp2", "the thick angry BROW stroke over the RIGHT (far) eye", "just the brow stroke")],
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a round armadillo pup with sandy-ochre fur, a cream belly and "
        "face patch, a short pointed snout with a round dark nose, two determined eyes with angry brows, two small round ears, four stubby "
        "legs with cream claws and a short ringed tail; on its back a big grey-beige stone shell of four curved plates with a cluster of "
        "four amber crystals on top and three round pebbles stuck to its edges. Hand-drawn: wobbly dark-brown ink line, crayon hatching, "
        "flat colours.")
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


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-17; người dùng chọn C = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): tatu con lông vàng đất, mai đá bốn tấm, "
          "cụm pha lê hổ phách, ba viên sỏi, mắt cau, tai tròn, bốn chân ngắn, đuôi khoanh. Mỗi nhóm chỉ giữ vài mảnh không chồng nhau, đúng "
          "chỗ, đúng cỡ, vẽ đủ phần bị che. Mắt, con ngươi, mày, miệng Claude cắt thẳng từ concept.", ""]
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
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `cong_da_manh.py ghep`); phần bị che vẽ đủ, viền kín; thân "
           "không còn mắt, mày, miệng, tai; mai có hốc trống ở đỉnh (không vẽ pha lê); nền trắng tinh."]
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
    """dải mép r px lấy màu TỐI NHẤT quanh nó (điểm khử răng cưa pha giấy trắng để lại viền sáng quanh mảnh)."""
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def luu_manh(A, m, ten, DATJ, nguon, sua=None):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    if sua is not None:
        rgb = sua(rgb, mm)
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


def cat(chi=None):
    DATJ = nap_dat()
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        slots = [s for s, _, _ in ds]
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = [i for i in range(1, n) if st[i, 4] > 30]
        gan = {s: [] for s in slots}
        for i in cum:
            c = cen[i]
            # cụm to (≥ 25 % mảnh to nhất của nhóm) gán theo tâm gần nhất; mảnh vụn (bụi mực) theo cụm to gần nhất
            def kc(s):
                ts = TAM[s] if isinstance(TAM[s], list) else [TAM[s]]
                return min(np.hypot(c[0] - x, c[1] - y) for x, y in ts)
            best = min(slots, key=kc)
            d = kc(best)
            if d < (110 if nh.startswith("F") else 260) or st[i, 4] > 20000:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {st[i, 4]} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:10s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            print(f"  {s:10s} hộp {b}, {len(ids)} cụm")
    ghi_dat(DATJ)


# ---------------------------------------------------------------- mắt, mày, miệng cắt thẳng từ concept
MAT_HOP = {"t": (805, 630, 945, 770), "p": (995, 620, 1075, 735)}      # hộp quanh mắt trái / phải (px concept)
MIENG_HOP = (935, 755, 1025, 810)


def mat():
    """tròng trắng hai mắt (vành mực quanh tròng, con ngươi tô trắng) → eyes; con ngươi (nâu sẫm + chấm trắng) → yq1; mày (nét mực dày
    phía trên mỗi mắt) → yp1 / yp2; miệng (nét mực cong) → mt1."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    lum = A.mean(2)
    m_trang = np.zeros((H, W), bool)
    m_nguoi = np.zeros((H, W), bool)
    m_may = {}
    for ben, (x0, y0, x1, y1) in MAT_HOP.items():
        sub = A[y0:y1, x0:x1]
        trang = (sub.min(2) > 215)
        n, lab, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), 8)
        k = 1 + int(np.argmax(st[1:, 4]))                              # tròng trắng = vùng trắng to nhất trong hộp
        tr = (lab == k).astype(np.uint8)
        cs, _ = cv2.findContours(tr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        kin = cv2.drawContours(np.zeros_like(tr), cs, -1, 1, -1).astype(bool)      # tròng kín (lấp con ngươi + chấm sáng)
        nguoi = kin & ~tr.astype(bool) & (sub.mean(2) < 150)
        nguoi = cv2.dilate(nguoi.astype(np.uint8), el(1)).astype(bool) & kin
        # con ngươi kín: lấp chấm sáng bên trong
        cs2, _ = cv2.findContours(nguoi.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        nguoi = cv2.drawContours(np.zeros_like(tr), cs2, -1, 1, -1).astype(bool)
        vanh = cv2.dilate(kin.astype(np.uint8), el(6)).astype(bool)        # tròng + vành mực
        m_trang[y0:y1, x0:x1] |= vanh
        m_nguoi[y0:y1, x0:x1] |= cv2.dilate(nguoi.astype(np.uint8), el(1)).astype(bool)
        # mày: nét mực dày phía trên tròng, không dính vành mắt: điểm tối trong dải phía trên, trừ vành mắt
        my0, my1 = max(0, y0 - 45), y0 + int(0.45 * (y1 - y0))
        dai = np.zeros((H, W), bool)
        dai[my0:my1, x0 - 15:x1 + 10] = True
        toi = (lum < 95) & dai
        toi[y0:y1, x0:x1] &= ~cv2.dilate(kin.astype(np.uint8), el(3)).astype(bool)
        n2, lab2, st2, _ = cv2.connectedComponentsWithStats(toi.astype(np.uint8), 8)
        if n2 > 1:
            k2 = 1 + int(np.argmax(st2[1:, 4]))
            m_may[ben] = cv2.dilate((lab2 == k2).astype(np.uint8), el(1)).astype(bool)

    def to_trang(rgb, mm):                                              # tròng: con ngươi tô trắng
        x0, y0 = hop_tam["x0"], hop_tam["y0"]
        sub = m_nguoi[y0:y0 + rgb.shape[0], x0:x0 + rgb.shape[1]]
        rgb[sub] = (250, 248, 242)
        return rgb

    ys, xs = np.nonzero(m_trang)
    hop_tam = dict(x0=max(0, xs.min() - 3), y0=max(0, ys.min() - 3))
    print("eyes", luu_manh(A, m_trang, "eyes", DATJ, "L1_duyet.png (cắt thẳng)", sua=to_trang))
    print("yq1", luu_manh(A, m_nguoi, "yq1", DATJ, "L1_duyet.png (cắt thẳng)"))
    for ben, ten in (("t", "yp1"), ("p", "yp2")):
        if ben in m_may:
            print(ten, luu_manh(A, m_may[ben], ten, DATJ, "L1_duyet.png (cắt thẳng)"))
        else:
            print(ten, "KHÔNG THẤY MÀY")
    x0, y0, x1, y1 = MIENG_HOP
    mi = np.zeros((H, W), bool)
    mi[y0:y1, x0:x1] = lum[y0:y1, x0:x1] < 95
    n3, lab3, st3, _ = cv2.connectedComponentsWithStats(mi.astype(np.uint8), 8)
    k3 = 1 + int(np.argmax(st3[1:, 4]))
    print("mt1", luu_manh(A, cv2.dilate((lab3 == k3).astype(np.uint8), el(1)).astype(bool), "mt1", DATJ, "L1_duyet.png (cắt thẳng)"))
    ghi_dat(DATJ)


THU_TU = ["tail", "footl2", "footr1", "body", "footl1", "hair3", "tinh_the", "hair4", "hair2", "hair1", "mmr", "mml", "body_truoc", "mt1",
          "eyes", "yq1", "yp1", "yp2"]


def ghep():
    """ghép mảnh theo thứ tự vẽ của rig lên nền trắng; đặt cạnh concept; IoU hình bóng."""
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


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prompt":
        prompt()
    elif cmd == "mat":
        mat()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
