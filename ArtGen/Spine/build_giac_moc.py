# -*- coding: utf-8 -*-
"""Gói GPT vẽ thú một sừng đảo Mộc (mã làm việc giac_moc, con gốc của rig: monster_3804). Tướng thứ 9 đảo Mộc (suất moc_tinh, ải 60).

Người dùng (2026-11-13): "sinh vật lớn, đi lại bằng 4 chân, có 1 sừng ở trên đầu, các phần trên lưng bạn có thể chủ động đổi thành dây
leo, hoa..."; chiêu cuối mở phần bụng, "trong phần bụng sẽ có 1 quả cầu năng lượng kiểu trái tim phát sáng (luôn có sẵn)"; "trước khi làm
cho tôi xem concept". Hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ đặt, cỡ, thứ tự
chồng từng part); hình là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (giac_moc_bo_cuc.py).

    py -3 -I ArtGen/Spine/giac_moc_bo_cuc.py all all
    py -3 -I ArtGen/Spine/build_giac_moc.py            (lượt 1b "mở ngực" của hướng nào chỉ dựng khi đã có tai_ve/L1_<hướng>.png)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/giac_moc_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "giac_moc"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
NGUOI_CAY = os.path.join(HERE, "inbox", "nguoi_cay_2", "tai_ve", "L1_duyet.png")
VOI_RUNG = os.path.join(HERE, "inbox", "voi_rung_2", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk():
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{K}")


def save_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "tai_ve")


def mau_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "mau")


STANCE = ("STANCE (the same in the layout guide, image 1): the beast stands on all FOUR legs in a broad, planted, battle-ready stance, "
          "seen from the side and slightly from the front, facing the viewer's RIGHT. The front of the body is raised higher than "
          "the rump (a proud, heavy, lion-like slope from the high shoulders down to the low hindquarters). The neck rises from the "
          "shoulders and the head is held high at the upper right, chin tucked, looking to the right in a three-quarter profile so "
          "that ONLY ONE eye is visible. The single great horn points forward and up to the upper right corner. The four legs are "
          "thick pillars set wide apart, all four feet flat on the same ground level. NO tail is visible (the foliage on the back "
          "covers the rear). The mouth is CLOSED. Calm but tense: a guardian that has just noticed an intruder. Majestic, fierce "
          "and battle-ready; appealing, not horror, not a skeleton, not a smiling cute mascot.")

BODY = (
    "- HORN (ONE horn only, the biggest feature of the head): it grows from the top of the snout at about x = 810, y = 760 and "
    "sweeps forward and up to its tip at about x = 980, y = 505; about 110 px thick at the base, tapering to a point. {sung}\n"
    "- HEAD (about x = 655 to x = 880, y = 675 to y = 890; one single solid piece, the mouth closed): a strong wedge-shaped "
    "head with a heavy brow and a short blunt muzzle pointing to the lower right (muzzle tip at about x = 830, y = 880). ONE "
    "eye at about x = 795, y = 765: narrow, sharp, determined, under a slanting brow. {dau}\n"
    "- HEAD CREST (behind and above the head, about x = 450 to x = 800, y = 465 to y = 750): FOUR very long, narrow blades that "
    "start at the back of the skull (about x = 700, y = 700) and sweep back and up like the feathers of a war bonnet, their "
    "tips at about (455, 510), (600, 470), (735, 505) and (790, 570); between them, behind the skull, a tuft of shorter "
    "lighter leaves. {mao}\n"
    "- NECK (from the head at about x = 700, y = 800 down to the shoulders at about x = 620, y = 1000): thick and muscular, the "
    "same hide as the body; down the BACK of the neck sit three small overlapping plates. {co}\n"
    "- BACK GARDEN, rear mass (behind and above the body, about x = 50 to x = 700, y = 580 to y = 1175): a big wild mane of "
    "about ten large separate pieces growing from the whole length of the back and streaming backward to the LEFT as if in a "
    "wind, the longest ones ending in thin drooping tips at about (285, 600), (150, 860), (50, 970) and (150, 1165). {la}\n"
    "- BACK ROW (a sawtooth row along the spine in front of that mane, from the withers at about x = 590, y = 800 down to the "
    "rump at about x = 270, y = 1040): FOUR tall pale plates, each about 150 px tall, leaning backward, alternating with FIVE "
    "pointed pieces of the same height standing just behind them. {hang}\n"
    "- BODY: a massive barrel. The SHOULDER is a big rounded muscle mass at about x = 370 to x = 650, y = 935 to y = 1250; the "
    "RUMP a second rounded mass at about x = 225 to x = 490, y = 975 to y = 1245, lower than the shoulder. {than}\n"
    "- SHOULDER RUFF AND THORNS: a ragged ruff sits on top of the near shoulder (about x = 520 to x = 690, y = 910 to "
    "y = 1060) and a smaller one behind the near elbow (about x = 380 to x = 450, y = 1120 to y = 1230). {reu} Out of the "
    "ruff on the near shoulder one thick short THORN points forward to the right (about x = 600 to x = 740, y = 900 to "
    "y = 990), and a second one sticks out from the far shoulder in front of the chest (about x = 800 to x = 875, y = 935 to "
    "y = 990). {cua}\n"
    "- CHEST POD (the special feature; about x = 600 to x = 810, y = 900 to y = 1250): on the FRONT of the chest, between and "
    "in front of the forelegs, bulges ONE big round closed pod, like a barrel carried on the breast; it reaches from the "
    "throat down to the height of the knees. {vo} It is CLOSED now. In the narrow seams between its plates thin lines of "
    "bright {khe} show, as if something bright were sealed inside (flat coloured lines only, NO glow). Along its front edge, "
    "from the throat at about x = 735, y = 800 down and around the bottom to about x = 640, y = 1245, runs a rim. {vanh}\n"
    "- LEGS (FOUR, all visible): thick, heavy pillar legs, each made of an upper leg, a lower leg and a big broad foot with FOUR "
    "toes; each toe ends in one large blunt claw. NEAR foreleg (in front of everything, about x = 400 to x = 600, y = 1000 to "
    "y = 1450; foot at about x = 425 to x = 605, y = 1370 to y = 1450). NEAR hind leg at the far left (about x = 90 to "
    "x = 335, y = 1140 to y = 1440; foot at about x = 90 to x = 255). FAR foreleg at the right, stepping forward under the "
    "pod (about x = 655 to x = 930, y = 1200 to y = 1435; foot at about x = 755 to x = 930). FAR hind leg between the near "
    "legs, mostly hidden (about x = 300 to x = 470, y = 1230 to y = 1430). {chan}")

FRAME = ("CANVAS AND FRAMING: portrait 1024x1536, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure fills the LOWER two thirds of the canvas: about 940 px wide (from "
         "the tips of the back foliage at about x = 50 to the tip of the horn at about x = 985) and about 990 px tall (from the top "
         "of the head crest at about y = 465 to the feet at about y = 1455). Leave the top of the canvas (above y = 440) empty "
         "white; do NOT enlarge or move the figure to fill it.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into many separate pieces and animated with a 2D skeleton): "
        "calm, clean resting pose exactly as in the guide. Draw every piece as a clear, simple, closed shape with its own ink "
        "outline, so that the pieces can be separated: horn / head / each crest blade / each piece of the back garden / each "
        "plate and each pointed piece of the back row / shoulder ruff / each thorn / every single plate of the chest pod / its "
        "rim / each leg (upper leg, lower leg, foot, each toe with its claw). Pieces of the back garden overlap like roof "
        "tiles but each keeps its own complete outline. No dust, no falling leaves, no petals in the air, no speed lines, no "
        "glow, no ground, no grass, no props, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram made of rough blobs: take ONLY the placement, the sizes, the overlaps and the "
        "kind of colour of each piece from it, never its line, its edge noise or its exact blob shapes (its flame-like ragged "
        "blobs on the back are only placeholders). Design the real shape of every piece yourself as described: bold, chunky, "
        "readable shapes with a clear silhouette and a rich but tidy amount of detail, the way a carefully designed final-stage "
        "Pokemon-like monster is drawn. Do not leave any piece as a plain empty blob. Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for "
        "small details (toes, claws, the eye, leaf veins, bark lines, seams of the pod); every area coloured with coloured "
        "pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside "
        "the outline. Clean and appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one "
        "piece on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the "
        "horn, not on the crystals, not on the claws), no gloss, no reflections, no glow, no halo, no rim light, no gradients, "
        "no 3D look. The only exception: one tiny light dot in the eye. A different tone appears only where the design itself "
        "lists a different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the character.")

D = {}

D["co_thu"] = dict(
    ten="thú cổ thụ: thân vỏ cây nâu, sừng gỗ ngọn hổ phách, lưng dương xỉ + dây leo + tinh thể hổ phách, ngực là thùng vỏ cây",
    intro=("CREATURE: an ANCIENT TREE BEAST, the plant-element guardian boss of a deep forest in a monster-collecting game: a huge "
           "four-legged animal, built like a cross between a rhinoceros and a bison with a lion's proud chest, whose whole body "
           "has turned into LIVING WOOD over a thousand years. Its hide is walnut-brown bark, moss grows on its shoulders, its "
           "back carries a wild garden of ferns, vines and amber crystals, ONE great horn of dark ringed wood with an amber "
           "crystal tip rises from its nose, and on the front of its chest it carries a sealed barrel of dark bark plates with "
           "amber light in the seams. It is an animal, NOT a tree with legs, NOT a human, NOT a dragon, NOT a dinosaur skeleton."),
    parts=dict(
        sung=("Dark old wood (#543A28) with three or four pale ring bands around it like the growth rings of a ram's horn; the "
              "last third, the TIP, is one sharp faceted AMBER CRYSTAL (#E8A838), a clean long shard with two or three facet "
              "lines, set into the wood like a spearhead."),
        dau=("The head is carved-looking smooth wood, a little lighter than the body (#966A46), with two or three short bark "
             "cracks; a pale wood (#D6BC8C) plate covers the lower jaw and chin; the eye has a bright amber-yellow iris "
             "(#FFD650) and a dark pupil; one nostril slit; the mouth is a firm closed line turned slightly down, with ONE "
             "small pale fang tip showing at the corner. A short thorn stands on the brow above the eye."),
        mao=("The four blades are long narrow LEAVES like the blades of a sword fern or a bromeliad, deep fern green (#3E7846) "
             "with one pale midrib line each; the tuft is young leaf green (#82B050)."),
        co="The plates are pale wood (#DAC496), like small bracket shields.",
        la=("They are huge FERN FRONDS and broad jungle LEAVES, deep fern green (#3E7846), each with a clear midrib and a few "
            "side veins, edges cut into big simple lobes (no tiny fringe); two or three of them end in long curling VINE "
            "TENDRILS (#5A8C3C), and two thin vines with small heart-shaped leaves trail out at the left (about x = 190 to "
            "x = 310, y = 815 to y = 940). The two rearmost fronds behind the head are young leaf green (#82B050)."),
        hang=("The four plates are pale wooden THORN PLATES (#DAC496), shaped like big curved shark fins or the back plates of "
              "a stegosaurus, each with two or three wood-grain lines; the five pointed pieces are raw AMBER CRYSTALS "
              "(#E8A838), chunky faceted shards with a few facet lines, growing out of the back between the plates."),
        than=("Walnut-brown bark hide (#7A5438) with a few long calm bark furrows following the muscles and two or three small "
              "knots; a paler underside (#D6BC8C) shows only as a narrow band under the belly behind the pod."),
        reu="Both ruffs are thick MOSS (#6E963E) with a scalloped, tufted lower edge.",
        cua="The thorns are dark root wood (#543A28).",
        vo=("It is built of about TEN big overlapping BARK PLATES of dark bark (#5C402C), arranged in rows like the staves of a "
            "barrel or the scales of a pine cone, each plate a clear four- or five-sided shape with one bark line; along the "
            "side of the pod next to the near foreleg, a column of about six smaller PALE WOOD rib plates (#DAC496) climbs "
            "from the elbow up to the base of the neck."),
        khe="amber yellow (#FFD650)",
        vanh=("The rim is a thick green VINE (#3E7846) wound along the edge like a rope binding the barrel shut, with eight or "
              "nine small pointed leaves along it and three small dark thorns pointing forward."),
        chan=("The upper legs are the same walnut bark as the body (#7A5438); the feet and toes are darker root wood "
              "(#543A28), shaped like the spreading roots of a tree; the claws are amber (#E8A838). A short dark thorn spur "
              "sticks out of the back of each heel.")),
    palette=("COLOURS, a warm deep forest palette (use exactly these, each area one flat colour): body bark walnut brown "
             "(#7A5438); head a lighter wood (#966A46); underside, jaw plate, neck plates and back thorn plates pale wood "
             "(#D6BC8C / #DAC496); horn wood, feet, thorns very dark root brown (#543A28); pod plates dark bark (#5C402C); "
             "fronds, crest blades and the rim vine deep fern green (#3E7846); young leaves (#82B050); vine tendrils "
             "(#5A8C3C); moss (#6E963E); the horn tip, the back crystals and the claws amber (#E8A838); the eye and the light "
             "lines in the pod seams bright amber yellow (#FFD650), flat, not glowing; every outline dark-brown ink (#2B2118). "
             "Only these colours. NO purple, NO blue, NO grey stone, NO white bone, NO pink, NO red."),
    mo=dict(
        long=("the inside of the pod is a dark hollow (#462C24) lined with a few pale root strands (#D6BC8C) that run down the "
              "walls and curl around the heart like the fingers of a hand holding it"),
        tim=("the HEART: one big round ball of pure amber-yellow energy (#FFD650), about 140 px across, with a slightly darker "
             "amber ring (#E8A838) just inside its outline and ONE small simple spiral or seed mark in its middle, like a "
             "glowing seed or a drop of sunlit sap"),
        vo_mo=("the dark bark plates have slid apart and back along the sides of the pod like the slats of a rolling shutter: "
               "they are now stacked closely, overlapping, in a narrow band along the LEFT edge of the opening and the bottom"),
        check="Lòng ngực sẫm có vài sợi rễ nhạt ôm lấy **quả tim tròn vàng hổ phách** (có một vòng sẫm hơn và một dấu xoắn / hạt ở giữa)."),
    check=["Thân là **vỏ cây nâu**, không phải cây có chân, không phải bộ xương; sừng gỗ sẫm có vòng, **ngọn là tinh thể hổ phách**.",
           "Lưng: **dương xỉ + lá to + tua dây leo**; hàng sống lưng xen **4 tấm gai gỗ nhạt** và **5 tinh thể hổ phách**.",
           "Ngực: **thùng vỏ cây sẫm** khoảng 10 tấm, **khe sáng vàng hổ phách**, vành là dây leo quấn; cột tấm sườn gỗ nhạt cạnh chân trước."],
)

D["bach_thu"] = dict(
    ten="bạch thú hoa: thú lông trắng kem, sừng gỗ xoắn ngọn vàng, lưng lá to + dây leo + nụ sen hồng, ngực là một nụ hoa khổng lồ",
    intro=("CREATURE: a WHITE FLOWER BEAST, the plant-element sacred guardian boss of a deep forest in a monster-collecting "
           "game: a huge four-legged animal with short cream-white fur, built like a cross between a bison and a lion with a "
           "rhinoceros's single horn. A whole garden grows on it: its mane and back are big deep-green leaves, vines and pink "
           "lotus buds, ONE great horn of twisted brown wood with a golden tip rises from its nose, and on the front of its "
           "chest it carries ONE giant closed FLOWER BUD of deep pink petals with golden light in the seams. It is a living "
           "animal, NOT a plant with legs, NOT a human, NOT a dragon, NOT a dinosaur, NOT a toad or a turtle."),
    parts=dict(
        sung=("Warm brown wood (#966A46) twisted like a rope or a unicorn's horn, with four or five spiral grooves; a thin "
              "green vine (#56963E) with two small leaves winds once around its base; the last third, the TIP, is one smooth "
              "pointed GOLDEN bud-shaped spike (#F4C446), like a closed flower bud of gold."),
        dau=("The head is covered in short cream-white fur (#F0E8D6), with a broad flat forehead, a dark brown nose pad "
             "(#785C42) on the blunt muzzle, and a tuft of longer fur under the chin; the eye has a warm orange-amber iris "
             "(#E89628) and a dark pupil, with a dark rim line; the mouth is a firm closed line turned slightly down. A "
             "small pointed ear shaped like a leaf sits behind the eye."),
        mao=("The four blades are long narrow LEAVES, deep green (#2E7C54) with one pale midrib line each; the tuft is light "
             "green (#8CBE60) and carries ONE small open pink flower."),
        co="The plates are light green sepals (#96C46E), like small leaf shields.",
        la=("They are huge broad jungle LEAVES (banana-leaf and monstera shapes), deep green (#2E7C54), each with a clear "
            "midrib and a few side veins, edges cut into big simple lobes (no tiny fringe); two or three of them end in long "
            "curling VINE TENDRILS (#56963E), and two thin vines with small heart-shaped leaves and two tiny white blossoms "
            "trail out at the left (about x = 190 to x = 310, y = 815 to y = 940). The two rearmost leaves behind the head "
            "are light green (#8CBE60)."),
        hang=("The four plates are big upright light-green SEPALS (#96C46E), shaped like broad curved leaf blades or the back "
              "plates of a stegosaurus, each with one midrib; the five pointed pieces are closed pink LOTUS BUDS (#E87896), "
              "plump pointed buds each made of three visible petals, standing between the sepals."),
        than=("Short cream-white fur (#F0E8D6), drawn smooth with only a few short fur ticks at the joints and along the "
              "belly line; a slightly warmer cream (#E2D6BE) shows only as a narrow band under the belly behind the bud."),
        reu="Both ruffs are collars of fresh green LEAVES (#68A848) with pointed tips, like a ruff of ivy.",
        cua="The thorns are green-brown rose thorns (#785C42).",
        vo=("It is ONE giant closed LOTUS BUD seen from the side: about TEN big overlapping PETALS of deep rose pink "
            "(#D65882), arranged in rows like roof tiles, each petal a clear rounded shape with one centre line; along the "
            "side of the bud next to the near foreleg, a column of about six smaller PALE PINK petals (#F0A0B4) climbs from "
            "the elbow up to the base of the neck."),
        khe="golden yellow (#FFE26E)",
        vanh=("The rim is a thick green STEM with eight or nine pointed SEPALS (#2E7C54) that clasp the bud from the front "
              "like fingers, and three small thorns pointing forward."),
        chan=("The upper and lower legs are cream-white fur (#F0E8D6) with a fringe of longer fur behind the knee; the feet "
              "are big furry paws with brown toes (#785C42); the claws are golden (#F4C446). A small green leaf spur sticks "
              "out of the back of each heel.")),
    palette=("COLOURS, a fresh, bright sacred-forest palette (use exactly these, each area one flat colour): fur cream white "
             "(#F0E8D6); belly band warmer cream (#E2D6BE); nose, toes and thorns brown (#785C42); horn wood (#966A46); big "
             "leaves, crest blades and the bud's sepals deep green (#2E7C54); light leaves (#8CBE60); upright back sepals and "
             "neck plates light green (#96C46E); leaf ruffs (#68A848); vines (#56963E); the chest bud's petals deep rose pink "
             "(#D65882) and pale pink (#F0A0B4); the lotus buds on the back pink (#E87896); horn tip and claws gold (#F4C446); "
             "the eye orange-amber (#E89628); the light lines in the bud's seams golden yellow (#FFE26E), flat, not glowing; "
             "every outline dark-brown ink (#2B2118). Only these colours. NO purple, NO blue, NO grey stone, NO black, NO red."),
    mo=dict(
        long=("the inside of the bud is a deep wine-pink hollow (#783250) ringed by a crown of short golden stamens (#F4C446) "
              "that stand around the heart like a nest"),
        tim=("the HEART: one big round ball of pure golden energy (#FFE26E), about 140 px across, with a slightly darker gold "
             "ring (#F4C446) just inside its outline and ONE small simple spiral or seed mark in its middle, like a glowing "
             "seed of light"),
        vo_mo=("the rose-pink petals have slid apart and back along the sides of the bud like the slats of a rolling shutter: "
               "they are now stacked closely, overlapping, in a narrow band along the LEFT edge of the opening and the bottom"),
        check="Lòng nụ hoa hồng rượu, vòng **nhị vàng** quanh **quả tim tròn vàng** (có một vòng sẫm hơn và một dấu xoắn / hạt ở giữa)."),
    check=["**Thú sống lông trắng kem** (không phải cây có chân); sừng gỗ xoắn, **ngọn vàng** hình nụ; mũi nâu, tai lá nhỏ.",
           "Lưng: **lá to + tua dây leo + hoa trắng nhỏ**; hàng sống lưng xen **4 đài hoa lục nhạt** và **5 nụ sen hồng**.",
           "Ngực: **một nụ sen khổng lồ** khoảng 10 cánh hồng sẫm, **khe sáng vàng**, đài hoa lục ôm phía trước; cột cánh hồng nhạt cạnh chân trước."],
)

CHECK_CHUNG = [
    "Thú **bốn chân** to nặng, vai cao hơn mông, nhìn sang PHẢI, chỉ lộ **một mắt**, **mồm ngậm**, không đuôi.",
    "**Một sừng** lớn mọc từ sống mũi chĩa lên phía trên bên phải, ngọn khác màu.",
    "Mào đầu **bốn lá dài** quét ra sau; bờm lưng khoảng mười mảnh lớn bay về bên trái.",
    "**Bầu ngực** tròn to phía trước giữa hai chân trước, đang ĐÓNG, có khe sáng mảnh (không quầng sáng).",
    "Bốn chân trụ, mỗi bàn **bốn ngón có móng**.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, không điểm sáng, không quầng; nền trắng tinh; hình nằm ở 2/3 dưới của khung.",
]

FIX = [
    ("Vẽ thành linh vật dễ thương / chibi", "It is a huge fierce final-stage guardian beast: small head on a massive body, stern eye, no smile."),
    ("Giống rùa cóc có hoa trên lưng", "Not a toad or turtle: long pillar legs, high shoulders, a neck, a horned wedge head; the back carries a mane of many leaves, not one flower."),
    ("Thiếu chân / chân lẫn vào nhau", "All FOUR legs must be clearly visible as in image 1: near foreleg in front, near hind leg at the far left, far foreleg at the right under the pod, far hind leg between."),
    ("Có bóng, mảng sáng tối, quầng sáng", "Flat colour only: remove every shadow, highlight, shine, glow and gradient; keep the crayon hatching as texture only."),
    ("Bầu ngực mở sẵn / không thấy bầu ngực", "The chest pod is CLOSED: a big round bulge of overlapping plates on the front of the chest, with only thin bright lines in the seams."),
    ("Hình bị phóng to lấp cả khung", "Keep the size and place of image 1: the figure fills only the lower two thirds; top of the head crest at about y = 465."),
    ("Há mồm, có hai mắt, có đuôi", "Mouth closed; three-quarter profile to the right with only ONE eye; no tail."),
]

MO_STANCE = ("POSE (the same as the layout guide, image 2): the beast has REARED UP its front: the forelegs are straightened, the "
             "chest is lifted high, the neck is stretched straight up and the head is thrown back so that the muzzle points up "
             "to the right and the horn points STRAIGHT UP (tip at about x = 590, y = 235; base on the head at about x = 690, "
             "y = 530; head at about x = 560 to x = 805, y = 460 to y = 630; eye at about x = 700, y = 520). All four feet "
             "stay on the ground in the same places as in image 1. The crest blades now lie almost horizontal, streaming to "
             "the left from the back of the head (about x = 310 to x = 620, y = 480 to y = 740). The back garden and the back "
             "row are tilted more steeply (from about x = 150 to x = 600, y = 660 to y = 1270).")


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}_nghi.png"),
         "LAYOUT GUIDE, 1024x1536, white background: a flat computer-made diagram of THIS creature in its resting stance, "
         "built from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which "
         "(the horn with a differently coloured tip at the upper right; the head with one eye below it; long crest blades "
         "behind the head; the big ragged mane of the back streaming to the left; a sawtooth row of pale plates and bright "
         "pointed pieces along the spine; the brown body with shoulder and rump; the round dark pod of plates on the front of "
         "the chest with its rim; ruffs and thorns on the shoulder; four thick legs with broad feet). Use it for placement, "
         "size and overlap only; design and redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1024 × 1536, nền trắng), dáng nghỉ: các khối tô phẳng theo nhóm màu (sừng ngọn khác màu ở trên "
         "phải; đầu một mắt; mào lá dài sau đầu; bờm lưng to bay sang trái; hàng tấm nhạt xen mảnh nhọn dọc sống lưng; thân; bầu ngực "
         "tròn sẫm phía trước; bốn chân). Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (NGUOI_CAY,
         "an approved hero of the same game and the same island (a hulking swamp plant brute), 1536x1024, white background: "
         "match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold "
         "chunky shapes and its fierce battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Người cây đầm lầy đã duyệt (1536 × 1024, nền trắng): quái rêu lục vai u, nắm tay gỗ. Lấy nét bút rung, vân sáp, tô phẳng, thần "
         "thái chiến"),
        (VOI_RUNG,
         "another approved hero of the same island (a four-legged beast covered in leaves), 1536x1024, white background: the "
         "same line and flat crayon colouring; see how its big leaves and its four legs are drawn. Do NOT copy its species, "
         "design or colours.",
         "Voi rừng đã duyệt (1536 × 1024, nền trắng): thú bốn chân phủ lá. Lấy nét, tô phẳng, cách vẽ lá to và bốn chân"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


def refs_mo(kieu):
    return [
        (os.path.join(save_dir(), f"L1_{kieu}.png"),
         "THE CHARACTER (already drawn, resting stance, 1024x1536, white background): this exact creature, with exactly this "
         "design, these colours, this ink line, this crayon hatching and this flat colouring. Every piece of it must look the "
         "same in the new picture; only the pose changes and the chest pod opens.",
         "Concept dáng nghỉ của chính hướng này (1024 × 1536, nền trắng): con vật, màu, nét phải giữ y nguyên"),
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}_mo.png"),
         "LAYOUT GUIDE FOR THE NEW POSE, 1024x1536, white background: a flat computer-made diagram of the same creature reared "
         "up with the chest pod OPEN: where every piece goes, how big it is and which overlaps which (the horn pointing "
         "straight up at the top; the head thrown back under it; crest blades streaming left; the back mane tilted steeply; "
         "the tall dark opening down the front of the neck and chest with a bright round ball in its lower half; the pod's "
         "plates pushed aside into a narrow band at the left of the opening; the four legs as before). Use it for placement, "
         "size and overlap only, never for line or shapes.",
         "Sơ đồ bố cục dáng mở ngực (1024 × 1536, nền trắng): sừng dựng thẳng, đầu ngửa, khoang ngực sẫm dài phía trước có quả cầu sáng "
         "tròn ở nửa dưới, các tấm vỏ dồn thành dải hẹp bên trái khoang. Lấy chỗ đặt, cỡ, thứ tự chồng"),
    ]


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` (thú một sừng bốn chân, tướng thứ 9 đảo Mộc, suất `moc_tinh`, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3804` (thú bốn chân một sừng, 136 mảnh lưới, vỏ ngực trượt mở). Hai hướng "
          "thiết kế là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/giac_moc_ghichu.md`.", "",
          "Mỗi hướng hai ảnh: `luot_1_concept_<hướng>.txt` (dáng nghỉ, ngực đóng) rồi `luot_1b_mo_nguc_<hướng>.txt` (ngẩng cao, ngực mở, "
          "lộ quả tim; chỉ dựng khi đã có ảnh dáng nghỉ). Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              d["intro"], "", STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1024x1536 canvas (x from the left, y from the top). The viewer's LEFT "
              "side of the picture is the creature's rear; the viewer's RIGHT is where it faces. NEAR = the side of the body "
              "toward the viewer; FAR = the other side.", "",
              BODY.format(**d["parts"]), "",
              d["palette"], "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"### Lượt 1: dáng nghỉ", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", "Kiểm riêng hướng này:", ""] + [f"- {c}" for c in d["check"]] + [""]
        # lượt 1b: mở ngực (cần ảnh dáng nghỉ)
        if os.path.exists(out):
            R2 = refs_mo(kieu)
            missing = [Wp(q) for q, _, _ in R2 if not os.path.exists(q)]
            if missing:
                raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
            out2 = os.path.join(save_dir(), f"L1b_{kieu}_mo.png")
            p2 = os.path.join(pk(), f"luot_1b_mo_nguc_{kieu}.txt")
            m = d["mo"]
            t = ["IMAGES (attached in this order; open each from its path):"]
            t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R2, 1)]
            t += ["", f"SAVE: save it as a PNG to {Wp(out2)}",
                  f"If a file with that name already exists, save as L1b_{kieu}_mo_2.png, L1b_{kieu}_mo_3.png ... in the same folder. "
                  "Do not edit, move or delete any other file.", "",
                  "TASK: draw the SAME creature as image 1 (same design, same pieces, same colours, same wobbly dark-brown ink line, "
                  "same crayon hatching, same completely flat colouring) in a NEW POSE: reared up, with its chest pod OPEN and the "
                  "glowing heart inside revealed. This is the creature's ultimate move just before it fires.", "",
                  MO_STANCE, "",
                  "Follow the layout guide (image 2) for WHERE every piece is, HOW BIG it is and WHICH piece overlaps which. "
                  "Coordinates are pixels on the 1024x1536 canvas (x from the left, y from the top).", "",
                  "THE OPEN CHEST (the point of this picture):",
                  "- THE OPENING: a tall opening shaped like a long leaf or a crescent runs down the FRONT of the neck and chest, "
                  "from just under the jaw at about x = 660, y = 625 down to the bottom of the pod at about x = 640, y = 1225; it "
                  "is narrow at the top (about 40 px wide on the neck) and widest low on the chest (about 150 px wide at "
                  "y = 950 to y = 1050); its right edge is the front line of the neck and chest (from about x = 690, y = 620 "
                  "down through x = 780, y = 880 to x = 800, y = 1010). Inside, " + m["long"] + ".",
                  "- " + m["tim"] + ", sitting in the widest part of the opening with its centre at about x = 703, y = 992. It is "
                  "the brightest thing in the picture. FLAT colour: no glow, no halo, no rays, no sparkles around it (the game "
                  "adds the light itself).",
                  "- THE POD'S PLATES: " + m["vo_mo"] + " (about x = 560 to x = 690, y = 700 to y = 1180), still each a separate "
                  "closed shape; the smaller pale plates stay in their column beside the near foreleg.",
                  "- THE RIM: the rim with its small leaves and thorns stays on the FRONT edge of the neck and chest, now pulled "
                  "long and thin along the right edge of the opening, from the jaw down to the bottom.",
                  "- Everything else is the same creature as image 1, only tilted into the new pose: the shoulder ruff and thorns, "
                  "the back row, the back garden, the four legs and feet (unchanged, same places).", "",
                  "CANVAS AND FRAMING: portrait 1024x1536, pure-white background, no ground line, no cast shadow; everything visible, "
                  "nothing cut by the edges. As in the guide the figure is about 840 px wide (about x = 95 to x = 935) and about "
                  "1215 px tall (horn tip at about y = 235, feet at about y = 1450); the same scale as image 1.", "",
                  "No dust, no falling leaves, no speed lines, no energy beam, no glow, no ground, no props, no second character.", "",
                  LINE.replace("(images 2 and 3)", "(image 1)"), FLAT.replace("The only exception: one tiny light dot in the eye.",
                                                                              "The only exception: one tiny light dot in the eye. The "
                                                                              "heart is bright only because its flat colour is bright."),
                  BG]
            ghi(p2, t)
            ra.append(p2)
            gd += ["### Lượt 1b: ngẩng cao, mở ngực, lộ quả tim", "",
                   f"**Chỉ gửi GPT đường dẫn:** `{Wp(p2)}`. GPT tự lưu vào `{Wp(out2)}`.", "",
                   "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
            gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R2, 1)]
            gd += ["", "Kiểm: cùng một con với ảnh dáng nghỉ (màu, chi tiết); sừng dựng thẳng lên; khoang ngực mở dài phía trước cổ và "
                   "ngực; " + m["check"] + " Các tấm vỏ dồn sang trái khoang; không quầng sáng, không tia.", ""]
        else:
            gd += ["### Lượt 1b: mở ngực", "", f"Chưa dựng: cần `{Wp(out)}` (ảnh lượt 1 của hướng này) trước.", ""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/giac_moc_bo_cuc.py all all`).",
           "", "## Kiểm chung (dáng nghỉ)", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 1c: sửa SỪNG (người dùng 2026-11-13, đã chọn hướng A)
# "hướng A cái sừng xấu quá, làm lại để nó liên kết với phần đầu thành 1 khối hơn". Rig: xương sừng (bone66) không bao giờ cử động so
# với xương đầu (bone65) trong mọi clip → đầu + sừng của mình là MỘT mảnh cứng liền.
SUNG_1C = {
    "lien": ("sừng mọc liền từ sống mũi và gờ mày (kiểu sừng tê giác), cùng thớ gỗ với sọ, ngọn nứt lộ tinh thể hổ phách",
             "THE HORN GROWS OUT OF THE SKULL AS ONE PIECE OF WOOD, like the nasal horn of a rhinoceros: its base is very broad and "
             "covers the whole top of the muzzle, from just above the nostril back to the brow over the eye (a base about 150 px "
             "long on the head). From this broad root the SAME wood of the head sweeps upward and forward in ONE smooth curve, "
             "slightly concave at the front and convex at the back, tapering to the tip at about x = 980, y = 505. There is NO "
             "line, NO collar and NO ring where the horn meets the head: the head's outline simply continues into the horn's "
             "outline, and three or four long bark grain lines run from the cheek and brow up along the horn, following its curve. "
             "The horn is the same lighter wood as the head (#966A46) at its root and darkens to dark root brown (#543A28) in its "
             "upper half (a flat change of colour along one jagged bark edge, not a gradient). At the top the wood SPLITS open "
             "like a cracked husk into three pointed bark tongues, and out of the split grows the tip: one long sharp faceted "
             "AMBER CRYSTAL (#E8A838), about the last quarter of the horn, with two or three facet lines."),
    "mu": ("mảng trán gỗ sẫm như mũ giáp phủ từ gáy tới mũi rồi vuốt lên thành sừng, mép dưới xếch tạo gờ mày, ngọn tinh thể hổ phách",
           "THE HORN AND THE TOP OF THE HEAD ARE ONE MASS: a single thick plate of dark root wood (#543A28), like a helmet or a "
           "beetle's head shield, covers the whole top of the skull from the back of the head over the brow down to the tip of the "
           "muzzle; its lower edge is one strong slanting line that forms the angry brow just above the eye and ends in a small "
           "hooked point over the nostril. In the middle of the head this plate RISES, without any seam, collar or ring, into the "
           "horn: a broad-based, slightly curved blade-like horn sweeping forward and up to the tip at about x = 980, y = 505, its "
           "root about 150 px long on the head. Two or three long ridge lines run from the back of the plate up along the horn, "
           "following its curve, and two short backward-pointing knobs sit on the back edge of the horn like the spines of a "
           "thorn. The last quarter of the horn is one long sharp faceted AMBER CRYSTAL (#E8A838) set into the wood, the wood "
           "gripping its base with three pointed tongues. Below the dark plate the face (cheek, muzzle side, jaw) stays the "
           "lighter wood (#966A46) with the pale jaw plate (#D6BC8C), exactly as in image 1."),
}


def build_1c():
    goc = os.path.join(save_dir(), "L1_co_thu.png")
    bo = os.path.join(mau_dir(), "bo_cuc_co_thu_nghi.png")
    ra = []
    gd = ["", "## Lượt 1c: sửa SỪNG của hướng A (người dùng 2026-11-13: \"cái sừng xấu quá, làm lại để nó liên kết với phần đầu thành 1 khối hơn\")",
          "", "Vẽ lại y hệt `L1_co_thu.png`, chỉ đổi sừng và chỗ sừng nối đầu. Hai kiểu để người dùng chọn.", ""]
    for kieu, (vi, en) in SUNG_1C.items():
        out = os.path.join(save_dir(), f"L1c_sung_{kieu}.png")
        p = os.path.join(pk(), f"luot_1c_sung_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(goc)}: THE DRAFT of the creature (1024x1536, white background): an ancient tree beast of walnut-brown "
             "bark standing on four legs, facing right, with a fern-and-vine mane, pale thorn plates and amber crystals along its "
             "back, a barrel-like chest pod of dark bark plates with amber seams, and one ringed horn on its head. Everything in it "
             "is approved EXCEPT the horn.",
             f"image 2 = {Wp(bo)}: layout diagram (1024x1536, white background, rough flat blobs made by computer): use it ONLY to "
             "see where the horn's tip and the head are; do not copy its shapes or line.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1c_sung_{kieu}_2.png, L1c_sung_{kieu}_3.png ... in the same "
             "folder. Do not edit, move or delete any other file.", "",
             "TASK: redraw image 1 exactly, changing ONLY the horn and the way it joins the head. Portrait 1024x1536, pure-white "
             "background. Coordinates are pixels on this canvas (x from the left, y from the top).", "",
             "KEEP IDENTICAL (same place, same size, same shapes, same colours, same ink line and crayon hatching; if the new "
             "picture were laid over image 1 everything listed here must coincide): the whole body, the four legs and feet with "
             "their amber claws, the moss on the shoulder and elbow, the thorns, the chest pod with its dark bark plates, amber "
             "seams, pale rib plates and the green vine rim with its leaves, the neck with its pale plates, the row of pale thorn "
             "plates and amber crystals along the back, the whole fern-and-vine mane, the leaf crest behind the head, and the FACE: "
             "the eye with its amber iris and slanting brow, the muzzle, the nostril, the closed mouth with the small fang, the "
             "pale jaw plate, the small ear. The head stays at about x = 655 to x = 880, y = 675 to y = 890 and keeps its size.", "",
             "CHANGE (the only change): REMOVE the old horn completely (the stack of brown rings with pale bands that sits on the "
             "forehead like a separate cone). Draw this new horn instead:",
             en, "",
             "The new horn has the same length and direction as the old one (from the head up to the upper right, tip at about "
             "x = 980, y = 505), is clearly the biggest feature of the head, and reads at first glance as PART OF THE SKULL, not as "
             "an object placed on it. The leaf crest stays behind it. Do not add a second horn, do not open the mouth, do not "
             "change the eye.", "",
             "Leave the top of the canvas (above y = 440) empty white, as in image 1. No dust, no glow, no ground, no shadow.", "",
             LINE.replace("(images 2 and 3)", "(image 1)"), FLAT, BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"- `{kieu}`: {vi}. **Chỉ gửi GPT đường dẫn:** `{Wp(p)}` → `{Wp(out)}`."]
    gd += ["", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
           f"| 1 | `{Wp(goc)}` | Concept hướng A dáng nghỉ (1024 × 1536, nền trắng): mọi thứ đã duyệt trừ sừng |",
           f"| 2 | `{Wp(bo)}` | Sơ đồ bố cục dáng nghỉ (1024 × 1536, nền trắng): chỉ để thấy chỗ ngọn sừng và đầu |", "",
           "Kiểm: sừng và đầu là MỘT khối (không vòng, không cổ, không nét ngăn ở chân sừng); ngọn vẫn là tinh thể hổ phách; mặt, thân, "
           "bờm, bầu ngực không đổi.", ""]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1c:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: MẢNH (sau khi concept được duyệt: tai_ve/L1_duyet.png)
# Theo đúng cách tách của rig gốc (skill mục 00): bảy tờ KHUNG PART (mỗi part một ô đúng khung ảnh vùng, hình bóng kín tô phẳng) + một
# tờ THÂN LIỀN (mông, vai, cổ, bốn chân: gen liền rồi cắt bằng mã). Tờ hướng dẫn do giac_moc_manh.py dựng.
CON = ("an ANCIENT TREE BEAST: a huge four-legged forest guardian of walnut-brown bark, facing right, with one great wooden horn "
       "with an amber crystal tip growing out of its skull, a leaf crest behind the head, a wild mane of fern fronds and vines, a row "
       "of pale wooden thorn plates and amber crystals along its back, moss on its shoulders, a barrel-like chest pod of dark bark "
       "plates with amber light in the seams bound by a green vine, and thick legs with dark root feet and amber claws")
LOAI = {
    "la": "a big FERN FROND or jungle LEAF, deep fern green (#3E7846): one pale-green midrib line along its length and a few side veins",
    "la_nhat": "a tuft of young LEAVES, light leaf green (#82B050), each leaf with a midrib line",
    "day": "a long thin VINE TENDRIL, vine green (#5A8C3C), plain, with one thin darker line along it",
    "tinh_the": "a raw AMBER CRYSTAL shard (#E8A838) with two or three thin facet lines",
    "gai": "a pale WOODEN plate (#DAC496) with two or three thin wood-grain lines",
    "vo": "a dark BARK PLATE (#5C402C) with one or two short bark lines; the thin bright amber-yellow band (#FFD650) along ONE edge "
          "stays exactly where the guide shows it, separated from the bark by a thin ink line",
    "vo_toi": "a piece of dark BARK wall (#5C402C) with a few long bark lines",
    "vo_nhat": "a pale WOODEN rib plate (#DAC496) with one or two wood-grain lines",
    "cua": "a short dark root-wood THORN (#543A28) with one grain line",
    "vanh": "a segment of thick green VINE (#3E7846) with one lighter vein line along it",
    "khe": "one small pointed LEAF, light leaf green (#82B050), with a midrib line",
    "reu": "a tuft of MOSS (#6E963E): scalloped, lumpy edge exactly as the guide, with a few small curved tuft marks inside",
    "dau": "a piece of the head's WOOD (#966A46) with one bark crack",
    "long": "the HOLLOW inside the chest: very dark brown (#462C24) with three pale ROOT strands (#D6BC8C) running down it where the "
            "guide shows the pale lines; make them real little roots that fork once or twice and taper",
    "tim": "THE HEART: a round ball of amber-yellow energy (#FFD650) with a darker amber ring (#E8A838) just inside its outline and "
           "one small spiral mark in the middle, exactly as the guide; flat colour, no glow, no rays",
    "ban_chan": "a TOE of dark root wood (#543A28) ending in one big blunt AMBER CLAW (#E8A838) exactly where the guide shows amber, "
                "with an ink line between toe and claw",
    "cua_got": "a small dark root-wood heel SPUR (#543A28)",
}
TEN_TO = {"A": "sáu mảng dương xỉ / lá to của bờm lưng", "B": "năm dải lá dài + sợi dây leo + hai túm lá sau đầu",
          "C": "mào đầu (sáu mảnh lá), năm tinh thể hổ phách, năm tấm gai gỗ", "D": "mười tấm vỏ ngực, tám tấm sườn gỗ nhạt, ba gai",
          "E": "chín đoạn dây leo vành ngực, tám lá nhỏ, mảng rêu nhỏ, ba tấm đốt cổ, mẩu gỗ gáy",
          "F": "lòng ngực, quả tim, ba dải vách xa của bầu ngực, mảng rêu gốc cổ", "G": "mười sáu ngón chân có móng, sáu gai gót",
          "H": "bảy túm rêu ở chân và vai, ba gai vai"}


def loai_o(M, ten):
    if ten == "tim":
        return "tim"
    if ten.startswith("B_bozi_E_1"):
        return "vo_toi"
    if ten.startswith("T") and "_3_" in ten:
        return "ban_chan"
    if ten.startswith("T"):
        return "cua_got"
    v = M.vai(ten)
    return {"ban_chan": "cua_got"}.get(v, v)


def build_manh():
    import json
    sys.path.insert(0, HERE)
    import giac_moc_manh as M
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có " + duyet)
    ra = []
    gd = ["", "## Lượt 2: MẢNH theo khung part của rig (sau khi duyệt concept)", "",
          "Mỗi tờ: ảnh 1 = concept đã duyệt (lấy nét, màu, vân sáp), ảnh 2 = tờ hướng dẫn tự dựng (mỗi part của rig một ô đúng khung, hình "
          "bóng kín tô phẳng). GPT vẽ lại sạch, GIỮ NGUYÊN hình bóng. Claude cắt bằng `giac_moc_manh.py cat_part <tờ>`, đo IoU.", ""]
    for to in M.TO:
        pj = os.path.join(mau_dir(), f"part_{to}.json")
        if not os.path.exists(pj):
            raise SystemExit("chưa có tờ hướng dẫn " + pj)
        Kh = json.load(open(pj, encoding="utf-8"))
        z = next(iter(Kh.values()))["z"]
        net_px = max(4, int(round(M.NET * z)))
        g_im = os.path.join(mau_dir(), f"part_{to}.png")
        out = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_2_manh_{to}.txt")
        nh = {}
        for ten, v in sorted(Kh.items(), key=lambda q: (q[1]["y"] // 120, q[1]["x"])):
            nh.setdefault(loai_o(M, ten), []).append(f"({v['x'] + v['w'] // 2}, {v['y'] + v['h'] // 2})")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, 1024x1536, white background: {CON}. It gives the design, the colours, "
             "the wobbly dark-brown ink line, the crayon hatching and the look of every material.",
             f"image 2 = {Wp(g_im)}: PARTS GUIDE, 1536x1024, white background, drawn by computer: {len(Kh)} separate flat shapes, each "
             "one a PART of the creature's 2D animation rig, enlarged, lying at the angle the rig needs. Each shape is the EXACT "
             "silhouette of its part, filled with the flat colour of its material and outlined in dark brown.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.", "",
             "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep "
             "EXACTLY every silhouette of image 2: the same outline, the same size, the same angle, the same position on the sheet "
             "(if your picture were laid over image 2, every shape must coincide with its shape there). Do not move, rotate, "
             "straighten, merge or rearrange the shapes; do not add or drop any; keep clear white between them. A program will cut "
             "this sheet by position.", "",
             "WHAT THE SHAPES ARE (centre of each shape in pixels on the sheet, x from the left, y from the top):"]
        for loai, cho in nh.items():
            t.append(f"- {LOAI[loai]}: {len(cho)} shape{'s' if len(cho) > 1 else ''}, centred at about " + ", ".join(cho) + ".")
        t += ["",
              f"OUTLINE: every shape gets ONE closed dark-brown ink outline (#2B2118), about {net_px} px thick on this sheet, wobbly like "
              "a real pen, lying just INSIDE the edge of the silhouette (never outside it). Inner detail lines are thinner (about "
              f"{max(2, net_px // 2)} px).",
              "COLOUR: keep the colour each shape has in image 2 (and keep every second colour exactly where image 2 shows it). Fill "
              "with visible loose diagonal crayon / coloured-pencil hatching as in image 1, kept inside the outline.",
              "Each shape is a complete, closed object on its own: do not draw neighbouring parts, do not draw the creature.", "",
              "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
              "darker side, no highlights or shine spots (not on the crystals, not on the claws), no glow, no gradients, no cast "
              "shadows, no 3D look. Pure white (#FFFFFF) background; no text, no labels, no numbers, no frames, no guide lines."]
        ghi(p, t)
        ra.append(p)
        gd += [f"- Tờ `{to}` ({TEN_TO[to]}; phóng {z} lần, nét ~{net_px} px): **chỉ gửi GPT đường dẫn** `{Wp(p)}` → `{Wp(out)}`; ảnh 2 = "
               f"`{Wp(g_im)}` (1536 × 1024, nền trắng, {len(Kh)} ô)."]
    # tờ thân liền
    g_im = os.path.join(mau_dir(), "lien.png")
    out = os.path.join(save_dir(), "N_lien.png")
    p = os.path.join(pk(), "luot_2_than_lien.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED creature, 1024x1536, white background: {CON}. It gives the design, the colours, the ink "
         "line, the crayon hatching and the look of its bark hide and root feet.",
         f"image 2 = {Wp(g_im)}: BODY GUIDE, 1536x1024, white background, drawn by computer: in the middle ONE big flat silhouette = "
         "the creature's bark BODY WITHOUT its head and without any decoration: the neck (top right, ending in a rounded stump where "
         "the head sits), the shoulder mass, the sloping back, the rump and the two NEAR legs (near hind leg at the left, near "
         "foreleg at the right), all fused into one shape; at the far left ONE separate leg = the far hind leg, at the far right ONE "
         "separate leg = the far foreleg, each complete from its top to its foot. Brown = bark hide, dark brown = the root-wood "
         "feet. It gives the exact silhouettes, sizes and positions.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY "
         "every silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, "
         "the shapes must coincide). This sheet will be cut by a program into the body parts of a 2D animation rig.", "",
         "VERY IMPORTANT, ONE CONTINUOUS SURFACE: the big shape in the middle is ONE piece of bark hide. Draw the dark-brown ink "
         "outline ONLY around the OUTSIDE of each silhouette. INSIDE a silhouette draw NO outline lines at all: no line where a leg "
         "joins the body, no line between the neck and the body, no line between the upper and lower leg, no folds, no creases, no "
         "knee rings. The bark colour and the crayon hatching run across the whole shape without any break.", "",
         "- BARK HIDE: walnut brown (#7A5438) with loose diagonal crayon hatching and a FEW long, calm, thin bark grain lines "
         "(thin darker pencil-like lines, much thinner than the outline) that flow along the length of the neck, along the back and "
         "down each leg, as on image 1; one small spiral knot on the rump. Keep the grain sparse: large calm areas of plain "
         "hatched bark.",
         "- FEET: the lower end of every leg is a broad foot of dark root wood (#543A28), exactly where image 2 shows dark brown, "
         "with ONE ink line between the bark and the foot. Do NOT draw toes or claws (they are separate parts): each foot is a "
         "plain rounded dark block.",
         "- OUTLINE: dark-brown ink (#2B2118), about 6 px thick on this canvas, wobbly like a real pen, closed around each "
         "silhouette and lying just INSIDE its edge.",
         "- The two separate legs at the sides: drawn the same way (bark, dark foot), each with its own closed outline.",
         "Draw nothing else: no head, no horn, no leaves, no moss, no crystals, no chest pod, no thorns, no ground.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
         "darker side, no highlights, no gradients, no cast shadows. Pure white (#FFFFFF) background; no text, no labels, no frames, "
         "no guide lines."]
    ghi(p, t)
    ra.append(p)
    gd += [f"- Tờ **thân liền** (mông, vai, cổ, bốn chân gen LIỀN rồi cắt bằng mã): `{Wp(p)}` → `{Wp(out)}`; ảnh 2 = `{Wp(g_im)}` "
           "(1536 × 1024, nền trắng: ở giữa một hình bóng nâu liền thân + cổ + hai chân gần, hai bên là hai chân xa; bàn chân nâu sẫm).",
           "", "Kiểm: hình bóng trùng tờ hướng dẫn (IoU ≥ 0,9 mới lắp); tờ thân liền KHÔNG có nét mực nào bên trong; tô phẳng; nền trắng.", ""]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


def build_dau():
    """tờ "đúng chỗ, đúng cỡ": ĐẦU LIỀN SỪNG (một mảnh cứng của mình trên xương đầu; rig gốc: xương sừng không cử động so với đầu)."""
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    out = os.path.join(save_dir(), "M_dau.png")
    p = os.path.join(pk(), "luot_2_dau_sung.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED creature, 1024x1536, white background: {CON}.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as M_dau_2.png, M_dau_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 1 with ONLY the creature's HEAD TOGETHER WITH ITS HORN (they are one single piece), in exactly the SAME "
         "POSITION and at exactly the SAME SIZE as in image 1 (portrait 1024x1536; if the new picture were laid over image 1, the "
         "head and horn must coincide with image 1). REMOVE everything else and leave pure white (#FFFFFF) there: no neck, no neck "
         "plates, no leaf crest, no leaves, no mane, no body, no vine.", "",
         "KEEP (one piece, about x = 640 to x = 995, y = 500 to y = 895): the whole head with the dark helmet-like brow plate that "
         "rises into the great horn, the horn with its ridge lines, its backward knobs and its amber crystal tip, the eye with the "
         "amber iris, the lighter cheek and muzzle, the nostril, the closed mouth with the small fang, the pale jaw plate, the "
         "small pointed ear.", "",
         "COMPLETE IT INTO ONE CLOSED SHAPE with the dark-brown ink outline running all the way around: in image 1 the back of the "
         "head is partly hidden behind the leaf crest and the bottom of the head sits on the neck. Draw those hidden parts: the "
         "back of the skull is a simple rounded shape (the dark brow plate continues around the back of the head, the lighter "
         "cheek below it), and the underside of the jaw and the back of the cheek close in one smooth rounded line where the neck "
         "used to be. Do not change anything that is visible in image 1.", "",
         "Same wobbly ink line, same line thickness, same colours, same crayon hatching, same completely flat colouring as image 1. "
         "Do not add anything: no shadows, no glow, no dust, no labels.", "",
         FLAT, BG]
    ghi(p, t)
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2 (đầu):")[0].rstrip("\n")
    gdm = ["", "## Lượt 2 (đầu): ĐẦU LIỀN SỪNG \"đúng chỗ, đúng cỡ\"", "",
           f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}` → `{Wp(out)}`. Ảnh mẫu 1 = `{Wp(duyet)}` (concept đã duyệt, 1024 × 1536, nền trắng).",
           "Kiểm: chỉ còn đầu + sừng, đúng chỗ và cỡ như concept, viền kín (gáy và dưới hàm vẽ bù tròn), nền trắng.", ""]
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gdm) + "\n")
    print(p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dau":
        build_dau()
    elif len(sys.argv) > 1 and sys.argv[1] == "manh":
        build_manh()
    elif len(sys.argv) > 1 and sys.argv[1] == "1c":
        build_1c()
    else:
        main()
