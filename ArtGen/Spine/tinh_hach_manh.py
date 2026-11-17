# -*- coding: utf-8 -*-
"""Thiên thạch thú, bản D2 "lưng rừng tinh thể" (tinh_hach; tướng 9 đảo Thổ, ải 60, rig monster_3806): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ
concept đã duyệt (tai_ve/L1_duyet.png = L2_D2.png, người dùng "làm D2" 2026-11-17). Cách làm như quy_nui_manh.py: concept căn lên con
gốc bằng co k + dời (mau/can.json), mỗi mảnh đặt theo chỗ của nó trên concept, rig (tinh_hach_rig.py) gắn vào nhóm lưới gốc tương ứng.

Mảnh (thứ tự vẽ sau → trước; "gần" = tay bên TRÁI tranh = slot *_r của họ, "xa" = bên phải = *_l):
    cum1..cum5      5 cụm tinh thể bay dưới chân                  Q2   ← qiu_* (gán theo chỗ)
    duoi            đuôi + quạt ba lưỡi tinh thể ngọc lam           Q3   ← chuỗi xương riêng ở hông (họ không có đuôi liền thân)
    ngon_xa1..      móng tay xa                                     Q5   ← xương ngón *_l
    tay_xa          tay xa (bắp, cẳng, bàn; không móng)             Q3   ← dabi_l, xiaobi_l, shouzhang_l + ngón *_l
    than            thân liền (bướu, vai, ngực, bụng, cổ)          Q1   ← shenti_02, shenti_03, shenti_04
    tt_sau          cụm tinh thể lưng phía sau (trên hông)          Q3   ← xương riêng con của xương thân
    tt_giua         cụm tinh thể lưng giữa (cao nhất)               Q5
    tt_truoc        cụm tinh thể lưng phía trước (sau đầu)          Q4
    long_mieng      lòng miệng đỏ                                   Q5   ← zuiba_01
    ham             hàm dưới + răng dưới                            Q4   ← zuiba_02 (xương hàm all10)
    tay_gan         tay gần (bắp, cẳng, bàn; không móng)            Q2   ← dabi_r, xiaobi_r + ngón *_r
    ngon_gan1..     móng tay gần                                    Q4   ← xương ngón *_r
    dau             đầu + diềm gai hổ phách + hàm trên răng trên    Q2   ← tou (xương đầu all6)
    BỎ của họ: vòng jinhuan_*, mây yun_*, sao xing_*, mảng tinh vân xingkong_* / xiongkong_*, đuôi chạc weiba (thay bằng đuôi liền thân).

    tinh_hach_manh.py can          căn concept lên hình con gốc (co + dời, IoU) → mau/can.json
    tinh_hach_manh.py prompt       file prompt từng nhóm → gui_gpt/tinh_hach_1/luot_3_<nhóm>.txt (+ nối HUONG_DAN.md)
    tinh_hach_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    tinh_hach_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
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
import tho9  # noqa: E402,F401  (đăng ký mã tinh_hach vào tho5.CON)
import tho5  # noqa: E402
import quy_nui_manh as Q  # noqa: E402

G = tho5.dat("tinh_hach")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "tinh_hach_1")

# tâm dự kiến (px concept) của từng mảnh, để gán cụm cắt ra cho đúng tên
TAM = {"than": (720, 520), "dau": (1035, 390), "tay_gan": (510, 620), "tay_xa": (930, 660), "duoi": (330, 740),
       "tt_sau": (570, 340), "tt_giua": (770, 220), "tt_truoc": (935, 200), "ham": (1090, 600), "long_mieng": (1075, 510),
       "rung": (750, 250), "tt_nam": (795, 365),
       "cum1": (765, 770), "cum2": (845, 855), "cum3": (945, 895), "cum4": (1075, 840), "cum5": (1180, 720)}
# vùng (px concept) của từng bộ móng: mọi cụm nằm trong vùng là một móng, xếp trái → phải
VUNG_NGON = {"ngon_gan": (480, 700, 720, 880), "ngon_xa": (960, 660, 1160, 820)}

HONG = ("the top of the back is a rounded obsidian hump whose outline runs just under the bases of the crystals (about y 440 at x 500, "
        "y 330 at x 620, y 300 at x 760, y 300 at x 900)")
NHOM = {
    "Q1": [("than", "the BODY: the hulking black obsidian torso (the hump of the back, the shoulders, the chest, the belly and the neck down "
            "from under the head) with its flat amber vein cracks",
            "draw it as ONE complete closed black stone torso: " + HONG + "; the neck continues up behind the head and ends in a rounded "
            "neck top; the parts hidden by the near arm on the left, by the far arm on the right and where the tail starts at the lower "
            "left continue as the same black stone (rounded hip at the lower left). NO head, NO jaw, NO arms, NO hands, NO claws, NO tail, "
            "NO crystals, NO floating stones")],
    "Q2": [("dau", "the HEAD: the upper head with the heavy brow, the narrow amber eye, the snout, the UPPER fangs, and the row of small "
            "amber crystal points along the back and top of the head (the frill)",
            "WITHOUT the lower jaw, the lower teeth and the red inside of the mouth: the upper jaw ends along its row of upper fangs; "
            "complete the back of the head and its bottom (where it meets the neck) as a rounded black shape"),
           ("tay_gan", "the NEAR ARM on the LEFT: the thick black shoulder, upper arm, forearm and the black hand resting on the ground, "
            "with its amber vein crack", "WITHOUT the cream claws (the hand ends in short rounded black finger tips where the claws "
            "start); complete its top, hidden against the body, as a rounded shoulder"),
           ("cum1", "the small floating CRYSTAL CLUSTER at the bottom just right of the near hand (crystals set in a chunk of brown rock)",
            "keep it exactly"),
           ("cum2", "the floating CRYSTAL CLUSTER below it, a little to the right", "keep it exactly"),
           ("cum3", "the small floating CRYSTAL CLUSTER at the bottom centre (the lowest one)", "keep it exactly"),
           ("cum4", "the BIG floating CRYSTAL CLUSTER at the bottom right, under the far hand", "complete its top, hidden under the far "
            "hand's claws, as the same crystals and rock"),
           ("cum5", "the small floating CRYSTAL CLUSTER at the far right", "keep it exactly")],
    "Q3": [("tay_xa", "the FAR ARM on the RIGHT: the black arm reaching from under the chest to the right, and its black hand",
            "WITHOUT the cream claws (the fingers end in short rounded black tips where the claws start); complete its root, hidden "
            "behind the body, as a rounded shoulder"),
           ("duoi", "the TAIL at the lower left: the thick black tail and the fan of three flat turquoise crystal blades at its end",
            "complete its root, hidden behind the body and the near arm, as a thick rounded black end"),
           ("tt_sau", "the REAR CRYSTALS on the back (the group of turquoise and amber crystals on the LEFT half of the back, over the "
            "hip and the near shoulder, x 470-660)", "draw each crystal complete (their hidden bottoms continue straight down to a flat "
            "base); NO body")],
    "Q4": [("ham", "the LOWER JAW with its row of lower fangs (the black chin and jaw below the open mouth)",
            "complete its back end, hidden under the cheek, as a rounded hinge; NO red inside of the mouth"),
           ("tt_truoc", "the FRONT CRYSTALS on the back (the group of turquoise and amber crystals just behind the head, x 840-1020, "
            "y 100-300)", "draw each crystal complete (their hidden bottoms continue straight down to a flat base); NO head, NO body"),
           ("ngon_gan", "the four curved cream CLAWS of the near hand on the left (on the ground)",
            "draw EACH claw as its own closed shape with a short rounded base where it comes out of the finger (the fingers are NOT "
            "drawn); keep a thin white gap between neighbouring claws")],
    "Q5": [("tt_giua", "the MIDDLE CRYSTALS on the back (the tallest group of turquoise and amber crystals in the middle of the back, "
            "x 620-900, including the big turquoise crystal lying over the shoulder)", "draw each crystal complete (their hidden "
            "bottoms continue straight down to a flat base); NO body, NO other crystals"),
           ("long_mieng", "the dark-red INSIDE OF THE MOUTH (with the tongue) between the upper and the lower fangs",
            "complete it as one closed rounded cavity shape that continues a little up behind the upper jaw and down behind the lower "
            "jaw; NO teeth, NO jaw, NO head"),
           ("ngon_xa", "the curved cream CLAWS of the far hand on the right (gripping the big crystal cluster)",
            "draw EACH claw as its own closed shape with a short rounded base where it comes out of the finger (the fingers are NOT "
            "drawn); keep a thin white gap between neighbouring claws")],
    # lượt sửa: Q2–Q5 mỗi tờ vẽ lại gần trọn rừng tinh thể có đáy phẳng (ba bản chồng nhau), Q2 vẽ tay gần lấn cả mảng ngực có mạch
    # hổ phách → rừng tinh thể gen MỘT ảnh (sau thân), tinh thể lớn vắt qua vai gen riêng (trước thân), tay gần gen lại chỉ cánh tay.
    "Q6": [("rung", "the FOREST OF CRYSTALS on the back: ALL the tall turquoise and amber crystal pillars growing out of the back, from the "
            "small ones over the hip on the left (x 480) to the ones just behind the head on the right (x 1015), EXCEPT the big turquoise "
            "crystal lying diagonally over the shoulder (x 700-890, y 285-450)",
            "draw every crystal complete and exactly as in image 1; their LOWER parts, hidden behind the body in image 1, continue "
            "STRAIGHT DOWN as the same crystals to about y 480-520 (they will be hidden behind the body); NO flat base line, NO ground, NO "
            "rock, NO body, NO head, NO small amber points of the head")],
    "Q7": [("tt_nam", "the BIG turquoise CRYSTAL lying diagonally over the shoulder (x 700-890, y 285-450), a long six-sided crystal "
            "pointing up to the left", "complete it as ONE closed crystal: its lower right end, partly hidden in image 1, ends in a flat "
            "cut end with an ink outline; NO other crystals"),
           ("tay_gan", "ONLY the NEAR ARM on the LEFT: the rounded shoulder (top at about x 500, y 445), the upper arm going down to the "
            "elbow at about x 430, y 600, the forearm going down to the right, and the black hand resting on the ground at about x 520-690, "
            "y 720-800", "the arm is ONLY the part LEFT of the small white gap at about x 565, y 610: the chest with the two amber vein "
            "cracks (x 590-780) is NOT part of the arm and must NOT be drawn; WITHOUT the cream claws (the hand ends in short rounded "
            "black finger tips where the claws start); complete its shoulder top, hidden against the body, as a rounded ball")],
}
# mảnh của lượt cũ không dùng (đã thay bằng Q6, Q7): cắt ra nhưng không lưu
BO = {("Q2", "tay_gan"), ("Q3", "tt_sau"), ("Q4", "tt_truoc"), ("Q5", "tt_giua")}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a hulking black obsidian METEOR BEAST crouching and "
        "lunging to the right, with flat amber vein cracks; a forest of tall turquoise and amber crystal pillars grows out of its back; a "
        "fierce head with a row of small amber crystal points behind it, an open fanged mouth and a narrow amber eye; a thick near arm on "
        "the left with four cream claws on the ground, a far arm on the right whose claws grip a big floating crystal cluster; a tail at "
        "the lower left ending in a fan of three turquoise crystal blades; five floating crystal clusters set in brown rock at the "
        "bottom. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
STYLE = Q.STYLE

Wp = Q.Wp
ghi = Q.ghi


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def _bind():
    """trỏ các hàm dùng chung của quy_nui_manh sang thư mục của tướng này."""
    Q.G, Q.CONCEPT, Q.MANH, Q.GUI = G, CONCEPT, MANH, GUI


def can():
    _bind()
    Q.can()


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3")[0].rstrip("\n") if os.path.exists(hd) else "# Gói GPT: tinh_hach"
    gd = ["", "## Lượt 3: mảnh đúng chỗ, đúng cỡ từ concept D2 đã chọn (2026-11-17; người dùng \"làm D2\" = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept D2 (1536 × 1024, nền trắng): thú thiên thạch đá vỏ chai đen mạch hổ phách, "
          "rừng trụ tinh thể ngọc lam + hổ phách trên lưng, đầu dữ có diềm gai hổ phách, đuôi quạt ba lưỡi tinh thể, năm cụm tinh thể bay. "
          "Mỗi nhóm chỉ giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị che.", ""]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_3_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap between the "
             "kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles, no glow."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): file prompt `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `tinh_hach_manh.py ghep`); phần bị che vẽ đủ, viền kín; "
           "nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def cat(chi=None):
    _bind()
    DATJ = Q.nap_dat()
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = Q.moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A, lab, cum = Q._cum(src)
        print(f"{nh} ({os.path.basename(src)}): {len(cum)} cụm")
        dung = set()
        for ten_ngon, (x0, y0, x1, y1) in VUNG_NGON.items():
            if ten_ngon not in [s for s, _, _ in ds]:
                continue
            chon = [c for c in cum if x0 <= c[2][0] <= x1 and y0 <= c[2][1] <= y1 and c[1] > 250]
            chon.sort(key=lambda c: c[2][0])
            for k, c in enumerate(chon, 1):
                b = Q.luu_manh(A, lab == c[0], f"{ten_ngon}{k}", DATJ, os.path.basename(src))
                dung.add(c[0])
                print(f"  {ten_ngon}{k:<3d} hộp {b}, {c[1]} px")
        slots = [s for s, _, _ in ds if s not in VUNG_NGON]
        gan = {s: [] for s in slots}
        for i, a, c, _ in cum:
            if i in dung or not slots:
                continue
            best = min(slots, key=lambda s: np.hypot(c[0] - TAM[s][0], c[1] - TAM[s][1]))
            d = np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1])
            if d < 260 or a > 20000:
                gan[best].append(i)
            else:
                print(f"  bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {a} px")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:10s} KHÔNG THẤY MẢNH")
                continue
            if (nh, s) in BO:
                print(f"  {s:10s} (bản cũ, bỏ)")
                continue
            b = Q.luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            print(f"  {s:10s} hộp {b}, {len(ids)} cụm")
    Q.ghi_dat(DATJ)


def thu_tu(DATJ):
    ng = lambda p: sorted([k for k in DATJ if k.startswith(p)])
    return (["cum1", "cum2", "cum3", "cum5", "cum4", "duoi"] + ng("ngon_xa") + ["tay_xa", "rung", "than", "tt_nam",
            "long_mieng", "ham", "tay_gan"] + ng("ngon_gan") + ["dau"])


def ghep():
    _bind()
    DATJ = Q.nap_dat()
    Q.THU_TU = thu_tu(DATJ)
    Q.ghep()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
