# Gói gửi GPT "bảng số, mở rương" của máy bi (2026-11-10). Người dùng: chép hiệu ứng máy bi tham khảo: bảng số dưới thanh cấp
# hiện EXP ăn được rồi mới đổ lên thanh, icon EXP bay từ ô lên bảng, ánh sáng và gradient, mở rương như mở capsule thú của máy đó
# (đưa ra tối đa 5 cái một lượt, lơ lửng, chạm từng cái hoặc mở tất cả, hiện thưởng một lượt).
# Chỉ học bộ phận và nhịp; hình vẽ mới theo nét đã duyệt (thân máy, tờ rương). Không đính ảnh của game đó, không nhắc tên game.
# Ánh sáng, gradient (quầng mềm, tia sáng, cột sáng, vệt lia, chấm LED) game sinh bằng code (sinh_anh_sang.py), GPT không vẽ.
# Ba lượt độc lập:
#   luot_1_bang_so.txt: bảng số kiểu biển đèn hội chợ treo trên đỉnh mặt chơi (màn tối trống, viền trơn để game gắn bóng đèn);
#   luot_2_keo_exp.txt: tờ 3 × 2: kẹo EXP, nắm kẹo EXP, thẻ úp, gối mây đỡ rương, dải ruy băng tiêu đề, nút tròn "mở tất cả";
#   luot_3_ruong_tach.txt: tờ 3 × 2: nắp rương gỗ, bạc, vàng rời; thân rương mở không nắp (nắp bật bay lên như vỏ capsule).
# GPT lưu tai_ve/bang_so.png, tai_ve/keo_exp.png, tai_ve/ruong_tach.png.
# Chạy: py -3 -I ArtGen/Pachinko/build_mo_ruong.py
# Duyệt: py -3 -I ArtGen/Pachinko/build_mo_ruong.py --duyet bang_so|keo_exp|ruong_tach [ảnh] (mặc định ảnh mới nhất trong tai_ve):
#   cắt, gọt sát, thu về cỡ hiện trên màn, lưu Assets/03 Art/Pachinko/pk_*.png; bảng số ghi thêm refs/bang_so.json (khung màn tối
#   theo tỉ lệ ảnh, để game đặt chữ số và bóng đèn); nắp và thân rương canh theo bề ngang rương đóng cùng loại.
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent  # ArtGen/Pachinko
_spec = importlib.util.spec_from_file_location("pk_build", HERE / "build.py")
pk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pk)

PACK = HERE / "gui_gpt" / "bang_so_mo_ruong"
INBOX = pk.INBOX
REFS = pk.REFS
GRID32 = pk.GRID32
GAME_DIR = HERE.parent.parent / "Assets" / "03 Art" / "Pachinko"
BOARD_JSON = REFS / "bang_so.json"
SCREEN = REFS / "man_may_bi_go.png"  # ảnh chụp màn Máy bi (bản 2026-11-06, có thể cũ hơn mặt máy hiện tại)
BOARD_NOW = HERE.parent.parent / "Assets" / "03 Art" / "Baked" / "Machine" / "may_tinh.png"

# tên ảnh trong game theo thứ tự ô; cạnh dài tối đa khi lưu (px, theo cỡ hiện trên màn 1080 × 1920)
NAMES = {
    "bang_so": [("pk_bang_so", 1024)],
    "keo_exp": [("pk_keo_exp", 160), ("pk_keo_exp_nam", 224), ("pk_the_up", 256),
                ("pk_may_do", 384), ("pk_ruy_bang", 1024), ("pk_nut_mo_het", 320)],
    "ruong_tach": [("pk_ruong_go_nap", 320), ("pk_ruong_bac_nap", 320), ("pk_ruong_vang_nap", 320),
                   ("pk_ruong_go_than", 320), ("pk_ruong_bac_than", 320), ("pk_ruong_vang_than", 320)],
}
CLOSED = ["pk_ruong_go", "pk_ruong_bac", "pk_ruong_vang"]


def chest_sheet():
    """tờ rương đã duyệt (ruong.png, ruong_2.png…), không lẫn ruong_tach.png của lượt 3"""
    files = [p for p in INBOX.glob("ruong*.png") if p.stem == "ruong" or p.stem[6:].isdigit()]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def grid_ref():
    return (GRID32, "1536 x 1024", "the numbered 3 x 2 grid of the sheet you draw: one item per cell, inside the grey inner box",
            "lưới 3 × 2 đánh số (ô hồng, khung xám là vùng an toàn)")


def head(refs, save):
    L = [pk.HEAD, "", "REFERENCE IMAGES (open each file from its full path):"]
    L += [f"image {i} = {p} ({size}): {what}" for i, (p, size, what, _) in enumerate(refs, 1)]
    return L + ["", save, ""]


def single_save(p):
    return (f"SAVE: save the finished image as a 1536 x 1024 PNG with a TRANSPARENT background to\n{p}\nCreate the folder if it is "
            f"missing. If that file already exists, save it as {p.stem}_2.png, {p.stem}_3.png … in the same folder instead. "
            f"Do not change, move or delete any other file.")


def tail(out, avoid, what):
    return ["", pk.STYLE_CAB, "", *pk.NO_SHADOW, "",
            "LIGHT: the game adds all glows, light beams and shine on top of your drawing by itself. Draw every item flat, with "
            "colour-pencil and crayon hatching, never with glow, gradients or glossy highlights.",
            "", f"AVOID: {avoid}", "", f"Remember: transparent background, {what}, save it to {out}"]


# ---------- lượt 1: bảng số ----------

def turn_board(cab):
    out = INBOX / "bang_so.png"
    refs = [cab,
            (BOARD_NOW, "920 x 1360", "the play board the game draws inside the cabinet window today (pegs, bumpers, prize slots); "
                                      "the scoreboard you draw hangs over the top of the arched play area, above the top peg; shown "
                                      "only so you understand the place, do NOT draw any of it",
             "mặt chơi game đang vẽ (đinh, máng, 5 ô); bảng số treo trên đỉnh vòm mặt chơi")]
    L = head(refs, single_save(out)) + [
        "WHAT THIS IS: the scoreboard of the ball-drop machine (a vertical pachinko) whose cabinet is image 1. It hangs at the top of "
        "the play window, over the top of the arch of image 2. While balls fall into the prize slots, little candy icons fly up into "
        "this sign and a big counter on it counts up the experience won; at the end the number pours into the level bar above. "
        "The game draws the digits, the candy icon, the light bulbs and every light effect on it by itself.",
        "",
        "DRAW ONE ITEM, centred in the 1536 x 1024 image, about 1400 px wide and 380 px tall (about 3.7 : 1), never touching the "
        "image edge:",
        "- a wide fairground marquee sign seen straight from the front: a chunky wooden frame in red-orange #E8553F with a slim "
        "orange #F39A2D bevel and a cream #FBF4E2 trim line on its inner edge;",
        "- the FRAME BAND is plain and even all around, about 70 px wide: the game places a row of round light bulbs along it, so do "
        "NOT draw bulbs, holes, studs or patterns on the band; only light crayon hatching. A small doodled rivet in each corner;",
        "- the top edge of the frame rises into a low gentle arch in the middle (a crest about 50 px higher than the corners), with "
        "one small doodled yellow #F7C948 star at its top;",
        "- inside the frame: one big flat dark plum-purple #3B2A4A screen with rounded corners, completely EMPTY: no digits, no "
        "dots, no grid, no reflections, no hatching pattern that looks like lights. The game lights digits and LED dots on it;",
        "- two short chunky wooden brackets under the bottom corners, as if the sign is fixed to the machine.",
        "",
        "COLOURS: red-orange #E8553F and orange #F39A2D wood, cream #FBF4E2 trim, dark plum #3B2A4A screen, yellow #F7C948 star, "
        "dark-brown ink #2B2118 outlines (about 6 px).",
    ] + tail(out, "text, letters, numbers, digits, light bulbs, LED dots, candy, characters, a background, a table, glow, light "
                  "rays, glossy highlights, a second sign.", "one sign in the middle")
    return dict(n=1, kind="bang_so", vi="bảng số", file=PACK / "luot_1_bang_so.txt", out=out, refs=refs, lines=L,
                what_vi="Bảng số kiểu biển đèn hội chợ treo trên đỉnh vòm mặt chơi (như bảng LED của máy tham khảo): kẹo EXP bay từ ô "
                        "lên bảng, số trên bảng đếm tăng, hết đợt số đổ lên thanh cấp. GPT vẽ khung gỗ và màn tối trống; chữ số, chấm "
                        "LED, bóng đèn chạy viền, quầng sáng do game làm.",
                checks=["ảnh 1536 × 1024 nền trong suốt, một biển ở giữa, dài khoảng 3,7 : 1;",
                        "viền gỗ đỏ cam đều quanh, trơn (không bóng đèn, không lỗ), giữa mép trên nhô vòm thấp có sao vàng nhỏ;",
                        "màn tím sẫm phẳng, trống trơn (không số, không chấm, không phản chiếu);",
                        "hai giá gỗ ngắn dưới hai góc; không bóng đổ, không quầng sáng."],
                fixes=["Same sign, but the screen must be completely empty flat dark plum, no digits, dots or reflections.",
                       "Same sign, but no bulbs or holes on the frame band: a plain even wooden band.",
                       "Same sign, but wider and lower, about 3.7 : 1, and fully inside the image with a margin."],
                after_vi=f"Xong thì nhắn Claude \"duyệt bảng số\". Tự cắt: `py -3 -I {HERE / 'build_mo_ruong.py'} --duyet bang_so` (lưu "
                         "`Assets/03 Art/Pachinko/pk_bang_so.png` và `refs/bang_so.json`); đặt bảng lên máy là việc code của Claude.")


# ---------- lượt 2: kẹo EXP và đồ của hộp mở rương ----------

def turn_candy(cab):
    out = INBOX / "keo_exp.png"
    chests = chest_sheet()
    refs = [cab, grid_ref(),
            (chests, "1536 x 1024", "the approved treasure chests of this machine (wooden, silver, golden; closed and open); shown "
                                    "for style and size, the cloud cushion of cell 4 must hold one of them",
             "tờ rương đã duyệt (gỗ, bạc, vàng; đóng và mở)")]
    L = head(refs, pk.sheet_save(out)) + [
        "WHAT THIS IS: small pieces for the ball-drop machine of image 1 and for its chest-opening screen. The experience points "
        "of the game are candies: when a ball lands in a prize slot, candies fly up to the scoreboard. When the player opens "
        "chests, up to five chests float on little clouds on a dark screen, burst open one by one, and the prizes come out as "
        "cards that flip over.",
        "", pk.SHEET_RULE, "",
        "CELLS:",
        "1 EXP CANDY (shown 60 px, it flies in big numbers): one chubby wrapped candy seen from the front: a round purple #9A6AD6 "
        "candy body with a lighter lilac #C18CF0 swirl stripe, and a twisted wrapper end on the left and on the right, like a bow "
        "tie; thick ink outline, flat colours, a small cream dot on the top left of the body. Simple and readable when tiny. About "
        "2 : 1 wide to tall.",
        "2 EXP CANDY PILE (shown 110 px): three candies exactly like cell 1 heaped together, one on top and two below, slightly "
        "overlapping. About 3 : 2.",
        "3 CARD BACK (shown 150 x 150 px): the back of a prize card lying face down, a rounded square: a thick cream #FBF4E2 border, "
        "inside a flat light-grey #E6E0D4 field with a big simple round ball emblem (a white circle with one horizontal band) in the "
        "middle and four tiny doodled stars in the corners. Light grey, because the game tints it with the rarity colour (blue, "
        "purple, gold).",
        "4 CLOUD CUSHION (shown 240 x 80 px): a soft fluffy white-cream #FBF4E2 cloud, wide and low (about 3 : 1), with a flat top "
        "where a chest stands on it, three or four round puffs on the bottom edge, light grey-blue #D6E2EA crayon hatching on the "
        "underside of the puffs. It floats; it is not a shadow.",
        "5 TITLE RIBBON (shown 700 x 140 px): a wide celebration ribbon banner: a long flat red-orange #E8553F band with a cream "
        "#FBF4E2 trim line along both edges, a gentle upward smile curve, and a folded ribbon tail at each end in darker red "
        "#C8432F with a V notch. The middle of the band is EMPTY and calm (the game writes the title there). About 5 : 1.",
        "6 OPEN-ALL BUTTON (shown 300 x 120 px): a chunky pill-shaped push-button of the same family as the cabinet: golden yellow "
        "#F7C948 face, thick cream #FBF4E2 collar, orange-wood #F39A2D base edge under it, three tiny doodled stars on the left end "
        "of the face; the middle of the face EMPTY (the game writes the label). About 5 : 2.",
        "", "COLOURS: the colours listed above, dark-brown ink #2B2118 outlines.",
    ] + tail(out, "text, letters, numbers, labels on the ribbon or the button, characters, a background, glow, light rays, glossy "
                  "highlights, two items in one cell.", "one item per cell in the order 1 to 6")
    return dict(n=2, kind="keo_exp", vi="kẹo EXP, đồ hộp mở rương", file=PACK / "luot_2_keo_exp.txt", out=out, refs=refs,
                lines=L,
                what_vi="Kẹo EXP (icon bay từ ô lên bảng số, như kẹo của máy tham khảo, thay ngôi sao XP vẽ tạm), nắm kẹo cho ô nhiều "
                        "EXP; đồ cho màn mở rương kiểu mở capsule: thẻ úp (game tô màu độ hiếm rồi lật), gối mây rương đứng lơ lửng, "
                        "ruy băng tiêu đề, nút \"Mở tất cả\".",
                checks=["lưới 3 × 2, nền trong suốt, mỗi ô một món đúng thứ tự;",
                        "kẹo ô 1 tím có xoắn giấy hai bên, nhìn rõ khi nhỏ; ô 2 là ba viên y hệt ô 1;",
                        "thẻ úp xám nhạt có viền kem, giữa là hình bi tròn có một dải ngang;",
                        "mây dẹt khoảng 3 : 1, mặt trên phẳng; không phải bóng;",
                        "ruy băng và nút: giữa trống trơn, không chữ; không bóng đổ, không quầng sáng."],
                fixes=["Same sheet, but the candy in cell 1 simpler and chunkier, readable at 60 px, wrapper twists on both sides.",
                       "Same sheet, but leave the middle of the ribbon and of the button completely empty, no text.",
                       "Same sheet, but the card back light grey so the game can tint it."],
                after_vi=f"Xong thì nhắn Claude \"duyệt kẹo\". Tự cắt: `py -3 -I {HERE / 'build_mo_ruong.py'} --duyet keo_exp` (lưu "
                         "`pk_keo_exp`, `pk_keo_exp_nam`, `pk_the_up`, `pk_may_do`, `pk_ruy_bang`, `pk_nut_mo_het`).")


# ---------- lượt 3: nắp và thân rương rời ----------

def turn_split(cab):
    out = INBOX / "ruong_tach.png"
    chests = chest_sheet()
    refs = [cab, grid_ref(),
            (chests, "1536 x 1024", "the approved treasure chests, 3 x 2 cells: 1 wooden closed, 2 wooden open, 3 silver closed, "
                                    "4 silver open, 5 golden closed, 6 golden open; the pieces you draw are cut from exactly these "
                                    "chests (same outline, size, colours, bands, lock)",
             "tờ rương đã duyệt: 1 gỗ đóng, 2 gỗ mở, 3 bạc đóng, 4 bạc mở, 5 vàng đóng, 6 vàng mở")]
    L = head(refs, pk.sheet_save(out)) + [
        "WHAT THIS IS: the treasure chests of image 3 taken apart into two pieces, for the chest-opening screen of the ball-drop "
        "machine of image 1. The game shows the closed chest, shakes it, then swaps it for these two pieces: the LID bursts off "
        "upward and spins away, the BODY stays and light pours out of it. So the two pieces of one chest must fit back together "
        "exactly into the closed chest of image 3: same width, same outline, same bands, same colours.",
        "", pk.SHEET_RULE, "",
        "SAME SIZE RULE: every piece is drawn at the scale of the chests of image 3, as wide as the closed chest of its material. "
        "The three lids have the same shape; the three bodies have the same shape.",
        "",
        "CELLS:",
        "1 WOODEN LID: only the rounded lid of the closed wooden chest (image 3 cell 1), from its top curve down to the seam where "
        "it meets the box, seen from the front exactly as on the closed chest: wooden planks, the two dark iron bands crossing it. "
        "Its bottom edge is a clean straight ink line. Nothing of the box below.",
        "2 SILVER LID: the same for the silver chest (image 3 cell 3): pale blue-grey wood, silver bands.",
        "3 GOLDEN LID: the same for the golden chest (image 3 cell 5): golden-yellow wood, orange-gold bands, the tiny crown doodle.",
        "4 WOODEN BODY, OPEN: only the box of the wooden chest without its lid, seen from the front and a little from above exactly "
        "as on the chest: the front with the planks, the two iron bands and the round brass lock plate at its top edge; at the "
        "top a flat light-yellow #FFF2A8 opening (the inside), with a thin wooden rim around it. No lid, no hinge, no stars, no "
        "coins.",
        "5 SILVER BODY, OPEN: the same for the silver chest (round silver lock with the small blue gem).",
        "6 GOLDEN BODY, OPEN: the same for the golden chest (round lock with the red gem).",
        "", "COLOURS: exactly the colours of image 3, dark-brown ink #2B2118 outlines.",
    ] + tail(out, "text, letters, numbers, characters, a background, glow, light rays, sparkles, coins, stars around the pieces, "
                  "a lid still attached to a body, two pieces in one cell.", "one piece per cell in the order 1 to 6")
    return dict(n=3, kind="ruong_tach", vi="nắp, thân rương rời", file=PACK / "luot_3_ruong_tach.txt", out=out, refs=refs,
                lines=L,
                what_vi="Nắp và thân rương rời của ba loại rương (cắt từ đúng tờ rương đã duyệt): lúc mở, rương lắc rồi nắp bật bay "
                        "xoáy lên, thân đứng lại và ánh sáng tuôn ra (như vỏ capsule tách đôi ở máy tham khảo).",
                checks=["lưới 3 × 2, nền trong suốt; hàng trên ba nắp, hàng dưới ba thân mở;",
                        "nắp trùng dáng nắp của rương đóng, mép dưới thẳng; thân có khoá tròn ở mép trên, miệng vàng nhạt phẳng;",
                        "nắp và thân cùng loại ghép lại khớp rương đóng (cùng bề ngang, cùng đai);",
                        "không sao, không xu, không bóng đổ, không quầng sáng."],
                fixes=["Same sheet, but each lid must be exactly the lid of the closed chest of image 3, same width, straight bottom edge.",
                       "Same sheet, but the bodies without any lid or hinge, only a flat light-yellow opening at the top.",
                       "Same sheet, but no stars, coins or glow around the pieces."],
                after_vi=f"Xong thì nhắn Claude \"duyệt rương tách\". Tự cắt: `py -3 -I {HERE / 'build_mo_ruong.py'} --duyet ruong_tach` "
                         "(lưu `pk_ruong_*_nap`, `pk_ruong_*_than`, cùng bề ngang rương đóng); hiệu ứng mở là việc code của Claude.")


# ---------- hướng dẫn ----------

def guide(turns):
    g = ["# Gói gửi GPT: máy bi, bảng số và mở rương", "",
         f"Sinh bằng `{HERE / 'build_mo_ruong.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè).", "",
         "Chép hiệu ứng máy bi tham khảo: bảng số dưới thanh cấp (kẹo EXP bay từ ô lên bảng, số đếm tăng, hết đợt mới đổ lên thanh), "
         "mở rương như mở capsule thú (tối đa 5 cái một lượt, lơ lửng, chạm từng cái hoặc mở tất cả, hiện thưởng một lượt). Hình vẽ "
         "theo nét đã duyệt (thân máy, rương); không đính ảnh của game đó cho GPT, không nhắc tên game.", "",
         "Ánh sáng và gradient (quầng mềm, tia sáng, cột sáng từ rương, vệt sáng lia qua bảng, chấm LED) game tự sinh bằng code, "
         "GPT chỉ vẽ hình phẳng.", "",
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

def main_piece(im):
    """khối liền lớn nhất (bỏ bụi, vệt lạc), gọt sát"""
    a = np.array(im.convert("RGBA"))
    lab, n = ndimage.label(a[..., 3] > 8)
    if n == 0:
        sys.exit("Ảnh trống")
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep = np.zeros_like(lab, bool)
    big = sizes.max()
    for i, s in enumerate(sizes, 1):
        if s >= big * 0.02:
            keep |= lab == i  # giữ các khối không quá nhỏ (giá gỗ rời, ngôi sao)
    a[..., 3] = np.where(keep, a[..., 3], 0)
    out = Image.fromarray(a)
    return out.crop(pk.bbox(keep))


def approve_board(src):
    im = main_piece(Image.open(src))
    im = pk.fit(im, NAMES["bang_so"][0][1])
    a = np.array(im).astype(int)
    # màn tối: khối liền lớn nhất của điểm đặc tối, tím sẫm (không phải mực nâu viền: mực mảnh, màn rộng)
    dark = (a[..., 3] > 200) & (a[..., :3].max(-1) < 110) & (a[..., 2] >= a[..., 1])
    dark = ndimage.binary_opening(dark, iterations=3)
    lab, n = ndimage.label(dark)
    if n == 0:
        sys.exit("Không thấy màn tối trong bảng số")
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    k = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lab == k)
    H, W = a.shape[:2]
    screen = [round(xs.min() / W, 4), round(ys.min() / H, 4), round((xs.max() + 1) / W, 4), round((ys.max() + 1) / H, 4)]
    # dải viền gỗ để gắn bóng đèn: giữa mép ngoài (khối không trong suốt) và mép màn, theo tỉ lệ ảnh
    pk.save_game(im, "pk_bang_so")
    data = {"image": [W, H], "screen": screen,
            "note": "khung màn tối theo tỉ lệ ảnh pk_bang_so (x0, y0, x1, y1, gốc trên trái); bóng đèn đặt giữa mép ảnh và mép màn"}
    BOARD_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Màn tối {screen}, ghi {BOARD_JSON}")


def approve_candy(src):
    for (name, side), im in zip(NAMES["keo_exp"], pk.cut_cells(src, 3, 2, split=True)):
        pk.save_game(pk.fit(im, side), name)


def approve_split(src):
    cells = pk.cut_cells(src, 3, 2, split=True)
    for i, ((name, side), im) in enumerate(zip(NAMES["ruong_tach"], cells)):
        closed = GAME_DIR / f"{CLOSED[i % 3]}.png"
        if closed.exists():
            w = Image.open(closed).width  # cùng bề ngang rương đóng (game ghép nắp lên thân theo khung rương đóng)
            im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
        pk.save_game(pk.fit(im, side), name)


APPROVERS = {"bang_so": approve_board, "keo_exp": approve_candy, "ruong_tach": approve_split}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="*", default=None, help="duyệt ảnh GPT: bang_so|keo_exp|ruong_tach [ảnh]")
    args = ap.parse_args()
    if args.duyet is not None:
        if not args.duyet or args.duyet[0] not in APPROVERS:
            sys.exit(f"Cần loại: {', '.join(APPROVERS)}")
        kind = args.duyet[0]
        src = Path(args.duyet[1]) if len(args.duyet) > 1 else pk.latest(f"{kind}*.png")
        if not src or not src.exists():
            sys.exit(f"Chưa có ảnh {kind} trong {INBOX}")
        print(f"Duyệt {src}")
        APPROVERS[kind](src)
        print("Trong Unity: menu \"PokiClash/Dựng lại danh mục ảnh\".")
        return
    cab = pk.cabinet_ref()
    if not cab:
        sys.exit("Chưa có thân máy đã duyệt (tai_ve/than_may.png)")
    if not chest_sheet():
        sys.exit("Chưa có tờ rương đã duyệt (tai_ve/ruong.png)")
    PACK.mkdir(parents=True, exist_ok=True)
    turns = [turn_board(cab), turn_candy(cab), turn_split(cab)]
    for t in turns:
        t["file"].write_text("\n".join(t["lines"]) + "\n", encoding="utf-8")
        print(f"lượt {t['n']} {t['vi']}: {t['file']}; GPT lưu {t['out']}")
    guide(turns)
    print(f"Hướng dẫn: {PACK / 'HUONG_DAN.md'}")


if __name__ == "__main__":
    main()
