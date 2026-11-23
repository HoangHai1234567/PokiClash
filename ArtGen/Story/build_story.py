# Đoạn cốt truyện mở đầu (lần đầu vào game, trước màn tải con tàu; học trang truyện tranh mở đầu Kingdom Rush): 2 trang, 6 khung,
# chạm một lần hiện một khung, ít chữ (game in chữ, GPT không vẽ chữ). Nội dung: một cậu bé thuần thú sư cầm sổ phép bị cơn bão cuốn
# vào thế giới lạ đầy sinh vật kỳ bí, kết bạn năm sinh vật nhỏ, rồi đi chinh phục năm đảo. Cậu là nhân vật chính (người chơi), cũng
# nói vài lời dẫn trong hướng dẫn người mới (chân dung bán thân). Gói gửi GPT theo luật ArtGen (CLAUDE.md): mỗi lượt một file prompt ghi
# đường dẫn đầy đủ của ảnh mẫu và chỗ GPT lưu ảnh; người dùng chỉ gửi GPT đường dẫn file đó.
# - Lượt 0: tờ thiết kế nhân vật chính (chốt hình cậu bé, sổ phép, bút chì phép).
# - Lượt 1 (chỉ dựng khi tờ nhân vật đã duyệt): chân dung bán thân nền trong suốt (lời dẫn hướng dẫn) + khung 2 (tỉnh dậy trên bãi
#   biển lạ, chốt nét truyện).
# - Lượt 2 (khung 1, 3) và lượt 3 (khung 4, 5, 6): chỉ dựng khi khung 2 đã duyệt.
# Chạy: py -3 -I ArtGen/Story/build_story.py              dựng gói (gui_gpt/: luot_k.txt, HUONG_DAN.md)
#       py -3 -I ArtGen/Story/build_story.py --duyet X [ảnh] duyệt X = nv (tờ nhân vật), cd (chân dung) hoặc số khung 1..6 (mặc định
#                                                         ảnh mới nhất trong tai_ve/): chép vào duyet/ rồi dựng lại gói
#       py -3 -I ArtGen/Story/build_story.py --nhap        chép khung và chân dung đã duyệt vào Assets/03 Art/Story, rồi chạy menu
#                                                         Unity "PokiClash/Prefab/Cốt truyện mở đầu (CotTruyen)" và
#                                                         "PokiClash/Prefab/Hướng dẫn người mới (lớp phủ)" để gắn ảnh
import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/Story
ROOT = HERE.parent.parent  # gốc dự án (tính từ chỗ đặt script, hai máy khác ổ)
ARTGEN = HERE.parent
ASSETS = ROOT / "Assets"
PACK = HERE / "gui_gpt"
DL = HERE / "tai_ve"  # GPT lưu ảnh vào đây
OK = HERE / "duyet"  # ảnh đã duyệt
OUT = ASSETS / "03 Art" / "Story"

WORLD_STYLE = ARTGEN / "Islands" / "refs" / "world_style.png"
HEROES = ASSETS / "03 Art" / "Heroes" / "Resources"
ISLANDS = ASSETS / "03 Art" / "Islands"
STARTERS = [  # 5 tướng khởi đầu, dạng 1 (heroes.json "starters")
    ("ti_tach_1", "Ti Tach, a small round water-drop creature with two bubble antennae (Water, blue)"),
    ("quy_lava_1", "a small lava imp with a flame crest, a shield and a short spear (Fire, red)"),
    ("tinh_sat_1", "a small spirit made of shining iron crystals (Metal, silver)"),
    ("tien_la_1", "a small round cactus creature with spines (Wood, green)"),
    ("cong_da_1", "a small armadillo with an amber stone shell (Earth, golden ochre)"),
]
BOSS = HEROES / "nui_lua_1" / "nui_lua_1_portrait.png"  # Hỏa Sơn Long, boss cuối đảo Hỏa

LAND, PORT, SQUARE = (1536, 1024), (1024, 1536), (1024, 1024)

STYLE = (
    "STYLE: hand-drawn storybook art for a vertical mobile game, in exactly the rendering of the reference drawing: bold "
    "dark-brown ink outlines (#2B2118), slightly wobbly like a real pen, colours laid in with coloured pencil and wax crayon on cream "
    "paper, light watercolour washes, chunky cute shapes with clear silhouettes, few small details. Warm, adventurous and a little "
    "mysterious, like a kid's adventure notebook drawn by a professional illustrator. No photorealism, no glossy 3D render, no heavy "
    "gradients, no glow halos, no lens flare.\n"
    "Characters and creatures: flat colour areas with pencil texture, no light-and-shade modelling, no cast shadows, no glossy "
    "highlights, a tiny white catch-light in each eye only.\n"
    "PALETTE: ink #2B2118, paper #FBF4E2, red #E8553F, orange #F39A2D, yellow #F7C948, green #6CBF4F, teal #3FB8A9, blue #4A90D9, "
    "purple #9A6AD6, pink #F07FA6. Element colours: water blue #4A90D9, fire red #E8553F, metal silver #B8C4CF, wood green #6CBF4F, "
    "earth golden ochre #E2A93B."
)
PANEL = (
    "PANEL: one full-bleed illustration that fills the whole canvas edge to edge: no comic border, no frame, no white margin, no "
    "rounded corners (the game adds the paper frame and tape). No text at all: no letters, no captions, no speech bubbles, no sound "
    "effects, no signs with writing, no logos, no watermark."
)
HERO = (
    "THE HERO (the player's character, a boy beast tamer; keep this exact design in every image): a boy of about eleven, drawn "
    "chunky and cute in proportions like the game's creatures (big head, short body), with a brave, determined face and a confident "
    "grin: big bright brown eyes, thick eyebrows, tousled chestnut-brown hair with one stubborn cowlick sticking up on top, a small "
    "plaster on his left cheek. Clothes: a short teal hooded cape (#3FB8A9 with a darker teal hem) fastened at the neck with a round "
    "brass clasp; a red scarf (#E8553F) under it; a cream tunic with rolled-up sleeves; a brown leather strap across his chest holding "
    "five coloured pencils like a bandolier (blue, red, silver, green, golden ochre: the five elements); a brown belt; dark-brown knee "
    "shorts; striped cream-and-teal socks; sturdy brown boots. His two magic tools: a big MAGIC SKETCHBOOK bound in brown leather "
    "with brass corners and a five-pointed star emblem in the five element colours on the cover, hanging from a strap at his hip or "
    "held open in one arm; and an oversized MAGIC PENCIL as long as his forearm, yellow with a red eraser and a small feather charm "
    "tied below the eraser, which he holds like a wand. When he uses magic, swirling coloured-pencil strokes and small doodled stars "
    "fly out of the open sketchbook, drawn as pencil lines (never as glowing light). He befriends and tames creatures by sketching "
    "them in the book. No hat, no cap, no gloves, no backpack."
)

# ảnh lẻ (không phải khung truyện): mã: (cỡ, tên file lưu, câu vẽ)
SHEET = (LAND, "nhan_vat", (
    "WHAT TO DRAW: a character design sheet of THE HERO on plain cream paper (#FBF4E2), no ruled lines, no grid, no labels, no "
    "colour swatches, no text. Left half: the hero full body, front view, standing in a brave ready pose, feet apart, holding the "
    "magic pencil up like a wand in his right hand and the open magic sketchbook in his left arm, a few coloured-pencil strokes and "
    "doodled stars swirling out of the book. Right half: three head-and-shoulders busts of the same boy, same size, in a column: "
    "a confident grin; wide-eyed surprise with mouth open; cheering, fist up, eyes squeezed happily. Between them, small, the closed "
    "sketchbook (cover emblem visible) and the magic pencil lying flat. Every part separated by clear paper space, nothing "
    "overlapping, no shadow under the feet or objects."))
PORTRAIT = (SQUARE, "chan_dung", (
    "WHAT TO DRAW: a head-and-shoulders portrait of THE HERO exactly as on the approved design sheet (image 1), for a speech note in "
    "the game's tutorial. Three-quarter view turned slightly to the right, a confident cheeky grin, one hand raising the magic pencil "
    "beside his face, the red scarf and the teal hood and the top of the pencil bandolier visible, cut off at mid-chest with a "
    "clean edge. The figure fills about 85% of the canvas height, centred. TRANSPARENT BACKGROUND (PNG with alpha): nothing behind "
    "him, no paper, no colour field, no frame, no circle, no shadow, no text. Keep the bold wobbly ink outline all around the figure."))

# khung: (cỡ, tên lượt, câu cảnh) — chữ in trong game nằm ở App/StoryIntro.cs (Caption), GPT không vẽ chữ
PANELS = {
    1: (LAND, "con bao", (
        "SCENE: night at sea in a wild storm. A small wooden sailboat with a patched sail is tossed on huge dark waves (lower left "
        "third). The hero, small and seen from behind, clings to the mast with one arm and hugs his magic sketchbook with the "
        "other; the book has flown open and its pages flutter. Above, the storm clouds twist into a giant spiral (upper right) "
        "drawn as huge swirling coloured-pencil strokes in five colours (blue, red, silver, green, golden ochre), like a doorway to "
        "another world, pulling the boat up in a ribbon of spray. Two jagged lightning bolts. Deep navy and purple flat colours with "
        "crayon hatching, white wave scribbles. Dramatic but cosy, not scary.")),
    2: (PORT, "tinh day", (
        "SCENE: bright morning on the white-sand beach of a strange island. Bottom part: calm turquoise sea and the broken sailboat "
        "lying on its side at the waterline, its sail torn. Middle: the hero sits up in the sand beside the boat, one hand still "
        "gripping the magic pencil, staring up in surprise; his magic sketchbook lies open in the sand next to him. Beside him, a "
        "trail of huge three-toed creature footprints runs up the beach into the jungle. Top part: an amazing jungle unlike ours: "
        "giant curly ferns, palm trees, enormous mushrooms with soft blue caps, trees bearing crystal fruits, vines, and a few small "
        "mysterious eyes peeking from the dark between the leaves.")),
    3: (PORT, "rung suong", (
        "SCENE: a dim misty jungle seen over the hero's shoulder (his teal hood, red scarf and the pencils of his bandolier in the "
        "bottom corner, from behind; he holds the magic pencil ready). Between giant leaves, roots and stones, five mysterious "
        "creatures peek out, only partly visible, each in its element colour: a pair of round glowing eyes above a flickering flame "
        "tail; a shy creature made of shining silver crystals behind a rock; a leafy creature hiding among ferns, only its eyes "
        "showing; a round mossy rock that is actually a creature with two eyes; a watery creature rising from a puddle. Mysterious "
        "and a little spooky, but cute. Cool green and teal mist in flat bands, crayon texture.")),
    4: (PORT, "ban moi", (
        "SCENE: a sunny jungle clearing. The hero stands in the middle, seen in three-quarter view, holding his magic sketchbook "
        "open toward the viewer with one arm and sketching with the magic pencil; coloured-pencil strokes and doodled stars swirl out "
        "of the pages. Around him, in a friendly semicircle, the five little creatures of images 3 to 7 step out of the bushes, "
        "curious and brave, each drawn with exactly the shape, colours and details of its reference image (ignore the references' "
        "white outline and background): {starters}. They look ready for adventure, a little cheeky, not shy.")),
    5: (PORT, "chua te", (
        "SCENE: dusk on a cliff edge. Bottom of the panel: the hero and the five little creatures, small and seen from behind, look "
        "out across the sea; the hero's cape flutters and he grips the magic pencil. Far away in the middle of the panel rises a "
        "volcanic island; on top of the volcano a gigantic island lord roars: the dragon-dinosaur of image 8, drawn huge as a dark "
        "silhouette in its shape with glowing yellow eyes, lava flowing down the volcano, smoke rising. Stormy orange and purple sky "
        "in flat bands. Dramatic and awe-inspiring, not gory, not too scary.")),
    6: (LAND, "len duong", (
        "SCENE: a wide panorama at sunrise over a calm sea. Across the background, five islands of the five elements in the look of "
        "image 9: a water island with palm trees and a lighthouse, a fire island with a smoking volcano, a metal island with snowy "
        "peaks and a golden bell tower, a wood island with one gigantic tree, an earth island with a stepped stone temple; each "
        "island is half-veiled by grey storm clouds. In the foreground, the repaired sailboat with a fresh striped sail heads "
        "toward them, leaving a white wake; the hero stands at the bow pointing forward with his magic pencil, cape flying, the "
        "sketchbook at his hip, and the five little creatures cheer on the deck. Hopeful and adventurous.")),
}

# lượt: danh sách việc ("nv" tờ nhân vật, "cd" chân dung, số = khung)
TURNS = {0: ["nv"], 1: ["cd", 2], 2: [1, 3], 3: [4, 5, 6]}


def item(x):
    """(cỡ, tên file lưu không đuôi, câu vẽ, tên hiện)"""
    if x == "nv":
        return SHEET[0], SHEET[1], SHEET[2], "hero design sheet"
    if x == "cd":
        return PORTRAIT[0], PORTRAIT[1], PORTRAIT[2], "hero portrait"
    size, _, scene = PANELS[x]
    starters = "; ".join(f"image {i + 3} = {t}" for i, (_, t) in enumerate(STARTERS))
    return size, f"khung_{x}", scene.replace("{starters}", starters), f"panel {x}"


def key(x):
    return {"nv": "nhan_vat", "cd": "chan_dung"}.get(x, f"khung_{x}")


def latest(x):
    files = sorted(DL.glob(f"{key(x)}*.png"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def save_path(x):
    return DL / f"{key(x)}.png"


def approved(x):
    return OK / f"{key(x)}.png"


def refs(turn):
    style = (WORLD_STYLE, "the game's approved hand-drawn map: copy its RENDERING (wobbly dark-brown ink outlines, coloured-pencil "
                          "and crayon hatching on cream paper, chunky cute doodles), ignore its content")
    if turn == 0:
        return [style, (HEROES / "ti_tach_1" / "ti_tach_1_portrait.png",
                        "one of the game's creatures: match its chunky cute proportions and flat colouring for the boy (ignore "
                        "its white outline and background)")]
    sheet = (approved("nv"), "the approved design sheet of THE HERO: draw the boy, his clothes, magic sketchbook and magic pencil "
                             "EXACTLY like this (same face, hair, cape, scarf, bandolier, colours)")
    if turn == 1:
        return [sheet, style, (ISLANDS / "sanh_dao_thuy.png", "the game's Water island: copy the look of its palm trees, sand, "
                                                              "rocks and turquoise sea for panel 2; ignore its layout")]
    r = [(approved(2), "the approved panel 2 of this same story: copy its exact rendering, line weight and colours"), sheet]
    if turn == 3:
        for aola, text in STARTERS:
            r.append((HEROES / aola / f"{aola}_portrait.png", f"one of the five little creatures: {text}"))
        r.append((BOSS, "the island lord of the fire island, a huge dragon-dinosaur: use only its shape for the silhouette in panel 5"))
        r.append((ISLANDS / "world.png", "the game's world map of the five element islands: copy the look of each island for panel 6"))
    return r


def prompt(turn):
    xs = TURNS[turn]
    rs = refs(turn)
    if turn == 3:  # ảnh tướng là image 3..7 trong câu khung 4: kiểm thứ tự
        assert rs[2][0].name.startswith(STARTERS[0][0])
    head = ("Read this whole file. Then open the reference images listed below from their full paths, draw "
            + ("ONE image" if len(xs) == 1 else f"{len(xs)} images, one after another (one image per step)")
            + " and save each as described under SAVE. Do not reply with text only.\n\n"
            "REFERENCE IMAGES (open each file from its full path):\n")
    head += "".join(f"image {i + 1} = {p}: {t}\n" for i, (p, t) in enumerate(rs))
    head += "\nSAVE:\n"
    for x in xs:
        size, name, _, label = item(x)
        head += f"- {label}: a {size[0]} x {size[1]} PNG saved to\n  {save_path(x)}\n"
    head += ("Create the folder if it is missing. If a file already exists, save it with _2, _3 … added before .png (for example "
             f"{key(xs[0])}_2.png) in the same folder instead. Do not change, move or delete any other file.\n\n")
    head += ("WHAT THIS IS: art for the opening comic of a hand-drawn mobile pet-battle adventure game, shown the first time the game "
             "starts. Two pages, six panels: a boy beast tamer with a magic sketchbook is swept by a storm into a strange world full "
             "of mysterious creatures, makes five little creature friends, and sets off to conquer five islands ruled by giant "
             "island lords. The panels appear one by one when the player taps. The game prints a few words on paper strips over the "
             "panels, so the art must have no text. The boy is the player's character and also appears in the tutorial.\n\n")
    head += STYLE + "\n\n" + HERO + "\n\n"
    if any(isinstance(x, int) for x in xs):
        head += PANEL + "\n\n"
    for n, x in enumerate(xs):
        size, _, text, label = item(x)
        orient = "landscape" if size[0] > size[1] else "portrait" if size[0] < size[1] else "square"
        head += f"STEP {n + 1}: {label.upper()} ({orient} {size[0]} x {size[1]})\n{text}\n"
        if isinstance(x, int):
            head += "Keep the important things away from the outer 6% of the canvas (the frame may crop a little).\n"
        head += f"Save it to {save_path(x)}\n\n"
    head += "Remember: no text in the images, and save every image to its path under SAVE."
    return head


GUIDE_REF = {
    WORLD_STYLE.name: "bản đồ vẽ tay mẫu của game (1024 x 1536, nền giấy kem): chỉ lấy nét vẽ (viền mực nâu rung, chì màu, sáp)",
    "ti_tach_1_portrait.png": "chân dung Tí Tách (nền trong suốt): lấy tỉ lệ mập, dễ thương và lối tô phẳng cho cậu bé",
    "nhan_vat.png": "tờ thiết kế nhân vật chính đã duyệt (1536 x 1024): khoá hình cậu bé, sổ phép, bút chì phép",
    "sanh_dao_thuy.png": "đảo Thủy trên bản đồ sảnh (nền trong suốt): lấy dáng cây dừa, cát, đá, biển xanh ngọc",
    "khung_2.png": "khung 2 đã duyệt (1024 x 1536): khoá nét vẽ truyện cho các khung sau",
    "world.png": "bản đồ thế giới năm đảo của sảnh (1480 x 2320): lấy dáng từng đảo cho khung 6",
    "nui_lua_1_portrait.png": "chân dung Hỏa Sơn Long, boss cuối đảo Hỏa (nền trong suốt): chỉ lấy dáng cho bóng chúa tể ở khung 5",
}
GUIDE_TITLE = {"nv": "tờ thiết kế nhân vật chính (ngang)", "cd": "chân dung bán thân, nền trong suốt (vuông)",
               1: "cơn bão (ngang)", 2: "tỉnh dậy trên bãi biển lạ (dọc)", 3: "rừng sương, sinh vật kỳ bí (dọc)",
               4: "năm người bạn mới (dọc)", 5: "chúa tể đảo lửa (dọc)", 6: "năm đảo, lên đường (ngang)"}
WAIT = {1: "chờ duyệt tờ nhân vật (--duyet nv)", 2: "chờ duyệt khung 2 (--duyet 2)", 3: "chờ duyệt khung 2 (--duyet 2)"}


def guide(ready):
    lines = ["# Cốt truyện mở đầu: gói gửi GPT", "",
             "Đoạn truyện tranh 2 trang, 6 khung chạy lần đầu vào game (trước màn tải con tàu). Chạm một lần hiện một khung; chữ do game "
             "in, GPT không vẽ chữ. Mỗi lượt bạn chỉ gửi GPT **đường dẫn file prompt**; GPT tự mở ảnh mẫu và tự lưu ảnh.", "",
             "**Nhân vật chính** (người chơi): cậu bé thuần thú sư khoảng 11 tuổi, tóc nâu hạt dẻ có một chỏm dựng, băng cá nhân trên má "
             "trái, áo choàng ngắn có mũ màu xanh mòng két cài khuy đồng, khăn đỏ, áo kem xắn tay, dây chéo ngực cài 5 cây bút chì 5 "
             "màu hệ, quần soóc nâu, tất sọc, ủng nâu. Cầm **sổ phép** bìa da nâu góc đồng, ngôi sao 5 màu trên bìa, và **bút chì phép** "
             "to cỡ cẳng tay (thân vàng, tẩy đỏ, buộc lông vũ) dùng như đũa phép. Thuần phục sinh vật bằng cách vẽ chúng vào sổ. Cũng "
             "nói vài lời dẫn trong hướng dẫn người mới (chân dung bán thân).", "",
             "| Trang | Khung | Nội dung | Chữ game in |", "|---|---|---|---|"]
    caps = {1: "Một đêm giông bão...", 2: "Tỉnh dậy ở một thế giới lạ.", 3: "", 4: "Những người bạn mới.", 5: "Mỗi đảo một chúa tể.",
            6: "Đi chinh phục thôi!"}
    for k in range(1, 7):
        lines.append(f"| {1 if k <= 3 else 2} | {k} | {GUIDE_TITLE[k]} | {caps[k] or '(không chữ)'} |")
    lines += ["", "## Các lượt", ""]
    for t, xs in TURNS.items():
        f = PACK / f"luot_{t}.txt"
        title = ", ".join(GUIDE_TITLE[x] for x in xs)
        if t in ready:
            lines.append(f"### Lượt {t}: {title}")
            lines.append(f"- Gửi GPT: `{f}`")
            lines.append("- Ảnh mẫu trong file:")
            for i, (p, _) in enumerate(refs(t)):
                desc = GUIDE_REF.get(p.name) or "chân dung tướng khởi đầu dạng 1 (nền trong suốt)"
                lines.append(f"  - image {i + 1} = `{p}`: {desc}")
            for x in xs:
                size = item(x)[0]
                lines.append(f"- Lưu: `{save_path(x)}` ({size[0]} x {size[1]})")
        else:
            lines.append(f"### Lượt {t}: {title} (chưa dựng: {WAIT[t]})")
        lines.append("")
    lines += ["## Kiểm", "",
              "- Tờ nhân vật: cậu bé trai mập, dễ thương, mặt quả quyết; đủ áo choàng xanh mòng két, khăn đỏ, dây 5 bút chì, sổ phép, "
              "bút chì phép; không mũ, không ba lô; không chữ, không ô màu, không bóng dưới chân.",
              "- Chân dung: nền trong suốt thật (không giấy, không khung tròn), cắt ngang giữa ngực, viền mực quanh hình.",
              "- Khung truyện: tràn kín khung, không viền, không chữ, không bóng loáng hay quầng sáng; phép thuật là nét chì màu, không "
              "phát sáng.",
              "- Nét viền mực nâu rung, tô chì màu và sáp như bản đồ mẫu; nhân vật tô phẳng, không mảng sáng tối.",
              "- Cậu bé cùng một hình ở mọi khung (so với tờ nhân vật).",
              "- Khung 4: năm bạn nhỏ đúng dáng năm tướng khởi đầu. Khung 5: chúa tể chỉ là bóng to mắt vàng.",
              "", "## Câu sửa nhanh (gửi GPT kèm ảnh vừa vẽ)", "",
              "- `Redraw it full-bleed: remove the border and the white margin.`",
              "- `Remove all text, letters, labels and speech bubbles.`",
              "- `Make the outlines bolder and more wobbly, with crayon texture like the reference map; flat colours, no shading.`",
              "- `Draw the boy exactly like on the design sheet (teal hooded cape, red scarf, pencil bandolier, sketchbook, magic pencil).`",
              "- `Make the background fully transparent: remove the paper and any circle behind him.`",
              "", "## Sau khi GPT lưu ảnh", "",
              "- Duyệt tờ nhân vật: `py -3 -I ArtGen/Story/build_story.py --duyet nv` → lượt 1 được dựng.",
              "- Duyệt chân dung: `--duyet cd`. Duyệt khung k: `--duyet k` (lấy ảnh mới nhất trong `tai_ve/`).",
              "- Duyệt khung 2 thì lượt 2, 3 được dựng.",
              "- Có ảnh duyệt: `py -3 -I ArtGen/Story/build_story.py --nhap`, rồi menu Unity `PokiClash/Prefab/Cốt truyện mở đầu "
              "(CotTruyen)` (khung) và `PokiClash/Prefab/Hướng dẫn người mới (lớp phủ)` (chân dung)."]
    return "\n".join(lines) + "\n"


def build():
    PACK.mkdir(parents=True, exist_ok=True)
    DL.mkdir(parents=True, exist_ok=True)
    OK.mkdir(parents=True, exist_ok=True)
    ready = [0]
    if approved("nv").exists():
        ready.append(1)
        if approved(2).exists():
            ready += [2, 3]
    for t in TURNS:
        f = PACK / f"luot_{t}.txt"
        if t in ready:
            missing = [str(p) for p, _ in refs(t) if not p.exists()]
            if missing:
                print("Thiếu ảnh mẫu:", *missing, sep="\n  ")
            f.write_text(prompt(t), encoding="utf-8")
        elif f.exists():
            f.unlink()  # lượt chưa đủ ảnh mẫu: bỏ file cũ (chính script sinh ra)
    (PACK / "HUONG_DAN.md").write_text(guide(ready), encoding="utf-8")
    print("Đã dựng gói:", PACK)
    for t in ready:
        print(f"  lượt {t}: {PACK / f'luot_{t}.txt'}")


def approve(x, src):
    src = Path(src) if src else latest(x)
    if not src or not src.exists():
        sys.exit(f"Không thấy ảnh {key(x)} trong {DL}")
    OK.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, approved(x))
    print(f"Đã duyệt {key(x)}: {src.name}")
    build()


def import_unity():
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for k in PANELS:
        src = approved(k)
        if not src.exists():
            print(f"  khung {k}: chưa duyệt")
            continue
        im = Image.open(src).convert("RGB")
        s = 1024 / max(im.size)
        if s < 1:
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(OUT / f"khung_{k}.png", optimize=True)
        n += 1
    src = approved("cd")
    if src.exists():
        im = Image.open(src).convert("RGBA")
        box = im.getchannel("A").getbbox()  # cắt sát hình (giữ 8 px lề)
        if box:
            l, t, r, b = box
            im = im.crop((max(0, l - 8), max(0, t - 8), min(im.width, r + 8), min(im.height, b + 8)))
        s = 512 / max(im.size)
        if s < 1:
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(OUT / "nhan_vat.png", optimize=True)
        print("  chân dung: nhan_vat.png")
    else:
        print("  chân dung: chưa duyệt")
    print(f"Đã chép {n} khung vào {OUT}. Chạy menu Unity 'PokiClash/Prefab/Cốt truyện mở đầu (CotTruyen)' và "
          "'PokiClash/Prefab/Hướng dẫn người mới (lớp phủ)' để gắn ảnh.")


def parse(x):
    return int(x) if x.isdigit() else x


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar=("X", "ANH"), help="nv | cd | 1..6 [đường dẫn ảnh]")
    ap.add_argument("--nhap", action="store_true")
    a = ap.parse_args()
    if a.duyet:
        x = parse(a.duyet[0])
        if x not in ("nv", "cd") and x not in PANELS:
            sys.exit("X phải là nv, cd hoặc 1..6")
        approve(x, a.duyet[1] if len(a.duyet) > 1 else None)
    elif a.nhap:
        import_unity()
    else:
        build()
