# Gói gửi GPT: thân máy bi (tủ máy vẽ tay có đầu máy chứa thanh kinh nghiệm). Xem ArtGen/Pachinko/PROMPTS.md.
# Học từ máy tham khảo (bản đục ở D:\CrittersRipper, chỉ học bố cục, không đính ảnh của nó): tủ đứng có đỉnh vòm viền bóng đèn,
# đầu máy là một bảng chứa thanh cấp (vòng cấp bên trái, thanh dài, số), mặt chơi ở giữa, đế máy dưới cùng.
# Khung máy trong game: khối máy 1080 × 1530 (Screens/Machine, "khoi_may", gốc trên trái), mặt máy "May" ở x 144,4, y 100,
# cỡ 791,2 × 1169,6 (bàn 460 × 680 nhân 1,72); thanh kinh nghiệm "thanh_kinh_nghiem" ở x 144, y 4, cỡ 696 × 92 (vòng cấp cao 97,
# thanh từ x 62, cao 50); cột cược bên trái tới x 134, khay rương bên phải từ x 944. Tủ máy chiếm x 122..958, y -80..1292.
# Ghi: refs/bo_cuc_than_may.png (ảnh bố cục 1024 × 1536 gửi GPT), refs/bo_cuc_than_may.json (khung từng phần theo px ảnh và
# px khối máy, để cắt ảnh GPT và đặt vào game), gói gui_gpt/than_may/ (luot_1_than_may.txt, HUONG_DAN.md).
# GPT lưu ảnh vào tai_ve/than_may.png.
# Lượt 2-4 (dựng khi đã có thân máy duyệt, lấy thân máy làm ảnh mẫu nét): luot_2_bo_phan.txt (12 bộ phận mặt máy, lưới 4 × 3),
# luot_3_hieu_ung.txt (6 hình hiệu ứng game đang dùng, lưới 3 × 2), luot_4_ruong.txt (6 rương gỗ, bạc, vàng đóng và mở, lưới 3 × 2).
# Ảnh mẫu thêm: refs/mat_may_danh_so.png (ảnh chụp máy trong game, đánh số từng bộ phận theo ô lưới, vẽ từ refs/mat_may_hien_tai.png),
# refs/hieu_ung_tam.png (6 hình hiệu ứng tạm trong Assets/03 Art/Fallback), refs/ruong_hien_tai.png (hộp mở rương trong game).
# Chạy: py -3 -I ArtGen/Pachinko/build.py
# Duyệt ảnh GPT đã lưu: py -3 -I ArtGen/Pachinko/build.py --duyet [ảnh] (mặc định ảnh mới nhất tai_ve/than_may*.png):
#   lọc hạt mờ lơ lửng ngoài viền, cắt sát, thu về đúng cỡ hiện trên màn (1 px khối máy), ghi Assets/03 Art/Pachinko/pk_than_may.png;
#   đo rãnh thanh, hốc vòng cấp, hốc nút tỉ lệ, mặt chơi trong ảnh, ghi refs/than_may_da_duyet.json (px khối máy) cho menu
#   Unity "PokiClash/Prefab/Máy bi: thân máy vẽ tay" đặt thân máy và dời thanh kinh nghiệm, nút tỉ lệ vào đúng hốc.
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/Pachinko
ART = HERE.parent
REFS = HERE / "refs"
PACK = HERE / "gui_gpt" / "than_may"
INBOX = HERE / "tai_ve"
STYLE = ART / "Islands" / "refs" / "world_style.png"
BOARD = ART / "StyleRefs" / "R2b_MayBi_KetVang.png"
SCREEN = REFS / "man_may_bi_hien_tai.png"  # ảnh chụp màn Máy bi trong Unity (thu nhỏ 540 × 960)
LAYOUT = REFS / "bo_cuc_than_may.png"
OUT = INBOX / "than_may.png"
APPROVED = REFS / "than_may_da_duyet.json"
GRID43 = ART / "guides" / "G_Sheet4x3.png"
GRID32 = ART / "guides" / "G_Sheet3x2.png"
BOARD_SHOT = REFS / "mat_may_hien_tai.png"  # ảnh chụp thân máy và mặt máy trong game, 1 px = 1 px khối máy, gốc ở (110, -100)
BOARD_SHOT_ORIGIN = (110, -100)
BOARD_NUM = REFS / "mat_may_danh_so.png"
FX_TMP = REFS / "hieu_ung_tam.png"
CHEST_SHOT = REFS / "ruong_hien_tai.png"
FALLBACK = HERE.parent.parent / "Assets" / "03 Art" / "Fallback"
FX_NAMES = ["fx_glow", "fx_sparkle", "fx_ring", "fx_star", "fx_streak", "fx_puff"]
GAME_ART = HERE.parent.parent / "Assets" / "03 Art" / "Pachinko" / "pk_than_may.png"

W, H = 1024, 1536
# tủ máy theo px khối máy (x0, y0, x1, y1)
CAB = (122, -80, 958, 1292)
BOARD_RECT = (144.4, 100, 935.6, 1269.6)  # mặt máy (game vẽ bàn, đinh, ô lên đây)
BADGE = (192, 50, 97)  # tâm x, y, đường kính vòng cấp
BAR = (206, 25, 840, 75)  # rãnh thanh EXP
INFO = (896, 50, 68)  # hốc nút tỉ lệ (sau này nút "i" tròn nằm đây)
CAB_H_IMG = 1480  # tủ cao bấy nhiêu px ảnh, chừa mép trên dưới

S = CAB_H_IMG / (CAB[3] - CAB[1])
OX = (W - (CAB[2] - CAB[0]) * S) / 2
OY = (H - CAB_H_IMG) / 2

INK = (43, 33, 24)
OUTSIDE = (214, 214, 214)
FRAME = (222, 140, 92)
CREST = (232, 170, 110)
WINDOW = (251, 244, 226)
GROOVE = (150, 110, 200)
BADGE_C = (240, 127, 166)
INFO_C = (74, 144, 217)
BULB = (247, 201, 72)
BASE = (190, 110, 70)


def px(x, y):
    """px khối máy -> px ảnh"""
    return OX + (x - CAB[0]) * S, OY + (y - CAB[1]) * S


def box(x0, y0, x1, y1):
    a, b = px(x0, y0)
    c, d = px(x1, y1)
    return [round(a), round(b), round(c), round(d)]


def circle(cx, cy, dia):
    return box(cx - dia / 2, cy - dia / 2, cx + dia / 2, cy + dia / 2)


def draw_layout():
    im = Image.new("RGB", (W, H), OUTSIDE)
    d = ImageDraw.Draw(im)
    # caro nhạt ở ngoài tủ: vùng trong suốt
    for y in range(0, H, 32):
        for x in range(0, W, 32):
            if (x // 32 + y // 32) % 2:
                d.rectangle([x, y, x + 31, y + 31], fill=(232, 232, 232))
    cab = box(*CAB)
    crest_h = 80 * S
    # thân tủ: chữ nhật bo góc dưới, đỉnh vòm (vòm cao bằng dải trên cùng 80 px khối máy)
    d.rounded_rectangle([cab[0], cab[1] + crest_h, cab[2], cab[3]], radius=round(28 * S), fill=FRAME, outline=INK, width=4)
    d.pieslice([cab[0], cab[1], cab[2], cab[1] + crest_h * 2], 180, 360, fill=CREST, outline=INK, width=4)
    d.rectangle([cab[0] + 3, cab[1] + crest_h - 2, cab[2] - 3, cab[1] + crest_h + 6], fill=FRAME)
    # bóng đèn dọc mép vòm
    cx, cy = (cab[0] + cab[2]) / 2, cab[1] + crest_h
    rx, ry = (cab[2] - cab[0]) / 2 - 16, crest_h - 14
    for i in range(15):
        a = math.pi + math.pi * (i + 0.5) / 15
        bx, by = cx + rx * math.cos(a), cy + ry * math.sin(a)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=BULB, outline=INK, width=2)
    # biểu tượng bi hồng giữa đỉnh vòm
    d.ellipse([cx - 26, cab[1] + 18, cx + 26, cab[1] + 70], fill=BADGE_C, outline=INK, width=3)
    # đầu máy: rãnh thanh, vòng cấp, hốc nút
    d.rounded_rectangle(box(*BAR), radius=round(25 * S), fill=GROOVE, outline=INK, width=3)
    d.ellipse(circle(*BADGE), fill=BADGE_C, outline=INK, width=4)
    d.ellipse(circle(*INFO), fill=INFO_C, outline=INK, width=4)
    # mặt chơi: trống
    d.rectangle(box(*BOARD_RECT), fill=WINDOW, outline=INK, width=4)
    # đế máy: hai chân dưới đáy
    fy0 = px(0, CAB[3])[1]
    for fx in (CAB[0] + 90, CAB[2] - 190):
        a, _ = px(fx, 0)
        c, _ = px(fx + 100, 0)
        d.rounded_rectangle([a, fy0 - 10, c, fy0 + 22], radius=8, fill=BASE, outline=INK, width=3)
    LAYOUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(LAYOUT, optimize=True)
    info = {
        "image": [W, H], "scale_img_per_block_px": S, "block_origin_in_image": [OX - CAB[0] * S, OY - CAB[1] * S],
        "cabinet_block": CAB, "cabinet_img": cab,
        "board_block": BOARD_RECT, "board_img": box(*BOARD_RECT),
        "bar_block": BAR, "bar_img": box(*BAR),
        "badge_block": BADGE, "badge_img": circle(*BADGE),
        "info_block": INFO, "info_img": circle(*INFO),
    }
    LAYOUT.with_suffix(".json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    return info


def save_rule(p):
    return (f"SAVE: save the finished image as a 1024 x 1536 PNG with a TRANSPARENT background to\n{p}\nCreate the folder if it is "
            f"missing. If that file already exists, save it as {p.stem}_2.png, {p.stem}_3.png … in the same folder instead. "
            f"Do not change, move or delete any other file.")


def refs_list():
    refs = [
        (STYLE, "1024 x 1536", "style reference only: the game's approved hand-drawn world map (wobbly dark-brown ink outlines, "
                               "colour-pencil and crayon hatching on cream paper, chunky cute doodles); copy its rendering, ignore its content"),
        (LAYOUT, "1024 x 1536", "the layout plan of the image you draw now: the exact outline and position of every part of the cabinet, "
                                "colour-coded; follow it exactly"),
        (BOARD, "920 x 1360", "what the game itself draws INSIDE the play window: pegs, red mushroom bumpers, two small cups, a golden "
                              "vault and eleven prize slots; shown only so you understand the machine; do NOT draw any of it"),
    ]
    if SCREEN.exists():
        refs.append((SCREEN, "540 x 960", "a screenshot of the machine screen in the game today, with the plain placeholder frame your "
                                          "cabinet replaces, the level bar on top, the bet buttons on the left, the chest tray on the right "
                                          "and the drop buttons below; shown only so you understand the space around the cabinet"))
    return refs


def prompt(info):
    refs = refs_list()
    L = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as "
         "described under SAVE. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    for i, (p, size, what) in enumerate(refs, 1):
        L.append(f"image {i} = {p} ({size}): {what}")
    L += ["", save_rule(OUT), ""]
    b = info["board_img"]
    bar = info["bar_img"]
    bd = info["badge_img"]
    inf = info["info_img"]
    cab = info["cabinet_img"]
    L += [
        "WHAT THIS IS: the cabinet of the ball-drop machine (a vertical pachinko) of a cute hand-drawn mobile game. The player taps to "
        "drop balls from the top; they bounce down through pegs into prize slots at the bottom. The game draws the pegs, the slots, the "
        "balls and every number itself, inside the play window and on the head panel. You draw only the cabinet around them: a chunky "
        "toy-like fairground cabinet seen straight from the front.",
        "",
        f"LAYOUT (image 2, follow it exactly, same pixels): the cabinet fills x {cab[0]}..{cab[2]}, y {cab[1]}..{cab[3]} of the image; "
        "everything outside it is transparent. Image 2 is only a colour-coded plan: grey checker = transparent, orange = cabinet body, "
        "light orange half-disc = arched crest, yellow dots = light bulbs, pink circle on the crest = ball emblem, purple rounded bar = "
        "level-bar groove, pink circle = level badge socket, blue circle = small round button socket, cream rectangle = play window, "
        "brown blocks = feet. Do not copy its flat colours or its straight lines; draw it by hand.",
        "",
        "PARTS:",
        f"- PLAY WINDOW x {b[0]}..{b[2]}, y {b[1]}..{b[3]}: one flat plain cream #FBF4E2 rectangle, completely EMPTY: no pegs, no dots, "
        "no slots, no lines, no hatching, no pattern, no glass reflections. Its edge is a clean ink line. The game covers it with the "
        "board of image 3, so it must stay flat and plain, and exactly this size.",
        f"- FRAME around the window: a thin warm wooden frame (about {round(22 * info['scale_img_per_block_px'])} px on the left, right "
        "and bottom), painted red-orange with a cream inner trim line, a few doodled rivets or little stars. Keep the sides this thin: "
        "the bet buttons and the chest tray of the game sit right next to them.",
        f"- HEAD PANEL above the window (y {cab[1] + round(80 * info['scale_img_per_block_px'])}..{b[1]}): a sturdy wooden plate in the "
        "same red-orange with a cream inset, like the scoreboard of a fairground machine. In it, three EMPTY sockets where the game "
        "places its own pieces:",
        f"  - LEVEL-BAR GROOVE x {bar[0]}..{bar[2]}, y {bar[1]}..{bar[3]}: a long rounded slot, sunk into the panel, plain dark "
        "brown-purple #4A3A5A inside with an ink rim; no bar, no fill, no marks, no numbers in it (the game draws the experience bar there);",
        f"  - LEVEL BADGE SOCKET at the left end of the groove, circle x {bd[0]}..{bd[2]}, y {bd[1]}..{bd[3]}: a round cream plate "
        "with a thick golden ring, empty in the middle (the game writes the level number there);",
        f"  - BUTTON SOCKET at the right end of the panel, circle x {inf[0]}..{inf[2]}, y {inf[1]}..{inf[3]}: a small round cream "
        "plate with a teal ring, empty (the game puts a round info button there).",
        f"- ARCHED CREST on top (y {cab[1]}..{cab[1] + round(80 * info['scale_img_per_block_px'])}): a half-round wooden arch in light "
        "orange with a row of about fifteen round yellow light bulbs along its edge (each bulb a small yellow circle with an ink "
        "outline and a tiny white dot; no glow, no halo, no light rays), and in the middle a round pink ball emblem with a white band, "
        "like the ball of the game. A couple of small doodled stars and a teal ribbon line along the arch.",
        "- FEET: two short chunky wooden feet under the bottom edge, as in image 2.",
        "",
        "COLOURS: warm red-orange #E8553F and orange #F39A2D wood, cream #FBF4E2 trims, yellow #F7C948 bulbs, teal #3FB8A9 accents, "
        "pink #F07FA6 emblem, dark-brown ink #2B2118 outlines. Cheerful and toy-like, readable at small size on a phone.",
        "",
        "STYLE (image 1): the hand-drawn storybook look of this game: slightly wobbly dark-brown ink outlines (about 5 px), flat warm "
        "colours, light colour-pencil and crayon hatching for texture, cream paper feel. Drawn neatly by a professional illustrator, "
        "not scribbly. No glossy highlights, no gradients, no 3D render, no airbrush, no metal shine.",
        "",
        "NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or background.",
        "Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed.",
        "",
        "AVOID: text, letters, numbers, labels, characters, creatures, pegs or balls inside the window, a bar inside the groove, a "
        "background, a floor, a table, glow, light rays, sparkles around the cabinet.",
        "",
        f"Remember: transparent background, cabinet exactly on the plan of image 2, save the image to {OUT}",
    ]
    return refs, L


def guide(refs, info, later):
    look = {
        STYLE: "bản đồ thế giới của game: bốn đảo vẽ tay, viền mực nâu, tô sáp màu (chỉ để học nét)",
        LAYOUT: "ảnh bố cục tủ máy: nền caro xám là trong suốt; thân cam, vòm cam nhạt có chấm vàng (bóng đèn) và tròn hồng (bi); "
                "rãnh tím là chỗ thanh kinh nghiệm, tròn hồng bên trái là vòng cấp, tròn xanh bên phải là nút tỉ lệ; chữ nhật kem "
                "là mặt chơi; hai khối nâu là chân",
        BOARD: "mặt máy game tự vẽ (đinh, nấm đỏ, cốc bạc, két vàng, 11 ô), chỉ để GPT hiểu, không vẽ lại",
        SCREEN: "ảnh chụp màn Máy bi trong game bây giờ (có thanh kinh nghiệm trên đầu máy, cột cược, khay rương, nút thả)",
    }
    g = ["# Gói gửi GPT: máy bi (thân máy, bộ phận, hiệu ứng, rương)", "",
         f"Sinh bằng `{HERE / 'build.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè).", "",
         "Thân máy là tủ máy vẽ tay bao quanh mặt máy, có đầu máy chứa thanh kinh nghiệm (vòng cấp, thanh EXP, nút tỉ lệ) và đỉnh "
         "vòm có bóng đèn. Game vẫn tự vẽ đinh, ô, bi, số trên ô (đổi theo mức cược) và thanh kinh nghiệm; ảnh chỉ là cái tủ.", "",
         "Bố cục học từ máy tham khảo: tủ đứng đỉnh vòm viền bóng đèn, đầu máy là bảng chứa thanh cấp, mặt chơi ở giữa. "
         "Không đính ảnh của game đó cho GPT, không nhắc tên game.", "",
         "**Chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh.", "",
         "## Lượt 1: thân máy", "",
         f"File prompt: `{PACK / 'luot_1_than_may.txt'}`. GPT lưu `{OUT}` (trùng tên thì thêm `_2`, `_3`).", "",
         "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    for i, (p, size, _) in enumerate(refs, 1):
        g.append(f"| {i} | `{p}` | {look[p]} ({size.replace(' x ', ' × ')}) |")
    cab = info["cabinet_img"]
    b = info["board_img"]
    g += ["",
          "Soi:",
          f"- ảnh dọc 1024 × 1536, nền trong suốt; tủ nằm trong x {cab[0]}..{cab[2]}, y {cab[1]}..{cab[3]}, đúng chỗ như ảnh bố cục;",
          f"- mặt chơi x {b[0]}..{b[2]}, y {b[1]}..{b[3]} là một chữ nhật kem phẳng, trống trơn (không đinh, không chấm, không ô);",
          "- rãnh thanh kinh nghiệm trống (không có thanh, không số), vòng cấp và hốc nút trống ở giữa;",
          "- khung hai bên mỏng (khoảng 24 px ảnh), vòm có hàng bóng đèn vàng và bi hồng ở giữa, hai chân dưới đáy;",
          "- không chữ, không số, không bóng đổ, không quầng sáng.",
          "",
          "Câu sửa nhanh (gửi kèm đường dẫn file prompt):",
          "- `Same cabinet, but the play window must be completely empty flat cream, exactly the rectangle of image 2.`",
          "- `Same cabinet, but the side frame thinner, exactly as in image 2.`",
          "- `Same cabinet, but the background must be transparent, no floor, no shadow.`",
          "- `Same cabinet, but leave the groove, the badge socket and the button socket empty, no numbers, no bar.`",
          "",
          "Xong thì nhắn Claude \"duyệt thân máy\". Tự làm cũng được:",
          f"1. `py -3 -I {HERE / 'build.py'} --duyet`: lọc mép, cắt sát, thu về đúng cỡ hiện trên màn, ghi `{GAME_ART}`; đo rãnh thanh, "
          f"hai hốc tròn, mặt chơi, ghi `{APPROVED}`;",
          "2. trong Unity, menu `PokiClash/Prefab/Máy bi: thân máy vẽ tay`: đặt thân máy sau mặt máy, tắt khung giấy tạm, dời thanh "
          "kinh nghiệm vào rãnh, nút tỉ lệ thành chữ \"i\" trong hốc tròn bên phải, nhích cột cược và khay rương khỏi viền tủ.", "",
          ]
    if not later:
        g += ["## Lượt sau", "", "Bộ phận mặt máy, hiệu ứng, rương: dựng file prompt sau khi có thân máy (lấy thân máy làm ảnh mẫu nét)."]
    for t in later:
        g += [f"## Lượt {t['n']}: {t['vi']}", "",
              f"File prompt: `{t['file']}`. GPT lưu `{t['out']}` (trùng tên thì thêm `_2`, `_3`).", "", t["what_vi"], "",
              "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        for i, (p, size, _, look_vi) in enumerate(t["refs"], 1):
            g.append(f"| {i} | `{p}` | {look_vi} ({size.replace(' x ', ' × ')}) |")
        g += ["", "Soi:"] + [f"- {c}" for c in t["checks"]] + ["", "Câu sửa nhanh (gửi kèm đường dẫn file prompt):"]
        g += [f"- `{q}`" for q in t["fixes"]] + ["", t["after_vi"], ""]
    (PACK / "HUONG_DAN.md").write_text("\n".join(g) + "\n", encoding="utf-8")


# ---------- lượt 2-4: bộ phận, hiệu ứng, rương ----------

K_BOARD = 1.72  # bàn 460 × 680 hiện ở cỡ 1,72 lần trong khối máy


def font(size):
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except OSError:
        return ImageFont.load_default()


FONT = font(30)
SHEET_RULE = ("SHEET: a 1536 x 1024 PNG with a TRANSPARENT background, one item per numbered cell of image 2, in the order of the "
              "numbers. Centre each item inside the grey inner box of its cell and let it fill most of that box; it must never touch "
              "the cell edge or another item. Do not draw the grid, the magenta lines, the grey boxes or the numbers.")
STYLE_CAB = ("STYLE: exactly the rendering of image 1, the approved cabinet of this machine: slightly wobbly dark-brown ink outlines "
             "#2B2118, flat warm colours, colour-pencil and crayon hatching for texture, cream paper feel. Drawn neatly by a "
             "professional illustrator, not scribbly. No glossy highlights, no gradients, no 3D render, no airbrush, no metal shine.")
NO_SHADOW = ["NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the items.",
             "Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed."]
HEAD = ("Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as "
        "described under SAVE. Do not reply with text only.")


def sheet_save(p):
    return (f"SAVE: save the finished sheet as a 1536 x 1024 PNG with a TRANSPARENT background to\n{p}\nCreate the folder if it is "
            f"missing. If that file already exists, save it as {p.stem}_2.png, {p.stem}_3.png … in the same folder instead. "
            f"Do not change, move or delete any other file.")


def cabinet_ref():
    src = latest("than_may*.png")
    return (src, "1024 x 1536", "the approved cabinet of this machine (transparent background): copy its exact drawing style, "
                                "ink weight, crayon texture and colours",
            "thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu") if src else None


def board_point(u, v):
    """toạ độ bàn (460 × 680) -> px trong ảnh chụp mặt máy"""
    return 144.4 + u * K_BOARD - BOARD_SHOT_ORIGIN[0], 100 + v * K_BOARD - BOARD_SHOT_ORIGIN[1]


def draw_board_numbers():
    """đánh số từng bộ phận lên ảnh chụp mặt máy (số trùng ô lưới của lượt 2)"""
    if not BOARD_SHOT.exists():
        return False
    im = Image.open(BOARD_SHOT).convert("RGB")
    a = np.array(im).astype(int)
    # máng mây: chùm điểm trắng tinh trong dải ray trên cùng
    y0, y1 = (round(board_point(0, v)[1]) for v in (4, 46))
    white = (a[y0:y1] >= 250).all(-1)
    xs = np.where(white)[1]
    cloud_x = (xs.mean() if len(xs) else board_point(230, 0)[0])
    cloud_u = (cloud_x + BOARD_SHOT_ORIGIN[0] - 144.4) / K_BOARD
    pieces = [  # số, điểm trên bàn (u, v), lệch của nhãn (px)
        (1, (137.5, 120), (40, -46)),
        (2, (114.4, 246), (-56, -44)),
        (3, (14, 162), (58, 30)),
        (4, (123.25, 574), (0, -70)),
        (5, (114.4, 420), (-58, 40)),
        (6, (193.6, 481), (-84, -36)),
        (7, (230, 528), (0, 62)),
        (8, (cloud_u, 26), (76, -14)),
        (9, (cloud_u, 40), (76, 34)),
        (10, (34, 87), (56, 46)),
        (11, (120, 24), (-30, 50)),
        (12, (200, 506), (150, 44)),
    ]
    d = ImageDraw.Draw(im)
    pink = (230, 0, 200)
    for n, (u, v), (ox, oy) in pieces:
        x, y = board_point(u, v)
        lx, ly = x + ox, y + oy
        d.line([x, y, lx, ly], fill=pink, width=4)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=pink, width=4)
        d.ellipse([lx - 22, ly - 22, lx + 22, ly + 22], fill=pink, outline=(255, 255, 255), width=3)
        d.text((lx, ly), str(n), fill=(255, 255, 255), font=FONT, anchor="mm")
    im.save(BOARD_NUM, optimize=True)
    return True


def draw_fx_placeholders():
    """6 hình hiệu ứng tạm đang dùng, xếp theo lưới 3 × 2 trên nền tối (hình gần trắng nên cần nền tối để thấy)"""
    sheet = Image.new("RGB", (1536, 1024), (58, 52, 70))
    d = ImageDraw.Draw(sheet)
    big = font(56)
    for i, name in enumerate(FX_NAMES):
        p = FALLBACK / f"{name}.png"
        cx, cy = (i % 3) * 512, (i // 3) * 512
        d.rectangle([cx + 4, cy + 4, cx + 507, cy + 507], outline=(230, 0, 200), width=4)
        d.text((cx + 20, cy + 12), str(i + 1), fill=(230, 0, 200), font=big)
        if p.exists():
            im = Image.open(p).convert("RGBA")
            k = min(360 / im.width, 360 / im.height)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
            sheet.paste(im, (cx + (512 - im.width) // 2, cy + (512 - im.height) // 2), im)
    sheet.save(FX_TMP, optimize=True)


def turn_parts(cab):
    out = INBOX / "bo_phan.png"
    refs = [cab,
            (GRID43, "1536 x 1024", "the numbered 4 x 3 grid of the sheet you draw: one item per cell, inside the grey inner box",
             "lưới 4 × 3 đánh số (ô hồng, khung xám là vùng an toàn)"),
            (BOARD_NUM, f"{Image.open(BOARD_NUM).width} x {Image.open(BOARD_NUM).height}",
             "the machine in the game today with the plain placeholder parts drawn by code; each numbered pink label points at the "
             "part that goes into the cell with the same number; shown so you understand what each part is and how big it is",
             "ảnh chụp máy trong game, nhãn hồng đánh số chỉ vào bộ phận tạm ứng với từng ô")]
    L = [HEAD, "", "REFERENCE IMAGES (open each file from its full path):"]
    L += [f"image {i} = {p} ({size}): {what}" for i, (p, size, what, _) in enumerate(refs, 1)]
    L += ["", sheet_save(out), "",
          "WHAT THIS IS: the separate parts of the board of the ball-drop machine (a vertical pachinko) whose cabinet is image 1. "
          "The game places every part at the exact spot of its physics and scales it to the size given below (on a phone), so draw "
          "each part alone, seen straight from the front, simple and bold enough to read at that small size. Outlines must be thick: "
          "about one tenth of the item's width for the small round parts.",
          "", SHEET_RULE, "",
          "CELLS (image 3 shows where each part sits):",
          "1 PEG (shown 17 px): one small round peg head seen from the front: a dark warm-grey circle with a thick ink outline and "
          "one small cream dot near its top left. Round, no stem, nothing around it.",
          "2 MUSHROOM BUMPER (shown 55 px): a round red mushroom cap seen from straight above: red #E8553F with five round white "
          "spots, a cream ring around the edge, thick ink outline. Round.",
          "3 WALL BUMP (shown 34 px): a round wooden knob, warm brown with a darker ring and a lighter centre, thick ink outline. "
          "Draw the full circle; the game hides half of it inside the side wall.",
          "4 SLOT POST (shown 12 x 180 px): one thin upright wooden post that separates two prize slots: a straight vertical stick, "
          "warm brown, with a round knob on its top end and a flat bottom end. About 1 : 12 width to height; as tall as the inner box.",
          "5 SILVER CUP (shown 40 x 28 px): a small catch cup seen from the front: a trapezoid bucket wider at the top, light "
          "silver-grey with a darker rim, thick ink outline, empty inside (the game puts a tiny chest in it). About 3 : 2.",
          "6 VAULT ROOF PLANK (shown 90 x 11 px): one thick golden plank lying horizontally with rounded ends, yellow-gold #F7C948 "
          "with a darker gold edge and two small rivets. About 8 : 1. The game turns it to a slant and mirrors it for the other side.",
          "7 VAULT FLOOR (shown 165 x 26 px): a shallow V-shaped golden tray: two golden planks meeting at a low point in the "
          "middle, with a small round golden knob on each upper end. About 6 : 1.",
          "8 CLOUD LAUNCHER (shown 110 x 53 px): a cute small white cloud seen from the front, with two dot eyes and a tiny smile, "
          "a flat bottom where the ball hangs, thick ink outline, pale grey hatching. About 2 : 1.",
          "9 BALL (shown 31 px): a round ball with one thin band across its middle, drawn ONLY in white and very light grey with a "
          "thick ink outline and one small white dot (the game tints it pink, blue or gold by the bet). Round.",
          "10 SHOULDER PLANK (shown 90 x 10 px): a short straight wooden plank lying horizontally with rounded ends, warm brown "
          "with a darker edge. About 9 : 1. The game turns it to a slant at the top corners of the board.",
          "11 LAUNCHER RAIL (shown 760 x 8 px): a long thin dark wooden rail lying horizontally with a small round cap at each end. "
          "Very long and thin, about 25 : 1, across the whole inner box.",
          "12 VAULT PLATE (shown 165 x 75 px): a flat pale-golden plate shaped like a wide hexagon (the backing behind the golden "
          "vault), soft light yellow #FFE9A8 with light hatching and a thin darker gold edge. About 2.2 : 1.",
          "", STYLE_CAB, "", *NO_SHADOW, "",
          "AVOID: text, letters, numbers, labels, characters, faces except the cloud's, a background, a floor, a board, extra parts, "
          "two parts in one cell.",
          "", f"Remember: transparent background, one part per cell in the order 1 to 12, save the sheet to {out}"]
    return dict(n=2, vi="bộ phận mặt máy", file=PACK / "luot_2_bo_phan.txt", out=out, refs=refs, lines=L,
                what_vi="12 bộ phận thay hình tạm vẽ bằng code trên mặt máy: đinh, nấm, u lồi tường, cọc vách ô, cốc bạc, mái két, "
                        "đáy két, máng mây, bi (trắng xám, game tô màu theo cược), ván vai, ray máng thả, tấm nền két.",
                checks=["lưới 1536 × 1024, nền trong suốt, mỗi ô một món đúng số, không chạm mép ô;",
                        "món nhỏ (đinh, bi, u lồi) viền mực dày, đơn giản, đọc được khi thu còn 17–34 px;",
                        "cọc vách ô đứng dọc, mái két, ván vai, ray nằm ngang (game tự xoay);",
                        "bi chỉ trắng và xám nhạt; máng mây có mắt;",
                        "không chữ, không số, không bóng đổ."],
                fixes=["Same sheet, but every part simpler and bolder, with thicker ink outlines.",
                       "Same sheet, but the ball only white and light grey, no colour.",
                       "Same sheet, but each part fully inside the grey box of its cell, not touching the cell edge."],
                after_vi=f"Xong thì nhắn Claude \"duyệt bộ phận\". Tự làm: `py -3 -I {HERE / 'build.py'} --duyet bo_phan` (cắt ô, ghép "
                         "mặt máy tĩnh `Baked/Machine/may_tinh.png` theo đúng toạ độ vật lý, ghi `pk_bumper`, `pk_may_tha`, `pk_bi`), rồi "
                         "trong Unity chạy menu `PokiClash/Dựng lại danh mục ảnh` và `PokiClash/Prefab/Máy bi: ảnh bộ phận`.")


def turn_fx(cab):
    out = INBOX / "hieu_ung.png"
    refs = [cab,
            (GRID32, "1536 x 1024", "the numbered 3 x 2 grid of the sheet you draw: one effect per cell, inside the grey inner box",
             "lưới 3 × 2 đánh số"),
            (FX_TMP, "1536 x 1024", "the six plain placeholder effect shapes the game uses today, white on a dark background, in the "
                                    "same cell order; draw a hand-made version of each shape",
             "6 hình hiệu ứng tạm game đang dùng (trắng trên nền tối), cùng thứ tự ô")]
    L = [HEAD, "", "REFERENCE IMAGES (open each file from its full path):"]
    L += [f"image {i} = {p} ({size}): {what}" for i, (p, size, what, _) in enumerate(refs, 1)]
    L += ["", sheet_save(out), "",
          "WHAT THIS IS: six small visual-effect sprites for the ball-drop machine of image 1 (sparkles when a ball hits a peg, rings "
          "when it lands in a slot, stars for treasure, a puff when a ball is dropped). The game scales, rotates, fades and TINTS "
          "them with many colours, so draw them in white and very pale grey only, soft and simple, with at most a thin ink outline.",
          "", SHEET_RULE, "",
          "CELLS (image 3 shows today's plain shapes in the same order):",
          "1 GLOW: a soft round glow: white in the middle fading smoothly to fully transparent at the edge; no outline, no rays.",
          "2 SPARKLE: a small four-pointed sparkle star with long thin points and a tiny round centre, white with a thin pale-grey "
          "edge; points straight up, down, left and right.",
          "3 RING: a thin round ring of light, hollow in the middle, white, its edges soft; the ring is about one tenth of its "
          "diameter thick.",
          "4 STAR: a chubby five-pointed star with rounded tips, white inside with a thin dark-brown ink outline and a little "
          "crayon hatching.",
          "5 STREAK: a soft tapered streak lying horizontally, like a motion trail: a bright rounded head on the RIGHT end, thinning "
          "and fading to nothing toward the LEFT; about 5 : 1 long, filling the width of the inner box.",
          "6 PUFF: a small round puff of cloud smoke made of four or five round bumps, white with light grey crayon hatching and a "
          "thin ink outline.",
          "", "COLOURS: only white, very pale grey and a little dark-brown ink #2B2118 for the outlines of 4 and 6. No other colour: "
              "the game tints every sprite.",
          "", STYLE_CAB.replace("No glossy highlights", "Glow and soft fading are allowed only for 1, 2, 3 and 5. No glossy "
                                                        "highlights"), "", *NO_SHADOW, "",
          "AVOID: text, letters, numbers, characters, a background, colours, sparkles outside the cells, two effects in one cell.",
          "", f"Remember: transparent background, white effects, one per cell in the order 1 to 6, save the sheet to {out}"]
    names = ", ".join(f"{i + 1} `{n}`" for i, n in enumerate(FX_NAMES))
    return dict(n=3, vi="hiệu ứng", file=PACK / "luot_3_hieu_ung.txt", out=out, refs=refs, lines=L,
                what_vi=f"6 hình hiệu ứng game đang dùng (hình tạm trong `Assets/03 Art/Fallback`): {names}. Game tự phóng, xoay, mờ, "
                        "tô màu nên GPT vẽ trắng.",
                checks=["lưới 1536 × 1024, nền trong suốt, mỗi ô một hình đúng thứ tự;",
                        "chỉ trắng và xám nhạt (sao và khói có viền mực mảnh); không màu khác;",
                        "quầng mờ dần về trong suốt ở mép; vòng rỗng giữa; vệt đầu sáng bên phải, đuôi mờ bên trái;",
                        "không chữ, không nền."],
                fixes=["Same sheet, but only white and very pale grey, no colour at all.",
                       "Same sheet, but the glow fades fully to transparent at its edge.",
                       "Same sheet, but each effect smaller and fully inside the grey box of its cell."],
                after_vi=f"Xong thì nhắn Claude \"duyệt hiệu ứng\". Tự làm: `py -3 -I {HERE / 'build.py'} --duyet hieu_ung` (cắt 6 ô, lưu "
                         "`Assets/03 Art/Pachinko/<tên>.png` cùng tên hình tạm), rồi trong Unity chạy menu `PokiClash/Dựng lại danh mục "
                         "ảnh`. Game tự dùng ảnh mới ở mọi chỗ đang dùng hình tạm đó (cả sao EXP bay lên thanh kinh nghiệm).")


def turn_chests(cab):
    out = INBOX / "ruong.png"
    refs = [cab,
            (GRID32, "1536 x 1024", "the numbered 3 x 2 grid of the sheet you draw: one chest per cell, inside the grey inner box",
             "lưới 3 × 2 đánh số"),
            (CHEST_SHOT, f"{Image.open(CHEST_SHOT).width} x {Image.open(CHEST_SHOT).height}",
             "the chest-opening box in the game today with the plain placeholder chest drawn by code (a golden chest); shown so "
             "you understand where the chests appear; do not copy its flat look",
             "hộp mở rương trong game hiện giờ, rương vàng vẽ tạm bằng code")]
    L = [HEAD, "", "REFERENCE IMAGES (open each file from its full path):"]
    L += [f"image {i} = {p} ({size}): {what}" for i, (p, size, what, _) in enumerate(refs, 1)]
    L += ["", sheet_save(out), "",
          "WHAT THIS IS: the treasure chests of the ball-drop machine of image 1. A ball that falls into a chest slot wins a wooden, "
          "silver or golden chest; the chest flies into a tray beside the machine, then opens in a box (image 3). The same drawing "
          "is shown small on the board (about 35 px), in the tray (about 90 px) and big in the opening box (about 200 px), so keep "
          "it chunky, simple and readable.",
          "", SHEET_RULE, "",
          "ALL SIX are the SAME chest shape and size, seen from the front and a little from above: a chunky box with a rounded lid, "
          "two metal bands, a round lock plate in the middle of the front. Only the material changes, and the open ones show the lid "
          "lifted back.",
          "1 WOODEN CHEST, closed: warm brown wooden planks with visible plank lines, dark iron bands, a small brass round lock.",
          "2 WOODEN CHEST, open: the same chest with the lid lifted back; inside a flat light-yellow fill with three or four doodled "
          "sparkle stars above it.",
          "3 SILVER CHEST, closed: pale blue-grey painted wood with shiny-looking silver bands drawn with hatching (no gloss), a "
          "round silver lock with a small blue gem.",
          "4 SILVER CHEST, open: the same silver chest open; inside a flat light-yellow fill with four or five doodled sparkle stars.",
          "5 GOLDEN CHEST, closed: golden-yellow #F7C948 body with orange-gold bands, a round lock with a red gem, a tiny crown "
          "doodle on the lid.",
          "6 GOLDEN CHEST, open: the same golden chest open, a few gold coins and doodled stars popping out above it, inside a flat "
          "light-yellow fill.",
          "", "LIGHT INSIDE: draw it as a flat light-yellow #FFF2A8 colour with a few doodled star shapes; no airbrush glow, no light "
              "rays, no halo (the game adds its own effects).",
          "", STYLE_CAB, "", *NO_SHADOW, "",
          "AVOID: text, letters, numbers, characters, a background, a floor, a table, glow halos, two chests in one cell.",
          "", f"Remember: transparent background, one chest per cell in the order 1 to 6, save the sheet to {out}"]
    return dict(n=4, vi="rương", file=PACK / "luot_4_ruong.txt", out=out, refs=refs, lines=L,
                what_vi="Rương gỗ, bạc, vàng (đóng và mở) cho ô rương trên mặt máy, khay \"Rương chờ\" và hộp mở rương; thay hình rương "
                        "vẽ bằng code (dùng chung với rương AFK).",
                checks=["lưới 1536 × 1024, nền trong suốt, mỗi ô một rương đúng thứ tự gỗ, gỗ mở, bạc, bạc mở, vàng, vàng mở;",
                        "sáu rương cùng dáng, cùng cỡ, chỉ khác chất liệu; rương mở thấy nắp lật ra sau;",
                        "trong rương mở tô vàng nhạt phẳng, không quầng sáng; không bóng đổ;",
                        "không chữ, không số."],
                fixes=["Same sheet, but all six chests exactly the same shape and size; only the material changes.",
                       "Same sheet, but no glow halo: the inside of the open chests is a flat light-yellow colour.",
                       "Same sheet, but each chest fully inside the grey box of its cell."],
                after_vi=f"Xong thì nhắn Claude \"duyệt rương\". Tự làm: `py -3 -I {HERE / 'build.py'} --duyet ruong` (cắt 6 ô thành "
                         "`pk_ruong_go`, `pk_ruong_bac`, `pk_ruong_vang`, bản mở thêm `_mo`), rồi trong Unity chạy menu `PokiClash/Dựng lại "
                         "danh mục ảnh`. Rương trên mặt máy, khay và hộp mở rương tự dùng ảnh mới (rương AFK màu riêng giữ hình vẽ tạm).")


def turns():
    """các lượt sau thân máy; chỉ dựng khi đã có thân máy (ảnh mẫu nét chung)"""
    cab = cabinet_ref()
    if not cab:
        return []
    out = []
    if draw_board_numbers():
        out.append(turn_parts(cab))
    draw_fx_placeholders()
    out.append(turn_fx(cab))
    if CHEST_SHOT.exists():
        out.append(turn_chests(cab))
    return out


def img_to_block(x, y):
    """px ảnh GPT -> px khối máy"""
    return (x - OX) / S + CAB[0], (y - OY) / S + CAB[1]


def bbox(mask):
    ys, xs = np.where(mask)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1) if len(xs) else None


def approve(src):
    im = Image.open(src).convert("RGBA")
    if im.size != (W, H):
        sys.exit(f"Ảnh {src} cỡ {im.size}, cần {W} x {H}")
    a = np.array(im)
    rgb, alpha = a[..., :3].astype(int), a[..., 3]
    # hạt mờ lơ lửng ngoài viền: giữ điểm mờ sát nét (khử răng cưa), bỏ điểm cách thân tủ hơn 3 px
    body = Image.fromarray(((alpha > 128) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
    keep = np.array(body) > 0
    a[..., 3] = np.where(keep, alpha, 0)
    print(f"  lọc {(~keep & (alpha > 0)).sum()} điểm mờ ngoài viền")
    # mặt chơi: vùng kem phẳng lớn
    cream = (np.abs(rgb - np.array([251, 244, 226])).sum(-1) < 30) & (alpha > 250)
    rows, cols = np.where(cream.sum(1) > W * 0.6)[0], np.where(cream.sum(0) > H * 0.6)[0]
    win = (int(cols.min()), int(rows.min()), int(cols.max()) + 1, int(rows.max()) + 1)
    # rãnh thanh: vùng tím sẫm ở đầu máy (trên mặt chơi)
    dark = (np.abs(rgb - np.array([100, 65, 95])).sum(-1) < 60) & (alpha > 250)
    dark[win[1] - 4:] = False
    grow = np.where(dark.sum(1) > W * 0.3)[0]
    if not len(grow):
        sys.exit("Không thấy rãnh thanh (vùng tím sẫm trên mặt chơi)")
    gcol = np.where(dark[grow].sum(0) > len(grow) * 0.5)[0]
    groove = (int(gcol.min()), int(grow.min()), int(gcol.max()) + 1, int(grow.max()) + 1)
    gy0 = groove[1] - 25
    # hốc vòng cấp: vòng vàng bên trái rãnh; hốc nút: vòng xanh ngọc bên phải rãnh (chỉ xét dải ngang đầu máy, dưới hàng bóng đèn)
    band = np.zeros_like(dark)
    band[gy0:win[1]] = True
    gold = (rgb[..., 0] > 200) & (rgb[..., 1] > 140) & (rgb[..., 2] < 110) & (alpha > 250) & band
    gold[:, groove[0] - 2:] = False
    teal = (rgb[..., 0] < 140) & (rgb[..., 1] > 140) & (rgb[..., 2] > 120) & (np.abs(rgb[..., 1] - rgb[..., 2]) < 70) & (alpha > 250) & band
    teal[:, :groove[2] + 2] = False
    def dense(m):
        # bỏ chấm lẻ: chỉ giữ hàng, cột có từ 4 điểm
        r, c = np.where(m.sum(1) >= 4)[0], np.where(m.sum(0) >= 4)[0]
        return (int(c.min()), int(r.min()), int(c.max()) + 1, int(r.max()) + 1) if len(r) and len(c) else None

    def ring(m):
        # vòng tròn (đáy có thể bị mặt chơi che): tâm ở hàng vòng rộng nhất, đường kính là bề rộng đó (px ảnh: cx, cy, d)
        r = dense(m)
        if not r:
            return None
        sub = m[r[1]:r[3], r[0]:r[2]]
        spans = [(np.where(row)[0].max() - np.where(row)[0].min() + 1) if row.any() else 0 for row in sub]
        best = max(spans)
        rows = [i for i, v in enumerate(spans) if v >= best - 1]
        return ((r[0] + r[2]) / 2, r[1] + sum(rows) / len(rows), best)

    badge, info = ring(gold), ring(teal)
    if not (groove and badge and info):
        sys.exit(f"Không đo được rãnh / hốc: rãnh {groove}, vòng cấp {badge}, nút {info}")
    crop = bbox(a[..., 3] > 0)

    def blk(r):
        x0, y0 = img_to_block(r[0], r[1])
        x1, y1 = img_to_block(r[2], r[3])
        return [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)]

    def circ(c):
        x, y = img_to_block(c[0], c[1])
        return [round(x, 1), round(y, 1), round(c[2] / S, 1)]

    info_json = {
        "source": str(src), "cabinet": blk(crop), "window": blk(win), "groove": blk(groove),
        "badge": circ(badge), "info": circ(info),
    }
    cab = info_json["cabinet"]
    size = (round(cab[2] - cab[0]), round(cab[3] - cab[1]))
    out = Image.fromarray(a).crop(crop).resize(size, Image.LANCZOS)
    GAME_ART.parent.mkdir(parents=True, exist_ok=True)
    out.save(GAME_ART, optimize=True)
    APPROVED.write_text(json.dumps(info_json, indent=1, ensure_ascii=False), encoding="utf-8")
    w = info_json["window"]
    print(f"  mặt chơi trong ảnh {w} (khung máy {BOARD_RECT}); rãnh {info_json['groove']}; vòng cấp {info_json['badge']}; nút {info_json['info']}")
    print(f"Ghi {GAME_ART} ({size[0]} x {size[1]}, {GAME_ART.stat().st_size // 1024} KB) và {APPROVED}")
    print("Trong Unity: menu \"PokiClash/Prefab/Máy bi: thân máy vẽ tay\"")


# ---------- duyệt tờ bộ phận, hiệu ứng, rương ----------

GAME_DIR = GAME_ART.parent  # Assets/03 Art/Pachinko
BOARD_PNG = HERE.parent.parent / "Assets" / "03 Art" / "Baked" / "Machine" / "may_tinh.png"
CHEST_NAMES = ["pk_ruong_go", "pk_ruong_go_mo", "pk_ruong_bac", "pk_ruong_bac_mo", "pk_ruong_vang", "pk_ruong_vang_mo"]


def cut_cells(src, cols, rows, split=False):
    """cắt tờ theo lưới: mỗi ô gọt sát phần không trong suốt (bỏ điểm mờ dưới 8); split: chỉ giữ khối liền chính"""
    im = Image.open(src).convert("RGBA")
    if im.size != (1536, 1024):
        sys.exit(f"Ảnh {src} cỡ {im.size}, cần 1536 x 1024")
    cw, ch = im.width / cols, im.height / rows
    out = []
    for r in range(rows):
        for c in range(cols):
            cell = im.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch)))
            a = np.array(cell)[..., 3] > 8
            if not a.any():
                sys.exit(f"Ô {r * cols + c + 1} của {src.name} trống")
            # món lấn sang ô bên (đuôi cọc dài, ánh sao) tách bằng khoảng trống: chỉ giữ dải hàng, dải cột liền có nhiều mực nhất
            if split:
                y0, y1 = main_run(a.sum(1))
                x0, x1 = main_run(a[y0:y1].sum(0))
                out.append(cell.crop((x0, y0, x1, y1)))
            else:
                out.append(cell.crop(bbox(a)))
    return out


def main_run(counts):
    """dải liền (không có hàng trống) có tổng lớn nhất: (đầu, cuối + 1)"""
    best, start, total, cur = (0, len(counts)), None, -1, 0
    for i, v in enumerate(list(counts) + [0]):
        if v > 0:
            if start is None:
                start, cur = i, 0
            cur += v
        elif start is not None:
            if cur > total:
                best, total = (start, i), cur
            start = None
    return best


def fit(im, max_side):
    k = max_side / max(im.size)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS) if k < 1 else im


def square(im, pad=0.06):
    """đặt vào ảnh vuông, giữa (hạt hiệu ứng được đặt cỡ vuông trong game)"""
    side = round(max(im.size) * (1 + 2 * pad))
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    return sq


def save_game(im, name):
    p = GAME_DIR / f"{name}.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, optimize=True)
    print(f"  {p.name} {im.width} x {im.height}, {p.stat().st_size // 1024} KB")


def approve_fx(src):
    cells = cut_cells(src, 3, 2)
    for name, im in zip(FX_NAMES, cells):
        save_game(fit(im, 384) if name == "fx_streak" else fit(square(im), 256), name)
    print("Trong Unity: menu \"PokiClash/Dựng lại danh mục ảnh\" (ảnh mới thay hình tạm cùng tên trong Fallback)")


def approve_chests(src):
    for name, im in zip(CHEST_NAMES, cut_cells(src, 3, 2)):
        save_game(fit(im, 320), name)
    print("Trong Unity: menu \"PokiClash/Dựng lại danh mục ảnh\"; ChestIcon tự dùng ảnh rương khi có")


# mặt máy CŨ (trước 2026-11-09, 11 ô và két vàng): bàn mới ghép bằng ghep_ban.py theo refs/mat_may.json
BW_, BH_, LEFT, RIGHT, SLOT_TOP, DROP_Y = 460, 680, 14, 446, 572, 46
SLOT_LAYOUT = ["chest_wood", "exp15", "exp5", "ball", "exp10", "chest_gold", "exp10", "ball", "exp5", "exp15", "chest_wood"]
SLOT_W = [25.25, 38, 46, 29.75, 59.25, 35.5, 59.25, 29.75, 46, 38, 25.25]
VAULT_X, GUARD_Y, GUARD_R, APEX_Y, SLIT, ROOF_HALF, ROOF_LOW_Y = 230, 446, 6, 470, 25.5, 60, 492
FLOOR_HALF, FLOOR_EDGE_Y, FLOOR_Y = 48, 516, 530
SLOT_COLOR = {
    "chest_wood": (255, 224, 176), "chest_gold": (255, 226, 122), "chest_silver": (223, 230, 238),
    "ball": (255, 210, 226), "exp15": (230, 210, 255), "exp10": (239, 226, 255), "exp5": (246, 239, 255),
}


def board_geometry():
    pegs, cups, posts = [], [], []
    in_vault = lambda x, y: abs(x - VAULT_X) < ROOF_HALF + 12 and GUARD_Y - 20 < y < FLOOR_Y + 20
    for i in range(10):
        y = 120 + i * 42
        odd = i % 2 == 1
        gap = 46.25
        for j in range(8 if odd else 9):
            x = (45 + gap / 2 if odd else 45) + j * gap
            if in_vault(x, y):
                continue
            if i == 3 and j in (1, 6) or i == 6 and j == 4:
                continue  # nấm: ảnh động
            if i == 7 and j in (1, 6):
                cups.append((x, y + 6))
                continue
            pegs.append((x, y, 5))
        if odd:
            posts += [(LEFT, y), (RIGHT, y)]
    pegs.append((VAULT_X, GUARD_Y, GUARD_R))
    xs = [LEFT]
    for w in SLOT_W:
        xs.append(xs[-1] + w)
    return pegs, cups, posts, xs


def three_slice(spr, length, thick):
    """ván, ray nằm ngang có hai đầu tròn: giữ hai đầu, kéo dài khúc giữa; ra ảnh length x thick"""
    w, h = spr.size
    cap = h // 2
    s = thick / h
    cw = max(1, round(cap * s))
    mid_len = max(1, round(length) - 2 * cw)
    left = spr.crop((0, 0, cap, h)).resize((cw, round(thick)), Image.LANCZOS)
    right = spr.crop((w - cap, 0, w, h)).resize((cw, round(thick)), Image.LANCZOS)
    mid = spr.crop((cap, 0, w - cap, h)).resize((mid_len, round(thick)), Image.LANCZOS)
    out = Image.new("RGBA", (2 * cw + mid_len, round(thick)), (0, 0, 0, 0))
    out.paste(left, (0, 0))
    out.paste(mid, (cw, 0))
    out.paste(right, (cw + mid_len, 0))
    return out


def compose_board(parts):
    """vẽ lại phần tĩnh của mặt máy (920 x 1360 = 2 lần bàn) từ bộ phận GPT, đúng toạ độ vật lý"""
    peg, _bumper, bump, post, cup, roof, floor, _cloud, _ball, shoulder, rail, plate = parts
    SS, OUT = 2, 2
    K = OUT * SS
    img = Image.new("RGBA", (BW_ * K, BH_ * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def P(x, y):
        return x * K, y * K

    def put(spr, cx, cy, w, h=None, angle=0):
        """dán ảnh cỡ w x h (đơn vị bàn) giữa ở (cx, cy), xoay angle độ (y xuống, chiều kim đồng hồ dương)"""
        h = h if h is not None else w * spr.height / spr.width
        im = spr.resize((max(1, round(w * K)), max(1, round(h * K))), Image.LANCZOS)
        if angle:
            im = im.rotate(-angle, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(im, (round(cx * K - im.width / 2), round(cy * K - im.height / 2)))

    def plank(spr, x1, y1, x2, y2, thick, extra):
        length = math.hypot(x2 - x1, y2 - y1) + 2 * extra
        im = three_slice(spr, length * K, thick * K)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        im = im.rotate(-ang, resample=Image.BICUBIC, expand=True)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        img.alpha_composite(im, (round(cx * K - im.width / 2), round(cy * K - im.height / 2)))

    # chấm trang trí trên mặt chơi (như draw_machine.py)
    y = 80
    while y < SLOT_TOP - 10:
        x = LEFT + 12 + ((y / 22) % 2) * 11
        while x < RIGHT - 6:
            d.ellipse([(x - 2.2) * K, (y - 2.2) * K, (x + 2.2) * K, (y + 2.2) * K], fill=(232, 85, 63, 31))
            x += 22
        y += 22
    pegs, cups, posts, xs = board_geometry()
    # ô đáy: gạch chéo hai mức đậm nhạt theo loại ô
    for i, kind in enumerate(SLOT_LAYOUT):
        x0, x1, y0, y1 = xs[i] + 1, xs[i + 1] - 1, SLOT_TOP, BH_ - 8
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        rgb = SLOT_COLOR[kind]
        ld.rectangle([P(x0, y0), P(x1, y1)], fill=rgb + (89,))
        span = int((x1 - x0) + (y1 - y0)) + 5
        for t in range(-span, span, 5):
            c = x0 + t
            ld.line([P(c, y1), P(c + (y1 - y0), y0)], fill=rgb + (255,), width=2 * K)
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).rectangle([P(x0, y0), P(x1, y1)], fill=255)
        clipped = Image.new("RGBA", img.size, (0, 0, 0, 0))
        clipped.paste(layer, (0, 0), mask)
        img.alpha_composite(clipped)
    d = ImageDraw.Draw(img)
    d.line([P(LEFT, BH_ - 8), P(RIGHT, BH_ - 8)], fill=(43, 33, 24, 255), width=3 * K)
    # cọc vách ô: núm tròn trên đầu (rộng KNOB), thân kéo dài tới đáy máy
    KNOB = 10
    knob_h = post.width
    s = KNOB / post.width
    top = post.crop((0, 0, post.width, knob_h))
    stick = post.crop((0, knob_h, post.width, post.height))
    for x in xs[1:-1]:
        y0 = SLOT_TOP - KNOB / 2
        stick_len = (BH_ - 8) - (y0 + knob_h * s) + 1
        put(stick, x, y0 + knob_h * s + stick_len / 2 - 0.5, post.width * s, stick_len)
        put(top, x, y0 + knob_h * s / 2, KNOB, knob_h * s)
    # ray máng thả, vai nghiêng
    plank(rail, LEFT + 8, DROP_Y - 22, RIGHT - 8, DROP_Y - 22, 7, 0)
    plank(shoulder, LEFT, 70, LEFT + 40, 104, 9, 3)
    plank(shoulder, RIGHT, 70, RIGHT - 40, 104, 9, 3)
    # két vàng: tấm nền, đáy V (núm hai đầu là hai cọc két), mái ^ hai tấm
    # tấm nền nằm gọn trong mái và đáy (viền nó không lòi ra ngoài két)
    put(plate, VAULT_X, (APEX_Y + FLOOR_EDGE_Y) / 2 + 4, 2 * ROOF_HALF - 18, FLOOR_EDGE_Y - APEX_Y + 4)
    put(floor, VAULT_X, (FLOOR_EDGE_Y + FLOOR_Y) / 2 - 1, 2 * FLOOR_HALF + 12, FLOOR_Y - FLOOR_EDGE_Y + 14)
    plank(roof, VAULT_X - ROOF_HALF, ROOF_LOW_Y, VAULT_X - SLIT / 2, APEX_Y, 9, 3)
    plank(roof.transpose(Image.FLIP_LEFT_RIGHT), VAULT_X + SLIT / 2, APEX_Y, VAULT_X + ROOF_HALF, ROOF_LOW_Y, 9, 3)
    # u lồi tường, đinh, cốc bạc
    for x, y in posts:
        put(bump, x, y, 21)
    for x, y, r in pegs:
        put(peg, x, y, 2 * r + 2)
    for x, y in cups:
        put(cup, x, y + 2, 30, 20)
    out = img.resize((BW_ * OUT, BH_ * OUT), Image.LANCZOS)
    return out


def approve_parts(src):
    # mặt máy tĩnh ghép bằng ghep_ban.py theo hình học bàn mới (refs/mat_may.json, bàn chép máy tham khảo 2026-11-09);
    # compose_board / board_geometry ở trên là bàn cũ (11 ô, két vàng), giữ lại để tra, không dùng nữa
    parts = cut_cells(src, 4, 3, split=True)
    if src.resolve() != (INBOX / "bo_phan.png").resolve():
        Image.open(src).save(INBOX / "bo_phan.png")
    import subprocess
    subprocess.run([sys.executable, "-I", str(HERE / "ghep_ban.py")], check=True)
    save_game(fit(square(parts[1], 0.03), 128), "pk_bumper")  # nấm: ảnh động phồng xẹp, thay hình tạm cùng tên
    save_game(fit(parts[7], 256), "pk_may_tha")  # máng mây
    save_game(fit(square(parts[8], 0.02), 64), "pk_bi")  # bi: game tô màu theo cược
    print("Trong Unity: menu \"PokiClash/Dựng lại danh mục ảnh\", rồi \"PokiClash/Prefab/Máy bi: ảnh bộ phận\"")


def latest(pattern):
    files = sorted(INBOX.glob(pattern), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


APPROVERS = {"than_may": None, "bo_phan": approve_parts, "hieu_ung": approve_fx, "ruong": approve_chests}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="*", default=None,
                    help="duyệt ảnh GPT: [than_may|bo_phan|hieu_ung|ruong] [ảnh] (mặc định thân máy, ảnh mới nhất trong tai_ve)")
    args = ap.parse_args()
    if args.duyet is not None:
        kind = args.duyet[0] if args.duyet and args.duyet[0] in APPROVERS else "than_may"
        rest = args.duyet[1:] if args.duyet and args.duyet[0] in APPROVERS else args.duyet
        src = Path(rest[0]) if rest else latest(f"{kind}*.png")
        if not src or not src.exists():
            sys.exit(f"Chưa có ảnh {kind} trong {INBOX}")
        print(f"Duyệt {src}")
        (APPROVERS[kind] or approve)(src)
        return
    info = draw_layout()
    refs, lines = prompt(info)
    PACK.mkdir(parents=True, exist_ok=True)
    (PACK / "luot_1_than_may.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    later = turns()
    for t in later:
        t["file"].write_text("\n".join(t["lines"]) + "\n", encoding="utf-8")
    guide(refs, info, later)
    print(f"Bố cục: {LAYOUT}")
    print(f"Gói: {PACK} (luot_1_than_may.txt, HUONG_DAN.md); GPT lưu {OUT}")
    for t in later:
        print(f"  lượt {t['n']} {t['vi']}: {t['file'].name}; GPT lưu {t['out']}")
    if not SCREEN.exists():
        print(f"  ! chưa có ảnh chụp màn Máy bi ({SCREEN}): file prompt bỏ ảnh đó")


if __name__ == "__main__":
    main()
