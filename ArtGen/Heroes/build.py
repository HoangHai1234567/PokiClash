# Sinh gói gửi GPT cho hình tướng: ArtGen/Heroes/gui_gpt/<mã>/ (quy trình: QUY_TRINH.md).
# Cách làm: vẽ con mới đè lên rig vector của aola (người dùng: "vẫn phải dùng rig cũ", 2026-11-02) để giữ animation aola.
# Mỗi dạng 2 lượt, mỗi lượt một file prompt (tiếng Anh): người dùng chỉ gửi GPT đường dẫn file đó (người dùng dặn 2026-11-03).
# File mở đầu bằng danh sách ảnh mẫu kèm đường dẫn đầy đủ (GPT tự mở), rồi chỗ GPT tự lưu ảnh (inbox/<mã>/tai_ve/). Kèm HUONG_DAN.md
# (tiếng Việt: file prompt từng lượt, ảnh mẫu trông ra sao, lưu đâu, kiểm gì, câu sửa nhanh).
#   luot_1_concept.txt:   concept cả con trên rig (bóng xám, bản đồ vùng) + tờ mẫu thiết kế (aola) + ảnh mốc nét vẽ (bản đồ).
#   luot_2_nhom_manh.txt: từng nhóm mảnh vẽ đè lên hình gốc của nhóm (refs/<hệ>/<mã>/orig/Nxx.png) + concept đã duyệt; một ảnh
#                         mỗi bước. Chỉ dựng khi đã có concept duyệt (inbox/<mã>/concept_duyet.png).
# Nét: vẽ tay như bản đồ world_style.png; thiết kế học từ tướng aola. Viền trắng giấy xé do game vẽ (shader), GPT không vẽ.
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
# UI và tướng không vẽ bóng (người dùng 2026-11-03, câu dán của ArtGen/README.md mục "Luật chung")
NO_SHADOWS = ("NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or "
              "background. Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed.")
RENDER = ("RENDERING (copy it from the game's hand-drawn map): drawn by hand by a professional illustrator for a storybook "
          "game: bold dark-brown ink outlines (#2B2118) of fairly even weight, slightly wobbly like a real pen; flat warm "
          "colours shaded with loose diagonal coloured-pencil hatching; a few small white highlights; clean and appealing, "
          "neither a crude kid scribble nor overly detailed. No glossy digital shine, no smooth airbrushed gradients, no 3D "
          "render. No white border or sticker outline around the creature or its parts: the game adds that itself.\n"
          + NO_SHADOWS)
DESIGN = ("DESIGN (learn it from the game's creatures in the style sheet): an appealing original creature in the classic "
          "Japanese monster-collecting look: a clear, chunky silhouette that reads at small size, big expressive eyes, simple "
          "readable shapes, few details. Take only the design approach from those creatures, never their glossy rendering "
          "and never their designs.")
LINE = ("LINE AND COLOUR: the hand-drawn rendering of image 2, not image 1's glossy vector look: a dark-brown ink outline "
        "(#2B2118) about {n} px thick on this 1024 canvas, the same weight on every edge, slightly wobbly like a real pen; flat "
        "warm colours shaded with loose diagonal coloured-pencil hatching (strokes thinner than the outline), kept inside the "
        "outline; a few small white highlights; no gradients, no glossy shine, no paper texture, no white border around the "
        "pieces.\n" + NO_SHADOWS + "\nPlain white background. Only this group. No text.")
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
    # dạng sau của một dòng: đính concept đã duyệt của dạng trước (giữ màu, mũ, mặt, nét)
    for pc, en, vi in f.get("prev", []):
        src = concept_path(pc)
        size = "{} × {}, ".format(*size_of(src)) if os.path.exists(src) else ""
        a1.append((src, en, f"Concept đã duyệt của `{pc}` ({size}nền trắng): {vi}"))
    have_prev = all(os.path.exists(src) for src, _, _ in a1)
    s1 = save + "concept.png"
    if have_prev:
        t1 = [head, ""] + refs_block(a1) + ["", "SAVE: when the image is done, " + save_rule(s1), "",
                                            f["concept"].replace("{RENDER}", RENDER).replace("{DESIGN}", DESIGN), "",
                                            f"Remember: save the image to {W(s1)}"]
        open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t1) + "\n")

    # ----- lượt 2: nhóm mảnh (chỉ dựng khi đã có concept duyệt) -----
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
                   prompt, "", frame, LINE.format(n=n), f"SAVE this step: {save_rule(save + code_g + '.png')}", ""]
        for code_e, _, en, n, _, prompt in f["extra"]:
            t2 += [f"=== STEP {code_e} ({en}) ===",
                   f"In this step: image 2 = reference image {ci}; there is no image 1.",
                   prompt, "", LINE.format(n=n).replace("not image 1's glossy vector look", "as in the concept"),
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
                   r["prompt"], "", r["frame"], LINE.format(n=r["n"]),
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
               f"(cần `{W(concept_path(code))}`). Ảnh gốc từng nhóm (GPT vẽ đè lên) đã có ở `{W(rd + 'orig')}`.", "",
               f"Gói này sinh từ `{W(ROOT + 'build.py')}`; sửa prompt ở đó rồi chạy lại.", ""]
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
           "| Nét số bóng loáng, chuyển sắc | `Render it hand-drawn like the map: dark-brown ink outlines, flat warm colours with coloured-pencil hatching; no glossy shine, no gradients.` |",
           "| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |",
           "| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |",
           "| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile with a tiny fang; not a big happy grin.` |",
           "| Vẽ cả con hoặc thêm phần ngoài nhóm | `Only the pieces of image 1, nothing else.` |",
           "| Mảnh lệch chỗ, xoay, đổi cỡ | `Put every piece back exactly where it is in image 1: same position, size and angle on the same 1024 x 1024 canvas.` |",
           "| Bàn tay, bàn chân ở sai đầu | `The hand/foot is at the BOTTOM end; the TOP end is the shoulder/hip.` |",
           "| Viền mảnh quá mảnh hoặc quá dày | `Make the dark-brown outline about <N> px thick, the same on every edge.` (N ghi ở từng nhóm trên) |",
           f"| Có bóng đổ, bóng dưới chân, bóng in xuống nền | `{NO_SHADOWS}` |",
           "| Nền xám, có ô lưới | `Plain pure white background, nothing else.` |", "",
           f"Gói này sinh từ `{W(ROOT + 'build.py')}`; sửa prompt ở đó rồi chạy lại.", ""]
    open(pk + "HUONG_DAN.md", "w", encoding="utf-8", newline="").write("\n".join(g_))
    return [W(p) for p in (p1, p2, p3) if os.path.exists(p)]


if __name__ == "__main__":
    for f in FORMS:
        print(*build(f))
