"""Gói GPT vẽ HÌNH HẠT cho hiệu ứng lửa (người dùng dặn 2026-11-10: "các sprite lửa/khói có thể gọi gpt ra gen cho đẹp").

Hiệu ứng vẫn là hạt chồng lớp (fxlib.py, bo_hoa.py); GPT chỉ vẽ HÌNH của hạt thay cho hình sinh bằng thuật toán (fire.py).
- H01..H05: hình XÁM có vân chì sáp, KHÔNG VIỀN (game nhuộm màu theo tuổi bằng Image.color và tự vẽ một viền mực ngoài cả khối).
- H06, H07: hạt nhỏ và đá đủ màu, có viền mực (không nhuộm, không chồng lớp).
Mỗi bước một ảnh 1024 vuông, lưới 2 x 2: bốn hình rời, mỗi hình nằm giữa ô của nó, cách nhau bằng khoảng trắng.

Hai gói: hat_lua (lửa, khói, dung nham; H01–H07) và hat_nuoc (bộ Thủy 2026-11-10: sóng cuộn, giọt, vương miện nước, bọt;
N01–N04). Chạy:
  py -3 -I build_hat.py [gói]          dựng gói ArtGen/Spine/gui_gpt/<gói>/ (file prompt + HUONG_DAN.md); mặc định hat_lua
  py -3 -I build_hat.py --nhap [gói]   cắt ảnh GPT mới nhất của từng bước (inbox/<gói>/tai_ve/<bước>*.png) thành
                                       hat_gpt/<tên>_<i>.png; fxlib.Art tự dùng ảnh trong hat_gpt/ khi có
Gen tự động: py -3 -I gen.py gui_gpt/<gói>/luot_1_hat.txt --steps N01,N02,...
"""
import glob
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE.replace("\\", "/") + "/"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
CODE = "hat_lua"
PK = os.path.join(HERE, "gui_gpt", CODE)
SAVE = os.path.join(HERE, "inbox", CODE, "tai_ve")
OUT = os.path.join(HERE, "hat_gpt")
FX_ART = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx"))


def W(p):
    return os.path.normpath(p)


GREY = ("FILL ONLY, NO OUTLINE: each shape is a flat medium-light neutral grey (about #BDBDBD) coloured with coloured "
        "pencils and wax crayons, the strokes visible as loose diagonal hatching a little lighter and darker than the grey "
        "(about #A8A8A8 to #D8D8D8). Absolutely NO outline, no ink line, no dark edge around or inside the shapes: the game "
        "colours this grey itself and draws one outline around the whole mass. No other colour at all.")
INKED = ("RENDERING: the hand-drawn look of image 1: drawn by hand on paper with a dark-brown ink pen (#2B2118), an outline "
         "about {n} px thick on this 1024 canvas, the same weight on every edge, slightly wobbly like a real pen; every area "
         "coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.")
FLAT = ("FLAT, NO LIGHT, NO SHADOW: every area one even colour, the strokes are texture only. No shading, no darker side, no "
        "shadows of any kind (nothing on the background), no white highlights or shine spots, no gloss, no glow or halo, no "
        "gradients, no 3D render.")
GRID = ("LAYOUT (see image 2): a square 1024 x 1024 image, plain pure white background, split in your head into a 2 x 2 grid "
        "of four equal squares. Draw ONE separate shape centred in each square, each filling about 70% of its square, with a "
        "clear white gap between shapes and around the edge (no shape touches another or the image edge). No creature, no "
        "ground, no text, no grid lines, no frame.")

# (bước, tên, tên tiếng Việt, viền px hoặc None = xám không viền, mô tả tiếng Anh, mô tả tiếng Việt, tên hạt khi nhập)
STEPS = [
    ("H01", "smoke", "khói", None,
     "Four different cartoon smoke puffs (top-left, top-right, bottom-left, bottom-right): each a soft rounded cloud made of "
     "three to six overlapping round bumps of different sizes, a fluffy bumpy edge all round, a little irregular so the four "
     "look different (one round, one wide, one tall, one lumpy). Like the round smoke puffs of a storybook cartoon.",
     "bốn cụm khói hoạt hình khác nhau: mỗi cụm là 3–6 bướu tròn chồng nhau, mép xù tròn, một cụm tròn, một cụm bè, một cụm "
     "cao, một cụm lổn nhổn", "sblob"),
    ("H02", "flame_puff", "cụm lửa tròn", None,
     "Four different round flame puffs: each a plump rounded blob of fire with a soft bumpy edge and one to three short "
     "rounded flame licks rising from its top, wider at the bottom; four different silhouettes.",
     "bốn cụm lửa tròn: mỗi cụm là khối tròn mập, mép gợn mềm, có 1–3 ngọn lửa ngắn tròn đầu nhô lên phía trên, đáy rộng",
     "blob"),
    ("H03", "flame_hook", "lưỡi lửa móc câu", None,
     "Four separate single flame tongues, all pointing straight UP: each has a round plump base at the bottom, an S-curved "
     "body and a sharp pointed tip that curls over to one side like a hook (two tips curl left, two curl right). Elegant "
     "storybook flame shapes like a decorative fire pattern.",
     "bốn lưỡi lửa rời chĩa thẳng lên: đáy tròn mập, thân cong chữ S, ngọn nhọn quặp sang một bên như móc câu (hai cái quặp "
     "trái, hai cái quặp phải)", "hook"),
    ("H04", "flame_swirl", "lưỡi lửa xoắn", None,
     "Four separate decorative flame tongues pointing UP in an oriental ornamental style: each a flame shape whose tip ends in "
     "a tight spiral curl, with one or two smaller curls branching from its side; plump at the base. Like traditional "
     "swirling fire ornaments.",
     "bốn lưỡi lửa trang trí kiểu phương Đông chĩa lên: ngọn kết thúc bằng một vòng xoắn ốc chặt, bên hông có 1–2 xoắn nhỏ",
     "xhook"),
    ("H05", "lava", "giọt và vệt dung nham", None,
     "Top row: two thick liquid drops flying UP, each a plump round blob with a short tapering tail hanging below it and one "
     "tiny droplet beside it. Bottom row: two flat liquid splats on the ground seen from a low angle, each a wide oval puddle "
     "about three times wider than tall with three or four short splashing tongues and two small droplets around it.",
     "hàng trên: hai giọt chất lỏng đặc bay lên (khối tròn mập, đuôi thon ngắn phía dưới, một giọt nhỏ bên cạnh); hàng dưới: "
     "hai vệt toé dẹt trên mặt đất nhìn chếch thấp (vũng bầu dục rộng gấp ba chiều cao, 3–4 lưỡi toé ngắn, hai giọt nhỏ)",
     "ldrop"),
    ("H06", "bits", "hạt nhỏ có màu", 10,
     "Four small fire bits, each in its own square: top-left a spark streak flying to the RIGHT (a long thin tapering streak, "
     "pointed tail on the left, round head on the right, yellow with a cream core); top-right a glowing ember chunk (a small "
     "rounded irregular lump, orange with a yellow middle); bottom-left a four-pointed sparkle star (yellow with a cream "
     "centre); bottom-right three flat ash flakes (small irregular thin flakes, two charcoal black and one ash grey).",
     "bốn hạt nhỏ: trên trái tia lửa bay sang phải (vệt thuôn dài, đuôi nhọn trái, đầu tròn phải, vàng lõi kem); trên phải cục "
     "than hồng (khối tròn méo nhỏ, cam giữa vàng); dưới trái sao bốn cánh (vàng tâm kem); dưới phải ba mảnh tro dẹt (hai đen "
     "than, một xám tro)", "bits"),
    ("H07", "rocks", "đá dung nham", 12,
     "Four different chunks of volcanic rock flung by an eruption: angular faceted lumps of dark purple-grey stone (about "
     "#48394A) with a few thin glowing cracks drawn as flat orange lines with a yellow core (flat colours, not glowing); four "
     "different shapes, small to medium.",
     "bốn cục đá núi lửa góc cạnh màu tím than (khoảng #48394A), có vài khe nứt mảnh tô cam lõi vàng (màu phẳng, không phát "
     "sáng), bốn dáng khác nhau", "rock"),
]


STEPS_NUOC = [
    ("N01", "wave", "sóng cuộn", None,
     "Four separate tongues of water, all rising straight UP, like small breaking waves seen from the side: each has a "
     "round plump base at the bottom, a thick curved body, and a top that curls over to one side into a rounded hook like a "
     "breaking wave crest (two curl to the left, two curl to the right); one or two of them have a second smaller curl on "
     "the shoulder. Thick, plump, storybook wave shapes like the curled crests in images 3 and 4. Shapes only: no foam "
     "bumps, no droplets.",
     "bốn lưỡi nước rời dựng thẳng lên như sóng nhỏ đang đổ nhìn ngang: chân tròn mập, thân dày cong, ngọn cuộn tròn sang một "
     "bên như mào sóng (hai cái cuộn trái, hai cái cuộn phải), một hai cái có thêm cuộn nhỏ ở vai", "wave"),
    ("N02", "drop", "giọt nước", None,
     "Four separate water droplets, one per square, each a teardrop with its pointed tail straight UP and its round belly "
     "down: one plump and short, one long and slim, one medium with a slightly bent tail, one small and round with a very "
     "short tail.",
     "bốn giọt nước rời hình giọt lệ, đuôi nhọn chĩa thẳng lên, bụng tròn ở dưới: một giọt mập ngắn, một giọt dài thon, một "
     "giọt vừa đuôi hơi cong, một giọt nhỏ tròn đuôi rất ngắn", "drop"),
    ("N03", "crown", "nước toé", None,
     "Top row: two splash crowns seen from the side, each a low wide base with five to seven pointed tongues of water of "
     "different heights rising and leaning outward like a crown. Bottom row: two round splash bursts seen from the front, "
     "each with seven to nine rounded pointed spikes of water radiating from the centre like image 3 (shape only, one solid "
     "silhouette, no separate droplets).",
     "hàng trên: hai vương miện nước nhìn ngang (đế thấp rộng, 5–7 lưỡi nước nhọn cao thấp khác nhau vươn lên và ngả ra "
     "ngoài); hàng dưới: hai vụ nước toé tròn nhìn thẳng (7–9 mũi nước nhọn bo tròn toả từ tâm), mỗi hình một khối liền", "crown"),
    ("N04", "foam", "bọt nước", None,
     "Four different puffs of sea foam: each a cluster of five to eight round bubbles of different sizes stuck together "
     "(clearly circular bumps, like the white foam on the wave crests in images 3 and 4), a little irregular so the four "
     "look different: one round, one wide, one tall, one small.",
     "bốn cụm bọt biển: mỗi cụm 5–8 bong bóng tròn to nhỏ dính nhau (bướu tròn rõ, như bọt trắng trên mào sóng), một cụm "
     "tròn, một cụm bè, một cụm cao, một cụm nhỏ", "foam"),
]
# Gói hat_gai (2026-11-12, Cầu Gai = suất tien_la đảo Mộc; người dùng: "chiêu đợi gpt xong thì gen ảnh"): hạt cho chiêu mana "Gồng
# Gai" (gai phóng tới đối thủ, gai trồi dưới chân nó, dăm gai văng lúc trúng). Xám vân chì, không viền, game nhuộm kem / lục.
STEPS_GAI = [
    ("G01", "thorn", "gai", None,
     "Four separate cactus thorns, one per square, each pointing straight UP with its base at the bottom: one fat short cone "
     "with a rounded bulging base; one long slim needle, very sharp; one medium thorn with a slightly curved tip like a claw; "
     "one stubby thick thorn. Each is one simple solid shape with a round base and ONE sharp point, like the cream thorns on "
     "the creature in image 3. Shapes only: no plant, no skin, no base plate.",
     "bốn cái gai xương rồng rời, mũi chĩa thẳng lên, gốc ở dưới: một nón mập ngắn gốc phình tròn, một kim dài mảnh rất nhọn, "
     "một gai vừa mũi hơi cong như vuốt, một gai lùn mập; mỗi cái một khối đặc gốc tròn một mũi nhọn", "thorn"),
    ("G02", "tuft", "cụm gai trồi", None,
     "Four separate CLUSTERS of cactus thorns seen from the side, each bursting UP out of the ground: a low wide base at the "
     "bottom and four to six sharp thorns of different lengths fanning upward and outward from it like a crown of spikes "
     "(the middle thorns tallest, the outer ones leaning left and right). Make the four different: one tall and narrow, one "
     "wide and low, one leaning a little to the left, one leaning a little to the right. Each cluster is ONE solid "
     "silhouette (the thorns joined at the base), same thorn shape as on the creature in image 3.",
     "bốn CỤM gai trồi lên từ đất nhìn ngang: đế thấp rộng, 4–6 gai nhọn dài ngắn khác nhau xoè lên và ra hai bên như vương "
     "miện gai (gai giữa cao nhất); một cụm cao hẹp, một cụm bè thấp, một cụm ngả trái, một cụm ngả phải; mỗi cụm một khối liền",
     "tuft"),
    ("G03", "shard", "dăm gai", None,
     "Four separate small broken thorn SPLINTERS, one per square, each a short jagged shard of a snapped thorn: one a broken "
     "thorn tip (a short sharp point with a rough snapped end), one a thin sliver with two pointed ends, one a chunky "
     "three-cornered chip, one a short curved shard. Angular, sharp, clearly different from each other.",
     "bốn mảnh dăm gai gãy rời: một đầu gai gãy (mũi nhọn ngắn, đầu kia nham nhở), một dăm mảnh hai đầu nhọn, một mẩu ba góc "
     "dày, một mảnh cong ngắn; góc cạnh, sắc, khác nhau rõ", "shard"),
]
STEPS_LUA = STEPS
PACKS = {
    "hat_gai": {"steps": STEPS_GAI, "ten": "hình hạt gai xương rồng (gai, cụm gai trồi, dăm gai)",
                "what": "particle sprites for a cactus-thorn attack in a 2D creature game with a hand-drawn storybook look. The "
                        "game spawns many of these little shapes, moves, scales, rotates and tints them (warm cream, dark "
                        "green) to build a volley of flying thorns, thorns bursting out of the ground and flying splinters, so "
                        "each image is a sheet of four separate shapes."},
    "hat_lua": {"steps": STEPS_LUA, "ten": "hình hạt lửa, khói, dung nham",
                "what": "particle sprites for fire effects in a 2D creature game with a hand-drawn storybook look. The game "
                        "spawns hundreds of these little shapes, moves, scales, rotates and tints them to build flames, smoke "
                        "and lava, so each image is a sheet of four separate shapes."},
    "hat_nuoc": {"steps": STEPS_NUOC, "ten": "hình hạt nước (sóng cuộn, giọt, nước toé, bọt)",
                 "what": "particle sprites for water effects in a 2D creature game with a hand-drawn storybook look. The game "
                         "spawns hundreds of these little shapes, moves, scales, rotates and tints them (deep blue, sky blue, "
                         "light blue, white foam) to build water jets, water balls and splashes, so each image is a sheet of "
                         "four separate shapes."},
}


def use(code):
    global CODE, PK, SAVE, STEPS
    CODE = code
    PK = os.path.join(HERE, "gui_gpt", CODE)
    SAVE = os.path.join(HERE, "inbox", CODE, "tai_ve")
    STEPS = PACKS[code]["steps"]


def layout_ref(path):
    """ảnh 2: bố cục lưới 2 x 2 bằng hình xám thuật toán hiện có (chỉ để GPT hiểu bố cục và dáng, không chép nét)."""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)  # chay bang py -3 -I thi thu muc script khong nam trong sys.path
    import fire
    S = 1024
    im = Image.new("RGB", (S, S), (255, 255, 255))
    d = ImageDraw.Draw(im)
    tiles = [fire.blob(0)[0], fire.hook(1)[0], fire.hook(2)[0], fire.blob(3)[0]]
    for i, t in enumerate(tiles):
        t = t.resize((340, 340), Image.LANCZOS)
        x, y = (i % 2) * 512 + 86, (i // 2) * 512 + 86
        im.paste(t, (x, y), t)
    for k in (512,):
        d.line([(k, 30), (k, S - 30)], fill=(220, 220, 220), width=2)
        d.line([(30, k), (S - 30, k)], fill=(220, 220, 220), width=2)
    im.save(path)


def build():
    os.makedirs(PK, exist_ok=True)
    os.makedirs(SAVE, exist_ok=True)
    ref2 = os.path.join(HERE, "chuan_fx", "hat_bo_cuc.png")
    layout_ref(ref2)
    ref3 = os.path.join(HERE, "chuan_fx", "hat_dung_the_nao.png")
    if CODE == "hat_lua":
        g = Image.open(os.path.join(HERE, "chuan_fx", "bo_hoa", "phun_lua.gif"))
        g.seek(22)
        g.convert("RGB").save(ref3)
    refs = [(WORLD_STYLE, "the game's approved hand-drawn map: copy its RENDERING (pencil and crayon hatching, ink line "
                          "where a step asks for one), ignore its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ"),
            (ref2, "LAYOUT ONLY: four separate shapes in a 2 x 2 grid on white (these grey shapes are rough placeholders made "
                   "by a program; draw much nicer hand-made shapes, the grey lines only show the four squares, do not draw them)",
             "Bố cục mẫu (1024 vuông, nền trắng): lưới 2 × 2, mỗi ô một hình xám thô do máy vẽ; chỉ để GPT hiểu bố cục"),
            (ref3, "how the game uses these shapes: it stacks many copies, tints them red, orange, yellow, cream or smoke "
                   "grey and draws one ink outline around the whole mass (a flame breath between two creatures)",
             "Một khung phun lửa của game (1080 × 928, sân Hỏa): cho GPT thấy game chồng nhiều hình, nhuộm màu, viền mực ngoài khối")]
    if CODE == "hat_nuoc":
        refs = refs[:2] + [
            (os.path.join(FX_ART, "no_nuoc.png"),
             "the game's approved water splash: copy its SHAPE language (plump pointed water spikes, round foam bumps), but "
             "draw this step's shapes as grey fill only, no outline, no blue",
             "Vụ nước toé đã duyệt của game (512 × 505, nền trong): mũi nước nhọn mập, bọt tròn; chỉ lấy dáng hình"),
            (os.path.join(FX_ART, "xoay_nuoc.png"),
             "the game's approved swirling water: copy the SHAPE of its curled wave crests, but grey fill only, no outline",
             "Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): ba dòng nước mào sóng cuộn; chỉ lấy dáng mào sóng")]
    if CODE == "hat_gai":
        refs = refs[:2] + [
            (os.path.join(HERE, "inbox", "xuong_rong_2", "tai_ve", "L1_duyet.png"),
             "the approved creature that uses these particles (a round cactus monster): copy the SHAPE language of its cream "
             "thorns (fat cones with a rounded base and one sharp point) and its crayon hatching, but draw this step's shapes "
             "as grey fill only, no outline, no cream, no green",
             "Concept Cầu Gai dạng 2 đã duyệt (1536 × 1024, nền trắng): xương rồng cầu lục sẫm, gai kem nón mập mũi nhọn; chỉ lấy "
             "dáng gai và vân sáp")]
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    order = [s[0] for s in STEPS]
    p1 = os.path.join(PK, "luot_1_hat.txt")
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", "WHAT THIS IS: " + PACKS[CODE]["what"], "",
          f"SAVE: every step's image goes into {W(SAVE)} under the step's name (for example {order[0]}.png). If that file "
          "already exists, add _2, _3 … before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. When I say \"next\", draw step {order[1]}, save it and stop: I "
          f"will check both. When I say \"continue\", draw the remaining steps one per reply, each after I say \"next\", in "
          f"this order: {', '.join(order[2:])}.", ""]
    if CODE == "hat_nuoc":  # hình xám của gói nước: ảnh mẫu 3, 4 có màu và viền, nhắc lại cho chắc
        t += ["IMPORTANT: images 3 and 4 are coloured and outlined, but YOUR shapes are flat grey with NO outline and NO blue.", ""]
    if CODE == "hat_gai":
        t += ["IMPORTANT: image 3 is coloured and outlined, but YOUR shapes are flat grey with NO outline and NO colour.", ""]
    for sc, name, _, n, en, _, _ in STEPS:
        t += [f"=== STEP {sc} ({name.replace('_', ' ')}) ===", en, ""]
        t += [GREY if n is None else INKED.format(n=n), FLAT, GRID]
        t += [f"SAVE this step: save it as a PNG to {W(os.path.join(SAVE, sc + '.png'))} (create the folder if it is missing; "
              f"if that file already exists, save it as {sc}_2.png, {sc}_3.png … in the same folder instead). Do not change, "
              "move or delete any other file.", ""]
    open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: {PACKS[CODE]['ten']} (`{CODE}`)", "",
          "Người dùng dặn 2026-11-10: hình hạt cho GPT vẽ cho đẹp. Hiệu ứng vẫn là hạt chồng lớp (`fxlib.py`, `bo_hoa.py`, "
          "`bo_thuy.py`); GPT chỉ vẽ **hình của hạt**. Bước ghi \"xám, KHÔNG viền\" là hình game tự nhuộm màu và tự vẽ một "
          "viền mực ngoài cả khối; bước ghi \"đủ màu\" thì có viền.", "",
          f"**Chỉ gửi GPT đường dẫn file prompt:** `{W(p1)}` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `{W(SAVE)}`.", "",
          f"1. GPT vẽ {order[0]}. Gõ `next`: GPT vẽ {order[1]}. Nhắn Claude \"soi {CODE}\".",
          f"2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: {', '.join(order[2:])}.",
          f"3. Đủ ảnh thì nhắn Claude \"nhập {CODE}\" (Claude chạy `py -3 -I build_hat.py --nhap {CODE}` rồi xuất lại bộ).",
          f"   Hoặc Claude tự gen: `py -3 -I gen.py gui_gpt/{CODE}/luot_1_hat.txt --steps {','.join(order)}`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(p)}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += ["", "Mỗi ảnh: 1024 vuông, nền trắng tinh, lưới 2 × 2 bốn hình rời không chạm nhau, không chạm mép. Kiểm từng ảnh:", ""]
    for sc, _, vi_name, n, _, vi, _ in STEPS:
        kind = "xám, KHÔNG viền" if n is None else f"đủ màu, viền mực khoảng {n} px"
        gd.append(f"- **{sc}** {vi_name} ({kind}): {vi}")
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| H01–H05 có viền mực hoặc mép sẫm | `No outline at all: only the flat grey crayon fill, the edge is just where the grey stops.` |",
           "| H01–H05 có màu (đỏ, cam...) | `Only neutral grey, no colour: the game tints the grey itself.` |",
           "| Có bóng, mảng sáng tối, quầng sáng | `" + FLAT + "` |",
           "| Hình chạm nhau, chạm mép | `Four separate shapes, one centred in each quarter, with clear white gaps between them and around the edge.` |",
           "| Không giống vẽ tay | `Draw it by hand on paper with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |",
           "", f"Gói sinh từ `{W(os.path.join(HERE, 'build_hat.py'))}`; sửa prompt ở đó rồi chạy lại.", ""]
    open(os.path.join(PK, "HUONG_DAN.md"), "w", encoding="utf-8", newline="").write("\n".join(gd))
    return W(p1)


# ---------------- nhập ảnh GPT ----------------
def _cut_quadrants(path):
    im = Image.open(path).convert("RGB")
    S = im.width
    out = []
    for i in range(4):
        q = im.crop(((i % 2) * S // 2, (i // 2) * S // 2, (i % 2 + 1) * S // 2, (i // 2 + 1) * S // 2))
        work = q.copy()
        w, h = q.size
        for sd in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)):
            if sum(work.getpixel(sd)) > 690:
                ImageDraw.floodfill(work, sd, (255, 0, 255), thresh=28)
        a = np.asarray(q.convert("RGBA")).copy()
        bg = np.all(np.asarray(work) == (255, 0, 255), axis=2)
        a[bg, 3] = 0
        r = Image.fromarray(a, "RGBA")
        bb = r.getbbox()
        out.append(r.crop(bb) if bb else r)
    return out


def _fit(im, side):
    s = side / max(im.size)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS) if s < 1 else im


def nhap():
    os.makedirs(OUT, exist_ok=True)
    done = []
    for sc, _, _, n, _, _, name in STEPS:
        src = sorted(glob.glob(os.path.join(SAVE, sc + "*.png")), key=os.path.getmtime, reverse=True)
        if not src:
            continue
        for i, q in enumerate(_cut_quadrants(src[0])):
            q = _fit(q, 256)
            # đặt giữa khung vuông có lề như hình thuật toán (fire.py): game vẽ ảnh hạt theo ô vuông, cắt sát thì hình bị bóp méo
            side = int(max(q.size) * 1.08)
            sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
            sq.paste(q, ((side - q.width) // 2, (side - q.height) // 2))
            q = sq
            a = np.asarray(q).astype(np.float32)
            if n is None:  # xám không viền -> ảnh xám nhuộm được: trung vị về 236 (như fire.GRAY), ảnh đặc cho lớp mực
                al = a[..., 3] > 8
                lum = a[..., :3].mean(axis=2)
                med = float(np.median(lum[al])) if al.any() else 200.0
                g = np.clip(lum * (236.0 / max(1.0, med)), 0, 255)
                a[..., 0] = a[..., 1] = a[..., 2] = g
                Image.fromarray(a.astype(np.uint8), "RGBA").save(os.path.join(OUT, f"{name}_{i}.png"), optimize=True)
                solid = np.zeros_like(a)
                solid[..., :3] = 255
                solid[..., 3] = a[..., 3]
                Image.fromarray(solid.astype(np.uint8), "RGBA").save(os.path.join(OUT, f"{name}_s_{i}.png"), optimize=True)
            else:
                q.save(os.path.join(OUT, f"{name}_{i}.png"), optimize=True)
            done.append(f"{name}_{i}")
    print("đã nhập:", ", ".join(done) if done else "(chưa có ảnh GPT)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use(args[0] if args else "hat_lua")
    if "--nhap" in sys.argv:
        nhap()
    else:
        print(build())
