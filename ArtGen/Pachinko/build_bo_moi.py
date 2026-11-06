# Gói gửi GPT "bộ mới" của máy bi (2026-11-06). Người dùng: xem thiết kế máy bi của máy tham khảo (nút, đinh…) rồi lên prompt
# làm giống họ theo style mình, xem toàn bộ hiệu ứng của họ. Bảng đối chiếu bộ phận và 36 hiệu ứng của máy đó: THAM_KHAO_MAY_BI.md.
# Chỉ học bộ phận, trạng thái và nhịp hiệu ứng; hình vẽ mới theo nét đã duyệt của mình. Không đính ảnh của game đó cho GPT,
# không nhắc tên game.
# Ba lượt, mỗi lượt một tờ 1536 × 1024 lưới 4 × 3 (G_Sheet4x3), ảnh mẫu đều là ảnh đã có (thân máy, bộ phận, hiệu ứng đã duyệt):
#   luot_1_nut.txt: nút thả tròn kiểu nút bấm máy (sẵn sàng, nhấn, hết bi, cược lớn), nút thả liền (thường, đang chạy),
#     viên cược (thường, đang chọn, khoá, mức cao nhất), bảng nút dưới máy, bàn tay chỉ (hướng dẫn);
#   luot_2_trang_thai.txt: bản sáng của đinh, nấm, u lồi, cốc bạc, tấm két; bóng đèn vòm tắt, sáng vàng, sáng hồng;
#     lớp sáng ô đáy (thường, ô rương); mây nháy mắt, mây há miệng;
#   luot_3_hieu_ung.txt: 12 hình hạt mới tô phẳng có viền mực (loé, vòng dày, vòng đứt, chấm, mảnh tam giác, tia toả, xoáy,
#     sao rỗng, lấp lánh rỗng, cặp ngoặc, vạch tốc, dây giấy), thay cho các lớp quầng mềm của máy tham khảo.
# GPT lưu tai_ve/nut.png, tai_ve/trang_thai.png, tai_ve/hieu_ung_2.png.
# Chạy: py -3 -I ArtGen/Pachinko/build_bo_moi.py
# Duyệt: py -3 -I ArtGen/Pachinko/build_bo_moi.py --duyet nut|trang_thai|hieu_ung_2 [ảnh] (mặc định ảnh mới nhất trong tai_ve):
#   tách khối liền theo ô chứa tâm khối (món tràn ô như bảng nút vẫn đủ), gọt sát, bỏ khung mực GPT vẽ thừa quanh lớp sáng ô,
#   canh các trạng thái của cùng một món vào chung một khung (nút: đáy giữa; viên cược, bóng đèn: tâm tròn) để đổi hình không nhảy,
#   thu về cỡ hiện trên màn, lưu Assets/03 Art/Pachinko/pk_*.png (tên ở NAMES).
import argparse
import json
import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True  # nạp build.py làm thư viện, không để __pycache__ trong ArtGen
HERE = Path(__file__).resolve().parent  # ArtGen/Pachinko
_spec = importlib.util.spec_from_file_location("pk_build", HERE / "build.py")
pk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pk)

PACK = HERE / "gui_gpt" / "bo_moi"
INBOX = pk.INBOX
REFS = pk.REFS
GRID = pk.GRID43
ROOT = HERE.parent.parent  # project
SHOT_SRC = ROOT / "Temp" / "PokiShots" / "ui" / "10_may_bi.png"  # ảnh chụp màn Máy bi nền gỗ (2026-11-06)
SHOT = REFS / "man_may_bi_go.png"
WOOD = "#7D5031"

# tên ảnh trong game theo thứ tự ô; cạnh dài tối đa khi lưu (px, theo cỡ hiện trên màn 1080 × 1920)
NAMES = {
    "nut": [("pk_nut_tha", 384), ("pk_nut_tha_nhan", 384), ("pk_nut_tha_het", 384), ("pk_nut_tha_lon", 384),
            ("pk_nut_lien", 224), ("pk_nut_lien_bat", 224), ("pk_cuoc", 128), ("pk_cuoc_chon", 128),
            ("pk_cuoc_khoa", 128), ("pk_cuoc_max", 128), ("pk_bang_nut", 1024), ("pk_tay_chi", 192)],
    "trang_thai": [("pk_dinh_sang", 64), ("pk_bumper_sang", 128), ("pk_u_loi_sang", 64), ("pk_coc_sang", 96),
                   ("pk_ket_sang", 384), ("pk_den_tat", 64), ("pk_den_sang", 64), ("pk_den_sang_hong", 64),
                   ("pk_o_sang", 256), ("pk_o_sang_ruong", 256), ("pk_may_tha_nhay", 256), ("pk_may_tha_wow", 256)],
    "hieu_ung_2": [("pk_fx_loe", 256), ("pk_fx_vong_day", 256), ("pk_fx_vong_dut", 256), ("pk_fx_cham", 64),
                   ("pk_fx_tam_giac", 96), ("pk_fx_tia_toa", 384), ("pk_fx_xoay", 256), ("pk_fx_sao_rong", 192),
                   ("pk_fx_lap_lanh_rong", 192), ("pk_fx_ngoac", 256), ("pk_fx_vach_toc", 192), ("pk_fx_day_giay", 192)],
}
SQUARE = {"hieu_ung_2"}  # hạt: đặt vào ảnh vuông (game đặt cỡ vuông)
# các trạng thái của cùng một món (số ô từ 0) và cách canh: "bottom" đáy giữa (nút: đế đứng yên, nắp lún), "circle" tâm hàng rộng nhất
GROUPS = {"nut": [((0, 1, 2, 3), "bottom"), ((4, 5), "bottom"), ((6, 7, 8, 9), "circle")],
          "trang_thai": [((5, 6, 7), "circle"), ((10, 11), "bottom")]}
FRAMED = {"trang_thai": (8, 9)}  # lớp sáng ô: GPT vẽ thêm khung chữ nhật mực, gọt bỏ


def grid_ref():
    return (GRID, "1536 x 1024", "the numbered 4 x 3 grid of the sheet you draw: one item per cell, inside the grey inner box",
            "lưới 4 × 3 đánh số (ô hồng, khung xám là vùng an toàn)")


def head(refs, out):
    L = [pk.HEAD, "", "REFERENCE IMAGES (open each file from its full path):"]
    L += [f"image {i} = {p} ({size}): {what}" for i, (p, size, what, _) in enumerate(refs, 1)]
    return L + ["", pk.sheet_save(out), ""]


def tail(out, avoid, what):
    return ["", pk.STYLE_CAB, "", *pk.NO_SHADOW, "",
            f"AVOID: {avoid}", "", f"Remember: transparent background, one {what} per cell in the order 1 to 12, save the sheet to {out}"]


# ---------- lượt 1: nút ----------

def turn_buttons(cab):
    out = INBOX / "nut.png"
    refs = [cab, grid_ref(),
            (SHOT, "540 x 960", f"a screenshot of the machine screen in the game today: the machine stands on a warm brown wooden "
                                f"table ({WOOD}); the bet buttons are the column on the left, the two flat drop buttons sit under the "
                                "machine; your round buttons replace them. Shown so you understand the space and the background",
             "ảnh chụp màn Máy bi bây giờ (nền bàn gỗ nâu, cột cược bên trái, hai nút thả chữ nhật dưới máy)")]
    L = head(refs, out) + [
        "WHAT THIS IS: the controls of the ball-drop machine (a vertical pachinko) whose cabinet is image 1. The player presses a "
        "big round arcade push-button under the machine to drop a ball, or holds it to keep dropping; a smaller round button drops "
        "twenty balls in a row; round tokens on the left choose the bet. Every button is a fairground toy of the same family as "
        "the cabinet: chunky, round, friendly, drawn by hand. The game writes every label (THẢ BI, ×2, ×5…) on top by itself, so "
        "the tops and centres stay EMPTY and calm.",
        "", f"BACKGROUND IN THE GAME: warm brown wood {WOOD} (image 3). Give every button a light cream rim and a thick dark ink "
            "outline so it reads clearly on that brown.",
        "", pk.SHEET_RULE, "",
        "SAME SHAPE RULE: cells 1 to 4 are ONE big button drawn four times in exactly the same size, outline and position inside "
        "its box; only the colours and the height of the cap change. The same for cells 5 and 6, and for cells 7 to 10.",
        "",
        "CELLS:",
        "1 BIG DROP BUTTON, READY (shown about 300 x 230 px): a big round arcade push-button seen from the front and a little from "
        "above: a chunky domed cap in coral red #E8553F standing in a thick round cream #FBF4E2 collar, which sits on a short round "
        "wooden base in orange #F39A2D. The top of the dome is one calm flat red area, empty (the label goes there); a little "
        "crayon hatching on the sides of the dome only; a small cream dot near the top left of the dome. About 4 : 3 wide to tall.",
        "2 BIG DROP BUTTON, PRESSED: the same collar and base, same size and place; the cap pushed down so only a thin low dome "
        "shows above the collar; the red a little darker #C8432F.",
        "3 BIG DROP BUTTON, NO BALLS: exactly the shape of 1; cap dull grey-brown #B8A898, collar #E2DCCD, base light brown; no red.",
        "4 BIG DROP BUTTON, BIG BET: exactly the shape of 1; cap golden yellow #F7C948, a ring of five small doodled stars around "
        "the lower edge of the dome, base teal #3FB8A9.",
        "5 SMALL AUTO-DROP BUTTON (shown 170 x 130 px): a smaller round push-button of the same family: orange #F39A2D domed cap, "
        "cream collar, wooden base, empty top. About 4 : 3.",
        "6 SMALL AUTO-DROP BUTTON, RUNNING: exactly the shape of 5; the cap pushed half down and coloured teal #3FB8A9.",
        "7 BET TOKEN (shown 96 x 96 px): a chunky round wooden token like a big board-game coin seen from the front: a flat cream "
        "#FBF4E2 face, a thick orange-brown rim #C9824A, empty centre (the game writes ×1, ×2…).",
        "8 BET TOKEN, CHOSEN: exactly the shape of 7; yellow #F7C948 face, darker gold rim, four tiny ink tick marks around the "
        "token as if it pops (marks only, no glow).",
        "9 BET TOKEN, LOCKED: exactly the shape of 7; grey #E2DCCD face and grey rim, a small padlock drawn on the lower right of "
        "the rim; the centre stays empty.",
        "10 BET TOKEN, TOP BET CHOSEN: exactly the shape of 7; purple #9A6AD6 face, golden rim, one tiny star on the top of the rim.",
        "11 BUTTON CONSOLE (shown 1000 x 250 px): a wide low wooden console that stands under the machine and holds the buttons: a "
        "long rounded rectangle in red-orange wood #E8553F with a cream #FBF4E2 inset panel and a few rivets; in the panel two "
        "EMPTY round sockets: a big one centred at 35 % of the width (diameter about 85 % of the panel height) and a smaller one "
        "centred at 78 % of the width (diameter about 55 % of the panel height), each a plain dark-brown hole with an ink rim. "
        "About 4 : 1, as wide as the inner box.",
        "12 POINTING HAND (shown 120 x 120 px): a cute cartoon hand in a white glove pointing down and to the left with the index "
        "finger (it shows new players where to tap): flat white with light grey hatching, thick ink outline.",
    ] + tail(out, "text, letters, numbers, labels, symbols on the button tops, characters, a background, a table, glow, light "
                  "rays, glossy highlights, two items in one cell.", "item")
    return dict(n=1, kind="nut", vi="nút thả, nút thả liền, viên cược", file=PACK / "luot_1_nut.txt", out=out, refs=refs, lines=L,
                what_vi="Nút thả tròn kiểu nút bấm máy thay hai nút chữ nhật dưới máy (học từ nút bấm vòm của máy tham khảo: một hình, "
                        "nhiều trạng thái đổi màu, nhấn thì lún), viên cược tròn thay cột ×1…×10, bảng nút dưới máy, bàn tay chỉ cho "
                        "hướng dẫn. Chữ (THẢ BI, ×2…) game tự viết đè lên.",
                checks=["lưới 1536 × 1024, nền trong suốt, mỗi ô một món đúng số, không chạm mép ô;",
                        "ô 1–4 cùng một nút y hệt dáng, cỡ, chỗ; chỉ khác màu (đỏ, đỏ lún, xám, vàng sao); ô 2 nắp lún thấp;",
                        "ô 5–6 và ô 7–10 cũng cùng dáng trong nhóm; viên khoá có ổ khoá nhỏ ở mép;",
                        "mặt nút, giữa viên cược trống trơn (không chữ, không số, không ký hiệu);",
                        "bảng nút ô 11 dài khoảng 4 : 1, có hai hốc tròn trống (to bên trái, nhỏ bên phải);",
                        "không bóng đổ, không quầng sáng, không bóng loáng; viền kem và viền mực rõ để nổi trên nền gỗ nâu."],
                fixes=["Same sheet, but cells 1 to 4 must be exactly the same button shape and size; only the colours change.",
                       "Same sheet, but leave the tops of the buttons and the centres of the tokens completely empty, no text.",
                       "Same sheet, but no shadow under the buttons and no glossy highlight; flat colours with crayon hatching."],
                after_vi=f"Xong thì nhắn Claude \"duyệt nút\". Tự cắt: `py -3 -I {HERE / 'build_bo_moi.py'} --duyet nut` (lưu "
                         "`Assets/03 Art/Pachinko/pk_nut_*.png`, `pk_cuoc*.png`, `pk_bang_nut.png`, `pk_tay_chi.png`); nối vào màn Máy bi "
                         "là việc code của Claude.")


# ---------- lượt 2: trạng thái mặt máy ----------

def turn_states(cab):
    out = INBOX / "trang_thai.png"
    parts = pk.latest("bo_phan*.png")
    refs = [cab, grid_ref(),
            (parts, "1536 x 1024", "the approved parts of this machine's board (transparent background), 4 x 3 cells: 1 peg, "
                                   "2 red mushroom bumper, 3 wooden wall knob, 4 slot post, 5 silver cup, 6 vault roof plank, 7 vault "
                                   "floor, 8 cloud launcher, 9 ball, 10 shoulder plank, 11 launcher rail, 12 golden vault plate; the lit "
                                   "versions you draw must keep their exact outlines",
             "tờ bộ phận đã duyệt (đinh, nấm, u lồi, cọc, cốc bạc, mái két, đáy két, mây, bi, ván vai, ray, tấm két)")]
    L = head(refs, out) + [
        "WHAT THIS IS: extra states of the board parts of the ball-drop machine of image 1. When a ball hits a part, the game swaps "
        "the normal drawing (image 3) for its LIT drawing for a split second, so each lit part must have EXACTLY the outline, size "
        "and proportions of the matching normal part; only the colours inside change. Light is shown with flat bright colours and "
        "small ink marks, never with glow.",
        "", pk.SHEET_RULE, "",
        "CELLS:",
        "1 PEG, LIT (shown 17 px): the peg of image 3 cell 1, same outline; its head bright yellow #F7C948 with a small flat white "
        "five-pointed star in the middle; thick ink outline.",
        "2 MUSHROOM BUMPER, LIT (shown 55 px): the mushroom cap of image 3 cell 2, same outline and the same five spots; the cap "
        "bright orange #FF9F43, the spots pale yellow #FFF2A8, the cream ring bright yellow #F7C948.",
        "3 WALL KNOB, LIT (shown 34 px): the knob of image 3 cell 3, same outline; bright orange-yellow #FFB347 with a pale yellow "
        "centre.",
        "4 SILVER CUP, LIT (shown 40 x 28 px): the cup of image 3 cell 5, same outline; its body pale yellow #FFF2A8 and its rim "
        "bright yellow #F7C948.",
        "5 GOLDEN VAULT PLATE, LIT (shown 165 x 75 px): the hexagon plate of image 3 cell 12, same outline; flat bright yellow "
        "#FFE052 with four small doodled sparkle stars on it.",
        "6 CREST BULB, OFF (shown 26 px): one small round light bulb like those on the arched crest of image 1, switched off: pale "
        "cream-yellow #F3E7C9, thick ink outline. Round.",
        "7 CREST BULB, ON: the same bulb lit: bright yellow #F7C948, one small white dot near its top left and four tiny ink tick "
        "marks around it like a comic shine (marks only, no glow, no rays of light).",
        "8 CREST BULB, ON, PINK: exactly 7 in pink #F07FA6 (the game alternates colours along the crest).",
        "9 SLOT LIGHT (shown about 60 x 185 px): a tall rectangle that lights up a prize slot when a ball lands in it: seven white "
        "crayon rays fanning up from the bottom centre, with transparent gaps between them, flat white, a thin ink edge on each "
        "ray. About 1 : 3. The game tints it with the colour of the slot.",
        "10 CHEST SLOT LIGHT: exactly the shape of 9, plus three small hollow white stars near the top between the rays.",
        "11 CLOUD LAUNCHER, BLINK: the cloud of image 3 cell 8, same outline and size; eyes closed in two happy upside-down U "
        "curves and a bigger smile (it blinks when it drops a ball).",
        "12 CLOUD LAUNCHER, WOW: the same cloud; eyes wide open round dots with a white dot each and a small round open mouth (when "
        "a ball lands in the golden vault).",
        "", "COLOURS: the lit colours listed above, the normal colours of image 3 for unchanged areas, dark-brown ink #2B2118 "
            "outlines; 9 and 10 white only.",
    ] + tail(out, "text, letters, numbers, characters except the cloud's face, a background, glow, halos, light rays around the "
                  "parts, changed outlines, two items in one cell.", "item")
    return dict(n=2, kind="trang_thai", vi="trạng thái sáng của mặt máy", file=PACK / "luot_2_trang_thai.txt", out=out,
                refs=refs, lines=L,
                what_vi="Bản sáng của đinh, nấm, u lồi, cốc bạc, tấm két (máy tham khảo đổi hình đinh sang hình sáng 0,067 giây mỗi lần "
                        "bi chạm); bóng đèn vòm tắt, sáng vàng, sáng hồng để game cho đèn chạy; lớp sáng ô đáy khi bi rơi vào; mây nháy "
                        "mắt khi thả, mây há miệng khi trúng két.",
                checks=["lưới 1536 × 1024, nền trong suốt, mỗi ô một món đúng số;",
                        "ô 1–5 trùng khít viền và cỡ với ô 1, 2, 3, 5, 12 của tờ bộ phận, chỉ đổi màu sáng; nấm vẫn 5 chấm;",
                        "bóng đèn 6–8 cùng một dáng; đèn sáng có vạch mực nhỏ quanh, không quầng sáng;",
                        "ô 9–10 là chữ nhật đứng khoảng 1 : 3, tia trắng từ đáy toả lên, khe trong suốt giữa các tia;",
                        "mây 11–12 trùng dáng mây cũ, chỉ đổi mặt (nhắm cười, tròn mắt há miệng);",
                        "không chữ, không bóng đổ, không quầng sáng."],
                fixes=["Same sheet, but each lit part must have exactly the outline and size of the matching part in image 3.",
                       "Same sheet, but no glow at all: light is only flat bright colour and small ink tick marks.",
                       "Same sheet, but the slot lights 9 and 10 white only, rays with transparent gaps, about 1 : 3."],
                after_vi=f"Xong thì nhắn Claude \"duyệt trạng thái\". Tự cắt: `py -3 -I {HERE / 'build_bo_moi.py'} --duyet trang_thai` "
                         "(lưu `pk_dinh_sang`, `pk_bumper_sang`, `pk_u_loi_sang`, `pk_coc_sang`, `pk_ket_sang`, `pk_den_*`, `pk_o_sang*`, "
                         "`pk_may_tha_nhay`, `pk_may_tha_wow`); nối vào mặt máy là việc code của Claude.")


# ---------- lượt 3: hạt hiệu ứng mới ----------

def turn_fx(cab):
    out = INBOX / "hieu_ung_2.png"
    fx = pk.latest("hieu_ung.png") or pk.latest("hieu_ung*.png")
    refs = [cab, grid_ref(),
            (fx, "1536 x 1024", "the six effect sprites the game already uses (white, transparent background), 3 x 2 cells: glow, "
                                "sparkle, ring, star, streak, puff; match the hand-drawn white star and puff (cells 4 and 6): white "
                                "fill, light grey crayon hatching, thin dark-brown ink outline",
             "6 hình hiệu ứng đang dùng (trắng, nền trong suốt): quầng, lấp lánh, vòng, sao, vệt, khói")]
    L = head(refs, out) + [
        "WHAT THIS IS: twelve more small effect sprites for the ball-drop machine of image 1 (pops when a ball hits, rings and "
        "rays when it lands in a slot or the vault, confetti for chests, a whirl while a button charges). The game scales, "
        "rotates, fades and TINTS them with many colours, so draw them white with light grey crayon hatching and a thin "
        "dark-brown ink outline, like the star and the puff of image 3. Everything is FLAT: the bright moments of this game are "
        "drawn as solid shapes, never as soft glows.",
        "", pk.SHEET_RULE, "",
        "CELLS:",
        "1 FLASH BURST: a flat white comic burst shape with ten uneven pointed spikes around a round centre, thin ink outline.",
        "2 THICK RING: a round ring drawn with a fat crayon, solid white, its band about one fifth of the diameter wide, thin ink "
        "edge inside and outside, empty centre.",
        "3 DASHED RING: a round ring made of twelve short thick white dashes with even gaps between them, each dash with a thin "
        "ink outline, empty centre.",
        "4 DOT: one round white dot with a thin ink outline, filling the grey box (it is shown tiny).",
        "5 TRIANGLE CONFETTI: one small white triangle with slightly rounded corners, thin ink outline, light hatching.",
        "6 SUNBURST: twelve flat white rays, alternating long and short, around an empty round centre, each ray a thin pointed "
        "wedge with a thin ink outline; transparent between the rays. The game puts it behind rewards and turns it slowly.",
        "7 SWIRL: a white spiral of two and a half turns drawn as one thick crayon stroke with thin ink edges, like a little "
        "whirlpool seen from above.",
        "8 HOLLOW STAR: a chubby five-pointed star with rounded tips drawn only as a thick white band (hollow, transparent "
        "centre), thin ink edges inside and outside.",
        "9 HOLLOW SPARKLE: a four-pointed sparkle with slim points straight up, down, left and right, drawn only as a white band "
        "(hollow centre), thin ink edges.",
        "10 ARC PAIR: two thick white curved arcs facing each other like round brackets ( ), together forming a broken circle "
        "with wide gaps at the top and bottom, thin ink edges.",
        "11 SPEED LINES: three short white comic speed lines one above the other, slightly fanned, each thick and rounded at the "
        "RIGHT end and tapering to a point on the LEFT, thin ink outline.",
        "12 PAPER STREAMER: one short curly white paper ribbon with two twists, thin ink outline, light hatching.",
        "", "COLOURS: only white, very pale grey hatching and dark-brown ink #2B2118 outlines. No other colour: the game tints "
            "every sprite.",
        "", "FLAT RULE: no glow, no halo, no soft or blurry edges, no gradients, no fading; every sprite is a crisp solid shape.",
    ] + tail(out, "text, letters, numbers, characters, a background, colours, glow, soft fading, sparkles outside the cells, two "
                  "effects in one cell.", "effect")
    return dict(n=3, kind="hieu_ung_2", vi="hạt hiệu ứng mới", file=PACK / "luot_3_hieu_ung.txt", out=out, refs=refs, lines=L,
                what_vi="12 hình hạt mới cho các bộ hiệu ứng chép từ máy tham khảo (bảng ở `THAM_KHAO_MAY_BI.md`). Máy đó dùng nhiều "
                        "lớp quầng mềm (glow, flash); luật mình tô phẳng nên lớp đó thay bằng hình loé, vòng dày, tia toả vẽ tay. GPT "
                        "vẽ trắng, game tô màu.",
                checks=["lưới 1536 × 1024, nền trong suốt, mỗi ô một hình đúng thứ tự;",
                        "chỉ trắng, gạch chì xám nhạt, viền mực nâu mảnh; không màu khác;",
                        "hình nào cũng sắc nét, phẳng: không quầng, không mờ mép, không chuyển màu;",
                        "vòng 2, 3, sao 8, lấp lánh 9, xoáy 7, ngoặc 10 rỗng giữa (trong suốt); vạch tốc đầu tròn bên phải;",
                        "không chữ, không nền."],
                fixes=["Same sheet, but only white with light grey hatching and thin dark-brown outlines, no colour at all.",
                       "Same sheet, but no glow and no soft edges: every effect a crisp flat shape with an ink outline.",
                       "Same sheet, but each effect smaller and fully inside the grey box of its cell."],
                after_vi=f"Xong thì nhắn Claude \"duyệt hiệu ứng 2\". Tự cắt: `py -3 -I {HERE / 'build_bo_moi.py'} --duyet hieu_ung_2` "
                         "(lưu `Assets/03 Art/Pachinko/pk_fx_*.png`, tên không trùng ảnh thay thế trong Fallback); thêm vào các bộ hạt "
                         "trong `MachineFx.cs` là việc code của Claude.")


# ---------- hướng dẫn ----------

def guide(turns):
    g = ["# Gói gửi GPT: máy bi, bộ mới (nút, trạng thái sáng, hạt hiệu ứng)", "",
         f"Sinh bằng `{HERE / 'build_bo_moi.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè).", "",
         "Học từ máy bi tham khảo: bộ phận nào có, mỗi bộ phận mấy trạng thái, hiệu ứng nào chạy lúc nào. Bảng đối chiếu đủ bộ phận "
         f"và 36 hiệu ứng của máy đó ở `{HERE / 'THAM_KHAO_MAY_BI.md'}`. Hình vẽ mới theo nét đã duyệt của mình (thân máy, tờ bộ "
         "phận): không đính ảnh của game đó cho GPT, không nhắc tên game.", "",
         f"Màn Máy bi giờ nằm trên mặt bàn gỗ nâu ({WOOD}), nên nút cần viền kem và viền mực rõ. Mọi tờ: không bóng đổ, không quầng "
         "sáng (luật UI và hiệu ứng tô phẳng).", "",
         "**Chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. "
         "Ba lượt độc lập, gửi lượt nào trước cũng được.", ""]
    for t in turns:
        g += [f"## Lượt {t['n']}: {t['vi']}", "",
              f"File prompt: `{t['file']}`. GPT lưu `{t['out']}` (trùng tên thì thêm `_2`, `_3`).", "", t["what_vi"], "",
              "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        for i, (p, size, _, look_vi) in enumerate(t["refs"], 1):
            g.append(f"| {i} | `{p}` | {look_vi} ({size.replace(' x ', ' × ')}) |")
        g += ["", "Soi:"] + [f"- {c}" for c in t["checks"]] + ["", "Câu sửa nhanh (gửi kèm đường dẫn file prompt):"]
        g += [f"- `{q}`" for q in t["fixes"]] + ["", t["after_vi"], ""]
    (PACK / "HUONG_DAN.md").write_text("\n".join(g) + "\n", encoding="utf-8")


# ---------- duyệt ----------

def pieces(src):
    """12 món theo lưới 4 × 3: mỗi khối liền (alpha > 8) về ô chứa tâm khung của nó, nên món tràn sang ô bên vẫn cắt đủ"""
    im = Image.open(src).convert("RGBA")
    if im.size != (1536, 1024):
        sys.exit(f"Ảnh {src} cỡ {im.size}, cần 1536 x 1024")
    a = np.array(im)
    lab, _ = ndimage.label(a[..., 3] > 8)
    cells = [[] for _ in range(12)]
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None or (lab[sl] == i).sum() < 30:
            continue  # bụi
        cx, cy = (sl[1].start + sl[1].stop) / 2, (sl[0].start + sl[0].stop) / 2
        cells[min(3, int(cx // 384)) + 4 * min(2, int(cy * 3 // 1024))].append((i, sl))
    out = []
    for k, comps in enumerate(cells):
        if not comps:
            sys.exit(f"Ô {k + 1} của {src.name} trống")
        y0, y1 = min(s[0].start for _, s in comps), max(s[0].stop for _, s in comps)
        x0, x1 = min(s[1].start for _, s in comps), max(s[1].stop for _, s in comps)
        keep = np.isin(lab[y0:y1, x0:x1], [i for i, _ in comps])
        crop = a[y0:y1, x0:x1].copy()
        crop[..., 3] = np.where(keep, crop[..., 3], 0)
        out.append(Image.fromarray(crop))
    return out


def unframe(im):
    """bỏ khung chữ nhật mực quanh hình: gọt vào từ mỗi mép qua hết dải mực đầu tiên, rồi gọt sát lại"""
    a = np.array(im)
    ink = (a[..., 3] > 128) & (a[..., :3].max(-1) < 110)
    h, w = ink.shape

    def depth(line):
        n = 0
        while n < len(line) // 4 and not line[n]:
            n += 1  # mép trong suốt
        while n < len(line) // 4 and line[n]:
            n += 1  # dải mực
        return n + 2

    l, r = depth(ink[h // 2]), depth(ink[h // 2][::-1])
    t, b = depth(ink[:, w // 2]), depth(ink[:, w // 2][::-1])
    inner = im.crop((l, t, w - r, h - b))
    m = np.array(inner)[..., 3] > 8
    return inner.crop(pk.bbox(m))


def anchor(im, mode):
    a = np.array(im)[..., 3] > 8
    ys, xs = np.where(a)
    if mode == "bottom":
        return (xs.min() + xs.max()) / 2, ys.max() + 1
    rows = a.sum(1)
    cy = np.where(rows >= rows.max() * 0.97)[0].mean()
    line = np.where(a[int(round(cy))])[0]
    return (line.min() + line.max()) / 2, cy


def align(ims, mode):
    """đặt các trạng thái vào chung một khung, khớp điểm neo (cùng cỡ, cùng chỗ khi đổi hình)"""
    anc = [anchor(im, mode) for im in ims]
    left = max(ax for ax, _ in anc)
    right = max(im.width - ax for im, (ax, _) in zip(ims, anc))
    top = max(ay for _, ay in anc)
    bottom = max(im.height - ay for im, (_, ay) in zip(ims, anc))
    W, H = int(np.ceil(left + right)), int(np.ceil(top + bottom))
    out = []
    for im, (ax, ay) in zip(ims, anc):
        c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        c.paste(im, (int(round(left - ax)), int(round(top - ay))), im)
        out.append(c)
    return out


def approve(kind, src):
    ims = pieces(src)
    for k in FRAMED.get(kind, ()):
        ims[k] = unframe(ims[k])
    for idx, mode in GROUPS.get(kind, []):
        for k, im in zip(idx, align([ims[k] for k in idx], mode)):
            ims[k] = im
    for (name, side), im in zip(NAMES[kind], ims):
        if kind in SQUARE:
            im = pk.square(im)
        elif name == "pk_bumper_sang":
            im = pk.square(im, 0.03)  # cùng lề với pk_bumper (build.py approve_parts) để đổi hình không phình
        pk.save_game(pk.fit(im, side), name)
    print("Trong Unity: menu \"PokiClash/Dựng lại danh mục ảnh\". Nối ảnh vào màn Máy bi: việc code (xem THAM_KHAO_MAY_BI.md).")


# ---------- bóng đèn vòm ----------

CAB_PNG = ROOT / "Assets" / "03 Art" / "Pachinko" / "pk_than_may.png"
BULBS_JSON = REFS / "den_vom.json"


def bulbs():
    """dò bóng đèn vàng trên vòm tủ (pk_than_may.png): khối vàng tròn cỡ đều ở dải trên cùng, bỏ vệt sáp và ngôi sao.
    Ghi refs/den_vom.json (tâm theo px ảnh tủ, đường kính ngoài kể viền mực, tỉ lệ hình tròn trong ảnh pk_den_*) cho menu Unity
    "PokiClash/Prefab/Máy bi: nút tròn, viên cược, đèn vòm" đặt đèn rời lên đúng bóng vẽ sẵn."""
    im = Image.open(CAB_PNG).convert("RGBA")
    a = np.array(im).astype(int)
    H, W = a.shape[:2]
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    yellow = (al > 200) & (r > 220) & (g > 170) & (g < 225) & (b < 120)
    yellow[int(H * 0.16):] = False
    lab, _ = ndimage.label(yellow)
    found = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i
        h, w = m.shape
        if m.sum() < 145 or (w + h) / 4 > 10 or not 0.7 < w / h < 1.4:
            continue
        ys, xs = np.where(m)
        found.append((round(xs.mean() + sl[1].start, 1), round(ys.mean() + sl[0].start, 1), (w + h) / 2))
    found.sort()
    if len(found) < 6:
        sys.exit(f"Chỉ thấy {len(found)} bóng đèn trên vòm, kiểm lại ngưỡng màu")
    yellow_d = float(np.median([d for _, _, d in found]))
    # tỉ lệ hình tròn (kể viền) trong khung ảnh pk_den_tat (chung khung với bản sáng có vạch)
    den = np.array(Image.open(CAB_PNG.parent / "pk_den_tat.png").convert("RGBA"))[..., 3] > 8
    ys, xs = np.where(den)
    fill = (xs.max() - xs.min() + 1) / den.shape[1]
    data = {"image": [W, H], "bulbs": [[x, y] for x, y, _ in found], "outer_d": round(yellow_d + 6, 1), "sprite_fill": round(float(fill), 3)}
    BULBS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(found)} bóng đèn, đường kính ngoài {data['outer_d']} px, ghi {BULBS_JSON}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="*", default=None, help="duyệt ảnh GPT: nut|trang_thai|hieu_ung_2 [ảnh]")
    ap.add_argument("--den", action="store_true", help="dò bóng đèn vòm trên ảnh tủ, ghi refs/den_vom.json")
    args = ap.parse_args()
    if args.den:
        bulbs()
        return
    if args.duyet is not None:
        if not args.duyet or args.duyet[0] not in NAMES:
            sys.exit(f"Cần loại: {', '.join(NAMES)}")
        kind = args.duyet[0]
        src = Path(args.duyet[1]) if len(args.duyet) > 1 else pk.latest(f"{kind}*.png")
        if not src or not src.exists():
            sys.exit(f"Chưa có ảnh {kind} trong {INBOX}")
        print(f"Duyệt {src}")
        approve(kind, src)
        return
    cab = pk.cabinet_ref()
    if not cab:
        sys.exit("Chưa có thân máy đã duyệt (tai_ve/than_may.png): dựng lượt 1 của build.py trước")
    if SHOT_SRC.exists():
        im = Image.open(SHOT_SRC).convert("RGB")
        im.resize((540, 960), Image.LANCZOS).save(SHOT, optimize=True)
    elif not SHOT.exists():
        sys.exit(f"Thiếu ảnh chụp màn Máy bi ({SHOT_SRC})")
    PACK.mkdir(parents=True, exist_ok=True)
    turns = [turn_buttons(cab), turn_states(cab), turn_fx(cab)]
    for t in turns:
        t["file"].write_text("\n".join(t["lines"]) + "\n", encoding="utf-8")
        print(f"lượt {t['n']} {t['vi']}: {t['file']}; GPT lưu {t['out']}")
    guide(turns)
    print(f"Hướng dẫn: {PACK / 'HUONG_DAN.md'}")


if __name__ == "__main__":
    main()
