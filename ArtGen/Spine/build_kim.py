# -*- coding: utf-8 -*-
"""Gói prompt Codex cho 10 dòng tướng đảo Kim vẽ lại thành tướng .atomik (2026-11-09, máy ổ D).

Theo cách đảo Hỏa (build_hoa.py, QUY_TRINH mục 19): Claude tự thiết kế, gen trọn con LIỀN một ảnh, rig một lưới bằng beast.py.
Khác Hỏa theo lời người dùng dặn khi giao đảo Kim: học từ thiết kế dòng aola gốc (xem hình goc_<id>_portrait.png); CHỈ dạng 1
chibi, dạng sau hết chibi, càng tiến hóa càng dữ, chiến, ngầu và đẹp hơn. Tướng gốc dạng robot, người giáp (Phi Thương, Khiên
Bạc, Chiến Thần, Thiết Phủ, Tam Kiếm) đổi thành thú mặc giáp, giữ vũ khí, màu chủ, mô-típ của gốc (người dùng duyệt 2026-11-09).

Mỗi dạng: gui_gpt/<id>_<k>/luot_1_lien.txt -> inbox/<id>_<k>/tai_ve/L1_lien.png. Dạng k > 1 đính ảnh các dạng trước
(L1_duyet.png nếu có, không thì L1_lien.png); dạng chưa có ảnh dạng trước thì chưa dựng.

    py -3 -I ArtGen/Spine/build_kim.py [id ...]
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
    "canh_cut_1": ("a round chibi penguin with short limbs holding a pan", "cánh cụt tròn chân tay ngắn cầm chảo (đảo Thủy)"),
    "gio_loc_2": ("a winged dragon floating in the air", "rồng chuồn chuồn bay lơ lửng (đảo Mộc)"),
    "giap_long_2": ("a low armoured dragon on four legs with its tail raised behind",
                    "rồng giáp bốn chân thân thấp, đuôi dựng sau (đảo Hỏa)"),
    "kim_su_3": ("a proud armoured lion on four legs", "sư tử giáp vàng bốn chân (đảo Hỏa)"),
    "nguu_quyen_3": ("a muscular bull brawler standing upright on its two legs",
                     "bò quyền thủ đứng hai chân, tay tách thân (đảo Hỏa)"),
    "mi_nhi_2": ("a bird standing on its two legs, wings held out", "chim đứng hai chân, cánh dang (đảo Thủy)"),
}

# kiểu dáng -> (ảnh mẫu dáng, ảnh mẫu nét thứ hai)
POSE_REF = {"scorp": ("giap_long_2", "de_hoa_1"), "quad": ("de_hoa_1", "moc_tinh_2"), "quad_big": ("moc_tinh_2", "de_hoa_1"),
            "hooves": ("kim_su_3", "de_hoa_1"), "mantis": ("long_vuot_2", "de_hoa_1"), "blob": ("canh_cut_1", "de_hoa_1"),
            "bird": ("mi_nhi_2", "de_hoa_1"), "flyer": ("gio_loc_2", "de_hoa_1"),
            "lancer": ("nguu_quyen_3", "de_hoa_1"), "guard": ("nguu_quyen_3", "de_hoa_1"),
            "axe": ("nguu_quyen_3", "de_hoa_1"), "sword": ("nguu_quyen_3", "de_hoa_1")}

_QUAD = ("- Stands on its FOUR legs, all paws flat on one level ground line (no ground drawn), a grounded ready-to-fight "
         "stance: the front a little lower, head forward.\n- All four legs are visible: the two near legs in front, the two "
         "far legs peeking out behind them; white gaps between the front pair and the back pair, and between each near leg "
         "and the far leg next to it where possible.\n- The tail sweeps up and back behind the body on the viewer's LEFT, "
         "clear of the legs with white space between, never crossing the body.")
_UP = ("- Stands upright on its two legs, both feet flat on one level ground line (no ground drawn), feet apart with a white "
       "gap between the legs, a grounded ready-to-fight stance.\n")
POSES = {
    "scorp": ("- A scorpion standing low on its legs, all feet on one level ground line (no ground drawn).\n- THREE walking legs "
              "are visible on the near side, the far-side legs only peek out behind them; white gaps between the legs.\n- The "
              "two big pincers reach forward to the viewer's right on short arms, a little apart from each other and from the "
              "face, with white space between them.\n- The segmented tail rises from the rear on the viewer's LEFT and arches "
              "up and forward ABOVE the back, the stinger high above the back; white space between the tail and the back, "
              "the tail never touches the head."),
    "quad": _QUAD,
    "quad_big": _QUAD,
    "hooves": ("- Stands on its FOUR legs, all hooves flat on one level ground line (no ground drawn), a proud ready-to-charge "
               "stance, head and neck raised forward.\n- All four legs are visible with white gaps between the front pair and "
               "the back pair; the cape stops above the knees and never covers the legs.\n- The mane falls behind the neck, "
               "the tail sweeps back on the viewer's LEFT, clear of the legs."),
    "mantis": (_UP.replace("two legs", "two thin hind legs (insect legs with a knee bend)") +
               "- The abdomen points back and down on the viewer's LEFT, clear of the legs.\n- The two scythe arms are raised "
               "in a fighting guard, away from the body with white space around them: the near scythe forward at chest "
               "height on the viewer's right, the far scythe raised higher behind it; the blades never cross the face or "
               "each other.\n- Wings (if any) rise or fold behind the shoulders, clear of the head and the antennae."),
    "blob": ("- Stands on its short legs, feet flat on one level ground line (no ground drawn), a grounded ready-to-fight "
             "stance.\n- Its small arms are held a little away from the round body with white space between each arm and "
             "the body; anything it holds is raised at shoulder height away from the body and the face."),
    "bird": (_UP + "- Its wings are held a little away from the body like arms, with white space between each wing and the "
             "body; the wing tips do not cover the face.\n- The tail feathers point back and down on the viewer's LEFT."),
    "flyer": ("- It FLIES (no ground drawn): its lowest point (talons) is about 90 px above where the ground would be.\n- Both "
              "wings are spread up and back above the shoulders, fully visible, clear of the head and of each other: the "
              "near wing in front, the far wing behind it, offset so both are readable.\n- The legs hang below the body, "
              "talons open, white space between the two legs.\n- The tail sweeps back on the viewer's LEFT."),
    "lancer": (_UP + "- The near arm holds one lance pointing forward and slightly down to the viewer's right; the far arm "
               "holds the other lance raised up and back on the viewer's left, pointing upward; both lances are straight and "
               "fully visible, clear of the head, the body and the legs, with white space around them; each hand grips its "
               "lance."),
    "guard": (_UP + "- The near arm holds the big shield out to the viewer's RIGHT beside the body at waist height, facing the "
              "viewer, NOT covering the body or the face; the far arm holds the spear upright behind the body on the viewer's "
              "left, the spear head above the shoulder, clear of the head; white space between the weapons and the body."),
    "axe": (_UP + "- The near arm holds the long-hafted weapon upright beside the body on the viewer's RIGHT, the shaft "
            "vertical, its blade above the shoulder and clear of the head with white space between; the other fist is "
            "clenched at hip height, a little away from the body."),
    "sword": (_UP + "- The near arm holds its sword forward and slightly down to the viewer's right, the blade clear of the legs; "
              "if there is a second sword the far arm raises it up and back on the viewer's left, clear of the head; white "
              "space between blades, arms and body.\n- A cape (if any) hangs behind on the viewer's LEFT and stops above the "
              "knees."),
}

# luật lớn lên (người dùng dặn 2026-11-09): chỉ dạng 1 chibi
STAGE = {
    "c1": ("FORM 1, the young stage: clearly chibi like a monster-collecting game starter: a big head (about 45% of the "
           "creature's height), a compact round body, short sturdy limbs, big expressive eyes. Cute but already brave."),
    "m2": ("FORM 2, the same creature grown into a young warrior: NOT chibi any more: the head is only about 30% of its "
           "height, longer limbs, a leaner and stronger body, sharper narrowed eyes, small fangs or spikes, a battle-ready "
           "stance. Clearly the same species and markings as form 1, visibly stronger and cooler."),
    "f2": ("FORM 2, the FINAL stage of this two-stage line: fully grown and NOT chibi: heroic proportions, the head only about "
           "25% of its height, a strong athletic body, full battle armour and weapons, sharp fierce eyes. The coolest and most "
           "beautiful design of the line: fierce, proud and battle-hardened, but NOT scary or monstrous. Clearly the same "
           "species and markings as form 1."),
    "f3": ("FORM 3, the FINAL stage: fully grown and NOT chibi: heroic proportions, the head only about 25% of its height, a "
           "powerful athletic body, full battle armour and weapons, sharp fierce eyes. The coolest and most beautiful design "
           "of the line: fierce, proud and battle-hardened, but NOT scary or monstrous. Clearly the same species and markings "
           "as forms 1 and 2."),
    "solo": ("This hero has ONLY ONE form, so draw it fully grown and NOT chibi: heroic proportions, the head only about 28% "
             "of its height, proud and battle-ready, sharp fierce eyes, the coolest and most beautiful version of this "
             "creature, but NOT scary or monstrous."),
}

SPIRIT = ("a MYTHICAL METAL BEAST of the metal element: an ANIMAL creature (not a human: no human face, no human body; it may "
          "wear the armour and hold the weapons listed), designed like a creature of a monster-collecting game: appealing, "
          "simple readable shapes. Its face is DETERMINED and ready to fight: lowered brows, confident focused eyes looking to "
          "the viewer's right, mouth set firm or slightly open; never a happy mascot grin, never scary.")

METAL = ("ARMOUR, METAL AND CRYSTAL: every armour plate, blade, weapon and gem is a flat shape with a closed dark-brown ink "
         "outline, filled with ONE flat crayon colour (trims are a second flat colour drawn as a separate band); no shine "
         "spots, no white highlights, no reflections, no chrome or metallic gradients, no sparkle; crystals and gems are flat "
         "colour with a few darker facet lines, and nothing glows. The armour follows the animal's body so the animal stays "
         "readable: its face, ears, paws or claws and tail are clearly visible.")

FLAMES = ("BLUE FLAMES: every flame (mane, elbow tufts, tail tip) is a solid part of the creature: a flat shape with a closed "
          "dark-brown ink outline, filled with flat crayon colours in at most three clear bands, never left as white paper; "
          "attached to the body, no loose floating flames or sparks; the flames do not glow or light up the body.")

# id -> ải, mỗi dạng: tên (theo heroes.json), kiểu dáng, giai đoạn, thiết kế tiếng Việt, mô tả tiếng Anh;
# "keep" (tuỳ chọn): câu tiếng Anh thay câu giữ màu khi đính ảnh dạng trước
LINES = {
    "bo_cap": {"order": 1, "gốc": "676→677→678: bọ cạp đeo ngọc pha lê tròn ở càng, đuôi; vỏ xanh ngọc → lục → đỏ đồng",
               "keep": ("keep the same species, face shape, body plan and the round turquoise crystal gems so the line "
                        "clearly grows up; the SHELL COLOUR changes as described for this form"),
               "forms": {
        1: {"name": "Bọ Cạp Pha Lê", "kind": "scorp", "stage": "c1",
            "vn": "bọ cạp con tròn, vỏ bạc ánh xanh ngọc, hai càng to ôm ngọc pha lê lam, đuôi cong ngắn chóp ngọc",
            "who": ("a chibi CRYSTAL SCORPION: a round compact body with a big head-shell and big eyes; smooth shell plates of "
                    "pale silver-teal (#9FD3CF) with thin teal trims (#4E9A97); two oversized round pincers, each holding a "
                    "round turquoise crystal gem (#3FB6D8) set in a small bronze rim (#C8873A); short stubby legs; a short "
                    "curled tail of four round segments ending in a round crystal-gem stinger.")},
        2: {"name": "Bọ Cạp Đá Lục", "kind": "scorp", "stage": "m2",
            "vn": "bọ cạp trẻ thon, vỏ lục bảo như đá, hàng gai lưng, càng dài răng cưa, ngọc lam ở càng, đầu, chóp đuôi",
            "who": ("the same scorpion grown into a lean, tough young scorpion: jade-green stone-like shell plates (#3E9A5A) "
                    "with thin dark-green trims (#2B6B3F) and a row of short pointed spines along the back; longer, sharper "
                    "pincers with jagged inner edges; the same turquoise crystal gems (#3FB6D8) in bronze rims, now set in "
                    "both pincers, on top of the head-shell and on the stinger; longer legs; a longer tail of five segments "
                    "with a sharp curved stinger; narrowed determined eyes.")},
        3: {"name": "Bọ Cạp Đồng", "kind": "scorp", "stage": "f3",
            "vn": "bọ cạp chiến đồng đỏ viền vàng, càng như lưỡi kéo lớn, đuôi sáu đốt cong cao qua lưng, ngọc lam ở càng, vai, "
                  "chóp đuôi",
            "who": ("the same scorpion as a mighty bronze war scorpion: copper-red armour shell (#B9532F) with bronze-gold "
                    "trims (#D9A441) along every plate; big blade-like pincers like heavy shears; turquoise crystal gems "
                    "(#3FB6D8) set in the pincers, on both shoulders and a big one at the base of the stinger; a long "
                    "six-segment tail arching high above the back, ending in a large hooked stinger; a sleek, low, powerful "
                    "body, a crested head plate over narrowed fierce eyes.")}}},
    "doc_giac": {"order": 5, "gốc": "656: ngựa một sừng giáp bạc, bờm đỏ dài, áo choàng đỏ có huy hiệu, sừng vàng", "forms": {
        1: {"name": "Độc Giác Thép", "kind": "hooves", "stage": "solo",
            "vn": "ngựa một sừng trưởng thành giáp bạc viền vàng, bờm và đuôi đỏ thẫm dài, áo choàng đỏ ngắn lót lam có huy "
                  "hiệu vàng, sừng xoắn vàng, ngọc lam trên trán",
            "who": ("a proud ARMOURED UNICORN: a white horse (#EEF0F2) clad in silver armour plates (#B8C3CC) trimmed with "
                    "gold (#D9A441): a face plate with a turquoise gem (#3FB6D8) on the forehead, a neck guard, a chest "
                    "plate and leg guards; a long golden spiral horn; a long flowing crimson mane (#B5302A) with darker "
                    "crimson locks (#7E1F22) and a matching crimson tail; a short royal-red cape (#C8352E) lined with deep "
                    "blue (#2E4A8C) over its back, held by gold clasps, with a small gold crest on it; dark navy hooves "
                    "(#2B3550).")}}},
    "bo_ngua": {"order": 10, "gốc": "683→684→685: bọ ngựa lục mắt to → giáp lam → thân thon hai liềm trăng khuyết lớn, ngọc đỏ "
                                    "ở khớp", "forms": {
        1: {"name": "Bọ Ngựa Con", "kind": "mantis", "stage": "c1",
            "vn": "bọ ngựa con đầu tam giác mắt to, vỏ lục ngọc bụng kem, liềm thép ngắn, ngọc đỏ ở khuỷu",
            "who": ("a chibi MANTIS: a big triangular head with huge round amber eyes (#E8A030) and two tiny antennae; a "
                    "leaf-jade carapace (#4FB36A) with a cream belly (#EEF2DE); two short curved scythe arms with small "
                    "silver-steel blades (#B8C8D6); a small red gem (#C8352E) on each elbow; a round little abdomen.")},
        2: {"name": "Bọ Ngựa Lưỡi Bén", "kind": "mantis", "stage": "m2",
            "vn": "bọ ngựa kiếm khách trẻ thân cao thon, liềm dài như kiếm, cánh lá thép gập sau lưng",
            "who": ("the same mantis grown into a lean young blade fighter: a tall slim body, a sharper triangular head with "
                    "narrowed amber eyes and long antennae swept back; jade-green carapace (#3E9A5A) with a cream belly and "
                    "plates of silver steel on the shoulders; long sword-like steel scythe blades (#B8C8D6) on both "
                    "forearms; slim steel-green wings (#7FB8A0) folded behind the back like blades; red gems (#C8352E) on "
                    "the elbows.")},
        3: {"name": "Bọ Ngựa Liềm Thép", "kind": "mantis", "stage": "f3",
            "vn": "bọ ngựa bậc thầy kiếm: hai liềm trăng khuyết thép lớn, giáp lục sẫm và bạc, ngọc đỏ ở khuỷu và trán, cánh "
                  "thép xoè như áo choàng",
            "who": ("the same mantis as a master blade warrior: tall, sleek and powerful; deep jade armour (#2F8550) with "
                    "silver-steel plates (#B8C8D6) on the shoulders and thorax; two huge crescent-moon scythes of steel "
                    "(#B8C8D6) with a gold trim at the base (#D9A441) on its forearms; ruby-red gems (#C8352E) at the elbow "
                    "joints and on the forehead; long blade-shaped steel-green wings (#7FB8A0) spread behind the shoulders "
                    "like a cape; long swept-back antennae; cold focused amber eyes.")}}},
    "phi_thuong": {"order": 15, "gốc": "835→836: kỵ sĩ máy mặt nạ tối mắt vàng, hai sừng vàng, hai mũi thương pha lê lam và đỏ",
                   "forms": {
        1: {"name": "Phi Thương Con", "kind": "quad", "stage": "c1",
            "vn": "nhím thép con bốn chân, mặt lông xanh đen mắt vàng, gai thép lam chóp vàng, hai gai vàng lớn trên đầu như "
                  "sừng chữ V",
            "who": ("a chibi STEEL PORCUPINE: a round body covered in a thick coat of steel-blue quills (#5D7FA6) tipped with "
                    "gold (#E0B23A); a dark navy fur face mask (#2B3550) with bright yellow eyes (#F2C230) and a cream "
                    "muzzle (#F1E6D0); two longer golden quills rising from the top of its head in a V like two horns; short "
                    "legs with cream paws; a short tail of quills.")},
        2: {"name": "Phi Thương", "kind": "lancer", "stage": "f2",
            "vn": "nhím kỵ sĩ đứng hai chân, bờm gai dựng thành chữ V vàng, áo choàng gai thép trên vai, giáp thép lam nhạt, hai "
                  "thương pha lê lam và đỏ",
            "who": ("the same porcupine as a fully grown lance knight standing upright: tall and athletic; its steel-blue "
                    "quills (#5D7FA6, gold tips #E0B23A) sweep back into a crest of long golden quills shaped like a V on "
                    "the head and a mantle of long steel quills over the shoulders and back; dark navy face mask (#2B3550) "
                    "with sharp yellow eyes (#F2C230); light steel-blue armour plates (#8FA9C9) on the chest, shoulders, "
                    "forearms and shins; two long faceted crystal lances with gold grips: a sapphire-blue one (#3F7FD0) in "
                    "the near hand and a ruby-red one (#C8352E) in the far hand.")}}},
    "khien_bac": {"order": 20, "gốc": "784→785: mũ sắt lam trắng có mặt nhỏ ló ra → hiệp sĩ khiên lớn lam, ngọc lục, chữ thập "
                                      "vàng, giáo", "forms": {
        1: {"name": "Khiên Sắt Tí Hon", "kind": "quad", "stage": "c1",
            "vn": "tatu con, mai tròn lam trắng như mũ sắt có đinh vàng, mặt ló dưới vành mai, chân ngắn",
            "who": ("a chibi ARMADILLO: a big round dome shell like a sky-blue knight's helmet (#5FA8E0) with white bands "
                    "(#F2F5F8) across it and two gold rivets (#D9A441) on the front rim; its small face peeks out under the "
                    "front rim of the shell: pale tan skin (#E9C9A0), big determined eyes, small rounded ears; four short "
                    "sturdy legs with cream claws; a short tail with a blue plated tip.")},
        2: {"name": "Vệ Sĩ Khiên Bạc", "kind": "guard", "stage": "f2",
            "vn": "tatu vệ sĩ đứng hai chân, giáp bạc lam từ dải mai, mũ đầu có vây lam, khiên lớn hình mũi tên ngọc lục chữ "
                  "thập vàng, giáo ba mũi cán vàng",
            "who": ("the same armadillo as a fully grown shield guardian standing upright: broad, sturdy and strong; its shell "
                    "bands have become silver-blue plate armour (#9FB8D6) with white bands (#F2F5F8) over the back, "
                    "shoulders and forearms; a helmet-like head plate with a blue crest fin (#4F95D8); tan face (#E9C9A0) "
                    "with sharp determined eyes; in the near hand a big kite shield shaped like an arrowhead, sky blue "
                    "(#4F95D8) with a silver rim (#C9D3DC), a green gem (#3E9A5A) in the centre and a small gold cross mark "
                    "(#D9A441); in the far hand a short trident spear with a gold shaft.")}}},
    "chien_than": {"order": 30, "gốc": "1083→1084: robot vàng tròn mắt lục, cánh nhỏ, bay → chiến thần máy vàng có cánh, tay "
                                       "pháo", "forms": {
        1: {"name": "Chiến Linh Con", "kind": "bird", "stage": "c1",
            "vn": "cú con lông vàng tròn, mặt trắng, mắt lục bảo, túm tai như sừng mũ, đầu cánh đeo găng lam",
            "who": ("a chibi GOLDEN OWLET: a round body of golden feathers (#E8B53A) with a cream belly patterned with small "
                    "gold scales; a white face disc (#F4F1E6) with huge emerald-green eyes (#2FA36B) and a small bronze beak "
                    "(#C8873A); two feather tufts on the head like the horns of a helmet; short wings used like arms, each "
                    "wing tip wearing a round sky-blue gauntlet (#4FA3D9); two short legs with bronze talons.")},
        2: {"name": "Chiến Thần", "kind": "flyer", "stage": "f2",
            "vn": "cú sừng chiến giáp vàng chạm khắc đang bay, cánh dài viền lam, ống pháo lam ở cổ cánh, móng vàng",
            "who": ("the same owl as a fully grown golden war owl, flying: powerful and noble; golden armour feathers "
                    "(#E0A92E) with engraved gold plates on the chest and the head; long horn-like ear tufts swept back like "
                    "a crested helmet; a white face disc (#F4F1E6) with sharp emerald eyes (#2FA36B) and a hooked bronze "
                    "beak; long broad wings of golden feathers edged with sky blue (#4FA3D9), each wing carrying a short "
                    "sky-blue cannon barrel with a gold muzzle at its wrist; strong legs with gold talons; a fan of tail "
                    "feathers.")}}},
    "thiet_phu": {"order": 40, "gốc": "1533→1534: hiệp sĩ thiếc đỏ tròn mắt lam, chùm lông trắng, chùy → rìu kích", "forms": {
        1: {"name": "Người Thiếc", "kind": "blob", "stage": "c1",
            "vn": "heo con đội mũ sắt đỏ tròn (mặt vẫn lộ) có đinh đồng, chùm lông trắng trên mũ, cầm chùy gỗ",
            "who": ("a chibi PIGLET KNIGHT: a round little boar piglet (rusty brown fur #A8643A, cream snout #F0D8B8, two "
                    "tiny tusks, teal eyes #2FB3B3) wearing a big round red iron helmet (#C8352E) with brass rivets "
                    "(#C8873A) and a white plume (#F4F4F4) on top; the helmet's visor is raised so the whole face (eyes, "
                    "snout, tusks) is clearly visible; small red iron shoulder pads; it holds a short wooden club "
                    "(#9A6A3E) in its near hand; short legs with dark hooves; a curly tail.")},
        2: {"name": "Thiết Phủ", "kind": "axe", "stage": "f2",
            "vn": "heo rừng chiến binh đứng hai chân, giáp đỏ đinh đồng, nanh ngà dài, bờm trắng dựng, mũ đỏ có gai, rìu kích "
                  "cán đồng",
            "who": ("the same boar as a fully grown iron boar warrior standing upright: big, muscular and heavy; rusty brown "
                    "fur (#A8643A); long curved ivory tusks (#F1E6D0); a white mane (#F4F4F4) bristling from the head down "
                    "the back; heavy red iron armour (#B9302A) with brass rivets (#C8873A) on the chest, shoulders and "
                    "forearms; an open-faced red helmet with a short horn spike; teal eyes (#2FB3B3); in the near hand a big "
                    "halberd-axe: a long bronze shaft (#C8873A), a broad crescent axe blade of grey steel (#9AA6B2) and a "
                    "spear tip on top.")}}},
    "tam_kiem": {"order": 50, "gốc": "1223→1224→1225: kiếm sĩ giáp trắng mào chữ V lam, chùm tóc trắng, áo choàng đỏ → song "
                                     "kiếm → vua ba kiếm vàng", "forms": {
        1: {"name": "Kiếm Sĩ Nhí", "kind": "sword", "stage": "c1",
            "vn": "linh miêu trắng con đứng hai chân, túm lông tai dài, mũ mào V lam, khăn đỏ, kiếm gỗ",
            "who": ("a chibi WHITE LYNX swordsman cub standing upright: white fur (#F4F4F2) with soft grey stripes "
                    "(#B9BEC4), long white ear tufts swept back like plumes; ice-blue eyes (#4FB3E0); a sky-blue cap-helmet "
                    "(#3F7FD0) with a V-shaped crest trimmed in gold (#D9A441); a short red scarf (#C8352E); a wooden "
                    "practice sword (#9A6A3E) in its near hand; a short tail.")},
        2: {"name": "Song Kiếm", "kind": "sword", "stage": "m2",
            "vn": "linh miêu kiếm khách trẻ thon nhanh, giáp ngực trắng viền vàng, mũ mào V lam, áo choàng đỏ, kiếm lam và "
                  "kiếm đỏ",
            "who": ("the same lynx as a lean, agile young twin-blade swordsman: white and grey-striped fur, long white ear "
                    "tufts, ice-blue eyes; white chest armour (#F2F2F0) with gold trims (#D9A441) and a sky-blue V-crested "
                    "helmet (#3F7FD0); a red cape (#C8352E); two swords with gold guards: a sapphire-blue blade (#3F7FD0) "
                    "in the near hand and a ruby-red blade (#C8352E) in the far hand.")},
        3: {"name": "Tam Kiếm Vương", "kind": "sword", "stage": "f3",
            "vn": "vua ba kiếm: giáp trắng vàng chạm mây, mào V vàng như vương miện, áo choàng đỏ lót lam, kiếm lam và đỏ trong "
                  "tay, kiếm vàng lớn đeo sau lưng",
            "who": ("the same lynx as the three-sword king: tall, regal and powerful; white and silver fur with grey "
                    "stripes, long ear tufts, ice-blue eyes with a commanding gaze; ornate white-and-gold armour engraved "
                    "with cloud scrolls (#F2F2F0, #D9A441); a golden V crest like a crown on its helmet; a long red cape "
                    "(#C8352E) lined with blue (#2E4A8C); a sapphire-blue sword (#3F7FD0) in the near hand and a ruby-red "
                    "sword (#C8352E) in the far hand, both with golden winged guards; a third, great golden sword sheathed "
                    "on its back, the hilt rising above the shoulder.")}}},
    "ung_thep": {"order": 60, "gốc": "1696→1697: ưng máy bạc cam, cánh lông pha lê bạc hà, đuôi tím, móng vàng", "forms": {
        1: {"name": "Ưng Thép Con", "kind": "bird", "stage": "c1",
            "vn": "ưng con tròn lông bạc, mũ mặt cam, mỏ vàng, cánh nhỏ lông pha lê bạc hà, đuôi tím ba lông",
            "who": ("a chibi STEEL HAWK chick: a round body of silver-grey feathers (#C9CED4) with an orange crest and face "
                    "mask (#E8862E) like a helmet; a short hooked gold beak (#E0B23A); sharp cyan eyes (#3FB6D8); small "
                    "wings whose flight feathers are flat mint crystal blades (#9FE3C8) with a few darker facet lines; a "
                    "dark purple tail (#4A3A6E) of three short feathers; short orange legs with gold talons.")},
        2: {"name": "Ưng Thép", "kind": "flyer", "stage": "f2",
            "vn": "ưng thép lớn đang bay, giáp bạc cam, mũ đầu cam có mào, cánh sáu lông pha lê bạc hà dài như lưỡi dao, đuôi "
                  "tím chẻ ba dài, móng vàng",
            "who": ("the same hawk as a fully grown steel war hawk, flying: sleek, powerful and sharp; silver armour feathers "
                    "(#C9CED4) with orange plates (#E8862E) on the head, chest and shoulders; a crested orange helmet-like "
                    "head with a hooked golden beak and narrowed cyan eyes; huge wings whose long flight feathers are six "
                    "flat mint crystal blades on each wing (#9FE3C8, darker facet lines), spread wide; a long dark purple "
                    "tail (#4A3A6E) split into three long streamers; strong orange legs with golden talons held forward, "
                    "ready to strike.")}}},
    "kim_nghe": {"order": 70, "flames": True,
                 "gốc": "1840→1841: thú con giáp vàng trắng mũ có ngọc lam, đuôi cáo → thần thú thon giáp vàng bạc, lửa lam",
                 "forms": {
        1: {"name": "Nghê Con", "kind": "quad", "stage": "c1",
            "vn": "nghê con bốn chân lông trắng bạc, mũ vàng có ngọc lam và hai vây sừng bạc, đuôi bông lửa lam, giáp ngực vàng",
            "who": ("a chibi NGHE pup (a mythical guardian beast with a fox-like body): white-silver fur (#F2F2F0) with a "
                    "cream belly; a big fluffy fox-like tail shaped like sapphire-blue flames (outer #2F5FB0, inner "
                    "#8FC3F0); a golden helmet (#E0B23A) with a big round sapphire gem (#2F6FC0) on the forehead and two "
                    "small silver horn fins; a golden chest plate with a round blue gem; big deep-blue eyes; short legs "
                    "with silver paws.")},
        2: {"name": "Kim Nghê", "kind": "quad_big", "stage": "f2",
            "vn": "thần thú nghê thân dài thon như cáo-sư tử, lông trắng bạc, giáp vàng chạm mây gắn ngọc lam, hai sừng bạc "
                  "vuốt ngược, bờm, túm khuỷu và chóp đuôi là lửa lam",
            "who": ("the same nghe as the fully grown legendary guardian beast: a long, sleek and powerful fox-lion body "
                    "with white-silver fur (#F2F2F0); ornate golden armour (#E0B23A) engraved with cloud scrolls on the "
                    "head, chest, shoulders and legs, set with sapphire gems (#2F6FC0); two long swept-back silver horns "
                    "(#C9D3DC); a flowing mane, tufts at the elbows and a long tail tip made of sapphire-blue flames (outer "
                    "#2F5FB0, middle #3F8FE0, inner #A8D8F8); deep-blue eyes with a fierce, noble gaze.")}}},
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
    f = ln["forms"][k]
    c, out_dir, save_dir, save = paths(hid, k)
    refs = refs_of(hid, k)
    if any(p is None for p, _, _ in refs):
        return None
    grown = f["stage"] != "c1"
    prop = " or body proportions (this creature has its own proportions, given below)" if grown else ""
    keep = ln.get("keep", "keep the same species, face, colours, markings and drawing style so the line clearly grows up")
    lines_img = []
    for p, d, role in refs:
        if role == "pose":
            lines_img.append((p, f"another hero of the same game ({d}), drawn exactly the way we need, 1536x1024, white "
                                 f"background: copy its framing, its pose logic (three-quarter side view facing right, limbs "
                                 f"separated by white gaps), its hand-drawn pen line and its flat crayon colouring. Do NOT copy "
                                 f"its species, design, colours{prop}"))
        elif role == "style":
            lines_img.append((p, f"another approved hero of the same game ({d}), 1536x1024, white background: match EXACTLY "
                                 f"its hand-drawn pen line, crayon texture, flat colouring, simple readable shapes and "
                                 f"determined expression. Do NOT copy its species, design, colours{prop}"))
        else:
            lines_img.append((p, f"FORM {role} of this same creature (approved), 1536x1024, white background: {keep}; the "
                                 f"new form is bigger, stronger and cooler than this one"))
    lines_img.append((WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen "
                                   "outline + coloured pencil / wax crayon hatching), nothing of its content"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(lines_img))
    boss = ""
    if ln["order"] >= 70:
        boss = ("\nThis line is the island's FINAL boss: the most splendid and refined design of the whole island (elegant "
                "shapes, rich but readable golden ornament), more so for later forms.")
    elif ln["order"] >= 30:
        boss = ("\nThis line belongs to one of the island's bosses: make the design especially beautiful and refined (elegant "
                "shapes, rich but readable ornament), more so for later forms.")
    extra = ("\n\n" + FLAMES) if ln.get("flames") else ""
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the hand-drawn style of images 1 and 2.

CREATURE: {SPIRIT}
{STAGE[f['stage']]}
{f['who']}{boss}

{METAL}{extra}

CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature is visible (weapons, wings, tail and horns included), nothing cut by the edges, at least 60 px of white margin all round. It is centred, about 720 px tall from its highest point to its lowest point; its lowest point is about 120 px above the bottom edge.

POSE (very important: the picture will be animated as ONE single drawing with a simple 2D skeleton, so body parts must be readable and must not overlap):
- Side three-quarter view turned toward the viewer's RIGHT; the head is at the right, the eyes look to the viewer's right.
{POSES[f['kind']]}
- Nothing covers the face. Ears, horns, crests, wings, weapons and tail do not cross each other.

{line(7).replace("of the style image, NOT the glossy look of the design image", "of images 1 and 2")}

Keep the design clean and readable: no text, no background, no extra props, no effects around the creature.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


KIND_VN = {"scorp": "bọ cạp thân thấp, đuôi cong trên lưng", "quad": "bốn chân", "quad_big": "bốn chân, thân dài",
           "hooves": "bốn chân móng guốc", "mantis": "bọ ngựa đứng hai chân sau, liềm giơ thủ thế",
           "blob": "tròn, tay chân ngắn", "bird": "chim đứng hai chân, cánh dang", "flyer": "bay, cánh xoè sau vai",
           "lancer": "đứng hai chân, hai thương", "guard": "đứng hai chân, khiên bên phải, giáo sau",
           "axe": "đứng hai chân, rìu kích dựng bên phải", "sword": "đứng hai chân, kiếm"}
STAGE_VN = {"c1": "chibi (đầu ~45%)", "m2": "hết chibi (đầu ~30%)", "f2": "dạng cuối, không chibi (đầu ~25%)",
            "f3": "dạng cuối, không chibi (đầu ~25%)", "solo": "chỉ một dạng, trưởng thành (đầu ~28%)"}


def huong_dan(hid):
    ln = LINES[hid]
    out = [f"# {hid}: tướng .atomik đảo Kim (rig từ một ảnh liền)", "",
           f"Đảo Kim, ải {ln['order']}. Gốc aola: {ln['gốc']}. Thú mặc giáp (không dạng người), chỉ dạng 1 chibi, càng tiến "
           f"hóa càng dữ, ngầu, đẹp. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người dùng muốn tự gửi thì "
           f"chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).", ""]
    for k, f in ln["forms"].items():
        c, out_dir, save_dir, save = paths(hid, k)
        prompt = W(out_dir, "luot_1_lien.txt")
        out += [f"## Dạng {k}: {f['name']} ({KIND_VN[f['kind']]}; {STAGE_VN[f['stage']]})", f"- Thiết kế: {f['vn']}."]
        if os.path.isfile(prompt) and all(p for p, _, _ in refs_of(hid, k)):
            out.append(f"- File prompt: `{prompt}`.")
        else:
            out.append(f"- File prompt: chưa dựng, chờ ảnh dạng {k - 1} được duyệt (chạy lại `build_kim.py {hid}`).")
        pose, second = POSE_REF[f["kind"]]
        out.append("- Ảnh mẫu theo thứ tự:")
        out.append(f"  1. `{picked(pose)}`: {REFS[pose][1]}; 1536x1024, nền trắng; lấy khung, dáng, nét.")
        out.append(f"  2. `{picked(second)}`: {REFS[second][1]}; 1536x1024, nền trắng; lấy nét, tô.")
        n = 3
        for j in range(1, k):
            out.append(f"  {n}. ảnh dạng {j} đã duyệt của dòng này (`{W(INBOX, code(hid, j))}`, L1_duyet.png hoặc "
                       f"tai_ve/L1_lien.png); 1536x1024, nền trắng; giữ loài, mặt, dấu hiệu.")
            n += 1
        out.append(f"  {n}. `{WORLD_STYLE}`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.")
        out += [f"- Lưu: `{save}` (trùng tên thì `L1_lien_2.png`, `_3`...).", ""]
    out += ["## Kiểm",
            "- Thú, không mặt người; mặt quả quyết, mắt nhìn sang phải; nhìn nghiêng 3/4 sang phải.",
            "- Dạng 1 chibi; dạng sau đầu nhỏ hẳn, dáng chiến, ngầu hơn dạng trước rõ rệt.",
            "- Tô phẳng: giáp, kim loại, pha lê mỗi mảng một màu, không đốm sáng, không phản chiếu, không phát sáng.",
            "- Chân tách nhau có khe trắng, tay và vũ khí tách thân, đuôi không vắt qua thân, cánh không đè đầu.",
            "- Khung 1536x1024, con cao khoảng 720 px, chừa lề trắng; không đường đất, không bóng dưới chân.", "",
            "## Câu sửa nhanh (gửi kèm `--note`)",
            "- \"Flat colour only: no shine spots, no metallic gradients, no reflections, no glow on the armour.\"",
            "- \"Not chibi: make the head much smaller (about a quarter of its height), longer limbs, a fiercer face.\"",
            "- \"Keep white gaps between the legs and between each arm, weapon and the body; the tail must not cross the body.\"",
            "- \"More determined face: lowered brows, firm mouth, not a happy grin.\""]
    p = W(HERE, "gui_gpt", code(hid, 1), "HUONG_DAN.md")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return p


def huong_dan_dao():
    out = ["# Đảo Kim: 10 dòng tướng .atomik (gen một ảnh liền, rig một lưới)", "",
           "Sinh bằng `py -3 -I ArtGen/Spine/build_kim.py [id ...]`. Mỗi dòng có `gui_gpt/<id>_1/HUONG_DAN.md` (gốc aola, ảnh "
           "mẫu, chỗ lưu, cách kiểm). Dạng 2, 3 chỉ dựng khi ảnh dạng trước đã có.", "",
           "| Ải | Dòng | Dạng | File prompt |", "|---|---|---|---|"]
    for hid, ln in LINES.items():
        for k, f in ln["forms"].items():
            p = W(HERE, "gui_gpt", code(hid, k), "luot_1_lien.txt")
            built = os.path.isfile(p) and all(x for x, _, _ in refs_of(hid, k))
            out.append(f"| {ln['order']} | `{hid}` | {k}. {f['name']} | {('`' + p + '`') if built else 'chờ dạng trước'} |")
    p = W(HERE, "gui_gpt", "HUONG_DAN_kim.md")
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
