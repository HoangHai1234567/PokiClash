# Sinh gói gửi GPT cho hình tướng: ArtGen/Heroes/gui_gpt/<mã>/ (quy trình: QUY_TRINH.md).
# Cách làm: vẽ con mới đè lên rig vector của aola (người dùng: "vẫn phải dùng rig cũ", 2026-11-02) để giữ animation aola.
# Mỗi dạng 2 lượt, mỗi lượt một thư mục con: ảnh đánh số đúng thứ tự đính kèm + 00_instructions.txt (tiếng Anh, GPT đọc rồi vẽ),
# kèm HUONG_DAN.md (tiếng Việt: gửi gì, lưu đâu, từng ảnh trông ra sao, câu sửa nhanh).
#   1_concept:   concept cả con trên rig (bóng xám, bản đồ vùng) + tờ mẫu thiết kế (aola) + ảnh mốc nét vẽ (bản đồ).
#   2_nhom_manh: từng nhóm mảnh vẽ đè lên hình gốc của nhóm (refs/<hệ>/<mã>/orig/Nxx.png) + concept đã duyệt; một ảnh mỗi lượt.
# Nét: vẽ tay như bản đồ world_style.png; thiết kế học từ tướng aola. Viền trắng giấy xé do game vẽ (shader), GPT không vẽ.
# Chạy: py -3 -I ArtGen/Heroes/build.py (từ thư mục PokiWar). Ảnh mẫu aola: tools/make_refs.py.
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = "E:/ProjectAtomik/PokiWar/ArtGen/Heroes/"
STYLE_SHEET = ROOT + "refs/style/style_sheet.png"
WORLD_STYLE = "E:/ProjectAtomik/PokiWar/ArtGen/Islands/refs/world_style.png"


def W(p):
    return p.replace("/", "\\")


# ---------- khối dùng chung ----------
RENDER = ("RENDERING (copy it from the game's hand-drawn map): drawn by hand by a professional illustrator for a storybook "
          "game: bold dark-brown ink outlines (#2B2118) of fairly even weight, slightly wobbly like a real pen; flat warm "
          "colours shaded with loose diagonal coloured-pencil hatching; a few small white highlights; clean and appealing, "
          "neither a crude kid scribble nor overly detailed. No glossy digital shine, no smooth airbrushed gradients, no 3D "
          "render. No white border or sticker outline around the creature or its parts: the game adds that itself.")
DESIGN = ("DESIGN (learn it from the game's creatures in the style sheet): an appealing original creature in the classic "
          "Japanese monster-collecting look: a clear, chunky silhouette that reads at small size, big expressive eyes, simple "
          "readable shapes, few details. Take only the design approach from those creatures, never their glossy rendering "
          "and never their designs.")
LINE = ("LINE AND COLOUR: the hand-drawn rendering of image 2, not image 1's glossy vector look: a dark-brown ink outline "
        "(#2B2118) about {n} px thick on this 1024 canvas, the same weight on every edge, slightly wobbly like a real pen; flat "
        "warm colours shaded with loose diagonal coloured-pencil hatching (strokes thinner than the outline), kept inside the "
        "outline; a few small white highlights; no gradients, no glossy shine, no paper texture, no white border around the "
        "pieces.\nPlain white background. Only this group. No text.")
KEEP_FRAME = ("FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the "
              "drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow "
              "image 1: take only colours, details and drawing style from image 2.")


def free_frame(joint):
    return (f"FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its {joint} "
            "stays exactly where it is, so the drawing can be put back on the old puppet. The outline follows image 2, not "
            "image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.")


# ---------- các dạng ----------
# rig: ảnh rig ở refs/<hệ>/<mã>/ (Silhouette.png, RegionMap.png, orig/Nxx.png); rig aola ở <aola>/reskin/pet<id>_parts.
# groups: (mã, tên vi, tên en ngắn, kiểu "giu"/"doi", viền px, mô tả ảnh gốc en, mô tả ảnh gốc vi, kiểm vi, prompt, FRAMING)
# extra: mảnh vẽ riêng không có ảnh gốc (vũ khí...): (mã, tên vi, tên en, viền px, kiểm vi, prompt); Claude gắn vào mảnh khi ghép.
FORMS = [
    {
        "code": "giot_suong_1", "elem": "thuy", "aola": 7,
        "hero": "Giọt Sương", "form": 1, "forms": 3, "form_name": "Giọt Nước",
        "role_vi": "tướng khởi đầu hệ Thủy, dạng 1/3, rig aola #7",
        "design_vi": ("tinh linh nước hiệp sĩ tập sự: đầu tròn bằng nước đội mũ giáp tròn kiểu cute có đôi cánh nhỏ hai bên và "
                      "chùm lông mũ hình giọt nước, giáp ngực bạc trơn, không họa tiết, tay phải nắm thanh kiếm ngắn hơi to so "
                      "với người, găng giáp bạc bọc nắm tay, đuôi nước cuộn, chân đi ủng bạc; mặt quả quyết, cười tự tin"),
        "rig_vi": ("con gốc #7 đứng hai chân, chéo 3/4: đầu to, hai vây tai hai bên đầu chĩa lên, chóp giọt nước trên đỉnh "
                   "cong sang trái, thân nhỏ, hai tay buông (mỗi tay 2 mảnh: bắp tay, cẳng tay liền bàn tay), hai chân, đuôi "
                   "nhỏ ở dưới trái cong lên"),
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature, the player's starter and the first stage of a three-stage Water evolution line: a small WATER SPIRIT who is an APPRENTICE KNIGHT, in the same front three-quarter view and pose as image 1, on a plain white background. An original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head with two growths on its sides and one crest on top, one small body, two arms, two legs, one tail, plus one short sword held in the viewer-right hand; no wings on the body, no extra limbs;
- every joint where it is: the neck hidden under the bottom of the head; the shoulders at the top of the body; the hips at the bottom of the body; the tail joining the back of the body at the lower left; the side growths starting at the sides of the head; the crest standing on top of the head;
- every limb pointing the same way: the arms hang down (viewer-left arm down-left, viewer-right arm down-right) with the hands at their LOWER ends; the legs go straight down with the feet at the BOTTOM, toes pointing down and slightly to the left; the tail tip curls UP at the upper left; the side growths point up and out;
- the body, arms and legs about the size and shape of regions 4, 6, 7, 9 and 10; the whole figure about the same height.

CHANGE (the new look, region by region):
1 the two side growths: two small wing-shaped ornaments of the helmet, like the little wings on a knight's helmet, pointing up and out, silver with a blue edge.
2 head: a big round head made of clear blue water with a soft light-blue face, wearing a cute rounded open-face knight helmet that covers the top and back of the head like a round cap with a short brow rim; big round eyes under the rim; the face shows clearly below the rim.
3 crest: the helmet's plume: a small water-drop shaped plume of blue water standing on top of the helmet, its tip curling up and to the left, about the size of region 3.
4 body: a small round body of blue water with a lighter belly.
5 on the chest: a plain silver breastplate with no emblem, about the size of region 5.
6 viewer-left arm: TOP end = shoulder, a small fist in a silver gauntlet at the BOTTOM end.
7 viewer-right arm: TOP end = shoulder, a small fist at the BOTTOM end gripping the hilt of a short sword that is a little too big for him (an apprentice's sword), the blade pointing down and forward; the fist in a silver gauntlet.
8 tail: a wispy tail of swirling water, a little larger than region 8; its wide end joins the body on the right and its tip curls UP at the upper left.
9 and 10 legs: two short legs, hip at the TOP, small silver boots at the BOTTOM, toes pointing down and slightly to the left.

ATTITUDE: an eager apprentice knight: brave and determined, brows angled down, a small confident smile showing a tiny fang, chest out, ready to fight; cute and small, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4.

COLOURS: clear sky blue and light blue water, silver armour with a few small gold trims, a dark blue water plume; few colours.

AVOID: a human face or human body, a full suit of armour that hides the creature, a cape, a shield, a sword taller than the creature, a water-drop head with a pointed top, horn-shaped fins, a sea shell, rainbow stripes, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view, glossy shine, gradients.""",
        "groups": [
            ("N01", "hai cánh mũ", "helmet wings", "doi", 10,
             "two blue fin-shaped ears", "hai vây tai hình sừng xanh nhạt, chóp có sọc cam và xanh lá; vây trái chĩa lên trái, gốc ở đầu dưới bên phải; vây phải chĩa lên, gốc ở đầu dưới bên trái; khoảng trống giữa là chỗ của đầu",
             """- cánh trái mọc từ đầu dưới bên phải của nó, cánh phải mọc từ đầu dưới bên trái, đúng chỗ gốc cũ;
- hai cánh nhỏ bạc viền xanh, chĩa lên và ra ngoài; không vẽ đầu.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two fin-shaped ears on the sides of a head (the head is not shown). The viewer-left one points up and to the left, its base (where it joins the head) at its lower RIGHT end. The viewer-right one points up, its base at its LOWER left end. Redraw THESE two pieces as the two small helmet wings of image 2 (the approved concept): each grows from its base end, silver feathers with a blue edge, pointing up and out; they may be a little bigger than the old fins.
Do NOT draw: a head, rainbow stripes, a smooth horn shape.""", "base end"),
            ("N02", "đầu, mặt, mũ giáp", "head with helmet", "doi", 10,
             "a round blue water-drop head with a face", "đầu tròn xanh bóng như giọt nước giữa ảnh; hai mắt to ở nửa dưới, má hồng nhạt, miệng nhỏ, vòng lưỡi liềm xanh chanh gần đỉnh",
             """- mép dưới đầu ngang mép dưới cũ (phủ cổ), đỉnh ngang đỉnh cũ;
- mắt, miệng đúng chỗ cũ (chồng lên ảnh 1 để so); mặt quả quyết, cười tự tin lộ răng nanh nhỏ;
- mũ giáp tròn che đỉnh và sau đầu, vành mũ ở chỗ vòng lưỡi liềm cũ; mặt lộ rõ dưới vành;
- không có cánh mũ, không có chùm lông mũ (hai nhóm riêng).""",
             """Image 1 is one group of a 2D cut-out animation puppet (the old design): a big round water-drop head with a face (two eyes, two cheeks, a mouth) and a lime crescent band near the top. Redraw THIS group as the head of image 2 (the approved concept): a round head of clear blue water with a soft light-blue face, wearing the cute rounded open-face knight helmet that covers the top and back of the head; the helmet's short brow rim sits where the lime crescent is; the big round eyes with a determined look and the small confident smile with a tiny fang exactly where the old eyes and mouth are.
Keep the bottom edge of the head at the same height as the old one (the neck goes under it) and the top at about the same height (the plume stands on it).
Do NOT draw: the helmet wings, the plume, a neck, a body, a pointed water-drop top.""", "eyes and mouth"),
            ("N03", "chùm lông mũ", "helmet plume", "doi", 28,
             "a blue water-drop crest, enlarged", "chóp giọt nước xanh trong phóng to khoảng 4 lần, mép dưới tròn (chỗ cắm vào đầu), chóp nhọn cong lên phía trên bên trái",
             """- đáy chùm lông nằm dọc mép dưới cũ (chỗ cắm vào mũ);
- chóp cong lên sang trái như chóp cũ; cỡ như cũ.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a water-drop crest; its lower edge sits in the head and its pointed tip curls up to the upper left. Redraw THIS piece as the helmet plume of image 2 (the approved concept): a water-drop shaped plume of darker blue water, its base along the old lower edge, its tip curling up and to the left like the old tip, about the same size.
Do NOT draw: a head, a helmet, a feather duster.""", "lower edge (the base)"),
            ("N04", "thân và giáp ngực", "body and breastplate", "giu", 28,
             "a drop-shaped blue body with a shell on the chest", "thân xanh hình giọt nước dựng đứng, cổ hẹp ở trên, bụng tròn ở dưới; vỏ sò kem viền đỏ ở ngực",
             """- viền thân như cũ: cổ hẹp ở trên, bụng tròn ở dưới;
- giáp ngực bạc trơn, không họa tiết đúng chỗ và cỡ của vỏ sò;
- không có tay, chân, đầu.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a small body shaped like a drop (narrow neck end at the TOP, round belly at the bottom) and a sea shell on the chest. Redraw THESE pieces as the body of image 2 (the approved concept): the body becomes the small round body of blue water with a lighter belly, same outline; the shell becomes the plain silver breastplate with no emblem, same place and size.
Do NOT draw: arms, legs, a head, a sea shell.""", None),
            ("N05", "tay trái", "viewer-left arm", "giu", 28,
             "a thin blue arm, shoulder at the upper right, hand at the bottom", "tay xanh gầy chéo từ trên phải (vai) xuống dưới trái; bàn tay tròn ở đầu dưới, vòng xanh chanh ở cổ tay",
             """- vai ở đầu trên bên phải, tay chạy xuống trái;
- nắm tay ở **đầu dưới** đeo găng giáp bạc bọc cả nắm tay và cổ tay (chỗ vòng xanh chanh cũ); không tay áo.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a thin arm. Its TOP end (upper right) is the shoulder; it runs down to the left; the round hand is at the BOTTOM end, with a lime band at the wrist. Redraw THESE pieces as the viewer-left arm of image 2 (the approved concept): blue water skin, a small fist at the BOTTOM end in a silver gauntlet that covers the fist and the wrist (where the lime band is).
Do NOT put the hand at the top. Do NOT draw: a sleeve, claws, a body, a weapon.""", None),
            ("N06", "tay phải nắm chuôi kiếm", "viewer-right arm", "giu", 28,
             "a thin blue arm, shoulder at the upper left, hand at the bottom", "tay xanh từ trên trái (vai) chạy xuống rồi cong sang phải; bàn tay tròn ở đầu dưới, vòng xanh chanh ở cổ tay",
             """- vai ở đầu trên bên trái, tay chạy xuống rồi cong sang phải;
- nắm tay ở **đầu dưới** nắm chuôi kiếm, chỉ thấy khúc chuôi trong nắm tay (lưỡi kiếm vẽ riêng ở bước N09);
- găng giáp bạc bọc nắm tay và cổ tay (chỗ vòng xanh chanh cũ); không tay áo.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a thin arm. Its TOP end (upper left) is the shoulder; it runs down and curves to the right; the round hand is at the BOTTOM end, with a lime band at the wrist. Redraw THESE pieces as the viewer-right arm of image 2 (the approved concept): blue water skin, a small fist at the BOTTOM end closed around the grip of the sword (show only the short piece of the grip inside the fist; the rest of the sword is drawn separately), the fist and the wrist in a silver gauntlet (where the lime band is).
Do NOT put the hand at the top. Do NOT draw: the sword's blade or guard, a sleeve, claws, a body.""", None),
            ("N07", "đuôi nước", "tail", "doi", 25,
             "a blue tail, joint edge on the right, tip curling up at the upper left", "đuôi xanh, mép thẳng rộng ở bên phải (chỗ nối thân), quét sang trái, chóp cong lên ở trên bên trái có sọc cam và xanh lá",
             """- mép nối thân vẫn ở **bên phải**, đúng chỗ mép thẳng cũ;
- chóp cong lên ở trên bên trái; to hơn đuôi cũ một chút, không chạm mép ảnh.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a tail. The wide straight edge on the RIGHT is where it joins the body (hidden behind it); it sweeps to the left and its tip curls UP at the upper left, with orange and green stripes at the tip. Redraw THIS piece as the wispy tail of swirling water of image 2 (the approved concept), a little bigger than the old tail.
The joint end stays on the RIGHT, exactly where the old straight edge is; the tip still curls up at the upper left.
Do NOT draw: rainbow stripes, a body, legs.""", "joint edge"),
            ("N08", "hai chân đi ủng", "legs with boots", "giu", 28,
             "two blue leaf-shaped legs", "hai chân xanh hình lá đứng cạnh nhau, đầu rộng ở trên (hông), mũi nhọn ở dưới (bàn chân) chĩa xuống hơi sang trái",
             """- hông ở **đầu trên** (đầu rộng), bàn chân ở **đầu dưới**;
- ủng bạc nhỏ ở đầu dưới, mũi chĩa xuống hơi sang trái ở cả hai chân.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two short legs. Each one has its hip at the TOP (the wide end) and its foot at the BOTTOM (the narrow pointed end, pointing down and slightly to the left). Redraw THESE two pieces as the two short legs of image 2 (the approved concept): blue water skin, small silver boots at the BOTTOM ends, toes pointing down and slightly to the left.
Do NOT put the feet at the top. Do NOT draw: a body, a tail, long armour plates.""", None),
        ],
        "extra": [
            ("N09", "thanh kiếm", "sword", 18,
             """- chỉ thanh kiếm, dựng thẳng: chuôi ở trên, mũi kiếm chĩa xuống;
- kiếm ngắn của hiệp sĩ tập sự như concept: lưỡi bạc, chắn tay vàng, chuôi ngắn, đốc tròn vàng nhỏ; cao khoảng 80% ảnh;
- không có tay, không có con vật.""",
             """Draw ONLY the short sword of image 2 (the approved concept), on its own: standing straight up and down, the hilt at the TOP and the point at the BOTTOM, centred on a plain white 1024 x 1024 canvas, about 80% of the canvas height. An apprentice knight's short sword: a silver blade, a gold crossguard like in the concept, a short grip, a small round gold pommel. It will be put into the creature's fist by the game.
Do NOT draw: a hand, the creature, a scabbard, glowing effects."""),
        ],
        "first": ["N02", "N06"],  # gen thử trước: một nhóm đổi dáng, một nhóm giữ viền
    },
]


def rig_dir(f):
    return ROOT + f"refs/{f['elem']}/{f['code']}/"


def concept_path(code):
    return ROOT + f"inbox/{code}/concept_duyet.png"


def build(f):
    code = f["code"]
    pk = ROOT + f"gui_gpt/{code}/"
    shutil.rmtree(pk, ignore_errors=True)
    os.makedirs(pk)
    save = ROOT + f"inbox/{code}/tai_ve/"
    os.makedirs(save, exist_ok=True)
    rd = rig_dir(f)

    # ----- lượt 1: concept -----
    d1 = pk + "1_concept/"
    os.makedirs(d1)
    a1 = [("01_Silhouette.png", rd + "Silhouette.png", "grey silhouette of the puppet rig",
           "Bóng xám của con gốc trên nền trắng (779 × 937): " + f["rig_vi"]),
          ("02_RegionMap.png", rd + "RegionMap.png", "the same figure split into numbered regions",
           "Cùng hình, tô màu từng vùng và đánh số (779 × 937, nền trắng): 1 vây tai, 2 đầu, 3 chóp, 4 thân, 5 vỏ sò ở ngực, 6 tay trái, 7 tay phải, 8 đuôi, 9 và 10 hai chân"),
          ("03_style_sheet.png", STYLE_SHEET, "eight creatures of the game: a DESIGN reference only (do not copy their glossy rendering or their designs)",
           "Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào"),
          ("04_world_style.png", WORLD_STYLE, "the game's approved hand-drawn map: copy its RENDERING (ink outlines, coloured-pencil hatching), ignore its content",
           "Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung")]
    t1 = ["Read this whole file, then draw ONE image. Do not reply with text only.", "",
          "ATTACHED IMAGES (in the order they are attached; this text file is not counted):"]
    t1 += [f"image {i} = {n}: {en}" for i, (n, _, en, _) in enumerate(a1, 1)]
    t1 += ["", f["concept"].replace("{RENDER}", RENDER).replace("{DESIGN}", DESIGN)]
    open(d1 + "00_instructions.txt", "w", encoding="utf-8", newline="\n").write("\n".join(t1) + "\n")
    for n, src, _, _ in a1:
        shutil.copyfile(src, d1 + n)

    # ----- lượt 2: nhóm mảnh -----
    d2 = pk + "2_nhom_manh/"
    os.makedirs(d2)
    gs = f["groups"]
    a2 = [(f"{i:02d}_{g[0]}.png", rd + f"orig/{g[0]}.png", f"old pieces of group {g[0]}: {g[5]}", g[6]) for i, g in enumerate(gs, 1)]
    ci = len(a2) + 1
    a2.append((f"{ci:02d}_concept.png", concept_path(code), "the approved concept of this creature",
               "concept đã duyệt của dạng này (nền trắng)"))
    have_c = os.path.exists(concept_path(code))
    for n, src, _, _ in a2:
        if os.path.exists(src):
            shutil.copyfile(src, d2 + n)
    order = f["first"] + [g[0] for g in gs if g[0] not in f["first"]] + [e[0] for e in f["extra"]]
    t2 = ["Read this whole file, then draw ONE image. Do not reply with text only.", "",
          "ATTACHED IMAGES (in the order they are attached; this text file is not counted):"]
    t2 += [f"image {i} = {n}: {en}" for i, (n, _, en, _) in enumerate(a2, 1)]
    t2 += ["", "WHAT THIS IS: a creature for a 2D cut-out animation game. Its animation already exists: it moves flat "
           "picture pieces around fixed joints. Each step below redraws ONE group of old puppet pieces as the matching "
           "part of the approved concept, on the same square canvas, so the old animation can play the new drawings. "
           "Inside a step, \"image 1\" means that step's old-pieces image and \"image 2\" means the approved concept "
           f"(attached image {ci}).",
           "Every reply: exactly ONE image for ONE step, a square 1024 x 1024 canvas, plain white background, no text.", "",
           f"ORDER: draw step {order[0]} now and stop. When I say \"next\", draw step {order[1]} and stop: I will check "
           f"both. When I say \"continue\", draw the remaining steps one per reply, each after I say \"next\", in this "
           f"order: {', '.join(order[2:])}.", ""]
    for i, g in enumerate(gs, 1):
        code_g, _, en, kind, n, _, _, _, prompt, joint = g
        frame = KEEP_FRAME if kind == "giu" else free_frame(joint)
        t2 += [f"=== STEP {code_g} ({en}) ===",
               f"In this step: image 1 = attached image {i} ({a2[i - 1][0]}); image 2 = attached image {ci} ({a2[ci - 1][0]}).",
               prompt, "", frame, LINE.format(n=n), ""]
    for code_e, _, en, n, _, prompt in f["extra"]:
        t2 += [f"=== STEP {code_e} ({en}) ===",
               f"In this step: image 2 = attached image {ci} ({a2[ci - 1][0]}); there is no image 1.",
               prompt, "", LINE.format(n=n).replace("not image 1's glossy vector look", "as in the concept"), ""]
    open(d2 + "00_instructions.txt", "w", encoding="utf-8", newline="\n").write("\n".join(t2) + "\n")

    # ----- HUONG_DAN.md -----
    g_ = [f"# Gói gửi GPT: {f['hero']} dạng {f['form']}/{f['forms']} ({f['form_name']}, `{code}`)", "",
          f"{f['role_vi'][:1].upper() + f['role_vi'][1:]}. Thiết kế: {f['design_vi']}. Quy trình: `{W(ROOT + 'QUY_TRINH.md')}`.", "",
          "Mỗi lượt: mở thư mục con, chọn **hết file** (Ctrl+A), kéo vào ô chat ChatGPT rồi gửi. Không cần dán prompt: GPT đọc "
          "`00_instructions.txt` rồi vẽ. ChatGPT không cho gửi khi ô chữ trống thì gõ `go`; GPT chỉ trả lời chữ thì gõ `draw it`.", "",
          f"Ảnh GPT trả về: tải về để vào `{W(save)}`, **không cần đổi tên**. Claude xem rồi đặt tên và chép vào đúng chỗ.", "",
          "Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.", "",
          "## Lượt 1: concept", "",
          f"Thư mục: `{W(d1)}`. Mở **chat mới**, kéo hết {len(a1) + 1} file vào, gửi. GPT vẽ một ảnh cả con trên rig.", "",
          "| File trong thư mục | Là ảnh gốc nào | Trông như thế nào |", "|---|---|---|",
          "| `00_instructions.txt` | lời dặn và prompt | chữ tiếng Anh: thứ tự ảnh, giữ gì của rig, đổi gì từng vùng, nét vẽ |"]
    g_ += [f"| `{n}` | `{W(src)}` | {vi} |" for n, src, _, vi in a1]
    g_ += ["", f"Xong thì nhắn Claude \"duyệt concept {code}\". Duyệt xong Claude lưu `{W(concept_path(code))}` và chép vào gói lượt 2.", "",
           "## Lượt 2: nhóm mảnh", "",
           f"Thư mục: `{W(d2)}`. "
           + (f"Có đủ file. Cùng chat với lượt 1 hoặc chat mới, kéo hết {len(a2) + 1} file vào, gửi." if have_c else
              f"**Chưa dùng được:** thiếu `{a2[ci - 1][0]}`, Claude chép vào sau khi duyệt concept."), "",
           f"1. GPT vẽ {order[0]}. Gõ `next`: GPT vẽ {order[1]}. Nhắn Claude \"soi thử {code}\".",
           f"2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: {', '.join(order[2:])}.",
           f"3. Đủ ảnh thì nhắn Claude \"ghép {code}\".", "",
           "Nếu ChatGPT báo quá nhiều file trong một tin nhắn: gửi `00_instructions.txt`, ảnh concept và 4 ảnh nhóm đầu trước, các ảnh còn lại ở tin nhắn sau.", "",
           "| File trong thư mục | Là ảnh gốc nào | Trông như thế nào |", "|---|---|---|",
           "| `00_instructions.txt` | lời dặn và prompt | chữ tiếng Anh: thứ tự ảnh, thứ tự vẽ, prompt từng nhóm |"]
    g_ += [f"| `{n}` | `{W(src)}` | {vi}{'' if os.path.exists(src) else ': **chưa có**, sinh ở lượt 1'} |" for n, src, _, vi in a2]
    g_ += ["", "Kiểm từng ảnh trước khi lưu:", ""]
    for g in gs:
        g_ += [f"**{g[0]} {g[1]}** ({'giữ viền' if g[3] == 'giu' else 'đổi dáng'}, viền khoảng {g[4]} px):", g[7], ""]
    for e in f["extra"]:
        g_ += [f"**{e[0]} {e[1]}** (vẽ riêng, Claude gắn vào bàn tay khi ghép; viền khoảng {e[3]} px):", e[4], ""]
    g_ += ["## GPT vẽ sai thì gửi thêm (cùng chat)", "",
           "| Sai | Gửi thêm |", "|---|---|",
           "| Nét số bóng loáng, chuyển sắc | `Render it hand-drawn like the map: dark-brown ink outlines, flat warm colours with coloured-pencil hatching; no glossy shine, no gradients.` |",
           "| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |",
           "| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |",
           "| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile with a tiny fang; not a big happy grin.` |",
           "| Vẽ cả con hoặc thêm phần ngoài nhóm | `Only the pieces of image 1, nothing else.` |",
           "| Mảnh lệch chỗ, xoay, đổi cỡ | `Put every piece back exactly where it is in image 1: same position, size and angle on the same 1024 x 1024 canvas.` |",
           "| Bàn tay, bàn chân ở sai đầu | `The hand/foot is at the BOTTOM end; the TOP end is the shoulder/hip.` |",
           "| Viền mảnh quá mảnh hoặc quá dày | `Make the dark-brown outline about <N> px thick, the same on every edge.` (N ghi ở từng nhóm trên) |",
           "| Nền xám, có bóng đổ, có ô lưới | `Plain pure white background, no shadow, nothing else.` |", "",
           f"Gói này sinh từ `{W(ROOT + 'build.py')}`; sửa prompt ở đó rồi chạy lại.", ""]
    open(pk + "HUONG_DAN.md", "w", encoding="utf-8", newline="").write("\n".join(g_))
    return pk, sorted(os.listdir(d1)), sorted(os.listdir(d2))


if __name__ == "__main__":
    for f in FORMS:
        print(*build(f))
