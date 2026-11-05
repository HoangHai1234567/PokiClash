# Bản đồ dài đảo Mộc 70 ải: dựng ảnh bố cục và gói gửi GPT, như build_zone70.py (đảo Thủy). Dùng lại phần chung của script đó
# (đường chữ S, cỡ bản đồ 1024 x 4288 ghép 3 đoạn, chỗ địa danh, nắn chỗ nối, biển trong suốt, bảng tên); không sửa build_zone70.py.
# Khác đảo Thủy:
# - đường lượn sang trái trước (soi gương đảo Thủy), cùng độ cao 10 ải tướng;
# - suối chạy ngang và cầu gỗ quấn dây leo ngay trước ải 15 (chặng 4, Rừng Dây Leo); hồ lá sen có lạch ra mép (chặng 6, Thung
#   Lũng Lá); cây thần ngàn năm đứng sau bãi đấu boss, tán lá phủ tới dải biển trên;
# - ảnh mẫu nét là đoạn 1 bản đồ dài đảo Thủy đã duyệt (cùng game, nét và cách dựng đã chốt), màu và đồ vật lấy bản đồ Mộc 8 ải cũ.
# Ghi: ArtGen/guides/L_zone70_moc.png (bố cục cả bản đồ), ArtGen/guides/zone70_moc.json (đường, ải tướng, địa danh; toạ độ 0..1 của
# bản đồ ghép, y từ trên; build_moc.py của BattleBG đọc để cắt địa danh làm ảnh mẫu nền trận), gói ArtGen/Islands/gui_gpt/zone_moc_70/
# (luot_k.txt, bo_cuc_k.png, HUONG_DAN.md).
# Chạy: py -3 -I ArtGen/Islands/build_zone70_moc.py
# Duyệt đoạn k GPT đã lưu: --duyet k [ảnh] (mặc định ảnh mới nhất zones/moc70/tai_ve/doan_k*.png): lưu zones/moc70/doan_k.png rồi
# dựng lại gói (có đoạn k thì có file prompt lượt k+1, bố cục đoạn k+1 dán dải đỉnh của đoạn k).
# Đủ 3 đoạn: --ghep (zones/moc70/zone_moc70.png), --xuat (Assets/03 Art/Islands/zone_moc.png, khoá zone_moc trong island_anim.json,
# đảo moc trong zones.json), rồi menu Unity PokiClash/Nhập dữ liệu.
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

import build_zone70 as z  # noqa: E402  (phần chung; đặt lại FIRST trước khi dựng đường)

z.FIRST = -1  # chặng đầu lượn sang trái

W, SH, H, OV, NSEG = z.W, z.SH, z.H, z.OV, z.NSEG
GUIDES = z.GUIDES
PACK = HERE / "gui_gpt" / "zone_moc_70"
WORK = HERE / "zones" / "moc70"  # tai_ve/: ảnh GPT trả về; doan_k.png: đoạn đã duyệt
STYLE = HERE / "zones" / "thuy70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Thủy đã duyệt
OLD = HERE / "zones" / "zone_moc.png"  # bản đồ Mộc 8 ải đang dùng
ART_OUT = z.ART_OUT
ZONES_JSON = z.ZONES_JSON

BRIDGE, POND, BOSS = 4, 6, 10

# địa danh từng chặng: tên chặng (IslandGen.Moc), kiểu chỗ (land xám, water xanh, bridge cầu qua suối, boss cây thần sau bãi đấu),
# bán kính, câu cho GPT
SPOTS = {
    1: ("Bờ Rêu", "land", 100, "big round mossy boulders and an old moss-covered wooden rowboat on the shore beside the start of the "
                               "road"),
    2: ("Đồng Hoa Sáng", "land", 100, "a meadow of giant bell-shaped flowers on tall stems, petals in soft pale yellow, pink and sky "
                                      "blue, with big round leaves"),
    3: ("Đồi Nấm", "land", 105, "a small grassy hill crowded with giant mushrooms (red and orange caps with cream spots); the two "
                                "biggest are cottages with round wooden doors and little round windows"),
    4: ("Rừng Dây Leo", "bridge", 0, "the road crosses the stream on a wide wooden bridge wrapped in thick green vines with leafy "
                                     "rails, exactly as wide as the road; the bridge is part of the road and stays empty; tall trees "
                                     "with long hanging vines stand on both banks"),
    5: ("Hang Nanh Gió", "land", 105, "the dark mouth of a cave in a grey rocky mound, its upper and lower edges lined with huge "
                                      "pointed rock fangs like an open mouth; a few wind-bent trees beside it"),
    6: ("Thung Lũng Lá", "water", 105, "a round pond in a leafy hollow, covered with giant round lily pads and a few pink water "
                                       "lilies, under trees with huge broad leaves; a small creek leaves it and runs off the {edge} "
                                       "edge"),
    7: ("Vách Vuốt Rồng", "land", 110, "a tall grey-green rock cliff slashed by three huge diagonal claw marks, with two curved rock "
                                       "spires like giant claws beside it"),
    8: ("Rừng Trúc Ngọc", "land", 110, "a dense grove of tall jade-green bamboo around a small stone shrine with a curved green-tiled "
                                       "roof and two stone lanterns"),
    9: ("Hang Pha Lê Lục", "land", 110, "a cave mouth in a mossy rock hill, bristling with big emerald-green crystals"),
    10: ("Cây Thần Ngàn Năm", "boss", 118, "the boss lair: the road ends in the big round empty arena; right behind it stands a giant "
                                           "ancient tree with a wide gnarled trunk and a small shrine in a hollow of the trunk; its "
                                           "thick roots curl around the back of the arena but never onto it, and its huge round crown "
                                           "of leaves spreads behind it up to the sea at the top edge"),
}

TREE = (96, 150, 84)
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

    # 4: suối chạy ngang từ mép phải sang mép trái, qua đường ở cầu ngay trước bãi ải 15
    sx = stops[BRIDGE - 1] - 120
    X = road.at(sx)
    stream = z.wavy((W + 40, X[1] + 70), X, 22, 13)[:-1] + z.wavy(X, (-40, X[1] - 50), 22, 14)
    z.check_water("suối cầu dây leo", stream, z.STREAM_W / 2, road, (sx - 200, sx + 200))
    water["streams"].append(stream)
    n = road.normal(sx)
    spots[BRIDGE] = {"bridge": X, "dir": (n[0], n[1])}

    # cây thần (10) ngay sau bãi đấu boss; các địa danh khác chọn chỗ cùng lúc, né suối và cây thần
    r10 = SPOTS[BOSS][2]
    boss = (pts[9][0], pts[9][1] - (clears[9][1] + r10 - 40))
    if boss[1] - r10 < z.TOP_SEA_Y + 10:
        z.warn("cây thần chạm biển trên")
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
    # 6: lạch nước từ hồ lá sen ra mép cùng phía
    if POND in spots:
        c, side = spots[POND]["c"], spots[POND]["side"]
        edge_x = W + 60 if side > 0 else -60
        creek = z.wavy(c, (edge_x, c[1] - 40), 18, 16)
        z.check_water("lạch hồ lá sen", creek, z.STREAM_W / 2, road)
        for num, sp in spots.items():
            if num != POND and "c" in sp and min(math.dist(p, sp["c"]) for p in creek) < sp["r"] + z.STREAM_W / 2:
                z.warn(f"lạch hồ lá sen chạm địa danh {num}")
        water["streams"].append(creek)
        spots[POND]["edge"] = "right" if side > 0 else "left"
    for num, sp in sorted(spots.items()):
        if "c" in sp:
            c = sp["c"]
            print(f"  địa danh {num:2d} {SPOTS[num][0]}: ({c[0]:.0f}, {c[1]:.0f}) đoạn {seg_of(c[1]) + 1}, "
                  f"{'phải' if sp['side'] > 0 else 'trái'} đường")
    b = spots[BRIDGE]["bridge"]
    print(f"  cầu dây leo (4): ({b[0]:.0f}, {b[1]:.0f}) đoạn {seg_of(b[1]) + 1}")
    return road, stops, pts, spots, water


def draw_guide(road, pts, spots, water):
    im = Image.new("RGB", (W, H), z.GROUND)
    d = ImageDraw.Draw(im, "RGBA")
    z.hatch(d, (0, 0, W, H), z.GROUND, 71, 9000)
    beach = z.shore(z.BEACH_Y, 14, 70, 0.6)
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
    sea = z.shore(z.SEA_Y, 10, 55, 1.4)
    d.polygon(sea + [(W, H), (0, H)], fill=z.WATER)
    d.line(sea, fill=z.INK, width=4)
    top = z.shore(z.TOP_SEA_Y, 12, 60, 2.5)
    d.polygon([(0, 0), (W, 0)] + top[::-1], fill=z.WATER)
    d.line(top, fill=z.INK, width=4)
    b = spots[BRIDGE]
    (bx, by), (nx, ny) = b["bridge"], b["dir"]
    tx, ty = -ny, nx
    hw, hl = z.ROAD_W / 2 + 18, 38
    poly = [(bx + nx * hw + tx * hl, by + ny * hw + ty * hl), (bx - nx * hw + tx * hl, by - ny * hw + ty * hl),
            (bx - nx * hw - tx * hl, by - ny * hw - ty * hl), (bx + nx * hw - tx * hl, by + ny * hw - ty * hl)]
    d.polygon(poly, fill=z.BRIDGE, outline=z.INK, width=5)
    z.label(d, (bx, by), str(BRIDGE), 52)
    for num, sp in spots.items():
        if "c" not in sp:
            continue
        c, r = sp["c"], sp["r"]
        if sp["kind"] == "land":
            d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=z.SPOT)
            z.dashed_circle(d, c, r, z.INK)
        elif sp["kind"] == "boss":
            z.disc(d, c, r, TREE)
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


def water_lines(k, spots, water):
    lines = []
    if k == 0:
        lines.append("the sea along the bottom edge behind a shore of pale sand, round pebbles and moss (the journey starts at the "
                     "water's edge);")
    if seg_of(spots[BRIDGE]["bridge"][1]) == k:
        a, b = stream_dir(water)
        lines.append(f"a stream that crosses the whole image from the {a} edge to the {b} edge and passes under the road at the "
                     f"bridge of spot {BRIDGE};")
    if POND in spots and seg_of(spots[POND]["c"][1]) == k:
        lines.append(f"spot {POND} is a round pond with giant lily pads; its small creek runs off the {spots[POND]['edge']} edge;")
    if k == NSEG - 1:
        lines.append("a strip of sea along the top edge beyond the northern tip of the island, behind the crown of the great tree.")
    return lines


GROUND_TEXT = (
    "GROUND: no island outline on the sides: the land runs off the left and right edges. The ground is lush green coloured-pencil "
    "hatching like the old Wood island map, mixed with clover patches, tiny flowers and soft grass tufts. On both sides of the road, "
    "low raised terraces with short earthy cliff faces (top in the ground colour, side in brown-green hatching) give the map depth. "
    "Clusters of round broad-leaf trees, a few tall pines, big ferns, small mushrooms and mossy grey rocks frame the road edges "
    "closely. Small props along the road edges: tree stumps, fallen mossy logs, short wooden fences, a wooden signpost without "
    "writing, little lanterns on posts, flower bushes. Dense, but every tree, rock and prop is a chunky doodle with a clear "
    "silhouette; no tiny noisy details, no 3D, no realistic rendering.")

CODES = ("The sketch is only a colour-coded plan: light green = ground, pale sand with an ink edge = road, blue = water, grey spot with "
         "a number = a landmark on land, blue spot with a number = a landmark in water, dark green spot with a number = the great "
         "tree, brown bar across the road = a bridge. Do not copy its flat colours, its numbers or its dashed outlines.")

RULES = ("Keep the road and the landmarks between x = 130 and x = 894 (narrow phones cut the outer strips); the outer strips have only "
         "ground, trees and rocks.\n"
         "Moving things are added later as animated sprites, so do NOT draw: falling leaves in the air, fireflies, sparkles, glows, "
         "wind lines, foam splashes, breaking wave crests.\n"
         "No text, no letters, no numbers, no signs with writing, no creatures, no people.")


def sketch_path(k):
    return PACK / f"bo_cuc_{k + 1}.png"


def prompt_path(k):
    return PACK / f"luot_{k + 1}.txt"


def save_path(k):
    return WORK / "tai_ve" / f"doan_{k + 1}.png"


OLD_EN = ("the old small map of this same Wood island: copy its colours and the look of its objects (bright green hatched ground, "
          "round broad-leaf trees, mossy grey rocks, red spotted mushrooms, flowers, the vine arch, the cave with stone fangs, the "
          "great tree with its little shrine, the blue river); ignore its layout, its thin path, its island outline, its empty "
          "background and its cream circles")
OLD_VI = ("bản đồ đảo Mộc 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xanh lá gạch chì, đường mòn mảnh có 8 vòng tròn "
          "kem, sông xanh, nấm đỏ chấm trắng, vòm dây leo, hang đá có nanh, cụm hoa, cây thần có miếu nhỏ, cây tròn, đá xám; lấy màu "
          "và dáng đồ vật")


def refs(k, spots):
    """ảnh mẫu GPT mở của lượt k: [(vai, đường dẫn, câu cho GPT, mô tả cho người dùng)]"""
    sk = ("sketch", sketch_path(k), "the layout sketch of the image you draw now: follow it exactly" +
          (f"; its bottom {OV} px strip is not a sketch but the top {OV} px of image 1, already painted" if k else ""),
          f"bố cục đoạn {k + 1} (1024 × 1536, nền xanh lá nhạt)" + (f"; dải {OV} px ở đáy là dải đỉnh của đoạn {k}" if k else "") +
          "; " + seg_desc(k, spots))
    old = ("old", OLD, OLD_EN, OLD_VI)
    if k == 0:
        return [("style", STYLE, "part 1 of the long map of ANOTHER island of this same game, already approved: copy its RENDERING "
                                 "and how the map is built (the wide pale-sand road with round clearings, raised terraces with short "
                                 "cliff faces, chunky trees, rocks and props framing the road, line weight, hatching); ignore its "
                                 "turquoise colours, its seaside objects and its layout",
                 "đoạn 1 bản đồ dài đảo Thủy đã duyệt (1024 × 1536, nền đặc): đường cát rộng lượn có bãi tròn, bậc đất có vách ngắn, "
                 "cọ, đá, đồ vật chen sát đường, đất ngọc lam; lấy nét và cách dựng, không lấy màu, đồ vật biển, bố cục"),
                old, sk]
    return [("prev", WORK / f"doan_{k}.png", f"part {k} of this map, already drawn and approved: copy its style, colours, line "
                                             f"weight and objects exactly, so all parts look like one picture",
             f"đoạn {k} bản đồ đảo Mộc đã duyệt (1024 × 1536)"),
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
        text += ("WHAT THIS IS: part 1 of 3 (the bottom part) of one long vertical map of the Wood island, a forest island, for a "
                 "vertical mobile game. The player scrolls up the map from the mossy shore at the bottom to the boss at the great "
                 "tree at the top. The three parts are drawn one after another and stacked. Part 2 repeats the top "
                 f"{OV} px of this image as its bottom strip, so keep the top {OV} px of this image plain: road, ground, a few bushes "
                 "and rocks, no landmark, no water.\n\n"
                 f"Draw a vertical 1024 x 1536 image in the rendering and map construction of image {idx['style']} with the colours "
                 f"and objects of image {idx['old']}: a green forest island, not a turquoise beach island. Outlines and hatching as "
                 f"bold as in image {idx['style']}.\n\n")
    else:
        part = "the middle part" if k == 1 else "the top part"
        text += (f"WHAT THIS IS: part {k + 1} of 3 ({part}) of one long vertical map of the Wood island, a forest island, for a "
                 f"vertical mobile game. The player scrolls up the map from the mossy shore at the bottom to the boss at the great "
                 f"tree at the top; your image goes right above image {idx['prev']}.\n\n"
                 f"Draw a vertical 1024 x 1536 image in exactly the style of image {idx['prev']}. Image {idx['old']} only shows how "
                 f"this island's objects look (the cave with stone fangs, the great tree); copy the drawing of image {idx['prev']}, "
                 f"not image {idx['old']}'s.\n\n"
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
        text += ("WATER: deeper blue than the ground, with a wobbly ink bank, a thin rim of pale sand or moss and white ripple "
                 "scribbles:\n" + "\n".join("- " + s for s in wl) + "\n")
        if k == 1 and not any("stream" in s for s in wl):
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
        parts.append("đáy là bờ cát sỏi rêu và biển, đường bắt đầu từ mép nước")
    for num in seg_spots(k, spots):
        sp = spots[num]
        if num == BRIDGE:
            parts.append(f"suối xanh chạy ngang hết bề ngang, thanh nâu số {BRIDGE} ngang đường là cầu dây leo")
        elif sp["kind"] == "land":
            parts.append(f"chấm xám số {num} là chỗ {SPOTS[num][0]}")
        elif sp["kind"] == "boss":
            parts.append(f"đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm xanh sẫm số {num} sau bãi là gốc cây thần")
        else:
            parts.append(f"chấm xanh số {num} là hồ lá sen {SPOTS[num][0]}, lạch nước chảy ra mép "
                         f"{'phải' if sp.get('edge') == 'right' else 'trái'}")
    if k == NSEG - 1:
        parts.append("dải biển dọc mép trên")
    return "; ".join(parts)


def guide_md(spots, water):
    p = lambda *a: str(Path(*a))  # noqa: E731
    lines = [
        "# Gói gửi GPT: bản đồ dài đảo Mộc 70 ải (`zone_moc_70`)",
        "",
        f"Sinh bằng `{p(HERE, 'build_zone70_moc.py')}`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Mộc mới cho 70 ải, cùng "
        f"khuôn bản đồ dài đảo Thủy: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ {W} × {H}. "
        f"Đường cát rộng lượn chữ S (lượn trái trước, ngược đảo Thủy) từ bờ rêu lên bãi đấu boss dưới cây thần, 10 bãi tròn cho 10 ải "
        f"tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường.",
        "",
        "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. "
        "Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude \"duyệt đoạn <k> đảo Mộc\"; Claude soi, lưu "
        "bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét. Gói nền trận đảo Mộc "
        "(`ArtGen\\BattleBG\\gui_gpt\\moc`) làm song song được, ở một chat khác.",
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
    vi = {1: "đá tròn phủ rêu, thuyền gỗ cũ phủ rêu trên bờ cạnh đầu đường",
          2: "đồng hoa chuông khổng lồ thân cao, cánh vàng nhạt, hồng, xanh trời",
          3: "đồi cỏ nhỏ mọc đầy nấm khổng lồ mũ đỏ, cam chấm kem; hai cây to là nhà có cửa gỗ tròn",
          4: "cầu gỗ quấn dây leo qua suối, rộng bằng đường; cây cao rủ dây leo hai bờ",
          5: "miệng hang tối trong gò đá xám, mép trên dưới có nanh đá nhọn như miệng mở; vài cây gió uốn",
          6: "hồ tròn đầy lá sen khổng lồ, vài bông súng hồng, cây lá to; lạch nước chảy ra mép",
          7: "vách đá xám xanh có ba vết vuốt chéo khổng lồ, hai mỏm đá cong như vuốt",
          8: "rừng trúc xanh ngọc quanh miếu đá nhỏ mái ngói xanh cong, hai đèn đá",
          9: "miệng hang trong đồi đá rêu, pha lê lục bảo to tua tủa",
          10: "cây thần cổ thụ sau bãi đấu boss, thân to sần có miếu nhỏ trong hốc, rễ ôm sau bãi, tán tròn phủ tới biển trên"}
    heads = z.HEADS + [71]
    for num in range(1, 11):
        rng = f"{heads[num - 1]}–{heads[num] - 1}" if heads[num] - 1 > heads[num - 1] else f"{heads[num - 1]}"
        lines.append(f"| {num} | {SPOTS[num][0]} ({rng}) | {vi[num]} |")
    lines += [
        "",
        "## Soi trước khi nhắn Claude",
        "",
        "- Đảo rừng xanh lá (không phải đảo biển ngọc lam như ảnh mẫu đảo Thủy), nét và cách dựng giống ảnh mẫu.",
        "- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường và các bãi tròn **trống**.",
        "- Địa danh đúng số, đứng sát đường, không đè lên đường.",
        "- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).",
        f"- Lượt 1, 2: dải {OV} px trên cùng chỉ có đường, đất, bụi, đá.",
        "- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không lá bay, đom đóm, lấp lánh, vệt gió (game thêm).",
        "",
        "## Sửa nhanh (gõ vào chat)",
        "",
        "| Lỗi | Gõ |",
        "|---|---|",
        "| Ra màu ngọc lam, đồ biển như đảo Thủy | `Same layout, but this is the green forest island: lush green hatched ground, broad-leaf "
        "trees, pines, ferns, mushrooms and mossy rocks; no palm trees, no turquoise ground, no seaside props.` |",
        "| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road and the round clearings completely empty: remove everything "
        "standing on them.` |",
        "| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round "
        "clearings.` |",
        "| Có số, chữ | `Same image without any numbers, letters or text.` |",
        "| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |",
        f"| Dải đáy không nối với đoạn trước | `Redraw it so the bottom {OV} px show exactly the same scene as the painted bottom strip of "
        "the sketch: same road position and width, same trees and rocks.` |",
        "| Rễ, tán cây thần đè lên bãi đấu | `Same image, but the great tree's roots and crown stay behind the arena: the round arena is "
        "completely empty.` |",
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
        "note": "Bố cục dự kiến của bản đồ dài đảo Mộc (build_zone70_moc.py); x, y từ 0 tới 1 theo bản đồ ghép, y từ trên. Có ảnh "
                "thật thì dò lại đường.",
        "map": [W, H], "segments": NSEG, "overlap": OV, "displayWidth": 1.27, "roadWidth": round(z.ROAD_W / W, 4),
        "pipGap": round(z.GAP, 1),
        "path": [[round(x / W, 4), round(y / H, 4)] for x, y in path],
        "stages": stages,
    }
    (GUIDES / "zone70_moc.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- ghép 3 đoạn đã duyệt ----------

FEATHER = 24  # nửa bề cao vùng trộn quanh đường cắt giữa dải chồng


def band_offset(lower, upper, rng=48):
    """GPT không giữ nguyên dải dán mà vẽ lại (đảo Mộc 2026-11-05: đoạn 3 vẽ dải lùi lên 33 px). Dò dời dọc dy để hàng SH-OV+i của
    đoạn trên khớp hàng i+dy của đoạn dưới (dy > 0: đặt đoạn trên thấp xuống dy px); trả (dy, chênh xám TB)"""
    A = np.asarray(Image.fromarray(lower.astype("uint8")).convert("L"), float)[:OV]
    B = np.asarray(Image.fromarray(upper.astype("uint8")).convert("L"), float)[SH - OV:]
    best = None
    for dy in range(-rng, rng + 1):
        a0, b0 = A[max(0, dy):OV + min(0, dy)], B[max(0, -dy):OV + min(0, -dy)]
        e = np.abs(a0 - b0).mean()
        if best is None or e < best[1]:
            best = (dy, e)
    return best


def seg_tops():
    """y trên của từng đoạn trong bản đồ ghép sau khi dời theo band_offset (zones/moc70/ghep.json do --ghep ghi)"""
    p = WORK / "ghep.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))["tops"]
    return [z.seg_top(k) for k in range(NSEG)]


def ghep():
    """ghép doan_1..3 đã duyệt thành bản đồ W x H (zones/moc70/zone_moc70.png). Mỗi chỗ nối: dò dời dọc của đoạn trên cho dải chồng
    khớp (band_offset), cắt ở giữa dải chồng và trộn FEATHER hàng hai bên. Đoạn trên cùng dời xuống thì hàng trống trên đỉnh lấy
    hàng đầu của nó (biển, game làm trong suốt)."""
    segs = [np.array(Image.open(WORK / f"doan_{k + 1}.png").convert("RGB")).astype(float) for k in range(NSEG)]
    tops = [H - SH]
    for k in range(1, NSEG):
        dy, err = band_offset(segs[k - 1], segs[k])
        tops.append(tops[-1] - (SH - OV) + dy)
        print(f"  nối đoạn {k} và {k + 1}: dời đoạn {k + 1} xuống {dy} px (chênh dải chồng {err:.1f})")
    img = np.zeros((H, W, 3))
    filled = np.zeros(H, bool)
    for k in range(NSEG):  # từ dưới lên; dải chồng: dưới đường cắt lấy đoạn dưới, trên lấy đoạn trên, trộn quanh đường cắt
        t = tops[k]
        y0, y1 = max(0, t), t + SH
        part = segs[k][y0 - t:y1 - t]
        if k == 0:
            img[y0:y1] = part
        else:
            lo_top = tops[k - 1]
            cut = (lo_top + y1) // 2  # giữa dải chồng
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
    out = WORK / "zone_moc70.png"
    Image.fromarray(img.clip(0, 255).astype("uint8")).save(out)
    (WORK / "ghep.json").write_text(json.dumps({"tops": tops}, ensure_ascii=False), encoding="utf-8")
    print(f"Đã ghi {out} ({W} x {H}); đỉnh các đoạn {tops}")


# ---------- dò đường thật trên bản đồ ghép ----------
# Đảo Mộc: GPT vẽ đường lệch bố cục (đoạn 2 lệch tới 100 px), nên game không dùng đường dự kiến như đảo Thủy mà dò lại trên ảnh:
# tâm đường theo từng hàng, 10 bãi ải là chỗ đường phình (sâu nhất khi gặm mòn mặt cát), suối và lạch theo mặt nước. Địa danh đo tay
# trên bản đồ ghép (SPOTS_REAL, px bản đồ) cho phần động và bên đặt bảng tên.

SPOTS_REAL = {1: ((285, 4139), 95), 2: ((765, 3862), 100), 3: ((315, 3667), 105), 5: ((300, 3127), 115), 6: ((742, 2583), 95),
              7: ((245, 2141), 120), 8: ((753, 1713), 120), 9: ((680, 913), 115), 10: ((510, 293), 125)}
BRIDGE_REAL = (412, 3344)


def depth_map(mask, steps=60):
    """độ sâu xấp xỉ (px) của từng điểm trong mặt cát: số lần gặm mòn 3 x 3 còn sống, làm trên ảnh thu nửa"""
    from PIL import ImageFilter
    small = Image.fromarray((mask * 255).astype("uint8")).resize((W // 2, H // 2), Image.NEAREST)
    depth = np.zeros((H // 2, W // 2), np.int16)
    cur = small
    for _ in range(steps):
        arr = np.asarray(cur) > 0
        if not arr.any():
            break
        depth += arr
        cur = cur.filter(ImageFilter.MinFilter(3))
    return depth * 2


def runs_of(row):
    xs = np.flatnonzero(row)
    if not len(xs):
        return []
    return [(r[0], r[-1]) for r in np.split(xs, np.flatnonzero(np.diff(xs) > 2) + 1)]


def trace_road(mask, y0, x0):
    """tâm đường theo hàng từ hàng y0 (tâm gần x0) lên tới bãi đấu boss, rồi xuống tới đầu đường ở bờ; khúc mất dấu (cầu) nội suy"""
    def walk(ys, cx):
        out, prev, lost = [], None, 0
        for y in ys:
            rs = [r for r in runs_of(mask[y]) if 30 <= r[1] - r[0] <= 420]
            if prev and not lost:
                rs = [r for r in rs if r[0] - 12 <= prev[1] and r[1] + 12 >= prev[0]]
            elif prev:  # vừa mất dấu (cầu): bắt lại khúc cát rộng như đường, gần tâm cũ
                rs = [r for r in rs if 70 <= r[1] - r[0] and abs((r[0] + r[1]) / 2 - cx) < 80 + lost]
            if rs:
                r = min(rs, key=lambda r: abs((r[0] + r[1]) / 2 - cx))
                prev, cx, lost = r, (r[0] + r[1]) / 2, 0
                out.append((cx, y))
            else:
                lost += 1
                if lost > 220:
                    break
        return out
    up = walk(range(y0, 0, -1), x0)
    down = walk(range(y0 + 1, H), x0)
    pts = sorted(up + down, key=lambda p: -p[1])  # từ dưới lên
    ys = np.array([p[1] for p in pts], float)
    xs = np.array([p[0] for p in pts], float)
    full_y = np.arange(ys.max(), ys.min() - 1, -1)
    full_x = np.interp(full_y, ys[::-1], xs[::-1])
    k = 41  # làm trơn
    pad = np.pad(full_x, k // 2, mode="edge")
    full_x = np.convolve(pad, np.ones(k) / k, mode="valid")
    return [(x, y) for x, y in zip(full_x, full_y)]


def resample(pts, step):
    out, acc = [pts[0]], 0.0
    for a, b in zip(pts, pts[1:]):
        acc += math.dist(a, b)
        if acc >= step:
            out.append(b)
            acc = 0.0
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def trace_water(blue, x_from, x_to, y_guess, step=16):
    """tâm mặt nước theo cột từ x_from tới x_to, bám theo dòng gần y_guess"""
    out, cy = [], y_guess
    for x in range(int(x_from), int(x_to), step if x_to > x_from else -step):
        col = blue[:, min(max(x, 0), W - 1)]
        rs = [r for r in runs_of(col) if 12 <= r[1] - r[0] <= 160 and abs((r[0] + r[1]) / 2 - cy) < 70]
        if rs:
            r = min(rs, key=lambda r: abs((r[0] + r[1]) / 2 - cy))
            cy = (r[0] + r[1]) / 2
            out.append((x, cy))
    return out


def that():
    """dò đường, 10 bãi ải, suối trên zones/moc70/zone_moc70.png; ghi zones/moc70/that.json và ảnh soi soi_that.png"""
    img = np.array(Image.open(WORK / "zone_moc70.png").convert("RGB")).astype(int)
    from PIL import ImageFilter
    sand = z.sand_mask(img)
    sand = np.asarray(Image.fromarray((sand * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3))
                      .filter(ImageFilter.MinFilter(3))) > 0
    with contextlib.redirect_stdout(io.StringIO()):
        road0, stops0, pts0, _, water0 = layout()
    y0 = 3950
    line = trace_road(sand, y0, road0.x_at(y0))
    path = resample(line, 6)
    d = [0.0]
    for a, b in zip(path, path[1:]):
        d.append(d[-1] + math.dist(a, b))
    L = d[-1]
    # bãi ải: bề rộng mặt cát đo vuông góc với đường (mặt nạ cát nới cho cả nét chì gạch trên đường): đường ~100 px, bãi ~170–200
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
                peaks.append((i + j - 1) // 2)  # giữa khúc phình
            i = j
        else:
            i += 1
    print(f"Đường thật: {len(path)} điểm, dài {L:.0f} px; bề rộng đường {np.median(prof):.0f} px, ngưỡng bãi {thr}; "
          f"{len(peaks)} khúc phình")
    # ghép khúc phình với 10 ải tướng theo tỉ lệ quãng đường dự kiến
    want = [s / road0.length for s in stops0]
    got = [d[k] / L for k in peaks]
    stops = []
    for i_, w in enumerate(want):
        cand = [k for k, g in zip(peaks, got) if abs(g - w) < 0.06 and (not stops or d[k] > d[stops[-1]] + 150)]
        if cand:
            stops.append(min(cand, key=lambda k: abs(d[k] / L - w)))
        else:
            z.warn(f"không thấy bãi ải {z.HEADS[i_]} gần {w:.3f} quãng đường; lấy theo tỉ lệ dự kiến")
            stops.append(int(np.argmin([abs(x / L - w) for x in d])))
    # suối và lạch
    blue = (img[..., 2] > img[..., 0] + 60) & (img[..., 2] > img[..., 1])
    sy = water0["streams"][0]
    stream = trace_water(blue, -8, W + 8, np.interp(0, [p[0] for p in sy[::-1]], [p[1] for p in sy[::-1]]))
    (px, py), _ = SPOTS_REAL[POND]
    creek = trace_water(blue, px + 80, W + 8, py - 20)
    data = {
        "path": [[round(x, 1), round(y, 1)] for x, y in path],
        "stops": [round(d[k], 1) for k in stops], "length": round(L, 1),
        "stages": [[round(path[k][0], 1), round(path[k][1], 1)] for k in stops],
        "streams": [[[round(x, 1), round(y, 1)] for x, y in s] for s in (stream, creek) if len(s) > 4],
    }
    (WORK / "that.json").write_text(json.dumps(data), encoding="utf-8")
    soi = Image.fromarray(img.astype("uint8"))
    dr = ImageDraw.Draw(soi)
    dr.line([tuple(p) for p in path], fill=(255, 0, 255), width=4)
    for k in stops:
        x, y = path[k]
        dr.ellipse((x - 30, y - 30, x + 30, y + 30), outline=(255, 0, 0), width=5)
    for s in data["streams"]:
        dr.line([tuple(p) for p in s], fill=(0, 0, 255), width=4)
    for num, ((x, y), r) in SPOTS_REAL.items():
        dr.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 0), width=4)
    soi.save(WORK / "soi_that.png")
    print("  ải tướng:", ", ".join(f"{z.HEADS[i_]} ({path[k][0]:.0f}, {path[k][1]:.0f})" for i_, k in enumerate(stops)))
    print(f"  suối {len(stream)} điểm, lạch {len(creek)} điểm; ghi {WORK / 'that.json'}, {WORK / 'soi_that.png'}")


# ---------- xuất sang Unity ----------

def real_spots(path):
    """địa danh đo tay trên bản đồ ghép (SPOTS_REAL) theo dạng spots của layout: c, r, side (phía so với đường thật)"""
    ys = np.array([p[1] for p in path])
    xs = np.array([p[0] for p in path])
    out = {}
    for num, (c, r) in SPOTS_REAL.items():
        rx = float(np.interp(c[1], ys[::-1], xs[::-1]))
        out[num] = {"c": c, "r": r, "kind": SPOTS[num][1], "side": 1 if c[0] > rx else -1}
    out[BRIDGE] = {"bridge": BRIDGE_REAL}
    return out


def anim_spec(spots, water):
    """phần động trên ảnh (IslandAnim, khoá zone_moc): lá rơi quanh cây thần và rừng trúc, gió ở hang nanh, lấp lánh ở đồng hoa, hang
    pha lê, miếu cây thần; gợn ở hồ lá sen; sóng ngoài biển; gợn chạy dọc suối và lạch. Toạ độ chia W, H; cỡ chia W"""
    items = []
    c, r = spots[BOSS]["c"], spots[BOSS]["r"]
    items += [("leaf", c[0] + dx * r, c[1] + dy * r, 34) for dx, dy in ((-0.9, -0.8), (0.1, -1.2), (0.9, -0.7))]
    items.append(("sparkle", c[0], c[1] + 0.1 * r, 30))
    c, r = spots[8]["c"], spots[8]["r"]
    items.append(("leaf", c[0] + 0.3 * r, c[1] - 0.6 * r, 30))
    c, r = spots[5]["c"], spots[5]["r"]
    items.append(("wind", c[0] + spots[5]["side"] * 0.9 * r, c[1] - 0.3 * r, 80))
    for n, offs in ((2, ((-0.3, -0.2), (0.35, 0.15))), (9, ((-0.3, -0.3), (0.3, 0.1), (0.0, 0.4)))):
        c, r = spots[n]["c"], spots[n]["r"]
        items += [("sparkle", c[0] + dx * r, c[1] + dy * r, 30) for dx, dy in offs]
    c, r = spots[POND]["c"], spots[POND]["r"]
    items.append(("ripple", c[0] + 0.15 * r, c[1] - 0.05 * r, 64))
    items += [("wave", 230, H - 30, 90), ("wave", 790, H - 40, 90), ("wave", 300, 24, 80), ("wave", 760, 30, 80)]
    rivers = [("stream", [(min(max(x, 2), W - 2), y) for x, y in st[::3]], z.STREAM_W) for st in water["streams"]]
    return {
        "items": [{"k": k, "x": round(x / W, 4), "y": round(y / H, 4), "s": round(sz / W, 4)} for k, x, y, sz in items],
        "rivers": [{"k": k, "w": round(rw / W, 4), "pts": [[round(x / W, 4), round(y / H, 4)] for x, y in pts]} for k, pts, rw in rivers],
    }


def xuat(art_out=None, zones_json=None):
    """đưa bản đồ đã ghép vào game, như build_zone70.xuat nhưng theo đường dò được (that.json): Assets/03 Art/Islands/zone_moc.png
    (biển hai mép trong suốt; thay bản đồ 8 ải cũ), khoá zone_moc trong island_anim.json, đảo moc trong zones.json (nodes = 10 bãi ải
    dò được, path = tâm đường thật tới giữa bãi đấu boss, stops, plates). Sau đó chạy menu Unity PokiClash/Nhập dữ liệu.
    art_out, zones_json: ghi chỗ khác để thử (mặc định Assets)."""
    art_out = Path(art_out or ART_OUT)
    zones_json = Path(zones_json or ZONES_JSON)
    th = json.loads((WORK / "that.json").read_text(encoding="utf-8"))
    src = WORK / "zone_moc70.png"
    a = np.array(Image.open(src).convert("RGB"))
    alpha = z.sea_alpha(a)
    rgba = np.dstack([a, (alpha * 255).round().astype("uint8")])
    art_out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(art_out / "zone_moc.png")
    print(f"Đã ghi {art_out / 'zone_moc.png'} ({W} x {H}); biển trong suốt {(alpha < 0.5).mean() * 100:.1f}% ảnh")

    full = [tuple(p) for p in th["path"]]
    d = [0.0]
    for p0, p1 in zip(full, full[1:]):
        d.append(d[-1] + math.dist(p0, p1))
    end = int(np.argmin([abs(x - th["stops"][-1]) for x in d]))  # đường dừng ở giữa bãi đấu boss
    line = full[:end + 1]
    road = z.Road(line)
    stops = th["stops"]
    pts = [tuple(p) for p in th["stages"]]
    spots = real_spots(full)
    water = {"streams": th["streams"]}
    if not art_out.joinpath("island_anim.json").exists() and (ART_OUT / "island_anim.json").exists():
        art_out.joinpath("island_anim.json").write_bytes((ART_OUT / "island_anim.json").read_bytes())
    anim_path = art_out / "island_anim.json"
    anim = json.loads(anim_path.read_text(encoding="utf-8"))
    anim["zone_moc"] = anim_spec(spots, water)
    nl = "\r\n" if b"\r\n" in anim_path.read_bytes() else "\n"
    anim_path.write_text(json.dumps(anim, ensure_ascii=False, indent=1), encoding="utf-8", newline=nl)
    print(f"Đã ghi khoá zone_moc trong {anim_path}: {len(anim['zone_moc']['items'])} món, {len(anim['zone_moc']['rivers'])} suối")

    data = json.loads((zones_json if zones_json.exists() else ZONES_JSON).read_text(encoding="utf-8"))
    zd = next(x for x in data["zones"] if x["id"] == "moc")
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
    zones_json.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Đã ghi đảo moc trong {zones_json}: 10 ải tướng, đường {len(path)} điểm, bảng tên {plates}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar="K [ANH]",
                    help="lưu đoạn K (1..3) GPT trả về (mặc định ảnh mới nhất tai_ve/doan_K*.png) rồi dựng lại gói")
    ap.add_argument("--ghep", action="store_true", help="ghép 3 đoạn đã duyệt thành zones/moc70/zone_moc70.png")
    ap.add_argument("--that", action="store_true", help="dò đường, bãi ải, suối thật trên bản đồ đã ghép (that.json)")
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
        WORK.mkdir(parents=True, exist_ok=True)
        im.save(WORK / f"doan_{k}.png")
        print(f"Đã lưu {WORK / f'doan_{k}.png'}")
    road, stops, pts, spots, water = layout()
    guide = draw_guide(road, pts, spots, water)
    GUIDES.mkdir(exist_ok=True)
    guide.save(GUIDES / "L_zone70_moc.png")
    save_json(road, stops, pts, spots)
    build_pack(spots, water, guide)
    print(f"Đã ghi {GUIDES / 'L_zone70_moc.png'}, {GUIDES / 'zone70_moc.json'}, gói {PACK}")
    if warnings:
        print(f"{len(warnings)} cảnh báo, xem trên")


if __name__ == "__main__":
    main()
