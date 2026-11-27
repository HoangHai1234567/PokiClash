# Sàn đấu đảo Thổ 70 ải: dựng bố cục và gói gửi GPT (ArtGen/BattleBG/PROMPTS.md, mục "Đảo Kim, Thổ 70 ải"). Sinh từ build_kim.py
# (cùng khuôn với build_hoa.py, cùng số đo khung), chỉ khác dữ liệu nền, ảnh mẫu và chữ (người dùng 2026-11-27: "làm đi", bộ sàn đấu
# vẽ tay cho đảo Kim, Thổ như đảo Mộc, Hỏa; trước đó mọi trận đảo Thổ dùng ảnh thay thế vẽ bằng code).
# Tiết kiệm dung lượng như đảo Mộc, Hỏa: 8 nền thay cho 17 nền của đảo Thủy, game dùng lại nền:
# - 2 nền thường, mỗi nền cho hai chặng đầu liền nhau (Bãi Đá Cuội + Hang Lửng: ải 1–9; Đồi Ngọc Lục + Mỏ Pha Lê: 10–19);
# - 5 nền chặng có mini boss (Đền Phù Văn … Lò Gốm Đất Nung): mini boss ải 20–60 và các ải thường sau nó cùng một nền; ải mini boss
#   thêm phần động mạnh hơn và phủ màu nhẹ (game);
# - 1 nền boss ải 70 (Kim Tự Viện); dạng 2, 3 của Thổ Tinh là nền đó phủ màu tối bụi dần, thêm bão cát, sét (game);
# - 1 sheet phần động 3 x 2 cho những món chưa có (luồng cát bay, vòng phù văn đất, lá sồi thu, đá vụn rơi, bụi phồng, phù văn đá
#   bay); khói, lấp lánh, quầng sáng, sương, lá, gió, mây bão, sét dùng lại ảnh có sẵn.
# Độc đáo: mỗi nền một giờ, một thời tiết, một bảng màu riêng (sáng nắng, chiều vàng, sương sớm tím, chiều thu, trưa hè mây trắng,
# hoàng hôn hẻm núi, đêm trăng sao, chạng vạng bão cát), địa danh lấy từ bản đồ dài đảo Thổ đã duyệt.
# Tướng Thổ phần lớn nâu, vàng đất, cam: đất cát nhạt dịu (không vàng đất đậm), điểm xanh lá, trời xanh, mặt bệ sáng để tướng nổi.
# Khổ: GPT vẽ dọc 1024 x 1536 một lượt (như build_moc.py). Ghi: gui_gpt/tho/ (<nn>_<mã>.txt, bo_cuc_<mã>.png, HUONG_DAN.md),
# refs/tho/ (địa danh cắt từ bản đồ dài đảo Thổ đã duyệt).
# Chạy: py -3 -I ArtGen/BattleBG/build_tho.py
# Duyệt ảnh GPT đã lưu: --duyet <mã> [ảnh] (mặc định ảnh mới nhất tho/tai_ve/<mã>*.png): lưu tho/<mã>.png, ảnh soi khung
# tho/soi_<mã>.png và bản cao tho/cao_<mã>.png (1080 x 1528), rồi dựng lại gói. Lượt cần ảnh chưa duyệt thì chưa có file prompt.
# Xuất vào game: --xuat [thư_mục_thử] (8 nền, sheet fx, khoá tho_* của arena_fx.json); phần động từng nền (FX) điền sau khi duyệt.
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
Z = "tho"  # khoá đảo: thư mục, tiền tố khoá arena_fx.json
ISLAND = "the Earth island, a sunny island of golden sand, red rock mesas, farm terraces and an old pyramid temple"
ISLAND_VI = "đảo Thổ"
PACK = HERE / "gui_gpt" / Z
WORK = HERE / Z  # <mã>.png: bản duyệt; soi_<mã>.png: ảnh soi khung; cao_<mã>.png: bản cao 1080 x 1528
INBOX = WORK / "tai_ve"  # ảnh GPT lưu
REFS = HERE / "refs" / Z
STYLE = HERE / "hoa" / "c12.png"  # nền trận Bến Đá Đen + Suối Dung Nham đảo Hỏa đã duyệt (1024 x 1536)
STYLE_VI = ("nền trận Bến Đá Đen + Suối Dung Nham đảo Hỏa đã duyệt (1024 × 1536, nền đặc): bờ biển, dốc đất đỏ cam, hai gò cát tro "
            "làm bệ, trời xanh gạch chì có mây nhỏ ở phần trên; lấy nét, góc nhìn, cỡ và kiểu bệ")
MAP1 = ART / "Islands" / "zones" / "tho70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Thổ đã duyệt: màu, dáng đồ vật
MAP1_EN = ("part 1 of the new map of this Earth island, seen from above: copy the look of its objects (golden hatched earth, "
           "flat-topped red-brown rock mesas, acacia trees with flat olive-green crowns, round pebbles in grey, beige and rusty red, "
           "the stone cairn, the spiral seashell, the badger den mound, stone lanterns, haystacks); ignore its layout and its "
           "top-down view, and make the colours softer and lighter")
MAP1_VI = ("đoạn 1 bản đồ dài đảo Thổ đã duyệt (1024 × 1536, nền đặc, nhìn từ trên): đất vàng gạch chì, gò đá đỏ nâu đỉnh bằng, cây "
           "keo tán dẹt, đá cuội, ụ đá xếp, vỏ ốc, hang lửng, đèn đá, đụn rơm; lấy dáng đồ vật, màu dịu hơn")
MAP_JSON = ART / "guides" / "zone70_tho.json"  # build_zone70_tho.py: chỗ địa danh trên bản đồ dài
MAP_WORK = ART / "Islands" / "zones" / "tho70"  # doan_k.png: đoạn bản đồ dài đã duyệt
DAIS = ART.parent / "Assets" / "03 Art" / "Islands" / "be_tho_boss.png"
DAIS_VI = "bệ boss của bản đồ đảo Thổ (nền trong suốt): đĩa đất có mặt bên, vòng trên mặt; lấy ý bệ nổi"
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
COL = {"sky": (200, 230, 248), "sea": (70, 150, 220), "water": (110, 180, 220), "ground": (238, 218, 166),
       "grass": (176, 200, 128), "tree": (122, 150, 82), "trunk": (128, 94, 68), "rock": (186, 106, 74), "ochre": (216, 164, 86),
       "stone": (226, 214, 188), "brick": (182, 86, 64), "gold": (232, 182, 60), "field": (146, 194, 102),
       "mark": (222, 222, 222)}
LEGEND = {"sky": "pale blue = sky", "sea": "blue = sea", "water": "light blue = pond water (a flat surface)",
          "ground": "pale sand = sandy earth or far dunes", "grass": "sage green = grassy ground",
          "tree": "olive green = leaf crowns, bushes or a far grove", "trunk": "brown = tree trunks and roots",
          "rock": "red-brown = layered rock mesas, cliffs and canyon walls", "ochre": "ochre = ochre rock hills, far hills or the pyramid",
          "stone": "beige = flagstones, sandstone or a smooth stone floor", "brick": "brick red = red bricks, red pillars",
          "gold": "gold = golden roofs", "field": "green = farm terraces", "mark": "light grey with an ink edge = the landmark"}
LEGEND_VI = {"sky": "xanh nhạt là trời", "sea": "xanh là biển", "water": "xanh nhạt là nước hồ (mặt phẳng)",
             "ground": "cát nhạt là đất cát, đụn xa", "grass": "xanh xám là nền cỏ", "tree": "xanh ô liu là tán lá, bụi, rừng xa",
             "trunk": "nâu là thân, rễ cây", "rock": "đỏ nâu là gò đá phân lớp, vách, vách hẻm",
             "ochre": "vàng đất là đồi đá vàng, đồi xa, kim tự tháp", "stone": "be là sân đá, sa thạch, nền đá phẳng",
             "brick": "đỏ gạch là gạch đỏ, cột đỏ", "gold": "vàng là mái vàng", "field": "xanh lá là ruộng bậc thang",
             "mark": "xám nhạt viền mực là địa danh"}

CONTRAST = ("The fighters of this island are mostly tan, brown, ochre and orange: keep the earth a soft pale sand (light "
            "cream-yellow, never saturated ochre or orange), add sage-green grass, blue sky and grey stones as cool accents, keep the "
            "middle light, and the two platform tops pale (cream sand or pale grey stone), so brown and orange fighters stand out.")
CONTRAST_VI = ("Tướng Thổ phần lớn nâu, vàng đất, cam: file prompt dặn đất cát nhạt dịu (không vàng đất đậm), điểm xanh lá, trời xanh, "
               "mặt bệ sáng để tướng nổi.")
C12_LOOK = ("Use the look of the objects of image 2 (golden hatched earth, flat-topped red-brown mesas, acacia trees with flat "
            "olive crowns, round pebbles), but softer and lighter: a sunny earth island, not a green forest and not a red volcano.")
GUIDE_INTRO = """Nền trận cho 70 ải đảo Thổ, cùng khuôn đảo Mộc, Hỏa, Kim: **tiết kiệm dung lượng, 8 nền thay cho 17 nền của đảo Thủy**, game dùng lại nền, nhưng mỗi nền một nơi, một giờ, một thời tiết riêng:
- **2 nền thường**, mỗi nền cho hai chặng đầu liền nhau: Bãi Đá Cuội + Hang Lửng (ải 1–9, sáng nắng), Đồi Ngọc Lục + Mỏ Pha Lê (ải 10–19, chiều vàng).
- **5 nền chặng có mini boss**: Đền Phù Văn (sương sớm tím), Rừng Sồi Già (chiều thu), Ruộng Bậc Thang (trưa hè mây trắng), Vách Kim Cương (hoàng hôn hẻm núi), Lò Gốm Đất Nung (đêm trăng sao). Ải mini boss (20, 30, 40, 50, 60) và các ải thường sau nó dùng chung một nền; ải mini boss game phủ màu nhẹ và thêm phần động mạnh hơn.
- **1 nền boss ải 70** (Kim Tự Viện, chạng vạng vàng tím, bão cát kéo tới). Dạng 2, 3 của Thổ Tinh không vẽ thêm: game phủ tối bụi dần, thêm bão cát, sét.
- **1 sheet phần động** 3 × 2, chỉ 6 món chưa có: luồng cát bay, vòng phù văn đất, lá sồi thu, đá vụn rơi, bụi phồng, phù văn đá bay. Khói, lấp lánh, lá, gió (ảnh phần động bản đồ đảo), quầng sáng, sương, mây bão, sét (ảnh sàn đấu các đảo khác) dùng lại."""
CHECK_VI = ("Đảo đất cát vàng nhạt dịu, điểm xanh lá, trời xanh (lượt 1 không lấy màu đỏ cam của ảnh mẫu đảo Hỏa), không mảng vàng "
            "đất đậm giữa sân (tướng nâu vàng sẽ chìm).")
WRONG_C12 = ("Same layout, but this is the sunny Earth island: soft pale golden sand and earth, sage-green grass tufts, round "
             "pebbles, flat-topped red-brown mesas far away; not red volcanic earth, not lush green.")


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
    dict(id="c12", kind="c", spots=[1, 2], place="the Pebble Beach and the Badger Den", stages="1–9",
         vi="Bãi Đá Cuội + Hang Lửng", vi_stages="ải 1–9 (chặng 1, 2)",
         shapes=[below("sea", 975, 975), poly("rock", (690, 990), (722, 902), (880, 892), (912, 970)),
                 poly("ground", (0, 1022), (300, 1032), (520, 1020), (640, 978), (780, 942), (1024, 912), (1024, CH), (0, CH)),
                 ell("mark", 0, 928, 182, 1066), ell("mark", 860, 880, 1024, 1068)],
         fx=[("rect", (190, 975, 540, 1024))],
         scene="where the earth island meets the sea, on a bright sunny morning. The calm sea fills the far part on the left up to "
               "the horizon at y = 975, with small soft wave lines; a plain wobbly shoreline with a thin band of pale sand and round "
               "pebbles runs from about y = 1022 at the left edge to y = 1020 at x = 520, just behind the far platform. On the right "
               "the land rises into a gentle slope of pale golden sand and dry earth with tufts of sage-green grass, whose crest "
               "reaches about y = 912 at the right edge; behind the slope, far away on the right, a small flat-topped mesa of "
               "layered red-brown rock. The near ground is pale sandy earth with soft patches of short sage-green grass and small "
               "round pebbles.",
         landmark="two landmarks of the island: at the far left on the shore (x 0-182, y 928-1066) heaps of big smooth round "
                  "pebbles and boulders in grey, beige and rusty red, a tall cairn of balanced flat stones and a big spiral "
                  "seashell half-buried in the sand (the Pebble Beach); at the right edge (x 860-1024, y 880-1068) a low grassy "
                  "earth mound with a big round burrow entrance framed by thick roots and two wooden props, a heap of dug-out dirt, "
                  "a pickaxe and a shovel leaning on the mound; the den is empty (the Badger Den).",
         details="a bleached driftwood log on the beach, small shells along the shore, dry grass tufts, a few small gold nuggets "
                 "on the dirt near the den, round pebbles over the right half of the ground.",
         top="the same bright pale-blue sky, hatched with diagonal pencil strokes like image 1, becoming only a little deeper blue "
             "towards the very top, with three or four small fluffy cream clouds with thin ink outlines, spread out.",
         plat="both are low round mounds of pale cream sand, clearly lighter than the ground, ringed with small grey pebbles.",
         light="bright sunny morning, light from the top-left.",
         effects=["small waves along the shore (pink dashed box): keep the water plain with a few calm wave lines"],
         leave="dust clouds, sparkles, glows, foam on the shore (the game adds small waves)",
         vi_desc="bờ biển cát nhạt lúc sáng nắng: biển bên trái xa, dốc cát vàng nhạt cỏ xanh xám bên phải, gò đá đỏ nâu đỉnh bằng xa; "
                 "đống cuội, ụ đá xếp, vỏ ốc to bên trái xa, hang lửng (gò cỏ, cửa hang khung rễ, cuốc xẻng) ở mép phải; bệ là gò "
                 "cát kem"),
    dict(id="c34", kind="c", spots=[3, 4], place="the Emerald Hill and the Crystal Mine", stages="10–19",
         vi="Đồi Ngọc Lục + Mỏ Pha Lê", vi_stages="ải 10–19 (chặng 3, 4)",
         shapes=[below("ochre", 885, 900), below("ground", 1002, 1012),
                 poly("ochre", (0, 1066), (0, 560), (80, 500), (190, 520), (260, 640), (290, 860), (270, 1060)),
                 ell("mark", 10, 820, 200, 1050), ell("tree", 862, 884, 1024, 1094)],
         fx=[("rect", (20, 480, 260, 660)), ("ell", (10, 820, 200, 1050))],
         scene="a sunny valley of rolling ochre hills on the earth island, on a warm golden afternoon. Far rolling hills of pale "
               "ochre with a few flat-crowned acacia trees close the back along the horizon (from about y = 885 at the left to "
               "y = 900 at the right); the near ground from about y = 1002 is pale sandy earth with sage-green grass tufts and "
               "small coloured crystal pebbles. A big round hill of ochre rock rises at the left from the ground up to about "
               "y = 500 (its right side ends at about x = 290). At the right edge, below y = 884, a small acacia tree with a flat "
               "olive-green crown.",
         landmark="big clusters of emerald-green crystals stick out of the top and sides of the ochre hill at the left (the "
                  "Emerald Hill; flat colours, no shine); at its foot (x 10-200, y 820-1050) a crystal mine entrance framed with "
                  "heavy wooden beams, clusters of pink and lilac crystals around it, a wooden wheelbarrow full of pink crystals "
                  "and a big spiral drill bit lying on the ground (the Crystal Mine).",
         details="small pink and green crystal pebbles in the grass, grey rocks, a wooden signpost without writing, a few dry "
                 "tufts, a stone lantern far behind in the middle.",
         top="the top of the ochre hill with its big emerald crystal clusters at the left; the rest a warm clear sky, pale amber "
             "near the horizon and soft blue higher, with two or three small cream clouds on the right.",
         plat="both are flat round tops of pale grey stone with a few tiny crystal chips on the rim, clearly lighter than the "
              "earth; the tops stay empty.",
         light="warm golden afternoon, amber light from the left.",
         effects=["the crystals sparkle (pink dashed box on the hill top and pink dashed oval at the mine): draw the crystals clear, "
                  "no sparkle stars, no glow"],
         leave="sparkle stars, glows, dust clouds, glowing dots",
         vi_desc="thung lũng đồi vàng chiều nắng: đồi đá vàng to bên trái cắm cụm ngọc lục bảo, cửa mỏ khung gỗ có pha lê hồng tím, "
                 "xe cút kít pha lê, mũi khoan xoắn; cây keo tán dẹt ở mép phải; bệ là mặt đá xám nhạt"),
    dict(id="c05", kind="m", spots=[5], place="the Rune Shrine", stages="20–29", boss_stage=20, boss="Sơn Viên",
         vi="Đền Phù Văn", vi_stages="ải 20 (mini boss Sơn Viên) và 21–29",
         shapes=[below("ochre", 950, 930), below("stone", 1005, 1012),
                 rect("rock", 16, 640, 64, 900), rect("rock", 176, 660, 220, 900), ell("mark", 0, 760, 236, 1040),
                 rect("mark", 880, 880, 1024, 1084)],
         fx=[("ell", (0, 700, 236, 1000)), ("rect", (300, 905, 1000, 985)), ("rect", (40, 520, 260, 690))],
         scene="a quiet stone plateau on the earth island, on a foggy early morning. Far mesas and rolling hills fade into soft "
               "lilac mist along the horizon (y 950 at the left, 930 at the right); the near ground from about y = 1005 is pale "
               "packed earth with big flat stones and short grass.",
         landmark="a rune shrine, big and grand at the far left (x 0-236, y 640-1040): a ring of tall grey standing stones on a "
                  "round stone platform around a flat altar stone; the stones are carved with simple spirals, zigzags and dots "
                  "(ornaments, not letters); at the right edge (x 880-1024, y 880-1084) two smaller standing stones and a stone "
                  "lantern.",
         details="small stacked stone cairns, offerings of fruit in a clay bowl on the altar, dry grass tufts, pale pebbles.",
         top="the tops of the tallest standing stones at the left; the rest a soft misty morning sky, peach and lilac low, pale "
             "blue higher, a pale low sun as a soft disc behind the mist on the right, two thin long clouds.",
         plat_far="a low raised round platform of grey stone blocks with carved spirals and zigzags on its short side face, its "
                  "top pale stone.",
         plat_near="a round circle of flat pale flagstones with a faint carved spiral.",
         light="foggy early morning: soft lilac and peach mist, a pale low sun, cool soft shadows; mysterious but calm.",
         effects=["the rune carvings glow (pink dashed oval at the stones): draw the carvings plain, no glow",
                  "mist drifting along the far hills (pink dashed box): only a soft plain mist band",
                  "glowing rune stones floating up (pink dashed box above the stones): keep that sky plain"],
         leave="glowing carvings, floating stones, glows, sparkles, glowing dots",
         vi_desc="cao nguyên đá sương sớm tím: vòng đá dựng chạm xoắn ốc, răng cưa quanh bàn thờ đá bên trái xa; hai đá dựng nhỏ, đèn "
                 "đá ở mép phải; gò đá xa mờ sương, mặt trời nhạt"),
    dict(id="c06", kind="m", spots=[6], place="the Old Oak Grove", stages="30–39", boss_stage=30, boss="Cổ Vương",
         vi="Rừng Sồi Già", vi_stages="ải 30 (mini boss Cổ Vương) và 31–39",
         shapes=[below("tree", 880, 898), below("grass", 1002, 1012),
                 poly("trunk", (0, CUT), (128, CUT), (150, 700), (186, 1072), (0, 1072)),
                 poly("tree", (0, CUT), (760, CUT), (720, 230), (420, 300), (140, 320), (0, 330)),
                 ell("water", 0, 1000, 262, 1066), ell("tree", 862, 884, 1024, 1094)],
         fx=[("rect", (360, 300, 1000, 640)), ("ell", (0, 1000, 262, 1066))],
         scene="a grove of old oaks on the earth island, on a golden autumn afternoon. Smaller oaks with round gold and olive "
               "crowns close the back (tree tops from about y = 880 at the left to y = 898 at the right); the near ground from "
               "about y = 1002 is soft grass with fallen golden leaves. At the left edge a huge old oak rises from the ground to "
               "the top of the image: a thick gnarled trunk with deep bark, big roots reaching into a small round pond at its foot "
               "(x 0-262, y 1000-1066); its wide crown of olive-green leaves turning gold and orange spreads across the top part "
               "(staying above y = 330). At the right edge, below y = 884, a round young oak bush.",
         landmark="the huge old oak with its roots in the pond at the far left (the Old Oak Grove): moss on the roots, a hollow in "
                  "the trunk, acorns and chestnuts scattered on the bank.",
         details="fallen golden oak leaves, acorns and chestnuts, mushrooms at the roots, a low wooden fence far behind, small "
                 "round stones on the pond's edge.",
         top="the oak's wide gold and olive crown crossing from the top-left; the rest a warm late-afternoon sky, pale gold near "
             "the horizon and soft blue higher, with two or three small cream clouds on the right.",
         plat_far="a low raised round platform: the flat cut top of a giant old oak stump, pale wood with tree rings, its short "
                  "side face rough bark.",
         plat_near="a flat round slab of pale sandstone with a few acorns on its rim.",
         light="golden autumn afternoon: warm gold light through the oak from the left, soft long shadows; cosy and calm.",
         effects=["golden leaves falling through the air (pink dashed box): no leaves in the air",
                  "ripples on the pond (pink dashed oval): keep the water flat and plain"],
         leave="leaves in the air, ripples, sparkles, glows, glowing dots",
         vi_desc="rừng sồi già chiều thu: sồi cổ thụ thân sần bên trái, rễ cắm xuống hồ nhỏ, tán vàng ô liu vắt phía trên; sồi non ở "
                 "mép phải; bệ là mặt gốc sồi cưa có vân năm"),
    dict(id="c07", kind="m", spots=[7], place="the Terraced Fields", stages="40–49", boss_stage=40, boss="Sa Trùng",
         vi="Ruộng Bậc Thang", vi_stages="ải 40 (mini boss Sa Trùng) và 41–49",
         shapes=[below("field", 880, 900), below("ground", 1004, 1012),
                 poly("field", (0, 1046), (0, 590), (90, 548), (200, 610), (256, 1046)),
                 ell("mark", 30, 460, 176, 590), rect("mark", 870, 880, 1024, 1090)],
         fx=[("rect", (300, 880, 1000, 1000)), ("rect", (870, 880, 1024, 1090))],
         scene="farmland on the earth island, at a bright summer noon. Rolling hills of green farm terraces curve along the "
               "horizon (from about y = 880 at the left to y = 900 at the right), each step edged with a thin earth wall; the near "
               "ground from about y = 1004 is a pale dry earth path with grass on its edges. A tall round hill of terraces rises at "
               "the left up to about y = 548.",
         landmark="at the far left the tall terraced hill (x 0-256): five or six stepped green fields curving around it, and on "
                  "its top step a small field hut with a straw roof (x 30-176, y 460-590); at the right edge (x 870-1024, "
                  "y 880-1090) two big haystacks and a wooden cart with a straw load.",
         details="a scarecrow without a face far away on a terrace, small wooden fences, baskets, wild flowers along the path, a "
                 "few pebbles.",
         top="the straw-roofed hut on the terraced hill top at the left; the rest a clear deep blue summer sky with two or three "
             "tall white cumulus clouds with thin ink outlines.",
         plat_far="a low raised round platform of packed earth edged with a ring of fieldstones, like one round terrace step, its "
                  "top pale dry sand.",
         plat_near="a flat round slab of pale stone with a ring of straw on its rim.",
         light="bright summer noon: clear blue sky, tall white clouds, fresh green fields, crisp sunlight; cheerful.",
         effects=["wind waves rolling over the fields (pink dashed box): plain fields, no wind lines",
                  "dust and loose straw blowing from the haystacks (pink dashed box at the right): no dust, no straw in the air"],
         leave="wind lines, dust clouds, straw in the air, sparkles, glows",
         vi_desc="ruộng bậc thang trưa hè: đồi ruộng bậc thang cao bên trái có chòi mái rơm trên đỉnh; đồi ruộng xanh nối nhau phía "
                 "sau; hai đụn rơm, xe gỗ chở rơm ở mép phải; mây tích trắng cao"),
    dict(id="c08", kind="m", spots=[8], place="the Diamond Cliff", stages="50–59", boss_stage=50, boss="Bùn Ngoạm",
         vi="Vách Kim Cương", vi_stages="ải 50 (mini boss Bùn Ngoạm) và 51–59",
         shapes=[below("rock", 890, 905), below("ground", 1005, 1012),
                 poly("rock", (0, CUT), (190, CUT), (220, 600), (250, 900), (240, 1066), (0, 1066)),
                 ell("mark", 0, 840, 200, 1062), rect("mark", 880, 880, 1024, 1090)],
         fx=[("ell", (0, 840, 200, 1062)), ("rect", (20, 420, 220, 820))],
         scene="the floor of a wide canyon on the earth island, at a hot orange sunset. Far canyon walls and flat-topped mesas of "
               "layered red-brown rock close the back (tops at about y 890-905); the near ground from about y = 1005 is pale sand "
               "with small stones and a few dry shrubs. A tall cliff of layered ochre and red-brown rock rises at the left edge from "
               "the ground to the top of the image (its right side at about x = 220-250).",
         landmark="big pale-blue diamond crystals stick out of the cliff face at the left (the Diamond Cliff; flat colours, no "
                  "shine), and a pile of fallen diamond crystals lies at its foot (x 0-200, y 840-1062); at the right edge "
                  "(x 880-1024, y 880-1090) a short red rock pillar with two small diamond crystals and a round cactus beside it.",
         details="small diamond chips in the sand, dry thorny shrubs, round stones, a broken wooden ladder against the cliff.",
         top="the top of the diamond cliff at the left; the rest a hot sunset sky, orange and gold low, pink and soft violet "
             "higher, long streaky cream clouds.",
         plat_far="a low raised round platform of layered red-brown rock with small pale-blue diamond chips around its short side "
                  "face, its top pale sand.",
         plat_near="a flat round slab of pale sandstone.",
         light="hot orange sunset in the canyon: orange and pink sky, warm red light on the cliffs, cool violet shadows; the sandy "
               "floor and the two platforms stay light.",
         effects=["the diamonds sparkle (pink dashed oval and box): draw the diamonds clear, no sparkle stars, no glow"],
         leave="sparkle stars, glows, dust clouds, glowing dots",
         vi_desc="lòng hẻm núi lúc hoàng hôn cam: vách đá phân lớp vàng đỏ bên trái cắm kim cương xanh nhạt, đống kim cương rơi dưới "
                 "chân; cột đá đỏ thấp, xương rồng ở mép phải; gò đá đỉnh bằng xa"),
    dict(id="c09", kind="m", spots=[9], place="the Terracotta Kiln Yard", stages="60–69", boss_stage=60, boss="Thiên Thạch Thú",
         vi="Lò Gốm Đất Nung", vi_stages="ải 60 (mini boss Thiên Thạch Thú) và 61–69",
         shapes=[below("ochre", 950, 930), below("stone", 1004, 1010),
                 poly("brick", (20, 1040), (30, 820), (66, 650), (92, 530), (140, 530), (166, 650), (202, 820), (212, 1040)),
                 ell("mark", 0, 900, 230, 1062), rect("mark", 888, 880, 1024, 1086)],
         fx=[("ell", (50, 930, 180, 1040)), ("rect", (60, 380, 170, 525)), ("rect", (420, 200, 1010, 620))],
         scene="a pottery yard on the earth island, on a clear night under a big full moon. Dark blue rolling hills and mesas reach "
               "the horizon (y 950 at the left, 930 at the right); the near ground from about y = 1004 is smooth pale packed clay "
               "lit by the moon, with a few broken potsherds.",
         landmark="at the far left a tall bottle-shaped kiln of red bricks (x 20-212, up to y = 530) with a dark arched firing mouth "
                  "at its foot, a soft warm glow deep inside (no fire); around its foot (x 0-230, y 900-1062) wooden shelves with "
                  "rows of terracotta jars, pots and vases drying, a potter's wheel and a stack of firewood; at the right edge "
                  "(x 888-1024, y 880-1086) a row of big terracotta jars and vases and a stack of firewood.",
         details="small clay pots, a basket of clay lumps, a water barrel, potsherds, a stone lantern.",
         top="the neck of the bottle kiln at the left; the rest a deep blue starry night sky with a big round pale-yellow full "
             "moon at the upper right and a few small clouds lit by the moon.",
         plat_far="a low raised round platform of red bricks with a short side face, its top pale cream clay tiles.",
         plat_near="a flat round slab of pale fired-clay tiles.",
         light="clear moonlit night: deep blue sky and cool blue shadows, silver moonlight on the yard and the platforms, warm "
               "orange light from the kiln mouth; the floor and the two platforms stay light.",
         effects=["the fire glowing in the kiln mouth (pink dashed oval): draw the mouth dark with only a soft warm glow deep "
                  "inside, no flames", "smoke from the kiln's neck (pink dashed box above it): keep that sky plain, no smoke",
                  "twinkling stars and shooting stars (pink dashed box in the sky): small plain dots only, no glow"],
         leave="flames, smoke, sparks, shooting stars, glow halos, glowing dots",
         vi_desc="sân lò gốm đêm trăng tròn: lò gạch đỏ hình cổ chai bên trái xa, cửa lò tối ánh cam, kệ gỗ chum vại phơi, bàn xoay "
                 "gốm; hàng chum vại, đống củi ở mép phải; trời sao"),
    dict(id="b70", kind="b", spots=[10], place="the Golden Pyramid Temple", stages="70", boss="Thổ Tinh",
         vi="Kim Tự Viện", vi_stages="ải 70 (boss Thổ Tinh, 3 dạng)",
         shapes=[below("ground", 975, 990), below("stone", 1022, 1036),
                 poly("ochre", (60, 975), (200, 760), (300, 560), (380, 390), (644, 390), (724, 560), (824, 760), (964, 975)),
                 rect("stone", 474, 390, 550, 975), rect("brick", 420, 268, 604, 390), poly("gold", (396, 286), (512, 196), (628, 286)),
                 ell("mark", 20, 820, 186, 1000), rect("mark", 880, 870, 1024, 1070)],
         fx=[("ell", (118, 1062, 482, 1160)), ("rect", (396, 180, 628, 300)), ("ell", (20, 820, 186, 1000)),
             ("rect", (0, 300, 300, 700)), ("rect", (724, 300, 1024, 640))],
         scene="the foot of the great pyramid temple at the heart of the earth island, at a grand dusk with a sandstorm rolling in. "
               "Behind the arena a huge stepped pyramid of sand-coloured stone blocks rises and fills the top part, a wide straight "
               "stairway in its middle coming down towards the arena (x 474-550); on its top platform a small temple with red "
               "pillars and a golden tiled roof with curved eaves (x 396-628, y 196-390). Beyond the far edge of the plaza, far "
               "dunes reach the horizon (y 975-990). The ground from about y = 1022 is old pale sandstone flagstones, a little "
               "lighter in the middle.",
         landmark="two big stone guardian lion statues on carved pedestals, facing the arena: one at the far left (x 20-186, "
                  "y 820-1000), one at the right edge (x 880-1024, y 870-1070); and the stepped pyramid with its golden-roofed "
                  "temple behind.",
         details="sandstone blocks along the plaza edge, two unlit bronze braziers, carved spiral tiles, a few plain pennants "
                 "without writing on poles far behind, small drifts of sand.",
         top="the top of the pyramid with the red-pillared temple and its golden roof at the top centre (a small golden ball on "
             "the roof ridge); a dramatic dusk sky, amber and gold low, violet higher, big rolling clouds of sand and dust "
             "gathering at both sides.",
         plat_far="a grand raised round dais of carved sandstone: spiral and zigzag carvings on its side face, a gold ring inlaid "
                  "in its pale stone top.",
         plat_near="a flat round slab of pale sandstone with a thin gold ring.",
         light="the climax of the island: a grand amber-gold and violet dusk, rolling sand clouds, warm golden rim light on the "
               "lions, the temple and the dais. Grand and dramatic, still cute, not horror. The game darkens this image for the "
               "boss's later forms and adds a sandstorm and lightning, so keep it clear, rich and not too dark.",
         effects=["an earth rune circle that lights up on the dais top (pink dashed oval): keep the top plain stone with only the "
                  "gold ring", "the golden roof shines (pink dashed box at the temple): plain roof, no sparkle", "the lions' eyes "
                  "glow (pink dashed oval at the left lion): plain stone eyes", "sand gusts blowing at both sides (pink dashed "
                  "boxes): big soft clouds are fine, no streaks of sand in the air", "sandstorm and lightning in the later forms: "
                  "no lightning"],
         leave="glowing runes, sparkles, streaks of sand in the air, glowing eyes, lightning, glows",
         vi_desc="chân kim tự tháp bậc lúc chạng vạng vàng tím, bão cát kéo tới: kim tự tháp đá cát, cầu thang giữa, đền cột đỏ mái "
                 "vàng trên đỉnh; hai tượng sư tử đá hai bên; bệ boss sa thạch chạm xoắn ốc, vòng vàng"),
    dict(id="fx", kind="fx", vi="Sheet phần động đảo Thổ", vi_stages="ải 1–70",
         items=["a gust of blowing sand: a long curling wisp of golden sand grains streaming to the right, thicker at its start "
                "and fading at its tail, no ink outline",
                "a glowing earth rune circle seen at a low angle (a wide flat ellipse): a ring of spirals, zigzags and dots inside "
                "a double ring, pale glowing amber",
                "a falling autumn oak leaf: a lobed oak leaf in warm orange and gold with a brown vein and a short stem, thin ink "
                "outline",
                "a falling small rock: a chunky little ochre-brown rock with two tiny pebbles beside it, thin ink outline",
                "a puff of dust: a round soft cloud of pale sandy dust made of three or four round bumps, thin light ink outline",
                "a floating rune stone: a small round flat stone token with a carved spiral, the carving glowing pale amber, thin "
                "ink outline"],
         names=["sandgust", "earthrune", "oakleaf", "pebble", "dust", "glyph"],
         vi_desc="6 món: luồng cát bay, vòng phù văn đất, lá sồi thu rơi, đá vụn rơi, bụi phồng, phù văn đá bay"),
]
BY_ID = {a["id"]: a for a in ARENAS}
KIND_VI = {"c": "thường", "m": "chặng có mini boss", "b": "boss", "fx": "phần động"}

# Game dùng nền thế nào: khoá nền game -> (ảnh duyệt, màu phủ hoặc None, phần động). Ải mini boss phủ màu nhẹ và thêm phần động mạnh
# hơn; boss dạng 2, 3 phủ tối bụi dần, thêm bão cát, sét. Ảnh có sẵn dùng lại: Islands/Anim anim_smoke_big, anim_smoke_small,
# anim_sparkle, anim_leaf, anim_wind; BattleBG/Anim san_glow, san_mist, san_wisp, san_cloud, san_bolt.
USES = {
    "tho_c01": ("c12", None, "sóng nhỏ mép bờ"),
    "tho_c02": ("c12", None, "như c01"),
    "tho_c03": ("c34", None, "lấp lánh pha lê"),
    "tho_c04": ("c34", None, "như c03"),
    "tho_c05": ("c05", None, "phù văn sáng, sương, phù văn đá bay"),
    "tho_s20": ("c05", "#e0dcec", "phù văn bừng, đá bay dày, sương dày"),
    "tho_c06": ("c06", None, "lá sồi rơi"),
    "tho_s30": ("c06", "#f0e2d4", "lá sồi rơi dày, đom đóm"),
    "tho_c07": ("c07", None, "gió lướt ruộng, bụi rơm"),
    "tho_s40": ("c07", "#e6e6d6", "bụi cát phồng dày, gió mạnh"),
    "tho_c08": ("c08", None, "lấp lánh kim cương"),
    "tho_s50": ("c08", "#f0dcd4", "lấp lánh dày, đá vụn rơi"),
    "tho_c09": ("c09", None, "lửa lò, khói, sao nhấp nháy"),
    "tho_s60": ("c09", "#d8d4e6", "lửa lò bùng, khói dày"),
    "tho_s70": ("b70", None, "vòng phù văn đất trên bệ, lấp lánh mái vàng, mắt sư tử sáng, luồng cát hai bên"),
    "tho_s70_2": ("b70", "#dcc8ac", "thêm mây bụi trôi, luồng cát dày"),
    "tho_s70_3": ("b70", "#a48874", "thêm bão cát dày, sét kèm chớp màn"),
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


SLUG = {1: "bai_da_cuoi", 2: "hang_lung", 3: "doi_ngoc_luc", 4: "mo_pha_le", 5: "den_phu_van", 6: "rung_soi_gia",
        7: "ruong_bac_thang", 8: "vach_kim_cuong", 9: "lo_gom_dat_nung", 10: "kim_tu_vien"}
SPOT_EN = {1: "the pebble heaps, the stone cairn and the spiral seashell on the beach", 2: "the badger den mound with its burrow",
           3: "the ochre hill with the emerald crystals", 4: "the crystal mine entrance with the wheelbarrow and the drill bit",
           5: "the ring of standing stones around the altar", 6: "the huge old oak by the pond",
           7: "the hill of farm terraces with the straw-roofed hut", 8: "the layered rock cliff with the diamond crystals",
           9: "the bottle kiln and the shelves of terracotta jars", 10: "the stepped pyramid with the golden-roofed temple and the "
                                                                     "lion statues"}
SPOT_VI = {1: "đống cuội, ụ đá xếp, vỏ ốc", 2: "hang lửng", 3: "đồi đá vàng cắm ngọc lục bảo", 4: "cửa mỏ pha lê, xe cút kít, mũi khoan",
           5: "vòng đá dựng quanh bàn thờ", 6: "sồi cổ thụ bên hồ", 7: "đồi ruộng bậc thang, chòi rơm", 8: "vách đá cắm kim cương",
           9: "lò gốm cổ chai, kệ chum vại", 10: "kim tự tháp bậc, đền mái vàng, tượng sư tử"}


# chỗ thật của địa danh trên bản đồ ghép đảo Thổ (px; build_zone70_tho.py SPOTS_REAL đo tay 2026-11-06)
SPOT_FIX = {1: (745, 4135), 2: (275, 3937), 3: (790, 3442), 4: (240, 3272), 5: (740, 3072), 6: (255, 2590), 7: (745, 2146),
            8: (235, 1726), 9: (320, 900), 10: (512, 180)}


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
# Đo trên ảnh đã duyệt 2026-11-27 (lưới 100 px). Phù văn đá bay: "wisp" với san_glyph; lá sồi, đá vụn: "leaf"; gió lướt ruộng:
# "wave" với anim_wind (như đảo Mộc); bụi: "wisp", "spout" với san_dust; luồng cát hai bên kim tự tháp: "cloud" với san_sandgust (trôi
# ngang chậm); lửa lò gốm: "glow" với anim_flame_a (như đảo Hỏa).
SMOKE, SMOKE_BIG = "anim_smoke_small", "anim_smoke_big"
LAMP = "#ffcf80"
_c01 = [fx("wave", 320, 978, 90, w=520, h=22, n=2), fx("sparkle", 790, 1070, 26, w=80, h=30, n=1)]
_c03 = [fx("sparkle", 150, 520, 34, w=200, h=220, n=3), fx("sparkle", 180, 800, 30, w=240, h=120, n=2),
        fx("glow", 140, 440, 120, c="#8dffb5")]
_c05 = [fx("glow", 120, 780, 160, c="#ffd27a"), fx("glow", 330, 760, 150, c="#ffd27a"),
        fx("wisp", 230, 760, 30, w=300, h=100, n=3, img="san_glyph"), fx("mist", 700, 860, 260, w=560, h=50, n=3),
        fx("glow", 959, 845, 50, c=LAMP)]
_leaves = [fx("leaf", x, y, s, n=2, img="san_oakleaf") for x, y, s in ((300, 600, 30), (560, 500, 30), (760, 650, 28), (450, 850, 28))]
_c06 = _leaves + [fx("ripple", 170, 1020, 80, w=260, h=20, n=2)]
_c07 = [fx("wave", 650, 900, 110, w=600, h=120, n=3, img="anim_wind"), fx("wisp", 930, 950, 40, w=120, h=30, n=2, img="san_dust")]
_c08 = [fx("sparkle", 90, 640, 34, w=160, h=480, n=3), fx("sparkle", 110, 990, 32, w=180, h=80, n=2),
        fx("sparkle", 950, 990, 28, w=60, h=60, n=1)]
_c09 = [fx("glow", 250, 925, 200, c="#ffb060"), fx("glow", 250, 940, 80, img="anim_flame_a"),
        fx("wisp", 117, 480, 50, w=20, h=8, n=2, img=SMOKE), fx("sparkle", 600, 420, 20, w=700, h=300, n=3),
        fx("glow", 767, 870, 50, c=LAMP)]
_gust = [fx("cloud", 150, 520, 180, w=300, h=240, n=2, img="san_sandgust"),
         fx("cloud", 870, 480, 180, w=300, h=240, n=2, img="san_sandgust")]
_s70 = [fx("rune", 300, 1108, 360, img="san_earthrune"), fx("sparkle", 512, 240, 36, w=200, h=80, n=2),
        fx("glow", 125, 800, 50, c="#ffd27a"), fx("glow", 934, 805, 50, c="#ffd27a")] + _gust
FX = {
    "tho_c01": _c01, "tho_c02": _c01, "tho_c03": _c03, "tho_c04": _c03,
    "tho_c05": _c05,
    "tho_s20": [fx("glow", 120, 780, 200, c="#ffd27a"), fx("glow", 330, 760, 190, c="#ffd27a"),
                fx("wisp", 230, 760, 32, w=320, h=120, n=5, img="san_glyph"), fx("mist", 700, 860, 280, w=600, h=60, n=4),
                fx("glow", 959, 845, 60, c=LAMP)],
    "tho_c06": _c06,
    "tho_s30": _c06 + [fx("leaf", 200, 420, 30, n=2, img="san_oakleaf"), fx("firefly", 600, 900, 34, w=600, h=200, n=3)],
    "tho_c07": _c07,
    "tho_s40": [fx("wave", 650, 900, 120, w=640, h=140, n=4, img="anim_wind"),
                fx("spout", 600, 1040, 60, w=420, h=60, n=2, img="san_dust"),
                fx("wisp", 930, 950, 44, w=140, h=30, n=3, img="san_dust")],
    "tho_c08": _c08,
    "tho_s50": _c08 + [fx("leaf", 170, 700, 26, n=2, img="san_pebble"), fx("leaf", 120, 520, 24, n=2, img="san_pebble")],
    "tho_c09": _c09,
    "tho_s60": [fx("glow", 250, 925, 240, c="#ffb060"), fx("glow", 250, 935, 110, img="anim_flame_a"),
                fx("wisp", 250, 900, 28, w=60, h=20, n=3, img="san_sparks"),
                fx("wisp", 117, 475, 70, w=24, h=10, n=3, img=SMOKE_BIG)] + _c09[3:],
    "tho_s70": _s70,
    "tho_s70_2": _s70 + [fx("cloud", 512, 150, 380, w=1000, h=120, n=3),
                         fx("cloud", 512, 930, 220, w=1000, h=100, n=2, img="san_sandgust")],
    "tho_s70_3": _s70 + [fx("cloud", 512, 140, 420, w=1000, h=140, n=4),
                         fx("cloud", 512, 930, 240, w=1000, h=120, n=3, img="san_sandgust"),
                         fx("bolt", 420, 680, 220, w=500, h=20)],
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
# FIXES: mã -> (câu sửa cho GPT, câu cho người dùng)
FIXES = {}


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
