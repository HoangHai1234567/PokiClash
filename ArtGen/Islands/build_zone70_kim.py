# Bản đồ dài đảo Kim 70 ải: dựng ảnh bố cục và gói gửi GPT, như build_zone70_hoa.py (đảo Hỏa). Dùng lại phần chung của
# build_zone70.py (đường chữ S, cỡ bản đồ 1024 x 4288 ghép 3 đoạn, chỗ địa danh) và band_offset của build_zone70_moc.py; không sửa
# các file đó.
# Khác đảo Hỏa:
# - đường lượn sang trái trước (như đảo Mộc, ngược đảo Hỏa), cùng độ cao 10 ải tướng;
# - sông nước xám xanh chạy ngang, đường qua cầu sắt có bánh răng đồng ngay sau ải 5 (chặng 2, Cầu Bánh Răng); hồ nước làm nguội
#   trước xưởng đúc chuông, lạch nước ra mép (chặng 6, Xưởng Đúc Chuông); núi thép có tháp chuông đứng sau bãi đấu boss, đỉnh chạm
#   dải biển trên;
# - ảnh mẫu nét là đoạn 1 bản đồ dài đảo Mộc đã duyệt (cùng game, nét và cách dựng đã chốt), màu và đồ vật lấy bản đồ Kim 8 ải cũ;
# - khói, hơi nước, tia lửa, lấp lánh, quầng sáng không vẽ: game có sẵn phần động smoke, sparkle, sóng (IslandAnim).
# Tên chặng theo IslandGen.Kim (Assets/01 Script/Editor/IslandGen.cs).
# Ghi: ArtGen/guides/L_zone70_kim.png (bố cục cả bản đồ), ArtGen/guides/zone70_kim.json (đường, ải tướng, địa danh; toạ độ 0..1 của
# bản đồ ghép, y từ trên), gói ArtGen/Islands/gui_gpt/zone_kim_70/ (luot_k.txt, bo_cuc_k.png, HUONG_DAN.md).
# Chạy: py -3 -I ArtGen/Islands/build_zone70_kim.py
# Duyệt đoạn k GPT đã lưu: --duyet k [ảnh] (mặc định ảnh mới nhất zones/kim70/tai_ve/doan_k*.png): lưu zones/kim70/doan_k.png rồi
# dựng lại gói (có đoạn k thì có file prompt lượt k+1, bố cục đoạn k+1 dán dải đỉnh của đoạn k).
# Đủ 3 đoạn: --ghep (zones/kim70/zone_kim70.png). Dò đường thật và đưa vào game (--that, --xuat như đảo Hỏa) viết khi có bản đồ
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
import build_zone70_moc as m  # noqa: E402  (band_offset; lúc nạp nó đặt z.FIRST = -1)

z.FIRST = -1  # chặng đầu lượn sang trái

W, SH, H, OV, NSEG = z.W, z.SH, z.H, z.OV, z.NSEG
GUIDES = z.GUIDES
PACK = HERE / "gui_gpt" / "zone_kim_70"
WORK = HERE / "zones" / "kim70"  # tai_ve/: ảnh GPT trả về; doan_k.png: đoạn đã duyệt
STYLE = HERE / "zones" / "moc70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Mộc đã duyệt
OLD = HERE / "zones" / "zone_kim.png"  # bản đồ Kim 8 ải đang dùng

BRIDGE, POND, BOSS = 2, 6, 10
AFTER = 150  # cầu cách tâm bãi ải 5 bao nhiêu px đường (về phía ải 10)

# màu ảnh bố cục (chỉ là mã màu cho GPT): đất xám xanh nhạt, nước xanh, núi thép xám sẫm, cầu đồng
GROUND = (196, 206, 216)
MOUNTAIN = (78, 84, 100)
BRONZE = (176, 122, 58)

# địa danh từng chặng: tên chặng (IslandGen.Kim), kiểu chỗ (land xám, water hồ nước, bridge cầu qua sông, boss núi thép sau bãi
# đấu), bán kính, câu cho GPT
SPOTS = {
    1: ("Cảng Sắt", "land", 100, "a small iron harbour beside the start of the road: a riveted iron dock crane with a big hook, "
                                 "stacked metal crates, a few barrels and a big iron anchor lying on the grey pebbles"),
    2: ("Cầu Bánh Răng", "bridge", 0, "the road crosses the river on a flat bridge of riveted iron plates, exactly as wide as the "
                                      "road, with a big bronze gear wheel standing upright at each end of the bridge beside the "
                                      "road; the bridge deck is part of the road and stays empty; grey stones and a few iron posts "
                                      "on both banks"),
    3: ("Rừng Lưỡi Liềm", "land", 105, "a grove of trees with silver-grey trunks and round crowns of long curved leaves shaped like "
                                       "sickle blades (leaves, not weapons), in steel blue and pale green, between a few grey rocks"),
    4: ("Tháp Canh Thép", "land", 105, "a tall watchtower of riveted steel girders with a small lookout cabin on top and a pointed "
                                       "spire like a lance tip, a few iron crates at its foot"),
    5: ("Gác Chuông Đồng", "land", 105, "a small open pavilion with a dark slate roof on four thick wooden posts on a square stone "
                                        "base, a big bronze bell hanging inside"),
    6: ("Xưởng Đúc Chuông", "water", 110, "a round pond of cooling water; at the back of the pond, on a rock, a bell foundry: a squat "
                                          "stone kiln with a short chimney, a big iron crucible full of molten bronze (a flat orange "
                                          "and yellow surface, no glow) and two bronze bells on wooden stands; a small stream "
                                          "leaves the pond and runs off the {edge} edge"),
    7: ("Mỏ Sắt Ngân", "land", 110, "a mine entrance with heavy wooden beams in a grey rock hill, a short rail track coming out of "
                                    "it with a mine cart full of shiny silver ore"),
    8: ("Thành Ba Kiếm", "land", 110, "a small fortress gate of grey stone blocks with two short towers and a closed iron door; in "
                                      "front of it three giant swords stuck point-down in the ground, with a red, a blue and a "
                                      "golden hilt"),
    9: ("Tổ Cánh Pha Lê", "land", 110, "a big round nest woven of bent steel rods on a rocky outcrop, with long pale-green crystal "
                                       "shards sticking out of its rim like feathers; the nest is empty"),
    10: ("Tháp Thiên Chung", "boss", 118, "the boss lair: the road ends in the big round empty arena; right behind it rises a tall "
                                          "steel-grey mountain with white snowy tips, and on its peak a big bell tower of stone and "
                                          "riveted steel with curved bronze roofs and a huge bronze bell hanging in its open top "
                                          "floor; two small stone statues of folded wings stand at the foot of the mountain on both "
                                          "sides behind the arena; the top of the tower reaches up to the sea at the top edge"),
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

    # 2: sông chạy ngang từ mép phải sang mép trái, qua đường ở cầu sắt ngay sau bãi ải 5 (trước bãi thì sông nằm sát bãi cát,
    # trông như chảy dọc bờ)
    sx = stops[BRIDGE - 1] + AFTER
    X = road.at(sx)
    stream = z.wavy((W + 40, X[1] + 70), X, 22, 23)[:-1] + z.wavy(X, (-40, X[1] - 50), 22, 24)
    z.check_water("sông", stream, z.STREAM_W / 2, road, (sx - 200, sx + 200))
    water["streams"].append(stream)
    n = road.normal(sx)
    spots[BRIDGE] = {"bridge": X, "dir": (n[0], n[1])}

    # núi thép (10) ngay sau bãi đấu boss; các địa danh khác chọn chỗ cùng lúc, né sông và núi
    r10 = SPOTS[BOSS][2]
    boss = (pts[9][0], pts[9][1] - (clears[9][1] + r10 - 40))
    if boss[1] - r10 < z.TOP_SEA_Y + 10:
        z.warn("núi thép chạm biển trên")
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
    # 6: lạch nước từ hồ ra mép cùng phía
    if POND in spots:
        c, side = spots[POND]["c"], spots[POND]["side"]
        edge_x = W + 60 if side > 0 else -60
        creek = z.wavy(c, (edge_x, c[1] - 40), 18, 26)
        z.check_water("lạch hồ xưởng đúc", creek, z.STREAM_W / 2, road)
        for num, sp in spots.items():
            if num != POND and "c" in sp and min(math.dist(p, sp["c"]) for p in creek) < sp["r"] + z.STREAM_W / 2:
                z.warn(f"lạch hồ xưởng đúc chạm địa danh {num}")
        water["streams"].append(creek)
        spots[POND]["edge"] = "right" if side > 0 else "left"
    for num, sp in sorted(spots.items()):
        if "c" in sp:
            c = sp["c"]
            print(f"  địa danh {num:2d} {SPOTS[num][0]}: ({c[0]:.0f}, {c[1]:.0f}) đoạn {seg_of(c[1]) + 1}, "
                  f"{'phải' if sp['side'] > 0 else 'trái'} đường")
    b = spots[BRIDGE]["bridge"]
    print(f"  cầu bánh răng (2): ({b[0]:.0f}, {b[1]:.0f}) đoạn {seg_of(b[1]) + 1}")
    return road, stops, pts, spots, water


def draw_guide(road, pts, spots, water):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im, "RGBA")
    z.hatch(d, (0, 0, W, H), GROUND, 73, 9000)
    beach = z.shore(z.BEACH_Y, 14, 70, 0.9)
    d.polygon(beach + [(W, H), (0, H)], fill=z.SAND)
    d.line(beach, fill=z.INK, width=4)
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
    b = spots[BRIDGE]
    (bx, by), (nx, ny) = b["bridge"], b["dir"]
    tx, ty = -ny, nx
    hw, hl = z.ROAD_W / 2 + 18, 38
    poly = [(bx + nx * hw + tx * hl, by + ny * hw + ty * hl), (bx - nx * hw + tx * hl, by - ny * hw + ty * hl),
            (bx - nx * hw - tx * hl, by - ny * hw - ty * hl), (bx + nx * hw - tx * hl, by + ny * hw - ty * hl)]
    d.polygon(poly, fill=BRONZE, outline=z.INK, width=5)
    z.label(d, (bx, by), str(BRIDGE), 52)
    for num, sp in spots.items():
        if "c" not in sp:
            continue
        c, r = sp["c"], sp["r"]
        if sp["kind"] == "land":
            d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=z.SPOT)
            z.dashed_circle(d, c, r, z.INK)
        elif sp["kind"] == "boss":
            z.disc(d, c, r, MOUNTAIN)
        else:
            z.disc(d, c, r, z.WATER)
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


WATER_LOOK = ("The river, the pond and the creek are cool grey-blue water with a wobbly ink bank lined with grey stones and a few "
              "white ripple scribbles; no foam, no splashes, no waterfalls.")


def water_lines(k, spots, water):
    lines = []
    if k == 0:
        lines.append("the sea along the bottom edge behind a shore of grey pebbles and pale sand (the journey starts at the water's "
                     "edge, at the iron harbour);")
    if seg_of(spots[BRIDGE]["bridge"][1]) == k:
        a, b = stream_dir(water)
        lines.append(f"a river that crosses the whole image from the {a} edge to the {b} edge and passes under the road at the "
                     f"iron gear bridge of spot {BRIDGE};")
    if POND in spots and seg_of(spots[POND]["c"][1]) == k:
        lines.append(f"spot {POND} is a round pond of cooling water in front of the bell foundry; its small creek runs off the "
                     f"{spots[POND]['edge']} edge;")
    if k == NSEG - 1:
        lines.append("a strip of sea along the top edge beyond the northern tip of the island, behind the bell tower mountain.")
    return lines


GROUND_TEXT = (
    "GROUND: no island outline on the sides: the land runs off the left and right edges. The ground is cool blue-grey coloured-pencil "
    "hatching like the old Metal island map, mixed with patches of darker slate grey, grey pebbles, small dry grass tufts and a few "
    "half-buried rusty gears and bolts. On both sides of the road, low raised terraces with short cliff faces of grey stone (top in "
    "the ground colour, side in darker grey hatching) give the map depth. Clusters of dark grey boulders, small grey peaks with white "
    "snowy tips, thin silver-grey trees with steel-blue crowns, iron posts and stacks of metal crates frame the road edges closely. "
    "Small props along the road edges: unlit iron lamp posts, an anvil, short iron fences, a wooden signpost without writing, little "
    "stone cairns, coils of chain, a rusty pipe. Dense, but every rock, tree and prop is a chunky doodle with a clear silhouette; no "
    "tiny noisy details, no 3D, no realistic rendering, no shiny chrome reflections.")

CODES = ("The sketch is only a colour-coded plan: light blue-grey = ground, pale sand with an ink edge = road, blue = sea and river "
         "water, grey spot with a number = a landmark on land, blue spot with a number = a landmark in a pond, dark slate spot with a "
         "number = the bell tower mountain, bronze bar across the road = the iron gear bridge. Do not copy its flat colours, its "
         "numbers or its dashed outlines.")

RULES = ("Keep the road and the landmarks between x = 130 and x = 894 (narrow phones cut the outer strips); the outer strips have only "
         "ground, rocks and trees.\n"
         "Moving things are added later as animated sprites, so do NOT draw: smoke, steam, sparks, flames, glows or light halos, "
         "sparkles or shine stars, foam splashes, breaking wave crests.\n"
         "No text, no letters, no numbers, no signs with writing, no creatures, no robots, no people.")


def sketch_path(k):
    return PACK / f"bo_cuc_{k + 1}.png"


def prompt_path(k):
    return PACK / f"luot_{k + 1}.txt"


def save_path(k):
    return WORK / "tai_ve" / f"doan_{k + 1}.png"


OLD_EN = ("the old small map of this same Metal island: copy its colours and the look of its objects (cool blue-grey hatched "
          "ground, small grey peaks with white tips, dark grey rocks, the grey-blue stream, the iron dock crane, the steel "
          "watchtower, the bell pavilion with a dark roof, the mine entrance with a rail cart, the foundry crucible, the nest of "
          "steel rods, the winged stone shrine); ignore its layout, its thin path, its island outline, its transparent "
          "background and its cream circles")
OLD_VI = ("bản đồ đảo Kim 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xám xanh gạch chì, đường mòn mảnh có 8 vòng "
          "tròn kem, núi xám đỉnh trắng, đá xám sẫm, suối xám xanh, cần cẩu sắt ở cảng, chòi canh thép, nhà chuông mái sẫm, cửa mỏ "
          "có xe goòng, lò đúc, tổ thép, miếu đá có cánh trên đỉnh; lấy màu và dáng đồ vật")


def refs(k, spots):
    """ảnh mẫu GPT mở của lượt k: [(vai, đường dẫn, câu cho GPT, mô tả cho người dùng)]"""
    sk = ("sketch", sketch_path(k), "the layout sketch of the image you draw now: follow it exactly" +
          (f"; its bottom {OV} px strip is not a sketch but the top {OV} px of image 1, already painted" if k else ""),
          f"bố cục đoạn {k + 1} (1024 × 1536, nền xám xanh nhạt)" + (f"; dải {OV} px ở đáy là dải đỉnh của đoạn {k}" if k else "") +
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
             f"đoạn {k} bản đồ đảo Kim đã duyệt (1024 × 1536)"),
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
        text += ("WHAT THIS IS: part 1 of 3 (the bottom part) of one long vertical map of the Metal island, an island of grey "
                 "stone, steel and bronze machinery, for a vertical mobile game. The player scrolls up the map from the iron "
                 "harbour at the bottom to the boss at the bell tower mountain at the top. The three parts are drawn one after "
                 f"another and stacked. Part 2 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px "
                 "of this image plain: road, ground, a few bushes and rocks, no landmark, no water.\n\n"
                 f"Draw a vertical 1024 x 1536 image in the rendering and map construction of image {idx['style']} with the colours "
                 f"and objects of image {idx['old']}: a cool blue-grey metal island, not a green forest island. Outlines and "
                 f"hatching as bold as in image {idx['style']}.\n\n")
    else:
        part = "the middle part" if k == 1 else "the top part"
        text += (f"WHAT THIS IS: part {k + 1} of 3 ({part}) of one long vertical map of the Metal island, an island of grey stone, "
                 f"steel and bronze machinery, for a vertical mobile game. The player scrolls up the map from the iron harbour at "
                 f"the bottom to the boss at the bell tower mountain at the top; your image goes right above image "
                 f"{idx['prev']}.\n\n"
                 f"Draw a vertical 1024 x 1536 image in exactly the style of image {idx['prev']}. Image {idx['old']} only shows how "
                 f"this island's objects look (the foundry, the mine, the nest, the peaks); copy the drawing of image "
                 f"{idx['prev']}, not image {idx['old']}'s.\n\n"
                 f"JOIN: the bottom {OV} px of your image must show the same scene as the painted bottom strip of {sk}, at the same "
                 f"place: the road at the same position and width, the same ground, trees and rocks. Then continue the map upward "
                 f"following the sketch, so image {idx['prev']} and your image join into one picture without a seam. Where the "
                 f"painted strip ends ({OV} px above the bottom edge) there must be no visible line or step: both edges of the road, "
                 f"the hatching, the colours and any object crossing that height continue smoothly.\n")
        if k == 1:
            text += (f"Part 3 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px plain: road, ground, "
                     "a few bushes and rocks, no landmark, no water.\n")
        text += "\n"
    text += (f"LAYOUT: copy {sk} exactly: the same road path and width, the same round clearings, the same water shapes, every "
             f"landmark on its numbered spot. {CODES}\n\n")
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
        text += ("WATER: " + sea + WATER_LOOK + "\n" + "\n".join("- " + s for s in wl) + "\n")
        if k == 1 and not any("river" in s or "pond" in s for s in wl):
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

def seg_desc(k, spots):
    parts = []
    if k == 0:
        parts.append("đáy là bờ sỏi xám, cát nhạt và biển, đường bắt đầu từ mép nước")
    for num in seg_spots(k, spots):
        sp = spots[num]
        if num == BRIDGE:
            parts.append(f"dải xanh (sông) chạy ngang hết bề ngang, thanh màu đồng số {BRIDGE} ngang đường là cầu sắt bánh răng")
        elif sp["kind"] == "land":
            parts.append(f"chấm xám số {num} là chỗ {SPOTS[num][0]}")
        elif sp["kind"] == "boss":
            parts.append(f"đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm xám đá sẫm số {num} sau bãi là núi thép có tháp chuông")
        else:
            parts.append(f"chấm xanh số {num} là hồ nước của {SPOTS[num][0]}, lạch nước chảy ra mép "
                         f"{'phải' if sp.get('edge') == 'right' else 'trái'}")
    if k == NSEG - 1:
        parts.append("dải biển dọc mép trên")
    return "; ".join(parts)


def guide_md(spots, water):
    p = lambda *a: str(Path(*a))  # noqa: E731
    lines = [
        "# Gói gửi GPT: bản đồ dài đảo Kim 70 ải (`zone_kim_70`)",
        "",
        f"Sinh bằng `{p(HERE, 'build_zone70_kim.py')}`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Kim mới cho 70 ải, cùng "
        f"khuôn bản đồ dài đảo Thủy, Mộc, Hỏa: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ "
        f"{W} × {H}. Đường cát rộng lượn chữ S (lượn trái trước, như đảo Mộc) từ cảng sắt lên bãi đấu boss dưới núi thép có tháp "
        f"chuông, 10 bãi tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và "
        f"chấm ải lên đường. Khói, hơi nước, tia lửa, lấp lánh, sóng là phần động game thêm sau, GPT không vẽ.",
        "",
        "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. "
        "Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude \"duyệt đoạn <k> đảo Kim\"; Claude soi, lưu "
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
    vi = {1: "cảng sắt nhỏ cạnh đầu đường: cần cẩu sắt tán đinh có móc lớn, thùng kim loại xếp chồng, vài thùng phuy, mỏ neo sắt "
             "trên sỏi xám",
          2: "cầu tấm sắt tán đinh qua sông, rộng bằng đường, mỗi đầu cầu một bánh răng đồng lớn dựng đứng cạnh đường; mặt cầu trống",
          3: "rừng cây thân xám bạc, tán tròn lá dài cong hình lưỡi liềm (lá, không phải vũ khí) xanh thép và xanh nhạt, xen đá xám",
          4: "tháp canh khung thép tán đinh cao, chòi canh nhỏ trên đỉnh, chóp nhọn như mũi thương, vài thùng sắt dưới chân",
          5: "nhà chuông mở mái đá sẫm trên bốn cột gỗ to, nền đá vuông, chuông đồng lớn treo bên trong",
          6: "hồ nước làm nguội tròn; sau hồ trên mỏm đá là xưởng đúc chuông: lò đá thấp có ống khói ngắn, nồi sắt đầy đồng nóng "
             "chảy (mảng cam vàng phẳng, không quầng sáng), hai chuông đồng trên giá gỗ; lạch nước chảy ra mép",
          7: "cửa mỏ khung gỗ dày trong đồi đá xám, đường ray ngắn chạy ra có xe goòng đầy quặng bạc",
          8: "cổng thành đá xám nhỏ có hai tháp thấp, cửa sắt đóng; trước cổng ba thanh kiếm khổng lồ cắm mũi xuống đất, chuôi đỏ, "
             "xanh, vàng",
          9: "tổ tròn lớn đan bằng thanh thép uốn trên mỏm đá, mảnh pha lê xanh nhạt dài cắm quanh vành như lông vũ; tổ trống",
          10: "núi thép xám đỉnh tuyết trắng ngay sau bãi đấu boss, trên đỉnh là tháp chuông đá và thép tán đinh mái đồng cong, chuông "
              "đồng khổng lồ ở tầng trên mở; hai tượng đá đôi cánh xếp nhỏ ở chân núi hai bên sau bãi; đỉnh tháp chạm dải biển trên"}
    heads = z.HEADS + [71]
    for num in range(1, 11):
        rng = f"{heads[num - 1]}–{heads[num] - 1}" if heads[num] - 1 > heads[num - 1] else f"{heads[num - 1]}"
        lines.append(f"| {num} | {SPOTS[num][0]} ({rng}) | {vi[num]} |")
    lines += [
        "",
        "## Soi trước khi nhắn Claude",
        "",
        "- Đảo kim loại xám xanh (không phải đảo rừng xanh lá như ảnh mẫu đảo Mộc), nét và cách dựng giống ảnh mẫu.",
        "- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường, mặt cầu và các bãi tròn **trống**.",
        "- Địa danh đúng số, đứng sát đường, không đè lên đường.",
        "- Sông, hồ, lạch là nước xám xanh có bờ đá, không bọt, không thác; đồng nóng chảy trong nồi là mảng cam vàng phẳng.",
        "- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).",
        f"- Lượt 1, 2: dải {OV} px trên cùng chỉ có đường, đất, bụi, đá.",
        "- Không chữ, không số, không sinh vật, người máy, người; không viền đảo ở hai bên; không khói, hơi nước, tia lửa, lấp lánh "
        "(game thêm).",
        "",
        "## Sửa nhanh (gõ vào chat)",
        "",
        "| Lỗi | Gõ |",
        "|---|---|",
        "| Ra màu xanh lá, cây rừng như đảo Mộc | `Same layout, but this is the cool blue-grey Metal island: blue-grey hatched ground, "
        "grey rocks and peaks, iron and bronze props, silver-grey trees with steel-blue crowns; no green grass, no green forest trees.` |",
        "| Kim loại bóng loáng, kiểu 3D | `Too shiny and too realistic. Redraw the metal as flat colour-pencil hatching with wobbly ink "
        "outlines, no chrome reflections, no gradients. Keep the same layout.` |",
        "| Có khói, hơi nước, tia lửa, quầng sáng | `Same image, but remove all smoke, steam, sparks, flames, sparkles and glows. The "
        "molten bronze stays a flat orange and yellow surface.` |",
        "| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road, the bridge deck and the round clearings completely empty: "
        "remove everything standing on them.` |",
        "| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round "
        "clearings.` |",
        "| Có số, chữ | `Same image without any numbers, letters or text.` |",
        "| Có người, người máy, sinh vật | `Same image without any people, robots or creatures.` |",
        "| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |",
        f"| Dải đáy không nối với đoạn trước | `Redraw it so the bottom {OV} px show exactly the same scene as the painted bottom strip of "
        "the sketch: same road position and width, same trees and rocks.` |",
        "| Chân núi hay tháp chuông đè lên bãi đấu | `Same image, but the mountain and the bell tower stay behind the arena: the round "
        "arena is completely empty.` |",
        "| Quá vụn | `Too detailed. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every "
        "rock, tree and prop a chunky doodle with a clear silhouette. Keep the same layout.` |",
        "",
    ]
    return "\n".join(lines)


# ---------- toạ độ dự kiến ----------

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
        "note": "Bố cục dự kiến của bản đồ dài đảo Kim (build_zone70_kim.py); x, y từ 0 tới 1 theo bản đồ ghép, y từ trên. Có ảnh "
                "thật thì dò lại đường.",
        "map": [W, H], "segments": NSEG, "overlap": OV, "displayWidth": 1.27, "roadWidth": round(z.ROAD_W / W, 4),
        "pipGap": round(z.GAP, 1),
        "path": [[round(x / W, 4), round(y / H, 4)] for x, y in path],
        "stages": stages,
    }
    (GUIDES / "zone70_kim.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- sửa chỗ nối của đoạn GPT trả về (như build_zone70_hoa.va_noi) ----------
# Đảo Hỏa đoạn 2 (2026-11-05): GPT giữ nguyên dải dán nhưng chỗ phần nó vẽ gặp dải dán có một dải khoảng 25 hàng phủ vạch sáng dọc
# mờ, hai mép đường có mẩu mực thừa và lệch 12–21 px. Cách dùng: trừ mẫu vạch theo cột, nắn mép đường.

FIX_TOP, FIX_CORE, FIX_ROAD = 36, 18, 28  # số hàng sửa vạch phía trên mép dải dán, số hàng lõi để đo mẫu vạch, số hàng nắn mép đường


def va_noi(a, k, road):
    """sửa chỗ nối của đoạn k (1, 2 = đoạn giữa, trên; a: mảng float H x W x 3 của ảnh GPT, sửa tại chỗ)"""
    from scipy.ndimage import median_filter
    seam = SH - OV  # từ hàng này xuống là dải dán từ đoạn dưới
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


# ---------- ghép 3 đoạn đã duyệt ----------

FEATHER = 24  # nửa bề cao vùng trộn quanh đường cắt giữa dải chồng


def ghep():
    """ghép doan_1..3 đã duyệt thành bản đồ W x H (zones/kim70/zone_kim70.png), như build_zone70_hoa.ghep"""
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
    out = WORK / "zone_kim70.png"
    Image.fromarray(img.clip(0, 255).astype("uint8")).save(out)
    (WORK / "ghep.json").write_text(json.dumps({"tops": tops}, ensure_ascii=False), encoding="utf-8")
    print(f"Đã ghi {out} ({W} x {H}); đỉnh các đoạn {tops}")


# ---------- dò đường thật trên bản đồ ghép ----------
# Như đảo Hỏa: tâm đường theo hàng (bắt lại sau cầu), 10 bãi ải là chỗ bề rộng mặt cát đo vuông góc vượt ngưỡng. Sông và lạch dò theo
# màu nước trên ảnh (GPT vẽ sông lệch bố cục khoảng 50 px ở mép phải). Địa danh, chỗ phần động đo tay trên bản đồ ghép (px bản đồ,
# 2026-11-05).

SPOTS_REAL = {1: ((760, 4000), 150), 3: ((150, 3450), 130), 4: ((795, 3240), 150), 5: ((300, 3090), 130), 6: ((765, 2585), 170),
              7: ((300, 2217), 150), 8: ((712, 1820), 170), 9: ((683, 922), 150), 10: ((510, 210), 190)}
BRIDGE_REAL = (555, 3735)
# phần động (IslandAnim, khoá zone_kim): (kiểu, x, y, cỡ px bản đồ). Bánh răng, chuông đã vẽ trên ảnh nên không dùng gear, bell
ANIM = [
    ("smoke", 790, 2395, 60),  # ống khói lò đúc chuông
    ("sparkle", 510, 140, 34),  # chuông tháp Thiên Chung
    ("sparkle", 300, 3115, 28),  # chuông Gác Chuông Đồng
    ("sparkle", 648, 2560, 24), ("sparkle", 905, 2560, 24),  # hai chuông của xưởng đúc
    ("sparkle", 428, 2282, 28),  # xe goòng quặng bạc
    ("sparkle", 630, 1885, 24), ("sparkle", 795, 1880, 24),  # chuôi kiếm Thành Ba Kiếm
    ("sparkle", 592, 855, 28), ("sparkle", 795, 870, 28),  # pha lê ở tổ
    ("ripple", 720, 2690, 70),  # hồ nước làm nguội
    ("wave", 230, H - 30, 90), ("wave", 790, H - 40, 90), ("wave", 300, 24, 80), ("wave", 800, 30, 80),
]
RIVER_BOX = (0, 3560, W, 3900)  # dải có sông chạy ngang (px bản đồ: x0, y0, x1, y1)
CREEK_BOX = (880, 2600, W, 2780)  # lạch từ hồ xưởng đúc ra mép phải


def water_mask(a):
    """mặt nước xanh lam (đậm hơn nền đảo xám xanh)"""
    from scipy import ndimage as ndi
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (b > 185) & (r < 150) & (b - r > 70) & (g < 210)
    return ndi.binary_closing(ndi.binary_opening(m, iterations=1), iterations=6)


def trace_across(m, box, step=12):
    """đường giữa dòng nước chạy ngang: mỗi cột lấy tâm đoạn liền gần tâm cột trước, trái sang phải"""
    x0, y0, x1, y1 = box
    pts, last = [], None
    for x in range(x0, min(x1, m.shape[1]), step):
        ys = np.nonzero(m[y0:y1, x])[0]
        if len(ys) == 0:
            continue
        runs = [r for r in np.split(ys, np.nonzero(np.diff(ys) > 3)[0] + 1) if len(r) >= 8]
        if not runs:
            continue
        cand = [(y0 + r.mean(), len(r)) for r in runs]
        cy = (max(cand, key=lambda c: c[1]) if last is None else min(cand, key=lambda c: abs(c[0] - last)))[0]
        if last is not None and abs(cy - last) > 40:
            continue
        pts.append((float(x), float(cy)))
        last = cy
    return pts


def that():
    """dò đường, 10 bãi ải, sông và lạch trên zones/kim70/zone_kim70.png; ghi zones/kim70/that.json và ảnh soi soi_that.png"""
    from PIL import ImageFilter
    img = np.array(Image.open(WORK / "zone_kim70.png").convert("RGB")).astype(int)
    sand = z.sand_mask(img)
    sand = np.asarray(Image.fromarray((sand * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3))
                      .filter(ImageFilter.MinFilter(3))) > 0
    with contextlib.redirect_stdout(io.StringIO()):
        road0, stops0, pts0, _, water0 = layout()
    y0 = 3950  # giữa bãi ải 1 và cầu
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
    wm = water_mask(img)
    streams = []
    for name, box, plan in (("sông", RIVER_BOX, water0["streams"][0]), ("lạch", CREEK_BOX, water0["streams"][-1])):
        st = trace_across(wm, box)
        if len(st) < 5:
            z.warn(f"không dò được {name} trên ảnh; lấy đường dự kiến")
            st = plan
        else:
            print(f"  {name}: {len(st)} điểm, x {st[0][0]:.0f}..{st[-1][0]:.0f}, y {min(p[1] for p in st):.0f}..{max(p[1] for p in st):.0f}")
        streams.append(st)
    data = {
        "path": [[round(x, 1), round(y, 1)] for x, y in path],
        "stops": [round(d[k], 1) for k in stops], "length": round(L, 1),
        "stages": [[round(path[k][0], 1), round(path[k][1], 1)] for k in stops],
        "streams": [[[round(x, 1), round(y, 1)] for x, y in s] for s in streams],
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
    out[BRIDGE] = {"bridge": BRIDGE_REAL}
    return out


def anim_spec(water):
    """phần động trên ảnh (IslandAnim, khoá zone_kim): khói, lấp lánh, gợn, sóng (ANIM), gợn chạy dọc sông và lạch. Toạ độ chia W, H;
    cỡ chia W"""
    rivers = [("stream", [(min(max(x, 2), W - 2), y) for x, y in st[::3]], z.STREAM_W) for st in water["streams"]]
    return {
        "items": [{"k": k, "x": round(x / W, 4), "y": round(y / H, 4), "s": round(sz / W, 4)} for k, x, y, sz in ANIM],
        "rivers": [{"k": k, "w": round(rw / W, 4), "pts": [[round(x / W, 4), round(y / H, 4)] for x, y in pts]} for k, pts, rw in rivers],
    }


def xuat(art_out=None, zones_json=None):
    """đưa bản đồ đã ghép vào game theo đường dò được (that.json): Assets/03 Art/Islands/zone_kim.png (biển hai mép trong suốt; thay
    bản đồ 8 ải cũ), khoá zone_kim trong island_anim.json, đảo kim trong zones.json (nodes = 10 bãi ải dò được, path = tâm đường thật
    tới giữa bãi đấu boss, stops, plates). Đọc lại hai file JSON ngay lúc ghi, chỉ thay phần của đảo Kim. Sau đó chạy menu Unity
    PokiClash/Nhập dữ liệu. art_out, zones_json: ghi chỗ khác để thử."""
    art_out = Path(art_out or z.ART_OUT)
    zones_json = Path(zones_json or z.ZONES_JSON)
    th = json.loads((WORK / "that.json").read_text(encoding="utf-8"))
    a = np.array(Image.open(WORK / "zone_kim70.png").convert("RGB"))
    alpha = z.sea_alpha(a)
    rgba = np.dstack([a, (alpha * 255).round().astype("uint8")])
    art_out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(art_out / "zone_kim.png", optimize=True)
    print(f"Đã ghi {art_out / 'zone_kim.png'} ({W} x {H}); biển trong suốt {(alpha < 0.5).mean() * 100:.1f}% ảnh")

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
    anim["zone_kim"] = anim_spec(water)
    nl = "\r\n" if b"\r\n" in anim_path.read_bytes() else "\n"
    anim_path.write_text(json.dumps(anim, ensure_ascii=False, indent=1), encoding="utf-8", newline=nl)
    print(f"Đã ghi khoá zone_kim trong {anim_path}: {len(anim['zone_kim']['items'])} món, {len(anim['zone_kim']['rivers'])} dòng")

    src_json = zones_json if zones_json.exists() else z.ZONES_JSON
    zl = "\r\n" if b"\r\n" in src_json.read_bytes() else "\n"  # giữ kiểu xuống dòng của file
    data = json.loads(src_json.read_text(encoding="utf-8"))
    zd = next(x for x in data["zones"] if x["id"] == "kim")
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
    print(f"Đã ghi đảo kim trong {zones_json}: 10 ải tướng, đường {len(path)} điểm, bảng tên {plates}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar="K [ANH]",
                    help="lưu đoạn K (1..3) GPT trả về (mặc định ảnh mới nhất tai_ve/doan_K*.png) rồi dựng lại gói")
    ap.add_argument("--ghep", action="store_true", help="ghép 3 đoạn đã duyệt thành zones/kim70/zone_kim70.png")
    ap.add_argument("--that", action="store_true", help="dò đường, bãi ải, sông thật trên bản đồ đã ghép (that.json)")
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
    guide.save(GUIDES / "L_zone70_kim.png")
    save_json(road, stops, pts, spots)
    build_pack(spots, water, guide)
    print(f"Đã ghi {GUIDES / 'L_zone70_kim.png'}, {GUIDES / 'zone70_kim.json'}, gói {PACK}")
    if warnings:
        print(f"{len(warnings)} cảnh báo, xem trên")


if __name__ == "__main__":
    main()
