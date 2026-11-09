# -*- coding: utf-8 -*-
"""Gói prompt Codex cho 9 dòng tướng còn lại của đảo Thủy, vẽ lại thành thú huyền thoại .atomik (2026-11-08).

Người dùng dặn: style cũ (bút mực + chì sáp, tô phẳng như các concept chibi đã duyệt), hướng thú huyền thoại hơi chibi kiểu
Pokémon, dạng sau dữ hơn nhưng không quá dữ, hạn chế dạng người, animation đơn giản kiểu Clash of Critters (hiệu ứng bù vào),
càng gần boss cuối càng đẹp. Gen trọn con LIỀN một ảnh (không tờ mảnh), rig thẳng từ ảnh (beast.py).

Mỗi dạng: gui_gpt/<id>_<k>/luot_1_lien.txt -> inbox/<id>_<k>/tai_ve/L1_lien.png. Dạng k > 1 đính ảnh dạng trước đã duyệt
(L1_duyet.png nếu có, không thì L1_lien.png); dạng chưa có ảnh dạng trước thì chưa dựng.

    py -3 -I ArtGen/Spine/build_beasts.py [id ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, ART, line  # noqa: E402

OLD = W(ART, "Heroes", "inbox")
STYLE_POOL = [("de_hoa_1", "a chubby flower-sheep creature"), ("canh_cut_1", "a chibi penguin"),
              ("ma_ket_1", "a chibi sea-goat"), ("huyen_vu_1", "a chibi turtle")]

CHIBI = {1: ("FORM 1, the young stage: clearly chibi like a monster-collecting game starter: a big head (about 45% of the "
             "creature's height), a compact round body, short sturdy limbs, big expressive eyes. Cute but already brave."),
         2: ("FORM 2, the same creature grown up: still a bit chibi (head about 38% of its height) but bigger, leaner and "
             "more confident, a little fiercer (sharper eyes, small fangs or spikes), clearly the same species, colours and "
             "markings as form 1."),
         3: ("FORM 3, the final stage: powerful and majestic, only slightly chibi (head about 32% of its height), the most "
             "detailed and beautiful design of the line, fierce and proud but still appealing, NOT scary or monstrous; "
             "clearly the same species, colours and markings as forms 1 and 2.")}

SPIRIT = ("a MYTHICAL WATER BEAST of the water element, a creature (not a human, no human body, no clothes except the items "
          "listed), designed like a creature of a monster-collecting game: appealing, simple readable shapes, few details. "
          "Its face is DETERMINED and ready to fight: lowered brows, confident focused eyes looking to the viewer's right, "
          "mouth set firm or slightly open; never a happy mascot grin, never scary.")

# id -> {"order": ải, "forms": {k: {"name", "vn", "who", "pose"}}}; pose = kiểu dáng đứng (xem POSES)
LINES = {
    "tieu_y": {"order": 5, "kind": "quad", "forms": {
        1: {"name": "Tiểu Y", "vn": "cáo nước con: lông xanh ngọc, ngực mõm trắng kem, tai vây, đuôi sóng bạc đầu, dấu đinh ba "
                                     "trên trán, mặt dây vỏ sò",
            "who": ("a small WATER FOX kit: aqua-blue fur (#4FB6D8) with a cream-white chest, muzzle and paw tips (#F4EEDC); "
                    "two large pointed ears whose edges are fins (flat pale aqua #BDEBF0 with a darker blue rim #2F86C0); "
                    "golden eyes (#F0B030); one big fluffy tail shaped like a curling ocean wave with a white foam crest; a "
                    "tiny three-pointed trident mark on the forehead (navy #24447A); a small scallop-shell pendant (cream "
                    "#F3E3BE, coral rim) on a thin cord around the neck.")},
        2: {"name": "Y Trạch", "vn": "cáo nước lớn: hai đuôi sóng, tai vây dài, mào ba gai vây hình đinh ba, dây đỏ san hô",
            "who": ("the same water fox grown into a lean, athletic young fox: deeper ocean-blue back (#2F86C0) and aqua "
                    "flanks (#4FB6D8), cream chest; TWO wave-shaped tails with white foam crests; longer fin-edged ears; a "
                    "trident-shaped crest of three short fin spikes on the forehead; the scallop-shell pendant now on a "
                    "coral-red cord (#D9483B); sharper golden eyes and two small fangs.")}}},
    "canh_cut": {"order": 10, "kind": "biped", "forms": {
        1: {"name": "Cánh Cụt Con", "vn": "chim cánh cụt băng con: lưng xanh lam đá, mào ba lông pha lê, khăn bếp, chảo băng",
            "who": ("a chibi FROST PENGUIN chick, an apprentice ice cook: slate-teal back and head (#3D7C94), white belly "
                    "(#F7F7F2), a crest of three ice-crystal feathers on the head (pale ice blue #BFE6F2 with blue rim), "
                    "orange beak and feet (#F08A3C), a little white cook's neckerchief with a tiny blue fish pattern. It "
                    "holds a small frying pan made of clear blue ice (#9BD8EE, frosty white rim) in the flipper on the "
                    "viewer's RIGHT, held out to the side at belly height, the whole pan clear of the body.")},
        2: {"name": "Đầu Bếp Cánh Cụt", "vn": "bếp trưởng cánh cụt băng: mũ bếp tuyết, tạp dề xanh băng, dao phay băng",
            "who": ("the same frost penguin grown into a sturdy head chef: deep teal back (#2F6478), white belly, a bigger "
                    "ice-crystal crest, a tall cook's hat made of packed snow with an ice-crystal band, a frosty blue apron "
                    "(#7FC4E0) with a fish-bone pattern, orange beak and feet. It holds a big cleaver whose blade is a slab "
                    "of blue ice (#9BD8EE with a frosty white edge, wooden handle) in the flipper on the viewer's RIGHT, "
                    "raised out to the side at shoulder height, the blade pointing up, clear of the head and body.")}}},
    "mi_nhi": {"order": 15, "kind": "bird", "forms": {
        1: {"name": "Tiểu Mi", "vn": "chim lia nước con: lông tím lam, chóp cánh ngọc lam, ngọc trai trên mào, đuôi hai lông "
                                      "cong thành đàn lia có dây nước",
            "who": ("a chibi WATER LYREBIRD chick, a songbird of the sea: lavender-blue feathers (#8C8FE0), turquoise wing "
                    "tips (#3CC0C0), cream belly (#F4EEDC); a small curled crest holding one round pearl (#F6F0E6 with a "
                    "pale pink rim); the tail is two curved feathers forming a small lyre (harp) shape with three "
                    "pale-aqua water strings stretched between them; short orange legs (#F08A3C).")},
        2: {"name": "Mi Nhi", "vn": "chim lia tiên: thon cao, lông lam ngọc tím, đuôi đàn lia lớn vân sóng, mào lông dải có "
                                     "ngọc trai, mỏ hé hát",
            "who": ("the same lyrebird grown into an elegant siren bird: slimmer and taller, sapphire (#3E5FC9) and violet "
                    "(#8C6FD8) plumage with turquoise wing tips, cream belly; a large lyre-shaped tail (two big curved outer "
                    "feathers with a wave pattern, four water strings between them) rising behind; long ribbon-like crest "
                    "feathers with two pearls; beak slightly open as if singing a battle song.")}}},
    "ma_ket": {"order": 20, "kind": "seagoat", "forms": {
        1: {"name": "Ma Kết Con", "vn": "dê biển con: nửa trước dê xanh biển, mũ lông bọt trắng, sừng bạc xoắn ngắn, nửa sau "
                                         "đuôi cá vảy ngọc vây cam san hô cuộn trên đất",
            "who": ("a chibi SEA-GOAT kid (capricorn): the front half is a little goat with sea-green fur (#3FA88F), a fluffy "
                    "white foam-like cap and a tiny beard (#F4F1E8), short curled silver horns (#C9CED6 with darker grey "
                    "ridges #8E96A3), two front legs with dark navy hooves (#2A3550); the back half is a chubby fish tail "
                    "with turquoise scales (#3CC0C0) and a coral-orange tail fin (#F08A5A), coiled on the ground behind.")},
        2: {"name": "Ma Kết Sừng Nhọn", "vn": "dê biển lớn: sừng bạc xoắn nhọn dài, vây sau má, đuôi cá dài vây diềm",
            "who": ("the same sea-goat grown: longer pointed spiral silver horns, frilly fin crests behind the cheeks, a "
                    "longer fish tail with frilled coral-orange fins, a bigger foam-white mane and beard, a determined ram "
                    "expression.")},
        3: {"name": "Ma Kết Thánh Giáp", "vn": "dê biển giáp thánh: giáp bạc viền vàng khắc sóng, sừng xoắn lớn đai vàng, "
                                                "bờm râu bọt trắng dài, đuôi cá vây san hô lộng lẫy",
            "who": ("the same sea-goat as a holy armoured guardian: a silver breastplate and head-guard trimmed with gold "
                    "(#E0A93A) and engraved with wave motifs, huge spiral silver horns ringed with gold bands, a long "
                    "flowing foam-white beard and mane, a long powerful fish tail with ornate coral-orange fins, a fierce "
                    "noble gaze.")}}},
    "vay_lam": {"order": 30, "kind": "quad", "forms": {
        1: {"name": "Cá Đốm", "vn": "cá mập con đi bốn chân vây: lưng xanh coban đốm trắng, bụng trắng, vây lưng tròn, răng "
                                     "nhỏ",
            "who": ("a chibi SHARK PUP that walks on four short fin-legs: cobalt-blue back (#3E6FC9) with white spots, white "
                    "belly (#F7F7F2), a small rounded dorsal fin, a short tail fin pointing up behind, big eyes with "
                    "determined brows, a row of small white teeth peeking out.")},
        2: {"name": "Cá Song Tiễn", "vn": "cá mập trẻ: hai vây lưng hình mũi tên, mõm nhọn, sọc nhạt, chân vây có vuốt",
            "who": ("the same shark creature grown leaner and faster: TWO arrow-head shaped dorsal fins, a sharper snout, "
                    "deeper blue (#2F5BB0) with pale stripes instead of spots, fin-legs with small claws, a crescent tail "
                    "fin.")},
        3: {"name": "Cá Mập Vây Lam", "vn": "cá mập vây lam: cơ bắp, viền vây xanh điện, vây lưỡi dao lớn, sẹo qua mắt, hàm "
                                             "răng cưa",
            "who": ("the same shark creature as a powerful blue-fin shark beast: muscular, deep blue (#24479A) with "
                    "electric-blue fin edges (#46C3F0), large blade-like dorsal and pectoral fins, a scar over one eye, "
                    "strong jaws with serrated white teeth (mouth slightly open), a big crescent tail fin.")}}},
    "kuba": {"order": 40, "kind": "crab", "forms": {
        1: {"name": "Kuba", "vn": "cua pha lê con: mai cam san hô, cụm pha lê ngọc biển trên lưng, hai càng giơ thế đấm, mắt "
                                   "cuống",
            "who": ("a chibi CRYSTAL CRAB: a rounded coral-orange shell (#E8794A) with a cluster of aquamarine crystals "
                    "(#7FD6E0 with darker facets #3FA6B8) growing on its back, a pale cream underside (#F3E3BE), two big "
                    "claws raised in a boxing stance (the one on the viewer's RIGHT bigger), eyes on short stalks with "
                    "determined brows, four short walking legs visible (two on each side).")},
        2: {"name": "Kuba Vỏ Cứng", "vn": "cua mai cứng: mai sần có gai pha lê quanh vành, càng đốt ngón pha lê",
            "who": ("the same crystal crab grown big and armoured: a rugged coral-orange shell with a ring of crystal spikes "
                    "along its rim and a bigger crystal cluster on top, claws with crystal knuckles, a stronger wider "
                    "stance.")},
        3: {"name": "Kuba Kim Cương", "vn": "vua cua kim cương: mai đội vương miện kim cương nhiều mặt, viền vàng, càng mũi "
                                             "kim cương",
            "who": ("the same crab as a diamond crab king: its shell crowned with large faceted diamond crystals (ice-white "
                    "#E8F6FA with aquamarine facets #7FD6E0), a golden rim on the shell (#E0A93A), massive diamond-tipped "
                    "claws, a regal fierce expression.")}}},
    "thuong_lam": {"order": 50, "kind": "dragon", "forms": {
        1: {"name": "Thương", "vn": "rồng băng sơ sinh: vảy xanh trời, yếm trắng, hai sừng pha lê nhỏ, cánh màng pha lê băng "
                                     "nhỏ, đuôi ngắn chóp pha lê",
            "who": ("a hatchling ICE DRAGON: pale sky-blue scales (#8CCBF0), white belly plates (#F4F8FA), a small rounded "
                    "snout, two tiny crystal horns, two little wings made of ice-crystal membranes (pale aqua #CFF1F7 with "
                    "blue veins #4F9FD8) folded half open on its back, four short legs, a short tail ending in a crystal "
                    "tip.")},
        2: {"name": "Thương Nhiễm", "vn": "rồng băng trẻ: cổ dài hơn, cánh pha lê sương lớn nửa xoè, sừng vuốt ngược, bờm gai "
                                           "sương",
            "who": ("the same ice dragon grown young and strong: a longer neck, bigger frost-crystal wings half spread up "
                    "behind, swept-back horns, a mane of frost spikes along the neck, a longer tail with an ice fin, deeper "
                    "blue on the back (#5FA8E0).")},
        3: {"name": "Thương Lam", "vn": "rồng băng uy nghi: xanh thẳm và trắng băng, cánh pha lê lớn xoè, vương miện sừng băng, "
                                         "bờm sương, giáp vảy ngực, đuôi lưỡi pha lê",
            "who": ("the same dragon as a majestic ice dragon: deep azure (#2F6FC0) and ice-white, large crystalline wings "
                    "spread up and back, a crown of icy horns, a flowing frost mane, ornate ice-blue armour scales on the "
                    "chest, a long tail ending in a crystal blade.")}}},
    "huyen_vu": {"order": 60, "kind": "turtle", "forms": {
        1: {"name": "Rùa Ngọc", "vn": "rùa ngọc con: da xanh ngọc, mai đen lục viền lục giác vàng, đuôi là rắn nước nhỏ "
                                       "quay đầu lại",
            "who": ("a chibi JADE TURTLE: jade-green skin (#6FBF73), a dark green-black shell (#2E4A3A) with golden hexagon "
                    "rim lines (#E0A93A), four stubby legs; its tail is a little blue water snake (#3E8FD0) whose head "
                    "curls up behind the shell on the viewer's LEFT and also looks to the right with a determined face.")},
        2: {"name": "Rùa Biển Ngọc", "vn": "rùa biển ngọc: chân trước dạng vây, mai ngọc khắc văn sóng, rắn đuôi dài cuộn "
                                            "lên mép mai",
            "who": ("the same turtle grown into a sea turtle: front legs shaped like flippers, the shell engraved with "
                    "golden wave runes and small spikes on its rim, the water-snake tail longer and coiled up over the back "
                    "edge of the shell.")},
        3: {"name": "Huyền Vũ", "vn": "Huyền Vũ cổ: mai ngọc đen văn vàng, gai vành, râu vây trắng dài, rắn nước lớn quấn "
                                       "quanh mai ngóc đầu",
            "who": ("the same turtle as the ancient Black Tortoise guardian: a black-jade shell (#22332B) with golden runes "
                    "and a spiky rim, long flowing white whisker fins on the head, a large water serpent (#2F7FC8 with "
                    "aqua belly) coiled around the shell, its head rising high above the shell on the viewer's LEFT and "
                    "facing right; both heads fierce and majestic.")}}},
    "lam_quan": {"order": 70, "kind": "quad", "forms": {
        1: {"name": "Lam Quân", "vn": "Bồ Lao con (rồng sư tử của chuông đồng): mình xanh biển, bờm sóng kem, sừng nhung vàng "
                                       "nhỏ, chuông đồng tua đỏ ở cổ, gầm nhỏ",
            "who": ("a chibi BELL LION-DRAGON cub (the mythical beast that sits on bronze temple bells): an ocean-blue body "
                    "(#3A78C8), a mane of wave-shaped cream curls (#F4EEDC) tipped with aqua, two small golden antler horns "
                    "(#E0A93A), big determined eyes, mouth open in a small roar, a bronze bell (#C8873A with darker bronze "
                    "bands #8A5420 and a coral-red tassel #D9483B) hanging from a collar, a tufted tail with a wave-shaped "
                    "tip.")},
        2: {"name": "Vạn Quân", "vn": "Bồ Lao trẻ: bờm sóng cuộn lớn, sừng vàng dài, chuông đồng lớn đeo lưng dây tết đỏ, giáp "
                                       "vai đồng khắc sóng",
            "who": ("the same bell lion-dragon grown young and proud: a big mane like rolling waves, longer golden horns, a "
                    "bigger bronze bell slung on its back by a braided coral-red cord, bronze shoulder guards engraved with "
                    "waves, a roaring proud expression.")},
        3: {"name": "Hắc Dực Vạn Quân", "vn": "chúa chuông: cánh lông đen chóp chàm xoè, bờm chàm ngọc như lửa nước, giáp vàng "
                                               "đồng chạm trổ, chuông đồng lớn chạm sóng đeo lưng",
            "who": ("the same bell lion-dragon as the bell lord, the most splendid design of the island: large black-feathered "
                    "wings (#2A2A3A with indigo tips #4B3F8F) spread up behind, a flowing indigo-and-aqua mane like water "
                    "flames, ornate gold-and-bronze armour, a huge ornate bronze bell with wave reliefs carried on its back "
                    "on a coral-red rope, majestic and imposing.")}}},
}

POSES = {
    "quad": ("- Stands on its FOUR legs, all paws flat on one level ground line (no ground drawn), a grounded ready-to-fight "
             "stance: the front a little lower, head forward.\n- All four legs are visible: the two near legs in front, the "
             "two far legs peeking out behind them; white gaps between the front pair and the back pair, and between each "
             "near leg and the far leg next to it where possible.\n- The tail sweeps up and back behind the body on the "
             "viewer's LEFT, clear of the legs with white space between, never crossing the body."),
    "biped": ("- Stands upright on its two feet, both flat on one level ground line (no ground drawn), feet a little apart "
              "with a white gap between them, a grounded ready-to-fight stance.\n- Both flippers are held a little away "
              "from the body with white space between flipper and body; the held item is fully clear of the head and the "
              "body."),
    "bird": ("- Stands on its two legs, feet flat on one level ground line (no ground drawn), a white gap between the legs, a "
             "ready-to-fight stance.\n- Both wings are held a little out from the body, their tips clear of the legs; the "
             "lyre tail rises up behind on the viewer's LEFT, clear of the body except at its root."),
    "seagoat": ("- Rests on its two front legs (hooves flat on one level ground line, no ground drawn, a white gap between "
                "the two legs) and on the coiled fish tail lying on the same ground line behind on the viewer's LEFT.\n- The "
                "tail fin curls up at the left end, clear of the body; head forward and up, horns clear of the body."),
    "crab": ("- Stands on its walking legs (two on each side, tips on one level ground line, no ground drawn), body low and "
             "wide.\n- Both claws are raised in front at chest height like a boxer, held apart from each other and away "
             "from the face, white space around them; the crystals on the back stay clear of the claws."),
    "dragon": ("- Stands on its FOUR legs, all feet flat on one level ground line (no ground drawn), a ready-to-fight stance, "
               "head and neck raised forward.\n- All four legs are visible with white gaps between the front pair and the "
               "back pair.\n- The wings rise up and back above the back, clear of the head; the tail sweeps back on the "
               "viewer's LEFT, clear of the legs."),
    "turtle": ("- Stands on its FOUR legs, feet flat on one level ground line (no ground drawn), head stretched forward out "
               "of the shell with the neck visible.\n- All four legs are visible, white gaps between front and back legs.\n"
               "- The snake (tail) is on the viewer's LEFT, behind the shell, its head clear of the shell outline where "
               "possible, looking to the right."),
}


def code(hid, k):
    return f"{hid}_{k}"


def paths(hid, k):
    c = code(hid, k)
    out_dir = W(HERE, "gui_gpt", c)
    save_dir = W(HERE, "inbox", c, "tai_ve")
    return c, out_dir, save_dir, W(save_dir, "L1_lien.png")


def approved(hid, k):
    """ảnh đã duyệt của dạng k (L1_duyet.png do Claude chọn sau khi soi), không thì L1_lien.png."""
    c = code(hid, k)
    for p in (W(HERE, "inbox", c, "L1_duyet.png"), paths(hid, k)[3]):
        if os.path.isfile(p):
            return p
    return None


def luot_1(hid, k):
    ln = LINES[hid]
    f = ln["forms"][k]
    c, out_dir, save_dir, save = paths(hid, k)
    refs = []
    pool = [(n, d) for n, d in STYLE_POOL if not n.startswith(hid)][:2]
    for n, d in pool:
        refs.append((W(OLD, n, "concept_duyet.png"),
                     f"an approved creature of the same game ({d}), white background: match EXACTLY its hand-drawn pen line, "
                     f"crayon texture, flat colouring, simple readable shapes and determined expression. Do NOT copy its "
                     f"species, design or colours"))
    refs.append((WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen "
                              "outline + coloured pencil / wax crayon hatching), nothing of its content"))
    for j in range(1, k):
        p = approved(hid, j)
        if not p:
            return None
        refs.append((p, f"FORM {j} of this same creature (approved), 1536x1024, white background: keep the same species, "
                        f"face, colours, markings and drawing style so the line clearly grows up"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    boss = ""
    if ln["order"] >= 40:
        boss = ("\nThis line belongs to one of the island's last bosses: make the design especially beautiful and refined "
                "(elegant shapes, rich but readable ornament), more so for later forms.")
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the hand-drawn style of the style images.

CREATURE: {SPIRIT}
{CHIBI[k]}
{f['who']}{boss}

CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature is visible, nothing cut by the edges, at least 60 px of white margin all round. It stands centred, about 720 px tall from the top of its head (ears, horns or crest included) to the soles; the soles rest about 120 px above the bottom edge.

POSE (very important: the picture will be animated as ONE single drawing with a simple 2D skeleton, so body parts must be readable and must not overlap):
- Side three-quarter view turned toward the viewer's RIGHT; the head is at the right, the eyes look to the viewer's right.
{POSES[ln['kind']]}
- Nothing covers the face. Ears, horns, crest and fins do not cross each other.

{line(7).replace("of the style image, NOT the glossy look of the design image", "of the style images")}

Keep the design clean and readable: no text, no background, no extra props, no effects around the creature.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


def huong_dan(hid):
    ln = LINES[hid]
    lines = [f"# {hid}: tướng .atomik thú huyền thoại (rig từ một ảnh liền)", "",
             f"Đảo Thủy, ải {ln['order']}. Người dùng dặn 2026-11-08: thú huyền thoại hơi chibi kiểu Pokémon, style cũ, dạng sau "
             f"dữ hơn nhưng không quá, hạn chế dạng người. Claude gọi Codex bằng `ArtGen/Spine/gen.py`; người dùng không phải "
             f"gửi tay.", ""]
    for k, f in ln["forms"].items():
        c, out_dir, save_dir, save = paths(hid, k)
        lines += [f"## Dạng {k}: {f['name']}", f"- Thiết kế: {f['vn']}.", f"- File prompt: `{W(out_dir, 'luot_1_lien.txt')}`.",
                  "- Ảnh mẫu: 2 concept chibi đã duyệt (nét, tô; ảnh vuông nền trắng, một con thú), bản đồ thế giới (nét)"
                  + (f", ảnh các dạng trước của dòng này (1536x1024)." if k > 1 else "."),
                  f"- Lưu: `{save}`.", ""]
    lines += ["## Kiểm", "- Thú, không dạng người; mặt quả quyết; tô phẳng không bóng không sáng; chân tách nhau, đuôi không vắt "
              "qua thân; dạng sau cùng loài, cùng màu dạng trước.", "",
              "## Câu sửa nhanh", "- \"Flat colour only: no shine spots, no shading, no glow.\"",
              "- \"Keep white gaps between the legs; the tail must not cross the body.\"",
              "- \"More determined face: lowered brows, firm mouth, not a happy grin.\""]
    p = W(HERE, "gui_gpt", code(hid, 1), "HUONG_DAN.md")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return p


def main(ids):
    for n, _ in STYLE_POOL:
        if not os.path.isfile(W(OLD, n, "concept_duyet.png")):
            sys.exit("thiếu ảnh mẫu: " + n)
    for hid in ids or list(LINES):
        for k in LINES[hid]["forms"]:
            p = luot_1(hid, k)
            if p:
                print(p)
        huong_dan(hid)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
