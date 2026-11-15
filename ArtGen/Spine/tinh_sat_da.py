# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt (tinh_sat, rig monster_3346): concept THEO CON GỐC rồi ĐỔI DA THEO KHUNG TỪNG PART (memory bam-con-goc-khung-part).
Mọi part giữ nguyên hình bóng, cỡ, chỗ, đường cấu trúc (cạnh mặt tinh thể); chỉ đổi chất liệu (tinh thể SẮT), màu, nét vẽ (bút mực + chì sáp,
tô phẳng). Rig dùng NGUYÊN lưới và xương của họ.

    tinh_sat_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/tinh_sat_1/mau/goc_ca_con.png (ảnh mẫu lượt concept)
    tinh_sat_da.py concept    ba file prompt concept (ba hướng màu sắt) → gui_gpt/tinh_sat_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    tinh_sat_da.py to         hai tờ mảnh GỐC cắt theo lưới, phóng to → mau/goc_<P|Q>.png + .json; prompt luot_2_da_<P|Q>.txt (cần L1_duyet.png)
    tinh_sat_da.py cat        cắt tờ Codex trả (tai_ve/D_<P|Q>.png) theo ô → inbox/tinh_sat_1/manh_part/<ảnh vùng>.png, IoU, tờ so
Ảnh mảnh gốc, hình cả con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tinh_sat as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
MANH = os.path.join(G.BASE, "manh_part")
GUI = os.path.join(HERE, "gui_gpt", "tinh_sat_1")
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
TI_TACH = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")
GOLEM = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
MUC = "#2B2118"

# ba hướng màu (Claude đề xuất, chờ người dùng chọn). Mỗi hướng: (tên Việt, mô tả màu tiếng Anh, mô tả Việt cho HUONG_DAN)
HUONG = {
    "A": ("thép lam (gần màu con gốc nhất)",
          "IRON-CRYSTAL PALETTE A, BLUE STEEL (each area ONE flat colour): the BIG crystals (the three on top of the head, the two long wing "
          "crystals at the sides) are BLUE STEEL: main faces #8EA3CB, the narrow side faces darker steel blue #5E6F9C; the SMALL lower side "
          "crystals (one under each wing) are pale SILVER-CYAN steel: main faces #BCD3DA, side faces #86A2AD; the TAIL crystals under the body "
          "are LAVENDER STEEL: main faces #A79FD3, side faces #7570A8; the two tiny crystals on the cheeks pale silver-blue #C9D6EA. The round "
          "BODY, the two little hand nubs and the two little feet are warm milky white #F7F4EC (one flat colour, NOT bluish at the bottom). "
          "The EYES golden yellow #F3C536 with a dark navy ring #2C2A5C; the small ':3' mouth dark navy #2C2A5C.",
          "tinh thể lớn thép lam (#8EA3CB, mặt bên #5E6F9C), tinh thể nhỏ dưới cánh bạc lam nhạt, đuôi thép oải hương; thân trắng sữa; mắt vàng "
          "viền xanh đen"),
    "B": ("sắt rèn đen ánh tím",
          "IRON-CRYSTAL PALETTE B, DARK WROUGHT IRON (each area ONE flat colour): ALL crystals are dark forged IRON: main faces gunmetal grey "
          "#646B7E, the narrow side faces darker iron #3F4455; on the big crystals the thin facet lines are drawn in pale silver #C8CDD8 "
          "instead of ink (only the INNER facet lines; the outline stays dark-brown ink); the TAIL crystals are dark iron with a violet "
          "tint: main faces #6F6890, side faces #4A4566; the two tiny crystals on the cheeks silver #C8CDD8. The round BODY, the hand nubs "
          "and the feet are pale silver-white #EEF0F3 (one flat colour). The EYES amber yellow #F1B936 with a dark ring #24222E; the small "
          "':3' mouth dark #24222E.",
          "mọi tinh thể sắt rèn xám than (#646B7E, mặt bên #3F4455), đường cạnh mặt bạc; đuôi sắt ánh tím; thân trắng bạc; mắt hổ phách"),
    "C": ("bạc + đồng thau",
          "IRON-CRYSTAL PALETTE C, SILVER AND BRASS (each area ONE flat colour): the BIG crystals (three on top, two long wing crystals) are "
          "bright SILVER steel: main faces #B9C1CE, side faces #868FA0; the SMALL lower side crystals and the TAIL crystals are warm BRASS: "
          "main faces #D9AE4E, side faces #A97E2E; the two tiny crystals on the cheeks brass #D9AE4E. The round BODY, the hand nubs and the "
          "feet are ivory #F6F0E2 (one flat colour). The EYES bright yellow #F5CC3A with a dark brown ring #3A2A1E; the small ':3' mouth "
          "dark brown #3A2A1E.",
          "tinh thể lớn bạc thép (#B9C1CE), tinh thể nhỏ + đuôi đồng thau (#D9AE4E); thân ngà; mắt vàng viền nâu"),
}

STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about {{px}} px) running all the way round every piece exactly on its silhouette, thinner ink lines for the inner "
    "structural edges (the FACET edges of every crystal, kept as in image 1 but simplified to a few clean straight lines), and every area "
    "filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. The reference (image 1) is painted in a smooth "
    "digital cel style with soft light and dark planes, white highlights and a bluish shade on the body: do NOT copy that painting style "
    "or its colours: no shading, no highlights, no white shine streaks on the crystals, no gradients, no glow, no shadows, no gloss, no "
    "sparkles: flat colour only. A different tone appears only where a different face (main face / side face) or material is listed. "
    "The only exception: one tiny light dot in each eye.")
BG = "Plain pure-white background (#FFFFFF), no paper grain outside the drawing, no labels, no numbers, no frame, nothing added."


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


def khung_ca_con(atts, cao=780.0):
    """phép đổi toạ độ rig → ảnh 1536 × 1024: cả con cao ~cao px, đặt giữa khung."""
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024."""
    _, imgs, atts = G.nap("att_idle0.json")
    s, cx, cy, T = khung_ca_con(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))            # mỗi part một lớp trong suốt rồi mới chồng
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)
        can.alpha_composite(lay.convert("RGBA"))
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")


MO_TA_CON = (
    "PIECE BY PIECE (as in image 1, seen from the front, facing slightly to the viewer's RIGHT): a round chubby BODY like a soft snowball, "
    "a little wider at the bottom, with a cute face: two big upright oval EYES and a tiny ':3' (omega-shaped) mouth between them, a tiny "
    "square crystal stuck on each cheek; two tiny rounded white HAND nubs at the lower sides of the body and two tiny rounded white FEET "
    "under it. Around the body float NINE separate CRYSTALS, each a chunky faceted gem: three on top of the head (a big one at the upper "
    "left, a smaller one in the middle, a big one at the upper right), one LONG wing-like crystal pointing out to the left and one "
    "pointing out to the right (each sitting behind the body), and one small slim crystal under each wing. Under the body hangs a short "
    "TAIL of three crystals: a small one, a tiny one and a long pointed one. Every crystal keeps its own complete ink outline and its own "
    "facet lines.")


def prompt_concept():
    """lượt concept: vẽ lại cả con gốc (đúng dáng, đúng từng mảnh) bằng chất liệu tinh thể SẮT, màu, nét của mình. Ba hướng màu."""
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, "the REFERENCE creature, 1536x1024, white background: a small round white snowball-like spirit with a cute ':3' face and "
               "yellow oval eyes, surrounded by NINE separate floating faceted crystals (three on its head, two long wing crystals at the "
               "sides, two small ones under them) and a tail of three crystals below. It is painted in a smooth digital cel style with "
               "blue-violet crystals. Keep its SHAPES and its face, change its LOOK.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): cục tròn trắng mặt \":3\", mắt bầu dục vàng, 9 tinh thể lam tím bay quanh "
          "(3 trên đầu, 2 cánh dài, 2 cái nhỏ dưới cánh), đuôi 3 tinh thể. Giữ hình và mặt, đổi chất liệu"),
         (TI_TACH, "an approved hero of our game (a round water blob), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen "
                   "line, its visible crayon hatching and its completely flat colouring. Do NOT copy its design or colours.",
          "Tí Tách đã duyệt (giọt nước tròn, 1536 × 1024, nền trắng): lấy nét bút rung, vân sáp, tô phẳng"),
         (GOLEM, "another approved hero of our game (a rock golem with faceted stone blocks), 1536x1024, white background: see how its hard "
                 "faceted blocks are drawn with flat colour faces and ink edges. Do NOT copy its design or colours.",
          "Golem đá lõi lửa đã duyệt (1536 × 1024, nền trắng): xem cách vẽ khối đá có mặt cạnh bằng màu phẳng + nét mực")]
    hd = ["# Gói GPT: tinh linh tinh thể sắt (tinh_sat), tướng 1 đảo Kim", "",
          "Con gốc của rig: `monster_3346` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng màu (2026-11-15)", "",
          "Người dùng: \"concept như ảnh\", tinh thể là tinh thể SẮT. Ba file, mỗi file một hướng màu; giữ nguyên dáng, mặt, từng mảnh của con gốc.",
          "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, en, vi2) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: RESTYLE. Redraw the creature of image 1 as ONE picture: the SAME creature in the SAME pose, with EVERY piece in the same "
              "place, at the same size, with the same silhouette and the same overlaps (if the new picture were laid over image 1, every "
              "piece must coincide), but with a NEW LOOK: its crystals are now crystals of IRON / STEEL (a metal spirit), new colours and "
              "our hand-drawn drawing style. Keep its cute face exactly (the two big oval eyes, the tiny ':3' mouth). Do not add, remove, "
              "merge or move pieces; keep the white gaps between pieces where image 1 has gaps.", "",
              MO_TA_CON, "", en, "",
              STYLE.format(px="7"), "",
              "CANVAS: landscape 1536x1024, pure-white background, no ground line, no cast shadow; the creature at the same place and size as "
              "in image 1. No sparkles, no glints, no dust, no glow, no speed lines.", BG]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng từng mảnh như ảnh 1 (chồng lên phải trùng); 9 tinh thể + 3 tinh thể đuôi đủ, mỗi cái viền mực riêng; mặt \":3\" "
           "y như con gốc; tinh thể màu sắt đúng bảng, mặt bên tông sẫm hơn; thân một màu phẳng (không ngả xanh ở đáy); nét bút mực rung, vân "
           "sáp, tô phẳng, không bóng, không vệt sáng trắng, không lấp lánh; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the white highlights / shine on the crystals, flat colour only\"; \"the body must be one flat colour, no "
           "blue shade at the bottom\"; \"keep every crystal at the same place and size as in image 1\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


# ---------------------------------------------------------------- lượt 1b: ĐỔI KIỂU DÁNG (người dùng 2026-11-15: "nhìn giống con gốc quá")
# Giữ số mảnh, chỗ, cỡ, hướng, thứ tự chồng của từng mảnh (để lắp lên đúng xương của rig gốc); đổi KIỂU DÁNG mặt, thân, mọi tinh thể.
# Chỗ từng mảnh trên ảnh 1 (L1_A.png, 1536 × 1024) đọc từ hình cả con gốc cùng khung.
CHO_MANH = dict(
    dau_trai="about x = 505 to x = 730, y = 135 to y = 395", dau_giua="about x = 712 to x = 870, y = 220 to y = 410",
    dau_phai="about x = 870 to x = 1062, y = 128 to y = 395", canh_trai="about x = 252 to x = 605, y = 378 to y = 612",
    canh_phai="about x = 1005 to x = 1282, y = 350 to y = 602", nho_trai="about x = 452 to x = 645, y = 635 to y = 742",
    nho_phai="about x = 975 to x = 1152, y = 588 to y = 702", than="about x = 588 to x = 1012, y = 362 to y = 722",
    duoi1="about x = 735 to x = 805, y = 698 to y = 745", duoi2="about x = 735 to x = 842, y = 745 to y = 845",
    duoi3="about x = 848 to x = 1118, y = 752 to y = 892", ma_trai="about x = 603 to x = 668, y = 478 to y = 562",
    ma_phai="about x = 983 to x = 1037, y = 478 to y = 548", mat="about x = 700 to x = 980, y = 420 to y = 535",
    mieng="about x = 805 to x = 908, y = 522 to y = 585")
KIEU = {
    "1": ("lưỡi thép: vương miện ba lưỡi giáo, cánh là hai lưỡi kiếm, đuôi xích + mũi tên, mặt quả quyết",
          ("THE THREE HEAD PIECES ({dau_trai}; {dau_giua}; {dau_phai}): a CROWN of three steel SPEARHEAD BLADES: the left and the right "
           "one are broad leaf-shaped spearheads pointing up and outwards (each with one straight central ridge line and a sharp tip), the "
           "middle one a short triangular blade crest pointing straight up. Blue steel #8EA3CB, the half beyond the ridge line darker "
           "steel #5E6F9C."),
          ("THE TWO WING PIECES ({canh_trai}; {canh_phai}): each becomes a long single-edged SWORD BLADE pointing outwards like a fin: a "
           "straight back edge on top, a curved cutting edge below, a sharp tip at the outer end, one thin groove line (fuller) along "
           "its middle, and a small square GUARD block where it meets the body. Blade #8EA3CB, groove and guard dark iron #4E5568."),
          ("THE TWO SMALL PIECES UNDER THE WINGS ({nho_trai}; {nho_phai}): each becomes a slim KUNAI-like DART pointing down and "
           "outwards, with a small ring at its inner end. Steel #A9B6CF, ring dark iron #4E5568."),
          ("THE TAIL (three separate pieces): the small piece right under the body ({duoi1}) becomes a round iron RING link; the tiny "
           "piece ({duoi2}) becomes a small oval CHAIN link; the long piece ({duoi3}) becomes a broad ARROWHEAD pointing down to the "
           "right with two barbs. Dark iron #5A6072, arrowhead blades #8EA3CB."),
          ("THE CHEEK PIECES ({ma_trai}; {ma_phai}): small round iron RIVETS (a dome with one tiny dot), dark iron #5A6072."),
          ("THE BODY ({than}): the same round chubby body, flat pale steel-white #F1F2F4, with a low curved BELLY BAND of darker grey "
           "#C9CDD6 carrying three small round rivets; the little hand nubs and feet are dark iron #5A6072 like small mittens and boots."),
          ("THE FACE ({mat}; mouth {mieng}): NOT the ':3' face. Two big round EYES, white with a big dark-navy #23264A pupil and one "
           "tiny light dot, each under a short thick angled BROW stroke (inner ends low): a determined, ready-to-fight look; the MOUTH a "
           "small closed confident smile with ONE tiny fang at one corner. Still cute.")),
    "2": ("quặng khối: tinh thể thành cụm khối lập phương (vàng đồng + sắt từ), trán có dấu nam châm, mắt vuông bo",
          ("THE THREE HEAD PIECES ({dau_trai}; {dau_giua}; {dau_phai}): each becomes a little cluster of CUBIC ore crystals (like "
           "pyrite): the left and the right one two or three stacked tilted cubes rising up and outwards, the middle one a single tilted "
           "cube. Each cube shows its top face and side faces as flat areas: brass gold #D9AE4E, side faces #A97E2E."),
          ("THE TWO WING PIECES ({canh_trai}; {canh_phai}): each becomes a row of THREE square iron BLOCKS getting smaller towards the "
           "outer end, stuck together in a slightly rising line (like a stepped arm of cubes). Dark magnetite iron #5B6273, side faces "
           "#3F4455, one tiny brass-gold square at the outer tip."),
          ("THE TWO SMALL PIECES UNDER THE WINGS ({nho_trai}; {nho_phai}): each becomes two small tilted CUBES stuck together, brass gold "
           "#D9AE4E, side faces #A97E2E."),
          ("THE TAIL (three separate pieces): the small piece right under the body ({duoi1}) becomes a small iron cube; the tiny piece "
           "({duoi2}) a smaller brass cube; the long piece ({duoi3}) a long flat iron INGOT bar with a pointed end, pointing down to the "
           "right. Iron #5B6273 / #3F4455, brass #D9AE4E."),
          ("THE CHEEK PIECES ({ma_trai}; {ma_phai}): tiny brass-gold cubes #D9AE4E."),
          ("THE BODY ({than}): the same round chubby body, flat warm light grey #E9E7E2; on the forehead between the head pieces, above the "
           "eyes, a small HORSESHOE MAGNET emblem (red #C8463C with two silver tips #C8CDD8); the hand nubs and feet the body colour."),
          ("THE FACE ({mat}; mouth {mieng}): NOT the ':3' face. Two ROUNDED-SQUARE eyes, amber #F0B23A with a thick dark ring #2A2420 "
           "and one tiny light dot, the top edge of each eye cut flat and slanted (a focused, determined look); the MOUTH a small straight "
           "line with a tiny smirk at one end. Still cute.")),
    "3": ("bismuth bậc thang: tinh thể thành khối bậc thang nhiều dải màu ánh kim, thân sắt sẫm, mắt vàng xếch",
          ("THE THREE HEAD PIECES ({dau_trai}; {dau_giua}; {dau_phai}): each becomes a STEPPED BISMUTH crystal: a spire built of nested "
           "square steps (like a staircase pyramid seen from the side), the left and right spires leaning outwards, the middle one short "
           "and upright. Each step is ONE flat colour band with a clean ink edge, the bands repeating gold #E3B341, magenta-pink #C95C9C, "
           "teal-blue #4F9DB4 (no blending between them)."),
          ("THE TWO WING PIECES ({canh_trai}; {canh_phai}): each becomes a long STEPPED BLADE pointing outwards: its upper and lower "
           "edges go down in small square STAIR steps towards the sharp outer tip; inside, three or four nested stepped bands in the same "
           "flat gold / magenta-pink / teal-blue colours."),
          ("THE TWO SMALL PIECES UNDER THE WINGS ({nho_trai}; {nho_phai}): each a small stepped square crystal, teal-blue #4F9DB4 with "
           "one gold #E3B341 inner step."),
          ("THE TAIL (three separate pieces): the small piece right under the body ({duoi1}) and the tiny piece ({duoi2}) become small "
           "stepped squares (magenta-pink #C95C9C, gold #E3B341); the long piece ({duoi3}) a long stepped point aimed down to the right "
           "with teal-blue, gold and pink bands."),
          ("THE CHEEK PIECES ({ma_trai}; {ma_phai}): tiny stepped squares, gold #E3B341."),
          ("THE BODY ({than}): the same round chubby body but DARK forged IRON, flat charcoal-blue #4A4F5E, with a slightly lighter "
           "round face patch #6A7080 where the eyes and mouth sit; the hand nubs and feet the body colour."),
          ("THE FACE ({mat}; mouth {mieng}): NOT the ':3' face. Two big ALMOND eyes slanted upwards at the outer ends, flat bright yellow "
           "#F5CC3A with a thin dark ring and one tiny light dot, no pupils (like a determined little iron spirit); the MOUTH a small "
           "open grin with a short row of tiny square teeth. Still cute, not scary.")),
}


def prompt_kieu():
    """ba phương án ĐỔI KIỂU DÁNG trên đúng bố cục của concept A (ảnh 1)."""
    mau = os.path.join(G.TAI, "L1_A.png")
    R = [(mau, "the CURRENT picture of our character, 1536x1024, white background: a round chubby spirit with a ':3' face, nine floating "
               "iron crystals around it (three on the head, two long wing crystals at the sides, two small ones under them) and a tail "
               "of three crystals below. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours. It looks too much like "
               "an existing design: REDESIGN its pieces.",
          "Concept A hiện tại (1536 × 1024, nền trắng): thân tròn mặt \":3\", 9 tinh thể sắt + đuôi 3 tinh thể. Giữ bố cục, đổi kiểu dáng"),
         (TI_TACH, "an approved hero of our game, 1536x1024, white background: match its wobbly dark-brown pen line, its visible crayon "
                   "hatching and its completely flat colouring. Do NOT copy its design.",
          "Tí Tách đã duyệt: lấy nét bút, vân sáp, tô phẳng")]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1b")[0].rstrip("\n")
    gd = ["", "## Lượt 1b: ĐỔI KIỂU DÁNG (2026-11-15; người dùng: \"nhìn giống con gốc quá\")", "",
          "Ba phương án, mỗi phương án một file. Giữ số mảnh, chỗ, cỡ, hướng, thứ tự chồng (để lắp lên đúng xương của rig); đổi kiểu dáng mặt, "
          "thân, mọi tinh thể.", "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += [""]
    for k, (vi, *manh) in KIEU.items():
        out, save = luu(f"L2_{k}")
        p = os.path.join(GUI, f"luot_1b_kieu_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: REDESIGN the character of image 1 so that it no longer looks like the design it was based on. Draw ONE picture of a "
              "NEW little iron spirit that keeps ONLY the LAYOUT of image 1: the same number of separate pieces, each piece in the SAME "
              "PLACE, covering about the SAME AREA (not much bigger, not much smaller), pointing in the SAME DIRECTION, with the same "
              "overlaps (the wing pieces and the small under-wing pieces sit BEHIND the body, the head pieces in front of the top of the "
              "body, the tail pieces float separately below). Every piece gets a NEW SHAPE and NEW details as described; do not just "
              "repaint the old shapes. Each piece keeps its own complete ink outline. Coordinates are pixels on the 1536x1024 canvas.", ""]
        t += [m.format(**CHO_MANH) for m in manh]
        t += ["",
              f"DRAWING STYLE: hand-drawn on paper like image 2: a wobbly dark-brown ink outline ({MUC}, about 7 px) round every piece, "
              "thinner ink lines for inner edges, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No "
              "shading, no highlights, no gradients, no glow, no shadows, no shine, no sparkles. Chunky, simple, readable shapes; a cute "
              "but determined little fighter (a first-stage Pokemon-like creature), not a smiling mascot, not scary.", "",
              "CANVAS: landscape 1536x1024, pure-white background, no ground line, no cast shadow, the character at the same place and size "
              "as in image 1. No sparks, no dust, no speed lines.", BG]
        ghi(p, t)
        gd += [f"- **Phương án {k}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    gd += ["", "Kiểm: đủ mảnh, đúng chỗ, gần đúng cỡ, đúng hướng mảnh cũ (để lắp lại lên cùng xương); kiểu dáng mới, không còn mặt \":3\"; tô phẳng, "
           "không bóng, không phát sáng; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- lượt 1c: SỬA NHẸ trên concept A (người dùng: lượt 1b "xấu quá, giữ dạng tinh
# thể như vừa rồi, sửa khác đi chút thôi"). Giữ bố cục, thân, màu thép lam, kiểu tinh thể mài cạnh; chỉ đổi vài chi tiết.
SUA = {
    "1": ("mặt quả quyết + tinh thể nhọn hơn",
          ["THE FACE: keep the two golden-yellow oval eyes with their dark navy ring and tiny light dot, but add a short thick dark-navy "
           "BROW stroke above each eye, slanted down towards the middle (a determined, ready-to-fight look); replace the ':3' mouth by a "
           "small closed confident smile with ONE tiny white fang at its right corner.",
           "EVERY CRYSTAL a little SHARPER: keep its base, its place, its direction and its faceted look, but make its outer tip longer and "
           "more pointed (about 15 % longer) with clean straight facet lines; the two long wing crystals end in a sharp point.",
           "THE TWO TINY SQUARE CHEEK CRYSTALS become tiny four-pointed iron STAR studs, same place and size, pale silver-blue #C9D6EA."]),
    "2": ("đai sắt ôm gốc tinh thể + mắt nheo quyết tâm",
          ["THE FIVE BIG CRYSTALS (three on the head, two wing crystals): each gets a narrow dark iron CLAMP BAND (#4E5568, two tiny round "
           "rivets on it) wrapped around its BASE, the end nearest the body, like a gem set in an iron mount. The crystal itself keeps its "
           "shape and colours.",
           "THE FACE: keep the golden-yellow oval eyes but give each a flat dark-navy UPPER LID line cutting off the top of the eye, slanted "
           "down towards the middle (focused, determined); replace the ':3' mouth by a small straight mouth with ONE tiny white fang.",
           "THE TWO TINY SQUARE CHEEK CRYSTALS become tiny round iron RIVETS (#4E5568), same place and size."]),
    "3": ("tinh thể mọc đôi + mắt mèo",
          ["THE BIG CRYSTALS: next to each of the three head crystals and each of the two wing crystals grows ONE small secondary crystal "
           "bud (about one third of its size, same faceted style and colours) from its side near the base, pointing a little away from "
           "it, like a twin crystal. The middle head crystal becomes a little taller with a double point.",
           "THE FACE: keep the golden-yellow oval eyes with the dark navy ring, but add a thin vertical dark-navy slit PUPIL in each eye "
           "(cat-like, alert); replace the ':3' mouth by a small open smile showing ONE tiny white fang.",
           "THE TAIL: the long tail crystal gets a second, smaller point beside its tip (a forked tip)."]),
}


def prompt_sua():
    mau = os.path.join(G.TAI, "L1_A.png")
    R = [(mau, "the CURRENT picture of our character, 1536x1024, white background: a round chubby cream spirit with yellow oval eyes and a "
               "':3' mouth, nine floating faceted blue-steel iron crystals around it (three on the head, two long wing crystals at the "
               "sides, two small pale ones under them) and a tail of three lavender-steel crystals below. Hand-drawn: wobbly dark-brown "
               "ink line, crayon hatching, flat colours.",
          "Concept A hiện tại (1536 × 1024, nền trắng): thân kem, mắt bầu dục vàng, miệng \":3\", 9 tinh thể thép lam + đuôi 3 tinh thể")]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1c")[0].rstrip("\n")
    gd = ["", "## Lượt 1c: SỬA NHẸ concept A (2026-11-15; người dùng chê lượt 1b: \"xấu quá, giữ dạng tinh thể như vừa rồi, sửa khác đi chút thôi\")",
          "", f"Ba phương án, mỗi phương án một file. Ảnh mẫu duy nhất (ảnh 1) = `{Wp(mau)}`: concept A (thân kem, mắt vàng, 9 tinh thể thép lam, "
          "đuôi 3 tinh thể oải hương). Giữ bố cục, thân, màu, kiểu tinh thể mài cạnh; chỉ đổi mặt và vài chi tiết.", ""]
    for k, (vi, doi) in SUA.items():
        out, save = luu(f"L3_{k}")
        p = os.path.join(GUI, f"luot_1c_sua_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: a SMALL EDIT of image 1. Draw ONE picture of the SAME character, in the SAME pose, at the same place and size on the "
              "canvas, with ONLY the changes listed under CHANGE.", "",
              "KEEP IDENTICAL (if the new picture were laid over image 1, all of this must coincide): the round cream body and its outline, "
              "the little hand nubs and feet, the number of crystals and the place, size, direction and overlap of every crystal, their "
              "chunky FACETED gem style with flat blue-steel faces and darker side faces, the colours (body cream, crystals blue steel "
              "#8EA3CB / #5E6F9C, small under-wing crystals pale silver-cyan, tail crystals lavender steel), the eye colour, the drawing "
              "style (wobbly dark-brown ink outline, crayon hatching, completely flat colour, no shading, no highlights, no glow).", "",
              "CHANGE (only this):"] + [f"- {d}" for d in doi] + ["",
              "Cute but determined little fighter, not a smiling mascot, not scary. Plain pure-white background, no ground line, no cast "
              "shadow, no sparkles, no labels."]
        ghi(p, t)
        gd += [f"- **Phương án {k}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    gd += ["", "Kiểm: mọi thứ ngoài phần CHANGE trùng ảnh 1; tô phẳng, không bóng; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- lượt 2: đổi da theo khung part (cần L1_duyet.png = concept đã chọn)
RES = 3                                              # ảnh mảnh của mình lưu ở cỡ ảnh vùng gốc × RES
TO = {
    "P": [[("body", 3.3), ("bin9", 3.3), ("bin3", 3.3)], [("bin6", 3.3), ("bin2", 3.3)]],
    "Q": [[("tail3", 4.2), ("bin1", 4.2), ("bin8", 4.2), ("bin7", 4.2)], [("tail2", 4.2), ("weitail1", 4.2), ("bin5", 4.2), ("bin4", 4.2)]],
    "R": [[("eyes", 4.6), ("biyan", 4.6), ("yun", 4.6)], [("mt", 4.6), ("youshou", 4.6), ("zuoshou", 4.6), ("youjiao", 4.6), ("zuojiao", 4.6)]],
}
NHOM_TT = {"lon": ("bin1", "bin2", "bin3", "bin6", "bin9"), "nho": ("bin7", "bin8"), "duoi": ("tail2", "tail3", "weitail1"), "ma": ("bin4", "bin5")}
# bảng màu từng hướng: (mặt chính, mặt bên) theo nhóm tinh thể; thân; mắt (lòng, viền); nét cạnh mặt trong
BANG = {
    "A": dict(lon=("#8EA3CB", "#5E6F9C"), nho=("#BCD3DA", "#86A2AD"), duoi=("#A79FD3", "#7570A8"), ma=("#C9D6EA", "#C9D6EA"),
              than="#F7F4EC", mat=("#F3C536", "#2C2A5C"), canh="thin dark-brown ink"),
    "B": dict(lon=("#646B7E", "#3F4455"), nho=("#646B7E", "#3F4455"), duoi=("#6F6890", "#4A4566"), ma=("#C8CDD8", "#C8CDD8"),
              than="#EEF0F3", mat=("#F1B936", "#24222E"), canh="thin pale silver (#C8CDD8)"),
    "C": dict(lon=("#B9C1CE", "#868FA0"), nho=("#D9AE4E", "#A97E2E"), duoi=("#D9AE4E", "#A97E2E"), ma=("#D9AE4E", "#D9AE4E"),
              than="#F6F0E2", mat=("#F5CC3A", "#3A2A1E"), canh="thin dark-brown ink"),
}
TEN_TT = {"bin1": "the SMALL CRYSTAL on the middle of the head", "bin2": "the LONG WING CRYSTAL at the left", "bin3": "the BIG CRYSTAL on the "
          "upper left of the head", "bin6": "the LONG WING CRYSTAL at the right", "bin9": "the BIG CRYSTAL on the upper right of the head",
          "bin7": "the SMALL SLIM CRYSTAL under the left wing", "bin8": "the SMALL SLIM CRYSTAL under the right wing",
          "tail2": "the TINY TAIL CRYSTAL", "tail3": "the LONG POINTED TAIL CRYSTAL", "weitail1": "the SMALL TAIL CRYSTAL right under the body",
          "bin4": "the TINY SQUARE CRYSTAL on the right cheek", "bin5": "the TINY SQUARE CRYSTAL on the left cheek"}
VI_TO = {"P": "thân tròn, hai tinh thể lớn trên đầu, hai tinh thể cánh dài",
         "Q": "tinh thể đuôi dài, tinh thể giữa đầu, hai tinh thể nhỏ dưới cánh; tinh thể đuôi nhỏ, tí hon, hai tinh thể má",
         "R": "mắt mở (một ảnh hai mắt), mắt nhắm > <, mắt choáng; miệng :3, hai tay, hai chân"}
SO_PART = {"P": "five parts in two rows: a big round body, two big chunky crystals; two long wing crystals",
           "Q": "eight crystals in two rows, from long to tiny",
           "R": "eight small parts in two rows: a pair of open eyes, a pair of closed eyes, a pair of dizzy eyes; a tiny mouth, two little "
                "hand nubs, two little feet"}


def zs():
    """tỉ lệ ảnh mảnh của mình so với ảnh vùng gốc (cho rig)."""
    return {r: RES for h in TO.values() for hang in h for r, _ in hang}


def vung():
    """{ảnh vùng: (hình, ảnh part gốc cắt theo lưới)} mọi ảnh vùng, kể cả mắt nhắm / choáng."""
    G.H._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in sorted(D["atts"], key=lambda q: (not q["cur"], q["order"])):
        r = a.get("region")
        if r in imgs and r not in out and a["slot"] != "shadow":
            out[r] = (a, G.part_goc(a))
    return out


def to_goc():
    V = vung()
    O = {}
    thieu = set(V) - {r for hang in TO.values() for h_ in hang for r, _ in h_}
    if thieu:
        print("ảnh vùng CHƯA xếp vào tờ nào:", sorted(thieu))
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o, cao = {}, []
        for h_ in hang:
            cs = [(r, z, V[r][1], int(round(V[r][1].width * z)), int(round(V[r][1].height * z))) for r, z in h_]
            cao.append((cs, max(c[4] for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        if ke_y < 30:
            raise SystemExit(f"tờ {ma}: quá cao ({sum(c[1] for c in cao)} px)")
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3] for c in cs)) // (len(cs) + 1)
            if ke < 30:
                raise SystemExit(f"tờ {ma}: hàng quá rộng ({sum(c[3] for c in cs)} px)")
            x = ke
            for r, z, im, cw, ch in cs:
                y0 = y + (hh - ch) // 2
                can.alpha_composite(im.resize((cw, ch), Image.LANCZOS), (x, y0))
                o[r] = dict(hop=[x, y0, cw, ch], z=z)
                x += cw + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    return O


def mo_ta(r, B):
    if r == "body":
        return (f"the round BODY, a soft snowball shape: ONE flat colour {B['than']} all over, outline in ink; the bluish shade and the white "
                "highlight of the reference become that same flat colour (no shade at all). No face on it (the face is a separate part).")
    if r == "eyes":
        return (f"a PAIR of big upright oval EYES side by side (one part): each eye flat golden {B['mat'][0]} with a thick dark ring "
                f"{B['mat'][1]} and ONE tiny light dot near its top; nothing else.")
    if r == "biyan":
        return f"a PAIR of tightly CLOSED eyes drawn as '>' and '<' marks (the same places as in the reference): bold strokes {B['mat'][1]}."
    if r == "yun":
        return f"a PAIR of DIZZY spiral eyes (the same places as in the reference): bold spiral strokes {B['mat'][1]}."
    if r == "mt":
        return f"a tiny ':3' (omega-shaped) MOUTH line: one bold stroke {B['mat'][1]}."
    if r in ("youshou", "zuoshou", "youjiao", "zuojiao"):
        ten_ = {"youshou": "HAND nub (the right one)", "zuoshou": "HAND nub (the left one)", "youjiao": "FOOT (the right one)",
                "zuojiao": "FOOT (the left one)"}[r]
        return (f"a little rounded {ten_}: flat body colour {B['than']}. Ink line ONLY where the reference part has its dark line (the outer "
                "rounded edge); the edge that tucks under the body has NO ink line at all (it stays soft, in the body colour), exactly like "
                "the reference part.")
    nh = next(k for k, v in NHOM_TT.items() if r in v)
    c1, c2 = B[nh]
    if nh == "ma":
        return f"{TEN_TT[r]}: a tiny square iron crystal, ONE flat colour {c1}, ink outline."
    return (f"{TEN_TT[r]}: a chunky faceted IRON crystal; keep its exact silhouette and its main facet edges (simplified to a few straight "
            f"{B['canh']} lines); main faces flat {c1}, the narrow side faces flat {c2}; no highlight, no shine streak, no gradient.")


CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of the separate PARTS of a 2D animation puppet (a little round snowball spirit with floating "
    "crystals), each part drawn alone on white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can "
    "be put back on the same puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its "
    "place on the sheet (if the new picture were laid over image 1, every part must coincide with the old one), and its main structural "
    "lines (the facet edges of the crystals, the strokes of the eyes and the mouth). Do NOT merge parts, do NOT add parts, do NOT move, "
    "rotate or resize parts. Pure white (#FFFFFF) between the parts.")


def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


def prompt_da(O, k):
    if not os.path.exists(CONCEPT):
        raise SystemExit("chưa có concept đã chọn " + Wp(CONCEPT))
    B = BANG[k]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", f"## Lượt 2: đổi da theo khung từng part, hướng màu {k} (2026-11-15)", "",
          "Ba tờ P, Q, R là các mảnh GỐC cắt ra từ rig (phóng to); GPT vẽ lại da đúng chỗ, đúng cỡ, đúng hình bóng từng mảnh. Ảnh mảnh gốc là của "
          "game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai.", ""]
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out, save = luu(f"D_{ma}")
        p = os.path.join(GUI, f"luot_2_da_{ma}.txt")
        R = [(mau, f"the PARTS SHEET, 1536x1024, white background: separate parts of the puppet, each drawn alone, at the exact size and "
                   f"place to keep ({SO_PART[ma]}). Painted in a smooth digital cel style with blue-violet crystals: keep the shapes, change "
                   "the look.",
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng {min(z for h_ in TO[ma] for _, z in h_)}–"
              f"{max(z for h_ in TO[ma] for _, z in h_)} lần: {VI_TO[ma]}. Hình cel số màu lam tím"),
             (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: the same spirit redrawn with IRON crystals in "
                       "our hand-drawn style. Take from it the exact colours, the material of each piece and the hand-drawn look (wobbly "
                       "brown ink line, crayon hatching, flat colour).",
              "Concept đã chọn (1536 × 1024, nền trắng): lấy màu, chất liệu từng mảnh, nét vẽ tay")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        st = STYLE.format(px="8").replace("images 2 and 3", "image 2").replace("The reference (image 1)", "The parts sheet (image 1)")
        t += [""] + save + ["", CHUNG, "", st, "", "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        t += [f"{i}. ({cho(o, r)}) {mo_ta(r, B)}" for i, r in enumerate(o, 1)]
        t += ["", BG]
        ghi(p, t)
        gd += [f"- **`{ma}`** ({VI_TO[ma]}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…). Ảnh mẫu 1 = "
               f"`{Wp(mau)}` (tờ mảnh gốc), ảnh mẫu 2 = `{Wp(CONCEPT)}` (concept đã chọn)."]
        print(p)
    gd += ["", "Kiểm từng tờ: mỗi mảnh trùng hình bóng, chỗ, cỡ với tờ mảnh gốc (Claude đo IoU bằng `tinh_sat_da.py cat`, đích ≥ 0,9); màu đúng "
           "bảng của concept; tô phẳng, không bóng, không vệt sáng; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt (như dat_nung_da.cat)
def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def cat(chi=None):
    import dat_nung_da as DN
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pi = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pi)) if os.path.exists(pi) else {}
    for ma in TO:
        if chi and ma not in chi:
            continue
        fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(f"D_{ma}") and f.endswith(".png")],
                    key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
        if not fs:
            print(f"tờ {ma}: chưa gen")
            continue
        src = os.path.join(G.TAI, fs[-1])
        A = DN.doc(src)
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg, fgG = ~DN.nen(A), Gd.min(2) < 238
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        so = []
        print(f"tờ {ma} ({os.path.basename(src)}):")
        for r, d in o.items():
            im, mm = DN.o_ra(A, lab, st, fgG, d)
            x, y, cw, ch = d["hop"]
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            a2 = np.asarray(im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            a2[..., 3] = np.where(cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool), a2[..., 3], 0)      # giữ trong hình bóng gốc nới 3 px
            b = fgG[y:y + ch, x:x + cw]
            iou = float((mm & b).sum()) / max(1, (mm | b).sum())
            if r in ious and ious[r] > iou + 0.01 and os.path.exists(os.path.join(MANH, r + ".png")):
                print(f"  {r:10s} IoU {iou:.3f} (giữ bản cũ {ious[r]:.3f})")
                continue
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            ious[r] = round(iou, 3)
            vis = np.full((ch, cw, 3), 255, np.uint8)
            vis[mm & b] = (170, 170, 170)
            vis[b & ~mm] = (230, 60, 60)
            vis[mm & ~b] = (60, 190, 60)
            so.append((Image.fromarray(vis), Image.fromarray(a2, "RGBA")))
            print(f"  {r:10s} IoU {iou:.3f}" + ("   <-- THẤP" if iou < 0.9 else ""))
        if so:
            DN.to_so(so, os.path.join(MANH, f"_so_{ma}.png"))
    json.dump(ious, open(pi, "w"), indent=1)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    elif cmd == "kieu":
        prompt_kieu()
    elif cmd == "sua":
        prompt_sua()
    elif cmd == "to":
        O = to_goc()
        if len(sys.argv) > 2:
            prompt_da(O, sys.argv[2])
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    else:
        print(__doc__)
