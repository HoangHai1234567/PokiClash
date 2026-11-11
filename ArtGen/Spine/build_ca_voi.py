"""Gói GPT vẽ concept dòng cá voi biến dị (tướng thứ 7 đảo Thủy, 2026-11-11, người dùng lên ý tưởng). Mã làm việc: ca_voi.

Ý người dùng: cá voi biến dị KHÔNG CÓ MẶT như con gốc (cả đầu là một cái miệng tròn đầy nanh), bỏ sừng, cuối đuôi là cụm đá đen
dưới biển (na ná mấy viên pha lê). Con gốc lấy làm DẠNG 2; Claude làm thêm DẠNG 1. idle / die như con gốc; đòn thường lao tới cắn
đớp mạnh (skill_01); chiêu mana lao tới quật đuôi; chiêu cuối há to mồm bắn luồng nước siêu to (skill_02); appear rơi từ trên trời
xuống rồi chống chân đứng dậy; mỗi dạng <= 0,5 MB. Ghi chú và mổ xẻ con gốc: inbox/ca_voi_ghichu.md.
Không đính ảnh con gốc vào prompt; đính sơ đồ bố cục tự vẽ bằng mã (ca_voi_bo_cuc.py). Nét vẽ là nét của dự án.

  dạng 2  (vẽ trước, là dạng bám con gốc) cá voi lưng lam đá sẫm, bụng trắng băng có rãnh họng, miệng tròn 10 nanh, ba mảnh đá đen
  dạng 1  cá voi con mũm mĩm, lam nhạt hơn, miệng 6 nanh nhỏ, hai mảnh đá đen nhỏ; chỉ dựng khi đã có ca_voi_2/tai_ve/L1_duyet.png

    py -3 -I ArtGen/Spine/ca_voi_bo_cuc.py
    py -3 -I ArtGen/Spine/build_ca_voi.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ca_voi_2/luot_1_concept.txt [--note "..."]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ca_voi_1/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ca_voi"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DROP = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")     # tướng khởi đầu Thủy đã duyệt: nét rung, tô phẳng
CLAM = os.path.join(HERE, "inbox", "so_gai_2", "tai_ve", "L1_duyet.png")      # sò đột biến dạng 2 đã duyệt: nanh, lòng miệng


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    return os.path.join(save_dir(k), "L1_duyet.png")


def ref2():
    """Ảnh dạng 2 làm mẫu cho dạng 1: bản đã duyệt nếu có, chưa thì bản concept mới nhất (gen thử dạng 1 để duyệt cả hai một lượt)."""
    if os.path.exists(chosen(2)):
        return chosen(2)
    c = [f for f in os.listdir(save_dir(2)) if f.startswith("L1_concept") and f.endswith(".png")] if os.path.isdir(save_dir(2)) else []
    return max((os.path.join(save_dir(2), f) for f in c), key=os.path.getmtime) if c else chosen(2)


def draft2():
    """Bản nháp dạng 2 người dùng đã xem và góp ý (2026-11-11: bỏ sọc trắng, đuôi đừng cụt, chân nối liền móng)."""
    p = os.path.join(save_dir(2), "L1_concept_2.png")
    return p if os.path.exists(p) else None


def guide(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau", "bo_cuc.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
NOFACE = ("NO FACE (the key idea of this creature): it has NO eyes, NO eyebrows, NO nose, NO nostrils on the front, NO cheeks, "
          "NO expression marks anywhere. Where a head would be there is only ONE ENORMOUS ROUND GAPING MOUTH ringed with big "
          "fangs. Do not draw any eye, dot or shape that could be read as an eye, anywhere on the body. Also NO horns, NO "
          "ears, NO dorsal fin, NO whiskers, NO tongue. NO white rings, bands or stripes anywhere on the tail or the limbs.")

PALETTE2 = ("COLOURS (use exactly these, each area one flat colour): back, upper jaw dome, tail stock and both flipper-legs deep "
            "slate navy (#2F4A6E); the thick upper-lip band sea blue (#4F86B0); lower jaw and belly ice white (#E6F1F4, never "
            "left as bare white paper); the wave-crest band along the bottom of the belly sea blue (#4F86B0); throat-groove "
            "lines soft blue (#8FB8CC); inside of the mouth in TWO flat tones: the roof of the mouth (upper half) dark plum "
            "(#8E2A55), the floor of the mouth (lower half) coral pink-red (#E2607A); all fangs and the three barnacles cream "
            "(#FBF1D2); the rock tail fluke, the small rock studs and all six claws charcoal black (#26252C) with flat facets "
            "of dark grey (#5A5866); the blowhole a short dark ink slit; every outline dark-brown ink (#2B2118). NO white or "
            "pale rings, bands, stripes, scars or vein lines anywhere on the navy parts or on the rock.")

FORM2 = ("CREATURE: a MUTANT WHALE monster of the water element for a monster-collecting game: a small deep-sea whale that "
         "mutated: its whole head became one giant fanged maw, its two flippers became clawed legs it stands on, and its tail fluke turned "
         "into black sea rock. A heavy, dangerous, battle-ready beast: bold shapes, a rich but readable design with "
         "clear character, NOT a simple mascot and NOT an empty diagram.\n"
         + NOFACE + "\n"
         "FORM 2, the grown form. Follow the LAYOUT GUIDE (image 1) closely for the construction, the placement, the size "
         "and the shape of every part listed here:\n"
         "- VIEW: three-quarter side view. The creature faces the viewer's RIGHT and a little toward the viewer: the mouth "
         "end is at the RIGHT, the tail at the LEFT. We look partly INTO the open mouth.\n"
         "- SILHOUETTE: a heavy WEDGE, like a door-stop: tallest and bulkiest at the right (the mouth end, about 580 px "
         "tall), and from the top of the head the BACK runs as one long, almost straight diagonal line down to the LEFT, "
         "continuing into a long tapering whale tail that floats above the ground at the far left. The belly lies low, almost on the "
         "ground. No neck: the body is basically two long jaws hinged in the middle of the body.\n"
         "- UPPER JAW: a thick navy dome like a helmet or the front of a skull. It arches over the mouth and its right side "
         "curves down around the front of the mouth like a cheek guard, ending at the front corner of the mouth. Along its "
         "whole mouth edge runs a THICK UPPER-LIP BAND of lighter sea blue, about 40 px wide.\n"
         "- LOWER JAW: a deep ice-white bowl, like a scoop: a thick lower lip, a rounded chin jutting out at the lower right.\n"
         "- THE MOUTH OPENING is NOT a round disc. It is a big tilted egg / teardrop shape, about 380 px wide and 400 px "
         "tall, wide and round at the right (front) and narrowing toward the left into a long SHARP POINTED CORNER: the back "
         "corner of the mouth is a pointed wedge that reaches far left into the body, to just above the near flipper, like a "
         "gash where the two jaws hinge. From the tip of that wedge the seam between the navy upper jaw and the ice-white "
         "lower jaw continues a little further left as an ink line and disappears behind the near flipper.\n"
         "- INSIDE THE MOUTH: two flat tones, no gradient: the ROOF of the mouth (upper half, including the pointed back "
         "corner) is dark plum; the FLOOR of the mouth (lower half) is coral pink-red; the border between the two tones is "
         "one soft curved edge running from the back corner to the front. No tongue, no throat hole, no uvula.\n"
         "- FANGS, the star of the design: TEN HUGE cream fangs, like tusks, FIVE hanging from the upper lip and FIVE "
         "standing on the lower lip. They are FAT, slightly CURVED and CROOKED, each a different size and leaning a little "
         "differently, like the teeth of a deep-sea predator, not neat equal triangles. Wide rounded roots, blunt-sharp "
         "tips. Upper row from back (left) to front (right): medium (about 130 px long), large (about 160 px), the BIGGEST "
         "(about 190 px long and 130 px wide, with one short crack line on it), large (about 150 px), and one small fang "
         "(about 70 px) at the front corner. Lower row from back to front: medium (about 110 px), large (about 140 px), the "
         "BIGGEST lower fang, a curved hook (about 170 px), large (about 140 px), and one small fang half hidden behind the "
         "last one. The ROOT of every fang sits ON the lip and overlaps it outward (the roots cover parts of the lip band); "
         "neighbouring fangs touch or slightly overlap at their roots. Together the fangs cover about half of the mouth "
         "opening. The two rows INTERLOCK like a zipper: each upper tip points down into the gap between two lower fangs "
         "and each lower tip points up into the gap between two upper fangs, but an upper fang NEVER touches or covers a "
         "lower fang: a zigzag band of mouth colour at least 15 px wide always stays between the two rows. Every fang has "
         "its own closed ink outline.\n"
         "- WHALE MARKS: a BLOWHOLE (one short dark ink slit, about 40 px) on top of the head, left of the highest point, "
         "nothing coming out of it; THREE small cream BARNACLES (little cone bumps) in a loose row on the back, halfway "
         "down the slope; TWO thin soft-blue THROAT GROOVE lines under the chin following the curve of the lower jaw. No "
         "scar lines, no white streaks on the head.\n"
         "- BELLY WAVE BAND: along the bottom of the ice-white lower jaw, between the near flipper and the chin, runs a sea-blue "
         "band whose upper edge is cut into TWO curling WAVE CRESTS (pointed, hooked tongues like breaking waves) pointing "
         "toward the RIGHT; thin ink outline.\n"
         "- TWO FLIPPER-LEGS: the whale's two side fins (pectoral flippers) have become thick, strong props it stands on, "
         "like the front flippers of a walrus. They are plain navy, the same colour as the back, with NO band, ring or "
         "stripe on them.\n"
         "- NEAR FLIPPER (in FRONT of the body): it hangs from the middle of the body, just left of the back corner of the "
         "mouth, and stands on the ground. Shaped like a broad paddle: a POINTED ELBOW sticking up at its top, then the "
         "blade widens downward (about 170 px wide at the top, about 230 px wide at the bottom, about 270 px tall), with "
         "its OWN closed ink outline drawn over the body and one fold line down its middle. Its lower end resting on the "
         "ground is split into THREE rounded knuckle lobes, like a mitten with three fat toes.\n"
         "- CLAWS GROW OUT OF THE FLIPPER: from under each knuckle lobe one chunky black rock claw sticks out and touches "
         "the ground: a blunt faceted triangle about 70 px tall, charcoal with one dark-grey facet. The navy knuckle lobe "
         "overlaps and wraps the root of its claw like a fingertip around a nail, so flipper and claws read as ONE limb. "
         "There is NO band, NO gap and NO separate ankle between the flipper and its claws.\n"
         "- FAR FLIPPER (BEHIND the lower jaw): the same kind of flipper on the far side, mostly hidden behind the chin: "
         "only its lower part shows to the right of the chin, ending on the ground in three knuckle lobes with THREE rock "
         "claws of the same kind, at the lower right.\n"
         "- Exactly these two flipper-legs are visible; no other legs or fins.\n"
         "- TAIL, long and whale-like, NOT a short stump: behind the near flipper the body keeps tapering smoothly toward "
         "the LEFT into a long, strong tail stock, like the tail of a real whale: about 150 px thick where it leaves the "
         "body, narrowing evenly over about 380 px of length to about 45 px thick at its end, floating above the ground "
         "and curving very slightly upward at the tip. Plain navy all along: no rings, no stripes. Two or three small "
         "black rock studs (little pointed chips) grow on it near its end, where the rock begins.\n"
         "- TAIL FLUKE OF BLACK ROCK: the tail ends in a real whale TAIL FLUKE: two wide pointed lobes spreading apart "
         "like a V with a notch between them, one lobe sweeping UP-LEFT and one sweeping DOWN-LEFT, each about 250 px "
         "long, the whole fluke about 430 px from tip to tip. But the fluke has turned into rough BLACK SEA ROCK (like "
         "black basalt or obsidian from the deep sea floor): each lobe is one big angular slab with straight broken "
         "edges and a sharp point, cut in flat facets like a rough crystal: charcoal black with a flat dark-grey facet "
         "along its front edge, one straight ridge line between the two tones. Matte rock: not glass, not gems, no "
         "sparkle, no highlights, no light lines.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The whole creature is about 1220 px wide from the tips of the rock fluke (far "
          "left, about x = 170) to the claws of the far flipper (far right, about x = 1390), and about 520 px tall from the top "
          "of the head (about y = 360) to the claws on the ground (about y = 880). The upper tip of the fluke reaches up to "
          "about y = 500.")

PALETTE1 = ("COLOURS (use exactly these, each area one flat colour; lighter and friendlier than form 2): back, upper jaw dome, "
            "tail stock and both flipper-legs medium sea blue (#4F86B0); the thick upper-lip band light sky blue (#7EB0D2); "
            "lower jaw and belly ice white (#E6F1F4, never left as bare white paper); the wave-crest band along the bottom of "
            "the belly light sky blue (#7EB0D2); throat-groove lines soft blue (#8FB8CC); inside of the mouth in TWO flat "
            "tones: the roof of the mouth (upper half) rose plum (#C45478), the floor of the mouth (lower half) soft coral "
            "pink (#F08A96); all fangs and the barnacles cream (#FBF1D2); the rock tail fluke, the rock stud and all six claws "
            "charcoal black (#26252C) with flat facets of dark grey (#5A5866); the blowhole a short dark ink slit; every "
            "outline dark-brown ink (#2B2118). NO white or pale rings, bands, stripes, scars or lines anywhere on the blue "
            "parts or on the rock.")

FORM1 = ("CREATURE: the YOUNG, FIRST FORM of the mutant whale monster of image 1 (form 2, the grown form, approved): the same "
         "creature, the same construction and the same drawing style, but a small, chubby calf: rounder, much shorter, "
         "lighter in colour, with fewer and smaller fangs and a small tail fluke. Cute but already bold and ready to bite: "
         "its big mouth is wide open.\n"
         + NOFACE + "\n"
         "FORM 1. Follow the LAYOUT GUIDE (image 2) for the construction, the placement and the size of the parts, and make "
         "every shape a little rounder and chubbier than the guide:\n"
         "- VIEW: the same three-quarter side view as image 1: the mouth end at the RIGHT facing right and a little toward "
         "the viewer, the tail at the LEFT. We look partly INTO the open mouth.\n"
         "- SILHOUETTE: a short, plump wedge: a big round head end at the right (about 440 px tall), the back sloping down "
         "to the left in a gentle curve into a short tapering tail. Compared with image 1 the body is much SHORTER from "
         "mouth to tail: the mouth end is about half of the whole length, so the calf looks big-headed and baby-like. The "
         "belly lies low on the ground.\n"
         "- UPPER JAW and LOWER JAW built exactly as in image 1: a rounded sea-blue helmet dome arching over the mouth, with "
         "a thick UPPER-LIP BAND of light sky blue (about 30 px wide) along its mouth edge and a cheek guard curving down "
         "at the right; below it the ice-white bowl of the lower jaw with a thick lower lip and a round chin.\n"
         "- THE MOUTH OPENING, as in image 1: a big tilted egg shape, about 300 px wide and 310 px tall, round at the right "
         "and narrowing at the left into a SHARP POINTED back corner that reaches into the body to just above the near "
         "flipper; from its tip the seam between the blue upper jaw and the ice-white lower jaw runs a little further left "
         "and disappears behind the near flipper.\n"
         "- INSIDE THE MOUTH: two flat tones, no gradient: the ROOF (upper half, including the pointed back corner) rose "
         "plum; the FLOOR (lower half) soft coral pink; one soft curved border between them. No tongue, no throat hole.\n"
         "- FANGS: only SIX baby fangs, cream: THREE hang from the upper lip and THREE stand on the lower lip. Short, fat, "
         "rounded milk teeth, slightly crooked and each a little different, about 80 to 110 px long (much smaller than in "
         "image 1: they cover only about a quarter of the mouth opening, so a lot of the inside of the mouth shows). The "
         "root of each fang sits ON the lip and overlaps it outward. They do NOT touch each other; upper and lower fangs "
         "are far apart. Every fang has its own closed ink outline. No crack lines.\n"
         "- WHALE MARKS: a BLOWHOLE (one short dark ink slit) on top of the head, nothing coming out of it; THREE tiny "
         "cream BARNACLES on the back; TWO thin soft-blue THROAT GROOVE lines under the chin.\n"
         "- BELLY WAVE BAND: along the bottom of the ice-white lower jaw, between the near flipper and the chin, a light "
         "sky-blue band whose upper edge is cut into TWO small curling WAVE CRESTS pointing toward the right; thin ink "
         "outline.\n"
         "- TWO FLIPPER-LEGS, as in image 1 but shorter and stubbier: the whale's two side fins used as props. Plain sea "
         "blue, NO band or stripe. NEAR FLIPPER (in front of the body, just left of the back corner of the mouth): a broad "
         "little paddle with a small POINTED ELBOW at its top, widening downward (about 130 px wide at the bottom, about "
         "220 px tall), its OWN closed ink outline, one fold line down its middle; its lower end on the ground is split "
         "into THREE rounded knuckle lobes. From under each knuckle lobe one small black rock claw sticks out and touches "
         "the ground (a blunt faceted triangle about 45 px tall, charcoal with one dark-grey facet); the knuckle lobe "
         "overlaps and wraps the root of its claw, so flipper and claws read as ONE limb, with no band and no gap. FAR "
         "FLIPPER (behind the lower jaw): only its lower part shows to the right of the chin, ending in three knuckle "
         "lobes with THREE small rock claws.\n"
         "- Exactly these two flipper-legs; no other legs or fins.\n"
         "- TAIL: behind the near flipper the body tapers smoothly toward the LEFT into a short whale tail stock (about "
         "200 px long, about 100 px thick where it leaves the body, about 35 px at its end), floating above the ground. "
         "Plain sea blue, no rings. ONE small black rock stud grows on it near its end.\n"
         "- SMALL TAIL FLUKE OF BLACK ROCK: the tail ends in a small whale tail fluke: two pointed lobes spreading apart "
         "like a V with a notch between them, one sweeping up-left and one down-left, each about 140 px long. The fluke "
         "has turned into rough BLACK SEA ROCK: each lobe is one angular slab with straight broken edges and a sharp "
         "point, charcoal black with a flat dark-grey facet along its front edge. Matte rock, no sparkle, no light lines.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The calf is clearly SMALLER in the frame than form 2: about 760 px wide from the "
          "tips of the rock fluke (about x = 440) to the claws of the far flipper (about x = 1195), and about 440 px tall from "
          "the top of the head (about y = 430) to the claws on the ground (about y = 870).")

POSE = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): standing still, "
        "propped on its two flipper-legs, in a calm, clean resting pose, mouth wide open. Every part is fully visible and "
        "clearly separated by ink outlines: the upper jaw, the lower jaw, every single fang, the near flipper, every claw, "
        "the tail, each lobe of the rock fluke. The tail and its fluke do not touch the flipper or the ground. Nothing crosses in front of the mouth. No water, no "
        "bubbles, no drool, no spray, no splashes, no breath, no sand, no rocks on the ground.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves, not perfect ellipses; the ink line is visibly "
        "wobbly and uneven in thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside "
        "every area. The layout guide is a stiff flat computer diagram: take the construction, the placement, the shapes "
        "and the proportions from it, never its mechanical line or its empty flat fills.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every edge, a closed outline "
        "around every part; every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal "
        "hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, few details, neither a "
        "crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the figure, "
        "on the ground or on the background), no white highlights or shine spots, no gloss, no wet look, no reflections, no "
        "glow, no rim light, no gradients, no 3D look. No depth shading inside the mouth: only the flat tones the design lists for it. A different "
        "tone appears only where the design itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (DROP, "an approved hero of the same game (a water-blob creature), 1536x1024, white background: match EXACTLY its "
               "wobbly pen line, its visible crayon hatching and its completely flat colouring. Do NOT copy its species, "
               "design, face or colours.",
         "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng"),
        (CLAM, "another approved hero of the same game (a spiky clam), 1536x1024, white background: see how fangs and the "
               "flat inside of a mouth are drawn simply in this style. Do NOT copy its species, eyes, design or colours.",
         "Sò đột biến dạng 2 đã duyệt (1536 × 1024, nền trắng): sò gai chàm, vành cam, nanh kem. Lấy cách vẽ nanh, lòng miệng phẳng"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    g = (guide(k), "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing how it is "
                   "built, where every part goes on the canvas, its shape and how big it is (the wedge body, the helmet-like "
                   "upper jaw with its lip band, the bowl-like lower jaw, the egg-shaped mouth with its pointed back corner "
                   "and two-tone inside, each huge fang, the belly wave band, the two flipper-legs with their claws, the "
                   "long tapering tail, the black rock tail fluke). Follow it closely; redraw everything in the hand-drawn style "
                   "of the approved heroes.",
         f"Sơ đồ bố cục dạng {k} tự vẽ bằng mã (1536 × 1024, nền trắng): hình phẳng cá voi hình nêm quay phải, không mặt, miệng "
         "quả trứng có khoé nhọn, nanh kem rất to đan cài, hàm trên lam sẫm, hàm dưới trắng băng có dải sóng lam, hai vây ngực làm "
         "chân có móng đá, đuôi dài thon dần và vây đuôi đá đen hai thuỳ. Lấy cách dựng, bố cục, tỉ lệ")
    if k == 2:
        d = draft2()
        if d:
            return [g, (d, "PREVIOUS DRAFT of THIS creature, 1536x1024, white background. KEEP from it, as they are: the head, "
                           "the helmet-like upper jaw and its lip band, the lower jaw, the egg-shaped mouth with its pointed "
                           "back corner and two-tone inside, all ten fangs (their sizes, shapes and places), the barnacles, "
                           "the blowhole, the belly wave band, the throat grooves, the colours, the wobbly ink line and the "
                           "crayon hatching. CHANGE only what the text below describes: the tail (now long, tapering, ending "
                           "in a rock whale fluke), the two legs (now flipper-legs whose knuckles wrap the claws), and REMOVE "
                           "every white ring, band and line (tail rings, ankle band, the two white lines on the head, the "
                           "blue lines on the rock). The whole creature is drawn a little smaller to make room for the tail, "
                           "as in the layout guide.",
                     "Bản nháp trước của dạng 2 (1536 × 1024, nền trắng): cá voi lam sẫm không mặt, nanh kem rất to; đuôi còn cụt, "
                     "có khoanh trắng. Giữ đầu, miệng, nanh, màu, nét; chỉ đổi đuôi, chân, bỏ sọc trắng")] + style
        return [g] + style
    return [(ref2(), "FORM 2 of THIS creature (the grown form, approved), 1536x1024, white background: keep its "
                        "construction (no face, the helmet-like upper jaw with a lip band, the bowl-like lower jaw, the "
                        "egg-shaped mouth with a pointed back corner and a two-tone inside, fangs sitting on the lips, the "
                        "belly wave band, the two flipper-legs whose knuckles wrap black rock claws, the tapering whale tail "
                        "ending in a black rock fluke), its view and its drawing style. Form 1 is the same creature as a "
                        "small chubby calf.",
             "Cá voi biến dị dạng 2 đã duyệt (1536 × 1024, nền trắng): cá voi lam sẫm không mặt, miệng quả trứng 10 nanh kem rất "
             "to, hai vây ngực làm chân có móng đá, đuôi dài kết thúc bằng vây đuôi đá đen"), g] + style


FORMS = {2: ("cá voi biến dị dạng 2", FORM2, PALETTE2, FRAME2), 1: ("cá voi biến dị dạng 1", FORM1, PALETTE1, FRAME1)}

CHECK = {
    2: ["**Không có mặt**: không mắt, mũi, mày; cả đầu là cái miệng há to. **Không sừng**.",
        "Dáng **hình nêm** quay sang phải: đầu cao bên phải, lưng chéo thẳng xuống đuôi bên trái.",
        "Miệng **hình quả trứng nghiêng có khoé nhọn** kéo dài sang trái vào thân; lòng miệng hai tông: vòm họng tím sẫm ở trên, "
        "sàn miệng hồng san hô ở dưới.",
        "Hàm trên là vòm lam sẫm như mũ sọ, có **dải môi trên lam nhạt dày**; hàm dưới là cái bát trắng băng, cằm nhô.",
        "**Mười nanh kem rất to, cong, to nhỏ không đều** (một nanh trên to nhất có vết nứt), gốc đè lên môi; hai hàng **đan cài "
        "như khoá kéo nhưng không chạm nhau**.",
        "Nét cá voi: lỗ phun, ba con hà trên lưng, hai rãnh họng dưới cằm, **dải sóng lam hai ngọn** dọc đáy bụng.",
        "**Hai vây ngực dùng như chân chống**: vây gần có mỏm khuỷu nhọn, bản vây rộng dần xuống, đầu vây chia ba mấu; **mỗi mấu "
        "ôm gốc một móng đá** (không có khoanh, khe hở giữa vây và móng); vây xa lộ sau cằm.",
        "**Đuôi dài thon dần như đuôi cá voi thật** (không cụt), trơn một màu lam sẫm; chót đuôi là **vây đuôi hai thuỳ bằng đá "
        "đen** nhiều mặt cắt, có khe chữ V; vài mẩu đá nhỏ ở chỗ nối.",
        "**Không còn sọc, khoanh trắng** ở đuôi, vây; không vết sẹo trắng, không vân sáng trên đá.",
        "Tô phẳng: **không** bóng, không điểm sáng; viền mực nâu; nền trắng tinh; không nước, bong bóng."],
    1: ["Cùng con, cùng cách dựng với dạng 2 nhưng là **cá voi con**: thân ngắn mũm mĩm, đầu to, màu lam nhạt hơn; nhỏ hơn hẳn "
        "trong khung.",
        "Vẫn **không có mặt**; miệng quả trứng có khoé nhọn, lòng miệng hai tông hồng (trên sẫm, dưới nhạt).",
        "Chỉ **sáu nanh sữa** (ba trên, ba dưới), ngắn mập, không chạm nhau; lộ nhiều lòng miệng.",
        "Hai vây ngực làm chân chống, ngắn mập; **mấu vây ôm gốc móng đá**, không khoanh trắng.",
        "Đuôi ngắn thon dần, trơn; chót là **vây đuôi đá đen nhỏ hai thuỳ**; một mẩu đá nhỏ trên lưng đuôi.",
        "Dải môi trên lam nhạt, dải sóng bụng, lỗ phun, ba con hà nhỏ, hai rãnh họng.",
        "Tô phẳng, không bóng, không sọc trắng, nền trắng tinh."],
}

FIX = [("Có mắt, mũi hoặc nét mặt", "Remove every eye, nose and face mark: the creature has NO face at all, only the giant "
                                    "round mouth."),
       ("Có bóng, mảng sáng tối, điểm sáng, lòng miệng tối dần", "Flat colour only: remove every shadow, highlight, shine spot "
                                                                 "and gradient; the inside of the mouth is one flat coral "
                                                                 "colour; keep the crayon hatching as texture only."),
       ("Có lưỡi, họng, nước dãi trong miệng", "The inside of the mouth is completely empty: one flat coral area, no tongue, "
                                               "no throat, no drool."),
       ("Nanh hàng trên đè lên nanh hàng dưới", "The two rows of fangs interlock like a zipper but never touch: keep a zigzag "
                                                "band of mouth colour at least 15 px wide between the upper fangs and the "
                                                "lower fangs."),
       ("Nanh nhỏ, đều tăm tắp, hiền", "Make the ten fangs HUGE, fat, curved and crooked, each a different size, covering about "
                                       "half of the mouth opening, like the teeth of a deep-sea predator."),
       ("Miệng tròn như cái đĩa", "The mouth opening is a tilted egg shape with a long sharp pointed back corner reaching left "
                                  "into the body, as in the layout guide; inside: dark plum roof above, coral floor below."),
       ("Thiếu chi tiết, trông sơ sài", "Add every listed detail: the thick upper-lip band, barnacles, scars, blowhole, throat "
                                        "grooves, the two wave crests on the belly band, the kite-shaped thigh with a pointed "
                                        "knee and ankle band, the tail rings and the faceted rock shards with a vein."),
       ("Có sừng, vây lưng", "Remove horns and the dorsal fin."),
       ("Còn sọc, khoanh trắng ở đuôi hoặc vây; còn vết sẹo, vân sáng", "Remove every white or pale ring, band, stripe, scar and "
                                                                         "vein line from the tail, the flippers, the head and "
                                                                         "the rock: these parts are plain flat colour."),
       ("Đuôi ngắn cụt", "Make the tail long and whale-like: a tail stock that tapers smoothly over about 380 px before the rock "
                         "fluke, as in the layout guide."),
       ("Móng rời khỏi vây (có khoanh hoặc khe hở)", "The three knuckle lobes at the end of each flipper overlap and wrap the roots "
                                                     "of the three rock claws: one continuous limb, no band, no gap."),
       ("Đá đuôi bóng loáng như đá quý, hoặc tròn như sỏi", "The rock fluke is matte black sea rock: two angular slabs with "
                                                            "straight broken edges and flat dark-grey facets, no sparkle, no "
                                                            "shine."),
       ("Quay sang trái hoặc nhìn nghiêng hẳn (không thấy lòng miệng)", "Three-quarter view facing the viewer's RIGHT and a "
                                                                        "little toward the viewer: we look straight into "
                                                                        "the round open mouth, tail at the left."),
       ("Bốn chân", "Only two flipper-legs are visible: the near flipper under the middle of the body and the lower part of "
                    "the far flipper beside the chin."),
       ("Dạng 1 không khác dạng 2 mấy", "Make form 1 a small chubby calf: much shorter body, big round mouth end, lighter "
                                        "blue, only six short milk fangs and a small rock fluke.")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    name, form, palette, frame = FORMS[k]
    refs = refs_of(k)
    check(refs)
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do "
          "not edit, move or delete any other file.", "",
          "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of "
          "the approved hero images.", "",
          form, "", palette, "", frame, "", POSE, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Tướng thứ 7 đảo Thủy, làm 2026-11-11 theo ý người dùng: cá voi biến dị không có mặt, bỏ sừng, chót đuôi là đá đen "
          "dưới biển. Dạng 2 bám con gốc, dạng 1 là cá voi con. Ghi chú thiết kế và mổ xẻ con gốc: "
          "`ArtGen/Spine/inbox/ca_voi_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự vẽ (`py -3 -I ArtGen/Spine/ca_voi_bo_cuc.py`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK[k]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


def main():
    print(W(build_form(2)))
    if os.path.exists(ref2()):
        print(W(build_form(1)), "(mẫu dạng 2:", os.path.basename(ref2()) + ")")
    else:
        print("dạng 1: chưa dựng, chờ ảnh dạng 2 trong", W(save_dir(2)))


if __name__ == "__main__":
    main()
