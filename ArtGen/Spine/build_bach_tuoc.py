# -*- coding: utf-8 -*-
"""Gói GPT vẽ bạch tuộc quái vật (mã làm việc bach_tuoc, con gốc của rig: monster_3616). Dạng người dùng giao là DẠNG 2.

Người dùng (2026-11-12): "concept bạch tuộc quái vật". Bản 1 (tím mực, đội mảnh vỏ ốc thay mảnh tàu, san hô đen, xích) bị trả:
"không nhất thiết phải thiết kế có cả phần tàu ở trên đâu, bạn có thể bỏ phần đấy, phần xúc tu cũng có thể làm khác đi" và "đổi màu
khác đi, màu tím này không đẹp, thử phối đúng màu hồng đỏ giống bạch tuộc bình thường xem".
Bản 2 (ĐỀ XUẤT của Claude, chờ duyệt): bạch tuộc HỒNG ĐỎ đầu trần, không mũ, không san hô, không xích; hai mắt vàng con ngươi ngang
dưới gờ mày dữ; mào ba gai thịt đỏ sẫm trên đỉnh đầu; đốm sẫm; phễu phụt mực; mặt dưới xúc tu kem có hai hàng giác hút.
Chỉ lấy của con gốc cách dựng (dáng, chỗ đặt, thứ tự chồng của đầu, mắt và các xúc tu). Con gốc nhìn trái; của mình LẬT NGANG.
Không đính ảnh con gốc vào prompt; đính sơ đồ bố cục tự dựng bằng mã (bach_tuoc.py bo_cuc).

    py -3 -I ArtGen/Spine/bach_tuoc.py bo_cuc
    py -3 -I ArtGen/Spine/build_bach_tuoc.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/bach_tuoc_2/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "bach_tuoc"
K = int(os.environ.get("BT_DANG", "2"))        # 2 = con bám con gốc (đã duyệt); 1 = con non trên cùng rig (BT_DANG=1)
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DRAGON = os.path.join(HERE, "inbox", "rong_vay_1", "tai_ve", "L1_duyet.png")
WHALE = os.path.join(HERE, "inbox", "ca_voi_2", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


PALETTE = ("COLOURS, the natural colours of a common red octopus, slightly muted (use exactly these, each area one flat colour): the "
           "whole skin (head and the upper side of every tentacle) warm CORAL RED, a pinkish red (#D45C4E); darker red blotches "
           "and spots (#B03E3A) scattered on the top and back of the head and on the upper side of the tentacles; the three crest "
           "spikes, the two brow ridges and the eyelids DARK MAROON RED (#8A2C30); the UNDERSIDE of the tentacles pale CREAM "
           "(#F7E4D2) with round suckers in soft salmon pink (#ECAA96), each sucker a ring with a small dark centre; the eyes "
           "warm yellow (#F4C84A) with a dark HORIZONTAL bar pupil and ONE tiny white dot in each; every outline dark-brown ink "
           "(#2B2118). Only these colours. NO purple, NO violet, NO blue, NO green, NO grey, NO black areas.")

FORM = ("CREATURE: a MONSTER OCTOPUS of the water element for a monster-collecting game: a heavy, squat, angry sea beast, a small "
        "kraken. A big round dome head sits directly on a skirt of SIX thick, short, curling tentacles. Its head is BARE: it "
        "wears nothing. It glares with two eyes under heavy, slanted brow ridges; a crest of three fleshy spikes runs over the "
        "back of its head. A menacing, stubborn, battle-ready monster, appealing but NOT a cute mascot, NOT smiling, no mouth "
        "visible. Everything on it is octopus: smooth skin with blotches, fleshy spikes, suckers. It has NO hat, NO helmet, NO "
        "shell, NO ship planks, NO coral, NO chain, NO clothes, NO arms, NO legs, NO teeth.\n"
        "Follow the LAYOUT GUIDE (image 1) closely for the construction, the placement, the size and the overlap order of every "
        "part listed here:\n"
        "- VIEW: three-quarter view; the creature faces the viewer's RIGHT. The two big front tentacles are at the right, the "
        "crest and the back tentacle at the left.\n"
        "- HEAD: one big smooth dome, about 700 px wide and 520 px tall (from about x = 476 to x = 1178, top at about y = 256), "
        "coral red, sitting low and wide; its lower edge is hidden behind the tentacles. About twelve darker red blotches of "
        "different sizes are scattered over its top and back (left) half, none on the face between the eyes.\n"
        "- EYES: TWO eyes, both on the right half of the head. The NEAR eye is the bigger one, at about x = 790, y = 560: an "
        "upright yellow oval about 80 px wide and 100 px tall. The FAR eye is smaller (about 65 px wide, 80 px tall), further "
        "right and a little higher, at about x = 1023, y = 488, just above the tip of the front tentacle. Each pupil is a dark "
        "HORIZONTAL bar (as real octopuses have); one tiny white dot in each eye. A dark-maroon upper eyelid covers the top "
        "quarter of each eye.\n"
        "- BROW RIDGES: above each eye one thick, dark-maroon ridge of skin, like an angry eyebrow, about 150 px long and 26 px "
        "thick. The two ridges slant DOWN toward the middle between the eyes (the near one runs from about x = 718, y = 468 down "
        "to x = 855, y = 510; the far one from about x = 1080, y = 415 down to x = 975, y = 450), giving a fierce scowl.\n"
        "- CREST: THREE fleshy spikes in a row over the back of the head, at the upper left, each a curved thorn with a wide "
        "base that grows out of the head outline and a sharp tip leaning backward (to the left): the biggest at the top (tip "
        "at about x = 780, y = 165, about 85 px wide at the base), the middle one at about x = 615, y = 240, the smallest at "
        "about x = 505, y = 370. Dark maroon red.\n"
        "- SIPHON: one short fleshy funnel tube on the cheek, below and between the eyes at about x = 910, y = 638: a darker "
        "red oval ring about 65 px wide with a dark opening, pointing forward (right). The creature shoots ink from it.\n"
        "- TENTACLES: SIX thick, short, tapering tentacles; upper side coral red with a few darker blotches, underside pale "
        "cream with TWO ROWS of round suckers. The TWO BIG FRONT tentacles are at the right and curl upward so their cream "
        "undersides with suckers face the viewer: the front-most one rises in front of the right side of the head, a fat "
        "crescent about 200 px wide and 340 px tall with its tip pointing up at about x = 1090, y = 530; the second one lies in "
        "front of the body and curls into a hook, tip pointing up-left at about x = 720, y = 730, its cream underside along "
        "the bottom (about x = 700-930, y = 700-900). THREE smaller tentacles hang side by side under the middle of the head "
        "(x = 450-700, y = 690-900) like three fat fingers, seen from their red upper side, tips on the ground. The LAST "
        "tentacle is at the far left, behind, its tip curling up to show a little cream underside at about x = 400, y = 630.\n"
        "- Exactly one head, two eyes, three crest spikes, six tentacles.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole creature is about 810 px wide (from about x = 370 to x = 1180) and "
         "about 745 px tall (from the tip of the top crest spike at about y = 160 to the tentacle tips at about y = 905).")

POSE = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): sitting still on "
        "its tentacles in a calm, clean resting pose. Every part is clearly separated by its own closed ink outline: the head, "
        "each eye, each crest spike, each tentacle. No water, no bubbles, no ink clouds, no sparkles, no magic lines, no "
        "splashes, no ground, no seaweed.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The "
        "layout guide is a stiff flat computer diagram with rough, jagged edges and broken outlines: take the construction, the "
        "placement, the proportions and the overlaps from it, never its mechanical line, its jagged edge noise, its cut-off "
        "straight edges or its empty flat fills. Redraw every shape cleanly, rounded and with character; where the guide shows "
        "a part cut off by a straight edge, complete it into a natural rounded shape that tucks behind its neighbour.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown ink "
        "pen (#2B2118), an outline about 6 px thick on this canvas for the head, the tentacles and the crest spikes and "
        "about 4 px for small details (suckers, blotches, the siphon, the eyes), a closed outline around every part; "
        "every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes "
        "thinner than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the brows, under "
        "the figure, on the ground or on the background), no white highlights or shine spots, no gloss, no wet or slimy look, no "
        "reflections, no glow, no rim light, no gradients, no 3D look. A different tone appears only where the design itself "
        "lists a different colour. The only white dots are the tiny ones in the eyes.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


DRAFT = os.path.join("..", "mau", "nhap_3_lat_ngang.png")
# Bản nháp 3 (L1_concept_3.png: một mắt, không mồm) vẽ theo sơ đồ LẬT NGANG vì tôi đoán sai hướng mặt con gốc; người dùng 2026-11-12:
# "hướng mắt bạn ngược rồi, trong game mắt hướng cùng với bên xúc tu ngắn, của bạn gen bị ngược". Con gốc nhìn sang PHẢI, về phía ba
# xúc tu ngắn; hai xúc tu to ở bên trái là phía sau. Lượt này: đính bản nháp 3 đã lật ngang bằng mã (xúc tu về đúng chỗ của rig) và
# chỉ sửa con mắt (nhìn sang phải) + dời mào gai ra sau đầu (trên trái).

REVISE = ("TASK: redraw image 1 (the previous draft of this creature) as ONE picture, changing ONLY the two things listed below.\n\n"
          "KEEP IDENTICAL (if the new picture were laid over image 1, everything else must match): the whole drawing style, the "
          "wobbly ink line, the crayon hatching, every colour; the size and place of the creature on the canvas; the round dome "
          "head and its outline; the darker red blotches; the small pointed warts; the scar; all six tentacles with their cream "
          "undersides and suckers, exactly where and how they are (the two big cream-and-red tentacles at the LEFT, the three "
          "short finger-like tentacles under the head at the middle and RIGHT, the last small tentacle at the far right).\n\n"
          "THE CREATURE FACES THE VIEWER'S RIGHT: its front is the side with the SHORT tentacles (right); the two big "
          "tentacles at the left are behind it. In image 1 the eye and the crest still point the wrong way. CHANGE:\n"
          "1. THE EYE LOOKS TO THE RIGHT. Keep the one eye where it is, in the middle of the visible side of the head, inside "
          "its round eye-socket ring, same size, but mirror its details left-to-right: the dark HORIZONTAL bar pupil sits "
          "toward the RIGHT side of the yellow eye and the tiny white dot is at the right end of the pupil; the heavy dark-maroon "
          "brow ridge above the eye is HIGH at its LEFT end and slants DOWN toward the RIGHT; the dark-maroon eyelid is lowered "
          "over the top of the eye, also lower at the right; the small round bump on the socket ring is at its upper LEFT "
          "(behind the eye). A fierce glare toward the right, exactly as the face is built in image 2.\n"
          "2. THE CREST IS ON THE BACK OF THE HEAD, AT THE UPPER LEFT. Remove the three dark-maroon crest spikes from the "
          "upper right of the head (that part of the outline becomes smooth dome with two or three small warts) and draw them "
          "over the upper LEFT of the head instead, as in image 2: the biggest one near the top of the head a little left of "
          "the middle, the middle one further left, the smallest lowest at the left, each a curved thorn with a wide base and "
          "its sharp tip leaning backward, to the LEFT.\n"
          "3. Nothing else changes. Still exactly one head, ONE eye, NO mouth and no hole anywhere, three crest spikes, six "
          "tentacles.")


def refs():
    return [
        (os.path.join(mau_dir(), "bo_cuc.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing how it is built, where "
         "every part goes on the canvas, how big it is and which part overlaps which (the coral-red dome head with its darker "
         "blotches; the two yellow eyes with horizontal pupils under the two slanted dark-maroon brow ridges; the three dark "
         "crest spikes at the upper left; the small siphon ring on the cheek; the two big cream-and-red front tentacles with "
         "suckers at the right; the smaller red tentacles under the head). Follow it closely; redraw everything in the "
         "hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn sang phải, đầu vòm to đầu trần có đốm sẫm, hai "
         "mắt vàng con ngươi ngang dưới hai gờ mày đỏ sẫm chéo, ba gai mào ở trên trái, phễu nhỏ trên má; hai xúc tu trước to (mặt "
         "dưới kem có giác hút) bên phải, các xúc tu nhỏ dưới đầu. Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng"),
        (DRAGON,
         "an approved hero of the same game (a winged sea-serpent), 1536x1024, white background: match EXACTLY its wobbly pen "
         "line, its visible crayon hatching and its completely flat colouring. Do NOT copy its species, its design or its "
         "colours.",
         "Rồng vây đã duyệt (1536 × 1024, nền trắng): rồng rắn chàm tím có cánh vây lam xám, sừng đen. Chỉ lấy nét bút rung, vân sáp, "
         "tô phẳng"),
        (WHALE,
         "another approved hero of the same game (a mutant whale monster, second evolution stage), 1536x1024, white background: "
         "the same line and flat crayon colouring; the same level of menace and of detail for a second-stage monster. Do NOT "
         "copy its species, design or colours.",
         "Cá voi biến dị dạng 2 đã duyệt (1536 × 1024, nền trắng): quái cá voi há miệng đầy nanh. Lấy nét, tô phẳng, mức \"dữ\" và mật "
         "độ chi tiết của một dạng 2"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]


CHECK = [
    "Nhìn sang **phải**, tức là về phía **ba xúc tu ngắn** (như con gốc); hai xúc tu to lộ mặt dưới kem nằm bên **trái** (phía sau). "
    "Đầu vòm to **hồng đỏ**, **đầu trần** (không mũ, vỏ, san hô, xích), ngồi trên **sáu xúc tu** ngắn mập.",
    "Mặt dựng như con gốc: **nhìn nghiêng, chỉ MỘT mắt** vàng **con ngươi ngang** nằm giữa vòm đầu, trong **vành hốc mắt tròn**; một "
    "**gờ mày đỏ sẫm** (nếp da thuôn hai đầu) cao ở bên trái, dốc xuống về bên phải; con ngươi lệch về bên **phải**; **không mồm, "
    "không phễu, không mắt thứ hai**.",
    "**Mào ba gai thịt** đỏ sẫm ở trên **trái** (sau đầu), mũi gai ngả sang trái; **đốm sẫm** lốm đốm trên đỉnh và sau đầu.",
    "Hai xúc tu to bên **trái** cong lên lộ **mặt dưới kem có giác hút**; ba xúc tu nhỏ như ba ngón dưới đầu ở giữa và bên phải; một "
    "xúc tu nhỏ ngoài cùng bên phải.",
    "Mỗi bộ phận có viền mực kín riêng. Tô phẳng: **không** bóng, không điểm sáng, không ướt bóng; nền trắng tinh. Không tím, lam.",
]

FIX = [
    ("Có mũ, vỏ ốc, mảnh tàu, san hô, xích", "The head is BARE: remove everything on it except the three fleshy crest spikes. No hat, no "
                                             "shell, no planks, no coral, no chain."),
    ("Có bóng, mảng sáng tối, da ướt bóng", "Flat colour only: remove every shadow, highlight, gradient and wet shine; keep the crayon "
                                            "hatching as texture only."),
    ("Mặt hiền, dễ thương kiểu linh vật", "Make it a glaring monster: heavy dark brow ridges slanting down toward the middle, eyelids "
                                          "lowered over the top of the eyes, the body heavy and squat. Not cute, not smiling."),
    ("Con ngươi tròn hoặc dọc", "Each pupil is a dark HORIZONTAL bar across the yellow eye."),
    ("Mắt nhìn sang trái, mào gai ở bên phải", "The creature faces the viewer's RIGHT, toward its short tentacles: the pupil sits "
                                               "toward the right of the eye, the brow slants down to the right, and the three crest "
                                               "spikes are over the upper LEFT of the head, leaning left."),
    ("Có hai mắt, hoặc có mồm / phễu / lỗ trên má", "The head is in profile: exactly ONE eye is visible, and there is NO mouth, no "
                                                    "funnel, no hole anywhere on the head."),
    ("Màu tím, lam, hoặc đỏ chói", "Use only the listed colours: muted coral red skin, darker red blotches, dark maroon spikes and "
                                    "brows, pale cream undersides, salmon suckers, yellow eyes."),
]


HOLE = ("TASK: draw ONE prop for a 2D game as ONE picture: a HOLE IN THE GROUND that a burrowing monster bursts out of, in the "
        "hand-drawn style of the reference images.\n\n"
        "THE HOLE: a wide, shallow-looking round pit in bare earth, seen from the side and slightly from above, so its opening is "
        "a wide flat ELLIPSE about 1180 px wide and 300 px tall, centred on the canvas at about x = 768, y = 520. The INSIDE of "
        "the hole is one flat, very dark earth-black (#231C19) ellipse with NOTHING in it. All around the opening runs a raised, "
        "broken RIM of pushed-up earth: lumpy clods and cracked slabs of soil thrown outward, like the crater a mole or a worm "
        "leaves. The rim at the BACK (above the dark ellipse) is low and thin, about 40 px tall; the rim at the FRONT (below the "
        "dark ellipse) is the biggest: a heap of chunky clods about 150 px tall that overlaps the lower edge of the dark "
        "ellipse with an uneven, bumpy top edge; at the left and right ends the rim is medium. About eight small loose clods "
        "and pebbles lie on the ground close around the rim. The whole prop is about 1380 px wide and 520 px tall.\n\n"
        "COLOURS (each area one flat colour): earth clods warm mid brown (#8C6A48); a second, darker brown (#6E5038) for the "
        "under-sides of some clods and the cracks between them, used as flat patches, not as shading; a few pale sandy "
        "pebbles (#CDB48C); the inside of the hole very dark earth-black (#231C19); every outline dark-brown ink (#2B2118). No "
        "grass, no plants, no water, no creature, no tentacles, no dust clouds, no flying debris, no motion lines.")


def build_hole():
    """Hố đất của clip appear (người dùng: "gen thêm 1 cái hố đất trồi lên (tách 2 layer trước sau)"): gen MỘT ảnh cả hố, mã tách hai
    lớp (bach_tuoc.py cat_ho): lớp sau = lòng hố + vành sau, lớp trước = vành trước (đè lên thân lúc trồi)."""
    R = [(DRAGON, "an approved hero of the same game, 1536x1024, white background: match EXACTLY its wobbly dark-brown pen line, its "
                  "visible crayon hatching and its completely flat colouring. Take nothing of its content.",
          "Rồng vây đã duyệt (1536 × 1024, nền trắng): chỉ lấy nét bút rung, vân sáp, tô phẳng"),
         (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: its line and colouring style (brown ink pen outline + coloured pencil / "
                       "wax crayon hatching) and the way it draws earth and rocks. Take nothing else of its content.",
          "Bản đồ vẽ tay đã duyệt (1024 × 1536): nét bút mực nâu, vân chì sáp, cách vẽ đất đá")]
    out = os.path.join(save_dir(), "H01.png")
    p = os.path.join(pk(), "luot_2_ho_dat.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          "If a file with that name already exists, save as H01_2.png, H01_3.png ... in the same folder. Do not edit, move or "
          "delete any other file.", "", HOLE, "",
          "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF) everywhere outside the prop: no ground plane, no ground "
          "colour, no horizon, no cast shadow. Nothing is cut by the edges.", "",
          LINE.replace("for the head, the shell, the tentacles and the big coral", "for the rim and the big clods")
              .replace("(suckers, ridges, barnacles, chain links, spots)", "(cracks, pebbles)"),
          FLAT.replace("no shadow under the shell, under the figure,", "no shadow under the clods,").replace(
              " The only white dots are the tiny ones in the eyes.", ""),
          BG.replace("around the figure", "around the prop").replace("around the creature", "around it")]
    os.makedirs(pk(), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, out, R


def chosen():
    return os.path.join(save_dir(), "L1_duyet.png")


P_SAME = ("Same hand-drawn look as image 1: wobbly dark-brown ink outline (#2B2118) of the same thickness as in image 1, the same "
          "flat colours (coral red #D45C4E, darker red blotches #B03E3A, dark maroon #8A2C30, pale cream #F7E4D2, salmon suckers "
          "#ECAA96, yellow eye #F4C84A), the same loose crayon hatching. FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even "
          "colour, no shading, no highlights, no gloss, no glow, no gradients.")
P_PAGE = ("CANVAS: 1536x1024, pure-white background (#FFFFFF) everywhere outside the parts: no paper grain, no ground line, no "
          "shadow, no text, no labels, no numbers, no frame, no white sticker border. Nothing else on the page.")
TENT = ("a piece of a TENTACLE, stored in the rig at the angle shown: coral-red upper skin with one or two darker red blotches "
        "where the guide has them; where the guide shows a cream area, that is the pale cream underside with its round salmon "
        "suckers (each a ring with a small dark centre), with the thin ink line between skin and underside exactly where the "
        "guide has it")
PART_EN = {
    "P_tou": "the HEAD: the big dome, coral red, with the darker red blotches where the guide has them, the big blotch with the "
             "pale SCAR across it (a jagged pale slash, pointed at both ends, as in image 1), the round EYE-SOCKET RING with the small round bump on it, and the dark-maroon BROW RIDGE "
             "above the ring (an organic fleshy ridge, thick in the middle, pointed at both ends). The inside of the socket ring "
             "is plain coral-red skin: do NOT draw the eye, it is a separate part. No mouth, no second eye",
    "P_yanjing1": "the EYE, open, stored at the angle shown: a yellow oval with a dark bar pupil and one tiny white dot, a "
                  "dark-maroon eyelid over part of it; keep the pupil bar and the edge of the lid exactly at the angle and place "
                  "the guide shows",
    "P_yanjing2": "the EYE, half closed, same shape and angle: the dark-maroon eyelid covers a little more than half of the yellow "
                  "eye; the pupil bar shows below the lid as in the guide",
    "P_yanjing3": "the EYE, closed, same shape and angle: all dark-maroon eyelid with one thick dark ink line across it where the "
                  "guide has it",
    "P_shou1_3": "the thick BASE of a tentacle: one smooth coral-red blob with one or two darker red blotches",
    "gai": "a CREST SPIKE: a curved fleshy thorn with a wide base and a sharp tip, dark maroon red, two or three short darker "
           "lines along it",
}
PART_VI = {"P_tou": "đầu (vòm, đốm, sẹo, vành hốc mắt, gờ mày; không vẽ mắt)", "P_yanjing1": "mắt mở", "P_yanjing2": "mắt lim dim",
           "P_yanjing3": "mắt nhắm", "P_shou1_3": "khối gốc xúc tu", "P_shou1_1": "xúc tu 1 ngọn", "P_shou1_2": "xúc tu 1 gốc",
           "P_shou2_1": "xúc tu 2 ngọn", "P_shou2_2": "xúc tu 2 gốc", "P_shou6_1": "xúc tu trước gốc", "P_shou6_2": "xúc tu trước ngọn",
           "P_shou3_1": "ngón 1", "P_shou4_1": "ngón 2", "P_shou5_1": "ngón 3", "gai_1": "gai mào to", "gai_2": "gai mào vừa",
           "gai_3": "gai mào nhỏ"}


if K == 1:
    P_SAME = P_SAME.replace("coral red #D45C4E, darker red blotches #B03E3A, dark maroon #8A2C30, pale cream #F7E4D2, salmon suckers "
                            "#ECAA96, yellow eye #F4C84A",
                            "light coral pink #EE7C6C, darker blotches #CE5852, dark rose-red #AA3E40, pale cream #FAE8D6, salmon suckers "
                            "#F0B2A0, yellow eye #F6CE54")
    assert "#EE7C6C" in P_SAME
    PART_EN["P_tou"] = ("the HEAD: the big dome, light coral pink, with the few darker blotches where the guide has them, the big round "
                        "EYE-SOCKET RING with the small round bump on it, and the small dark rose-red BROW RIDGE above the ring (a short "
                        "organic fleshy ridge, pointed at both ends). The inside of the socket ring is plain coral-pink skin: do NOT draw "
                        "the eye, it is a separate part. No scar, no mouth, no second eye")
    PART_EN["P_yanjing1"] = PART_EN["P_yanjing1"].replace("a \"\n", "a ").replace("dark-maroon eyelid over part of it", "thin dark rose-red eyelid over its top edge")
    TENT = TENT.replace("coral-red upper skin", "light coral-pink upper skin")
    PART_EN["P_shou1_3"] = PART_EN["P_shou1_3"].replace("coral-red", "light coral-pink")
    PART_EN["gai"] = "a small budding CREST SPIKE: a short curved fleshy thorn with a wide base, dark rose-red"


def build_parts():
    """lượt 3: tờ mảnh theo khung part (bach_tuoc.py nhom_part → mau/part_Q<k>.png). Chỉ dựng khi concept đã duyệt (L1_duyet.png)."""
    import json
    out = []
    if not os.path.exists(chosen()):
        return out
    for k in range(1, 12):
        to = f"Q{k}"
        gimg, gj = os.path.join(mau_dir(), f"part_{to}.png"), os.path.join(mau_dir(), f"part_{to}.json")
        if not os.path.exists(gj):
            break
        K_ = json.load(open(gj, encoding="utf-8"))
        luu = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_3_part_{to}.txt")
        n = len(K_)
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(chosen())}: the APPROVED picture of the creature (" + (
                 "a coral-red monster octopus in profile, one yellow eye, three dark crest spikes" if K == 2 else
                 "a young light coral-pink octopus in profile, one very big yellow eye, two small crest spikes") + "), 1536x1024, white "
             "background. Use it for the design, the colours, the wobbly dark-brown ink line and the crayon texture.",
             f"image 2 = {Wp(gimg)}: PART SHEET GUIDE, 1536x1024, white background: {n} separate cut-out parts of the creature's "
             "animation rig. Each part is shown as its exact SILHOUETTE (outline, size, orientation and place on the sheet are "
             "all fixed by the rig; several parts are stored rotated or cut off by straight edges), coloured flat by a computer: "
             "the colours and the pattern are in the right places, but the lines are stiff and mechanical.",
             "", f"SAVE: save it as a PNG to {Wp(luu)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             f"TASK: redraw image 2 as the finished, clean sheet of these {n} cut-out parts, drawn in the style of image 1.", "",
             "RULES:",
             "- EVERY PART KEEPS ITS SILHOUETTE EXACTLY: the same outline, the same size, the same orientation, the same position "
             "on the canvas as in image 2. Do not rotate, mirror, move, resize, shrink, straighten, complete or simplify any shape. "
             "If the result were laid over image 2, every part would cover its shape exactly, no more and no less.",
             "- A dark-brown ink outline (#2B2118, about 6 px) runs all the way around each silhouette, ON its edge (ONE CLOSED "
             "SHAPE per part). Where a part is cut straight in the guide, keep that straight cut and outline it too.",
             "- Inside, keep the colours and the pattern where the guide has them (the cream underside on the same side, the "
             "suckers and blotches in the same places) and redraw them cleanly and organically: flat colours with loose crayon "
             "hatching, wobbly hand-drawn lines instead of the guide's stiff ones.",
             "- Flat fill only: no shading, no shadow, no highlight, no gradient.",
             f"- Exactly these {n} parts, white background between them, nothing else. Do not assemble them into a creature.", "",
             f"THE {n} PARTS (the place is the centre of the part's box on the 1536x1024 canvas):"]
        vi = []
        for i, (ten, v) in enumerate(K_.items(), 1):
            en = PART_EN.get(ten) or (PART_EN["gai"] if ten.startswith("gai") else TENT)
            t.append(f"{i}. at about x = {v['x'] + v['w'] / 2:.0f}, y = {v['y'] + v['h'] / 2:.0f} (about {v['w']} px wide, {v['h']} px "
                     f"tall): {en}.")
            vi.append(f"`{ten}` ({PART_VI.get(ten, ten)})")
        t += ["", P_SAME, P_PAGE]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        out.append((to, p, gimg, luu, vi))
    return out


def build_mini():
    """bạch tuộc con của chiêu cuối (người dùng: "triệu hồi ra các con bạch tuộc mini"): một ảnh, một con, cùng màu, cùng nét với concept
    đã duyệt → tai_ve/C01.png (bach_tuoc.py cat_con cắt nền → manh/con.png)."""
    if not os.path.exists(chosen()):
        return None
    luu = os.path.join(save_dir(), "C01.png")
    p = os.path.join(pk(), "luot_3_bach_tuoc_con.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(chosen())}: the APPROVED picture of the PARENT creature (a coral-red monster octopus in profile, one yellow "
         "eye, three dark crest spikes), 1536x1024, white background. Use it for the colours, the wobbly dark-brown ink line, the "
         "crayon texture and the way the eye, the brow, the blotches and the suckers are drawn.",
         "", f"SAVE: save it as a PNG to {Wp(luu)}",
         "If a file with that name already exists, save as C01_2.png, C01_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: draw ONE BABY of the creature in image 1 as ONE picture: a tiny octopus minion that the big one summons in battle.", "",
         "THE BABY: the same species, much simpler and rounder: one smooth round dome head, coral red, with three or four small "
         "darker red blotches and ONE small dark-maroon crest spike on the back of its head (upper left); seen in profile, facing "
         "the viewer's RIGHT, with ONE big yellow eye (dark horizontal bar pupil toward the right, one tiny white dot) under a small "
         "dark-maroon brow that slants down to the right: a cheeky, fierce little glare. NO mouth. Under the head FOUR short, fat, "
         "stubby tentacles side by side, coral red, their tips curling up a little to show a bit of pale cream underside with one or "
         "two salmon suckers. It stands on its tentacles, ready to pounce. About 620 px wide and 560 px tall, centred on the canvas, "
         "nothing cut by the edges.", "",
         "Draw it as ONE closed shape with a dark-brown ink outline about 8 px thick (it will be shown very small in the game, so "
         "keep the shapes big and simple, with few details).", "",
         P_SAME, P_PAGE.replace("outside the parts", "outside the creature")]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, luu


def build_arm():
    """xúc tu DÀI của clip appear (người dùng 2026-11-12, xem bản kéo dài xúc tu ngắn của thân: "nhìn hơi xấu, bị gãy mesh nhiều"): một
    xúc tu duỗi thẳng nằm ngang, gốc bên trái → tai_ve/V01.png (bach_tuoc.py cat_voi → manh/voi.png; rig dựng thành dải lưới nhiều đốt)."""
    if not os.path.exists(chosen()):
        return None
    luu = os.path.join(save_dir(), "V01.png")
    p = os.path.join(pk(), "luot_3_xuc_tu_dai.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(chosen())}: the APPROVED picture of the creature (a coral-red monster octopus), 1536x1024, white background. "
         "Use it for the colours, the wobbly dark-brown ink line, the crayon texture and the way the tentacles, their cream "
         "undersides, the suckers and the darker blotches are drawn.",
         "", f"SAVE: save it as a PNG to {Wp(luu)}",
         "If a file with that name already exists, save as V01_2.png, V01_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: draw ONE long arm (tentacle) of the creature in image 1 as ONE picture, stretched out perfectly STRAIGHT and "
         "HORIZONTAL, seen from the side. It will be bent by a skeleton in the game, so it must be straight here.", "",
         "THE ARM: about 1380 px long, lying exactly along the horizontal middle line of the canvas (y = 512), from x = 80 to "
         "x = 1460. Its BASE is at the LEFT, about 230 px thick; it tapers smoothly and evenly, like a long carrot, to a rounded TIP "
         "at the RIGHT, about 46 px thick. Its upper and lower edges are both straight, symmetric about the middle line (no waves, "
         "no curl, no bend, no hook at the tip). The UPPER two thirds of its thickness are coral-red skin with about seven "
         "darker red oval blotches of different sizes spread along it; the LOWER third is the pale cream underside, a band that "
         "runs the whole length and narrows with the arm, with ONE row of about twelve round salmon suckers (each a ring with a "
         "small dark centre) that get smaller toward the tip; one thin ink line runs along the whole arm between the skin and the "
         "underside. The base end at the left is cut off straight (a vertical cut, it will be hidden inside the body) and is "
         "outlined too.", "",
         "Draw it as ONE closed shape with a dark-brown ink outline about 6 px thick.", "",
         P_SAME, P_PAGE.replace("outside the parts", "outside the arm")]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, luu


NON = ("TASK: draw the YOUNG form (the first evolution stage) of the creature in image 1 as ONE picture, in a clean animation-ready "
       "resting pose. Image 1 is the grown, fierce adult; this is the same species as a youngster: smaller, rounder, big-headed, "
       "with a huge eye, plucky and stubborn rather than fierce. Same drawing style as image 1.\n\n"
       "Follow the LAYOUT GUIDE (image 2) closely for the construction, the placement, the size and the overlap order of every part:\n"
       "- VIEW: seen from the side, in profile; the creature faces the viewer's RIGHT, toward its short tentacles. Only ONE eye is "
       "visible. It has NO mouth, no hole, no siphon anywhere.\n"
       "- HEAD: one very big smooth round dome, about 745 px wide and 500 px tall (from about x = 380 to x = 1125, top at about "
       "y = 225), much bigger than the tentacles under it. LIGHT CORAL PINK. Only about five small darker oval blotches, spread "
       "over the top and the back; NO scar, NO warts.\n"
       "- EYE: ONE very big eye in the middle of the visible side of the head, at about x = 785, y = 540: an upright yellow oval "
       "about 135 px wide and 165 px tall, with a dark HORIZONTAL bar pupil shifted a little toward the RIGHT and one tiny white "
       "dot at the right end of the pupil. It sits inside a round raised EYE SOCKET: one thin ink ring about 210 px across "
       "around the eye, with one small round bump on the ring at its upper LEFT. A thin dark rose-red upper eyelid covers only "
       "the very top of the eye, slanting down a little toward the right. Above the ring, a SMALL, short brow ridge (about 160 px "
       "long, thin, pointed at both ends, dark rose-red), high at its left end and slanting gently down to the right: a "
       "determined, cheeky look, NOT angry-monstrous, NOT smiling, NOT sleepy.\n"
       "- CREST: only TWO small budding spikes on the back of the head, at the upper LEFT: short curved thorns with a wide base, "
       "the bigger one near the top (tip at about x = 725, y = 180, only about 55 px tall), the smaller one further left (tip "
       "at about x = 560, y = 230). Dark rose-red.\n"
       "- TENTACLES: SIX short, stubby, chubby tentacles, shorter than the adult's; upper side light coral pink with one or two "
       "small darker blotches each, underside pale cream with a few round salmon suckers (ring with a small dark centre). The "
       "TWO bigger ones are at the LEFT (behind) and curl up to show their cream undersides (about x = 500-860, y = 550-840). "
       "THREE small finger-like ones hang side by side under the head at the middle and right (about x = 850-1080, y = 680-855). "
       "The LAST small one is at the far right behind them (about x = 1050-1150, y = 690-830).\n"
       "- Exactly one head, ONE eye, NO mouth, two small crest spikes, six tentacles.")

PALETTE_NON = ("COLOURS (each area one flat colour): the whole skin LIGHT CORAL PINK (#EE7C6C), clearly lighter and pinker than the "
               "adult in image 1; the few blotches a darker coral (#CE5852); the two crest spikes, the brow ridge and the eyelid dark "
               "rose-red (#AA3E40); the underside of the tentacles pale cream (#FAE8D6) with salmon suckers (#F0B2A0); the eye warm "
               "yellow (#F6CE54) with a dark horizontal bar pupil and ONE tiny white dot; every outline dark-brown ink (#2B2118). "
               "Only these colours. NO purple, NO blue, NO green, NO grey.")

FRAME_NON = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
             "nothing cut by the edges. As in the guide, the whole creature is about 775 px wide (from about x = 380 to x = 1155) and "
             "about 680 px tall (from the tip of the top crest spike at about y = 175 to the tentacle tips at about y = 855).")

CHECK_NON = [
    "Con NON của dạng 2: cùng loài, cùng nét; **đầu rất to** so với xúc tu, da **hồng san hô nhạt** hơn dạng 2.",
    "Nhìn nghiêng sang **phải**, **một mắt rất to** vàng con ngươi ngang lệch phải, trong vành hốc mắt tròn có bướu nhỏ ở trên trái; mí "
    "mỏng, **gờ mày nhỏ** dốc nhẹ xuống phải: lì lợm, quả quyết, chưa dữ. **Không mồm.**",
    "Mào mới nhú **hai gai nhỏ** ở trên trái; khoảng năm đốm nhỏ; **không sẹo, không mụn gai**.",
    "**Sáu xúc tu ngắn mập**: hai cái to hơn ở bên trái lộ mặt dưới kem có giác hút, ba ngón nhỏ ở giữa và bên phải, một cái nhỏ ngoài "
    "cùng bên phải.",
    "Mỗi bộ phận có viền mực kín riêng. Tô phẳng, không bóng, không điểm sáng; nền trắng tinh.",
]


def main_non():
    """gói của DẠNG 1 (con non, BT_DANG=1): concept vẽ theo concept dạng 2 đã duyệt + sơ đồ bố cục dựng từ rig dạng 1
    (BT_DANG=1 bach_tuoc_rig.py bo_cuc <mau/bo_cuc.png>); lượt 3 (tờ mảnh) như dạng 2. Hố đất, bạch tuộc con, xúc tu dài dùng chung."""
    lon = os.path.join(HERE, "inbox", f"{CODE}_2", "tai_ve", "L1_duyet.png")
    R = [(lon, "the APPROVED ADULT form of the creature (second evolution stage): a coral-red monster octopus in profile, facing "
               "right, one yellow eye in a round socket ring under a heavy brow, three dark crest spikes, blotches, a scar, small "
               "warts, six tentacles, 1536x1024, white background. Match EXACTLY its drawing style: the wobbly dark-brown ink line, "
               "the crayon hatching, the completely flat colouring, the way the eye, the socket ring, the blotches, the cream "
               "undersides and the suckers are drawn. The young form is this same animal, younger (see the TASK).",
          "Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn nghiêng sang phải, một mắt vàng trong vành hốc mắt "
          "dưới gờ mày dữ, mào ba gai, đốm, sẹo. Lấy nét vẽ, cách vẽ mắt, vành hốc mắt, đốm, giác hút"),
         (os.path.join(mau_dir(), "bo_cuc.png"),
          "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of the YOUNG form showing how it is built, where "
          "every part goes on the canvas, how big it is and which part overlaps which (the very big light-pink dome head with its "
          "few blotches; the one very big yellow eye in its socket ring with the small bump and the small brow ridge; the two "
          "small crest spikes at the upper left; the two bigger cream-and-pink tentacles at the left; the short tentacles under "
          "the head at the right). Follow it closely; redraw everything cleanly and organically in the hand-drawn style of image 1, "
          "never its stiff mechanical lines.",
          "Sơ đồ bố cục dựng từ rig dạng 1 (1536 × 1024, nền trắng): đầu vòm rất to hồng nhạt, một mắt to vàng trong vành hốc mắt, hai "
          "gai mào nhỏ ở trên trái, hai xúc tu to hơn bên trái, các xúc tu ngắn bên phải. Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng"),
         (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured "
                       "pencil / wax crayon hatching), nothing of its content.",
          "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp")]
    missing = [Wp(p_) for p_, _, _ in R if not os.path.exists(p_)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    out = os.path.join(save_dir(), "L1_concept.png")
    p = os.path.join(pk(), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not edit, "
          "move or delete any other file.", "", NON, "", PALETTE_NON, "", FRAME_NON, "", POSE.replace("each eye", "the eye"), "",
          LINE, FLAT.replace("The only white dots are the tiny ones in the eyes.", "The only white dot is the tiny one in the eye."), BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: `{CODE}` dạng 1 (bạch tuộc con non, tên chưa đặt)", "",
          "Làm 2026-11-12 sau khi dạng 2 xong (người dùng: \"làm dạng 1, con non\"). Cùng rig, cùng lưới, cùng clip với dạng 2 (con gốc "
          "`monster_3616`); chỉ vẽ lại da trong cùng khung part và đổi tỉ lệ vài xương. Thiết kế là đề xuất của Claude, chờ duyệt concept. "
          "Ghi chú: `ArtGen/Spine/inbox/bach_tuoc_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `BT_DANG=1 py -3 -I ArtGen/Spine/build_bach_tuoc.py` rồi `py -3 -I ArtGen/Spine/gen.py "
          f"ArtGen/Spine/gui_gpt/{CODE}_1/luot_1_concept.txt`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "Sơ đồ bố cục dựng lại bằng `BT_DANG=1 py -3 -I ArtGen/Spine/bach_tuoc_rig.py bo_cuc <đường dẫn mau/bo_cuc.png>`.", "",
           "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK_NON]
    L3 = build_parts()
    if L3:
        gd += ["", "## Lượt 3: tờ mảnh theo khung part (concept đã duyệt)", "",
               f"Ảnh 1 của mọi tờ = `{Wp(chosen())}` (concept dạng 1 đã duyệt, 1536 × 1024, nền trắng: bạch tuộc non hồng nhạt, một mắt rất to, "
               "hai gai mào nhỏ). Ảnh 2 = tờ hướng dẫn (1536 × 1024, nền trắng): mỗi part của rig là một hình bóng kín đúng cỡ, đúng hướng, tô "
               "phẳng bằng mã theo thiết kế dạng 1. Dựng tờ hướng dẫn: `BT_DANG=1 py -3 -I ArtGen/Spine/bach_tuoc.py nhom_part`; cắt: "
               "`BT_DANG=1 ... bach_tuoc.py cat_part Q1 Q2 ...`.", "",
               "| Tờ | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Mảnh |", "|---|---|---|---|---|"]
        gd += [f"| {X} | `{Wp(pp)}` | `{Wp(g)}` | `{Wp(o)}` | {', '.join(vi)} |" for X, pp, g, o, vi in L3]
    gd += ["", "Hố đất, bạch tuộc con, xúc tu dài của appear: dùng chung ảnh của dạng 2 (`inbox/bach_tuoc_2/tai_ve/H01, C01, V01`)."]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)
    for x in L3:
        print(x[1])


def main():
    R = refs()
    dr = os.path.join(save_dir(), DRAFT)
    sua = os.path.exists(dr)
    if sua:
        R = [(dr, "PREVIOUS DRAFT of THIS creature, 1536x1024, white background: a coral-red monster octopus in profile with one "
                  "yellow eye inside a round eye-socket ring, a dark brow ridge, three dark crest spikes, blotches, warts and a "
                  "scar; its two big tentacles are at the left. Redraw it, keeping everything except the direction of the eye and "
                  "the place of the crest (see KEEP IDENTICAL and CHANGE below).",
              "Bản nháp 3 đã lật ngang bằng mã (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn nghiêng, một mắt vàng trong vành hốc "
              "mắt, hai xúc tu to ở bên TRÁI, ba xúc tu ngắn ở giữa và bên phải; con mắt còn nhìn sang trái và mào gai còn ở trên "
              "phải. Giữ nguyên mọi thứ, chỉ sửa: mắt nhìn sang PHẢI (phía xúc tu ngắn), mào gai dời ra sau đầu (trên trái)")] + R
        R[1] = (R[1][0], "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature (drawn a little "
                         "smaller than image 1). Use it ONLY to see which way the FACE points and where the CREST sits: the one "
                         "yellow eye with its pupil toward the right under a brow ridge that slants down to the right, the small "
                         "bump at the upper left of the socket ring, and the three crest spikes over the upper left of the head, "
                         "leaning left. Do not copy its stiff lines or its size.",
                "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn sang PHẢI, một mắt vàng con ngươi ngang "
                "lệch phải dưới gờ mày dốc xuống phải, ba gai mào ở trên TRÁI (sau đầu), hai xúc tu to bên trái, xúc tu ngắn bên "
                "phải. Lượt này chỉ lấy hướng mắt và chỗ đặt mào gai")
    missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    out = os.path.join(save_dir(), "L1_concept.png")
    p = os.path.join(pk(), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
          "approved hero images.", "",
          FORM, "", PALETTE, "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
    if sua:
        t = t[:t.index("TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
                       "approved hero images.")] + [REVISE, "", PALETTE.replace("the two brow ridges and the eyelids", "the brow ridge and the eyelid")
                                                    .replace("the eyes \"\n", "the eyes ").replace("ONE tiny white dot in each", "ONE tiny white dot"),
                                                    "", POSE.replace("each eye", "the eye"), "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (bạch tuộc quái vật, tên chưa đặt)", "",
          "Làm 2026-11-12: reskin theo khung part của con gốc `monster_3616` (con gốc là dạng 2); màu và chi tiết là đề xuất của "
          "Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/bach_tuoc_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept.txt` (thêm `--note \"...\"` để "
          "sửa nhanh).", "",
          "Lượt 2 (tờ mảnh theo khung part) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/bach_tuoc.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    hp, ho, hR = build_hole()
    gd += ["", "## Hố đất của clip appear", "",
           f"File prompt: `{Wp(hp)}` → lưu `{Wp(ho)}` (1536 × 1024, nền trắng: một cái hố đất nhìn chéo từ trên, lòng hố đen, vành đất "
           "vỡ đùn lên quanh miệng, vành trước cao nhất). Mã tách hai lớp trước / sau: `py -3 -I ArtGen/Spine/bach_tuoc.py cat_ho`.", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(hR, 1)]
    gd += ["", "Kiểm: lòng hố là MỘT elip đen phẳng, không có gì bên trong; vành trước đè lên mép dưới elip; không cỏ, bụi, bóng đổ; "
           "nền trắng tinh."]
    L3 = build_parts()
    mn = build_mini()
    if L3:
        gd += ["", "## Lượt 3: tờ mảnh theo khung part (concept đã duyệt)", "",
               f"Ảnh 1 của mọi tờ = `{Wp(chosen())}` (concept đã duyệt, 1536 × 1024, nền trắng: bạch tuộc hồng đỏ nhìn nghiêng sang phải, "
               "một mắt vàng, mào ba gai). Ảnh 2 = tờ hướng dẫn (1536 × 1024, nền trắng): mỗi part của rig là một hình bóng kín đúng cỡ, "
               "đúng hướng, tô phẳng bằng mã theo thiết kế; GPT vẽ lại sạch mà giữ nguyên hình bóng. Dựng tờ hướng dẫn: "
               "`py -3 -I ArtGen/Spine/bach_tuoc.py nhom_part`; cắt: `bach_tuoc.py cat_part Q1 Q2 ...` → `manh/part/<tên>.png`.", "",
               "| Tờ | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Mảnh |", "|---|---|---|---|---|"]
        gd += [f"| {X} | `{Wp(pp)}` | `{Wp(g)}` | `{Wp(o)}` | {', '.join(vi)} |" for X, pp, g, o, vi in L3]
        gd += ["", "Kiểm từng tờ: đủ số mảnh, mỗi mảnh đúng chỗ, đúng cỡ, đúng hướng như tờ hướng dẫn; viền mực kín; nền trắng tinh; đầu "
               "không có mắt (mắt là mảnh riêng).", "",
               "| Sai | Gửi thêm |", "|---|---|",
               "| Mảnh lệch chỗ, sai cỡ, bị xoay | `Every part must keep exactly the silhouette, size, orientation and position it has in "
               "image 2.` |",
               "| Ghép các mảnh thành con, hoặc thêm mảnh | `Draw only the listed cut-out parts, separate, each in its own place; do not "
               "assemble them.` |"]
    vt = build_arm()
    if vt:
        gd += ["", "## Xúc tu dài của clip appear", "",
               f"File prompt: `{Wp(vt[0])}` → lưu `{Wp(vt[1])}` (1536 × 1024, nền trắng: một xúc tu duỗi thẳng nằm ngang, gốc dày bên trái, "
               "ngọn thon bên phải, hai phần ba trên là da hồng đỏ có đốm, một phần ba dưới là mặt dưới kem có một hàng giác hút). Ảnh "
               "mẫu duy nhất: concept đã duyệt. Cắt nền: `py -3 -I ArtGen/Spine/bach_tuoc.py cat_voi`. Rig dựng nó thành dải lưới 10 đốt "
               "cho hai xúc tu chống đẩy thân lên khỏi hố.", "",
               "Kiểm: thẳng tắp, nằm ngang, hai mép đối xứng qua trục giữa; không cong, không móc ở ngọn; viền kín; nền trắng tinh."]
        print(vt[0])
    if mn:
        gd += ["", "## Bạch tuộc con (chiêu cuối)", "",
               f"File prompt: `{Wp(mn[0])}` → lưu `{Wp(mn[1])}` (1536 × 1024, nền trắng: một bạch tuộc con hồng đỏ nhìn sang phải, một mắt, "
               "một gai mào, bốn xúc tu ngắn). Ảnh mẫu duy nhất: concept đã duyệt. Cắt nền: `py -3 -I ArtGen/Spine/bach_tuoc.py cat_con`."]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)
    print(hp)
    for x in L3:
        print(x[1])
    if mn:
        print(mn[0])


if __name__ == "__main__":
    main_non() if K == 1 else main()
