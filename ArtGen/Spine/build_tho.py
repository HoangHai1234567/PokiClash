# -*- coding: utf-8 -*-
"""Gói prompt Codex cho 10 dòng tướng đảo Thổ vẽ lại thành tướng .atomik (2026-11-10, máy ổ C).

Khuôn như build_kim.py (QUY_TRINH mục 20): Claude tự thiết kế, gen trọn con LIỀN một ảnh, rig một lưới bằng beast.py. Học từ
thiết kế dòng aola gốc (goc_<id>_portrait.png); CHỈ dạng 1 chibi, dạng sau hết chibi, càng tiến hóa càng dữ, chiến, ngầu, đẹp.
Gốc dạng golem, người (Thạch Nhân, Phù Văn, Hạt Dẻ, Cự Phủ, Giáp Nham) đổi thành thú, giữ màu chủ, vũ khí, mô-típ của gốc:
vượn đá, tê giác đá phù văn, sóc hiệp sĩ hạt dẻ, gấu rìu, tê tê giáp vàng (Claude chốt, người dùng giao "làm nốt" 2026-11-10).

Mỗi dạng: gui_gpt/<id>_<k>/luot_1_lien.txt -> inbox/<id>_<k>/tai_ve/L1_lien.png. Dạng k > 1 đính ảnh các dạng trước
(L1_duyet.png nếu có, không thì L1_lien.png); dạng chưa có ảnh dạng trước thì chưa dựng.

    py -3 -I ArtGen/Spine/build_tho.py [id ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, line  # noqa: E402
from build_kim import POSES as _KIM_POSES, REFS as _KIM_REFS, STAGE, _UP  # noqa: E402

INBOX = W(HERE, "inbox")

# ảnh liền đã vào game dùng làm mẫu nét, khung, dáng: mã -> (mô tả tiếng Anh, mô tả tiếng Việt cho HUONG_DAN)
REFS = dict(_KIM_REFS)
REFS.update({
    "thiet_phu_2": ("an armoured boar warrior standing upright on its two legs holding a long-hafted axe",
                    "heo rừng giáp đỏ đứng hai chân cầm rìu kích (đảo Kim)"),
    "khien_bac_2": ("an armoured armadillo guard standing upright with a shield and a trident",
                    "tatu vệ sĩ đứng hai chân, khiên và đinh ba (đảo Kim)"),
})

# kiểu dáng -> (ảnh mẫu dáng, ảnh mẫu nét thứ hai)
POSE_REF = {"quad": ("de_hoa_1", "moc_tinh_2"), "quad_big": ("moc_tinh_2", "de_hoa_1"), "blob": ("canh_cut_1", "de_hoa_1"),
            "turtle": ("giap_long_2", "de_hoa_1"), "brawler": ("nguu_quyen_3", "de_hoa_1"),
            "axe": ("thiet_phu_2", "de_hoa_1"), "guard": ("khien_bac_2", "de_hoa_1")}

POSES = {k: _KIM_POSES[k] for k in ("quad", "quad_big", "blob", "axe", "guard")}
POSES["turtle"] = ("- Stands low on its FOUR short legs, all feet flat on one level ground line (no ground drawn), the neck "
                   "and head stretched forward on the viewer's right, a grounded ready-to-fight stance.\n- All four legs "
                   "are visible under the shell with white gaps between the front pair and the back pair.\n- The whole "
                   "shell is visible on top of the body; anything growing on the shell stays above it, clear of the head.\n"
                   "- The tail points back on the viewer's LEFT, clear of the back legs.")
POSES["brawler"] = (_UP + "- Both arms are held a little away from the body in a fighter's guard, hands clenched into fists "
                    "(or claws) with white space between each arm and the body: the near fist forward at chest height on "
                    "the viewer's right, the far fist raised behind it; the fists never cover the face.\n- A tail (if any) "
                    "sweeps back and down on the viewer's LEFT, clear of the legs; a cape (if any) hangs behind on the "
                    "viewer's LEFT and stops above the knees.")

SPIRIT = ("a MYTHICAL EARTH BEAST of the earth element: an ANIMAL creature (not a human: no human face, no human body; it may "
          "wear the armour and hold the weapons listed), designed like a creature of a monster-collecting game: appealing, "
          "simple readable shapes. Its face is DETERMINED and ready to fight: lowered brows, confident focused eyes looking to "
          "the viewer's right, mouth set firm or slightly open; never a happy mascot grin, never scary.")

EARTH = ("STONE, CRYSTAL, ARMOUR AND MOSS: every stone plate, rock, crystal, armour piece, weapon and gem is a flat shape with "
         "a closed dark-brown ink outline, filled with ONE flat crayon colour (trims are a second flat colour drawn as a "
         "separate band); rock cracks and carved runes are thin darker lines drawn on the flat colour; no shine spots, no "
         "white highlights, no reflections, no metallic gradients, no sparkle; crystals and gems are flat colour with a few "
         "darker facet lines, and nothing glows (rune lines are flat carved colour, never glowing). Moss and leaves are flat "
         "green shapes. The armour and rocks follow the animal's body so the animal stays readable: its face, ears, paws or "
         "claws and tail are clearly visible.")

# id -> ải, mỗi dạng: tên (theo 13_DanhSachTuong), kiểu dáng, giai đoạn, thiết kế tiếng Việt, mô tả tiếng Anh;
# "keep" (tuỳ chọn): câu tiếng Anh thay câu giữ màu khi đính ảnh dạng trước
LINES = {
    "thach_nhan": {"order": 1, "gốc": "34→35→36: đá rêu tròn mắt cam, chỏm cỏ → người đá khối vuông, hoa văn xoắn lục, rêu "
                                      "vai → người đá cổ cột đá sau vai, rêu dây leo (đổi thành vượn đá)",
                   "keep": ("keep the same species, ape face, orange eyes, mossy stone body and green spiral glyphs so the "
                            "line clearly grows up"),
                   "forms": {
        1: {"name": "Thạch Nhân", "kind": "blob", "stage": "c1",
            "vn": "vượn đá con tròn như hòn đá rêu, mắt cam to dưới mày đá, chỏm cỏ trên đầu, nắm đấm đá tròn",
            "who": ("a chibi ROCK APE cub: a round boulder-like body of mossy grey-olive stone (#8C8A62) with darker stone "
                    "cracks (#5E5C40); a big round head merged with the body, an ape face with a flat muzzle and small "
                    "nostrils (not a human face), big round orange eyes (#F07A1E) under heavy stone brows; a tuft of bright "
                    "moss-green grass (#9DBF3A) sprouting on top of the head; small moss patches (#7FA33A) on the shoulders; "
                    "short thick stone arms ending in big round stone fists; short stubby legs.")},
        2: {"name": "Thạch Nhân", "kind": "brawler", "stage": "m2",
            "vn": "vượn đá trẻ thân khối đá vuông, tay dài nắm đấm vuông, rêu và dương xỉ trên vai, hoa văn xoắn lục ở ngực, "
                  "cẳng tay, mày đá, hai nanh nhỏ",
            "who": ("the same rock ape grown into a young STONE GORILLA warrior: a broad blocky body of square stone slabs "
                    "(#7E7C5A, darker cracks #55533A), thick long arms with heavy square stone fists, short sturdy legs; moss "
                    "(#7FA33A) and small fern leaves on the shoulders and back; a carved green spiral glyph (#4F8A3A) on the "
                    "chest and on each forearm; a square stone brow over narrowed orange eyes (#F07A1E), a stone jaw with "
                    "two small tusks.")},
        3: {"name": "Thạch Nhân", "kind": "brawler", "stage": "f3",
            "vn": "khổng lồ vượn đá cổ, hai cột đá dựng sau vai như vương miện đá, rêu và dây leo, hoa văn xoắn lục ở ngực, vai, "
                  "nắm đấm, mắt cam dữ",
            "who": ("the same rock ape as a towering ANCIENT STONE GORILLA TITAN: a massive body of carved square stone "
                    "blocks (#6F6E50, darker cracks #4A4934); huge stone fists with knuckle plates; two tall standing-stone "
                    "pillars rising behind the shoulders like a crown of standing stones; thick moss (#7FA33A) and hanging "
                    "vines with small leaves on the shoulders and pillars; green spiral glyphs (#4F8A3A) carved on the chest, "
                    "shoulders and fists; a heavy stone brow, narrowed fierce orange eyes (#F07A1E), a set jaw with tusks.")}}},
    "lung_vuong": {"order": 5, "gốc": "70→71→72: lửng nâu tròn mày trắng, dây thừng đỏ trắng, pha lê lam trên đầu → lửng võ sĩ "
                                      "vuốt vàng → vua lửng lông trắng, mũ vàng ngọc lam, đuôi lam", "forms": {
        1: {"name": "Lửng Con", "kind": "blob", "stage": "c1",
            "vn": "lửng con nâu tròn, mày và ria trắng xoè, pha lê lam trên đầu, dây thừng đỏ trắng làm thắt lưng, xoắn kem ở "
                  "bụng, đuôi khoang",
            "who": ("a chibi BADGER cub: a round chubby body of warm brown fur (#8A5A3C) with a cream spiral marking on the "
                    "belly (#E8CFA8); a broad white face stripe and big bushy white eyebrows and whiskers flaring out to the "
                    "sides (#F2EEE6); a small blue crystal (#3F8FD8) set on top of the head in a little brown fur crest; a "
                    "thick red-and-white twisted rope (#C8342C / #F2EEE6) worn as a belt; small bright blue eyes; a bushy "
                    "tail banded brown and cream; short legs with small cream claws.")},
        2: {"name": "Lửng Võ Sĩ", "kind": "brawler", "stage": "m2",
            "vn": "lửng võ sĩ đứng hai chân, vuốt vàng cong dài, sừng mào vàng gắn pha lê lam, vòng cổ dây thừng, khăn trắng bay "
                  "sau hông",
            "who": ("the same badger grown into a young BADGER BRAWLER: a lean strong body of brown fur (#8A5A3C) with the "
                    "cream spiral on the belly and the white face stripe; long curved golden claws (#E0B23A) on both hands "
                    "like knuckle blades; a golden horn crest (#E0B23A) with a blue crystal (#3F8FD8) on the forehead and a "
                    "small red feather crest; a brown leather collar wound with the red-and-white rope; a white sash "
                    "(#F2EEE6) streaming back from the waist; red wraps on the ankles; a banded bushy tail.")},
        3: {"name": "Lửng Vương", "kind": "brawler", "stage": "f3",
            "vn": "vua lửng lông trắng vằn lam nhạt, bờm trắng, mũ vua vàng ngọc lam, giáp vai và cổ tay vàng, vuốt vàng, đuôi "
                  "trắng khoang lam đậm",
            "who": ("the same badger as the BADGER KING: thick white fur (#F4F2EC) with pale-blue markings (#9CC8EA) and a "
                    "cream belly, a ruff of white fur around the neck; a golden king helmet (#E0B23A) with a big round "
                    "sapphire gem (#2F6FC0); golden shoulder plates and wrist guards; long golden claws on both hands; a huge "
                    "bushy white tail with deep-blue bands (#2F6FC0); deep-blue fur on the lower legs with golden toe caps; "
                    "fierce narrowed blue eyes.")}}},
    "cao_da": {"order": 10, "gốc": "458→459→460: cáo nâu mặt nạ trắng ngọc lam, găng đá lục gai → cáo võ, dây thừng đỏ trắng → "
                                   "cáo bốn chân găng đá lục gai to, sừng pha lê lam", "forms": {
        1: {"name": "Cáo Con", "kind": "quad", "stage": "c1",
            "vn": "cáo con nâu ngực kem, mũ mặt nạ trắng sọc đỏ ngọc lam, găng đá lục tròn ở chân trước, đuôi bông chóp trắng",
            "who": ("a chibi FOX kit: warm brown fur (#B5703C) with a cream chest and muzzle (#F2E2C8) and white tips on the "
                    "big ears and the big fluffy tail; a white mask-helmet plate (#F2EEE6) on the forehead with a red stripe "
                    "(#C8342C) and a deep-blue gem (#2F5FB0); rounded leaf-green stone shards (#5FA63A) like little gauntlets "
                    "on the front paws; big red-brown eyes.")},
        2: {"name": "Cáo Đá", "kind": "quad", "stage": "m2",
            "vn": "cáo trẻ thon, mũ mặt nạ trắng có mũi pha lê lam chĩa trước, găng đá lục gai ở cả bốn cẳng chân, dây thừng "
                  "đỏ trắng buộc cổ",
            "who": ("the same fox grown into a lean young FOX WARRIOR: brown fur (#B5703C), a cream chest, a long fluffy tail "
                    "with a white tip; a white mask helmet (#F2EEE6) with red stripes and a pointed blue crystal (#3FA0E0) "
                    "jutting forward from the forehead; jade-green stone gauntlets (#4E9A3A, darker #2E6B2A) with short "
                    "spikes on all four lower legs; a red-and-white twisted rope (#C8342C / #F2EEE6) tied around the neck "
                    "with trailing ends; narrowed red eyes.")},
        3: {"name": "Cáo Đá Lục Bảo", "kind": "quad_big", "stage": "f3",
            "vn": "cáo đá lục bảo thân dài, găng pha lê lục bảo gai nhọn bốn chân, hàng gai lục bảo trên vai, sừng pha lê lam "
                  "lớn, dây thừng quấn ngực",
            "who": ("the same fox as a fierce EMERALD STONE FOX: a long sleek powerful body with brown fur (#A9622F) and a "
                    "cream chest; a white mask helmet (#F2EEE6) with red stripes and a big pointed sapphire crystal (#2F7FD0) "
                    "on the forehead; massive emerald-green crystal-stone gauntlets (#3E9A4A, darker #276B33) with sharp "
                    "spikes on all four legs and a row of emerald spikes along the shoulders; a thick red-and-white rope "
                    "(#C8342C / #F2EEE6) wound around the chest; a large flowing tail with a white tip; long cream claws.")}}},
    "ho_khoan": {"order": 15, "gốc": "485→486→487: hổ con cam tròn mắt lục → hổ múa lân áo đỏ, tua pháo → hổ vương mũ đồng sừng "
                                     "khoan đỏ, pha lê lục trên lưng", "forms": {
        1: {"name": "Hổ Cát Tường", "kind": "quad", "stage": "c1",
            "vn": "hổ con cam vằn nâu nhạt, mắt lục to, mũ lân nhỏ vải đỏ thẫm mào xoăn ngọc lục, tai to lót hồng",
            "who": ("a chibi LUCKY TIGER cub: round orange fur (#F0A02A) with soft brown stripes and a cream muzzle; big round "
                    "green eyes (#3FB27A); a small festive lion-dance mask cap on its head: dark-red cloth (#9E2A2A) with a "
                    "teal curly crest (#3FB0A0) and a gold trim; big pink-lined ears; a short tail with a dark-red tuft; "
                    "short sturdy legs.")},
        2: {"name": "Hổ Pháo Hoa", "kind": "quad", "stage": "m2",
            "vn": "hổ trẻ thon, mũ trùm lân đỏ viền mây vàng, diềm lông trắng, ngọc đỏ trên đỉnh, hai tua pháo đỏ quả cầu vàng",
            "who": ("the same tiger grown into a young FIRECRACKER TIGER: lean orange fur (#E8862A) with dark-brown stripes "
                    "and a cream belly; a lion-dance hood over the head and shoulders: red cloth (#C8342C) with golden curly "
                    "cloud trims (#E0B23A), a white fur fringe along its edge and a small round red gem on top in a gold "
                    "mount; two red firecracker tassels with gold pom-poms hanging from the hood; a long striped tail; "
                    "narrowed determined green eyes.")},
        3: {"name": "Hổ Khoan Vương", "kind": "quad_big", "stage": "f3",
            "vn": "hổ vương thân dài, mũ đồng có sừng khoan xoắn pha lê đỏ, cụm pha lê lục bảo lởm chởm trên lưng, vai, hông, "
                  "giáp ngực đồng ngọc đỏ",
            "who": ("the same tiger as the DRILL-HORN TIGER KING: a long powerful striped body (orange-tan #D58A3A, dark-brown "
                    "stripes) with a cream chest; a bronze helmet (#9A5A32) over the head with a long spiralled ruby-red "
                    "crystal drill horn (#C8344A) pointing forward and up from the forehead; clusters of jagged emerald-green "
                    "crystals (#4FA84A, darker #2E7A35) rising along the back and on the shoulders and haunches; a bronze "
                    "chest plate with a red gem; teal-blue eyes (#3FA8B0); a long striped tail.")}}},
    "phu_van": {"order": 20, "gốc": "718→719→720: lính đá xám lam sừng vàng mắt vàng → người đá tím vân lam, sừng vàng → khổng "
                                    "lồ đá ngọc vân lục lam (đổi thành tê giác đá phù văn)",
                "keep": ("keep the same species, golden horns, stone plates and carved rune-line markings so the line clearly "
                         "grows up; the STONE COLOUR changes as described for this form"),
                "forms": {
        1: {"name": "Lính Đá Con", "kind": "quad", "stage": "c1",
            "vn": "tê giác đá con tròn, phiến đá xám lam khắc vạch phù văn lam, hai sừng vàng cong, mắt hổ phách to",
            "who": ("a chibi STONE RHINO calf: a round body of blue-grey stone plates (#8FA6AE, darker cracks #5E737B) with "
                    "thin cyan rune lines carved into them (#3FC6D8); two curved golden horns (#E0B23A), one on the nose and "
                    "a smaller one above it; big round amber eyes (#F2B233); short thick stone legs with rock-chunk feet; a "
                    "stubby tail.")},
        2: {"name": "Lính Đá Phù Văn", "kind": "quad_big", "stage": "m2",
            "vn": "tê giác đá phù văn trẻ, phiến đá tím xám khắc chữ vuông lam, sừng mũi vàng lớn và hai sừng mày cong, khối "
                  "vai đá vuông",
            "who": ("the same rhino grown into a strong young RUNE-STONE RHINO: a heavy body of violet-grey stone slabs "
                    "(#7C7290, darker cracks #50496A) carved with straight cyan rune lines and square glyphs (#3FC6D8); a big "
                    "curved golden horn on the nose and two smaller golden horns curling up from the brow (#E0B23A); a golden "
                    "rim along the jaw; massive square stone shoulder blocks; thick stone legs with blocky feet; narrowed "
                    "amber eyes.")},
        3: {"name": "Cự Thần Phù Văn", "kind": "quad_big", "stage": "f3",
            "vn": "tê giác khổng lồ đá ngọc xám khắc đai phù văn lục lam, sừng mũi vàng to, vương miện sừng vàng, vòng vàng trên "
                  "trán, giáp vai đá vuông",
            "who": ("the same rhino as a colossal RUNE TITAN RHINO: an immense body of jade-grey stone blocks (#7FA39A, darker "
                    "cracks #4E6D66) carved all over with bands of teal rune glyphs (#2FA8A8); a huge curved golden nose horn "
                    "and a crown of golden horns curving up from the brow (#E0B23A), a golden ring set on the forehead; giant "
                    "square stone shoulder pauldrons with rune bands; pillar-like stone legs; a short heavy stone tail; fierce "
                    "narrowed amber eyes.")}}},
    "hat_de": {"order": 30, "gốc": "927→928: lính tí hon tóc lam, mũ hạt dẻ kính lam, khiên hạt dẻ (đổi thành sóc hiệp sĩ)",
               "forms": {
        1: {"name": "Lính Hạt Dẻ", "kind": "blob", "stage": "c1",
            "vn": "sóc con nâu hạt dẻ đuôi bông cuộn, chỏm lông lam, mũ nón hạt dẻ dải kính lam, khiên vỏ hạt dẻ tròn và chùy "
                  "hạt dẻ",
            "who": ("a chibi SQUIRREL soldier: warm chestnut-brown fur (#9C5A2E) with a cream belly and a huge fluffy curled "
                    "tail; a spiky sky-blue tuft of fur on the head (#5FC8E0); a round acorn-cap helmet (#7A4A26, with a "
                    "crosshatched pattern and a little stalk on top) with a blue visor band (#3F8FD8) above the eyes; it "
                    "carries a round acorn-shell shield (#B8813F) on one arm and a little acorn-headed mace in the other "
                    "hand; short legs with small brown boots; big blue eyes.")},
        2: {"name": "Dũng Sĩ Hạt Dẻ", "kind": "guard", "stage": "f2",
            "vn": "sóc hiệp sĩ đứng hai chân, mào lông lam vuốt ngược, mũ hạt dẻ, giáp vỏ hạt dẻ vàng kem ngọc đỏ, khiên cao như "
                  "nửa vỏ hạt dẻ, giáo mũi hạt dẻ vàng",
            "who": ("the same squirrel as a brave CHESTNUT KNIGHT: a lean strong body with chestnut-brown fur (#9C5A2E) and a "
                    "cream belly; a big fluffy tail curling up behind the back on the viewer's left; a spiky sky-blue crest "
                    "of fur (#5FC8E0) sweeping back from an acorn helmet (#7A4A26) whose blue visor band (#3F8FD8) is pushed "
                    "up above the eyes; cream-gold acorn-shell armour (#D8B26A) on the chest and shoulders with a small red "
                    "gem; a tall shield shaped like half an acorn shell (#B8813F, its cap band #7A4A26); a spear with a "
                    "sharp acorn-shaped golden head (#E0B23A).")}}},
    "rua_nui": {"order": 40, "gốc": "1203→1204: rùa mầm lục nhạt, mai đất rêu → rùa núi mai là ngọn núi có cây, vuốt pha lê "
                                    "lam", "forms": {
        1: {"name": "Rùa Mầm Đá", "kind": "turtle", "stage": "c1",
            "vn": "rùa con xanh bạc hà, mầm hai lá trên đầu kèm viên sỏi lam, mai như cục đất nâu phủ rêu, má hồng",
            "who": ("a chibi SPROUT TURTLE: a round mint-green head and body (#9ED89A) with a few darker green spots, big "
                    "round dark eyes, pink cheeks; a two-leaf sprout (#7CC83A) growing from the top of the head next to a "
                    "small round blue-grey pebble (#8FB4C0); a domed shell like a clump of brown earth (#8A5A34) topped with "
                    "a layer of moss (#6FB33A) and a little blue pebble; short stubby legs with pale claws.")},
        2: {"name": "Rùa Núi", "kind": "turtle", "stage": "f2",
            "vn": "rùa núi to, cổ khỏe, mày xương vàng nâu có mào, mai là ngọn núi vách đá nâu, đỉnh xám tuyết trắng, gờ cỏ và "
                  "vài cây tròn, vuốt pha lê lam băng",
            "who": ("the same turtle as a huge MOUNTAIN TURTLE: a long strong neck and head with mint-green skin (#8FCFA0) "
                    "and a hard tan bony brow plate with crests (#D2A35A); the shell is a small mountain: layered brown rock "
                    "cliffs (#8A5A34, darker #5E3C22) rising to a pale grey rocky peak with a white snow cap, green grassy "
                    "ledges (#6FB33A) and two or three small flat round trees (#5FA63A) on top; thick legs with ice-blue "
                    "crystal claws (#7FD0E8); a short tail ending in a small ice-blue crystal fin; fierce narrowed blue "
                    "eyes.")}}},
    "ho_kim_cuong": {"order": 50, "gốc": "1380: siêu tiến hóa của 487, hổ giáp vàng sừng khoan đỏ, quạt lưỡi pha lê tím trắng "
                                         "sau vai, vuốt vàng", "forms": {
        1: {"name": "Hổ Kim Cương", "kind": "quad_big", "stage": "solo",
            "vn": "hổ vương lông vàng nâu vằn sẫm, giáp vàng gắn ngọc lục, sừng khoan pha lê đỏ, hai quạt lưỡi kim cương tím "
                  "nhạt xoè sau vai, gai pha lê lục trên lưng, vuốt vàng",
            "who": ("the DIAMOND TIGER KING (the super-evolved drill-horn tiger): a long powerful tiger body with golden-tan "
                    "fur (#D9A04A), dark-brown stripes and a cream chest; golden armour (#E0B23A) on the head, shoulders, "
                    "chest and legs with emerald-green gem settings (#3FA85A); a long spiralled ruby-red crystal drill horn "
                    "(#C8344A) on the forehead; two wing-like fans of long pale-violet diamond crystal blades (#B8B0E8, "
                    "darker facet lines #7E74C0) spreading up and back from the shoulders, clear of the head; short emerald "
                    "crystal spikes along the back; golden claws; a long striped tail; fierce teal eyes (#3FA8B0).")}}},
    "cu_phu": {"order": 60, "gốc": "1209→1210: con thú tròn đội mũ đá pha lê vàng cát, ngọc lam, chỏm lửa → chiến binh giáp vàng "
                                   "cát, rìu tím khổng lồ (đổi thành gấu)", "forms": {
        1: {"name": "Phủ Con", "kind": "blob", "stage": "c1",
            "vn": "gấu con lông kem, mũ đá pha lê vàng cát trùm đầu vai, ngọc lam trên trán, chỏm pha lê đỏ cam, nắm đấm và ủng "
                  "đá vàng",
            "who": ("a chibi BEAR cub: a round body of cream-tan fur (#E8CFA0); a big helmet of chunky golden-sand crystal "
                    "rocks (#D8B05A, darker facets #A47A34) over the head and shoulders with a teal gem (#3FB8C0) on the "
                    "forehead and a small red-orange crystal plume (#E0582A) on top; small round ears poking out; big green "
                    "eyes (#3FB27A); stubby arms ending in golden crystal-rock fists; short legs with golden crystal boots "
                    "banded in teal.")},
        2: {"name": "Cự Phủ", "kind": "axe", "stage": "f2",
            "vn": "gấu chiến binh đứng hai chân, giáp pha lê vàng cát góc cạnh gắn ngọc lam, mào pha lê đỏ cam vuốt ngược, rìu "
                  "hai lưỡi thép tím cán vàng dài",
            "who": ("the same bear as a mighty AXE WARRIOR BEAR: a strong body with tan fur (#D9B07A); angular golden-sand "
                    "crystal armour (#D8B05A, darker facets #A47A34) on the head, chest, shoulders and legs, set with teal "
                    "gems (#3FB8C0); a crest of red-orange crystal plumes (#E0582A) sweeping back from the helmet; a huge "
                    "double-bladed battle axe with violet-steel blades (#8A6FC8, darker #5E4A9A) on a long golden haft "
                    "(#E0B23A); green eyes (#3FB27A), narrowed and fierce.")}}},
    "giap_nham": {"order": 70, "gốc": "1273→1274 (BOSS): chiến binh giáp vàng góc cạnh, kính mắt lục, áo choàng đỏ (đổi thành tê "
                                      "tê giáp vàng)", "forms": {
        1: {"name": "Đấu Sĩ Nham", "kind": "brawler", "stage": "c1",
            "vn": "tê tê con đứng hai chân, vảy vàng góc cạnh như giáp, mặt bụng kem, mắt lục sáng, áo choàng đỏ ngắn, găng "
                  "trắng, đuôi vảy cuộn",
            "who": ("a chibi PANGOLIN fighter standing upright: a round body covered in big angular golden scale plates "
                    "(#E8B53A, darker edges #B9832A) like armour, a cream-tan face and belly (#E8D2A8); bright green eyes "
                    "(#4FD06A) under a golden scale brow; a short red cape (#B8282E) on the shoulders; small fists in white "
                    "gloves; a thick tail of golden scales curling behind on the viewer's left; short legs.")},
        2: {"name": "Giáp Nham", "kind": "brawler", "stage": "f2",
            "vn": "chiến thần tê tê đứng hai chân, giáp vảy vàng góc cạnh, giáp vai nhọn vuốt lên như lưỡi, mũ mào lưỡi gắn ngọc "
                  "lục, viền lục chanh, áo choàng đỏ thẫm, găng trắng đốt vàng, đuôi vảy dài",
            "who": ("the same pangolin as the GOLDEN ARMOURED WAR GOD: a tall powerful upright body clad in sharp angular "
                    "golden scale armour (#E8B53A, darker edges #B9832A) with layered pointed pauldrons sweeping up like "
                    "crown blades; a crested golden helmet with swept-back blades and a green gem; vivid green eyes "
                    "(#4FD06A); thin lime-green trims along the armour edges (#7FE05A); a long crimson cape (#B8282E, lining "
                    "#7E1A22) from the shoulders, stopping above the knees; white-gloved fists with golden knuckle plates; a "
                    "long heavy tail of overlapping golden scales sweeping back on the viewer's LEFT.")}}},
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
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the hand-drawn style of images 1 and 2.

CREATURE: {SPIRIT}
{STAGE[f['stage']]}
{f['who']}{boss}

{EARTH}

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
           "axe": "đứng hai chân, rìu dựng bên phải", "turtle": "rùa bốn chân thấp, mai trên lưng",
           "brawler": "đứng hai chân, thế quyền, nắm đấm tách thân"}
STAGE_VN = {"c1": "chibi (đầu ~45%)", "m2": "hết chibi (đầu ~30%)", "f2": "dạng cuối, không chibi (đầu ~25%)",
            "f3": "dạng cuối, không chibi (đầu ~25%)", "solo": "chỉ một dạng, trưởng thành (đầu ~28%)"}


def huong_dan(hid):
    ln = LINES[hid]
    out = [f"# {hid}: tướng .atomik đảo Thổ (rig từ một ảnh liền)", "",
           f"Đảo Thổ, ải {ln['order']}. Gốc aola: {ln['gốc']}. Thú (không dạng người, gốc golem hay người đã đổi thành thú), chỉ dạng 1 chibi, càng tiến "
           f"hóa càng dữ, ngầu, đẹp. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người dùng muốn tự gửi thì "
           f"chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).", ""]
    for k, f in ln["forms"].items():
        c, out_dir, save_dir, save = paths(hid, k)
        prompt = W(out_dir, "luot_1_lien.txt")
        out += [f"## Dạng {k}: {f['name']} ({KIND_VN[f['kind']]}; {STAGE_VN[f['stage']]})", f"- Thiết kế: {f['vn']}."]
        if os.path.isfile(prompt) and all(p for p, _, _ in refs_of(hid, k)):
            out.append(f"- File prompt: `{prompt}`.")
        else:
            out.append(f"- File prompt: chưa dựng, chờ ảnh dạng {k - 1} được duyệt (chạy lại `build_tho.py {hid}`).")
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
            "- Tô phẳng: đá, giáp, pha lê, rêu mỗi mảng một màu, không đốm sáng, không phản chiếu, không phát sáng.",
            "- Chân tách nhau có khe trắng, tay và vũ khí tách thân, đuôi không vắt qua thân, cánh không đè đầu.",
            "- Khung 1536x1024, con cao khoảng 720 px, chừa lề trắng; không đường đất, không bóng dưới chân.", "",
            "## Câu sửa nhanh (gửi kèm `--note`)",
            "- \"Flat colour only: no shine spots, no metallic gradients, no reflections, no glow on the stone, crystals or runes.\"",
            "- \"Not chibi: make the head much smaller (about a quarter of its height), longer limbs, a fiercer face.\"",
            "- \"Keep white gaps between the legs and between each arm, weapon and the body; the tail must not cross the body.\"",
            "- \"More determined face: lowered brows, firm mouth, not a happy grin.\""]
    p = W(HERE, "gui_gpt", code(hid, 1), "HUONG_DAN.md")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return p


def huong_dan_dao():
    out = ["# Đảo Thổ: 10 dòng tướng .atomik (gen một ảnh liền, rig một lưới)", "",
           "Sinh bằng `py -3 -I ArtGen/Spine/build_tho.py [id ...]`. Mỗi dòng có `gui_gpt/<id>_1/HUONG_DAN.md` (gốc aola, ảnh "
           "mẫu, chỗ lưu, cách kiểm). Dạng 2, 3 chỉ dựng khi ảnh dạng trước đã có.", "",
           "| Ải | Dòng | Dạng | File prompt |", "|---|---|---|---|"]
    for hid, ln in LINES.items():
        for k, f in ln["forms"].items():
            p = W(HERE, "gui_gpt", code(hid, k), "luot_1_lien.txt")
            built = os.path.isfile(p) and all(x for x, _, _ in refs_of(hid, k))
            out.append(f"| {ln['order']} | `{hid}` | {k}. {f['name']} | {('`' + p + '`') if built else 'chờ dạng trước'} |")
    p = W(HERE, "gui_gpt", "HUONG_DAN_tho.md")
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
