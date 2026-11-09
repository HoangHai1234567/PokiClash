# -*- coding: utf-8 -*-
"""Gói prompt Codex cho 10 dòng tướng đảo Hỏa vẽ lại thành tướng .atomik (2026-11-09).

Theo cách hai đảo Thủy, Mộc (QUY_TRINH mục 16, 18; skill pokiclash-spine-rig mục 13, 15): thú huyền thoại hơi chibi kiểu
Pokémon, style cũ (bút mực + chì sáp, tô phẳng), dạng sau dữ hơn nhưng không quá, hạn chế dạng người, càng gần boss cuối càng
đẹp. Gen trọn con LIỀN một ảnh (không tờ mảnh, không lớp dưới), rig thẳng từ ảnh bằng beast.py (một lưới).

Đảo Hỏa chưa có concept nào đã duyệt, nên Claude tự thiết kế như đảo Thủy: giữ chủ đề, loài của dòng aola người dùng chọn
(GD_Claude/13, mục Hỏa), đổi màu, chi tiết thành con riêng. Mỗi dòng một bảng màu để cả đảo không chỉ một màu đỏ. Ảnh mẫu nét,
dáng là các ảnh liền của Thủy, Mộc đã vào game (đúng khung 1536x1024, đúng dáng rig được).

Mỗi dạng: gui_gpt/<id>_<k>/luot_1_lien.txt -> inbox/<id>_<k>/tai_ve/L1_lien.png. Dạng k > 1 đính ảnh các dạng trước
(L1_duyet.png nếu có, không thì L1_lien.png); dạng chưa có ảnh dạng trước thì chưa dựng.

    py -3 -I ArtGen/Spine/build_hoa.py [id ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, line  # noqa: E402

INBOX = W(HERE, "inbox")

# ảnh liền đã vào game dùng làm mẫu nét, khung, dáng: mã -> (mô tả tiếng Anh, mô tả tiếng Việt cho HUONG_DAN)
REFS = {
    "de_hoa_1": ("a chubby flower-sheep on four legs", "cừu hoa lông kem bốn chân (đảo Mộc)"),
    "moc_tinh_2": ("a crystal wolf on four legs", "sói xám pha lê lục bảo bốn chân (đảo Mộc)"),
    "long_vuot_2": ("a winged dragon standing on its two hind legs", "rồng lá đứng hai chân, cánh xoè (đảo Mộc)"),
    "canh_cut_1": ("a round chibi penguin with short limbs", "cánh cụt tròn chân tay ngắn cầm chảo (đảo Thủy)"),
    "gio_loc_2": ("a winged dragon floating in the air", "rồng chuồn chuồn bay lơ lửng (đảo Mộc)"),
    "thuong_lam_2": ("a winged ice dragon on four legs", "rồng băng bốn chân, cánh xoè (đảo Thủy)"),
}

# kiểu dáng -> ảnh mẫu dáng (ảnh đầu), ảnh mẫu nét thứ hai. Không dùng Lam Quân (Bồ Lao sừng vàng, bờm xoăn) làm mẫu: gần
# kỳ lân, sư tử của đảo này quá, Codex dễ chép thiết kế.
POSE_REF = {"quad": ("de_hoa_1", "moc_tinh_2"), "fox": ("moc_tinh_2", "de_hoa_1"),
            "humanoid": ("long_vuot_2", "de_hoa_1"), "raptor": ("long_vuot_2", "de_hoa_1"),
            "blob": ("canh_cut_1", "de_hoa_1"), "genie": ("gio_loc_2", "de_hoa_1"),
            "winged": ("thuong_lam_2", "de_hoa_1")}

POSES = {
    "quad": ("- Stands on its FOUR legs, all paws flat on one level ground line (no ground drawn), a grounded ready-to-fight "
             "stance: the front a little lower, head forward.\n- All four legs are visible: the two near legs in front, the "
             "two far legs peeking out behind them; white gaps between the front pair and the back pair, and between each "
             "near leg and the far leg next to it where possible.\n- The tail sweeps up and back behind the body on the "
             "viewer's LEFT, clear of the legs with white space between, never crossing the body."),
    "humanoid": ("- Stands upright on its two hind legs, both feet flat on one level ground line (no ground drawn), feet a "
                 "little apart with a white gap between the legs, a grounded ready-to-fight stance.\n- Both arms are held a "
                 "little away from the body with white space between each arm and the body; the fists are clenched at about "
                 "hip height, NOT raised in front of the chest or the face.\n- The tail (if any) sweeps back and down on the "
                 "viewer's LEFT, clear of the legs."),
    "raptor": ("- Stands upright on its two hind legs like a small upright dragon, both feet flat on one level ground line (no "
               "ground drawn), a white gap between the legs, the body leaning slightly forward, ready to fight.\n- Its arms are "
               "held a little in front of the chest, away from the body with white space around them.\n- The wings rise up "
               "and back behind the shoulders, clear of the head and horns.\n- The tail sweeps back on the viewer's LEFT "
               "behind the legs, clear of them, its tip near the ground."),
    "blob": ("- Stands on its short legs (or its round bottom), feet flat on one level ground line (no ground drawn), a grounded "
             "ready-to-fight stance.\n- Its small arms are held a little away from the round body with white space between "
             "each arm and the body."),
    "genie": ("- It FLOATS in the air (no ground drawn) and has NO legs: its lower body narrows into a curling tail of lava "
              "and flame whose tip curls toward the viewer's LEFT, about 90 px above the ground line.\n- Both arms are held a "
              "little away from the body with white space between each arm and the body; the rock fists are at about waist "
              "height, not in front of the face."),
    "winged": ("- Stands on its FOUR legs, all hooves flat on one level ground line (no ground drawn), a proud ready-to-fight "
               "stance, head and neck raised forward.\n- All four legs are visible with white gaps between the front pair "
               "and the back pair.\n- The two wings rise up and back above the shoulders, clear of the head, the antlers and "
               "the mane; the tail sweeps back on the viewer's LEFT, clear of the legs."),
}
POSES["fox"] = POSES["quad"]

CHIBI = {1: ("FORM 1, the young stage: clearly chibi like a monster-collecting game starter: a big head (about 45% of the "
             "creature's height), a compact round body, short sturdy limbs, big expressive eyes. Cute but already brave."),
         2: ("FORM 2, the same creature grown up: still a bit chibi (head about 38% of its height) but bigger, leaner and "
             "more confident, a little fiercer (sharper eyes, small fangs or spikes), clearly the same species, colours and "
             "markings as form 1."),
         3: ("FORM 3, the final stage: powerful and majestic, only slightly chibi (head about 32% of its height), the most "
             "detailed and beautiful design of the line, fierce and proud but still appealing, NOT scary or monstrous; "
             "clearly the same species, colours and markings as forms 1 and 2.")}
FINAL2 = ("FORM 2, the FINAL stage of this two-stage line: powerful and majestic, only slightly chibi (head about 35% of its "
          "height), the most detailed and beautiful design of the line, fierce and proud but still appealing, NOT scary or "
          "monstrous; clearly the same species, colours and markings as form 1.")

SPIRIT = ("a MYTHICAL FIRE BEAST of the fire element, a creature (not a human, no human face or human body, no clothes except "
          "the items listed), designed like a creature of a monster-collecting game: appealing, simple readable shapes, few "
          "details. Its face is DETERMINED and ready to fight: lowered brows, confident focused eyes looking to the viewer's "
          "right, mouth set firm or slightly open; never a happy mascot grin, never scary.")

FLAMES = ("FLAMES AND LAVA: every flame (mane, crest, tufts, tail tip, wings) is a solid part of the creature: a flat shape "
          "with a closed dark-brown ink outline, filled with flat crayon colours in at most three clear bands (outer, middle, "
          "inner), never left as white paper. Flames are attached to the body: no loose floating flames, sparks, embers, smoke "
          "or heat haze around the creature. Lava, embers and cracks are flat orange or yellow colour areas. Nothing glows: no "
          "light coming from the flames, no bright halo, the flames do not light up the body.")

# id -> ải, mỗi dạng: tên (theo heroes.json), kiểu dáng, thiết kế tiếng Việt, mô tả tiếng Anh
LINES = {
    "su_tu_lua": {"order": 1, "forms": {
        1: {"name": "Sư Tử Lửa", "kind": "quad",
            "vn": "sư tử lửa con: lông cam, mõm ngực kem, bờm túm lửa ba màu, chóp đuôi lửa, băng vải nâu quấn hai chân trước "
                  "như võ sĩ nhí",
            "who": ("a chibi FIRE LION cub: warm orange fur (#F08A3C) with a cream muzzle, chest and paw tips (#F6E3C2); a "
                    "short round mane of chunky flame tufts framing the face (outer red #D9483B, middle orange #F5A03A, inner "
                    "yellow #F7D14A); amber eyes (#F0B030); small rounded ears, one with a little notch; the thin tail ends "
                    "in a small flame tuft of the same three colours; dark-brown cloth wraps (#6B4A3A) around both front "
                    "paws like a young boxer.")},
        2: {"name": "Sư Tử Lửa", "kind": "quad",
            "vn": "sư tử trẻ: bờm lửa vuốt ngược tới vai, túm lửa ở khuỷu, băng vải dài hơn có dải đỏ, răng nanh",
            "who": ("the same fire lion grown into a lean, athletic young lion: deeper orange fur (#E8752E), cream muzzle and "
                    "chest; a bigger mane of swept-back flame locks (red, orange, yellow bands) reaching the shoulders; "
                    "small flame tufts at the elbows; longer dark-brown cloth wraps on both front legs, each tied with a "
                    "short red cloth end (#C8352E); small fangs; a pounce-ready stance.")},
        3: {"name": "Sư Tử Lửa", "kind": "humanoid",
            "vn": "sư tử võ sĩ đứng hai chân: cơ bắp, bờm lửa lớn trùm vai, tay quấn vải nâu có miếng đồng ở đốt tay, đai đỏ "
                  "thắt hông, đuôi chóp lửa lớn",
            "who": ("the same fire lion as a mighty lion brawler that now stands up on its hind legs: muscular, burnt-orange "
                    "fur (#D9662A) with a cream chest and muzzle; a huge mane of big flame locks (red #C8352E, orange, yellow "
                    "core) around the head and over the shoulders; flame tufts on the forearms; both fore-paws wrapped in "
                    "dark-brown cloth with brass knuckle plates (#C8873A); a red sash belt (#B5302A) knotted at the hip; a "
                    "long tail ending in a big flame tuft; small fangs, a proud fierce gaze.")}}},
    "khong_lo": {"order": 5, "forms": {
        1: {"name": "Viên Than", "kind": "blob",
            "vn": "viên than sống: thân tròn than xám, vết nứt màu cam than hồng, chồi lửa trên đầu, tay chân tròn ngắn",
            "who": ("a chibi CHARCOAL SPRITE, a round living lump of coal: a round body of charcoal grey (#4A4248) with a few "
                    "ember-orange crack lines (#F08A3C) drawn on it; a lively flame sprout on top of its head (red, orange, "
                    "yellow bands); big eyes with ember-orange irises and determined brows; two stubby round arms and two "
                    "short round feet of the same charcoal.")},
        2: {"name": "Sừng Than", "kind": "humanoid",
            "vn": "than con lực sĩ đứng hai chân: sừng xương ngà cong ngắn, mào lửa giữa hai sừng, nắm đấm to, dấu lõi than "
                  "hồng trên ngực",
            "who": ("the same charcoal creature grown into a stocky young brute standing on two short legs: a chunky charcoal "
                    "body (#3E373D) with more ember-orange cracks; two short curved horns of pale bone (#E9DCC0); a flame "
                    "crest between the horns; thick arms ending in big round fists; an ember-orange core mark on the chest; a "
                    "short tail with an ember-orange tip.")},
        3: {"name": "Khổng Lồ Lửa", "kind": "humanoid",
            "vn": "khổng lồ than: vai và nắm đấm đá than nứt to, sừng xương lớn, bờm lửa từ đỉnh đầu xuống gáy, lõi cam trong "
                  "khung sắt ở ngực, còng sắt gãy ở cổ tay",
            "who": ("the same creature as a towering coal giant: massive shoulders and huge fists of cracked charcoal rock "
                    "(#352F34) with ember-orange seams; big curved bone horns; a flame mane running from the top of the head "
                    "down the back of the neck; a molten-orange core in the chest framed by a riveted iron plate (#6E6A70); "
                    "broken iron cuffs on both wrists; short sturdy legs; long arms whose fists hang low beside the legs, "
                    "not touching them.")}}},
    "kim_su": {"order": 10, "forms": {
        1: {"name": "Sư Con", "kind": "quad",
            "vn": "sư tử thần giữ đền con: lông vàng cát, bờm lửa xoắn đỏ thẫm chóp vàng như sư tử đá, mắt ngọc lam, mề đay "
                  "vàng dây đỏ",
            "who": ("a chibi GOLDEN GUARDIAN LION cub: sandy-gold fur (#E8C27A) with a cream muzzle and belly (#F6E9CC); a "
                    "round mane of curling flame swirls in crimson (#C2303A) with gold tips (#F2C14E), like the curls of a "
                    "temple lion statue; turquoise eyes (#2FB3A8); a round golden medallion (#E0A93A) on a short crimson "
                    "cord at the neck; the tail ends in a crimson flame curl.")},
        2: {"name": "Liệt Hỏa Sư", "kind": "quad",
            "vn": "sư tử trẻ: bờm xoắn lửa lớn trùm vai, giáp trán vàng ngọc lam, vòng vàng ở chân trước, răng nanh",
            "who": ("the same golden lion grown young and strong: a bigger mane of crimson flame swirls with gold tips "
                    "sweeping back over the shoulders; a small golden forehead plate with a turquoise gem; golden bands on "
                    "the front legs; crimson flame curls at the elbows and the tail tip; small fangs.")},
        3: {"name": "Kim Sư", "kind": "quad",
            "vn": "kim sư giáp vàng: mũ giáp vàng ngọc lam, giáp vai và giáp chân khắc xoắn lửa, bờm xoắn đỏ vàng lớn",
            "who": ("the same lion as a regal guardian lion in golden armour: a golden helmet-crest with a turquoise gem; "
                    "golden shoulder plates and leg guards engraved with flame-swirl patterns; a magnificent mane of large "
                    "crimson flame swirls tipped with gold; a long tail ending in a big flame curl; proud and fierce.")}}},
    "nham_than": {"order": 15, "forms": {
        1: {"name": "Nham Con", "kind": "genie",
            "vn": "tinh linh dung nham con bay lơ lửng: thân dung nham cam, bụng vàng, nửa dưới là đuôi lửa xoắn ngắn, mũ mặt "
                  "nạ đá bazan hai sừng nhỏ, găng đá",
            "who": ("a chibi LAVA SPIRIT that floats: a body of molten lava in flat orange (#F08A3C) with a yellow belly patch "
                    "(#F7D14A); its lower body narrows into a short curling flame tail instead of legs; it wears a "
                    "helmet-mask of dark basalt rock (#5A4A44, darker cracks #3A2E2A) with two short rock horns, the face "
                    "showing through with big yellow eyes and determined brows; two small arms ending in chunky basalt "
                    "rock mitts; a flame crest rising from the top of the helmet.")},
        2: {"name": "Nham Hỏa", "kind": "genie",
            "vn": "dung nham lớn: giáp vai, giáp ngực đá bazan, găng đá to, mào lửa ba ngọn, đuôi dung nham dài hơn",
            "who": ("the same lava spirit grown bigger and tougher: broad basalt shoulder plates and a basalt chest guard over "
                    "its molten body; larger rock gauntlets; a taller flame crest with three points; the rock helmet with "
                    "longer horns; a longer curling lava tail below the waist.")},
        3: {"name": "Nham Thần", "kind": "genie",
            "vn": "chúa dung nham: giáp đá bazan to có mạch dung nham, vương miện gai đá, bờm lửa, nắm đá khổng lồ, đuôi dung "
                  "nham dài",
            "who": ("the same creature as the lava lord: massive basalt armour with molten-orange seams; a crown of rock "
                    "spikes; a blazing flame mane flowing back from the crown; huge rock fists; a long thick curling tail of "
                    "magma below the waist; a fierce commanding gaze.")}}},
    "nguu_quyen": {"order": 20, "forms": {
        1: {"name": "Nghé Lửa", "kind": "quad",
            "vn": "nghé lửa: da đỏ gạch, mõm bụng kem, sừng ngà ngắn, khoen mũi đồng, túm lửa trên trán và chóp đuôi",
            "who": ("a chibi FIRE BULL calf: brick-red hide (#B5462E) with a cream muzzle and belly (#F1D9B5); two short ivory "
                    "horns (#EFE3C8); a brass nose ring (#C8873A); a flame tuft on the forehead and a flame tuft at the tip "
                    "of its thin tail (red, orange, yellow bands); dark-brown hooves (#4A3228); big eyes with determined "
                    "brows; snorting, ready to charge.")},
        2: {"name": "Ngưu Lãng Tử", "kind": "humanoid",
            "vn": "ngưu lãng tử đứng hai chân: khăn cổ xanh mòng két, thắt lưng da khoá đồng tròn, tay quấn vải kem như nắm "
                  "đấm, sừng dài hơn",
            "who": ("the same fire bull grown into a young wandering brawler that stands on its hind legs: brick-red hide, "
                    "cream muzzle and chest, longer curved ivory horns, the brass nose ring; a teal-blue neckerchief "
                    "(#2F8C8C) tied at the neck; a brown leather belt with a big round brass buckle; both fore-hooves "
                    "wrapped in cream cloth like fists; a flame tuft between the horns and a flame tail tip.")},
        3: {"name": "Ngưu Quyền", "kind": "humanoid",
            "vn": "ngưu quyền thủ: cơ bắp, sừng lớn vòng đồng, bờm lửa dáng mây lửa trùm vai, găng đấm đỏ cổ đồng, đai vô "
                  "địch xanh mòng két vân mây lửa",
            "who": ("the same fire bull as a mighty bull boxer: broad and muscular, deep brick-red hide (#9E3A26); big curved "
                    "ivory horns with brass rings; a mane of flame shaped like rolling fire clouds over the neck and "
                    "shoulders; big red boxing gloves (#C8352E) with brass cuffs; a teal-blue champion sash with a "
                    "fire-cloud pattern tied at the waist; the brass nose ring; a long tail with a flame tip; proud and "
                    "fierce.")}}},
    "hong_lien": {"order": 30, "forms": {
        1: {"name": "Đốm Hồng", "kind": "raptor",
            "vn": "rồng con sen lửa đứng hai chân: vảy đỏ hồng, bụng kem, đốm vàng trên đầu và lưng, cánh nhỏ hình cánh sen, "
                  "chóp đuôi lửa hình nụ sen",
            "who": ("a chibi LOTUS FIRE DRAGONLING standing on its hind legs: rose-red scales (#E0504A) with a cream belly "
                    "(#F6E3D0) and yellow spots (#F7C844) on its head and back; two tiny cream horn nubs; big golden eyes; "
                    "small arms with little claws; a pair of small wings shaped like red lotus petals (pink #F07C8C with a "
                    "darker rose rim #C2405A and a yellow base); the tail ends in a flame shaped like a lotus bud.")},
        2: {"name": "Phi Viêm", "kind": "raptor",
            "vn": "rồng sen trẻ: thon cao, vằn đỏ thẫm trên lưng, sừng vuốt ngược, cánh lửa nhiều cánh sen nửa xoè, diềm "
                  "cánh sen sau đầu",
            "who": ("the same lotus fire dragon grown young and agile: slimmer and taller, rose-red with deeper crimson "
                    "stripes on the back (#B8323C); swept-back cream horns; larger wings of overlapping lotus-petal flames "
                    "(pink, rose, yellow base) half spread up behind; a frill of small petal flames on the back of the head; "
                    "a longer tail ending in an open lotus flame.")},
        3: {"name": "Hồng Liên", "kind": "raptor",
            "vn": "rồng lửa sen đỏ: vảy đỏ thẫm, vương miện sừng vàng như gương sen, cánh lửa nhiều lớp cánh sen xoè, trang "
                  "sức ngực hoa sen vàng hồng ngọc, vuốt vàng",
            "who": ("the same dragon as the Red Lotus, a graceful fire dragon: crimson (#B8323C) and rose-red scales with "
                    "cream belly plates; a crown of golden horns (#E0A93A) shaped like a lotus pod; large wings made of many "
                    "layered lotus-petal flames spread up and back; a golden lotus-shaped chest ornament with a ruby; golden "
                    "claws; a long tail ending in a big blooming lotus flame; elegant, fierce and noble.")}}},
    "giap_long": {"order": 40, "forms": {
        1: {"name": "Giáp Long Con", "kind": "quad",
            "vn": "rồng giáp con: thân đỏ thẫm, giáp thép xám xanh trên đầu (một sừng thép ở mõm), lưng, vai; mào lửa sau "
                  "mũ, chóp đuôi lửa",
            "who": ("a chibi ARMOURED FIRE DRAGON pup on four legs: a chubby crimson body (#C8323A) with a cream belly "
                    "(#F3DCC6); steel armour plates of blue-grey gunmetal (#6E7A94, darker rivets #4A5266) on its head (a "
                    "helmet-plate with one short steel horn on the snout), back and shoulders; red-orange claws (#E8582E); a "
                    "flame crest behind the helmet and a flame tail tip (red, orange, yellow bands); golden eyes.")},
        2: {"name": "Giáp Long", "kind": "quad",
            "vn": "rồng giáp lửa: giáp thép kín, gai thép lớn chóp đỏ lửa dọc lưng, vai, đuôi; mũ giáp hai sừng thép; bờm "
                  "lửa dọc cổ; vuốt đỏ",
            "who": ("the same dragon as a heavy armoured fire dragon: crimson body; full gunmetal steel armour with big steel "
                    "spikes whose tips are fiery red-orange (#E8582E) along the back, the shoulders and the tail; a horned "
                    "steel helmet with two swept-back steel horns; a flame mane flowing from under the helmet along the "
                    "neck; large red claws; a long armoured tail ending in a steel spike with a flame; massive and fierce.")}}},
    "huyen_viem": {"order": 50, "forms": {
        1: {"name": "Linh Viêm", "kind": "fox",
            "vn": "cáo lửa ảo con: lông đỏ hồng sẫm, chóp tai lửa tím, một đuôi chóp lửa tím hồng, dấu trăng khuyết vàng "
                  "trên trán, mắt tím",
            "who": ("a chibi ILLUSION FIRE FOX kit: deep rose-red fur (#C2405A) with a cream muzzle, chest and paw tips "
                    "(#F6E3D6); big pointed ears whose tips are violet flames (#8C5FD0 with a pink #E06AB0 inner band); one "
                    "fluffy tail ending in a violet-and-pink flame; a golden crescent-moon mark on the forehead (#E0A93A); "
                    "violet eyes (#7A4FC8).")},
        2: {"name": "Huyễn Viêm", "kind": "fox",
            "vn": "cáo ảo trẻ: hai đuôi lửa tím hồng xoè, tai dài chóp lửa tím, dấu trăng vàng ở trán và vai, diềm lửa hồng "
                  "ở cổ",
            "who": ("the same illusion fox grown lean and quick: TWO flame tails (violet and pink bands) fanned up behind "
                    "from one root; longer ears with violet flame tips; golden crescent marks on the forehead and the "
                    "shoulders; a short ruff of pink flame fur at the neck; sharper eyes and small fangs.")},
        3: {"name": "Thánh Huyễn Viêm", "kind": "fox",
            "vn": "thánh hồ lửa ảo: ba đuôi lửa lớn xoè (tím, hồng, vàng), vương miện trán vàng ngọc tím, trang sức trăng "
                  "vàng nối chuỗi hạt tím, vòng chân vàng",
            "who": ("the same fox as the holy illusion fox: THREE large flame tails fanned up behind from one root (violet, "
                    "pink and gold bands); an ornate golden forehead crown with a violet gem; golden crescent ornaments on "
                    "the shoulders joined by a string of violet beads across the chest; a flowing ruff of pink flame around "
                    "the neck; elegant long legs with golden anklets; mystical, fierce and beautiful.")}}},
    "hoa_tinh": {"order": 60, "forms": {
        1: {"name": "Tiểu Hỏa Tinh", "kind": "fox",
            "vn": "sói lửa con: lông đỏ san hô, ngực mõm kem, đuôi xù hình ngọn lửa, viên hồng ngọc trên trán",
            "who": ("a chibi FIRE WOLF pup: fiery coral-red fur (#E2553F) with a cream chest, muzzle and paw tips (#F6E3CC); "
                    "a fluffy flame-shaped tail (coral #F07A6A, orange and pale-yellow bands); a small faceted ruby crystal "
                    "(#C8243C with lighter facets #E85A6E) on the forehead; pointed ears with dark-brown tips; golden eyes; "
                    "small fangs.")},
        2: {"name": "Hỏa Tinh", "kind": "fox",
            "vn": "sói giáp lửa hồng: giáp đá vỏ chai viền vàng ở đầu, vai, chân trước; cụm hồng ngọc mọc trên giáp vai; bờm "
                  "lửa hồng san hô; đuôi lửa lớn",
            "who": ("the same wolf as an armoured fire wolf: lean and powerful, coral-red fur; obsidian armour plates "
                    "(#2E2A33 with gold trim #E0A93A) on the head, the shoulders and the front legs; clusters of ruby "
                    "crystals rising from the shoulder plates; a mane of coral-pink flames flowing back along the neck; a "
                    "big flame tail; a ruby crystal on the forehead plate; majestic and fierce.")}}},
    "lan_hoa": {"order": 70, "forms": {
        1: {"name": "Lân Con", "kind": "quad",
            "vn": "kỳ lân lửa con: vảy đỏ thẫm, bụng kem, bờm xoắn lửa đỏ vàng, một sừng vàng nhỏ, móng vàng, xoắn mây lửa "
                  "ở khuỷu",
            "who": ("a chibi FIRE QILIN calf (the mythical scaled deer of good fortune): crimson scales (#C8323A) on the back "
                    "and legs with a cream belly (#F6E3C8); a curly mane of red-and-gold flame swirls (#D9483B, #F2C14E); one "
                    "small golden antler-horn (#E0A93A) on the forehead; golden hooves; cloud-shaped flame curls at the "
                    "elbows; a tail ending in a curly flame tuft; big golden eyes with determined brows.")},
        2: {"name": "Lân Ngàn Năm", "kind": "quad",
            "vn": "kỳ lân trẻ: chân dài hơn, bờm lửa lớn, hai sừng vàng phân nhánh, viền vảy ngọc bích dọc sống lưng, giáp "
                  "ngực vân mây vàng",
            "who": ("the same qilin grown into a proud young qilin: longer legs; a bigger mane of red-and-gold flame swirls; "
                    "two branching golden antlers; jade-green (#3FA88F) scale edges along the spine; golden cloud-pattern "
                    "plates on the chest; flame curls at the elbows and the tail; small fangs.")},
        3: {"name": "Thánh Lân", "kind": "winged",
            "vn": "thánh kỳ lân: vảy đỏ vàng, bờm lửa trắng vàng đỏ lộng lẫy, sừng vàng lớn chóp ngọc bích, giáp vàng chạm "
                  "mây, hai cánh lông lửa xoè sau vai, đuôi lửa xoắn lớn",
            "who": ("the same qilin as the Holy Qilin: crimson and gold scales; a magnificent mane of white-gold (#F6E7B0) and "
                    "red flame swirls; large branching golden antlers with jade-green tips; ornate golden armour plates "
                    "with cloud reliefs on the chest, the shoulders and the legs; two wings made of long flame feathers (red, "
                    "orange and gold bands) rising up and back behind the shoulders; a long tail ending in a big swirling "
                    "flame; majestic and imposing.")}}},
}


def code(hid, k):
    return f"{hid}_{k}"


def paths(hid, k):
    c = code(hid, k)
    out_dir = W(HERE, "gui_gpt", c)
    save_dir = W(INBOX, c, "tai_ve")
    return c, out_dir, save_dir, W(save_dir, "L1_lien.png")


def picked(c):
    """ảnh Claude chọn của một dạng: L1_duyet.png nếu có (bản gen lại được chọn), không thì L1_lien.png."""
    for p in (W(INBOX, c, "L1_duyet.png"), W(INBOX, c, "tai_ve", "L1_lien.png")):
        if os.path.isfile(p):
            return p
    return None


def refs_of(hid, k):
    f = LINES[hid]["forms"][k]
    pose, second = POSE_REF[f["kind"]]
    out = [(picked(pose), REFS[pose][0], "pose"), (picked(second), REFS[second][0], "style")]
    for j in range(1, k):
        out.append((picked(code(hid, j)), None, j))
    return out


def luot_1(hid, k):
    ln = LINES[hid]
    forms = ln["forms"]
    f = forms[k]
    c, out_dir, save_dir, save = paths(hid, k)
    refs = refs_of(hid, k)
    if any(p is None for p, _, _ in refs):
        return None
    lines_img = []
    for p, d, role in refs:
        if role == "pose":
            lines_img.append((p, f"another hero of the same game ({d}), drawn exactly the way we need, 1536x1024, white "
                                 f"background: copy its framing, its pose logic (three-quarter side view facing right, limbs "
                                 f"separated by white gaps), its hand-drawn pen line and its flat crayon colouring. Do NOT copy "
                                 f"its species, design or colours"))
        elif role == "style":
            lines_img.append((p, f"another approved hero of the same game ({d}), 1536x1024, white background: match EXACTLY "
                                 f"its hand-drawn pen line, crayon texture, flat colouring, simple readable shapes and "
                                 f"determined expression. Do NOT copy its species, design or colours"))
        else:
            lines_img.append((p, f"FORM {role} of this same creature (approved), 1536x1024, white background: keep the same "
                                 f"species, face, colours, markings and drawing style so the line clearly grows up"))
    lines_img.append((WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen "
                                   "outline + coloured pencil / wax crayon hatching), nothing of its content"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(lines_img))
    stage = FINAL2 if (len(forms) == 2 and k == 2) else CHIBI[k]
    boss = ""
    if ln["order"] >= 70:
        boss = ("\nThis line is the island's FINAL boss: the most splendid and refined design of the whole island (elegant "
                "shapes, rich but readable golden ornament), more so for later forms.")
    elif ln["order"] >= 30:
        boss = ("\nThis line belongs to one of the island's bosses: make the design especially beautiful and refined (elegant "
                "shapes, rich but readable ornament), more so for later forms.")
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the hand-drawn style of images 1 and 2.

CREATURE: {SPIRIT}
{stage}
{f['who']}{boss}

{FLAMES}

CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature is visible, nothing cut by the edges, at least 60 px of white margin all round. It is centred, about 720 px tall from the top of its head (ears, horns, crest or flames included) to its lowest point; its lowest point is about 120 px above the bottom edge.

POSE (very important: the picture will be animated as ONE single drawing with a simple 2D skeleton, so body parts must be readable and must not overlap):
- Side three-quarter view turned toward the viewer's RIGHT; the head is at the right, the eyes look to the viewer's right.
{POSES[f['kind']]}
- Nothing covers the face: no flame lock crosses the eyes. Ears, horns, crest, mane flames and wings do not cross each other.

{line(7).replace("of the style image, NOT the glossy look of the design image", "of images 1 and 2")}

Keep the design clean and readable: no text, no background, no extra props, no effects around the creature.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


KIND_VN = {"quad": "bốn chân", "fox": "bốn chân (thân thon)", "humanoid": "đứng hai chân, tay tách thân",
           "raptor": "rồng đứng hai chân, cánh sau vai", "blob": "tròn, tay chân ngắn", "genie": "bay, không chân, đuôi dung nham",
           "winged": "bốn chân, hai cánh sau vai"}


def huong_dan(hid):
    ln = LINES[hid]
    out = [f"# {hid}: tướng .atomik đảo Hỏa (rig từ một ảnh liền)", "",
           f"Đảo Hỏa, ải {ln['order']}. Làm theo cách hai đảo Thủy, Mộc: thú huyền thoại hơi chibi kiểu Pokémon, style cũ, dạng "
           f"sau dữ hơn nhưng không quá, hạn chế dạng người. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người "
           f"dùng muốn tự gửi thì chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).", ""]
    for k, f in ln["forms"].items():
        c, out_dir, save_dir, save = paths(hid, k)
        prompt = W(out_dir, "luot_1_lien.txt")
        out += [f"## Dạng {k}: {f['name']} ({KIND_VN[f['kind']]})", f"- Thiết kế: {f['vn']}."]
        if os.path.isfile(prompt) and all(p for p, _, _ in refs_of(hid, k)):
            out.append(f"- File prompt: `{prompt}`.")
        else:
            out.append(f"- File prompt: chưa dựng, chờ ảnh dạng {k - 1} được duyệt (chạy lại `build_hoa.py {hid}`).")
        pose, second = POSE_REF[f["kind"]]
        out.append("- Ảnh mẫu theo thứ tự:")
        out.append(f"  1. `{picked(pose)}`: {REFS[pose][1]}; 1536x1024, nền trắng; lấy khung, dáng, nét.")
        out.append(f"  2. `{picked(second)}`: {REFS[second][1]}; 1536x1024, nền trắng; lấy nét, tô.")
        n = 3
        for j in range(1, k):
            out.append(f"  {n}. ảnh dạng {j} đã duyệt của dòng này (`{W(INBOX, code(hid, j))}`, L1_duyet.png hoặc "
                       f"tai_ve/L1_lien.png); 1536x1024, nền trắng; giữ loài, màu, mặt.")
            n += 1
        out.append(f"  {n}. `{WORLD_STYLE}`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.")
        out += [f"- Lưu: `{save}` (trùng tên thì `L1_lien_2.png`, `_3`...).", ""]
    out += ["## Kiểm",
            "- Thú, không mặt người; mặt quả quyết, mắt nhìn sang phải; nhìn nghiêng 3/4 sang phải.",
            "- Tô phẳng: không bóng, không điểm sáng, không phát sáng; lửa là mảng màu có viền mực khép kín, tối đa ba dải màu, "
            "không để giấy trắng; không tàn lửa, khói bay quanh.",
            "- Chân tách nhau có khe trắng, tay tách thân, đuôi không vắt qua thân, cánh không đè đầu, sừng.",
            "- Khung 1536x1024, con cao khoảng 720 px, chừa lề trắng; không đường đất, không bóng dưới chân.",
            "- Dạng sau cùng loài, cùng màu, cùng dấu hiệu dạng trước.", "",
            "## Câu sửa nhanh (gửi kèm `--note`)",
            "- \"Flat colour only: no shine spots, no shading, no glow; the flames do not light up the body.\"",
            "- \"Close every flame with a dark-brown ink outline and fill it with flat crayon colour, never white paper; no "
            "floating sparks or embers.\"",
            "- \"Keep white gaps between the legs and between each arm and the body; the tail must not cross the body.\"",
            "- \"More determined face: lowered brows, firm mouth, not a happy grin.\""]
    p = W(HERE, "gui_gpt", code(hid, 1), "HUONG_DAN.md")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return p


def huong_dan_dao():
    out = ["# Đảo Hỏa: 10 dòng tướng .atomik (gen một ảnh liền, rig một lưới)", "",
           "Sinh bằng `py -3 -I ArtGen/Spine/build_hoa.py [id ...]`. Mỗi dòng có `gui_gpt/<id>_1/HUONG_DAN.md` (ảnh mẫu, chỗ "
           "lưu, cách kiểm). Dạng 2, 3 chỉ dựng khi ảnh dạng trước đã có.", "",
           "| Ải | Dòng | Dạng | File prompt |", "|---|---|---|---|"]
    for hid, ln in LINES.items():
        for k, f in ln["forms"].items():
            p = W(HERE, "gui_gpt", code(hid, k), "luot_1_lien.txt")
            built = os.path.isfile(p) and all(x for x, _, _ in refs_of(hid, k))
            out.append(f"| {ln['order']} | `{hid}` | {k}. {f['name']} | {('`' + p + '`') if built else 'chờ dạng trước'} |")
    p = W(HERE, "gui_gpt", "HUONG_DAN_hoa.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return p


def main(ids):
    for n in {r for pair in POSE_REF.values() for r in pair}:
        if not picked(n):
            sys.exit("thiếu ảnh mẫu: " + n)
    if not os.path.isfile(WORLD_STYLE):
        sys.exit("thiếu ảnh mẫu: " + WORLD_STYLE)
    for hid in ids or list(LINES):
        if hid not in LINES:
            sys.exit("không có dòng: " + hid)
        for k in LINES[hid]["forms"]:
            p = luot_1(hid, k)
            if p:
                print(p)
        print(huong_dan(hid))
    print(huong_dan_dao())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
