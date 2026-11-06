# Bản đồ dài đảo Thổ 70 ải: dựng ảnh bố cục và gói gửi GPT, như build_zone70_kim.py (đảo Kim). Dùng lại phần chung của
# build_zone70.py (đường chữ S, cỡ bản đồ 1024 x 4288 ghép 3 đoạn, chỗ địa danh), band_offset của build_zone70_moc.py và va_noi của
# build_zone70_kim.py; không sửa các file đó.
# Khác đảo Kim:
# - đường lượn sang phải trước (như đảo Thủy, Hỏa; ngược đảo Kim), cùng độ cao 10 ải tướng;
# - không có sông: hẻm núi khô chạy ngang hết bề ngang ngay sau bãi ải 5, đường qua cầu treo gỗ (không gắn với chặng nào, chặng 2
#   Hang Lửng có địa danh riêng); hồ nước dưới gốc sồi cổ thụ, lạch nước ra mép (chặng 6, Rừng Sồi Già); kim tự tháp bậc có đền
#   mái vàng đứng sau bãi đấu boss, đỉnh chạm dải biển trên;
# - nền vàng đất đậm hơn hẳn mặt đường cát kem (đường dò theo màu cát nhạt, sand_mask);
# - ảnh mẫu nét là đoạn 1 bản đồ dài đảo Mộc đã duyệt (như đảo Hỏa, Kim), màu và đồ vật lấy bản đồ Thổ 8 ải cũ;
# - khói, bụi, lửa, lấp lánh, quầng sáng không vẽ: game có sẵn phần động smoke, sparkle, gợn, sóng (IslandAnim).
# Tên chặng theo IslandGen.Tho (Assets/01 Script/Editor/IslandGen.cs).
# Ghi: ArtGen/guides/L_zone70_tho.png (bố cục cả bản đồ), ArtGen/guides/zone70_tho.json (đường, ải tướng, địa danh, cầu; toạ độ
# 0..1 của bản đồ ghép, y từ trên), gói ArtGen/Islands/gui_gpt/zone_tho_70/ (luot_k.txt, bo_cuc_k.png, HUONG_DAN.md).
# Chạy: py -3 -I ArtGen/Islands/build_zone70_tho.py
# Duyệt đoạn k GPT đã lưu: --duyet k [ảnh] (mặc định ảnh mới nhất zones/tho70/tai_ve/doan_k*.png): lưu zones/tho70/doan_k.png rồi
# dựng lại gói (có đoạn k thì có file prompt lượt k+1, bố cục đoạn k+1 dán dải đỉnh của đoạn k). k >= 2 tự sửa chỗ nối như đảo Kim.
# Đủ 3 đoạn: --ghep (zones/tho70/zone_tho70.png). Dò đường thật và đưa vào game (--that, --xuat như đảo Kim) viết khi có bản đồ
# ghép, vì phải đo tay địa danh trên ảnh thật.
import argparse
import contextlib
import io
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent  # ArtGen/Islands
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import build_zone70 as z  # noqa: E402  (phần chung)
import build_zone70_moc as m  # noqa: E402  (band_offset)
import build_zone70_kim as kim  # noqa: E402  (va_noi; lúc nạp hai file trên đặt z.FIRST = -1 nên đặt lại ngay dưới)

z.FIRST = 1  # chặng đầu lượn sang phải

W, SH, H, OV, NSEG = z.W, z.SH, z.H, z.OV, z.NSEG
GUIDES = z.GUIDES
PACK = HERE / "gui_gpt" / "zone_tho_70"
WORK = HERE / "zones" / "tho70"  # tai_ve/: ảnh GPT trả về; doan_k.png: đoạn đã duyệt
STYLE = HERE / "zones" / "moc70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Mộc đã duyệt
OLD = HERE / "zones" / "zone_tho.png"  # bản đồ Thổ 8 ải đang dùng

POND, BOSS = 6, 10
GORGE_AT = 1  # hẻm núi sau bãi ải tướng thứ mấy (0 = ải 1, 1 = ải 5)
AFTER = 150  # cầu cách tâm bãi đó bao nhiêu px đường (về phía ải 10)
GORGE_W = 60  # bề rộng hẻm núi trên ảnh bố cục

# màu ảnh bố cục (chỉ là mã màu cho GPT): đất vàng đất, hẻm núi nâu sẫm, kim tự tháp xám đá, cầu gỗ
GROUND = (226, 178, 96)
CANYON = (96, 52, 32)
PYRAMID = (112, 106, 116)
WOOD = (176, 122, 58)

# địa danh từng chặng: tên chặng (IslandGen.Tho), kiểu chỗ (land xám, water hồ nước, boss kim tự tháp sau bãi đấu), bán kính,
# câu cho GPT
SPOTS = {
    1: ("Bãi Đá Cuội", "land", 100, "a pebble beach beside the start of the road: heaps of big smooth round pebbles and boulders in "
                                    "grey, beige and rusty red, a tall cairn of balanced flat stones, a big spiral seashell "
                                    "half-buried in the sand and a bleached driftwood log"),
    2: ("Hang Lửng", "land", 105, "a badger den: a low grassy earth mound with a big round burrow entrance framed by thick roots and "
                                  "two wooden props, heaps of fresh dug-out dirt, a pickaxe and a shovel leaning on the mound and a "
                                  "few small gold nuggets on the dirt; the den is empty"),
    3: ("Đồi Ngọc Lục", "land", 105, "a small round hill of ochre rock with big clusters of emerald-green crystals sticking out of "
                                     "its sides and top (flat colours, no shine)"),
    4: ("Mỏ Pha Lê", "land", 105, "a crystal mine: a cave entrance with heavy wooden beams in an ochre rock hill, clusters of pink "
                                  "and lilac crystals around the entrance, a wooden wheelbarrow full of pink crystals and a big "
                                  "spiral drill bit lying on the ground"),
    5: ("Đền Phù Văn", "land", 110, "a rune shrine: a ring of tall grey standing stones on a round stone platform around a flat altar "
                                    "stone; the stones are carved with simple spirals, zigzags and dots (ornaments, not letters)"),
    6: ("Rừng Sồi Già", "water", 110, "a round pond at the foot of a huge old oak: the oak stands on the bank at the back of the pond "
                                      "with a thick gnarled trunk, big roots reaching into the water and a wide round crown of dark "
                                      "olive-green leaves; acorns and chestnuts on the bank, two or three smaller oaks around; a "
                                      "small stream leaves the pond and runs off the {edge} edge"),
    7: ("Ruộng Bậc Thang", "land", 115, "a round hill of farm terraces: five or six stepped green fields curving around the hill, "
                                        "each step edged with a thin earth wall, a small straw-roofed field hut on the top step and a "
                                        "few haystacks at the foot"),
    8: ("Vách Kim Cương", "land", 110, "a tall cliff of layered ochre and red-brown rock with big pale-blue diamond crystals sticking "
                                       "out of its face (flat colours, no shine) and a pile of fallen diamond crystals at its foot"),
    9: ("Lò Gốm Đất Nung", "land", 110, "a pottery yard: a tall bottle-shaped kiln of red bricks with a dark arched firing mouth (no "
                                        "fire, no glow), wooden shelves with rows of terracotta jars, pots and vases drying, a "
                                        "potter's wheel and a stack of firewood"),
    10: ("Kim Tự Viện", "boss", 120, "the boss lair: the road ends in the big round empty arena; right behind it rises a big stepped "
                                     "pyramid of sand-coloured stone blocks with a wide straight stairway in the middle coming down "
                                     "towards the arena, and on its top platform a small temple with red pillars and a golden tiled "
                                     "roof with curved eaves; two big stone guardian lion statues sit on both sides of the foot of the "
                                     "stairway, behind the arena; the top of the temple reaches up to the sea at the top edge"),
}

warnings = z.warnings


def seg_of(y):
    return z.seg_of(y)


# ---------- bố cục ----------

def layout():
    line, stops = z.build_road()
    road = z.Road(line)
    pts = [road.at(s) for s in stops]
    clears = [(p, z.CLEAR[z.KIND[i]] * z.ROAD_W) for i, p in enumerate(pts)]
    print(f"Bản đồ {W} x {H}, dải nối {z.BANDS}; đường {road.length:.0f} px ảnh = {road.length * z.DISPLAY:.0f} px khung 1080")
    print("  ải tướng:", ", ".join(f"{z.HEADS[i]} ({p[0]:.0f}, {p[1]:.0f})" for i, p in enumerate(pts)))
    spots, water = {}, {"streams": [], "pools": [], "bays": []}

    # hẻm núi khô chạy ngang từ mép trái (thấp) sang mép phải (cao), qua đường ở cầu treo ngay sau bãi ải 5; nghiêng như sông
    # dung nham đảo Hỏa (cùng lượn phải trước): nghiêng như đảo Kim thì hẻm ôm sát mép trên bãi ải 5
    sx = stops[GORGE_AT] + AFTER
    X = road.at(sx)
    gorge = z.wavy((-40, X[1] + 70), X, 22, 31)[:-1] + z.wavy(X, (W + 40, X[1] - 50), 22, 32)
    z.check_water("hẻm núi", gorge, GORGE_W / 2, road, (sx - 200, sx + 200))
    n = road.normal(sx)
    water["gorge"] = gorge
    water["bridge"] = {"c": X, "dir": (n[0], n[1])}

    # kim tự tháp (10) ngay sau bãi đấu boss; các địa danh khác chọn chỗ cùng lúc, né hẻm núi và kim tự tháp
    r10 = SPOTS[BOSS][2]
    boss = (pts[9][0], pts[9][1] - (clears[9][1] + r10 - 40))
    if boss[1] - r10 < z.TOP_SEA_Y + 10:
        z.warn("kim tự tháp chạm biển trên")
    obstacles = [(p, GORGE_W / 2 + 6) for p in gorge[::3]] + [(boss, r10)]
    nums = list(range(1, 10))
    radius = {k: SPOTS[k][2] for k in nums}
    cands = {k: z.candidates(road, stops[k - 1], radius[k], clears, obstacles, bottom=(k == 1)) for k in nums}
    for k in nums:
        if not cands[k]:
            z.warn(f"không có chỗ cho địa danh {k} ({SPOTS[k][0]})")
    chosen = z.assign({k: c for k, c in cands.items() if c}, radius)
    chosen[BOSS] = boss

    for num in range(1, 11):
        if num not in chosen:
            continue
        c = chosen[num]
        side = 1 if c[0] > road.x_at(c[1]) else -1
        spots[num] = {"c": c, "r": SPOTS[num][2], "kind": SPOTS[num][1], "side": side}
    # 6: lạch nước từ hồ ra mép cùng phía
    if POND in spots:
        c, side = spots[POND]["c"], spots[POND]["side"]
        edge_x = W + 60 if side > 0 else -60
        creek = z.wavy(c, (edge_x, c[1] - 40), 18, 26)
        z.check_water("lạch hồ sồi", creek, z.STREAM_W / 2, road)
        for num, sp in spots.items():
            if num != POND and min(math.dist(p, sp["c"]) for p in creek) < sp["r"] + z.STREAM_W / 2:
                z.warn(f"lạch hồ sồi chạm địa danh {num}")
        water["streams"].append(creek)
        spots[POND]["edge"] = "right" if side > 0 else "left"
    for num, sp in sorted(spots.items()):
        c = sp["c"]
        print(f"  địa danh {num:2d} {SPOTS[num][0]}: ({c[0]:.0f}, {c[1]:.0f}) đoạn {seg_of(c[1]) + 1}, "
              f"{'phải' if sp['side'] > 0 else 'trái'} đường")
    b = water["bridge"]["c"]
    print(f"  cầu treo qua hẻm núi: ({b[0]:.0f}, {b[1]:.0f}) đoạn {seg_of(b[1]) + 1}")
    return road, stops, pts, spots, water


def draw_guide(road, pts, spots, water):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im, "RGBA")
    z.hatch(d, (0, 0, W, H), GROUND, 79, 9000)
    beach = z.shore(z.BEACH_Y, 14, 70, 0.9)
    d.polygon(beach + [(W, H), (0, H)], fill=z.SAND)
    d.line(beach, fill=z.INK, width=4)
    for w, col in ((GORGE_W + 10, z.INK), (GORGE_W, CANYON)):
        z.stamp_line(d, water["gorge"], w, col)
    for st in water["streams"]:
        for w, col in ((z.STREAM_W + 10, z.INK), (z.STREAM_W, z.WATER)):
            z.stamp_line(d, st, w, col)
    for w, col in ((z.ROAD_W + 10, z.INK), (z.ROAD_W, z.ROAD)):
        z.stamp_line(d, road.p, w, col)
        for i, p in enumerate(pts):
            rad = z.CLEAR[z.KIND[i]] * z.ROAD_W + (5 if col == z.INK else 0)
            d.ellipse((p[0] - rad, p[1] - rad, p[0] + rad, p[1] + rad), fill=col)
    sea = z.shore(z.SEA_Y, 10, 55, 1.9)
    d.polygon(sea + [(W, H), (0, H)], fill=z.WATER)
    d.line(sea, fill=z.INK, width=4)
    top = z.shore(z.TOP_SEA_Y, 12, 60, 0.4)
    d.polygon([(0, 0), (W, 0)] + top[::-1], fill=z.WATER)
    d.line(top, fill=z.INK, width=4)
    b = water["bridge"]
    (bx, by), (nx, ny) = b["c"], b["dir"]
    tx, ty = -ny, nx
    hw, hl = z.ROAD_W / 2 + 18, GORGE_W / 2 + 16
    poly = [(bx + nx * hw + tx * hl, by + ny * hw + ty * hl), (bx - nx * hw + tx * hl, by - ny * hw + ty * hl),
            (bx - nx * hw - tx * hl, by - ny * hw - ty * hl), (bx + nx * hw - tx * hl, by + ny * hw - ty * hl)]
    d.polygon(poly, fill=WOOD, outline=z.INK, width=5)
    for f in (-0.5, 0, 0.5):  # vạch ván cầu
        d.line([(bx + nx * hw + tx * hl * f, by + ny * hw + ty * hl * f),
                (bx - nx * hw + tx * hl * f, by - ny * hw + ty * hl * f)], fill=z.INK, width=3)
    for num, sp in spots.items():
        c, r = sp["c"], sp["r"]
        if sp["kind"] == "land":
            d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=z.SPOT)
            z.dashed_circle(d, c, r, z.INK)
        elif sp["kind"] == "boss":
            z.disc(d, c, r, PYRAMID)
        else:
            z.disc(d, c, r, z.WATER)
        z.label(d, c, str(num))
    return im


# ---------- gói gửi GPT ----------

def seg_spots(k, spots):
    return [num for num, sp in sorted(spots.items()) if seg_of(sp["c"][1]) == k]


def spot_line(num, spots):
    text = SPOTS[num][3]
    if num == POND:
        text = text.format(edge=spots[POND]["edge"])
    return f"{num} {text};"


def gorge_dir(water):
    s = water["gorge"]
    return ("right", "left") if s[0][0] > s[-1][0] else ("left", "right")


def gorge_here(k, water):
    return seg_of(water["bridge"]["c"][1]) == k


WATER_LOOK = ("The pond and the creek are clear blue water with a wobbly ink bank lined with sandstone pebbles and a few white "
              "ripple scribbles; no foam, no splashes, no waterfalls.")


def water_lines(k, spots):
    lines = []
    if k == 0:
        lines.append("the sea along the bottom edge behind a shore of pale sand and round pebbles (the journey starts at the water's "
                     "edge, at the pebble beach);")
    if POND in spots and seg_of(spots[POND]["c"][1]) == k:
        lines.append(f"spot {POND} is a round pond at the foot of the old oak; its small creek runs off the "
                     f"{spots[POND]['edge']} edge;")
    if k == NSEG - 1:
        lines.append("a strip of sea along the top edge beyond the northern tip of the island, behind the pyramid temple.")
    return lines


def gorge_text(water):
    a, b = gorge_dir(water)
    return (f"CANYON: a narrow deep dry canyon on the dark brown band of the sketch, crossing the whole image from the {a} edge to "
            f"the {b} edge. Two wobbly rims of ochre rock; its far (upper) wall shows layered red-brown and ochre rock stripes going "
            f"down, its bottom is dark brown hatching (not pure black); a few small rocks and dry tufts on the rims; no water and no "
            f"lava in it. The road crosses it on a wooden rope bridge: planks tied with thick ropes between four stout wooden posts, "
            f"two at each end beside the road, exactly as wide as the road; the bridge deck is part of the road and stays empty.")


GROUND_TEXT = (
    "GROUND: no island outline on the sides: the land runs off the left and right edges. The ground is warm golden-ochre "
    "coloured-pencil hatching like the old Earth island map (a deep golden yellow, clearly darker and more orange than the pale "
    "road), mixed with patches of red-brown clay, cracked dry earth, small dry grass tufts and wavy wind lines. On both sides of the "
    "road, low raised terraces with short cliff faces of layered sandstone (top in the ground colour, side in reddish-brown hatching) "
    "give the map depth. Small flat-topped mesas of red-brown rock, clusters of sandstone boulders, round olive-green bushes, short "
    "trees with flat umbrella crowns and a few small cacti frame the road edges closely. Small props along the road edges: clay jars, "
    "a wooden hand cart, little stone cairns, short wooden fences, haystacks, a wooden signpost without writing, small unlit stone "
    "lanterns. Dense, but every rock, tree and prop is a chunky doodle with a clear silhouette; no tiny noisy details, no 3D, no "
    "realistic rendering.")

CODES = ("The sketch is only a colour-coded plan: golden ochre = ground, pale sand with an ink edge = road, blue = sea, pond and creek "
         "water, dark brown band = the dry canyon, wooden bar across the road = the rope bridge, grey spot with a number = a landmark "
         "on land, blue spot with a number = a landmark in a pond, dark grey spot with a number = the pyramid temple. Do not copy its "
         "flat colours, its numbers or its dashed outlines.")

RULES = ("Keep the road and the landmarks between x = 130 and x = 894 (narrow phones cut the outer strips); the outer strips have only "
         "ground, rocks and trees.\n"
         "Moving things are added later as animated sprites, so do NOT draw: smoke, dust clouds, fire or flames, glows or light halos, "
         "sparkles or shine stars on the crystals, foam splashes, breaking wave crests.\n"
         "No text, no letters, no numbers, no signs with writing, no creatures, no people (stone statues are fine).")


def sketch_path(k):
    return PACK / f"bo_cuc_{k + 1}.png"


def prompt_path(k):
    return PACK / f"luot_{k + 1}.txt"


def save_path(k):
    return WORK / "tai_ve" / f"doan_{k + 1}.png"


OLD_EN = ("the old small map of this same Earth island: copy its colours and the look of its objects (warm golden-ochre hatched "
          "ground with wavy wind lines, red-brown flat-topped mesas, grey rocks, dry grass tufts, the stepped terraced hill, the "
          "rope bridge, the temple with red pillars and a golden roof on a stepped stone base, the stone guardian lions); ignore its "
          "layout, its thin path, its cracked dry riverbed, its palm oasis, its island outline, its transparent background and its "
          "cream circles")
OLD_VI = ("bản đồ đảo Thổ 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền vàng đất gạch chì có vân gió, đường mòn mảnh có 8 "
          "vòng tròn kem, núi đất đỏ đỉnh bằng, đá xám, đồi ruộng bậc thang, bệ đá có cọc gỗ, lòng sông khô nứt có cầu treo, ốc đảo "
          "có cây dừa, trên đỉnh là đền cột đỏ mái vàng trên nền đá bậc và hai tượng sư tử đá; lấy màu và dáng đồ vật")


def refs(k, spots, water):
    """ảnh mẫu GPT mở của lượt k: [(vai, đường dẫn, câu cho GPT, mô tả cho người dùng)]"""
    sk = ("sketch", sketch_path(k), "the layout sketch of the image you draw now: follow it exactly" +
          (f"; its bottom {OV} px strip is not a sketch but the top {OV} px of image 1, already painted" if k else ""),
          f"bố cục đoạn {k + 1} (1024 × 1536, nền vàng đất)" + (f"; dải {OV} px ở đáy là dải đỉnh của đoạn {k}" if k else "") +
          "; " + seg_desc(k, spots, water))
    old = ("old", OLD, OLD_EN, OLD_VI)
    if k == 0:
        return [("style", STYLE, "part 1 of the long map of ANOTHER island of this same game, already approved: copy its RENDERING "
                                 "and how the map is built (the wide pale-sand road with round clearings, raised terraces with short "
                                 "cliff faces, chunky trees, rocks and props framing the road, line weight, hatching); ignore its "
                                 "green colours, its forest objects and its layout",
                 "đoạn 1 bản đồ dài đảo Mộc đã duyệt (1024 × 1536, nền đặc): đường cát rộng lượn có bãi tròn, bậc đất có vách ngắn, "
                 "cây tròn, đá, đồ vật chen sát đường, nền xanh lá; lấy nét và cách dựng, không lấy màu, đồ vật rừng, bố cục"),
                old, sk]
    return [("prev", WORK / f"doan_{k}.png", f"part {k} of this map, already drawn and approved: copy its style, colours, line "
                                             f"weight and objects exactly, so all parts look like one picture",
             f"đoạn {k} bản đồ đảo Thổ đã duyệt (1024 × 1536)"),
            sk, old]


def instructions(k, spots, water):
    rs = refs(k, spots, water)
    idx = {role: i + 1 for i, (role, *_rest) in enumerate(rs)}
    nums = seg_spots(k, spots)
    out = save_path(k)
    text = ("Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as "
            "described under SAVE. Do not reply with text only.\n\n"
            "REFERENCE IMAGES (open each file from its full path; all are 1024 x 1536):\n")
    text += "".join(f"image {i + 1} = {path}: {en}\n" for i, (_, path, en, _) in enumerate(rs))
    text += (f"\nSAVE: save the finished image as a 1024 x 1536 PNG to\n{out}\nCreate the folder if it is missing. If that file "
             f"already exists, save it as {out.stem}_2.png, {out.stem}_3.png … in the same folder instead. Do not change, move or "
             f"delete any other file.\n\n")
    sk = f"image {idx['sketch']}"
    if k == 0:
        text += ("WHAT THIS IS: part 1 of 3 (the bottom part) of one long vertical map of the Earth island, an island of golden "
                 "earth, sandstone, red clay and crystals, for a vertical mobile game. The player scrolls up the map from the pebble "
                 "beach at the bottom to the boss at the pyramid temple at the top. The three parts are drawn one after another and "
                 f"stacked. Part 2 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px of this image "
                 "plain: road, ground, a few bushes and rocks, no landmark, no water, no canyon.\n\n"
                 f"Draw a vertical 1024 x 1536 image in the rendering and map construction of image {idx['style']} with the colours "
                 f"and objects of image {idx['old']}: a warm golden-ochre earth island, not a green forest island. Outlines and "
                 f"hatching as bold as in image {idx['style']}.\n\n")
    else:
        part = "the middle part" if k == 1 else "the top part"
        text += (f"WHAT THIS IS: part {k + 1} of 3 ({part}) of one long vertical map of the Earth island, an island of golden "
                 f"earth, sandstone, red clay and crystals, for a vertical mobile game. The player scrolls up the map from the pebble "
                 f"beach at the bottom to the boss at the pyramid temple at the top; your image goes right above image "
                 f"{idx['prev']}.\n\n"
                 f"Draw a vertical 1024 x 1536 image in exactly the style of image {idx['prev']}. Image {idx['old']} only shows how "
                 f"this island's objects look (the terraced hill, the temple with a golden roof, the stone lions); copy the drawing "
                 f"of image {idx['prev']}, not image {idx['old']}'s.\n\n"
                 f"JOIN: the bottom {OV} px of your image must show the same scene as the painted bottom strip of {sk}, at the same "
                 f"place: the road at the same position and width, the same ground, trees and rocks. Then continue the map upward "
                 f"following the sketch, so image {idx['prev']} and your image join into one picture without a seam. Where the "
                 f"painted strip ends ({OV} px above the bottom edge) there must be no visible line or step: both edges of the road, "
                 f"the hatching, the colours and any object crossing that height continue smoothly.\n")
        if k == 1:
            text += (f"Part 3 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px plain: road, ground, "
                     "a few bushes and rocks, no landmark, no water.\n")
        text += "\n"
    text += (f"LAYOUT: copy {sk} exactly: the same road path and width, the same round clearings, the same water and canyon shapes, "
             f"every landmark on its numbered spot. {CODES}\n\n")
    road = z.ROAD_TEXT + " The road is pale cream sand, clearly paler than the golden-ochre ground."
    if k == 0:
        road += " The road starts at the water's edge on the shore at the bottom and leaves the top edge exactly where the sketch does."
    elif k == 1:
        road += " The road enters at the bottom and leaves the top edge exactly where the sketch does."
    else:
        road += " The road enters at the bottom and ends in the big round arena near the top."
    text += f"{road}\n\n{GROUND_TEXT}\n\n"
    if gorge_here(k, water):
        text += gorge_text(water) + "\n\n"
    wl = water_lines(k, spots)
    if wl:
        sea = "the sea is blue with a wobbly ink bank and white ripple scribbles. " if k in (0, NSEG - 1) else ""
        look = WATER_LOOK if any("pond" in s for s in wl) else ""
        text += ("WATER: " + (sea + look).strip() + "\n" + "\n".join("- " + s for s in wl) + "\n")
        if k == 0:
            text += "No other water in this part.\n"
        text += "\n"
    else:
        text += "WATER: no water in this part.\n\n"
    text += (f"LANDMARKS: each stands on its numbered spot of {sk}, right beside the road, about the size of that spot, and never "
             f"covers the road or a clearing:\n" + "\n".join("- " + spot_line(n, spots) for n in nums) + f"\n\n{RULES}\n\n"
             f"Remember: save the image to {out}\n")
    return text


def ready(k):
    return k == 0 or (WORK / f"doan_{k}.png").exists()


def build_pack(spots, water, guide):
    PACK.mkdir(parents=True, exist_ok=True)
    (WORK / "tai_ve").mkdir(parents=True, exist_ok=True)
    for k in range(NSEG):
        if not ready(k):
            continue
        crop = guide.crop((0, z.seg_top(k), W, z.seg_top(k) + SH))
        if k > 0:
            done = Image.open(WORK / f"doan_{k}.png").convert("RGB")
            crop.paste(done.crop((0, 0, W, OV)), (0, SH - OV))
        crop.save(sketch_path(k))
        prompt_path(k).write_text(instructions(k, spots, water), encoding="utf-8")
    (PACK / "HUONG_DAN.md").write_text(guide_md(spots, water), encoding="utf-8")


# ---------- hướng dẫn cho người dùng ----------

def seg_desc(k, spots, water):
    parts = []
    if k == 0:
        parts.append("đáy là bờ cát nhạt, đá cuội và biển, đường bắt đầu từ mép nước")
    if gorge_here(k, water):
        parts.append("dải nâu sẫm chạy ngang hết bề ngang là hẻm núi khô, thanh màu gỗ có vạch ngang đường là cầu treo")
    for num in seg_spots(k, spots):
        sp = spots[num]
        if sp["kind"] == "land":
            parts.append(f"chấm xám số {num} là chỗ {SPOTS[num][0]}")
        elif sp["kind"] == "boss":
            parts.append(f"đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm xám sẫm số {num} sau bãi là kim tự tháp có đền mái vàng")
        else:
            parts.append(f"chấm xanh số {num} là hồ nước của {SPOTS[num][0]}, lạch nước chảy ra mép "
                         f"{'phải' if sp.get('edge') == 'right' else 'trái'}")
    if k == NSEG - 1:
        parts.append("dải biển dọc mép trên")
    return "; ".join(parts)


def guide_md(spots, water):
    p = lambda *a: str(Path(*a))  # noqa: E731
    lines = [
        "# Gói gửi GPT: bản đồ dài đảo Thổ 70 ải (`zone_tho_70`)",
        "",
        f"Sinh bằng `{p(HERE, 'build_zone70_tho.py')}`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Thổ mới cho 70 ải, cùng "
        f"khuôn bản đồ dài đảo Thủy, Mộc, Hỏa, Kim: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ "
        f"{W} × {H}. Đường cát kem rộng lượn chữ S (lượn phải trước) từ bãi đá cuội lên bãi đấu boss dưới kim tự tháp có đền mái "
        f"vàng, 10 bãi tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Đường qua hẻm núi khô bằng cầu treo ngay sau "
        f"bãi ải 5. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường. Khói, bụi, lửa, lấp lánh, sóng là phần động game "
        f"thêm sau, GPT không vẽ.",
        "",
        "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. "
        "Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude \"duyệt đoạn <k> đảo Thổ\"; Claude soi, lưu "
        "bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét.",
        "",
        "| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |",
        "|---|---|---|---|",
    ]
    names = ("đoạn dưới", "đoạn giữa", "đoạn trên")
    for k in range(NSEG):
        nums = ", ".join(map(str, seg_spots(k, spots)))
        prompt = f"`{prompt_path(k)}`" + ("" if ready(k) else f" (chưa có: Claude dựng khi duyệt đoạn {k})")
        imgs = "; ".join(f"{i + 1} `{path}`: {desc}" + ("" if Path(path).exists() or ready(k) else " (chưa có)")
                         for i, (_, path, _, desc) in enumerate(refs(k, spots, water)))
        lines.append(f"| {k + 1}: {names[k]}, địa danh {nums} | {prompt} | {imgs} | `{save_path(k)}` |")
    lines += ["", f"Bản duyệt Claude lưu ở `{p(WORK, 'doan_<k>.png')}`. Không để ảnh vào `{p(HERE, 'inbox')}` (menu nhập ảnh sẽ chép "
              f"nguyên khổ vào game).", ""]
    lines += ["## Địa danh", "", "| Số | Chặng (ải) | Vẽ gì |", "|---|---|---|"]
    vi = {1: "bãi đá cuội cạnh đầu đường: đống cuội tròn to nhỏ màu xám, be, đỏ gỉ, tháp đá dẹt xếp chồng cao, vỏ ốc xoắn lớn vùi nửa "
             "trong cát, khúc gỗ trôi dạt bạc màu",
          2: "hang lửng: gò đất phủ cỏ thấp có cửa hang tròn lớn, viền rễ cây và hai cột gỗ chống, đống đất mới đào, cuốc chim và xẻng "
             "dựng bên gò, vài cục vàng nhỏ trên đất; hang trống",
          3: "đồi đá vàng đất nhỏ tròn, cụm pha lê xanh ngọc lục bảo to nhô ra sườn và đỉnh (màu phẳng, không lấp lánh)",
          4: "mỏ pha lê: cửa hang khung gỗ dày trong đồi đá vàng đất, cụm pha lê hồng tím quanh cửa, xe cút kít gỗ đầy pha lê hồng, "
             "mũi khoan xoắn lớn nằm dưới đất",
          5: "đền phù văn: vòng đá dựng cao màu xám trên nền đá tròn quanh phiến đá tế phẳng, đá khắc xoắn ốc, răng cưa, chấm (hoa "
             "văn, không phải chữ)",
          6: "hồ tròn dưới gốc sồi cổ thụ: sồi đứng bờ sau hồ, thân to sần, rễ lớn thò xuống nước, tán tròn rộng xanh ô liu sẫm; quả "
             "sồi, hạt dẻ trên bờ, hai ba cây sồi nhỏ quanh; lạch nước chảy ra mép",
          7: "đồi ruộng bậc thang: năm, sáu bậc ruộng xanh uốn quanh đồi tròn, bờ đất mảnh giữa các bậc, chòi mái rơm nhỏ trên bậc cao "
             "nhất, vài đống rơm dưới chân",
          8: "vách đá cao nhiều lớp vàng đất và nâu đỏ, kim cương xanh nhạt to nhô ra mặt vách (màu phẳng), đống kim cương rơi dưới "
             "chân vách",
          9: "xưởng gốm: lò gạch đỏ cao hình cổ chai, cửa lò vòm tối (không lửa, không quầng sáng), kệ gỗ xếp hàng chum, bình, vò đất "
             "nung đang phơi, bàn xoay gốm, đống củi",
          10: "kim tự tháp bậc bằng khối đá màu cát ngay sau bãi đấu boss, cầu thang thẳng rộng ở giữa đi xuống phía bãi đấu, đền nhỏ "
              "cột đỏ mái ngói vàng mái cong trên đỉnh; hai tượng sư tử đá lớn ngồi hai bên chân cầu thang, sau bãi; đỉnh đền chạm "
              "dải biển trên"}
    heads = z.HEADS + [71]
    for num in range(1, 11):
        rng = f"{heads[num - 1]}–{heads[num] - 1}" if heads[num] - 1 > heads[num - 1] else f"{heads[num - 1]}"
        lines.append(f"| {num} | {SPOTS[num][0]} ({rng}) | {vi[num]} |")
    lines += [
        "",
        "Hẻm núi khô có cầu treo (không thuộc chặng nào): khe sâu chạy ngang hết bề ngang ngay sau bãi ải 5, vách xa lộ vân đá nhiều "
        "lớp nâu đỏ và vàng đất, đáy gạch chì nâu sẫm, không nước, không dung nham; cầu ván gỗ buộc dây thừng giữa bốn cột gỗ, rộng "
        "bằng đường, mặt cầu trống.",
        "",
        "## Soi trước khi nhắn Claude",
        "",
        "- Đảo đất vàng (không phải đảo rừng xanh lá như ảnh mẫu đảo Mộc), nét và cách dựng giống ảnh mẫu.",
        "- **Đường cát kem nhạt hơn hẳn nền vàng đất**, nhìn rõ mép đường (game dò đường theo màu cát nhạt).",
        "- Đường đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường, mặt cầu và các bãi tròn **trống**.",
        "- Địa danh đúng số, đứng sát đường, không đè lên đường.",
        "- Lượt 1: hẻm núi khô (không có nước) chạy ngang, cầu treo rộng bằng đường, đường đi thẳng qua cầu.",
        "- Hồ, lạch là nước xanh có bờ đá cuội, không bọt, không thác; lò gốm không có lửa.",
        "- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).",
        f"- Lượt 1, 2: dải {OV} px trên cùng chỉ có đường, đất, bụi, đá.",
        "- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không khói, bụi, lửa, lấp lánh (game thêm).",
        "",
        "## Sửa nhanh (gõ vào chat)",
        "",
        "| Lỗi | Gõ |",
        "|---|---|",
        "| Ra màu xanh lá, cây rừng như đảo Mộc | `Same layout, but this is the warm golden-ochre Earth island: golden-ochre hatched "
        "ground, red-brown clay and sandstone, olive bushes and a few small trees; no bright green grass, no green forest.` |",
        "| Đường lẫn vào nền | `Same image, but make the road and the clearings a much paler cream sand than the golden-ochre ground, "
        "with a clear wobbly ink edge.` |",
        "| Hẻm núi có nước hoặc thành sông | `Same image, but the canyon is dry: layered rock walls going down to a dark brown bottom, "
        "no water, no lava.` |",
        "| Cầu treo hẹp, lệch hay chắn đường | `Same image, but the rope bridge is exactly as wide as the road and the road runs straight "
        "across it; the bridge deck stays empty.` |",
        "| Có khói, bụi, lửa, quầng sáng, lấp lánh | `Same image, but remove all smoke, dust, fire, flames, sparkles and glows. The kiln "
        "mouth is just dark, the crystals are flat colours.` |",
        "| Đá đền Phù Văn có chữ | `Same image, but the standing stones carry only spirals, zigzags and dots, nothing that looks like "
        "letters or writing.` |",
        "| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road, the bridge deck and the round clearings completely empty: "
        "remove everything standing on them.` |",
        "| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round "
        "clearings.` |",
        "| Có số, chữ | `Same image without any numbers, letters or text.` |",
        "| Có người, sinh vật | `Same image without any people or creatures; stone statues are fine.` |",
        "| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |",
        f"| Dải đáy không nối với đoạn trước | `Redraw it so the bottom {OV} px show exactly the same scene as the painted bottom strip of "
        "the sketch: same road position and width, same trees and rocks.` |",
        "| Kim tự tháp hay tượng sư tử đè lên bãi đấu | `Same image, but the pyramid, its stairway and the stone lions stay behind the "
        "arena: the round arena is completely empty.` |",
        "| Quá vụn | `Too detailed. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every "
        "rock, tree and prop a chunky doodle with a clear silhouette. Keep the same layout.` |",
        "",
    ]
    return "\n".join(lines)


# ---------- toạ độ dự kiến ----------

def save_json(road, stops, pts, spots, water):
    path = [road.at(s) for s in range(0, int(road.length) + 1, 24)] + [road.p[-1]]
    stages = []
    for i, p in enumerate(pts):
        st = {"idx": z.HEADS[i], "x": round(p[0] / W, 4), "y": round(p[1] / H, 4), "road": round(stops[i] / road.length, 4)}
        sp = spots.get(i + 1)
        if sp:
            st["spot"] = [round(sp["c"][0] / W, 4), round(sp["c"][1] / H, 4), round(sp["r"] / W, 4)]
            st["spotSide"] = sp["side"]
        stages.append(st)
    b = water["bridge"]["c"]
    data = {
        "note": "Bố cục dự kiến của bản đồ dài đảo Thổ (build_zone70_tho.py); x, y từ 0 tới 1 theo bản đồ ghép, y từ trên. Có ảnh "
                "thật thì dò lại đường.",
        "map": [W, H], "segments": NSEG, "overlap": OV, "displayWidth": 1.27, "roadWidth": round(z.ROAD_W / W, 4),
        "pipGap": round(z.GAP, 1),
        "path": [[round(x / W, 4), round(y / H, 4)] for x, y in path],
        "stages": stages,
        "bridge": [round(b[0] / W, 4), round(b[1] / H, 4)],
        "gorge": [[round(x / W, 4), round(y / H, 4)] for x, y in water["gorge"][::2]],
    }
    (GUIDES / "zone70_tho.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- ghép 3 đoạn đã duyệt ----------

FEATHER = 24  # nửa bề cao vùng trộn quanh đường cắt giữa dải chồng


def ghep():
    """ghép doan_1..3 đã duyệt thành bản đồ W x H (zones/tho70/zone_tho70.png), như build_zone70_kim.ghep"""
    segs = [np.array(Image.open(WORK / f"doan_{k + 1}.png").convert("RGB")).astype(float) for k in range(NSEG)]
    tops = [H - SH]
    for k in range(1, NSEG):
        dy, err = m.band_offset(segs[k - 1], segs[k])
        tops.append(tops[-1] - (SH - OV) + dy)
        print(f"  nối đoạn {k} và {k + 1}: dời đoạn {k + 1} xuống {dy} px (chênh dải chồng {err:.1f})")
    img = np.zeros((H, W, 3))
    filled = np.zeros(H, bool)
    for k in range(NSEG):
        t = tops[k]
        y0, y1 = max(0, t), t + SH
        part = segs[k][y0 - t:y1 - t]
        if k == 0:
            img[y0:y1] = part
        else:
            cut = (tops[k - 1] + y1) // 2  # giữa dải chồng
            for y in range(y0, y1):
                src = part[y - y0]
                if y < cut - FEATHER:
                    img[y] = src
                elif y < cut + FEATHER and filled[y]:
                    w = (y - (cut - FEATHER)) / (2 * FEATHER)  # 0 ở trên (đoạn trên), 1 ở dưới (đoạn dưới)
                    img[y] = src * (1 - w) + img[y] * w
                elif not filled[y]:
                    img[y] = src
        filled[y0:y1] = True
    if tops[-1] > 0:
        img[:tops[-1]] = img[tops[-1]]
    out = WORK / "zone_tho70.png"
    Image.fromarray(img.clip(0, 255).astype("uint8")).save(out)
    (WORK / "ghep.json").write_text(json.dumps({"tops": tops}, ensure_ascii=False), encoding="utf-8")
    print(f"Đã ghi {out} ({W} x {H}); đỉnh các đoạn {tops}")


# ---------- dò đường thật trên bản đồ ghép ----------
# Như đảo Kim: tâm đường theo hàng (bắt lại sau cầu treo), 10 bãi ải là chỗ bề rộng mặt cát đo vuông góc vượt ngưỡng. Khác đảo Kim:
# - nền vàng chanh lọt mặt nạ "cát lỏng" của đảo Kim (b gần 0 nhưng r, g cao), nên bề rộng đo trên chính sand_mask đã đóng lỗ;
# - bậc kim tự tháp màu cát nối liền bãi đấu boss: bỏ mặt cát phía trên STOP_Y để đường dừng ở mép trên bãi đấu;
# - không có sông: chỉ lạch từ hồ sồi ra mép trái (dò theo màu nước, đảo chiều cho chảy từ hồ ra mép).
# Địa danh, chỗ phần động đo tay trên bản đồ ghép (px bản đồ, 2026-11-06).

STOP_Y = 300  # mép trên bãi đấu boss (chân cầu thang kim tự tháp)
SPOTS_REAL = {1: ((745, 4135), 150), 2: ((275, 3937), 165), 3: ((790, 3442), 150), 4: ((240, 3272), 190), 5: ((740, 3072), 175),
              6: ((255, 2590), 170), 7: ((745, 2146), 190), 8: ((235, 1726), 200), 9: ((320, 900), 190), 10: ((512, 180), 200)}
BRIDGE_REAL = (415, 3692)
# phần động (IslandAnim, khoá zone_tho): (kiểu, x, y, cỡ px bản đồ)
ANIM = [
    ("smoke", 395, 772, 60),  # miệng lò gốm cổ chai
    ("sparkle", 512, 28, 26),  # quả cầu vàng trên mái đền Kim Tự Viện
    ("sparkle", 170, 1641, 28), ("sparkle", 295, 1731, 26), ("sparkle", 215, 1861, 26),  # kim cương trên vách
    ("sparkle", 805, 3355, 28), ("sparkle", 875, 3485, 24),  # pha lê ngọc lục bảo
    ("sparkle", 195, 3127, 26), ("sparkle", 375, 3312, 24), ("sparkle", 165, 3342, 22),  # pha lê hồng tím ở mỏ
    ("sparkle", 205, 3992, 20),  # cục vàng trước hang lửng
    ("ripple", 265, 2681, 70),  # hồ sồi
    ("leaf", 200, 2440, 34), ("leaf", 330, 2470, 34),  # lá sồi cổ thụ
    ("wind", 560, 2350, 80), ("wind", 300, 1250, 70), ("wind", 700, 520, 70),  # gió cát trên nền vân gió
    ("wave", 230, H - 30, 90), ("wave", 790, H - 40, 90), ("wave", 200, 24, 80), ("wave", 850, 28, 80),
]
CREEK_BOX = (0, 2560, 150, 2720)  # lạch từ hồ sồi ra mép trái (px bản đồ: x0, y0, x1, y1)


def road_sand(img):
    """mặt đường cát kem: sand_mask đóng lỗ (nét gạch chì trên đường), bỏ phần trên STOP_Y"""
    from PIL import ImageFilter
    sand = z.sand_mask(img)
    sand = np.asarray(Image.fromarray((sand * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5))
                      .filter(ImageFilter.MinFilter(5))) > 0
    sand[:STOP_Y] = False
    return sand


def that():
    """dò đường, 10 bãi ải, lạch trên zones/tho70/zone_tho70.png; ghi zones/tho70/that.json và ảnh soi soi_that.png"""
    img = np.array(Image.open(WORK / "zone_tho70.png").convert("RGB")).astype(int)
    sand = road_sand(img)
    with contextlib.redirect_stdout(io.StringIO()):
        road0, stops0, pts0, _, water0 = layout()
    y0 = 3900  # giữa bãi ải 1 và cầu treo
    path = m.resample(m.trace_road(sand, y0, road0.x_at(y0)), 6)
    d = [0.0]
    for a_, b_ in zip(path, path[1:]):
        d.append(d[-1] + math.dist(a_, b_))
    L = d[-1]
    P = np.array(path)
    ts = np.arange(-200, 201)
    prof = []
    for i_ in range(len(P)):
        t = P[min(len(P) - 1, i_ + 4)] - P[max(0, i_ - 4)]
        tl = math.hypot(*t) or 1
        nx, ny = -t[1] / tl, t[0] / tl
        xs = np.clip(np.round(P[i_, 0] + nx * ts).astype(int), 0, W - 1)
        ys = np.clip(np.round(P[i_, 1] + ny * ts).astype(int), 0, H - 1)
        v = sand[ys, xs]
        if not v[200]:
            prof.append(0)
            continue
        lo = hi = 200
        while lo > 0 and v[lo - 1]:
            lo -= 1
        while hi < len(v) - 1 and v[hi + 1]:
            hi += 1
        prof.append(hi - lo)
    prof = np.array(prof)
    thr = 140
    peaks, i = [], 0
    while i < len(prof):
        if prof[i] >= thr:
            j = i
            while j < len(prof) and prof[j] >= thr:
                j += 1
            if j - i >= 4:
                peaks.append((i + j - 1) // 2)
            i = j
        else:
            i += 1
    print(f"Đường thật: {len(path)} điểm, dài {L:.0f} px; bề rộng đường {np.median(prof):.0f} px, ngưỡng bãi {thr}; "
          f"{len(peaks)} khúc phình")
    want = [s / road0.length for s in stops0]
    stops = []
    for i_, w in enumerate(want):
        cand = [k for k in peaks if abs(d[k] / L - w) < 0.06 and (not stops or d[k] > d[stops[-1]] + 150)]
        if cand:
            stops.append(min(cand, key=lambda k: abs(d[k] / L - w)))
        else:
            z.warn(f"không thấy bãi ải {z.HEADS[i_]} gần {w:.3f} quãng đường; lấy theo tỉ lệ dự kiến")
            stops.append(int(np.argmin([abs(x / L - w) for x in d])))
    wm = kim.water_mask(img)
    creek = kim.trace_across(wm, CREEK_BOX)
    if len(creek) < 5:
        z.warn("không dò được lạch trên ảnh; lấy đường dự kiến")
        creek = water0["streams"][0]
    else:
        creek = creek[::-1]  # chảy từ hồ ra mép trái
        print(f"  lạch: {len(creek)} điểm, x {creek[0][0]:.0f}..{creek[-1][0]:.0f}, "
              f"y {min(p[1] for p in creek):.0f}..{max(p[1] for p in creek):.0f}")
    data = {
        "path": [[round(x, 1), round(y, 1)] for x, y in path],
        "stops": [round(d[k], 1) for k in stops], "length": round(L, 1),
        "stages": [[round(path[k][0], 1), round(path[k][1], 1)] for k in stops],
        "streams": [[[round(x, 1), round(y, 1)] for x, y in creek]],
        "bridge": list(BRIDGE_REAL),
    }
    (WORK / "that.json").write_text(json.dumps(data), encoding="utf-8")
    soi = Image.fromarray(img.astype("uint8"))
    dr = ImageDraw.Draw(soi)
    dr.line([tuple(p) for p in path], fill=(255, 0, 255), width=4)
    for k in stops:
        x, y = path[k]
        dr.ellipse((x - 30, y - 30, x + 30, y + 30), outline=(0, 255, 0), width=5)
    for s in data["streams"]:
        dr.line([tuple(p) for p in s], fill=(255, 0, 0), width=4)
    for num, ((x, y), r) in SPOTS_REAL.items():
        dr.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 0), width=4)
    for kind, x, y, sz in ANIM:
        dr.rectangle((x - sz / 2, y - sz / 2, x + sz / 2, y + sz / 2), outline=(0, 255, 255), width=3)
    soi.save(WORK / "soi_that.png")
    print("  ải tướng:", ", ".join(f"{z.HEADS[i_]} ({path[k][0]:.0f}, {path[k][1]:.0f})" for i_, k in enumerate(stops)))
    print(f"  ghi {WORK / 'that.json'}, {WORK / 'soi_that.png'}")


# ---------- xuất sang Unity ----------

def real_spots(path):
    """địa danh đo tay (SPOTS_REAL) theo dạng spots của layout: c, r, side (phía so với đường thật)"""
    ys = np.array([p[1] for p in path])
    xs = np.array([p[0] for p in path])
    out = {}
    for num, (c, r) in SPOTS_REAL.items():
        rx = float(np.interp(c[1], ys[::-1], xs[::-1]))
        out[num] = {"c": c, "r": r, "kind": SPOTS[num][1], "side": 1 if c[0] > rx else -1}
    return out


def anim_spec(water):
    """phần động trên ảnh (IslandAnim, khoá zone_tho): khói, lấp lánh, gợn, lá, gió, sóng (ANIM), gợn chạy dọc lạch. Toạ độ chia
    W, H; cỡ chia W"""
    rivers = [("stream", [(min(max(x, 2), W - 2), y) for x, y in st[::3]], z.STREAM_W) for st in water["streams"]]
    return {
        "items": [{"k": k, "x": round(x / W, 4), "y": round(y / H, 4), "s": round(sz / W, 4)} for k, x, y, sz in ANIM],
        "rivers": [{"k": k, "w": round(rw / W, 4), "pts": [[round(x / W, 4), round(y / H, 4)] for x, y in pts]}
                   for k, pts, rw in rivers if len(pts) >= 2],
    }


def xuat(art_out=None, zones_json=None):
    """đưa bản đồ đã ghép vào game theo đường dò được (that.json): Assets/03 Art/Islands/zone_tho.png (biển hai mép trong suốt; thay
    bản đồ 8 ải cũ), khoá zone_tho trong island_anim.json, đảo tho trong zones.json (nodes = 10 bãi ải dò được, path = tâm đường thật
    tới giữa bãi đấu boss, stops, plates). Đọc lại hai file JSON ngay lúc ghi, chỉ thay phần của đảo Thổ. Sau đó chạy menu Unity
    PokiClash/Nhập dữ liệu. art_out, zones_json: ghi chỗ khác để thử."""
    art_out = Path(art_out or z.ART_OUT)
    zones_json = Path(zones_json or z.ZONES_JSON)
    th = json.loads((WORK / "that.json").read_text(encoding="utf-8"))
    a = np.array(Image.open(WORK / "zone_tho70.png").convert("RGB"))
    alpha = z.sea_alpha(a)
    rgba = np.dstack([a, (alpha * 255).round().astype("uint8")])
    art_out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(art_out / "zone_tho.png", optimize=True)
    print(f"Đã ghi {art_out / 'zone_tho.png'} ({W} x {H}); biển trong suốt {(alpha < 0.5).mean() * 100:.1f}% ảnh")

    full = [tuple(p) for p in th["path"]]
    d = [0.0]
    for p0, p1 in zip(full, full[1:]):
        d.append(d[-1] + math.dist(p0, p1))
    end = int(np.argmin([abs(x - th["stops"][-1]) for x in d]))  # đường dừng ở giữa bãi đấu boss
    road = z.Road(full[:end + 1])
    stops = th["stops"]
    pts = [tuple(p) for p in th["stages"]]
    spots = real_spots(full)
    water = {"streams": th["streams"]}
    if not art_out.joinpath("island_anim.json").exists() and (z.ART_OUT / "island_anim.json").exists():
        art_out.joinpath("island_anim.json").write_bytes((z.ART_OUT / "island_anim.json").read_bytes())
    anim_path = art_out / "island_anim.json"
    anim = json.loads(anim_path.read_text(encoding="utf-8"))
    anim["zone_tho"] = anim_spec(water)
    nl = "\r\n" if b"\r\n" in anim_path.read_bytes() else "\n"
    anim_path.write_text(json.dumps(anim, ensure_ascii=False, indent=1), encoding="utf-8", newline=nl)
    print(f"Đã ghi khoá zone_tho trong {anim_path}: {len(anim['zone_tho']['items'])} món, {len(anim['zone_tho']['rivers'])} dòng")

    src_json = zones_json if zones_json.exists() else z.ZONES_JSON
    zl = "\r\n" if b"\r\n" in src_json.read_bytes() else "\n"  # giữ kiểu xuống dòng của file
    data = json.loads(src_json.read_text(encoding="utf-8"))
    zd = next(x for x in data["zones"] if x["id"] == "tho")
    path = [road.at(s) for s in np.arange(0, road.length, 32)] + [road.p[-1]]
    plates = [z.plate_side(i, p, spots) for i, p in enumerate(pts)]
    new = {}
    for k, v in zd.items():
        if k in ("path", "stops", "plates"):
            continue
        new[k] = v
        if k == "nodes":
            new["nodes"] = [[round(x / W, 4), round(y / H, 4)] for x, y in pts]
            new["path"] = [[round(x / W, 4), round(y / H, 4)] for x, y in path]
            new["stops"] = [round(s / road.length, 5) for s in stops]
            new["plates"] = plates
    data["zones"][data["zones"].index(zd)] = new
    zones_json.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline=zl)
    print(f"Đã ghi đảo tho trong {zones_json}: 10 ải tướng, đường {len(path)} điểm, bảng tên {plates}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar="K [ANH]",
                    help="lưu đoạn K (1..3) GPT trả về (mặc định ảnh mới nhất tai_ve/doan_K*.png) rồi dựng lại gói")
    ap.add_argument("--ghep", action="store_true", help="ghép 3 đoạn đã duyệt thành zones/tho70/zone_tho70.png")
    ap.add_argument("--that", action="store_true", help="dò đường, bãi ải, lạch thật trên bản đồ đã ghép (that.json)")
    ap.add_argument("--xuat", nargs="?", const="", metavar="THU_MUC",
                    help="đưa bản đồ đã ghép vào Assets (ảnh, phần động, zones.json), hoặc vào THU_MUC để thử")
    a = ap.parse_args()
    if a.ghep:
        ghep()
        return
    if a.that:
        that()
        return
    if a.xuat is not None:
        if a.xuat:
            xuat(a.xuat, Path(a.xuat) / "zones.json")
        else:
            xuat()
        return
    if a.duyet:
        k = int(a.duyet[0])
        if len(a.duyet) > 1:
            src = Path(a.duyet[1])
        else:
            found = sorted((WORK / "tai_ve").glob(f"doan_{k}*.png"), key=lambda f: f.stat().st_mtime)
            if not found:
                sys.exit(f"Không thấy ảnh doan_{k}*.png trong {WORK / 'tai_ve'}")
            src = found[-1]
        print(f"Duyệt đoạn {k}: {src}")
        im = Image.open(src).convert("RGB")
        if im.size != (W, SH):
            print(f"  ! ảnh {im.size[0]} x {im.size[1]}, đưa về {W} x {SH}")
            im = im.resize((W, SH), Image.LANCZOS)
        if k > 1:  # đoạn có dải dán: sửa chỗ nối (ảnh GPT trong tai_ve giữ nguyên)
            with contextlib.redirect_stdout(io.StringIO()):
                road = layout()[0]
            arr = np.array(im).astype(float)
            kim.va_noi(arr, k - 1, road)
            im = Image.fromarray(arr.clip(0, 255).astype("uint8"))
        WORK.mkdir(parents=True, exist_ok=True)
        im.save(WORK / f"doan_{k}.png")
        print(f"Đã lưu {WORK / f'doan_{k}.png'}")
    road, stops, pts, spots, water = layout()
    guide = draw_guide(road, pts, spots, water)
    GUIDES.mkdir(exist_ok=True)
    guide.save(GUIDES / "L_zone70_tho.png")
    save_json(road, stops, pts, spots, water)
    build_pack(spots, water, guide)
    print(f"Đã ghi {GUIDES / 'L_zone70_tho.png'}, {GUIDES / 'zone70_tho.json'}, gói {PACK}")
    if warnings:
        print(f"{len(warnings)} cảnh báo, xem trên")


if __name__ == "__main__":
    main()
