"""Gói GPT vẽ concept dòng cá đèn lồng (mã tạm `ca_den`, tướng thứ 3 đảo Thủy; người dùng lên ý 2026-11-11, chưa đặt tên).

Ý người dùng: một con cá đèn lồng (cá có bóng đèn chìa ra trước trán) có chân, đuôi thằn lằn; thân, chân, đuôi là MỘT mảng màu
liền như con gốc (không tách màu từng phần cho khỏi dị); mắt và răng có thể làm kiểu con gốc. Đánh thường quật bóng đèn vào đối
thủ; chiêu mana há mồm bắn nước rồi ngậm lại; chiêu cuối nghiêng người đứng một chân, dậm chân kia, há mồm gầm; xuất hiện thì
dùng chân nhảy vào màn; dạng 2 to hơn, chiến hơn. Rig và nhịp animation học từ một con quái cá hai chân của game tham khảo (ghi
chú mổ xẻ: ArtGen/Spine/inbox/ca_den_ghichu.md). Không đính ảnh con gốc vào prompt; thiết kế tả bằng lời; nét vẽ là nét của dự án
(bút mực nâu + chì sáp, tô phẳng).

  dạng 1  cá đèn lồng tròn nhỏ hai chân, đuôi thằn lằn, một bóng đèn
  dạng 2  cùng con, to hơn, chiến hơn (ý người dùng); ảnh mẫu là L1_duyet.png của dạng 1

Lượt 1: concept trọn con một ảnh, miệng khép. Dạng 2 chỉ dựng khi đã có inbox/ca_den_1/tai_ve/L1_duyet.png (bản dạng 1 người
dùng chọn). Lượt 2 (dáng há miệng, lòng miệng, phần khuất của chân, đuôi, cần đèn) viết sau khi người dùng duyệt concept.

    py -3 -I ArtGen/Spine/build_ca_den.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ca_den_1/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ca_den"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
FROG = os.path.join(HERE, "inbox", "ech_xanh_1", "tai_ve", "L1_duyet.png")     # nét, tô sáp phẳng, mặt quả quyết (Thủy, đã duyệt)
SHARK = os.path.join(HERE, "inbox", "vay_lam_1", "tai_ve", "L1_lien.png")      # nét, tô sáp phẳng (Thủy, đã duyệt)


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    """Concept đã chọn của dạng k (chép từ L1_concept*.png sau khi người dùng duyệt)."""
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE = ("COLOURS (use exactly these, each area one flat colour): the whole upper body, the head, the eyelids, the lantern "
           "stalk, both legs, both feet and the whole tail are ONE and the same deep indigo blue (#4C5FC4): one continuous "
           "colour mass, the legs and the tail are NOT a different colour from the body; the three round spots on the back "
           "darker indigo (#34428F); lower jaw, throat and belly pale cream (#F4EBCB, never left as bare white paper); teeth "
           "ivory (#FBF6E6); the lantern bulb warm yellow (#FFD75A); the webbing of the back fin and of the side fin soft "
           "periwinkle (#9BA8F2); eyeballs pale cream (#F4EBCB); pupils dark brown-black (#2B2118) with one tiny white dot "
           "each; every outline dark-brown ink (#2B2118).")

FORM1 = ("CREATURE: a small, plump LANTERN FISH (a deep-sea anglerfish) that WALKS ON TWO SHORT LEGS and has a LIZARD TAIL, a "
         "pet-like battle creature of the water element in a monster-collecting game: iconic, appealing, as simple as "
         "possible, readable at a tiny size. Cute but with a grumpy, determined, ready-to-fight face. It is an original "
         "design: do not imitate any existing franchise character.\n"
         "FORM 1, the first and smallest form:\n"
         "- BODY: head and body are ONE big round shape with NO neck, like a fat round fish that is mostly head and mouth, a "
         "little wider than tall (about 1.2 to 1). The UPPER part (forehead, top and back) is deep indigo blue, like a smooth "
         "cap covering the top and the back (viewer's left) side. The LOWER FRONT part is one big, round, bulging pale-cream "
         "LOWER JAW AND BELLY (jaw, throat and belly are one single round bulge) that takes about half of the front of the "
         "body. The cream part is completely plain: no marks, no folds.\n"
         "- MOUTH: the border between the indigo upper part and the cream lower part at the front IS the mouth: ONE long, "
         "very wide, CLOSED mouth line that runs from the far right edge of the face, across the front, to the left cheek, "
         "with the corners turned DOWN (a grumpy scowl, not a smile). It is an UNDERBITE: the cream lower jaw sticks out a "
         "little further forward than the indigo upper lip.\n"
         "- TEETH: THREE pointed ivory teeth grow from the edge of the cream lower jaw and point UP, lying over the indigo "
         "upper lip: one BIG fang (about 70 px tall, 50 px wide at its base) near the front of the mouth, a little right of "
         "the centre of the body; a medium tooth (about 45 px tall) to the left of it; a small tooth (about 30 px tall) near "
         "the left corner of the mouth. Simple curved cones with their own ink outline, no gums, no upper teeth.\n"
         "- EYES: two big round bulging eyes placed high on the head. The NEAR eye is the bigger one, about 120 px across, on "
         "the upper middle of the head, a little right of the centre; the FAR eye, about 85 px across, sits at the upper "
         "right edge of the head and is partly hidden behind the curve of the head. Each eye: a round pale-cream eyeball "
         "with an ink outline, one big round dark pupil (about half the width of the eyeball) looking toward the viewer's "
         "RIGHT, one tiny white dot in the pupil, and a heavy indigo upper eyelid that covers the top third of the eyeball "
         "and slants down toward the front: a calm, stubborn, battle-ready stare. No eyelashes, no eyebrows.\n"
         "- LANTERN (the signature and the weapon of this creature): from the top of the forehead, just above and between "
         "the eyes, grows ONE long thin flexible STALK, deep indigo like the body, about 16 px thick with its own ink "
         "outline. It rises up, bends FORWARD (toward the viewer's right) in one smooth arc like a fishing rod, and ends in "
         "a round LANTERN BULB that hangs in the air above and in front of the face. The stalk is about 330 px long along "
         "its curve. The bulb is a plump round drop about 100 px across, flat warm yellow, with its own closed ink outline "
         "and a small indigo cap where the stalk joins it. The bulb and the upper two thirds of the stalk are surrounded by "
         "clear white background: the bulb does NOT touch or overlap the face, the eyes or the teeth (at least 50 px of "
         "white between the bulb and the head). The bulb is a plain flat yellow shape: it does NOT glow, no rays, no halo, "
         "no sparkles, no light falling on the face.\n"
         "- FINS: on the back, behind the lantern stalk (upper left of the body), ONE small sail-like back fin: three short "
         "indigo spines joined by periwinkle webbing, about 150 px long and 80 px high, leaning backward. On the side of the "
         "body, behind the left corner of the mouth, ONE small fan-shaped side fin (about 80 px), periwinkle webbing with "
         "indigo ribs, pointing back and slightly down. No other fins.\n"
         "- LEGS: exactly TWO short, sturdy legs under the body, deep indigo like the body, like the hind legs of a little "
         "lizard. The NEAR leg is at the lower-left of the body: a short round thigh that comes out of the body, a short "
         "shin, and a flat foot with three stubby round toes pointing right. The FAR leg is at the lower-right, under the "
         "cream belly: only its shin and its three-toed foot show below the belly. Each leg is about 90 px tall below the "
         "body. No arms, no hands.\n"
         "- TAIL: a LIZARD tail, not a fish tail: it grows out of the lower back of the body on the viewer's left, thick at "
         "its base (about 120 px), and tapers smoothly to a pointed tip, curving up and to the left like a comma. About "
         "300 px long. Deep indigo like the body, with NO fin, NO flame, NO tuft and NO different colour at its end. Clear "
         "white background between the tail and the back fin and between the tail and the near leg.\n"
         "- MARKINGS: three round darker-indigo spots of different sizes (25 to 55 px) on the back, between the back fin "
         "and the tail; flat spots with no outline. No scales pattern, no stripes, no gills drawn, no clothes, no "
         "accessories.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The round body is about 520 px wide and about 430 px tall, its centre a little "
          "right of the centre of the canvas (the tail needs room on the left); the soles of both feet are on one horizontal "
          "level about 130 px above the bottom edge of the image. The lantern stalk rises about 200 px above the top of the "
          "head; at least 70 px of white above its highest point, at least 80 px of white to the right of the bulb and to "
          "the left of the tail tip.")

PALETTE2 = ("COLOURS (use exactly these, each area one flat colour): the whole upper body, the head, the eyelids, the brow "
            "ridges, the lantern stalks, both legs, both feet and the whole tail are ONE and the same dark midnight indigo "
            "(#3A4AA6), clearly darker than image 1: one continuous colour mass; the spots and the tail spikes darker indigo "
            "(#27326F); lower jaw, throat and belly pale cream (#F4EBCB, never left as bare white paper); teeth and toe "
            "claws ivory (#FBF6E6); the lantern bulb deep amber yellow (#FFC233); the webbing of the back fin and of the "
            "side fin periwinkle (#8C9AEE); eyeballs pale cream (#F4EBCB); pupils dark brown-black (#2B2118) with one tiny "
            "white dot each; every outline dark-brown ink (#2B2118).")

FORM2 = ("CREATURE: the GROWN FORM of the walking lantern fish of image 1 (form 1, approved): the same creature, the same "
         "design language and drawing style, in the SAME pose and the same layout of parts, but clearly BIGGER, HEAVIER and "
         "more of a FIGHTER: a burly deep-sea brawler. It must be instantly recognisable as the same line. Tough and "
         "battle-hardened, not cute-chubby, not scary, not evil.\n"
         "FORM 2:\n"
         "- BODY: head and body are still ONE big round mass with no neck, but broader and heavier, about 1.3 times wider "
         "than tall, with a huge heavy lower jaw. The upper part is dark midnight indigo; the lower front is one big round "
         "pale-cream LOWER JAW AND BELLY (one single bulge), completely plain.\n"
         "- MOUTH: exactly as in image 1, the border between the indigo upper part and the cream lower part IS the mouth: "
         "ONE long, very wide, CLOSED mouth line with the corners turned clearly DOWN in a hard scowl; a strong UNDERBITE.\n"
         "- TEETH: FIVE pointed ivory teeth grow from the edge of the cream lower jaw and point UP over the indigo upper "
         "lip: two BIG fangs (about 110 px tall) near the front, and three smaller teeth (40 to 70 px) spaced toward the "
         "left corner of the mouth. Simple curved cones with ink outlines, no gums, no upper teeth.\n"
         "- EYES: the same kind of eyes as in image 1, but SMALLER relative to the body so the body reads as big (near eye "
         "about 120 px across, far eye about 85 px and partly hidden). Each has a heavy indigo upper eyelid that covers the "
         "top HALF of the eyeball and slants steeply down toward the front, rising at its back end into ONE short blunt "
         "BROW RIDGE like a small horn swept backward (about 50 px): a fierce, narrow glare.\n"
         "- LANTERN: as in image 1, ONE stalk growing from the top of the forehead, arching forward to the viewer's right, "
         "but thicker (about 22 px) and longer (about 420 px along its curve), ending in a bigger, heavier bulb about "
         "150 px across, flat deep amber yellow, with an indigo cap that has three short blunt spikes, like a mace. The "
         "bulb does NOT touch or overlap the face (at least 50 px of white around it). It does NOT glow: no rays, no halo, "
         "no sparkles.\n"
         "- FINS: the back fin is taller and sharper than in image 1: four long indigo spines joined by periwinkle webbing, "
         "about 240 px long and 150 px high, leaning backward. One fan-shaped side fin behind the left corner of the mouth, "
         "about 120 px. No other fins.\n"
         "- LEGS: exactly TWO legs in the same places as in image 1, but thick and muscular, each foot with three toes that "
         "end in short blunt ivory claws. No arms.\n"
         "- TAIL: the same LIZARD tail as in image 1, thicker and longer (about 420 px), curving up and to the left, with a "
         "row of four small blunt triangular spikes along its upper edge, getting smaller toward the pointed tip. Same "
         "indigo as the body, NO fin, NO flame and NO different colour at its end.\n"
         "- MARKINGS: five round darker-indigo spots on the back. No scales pattern, no stripes, no scars, no armour, no "
         "clothes, no accessories.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The creature is much bigger in the frame than in image 1: the round body is "
          "about 760 px wide and about 590 px tall, its centre a little right of the centre of the canvas; the soles of both "
          "feet are on one horizontal level about 60 px above the bottom edge of the image. At least 40 px of white above "
          "the highest point of the lantern stalk, to the right of the bulb and to the left of the tail tip.")

POSE = ("VIEW (very important: the picture will be cut into separate parts and animated with a 2D skeleton): three-quarter "
        "view turned toward the viewer's RIGHT, standing still and upright on its two legs, mouth CLOSED, the lantern stalk "
        "in a relaxed smooth arc, the tail relaxed. Not jumping, not leaning, not squashed, not attacking. The only "
        "overlaps are: the teeth over the upper lip, the side fin over the body, the near leg in front of the body, the "
        "root of the lantern stalk on the forehead, and the belly in front of the far leg. No drool, no drops, no bubbles, "
        "no splashes, no puddle, nothing around the creature.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every outer edge, slightly wobbly "
        "like a real pen; closed outlines around the body, each eye, each tooth, the stalk, the bulb, each fin, each leg and "
        "the tail; the mouth line, the eyelid lines and the fin ribs drawn with the same pen, about 5 px. Every area "
        "coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no darker rim, no shadows of any kind (no cast shadow, no shadow "
        "under the figure, under the jaw, on the ground or on the background), no white highlights or shine spots on the "
        "skin, belly, teeth or lantern bulb, no gloss, no wet or slimy look, no reflections, no glow, no rim light, no "
        "gradients, no 3D look. The lantern bulb is NOT a light source in this drawing. The only white dot allowed is the "
        "tiny one inside each pupil. A different tone appears only where the design itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (FROG, "an approved hero of the same game (a green frog), 1536x1024, white background: match EXACTLY its pen line, "
               "crayon texture and flat colouring, and see how simple, round and determined a first form looks. Do NOT copy "
               "its species, design, face, tongue or colours.",
         "Ếch xanh dạng 1 đã duyệt (1536 × 1024, nền trắng): ếch xanh lá tròn, bụng kem, lưỡi đỏ. Chỉ lấy nét bút, vân sáp, "
         "cách tô phẳng, độ đơn giản và vẻ quả quyết"),
        (SHARK, "another approved hero of the same game (a blue shark beast), 1536x1024, white background: the same pen "
                "line and flat crayon colouring on a fish creature. Do NOT copy its species, design, face or colours.",
         "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Chỉ lấy nét bút, vân sáp, cách tô phẳng"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if k == 1:
        return style
    return [(chosen(1), "FORM 1 of THIS creature (approved), 1536x1024, white background: keep its body shape language, its "
                        "pose, the layout of its parts (mouth line = border of indigo and cream, underbite teeth pointing "
                        "up, lantern stalk arching forward from the forehead, back fin, side fin, near leg at the "
                        "lower-left, far leg under the belly, lizard tail on the left), its line and its colouring style. "
                        "Form 2 is the same fish grown big, heavy and fierce; do not simply enlarge it.",
             "Cá đèn lồng dạng 1 đã duyệt (1536 × 1024, nền trắng): cá tròn màu chàm, hàm dưới và bụng kem, răng chĩa lên, cần "
             "đèn vàng vươn ra trước trán, hai chân, đuôi thằn lằn bên trái")] + style


FORMS = {1: ("cá đèn lồng dạng 1 (chưa đặt tên)", FORM1, FRAME1, PALETTE),
         2: ("cá đèn lồng dạng 2 (chưa đặt tên)", FORM2, FRAME2, PALETTE2)}

CHECK = {
    1: ["Một con **cá đèn lồng tròn mập**, đầu liền thân không cổ, hơi rộng hơn cao; nửa trên màu chàm, nửa dưới phía trước là "
        "**hàm dưới và bụng kem to tròn, trơn**.",
        "**Thân, hai chân và đuôi cùng một màu chàm liền mảng** (chân, đuôi không khác màu thân).",
        "**Miệng khép** là đường ranh chàm và kem, rất rộng, hai khoé trễ xuống; hàm dưới chìa ra (**răng hô dưới**): **ba răng "
        "ngà nhọn** mọc từ hàm dưới chĩa lên, đè lên môi trên, một răng nanh to gần phía trước.",
        "Hai **mắt tròn lồi** to đặt cao trên đầu, tròng kem, con ngươi tròn đen to nhìn sang phải, mí trên chàm sụp một phần "
        "ba (mặt lì, quả quyết).",
        "**Cần đèn** mọc từ trán, vươn lên rồi cong ra **phía trước (bên phải)**, cuối cần là **bóng đèn vàng tròn** treo "
        "trước mặt; bóng đèn **không chạm, không đè lên mặt**, có khoảng trắng bao quanh; **không phát sáng, không tia, không quầng**.",
        "Một vây lưng nhỏ ba gai (màng tím nhạt) sau cần đèn; một vây bên nhỏ hình quạt sau khoé miệng.",
        "**Hai chân ngắn** kiểu thằn lằn: chân gần ở dưới trái (đùi, ống, bàn ba ngón), chân xa ló dưới bụng bên phải. Không tay.",
        "**Đuôi thằn lằn** bên trái: gốc to, thon dần tới chóp nhọn, cong lên như dấu phẩy; **không vây, không lửa** ở chóp.",
        "Nhìn nghiêng 3/4 sang **phải**, đứng yên trên hai chân.",
        "Tô phẳng: **không** bóng, không điểm sáng, không ướt bóng; viền mực nâu; nền trắng tinh."],
    2: ["Cùng con với dạng 1, **cùng dáng đứng và cùng cách xếp các phần**, nhưng **to, nặng, bè hơn hẳn** (chiếm gần hết khung), "
        "chàm **đậm hơn**.",
        "Mặt **dữ hơn**: mí sụp nửa mắt, xếch mạnh, mỗi mắt có một **gờ mày nhọn tù**; khoé miệng trễ hẳn; **năm răng**, hai "
        "nanh to. Không ác.",
        "**Cần đèn dày và dài hơn**, bóng đèn to nặng như chuỳ (chụp chàm có ba gai tù); vẫn không chạm mặt, không phát sáng.",
        "Vây lưng cao, bốn gai dài; chân to khoẻ, ngón có vuốt ngà tù; đuôi dày dài hơn, có hàng bốn gai tù dọc sống đuôi.",
        "Thân, chân, đuôi vẫn **một mảng màu liền**; bụng kem trơn.",
        "Nhìn nghiêng 3/4 sang **phải**; tô phẳng, không bóng, không điểm sáng; viền mực nâu; nền trắng tinh."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng trắng trên da, bụng, răng, bóng đèn",
        "Flat colour only: remove every shadow, highlight, shine spot, darker rim and gradient; keep the crayon hatching as "
        "texture only. The only white dot is the tiny one inside each pupil."),
       ("Bóng đèn phát sáng, có tia, có quầng", "The lantern bulb is a plain flat warm-yellow shape with an ink outline: "
                                                "remove every glow, ray, halo and sparkle, and any light on the face."),
       ("Bóng đèn đè lên mặt hoặc chạm đầu", "Move the lantern bulb up and forward so it hangs in the air in front of the "
                                             "face with at least 50 px of white between the bulb and the head; only the "
                                             "root of the stalk touches the forehead."),
       ("Chân hoặc đuôi khác màu thân", "The legs, the feet and the whole tail are exactly the same deep indigo as the upper "
                                         "body: one continuous colour mass, no different colour on them."),
       ("Đuôi cá, đuôi có vây hoặc có lửa", "The tail is a plain LIZARD tail: thick at the base, tapering to a pointed tip, "
                                             "curving up to the left; no fin, no flame, no tuft at its end."),
       ("Miệng há hoặc cười", "The mouth is CLOSED: one long wide line where the indigo meets the cream lower jaw, corners "
                              "turned down, with the lower teeth pointing up over the upper lip."),
       ("Có tay hoặc bốn chân", "Exactly two legs and no arms: the near leg at the lower-left and the far leg under the "
                                "belly at the lower-right. Remove every other limb."),
       ("Quay sang trái hoặc nhìn thẳng", "Turn the creature three-quarters toward the viewer's RIGHT: pupils look right, "
                                          "the far eye is smaller and partly hidden, the tail is on the left, the lantern "
                                          "arches to the right."),
       ("Mặt hiền, cười, quá dễ thương", "Give it a grumpy, stubborn, battle-ready face: heavy upper eyelids slanting down "
                                         "toward the front, mouth corners turned down. Still cute, not scary."),
       ("Quá nhiều chi tiết (vảy, mang, sọc)", "Simplify: no scales, no gills, no stripes; only three flat spots on the "
                                               "back."),
       ("Dạng 2 chỉ là dạng 1 phóng to, vẫn dễ thương", "Form 2 is a burly fighter, not an enlarged baby: heavier jaw, five "
                                                          "teeth with two big fangs, smaller eyes relative to the body, "
                                                          "eyelids covering half of each eye with blunt brow ridges, a "
                                                          "thicker stalk with a heavy mace-like bulb, a taller back fin, "
                                                          "spikes along the tail."),
       ("Dạng 2 đổi dáng, đổi chỗ các phần", "Keep exactly the pose and layout of image 1: standing three-quarters to the "
                                             "right on two legs, mouth closed, lantern arching forward, tail curving up on "
                                             "the left.")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    name, form, frame, palette = FORMS[k]
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
          form, "", palette, "", frame, "", POSE, "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Tướng thứ 3 đảo Thủy, người dùng lên ý 2026-11-11: cá đèn lồng có chân, đuôi thằn lằn, thân chân đuôi một mảng màu; "
          "dạng 2 cùng con, to hơn, chiến hơn. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ca_den_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.", "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK[k]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# ---------------------------------------------------------------- lượt 2: hình HÁ MIỆNG (đổi ảnh khi há, như con gốc)
# Người dùng dặn 2026-11-11: há miệng bằng uốn lưới nhìn chắp vá; con gốc đổi sang hình miệng há vẽ riêng, hai hàm khít nhau ở mép
# bên kia. GPT vẽ lại đúng concept đã duyệt, chỉ đổi miệng; ca_den.py khớp ảnh này vào concept rồi chỉ lấy vùng miệng + hàm.
HA_GIU = ("KEEP IDENTICAL TO IMAGE 1 (same position on the canvas, same size, same shapes, same colours, same line): the canvas "
          "(1536x1024, pure white), the outline of the top of the head and of the back, BOTH EYES with their eyelids{may} and pupils "
          "(same place, same size, same angry look), the lantern stalk and bulb, the back fin, the side fin, the spots on the back, "
          "the tail{gai}, both legs and feet. Do NOT move, turn, tilt, enlarge, shrink or re-pose the creature: if this picture is "
          "laid over image 1, everything except the mouth and the lower jaw must coincide.")

HA_MIENG = ("CHANGE ONLY THE MOUTH AND THE LOWER JAW (the face is seen in the same three-quarter view, we now look INTO the mouth):\n"
            "- UPPER LIP: stays deep indigo. Its lower edge becomes ONE wide smooth ARCH, like the top half of an oval, from the "
            "NEAR mouth corner (viewer's left, in the same place as the left end of the mouth line in image 1, just right of the "
            "side fin) to the FAR mouth corner (viewer's right). The arch stays BELOW the eyes: keep at least 15 px of indigo "
            "skin between each eye outline and the mouth opening.\n"
            "- LOWER JAW: the pale-cream lower jaw DROPS. Its upper rim becomes ONE wide smooth U-shaped curve, like the rim of a "
            "bowl, the bottom half of the same oval. Below the rim the lower jaw and belly stay ONE plain pale-cream shape, as "
            "in image 1; the bottom outline of the belly may hang up to 40 px lower than in image 1 but stays above the soles of "
            "the feet.\n"
            "- THE FAR CORNER (most important): on the viewer's RIGHT the opening does NOT run out to the outline of the body. The "
            "indigo upper lip curves DOWN and the cream rim of the lower jaw curves UP, and they MEET in a closed mouth corner "
            "INSIDE the body, about {mep} px in from the right outline. To the right of that corner the far cheek is visible as a "
            "band of skin: indigo above, cream below, with the ink line of the closed lips between them running from the corner "
            "to the right outline. So the open mouth is ONE CLOSED ROUNDED HOLE, completely surrounded by lips: indigo lip above "
            "and on the upper right, cream jaw rim below and on the lower right. The dark-rose inside of the mouth must NOT touch "
            "the outer outline of the body anywhere.\n"
            "- THE NEAR CORNER (viewer's left): the two lips also meet in a closed pointed corner, at the same place as the left "
            "end of the mouth line in image 1.\n"
            "- SIZE OF THE OPENING: about {rong} px wide and about {cao} px tall at its tallest point (the middle).\n"
            "- INSIDE THE MOUTH: flat dark rose (#B04062). At the back, in the middle, a darker plum throat (#702242) as one soft "
            "rounded shape. On the floor of the mouth a rounded pink tongue (#E27080) with its own ink outline and a short centre "
            "line; the tongue rises a little above the lower rim, behind the lower teeth.\n"
            "- LOWER TEETH: {rang_duoi} They stand on the cream rim, in front of the opening, pointing UP, ivory with ink outlines.\n"
            "- UPPER TEETH: {rang_tren} small pointed ivory teeth hang DOWN from the indigo upper lip arch, pointing down, about "
            "{dai_rang} px long, with ink outlines, spaced so that they would fit between the lower teeth when the mouth closes.\n"
            "- No drool, no spit, no water, no breath, no sound lines, no effects of any kind.")

HA_SO = {
    1: dict(may="", gai="", mep=45, rong=430, cao=200, dai_rang=45, rang_tren="FOUR",
            rang_duoi="the SAME THREE teeth as in image 1 (the big fang toward the viewer's right, the medium tooth in the middle, "
                      "the small tooth near the near corner), the same sizes."),
    2: dict(may=" and brow ridges", gai=" with its spikes", mep=55, rong=560, cao=250, dai_rang=55, rang_tren="FIVE",
            rang_duoi="the SAME FIVE teeth as in image 1 (two big fangs toward the viewer's right, three smaller teeth toward the near "
                      "corner), the same sizes. The front fang stands on the rim just LEFT of the far mouth corner, inside the body "
                      "outline."),
}

CHECK_HA = ["Mọi thứ ngoài miệng **giữ nguyên chỗ, nguyên cỡ**: hai mắt, cần đèn, vây lưng, vây bên, đuôi, chân (chồng lên concept phải trùng).",
            "Miệng há thành **một hốc tròn khép kín**: môi trên chàm vồng lên, vành hàm kem võng xuống.",
            "**Mép bên kia (bên phải)**: môi trên và hàm dưới **gặp nhau, khít lại bên trong viền thân**; bên phải mép là dải má "
            "(chàm trên, kem dưới). Thịt hồng **không chạm viền ngoài**.",
            "Vòm môi **nằm dưới mắt**, không đè lên mắt.",
            "Trong miệng: hồng mận phẳng, họng sẫm ở giữa, lưỡi hồng có viền. Răng dưới đứng trên vành hàm; hàng răng trên nhỏ chĩa xuống.",
            "Tô phẳng, không bóng, không nước dãi, không hiệu ứng; nền trắng tinh."]

FIX_HA = [("Con vật bị dời, đổi cỡ, đổi dáng", "Do not re-pose: the eyes, the lantern, the fins, the tail and the legs must be in exactly "
                                                "the same place and size as in image 1; change only the mouth and the lower jaw."),
          ("Thịt hồng chạy ra tới viền bên phải", "Close the far corner: on the right the indigo upper lip curves down and the cream jaw "
                                                   "rim curves up and they meet INSIDE the body; a band of cheek skin (indigo above, cream "
                                                   "below) separates the mouth from the right outline."),
          ("Miệng đè lên mắt", "Lower the upper lip arch: at least 15 px of indigo skin between each eye and the mouth opening; the "
                               "mouth opens mostly downward."),
          ("Có bóng, điểm sáng, nước dãi", "Flat colours only, no shading, no highlights, no drool or spit.")]


def build_ha(k):
    """lượt 2: hình há miệng của dạng k (cần L1_duyet.png của chính dạng đó)."""
    name = FORMS[k][0]
    refs = [(chosen(k), "the approved creature with its mouth CLOSED, 1536x1024, white background. The new picture is this exact "
                        "picture with only the mouth changed.",
             f"{name} đã duyệt (1536 × 1024, nền trắng), miệng khép")]
    check(refs)
    out = os.path.join(save_dir(k), "M01.png")
    p = os.path.join(pk(k), "luot_2_ha_mieng.txt")
    so = HA_SO[k]
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as M01_2.png, M01_3.png ... in the same folder. Do not edit, move or "
          "delete any other file.", "",
          "TASK: redraw image 1 EXACTLY, changing ONE thing only: the mouth is now WIDE OPEN in a roar. This picture replaces the "
          "mouth area of image 1 for a few frames of a 2D animation, so everything outside the mouth must stay exactly where it is.",
          "", HA_GIU.format(**so), "", HA_MIENG.format(**so), "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k}, lượt 2: hình há miệng", "",
          "Con gốc há miệng bằng cách đổi sang một hình miệng há vẽ riêng (hai hàm khít nhau ở mép bên kia). GPT vẽ lại đúng concept, "
          "chỉ đổi miệng; `ArtGen/Spine/ca_den.py` khớp ảnh này vào concept rồi chỉ lấy vùng miệng và hàm dưới.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_2_ha_mieng.txt` (thêm `--note \"...\"`).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm", ""] + [f"- {c}" for c in CHECK_HA]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX_HA]
    open(os.path.join(pk(k), "HUONG_DAN_luot_2.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


if __name__ == "__main__":
    print("dạng 1:", build_form(1))
    if os.path.exists(chosen(1)):
        print("dạng 2:", build_form(2))
        print("dạng 1, lượt 2 (há miệng):", build_ha(1))
    else:
        print("dạng 2: chưa dựng (chưa có", W(chosen(1)) + ")")
    if os.path.exists(chosen(2)):
        print("dạng 2, lượt 2 (há miệng):", build_ha(2))
