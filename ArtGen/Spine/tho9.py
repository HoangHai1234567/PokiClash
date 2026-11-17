# -*- coding: utf-8 -*-
"""Tướng 9 đảo Thổ (ải 60 "Lò Gốm Đất Nung", id game hiện `cu_phu`): người dùng 2026-11-17 "tôi không nghĩ ra concept nữa rồi, bạn research
và cho tôi concept đi, miễn đẹp, epic và chiến hơn 8 con trước". Claude tự chọn rig trong kho SwordxStaff và đề xuất ba hướng, mỗi hướng một
rig (con gốc khác nhau), chờ người dùng chọn. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai.

    tho9.py ca_con [mã]      hình cả con gốc khung 0 idle → inbox/<mã>_1/mau/goc_ca_con.png (+ .json)
    tho9.py slot <mã>        bảng slot (thứ tự vẽ, ảnh, xương, khung trên ảnh ca_con)
    tho9.py concept          file prompt concept ba hướng → gui_gpt/<mã>_1/luot_1_concept_<k>.txt + gui_gpt/tho9/HUONG_DAN.md
    tho9.py so_goc <mã>      chồng viền hình bóng con gốc lên concept, in IoU → inbox/<mã>_1/mau/_so_goc.png

Mã làm việc: `nhan_su` (A, monster_3623), `nguu_ma` (B, monster_3626), `thach_quy` (C, monster_3456).
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402

_I = os.path.join(HERE, "inbox")
RONG = os.path.join(_I, "rong_cat_1", "tai_ve", "L1_duyet.png")
QUY = os.path.join(_I, "quy_nui_1", "tai_ve", "L1_duyet.png")
REFS = [
    (RONG, "an approved EARTH hero of our game (a sandstone-armoured drake), 1536x1024, white background: match EXACTLY its wobbly dark-brown "
           "pen line, its crayon hatching, its completely flat earth colours and its fierce narrow eye. Do NOT copy its design.",
     "Rồng giáp sa thạch (tướng 4 đảo Thổ) đã duyệt: lấy nét bút mực rung, vân sáp, màu đất phẳng, mắt hẹp dữ"),
    (QUY, "an approved EARTH hero of our game (a four-armed rock ape), 1536x1024, white background: match EXACTLY how big heavy rock and "
          "muscle are drawn in our style (flat front-face tone, darker side-face tone, nothing else) and its flat amber crystal. Do NOT copy "
          "its design.",
     "Vượn núi đá bốn tay (tướng 5 đảo Thổ) đã duyệt: lấy cách vẽ đá nặng, cơ bắp (hai tông mặt trước / mặt bên), hổ phách phẳng"),
]

MOOD = ("MOOD: this is the MINI-BOSS of the earth island, stronger and more epic than every hero before it: fierce, battle-ready, heavy and "
        "powerful, a determined scowl, mature proportions (NOT chibi, NOT a cute mascot, no smile, no big round baby head), but still a clean, "
        "compact, stylised creature for a family game with few details: no gore, no blood, no skulls.")


def _goc(mo_ta):
    return (f"the ORIGINAL rig character from another game ({mo_ta}, 1536x1024, white background). It is painted in a smooth digital cel "
            "style. Use it ONLY for the pose, the body plan and where each big piece sits; do NOT copy its shapes, its face, its head, its "
            "weapons, its details or its colours.")


def _task(sinh_vat, manh):
    return (f"TASK: DESIGN A NEW CHARACTER, LOOSELY BASED ON image 1: {sinh_vat}. Image 1 is ONLY a guide for the POSE and the BODY PLAN (the "
            "new character will be animated with the same skeleton): keep its pose, its facing, its size and place on the canvas, the length "
            f"and thickness of the limbs, and roughly where {manh} are and which way they point. EVERYTHING ELSE IS OUR OWN NEW DESIGN, "
            "described below. The result must NOT look like a recolour or a trace of image 1: someone who knows image 1 must see a DIFFERENT "
            "creature in the same pose. Every limb, the tail and every carried piece stay joined to the body (no white gaps, no broken or "
            "missing limbs; the far legs are visible where image 1 shows them).")


HUONG = {
    # ------------------------------------------------------------------------------------------------------------------------------
    "A": dict(
        code="nhan_su", mon="monster_3623",
        ten="Nhân sư bia kiếm",
        vi=("Nhân sư sa thạch vác ba BIA KIẾM hình tháp (obelisk) mũi hổ phách; khăn trùm đầu kẻ sọc đất nung / kem rủ hai vạt xuống ngực "
            "thay bờm xoăn; râu tết; thân lông ngắn vàng cát, bụng kem; dây da giữ kiếm"),
        goc_vi="Con gốc `monster_3623` (sư tử đá xanh xám bờm mây xoăn, vác hai đại kiếm chéo + một kiếm sau lưng, mũ có âm dương)",
        goc_en=_goc("a blue-grey stone guardian lion with a curly cloud mane, two great swords strapped diagonally across its side and a third "
                    "behind its back"),
        task=_task("a SPHINX-LION GUARDIAN OF THE DESERT TOMBS, a powerful four-legged beast carrying three giant stone OBELISK BLADES",
                   "the head, the chest, the four legs and paws, the tail, the three long blades and the harness"),
        plan=("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 320-1220, y 110-910, a big four-legged "
              "beast standing square and braced, FACING RIGHT. The HEAD is at the upper right (about x 940-1180, y 210-630), seen three-"
              "quarter from the front, both eyes visible, the mouth near x 1000-1100, y 470-630. The deep CHEST is at the centre right "
              "(x 710-1000, y 460-770); the body mass x 560-1040, y 250-820. Near front leg on the right (x 920-1200, y 575-905, big paw at "
              "x 1060-1215, y 790-905); near hind leg at the left (x 495-790, y 365-900); the two far legs show behind them (paws at about "
              "x 440-560 and x 600-770, y 820-905). The TAIL rises from the rump and curls up at the upper left (x 410-710, y 180-630). "
              "THREE long BLADES: blade 1 strapped diagonally across the near side, hilt at the upper left (x 325, y 190) and point at "
              "x 815, y 480; blade 2 parallel below it, hilt at x 320, y 460 and point at x 850, y 895; blade 3 behind the body, mostly "
              "hidden, its hilt sticking up above the back behind the head (top at x 940, y 115). A HARNESS round the neck and chest holds "
              "the blades; a head piece sits on top of the head (x 875-1125, y 240-375)."),
        doi=["CREATURE: a muscular SPHINX-LION made of living SANDSTONE: smooth SHORT-HAIRED hide, sand ochre #D9AE6A, cream chest and "
             "belly #EFDDB4; big paws with dark brown claws #4E3726. NO curly fur, NO cloud swirls, NO mane of locks.",
             "HEAD (new): a broad, fierce lion-sphinx face, short muzzle, mouth slightly open with two strong fangs #F4EAD2, flat nose "
             "#4E3726, two fierce narrow amber eyes (iris #F6C443, black slit pupil, one small white dot) under a heavy scowling brow. "
             "Short round ears.",
             "HEADCLOTH (replaces the mane): a ROYAL STRIPED HEADCLOTH carved in stone, like an ancient desert king's: a smooth hood over "
             "the top of the head that falls in TWO WIDE FLAPS beside the face down onto the chest, flat alternating bands of terracotta "
             "#B0573A and cream #EFDDB4; a plain band across the brow with ONE flat amber rhombus #EFA330 in the middle. No helmet, no "
             "symbol, no yin-yang.",
             "BEARD: a short braided stone beard under the chin, terracotta #B0573A with cream bands.",
             "BLADES (new shape, not swords): three huge OBELISK BLADES: each a long straight FOUR-SIDED stone shaft that tapers to a "
             "PYRAMID POINT, front face sandstone #E2BD7C, side face darker #A87A45, the pyramid point made of flat AMBER crystal #EFA330 "
             "(side face #C77A1E); a short square stone crossguard, a grip wrapped in dark brown leather #5A3A26 and a round stone pommel. "
             "No runes, no inscriptions, no engraving on the blades.",
             "HARNESS: wide dark brown leather straps #6E4630 with flat square sandstone buckle plates, round the neck, across the chest "
             "and over the back, holding the blades.",
             "TAIL: a long lion tail curling up, ending in a stone tassel tuft, terracotta #B0573A.",
             "PALETTE (flat): sand ochre #D9AE6A, cream #EFDDB4, terracotta #B0573A, dark brown #5A3A26, amber #EFA330."]),
    # ------------------------------------------------------------------------------------------------------------------------------
    "B": dict(
        code="nguu_ma", mon="monster_3626",
        ten="Trâu thần xiềng đá",
        vi=("Trâu nước khổng lồ đứng hai chân như quái lực sĩ: đầu trâu, đôi sừng trâu cong rộng, khoen mũi đá gãy; lưng mọc một NÚI BÀN sa "
            "thạch phân tầng có ba cụm hổ phách; bờm lông nâu sẫm; giáp đá trên cẳng tay; vòng đá vỡ ở cổ tay, dây thừng đứt lủng lẳng"),
        goc_vi=("Con gốc `monster_3626` (quái thú lưng gù mai đồng xanh, bờm trắng, mặt nạ, nanh lợn, tay to có tinh thể lam, cùm vuông và "
                "xích sắt)"),
        goc_en=_goc("a hunched blue-grey brute with a green bronze shell, a white mane, a mask, boar tusks, blue crystals on its huge arms, "
                    "square cuffs and iron chains"),
        task=_task("a colossal WATER-BUFFALO TITAN, an ancient earth beast that stands on two legs like a giant brawler and has just broken "
                   "its stone shackles",
                   "the head, the hump, the shoulder fur, the two huge arms and fists, the wrist cuffs, the hanging pieces, the belt and "
                   "the two short legs"),
        plan=("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 290-1260, y 120-910: a huge hunched brute "
              "standing on TWO short thick legs (x 460-940, y 560-910), with TWO ENORMOUS ARMS hanging forward and down, the fists near the "
              "ground: near arm on the LEFT (shoulder x 290-620, y 320-590, forearm x 325-740, y 455-665, fist x 680-870, y 550-750); far "
              "arm on the RIGHT (shoulder x 890-1255, y 310-590, forearm x 960-1235, y 475-725, fist x 830-1025, y 620-805). A massive "
              "HUMP / back rises behind the head (x 420-1020, y 120-420). The HEAD is small and LOW between the shoulders, centre right "
              "(x 760-1080, y 200-630), facing the viewer and a little to the right, BOTH eyes visible (near x 845-990, y 375-440). A "
              "shaggy COLLAR covers the shoulders and the back of the neck (x 620-1050, y 140-600). A wide BELT round the waist (x 545-840, "
              "y 520-700). Long HANGING pieces dangle from the left side of the back (x 370-650, y 240-715) and over the right shoulder "
              "(x 905-1080, y 220-570). A thick CUFF on each wrist (x 570-725, y 505-670 and x 960-1130, y 565-745)."),
        doi=["HEAD (new): a broad WATER-BUFFALO head, wide flat muzzle #7A4A34 with flared nostrils, a BROKEN STONE NOSE RING #8E7A66, heavy "
             "brow, two small fierce amber eyes (iris #F6C443, black pupil, one small white dot), a snorting scowl. TWO MASSIVE HORNS "
             "sweep out sideways from the top of the head and curve back and up (water-buffalo shape), wider than the shoulders, cream "
             "#EDE0C2 with dark brown tips #4E3726 and three flat ring grooves. No mask, no tusks, no flame hair.",
             "HUMP (new, replaces the shell): a small flat-topped MESA of LAYERED SANDSTONE grows out of the hump: cliff sides with "
             "horizontal strata (cream #EAD7AE, ochre #C99A57, rust #A85F3A, side faces darker), and THREE flat AMBER crystal clusters "
             "#EFA330 jutting from its top. No shell, no meander pattern.",
             "FUR: a coarse SHAGGY dark umber fur collar #5B3A28 over the shoulders and neck, short thick rough tufts (NOT white, NOT long "
             "flowing hair).",
             "HIDE: thick dark terracotta-brown skin #8A5238 on the arms and legs, chest and belly lighter #B07A55; huge muscular arms.",
             "FOREARMS: rough flat SANDSTONE ARMOUR PLATES #C99A57 (side faces #9E7442) growing out of the outer forearms, with jagged "
             "straight-edged tops. No crystals on the arms.",
             "SHACKLES: on each wrist a heavy ROUND BOULDER RING, rough grey-brown stone #8E7A66, split by one crack. From the rings and "
             "from the hump hang thick BROKEN BRAIDED ROPES, straw ochre #C9A15A, with frayed ends. NO metal chains, no square cuffs.",
             "BELT: a wide braided rope belt with one flat stone plaque; a short loincloth, earth red #8E3B2A.",
             "LEGS: short and thick, ending in big cloven hooves, dark brown #3F2D22.",
             "PALETTE (flat): terracotta brown #8A5238, umber #5B3A28, cream horns #EDE0C2, sandstone #C99A57, straw rope #C9A15A, amber "
             "#EFA330."]),
    # ------------------------------------------------------------------------------------------------------------------------------
    "C": dict(
        code="thach_quy", mon="monster_3456",
        ten="Thạch quỷ cánh đá",
        vi=("Quỷ đá giữ đền (gargoyle) sống dậy: đầu quỷ sừng cừu, nanh vểnh, tai dơi (bỏ mỏ chim, bỏ mặt nạ); đôi cánh dơi lợp bằng PHIẾN "
            "SA THẠCH như ngói; thân cơ bắp đá kem; búa tạ đầu khối bazan buộc thừng; cọc đá; khố đỏ đất"),
        goc_vi="Con gốc `monster_3456` (người quạ mặt nạ, cánh lông đen, búa nhỏ đỏ và dùi, khố đen)",
        goc_en=_goc("a crow-masked winged man with black feathered wings, a small red mallet in one hand and a spike in the other"),
        task=_task("an ancient STONE GARGOYLE WARRIOR, a carved temple guardian come to life, with stone wings and a heavy maul",
                   "the wings, the torso, the head, the two arms and hands, the maul, the stake, the loincloth and the short legs"),
        plan=("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 340-1190, y 110-910. TWO HUGE WINGS spread "
              "in a wide crescent behind the body, their tips curving up at the top (left wing x 340-805, y 110-755; right wing x 785-1190, "
              "y 135-680). A muscular hunched TORSO in the middle (x 640-1045, y 395-770), leaning forward to the right. The HEAD sits LOW "
              "in front of the chest, centre right (x 735-1060, y 400-695), facing right and the viewer, both eyes visible (x 855-995, "
              "y 520-575). Near arm on the LEFT, elbow out (upper arm x 455-745, y 445-665, forearm x 455-650, y 595-790), the near hand "
              "(x 590-735, y 660-830) gripping the haft of the MAUL (maul x 595-810, y 575-850, its head up and left of the hand). Far arm "
              "on the RIGHT (x 940-1170, y 485-790), the fist (x 950-1070, y 700-850) gripping a short STAKE that points down and right "
              "(x 935-1110, y 695-870). A short loincloth and two short legs below (x 580-950, y 690-910), the feet pointing down."),
        doi=["HEAD (new, NOT a bird: no beak, no mask, no feathers): a horned GARGOYLE beast head: a wide mouth with two upward fangs "
             "#F4EAD2, a broad flat nose, pointed bat ears, a heavy carved scowling brow, two fierce narrow amber eyes (iris #F6C443, black "
             "slit pupil, one small white dot), and two thick horns curling back like a ram's, cream #EDE0C2 with flat ring grooves.",
             "WINGS (new): big BAT-LIKE STONE WINGS: a thick bony arm along the top edge with one hooked claw at the wrist, the wing made of "
             "large flat SANDSTONE SLABS overlapping like roof tiles, each slab flat ochre #C99A57 with a darker side face #9E7442 and "
             "straight chipped edges. No feathers.",
             "BODY: muscular, carved pale sandstone skin #E2CFA4 (side faces #B9A27A), a few simple carved lines for the chest and belly; "
             "no tattoos, no gold, no bracelets.",
             "MAUL (bigger than image 1's mallet): a heavy WAR MAUL: a big rectangular block head of dark basalt brown #5A4030 (side face "
             "#3F2D22) with one flat amber crystal #EFA330 set in its face, bound with straw rope #C9A15A to a thick wooden haft #8A5A3A.",
             "STAKE: a long four-sided stone spike #B9A27A, the grip wrapped with straw rope #C9A15A.",
             "CLOTHING: a short ragged loincloth, earth red #8E3B2A, on a braided rope belt. Short thick legs ending in clawed stone feet "
             "#B9A27A with dark claws #4E3726.",
             "PALETTE (flat): pale sandstone #E2CFA4, ochre #C99A57, basalt brown #5A4030, earth red #8E3B2A, amber #EFA330."]),
}

# ----------------------------------------------------------------------------------------------------------------------------------
# Lượt 2 (2026-11-17): người dùng "nhìn được nhưng chưa đủ ấn tượng so với các con trước, bạn có thể tự nghĩ concept của riêng mình".
# Ba ý tưởng riêng của Claude, mỗi ý một điểm nhấn nhìn thấy ngay trên hình + bảng màu tương phản (8 con trước đều vàng cát / nâu), trên ba
# rig boss có đòn hoành tráng: 3806 (vòng cầu quanh người, xoay quanh sân), 3624 (rồng rắn lặn vọt khỏi khung), 3704 (rồng cánh tấm bắn mũi
# nhọn, bay vút rồi lao xuống).
MOOD2 = ("MOOD: this is the MINI-BOSS of the earth island and must look MORE EPIC AND MORE IMPRESSIVE than every earth hero before it (they "
         "were all plain sand-brown creatures): a majestic, fierce, battle-ready legendary beast with a striking silhouette and bold colour "
         "contrast, mature proportions (NOT chibi, NOT a cute mascot, no smile, no big round baby head), but still a clean stylised creature "
         "for a family game: no gore, no blood, no skulls, no bones.")


def style2():
    return tho5.style().replace("VERY SIMPLE DESIGN, FEW DETAILS:",
                                "CLEAN, BOLD DESIGN with big readable shapes and moderate detail (no clutter):")


HUONG2 = {
    "D": dict(
        code="tinh_hach", mon="monster_3806",
        ten="Thiên thạch thú (Tinh Hạch)",
        vi=("Quái thú sinh ra từ thiên thạch rơi xuống lòng đất: da đá vỏ chai đen có mạch hổ phách như vết nứt của hốc tinh thể; đầu thú giáp đá "
            "có SỪNG MŨI PHA LÊ HỔ PHÁCH, hai sừng ngọc lam vuốt ra sau; mảnh lưỡi liềm thành HỐC TINH THỂ bổ đôi lòng ngọc lam; đuôi dài mũi "
            "giáo ba chạc hổ phách; các quả cầu thành HỐC ĐÁ (geode) nứt hé lộ lòng hổ phách / ngọc lam, bay quanh người"),
        goc_vi="Con gốc `monster_3806` (quái thú gù đen lốm đốm sao, đầu sọ trắng, lưỡi liềm trắng bên sườn, đuôi chạc vàng, vòng vàng, các quả cầu màu)",
        goc_en=_goc("a hunched black beast with starry patches, a white skull head, a big white crescent along its side, a golden forked tail, "
                    "golden rings and coloured spheres"),
        task=_task("an ancient METEOR BEAST born from a meteorite that crashed deep into the earth: a hulking obsidian predator surrounded by "
                   "floating GEODE SPHERES",
                   "the head, the horns, the hump, the big crescent along the side, the two arms and clawed hands, the long tail on the "
                   "ground, the rings and the spheres"),
        plan=("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 345-1200, y 135-910: a hulking beast "
              "crouching low and lunging forward, FACING RIGHT. A massive arched HUMP / back (x 580-1125, y 240-780). The HEAD is low and "
              "forward at the right (x 965-1200, y 300-610), its jaws at x 910-1120, y 440-607, one horn pointing forward on the snout; "
              "TWO LONG HORNS sweep up and back from the top of the head toward the upper left (x 740-1100, y 135-425). A big CRESCENT "
              "piece curves down along the near side from the hump to the ground (x 582-844, y 271-782). Near arm on the LEFT reaching "
              "down to the ground (x 437-710, y 420-820, clawed hand at x 566-710, y 680-820) with a RING round its wrist (x 519-624, "
              "y 581-732); far arm reaching forward to the right (x 721-1100, y 437-770), clawed hand at x 900-1100, y 625-770 resting on "
              "the biggest SPHERE. A long thin TAIL lies along the ground to the left (x 343-664, y 687-808) ending in a three-pronged "
              "tip. SEVEN SPHERES of different sizes lie in an arc at the bottom right (x 646-1183, y 685-911, the biggest x 1033-1183, "
              "y 726-876); a ring floats round the tip of the crescent (x 792-898, y 687-880) and another near the head (x 1076-1195, "
              "y 612-686)."),
        doi=["BODY: a hulking OBSIDIAN beast: glossless black stone hide #2E2833 (side faces #1E1A22), with a few flat jagged AMBER crystal "
             "VEINS #EFA330 running over the hump like the cracks of a geode. NO stars, no galaxy, no stitches, no clouds.",
             "HEAD (new, NOT a skull, no bone mask): a broad, heavy beast head of black stone with a jutting brow, a wide jaw with a row of "
             "strong cream fangs #EDE0C2, the inside of the mouth terracotta red #A2412E, two fierce narrow amber eyes (iris #F6C443, black "
             "slit pupil, one small white dot), and ONE big faceted AMBER CRYSTAL HORN #EFA330 (side faces #C77A1E) on the snout.",
             "HORNS: two long back-swept horns made of stacked TURQUOISE crystal shards #3FB8A8 (side faces #2A8A7E).",
             "CRESCENT (new): a giant curved GEODE CREST along the side: its outer rim rough warm-grey rock #7A6A60, its hollow inner face "
             "packed with flat TURQUOISE crystal facets #3FB8A8 / #2A8A7E, like half of a split geode.",
             "ARMS: thick, muscular black arms with big cream claws #EDE0C2.",
             "TAIL: a long thin black tail ending in a three-pronged AMBER crystal spearhead #EFA330.",
             "SPHERES (new): GEODES: round rough rock shells, warm grey-brown #8E7A66 (side faces #6E5E50), each CRACKED OPEN on one side "
             "showing a flat crystal heart: some amber #EFA330, some turquoise #3FB8A8. No planets, no glossy balls.",
             "RINGS: rough stone rings #8E7A66 with two small amber spikes each (no gold, no metal).",
             "PALETTE (flat): obsidian #2E2833, amber #EFA330, turquoise #3FB8A8, warm grey rock #8E7A66, cream #EDE0C2."]),
    # ------------------------------------------------------------------------------------------------------------------------------
    "E": dict(
        code="son_long", mon="monster_3624",
        ten="Long mạch (rồng núi)",
        vi=("Rồng phương Đông mà thân chính là một DÃY NÚI: vây lưng thành hàng tháp núi đá vôi dựng đứng, trên đỉnh lưng có một NGÔI CHÙA ĐÁ "
            "nhỏ ba tầng mái ngói ngọc lam; thân đỏ hẻm núi bụng kem; đầu rồng gạc đá, râu dài, bờm phiến đá; hai vây lớn thành VÁCH ĐÁ PHÂN "
            "TẦNG"),
        goc_vi="Con gốc `monster_3624` (rồng biển xanh lam vây trong, bờm trắng, mỏ chim, mai sẫm trên lưng)",
        goc_en=_goc("a blue sea-serpent dragon with translucent fins, a white mane, a beak-like snout and a dark patch on its back"),
        task=_task("LONG MACH, the DRAGON VEIN of the earth: an ancient eastern earth dragon whose long body IS a mountain range, rising "
                   "out of the land",
                   "the head, the crest, the neck, the coiled body, the row of tall back fins, the dark patch on the back, the two big "
                   "lower fins and the tail"),
        plan=("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 350-1185, y 110-910: a long serpent dragon "
              "rearing up, FACING RIGHT. The HEAD is at the upper right (x 818-1060, y 112-322), snout pointing right, ONE eye visible "
              "(x 945-985, y 195-215), crest pieces fanning back from the head (x 715-953, y 112-322). The NECK rises from the body "
              "(x 821-1047, y 234-588). The BODY makes a big round LOOP on the left (x 414-935, y 325-730). The TAIL comes up at the right "
              "behind the neck (x 1035-1185, y 310-523) and ends in a flat fluke. A ROW OF TALL BACK FINS stands along the top of the loop "
              "and the back (x 350-805, y 194-578), tallest in the middle. A raised PATCH sits on top of the back (x 512-807, y 325-553). "
              "TWO BIG LOWER FINS hang down like wings: the big near one sweeps down-left to a point at the bottom (x 388-912, y 443-910), "
              "the far one hangs down at the right (x 882-1140, y 502-887)."),
        doi=["BODY: a long eastern dragon of RED CANYON ROCK #B5532F (side faces #8E3E24), with a column of cream sandstone belly plates "
             "#EAD7AE.",
             "BACK FINS (new): a ROW OF TALL, STEEP KARST ROCK PEAKS like a mountain range seen from far away: needle-shaped limestone towers, "
             "pale cream-grey #DCD0B8 front faces and darker #A8987C side faces, jagged tops.",
             "PATCH ON THE BACK (new): a small rocky summit on which stands ONE TINY ANCIENT STONE PAGODA, three tiers, with TURQUOISE roof "
             "tiles #3FB8A8 and cream walls #EDE3CC (small, simple, the signature of the design).",
             "HEAD (new, NOT a bird, no beak): a classic eastern DRAGON head: long snout, jaw slightly open with strong fangs #F4EAD2, two "
             "branching ANTLER HORNS of cream stone #EDE0C2, two long whisker tendrils ochre #C99A57, a mane of layered ochre ROCK FLAKES "
             "#C99A57 (side faces #9E7442) instead of fur, one fierce narrow amber eye (iris #F6C443, black slit pupil, one small white "
             "dot).",
             "BIG LOWER FINS (new): two huge CLIFF SLABS of LAYERED CANYON ROCK, flat horizontal strata bands of cream #EAD7AE, ochre "
             "#C99A57, rust #A85F3A and deep red #8E3E24, jagged chipped lower edges. No constellation lines, no translucency.",
             "TAIL: ends in a flat fluke of layered red rock.",
             "PALETTE (flat): canyon red #B5532F, cream #EAD7AE, limestone #DCD0B8, ochre #C99A57, turquoise roof #3FB8A8, amber eye "
             "#F6C443."]),
    # ------------------------------------------------------------------------------------------------------------------------------
    "F": dict(
        code="phach_long", mon="monster_3704",
        ten="Phách long (rồng cánh hổ phách)",
        vi=("Rồng giáp đá cẩm thạch kem, đôi cánh là hai quạt LƯỠI PHA LÊ HỔ PHÁCH khổng lồ, trong hai lưỡi có bóng một con chuồn chuồn hoá "
            "thạch; mũ ba gai đá có ngọc hổ phách; các mũi nhọn đỏ thành gai pha lê hổ phách; thân dưới bazan nâu sẫm"),
        goc_vi="Con gốc `monster_3704` (rồng giáp vàng cánh tấm phẳng khắc hoa văn, mũ gai có ngọc đỏ, mũi nhọn đỏ ở đuôi và hông, đuôi vòng)",
        goc_en=_goc("a gold-armoured dragon with wings of big flat carved panels, a spiked crown with a red gem, red cone spikes and a ringed "
                    "tail"),
        task=_task("an AMBER DRAGON, the living guardian of the island's amber veins: a stone-armoured dragon whose wings are made of giant "
                   "AMBER CRYSTAL BLADES",
                   "the head and crown, the neck, the chest, the two big fanned wings, the legs and claws, the looped tail and the two "
                   "spiked cones on the lower sides"),
        plan=("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 373-1161, y 112-910: a winged dragon "
              "rearing upright, facing the viewer and a little to the right. The HEAD is in the centre (x 750-960, y 257-560) with a tall "
              "spiked CROWN (x 790-960, y 257-470); the NECK below it (x 797-897, y 403-574); the CHEST (x 774-940, y 520-670). TWO HUGE "
              "WINGS spread up and out in a wide V, each a FAN of about eight long flat BLADES: left wing x 373-800, y 113-693, right wing "
              "x 895-1161, y 177-684. Two clawed legs at the bottom centre (x 726-1043, y 687-910). A ringed TAIL makes a big loop at the "
              "bottom left (x 408-830, y 564-860). Two SPIKED CONES on the lower sides point outwards, one at the lower left (x 451-592, "
              "y 614-859) and one at the right (x 940-1161, y 673-785), each with two small fins."),
        doi=["WINGS (new): each wing a fan of seven or eight HUGE FLAT AMBER CRYSTAL BLADES, long, straight-edged and faceted, front faces "
             "amber #EFA330, side faces #C77A1E; inside ONE blade of each wing a small dark silhouette of a FOSSIL DRAGONFLY #6E4020 (the "
             "amber-fossil signature). No carved swirls, no metal frame.",
             "ARMOUR (new): smooth plates of pale CREAM MARBLE / LIMESTONE #EDE3CC (side faces #C9BBA0) over a dark BASALT-BROWN under-body "
             "#4A3A32. No gold, no metal, no carved patterns.",
             "HEAD (new, NOT a bone skull): a sleek, fierce dragon head of cream stone, short snout, jaw slightly open with sharp fangs, two "
             "fierce narrow amber eyes (iris #F6C443, black slit pupil, one small white dot); a CROWN of three tall stone spikes #EDE3CC "
             "with ONE flat amber gem #EFA330 in the middle.",
             "SPIKES: every red cone of image 1 becomes a faceted AMBER crystal spike #EFA330 set in a cream stone socket.",
             "JOINT BEADS: the round red gems at the joints become flat amber beads #EFA330.",
             "TAIL: segmented cream stone rings over the dark basalt tail.",
             "CLAWS: dark basalt #3F2D22.",
             "PALETTE (flat): cream marble #EDE3CC, basalt brown #4A3A32, amber #EFA330 / #C77A1E, dark brown #3F2D22."]),
}

for _k, _h in list(HUONG.items()) + list(HUONG2.items()):
    tho5.CON[_h["code"]] = (_h["mon"], 9, 60)

# ----------------------------------------------------------------------------------------------------------------------------------
# Lượt 3 (2026-11-17): người dùng "tôi thích D nhất nhưng nhìn quá giống con gốc". D giữ 1:1 mọi mảnh nhận diện của monster_3806 (hai sừng
# dài vuốt sau, sừng mũi, lưỡi liềm bên sườn, cung quả cầu tròn, vòng, đuôi chạc). Giữ cái người dùng thích (thân đá đen mạch hổ phách, tinh
# thể ngọc lam + hổ phách, mặt dữ, chủ đề thiên thạch / hốc đá), ĐỔI HẲN DÁNG các mảnh đó; ba biến thể bóng dáng khác nhau. Rig: sừng / đầu
# (jiao_*, tou) cứng trên xương đầu all6, đuôi weiba, từng quả cầu qiu_*, từng vòng jinhuan_* là mảnh một xương; lưỡi liềm shenti_04 là lưới
# trên xương thân: đổi dáng đều không ảnh hưởng clip; vòng, mây (yun), sao (xing) bỏ thì ẩn slot.
D_DUYET = os.path.join(_I, "tinh_hach_1", "tai_ve", "L1_D.png")
REF_D = (D_DUYET, "OUR previous concept of this character, which the art director LIKES for its colours, materials and fierce face but "
                  "REJECTED because its shapes still copy image 1. Keep from image 2 ONLY: the black obsidian hide with flat amber vein "
                  "cracks, the turquoise and amber crystal materials, the fierce head with the wide fanged jaw and narrow amber eyes, the "
                  "drawing style. Do NOT keep its two long back-swept horns, its horn on the nose, the crescent along its side, the arc of "
                  "round balls, the rings or the three-pronged tail tip.",
         "Concept D lượt 2 (người dùng thích màu, chất liệu, mặt; chê giống con gốc): chỉ lấy da đen mạch hổ phách, tinh thể, mặt dữ")

PLAN3 = ("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills about x 345-1200, y 135-910: a hulking beast "
         "crouching low and lunging forward, FACING RIGHT. A massive arched back (x 580-1125, y 240-780). The HEAD is low and forward at "
         "the right (x 965-1200, y 300-610), its jaws at x 910-1120, y 440-607. The space above and behind the head (x 740-1100, "
         "y 135-425) holds the new head crest described below (or stays empty). The near FLANK runs from the back down to the ground "
         "(x 582-844, y 271-782). Near arm on the LEFT reaching down to the ground (x 437-710, y 420-820, clawed hand at x 566-710, "
         "y 680-820); far arm reaching forward to the right (x 721-1100, y 437-770), clawed hand at x 900-1100, y 625-770. A long TAIL lies "
         "along the ground to the left (x 343-664, y 687-808). A loose group of FLOATING STONES hovers low at the bottom right (x 646-1183, "
         "y 685-911), the biggest one under the far hand (about x 1033-1183, y 726-876).")

COMMON3 = ["KEEP from image 2: black obsidian hide #2E2833 (side faces #1E1A22) with a few flat jagged AMBER vein cracks #EFA330; the fierce "
           "head: heavy brow, wide jaw with strong cream fangs #EDE0C2, inside of the mouth terracotta red #A2412E, two fierce narrow "
           "amber eyes (iris #F6C443, black slit pupil, one small white dot); thick muscular arms with big cream claws.",
           "REMOVE (these copy image 1): NO two long thin horns sweeping back, NO horn on the nose, NO crescent or sickle shape along the "
           "side, NO rings, NO neat row or arc of round balls, NO forked or three-pronged tail tip, no stars, no clouds, no skull."]

HUONG3 = {
    "D1": dict(
        ten="Gù thiên thạch",
        vi=("lưng mọc một TẢNG THIÊN THẠCH khổng lồ nứt toạc lộ mạch ngọc lam; vương miện ba tinh thể hổ phách ngắn trên trán, hai nanh vểnh "
            "hàm dưới; sườn ba tấm giáp đá chồng; đuôi CHÙY ĐÁ thiên thạch cắm gai hổ phách; đá bay là mảnh thiên thạch góc cạnh"),
        doi=["HEAD CREST (new): a short CROWN of three thick AMBER crystals #EFA330 (side faces #C77A1E) on the brow, pointing up and back; "
             "two cream TUSKS jutting up from the lower jaw. Nothing else on the head.",
             "BACK (new, the signature): a HUGE rough METEORITE BOULDER fused into the hump, dark rust-brown crust #5E4034 (side faces "
             "#432C24), split open along its top by a jagged seam packed with flat TURQUOISE crystals #3FB8A8 (side faces #2A8A7E). It "
             "makes the back a big round rocky dome, not a smooth arch.",
             "FLANK (new): three heavy overlapping obsidian ARMOUR PLATES down the side, each edged with one thin amber vein.",
             "TAIL (new): a thick tail ending in a heavy MACE of rough meteorite rock #5E4034, studded with three short amber crystal "
             "spikes, like an armoured club.",
             "FLOATING STONES (new): five ANGULAR, jagged METEORITE SHARDS of different sizes (not balls), dark rust-brown #5E4034, each "
             "with one flat crystal face (turquoise or amber), hovering in a loose cluster."]),
    "D2": dict(
        ten="Lưng rừng tinh thể",
        vi=("từ lưng và vai mọc một RỪNG TRỤ TINH THỂ ngọc lam + hổ phách cao thấp (hốc đá lộn trong ra ngoài); diềm đá sau đầu viền tinh "
            "thể hổ phách nhỏ; đuôi xoè ba lưỡi tinh thể ngọc lam; đá bay là cụm tinh thể lơ lửng"),
        doi=["HEAD CREST (new): a short flared ROCK FRILL behind the head (like a horned-dinosaur frill but without horns), obsidian with a "
             "row of small amber crystal points #EFA330 along its rim. No horns at all.",
             "BACK (new, the signature): a big CLUSTER of tall CRYSTAL PILLARS of different heights erupting from the hump and the "
             "shoulders, like a geode turned inside out: most turquoise #3FB8A8 (side faces #2A8A7E), a few amber #EFA330 (side faces "
             "#C77A1E), pointing up and back. It is the tallest part of the silhouette.",
             "FLANK: plain obsidian hide with two flat amber vein cracks (no extra piece).",
             "TAIL (new): a long tail ending in a FAN of three flat turquoise crystal blades spreading apart.",
             "FLOATING STONES (new): four floating CLUSTERS of three or four small crystals each (turquoise and amber) set in a chunk of "
             "dark rock, hovering in a loose group (not balls)."]),
    "D3": dict(
        ten="Bờm thiên thạch",
        vi=("đầu sư tử rồng có BỜM ĐÁ THIÊN THẠCH lởm chởm quanh đầu và vai; lưng có ba MIỆNG HỐ VA CHẠM chứa tinh thể hổ phách; đuôi một "
            "lưỡi tinh thể ngọc lam lớn; đá bay là tảng đá có lõi ngọc lam"),
        doi=["HEAD CREST (new, the signature): a huge shaggy MANE of jagged dark METEORITE ROCKS round the head, the neck and the shoulders, "
             "like a lion's mane made of broken rock: dark rust-brown #5E4034 (side faces #432C24), the rock tips pointing back and out; a "
             "few small turquoise crystals #3FB8A8 between the rocks. No horns.",
             "BACK (new): the arched obsidian back carries three round IMPACT CRATERS, each a shallow rocky ring filled with flat amber "
             "crystals #EFA330.",
             "FLANK: plain obsidian hide with two flat amber vein cracks.",
             "TAIL (new): a long tail ending in ONE big flat TURQUOISE crystal blade, like a spear blade.",
             "FLOATING STONES (new): five rough lumpy rocks of different sizes (not perfect balls), dark rust-brown #5E4034, each cracked "
             "to show a turquoise crystal core, hovering in a loose group."]),
}


def concept3():
    Wp = tho5.Wp
    h0 = HUONG2["D"]
    G = tho5.dat("tinh_hach")
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, h0["goc_en"], h0["goc_vi"]), REF_D, REFS[0]]
    p_hd = os.path.join(HERE, "gui_gpt", "tho9", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n")
    hd += ["", "## Lượt 3: ba biến thể của D, đổi dáng mảnh nhận diện (2026-11-17)", "",
           "Người dùng: \"tôi thích D nhất nhưng nhìn quá giống con gốc\".", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    task = ("TASK: REDESIGN the METEOR BEAST of image 2 so that its SILHOUETTE NO LONGER RESEMBLES image 1. Image 1 is ONLY a guide for "
            "the POSE and the BODY PLAN (the character will be animated with the same skeleton): keep its pose, facing, size and place on "
            "the canvas and the length and thickness of the body, arms and tail. Every big shape that made image 2 look like image 1 is "
            "REPLACED by the new shapes below. Someone who knows image 1 must see a clearly DIFFERENT creature. Every limb, the tail and "
            "every piece stay joined to the body (no white gaps).")
    for k, h in HUONG3.items():
        out = os.path.join(G.TAI, f"L2_{k}.png")
        p = os.path.join(HERE, "gui_gpt", "tinh_hach_1", f"luot_2_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t = [x.replace("(images 2 and 3)", "(images 2 and 3)") for x in t]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L2_{k}_2.png, L2_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", task, "", PLAN3, "", "DESIGN:"] + [f"- {d}" for d in COMMON3 + h["doi"]] + [
              "- PALETTE (flat): obsidian #2E2833, amber #EFA330, turquoise #3FB8A8, rust-brown meteorite rock #5E4034, cream #EDE0C2.",
              "", style2(), "", MOOD2, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no flying debris, no glow, no aura round the character, no "
              "smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **{k} {h['ten']}**: {h['vi']}. File prompt `{Wp(p)}`; ảnh lưu `{Wp(out)}`."]
        print(p)
    tho5.ghi(p_hd, hd)


def concept2():
    Wp = tho5.Wp
    p_hd = os.path.join(HERE, "gui_gpt", "tho9", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n") if os.path.exists(p_hd) else []
    hd += ["", "## Lượt 2: ba concept riêng của Claude (2026-11-17)", "",
           "Người dùng: \"nhìn được nhưng chưa đủ ấn tượng so với các con trước, bạn có thể tự nghĩ concept của riêng mình\".", ""]
    for k, h in HUONG2.items():
        G = tho5.dat(h["code"])
        mau = os.path.join(G.MAU, "goc_ca_con.png")
        R = [(mau, h["goc_en"], h["goc_vi"])] + REFS
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{h['code']}_1", f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", h["task"], "", h["plan"], "", "DESIGN:"] + [f"- {d}" for d in h["doi"]] + ["", style2(), "", MOOD2, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no flying debris, no glow, no aura round the character, no "
              "smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"### Hướng {k}: {h['ten']} (`{h['code']}`, rig `{h['mon']}`)", "", h["vi"] + ".", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        hd += ["", f"File prompt: `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", ""]
        print(p)
    tho5.ghi(p_hd, hd)


def concept():
    Wp = tho5.Wp
    hd = ["# Gói GPT: tướng 9 đảo Thổ (ải 60), ba hướng concept", "",
          "Người dùng (2026-11-17): \"tôi không nghĩ ra concept nữa rồi, bạn research và cho tôi concept đi, miễn đẹp, epic và chiến hơn 8 "
          "con trước\". Mỗi hướng một rig khác nhau trong kho game tham khảo (Claude chọn). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong "
          "máy, không đăng công khai. Gen qua Magnific (GPT 2.6, 1k high, 95 credit / ảnh).", ""]
    for k, h in HUONG.items():
        G = tho5.dat(h["code"])
        mau = os.path.join(G.MAU, "goc_ca_con.png")
        R = [(mau, h["goc_en"], h["goc_vi"])] + REFS
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{h['code']}_1", f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", h["task"], "", h["plan"], "", "DESIGN:"] + [f"- {d}" for d in h["doi"]] + ["", tho5.style(), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no flying debris, no glow, no aura round the character, no "
              "smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"## Hướng {k}: {h['ten']} (`{h['code']}`, rig `{h['mon']}`)", "", h["vi"] + ".", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        hd += ["", f"File prompt: `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", ""]
        print(p)
    hd += ["Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: cùng dáng, cùng hướng, cùng chỗ các mảnh to như ảnh 1 nhưng nhìn ra con KHÁC; mọi chi dính thân; mắt có chấm trắng; nét bút "
           "mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"it still looks like image 1: change the head and the big pieces more\"; \"remove the shading / highlights / "
           "glow, flat colour only\"; \"every limb joined to the body, no white gap\"."]
    tho5.ghi(os.path.join(HERE, "gui_gpt", "tho9", "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "ca_con":
        for c in (a[1:] or [h["code"] for h in HUONG.values()]):
            tho5.ca_con(c)
    elif a[0] == "slot":
        tho5.slot(a[1])
    elif a[0] == "concept":
        concept()
    elif a[0] == "concept2":
        concept2()
    elif a[0] == "concept3":
        concept3()
    elif a[0] == "so_goc":
        for k, h in list(HUONG.items()) + list(HUONG2.items()):
            if a[1:] in ([], [h["code"]]):
                tho5.so_goc(h["code"], k)
