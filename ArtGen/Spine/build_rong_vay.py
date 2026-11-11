"""Gói GPT vẽ concept rồng vây (tướng thứ 8 đảo Thủy, 2026-11-11). Mã làm việc: rong_vay (tên chưa đặt).

Người dùng: reskin con gốc monster_3458 (game tham khảo) theo đúng cách tách mảnh của nó, gen trước, animation tính sau. Người dùng
không dặn màu, chi tiết: thiết kế dưới đây là ĐỀ XUẤT của Claude, chờ duyệt concept. Chỉ lấy cách dựng (dáng, chỗ đặt, thứ tự chồng
của 34 mảnh); hình là của mình: rồng biển kiểu cá chuồn, thân chàm tím, bụng kem, vây và màng cánh lam xám trầm có tia vây chàm sẫm,
sừng màu cát, giáp vỏ sò, đốm kem trên cánh, mắt hổ phách; không lông, không lông vũ, không vân sáng, không mây.
Không đính ảnh con gốc vào prompt; đính sơ đồ bố cục tự dựng bằng mã (rong_vay_bo_cuc.py). Mổ xẻ con gốc: inbox/rong_vay_ghichu.md.

    py -3 -I ArtGen/Spine/rong_vay_bo_cuc.py
    py -3 -I ArtGen/Spine/build_rong_vay.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rong_vay_1/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "rong_vay"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
SNAKE = os.path.join(HERE, "inbox", "ran_sung_1", "tai_ve", "L1_duyet.png")   # rắn sừng dạng 1 đã duyệt: nét, vạch bụng, mắt
DROP = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")     # Tí Tách dạng 1 đã duyệt: nét rung, tô phẳng


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def guide(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau", "bo_cuc.png")


PALETTE = ("COLOURS, a calm, MUTED palette (use exactly these, each area one flat colour): back and sides of the whole body, "
           "the head and the neck deep indigo blue (#34408F); the brow ridge darker indigo (#242C68); belly plates (throat, "
           "chest and the whole underside of the body) warm cream (#F3E6C4), with thin ink lines between the plates; every "
           "fin web and both wing membranes a soft DUSTY GREY-TEAL (#6A9BA8), low in saturation, never bright turquoise or "
           "cyan; every fin ray and both wing spars DARK NAVY (#242C68); both horns and the beak CHARCOAL BLACK (#26252C), flat matte black, with at most two or three short dark-grey (#5A5866) lines on each (ring lines near the horn base, the mouth line on the beak); the "
           "scallop shells and the wing spots pale cream (#FAF0D6), shell ribs soft ochre (#C99A55); the eye amber (#F2B33D) "
           "with a dark vertical pupil and ONE tiny white dot; every outline dark-brown ink (#2B2118). Only these colours. "
           "NO orange, NO coral, NO red, NO bright turquoise anywhere: apart from the small amber eye the whole creature "
           "is cool blues, cream and black; sand ochre appears only on the shell ribs. No white fur, no glowing lines.")

FORM = ("CREATURE: a WINGED SEA-SERPENT DRAGON of the water element for a monster-collecting game, built like a flying fish "
        "grown into a dragon: a long, thick serpent body coiled in one loop, two long FIN-WINGS (the pectoral fins of a flying "
        "fish, with fin rays), ray-finned sails along its back and a forked fish tail. It hovers in the air. A proud, fierce, "
        "battle-ready beast with grown-up proportions (small head, long powerful body), appealing but NOT a chibi mascot. "
        "A rich, readable design. Everything on it is fish and sea material: scales plates, fin webs with rays, horn, shell. "
        "It has NO fur, NO feathers, NO hair, NO mane, NO whiskers, NO legs, NO arms.\n"
        "Follow the LAYOUT GUIDE (the image called LAYOUT GUIDE in the list above) closely for the construction, the placement, the size and the overlap order of "
        "every part listed here:\n"
        "- VIEW: side view. The head is at the upper RIGHT and faces the viewer's RIGHT, chin slightly raised; the big body "
        "loop is at the LEFT; the two wings hang downward.\n"
        "- HEAD (about 270 px wide with the beak, small compared with the body): a compact, smooth reptile head, indigo. A "
        "SHORT BLUNT MUZZLE ending in a small charcoal-black horn BEAK like a sea turtle's: an upper part with a little hooked "
        "tip and a smaller lower part, mouth closed, one short mouth line. ONE visible EYE, large for the head (about 45 px "
        "wide), almond shaped, amber with a dark vertical slit pupil and one tiny white dot, set under a dark pointed BROW "
        "RIDGE that gives it a determined, fierce look. No nostril detail needed, no teeth showing.\n"
        "- HORNS: TWO smooth charcoal-black horns grow from the top back of the head and sweep back toward the upper LEFT, "
        "gently curved and pointed like the horns of an antelope: a front one standing more upright (about 120 px long) and a "
        "longer one behind it (about 190 px long, lower, more horizontal). Plain smooth horn, one or two short ring lines near the base. Not "
        "feathers, not antlers, no branches.\n"
        "- HEAD FINS: behind the cheek a BIG WEBBED EAR-FIN points back to the LEFT (about 200 px long): a dusty grey-teal web "
        "stretched on three dark-navy rays, its rear edge scalloped between the ray tips. Below it a second, small ear-fin of the "
        "same kind (about 90 px). On the cheek, under and behind the eye, one small dusty grey-teal gill-fin with two short rays.\n"
        "- NECK AND CHEST: the neck rises from the body in a strong S curve to the head. Its back is indigo. Its front, from "
        "under the chin down the throat and over the chest, is covered with broad cream BELLY PLATES: wide horizontal bands "
        "like the belly of a snake, each separated by one thin ink line, with a clean smooth border against the indigo (the "
        "jagged border in the guide is NOT wanted: draw it as a smooth line).\n"
        "- BODY: one continuous thick serpent tube, about 190 px thick at the chest and over the back. From the chest it "
        "runs to the LEFT over the top (the back), then curls DOWN and around into one big open LOOP at the left (the loop "
        "is about 420 px across, with an empty hole in its middle through which the white background shows), then passes "
        "low along the bottom toward the right, hidden for a stretch behind the near wing, then rises again as a thinner "
        "tail BEHIND the chest and ends to the right of the neck. On the outer side of the loop and along the underside the "
        "cream belly plates show as a broad band of cross-wise plates; the rest is indigo. Where one stretch of body passes "
        "in front of another, the front one has its own closed ink outline.\n"
        "- SHELL ARMOUR: on the top of the back, where the body is highest (left of the neck), THREE overlapping SCALLOP "
        "SHELLS sit in a row like saddle armour: fan-shaped ribbed shells, pale cream with soft ochre ribs, each about 80 px wide "
        "(clearly bigger than the tiny ones in the guide), hinge side down on the back.\n"
        "- DORSAL SAIL FINS: FIVE tall pointed sail fins stand along the back and the outer side of the loop, where the "
        "guide shows them (the tallest about 230 px): each is a dusty grey-teal web on one to three dark-navy rays that end in sharp "
        "tips, the web edge sagging in a curve between the tips. Each sail has its own closed outline; neighbours overlap.\n"
        "- SMALL FINS: four or five small pointed fins of the same kind (dusty grey-teal web, one dark-navy ray) along the inner side "
        "of the loop and under the body, where the guide shows them.\n"
        "- THE TWO FIN-WINGS, the star of the design: long, narrow wings like the pectoral fins of a flying fish. Both grow "
        "from the SHOULDER, the side of the body just below the chest, and hang downward, slightly spread.\n"
        "  * NEAR WING, in FRONT of the body: it sweeps down to the LOWER LEFT, about 720 px long and about 210 px wide at "
        "its widest. Along its lower-right edge runs a strong dark-navy SPAR like a bony arm: thick (about 60 px) at the "
        "shoulder, tapering to a point at the wing tip, with two or three small knuckle bumps. From the shoulder SIX thin "
        "dark-navy RAYS fan out through the dusty grey-teal membrane to the upper-left TRAILING EDGE; the trailing edge is cut into "
        "soft ROUNDED SCALLOPS, one between each pair of ray tips (clean curves, NOT ragged, NOT flame shaped). THREE round "
        "pale-cream SPOTS in a row on the membrane, getting smaller toward the tip.\n"
        "  * FAR WING, BEHIND the body: the same kind of wing, hanging down to the LOWER RIGHT, about 430 px of it visible "
        "below the body, narrower (about 130 px), its dark-navy spar along its right edge, four rays, scalloped left edge, two "
        "cream spots.\n"
        "- TAIL FIN: the tail ends, to the right of the neck and behind it, in a forked FISH TAIL FIN pointing up-right "
        "(about 200 px): two pointed lobes, dusty grey-teal web on dark-navy rays.\n"
        "- Exactly one head, two wings, no limbs.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
         "visible, nothing cut by the edges. As in the guide, the whole creature is about 920 px wide (from the sail-fin tips "
         "at about x = 310 to the far wing tip at about x = 1230) and about 890 px tall (from the horn tips at about y = 75 "
         "to the wing tips at about y = 960).")

POSE = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): hovering "
        "still in a calm, clean resting pose, mouth closed, wings hanging open. Every part is clearly separated by its own "
        "closed ink outline: the head, the beak, each horn, each head fin, each stretch of the body, each sail fin, each "
        "small fin, each wing spar and each wing membrane, the tail fin. No water, no bubbles, no clouds, no mist, no "
        "sparkles, no stars, no magic lines, no splashes, no ground.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The "
        "layout guide is a stiff flat computer diagram with rough edges: take the construction, the placement, the "
        "proportions and the overlaps from it, never its mechanical line, its jagged edge noise or its empty flat fills. "
        "Redraw every shape cleanly and with character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 6 px thick on this canvas for the body, head, wings and big fins and about 4 px "
        "for small details (rays, belly plate lines, shell ribs), a closed outline around every part; every area coloured "
        "with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the "
        "outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the figure, "
        "on the ground or on the background), no white highlights or shine spots, no gloss, no wet look, no reflections, no "
        "glow, no rim light, no gradients, no transparency in the fin webs, no 3D look. A different tone appears only where "
        "the design itself lists a different colour. The only white dot is the tiny one in the eye.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def draft():
    """Bản nháp mới nhất người dùng đã xem. 2026-11-11: bản 1 "phối màu cánh xanh cam loè loẹt quá, đổi sang màu trầm" → bản 2 tông
    trầm; bản 2 "mỏ và sừng cho sang màu đen"."""
    d = save_dir(1)
    c = [os.path.join(d, f) for f in os.listdir(d) if f.startswith("L1_concept") and f.endswith(".png")] if os.path.isdir(d) else []
    return max(c, key=os.path.getmtime) if c else None


def refs():
    d = draft()
    pre = [(d, "PREVIOUS DRAFT of THIS creature, 1536x1024, white background. The drawing AND its colours are approved: KEEP "
               "every shape, every part, its place, its size, the pose, the wobbly ink line, the crayon hatching and every "
               "colour exactly as they are. CHANGE ONLY ONE THING: the TWO HORNS and the BEAK (both its upper and its lower "
               "part) become CHARCOAL BLACK (#26252C), flat matte black with the same crayon texture, with two or three "
               "short dark-grey ring lines near the base of each horn and a thin dark-grey mouth line on the beak. Nothing "
               "else changes: the shells keep their cream and ochre, the eye stays amber.",
            "Bản nháp trước (1536 × 1024, nền trắng): rồng vây thân chàm tím, vây lam xám trầm, sừng và mỏ màu cát. Giữ nguyên "
            "nét vẽ và màu, chỉ đổi hai sừng và mỏ sang đen than")] if d else []
    return pre + [
        (guide(1), "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing how it is "
                   "built, where every part goes on the canvas, how big it is and which part overlaps which (the small head "
                   "with beak, eye, brow, two horns and head fins at the upper right; the S-curved neck with cream chest "
                   "plates; the thick body looping at the left with its cream underside; the three shells and the five "
                   "sail fins on the back; the near wing sweeping down-left in front of the body with its dark-navy spar, rays "
                   "and spots; the far wing hanging down-right behind the body; the tail fin behind the neck at the right). "
                   "Follow it closely; redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): rồng rắn thân chàm tím cuộn một vòng bên trái, đầu nhỏ có mỏ ở "
         "trên phải, bụng kem có vạch, năm vây buồm và ba vỏ sò trên lưng, hai cánh vây lam xám trầm có sống chàm sẫm buông xuống, đốm kem. "
         "Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng"),
        (SNAKE, "an approved hero of the same game (a small horned water snake), 1536x1024, white background: match EXACTLY "
                "its wobbly pen line, its visible crayon hatching and its completely flat colouring; see how its belly plates, "
                "its eye and its smooth horns are drawn. Do NOT copy its species, its chibi proportions, its design or its "
                "colours.",
         "Rắn sừng dạng 1 đã duyệt (1536 × 1024, nền trắng): rắn lam cuộn tròn, sừng đen, mắt cam. Lấy nét bút rung, vân sáp, tô "
         "phẳng, cách vẽ vạch bụng, mắt, sừng trơn"),
        (DROP, "another approved hero of the same game (a water-blob creature), 1536x1024, white background: the same line and "
               "flat crayon colouring. Do NOT copy its species, design or colours.",
         "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam. Chỉ lấy nét bút rung, vân sáp, tô phẳng"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]


CHECK = [
    "Dáng như sơ đồ: đầu nhỏ ở trên phải quay sang phải, cổ chữ S, thân dày cuộn **một vòng hở** bên trái, đuôi vòng ra sau ngực.",
    "Đầu: mõm ngắn có **mỏ sừng đen**, **một mắt hổ phách con ngươi dọc** dưới gờ mày sẫm, **hai sừng đen trơn** vuốt ra sau, "
    "vây tai lớn + vây tai nhỏ + vây mang trên má. **Không lông, lông vũ, bờm, râu.**",
    "Ngực và bụng: **vạch bụng kem** ngang thân, ranh với phần chàm là đường trơn.",
    "Lưng: **ba vỏ sò** kem gân màu cát; **năm vây buồm** lam xám trầm có tia chàm sẫm nhọn; vài vây nhỏ ở lòng vòng cuộn và dưới thân.",
    "**Hai cánh vây** buông xuống: cánh gần quét xuống trái, đè trước thân, sống chàm sẫm dày, sáu tia, mép sau **lượn sò tròn** (không "
    "rách kiểu lửa), ba đốm kem; cánh xa buông xuống phải sau thân.",
    "Vây đuôi chẻ đôi sau cổ, bên phải.",
    "Mỗi bộ phận có viền mực kín riêng (để cắt mảnh): từng khúc thân, từng vây, sống cánh, màng cánh.",
    "Tô phẳng: **không** bóng, không điểm sáng, không vân phát sáng, không mây, nước; nền trắng tinh.",
]

FIX = [
    ("Có lông, lông vũ, bờm trắng quanh cổ", "Remove all fur, feathers and mane: the throat and chest are smooth cream belly "
                                             "plates, the horns are smooth charcoal-black horn, the ear is a webbed fin with rays."),
    ("Mép cánh rách kiểu ngọn lửa, có vân sáng / chòm sao", "The trailing edge of each wing is cut into soft rounded scallops "
                                                            "between the ray tips, clean curves; remove every glowing line "
                                                            "and star: the membrane is flat dusty grey-teal with dark-navy rays and "
                                                            "three cream spots."),
    ("Có bóng, mảng sáng tối, điểm sáng, màng vây trong suốt", "Flat colour only: remove every shadow, highlight, gradient "
                                                               "and transparency; keep the crayon hatching as texture only."),
    ("Chibi, đầu to", "Grown-up proportions: the head is small (about 270 px wide), the body long and thick, as in the layout "
                      "guide."),
    ("Thân không cuộn vòng hoặc vòng bị lấp kín", "The body curls into one big open loop at the left with an empty hole in "
                                                  "its middle, exactly as in the layout guide."),
    ("Cánh dính liền thân, không có viền riêng", "Each wing spar and each wing membrane has its own closed ink outline and "
                                                 "is drawn over (near wing) or behind (far wing) the body."),
    ("Thiếu vỏ sò, vây buồm, đốm cánh", "Add every listed detail: three scallop shells on the back, five ray-finned sail "
                                        "fins, the small fins, three cream spots on the near wing, two on the far wing."),
    ("Có mây, nước, tia sáng quanh con", "Remove everything around the creature: plain white background only."),
    ("Mặt hiền, mắt tròn", "Make the eye almond shaped under a dark pointed brow ridge: a determined, fierce look."),
]


# ---------------------------------------------------------------- lượt 2: từng nhóm mảnh, đúng chỗ, đúng cỡ như concept đã duyệt
def chosen(k=1):
    return os.path.join(save_dir(k), "L1_duyet.png")


PART = {
    "than_1": "NECK: the S-curved neck, from just under the head down to where it joins the chest. Indigo back, cream belly "
              "plates in front. Its top end (hidden under the head in image 1) and its bottom end (tucked into the chest) are "
              "simple rounded ends. No head, no horns, no head fins, no tail fin on it.",
    "than_2": "CHEST: the thick stretch of body under the neck, curving from the base of the neck to the left under the back: "
              "indigo, with the cream belly plates along its right and lower side. Both ends are rounded. WITHOUT the wings: "
              "where the near wing and its spar cover it in image 1, continue the indigo body and the cream plates.",
    "than_3": "BACK: the high stretch of body on top, left of the neck, carrying the THREE scallop shells (the shells belong "
              "to this part: keep them exactly as in image 1). Indigo. Both ends rounded; where sail fins or the next stretch "
              "of body cover it, continue the indigo body. No sail fins on it.",
    "than_4": "LOOP: the big C-shaped stretch of body at the left that forms the loop: cream belly plates on its outer side, "
              "indigo on its inner side. Both ends rounded. No fins on it.",
    "than_5": "LOWER BODY: the stretch of body that runs low along the bottom, from the lower end of the loop toward the "
              "right; in image 1 most of it is hidden behind the near wing. Draw it complete, filling the pink area of image 2: indigo, cream "
              "belly plates along its right end and a little at its left end, both ends rounded.",
    "than_6": "TAIL STOCK: the thinner tail stretch that rises behind the chest; in image 1 only a piece of it shows through "
              "the gap left of the neck. Draw it complete, filling the pink area of image 2: a short curved tube, cream belly plates on its "
              "left side, a narrow indigo strip on its right side, both ends rounded.",
    "dau": "HEAD: the head with its amber eye and its dark brow ridge exactly as in image 1, but WITHOUT the beak, WITHOUT the "
           "two horns, WITHOUT the ear fins and WITHOUT the cheek fin. Where those covered the head, continue the plain indigo "
           "head. One closed rounded shape: a blunt rounded muzzle end at the right (where the beak attaches), a rounded back "
           "end at the left (neck side).",
    "mo_tren": "UPPER BEAK: only the upper part of the black beak with its little hooked tip. Its base, hidden inside the "
               "muzzle, is rounded.",
    "mo_duoi": "LOWER BEAK: only the lower part of the black beak, a small closed wedge. Its base is rounded.",
    "sung_t": "FRONT HORN: the more upright black horn, complete down to a rounded base (the base is hidden in the head).",
    "sung_s": "REAR HORN: the longer, more horizontal black horn, complete to a rounded base.",
    "tai_lon": "BIG EAR-FIN: the large fin behind the cheek, grey-teal web on dark-navy rays, complete with a narrow rounded "
               "root where it joins the head.",
    "tai_nho": "SMALL EAR-FIN: the small fin below the big ear-fin, complete with a rounded root.",
    "vay_ma": "CHEEK FIN: the small gill-fin on the cheek under and behind the eye, complete, with a rounded root.",
    "vay_duoi": "TAIL FIN: the forked fish tail fin at the right of the neck together with the short thin indigo tail stem it "
                "grows from, as in image 1; where the neck hides the stem, continue it to a rounded end.",
    "vay_14": "BIG SAIL FINS: the cluster of tall pointed sail fins on the back, joined at their bases into ONE part, as in "
              "image 1. Its lower edge, hidden behind the body and the shells, continues about 30 px down and ends in one "
              "smooth curved base line.",
    "vay_15": "SAIL FIN NEXT TO THE NECK: the tall narrow sail fin between the shells and the neck, complete; its base, "
              "hidden behind the body, ends in a smooth rounded edge.",
    "canh_g_mang": "NEAR WING MEMBRANE: the whole grey-teal membrane of the near wing with its dark-navy rays, its scalloped "
                   "trailing edge and its three cream spots, WITHOUT the thick dark-navy spar. Where the spar covered it, "
                   "continue the membrane and the rays up to the shoulder; the edge that ran along the spar becomes a smooth "
                   "line. One closed shape.",
    "canh_g_song": "NEAR WING SPAR: only the thick dark-navy bony spar of the near wing, from the shoulder to the wing tip, "
                   "with its knuckle bumps, exactly as in image 1. One closed shape, the shoulder end rounded.",
    "canh_x_mang": "FAR WING MEMBRANE: the grey-teal membrane of the far wing with its rays and cream spots, WITHOUT its spar, "
                   "complete: the upper part hidden behind the body continues up to the shoulder over the pink area of image 2.",
    "canh_x_song": "FAR WING SPAR: only the thin dark-navy spar of the far wing, complete from the shoulder (hidden behind "
                   "the body in image 1) down to the wing tip, over the pink area of image 2.",
}
FIN = ("FIN: the pointed fin at this place (grey-teal web with its dark-navy ray or rays), exactly as in image 1 where it is "
       "visible. Draw it complete, filling the pink area of image 2: its base, hidden behind the body in image 1, runs a little into the body "
       "and ends in a smooth rounded edge.")
VI = {"than_1": "cổ", "than_2": "ngực", "than_3": "lưng mang ba vỏ sò", "than_4": "vòng cuộn chữ C", "than_5": "khúc đáy",
      "than_6": "khúc đuôi mảnh sau ngực", "dau": "đầu (có mắt, gờ mày; không mỏ, sừng, vây)", "mo_tren": "mỏ trên",
      "mo_duoi": "mỏ dưới", "sung_t": "sừng trước", "sung_s": "sừng sau", "tai_lon": "vây tai lớn", "tai_nho": "vây tai nhỏ",
      "vay_ma": "vây má", "vay_duoi": "vây đuôi + cuống đuôi", "vay_14": "cụm vây buồm lớn", "vay_15": "vây buồm cạnh cổ",
      "canh_g_mang": "màng cánh gần (không sống)", "canh_g_song": "sống cánh gần", "canh_x_mang": "màng cánh xa",
      "canh_x_song": "sống cánh xa"}

P_SAME = ("Same hand-drawn look as image 1: wobbly dark-brown ink outline (#2B2118) of the same thickness as in image 1, the "
          "same flat colours (indigo #34408F, cream #F3E6C4, dusty grey-teal #6A9BA8, dark navy #242C68, charcoal black "
          "#26252C, pale cream #FAF0D6 with ochre ribs, amber eye), the same loose crayon hatching. FLAT COLOUR, NO LIGHT, NO "
          "SHADOW: every area one even colour, no shading, no highlights, no gloss, no glow, no gradients.")
P_PAGE = ("CANVAS: 1536x1024, pure-white background (#FFFFFF) everywhere outside the parts: no paper grain, no ground line, no "
          "shadow, no text, no labels, no numbers, no frame, no white sticker border. Nothing else on the page.")


def build_parts():
    import json
    nj = os.path.join(HERE, "inbox", f"{CODE}_1", "mau", "nhom.json")
    if not (os.path.exists(chosen()) and os.path.exists(nj)):
        print("lượt 2: chưa dựng (cần L1_duyet.png và mau/nhom.json: chạy rong_vay.py nhom)")
        return []
    G = json.load(open(nj, encoding="utf-8"))
    files = []
    for X, parts in G.items():
        gimg = os.path.join(HERE, "inbox", f"{CODE}_1", "mau", f"nhom_{X}.png")
        out = os.path.join(save_dir(1), f"N_{X}.png")
        p = os.path.join(pk(1), f"luot_2_nhom_{X}.txt")
        n = len(parts)
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {W(chosen())}: the APPROVED picture of the whole creature (a winged sea-serpent dragon), 1536x1024, "
             "white background. Use it to understand what each part is and how its hidden areas should look.",
             f"image 2 = {W(gimg)}: CUT-OUT GUIDE, 1536x1024, white background: it is image 1 with everything erased except "
             f"the {n} parts wanted in this picture, each exactly where it is in image 1. The flat HOT-PINK areas (#FF69B4) are "
             "NOT part of the drawing: they are markers showing where a part continues, hidden in image 1 behind parts that "
             "were erased. Some cut edges of the parts are ragged because a computer cut them.",
             "", f"SAVE: save it as a PNG to {W(out)}",
             f"If a file with that name already exists, save as N_{X}_2.png, N_{X}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             f"TASK: redraw image 2 as a finished cut-out sheet of these {n} separate parts for 2D skeleton animation.", "",
             "RULES:",
             "- KEEP every drawn (non-pink) area of image 2 EXACTLY as it is and exactly where it is: the same position on "
             "the canvas, the same size, the same outline, the same details, the same colours. Do not move, scale, rotate, "
             "tidy up or restyle the parts. If the result were laid over image 2, every drawn area would line up.",
             "- REPLACE every pink area by the missing continuation of the part it touches: continue that part's colours and "
             "pattern over the pink area (cream belly plates continue as cross-wise bands with thin ink lines, the indigo back "
             "stays indigo, fin webs and their dark-navy rays continue to the fin base, a wing membrane continues to the "
             "shoulder) and round off its end. A part that is shown ONLY as a pink shape (completely hidden in image 1) is "
             "drawn new, filling that pink shape.",
             "- Smooth the ragged computer-cut edges into a clean hand-drawn outline.",
             "- Each part ends up as ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it, also "
             "along the edges that were hidden. No pink anywhere in the result.",
             f"- Exactly these {n} parts, not touching each other, white background between them. Do not add any other part "
             "of the creature. Ignore tiny stray specks of image 2.", "",
             f"THE {n} PARTS (the place is the centre of the part on the 1536x1024 canvas):"]
        vi = []
        for i, q in enumerate(parts, 1):
            x, y = q["tam"]
            t.append(f"{i}. at about x = {x:.0f}, y = {y:.0f}: " + PART.get(q["ten"], FIN))
            vi.append(f"{q['ten']} ({VI.get(q['ten'], 'vây')})")
        t += ["", P_SAME, P_PAGE]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        files.append((X, p, gimg, out, vi))
    return files



# ---------------------------------------------------------------- lượt 2, nhóm M: mỏ trên, mỏ dưới, mí mắt nhắm (tờ phóng to 6 lần)
MO_O = (1095, 150, 1245, 270)        # ô quanh mỏ và mắt trên concept (x0, y0, x1, y1)
MAT_O = (1040, 140, 1140, 220)
MO_Z = 6


def build_beak():
    from PIL import Image
    if not os.path.exists(chosen()):
        return None
    con = Image.open(chosen()).convert("RGB")
    mau = os.path.join(HERE, "inbox", f"{CODE}_1", "mau")
    os.makedirs(mau, exist_ok=True)
    crop = os.path.join(mau, "mo_x6.png")
    x0, y0, x1, y1 = (min(MO_O[0], MAT_O[0]), min(MO_O[1], MAT_O[1]), max(MO_O[2], MAT_O[2]), max(MO_O[3], MAT_O[3]))
    con.crop((x0, y0, x1, y1)).resize(((x1 - x0) * MO_Z, (y1 - y0) * MO_Z), Image.LANCZOS).save(crop)
    out = os.path.join(save_dir(1), "N_M.png")
    p = os.path.join(pk(1), "luot_2_nhom_M.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the whole creature (a winged sea-serpent dragon), 1536x1024, white "
         "background.",
         f"image 2 = {W(crop)}: a 6x ENLARGEMENT of the face of image 1 ({(x1 - x0) * MO_Z}x{(y1 - y0) * MO_Z}): the amber eye "
         "under its brow at the left and the charcoal-black beak at the right, with the thin grey mouth line that separates "
         "the upper beak (hooked tip) from the smaller lower beak.",
         "", f"SAVE: save it as a PNG to {W(out)}",
         "If a file with that name already exists, save as N_M_2.png, N_M_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: a cut-out sheet of THREE small separate parts of the face for 2D skeleton animation (the beak must be able to "
         "open, the eye must be able to close). Draw every part at the SAME SCALE as image 2 (6 times the size it has in "
         "image 1) and in the same orientation as in image 2 (the beak points to the right). Three parts in one row, far "
         "apart, white background between them:",
         "1. LEFT third of the canvas, UPPER BEAK: only the upper part of the beak, everything above the mouth line, with "
         "its hooked tip, exactly the shape it has in image 2. Complete it at the left: its base, which is hidden inside the "
         "muzzle, continues about 150 px further left and ends in a rounded edge. Flat charcoal black (#26252C), its lower "
         "edge (the mouth line side) is a clean ink outline.",
         "2. MIDDLE third, LOWER BEAK: only the lower part of the beak, everything below the mouth line: a small wedge "
         "pointing right. Complete it: its top, hidden behind the upper beak, rises about 40 px above the mouth line as a "
         "gentle bulge, and its base at the left continues about 120 px into the muzzle and ends rounded. Flat charcoal "
         "black (#26252C).",
         "3. RIGHT third, CLOSED EYE: the same almond eye shape as in image 2, at the same size, but CLOSED: the whole almond "
         "is filled with the indigo skin colour of the head (#3A4AB2, the same blue as around the eye in image 2), with ONE "
         "curved dark-brown ink line across its lower third (the shut eyelid, curving downward like a frown, matching the "
         "fierce brow), and the dark-brown ink outline around the almond. No amber, no pupil, no white dot, no eyelashes.",
         "",
         "Each part is ONE CLOSED SHAPE with a dark-brown ink outline (#2B2118) all the way around, about 36 px thick at this "
         "enlarged scale (it is 6 px in image 1). " + P_SAME.split("FLAT COLOUR")[0].strip(),
         "FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour with loose crayon hatching as texture; no shading, no "
         "highlights, no gloss, no gradients.", P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return ("M", p, crop, out, ["mo_tren (mỏ trên)", "mo_duoi (mỏ dưới)", "mat_nham (mí mắt nhắm)"])



# ---------------------------------------------------------------- lượt 2, nhóm S: dải cạnh cánh (cánh nhìn đúng cạnh)
def build_strip():
    """Mổ clip idle của con gốc (scan/monster_3458/idle_lo.json): mảnh duy nhất idle dùng mà mình thiếu là dải mỏng P_chibangR08_2
    (301 × 22, một ảnh cho cả hai cánh): lúc nghỉ nấp sau sống cánh, lúc cánh quay ngang (màng ép dẹt) thì lộ ra làm bề dày cánh."""
    if not os.path.exists(chosen()):
        return None
    out = os.path.join(save_dir(1), "N_S.png")
    p = os.path.join(pk(1), "luot_2_nhom_S.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the creature (a winged sea-serpent dragon), 1536x1024, white "
         "background. Look at its two fin-wings: a dark-navy bony spar along the leading edge and a dusty grey-teal membrane "
         "with dark-navy rays. Use it only for the colours, the ink line and the crayon texture.",
         "", f"SAVE: save it as a PNG to {W(out)}",
         "If a file with that name already exists, save as N_S_2.png, N_S_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: draw ONE small cut-out part for 2D skeleton animation: the WING SEEN EXACTLY EDGE-ON. When a wing of the "
         "creature in image 1 turns its edge toward the viewer, all that is visible is one long thin blade: the spar with the "
         "folded membrane lying flat against it.",
         "Draw it as ONE long, thin, slightly wavy STRIP lying HORIZONTALLY in the middle of the canvas:",
         "- about 620 px long, from about x = 460 (left end) to about x = 1080 (right end), centred at about y = 512;",
         "- the LEFT end is the shoulder: about 40 px thick, with a rounded end;",
         "- it tapers smoothly along its whole length to a SHARP POINT at the right end (the wing tip);",
         "- its upper three quarters are the spar: flat dark navy (#242C68), with two or three low knuckle bumps on the top "
         "edge, like the spar in image 1;",
         "- along its whole bottom edge runs a narrow band, about 9 px thick at the shoulder and thinning to nothing at the "
         "tip, of dusty grey-teal (#6A9BA8): the folded membrane seen from the side; a thin ink line separates it from the "
         "navy spar;",
         "- a wobbly dark-brown ink outline (#2B2118), about 6 px thick, all the way around: ONE CLOSED SHAPE.",
         "Nothing else on the page: no wing membrane spread out, no rays, no spots, no second strip.", "",
         P_SAME, P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return ("S", p, chosen(), out, ["canh_canh (dải cạnh cánh, một ảnh dùng cho cả hai cánh)"])



# ---------------------------------------------------------------- lượt 2, nhóm T: CẢ THÂN liền một ảnh (cắt khúc bằng mã)
def build_body():
    """Người dùng 2026-11-11: "những khớp nối thì gen cả con ra rồi cắt chứ không gen riêng không thì sẽ lệch". Năm khúc thân gen
    riêng (nhóm B, C, D) vạch bụng mỗi khúc một kiểu nên chỗ nối lệch. Nhóm T gen cả thân liền một ảnh; rong_vay.py cat_than cắt.
    Bản đầu (N_T.png) khúc đáy bị dày: người dùng "phần thân này màu xanh hơi dày, giảm đi chút" → thêm mục THICKNESS (N_T_2)."""
    gimg = os.path.join(HERE, "inbox", f"{CODE}_1", "mau", "nhom_T.png")
    if not (os.path.exists(chosen()) and os.path.exists(gimg)):
        return None
    out = os.path.join(save_dir(1), "N_T.png")
    p = os.path.join(pk(1), "luot_2_nhom_T.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the whole creature (a winged sea-serpent dragon), 1536x1024, white "
         "background. Use it to understand how the serpent body runs.",
         f"image 2 = {W(gimg)}: BODY GUIDE, 1536x1024, white background: it is image 1 with everything erased except the "
         "serpent BODY (neck, chest, the back with its three scallop shells, the big loop, the lower stretch), exactly where "
         "it is in image 1. The flat HOT-PINK areas (#FF69B4) are NOT part of the drawing: they mark where the body continues, "
         "hidden in image 1 behind the wings, the fins and the head that were erased. Some cut edges are ragged because a "
         "computer cut them.",
         "", f"SAVE: save it as a PNG to {W(out)}",
         "If a file with that name already exists, save as N_T_2.png, N_T_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 as the finished picture of the serpent BODY ALONE: ONE continuous thick tube, with no wings, no "
         "fins, no head, no horns, no tail fin.", "",
         "RULES:",
         "- KEEP every drawn (non-pink) area of image 2 EXACTLY as it is and exactly where it is: same position, same size, "
         "same outline, same cream belly plates with their lines, same three shells, same colours. Do not move, scale, rotate, "
         "tidy up or restyle it. If the result were laid over image 2, every drawn area would line up.",
         "- REPLACE every pink area by the body continuing through it, so the tube is unbroken: the indigo back continues as "
         "indigo; the band of cream belly plates continues along the same side of the tube with the same width and the same "
         "spacing of cross lines, joining smoothly onto the plates on both sides of the gap; the dark-brown ink outline runs "
         "along both edges of the tube.",
         "- THICKNESS (important): the tube keeps an even, moderate thickness. Along the big loop and the lowest stretch it is "
         "about 160 px across in total (the indigo part about 100 px, the cream plates about 60 px), clearly SLIMMER than the "
         "chest. The pink areas are wider than the body really is: do NOT fill their whole width. Along the lowest stretch the "
         "indigo part must not be thick: its inner outline (the edge of the empty hole of the loop) runs INSIDE the pink area, "
         "which makes the hole of the loop larger.",
         "- The pink cap at the very top (where the head was) becomes the rounded top end of the neck.",
         "- The big empty hole in the middle of the loop stays empty white background.",
         "- At the lower right, where the lowest stretch of the body disappears behind the chest, simply let it end there "
         "as it does in image 2.",
         "- Smooth the ragged computer-cut edges into a clean hand-drawn outline. No pink anywhere in the result. Nothing "
         "else on the page.", "",
         P_SAME, P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return ("T", p, gimg, out, ["than_1 … than_5 (cả thân liền một ảnh, `rong_vay.py cat_than` cắt thành năm khúc chờm mép nhau)"])



# ---------------------------------------------------------------- lượt 2, nhóm U: PHẦN ĐUÔI liền một ảnh (cắt khúc bằng mã)
def build_tail():
    """Người dùng 2026-11-11: "phần đuôi đâu, nhìn hướng này ổn áp hơn đó": đuôi cũng gen liền rồi cắt như thân. Ảnh 2: khúc đáy lấy
    nguyên từ ảnh cả thân N_T, mẩu đuôi lộ bên trái cổ và cuống + vây đuôi lấy từ concept, đoạn nấp sau ngực và cổ tô hồng."""
    gimg = os.path.join(HERE, "inbox", f"{CODE}_1", "mau", "nhom_U.png")
    if not (os.path.exists(chosen()) and os.path.exists(gimg)):
        return None
    out = os.path.join(save_dir(1), "N_U.png")
    p = os.path.join(pk(1), "luot_2_nhom_U.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the whole creature (a winged sea-serpent dragon), 1536x1024, white "
         "background. Its long tail runs from the lowest stretch of the body, up BEHIND the chest and the neck, and comes out "
         "at the right of the neck, where it ends in a forked fish tail fin.",
         f"image 2 = {W(gimg)}: TAIL GUIDE, 1536x1024, white background: only the rear of the serpent, exactly where it is in "
         "image 1: at the bottom the lowest stretch of the body (indigo, cream belly plates at its ends); in the middle a small "
         "piece of the tail with cream plates; at the upper right the thin tail stem with its forked tail fin. The flat "
         "HOT-PINK band (#FF69B4) that joins them is NOT part of the drawing: it marks the path of the tail where it is hidden "
         "in image 1 behind the chest and the neck (which are erased here).",
         "", f"SAVE: save it as a PNG to {W(out)}",
         "If a file with that name already exists, save as N_U_2.png, N_U_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 as the finished picture of the REAR BODY AND TAIL ALONE: ONE continuous tube that starts as the "
         "thick lowest stretch of the body, rises, bends to the right and tapers smoothly into the thin tail stem and its "
         "tail fin. No chest, no neck, no head, no wings, no other fins.", "",
         "RULES:",
         "- KEEP every drawn (non-pink) area of image 2 EXACTLY as it is and exactly where it is: same position, same size, "
         "same outline, same cream belly plates, same tail fin, same colours. If the result were laid over image 2, every "
         "drawn area would line up.",
         "- REPLACE the pink band by the tail running through it, joining the three drawn pieces into one unbroken tube that "
         "gets steadily thinner toward the tail fin: the indigo back continues as indigo; the band of cream belly plates "
         "continues along the same side of the tube, with the same kind of cross lines, getting narrower with the tube and "
         "fading out before the thin tail stem; the dark-brown ink outline runs along both edges of the tube.",
         "- Follow the pink band's path and width; smooth its lumpy computer-made edge into a clean hand-drawn outline.",
         "- No pink anywhere in the result. Nothing else on the page.", "",
         P_SAME, P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return ("U", p, gimg, out, ["phần đuôi liền một ảnh: nối khúc đáy → than_6 → vay_duoi (cuống + vây); `rong_vay.py cat_duoi` cắt"])



# ---------------------------------------------------------------- lượt 3: mảnh vẽ ĐÚNG KHUNG part của rig (y hệt tỉ lệ, hướng)
PART_EN = {
    "P_chibangR08": "the long, thin, slightly wavy dark-navy SPAR of the near wing (the bony leading edge), running diagonally from "
                    "the upper right (shoulder end, with two or three small knuckle bumps) down to a point at the lower left. Flat "
                    "dark navy (#242C68).",
    "P_weiba": "the TAIL FIN: one broad fish fin, a dusty grey-teal web (#6A9BA8) stretched on four or five dark-navy rays that "
               "fan out from its narrow root at the upper left toward its wide outer edge; the outer edge is gently scalloped "
               "between the ray tips.",
    "P_shenti06": "a short curved piece of the TAIL of the serpent body: almost all of it is cream belly plates (#F3E6C4), broad "
                  "cross-wise bands separated by thin ink lines that follow the curve; only a narrow strip along the concave "
                  "(right) edge is indigo (#34408F). Both ends are simple rounded ends with no detail.",
    "P_chibangL05": "the long, thin, slightly wavy dark-navy SPAR of the far wing, running from the top down to a point at the "
                    "bottom, with two small knuckle hooks on its left side. Flat dark navy (#242C68).",
    "P_yuqi02": "a SMALL EAR-FIN: a tiny pointed fin, dusty grey-teal web (#6A9BA8) with one dark-navy ray.",
}
PART_VI = {"P_chibangR08": "sống cánh gần", "P_weiba": "vây đuôi", "P_shenti06": "khúc đuôi (dùng cho cả khúc đuôi thứ hai)",
           "P_chibangL05": "sống cánh xa", "P_yuqi02": "vây tai nhỏ"}


def build_part(to="P1"):
    """Người dùng 2026-11-11: "sao không gen theo đó ghép lại rồi đổi pose là được", "gen theo y hệt đúng tỉ lệ luôn, đúng hướng".
    Mảnh vẽ ngay trong khung ảnh của part trên rig (hình bóng phẳng đúng cỡ, đúng hướng): rig dùng nguyên lưới + uv của part đó."""
    import json
    mau = os.path.join(HERE, "inbox", f"{CODE}_1", "mau")
    gimg, gj = os.path.join(mau, f"part_{to}.png"), os.path.join(mau, f"part_{to}.json")
    if not (os.path.exists(chosen()) and os.path.exists(gj)):
        return None
    K = json.load(open(gj, encoding="utf-8"))
    out = os.path.join(save_dir(1), f"N_{to}.png")
    p = os.path.join(pk(1), f"luot_3_part_{to}.txt")
    n = len(K)
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the creature (a winged sea-serpent dragon), 1536x1024, white "
         "background. Use it for the design, the colours, the wobbly dark-brown ink line and the crayon texture.",
         f"image 2 = {W(gimg)}: PART SHEET GUIDE, 1536x1024, white background: {n} separate flat shapes. Each shape is the exact "
         "SILHOUETTE of one cut-out part of the creature's animation rig: its outline, its size, its orientation and its place "
         "on the sheet are all fixed by the rig.",
         "", f"SAVE: save it as a PNG to {W(out)}",
         f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
         "or delete any other file.", "",
         f"TASK: redraw image 2 as a finished sheet of these {n} cut-out parts, drawn in the style of image 1.", "",
         "RULES:",
         "- EVERY PART KEEPS ITS SILHOUETTE EXACTLY: the same outline, the same size, the same orientation, the same position "
         "on the canvas as the flat shape in image 2. Do not rotate, mirror, move, resize, straighten or simplify any shape. If "
         "the result were laid over image 2, every part would cover its flat shape exactly.",
         "- Inside each silhouette draw the finished part as described below: flat colours, loose crayon hatching, and a "
         "dark-brown ink outline (#2B2118, about 6 px) running all the way around the silhouette (ONE CLOSED SHAPE per part).",
         "- Smooth away the small computer-made specks and jagged pixels of the guide; keep the overall outline.",
         f"- Exactly these {n} parts, white background between them, nothing else.", "",
         f"THE {n} PARTS (the place is the centre of the part's box on the 1536x1024 canvas):"]
    vi = []
    for i, (slot, (x, y, w, h)) in enumerate(K.items(), 1):
        t.append(f"{i}. at about x = {x + w / 2:.0f}, y = {y + h / 2:.0f} (the shape is about {w} px wide and {h} px tall): "
                 + PART_EN[slot])
        vi.append(f"`{slot}` ({PART_VI[slot]})")
    t += ["", P_SAME, P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return (to, p, gimg, out, vi)



# ---------------------------------------------------------------- lượt 3, tờ P2…: mọi part còn lại, hình hiện có đã nướng vào khung
THAN_EN = ("a stretch of the serpent BODY: indigo back with a band of cream belly plates (cross-wise bands, thin ink lines) along "
           "one long side. Its two ENDS are cut ends that tuck under the neighbouring stretches: draw NO ink outline across the "
           "ends, the colours simply run to the edge; the ink outline runs only along the two long sides. Remove any stray ink "
           "line that crosses the body from side to side (leftovers of other parts).")
PART_EN2 = {
    "than": THAN_EN,
    "than_3": THAN_EN + " This stretch carries the THREE scallop shells on its upper side: keep them.",
    "dau": "the HEAD (indigo) with its amber eye under the dark brow, without beak, horns or fins; where those were, plain indigo.",
    "dau:P_erduo": "the small dark-indigo pointed BROW CREST on top of the head: one small pointed shape, closed outline.",
    "mo_tren": "the UPPER BEAK: charcoal black (#26252C), with its small hooked tip; closed outline.",
    "mo_duoi": "the LOWER BEAK: a small charcoal-black wedge (#26252C); closed outline.",
    "sung": "a smooth charcoal-black HORN (#26252C) with two or three short grey ring lines near its base; closed outline.",
    "tai_lon": "the big EAR-FIN: dusty grey-teal web on dark-navy rays, scalloped rear edge; closed outline.",
    "vay": "a pointed FIN: dusty grey-teal web (#6A9BA8) with its dark-navy ray or rays; closed outline all around.",
    "mang": "a WING MEMBRANE: dusty grey-teal web with dark-navy rays fanning from the wing root, round cream spots, softly "
            "scalloped trailing edge; closed outline all around.",
}


def _part_en(ten, slot):
    for k in (f"{ten}:{slot}", ten, ten.split("_")[0], "mang" if ten.endswith("_mang") else ""):
        if k in PART_EN2:
            return PART_EN2[k]
    return PART_EN2["vay"]


def build_part2(to):
    import json
    mau = os.path.join(HERE, "inbox", f"{CODE}_1", "mau")
    gimg, gj = os.path.join(mau, f"part_{to}.png"), os.path.join(mau, f"part_{to}.json")
    if not (os.path.exists(chosen()) and os.path.exists(gj)):
        return None
    K = json.load(open(gj, encoding="utf-8"))
    out = os.path.join(save_dir(1), f"N_{to}.png")
    p = os.path.join(pk(1), f"luot_3_part_{to}.txt")
    n = len(K)
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the creature (a winged sea-serpent dragon), 1536x1024, white "
         "background. Use it for the design, the colours, the wobbly dark-brown ink line and the crayon texture.",
         f"image 2 = {W(gimg)}: PART SHEET GUIDE, 1536x1024, white background: {n} separate cut-out parts of the creature's "
         "animation rig, each inside its exact SILHOUETTE (outline, size, orientation and place on the sheet are fixed by the "
         "rig). Most of each part is already drawn. The flat HOT-PINK areas (#FF69B4) are NOT part of the drawing: they mark "
         "the rest of the silhouette that still has to be drawn. Some edges are ragged because a computer cut them.",
         "", f"SAVE: save it as a PNG to {W(out)}",
         f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
         "or delete any other file.", "",
         f"TASK: redraw image 2 as the finished sheet of these {n} cut-out parts.", "",
         "RULES:",
         "- EVERY PART KEEPS ITS SILHOUETTE EXACTLY: drawn area plus pink area together are the part's shape. Same outline, same "
         "size, same orientation, same position on the canvas. Do not rotate, mirror, move, resize or simplify. If the result "
         "were laid over image 2, every part would cover its drawn-plus-pink shape exactly, no more and no less.",
         "- KEEP the already drawn (non-pink) areas as they are: same colours, same pattern, same lines.",
         "- REPLACE every pink area by the missing continuation of the part it belongs to (same colours and pattern continuing "
         "smoothly: belly plates continue as cross-wise bands, fin webs and rays continue to the edge).",
         "- Clean the ragged computer-cut edges into a smooth hand-drawn edge along the silhouette. No pink anywhere in the "
         "result.",
         f"- Exactly these {n} parts, white background between them, nothing else.", "",
         f"THE {n} PARTS (the place is the centre of the part's box on the 1536x1024 canvas):"]
    vi = []
    for i, (slot, v) in enumerate(K.items(), 1):
        t.append(f"{i}. at about x = {v['x'] + v['w'] / 2:.0f}, y = {v['y'] + v['h'] / 2:.0f} (about {v['w']} px wide, {v['h']} px "
                 f"tall): " + _part_en(v["ten"], slot))
        vi.append(f"`{slot}` ({v['ten']})")
    t += ["", P_SAME, P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return (to, p, gimg, out, vi)



# ---------------------------------------------------------------- lượt 3, tờ Q2…: như P2… nhưng tờ hướng dẫn là HÌNH BÓNG KÍN
# (tờ P2–P6 để phần thiếu màu hồng: GPT hay bỏ, mảnh lệch hình bóng, lắp vào lưới của rig thì khuyết; tờ Q tô sẵn phần thiếu)
THAN_Q = ("a stretch of the serpent BODY: indigo back with a band of cream belly plates (cross-wise bands separated by thin ink "
          "lines) along one long side, exactly where the guide shows cream. Remove any dark line that crosses the indigo from "
          "side to side (leftover of a neighbouring part); the indigo is one plain area.")
PART_ENQ = dict(PART_EN2)
PART_ENQ.update({
    "than": THAN_Q,
    "than_3": THAN_Q + " This stretch carries the THREE scallop shells on its upper side: keep them.",
    "dau": "the HEAD: plain indigo with its amber eye under the dark brow exactly where the guide shows it; no beak, no horns, no "
           "fins, no cream patch: everything except the eye and brow is plain indigo.",
    "dau:P_erduo": "the small dark-navy pointed BROW CREST of the head: one plain dark-navy shape (#242C68).",
    "mo_tren": "the UPPER BEAK: plain charcoal black (#26252C) with a slightly lighter crayon texture; its hooked tip follows the "
               "silhouette.",
    "mo_duoi": "the LOWER BEAK: a small plain charcoal-black wedge (#26252C).",
    "sung": "a smooth HORN: plain charcoal black (#26252C) with two or three short grey ring lines across it near its wide end.",
})


def _part_enq(ten, slot):
    for k in (f"{ten}:{slot}", ten, ten.split("_")[0], "mang" if ten.endswith("_mang") else ""):
        if k in PART_ENQ:
            return PART_ENQ[k]
    return PART_ENQ["vay"]


def build_part3(to):
    import json
    mau = os.path.join(HERE, "inbox", f"{CODE}_1", "mau")
    gimg, gj = os.path.join(mau, f"part_{to}.png"), os.path.join(mau, f"part_{to}.json")
    if not (os.path.exists(chosen()) and os.path.exists(gj)):
        return None
    K = json.load(open(gj, encoding="utf-8"))
    out = os.path.join(save_dir(1), f"N_{to}.png")
    p = os.path.join(pk(1), f"luot_3_part_{to}.txt")
    n = len(K)
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(chosen())}: the APPROVED picture of the creature (a winged sea-serpent dragon), 1536x1024, white "
         "background. Use it for the design, the colours, the wobbly dark-brown ink line and the crayon texture.",
         f"image 2 = {W(gimg)}: PART SHEET GUIDE, 1536x1024, white background: {n} separate cut-out parts of the creature's "
         "animation rig. Each part is shown as its exact SILHOUETTE (outline, size, orientation and place on the sheet are all "
         "fixed by the rig), roughly coloured in by a computer: the colours and the pattern are in the right places, but some "
         "patches are smeared, streaky or greyish, and the edge is mechanical.",
         "", f"SAVE: save it as a PNG to {W(out)}",
         f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
         "or delete any other file.", "",
         f"TASK: redraw image 2 as the finished, clean sheet of these {n} cut-out parts, drawn in the style of image 1.", "",
         "RULES:",
         "- EVERY PART KEEPS ITS SILHOUETTE EXACTLY: the same outline, the same size, the same orientation, the same position "
         "on the canvas as in image 2. Do not rotate, mirror, move, resize, shrink, straighten or simplify any shape. Every "
         "bump, hook and point of the silhouette stays. If the result were laid over image 2, every part would cover its shape "
         "exactly, no more and no less.",
         "- A dark-brown ink outline (#2B2118, about 6 px) runs all the way around each silhouette, ON its edge (ONE CLOSED "
         "SHAPE per part). Where a part is cut straight by the border of the guide, keep that straight cut.",
         "- Inside, keep the colours and the pattern where the guide has them (the cream band on the same side, the rays in the "
         "same directions, the spots in the same places) and redraw them cleanly: flat colours with loose crayon hatching. "
         "Smeared, streaky or greyish patches become a clean continuation of the colour and pattern next to them.",
         "- Flat fill only: no shading, no shadow, no highlight, no gradient.",
         f"- Exactly these {n} parts, white background between them, nothing else.", "",
         f"THE {n} PARTS (the place is the centre of the part's box on the 1536x1024 canvas):"]
    vi = []
    for i, (slot, v) in enumerate(K.items(), 1):
        t.append(f"{i}. at about x = {v['x'] + v['w'] / 2:.0f}, y = {v['y'] + v['h'] / 2:.0f} (about {v['w']} px wide, {v['h']} px "
                 f"tall): " + _part_enq(v["ten"], slot))
        vi.append(f"`{slot}` ({v['ten']})")
    t += ["", P_SAME, P_PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return (to, p, gimg, out, vi)



def main():
    k = 1
    R = refs()
    missing = [W(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do "
          "not edit, move or delete any other file.", "",
          "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of "
          "the approved hero images.", "",
          FORM, "", PALETTE, "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: `{CODE}` dạng {k} (rồng vây, tên chưa đặt)", "",
          "Tướng thứ 8 đảo Thủy, làm 2026-11-11: reskin theo cách tách mảnh của con gốc `monster_3458`; màu và chi tiết là đề xuất "
          "của Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/rong_vay_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "Lượt 2 (từng mảnh, theo bảng mổ 34 mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/rong_vay_bo_cuc.py`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    L2 = build_parts()
    M = build_beak() if L2 else None
    if M:
        L2.append(M)
    S_ = build_strip() if L2 else None
    if S_:
        L2.append(S_)
    T_ = build_body() if L2 else None
    if T_:
        L2.append(T_)
    U_ = build_tail() if L2 else None
    if U_:
        L2.append(U_)
    P_ = build_part("P1") if L2 else None
    if P_:
        L2.append(P_)
    for so in range(2, 12):
        Pk = build_part2(f"P{so}") if L2 else None
        if Pk:
            L2.append(Pk)
    for so in range(2, 12):
        Pk = build_part3(f"Q{so}") if L2 else None
        if Pk:
            L2.append(Pk)
    if L2:
        gd += ["", "## Lượt 2: từng nhóm mảnh (concept đã duyệt)", "",
               "Mỗi nhóm một file prompt, một ảnh: GPT vẽ lại concept chỉ còn các mảnh của nhóm, **đúng chỗ, đúng cỡ**, mỗi mảnh "
               "một hình kín có cả phần khuất. Chia mảnh một – một theo con gốc (bảng ở `inbox/rong_vay_ghichu.md`).", "",
               f"Ảnh mẫu của mọi nhóm: ảnh 1 = `{W(chosen())}` (concept đã duyệt, 1536 × 1024, nền trắng: rồng vây thân chàm tím, "
               "vây lam xám, sừng và mỏ đen); ảnh 2 = tờ hướng dẫn của nhóm (1536 × 1024, nền trắng: chính concept "
               "đã xoá mọi thứ ngoài các mảnh của nhóm, đúng chỗ; phần khuất của từng mảnh tô hồng để GPT vẽ bù).", "",
               "Nhóm M (mỏ trên, mỏ dưới, mí mắt nhắm) vẽ rời trên tờ phóng to 6 lần: ảnh 2 của nó là ô mặt của concept phóng 6 lần "
               "(mắt hổ phách bên trái, mỏ đen bên phải).", "",
               "Nhóm S (dải cạnh cánh) chỉ đính concept (ảnh 1) để lấy màu, nét; không có ảnh 2: cột tờ hướng dẫn ghi lại concept.", "",
               "**Nhóm T thay các khúc thân của nhóm B, C, D**: khúc nối nhau phải cắt từ MỘT ảnh cả thân, gen riêng thì vạch bụng "
               "lệch ở chỗ nối. Ảnh 2 của T: concept chỉ còn năm khúc thân, phần thân bị cánh, vây, đầu che tô hồng.", "",
               "**Lượt 3 (tờ P1…): mảnh vẽ đúng khung part của rig.** Ảnh 2: mỗi part một hình bóng phẳng đúng cỡ, đúng hướng như ảnh "
               "part trong rig (không có nét vẽ của game gốc); GPT tô lại theo thiết kế của mình mà giữ nguyên hình bóng. Cắt bằng "
               "`rong_vay.py cat_part P1` → `manh/part/<slot>.png`.", "",
               "| Nhóm | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Mảnh |", "|---|---|---|---|---|"]
        gd += [f"| {X} | `{W(pp)}` | `{W(g)}` | `{W(o)}` | {', '.join(vi)} |" for X, pp, g, o, vi in L2]
        gd += ["", "Kiểm từng ảnh: đủ số mảnh; mảnh không chạm nhau; mỗi mảnh viền mực kín; phần lộ trùng concept; nền trắng tinh. "
               "Sau đó `py -3 -I ArtGen/Spine/rong_vay.py cat` rồi `ghep` để soi ghép khít.", "",
               "| Sai | Gửi thêm |", "|---|---|",
               "| Mảnh dính nhau hoặc thiếu mảnh | `Draw exactly the listed parts, each as its own closed shape, with white "
               "background between them.` |",
               "| Mảnh lệch chỗ, sai cỡ | `Every part must stay in the same position and at the same size as in image 1.` |",
               "| Còn bộ phận khác của con | `Remove everything that is not one of the listed parts.` |"]
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(W(p))
    for X, pp, _, _, _ in L2:
        print(W(pp))


if __name__ == "__main__":
    main()
