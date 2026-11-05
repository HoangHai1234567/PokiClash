# Bản đồ dài đảo Hỏa 70 ải: dựng ảnh bố cục và gói gửi GPT, như build_zone70_moc.py (đảo Mộc). Dùng lại phần chung của
# build_zone70.py (đường chữ S, cỡ bản đồ 1024 x 4288 ghép 3 đoạn, chỗ địa danh) và band_offset của build_zone70_moc.py; không sửa
# hai file đó.
# Khác đảo Mộc:
# - đường lượn sang phải trước (ngược đảo Mộc), cùng độ cao 10 ải tướng;
# - sông dung nham chạy ngang, đường qua cầu đá bazan ngay trước ải 5 (chặng 2, Suối Dung Nham); hồ dung nham có lá sen đá và chùa
#   mái đỏ, lạch dung nham ra mép (chặng 6, Chùa Liên Hoa); núi lửa đứng sau bãi đấu boss, đỉnh chạm dải biển trên;
# - ảnh mẫu nét là đoạn 1 bản đồ dài đảo Mộc đã duyệt (cùng game, nét và cách dựng đã chốt), màu và đồ vật lấy bản đồ Hỏa 8 ải cũ;
# - khói, lửa, tàn lửa, quầng sáng không vẽ: game có sẵn phần động smoke, flame, sparkle và dòng dung nham chảy (IslandAnim).
# Ghi: ArtGen/guides/L_zone70_hoa.png (bố cục cả bản đồ), ArtGen/guides/zone70_hoa.json (đường, ải tướng, địa danh; toạ độ 0..1 của
# bản đồ ghép, y từ trên; gói nền trận đảo Hỏa đọc để cắt địa danh), gói ArtGen/Islands/gui_gpt/zone_hoa_70/ (luot_k.txt,
# bo_cuc_k.png, HUONG_DAN.md).
# Chạy: py -3 -I ArtGen/Islands/build_zone70_hoa.py
# Duyệt đoạn k GPT đã lưu: --duyet k [ảnh] (mặc định ảnh mới nhất zones/hoa70/tai_ve/doan_k*.png): lưu zones/hoa70/doan_k.png rồi
# dựng lại gói (có đoạn k thì có file prompt lượt k+1, bố cục đoạn k+1 dán dải đỉnh của đoạn k).
# Đủ 3 đoạn: --ghep (zones/hoa70/zone_hoa70.png). Dò đường thật và đưa vào game (--that, --xuat như đảo Mộc) viết khi có bản đồ
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
import build_zone70_moc as m  # noqa: E402  (band_offset; lúc nạp nó đặt z.FIRST = -1 nên đặt lại ngay dưới)

z.FIRST = 1  # chặng đầu lượn sang phải

W, SH, H, OV, NSEG = z.W, z.SH, z.H, z.OV, z.NSEG
GUIDES = z.GUIDES
PACK = HERE / "gui_gpt" / "zone_hoa_70"
WORK = HERE / "zones" / "hoa70"  # tai_ve/: ảnh GPT trả về; doan_k.png: đoạn đã duyệt
STYLE = HERE / "zones" / "moc70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Mộc đã duyệt
OLD = HERE / "zones" / "zone_hoa.png"  # bản đồ Hỏa 8 ải đang dùng

BRIDGE, POND, BOSS = 2, 6, 10
AFTER = 150  # cầu cách tâm bãi ải 5 bao nhiêu px đường (về phía ải 10)

# màu ảnh bố cục (chỉ là mã màu cho GPT): đất cam đất nhạt, dung nham cam, núi lửa nâu đỏ sẫm, cầu đá xám
GROUND = (236, 186, 150)
LAVA = (245, 140, 35)
VOLCANO = (110, 60, 50)
STONE = (95, 90, 88)

# địa danh từng chặng: tên chặng (IslandGen.Hoa), kiểu chỗ (land xám, water hồ dung nham, bridge cầu qua sông dung nham, boss núi
# lửa sau bãi đấu), bán kính, câu cho GPT
SPOTS = {
    1: ("Bến Đá Đen", "land", 100, "big black basalt boulders with flat six-sided tops, a short wooden pier on black posts and an old "
                                   "wooden boat pulled up on the dark sand beside the start of the road"),
    2: ("Suối Dung Nham", "bridge", 0, "the road crosses the lava river on a wide arched bridge of dark basalt blocks with low stone "
                                       "rails, exactly as wide as the road; the bridge is part of the road and stays empty; black "
                                       "rocks and a few charred trees on both banks"),
    3: ("Rừng Than Hồng", "land", 105, "a grove of charred black trees with thin orange cracks in their bark and round crowns of "
                                       "orange and red leaves, between a few black boulders"),
    4: ("Sườn Núi Khói", "land", 105, "a grey rocky slope of layered stone with three round vent holes ringed with yellow sulfur crust; "
                                      "no smoke (the game adds it)"),
    5: ("Lò Lửa Thiền", "land", 105, "a big round dome furnace of old grey stone bricks with a dark empty arched opening, beside a "
                                     "small stone meditation platform with a bronze incense burner and two stone lanterns"),
    6: ("Chùa Liên Hoa", "water", 110, "a round pool of lava with big flat stone lotus leaves lying on it; at the back of the pool, on "
                                       "a rock, a small temple with curved red roofs and a golden lotus on the roof top; a small lava "
                                       "creek leaves the pool and runs off the {edge} edge"),
    7: ("Lò Rèn Gai Thép", "land", 110, "a blacksmith forge under a sloping roof of black iron plates, with a tall stone chimney, a big "
                                        "anvil and racks of spiked steel shields and spears; a few iron spikes stick out of the "
                                        "ground around it"),
    8: ("Rừng Lửa Ảo", "land", 110, "a grove of strange twisted trees whose crowns are solid leaves shaped like big flames (leaves, "
                                    "not fire) in orange, pink and violet, with a few round violet crystals between their roots"),
    9: ("Hang Hồng Ngọc", "land", 110, "a cave mouth in a dark rock hill, bristling with big red ruby crystals"),
    10: ("Miệng Núi Lửa", "boss", 118, "the boss lair: the road ends in the big round empty arena; right behind it rises a big dark "
                                       "volcano with a wide crater full of lava at its top and a few lava streams running down its "
                                       "slopes to the sides, never onto the arena; two small stone guardian statues stand at the foot "
                                       "of the volcano on both sides behind the arena; the top of the volcano reaches up to the sea at "
                                       "the top edge"),
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

    # 2: sông dung nham chạy ngang từ mép trái sang mép phải, qua đường ở cầu đá ngay sau bãi ải 5 (trước bãi thì sông nằm sát bãi
    # cát, trông như chảy dọc bờ)
    sx = stops[BRIDGE - 1] + AFTER
    X = road.at(sx)
    stream = z.wavy((-40, X[1] + 70), X, 22, 23)[:-1] + z.wavy(X, (W + 40, X[1] - 50), 22, 24)
    z.check_water("sông dung nham", stream, z.STREAM_W / 2, road, (sx - 200, sx + 200))
    water["streams"].append(stream)
    n = road.normal(sx)
    spots[BRIDGE] = {"bridge": X, "dir": (n[0], n[1])}

    # núi lửa (10) ngay sau bãi đấu boss; các địa danh khác chọn chỗ cùng lúc, né sông và núi lửa
    r10 = SPOTS[BOSS][2]
    boss = (pts[9][0], pts[9][1] - (clears[9][1] + r10 - 40))
    if boss[1] - r10 < z.TOP_SEA_Y + 10:
        z.warn("núi lửa chạm biển trên")
    obstacles = [(p, z.STREAM_W / 2 + 6) for p in stream[::3]] + [(boss, r10)]
    nums = [i + 1 for i in range(9) if SPOTS[i + 1][1] != "bridge"]
    radius = {k: SPOTS[k][2] for k in nums}
    cands = {k: z.candidates(road, stops[k - 1], radius[k], clears, obstacles, bottom=(k == 1)) for k in nums}
    for k in nums:
        if not cands[k]:
            z.warn(f"không có chỗ cho địa danh {k} ({SPOTS[k][0]})")
    chosen = z.assign({k: c for k, c in cands.items() if c}, radius)
    chosen[BOSS] = boss

    for num in range(1, 11):
        name, kind, r, _ = SPOTS[num]
        if kind == "bridge" or num not in chosen:
            continue
        c = chosen[num]
        side = 1 if c[0] > road.x_at(c[1]) else -1
        spots[num] = {"c": c, "r": r, "kind": kind, "side": side}
    # 6: lạch dung nham từ hồ ra mép cùng phía
    if POND in spots:
        c, side = spots[POND]["c"], spots[POND]["side"]
        edge_x = W + 60 if side > 0 else -60
        creek = z.wavy(c, (edge_x, c[1] - 40), 18, 26)
        z.check_water("lạch hồ dung nham", creek, z.STREAM_W / 2, road)
        for num, sp in spots.items():
            if num != POND and "c" in sp and min(math.dist(p, sp["c"]) for p in creek) < sp["r"] + z.STREAM_W / 2:
                z.warn(f"lạch hồ dung nham chạm địa danh {num}")
        water["streams"].append(creek)
        spots[POND]["edge"] = "right" if side > 0 else "left"
    for num, sp in sorted(spots.items()):
        if "c" in sp:
            c = sp["c"]
            print(f"  địa danh {num:2d} {SPOTS[num][0]}: ({c[0]:.0f}, {c[1]:.0f}) đoạn {seg_of(c[1]) + 1}, "
                  f"{'phải' if sp['side'] > 0 else 'trái'} đường")
    b = spots[BRIDGE]["bridge"]
    print(f"  cầu đá (2): ({b[0]:.0f}, {b[1]:.0f}) đoạn {seg_of(b[1]) + 1}")
    return road, stops, pts, spots, water


def draw_guide(road, pts, spots, water):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im, "RGBA")
    z.hatch(d, (0, 0, W, H), GROUND, 73, 9000)
    beach = z.shore(z.BEACH_Y, 14, 70, 0.9)
    d.polygon(beach + [(W, H), (0, H)], fill=z.SAND)
    d.line(beach, fill=z.INK, width=4)
    for st in water["streams"]:
        for w, col in ((z.STREAM_W + 10, z.INK), (z.STREAM_W, LAVA)):
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
    b = spots[BRIDGE]
    (bx, by), (nx, ny) = b["bridge"], b["dir"]
    tx, ty = -ny, nx
    hw, hl = z.ROAD_W / 2 + 18, 38
    poly = [(bx + nx * hw + tx * hl, by + ny * hw + ty * hl), (bx - nx * hw + tx * hl, by - ny * hw + ty * hl),
            (bx - nx * hw - tx * hl, by - ny * hw - ty * hl), (bx + nx * hw - tx * hl, by + ny * hw - ty * hl)]
    d.polygon(poly, fill=STONE, outline=z.INK, width=5)
    z.label(d, (bx, by), str(BRIDGE), 52)
    for num, sp in spots.items():
        if "c" not in sp:
            continue
        c, r = sp["c"], sp["r"]
        if sp["kind"] == "land":
            d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=z.SPOT)
            z.dashed_circle(d, c, r, z.INK)
        elif sp["kind"] == "boss":
            z.disc(d, c, r, VOLCANO)
        else:
            z.disc(d, c, r, LAVA)
        z.label(d, c, str(num))
    return im


# ---------- gói gửi GPT ----------

def seg_spots(k, spots):
    out = []
    for num, sp in sorted(spots.items()):
        y = sp["c"][1] if "c" in sp else sp["bridge"][1]
        if seg_of(y) == k:
            out.append(num)
    return out


def spot_line(num, spots):
    text = SPOTS[num][3]
    if num == POND:
        text = text.format(edge=spots[POND]["edge"])
    return f"{num} {text};"


def stream_dir(water):
    s = water["streams"][0]
    return ("right", "left") if s[0][0] > s[-1][0] else ("left", "right")


LAVA_LOOK = ("LAVA is a flat orange and yellow surface with dark red crust lines and a wobbly ink bank of black rock; no glow, no "
             "bubbles, no splashes, no smoke (the game animates it).")


def water_lines(k, spots, water):
    lines = []
    if k == 0:
        lines.append("the sea along the bottom edge behind a shore of dark sand and round black pebbles (the journey starts at the "
                     "water's edge);")
    if seg_of(spots[BRIDGE]["bridge"][1]) == k:
        a, b = stream_dir(water)
        lines.append(f"a river of lava that crosses the whole image from the {a} edge to the {b} edge and passes under the road at "
                     f"the stone bridge of spot {BRIDGE};")
    if POND in spots and seg_of(spots[POND]["c"][1]) == k:
        lines.append(f"spot {POND} is a round pool of lava with stone lotus leaves; its small lava creek runs off the "
                     f"{spots[POND]['edge']} edge;")
    if k == NSEG - 1:
        lines.append("a strip of sea along the top edge beyond the northern tip of the island, behind the volcano.")
    return lines


GROUND_TEXT = (
    "GROUND: no island outline on the sides: the land runs off the left and right edges. The ground is warm red-orange coloured-pencil "
    "hatching like the old Fire island map, mixed with patches of darker red-brown earth, cracks in the ground with a little orange "
    "lava inside, scattered black cinders and small dry grass tufts. On both sides of the road, low raised terraces with short cliff "
    "faces of dark basalt (top in the ground colour, side in dark grey-brown hatching) give the map depth. Clusters of charred black "
    "trees with round orange leaf crowns, dry thorny bushes, black boulders, small red crystals and a few yellow sulfur rocks frame "
    "the road edges closely. Small props along the road edges: stone lanterns, empty iron braziers, short fences of black stone, a "
    "wooden signpost without writing, little stone cairns, prayer flags without writing. Dense, but every tree, rock and prop is a "
    "chunky doodle with a clear silhouette; no tiny noisy details, no 3D, no realistic rendering.")

CODES = ("The sketch is only a colour-coded plan: light orange-brown = ground, pale sand with an ink edge = road, blue = sea, orange "
         "with an ink edge = lava, grey spot with a number = a landmark on land, orange spot with a number = a landmark in a lava pool, "
         "dark red-brown spot with a number = the volcano, dark grey bar across the road = the stone bridge. Do not copy its flat "
         "colours, its numbers or its dashed outlines.")

RULES = ("Keep the road and the landmarks between x = 130 and x = 894 (narrow phones cut the outer strips); the outer strips have only "
         "ground, trees and rocks.\n"
         "Moving things are added later as animated sprites, so do NOT draw: smoke, steam, flames, flying sparks or embers, glows or "
         "light halos, heat shimmer, lava bubbles or splashes, sparkles, foam splashes, breaking wave crests.\n"
         "No text, no letters, no numbers, no signs with writing, no creatures, no people.")


def sketch_path(k):
    return PACK / f"bo_cuc_{k + 1}.png"


def prompt_path(k):
    return PACK / f"luot_{k + 1}.txt"


def save_path(k):
    return WORK / "tai_ve" / f"doan_{k + 1}.png"


OLD_EN = ("the old small map of this same Fire island: copy its colours and the look of its objects (warm red-orange hatched "
          "ground, black rocks, cracks in the ground, charred trees with orange crowns, the orange lava river, the round stone "
          "furnace, the lotus temple with red roofs, the volcano, the wooden pier); ignore its layout, its thin path, its island "
          "outline, its empty background, its cream circles and its golden wheel symbols")
OLD_VI = ("bản đồ đảo Hỏa 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền đỏ cam gạch chì, đường mòn mảnh có 8 vòng tròn "
          "kem, sông dung nham cam, núi lửa có bánh xe vàng trên đỉnh, cổng bánh xe, lò đá tròn, chùa sen mái đỏ, cây cháy tán cam, "
          "đất nứt, đá đen, bến gỗ ở đáy; lấy màu và dáng đồ vật (không lấy bánh xe vàng)")


def refs(k, spots):
    """ảnh mẫu GPT mở của lượt k: [(vai, đường dẫn, câu cho GPT, mô tả cho người dùng)]"""
    sk = ("sketch", sketch_path(k), "the layout sketch of the image you draw now: follow it exactly" +
          (f"; its bottom {OV} px strip is not a sketch but the top {OV} px of image 1, already painted" if k else ""),
          f"bố cục đoạn {k + 1} (1024 × 1536, nền cam đất nhạt)" + (f"; dải {OV} px ở đáy là dải đỉnh của đoạn {k}" if k else "") +
          "; " + seg_desc(k, spots))
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
             f"đoạn {k} bản đồ đảo Hỏa đã duyệt (1024 × 1536)"),
            sk, old]


def instructions(k, spots, water):
    rs = refs(k, spots)
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
        text += ("WHAT THIS IS: part 1 of 3 (the bottom part) of one long vertical map of the Fire island, a volcanic island, for a "
                 "vertical mobile game. The player scrolls up the map from the dark shore at the bottom to the boss at the volcano "
                 "at the top. The three parts are drawn one after another and stacked. Part 2 repeats the top "
                 f"{OV} px of this image as its bottom strip, so keep the top {OV} px of this image plain: road, ground, a few bushes "
                 "and rocks, no landmark, no lava.\n\n"
                 f"Draw a vertical 1024 x 1536 image in the rendering and map construction of image {idx['style']} with the colours "
                 f"and objects of image {idx['old']}: a warm red-orange volcanic island, not a green forest island. Outlines and "
                 f"hatching as bold as in image {idx['style']}.\n\n")
    else:
        part = "the middle part" if k == 1 else "the top part"
        text += (f"WHAT THIS IS: part {k + 1} of 3 ({part}) of one long vertical map of the Fire island, a volcanic island, for a "
                 f"vertical mobile game. The player scrolls up the map from the dark shore at the bottom to the boss at the volcano "
                 f"at the top; your image goes right above image {idx['prev']}.\n\n"
                 f"Draw a vertical 1024 x 1536 image in exactly the style of image {idx['prev']}. Image {idx['old']} only shows how "
                 f"this island's objects look (the lotus temple, the volcano); copy the drawing of image {idx['prev']}, not image "
                 f"{idx['old']}'s.\n\n"
                 f"JOIN: the bottom {OV} px of your image must show the same scene as the painted bottom strip of {sk}, at the same "
                 f"place: the road at the same position and width, the same ground, trees and rocks. Then continue the map upward "
                 f"following the sketch, so image {idx['prev']} and your image join into one picture without a seam. Where the "
                 f"painted strip ends ({OV} px above the bottom edge) there must be no visible line or step: both edges of the road, "
                 f"the hatching, the colours and any object crossing that height continue smoothly.\n")
        if k == 1:
            text += (f"Part 3 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px plain: road, ground, "
                     "a few bushes and rocks, no landmark, no lava.\n")
        text += "\n"
    text += (f"LAYOUT: copy {sk} exactly: the same road path and width, the same round clearings, the same lava and water shapes, "
             f"every landmark on its numbered spot. {CODES}\n\n")
    road = z.ROAD_TEXT
    if k == 0:
        road += " The road starts at the water's edge on the shore at the bottom and leaves the top edge exactly where the sketch does."
    elif k == 1:
        road += " The road enters at the bottom and leaves the top edge exactly where the sketch does."
    else:
        road += " The road enters at the bottom and ends in the big round arena near the top."
    text += f"{road}\n\n{GROUND_TEXT}\n\n"
    wl = water_lines(k, spots, water)
    if wl:
        sea = "the sea is blue with a wobbly ink bank and white ripple scribbles. " if k in (0, NSEG - 1) else ""
        text += ("WATER AND LAVA: " + sea + LAVA_LOOK + "\n" + "\n".join("- " + s for s in wl) + "\n")
        if k == 1 and not any("river" in s or "pool" in s for s in wl):
            text += "No other lava in this part.\n"
        text += "\n"
    else:
        text += "WATER AND LAVA: no water and no lava in this part, except small cracks in the ground.\n\n"
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

def seg_desc(k, spots):
    parts = []
    if k == 0:
        parts.append("đáy là bờ cát sẫm sỏi đen và biển, đường bắt đầu từ mép nước")
    for num in seg_spots(k, spots):
        sp = spots[num]
        if num == BRIDGE:
            parts.append(f"dải cam (dung nham) chạy ngang hết bề ngang, thanh xám số {BRIDGE} ngang đường là cầu đá")
        elif sp["kind"] == "land":
            parts.append(f"chấm xám số {num} là chỗ {SPOTS[num][0]}")
        elif sp["kind"] == "boss":
            parts.append(f"đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm nâu đỏ sẫm số {num} sau bãi là núi lửa")
        else:
            parts.append(f"chấm cam số {num} là hồ dung nham {SPOTS[num][0]}, lạch dung nham chảy ra mép "
                         f"{'phải' if sp.get('edge') == 'right' else 'trái'}")
    if k == NSEG - 1:
        parts.append("dải biển dọc mép trên")
    return "; ".join(parts)


def guide_md(spots, water):
    p = lambda *a: str(Path(*a))  # noqa: E731
    lines = [
        "# Gói gửi GPT: bản đồ dài đảo Hỏa 70 ải (`zone_hoa_70`)",
        "",
        f"Sinh bằng `{p(HERE, 'build_zone70_hoa.py')}`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Hỏa mới cho 70 ải, cùng "
        f"khuôn bản đồ dài đảo Thủy, đảo Mộc: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ "
        f"{W} × {H}. Đường cát rộng lượn chữ S (lượn phải trước, ngược đảo Mộc) từ bến đá đen lên bãi đấu boss dưới núi lửa, 10 bãi "
        f"tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường. "
        f"Khói, lửa, tàn lửa, dòng dung nham chảy là phần động game thêm sau, GPT không vẽ.",
        "",
        "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. "
        "Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude \"duyệt đoạn <k> đảo Hỏa\"; Claude soi, lưu "
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
                         for i, (_, path, _, desc) in enumerate(refs(k, spots)))
        lines.append(f"| {k + 1}: {names[k]}, địa danh {nums} | {prompt} | {imgs} | `{save_path(k)}` |")
    lines += ["", f"Bản duyệt Claude lưu ở `{p(WORK, 'doan_<k>.png')}`. Không để ảnh vào `{p(HERE, 'inbox')}` (menu nhập ảnh sẽ chép "
              f"nguyên khổ vào game).", ""]
    lines += ["## Địa danh", "", "| Số | Chặng (ải) | Vẽ gì |", "|---|---|---|"]
    vi = {1: "đá bazan đen mặt sáu cạnh, bến gỗ ngắn trên cọc đen, thuyền gỗ cũ kéo lên bờ cát sẫm cạnh đầu đường",
          2: "cầu vòm đá bazan qua sông dung nham, rộng bằng đường, lan can đá thấp; đá đen, cây cháy hai bờ",
          3: "rừng cây cháy đen, vỏ có vết nứt cam, tán lá tròn cam đỏ, xen đá đen",
          4: "sườn đá xám xếp lớp, ba lỗ phun viền lưu huỳnh vàng; không vẽ khói (game thêm)",
          5: "lò vòm tròn gạch đá xám có cửa vòm tối, cạnh bệ thiền đá nhỏ có lư hương đồng và hai đèn đá",
          6: "hồ dung nham tròn có lá sen đá, chùa nhỏ mái đỏ cong có hoa sen vàng trên nóc đứng trên mỏm đá sau hồ; lạch "
             "dung nham chảy ra mép",
          7: "lò rèn mái tôn đen, ống khói đá cao, đe lớn, giá khiên và giáo gai thép; vài gai sắt cắm quanh",
          8: "rừng cây xoắn lạ, tán lá hình ngọn lửa (lá, không phải lửa) cam, hồng, tím; vài pha lê tím tròn giữa rễ",
          9: "miệng hang trong đồi đá sẫm, hồng ngọc đỏ to tua tủa",
          10: "núi lửa sẫm ngay sau bãi đấu boss, miệng rộng đầy dung nham, vài dòng dung nham chảy xuống hai bên sườn (không "
              "chạm bãi), hai tượng đá hộ vệ nhỏ ở chân núi, đỉnh chạm dải biển trên"}
    heads = z.HEADS + [71]
    for num in range(1, 11):
        rng = f"{heads[num - 1]}–{heads[num] - 1}" if heads[num] - 1 > heads[num - 1] else f"{heads[num - 1]}"
        lines.append(f"| {num} | {SPOTS[num][0]} ({rng}) | {vi[num]} |")
    lines += [
        "",
        "## Soi trước khi nhắn Claude",
        "",
        "- Đảo núi lửa đỏ cam (không phải đảo rừng xanh lá như ảnh mẫu đảo Mộc), nét và cách dựng giống ảnh mẫu.",
        "- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường và các bãi tròn **trống**.",
        "- Địa danh đúng số, đứng sát đường, không đè lên đường.",
        "- Dung nham là mảng cam vàng phẳng có vân vỏ sẫm, không quầng sáng, không bọt, không khói.",
        "- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).",
        f"- Lượt 1, 2: dải {OV} px trên cùng chỉ có đường, đất, bụi, đá.",
        "- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không khói, lửa, tàn lửa, lấp lánh (game thêm).",
        "",
        "## Sửa nhanh (gõ vào chat)",
        "",
        "| Lỗi | Gõ |",
        "|---|---|",
        "| Ra màu xanh lá, cây rừng như đảo Mộc | `Same layout, but this is the red-orange volcanic Fire island: warm red-orange hatched "
        "ground, charred trees with orange crowns, black basalt rocks, red crystals; no green grass, no green forest trees.` |",
        "| Có khói, lửa, quầng sáng | `Same image, but remove all smoke, flames, sparks, embers and glows. Lava stays a flat orange and "
        "yellow surface with dark crust lines.` |",
        "| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road and the round clearings completely empty: remove everything "
        "standing on them.` |",
        "| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round "
        "clearings.` |",
        "| Có số, chữ | `Same image without any numbers, letters or text.` |",
        "| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |",
        f"| Dải đáy không nối với đoạn trước | `Redraw it so the bottom {OV} px show exactly the same scene as the painted bottom strip of "
        "the sketch: same road position and width, same trees and rocks.` |",
        "| Dung nham hay chân núi lửa đè lên bãi đấu | `Same image, but the volcano and its lava stay behind the arena: the round arena "
        "is completely empty.` |",
        "| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, "
        "wobbly ink outlines, every tree and rock a chunky doodle with a clear silhouette. Keep the same layout.` |",
        "",
    ]
    return "\n".join(lines)


# ---------- toạ độ cho game, cho gói nền trận ----------

def save_json(road, stops, pts, spots):
    path = [road.at(s) for s in range(0, int(road.length) + 1, 24)] + [road.p[-1]]
    stages = []
    for i, p in enumerate(pts):
        st = {"idx": z.HEADS[i], "x": round(p[0] / W, 4), "y": round(p[1] / H, 4), "road": round(stops[i] / road.length, 4)}
        sp = spots.get(i + 1, {})
        if "c" in sp:
            st["spot"] = [round(sp["c"][0] / W, 4), round(sp["c"][1] / H, 4), round(sp["r"] / W, 4)]
            st["spotSide"] = sp["side"]
        elif "bridge" in sp:
            st["bridge"] = [round(sp["bridge"][0] / W, 4), round(sp["bridge"][1] / H, 4)]
        stages.append(st)
    data = {
        "note": "Bố cục dự kiến của bản đồ dài đảo Hỏa (build_zone70_hoa.py); x, y từ 0 tới 1 theo bản đồ ghép, y từ trên. Có ảnh "
                "thật thì dò lại đường.",
        "map": [W, H], "segments": NSEG, "overlap": OV, "displayWidth": 1.27, "roadWidth": round(z.ROAD_W / W, 4),
        "pipGap": round(z.GAP, 1),
        "path": [[round(x / W, 4), round(y / H, 4)] for x, y in path],
        "stages": stages,
    }
    (GUIDES / "zone70_hoa.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- sửa chỗ nối của đoạn GPT trả về ----------
# Đảo Hỏa đoạn 2 (2026-11-05): GPT giữ nguyên dải dán (trùng từng điểm ảnh) nhưng chỗ phần nó vẽ gặp dải dán có một dải khoảng 25
# hàng phủ vạch sáng dọc mờ (giữ nguyên theo cột, nét gạch vẫn còn dưới), hai mép đường có mẩu mực thừa và lệch 12–21 px. Tô lấp
# (cv2.inpaint) làm nhòe vân; chép vân từ trên xuống kéo cả đá vào dải. Cách dùng: trừ mẫu vạch theo cột, nắn mép đường.

FIX_TOP, FIX_CORE, FIX_ROAD = 36, 18, 28  # số hàng sửa vạch phía trên mép dải dán, số hàng lõi để đo mẫu vạch, số hàng nắn mép đường


def va_noi(a, k, road):
    """sửa chỗ nối của đoạn k (1, 2 = đoạn giữa, trên; a: mảng float H x W x 3 của ảnh GPT, sửa tại chỗ)"""
    from scipy.ndimage import median_filter
    seam = SH - OV  # từ hàng này xuống là dải dán từ đoạn dưới
    # 1. vạch sáng dọc: phần dư sau lọc trung vị theo hàng; trung vị qua các hàng lõi (nét gạch chéo đổi cột theo hàng nên bị loại)
    # ra mẫu vạch theo cột; mỗi hàng trừ mẫu theo độ mạnh hồi quy được
    rows = range(seam - FIX_TOP, seam)
    res = np.stack([a[y] - median_filter(a[y], size=(9, 1)) for y in rows])
    stripe = np.median(res[FIX_TOP - FIX_CORE:], axis=0)
    lum = stripe.mean(axis=1)
    strength = []
    for i, y in enumerate(rows):
        s = float(np.dot(res[i].mean(axis=1), lum) / (np.dot(lum, lum) + 1e-9))
        strength.append(min(max(s, 0.0), 1.3))
        a[y] -= strength[-1] * stripe
    print(f"  vạch dọc chỗ nối: lệch cột {lum.std():.1f}, độ mạnh lớn nhất {max(strength):.2f} (0 là không có)")
    # 2. mép đường: các hàng sạch hai đầu dải được kéo ngang cho mép nằm trên đoạn thẳng nối mép trên và mép dưới, chỉ quanh mặt đường
    b0, b1 = seam - FIX_ROAD, seam
    mask = z.sand_mask(a.astype(int))
    cx = road.x_at(z.seg_top(k) + seam)
    top, bot = z.road_run(mask[b0 - 1], cx), z.road_run(mask[b1], cx)
    if not top or not bot:
        z.warn(f"đoạn {k + 1}: không thấy mép đường ở chỗ nối, chưa nắn")
        return
    up = [(y, z.road_run(mask[y], cx)) for y in range(b0 - 8, b0)]
    dn = [(y, z.road_run(mask[y], cx)) for y in range(b1, b1 + 8)]
    up, dn = [s for s in up if s[1]], [s for s in dn if s[1]]
    src = a.copy()
    for y in range(b0, b1):
        t = (y - b0 + 1) / (FIX_ROAD + 1)
        L, R = top[0] + (bot[0] - top[0]) * t, top[1] + (bot[1] - top[1]) * t
        pair = []
        for group in (up, dn):
            sy, (sl, sr) = group[(y - b0) % len(group)]
            pair.append(z.warp_row(src[sy], [0, L - 40, L, R, R + 40, W - 1], [0, sl - 40, sl, sr, sr + 40, W - 1]))
        tt = t * t * (3 - 2 * t)
        row = pair[0] * (1 - tt) + pair[1] * tt
        lo, hi = int(L - 16), int(R + 17)
        wgt = np.ones(hi - lo)
        wgt[:8] = np.linspace(0, 1, 8)
        wgt[-8:] = np.linspace(1, 0, 8)
        a[y, lo:hi] = a[y, lo:hi] * (1 - wgt[:, None]) + row[lo:hi] * wgt[:, None]
    print(f"  mép đường chỗ nối: trên {top}, dưới {bot}; đã nắn {FIX_ROAD} hàng")


# ---------- ghép 3 đoạn đã duyệt (như build_zone70_moc.ghep) ----------

FEATHER = 24  # nửa bề cao vùng trộn quanh đường cắt giữa dải chồng


def ghep():
    """ghép doan_1..3 đã duyệt thành bản đồ W x H (zones/hoa70/zone_hoa70.png). Mỗi chỗ nối: dò dời dọc của đoạn trên cho dải chồng
    khớp (m.band_offset), cắt ở giữa dải chồng và trộn FEATHER hàng hai bên. Đoạn trên cùng dời xuống thì hàng trống trên đỉnh lấy
    hàng đầu của nó (biển, game làm trong suốt)."""
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
    out = WORK / "zone_hoa70.png"
    Image.fromarray(img.clip(0, 255).astype("uint8")).save(out)
    (WORK / "ghep.json").write_text(json.dumps({"tops": tops}, ensure_ascii=False), encoding="utf-8")
    print(f"Đã ghi {out} ({W} x {H}); đỉnh các đoạn {tops}")


# ---------- dò đường thật trên bản đồ ghép ----------
# Như đảo Mộc: tâm đường theo hàng (bắt lại sau cầu đá), 10 bãi ải là chỗ bề rộng mặt cát đo vuông góc vượt ngưỡng. Sông và lạch dung
# nham lấy đường dự kiến: đoạn 1, 2 vẽ sát bố cục (đường lệch trung vị 4 và 1,5 px; đã chồng soi, sông nằm trong lòng sông vẽ). Địa danh,
# chỗ phần động đo tay trên bản đồ ghép (px bản đồ).

SPOTS_REAL = {1: ((200, 4080), 125), 3: ((830, 3472), 130), 4: ((230, 3312), 150), 5: ((760, 3110), 130), 6: ((260, 2570), 170),
              7: ((730, 2150), 170), 8: ((285, 1700), 150), 9: ((360, 820), 140), 10: ((530, 190), 190)}
BRIDGE_REAL = (420, 3742)
# phần động (IslandAnim, khoá zone_hoa): (kiểu, x, y, cỡ px bản đồ)
ANIM = [
    ("smoke", 550, 50, 120),  # miệng núi lửa
    ("sparkle", 600, 60, 30),
    ("smoke", 260, 3244, 50), ("smoke", 190, 3300, 44), ("smoke", 350, 3360, 44),  # ba lỗ phun Sườn Núi Khói
    ("flame", 770, 3080, 40),  # cửa lò Lò Lửa Thiền
    ("smoke", 740, 3164, 30),  # lư hương
    ("smoke", 850, 1970, 50),  # ống khói lò rèn
    ("sparkle", 190, 2390, 30),  # hoa sen vàng trên nóc chùa
    ("sparkle", 200, 1790, 30), ("sparkle", 344, 1790, 28),  # pha lê tím Rừng Lửa Ảo
    ("sparkle", 370, 730, 30), ("sparkle", 270, 870, 28), ("sparkle", 440, 880, 28),  # hồng ngọc
    ("wave", 230, H - 30, 90), ("wave", 790, H - 40, 90), ("wave", 300, 24, 80), ("wave", 800, 30, 80),
]
LAVA_W = (0.012, 0.009)  # bề rộng dòng tàn lửa: sông, lạch (theo bề ngang ảnh; IslandAnim.Flow)


def that():
    """dò đường, 10 bãi ải trên zones/hoa70/zone_hoa70.png; ghi zones/hoa70/that.json và ảnh soi soi_that.png"""
    from PIL import ImageFilter
    img = np.array(Image.open(WORK / "zone_hoa70.png").convert("RGB")).astype(int)
    sand = z.sand_mask(img)
    sand = np.asarray(Image.fromarray((sand * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3))
                      .filter(ImageFilter.MinFilter(3))) > 0
    with contextlib.redirect_stdout(io.StringIO()):
        road0, stops0, pts0, _, water0 = layout()
    y0 = 3950  # giữa bãi ải 1 và cầu đá
    path = m.resample(m.trace_road(sand, y0, road0.x_at(y0)), 6)
    d = [0.0]
    for a_, b_ in zip(path, path[1:]):
        d.append(d[-1] + math.dist(a_, b_))
    L = d[-1]
    r_, g_, b_ = img[..., 0], img[..., 1], img[..., 2]
    loose = (r_ > 185) & (g_ > 150) & (b_ < 205) & (r_ - b_ > 35) & (r_ >= g_ - 4)
    loose = np.asarray(Image.fromarray((loose * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5))
                       .filter(ImageFilter.MinFilter(5))) > 0
    P = np.array(path)
    ts = np.arange(-200, 201)
    prof = []
    for i_ in range(len(P)):
        t = P[min(len(P) - 1, i_ + 4)] - P[max(0, i_ - 4)]
        tl = math.hypot(*t) or 1
        nx, ny = -t[1] / tl, t[0] / tl
        xs = np.clip(np.round(P[i_, 0] + nx * ts).astype(int), 0, W - 1)
        ys = np.clip(np.round(P[i_, 1] + ny * ts).astype(int), 0, H - 1)
        v = loose[ys, xs]
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
    data = {
        "path": [[round(x, 1), round(y, 1)] for x, y in path],
        "stops": [round(d[k], 1) for k in stops], "length": round(L, 1),
        "stages": [[round(path[k][0], 1), round(path[k][1], 1)] for k in stops],
        "streams": [[[round(x, 1), round(y, 1)] for x, y in s] for s in water0["streams"]],
    }
    (WORK / "that.json").write_text(json.dumps(data), encoding="utf-8")
    soi = Image.fromarray(img.astype("uint8"))
    dr = ImageDraw.Draw(soi)
    dr.line([tuple(p) for p in path], fill=(255, 0, 255), width=4)
    for k in stops:
        x, y = path[k]
        dr.ellipse((x - 30, y - 30, x + 30, y + 30), outline=(0, 255, 0), width=5)
    for s in data["streams"]:
        dr.line([tuple(p) for p in s], fill=(0, 0, 255), width=4)
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
    out[BRIDGE] = {"bridge": BRIDGE_REAL}
    return out


def anim_spec(water):
    """phần động trên ảnh (IslandAnim, khoá zone_hoa): khói, lửa, lấp lánh, sóng (ANIM), tàn lửa trôi dọc sông và lạch dung nham.
    Toạ độ chia W, H; cỡ chia W"""
    rivers = [("lava", [(min(max(x, 2), W - 2), y) for x, y in st[::3]], LAVA_W[min(i, 1)]) for i, st in enumerate(water["streams"])]
    return {
        "items": [{"k": k, "x": round(x / W, 4), "y": round(y / H, 4), "s": round(sz / W, 4)} for k, x, y, sz in ANIM],
        "rivers": [{"k": k, "w": rw, "pts": [[round(x / W, 4), round(y / H, 4)] for x, y in pts]} for k, pts, rw in rivers],
    }


def xuat(art_out=None, zones_json=None):
    """đưa bản đồ đã ghép vào game theo đường dò được (that.json): Assets/03 Art/Islands/zone_hoa.png (biển hai mép trong suốt; thay
    bản đồ 8 ải cũ), khoá zone_hoa trong island_anim.json, đảo hoa trong zones.json (nodes = 10 bãi ải dò được, path = tâm đường thật
    tới giữa bãi đấu boss, stops, plates). Sau đó chạy menu Unity PokiClash/Nhập dữ liệu. art_out, zones_json: ghi chỗ khác để thử."""
    art_out = Path(art_out or z.ART_OUT)
    zones_json = Path(zones_json or z.ZONES_JSON)
    th = json.loads((WORK / "that.json").read_text(encoding="utf-8"))
    a = np.array(Image.open(WORK / "zone_hoa70.png").convert("RGB"))
    alpha = z.sea_alpha(a)
    rgba = np.dstack([a, (alpha * 255).round().astype("uint8")])
    art_out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(art_out / "zone_hoa.png")
    print(f"Đã ghi {art_out / 'zone_hoa.png'} ({W} x {H}); biển trong suốt {(alpha < 0.5).mean() * 100:.1f}% ảnh")

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
    anim["zone_hoa"] = anim_spec(water)
    nl = "\r\n" if b"\r\n" in anim_path.read_bytes() else "\n"
    anim_path.write_text(json.dumps(anim, ensure_ascii=False, indent=1), encoding="utf-8", newline=nl)
    print(f"Đã ghi khoá zone_hoa trong {anim_path}: {len(anim['zone_hoa']['items'])} món, {len(anim['zone_hoa']['rivers'])} dòng")

    src_json = zones_json if zones_json.exists() else z.ZONES_JSON
    zl = "\r\n" if b"\r\n" in src_json.read_bytes() else "\n"  # giữ kiểu xuống dòng của file (máy autocrlf ghi CRLF)
    data = json.loads(src_json.read_text(encoding="utf-8"))
    zd = next(x for x in data["zones"] if x["id"] == "hoa")
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
    print(f"Đã ghi đảo hoa trong {zones_json}: 10 ải tướng, đường {len(path)} điểm, bảng tên {plates}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar="K [ANH]",
                    help="lưu đoạn K (1..3) GPT trả về (mặc định ảnh mới nhất tai_ve/doan_K*.png) rồi dựng lại gói")
    ap.add_argument("--ghep", action="store_true", help="ghép 3 đoạn đã duyệt thành zones/hoa70/zone_hoa70.png")
    ap.add_argument("--that", action="store_true", help="dò đường, bãi ải thật trên bản đồ đã ghép (that.json)")
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
            va_noi(arr, k - 1, road)
            im = Image.fromarray(arr.clip(0, 255).astype("uint8"))
        WORK.mkdir(parents=True, exist_ok=True)
        im.save(WORK / f"doan_{k}.png")
        print(f"Đã lưu {WORK / f'doan_{k}.png'}")
    road, stops, pts, spots, water = layout()
    guide = draw_guide(road, pts, spots, water)
    GUIDES.mkdir(exist_ok=True)
    guide.save(GUIDES / "L_zone70_hoa.png")
    save_json(road, stops, pts, spots)
    build_pack(spots, water, guide)
    print(f"Đã ghi {GUIDES / 'L_zone70_hoa.png'}, {GUIDES / 'zone70_hoa.json'}, gói {PACK}")
    if warnings:
        print(f"{len(warnings)} cảnh báo, xem trên")


if __name__ == "__main__":
    main()
