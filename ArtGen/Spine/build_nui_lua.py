# -*- coding: utf-8 -*-
"""Gói GPT vẽ khủng long núi lửa đảo Hỏa (mã làm việc nui_lua, con gốc của rig: monster_3654). Tướng thứ 10 đảo Hỏa, FINAL BOSS (suất
lan_hoa, ải 70).

Người dùng (2026-11-14): "concept khủng long núi lửa như con gốc ... con này final boss, cần làm thật đẹp, hoành tráng". Ba hướng màu dưới
đây là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ đặt, cỡ, thứ tự chồng từng part); hình là của mình.
Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (nui_lua_bo_cuc.py). Toạ độ trong prompt đọc từ inbox/nui_lua_1/mau/bo_cuc.json.

    py -3 -I ArtGen/Spine/nui_lua_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_nui_lua.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/nui_lua_1/luot_1_concept_<hướng>.txt [--note "..."]   (chạy nền hoặc < /dev/null)
"""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "nui_lua"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
GOLEM = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")
GIAC_MOC = os.path.join(HERE, "inbox", "giac_moc_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk():
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{K}")


def save_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "tai_ve")


def mau_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "mau")


def co(p):
    w, h = Image.open(p).size
    return f"{w}x{h}", f"{w} × {h}"


def hx(c):
    return "#%02X%02X%02X" % tuple(c)


def bx(b):
    return f"about x = {b[0]} to x = {b[2]}, y = {b[1]} to y = {b[3]}"


STANCE = ("STANCE (the same in the layout guide, image 1): a huge, very heavy FOUR-LEGGED armoured dinosaur, built low and wide like an "
          "ankylosaur, seen from the side and slightly from the front, facing the viewer's RIGHT. Its whole back is a mountain range: "
          "a big dark central peak with a crowd of leaning VOLCANO CHIMNEYS of different sizes growing out of the back, the rump, "
          "the shoulders and even the head. The massive head hangs LOW at the lower right, chin tucked, muzzle pointing down and to "
          "the right, like a bull about to charge; ONE eye is seen. Four short pillar legs are planted wide. No tail is visible. "
          "Angry, unstoppable, a walking erupting mountain: the final boss of a volcano island. Appealing and powerful, not horror, "
          "not gory, not a smiling cute mascot.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure fills {tat_ca}. Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into about fifty separate rigid pieces and animated with a 2D "
        "skeleton): calm, clean resting pose exactly as in the guide. Draw every piece as a clear, simple, closed shape with its "
        "own complete ink outline, so the pieces can be separated: EVERY single chimney (each keeps its own full outline even "
        "where another piece overlaps it) / every slab of the central peak / every flank boulder / the upper skull / the lower jaw "
        "/ each leg segment / each foot with its claws. Pieces overlap like stacked rocks; they do not melt into each other. NO "
        "smoke, NO flames, NO sparks, NO flying rocks, NO lava drops, NO glow, no ground, no props, no second character: smoke and "
        "fire are added later by the game.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram made of rough blobs: take ONLY the placement, the sizes, the overlaps and the kind "
        "of colour of each piece from it, never its line, its edge noise or its exact blob shapes. Design the real shape of every "
        "piece yourself as described: bold, chunky, faceted rock shapes with a clear silhouette and a rich but tidy amount of "
        "detail (a few big facet lines and chips per rock, not many tiny scratches), the way a carefully designed final-stage "
        "Pokemon-like legendary beast is drawn. Do not leave any piece as a plain empty blob. Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (facet lines, cracks, teeth, claws, the eye, the crater rims); every area coloured with coloured pencils and wax "
        "crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. "
        "Clean and appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no lighter top faces, no shadows of any kind (no cast shadow of one "
        "rock on another, no shadow under the figure or on the background), no white highlights or shine spots, no gloss, no "
        "reflections, NO GLOW and no halo around the lava, no rim light, NO GRADIENTS (the hot band at the top of a chimney is a "
        "flat colour band with a clean hand-drawn edge against the rock colour, never a soft blend), no 3D look. Lava is NOT "
        "luminous: it is simply an area of flat bright colour with an ink outline. The only exception: one tiny light dot in the "
        "eye. A different tone appears only where the design itself lists a different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the character.")

KHONG = ("FORBIDDEN: NO smoke, NO flames, NO fire in the air, NO tail, NO wings, NO crystals, NO gems, NO metal armour, NO chains, NO "
         "humanoid shape, NO standing upright, NO turtle shell, NO purple or pink colours, NO magenta lava.")

D = {
    "den": dict(
        ten="đá bazan đen than, dung nham cam lõi vàng, hàm dưới và móng màu ngà (kinh điển)",
        rock="charcoal basalt grey", dark="near-black basalt", lava="lava orange", core="golden yellow", bone="warm ivory bone",
        loai="BASALT VOLCANO DINOSAUR: its body is stacked blocks of charcoal-black basalt, its chimneys are filled with orange lava",
        them="NO blue, NO teal, NO green, NO brown rock."),
    "do": dict(
        ten="đá xỉ đỏ gạch, đỉnh lưng nâu sẫm, dung nham vàng lõi kem, hàm dưới và móng than",
        rock="brick-red volcanic scoria rock", dark="dark maroon-brown rock", lava="molten golden yellow", core="pale cream yellow",
        bone="charcoal black horn",
        loai="RED-ROCK VOLCANO DINOSAUR: its body is stacked blocks of brick-red scoria, its chimneys are filled with bright golden lava",
        them="NO blue, NO teal, NO green, NO grey rock."),
    "lam": dict(
        ten="đá phiến xám lam, đỉnh lưng lam sẫm, dung nham đỏ cam lõi vàng, hàm dưới và móng màu ngà (đá lạnh, lửa nóng)",
        rock="cool slate blue-grey rock", dark="dark navy-slate rock", lava="hot red-orange lava", core="golden yellow",
        bone="pale ivory bone",
        loai="SLATE VOLCANO DINOSAUR: its body is stacked blocks of cool blue-grey slate, its chimneys are filled with red-orange lava",
        them="NO green, NO brown rock, NO black rock."),
}

# Lượt 2 (2026-11-14, người dùng: "A đẹp nhưng nhìn hơi giống con gốc, sáng tạo hơn chút"): giữ bảng màu A, đổi THIẾT KẾ. Ba biến thể là
# đề xuất của Claude. Chỗ trống {…} điền trong body(): rock dark lava core bone mat mx my b_lung b_suon b_dau b_htren b_hduoi m11.
PEAK_MIENG = (
    "- MAIN VOLCANO ({b_lung}): the dinosaur's back is one big steep VOLCANO built from four or five huge overlapping slabs of "
    "{dark}; its blunt summit at about x = 700 to x = 850, y = 136 is cut open into the MAIN CRATER, the biggest crater of all: an "
    "ellipse about 135 px wide centred at about (772, 160), seen slightly from above, with a thick chipped rim and a pool of flat "
    "{core}. From the crater a broad river of flat {lava} runs down the front face of the mountain to about y = 430 and splits into "
    "three branches that end in pointed drips (one closed shape with an ink outline). Lower shoulders of rock step down to the "
    "right toward the head, with a few long facet lines. This dark mountain is the darkest area of the figure and makes the bright "
    "craters stand out.")
JAW_NGA = (
    "LOWER JAW ({b_hduoi}): a long, heavy jaw of {bone}, hinged at the upper left (about x = 850, y = 700) and reaching down and "
    "right to a blunt tip at about x = 1100, y = 890; along its upper edge a row of big SAW TEETH cut from the same piece; two or "
    "three chips and one crack. The mouth is slightly open: between the upper teeth and the saw teeth a wedge of flat {lava} (the "
    "throat) is visible.")
EYE = ("ONE fierce, narrow, slanted EYE at about ({mx}, {my}) under the brow: flat yellow iris ({mat}) with a thin dark slit pupil "
       "and one tiny light dot, set in a dark socket.")

D["giap"] = dict(
    ten="LƯỢT 2 · khủng long giáp: đá bazan đen + GIÁP XƯƠNG NGÀ (mũ xương, khiên hông, khiên vai, vảy sườn), ĐUÔI CHUỲ, đỉnh lưng là "
        "miệng núi lửa chính có sông dung nham, mỗi ống là một nón núi lửa nhỏ",
    rock="charcoal basalt grey", dark="near-black basalt", lava="lava orange", core="golden yellow", bone="warm ivory bone",
    loai="ARMOURED VOLCANO ANKYLOSAUR: a dinosaur of charcoal-black basalt wearing natural ivory BONE ARMOUR (a bone helmet, a hip "
         "shield, a shoulder shield, flank scutes, a bone tail club) and carrying a real VOLCANO on its back: one main crater "
         "mountain surrounded by a crowd of smaller crater cones",
    them="NO blue, NO teal, NO green, NO brown rock.",
    stance=STANCE.replace("No tail is visible.",
                          "A short thick TAIL sticks out behind the rump at the left and ends in a heavy bone club."),
    khong=KHONG.replace("NO tail, ", ""),
    tat_ca=[90, 68, 1259, 967],
    so_do=" In THIS guide the light ivory blobs are the bone armour (the helmet = upper skull, the horn stumps on it, the hip shield, "
          "the shoulder shield and flank scutes, the tail club at the far left) and the claws; the yellow ellipse on top of the dark "
          "central mountain is the main crater; the lower jaw is dark rock.",
    ong_ve="- HOW EVERY VOLCANO CONE IS DRAWN (there are about eighteen; called chimneys below; this is the key feature): NOT a pipe "
           "and NOT a smooth cylinder: a small steep VOLCANO CONE, clearly wider at its base, narrowing upward, then flaring a "
           "little into a thick chipped crater rim, like a tiny stratovolcano growing out of the animal's hide, leaning in its own "
           "direction. Its rock is {rock}, marked with three or four slightly curved horizontal STRATA lines (layers of old lava "
           "flows) and a few chips; no random lightning cracks. From the crater rim ONE long tongue of flat {lava} runs down one "
           "side of the cone and forks once near its end (a closed shape with an ink outline), with two short pointed drips beside "
           "it; there is NO continuous band of lava around the top. The very top is an OPEN CRATER MOUTH seen slightly from above: "
           "an ellipse with a thick chipped rim and inside it a pool of flat {core}. Every cone shows its crater mouth. Cones have "
           "different heights and widths.",
    peak=PEAK_MIENG,
    flank="- BONE ARMOUR (this is what makes this dinosaur its own animal): thick plates of {bone} grown over the rock like the "
          "armour of an ankylosaur. Each plate is one flat ivory shape with its full ink outline, a low keel ridge line down its "
          "middle, a chipped edge and two or three short cracks; no lava on the plates. They are: a big HIP SHIELD at about "
          "x = 331 to x = 570, y = 504 to y = 720 (a long rounded plate lying over the hip, under the rump cones); a SHOULDER "
          "SHIELD at about x = 613 to x = 785, y = 606 to y = 745 (a rounded pentagon); two overlapping FLANK SCUTES at about "
          "x = 731 to x = 981, y = 606 to y = 837, between the forelegs. The other body boulders between them stay {rock}, chunky "
          "and rounded, overlapping like stacked rocks. In the gaps under them the BELLY shows as narrow slivers of flat {lava}, "
          "outlined in ink.",
    head="- HEAD ({b_dau}), hanging low at the lower right, two separate pieces. BONE HELMET ({b_htren}): the whole upper skull is "
         "a thick helmet of {bone}, like the armoured head of an ankylosaur: a heavy angular block with a thick overhanging BROW "
         "ridge, a chipped edge and two cracks; its lower edge is a row of five or six big jagged teeth cut from the same bone, "
         "pointing down. " + EYE + " On top of the helmet stand three short thick HORN STUMPS of the same {bone}, hollow like "
         "broken-off horns, each open at the top with a small pool of flat {core} inside (they are vents too): two side by side at "
         "about x = 1060 to x = 1200, y = 470 to y = 640, and one lower at the right with its mouth at about {m11}. LOWER JAW "
         "({b_hduoi}): a long, heavy jaw of {rock}, hinged at the upper left (about x = 850, y = 700) and reaching down and right "
         "to a blunt tip at about x = 1100, y = 890; along its upper edge a row of big ivory SAW TEETH ({bone}); one forked lava "
         "crack on its side. The mouth is slightly open: between the upper teeth and the saw teeth a wedge of flat {lava} (the "
         "throat) is visible.",
    them_parts=["- TAIL (behind everything, at the far left, about x = 90 to x = 380, y = 520 to y = 700; shown in the guide): a "
                "short, thick tail of {rock} in three chunky stacked segments comes out from BEHIND the rump cones at about "
                "(380, 670), runs to the left and slightly up, tapering, and ends in a heavy two-lobed BONE CLUB of {bone} centred "
                "at about (150, 572), about 125 px wide and 100 px tall, with a chipped surface and one short forked crack of flat "
                "{lava}. The tail is behind the rump cones and behind the hind leg; it does not touch the ground."],
    pal="COLOURS (use exactly these, each area one flat colour): cone rock, body boulders, lower jaw, tail and legs {rock}; main "
        "volcano {dark}; lava tongues, drips, the main lava river, belly slivers, throat and hind-leg tips {lava}; crater pools "
        "{core}; eye ({mat}); bone helmet, horn stumps, hip shield, shoulder shield, flank scutes, tail club, all teeth and the "
        "front claws {bone}; every outline dark-brown ink (#2B2118). Only these colours.",
    kiem="mũ xương ngà trên đầu (hàm dưới là đá sẫm, răng ngà); khiên hông, khiên vai, vảy sườn màu ngà; đuôi ngắn có chuỳ xương ở "
         "bên trái; đỉnh lưng có miệng núi lửa lớn và sông dung nham chẻ ba; mỗi ống là nón núi lửa có vân tầng ngang, một lưỡi dung nham")

D["sung"] = dict(
    ten="LƯỢT 2 · khủng long sừng: đá bazan đen, HAI SỪNG HÚC ngà chĩa ra trước (mảnh thêm), đỉnh lưng là miệng núi lửa chính có sông "
        "dung nham, mỗi ống là một tháp vòng đá xếp tầng",
    rock="charcoal basalt grey", dark="near-black basalt", lava="lava orange", core="golden yellow", bone="warm ivory bone",
    loai="HORNED VOLCANO DINOSAUR: a charging dinosaur of charcoal-black basalt with TWO GREAT IVORY RAM HORNS like the brow horns "
         "of a triceratops, carrying a real VOLCANO on its back: one main crater mountain surrounded by a crowd of smaller tiered "
         "crater towers",
    them="NO blue, NO teal, NO green, NO brown rock.",
    tat_ca=[276, 68, 1352, 967],
    so_do=" In THIS guide the two curved ivory shapes at the right of the head are the two ram horns; the yellow ellipse on top of "
          "the dark central mountain is the main crater.",
    ong_ve="- HOW EVERY VOLCANO CHIMNEY IS DRAWN (there are about eighteen; this is the key feature): NOT a smooth pipe: a rough "
           "TIERED TOWER built from three or four thick rock RINGS stacked on top of each other, each ring a little narrower than "
           "the one below and slightly shifted, so that the outline is stepped like a stack of millstones, leaning in its own "
           "direction. The rings are {rock} with a few short facet lines and chips. In the seam between two rings a thin flat line "
           "of {lava} shows, and from the top seam two or three pointed drips of flat {lava} run down over the ring below (closed "
           "shapes with ink outlines). The top ring is the CRATER LIP: thick and chipped; inside it, seen slightly from above, an "
           "elliptical pool of flat {core}. Every chimney shows its crater mouth. Chimneys have different heights and widths; the "
           "small ones have only two rings. No random lightning cracks.",
    peak=PEAK_MIENG,
    flank="- FLANK ({b_suon}): along the side of the body, under the chimneys, a row of six chunky rounded BOULDERS of {rock} "
          "overlapping like armour scutes; each boulder carries ONE short blunt STUD of {bone} in its middle, like the bony knobs "
          "on a dinosaur's hide. In the gaps between and under the boulders the BELLY shows as flat {lava} (the creature is full "
          "of lava), outlined in ink; only narrow slivers of it are visible.",
    head="- HEAD ({b_dau}), hanging low at the lower right, lowered to ram. UPPER SKULL ({b_htren}): a heavy angular block of "
         "{rock} like the armoured skull of a dinosaur, with a thick overhanging BROW ridge; its lower edge is a row of five or six "
         "big jagged ROCK TEETH pointing down. " + EYE + " On top of the skull stand two short thick tiered chimneys side by side "
         "(mouths at about x = 1060 to x = 1200, y = 470 to y = 640). TWO GREAT RAM HORNS of {bone} (shown in the guide; the star "
         "of the design): they grow from the brow at the right side of the skull and sweep FORWARD to the right and then upward, "
         "like the brow horns of a triceratops, built for ramming. The NEAR horn: its base, about 65 px thick, sits on the front of "
         "the skull at about (1175, 660); it curves out to the right and up to a sharp tip at about (1350, 515). The FAR horn: "
         "slimmer, behind the head, only its outer half visible, from about (1220, 550) to a sharp tip at about (1295, 450). Each "
         "horn is one flat ivory shape with its full ink outline, three or four curved ring grooves near the base and one chip; no "
         "lava on the horns. " + JAW_NGA,
    pal="COLOURS (use exactly these, each area one flat colour): chimney rings, flank boulders, skull and legs {rock}; main volcano "
        "{dark}; lava seams, drips, the main lava river, belly slivers, throat and hind-leg tips {lava}; crater pools {core}; eye "
        "({mat}); the two ram horns, the boulder studs, the lower jaw and the front claws {bone}; every outline dark-brown ink "
        "(#2B2118). Only these colours.",
    kiem="hai sừng ngà cong chĩa ra trước rồi vểnh lên ở bên phải đầu (sừng gần to, sừng xa lấp sau đầu); đỉnh lưng có miệng núi lửa "
         "lớn và sông dung nham chẻ ba; mỗi ống là tháp 3–4 vòng đá xếp tầng, dung nham ở khe giữa các vòng; tảng sườn có núm xương")

D["cot"] = dict(
    ten="LƯỢT 2 · cột bazan: cả con dựng bằng CỘT BAZAN LỤC GIÁC (như ghềnh đá cột biết đi), mỗi ống là một bó cột cao thấp so le, dung "
        "nham ở khe thẳng giữa các cột",
    rock="blue-black basalt", dark="near-black basalt", lava="lava orange", core="golden yellow", bone="warm ivory bone",
    loai="COLUMNAR-BASALT VOLCANO DINOSAUR: its whole body is built from HEXAGONAL BASALT COLUMNS, as if a sea cliff of six-sided "
         "stone pillars got up and walked; flat orange lava shows in the straight joints between the columns",
    them="NO teal, NO green, NO brown rock. The columns are matte rock, NOT glassy crystals.",
    ong_ve="- HOW EVERY VOLCANO CHIMNEY IS DRAWN (there are about eighteen; this is the key feature): NOT a round pipe: a BUNDLE of "
           "four to six HEXAGONAL BASALT COLUMNS fused side by side, of unequal heights so that the top is STEPPED like organ pipes, "
           "the whole bundle leaning in its own direction. Each column is a long straight six-sided prism of {rock}: two or three "
           "of its flat faces are seen, separated by long straight edge lines, and on top its flat HEXAGON face seen slightly from "
           "above. The one or two tallest columns in the middle of the bundle are hollow: their hexagon top is an open crater with "
           "a thick rim and a hexagonal pool of flat {core}. The upper tenth of every column is a band of flat {lava} with a "
           "straight, slightly chipped lower edge. In two or three of the straight joints between columns a thin straight seam of "
           "flat {lava} runs down half the length. A few columns are cracked across (one short horizontal line). No random "
           "lightning cracks, no drips, no round pipes. Bundles have different heights and widths; the small ones have only three "
           "columns.",
    peak="- CENTRAL CLIFF ({b_lung}): the dinosaur's back is one big steep cliff of tall hexagonal columns of {dark} standing side "
         "by side in four or five overlapping groups; their flat hexagon tops form a STAIRCASE skyline that climbs to the blunt "
         "summit at about x = 700 to x = 900, y = 136 to y = 420 and steps down to the right toward the head. Long straight "
         "vertical joints, two or three thin straight lava seams; no crater on it. It is the darkest area of the figure and makes "
         "the bright chimneys stand out.",
    flank="- FLANK ({b_suon}): along the side of the body, under the chimneys, a row of six big, thick HEXAGONAL SLABS of {rock} "
          "(short column ends) overlapping like armour scutes, each with a clear six-sided outline and one smaller hexagon line "
          "inside. In the straight gaps between and under them the BELLY shows as flat {lava}, outlined in ink; only narrow "
          "slivers of it are visible.",
    head="- HEAD ({b_dau}), hanging low at the lower right, two separate pieces. UPPER SKULL ({b_htren}): a heavy angular block of "
         "{rock} built from a few big flat hexagon facets; its BROW ridge is a ledge of three short column stubs sticking forward; "
         "its lower edge is a row of five or six blunt square ROCK TEETH (short column ends) pointing down. " + EYE + " On top of "
         "the skull stand two short thick column bundles side by side like horns (mouths at about x = 1060 to x = 1200, y = 470 to "
         "y = 640) and a small one at the right (mouth at about {m11}). " + JAW_NGA,
    kiem="mỗi ống là bó 4–6 cột lục giác cao thấp so le, mặt trên lục giác, cột giữa rỗng có lõi vàng; đỉnh lưng là vách cột bậc "
         "thang; tảng sườn là phiến lục giác; khe dung nham thẳng, không có vết nứt ngoằn ngoèo")


def refs(kieu):
    c1, v1 = co(os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"))
    c2, v2 = co(GOLEM)
    c3, v3 = co(GIAC_MOC)
    c4, v4 = co(WORLD_STYLE)
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         f"LAYOUT GUIDE, {c1}, white background: a flat computer-made diagram of THIS creature in its resting stance, built from "
         "rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (many leaning "
         "chimney blobs, each with a bright band and a bright ellipse = its crater mouth at the top; the big dark central peak; "
         "the row of flank boulders; the low head at the lower right with one eye, a light-coloured lower jaw with saw teeth; four "
         "legs, the two front feet with light claws). Use it for placement, size, overlap and colour family only; design and "
         "redraw everything in the hand-drawn style of the approved heroes." + D[kieu].get("so_do", ""),
         f"Sơ đồ bố cục tự dựng bằng mã ({v1}, nền trắng): các khối tô phẳng (nhiều ống núi lửa nghiêng, mỗi ống có dải dung nham và "
         "elip miệng ở đỉnh; đỉnh núi sẫm ở giữa; hàng tảng đá sườn; đầu cúi thấp ở dưới phải có một mắt, hàm dưới màu sáng có răng "
         "cưa; bốn chân, hai bàn chân trước có móng). Lấy chỗ đặt, cỡ, thứ tự chồng, họ màu"),
        (GOLEM,
         f"an approved hero of the same game and the same fire island (a stone golem with fire), {c2}, white background: match "
         "EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring (see how its rocks "
         "are one flat colour with a few facet lines, and how its fire is flat colour bands, not gradients), its bold chunky "
         "shapes and its fierce battle-ready eye. Do NOT copy its species, its design or its colours.",
         f"Golem lửa đã duyệt ({v2}, nền trắng): người đá có lửa. Lấy nét bút rung, vân sáp, tô phẳng, cách vẽ đá một màu với vài "
         "nét cạnh, mắt chiến"),
        (GIAC_MOC,
         f"another approved hero of the same game (a big four-legged horned forest beast), {c3}, white background: the same line "
         "and flat crayon colouring; see how its thick four legs, broad feet and claws are drawn. Do NOT copy its species, "
         "design or colours.",
         f"Giác Mộc đã duyệt ({v3}, nền trắng): thú bốn chân to. Lấy nét, tô phẳng, cách vẽ bốn chân và móng"),
        (WORLD_STYLE,
         f"the game's hand-drawn map, {c4}: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / wax "
         "crayon hatching), nothing of its content.",
         f"Bản đồ vẽ tay đã duyệt ({v4}): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


def body(kieu, C, Hh):
    d = D[kieu]
    O = Hh["ong"]
    rock, dark, lava, core, bone = (f"{d['rock']} ({hx(C['da'])})", f"{d['dark']} ({hx(C['da_dam'])})", f"{d['lava']} ({hx(C['nham'])})",
                                    f"{d['core']} ({hx(C['loi'])})", f"{d['bone']} ({hx(C['xuong'])})")

    def ong(k):
        o = O[k]
        return (f"from its base at about ({o['day'][0]}, {o['day'][1]}) up to its crater mouth at about ({o['mieng'][0]}, "
                f"{o['mieng'][1]}), about {o['rong']} px wide and {o['dai']} px long")

    L = [
        f"- HOW EVERY VOLCANO CHIMNEY IS DRAWN (there are about eighteen; this is the key feature): a thick, slightly tapering, "
        f"FACETED rock column like a broken basalt pillar or a small steep cone, leaning in its own direction. The lower four "
        f"fifths are {rock} with two or three long facet lines and ONE or TWO bold forked LAVA CRACKS (flat {lava}, each crack a "
        f"closed jagged shape like a small lightning bolt or a river with two branches, outlined in ink). The top fifth is a hot "
        f"band of flat {lava} with a ragged, dripping lower edge (three or four pointed drips running down the column). The very "
        f"top is an OPEN CRATER MOUTH seen slightly from above: an ellipse with a thick chipped rim, and inside it a pool of flat "
        f"{core}. Every chimney shows its crater mouth. Chimneys are different heights and widths; none is a perfect cylinder.",
        f"- TWO GIANT REAR CHIMNEYS (the tallest pieces, at the upper left, {bx(Hh['ong_lung_sau'])}): the biggest one {ong('09')}, "
        f"standing almost upright; beside it on the left a slimmer one {ong('10')}, leaning a little to the left.",
        f"- MIDDLE CHIMNEY in front of the central peak: {ong('02')}, leaning to the RIGHT; a short stubby one below it with its "
        f"mouth at about ({O['01']['mieng'][0]}, {O['01']['mieng'][1]}).",
        f"- THREE FAR CHIMNEYS behind the central peak at the upper right ({bx(Hh['ong_lung_xa'])}), partly hidden by the peak, "
        f"fanning out to the right: one {ong('15')}; one {ong('14')}; the lowest {ong('13')}.",
        f"- RUMP CHIMNEYS at the left ({bx(Hh['ong_mong'])}): five smaller chimneys fanning out to the left like the spikes of a "
        f"stegosaur, mouths at about ({O['03']['mieng'][0]}, {O['03']['mieng'][1]}), ({O['04']['mieng'][0]}, {O['04']['mieng'][1]}), "
        f"({O['06']['mieng'][0]}, {O['06']['mieng'][1]}), ({O['07']['mieng'][0]}, {O['07']['mieng'][1]}) and, lowest, pointing "
        f"left, ({O['08']['mieng'][0]}, {O['08']['mieng'][1]}).",
        f"- CENTRAL PEAK ({bx(Hh['lung'])}): the dinosaur's back is one big steep MOUNTAIN PEAK built from four or five huge "
        f"overlapping slabs of {dark}, the tallest slab a blunt summit at about x = 700 to x = 900, y = 136 to y = 420, lower "
        f"shoulders of rock stepping down to the right toward the head. Plain dark rock with a few long facet lines and two or "
        f"three thin lava cracks; no crater on it. It is the darkest area of the figure and makes the bright chimneys stand out.",
        f"- FLANK ({bx(Hh['da_suon'])}): along the side of the body, under the chimneys, a row of six chunky rounded BOULDERS of "
        f"{rock} overlapping like armour scutes. In the gaps between and under them the BELLY shows as flat {lava} (the creature "
        f"is full of lava), outlined in ink; only narrow slivers of it are visible.",
        f"- HEAD ({bx(Hh['dau'])}), hanging low at the lower right, two separate pieces. UPPER SKULL ({bx(Hh['ham_tren'])}): a heavy "
        f"angular block of {rock} like the armoured skull of a dinosaur, with a thick overhanging BROW ridge; its lower edge is a "
        f"row of five or six big jagged ROCK TEETH pointing down. ONE fierce, narrow, slanted EYE at about ({Hh['mat'][0]}, "
        f"{Hh['mat'][1]}) under the brow: flat {core.split(' (')[0]} iris ({hx(C['mat'])}) with a thin dark slit pupil and one tiny "
        f"light dot, set in a dark socket. On top of the skull stand TWO short thick chimneys side by side like horns (mouths at "
        f"about x = 1060 to x = 1200, y = 560 to y = 640), and two or three small ones behind them (mouths at about "
        f"({O['12']['mieng'][0]}, {O['12']['mieng'][1]}) and ({O['11']['mieng'][0]}, {O['11']['mieng'][1]})). LOWER JAW "
        f"({bx(Hh['ham_duoi'])}): a long, heavy jaw of {bone}, hinged at the upper left (about x = 850, y = 700) and reaching down "
        f"and right to a blunt tip at about x = 1100, y = 890; along its upper edge a row of big SAW TEETH cut from the same "
        f"piece; two or three chips and one crack. The mouth is slightly open: between the rock teeth and the saw teeth a wedge of "
        f"flat {lava} (the throat) is visible.",
        f"- LEGS (four short, very thick pillar legs, each built from two or three stacked blocks of {rock} with one lava crack). "
        f"NEAR FORELEG in the middle foreground ({bx(Hh['chan_truoc_gan'])}): its shoulder block carries one short chimney "
        f"(mouth at about ({O['P_qiantuiR5']['mieng'][0]}, {O['P_qiantuiR5']['mieng'][1]})); it ends in a broad foot with THREE "
        f"big blunt CLAWS of {bone} ({bx(Hh['mong_truoc_gan'])}). FAR FORELEG at the lower right under the head "
        f"({bx(Hh['chan_truoc_xa'])}), with three claws of the same colour ({bx(Hh['mong_truoc_xa'])}). NEAR HIND LEG at the far "
        f"left ({bx(Hh['chan_sau_gan'])}): a bent pillar ending in a blunt stone peg whose lowest part is flat {lava} with a ragged "
        f"upper edge, like a rock dipped in lava; a short chimney on its hip. FAR HIND LEG between them, mostly hidden "
        f"({bx(Hh['chan_sau_xa'])}), ending the same way.",
    ]
    PAL = (f"COLOURS (use exactly these, each area one flat colour): chimney columns, flank boulders, skull and legs {rock}; central "
         f"peak {dark}; hot bands, lava cracks, belly slivers, throat and hind-leg tips {lava}; crater pools {core}; eye "
         f"({hx(C['mat'])}); lower jaw and front claws {bone}; every outline dark-brown ink (#2B2118). Only these colours. "
         f"{d['them']}")
    fm = dict(rock=rock, dark=dark, lava=lava, core=core, bone=bone, mat=hx(C["mat"]), mx=Hh["mat"][0], my=Hh["mat"][1],
              b_lung=bx(Hh["lung"]), b_suon=bx(Hh["da_suon"]), b_dau=bx(Hh["dau"]), b_htren=bx(Hh["ham_tren"]),
              b_hduoi=bx(Hh["ham_duoi"]), m11=f"({O['11']['mieng'][0]}, {O['11']['mieng'][1]})")
    for i, k in ((0, "ong_ve"), (5, "peak"), (6, "flank"), (7, "head"), (8, "legs")):
        if k in d:
            L[i] = d[k].format(**fm)
    L += [t.format(**fm) for t in d.get("them_parts", ())]
    if "pal" in d:
        PAL = d["pal"].format(**fm) + " " + d["them"]
    return "\n".join(L), PAL


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    sys.path.insert(0, HERE)
    import nui_lua_bo_cuc as BC
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    Hh = json.load(open(os.path.join(mau_dir(), "bo_cuc.json"), encoding="utf-8"))
    gd = [f"# Gói gửi GPT: `{CODE}` (khủng long núi lửa, tướng thứ 10 đảo Hỏa, FINAL BOSS, suất `lan_hoa`, tên chưa đặt)", "",
          "Làm 2026-11-14: dựng trên rig của con gốc `monster_3654` (thú đá lưng mọc ống núi lửa, 75 xương, 51 mảnh cứng). Người dùng dặn: "
          "concept khủng long núi lửa như con gốc; final boss, thật đẹp, hoành tráng. Ba hướng màu là đề xuất của Claude, chờ người dùng "
          "chọn. Khói, lửa KHÔNG vẽ trong concept (game thêm). Ghi chú: `ArtGen/Spine/inbox/nui_lua_ghichu.md`.", "",
          "LƯỢT 2 (cùng ngày): người dùng xem ba hướng màu, nói \"A đẹp nhưng nhìn hơi giống con gốc, sáng tạo hơn chút\". Thêm ba biến "
          "thể giữ bảng màu A, đổi thiết kế: `giap` (giáp xương ngà, đuôi chuỳ), `sung` (hai sừng húc), `cot` (cột bazan lục giác). "
          "Đuôi chuỳ và hai sừng là MẢNH THÊM ngoài 51 mảnh của rig (gắn xương mới khi dựng).", "",
          "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        BODY, PAL = body(kieu, BC.HUONG[kieu], Hh)
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              f"CREATURE: a {d['loai']}. A legendary fire-element beast, the FINAL BOSS of a volcano island in a monster-collecting "
              "game: a gigantic four-legged armoured dinosaur whose back is a living volcano range, a crowd of rock chimneys with "
              "open crater mouths. It is an animal made of rock, NOT a human, NOT a golem standing upright, NOT a turtle, NOT a "
              "dragon with wings.", "", d.get("stance", STANCE), "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). The viewer's LEFT "
              "side of the picture is the creature's rear; the viewer's RIGHT is where it faces. NEAR = the side of the body "
              "toward the viewer; FAR = the other side.", "",
              "PARTS:", BODY, "", d.get("khong", KHONG), "", PAL, "", FRAME.format(tat_ca=bx(d.get("tat_ca", Hh["_tat_ca"]))), "", POSE, "", SOFT, "", LINE, "", FLAT,
              "", BG]
        ghi(p, t)
        print(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"- File prompt: `{Wp(p)}`", f"- Ảnh lưu: `{Wp(out)}` (trùng tên thì `_2`, `_3`…)", "- Ảnh mẫu:"]
        gd += [f"  {i}. `{Wp(r)}`: {vi}." for i, (r, _, vi) in enumerate(R, 1)]
        if "kiem" in d:
            gd += [f"- Kiểm riêng: {d['kiem']}."]
        gd += [""]
    gd += ["## Cách kiểm", "",
           "- Đúng bố cục sơ đồ: thú bốn chân thấp, rộng, nhìn sang PHẢI; đầu cúi thấp ở dưới phải; hai ống cao nhất ở trên trái; đỉnh núi "
           "sẫm ở giữa; ba ống xa ngả sang phải; năm ống nhỏ xoè ra sau mông.",
           "- Mỗi ống núi lửa: cột đá có cạnh, dải dung nham PHẲNG ở đỉnh có mép nhỏ giọt, miệng núi lửa hình elip có lõi; có vết nứt "
           "dung nham chẻ nhánh. KHÔNG khói, KHÔNG lửa, KHÔNG phát sáng, KHÔNG chuyển màu mềm.",
           "- Đầu: sọ đá có gờ mày, MỘT mắt xếch dữ, hàng răng đá; hàm dưới màu khác có răng cưa; miệng hé thấy họng dung nham.",
           "- Hai bàn chân trước mỗi bàn ba móng; hai chân sau là trụ đá đầu nhúng dung nham.",
           "- Nét bút mực nâu hơi rung, vân chì sáp, không bóng, không điểm sáng trắng; nền trắng tinh, không viền sticker.", "",
           "## Câu sửa nhanh", "",
           "- Có khói / lửa: `--note \"Remove all smoke and flames: only rock, flat lava bands and crater pools.\"`",
           "- Dung nham phát sáng / chuyển màu: `--note \"Lava must be FLAT colour with an ink outline: no glow, no gradient.\"`",
           "- Lệch bố cục: `--note \"Follow the layout guide exactly: same placement and size of every piece, do not move or enlarge.\"`",
           "- Đầu không rõ: `--note \"Make the head clearer: heavy rock skull with a brow ridge, one fierce slanted eye, rock teeth, a "
           "separate lower jaw with saw teeth.\"`", ""]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    print(os.path.join(pk(), "HUONG_DAN.md"))


# ================================================================ LƯỢT 2: tờ MẢNH theo khung part (sau khi duyệt concept "sừng")
CON = ("a huge four-legged volcano dinosaur of charcoal-black basalt with two great ivory ram horns; its back carries a main crater "
       "mountain and a crowd of tiered crater towers")
LOAI = {
    "ong": "a VOLCANO CHIMNEY from the creature's back: a TIERED TOWER of thick stacked rock rings of charcoal basalt (#56505C). "
           "The orange (#F07828) lines across it are the lava seams between two rings; the orange cap at one end is the CRATER "
           "LIP with its pointed lava drips running down; the yellow (#FACC50) ellipse inside the cap is the lava pool of the "
           "crater mouth. Keep all of these exactly where they are. On each rock ring add two or three short facet lines and a "
           "chip, as on the towers of image 1",
    "ong_chan": "a LEG BLOCK of charcoal basalt (#56505C) that carries one short volcano chimney: the orange (#F07828) cap is the "
                "crater lip with its drips, the yellow (#FACC50) ellipse is the lava pool, the orange lines are lava seams. Keep "
                "them exactly; add a few facet lines and chips on the rock",
    "da": "a ROCK BOULDER of the body or of a leg: plain charcoal basalt (#56505C), chunky and faceted: three or four facet lines "
          "and one or two chips, as the boulders of image 1. No lava on it",
    "da_num": "a ROCK BOULDER of the flank: charcoal basalt (#56505C) with a few facet lines; the small ivory (#E4CEA4) shape on "
              "it is a short curved BONE THORN growing out of the rock (like a rose thorn, sharp tip, wider base): keep it where "
              "it is and at that size, give it its own ink outline and one tiny curved ring line near its base",
    "vo": "a curved ROCK SHELL (a rib-like armour plate of the belly): charcoal basalt (#56505C) with a few facet lines; where the "
          "guide shows orange (#F07828) along its inner edge, that is lava showing: keep it flat orange with an ink line between "
          "rock and lava",
    "vo_num": "a curved ROCK SHELL of the flank: charcoal basalt (#56505C) with a few facet lines; orange (#F07828) areas are lava: "
              "keep them; the small ivory (#E4CEA4) shape is a short curved BONE THORN (sharp tip, wider base): keep it where it "
              "is, with its own ink outline and one tiny ring line near its base",
    "chan_nhung": "a HIND FOOT: a thick pillar of charcoal basalt (#56505C) with a few facet lines; its end is dipped in lava: the "
                  "orange (#F07828) band with the zigzag edge. Keep the band and its zigzag edge exactly",
    "long": "a piece of the creature's LAVA BELLY that shows in the gaps between the rocks: plain flat lava orange (#F07828) with "
            "loose crayon hatching only. No rock, no lines inside, no drips",
    "lung": "a huge SLAB of the back mountain: near-black basalt (#36323C), the darkest rock of the creature: three to five long "
            "facet lines and a few chips, as on the dark mountain of image 1. No lava",
    "dinh": "the MAIN VOLCANO, the summit slab of the back: near-black basalt (#36323C) with long facet lines. At its top the MAIN "
            "CRATER: an orange (#F07828) chipped lip around a yellow (#FACC50) lava pool; from it a river of flat orange lava runs "
            "down and forks into three branches ending in pointed drips. Keep the crater and the river exactly where they are",
    "so": "the UPPER SKULL (the head without the lower jaw), of charcoal basalt (#56505C). Its jagged lower edge is a row of big "
          "ROCK TEETH. The yellow slanted EYE with the thin dark slit pupil and the tiny light dot: keep it EXACTLY as drawn (same "
          "place, size, tilt) and add a heavy angry BROW ridge line just above it. The near-black block beside the eye is the "
          "dark inside of the mouth behind the teeth: keep it flat near-black (#36323C). The two rounded lobes at the top are the "
          "rocky bumps of the forehead where the horns grow: plain rock, NO craters, NO circles, NO lava on them. Elsewhere a few "
          "big facet lines and chips",
    "ham": "the LOWER JAW: warm ivory bone (#E4CEA4), heavy, with a row of big SAW TEETH cut from the same piece; three or four "
           "chips and one or two cracks, as the jaw of image 1",
    "rang_xa": "the FAR ROW OF SAW TEETH of the lower jaw: warm ivory bone (#E4CEA4), a few chips and one crack",
    "hong": "the FIRE IN THE THROAT: a flat lava-orange (#F07828) blob with a flat yellow (#FACC50) centre, an ink line between "
            "them. No glow",
    "sung": "a great RAM HORN: warm ivory bone (#E4CEA4), curved, sharp at the tip, thick and rounded at the base; the ink lines "
            "across it near the base are ring grooves: keep them, slightly curved; add one small chip. No lava",
    "mong": "a FOOT TIP WITH CLAWS: warm ivory bone (#E4CEA4): each bump of the silhouette is one big blunt claw; separate the "
            "claws with ink lines running in from the notches; one short crack",
}
TEN_TO = {"O1": "năm ống núi lửa lớn", "O2": "tám ống núi lửa nhỏ + hai tảng đá nhỏ", "L": "đỉnh núi lửa chính + năm phiến lưng",
          "D": "sọ trên, hàm dưới, hàng răng xa, lửa họng, hai sừng, hai bàn móng", "B": "lòng bụng dung nham + sáu vỏ sườn",
          "C1": "mười mảnh hai chân gần", "C2": "sáu mảnh hai chân xa",
          "S": "tờ SỬA: sọ (bỏ hai miệng ống trên trán) + bốn tảng sườn có gai xương; đè lên bản ở tờ D, C1, B"}


def build_manh():
    sys.path.insert(0, HERE)
    import nui_lua_manh as M
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có " + duyet)
    cd, vd = co(duyet)
    gd = ["", "## Lượt 2: MẢNH theo khung part của rig (sau khi người dùng chốt concept `sung`, 2026-11-14)", "",
          f"Mỗi tờ: ảnh 1 = concept đã duyệt `{Wp(duyet)}` ({vd}, nền trắng: khủng long đá đen hai sừng ngà, ống núi lửa xếp tầng; lấy "
          "nét, màu, vân sáp), ảnh 2 = tờ hướng dẫn tự dựng bằng mã (1536 × 1024, nền trắng, các hình bóng tô phẳng viền nâu sẫm). Máy "
          "vẽ lại sạch, GIỮ NGUYÊN hình bóng. Claude cắt bằng `nui_lua_manh.py cat_part <tờ>` (đo IoU, dưới 0,9 thì gen lại).", ""]
    for to in M.TO:
        pj = os.path.join(mau_dir(), f"part_{to}.json")
        if not os.path.exists(pj):
            raise SystemExit("chưa có tờ hướng dẫn " + pj)
        Kh = json.load(open(pj, encoding="utf-8"))
        z = next(iter(Kh.values()))["z"]
        net_px = max(4, int(round(M.M.NET * z)))
        g_im = os.path.join(mau_dir(), f"part_{to}.png")
        out = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_2_manh_{to}.txt")
        nh = {}
        for ten, v in sorted(Kh.items(), key=lambda q: (q[1]["y"] // 120, q[1]["x"])):
            nh.setdefault(M.loai(ten), []).append(f"({v['x'] + v['w'] // 2}, {v['y'] + v['h'] // 2})")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, {cd}, white background: {CON}. It gives the design, the colours, the "
             "wobbly dark-brown ink line, the crayon hatching and the look of every material (rock, lava, ivory bone).",
             f"image 2 = {Wp(g_im)}: PARTS GUIDE, 1536x1024, white background, drawn by computer: {len(Kh)} separate flat shapes, each "
             "one a PART of the creature's 2D animation rig, enlarged, lying at the angle the rig needs. Each shape is the EXACT "
             "silhouette of its part, filled with the flat colours of its materials and outlined in dark brown.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.", "",
             "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep "
             "EXACTLY every silhouette of image 2: the same outline, the same size, the same angle, the same position on the sheet "
             "(if your picture were laid over image 2, every shape must coincide with its shape there). Do not move, rotate, "
             "straighten, merge or rearrange the shapes; do not add or drop any; keep clear white between them. A program will cut "
             "this sheet by position.", "",
             "WHAT THE SHAPES ARE (centre of each shape in pixels on the sheet, x from the left, y from the top):"]
        for lo, cho in nh.items():
            t.append(f"- {LOAI[lo]}: {len(cho)} shape{'s' if len(cho) > 1 else ''}, centred at about " + ", ".join(cho) + ".")
        t += ["",
              f"OUTLINE: every shape gets ONE closed dark-brown ink outline (#2B2118), about {net_px} px thick on this sheet, wobbly "
              "like a real pen, lying just INSIDE the edge of the silhouette (never outside it). Inner lines (facet lines, chips, "
              f"cracks, the lines between two colours) are thinner (about {max(2, net_px // 2)} px).",
              "COLOUR: keep the colour each shape has in image 2, and keep every second colour exactly where image 2 shows it. Fill "
              "every area with visible loose diagonal crayon / coloured-pencil hatching as in image 1, kept inside the outline.",
              "Each shape is a complete, closed object on its own: do not draw neighbouring parts, do not draw the creature, do not "
              "add smoke, flames or sparks.", "",
              "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
              "darker side, no lighter top faces, no highlights or shine spots (not on the horns, not on the claws, not on the "
              "lava), NO GLOW around the lava, NO GRADIENTS (two colours always meet at a clean inked edge), no cast shadows, no 3D "
              "look. Pure white (#FFFFFF) background; no text, no labels, no numbers, no frames, no guide lines."]
        ghi(p, t)
        print(p)
        gd += [f"- Tờ `{to}` ({TEN_TO[to]}; phóng {z} lần, nét ~{net_px} px): **chỉ gửi GPT đường dẫn** `{Wp(p)}` → `{Wp(out)}`; ảnh 2 = "
               f"`{Wp(g_im)}` ({len(Kh)} ô)."]
    gd += ["", "Kiểm: hình bóng trùng tờ hướng dẫn (IoU ≥ 0,9 mới lắp); mỗi vùng một màu phẳng; dung nham không phát sáng; con mắt trên "
           "sọ còn đúng chỗ (hỏng thì `nui_lua_manh.py mat` dán lại bằng mã); sừng có rãnh vòng ở gốc.", ""]
    pg = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(pg, encoding="utf-8").read().split("\n## Lượt 2: MẢNH")[0].rstrip("\n")
    ghi(pg, [cu] + gd)
    print(pg)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manh":
        build_manh()
    else:
        main()
