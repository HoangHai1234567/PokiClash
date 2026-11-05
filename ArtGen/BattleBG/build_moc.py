# Sàn đấu đảo Mộc 70 ải: dựng bố cục và gói gửi GPT (ArtGen/BattleBG/PROMPTS.md, mục "Đảo Mộc 70 ải").
# Tiết kiệm dung lượng (người dùng 2026-11-05): 8 nền thay cho 17 nền của đảo Thủy, game dùng lại nền:
# - 2 nền thường, mỗi nền cho hai chặng đầu liền nhau (Bờ Rêu + Đồng Hoa Sáng: ải 1–9; Đồi Nấm + Rừng Dây Leo: ải 10–19);
# - 5 nền chặng có mini boss (Hang Nanh Gió … Hang Pha Lê Lục): mini boss ải 20–60 và các ải thường sau nó cùng một nền; ải mini
#   boss thêm phần động mạnh hơn và phủ màu tối nhẹ (game);
# - 1 nền boss ải 70 (Cây Thần Ngàn Năm); dạng 2, 3 của Thanh Long là nền đó phủ màu tối dần, thêm mưa, sét (game), không vẽ thêm;
# - 1 sheet phần động 3 x 2 cho những món đảo Mộc chưa có (lốc lá, cánh hoa, lá trúc, tia nắng, vòng phù văn lá, hạt bồ công anh);
#   lá rơi, gió, lấp lánh, đom đóm, đốm hồn, quầng sáng, sương, sét, mây bão dùng lại ảnh có sẵn (Islands/Anim, BattleBG/Anim).
# Khổ: GPT vẽ dọc 1024 x 1536 một lượt, có sẵn phần trời dư cho máy dài (không cần lượt nối trời như build_troi.py). 880 px dưới
# (y 656..1536) là khung sân 1080 x 928 thu về bề ngang 1024; game lấy y 87..1536 phóng về 1080 x 1528 (600 trời dư + khung 928, như
# bản cao của đảo Thủy; StageView.FitBg neo đáy ảnh vào đáy khung). Hai chỗ đứng theo StageView.Pos, cỡ tướng như build_thuy.py.
# Ghi: gui_gpt/moc/ (<nn>_<mã>.txt, bo_cuc_<mã>.png, HUONG_DAN.md), refs/moc/ (địa danh cắt từ bản đồ dài đảo Mộc đã duyệt, nếu có).
# Chạy: py -3 -I ArtGen/BattleBG/build_moc.py
# Duyệt ảnh GPT đã lưu: --duyet <mã> [ảnh] (mặc định ảnh mới nhất moc/tai_ve/<mã>*.png): lưu moc/<mã>.png, ảnh soi khung
# moc/soi_<mã>.png và bản cao moc/cao_<mã>.png (1080 x 1528), rồi dựng lại gói. Lượt cần ảnh chưa duyệt thì chưa có file prompt.
# Xuất vào game (làm khi có ảnh): theo bảng USES; cần code StageView đọc nền dùng chung và màu phủ (xem PROMPTS.md).
import argparse
import json
import math
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/BattleBG
ART = HERE.parent
PACK = HERE / "gui_gpt" / "moc"
WORK = HERE / "moc"  # <mã>.png: bản duyệt; soi_<mã>.png: ảnh soi khung; cao_<mã>.png: bản cao 1080 x 1528
INBOX = WORK / "tai_ve"  # ảnh GPT lưu
REFS = HERE / "refs" / "moc"
STYLE = HERE / "troi" / "c01.png"  # nền trận Bãi Vỏ Sò đảo Thủy đã duyệt, bản cao 1080 x 1528
OLD = ART / "Islands" / "zones" / "zone_moc.png"  # bản đồ Mộc 8 ải đang dùng
MAP_JSON = ART / "guides" / "zone70_moc.json"  # build_zone70_moc.py: chỗ địa danh trên bản đồ dài
MAP_WORK = ART / "Islands" / "zones" / "moc70"  # doan_k.png: đoạn bản đồ dài đã duyệt
DAIS = ART.parent / "Assets" / "03 Art" / "Islands" / "be_moc_boss.png"
GRID = ART / "guides" / "G_Sheet3x2.png"

CW, CH = 1024, 1536  # khung GPT
FW, FH, EXTRA = 1080, 928, 600  # khung sân, trời dư (tới 21:9)
S = CW / FW
TOP = CH - round(FH * S)  # 656: mép trên khung sân 9:16 trong ảnh GPT
CUT = CH - round((FH + EXTRA) * S)  # 87: phía trên không máy nào thấy
SHOWS = [(300, "2960x1440"), (480, "20:9"), (600, "21:9")]  # phần dôi của vùng sân theo máy (px khung)


def gp(x, y):
    """toạ độ khung sân 1080 x 928 -> ảnh GPT"""
    return x * S, TOP + y * S


def gbox(x0, y0, x1, y1):
    a, b = gp(x0, y0), gp(x1, y1)
    return round(a[0]), round(a[1]), round(b[0]), round(b[1])


FOE, ME = gp(316, 472), gp(784, 836)  # chân địch, chân phe mình (StageView.Pos)
FOE_PLAT = (round(FOE[0]), round(FOE[1] + 4), 344, 100)  # tâm, rộng, cao (như build_thuy.py, đổi tỉ lệ)
FOE_LOW = (round(FOE[0]), round(FOE[1] + 5), 380, 110, 24)  # bệ nổi thấp của chặng có mini boss: tâm mặt trên, rộng, cao, mặt bên
FOE_DAIS = (round(FOE[0]), round(FOE[1] + 7), 404, 117, 38)  # bệ nổi lớn của boss 70
ME_PLAT = (round(ME[0]), round(ME[1] + 6), 464, 137)
FOE_BOX = gbox(198, 110, 434, 472)  # thân tướng địch, cao tới 300 x 1,18 (boss) px khung
ME_BOX = gbox(648, 448, 920, 836)
PANELS = [gbox(583, 0, 1080, 217), gbox(12, 689, 496, 870)]  # bảng tên, máu: địch trên phải, phe mình dưới trái

INK = (43, 33, 24)
COL = {"sky": (200, 230, 248), "sea": (70, 150, 220), "water": (130, 200, 240), "grass": (178, 222, 170),
       "forest": (92, 150, 90), "trunk": (150, 105, 70), "rock": (140, 140, 140), "stone": (205, 198, 178),
       "mark": (222, 222, 222)}
LEGEND = {"sky": "pale blue = sky", "sea": "blue = sea", "water": "light blue = pond or shallow water",
          "grass": "light green = grass, meadow, moss or far hills", "forest": "dark green = trees, leaves, bamboo or far forest",
          "trunk": "brown = big tree trunks, branches and roots", "rock": "dark grey = rocks, cliffs or cave walls",
          "stone": "beige grey = flagstones, stone tiles or a smooth rock floor",
          "mark": "light grey with an ink edge = the landmark"}
LEGEND_VI = {"sky": "xanh nhạt là trời", "sea": "xanh là biển", "water": "xanh sáng là hồ, nước nông",
             "grass": "xanh lá nhạt là cỏ, đồng, rêu, đồi xa", "forest": "xanh lá sẫm là cây, lá, trúc, rừng xa",
             "trunk": "nâu là thân, cành, rễ cây lớn", "rock": "xám sẫm là đá, vách, vách hang",
             "stone": "be xám là sân đá, nền đá phẳng", "mark": "xám nhạt viền mực là địa danh"}


def below(col, yl, yr):
    return ("below", col, (yl, yr))


def ell(col, *box):
    return ("ell", col, box)


def rect(col, *box):
    return ("rect", col, box)


def poly(col, *pts):
    return ("poly", col, pts)


PLAIN = ("text, letters, numbers, signs with writing; creatures, people, birds, insects; any UI, frame or border; "
         "white sticker outlines")

# Mỗi nền: id, kind (c thường, m chặng có mini boss, b boss, fx sheet), spots (số địa danh trên bản đồ dài), chặng và ải dùng nền,
# hình bố cục (toạ độ ảnh GPT 1024 x 1536), câu tả. top: phần trên khung sân (chỉ máy dài thấy).
ARENAS = [
    dict(id="c12", kind="c", spots=[1, 2], place="the Mossy Shore and the Glowing Meadow", stages="1–9",
         vi="Bờ Rêu + Đồng Hoa Sáng", vi_stages="ải 1–9 (chặng 1, 2)",
         shapes=[below("sea", 975, 975),
                 poly("grass", (0, 1022), (300, 1032), (520, 1020), (640, 978), (780, 942), (1024, 912), (1024, CH), (0, CH)),
                 ell("mark", 0, 928, 182, 1066), ell("mark", 872, 876, 1024, 1068)],
         scene="where the forest island meets the sea, on a sunny morning. The calm sea fills the far part on the left up to the "
               "horizon at y = 975, with small soft wave lines; a plain wobbly shoreline with a thin band of pale sand, round "
               "pebbles and moss runs from about y = 1022 at the left edge to y = 1020 at x = 520, just behind the far platform. "
               "On the right the land rises into a gentle green meadow hill whose crest reaches about y = 912 at the right edge. "
               "The near ground is soft grass and moss dotted with small flowers.",
         landmark="two landmarks of the island: at the far left on the shore (x 0-182, y 928-1066) a heap of big round mossy "
                  "boulders and an old moss-covered wooden rowboat (the Mossy Shore); at the right edge on the meadow (x 872-1024, "
                  "y 876-1068) a cluster of giant bell-shaped flowers on tall stems, petals in soft pale yellow, pink and sky blue, "
                  "with big round leaves (the Glowing Meadow).",
         details="reeds and pebbles along the shore, clover patches, small bell flowers scattered over the right half of the "
                 "ground, a few mossy stones, grass tufts.",
         top="the same bright pale-blue sky, hatched with the same diagonal pencil strokes as image 1, becoming only a little deeper "
             "blue towards the very top, with three or four small fluffy cream clouds with thin ink outlines, spread out.",
         plat="both are low round mounds of soft green moss, a little lighter on top, ringed with small pebbles and clover.",
         light="bright sunny morning, light from the top-left.",
         leave="sparkles, floating petals, glowing dots, foam on the shore (the game adds petals and sparkles over the flowers and "
               "small waves on the shore)",
         vi_desc="bờ biển rêu lúc sáng nắng: biển bên trái xa, đồi đồng hoa bên phải; đá rêu và thuyền gỗ rêu bên trái xa, cụm hoa "
                 "chuông khổng lồ ở mép phải"),
    dict(id="c34", kind="c", spots=[3, 4], place="Mushroom Hill and the Vine Forest", stages="10–19",
         vi="Đồi Nấm + Rừng Dây Leo", vi_stages="ải 10–19 (chặng 3, 4)",
         shapes=[below("forest", 880, 898), below("grass", 1002, 1012),
                 poly("trunk", (0, CUT), (128, CUT), (150, 700), (178, 1072), (0, 1072)),
                 poly("forest", (0, CUT), (760, CUT), (720, 230), (420, 300), (140, 320), (0, 330)),
                 rect("forest", 196, 300, 208, 712), rect("forest", 262, 300, 272, 640), rect("forest", 340, 290, 348, 560),
                 ell("mark", 0, 880, 186, 1072), ell("forest", 862, 884, 1024, 1094)],
         scene="a sunny clearing in the forest. A wall of round forest trees closes the back along the horizon (tree tops from "
               "about y = 880 at the left to y = 898 at the right); the near ground from about y = 1002 is soft grass and moss. "
               "At the far left edge a giant old tree trunk wrapped in thick vines rises from the ground to the top of the image; "
               "its huge leafy branch reaches across the top part with long vines hanging from it (the vines end above y = 720 "
               "and stay at x < 360). At the right edge, below y = 884, a round vine-covered bush mound.",
         landmark="at the far left, in front of the giant trunk (x 0-186, y 880-1072), a few giant mushrooms with red and orange "
                  "caps and cream spots; the biggest one is a cottage with a round wooden door and a little round window (Mushroom "
                  "Hill); and the vines everywhere on the trunk, the branch and the right bush (the Vine Forest).",
         details="small mushrooms around the bush mound on the right, ferns, mossy stones, fallen leaves on the grass, a short "
                 "wooden fence far behind on the left.",
         top="the giant leafy branch crossing from the top-left with long hanging vines, the rest a bright pale-blue hatched sky "
             "with two or three small fluffy cream clouds on the right.",
         plat="both are flat tops of huge cut tree stumps with visible pale growth rings, a little moss and a few small "
              "mushrooms on the rim; the tops stay empty.",
         light="warm sunny afternoon, light from the top-left.",
         leave="falling leaves, sunbeams, sparkles, glowing dots",
         vi_desc="bãi trống trong rừng chiều nắng: thân cây cổ thụ quấn dây leo bên trái, cành lá vắt ngang phía trên rủ dây leo; "
                 "nấm khổng lồ có một nấm là nhà bên trái xa; bệ là mặt gốc cây cưa"),
    dict(id="c05", kind="m", spots=[5], place="Wind Fang Cave", stages="20–29", boss_stage=20, boss="Phong Linh",
         vi="Hang Nanh Gió", vi_stages="ải 20 (mini boss Phong Linh) và 21–29",
         shapes=[below("grass", 965, 935),
                 poly("rock", (0, 400), (110, 360), (230, 420), (320, 640), (345, 900), (332, 1046), (0, 1062)),
                 ell("mark", 10, 772, 186, 1036),
                 poly("rock", (884, 1084), (902, 930), (936, 880), (962, 960), (988, 888), (1024, 872), (1024, 1084))],
         fx=[("ell", (10, 772, 186, 1036)), ("rect", (420, 250, 1010, 640))],
         scene="a windswept rocky hillside in front of a great cave, on a windy late afternoon. Rolling grassy hills reach the "
               "horizon (y 965 at the left, 935 at the right); a big grey rocky mound rises at the left from the ground up to "
               "about y = 360 (its right side ends at about x = 345); two leaning fang-shaped rock spires stand at the right edge "
               "(x 884-1024, y 872-1084). The near ground is rocky grass with wind-bent tufts and scattered stones.",
         landmark="the cave mouth in the rocky mound, big and grand at the far left (x 10-186, y 772-1036): a deep dark opening "
                  "whose upper and lower edges are lined with huge pointed rock fangs like an open mouth, a few wind-bent trees "
                  "clinging to the mound above it.",
         details="wind-bent grass and small bent trees on the hills, scattered grey stones, a few loose rocks at the cave mouth.",
         top="the top of the rocky mound at the left; the rest a dramatic windy sky: long fast clouds streaming from the right "
             "to the left, cool blue-grey with warm light breaking through on the right, a little deeper blue towards the very top.",
         plat_far="a low raised round platform of grey stone with a carved swirl pattern on its short side face.",
         plat_near="a flat round slab of grey rock with a little moss on its rim.",
         light="windy late afternoon: cool blue-grey sky with fast streaming clouds and warm light breaking through on the right; "
               "strong but friendly.",
         effects=["wind gusts and swept leaves blowing out of the cave and across the sky (pink dashed box in the sky, pink dashed "
                  "oval at the cave mouth): no wind lines, no flying leaves; keep the inside of the cave plain dark"],
         leave="wind lines, flying leaves, dust puffs",
         vi_desc="sườn đồi đá lộng gió chiều, miệng hang có nanh đá to bên trái xa, hai mỏm đá nanh ở mép phải, mây chạy nhanh"),
    dict(id="c06", kind="m", spots=[6], place="Leaf Valley", stages="30–39", boss_stage=30, boss="Gió Lốc",
         vi="Thung Lũng Lá", vi_stages="ải 30 (mini boss Gió Lốc) và 31–39",
         shapes=[below("forest", 900, 915), below("grass", 990, 1000), ell("water", 0, 958, 560, 1062),
                 poly("trunk", (0, 450), (120, 462), (158, 1002), (0, 1012)),
                 poly("forest", (0, CUT), (360, CUT), (300, 300), (150, 472), (0, 482)),
                 poly("forest", (640, CUT), (1024, CUT), (1024, 600), (900, 560), (760, 400)),
                 ell("forest", 870, 880, 1024, 1092)],
         fx=[("rect", (410, 600, 548, 1000))],
         scene="a deep green valley among giant broad-leaf trees, at golden late afternoon. Forested slopes close the back (tree "
               "tops at about y 900-915); the near ground from about y = 990 is lush grass. A giant tree stands at the left edge "
               "(trunk at x 0-158, its crown filling the top-left), another tree's crown fills the top-right corner above "
               "y = 600, and a round leafy bush stands at the right edge below y = 880.",
         landmark="a round pond right behind the far platform (x 0-560, y 958-1062), covered with giant round lily pads and a few "
                  "pink water lilies; huge broad leaves, bigger than the fighters, arch from the trees on both sides.",
         details="giant leaves lying on the grass, ferns, mossy stones at the pond's edge, small round bushes on the slopes.",
         top="the crowns of the two giant trees with huge broad leaves at the top-left and top-right corners, and between them a "
             "warm golden-blue hatched sky with two small soft clouds.",
         plat_far="a low raised round platform of mossy grey stone on the near bank of the pond, a ring of carved leaves on its "
                  "short side face.",
         plat_near="a flat round slab of mossy stone in the grass.",
         light="golden late afternoon: warm gold light from the top-left through the leaves, green-gold colours.",
         effects=["a whirlwind of leaves that spins up in the valley for the mini-boss battle (pink dashed box): keep the slopes "
                  "and sky there plain", "falling leaves and ripples on the pond: no leaves in the air, no ripple rings"],
         leave="leaves in the air, a whirlwind, ripple rings, sunbeams",
         vi_desc="thung lũng xanh giữa cây lá to lúc chiều vàng, hồ lá sen sau bệ địch, lá khổng lồ vươn hai bên"),
    dict(id="c07", kind="m", spots=[7], place="Dragon Claw Cliff", stages="40–49", boss_stage=40, boss="Long Vuốt",
         vi="Vách Vuốt Rồng", vi_stages="ải 40 (mini boss Long Vuốt) và 41–49",
         shapes=[below("forest", 985, 1000), below("grass", 1010, 1025),
                 poly("rock", (0, CUT), (300, CUT), (370, 380), (420, 700), (432, 1000), (380, 1042), (0, 1052)),
                 rect("mark", 15, 540, 185, 1000),
                 poly("rock", (880, 1086), (900, 930), (935, 880), (960, 960), (985, 890), (1024, 870), (1024, 1086))],
         fx=[("rect", (15, 540, 185, 1000)), ("rect", (440, 958, 1024, 1012))],
         scene="a high grassy rock ledge at the foot of a tall cliff, on a misty morning. The grey-green cliff rises at the left "
               "from the ledge to the top of the image (its right side ends at about x = 432); the ledge's far edge is at about "
               "y = 1010, and beyond it, far below, a sea of round forest treetops lies in soft mist up to the horizon (y 985-1000) "
               "with faint blue mountains behind. Two curved rock spires like giant claws stand at the right edge (x 880-1024, "
               "y 870-1086).",
         landmark="three huge diagonal claw marks slashed deep into the cliff face at the far left (x 15-185, y 540-1000), dark "
                  "gashes with broken rock edges; the rest of the cliff behind the far fighter stays plain rock.",
         details="tufts of grass and small ferns on the ledge, loose stones, a few twisted small pines clinging to the cliff.",
         top="the cliff rising at the left with more claw marks and small pines; on the right a pale silver-green misty morning "
             "sky with soft clouds, a little deeper towards the very top.",
         plat_far="a low raised round platform of grey-green stone with three carved claw marks on its short side face.",
         plat_near="a flat round slab of grey rock with moss on its rim.",
         light="cool misty morning: pale silver-green sky, the low sun at the upper left gives a soft warm glow on the cliff.",
         effects=["the claw marks glow green during the mini-boss battle (pink dashed box on the cliff): draw them as plain dark "
                  "gashes, no glow", "mist drifting along the ledge edge (pink dashed band): soft plain colours there, no mist puffs"],
         leave="glowing marks, mist puffs, falling stones",
         vi_desc="gờ đá cao dưới vách đá sáng sương, ba vết vuốt khổng lồ trên vách bên trái xa, rừng xa trong sương, hai mỏm đá "
                 "cong như vuốt ở mép phải"),
    dict(id="c08", kind="m", spots=[8], place="the Jade Bamboo Forest", stages="50–59", boss_stage=50, boss="Thỏ Hoàng",
         vi="Rừng Trúc Ngọc", vi_stages="ải 50 (mini boss Thỏ Hoàng) và 51–59",
         shapes=[below("forest", 890, 905), below("stone", 1005, 1012),
                 poly("forest", (0, CUT), (230, CUT), (215, 600), (200, 1066), (0, 1066)),
                 poly("forest", (230, CUT), (560, CUT), (420, 200), (240, 262)),
                 ell("mark", 0, 830, 186, 1062), ell("forest", 868, 900, 1024, 1096)],
         scene="a clearing in a jade-green bamboo forest at dusk. Shorter bamboo thickets close the back along the horizon (tops "
               "at about y 890-905); the near ground from about y = 1005 is a courtyard of flat stone tiles with moss in the "
               "joints. Tall bamboo grows at the left edge up to the top of the image, its leafy tops arching over the top-left; "
               "low bamboo bushes stand at the right edge below y = 900.",
         landmark="at the far left, in front of the tall bamboo (x 0-186, y 830-1062), a small stone shrine with a curved "
                  "green-tiled roof and two stone lanterns whose windows glow warm orange.",
         details="bamboo shoots, round mossy stones, a low stone wall far behind, a few fallen bamboo leaves on the tiles.",
         top="the tall bamboo and its arching leafy tops at the left; the rest a calm dusk sky, peach and lilac low, soft violet "
             "higher, two or three small soft clouds.",
         plat_far="a low raised round platform of pale jade-green stone with a carved bamboo-leaf pattern on its short side face.",
         plat_near="a round circle of flat stone tiles with moss in the joints.",
         light="calm dusk: peach and lilac sky, jade-green shadows, warm orange light from the lantern windows.",
         effects=["drifting bamboo leaves, fireflies and the lanterns' glow: no leaves in the air, no glowing dots, no halo around "
                  "the lanterns"],
         leave="leaves in the air, glowing dots, light halos",
         vi_desc="bãi trống trong rừng trúc ngọc lúc chạng vạng, miếu đá mái ngói xanh và hai đèn đá bên trái xa, sân đá lát"),
    dict(id="c09", kind="m", spots=[9], place="the Green Crystal Cave", stages="60–69", boss_stage=60, boss="Mộc Tinh",
         vi="Hang Pha Lê Lục", vi_stages="ải 60 (mini boss Mộc Tinh) và 61–69",
         shapes=[rect("rock", 0, 0, CW, CH), ell("sky", 380, 560, 980, 1180), ell("forest", 420, 930, 940, 1060),
                 below("stone", 1000, 1000), ell("mark", 0, 760, 186, 1062), rect("mark", 888, 880, 1024, 1086)],
         fx=[("ell", (0, 760, 186, 1062)), ("rect", (888, 880, 1024, 1086))],
         scene="inside the entrance hall of a great cave. Dark mossy rock walls close the scene on both sides and above; a wide "
               "arched opening in the back (x 380-980, its top at about y = 560) shows a soft teal twilight sky and the round "
               "tops of a far forest; the floor from about y = 1000 is smooth light-grey rock with patches of bright green moss.",
         landmark="big clusters of emerald-green crystals: a large one at the far left (x 0-186, y 760-1062) and another at the "
                  "right edge (x 888-1024, y 880-1086); smaller crystals hang from the ceiling and dot the walls.",
         details="moss and small ferns on the rock, crystal pebbles on the floor, a few stalagmites near the walls.",
         top="the cave ceiling: dark rock with moss, hanging roots and crystals hanging down, the top of the arched opening.",
         plat_far="a low raised round platform of dark stone with small green crystals around its rim and a short side face.",
         plat_near="a flat round slab of smooth grey rock with tiny crystal pebbles on its rim.",
         light="magical cool twilight: the crystals give a soft green light, the opening shows a teal evening sky; the walls cool "
               "slate and teal, but the floor and the two platforms stay light.",
         effects=["the crystal clusters pulse with light (pink dashed ovals): draw the crystals clear and bright, no halo around "
                  "them", "sparkles and floating spores: no glowing dots, no sparkle stars"],
         leave="glow halos, sparkle stars, glowing dots",
         vi_desc="trong sảnh cửa hang, vách đá rêu tối, cửa vòm lớn phía sau thấy trời chạng vạng, cụm pha lê lục bảo to bên trái "
                 "xa và mép phải"),
    dict(id="b70", kind="b", spots=[10], place="the Thousand-Year Tree", stages="70", boss="Thanh Long",
         vi="Cây Thần Ngàn Năm", vi_stages="ải 70 (boss Thanh Long, 3 dạng)",
         shapes=[below("forest", 975, 990), below("stone", 1022, 1036),
                 poly("trunk", (0, CUT), (230, CUT), (300, 500), (330, 850), (360, 1050), (0, 1062)),
                 poly("forest", (0, CUT), (1024, CUT), (1024, 420), (820, 560), (600, 598), (380, 560), (250, 450), (0, 470)),
                 poly("trunk", (300, 1000), (560, 1014), (800, 1028), (800, 1044), (560, 1034), (300, 1046)),
                 ell("mark", 40, 820, 186, 1000)],
         fx=[("ell", (118, 1062, 482, 1160)), ("ell", (40, 820, 186, 1000))],
         scene="the sacred grove at the top of the forest island, at a dramatic dusk. A giant ancient tree stands at the left: its "
               "massive gnarled trunk (x 0-360 at the ground, narrower higher) rises to the top of the image, and its huge round "
               "crown of leaves spreads across the whole top part, its lower edge at about y = 560-600; thick roots curl along "
               "the ground behind the arena (y 1000-1046). Beyond the grove's edge, far forest hills and a sea of mist reach the "
               "horizon (y 975-990). The ground from about y = 1022 is old mossy flagstones crossed by small roots.",
         landmark="the trunk of the great tree, big and grand, with a small shrine in a hollow of the trunk at the far left "
                  "(x 40-186, y 820-1000): a little wooden shrine with a curved roof, glowing warm gold inside.",
         details="moss and small ferns between the flagstones, two old stone lanterns far on the right, roots and mossy stones "
                 "along the arena edge.",
         top="the huge crown of the great tree across the whole top part, with gaps of stormy sky; heavy teal-violet storm "
             "clouds gathering behind it.",
         plat_far="a grand raised round dais of carved mossy stone: leaf-and-vine carvings on its side face, a gold ring inlaid "
                  "in its top, roots of the great tree curling around its back rim (never onto its top).",
         plat_near="a flat round slab of mossy stone.",
         light="the climax of the island: deep teal-green and violet dusk, heavy storm clouds gathering, warm golden light from "
               "the shrine and a golden rim on the trunk and the dais. Grand and dramatic, still cute, not horror. The game darkens "
               "this image for the boss's later forms and adds rain and lightning, so keep it clear, rich and not too dark.",
         effects=["a green rune circle that lights up on the dais top (pink dashed oval): keep the top plain stone with only the "
                  "gold ring", "the shrine's glow and glowing spirit motes rising from it (pink dashed oval): a soft warm light "
                  "inside the hollow, no halo, no glowing dots", "falling leaves from the crown, rain and lightning in the later "
                  "forms: no leaves in the air, plain clouds, no rain, no lightning"],
         leave="glowing runes, glowing dots, leaves in the air, rain, lightning",
         vi_desc="rừng thiêng trên đỉnh đảo lúc chạng vạng bão, thân cây thần to bên trái có miếu nhỏ trong hốc, tán phủ cả phần "
                 "trên, rễ ôm sau sân; bệ boss nổi chạm lá dây, vòng vàng"),
    dict(id="fx", kind="fx", vi="Sheet phần động đảo Mộc", vi_stages="ải 1–70",
         items=["a small whirlwind: a tall twisting funnel of pale wind lines, narrow at the bottom and wide at the top, with five "
                "or six green leaves caught in it, thin ink outline",
                "a single pink flower petal, slightly curled, with a thin ink outline",
                "a long slim jade-green bamboo leaf with a pointed tip and a thin ink outline",
                "a long soft diagonal sunbeam: a band of pale warm yellow light, wider at the bottom, solid pale yellow with soft "
                "yellow pencil hatching, no ink outline",
                "a glowing green rune circle seen at a low angle (a wide flat ellipse): a ring of leaf and vine patterns and small "
                "dots inside a double ring, pale glowing green",
                "a dandelion seed: a small brown seed with a round white puff of fine threads on a thin stem"],
         names=["whirlwind", "petal", "bamboo", "sunbeam", "leafrune", "seed"],
         vi_desc="6 món: lốc lá, cánh hoa hồng, lá trúc, tia nắng chéo, vòng phù văn lá, hạt bồ công anh"),
]
BY_ID = {a["id"]: a for a in ARENAS}
KIND_VI = {"c": "thường", "m": "chặng có mini boss", "b": "boss", "fx": "phần động"}

# Game dùng nền thế nào (xuất làm khi có ảnh): khoá nền game -> (ảnh duyệt, màu phủ hoặc None, phần động). Ải mini boss, boss phủ màu
# tối nhẹ và thêm phần động mạnh hơn; boss dạng 2, 3 phủ tối dần, thêm mưa, sét. Ảnh có sẵn dùng lại: Islands/Anim anim_leaf,
# anim_wind, anim_sparkle; BattleBG/Anim san_firefly, san_wisp, san_glow, san_mist, san_bolt, san_cloud.
USES = {
    "moc_c01": ("c12", None, "cánh hoa, lấp lánh ở cụm hoa, sóng nhỏ mép bờ"),
    "moc_c02": ("c12", None, "như c01"),
    "moc_c03": ("c34", None, "lá rơi, tia nắng"),
    "moc_c04": ("c34", None, "như c03"),
    "moc_c05": ("c05", None, "gió (anim_wind), lá bay"),
    "moc_s20": ("c05", "#e4e0ee", "gió mạnh, lốc lá ở miệng hang"),
    "moc_c06": ("c06", None, "lá rơi, gợn hồ, tia nắng"),
    "moc_s30": ("c06", "#efe2cf", "lốc lá lớn giữa thung lũng, lá bay dày"),
    "moc_c07": ("c07", None, "sương dọc gờ đá"),
    "moc_s40": ("c07", "#dfe4e8", "vết vuốt sáng xanh, sương dày"),
    "moc_c08": ("c08", None, "lá trúc bay, quầng đèn"),
    "moc_s50": ("c08", "#e6dcee", "lá trúc bay dày, đom đóm"),
    "moc_c09": ("c09", None, "quầng pha lê, lấp lánh"),
    "moc_s60": ("c09", "#d8e4e0", "pha lê bừng sáng, đốm hồn bay"),
    "moc_s70": ("b70", None, "vòng phù văn lá trên bệ, quầng miếu, đốm hồn, lá rơi"),
    "moc_s70_2": ("b70", "#b8bcd8", "thêm mây bão trôi, mưa"),
    "moc_s70_3": ("b70", "#7f82b4", "thêm mưa dày, sét kèm chớp màn"),
}


def approved(i):
    return WORK / f"{i}.png"


def needs(a):
    return [] if a["id"] == "c12" else ["c12"]


def ready(a):
    return all(approved(n).exists() for n in needs(a))


# ---------- ảnh mẫu ----------

def map_spots():
    """chỗ địa danh trên bản đồ dài đảo Mộc (build_zone70_moc.py): số -> (x, y) px bản đồ ghép"""
    if not MAP_JSON.exists():
        return {}
    d = json.loads(MAP_JSON.read_text(encoding="utf-8"))
    mw, mh = d["map"]
    out = {}
    for i, st in enumerate(d["stages"]):
        p = st.get("spot") or st.get("bridge")
        if p:
            out[i + 1] = (p[0] * mw, p[1] * mh)
    return out, d


SLUG = {1: "bo_reu", 2: "dong_hoa_sang", 3: "doi_nam", 4: "rung_day_leo", 5: "hang_nanh_gio", 6: "thung_lung_la",
        7: "vach_vuot_rong", 8: "rung_truc_ngoc", 9: "hang_pha_le_luc", 10: "cay_than"}
SPOT_EN = {1: "the mossy boulders and the old mossy rowboat on the shore", 2: "the giant bell flowers of the meadow",
           3: "the giant mushrooms and the mushroom cottages", 4: "the vine-wrapped wooden bridge and the vine trees",
           5: "the cave mouth with the stone fangs", 6: "the lily-pad pond", 7: "the cliff with the claw marks",
           8: "the bamboo grove and the little shrine", 9: "the cave mouth with the green crystals",
           10: "the great tree with its shrine"}
SPOT_VI = {1: "đá rêu, thuyền gỗ rêu trên bờ", 2: "cụm hoa chuông khổng lồ", 3: "nấm khổng lồ, nhà nấm", 4: "cầu gỗ quấn dây leo",
           5: "miệng hang có nanh đá", 6: "hồ lá sen", 7: "vách có vết vuốt", 8: "rừng trúc và miếu nhỏ", 9: "hang pha lê lục",
           10: "cây thần có miếu"}


# chỗ thật của địa danh trên đoạn đã duyệt (px bản đồ ghép) khi GPT vẽ lệch bố cục: đoạn 2 (2026-11-05) vẽ vách vuốt rồng lệch trái
# khoảng 180 px, hồ lá sen và rừng trúc lệch ít
SPOT_FIX = {6: (742, 2540), 7: (245, 2141), 8: (753, 1713)}


def make_refs():
    """cắt địa danh khỏi đoạn bản đồ dài đảo Mộc đã duyệt (512 x 512 quanh chỗ địa danh); đoạn chưa duyệt thì chưa có"""
    got = map_spots()
    if not got:
        return
    spots, d = got
    spots.update(SPOT_FIX)
    mw, mh = d["map"]
    sh, ov, nseg = 1536, d["overlap"], d["segments"]
    REFS.mkdir(parents=True, exist_ok=True)
    for num, (x, y) in spots.items():
        for k in range(nseg):
            top = mh - sh - k * (sh - ov)
            seg = MAP_WORK / f"doan_{k + 1}.png"
            if top <= y < top + sh and seg.exists():  # địa danh tránh dải nối nên chỉ nằm trong một đoạn
                with Image.open(seg) as im:
                    x0 = min(max(round(x) - 256, 0), mw - 512)
                    y0 = min(max(round(y - top) - 256, 0), sh - 512)
                    im.convert("RGB").crop((x0, y0, x0 + 512, y0 + 512)).save(REFS / f"{num:02d}_{SLUG[num]}.png")
                break


def crop_of(num):
    p = REFS / f"{num:02d}_{SLUG[num]}.png"
    return p if p.exists() else None


def size_of(p):
    try:
        with Image.open(p) as im:
            return im.size
    except OSError:
        return None


def ref_list(a):
    """[(đường dẫn, câu cho GPT, câu cho người dùng)] theo thứ tự ảnh"""
    k = a["kind"]
    if k == "fx":
        return [(approved("c12"), "an approved battle background of this game: copy its RENDERING (ink, pencil hatching, colours); "
                                  "ignore its content", "nền trận Bờ Rêu + Đồng Hoa Sáng đã duyệt (1024 × 1536, nền đặc): lấy nét"),
                (GRID, "the numbered 3 x 2 grid: one object per cell, in number order",
                 "lưới 3 × 2 đánh số (1536 × 1024, nền trắng, ô viền hồng, số hồng ở góc): mỗi ô một món")]
    out = []
    if a["id"] == "c12":
        out.append((STYLE, "an approved battle background of ANOTHER island of this game, in the same tall format: copy its "
                           "RENDERING, perspective, platform size and look, and the plain hatched sky with small clouds in the "
                           "top part; not its content or colours",
                    "nền trận Bãi Vỏ Sò đảo Thủy đã duyệt, bản cao (1080 × 1528, nền đặc): bãi cát, biển, hai bệ cát, trời xanh "
                    "gạch chì có mây nhỏ ở phần trên; lấy nét, góc nhìn, cỡ và kiểu bệ"))
        out.append((OLD, "the old small map of this Wood island: copy its colours and the look of its objects (bright green "
                         "hatched grass, round trees, mossy grey rocks, red spotted mushrooms, flowers, vines); ignore its layout",
                    "bản đồ đảo Mộc 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo xanh lá gạch chì, nấm đỏ, hoa, dây leo, hang "
                    "đá có nanh, cây thần; lấy màu và dáng đồ vật"))
    else:
        copy = ("copy its rendering, colours, perspective, platform look and brightness; not its content" if k == "c" else
                "copy its rendering, perspective and platform look; not its content, colours or daylight (this place has its own "
                "light)")
        out.append((approved("c12"), f"the approved battle background of this island (a normal stage): {copy}",
                    "nền trận Bờ Rêu + Đồng Hoa Sáng đã duyệt (1024 × 1536, nền đặc): lấy nét, góc nhìn, kiểu bệ, độ sáng"))
    crops = [n for n in a["spots"] if crop_of(n)]
    for n in crops:
        sz = size_of(crop_of(n)) or (512, 512)
        out.append((crop_of(n), f"a crop of this island's new map, seen from above, showing {SPOT_EN[n]}: draw the same landmark "
                                f"here, seen from the side, with its colours and shapes",
                    f"mảnh cắt bản đồ dài đảo Mộc ({sz[0]} × {sz[1]}, nhìn từ trên xuống): {SPOT_VI[n]}"))
    if a["id"] != "c12" and not crops:
        out.append((OLD, "the old small map of this Wood island: the look of its objects (round trees, mossy rocks, mushrooms, the "
                         "cave with stone fangs, the great tree with its shrine); ignore its layout",
                    "bản đồ đảo Mộc 8 ải đang dùng (1024 × 1536, nền trong suốt): lấy dáng đồ vật"))
    if k in ("m", "b"):
        out.append((DAIS, "the island map's boss plate: a raised round platform with a flat top, a visible side face and a ring on "
                          "its top; copy only this idea for the far platform, in the material described below" +
                          (", lower and simpler" if k == "m" else ""),
                    "bệ boss của bản đồ đảo Mộc (400 × 250, nền trong suốt): đĩa cỏ dày có mặt bên đất, vòng vàng trên mặt, đá viền"))
    out.append((PACK / f"bo_cuc_{a['id']}.png", "the layout sketch of the image you draw now: follow it exactly",
                f"bố cục lượt này (1024 × 1536): {sketch_vi(a)}"))
    return out


# ---------- bố cục ----------

def wavy(yl, yr, ph=0.0, amp=6):
    return [(x, yl + (yr - yl) * x / CW + amp * math.sin(x / 60 + ph)) for x in range(0, CW + 1, 16)]


def dashed_ellipse(d, box, col, width=5, n=40):
    for k in range(n):
        d.arc(box, k * 360 / n, (k + 0.55) * 360 / n, fill=col, width=width)


def dashed_rect(d, box, col, width=5, step=26):
    x0, y0, x1, y1 = box
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        L = math.dist(a, b)
        for s in range(0, int(L), step):
            t0, t1 = s / L, min(1, (s + step * 0.55) / L)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                   fill=col, width=width)


def dashed_hline(d, y, col, width=4, step=30):
    for x in range(0, CW, step):
        d.line([(x, y), (min(CW, x + step * 0.55), y)], fill=col, width=width)


def draw_plat(d, cx, cy, w, h, side=0, ring=False):
    if side:
        d.ellipse((cx - w / 2, cy - h / 2 + side, cx + w / 2, cy + h / 2 + side), fill=(205, 170, 120), outline=INK, width=6)
        d.rectangle((cx - w / 2, cy, cx + w / 2, cy + side), fill=(205, 170, 120))
        d.line([(cx - w / 2, cy), (cx - w / 2, cy + side)], fill=INK, width=6)
        d.line([(cx + w / 2, cy), (cx + w / 2, cy + side)], fill=INK, width=6)
    d.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(252, 244, 214), outline=INK, width=6)
    if ring:
        d.ellipse((cx - w / 2 + 34, cy - h / 2 + 12, cx + w / 2 - 34, cy + h / 2 - 12), outline=(236, 186, 58), width=6)


def overlay_frame(im, lines=True):
    """bảng máu (gạch chéo xám), phần không máy nào thấy (tối), mép trên khung 9:16 (nét đứt trắng)"""
    for (x0, y0, x1, y1) in PANELS:
        layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        hgt = y1 - y0
        for k in range(-hgt, x1 - x0, 22):
            ld.line([(k, hgt), (k + hgt, 0)], fill=(90, 90, 90, 200), width=4)
        im.alpha_composite(layer, (x0, y0))
    shade = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    ImageDraw.Draw(shade).rectangle((0, 0, CW, CUT), fill=(20, 20, 30, 140))
    im.alpha_composite(shade)
    if lines:
        dashed_hline(ImageDraw.Draw(im), TOP, (255, 255, 255))


def platforms(a):
    k = a["kind"]
    if k == "b":
        return FOE_DAIS, True
    if k == "m":
        return FOE_LOW, False
    return FOE_PLAT + (0,), False


def draw_sketch(a):
    im = Image.new("RGBA", (CW, CH), COL["sky"] + (255,))
    d = ImageDraw.Draw(im)
    for i, (kind, col, g) in enumerate(a["shapes"]):
        fill = COL[col]
        if kind == "below":
            line = wavy(g[0], g[1], i)
            d.polygon(line + [(CW, CH), (0, CH)], fill=fill)
            d.line(line, fill=INK, width=4)
        elif kind == "ell":
            d.ellipse(g, fill=fill, outline=INK, width=4)
        elif kind == "rect":
            d.rectangle(g, fill=fill, outline=INK if col != "rock" or g[2] - g[0] < CW else None, width=4)
        elif kind == "poly":
            d.polygon(list(g), fill=fill, outline=INK, width=4)
    (cx, cy, w, h, side), ring = platforms(a)
    draw_plat(d, cx, cy, w, h, side, ring)
    draw_plat(d, *ME_PLAT)
    for kind, box in a.get("fx", []):
        (dashed_ellipse if kind == "ell" else dashed_rect)(d, box, (240, 40, 200))
    dashed_rect(d, FOE_BOX, (255, 255, 255), 4, 20)
    dashed_rect(d, ME_BOX, (255, 255, 255), 4, 20)
    overlay_frame(im)
    return im.convert("RGB")


def colours(a):
    cols = []
    for _, c, _ in a["shapes"]:
        if c not in cols and c != "sky":
            cols.append(c)
    return cols


def sketch_vi(a):
    parts = [LEGEND_VI["sky"]] + [LEGEND_VI[c] for c in colours(a)]
    note = {"b": " (bệ địch là bệ nổi lớn có mặt bên và vòng vàng)", "m": " (bệ địch là bệ nổi thấp có mặt bên)"}.get(a["kind"], "")
    parts.append("hai bầu dục kem viền mực là hai bệ" + note)
    if a.get("fx"):
        parts.append("nét đứt hồng là chỗ để trống cho phần động")
    parts += ["khung trắng nét đứt là thân hai tướng", "gạch chéo xám là chỗ bảng máu che",
              f"nét đứt trắng ngang y {TOP} là mép trên màn 9:16 (máy dài thấy thêm phía trên)",
              f"dải tối trên cùng ({CUT} px) không máy nào thấy"]
    return "; ".join(parts)


def sketch_en(a):
    parts = [LEGEND["sky"]] + [LEGEND[c] for c in colours(a)]
    note = {"b": " (the far one drawn as a grand raised dais with a side face and a gold ring)",
            "m": " (the far one drawn as a low raised platform with a short side face)"}.get(a["kind"], "")
    parts.append("cream ovals with a thick ink edge = the two platforms" + note)
    if a.get("fx"):
        parts.append("pink dashed outlines = places to keep plain for the game's moving effects (see EFFECTS)")
    parts += ["white dashed boxes = the fighters' bodies", "grey diagonal lines = covered by the game's panels",
              f"white dashed line across at y = {TOP} = the top edge of the battle area on ordinary phones",
              f"dark strip at the very top = never shown"]
    return "; ".join(parts)


# ---------- file prompt ----------

def head(refs):
    out = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save "
           "it as described under SAVE. Do not reply with text only.", "",
           "REFERENCE IMAGES (open each file from its full path):"]
    for i, (p, en, _) in enumerate(refs):
        sz = size_of(p) if p.exists() else ((CW, CH) if p.name.startswith("bo_cuc") or p.parent == WORK else None)
        dim = f" ({sz[0]} x {sz[1]})" if sz else ""
        out.append(f"image {i + 1} = {p}{dim}: {en}")
    return out


def save_block(a, w=CW, h=CH):
    p = INBOX / f"{a['id']}.png"
    return ["", f"SAVE: save the finished image as a {w} x {h} PNG to", str(p),
            f"Create the folder if it is missing. If that file already exists, save it as {a['id']}_2.png, {a['id']}_3.png … in the "
            f"same folder instead. Do not change, move or delete any other file."]


def frame_text(a, n_sketch):
    return [
        "",
        f"TALL FORMAT: draw a vertical {CW} x {CH} image. Ordinary phones show only its bottom {CH - TOP} px (the battle area, "
        f"from the white dashed line at y = {TOP} down); longer phones show more of the top, up to y = {CUT} on the longest. The "
        f"top {CUT} px (dark strip in the sketch) are never shown. So everything the battle needs (both platforms, the landmark, "
        f"the horizon) is in the bottom {CH - TOP} px, and the top part only continues the scene upward.",
        "",
        "VIEW: a side three-quarter view like a stage in a picture book: eye level a little above the fighters' heads, looking "
        "slightly down; the ground rises towards the horizon and things get smaller with distance. Not a top-down map.",
        "",
        f"LAYOUT: follow image {n_sketch} exactly. It is only a colour-coded plan: {sketch_en(a)}. Do not copy its flat colours, its "
        f"grey diagonal lines, its dashed lines or its dark strip.",
        "",
        f"FIGHTERS: the far fighter is up to about {FOE_BOX[3] - FOE_BOX[1]} px tall (white dashed box x {FOE_BOX[0]}-{FOE_BOX[2]}, "
        f"y {FOE_BOX[1]}-{FOE_BOX[3]}), the near one up to about {ME_BOX[3] - ME_BOX[1]} px (box x {ME_BOX[0]}-{ME_BOX[2]}, "
        f"y {ME_BOX[1]}-{ME_BOX[3]}). Right behind their bodies keep only calm sky, water, rock or ground: no tall object, bright "
        f"spot or busy pattern. Keep the diagonal between the two platforms open and calm (flat ground or water, a few small "
        f"tufts): the fighters lunge across it.",
        "",
        f"PANELS: the game covers the top-right of the battle area (x {PANELS[0][0]}-{PANELS[0][2]}, y {PANELS[0][1]}-"
        f"{PANELS[0][3]}) and the bottom-left (x {PANELS[1][0]}-{PANELS[1][2]}, y {PANELS[1][1]}-{PANELS[1][3]}) with "
        f"name-and-health panels (grey diagonal lines in the sketch). Draw only plain sky, water or ground there: no landmark, no "
        f"tree top, no bright spot.",
    ]


def platforms_text(a):
    mx, my, mw, mh = ME_PLAT
    near = (f"the near one centred at ({mx}, {my}), about {mw} x {mh} px, its bottom edge about {CH - my - mh // 2} px above the "
            f"image bottom")
    k = a["kind"]
    if k in ("m", "b"):
        cx, cy, w, h, side = FOE_DAIS if k == "b" else FOE_LOW
        far = (f"the far one is a {'grand raised boss dais' if k == 'b' else 'low raised platform'}: its flat top centred at "
               f"({cx}, {cy}), about {w} x {h} px, with a side face about {side} px tall below it")
        mat = f"Far platform: {a['plat_far']} Near platform: {a['plat_near']}"
    else:
        cx, cy, w, h = FOE_PLAT
        far = f"the far one centred at ({cx}, {cy}), about {w} x {h} px"
        mat = f"Material: {a['plat']}"
    return ["", f"PLATFORMS: exactly where the sketch has them, same centre and size: {far}; {near}. Their tops are flat, level, "
                f"EMPTY and a little lighter than the ground around them, with a crayon-hatched rim and a soft contact shadow; "
                f"nothing stands on them. {mat}"]


def rendering_text(a):
    if a["id"] == "c12":
        return ["", "RENDERING: copy image 1's rendering: wobbly dark-brown ink outlines (#2B2118), coloured-pencil hatching on "
                    "cream paper, flat warm colours with light watercolour washes, chunky cute doodle shapes with clear "
                    "silhouettes; the same perspective, the same platform size and look, the same plain hatched sky. Ink about "
                    "6 px on near things and 3-4 px on far things. Use the colours and the look of the objects of image 2 (bright "
                    "green hatched grass, round trees, mossy grey rocks, flowers): a green forest island, not a beach. Not 3D, not "
                    "glossy, no realistic rendering, no tiny noisy details.",
                "",
                "CONTRAST: the fighters must stand out, so the background is a little softer and lighter than the old map, with "
                "the most detail and contrast on the landmarks and along the left and right edges; the middle stays simple."]
    return ["", "RENDERING: exactly as image 1 (the approved battle background of this island): the same ink, hatching, paper, "
                "perspective, platform size and look. Not 3D, not glossy, no tiny noisy details. The fighters must stand out: most "
                "detail and contrast on the landmark and along the left and right edges; the middle stays simple."]


def arena_prompt(a, refs):
    k = a["kind"]
    lines = head(refs) + save_block(a)
    if k == "c":
        what = (f"the battle background for the stages at {a['place']} (stages {a['stages']}) of the Wood island, a forest "
                f"island, in a vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added "
                f"by the game) fight on it: the enemy on the smaller far platform at the upper left, the player's fighter on the "
                f"bigger near platform at the lower right.")
    elif k == "m":
        what = (f"the battle background for {a['place']} (stages {a['stages']}) of the Wood island, a forest island, in a "
                f"vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added by the "
                f"game) fight on it: the enemy on the far raised platform at the upper left, the player's fighter on the bigger "
                f"near platform at the lower right.")
    else:
        what = (f"the battle background for the final boss stage at {a['place']} (stage 70) of the Wood island, a forest island, "
                f"in a vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added by the "
                f"game) fight on it: the boss on the far raised dais at the upper left, the player's fighter on the bigger near "
                f"platform at the lower right.")
    lines += ["", f"WHAT THIS IS: {what}"]
    dais = len(refs) - 1  # ảnh bệ boss đứng ngay trước bố cục
    if k == "m":
        s0 = a["boss_stage"]
        lines += ["", f"THIS PLACE ALSO HOSTS A MINI-BOSS: the game uses this same image for the mini-boss battle (stage {s0}) and "
                      f"for the normal stages after it (stages {s0 + 1}-{s0 + 9}), adding moving effects and a slightly darker tint "
                      f"for the mini-boss. So give the place its own strong mood (time of day, weather) and a big, grand landmark, "
                      f"richer than a plain stage, but keep it light and readable for everyday battles, cute and cosy, never scary. "
                      f"The far platform is a low raised round platform with a short side face (the idea of image {dais}, built from "
                      f"the material below), used by every enemy here."]
    if k == "b":
        lines += ["", f"THIS IS THE ISLAND'S FINAL BOSS STAGE: the most spectacular background of the island, grand, stormy and "
                      f"magical, but still cute and cosy, never scary. The far platform is a grand raised boss dais (the idea of "
                      f"image {dais}, built from the material below)."]
    lines += rendering_text(a)
    lines += frame_text(a, len(refs))
    lines += ["", f"SCENE: {a['scene']}", "", f"LANDMARK: {a['landmark']}"]
    crops = [i + 1 for i, (p, _, _) in enumerate(refs) if p.parent == REFS]
    if crops:
        lines.append(f"Draw it like image{'s' if len(crops) > 1 else ''} {', '.join(map(str, crops))} (the same landmark on the "
                     f"island map, seen from above there; draw it from the side here, much bigger).")
    lines += ["", f"DETAILS: {a['details']}", "", f"TOP PART (y {CUT}-{TOP}, only on longer phones): {a['top']}"]
    lines += platforms_text(a)
    lines += ["", f"LIGHT: {a['light']}"]
    if a.get("effects"):
        lines += ["", "EFFECTS: the game animates these on top of your image, so leave their places as described and do NOT draw "
                      "them:"] + [f"- {e};" for e in a["effects"]]
    lines += ["", f"Do not draw: {PLAIN}; {a['leave']}.", "", f"Remember: save the image to {INBOX / (a['id'] + '.png')}"]
    return "\n".join(lines) + "\n"


def fx_prompt(a, refs):
    rows, cols = 2, 3
    gw, gh = 1536, 1024
    cw, ch = gw // cols, gh // rows
    lines = head(refs) + save_block(a, gw, gh)
    lines += ["",
              f"WHAT THIS IS: a sprite sheet of {len(a['items'])} separate effect objects for the battle backgrounds of the Wood "
              f"island (a forest island) of a vertical mobile game. The game cuts the sheet into {len(a['items'])} sprites and "
              f"animates them (moves, spins, fades, scales, makes them see-through), so draw each object complete and on its own.",
              "",
              f"Draw a {gw} x {gh} image with a fully TRANSPARENT background (PNG with alpha), in the rendering of image 1 (same "
              f"wobbly ink, same pencil hatching, same colours). One object per cell of image 2's numbered {cols} x {rows} grid "
              f"({cw} x {ch} px cells): each object about the size of the cell's inner grey frame and centred in its cell, "
              f"nothing crossing a cell edge, no ground, no shadow, no background colour, no grid lines, no numbers. Glows and "
              f"light are drawn as solid pale shapes (the game makes them see-through).",
              "",
              "In grid order:"]
    lines += [f"{i + 1} {t};" for i, t in enumerate(a["items"])]
    lines += ["", f"Do not draw: {PLAIN}.", "", f"Remember: save the image to {INBOX / (a['id'] + '.png')}"]
    return "\n".join(lines) + "\n"


def prompt(a):
    refs = ref_list(a)
    return (fx_prompt if a["kind"] == "fx" else arena_prompt)(a, refs)


# ---------- hướng dẫn ----------

def guide():
    rows = []
    for n, a in enumerate(ARENAS, 1):
        name = f"{n:02d}_{a['id']}.txt"
        if ready(a):
            refs = "; ".join(f"{i + 1} `{p}`: {vi}" for i, (p, _, vi) in enumerate(ref_list(a)))
            file = f"`{PACK / name}`"
        else:
            refs = "chưa có: cần " + ", ".join(f"`{x}`" for x in needs(a) if not approved(x).exists()) + " đã duyệt"
            file = "chưa dựng"
        size = "1536 × 1024, nền trong suốt" if a["kind"] == "fx" else "1024 × 1536"
        rows.append(f"| {n}. {a['vi']}; {a['vi_stages']}, {KIND_VI[a['kind']]}: {a['vi_desc']} ({size}) | {file} | {refs} | "
                    f"`{INBOX / (a['id'] + '.png')}` |")
    use_rows = []
    for key, (img, tint, fx) in USES.items():
        use_rows.append(f"| `battle_{key}` | `{img}` | {tint or 'không'} | {fx} |")
    return f"""# Gói gửi GPT: sàn đấu đảo Mộc 70 ải (`moc`)

Sinh bằng `{HERE / 'build_moc.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè). Nền trận cho 70 ải đảo Mộc, **tiết kiệm dung lượng: 8 nền thay cho 17 nền của đảo Thủy**, game dùng lại nền:
- **2 nền thường**, mỗi nền cho hai chặng đầu liền nhau: Bờ Rêu + Đồng Hoa Sáng (ải 1–9), Đồi Nấm + Rừng Dây Leo (ải 10–19).
- **5 nền chặng có mini boss** (Hang Nanh Gió, Thung Lũng Lá, Vách Vuốt Rồng, Rừng Trúc Ngọc, Hang Pha Lê Lục): ải mini boss (20, 30, 40, 50, 60) và các ải thường sau nó dùng chung một nền; mỗi nơi một giờ, một thời tiết riêng, địa danh to; ải mini boss game phủ màu tối nhẹ và thêm phần động mạnh hơn.
- **1 nền boss ải 70** (Cây Thần Ngàn Năm). Dạng 2, 3 của Thanh Long không vẽ thêm: game phủ tối dần, thêm mây bão, mưa, sét.
- **1 sheet phần động** 3 × 2 cho những món đảo Mộc chưa có. Lá rơi, gió, lấp lánh, đom đóm, đốm hồn, quầng sáng, sương, sét, mây bão dùng lại ảnh đã có.

**Khổ dọc, vẽ một lượt:** GPT vẽ 1024 × 1536. 880 px dưới (từ nét đứt trắng y {TOP}) là khung sân máy 9:16, phần trên là trời, tán cây dư cho máy dài (như bản nối trời của đảo Thủy, nhưng không cần lượt nối riêng). Game lấy y {CUT}..1536 phóng về 1080 × 1528.

Ước dung lượng (ASTC 6×6 như nền đảo Thủy, 1080 × 1528 khoảng 0,7 MB mỗi nền): đảo Mộc 8 nền khoảng 5,6 MB, đảo Thủy 17 nền khoảng 11,9 MB.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Làm lượt 1 trước (chốt nét): GPT lưu xong thì nhắn Claude "duyệt c12"; Claude soi, lưu bản duyệt và dựng file prompt các lượt sau. Nên làm mọi lượt trong cùng một chat để GPT giữ nét.

Gói bản đồ dài đảo Mộc (`{ART / 'Islands' / 'gui_gpt' / 'zone_moc_70'}`) làm song song được, ở chat khác. Đoạn bản đồ nào đã duyệt thì lượt nền trận của các địa danh trong đoạn đó có thêm ảnh cắt địa danh (Claude dựng lại gói khi duyệt), để địa danh trên nền trận giống bản đồ.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
{chr(10).join(rows)}

Bản duyệt Claude lưu ở `{WORK}\\<mã>.png`, kèm ảnh soi khung `soi_<mã>.png` và bản cao vào game `cao_<mã>.png` (1080 × 1528).

## Game dùng nền thế nào

Xuất vào game làm khi có ảnh; cần thêm code để `StageView` đọc nền dùng chung và màu phủ (hiện chỉ tìm `battle_<đảo>_s<ải>` rồi `battle_<đảo>_c<chặng>`).

| Khoá nền game | Ảnh | Màu phủ | Phần động |
|---|---|---|---|
{chr(10).join(use_rows)}

## Soi trước khi nhắn Claude

- Ảnh dọc 1024 × 1536. Hai bệ đúng chỗ như bố cục (bệ xa trên trái, bệ gần to dưới phải); mặt bệ **trống**.
- Mọi thứ trận cần (hai bệ, địa danh, chân trời) nằm dưới nét đứt trắng; phần trên chỉ là trời, tán cây, vách nối lên.
- Giữa hai bệ thoáng; ngay sau lưng hai tướng (khung trắng nét đứt) không có vật cao, chỗ sáng.
- Góc trên phải và dưới trái của khung sân (gạch chéo xám) chỉ có trời, nước, đất: bảng máu che chỗ đó.
- Đảo rừng xanh lá (lượt 1 không lấy màu cát biển của ảnh mẫu đảo Thủy).
- Chặng có mini boss, boss: rõ là nơi đặc biệt (giờ, thời tiết, địa danh to, bệ địch nổi có mặt bên) mà vẫn đủ sáng cho ải thường, dễ thương, không đáng sợ.
- **Không vẽ phần động** file đã dặn chừa (vệt gió, lá bay, lốc, sương, quầng sáng, đom đóm, phù văn, mưa, sét).
- Sheet: nền trong suốt, mỗi món gọn trong ô của mình, không viền lưới, không số.
- Không chữ, số, sinh vật, người, khung viền.

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Ra ảnh ngang hoặc vuông | `Redraw it as a vertical 1024 x 1536 image following the sketch: the battle area in the bottom 880 px, sky and tree tops above.` |
| Bệ lệch chỗ hoặc sai cỡ | `Same image, but put the two platforms exactly where the sketch has them: same centre and size.` |
| Có đồ trên bệ, giữa hai bệ rối | `Same image, but keep both platform tops empty and the ground between the two platforms calm and simple.` |
| Vật cao, chỗ sáng sau lưng tướng | `Same image, but nothing tall or bright right behind the fighters' places (the white dashed boxes of the sketch).` |
| Vẽ đồ ở chỗ bảng máu | `Same image, but only plain sky, water or ground in the top-right and bottom-left areas the sketch crosses with grey lines.` |
| Lượt 1 ra bãi cát như đảo Thủy | `Same layout, but this is the green forest island: soft green grass and moss, mossy rocks, flowers; only a thin sandy line at the shore.` |
| Vẽ cả phần động | `Same image, but remove the [wind lines / flying leaves / whirlwind / mist / glow / fireflies / runes / rain / lightning]; leave that place plain as the file says.` |
| Chặng mini boss, boss chưa đủ "đã" | `Make it more dramatic and special: a bigger, grander landmark, a stronger sky and light, richer details along the left and right edges. Keep the layout, the platforms and the empty places.` |
| Tối quá, tướng sẽ chìm | `Same image, a little lighter in the middle, and the two platform tops clearly lighter than the ground around them.` |
| Sheet có nền hoặc món chạm ô | `Same sheet, but a fully transparent background and every object a little smaller, centred inside its own cell, not touching the cell edges; no grid lines, no numbers.` |
| Có chữ, số, sinh vật | `Same image without any text, numbers, creatures or people.` |
| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it in the rendering of image 1: pencil hatching on cream paper, wobbly ink outlines, chunky doodles with clear silhouettes. Keep the same layout.` |
"""


# ---------- soi, duyệt ----------

def tall_of(im):
    """bản cao vào game: y CUT..CH phóng về 1080 x 1528 (600 trời dư + khung 928)"""
    return im.convert("RGB").resize((CW, CH)).crop((0, CUT, CW, CH)).resize((FW, FH + EXTRA), Image.LANCZOS)


def soi(a, im):
    """vẽ lại khung game lên ảnh đã duyệt: bảng máu, mép 9:16 và các máy dài, chỗ bệ theo code, chân tướng, thân tướng"""
    im = im.convert("RGBA").resize((CW, CH))
    overlay_frame(im)
    d = ImageDraw.Draw(im)
    for e, _ in SHOWS:
        dashed_hline(d, round(TOP - e * S), (255, 220, 0), 3, 24)
    (cx, cy, w, h, _), _ = platforms(a)
    for (x, y, ww, hh) in ((cx, cy, w, h), ME_PLAT[:4]):
        d.ellipse((x - ww / 2, y - hh / 2, x + ww / 2, y + hh / 2), outline=(255, 0, 255), width=4)
    for p in (FOE, ME):
        d.line([(p[0] - 14, p[1]), (p[0] + 14, p[1])], fill=(255, 0, 255), width=4)
        d.line([(p[0], p[1] - 14), (p[0], p[1] + 14)], fill=(255, 0, 255), width=4)
    dashed_rect(d, FOE_BOX, (255, 255, 255), 3, 18)
    dashed_rect(d, ME_BOX, (255, 255, 255), 3, 18)
    return im.convert("RGB")


def approve(i, src):
    a = BY_ID.get(i)
    if not a:
        sys.exit(f"không có mã {i}; các mã: {', '.join(BY_ID)}")
    if src is None:
        found = sorted(INBOX.glob(f"{i}*.png"), key=lambda p: p.stat().st_mtime)
        found = [p for p in found if p.stem == i or p.stem.startswith(i + "_")]
        if not found:
            sys.exit(f"chưa có ảnh {INBOX / (i + '.png')}")
        src = found[-1]
    src = Path(src)
    sz = size_of(src)
    want = (1536, 1024) if a["kind"] == "fx" else (CW, CH)
    if sz != want:
        print(f"  ! {src.name} cỡ {sz}, cần {want[0]} x {want[1]}")
    WORK.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, approved(i))
    print(f"Duyệt {i}: {src} -> {approved(i)}")
    if a["kind"] != "fx":
        with Image.open(src) as im:
            soi(a, im).save(WORK / f"soi_{i}.png")
            tall_of(im).save(WORK / f"cao_{i}.png")
        print(f"  ảnh soi: {WORK / f'soi_{i}.png'}; bản cao: {WORK / f'cao_{i}.png'}")


# ---------- xuất vào game ----------
# Nền: bản cao 1080 x 1528 (moc/cao_<mã>.png, --duyet ghi) lưu Assets/03 Art/BattleBG/battle_moc_<khoá>.png cho 8 ảnh (khoá chính
# trong ART_KEY). Khoá dùng chung (USES) không có ảnh: arena_fx.json ghi "use" (khoá có ảnh), "tint" (màu phủ ảnh nền), phần động
# riêng; StageView mượn ảnh theo "use". Sheet fx cắt thành BattleBG/Anim/san_<tên> (lọc quầng trắng GPT để lại quanh mỗi món).
# arena_fx.json chỉ thay các khoá moc_*, giữ khoá đảo khác.
ASSETS = ART.parent / "Assets"
OUT = ASSETS / "03 Art" / "BattleBG"
OUT_FX = OUT / "Anim"
OUT_JSON = OUT / "Resources" / "arena_fx.json"
ART_KEY = {"c12": "moc_c01", "c34": "moc_c03", "c05": "moc_c05", "c06": "moc_c06", "c07": "moc_c07", "c08": "moc_c08",
           "c09": "moc_c09", "b70": "moc_s70"}


def fx(k, x, y, s, **kw):
    return dict(k=k, x=x, y=y, s=s, **kw)


# phần động, toạ độ ảnh GPT 1024 x 1536 (khung sân là y 656..1536; món ở trên y 656 chỉ máy dài thấy). Món như ArenaAnim.cs; "img"
# đổi ảnh: san_petal, san_bamboo (lá), san_seed (đốm bay), san_sunbeam (quầng), san_leafrune (phù văn), san_whirlwind (vòi lốc),
# anim_wind (sóng trôi)
_c01 = [fx("leaf", 930, 900, 34, n=3, img="san_petal"), fx("sparkle", 940, 940, 40, w=150, h=120, n=2),
        fx("wave", 320, 975, 90, w=420, h=10, n=2), fx("wisp", 520, 900, 38, w=700, h=200, n=2, img="san_seed")]
_c03 = [fx("leaf", 200, 720, 44, n=3), fx("leaf", 560, 700, 40, n=2), fx("glow", 430, 820, 360, img="san_sunbeam")]
_c05 = [fx("wave", 660, 820, 110, w=600, h=200, n=3, img="anim_wind"), fx("leaf", 520, 760, 34, n=2)]
_c06 = [fx("leaf", 150, 700, 44, n=2), fx("leaf", 900, 680, 44, n=2), fx("ripple", 300, 1010, 90, w=400, h=30, n=2),
        fx("glow", 560, 820, 360, img="san_sunbeam"), fx("wisp", 520, 900, 36, w=600, h=200, n=2, img="san_seed")]
_c07 = [fx("mist", 730, 985, 260, w=560, h=30, n=3)]
_c08 = [fx("leaf", 160, 720, 50, n=3, img="san_bamboo"), fx("glow", 54, 955, 70, c="#ffcf80"), fx("glow", 216, 955, 70, c="#ffcf80"),
        fx("firefly", 600, 900, 40, w=600, h=200, n=3)]
_c09 = [fx("glow", 90, 950, 220, c="#8dffb5"), fx("glow", 950, 990, 180, c="#8dffb5"),
        fx("sparkle", 90, 930, 40, w=160, h=200, n=2), fx("sparkle", 950, 980, 36, w=120, h=160, n=2),
        fx("sparkle", 720, 420, 36, w=300, h=200, n=2), fx("firefly", 650, 900, 34, w=500, h=200, n=3)]
_s70 = [fx("rune", 300, 1110, 360, img="san_leafrune"), fx("glow", 126, 930, 160, c="#ffd27a"),
        fx("wisp", 126, 920, 44, w=120, h=60, n=3), fx("leaf", 400, 640, 44, n=3), fx("leaf", 800, 600, 44, n=2)]
FX = {
    "moc_c01": _c01, "moc_c02": _c01, "moc_c03": _c03, "moc_c04": _c03,
    "moc_c05": _c05,
    "moc_s20": [fx("wave", 660, 820, 120, w=700, h=240, n=5, img="anim_wind"), fx("leaf", 520, 760, 36, n=4),
                fx("spout", 150, 1010, 130, w=40, h=10, n=1, img="san_whirlwind")],
    "moc_c06": _c06,
    "moc_s30": _c06[:2] + [fx("leaf", 500, 700, 44, n=3), fx("spout", 480, 995, 170, w=60, h=10, n=1, img="san_whirlwind")] + _c06[2:],
    "moc_c07": _c07,
    "moc_s40": [fx("glow", 110, 760, 260, c="#7dffb0"), fx("mist", 730, 985, 280, w=600, h=40, n=4)],
    "moc_c08": _c08,
    "moc_s50": _c08[:3] + [fx("leaf", 600, 700, 46, n=3, img="san_bamboo"), fx("firefly", 600, 900, 40, w=800, h=260, n=6)],
    "moc_c09": _c09,
    "moc_s60": _c09 + [fx("wisp", 500, 1000, 50, w=800, h=200, n=4)],
    "moc_s70": _s70,
    "moc_s70_2": _s70 + [fx("cloud", 512, 700, 380, w=1000, h=120, n=3), fx("rain", 512, 1096, 46, n=40)],
    "moc_s70_3": _s70 + [fx("cloud", 512, 690, 420, w=1000, h=140, n=4), fx("bolt", 600, 660, 210, w=700, h=20),
                         fx("rain", 512, 1096, 56, n=54)],
}
FX_NAMES = ["whirlwind", "petal", "bamboo", "sunbeam", "leafrune", "seed"]  # sheet fx 3 x 2
SEED_PUFF = (270, 168, 130, 92)  # cụm tơ bồ công anh trong ô 6 (tâm, bán trục; px ô): giữ nguyên độ trong, quầng dính liền tơ


def to_frame(item):
    """toạ độ ảnh GPT -> 0..1 theo khung sân (x theo bề ngang, y từ mép trên khung; cỡ theo bề ngang khung)"""
    fh = CH - TOP
    out = dict(item)
    out["x"] = round(item["x"] / CW, 4)
    out["y"] = round((item["y"] - TOP) / fh, 4)
    for k in ("s", "w"):
        if k in item:
            out[k] = round(item[k] / CW, 4)
    if "h" in item:
        out["h"] = round(item["h"] / fh, 4)
    return out


def sky_of(im, tint=None):
    """màu trời phủ phần dôi trên đầu máy dài: trung bình 6 hàng trên cùng của bản cao (nhân màu phủ nếu có)"""
    px = im.crop((0, 0, FW, 6)).resize((1, 1), Image.BOX).getpixel((0, 0))[:3]
    if tint:
        t = [int(tint[i:i + 2], 16) for i in (1, 3, 5)]
        px = tuple(round(a * b / 255) for a, b in zip(px, t))
    return "#%02x%02x%02x" % px


def clean_cell(cell, name):
    """bỏ quầng trắng mờ quanh món (GPT 'nền trong suốt'): giữ nét mực và vùng có màu, lấp lòng món (trừ vòng phù văn), cụm tơ bồ
    công anh giữ nguyên"""
    import numpy as np
    from PIL import ImageFilter
    a = np.array(cell.convert("RGBA")).astype(int)
    A, rgb = a[..., 3], a[..., :3]
    mx, sat = rgb.max(2), rgb.max(2) - rgb.min(2)
    core = (A > 40) & ((mx < 175) | (sat > 26))
    m = Image.fromarray((core * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))
    if name != "leafrune":
        w, h = m.size
        for p in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)):
            if m.getpixel(p) == 0:
                ImageDraw.floodfill(m, p, 128)
        m = Image.fromarray(np.where(np.array(m) == 128, 0, 255).astype("uint8"))
    keep = np.array(m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))) / 255.0
    if name == "seed":
        cx, cy, rx, ry = SEED_PUFF
        yy, xx = np.mgrid[:a.shape[0], :a.shape[1]]
        keep = np.maximum(keep, (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1).astype(float))
    a[..., 3] = (A * keep).round().astype(int)
    return Image.fromarray(a.astype("uint8"), "RGBA")


def cut_fx(out_fx):
    out_fx.mkdir(parents=True, exist_ok=True)
    with Image.open(approved("fx")) as im:
        im = im.convert("RGBA")
        cw, ch = im.width // 3, im.height // 2
        for k, name in enumerate(FX_NAMES):
            cell = clean_cell(im.crop(((k % 3) * cw, (k // 3) * ch, (k % 3 + 1) * cw, (k // 3 + 1) * ch)), name)
            box = cell.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
            if not box:
                print(f"  ! fx ô {k + 1} trống")
                continue
            box = (max(0, box[0] - 4), max(0, box[1] - 4), min(cw, box[2] + 4), min(ch, box[3] + 4))
            cell.crop(box).save(out_fx / f"san_{name}.png")
    print(f"  fx: {len(FX_NAMES)} ảnh -> {out_fx}")


def export(out=OUT, out_fx=OUT_FX, out_json=OUT_JSON):
    out.mkdir(parents=True, exist_ok=True)
    data = {}
    imgs = {}
    for i, key in ART_KEY.items():
        src = WORK / f"cao_{i}.png"
        if not src.exists():
            print(f"  ! chưa có {src} (duyệt {i} trước)")
            continue
        with Image.open(src) as im:
            imgs[key] = im.convert("RGB")
        imgs[key].save(out / f"battle_{key}.png")
        print(f"  {i} -> battle_{key}.png ({imgs[key].width} x {imgs[key].height})")
    for key, (img, tint, _) in USES.items():
        base = ART_KEY[img]
        if base not in imgs:
            continue
        e = {"sky": sky_of(imgs[base], tint)}
        if key != base:
            e["use"] = base
        if tint:
            e["tint"] = tint
        e["fx"] = [to_frame(f) for f in FX.get(key, [])]
        data[key] = e
    if approved("fx").exists():
        cut_fx(out_fx)
    old = json.loads(out_json.read_text(encoding="utf-8")) if out_json.exists() else {}
    arenas = {k: v for k, v in old.get("arenas", {}).items() if not k.startswith("moc_")}
    arenas.update(data)
    note = old.get("note", "toạ độ 0..1 theo khung sân 1080 x 928, y từ trên; cỡ theo bề ngang khung")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({"note": note, "arenas": arenas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Xuất {len(imgs)} nền, {len(data)} khoá moc_* (giữ {len(arenas) - len(data)} khoá đảo khác) vào {out_json}")


def build():
    PACK.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    make_refs()
    for f in PACK.glob("*.txt"):
        f.unlink()
    for a in ARENAS:
        if a["kind"] != "fx":
            draw_sketch(a).save(PACK / f"bo_cuc_{a['id']}.png")
    built = []
    for n, a in enumerate(ARENAS, 1):
        if not ready(a):
            continue
        for p, _, _ in ref_list(a):
            if not p.exists():
                print(f"  ! lượt {n} ({a['id']}) thiếu ảnh mẫu {p}")
        name = f"{n:02d}_{a['id']}.txt"
        (PACK / name).write_text(prompt(a), encoding="utf-8")
        built.append(name)
    (PACK / "HUONG_DAN.md").write_text(guide(), encoding="utf-8")
    print(f"Gói {PACK}: {len(built)} file prompt ({', '.join(built) or 'chưa có'}); {len(ARENAS) - len(built)} lượt chờ ảnh duyệt")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar=("MA", "ANH"), help="duyệt ảnh GPT của lượt <mã> (mặc định ảnh mới nhất)")
    ap.add_argument("--xuat", nargs="?", const="", metavar="THU_MUC",
                    help="xuất 8 nền, sheet phần động và khoá moc_* của arena_fx.json vào Assets (hoặc vào THU_MUC để thử)")
    args = ap.parse_args()
    if args.duyet:
        approve(args.duyet[0], args.duyet[1] if len(args.duyet) > 1 else None)
    if args.xuat is not None:
        if args.xuat:
            d = Path(args.xuat)
            j = d / "arena_fx.json"
            if OUT_JSON.exists() and not j.exists():
                j.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(OUT_JSON, j)
            export(d, d / "Anim", j)
        else:
            export()
    else:
        build()
