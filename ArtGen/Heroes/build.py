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
        g_ += [f"File prompt `{W(p2)}`: **chưa có**. Claude viết prompt từng nhóm và dựng file này khi đã duyệt concept "
               f"(cần `{W(concept_path(code))}`). Ảnh gốc từng nhóm (GPT vẽ đè lên) đã có ở `{W(rd + 'orig')}`.", ""]
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
