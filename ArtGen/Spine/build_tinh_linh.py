# -*- coding: utf-8 -*-
"""Gói GPT vẽ tinh linh rừng mập (mã làm việc tinh_linh, con gốc của rig: monster_3407). Tướng thứ 2 đảo Mộc, DẠNG 1.

Người dùng (2026-11-12): "concept tinh linh rừng chubby cute như hình, hơi trong suốt nhẹ; tạo hình chubby giống với hình, phần tóc trên
đầu có thể thay đổi tuỳ bạn". Bản đầu (thạch lục + vòng lá + hai nụ + mầm cây trong bụng, mắt có con ngươi, mồm chữ w) bị trả:
"nhìn giống con gốc quá", "mắt làm chỉ lòng trắng thôi", "miệng gen thêm chỉ bật khi bắn chiêu, miệng cũng hình tròn tròn thôi, xem tướng
1 đảo thủy" (Tí Tách: mắt bầu dục trống, vành dày màu thân đậm; lúc nghỉ không có mồm).
Lượt 2: BA hướng thiết kế cho người dùng chọn (màu, tóc, thứ trong bụng đều là ĐỀ XUẤT của Claude). Giữ của con gốc chỉ dáng mập và
chỗ đặt thân, tay, mắt (để lắp lưới); tóc và thứ trong bụng là mảnh riêng của mình, tả bằng lời.
Không đính ảnh con gốc vào prompt; đính sơ đồ bố cục tự dựng bằng mã (tinh_linh.py bo_cuc).

    py -3 -I ArtGen/Spine/tinh_linh.py bo_cuc
    py -3 -I ArtGen/Spine/build_tinh_linh.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tinh_linh_1/luot_1_concept_<kiểu>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tinh_linh"
K = int(os.environ.get("TL_DANG", "2"))        # dạng: TL_DANG=1 (hạt mầm, làm sau) | 2 (mầm hai lá, đã duyệt; ba hướng của lượt chọn)
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DROP = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")
WHALE = os.path.join(HERE, "inbox", "ca_voi_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


# mỗi hướng: tên Việt, loài, màu thân / nét trong thân / vành mắt / má, bảng màu tóc, tả TÓC, tả thứ TRONG BỤNG, câu cấm riêng
KIEU = {
    "mam": dict(
        vi="mầm hai lá (thạch matcha non, hạt giống nảy mầm trong bụng)",
        loai="a SEED SPIRIT: a jelly dumpling that has grown around a sprouting seed",
        than="pale MATCHA LIME (#C8DE8E)", nep="olive green (#7FA050)", vanh="leaf green (#628C3E)", ma="soft peach pink (#F0AA96)",
        mau_them="the two big leaves on the head deep LEAF GREEN (#3E8C58) with a thin lighter-green centre vein; the short stem and "
                 "the small ruff of leaflets fresh yellow-green (#9CCC5C); the seed inside the belly warm nut BROWN (#B98552) with a "
                 "cream root (#F4EAD0)",
        toc="- SPROUT ON THE HEAD (the creature's \"hair\", the main feature of its silhouette): from the centre of the top of the "
            "head, at about x = 790, y = 310, grows ONE short thick stem about 45 px wide and 70 px tall that opens into TWO very "
            "BIG, fat, rounded seedling leaves (like the first two leaves of a bean sprout) spread in a wide V: the LEFT leaf is the "
            "bigger one, about 300 px long and 170 px wide, leaning out to the upper left and drooping a little at its rounded tip "
            "(tip at about x = 520, y = 190); the RIGHT leaf is a bit smaller, about 250 px long, standing up to the upper right "
            "(tip at about x = 1010, y = 120). Each leaf is a plump smooth oval with one centre vein, no side veins. Around the base "
            "of the stem, lying flat on the head like a small collar, a ruff of four or five tiny yellow-green leaflets (the whole "
            "ruff about 200 px wide). Nothing else on the head: NO flowers, NO buds, NO balls, NO vines, NO tuft of many leaves.",
        trong="- SEED INSIDE THE BELLY (this is what shows that the body is translucent): low in the middle of the belly, at about "
              "x = 790, y = 800, floats ONE plump bean-shaped SEED about 110 px long, split open at the top, with a short curled "
              "cream root coming out below and a tiny two-leaf shoot coming out above (the whole thing about 110 px wide and 170 px "
              "tall). Around it three small round bubbles of different sizes (20 to 40 px). All of it is seen THROUGH the jelly: "
              "paler and washed out, with thin olive-green pencil outlines instead of dark ink. It does not touch the outline of "
              "the belly.",
        cam="NO teal, NO blue, NO red, NO orange, NO purple."),
    "nam": dict(
        vi="mũ nấm (thạch kem đào, bào tử trôi trong bụng)",
        loai="a MUSHROOM SPIRIT: a soft jelly dumpling wearing a big mushroom cap",
        than="creamy PEACH (#F6D9B8)", nep="warm tan (#BE8C60)", vanh="chestnut tan (#B07A4E)", ma="soft rose pink (#F09690)",
        mau_them="the mushroom cap brick RED-BROWN (#C5563F) with round cream spots (#FBF1DC); the frilly gill ruffle under the "
                 "cap edge cream (#FBF1DC) with thin tan lines; the two tiny leaves on the cap moss green (#6FA85A); the spores "
                 "inside the belly pale cream",
        toc="- MUSHROOM CAP (the creature's \"hair\", the main feature of its silhouette): one BIG round mushroom cap sits on the "
            "head like a hat that is a little too large: a fat dome about 520 px wide and 230 px tall, from about x = 530 to "
            "x = 1050, its top at about y = 120 and its lower rim at about y = 350, tilted slightly so the left side hangs a bit "
            "lower. The cap is brick red-brown with five or six round cream spots of different sizes. Under the rim, all along "
            "it, shows a narrow wavy cream ruffle of gills (about 30 px) lying on the head. On top of the cap, a little right of "
            "the centre, ONE tiny baby mushroom about 80 px tall with the same red-brown cap, and beside it two tiny moss-green "
            "leaves. The cap covers the top of the head down to just above the eyes. NO leaves crown, NO flowers, NO vines.",
        trong="- SPORES INSIDE THE BELLY (this is what shows that the body is translucent): in the lower half of the belly drift "
              "six or seven small round spores of different sizes (15 to 45 px), loosely scattered from about x = 660 to x = 930 "
              "and y = 690 to y = 880, and among them ONE tiny mushroom about 70 px tall floating upright. All of it is seen THROUGH "
              "the jelly: pale, washed out, with thin tan pencil outlines instead of dark ink. Nothing touches the outline of the "
              "belly.",
        cam="NO green body, NO teal, NO blue, NO purple, NO yellow."),
    "ho_phach": dict(
        vi="nhựa cây hổ phách (thạch mật ong, lá kẹt trong bụng, mũ rêu và hai cành non)",
        loai="a TREE-SAP SPIRIT: a fat drop of golden tree resin (amber) that came alive",
        than="warm HONEY AMBER (#EDB85A)", nep="dark honey (#B9802E)", vanh="brown amber (#A06824)", ma="soft coral (#E88260)",
        mau_them="the moss cap on the head MOSS GREEN (#6FA85A); the two little twigs bark brown (#8A5A3C); the leaves on the twigs "
                 "and the leaf inside the belly deep leaf green (#3E8C58)",
        toc="- MOSS CAP AND TWO TWIGS (the creature's \"hair\", the main feature of its silhouette): the top of the head is covered "
            "by a low, soft, round cushion of MOSS, like a small beret, about 380 px wide and 110 px tall (from about x = 600 to "
            "x = 980, y = 245 to y = 355), its lower edge a row of small rounded scallops lying on the head. Out of the moss stand "
            "TWO short forked TWIGS like the tiny antlers of a fawn: the LEFT twig leans to the upper left, about 190 px tall, with "
            "one fork (tips at about x = 600, y = 110 and x = 690, y = 130); the RIGHT twig leans to the upper right, about 170 px "
            "tall, with one fork (tips at about x = 900, y = 120 and x = 990, y = 160). Each twig is a plain brown stick about "
            "22 px thick with ONE small pointed green leaf at one of its tips. NO tuft of many leaves, NO flowers, NO balls, NO vines.",
        trong="- LEAF TRAPPED INSIDE THE BELLY, like an insect in amber (this is what shows that the body is translucent): in the "
              "lower middle of the belly, at about x = 790, y = 790, floats ONE pointed green LEAF about 170 px long, tilted about "
              "30 degrees, with a centre vein and a few side veins, and around it four small round bubbles of different sizes (15 "
              "to 40 px). All of it is seen THROUGH the amber: the leaf darker and muted (olive), with thin dark-honey pencil "
              "outlines instead of dark ink. Nothing touches the outline of the belly.",
        cam="NO green body, NO teal, NO blue, NO purple, NO pink body."),
}


# DẠNG 1 (người dùng 2026-11-12: "làm dạng 1 đi, con này là dạng 2"; không tả gì thêm: thiết kế là ĐỀ XUẤT của Claude): cùng thân, cùng mắt
# với dạng 2 nhưng NON hơn: hạt chưa nứt trong bụng, trên đầu mới nhú một mầm cong tí hon, thân nhạt màu hơn
KIEU_1 = {
    "hat": dict(
        vi="dạng 1: hạt mầm (thân lục nhạt, hạt chưa nứt trong bụng, một mầm cong tí hon trên đầu)",
        loai="a SEED SPIRIT, the BABY form: a jelly dumpling that has grown around a seed which has NOT sprouted yet. Image 2 shows "
             "this same creature AFTER it evolves; this younger form has the same body and the same eyes but is simpler and "
             "paler, with only one tiny curled shoot on its head instead of two big leaves",
        than="very pale YELLOW-LIME (#E0EA96)", nep="soft olive (#96AC54)", vanh="leaf green (#688C3E)", ma="soft peach pink (#F2AC96)",
        mau_them="the tiny shoot on the head fresh YELLOW-GREEN (#9CCC5C), its one small folded leaf a slightly deeper fresh green "
                 "(#6FB45A); the seed inside the belly warm nut BROWN (#B98552)",
        toc="- ONE TINY SHOOT ON THE HEAD (the creature's only \"hair\"): from the centre of the top of the head, at about x = 790, "
            "y = 300, grows ONE short, plump shoot about 34 px thick and about 130 px tall that leans a little to the right and "
            "CURLS over at its tip like a small hook or a fiddlehead (the tip at about x = 850, y = 180). At the curled tip sits "
            "ONE small leaf that is still half folded, a little plump teardrop about 70 px long pointing down-right, with one "
            "centre line. The whole shoot fits in a box of about 130 x 150 px, from about x = 760 to x = 890 and y = 165 to "
            "y = 315. It has a closed ink outline. Nothing else on the head: NO big leaves, NO second leaf, NO ruff of "
            "leaflets, NO flowers, NO buds, NO balls.",
        trong="- SEED INSIDE THE BELLY (this is what shows that the body is translucent): in the lower middle of the belly, at about "
              "x = 790, y = 790, floats ONE plump, WHOLE, closed bean-shaped SEED about 120 px wide and 100 px tall, not split, "
              "with one short curved line on it (the seam) and a tiny cream root tip just peeking out at the bottom (about 20 px). "
              "Beside it two small round bubbles (about 25 and 40 px). All of it is seen THROUGH the jelly: paler and washed "
              "out, with thin olive-green pencil outlines instead of dark ink. It does not touch the outline of the belly.",
        cam="NO deep green body, NO teal, NO blue, NO red, NO orange, NO purple."),
}


# DẠNG 3 (người dùng 2026-11-12: "làm thêm dạng 3 cũng được"; không tả: thiết kế là ĐỀ XUẤT của Claude): hạt → mầm hai lá → NỞ HOA.
# Cùng thân, cùng mắt; thân lục đậm hơn, trên đầu một bông hoa to nở giữa hai lá lớn, trong bụng hạt đã thành quả
KIEU_3 = {
    "hoa": dict(
        vi="dạng 3: nở hoa (thân lục đậm hơn, một bông hoa san hô to nở giữa hai lá lớn, quả chín trong bụng)",
        loai="a SEED SPIRIT in its FINAL, fully grown form: the jelly dumpling whose sprout has now BLOOMED. Image 2 shows this "
             "same creature in its EARLIER form; this grown form has the same body and the same eyes, but a deeper green body, "
             "ONE BIG open flower on its head between two large leaves, and a ripe fruit inside its belly. Still chubby and "
             "cute, but prouder and more confident",
        than="fresh LEAF-JADE green (#9CCB6A), clearly deeper than in image 2", nep="deep olive green (#5F8F3E)",
        vanh="dark leaf green (#3A702C)", ma="soft coral pink (#F0A08C)",
        mau_them="the two big leaves deep LEAF GREEN (#35804E) with a thin lighter centre vein; the stem and the ruff of leaflets "
                 "fresh yellow-green (#9CCC5C); the five flower petals warm CORAL PINK (#F08A7C); the round centre of the "
                 "flower golden yellow (#F2C24A); the fruit inside the belly the same coral pink, paler",
        toc="- FLOWER CROWN (the creature's \"hair\", the main feature of its silhouette): from the centre of the top of the head, at "
            "about x = 790, y = 305, rises ONE short thick stem (about 44 px wide, 70 px tall) that carries ONE BIG OPEN FLOWER, "
            "turned toward the viewer: five broad, rounded petals in coral pink around one round golden-yellow centre, the whole "
            "flower about 240 px across, centred at about x = 795, y = 165 (its top petal reaches about y = 55). Each petal has "
            "its own closed ink outline and one short centre line. Under the flower, one LARGE plump leaf grows out of the stem "
            "on each side, like the leaves of image 2: the LEFT leaf about 270 px long, spreading left and drooping a little, "
            "its rounded tip at about x = 505, y = 270; the RIGHT leaf about 240 px long, spreading right and slightly up, its "
            "tip at about x = 1050, y = 215. Each leaf is a smooth plump oval with one centre vein. Around the base of the "
            "stem, a small ruff of four or five tiny yellow-green leaflets lying on the head. Exactly ONE flower and TWO big "
            "leaves: NO buds, NO second flower, NO vines, NO fruit on the head.",
        trong="- FRUIT INSIDE THE BELLY (this is what shows that the body is translucent): in the lower middle of the belly, at about "
              "x = 790, y = 790, floats ONE round, plump FRUIT about 130 px across, like a small peach, with a tiny stem and "
              "one tiny leaf on top. Around it three small round bubbles of different sizes (20 to 40 px). All of it is seen "
              "THROUGH the jelly: paler and washed out, with thin deep-olive pencil outlines instead of dark ink. It does not "
              "touch the outline of the belly.",
        cam="NO blue, NO teal, NO purple, NO red, NO orange body."),
}


def form(c):
    return ("CREATURE: a chubby little FOREST SPIRIT of the plant element for a monster-collecting game, first evolution stage: "
            + c["loai"] + ". A soft, round, very fat blob of slightly TRANSLUCENT jelly, like a big mochi sitting on the ground. Very "
            "cute and squishy, small and compact (a little chibi), calm and a little dopey, with blank white eyes. Simple, with "
            "few details. It has NO mouth, NO nose, NO legs, NO feet, NO tail, NO ears, NO hands or fingers, NO clothes.\n"
            "Follow the LAYOUT GUIDE (image 1) closely for the body, the two arms and the eyes: their construction, placement, "
            "size and overlap order. The guide does NOT show the things on the head or inside the belly: draw those from the "
            "description below.\n"
            "- VIEW: three-quarter front view; the creature is turned slightly toward the viewer's RIGHT, sitting on the ground.\n"
            "- BELLY: one huge, wide, sagging round belly like a fat pear or a full water balloon resting on the ground, about "
            "600 px wide and 455 px tall, from about x = 485 to x = 1084 and y = 462 to y = 918; the bottom is flattened where it "
            "sits (a gentle wobbly line at about y = 915, with one small dent in the middle), the sides bulge out.\n"
            "- HEAD: a smaller, wide, rounded dome sitting directly on the belly with NO neck, about 450 px wide, from about "
            "x = 568 to x = 1016, its top at about y = 290. The head and the belly are ONE continuous jelly mass with one ink "
            "outline around both together: where the head meets the belly there is only a short soft fold line at each side (a "
            "chubby neck crease, at about y = 520 on the left and y = 590 on the right), NO line across the middle.\n"
            "- FRONT ARM (at the viewer's left, IN FRONT of the body): one short, fat, soft flipper arm with a rounded tip and NO "
            "hand, shaped like a plump bean, about 200 px wide and 270 px long, hanging from the left shoulder at about x = 560, "
            "y = 510 down and out to the left, its tip at about x = 470, y = 770. It has its own closed ink outline and overlaps "
            "the left side of the belly.\n"
            "- BACK ARM (at the viewer's right, BEHIND the body): the same kind of flipper arm, mostly hidden behind the belly; "
            "only a narrow curved sliver about 25 px wide shows along the right edge of the belly, from about x = 1040, y = 590 "
            "down to about x = 1100, y = 775.\n"
            "- EYES: two big, simple, completely BLANK oval eyes low on the head, exactly as in the guide and like the eyes of the "
            "water-drop hero in " + ("image 3" if K in (1, 3) else "image 2") + ": the LEFT eye (nearer to the viewer) is a wide oval about 128 px wide and 104 px tall "
            "centred at about x = 804, y = 490; the RIGHT eye sits at the right edge of the face and is narrower because the head "
            "is turned: about 56 px wide and 88 px tall, centred at about x = 981, y = 494. Each eye is plain pure WHITE inside "
            "with one thick rim about 9 px wide in " + c["vanh"] + " (a coloured rim, not black ink). NO pupils, NO iris, NO "
            "shine dots, NO eyelashes, NO eyebrows.\n"
            "- CHEEKS: one flat oval blush mark under each eye (the right one half hidden by the edge of the face). There is NO "
            "mouth at all: the face is only the two blank eyes and the two blush marks.\n"
            + c["toc"] + "\n" + c["trong"] + "\n"
            "- Exactly one head-and-belly body, two flipper arms, two blank eyes, two blush marks, the head decoration described "
            "above and the things inside the belly described above. Nothing else.")


def palette(c):
    return ("COLOURS, a calm, soft, slightly muted palette (use exactly these, each area one flat colour): the whole jelly body "
            "(head, belly, both arms) " + c["than"] + "; the few soft fold lines on the body and every outline of the things INSIDE "
            "the belly " + c["nep"] + ", drawn as thin pencil lines, not ink; the eyes pure white with a thick " + c["vanh"]
            + " rim; the two blush marks " + c["ma"] + "; " + c["mau_them"] + "; every ink outline dark brown (#2B2118). Only these "
            "colours. " + c["cam"] + " NO white shine.")


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. The body is placed exactly as in the guide (from about x = 430 to x = 1103, the bottom of the "
         "belly at about y = 918); the decoration on the head reaches up to about y = 100, never higher than y = 60.")

POSE = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): sitting still in "
        "a calm, clean resting pose, exactly as in the guide. The front arm and every separate piece on the head are clearly "
        "separated by their own closed ink outline. No dust, no sparkles, no floating leaves or petals outside the body, no motion "
        "lines, no sweat drops, no ground, no grass, no props.")

JELLY = ("TRANSLUCENT JELLY, DRAWN FLAT: the body is soft translucent jelly, but this is a flat hand-drawn picture, so do NOT "
         "paint glass, water or gloss. The translucency is shown ONLY by the pale things visible inside the belly. The jelly "
         "itself is one even colour with crayon hatching: NO white shine marks, NO reflection windows, NO glossy highlights, NO "
         "darker rim, NO gradients, NO see-through background.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The "
        "layout guide is a stiff flat computer diagram with rough, jagged edges and empty flat fills: take the construction, the "
        "placement, the proportions and the overlaps from it, never its mechanical line or its jagged edge noise. Redraw every "
        "shape cleanly, rounded and with character: the body fat, soft and squishy.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown ink "
        "pen (#2B2118), an outline about 6 px thick on this canvas for the body, the arms and the big pieces on the head and "
        "about 4 px for small details; the fold lines and everything inside the belly are thin pencil lines about 3 px in the "
        "darker body tone, not ink; the eye rims are thick coloured rims, not ink; every area coloured with coloured pencils and "
        "wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the "
        "outline. Clean and appealing, neither a crude scribble nor overly detailed.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside of the belly, no lighter patches or blotches, no shadows of any kind "
        "(no cast shadow, no shadow under the head, under the arm, under the head decoration, on the ground or on the "
        "background), no white highlights or shine spots anywhere (the eyes are plain white, without any dot), no gloss, no "
        "reflections, no glow, no rim light, no gradients, no 3D look. A different tone appears only where the design itself "
        "lists a different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def refs(kieu):
    R = [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of the BODY of this creature: the fat belly with "
         "the smaller head dome on top, the bean-shaped front arm at the left, the sliver of the back arm at the right edge, the "
         "two blank white oval eyes with their coloured rims, the two blush marks. Follow it closely for these parts (placement, "
         "size, overlap, colours). It does not show the decoration on the head or the things inside the belly: add those from "
         "the text. Redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): khối thân mập (bụng to, đầu vòm nhỏ hơn), tay trước hình hạt đậu bên "
         "trái, hai mắt bầu dục trắng trơn có vành màu, má hồng. Không có tóc, không có thứ trong bụng (tả bằng lời)"),
        (DROP,
         "an approved hero of the same game (a little water-drop blob, first evolution stage), 1536x1024, white background: match "
         "EXACTLY its wobbly pen line, its visible crayon hatching, its completely flat colouring, and above all the way its EYES "
         "are drawn: blank ovals with a thick coloured rim, no pupils, no mouth. Do NOT copy its shape, its bubbles or its blue "
         "colours.",
         "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam, mắt bầu dục trống vành lam dày, má lam, không mồm. Lấy nét, "
         "vân sáp, tô phẳng và CÁCH VẼ MẮT"),
        (WHALE,
         "another approved hero of the same game (a little whale monster), 1536x1024, white background: the same line and flat "
         "crayon colouring, the same calm muted colours. Do NOT copy its species, design or colours.",
         "Cá voi biến dị dạng 1 đã duyệt (1536 × 1024, nền trắng): cá voi lam nhỏ. Lấy nét, tô phẳng, tông màu trầm"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if K == 3:
        R.insert(1, (os.path.join(HERE, "inbox", f"{CODE}_2", "tai_ve", "L1_duyet.png"),
                     "the approved picture of this SAME creature in its EARLIER form (two big seedling leaves on the head, a "
                     "sprouting seed inside the belly), 1536x1024, white background: the picture you draw is its FINAL, grown "
                     "form. Keep EXACTLY the same body shape, the same placement, the same blank white eyes with a green rim, the "
                     "same blush marks, the same wobbly ink line and crayon hatching, and the same kind of big plump leaves. "
                     "Change only what the text says: a deeper green body, one big open flower on the head between the two "
                     "leaves, a ripe fruit inside the belly.",
                     "Concept dạng 2 đã duyệt (mầm hai lá; 1536 × 1024, nền trắng): cùng thân, cùng mắt, cùng nét, cùng kiểu lá. Dạng 3 là bản lớn"))
    if K == 1:
        R.insert(1, (os.path.join(HERE, "inbox", f"{CODE}_2", "tai_ve", "L1_duyet.png"),
                     "the approved picture of this SAME creature in its LATER, evolved form (two big seedling leaves on the head, a "
                     "sprouting seed inside the belly), 1536x1024, white background: the picture you draw is its YOUNGER form. Keep "
                     "EXACTLY the same body shape, the same placement, the same blank white eyes with a green rim, the same blush "
                     "marks, the same wobbly ink line and crayon hatching. Change only what the text says: a paler body, one tiny "
                     "curled shoot instead of the two big leaves and the ruff, a whole unopened seed inside.",
                     "Concept dạng 2 đã duyệt (mầm hai lá; 1536 × 1024, nền trắng): cùng thân, cùng mắt, cùng nét. Dạng 1 là bản non hơn"))
    return R


CHECK = [
    "**Mập, mềm, tròn**: bụng to xệ ngồi bệt, đầu vòm nhỏ hơn đặt thẳng lên bụng, không cổ; đầu và bụng **liền một khối**. Không chân, "
    "không đuôi, không tai.",
    "Tay trước (bên trái người xem) hình hạt đậu mập, **đè lên** mép trái bụng, có viền kín riêng; tay sau chỉ lộ một dải hẹp ở mép phải.",
    "**Mắt chỉ lòng trắng**: hai bầu dục trắng trơn, vành dày màu thân đậm (không mực đen), không con ngươi, không chấm sáng. Má hồng. "
    "**Không có mồm** (mồm tròn chỉ hiện lúc bắn chiêu, làm ở lượt sau).",
    "Tóc và thứ trong bụng đúng hướng thiết kế của file (mầm hai lá + hạt giống / mũ nấm + bào tử / mũ rêu hai cành + lá kẹt); thứ "
    "trong bụng nhạt màu, nét mảnh không mực.",
    "Tô phẳng: **không** vệt bóng trắng, không phản chiếu, không bóng đổ; nền trắng tinh.",
]

FIX = [
    ("Vẽ con ngươi, chấm sáng trong mắt", "The eyes are completely blank: plain white ovals with a thick coloured rim. Remove the "
                                          "pupils and every dot."),
    ("Vẽ mồm, mũi", "Remove the mouth and the nose: the face is only the two blank eyes and the two blush marks."),
    ("Vẽ bóng loáng, vệt sáng trắng, kiểu thuỷ tinh / nước", "Flat colour only: remove every white shine mark, reflection, glossy "
                                                             "highlight, darker rim and gradient; only the pale things inside the "
                                                             "belly show that it is translucent."),
    ("Gầy, cao, có cổ, có chân", "Make it much fatter and rounder: a huge sagging belly sitting flat on the ground, a smaller head "
                                 "dome directly on it with no neck, NO legs and NO feet."),
    ("Đầu và bụng tách hai khối có nét mực chạy ngang", "The head and the belly are ONE jelly mass: remove the ink line across the "
                                                        "middle; keep only a short soft fold line at each side."),
    ("Thứ trong bụng đậm như bên ngoài, nét mực đen", "The things inside the belly are INSIDE the jelly: redraw them paler and "
                                                      "washed out, with thin pencil outlines in the darker body tone, no ink."),
    ("Thân lệch sơ đồ", "Follow image 1 exactly for the body: turned slightly to the viewer's right, the front arm at the left "
                        "overlapping the belly, the eyes low on the head."),
]


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (tinh linh rừng mập, tướng thứ 2 đảo Mộc, tên chưa đặt)", "",
          ("DẠNG 1 (làm sau dạng 2, cùng rig): một file prompt, thiết kế là đề xuất của Claude, chờ duyệt. " if K == 1 else "")
          + "Làm 2026-11-12, lượt 2: bản đầu bị trả (\"nhìn giống con gốc quá\"; mắt chỉ lòng trắng; mồm chỉ hiện khi bắn chiêu). Ba hướng "
          "thiết kế cho người dùng chọn một; màu và chi tiết là đề xuất của Claude. Thân, tay, mắt theo khung part của con gốc "
          "`monster_3407`; tóc và thứ trong bụng là mảnh riêng. Ghi chú: `ArtGen/Spine/inbox/tinh_linh_ghichu.md`.", "",
          "Mỗi hướng một file prompt; **chỉ gửi GPT đường dẫn file**, GPT tự mở ảnh mẫu và tự lưu (trùng tên thì `_2`, `_3`…):", "",
          "| Hướng | File prompt | Ảnh lưu ở |", "|---|---|---|"]
    ps = []
    for kieu, c in (KIEU_1 if K == 1 else KIEU_3 if K == 3 else KIEU).items():
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
              form(c), "", palette(c), "", FRAME, "", POSE, "", JELLY, "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        gd.append(f"| {c['vi']} | `{Wp(p)}` | `{Wp(out)}` |")
        ps.append(p)
    R = refs("hat" if K == 1 else "hoa" if K == 3 else "mam")
    gd += ["", f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_<hướng>.txt` (thêm "
           "`--note \"...\"` để sửa nhanh).", "",
           "Lượt 2 (tờ mảnh theo khung part, mồm tròn lúc bắn chiêu, các bộ mắt) chỉ dựng sau khi concept được duyệt "
           "(`tai_ve/L1_duyet.png`).", "",
           "Ảnh mẫu (ảnh 1 mỗi hướng một sơ đồ `bo_cuc_<hướng>.png`, cùng hình, khác màu):", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/tinh_linh.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ps:
        print(p)


if __name__ == "__main__":
    main()
