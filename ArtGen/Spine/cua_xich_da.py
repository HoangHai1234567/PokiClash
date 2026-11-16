# -*- coding: utf-8 -*-
"""Tinh linh đuôi máy cưa (cua_xich, rig monster_3374): concept THEO CON GỐC (đầu tròn quay phải, mũ trùm sẫm che nửa trên con mắt, sừng
nhọn vút trái trên, ba tinh thể sau đầu, thân tròn nhỏ, hai chân que, đuôi mang đĩa bánh răng), đổi sang tinh linh MÁY CƯA: đĩa thành lưỡi
cưa tròn, thêm tay cầm dây giật khởi động ở bụng (appear kéo dây), đổi dáng mũ + các mảnh sau đầu (mảnh nhận diện).

    cua_xich_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/cua_xich_1/mau/goc_ca_con.png (+ .json: khung từng part)
    cua_xich_da.py concept    ba file prompt concept (ba hướng) → gui_gpt/cua_xich_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    cua_xich_da.py concept2   lượt 2 thú hoang, quặng sắt trên đầu, đuôi như con gốc → luot_2_concept_<D|E|F>.txt
    cua_xich_da.py sua_dau    lượt 3 sửa đầu / mặt bản D (KEEP / CHANGE) → luot_3_dau_<D1|D2|D3>.txt
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cua_xich as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "cua_xich_1")
TINH_SAT = os.path.join(HERE, "inbox", "tinh_sat_1", "tai_ve", "L1_duyet.png")
CHIEN_SAT = os.path.join(HERE, "inbox", "chien_sat_1", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"

# slot của họ → tên bộ phận (để ghi khung bao vào prompt)
TEN = {"to_01": "HEAD (round face ball)", "to_02": "HOOD over the head", "zuoerduo": "UPPER-LEFT HORN", "tofa": "THREE BACK PIECES",
       "youerduo": "DARK BACK SPIKE (right)", "yanjing_01": "EYE", "shenti": "BODY", "zuoshou": "LEFT HAND", "youshou": "RIGHT HAND",
       "zuodatui2": "LEFT THIGH (ribbed dome)", "zuoxiaotui2": "LEFT SHIN", "youxiaotui2": "RIGHT LEG", "weiba_03": "TAIL BASE",
       "weiba_01": "SAW HOUSING (oblong plate with hub)", "weiba_04": "HOUSING BACK PLATE", "juzi_04": "SAW DISC"}


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
    "PIECE BY PIECE (as in image 1): a small sturdy creature in three-quarter view, FACING THE VIEWER'S RIGHT: a big round HEAD on a small "
    "round BODY, two short stick legs, and a TAIL that carries a round SAW DISC behind it on the left.\n"
    "- HEAD: a big pale round ball (the face), turned to the right. Over the top and the right side of it sits a big dark HOOD (like a "
    "helmet or a cowl); the hood's lower front edge comes down across the UPPER HALF OF THE EYE, so the eye looks narrowed and determined; "
    "the hood ends in a point at the lower right of the face. From the upper left of the hood a long POINTED HORN sweeps out to the upper "
    "left (its underside a lighter colour). On the back of the head, behind the hood, stand THREE tall pieces leaning up and to the right "
    "(a tall one in the middle, a shorter one on its left, a slanted one at the lower right), plus a dark curved SPIKE just behind them on "
    "the far right.\n"
    "- FACE: ONLY ONE EYE shows (the other one is hidden by the turn of the head): a big round eye on the right part of the face, pale "
    "yellow with a big round orange iris filling most of it. No mouth, no nose, no brows. On the left part of the face, three short dark "
    "vertical STRIPES.\n"
    "- BODY: a small pale round body under the head, mostly hidden. Two tiny dark mitten HANDS on the front of the belly: the left hand "
    "near the middle of the belly, the right hand at the right.\n"
    "- LEGS: the near leg (left) has a dark ribbed dome-shaped THIGH (like a scallop shell) and a dark stick shin slanting down to the lower "
    "left; the far leg (right) is a dark stick slanting down to the lower right. Both legs grow out from under the body.\n"
    "- TAIL: from the back of the body on the left, a short dark tail base leads to the SAW: a dark rounded oblong plate (the HOUSING) "
    "standing slanted, with a round HUB near its upper end; behind it a large round DISC centred on the hub, with teeth all round its edge.")

KHONG = ("VERY SIMPLE DESIGN, FEW DETAILS (like image 1): no extra spikes, bolts, rivets, cables, gauges, scratches, cracks, runes, badges "
         "or glowing parts; no mouth, no teeth on the face, no brows, no arms; nothing that is not listed.")

DIA = ("SAW DISC: becomes a real CIRCULAR SAW BLADE: a flat round steel disc in the SAME place and at the SAME size as the disc in image 1, "
       "centred on the hub, with 14 sharp hooked triangular saw TEETH evenly all round its edge, all leaning the same way (clockwise); one "
       "thin ring line around the hub. Flat steel grey #BCC3CC, the side of each tooth a little darker #98A0AA.")
MAT = ("EYE: the SAME single round eye, same place and size, still cut across its top half by the edge of the head-piece above it; pale "
       "{n} with a big round {i} iris and one tiny white dot. Still only one eye.")
SOC = "STRIPES: the three dark stripes on the left of the face become three short dark VENT SLITS {c} (same places)."
DAY = ("ADD ONE NEW small piece, a PULL-START HANDLE (like the starter cord of a lawnmower or a chainsaw): a small {g} T-shaped grip "
       "(about 90 px wide) lying across the front of the belly just under the LEFT HAND (the hand touches it), joined by a short {c} cord to "
       "a small round hole in the belly. The creature pulls this cord to start the saw on its tail.")

# ba hướng (Claude đề xuất, chờ người dùng chọn). Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("cam máy công cụ: mũ bảo hộ cam, vây răng cưa, ống xả",
          "mũ trùm ĐỔI DÁNG thành mũ bảo hộ cam có vành cứng chìa ra che nửa trên con mắt; sừng trái thành ống xả đen ngắn; ba tinh thể "
          "+ gai sau đầu thành bốn vây thép hình răng cưa móc ngược; thân xám thép, tay chân than chì, đùi gân cam; vỏ cưa cam; mắt "
          "vàng tròng cam",
          ["HOOD: changes SHAPE into a smooth rounded HARD-HAT dome, bright safety ORANGE #E8762C, covering the same area of the head, with a "
           "short straight stiff BRIM jutting forward to the right over the eye (the brim's lower edge cuts across the top half of the eye) "
           "and one thin ridge line over the top of the dome.",
           "HORN (upper left): becomes a short black EXHAUST PIPE #34363B: a slightly bent tube pointing up-left out of the back of the "
           "helmet, with an open round end (a dark oval opening); about two thirds of the old horn's length.",
           "THE THREE BACK PIECES and THE DARK SPIKE become FOUR steel SAW-TOOTH FINS standing on the back of the head in the same places "
           "and leans: each a flat blade shaped like one big tooth of a saw (straight front edge, curved back edge, sharp tip hooked "
           "backward). Steel grey #A9B1BC, each with one darker side face #7D8590.",
           "HEAD (face) and BODY: pale steel grey #CFD3D8; the belly between the legs dark #3A3C42.",
           MAT.format(n="yellow #F6E6A6", i="orange #E8902F"),
           SOC.format(c="#4A4E55"),
           "HANDS, SHINS, RIGHT LEG, TAIL BASE: dark charcoal #3A3C42. LEFT THIGH dome: orange #E8762C with dark rib lines.",
           "SAW HOUSING: orange #E8762C, the hub black #2E3035 with one small steel bolt in its middle; the housing back plate charcoal.",
           DIA,
           DAY.format(g="black", c="orange")]),
    "B": ("vạch cảnh báo vàng đen: mũ lam thép mép răng cưa, ống xả",
          "mũ trùm giữ dáng chụp nhưng cả mép trên ĐỔI thành hàng 5 răng cưa móc ngược; sừng trái thành lưỡi thép cong; ba tinh thể "
          "thành ống xả đen (hai to, một nhỏ), gai sau thành gai thép; lam thép + vàng cảnh báo + đen; vỏ cưa vàng vạch đen; mắt "
          "tròng đỏ cam",
          ["HOOD: keeps its cowl shape over the head and eye, but its whole TOP EDGE (from the horn's base back to the back of the head) is "
           "SERRATED into a row of 5 big saw teeth leaning backward, like the edge of a saw blade. Flat steel blue #5F7894.",
           "HORN (upper left): becomes a curved steel BLADE like a hooked fin, same place and same upward-left sweep, a little shorter and "
           "wider; steel blue #5F7894, its underside lighter #8EA3BA.",
           "THE THREE BACK PIECES become black EXHAUST PIPES #303237: two short fat cylinders with open round ends leaning back up-right "
           "(where the tall middle piece and the lower right piece were) and one small pipe (where the left piece was). The DARK SPIKE "
           "becomes a plain curved steel-blue spike.",
           "HEAD (face) and BODY: pale grey #D5D8DC; the belly between the legs black #2F3136.",
           MAT.format(n="cream #F4EBD0", i="red-orange #E2552F"),
           SOC.format(c="#454A52"),
           "HANDS, SHINS, RIGHT LEG, TAIL BASE: black #2F3136. LEFT THIGH dome: hazard yellow #F2C230 with black rib lines.",
           "SAW HOUSING: hazard YELLOW #F2C230 with THREE black diagonal stripes across it; the hub black with one small steel bolt in its "
           "middle; the housing back plate black.",
           DIA,
           DAY.format(g="black", c="yellow")]),
    "C": ("thép súng + đồng đỏ, tinh thể tia lửa hổ phách",
          "mũ trùm ĐỔI DÁNG thành mũ kiểu mặt nạ hàn: vòm tròn thép súng, mép trước thẳng ngang cắt nửa trên con mắt, một đai đồng dọc "
          "mép; sừng trái thành vây đồng vuốt ngược ngắn; ba tinh thể thành tinh thể hổ phách hình TIA LỬA gãy khúc; vỏ cưa đồng; mắt "
          "vàng tròng cam",
          ["HOOD: changes SHAPE into a rounded WELDING-MASK helmet: a smooth dome of dark gunmetal #4B4F57 over the same area of the head; "
           "its lower front edge is one STRAIGHT LEVEL line cutting across the top half of the eye, with ONE thin copper band #C97A45 "
           "along that edge.",
           "HORN (upper left): becomes a short wide copper FIN swept back to the upper left #C97A45 (about two thirds of the old horn's "
           "length), its underside darker copper #9A5632.",
           "THE THREE BACK PIECES become amber SPARK CRYSTALS in the same places and leans, each shaped like a frozen spark: a sharp "
           "jagged shard with two zigzag bends (like a little lightning bolt), not a straight prism. Flat amber orange #F0A040, one darker "
           "side face #C9762A. The DARK SPIKE stays a plain gunmetal spike.",
           "HEAD (face) and BODY: pale steel #D2D5D9; the belly between the legs dark gunmetal #3B3E45.",
           MAT.format(n="yellow #F6E6A6", i="amber-orange #E8902F"),
           SOC.format(c="#4A4E55"),
           "HANDS, SHINS, RIGHT LEG, TAIL BASE: dark gunmetal #3B3E45. LEFT THIGH dome: copper #C97A45 with dark rib lines.",
           "SAW HOUSING: copper #C97A45, the hub gunmetal with one small steel bolt in its middle; the housing back plate dark gunmetal.",
           DIA,
           DAY.format(g="dark gunmetal", c="copper")]),
}

# Lượt 2 (người dùng 2026-11-16: "làm nó mang tính sinh vật hoang dã hơn, có quặng sắt trên đầu, đuôi cưa cũng nên làm giống con gốc"):
# bỏ mọi thứ máy móc (mũ bảo hộ, ống xả, khe gió); mũ trùm thành mai / bờm tự nhiên; ba tinh thể thành QUẶNG SẮT; đuôi giữ đúng dáng con gốc.
DUOI2 = ("TAIL: keep it EXACTLY like image 1 in shape, place and size (do not turn it into a circular saw blade): the short tail base, the "
         "slanted rounded oblong HOUSING plate with the round HUB near its upper end (a round boss with one thin ring around it), and behind "
         "it the round toothed DISC centred on the hub with its 8 blunt square TEETH evenly round the edge, same shapes. Only recolour it: "
         "{c}.")
DAY2 = ("ADD ONE NEW small piece: a short thick {c} CORD coming out of a small hole in the middle of the belly, ending in a small round "
        "RING grip that lies just under the LEFT HAND (the left hand touches the ring). The cord is short (about 70 px) and does NOT reach "
        "the right hand. (The creature pulls it to start the saw on its tail.)")
TAY2 = "HANDS: the two tiny mitten hands become small wild PAWS with three short blunt claws each (same places and sizes), {c}."
MAT2 = ("EYE: the SAME single round eye (same place and size, its top half still cut by the edge of the head-piece above it): pale "
        "{n} with a big round {i} iris and a narrow dark vertical SLIT PUPIL (a wild animal's eye), one tiny white dot. Still only one eye.")
SOC2 = "FACE MARKINGS: the three dark stripes on the left of the face stay (same places), like an animal's markings, {c}."
QUANG = ("THE THREE BACK PIECES become raw IRON ORE growing out of the back of the head, in the same places, sizes and leans as the "
         "crystals of image 1: ")
HOANG = ("Make it a WILD ANIMAL-LIKE CREATURE: no helmet, no visor, no clothes, no pipes, no vents, no bolts, no machine parts anywhere "
         "except the saw on its tail.")

HUONG2 = {
    "D": ("mai đá sẫm + cục quặng sắt gỉ",
          "mũ trùm thành mai đá sẫm tự nhiên (giữ dáng chụp, mép trên vài gờ vảy thấp); sừng thành sừng thú cong, lót gỉ cam; ba tinh "
          "thể thành ba cục quặng sắt thô đầu bằng, mảng gỉ cam; tay thành chân thú ba vuốt; mắt đồng tử dọc; đuôi giữ dáng con gốc "
          "(vỏ đá sẫm, vòng trục gỉ cam, răng sắt nhạt)",
          ["HOOD: becomes a thick natural SHELL PLATE (like the hard back plate of an armadillo or a beetle), the SAME cowl shape and place, "
           "its lower front edge still across the top half of the eye; along its top edge three or four low rounded bumps like scales. "
           "Flat dark slate #4D5058.",
           "HORN (upper left): a natural curved animal HORN, same place and sweep, dark slate #4D5058, its underside rusty orange #B5622E.",
           QUANG + "each a blunt, chunky, irregular LUMP of ore with 3 to 4 big flat broken faces (no sharp crystal tips), dark iron grey "
           "#5E646E with one darker face #3F444C and ONE flat rust patch #B9612C on each lump. The DARK SPIKE becomes a smaller ore lump "
           "of the same kind.",
           "FACE and BODY skin: pale stone grey #C9C6C0; the belly between the legs dark slate #3E4148.",
           SOC2.format(c="dark grey #5A5752"),
           MAT2.format(n="yellow #F6E6A6", i="amber #E39A2D"),
           TAY2.format(c="dark slate #3E4148"),
           "LEGS and TAIL BASE: dark slate #3E4148; the LEFT THIGH dome dark slate with darker rib lines.",
           DUOI2.format(c="housing plate dark slate #4D5058, hub boss #3A3D44 with a thin rust-orange ring #C7772F, disc dark iron "
                          "#3F444C, its teeth pale raw iron #BFC4CB"),
           DAY2.format(c="dark brown")]),
    "E": ("mai nâu gỉ + quặng hematit dạng bong bóng",
          "mũ trùm thành mai nâu gỉ; sừng cong lót màu cát; ba tinh thể thành ba chùm quặng hematit dạng bong bóng (4–6 bong tròn dính "
          "nhau, xám sắt sẫm); da cát xám, sọc nâu gỉ; chân thú ba vuốt; mắt đồng tử dọc; đuôi giữ dáng con gốc (vỏ nâu gỉ, răng sắt "
          "nhạt)",
          ["HOOD: becomes a thick natural SHELL PLATE, the SAME cowl shape and place, its lower front edge still across the top half of the "
           "eye. Flat rust brown #8A4A32.",
           "HORN (upper left): a natural curved animal HORN, same place and sweep, rust brown #8A4A32, its underside sand #D8BE8E.",
           QUANG + "each a cluster of KIDNEY IRON ORE (botryoidal hematite): 4 to 6 rounded BUBBLES of different sizes grown together into "
           "one lump, filling the same outline as the crystal it replaces. Flat dark metallic iron grey #4A4F57, each bubble with its own "
           "ink outline, no highlights. The DARK SPIKE becomes a small cluster of 2 or 3 bubbles of the same kind.",
           "FACE and BODY skin: warm sandy grey #CFC3AE; the belly between the legs dark brown #43312A.",
           SOC2.format(c="rust brown #7A4530"),
           MAT2.format(n="yellow #F6E6A6", i="amber #E39A2D"),
           TAY2.format(c="dark brown #43312A"),
           "LEGS and TAIL BASE: dark brown #43312A; the LEFT THIGH dome rust brown #8A4A32 with dark rib lines.",
           DUOI2.format(c="housing plate rust brown #8A4A32, hub boss dark brown #43312A with a thin sand-gold ring #D8A955, disc dark "
                          "iron #3F444C, its teeth pale raw iron #BFC4CB"),
           DAY2.format(c="dark brown")]),
    "F": ("bờm lông xù than chì + cục quặng sắt gỉ đỏ",
          "mũ trùm thành BỜM LÔNG xù dày màu than chì (giữ vùng phủ, mép thành các chỏm lông nhọn ngắn, mép trước vẫn cắt nửa trên "
          "mắt); sừng thành sừng thú cong ngà; ba tinh thể thành ba cục quặng sắt gỉ đỏ thô; chân thú ba vuốt; mắt đồng tử dọc; đuôi giữ "
          "dáng con gốc (vỏ than chì, vòng trục gỉ, răng sắt nhạt)",
          ["HOOD: becomes a thick shaggy FUR MANE covering the same area of the head (a hood of fur, not hair on a human): flat dark "
           "charcoal #3F4045, its outer edges broken into short pointed tufts, its lower front edge a row of short tufts still across the "
           "top half of the eye.",
           "HORN (upper left): a natural curved animal HORN, same place and sweep, ivory #E3D8BF with a darker ivory underside #C2B490.",
           QUANG + "each a blunt, chunky, irregular LUMP of RUSTY iron ore with 3 to 4 big flat broken faces (no sharp crystal tips), "
           "rust red-brown #9C4A2C with one darker face #6E3220 and one flat dark iron patch #4A4F57 on each lump. The DARK SPIKE "
           "becomes a smaller rusty ore lump.",
           "FACE and BODY skin: pale warm grey #CDC8C1; the belly between the legs dark charcoal #3A3B40.",
           SOC2.format(c="dark charcoal #4A4A4F"),
           MAT2.format(n="yellow #F6E6A6", i="orange #E8862F"),
           TAY2.format(c="dark charcoal #3A3B40"),
           "LEGS and TAIL BASE: dark charcoal #3A3B40; the LEFT THIGH dome rust red-brown #9C4A2C with dark rib lines.",
           DUOI2.format(c="housing plate dark charcoal #45464C, hub boss #34353A with a thin rust-orange ring #C7772F, disc dark iron "
                          "#3F444C, its teeth pale raw iron #BFC4CB"),
           DAY2.format(c="dark brown")]),
}

STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) for the "
    "few inner lines (facet edges, the saw teeth, the vent slits, the rib lines), and every area filled with ONE flat colour with visible "
    "coloured-pencil / wax-crayon hatching. Image 1 is painted in a smooth digital style with soft gradients (purple-pink crystals, soft "
    "light on the grey parts): do NOT copy that painting style or its colours: no shading, no highlights, no white shine streaks, no "
    "gradients, no glow, no shadows, no gloss, no sparkles: flat colour only. A different tone appears only where a different face or "
    "material is listed. The only exception: one tiny white dot in the eye. Drawn carefully and cleanly, not scribbled.")


def prompt_concept():
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    hop = json.load(open(mau[:-4] + ".json"))["hop"]
    R = [(mau, "the REFERENCE creature, 1536x1024, white background: a small creature facing right with a big pale round head under a "
               "dark hood, one big amber eye, a pointed horn at the upper left, three purple crystals on the back of its head, a small "
               "round body with two stick legs, and a tail carrying a dark plate and a toothed disc on the left. It is painted in a "
               "smooth digital style with gradients. Keep its POSE, its PIECES, their PLACES and SIZES and its single EYE; change its "
               "LOOK as described.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): đầu tròn xám nhạt quay phải dưới mũ trùm sẫm, một mắt hổ phách to, sừng "
          "nhọn trái trên, ba tinh thể tím sau đầu, thân tròn nhỏ, hai chân que, đuôi mang tấm vỏ sẫm và đĩa bánh răng bên trái. Giữ dáng, "
          "từng mảnh, chỗ, cỡ, con mắt; đổi hình theo hướng"),
         (CHIEN_SAT, "an approved hero of our game from the same metal island (a little armoured spear knight), 1536x1024, white "
                     "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and how flat steel parts "
                     "are drawn and coloured. Do NOT copy its design, face or colours.",
          "Chiến binh sắt (tướng 2 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô thép phẳng"),
         (TINH_SAT, "another approved hero of our game from the same island (a little iron-crystal spirit), 1536x1024, white "
                    "background: see how flat metal facets and darker side facets are drawn. Do NOT copy its design, face or colours.",
          "Tinh linh tinh thể sắt (tướng 1 đảo Kim) đã duyệt: xem cách tô mặt kim loại phẳng + mặt bên sẫm")]
    vi_tri = ["POSITIONS on the 1536x1024 canvas (bounding boxes of each piece in image 1; keep them):"]
    for slot, ten in TEN.items():
        if slot in hop:
            x0, y0, x1, y1 = hop[slot]
            vi_tri.append(f"- {ten}: x = {x0} to {x1}, y = {y0} to {y1}")
    hd = ["# Gói GPT: tinh linh đuôi máy cưa (cua_xich), tướng 4 đảo Kim", "",
          "Con gốc của rig: `monster_3374` (đầu tròn mũ trùm sẫm, tinh thể tím sau đầu, đuôi đĩa bánh răng; game tham khảo). Ảnh mẫu 1 là "
          "hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng (2026-11-16)", "",
          "Người dùng: \"concept tinh linh đuôi máy cưa\"; appear kéo một dây trên người để khởi động cưa ở đuôi. Ba file, mỗi file một "
          "hướng. Giữ dáng, chỗ, cỡ từng mảnh của con gốc (để lắp lên đúng xương) và con mắt duy nhất bị mép mũ cắt nửa trên; đĩa thành "
          "lưỡi cưa tròn; thêm tay cầm dây giật ở bụng ngay dưới tay trái; đổi dáng mũ và các mảnh sau đầu.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: REDESIGN. Redraw the creature of image 1 as ONE picture of a little CHAINSAW-TAIL SPIRIT (a living little machine "
              "creature of steel whose tail is a spinning circular saw): the SAME creature in the SAME pose, with EVERY piece in the same "
              "place, at the same size, with the same overlaps (if the new picture were laid over image 1, every piece must coincide), "
              "except the shape changes described below; new colours and our hand-drawn drawing style. Do not remove, merge or move "
              "pieces; add only the one new piece listed. Keep the FACE as in image 1: facing right, ONE eye only, its top half cut by "
              "the edge of the head-piece above it, no mouth.", "",
              MO_TA_CON, ""] + vi_tri + ["",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              "Every leg, hand and the tail base stay JOINED to the body (no white gap between a limb and the body); every piece whole "
              "and unbroken.", "",
              KHONG, "",
              STYLE, "",
              "Mood: a tough, determined little machine spirit ready to fight (a game hero), not a cute mascot, not scary.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the creature at the same "
              "place and size as in image 1. No sparks, no smoke, no motion lines, no glow, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng từng mảnh như ảnh 1 (chồng lên phải trùng, trừ các mảnh đổi dáng); quay phải, một con mắt duy nhất bị "
           "mép mũ cắt nửa trên, không miệng; đĩa đuôi là lưỡi cưa tròn răng móc cùng chiều; có tay cầm chữ T nhỏ dưới tay trái nối dây "
           "vào bụng; chân, tay, gốc đuôi dính thân; nét bút mực rung, vân sáp, tô phẳng, không bóng, không phát sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"keep only one eye, its top half cut by the edge of the head-piece\"; \"remove the shading and highlights, flat "
           "colour only\"; \"keep every piece at the same place and size as in image 1\"; \"the legs must join the body\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


def prompt_concept2():
    """lượt 2: thú hoang, quặng sắt trên đầu, đuôi giữ dáng con gốc. Ảnh mẫu như lượt 1."""
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    hop = json.load(open(mau[:-4] + ".json"))["hop"]
    R = [(mau, "the REFERENCE creature, 1536x1024, white background: a small creature facing right with a big pale round head under a "
               "dark hood, one big amber eye, a pointed horn at the upper left, three purple crystals on the back of its head, a small "
               "round body with two stick legs, and a tail carrying a dark oblong plate with a hub and a toothed disc on the left. It is "
               "painted in a smooth digital style with gradients. Keep its POSE, its PIECES, their PLACES and SIZES, its single EYE and "
               "the SHAPE of its TAIL; change its LOOK as described.",
          "Hình cả con gốc ở dáng nghỉ (như lượt 1). Giữ dáng, từng mảnh, chỗ, cỡ, con mắt và DÁNG ĐUÔI; đổi hình theo hướng"),
         (CHIEN_SAT, "an approved hero of our game from the same metal island, 1536x1024, white background: match EXACTLY its wobbly "
                     "dark-brown pen line, its visible crayon hatching and how flat metal parts are coloured. Do NOT copy its design, "
                     "face or colours.",
          "Chiến binh sắt (tướng 2 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp"),
         (TINH_SAT, "another approved hero of our game from the same island (a little iron-crystal spirit), 1536x1024, white "
                    "background: see how flat facets and darker side faces are drawn. Do NOT copy its design, face or colours.",
          "Tinh linh tinh thể sắt (tướng 1 đảo Kim) đã duyệt: xem cách tô mặt phẳng + mặt bên sẫm")]
    vi_tri = ["POSITIONS on the 1536x1024 canvas (bounding boxes of each piece in image 1; keep them):"]
    for slot, ten in TEN.items():
        if slot in hop:
            x0, y0, x1, y1 = hop[slot]
            vi_tri.append(f"- {ten}: x = {x0} to {x1}, y = {y0} to {y1}")
    hd_p = os.path.join(GUI, "HUONG_DAN.md")
    hd = open(hd_p, encoding="utf-8").read().rstrip("\n").split("\n") if os.path.exists(hd_p) else []
    if "## Lượt 2" in "\n".join(hd):
        hd = hd[:hd.index(next(x for x in hd if x.startswith("## Lượt 2")))]
    hd += ["", "## Lượt 2: thú hoang, quặng sắt trên đầu, đuôi giữ dáng con gốc (2026-11-16)", "",
           "Người dùng: \"làm nó mang tính sinh vật hoang dã hơn, có quặng sắt trên đầu, đuôi cưa cũng nên làm giống con gốc\". Ảnh mẫu như "
           "lượt 1 (1 con gốc, 2 chiến binh sắt, 3 tinh linh tinh thể sắt). Bỏ mọi thứ máy móc; mũ trùm thành mai / bờm; ba tinh thể thành "
           "quặng sắt; tay thành chân thú ba vuốt; mắt đồng tử dọc; đuôi giữ đúng dáng con gốc (tấm vỏ thuôn có trục, đĩa 8 răng vuông); "
           "dây giật ngắn từ lỗ giữa bụng tới vòng cầm dưới tay trái.", ""]
    for k, (vi, vi2, doi) in HUONG2.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_2_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: REDESIGN. Redraw the creature of image 1 as ONE picture of a little WILD IRON BEAST: a wild animal-like creature "
              "with raw IRON ORE growing on its head and a SAW on the end of its tail: the SAME creature in the SAME pose, with EVERY "
              "piece in the same place, at the same size, with the same overlaps (if the new picture were laid over image 1, every piece "
              "must coincide), except the shape changes described below; new colours and our hand-drawn drawing style. Do not remove, "
              "merge or move pieces; add only the one new piece listed. Keep the FACE as in image 1: facing right, ONE eye only, its "
              "top half cut by the edge of the head-piece above it, no mouth.", "",
              HOANG, "",
              MO_TA_CON, ""] + vi_tri + ["",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              "Every leg, paw and the tail base stay JOINED to the body (no white gap between a limb and the body); every piece whole "
              "and unbroken.", "",
              KHONG, "",
              STYLE, "",
              "Mood: a tough, fierce little wild beast ready to fight (a game hero), not a cute mascot, not scary.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the creature at the same "
              "place and size as in image 1. No sparks, no smoke, no motion lines, no glow, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Kiểm: như lượt 1, thêm: không còn mũ, ống, khe, bu lông; quặng là cục / chùm thô (không phải tinh thể nhọn); đuôi đúng dáng "
           "con gốc (đĩa 8 răng vuông, không thành lưỡi cưa tròn); tay là chân thú ba vuốt; dây giật ngắn, không chạm tay phải.", "",
           "Câu sửa nhanh: \"keep the tail exactly like image 1: oblong plate with a hub, disc with 8 blunt square teeth\"; \"the cord goes "
           "from a hole in the belly to the ring under the left hand only\"."]
    ghi(hd_p, hd)


# Lượt 3 (người dùng 2026-11-16: "làm D nhưng bạn sửa lại đầu/mặt đi chút cho đỡ giống con gốc"): sửa trên bản nháp D (KEEP / CHANGE),
# ba kiểu để chọn: D1 đổi mai + sừng, D2 đổi mặt (mõm ngắn, nanh, gờ mày), D3 cả hai. Mọi kiểu dời lỗ dây xuống thấp (bản D lỗ sát cằm).
SUA_MAI = ["HEAD SHELL: instead of one smooth cowl, make it a shell of THREE overlapping ARMOUR BANDS like an armadillo or a pangolin, "
           "running across the head from front to back (each band a curved plate whose back edge overlaps the next, a thin ink line between "
           "bands, all the same flat dark slate as in image 1). The front band is a heavy BROW over the eye: its lower edge is a thick, "
           "slightly arched line still cutting across the top half of the eye. REMOVE the long point that comes down at the lower right of "
           "the face in image 1: the shell now ends at the cheek in a short rounded edge level with the middle of the eye, so more of the "
           "pale round face shows below and to the right of the eye. On the top of the head the shell covers about the same area as before; "
           "the small scalloped bumps along its top are replaced by the band edges.",
           "HORN: shorter and THICKER, curving forward over the top of the head like a hook (its tip pointing to the right, not up), growing "
           "from the same place at the upper left of the shell, same colours (dark slate, rusty-orange underside)."]
SUA_MAT = ["SNOUT: the lower right part of the pale round face (below and to the right of the eye) bulges out to the right into a short, "
           "blunt, rounded MUZZLE with one small dark nostril dot near its tip, a CLOSED mouth line along its underside and ONE small white "
           "FANG pointing down from the mouth line near the tip. Small and simple, not a long dog snout.",
           "BROW: the front edge of the shell over the eye becomes a thick brow ridge with a small downward notch above the eye (a fierce "
           "frown), still cutting across the top half of the eye."]
SUA_MAT_MAI_DAI = ("The long point of the shell that comes down at the lower right of the face now stops ABOVE the snout, level with the "
                   "bottom of the eye.")
SUA_VAN = ("FACE MARKINGS: replace the three grey stripes on the left of the face with TWO short slanted rust-orange #B5622E marks on the "
           "cheek, below and to the left of the eye (like war paint).")
SUA_DAY = ("CORD: move the cord's HOLE lower: a small hole LOW on the belly, between the two legs, well below the face; the short cord goes "
           "from that hole up to the SAME ring under the left paw. Nothing on or near the face may look like a mouth holding a cord.")
KIEU3 = {
    "D1": ("đổi mai + sừng", "mai thành ba đốt giáp chồng nhau kiểu tê tê, đốt trước là gờ mày dày cắt nửa trên mắt, bỏ mũi nhọn chạy xuống má "
           "phải (lộ thêm mặt); sừng ngắn dày quặp về trước như móc; vằn mặt thành hai vạch gỉ cam chéo trên má; dời lỗ dây xuống thấp",
           SUA_MAI + [SUA_VAN, SUA_DAY]),
    "D2": ("đổi mặt", "thêm mõm ngắn tròn bên phải dưới mắt (một chấm mũi, miệng ngậm, một nanh trắng nhỏ), gờ mày có khấc nhíu; mũi nhọn của "
           "mai dừng phía trên mõm; giữ mai, sừng như D; vằn mặt thành hai vạch gỉ cam; dời lỗ dây xuống thấp",
           SUA_MAT + [SUA_MAT_MAI_DAI, SUA_VAN, SUA_DAY]),
    "D3": ("đổi cả mai, sừng và mặt", "gộp D1 + D2: mai ba đốt giáp, sừng móc, mõm ngắn có nanh, gờ mày nhíu, vằn gỉ cam, dời lỗ dây",
           [SUA_MAI[0].replace("REMOVE the long point that comes down at the lower right of the face in image 1: the shell now ends at the "
                               "cheek in a short rounded edge level with the middle of the eye, so more of the pale round face shows below "
                               "and to the right of the eye.",
                               "REMOVE the long point that comes down at the lower right of the face in image 1: the shell now ends at the "
                               "cheek in a short rounded edge level with the middle of the eye, above the new snout."),
            SUA_MAI[1], SUA_MAT[0], SUA_MAT[1].replace("the front edge of the shell", "the front band's edge"), SUA_VAN, SUA_DAY]),
}


def prompt_sua_dau():
    """lượt 3: sửa đầu / mặt trên bản nháp D, ba kiểu D1 D2 D3."""
    nhap = os.path.join(G.TAI, "L1_D.png")
    goc = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(nhap, "OUR DRAFT, 1536x1024, white background: a wild little iron beast facing right, a dark slate shell over its head with a "
                "curved horn at the upper left, iron ore columns with rusty tops on the back of its head, one big amber slit-pupil eye, "
                "small clawed paws, a ring-pull cord on the belly, and a tail with an oblong plate, a hub and a toothed disc. KEEP "
                "everything of it except what is listed under CHANGE.",
          "Bản nháp D người dùng chọn (mai đá sẫm, sừng cong, quặng cột đầu gỉ, mắt hổ phách đồng tử dọc, đuôi như con gốc)"),
         (goc, "the creature our draft was based on (another design, painted digitally), 1536x1024. Our hero's HEAD and FACE must look LESS "
               "like this one: use it only to see what to move away from. Do not copy anything from it.",
          "Hình con gốc: chỉ để biết phải đi XA khỏi nó ở đầu, mặt")]
    hd_p = os.path.join(GUI, "HUONG_DAN.md")
    hd = open(hd_p, encoding="utf-8").read().rstrip("\n").split("\n") if os.path.exists(hd_p) else []
    if any(x.startswith("## Lượt 3") for x in hd):
        hd = hd[:hd.index(next(x for x in hd if x.startswith("## Lượt 3")))]
    hd += ["", "## Lượt 3: sửa đầu / mặt bản D cho đỡ giống con gốc (2026-11-16)", "",
           "Người dùng: \"làm D nhưng bạn sửa lại đầu/mặt đi chút cho đỡ giống con gốc\". Ảnh mẫu 1 = bản nháp D (giữ mọi thứ khác), ảnh 2 = "
           "con gốc (chỉ để biết đi xa khỏi nó). Ba kiểu, mỗi file một kiểu:", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in KIEU3.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_3_dau_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: EDIT image 1 (our draft). Redraw it on the same 1536x1024 canvas, same pose, every piece in the same place and at the "
              "same size: if the new picture were laid over image 1, everything outside the changed parts must coincide exactly. Change "
              "ONLY the head and face as listed, so the head looks clearly less like image 2.", "",
              "KEEP IDENTICAL (as in image 1): the whole tail (oblong housing plate, hub with its thin rusty ring, disc with 8 square "
              "pale teeth); the body; both legs and the ribbed left thigh; both paws with their claws; the ring of the pull cord under the "
              "left paw; the three iron ore columns with rusty tops and the small ore lump behind the head (same shapes, places, sizes); "
              "the single round amber eye with its slit pupil and white dot (same place and size, its top half cut by the edge of the "
              "shell above it); facing right; all colours; the drawing style (wobbly dark-brown ink outline, visible crayon hatching, "
              "flat colours, no shading, no highlights, no glow).", "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              "Every leg, paw and the tail base stay JOINED to the body; every piece whole and unbroken. Very simple design, few details: "
              "add nothing that is not listed (no scars, no cracks, no extra spikes, no bolts).", "",
              "Mood: a tough, fierce little wild beast ready to fight (a game hero), not a cute mascot, not scary.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **{k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Kiểm: ngoài đầu, mặt, vằn và lỗ dây thì chồng lên D phải trùng; vẫn một mắt, mép mai cắt nửa trên mắt; lỗ dây thấp giữa hai "
           "chân, không gì trên mặt trông như miệng ngậm dây (trừ miệng ngậm của mõm ở D2, D3)."]
    ghi(hd_p, hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "sua_dau":
        prompt_sua_dau()
    elif cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    elif cmd == "concept2":
        prompt_concept2()
    else:
        print(__doc__)
