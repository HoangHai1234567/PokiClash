# Sàn đấu đảo Kim 70 ải: dựng bố cục và gói gửi GPT (ArtGen/BattleBG/PROMPTS.md, mục "Đảo Kim, Thổ 70 ải"). Sinh từ build_hoa.py
# (cùng khuôn, cùng số đo khung), chỉ khác dữ liệu nền, ảnh mẫu và chữ (người dùng 2026-11-27: "làm đi", bộ sàn đấu vẽ tay cho đảo
# Kim, Thổ như đảo Mộc, Hỏa; trước đó mọi trận đảo Kim dùng ảnh thay thế vẽ bằng code).
# Tiết kiệm dung lượng như đảo Mộc, Hỏa: 8 nền thay cho 17 nền của đảo Thủy, game dùng lại nền:
# - 2 nền thường, mỗi nền cho hai chặng đầu liền nhau (Cảng Sắt + Cầu Bánh Răng: ải 1–9; Rừng Lưỡi Liềm + Tháp Canh Thép: 10–19);
# - 5 nền chặng có mini boss (Gác Chuông Đồng … Tổ Cánh Pha Lê): mini boss ải 20–60 và các ải thường sau nó cùng một nền; ải mini boss
#   thêm phần động mạnh hơn và phủ màu nhẹ (game);
# - 1 nền boss ải 70 (Tháp Thiên Chung); dạng 2, 3 của Nhật Vương là nền đó phủ màu tối lạnh dần, thêm mây bão, sét (game);
# - 1 sheet phần động 3 x 2 cho những món chưa có (bông tuyết, lá lưỡi liềm, vòng phù văn thép, vòng sóng chuông, dải cực quang, lông
#   vũ thép); bánh răng, chuông, khói, tia lửa, lấp lánh, quầng sáng, sương, tia nắng, mây bão, sét dùng lại ảnh có sẵn.
# Độc đáo: mỗi nền một giờ, một thời tiết, một bảng màu riêng (sáng trong, chiều lộng gió, bình minh sương, chiều vàng, sáng u ám
# sương thấp, hoàng hôn rực, đêm tuyết cực quang, bình minh vàng trên biển mây), địa danh lấy từ bản đồ dài đảo Kim đã duyệt.
# Tướng Kim phần lớn xám sẫm, bạc, điểm đỏ: nền sáng (đất xám xanh nhạt, kem), không mảng xám sẫm giữa sân, mặt bệ kem sáng.
# Khổ: GPT vẽ dọc 1024 x 1536 một lượt (như build_moc.py). Ghi: gui_gpt/kim/ (<nn>_<mã>.txt, bo_cuc_<mã>.png, HUONG_DAN.md),
# refs/kim/ (địa danh cắt từ bản đồ dài đảo Kim đã duyệt).
# Chạy: py -3 -I ArtGen/BattleBG/build_kim.py
# Duyệt ảnh GPT đã lưu: --duyet <mã> [ảnh] (mặc định ảnh mới nhất kim/tai_ve/<mã>*.png): lưu kim/<mã>.png, ảnh soi khung
# kim/soi_<mã>.png và bản cao kim/cao_<mã>.png (1080 x 1528), rồi dựng lại gói. Lượt cần ảnh chưa duyệt thì chưa có file prompt.
# Xuất vào game: --xuat [thư_mục_thử] (8 nền, sheet fx, khoá kim_* của arena_fx.json); phần động từng nền (FX) điền sau khi duyệt.
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
Z = "kim"  # khoá đảo: thư mục, tiền tố khoá arena_fx.json
ISLAND = "the Metal island, an island of steel mountains, iron harbours and bronze bells"
ISLAND_VI = "đảo Kim"
PACK = HERE / "gui_gpt" / Z
WORK = HERE / Z  # <mã>.png: bản duyệt; soi_<mã>.png: ảnh soi khung; cao_<mã>.png: bản cao 1080 x 1528
INBOX = WORK / "tai_ve"  # ảnh GPT lưu
REFS = HERE / "refs" / Z
STYLE = HERE / "moc" / "c12.png"  # nền trận Bờ Rêu + Đồng Hoa Sáng đảo Mộc đã duyệt (1024 x 1536)
STYLE_VI = ("nền trận Bờ Rêu + Đồng Hoa Sáng đảo Mộc đã duyệt (1024 × 1536, nền đặc): bờ biển rêu, đồi cỏ, hai gò rêu làm bệ, trời "
            "xanh gạch chì có mây nhỏ ở phần trên; lấy nét, góc nhìn, cỡ và kiểu bệ")
MAP1 = ART / "Islands" / "zones" / "kim70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Kim đã duyệt: màu, dáng đồ vật
MAP1_EN = ("part 1 of the new map of this Metal island, seen from above: copy its colours and the look of its objects (pale "
           "blue-grey hatched ground, grey rocks, silver-trunked trees with steel-blue leaf crowns, the riveted iron dock crane, "
           "crates and barrels, the iron bridge with bronze gears, the blue river); ignore its layout and its top-down view")
MAP1_VI = ("đoạn 1 bản đồ dài đảo Kim đã duyệt (1024 × 1536, nền đặc, nhìn từ trên): đất xám xanh nhạt gạch chì, đá xám, cây thân bạc "
           "tán xanh thép, cần cẩu sắt, thùng, cầu sắt bánh răng đồng, sông xanh; lấy màu và dáng đồ vật")
MAP_JSON = ART / "guides" / "zone70_kim.json"  # build_zone70_kim.py: chỗ địa danh trên bản đồ dài
MAP_WORK = ART / "Islands" / "zones" / "kim70"  # doan_k.png: đoạn bản đồ dài đã duyệt
DAIS = ART.parent / "Assets" / "03 Art" / "Islands" / "be_kim_boss.png"
DAIS_VI = "bệ boss của bản đồ đảo Kim (nền trong suốt): đĩa đá có mặt bên, vòng trên mặt; lấy ý bệ nổi"
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
COL = {"sky": (200, 230, 248), "sea": (70, 150, 220), "water": (120, 180, 214), "ground": (206, 214, 224),
       "tree": (110, 150, 186), "trunk": (176, 176, 186), "rock": (122, 120, 128), "stone": (214, 204, 182),
       "steel": (86, 94, 112), "bronze": (196, 136, 62), "roof": (74, 84, 116), "snow": (244, 246, 252),
       "cloud": (238, 228, 236), "lava": (245, 150, 40), "mark": (222, 222, 222)}
LEGEND = {"sky": "pale blue = sky", "sea": "blue = sea", "water": "light blue = river or pond water (a flat surface)",
          "ground": "pale blue-grey = gravel ground, pebbles or far hills", "tree": "steel blue = leaf crowns, bushes or a far grove",
          "trunk": "light grey = silver tree trunks, wooden posts and beams", "rock": "dark grey = rocks, ridges, cliffs or mountains",
          "stone": "beige = flagstones, stone walls or a smooth stone floor", "steel": "dark blue-grey = riveted steel structures",
          "bronze": "bronze = bronze bells, gears and roofs", "roof": "slate blue = slate roofs and tower cones",
          "snow": "white = snow", "cloud": "pale pink-white = a sea of clouds below the peak",
          "lava": "orange = molten bronze (a flat surface)", "mark": "light grey with an ink edge = the landmark"}
LEGEND_VI = {"sky": "xanh nhạt là trời", "sea": "xanh là biển", "water": "xanh nhạt là nước sông, hồ (mặt phẳng)",
             "ground": "xám xanh nhạt là nền sỏi, đồi xa", "tree": "xanh thép là tán lá, bụi, rừng xa",
             "trunk": "xám nhạt là thân cây bạc, cột, xà gỗ", "rock": "xám sẫm là đá, gờ, vách, núi",
             "stone": "be là sân đá, tường đá, nền đá phẳng", "steel": "xám xanh sẫm là khung thép đinh tán",
             "bronze": "màu đồng là chuông, bánh răng, mái đồng", "roof": "xanh đá là mái đá, nón tháp", "snow": "trắng là tuyết",
             "cloud": "hồng trắng nhạt là biển mây dưới đỉnh", "lava": "cam là đồng nóng chảy (mặt phẳng)",
             "mark": "xám nhạt viền mực là địa danh"}

CONTRAST = ("The fighters of this island are mostly dark steel grey and silver with a few red details: keep the whole battle "
            "area light (pale blue-grey gravel, cream stone, soft greens, warm bronze accents), never a dark grey middle, and the two "
            "platform tops pale cream, so dark grey fighters stand out.")
CONTRAST_VI = "Tướng Kim phần lớn xám sẫm, bạc: file prompt dặn nền sáng (sỏi xám xanh nhạt, đá kem), mặt bệ kem sáng để tướng nổi."
C12_LOOK = ("Use the colours and the look of the objects of image 2 (pale blue-grey hatched ground, grey rocks, silver-trunked trees "
            "with steel-blue leaf crowns, riveted iron, warm bronze gears): a cool steel island, not a green forest.")
GUIDE_INTRO = """Nền trận cho 70 ải đảo Kim, cùng khuôn đảo Mộc, Hỏa: **tiết kiệm dung lượng, 8 nền thay cho 17 nền của đảo Thủy**, game dùng lại nền, nhưng mỗi nền một nơi, một giờ, một thời tiết riêng:
- **2 nền thường**, mỗi nền cho hai chặng đầu liền nhau: Cảng Sắt + Cầu Bánh Răng (ải 1–9, sáng trong), Rừng Lưỡi Liềm + Tháp Canh Thép (ải 10–19, chiều lộng gió).
- **5 nền chặng có mini boss**: Gác Chuông Đồng (bình minh sương), Xưởng Đúc Chuông (chiều vàng), Mỏ Sắt Ngân (sáng u ám sương thấp), Thành Ba Kiếm (hoàng hôn rực), Tổ Cánh Pha Lê (đêm tuyết, cực quang). Ải mini boss (20, 30, 40, 50, 60) và các ải thường sau nó dùng chung một nền; ải mini boss game phủ màu nhẹ và thêm phần động mạnh hơn.
- **1 nền boss ải 70** (Tháp Thiên Chung, bình minh vàng trên biển mây). Dạng 2, 3 của Nhật Vương không vẽ thêm: game phủ tối lạnh dần, thêm mây bão, tuyết, sét.
- **1 sheet phần động** 3 × 2, chỉ 6 món chưa có: bông tuyết, lá lưỡi liềm, vòng phù văn thép, vòng sóng chuông, dải cực quang, lông vũ thép. Bánh răng, chuông, khói, lấp lánh (ảnh phần động bản đồ đảo), tia lửa, quầng sáng, sương, tia nắng, mây bão, sét (ảnh sàn đấu các đảo khác) dùng lại."""
CHECK_VI = "Đảo thép sáng, mát (lượt 1 không lấy màu xanh lá của ảnh mẫu đảo Mộc), không mảng xám sẫm giữa sân (tướng xám sẽ chìm)."
WRONG_C12 = ("Same layout, but this is the cool steel Metal island: pale blue-grey gravel ground, grey rocks, riveted iron and bronze "
             "gears, silver-trunked trees with steel-blue leaves; no lush green grass.")


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
    dict(id="c12", kind="c", spots=[1, 2], place="the Iron Harbour and the Gear Bridge", stages="1–9",
         vi="Cảng Sắt + Cầu Bánh Răng", vi_stages="ải 1–9 (chặng 1, 2)",
         shapes=[below("sea", 975, 975),
                 poly("ground", (0, 1022), (300, 1032), (520, 1020), (640, 978), (780, 942), (1024, 912), (1024, CH), (0, CH)),
                 poly("water", (560, 1012), (700, 998), (860, 990), (1024, 982), (1024, 1006), (860, 1014), (700, 1022), (560, 1028)),
                 ell("mark", 0, 928, 182, 1066), ell("mark", 860, 880, 1024, 1068)],
         fx=[("rect", (560, 975, 860, 1030))],
         scene="where the steel island meets the sea, on a bright clear morning. The calm sea fills the far part on the left up to "
               "the horizon at y = 975, with small soft wave lines; a plain wobbly shoreline with a thin band of grey pebbles runs "
               "from about y = 1022 at the left edge to y = 1020 at x = 520, just behind the far platform. On the right the land "
               "rises into a gentle slope of pale blue-grey gravel with patches of short silvery-green grass, whose crest reaches "
               "about y = 912 at the right edge. A narrow calm river of clear blue water flows across the far slope from the right "
               "edge towards the middle (y about 982-1028) and runs into the sea at about x = 560, well behind the far platform. "
               "The near ground is pale blue-grey gravel with soft patches of silvery grass and small flat stones.",
         landmark="two landmarks of the island: at the far left on the shore (x 0-182, y 928-1066) a small iron harbour: a "
                  "riveted iron dock crane with a big hook, stacked metal crates, two barrels and a big iron anchor lying on the "
                  "pebbles (the Iron Harbour); at the right edge (x 860-1024, y 880-1068) the end of a flat bridge of riveted iron "
                  "plates over the river, with a big bronze gear wheel standing upright at its end (the Gear Bridge).",
         details="a coil of rope and a few grey pebbles on the shore, two iron posts with a short chain between them, tufts of "
                 "silvery grass, a few small bolts and nuts in the gravel over the right half of the ground.",
         top="the same bright pale-blue sky, hatched with diagonal pencil strokes like image 1, becoming only a little deeper blue "
             "towards the very top, with three or four small fluffy cream clouds with thin ink outlines, spread out.",
         plat="both are low round mounds of pale cream sand, clearly lighter than the gravel, ringed with small grey pebbles.",
         light="bright clear morning, light from the top-left.",
         effects=["small waves on the river (pink dashed box): keep the water flat and plain with a few calm wave lines"],
         leave="steam, smoke, sparks, sparkles, glows, foam on the shore (the game adds small waves on the river)",
         vi_desc="bờ biển sỏi xám lúc sáng trong: biển bên trái xa, dốc sỏi xám xanh có cỏ bạc bên phải, sông nhỏ chảy ra biển; "
                 "cảng sắt (cần cẩu, thùng, mỏ neo) bên trái xa, đầu cầu sắt có bánh răng đồng ở mép phải; bệ là gò cát kem"),
    dict(id="c34", kind="c", spots=[3, 4], place="the Sickle-Leaf Grove and the Steel Watchtower", stages="10–19",
         vi="Rừng Lưỡi Liềm + Tháp Canh Thép", vi_stages="ải 10–19 (chặng 3, 4)",
         shapes=[below("tree", 880, 898), below("ground", 1002, 1012),
                 poly("steel", (24, 1072), (64, 330), (136, 330), (176, 1072)), rect("steel", 34, 236, 166, 336),
                 poly("steel", (84, 236), (100, 130), (116, 236)),
                 ell("mark", 0, 900, 200, 1072), ell("tree", 862, 884, 1024, 1094)],
         fx=[("rect", (420, 300, 1000, 640))],
         scene="a clearing in a grove of strange trees on the steel island, on a clear, windy afternoon. A wall of round trees with "
               "silver-grey trunks and crowns of long curved leaves shaped like sickle blades (leaves, not weapons), steel blue and "
               "pale green, closes the back along the horizon (tree tops from about y = 880 at the left to y = 898 at the right); "
               "the near ground from about y = 1002 is pale blue-grey gravel with short silvery grass and a few fallen curved "
               "leaves. At the right edge, below y = 884, one smaller tree of the same kind with a round crown.",
         landmark="at the far left a tall watchtower of riveted steel girders (x 24-176) rises from the ground up into the top "
                  "part: a small lookout cabin with windows at about y 236-336 and a pointed spire like a lance tip up to about "
                  "y = 130; at its foot (x 0-200, y 900-1072) a few iron crates and a ladder (the Steel Watchtower); and the "
                  "sickle-leaf trees all around (the Sickle-Leaf Grove).",
         details="fallen curved leaves on the gravel, grey rocks with silvery moss, a short wooden fence far behind in the middle, "
                 "a small pennant on the spire (plain, no writing).",
         top="the top of the steel watchtower with its lookout cabin and spire at the left; the rest a clear, fresh sky, pale blue "
             "with long thin wind-swept cream clouds streaming to the right.",
         plat="both are flat round slabs of pale cream stone set in a thin riveted iron rim, clearly lighter than the gravel; the "
              "tops stay empty.",
         light="clear windy afternoon, crisp light from the left, cool and fresh.",
         effects=["curved leaves blowing through the air (pink dashed box): no leaves in the air"],
         leave="leaves in the air, smoke, sparks, glowing dots, glows",
         vi_desc="bãi trống trong rừng cây lá lưỡi liềm chiều lộng gió: tháp canh thép đinh tán có chòi và chóp mũi giáo bên trái xa "
                 "vươn lên phần trên, thùng sắt dưới chân; cây thân bạc tán xanh thép ở mép phải; bệ là phiến đá kem viền sắt"),
    dict(id="c05", kind="m", spots=[5], place="the Bronze Bell Pavilion", stages="20–29", boss_stage=20, boss="Quỷ Xích",
         vi="Gác Chuông Đồng", vi_stages="ải 20 (mini boss Quỷ Xích) và 21–29",
         shapes=[below("rock", 950, 930), below("stone", 1005, 1012),
                 poly("roof", (0, 706), (14, 640), (116, 560), (222, 640), (240, 706)), ell("mark", 10, 700, 230, 1040),
                 rect("mark", 880, 880, 1024, 1084)],
         fx=[("ell", (60, 740, 190, 900)), ("rect", (300, 905, 1000, 985))],
         scene="a quiet stone terrace on a hilltop of the steel island, at a misty dawn. Far steel-grey mountains with white snowy "
               "tips reach the horizon (y 950 at the left, 930 at the right), soft morning mist lying in the valleys in front of "
               "them; a low wall of grey stones runs along the far edge of the terrace; the near ground from about y = 1005 is a "
               "terrace of big flat pale flagstones.",
         landmark="an open bell pavilion, big and grand at the far left (x 10-230, y 700-1040): a curved dark slate roof (up to "
                  "about y = 560) on four thick wooden posts on a square stone base, and a big bronze bell hanging still inside "
                  "(the bell at about x 60-190, y 740-900); at the right edge (x 880-1024, y 880-1084) two stone lanterns and a "
                  "wooden rack with three smaller bronze bells.",
         details="small pine bonsai in stone pots, a wooden striker beam hanging beside the big bell, small stacked stone cairns, "
                 "pale pebbles in the flagstone joints.",
         top="the curved slate roof of the pavilion at the left; the rest a soft dawn sky, pale gold and pink low behind the "
             "mountains, pale blue higher, two or three thin long cream clouds.",
         plat_far="a low raised round platform of grey stone blocks with a bronze band and small bronze studs around its short side "
                  "face, its top pale stone.",
         plat_near="a round circle of flat pale flagstones.",
         light="misty dawn: pale gold and pink sky low, soft cool shadows, morning mist in the valleys; calm and fresh.",
         effects=["the big bell swings and rings with sound waves (pink dashed oval at the bell): draw the bell hanging still, no "
                  "sound lines", "mist drifting along the far valley (pink dashed box): keep only a soft plain mist band there"],
         leave="sound waves, sparkles, smoke, glowing dots, light halos",
         vi_desc="sân đá đỉnh đồi lúc bình minh sương: gác chuông mái đá cong, chuông đồng to bên trái xa; hai đèn đá, giá ba chuông "
                 "nhỏ ở mép phải; núi thép đỉnh tuyết, sương trong thung"),
    dict(id="c06", kind="m", spots=[6], place="the Bell Foundry", stages="30–39", boss_stage=30, boss="Sói Giáp",
         vi="Xưởng Đúc Chuông", vi_stages="ải 30 (mini boss Sói Giáp) và 31–39",
         shapes=[below("rock", 905, 915), below("stone", 990, 1000), ell("water", 0, 960, 300, 1052),
                 rect("rock", 70, 520, 122, 720), ell("mark", 0, 700, 196, 990), ell("lava", 150, 925, 236, 965),
                 poly("trunk", (560, 392), (1024, 342), (1024, 372), (560, 422)), ell("bronze", 760, 400, 860, 500),
                 rect("mark", 870, 860, 1024, 1090)],
         fx=[("ell", (0, 960, 300, 1052)), ("rect", (36, 360, 160, 520)), ("ell", (146, 915, 240, 972))],
         scene="the yard of a bell foundry on the steel island, on a warm golden late afternoon. The stone wall of the yard and far "
               "grey mountains close the back (y about 905-915); the near ground from about y = 990 is a yard of pale flagstones "
               "with a little bronze dust. A long wooden gantry beam crosses the top-right part (y about 342-422) with a finished "
               "bronze bell hanging from it by a chain (x 760-860, y 400-500), high above the yard.",
         landmark="at the far left a squat stone kiln with a short brick chimney (x 70-122 up to y = 520), its arched mouth dark "
                  "with a soft warm glow at the back (x 0-196, y 700-990); beside it on a rock an iron crucible full of molten "
                  "bronze (x 150-236, y 925-965: a flat orange and yellow surface, no glow); in front of them a round pond of "
                  "cooling water (x 0-300, y 960-1052) with a stone rim; at the right edge (x 870-1024, y 860-1090) two big bronze "
                  "bells on wooden stands.",
         details="stacked moulds of clay, a pile of firewood, iron tongs and a hammer on a workbench, small bronze ingots, a water "
                 "bucket.",
         top="the wooden gantry beam with the hanging bronze bell at the top-right, the chimney top at the left; the rest a warm "
             "golden sky, pale gold low and soft blue higher, two or three small cream clouds lit gold.",
         plat_far="a low raised round platform of pale stone with a bronze band around its short side face, cast with simple ring "
                  "patterns like a bell.",
         plat_near="a flat round slab of pale stone with a thin bronze ring.",
         light="warm golden late afternoon: gold light from the right, long soft shadows, warm orange light from the kiln mouth "
               "and the crucible; cosy and busy.",
         effects=["steam rising from the cooling pond (pink dashed oval): keep the water flat and plain, no steam",
                  "smoke from the chimney (pink dashed box above the chimney top): keep that sky plain, no smoke",
                  "the crucible's glow (pink dashed oval at the crucible): flat molten bronze, no halo"],
         leave="steam, smoke, sparks, flames, glowing dots, light halos",
         vi_desc="sân xưởng đúc chuông chiều vàng: lò đá có ống khói, nồi đồng nóng chảy bên trái xa, hồ nước làm nguội trước lò, "
                 "hai chuông đồng trên giá gỗ ở mép phải; xà gỗ treo chuông vắt góc trên phải"),
    dict(id="c07", kind="m", spots=[7], place="the Silver Iron Mine", stages="40–49", boss_stage=40, boss="Thần Cơ",
         vi="Mỏ Sắt Ngân", vi_stages="ải 40 (mini boss Thần Cơ) và 41–49",
         shapes=[below("rock", 950, 965), below("ground", 1008, 1020),
                 poly("rock", (0, 420), (150, 400), (300, 560), (350, 900), (332, 1046), (0, 1062)),
                 ell("mark", 10, 772, 186, 1036), rect("mark", 888, 880, 1024, 1086)],
         fx=[("ell", (10, 772, 186, 1036)), ("rect", (380, 880, 1000, 965))],
         scene="a mining yard on a rocky hillside of the steel island, on a cool overcast morning with low mist. Grey rocky ridges "
               "with dark pines reach the horizon (y 950 at the left, 965 at the right), a soft low mist along their foot; a big "
               "grey rock hill rises at the left from the ground up to about y = 400 (its right side ends at about x = 350). The "
               "near ground from about y = 1008 is packed pale grey earth with scattered small silver ore pebbles; a short rail "
               "track comes out of the mine and curves away to the left edge (never between the two platforms).",
         landmark="the mine entrance in the rock hill at the far left (x 10-186, y 772-1036): a dark opening framed with heavy "
                  "wooden beams, a lantern hanging on each side, a mine cart full of shiny silver ore on the rails in front; at the "
                  "right edge (x 888-1024, y 880-1086) a wooden hand winch with a rope, a stack of timber props and a lantern on a "
                  "post.",
         details="silver ore chunks, a pickaxe leaning on a rock, wooden crates, small pines on the hill, pale pebbles.",
         top="the top of the rock hill with a few small pines at the left; the rest a soft overcast sky, pale silver-blue, heavy "
             "soft cream-grey clouds, lighter towards the horizon.",
         plat_far="a low raised round platform of riveted iron plates with a short side face, its top pale grey stone.",
         plat_near="a flat round slab of pale stone with small silver ore chips on its rim.",
         light="cool overcast morning: soft silver light, low mist, warm lantern light at the mine mouth; calm and a little "
               "mysterious, but the floor and the platforms stay light.",
         effects=["the lanterns glow and the silver ore glints (pink dashed oval at the mine): draw the lanterns plain, no halo, "
                  "no sparkle stars", "mist drifting along the far ridges (pink dashed box): only a soft plain mist band"],
         leave="sparkles, glow halos, smoke, dust clouds, glowing dots",
         vi_desc="sân mỏ trên sườn đồi đá sáng u ám sương thấp: cửa mỏ khung gỗ, hai đèn treo, xe goòng quặng bạc trên ray bên trái "
                 "xa; tời gỗ, cột chống, đèn cột ở mép phải; nền đất xám nhạt"),
    dict(id="c08", kind="m", spots=[8], place="the Three-Sword Fortress", stages="50–59", boss_stage=50, boss="Vong Kỵ",
         vi="Thành Ba Kiếm", vi_stages="ải 50 (mini boss Vong Kỵ) và 51–59",
         shapes=[below("ground", 940, 955), below("stone", 1005, 1012),
                 rect("stone", 0, 720, 236, 1000), rect("stone", 6, 566, 80, 1000), rect("stone", 160, 606, 234, 1000),
                 poly("roof", (0, 566), (43, 470), (86, 566)), poly("roof", (154, 606), (197, 520), (240, 606)),
                 ell("mark", 0, 860, 190, 1080), rect("mark", 880, 880, 1024, 1090)],
         fx=[("rect", (300, 150, 1000, 600)), ("ell", (0, 860, 190, 1000))],
         scene="the courtyard in front of an old fortress of the steel island, at a heroic warm sunset. Far rolling hills catch the "
               "last light along the horizon (y 940-955); the near ground from about y = 1005 is a courtyard of big pale "
               "flagstones with grass in the joints.",
         landmark="at the far left a small fortress gate of grey stone blocks (x 0-236, y 720-1000) with a closed iron door and "
                  "two short round towers with pointed slate-blue cone roofs (up to about y = 470 and 520); in front of the gate "
                  "(x 0-190, y 860-1080) three giant swords stuck point-down in the ground at slightly different angles, with a "
                  "red, a blue and a golden hilt; at the right edge (x 880-1024, y 880-1090) a piece of stone wall with a rack of "
                  "round shields.",
         details="small plain pennants (no writing) on the towers, iron torch holders (unlit) on the wall, grass tufts in the "
                 "flagstone joints, a few fallen shields.",
         top="the two tower tops with their cone roofs and pennants at the left; the rest a heroic sunset sky, warm orange and gold "
             "low, pink and soft violet higher, long glowing cream clouds.",
         plat_far="a low raised round platform of grey stone blocks, a carved crossed-swords relief on its short side face, its "
                  "top pale stone.",
         plat_near="a flat round slab of pale stone with an inlaid red-and-gold ring.",
         light="heroic warm sunset: orange and gold sky, warm golden light from the right, long blue-violet shadows; brave and "
               "noble, still bright and friendly.",
         effects=["sunbeams breaking through the clouds (pink dashed box in the sky): plain sky and clouds, no light rays",
                  "glints on the sword hilts (pink dashed oval): plain hilts, no sparkle stars"],
         leave="light rays, sparkle stars, flames, smoke, glowing dots",
         vi_desc="sân trước thành cổ lúc hoàng hôn rực: cổng thành đá hai tháp nón đá xanh bên trái xa, ba thanh kiếm khổng lồ cắm "
                 "ngược trước cổng (chuôi đỏ, xanh, vàng); tường đá giá khiên ở mép phải"),
    dict(id="c09", kind="m", spots=[9], place="the Crystal-Wing Nest", stages="60–69", boss_stage=60, boss="Pháo Giáp",
         vi="Tổ Cánh Pha Lê", vi_stages="ải 60 (mini boss Pháo Giáp) và 61–69",
         shapes=[below("rock", 950, 930), below("snow", 1004, 1010),
                 poly("rock", (0, 560), (120, 520), (260, 640), (300, 900), (290, 1046), (0, 1062)),
                 ell("mark", 0, 760, 240, 1000), rect("mark", 888, 880, 1024, 1086)],
         fx=[("rect", (300, 150, 1000, 560)), ("ell", (0, 760, 240, 1000)), ("rect", (888, 880, 1024, 1086))],
         scene="a snowy ledge high in the steel mountains, on a clear cold night. Snowy mountain peaks reach the horizon (y 950 at "
               "the left, 930 at the right); a rocky outcrop rises at the left up to about y = 520. The near ground from about "
               "y = 1004 is smooth pale rock covered with soft snow, lit silver-blue by the night sky.",
         landmark="on top of the outcrop at the far left (x 0-240, y 760-1000) a big round nest woven of bent steel rods, long "
                  "pale-green crystal shards sticking out of its rim like feathers; the nest is empty; at the right edge (x 888-1024, "
                  "y 880-1086) a cluster of pale-green crystal shards in the snow and a giant fallen steel feather.",
         details="small crystal shards in the snow, grey rocks with snow caps, a few small snowy fir trees far behind.",
         top="the top of the rocky outcrop with snow at the left; the rest a deep blue starry night sky with soft green and teal "
             "aurora ribbons (drawn as calm flat bands, not glowing) and a few small clouds.",
         plat_far="a low raised round platform of grey rock with pale-green crystal shards around its rim and a short side face, "
                  "its top covered in pale snow.",
         plat_near="a flat round slab of smooth pale grey rock with a little snow on its rim.",
         light="clear cold night: deep blue sky, green-teal aurora, silver-blue moonlight on the snow; the snowy floor and the two "
               "platforms stay light.",
         effects=["the aurora ribbons wave and shimmer (pink dashed box in the sky): keep only faint flat bands, no glow",
                  "the crystals pulse with light (pink dashed oval and box): draw the crystals clear, no halo, no sparkle stars",
                  "snow falling: no snowflakes in the air"],
         leave="glow halos, sparkle stars, snowflakes in the air, glowing dots",
         vi_desc="gờ núi tuyết đêm trong: tổ đan bằng thanh thép, cắm mảnh pha lê lục như lông vũ trên mỏm đá bên trái xa; cụm pha lê "
                 "và chiếc lông vũ thép to ở mép phải; trời sao, cực quang xanh"),
    dict(id="b70", kind="b", spots=[10], place="the Heavenly Bell Tower", stages="70", boss="Nhật Vương",
         vi="Tháp Thiên Chung", vi_stages="ải 70 (boss Nhật Vương, 3 dạng)",
         shapes=[below("cloud", 975, 990), below("stone", 1022, 1036),
                 poly("rock", (0, 975), (0, 760), (220, 520), (380, 330), (440, 310), (584, 310), (644, 330), (800, 520),
                      (1024, 760), (1024, 975)),
                 poly("snow", (380, 330), (440, 310), (584, 310), (644, 330), (610, 390), (512, 366), (414, 390)),
                 rect("steel", 452, 168, 572, 320), poly("bronze", (430, 184), (512, 112), (594, 184)),
                 ell("bronze", 482, 200, 542, 262),
                 ell("mark", 20, 820, 186, 1000), rect("mark", 880, 870, 1024, 1070)],
         fx=[("ell", (118, 1062, 482, 1160)), ("rect", (430, 190, 594, 280)), ("rect", (600, 120, 1000, 480))],
         scene="the snowy summit of the great steel mountain at the top of the island, above a sea of clouds, at a grand golden "
               "sunrise. Behind the arena the peak rises and fills the top part: steel-grey rock with white snow on its top. On the "
               "peak stands a tall bell tower of stone and riveted steel with a curved bronze roof and a huge bronze bell hanging "
               "in its open top floor (x 452-572, y 112-320). Beyond the far edge of the summit a sea of soft pink-gold clouds "
               "reaches the horizon (y 975-990). The ground from about y = 1022 is old pale flagstones with snow in the joints.",
         landmark="two stone statues of great folded wings on carved pedestals, facing the arena: one at the far left (x 20-186, "
                  "y 820-1000), one at the right edge (x 880-1024, y 870-1070); and the bell tower on the snowy peak behind.",
         details="small snowy rocks along the arena edge, two unlit bronze braziers, bronze gears half sunk in the snow, plain "
                 "pennants without writing on poles far behind.",
         top="the snowy peak with the bell tower and its huge bronze bell at the top centre; behind the tower the rising sun as a "
             "big pale gold disc, a rose and gold sky with heavy soft clouds gathering at both sides.",
         plat_far="a grand raised round dais of carved pale stone banded with riveted steel: gear and wing carvings on its side "
                  "face, a gold ring inlaid in its pale stone top.",
         plat_near="a flat round slab of pale stone with a thin gold ring.",
         light="the climax of the island: a grand golden sunrise above a sea of clouds, rose and gold sky, warm golden rim light on "
               "the statues, the tower and the dais. Grand and dramatic, still cute, not horror. The game darkens this image for "
               "the boss's later forms and adds storm clouds and lightning, so keep it clear, rich and not too dark.",
         effects=["a steel rune circle that lights up on the dais top (pink dashed oval): keep the top plain stone with only the "
                  "gold ring", "the great bell rings with sound waves (pink dashed box at the bell): the bell hangs still, no sound "
                  "lines", "sunbeams through the clouds (pink dashed box in the sky): plain sky, no light rays",
                  "storm clouds and lightning in the later forms: no lightning"],
         leave="glowing runes, sound waves, light rays, sparkles, snowflakes in the air, lightning, glows",
         vi_desc="đỉnh núi thép tuyết trên biển mây lúc bình minh vàng: tháp chuông đá thép mái đồng, chuông đồng khổng lồ trên đỉnh, "
                 "mặt trời mọc sau tháp; hai tượng cánh xếp hai bên; bệ boss đá kem viền thép chạm bánh răng, vòng vàng"),
    dict(id="fx", kind="fx", vi="Sheet phần động đảo Kim", vi_stages="ải 1–70",
         items=["a snowflake: a small soft six-armed snowflake, white with a pale blue edge, thin ink outline",
                "a falling leaf shaped like a sickle blade: a long curved steel-blue leaf with a pale green middle vein and a short "
                "stem, thin ink outline",
                "a glowing steel rune circle seen at a low angle (a wide flat ellipse): a ring of gear teeth, small wing shapes "
                "and dots inside a double ring, pale glowing gold",
                "a bell's sound wave: three curved arcs nested side by side like a bracket ), getting bigger outward, pale gold, "
                "thin ink outline",
                "an aurora ribbon: a long soft wavy ribbon of pale green fading to teal at its ends, wider in the middle, no ink "
                "outline",
                "a falling steel feather: a long silver-grey feather with a pale blue edge and a thin dark quill, thin ink outline"],
         names=["snow", "bladeleaf", "steelrune", "bellwave", "aurora", "feather"],
         vi_desc="6 món: bông tuyết, lá lưỡi liềm rơi, vòng phù văn thép, vòng sóng chuông, dải cực quang, lông vũ thép rơi"),
]
BY_ID = {a["id"]: a for a in ARENAS}
KIND_VI = {"c": "thường", "m": "chặng có mini boss", "b": "boss", "fx": "phần động"}

# Game dùng nền thế nào: khoá nền game -> (ảnh duyệt, màu phủ hoặc None, phần động). Ải mini boss phủ màu nhẹ và thêm phần động mạnh
# hơn; boss dạng 2, 3 phủ tối lạnh dần, thêm mây bão, sét. Ảnh có sẵn dùng lại: Islands/Anim anim_gear_big, anim_gear_small,
# anim_bell, anim_smoke_big, anim_smoke_small, anim_sparkle, anim_wind; BattleBG/Anim san_glow, san_mist, san_wisp, san_sparks,
# san_sunbeam, san_cloud, san_bolt.
USES = {
    "kim_c01": ("c12", None, "sóng nhỏ trên sông, lấp lánh"),
    "kim_c02": ("c12", None, "như c01"),
    "kim_c03": ("c34", None, "lá lưỡi liềm bay theo gió"),
    "kim_c04": ("c34", None, "như c03"),
    "kim_c05": ("c05", None, "sóng chuông, sương thung"),
    "kim_s20": ("c05", "#e0dcec", "sóng chuông dày, sương dày"),
    "kim_c06": ("c06", None, "hơi nước hồ làm nguội, khói ống khói, quầng nồi đồng"),
    "kim_s30": ("c06", "#f0e2d4", "tia lửa ở nồi đồng, khói dày, hơi nước dày"),
    "kim_c07": ("c07", None, "quầng đèn mỏ, lấp lánh quặng, sương"),
    "kim_s40": ("c07", "#dcdfe6", "đèn bừng, lấp lánh dày, sương dày"),
    "kim_c08": ("c08", None, "tia nắng qua mây, lấp lánh chuôi kiếm"),
    "kim_s50": ("c08", "#f0dcd4", "tia nắng mạnh, lấp lánh dày"),
    "kim_c09": ("c09", None, "cực quang, quầng pha lê, tuyết rơi"),
    "kim_s60": ("c09", "#d8dcec", "cực quang dày, tuyết dày, pha lê bừng"),
    "kim_s70": ("b70", None, "vòng phù văn thép trên bệ, sóng chuông, tia nắng, lông vũ thép bay"),
    "kim_s70_2": ("b70", "#c4c8dc", "thêm mây bão trôi, tuyết rơi"),
    "kim_s70_3": ("b70", "#8c8cac", "thêm tuyết dày, sét kèm chớp màn"),
}


def approved(i):
    return WORK / f"{i}.png"


def needs(a):
    return [] if a["id"] == "c12" else ["c12"]


def ready(a):
    return all(approved(n).exists() for n in needs(a))


# ---------- ảnh mẫu ----------

def map_spots():
    """chỗ địa danh trên bản đồ dài (build_zone70_<đảo>.py): số -> (x, y) px bản đồ ghép"""
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


SLUG = {1: "cang_sat", 2: "cau_banh_rang", 3: "rung_luoi_liem", 4: "thap_canh_thep", 5: "gac_chuong_dong", 6: "xuong_duc_chuong",
        7: "mo_sat_ngan", 8: "thanh_ba_kiem", 9: "to_canh_pha_le", 10: "thap_thien_chung"}
SPOT_EN = {1: "the iron harbour with the dock crane, crates and the anchor", 2: "the iron bridge with the bronze gear wheels",
           3: "the trees with silver trunks and sickle-shaped steel-blue leaves", 4: "the steel watchtower",
           5: "the bell pavilion with the bronze bell", 6: "the bell foundry with the kiln, the crucible and the cooling pond",
           7: "the mine entrance with the cart of silver ore", 8: "the fortress gate with the three giant swords",
           9: "the nest of steel rods with the crystal shards", 10: "the bell tower on the snowy mountain and the wing statues"}
SPOT_VI = {1: "cảng sắt, cần cẩu, thùng, mỏ neo", 2: "cầu sắt bánh răng đồng", 3: "cây thân bạc lá lưỡi liềm", 4: "tháp canh thép",
           5: "gác chuông đồng", 6: "xưởng đúc chuông, hồ làm nguội", 7: "cửa mỏ, xe goòng quặng bạc", 8: "cổng thành, ba thanh kiếm",
           9: "tổ thanh thép cắm pha lê", 10: "tháp chuông trên núi tuyết, tượng cánh"}


# chỗ thật của địa danh trên bản đồ ghép đảo Kim (px; build_zone70_kim.py SPOTS_REAL, BRIDGE_REAL đo tay 2026-11-05)
SPOT_FIX = {1: (760, 4000), 2: (555, 3735), 3: (150, 3450), 4: (795, 3240), 5: (300, 3090), 6: (765, 2585), 7: (300, 2217),
            8: (712, 1820), 9: (683, 922), 10: (510, 210)}


def make_refs():
    """cắt địa danh khỏi đoạn bản đồ dài của đảo đã duyệt (512 x 512 quanh chỗ địa danh); đoạn chưa duyệt thì chưa có"""
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
                                  "ignore its content",
                 f"nền trận {BY_ID['c12']['vi']} đã duyệt (1024 × 1536, nền đặc): lấy nét"),
                (GRID, "the numbered 3 x 2 grid: one object per cell, in number order",
                 "lưới 3 × 2 đánh số (1536 × 1024, nền trắng, ô viền hồng, số hồng ở góc): mỗi ô một món")]
    out = []
    if a["id"] == "c12":
        out.append((STYLE, "an approved battle background of ANOTHER island of this game, in the same tall format: copy its "
                           "RENDERING, perspective, platform size and look, the calm open middle and the plain hatched sky with "
                           "small clouds in the top part; not its content or colours",
                    STYLE_VI))
        out.append((MAP1, MAP1_EN, MAP1_VI))
    else:
        copy = ("copy its rendering, colours, perspective, platform look and brightness; not its content" if k == "c" else
                "copy its rendering, perspective and platform look; not its content, colours or daylight (this place has its own "
                "light)")
        out.append((approved("c12"), f"the approved battle background of this island (a normal stage): {copy}",
                    f"nền trận {BY_ID['c12']['vi']} đã duyệt (1024 × 1536, nền đặc): lấy nét, góc nhìn, kiểu bệ, độ sáng"))
    crops = [n for n in a["spots"] if crop_of(n)]
    for n in crops:
        sz = size_of(crop_of(n)) or (512, 512)
        out.append((crop_of(n), f"a crop of this island's new map, seen from above, showing {SPOT_EN[n]}: draw the same landmark "
                                f"here, seen from the side, with its colours and shapes",
                    f"mảnh cắt bản đồ dài {ISLAND_VI} ({sz[0]} × {sz[1]}, nhìn từ trên xuống): {SPOT_VI[n]}"))
    if a["id"] != "c12" and not crops:
        out.append((MAP1, "part of the new map of this island: the look of its objects; ignore its layout",
                    f"đoạn 1 bản đồ dài {ISLAND_VI} (1024 × 1536): lấy dáng đồ vật"))
    if k in ("m", "b"):
        out.append((DAIS, "the island map's boss plate: a raised round platform with a flat top, a visible side face and a ring on "
                          "its top; copy only this idea for the far platform, in the material described below" +
                          (", lower and simpler" if k == "m" else ""),
                    DAIS_VI))
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
                    "silhouettes; the same perspective, the same platform size and look, the same calm open middle and plain "
                    "hatched sky. Ink about 6 px on near things and 3-4 px on far things. " + C12_LOOK + " Not 3D, not glossy, "
                    "no realistic rendering, no tiny noisy details.",
                "",
                "CONTRAST: the fighters must stand out, so the background is a little softer and lighter than the map, with "
                "the most detail and contrast on the landmarks and along the left and right edges; the middle stays simple. "
                + CONTRAST]
    return ["", "RENDERING: exactly as image 1 (the approved battle background of this island): the same ink, hatching, paper, "
                "perspective, platform size and look. Not 3D, not glossy, no tiny noisy details. The fighters must stand out: most "
                "detail and contrast on the landmark and along the left and right edges; the middle stays simple. " + CONTRAST]


def arena_prompt(a, refs):
    k = a["kind"]
    lines = head(refs) + save_block(a)
    if k == "c":
        what = (f"the battle background for the stages at {a['place']} (stages {a['stages']}) of {ISLAND}, "
                f"in a vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added "
                f"by the game) fight on it: the enemy on the smaller far platform at the upper left, the player's fighter on the "
                f"bigger near platform at the lower right.")
    elif k == "m":
        what = (f"the battle background for {a['place']} (stages {a['stages']}) of {ISLAND}, in a "
                f"vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added by the "
                f"game) fight on it: the enemy on the far raised platform at the upper left, the player's fighter on the bigger "
                f"near platform at the lower right.")
    else:
        what = (f"the battle background for the final boss stage at {a['place']} (stage 70) of {ISLAND}, "
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
              f"WHAT THIS IS: a sprite sheet of {len(a['items'])} separate effect objects for the battle backgrounds of "
              f"{ISLAND} of a vertical mobile game. The game cuts the sheet into {len(a['items'])} sprites and "
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
    return f"""# Gói gửi GPT: sàn đấu {ISLAND_VI} 70 ải (`{Z}`)

Sinh bằng `{Path(__file__).resolve()}`, đừng sửa tay (chạy lại script sẽ ghi đè). {GUIDE_INTRO}

{CONTRAST_VI}

**Khổ dọc, vẽ một lượt:** GPT vẽ 1024 × 1536. 880 px dưới (từ nét đứt trắng y {TOP}) là khung sân máy 9:16, phần trên là trời, vật cao dư cho máy dài. Game lấy y {CUT}..1536 phóng về 1080 × 1528.

Ước dung lượng (ASTC 6×6, 1080 × 1528 khoảng 0,7 MB mỗi nền): 8 nền khoảng 5,6 MB như đảo Mộc, Hỏa; sheet phần động thêm khoảng 0,2 MB.

**Cách gen:** 2026-11-27 Claude gen thẳng qua Magnific (GPT 2.6, 1k high, 95 credit/ảnh): tải ảnh mẫu theo đúng thứ tự trong file prompt, gửi phần chữ của file, tải ảnh về chỗ SAVE rồi duyệt. Gửi GPT tay vẫn được: **mỗi lượt chỉ gửi GPT đường dẫn file prompt** (file ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu và chỗ lưu). Lượt 1 chốt nét {ISLAND_VI}; các lượt sau chỉ cần lượt 1 đã duyệt.

Ảnh địa danh: bản đồ dài {ISLAND_VI} đã duyệt đủ 3 đoạn, nên mỗi lượt có ảnh cắt địa danh của nơi đó (`{REFS}`), để địa danh trên nền trận giống bản đồ.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
{chr(10).join(rows)}

Bản duyệt Claude lưu ở `{WORK}\\<mã>.png`, kèm ảnh soi khung `soi_<mã>.png` và bản cao vào game `cao_<mã>.png` (1080 × 1528).

## Game dùng nền thế nào

Như đảo Mộc, Hỏa: `StageView` mượn ảnh theo `use` và phủ `tint` (khoá trong `arena_fx.json`). Phần động từng nền đo trên ảnh đã duyệt khi xuất, chỉ dùng kiểu có sẵn của `ArenaAnim`.

| Khoá nền game | Ảnh | Màu phủ | Phần động |
|---|---|---|---|
{chr(10).join(use_rows)}

## Soi trước khi nhắn Claude

- Ảnh dọc 1024 × 1536. Hai bệ đúng chỗ như bố cục (bệ xa trên trái, bệ gần to dưới phải); mặt bệ **trống** và **sáng** hơn đất.
- Mọi thứ trận cần (hai bệ, địa danh, chân trời) nằm dưới nét đứt trắng; phần trên chỉ là trời và vật cao nối lên.
- Giữa hai bệ thoáng; ngay sau lưng hai tướng (khung trắng nét đứt) không có vật cao, chỗ sáng.
- Góc trên phải và dưới trái của khung sân (gạch chéo xám) chỉ có trời, đất: bảng máu che chỗ đó.
- {CHECK_VI}
- Chặng có mini boss, boss: rõ là nơi đặc biệt (giờ, thời tiết, địa danh to, bệ địch nổi có mặt bên) mà vẫn đủ sáng cho ải thường, dễ thương, không đáng sợ.
- **Không vẽ phần động** file đã dặn chừa (mục EFFECTS của từng file).
- Sheet: nền trong suốt, mỗi món gọn trong ô của mình, không viền lưới, không số.
- Không chữ, số, sinh vật, người, khung viền.

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Ra ảnh ngang hoặc vuông | `Redraw it as a vertical 1024 x 1536 image following the sketch: the battle area in the bottom 880 px, sky above.` |
| Bệ lệch chỗ hoặc sai cỡ | `Same image, but put the two platforms exactly where the sketch has them: same centre and size.` |
| Có đồ trên bệ, giữa hai bệ rối | `Same image, but keep both platform tops empty and the ground between the two platforms calm and simple.` |
| Vật cao, chỗ sáng sau lưng tướng | `Same image, but nothing tall or bright right behind the fighters' places (the white dashed boxes of the sketch).` |
| Vẽ đồ ở chỗ bảng máu | `Same image, but only plain sky or ground in the top-right and bottom-left areas the sketch crosses with grey lines.` |
| Lượt 1 ra màu đảo khác | `{WRONG_C12}` |
| Vẽ cả phần động | `Same image, but remove the [smoke / steam / sparks / sound waves / light rays / aurora glow / snowflakes / leaves in the air / glow / lightning]; leave that place plain as the file says.` |
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
# Như build_moc.py: bản cao 1080 x 1528 (<đảo>/cao_<mã>.png, --duyet ghi) lưu Assets/03 Art/BattleBG/battle_<đảo>_<khoá>.png cho 8 ảnh
# (ART_KEY); khoá dùng chung (USES) ghi "use", "tint", phần động vào arena_fx.json; sheet fx cắt thành BattleBG/Anim/san_<tên>.
# arena_fx.json chỉ thay các khoá <đảo>_*, giữ khoá đảo khác.
ASSETS = ART.parent / "Assets"
OUT = ASSETS / "03 Art" / "BattleBG"
OUT_FX = OUT / "Anim"
OUT_JSON = OUT / "Resources" / "arena_fx.json"
ART_KEY = {i: f"{Z}_{k}" for i, k in (("c12", "c01"), ("c34", "c03"), ("c05", "c05"), ("c06", "c06"), ("c07", "c07"),
                                       ("c08", "c08"), ("c09", "c09"), ("b70", "s70"))}


def fx(k, x, y, s, **kw):
    return dict(k=k, x=x, y=y, s=s, **kw)


# phần động từng khoá, toạ độ ảnh GPT 1024 x 1536 (khung sân là y 656..1536; món ở trên y 656 chỉ máy dài thấy), đo trên ảnh đã duyệt.
# Chỉ dùng kiểu có sẵn của ArenaAnim (wisp, leaf, glow, sparkle, wave, mist, rune, cloud, bolt, spout...).
# Đo trên ảnh đã duyệt 2026-11-27 (lưới 100 px). Chuông: "glow" với san_bellwave (vòng sóng chuông phập phồng cạnh chuông); cực
# quang: "glow" với san_aurora; tuyết, lá lưỡi liềm, lông vũ: "leaf"; tia nắng: "glow" với san_sunbeam (như đảo Mộc); hơi nước hồ làm
# nguội: "wisp" với san_mist; khói ống khói: "wisp" với ảnh khói bản đồ đảo; lửa lò: "glow" với anim_flame_a (như đảo Hỏa).
SMOKE, SMOKE_BIG, BELL = "anim_smoke_small", "anim_smoke_big", "san_bellwave"
LAMP = "#ffcf80"
_c01 = [fx("wave", 480, 985, 90, w=520, h=24, n=2), fx("sparkle", 650, 1000, 26, w=350, h=30, n=2)]
_c03 = [fx("leaf", 520, 700, 30, n=2, img="san_bladeleaf"), fx("leaf", 820, 640, 30, n=2, img="san_bladeleaf"),
        fx("leaf", 650, 900, 28, n=2, img="san_bladeleaf"), fx("wave", 520, 980, 80, w=600, h=20, n=2)]
_lamps05 = [fx("glow", 717, 885, 50, c=LAMP), fx("glow", 984, 870, 50, c=LAMP)]
_c05 = [fx("glow", 250, 820, 90, img=BELL), fx("mist", 650, 935, 260, w=600, h=30, n=3)] + _lamps05
_c06 = [fx("glow", 100, 920, 200, c="#ffb060"), fx("glow", 100, 935, 90, img="anim_flame_a"),
        fx("wisp", 75, 540, 50, w=20, h=8, n=2, img=SMOKE), fx("glow", 175, 915, 90, c="#ffcf60"),
        fx("wisp", 110, 1040, 60, w=200, h=20, n=3, img="san_mist"), fx("glow", 880, 545, 90, img=BELL)]
_c07 = [fx("glow", 78, 800, 60, c=LAMP), fx("glow", 350, 800, 60, c=LAMP), fx("glow", 942, 833, 55, c=LAMP),
        fx("sparkle", 250, 905, 30, w=90, h=30, n=2), fx("mist", 650, 860, 260, w=600, h=50, n=3)]
_c08 = [fx("glow", 620, 450, 420, img="san_sunbeam"), fx("sparkle", 160, 890, 32, w=200, h=30, n=2)]
_snow = [fx("leaf", x, y, 18, n=2, img="san_snow") for x, y in ((300, 700), (620, 660), (860, 720))]
_c09 = [fx("glow", 450, 380, 500, img="san_aurora"), fx("glow", 800, 480, 420, img="san_aurora"),
        fx("glow", 130, 760, 120, c="#b8ffb0"), fx("glow", 390, 770, 110, c="#b8ffb0"),
        fx("glow", 930, 950, 120, c="#b8ffb0")] + _snow
_s70 = [fx("rune", 300, 1108, 360, img="san_steelrune"), fx("glow", 590, 230, 110, img=BELL),
        fx("glow", 460, 360, 500, img="san_sunbeam"), fx("leaf", 200, 700, 30, n=2, img="san_feather"),
        fx("leaf", 820, 720, 30, n=2, img="san_feather")]
FX = {
    "kim_c01": _c01, "kim_c02": _c01, "kim_c03": _c03, "kim_c04": _c03,
    "kim_c05": _c05,
    "kim_s20": [fx("glow", 250, 820, 120, img=BELL), fx("glow", 130, 820, 160, c="#ffd27a"),
                fx("mist", 650, 935, 280, w=640, h=40, n=4)] + _lamps05,
    "kim_c06": _c06,
    "kim_s30": [fx("glow", 100, 920, 240, c="#ffb060"), fx("glow", 100, 930, 120, img="anim_flame_a"),
                fx("wisp", 175, 905, 30, w=60, h=20, n=3, img="san_sparks"),
                fx("wisp", 75, 535, 70, w=24, h=10, n=3, img=SMOKE_BIG),
                fx("wisp", 110, 1040, 60, w=220, h=20, n=4, img="san_mist"), fx("glow", 880, 545, 110, img=BELL)],
    "kim_c07": _c07,
    "kim_s40": [fx("glow", 78, 800, 80, c=LAMP), fx("glow", 350, 800, 80, c=LAMP), fx("glow", 942, 833, 70, c=LAMP),
                fx("sparkle", 250, 905, 32, w=100, h=40, n=3), fx("mist", 650, 860, 280, w=640, h=60, n=4)],
    "kim_c08": _c08,
    "kim_s50": [fx("glow", 620, 450, 480, img="san_sunbeam"), fx("glow", 860, 520, 360, img="san_sunbeam"),
                fx("sparkle", 160, 890, 34, w=200, h=40, n=3)],
    "kim_c09": _c09,
    "kim_s60": _c09 + [fx("leaf", x, y, 20, n=2, img="san_snow") for x, y in ((450, 850), (750, 900), (200, 950))]
               + [fx("sparkle", 260, 770, 30, w=300, h=60, n=2)],
    "kim_s70": _s70,
    "kim_s70_2": _s70 + [fx("cloud", 512, 150, 380, w=1000, h=120, n=3)] + _snow,
    "kim_s70_3": _s70 + [fx("cloud", 512, 140, 420, w=1000, h=140, n=4), fx("bolt", 420, 680, 220, w=500, h=20)] + _snow
                 + [fx("leaf", x, y, 20, n=2, img="san_snow") for x, y in ((450, 880), (750, 920), (150, 980))],
}
FX_NAMES = [a for a in BY_ID["fx"]["names"]]  # sheet fx 3 x 2


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
    """bỏ quầng trắng mờ quanh món (GPT 'nền trong suốt'): giữ nét mực và vùng có màu, lấp lòng món (trừ vòng phù văn)"""
    import numpy as np
    from PIL import ImageFilter
    a = np.array(cell.convert("RGBA")).astype(int)
    A, rgb = a[..., 3], a[..., :3]
    mx, sat = rgb.max(2), rgb.max(2) - rgb.min(2)
    core = (A > 40) & ((mx < 175) | (sat > 26))
    m = Image.fromarray((core * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))
    if name not in ("leafrune", "firerune", "steelrune", "earthrune"):
        w, h = m.size
        for p in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)):
            if m.getpixel(p) == 0:
                ImageDraw.floodfill(m, p, 128)
        m = Image.fromarray(np.where(np.array(m) == 128, 0, 255).astype("uint8"))
    keep = np.array(m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))) / 255.0
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
    arenas = {k: v for k, v in old.get("arenas", {}).items() if not k.startswith(Z + "_")}
    arenas.update(data)
    note = old.get("note", "toạ độ 0..1 theo khung sân 1080 x 928, y từ trên; cỡ theo bề ngang khung")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({"note": note, "arenas": arenas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Xuất {len(imgs)} nền, {len(data)} khoá {Z}_* (giữ {len(arenas) - len(data)} khoá đảo khác) vào {out_json}")


# ---------- lượt sửa ----------
# Ảnh đã duyệt tạm nhưng sai một chỗ: file sua_<mã>.txt bảo GPT sửa đúng chỗ đó trên chính ảnh của nó (ảnh mẫu: ảnh đó, ảnh soi khung,
# bố cục). GPT lưu <mã>_2.png cạnh ảnh cũ; --duyet <mã> lấy ảnh mới nhất. Sửa xong thì bỏ mã khỏi FIXES.
# FIXES: mã -> (câu sửa cho GPT, câu cho người dùng). 2026-11-27: c06 bệ xa vẽ thấp, lệch trái (chân tướng rơi vào mép sau bệ),
# b70 bệ boss vẽ cao ~60 px (chân boss rơi vào mặt bên), như c08, b70 đảo Hỏa.
FIXES = {}  # c06, b70 đã sửa (sua_c06.txt, sua_b70.txt qua Magnific) và duyệt 2026-11-27


def fix_refs(i):
    return [(approved(i), "the battle background you drew for this place: edit THIS image",
             f"nền {i} GPT đã vẽ (1024 × 1536): ảnh cần sửa"),
            (WORK / f"soi_{i}.png", "the same image with the game's frame drawn over it: the magenta ovals and crosses are where "
                                    "the game puts the platforms and the fighters' feet, white dashed boxes = the fighters' "
                                    "bodies, grey diagonal lines = covered by the game's panels; ignore the yellow lines",
             f"ảnh soi khung của {i} (1024 × 1536): vòng và dấu cộng tím là chỗ bệ, chân tướng trong game; khung trắng là thân tướng"),
            (PACK / f"bo_cuc_{i}.png", "the original layout sketch", f"bố cục {i} (1024 × 1536)")]


def fix_prompt(i, task):
    a = BY_ID[i]
    lines = head(fix_refs(i)) + save_block(a)
    lines += ["", f"WHAT THIS IS: a correction of image 1, the battle background for {a['place']} of {ISLAND} in a vertical "
                  f"mobile monster-battle game. Image 1 is approved except for the point below.",
              "", f"FIX: {task}",
              "", "KEEP: everything else exactly as in image 1: the same rendering, colours, light, sky, landmarks, details and the "
                  "look of both platforms; the same size 1024 x 1536. Do not add anything new. Do not draw the magenta, white, grey "
                  "or yellow marks of image 2.",
              "", f"Remember: save the image to {INBOX / (i + '.png')}"]
    return "\n".join(lines) + "\n"


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
    md = guide()
    fixes = [(i, t) for i, t in FIXES.items() if approved(i).exists() and (WORK / f"soi_{i}.png").exists()]
    if fixes:
        md += "\n## Lượt sửa (gửi trong cùng chat)\n\n| File prompt gửi GPT | Sửa gì | Ảnh mẫu GPT mở | GPT lưu ảnh vào |\n|---|---|---|---|\n"
        for i, (en, vi) in fixes:
            name = f"sua_{i}.txt"
            (PACK / name).write_text(fix_prompt(i, en), encoding="utf-8")
            built.append(name)
            refs = "; ".join(f"{k + 1} `{p}`: {d}" for k, (p, _, d) in enumerate(fix_refs(i)))
            md += f"| `{PACK / name}` | {vi} | {refs} | `{INBOX / (i + '_2.png')}` (GPT tự thêm `_2` vì đã có `{i}.png`) |\n"
    (PACK / "HUONG_DAN.md").write_text(md, encoding="utf-8")
    print(f"Gói {PACK}: {len(built)} file prompt ({', '.join(built) or 'chưa có'}); {sum(1 for a in ARENAS if not ready(a))} lượt chờ ảnh duyệt")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar=("MA", "ANH"), help="duyệt ảnh GPT của lượt <mã> (mặc định ảnh mới nhất)")
    ap.add_argument("--xuat", nargs="?", const="", metavar="THU_MUC",
                    help=f"xuất 8 nền, sheet phần động và khoá {Z}_* của arena_fx.json vào Assets (hoặc vào THU_MUC để thử)")
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
