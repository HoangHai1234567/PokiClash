# -*- coding: utf-8 -*-
"""Chiến binh sắt (chien_sat, rig monster_3348): concept THEO CON GỐC (hiệp sĩ băng khiên + giáo), đổi sang chất liệu SẮT, bỏ bông tuyết.

    chien_sat_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/chien_sat_1/mau/goc_ca_con.png (+ .json: khung từng part)
    chien_sat_da.py concept    ba file prompt concept (ba hướng) → gui_gpt/chien_sat_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chien_sat as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "chien_sat_1")
CUNG_LUA = os.path.join(HERE, "inbox", "cung_lua_1", "mau", "concept_A.png")
TINH_SAT = os.path.join(HERE, "inbox", "tinh_sat_1", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"


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


def khung_ca_con(atts, cao=800.0):
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
        print(k, v)


MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: a small chubby armoured knight seen from the front, turned slightly to the viewer's RIGHT, standing "
    "on two short legs): a big round closed HELMET (a dark round back part, a pale metal FACE-PLATE with vertical eye slits on its "
    "right side and a round disc on its left side), a big curved CREST on top of the helmet sweeping up and back to the left; a big "
    "kite-shaped SHIELD held in front of the body on the viewer's LEFT, covering the left half of the body down to the feet; a narrow "
    "cloth TABARD hanging down the middle of the chest under the helmet; small shoulder plates, a small chest plate and a short "
    "armoured skirt; a dark under-suit at the neck, the upper arm and the thighs; short armoured shins and boots; on the viewer's "
    "RIGHT the near arm holds a LONG SPEAR upright: the fist with a little cuff round the wrist grips the shaft just under the "
    "spearhead collar, the big pointed SPEARHEAD stands above the fist up to the height of the crest, the thin shaft goes down to a "
    "small pointed butt cap near the ground.")

# ba hướng (Claude đề xuất, chờ người dùng chọn). Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("thép xám + đỏ thẫm (giữ dáng gốc nhất)",
          "mọi mảnh giữ hình bóng; mào thành chùm lông ngựa đỏ thẫm cùng dáng quạt; khiên thép, bỏ bông tuyết thay bằng núm sắt tròn "
          "4 đinh tán; vạt áo đỏ trơn; mũi giáo sắt hình lá; búp lông trắng thành tua đỏ; khe mặt nạ tối",
          ["ARMOUR (helmet face-plate, the disc, shoulder plates, chest plate, skirt, shins, boots, the fist): plain forged STEEL, "
           "main faces flat steel grey #9EA6B2, the faces turned away darker steel #6E7684, rims and edges the same steel (no white "
           "rims, no blue); the round BACK of the helmet dark iron #4C525E; the under-suit near-black #24262C.",
           "EYE SLITS of the face-plate: flat dark charcoal #2A2D33 inside (no cyan, no glow), same number, place and shape.",
           "CREST: the SAME curved fan shape, place and size, but made of stiff CRIMSON HORSEHAIR: flat red #C2403A with a darker red "
           "#8A2B2A band along its inner (lower) edge, a few thin ink strand lines following the curve, its outer edge slightly "
           "brushy; it grows from a small dark iron crest holder on top of the helmet.",
           "SHIELD: the SAME kite shape, place, size and thickness, plain STEEL: the raised border frame round the front face keeps "
           "its shape but is light steel #B6BDC7, the inner field inside the frame #7F8896, its thick side edge darker #646C79, the "
           "top band (cyan glass in image 1) becomes a plain steel band #9EA6B2. NO SNOWFLAKE: in the middle of the front face "
           "only one round raised iron BOSS (dark iron #4C525E, one ring line) with four small round rivets around it. Nothing else "
           "on the shield.",
           "TABARD: the SAME narrow cloth strip, flat crimson #B8383A with one dark iron #4C525E band near its bottom edge. NO "
           "snowflake, no emblem.",
           "SPEAR: the big crystal spearhead becomes a forged IRON spearhead of the SAME length, place and outline: a long leaf-"
           "shaped blade with ONE straight central ridge line, the half on one side of the ridge #AEB5C0, the other half #7C8491, "
           "a short dark iron collar under it; the white fluffy tuft under the collar becomes a short RED TASSEL #C2403A (same place, "
           "same size); the shaft dark iron #4C525E; the crystal butt cap becomes a small pointed iron cap #7C8491.",
           "WRIST CUFF: the white fluffy cuff becomes a red cloth wrap #C2403A of the same size."]),
    "B": ("gang sẫm + đồng thau (mào thành lưỡi thép)",
          "giáp gang xám sẫm viền đồng thau; mào ĐỔI DÁNG thành ba bản thép cong xếp lớp (cùng chỗ, cùng cỡ); khiên gang viền đồng, "
          "hình mũi giáo đồng thau nổi ở giữa; vạt áo xanh than viền đồng; khe mặt nạ màu hổ phách; mũi giáo thép, khâu đồng",
          ["ARMOUR (helmet face-plate, the disc, shoulder plates, chest plate, skirt, shins, boots, the fist): dark GUNMETAL iron, main "
           "faces #646C7B, faces turned away #474E5B; the rims of the face-plate, the disc, the shoulder plates and the skirt are a "
           "thin BRASS trim #C99A3E (one narrow band, no rivets everywhere); the round BACK of the helmet darker iron #3C424D; the "
           "under-suit near-black #24262C.",
           "EYE SLITS of the face-plate: flat AMBER #F0B23A inside (flat colour, no glow), same number, place and shape.",
           "CREST: a NEW SHAPE in the SAME place, covering about the same area and sweeping up and back to the left like the old one: "
           "THREE overlapping curved STEEL PLATES like the blades of a fan or the feathers of a metal wing, each a long curved blade "
           "with a rounded back and a pointed tip, the front one longest; plates steel #A7AFBA with the inner edge of each plate "
           "darker #6E7684, held by a small brass crest holder #C99A3E on top of the helmet. No feathers, no hair.",
           "SHIELD: the SAME kite shape, place, size and thickness: front face dark gunmetal #565E6C, its thick side edge #3C424D, a "
           "brass rim #C99A3E round the front face, the top band (cyan glass in image 1) becomes a brass band. NO SNOWFLAKE: in the "
           "middle only one big raised SPEARHEAD emblem pointing up, flat brass #C99A3E with one central ridge line. Nothing else.",
           "TABARD: the SAME narrow cloth strip, flat dark navy #34406A with a brass #C99A3E band at its bottom edge. NO snowflake, no "
           "emblem.",
           "SPEAR: the big crystal spearhead becomes a forged STEEL spearhead of the SAME length, place and outline (long leaf-shaped "
           "blade, ONE central ridge line, one half #B3BAC4, the other half #7C8491); the white fluffy tuft under it becomes a short "
           "brass COLLAR ring #C99A3E (same place); the shaft dark iron #3C424D; the butt cap a small pointed brass cap #C99A3E.",
           "WRIST CUFF: the white fluffy cuff becomes a plain brass cuff ring #C99A3E of the same size."]),
    "C": ("bạc sáng + đồng đỏ (mào chùm kim sắt)",
          "giáp bạc sáng, chi tiết sắt sẫm; mào ĐỔI DÁNG thành chùm 5 cây kim sắt dài xoè quạt (gợi chiêu kim sắt); khiên sắt sẫm viền "
          "bạc, giữa là ba cây kim xoè lên; vạt áo đồng đỏ; tua giáo đồng đỏ; khe mặt nạ tối",
          ["ARMOUR (helmet face-plate, the disc, shoulder plates, chest plate, skirt, shins, boots, the fist): bright polished SILVER "
           "steel, main faces flat #C3CAD3, faces turned away #8C95A2 (flat colours, no shine marks); the round BACK of the helmet "
           "dark iron #4A505B; the under-suit near-black #24262C.",
           "EYE SLITS of the face-plate: flat dark charcoal #2A2D33 inside (no cyan, no glow), same number, place and shape.",
           "CREST: a NEW SHAPE in the SAME place, covering about the same area and sweeping up and back to the left like the old one: "
           "a fan of FIVE long slim iron NEEDLES (long thin spikes with sharp tips) spreading from one dark iron crest holder on top "
           "of the helmet, the front needle longest, the needles close together like the ribs of a half-open fan, each with its own "
           "ink outline; needles dark iron #5A616E with one thin lighter line #9AA2AE along each.",
           "SHIELD: the SAME kite shape, place, size and thickness: front face dark iron #565D69, its thick side edge #3E444F, a "
           "silver rim #C3CAD3 round the front face, the top band (cyan glass in image 1) becomes a silver band. NO SNOWFLAKE: in the "
           "middle only a simple emblem of THREE silver needles #C3CAD3 fanning upward from one point near the bottom. Nothing else.",
           "TABARD: the SAME narrow cloth strip, flat copper-red #B5562F with one dark iron #4A505B band near its bottom edge. NO "
           "snowflake, no emblem.",
           "SPEAR: the big crystal spearhead becomes a forged IRON spearhead of the SAME length, place and outline (long narrow "
           "needle-like leaf blade, ONE central ridge line, one half #C3CAD3, the other half #8C95A2); the white fluffy tuft under it "
           "becomes a short copper-red TASSEL #B5562F (same place, same size); the shaft dark iron #4A505B; the butt cap a small "
           "pointed iron cap #8C95A2.",
           "WRIST CUFF: the white fluffy cuff becomes a copper-red cloth wrap #B5562F of the same size."]),
}

STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) for the "
    "few inner structural edges (the edge between the front face and the side face of a plate, the eye slits, the ridge of the "
    "spearhead), and every area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. Image 1 is painted in a "
    "smooth digital cel style with soft light and dark planes and white highlights: do NOT copy that painting style or its icy colours: "
    "no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows, no gloss, no sparkles: flat colour only. A "
    "different tone appears only where a different face (front face / side face) or material is listed. VERY SIMPLE DESIGN, FEW "
    "DETAILS: no extra rivets, engravings, scratches, dents, chains, belts, badges or patterns beyond what is listed.")


def prompt_concept():
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, "the REFERENCE character, 1536x1024, white background: a small chubby ICE knight with a big round closed helmet (pale "
               "face-plate with glowing cyan eye slits), a big white-and-blue feather crest, a big kite shield with a SNOWFLAKE emblem "
               "on the viewer's left, a narrow white tabard with a snowflake, and a long spear with a cyan ice-crystal spearhead held "
               "upright on the viewer's right. It is painted in a smooth digital cel style with icy blue colours. Keep its POSE, its "
               "PIECES and their PLACES, change its LOOK.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): hiệp sĩ băng mũ tròn kín, mặt nạ khe xanh băng, mào lông trắng lam, "
          "khiên bông tuyết bên trái, vạt áo trắng bông tuyết, giáo mũi tinh thể băng cầm dựng bên phải. Giữ dáng và từng mảnh, đổi "
          "chất liệu"),
         (CUNG_LUA, "an approved hero of our game (a chubby armoured knight archer), 1536x1024, white background: match EXACTLY its "
                    "wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring of armour plates. Do "
                    "NOT copy its design, horns, flames or colours.",
          "Quỷ lửa bắn cung đã duyệt (hiệp sĩ giáp mũ tròn, 1536 × 1024, nền trắng): lấy nét bút rung, vân sáp, cách tô giáp phẳng"),
         (TINH_SAT, "another approved hero of our game from the same metal island (a little iron-crystal spirit), 1536x1024, white "
                    "background: see how flat steel faces and darker side faces are drawn. Do NOT copy its design.",
          "Tinh linh tinh thể sắt (tướng 1 đảo Kim) đã duyệt: xem cách tô mặt thép phẳng + mặt bên sẫm")]
    hd = ["# Gói GPT: chiến binh sắt (chien_sat), tướng 2 đảo Kim", "",
          "Con gốc của rig: `monster_3348` (hiệp sĩ băng khiên + giáo, game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, "
          "không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng (2026-11-16)", "",
          "Người dùng: \"concept chiến binh sắt, bỏ icon bông tuyết đi\". Ba file, mỗi file một hướng; giữ dáng đứng, chỗ và cỡ từng mảnh "
          "của con gốc (để lắp lên đúng xương), đổi chất liệu sang sắt. A giữ hình bóng mọi mảnh; B, C đổi dáng cái mào (mảnh làm nên "
          "bóng dáng) để khỏi giống con gốc.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: RESTYLE. Redraw the knight of image 1 as ONE picture of an IRON WARRIOR: the SAME character in the SAME pose, with "
              "EVERY piece in the same place, at the same size, with the same silhouette and the same overlaps (if the new picture were "
              "laid over image 1, every piece must coincide), except the pieces whose new shape is described below; new materials "
              "(forged iron and steel instead of ice), new colours and our hand-drawn drawing style. Do not add, remove, merge or move "
              "pieces. The SNOWFLAKE emblems are removed everywhere.", "",
              MO_TA_CON, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a sturdy, determined little iron warrior ready to fight (a game hero), not a cute mascot, not scary. The near leg, "
              "the far leg and the arm must stay attached to the body exactly as in image 1.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng từng mảnh như ảnh 1 (chồng lên phải trùng, trừ cái mào ở B, C); không còn bông tuyết ở khiên và vạt áo; "
           "khe mặt nạ không phát sáng; mũi giáo sắt dài bằng mũi tinh thể cũ; tay cầm giáo, hai chân dính thân; nét bút mực rung, vân sáp, "
           "tô phẳng, không bóng, không vệt sáng trắng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the white highlights / shine on the armour, flat colour only\"; \"remove the snowflake, keep only the "
           "listed emblem\"; \"keep every piece at the same place and size as in image 1\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


# ================================================================ lượt 2: ĐỔI DA THEO KHUNG PART (concept A đã duyệt: tai_ve/L1_duyet.png)
# Tờ hướng dẫn = CHÍNH CÁC MẢNH GỐC cắt theo lưới (phóng 2,3–5,5 lần); GPT chỉ đổi da theo concept, giữ hình bóng, cỡ, chỗ, đường cấu trúc
# (skill pokiclash-spine-rig mục 23, memory reskin-theo-part-goc). Giáo (64 × 310) đặt NẰM NGANG trên tờ (mũi chĩa phải), cắt xong xoay lại.
import cv2  # noqa: E402

RES = 2                      # ảnh mảnh của mình = ảnh vùng của họ × RES
MANH = os.path.join(G.BASE, "manh")
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
# tờ → các hàng [(vùng, phóng, xoay)]; xoay 90 = quay theo chiều kim đồng hồ (đỉnh ảnh vùng chĩa sang phải)
TO = {
    "A": [[("guan_01", 2.5, 0), ("hujing_01", 2.5, 0), ("tou_01", 2.5, 0)],
          [("dun_01", 2.5, 0), ("qizi_01", 2.5, 0), ("wuqi_01", 2.3, 90)]],
    "B": [[("st_01", 4.0, 0), ("qunbai_01", 4.0, 0), ("hujian_l_01", 4.0, 0), ("hujian_r_01", 4.0, 0), ("xiaobi_r_02", 4.0, 0)],
          [("xiaotui_l_01", 4.0, 0), ("xiaotui_r_01", 4.0, 0), ("datui_l_01", 4.0, 0), ("datui_r_01", 4.0, 0), ("dang_01", 4.0, 0),
           ("dabi_r_01", 4.0, 0), ("bozi_01", 4.0, 0)],
          [("xiaobi_r_01", 5.5, 0), ("sizhi_01", 5.5, 0), ("damz_01", 5.5, 0)]],
}
PX = {"A": "6", "B": "9 (about 12 on the three hand pieces of the bottom row)"}

CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of the separate body PARTS of a 2D animation puppet (a chubby armoured knight with a shield and a "
    "spear), each part drawn alone on white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be "
    "put back on the same puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place "
    "on the sheet (if the new picture were laid over image 1, every part must coincide with the old one), and its main structural lines "
    "(plate edges, the frame of the shield, the eye slits, the edge between a front face and a side face). Do NOT merge parts, do NOT add "
    "parts, do NOT move parts. Pure white (#FFFFFF) between the parts.")
STYLE2 = (
    "NEW LOOK (the same for all parts; see image 2, the approved picture of OUR character, for the exact colours and drawing style): an "
    "IRON WARRIOR in plain forged steel. Hand-drawn on paper: a wobbly dark-brown ink outline (#2B2118, about {px} px) running all the way "
    "round every part exactly on its silhouette, thinner ink lines for the inner structural lines, and every area filled with ONE flat "
    "colour with visible coloured-pencil / wax-crayon hatching. Colours: steel plates #A0A2AA, faces turned away / thick edges darker steel "
    "#696A70, light steel #BFC0C3 only where listed, dark iron #5A585F, under-suit near-black #2D2D2F, crimson red #C63D3E with darker red "
    "#973B31. The parts of image 1 are painted in a smooth digital cel style with icy blue and white colours, glowing cyan slits, "
    "SNOWFLAKE emblems and light / dark shading bands: do NOT copy that painting style, those colours or the snowflakes; no shading, no "
    "highlights, no white shine streaks, no gradients, no glow, no shadows: flat colour only. VERY SIMPLE: no extra rivets, engravings, "
    "scratches or patterns beyond what is listed.")
BG2 = "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."

MO_TA = {
    "A": [
        ("guan_01", "THE HELMET CREST (a big curved fan sweeping up and to the left): the same silhouette, now stiff CRIMSON HORSEHAIR: flat "
                    "red #C63D3E, with the darker red #973B31 zone where image 1 has its darker blue inner band (along the lower inner edge "
                    "near the helmet); a few thin ink strand lines following the curve; the outer edge may have a few small brushy notches "
                    "but stays on the silhouette."),
        ("hujing_01", "THE HELMET FACE-PLATE with the round disc on its left: plate steel #A0A2AA, the narrow side band on its right edge "
                      "darker steel #696A70; the white rim band along its top edge becomes plain steel #A0A2AA with one ink line; the "
                      "vertical eye slits stay exactly where they are, same shape, filled flat dark charcoal #2D2D2F (no cyan, no glow); "
                      "the round disc on the left light steel #BFC0C3 with its inner ring line."),
        ("tou_01", "THE ROUND BACK DOME of the helmet (a ball with a small knob on top): one flat dark iron #5A585F; the knob on top darker "
                   "#45444A. No shading crescent."),
        ("dun_01", "THE KITE SHIELD (front face with a raised border frame, the thick side edge on the right, a band along the top): the "
                   "raised border frame light steel #BFC0C3, keeping its exact shape (including its V-shaped top inner edge); the inner "
                   "field inside the frame steel #848C9B; the thick side edge darker steel #696A70; the top band (cyan glass in image 1) "
                   "becomes plain steel #A0A2AA. NO SNOWFLAKE: in the middle of the inner field only one round raised iron BOSS (dark "
                   "iron #595B64 with one ring line) and four small round rivets around it (above, below, left, right). Nothing else."),
        ("qizi_01", "THE TABARD (a narrow hanging cloth strip): flat crimson #C63D3E; its light-blue border becomes the same crimson with "
                    "one ink line; near its bottom one dark iron band #5A585F where image 1 has its pale stripe. NO snowflake, no emblem."),
        ("wuqi_01", "THE SPEAR (lying horizontally on this sheet, its tip pointing RIGHT): the big crystal head becomes a forged IRON "
                    "leaf-shaped spearhead of the SAME outline with ONE straight central ridge line along its length, the half above "
                    "the ridge light steel #B7BABF, the half below #848B98; a short dark iron collar #5A585F where the head meets the "
                    "fluff; the white fluffy tuft becomes a short crimson TASSEL #C63D3E (same place, same outline, a few strand lines); "
                    "the long thin shaft steel #737985; the crystal butt cap at the left end becomes a small pointed iron cap #848B98."),
    ],
    "B": [
        ("st_01", "CHEST PLATE: steel #A0A2AA, the face turned away darker #696A70; its white rim becomes light steel #BFC0C3."),
        ("qunbai_01", "SHORT ARMOURED SKIRT (plates hanging from the waist): steel #A0A2AA, the plates turned away darker #696A70; the white "
                      "trims become light steel #BFC0C3."),
        ("hujian_l_01", "SHOULDER PLATE (shield side): steel #A0A2AA, its white rim light steel #BFC0C3."),
        ("hujian_r_01", "SHOULDER PLATE (spear side): the same."),
        ("xiaobi_r_02", "FOREARM (the rounded piece): a crimson red cloth WRAP #C63D3E with two thin darker red #973B31 wrap lines across it."),
        ("xiaotui_l_01", "SHIN AND BOOT (near leg): steel #A0A2AA, the boot's toe and the face turned away darker #696A70; keep the plate lines."),
        ("xiaotui_r_01", "SHIN AND BOOT (far leg): the same."),
        ("datui_l_01", "THIGH (near): under-suit near-black #2D2D2F, plain."),
        ("datui_r_01", "THIGH (far): under-suit near-black #2D2D2F, plain."),
        ("dang_01", "HIP PIECE: under-suit near-black #2D2D2F, plain."),
        ("dabi_r_01", "UPPER ARM: under-suit near-black #2D2D2F, plain."),
        ("bozi_01", "NECK (a dark oval): under-suit near-black #2D2D2F, plain."),
        ("xiaobi_r_01", "PALM behind the spear shaft (bottom row, drawn very big): steel gauntlet #7B808B, plain."),
        ("sizhi_01", "FINGERS in front of the spear shaft (bottom row, drawn very big): steel gauntlet #7B808B; keep the lines between the "
                     "fingers."),
        ("damz_01", "THUMB (bottom row, drawn very big): steel gauntlet #7B808B."),
    ],
}
VI_TO = {"A": "mào, mặt nạ mũ + đĩa tròn, vòm sau mũ; khiên, vạt áo, giáo (nằm ngang)",
         "B": "giáp ngực, váy giáp, hai giáp vai, cẳng tay; hai ống chân, hai đùi, đũng, bắp tay, cổ; lòng bàn tay, ngón tay, ngón cái"}
SO_PART = {"A": "Six parts: top row a big curved helmet crest, the helmet face-plate with eye slits and a round disc, the round back dome "
                "of the helmet; bottom row a big kite shield, a narrow tabard, a long spear lying horizontally with its tip to the right.",
           "B": "Fifteen parts: top row a chest plate, a short armoured skirt, two shoulder plates, a rounded forearm; middle row two shins "
                "with boots, two dark thighs, a dark hip piece, a dark upper arm, a dark neck oval; bottom row three gauntlet pieces of "
                "the spear hand (palm, fingers, thumb), drawn very big."}


def vung():
    """{vùng: (hình đầu tiên dùng vùng đó, ảnh part cắt theo lưới)}."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_goc.json")
    out = {}
    for a in atts:
        if a["region"] not in out:
            out[a["region"]] = (a, G.part_goc(a))
    return out


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def to():
    V = vung()
    os.makedirs(G.MAU, exist_ok=True)
    O = {}
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = []
            for r, z, xoay in h_:
                big = V[r][1].resize((int(round(V[r][1].width * z)), int(round(V[r][1].height * z))), Image.LANCZOS)
                if xoay:
                    big = big.rotate(-xoay, expand=True, resample=Image.BICUBIC)
                cs.append((r, z, xoay, big))
            cao.append((cs, max(c[3].height for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3].width for c in cs)) // (len(cs) + 1)
            x = ke
            for r, z, xoay, big in cs:
                y0 = y + (hh - big.height) // 2
                can.alpha_composite(big, (x, y0))
                o[r] = dict(hop=[x, y0, big.width, big.height], z=z, xoay=xoay)
                x += big.width + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    prompt_da(O)


def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


def prompt_da(O):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: đổi da từng mảnh theo khung part (concept A đã duyệt 2026-11-16)", "",
          "Mỗi tờ là các mảnh GỐC cắt ra từ rig con gốc (phóng to); GPT vẽ lại da từng mảnh đúng chỗ, đúng cỡ, đúng hình bóng. Ảnh mảnh gốc là "
          "của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai.", ""]
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out = os.path.join(G.TAI, f"D_{ma}.png")
        p = os.path.join(GUI, f"luot_2_da_{ma}.txt")
        R = [(mau, "the PARTS SHEET, 1536x1024, white background: the separate body parts of the puppet, each drawn alone, at the exact "
                   "size and place to keep. " + SO_PART[ma] + " They are painted in a smooth icy-blue digital style.",
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng 2,3–5,5 lần: {VI_TO[ma]}. Hình cel số màu băng lam trắng"),
             (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: a chubby iron warrior in plain grey steel "
                       "armour, a crimson horsehair crest, a steel kite shield with one round iron boss and four rivets, a crimson tabard, "
                       "and a long iron spear with a red tassel. Take from it the colours, the materials and the hand-drawn look (wobbly "
                       "brown ink line, crayon hatching, flat colour). The shapes come from image 1.",
              "Concept A đã duyệt (1536 × 1024, nền trắng): lấy màu, chất liệu, nét vẽ tay"),
             (CUNG_LUA, "an approved hero of the same game (an armoured knight), 1536x1024: the hand-drawn ink and crayon style to match. "
                        "Do NOT copy its design.",
              "Quỷ lửa bắn cung đã duyệt: chỉ lấy nét vẽ")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "", CHUNG, "", STYLE2.format(px=PX[ma]), "",
              "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        t += [f"{i}. ({cho(o, r)}) {mt}" for i, (r, mt) in enumerate(MO_TA[ma], 1)]
        t += ["", BG2]
        ghi(p, t)
        print(p)
        gd += [f"### Tờ `{ma}`: {VI_TO[ma]}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["Kiểm: mỗi mảnh đúng chỗ, đúng cỡ, đúng hình bóng mảnh gốc; đủ số mảnh, không dính nhau; da thép xám, đỏ thẫm, không còn lam băng, "
           "bông tuyết, khe phát sáng; tô phẳng; nền trắng tinh. Cắt: `py -3 -I ArtGen/Spine/chien_sat_da.py cat` (in độ khớp hình bóng từng mảnh).", "",
           "Câu sửa nhanh: \"Every part must stay at exactly the same place and size as in image 1\"; \"remove every icy blue colour and the "
           "snowflakes\"; \"flat colour only: no shading bands, no highlights\"."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def nen(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def cat(chi=None):
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    for ma in TO:
        if chi and ma != chi:
            continue
        fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(f"D_{ma}") and f.endswith(".png")],
                    key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
        if not fs:
            print(f"tờ {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(os.path.join(G.TAI, fs[-1])).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        print(f"tờ {ma}: {fs[-1]}")
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg = ~nen(A)
        fgG = ~nen(Gd)                       # hình gốc lấp kín (mảng trắng bông tuyết / khung trắng là thịt, không phải nền)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        so = []
        for r, d in o.items():
            x, y, cw, ch = d["hop"]
            pad = 14
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
            gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
            sub = lab[y0:y1, x0:x1]
            ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
            m = np.isin(lab, ids)
            m[:y0] = m[y1:] = False
            m[:, :x0] = m[:, x1:] = False
            rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
            mm = m[y:y + ch, x:x + cw]
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
            sang = rgb.min(2).astype(np.float32)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            if d["xoay"]:
                im = im.rotate(d["xoay"], expand=True, resample=Image.BICUBIC)
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
            a2 = np.asarray(im2).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
            a2[..., 3] = np.where(gioi, a2[..., 3], 0)
            # chỗ GPT vẽ hụt trong hình bóng gốc: lấy màu gần nhất của mảnh (khỏi khuyết khi lắp vào lưới)
            thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)   # chỉ hụt sát mép
            if thieu.any() and (a2[..., 3] >= 128).any():
                co = (a2[..., 3] >= 128).astype(np.uint8)
                _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                ys_, xs_ = np.nonzero(co)
                bang = np.zeros((lbl.max() + 1, 3), np.uint8)
                bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
                a2[thieu, :3] = bang[lbl[thieu]]
                a2[thieu, 3] = 255
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            a = mm
            b = fgG[y:y + ch, x:x + cw]
            iou = float((a & b).sum()) / max(1, (a | b).sum())
            ious[r] = round(iou, 3)
            vis = np.full((ch, cw, 3), 255, np.uint8)
            vis[a & b] = (170, 170, 170)
            vis[b & ~a] = (230, 60, 60)
            vis[a & ~b] = (60, 190, 60)
            visI = Image.fromarray(vis)
            if d["xoay"]:
                visI = visI.rotate(d["xoay"], expand=True)
            so.append((visI.resize((tw, th)), Image.fromarray(a2, "RGBA")))
            print(f"  {r:12s} IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
        w_ = sum(max(s[0].width, s[1].width) + 10 for s in so)
        hh = max(s[0].height for s in so)
        h2 = max(s[1].height for s in so)
        out = Image.new("RGB", (w_ + 10, hh + h2 + 30), (150, 150, 150))
        xx = 10
        for vis, kh in so:
            out.paste(vis, (xx, 10))
            out.paste(kh, (xx, hh + 20), kh)
            xx += max(vis.width, kh.width) + 10
        out.save(os.path.join(MANH, f"_so_{ma}.png"))
        print(os.path.join(MANH, f"_so_{ma}.png"))
    json.dump(ious, open(pj, "w"), indent=1)


# ================================================================ DẠNG 2 (dạng tiến hóa) trên CÙNG rig: tỉ lệ đổi ở rig (chien_sat_rig.py
# CS_DANG=2: mũ 0,82, mào 1,32, giáp vai 1,6), hình bố cục dựng bằng da dạng 1 (mau/bo_cuc.png) làm ảnh mẫu; concept chỉ đổi da + thêm vài
# mảnh cứng (gai vai, núm gai khiên, cánh mũ) + mũi giáo to bản. Người dùng 2026-11-16: "làm dạng 2 của tướng này".
BASE2 = os.path.join(os.path.dirname(G.BASE), "chien_sat_2")
MAU2, TAI2 = os.path.join(BASE2, "mau"), os.path.join(BASE2, "tai_ve")
GUI2 = os.path.join(HERE, "gui_gpt", "chien_sat_2")
HUONG2 = {
    "A": ("thép đen + vàng + đỏ thẫm",
          "giáp thép đen, viền vàng; mào hai lớp (đỏ thẫm phủ trên lớp đen); khe mặt nạ hổ phách; giáp vai mỗi bên một gai; khiên viền vàng, "
          "núm gai giữa; mũi giáo to bản hai cánh (kiểu đinh ba lá), khâu vàng; vạt đỏ thẫm viền vàng",
          ["ARMOUR COLOURS: blackened steel plates #545A66, faces turned away #3A3F49; a narrow GOLD trim #D2A23E along the rims of the "
           "face-plate, the round disc, the shoulder plates, the chest plate and the skirt (one thin band each, nothing more); under-suit "
           "near-black #26272B.",
           "EYE SLITS: the same slits, filled flat amber #F0B23A (flat colour, no glow): a fiercer look.",
           "CREST: the same big curved fan (place and size of image 1) but TWO LAYERS: the front layer crimson horsehair #B02A30 with darker "
           "#7E1F25 inner band, and behind it a slightly bigger black horsehair layer #2F3036 showing as a dark border along its outer curve.",
           "SHOULDER PLATES: bigger layered plates (two overlapping plates each), each with ONE short sharp conical iron SPIKE pointing up and "
           "outwards; the near shoulder plate rises above the top edge of the shield.",
           "SHIELD: the same kite shape and place; frame gold #D2A23E, inner field blackened steel #4A505B, thick side edge #3A3F49; in the "
           "middle one round iron boss with a short sharp conical SPIKE pointing at the viewer; no rivets.",
           "TABARD: crimson #B02A30 with a gold #D2A23E band near its bottom.",
           "SPEAR: the same long shaft (dark iron #3A3F49) but a BIGGER spearhead: a long broad leaf blade with two small curved side WINGS "
           "at its base (like a partisan), light steel #C2C6CE with one central ridge line; a gold collar #D2A23E; a crimson tassel."]),
    "B": ("thép xám thẫm + bạc + đỏ (giữ màu dòng)",
          "giữ màu dòng dạng 1 nhưng đậm hơn: thép xám thẫm, viền bạc sáng; hai bên mũ thêm hai cánh thép vuốt ra sau; mào đỏ to; giáp vai "
          "hai lớp; khiên viền bạc, núm có gai ngắn + bốn đinh; mũi giáo dài to bản; khe mặt nạ tối",
          ["ARMOUR COLOURS: darker steel plates #7A808C, faces turned away #555A65; a narrow bright SILVER trim #CDD2DA along the rims of "
           "the face-plate, the shoulder plates, the chest plate and the skirt; under-suit near-black #26272B.",
           "EYE SLITS: the same slits, flat dark charcoal #22252B.",
           "HELMET WINGS: on the left side of the helmet, where the round disc is, the disc becomes the root of a short swept-back steel WING "
           "made of three stacked feather-like metal blades pointing up and back to the left (like a winged helm), steel #A9AEB8 with darker "
           "#7A808C undersides; it stays smaller than the crest and does not cover the face-plate.",
           "CREST: the same big curved crimson horsehair fan #B8333A with darker #84252B inner band.",
           "SHOULDER PLATES: bigger, two overlapping steel plates each with a silver rim; the near one rises above the top edge of the shield.",
           "SHIELD: the same kite shape and place; frame silver #CDD2DA, inner field dark steel #626874, thick side edge #4A4F59; in the "
           "middle one round iron boss with a short blunt spike and four small rivets around it.",
           "TABARD: crimson #B8333A with a silver #CDD2DA band near its bottom.",
           "SPEAR: the same long shaft (dark iron #4A4F59) with a LONGER and BROADER leaf-shaped steel spearhead #C2C6CE (one ridge line), "
           "a silver collar, a crimson tassel."]),
    "C": ("gang xanh thép + đồng thau + đỏ",
          "giáp gang ánh xanh thép, viền đồng thau; trên đỉnh mũ thêm một sống thép (vây) dưới chùm mào; khe mặt nạ vàng nhạt; giáp vai hai "
          "gai; khiên viền đồng thau, mép trên có ba mấu nhọn; mũi giáo to bản có ngạnh",
          ["ARMOUR COLOURS: blue-black gunmetal plates #55607A, faces turned away #3D4659; a narrow BRASS trim #C99A3E along the rims of the "
           "face-plate, the round disc, the shoulder plates, the chest plate and the skirt; under-suit near-black #26272B.",
           "EYE SLITS: the same slits, filled flat pale gold #F2D27A (no glow).",
           "HELMET RIDGE: along the top of the helmet, under the crest, a tall narrow steel RIDGE (a fin-shaped crest plate) #8A94A8 with a "
           "brass edge, from the face-plate top back to the crest root.",
           "CREST: the same big curved fan, crimson horsehair #B02A30 with darker #7E1F25 inner band.",
           "SHOULDER PLATES: bigger, each with TWO short iron spikes in a row; the near one rises above the top edge of the shield.",
           "SHIELD: the same kite shape and place; frame brass #C99A3E, inner field gunmetal #4E586E, thick side edge #3D4659; the top edge "
           "gets three small pointed iron prongs; in the middle one round brass boss.",
           "TABARD: crimson #B02A30 with a brass #C99A3E band near its bottom.",
           "SPEAR: the same long shaft (gunmetal #3D4659) with a BIGGER spearhead: a broad steel blade #B9C1CF with one ridge line and two "
           "short backward BARBS at its base; a brass collar; a crimson tassel."]),
}


def bo_cuc_khung():
    """bố cục dạng 2 (rig dựng bằng da dạng 1) đặt giữa khung 1536 × 1024 nền trắng."""
    im = Image.open(os.path.join(MAU2, "bo_cuc.png")).convert("RGB")
    k = 1000.0 / im.height
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    can.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    p = os.path.join(MAU2, "bo_cuc_khung.png")
    can.save(p)
    return p


def prompt_concept2():
    bc = bo_cuc_khung()
    R = [(bc, "the LAYOUT of the new form, 1536x1024, white background: OUR approved first-form iron knight re-proportioned for its "
              "evolved form (smaller helmet, bigger crest, bigger shoulder plates), in its idle pose: a crimson horsehair crest, a grey "
              "steel closed helmet with eye slits, a steel kite shield with a round boss on the viewer's left, a crimson tabard, a long "
              "iron spear with a red tassel held upright on the viewer's right. Keep its POSE, its PROPORTIONS and the PLACE and SIZE of "
              "every piece.",
          "Bố cục dạng 2 (1536 × 1024, nền trắng): chính dạng 1 đã duyệt, dựng lại trên rig với mũ nhỏ hơn, mào và giáp vai to hơn, dáng idle"),
         (CONCEPT, "the APPROVED first form of this character, 1536x1024, white background: the hand-drawn look to keep (wobbly brown ink "
                   "line, crayon hatching, flat colour) and its identity (crimson crest, slit helmet, kite shield, spear with tassel).",
          "Concept dạng 1 đã duyệt: nét vẽ, nhận diện dòng"),
         (CUNG_LUA, "an approved hero of the same game (an armoured knight), 1536x1024: the hand-drawn ink and crayon style and the flat "
                    "colouring of armour plates. Do NOT copy its design, horns or flames.",
          "Quỷ lửa bắn cung đã duyệt: chỉ lấy nét vẽ, cách tô giáp phẳng")]
    hd = ["# Gói GPT: chiến binh sắt DẠNG 2 (chien_sat_2), tướng 2 đảo Kim", "",
          "Người dùng 2026-11-16 duyệt dạng 1 (`ArtGen/Spine/inbox/chien_sat_1/tai_ve/L1_duyet.png`) rồi dặn \"làm dạng 2 của tướng này\". Dạng 2 "
          "dùng CÙNG rig, cùng clip; tỉ lệ đổi ở rig (mũ 0,82, mào 1,32, giáp vai 1,6), hình bố cục dựng bằng da dạng 1 làm ảnh mẫu 1.", "",
          "## Lượt 1: concept dạng 2, ba hướng (Claude đề xuất, chờ người dùng chọn)", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG2.items():
        out = os.path.join(TAI2, f"L1_{k}.png")
        p = os.path.join(GUI2, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: draw the EVOLVED SECOND FORM of our iron knight (image 2 is its first form): an older, stronger, battle-hardened elite "
              "iron warrior of the same line. ONE picture in EXACTLY the pose, proportions and layout of image 1: every piece in the same "
              "place and at the same size (helmet, crest, shield, tabard, skirt, legs, spear arm and fist, spear), with the same overlaps, "
              "so that it fits the same animation puppet. Keep the identity: closed helmet with vertical eye slits on its right side and "
              "the round disc on its left, big horsehair crest, kite shield in front on the viewer's left, tabard down the chest, long "
              "spear held upright in the right fist with a tassel under the head. Change ONLY what is listed:", ""]
        t += [f"- {d}" for d in doi]
        t += ["",
              f"DRAWING STYLE (very important): hand-drawn on paper like images 2 and 3: a wobbly dark-brown ink outline ({MUC}, about 7 px) "
              "round every piece, thinner ink lines for the few inner structural edges, every area ONE flat colour with visible "
              "coloured-pencil / wax-crayon hatching. No shading, no highlights, no white shine streaks, no gradients, no glow, no "
              "shadows, no gloss, no sparkles. SIMPLE DESIGN: no extra rivets, engravings, scratches, chains, belts, capes, badges or "
              "patterns beyond what is listed.", "",
              "Mood: a sturdy, fierce, determined elite iron warrior ready to fight, not a cute mascot, not scary. Both legs and the spear "
              "arm stay attached to the body exactly as in image 1.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no dust, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng tỉ lệ, đúng chỗ và cỡ từng mảnh như ảnh 1 (chồng lên phải trùng, trừ phần thêm: gai, cánh mũ, sống mũ, mũi giáo to "
           "bản); vẫn nhận ra cùng dòng với dạng 1; màu đậm hơn dạng 1; tô phẳng, không bóng; tay cầm giáo, hai chân dính thân; nền trắng tinh."]
    ghi(os.path.join(GUI2, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    elif cmd == "to":
        to()
    elif cmd == "cat":
        cat(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "concept2":
        prompt_concept2()
    else:
        print(__doc__)
