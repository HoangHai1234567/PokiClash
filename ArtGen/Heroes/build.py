# Sinh gói gửi GPT cho hình tướng: ArtGen/Heroes/gui_gpt/<mã>/ (quy trình: QUY_TRINH.md).
# Cách làm: vẽ con mới đè lên rig vector của aola (người dùng: "vẫn phải dùng rig cũ", 2026-11-02) để giữ animation aola.
# Mỗi dạng 2 lượt, mỗi lượt một file prompt (tiếng Anh): người dùng chỉ gửi GPT đường dẫn file đó (người dùng dặn 2026-11-03).
# File mở đầu bằng danh sách ảnh mẫu kèm đường dẫn đầy đủ (GPT tự mở), rồi chỗ GPT tự lưu ảnh (inbox/<mã>/tai_ve/). Kèm HUONG_DAN.md
# (tiếng Việt: file prompt từng lượt, ảnh mẫu trông ra sao, lưu đâu, kiểm gì, câu sửa nhanh).
#   luot_1_concept.txt:   concept cả con trên rig (bóng xám, bản đồ vùng) + tờ mẫu thiết kế (aola) + ảnh mốc nét vẽ (bản đồ).
#   luot_2_nhom_manh.txt: từng nhóm mảnh vẽ đè lên hình gốc của nhóm (refs/<hệ>/<mã>/orig/Nxx.png) + concept đã duyệt; một ảnh
#                         mỗi bước. Chỉ dựng khi đã có concept duyệt (inbox/<mã>/concept_duyet.png).
# Nét: vẽ tay trên giấy bằng bút mực, tô chì màu và sáp màu như bản đồ world_style.png; tô phẳng, không bóng, không ánh sáng
# (người dùng 2026-11-04). Thiết kế học từ tướng aola. Viền trắng giấy xé do game vẽ (shader), GPT không vẽ.
# Chạy: py -3 -I ArtGen/Heroes/build.py. Đường dẫn tính từ chỗ đặt file này nên chạy được trên cả hai máy. Ảnh mẫu aola:
# tools/make_refs.py.
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/"
STYLE_SHEET = ROOT + "refs/style/style_sheet.png"
WORLD_STYLE = os.path.normpath(ROOT + "../Islands/refs/world_style.png").replace("\\", "/")


def W(p):
    return p.replace("/", "\\")


# ---------- khối dùng chung ----------
# Luật tướng (người dùng 2026-11-04, áp cho mọi tướng: concept, mảnh, vũ khí, hiệu ứng, mặt tướng): vẽ tay trên giấy bằng bút
# mực, tô chì màu và sáp màu; "không bóng", "không ánh sáng": mỗi vùng một màu đều, nét chì sáp chỉ là vân, không mảng sáng tối,
# không bóng đổ, không điểm sáng (chừa một chấm sáng nhỏ trong mắt). Thay luật 2026-11-03 (bóng chì gạch chéo, vài điểm sáng).
STYLE_ANCHOR = ROOT + "refs/style_anchor.png"
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the figure, on "
        "the ground or on the background), no white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no "
        "3D look. The only white allowed is one small catchlight dot in each eye. A darker tone appears only where the design "
        "itself has a darker colour (for example the inside of a cape).")
RENDER = ("DRAWING STYLE (the game's own look: copy the line and the colouring of the game's hand-drawn map): drawn by hand ON "
          "PAPER by a professional storybook illustrator: outlines in dark-brown ink pen (#2B2118), fairly even weight, slightly "
          "wobbly like a real pen; every area coloured by hand with COLOURED PENCILS and WAX CRAYONS, the strokes clearly visible "
          "as loose diagonal hatching, which gives the soft crayon-on-paper texture; clean and appealing, neither a crude kid "
          "scribble nor overly detailed.\n" + FLAT + "\n"
          "Plain white background around the figure: no paper colour or paper grain outside it, no white border or sticker "
          "outline around the figure or its parts (the game adds that itself).")
DESIGN = ("DESIGN (learn it from the game's creatures in the style sheet): an appealing original creature in the classic "
          "Japanese monster-collecting look: a clear, chunky silhouette that reads at small size, big expressive eyes, simple "
          "readable shapes, few details. Take only the design approach from those creatures, never their glossy rendering "
          "and never their designs.")
# dòng tướng dạng người (Tiểu Y): cách thiết kế như trên nhưng là nhân vật, không phải sinh vật
DESIGN_CHIBI = ("DESIGN (learn the approach from the creatures in image 3): a character in the classic Japanese monster-collecting "
                "game look: a clear, chunky silhouette that reads at small size, big expressive eyes, simple readable shapes, few "
                "details. Take only the design approach from image 3, never its glossy rendering and never its designs.")
LINE = ("LINE AND COLOUR: the game's hand-drawn look of image 2, not image 1's glossy vector look: drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about {n} px thick on this 1024 canvas, the same weight on every edge, slightly "
        "wobbly like a real pen; every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal "
        "hatching (strokes thinner than the outline), kept inside the outline.\n"
        "FLAT COLOUR, NO LIGHT, NO SHADOW: each area one even colour, the strokes are texture only. No shading, no darker side, "
        "no shadows of any kind, no white highlights or shine spots (only a small catchlight dot in an eye), no gloss, no glow, "
        "no gradients; no paper colour or paper grain outside the drawing, no white border around the pieces.\n"
        "Plain white background. Only this group. No text.")
FLAT_FIX = ("Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, "
            "no white highlights or shine (only a small catchlight dot in each eye), no glow, no gradients.")
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
        "regions_vi": "1 vây tai, 2 đầu, 3 chóp, 4 thân, 5 vỏ sò ở ngực, 6 tay trái, 7 tay phải, 8 đuôi, 9 và 10 hai chân",
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
    {
        "code": "giot_suong_2", "elem": "thuy", "aola": 8,
        "hero": "Giọt Sương", "form": 2, "forms": 3, "form_name": "Tiên Sương",
        "role_vi": "tướng khởi đầu hệ Thủy, dạng 2/3, rig aola #8",
        "design_vi": ("hiệp sĩ nước, lớn lên từ dạng 1: mũ giáp tròn như dạng 1 nhưng mỗi bên có hai lông cánh bạc, chùm lông "
                      "mũ thành bọt nước lớn bốn mũi trên đế vàng, giáp cổ bạc có hình giọt nước vàng, giáp ngực bạc, áo choàng "
                      "nước che tay trái, tay phải đeo găng bạc cầm kiếm hiệp sĩ dài hơn kiếm dạng 1 (chắn tay hình hai cánh "
                      "vàng), đuôi nước dài uốn chữ S có vây chẻ đôi, hai chân nhọn bọc giáp (lơ lửng); mặt quả quyết"),
        "rig_vi": ("con gốc #8 lơ lửng, chéo 3/4: đầu tròn to, bốn vây hai bên đầu (mỗi bên hai vây), mào lá to trên cuống ở "
                   "đỉnh đầu xòe lên trái, chuỗi vỏ sò ở cổ, thân nhỏ, tay trái là vây lớn quét xuống trái (bốn mũi), tay phải "
                   "gầy buông xuống phải (ba mũi ở đầu dưới), hai chân nhọn không bàn chân, đuôi dài vòng xuống trái rồi quét "
                   "sang phải dưới thân, cuối đuôi có vây chẻ đôi"),
        "regions_vi": ("1 bốn vây hai bên đầu, 2 mào trên đỉnh, 3 đầu, 4 thân, 5 chuỗi vỏ sò ở cổ, 6 tay trái (vây lớn), "
                       "7 tay phải, 8 đuôi, 9 và 10 hai chân"),
        "prev": [("giot_suong_1", "the approved FIRST stage of this evolution line: keep its colours, helmet, face, armour and "
                                  "drawing style",
                  "dạng 1, tinh linh nước hiệp sĩ tập sự đội mũ giáp tròn có hai cánh nhỏ và chùm lông mũ giọt nước, giáp "
                  "ngực bạc, găng bạc, cầm kiếm ngắn chắn tay vàng, đuôi nước cuộn. Giữ màu, mũ, mặt, giáp, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: the SECOND stage of a three-stage Water evolution line whose first stage is image 5. The little water-spirit apprentice knight of image 5 has grown into a full WATER KNIGHT: taller, braver, with a real knight's sword; still a small cute creature, not a human. Same front three-quarter view and pose as image 1, on a plain white background. Not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one big round head with four growths on its sides (two on each side) and one large crest on top, a collar piece at the neck, one small body, two arms, two legs, one long tail, plus one sword held in the viewer-right hand; no wings on the body, no extra limbs;
- every joint where it is: the neck hidden under the bottom of the head, behind the collar; the shoulders at the top of the body; the hips at the bottom of the body; the tail starting behind the body at the lower left; the side growths starting at the sides of the head; the crest standing on a short stem on top of the head;
- every part pointing the same way: on the viewer-left side of the head the upper growth points up and out to the upper left and the lower one points out to the left; on the viewer-right side the upper growth points straight up and the lower one points out to the right; the crest fans up and to the left; the viewer-left arm sweeps down to the left; the viewer-right arm hangs down to the right with the hand at its LOWER end; the two legs taper straight down to points (the creature hovers, no feet on the ground); the tail loops down to the left, sweeps right under the body and ends in a two-lobed fin at the lower right;
- the head, body, arms and legs about the size and shape of regions 3, 4, 6, 7, 9 and 10; the whole figure about the same height.

CHANGE (the new look, region by region):
1 the four side growths: four silver feathers of a winged knight's helmet, two on each side: the small helmet wings of image 5 grown into two-feathered wings, silver with a blue edge, each feather pointing the way its region points.
2 crest: the helmet's plume grown big: a splashing plume of dark blue water with four pointed tips fanning up and to the left, standing in a short gold socket on top of the helmet, about the size of region 2.
3 head: a big round head of clear blue water with a soft light-blue face, wearing the same cute rounded open-face knight helmet as image 5 (a silver dome over the top and back of the head, a short brow rim, a small gold diamond on the brow); the face shows clearly below the rim, with big round eyes about halfway down the head.
4 body: a small body of blue water wearing a plain silver breastplate with a thin gold trim along its lower edge.
5 at the neck: a round silver gorget (collar armour) with a gold water-drop emblem in its middle and two small round rivets at its sides, about the size and place of region 5.
6 viewer-left arm: hidden under a short knight's cape of flowing blue water that hangs from the viewer-left shoulder and sweeps down to the left; its hem ends in pointed tips like the edge of region 6; no hand shows.
7 viewer-right arm: TOP end = shoulder, a fist in a silver gauntlet with a flared cuff at the BOTTOM end, gripping a knight's sword: longer than the apprentice sword of image 5 but still shorter than the creature; a silver blade pointing down and forward, a gold crossguard shaped like two small wings, a blue grip, a small round gold pommel.
8 tail: a long tail of swirling water following region 8: it loops down to the left, sweeps right under the body and ends in a two-lobed water fin at the lower right, both lobes pointing left.
9 and 10 legs: two short tapering legs of blue water, hip at the TOP, each ending in a pointed silver greave at its BOTTOM tip; no feet: the knight hovers.

ATTITUDE: a brave young water knight, proud of its first real sword: brows angled down, a confident smile showing a tiny fang, chest out, sword ready; cute and small, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is the approved first stage of this line: keep its colours, helmet, face, armour and drawing style, so both stages read as the same creature growing up.

COLOURS: as in image 5: clear sky blue and light blue water, silver armour with a few small gold trims, dark blue water for the plume and the cape's inside; few colours.

AVOID: a human face or human body, a full suit of armour that hides the creature, a shield, a sword taller than the creature, a sea shell, beads, a leafy crest, a tongue sticking out, bubbles, rainbow stripes, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view, glossy shine, gradients.""",
        "groups": [
            ("N01", "bốn cánh mũ", "four helmet-wing feathers", "doi", 15,
             "four detached side fins: upper-left points up-left, lower-left points left, upper-right points up, lower-right points right",
             "Bốn vây tách rời hai bên đầu (1024 × 1024, nền trắng): trên trái dài chĩa lên trái, dưới trái ngang sang trái, trên phải chĩa lên, dưới phải ngang sang phải; đầu gần tâm là gốc gắn vào mũ",
             "Giữ bốn gốc khớp ở phía gần tâm ảnh. Mỗi vây thành một lông cánh mũ bạc viền xanh, đúng hướng và gần đúng cỡ cũ; không vẽ đầu, mào hay cánh trên thân.",
             "Image 1 has exactly FOUR separate old side fins from a puppet head. Redraw exactly FOUR separate silver knight-helmet feathers edged blue, matching the four positions, roots and directions: viewer-left upper up-left, viewer-left lower left, viewer-right upper straight up, viewer-right lower right. The end nearer the centre of the canvas is the ROOT joining the head; keep every root exactly there. Match image 2's helmet-wing design and pencil texture. Do NOT draw a head, plume, body wings, rainbow bands or any extra feathers.", "each inner root"),
            ("N02", "chùm lông mũ", "helmet water plume", "doi", 25,
             "one large four-point crest with a short stem at bottom-right",
             "Mào lớn (1024 × 1024, nền trắng): bốn mũi xòe lên và sang trái, cuống ngắn ở dưới bên phải cắm vào đỉnh đầu; phần rỗng giữa các mũi phải còn rõ",
             "Giữ chân cuống ở dưới phải, bốn mũi và khoảng trống giữa mũi; đổi thành nước xanh đậm, ổ cắm vàng ngắn ở chân. Không vẽ mũ hoặc đầu.",
             "Image 1 is ONE large four-tipped crest. Its short stem at the LOWER RIGHT joins the top of the helmet; all four tips fan upward and to the left. Redraw it as image 2's dark-blue splashing water plume, with a short gold socket at the stem. Preserve the stem position and the distinct four-point silhouette and gaps, at about the same size. Do NOT draw a helmet, head, leaves or separate floating droplets.", "lower-right stem"),
            ("N03", "đầu, mặt và mũ", "head face and helmet", "doi", 15,
             "one large round water head with two eyes and mouth halfway down, no side fins or crest",
             "Đầu tròn (1024 × 1024, nền trắng): hai mắt ở nửa dưới, miệng ở giữa dưới; mép dưới là cổ giấu sau giáp cổ; bốn cánh mũ và mào thuộc nhóm khác",
             "Mặt xanh nhạt, mắt to mày xếch, cười tự tin lộ một nanh; mũ bạc tròn che đỉnh và sau đầu, vành ngắn, kim cương vàng giữa trán; đáy đầu đúng chỗ cũ. Không vẽ cánh mũ, mào hay cổ.",
             "Image 1 is ONE big round water head. Redraw it as image 2's clear sky-blue round head with pale-blue face and silver open-face rounded knight helmet: dome over top and rear, short brow rim, tiny gold diamond centred on the brow. Keep the old head's size, position, lower neck edge and the two eyes and mouth in the same approximate places. Big expressive eyes, determined angled brows, small confident smile with one tiny fang. Do NOT draw helmet side wings, plume, collar, body, tongue or a pointed drop-shaped top.", "bottom neck edge"),
            ("N04", "thân, giáp cổ và giáp ngực", "body gorget and breastplate", "giu", 24,
             "one narrow-necked small water body with a large shell at its upper front and small beads at the neck",
             "Thân xanh bụng tròn, cổ hẹp ở trên; vỏ sò lớn ở ngực, hai hạt tròn hai bên cổ (1024 × 1024, nền trắng). Viền thân phải giữ vì rig xoay thân quanh cổ và hông",
             "Thay vỏ sò bằng giáp cổ tròn bạc có giọt vàng giữa và hai đinh tán nhỏ, dưới là giáp ngực bạc trơn viền vàng mảnh. Giữ viền ngoài thân; không vẽ đầu, tay, chân, vỏ sò.",
             "Image 1 contains the puppet's small blue body, narrow neck at TOP, round belly at BOTTOM, an oversized shell at the upper front, and two round neck beads. Keep the BODY OUTER CONTOUR, canvas position and scale. Redraw the shell and beads as image 2's round silver gorget at the neck, a small gold water-drop emblem in its middle, two small round rivets at the sides, and a plain silver breastplate below with thin gold trim on its lower edge. Blue-water body remains visible. Do NOT draw a shell, necklace, head, arms, legs or sword.", "top neck and lower hips"),
            ("N05", "tay trái dưới áo choàng", "viewer-left cape arm", "giu", 25,
             "a broad left-sweeping arm fin: narrow shoulder at upper right, three pointed hem tips at lower left",
             "Tay/vây lớn bên trái người xem (1024 × 1024, nền trắng): đầu hẹp ở trên phải là vai, quét xuống trái; đầu rộng dưới trái xẻ ba mũi. Không có bàn tay lộ ra",
             "Giữ viền ngoài và vị trí vai; phủ thành áo choàng nước xanh, lòng xanh đậm, vạt ba mũi như cũ. Không vẽ bàn tay, găng hay thân.",
             "Image 1 is the viewer-LEFT arm as a broad fin. Its narrow UPPER RIGHT end is the SHOULDER; it sweeps down to the left and ends in THREE pointed tips at the LOWER LEFT. Keep its OUTER CONTOUR, scale, position, shoulder joint and three-tip hem. Redraw its surface as the short flowing blue-water knight cape in image 2, with deeper blue inside and simple pencil hatching. The arm is hidden under the cape; NO hand is visible. Do NOT draw a fist, gauntlet, torso, unrelated wings or rainbow stripes.", "upper-right shoulder"),
            ("N06", "tay phải nắm kiếm", "viewer-right sword arm", "giu", 28,
             "a long fin arm: narrow shoulder at upper left, broad three-point lower end at bottom right",
             "Tay bên phải người xem (1024 × 1024, nền trắng): đầu hẹp ở trên trái là vai, chạy xuống phải; đầu dưới phải là bàn tay ba mũi (không phải vai); kiếm chưa có trong ảnh gốc",
             "Giữ viền và vị trí vai, tay xanh và găng bạc bao đầu dưới, nắm đoạn chuôi xanh ở đầu dưới. Kiếm đầy đủ vẽ riêng N09; không vẽ lưỡi hoặc chắn tay ở nhóm này.",
             "Image 1 is the viewer-RIGHT arm. Its narrow UPPER LEFT end is the SHOULDER; its broad THREE-TIPPED LOWER RIGHT end is the HAND, never another shoulder. Keep the original OUTER CONTOUR, scale, position and shoulder joint for animation. Redraw as image 2's blue-water arm with a silver gauntlet and flared cuff enclosing the BOTTOM hand; the fist grips only a short blue grip segment. The full sword is separate N09. Do NOT draw sword blade, crossguard, a hand at the top, extra limb, body or rainbow colors.", "upper-left shoulder and lower-right hand"),
            ("N07", "đuôi nước vây chẻ đôi", "long water tail", "doi", 20,
             "a long S-loop tail with broad joint at upper right and a two-lobed fin at lower right, both lobes pointing left",
             "Đuôi chữ S dài (1024 × 1024, nền trắng): mép rộng trên phải nối sau thân, vòng xuống trái rồi quét ngang phải, cuối đuôi chẻ hai vây ở dưới phải cùng chĩa trái",
             "Giữ mép nối trên phải và đường vòng chữ S, hai thùy chĩa trái ở cuối; đổi thành nước xanh trời/xanh đậm như concept. Không vẽ chân hay thân.",
             "Image 1 is ONE long S-loop tail. Its broad UPPER RIGHT end joins behind the lower body, then it loops down-left, sweeps right underneath, and ends at the LOWER RIGHT in TWO fin lobes, BOTH pointing LEFT. Keep the joint edge exactly where it is and preserve the loop and two-lobe ending at about the same scale. Redraw as image 2's swirling clear-blue water tail with a darker-blue stream inside and hand-drawn pencil shading. Do NOT draw extra fins, legs, body or rainbow-red tips.", "broad upper-right joint edge"),
            ("N08", "hai chân nhọn", "two pointed hovering legs", "giu", 40,
             "two separate tapering legs, broad hip at top, pointed end at bottom, no feet",
             "Hai chân rời (1024 × 1024, nền trắng): mỗi chân gốc rộng ở trên là hông, mũi nhọn ở dưới; chân phải theo người xem cong nhẹ sang trái ở chóp, không có bàn chân đặt đất",
             "Giữ viền từng chân, gốc hông và hướng chóp; tô nước xanh, giáp ống chân bạc ở đầu dưới, không vẽ bàn chân hay ủng rời.",
             "Image 1 has exactly TWO separate short tapering legs. The broad TOP end of each is its HIP; the pointed BOTTOM end is its hovering leg tip. Keep each leg's OUTER CONTOUR, canvas position, size, hip and downward direction. Redraw the upper parts as blue water and the lower pointed tips as simple silver greaves, matching image 2. The viewer-right tip bends slightly left. No feet touch a floor. Do NOT draw separate boots, body, tail, extra leg or feet at the top.", "both top hips"),
        ],
        "extra": [
            ("N09", "thanh kiếm hiệp sĩ", "knight sword", 20,
             "Vẽ riêng một thanh kiếm đứng dọc trên nền trắng 1024 × 1024: chuôi và đốc ở trên, mũi ở dưới; lưỡi bạc ngắn hơn cả con, chắn tay vàng hình hai cánh, chuôi xanh, đốc tròn vàng; không có bàn tay.",
             "Draw ONLY the full knight sword from image 2, vertically on its own on a plain white 1024 x 1024 canvas. Pommel and blue grip at the TOP, blade tip at the BOTTOM. Silver blade, small gold crossguard shaped as two wings, small round gold pommel. Longer than the first-stage apprentice sword but still shorter than this creature, about 75% of the square's height. The game will attach it to the viewer-right fist. Do NOT draw the hand, creature, scabbard, glow or background effects."),
        ],
        "first": ["N03", "N06"],
        # vẽ lại sau khi ghép (lượt 3): N06 lần đầu giữ ba mũi vây cũ ở đầu dưới nên găng thành ba miếng nhọn, nắm tay quay mặt ra
        # trước, chuôi kiếm vẽ sẵn chĩa thẳng xuống (lệch với kiếm gắn vào), tay xanh đậm (người dùng: "tay bị lỗi", 2026-11-03)
        "redo": [
            {"code": "N06", "vi": "tay phải cầm kiếm", "en": "viewer-right sword arm", "n": 28,
             "old_en": "a long fin arm: narrow shoulder at upper left, broad three-point lower end at bottom right",
             "old_vi": "Tay bên phải người xem của con gốc (1024 × 1024, nền trắng): đầu hẹp ở trên trái là vai, chạy xuống phải; đầu dưới rộng xẻ ba mũi là bàn tay",
             "why_vi": "lần trước găng thành ba miếng nhọn quanh nắm tay, chuôi kiếm vẽ sẵn chĩa thẳng xuống nên lệch với kiếm gắn vào, tay xanh đậm",
             "check_vi": """- vai (đầu hẹp trên trái) đúng chỗ cũ, tay chạy xuống phải như cũ;
- tay xanh trời như thân trong concept, găng bạc có cổ loe viền vàng ở cổ tay;
- đầu dưới là **nắm tay tròn nhìn nghiêng** như concept, không còn ba mũi nhọn, không có miếng nhọn quanh nắm tay;
- **không có chuôi, núm, chắn tay hay lưỡi kiếm** (kiếm gắn sau nắm tay khi ghép).""",
             "prompt": """Image 1 is one piece of a 2D cut-out animation puppet (the old design): the creature's viewer-RIGHT arm. Its narrow UPPER LEFT end is the SHOULDER (it hides behind the body); the arm runs down and to the right; its broad LOWER end is the HAND. Redraw THIS piece as the sword arm of image 2 (the approved concept): a sky-blue water arm (the same light blue as the concept's body, not dark blue), a silver gauntlet with a flared gold-trimmed cuff at the wrist, and at the BOTTOM end a round, closed silver fist seen from the side like the concept's fist, knuckles towards viewer-right. The game slips the sword in BEHIND the fist (the pommel shows above the fist, the guard and blade below it), so draw the fist closed around nothing visible.
Do NOT draw: the sword or any part of it (no grip, no pommel, no guard, no blade), the three pointed tips of the old hand, pointed flaps, spikes or claws around the fist, a sleeve, a body.""",
             "frame": """FRAMING: the same square canvas; the arm keeps its place, length and direction from image 1 and its shoulder end (the narrow upper-left end) stays exactly where it is, so the drawing can be put back on the old puppet. The hand end does NOT keep image 1's three pointed tips: it becomes the round fist of image 2, about as big as the old hand end or a little smaller."""},
        ],
    },
    {
        "code": "giot_suong_3", "elem": "thuy", "aola": 9,
        "hero": "Giọt Sương", "form": 3, "forms": 3, "form_name": "Sương Long",
        "role_vi": "tướng khởi đầu hệ Thủy, dạng 3/3, rig aola #9",
        "design_vi": ("rồng nước hiệp sĩ: rồng bốn chân bằng nước trong, nhìn nghiêng quay phải, đội mũ giáp bạc như dạng 1 "
                      "(vành ngắn, hình thoi vàng trên trán), mào sáu vây nước viền bạc (cánh mũ dạng 1 lớn thành mào rồng), "
                      "giáp cổ vảy bạc có huy hiệu giọt nước vàng, giáp ngực bạc, giáp ống chân bạc, móng ngắn, đuôi dài cuối "
                      "đuôi là hai vây hình lưỡi kiếm (kiếm tập sự thành lưỡi đuôi); mặt quả quyết, oai mà vẫn dễ thương"),
        "rig_vi": ("con gốc #9 bốn chân nhìn nghiêng, quay sang phải, ngồi thẳng: cổ dài vươn lên, đầu ở trên bên phải mõm "
                   "chĩa phải, sáu vây mào trên đầu (bốn vây dài quét ra sau lên trái, hai vây nhỏ chĩa thẳng lên), chuỗi hạt và vỏ sò chéo trên ngực, hai chân trước "
                   "thẳng xuống đất (chân gần to, chân xa sau nó), một chân sau, đuôi dài quét xuống trái sát đất có hai vây "
                   "ở cuối"),
        "regions_vi": ("1 vây mào, 2 đầu, 3 cổ và thân, 4 chuỗi hạt và vỏ sò, 5 chân trước gần, 6 chân trước xa, 7 chân sau, "
                       "8 mẩu nhỏ ở bàn chân trước gần, 9 đuôi"),
        "prev": [("giot_suong_1", "the approved FIRST stage of this evolution line: keep its colours, helmet, face, armour and "
                                  "drawing style",
                  "dạng 1, tinh linh nước hiệp sĩ tập sự đội mũ giáp tròn có hai cánh nhỏ và chùm lông mũ giọt nước, giáp "
                  "ngực bạc, găng bạc, cầm kiếm ngắn chắn tay vàng, đuôi nước cuộn. Giữ màu, mũ, mặt, giáp, nét vẽ"),
                 ("giot_suong_2", "the approved SECOND stage of this evolution line: keep its colours, helmet, face, gorget, "
                                  "armour and drawing style",
                  "dạng 2, hiệp sĩ nước lơ lửng: mũ giáp tròn mỗi bên hai lông cánh bạc, chùm lông mũ nước xanh đậm trên đế "
                  "vàng, giáp cổ bạc có giọt nước vàng, giáp ngực viền vàng, áo choàng nước che tay trái, kiếm chắn tay hình "
                  "hai cánh vàng, hai chân nhọn bọc giáp, đuôi nước chữ S vây chẻ đôi. Giữ màu, mũ, mặt, giáp cổ, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: the THIRD and final stage of a three-stage Water evolution line whose first two stages are image 5 and image 6. The little apprentice knight of image 5, who grew into the water knight of image 6, has become a WATER DRAGON KNIGHT: a proud four-legged dragon made of clear water, still wearing its knight's helmet and armour, seen from the side facing viewer-right, in the same pose as image 1, on a plain white background. Strong and noble but still cute and chunky, never scary; not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head facing right with a crest of six fins on its top and back, one long neck rising from one big body, a collar piece hanging across the chest, two front legs (a near one and a far one just behind it), one hind leg, one long tail; no wings, no arms, no hands, no weapon held, no extra limbs;
- every joint where it is: the head on top of the neck at the upper right; the crest fins growing from the top and back of the head; the neck rising from the front of the body; the front legs starting under the chest; the hind leg starting at the lower back of the body; the tail starting at the back of the body at the lower left;
- every part pointing the same way: the head and its short snout face right; four long crest fins sweep up and back to the upper left and two small ones on top point straight up; the front legs go straight down to the ground with the feet at the BOTTOM; the hind leg goes down to the ground with the foot at the BOTTOM; the tail sweeps down and to the left along the ground and ends in two fins pointing left;
- the head, neck, body and legs about the size and shape of regions 2, 3, 5, 6 and 7; the whole figure about the same size.

CHANGE (the new look, region by region):
1 crest: six fins of blue water edged in silver (four long swept-back ones, two small upright ones): the helmet-wing feathers of images 5 and 6 grown into a dragon's crest, each fin pointing the way its region points.
2 head: a rounded dragon head of clear blue water facing right with a short snout, wearing a cute silver knight helmet like the one in images 5 and 6 (a dome over the top and back of the head, a short brow rim, a small gold diamond on the brow); one big round determined eye under the rim; a small confident closed smile with a tiny fang.
3 neck and body: a long strong neck and a big rounded body of clear blue water with a light-blue belly and chest, deeper blue along the back; a plain silver breastplate on the front of the chest under the neck.
4 across the chest: a silver gorget of small round silver scales running from the upper left down to the right, ending in a gold water-drop medallion like the one on image 6's gorget, where region 4's big round end is, about the same size.
5 near front leg: TOP end = shoulder, foot at the BOTTOM: a thick leg of blue water with a silver greave on the lower leg and three short pale claws at the bottom.
6 far front leg: the same as the near one, a little narrower, just behind it.
7 hind leg: TOP end = hip, foot at the BOTTOM: a shorter leg of deeper blue water with a silver knee plate and a pointed foot.
8 region 8 is a tiny sliver at the near front foot: treat it as part of leg 5.
9 tail: a long tail of swirling water sweeping down and to the left along the ground, ending in two broad fins shaped like sword blades, silver-edged, pointing left: the knight's sword of images 5 and 6 has become the dragon's tail blades.

ATTITUDE: a proud, battle-ready water dragon knight: head held high, a determined eye with the brow angled down, chest out, ready to charge; noble and strong but cute and chunky, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Images 5 and 6 are the approved first and second stages of this line: keep their colours, helmet, face, armour and drawing style, so all three stages read as the same creature growing up.

COLOURS: as in images 5 and 6: clear sky blue, light blue and some deeper blue water, silver armour with a few small gold trims; few colours.

AVOID: a human, arms or hands, a sword held anywhere, wings on the back, a sea shell, beads, a pearl necklace, rainbow stripes, a dark face mask, a slit eye, a scary dragon face with many teeth, horns, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view, glossy shine, gradients.""",
        # rig #9, khung đứng đầu: 2 chân sau xa, 3 hai vây nhỏ, 4 đầu, 5 cặp vây trên, 6 chân trước xa, 7 cổ và thân, 8 chân sau
        # gần, 9 chân trước gần, 10 vỏ sò, 11 chuỗi hạt, 12 mắt, 13 cặp vây trái, 14-16 đuôi, 17-19 bong bóng. Viền px = 0,85% chiều
        # cao cả con trong RegionMap (9,1 px) × tỉ lệ phóng của orig/Nxx.png. Giáp ngực vẽ ở phần trên chân trước gần (N05): ảnh gốc
        # N04 đã kín khung, và chỗ đó của rig nằm ngay dưới chuỗi hạt.
        "groups": [
            ("N01", "sáu vây mào", "six crest fins", "doi", 20,
             "six separate crest fins: four long ones on the left sweeping up-left, two small ones on the right pointing up",
             "Sáu vây rời (1024 × 1024, nền trắng): bên trái bốn vây dài thành hai cặp quét lên trái, gốc ở đầu dưới bên phải; bên phải hai vây nhỏ chĩa thẳng lên, gốc ở đầu dưới; khoảng trống giữa là chỗ của đầu",
             """- đủ sáu vây, mỗi vây đúng chỗ, đúng hướng, gốc ở đúng chỗ gốc cũ;
- vây nước xanh viền bạc như concept; không vẽ đầu, mũ; không sọc cam đỏ.""",
             """Image 1 is the crest of a 2D cut-out animation puppet (the old design): SIX separate fins that grow from the top and back of a head (the head is not shown). Four long fins on the left, in two pairs, sweep up and to the upper left; each grows from its LOWER RIGHT end. Two small fins on the right point straight up; each grows from its LOWER end. Redraw THESE six fins as the crest of image 2 (the approved concept): fins of blue water edged in silver, each in the same place, direction and about the same size as its old fin, every root exactly where the old root is.
Do NOT draw: the head, the helmet, orange or red stripes, extra fins.""", "root of every fin"),
            ("N02", "đầu, mặt và mũ", "head with helmet", "doi", 22,
             "a dragon head in side view facing right: dark-blue hood, pale lower face, snout tip at the right",
             "Đầu nhìn nghiêng quay phải (1024 × 1024, nền trắng): mũ trùm xanh đậm trên đỉnh và sau đầu, mắt hẹp trắng, mặt dưới xanh nhạt, chóp mõm ở bên phải; mép dưới trái nối cổ (cổ là mảnh khác vẽ đè lên mép đó)",
             """- chóp mõm, đỉnh đầu, mép dưới trái (chỗ nối cổ) đúng chỗ cũ; cỡ như cũ;
- mũ bạc vành ngắn, hình thoi vàng trên trán; một mắt tròn to quả quyết dưới vành; miệng cười tự tin khép, lộ một nanh nhỏ;
- không mặt nạ đậm, không mắt hẹp; không vẽ vây mào, cổ, thân.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): the head in side view facing right: a dark-blue rounded hood over the top and back, a narrow eye, a pale lower face and the pointed snout tip at the RIGHT; its lower LEFT edge joins the neck (the neck is a separate piece drawn over that edge). Redraw THIS piece as the head of image 2 (the approved concept): a rounded dragon head of clear blue water facing right with a short snout, wearing the silver knight helmet with the short brow rim and the small gold diamond on the brow; one big round determined eye under the rim; a small confident closed smile with a tiny fang near the snout.
Keep the snout tip, the top of the head and the lower left neck edge where they are, and the head about the same size.
Do NOT draw: the crest fins, a neck, a body, a dark face mask, a narrow slit eye.""", "lower left neck edge and the snout tip"),
            ("N03", "cổ và thân", "neck and body", "giu", 14,
             "the neck and body in side view facing right: neck top at upper right, chest at right, back sloping to lower left",
             "Cổ và thân nhìn nghiêng quay phải (1024 × 1024, nền trắng): đầu hẹp trên phải là đỉnh cổ (đè lên đáy đầu), ngực bên phải, lưng dốc xuống trái tới chỗ nối đuôi, bụng ở dưới; trước xanh nhạt, lưng xanh đậm",
             """- giữ viền ngoài: đỉnh cổ trên phải, lưng dốc xuống trái, bụng ở dưới;
- nước xanh trong, họng, ngực và bụng xanh nhạt, lưng xanh đậm có vài vệt sóng như concept;
- không vẽ đầu, giáp cổ, giáp ngực, chân, đuôi.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): the neck and the body in side view facing right. The narrow TOP RIGHT end is the top of the neck (it is drawn over the bottom of the head); the chest is at the right; the back slopes down to the lower left, where the tail joins; the belly is at the bottom. The legs and the tail are separate pieces. Redraw THIS piece as the neck and body of image 2 (the approved concept): clear blue water with a light-blue throat, chest and belly, deeper blue along the back with a few wave-like swirls as in the concept.
Do NOT draw: the head, the gorget, the breastplate, legs, the tail, beads, a sea shell.""", None),
            ("N04", "giáp cổ và huy hiệu", "gorget and medallion", "doi", 31,
             "a necklace on the chest: a row of beads from the upper left down to the right, ending in a big shell at the lower right",
             "Chuỗi hạt trên ngực (1024 × 1024, nền trắng): hàng hạt tròn từ trên trái chạy xuống phải, cuối là vỏ sò to ở dưới phải; vẽ đè lên cổ, thân và chân trước gần",
             """- hàng vảy bạc tròn có đinh vàng nhỏ đi đúng đường hàng hạt cũ;
- huy hiệu giọt nước vàng đúng chỗ vỏ sò, cỡ gần bằng vỏ sò;
- không vẽ giáp ngực (nằm ở nhóm N05), cổ, thân; không hạt, không vỏ sò.""",
             """Image 1 is one group of a 2D cut-out animation puppet (the old design): a necklace worn on the chest: a row of round beads running from the UPPER LEFT down to the right, ending in a big sea shell at the LOWER RIGHT. It is drawn on top of the neck, the body and the near front leg. Redraw THIS group as the gorget of image 2 (the approved concept): a row of small round silver scales with tiny gold rivets following the old bead row, and the gold water-drop medallion where the shell is, about the shell's size.
Do NOT draw: the breastplate (another group), the neck, the body, legs, beads, a sea shell.""", "bead row and the shell's place"),
            ("N05", "chân trước gần và giáp ngực", "near front leg with breastplate", "giu", 11,
             "a tall front leg: rounded shoulder at the top, lime band and three red claws at the bottom",
             "Chân trước gần, cao (1024 × 1024, nền trắng): đầu trên tròn là vai (ngay dưới chuỗi hạt), chạy thẳng xuống, cuối có vòng xanh chanh và ba móng đỏ",
             """- giữ viền ngoài; vai ở **đầu trên**, bàn chân ở **đầu dưới**;
- phần trên (ngay dưới chuỗi hạt) phủ giáp ngực bạc, mép dưới viền vàng như ngực trong concept;
- giáp ống chân bạc viền vàng ở chỗ vòng xanh chanh cũ; ba móng ngắn màu kem ở chỗ ba móng đỏ.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): the near front leg, tall and thick. Its rounded TOP end is the shoulder (just under the necklace); it goes straight down; the foot is at the BOTTOM end, with a lime band and three red claws. Redraw THIS piece as the near front leg of image 2 (the approved concept): a thick leg of clear blue water; its upper part, just under the necklace, is covered by the silver breastplate with the gold-trimmed lower edge that the concept shows on the chest; a silver greave with gold trim on the lower leg where the lime band is; three short pale claws at the bottom where the red claws are.
Do NOT put the foot at the top. Do NOT draw: the gorget or medallion, the body, other legs, orange or red colours.""", None),
            ("N06", "chân trước xa", "far front leg", "giu", 17,
             "a front leg: narrow top hidden behind the chest, lime band and red claws at the bottom",
             "Chân trước xa (1024 × 1024, nền trắng): đầu trên hẹp khuất sau ngực, chạy thẳng xuống, cuối có vòng xanh chanh và móng đỏ",
             """- giữ viền ngoài; đầu trên là vai, bàn chân ở **đầu dưới**;
- nước xanh, giáp ống chân bạc viền vàng ở chỗ vòng xanh chanh, móng ngắn màu kem ở chỗ móng đỏ.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): the far front leg. Its narrow TOP end is the shoulder, hidden behind the chest; it goes straight down; the foot is at the BOTTOM end, with a lime band and red claws. Redraw THIS piece as the far front leg of image 2 (the approved concept): a leg of clear blue water, a silver greave with gold trim on the lower leg where the lime band is, short pale claws at the bottom where the red claws are.
Do NOT put the foot at the top. Do NOT draw: the breastplate, the body, other legs, orange or red colours.""", None),
            ("N07", "hai chân sau", "two hind legs", "giu", 24,
             "two hind legs: the near one (left, dark blue, hip at top, foot at bottom) and the far one (right, a narrow dark plate)",
             "Hai chân sau (1024 × 1024, nền trắng): chân gần bên trái xanh đậm, hông ở trên, bàn chân nhọn ở dưới; chân xa bên phải là tấm hẹp xanh đậm, gần như khuất",
             """- giữ viền cả hai chân; hông ở **đầu trên**, bàn chân ở **đầu dưới**;
- chân gần nước xanh đậm, giáp gối hoặc ống chân bạc viền vàng, móng ngắn màu kem ở đầu dưới; chân xa xanh đậm trơn.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): the two hind legs. The near one, on the LEFT, is dark blue: its TOP end is the hip, it goes down to a pointed foot at the BOTTOM. The far one, on the RIGHT, is a narrow dark plate, mostly hidden behind the body. Redraw THESE two pieces as the hind legs of image 2 (the approved concept): the near one a leg of deeper blue water with a silver greave trimmed in gold and short pale claws at the bottom, like the concept's hind leg; the far one plain deeper blue water, same outline.
Do NOT put the feet at the top. Do NOT draw: the body, the tail, front legs, extra legs.""", None),
            ("N08", "đuôi lưỡi kiếm", "tail with blade fins", "doi", 12,
             "a tail: thick joint end at upper right, sweeping down-left to two fins pointing left",
             "Đuôi (1024 × 1024, nền trắng): đầu dày trên phải nối lưng, quét xuống trái, cuối là hai vây (trên, dưới) chĩa trái có chóp cam đỏ",
             """- đầu nối thân (đầu dày trên phải) đúng chỗ cũ; hai vây cuối đúng chỗ hai vây cũ, chĩa trái;
- đuôi nước xanh có vệt sóng đậm; hai vây hình lưỡi kiếm viền bạc như concept; không chóp cam đỏ.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a tail. Its thick UPPER RIGHT end joins the back of the body; it sweeps down and to the left and ends in TWO fins (an upper one and a lower one) pointing left, with orange-red tips. Redraw THESE pieces as the tail of image 2 (the approved concept): a swirling clear-blue water tail with a darker wave stripe, ending in the two broad fins shaped like sword blades, silver-edged, pointing left.
Keep the joint end where it is and the two fins where the old fins are, about the same size.
Do NOT draw: orange or red tips, the body, legs.""", "thick upper right joint end"),
        ],
        "extra": [],
        "first": ["N02", "N05"],  # gen thử trước: đầu (đổi dáng), chân trước gần có giáp ngực (giữ viền)
    },
    # Dòng Tiểu Y (aola 1319 → 1320). Người dùng chốt 2026-11-04: giữ theme thần biển Poseidon, DẠNG NGƯỜI (ngoại lệ của luật
    # "tướng là thú nuôi"), thiết kế theo DESIGN_CHIBI.
    # Hiệu ứng nước tự chạy (lốc nước, vòng nước, dải nước) giữ hình gốc để không mất animation: bỏ khỏi bóng xám, không có nhóm.
    # Bộ ghép: <aola>/reskin/thuy_1319, thuy_1320 (regions.json, groups.json). Viền px = 0,85% chiều cao cả con × tỉ lệ phóng.
    {
        "code": "tieu_y_1", "elem": "thuy", "aola": 1319,
        "hero": "Tiểu Y", "form": 1, "forms": 2, "form_name": "Tiểu Y",
        "role_vi": "tướng Thường hệ Thủy, dạng 1/2, rig aola #1319",
        "design_vi": ("tiểu thần biển dạng người (người dùng chốt 2026-11-04: giữ theme thần Poseidon, dạng người): bé trai chibi "
                      "tóc xanh thẫm thành năm lọn sóng cuộn, ngọn vỡ bọt trắng; chóp vương miện vàng nhỏ có ngọc trai trên trán, "
                      "kẹp sao biển vàng trên lọn tóc phải; hai vây tai xanh ngọc viền vàng; da hồng nhạt, mắt xanh ngọc to; hai vai "
                      "vỏ sò điệp trắng ngà viền vàng; cổ áo chiton trắng viền hoa văn sóng vàng, ghim tròn vàng có ngọc xanh ngọc; "
                      "tay mũm mĩm đeo vòng vàng mảnh, cầm đinh ba tập sự cán gỗ trôi dạt, ba mũi vỏ sò trắng ngà buộc vàng; nửa dưới "
                      "là vòi rồng nước nhỏ; mặt quả quyết, cười tự tin"),
        "rig_vi": ("con gốc #1319 là bé chibi nhìn chéo 3/4 quay phải: đầu rất to, chỏm năm lọn tóc to vuốt lên, hai vây tai sau "
                   "hai bên đầu (vây trái to chĩa lên trái, vây phải mảnh chĩa lên), hai cục vai ở hai bên dưới đầu, cổ giáp nhỏ "
                   "dưới cằm, không thấy cánh tay; tay trái nắm cây đinh ba ngắn nằm chéo (đuôi cán trên trái, đầu dưới phải), tay "
                   "phải nắm lại cạnh cằm; nửa dưới là lốc nước thay chân. Bỏ khỏi bóng xám: bóng dưới chân và hai vòng nước"),
        "regions_vi": ("1 hai vây tai, 2 chỏm năm lọn tóc, 3 đầu và mặt, 4 hai hạt trang sức nhỏ (trán, lọn tóc phải), 5 hai cục "
                       "vai, 6 cổ giáp dưới cằm, 7 tay trái nắm đinh ba, 8 nắm tay phải, 9 đinh ba, 10 lốc nước thay chân (vùng hồng "
                       "phía dưới; số 10 in đè lên chỗ đinh ba)"),
        "anchor": True, "design": DESIGN_CHIBI,
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original character: a LITTLE SEA GOD, a chibi boy who is the young prince of the sea (in the spirit of the young Poseidon or Triton of Greek myth, but an original design), the first stage of a two-stage Water evolution line, in the same front three-quarter view and pose as image 1, on a plain white background. Instead of legs he rides a small waterspout. An original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new character will be animated on. They tell you where each part and joint is, NOT what the character looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one big round head with a crest of five big hair tufts on top and two fins behind its sides; two tiny ornaments (one on the forehead, one on the right-hand tuft); two small shoulder pieces at the lower sides of the head; a small chest piece right under the chin; two small hands close to the body, the arms hidden; one short trident; a small waterspout instead of legs. No legs, no feet, no tail, no wings, no extra limbs;
- every joint where it is: the head sits straight on the chest piece (no neck shows); the tufts grow from the top of the head; the fins grow from behind the sides of the head; the shoulder pieces sit at the lower left and lower right of the head; the viewer-left hand is at the left of the chest, closed around the trident shaft; the viewer-right hand is a small fist at the right, beside the chin; the waterspout starts under the chest piece;
- every part pointing the same way: the face is turned a little to the viewer's right; the big viewer-left fin points up and out to the upper left, the small viewer-right fin points up; the tufts sweep upward, the two biggest ones up-left and up; the trident lies diagonally, its butt end at the upper left behind the viewer-left hand and its prongs at the lower right, pointing down-right; the waterspout narrows down to a thin tip at the bottom;
- the head and hair about the size and shape of regions 3 and 2 together (more than half of the figure: a chibi); the hands, the trident and the waterspout about the size of regions 7, 8, 9 and 10 (region 10 is the pink swirl under the body; its number is printed over the trident); the whole figure about the same height.

CHANGE (the new look, region by region):
1 the two fins: sea-green fish fins with a thin gold edge and a few darker green ribs, pointing the way their regions point.
2 hair: five big curls of dark navy-blue hair, each shaped like a curling ocean wave whose tip breaks into white sea foam; they keep the places and sizes of the five tufts of region 2.
3 head: a chibi boy's face: light warm peach skin, big round sea-green eyes, short thick brows angled down, a small confident smile with one corner raised; navy hair framing the face.
4 the two tiny ornaments: on the forehead, one small gold crown point holding a white pearl (the young prince's circlet); on the right-hand tuft, a tiny gold starfish hair clip.
5 the two shoulder pieces: two small scallop shells, pearl white with gold rims, worn as shoulder pads.
6 the chest piece: the top of a white Greek tunic with a gold wave-pattern collar and a small round gold brooch holding a sea-green gem.
7 viewer-left hand: a small chubby hand with a thin gold bangle at the wrist, closed around the trident shaft.
8 viewer-right hand: a small chubby fist with a thin gold bangle, raised beside the chin, ready to fight.
9 trident: a short apprentice's trident: a pale driftwood shaft, a blue cord wrapped just below the head, three pointed prongs of pearl-white shell (the middle one longest) bound to the shaft with gold; the same length and the same diagonal as region 9.
10 waterspout: a small swirling waterspout of light-blue water with white foam curls, wide under the chest piece and narrowing down to a thin tip.

ATTITUDE: a brave little sea prince on his first adventure: brows angled down, a confident small smile, chin up, fist raised and trident ready; cute and small, never scary, never a goofy mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those.

COLOURS: dark navy-blue hair with white foam; light warm peach skin; sea-green eyes and fins; white tunic; gold trims; pale driftwood and pearl-white shell; light-blue water. Few colours.

AVOID: white or grey spiky hair, red eyes, red cheek marks, tan skin, a gold collar with a blue gem, gold diamond-shaped shoulder pieces, a gold trident, legs or feet, a fish tail, a cape, a helmet, a tall spiky crown, armour plates, water splashes or water rings around the hands (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #1319, khung đứng đầu: 1 bóng, 2 vây phải, 3 lọn tóc phải, 4 lốc nước (tự chạy), 5 cổ giáp, 6 vòng nước phải (tự
        # chạy), 7 cục vai phải, 8 đầu (mũ tóc nâu, mặt), 9 lọn tóc trái lớn, 10 lọn nhỏ phải, 11 hạt xanh lọn phải, 12 lọn phải
        # trước, 13 vây trái, 14 cục vai trái, 15 lọn trước trán, 16 mắt trái, 17 hạt xanh trán, 18 mắt phải, 19 nắm tay phải,
        # 20 đuôi cán đinh ba, 21 tay trái, 22 vòng nước trái (tự chạy), 23 đầu đinh ba. Khung N05, N06 nới rộng (mảnh nhỏ, phóng
        # to quá thì viền 38, 60 px).
        "groups": [
            ("N01", "hai vây tai", "two fins", "doi", 9,
             "two blue scaled fins: a big one on the left pointing up-left, base at its lower right; a thin one on the right pointing up, base at its bottom",
             "Hai vây xanh lam có vảy (1024 × 1024, nền trắng): vây trái to chĩa lên trái, gốc ở góc dưới bên phải; vây phải mảnh chĩa lên, gốc ở đầu dưới; khoảng trống giữa là chỗ của đầu",
             """- gốc vây trái ở góc dưới phải, gốc vây phải ở đầu dưới, đúng chỗ gốc cũ;
- vây cá xanh ngọc viền vàng mảnh, vài gân xanh đậm, đúng hướng cũ, cỡ như cũ hoặc to hơn chút;
- không vẽ đầu, tóc, vảy xanh lam.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two fins behind the sides of a head (the head is not shown). The big viewer-left fin points up and to the upper left; its base, where it joins the head, is its LOWER RIGHT end. The thin viewer-right fin points up; its base is its BOTTOM end. Redraw THESE two pieces as the two fins of image 2 (the approved concept): sea-green fish fins with a thin gold edge and a few darker green ribs, each in the same place and direction as its old fin, about the same size or a little bigger.
Do NOT draw: the head, hair, blue scales, extra fins.""", "base end of each fin"),
            ("N02", "đầu và mặt", "head and face", "doi", 15,
             "a big round head: brown hair cap over the top and forehead, a face below with two big red eyes, turned a little to the right",
             "Đầu tròn to (1024 × 1024, nền trắng): mảng tóc nâu trùm đỉnh và trán, mặt da nâu ở dưới, hai mắt to đỏ hơi lệch sang phải, má hồng; năm lọn tóc và hai vây là nhóm khác",
             """- cằm đúng chỗ cũ, đầu cỡ như cũ; hai mắt đúng chỗ hai mắt cũ;
- mặt bé trai da hồng nhạt, mắt xanh ngọc to, mày xếch xuống, cười tự tin; mảng tóc xanh thẫm trùm đỉnh và trán ở chỗ mũ tóc nâu cũ;
- không vẽ năm lọn tóc to, vây, chóp vương miện (nhóm N03); không mắt đỏ, không vệt đỏ trên má;
- tô phẳng, chỉ một chấm sáng nhỏ trong mỗi mắt.""",
             """Image 1 is one group of a 2D cut-out animation puppet (the old design): a big round head: a brown hair cap over the top and the forehead and, below it, a face with two big eyes, turned a little to the viewer's right. Redraw THIS group as the head of image 2 (the approved concept): the chibi boy's face with light warm peach skin, big round sea-green eyes exactly where the old eyes are, short thick brows angled down, a small confident smile; the cap of dark navy-blue hair over the top and the forehead where the brown cap is.
Keep the chin where it is and the head about the same size: the five big hair curls and the fins are drawn over it in other groups.
Do NOT draw: the five big hair curls, the fins, the crown point, a neck, a body, red eyes, red cheek marks.""", "eyes and the chin"),
            ("N03", "chỏm tóc sóng, chóp vương miện, kẹp sao biển", "wave-hair crest and ornaments", "doi", 11,
             "five big white hair tufts sweeping up, a small blue drop on the front tuft and one on the right tuft",
             "Năm lọn tóc trắng xám to vuốt lên (1024 × 1024, nền trắng): hai lọn lớn trên trái và trên phải, ba lọn nhỏ phía trước trán; hai hạt xanh, một trên lọn trước trán, một trên lọn phải",
             """- năm lọn đúng chỗ, đúng hướng, gốc lọn dọc đỉnh đầu như cũ;
- mỗi lọn là sóng cuộn tóc xanh thẫm, ngọn vỡ thành bọt trắng;
- chỗ hạt trước trán: chóp vương miện vàng nhỏ giữ ngọc trai trắng; chỗ hạt bên phải: kẹp sao biển vàng nhỏ;
- không vẽ mặt, vây; không tóc trắng xám.""",
             """Image 1 is one group of a 2D cut-out animation puppet (the old design): a crest of five big hair tufts that grow from the top of a head (the face is not shown) and sweep upward: two big ones at the upper left and the upper right, three smaller ones at the front over the forehead; a small blue drop sits on the front tuft at the forehead and another on the right tuft. Redraw THIS group as the hair of image 2 (the approved concept): five big curls of dark navy-blue hair, each shaped like a curling ocean wave whose tip breaks into white sea foam, each curl in the place, direction and about the size of its old tuft, every root along the top of the head where the old roots are. Where the forehead drop is, draw the small gold crown point holding a white pearl; where the right drop is, draw the tiny gold starfish hair clip.
Do NOT draw: the face, the fins, white or grey hair, blue drops.""", "roots of the tufts along the top of the head"),
            ("N04", "vai vỏ sò và cổ áo", "shell shoulder pads and tunic collar", "giu", 13,
             "two small gold diamond shoulder pieces left and right, a gold collar with a blue gem in the middle",
             "Ba mảnh (1024 × 1024, nền trắng): hai cục vàng hình thoi hai bên (vai), giữa là cổ giáp vàng có ngọc xanh, ngay dưới cằm",
             """- ba mảnh đúng chỗ, đúng cỡ cũ;
- hai vai thành vỏ sò điệp trắng ngà viền vàng; giữa là cổ áo chiton trắng viền hoa văn sóng vàng, ghim tròn vàng có ngọc xanh ngọc;
- không vẽ đầu, tay, lốc nước.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): two small gold diamond-shaped shoulder pieces at the left and the right, and between them a small gold collar with a blue gem: the chest piece right under the chin. Redraw THESE pieces as image 2 (the approved concept) shows them: the two shoulder pieces become two small scallop shells, pearl white with gold rims; the chest piece becomes the top of the white Greek tunic with a gold wave-pattern collar and a small round gold brooch holding a sea-green gem.
Do NOT draw: the head, the hands, the waterspout, gold diamonds, a blue gem.""", None),
            ("N05", "tay trái nắm đinh ba", "viewer-left hand on the trident", "giu", 23,
             "a small hand closed around a diagonal shaft (not shown): wrist with a gold ring at the upper right, knuckles at the lower left",
             "Bàn tay nhỏ (1024 × 1024, nền trắng, khung rộng): nắm quanh cán chéo (cán không có trong ảnh), cổ tay ở trên phải có vòng vàng, khớp ngón ở dưới trái",
             """- viền và chỗ như cũ; cổ tay trên phải, khớp ngón dưới trái;
- tay mũm mĩm da hồng nhạt, vòng vàng mảnh ở cổ tay;
- nắm rỗng, không vẽ cán đinh ba (cán ở nhóm N07).""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a small hand closed around a shaft that runs diagonally through it (the shaft is not shown). The wrist, with a gold ring, is at the UPPER RIGHT; the knuckles are at the lower left. Redraw THIS piece as the viewer-left hand of image 2 (the approved concept): a small chubby hand with light warm peach skin and a thin gold bangle at the wrist, closed around nothing visible: the trident is drawn in another group and passes through this fist.
Do NOT draw: the trident or any part of it, an arm, a sleeve, claws.""", None),
            ("N06", "nắm tay phải", "viewer-right fist", "giu", 18,
             "a small round fist, thumb at the top",
             "Nắm tay tròn nhỏ (1024 × 1024, nền trắng, nằm giữa khung rộng): ngón cái ở trên",
             """- đúng chỗ, đúng cỡ cũ;
- nắm tay mũm mĩm da hồng nhạt, vòng vàng mảnh ở cổ tay nếu có chỗ;
- không vẽ cánh tay.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a small round fist, thumb at the top, held beside the chin. Redraw THIS piece as the viewer-right fist of image 2 (the approved concept): a small chubby fist with light warm peach skin, a thin gold bangle showing at the wrist if there is room.
Do NOT draw: an arm, a sleeve, a weapon, claws.""", None),
            ("N07", "đinh ba tập sự", "apprentice trident", "doi", 16,
             "a gold trident lying diagonally: butt end at the upper left, head at the lower right (leaf-shaped middle point, two curled side prongs, blue gem)",
             "Đinh ba vàng nằm chéo (1024 × 1024, nền trắng): đuôi cán ở trên trái, đầu ở dưới phải (mũi giữa hình lá, hai mũi bên cong, ngọc xanh ở chỗ nối)",
             """- cán chéo đúng đường cũ, đuôi cán trên trái, đầu dưới phải, dài như cũ;
- cán gỗ trôi dạt nhạt màu, dây xanh quấn hai chỗ (gần đuôi cán và ngay dưới đầu) như concept;
- chạc vàng nhỏ giữ ba mũi là vỏ ốc xoắn trắng ngà, mũi giữa dài nhất, chĩa xuống phải;
- không vẽ bàn tay; không cán vàng, không ngọc xanh.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a short trident lying diagonally: its butt end at the UPPER LEFT, its shaft running down to the right, its head at the LOWER RIGHT (a leaf-shaped middle point, two curled side prongs and a blue gem). A hand holds the shaft near the butt end (the hand is another group). Redraw THESE pieces as the apprentice trident of image 2 (the approved concept): a pale driftwood shaft along exactly the same line and length, blue cord wrapped in two places (near the butt end and just below the head) as in the concept, a small gold fork at the head holding three pearl-white spiral shells as the prongs (the middle one longest), the prongs pointing down-right where the old head is.
Do NOT draw: the hand, a gold shaft, a blue gem, curled gold side prongs, glowing effects.""", "shaft line and grip point"),
        ],
        "extra": [],
        "first": ["N02", "N05"],  # gen thử trước: đầu (đổi dáng), tay nắm đinh ba (giữ viền)
    },
    {
        "code": "tieu_y_2", "elem": "thuy", "aola": 1320,
        "hero": "Tiểu Y", "form": 2, "forms": 2, "form_name": "Y Trạch",
        "role_vi": "tướng Thường hệ Thủy, dạng 2/2, rig aola #1320",
        "design_vi": ("thần biển trẻ dạng người, lớn lên từ dạng 1: bờm tóc xanh thẫm vuốt ngược như sóng vỡ, ngọn cuộn bọt trắng; "
                      "vương miện vàng ba chóp có ngọc trai; râu ngắn gọn xanh thẫm; khuyên tai vàng hình vây có giọt ngọc trai; hai "
                      "vây tai xanh ngọc viền vàng; hai lọn tóc dài buộc vòng vàng rủ trên ngực; áo choàng xanh ngọc viền sóng vàng, "
                      "lót xanh thẫm; ngực trần da hồng nhạt với dải vải trắng viền vàng, móc vỏ sò vàng, huy chương vàng có ngọc trai "
                      "lớn, thắt lưng vàng hoa văn sóng; găng đồng xanh ngọc viền vàng; đinh ba cán trắng ngà quấn đai vàng, ba mũi vàng "
                      "hình sóng vỡ, ngọc xanh ngọc tròn to; nửa dưới là vòi rồng nước lớn; oai, tự tin"),
        "rig_vi": ("con gốc #1320 là người lớn cơ bắp nhìn chéo 3/4 quay phải: bờm tóc vuốt ngược, hai vây tai, băng trán, hai khối "
                   "vàng ở quai hàm, hai lọn tóc dài rủ trên ngực, áo choàng (mảng lớn vắt vai trái lộ lòng tối, mảng nhỏ trên vai "
                   "phải), ngực trần có đai ngực, huy chương, thắt lưng; tay trái co, nắm cán đinh ba dựng đứng bên trái ngang ngực; "
                   "tay phải duỗi sang phải, bàn tay mở cong như vuốt; nửa dưới là lốc nước lớn. Bỏ khỏi bóng xám: bóng dưới chân "
                   "và bốn hiệu ứng nước (vòng nước ở tay phải, hai dải nước, sóng nước trên trái)"),
        "regions_vi": ("1 hai vây tai, 2 bờm tóc, 3 đầu và mặt, 4 băng trán, 5 hai khối vàng ở quai hàm, 6 hai lọn tóc trên ngực, "
                       "7 áo choàng, 8 cổ và thân, 9 đai ngực, huy chương, thắt lưng, 10 tay trái, 11 nắm tay trái trên cán đinh ba, "
                       "12 tay phải duỗi, 13 bàn tay phải mở, 14 đinh ba, 15 lốc nước thay chân"),
        "anchor": True, "design": DESIGN_CHIBI,
        "prev": [("tieu_y_1", "the approved FIRST stage of this evolution line: keep its colours, hair, face, eyes, fins and "
                              "drawing style",
                  "dạng 1, tiểu thần biển: tóc xanh thẫm năm lọn sóng ngọn bọt trắng, chóp vương miện vàng có ngọc trai, vây tai "
                  "xanh ngọc viền vàng, mắt xanh ngọc, cổ áo chiton trắng viền sóng vàng, đinh ba tập sự. Giữ màu, tóc, mặt, mắt, "
                  "vây, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original character: the SECOND and final stage of a two-stage Water evolution line whose first stage is image 6. The little sea prince of image 6 has grown into the SEA GOD himself: a strong young sea king in the spirit of Poseidon of Greek myth (an original design), tall and heroic, his tall trident planted beside him, his open hand commanding the water, a big waterspout under him instead of legs. Same front three-quarter view and pose as image 1, on a plain white background. Not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new character will be animated on. They tell you where each part and joint is, NOT what the character looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head with a big mane of hair on top, two fins behind the sides of the head, a band across the forehead, two small ornaments at the sides of the jaw, two long locks hanging over the chest, a cape (a big drape over the viewer-left shoulder with its lining showing behind the viewer-left fist, and a small drape on the viewer-right shoulder), a neck and a bare torso, a strap across the chest with two clasps and a round medallion, a belt, two arms, one tall trident, a big waterspout instead of legs. No legs, no feet, no tail, no wings, no extra limbs;
- every joint where it is: the head on the neck at the top of the torso; the mane growing from the top and the back of the head; the fins growing from behind the sides of the head; the long locks starting beside the neck; the cape hanging from the shoulders; the viewer-left arm goes down from the shoulder and bends to the left, its fist closed around the trident shaft at chest height; the viewer-right arm stretches out to the right at shoulder height with the open hand at its end; the waterspout starts at the belt;
- every part pointing the same way: the face is turned a little to the viewer's right; the mane sweeps up and back, its tips pointing up and to the upper left; the viewer-left fin points up and to the upper left, the viewer-right fin points up; the locks hang down; the trident stands upright on the viewer-left, prongs at the TOP, its shaft going straight down past the waterspout; the open hand's fingers curl down like a claw; the waterspout widens into a big swirl under the belt and narrows down to a thin tip at the bottom;
- the torso and the arms about the size and shape of regions 8, 10 and 12; the head a little BIGGER than region 3 (up to about one and a half times its size), so the face and the big eyes of image 6 still read when the figure is small, its chin and neck joint staying where region 3's are; the trident as tall as region 14; the whole figure about the same height.

CHANGE (the new look, region by region):
1 fins: sea-green fish fins with a gold edge and darker green ribs, bigger and sharper than in image 6.
2 hair: a big mane of dark navy-blue hair swept up and back like a breaking wave, its tips curling into white sea foam: image 6's wave hair grown long.
3 head: a confident young sea king's face: light warm peach skin, sea-green eyes under strong brows angled down, a calm confident smile, a short neat navy-blue beard along the jaw and the chin.
4 forehead band: a gold crown band across the forehead with three small upright points like the prongs of a trident and a white pearl in the middle (image 6's little crown point grown into a crown).
5 jaw ornaments: two gold ear cuffs shaped like small fins, each with a pearl drop.
6 chest locks: two long locks of navy hair hanging down over the chest, each tied with a gold ring and ending in a white foam curl.
7 cape: a sea-green cape with a gold wave-pattern border and a deep navy lining: the big drape over the viewer-left shoulder, its navy lining showing behind the viewer-left fist, and a small drape on the viewer-right shoulder.
8 neck and torso: a strong bare chest and stomach, light warm peach skin, the muscles drawn with a few simple ink lines.
9 strap, clasps, medallion, belt: a white sash with gold edges across the chest from shoulder to shoulder, held by two gold scallop-shell clasps; a round gold medallion with a big white pearl in its middle; a gold belt with a wave pattern at the waist.
10 viewer-left arm: a strong arm, a sea-green bronze bracer with gold rims at the wrist, a small gold shell guard at the elbow.
11 viewer-left hand: a big fist closed around the trident shaft.
12 viewer-right arm: stretched out to the right, the same bracer and a gold wrist band.
13 viewer-right hand: open, the fingers curled down like a claw, commanding the water.
14 trident: a tall sea god's trident: a pearl-white shaft with gold bands, three gold prongs shaped like breaking waves (the middle one tallest), a big round sea-green gem where the prongs meet the shaft; the same height and place as region 14.
15 waterspout: a big swirling waterspout of light-blue water with white foam curls, wide under the belt and narrowing down to a thin tip.

ATTITUDE: a proud, powerful young sea king: head high, brows angled down, a calm confident smile, the open hand ready to raise the waves, the trident planted beside him; heroic and appealing, never scary, never a goofy mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those. Image 6 is the approved first stage of this line: keep its colours, hair, face, eyes, fins and drawing style, so both stages read as the same character growing up.

COLOURS: as in image 6: dark navy-blue hair with white foam; light warm peach skin; sea-green eyes, fins, cape and bracers; white sash; gold trims; pearl white; light-blue water. Few colours.

AVOID: white or grey hair, red eyes, red face marks, tan skin, a white cape, a gold chest harness, gold bracers with blade-like fins, a spear-shaped middle prong, a helmet, armour plates over the chest, legs or feet, a fish tail, wings, water splashes or water rings around the hands (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #1320, khung đứng đầu (60 mảnh): 1 bóng, 2 lốc nước, 4 vòng nước tay phải, 31 dải nước phải, 51 sóng nước trên
        # trái, 60 dải nước quấn lốc (đều tự chạy, giữ gốc); vây 36 41; bờm 40 45 46 50 16; đầu 38 39 43 44 48 49, băng trán
        # 47, khối vàng quai hàm 37 42; lọn tóc ngực 30 35; áo choàng 17 34 28; cổ 27, thân 22; đai ngực 29 23 24 32, thắt lưng
        # 25 26 52; tay trái 18 19 20 21, nắm tay trái 33 56-59; tay phải 3 15 14 13 12, bàn tay phải 9 5-8 10 11; đinh ba 53 54
        # 55. Tóc 30 35 40 tự chạy (tóc bay): khi ghép phải khớp hình mới vào từng khung con. Khung N03, N09, N11 nới rộng.
        "groups": [
            ("N01", "hai vây tai", "two fins", "doi", 34,
             "two dark-blue fins: the left one big with a light pattern, pointing up-left, base at its lower right; the right one slim and curved, pointing up, base at its bottom",
             "Hai vây xanh đậm (1024 × 1024, nền trắng): vây trái to có vân sáng, chĩa lên trái, gốc ở góc dưới phải; vây phải mảnh cong như sừng, chĩa lên, gốc ở đầu dưới",
             """- gốc hai vây đúng chỗ cũ, đúng hướng cũ;
- vây cá xanh ngọc viền vàng, gân xanh đậm, sắc hơn dạng 1, cỡ như cũ hoặc to hơn chút;
- không vẽ đầu, tóc; không vân xanh lam cũ.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two fins behind the sides of a head (the head is not shown). The big viewer-left fin points up and to the upper left; its base, where it joins the head, is its LOWER RIGHT end. The slim viewer-right fin curves up; its base is its BOTTOM end. Redraw THESE two pieces as the fins of image 2 (the approved concept): sea-green fish fins with a gold edge and darker green ribs, each in the place and direction of its old fin, about the same size or a little bigger.
Do NOT draw: the head, hair, a horn, blue patterns.""", "base end of each fin"),
            ("N02", "bờm tóc", "hair mane", "doi", 24,
             "a big white mane swept up and back with spiky tips, curled front locks at the lower right, grey back tufts at the left",
             "Bờm tóc trắng lớn (1024 × 1024, nền trắng): vuốt lên và ra sau, các chóp nhọn chĩa lên và lên trái; lọn tóc cong ở dưới phải (trước trán); mảng xám bên trái là tóc sau gáy (nằm sau vây trái)",
             """- bờm đúng chỗ, đúng hướng; đường chân tóc trước trán (mép dưới phải) đúng chỗ cũ;
- tóc xanh thẫm vuốt ngược như sóng vỡ, ngọn cuộn bọt trắng; mảng sau gáy xanh thẫm đậm hơn;
- không vẽ mặt, vương miện, vây; không tóc trắng xám.""",
             """Image 1 is one group of a 2D cut-out animation puppet (the old design): a big mane of hair that grows from the top and the back of a head (the face is not shown): it sweeps up and back, its spiky tips pointing up and to the upper left; curled front locks hang at the lower right, over the forehead; the grey tufts at the left are the back of the hair, behind the viewer-left fin. Redraw THIS group as the hair of image 2 (the approved concept): a big mane of dark navy-blue hair swept up and back like a breaking wave, its tips curling into white sea foam; the front locks navy with foam tips; the back tufts a deeper navy. Keep every part in its place, direction and about its size, and the hairline over the forehead (the lower right edge) where it is.
Do NOT draw: the face, the crown band, the fins, white or grey hair.""", "hairline over the forehead and the back of the head"),
            ("N03", "đầu, mặt, vương miện, khuyên tai", "head, face, crown band and ear cuffs", "doi", 32,
             "a head in three-quarter view turned right: brown hair cap, white band across the forehead, red eyes, a red cheek mark, big gold ornaments at both sides of the jaw",
             "Đầu nhìn chéo quay phải (1024 × 1024, nền trắng, khung rộng): mũ tóc nâu, băng trắng vắt ngang trán có vạch xanh, mắt đỏ, vệt đỏ trên má trái, hai khối vàng to ở hai bên quai hàm",
             """- cằm, mắt, miệng đúng chỗ cũ; đầu cỡ như cũ;
- mặt thần biển trẻ da hồng nhạt, mắt xanh ngọc, mày xếch, cười điềm tĩnh tự tin, râu ngắn gọn xanh thẫm dọc quai hàm và cằm;
- băng trán thành vương miện vàng ba chóp nhỏ có ngọc trai giữa, đúng đường băng cũ; hai khối vàng thành khuyên tai vàng nhỏ có ngọc trai treo (như concept);
- không mắt đỏ, không vệt trên mặt; không vẽ bờm, vây.""",
             """Image 1 is one group of a 2D cut-out animation puppet (the old design): the head in three-quarter view turned to the viewer's right: a brown hair cap over the top, a white band across the forehead, red eyes, a red mark on the cheek, and two big gold ornaments at the sides of the jaw. Redraw THIS group as the head of image 2 (the approved concept): the confident young sea king's face with light warm peach skin, sea-green eyes under strong brows angled down exactly where the old eyes are, a calm confident smile where the old mouth is, a short neat navy-blue beard along the jaw and the chin, navy hair over the top where the brown cap is; the band becomes the gold crown band with three small upright points and a white pearl in the middle, on the same line across the forehead; the two jaw ornaments become the small gold earrings of image 2, each with a round white pearl hanging from it, in the same places.
Keep the chin, the eyes and the mouth where they are and the head about the same size.
Do NOT draw: the big mane, the fins, red eyes, face marks, a helmet.""", "eyes, mouth and chin"),
            ("N04", "hai lọn tóc trên ngực", "two chest locks", "doi", 35,
             "two long hair locks starting beside the neck: the left one long and wavy hanging down, the right one shorter, curled, with a pointed end",
             "Hai lọn tóc dài (1024 × 1024, nền trắng): lọn trái dài lượn sóng rủ xuống, lọn phải ngắn cong có chóp nhọn; đầu trên của mỗi lọn là chỗ bắt đầu cạnh cổ",
             """- đầu trên mỗi lọn đúng chỗ cũ, lọn rủ đúng hướng cũ;
- tóc xanh thẫm, buộc một vòng vàng, cuối lọn cuộn bọt trắng;
- không vẽ mặt, râu, ngực; không tóc trắng xám.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two long locks of hair that start beside the neck and hang down over the chest: the viewer-left one long and wavy, the viewer-right one shorter and curled with a pointed end. Their TOP ends are where they start beside the neck. Redraw THESE two pieces as the chest locks of image 2 (the approved concept): long locks of dark navy-blue hair, each tied with a gold ring and ending in a white foam curl, in the same places and directions, about the same size.
Do NOT draw: the face, the beard, the chest, white or grey hair.""", "top end of each lock"),
            ("N05", "áo choàng", "cape", "giu", 18,
             "a cape: a big drape over the left shoulder (cream outside, dark lining at its left end) and a small cream drape on the right shoulder",
             "Áo choàng (1024 × 1024, nền trắng): mảng lớn bên trái mặt ngoài trắng ngà, lòng đen lộ ở đầu trái; mảng nhỏ bên phải trắng ngà vắt trên vai",
             """- giữ viền hai mảng; lòng áo lộ ra ở đầu trái như cũ;
- áo choàng xanh ngọc viền hoa văn sóng vàng, lòng xanh thẫm; mảng nhỏ bên phải cùng màu, cùng viền;
- không vẽ tay, thân, đinh ba; không áo trắng.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): the cape: a big drape over the viewer-left shoulder (cream outside, its dark lining showing at its left end) and a small cream drape on the viewer-right shoulder. Redraw THESE pieces as the cape of image 2 (the approved concept): sea-green cloth with a gold wave-pattern border, its deep navy lining showing where the old dark lining is; the small drape the same sea-green with the gold border.
Do NOT draw: arms, hands, the torso, the trident, a white cape.""", None),
            ("N06", "cổ và thân", "neck and torso", "giu", 33,
             "the neck at the top and a bare muscular torso below it, abs at the bottom",
             "Cổ và thân trần (1024 × 1024, nền trắng): cổ ở trên, ngực, bụng có múi ở dưới",
             """- giữ viền; cổ ở trên, bụng ở dưới;
- da hồng nhạt, cơ ngực bụng vẽ bằng vài nét mực đơn giản, không tô khối;
- không vẽ dải vải, huy chương, thắt lưng, tóc.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): the neck (at the TOP) and a bare muscular torso below it, the stomach with abs at the bottom. Redraw THESE pieces as the neck and torso of image 2 (the approved concept): light warm peach skin, the chest and stomach muscles shown with a few simple ink lines, no shading.
Do NOT draw: the sash, the medallion, the belt, hair, the cape.""", None),
            ("N07", "dải vải ngực, huy chương, thắt lưng", "sash, clasps, medallion and belt", "giu", 38,
             "a gold strap across the chest with two clasps and a big round buckle in the middle, a gold belt below",
             "Đai ngực vàng (1024 × 1024, nền trắng): đai ngang ngực có khóa tròn lớn ở giữa và hai móc hai bên; dưới là thắt lưng vàng",
             """- giữ viền và chỗ từng mảnh;
- đai ngực thành dải vải trắng viền vàng, hai móc thành vỏ sò điệp vàng, khóa giữa ngực thành nút vàng tròn nhỏ chỗ dải vải bắt chéo (không ngọc trai); thắt lưng vàng hoa văn sóng, giữa là khóa tròn vàng có ngọc trai lớn (như concept);
- không vẽ ngực, tay.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a gold strap across the chest with two clasps at its ends and a big round buckle in the middle, and below them a gold belt at the waist. Redraw THESE pieces as image 2 (the approved concept) shows them: the strap becomes the white sash with gold edges, the two clasps become the gold scallop-shell clasps, the buckle in the middle becomes a small round gold knot where the sash crosses the chest (no pearl there), the belt becomes the gold belt with a wave pattern and, in its middle, the round gold buckle with a big white pearl, as in image 2; every piece in its place and about its size.
Do NOT draw: the chest, arms, hair, a gold chest harness.""", None),
            ("N08", "tay trái", "viewer-left arm", "giu", 32,
             "an arm: round shoulder at the right, forearm going left, a gold bracer with a curved blade fin at the wrist end on the left",
             "Tay trái người xem (1024 × 1024, nền trắng): đầu tròn bên phải là vai, cẳng tay chạy sang trái, găng vàng có vây lưỡi cong ở cổ tay (đầu trái); bàn tay là nhóm khác",
             """- vai ở đầu phải, cổ tay ở đầu trái, đúng chỗ cũ;
- da hồng nhạt, găng đồng xanh ngọc viền vàng ở cổ tay (không vây lưỡi), như concept;
- không vẽ bàn tay, đinh ba.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the viewer-left arm: its round RIGHT end is the shoulder; the forearm runs to the left; a gold bracer with a curved blade-like fin sits at the LEFT end, the wrist (the hand is another group). Redraw THESE pieces as the viewer-left arm of image 2 (the approved concept): a strong arm with light warm peach skin, the sea-green bronze bracer with gold rims at the wrist (no blade fin), as in image 2.
Do NOT put the hand at the shoulder end. Do NOT draw: the hand, the trident, the cape, a gold bracer with a blade.""", None),
            ("N09", "nắm tay trái trên cán đinh ba", "viewer-left fist on the trident", "giu", 43,
             "a big fist seen from the knuckle side, four curled fingers, closed around a vertical shaft (not shown)",
             "Nắm tay to (1024 × 1024, nền trắng, khung rộng): nhìn từ phía khớp ngón, bốn ngón cuộn, nắm quanh cán dọc (cán không có trong ảnh)",
             """- giữ viền, chỗ các ngón như cũ;
- da hồng nhạt; nắm rỗng, không vẽ cán (cán ở nhóm N12).""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a big fist seen from the knuckle side: the palm and four curled fingers, closed around a vertical shaft that passes through it (the shaft is not shown). Redraw THESE pieces as the viewer-left fist of image 2 (the approved concept): light warm peach skin, the same fingers in the same places, closed around nothing visible: the trident is drawn in another group.
Do NOT draw: the trident shaft, the bracer, claws, a glove.""", None),
            ("N10", "tay phải duỗi", "viewer-right arm", "giu", 40,
             "an arm stretched to the right: round shoulder at the left, forearm, a gold bracer with fins and a wrist band at the right end",
             "Tay phải người xem duỗi sang phải (1024 × 1024, nền trắng): đầu tròn bên trái là vai, cẳng tay, găng vàng có vây và vòng cổ tay ở đầu phải; bàn tay là nhóm khác",
             """- vai ở đầu trái, cổ tay ở đầu phải, đúng chỗ cũ;
- da hồng nhạt, găng đồng xanh ngọc viền vàng (không vây lưỡi), vòng cổ tay vàng, như concept;
- không vẽ bàn tay, nước.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the viewer-right arm stretched out to the right: its round LEFT end is the shoulder; then the forearm; a gold bracer with fins and a gold wrist band at the RIGHT end, the wrist (the hand is another group). Redraw THESE pieces as the viewer-right arm of image 2 (the approved concept): light warm peach skin, the sea-green bronze bracer with gold rims (no blade fins) and the gold wrist band, as in image 2, each in its place.
Do NOT put the hand at the shoulder end. Do NOT draw: the hand, water, a gold bracer with blades.""", None),
            ("N11", "bàn tay phải mở", "viewer-right open hand", "giu", 47,
             "an open hand like the letter C: wrist at the upper left, fingers curling down to the right, thumb at the bottom",
             "Bàn tay mở hình chữ C (1024 × 1024, nền trắng, khung rộng): cổ tay ở trên trái, các ngón cuộn xuống sang phải, ngón cái ở dưới",
             """- giữ viền chữ C, chỗ từng ngón như cũ;
- da hồng nhạt, ngón cuộn như vuốt đang điều khiển nước; không móng nhọn dài;
- không vẽ nước, găng.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the viewer-right hand, open like the letter C: the wrist at the UPPER LEFT, the fingers curling down to the right like a claw, the thumb at the bottom. Redraw THESE pieces as the open hand of image 2 (the approved concept): light warm peach skin, the same curled fingers in the same places, commanding the water.
Do NOT draw: water, the bracer, long sharp claws, a glove.""", None),
            ("N12", "đinh ba thần biển", "sea god's trident", "doi", 8,
             "a tall gold trident standing upright: long shaft, three prongs at the top (the middle one spear-shaped), a blue gem where they meet the shaft",
             "Đinh ba vàng dựng đứng (1024 × 1024, nền trắng): cán dài, đầu ba mũi ở trên (mũi giữa hình giáo), ngọc xanh ở chỗ nối",
             """- cán thẳng đứng đúng đường cũ, đầu ở trên, đáy cán đúng chỗ cũ, cao như cũ;
- cán trắng ngà quấn đai vàng, ba mũi vàng hình sóng vỡ (mũi giữa cao nhất), ngọc xanh ngọc tròn to ở chỗ nối;
- không vẽ bàn tay; không mũi giữa hình giáo, không ngọc xanh lam.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a tall trident standing upright: a long straight shaft, a head with three prongs at the TOP (the middle one spear-shaped) and a blue gem where the prongs meet the shaft. A fist holds the shaft at chest height (the fist is another group). Redraw THESE pieces as the sea god's trident of image 2 (the approved concept): a pearl-white shaft with gold bands along exactly the same line and length, three gold prongs shaped like breaking waves (the middle one tallest) where the old head is, a big round sea-green gem where they meet the shaft.
Do NOT draw: the fist, a spear-shaped middle prong, a blue gem, glowing effects.""", "shaft line, its bottom end and its grip point"),
        ],
        "extra": [],
        "first": ["N03", "N11"],  # gen thử trước: đầu có vương miện (đổi dáng), bàn tay mở nhiều ngón (giữ viền)
    },
    # Dòng Cánh Cụt (aola 1691 → 1692), tướng Thường ải 10 đảo Thủy, "Đầu bếp xứ băng". Thiết kế Claude đề xuất 2026-11-06 (người
    # dùng chưa duyệt): cánh cụt mào kiểu rockhopper (mặt xanh thẫm, mày lông vàng xếch cho vẻ chiến), khác con gốc (xanh trời, mặt
    # trắng, khăn đỏ, cá băng, đĩa sứ bánh cá, chim con tím). Dạng 1 tập sự bếp cầm chảo gang; dạng 2 bếp trưởng, khay băng cá nướng,
    # chim non phụ bếp. Vòng băng có sao băng (tự chạy) và hơi nóng trên đĩa giữ hình gốc: bỏ khỏi bóng xám, không có nhóm; khi ghép
    # Claude tô lại cho hợp nét tướng như hiệu ứng nước của Tiểu Y. Bộ ghép: <aola>/reskin/thuy_1691, thuy_1692 (regions.json,
    # groups.json). Viền px = 0,85% chiều cao cả con trong RegionMap × tỉ lệ phóng của orig/Nxx.png.
    {
        "code": "canh_cut_1", "elem": "thuy", "aola": 1691,
        "hero": "Cánh Cụt", "form": 1, "forms": 2, "form_name": "Cánh Cụt Con",
        "role_vi": "tướng Thường hệ Thủy (ải 10 đảo Thủy), dạng 1/2, rig aola #1691",
        "design_vi": ("cánh cụt con tập sự bếp kiểu cánh cụt mào: đầu, lưng và mặt xanh thẫm, bụng trắng lên tới dưới mỏ, mắt to "
                      "lòng trắng, mày lông vàng xếch xuống phía mỏ, chóp lông nhọn ở hai bên; mào lông nhọn xanh thẫm trên đỉnh; mỏ "
                      "cam đỏ cười nhếch; khăn bếp xanh trời viền trắng thắt nút bên trái; hai vây ôm chảo gang nhỏ giơ như chùy (mép "
                      "chảo đóng sương trắng, băng nhũ nhỏ, cán gỗ quấn dây xanh trời, vòng treo tròn); đuôi nhọn xanh thẫm; chân màng "
                      "hồng nhạt; mặt quả quyết"),
        "rig_vi": ("con gốc #1691 là chim cánh cụt con mập nhìn thẳng hơi quay phải: đầu liền thân thành một khối tròn, chỏm lông "
                   "hai thùy trên đỉnh, mỏ hơi lệch phải, khăn vắt ngang ngực thắt nút bên trái hai vạt bay sang trái, hai vây ngắn "
                   "ôm con cá băng dựng đứng trước bụng (đầu cá trên phải, đuôi cá tròn ở dưới), đuôi nhọn lộ sau thân ở dưới trái, "
                   "hai bàn chân màng phẳng. Bỏ khỏi bóng xám: bóng dưới chân và vòng băng có sao băng"),
        "regions_vi": ("1 chỏm lông, 2 đầu liền thân và mặt, 3 mỏ, 4 dải khăn, 5 hai vạt nút khăn, 6 con cá cầm tay (thành chảo), "
                       "7 vây trái, 8 vây phải, 9 đuôi, 10 hai bàn chân"),
        "anchor": True,
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: a little PENGUIN COOK, a scrappy apprentice cook from the icy seas who fights with a small frying pan, the first stage of a two-stage Water evolution line, in the same front view (turned a little to the viewer's right) and pose as image 1, on a plain white background. A chubby penguin chick in the spirit of a crested rockhopper penguin, but an original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one round chubby blob that is the head and the body together (no neck), one small crest on top, one beak, a neckerchief (a band across the chest and two knot ends), one small frying pan held upright in front of the belly, two short flippers holding it, one short tail, two flat webbed feet; no arms or hands, no legs showing, no wings, no extra limbs;
- every joint where it is: the crest sits on top of the head; the beak sits on the face a little right of centre, between the eyes; the neckerchief band wraps across the chest where the head part meets the belly part, its knot at the viewer-left side; the flippers start at the sides of the body and reach in front of the belly from the left and the right, closing around the pan where its round part meets the handle; the tail sticks out from behind the lower left of the body; the feet sit flat under the bottom of the body;
- every part pointing the same way: the face is turned a little to the viewer's right; the upper knot end points up and to the left, the lower one out to the left; the pan's round part is at the TOP, a little right of centre, and its handle curves down and to the left to a round end at the BOTTOM, between the feet; the tail tip points up and to the left;
- the body, the flippers and the feet about the size and shape of regions 2, 7, 8 and 10; the whole figure about the same height.

CHANGE (the new look, region by region):
1 crest: a short spiky crest of three or four navy-blue feathers standing up on top of the head, about the size of region 1.
2 head and body: a round chubby penguin chick: dark navy-blue head, back and sides, and a dark navy face; a white belly that rises up to just under the beak; two big round eyes (a white eye-white, a large dark pupil, one small catchlight dot), and over each eye a bright yellow feather brow that angles down toward the beak and ends in a few short spiky tips at the side of the head, inside the outline: a fierce look. No blush on the cheeks.
3 beak: a short stubby orange-red beak set in a confident smirk.
4 and 5 neckerchief: a sky-blue cook's neckerchief with a thin white edge, tied at the viewer-left, its two knot ends fluttering out to the left like the two pieces of region 5.
6 frying pan: a small black iron frying pan held up like a club: the round pan at the top where region 6 is wide, seen face-on as a tilted oval with the inside of the pan facing the viewer, a crust of white frost and tiny icicles along its rim; a short wooden handle wrapped in sky-blue cord, curving down and to the left and ending in a round hanging ring at the bottom.
7 and 8 flippers: two short navy flippers with a lighter blue underside, closed around the pan where its round part meets the handle.
9 tail: a short pointed navy tail.
10 feet: two flat webbed feet, pale pink.

ATTITUDE: a scrappy apprentice cook ready to fight: brows angled down, a confident smirk, the pan gripped tight in both flippers, chest out; cute and chubby, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those.

COLOURS: dark navy blue, with a lighter blue on the flipper undersides; a white belly; bright yellow brows; an orange-red beak; pale pink feet; a sky-blue neckerchief; a black iron pan with white frost and a pale wood handle. Few colours.

AVOID: a bright sky-blue body, a white face, a tan belly, pink blush cheeks, a red scarf, a fish held in the flippers, a round two-lobed tuft, a chef hat, ice crystals, snowflakes or rings around the creature (the game adds them), a human face or body, arms or hands, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #1691, khung đứng đầu (21 mảnh): 1 bóng, 2 và 21 vòng băng có sao băng (tự chạy, giữ gốc), 3 chân phải, 4 chân
        # trái, 5 đuôi, 6 đầu liền thân, 7 chỏm lông, 8 mỏ, 9 và 10 hai vạt nút khăn, 11 dải khăn, 12 cá băng, 13 và 14 vân trên
        # cá, 15 vây phải, 16 vây trái, 17 má phải, 18 mắt phải, 19 má trái, 20 mắt trái. Clip đứng có mắt nhắm (biến thể), clip
        # chiêu có chỏm lông dựng gai và mặt há mỏ: xử lý khi ghép.
        "groups": [
            ("N01", "mào lông", "head crest", "doi", 17,
             "a small blue tuft with two round lobes, its flat bottom edge sits on the head",
             "Chỏm lông xanh hai thùy (1024 × 1024, nền trắng): thùy trái to, thùy phải nhỏ; mép dưới phẳng là chỗ cắm vào đỉnh đầu",
             """- mép dưới (chỗ cắm vào đầu) đúng chỗ mép dưới cũ, rộng như cũ;
- ba bốn lông xanh thẫm nhọn dựng lên như concept, cao hơn chỏm cũ một chút được;
- không vẽ đầu, không chỏm tròn hai thùy, không lông vàng.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a small blue tuft with two round lobes (a big one at the left, a small one at the right); its flat BOTTOM edge sits on the top of the head (the head is not shown). Redraw THIS piece as the crest of image 2 (the approved concept): a short spiky crest of three or four navy-blue feathers standing up, its base along the old bottom edge and about as wide, a little taller than the old tuft if needed.
Do NOT draw: the head, round lobes, yellow feathers.""", "bottom edge (the base)"),
            ("N02", "đầu liền thân, mặt, mỏ", "head-body with face and beak", "giu", 8,
             "one round blue blob that is head and body together: white face with two black eyes and pink cheeks, a yellow beak, a tan and white belly",
             "Khối tròn xanh là đầu liền thân (1024 × 1024, nền trắng): mặt trắng, hai mắt đen, má hồng, mỏ vàng hơi lệch phải; bụng nâu nhạt và trắng; mép dưới phẳng là đáy thân",
             """- giữ viền ngoài khối tròn như cũ (đỉnh, hai bên, đáy phẳng);
- đầu, lưng, hai bên và mặt xanh thẫm; bụng trắng lên tới ngay dưới mỏ;
- hai mắt to (lòng trắng, con ngươi đen, một chấm sáng nhỏ) đúng chỗ mắt cũ; mày lông vàng xếch xuống phía mỏ, chóp lông nhọn ở hai bên nằm trong viền;
- mỏ cam đỏ ngắn đúng chỗ mỏ cũ, cười nhếch tự tin; không má hồng;
- không vẽ khăn, mào, vây, chảo, chân.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): one round blob that is the head and the body together (no neck), with a white face, two black eyes, pink cheeks, a yellow beak a little right of centre, and a tan and white belly; its flat BOTTOM edge is the bottom of the body. Redraw THESE pieces as the head and body of image 2 (the approved concept), keeping the outline of the blob: dark navy-blue head, back, sides and face; a white belly rising up to just under the beak; the two big round eyes (a white eye-white, a large dark pupil, one small catchlight dot) exactly where the old eyes are, under the bright yellow feather brows that angle down toward the beak and end in short spiky tips at the sides, inside the outline; the short orange-red beak where the old beak is, in a confident smirk.
The neckerchief, the flippers and the pan are drawn over this group later: draw the whole body under them.
Do NOT draw: the neckerchief, the crest, the flippers, the frying pan, the feet, pink cheeks, a white face, a tan belly.""", None),
            ("N03", "khăn bếp", "neckerchief", "doi", 6,
             "a red scarf: a band curving across the chest, its knot at the left with two ends fluttering out to the left",
             "Khăn đỏ (1024 × 1024, nền trắng): dải khăn cong lõm xuống vắt ngang ngực, nút ở đầu trái với hai vạt bay sang trái (vạt trên chĩa lên trái, vạt dưới chĩa trái); đầu phải nhọn cong lên",
             """- dải khăn đi đúng đường cong cũ, hai đầu dải đúng chỗ cũ;
- nút ở đầu trái, hai vạt bay sang trái đúng hướng cũ, cỡ như cũ;
- khăn xanh trời viền trắng mảnh như concept; không khăn đỏ;
- không vẽ thân, đầu.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a red scarf: a band that curves across the chest from the left to the right (the body is not shown), its knot at the LEFT end with two ends fluttering out to the left (the upper one points up and to the left, the lower one out to the left); the right end of the band curls up. Redraw THESE pieces as the neckerchief of image 2 (the approved concept): a sky-blue cook's neckerchief with a thin white edge, the band following exactly the old curve, the knot and its two ends at the left, each end in the place and direction of the old one, about the same size.
Do NOT draw: the body, the head, a red scarf.""", "band curve and the knot at the left end"),
            ("N04", "chảo gang", "frying pan", "doi", 14,
             "a pale-blue frozen fish held upright: wide head at the upper right, body curving down to the left to a round tail at the bottom",
             "Con cá băng xanh nhạt dựng đứng (1024 × 1024, nền trắng): đầu cá rộng hình bầu dục ở trên bên phải, thân cong xuống trái, đuôi tròn ở dưới",
             """- mặt chảo tròn ở chỗ đầu cá (trên phải), cán cong xuống trái tới vòng treo tròn ở chỗ đuôi cá (dưới); cỡ như cá cũ;
- chảo gang đen, lòng chảo quay ra người xem, mép đóng sương trắng và băng nhũ nhỏ; cán gỗ nhạt quấn dây xanh trời;
- không vẽ vây (nhóm N05), không vẽ cá, không hơi nóng.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a frozen fish held upright: its wide oval head at the UPPER RIGHT, its body curving down and to the left, a round tail at the BOTTOM. Two flippers hold it around the middle (the flippers are another group). Redraw THESE pieces as the small frying pan of image 2 (the approved concept), held up like a club: the round pan where the fish's head is, seen face-on as a tilted oval with the inside of the pan facing the viewer, black iron with a crust of white frost and tiny icicles along its rim; the short pale wooden handle, wrapped in sky-blue cord, following the fish's curve down and to the left and ending in a round hanging ring where the round tail is. About the same size as the fish.
Do NOT draw: the flippers, a fish, glowing effects, steam.""", "handle line and its round bottom end"),
            ("N05", "hai vây", "two flippers", "giu", 10,
             "two short blue flippers: the left one wide, root at its left end, tip at the right; the right one smaller, root at the right, tip at the left",
             "Hai vây xanh ngắn (1024 × 1024, nền trắng): vây trái to bè, gốc ở đầu trái, chóp tròn ở bên phải; vây phải nhỏ hơn, gốc ở bên phải, chóp ở bên trái; khoảng trống giữa là chỗ cán chảo",
             """- viền và chỗ hai vây như cũ;
- vây xanh thẫm, mặt dưới xanh nhạt hơn; chóp hai vây khép về phía khoảng trống (chỗ cán chảo);
- không vẽ chảo, thân, ngón tay, móng.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two short flippers that reach across the front of the belly (the body is not shown) and hold an object between them (the object is another group). The viewer-left flipper is the wide one: its root is at its LEFT end, its rounded tip at the right. The viewer-right flipper is smaller: its root is at its RIGHT end, its tip at the left. Redraw THESE two pieces as the flippers of image 2 (the approved concept): dark navy flippers with a lighter blue underside, the tips closed toward the gap between them, as if gripping the pan's handle there.
Do NOT draw: the frying pan, the body, claws, fingers.""", None),
            ("N06", "đuôi và hai bàn chân", "tail and feet", "giu", 8,
             "a pointed blue tail at the upper left (narrow tip at the top, wide end at the bottom right) and two flat orange webbed feet at the bottom",
             "Đuôi xanh nhọn ở trên trái (chóp hẹp ở trên, đầu rộng ở dưới phải là chỗ giấu sau thân) và hai bàn chân màng cam phẳng ở dưới: chân trái dưới đuôi, chân phải ở bên phải",
             """- đuôi và hai bàn chân đúng chỗ, đúng cỡ, đúng hướng cũ;
- đuôi xanh thẫm, chóp nhọn ở trên trái; hai bàn chân màng hồng nhạt;
- không vẽ thân, không vẽ chân dài.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a short pointed tail (its narrow tip at the TOP LEFT, its wide end at the bottom right, where it hides behind the body) and two flat orange webbed feet at the bottom (the viewer-left foot under the tail, the viewer-right foot at the right). The body is not shown. Redraw THESE pieces as image 2 (the approved concept) shows them: a short pointed dark navy tail and two flat pale-pink webbed feet, each in its old place, size and direction.
Do NOT draw: the body, legs, orange feet.""", None),
        ],
        "extra": [],
        "first": ["N02", "N04"],  # gen thử trước: đầu liền thân có mặt (giữ viền), chảo (đổi dáng)
    },
    {
        "code": "canh_cut_2", "elem": "thuy", "aola": 1692,
        "hero": "Cánh Cụt", "form": 2, "forms": 2, "form_name": "Đầu Bếp Cánh Cụt",
        "role_vi": "tướng Thường hệ Thủy (ải 10 đảo Thủy), dạng 2/2, rig aola #1692",
        "design_vi": ("cánh cụt bếp trưởng, lớn lên từ dạng 1: cùng màu xanh thẫm, bụng trắng, mắt to lòng trắng, mày lông vàng dài "
                      "xếch thành chùm lông nhọn hai bên đầu; mỏ cam đỏ há như đang hô; mào lông nhọn trên đỉnh; mũ bếp trắng cao có "
                      "nếp, đai xanh trời, nghiêng trái; cổ áo bếp trắng viền xanh trời, tạp dề trắng mép sóng xanh trời; khăn xanh "
                      "trời nút to giữa ngực; vây trái cuộn như nắm đấm; vây phải đỡ khay băng trong có ba con cá nướng; chim cánh cụt "
                      "con lông tơ xám (phụ bếp) ngồi trước chân ôm cá nướng; chân hồng nhạt; oai, quả quyết"),
        "rig_vi": ("con gốc #1692 là chim cánh cụt mập đứng nhìn thẳng hơi quay phải: đầu tròn to (mỏ há), chỏm lông trên đỉnh, mũ "
                   "bếp phồng nghiêng bên trái đầu, cổ áo hai miếng và tạp dề, khăn nút giữa ngực hai vạt rủ, vây trái giơ trước "
                   "người như giơ ngón cái, vây phải giấu sau thân đỡ cái đĩa chìa ra bên phải có ba bánh cá, đuôi lộ sau thân ở "
                   "dưới trái, hai bàn chân màng, chim cánh cụt con tím ngồi trước chân ôm bánh cá. Bỏ khỏi bóng xám: bóng, vòng "
                   "băng có sao băng, hơi nóng bốc trên đĩa"),
        "regions_vi": ("1 chỏm lông, 2 mũ bếp, 3 đầu và mặt, 4 mỏ há, 5 thân, 6 cổ áo và tạp dề, 7 khăn, 8 vây trái, 9 vây phải "
                       "(gần như khuất sau thân, đỡ đĩa), 10 đĩa, 11 ba món trên đĩa, 12 đuôi, 13 hai bàn chân, 14 chim cánh cụt "
                       "con"),
        "anchor": True,
        "prev": [("canh_cut_1", "the approved FIRST stage of this evolution line: keep its colours, crest, face, brows, beak, "
                                "neckerchief and drawing style",
                  "dạng 1, cánh cụt con tập sự bếp: xanh thẫm, bụng trắng, mày lông vàng xếch, mỏ cam đỏ, khăn bếp xanh trời, "
                  "cầm chảo gang. Giữ màu, mào, mặt, mày, mỏ, khăn, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: the SECOND and final stage of a two-stage Water evolution line whose first stage is image 6. The scrappy apprentice penguin cook of image 6 has grown into a big, proud HEAD CHEF of the icy seas: a chubby, strong penguin in a chef's toque and apron, one flipper raised in a fist, the other holding out a platter of clear ice with three grilled fish, and its own tiny chick apprentice sitting at its feet. Same front view (turned a little to the viewer's right) and pose as image 1, on a plain white background. Not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one big round head with a small crest on top and a chef's hat on its viewer-left side, one open beak, one chubby body, two jacket collar pieces at the neck and an apron over the belly, a neckerchief (a band across the chest, a knot near the centre, two tails hanging down), two flippers, one platter with three grilled fish on it, one short tail, two flat webbed feet, and one tiny chick sitting in front of the feet hugging a small fish; no arms or hands, no legs showing, no wings, no extra limbs;
- every joint where it is: the head sits on the body (no neck shows); the crest stands on top of the head and the hat sits tilted on the upper viewer-left of the head; the collar pieces sit at both sides under the face; the apron covers the belly; the neckerchief wraps across the chest under the face, its knot a little right of centre; the viewer-left flipper is held up in front of the body at the left; the viewer-right flipper rises behind the body on the right and holds the platter up from below (it is almost hidden); the platter is held out at the viewer-right, level with the chin; the tail sticks out from behind the lower left of the body; the feet sit flat under the bottom of the body; the chick sits on the ground in front of the feet, a little right of centre;
- every part pointing the same way: the face is turned a little to the viewer's right; the hat leans to the upper left; the crest's feathers point up; the two neckerchief tails hang down, the right one longer and flaring out to the lower right; the tip of the viewer-left flipper curls up; the platter lies flat, seen almost edge-on, its long side running left to right; the tail's tip points down to the lower right;
- the head, the body, the flippers and the feet about the size and shape of regions 3, 5, 8, 9 and 13; the whole figure about the same height.

CHANGE (the new look, region by region):
1 crest: a spiky crest of navy feathers on top of the head, a little bigger than in image 6.
2 hat: a tall pleated white chef's toque with a sky-blue band, leaning to the upper left, about the size of region 2 or a little taller.
3 head: the same dark navy head and face as image 6, grown up: two big round eyes (a white eye-white, a large dark pupil, one small catchlight dot) under long bright yellow feather brows that angle down toward the beak and sweep out into spiky plumes at the sides of the head; a white throat under the beak. No blush on the cheeks.
4 beak: a bigger orange-red beak, open in a confident battle shout, a small red mouth inside.
5 body: a big chubby body: navy sides and a white belly.
6 collar and apron: the white collar of a chef's jacket with sky-blue piping, in two pieces at both sides under the face; a white apron with a sky-blue wavy hem over the belly, its bottom edge following the lower outline of region 6.
7 neckerchief: the sky-blue neckerchief of image 6 grown big, with a thin white edge: a band across the chest, a big knot and two tails hanging down.
8 viewer-left flipper: a short navy flipper with a lighter blue underside, curled up in front of the body like a fist ready to punch, its tip curled up where region 8 has a bump at the top.
9 viewer-right flipper: navy, raised behind the body, holding the platter up from below; only small bits of it show.
10 platter: a flat oval platter carved from clear pale-blue ice, with a frosty white rim, held out at the viewer-right like region 10.
11 food: three grilled fish lying on the platter, golden brown with dark grill stripes, their tails curled up, piled like region 11.
12 tail: a short pointed navy tail.
13 feet: two flat webbed feet, pale pink.
14 chick: a tiny round penguin chick of fluffy pale-grey down with a white face, two tiny yellow brow tufts, small fierce open eyes, a stubby orange-red beak and pink feet, hugging a small grilled fish to its chest: the head chef's own little apprentice, about the size of region 14.

ATTITUDE: a proud, fiery head chef ready to fight: brows angled down, the beak open in a confident shout, the fist raised, the platter held high; the chick looks just as determined; strong and chubby, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those. Image 6 is the approved first stage of this line: keep its colours, crest, face, brows, beak, neckerchief and drawing style, so both stages read as the same creature growing up.

COLOURS: as in image 6: dark navy blue with a lighter blue on the flipper undersides; white belly, collar, apron and hat; sky-blue neckerchief, hat band and trims; bright yellow brows; an orange-red beak; pale pink feet; clear pale-blue ice; golden brown fish; a pale grey chick. Few colours.

AVOID: a bright sky-blue body, a white face, a tan belly, pink blush cheeks, a red scarf, a white porcelain plate, cakes or pastries, a purple chick, a chick with closed eyes, a frying pan, steam or smoke, ice crystals, snowflakes or rings around the creature (the game adds them), a human face or body, arms or hands, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #1692, khung đứng đầu (44 mảnh): 1 bóng, 2 và 44 vòng băng có sao băng, 41 và 42 hơi nóng (giữ gốc); 3 chân trái,
        # 4 đuôi, 5 chân phải, 6 vây phải (sau thân, đỡ đĩa), 7 thân, 8 đầu, 9 và 21 cổ áo, 10 tạp dề, 11 mỏ, 12 miệng, 13 lưỡi,
        # 14 và 15 má, 16 mắt phải, 43 mắt trái, 17 và 33 dải khăn, 34 nút khăn, 19 và 20 hai vạt, 18 vây trái, 22-32 chim con
        # (thân, chân, má, bánh cá, vây, mỏ, mắt), 35 chỏm lông, 36 mũ bếp, 37 đĩa, 38-40 ba bánh cá. Đòn đánh tung chim con lao
        # tới đối thủ (hình chim con trượt to là biến thể): xử lý khi ghép.
        "groups": [
            ("N01", "mào lông và mũ bếp", "head crest and chef hat", "doi", 12,
             "a puffy white chef hat at the left, tilted; a blue crest of rounded feathers at the right, its flat bottom edge on the head",
             "Mũ bếp trắng phồng ở bên trái (nghiêng sang trái, đáy mũ ở dưới phải là chỗ đội lên đầu); chỏm lông xanh ba thùy tròn ở bên phải, mép dưới phẳng cắm vào đỉnh đầu",
             """- đáy mũ và mép dưới chỏm lông đúng chỗ cũ;
- mũ bếp trắng cao có nếp gấp, đai xanh trời, nghiêng lên trái; chỏm lông xanh thẫm nhọn dựng lên;
- không vẽ đầu, mặt.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design). At the LEFT, a puffy white chef hat tilted to the left; its bottom, at its lower right, sits on the upper viewer-left of the head (the head is not shown). At the RIGHT, a blue crest of three rounded feathers; its flat BOTTOM edge sits on the top of the head. Redraw THESE two pieces as image 2 (the approved concept) shows them: the tall pleated white chef's toque with a sky-blue band, leaning to the upper left, its bottom where the old hat's bottom is; the spiky crest of navy feathers, its base along the old bottom edge. Each about the size of the old piece; the hat may be a little taller.
Do NOT draw: the head, a face, round blue lobes.""", "bottom of the hat and the base of the crest"),
            ("N02", "đầu, mặt, mỏ", "head with face and beak", "doi", 10,
             "a big round head: blue top and sides, white face with two black eyes, pink cheeks and an open yellow beak; tan chin at the bottom",
             "Đầu tròn to (1024 × 1024, nền trắng): đỉnh và hai bên xanh, mặt trắng, hai mắt đen, má hồng, mỏ vàng há có lưỡi đỏ hơi lệch phải; cằm nâu nhạt ở dưới",
             """- mép dưới (cằm), hai mắt, mỏ đúng chỗ cũ; đầu cỡ như cũ;
- đầu và mặt xanh thẫm như concept, họng trắng dưới mỏ; mắt to lòng trắng, con ngươi đen, một chấm sáng; mày lông vàng dài xếch, chùm lông nhọn ở hai bên đầu;
- mỏ cam đỏ há như đang hô, miệng đỏ nhỏ; không má hồng, không thè lưỡi;
- không vẽ mũ, mào trên đỉnh, khăn, thân.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a big round head: blue top and sides, a white face with two black eyes and pink cheeks, an open yellow beak with a tongue a little right of centre, a tan chin at the bottom. Redraw THESE pieces as the head of image 2 (the approved concept): the dark navy head and face with a white throat under the beak; the two big round eyes (a white eye-white, a large dark pupil, one small catchlight dot) exactly where the old eyes are, under long bright yellow feather brows that angle down toward the beak and sweep out into spiky plumes at the sides of the head; the bigger orange-red beak, open in a confident shout with a small red mouth inside, where the old beak is.
Keep the bottom edge (the chin) where it is and the head about the same size: the hat, the crest, the collar and the neckerchief are drawn over it in other groups.
Do NOT draw: the chef hat, the crest on top, the neckerchief, the body, pink cheeks, a white face, a tongue sticking out.""", "eyes, beak and the bottom edge (the chin)"),
            ("N03", "thân, cổ áo, tạp dề", "body, collar and apron", "giu", 10,
             "a chubby body: tan front, blue sides, white top; two white collar pieces with a blue stripe at the top corners; a light-blue apron with a wave pattern and a bottom edge with two V points",
             "Thân mập (1024 × 1024, nền trắng): trước nâu nhạt, hai bên xanh, đỉnh trắng; hai miếng cổ áo trắng sọc xanh ở hai góc trên; tạp dề xanh nhạt hoa văn sóng, mép dưới có hai mũi chữ V",
             """- viền thân như cũ; hai miếng cổ áo và tạp dề đúng chỗ, đúng cỡ;
- thân hai bên xanh thẫm, bụng trắng; cổ áo bếp trắng viền xanh trời; tạp dề trắng mép sóng xanh trời, mép dưới như cũ;
- không vẽ đầu, khăn, vây, chân, chim con.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a chubby body (a tan front, blue sides, a white top where the head goes over it); at its top corners two white collar pieces with a blue stripe; over the belly a light-blue apron with a wave pattern and a bottom edge with two V points. Redraw THESE pieces as the body of image 2 (the approved concept), keeping the outline: navy sides and a white belly; the two collar pieces become the white collar of a chef's jacket with sky-blue piping; the apron becomes the white apron with a sky-blue wavy hem, the same outline and bottom edge.
Do NOT draw: the head, the neckerchief, the flippers, the feet, the chick, a tan belly, a light-blue apron.""", None),
            ("N04", "khăn bếp", "neckerchief", "doi", 9,
             "a red neckerchief: a band across the chest, a round knot a little right of centre, two tails hanging down (the right one longer, flaring to the lower right)",
             "Khăn đỏ (1024 × 1024, nền trắng): dải khăn vắt ngang ngực, nút tròn hơi lệch phải, hai vạt rủ xuống (vạt trái thẳng xuống, vạt phải dài xòe xuống phải)",
             """- dải, nút, hai vạt đúng chỗ, đúng hướng cũ;
- khăn xanh trời viền trắng mảnh như dạng 1; không khăn đỏ;
- không vẽ thân, đầu, cổ áo.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a red neckerchief: a band across the chest from the left to the right (the body is not shown), a round knot a little right of centre, and two tails hanging down from the knot (the left one straight down, the right one longer, flaring out to the lower right). Redraw THESE pieces as the neckerchief of image 2 (the approved concept): sky-blue with a thin white edge, the band along exactly the old line, the knot where the old knot is, both tails in the places and directions of the old tails, about the same size.
Do NOT draw: the body, the head, the collar, a red scarf.""", "band line and the knot"),
            ("N05", "hai vây", "two flippers", "giu", 9,
             "two flippers: at the left a round blue mitten with a thumb-like bump at the top; at the right a long dark-blue flipper with a tan palm, wide at the top, pointed at the bottom",
             "Hai vây (1024 × 1024, nền trắng): bên trái vây tròn như găng có cục ngón cái ở trên; bên phải vây dài xanh thẫm có lòng nâu nhạt, đầu rộng ở trên (đỡ đĩa), nhọn ở dưới",
             """- viền và chỗ hai vây như cũ;
- vây trái xanh thẫm, mặt dưới xanh nhạt, cuộn lại như nắm đấm, chóp cong lên ở chỗ cục ngón cái cũ;
- vây phải xanh thẫm, mặt dưới xanh nhạt (thay lòng nâu nhạt), đầu rộng ở trên;
- không vẽ khay, thân, ngón tay.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design). At the LEFT, the viewer-left flipper: a round mitten-like flipper held up in front of the body, with a thumb-like bump at its top. At the RIGHT, the viewer-right flipper: a long dark-blue flipper with a tan palm; it rises behind the body, its wide TOP end holding the platter up from below, its narrow pointed end at the bottom. Redraw THESE two pieces as the flippers of image 2 (the approved concept): dark navy with a lighter blue underside (instead of the tan palm); the viewer-left one curled up like a fist ready to punch, its tip curled up where the bump is.
Do NOT draw: the platter, the body, fingers, a thumbnail, claws.""", None),
            ("N06", "khay băng cá nướng", "ice platter with grilled fish", "doi", 15,
             "a white plate seen almost edge-on with three golden fish-shaped cakes piled on it",
             "Đĩa trắng nhìn gần ngang (1024 × 1024, nền trắng) với ba bánh cá vàng chất lên, chiếc lớn nhất nằm trên cùng",
             """- khay đúng chỗ, đúng cỡ, đúng độ nghiêng của đĩa cũ; ba con cá nằm đúng chỗ ba bánh cũ;
- khay băng trong xanh nhạt, mép sương trắng; **đúng ba** con cá nướng vàng nâu có sọc nướng sẫm, đuôi cong lên (concept vẽ bốn con, rig chỉ có ba mảnh món ăn);
- không vẽ hơi nóng, bánh, đĩa sứ trắng, vây.""",
             """Image 1 is four pieces of a 2D cut-out animation puppet (the old design): a flat white plate seen almost edge-on and three golden fish-shaped cakes piled on it, the biggest one on top. A flipper holds the plate up from below at its left part (the flipper is another group). Redraw THESE pieces as image 2 (the approved concept) shows them: a flat oval platter carved from clear pale-blue ice with a frosty white rim, in the place, size and tilt of the old plate; exactly THREE grilled fish, golden brown with dark grill stripes, their tails curled up, each in the place of an old cake and about its size (image 2 shows four fish: draw only three, one for each old cake, because each fish is a separate puppet piece).
Do NOT draw: steam, cakes or pastries, a white porcelain plate, the flipper, a fourth fish.""", "plate's place and tilt"),
            ("N07", "đuôi và hai bàn chân", "tail and feet", "giu", 9,
             "a blue tail at the left (rounded upper left, pointed lower right) and two flat orange webbed feet at the bottom",
             "Đuôi xanh ở bên trái (đầu tròn ở trên trái, nhọn ở dưới phải) và hai bàn chân màng cam phẳng ở dưới: chân trái dưới đuôi, chân phải ở bên phải",
             """- đuôi và hai bàn chân đúng chỗ, đúng cỡ cũ;
- đuôi xanh thẫm; hai bàn chân màng hồng nhạt như dạng 1;
- không vẽ thân, chim con.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a tail (rounded at its upper left, narrowing to a point at its lower right; it sticks out from behind the body, which is not shown) and two flat orange webbed feet at the bottom (the viewer-left foot under the tail, the viewer-right foot at the right). Redraw THESE pieces as image 2 (the approved concept) shows them: a short dark navy tail and two flat pale-pink webbed feet, each in its old place, size and direction.
Do NOT draw: the body, legs, the chick, orange feet.""", None),
            ("N08", "chim cánh cụt con phụ bếp", "chick helper", "doi", 25,
             "a tiny purple penguin chick sitting, eyes squeezed shut, hugging a golden fish-shaped cake, two small feet at the bottom",
             "Chim cánh cụt con tím ngồi (1024 × 1024, nền trắng): mắt nhắm tịt hình > <, má hồng, mỏ vàng, hai vây ôm bánh cá vàng trước ngực, hai bàn chân nhỏ ở dưới",
             """- chim con đúng chỗ, cỡ như cũ, hai bàn chân ở dưới đúng chỗ cũ;
- lông tơ xám nhạt, mặt trắng, hai túm mày vàng nhỏ, mắt nhỏ mở quả quyết, mỏ cam đỏ, chân hồng, ôm con cá nướng nhỏ;
- không tím, không mắt nhắm, không bánh.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a tiny penguin chick sitting on the ground, its eyes squeezed shut, hugging a golden fish-shaped cake to its chest with its two small flippers, two small feet at the bottom. Redraw THESE pieces as the chick of image 2 (the approved concept): a tiny round penguin chick of fluffy pale-grey down with a white face, two tiny yellow brow tufts, small fierce open eyes, a stubby orange-red beak and pink feet, hugging a small grilled fish (golden brown with dark grill stripes) to its chest; in the same place and about the same size, the feet where the old feet are.
Do NOT draw: the big penguin, purple colours, closed eyes, a cake.""", "feet and its place on the ground"),
        ],
        "extra": [],
        "first": ["N02", "N03"],  # gen thử trước: đầu (đổi dáng), thân có tạp dề (giữ viền)
    },
    # Dòng Mi Nhi (aola 983 → 984), tướng Khá ải 15 đảo Thủy, "Tiên cầm sóng biếc". Người dùng chốt 2026-11-06: giữ tiên cá DẠNG
    # NGƯỜI (ngoại lệ thứ hai của luật "tướng là thú nuôi", như dòng Tiểu Y), thiết kế theo DESIGN_CHIBI. Thiết kế mới khác bản gốc
    # (tóc xanh ngọc, kẹp sao vàng, mắt xanh lá, đàn vàng đỏ, đuôi xanh lam): tóc tím oải hương ngọn bọt trắng, mắt xanh sapphire, kẹp
    # vỏ sò hồng giữ ngọc trai, đuôi xanh ngọc bích vây tím nhạt, đàn san hô và xương trắng ngà dây bạc. Vòng sao (tự chạy) giữ hình
    # gốc: bỏ khỏi bóng xám, không có nhóm. Bộ ghép: <aola>/reskin/thuy_983, thuy_984 (regions.json, groups.json). Viền px = 0,85%
    # chiều cao cả con trong RegionMap × tỉ lệ phóng của orig/Nxx.png.
    {
        "code": "mi_nhi_1", "elem": "thuy", "aola": 983,
        "hero": "Mi Nhi", "form": 1, "forms": 2, "form_name": "Tiểu Mi",
        "role_vi": "tướng Khá hệ Thủy (ải 15 đảo Thủy), dạng 1/2, rig aola #983",
        "design_vi": ("tiên cá nhỏ chơi đàn dạng người (người dùng chốt 2026-11-06: giữ tiên cá dạng người): bé gái chibi tóc tím oải "
                      "hương, mái và lọn tóc cuộn bọt trắng ở ngọn, một lọn tóc dựng cong trên đỉnh; vây tai xanh nhạt gân tím viền trắng "
                      "ngọc; kẹp vỏ sò hồng giữ ngọc trai trắng; da hồng nhạt, mắt xanh sapphire to, mày xếch quả quyết; áo vảy vỏ sò "
                      "hồng nhạt; tay mũm mĩm đeo vòng ngọc trai; đàn lia nhỏ bằng san hô trắng hồng, dây bạc, ngọc trai trên đỉnh, đế "
                      "vỏ ốc hồng; đuôi cá xanh ngọc bích vảy chấm đậm, vây tím nhạt"),
        "rig_vi": ("con gốc #983 là bé tiên cá chibi nhìn thẳng hơi quay phải: đầu rất to, mái tóc dày, hai lọn tóc hai bên mặt, một "
                   "lọn tóc dựng cong trên đỉnh vắt sang phải, tóc dài phía sau xõa xuống dưới trái, một vây tai to sau bên trái đầu, "
                   "kẹp sao ở trên trái đầu; thân nhỏ dưới đầu; hai tay ngắn với sang phải gảy cây đàn lia nhỏ dựng ở bên phải; dưới "
                   "là đuôi cá ngắn cuộn ở dưới, vây nhỏ chĩa trái. Bỏ khỏi bóng xám: bóng dưới chân và vòng sao"),
        "regions_vi": ("1 vây tai, 2 tóc trên đầu (mái, lọn hai bên, lọn dựng trên đỉnh), 3 tóc dài phía sau, 4 mặt, 5 kẹp tóc, "
                       "6 thân, 7 tay sau, 8 tay trước, 9 đàn lia, 10 đuôi cá"),
        "anchor": True, "design": DESIGN_CHIBI,
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original character: a LITTLE MERMAID BARD, a chibi mermaid girl who fights with music, plucking a small lyre to raise the waves, the first stage of a two-stage Water evolution line, in the same front view (turned a little to the viewer's right) and pose as image 1, on a plain white background. An original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new character will be animated on. They tell you where each part and joint is, NOT what the character looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one big round head with its hair (thick bangs, two short locks at the sides of the face, one long curl standing on top), long back hair hanging behind, one big fin ear behind the viewer-left side of the head, one hair ornament at the upper left of the head; a small torso under the head; two short arms; one small lyre; a short fish tail with one small fin. No legs, no feet, no wings, no extra limbs;
- every joint where it is: the head sits straight on the torso (no neck shows); the curl grows from the top of the head; the back hair grows from the back of the head; the fin ear grows from behind the viewer-left side of the head; the arms start at the shoulders at the top of the torso; the tail starts at the bottom of the torso;
- every part pointing the same way: the face is turned a little to the viewer's right; the curl rises from the top of the head and arcs over to the right, its tip pointing down-right; the fin ear opens up and out to the left; the back hair sweeps down to the lower left; both arms reach to the viewer's right toward the lyre, the front hand on the strings; the lyre stands upright at the right, its scroll at the upper right and its base at the bottom; the tail curls at the bottom, its small fin pointing to the left and its end curving down to the lower right;
- the head and hair together about the size and shape of regions 2, 3 and 4 (more than half of the figure: a chibi); the torso, the arms, the lyre and the tail about the size of regions 6, 7, 8, 9 and 10; the whole figure about the same height.

CHANGE (the new look, region by region):
1 fin ear: a pale aqua fin with lilac ribs and a thin pearl-white edge, opening like a fan to the left.
2 hair on the head: lavender-lilac hair, thick soft bangs, the locks at the sides and the curl on top ending in little white sea-foam curls; the curl keeps the place and the arc of region 2's curl.
3 back hair: long lavender-lilac hair flowing down to the lower left in soft waves, its tips curling into white sea foam.
4 face: a chibi girl's face: light warm peach skin, big round sapphire-blue eyes, short brows angled down, a small determined smile.
5 hair ornament: a pink scallop-shell hair clip holding a white pearl, about the size of region 5.
6 torso: a small chibi torso with a short top of overlapping pale-pink seashell scales.
7 and 8 arms: two short chubby arms with light warm peach skin and a thin pearl bracelet on the front wrist; the front hand plucks the strings.
9 lyre: a small lyre carved from a pale coral branch, white with a soft pink tint, its arms curling like the frame of region 9, silver strings, a white pearl set in the scroll at the top, a base made of a pink conch shell.
10 tail: a short fish tail of jade-teal scales with a few darker dots and a lilac fin.

ATTITUDE: a brave little sea bard about to play a battle song: brows angled down, a small determined smile, the hand ready on the strings; cute and small, never scary, never a goofy mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those.

COLOURS: lavender-lilac hair with white foam; light warm peach skin; sapphire-blue eyes; pale aqua and lilac fin; pale-pink shells; white-pink coral and silver; jade-teal tail with a lilac fin. Few colours.

AVOID: cyan or turquoise hair, green eyes, star-shaped clips or stars, a gold lyre, an orange base, a blue tail, a dark navy fin, legs or feet, a crown, wings, armour, rings of stars or water around the character (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #983, khung đứng đầu (27 mảnh): 1 bóng, 2 và 27 vòng sao (tự chạy, giữ gốc), 3 và 4 tóc dài sau, 5 vây nhỏ của đuôi,
        # 6 và 7 lọn tóc bên phải, 8 cẳng tay sau, 9 chóp đuôi, 10 thân, 11 đế đàn, 12 đàn, 13 mặt, 14 15 mắt, 16 miệng, 17 vây
        # tai, 18 lọn tóc trước trái, 19 lọn bên phải, 20 mái, 21 lọn dựng trên đỉnh, 22 kẹp sao, 23 bắp tay sau, 24 bắp tay
        # trước, 25 bàn tay trước, 26 cẳng tay trước. Khung N05, N06, N07 nới rộng (mảnh nhỏ).
        "groups": [
            ("N01", "vây tai", "fin ear", "doi", 16,
             "a dark-blue webbed fin: its right edge is the base behind the head, ribs fanning out to a point at the left",
             "Vây tai xanh lam đậm có gân (1024 × 1024, nền trắng): mép phải dựng đứng là gốc (nằm sau đầu), các gân xòe ra trái, chóp nhọn ở trên trái và dưới",
             """- gốc (mép phải) đúng chỗ cũ, vây xòe ra trái như cũ, cỡ như cũ hoặc to hơn chút;
- vây xanh nhạt, gân tím nhạt, viền trắng ngọc mảnh;
- không vẽ đầu, tóc; không xanh lam đậm.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a webbed fin ear behind the side of a head (the head is not shown). Its RIGHT edge, standing upright, is the base where it joins the head; the ribs fan out to the left and end in points at the upper left and at the bottom. Redraw THIS piece as the fin ear of image 2 (the approved concept): a pale aqua fin with lilac ribs and a thin pearl-white edge, its base along the old right edge, opening to the left like the old fin, about the same size or a little bigger.
Do NOT draw: the head, hair, a dark navy fin.""", "right edge (the base)"),
            ("N02", "mặt", "face", "doi", 13,
             "a chibi face: pink skin, two big green eyes, a small open mouth, turned a little to the right; no hair",
             "Mặt chibi (1024 × 1024, nền trắng): da hồng, hai mắt xanh lá to (mắt trái to hơn), miệng nhỏ há, hơi quay phải; tóc là nhóm khác",
             """- mặt đúng chỗ, đúng cỡ cũ; hai mắt đúng chỗ hai mắt cũ, miệng đúng chỗ cũ;
- da hồng nhạt, mắt xanh sapphire to, mày xếch quả quyết, cười nhỏ;
- không vẽ tóc (mái tóc phủ lên mặt ở nhóm N03); không mắt xanh lá.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a chibi face turned a little to the viewer's right: pink skin, two big green eyes (the viewer-left one bigger), a small open mouth. The hair is another group drawn over it. Redraw THESE pieces as the face of image 2 (the approved concept): light warm peach skin, big round sapphire-blue eyes exactly where the old eyes are, short brows angled down, a small determined smile where the old mouth is. Keep the outline of the face (the bangs cover its top) and its size.
Do NOT draw: hair, a neck, a body, green eyes.""", "eyes, mouth and the chin"),
            ("N03", "tóc trên đầu và kẹp tóc", "hair on the head and hair clip", "doi", 9,
             "cyan bangs over the forehead, two short locks at the sides, a long curl standing on top arcing to the right, a gold star clip at the upper left",
             "Tóc xanh ngọc trên đầu (1024 × 1024, nền trắng): mái dày trùm trán, hai lọn ngắn hai bên mặt, một lọn dài dựng trên đỉnh cong sang phải, kẹp sao vàng ở trên trái; chỗ trống ở giữa dưới là chỗ của mặt",
             """- mái, hai lọn hai bên, lọn dựng trên đỉnh đúng chỗ, đúng hướng, cỡ như cũ; chỗ trống cho mặt như cũ;
- tóc tím oải hương, ngọn cuộn bọt trắng nhỏ;
- chỗ kẹp sao: kẹp vỏ sò hồng giữ ngọc trai trắng;
- không vẽ mặt, vây tai, tóc dài phía sau; không tóc xanh ngọc, không sao.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the hair on a chibi head (the face is not shown): thick cyan bangs over the forehead, two short locks at the sides of the face, one long curl standing on top that arcs over to the right with its tip pointing down-right, and a gold star clip at the upper left. Redraw THESE pieces as image 2 (the approved concept) shows them: lavender-lilac hair, the bangs, the side locks and the curl each in the place, direction and about the size of the old ones, their tips ending in little white sea-foam curls; where the star clip is, the pink scallop-shell clip holding a white pearl. Keep the open space for the face where it is.
Do NOT draw: the face, the fin ear, the long back hair, cyan hair, stars.""", "hairline around the face and the root of the curl"),
            ("N04", "tóc dài phía sau", "long back hair", "doi", 9,
             "long cyan hair hanging behind: a big wavy mass at the left ending in pointed tips at the lower left, a smaller lock at the right",
             "Tóc dài xanh ngọc phía sau (1024 × 1024, nền trắng): mảng lớn lượn sóng bên trái, ngọn nhọn ở dưới trái; lọn nhỏ hơn bên phải; mép trên là chỗ mọc từ sau đầu",
             """- hai mảng tóc đúng chỗ, đúng hướng; mép trên (chỗ mọc sau đầu) đúng chỗ cũ;
- tóc tím oải hương lượn sóng, ngọn cuộn bọt trắng;
- không vẽ đầu, mặt, vây tai; không tóc xanh ngọc.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): long hair hanging behind the head and body: a big wavy mass at the left that sweeps down to pointed tips at the lower left, and a smaller lock at the right. Their TOP edges grow from the back of the head (the head is not shown). Redraw THESE pieces as the long back hair of image 2 (the approved concept): lavender-lilac hair in soft waves, its tips curling into white sea foam, each part in the place, direction and about the size of the old one.
Do NOT draw: the head, the face, the fin ear, cyan hair.""", "top edge where the hair grows from the head"),
            ("N05", "thân", "torso", "giu", 15,
             "a small chibi torso: pink skin on top, a blue band and blue scales below",
             "Thân chibi nhỏ (1024 × 1024, nền trắng, khung rộng): trên là da hồng (vai, ngực), dưới là dải xanh và vảy xanh lam",
             """- viền thân như cũ;
- da hồng nhạt ở trên, áo ngắn bằng vảy vỏ sò hồng nhạt chồng lên nhau ở dưới;
- không vẽ đầu, tay, đuôi.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a small chibi torso: pink skin at the top (the shoulders and the chest), a blue band and blue scales below. The head, the arms and the tail are other groups. Redraw THIS piece as the torso of image 2 (the approved concept), keeping its outline: light warm peach skin at the top, the short top of overlapping pale-pink seashell scales below.
Do NOT draw: the head, the arms, the tail, blue scales.""", None),
            ("N06", "hai tay", "two arms", "giu", 21,
             "two short pink arms reaching to the right: the back arm above, the front arm below it with a small hand at its right end",
             "Hai tay hồng ngắn với sang phải (1024 × 1024, nền trắng, khung rộng): tay sau ở trên, tay trước ở dưới có bàn tay nhỏ ở đầu phải; đầu trái của mỗi tay là vai",
             """- viền và chỗ hai tay như cũ; vai ở đầu trái, bàn tay ở đầu phải;
- tay mũm mĩm da hồng nhạt, vòng ngọc trai mảnh ở cổ tay trước;
- không vẽ đàn, thân.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): two short arms reaching to the viewer's right: the back arm above, the front arm below it with a small hand at its RIGHT end. The LEFT end of each arm is the shoulder. Redraw THESE pieces as the arms of image 2 (the approved concept): short chubby arms with light warm peach skin, a thin pearl bracelet on the front wrist, each in its old place, outline and direction; the front hand plucks the strings (the lyre is another group).
Do NOT put the hands at the left. Do NOT draw: the lyre, the torso, claws.""", None),
            ("N07", "đàn lia san hô", "coral lyre", "doi", 21,
             "a small golden lyre: an S-shaped frame with a scroll at the top right and a curl at the bottom left, teal strings, an orange round base at the bottom left",
             "Đàn lia vàng nhỏ (1024 × 1024, nền trắng): khung chữ S, cuộn tròn ở trên phải và ở dưới trái, dây xanh ngọc, đế tròn cam ở dưới trái",
             """- khung đàn đúng đường cong cũ, cuộn trên phải và dưới trái đúng chỗ, đế ở dưới trái; cỡ như cũ;
- khung bằng san hô trắng ánh hồng, dây bạc, ngọc trai trắng ở cuộn trên, đế là vỏ sò điệp hồng như concept;
- không vẽ bàn tay; không vàng, không cam.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a small lyre standing upright: an S-shaped gold frame with a scroll at the TOP RIGHT and a curl at the bottom left, teal strings, and a round orange base at the bottom left. A hand plucks it (the hand is another group). Redraw THESE pieces as the coral lyre of image 2 (the approved concept): the frame carved from pale coral, white with a soft pink tint, along exactly the old curve, silver strings, a white pearl set in the top scroll, a base made of a pink scallop shell where the orange base is, as in the concept; about the same size.
Do NOT draw: the hand, a gold frame, an orange base, glowing effects.""", "frame curve and the base"),
            ("N08", "đuôi cá", "fish tail", "giu", 16,
             "a short blue fish tail: a small fin pointing left at the upper left, the tail end curving down to a point at the lower right",
             "Đuôi cá xanh lam ngắn (1024 × 1024, nền trắng): vây nhỏ chĩa trái ở trên trái, chóp đuôi cong xuống thành mũi nhọn ở dưới phải; mép trên là chỗ nối thân",
             """- viền đuôi và vây như cũ; vây chĩa trái, chóp đuôi cong xuống phải;
- vảy xanh ngọc bích có chấm đậm, vây tím nhạt;
- không vẽ thân, chân; không xanh lam.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a short fish tail: a small fin pointing to the left at the upper left, and the tail end curving down to a point at the lower right. Its top edge joins the torso (the torso is not shown). Redraw THESE pieces as the tail of image 2 (the approved concept), keeping their outline: jade-teal scales with a few darker dots, a lilac fin.
Do NOT draw: the torso, legs, feet, a blue tail.""", None),
        ],
        "extra": [],
        "first": ["N02", "N06"],  # gen thử trước: mặt (đổi dáng), hai tay (giữ viền)
    },
    {
        "code": "mi_nhi_2", "elem": "thuy", "aola": 984,
        "hero": "Mi Nhi", "form": 2, "forms": 2, "form_name": "Mi Nhi",
        "role_vi": "tướng Khá hệ Thủy (ải 15 đảo Thủy), dạng 2/2, rig aola #984",
        "design_vi": ("tiên cá nghệ sĩ dạng người, lớn lên từ dạng 1: tóc tím oải hương rất dài bay ra sau, ngọn cuộn bọt trắng, lọn "
                      "dựng trên đỉnh; quạt san hô hồng hai thùy cài sau đầu; vây tai xanh nhạt gân tím; kẹp vỏ sò hồng giữ ngọc trai; "
                      "mắt xanh sapphire, mày xếch quả quyết; áo lụa biển tím nhạt có chuỗi ngọc trai, diềm vây xanh nhạt ở hai vai; khăn "
                      "quấn hông trắng ngọc viền tím; đuôi cá xanh ngọc bích vây tím nhạt; tay da hồng nhạt, vòng ngọc trai; đàn hạc cao "
                      "khung xương trắng ngà uốn như sóng, cuộn san hô hồng trên đỉnh, chân xoắn vỏ ốc, dây bạc"),
        "rig_vi": ("con gốc #984 là tiên cá chibi nhìn thẳng hơi quay phải, đứng cạnh cây đàn hạc cao hơn người: đầu to tóc ngắn có mái, "
                   "hai kẹp sao, một lọn dựng trên đỉnh bên phải; vật trang trí hình lá dựng sau trên trái đầu; vây tai xanh đậm sau bên "
                   "trái đầu; tóc rất dài bay ra sau xuống dưới trái; thân nhỏ, áo hai vỏ sò, diềm ở hai vai; khăn sọc quấn hông; đuôi cá "
                   "đi xuống, vây ở dưới trái; tay trước duỗi sang phải, bàn tay xòe trên dây đàn; tay sau ở sau dây đàn; đàn hạc dựng "
                   "bên phải: cuộn đỏ ở trên trái sau đầu, khung vòng qua bên phải xuống chân xoắn vàng ở dưới. Bỏ khỏi bóng xám: bóng "
                   "và vòng sao"),
        "regions_vi": ("1 vật trang trí sau đầu, 2 đầu và mặt, 3 lọn tóc dựng trên đỉnh, 4 tóc rất dài phía sau, 5 vây tai, 6 thân, "
                       "áo và diềm vai, 7 khăn quấn hông, 8 đuôi cá, 9 tay trước, 10 tay sau, 11 đàn hạc"),
        "anchor": True, "design": DESIGN_CHIBI,
        "prev": [("mi_nhi_1", "the approved FIRST stage of this evolution line: keep its colours, hair, face, eyes, fin ear, "
                              "shell clip and drawing style",
                  "dạng 1, tiên cá nhỏ chơi đàn lia: tóc tím oải hương ngọn bọt trắng, mắt xanh sapphire, vây tai xanh nhạt gân "
                  "tím, kẹp vỏ sò hồng giữ ngọc trai, đuôi xanh ngọc bích vây tím. Giữ màu, tóc, mặt, mắt, vây tai, kẹp, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original character: the SECOND and final stage of a two-stage Water evolution line whose first stage is image 6. The little mermaid bard of image 6 has grown into a MERMAID MAESTRO: an older chibi mermaid girl with very long flowing hair, standing beside a tall harp taller than herself, one hand sweeping the strings to call up the waves. Same front view (turned a little to the viewer's right) and pose as image 1, on a plain white background. Not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new character will be animated on. They tell you where each part and joint is, NOT what the character looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one big head with short hair and bangs and its hair clips, one curl standing on top at the right, one ornament standing up behind the upper left of the head, very long hair streaming behind, one fin ear behind the viewer-left side of the head; a small torso with frills at both shoulders; a wrap around the hips; a fish tail; two arms; one very tall harp. No legs, no feet, no wings, no extra limbs;
- every joint where it is: the head sits on the torso (no neck shows); the curl grows from the top of the head; the ornament stands behind the upper left of the head; the long hair grows from the back of the head; the fin ear grows from behind the viewer-left side of the head; the arms start at the shoulders; the hip wrap sits at the bottom of the torso; the tail goes down from the hips; the harp stands on the ground at the right, its top scroll behind the upper left of the head;
- every part pointing the same way: the face is turned a little to the viewer's right; the curl arcs up and over to the right; the ornament points up and to the upper left; the long hair streams down to the lower left almost to the ground; the fin ear points to the left; the front arm stretches to the right at chest height with the open hand on the strings, fingers spread; the back hand is on the strings behind, at the right; the tail goes down and curves to the left, its forked fin at the lower left; the harp frame arcs from its top scroll at the upper left over the right side and down to a spiral foot at the bottom, its strings standing upright;
- the head about the size of region 2 (a chibi), the torso, the arms and the tail about the size of regions 6, 8, 9 and 10, the harp as tall as region 11; the whole figure about the same height.

CHANGE (the new look, region by region):
1 ornament: a pale-pink sea-fan coral ornament with two lobes standing up behind the head, about the size of region 1.
2 head: the same face as image 6, a little older: light warm peach skin, big sapphire-blue eyes under short brows angled down, a small determined open mouth as if singing a battle song; short lavender-lilac hair with thick bangs; the pink scallop-shell clip with a white pearl of image 6 where region 2's clips are.
3 curl: a lavender-lilac curl of hair arcing over to the right, its tip curling into white sea foam.
4 long hair: very long lavender-lilac hair streaming down to the lower left in big soft waves, its tips curling into white sea foam.
5 fin ear: the fin ear of image 6 grown sharper: pale aqua with lilac ribs and a pearl-white edge.
6 torso: a short top of lilac sea-silk with a string of small pearls, little frilly fins of pale aqua at both shoulders.
7 hip wrap: a sash of pearl-white sea-silk with a lilac edge wrapped around the hips, one end hanging down at the right.
8 tail: a fish tail of jade-teal scales with a few darker dots and a lilac forked fin.
9 front arm: light warm peach skin, a pearl bracelet at the wrist, an open hand sweeping the strings.
10 back arm: the same skin, its hand on the strings behind.
11 harp: a tall harp whose frame is a curving wave of pearl-white bone, a coral-pink scroll at the top, a spiral foot shaped like a pale lilac sea-snail shell at the bottom, four silver strings; the same height and place as region 11.

ATTITUDE: a proud young sea maestro calling up a storm with her harp: brows angled down, a determined open mouth singing, the hand sweeping the strings; graceful and strong, never scary, never a goofy mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those. Image 6 is the approved first stage of this line: keep its colours, hair, face, eyes, fin ear, shell clip and drawing style, so both stages read as the same character growing up.

COLOURS: as in image 6: lavender-lilac hair with white foam; light warm peach skin; sapphire-blue eyes; pale aqua and lilac fins; pale-pink coral and shells; pearl white; jade-teal tail with a lilac fin; silver strings. Few colours.

AVOID: cyan or turquoise hair, green eyes, star-shaped clips or stars, a red or gold harp, a blue tail, a striped blue sash, a dark navy fin, legs or feet, a crown, wings, armour, rings of stars or water around the character (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #984, khung đứng đầu (26 mảnh): 1 bóng, 2 và 26 vòng sao (tự chạy, giữ gốc), 3 bắp tay sau, 4 bàn tay sau, 5 đàn
        # hạc, 6 và 7 vật trang trí hình lá, 8 tóc dài, 9 và 19 diềm vai, 10 vây đuôi, 11 và 12 đuôi, 13 thân, 14 15 hai vỏ sò,
        # 16 đuôi khăn, 17 và 18 khăn quấn hông, 20 vây tai, 21 lọn dựng trên đỉnh, 22 bắp tay trước, 23 bàn tay trước, 24 cẳng tay
        # trước có vòng, 25 đầu (cả mặt, mái, kẹp sao). Khung N01, N04, N05, N06 nới rộng (mảnh nhỏ).
        "groups": [
            ("N01", "quạt san hô sau đầu", "sea-fan ornament", "doi", 16,
             "a light-blue two-lobed leaf ornament pointing up-left, its narrow base at the lower right",
             "Vật trang trí hình lá hai thùy xanh nhạt (1024 × 1024, nền trắng, khung rộng): chĩa lên trái, gốc hẹp ở dưới phải (cắm sau đầu)",
             """- gốc (dưới phải) đúng chỗ cũ, chĩa lên trái như cũ, cỡ như cũ;
- quạt san hô hồng nhạt hai thùy, gân san hô mảnh;
- không vẽ đầu, tóc, đàn.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): an ornament standing up behind a head (the head is not shown): two leaf-shaped lobes pointing up and to the upper left; its narrow base at the LOWER RIGHT joins the back of the head. Redraw THESE pieces as the ornament of image 2 (the approved concept): a pale-pink sea-fan coral with two lobes and fine coral ribs, its base where the old base is, pointing the same way, about the same size.
Do NOT draw: the head, hair, the harp, leaves, feathers.""", "base at the lower right"),
            ("N02", "đầu, mặt, kẹp tóc, lọn dựng", "head with face, clip and curl", "doi", 14,
             "a big head: cyan bob hair with bangs, two gold star clips at the upper left, a long curl on top at the right, a pink face with two big green eyes and a small open mouth",
             "Đầu to (1024 × 1024, nền trắng): tóc ngắn xanh ngọc có mái, hai kẹp sao vàng ở trên trái, lọn dài dựng trên đỉnh bên phải, mặt hồng, hai mắt xanh lá to, miệng nhỏ há",
             """- đầu cỡ như cũ, cằm, hai mắt, miệng đúng chỗ cũ; lọn dựng trên đỉnh đúng chỗ, đúng hướng;
- tóc tím oải hương, mái dày, ngọn cuộn bọt trắng; mắt xanh sapphire, mày xếch, miệng há nhỏ như đang hát;
- chỗ hai kẹp sao: kẹp vỏ sò hồng giữ ngọc trai như dạng 1;
- không vẽ tóc dài phía sau, vây tai, quạt san hô; không tóc xanh ngọc, không mắt xanh lá, không sao.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a big chibi head turned a little to the viewer's right: cyan bob hair with thick bangs, two gold star clips at the upper left, a pink face with two big green eyes and a small open mouth; and a long curl of hair standing on top at the right, arcing over. Redraw THESE pieces as the head of image 2 (the approved concept): short lavender-lilac hair with thick bangs and little white sea-foam curls at the tips, the curl in its old place and arc; light warm peach skin, big sapphire-blue eyes exactly where the old eyes are, brows angled down, a small determined open mouth as if singing where the old mouth is; the pink scallop-shell clip with a white pearl where the star clips are.
Keep the chin where it is and the head about the same size.
Do NOT draw: the long back hair, the fin ear, the ornament behind the head, cyan hair, green eyes, stars.""", "eyes, mouth and the chin"),
            ("N03", "tóc dài", "long hair", "doi", 9,
             "very long cyan hair streaming from the top down to the lower left in two big locks with pointed tips",
             "Tóc rất dài xanh ngọc (1024 × 1024, nền trắng): từ trên (sau đầu) bay xuống dưới trái thành hai lọn lớn, ngọn nhọn",
             """- đầu trên (chỗ mọc sau đầu) đúng chỗ cũ; hai lọn bay xuống dưới trái đúng hướng, dài như cũ;
- tóc tím oải hương lượn sóng lớn, ngọn cuộn bọt trắng;
- không vẽ đầu, mặt; không tóc xanh ngọc.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): very long hair that grows from the back of the head at the TOP and streams down to the lower left in two big locks with pointed tips. Redraw THIS piece as the long hair of image 2 (the approved concept): very long lavender-lilac hair in big soft waves, its tips curling into white sea foam, the top where the old top is, streaming the same way and as long.
Do NOT draw: the head, the face, cyan hair.""", "top where the hair grows from the head"),
            ("N04", "vây tai", "fin ear", "doi", 15,
             "a small dark-navy fin pointing left, its base at the right",
             "Vây tai nhỏ xanh tím đậm (1024 × 1024, nền trắng, khung rộng): chĩa sang trái, gốc ở bên phải (sau đầu)",
             """- gốc (bên phải) đúng chỗ cũ, chĩa trái như cũ, cỡ như cũ hoặc to hơn chút;
- vây xanh nhạt gân tím, viền trắng ngọc như dạng 1;
- không vẽ đầu; không xanh tím đậm.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a small fin ear behind the side of a head (the head is not shown), pointing to the left; its base is its RIGHT end. Redraw THIS piece as the fin ear of image 2 (the approved concept): pale aqua with lilac ribs and a thin pearl-white edge, its base where the old base is, pointing the same way, about the same size or a little bigger.
Do NOT draw: the head, a dark navy fin.""", "base at the right"),
            ("N05", "thân, áo, diềm vai", "torso, top and shoulder frills", "giu", 22,
             "a small torso: pink skin, a top of two blue scallop shells, little pale-blue frills at both shoulders",
             "Thân nhỏ (1024 × 1024, nền trắng, khung rộng): da hồng, áo hai vỏ sò xanh, diềm xanh nhạt nhỏ ở hai vai",
             """- viền thân, hai diềm vai đúng chỗ, đúng cỡ cũ;
- da hồng nhạt, áo lụa biển tím nhạt có chuỗi ngọc trai nhỏ, diềm vây xanh nhạt ở hai vai;
- không vẽ đầu, tay, khăn hông; không vỏ sò xanh.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a small torso with pink skin, a top made of two blue scallop shells, and little pale-blue frills at both shoulders. Redraw THESE pieces as the torso of image 2 (the approved concept), keeping the outline and the place of each piece: light warm peach skin, the short top of lilac sea-silk with a string of small pearls, the little frilly pale-aqua fins at both shoulders.
Do NOT draw: the head, the arms, the hip wrap, blue shells.""", None),
            ("N06", "khăn quấn hông", "hip wrap", "giu", 24,
             "a striped light-blue sash wrapped around the hips, its end hanging down at the right",
             "Khăn sọc xanh nhạt quấn hông (1024 × 1024, nền trắng, khung rộng): vòng quanh hông, một đầu khăn rủ xuống bên phải",
             """- viền khăn và đầu khăn rủ đúng chỗ cũ;
- lụa trắng ngọc viền tím nhạt, không sọc xanh;
- không vẽ thân, đuôi.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a striped sash wrapped around the hips, one end hanging down at the right. Redraw THESE pieces as the hip wrap of image 2 (the approved concept), keeping their outline and place: pearl-white sea-silk with a lilac edge.
Do NOT draw: the torso, the tail, blue stripes.""", None),
            ("N07", "đuôi cá", "fish tail", "giu", 21,
             "a blue fish tail going down from the hips, curving to the left, with a forked fin at the bottom left",
             "Đuôi cá xanh lam (1024 × 1024, nền trắng): từ hông đi xuống, cong sang trái, vây chẻ đôi ở dưới trái; mép trên là chỗ nối hông",
             """- viền đuôi và vây như cũ;
- vảy xanh ngọc bích có chấm đậm, vây chẻ đôi tím nhạt;
- không vẽ khăn hông, thân, chân; không xanh lam.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a fish tail that goes down from the hips (its TOP edge) and curves to the left, ending in a forked fin at the lower left. Redraw THESE pieces as the tail of image 2 (the approved concept), keeping their outline: jade-teal scales with a few darker dots, a lilac forked fin.
Do NOT draw: the hip wrap, the torso, legs, a blue tail.""", None),
            ("N08", "hai tay", "two arms", "giu", 21,
             "the front arm stretched to the right (upper arm, forearm with a gold bracelet, an open hand with fingers spread at the right end), the back hand above it at the right",
             "Hai tay (1024 × 1024, nền trắng): tay trước duỗi sang phải (bắp tay, cẳng tay đeo vòng vàng, bàn tay xòe ngón ở đầu phải); bàn tay sau ở trên, bên phải, ngón giơ lên; vai ở đầu trái",
             """- viền và chỗ từng mảnh như cũ; vai ở đầu trái, bàn tay xòe ở đầu phải;
- da hồng nhạt, vòng ngọc trai ở cổ tay trước (thay vòng vàng);
- không vẽ đàn, dây đàn, thân; không móng dài.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the front arm stretched to the viewer's right at chest height (its LEFT end is the shoulder; then the forearm with a gold bracelet; an open hand with fingers spread at the RIGHT end), and the back hand above it at the right with fingers raised. Redraw THESE pieces as the arms of image 2 (the approved concept): light warm peach skin, a pearl bracelet at the front wrist instead of the gold one, every piece in its old place, outline and direction; the fingers keep their old shapes.
Do NOT put the hand at the shoulder end. Do NOT draw: the harp, its strings, the torso, long nails.""", None),
            ("N09", "đàn hạc", "harp", "doi", 7,
             "a very tall red-and-gold harp: a red scroll at the top left, the frame arcing over the right side and down to a gold spiral foot at the bottom, four thin cyan strings",
             "Đàn hạc đỏ vàng rất cao (1024 × 1024, nền trắng): cuộn đỏ ở trên trái, khung vòng qua bên phải xuống chân xoắn vàng ở dưới, bốn dây xanh mảnh",
             """- khung đàn đi đúng đường cũ, cuộn trên trái và chân xoắn dưới đúng chỗ, cao như cũ;
- khung xương trắng ngà uốn như sóng, cuộn san hô hồng ở trên, chân xoắn vỏ ốc tím nhạt, bốn dây bạc;
- không vẽ tay; không đỏ, không vàng.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a very tall harp: a red scroll at the TOP LEFT, the frame arcing over the right side and down to a gold spiral foot at the BOTTOM, four thin strings standing upright inside. Hands play it (they are another group). Redraw THIS piece as the harp of image 2 (the approved concept): a frame of pearl-white bone curving like a wave along exactly the old line, a coral-pink scroll at the top, a spiral foot shaped like a pale lilac sea-snail shell at the bottom, four silver strings; the same height.
Do NOT draw: the hands, a red or gold frame, glowing effects.""", "frame line, the top scroll and the foot"),
        ],
        "extra": [],
        "first": ["N02", "N08"],  # gen thử trước: đầu (đổi dáng), hai tay (giữ viền)
    },
    # Dòng Ma Kết (aola 758 → 759 → 760), tướng Hiếm ải 20 đảo Thủy (mini boss), "Thánh giáp sừng bạc". Claude đề xuất
    # 2026-11-06, chờ duyệt concept: dê biển (thân dê, đuôi cá), khác bản gốc (lông trắng xù, xoáy lông trên trán, tai thỏ hồng,
    # mắt đỏ, sừng nâu nhạt; dạng 2 sừng tím hồng, mắt xanh ngọc; dạng 3 giáp vàng ngọc xanh lá, vây xanh tím): lông xanh mòng két,
    # mõm và len trắng kem, sừng bạc có ngấn, tai là vây cam san hô, mắt hổ phách; giáp vỏ sò điệp hồng san hô viền bạc lớn dần (dạng
    # 2 vỏ sò đeo ngực, dạng 3 mũ và giáp vai). Rig: <aola>/reskin/thuy_758, thuy_759, thuy_760 (regions.json; groups.json của
    # #758 tạm, chốt khi duyệt concept). Prompt nhóm viết sau khi duyệt concept.
    {
        "code": "ma_ket_1", "elem": "thuy", "aola": 758,
        "hero": "Ma Kết", "form": 1, "forms": 3, "form_name": "Ma Kết Con",
        "role_vi": "tướng Hiếm hệ Thủy (ải 20 đảo Thủy, mini boss), dạng 1/3, rig aola #758",
        "design_vi": ("dê biển con lơ lửng, thân dê đuôi cá: lông ngắn xanh mòng két, mõm và cằm trắng kem, chỏm len trắng kem ba lọn "
                      "nhọn trên trán (không xoáy); hai sừng bạc ngắn có ngấn; tai là vây cam san hô gân xanh mòng két; mắt hổ phách "
                      "to, vệt mày xếch; cười nhếch; thân tròn bụng kem, thon thành đuôi cá ngắn có vảy, vây đuôi cam san hô; móng "
                      "xanh thẫm; mặt quả quyết"),
        "rig_vi": ("con gốc #758 là dê biển con lơ lửng, nhìn thẳng hơi quay phải: đầu rất to lông trắng xù có xoáy lông cuộn trên "
                   "trán, hai sừng nâu nhạt (sừng trái to, sừng phải nhỏ sau đầu, cả hai chĩa lên hơi nghiêng trái), hai tai thỏ "
                   "hồng chìa ngang hai bên đầu, mắt đỏ to (mắt trái to, mắt phải nhỏ sát mép phải), má hồng; thân tròn nhỏ dưới "
                   "đầu, hai chân trước ngắn buông thẳng; thân thon thành đuôi cá ngắn ở dưới trái, vây đuôi màu kem rủ xuống. Bỏ "
                   "khỏi bóng xám: bóng dưới chân"),
        "regions_vi": ("1 sừng trái to, 2 sừng phải nhỏ, 3 tai trái, 4 tai phải, 5 đầu có mặt và hai mắt, 6 thân tròn (đuôi cá bắt "
                       "đầu ở dưới trái), 7 chân trước trái, 8 chân trước phải, 9 vây đuôi"),
        "anchor": True,
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: a little SEA-GOAT KID, a brave baby goat of the reef whose body ends in a fish tail and who fights by butting with its small silver horns, the first stage of a three-stage Water evolution line, in the same front view (turned a little to the viewer's right) and pose as image 1, floating a little above the ground, on a plain white background. A chubby baby goat with a fish tail, but an original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one big round head (more than half of the figure: a chibi baby), two horns on top of it (a big one at the viewer-left, a small one behind the head at the right), two ears sticking out at the sides of the head, one small round body under the head, two short front legs, and a short fish tail ending in one fin; no hind legs, no arms or hands, no wings, no extra limbs;
- every joint where it is: the big horn grows from the upper left of the head and the small horn from behind its upper right; the ears grow from the left and the right side of the head, just under the horns; the head sits right on the body (no neck shows); the two front legs hang side by side from the front of the body, a little right of centre; the fish tail starts at the lower left of the body and ends in the fin at the lower left of the figure;
- every part pointing the same way: the face is turned a little to the viewer's right, so the two big eyes sit a little right of the middle of the face, the viewer-left eye bigger and the viewer-right eye smaller near the right edge of the face; both horns point up, leaning a little to the left, their tips at the TOP; the viewer-left ear points out to the left, the viewer-right ear out to the right; the front legs hang straight down with the hooves at the BOTTOM; the fin hangs down at the lower left, its wide end at the bottom;
- the head, the body, the legs and the fin about the size and shape of regions 5, 6, 7, 8 and 9; the horns about as long as regions 1 and 2; the whole figure about the same height.

CHANGE (the new look, region by region):
1 and 2 horns: two short, strong silver horns with three or four ring ridges across them and pointed tips; the viewer-left one big like region 1, the viewer-right one small like region 2.
3 and 4 ears: each ear is a small fin instead of a goat ear: a coral-orange fin membrane stretched over three deep-teal ribs, its tip pointing out like region 3 and region 4.
5 head: a round, chubby kid-goat head covered in short deep-teal fur, with a cream-white muzzle and chin and a small dark nose; on the forehead a short tuft of cream-white wool in three spiky locks (no curl, no swirl). Two big round amber-gold eyes (a large dark pupil, one small catchlight dot), each under a short dark-teal brow mark angled down toward the nose: a fierce look. A small confident smirk. No blush on the cheeks.
6 body: a small round deep-teal body with a cream-white belly patch; at its lower left it narrows into a short deep-teal fish tail with a few darker scale marks.
7 and 8 front legs: two short deep-teal legs with small dark navy hooves at the bottom.
9 fin: a coral-orange tail fin with deep-teal ribs, the shape of region 9.

ATTITUDE: a scrappy little sea-goat kid ready to butt: brows angled down, a confident smirk, chin up; cute and chubby, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those.

COLOURS: deep teal fur; a cream-white muzzle, belly and forehead tuft; silver horns with grey ridges; amber-gold eyes; coral-orange fins with deep-teal ribs; dark navy hooves. Few colours.

AVOID: a white fluffy woolly head, a swirl or curl on the forehead, pink rabbit-like ears, red eyes, pink blush cheeks, tan or brown horns, a cream or tan tail fin, hind legs, a human face or body, arms or hands, wings, water rings or bubbles around the creature (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #758, khung đứng đầu (12 mảnh): 1 bóng, 2 vây đuôi, 3 thân, 4 chân trước phải, 5 chân trước trái, 6 sừng phải,
        # 7 sừng trái, 8 tai phải, 9 đầu (mũi, miệng, má liền đầu), 10 mắt trái, 11 mắt phải, 12 tai trái. Nhóm tạm (groups.json):
        # N01 hai sừng, N02 hai tai, N03 đầu có mặt, N04 thân, N05 hai chân trước, N06 vây đuôi.
        # Viền px = 0,85% chiều cao cả con trong RegionMap (594 px, 4 px mỗi đơn vị SVG) × k của orig_groups.json:
        # N01–N03 k 7,5 → 10 px; N04 k 18,3 → 23 px; N05 k 17,3 → 22 px; N06 k 12,9 → 16 px.
        "groups": [
            ("N01", "hai sừng", "two horns", "doi", 10,
             "two tan horns: a big one at the left (wide base at its lower right, tip at the top left) and a small one at the right (base at the bottom, tip at the top)",
             "Hai sừng nâu nhạt (1024 × 1024, nền trắng): sừng trái to (gốc rộng ở dưới phải, cong lên tới chóp ở trên trái), sừng phải nhỏ (gốc ở dưới, chóp ở trên); đầu không có trong ảnh",
             """- gốc hai sừng đúng chỗ gốc cũ, rộng như cũ; sừng to bên trái, sừng nhỏ bên phải, chóp chĩa lên hơi nghiêng trái như cũ;
- sừng bạc một màu xám bạc đều, ba bốn ngấn xám sẫm ngang, chóp nhọn; cỡ gần như cũ;
- không vẽ đầu, chỏm len, tai; không sừng nâu.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two tan horns standing on the head (the head is not shown). The viewer-left horn is the big one: its wide BASE is at its lower right, where it sits on the head, and it curves up to a pointed tip at the TOP LEFT. The viewer-right horn is the small one: its base is at the BOTTOM, behind the head, and its tip at the TOP. Redraw THESE two pieces as the horns of image 2 (the approved concept): strong silver horns, one even silver-grey colour with three or four darker grey ring ridges drawn across them, pointed tips; each with its base along the old base, pointing the same way, about the size of the old horn.
Do NOT draw: the head, the wool tuft, the ears, tan or brown horns, light and dark bands on the horns.""", "horn base line"),
            ("N02", "hai vây tai", "two fin ears", "doi", 10,
             "two pink-lined ears sticking out sideways: a big one at the left (base at its right end), a small one at the right (base at its left end)",
             "Hai tai thỏ lòng hồng chìa ngang (1024 × 1024, nền trắng): tai trái to chĩa sang trái (gốc ở đầu phải, có mẩu nhỏ nối vào đầu), tai phải nhỏ chĩa sang phải (gốc ở đầu trái)",
             """- gốc mỗi tai đúng chỗ gốc cũ (tai trái gốc ở bên phải, tai phải gốc ở bên trái); tai trái mở sang trái, tai phải mở sang phải;
- mỗi tai là vây: màng cam san hô căng trên ba gân xanh mòng két tỏa từ gốc, mép ngoài lượn sóng, gân trên cùng xanh mòng két như concept; cỡ gần như tai cũ, to hơn chút được;
- không vẽ đầu, sừng; không tai thỏ hồng.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two ears sticking out sideways from the head (the head is not shown). The viewer-left ear is the big one: its BASE is at its RIGHT end, where it joins the head, and it opens out to the left. The viewer-right ear is the small one: its BASE is at its LEFT end and it opens out to the right. Redraw THESE two pieces as the fin ears of image 2 (the approved concept): each ear a small fin, a coral-orange membrane stretched over three deep-teal ribs that fan out from the base, the top rib a thicker deep-teal edge, the outer edge scalloped; each with its base where the old base is, opening the same way, about the size of the old ear or a little bigger.
Do NOT draw: the head, the horns, pink rabbit ears.""", "joint line at the base of each ear"),
            ("N03", "đầu có mặt", "head with face", "giu", 10,
             "a big fluffy white head with a curled swirl at the upper right, two red eyes, pink cheeks, a small nose and mouth",
             "Đầu lông trắng xù rất to (1024 × 1024, nền trắng): xoáy lông cuộn ở trên phải, hai mắt đỏ (mắt trái to, mắt phải nhỏ sát mép phải), má hồng, mũi và miệng nhỏ; mép dưới gần phẳng",
             """- giữ viền ngoài đầu như cũ (hai bên, mép dưới); chỉ chỏm len kem được nhô lên khỏi mép trên một chút;
- lông ngắn xanh mòng két, mõm và cằm trắng kem, mũi xanh thẫm nhỏ, cười nhếch; chỏm len kem ba lọn nhọn trên trán, không xoáy;
- hai mắt hổ phách to (con ngươi đen, một chấm sáng) đúng chỗ mắt cũ, vệt mày xanh thẫm xếch xuống phía mũi;
- không má hồng; không vẽ sừng, tai, thân.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a big round fluffy white head with a curled swirl of wool at its upper right, two red eyes (the viewer-left eye big, the viewer-right eye smaller near the right edge), pink cheeks, a small nose and mouth; its bottom edge is almost flat. Redraw THESE pieces as the head of image 2 (the approved concept), keeping the outline of the old head: short deep-teal fur; a cream-white muzzle and chin; a small dark navy nose and a confident smirk; a short tuft of cream-white wool in three spiky locks on the forehead, which may rise a little above the old top edge; the two big round amber-gold eyes (a large dark pupil, one small catchlight dot) exactly where the old eyes are, each under a short dark-teal brow mark angled down toward the nose.
The horns and the ears are other groups: draw only the head.
Do NOT draw: the horns, the ears, the body, a swirl or curl, white fluffy fur, pink cheeks, red eyes.""", None),
            ("N04", "thân", "body", "giu", 23,
             "a small round lavender body with a tan patch at the lower left where the tail starts; its top is hidden under the head",
             "Thân tròn nhỏ tím trắng (1024 × 1024, nền trắng): mảng nâu nhạt ở dưới trái là chỗ đuôi cá bắt đầu; mép trên hở vì đầu che",
             """- giữ viền thân như cũ;
- thân xanh mòng két, bụng kem phía trước; dưới trái thon thành khúc đuôi cá xanh mòng két có vài vảy sẫm như concept;
- không vẽ đầu, chân, vây đuôi; không thân tím trắng.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a small round body; the head covers its top (the head is not shown), the two front legs hang in front of it (another group), and at its lower left a tan patch is where the fish tail starts. Redraw THIS piece as the body of image 2 (the approved concept), keeping its outline: deep-teal fur with a cream-white belly patch at the front; at the lower left the body narrows into the start of the deep-teal fish tail with a few darker scale marks, as in image 2.
Draw the whole body under the legs: they are drawn over it later.
Do NOT draw: the head, the legs, the tail fin, a lavender or white body, a tan patch.""", None),
            ("N05", "hai chân trước", "two front legs", "giu", 22,
             "two short pale legs hanging down side by side, cream hooves at the bottom; their tops hidden under the body",
             "Hai chân trước ngắn màu trắng (1024 × 1024, nền trắng): chân trái và chân phải buông thẳng, móng kem ở dưới; mép trên hở là chỗ nối vào thân",
             """- viền và chỗ hai chân như cũ; móng ở đầu dưới;
- chân xanh mòng két, móng xanh thẫm nhỏ;
- không vẽ thân, bụng kem; không móng kem.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two short front legs hanging straight down side by side (the body is not shown): the TOP of each leg is where it joins the body, a small hoof at the BOTTOM. Redraw THESE two pieces as the front legs of image 2 (the approved concept): short deep-teal legs with small dark navy hooves at the bottom, each in its old place, outline and direction.
Do NOT draw: the body, the belly, cream hooves, toes or claws.""", None),
            ("N06", "vây đuôi", "tail fin", "doi", 16,
             "a tan bean-shaped fin with brown lines, hanging down at the lower left; it joins the tail at its upper right end",
             "Vây đuôi nâu nhạt hình hạt đậu có vân nâu (1024 × 1024, nền trắng): rủ xuống ở dưới trái, đầu trên phải là chỗ nối vào khúc đuôi",
             """- đầu nối (trên phải) đúng chỗ cũ, vây rủ xuống như cũ, cỡ như cũ hoặc to hơn chút;
- vây cam san hô hình quạt, gân xanh mòng két tỏa từ chỗ nối, mép lượn, gốc xanh mòng két như concept;
- không vẽ thân, khúc đuôi có vảy; không vây nâu.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a bean-shaped tail fin hanging down at the lower left; its upper right end is where it joins the fish tail (the tail and the body are not shown). Redraw THIS piece as the tail fin of image 2 (the approved concept): a coral-orange fan-shaped fin with deep-teal ribs spreading from a small deep-teal base at the joint, a scalloped outer edge; its joint where the old joint is, hanging down like the old fin, about its size or a little bigger.
Do NOT draw: the body, the scaled part of the tail, a tan fin.""", "upper right joint"),
        ],
        "extra": [],
        "first": ["N03", "N02"],  # gen thử trước: đầu có mặt (giữ viền), vây tai (đổi dáng)
    },
    {
        "code": "ma_ket_2", "elem": "thuy", "aola": 759,
        "hero": "Ma Kết", "form": 2, "forms": 3, "form_name": "Ma Kết Sừng Nhọn",
        "role_vi": "tướng Hiếm hệ Thủy (ải 20 đảo Thủy, mini boss), dạng 2/3, rig aola #759",
        "design_vi": ("dê biển trẻ, lớn lên từ dạng 1: cùng lông xanh mòng két, mõm kem dài hơn, mắt hổ phách, vệt mày xếch; sừng bạc "
                      "dài nhọn có ngấn; vây tai cam san hô to hơn; túm len má và chỏm len trắng kem nhọn (chỏm hất sang phải như ngọn "
                      "sóng); ngực kem đeo vỏ sò điệp hồng san hô trên vòng bạc (mảnh giáp đầu tiên); chân khỏe móng chẻ xanh thẫm; "
                      "đuôi cá xanh mòng két vảy xanh thẫm, vây đuôi to cam san hô"),
        "rig_vi": ("con gốc #759 là dê biển đứng trên hai chân trước, nhìn ba phần tư quay phải: đầu trắng, hai sừng tím hồng nhọn "
                   "(sừng trái to vươn lên trái, sừng phải nhỏ chĩa lên), một tai hồng ở trên trái đầu, túm lông má bên trái, chỏm "
                   "lông nhọn trên phải đầu, mắt xanh ngọc; thân trắng tím nhạt, hai chân trước móng tím (chân trái trước, chân phải "
                   "sau), đuôi cá xanh ngọc sau thân, vây đuôi to hai thùy ở bên trái. Bỏ khỏi bóng xám: bóng"),
        "regions_vi": ("1 sừng trái to, 2 sừng phải nhỏ, 3 tai, 4 đầu có mặt, 5 túm lông má trái, 6 chỏm lông trên phải đầu, 7 thân, "
                       "8 chân trước trái và móng, 9 chân trước phải và móng, 10 đuôi cá, 11 vây đuôi"),
        "anchor": True,
        "prev": [("ma_ket_1", "the approved FIRST stage of this evolution line: keep its colours, horns, fin ears, face and "
                              "drawing style",
                  "dạng 1, dê biển con: lông xanh mòng két, mõm kem, chỏm len kem, sừng bạc ngắn có ngấn, vây tai và vây đuôi cam "
                  "san hô, mắt hổ phách. Giữ màu, sừng, vây tai, mặt, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: the SECOND stage of a three-stage Water evolution line whose first stage is image 6. The little sea-goat kid of image 6 has grown into a bold YOUNG SEA-GOAT: a goat in front with two strong front legs and long pointed silver horns, its body ending in a big fish tail, the first piece of its shell armour hanging on its chest; still a cute, chunky creature. Same front three-quarter view (facing the viewer's right) and pose as image 1, on a plain white background. Not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head with its face, two horns (a big one at the viewer-left, a small one at the right), one ear at the upper left of the head (the other ear is hidden), a cheek ruff at the left side of the head, a spiky tuft at the upper right of the head, one body, two front legs with hooves, one fish tail with one big fin; no hind legs, no second ear, no arms or hands, no wings, no extra limbs;
- every joint where it is: the head sits on the front of the body at the upper right; the big horn grows from the top of the head at its left and the small horn from its upper right, behind the tuft; the ear grows from the upper left of the head, under the big horn; the cheek ruff grows from the left side of the head, behind the face; the tuft sits on the upper right of the head; the front legs start under the front of the body, the viewer-left leg in front and the viewer-right leg behind it at the right; the fish tail starts at the back of the body on the left and ends in the big fin at the left;
- every part pointing the same way: the face is turned to the viewer's right; the big horn rises up and to the left, its tip at the TOP LEFT; the small horn points up; the ear points up and to the left; the ruff's spiky locks point to the left; the tuft's spiky locks point to the right; the viewer-left leg goes straight down and the viewer-right leg goes down and a little to the right, each with its hoof at the BOTTOM; the tail fin has two lobes, the upper one pointing up and the lower one pointing to the left;
- the head, the body, the legs, the tail and the fin about the size and shape of regions 4, 7, 8, 9, 10 and 11; the horns about as long as regions 1 and 2; the whole figure about the same size.

CHANGE (the new look, region by region):
1 and 2 horns: the silver horns of image 6 grown long and pointed: silver with grey ring ridges, the big one curving up and to the left like region 1, the small one like region 2.
3 ear: the coral-orange fin ear of image 6 grown bigger: a coral-orange fin membrane over three deep-teal ribs, pointing up and to the left.
4 head: the deep-teal head of image 6 grown up: a longer cream-white muzzle and chin, a small dark nose, two big amber-gold eyes (a large dark pupil, one small catchlight dot) under dark-teal brow marks angled down: a fierce look; a confident smirk. No blush on the cheeks.
5 cheek ruff: a ruff of cream-white wool in spiky locks pointing to the left, like region 5.
6 tuft: a cream-white wool forelock in spiky locks swept to the right like a breaking wave, like region 6.
7 body: a deep-teal body with a cream-white chest; on the chest hangs a small pale coral-pink scallop shell with cream ribs on a silver ring: the first piece of its shell armour.
8 and 9 front legs: strong deep-teal legs with dark navy split hooves at the bottom.
10 fish tail: a deep-teal fish tail with darker navy scale marks.
11 tail fin: a big coral-orange fin with deep-teal ribs, the shape of region 11.

ATTITUDE: a bold young sea-goat ready to charge horns first: brows angled down, a confident smirk, chest out, legs braced; cute and chunky, never scary, never a cheerful mascot.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those. Image 6 is the approved first stage of this line: keep its colours, horns, fin ears, face and drawing style, so both stages read as the same creature growing up.

COLOURS: as in image 6: deep teal fur; a cream-white muzzle, chest, ruff and tuft; silver horns with grey ridges; amber-gold eyes; coral-orange fins with deep-teal ribs; dark navy hooves and scale marks; a pale coral-pink shell on a silver ring. Few colours.

AVOID: a white or lavender body, mauve, pink or purple horns, teal-green eyes, a pink goat ear, a turquoise tail or fin, hind legs, a human face or body, arms or hands, wings, water rings or bubbles around the creature (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #759, khung đứng đầu (17 mảnh): 1 bóng, 2 chân trước phải, 3 móng phải, 4 sừng phải, 5 vây đuôi, 6 đuôi cá,
        # 7 thân, 8 chân trước trái, 9 đầu, 10 mắt phải, 11 túm lông má trái, 12 chỏm lông trên phải, 13 sừng trái, 14 móng trái,
        # 15 tai, 16 mắt trái, 17 miệng. Nhóm (groups.json): N01 hai sừng (13, 4), N02 vây tai (15), N03 đầu, mặt, túm len má,
        # chỏm len (9, 10, 16, 17, 11, 12), N04 thân (7), N05 hai chân trước (8, 14, 2, 3), N06 đuôi cá và vây (6, 5).
        # Viền px = 0,85% × 695 px (chiều cao cả con trong RegionMap) ÷ 4 × k: N01 10, N02 11, N03 11, N04 21, N05 18, N06 13.
        "groups": [
            ("N01", "hai sừng", "two horns", "doi", 10,
             "two mauve horns: a big one at the left (wide base at its lower right, curving up to a tip at the top left) and a small one at the right (base at the bottom, tip at the top)",
             "Hai sừng tím hồng (1024 × 1024, nền trắng): sừng trái to (gốc rộng ở dưới phải, cong lên tới chóp ở trên trái), sừng phải nhỏ (gốc ở dưới, chóp ở trên); đầu không có trong ảnh",
             """- gốc hai sừng đúng chỗ gốc cũ, rộng như cũ; sừng to vươn lên trái, sừng nhỏ chĩa lên như cũ;
- sừng bạc một màu xám bạc đều, bốn năm ngấn xám sẫm ngang, chóp nhọn như concept; cỡ gần như cũ;
- không vẽ đầu, chỏm len, tai; không sừng tím.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two mauve horns standing on the head (the head is not shown). The viewer-left horn is the big one: its wide BASE is at its lower right, where it sits on the head, and it curves up to a pointed tip at the TOP LEFT. The viewer-right horn is the small one: its base is at the BOTTOM and its tip at the TOP. Redraw THESE two pieces as the long pointed horns of image 2 (the approved concept): silver horns, one even silver-grey colour with four or five darker grey ring ridges drawn across them, sharp tips; each with its base along the old base, pointing the same way, about the size of the old horn.
Do NOT draw: the head, the wool tuft, the ear, mauve or purple horns, light and dark bands on the horns.""", "horn base line"),
            ("N02", "vây tai", "fin ear", "doi", 11,
             "one long goat ear with a pink inside, pointing to the upper left: its tip at the left end, its base at the right end",
             "Một tai dê dài lòng hồng (1024 × 1024, nền trắng): chĩa lên trái, chóp ở đầu trái, gốc (mép hở) ở đầu phải là chỗ nối vào đầu",
             """- gốc tai (đầu phải) đúng chỗ gốc cũ; vây mở lên trái như tai cũ, to hơn tai cũ được như concept;
- màng cam san hô căng trên ba gân xanh mòng két tỏa từ gốc, mép trên là gân xanh mòng két dày, mép ngoài lượn sóng;
- không vẽ đầu, sừng, túm len; không tai dê lòng hồng.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): one long goat ear pointing to the upper left; its tip is at its LEFT end and its BASE is at its RIGHT end, where it joins the head (the head is not shown). Redraw THIS piece as the fin ear of image 2 (the approved concept): a big fin, a coral-orange membrane stretched over three deep-teal ribs that fan out from the base, the top edge a thicker deep-teal rib, the outer edge scalloped; its base where the old base is, opening up and to the left like the old ear, bigger than the old ear as in image 2.
Do NOT draw: the head, the horns, the wool, a goat ear with a pink inside.""", "joint line at the base of the ear (its right end)"),
            ("N03", "đầu, mặt, túm len má, chỏm len", "head with face and wool", "giu", 11,
             "a white head facing right with two teal eyes, a small nose and mouth; a spiky white cheek ruff at its left and a spiky white-and-lavender tuft at its upper right",
             "Đầu trắng quay phải (1024 × 1024, nền trắng): hai mắt xanh ngọc, mũi và miệng nhỏ; túm lông má trắng nhọn ở bên trái, chỏm lông nhọn trắng tím ở trên phải",
             """- giữ viền ngoài đầu như cũ; túm len má ở bên trái và chỏm len ở trên phải đúng chỗ cũ, cỡ như cũ;
- đầu lông xanh mòng két, mõm và cằm trắng kem, mũi xanh thẫm nhỏ, cười nhếch; túm len má kem lọn nhọn chĩa trái; chỏm len kem lọn nhọn hất sang phải;
- hai mắt hổ phách to (con ngươi đen, một chấm sáng) đúng chỗ mắt cũ, vệt mày xanh thẫm xếch;
- không má hồng; không vẽ sừng, tai, thân, vỏ sò.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a white head turned to the viewer's right, with two teal eyes (the viewer-right eye smaller, near the right edge), a small nose and a small mouth; a spiky white cheek ruff sticks out at its LEFT side and a spiky white-and-lavender tuft sits on its UPPER RIGHT. Redraw THESE pieces as the head of image 2 (the approved concept), keeping the outline of the old head, ruff and tuft: short deep-teal fur; a cream-white muzzle and chin; a small dark navy nose and a confident smirk; the two big round amber-gold eyes (a large dark pupil, one small catchlight dot) exactly where the old eyes are, under dark-teal brow marks angled down; the cheek ruff as cream-white wool in spiky locks pointing to the left; the tuft as a cream-white wool forelock in spiky locks swept to the right.
The horns, the ear and the body are other groups: draw only these pieces.
Do NOT draw: the horns, the ear, the body, the shell necklace, a white face, teal eyes, pink cheeks.""", None),
            ("N04", "thân", "body", "giu", 21,
             "a chubby lavender-white body with a white chest patch and a small fur mark; open at the upper right where the head covers it",
             "Thân mập tím trắng (1024 × 1024, nền trắng): mảng ngực trắng, vệt lông nhỏ; mép trên phải hở vì đầu che",
             """- giữ viền thân như cũ;
- thân xanh mòng két, ngực trắng kem mép lông xù ở phía trước bên phải;
- trên ngực, ngay dưới cằm: vỏ sò điệp nhỏ hồng san hô nhạt gân kem treo trên vòng bạc như concept;
- không vẽ đầu, chân, đuôi; không thân tím trắng.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): a chubby body; the head covers its upper right (the head is not shown), the front legs hang from its bottom and the fish tail starts behind its left side (other groups). Redraw THIS piece as the body of image 2 (the approved concept), keeping its outline: deep-teal fur with a cream-white chest at the front right, its edge in soft fur tufts; on the chest, just under where the chin comes, a small pale coral-pink scallop shell with cream ribs hanging on a silver ring, as in image 2.
Draw the whole body under the legs and the head: they are drawn over it later.
Do NOT draw: the head, the legs, the tail, a lavender or white body.""", None),
            ("N05", "hai chân trước", "two front legs", "giu", 18,
             "two front legs: the left one straight down, the right one going down to the right; pale lavender legs with dark mauve split hooves at the bottom",
             "Hai chân trước (1024 × 1024, nền trắng): chân trái thẳng xuống, chân phải chĩa xuống phải; chân tím trắng, móng chẻ tím sẫm ở dưới; mép trên hở là chỗ nối vào thân",
             """- viền và chỗ hai chân như cũ; móng ở đầu dưới;
- chân xanh mòng két, móng chẻ xanh thẫm;
- không vẽ thân, ngực kem; không móng tím.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): two front legs (the body is not shown). The viewer-left leg goes straight down; the viewer-right leg goes down and a little to the right. The TOP of each leg is where it joins the body; a split hoof is at the BOTTOM. Redraw THESE pieces as the front legs of image 2 (the approved concept): strong deep-teal legs with dark navy split hooves at the bottom, each in its old place, outline and direction.
Do NOT draw: the body, the chest, mauve hooves, toes or claws.""", None),
            ("N06", "đuôi cá và vây", "fish tail and fin", "giu", 13,
             "a turquoise fish tail: its thick base at the right (hidden behind the body) and a big two-lobed fin at the left (one lobe pointing up, one pointing left)",
             "Đuôi cá xanh ngọc (1024 × 1024, nền trắng): khúc đuôi dày ở bên phải (giấu sau thân), vây to hai thùy ở bên trái (thùy trên chĩa lên, thùy dưới chĩa trái)",
             """- viền khúc đuôi và vây như cũ; hai thùy chĩa đúng hướng cũ;
- khúc đuôi xanh mòng két vảy cong xanh thẫm; vây cam san hô, gân xanh mòng két dọc mỗi thùy, mép trước xanh mòng két như concept;
- không vẽ thân, chân; không vây xanh ngọc.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a fish tail: its thick base at the RIGHT, where it starts behind the body (the body is not shown), and a big fin with two lobes at the LEFT, one lobe pointing up and one pointing to the left. Redraw THESE pieces as the tail of image 2 (the approved concept), keeping their outline: a deep-teal fish tail with curved darker navy scale marks, and a coral-orange fin with a deep-teal rib along each lobe and a deep-teal leading edge.
Do NOT draw: the body, the legs, a turquoise fin.""", None),
        ],
        "extra": [],
        "first": ["N03", "N02"],  # gen thử trước: đầu có len (giữ viền), vây tai (đổi dáng)
    },
    {
        "code": "ma_ket_3", "elem": "thuy", "aola": 760,
        "hero": "Ma Kết", "form": 3, "forms": 3, "form_name": "Ma Kết Thánh Giáp",
        "role_vi": "tướng Hiếm hệ Thủy (ải 20 đảo Thủy, mini boss), dạng 3/3, rig aola #760",
        "design_vi": ("dê biển thánh giáp, lớn lên từ dạng 2: thân thon xanh mòng két, ngực và mõm kem, bờm len trắng kem hất ra sau "
                      "thành lọn nhọn, mắt hổ phách; sừng bạc dài sắc có ngấn; mũ thánh giáp bằng vỏ sò điệp hồng san hô gân kem viền "
                      "bạc, ngọc trai xanh thẫm trước trán; giáp vai cùng vỏ sò viền bạc, dây da nâu sẫm; vây tai cam san hô; bờm "
                      "sau mũ xanh thẫm; đuôi cá vảy xanh thẫm, ba vây lớn cam san hô căng giữa gai xanh mòng két, ba vây nhỏ xanh "
                      "thẫm; khom thấp sắp vồ, oai, không đáng sợ"),
        "rig_vi": ("con gốc #760 là dê biển giáp vàng nhìn nghiêng quay phải, khom thấp như sắp vồ: đầu thấp ở bên phải mõm chĩa "
                   "phải, bờm trắng hất ra sau, mũ giáp vàng có ngọc xanh lá, sừng xanh xám to vươn ra sau lên trái và sừng nhỏ ở "
                   "bên phải mũ, tai trong nâu, bờm sẫm sau mũ; giáp vai vàng có dây dưới ngực; chân trước gần chạm đất, móng chĩa "
                   "ra sau, chân trước xa gập dưới ngực; đuôi cá xanh tím chạy sang trái với vây gai rất lớn dựng lên (hình chữ L), "
                   "vây giữa, vây dưới dài và ba vây nhỏ sẫm. Bỏ khỏi bóng xám: bóng"),
        "regions_vi": ("1 sừng to, 2 sừng nhỏ, 3 mũ giáp có ngọc, 4 đầu có mặt và bờm hất sau, 5 tai, 6 bờm sẫm sau mũ, 7 thân, "
                       "8 giáp vai và dây, 9 chân trước gần, 10 chân trước xa (gập), 11 đuôi cá, 12 vây gai lớn dựng lên, 13 vây "
                       "giữa, 14 vây dưới dài, 15 ba vây nhỏ"),
        "anchor": True,
        "prev": [("ma_ket_1", "the approved FIRST stage of this evolution line: keep its colours, horns, fin ears, face and "
                              "drawing style",
                  "dạng 1, dê biển con: lông xanh mòng két, mõm kem, chỏm len kem, sừng bạc ngắn có ngấn, vây tai và vây đuôi cam "
                  "san hô, mắt hổ phách. Giữ màu, sừng, vây tai, mặt, nét vẽ"),
                 ("ma_ket_2", "the approved SECOND stage of this evolution line: keep its colours, horns, fin ear, face, wool, "
                              "shell and drawing style",
                  "dạng 2, dê biển trẻ: sừng bạc dài nhọn, vây tai cam san hô, túm len má và chỏm len kem, vỏ sò hồng san hô trên "
                  "ngực, đuôi cá xanh mòng két vây cam san hô. Giữ màu, sừng, vây tai, mặt, len, vỏ sò, nét vẽ")],
        "concept": """Character concept for a 2D cut-out animation game. Draw ONE original creature: the THIRD and final stage of a three-stage Water evolution line whose first two stages are image 6 and image 7. The sea-goat kid of image 6, who grew into the young sea-goat of image 7, has become a HOLY-ARMOURED SEA-GOAT, a knight of the deep: a sleek, powerful sea-goat in shell armour, crouched low and ready to pounce, its fish tail spread into huge spiky fins. Seen from the side facing the viewer's right, in the same pose as image 1, on a plain white background. Noble and strong but still appealing, never scary; not any existing character, and clearly DIFFERENT from the figure the silhouette came from.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head facing right with its face and a mane sweeping back, one helmet on the head with a gem at its front, two horns (a big one sweeping up and back from the helmet, a small one at the right end of the helmet), one ear behind the helmet, a dark back mane showing behind the helmet, one body, one shoulder armour plate with a strap, two front legs (a near one and a far one folded under the chest), one long fish tail going back to the left, one huge tail fin spike, one middle back fin, one long lower fin and three small fins; no hind legs, no arms or hands, no wings, no weapon, no extra limbs;
- every joint where it is: the head is low at the right end of the body, its snout at the far right; the mane grows from the back of the head and sweeps back over the neck; the helmet sits on top of the head, its gem just above the eye; the big horn rises from the top of the helmet; the small horn rises from the right end of the helmet; the ear and the dark back mane stick out from behind the helmet; the shoulder plate lies across the shoulder behind the head, its strap under the chest; the near front leg starts at the shoulder and reaches down to the ground; the far front leg is folded under the chest; the fish tail starts at the back of the body and runs to the left; the huge fin spike, the middle fin and one small fin rise from the top of the tail; the long lower fin and two small fins hang from its underside;
- every part pointing the same way: the head and the snout point right, a little down; the mane's spiky locks sweep back to the upper left; the big horn sweeps up and back to the upper left, its tip at the TOP; the small horn points up; the ear points up and back to the upper left; the near front leg goes down to the ground with its hoof at the BOTTOM, the hoof pointing back to the left; the hoof of the folded far leg points to the left; the huge fin spike rises almost straight up from the tail, with a second long point running back to the left from its base (an L shape like region 12); the middle fin points up and to the left; the long lower fin points to the lower left;
- the head, the body, the legs, the tail and the big fins about the size and shape of regions 4, 7, 9, 10, 11, 12, 13 and 14; the whole figure about the same size.

CHANGE (the new look, region by region):
1 and 2 horns: the silver horns of image 7, now long and sharp: silver with grey ring ridges; the big one sweeping up and back like region 1, the small one like region 2.
3 helmet: a holy helmet made of a pale coral-pink scallop shell with cream ribs and a silver rim, its crest rising like region 3, a deep-blue round pearl set at its front above the eye.
4 head: the deep-teal head of image 7 grown sleek and noble: a long cream-white muzzle, a small dark nose, a fierce amber-gold eye (a large dark pupil, one small catchlight dot) under a dark-teal brow mark angled down, a confident set mouth; a mane of cream-white wool sweeping back from the head in long spiky locks, like region 4.
5 ear: the coral-orange fin ear of image 7, bigger: a coral-orange fin membrane over deep-teal ribs, pointing up and back.
6 back mane: deep navy-teal spiky locks showing behind the helmet.
7 body: a sleek deep-teal body with a cream-white chest.
8 shoulder armour: a curved shoulder plate of the same pale coral-pink shell with cream ribs and a silver rim, held by a dark-brown leather strap.
9 and 10 front legs: strong deep-teal legs with dark navy hooves.
11 fish tail: a long deep-teal fish tail with darker navy scale marks.
12, 13 and 14 big fins: coral-orange fin membranes stretched between deep-teal spines along their edges, each the shape of its region.
15 small fins: three small deep navy-teal fins.

ATTITUDE: a noble armoured sea-goat about to pounce: a focused, fierce eye, the brow angled down, a confident set mouth, the body low and coiled; powerful and proud, with chunky, readable shapes; never scary.

{RENDER}
{DESIGN}
The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some darker shading: do NOT copy those. Image 6 and image 7 are the approved first and second stages of this line: keep their colours, silver horns, fin ears, face, cream wool and coral-pink shell, so all three stages read as the same creature growing up.

COLOURS: as in image 7: deep teal fur; a cream-white muzzle, chest and mane; silver horns with grey ridges; an amber-gold eye; coral-orange fins with deep-teal spines; pale coral-pink shell armour with cream ribs and silver rims; a deep-blue pearl; a deep navy-teal back mane and small fins; dark navy hooves; a dark-brown strap. Few colours.

AVOID: a gold helmet, a green gem, violet or blue-purple fins, a white or lavender body, blue-grey horns, blue eyes, a brown inner ear, hind legs, a human face or body, arms or hands, wings, a weapon, water rings, bubbles or slashes around the creature (the game adds them), text, labels, numbers, the region colours, frames, background scenery, a second view, shading, shadows, white highlights, glossy shine, glow, gradients.""",
        # rig #760, khung đứng đầu (26 mảnh): 1 bóng, 2 3 4 ba vây nhỏ sẫm, 5 móng chân xa, 6 7 chân trước xa (gập), 8 đuôi cá,
        # 9 vây dưới dài, 10 vây gai lớn chữ L, 11 vây giữa, 12 dây giáp, 13 thân, 14 giáp vai, 15 bờm sẫm sau mũ, 16 đầu và bờm,
        # 17 sừng to, 18 tai, 19 sừng nhỏ, 20 má mũ bên phải, 21 mũ giáp, 22 miệng, 23 mắt, 24 móng chân gần, 25 26 chân trước
        # gần. Clip đánh gốc có hình sừng xanh to quét ngang (biến thể): xử lý khi ghép. Nhóm (groups.json): N01 hai sừng (17, 19),
        # N02 mũ (21, 20), N03 đầu và bờm (16, 22, 23), N04 tai và bờm sẫm (15, 18), N05 thân (13), N06 giáp vai và dây (14, 12),
        # N07 chân gần (26, 25, 24), N08 chân xa (6, 7, 5), N09 đuôi cá và ba vây nhỏ (8, 2, 3, 4), N10 ba vây lớn (10, 11, 9).
        # Viền px = 0,85% × 957 px ÷ 4 × k: N01 14, N02 14, N03 13, N04 14, N05 16, N06 16, N07 19, N08 21, N09 11, N10 8.
        "groups": [
            ("N01", "hai sừng", "two horns", "doi", 14,
             "two blue-grey horns: a big one curving up and back to a tip at the top left (base at its lower right), a small one at the right (base at the bottom, tip at the top)",
             "Hai sừng xanh xám (1024 × 1024, nền trắng): sừng to cong lên ra sau, chóp ở trên trái, gốc ở dưới phải; sừng nhỏ ở bên phải, gốc ở dưới, chóp ở trên",
             """- gốc hai sừng đúng chỗ gốc cũ; sừng to vươn lên ra sau, sừng nhỏ chĩa lên như cũ;
- sừng bạc một màu xám bạc đều, ngấn xám sẫm ngang, chóp sắc như concept; cỡ gần như cũ;
- không vẽ mũ, đầu, tai; không sừng xanh xám.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two blue-grey horns that rise from the helmet (the helmet and the head are not shown). The big horn's BASE is at its lower right and it curves up and back to a sharp tip at the TOP LEFT. The small horn stands at the right: its base at the BOTTOM, its tip at the TOP. Redraw THESE two pieces as the horns of image 2 (the approved concept): long, sharp silver horns, one even silver-grey colour with darker grey ring ridges drawn across them; each with its base where the old base is, pointing the same way, about the size of the old horn.
Do NOT draw: the helmet, the head, the ear, blue-grey horns, light and dark bands on the horns.""", "horn base line"),
            ("N02", "mũ thánh giáp", "shell helmet", "doi", 14,
             "a gold helmet crest rising to a point, a green gem at its lower right front, a small gold side piece at its right",
             "Mũ giáp vàng (1024 × 1024, nền trắng): mào vàng nhọn dựng lên, ngọc xanh lá ở phía trước dưới phải, mảnh vàng nhỏ bên phải; mép dưới là chỗ ôm đầu",
             """- mép dưới (chỗ ôm đầu) và chỗ ngọc đúng chỗ cũ; mũ to hơn mũ cũ được như concept;
- vành bạc ôm trán, quạt vỏ sò điệp hồng san hô gân kem dựng lên sau vành, ngọc trai xanh thẫm gắn trên vành ở chỗ ngọc cũ;
- không chấm sáng trên ngọc; không vẽ sừng, đầu, mắt; không mũ vàng, không ngọc xanh lá.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a gold helmet sitting on top of the head (the head is not shown): a crest rising to a point, a green gem at its lower right front, just above the eye, and a small gold side piece at its right end. Redraw THESE pieces as the helmet of image 2 (the approved concept): a silver circlet hugging the forehead along the old lower edge, a fan of pale coral-pink scallop shell with cream ribs rising behind it in place of the crest, and a deep-blue round pearl set in the silver at the front, where the old gem is. It may be bigger than the old helmet, as in image 2.
Do NOT draw: the horns, the head, the eye, a gold helmet, a green gem, a white shine spot on the pearl.""", "lower edge on the head and the gem's place"),
            ("N03", "đầu và bờm", "head with face and mane", "giu", 13,
             "a white head facing right: a blue eye, a mouth line, the snout at the right; long lavender-white mane spikes sweeping back to the upper left",
             "Đầu trắng quay phải (1024 × 1024, nền trắng): mắt xanh, nét miệng, mõm ở bên phải; bờm trắng tím nhạt thành gai dài hất ra sau lên trái",
             """- giữ viền đầu và các gai bờm như cũ; mắt, miệng đúng chỗ cũ;
- đầu xanh mòng két, mõm và hàm dưới trắng kem, mũi xanh thẫm nhỏ, cười tự tin; mắt hổ phách (con ngươi đen, một chấm sáng) dưới vệt mày xanh thẫm xếch;
- các gai bờm hất ra sau là len trắng kem;
- không vẽ mũ, sừng, tai.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a white head seen from the side, facing right (the snout at the RIGHT end), with a blue eye and a mouth line; long lavender-white mane spikes sweep back from it to the upper left. Redraw THESE pieces as the head of image 2 (the approved concept), keeping the outline of the head and of every mane spike: a deep-teal head; a cream-white muzzle and lower jaw; a small dark navy nose and a confident smile; a fierce amber-gold eye (a large dark pupil, one small catchlight dot) exactly where the old eye is, under a dark-teal brow mark angled down; the mane spikes as cream-white wool locks sweeping back.
The helmet, the horns and the ear are drawn over this group later: draw the whole head under them.
Do NOT draw: the helmet, the horns, the ear, a white head, a blue eye.""", None),
            ("N04", "vây tai và bờm sẫm", "fin ear and back mane", "doi", 14,
             "a long ear with a brown inside pointing up and to the left, and behind it a grey back mane with two points (one up-left, one up)",
             "Tai dài lòng nâu chĩa lên trái và bờm xám sau nó có hai mũi (một chĩa lên trái, một chĩa lên) (1024 × 1024, nền trắng); mép dưới là chỗ giấu sau mũ",
             """- tai chĩa lên ra sau (lên trái) như tai cũ, gốc đúng chỗ cũ; không nằm ngang ra sau;
- tai là vây: màng cam san hô căng trên gân xanh mòng két, mép trên là gân xanh mòng két dày;
- bờm sẫm xanh thẫm, lọn nhọn đúng chỗ hai mũi cũ;
- không vẽ mũ, đầu, sừng; không tai lòng nâu, không bờm xám.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design), both sticking out from behind the helmet (the helmet and the head are not shown): in front, a long ear with a brown inside, pointing UP and back to the upper left, its base at its lower right; behind it, a grey back mane with two points, one pointing up and to the left, one pointing up at the right. Redraw THESE pieces as image 2 (the approved concept) shows them: the ear as a fin, a coral-orange membrane over deep-teal ribs with a thicker deep-teal top edge, pointing up and back like the old ear (not lying flat); the back mane as deep navy-teal spiky locks, their tips where the old points are.
Do NOT draw: the helmet, the head, the horns, a brown-lined ear, a grey mane.""", "base, hidden behind the helmet at the lower right,"),
            ("N05", "thân", "body", "giu", 16,
             "a grey-lavender body seen from the side: a pointed back edge at the upper left, the chest at the lower right",
             "Thân xám tím nhìn nghiêng (1024 × 1024, nền trắng): mép lưng có mũi nhọn ở trên trái, ngực ở dưới phải; đầu, chân, đuôi không có trong ảnh",
             """- giữ viền thân như cũ;
- thân xanh mòng két, ngực trắng kem ở phía trước dưới phải như concept;
- không vẽ đầu, giáp vai, chân, đuôi; không thân xám tím.""",
             """Image 1 is one piece of a 2D cut-out animation puppet (the old design): the body seen from the side; the head joins it at the right, the tail at the left, the legs under it (other groups). Redraw THIS piece as the body of image 2 (the approved concept), keeping its outline: sleek deep-teal fur with a cream-white chest at its lower right front.
Draw the whole body under the other parts: they are drawn over it later.
Do NOT draw: the head, the mane, the shoulder armour, the legs, the tail, a grey or lavender body.""", None),
            ("N06", "giáp vai và dây", "shoulder armour and strap", "doi", 16,
             "a gold crescent plate running from the upper left down to the lower right, and a brown strap curling up to the right at its lower end",
             "Giáp vai vàng hình lưỡi liềm (1024 × 1024, nền trắng): chạy từ trên trái xuống dưới phải; dây nâu cong lên bên phải ở đầu dưới",
             """- giáp nằm đúng chỗ, đúng hướng giáp cũ (trên trái xuống dưới phải), to hơn được như concept; dây đúng chỗ dây cũ;
- giáp vỏ sò điệp hồng san hô gân kem, viền bạc; dây da nâu sẫm có khoen bạc nhỏ;
- không vẽ thân, chân, bờm; không giáp vàng.""",
             """Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a gold crescent shoulder plate lying across the shoulder, running from the upper left down to the lower right, and a brown strap that curls up to the right from its lower end, under the chest (the body is not shown). Redraw THESE pieces as image 2 (the approved concept) shows them: the plate as a curved shoulder guard of pale coral-pink scallop shell with cream ribs and a silver rim, in the place and direction of the old plate, it may be wider as in image 2; the strap as a dark-brown leather strap with a small silver ring, along the old strap.
Do NOT draw: the body, the legs, the mane, a gold plate.""", "plate line and strap end"),
            ("N07", "chân trước gần", "near front leg", "giu", 19,
             "a white-lavender front leg: fluffy points at its top (the shoulder), bent lower down, a blue-grey hoof at the bottom left pointing left",
             "Chân trước gần trắng tím (1024 × 1024, nền trắng): đầu trên có mấy mũi lông xù là vai, gập ở dưới, móng xanh xám ở dưới trái chĩa sang trái",
             """- viền và chỗ chân như cũ; vai ở đầu trên, móng ở đầu dưới chĩa trái;
- chân xanh mòng két, mấy mũi lông ở vai trắng kem, móng xanh thẫm;
- không vẽ thân, giáp vai; không móng xanh xám.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the near front leg (the body is not shown). Its TOP end, with a few fluffy points, is the shoulder; the leg comes down and bends, and its hoof is at the BOTTOM LEFT, pointing to the left. Redraw THESE pieces as the near front leg of image 2 (the approved concept), keeping the outline: a deep-teal leg, the fluffy points at the shoulder in cream-white wool, a dark navy hoof at the bottom pointing left.
Do NOT put the hoof at the shoulder end. Do NOT draw: the body, the shoulder armour, a blue-grey hoof.""", None),
            ("N08", "chân trước xa", "far front leg", "giu", 21,
             "a grey-lavender front leg folded under the chest: fluffy points at its top, a blue-grey hoof at the bottom left pointing left",
             "Chân trước xa xám tím gập dưới ngực (1024 × 1024, nền trắng): đầu trên có mũi lông xù là vai, móng xanh xám ở dưới trái chĩa sang trái",
             """- viền và chỗ chân như cũ; móng ở đầu dưới chĩa trái;
- chân xanh mòng két (cùng màu chân gần, không tô sẫm hơn), mũi lông ở vai trắng kem, móng xanh thẫm;
- không vẽ thân, chân gần.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): the far front leg, folded under the chest (the body is not shown). Its TOP end, with fluffy points, is the shoulder; its hoof is at the BOTTOM LEFT, pointing to the left. Redraw THESE pieces as the far front leg of image 2 (the approved concept), keeping the outline: a deep-teal leg in the same colour as the near leg (not darker), the fluffy points in cream-white wool, a dark navy hoof pointing left.
Do NOT put the hoof at the shoulder end. Do NOT draw: the body, the near leg, a grey leg, a blue-grey hoof.""", None),
            ("N09", "đuôi cá và ba vây nhỏ", "fish tail and small fins", "giu", 11,
             "a navy-blue rounded tail piece with three small dark fins: one on top at the left, one at the left end, one underneath",
             "Khúc đuôi xanh tím tròn (1024 × 1024, nền trắng) với ba vây nhỏ sẫm: một vây trên ở bên trái, một vây ở đầu trái, một vây dưới",
             """- viền khúc đuôi và ba vây nhỏ như cũ;
- khúc đuôi xanh mòng két, vảy cong xanh thẫm; ba vây nhỏ xanh thẫm;
- không vẽ vây lớn, thân; không xanh tím.""",
             """Image 1 is several pieces of a 2D cut-out animation puppet (the old design): a rounded navy-blue tail piece (its wide end at the right joins the body, which is not shown) with three small dark fins: one on its top at the left, one at its left end and one underneath. Redraw THESE pieces as image 2 (the approved concept) shows them, keeping every outline: the tail in deep-teal fur turning into curved darker navy scale marks; the three small fins deep navy-teal.
Do NOT draw: the big fins, the body, violet or blue-purple colours.""", None),
            ("N10", "ba vây lớn", "three big fins", "giu", 8,
             "three blue-violet fins: a huge L-shaped spike (one point up, one point to the left), a smaller fin pointing up at the right, a long fin pointing to the lower left at the bottom",
             "Ba vây xanh tím (1024 × 1024, nền trắng): vây gai rất lớn hình chữ L (một mũi chĩa lên, một mũi chĩa trái), vây nhỏ hơn chĩa lên ở bên phải, vây dài chĩa xuống trái ở dưới",
             """- viền ba vây như cũ, đúng hướng cũ;
- màng vây cam san hô, gân và mép trước xanh mòng két như concept;
- không vẽ đuôi, thân; không vây xanh tím.""",
             """Image 1 is three pieces of a 2D cut-out animation puppet (the old design): three blue-violet fins that grow from the tail (the tail is not shown): a huge L-shaped fin spike (one long point straight up, one long point to the left, its base at the lower right), a smaller fin at the right pointing up and to the left, and a long fin at the bottom pointing to the lower left. Redraw THESE pieces as the fins of image 2 (the approved concept), keeping their outlines: coral-orange fin membranes with deep-teal spines along their edges and a deep-teal rib inside.
Do NOT draw: the tail, the body, blue or violet fins.""", None),
        ],
        "extra": [],
        "first": ["N03", "N02"],  # gen thử trước: đầu và bờm (giữ viền), mũ vỏ sò (đổi dáng)
    },
]


def rig_dir(f):
    return ROOT + f"refs/{f['elem']}/{f['code']}/"


def concept_path(code):
    return ROOT + f"inbox/{code}/concept_duyet.png"


def size_of(path):
    with Image.open(path) as im:
        return im.size


def refs_block(refs):
    """danh sách ảnh mẫu đầu file prompt: image N = đường dẫn đầy đủ: là gì"""
    return (["REFERENCE IMAGES (open each file from its full path):"]
            + [f"image {i} = {W(src)}: {en}" for i, (src, en, _) in enumerate(refs, 1)])


def save_rule(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    return (f"save it as a PNG to {W(path)} (create the folder if it is missing; if that file already exists, save it as "
            f"{stem}_2.png, {stem}_3.png … in the same folder instead). Do not change, move or delete any other file.")


def build(f):
    code = f["code"]
    pk = ROOT + f"gui_gpt/{code}/"
    os.makedirs(pk, exist_ok=True)
    save = ROOT + f"inbox/{code}/tai_ve/"
    os.makedirs(save, exist_ok=True)
    rd = rig_dir(f)
    head = ("Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save "
            "it as described under SAVE. Do not reply with text only.")

    # ----- lượt 1: concept -----
    p1 = pk + "luot_1_concept.txt"
    sw, sh = size_of(rd + "Silhouette.png")
    a1 = [(rd + "Silhouette.png", "grey silhouette of the puppet rig",
           f"Bóng xám của con gốc trên nền trắng ({sw} × {sh}): " + f["rig_vi"]),
          (rd + "RegionMap.png", "the same figure split into numbered regions",
           f"Cùng hình, tô màu từng vùng và đánh số ({sw} × {sh}, nền trắng): " + f["regions_vi"]),
          (STYLE_SHEET, "eight creatures of the game: a DESIGN reference only (do not copy their glossy rendering or their designs)",
           "Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào"),
          (WORLD_STYLE, "the game's approved hand-drawn map: copy its RENDERING (ink outlines, coloured-pencil hatching), ignore its content",
           "Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung")]
    # ảnh mốc style (QUY_TRINH mục 1): concept Giọt Sương dạng 1 đã chốt, chỉ lấy nét và độ chi tiết
    if f.get("anchor"):
        a1.append((STYLE_ANCHOR, "an approved character of this game: copy its ink line and its pencil and crayon texture only, "
                                 "not its design, not its white shine spots or darker shading",
                   "Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm "
                   "kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó"))
    # dạng sau của một dòng: đính concept đã duyệt của dạng trước (giữ màu, mũ, mặt, nét)
    for pc, en, vi in f.get("prev", []):
        src = concept_path(pc)
        size = "{} × {}, ".format(*size_of(src)) if os.path.exists(src) else ""
        a1.append((src, en, f"Concept đã duyệt của `{pc}` ({size}nền trắng): {vi}"))
    have_prev = all(os.path.exists(src) for src, _, _ in a1)
    s1 = save + "concept.png"
    if have_prev:
        t1 = [head, ""] + refs_block(a1) + ["", "SAVE: when the image is done, " + save_rule(s1), "",
                                            f["concept"].replace("{RENDER}", f.get("render", RENDER))
                                            .replace("{DESIGN}", f.get("design", DESIGN)), "",
                                            f"Remember: save the image to {W(s1)}"]
        open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t1) + "\n")

    # ----- lượt 2: nhóm mảnh (chỉ dựng khi đã có concept duyệt) -----
    line = LINE
    p2 = pk + "luot_2_nhom_manh.txt"
    gs = f["groups"]
    a2 = [(rd + f"orig/{g[0]}.png", f"old pieces of group {g[0]}: {g[5]}", g[6]) for g in gs]
    ci = len(a2) + 1
    a2.append((concept_path(code), "the approved concept of this creature", "concept đã duyệt của dạng này (nền trắng)"))
    have_c = os.path.exists(concept_path(code))
    order = f["first"] + [g[0] for g in gs if g[0] not in f["first"]] + [e[0] for e in f["extra"]]
    have_g = len(order) >= 2  # prompt nhóm viết sau khi duyệt concept
    if have_c and have_g:
        t2 = [head.replace("draw ONE image and save it as described under SAVE",
                           "draw ONE image per reply and save each one as its step says")]
        t2 += [""] + refs_block(a2)
        t2 += ["", "WHAT THIS IS: a creature for a 2D cut-out animation game. Its animation already exists: it moves flat "
               "picture pieces around fixed joints. Each step below redraws ONE group of old puppet pieces as the matching "
               "part of the approved concept, on the same square canvas, so the old animation can play the new drawings. "
               "Inside a step, \"image 1\" means that step's old-pieces image and \"image 2\" means the approved concept "
               f"(reference image {ci}).",
               "Every reply: exactly ONE image for ONE step, a square 1024 x 1024 canvas, plain white background, no text; "
               "save it where that step says.", "",
               f"SAVE: every step's image goes into {W(save)} under the step's name (for example {order[0]}.png). If that file "
               f"already exists, add _2, _3 … before .png. Do not change, move or delete any other file.", "",
               f"ORDER: draw step {order[0]} now, save it and stop. When I say \"next\", draw step {order[1]}, save it and stop: "
               f"I will check both. When I say \"continue\", draw the remaining steps one per reply, each after I say \"next\", "
               f"in this order: {', '.join(order[2:])}.", ""]
        for i, g in enumerate(gs, 1):
            code_g, _, en, kind, n, _, _, _, prompt, joint = g
            frame = KEEP_FRAME if kind == "giu" else free_frame(joint)
            t2 += [f"=== STEP {code_g} ({en}) ===",
                   f"In this step: image 1 = reference image {i} ({W(a2[i - 1][0])}); image 2 = reference image {ci}.",
                   prompt, "", frame, line.format(n=n), f"SAVE this step: {save_rule(save + code_g + '.png')}", ""]
        for code_e, _, en, n, _, prompt in f["extra"]:
            t2 += [f"=== STEP {code_e} ({en}) ===",
                   f"In this step: image 2 = reference image {ci}; there is no image 1.",
                   prompt, "", line.format(n=n).replace("not image 1's glossy vector look", "as in the concept"),
                   f"SAVE this step: {save_rule(save + code_e + '.png')}", ""]
        open(p2, "w", encoding="utf-8", newline="\n").write("\n".join(t2) + "\n")

    # ----- lượt 3: vẽ lại nhóm bị lỗi sau khi ghép (khoá "redo"), lưu <mã>_ve_lai.png; bộ ghép lấy ảnh mới nhất của nhóm -----
    p3 = pk + "luot_3_ve_lai.txt"
    rs = f.get("redo", [])
    a3 = [(rd + f"orig/{r['code']}.png", f"old piece of group {r['code']}: {r['old_en']}", r["old_vi"]) for r in rs]
    c3 = len(a3) + 1
    a3.append((concept_path(code), "the approved concept of this creature", "concept đã duyệt của dạng này (nền trắng)"))
    if have_c and rs:
        t3 = [head.replace("draw ONE image and save it as described under SAVE",
                           "draw ONE image per reply and save each one as its step says")]
        t3 += [""] + refs_block(a3)
        t3 += ["", "WHAT THIS IS: a creature for a 2D cut-out animation game. Its animation already exists: it moves flat "
               "picture pieces around fixed joints. Each step below redraws ONE old puppet piece as the matching part of the "
               "approved concept, on the same square canvas, so the old animation can play the new drawing. Inside a step, "
               f"\"image 1\" means that step's old-piece image and \"image 2\" means the approved concept (reference image {c3}).",
               "Every reply: exactly ONE image for ONE step, a square 1024 x 1024 canvas, plain white background, no text.", "",
               f"ORDER: draw step {rs[0]['code']} now, save it and stop."
               + (f" When I say \"next\", draw the next step: {', '.join(r['code'] for r in rs[1:])}." if len(rs) > 1 else ""), ""]
        for i, r in enumerate(rs, 1):
            t3 += [f"=== STEP {r['code']} ({r['en']}) ===",
                   f"In this step: image 1 = reference image {i} ({W(a3[i - 1][0])}); image 2 = reference image {c3}.",
                   r["prompt"], "", r["frame"], line.format(n=r["n"]),
                   f"SAVE this step: {save_rule(save + r['code'] + '_ve_lai.png')}", ""]
        open(p3, "w", encoding="utf-8", newline="\n").write("\n".join(t3) + "\n")

    # ----- HUONG_DAN.md -----
    g_ = [f"# Gói gửi GPT: {f['hero']} dạng {f['form']}/{f['forms']} ({f['form_name']}, `{code}`)", "",
          f"{f['role_vi'][:1].upper() + f['role_vi'][1:]}. Thiết kế: {f['design_vi']}. Quy trình: `{W(ROOT + 'QUY_TRINH.md')}`.", "",
          "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT "
          f"tự lưu ảnh (`{W(save)}`). Claude xem rồi đặt tên và chép vào đúng chỗ.", "",
          "Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.", "",
          "## Lượt 1: concept", ""]
    if have_prev:
        g_ += [f"File prompt: `{W(p1)}`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `{W(s1)}`.", ""]
    else:
        g_ += [f"File prompt `{W(p1)}`: **chưa có**, cần concept đã duyệt của dạng trước "
               f"({', '.join(W(concept_path(pc)) for pc, _, _ in f.get('prev', []))}).", ""]
    g_ += ["| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    g_ += [f"| {i} | `{W(src)}` | {vi} |" for i, (src, _, vi) in enumerate(a1, 1)]
    g_ += ["", f"Xong thì nhắn Claude \"duyệt concept {code}\". Duyệt xong Claude lưu `{W(concept_path(code))}` và chạy lại "
               f"`build.py` để có file prompt lượt 2.", "",
           "## Lượt 2: nhóm mảnh", ""]
    if not (have_c and have_g):
        orig_note = (f"Ảnh gốc từng nhóm (GPT vẽ đè lên) đã có ở `{W(rd + 'orig')}`." if os.path.isdir(rd + "orig")
                     else "Ảnh gốc từng nhóm (GPT vẽ đè lên) Claude dựng cùng lúc.")
        g_ += [f"File prompt `{W(p2)}`: **chưa có**. Claude viết prompt từng nhóm và dựng file này khi đã duyệt concept "
               f"(cần `{W(concept_path(code))}`). {orig_note}", ""]
        if have_prev:  # bảng câu sửa nhanh cho lượt concept
            g_ += ["## Concept sai thì gửi thêm (cùng chat)", "",
                   "| Sai | Gửi thêm |", "|---|---|",
                   "| Không giống vẽ tay trên giấy, không thấy nét chì sáp | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |",
                   f"| Có mảng sáng tối, điểm sáng trắng, bóng loáng, chuyển sắc | `{FLAT_FIX}` |",
                   f"| Có bóng đổ, bóng dưới chân, bóng in xuống nền | `{FLAT_FIX}` |",
                   "| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |",
                   "| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |",
                   "| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile; not a big happy grin.` |",
                   "| Vẽ thêm chân, đuôi, cánh không có trong rig | `Only the parts listed under KEEP FROM THE RIG: no extra legs, tails or wings.` |",
                   "| Sai dáng rig (tay, đinh ba, vây lệch chỗ) | `Keep the pose and the parts of image 1 exactly: every part where image 2 puts it, pointing the same way.` |",
                   "| Có cảnh nền, chữ, khung | `Plain pure white background: no scenery, no text, no frame.` |", ""]
        g_ += [f"Gói này sinh từ `{W(ROOT + 'build.py')}`; sửa prompt ở đó rồi chạy lại.", ""]
        open(pk + "HUONG_DAN.md", "w", encoding="utf-8", newline="").write("\n".join(g_))
        return [W(p) for p in (p1, p2) if os.path.exists(p)]
    g_ += [f"File prompt: `{W(p2)}`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `{W(save)}<mã nhóm>.png`.", "",
           f"1. GPT vẽ {order[0]}. Gõ `next`: GPT vẽ {order[1]}. Nhắn Claude \"soi thử {code}\".",
           f"2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: {', '.join(order[2:])}.",
           f"3. Đủ ảnh thì nhắn Claude \"ghép {code}\".", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    g_ += [f"| {i} | `{W(src)}` | {vi}{'' if os.path.exists(src) else ': **chưa có**, sinh ở lượt 1'} |"
           for i, (src, _, vi) in enumerate(a2, 1)]
    g_ += ["", "Kiểm từng ảnh trước khi lưu:", ""]
    for g in gs:
        g_ += [f"**{g[0]} {g[1]}** ({'giữ viền' if g[3] == 'giu' else 'đổi dáng'}, viền khoảng {g[4]} px):", g[7], ""]
    for e in f["extra"]:
        g_ += [f"**{e[0]} {e[1]}** (vẽ riêng, Claude gắn vào bàn tay khi ghép; viền khoảng {e[3]} px):", e[4], ""]
    if rs:
        g_ += ["## Lượt 3: vẽ lại nhóm bị lỗi sau khi ghép", "",
               f"File prompt: `{W(p3)}`. Gửi trong **chat mới**. GPT vẽ lại {', '.join(r['code'] for r in rs)}, lưu thành "
               f"`{W(save)}<mã nhóm>_ve_lai.png` (ảnh cũ giữ nguyên; khi ghép Claude dùng ảnh mới nhất của nhóm).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        g_ += [f"| {i} | `{W(src)}` | {vi} |" for i, (src, _, vi) in enumerate(a3, 1)]
        g_ += [""]
        for r in rs:
            g_ += [f"**{r['code']} {r['vi']}** (vẽ lại vì {r['why_vi']}; viền khoảng {r['n']} px):", r["check_vi"], ""]
        g_ += [f"Xong thì nhắn Claude \"ghép lại {code}\".", ""]
    g_ += ["## GPT vẽ sai thì gửi thêm (cùng chat)", "",
           "| Sai | Gửi thêm |", "|---|---|",
           "| Không giống vẽ tay trên giấy, không thấy nét chì sáp | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |",
           f"| Có mảng sáng tối, điểm sáng trắng, bóng loáng, chuyển sắc | `{FLAT_FIX}` |",
           "| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |",
           "| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |",
           "| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile; not a big happy grin.` |",
           "| Vẽ cả con hoặc thêm phần ngoài nhóm | `Only the pieces of image 1, nothing else.` |",
           "| Mảnh lệch chỗ, xoay, đổi cỡ | `Put every piece back exactly where it is in image 1: same position, size and angle on the same 1024 x 1024 canvas.` |",
           "| Bàn tay, bàn chân ở sai đầu | `The hand/foot is at the BOTTOM end; the TOP end is the shoulder/hip.` |",
           "| Viền mảnh quá mảnh hoặc quá dày | `Make the dark-brown outline about <N> px thick, the same on every edge.` (N ghi ở từng nhóm trên) |",
           f"| Có bóng đổ, bóng dưới chân, bóng in xuống nền | `{FLAT_FIX}` |",
           "| Nền xám, có ô lưới | `Plain pure white background, nothing else.` |", "",
           f"Gói này sinh từ `{W(ROOT + 'build.py')}`; sửa prompt ở đó rồi chạy lại.", ""]
    open(pk + "HUONG_DAN.md", "w", encoding="utf-8", newline="").write("\n".join(g_))
    return [W(p) for p in (p1, p2, p3) if os.path.exists(p)]


if __name__ == "__main__":
    # py -3 -I build.py [mã ...]: chỉ dựng các dạng có mã đó (để không ghi lại gói của dạng khác)
    only = set(sys.argv[1:])
    for f in FORMS:
        if not only or f["code"] in only:
            print(*build(f))
