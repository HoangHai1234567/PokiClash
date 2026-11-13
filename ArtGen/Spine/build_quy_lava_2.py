# -*- coding: utf-8 -*-
"""Gói GPT vẽ DẠNG 2 của tiểu quỷ lava (quy_lava_2). Người dùng 2026-11-13: "ok ổn rồi, làm dạng 2 đi con này là dạng 1"; con gốc dạng 2:
"tự nghĩ thôi, lên concept rồi gen"; chiêu: "giữ kiểu dạng 1, mạnh hơn".

Cách làm (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc"): dùng lại rig monster_3336 và clip đã duyệt của dạng 1; concept dạng 2 vẽ CÙNG
TƯ THẾ, CÙNG BỐ CỤC với concept dạng 1 (mỗi bộ phận gần như cùng chỗ) để mảnh lắp đúng xương; khác hẳn ở dáng nhận diện (thân cao hơn, giáp, sừng,
bờm lửa, giáo, khiên, mặt bớt chibi), màu đậm hơn (tiêu chí 0a của skill). Hai hướng là ĐỀ XUẤT của Claude, chờ người dùng chọn.

    py -3 -I ArtGen/Spine/build_quy_lava_2.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_lava_2/luot_1_concept_<hướng>.txt
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_quy_lava as B1  # noqa: E402

PK = os.path.join(HERE, "gui_gpt", "quy_lava_2")
TAI = os.path.join(HERE, "inbox", "quy_lava_2", "tai_ve")
DANG1 = os.path.join(HERE, "inbox", "quy_lava_1", "tai_ve", "L1_duyet.png")

LAYOUT = (
    "SAME POSE, SAME LAYOUT AS IMAGE 1 (very important: the new picture will be cut into pieces and fitted onto the SAME animation skeleton as "
    "image 1). Draw the evolved creature in exactly the pose of image 1, facing the viewer's right in the same light three-quarter view with BOTH "
    "eyes visible, and keep every part at the SAME PLACE on the 1536x1024 canvas, about the same size or a little bigger, never moved: the round "
    "head-body in the middle (about x = 595 to x = 990; its TOP may rise to about y = 330 because the body is now taller, its bottom stays at "
    "about y = 800); the near eye at about x = 750 to x = 845, y = 490 to y = 570 and the far eye at about x = 920 to x = 970, y = 485 to y = 560; "
    "the mouth at about x = 815 to x = 945, y = 575 to y = 620; the near horn rising from about (745, 430) and the far horn from about (950, 440); "
    "the fire on the head rising behind the horns from the top of the head; the big near gauntlet at about x = 500 to x = 750, y = 545 to "
    "y = 800 with its shoulder piece on top at about x = 585 to x = 715, y = 540 to y = 630 and its knuckles at the bottom; the two-part "
    "spear-blade diagonal across the front, its back slab at the upper left (back end at about x = 355, y = 470) passing behind the gauntlet and "
    "its crystal spike in front of the belly ending at about x = 1000, y = 915; the far fist at about x = 980 to x = 1060, y = 530 to y = 700 "
    "BEHIND the tall shield at about x = 995 to x = 1192, y = 420 to y = 882 (only the shield is seen there, no fingers); the stone feet at the "
    "bottom at about y = 800 to y = 870.")

COMMON = (
    "WHAT MAKES IT THE EVOLVED FORM (it must read at a glance as the SAME creature grown up and much stronger, but clearly a different, cooler "
    "silhouette): no longer a baby: the head-body is taller (an upright egg instead of a ball), the eyes are smaller, narrower and fiercer "
    "(still solid yellow half-moons without pupils, with a sharper slant), the zigzag mouth shows FOUR fangs, two bigger; tougher, battle-worn, "
    "proud and menacing, still appealing, not horror.")

D = {
    "hiep_si": dict(
        ten="hiệp sĩ dung nham: thân đỏ bazan đậm, giáp ngực đá có lõi dung nham, sừng cong ra trước, bờm lửa lớn, giáo có ngạnh, khiên mặt quỷ",
        body=(
            "DESIGN: a LAVA KNIGHT.\n"
            "- Head-body: deep basalt red (#5E2A24) with a few thin glowing orange-yellow lava cracks (#FFA034); a dark stone CHEST PLATE (#2E2020) "
            "covers the lower front like a cuirass, with a round glowing MAGMA CORE (#FFB43C ring around a #FFE07A centre) set in its middle; the "
            "lighter belly patch is gone under the plate.\n"
            "- Horns: two much BIGGER horns of black volcanic glass (#2A1E1E) with orange cracks, curving FORWARD like a bull's, the far one sweeping "
            "out to the right; a short third spike on the brow between them.\n"
            "- Fire on the head: a bigger, wilder mane of flame with SIX or SEVEN tongues (red-orange outside, orange, a large yellow core), rising "
            "higher (its top at about y = 20) and streaming back to the left, two small separate flame drops; same hand-drawn campfire style as "
            "image 1.\n"
            "- Near gauntlet: bigger and armoured, its shoulder piece becomes a heavy spiked PAULDRON with three short stone spikes; three glowing "
            "cracks on the gauntlet.\n"
            "- Spear-blade: the back slab is a longer, jagged stone blade with a glowing crack; the crystal spike becomes a bigger MAGMA HEAD with two "
            "short side barbs near its base (like a winged spear), bright orange (#FA842C) with a yellow line (#FFE07A).\n"
            "- Shield: taller heater shield of black stone with a carved horned DEMON FACE emblem whose eyes and mouth glow orange, a thick rim with "
            "four rivets, two short spikes at the bottom point.\n"
            "- Feet: bigger stone boots with glowing cracks."),
        mau=("deep basalt red body (#5E2A24); black-brown stone armour, horns, shield (#2A1E1E / #2E2020); glowing lava (#FFA034, #FFE07A); "
             "fire red-orange (#E03E24), orange (#F48824), yellow (#FFD652); eyes yellow (#FFE070); white fangs; dark-brown ink (#2B2118)."),
        check=["Thân đỏ bazan đậm, có giáp ngực đá với lõi dung nham tròn sáng; sừng to cong ra trước, thêm gai trán.",
               "Bờm lửa to 6–7 lưỡi; giáo đầu tinh thể có hai ngạnh; khiên mặt quỷ có sừng, mắt miệng sáng cam."]),
    "quy_vuong": dict(
        ten="quỷ vương núi lửa: thân hắc diện thạch nứt dung nham khắp người, vương miện lửa, sừng cừu xoắn, giáo lưỡi kích, khiên mắt dung nham",
        body=(
            "DESIGN: a VOLCANO DEMON LORD.\n"
            "- Head-body: black OBSIDIAN (#2A2024) crossed all over by a network of bright glowing lava cracks (#FF8A2A with #FFD25A cores), like "
            "cooling lava rock; the belly patch becomes a glowing molten patch (#F26A2A) with dark crust islands.\n"
            "- Horns: two big RAM HORNS of dark stone (#4A2C24) with orange ridges, each curling backward and around beside the head; small horn "
            "spikes along the top of the head.\n"
            "- Fire on the head: a tall CROWN OF FIRE: five tall upright flame tongues standing in a row like a crown (red-orange outside, orange, "
            "yellow core), the middle one the tallest (top at about y = 20), plus a few small separate flame drops; same hand-drawn campfire style.\n"
            "- Near gauntlet: obsidian with glowing cracks, its shoulder piece a tall flame-shaped stone PAULDRON (a stone shaped like a frozen flame).\n"
            "- Spear-blade: becomes a HALBERD: the back slab is a long obsidian shaft blade with glowing veins, the front is a big crescent-and-spike "
            "magma blade (bright orange #FA842C with a yellow line #FFE07A).\n"
            "- Shield: black obsidian shield with ONE big glowing magma EYE in the middle (orange ring, yellow centre, dark slit pupil) and glowing "
            "cracks radiating from it, a jagged rim.\n"
            "- Feet: obsidian boots with glowing cracks."),
        mau=("black obsidian body and armour (#2A2024); dark stone horns (#4A2C24); glowing lava (#FF8A2A, #FFD25A, #F26A2A); fire red-orange "
             "(#E03E24), orange (#F48824), yellow (#FFD652); eyes yellow (#FFE070); white fangs; dark-brown ink (#2B2118)."),
        check=["Thân hắc diện thạch đen chi chít vết nứt dung nham sáng; bụng là mảng dung nham chảy.",
               "Vương miện lửa 5 lưỡi dựng; sừng cừu xoắn; giáo thành kích lưỡi trăng khuyết; khiên có mắt dung nham."]),
}


def refs():
    return [
        (DANG1, "THE FIRST-STAGE FORM of this creature (approved, 1536x1024, white background): the chubby lava imp. Draw its EVOLVED form: the same "
                "creature, the same pose, the same layout, the same hand-drawn style; change the design as described.",
         "Concept dạng 1 đã duyệt (1536 × 1024): cùng tư thế, cùng bố cục; dạng 2 đổi thiết kế"),
        (B1.KIEM_SI, "an approved hero of the same game (an armoured monkey samurai, a later-stage hero), 1536x1024: match its wobbly dark-brown pen "
                     "line, crayon hatching, completely flat colouring and its fierce, armoured attitude. Do NOT copy its species or colours.",
         "Voọc Tướng đã duyệt: nét, tô phẳng, thần thái mặc giáp"),
        (B1.WORLD_STYLE, "the game's hand-drawn map: use ONLY its line and colouring style.", "Bản đồ vẽ tay: chỉ lấy nét"),
    ]


def main():
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    R = refs()
    gd = ["# Gói gửi GPT: `quy_lava_2` (dạng 2 của tiểu quỷ lava)", "",
          "Dùng lại rig monster_3336 và clip của dạng 1; concept vẽ cùng tư thế, cùng bố cục với dạng 1. Hai hướng là đề xuất của Claude, chờ người "
          "dùng chọn. Ghi chú: `ArtGen/Spine/inbox/quy_lava_ghichu.md`.", ""]
    for k, d in D.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(PK, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {B1.Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {B1.Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or delete "
              "any other file.", "",
              "TASK: draw the SECOND-STAGE (evolved) form of the creature in image 1 as ONE picture, in the hand-drawn style of the approved heroes.", "",
              LAYOUT, "", COMMON, "", d["body"], "", "COLOURS (each area one flat colour): " + d["mau"] + " No purple, no blue, no green.", "",
              "Draw every piece as a clear closed shape with its own ink outline (fire / head-body / each horn / each eye / mouth / gauntlet / "
              "pauldron / knuckles / spear-blade / far fist / shield / each foot). No sparks, no embers in the air, no smoke, no glow, no ground, "
              "no props, no second character.", "",
              B1.LINE.replace("(images 2 and 3)", "(images 1 and 2)"), B1.FLAT.replace("except the designed belly patch", "except the designed areas"),
              B1.BG]
        B1.ghi(p, t)
        print(p)
        gd += [f"## Hướng `{k}`: {d['ten']}", "", f"**Chỉ gửi GPT đường dẫn:** `{B1.Wp(p)}`. GPT lưu vào `{B1.Wp(out)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{B1.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", "Kiểm:", ""] + [f"- {c}" for c in d["check"]] + [
            "- Cùng tư thế, cùng chỗ từng bộ phận như dạng 1 (đặt chồng lên thấy khớp); lộ hai mắt; nắm tay xa nằm SAU khiên.", ""]
    B1.ghi(os.path.join(PK, "HUONG_DAN.md"), gd)


# ---------------------------------------------------------------- lượt 2: mảnh "đúng chỗ, đúng cỡ" từ concept dạng 2 đã duyệt (hướng A, hiep_si)
TO_MANH = {
    "A": [
        "THE HEAD-BODY (about x = 625 to x = 1012, y = 262 to y = 862): the one tall egg-shaped body: the deep basalt-red head with its glowing "
        "cracks and the short stone spike on the brow (about x = 838 to x = 902, y = 262 to y = 362), and the dark stone chest plate covering the "
        "lower body with the round glowing magma core (about x = 822 to x = 900, y = 625 to y = 705). WITHOUT the eyes and WITHOUT the mouth and "
        "fangs: where they are in image 1 draw plain basalt-red skin. WITHOUT the fire, the two big horns, the gauntlet, the pauldron, the "
        "spear-blade, the shield and the boots. Complete everything they hide: the top of the head is one smooth round dome under where the fire "
        "and horns were (top of the dome at about y = 365, the brow spike on it); the left side is a smooth curve behind where the gauntlet and "
        "pauldron were (leftmost at about x = 625); the right side a smooth curve behind the shield at about x = 1012; the bottom a broad rounded "
        "base at about y = 862 (the chest plate continues to it). No legs, no arms. One closed outline all the way around.",
    ],
    "B": [
        "THE FIRE (about x = 318 to x = 1038, y = 10 to y = 470): the whole big mane of flame with all its tongues and its three nested colours, "
        "WITHOUT the two separate small flame drops, WITHOUT the horns and the head. Complete its base: where the head and horns cover it, the flame "
        "continues down (yellow core and orange) and is closed by a broad, gently rounded bottom edge that follows the top of the head at about "
        "y = 470, from about x = 600 to x = 1000. One closed shape.",
        "THE TWO SMALL FLAME DROPS (one at about x = 308 to x = 392, y = 82 to y = 165; one at about x = 253 to x = 347, y = 206 to y = 270): exactly "
        "as in image 1, each its own small closed shape.",
        "THE SPEAR-BLADE (about x = 222 to x = 1004, y = 408 to y = 940): the whole weapon as ONE closed shape, WITHOUT the gauntlet, its knuckles and "
        "the pauldron in front of it: the long jagged dark stone back blade with its glowing crack at the upper left (from its back end at about "
        "x = 225, y = 420), continuing straight down-right behind where the gauntlet was, then a short dark stone collar (about x = 625 to "
        "x = 690, y = 700 to y = 760) where it joins the big orange magma head with its two side barbs and its yellow middle line, ending in a "
        "sharp point at about x = 998, y = 935. Keep the visible parts exactly as in image 1.",
    ],
    "C": [
        "THE SHIELD (about x = 1003 to x = 1247, y = 402 to y = 912): the tall dark stone shield with its rim, its four orange rivets, its glowing "
        "horned demon-face emblem and its two spikes at the bottom, complete (nothing in front of it).",
        "THE NEAR HORN (about x = 588 to x = 806, y = 158 to y = 402): the big curved black horn with its orange cracks that sweeps up and to the "
        "left, complete, its base closed with a rounded edge (no head).",
        "THE NEAR EYE (about x = 760 to x = 872, y = 452 to y = 508) and THE FAR EYE (about x = 922 to x = 997, y = 452 to y = 508): the two "
        "narrow yellow eyes with their ink outlines, exactly as in image 1, each its own closed shape.",
        "THE MOUTH (about x = 798 to x = 962, y = 522 to y = 580): the zigzag ink line with its four white fangs, exactly as in image 1.",
        "THE NEAR LEG (hidden in image 1 behind the gauntlet and the boot): ONE short, thick, stubby leg of the same deep basalt-red skin as the "
        "head (#5E2A24) with one thin glowing crack, from a rounded upper end centred at about x = 700, y = 820 down-left to a rounded lower end "
        "centred at about x = 560, y = 885; about 90 px thick, one closed ink outline all round.",
    ],
    "D": [
        "THE FAR HORN (about x = 938 to x = 1168, y = 198 to y = 392): the big curved black horn with its orange cracks that sweeps out to the "
        "right, complete, its base closed with a rounded edge (no head).",
        "THE FAR FIST (hidden in image 1 behind the shield; draw it at about x = 995 to x = 1080, y = 520 to y = 690): a stack of four chunky dark "
        "stone knuckles with thin glowing cracks, like the knuckles of the near gauntlet but smaller, as ONE closed shape.",
        "THE NEAR BOOT (about x = 425 to x = 657, y = 852 to y = 952): the dark stone boot with its glowing cracks at the bottom left, complete "
        "(its top closed with a rounded edge where the knuckles covered it).",
        "THE FAR BOOT (about x = 843 to x = 1057, y = 790 to y = 952): the dark stone shin guard and boot with its glowing cracks at the bottom "
        "middle right, complete as ONE closed shape (draw the part hidden by the spear-blade).",
    ],
    "E": [
        "THE GAUNTLET (about x = 425 to x = 692, y = 590 to y = 790): the big dark stone forearm block with its long glowing cracks, WITHOUT the "
        "spiked pauldron on top (where the pauldron covers it, draw the block's rounded top edge at about y = 590) and WITHOUT the round knuckles at "
        "its bottom (close its bottom with a rounded edge at about y = 790). One closed shape.",
        "THE CLOSED EYES, NEAR (at about x = 760 to x = 872, y = 470 to y = 505) and FAR (at about x = 922 to x = 997, y = 470 to y = 505): in place "
        "of each open eye, one thick dark-brown ink stroke bent like an upside-down U (a squeezed-shut eye), about as wide as the open eye.",
    ],
    "F": [
        "THE PAULDRON (about x = 443 to x = 712, y = 422 to y = 612): the big spiked dark stone shoulder guard of the near arm with its three "
        "spikes, complete, its lower edge closed with a rounded edge where it overlaps the gauntlet.",
        "THE NEAR KNUCKLES (about x = 443 to x = 640, y = 735 to y = 858): the row of round dark stone knuckle lumps at the bottom of the gauntlet, "
        "as ONE closed cluster (the lumps joined, separating lines kept inside), complete where the gauntlet covers their tops.",
        "THE FAR ARM (hidden in image 1 behind the body and the shield): a short, thick, chubby arm of deep basalt-red skin (#5E2A24) with a dark "
        "stone bracer band near its lower end, from a rounded shoulder end centred at about x = 965, y = 585 to a rounded wrist end centred at "
        "about x = 1045, y = 655; about 80 px thick, one closed ink outline all round. No hand.",
    ],
}


def build_manh():
    duyet = os.path.join(TAI, "L1_duyet.png")
    head = (f"image 1 = {B1.Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: a LAVA KNIGHT demon facing right: a big "
            "mane of fire, two big curved black horns, a tall deep basalt-red head with glowing cracks and a brow spike, narrow yellow eyes, a "
            "zigzag mouth with four fangs, a dark stone chest plate with a round glowing magma core, a huge spiked pauldron and dark stone gauntlet "
            "gripping a winged magma spear, a tall dark shield with a glowing horned demon face, and dark stone boots.")
    rule = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
            "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else and leave pure "
            "white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
            "where a part is hidden behind another part in image 1, DRAW the hidden portion as described. The kept parts must NOT touch each other: "
            "clear white between them. Same wobbly ink line, same line thickness, same colours, same crayon hatching, same completely flat colouring "
            "as image 1. Do not add anything: no shadows, no glow, no sparks, no labels. Coordinates are pixels on the 1536x1024 canvas (x from the "
            "left, y from the top).")
    for ten, ds in TO_MANH.items():
        out = os.path.join(TAI, f"M_{ten}.png")
        p = os.path.join(PK, f"luot_2_manh_{ten}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", head, "", f"SAVE: save it as a PNG to {B1.Wp(out)}",
             f"If a file with that name already exists, save as M_{ten}_2.png, M_{ten}_3.png ... in the same folder. Do not edit, move or delete "
             "any other file.", "", rule, "", "KEEP:"]
        t += [f"{i}. {d}" for i, d in enumerate(ds, 1)]
        B1.ghi(p, t + ["", B1.FLAT.replace("except the designed belly patch", "except the designed areas"), B1.BG])
        print(p)


# ---------------------------------------------------------------- lượt 3: dáng HAI TAY ÔM GIÁO DỰNG của chiêu cuối (đổi ảnh)
# Người dùng (2026-11-13, kèm hình vẽ vị trí): giáo dọc phía bên phải thân, tay phải nắm cán phía ngoài, tay trái vòng qua bụng; "tay trái sao bạn lại
# bẻ cánh tay đi 90 độ, tay phải nhìn không rõ, cần ảnh thì gen thêm cho hợp". Ghép từ mảnh của dáng đứng không ra dáng này → gen một hình dáng ôm
# giáo (cam1), rồi tách riêng khối hai tay + giáo (cam2); rig đổi sang khối đó trong đoạn cầm giáo.
CAM_DANG = (
    "NEW ARM POSE (the only change): the creature now holds its spear VERTICALLY with BOTH hands, ready to stab straight down:\n"
    "- THE SPEAR stands straight up and down on the RIGHT side of the body, a little right of the middle: the shaft runs vertically at about "
    "x = 890, the long jagged dark stone back blade pointing UP (its top end at about y = 90, in front of the fire, between the horns), the short "
    "dark stone collar at about y = 600 to y = 650, and the big orange winged magma head pointing straight DOWN, its sharp tip at about x = 890, "
    "y = 1010. Same spear design as image 1, only turned upright.\n"
    "- THE NEAR (LEFT) ARM reaches ACROSS THE BELLY: the spiked pauldron stays on the shoulder exactly where it is in image 1 (about x = 443 to "
    "x = 712, y = 422 to y = 612); below it a short thick basalt-red upper arm goes down and slightly right to the elbow at about (640, 700); the big "
    "dark stone gauntlet forearm lies almost horizontally across the front of the belly from the elbow to the spear, and its fist of round "
    "knuckles closes around the shaft just above the collar at about x = 850 to x = 940, y = 560 to y = 660, the knuckles facing the viewer and "
    "wrapping IN FRONT of the shaft.\n"
    "- THE FAR (RIGHT) ARM: a short thick basalt-red arm with a dark stone bracer comes from the right side of the body (shoulder at about "
    "x = 1000, y = 560), bends, and its fist of four dark stone knuckles grips the shaft from the OUTSIDE (the right side) just ABOVE the left fist, "
    "at about x = 880 to x = 975, y = 470 to y = 560, the knuckles wrapping in front of the shaft.\n"
    "- THE SHIELD is slung on the back: not visible.\n"
    "Everything else stays EXACTLY as in image 1 (same place, same size, same shapes): the fire, both horns, the head-body with its brow spike, "
    "cracks, chest plate and magma core, the eyes, the mouth and fangs, both boots. Where the spear and the hands now cover the face or the body, "
    "they are simply in front of it.")


def build_cam():
    duyet = os.path.join(TAI, "L1_duyet.png")
    out1 = os.path.join(TAI, "L2_cam_giao.png")
    p1 = os.path.join(PK, "luot_3_cam_giao.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {B1.Wp(duyet)}: THE CHARACTER, already drawn and approved (1536x1024, white background): a lava knight demon with a big fire "
         "mane, big curved horns, a spiked pauldron and stone gauntlet on the near arm holding a winged magma spear diagonally, and a tall demon-face "
         "shield in the far hand.",
         "", f"SAVE: save it as a PNG to {B1.Wp(out1)}",
         "If a file with that name already exists, save as L2_cam_giao_2.png, L2_cam_giao_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 1 with the SAME creature, the SAME design, the SAME colours, the SAME wobbly dark-brown ink line, crayon hatching and "
         "completely flat colouring, on the same canvas at the same place and size, changing ONLY the arms, the spear and the shield as follows.", "",
         CAM_DANG, "",
         "No sparks, no glow, no motion lines, no ground, no props, no second character.", "",
         B1.FLAT.replace("except the designed belly patch", "except the designed areas"), B1.BG]
    B1.ghi(p1, t)
    print(p1)
    if not os.path.exists(out1):
        return
    out2 = os.path.join(TAI, "M_cam.png")
    p2 = os.path.join(PK, "luot_3b_tach_tay_giao.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {B1.Wp(out1)}: the creature holding its spear upright with both hands (1536x1024, white background).",
         "", f"SAVE: save it as a PNG to {B1.Wp(out2)}",
         "If a file with that name already exists, save as M_cam_2.png, M_cam_3.png ... in the same folder. Do not edit, move or delete any other "
         "file.", "",
         "TASK: redraw image 1, but keep ONLY the parts listed under KEEP, in exactly the SAME POSITION and at exactly the SAME SIZE as in image 1 "
         "(laid over image 1 they must coincide). REMOVE everything else (the fire, the horns, the head-body, the face, the boots) and leave pure white "
         "(#FFFFFF) there. Same wobbly ink line, same colours, same crayon hatching, same completely flat colouring as image 1. No shadows, no glow, "
         "no labels.", "",
         "KEEP, as ONE single closed group (these parts touch and overlap each other, that is fine):",
         "1. THE SPEAR, whole and upright (back blade at the top, collar, magma head at the bottom), drawn complete where the hands cover it (the "
         "shaft continues behind the fists).",
         "2. THE NEAR ARM: the spiked pauldron, the basalt-red upper arm and the stone gauntlet forearm with its fist closed around the shaft (fist IN "
         "FRONT of the shaft). Where the body covered the upper arm, draw it complete with a rounded shoulder end hidden under the pauldron.",
         "3. THE FAR ARM: the basalt-red arm with its bracer and its fist closed around the shaft above the near fist (fist IN FRONT of the shaft). Its "
         "shoulder end, hidden behind the body in image 1, is drawn complete and rounded at about x = 1000, y = 560.", "",
         B1.FLAT.replace("except the designed belly patch", "except the designed areas"), B1.BG]
    B1.ghi(p2, t)
    print(p2)


if __name__ == "__main__":
    if sys.argv[1:2] == ["manh"]:
        build_manh()
    elif sys.argv[1:2] == ["cam"]:
        build_cam()
    else:
        main()
