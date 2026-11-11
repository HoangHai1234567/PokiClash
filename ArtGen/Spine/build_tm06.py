"""Gói GPT dòng 6 lô Thủy (`tm06`, thay suất ải 30 Vây Lam): dòng GIÔNG BÃO, kỳ giông nước cõng đồ trên lưng.

Con gốc tham khảo (monster_3241, game khác) là thủy quái ếch cõng thùng gỗ: chỉ giữ chủ đề "thủy quái lưỡng cư mang đồ trên lưng"
và dáng ngồi xổm hai chân; hình, màu, chi tiết, diễn xuất là của mình. KHÔNG đính ảnh con gốc vào prompt (đặc tả lô, mục 3).
Dòng 3 (tm03) là ếch/nòng nọc tròn, nên dòng này là KỲ GIÔNG (đuôi dài, mang lông chim, đầu dẹt), không ếch, không cóc.

  dạng 1 Giông Mưa: kỳ giông con chibi, xanh đá mưa, bụng cam mơ, mang san hô, cõng quả bầu hồ lô.
  dạng 2 Giông Bão: kỳ giông núi khổng lồ BÒ BỐN CHÂN, thân to dẹt, xám tím mây giông, bụng hổ phách, mang đỏ son, vây lưng nối
                    đuôi, cõng bình đồng như mai (điều phối đổi 2026-11-11: bản đứng hai chân thế võ trùng dạng 2 của tm01).
    py -3 -I ArtGen/Spine/build_tm06.py manh 1           dựng gui_gpt/tm06_1/luot_2_manh.txt (tờ mảnh M01..M03 theo concept đã chọn)

    py -3 -I ArtGen/Spine/build_tm06.py                 dựng file prompt (dạng 2 chỉ dựng khi dạng 1 đã chọn)
    py -3 -I ArtGen/Spine/build_tm06.py chon 1 L1_concept_2.png
                                                        chép concept đã chọn của dạng 1 thành inbox/tm06_1/tai_ve/L1_duyet.png
                                                        rồi dựng lại (dạng 2 đính ảnh này)
    py -3 -I ArtGen/Spine/build_tm06.py sua 1 L1_concept.png
                                                        dựng gui_gpt/tm06_1/luot_1_sua.txt: đính bản nháp, giữ bố cục, sửa theo FIX[1]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm06_1/luot_1_concept.txt
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm06"
INBOX = os.path.join(HERE, "inbox")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
# ảnh mẫu là tướng đã duyệt của dự án, khác loài (không ếch, không kỳ giông)
PENGUIN = os.path.join(INBOX, "canh_cut_1", "tai_ve", "L1_lien.png")     # chibi đứng hai chân, tay tách thân, cầm đồ
LION = os.path.join(INBOX, "lam_quan_1", "tai_ve", "L1_lien.png")        # chibi xanh, mặt quả quyết, há miệng thấy lòng miệng
BRAWLER = os.path.join(INBOX, "khong_lo_3", "tai_ve", "L1_lien.png")    # dạng cuối đứng hai chân, khom, thế đánh
DRAGON3 = os.path.join(INBOX, "thuong_lam_3", "tai_ve", "L1_lien.png")  # dạng cuối Thủy: nét, tô phẳng, độ chi tiết
LIZARD = os.path.join(INBOX, "giap_long_2", "tai_ve", "L1_lien.png")    # dạng cuối bốn chân thân thấp dài (dáng bò, thế vồ)


def W(*p):
    return os.path.normpath(os.path.join(*p))


def pk(k):
    return W(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return W(INBOX, f"{CODE}_{k}", "tai_ve")


def chosen(k):
    return W(save_dir(k), "L1_duyet.png")


LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the feet, "
        "nothing on the background), no white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D "
        "look. The only white allowed is one small catchlight dot in each eye (cream spots and foam stripes are flat skin "
        "markings, not highlights). A darker tone appears only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no water, no rain, no effects around it.")
ANIMAL = ("It is an ANIMAL creature of a monster-collecting game (not a human: no human face, no human body, no clothes; only "
          "the carried object and its harness listed below), simple readable shapes. Its face is DETERMINED and ready to "
          "fight: lowered brows, focused eyes looking to the viewer's right; never a happy mascot grin, never scary.")
NOT_FROG = ("Its species must read at once as a SALAMANDER (an axolotl-like newt): a long thick tail, a wide flat head with "
            "feathery external gills, smooth skin. It is NOT a frog, NOT a toad, NOT a tadpole: no frog legs folded under a "
            "round body, no bulging frog eyes, no beak, no shell, no plate or leaves on the head.")

FORMS = {
    1: {
        "name": "Giông Mưa",
        "vn": "kỳ giông con chibi xanh đá mưa, bụng cam mơ, ba lá mang san hô mỗi bên, đốm kem như giọt mưa, đuôi có vây; "
              "cõng quả bầu hồ lô vàng rơm nút gỗ, dây đeo chàm chéo ngực, tua kem",
        "stage": ("FORM 1, the young stage: clearly chibi like a monster-collecting game starter: a big head (about 45% of the "
                  "creature's height), a plump pear-shaped body, short sturdy limbs, expressive eyes. Cute but already brave."),
        "design": [
            "THE CREATURE: a chibi RAIN SALAMANDER pup, a young mythical water amphibian of the water element that carries "
            "the first rain of the season in a gourd on its back.",
            "- Head: wide, flat and rounded, like a broad bean seen from the side, longer than tall. A WIDE mouth runs far "
            "back along the side of the head; it is slightly open, showing the deep-rose inside of the mouth (#C2475E) and "
            "the tip of a pink tongue (#E27C92); no big teeth (at most a row of tiny cream nubs). Two medium round eyes sit "
            "high on the head near the front: golden-yellow irises (#F2C641), a dark round pupil, one small catchlight dot, "
            "short lowered brow lines above them.",
            "- Gills: on each side of the head, just behind the cheek, THREE feathery external gill fronds, each like a "
            "little fern branch with small rounded fringes along both edges, coral red-orange (#E5603F). The three fronds "
            "of a side fan out backward and a little upward from one root behind the cheek; the far-side fronds only peek "
            "out above and behind the head.",
            "- Skin: smooth slate rain-blue (#6E88BC) on the head, back, arms, legs and tail. The throat, chest and belly "
            "are one soft apricot-orange patch (#F4A65A). Round cream spots (#F4EEDC) of a few different sizes, like "
            "raindrops, are scattered along the top of the head, the back and the tail (not on the face).",
            "- Limbs: short thick hind legs with wide webbed feet, four rounded toes; short arms with small webbed "
            "four-fingered hands.",
            "- Tail: long and thick, with a soft low fin (pale blue #9CC0E8) along its top and bottom edges, the tip "
            "curling up.",
            "- What it carries: a big CALABASH GOURD water flask on its back, as tall as its body: two bulbs (the lower "
            "bulb bigger), straw yellow (#E8C66A) with a few paler lengthwise stripes, a carved round wooden stopper "
            "(#8A5A33) in its narrow neck, a small cream tassel (#F4EEDC) tied just below the stopper. It hangs from an "
            "indigo cord harness (#2F4F8F): one cord crosses the chest diagonally from the near shoulder down to the far "
            "hip, with a simple knot on the chest.",
        ],
        "pose": [
            "- Side three-quarter view turned toward the viewer's RIGHT; the head is at the right, the eyes look to the "
            "viewer's right.",
            "- It stands upright on its two hind legs, both feet flat on one level ground line (no ground drawn), feet apart "
            "with a white gap between the legs, knees a little bent: a grounded ready-to-fight squat, the body leaning a "
            "little forward.",
            "- The near arm is raised forward at chest height with a small clenched fist; the far arm is held a little back "
            "and up behind the body with the hand open, fingers spread. Both arms are clear of the body and of the face, "
            "with white space between.",
            "- The tail lies behind it on the viewer's LEFT and rests on the ground line, its tip curling up, clear of the "
            "legs with white space between, never crossing the body.",
            "- The gourd sits on its back on the viewer's LEFT side of the body, tilted back a little, its neck and stopper "
            "sticking up behind the shoulders, BELOW and BEHIND the gill fronds with white space between the gourd and the "
            "fronds; the gourd never covers the head, the arms or the legs. The gill fronds do not cross each other.",
            "- Mouth slightly open (the inside visible). Nothing covers the face.",
        ],
        "height": 700,
        "check": [
            "Kỳ giông (đuôi dài, đầu dẹt rộng, mang lông chim), **không** ra ếch / cóc / nòng nọc; không mỏ, không đĩa, không lá trên đầu.",
            "Chibi đầu khoảng 45%; mặt quả quyết (mày hạ), không cười toe; nhìn sang **phải**.",
            "Màu: thân xanh đá mưa, bụng cam mơ, ba lá mang san hô mỗi bên, đốm kem, vây đuôi lam nhạt.",
            "Quả bầu hồ lô vàng rơm, nút gỗ nâu, tua kem, dây chàm chéo ngực; bầu ở sau lưng phía trái, không che đầu, mang, tay.",
            "Hai chân tách nhau có khe trắng, tay tách thân, đuôi không chéo chân; miệng hé thấy lòng miệng.",
            "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không đường đất.",
        ],
    },
    2: {
        "name": "Giông Bão",
        "vn": "kỳ giông núi khổng lồ BÒ BỐN CHÂN, thân to dẹt nặng, đầu rộng dẹt mõm tròn, miệng rộng nanh nhỏ, mắt nhỏ xếch; da xám "
              "tím mây giông #5A5878 (sống lưng #3E3C58), sọc bọt sóng, bụng hổ phách chia tấm, mang lông chim đỏ son lớn, vây "
              "lưng nối vây đuôi dẹt dài; cõng bình đồng xanh rỉ đai vàng như mai, dây thừng chàm quấn ngực và bụng, vòng cổ đồng",
        "stage": ("FORM 2, the FINAL stage of this two-stage line: fully grown and NOT chibi at all: a huge, heavy, low GIANT "
                  "SALAMANDER that crawls on FOUR legs; the head is only about one fifth of the body length; small sharp narrowed "
                  "eyes, a broad mouth with small fangs; fierce, proud and battle-hardened, but NOT scary or monstrous. A "
                  "completely different silhouette from form 1 (form 1 stands up on two legs like a chibi; form 2 crawls low on "
                  "four legs like a giant mountain salamander carrying a big load on its back), but clearly the same line (big "
                  "red feathery gill fronds, orange belly, something carried on its back)."),
        "design": [
            "THE CREATURE: a GIANT MOUNTAIN STORM SALAMANDER, the grown-up form of the rain salamander of image 1, a mythical "
            "water amphibian that carries a whole thunderstorm sealed in a bronze urn on its back like a shell. This line "
            "belongs to one of the island's bosses: make it especially beautiful and refined (elegant shapes, rich but "
            "readable ornament).",
            "- Body: like a real giant salamander: a long, broad, flat, heavy body carried low just above the ground, a few "
            "wavy ink lines for the loose skin folds along the flank; a white gap between the belly and the ground line.",
            "- Head: very broad and flat, rounded at the front like a shovel (a round blunt snout, NOT a long crocodile or "
            "lizard snout), wider than tall, held low and forward; small sharp narrowed eyes set high near the front, amber "
            "irises (#F0A030) with a dark slit pupil and one small catchlight dot, a heavy brow; the very wide mouth runs far "
            "back along the side of the head and is slightly open, showing the deep-rose inside (#B8405A), a row of small "
            "pointed cream teeth and two small fangs.",
            "- Gills: on each side of the head behind the jaw, THREE BIG feathery gill fronds like long fern branches, crimson "
            "red (#C8383A), much bigger and longer than those of form 1, sweeping up and back like a war crest; the far-side "
            "fronds only peek out above the head.",
            "- Skin: storm-cloud grey-violet (#5A5878) on the head, back, legs and tail, with a darker grey-violet band "
            "(#3E3C58) along the top of the back and the top of the tail; white-foam markings (#EAF2F8) shaped like small "
            "curling wave crests on the back, the flanks, the legs and the tail. The throat and the belly are a row of wide "
            "amber-orange belly plates (#E8782E) separated by thin ink lines, visible along the underside.",
            "- Legs: four short, thick, bowed legs splayed a little sideways like a salamander's, broad webbed feet with four "
            "toes and short dark claws (#2B2118).",
            "- Back fin and tail: a low wavy fin crest, pale storm-blue membrane (#8FB3E0) with thin dark-brown ink spines, "
            "runs from the back of the head along the spine (hidden behind the urn) and continues as a taller fin along the "
            "top and the bottom of the long, thick, flattened paddle tail.",
            "- What it carries: a big BRONZE WATER URN lying on its back like a shell, as wide as about half of the body: "
            "old verdigris bronze (#4E9E8A) with gold-bronze bands (#D4A23F) and a raised curling-wave relief around its "
            "belly, a heavy domed bronze lid with a ring handle, the short neck of the urn pointing up and a little forward. "
            "It is tied on with a thick indigo rope harness (#2A3F78) with knots: one rope loops around the chest just behind "
            "the front legs, one around the belly just before the hind legs, and a bronze collar band (verdigris with a gold "
            "rim) sits around the neck.",
        ],
        "pose": [
            "- Side view turned slightly toward the viewer, facing the viewer's RIGHT; the head is at the right, the eyes look "
            "to the viewer's right.",
            "- It crawls low on ALL FOUR legs, all four feet flat on one level ground line (no ground drawn), the body low and "
            "horizontal, ready to lunge: the front a little lower, the head low and forward, the jaws slightly open.",
            "- All four legs are visible: the two near legs in front, the two far legs peeking out behind them; white gaps "
            "between the front pair and the back pair, and between each near leg and the far leg next to it where possible.",
            "- The long tail sweeps back on the viewer's LEFT, roughly horizontal, its tip lifted a little, clear of the hind "
            "legs with white space between.",
            "- The urn sits on the middle of the back; it never covers the head or the gill fronds. The gill fronds do not "
            "cross each other. Nothing covers the face.",
            "- It does NOT stand on two legs: no fists, no raised arms, no boxing or martial-arts pose.",
        ],
        "frame": ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole "
                  "creature is visible (urn, gill fronds and tail included), nothing cut by the edges, at least 60 px of white "
                  "margin all round. It is centred, about 1380 px wide from the tail tip to the snout and about 600 px tall "
                  "from the top of the urn to the feet; its lowest point is about 150 px above the bottom edge."),
        "height": 600,
        "check": [
            "**Bò bốn chân** thân to dẹt sát đất như kỳ giông núi khổng lồ; không đứng hai chân, không nắm đấm, không thế võ.",
            "Đầu rộng dẹt mõm tròn (không mõm dài kiểu cá sấu, thằn lằn), miệng rộng hé có nanh nhỏ, mắt nhỏ xếch; nhìn sang **phải**.",
            "Màu xám tím mây giông (không chàm, không cobalt), sống lưng sẫm hơn, sọc bọt sóng, bụng hổ phách chia tấm, mang đỏ son lớn.",
            "Bình đồng xanh rỉ đai vàng nằm trên lưng như mai, dây thừng chàm quấn ngực và bụng, vòng cổ đồng; bình không che đầu, mang.",
            "Bốn chân tách nhau có khe trắng, đuôi dẹt có vây trên dưới nằm sau bên trái, không chéo chân.",
            "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không đường đất.",
        ],
    },
}


def refs_of(k):
    """(đường dẫn, mô tả tiếng Anh, mô tả tiếng Việt)."""
    if k == 1:
        return [
            (PENGUIN, "another approved hero of the same game (a round chibi penguin holding a pan), 1536x1024, white "
                      "background: copy its framing, its pose logic (three-quarter side view facing right, limbs separated "
                      "from the body by white gaps), its hand-drawn pen line and its flat crayon colouring. Do NOT copy its "
                      "species, design or colours",
             "Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi xanh ngọc cầm chảo, đứng hai chân. Lấy bố "
             "cục, dáng tách tay chân, nét"),
            (LION, "another approved hero of the same game (a chibi blue lion cub), 1536x1024, white background: match EXACTLY "
                   "its pen line, crayon texture, flat colouring, simple readable shapes and its determined face with the "
                   "mouth slightly open. Do NOT copy its species, design or colours",
             "Lam Quân dạng 1 đã duyệt (1536 × 1024, nền trắng): sư tử con chibi xanh lam bờm mây kem, há miệng. Lấy nét, vân "
             "sáp, mặt quả quyết"),
            (WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
        ]
    return [
        (chosen(1), "FORM 1 of this same creature (approved), 1536x1024, white background: keep the same species (a "
                    "salamander), the feathery gill fronds, the orange belly, the idea of carrying something on its back "
                    "and the drawing style, so the line clearly grows up. Do NOT copy its chibi proportions, its two-legged "
                    "pose, its colours, its spots or its gourd: form 2 is described below and is bigger, fiercer and different",
         "Concept dạng 1 Giông Mưa đã chọn (1536 × 1024, nền trắng): kỳ giông con chibi xanh đá mưa cõng bầu hồ lô"),
        (LIZARD, "another approved FINAL-form hero of the same game (a fire lizard), 1536x1024, white background: take ONLY its "
                 "low four-legged crawling stance (long body close to the ground, four separated legs, tail behind on the "
                 "left), its fierce attitude and its level of detail. Do NOT copy its species, armour, horns, spikes, flames "
                 "or colours",
         "Giáp Long dạng 2 đã duyệt (1536 × 1024, nền trắng): thằn lằn lửa giáp bò bốn chân. Chỉ lấy dáng bò thấp, thần thái"),
        (DRAGON3, "another approved final-form water hero of the same game (an ice dragon), 1536x1024, white background: match "
                  "EXACTLY its pen line, crayon texture, flat colouring and level of ornament. Do NOT copy its species, "
                  "wings, colours or pose",
         "Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): rồng băng cánh xanh nhạt. Lấy nét, tô phẳng, mức hoa văn"),
        (WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                      "outline + coloured pencil / wax crayon hatching), nothing of its content",
         "Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay. Chỉ lấy nét"),
    ]


def check(refs):
    miss = [W(p) for p, _, _ in refs if not os.path.isfile(p)]
    return miss


def build_form(k):
    f = FORMS[k]
    refs = refs_of(k)
    miss = check(refs)
    if miss:
        print(f"(chưa dựng dạng {k}: thiếu {', '.join(miss)})")
        return None
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = free_name(save_dir(k), "L1_concept")
    p = W(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {out}",
          "If a file with that name already exists, add _2, _3 ... before .png (the first free name) in the same folder. Do "
          "not edit, move or delete any other file.", "",
          "TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the "
          "hand-drawn style of the style images. It is a concept sheet: later the same creature will be redrawn as separate "
          "parts for a 2D skeleton animation, so the shapes must be clear and well separated.", "",
          "CREATURE: " + ANIMAL, NOT_FROG, f["stage"], ""]
    t += f["design"]
    t += ["", f.get("frame") or (
              f"CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole "
              f"creature is visible (the carried object, gill fronds and tail included), nothing cut by the edges, at least "
              f"60 px of white margin all round. It is centred, about {f['height']} px tall from its highest point to its "
              f"lowest point; its lowest point is about 120 px above the bottom edge."), "",
          "POSE (very important: body parts must be readable and must not overlap):"]
    t += f["pose"]
    t += ["", LINE.format(n=7), FLAT, BG]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng Giông Bão, dạng {k} {f['name']} (`{CODE}_{k}`)", "",
          f"Lô 10 tướng mới đảo Thủy, dòng 6 (thay suất ải 30, Vây Lam, hiếm). Thiết kế: {f['vn']}.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{p}`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `{out}` "
          "(trùng tên thì `L1_concept_2.png`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` (chạy nền, "
          "khoá Codex chung).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; mọi ảnh mẫu là tướng của dự án.", "", "## Kiểm", ""]
    gd += [f"- {c}" for c in f["check"]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note \"...\"`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Ra ếch, cóc | `It must be a salamander: a long thick tail, a wide flat head, feathery gill fronds; not a frog or a toad.` |",
           "| Có bóng, mảng sáng tối, điểm sáng | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |",
           "| Đồ trên lưng che đầu, mang | `Move the carried object lower and further back so it never covers the head or the gill fronds.` |",
           "| Tay chân dính thân, chéo nhau | `Leave white gaps between the legs and between each arm and the body; nothing crosses.` |",
           "| Nhìn sang trái | `The creature must face the viewer's RIGHT.` |"]
    if k == 2:
        gd += ["| Đứng hai chân, thế võ | `It must crawl low on all four legs like a giant salamander: no standing, no fists.` |",
               "| Mõm dài như cá sấu, thằn lằn | `The head is very broad and flat with a round blunt snout like a giant salamander.` |",
               "| Màu ra chàm, lam đậm | `The skin is storm-cloud grey-violet #5A5878, not indigo or blue.` |"]
    with open(W(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(gd) + "\n")
    return p


# sửa một bản nháp đã gen: đính bản nháp làm ảnh mẫu, giữ bố cục, chỉ sửa những điều ghi ở đây (dạng: danh sách câu tiếng Anh)
FIX = {
    1: ["Keep EVERYTHING of image 1 that is not listed below: the same creature, the same compact chibi proportions, the "
        "same pose, the same determined shouting face with the open mouth and the pink tongue, the same gill fronds, the same "
        "cream spots, the same striped gourd strapped on its back with the indigo cord across the chest, the same framing.",
        "CHANGE 1, the skin colour: every slate-blue area (head, back, arms, legs, tail) becomes a MUTED GREYISH SLATE BLUE "
        "#6E88BC, like a rain cloud: clearly duller and greyer than the bright cornflower blue of image 1. The belly stays "
        "apricot orange, the gills coral, the tail fin pale blue.",
        "CHANGE 2: remove the small white shine strokes on the top of the head and any other white highlight or shine mark "
        "anywhere (the gourd too). The only white is one catchlight dot in each eye; the cream spots stay as flat cream spots.",
        "CHANGE 3: move the far open hand a little so it no longer overlaps the gourd: leave a clear white gap between that "
        "hand and the gourd.",
        "Draw it again as a clean new picture with the same pen line and flat crayon colouring; do not trace image 1 as a "
        "photo edit."],
}


def build_fix(k, draft):
    f = FORMS[k]
    src = W(save_dir(k), draft)
    if not os.path.isfile(src):
        raise SystemExit("không có " + src)
    refs = [(src, "the DRAFT of this creature to correct, 1536x1024, white background", "bản nháp cần sửa")]
    refs += [r for r in refs_of(k) if r[0] != src]
    n = 2
    while os.path.exists(W(save_dir(k), f"L1_concept_{n}.png")):
        n += 1
    out = W(save_dir(k), f"L1_concept_{n}.png")
    p = W(pk(k), "luot_1_sua.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {out}",
          f"If a file with that name already exists, save as L1_concept_{n + 1}.png, L1_concept_{n + 2}.png ... in the same "
          "folder. Do not edit, move or delete any other file.", "",
          "TASK: redraw the creature of image 1 as ONE full picture with the corrections below, in the hand-drawn style of "
          "the style images.", ""]
    t += FIX[k]
    t += ["", "CREATURE: " + ANIMAL, NOT_FROG, f["stage"], ""]
    t += f["design"]
    t += ["", "CANVAS: landscape 1536x1024, pure-white background, NO ground line, no cast shadow, the whole creature "
              "visible with at least 60 px of white margin all round.", "", LINE.format(n=7), FLAT, BG]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(t) + "\n")
    return p


def free_name(d, stem):
    """đường dẫn tên trống đầu tiên: stem.png, stem_2.png, ..."""
    p = W(d, stem + ".png")
    n = 2
    while os.path.exists(p):
        p = W(d, f"{stem}_{n}.png")
        n += 1
    return p


# ------------------------------------------------------------------ tờ mảnh (pha 2)
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene and NOT a whole creature: every part "
          "is drawn COMPLETE and on its own, flat on the white page like stickers laid out on a table, with at least 60 px of "
          "pure white between any two parts and between a part and the image edge. No part touches or overlaps another. Do "
          "not draw a whole creature, do not draw extra parts, do not draw labels, numbers, arrows or guide lines.")
SAME = ("Draw every part EXACTLY as it looks in the approved concept (image 1): the same shape, the same angle, the same curve, "
        "the same colours, markings and line, only bigger and complete: the areas that are hidden behind other parts in "
        "image 1 are drawn in, and where a part joins another part it ends in a smooth rounded stump that continues the shape "
        "a little (the joint is hidden under the other part).")
# (bước, tiêu đề, mô tả tiếng Anh, ghi chú tiếng Việt)
STEPS = {
    1: [
        ("M01", "head, jaw, mouth, eyelids, gill fronds, stopper",
         "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n"
         "- top-left cell: the HEAD, UPPER PART ONLY, as in image 1 (side view facing the viewer's RIGHT): the wide flat bean-"
         "shaped skull with its cream spots, both eyes OPEN (the big near eye and the narrow far eye at the front edge) with "
         "their lowered brows, the nostril dots, and the UPPER lip line of the open mouth along the bottom edge. NOT the lower "
         "jaw, NOT the chin, NOT the tongue, NOT the gill fronds. The lower back end (where the neck joins) is a smooth rounded "
         "stump. About 460 px wide.\n"
         "- top-middle cell: the LOWER JAW alone, as in image 1: the apricot-orange chin and lower lip as one wedge, the pink "
         "tongue (#E27C92) lying inside along its top edge with a thin strip of the deep-rose inner mouth (#C2475E) above the "
         "gum line, no teeth; its back end (the jaw hinge, under the cheek) is a rounded knob. About 300 px wide.\n"
         "- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob of flat deep rose (#C2475E) with a slightly "
         "darker throat spot in the middle, brown ink outline, about 220 px wide and 140 px tall. No teeth, no tongue.\n"
         "- bottom-left cell: TWO CLOSED EYELIDS stacked one above the other with white between them, for the eyes of the head "
         "above: each is a small patch of the slate-blue head skin (#6E88BC, crayon hatching) with the brown ink outline all "
         "round and ONE thick dark-brown curved line across its lower half (the shut eye, a stern frown); the big one (near "
         "eye) about 120 px wide and 105 px tall, the small one (far eye) about 70 px wide and 100 px tall.\n"
         "- bottom-middle cell: THREE GILL FRONDS stacked one above the other with white between them, each drawn perfectly "
         "STRAIGHT and horizontal like a fern leaf lying on the table: the rounded root on the LEFT, the tip on the RIGHT, the "
         "same coral red-orange (#E5603F) fern fringes along both edges as in image 1; lengths about 330 px, 280 px and "
         "230 px, about 80 px wide at the widest.\n"
         "- bottom-right cell: the gourd's carved round wooden STOPPER alone (#8A5A33), about 110 px wide and 100 px tall.",
         "đầu (phần trên, mắt mở, không hàm, không mang), hàm dưới có lưỡi, mảng lòng miệng, hai mí nhắm, ba lá mang duỗi thẳng, "
         "nút bầu"),
        ("M02", "torso, tail, arms",
         "Canvas 1536 x 1024.\n"
         "- LEFT third of the canvas: the TORSO alone, as in image 1: chest, apricot-orange belly patch, slate-blue back and "
         "sides with cream spots, the shoulders and the hips, the indigo cord crossing the chest with its round knot. NOT the "
         "head (the neck at the top ends in a smooth rounded stump that rises a little higher than in image 1), NOT the arms "
         "(rounded shoulder stumps), NOT the legs (rounded hip stumps), NOT the tail, NOT the gourd. About 380 px wide and "
         "500 px tall.\n"
         "- RIGHT two thirds, top half: the TAIL alone, as in image 1, with the SAME curve (it sweeps to the left and its tip "
         "curls up), the cream spots and the pale blue fins along its top and bottom edges; its root end (on the RIGHT, where "
         "it joins the hips) is a thick smooth rounded stump. About 760 px wide and 420 px tall.\n"
         "- RIGHT two thirds, bottom half, two parts side by side with white between them: (a) the NEAR ARM, as in image 1: "
         "from the rounded shoulder stump, the short slate-blue arm bent at the elbow with the clenched fist, about 260 px wide "
         "and 220 px tall; (b) the FAR ARM, as in image 1: from the rounded shoulder stump, the short arm raised with the open "
         "webbed hand, fingers spread, about 230 px wide and 300 px tall.",
         "thân (ngực, bụng, dây chéo, không đầu, tay, chân, đuôi), đuôi cong như concept, tay gần nắm đấm, tay xa xoè"),
        ("M03", "legs and gourd",
         "Canvas 1536 x 1024. Three parts in one row, left to right, with white between them:\n"
         "- the LEFT LEG (the leg on the viewer's left in image 1), as in image 1: the thick slate-blue thigh from a rounded "
         "hip stump at the top, the bent knee and the wide webbed foot with four rounded toes and pale blue webbing, flat on "
         "the invisible ground; about 300 px wide and 380 px tall.\n"
         "- the RIGHT LEG (the leg on the viewer's right in image 1), as in image 1, the same way; about 330 px wide and 380 "
         "px tall.\n"
         "- the GOURD alone, as in image 1 with the same tilt: both bulbs, the pale lengthwise stripes, the indigo cord band "
         "around its lower bulb, the cream tassel tied below the neck; WITHOUT the wooden stopper (the open round mouth of the "
         "neck is seen as a short ring); about 330 px wide and 520 px tall.",
         "chân trái, chân phải (như concept), quả bầu không nút"),
    ],
    2: [
        ("M01", "head, jaw, mouth, eyelids, gill fronds",
         "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n"
         "- top-left cell: the HEAD, UPPER PART ONLY, as in image 1 (side view facing the viewer's RIGHT): the broad flat "
         "grey-violet skull with the white wave marking on the brow, the amber eye with its slit pupil and heavy brow, the "
         "nostril, the rounded snout, and the upper lip with the upper teeth hanging along its bottom edge. NOT the lower jaw, "
         "NOT the orange chin, NOT the gill fronds, NOT the bronze collar, NOT the back fin. The back end (where the neck "
         "joins) is a smooth rounded stump. About 470 px wide.\n"
         "- top-middle cell: the LOWER JAW alone, as in image 1: one long wedge, amber-orange (#E8782E) underside and chin, "
         "the lower teeth standing along its top edge with a thin strip of the deep-rose inner mouth (#B8405A) above the gum "
         "line; its back end (the jaw hinge) is a rounded knob. About 420 px wide.\n"
         "- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob of flat deep rose (#B8405A) with a slightly "
         "darker throat spot in the middle, brown ink outline, about 260 px wide and 150 px tall. No teeth.\n"
         "- bottom-left cell: TWO CLOSED EYELIDS stacked one above the other with white between them, for the eyes of the head "
         "above: each is a small patch of the grey-violet head skin (#5A5878, crayon hatching) with the brown ink outline all "
         "round and ONE thick dark-brown curved line across its lower half (the shut eye, a stern frown); the big one (near "
         "eye) about 130 px wide and 95 px tall, the small one (far eye at the snout) about 60 px wide and 80 px tall.\n"
         "- bottom-middle and bottom-right cells together: THREE GILL FRONDS one above the other with white between them, each "
         "drawn perfectly STRAIGHT and horizontal like a long fern leaf lying on the table: the rounded root on the LEFT, the "
         "tip on the RIGHT, the same crimson (#C8383A) feathery fringes along both edges as in image 1; lengths about 380 px, "
         "320 px and 260 px, about 100 px wide at the widest.",
         "đầu (phần trên, răng trên, không hàm, không mang, không vòng cổ), hàm dưới có răng, mảng lòng miệng, hai mí nhắm, ba lá "
         "mang duỗi thẳng"),
        ("M02", "body trunk and tail",
         "Canvas 1536 x 1024. Two parts, one above the other, with white between them:\n"
         "- top: the BODY TRUNK alone, as in image 1, side view: from the neck at the RIGHT end (with the bronze collar band "
         "around it, verdigris with the gold rim and wave relief) to the hips at the LEFT end: the grey-violet back with the "
         "darker band along the top and the white wave markings, the low wavy pale storm-blue fin along the top of the back, "
         "the row of amber-orange belly plates along the underside, the indigo rope loops around the chest and the belly with "
         "their knots. NOT the urn (draw the back complete where the urn would sit), NOT the legs (smooth rounded shoulder and "
         "hip stumps), NOT the head (the neck ends in a rounded stump just in front of the collar), NOT the tail (rounded "
         "stump at the left). About 1050 px wide and 330 px tall.\n"
         "- bottom: the TAIL alone, as in image 1, with the SAME curve (it sweeps to the left and its tip curls up), the "
         "white wave markings, the darker band along its top, and the tall wavy pale storm-blue fins along its top and its "
         "bottom edge; its root end (on the RIGHT, where it joins the hips) is a thick smooth rounded stump. About 620 px wide "
         "and 400 px tall.",
         "thân (cả vòng cổ đồng, vây lưng thấp, dây thừng quanh ngực bụng; không bình, không chân, không đầu, không đuôi), đuôi cong "
         "như concept có vây trên dưới"),
        ("M03", "urn, lid and four legs",
         "Canvas 1536 x 1024.\n"
         "- top half, two parts side by side with white between them: (a) the BRONZE URN alone, as in image 1 with the same "
         "tilt: the round verdigris body with the gold bands and the curling-wave relief, the indigo ropes running over it "
         "with their knots at the bottom, the short neck with its gold rim; WITHOUT the lid (the open round mouth of the neck "
         "is seen as a short ring); about 520 px wide and 420 px tall. (b) the domed bronze LID alone, as in image 1: "
         "verdigris dome with the gold rim, the wave pattern and the round gold ring handle on top; about 300 px wide and "
         "260 px tall.\n"
         "- bottom half, FOUR LEGS in one row from left to right, each as in image 1 with the same angle, each from a smooth "
         "rounded top stump (where it joins the body) down to the broad webbed foot with its pale blue webbing and dark "
         "claws, flat on the invisible ground: (1) the leg at the far LEFT of image 1 (hind leg near the tail), about 300 px "
         "wide and 300 px tall; (2) the second leg from the left in image 1 (the smaller darker hind leg behind the belly), "
         "about 240 px wide and 220 px tall; (3) the third leg from the left (under the middle of the body), about 300 px wide "
         "and 290 px tall; (4) the leg at the far RIGHT of image 1 (the front leg reaching forward under the head), about 320 "
         "px wide and 300 px tall.",
         "bình đồng không nắp (có dây thừng trên bình), nắp bình có vòng, bốn chân theo thứ tự trái → phải trên concept"),
    ],
}


def build_parts(k):
    """luot_2_manh.txt của dạng k: các tờ mảnh vẽ theo concept đã chọn (chosen(k))."""
    if k not in STEPS:
        raise SystemExit(f"chưa viết STEPS cho dạng {k}")
    concept = chosen(k)
    if not os.path.isfile(concept):
        raise SystemExit("chưa có " + concept)
    f = FORMS[k]
    refs = [(concept, f"the APPROVED CONCEPT of this creature ({f['name']}), 1536x1024: every part you draw belongs to THIS "
                      "creature: the same species, shapes, colours, markings, line and crayon texture. Draw its parts "
                      "separately as described; do not redraw the whole creature",
             f"Concept dạng {k} {f['name']} đã chọn (1536 × 1024, nền trắng)"),
            (WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay. Chỉ lấy nét")]
    steps = STEPS[k]
    order = [s[0] for s in steps]
    sd = save_dir(k)
    p = W(pk(k), "luot_2_manh.txt")
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", "WHAT THIS IS: sheets of separate, complete parts of the creature of image 1, for a 2D cut-out animation rig. "
              "The animation software moves each part with bones (it bends the tail and the gill fronds, opens the lower jaw, "
              "blinks the eyelids, swings the limbs), so every part must be drawn whole, clean, and well separated.", "",
          f"SAVE: every step's image goes into {sd} under the step's name (for example {order[0]}.png). If that file already "
          "exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and stop, "
          f"in this order: {', '.join(order[1:])}.", "", SAME, ""]
    for sc, title, en, _ in steps:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, SAME, en, "", LINE.format(n=7), FLAT, BG,
              f"SAVE this step: save it as a PNG to {W(sd, sc + '.png')} (create the folder if it is missing; if that file "
              f"already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do not change, move or "
              "delete any other file.", ""]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(t) + "\n")
    gd = open(W(pk(k), "HUONG_DAN.md"), encoding="utf-8").read() if os.path.isfile(W(pk(k), "HUONG_DAN.md")) else ""
    mark = "\n## Lượt 2: tờ mảnh\n"
    gd = gd.split(mark)[0].rstrip("\n") + "\n" + mark + "\n" + "\n".join(
        [f"**Chỉ gửi GPT đường dẫn:** `{p}`, các bước {', '.join(order)} (gõ `next` sau mỗi ảnh). GPT lưu vào `{sd}`.", "",
         f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_2_manh.txt --steps {','.join(order)}`.",
         "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        + [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
        + ["", "Kiểm: mỗi tờ 1536 × 1024 nền trắng, các mảnh rời nhau ít nhất 60 px, vẽ đúng dáng concept, đủ phần bị che.", ""]
        + [f"- **{sc}**: {vi}" for sc, _, _, vi in steps]) + "\n"
    with open(W(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(gd)
    return p


def main(argv):
    if argv[:1] == ["sua"]:
        print(build_fix(int(argv[1]), argv[2]))
        return
    if argv[:1] == ["manh"]:
        print(build_parts(int(argv[1])))
        return
    if argv[:1] == ["concept"]:
        print(build_form(int(argv[1])))
        return
    if argv[:1] == ["chon"]:
        k, name = int(argv[1]), argv[2]
        src = W(save_dir(k), name)
        if not os.path.isfile(src):
            raise SystemExit("không có " + src)
        shutil.copyfile(src, chosen(k))
        print("đã chọn", src, "->", chosen(k))
    for k in sorted(FORMS):
        p = build_form(k)
        if p:
            print(p)


if __name__ == "__main__":
    main(sys.argv[1:])
