# -*- coding: utf-8 -*-
"""Chiến binh đất nung (dat_nung, rig monster_3625): ĐỔI DA THEO KHUNG TỪNG PART của con gốc (người dùng 2026-11-14, sau khi xem bản tự chế:
"không được, concept này chưa đạt, làm giống con gốc, mổ xẻ kĩ con gốc ra làm theo"). Mọi part giữ nguyên hình bóng, cỡ, chỗ, đường cấu trúc;
chỉ đổi chất liệu, màu, nét vẽ (đất nung, đá dung nham, lõi dung nham; bút mực + chì sáp, tô phẳng). Rig dùng NGUYÊN lưới của họ.

    dat_nung_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/dat_nung_1/mau/goc_ca_con.png (ảnh mẫu của lượt concept)
    dat_nung_da.py to         sáu tờ mảnh GỐC cắt theo lưới, phóng to → mau/goc_<A..F>.png + .json; prompt gui_gpt/dat_nung_1/luot_3_*.txt
    dat_nung_da.py cat        cắt tờ Codex trả (tai_ve/D_<A..F>.png) theo ô → inbox/dat_nung_1/manh_part/<ảnh vùng>.png (ảnh vùng × 2), IoU,
                              tờ so manh_part/_so_<tờ>.png
Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dat_nung as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
RES = 2
MANH = os.path.join(G.BASE, "manh_part")
GUI = os.path.join(HERE, "gui_gpt", "dat_nung_1")
CONCEPT = os.path.join(G.TAI, "L2_duyet.png")
GOLEM = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")
QUY = os.path.join(HERE, "inbox", "quy_dao_1", "tai_ve", "L1_duyet.png")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DAT, DAT_SAM, NHAM, LAVA, LOI, MUC = "#C8683C", "#96482C", "#4A3E3C", "#EE7A22", "#FFD64A", "#2B2118"

# tờ → hàng → (ảnh vùng, độ phóng)
NGON = ["P_shouR4_01", "P_shouR4_02", "P_shouR4_03", "P_shouR4_04", "P_shouR4_05", "P_shouR4_06", "P_shouR4_07", "P_shouR4_08", "P_shouR4_09",
        "P_shouR4_10", "P_shouR4_11"]
TO = {
    "A": [[("P_tou", 2.0), ("P_jianjiaR1", 2.0), ("P_jianjiaL2", 2.0)],
          [("P_jianjiaL1", 2.0), ("P_jianjiaR2", 2.0), ("P_shouL1", 2.0), ("P_huoyan17", 2.6)]],
    "B": [[("P_shouL2_2", 2.2), ("P_shouL2_1", 2.2), ("P_shouL4_1", 2.2), ("P_dun01", 2.2)],
          [("P_shouL3_1", 2.2), ("P_shouL3_3", 2.2), ("P_shouL3_2", 2.2), ("P_shouL4_2", 2.6)]],
    "C": [[("P_dun10", 1.7), ("P_dun07", 1.7), ("P_dun09", 1.7), ("P_dun08", 1.7), ("P_dun05", 1.7)],
          [("P_dun06", 1.7), ("P_dun04", 1.7), ("P_dun12", 1.7), ("P_dun11", 1.7)]],
    "D": [[("P_wuqi", 1.5), ("P_huoyan20", 2.0), ("P_dun03", 2.0)]],
    "E": [[("P_dun02", 2.2), ("P_jianjiaR4", 2.2), ("P_shenti1_1", 2.4), ("P_jianjiaL3", 2.2), ("P_shenti1_3", 2.4)],
          [("P_jianjiaR3", 2.2), ("P_jianjiaL4", 2.2), ("P_jianjiaR5", 3.0), ("P_jianjiaL5", 3.0), ("P_shenti1_2", 2.4)]],
    "F": [[("P_shouR2", 2.6), ("P_shouR3", 2.6), ("P_shouR4", 2.6), (NGON[0], 4.4), (NGON[1], 4.4)],
          [(n, 4.4) for n in NGON[2:7]],
          [(n, 4.4) for n in NGON[7:]]],
}


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vung():
    """{ảnh vùng: (hình đầu tiên dùng vùng đó, ảnh part cắt theo lưới)}."""
    G.Q._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in sorted(D["atts"], key=lambda q: (not q["cur"], q["order"])):
        r = a.get("region")
        if r in imgs and r not in out and a["slot"] not in ("shadow", "wangge"):
            out[r] = (a, G.part_goc(a))
    return out


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024 (đúng khung của sơ đồ bố cục cũ: 0,74 px / đơn vị)."""
    import dat_nung_bo_cuc as B
    imgs, atts = B.nap()
    T, _ = B.khung_T(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))            # mỗi part một lớp trong suốt rồi mới chồng (vẽ thẳng lên nền thì ô
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)     # tam giác đè đen lên phần đã vẽ)
        can.alpha_composite(lay.convert("RGBA"))
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    print(p)


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
        if ke_y < 10:
            raise SystemExit(f"tờ {ma}: quá cao ({sum(c[1] for c in cao)} px)")
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3] for c in cs)) // (len(cs) + 1)
            if ke < 14:
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


# ---------------------------------------------------------------- prompt
LOOK = (
    f"NEW LOOK: a TERRACOTTA WARRIOR GOLEM with a heart of lava. MATERIALS AND COLOURS (use exactly these, each area ONE flat colour): the "
    f"ARMOUR (every carved armour plate, the head, the arm pieces, the fists, the sword guard) is FIRED CLAY, terracotta orange-brown ({DAT}); "
    f"the under sides, inner faces, side faces and bevels of those pieces (the faces that are a darker tone in the reference) are darker "
    f"brick-brown clay ({DAT_SAM}); the engraved patterns are simple carved GROOVES drawn as darker brick-brown lines ({DAT_SAM}); the big "
    f"curved BACK PLATES that fan out behind the body, the finger joints, the round pegs / studs, the sword blade and the small dark "
    f"lower pieces are cooled LAVA ROCK, warm charcoal brown-black ({NHAM}); MOLTEN LAVA is flat orange ({LAVA}); the small round CORE, the "
    f"eyes and the thin bright lines are bright lava yellow ({LOI}).")
STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game: a wobbly dark-brown INK outline ({MUC}, about "
    "{px} px) running all the way round every part exactly on its silhouette, thinner ink or dark pencil lines for the inner structural "
    "edges (the edges between faces, plates and fingers), and every area filled with ONE flat colour with visible coloured-pencil / "
    "wax-crayon hatching. The reference is painted in a smooth digital cel style with grey-green stone, teal highlights and light / dark "
    "shading: do NOT copy that painting style or those colours: no shading, no highlights, no gradients, no glow, no shadows, no shine: "
    "flat colour only. A different tone appears only where a different face or material is listed.")
BG = "Plain pure-white background (#FFFFFF), no paper grain outside the drawing, no labels, no numbers, no frame, nothing added."
CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of the separate PARTS of a 2D animation puppet (a floating stone-armour golem with a big sword), each "
    "part drawn alone on white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on "
    "the same puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
    "(if the new picture were laid over image 1, every part must coincide with the old one), and its main structural lines (the edges "
    "between faces and bevels, the lines between fingers, the edge of a carved band). Do NOT merge parts, do NOT add parts, do NOT move, "
    "rotate or resize parts. Pure white (#FFFFFF) between the parts.")

MO_TA = {
    "A": [("P_tou", "HEAD: a horned helmet-head: two tall horns, a block-shaped face with a brow ridge, two small eyes and two thin tusk-like "
                    "stripes. Terracotta clay; the side faces and under-faces darker clay; the engraved marks on the horns and brow as "
                    "simple darker grooves; the two EYES bright lava yellow; the two thin stripes under the eyes flat lava orange."),
          ("P_jianjiaR1", "BIG SHOULDER PLATE with an engraved square-spiral pattern and a curved hook on top: terracotta clay; its side "
                          "face darker clay; keep the square-spiral as ONE bold carved groove (darker clay lines), simplified."),
          ("P_jianjiaL2", "LONG CURVED COLLAR BAND with a square block at one end: terracotta clay, the side face darker clay, the engraved "
                          "angular mark as a darker groove; the thin bright rim along its inner edge flat lava orange."),
          ("P_jianjiaL1", "BIG SHOULDER PLATE with an engraved square-spiral and three small squares: terracotta clay, side face darker "
                          "clay, the engraving as bold darker grooves."),
          ("P_jianjiaR2", "CURVED COLLAR BAND with a block on top and an engraved square-spiral at the bottom: terracotta clay, side face "
                          "darker clay, the spiral a darker groove; the thin bright rim along its inner edge flat lava orange."),
          ("P_shouL1", "SHOULDER JOINT: a round ball joint behind a square block with an engraved square plate: the round ball cooled lava "
                       "rock (charcoal); the square block terracotta clay with darker-clay side faces; the engraved lines darker grooves."),
          ("P_huoyan17", "THE CORE: a small round disc with concentric rings: bright lava yellow with ONE orange ring line; flat, no glow.")],
    "B": [("P_shouL2_2", "UPPER-ARM SLAB with a round peg standing on it (a T-shaped engraved mark under the peg): the slab terracotta clay "
                         "with darker-clay side faces; the round peg and its stem cooled lava rock (charcoal); marks as darker grooves."),
          ("P_shouL2_1", "UPPER-ARM SLAB with a round peg: the same: terracotta slab, darker-clay side faces, charcoal lava-rock peg (its "
                         "engraved band a darker line)."),
          ("P_shouL4_1", "FIST: a big gauntlet fist, four fingers with round knuckle studs, a cuff with a curl mark: terracotta clay; the "
                         "lines between the fingers ink; the round studs charcoal lava rock; the engraved marks darker grooves."),
          ("P_dun01", "TALL ARM PLATE with an engraved angular pattern: terracotta clay, its side face darker clay, the pattern darker grooves."),
          ("P_shouL3_1", "FOREARM SLAB (a wide flat slab with cracked surface lines): terracotta clay, side faces darker clay; keep two or "
                         "three crack lines as thin dark lines."),
          ("P_shouL3_3", "FOREARM UNDER-SLAB: darker brick-brown clay, its side face cooled lava rock (charcoal)."),
          ("P_shouL3_2", "FOREARM ROD (a short cylinder): cooled lava rock (charcoal)."),
          ("P_shouL4_2", "small dark THUMB block: cooled lava rock (charcoal).")],
    "C": [("P_dun10", "BIG BACK PLATE (a long curved blade-like slab with an engraved pattern near one end): cooled LAVA ROCK, warm "
                      "charcoal; its narrow side face a slightly lighter charcoal-brown; replace the engraved pattern by ONE thin zigzag "
                      "CRACK of flat orange lava along the middle of its broad face."),
          ("P_dun07", "BIG BACK PLATE (curved slab): the same: charcoal lava rock, narrow side face slightly lighter, one thin orange lava crack."),
          ("P_dun09", "BACK PLATE (curved slab): the same."), ("P_dun08", "NARROW BACK PLATE (a thin upright blade): the same, a very short crack."),
          ("P_dun05", "NARROW BACK PLATE with an engraved pattern: the same: charcoal lava rock, the pattern replaced by one thin orange lava crack."),
          ("P_dun06", "BACK PLATE (curved slab seen from the side): charcoal lava rock, side face slightly lighter."),
          ("P_dun04", "BACK PLATE (a curved fan-shaped slab): charcoal lava rock, side face slightly lighter."),
          ("P_dun12", "BACK PLATE (curved slab): charcoal lava rock, side face slightly lighter."),
          ("P_dun11", "SMALL BACK PLATE: charcoal lava rock, side face slightly lighter.")],
    "D": [("P_wuqi", "THE SWORD (tip at the top): keep its exact shape. The BLADE is cooled lava rock (charcoal) with its bevelled edges a "
                     "slightly lighter charcoal-brown; the dark central channel of the blade stays dark charcoal and the bright chain-like "
                     "rune line inside it becomes MOLTEN LAVA: flat orange with a thin bright-yellow centre, the same angular zigzag path, "
                     "simplified; the GUARD block is terracotta clay; the GRIP and the round POMMEL cooled lava rock (dark charcoal)."),
          ("P_huoyan20", "THE LAVA HEART: a big plain round disc: flat MOLTEN-LAVA orange, with five or six small darker-orange crust "
                         "patches (#C8581E) spread over it; one ink outline; no glow."),
          ("P_dun03", "SIDE PLATE (a big pointed triangular slab): terracotta clay; its narrow side face darker clay.")],
    "E": [("P_dun02", "SIDE PLATE (a pointed triangular slab): terracotta clay; its narrow lower face darker clay."),
          ("P_jianjiaR4", "small curved armour piece: darker brick-brown clay; its thin bright edge flat lava orange."),
          ("P_shenti1_1", "LOWER BODY piece (a socket-like block with a dark hollow and a pointed lower end): the block terracotta clay, "
                          "the hollow and the dark cap cooled lava rock (charcoal)."),
          ("P_jianjiaL3", "small block (a bar seen from the side): terracotta clay, its side face darker clay."),
          ("P_shenti1_3", "small pointed piece with a bright edge: cooled lava rock (charcoal); its bright edge flat lava orange."),
          ("P_jianjiaR3", "small flat bar: darker brick-brown clay."),
          ("P_jianjiaL4", "small curved armour piece with an engraved mark: terracotta clay, the mark a darker groove; its thin bright edge "
                          "flat lava orange."),
          ("P_jianjiaR5", "tiny pointed piece: cooled lava rock (charcoal); its bright edge flat lava orange."),
          ("P_jianjiaL5", "tiny flat piece: cooled lava rock (charcoal)."),
          ("P_shenti1_2", "small flat piece: cooled lava rock (charcoal).")],
    "F": [("P_shouR2", "FAR UPPER ARM: a chunky block: darker brick-brown clay with terracotta top face."),
          ("P_shouR3", "FAR FOREARM: a ribbed block of three rounded bars: terracotta clay, the grooves between the bars ink."),
          ("P_shouR4", "FAR PALM: a rounded block with a round boss: terracotta clay; the round boss darker clay.")]
         + [(n, "FINGER JOINT of the open far hand (a small chunky block): cooled lava rock (charcoal), one facet line.") for n in NGON],
}
VI = {"A": "đầu hai sừng, giáp vai xa, vành cổ dài, giáp vai gần, vành cổ ngắn, khớp vai, viên lõi",
      "B": "hai tấm bắp tay có chốt tròn, nắm tay, tấm dựng; tấm cẳng tay, tấm dưới cẳng tay, thanh trụ, mẩu ngón cái",
      "C": "chín phiến đá cong xoè sau lưng",
      "D": "thanh kiếm, quầng dung nham tròn, phiến bên nhọn",
      "E": "phiến bên thứ hai, các mảnh giáp nhỏ quanh ngực, ba mảnh thân dưới",
      "F": "bắp tay xa, cẳng tay xa, lòng bàn tay xa, mười một đốt ngón (phóng 4,4 lần)"}
SO_PART = {"A": "seven parts in two rows: a horned head, two big shoulder plates, two curved collar bands, a shoulder joint, a small round core",
           "B": "eight parts in two rows: two arm slabs with round pegs, a fist, a tall plate; a forearm slab, an under-slab, a short rod, a "
                "small thumb block",
           "C": "nine curved back plates in two rows", "D": "three parts in one row: a big sword (tip up), a big round disc, a pointed triangular slab",
           "E": "ten small armour pieces in two rows", "F": "fourteen parts in three rows: three arm blocks and eleven very small finger joints drawn very big"}


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


def prompt_concept():
    """lượt concept MỚI: vẽ lại cả con gốc (đúng dáng, đúng từng mảnh) bằng chất liệu, màu, nét của mình."""
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    out, save = luu("L2_theo_goc")
    p = os.path.join(GUI, "luot_1c_concept_theo_goc.txt")
    R = [(mau, "the REFERENCE creature, 1536x1024, white background: a floating stone-armour golem warrior (no legs) made of separate carved "
               "armour pieces: a horned helmet-head in the middle of a hollow chest that holds a big round disc with a small bright core, two "
               "big engraved shoulder plates, curved collar bands, many big curved plates fanned out behind it, a far open hand at the lower "
               "left, a near arm of stacked slabs with round pegs across the bottom ending in a big fist that holds a huge sword upright at the "
               "left. It is painted in a smooth digital cel style in grey-green. Keep its SHAPES, change its LOOK.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): golem giáp đá lơ lửng xám lục, đầu hai sừng, lõi tròn giữa ngực, hai giáp vai "
          "khắc xoắn vuông, chùm phiến cong sau lưng, tay gần vắt ngang nắm kiếm lớn dựng chéo bên trái. Giữ hình, đổi chất liệu"),
         (GOLEM, "an approved hero of our game (a rock golem with flames), 1536x1024, white background: match EXACTLY its wobbly dark-brown "
                 "pen line, its visible crayon hatching and its completely flat colouring. Do NOT copy its design or colours.",
          "Golem lõi lửa đã duyệt (1536 × 1024, nền trắng): lấy nét bút rung, vân sáp, tô phẳng"),
         (QUY, "another approved hero of our game (a fire demon with a huge blade), 1536x1024, white background: the same line and flat "
               "crayon colouring; see how its armour and weapon are drawn. Do NOT copy its design or colours.",
          "Quỷ lửa vác đao đã duyệt (1536 × 1024, nền trắng): lấy nét, tô phẳng, cách vẽ giáp và vũ khí")]
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += [""] + save + ["",
          "TASK: RESTYLE. Redraw the creature of image 1 as ONE picture: the SAME creature in the SAME pose, with EVERY piece in the same "
          "place, at the same size, with the same silhouette and the same overlaps (if the new picture were laid over image 1, every piece "
          "must coincide), but with a NEW LOOK: new materials, new colours and our hand-drawn drawing style. Do not add, remove, merge or "
          "move pieces; keep the white gaps between pieces where image 1 has gaps.", "",
          LOOK, "",
          "PIECE BY PIECE: the HEAD (horned helmet), the two big SHOULDER PLATES, the curved COLLAR BANDS, the three flat pointed SIDE "
          "PLATES (two at the left behind the sword, one tall plate at the right in front of the arm), the arm SLABS and the big FIST: "
          "terracotta clay, their side faces and under-faces darker clay. The many big curved BACK PLATES fanned out behind the body: cooled "
          "lava rock (charcoal), each with ONE thin zigzag crack of orange lava instead of an engraved pattern. The big round disc in the "
          "chest: the LAVA HEART, flat orange with a few darker crust patches; the small round ball on it: the bright-yellow CORE with one "
          "orange ring. The round pegs on the arm slabs, the ball of the shoulder joint, the finger joints of the open hand, the dark lower "
          "pieces: cooled lava rock (charcoal). The SWORD: a charcoal lava-rock blade whose bright rune line becomes a zigzag line of "
          "orange-and-yellow lava, a terracotta guard, a charcoal grip and pommel. The EYES bright lava yellow. Simplify the engraved "
          "patterns of the armour into a few bold carved grooves (keep one square-spiral on each shoulder plate).", "",
          STYLE.format(px="6"), "",
          "CANVAS: landscape 1536x1024, pure-white background, no ground line, no cast shadow; the creature at the same place and size as "
          "in image 1. No dust, sparks, embers, smoke, flames or glow.", BG]
    ghi(p, t)
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1c")[0].rstrip("\n") if os.path.exists(hd) else ""
    gd = ["", "## Lượt 1c: concept THEO CON GỐC (2026-11-14; người dùng bỏ bản tự chế: \"làm giống con gốc, mổ xẻ kĩ con gốc ra làm theo\")", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…). Bản được duyệt chép thành `L2_duyet.png`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "Kiểm: đúng dáng, đúng từng mảnh như ảnh 1 (chồng lên phải trùng); giáp màu đất nung cam, mặt bên sẫm; chùm phiến sau lưng đá than "
           "có khe dung nham cam; đĩa dung nham cam + viên lõi vàng; kiếm đá than có đường dung nham; nét bút mực rung, vân sáp, tô phẳng, không "
           "bóng, không phát sáng; nền trắng tinh. Ảnh 1 là hình của game tham khảo: chỉ dùng trong máy, không đăng công khai."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))
    print(p)


def prompt_da(O):
    if not os.path.exists(CONCEPT):
        raise SystemExit("chưa có concept theo con gốc đã chọn " + Wp(CONCEPT))
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3")[0].rstrip("\n")
    gd = ["", "## Lượt 3: đổi da theo khung từng part (2026-11-14)", "",
          "Sáu tờ A–F là các mảnh GỐC cắt ra từ rig (phóng to); GPT vẽ lại da đúng chỗ, đúng cỡ, đúng hình bóng từng mảnh. Ảnh mảnh gốc là của game "
          "tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai.", ""]
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out, save = luu(f"D_{ma}")
        p = os.path.join(GUI, f"luot_3_da_{ma}.txt")
        R = [(mau, f"the PARTS SHEET, 1536x1024, white background: separate parts of the puppet, each drawn alone, at the exact size and "
                   f"place to keep ({SO_PART[ma]}). Painted in a smooth digital cel style in grey-green: keep the shapes, change the look.",
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng {min(z for h_ in TO[ma] for _, z in h_)}–"
              f"{max(z for h_ in TO[ma] for _, z in h_)} lần: {VI[ma]}. Hình cel số màu xám lục"),
             (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: the same golem redrawn as a terracotta warrior "
                       "with charcoal lava-rock back plates, an orange lava heart with a yellow core and a lava-rock sword. Take from it the "
                       "exact colours, the materials of each piece and the hand-drawn look (wobbly brown ink line, crayon hatching, flat "
                       "colour).",
              "Concept theo con gốc đã chọn (1536 × 1024, nền trắng): lấy màu, chất liệu từng mảnh, nét vẽ tay")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += [""] + save + ["", CHUNG, "", LOOK, "", STYLE.format(px={"A": "6", "B": "6", "C": "6", "D": "6", "E": "6", "F": "8"}[ma]), "",
                            "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        t += [f"{i}. ({cho(o, r)}) {mt}" for i, (r, mt) in enumerate(MO_TA[ma], 1)]
        t += ["", BG]
        ghi(p, t)
        gd += [f"- **`{ma}`** ({VI[ma]}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…). Ảnh mẫu 1 = "
               f"`{Wp(mau)}` (tờ mảnh gốc), ảnh mẫu 2 = `{Wp(CONCEPT)}` (concept theo con gốc)."]
        print(p)
    gd += ["", "Kiểm từng tờ: mỗi mảnh trùng hình bóng, chỗ, cỡ với tờ mảnh gốc (Claude đo IoU bằng `dat_nung_da.py cat`, đích ≥ 0,9); màu đúng "
           "bảng (đất nung cam, mặt bên sẫm, đá than, dung nham cam, lõi vàng); tô phẳng, không bóng, không phát sáng; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- lượt 4: concept MẶT + GIÁP mới (người dùng 2026-11-14: "nhìn ổn nhưng gen
# lại mặt cho khác đi, giáp xung quanh cũng nên gen lại cho khác"): giữ dáng, tay, kiếm, lõi; đầu và các tấm giáp đổi KIỂU DÁNG, vẫn đúng chỗ, cỡ
MG = {
    "1": ("mũ trụ mào lưỡi, giáp ngói xếp lớp",
          "THE HEAD: a rounded terracotta DOME HELMET (no tall horns). Along its top, from front to back, stands ONE tall thin CREST BLADE of "
          "charcoal lava rock shaped like an axe blade, about as tall as the old horns. The face is a wide dark charcoal VISOR SLOT across "
          "the front of the helmet with TWO angular bright-yellow eyes in it, slanted and determined; under the slot a short pointed clay CHIN "
          "guard; a darker-clay brow band over the slot with three small round studs; ONE thin orange lava crack down one cheek.",
          "THE TWO BIG SHOULDER PLATES: each becomes a LAYERED pauldron of THREE overlapping curved terracotta ROOF TILES (like lamellar "
          "armour), each tile with a rounded lower edge and a darker-clay rim, the top tile with a row of three round charcoal studs. No "
          "square-spiral engraving, no hook on top. THE CURVED COLLAR BANDS: each becomes a curved row of five or six separate-looking "
          "rectangular clay BRICKS joined by thin orange lava seams (still ONE piece each, the same curve). THE FLAT SIDE PLATES: each becomes "
          "a KITE-SHAPED clay shield plate with one raised ridge down its middle and a darker-clay rim.",
          "THE BACK PLATES: keep them exactly as in image 1 (charcoal lava-rock curved slabs with orange cracks)."),
    "2": ("mặt nạ thú gốm sừng ngắn, giáp đá vỡ gai",
          "THE HEAD: a broad terracotta BEAST MASK, wider than tall, like a clay guardian mask: a heavy angry V-shaped brow, two big angular "
          "bright-yellow eyes, a flat snout block, and a square JAW plate with a row of four blunt clay teeth; the mouth gap between the teeth "
          "is flat orange lava. Instead of the two tall horns: two SHORT THICK horns of charcoal lava rock that sweep sideways and curve "
          "forward (like a bull), each with an orange lava tip. Fierce and determined but still cute, not scary.",
          "THE TWO BIG SHOULDER PLATES: each becomes a thick ROUGH CLAY SLAB with a broken, jagged lower edge (chipped like broken pottery), "
          "two orange lava cracks running across it, and ONE big cone-shaped SPIKE of charcoal lava rock standing on its upper part. No "
          "square-spiral engraving, no hook. THE CURVED COLLAR BANDS: each becomes a curved band of clay with a row of five or six pointed "
          "charcoal TEETH along its outer edge, like a spiked collar (still ONE piece each, the same curve). THE FLAT SIDE PLATES: each "
          "becomes a jagged pointed SHARD of clay with a chipped edge and one orange crack.",
          "THE BACK PLATES: the same number, the same places and the same directions, but each becomes a JAGGED SHARD of charcoal lava rock "
          "with a notched, broken outline (like obsidian splinters) instead of a smooth curved slab; one thin orange crack each."),
    "3": ("đầu vò gốm khe chữ T, giáp vòm tròn đính ngọc dung nham",
          "THE HEAD: a smooth rounded terracotta POT HELMET, shaped like an upside-down clay jar, slightly taller than wide, with a flat "
          "darker-clay rim band round its top and a short flame-shaped FIN of charcoal lava rock on top of that (much shorter than the old "
          "horns). The face is a T-SHAPED OPENING cut in the front (a wide slot for the eyes and a narrow slot going down): inside it is flat "
          "orange lava with TWO round-cornered bright-yellow eyes, slanted and determined. On each side of the helmet a small flat EAR FIN of "
          "darker clay pointing backwards.",
          "THE TWO BIG SHOULDER PLATES: each becomes a smooth ROUND DOME SHELL of terracotta (like a turtle shell or a big pot lid) with a "
          "thick darker-clay RIM band all round it, four small round charcoal rivets on the rim, and ONE round bright-yellow LAVA GEM with an "
          "orange ring in its middle. No square-spiral engraving, no hook. THE CURVED COLLAR BANDS: each becomes a smooth thick clay RING "
          "segment with a round charcoal rivet at each end and one thin orange line along its middle (still ONE piece each, the same curve). "
          "THE FLAT SIDE PLATES: each becomes a rounded PADDLE-shaped clay plate (round end, no sharp point) with a darker-clay rim.",
          "THE BACK PLATES: the same number, the same places and the same directions, but each becomes a FLAME-TONGUE shape of charcoal lava "
          "rock: a wavy, pointed tongue curling a little at its tip, with an orange lava core line along its middle."),
}


def prompt_mat_giap():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 4")[0].rstrip("\n")
    mau = os.path.join(G.TAI, "L2_theo_goc.png")
    gd = ["", "## Lượt 4: concept MẶT và GIÁP mới (2026-11-14; người dùng: \"nhìn ổn nhưng gen lại mặt cho khác đi, giáp xung quanh cũng nên gen "
          "lại cho khác\")", "",
          "Ba phương án, mỗi phương án một file. Ảnh mẫu duy nhất (ảnh 1) = "
          f"`{Wp(mau)}`: concept theo con gốc đang dùng (1536 × 1024, nền trắng): golem giáp đất nung cam lơ lửng, đầu hai sừng giữa ngực rỗng, "
          "quầng dung nham cam có viên lõi vàng, hai giáp vai khắc xoắn vuông, chùm phiến đá than sau lưng, tay gần vắt ngang nắm kiếm đá than "
          "dựng chéo bên trái. Giữ nguyên tay, kiếm, lõi, dáng; chỉ đổi kiểu dáng đầu và các tấm giáp.", ""]
    for k, (vi, dau, giap, lung) in MG.items():
        out, save = luu(f"L3_{k}")
        p = os.path.join(GUI, f"luot_4_concept_mat_giap_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(mau)}: the CURRENT picture of our character, 1536x1024, white background: a floating terracotta-armour golem "
             "warrior (no legs) made of separate pieces: a horned helmet-head in the middle of a hollow chest, in front of a big round orange "
             "lava disc with a small bright-yellow core; two big engraved shoulder plates (one at the left of the head, one at the right); "
             "curved collar bands round the chest opening; flat pointed side plates at the far right; many big charcoal back plates fanned out "
             "behind it; a far open hand at the lower left; a near arm of stacked slabs with round pegs across the bottom, ending in a big fist "
             "that holds a huge charcoal sword upright at the left. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.",
             ""] + save + ["",
             "TASK: REDESIGN THE HEAD AND THE ARMOUR PLATES of the character of image 1; everything else stays. Draw ONE picture of the SAME "
             "character in the SAME pose, at the same place and size on the canvas.", "",
             "KEEP EXACTLY AS IN IMAGE 1 (same shape, place, size, colours): the SWORD, the near ARM (slabs, round pegs, the big fist), the far "
             "OPEN HAND, the shoulder ball joint, the big round orange LAVA DISC and the small yellow CORE, the small dark pieces under the "
             "chest. Keep the overall layout: the same number of pieces, every piece still a SEPARATE floating piece with white gaps where "
             "image 1 has gaps, the same overlaps (what is in front stays in front).", "",
             "REDESIGN (new shapes, NOT the old shapes repainted). Every redesigned piece stays in the SAME PLACE, covers about the SAME AREA "
             "(not bigger than the old piece by more than a little, not much smaller), points in the SAME DIRECTION and is tilted the same "
             "way as the piece it replaces:", dau, giap, lung, "",
             f"COLOURS AND MATERIALS (each area ONE flat colour): fired clay, terracotta orange-brown ({DAT}), with darker brick-brown clay "
             f"({DAT_SAM}) for side faces, rims and carved grooves; cooled lava rock, warm charcoal brown-black ({NHAM}); molten lava flat "
             f"orange ({LAVA}); eyes, core and gems bright lava yellow ({LOI}). The head looks towards the lower left (towards the sword), "
             "tilted like the old head.", "",
             f"DRAWING STYLE: exactly the hand-drawn style of image 1: a wobbly dark-brown INK outline ({MUC}, about 6 px) round every piece, "
             "thinner lines for inner edges, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, no "
             "highlights, no gradients, no glow, no shadows, no shine. Chunky, simple, few details; a determined fighting look, still cute.", "",
             "CANVAS: landscape 1536x1024, pure-white background, no ground line, no cast shadow. No dust, sparks, embers, smoke, flames or "
             "glow.", BG]
        ghi(p, t)
        gd += [f"- **Phương án {k}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    gd += ["", "Kiểm: tay, kiếm, lõi, quầng dung nham, dáng y như ảnh 1; đầu và các tấm giáp là kiểu dáng MỚI nhưng đúng chỗ, gần đúng cỡ, đúng "
           "hướng mảnh cũ (để lắp lại lên cùng xương); tô phẳng, không bóng, không phát sáng; nền trắng tinh.",
           "Câu sửa nhanh: \"the head is still the old horned head: replace it by the new head described\"; \"the shoulder plate is bigger than "
           "the old one: shrink it to the old size\"; \"remove the glow / shading, flat colour only\"."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
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


def khu_vien(rgb, mm, r=2):
    """dải mép r px của mảnh lấy màu TỐI NHẤT quanh nó: điểm khử răng cưa pha giấy trắng ở mép để lại viền sáng quanh mảnh sẫm."""
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def moi_nhat(tien_to):
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(tien_to) and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def doc(p):
    return np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)


def o_ra(A, lab, st, fgG, d, pad=14):
    """mảnh trong ô d["hop"]: cụm liền nào chạm hình bóng tờ hướng dẫn (nới 10 px) thì lấy; trả RGBA đúng khung ô + mặt nạ."""
    x, y, cw, ch = d["hop"]
    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
    gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
    sub = lab[y0:y1, x0:x1]
    ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
    m = np.isin(lab, ids)
    m[:y0] = m[y1:] = False
    m[:, :x0] = m[:, x1:] = False
    rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
    mm = m[y:y + ch, x:x + cw]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    return Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA"), mm


def to_so(so, p):
    w_ = sum(max(s[0].width, s[1].width) + 10 for s in so)
    hh, h2 = max(s[0].height for s in so), max(s[1].height for s in so)
    out = Image.new("RGB", (w_ + 10, hh + h2 + 30), (150, 150, 150))
    xx = 10
    for vis, kh in so:
        out.paste(vis, (xx, 10))
        out.paste(kh, (xx, hh + 20), kh)
        xx += max(vis.width, kh.width) + 10
    out.save(p)
    print(p)


def cat(chi=None):
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pi = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pi)) if os.path.exists(pi) else {}
    for ma in TO:
        if chi and ma not in chi:
            continue
        src = moi_nhat(f"D_{ma}")
        if not src:
            print(f"tờ {ma}: chưa gen")
            continue
        A = doc(src)
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg, fgG = ~nen(A), Gd.min(2) < 238
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        so = []
        print(f"tờ {ma} ({os.path.basename(src)}):")
        for r, d in o.items():
            im, mm = o_ra(A, lab, st, fgG, d)
            x, y, cw, ch = d["hop"]
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            a2 = np.asarray(im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            a2[..., 3] = np.where(cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool), a2[..., 3], 0)      # giữ trong hình bóng gốc nới 3 px
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            b = fgG[y:y + ch, x:x + cw]
            iou = float((mm & b).sum()) / max(1, (mm | b).sum())
            ious[r] = round(iou, 3)
            vis = np.full((ch, cw, 3), 255, np.uint8)
            vis[mm & b] = (170, 170, 170)
            vis[b & ~mm] = (230, 60, 60)
            vis[mm & ~b] = (60, 190, 60)
            so.append((Image.fromarray(vis), Image.fromarray(a2, "RGBA")))
            print(f"  {r:14s} IoU {iou:.3f}" + ("   <-- THẤP" if iou < 0.9 else ""))
        to_so(so, os.path.join(MANH, f"_so_{ma}.png"))
    json.dump(ious, open(pi, "w"), indent=1)


# ---------------------------------------------------------------- lượt 5: mảnh ĐỔI KIỂU DÁNG (đầu, giáp) theo concept mặt + giáp đã chọn
MANH2 = os.path.join(G.BASE, "manh_part2")
CONCEPT2 = os.path.join(G.TAI, "L3_duyet.png")
NGUON2 = None                                             # thư mục mảnh có lề dùng làm hình trong tờ hướng dẫn (dạng 1: mảnh dạng 2); None = manh_part/
LUOT2 = dict(so="5", tep="luot_5_manh_moi_", ten="mảnh ĐỔI KIỂU DÁNG (đầu, giáp) theo concept mặt + giáp đã chọn (2026-11-14)",
             cu="OLD", anh2="the APPROVED picture of our character with its NEW head and NEW armour, 1536x1024, white background: a floating "
                           "terracotta-armour golem with a lava heart, holding a huge sword at the left. Take from it the NEW DESIGN of each "
                           "piece (its shape, details, colours) and the hand-drawn look.",
             vi2="Concept mặt + giáp mới đã chọn (1536 × 1024, nền trắng): lấy kiểu dáng mới, màu, nét của từng mảnh")
LE_TO = {"G": 70, "K": 130, "H": 60, "I": 34, "W": 110}             # lề quanh ô trên tờ (px tờ): hình mới được lấn ra ngoài khung part chừng này
TO2 = {
    "G": [[("P_tou", 1.8), ("P_jianjiaL2", 1.8), ("P_jianjiaR2", 1.8)]],
    "K": [[("P_jianjiaR1", 2.0), ("P_jianjiaL1", 2.0)]],
    "H": [[("P_dun01", 2.2), ("P_dun03", 2.0), ("P_dun02", 2.2)]],
    "I": [[(r, 1.5) for r, _ in h_] for h_ in TO["C"]],
}
# kiểu dáng mới từng mảnh theo concept đã chọn L3_duyet.png (phương án 2: mặt nạ thú gốm sừng ngắn, giáp đá vỡ có gai)
_PHIEN = ("BACK PLATE: a JAGGED SHARD of cooled lava rock (charcoal), like an obsidian splinter: the same length, the same curve and the "
          "same direction as the old slab, but its outline is NOTCHED and BROKEN (three to five angular notches and chipped corners along "
          "both long edges, a broken pointed tip) instead of smooth; its narrow side face a slightly lighter charcoal-brown; ONE thin "
          "forked crack of flat orange lava along the middle of its broad face.")
TA2 = {
    "P_tou": "THE HEAD, a broad terracotta BEAST MASK seen from the front, turned a little to the lower left: about 400 px wide (with the "
             "horns) and 320 px tall, standing in the LOWER two thirds of the old box (its jaw at the bottom of the old box; nothing as "
             "tall as the old horns). A heavy angry V-shaped brow block; two big angular bright-yellow eyes under it; a flat snout block "
             "between them; a square JAW plate with a row of four blunt clay teeth, the gap between and under the teeth flat orange lava. "
             "On each side of the head a round clay ring boss, and out of each grows ONE SHORT THICK HORN of charcoal lava rock that sweeps "
             "sideways and curves upward like the horn of a bull, with an orange lava tip. Side faces darker clay. Fierce, determined, "
             "still cute.",
    "P_jianjiaL2": "THE LONG CURVED COLLAR BAND: the same curve, length and width as the old band, terracotta clay with a darker-clay side "
                   "face, and a row of five or six pointed charcoal lava-rock TEETH (small cones) standing along its OUTER (convex) edge, "
                   "like a spiked collar; instead of the old square block at its end, the band ends in one bigger charcoal tooth.",
    "P_jianjiaR2": "THE SHORT CURVED COLLAR BAND: the same curve and size as the old one, terracotta clay with a darker-clay side face, a "
                   "row of four pointed charcoal lava-rock teeth along its outer (convex) edge; the block across its top becomes a chunky "
                   "rough clay block with chipped corners.",
    "P_jianjiaR1": "THE FAR SHOULDER PLATE: a thick ROUGH CLAY SLAB about as wide and as tall as the old plate, with a BROKEN, JAGGED lower "
                   "edge (chipped like broken pottery, four or five angular chips), a darker-clay side face along that broken edge, and a "
                   "network of two or three thin orange lava cracks on its broad face. On its upper part stands ONE big cone-shaped SPIKE "
                   "of charcoal lava rock (about 110 px tall, a slightly lighter facet on one side), pointing up and a little outwards; "
                   "the spike may stick out above the old outline. No square-spiral engraving, no curved hook.",
    "P_jianjiaL1": "THE NEAR SHOULDER PLATE: the same design as the other shoulder plate: a thick rough terracotta slab about as wide and "
                   "as tall as the old plate, a broken jagged lower edge with a darker-clay side face, two or three thin orange lava "
                   "cracks, and ONE big cone-shaped charcoal SPIKE (about 110 px tall) standing on its upper part, pointing up and a little "
                   "outwards; the spike may stick out above the old outline. No square-spiral engraving.",
    "P_dun01": "THE TALL SIDE PLATE: a tall JAGGED SHARD of terracotta clay, the same height and width as the old plate, pointed at the "
               "bottom, with chipped, notched long edges, a darker-clay side face, and one thin forked orange lava crack down its middle.",
    "P_dun03": "A POINTED SIDE PLATE: a jagged pointed SHARD of terracotta clay, the same size and direction as the old triangular slab, "
               "with a chipped notched edge, a darker-clay narrow side face and one thin orange lava crack.",
    "P_dun02": "THE SECOND POINTED SIDE PLATE: the same: a jagged pointed shard of terracotta clay, the same size and direction as the old "
               "slab, chipped notched edge, darker-clay side face, one thin orange lava crack.",
}
TA2.update({r: _PHIEN for h_ in TO["C"] for r, _ in h_})
TEN2 = {"P_tou": "the HEAD", "P_jianjiaR1": "the big SHOULDER PLATE at the LEFT of the head (the far shoulder)",
        "P_jianjiaL2": "the LONG CURVED COLLAR BAND that runs under the head",
        "P_jianjiaL1": "the big SHOULDER PLATE at the RIGHT of the head (the near shoulder)",
        "P_jianjiaR2": "the SHORT CURVED COLLAR BAND at the left of the chest opening",
        "P_dun01": "the TALL SIDE PLATE standing in front of the near arm at the right",
        "P_dun03": "the big pointed SIDE PLATE at the far right", "P_dun02": "the second pointed SIDE PLATE at the far right"}
VI2 = {"G": "đầu, vành cổ dài, vành cổ ngắn", "K": "giáp vai xa, giáp vai gần", "H": "tấm dựng trước tay gần, hai phiến bên nhọn",
       "I": "chín phiến sau lưng"}


def to_minh(chi):
    """tờ hướng dẫn = mảnh ĐANG DÙNG của mình (manh_part/, kiểu dáng con gốc) xếp vào ô đúng cỡ; ô cách nhau đủ cho lề LE2."""
    V = vung()
    O = {}
    for ma in chi:
        hang = TO2[ma]
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o, cao = {}, []
        for h_ in hang:
            cs = []
            for r, z in h_:
                g = V[r][1]
                le_r = 0.0
                if NGUON2 and os.path.exists(os.path.join(NGUON2, r + ".png")):
                    im = Image.open(os.path.join(NGUON2, r + ".png")).convert("RGBA")
                    le_r = float(json.load(open(os.path.join(NGUON2, r + ".json")))["le"])
                else:
                    im = Image.open(os.path.join(MANH, r + ".png")).convert("RGBA")
                cs.append((r, z, (im, le_r), int(round(g.width * z)), int(round(g.height * z))))
            cao.append((cs, max(c[4] for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3] for c in cs)) // (len(cs) + 1)
            if min(ke, ke_y) < 2 * LE_TO[ma] + 6:
                raise SystemExit(f"tờ {ma}: ô sát nhau quá (kẽ {ke} × {ke_y} px, cần {2 * LE_TO[ma] + 6})")
            x = ke
            for r, z, (im, le_r), cw, ch in cs:
                y0 = y + (hh - ch) // 2
                d_ = int(round(le_r * z))                # ảnh có lề: ô vẫn là khung part, hình lấn ra ngoài ô đúng phần lề
                can.alpha_composite(im.convert("RGBa").resize((cw + 2 * d_, ch + 2 * d_), Image.LANCZOS).convert("RGBA"), (x - d_, y0 - d_))
                o[r] = dict(hop=[x, y0, cw, ch], z=z, le=LE_TO[ma])
                x += cw + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"minh_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    return O


def prompt_moi(O, ta=None):
    ta = ta or TA2
    """ta = {ảnh vùng: câu tả kiểu dáng mới của mảnh đó (tiếng Anh)}; tờ nào thiếu câu tả cho một mảnh thì báo."""
    if not os.path.exists(CONCEPT2):
        raise SystemExit("chưa có concept mặt + giáp đã chọn " + Wp(CONCEPT2))
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt " + LUOT2["so"])[0].rstrip("\n")
    gd = ["", f"## Lượt {LUOT2['so']}: {LUOT2['ten']}", "",
          "Mỗi tờ: ảnh 1 = các mảnh ĐANG DÙNG (kiểu dáng cũ) xếp đúng chỗ, đúng cỡ, đúng hướng; ảnh 2 = concept mặt + giáp đã chọn. GPT vẽ kiểu dáng "
          "mới của từng mảnh vào đúng chỗ đó, vẽ đủ cả phần khuất, viền kín.", ""]
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"minh_{ma}.png")
        out, save = luu(f"N_{ma}")
        p = os.path.join(GUI, f"{LUOT2['tep']}{ma}.txt")
        n = len(o)
        R = [(mau, f"the PLACEMENT SHEET, 1536x1024, white background: {n} separate armour pieces of our puppet in their {LUOT2['cu']} design, each drawn "
                   "alone. It tells WHERE each piece goes on the sheet, HOW BIG it is and WHICH WAY it is turned. Do NOT copy the old shapes.",
              f"Tờ mảnh đang dùng (kiểu dáng cũ) của mình, 1536 × 1024, nền trắng: {VI2[ma]}; cho biết chỗ, cỡ, hướng từng mảnh"),
             (CONCEPT2, LUOT2["anh2"], LUOT2["vi2"])]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              f"TASK: draw a PARTS SHEET of {n} separate pieces of a 2D animation puppet, each piece drawn ALONE on white, in its NEW design "
              "(the design it has in image 2). Each new piece is drawn at the SAME PLACE on the sheet as the piece of image 1 that it "
              f"replaces, centred on it, about the SAME SIZE (it may stick out of the old outline by at most about {LE_TO[ma] - 12} px, and must not be much "
              "smaller), and TURNED THE SAME WAY as that old piece (the pieces of image 1 are turned almost exactly as they are in the "
              "assembled character of image 2). Draw every piece COMPLETE: in image 2 some pieces are partly hidden behind others; here draw "
              "the whole piece, also the hidden part, as ONE CLOSED SHAPE with an ink outline all the way round. Do not draw anything of the "
              "neighbouring pieces. Pure white (#FFFFFF) between the pieces, at least 40 px. Coordinates of pieces that are alone on "
              "the sheet still matter: keep them where image 1 has them.", "",
              "THE PIECES (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top; they are the box of the OLD piece):"]
        for i, r in enumerate(o, 1):
            if r not in ta:
                raise SystemExit(f"thiếu câu tả kiểu dáng mới cho {r}")
            t += [f"{i}. ({cho(o, r)}) {ta[r]}"]
        t += ["",
              f"COLOURS (each area ONE flat colour, exactly as in image 2): fired clay terracotta orange-brown ({DAT}); darker brick-brown clay "
              f"({DAT_SAM}) for side faces, rims and grooves; cooled lava rock, warm charcoal brown-black ({NHAM}); molten lava flat orange "
              f"({LAVA}); eyes and gems bright lava yellow ({LOI}).", "",
              f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown INK outline ({MUC}, about 6 px) round every piece, "
              "thinner lines for inner edges, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, no "
              "highlights, no gradients, no glow, no shadows, no shine.", "", BG]
        ghi(p, t)
        gd += [f"- **`{ma}`** ({VI2[ma]}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…). Ảnh mẫu 1 = "
               f"`{Wp(mau)}`, ảnh mẫu 2 = `{Wp(CONCEPT2)}`."]
        print(p)
    gd += ["", "Kiểm từng tờ: mỗi mảnh là kiểu dáng mới như concept, nằm đúng chỗ mảnh cũ, gần đúng cỡ, đúng hướng, viền kín, không dính mảnh "
           "khác; tô phẳng; nền trắng tinh. Claude cắt bằng `dat_nung_da.py cat_moi` (báo cỡ so với mảnh cũ, mảnh nào chạm lề)."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def cat_moi(chi=None):
    """cắt tờ N_<tờ>: mỗi mảnh lấy ô của nó nới lề LE2 → manh_part2/<ảnh vùng>.png (ảnh vùng × 2, có lề) + .json {"le": lề theo px ảnh vùng}."""
    V = vung()
    os.makedirs(MANH2, exist_ok=True)
    for ma in TO2:
        if chi and ma not in chi:
            continue
        src = moi_nhat(f"N_{ma}")
        pj = os.path.join(G.MAU, f"minh_{ma}.json")
        if not src or not os.path.exists(pj):
            print(f"tờ {ma}: chưa gen")
            continue
        A = doc(src)
        o = json.load(open(pj, encoding="utf-8"))
        Gd = np.asarray(Image.open(pj[:-5] + ".png").convert("RGB")).astype(np.int32)
        fg, fgG = ~nen(A), Gd.min(2) < 238
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        so = []
        print(f"tờ {ma} ({os.path.basename(src)}):")
        for r, d in o.items():
            x, y, cw, ch = d["hop"]
            z, LE2 = d["z"], d["le"]
            loi = cv2.erode(fgG[y:y + ch, x:x + cw].astype(np.uint8), el(12)).astype(bool)        # lõi hình cũ: cụm nào chạm thì là mảnh này
            sub = lab[y:y + ch, x:x + cw]
            ids = [i for i in np.unique(sub[loi]) if i > 0 and st[i, 4] > 200]
            if not ids:
                print(f"  {r:14s} KHÔNG THẤY mảnh trong ô")
                continue
            m = np.isin(lab, ids)
            ys_, xs_ = np.nonzero(m)                     # lề = phần hình mới lấn ra ngoài ô cũ (mặt nạ chỉ lấy cụm của mảnh nên không dính mảnh bên)
            LE2 = int(max(x - xs_.min(), xs_.max() + 1 - (x + cw), y - ys_.min(), ys_.max() + 1 - (y + ch), 4)) + 8
            x0, y0, x1, y1 = x - LE2, y - LE2, x + cw + LE2, y + ch + LE2
            D_ = 400
            mP = np.pad(m, D_)
            AP = np.pad(A, ((D_, D_), (D_, D_), (0, 0)), constant_values=255)
            fP = np.pad(fgG, D_)
            ngoai = np.zeros(1, bool)
            mm = mP[y0 + D_:y1 + D_, x0 + D_:x1 + D_]
            rgb = khu_vien(AP[y0 + D_:y1 + D_, x0 + D_:x1 + D_].astype(np.uint8), mm)
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - rgb.min(2).astype(np.float32)) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            goc = V[r][1]
            le = LE2 / z                                                                          # lề theo px ảnh vùng
            tw, th = int(round((goc.width + 2 * le) * RES)), int(round((goc.height + 2 * le) * RES))
            im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
            im2.save(os.path.join(MANH2, r + ".png"))
            json.dump({"le": le, "to": os.path.basename(src)}, open(os.path.join(MANH2, r + ".json"), "w"))
            b = fP[y0 + D_:y1 + D_, x0 + D_:x1 + D_]
            ys, xs = np.nonzero(mm)
            yb, xb = np.nonzero(b)
            ti = (xs.max() - xs.min() + 1) / (xb.max() - xb.min() + 1), (ys.max() - ys.min() + 1) / (yb.max() - yb.min() + 1)
            lech = (xs.mean() - xb.mean()) / z, (ys.mean() - yb.mean()) / z
            vis = np.full((y1 - y0, x1 - x0, 3), 255, np.uint8)
            vis[mm & b] = (170, 170, 170)
            vis[b & ~mm] = (230, 60, 60)
            vis[mm & ~b] = (60, 190, 60)
            so.append((Image.fromarray(vis), im2))
            print(f"  {r:14s} {len(ids)} cụm, lề {LE2} px, rộng × {ti[0]:.2f}, cao × {ti[1]:.2f}, tâm lệch ({lech[0]:+.0f}, {lech[1]:+.0f}) px vùng"
                  + ("   <-- CHẠM LỀ (bị cắt)" if ngoai.any() else "") + ("   <-- KHÔNG THẤY" if not ids else ""))
        to_so(so, os.path.join(MANH2, f"_so_{ma}.png"))


# ---------------------------------------------------------------- DẠNG 1 (Viêm Dũng Nhi, chibi): concept trên hình bố cục dựng từ rig (DN_NON=1)
BASE_NON = os.path.join(HERE, "inbox", "dat_nung_non")
GUI_NON = os.path.join(HERE, "gui_gpt", "dat_nung_non")
NON = {
    "theo_bo_cuc": ("bám sát bố cục, mặt nạ thú non",
                    "THE HEAD (the biggest piece, keep its size and place): a YOUNG version of the beast mask: the same blocky terracotta mask but "
                    "smoother and rounder at the corners, a small determined V brow, two BIG bright-yellow eyes with rounded corners and one tiny "
                    "white dot in each, a small snout block, and a small jaw with only TWO little square teeth (orange lava between them). The two "
                    "horns are SHORT STUBS of charcoal lava rock with small orange tips (baby horns just starting to grow), not long curved horns."),
    "tron_hon": ("tròn và ngộ hơn, đầu vò gốm tròn",
                 "THE HEAD (the biggest piece, keep its place; it may be a little rounder than in image 1): a ROUND terracotta mask-helmet like a "
                 "small clay pot, almost a ball, with a darker-clay brow band, two VERY BIG round-cornered bright-yellow eyes set low and wide "
                 "apart, slanted a little so that the look is brave and determined, one tiny white dot in each, a tiny snout bump, and a small "
                 "mouth slot with ONE little square tooth at each end (orange lava in the slot). On top two tiny rounded HORN BUDS of charcoal "
                 "lava rock with orange tips. One thin orange lava crack on one cheek."),
}


def prompt_non():
    os.makedirs(GUI_NON, exist_ok=True)
    os.makedirs(os.path.join(BASE_NON, "tai_ve"), exist_ok=True)
    bo = os.path.join(BASE_NON, "mau", "bo_cuc_non.png")
    lon = os.path.join(G.TAI, "L3_duyet.png")
    if not os.path.exists(bo):
        raise SystemExit("chưa có hình bố cục: DN_NON=1 py -3 -I dat_nung_rig.py bo_cuc")
    R = [(bo, "the LAYOUT of the child form, 1536x1024, white background, built by the animation rig from the ADULT pieces: a small floating "
              "armour golem (no legs) with a very big head in the middle, small shoulder plates left and right of it, a round orange lava disc "
              "with a small yellow core under the head, a far open hand at the lower left, a near arm of stacked slabs with two round pegs "
              "across the bottom ending in a big fist that holds a short sword upright at the left, and a few small dark shards behind. It "
              "tells WHERE every piece is and HOW BIG it is. Its pieces still have the ADULT design: do not copy that design.",
          "Hình bố cục dạng 1 do rig dựng (1536 × 1024, nền trắng): golem giáp nhỏ lơ lửng, đầu rất to ở giữa, giáp vai nhỏ hai bên, quầng dung nham "
          "cam + viên lõi vàng dưới đầu, bàn tay xa mở ở dưới trái, tay gần vắt ngang nắm kiếm ngắn dựng bên trái, vài mảnh đá than nhỏ phía sau. "
          "Các mảnh còn mang kiểu dáng dạng lớn"),
         (lon, "the ADULT form of the same character (approved), 1536x1024, white background: a fierce terracotta beast-mask golem with spiked "
               "broken-clay shoulder plates, a spiked collar, jagged charcoal shards behind and a huge lava-rock sword. Take from it the "
               "materials, the colours and the hand-drawn look (wobbly dark-brown ink line, crayon hatching, flat colours). The child must "
               "clearly be the YOUNG form of this character.",
          "Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): lấy chất liệu, màu, nét vẽ tay; dạng 1 phải ra là con non của nó")]
    hd = ["# Viêm Dũng Nhi (dạng 1 của tướng thứ 8 đảo Hỏa, mã dat_nung_non)", "",
          "Người dùng 2026-11-14: \"cho vào game đi rồi làm dạng 1 của tướng này\". Dạng 1 dùng CÙNG bộ xương, cùng clip với dạng lớn; hình bố cục do rig "
          "dựng (đầu phóng 1,5; giáp, phiến, kiếm thu nhỏ; bớt bốn phiến lưng), concept vẽ trên bố cục đó để lắp lại được.", "",
          "## Lượt 1: concept (hai phương án)", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, dau) in NON.items():
        out = os.path.join(BASE_NON, "tai_ve", f"L1_{k}.png")
        p = os.path.join(GUI_NON, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or delete "
              "any other file.", "",
              "TASK: draw the CHILD FORM (first evolution stage) of the character of image 2, as ONE picture, on the LAYOUT of image 1: every "
              "piece stays where image 1 has it and at about the size image 1 gives it (the same pose, the same overlaps, separate floating "
              "pieces with white gaps where image 1 has gaps), but every piece is REDESIGNED as a young, small, cute version. A chibi little "
              "clay warrior: big head, small armour, a short sword; brave and ready to fight, cute, not scary, not a happy mascot.", "",
              dau,
              "THE TWO SHOULDER PLATES (small, left and right of the head): small ROUNDED lumps of terracotta clay with only two or three small "
              "chips on the lower edge, one thin orange crack each, and one SHORT blunt charcoal spike nub on top (a small cone, a quarter of "
              "the adult spike).",
              "THE COLLAR BANDS (the curved bands round the lava disc): plain smooth clay bands with two or three tiny round charcoal studs "
              "instead of long teeth.",
              "THE LAVA DISC AND THE CORE: keep them as in image 1: a flat orange disc with a few darker crust patches and a round "
              "bright-yellow core with one orange ring; the core is clearly visible.",
              "THE SWORD (short, at the left, tip up, held by the fist): a SHORT, WIDE, stubby blade of charcoal lava rock like a training "
              "sword, with one simple orange-and-yellow zigzag lava line down the middle, a small terracotta guard, a charcoal grip and a round "
              "pommel. The same place, length and direction as in image 1.",
              "THE NEAR ARM AND THE FIST (across the bottom), THE FAR OPEN HAND (lower left): the same pieces as image 1 in the same places: "
              "terracotta slabs with two round charcoal pegs, a chunky clay fist with round charcoal knuckle studs, charcoal finger blocks; "
              "simplify the engraved marks to one or two grooves, rounder corners.",
              "THE SMALL SHARDS BEHIND (charcoal, peeking out behind the shoulders) AND THE SMALL SIDE PLATES (clay, at the right): small "
              "stubby chips, the same places as in image 1, each with one short orange crack; few and small.", "",
              f"COLOURS (each area ONE flat colour): fired clay terracotta orange-brown ({DAT}), a little lighter and fresher than the adult; "
              f"darker brick-brown clay ({DAT_SAM}) for side faces and grooves; cooled lava rock, warm charcoal brown-black ({NHAM}); molten "
              f"lava flat orange ({LAVA}); eyes and core bright lava yellow ({LOI}).", "",
              f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown INK outline ({MUC}, about 6 px) round every piece, "
              "thinner lines for inner edges, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, no "
              "highlights (except the one tiny dot in each eye), no gradients, no glow, no shadows, no shine. Chunky, simple, few details.", "",
              "CANVAS: landscape 1536x1024, pure-white background, no ground line, no cast shadow; the character at the same place and size as "
              "in image 1. No dust, sparks, embers, smoke, flames or glow.", BG]
        ghi(p, t)
        hd += [f"- **`{k}`** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Kiểm: mọi mảnh nằm đúng chỗ, gần đúng cỡ như hình bố cục (đầu to ở giữa, kiếm ngắn bên trái, tay gần vắt ngang dưới); ra là con non "
           "của dạng lớn (cùng chất liệu, màu), mặt dễ thương mà vẫn có vẻ chiến; lõi vàng lộ rõ; tô phẳng, không bóng, không phát sáng; nền trắng tinh.",
           "Câu sửa nhanh: \"the head is too small: make it as big as in image 1\"; \"this is still the adult design: make it younger and "
           "rounder, shorter horns, smaller spikes\"; \"remove the shading / glow, flat colour only\".",
           "Bản được chọn chép thành `L1_duyet.png` cùng thư mục."]
    ghi(os.path.join(GUI_NON, "HUONG_DAN.md"), hd)


TO_NON = {"G": TO2["G"], "K": TO2["K"], "W": [[("P_wuqi", 0.9)]]}       # dạng 1 vẽ riêng: đầu + hai vành cổ, hai giáp vai, kiếm (mảnh khác dùng của dạng 2)
VI2["W"] = "thanh kiếm"
# câu tả từng mảnh theo concept dạng 1 đã chọn (A · mặt nạ thú non, inbox/dat_nung_non/tai_ve/L1_duyet.png)
TA_NON = {
    "P_tou": "THE HEAD of the child, at the same place and about the same size as the adult head of image 1 (as wide with its horns, as "
             "tall): a blocky terracotta MASK with ROUNDED corners, seen from the front, turned a little to the lower left. A darker-clay "
             "V-shaped brow band across the top; two BIG ROUND bright-yellow eyes with a thick ink outline and one small white dot in each, "
             "the brow cutting a little into their tops so the look is brave; a small square snout block between the eyes; a jaw band "
             "with only TWO little square bright-yellow teeth. On top, at each side, a round clay boss with ONE SHORT THICK HORN STUB of "
             "charcoal lava rock, curved inwards, with a jagged orange tip (baby horns). Side faces darker clay. Cute and determined.",
    "P_jianjiaL2": "THE LONG CURVED COLLAR BAND of the child: the same curve, length and width as the adult band of image 1 but PLAIN and "
                   "smooth: terracotta clay with a darker-clay side face, one thin orange lava crack along it, and ONE round charcoal stud "
                   "at each end. NO teeth, no spikes, no big tooth at the end.",
    "P_jianjiaR2": "THE SHORT CURVED COLLAR BAND of the child: the same curve and size as the adult one but plain and smooth: terracotta "
                   "clay with a darker-clay side face and one round charcoal stud at its lower end; the block across its top becomes a "
                   "small ROUNDED clay lump. NO teeth, no spikes.",
    "P_jianjiaR1": "THE FAR SHOULDER PLATE of the child: a small ROUNDED lump of terracotta clay, about as wide as the slab of the adult "
                   "plate of image 1, with only three or four small chips along its lower edge, a darker-clay side face along that edge, a "
                   "small network of thin orange lava cracks, and ONE SHORT blunt cone spike of charcoal lava rock on top (about 45 px "
                   "tall, much shorter than the adult spike).",
    "P_jianjiaL1": "THE NEAR SHOULDER PLATE of the child: the same design as the other one: a small rounded lump of terracotta clay about as "
                   "wide as the slab of the adult plate, three or four small chips along its lower edge with a darker-clay side face, thin "
                   "orange lava cracks, and ONE SHORT blunt charcoal cone spike on top (about 45 px tall).",
    "P_wuqi": "THE SWORD of the child (tip at the top, exactly as LONG as the adult sword of image 1 and in the same place, but about TWICE AS "
              "WIDE, so that it reads as a short stubby training sword): a wide blade of charcoal lava rock with a blunt pointed tip and "
              "slightly lighter bevelled edges, ONE bold zigzag line of molten lava down its middle (flat orange with a bright-yellow "
              "centre); a simple terracotta bar guard, wider than the blade; a short charcoal grip and a round terracotta pommel. No chain "
              "runes, no long narrow blade.",
}


def sang_non():
    """trỏ lượt mảnh (to_minh, prompt_moi, cat_moi) sang dạng 1: tờ hướng dẫn = mảnh dạng 2, concept = L1_duyet của dạng 1."""
    global GUI, MANH2, CONCEPT2, NGUON2, TO2, TA2, LUOT2
    NGUON2 = MANH2
    G.MAU, G.TAI = os.path.join(BASE_NON, "mau"), os.path.join(BASE_NON, "tai_ve")
    GUI, MANH2 = GUI_NON, os.path.join(BASE_NON, "manh_part2")
    CONCEPT2 = os.path.join(BASE_NON, "tai_ve", "L1_duyet.png")
    TO2, TA2 = TO_NON, TA_NON
    LUOT2 = dict(so="2", tep="luot_2_manh_", ten="mảnh vẽ riêng của dạng 1 (đầu, vành cổ, giáp vai) theo concept đã chọn", cu="ADULT",
                 anh2="the APPROVED picture of the CHILD FORM of our character, 1536x1024, white background: a small floating terracotta golem "
                      "with a very big head, small shoulder plates, a lava heart with a yellow core and a short sword at the left. Take from "
                      "it the CHILD DESIGN of each piece (its shape, details, colours) and the hand-drawn look.",
                 vi2="Concept dạng 1 đã chọn (1536 × 1024, nền trắng): lấy kiểu dáng non, màu, nét của từng mảnh")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "non":
        prompt_non()
        sys.exit()
    if c.startswith("non_"):                              # non_to_minh, non_cat_moi: như to_minh, cat_moi nhưng cho dạng 1
        sang_non()
        c = c[4:]
    if c == "ca_con":
        ca_con()
        prompt_concept()
    elif c == "to":
        prompt_da(to_goc())
    elif c == "mat_giap":
        prompt_mat_giap()
    elif c == "to_minh":
        prompt_moi(to_minh(sys.argv[2:] or list(TO2)))
    elif c == "cat_moi":
        cat_moi(sys.argv[2:] or None)
    elif c == "cat":
        cat(sys.argv[2:] or None)
    else:
        print(__doc__)
