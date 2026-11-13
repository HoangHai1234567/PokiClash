# -*- coding: utf-8 -*-
"""Gói GPT vẽ boss cuối đảo Mộc (mã làm việc moc_vuong, con gốc của rig: monster_3709). Tướng thứ 10 đảo Mộc.

Người dùng (2026-11-13): "làm tướng cuối cùng ở đảo mộc, final boss; concept như con gốc nhưng phải thay đổi nhiều tránh copy".
Thiết kế dưới đây là ĐỀ XUẤT của Claude, chờ người dùng duyệt: RỒNG TRÚC bốn cánh. Chỉ lấy của con gốc cách dựng (bốn chân, bốn cánh
xếp từ từng chiếc lông rời, đuôi dải dài vắt trước thân, chỗ đặt, cỡ, thứ tự chồng). Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng
bằng mã (moc_vuong.py bo_cuc).

    py -3 -I ArtGen/Spine/moc_vuong.py bo_cuc
    py -3 -I ArtGen/Spine/build_moc_vuong.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/moc_vuong_1/luot_1_concept_<kiểu>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "moc_vuong"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
CHIM_LA = os.path.join(HERE, "inbox", "chim_la_1", "tai_ve", "L1_duyet.png")
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
PK = os.path.join(HERE, "gui_gpt", f"{CODE}_1")
SAVE = os.path.join(HERE, "inbox", f"{CODE}_1", "tai_ve")
MAU = os.path.join(HERE, "inbox", f"{CODE}_1", "mau")


def Wp(p):
    return os.path.normpath(p)


INTRO = ("CREATURE: the BAMBOO DRAGON KING, the final boss of the forest island in a monster-collecting game (plant element): an "
         "ancient, majestic FOUR-LEGGED, FOUR-WINGED dragon-beast that has lived for a thousand years in a golden-bamboo grove. "
         "Everything on it grows from BAMBOO: its four wings are fans of long bamboo LEAVES, its two tall horns are cut bamboo "
         "stalks, its armour is split bamboo, its tail is one endless ribbon-like leaf. Proud, fierce, calm and dangerous, a "
         "ruler: NOT cute, NOT chibi (adult heroic proportions, the head is small compared to the body and wings), NOT a "
         "smiling mascot, NOT scary or monstrous, NOT a human, NOT a bird (no beak).")

STANCE = ("STANCE (the same in the layout guide, image 1): the beast stands on all four legs in a low, proud guard, seen in a "
          "three-quarter view, FACING THE VIEWER'S RIGHT. Chest forward, neck curved up in an S, the head held high in the upper "
          "middle of the picture (about x = 838-1022, y = 354-494) in profile looking to the RIGHT, so ONLY ONE eye is visible. "
          "The two UPPER wings are raised and spread wide in a big V behind the body; the two LOWER wings hang down and outward "
          "over the flanks like a cloak. The long tail sweeps around from behind and lies across the FRONT of the legs. "
          "Symmetrical, monumental, like a crest or a throne.")

PARTS = (
    "- UPPER WINGS (the biggest shapes of the picture; the NEAR one on the viewer's left from about x = 162 to x = 819, "
    "y = 69 to y = 755; the FAR one on the right from about x = 883 to x = 1375, y = 70 to y = 760): each wing is a FAN of about "
    "twenty-five SEPARATE long BAMBOO LEAVES growing out of the shoulder, overlapping like roof tiles. A bamboo leaf is a slender "
    "lance: narrow where it is attached, widest about one third along, then tapering to a long sharp point, with ONE thin centre "
    "vein and two or three fine parallel side veins. Three tiers, as in the guide: the OUTER, longest leaves (up to about 330 px "
    "long) are {la_dam_t}; the MIDDLE leaves are {la_t}; the short INNER leaves near the shoulder are {la_nhat_t}. The leaf tips "
    "at the top and the outer edge of each wing stick out freely one by one (a spiky, feathery edge, never one smooth outline). "
    "Three or four tiny loose leaves float just off the outer tips of each wing. From under each upper wing ONE long thin VINE "
    "tendril hangs down and curls outward, ending in a small curled hook with a {nhan_t} bud (near side: about x = 185-420, "
    "y = 610-770; far side: about x = 1180-1350, y = 600-770).\n"
    "- LOWER WINGS (the NEAR one from about x = 312 to x = 794, y = 536 to y = 941; the FAR one from about x = 983 to x = 1344, "
    "y = 553 to y = 962): smaller fans of about twenty SEPARATE leaves that hang DOWN and outward, shorter and broader than the "
    "upper ones, coloured like DRIED GOLDEN bamboo leaves: {nga_t}, the lower rows {nga_dam_t}, and the last long leaves at the "
    "bottom outer corner {la_nhat_t}. Same leaf shape, each with a centre vein.\n"
    "- HORNS (two, very tall, from the top of the head up to about y = 57; together about x = 698-1077, y = 57-426; the near "
    "horn is the bigger one and leans a little to the left, the far horn is slimmer and stands behind it): each horn is a thick "
    "stalk of GOLDEN BAMBOO, gently curved backward, made of three or four segments with a raised dark-green NODE ring between "
    "segments, its TIP CUT DIAGONALLY into a sharp point like a bamboo spear. From the upper node of each horn grows ONE thin "
    "twig carrying two or three small fresh-green bamboo leaves. No flames, no antler branches.\n"
    "- HEAD (about x = 838-1022, y = 354-494): a noble DRAGON head in profile (like an Asian kirin crossed with a wolf; NOT a "
    "bird, NO beak): a long tapering muzzle with a nostril slit, the mouth shut in a firm line with TWO small fangs showing; a "
    "heavy slanted brow plate; ONE visible eye, narrow and sharp, amber iris with a vertical slit pupil; a leaf-shaped ear "
    "pointing back; a short pointed chin tuft. {dau_t}\n"
    "- MANE (about x = 611-1003, y = 307-675): a thick mane of long pointed locks runs from the forehead, between the horns, "
    "down the back of the neck to the shoulders, each lock a separate clear shape sweeping to the LEFT; {bom_t}.\n"
    "- NECK, CHEST AND BODY (about x = 648-1021, y = 361-834): a strong curved neck and a deep chest covered in short fur, "
    "{than_t}. Down the FRONT of the neck runs a row of six or seven overlapping belly plates shaped like short bamboo "
    "segments, {vay_t}.\n"
    "- CHEST ARMOUR (about x = 791-1053, y = 544-733): a collar of pale SPLIT-BAMBOO plates lies around the base of the neck: "
    "two pointed plates spreading left and right like a yoke, and in the middle of the chest ONE big oval polished JADE stone "
    "(about 70 px tall, {ngoc_t}) held in a bamboo frame, with a small pointed tassel of pale leaves below it. On each shoulder "
    "sits a SHOULDER GUARD made of a curved piece of split bamboo with one small jade stud (near: about x = 754-899, "
    "y = 531-666; far: about x = 1008-1081, y = 548-668). {giap_t}\n"
    "- LEGS (four; near front leg about x = 684-967, y = 603-958; far front leg about x = 920-1234, y = 597-958; near hind leg "
    "about x = 575-757, y = 731-959; far hind leg about x = 797-952, y = 764-955): powerful big-cat / dragon legs planted wide. "
    "Upper legs in body fur. Each LOWER leg wears a GREAVE of three bamboo segments with node rings, {chan_t}; a small tuft of "
    "{nga_dam_t} leaves sticks out behind each front elbow. Big paws with four toes, {ban_t}, each toe ending in a short "
    "strong claw.\n"
    "- TAIL (about x = 376-1301, y = 620-974): one enormously long, FLAT, ribbon-like tail shaped like a single giant bamboo "
    "leaf / blade of grass, about 110 px wide: it comes out from behind the hindquarters at the left (about x = 380, y = 640), "
    "sweeps down and to the right in a big loop ACROSS THE FRONT of the legs (lowest at about y = 960), and its end rises and "
    "flicks up at the far right (about x = 1250-1300, y = 760). It twists once like a ribbon, so both faces show: the upper "
    "face {la_t}, the under face {la_dam_t}; one centre vein runs along it; three or four short pointed side blades split off "
    "its edges. It partly hides the feet, exactly as in the guide.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into about 170 separate pieces and animated with a 2D "
        "skeleton): calm, clean resting pose exactly as in the guide. EVERY LEAF of every wing is its own closed shape with its "
        "own complete ink outline, overlapping its neighbours like tiles; do not merge leaves into one mass and do not draw "
        "leaves as mere lines inside a big shape. Likewise every mane lock, each horn, the head, each armour plate, the jade "
        "stone, each shoulder guard, each leg segment, each paw and the tail are clear, simple, closed shapes. No flying dust, "
        "no falling leaves other than the few listed, no speed lines, no glow, no aura, no ground, no grass, no props, no "
        "second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram made of rough blobs with jagged edges: take ONLY the placement, the sizes, the "
        "overlaps and the kind of colour of each piece from it, never its line, its jagged edge noise or its exact blob shapes "
        "(its horns are plain tubes and its head is a rough blob: design them properly as described). Design the real shape of "
        "every piece yourself: elegant, sharp, readable shapes with a clear silhouette, the way a carefully designed legendary "
        "Pokemon is drawn. Do not leave any piece as a plain empty blob.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece (body, head, horns, "
        "legs, tail, armour), about 4 px around each wing leaf and mane lock, and about 3 px for small details (veins, eye, "
        "claws, node rings); every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal "
        "hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude scribble "
        "nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one "
        "leaf on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the "
        "jade, not on the bamboo), no gloss, no reflections, no glow, no rim light, no gradients, no 3D look, no translucent "
        "crystal look. The only exception: one tiny light dot in the eye. A different tone appears only where the design itself "
        "lists a different colour (for example the three tiers of leaves).")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the character.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole figure is about 1215 px wide (wing tip at about x = 162 to wing "
         "tip at about x = 1375) and about 920 px tall (horn tips at about y = 57 to the feet and the tail loop at about y = 974).")

D = {
    "nga": dict(
        ten="rồng trúc ngà: lông kem, mặt vảy ngọc, cánh lá trúc lục + cánh lá ngà vàng",
        la_dam_t="deep bamboo green (#2F6B3F)", la_t="fresh bamboo green (#5FA84A)", la_nhat_t="pale young green (#A8D468)",
        nga_t="ivory-bamboo gold (#E8C04A)", nga_dam_t="darker old gold (#C99A2E)", nhan_t="vermilion (#D9482B)",
        ngoc_t="jade green #3FBF8F",
        dau_t=("The top of the head, the brow and the upper muzzle are covered in smooth jade-green scales (#3E8F6A); the lower "
               "jaw, cheek and throat are cream (#F4EBD0); the brow plate has a thin gold (#E8C04A) edge."),
        bom_t="cream white (#F4EBD0), the tips of the longest locks pale young green (#A8D468)",
        than_t="cream (#F4EBD0)",
        vay_t="jade green (#3E8F6A) with a thin darker edge",
        giap_t="All armour bamboo is pale ivory (#E9D9A6) with dark-green node lines.",
        chan_t="dark bamboo green (#2A5A4A) with pale ivory node rings",
        ban_t="ivory-bamboo gold (#E8C04A) with dark-green (#2A5A4A) claws",
        mau=("COLOURS, a fresh, noble palette (use exactly these, each area one flat colour; three hues only: bamboo GREEN as the "
             "main colour, ivory GOLD as the second, cream as the neutral, plus tiny vermilion accents): outer wing leaves and "
             "tail underside deep bamboo green (#2F6B3F); middle wing leaves and tail top fresh green (#5FA84A); inner wing "
             "leaves, mane tips and lowest lower-wing leaves pale young green (#A8D468); lower wings and horns and paws "
             "ivory-bamboo gold (#E8C04A), their second rows old gold (#C99A2E); fur, mane, jaw cream (#F4EBD0); head scales "
             "and neck plates jade (#3E8F6A); greaves and claws dark green (#2A5A4A); armour bamboo pale ivory (#E9D9A6); the "
             "jade stone and studs #3FBF8F; vine buds vermilion (#D9482B); eye amber (#F0AA32) with a dark pupil; ink #2B2118.")),
    "mac": dict(
        ten="rồng trúc mực: lông than mực, giáp vàng ngà, cánh lục bảo + cánh vàng",
        la_dam_t="deep emerald (#1E543E)", la_t="emerald green (#348C5C)", la_nhat_t="light leaf green (#78C480)",
        nga_t="ivory gold (#ECC450)", nga_dam_t="darker old gold (#C49228)", nhan_t="vermilion (#D9482B)",
        ngoc_t="jade green #3FBF8F",
        dau_t=("The whole head is covered in short ink-charcoal fur and scales (#3A4440); the brow plate, the ridge of the "
               "muzzle and the chin tuft are ivory gold (#ECC450); the lower jaw is a slightly lighter grey (#59645F)."),
        bom_t="cream white (#F0E8CE), the tips of the longest locks ivory gold (#ECC450)",
        than_t="ink charcoal (#3A4440), like black bamboo",
        vay_t="old gold (#C49228) with a thin darker edge",
        giap_t="All armour bamboo is ivory gold (#ECC450) with dark node lines.",
        chan_t="near-black ink green (#242C2A) with gold node rings",
        ban_t="ink charcoal (#3A4440) with ivory-gold (#ECC450) claws",
        mau=("COLOURS, a dark, regal palette (use exactly these, each area one flat colour; three hues only: EMERALD green as "
             "the main colour, ivory GOLD as the second, ink charcoal as the neutral, plus tiny vermilion accents): outer wing "
             "leaves and tail underside deep emerald (#1E543E); middle wing leaves and tail top emerald (#348C5C); inner wing "
             "leaves and lowest lower-wing leaves light green (#78C480); lower wings, horns, armour, brow and claws ivory gold "
             "(#ECC450), their second rows and the neck plates old gold (#C49228); body and head fur ink charcoal (#3A4440); "
             "greaves near-black (#242C2A); mane cream (#F0E8CE); the jade stone and studs #3FBF8F; vine buds vermilion "
             "(#D9482B); eye amber (#F0AA32) with a dark pupil; ink #2B2118.")),
}


def main(chon=None):
    os.makedirs(PK, exist_ok=True)
    os.makedirs(SAVE, exist_ok=True)
    ra = []
    for k, d in D.items():
        if chon and k not in chon:
            continue
        bc = os.path.join(MAU, f"bo_cuc_{k}.png")
        if not os.path.exists(bc):
            print("thiếu sơ đồ bố cục, chạy moc_vuong.py bo_cuc trước:", bc)
            continue
        out = os.path.join(SAVE, f"L1_{k}.png")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(bc)}: LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its "
             "resting stance, built from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece "
             "overlaps which (two huge raised fans of green leaves = the upper wings; two hanging fans of golden leaves = the lower "
             "wings; two tall golden tubes = the horns; the small blob between them = the head; the pale mass = mane, neck and "
             "chest with the collar armour and the jade stone; the long green band looping across the bottom = the tail; four legs "
             "under it). Use it ONLY for placement, size, overlap and the kind of colour. It is NOT the art style.",
             f"image 2 = {Wp(CHIM_LA)}: an approved hero of the same game and the same island (a leaf-winged bird), 1536x1024, white "
             "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring, "
             "and see how each leaf of its wings is its own outlined shape. Do NOT copy its species, its design or its colours.",
             f"image 3 = {Wp(KIEM_SI)}: another approved hero of the same island (an armoured langur), 1536x1024, white background: "
             "the same line and flat crayon colouring; see how its bamboo-and-lacquer armour is drawn. Do NOT copy its species, "
             "design or colours.",
             f"image 4 = {Wp(WORLD_STYLE)}: the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
             "outline + coloured pencil / wax crayon hatching), nothing of its content.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.",
             "", "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of "
             "the approved hero images.",
             "", INTRO, "", STANCE, "",
             "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
             "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). The viewer's LEFT side "
             "of the picture is the creature's back and NEAR side; the viewer's RIGHT is where it faces.",
             "", PARTS.format(**d), "", d["mau"], "", POSE, "", SOFT, "", LINE, "", FLAT, "", FRAME, "", BG, ""]
        p = os.path.join(PK, f"luot_1_concept_{k}.txt")
        open(p, "w", encoding="utf-8").write("\n".join(t))
        ra.append((k, d["ten"], p, out, bc))
        print(p)
    hd = ["# Boss cuối đảo Mộc (`moc_vuong`): gói GPT", "",
          "Con gốc của rig: `monster_3709` (game tham khảo). Chỉ lấy cách dựng; hình là thiết kế của mình: **rồng trúc bốn cánh**.", "",
          "## Lượt 1: concept (mỗi kiểu một file, gửi GPT đường dẫn file)", ""]
    for k, ten, p, out, bc in ra:
        hd += [f"- **{k}** ({ten}): `{Wp(p)}`", f"  - lưu: `{Wp(out)}`"]
    hd += ["", "## Ảnh mẫu trong file prompt", "",
           f"1. `{Wp(os.path.join(MAU, 'bo_cuc_<kiểu>.png'))}`: sơ đồ bố cục 1536x1024 nền trắng, máy dựng: hai quạt lá lục to giơ chữ V "
           "(cánh trên), hai quạt lá vàng rủ xuống (cánh dưới), hai ống vàng cao (sừng), khối kem giữa (bờm, cổ, ngực, giáp, ngọc), dải lục "
           "dài vắt ngang phía dưới (đuôi), bốn chân. Chỉ để lấy chỗ đặt, cỡ, thứ tự chồng.",
           f"2. `{Wp(CHIM_LA)}`: concept chim lá đã duyệt, 1536x1024 nền trắng: mốc nét mực, vân sáp, tô phẳng, cách vẽ từng chiếc lá.",
           f"3. `{Wp(KIEM_SI)}`: concept Voọc Tướng đã duyệt, 1536x1024 nền trắng: mốc nét và cách vẽ giáp tre.",
           f"4. `{Wp(WORLD_STYLE)}`: bản đồ thế giới 1024x1536: mốc nét bút mực + chì sáp.", "",
           "## Cách kiểm", "",
           "- Đủ bốn cánh (hai quạt lục giơ lên, hai quạt vàng rủ xuống), từng chiếc lá có viền riêng, không dính thành mảng.",
           "- Đầu rồng mõm dài có nanh, một mắt, nhìn sang PHẢI; không phải mỏ chim. Hai sừng ống trúc vát nhọn, có mắt trúc.",
           "- Đuôi dải lá dài vắt ngang TRƯỚC chân. Bốn chân có ống giáp trúc. Ngọc bích giữa ngực.",
           "- Tô phẳng: không bóng, không điểm sáng trắng, không bóng loáng, không quầng sáng; chỉ một chấm sáng trong mắt.",
           "- Nền trắng tinh, không viền sticker, không đất, không chữ.", "",
           "## Câu sửa nhanh (`--note`)", "",
           "- Còn bóng / điểm sáng: `Remove every highlight, shine spot and shadow: each area one flat colour.`",
           "- Lá dính mảng: `Every wing leaf must be its own closed outlined shape, overlapping like tiles.`",
           "- Ra mỏ chim: `The head is a dragon/kirin head with a long muzzle and fangs, NOT a bird beak.`",
           "- Vẫn chibi: `Not chibi at all: adult heroic proportions, small head, long neck, huge wings.`", ""]
    open(os.path.join(PK, "HUONG_DAN.md"), "w", encoding="utf-8").write("\n".join(hd))
    print(os.path.join(PK, "HUONG_DAN.md"))


# ---------------------------------------------------------------- lượt 1b: sửa SỪNG trên bản nháp kiểu tối (người dùng 2026-11-13: "bản màu
# đen đẹp hơn nhưng 2 cái sừng hình 2 ống tre không đẹp và sừng bên phải đang cắm ở sai chỗ theo logic")
GOC_SUNG = ("WHERE THE HORNS GROW (anatomy, very important): BOTH horns grow out of the TOP OF THE SKULL, on the crown of the head "
            "BEHIND the brow and the eye and just above the ear, side by side like the two horns of a deer or a dragon. The NEAR "
            "horn's root is at about x = 865, y = 340; the FAR horn's root is right next to it, a little further right and partly "
            "hidden behind the near horn's root and the top of the skull, at about x = 925, y = 345. NOTHING grows out of the "
            "muzzle, the nose, the cheek or the neck: in image 1 the right-hand horn wrongly comes up from behind the snout; that "
            "is the mistake to fix. Where the old horns were, draw what is behind them (the wing leaves, the mane) so no gap or "
            "ghost of the old horn is left. A tuft of the cream mane sits between the two horn roots.")

SUNG = {
    "mang": ("sừng măng tre: hai sừng cong to như búp măng xếp bẹ, mực than viền vàng",
             "NEW HORNS, bamboo-SHOOT horns: two big, thick, powerful horns shaped like giant BAMBOO SHOOTS: each is a strong cone, "
             "wide at the root (about 70 px) and tapering smoothly to one very sharp point, sweeping up and BACKWARD in a single "
             "gentle curve; its whole surface is built of five or six overlapping pointed SHEATH scales (like the layered husk of "
             "a bamboo shoot, each sheath a clear shape whose pointed tip lies on the next), coloured ink charcoal (#3A4440) with "
             "an ivory-gold (#ECC450) edge band on every sheath, and the last third of the horn solid ivory gold. The near horn "
             "is the bigger one: from its root it rises up and to the LEFT, its tip at about x = 735, y = 45. The far horn is a "
             "little slimmer: it rises almost straight up and slightly to the right, its tip at about x = 985, y = 70. No twigs, "
             "no leaves on the horns, no flames."),
    "nhanh": ("sừng rồng chia nhánh: gạc rồng vàng ngà ba nhánh nhọn, có mắt trúc",
              "NEW HORNS, branching DRAGON ANTLERS: two long, elegant antlers like those of an Asian dragon or kirin, in ivory "
              "gold (#ECC450): each has one main beam about 40 px thick at the root, tapering, that sweeps up and BACKWARD in an "
              "S curve and splits into THREE sharp, slightly curved tines (one short tine pointing forward low on the beam, two "
              "long ones at the top), every tip a clean sharp point. Three or four thin dark-green node rings cross each beam "
              "like the nodes of bamboo, and the roots are wrapped by a short old-gold (#C49228) collar. The near antler is the "
              "bigger one: it rises up and to the LEFT, its highest tip at about x = 720, y = 45. The far antler rises up and "
              "slightly to the right, its highest tip at about x = 1000, y = 65. No leaves on the antlers, no flames."),
    "liem": ("sừng trúc đen lưỡi liềm: hai sừng dài cong ngược ra sau, mực đen đốt vàng, mũi nhọn",
             "NEW HORNS, long SCIMITAR horns of black bamboo: two long, slender, sleek horns like those of an oryx or an ibex, each "
             "one smooth curve sweeping up and far BACKWARD (toward the upper left), about 46 px thick at the root and tapering "
             "evenly to a needle-sharp point; made of BLACK BAMBOO: near-black ink green (#242C2A), divided into six or seven "
             "segments by thin raised ivory-gold (#ECC450) node rings that get closer together toward the tip, and the last "
             "segment (the tip) solid ivory gold. The near horn is the longer one: from its root it curves up and to the LEFT, "
             "its tip at about x = 640, y = 70. The far horn runs parallel to it just behind and to the right, slightly shorter, "
             "its tip at about x = 760, y = 40. At the root of each horn one small upright jade-green (#3FBF8F) leaf-shaped "
             "crest plate. No twigs, no flames."),
}


def sung(chon=None):
    nhap = os.path.join(SAVE, "L1_mac.png")
    ra = []
    for k, (ten, mo_ta) in SUNG.items():
        if chon and k not in chon:
            continue
        out = os.path.join(SAVE, f"L1_mac_{k}.png")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(nhap)}: the approved DRAFT of this creature (a four-winged bamboo dragon king with an ink-charcoal body), "
             "1536x1024, white background. This is the picture to redraw: its line, flat crayon colouring, pose, proportions and "
             "every piece are right, EXCEPT the two horns.",
             f"image 2 = {Wp(WORLD_STYLE)}: the game's hand-drawn map, 1024x1536: only a reminder of the line and colouring style (brown "
             "ink pen outline + coloured pencil / wax crayon hatching), nothing of its content.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1_mac_{k}_2.png, L1_mac_{k}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.",
             "", "TASK: redraw image 1 as the SAME picture, changing ONLY the horns.",
             "", "KEEP IDENTICAL (if the new picture were laid over image 1, everything except the horns must coincide): the canvas "
             "1536x1024 and the white background; the pose, the size and the place of the whole creature; the four wings leaf by "
             "leaf (shape, place and colour of every leaf); the head (muzzle, fangs, eye, brow, ear), the cream mane, the neck "
             "plates, the collar armour with the jade stone and the shoulder guards, the four legs with their greaves and paws, the "
             "ribbon tail, the two vine tendrils with red buds, the small loose leaves; the wobbly dark-brown pen line, the visible "
             "crayon hatching and the completely flat colours.",
             "", "CHANGE ONLY: REMOVE both yellow bamboo-tube horns together with the little leafy twigs growing on them, and draw new "
             "horns instead.",
             "", mo_ta, "", GOC_SUNG, "",
             "The horns are two separate, clear, closed shapes, each with its own complete dark-brown ink outline (about 5 px), flat "
             "colours with visible crayon hatching: no highlights, no shine, no shadow, no gradient, no glow. Nothing is cut by the "
             "canvas edge (keep the horn tips at least 30 px below the top edge). " + BG, ""]
        p = os.path.join(PK, f"luot_1b_sung_{k}.txt")
        open(p, "w", encoding="utf-8").write("\n".join(t))
        ra.append((k, ten, p, out))
        print(p)
    hd = ["", "## Lượt 1b: sửa sừng trên bản nháp kiểu tối (2026-11-13)", "",
          "Người dùng: \"bản màu đen đẹp hơn nhưng 2 cái sừng hình 2 ống tre không đẹp và sừng bên phải đang cắm ở sai chỗ\". Mỗi file vẽ lại "
          f"`{Wp(nhap)}` (bản nháp 1536x1024 nền trắng: rồng trúc thân mực than), giữ nguyên mọi thứ, chỉ thay hai sừng; cả hai sừng mọc từ "
          "đỉnh sọ sau mày.", ""]
    for k, ten, p, out in ra:
        hd += [f"- **{k}** ({ten}): `{Wp(p)}`", f"  - lưu: `{Wp(out)}`"]
    hd += ["", "Kiểm: hai gốc sừng nằm cạnh nhau trên đỉnh đầu, sau mắt; không còn bóng ống tre cũ; cánh, thân, đuôi trùng bản nháp.", ""]
    f = os.path.join(PK, "HUONG_DAN.md")
    cu = open(f, encoding="utf-8").read().split("\n## Lượt 1b")[0].rstrip("\n") if os.path.exists(f) else ""
    open(f, "w", encoding="utf-8").write(cu + "\n" + "\n".join(hd))


# ---------------------------------------------------------------- lượt 2: mảnh theo KHUNG PART của rig (moc_vuong.py nhom_part)
DUYET = os.path.join(SAVE, "L1_duyet.png")
KIEU = {
    "la": "a single BAMBOO LEAF (most pieces; green ones belong to the upper wings, golden ones to the lower wings or to the elbow "
          "tufts, cream ones to the chest tassel): draw the one centre vein the guide shows and add four to six pairs of very fine "
          "slanted side veins; nothing else. A piece with a notch, a fork or a ragged end is a torn leaf: keep that exact shape.",
    "hang_la": "a ROW of small overlapping leaves seen as one piece with a scalloped edge: draw the little pointed leaves inside it "
               "(each with a centre vein), their tips forming the scallops; keep the outer shape exactly.",
    "day": "a long, curling VINE STREAMER that hangs from a wing: a flat green band like a very long narrow leaf with a centre vein; "
           "at the end where the guide is red sits a small vermilion flower BUD.",
    "dai": "one SECTION of the creature's long flat ribbon-like leaf TAIL: a broad band with one centre vein running lengthwise and a "
           "few fine parallel veins beside it; the short pointed side blades the silhouette shows are part of the leaf.",
    "long": "a patch of short ink-charcoal FUR (a thigh, a shoulder or the back of a paw): one flat charcoal colour with a few short "
            "fur tick strokes in dark-brown ink; no rings, no plates.",
    "giap_chan": "a lower-leg GREAVE of black bamboo: near-black ink green, crossed by the three ivory-gold NODE RINGS the guide shows "
                 "(each ring a clean band with a thin ink line on both sides); a few fine lengthwise grain lines between the rings.",
    "ngon": "ONE TOE of a paw: a charcoal toe ending in the ivory-gold CLAW the guide shows (sharp, slightly curved).",
    "than": "the creature's whole NECK, CHEST AND BELLY in one piece: ink-charcoal short fur with fur tick strokes; the old-gold strip "
            "the guide shows along its edge is the row of overlapping BELLY PLATES shaped like short bamboo segments (keep the guide's "
            "dividing lines as the plate edges, each plate slightly overlapping the next).",
    "giap": "a piece of ivory-gold SPLIT-BAMBOO ARMOUR (a collar plate, a spike or a small knob): one flat gold colour with two or three "
            "fine grain lines along its length and a thin inner edge line.",
    "giap_vai": "a SHOULDER GUARD of ivory-gold split bamboo with fine grain lines and a thin inner edge line; the small green shape the "
                "guide shows on it is a round polished JADE stud.",
    "o_ngoc": "the bamboo FRAME that holds the chest jewel: an ivory-gold rim around a deep-green inner field.",
    "ngoc": "the big polished oval JADE stone of the chest in its thin gold rim: flat jade green, with one simple leaf-shaped engraving "
            "line; no shine, no highlight.",
    "bom": "a lock of the cream-white MANE: flat cream, the pointed strands drawn with a few long flowing ink lines following the lock.",
    "so": "the creature's HEAD WITHOUT THE LOWER JAW, in profile facing RIGHT (the charcoal piece with the gold marks; compare the head "
          "in image 2): the skull and upper jaw of a fierce dragon covered in short ink-charcoal fur; the pointed spikes at its back "
          "(left) are swept-back fur tufts; the muzzle tapers to the right and its lower edge is the upper lip, with a row of four or "
          "five small sharp ivory TEETH and one longer FANG near the front pointing down (keep them inside the silhouette); a small "
          "nostril slit near the tip; where the guide is gold, a heavy ivory-gold BROW PLATE sweeping back over the eye and a small gold "
          "horn stud on the forehead; the EYE (the small amber shape in the gold) is narrow, slanted and angry, amber with a vertical "
          "slit pupil and ONE tiny light dot.",
    "ham": "the LOWER JAW, outer side (the lighter grey strip): charcoal-grey fur, its upper edge is the lower lip with a row of small "
           "sharp ivory teeth pointing up and one longer fang at the front (inside the silhouette); a short pointed chin tuft at the tip.",
    "ham_trong": "the far, inner side of the lower jaw (the near-black strip): plain very dark ink green, no teeth, no detail.",
    "luoi": "the TONGUE (the red piece): flat warm red with one centre line; pointed tip.",
    "tai": "a leaf-shaped EAR (the green piece): a pointed green ear like a bamboo leaf, with a centre vein and a thin gold rim line.",
    "sung": "a HORN shaped like a giant BAMBOO SHOOT, lying on its side (root at the left, sharp tip at the right): a strong smooth cone "
            "built of five overlapping pointed SHEATH scales in ink charcoal, each sheath edged by the ivory-gold V-shaped band the "
            "guide shows (the point of every V aims at the tip), and the last third of the horn solid ivory gold; fine lengthwise grain "
            "lines on each sheath. Keep the cone's exact outline; the flat cut at the root stays flat.",
    "tron": "a plain piece: keep it as the guide shows.",
}


def parts(chon=None):
    import json
    muc = json.load(open(os.path.join(MAU, "part_Q.json"), encoding="utf-8"))
    ra = []
    for to, v in muc.items():
        if chon and to not in chon:
            continue
        khung = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
        kieu = []
        for kv in khung.values():
            if kv["kieu"] not in kieu:
                kieu.append(kv["kieu"])
        gd = os.path.join(MAU, f"part_{to}.png")
        out = os.path.join(SAVE, f"N_{to}.png")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(gd)}: PIECE GUIDE, 1536x1024, white background: {len(khung)} separate flat computer-made shapes. Each shape is "
             "ONE loose piece of the creature of image 2 (the creature has been taken apart for 2D skeletal animation), lying exactly "
             "where it must be on the canvas, at its exact size and angle, filled with its flat colour.",
             f"image 2 = {Wp(DUYET)}: the approved picture of the creature these pieces belong to (a four-winged bamboo dragon king with an "
             "ink-charcoal body, leaf wings, gold bamboo armour), 1536x1024, white background: use it ONLY to see the hand-drawn line, "
             "the crayon hatching, the flat colours and what each material looks like. Do NOT draw the creature.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.",
             "", f"TASK: redraw image 1 as a clean hand-drawn sheet of the same {len(khung)} loose pieces, in the style of image 2.",
             "", "KEEP EXACTLY (if the new sheet were laid over image 1, every piece must coincide with its shape): the canvas 1536x1024 and "
             "the pure-white background; the NUMBER of pieces; each piece's place, size, angle and SILHOUETTE (the same outline, bump for "
             "bump, the same pointed ends: do not straighten, round off, simplify, enlarge or shrink anything); each piece's flat "
             "colours exactly where the guide has them. Pieces never touch or overlap each other: keep the white gaps between them. Do "
             "not add any piece, do not join pieces, do not leave any out.",
             "", "WHAT THE PIECES ARE:"]
        t += [f"- {KIEU[k]}" for k in kieu]
        t += ["", "HOW TO DRAW EACH PIECE: a closed dark-brown ink outline (#2B2118) all the way around, sitting exactly on the edge of the "
              "guide's shape, about as thick as the guide's outline, slightly wobbly like a real pen; inside, the guide's flat colour "
              "with loose diagonal coloured-pencil / wax-crayon hatching clearly visible (texture only); inner detail lines thinner than "
              "the outline. FLAT COLOUR, NO LIGHT: no shading, no darker or lighter patches, no highlights, no shine, no gloss, no "
              "gradients, no shadows under or beside the pieces, no glow. No text, no labels, no numbers, no frame, no arrows.", ""]
        p = os.path.join(PK, f"luot_2_part_{to}.txt")
        open(p, "w", encoding="utf-8").write("\n".join(t))
        ra.append((to, v["nhom"], len(khung), p, out, gd))
    print(len(ra), "file prompt lượt 2 →", PK)
    hd = ["", "## Lượt 2: mảnh theo khung part của rig (2026-11-13, sau khi chốt concept bản tối + sừng măng)", "",
          f"Concept đã duyệt: `{Wp(DUYET)}` (1536x1024 nền trắng: rồng trúc thân mực than, bốn cánh lá, sừng măng).", "",
          "Mỗi tờ: ảnh 1 là tờ hướng dẫn (các khối phẳng máy dựng, mỗi khối một mảnh rời nằm đúng chỗ, đúng cỡ); ảnh 2 là concept đã duyệt "
          "(chỉ để lấy nét và chất liệu). GPT vẽ lại sạch từng mảnh, giữ nguyên hình bóng. Claude cắt bằng `moc_vuong.py cat_part Q<k>`.", ""]
    for to, nh, n, p, out, gd in ra:
        hd += [f"- **{to}** ({nh}, {n} mảnh): `{Wp(p)}`", f"  - ảnh 1: `{Wp(gd)}`; lưu: `{Wp(out)}`"]
    hd += ["", "Kiểm: đủ số mảnh, mảnh không dính nhau, hình bóng trùng tờ hướng dẫn (Claude đo IoU, dưới 0,9 thì gen lại tờ đó); tô phẳng, "
           "không bóng, không điểm sáng.", ""]
    f = os.path.join(PK, "HUONG_DAN.md")
    cu = open(f, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n") if os.path.exists(f) else ""
    open(f, "w", encoding="utf-8").write(cu + "\n" + "\n".join(hd))


if __name__ == "__main__":
    if sys.argv[1:2] == ["parts"]:
        parts(sys.argv[2:] or None)
    elif sys.argv[1:2] == ["sung"]:
        sung(sys.argv[2:] or None)
    else:
        main(sys.argv[1:] or None)
