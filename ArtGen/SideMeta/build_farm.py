"""Gói gửi GPT cho cảnh Trang trại (người dùng dặn 2026-11-10: trang trại là một cảnh thật, thú thả đi lại, mỗi khu một việc).

Sinh vào ArtGen/SideMeta/gui_gpt/farm/:
- bo_cuc_farm.png: sơ đồ bố cục 1024 x 1536 (khu, chỗ đứng đánh số, bãi cỏ thả thú, đống rơm chỗ ngủ);
- luot_1_nen.txt: nền trang trại theo sơ đồ (lưu ArtGen/SideMeta/farm/tai_ve/farm_bg.png);
- luot_2_do_vat.txt: tấm 4 x 3 đồ nghề và hạt hiệu ứng nền trắng (lưu ArtGen/SideMeta/farm/tai_ve/farm_props.png);
- HUONG_DAN.md cho người dùng.

Toạ độ chỗ đứng (SPOTS) trùng balance.json farm.spots (x, y theo tỉ lệ ảnh) và menu Unity
"PokiClash/Prefab/Trang trại: cảnh thật" (Editor/FarmSceneMenu.cs). Đổi ở đây thì đổi cả hai chỗ đó.

    python -I ArtGen/SideMeta/build_farm.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(HERE, "gui_gpt", "farm")
SAVE_DIR = os.path.join(HERE, "farm", "tai_ve")
W, H = 1024, 1536

# chỗ đứng làm việc (thứ tự như balance.json farm.spots), px trên ảnh 1024 x 1536 (gốc trên trái)
SPOTS = [
    ("duck1", 640, 700), ("veg1", 200, 1200), ("orchard1", 190, 700), ("bakery", 800, 1250),
    ("smithy", 850, 960), ("duck2", 820, 690), ("veg2", 380, 1200), ("orchard2", 360, 700),
]
# khu (màu sơ đồ, hình): ellipse (cx, cy, rx, ry) hoặc rect (x0, y0, x1, y1)
ZONES = [
    ("pond", "#5aa9e6", "ellipse", (730, 560, 200, 115)),
    ("orchard_trees", "#3f8f33", "rect", (100, 440, 450, 600)),
    ("orchard_grass", "#a6d98a", "rect", (100, 600, 450, 760)),
    ("meadow", "#c8eaa0", "ellipse", (512, 905, 225, 125)),
    ("hay", "#e8c35a", "rect", (110, 860, 270, 1010)),
    ("shed", "#9a9a9a", "rect", (790, 770, 950, 890)),
    ("shed_yard", "#d8c9a8", "rect", (770, 890, 950, 1030)),
    ("oven", "#c0623a", "rect", (730, 1070, 890, 1170)),
    ("oven_yard", "#d8c9a8", "rect", (700, 1170, 920, 1310)),
    ("field", "#8a5a34", "rect", (100, 1090, 480, 1300)),
    ("barn", "#c84a3a", "rect", (110, 170, 390, 390)),
    ("windmill", "#b08860", "rect", (760, 150, 900, 400)),
]
PATH = [(512, 1536), (512, 1350), (520, 1180), (512, 1030), (512, 780), (560, 720), (520, 420), (300, 400)]


def sketch(path):
    img = Image.new("RGB", (W, H), "#9fd27c")
    d = ImageDraw.Draw(img)
    d.line(PATH, fill="#f1dfb0", width=70, joint="curve")
    for name, col, shape, r in ZONES:
        if shape == "ellipse":
            cx, cy, rx, ry = r
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=col, outline="#2b2118", width=4)
        else:
            d.rectangle(r, fill=col, outline="#2b2118", width=4)
        if name == "field":
            for y in range(r[1] + 25, r[3], 40):
                d.line((r[0] + 12, y, r[2] - 12, y), fill="#5e3a1e", width=8)
    try:
        font = ImageFont.truetype("arialbd.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    for i, (_, x, y) in enumerate(SPOTS):
        d.ellipse((x - 62, y - 30, x + 62, y + 30), fill="#fff6d8", outline="#2b2118", width=4)
        d.text((x, y), str(i + 1), fill="#2b2118", font=font, anchor="mm")
    # dải an toàn: trên 8 %, dưới 12 % (UI che), hai bên 80 px (bị cắt khi khung rộng)
    for y0, y1 in ((0, int(H * 0.08)), (int(H * 0.88), H)):
        d.rectangle((0, y0, W, y1), outline="#ff3b8d", width=5)
    for x in (80, W - 80):
        d.line((x, 0, x, H), fill="#ff3b8d", width=3)
    img.save(path)


STYLE = ("hand-drawn storybook cartoon for a vertical mobile game: bold dark-brown ink outlines (#2B2118), slightly wobbly "
         "like a real pen, coloured-pencil and crayon hatching that stays visible, flat warm colours with light watercolour "
         "washes, subtle cream paper grain. Cozy, cheerful, chunky cute shapes, drawn beautifully, not scribbly, no glossy "
         "digital rendering, no photorealism, no heavy gradients")


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.strip() + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SAVE_DIR, exist_ok=True)
    layout = os.path.join(OUT, "bo_cuc_farm.png")
    sketch(layout)
    style_ref = os.path.join(ART, "Islands", "refs", "world_style.png")
    grid_ref = os.path.join(ART, "guides", "G_Sheet4x3.png")
    bg_save = os.path.join(SAVE_DIR, "farm_bg.png")
    props_save = os.path.join(SAVE_DIR, "farm_props.png")
    for p in (style_ref, grid_ref):
        if not os.path.exists(p):
            sys.exit("Thiếu ảnh mẫu: " + p)

    write(os.path.join(OUT, "luot_1_nen.txt"), f"""
Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as described under SAVE. Do not reply with text only.

REFERENCE IMAGES (open each file from its full path; both are 1024 x 1536):
image 1 = {style_ref}: the game's approved hand-drawn map: copy its RENDERING (wobbly dark-brown ink outlines, coloured-pencil hatching on cream paper, chunky cute doodles), ignore its content
image 2 = {layout}: the layout sketch of the image you draw now: follow it exactly

SAVE: the finished image is 1024 x 1536; save it as a PNG to {bg_save}
Create the folder if it is missing. If that file already exists, save it as farm_bg_2.png, farm_bg_3.png … in the same folder instead. Do not change, move or delete any other file.

WHAT THIS IS: the full-screen background of the FARM scene of a vertical mobile monster-pet game, seen from a high three-quarter top-down view, like the map in image 1. The player's pet creatures will walk around on it and work at the farm's work stations; the game draws the creatures, the signs and every marker itself. So draw NO creatures, NO animals, NO people, NO text, NO signs with writing, NO UI.

STYLE: {STYLE}. Same rendering as image 1, outlines and hatching as bold as in image 1.

LAYOUT: copy image 2 exactly: every area on the same place with the same size. The sketch is only a colour-coded plan; do not copy its flat colours, its numbers, its pink guide lines or its black outlines. Legend of the sketch:
- light green = grass ground of the farm; pale sand band = a dirt footpath winding from the bottom edge up to the barn;
- red block top-left = a big red wooden barn with a white-trimmed door and a hay loft; tan block top-right = a wooden windmill with four sails;
- blue oval = the DUCK POND: clear blue water with a few reeds and lily pads at its back and sides, a flat pale sandy bank along its whole front (bottom) edge;
- dark green block = the ORCHARD: a row of three round fruit trees with red apples, standing at the back; light green block below it = the orchard's open lawn;
- big pale green oval in the centre = the PET MEADOW: a soft, short, even lawn with a low wooden rail fence along its back half only, open at the front, a few tiny flowers on its rim; keep its inside completely empty and flat (the pets roam there);
- yellow block on the left = two round haystacks and a little straw bed (the pets nap there); keep the straw bed in front of the haystacks flat and empty;
- grey block on the right = the TOOL WORKSHOP: a small open wooden shed with an anvil, a tool rack and a barrel at its back; beige block below it = its flat packed-earth yard;
- orange-red block on the lower right = the BREAD OVEN: a round clay dome oven with a little chimney and a stack of firewood; beige block below it = its flat packed-earth yard;
- brown block with stripes on the lower left = the VEGETABLE FIELD: neat tilled soil rows with young green sprouts, carrots and cabbages, a low fence around it;
- the eight cream ovals with numbers = WORK SPOTS where the game stands a creature (about 125 x 60 px each): draw each as plain flat ground of the area it sits in (sandy bank, lawn, packed earth, a bare soil row), completely EMPTY: no tree, rock, plant, tool, prop or marker on it, nothing standing in front of it.

DEPTH AND DETAIL: things further up are further away; trees, the barn and the windmill overlap the ground behind them naturally. Between the areas: grass tufts, little flower clusters, a few stones, short wooden fences, a wheelbarrow, a water trough, a mailbox by the path. Dense and lively, but every area and every work spot stays clear and readable.

EDGES: the land runs off all four edges (no island outline, no sea). Keep the top 8 % (above the upper pink line) calm: sky-blue distance with soft hills and treetops only. Keep the bottom 12 % (below the lower pink line) calm: grass, the start of the path, a few flowers. The 80 px on the far left and far right (outside the pink vertical lines) may be cut off on some phones: put only trees and bushes there.

LIGHT: soft daylight from the top-left; light pencil shading under trees and buildings is fine. Do not paint any creature shadow on the work spots or the meadow.
""")

    write(os.path.join(OUT, "luot_2_do_vat.txt"), f"""
Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as described under SAVE. Do not reply with text only.

REFERENCE IMAGES (open each file from its full path):
image 1 = {style_ref}: the game's approved hand-drawn map (1024 x 1536): copy its RENDERING (wobbly dark-brown ink outlines, coloured-pencil hatching on cream paper, chunky cute doodles), ignore its content
image 2 = {grid_ref}: a 4 x 3 numbered grid guide (1536 x 1024): put one item in the centre of each cell, in the numbered order; do not copy the grid lines or numbers

SAVE: the finished image is 1536 x 1024; save it as a PNG to {props_save}
Create the folder if it is missing. If that file already exists, save it as farm_props_2.png, farm_props_3.png … in the same folder instead. Do not change, move or delete any other file.

WHAT THIS IS: a sheet of 12 separate small farm tools and effect sprites for the FARM scene of a vertical mobile monster-pet game. The game cuts each cell out and has the pet creatures hold or use the tools while they work.

STYLE: {STYLE}.
NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the items or on the background. Shade only with colour-pencil hatching inside the shapes.

BACKGROUND: pure flat white (#FFFFFF) everywhere between the items, no paper texture, no grid, no frame. Each item sits alone in the middle of its cell, about 230 px on its longest side, at least 40 px of white around it, nothing touching another cell.

THE 12 ITEMS (left to right, top row first):
1. a garden hoe, drawn diagonally, wooden handle from lower left to the metal blade at upper right;
2. a green watering can seen from the side, spout pointing right;
3. a woven wicker basket full of red apples;
4. a round golden loaf of bread with a scored top;
5. a blacksmith hammer, drawn diagonally, wooden handle from lower left to the iron head at upper right;
6. a small cloth sack of grain, open at the top, a few grains spilling;
7. one red apple with a leaf;
8. one orange carrot with green leaves;
9. a puff of brown dust (three round cartoon clouds);
10. a small burst of yellow-orange sparks (five short spiky rays and three dots);
11. a soft grey-white puff of smoke (round cartoon cloud);
12. a pink cartoon heart.
""")

    write(os.path.join(OUT, "HUONG_DAN.md"), f"""
# Trang trại: gói gửi GPT

Mỗi lượt gửi GPT (hoặc Codex) **đường dẫn một file prompt**; GPT tự mở ảnh mẫu và tự lưu ảnh.

| Lượt | File prompt | Ảnh lưu vào |
|---|---|---|
| 1 | `{os.path.join(OUT, 'luot_1_nen.txt')}` | `{bg_save}` |
| 2 | `{os.path.join(OUT, 'luot_2_do_vat.txt')}` | `{props_save}` |

Hai lượt độc lập, làm lượt nào trước cũng được.

## Ảnh mẫu

- `world_style.png` (1024 × 1536, nền giấy kem): bản đồ đảo vẽ tay đã duyệt, chỉ lấy nét (viền mực nâu hơi rung, chì màu gạch chéo).
- `bo_cuc_farm.png` (1024 × 1536, nền xanh cỏ): sơ đồ bố cục: chuồng đỏ trên trái, cối xay gió trên phải, ao xanh dương, vườn cây xanh đậm,
  bãi cỏ thả thú (bầu dục xanh nhạt ở giữa), đống rơm vàng (chỗ thú ngủ), xưởng xám, lò bánh cam, ruộng nâu sọc; 8 ô kem đánh số là chỗ
  tướng đứng làm việc; đường hồng là dải an toàn (trên 8 %, dưới 12 % bị UI che; 80 px hai bên có máy cắt mất).
- `G_Sheet4x3.png` (1536 × 1024): lưới 4 × 3 đánh số cho tấm đồ nghề.

## Cách kiểm

- **Nền:** đúng chỗ từng khu như sơ đồ; 8 chỗ đứng là đất phẳng trống (không cây, đá, đồ đạc); bãi cỏ giữa trống; không vẽ con vật, người,
  chữ; trên và dưới yên (trời, cỏ).
- **Đồ nghề:** 12 món đúng thứ tự, mỗi món một ô, nền trắng phẳng, không bóng đổ.

## Câu sửa nhanh

- `Same farm; keep the eight work spots and the centre meadow completely empty and flat, follow the layout sketch more exactly.`
- `Same farm; no animals or creatures anywhere, no text.`
- `Same sheet; pure white background, no shadows, one item per cell in the numbered order.`
""")
    print("Đã sinh", OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
