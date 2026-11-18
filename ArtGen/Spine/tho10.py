# -*- coding: utf-8 -*-
"""Tướng 10 đảo Thổ (ải 70, FINAL BOSS, id game hiện `giap_nham`): người dùng 2026-11-18 chọn con gốc `monster_3802` (khổng lồ đá nổi, lõi
đen nứt tím, hai nắm đấm rời) và dặn "con này ổn nhưng tôi muốn bạn cải tiến nó thêm nữa, chiến hơn nữa, lạ hơn". Ba hướng cải tiến của
Claude trên cùng một rig, chờ người dùng chọn. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai.

    tho10.py ca_con          hình cả con gốc khung 0 idle → inbox/thach_de_1/mau/goc_ca_con.png (+ .json)
    tho10.py slot            bảng slot (thứ tự vẽ, ảnh, xương, khung trên ảnh ca_con)
    tho10.py concept         file prompt ba hướng → gui_gpt/thach_de_1/luot_1_concept_<k>.txt + HUONG_DAN.md
    tho10.py so_goc          chồng viền hình bóng con gốc lên concept, in IoU → inbox/thach_de_1/mau/_so_goc.png

Mã làm việc: `thach_de`. Rig: 134 xương, 108 slot, 15 clip (generate_01 trồi từ đất, skill_01_1..3, skill_02..05); hầu hết tảng đá là mảnh
cứng một xương (P_*_shitou*, P_R_beiji*, P_*_xiaobi*, P_*_shouzh*), thân P_shenti01/02 và đầu P_tou1/2 là lưới.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
import tho9  # noqa: E402

CODE, MON = "thach_de", "monster_3802"
tho5.CON[CODE] = (MON, 10, 70)

_I = os.path.join(HERE, "inbox")
QUY = os.path.join(_I, "quy_nui_1", "tai_ve", "L1_duyet.png")
TINH = os.path.join(_I, "tinh_hach_1", "tai_ve", "L1_duyet.png")
REFS = [
    (QUY, "an approved EARTH hero of our game (a four-armed rock ape), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen "
          "line, its crayon hatching and how big heavy rock is drawn in our style (one flat front-face tone, one darker side-face tone, "
          "nothing else). Do NOT copy its design or its brown colours.",
     "Vượn núi đá bốn tay (tướng 5 đảo Thổ) đã duyệt: lấy nét bút mực rung, vân sáp, cách vẽ đá nặng hai tông"),
    (TINH, "another approved EARTH hero of our game (a dark meteor beast with crystals), 1536x1024, white background: match EXACTLY how dark "
           "rock, flat vein cracks and flat faceted crystals are drawn in our style, and its fierce narrow eye. Do NOT copy its design or its "
           "colours.",
     "Thiên Thạch Thú (tướng 9 đảo Thổ) đã duyệt: lấy cách vẽ đá sẫm, mạch nứt phẳng, tinh thể phẳng, mắt hẹp dữ"),
]

GOC_VI = "Con gốc `monster_3802` (khổng lồ đá nổi: lõi tròn đen nứt tím, đá trắng bọc ngoài, đầu nhỏ mặt nạ trắng có sừng, hai nắm đấm rời)"
GOC_EN = tho9._goc("a colossus made of floating rocks: a round black core with glowing purple cracks, white stone slabs round it, a small "
                   "head with a white mask and horns, two huge detached fists, two tiny legs")

MOOD = ("MOOD: this is the FINAL BOSS of the earth island, the ruler of every earth creature, and must look MORE EPIC, MORE FIERCE AND "
        "STRANGER than all of them: an ancient, colossal, battle-ready titan with a striking silhouette and bold colour contrast, a furious "
        "scowl, mature proportions (NOT chibi, NOT a cute mascot, no smile), but still a clean stylised creature for a family game: no "
        "gore, no blood, no skulls, no bones.")

TASK = ("TASK: REDESIGN the rock colossus of image 1 into OUR OWN, FIERCER AND STRANGER final boss: {sv}. Image 1 is the guide for the POSE "
        "and the BODY PLAN (the new character will be animated with the same skeleton): keep its pose, its facing, its size and place on the "
        "canvas, the huge round core, the small low head, the two enormous detached fists, the two tiny legs and the idea of separate "
        "rocks floating close together. KEEP that body type, but every rock, the head, the crest and the fists get the NEW shapes, "
        "materials and colours described below; someone who knows image 1 must see a clearly different, more dangerous creature. Like in "
        "image 1 the rocks float close to each other with only small white gaps between them; no piece is missing.")

PLAN = ("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 260-1280, y 115-910: a hunched colossus leaning "
        "forward, facing the viewer and a little to the RIGHT. The CORE is one huge round boulder in the centre (x 496-1030, y 151-640) with "
        "a smaller belly / waist block under it (x 534-882, y 504-723). The HEAD is small and LOW, in front of the core at the centre right: "
        "the face is about x 870-980, y 400-610 (jaw at y 515-611), and its horns / head crest spread round it within x 687-1091, y 291-570. "
        "A BACK CREST of about ten tall pieces stands in a row along the top of the core (x 607-957, y 115-458), tallest in the middle. "
        "LEFT SHOULDER (viewer's left): a cluster of big floating pieces at x 333-599, y 162-553. LEFT ARM: a big forearm boulder reaching "
        "down-left (x 277-590, y 409-842) ending in a giant FIST resting on the ground (knuckle and finger stones at x 417-683, y 646-887). "
        "RIGHT SHOULDER (viewer's right): a cluster of floating pieces at x 975-1173, y 243-592. RIGHT FIST: a huge round boulder floating "
        "at the lower right, detached from the body (x 977-1279, y 472-855), with a row of finger stones under it (x 926-1194, y 729-909). "
        "Two TINY short legs under the core: x 474-629, y 670-880 and x 745-870, y 667-871, with a hip block between them (x 578-756, "
        "y 685-812).")

HUONG = {
    # ------------------------------------------------------------------------------------------------------------------------------
    "A": dict(
        ten="Tam Thủ Thạch Vương (hai nắm đấm là hai đầu thú)",
        vi=("Hai NẮM ĐẤM thành hai ĐẦU NGHÊ ĐÁ khổng lồ há mồm (các đốt ngón tay thành hàm răng dưới): con ba đầu, đấm là cắn. Đá bọc màu "
            "ngà, vết nứt hàn VÀNG (kintsugi) thay mạch tím, lõi bazan than, ngọc bích ở mắt và trán; đầu thật đội vương miện ba lưỡi ngọc, "
            "nanh vểnh; hàng đá lưng thành quạt lưỡi đá ngà mũi vàng"),
        sv=("a THREE-HEADED STONE KING: its two giant fists are two colossal carved GUARDIAN-BEAST HEADS that bite, and its broken stones "
            "are mended with gold"),
        doi=["FISTS (new, the signature): each fist is a giant carved stone GUARDIAN-LION HEAD (like the stone lion-dogs that guard old "
             "temples), facing RIGHT, as big as the boulder it replaces: a heavy scowling brow, ONE fierce eye visible (iris jade green "
             "#2FA37A, black slit pupil, one small white dot), a flat broad nose, a short curly stone mane of three or four chunky rock "
             "curls at the back, and a WIDE OPEN JAW: the row of finger stones under the boulder becomes the LOWER JAW with four or five big "
             "blunt stone fangs pointing up, and the boulder has matching upper fangs. Ivory stone #EDE6D6 (side faces #BFB5A3), the inside "
             "of the mouth dark charcoal #35303A. The left one rests on the ground, the right one floats. No arms join them to the body.",
             "CORE: a huge round boulder of dark charcoal basalt #35303A (side faces #25212A), wrapped by big ivory stone plates #EDE6D6 "
             "(side faces #BFB5A3). Every crack of the core and of the plates is filled with a flat GOLD seam #E2A93B, like broken pottery "
             "mended with gold: a few bold branching seams, not a fine net. NO purple, no glow.",
             "HEAD (new): a small fierce stone-beast face of ivory stone, short muzzle, two tusks #F4EAD2 jutting up from the lower jaw, two "
             "fierce narrow jade-green eyes (iris #2FA37A, black slit pupil, one small white dot) under a heavy angry brow; on top a CROWN "
             "of three tall flat JADE crystal blades #2FA37A (side faces #1E7A5A) set in a gold band #E2A93B; two thick dark basalt horns "
             "curve forward beside the face.",
             "BACK CREST (new): a fan of tall, straight-edged ivory stone BLADES like a rising sun, each tipped with a flat gold cap "
             "#E2A93B.",
             "SHOULDERS: on each side three big ivory slabs stacked like the plates of a pauldron, each crossed by one gold seam, with one "
             "flat jade crystal #2FA37A between them.",
             "LEGS: tiny, dark basalt with ivory knee stones and gold seams.",
             "PALETTE (flat): ivory stone #EDE6D6 / #BFB5A3, charcoal basalt #35303A, gold #E2A93B, jade green #2FA37A."]),
    # ------------------------------------------------------------------------------------------------------------------------------
    "B": dict(
        ten="Thổ Tinh (lõi hành tinh có vành đá)",
        vi=("Lõi tròn thành một HÀNH TINH ĐÁ kẻ dải ngang (kem, vàng đất, đỏ gạch) có VÀNH ĐÁ nghiêng bay quanh như sao Thổ; đá bọc và vành "
            "màu đá phiến xanh đen; tinh thể thạch anh tím thay mạch tím; đầu là mặt nạ chiến sừng trâu rộng, nanh; nắm đấm cắm gai tinh "
            "thể tím ở khớp; hàng đá lưng thành vương miện trụ thạch anh tím"),
        sv=("a living RINGED PLANET of rock: its round core is a banded stone planet circled by a tilted ring of orbiting boulders, with "
            "amethyst crystal weapons"),
        doi=["CORE (new, the signature): the huge round core is a smooth STONE PLANET with flat HORIZONTAL BANDS running round it like the "
             "bands of a gas giant: cream #EAD7AE, ochre #D9A441 and brick red #B5532F, six or seven bands of different widths, with ONE "
             "big dark oval storm spot #7A3A26 on it. No cracks on the core, no glow.",
             "RING (new, the signature): a wide, flat, TILTED RING of orbiting rocks circles the core like the ring of Saturn, tilted so "
             "that it runs from the lower left (about x 430, y 560) up across the FRONT of the core to the upper right (about x 1080, "
             "y 300) and back round behind it: twelve to sixteen angular slate boulders of different sizes with small gaps between them, "
             "dark blue-grey slate #3F4656 (side faces #2B303D). The ring passes BEHIND the head.",
             "ARMOUR ROCKS: the shoulder clusters and the forearm are big angular slabs of the same dark slate #3F4656 (side faces "
             "#2B303D), each with one or two flat AMETHYST crystals #8E5BD0 (side faces #5E3A99) growing out of it. No purple cracks, no "
             "glowing veins.",
             "HEAD (new): a fierce WAR MASK of pale bone-cream stone #EFE4CC: a broad angry brow, two fierce narrow amber eyes (iris "
             "#F6C443, black slit pupil, one small white dot), a jutting lower jaw with two big tusks; two HUGE dark slate HORNS sweep out "
             "sideways and curve up like the horns of a water buffalo, much wider than the face; one flat amethyst rhombus on the forehead.",
             "BACK CREST (new): a crown of seven tall faceted AMETHYST crystal pillars #8E5BD0 (side faces #5E3A99) of different heights, "
             "tallest in the middle, growing from a slate base.",
             "FISTS: two enormous slate boulder fists with big squared knuckle stones of cream stone #EFE4CC; three short amethyst crystal "
             "spikes on the knuckles of each fist.",
             "LEGS: tiny, dark slate with cream knee stones.",
             "PALETTE (flat): banded core cream #EAD7AE / ochre #D9A441 / brick red #B5532F, dark slate #3F4656, amethyst #8E5BD0, "
             "bone-cream #EFE4CC, amber eyes #F6C443."]),
    # ------------------------------------------------------------------------------------------------------------------------------
    "C": dict(
        ten="Nhãn Sơn (con mắt trong lõi núi)",
        vi=("Giữ bộ màu đen / trắng / tím của con gốc. Lõi tròn nứt toạc một khe lớn, bên trong là MỘT CON MẮT KHỔNG LỒ nhìn ra (con thật "
            "nằm trong lõi; đầu nhỏ chỉ là mặt nạ): idle hé, tung chiêu thì mở to. Mặt nạ đổi thành mặt quỷ đá sừng cong lớn, nanh; hàng đá "
            "lưng thành vương miện lưỡi thạch anh tím; nắm đấm có gai tinh thể; mạch tím thành mạch nứt phẳng"),
        sv=("a mountain with a living EYE inside: its round black core is split by a great crack through which ONE GIANT EYE glares out; "
            "the small masked head is only its war mask"),
        doi=["CORE (new, the signature): the huge round core is black volcanic rock #2E2A36 (side faces #1F1C26). On its LEFT-FRONT face "
             "(about x 530-720, y 330-540, the part not hidden by the head) it is split by ONE wide jagged almond-shaped CRACK, and inside "
             "the crack sits ONE GIANT FIERCE EYE looking to the right: flat violet iris #A66BE0, a tall black slit pupil, ONE small white "
             "dot, a flat pale lilac eyeball #E9DDF5, the upper edge of the crack cutting across the top of the eye like an angry eyelid. "
             "The edges of the crack are jagged rock teeth. A few flat violet vein cracks #8E5BD0 branch away from the eye across the core "
             "(bold, few, flat; NOT glowing).",
             "ARMOUR ROCKS: big angular slabs of white limestone #EEEAF2 (side faces #B9B2C6) float round the core on the shoulders and the "
             "forearm, sharper and more blade-like than in image 1, each rooted in black rock.",
             "HEAD (new): a fierce stone DEMON WAR MASK, white limestone #EEEAF2: a heavy angry brow, two narrow slanted eye slits filled "
             "with flat violet #A66BE0 (no pupils: it is a mask), a wide jaw with a row of jagged stone fangs and two tusks; two BIG black "
             "horns curve up and forward from the temples, much bigger than in image 1; a jagged black rock mane behind the mask.",
             "BACK CREST (new): a crown of nine tall, sharp AMETHYST crystal blades #8E5BD0 (side faces #5E3A99) fanning out along the top "
             "of the core, tallest in the middle, with small white limestone shards between their bases.",
             "FISTS: two enormous black boulder fists crossed by flat violet vein cracks, with big white limestone knuckle and finger "
             "stones; on each fist a row of three sharp amethyst crystal spikes over the knuckles.",
             "LEGS: tiny, black rock with white knee stones and one violet crack each.",
             "PALETTE (flat): black volcanic rock #2E2A36, white limestone #EEEAF2 / #B9B2C6, amethyst violet #8E5BD0 / #5E3A99, eye iris "
             "#A66BE0."]),
}


def concept():
    Wp = tho5.Wp
    G = tho5.dat(CODE)
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, GOC_EN, GOC_VI)] + REFS
    hd = ["# Gói GPT: tướng 10 đảo Thổ (ải 70, final boss), ba hướng cải tiến trên rig `monster_3802`", "",
          "Người dùng (2026-11-18) chọn con gốc `monster_3802`: \"con này ổn nhưng tôi muốn bạn cải tiến nó thêm nữa, chiến hơn nữa, lạ "
          "hơn\". Ba hướng dưới đây cùng một rig, cùng dáng; khác nhau ở điểm nhấn lạ và bộ màu. Ảnh mẫu 1 là hình con gốc: chỉ dùng "
          "trong máy, không đăng công khai. Gen qua Magnific (GPT 2.6, 1k high, 3:2, 95 credit / ảnh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} (1536x1024, nền trắng) |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, h in HUONG.items():
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{CODE}_1", f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", TASK.format(sv=h["sv"]), "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in h["doi"]] + ["", tho9.style2(), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no flying debris, no glow, no aura round the character, no "
              "smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"## Hướng {k}: {h['ten']}", "", h["vi"] + ".", "",
               f"File prompt: `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", ""]
        print(p)
    hd += ["Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: cùng dáng, cùng hướng, cùng chỗ các khối to như ảnh 1 (lõi tròn, đầu nhỏ thấp, hai nắm đấm rời, hai chân bé) nhưng nhìn "
           "ra con KHÁC và dữ hơn; mắt có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng, mạch nứt KHÔNG "
           "phát sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"it still looks like image 1: change the head, the crest and the fists more\"; \"remove the shading / "
           "highlights / glow, flat colour only\"; \"the cracks must be flat colour, not glowing\"; \"keep the fists detached and as big "
           "as in image 1\"."]
    tho5.ghi(os.path.join(HERE, "gui_gpt", f"{CODE}_1", "HUONG_DAN.md"), hd)


# ----------------------------------------------------------------------------------------------------------------------------------
# Lượt 2 (2026-11-18): người dùng "concept B lấy hành tinh làm lõi rất hay nhưng có thể phát triển thêm nữa cho nhất quán hơn, các bộ phận
# cùng các rải đá xung quanh nhìn chưa được hợp". Bản B có bốn kiểu hình không liên quan: lõi nhẵn kẻ dải, đá phiến đen góc cạnh, tinh thể
# tím, chuỗi sỏi làm vành. Giữ lõi hành tinh; ba cách làm MỌI bộ phận cùng một thế giới với lõi (mỗi cách chỉ hai chất liệu + một màu nhấn).
B_DUYET = os.path.join(_I, f"{CODE}_1", "tai_ve", "L1_B.png")
REF_B = (B_DUYET, "OUR previous concept of this character (1536x1024, white background). The art director LOVES its idea: the round core is "
                  "a BANDED STONE PLANET. Keep that idea. He REJECTED the rest because it is not consistent: the dark angular slate "
                  "blocks, the purple crystals and the thin chain of pebbles look like parts of a different creature. Do NOT keep those "
                  "blocks, those crystals, that chain of pebbles, its ape-like face or its symmetric front-on pose.",
         "Concept B lượt 1 (người dùng thích lõi hành tinh; chê bộ phận và dải đá không hợp): chỉ lấy ý lõi hành tinh kẻ dải")

TASK2 = ("TASK: REDESIGN our ringed-planet colossus of image 4 so that the WHOLE creature is ONE consistent idea: {sv}. Keep the banded stone "
         "planet as the core. Every other part (shoulders, back crest, forearm, fists, legs, head, ring) must visibly belong to the same "
         "world as that planet, built from the SAME few materials listed below and nothing else. Image 1 is the guide for the POSE and the "
         "BODY PLAN (the character will be animated with the same skeleton): keep its three-quarter pose leaning forward, its facing, its "
         "size and place on the canvas, the huge round core, the small low head, the two enormous detached fists (the one on the viewer's "
         "left bigger, lower and resting on the ground; the one on the right floating), the two tiny legs and the idea of separate pieces "
         "floating close together with only small white gaps. It must NOT look like a recolour of image 1.")

COMMON2 = ["CORE (keep the idea of image 4, but make it read as ROCK, not a gas planet): the huge round core is a STONE PLANET with flat "
           "horizontal bands of rock strata running round it, their edges gently wavy: sand cream #EAD7AE, ochre #D9A441, terracotta "
           "#B5532F and umber #7A4A2E, six or seven bands of different widths. NO oval storm spot. Two or three shallow round craters on "
           "it, each one flat darker tone. No cracks, no glow.",
           "REMOVE: no purple, no amethyst, no crystals of any kind, no plain dark slate blocks, no chain of small pebbles, no extra "
           "materials or colours beyond the palette.",
           "HEAD: NOT an ape, NOT a gorilla, NOT a human face: a horned stone BEAST MASK with a short broad muzzle like a bull-lion, a "
           "heavy angry brow, two fierce narrow amber eyes (iris #F6C443, black slit pupil, one small white dot) and a jutting lower jaw "
           "with two big cream tusks #F4EAD2."]

HUONG2 = {
    "B1": dict(
        ten="Vỏ hành tinh vỡ",
        vi=("Hành tinh phá vỡ lớp VỎ sẫm của chính nó: mọi bộ phận là mảnh vỏ CONG ôm theo mặt cầu, mặt ngoài nâu than, mép vỡ lộ đúng các "
            "dải địa tầng của lõi; vành là hai làn mảnh vỏ dẹt xếp thành elip rõ; sừng kẻ khoang cùng màu dải lõi; hàng đá lưng là mảnh vỏ "
            "dựng toả như vương miện. Hai chất liệu: đá dải + vỏ sẫm"),
        sv=("a stone planet that has BURST OUT OF ITS OWN DARK CRUST: every body part is a thick CURVED piece of that broken crust, and the "
            "broken edges show the same banded strata as the planet"),
        doi=["CRUST (the one other material): thick plates of dark umber-slate rock #4B4048 (side faces #332B33). Wherever a plate is "
             "broken, its thick EDGE shows three flat strata stripes, cream #EAD7AE, ochre #D9A441 and terracotta #B5532F, the same bands "
             "as the planet, like a slice of layered rock. This banded edge appears on EVERY crust piece: it is what ties the creature "
             "together.",
             "SHOULDERS: on each side two or three big CURVED crust plates, like pieces of a broken eggshell, floating just off the "
             "sphere and following its curve (concentric with the core), the bigger one on the viewer's left.",
             "BACK CREST: a row of nine tall crust shards standing along the top of the core and fanning outward like a crown, tallest in "
             "the middle, each with its banded edge facing the viewer.",
             "RING: a wide, flat, TILTED RING drawn as one clear ellipse round the core, like the ring of Saturn: TWO concentric lanes of "
             "flat crust shards (dark tops, banded edges), bigger shards in the outer lane. Its front arc crosses in FRONT of the lower "
             "half of the core from the left (about x 400, y 520) to the right (about x 1120, y 430); its back arc passes BEHIND the core "
             "and behind the head.",
             "FISTS AND FOREARM: each fist is a huge rounded crust boulder (dark, with one banded broken edge); the knuckle and finger "
             "stones are squared blocks cut from the planet's banded stone, each showing two or three bands.",
             "HORNS: two huge horns sweep out sideways and curve up, wider than the face, ringed with the planet's bands (cream, ochre, "
             "terracotta rings along their length), dark umber tips. The mask itself is dark crust with cream tusks.",
             "LEGS: tiny, dark crust with one banded knee block each.",
             "PALETTE (flat): strata bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F / umber #7A4A2E, dark crust #4B4048 / "
             "#332B33, tusks #F4EAD2, amber eyes #F6C443."]),
    "B2": dict(
        ten="Thổ Tinh và các vệ tinh",
        vi=("Lõi là hành tinh, hai NẮM ĐẤM là hai MẶT TRĂNG tròn đầy hố, vai là hai vỏ trăng khuyết ôm lõi, hàng đá lưng là các lưỡi trăng "
            "khuyết, cặp sừng ghép thành một vầng trăng lưỡi liềm; vành là MỘT DẢI PHẲNG liền (elip rõ, hai làn màu) có vài viên đá trăng "
            "cưỡi trên. Hai chất liệu: đá dải + đá trăng xám hoa cà"),
        sv=("a stone PLANET WITH ITS MOONS: the core is the planet, the two fists are two cratered MOONS, and every other piece is moon "
            "rock shaped like a crescent"),
        doi=["MOON ROCK (the one other material): pale grey-lilac rock #CFC8D6 (side faces #9D95AB) with a few flat round craters "
             "#B3ABC0. Every piece that is not the planet or the ring is this moon rock.",
             "FISTS (the signature): each fist is a round cratered MOON, a clean sphere of moon rock with four or five flat craters; under "
             "it a row of chunky rounded moon-rock knuckle stones. The moon on the viewer's left is bigger and rests on the ground, the "
             "right one floats. The forearm on the left is a smaller half-moon chunk behind its fist.",
             "SHOULDERS: on each side one big thick CRESCENT-shaped shell of moon rock (a broken half moon) cupping the core, its horns "
             "pointing up, with one smaller crescent above it.",
             "BACK CREST: a crown of seven tall CRESCENT BLADES of moon rock standing along the top of the core, curved like sickle "
             "moons, tallest in the middle, all curving the same way.",
             "RING: a wide, flat, TILTED RING like the ring of Saturn, drawn as ONE SOLID FLAT BAND in a clean ellipse round the core with "
             "TWO colour lanes (inner lane cream #EAD7AE, outer lane ochre #D9A441) and a thin gap between them; five or six small "
             "moon-rock chunks ride on it. Its front arc crosses in FRONT of the lower half of the core from the left (about x 400, "
             "y 520) to the right (about x 1120, y 430); its back arc passes BEHIND the core and behind the head.",
             "HORNS: the two horns of the mask curve up and inward so that together they make ONE big upward CRESCENT MOON above the "
             "face, moon rock with umber tips. The mask is moon rock with cream tusks.",
             "LEGS: tiny, moon rock, one small crater each.",
             "PALETTE (flat): strata bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F / umber #7A4A2E, moon rock #CFC8D6 / "
             "#9D95AB, tusks #F4EAD2, amber eyes #F6C443."]),
    "B3": dict(
        ten="Hỗn thiên nghi đá",
        vi=("Hành tinh nằm trong bộ VÒNG ĐÁ CHẠM của một cỗ máy thiên văn cổ (hỗn thiên nghi): một vòng rộng nghiêng như vành sao Thổ nhưng "
            "là vòng đá liền có khía vuông, một vòng dựng sau lưng mà hàng đá lưng là răng khía của nó; vai là cung vòng gãy; nắm đấm là "
            "khối găng đá có đai vòng; đinh ngọc bích. Hai chất liệu: đá dải + sa thạch chạm, nhấn ngọc bích"),
        sv=("a stone planet held inside the carved STONE HOOPS of an ancient astronomers' ARMILLARY SPHERE that has come alive: every body "
            "part is a piece of those carved hoops"),
        doi=["CARVED STONE (the one other material): pale carved sandstone #E3D3B0 (side faces #B39F78), cut in clean geometric shapes "
             "with squared edges, like parts of an ancient stone instrument. The only decoration: a row of evenly spaced SQUARE NOTCHES "
             "along the rims, and a few flat square JADE studs #2FA37A.",
             "RING (the signature): a wide, flat, TILTED HOOP of carved sandstone round the core, like the ring of Saturn but ONE SOLID "
             "carved ring with square notches along its outer rim and six jade studs. Drawn as a clean ellipse: its front arc crosses in "
             "FRONT of the lower half of the core from the left (about x 400, y 520) to the right (about x 1120, y 430); its back arc "
             "passes BEHIND the core and behind the head. The hoop is broken in one place, with a gap.",
             "BACK CREST: the top arc of a second, UPRIGHT hoop stands behind the core like a halo, and on it a row of nine tall squared "
             "stone TEETH (like the teeth of a great gear or a sundial crown), tallest in the middle.",
             "SHOULDERS: on each side two thick curved ARC SEGMENTS broken from a hoop, stacked like pauldrons, notched rims, one jade "
             "stud each.",
             "FISTS AND FOREARM: each fist is a massive squared sandstone GAUNTLET block with four big squared knuckle stones, wrapped by "
             "one narrow notched stone band with a jade stud; the fist on the viewer's left bigger, resting on the ground.",
             "HORNS: two huge horns sweep out sideways and curve up, wider than the face, carved sandstone with three notched bands; one "
             "square jade stud on the forehead of the mask. The mask is carved sandstone with cream tusks.",
             "LEGS: tiny, carved sandstone blocks.",
             "PALETTE (flat): strata bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F / umber #7A4A2E, carved sandstone #E3D3B0 / "
             "#B39F78, jade #2FA37A, tusks #F4EAD2, amber eyes #F6C443."]),
}


def concept2():
    Wp = tho5.Wp
    G = tho5.dat(CODE)
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, GOC_EN, GOC_VI)] + REFS + [REF_B]
    p_hd = os.path.join(HERE, "gui_gpt", f"{CODE}_1", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n")
    hd = hd[:hd.index("## Lượt 2: phát triển hướng B cho nhất quán (2026-11-18)") - 1] if any(x.startswith("## Lượt 2") for x in hd) else hd
    hd += ["", "## Lượt 2: phát triển hướng B cho nhất quán (2026-11-18)", "",
           "Người dùng: \"concept B lấy hành tinh làm lõi rất hay nhưng có thể phát triển thêm nữa cho nhất quán hơn, các bộ phận cùng các "
           "rải đá xung quanh nhìn chưa được hợp\". Giữ lõi hành tinh; mỗi bản chỉ hai chất liệu.", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} (1536x1024, nền trắng) |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, h in HUONG2.items():
        out = os.path.join(G.TAI, f"L2_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{CODE}_1", f"luot_2_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L2_{k}_2.png, L2_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", TASK2.format(sv=h["sv"]), "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in COMMON2[:1] + h["doi"] + COMMON2[1:]] + [
              "", tho9.style2(), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no flying debris, no glow, no aura round the character, no "
              "smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **{k} {h['ten']}**: {h['vi']}. File prompt `{Wp(p)}`; ảnh lưu `{Wp(out)}`."]
        print(p)
    tho5.ghi(p_hd, hd)


# ----------------------------------------------------------------------------------------------------------------------------------
# Lượt 3 (2026-11-18): người dùng "b3 khá đẹp nhưng có thể lược bỏ vành đai đi hoặc đổi sang đá di chuyển xung quanh, concept là 1 chuyện
# nhưng bạn phải chắc chắn về tính khả thi của animation, animation cũng cần phải thật lạ, độc đáo nhưng cũng phải thật đẹp". Giữ B3, hai
# bản: X bỏ hẳn vành; Y thay vành bằng năm viên đá then (keystone) bay quanh lõi (trước lõi to, sau lõi nhỏ: làm bằng slot trước / sau như
# hành tinh của Nhật Vương). Cả hai: dáng ba phần tư lệch như rig, ít khía chạm hơn, vòng răng dựng sau lõi thành BÁNH RĂNG tròn đủ (xoay
# từng nấc như kim đồng hồ: một ảnh sau lõi, chỉ cần khoá xoay), lõi có ba hố (hố trôi ngang dưới mặt nạ tròn = hành tinh tự quay).
B3_DUYET = os.path.join(_I, f"{CODE}_1", "tai_ve", "L2_B3.png")
TASK3 = ("TASK: REDRAW our approved character concept (image 2) with a few changes. KEEP its design: the banded stone planet as the core, "
         "the pale carved sandstone parts with square notches and flat square jade studs, the toothed stone hoop standing upright behind "
         "the core, the stacked arc-shaped shoulder pieces, the squared gauntlet fists with their notched band, the horned beast mask with "
         "amber eyes and tusks, the colours and the hand-drawn style. Image 1 is the original rig character from another game: use it ONLY "
         "for the POSE (the character is animated with its skeleton); do not copy its shapes or colours.")
CHUNG3 = ["POSE (change): the three-quarter, lopsided pose of image 1, not the symmetric front-on pose of image 2: the body leans forward "
          "and faces a little to the RIGHT; the fist on the viewer's LEFT is clearly BIGGER and LOWER, resting on the ground in front "
          "(about x 280-690, y 410-890); the fist on the viewer's RIGHT is smaller and FLOATS higher (about x 930-1280, y 470-910); the "
          "left shoulder pieces are bigger and nearer (x 333-599, y 162-553) than the right ones (x 975-1173, y 243-592); the small head "
          "sits low in front of the core at the centre right (face about x 870-980, y 400-610); two tiny legs under the core.",
          "CORE: the huge round banded stone planet exactly as in image 2 (x 496-1030, y 151-640), a perfect circle, with exactly three "
          "shallow round craters; nothing is carved on it.",
          "GEAR HALO (change): the upright hoop behind the core becomes one complete round stone GEAR standing behind the planet, a little "
          "bigger than the planet and with the same centre, so that only its rim shows all round the top and the sides of the planet: a "
          "ring of evenly spaced squared TEETH pointing outward, all the same size (about sixteen teeth round the whole gear, nine or ten "
          "visible above the planet).",
          "SIMPLER CARVING (change): fewer, bigger square notches than in image 2: one row along the rim of each shoulder arc and of each "
          "fist band, no notches on the horns, the legs or the knuckles. One square jade stud on each shoulder arc, each fist band and "
          "the forehead."]
HUONG3 = {
    "X": dict(
        ten="B3 bỏ vành",
        vi="B3 bỏ hẳn vành nghiêng: không còn gì cắt ngang trước hành tinh; bánh răng tròn đủ sau lõi; dáng ba phần tư lệch như rig",
        doi=["NO RING (change): REMOVE the tilted hoop that circles the core in image 2. Nothing crosses in front of the planet and "
             "nothing orbits it: the whole face of the planet is visible except where the head and the fists overlap it."]),
    "Y": dict(
        ten="B3 đá bay quanh",
        vi=("B3 thay vành nghiêng bằng NĂM VIÊN ĐÁ THEN chạm (mảnh vòng gãy, có khía và đinh ngọc) bay quanh lõi theo quỹ đạo nghiêng: ba "
            "viên phía gần to, đi trước lõi; hai viên phía xa nhỏ, ló ra sau mép lõi"),
        doi=["ORBITING STONES (change): REMOVE the tilted hoop that circles the core in image 2. In its place FIVE separate carved "
             "sandstone KEYSTONES orbit the planet on the same tilted elliptical path, with wide empty gaps between them (they do NOT "
             "form a ring): each is a short, thick, slightly wedge-shaped block (a piece of a broken hoop) with a notched rim on its outer "
             "side and one square jade stud. THREE are on the near side, in FRONT of the lower half of the planet, big (about 120 px "
             "wide), at about (450, 545), (660, 600) and (1090, 450); TWO are on the far side, smaller (about 75 px), half hidden BEHIND "
             "the planet, peeking out beside its upper-left and upper-right edge. The stones pass behind the head and the fists."]),
}


def concept3():
    Wp = tho5.Wp
    G = tho5.dat(CODE)
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, "the ORIGINAL rig character from another game (1536x1024, white background): POSE ONLY.", GOC_VI),
         (B3_DUYET, "OUR approved concept of this character (1536x1024, white background): keep its design, materials, colours and "
                    "drawing style; apply the changes listed below.", "Concept B3 lượt 2 (người dùng: khá đẹp): giữ thiết kế, màu, nét")]
    p_hd = os.path.join(HERE, "gui_gpt", f"{CODE}_1", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n")
    if "## Lượt 3: B3 bỏ vành / đá bay quanh (2026-11-18)" in hd:
        hd = hd[:hd.index("## Lượt 3: B3 bỏ vành / đá bay quanh (2026-11-18)") - 1]
    hd += ["", "## Lượt 3: B3 bỏ vành / đá bay quanh (2026-11-18)", "",
           "Người dùng: \"b3 khá đẹp nhưng có thể lược bỏ vành đai đi hoặc đổi sang đá di chuyển xung quanh\".", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} (1536x1024, nền trắng) |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, h in HUONG3.items():
        out = os.path.join(G.TAI, f"L3_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{CODE}_1", f"luot_3_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L3_{k}_2.png, L3_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", TASK3, "", "CHANGES AND DETAILS:"] + [f"- {d}" for d in h["doi"] + CHUNG3] + [
              "- PALETTE (flat, as in image 2): strata bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F / umber #7A4A2E, carved "
              "sandstone #E3D3B0 / #B39F78, jade #2FA37A, tusks #F4EAD2, amber eyes #F6C443.",
              "", "DRAWING STYLE: exactly as image 2: a wobbly dark-brown ink outline (#2B2118, about 7 px) round every piece, thinner "
              "inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching; a second, darker tone only on "
              "side faces. No shading, no highlights, no gradients, no glow, no shadows, no gloss, no sparkles.",
              "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character fills about "
              "x 260-1280, y 115-910. No dust, no debris, no glow, no aura, no smoke, no speed lines, no motion trails, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **{k} {h['ten']}**: {h['vi']}. File prompt `{Wp(p)}`; ảnh lưu `{Wp(out)}`."]
        print(p)
    tho5.ghi(p_hd, hd)


# Lượt 3b (2026-11-18): người dùng "tôi nhầm, b2 không phải b3". Làm lại đúng trên B2 (hành tinh + các mặt trăng): X bỏ hẳn vành; Y thay
# vành bằng năm MẶT TRĂNG NHỎ bay quanh (quả cầu nên nhìn đúng ở mọi chỗ trên quỹ đạo, không vướng phối cảnh như mảnh vòng).
B2_DUYET = os.path.join(_I, f"{CODE}_1", "tai_ve", "L2_B2.png")
TASK3B = ("TASK: REDRAW our approved character concept (image 2) with a few changes. KEEP its design: the banded stone planet as the core, "
          "the pale grey-lilac cratered MOON ROCK of every other piece, the two fists that are two round cratered MOONS with chunky knuckle "
          "stones under them, the thick crescent-shaped shoulder shells, the crown of crescent blades along the top of the core, the horned "
          "beast mask whose two horns make one upward crescent moon, the amber eyes and tusks, the colours and the hand-drawn style. Image "
          "1 is the original rig character from another game: use it ONLY for the POSE (the character is animated with its skeleton); do "
          "not copy its shapes or colours.")
CHUNG3B = [CHUNG3[0],
           "CORE: the huge round banded stone planet exactly as in image 2 (x 496-1030, y 151-640), a perfect circle, with exactly three "
           "shallow round craters.",
           "FIERCER (change): the mask scowls harder, with a heavier angry brow and bigger tusks; the crescent blades of the crown and the "
           "tips of the shoulder crescents are sharper, like sickle blades. Still clean and simple."]
HUONG3B = {
    "B2X": dict(
        ten="B2 bỏ vành",
        vi="B2 bỏ hẳn vành: không còn gì cắt ngang trước hành tinh; dáng ba phần tư lệch như rig; lưỡi trăng và mặt dữ hơn",
        doi=["NO RING (change): REMOVE the flat ring round the core of image 2 and the small rocks riding on it. Nothing crosses in "
             "front of the planet and nothing orbits it: the whole face of the planet is visible except where the head and the fists "
             "overlap it."]),
    "B2Y": dict(
        ten="B2 mặt trăng nhỏ bay quanh",
        vi=("B2 thay vành bằng NĂM MẶT TRĂNG NHỎ (quả cầu đá trăng có hố, to nhỏ khác nhau) bay quanh lõi theo quỹ đạo nghiêng: ba quả "
            "phía gần to, đi trước lõi; hai quả phía xa nhỏ, ló ra sau mép lõi"),
        doi=["ORBITING MOONLETS (change): REMOVE the flat ring round the core of image 2. In its place FIVE separate small round "
             "MOONLETS orbit the planet on the same tilted elliptical path, with wide empty gaps between them (they do NOT form a ring, "
             "and there is NO band or line joining them): each is a small clean SPHERE of the same grey-lilac moon rock with two or three "
             "flat craters. THREE are on the near side, in FRONT of the lower half of the planet, at about (450, 545), (665, 600) and "
             "(1090, 450), of three different sizes (about 120, 90 and 70 px across); TWO are on the far side, smaller (about 60 and "
             "45 px), half hidden BEHIND the planet, peeking out beside its upper-left and upper-right edge. The moonlets pass behind the "
             "head and the fists."]),
}
PAL3B = ("PALETTE (flat, as in image 2): strata bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F / umber #7A4A2E, moon rock "
         "#CFC8D6 / #9D95AB, craters #B3ABC0, tusks #F4EAD2, amber eyes #F6C443.")


def concept3b():
    Wp = tho5.Wp
    G = tho5.dat(CODE)
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, "the ORIGINAL rig character from another game (1536x1024, white background): POSE ONLY.", GOC_VI),
         (B2_DUYET, "OUR approved concept of this character (1536x1024, white background): keep its design, materials, colours and "
                    "drawing style; apply the changes listed below.", "Concept B2 lượt 2 (người dùng: khá đẹp): giữ thiết kế, màu, nét")]
    p_hd = os.path.join(HERE, "gui_gpt", f"{CODE}_1", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n")
    td = "## Lượt 3b: B2 bỏ vành / mặt trăng nhỏ bay quanh (2026-11-18)"
    if td in hd:
        hd = hd[:hd.index(td) - 1]
    hd += ["", td, "", "Người dùng: \"tôi nhầm, b2 không phải b3\" (lượt 3 trên B3 là làm nhầm bản, giữ làm tư liệu).", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} (1536x1024, nền trắng) |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, h in HUONG3B.items():
        out = os.path.join(G.TAI, f"L3_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{CODE}_1", f"luot_3_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L3_{k}_2.png, L3_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", TASK3B, "", "CHANGES AND DETAILS:"] + [f"- {d}" for d in h["doi"] + CHUNG3B] + [f"- {PAL3B}",
              "", "DRAWING STYLE: exactly as image 2: a wobbly dark-brown ink outline (#2B2118, about 7 px) round every piece, thinner "
              "inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching; a second, darker tone only on "
              "side faces. No shading, no highlights, no gradients, no glow, no shadows, no gloss, no sparkles.",
              "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character fills about "
              "x 260-1280, y 115-910. No dust, no debris, no glow, no aura, no smoke, no speed lines, no motion trails, no orbit lines, no "
              "labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **{k} {h['ten']}**: {h['vi']}. File prompt `{Wp(p)}`; ảnh lưu `{Wp(out)}`."]
        print(p)
    tho5.ghi(p_hd, hd)


def so_goc2():
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    G = tho5.dat(CODE)
    g = tho5._mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
    gi = Image.fromarray((g * 255).astype(np.uint8))
    vien = np.asarray(gi.filter(ImageFilter.MaxFilter(5))) ^ np.asarray(gi.filter(ImageFilter.MinFilter(3)))
    font = ImageFont.truetype("arial.ttf", 56)
    o = []
    for k in HUONG2:
        p = os.path.join(G.TAI, f"L2_{k}.png")
        if not os.path.exists(p):
            continue
        m = tho5._mat_na(p)
        iou = (m & g).sum() / max(1, (m | g).sum())
        im = np.asarray(Image.open(p).convert("RGB").resize((tho5.W, tho5.HH))).copy()
        im[vien > 0] = (230, 30, 30)
        im = Image.fromarray(im)
        ImageDraw.Draw(im).text((30, 30), f"{k}  IoU {iou:.3f}", fill=(230, 30, 30), font=font)
        o.append(im.resize((tho5.W // 2, tho5.HH // 2), Image.LANCZOS))
        print(CODE, k, f"IoU {iou:.3f}")
    if o:
        c = Image.new("RGB", (tho5.W // 2 * len(o), tho5.HH // 2), "white")
        for i, im in enumerate(o):
            c.paste(im, (i * tho5.W // 2, 0))
        c.save(os.path.join(G.MAU, "_so_goc_L2.png"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "ca_con":
        tho5.ca_con(CODE)
    elif a[0] == "slot":
        tho5.slot(CODE)
    elif a[0] == "concept":
        concept()
    elif a[0] == "so_goc":
        tho5.so_goc(CODE, "".join(HUONG))
    elif a[0] == "concept2":
        concept2()
    elif a[0] == "so_goc2":
        so_goc2()
    elif a[0] == "concept3":
        concept3()
    elif a[0] == "concept3b":
        concept3b()
