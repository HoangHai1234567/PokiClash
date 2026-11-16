# -*- coding: utf-8 -*-
"""Tinh linh quặng sắt (quang_sat, rig monster_3371): concept THEO CON GỐC (khối vỏ tròn, dải mặt tối hai mắt bầu dục, ba tinh thể trên
đầu, hai tinh thể làm tay), đổi sang chất liệu ĐÁ + QUẶNG SẮT, giữ nguyên mắt (người dùng: "chủ ý làm biểu cảm mắt như con gốc").

    quang_sat_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/quang_sat_1/mau/goc_ca_con.png (+ .json: khung từng part)
    quang_sat_da.py concept    ba file prompt concept (ba hướng) → gui_gpt/quang_sat_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quang_sat as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "quang_sat_1")
TINH_SAT = os.path.join(HERE, "inbox", "tinh_sat_1", "tai_ve", "L1_duyet.png")
TUONG_DA = os.path.join(HERE, "inbox", "tuong_da_2", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"

# slot của họ → tên bộ phận (để ghi khung bao vào prompt)
TEN = {"longdan_9": "SHELL (body)", "longdan_4": "BIG TOP CHUNK", "longdan_3": "LEFT TOP CHUNK", "longdan_2": "RIGHT TOP CHUNK",
       "longdan_1": "LEFT HAND", "longdan_0": "RIGHT HAND", "longdan_7": "LEFT EYE", "longdan_8": "RIGHT EYE"}


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def khung_ca_con(atts, cao=760.0):
    """phép đổi toạ độ rig → ảnh 1536 × 1024: cả con cao ~cao px, đặt giữa khung."""
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024; ghi khung bao từng part trên ảnh."""
    _, imgs, atts = G.nap("att_idle0.json")
    s, cx, cy, T = khung_ca_con(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    hop = {}
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)
        lay = lay.convert("RGBA")
        al = np.asarray(lay)[..., 3] > 60
        if al.any():
            ys, xs = np.nonzero(al)
            hop[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
        can.alpha_composite(lay)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")
    for k, v in hop.items():
        print(k, TEN.get(k, ""), v)


MO_TA_CON = (
    "PIECE BY PIECE (as in image 1): a chubby round DOME-shaped little creature seen from the front, turned slightly to the viewer's RIGHT, "
    "sitting low on the ground (no legs). Its body is one big rounded SHELL like a helmet or a turtle dome. Across the lower half of the "
    "front there is a wide DARK FACE BAND (an opening in the shell, like a visor): its top edge dips down in a V in the middle (this V "
    "gives the face a determined frown), its bottom edge is a wavy zigzag, and under it the shell continues as a thick rounded lower lip. "
    "Inside the dark band two upright vertical OVAL EYES, flat colour, no pupils: the left eye (viewer's left) a little bigger, the right "
    "eye a little smaller (the head is turned slightly right). No mouth, no nose, no brows. Two small diamond-shaped STUDS sit on the "
    "shell just above the two upper corners of the dark band (like little brows). Two thin seam lines run down over the top of the shell. "
    "On top of the shell THREE pieces stand up: a BIG one in the middle (the tallest, leaning slightly right), a smaller one on the upper "
    "left leaning out to the left, and a small slim one on the upper right leaning out to the right; their lower ends overlap the top of "
    "the shell. At the two sides float two separate pieces that are its HANDS (they do not touch the body; there are no arms): a long one "
    "at the lower left, in FRONT of the shell edge, slanting down to the left with its lower end near the ground, and a short slim one at "
    "the lower right, just beside the lower right edge of the shell (touching it, slightly behind it), pointing down.")

KHONG = ("VERY SIMPLE DESIGN, FEW DETAILS (like image 1): no extra chunks, spikes or rocks, no cracks all over, no moss, no runes, no "
         "glowing veins, no bolts, no badges, no mouth, no brows, no arms, no legs, nothing that is not listed.")

# ba hướng (Claude đề xuất, chờ người dùng chọn). Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("đá xám + quặng sắt gỉ (khối quặng cục)",
          "vỏ đá xám ấm; ba khối trên đầu + hai tay thành CỤC QUẶNG SẮT thô đầu bằng, mặt vỡ phẳng (bỏ mũi nhọn tinh thể), sắt xám "
          "sẫm có mảng gỉ cam; hai núm trên trán là hạt gỉ; mắt xanh lơ như con gốc",
          ["SHELL: rough grey STONE, ONE flat colour warm stone grey #B3ADA3 on the dome, the thick lower lip under the dark band a darker "
           "stone grey #918B82; the two seam lines on the top become two thin ink cracks (same places). The DARK FACE BAND flat charcoal "
           "#2E2C33 (same shape: V dip on top, wavy zigzag bottom).",
           "EYES: the SAME two upright ovals, same places and sizes, flat bright cyan #5FD8EE, one tiny white dot near the top of each "
           "eye. Nothing else in the dark band.",
           "STUDS: two small RUST nuggets (same diamond shape and place), flat rust orange #C0652F.",
           "THE THREE TOP PIECES and THE TWO HANDS become raw IRON ORE CHUNKS: each one keeps the SAME place, SIZE, LEAN and overlap as "
           "the crystal in image 1, but its shape is a blunt, chunky, irregular LUMP of ore broken out of a mine: a flat broken top "
           "face instead of a sharp tip, 3 to 4 big flat facets, slightly uneven edges. Colours: main facets dark iron grey #636A77, "
           "the facets turned away darker iron #444A56, and on each chunk ONE flat RUST patch #B9612C covering part of one facet (a "
           "flat colour area with its own thin ink edge). The long LEFT HAND chunk is a long blunt lump; the short RIGHT HAND chunk a "
           "short slim blunt lump."]),
    "B": ("đá cát + hematit đỏ (cụm khối vuông)",
          "vỏ đá cát vàng nhạt; ba khối trên đầu + hai tay ĐỔI DÁNG thành CỤM KHỐI LẬP PHƯƠNG (2–3 khối vuông lồng nhau) quặng "
          "hematit đỏ nâu, mặt trên xám thép; hai núm trán thép xám; mắt hổ phách",
          ["SHELL: smooth sandy STONE, ONE flat colour pale sand #D3C2A0 on the dome, the thick lower lip under the dark band darker "
           "sand #B09D7B; the two seam lines on the top stay two thin ink lines (same places). The DARK FACE BAND flat dark brown-"
           "charcoal #2F2A2C (same shape: V dip on top, wavy zigzag bottom).",
           "EYES: the SAME two upright ovals, same places and sizes, flat warm AMBER #F2A93B, one tiny white dot near the top of each "
           "eye. Nothing else in the dark band.",
           "STUDS: two small steel-grey studs #A3ABB6 (same diamond shape and place).",
           "THE THREE TOP PIECES and THE TWO HANDS change SHAPE: each becomes a cluster of CUBE-shaped ore crystals (like natural "
           "cubic iron ore): 2 or 3 sharp-edged cubes of different sizes grown into each other, each cube drawn in simple 3/4 view with "
           "a TOP face, a FRONT face and a SIDE face. Each cluster fills the SAME place, the same overall size and follows the same lean "
           "as the crystal in image 1 (the big middle one: a big cube with a smaller cube on its side; the long LEFT HAND: three cubes in "
           "a row along the old crystal's length, getting smaller toward the lower end; the RIGHT HAND: two small cubes stacked). "
           "Colours: front faces reddish iron ore (hematite) #9A4535, side faces darker #6E2E25, top faces steel grey #A3ABB6."]),
    "C": ("đá xám lam + từ thạch đen (tinh thể bát diện)",
          "vỏ đá xám lam nhạt, vài chấm sắt sẫm; ba khối trên đầu + hai tay ĐỔI DÁNG thành tinh thể BÁT DIỆN (hai chóp úp đáy, như "
          "từ thạch) sắt đen, một đường gờ bạc; hai núm trán bạc; mắt xanh lơ",
          ["SHELL: pale blue-grey STONE, ONE flat colour #B7BDC5 on the dome with only THREE small dark iron speckles #4A4F59 on it, the "
           "thick lower lip under the dark band darker #959BA4; the two seam lines on the top stay two thin ink lines (same places). "
           "The DARK FACE BAND flat charcoal #2A2C33 (same shape: V dip on top, wavy zigzag bottom).",
           "EYES: the SAME two upright ovals, same places and sizes, flat bright cyan #5FD8EE, one tiny white dot near the top of each "
           "eye. Nothing else in the dark band.",
           "STUDS: two small silver studs #C9CFD7 (same diamond shape and place).",
           "THE THREE TOP PIECES and THE TWO HANDS change SHAPE: each becomes a black IRON (magnetite) OCTAHEDRON crystal: a double-"
           "pointed diamond shape made of two pyramids joined base to base, with a pointed tip at both ends and one clear middle edge "
           "where the two pyramids meet. Each fills the SAME place, length and lean as the crystal in image 1 (the big middle one a big "
           "fat octahedron standing on the shell, its lower tip hidden behind the shell top; the two hands long double-pointed shards). "
           "Colours: lit facets black iron #434751, facets turned away darker #2A2D34, ONE thin silver line #C3CAD3 along the main ridge "
           "of each crystal."]),
}

STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) for the "
    "few inner edges (the facet edges of the ore chunks, the edge of the dark face band, the seam lines), and every area filled with ONE "
    "flat colour with visible coloured-pencil / wax-crayon hatching. Image 1 is painted in a smooth digital style with soft gradients "
    "(purple to pink crystals, glowing eyes, soft light on the shell): do NOT copy that painting style or its colours: no shading, no "
    "highlights, no white shine streaks, no gradients, no glow, no shadows, no gloss, no sparkles: flat colour only. A different tone "
    "appears only where a different facet or material is listed. The only exception: one tiny white dot in each eye. Drawn carefully and "
    "cleanly, not scribbled.")


def prompt_concept():
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    hop = json.load(open(mau[:-4] + ".json"))["hop"]
    R = [(mau, "the REFERENCE creature, 1536x1024, white background: a chubby round pale dome-shaped spirit with a wide dark face band "
               "and two glowing cyan oval eyes, three purple-pink CRYSTALS standing on its head and two floating purple-pink crystals as "
               "its hands. It is painted in a smooth digital style with gradients. Keep its POSE, its PIECES, their PLACES and SIZES, "
               "and its EYES; change its MATERIAL and LOOK.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): khối vỏ tròn trắng, dải mặt tối hai mắt bầu dục xanh lơ, ba tinh thể "
          "tím hồng trên đầu, hai tinh thể làm tay lơ lửng hai bên. Giữ dáng, từng mảnh, chỗ, cỡ và đôi mắt; đổi chất liệu"),
         (TINH_SAT, "an approved hero of our game from the same metal island (a little iron-crystal spirit), 1536x1024, white "
                    "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and how flat metal facets "
                    "and darker side facets are drawn. Do NOT copy its design, face or colours.",
          "Tinh linh tinh thể sắt (tướng 1 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô mặt kim loại phẳng + mặt bên sẫm"),
         (TUONG_DA, "another approved hero of our game (a stone golem), 1536x1024, white background: see how flat STONE is drawn and "
                    "coloured with crayon. Do NOT copy its design, plants or colours.",
          "Tượng đá giữ rừng đã duyệt: xem cách tô đá phẳng bằng sáp màu")]
    vi_tri = ["POSITIONS on the 1536x1024 canvas (bounding boxes of each piece in image 1; keep them):"]
    for slot, ten in TEN.items():
        if slot in hop:
            x0, y0, x1, y1 = hop[slot]
            vi_tri.append(f"- {ten}: x = {x0} to {x1}, y = {y0} to {y1}")
    hd = ["# Gói GPT: tinh linh quặng sắt (quang_sat), tướng 3 đảo Kim", "",
          "Con gốc của rig: `monster_3371` (khối vỏ trắng mặt tối, tinh thể tím; game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng "
          "trong máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng (2026-11-16)", "",
          "Người dùng: \"concept tinh linh quặng sắt, chủ ý làm biểu cảm mắt như con gốc\". Ba file, mỗi file một hướng; giữ dáng, chỗ và "
          "cỡ từng mảnh của con gốc (để lắp lên đúng xương), giữ nguyên đôi mắt bầu dục + dải mặt tối, đổi vỏ sang đá và tinh thể sang "
          "quặng sắt. A giữ gần hình bóng (tinh thể thành cục quặng đầu bằng); B, C đổi dáng khối quặng (khối lập phương; bát diện).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: RESTYLE. Redraw the creature of image 1 as ONE picture of a little IRON ORE SPIRIT (a living lump of stone and iron "
              "ore): the SAME creature in the SAME pose, with EVERY piece in the same place, at the same size, with the same overlaps (if "
              "the new picture were laid over image 1, every piece must coincide), except the shape changes described below; new "
              "materials (stone and iron ore instead of a pale shell and purple crystals), new colours and our hand-drawn drawing style. "
              "Do not add, remove, merge or move pieces. Keep the EYES exactly as in image 1 (two upright ovals in the dark band, same "
              "size, same place, no pupils, no brows): the eyes are the character's expression.", "",
              MO_TA_CON, ""] + vi_tri + ["",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              KHONG, "",
              STYLE, "",
              "Mood: a sturdy, determined little ore spirit ready to fight (a game hero), not a cute mascot, not scary.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the creature at the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng từng mảnh như ảnh 1 (chồng lên phải trùng, trừ dáng khối quặng ở B, C); mắt hai hình bầu dục đứng trong "
           "dải mặt tối đúng chỗ, mắt trái to hơn chút, không con ngươi, không mày, không miệng; tay trái nằm TRƯỚC mép vỏ, tay phải nằm "
           "SAU vỏ; nét bút mực rung, vân sáp, tô phẳng, không bóng, không vệt sáng trắng, không phát sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"keep the eyes exactly as in image 1: two upright flat ovals, no pupils, no brows\"; \"remove the shading and "
           "highlights, flat colour only\"; \"keep every piece at the same place and size as in image 1\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)
