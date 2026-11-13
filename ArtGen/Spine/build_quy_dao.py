# -*- coding: utf-8 -*-
"""Gói GPT vẽ quỷ lửa cầm đao lớn (mã làm việc quy_dao, con gốc của rig: monster_3655). Tướng thứ 7 đảo Hỏa.

Người dùng (2026-11-13): "làm tướng thứ 7 đảo hỏa; concept quỷ lửa cầm đao lớn; idle làm khác con gốc đi, walk cũng vậy; tấn công
thường vung đao chém một cách nặng nề nhưng impact lớn; chiêu cast mana làm giống skill_01, có thể đổi nhẹ đi một chút; chiêu cuối làm
giống skill_04_1, lao tới rồi thực hiện liên hoàn chém giống animation gốc; chết, appear bạn có thể tự làm".
Ba hướng màu là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ, cỡ, thứ tự chồng từng part); hình là của
mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (quy_dao_bo_cuc.py).

    py -3 -I ArtGen/Spine/quy_dao_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_quy_dao.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "quy_dao"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
GOLEM = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk():
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{K}")


def save_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "tai_ve")


def mau_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "mau")


def bc():
    return json.load(open(os.path.join(mau_dir(), "bo_cuc.json"), encoding="utf-8"))


def xy(b):
    return f"x = {b[0]} to x = {b[2]}, y = {b[1]} to y = {b[3]}"


def pt(p):
    return f"({p[0]}, {p[1]})"


STANCE = ("STANCE (the same as in the layout guide, image 1): a HULKING, HUNCHBACKED FIRE DEMON BRUTE seen in three-quarter view, "
          "FACING THE VIEWER'S RIGHT and leaning forward. Top-heavy like a gorilla: a massive chest and one ENORMOUS near arm "
          "hanging low in front of the body with a big clawed hand, a huge round shoulder guard on the near shoulder, and short "
          "bent legs. Its small head sits LOW and FORWARD between the shoulders, wearing a horned demon mask, and a huge MANE OF "
          "FIRE streams from the head back over the shoulders and the back. Its far arm reaches up behind the head and grips the "
          "handle of a GIANT DAO (a broad single-edged chopping sabre, longer than the demon is tall) that it carries diagonally "
          "across its back: handle up at the upper left, blade running down behind the body to the lower right, the tip resting "
          "on the ground. Fierce, heavy, ready to strike. Chunky and appealing like a monster-collecting game creature, NOT a "
          "cute smiling mascot, NOT horror, NOT a human knight, NOT a robot.")

BODY = (
    "- THE GIANT DAO (behind everything else; one straight weapon about {dai} px long): its handle end, with a round RING POMMEL, "
    "is at the top at about {chuoi}; the long wrapped handle runs down-right; a small oval hand guard sits at about {chan}; from "
    "there the BLADE runs on down-right to its tip on the ground at about {mui}. The middle of the weapon is hidden behind the "
    "fire mane, the head and the body: you see the ring pommel and the upper handle above the mane (the far hand grips it at "
    "about {ban_tay_xa}), and the lower half of the blade at the lower right (about {ban_dao}). THE BLADE is a dao / giant "
    "cleaver, NOT a sword: ONE cutting edge only, the blade gets WIDER toward the tip (about a quarter as wide as the weapon "
    "is long), a thick straight BACK on the upper-right side with ONE square notch near the tip (about {khac}), and the end "
    "cut off in one slanted line to a point. The cutting edge is the long edge on the LOWER-LEFT side (toward the body): a "
    "band along it is hot orange ({lua1}), as if heated. The blade is {dao_ten}, the guard and ring pommel {vanh_ten}, the "
    "handle wrap {can_ten}. No cross-guard, no second edge, no cracks, no runes, no gems, no flames on the blade.\n"
    "- THE MANE OF FIRE (about {bom}): the demon's hair is living FIRE: five or six huge overlapping locks of flame growing "
    "from the head, sweeping BACK (to the viewer's left) and up, covering the back of the head, the far shoulder and the back, "
    "reaching down behind the shoulder guard to about hip height at the left. Each lock is a real hand-drawn FLAME: a fat body "
    "with two or three pointed tongues whose tips lick up and back. Three nested flat colour zones: red-orange {lua0} outside, "
    "orange {lua1}, yellow {lua2} inside. The mane is a few BIG shapes, not many small ones; no loose sparks.\n"
    "- THE MASK (about {mat_na}, colour {mat_na_ten}): an angular DEMON MASK covering the whole face, turned three-quarters to "
    "the right and tilted down, looking at the enemy. Its top edge rises into a jagged CREST of three blade-like points (the "
    "tallest in the middle, tip about {mao}); a heavy angry brow ridge; under it TWO slanted, narrow, fierce eyes with no "
    "pupils (at about {mat0} and {mat1}), flat bright yellow ({lua2}); a short nose ridge; the chin narrows to a point. No "
    "mouth is visible, no teeth, no tongue, no ears.\n"
    "- THE FIRE BEARD (about {rau}): a short beard of the same fire hangs under the mask and overlaps its lower edge: three or "
    "four small flame tongues pointing down-left.\n"
    "- TWO HORNS (colour {sung_ten}): thick, smooth, cone-shaped bull horns growing from the two upper corners of the mask. "
    "The NEAR horn is the big one: thick base at about {sg_goc} on the left of the mask, curving up to a sharp tip at about "
    "{sg_mui}; it stands IN FRONT of the fire mane. The FAR horn is smaller: base at about {sx_goc} on the right of the mask, "
    "curving up to a tip at about {sx_mui}. Each horn one flat colour with a darker tip; no rings, no cracks.\n"
    "- THE SHOULDER GUARD (about {giap_vai}, colour {giap_ten}): one huge round domed pauldron sitting on the near shoulder, in "
    "FRONT of the mane and the upper arm, like half a big iron ball, with a thick rim band along its lower edge, one round "
    "boss in the middle, and ONE big curved spike rising from its upper left to a tip at about {giap_gai}. No other spikes.\n"
    "- THE BODY (colour {da_ten}): a broad bare chest and belly (about {than}), mostly hidden behind the shoulder guard, the "
    "near arm and the beard. THE NEAR ARM (about {tay_gan}) is the biggest limb: a thick upper arm coming down from under the "
    "shoulder guard, a thick forearm reaching right (about {cang_tay_gan}) wrapped in a chunky armoured bracer ({giap_ten}), "
    "and a big open clawed hand (about {ban_tay_gan}) with four thick curled fingers ending in claws ({vuot_ten}), held in "
    "front of the blade, not touching it. THE FAR ARM goes up behind the head (about {tay_xa}): only its bracer ({giap_ten}) "
    "and the fist gripping the dao handle show above the mane.\n"
    "- THE WAIST AND LEGS: a belt of two or three dark armour plates and a short ragged loincloth (about {dai_lung}; plates "
    "{giap_ten}, cloth {vai_ten}). Two SHORT bent legs with big thighs in ragged shorts and wrapped shins ending in simple "
    "blunt feet ({vai_ten}); near leg about {chan_gan}, far leg about {chan_xa} with a small armour knee cap. Both feet on the "
    "same ground level.")

SIMPLE = ("VERY SIMPLE DESIGN, FEW DETAILS (very important): big clean chunky shapes, each piece ONE flat colour with at most ONE "
          "inner line; NO lava cracks, NO glowing lines or patterns on the skin, NO runes, NO tattoos, NO scars, NO chains, NO "
          "skulls, NO extra spikes, NO extra horns, NO extra flames, NO smoke, NO embers. The ONLY fire-coloured things are: "
          "the mane, the beard, the two eyes and the heated edge band of the dao.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide: the whole figure with its weapon spans from about x = {x0} (the leftmost "
         "flame tip) to x = {x1} (the blade), and from about y = {y0} (the ring pommel at the top) to y = {y1} (the feet and "
         "the blade tip on the ground). Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, "
        "clean resting pose exactly as in the guide. Draw every piece as a clear, simple, closed shape with its own complete ink "
        "outline, so the pieces can be separated: the dao, each lock of the fire mane, the mask, each horn, the beard, the "
        "shoulder guard, the upper arm, the forearm with its bracer, the hand, each finger, the chest, the belt plates, each "
        "thigh, each shin. The pieces touch or overlap but are NOT melted into one blob. No sparks, no embers, no smoke, no "
        "glow, no speed lines, no ground, no props, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram: take ONLY the placement, the sizes, the overlaps and the kind of colour of each "
        "piece from it, never its line, its jagged edges or its exact shapes. Design the real shape of every piece yourself as "
        "described: bold, chunky, readable shapes with a clear silhouette, the way a carefully designed Pokemon-like monster is "
        "drawn. Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (the eyes, the fingers, the handle wrap); every area coloured with coloured pencils and wax crayons, the strokes "
        "visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, "
        "neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no shadows of any kind (no cast shadow of a piece on another, no shadow "
        "under the figure or on the background), no white highlights or shine spots, no gloss, no metal reflections, NO GLOW "
        "around the fire, the eyes or the blade edge, no halo, no rim light, no gradients, no 3D look. The fire looks hot only "
        "because its flat colours are bright.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no effects around the "
      "character.")

LUA = ("#E0441F", "#F7902A", "#FFD45A")
D = {
    "do_tham": dict(
        ten="da đỏ thẫm, mặt nạ + sừng màu ngà, giáp sắt đen",
        da_ten="deep crimson red skin (#B0342C)", giap_ten="black iron (#3E3C44)", vai_ten="dark brown leather (#4E382E)",
        mat_na_ten="ivory bone (#ECE2C8)", sung_ten="pale ivory (#F0E8D4) with a dark-brown tip (#60463C)",
        vuot_ten="pale ivory, #F0E8D4", dao_ten="steel grey (#707682)", vanh_ten="black iron (#3E3C44)",
        can_ten="brown leather (#603E2C)",
        palette=("COLOURS (use exactly these, each area one flat colour): skin deep crimson red (#B0342C); the mask ivory bone "
                 "(#ECE2C8); both horns and the claws pale ivory (#F0E8D4), horn tips dark brown (#60463C); the shoulder guard, "
                 "both bracers, the belt plates and the knee cap black iron (#3E3C44); loincloth, shorts and shin wraps dark "
                 "brown (#4E382E); the dao blade steel grey (#707682) with the heated edge band orange (#F7902A), guard and ring "
                 "pommel black iron, handle wrap brown (#603E2C); the fire red-orange (#E0441F) / orange (#F7902A) / yellow "
                 "(#FFD45A); the eyes yellow (#FFD45A); every outline dark-brown ink (#2B2118). Only these colours: NO blue, NO "
                 "green, NO purple, NO pink."),
        check=["Da **đỏ thẫm**, mặt nạ **ngà**, hai sừng + vuốt **ngà nhạt** (mũi sừng nâu), giáp vai / bao tay / đai **sắt đen**, bản đao **xám thép**."]),
    "than": dict(
        ten="da xám than, giáp đồng, mặt nạ đỏ son, sừng ngà",
        da_ten="charcoal grey skin (#54505C)", giap_ten="warm bronze (#BA783A)", vai_ten="near-black cloth (#342E34)",
        mat_na_ten="lacquer red (#962C26)", sung_ten="pale ivory (#F0E8D4) with a brown tip (#6E5446)",
        vuot_ten="pale ivory, #F0E8D4", dao_ten="dark iron (#464650)", vanh_ten="warm bronze (#BA783A)",
        can_ten="dark red wrap (#6E2C26)",
        palette=("COLOURS (use exactly these, each area one flat colour): skin charcoal grey like cooled coal (#54505C); the mask "
                 "lacquer red (#962C26); both horns and the claws pale ivory (#F0E8D4), horn tips brown (#6E5446); the shoulder "
                 "guard, both bracers, the belt plates and the knee cap warm bronze (#BA783A); loincloth, shorts and shin wraps "
                 "near-black (#342E34); the dao blade dark iron (#464650) with the heated edge band orange (#F7902A), guard and "
                 "ring pommel bronze, handle wrap dark red (#6E2C26); the fire red-orange (#E0441F) / orange (#F7902A) / yellow "
                 "(#FFD45A); the eyes yellow (#FFD45A); every outline dark-brown ink (#2B2118). Only these colours: NO blue, NO "
                 "green, NO purple, NO pink."),
        check=["Da **xám than**, mặt nạ **đỏ son**, sừng + vuốt **ngà**, giáp vai / bao tay / đai **đồng**, bản đao **sắt sẫm**."]),
    "tro": dict(
        ten="da tro nhạt, giáp + mặt nạ sắt đen, sừng đỏ thẫm",
        da_ten="pale warm ash-grey skin (#CEC4BA)", giap_ten="black iron (#3A3840)", vai_ten="dark red cloth (#7C2A26)",
        mat_na_ten="black iron (#322E36)", sung_ten="dark crimson (#842624) with a near-black tip (#461E20)",
        vuot_ten="black iron, #3A3840", dao_ten="blue-grey steel (#585A66)", vanh_ten="black iron (#3A3840)",
        can_ten="dark red wrap (#7C2A26)",
        palette=("COLOURS (use exactly these, each area one flat colour): skin pale warm ash-grey (#CEC4BA); the mask black iron "
                 "(#322E36); both horns dark crimson (#842624) with near-black tips (#461E20); the claws, the shoulder guard, "
                 "both bracers, the belt plates and the knee cap black iron (#3A3840); loincloth, shorts and shin wraps dark red "
                 "(#7C2A26); the dao blade blue-grey steel (#585A66) with the heated edge band orange (#F7902A), guard and ring "
                 "pommel black iron, handle wrap dark red (#7C2A26); the fire red-orange (#E0441F) / orange (#F7902A) / yellow "
                 "(#FFD45A); the eyes yellow (#FFD45A); every outline dark-brown ink (#2B2118). Only these colours: NO bright "
                 "blue, NO green, NO purple, NO pink."),
        check=["Da **tro nhạt**, mặt nạ + giáp + vuốt **sắt đen**, hai sừng **đỏ thẫm**, vải **đỏ sẫm**, bản đao **thép xám lam**."]),
}

CHECK_CHUNG = [
    "Bố cục y sơ đồ: quỷ lưng gù nhìn sang **phải**, đầu thấp chúi tới; tay gần to buông trước, tay xa vòng lên sau đầu nắm cán đao.",
    "**Đao lớn một lưỡi** (không phải kiếm): bản loe dần về mũi, sống thẳng có một khấc, mũi vát; chuôi có khâu tròn ở trên cùng bên "
    "trái, mũi đao chống đất bên phải; dải lưỡi sắc màu cam nằm phía dưới trái (phía thân).",
    "**Bờm lửa** là lửa thật ba vùng màu phẳng, vài búi to tạt về sau; có **râu lửa** ngắn dưới mặt nạ.",
    "**Mặt nạ quỷ** liền, mào ba mũi, hai mắt vàng xếch không con ngươi, không miệng; **hai sừng nón** trơn (gần to, xa nhỏ).",
    "**Giáp vai vòm tròn** to ở vai gần, có vành + một gai cong; bao tay ở cẳng tay gần và tay xa; đai giáp + khố ngắn; hai chân ngắn.",
    "Ít chi tiết: không vết nứt dung nham, không hoa văn trên da, không gai thừa, không lửa thừa.",
    "Tô phẳng, không bóng, **không quầng sáng** quanh lửa; nét bút nâu rung, vân sáp; nền trắng.",
]

FIX = [
    ("Đao thành kiếm hai lưỡi / có chắn tay chữ thập", "The weapon is a DAO: a giant single-edged chopper. One cutting edge only (lower-left side, orange band), thick straight back with one notch, blade widening toward a slanted clipped tip, small oval guard, ring pommel. No cross-guard."),
    ("Quay mặt sang trái / nhìn thẳng", "The demon FACES THE VIEWER'S RIGHT exactly as in the layout guide: mask at the right, fire mane streaming to the left."),
    ("Có quầng sáng / tia lửa bay / khói", "Remove every glow, halo, spark, ember and smoke. Flat colours only."),
    ("Thêm vết nứt dung nham / hoa văn", "Remove all lava cracks, glowing lines, runes and ornaments: each piece one flat colour."),
    ("Mặt có miệng nhe răng / thành mặt người", "The face is a rigid angular MASK with a three-point crest, a heavy brow and two slanted yellow eyes; no mouth, no teeth; a short beard of fire hangs under it."),
    ("Đầu to chibi / dễ thương", "Small head set low between huge shoulders, hulking top-heavy brute, fierce; not chibi, not cute."),
    ("Các mảnh dính liền một cục", "Every piece (dao, each flame lock, mask, horns, shoulder guard, upper arm, forearm, hand, fingers, thighs, shins) is a separate closed shape with its own complete ink outline."),
    ("Có bóng đổ / tô khối", "Flat colour only: no shading, no cast shadow, no highlights, no metal shine."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (the "
         "giant dao behind everything, ring pommel at the top, blade at the lower right; the big fire mane at the left; the "
         "round shoulder guard with one spike; the masked head with two horns low at the right; the fire beard; the big near "
         "arm with bracer and clawed hand; the short legs). Use it for placement, size and overlap only; design and redraw "
         "everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng) ở dáng nghỉ của rig: đao lớn nằm sau cùng (khâu tròn trên cùng, bản "
         "đao dưới phải), bờm lửa to bên trái, giáp vai vòm một gai, đầu mặt nạ hai sừng thấp bên phải, râu lửa, tay gần to có bao "
         "tay và vuốt, chân ngắn. Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (KIEM_SI,
         "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match EXACTLY its wobbly "
         "dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold chunky shapes and its fierce "
         "battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): khỉ samurai giáp lục. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến"),
        (GOLEM,
         "another approved hero of the same game and the same volcano island, a stone golem with flames, 1536x1024, white "
         "background: see how its fire is drawn (three flat colour zones, wobbly ink outline, crayon hatching, no glow). Do NOT "
         "copy its design, its body or its colours.",
         "Golem lõi lửa (tướng 4 đảo Hỏa, đã duyệt; 1536 × 1024, nền trắng): lấy cách vẽ lửa"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


def build_sung():
    """lượt 1b (người dùng 2026-11-13: "tôi thích dạng C nhưng đổi sừng sang đen đậm"): vẽ lại đúng L1_tro.png, chỉ đổi màu hai sừng."""
    src = os.path.join(save_dir(), "L1_tro.png")
    out = os.path.join(save_dir(), "L1b_tro_sung_den.png")
    p = os.path.join(pk(), "luot_1b_sung_den.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(src)}: the current draft of our own game creature (an ash-grey fire demon with a mane of fire, a black mask, "
         "two dark-red horns and a giant dao on its back, facing right), 1536x1024, white background. It is the picture to redraw.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1b_tro_sung_den_2.png, L1b_tro_sung_den_3.png ... in the same folder. Do "
         "not edit, move or delete any other file.", "",
         "TASK: redraw image 1 as the SAME picture, same canvas 1536x1024, changing ONLY ONE THING: the COLOUR of the two horns.", "",
         "KEEP IDENTICAL (if the new picture were laid over image 1, everything must coincide): the whole creature at the same "
         "position and size; every shape and every outline, including the shapes of the two horns themselves; the fire mane and "
         "the fire beard; the black mask with its three-point crest and its two yellow eyes; the round shoulder guard with its "
         "spike; the ash-grey body, arms and clawed hand; the bracers, the belt, the dark-red cloth, the legs; the giant dao with "
         "its ring pommel, wrapped handle and orange edge band; all colours other than the horns; the same wobbly dark-brown ink "
         "outline and visible crayon hatching; completely flat colouring; pure-white background.", "",
         "CHANGE ONLY THIS: the two horns on the head (the big near horn that rises from the left side of the mask in front of the "
         "fire mane, and the smaller far horn at the right side of the mask) are now DEEP BLACK: one flat, very dark charcoal black "
         "(#1E1C21) over the WHOLE horn, base and tip alike. No dark red, no brown, no lighter base, no separate tip colour, no "
         "bands, no rings, no cracks, no highlights, no shine. The crayon hatching stays faintly visible in the black. Keep the "
         "dark-brown ink outline around each horn. The horns must stay clearly separate shapes from the black-iron mask: keep the "
         "ink line between each horn and the mask, and the horns are a little darker than the mask.", "",
         "Do not add or change anything else: no new spikes, no cracks, no glow, no sparks, no smoke, no shadow, no ground line, no "
         "text. No white border or sticker outline around the figure."]
    ghi(p, t)
    print(p)
    return p


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    B = bc()
    x0, y0, x1, y1 = B["_khung"]
    S = B["slot"]
    gd = [f"# Gói gửi GPT: `{CODE}` (quỷ lửa cầm đao lớn, tướng thứ 7 đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3655` (quỷ lửa lưng gù vác kiếm khổng lồ). Ba hướng màu là đề xuất "
          "của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/quy_dao_ghichu.md`.",
          "", "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        body = BODY.format(
            dai=B["dao"]["dai_px"], chuoi=pt(B["dao"]["chuoi"]), chan=pt(B["dao"]["chan"]), mui=pt(B["dao"]["mui"]),
            ban_tay_xa=xy(B["ban_tay_xa"]), ban_dao=xy(B["ban_dao"]), khac=pt(B["dao"]["khac"]), lua0=LUA[0], lua1=LUA[1],
            lua2=LUA[2], dao_ten=d["dao_ten"], vanh_ten=d["vanh_ten"], can_ten=d["can_ten"], bom=xy(B["bom"]),
            mat_na=xy(B["mat_na"]), mat_na_ten=d["mat_na_ten"], mao=pt(B["mao"]), mat0=pt(B["mat"][0]), mat1=pt(B["mat"][1]),
            rau=xy(B["rau"]), sung_ten=d["sung_ten"], sg_goc=pt(B["sung_gan"]["goc"]), sg_mui=pt(B["sung_gan"]["mui"]),
            sx_goc=pt(B["sung_xa"]["goc"]), sx_mui=pt(B["sung_xa"]["mui"]), giap_vai=xy(B["giap_vai"]), giap_ten=d["giap_ten"],
            giap_gai=pt(B["giap_gai"]), da_ten=d["da_ten"], than=xy(B["than"]), tay_gan=xy(B["tay_gan"]),
            cang_tay_gan=xy(B["cang_tay_gan"]), ban_tay_gan=xy(B["ban_tay_gan"]), vuot_ten=d["vuot_ten"], tay_xa=xy(B["tay_xa"]),
            dai_lung=xy(B["dai"]), vai_ten=d["vai_ten"], chan_gan=xy(B["chan_gan"]), chan_xa=xy(B["chan_xa"]))
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              "CREATURE: a FIRE DEMON WITH A GIANT DAO, a fire-element hero of the volcano island in a monster-collecting game: a "
              "hulking horned demon brute with a mane of living fire, a rigid demon mask, one huge armoured shoulder, and a giant "
              "single-edged chopping sabre carried across its back. It is a creature (an elemental monster), NOT a human, NOT a "
              "knight, NOT a robot.", "",
              STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). NEAR = the side of "
              "the body toward the viewer; FAR = the other side, partly hidden. LEFT / RIGHT are the viewer's.", "",
              body, "", SIMPLE, "",
              d["palette"], "", FRAME.format(x0=x0, x1=x1, y0=y0, y1=y1), "", POSE, "", SOFT, LINE, FLAT, BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", "Kiểm riêng hướng này:", ""] + [f"- {c}" for c in d["check"]] + [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/quy_dao_bo_cuc.py all`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sung":
        build_sung()
    else:
        main()
