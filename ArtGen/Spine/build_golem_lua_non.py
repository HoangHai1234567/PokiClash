# -*- coding: utf-8 -*-
"""Gói GPT vẽ concept DẠNG 1 của golem lõi lửa ("Nham Con", mã làm việc golem_lua_non; dạng non của golem_lua_1 đã duyệt, suất
`nham_than` đảo Hỏa). Cùng rig, cùng clip với dạng 2.

Người dùng (2026-11-13): "làm dạng 1 và vfx riêng đi". Ba hướng là ĐỀ XUẤT của Claude, chờ người dùng chọn. Ảnh mẫu: hình bố cục
(mảnh dạng 2 xếp lại ở tỉ lệ dạng non, golem_lua_non.py bo_cuc), concept dạng 2 đã duyệt, Voọc Tướng, bản đồ.

    py -3 -I ArtGen/Spine/golem_lua_non.py bo_cuc
    py -3 -I ArtGen/Spine/build_golem_lua_non.py
    py -3 -I ArtGen/Spine/chay_hoa.py ArtGen/Spine/gui_gpt/golem_lua_non/luot_1_concept_<hướng>.txt ...
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_golem_lua import SOFT, LINE, FLAT, BG, KIEM_SI, WORLD_STYLE, Wp, ghi  # noqa: E402

CODE = "golem_lua_non"
PK = os.path.join(HERE, "gui_gpt", CODE)
TAI = os.path.join(HERE, "inbox", CODE, "tai_ve")
MAU = os.path.join(HERE, "inbox", CODE, "mau")
DUYET2 = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")

CHUNG = (
    "YOUNG FIRST FORM: this is the FIRST, young evolution stage of the creature in image 2 (image 2 is its approved grown-up final "
    "form). The SAME species and the SAME build: a hunched living STONE GOLEM made of thick separate stone blocks, standing on two "
    "short stubby legs, FACING THE VIEWER'S RIGHT; a huge rounded back; a small skull-like stone face with ONE round eye, low at the "
    "front right under a brow plate; a round FIRE CORE showing in the opening of the C-shaped chest shell; two long heavy arms ending "
    "in big rounded stone hands on the ground; flames coming out of round holes with dark collars. But it is YOUNG: its fire has only "
    "just been lit, so it is smaller-flamed, blunter and less armed than image 2. It is still a determined little fighter ready for "
    "battle (the brow comes down just above the eye): NOT a smiling mascot, NOT a baby toy, NOT horror, NOT a robot.\n"
    "- LAYOUT: follow image 1 exactly for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps which (image 1 is "
    "the final form's own art re-arranged in the young form's proportions). Same framing: the figure stands in the middle of the "
    "1536x1024 canvas, from about x = {x0} to x = {x1}, and from about y = {y0} (top of the tallest flame) to y = {y1} (bottom of the "
    "feet and claws). Do NOT enlarge, shrink or move the figure.\n"
    "- KEEP THE SAME PIECES (very important: the picture will be cut into the same pieces and animated with the same skeleton as "
    "image 2; the stone pieces fly apart and come back together): the big back slab; the smaller top plate with its small hole; the "
    "round near-shoulder plate with its thick ring; the angular brow plate and the long blade-shaped cheek plate behind it; the "
    "skull-like face with its one eye and the small socket ring on the forehead; the separate lower jaw block; the C-shaped chest "
    "shell around the fire core; the chest block left of it; the hip blocks; the two dark wrist blocks; the two big hands, each with "
    "THREE separate claws; the two legs (thigh block, round glowing knee ball, small square foot). Every piece one clear closed shape "
    "with its own complete ink outline; pieces touch or overlap but are NOT melted into one blob.\n"
    "- SAME MATERIALS AND COLOURS as image 2, each area one flat colour: stone plates, face, hands, legs warm pale ash-grey volcanic "
    "stone (#B2A79A), at most ONE carved groove line per plate (#928678); rings, hole collars, wrist blocks, jaw dark charcoal "
    "(#3F3B46); claws charcoal black (#2E2A30); fire red-orange (#E0441F) / orange (#F7902A) / yellow (#FFD45A); outlines dark-brown "
    "ink (#2B2118). Only these colours.\n"
    "- CLAWS: short, thick, BLUNT claw nubs (about half as long as in image 2), like a cub's; still three per hand, touching the "
    "ground.\n"
    "- THE EYE: one round yellow eye (#FFD45A) with a dark pupil looking right and one tiny pale dot, a little bigger than in image 2, "
    "in a charcoal-rimmed socket; determined, slightly frowning.\n"
    "- VERY SIMPLE, FEW DETAILS: big clean chunky shapes; NO cracks, NO lava cracks, NO runes, NO rivets, NO moss, NO extra spikes, "
    "NO horns, NO extra flames, NO smoke.\n")

FLAME_STYLE = ("Every flame is drawn like a real small hand-drawn fire: a rounded base coming out of the hole, a short body bending in a "
               "soft S-curve, ONE pointed tip curling a little up and back (toward the viewer's left), at most one small side lick; "
               "three nested flat colour zones (red-orange outside, orange, yellow inside near the base). Not a spike, horn, crystal "
               "or leaf.")

HUONG = {
    "moi_lua": dict(
        ten="A · mồi lửa: giữ khối dáng dạng 2; chỉ ba ngọn lửa nhỏ (vai, đỉnh lưng, trán), các lỗ còn lại tắt; vuốt cụt",
        thay=("- DESIGN A, PILOT FLAMES: only THREE flames are lit, and they are SMALL (about half the size of image 2): (1) out of "
              "the ring on the near shoulder, base about {vai_g}, the flame stays within about {vai_h}; (2) out of the ring on top of "
              "the back, base about {dinh_g}, within about {dinh_h}; (3) out of the socket on the forehead, base about {tran_g}, "
              "shooting forward to the right and a little up, within about {tran_h}. " + FLAME_STYLE + "\n"
              "- EVERY OTHER HOLE IS COLD (the small hole on the top plate, the hole on the back of the head, the hole on top of the "
              "near wrist block, the hole on the hip block between the legs): just an empty dark round hole with its charcoal collar, "
              "its inside dark charcoal-brown (#4A4038); NO flame there, NO smoke, NO glow.\n"
              "- THE FIRE CORE: the same round ball in the chest opening, but calmer: mostly orange (#F7902A) with a red-orange outer "
              "zone and only a SMALL yellow heart; wavy flat zones, no glow. The two knee balls stay glowing orange with a yellow "
              "centre. The stone blocks keep the chunky bevelled shapes of image 2."),
        check=["**Ba ngọn lửa nhỏ** (vai gần, đỉnh lưng, trán); bốn lỗ còn lại **tắt** (lỗ tối có vành than, không lửa, không khói).",
               "Khối đá giữ dáng vát cạnh như dạng 2; lõi lửa dịu hơn (tim vàng nhỏ)."]),
    "cuoi_tron": dict(
        ten="B · cuội tròn: thú non chibi; đầu và mắt to hơn, khối đá tròn như đá cuội, tay nhỏ hơn; ba ngọn lửa nhỏ, các lỗ còn lại tắt",
        thay=("- DESIGN B, ROUND PEBBLE CUB: a rounder, cub-like body. As image 1 shows, the HEAD (face, brow, jaw) is clearly BIGGER "
              "in proportion than in image 2 and the eye is bigger; the hands are smaller; the near-shoulder plate a little smaller. "
              "Every stone block is ROUNDER, like big smooth river pebbles and cobbles: soft rounded corners instead of sharp bevels; "
              "the brow plate is a shorter, rounder slab (still coming down just above the eye); the cheek plate is a short rounded "
              "leaf shape. Still the same pieces, each with its own outline.\n"
              "- only THREE flames are lit, and they are SMALL (about half the size of image 2): (1) out of the ring on the near "
              "shoulder, base about {vai_g}, within about {vai_h}; (2) out of the ring on top of the back, base about {dinh_g}, within "
              "about {dinh_h}; (3) out of the socket on the forehead, base about {tran_g}, forward to the right and a little up, "
              "within about {tran_h}. " + FLAME_STYLE + "\n"
              "- EVERY OTHER HOLE IS COLD (top plate, back of the head, near wrist block, hip block): an empty dark round hole with "
              "its charcoal collar, inside dark charcoal-brown (#4A4038); NO flame, NO smoke.\n"
              "- THE FIRE CORE: mostly orange (#F7902A) with a red-orange outer zone and a SMALL yellow heart; the two knee balls "
              "glowing orange with a yellow centre."),
        check=["**Chibi**: đầu, mắt to hơn dạng 2, tay nhỏ hơn; khối đá **tròn như đá cuội** (góc bo, không vát sắc).",
               "**Ba ngọn lửa nhỏ**, bốn lỗ còn lại tắt. Vẫn mặt quả quyết, không cười."]),
    "du_lua": dict(
        ten="C · đủ lửa nhỏ: giữ khối dáng dạng 2 và đủ bảy ngọn lửa, mọi ngọn chỉ bằng nửa; vuốt cụt",
        thay=("- DESIGN C, ALL HOLES LIT, SMALL: all SEVEN flames of image 2 are lit, but every one is SMALL (about half the size of "
              "image 2), exactly as placed in image 1: near shoulder ring (base about {vai_g}, within about {vai_h}); ring on top of "
              "the back (base about {dinh_g}, within about {dinh_h}); forehead socket (base about {tran_g}, forward to the right, "
              "within about {tran_h}); and four tiny flames: on the top plate (within about {dn_h}), on the back of the head (within "
              "about {sd_h}), on top of the near wrist block (within about {ct_h}), on the hip block between the legs (within about "
              "{hg_h}). " + FLAME_STYLE + "\n"
              "- THE FIRE CORE: the same round ball, a little calmer than image 2: orange with a red-orange outer zone and a yellow "
              "heart. The two knee balls glowing orange with a yellow centre. The stone blocks keep the chunky bevelled shapes of "
              "image 2."),
        check=["**Đủ bảy ngọn lửa**, ngọn nào cũng chỉ bằng nửa dạng 2; khối đá giữ dáng dạng 2."]),
}

CHECK_CHUNG = [
    "Bố cục y hình bố cục: golem gù nhìn sang **phải**, mặt đầu lâu nhỏ một mắt thấp phía trước dưới tấm mày, lõi lửa lộ ở khe ngực chữ C.",
    "**Đủ các mảnh như dạng 2** (lưng, tấm đỉnh, vai + vòng, mày + má, mặt, hàm, vỏ ngực, khối ngực, hông, hai cổ tay, hai bàn tay ba vuốt, "
    "hai chân có gối dung nham), mỗi mảnh viền kín riêng.",
    "**Vuốt cụt, tù**; mắt hơi to hơn dạng 2; cùng màu đá tro, mảng phụ than chì.",
    "Ít chi tiết: không vết nứt, hoa văn, gai, sừng, lửa thừa, khói. Tô phẳng, **không quầng sáng**, nền trắng.",
]
FIX = [
    ("Lửa to như dạng 2", "The flames must be SMALL, about half the size of image 2, staying inside the boxes given."),
    ("Lỗ tắt vẫn có lửa / khói (hướng A, B)", "The cold holes are empty dark holes with a charcoal collar: remove the flame and any smoke there."),
    ("Thiếu mảnh / gộp mảnh", "Keep every piece of image 2 as a separate closed shape with its own ink outline, placed as in image 1."),
    ("Quá dễ thương / cười", "Determined little fighter: the brow comes down just above the eye, no smile, no blush."),
    ("Thêm vết nứt / gai / sừng", "Remove all cracks, spikes, horns and ornaments: each stone plate one flat colour with at most one groove line."),
    ("Có quầng sáng / bóng", "Flat colours only: no glow, no halo, no shading, no cast shadow, no highlights."),
]


def hopxy(b):
    return f"x = {b[0]} to x = {b[2]}, y = {b[1]} to y = {b[3]}"


def main():
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    B = json.load(open(os.path.join(MAU, "bo_cuc.json"), encoding="utf-8"))
    gd = [f"# Gói gửi GPT: `{CODE}` (dạng 1 \"Nham Con\" của golem lõi lửa, suất `nham_than` đảo Hỏa)", "",
          "Làm 2026-11-13 theo lời người dùng \"làm dạng 1\". Cùng rig, cùng clip với dạng 2 đã duyệt (`golem_lua_1`). Ba hướng là đề xuất "
          "của Claude, chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/golem_lua_ghichu.md` mục 7.", "",
          "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in HUONG.items():
        b = B[kieu]
        L = b["lua"]
        R = [(os.path.join(MAU, f"bo_cuc_{kieu}.png"),
              "LAYOUT GUIDE, 1536x1024, white background: the final form's own art re-arranged in the proportions of the YOUNG first "
              "form (short flames, smaller hands with short claws" + (", bigger head and eye" if kieu == "cuoi_tron" else "") +
              (", cold dark holes where a flame is not lit" if kieu != "du_lua" else "") +
              "). Use it for where every piece is, how big it is and which piece overlaps which; redraw everything cleanly.",
              "Hình bố cục dạng non (1536 × 1024, nền trắng): mảnh dạng 2 xếp lại, lửa ngắn, tay nhỏ vuốt cụt" +
              (", đầu và mắt to hơn" if kieu == "cuoi_tron" else "") + (", lỗ tắt là lỗ tối" if kieu != "du_lua" else "") +
              ". Lấy chỗ đặt, cỡ, thứ tự chồng"),
             (DUYET2,
              "the APPROVED FINAL FORM of this creature, 1536x1024, white background: the design this young form grows into, and the "
              "exact line, colours and colouring style to keep.",
              "Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): golem đá tro lõi lửa, bảy ngọn lửa, vuốt đen to. Thiết kế gốc, nét và cách tô"),
             (KIEM_SI,
              "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match its wobbly "
              "dark-brown pen line, visible crayon hatching and completely flat colouring. Do NOT copy its design or colours.",
              "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): lấy nét bút rung, vân sáp, tô phẳng"),
             (WORLD_STYLE,
              "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
              "wax crayon hatching), nothing of its content.",
              "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp")]
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(TAI, f"L1_{kieu}.png")
        p = os.path.join(PK, f"luot_1_concept_{kieu}.txt")
        kw = dict(vai_g=tuple(L["lua_vai"]["goc"]), vai_h=hopxy(L["lua_vai"]["hop"]), dinh_g=tuple(L["lua_dinh"]["goc"]),
                  dinh_h=hopxy(L["lua_dinh"]["hop"]), tran_g=tuple(L["lua_tran"]["goc"]), tran_h=hopxy(L["lua_tran"]["hop"]))
        if kieu == "du_lua":
            kw.update(dn_h=hopxy(L["lua_dinh_nho"]["hop"]), sd_h=hopxy(L["lua_sau_dau"]["hop"]), ct_h=hopxy(L["lua_co_tay"]["hop"]),
                      hg_h=hopxy(L["lua_hong"]["hop"]))
        x0, y0, x1, y1 = b["khung"]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw the YOUNG FIRST FORM of the creature of image 2 as ONE picture, in a clean animation-ready resting pose, in "
              "the hand-drawn style of image 2.", "",
              CHUNG.format(x0=x0, x1=x1, y0=y0, y1=y1) + d["thay"].format(**kw), "",
              "Coordinates are pixels on the 1536x1024 canvas (x from the left, y from the top). NEAR = the side toward the viewer "
              "(the viewer's left); FAR = the other side.", "",
              "ANIMATION-READY: calm resting pose exactly as in image 1; no sparks, no embers, no smoke, no glow, no speed lines, no "
              "ground line, no cast shadow, no props, no second character.", "", SOFT, LINE, FLAT, BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", "Kiểm riêng hướng này:", ""] + [f"- {c}" for c in d["check"]] + [""]
    gd += ["## Kiểm chung", ""] + [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(PK, "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2 (người dùng chọn A "mồi lửa", 2026-11-13): MỘT tờ mảnh riêng của
# dạng 1. Các tấm đá dùng lại mảnh dạng 2 (cùng thiết kế); chỉ vẽ mới thứ khác dạng 2: ba ngọn lửa nhỏ (gốc hẹp vừa miệng lỗ), sáu vuốt cụt,
# lõi lửa dịu. Lửa đặt ĐÚNG CHỖ trên khung concept (gốc ở tâm lỗ); vuốt xếp một hàng phía dưới, lõi ở góc dưới phải (golem_lua_non.py manh
# tự đặt lại vào chỗ).
LUA_NON = [  # (tên, gốc dưới (x, y), bề rộng gốc, ngọn (x, y), bề rộng lớn nhất, mô tả)
    ("lua_vai", (522, 410), 64, (432, 268), 120, "the SHOULDER flame: it leans up and to the LEFT"),
    ("lua_dinh", (695, 276), 50, (700, 140), 88, "the BACK-TOP flame: it rises straight up"),
    ("lua_tran", (1055, 468), 30, (1160, 372), 70, "the FOREHEAD flame: it shoots to the RIGHT and a little up"),
]
VUOT_NON = ["vuot_gan1", "vuot_gan2", "vuot_gan3", "vuot_xa2", "vuot_xa3", "vuot_xa1"]   # trái → phải trên concept
VUOT_X0, VUOT_DX, VUOT_Y = 150, 150, 860
LOI_TAM, LOI_DK = (1310, 800), 250


def build_manh():
    duyet = os.path.join(TAI, "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt: " + Wp(duyet))
    out = os.path.join(TAI, "M_1.png")
    p = os.path.join(PK, "luot_2_manh_1.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: a hunched ash-grey stone golem "
         "facing right, with three small flames coming out of dark rings (near shoulder, top of the back, forehead), a round fire core "
         "in its chest, two big stone hands each with three short blunt dark claws.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as M_1_2.png, M_1_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: on a pure-white 1536x1024 canvas draw ONLY the ten separate pieces listed below, taken from image 1, each COMPLETE "
         "(also the part that is hidden in image 1), in exactly the same hand-drawn style, colours and size as in image 1: dark-brown "
         "wobbly ink outline (#2B2118) about 5 px thick all the way around every piece, flat colours with visible crayon hatching. The "
         "pieces must NOT touch each other. Nothing else on the canvas: no stone plates, no rings, no hands, no body.", "",
         "A. THREE SMALL FLAMES (the three flames of image 1, same size and shape as there: red-orange #E0441F outside, orange #F7902A, "
         "yellow #FFD45A inside near the base; one pointed tip curling a little up and back, at most one small side lick). Each flame "
         "comes OUT OF A ROUND HOLE: its ROOT must be NARROW (the width given), with a rounded bottom end closed by the ink outline, "
         "and the flame WIDENS gradually above the root. Each flame is ONE closed shape; no separate floating flame bits."]
    for i, (ten, (gx, gy), w, (tx, ty), ww, mo) in enumerate(LUA_NON, 1):
        t.append(f"  {i}. {mo}: root bottom centred at x = {gx}, y = {gy}, root {w} px wide; its tip at about x = {tx}, y = {ty}; at "
                 f"most {ww} px wide.")
    t += ["",
          "B. SIX CLAWS in one row along the bottom (the six short blunt charcoal-black claws #2E2A30 of image 1, same size and the "
          "same slant as in image 1). Each claw is drawn COMPLETE as one closed shape: its blunt tip at the bottom AND its rounded "
          "upper end (the part hidden inside the hand in image 1, about one third of its length more). From left to right: the three "
          "claws of the NEAR hand (left, middle, right claw), then the three claws of the FAR hand (left, middle, right claw). Centre "
          f"them at x = {', '.join(str(VUOT_X0 + i * VUOT_DX) for i in range(6))}, all at about y = {VUOT_Y} (each claw stays within "
          "60 px of its centre).", "",
          f"C. THE FIRE CORE: the round ball of fire from the chest of image 1, drawn as ONE WHOLE circle (in image 1 most of it is "
          f"hidden behind the stone shell and the jaw): centre at x = {LOI_TAM[0]}, y = {LOI_TAM[1]}, diameter {LOI_DK} px. A calm young "
          "fire: a red-orange (#E0441F) outer zone, a wide orange (#F7902A) zone, and only a SMALL yellow (#FFD45A) heart in the "
          "middle (about one quarter of the diameter); the borders between the zones wavy like flame tongues; ink outline around the "
          "circle. No eye, no face, no glow.", "",
          "Exactly 10 separate pieces on the canvas (3 flames, 6 claws, 1 ball), nothing else.", "", FLAT, BG]
    ghi(p, t)
    gd = ["", "## Lượt 2: tờ mảnh riêng của dạng 1 (sau khi người dùng chọn hướng A, 2026-11-13)", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(duyet)}` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng): golem đá tro, ba ngọn lửa nhỏ, bốn lỗ tắt, vuốt cụt |", "",
          "Kiểm: đúng 10 mảnh rời nhau trên nền trắng: 3 ngọn lửa (gốc HẸP có viền kín, đặt đúng chỗ như concept), 6 vuốt cụt xếp một hàng "
          "phía dưới (đủ cả đầu trên bị bàn tay che), 1 lõi lửa tròn đủ (tim vàng nhỏ) ở góc dưới phải. Không có tấm đá, vòng, bàn tay.", "",
          "| Sai | Gửi thêm |", "|---|---|",
          "| Lửa gốc to / không khép viền | `Each flame's root must be narrow as given and closed with the ink outline.` |",
          "| Thiếu vuốt / vuốt dính nhau | `Exactly six separate claws in one row, not touching.` |",
          "| Lõi có mặt / quầng sáng | `The core is a plain ball of fire: no face, no glow.` |"]
    hd = os.path.join(PK, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read()
    moc = "\n## Lượt 2: tờ mảnh riêng"
    if moc in cu:
        cu = cu[:cu.index(moc)].rstrip("\n") + "\n"
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n".join(gd) + "\n")
    print(p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manh":
        build_manh()
    else:
        main()
