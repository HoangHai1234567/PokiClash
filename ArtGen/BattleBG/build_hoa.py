# Sàn đấu đảo Hỏa 70 ải: dựng bố cục và gói gửi GPT (ArtGen/BattleBG/PROMPTS.md, mục "Đảo Hỏa 70 ải"). Sinh từ build_moc.py
# (cùng khuôn, cùng số đo khung), chỉ khác dữ liệu nền, ảnh mẫu và chữ.
# Tiết kiệm dung lượng như đảo Mộc (người dùng 2026-11-05: "tiết kiệm dung lượng, tái sử dụng nếu có thể nhưng vẫn phải độc đáo,
# khác biệt"): 8 nền thay cho 17 nền của đảo Thủy, game dùng lại nền:
# - 2 nền thường, mỗi nền cho hai chặng đầu liền nhau (Bến Đá Đen + Suối Dung Nham: ải 1–9; Rừng Than Hồng + Sườn Núi Khói: 10–19);
# - 5 nền chặng có mini boss (Lò Lửa Thiền … Hang Hồng Ngọc): mini boss ải 20–60 và các ải thường sau nó cùng một nền; ải mini boss
#   thêm phần động mạnh hơn và phủ màu nhẹ (game);
# - 1 nền boss ải 70 (Miệng Núi Lửa); dạng 2, 3 của Lân Hỏa là nền đó phủ màu tối đỏ dần, thêm tro rơi, sét (game), không vẽ thêm;
# - 1 sheet phần động 3 x 2 cho những món chưa có (tro rơi, bọt dung nham nổ, vòng phù văn lửa, chùm tia lửa, lửa ma tím, cục dung
#   nham bay); khói, lửa, tàn lửa, lấp lánh, quầng sáng, sương, đốm hồn, cánh hoa, mây bão, sét dùng lại ảnh có sẵn.
# Độc đáo: mỗi nền một giờ, một thời tiết, một bảng màu riêng (sáng trong, chiều hanh, chạng vạng xanh, bình minh hồng, trưa u ám,
# chạng vạng tím, đêm trăng, hoàng hôn đỏ thẫm), địa danh lấy từ bản đồ dài đảo Hỏa đã duyệt.
# Tướng Hỏa phần lớn đỏ, cam: đất đỏ cam dịu, mặt bệ sáng để tướng nổi.
# Khổ: GPT vẽ dọc 1024 x 1536 một lượt (như build_moc.py). Ghi: gui_gpt/hoa/ (<nn>_<mã>.txt, bo_cuc_<mã>.png, HUONG_DAN.md),
# refs/hoa/ (địa danh cắt từ bản đồ dài đảo Hỏa đã duyệt).
# Chạy: py -3 -I ArtGen/BattleBG/build_hoa.py
# Duyệt ảnh GPT đã lưu: --duyet <mã> [ảnh] (mặc định ảnh mới nhất hoa/tai_ve/<mã>*.png): lưu hoa/<mã>.png, ảnh soi khung
# hoa/soi_<mã>.png và bản cao hoa/cao_<mã>.png (1080 x 1528), rồi dựng lại gói. Lượt cần ảnh chưa duyệt thì chưa có file prompt.
# Xuất vào game: --xuat [thư_mục_thử] (8 nền, sheet fx, khoá hoa_* của arena_fx.json); phần động từng nền (FX) điền sau khi duyệt.
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
PACK = HERE / "gui_gpt" / "hoa"
WORK = HERE / "hoa"  # <mã>.png: bản duyệt; soi_<mã>.png: ảnh soi khung; cao_<mã>.png: bản cao 1080 x 1528
INBOX = WORK / "tai_ve"  # ảnh GPT lưu
REFS = HERE / "refs" / "hoa"
STYLE = HERE / "moc" / "c12.png"  # nền trận Bờ Rêu + Đồng Hoa Sáng đảo Mộc đã duyệt (1024 x 1536)
MAP1 = ART / "Islands" / "zones" / "hoa70" / "doan_1.png"  # đoạn 1 bản đồ dài đảo Hỏa đã duyệt: màu, dáng đồ vật
MAP_JSON = ART / "guides" / "zone70_hoa.json"  # build_zone70_hoa.py: chỗ địa danh trên bản đồ dài
MAP_WORK = ART / "Islands" / "zones" / "hoa70"  # doan_k.png: đoạn bản đồ dài đã duyệt
DAIS = ART.parent / "Assets" / "03 Art" / "Islands" / "be_hoa_boss.png"
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
COL = {"sky": (200, 230, 248), "sea": (70, 150, 220), "lava": (245, 140, 35), "ground": (232, 166, 136),
       "ember": (226, 120, 62), "trunk": (96, 70, 60), "rock": (122, 116, 116), "stone": (205, 198, 178),
       "iron": (112, 122, 138), "roof": (196, 72, 60), "mark": (222, 222, 222)}
LEGEND = {"sky": "pale blue = sky", "sea": "blue = sea", "lava": "orange = lava (a flat surface)",
          "ground": "light red-orange = volcanic earth, ash or far hills",
          "ember": "dark orange = tree crowns, leafy bushes or a far forest",
          "trunk": "dark brown = charred trunks, branches and roots", "rock": "dark grey = basalt rocks, ridges, cliffs or cave walls",
          "stone": "beige grey = flagstones, stone tiles or a smooth rock floor", "iron": "blue grey = iron plates, roofs and spikes",
          "roof": "red = temple roofs and eaves", "mark": "light grey with an ink edge = the landmark"}
LEGEND_VI = {"sky": "xanh nhạt là trời", "sea": "xanh là biển", "lava": "cam là dung nham (mặt phẳng)",
             "ground": "đỏ cam nhạt là đất núi lửa, tro, đồi xa", "ember": "cam sẫm là tán cây, bụi lá, rừng xa",
             "trunk": "nâu sẫm là thân, cành, rễ cây cháy", "rock": "xám sẫm là đá bazan, gờ, vách, vách hang",
             "stone": "be xám là sân đá, gạch đá, nền đá phẳng", "iron": "xám xanh là tấm sắt, mái tôn, gai sắt",
             "roof": "đỏ là mái chùa", "mark": "xám nhạt viền mực là địa danh"}

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
    dict(id="c12", kind="c", spots=[1, 2], place="the Black Stone Pier and the Lava Stream", stages="1–9",
         vi="Bến Đá Đen + Suối Dung Nham", vi_stages="ải 1–9 (chặng 1, 2)",
         shapes=[below("sea", 975, 975),
                 poly("ground", (0, 1022), (300, 1032), (520, 1020), (640, 978), (780, 942), (1024, 912), (1024, CH), (0, CH)),
                 poly("lava", (560, 1012), (700, 998), (860, 990), (1024, 982), (1024, 1004), (860, 1012), (700, 1020), (560, 1026)),
                 ell("mark", 0, 928, 182, 1066), ell("mark", 860, 880, 1024, 1068)],
         fx=[("rect", (560, 975, 860, 1030))],
         scene="where the volcanic island meets the sea, on a bright clear morning. The calm sea fills the far part on the left up "
               "to the horizon at y = 975, with small soft wave lines; a plain wobbly shoreline with a thin band of dark sand and "
               "round black pebbles runs from about y = 1022 at the left edge to y = 1020 at x = 520, just behind the far platform. "
               "On the right the land rises into a gentle slope of soft red-orange volcanic earth whose crest reaches about y = 912 "
               "at the right edge. A narrow stream of lava flows across the far slope from the right edge towards the middle (y "
               "about 982-1026) and sinks into a crack in the ground at about x = 560, well behind the far platform. The near "
               "ground is soft red-orange earth with patches of grey ash, small cracks and dry tufts.",
         landmark="two landmarks of the island: at the far left on the shore (x 0-182, y 928-1066) a short wooden pier on black "
                  "posts and a heap of big black basalt boulders with flat six-sided tops (the Black Stone Pier); at the right edge "
                  "(x 860-1024, y 880-1068) a small arched bridge of dark basalt blocks with low stone rails, the lava stream "
                  "flowing under it (the Lava Stream).",
         details="black pebbles and a little driftwood along the shore, small cracks in the earth with a thin orange line inside, "
                 "dry grass tufts, a few small red crystals and black stones over the right half of the ground.",
         top="the same bright pale-blue sky, hatched with diagonal pencil strokes like image 1, becoming only a little deeper blue "
             "towards the very top, with three or four small fluffy cream clouds with thin ink outlines, spread out.",
         plat="both are low round mounds of pale ash-grey sand, clearly lighter than the earth, ringed with small black pebbles.",
         light="bright clear morning, light from the top-left.",
         effects=["embers drifting over the lava stream (pink dashed box): keep the lava flat and plain, no embers, no glow"],
         leave="smoke, steam, sparks, flying embers, glows, foam on the shore (the game adds embers over the lava and small waves "
               "on the shore)",
         vi_desc="bờ biển cát sẫm lúc sáng trong: biển bên trái xa, dốc đất đỏ cam bên phải có suối dung nham nhỏ; bến gỗ cọc đen "
                 "và đá bazan bên trái xa, cầu vòm đá bazan qua suối ở mép phải; bệ là gò cát tro nhạt"),
    dict(id="c34", kind="c", spots=[3, 4], place="the Ember Forest and the Smoky Slope", stages="10–19",
         vi="Rừng Than Hồng + Sườn Núi Khói", vi_stages="ải 10–19 (chặng 3, 4)",
         shapes=[below("ember", 880, 898), below("ground", 1002, 1012),
                 poly("trunk", (0, CUT), (128, CUT), (150, 700), (178, 1072), (0, 1072)),
                 poly("ember", (0, CUT), (760, CUT), (720, 230), (420, 300), (140, 320), (0, 330)),
                 ell("mark", 0, 880, 186, 1072), ell("ember", 862, 884, 1024, 1094)],
         fx=[("rect", (10, 560, 200, 870))],
         scene="a clearing in a forest of charred black trees with ember-orange leaves, on a hazy warm afternoon. A wall of round "
               "ember-leaf trees closes the back along the horizon (tree tops from about y = 880 at the left to y = 898 at the "
               "right); the near ground from about y = 1002 is soft volcanic earth with grey ash and fallen orange leaves. At the "
               "far left edge a giant old charred tree with thin orange cracks in its black bark rises from the ground to the top "
               "of the image; its huge branch with round crowns of orange and red leaves reaches across the top part (staying "
               "above y = 330). At the right edge, below y = 884, a round bush of ember-orange leaves.",
         landmark="at the far left, in front of the giant trunk (x 0-186, y 880-1072), a mound of layered grey rock with three "
                  "round vent holes ringed with yellow sulfur crust (the Smoky Slope; no smoke, the game adds it); and the giant "
                  "charred tree with its ember-orange leaves and the ember forest all around (the Ember Forest).",
         details="fallen orange leaves and black twigs on the ground, small sulfur-yellow rocks near the vents, black stones, dry "
                 "tufts, a short stone fence far behind in the middle.",
         top="the giant charred branch with round ember-orange crowns crossing from the top-left, the rest a warm hazy sky, pale "
             "amber near the horizon and soft blue higher, with two or three small cream clouds on the right.",
         plat="both are flat round tops of cooled lava rock, pale grey and clearly lighter than the earth, with a crackle "
              "pattern of thin dark lines and a few tiny orange glints in the cracks; the tops stay empty.",
         light="hazy warm afternoon, amber light from the top-left.",
         effects=["smoke rising from the three vent holes (pink dashed box above the mound): keep the air there plain, no smoke"],
         leave="smoke, steam, falling leaves in the air, sparks, glowing dots, glows",
         vi_desc="bãi trống trong rừng cây cháy tán lá cam chiều nắng hanh: cây cổ thụ cháy đen nứt vệt cam bên trái, cành tán cam "
                 "vắt phía trên; gò đá xám có ba lỗ phun viền lưu huỳnh bên trái xa; bệ là mặt đá dung nham nguội nứt vân"),
    dict(id="c05", kind="m", spots=[5], place="the Zen Fire Furnace", stages="20–29", boss_stage=20, boss="Hồ Lửa (tạm)",
         vi="Lò Lửa Thiền", vi_stages="ải 20 (mini boss, đang tạm là Hồ Lửa) và 21–29",
         shapes=[below("ground", 950, 930), below("stone", 1005, 1012),
                 rect("rock", 118, 600, 160, 800), ell("mark", 10, 760, 200, 1040), rect("mark", 880, 880, 1024, 1084)],
         fx=[("ell", (50, 900, 170, 1030)), ("rect", (880, 880, 1024, 1000))],
         scene="a quiet stone terrace of a mountain monastery of fire, at blue dusk. Dark blue mountain ridges reach the horizon "
               "(y 950 at the left, 930 at the right); a low wall of grey stones runs along the far edge of the terrace; the near "
               "ground from about y = 1005 is a courtyard of big flat stone tiles with ash in the joints.",
         landmark="a big round dome furnace of old grey stone bricks with a short chimney (x 118-160 up to y = 600), big and grand "
                  "at the far left (x 10-200, y 760-1040); its arched mouth faces the arena, dark inside with a soft warm orange "
                  "glow at the back (the game adds the flames); at the right edge (x 880-1024, y 880-1084) a small round stone "
                  "meditation platform with a bronze incense burner between two stone lanterns whose windows glow warm orange.",
         details="small stacked stone cairns, prayer flags without writing on a rope far behind, ash in the tile joints, small "
                 "pine bonsai in stone pots.",
         top="the dome of the furnace and its chimney at the left; the rest a calm dusk sky, deep blue higher with the first few "
             "stars, warm orange low behind the mountains, two thin long clouds.",
         plat_far="a low raised round platform of grey stone bricks with a carved flame pattern on its short side face.",
         plat_near="a round circle of flat pale stone tiles with ash in the joints.",
         light="calm blue dusk: deep blue sky and cool blue shadows, warm orange light from the furnace mouth and the lantern "
               "windows; peaceful.",
         effects=["flames dancing in the furnace mouth and sparks (pink dashed oval at the furnace mouth): draw the mouth dark with "
                  "only a soft warm glow at the back, no flames, no sparks", "incense smoke and the lanterns' glow (pink dashed "
                  "box at the right): no smoke, no halo around the lanterns"],
         leave="flames, sparks, smoke, glowing dots, light halos",
         vi_desc="sân đá tu viện lửa trên núi lúc chạng vạng xanh: lò vòm gạch đá to có ống khói bên trái xa, cửa lò tối ánh cam; bệ "
                 "thiền, lư hương đồng, hai đèn đá ở mép phải; núi xa xanh thẫm, sao đầu tiên"),
    dict(id="c06", kind="m", spots=[6], place="the Lotus Temple", stages="30–39", boss_stage=30, boss="Hồng Liên",
         vi="Chùa Liên Hoa", vi_stages="ải 30 (mini boss Hồng Liên) và 31–39",
         shapes=[below("ground", 905, 915), below("stone", 990, 1000), ell("lava", 0, 960, 300, 1052),
                 ell("mark", 0, 700, 186, 990),
                 poly("roof", (560, CUT), (1024, CUT), (1024, 430), (900, 405), (760, 330), (640, 250)),
                 ell("ember", 870, 880, 1024, 1092)],
         fx=[("ell", (0, 960, 300, 1052)), ("rect", (360, 300, 1000, 640))],
         scene="a temple courtyard on the slope of the volcano, at a soft pink sunrise. Terraced slopes with small orange bushes "
               "close the back (y about 905-915); the near ground from about y = 990 is a courtyard of pale flagstones. The curved "
               "red eave of a temple roof with small bronze bells crosses the top-right corner (above y = 430). A round bush of "
               "pink and orange flowering shrubs stands at the right edge below y = 880.",
         landmark="at the far left a small temple with curved red roofs and a golden lotus on its roof top (x 0-186, y 700-990), "
                  "and in front of it a round pool of lava (x 0-300, y 960-1052): a flat orange surface with dark crust lines, "
                  "half covered by big flat grey stone lotus leaves and two closed stone lotus buds.",
         details="stone lanterns at the pool's edge, pink and orange flowering shrubs, a stone bowl with incense sticks, pale "
                 "pebbles.",
         top="the curved red temple eave with bells at the top-right corner, the top of the temple roof at the left, and between "
             "them a soft pink and gold sunrise sky with two small cream clouds.",
         plat_far="a low raised round platform of pale stone, a ring of carved lotus petals on its short side face.",
         plat_near="a flat round slab of pale stone with a carved lotus flower outline.",
         light="soft pink sunrise: rosy gold light from the right, pink sky, warm reflections on the flagstones; gentle and calm.",
         effects=["lava bubbles popping in the pool (pink dashed oval): keep the lava surface flat and plain, no bubbles",
                  "lotus petals drifting through the sky (pink dashed box): no petals in the air"],
         leave="bubbles, splashes, smoke, petals in the air, glows",
         vi_desc="sân chùa trên sườn núi lửa lúc bình minh hồng: chùa nhỏ mái đỏ có sen vàng bên trái xa, hồ dung nham phủ lá sen "
                 "đá trước chùa, mái chùa cong treo chuông ở góc trên phải, bụi hoa hồng cam ở mép phải"),
    dict(id="c07", kind="m", spots=[7], place="the Spiked Steel Forge", stages="40–49", boss_stage=40, boss="Giáp Long",
         vi="Lò Rèn Gai Thép", vi_stages="ải 40 (mini boss Giáp Long) và 41–49",
         shapes=[below("rock", 950, 965), below("ground", 1008, 1020),
                 rect("rock", 110, 420, 190, 760), poly("iron", (0, 660), (250, 720), (240, 770), (0, 735)),
                 ell("mark", 0, 740, 190, 1050),
                 poly("iron", (880, 1086), (900, 930), (935, 880), (960, 960), (985, 890), (1024, 870), (1024, 1086))],
         fx=[("ell", (20, 880, 180, 1040)), ("rect", (90, 140, 290, 420))],
         scene="a forge yard on a rocky ridge of the volcano, at a smoky overcast noon. A dark rocky ridge closes the back (y "
               "950-965); the near ground from about y = 1008 is packed dark earth with iron filings and scattered metal scraps. A "
               "tall stone chimney rises at the left from the forge roof up to about y = 420 (x 110-190). At the right edge a "
               "cluster of big iron spikes sticks out of the ground at angles (x 880-1024, y 870-1086).",
         landmark="a blacksmith forge at the far left (x 0-190, y 740-1050) under a sloping roof of black riveted iron plates: a "
                  "stone hearth with a soft warm orange glow, a big anvil on a tree stump, racks of spiked steel shields and spears, "
                  "a water barrel.",
         details="broken spear shafts stuck in the ground, a pile of coal, chains hanging from a beam, horseshoes and metal "
                 "scraps, a grindstone.",
         top="the top of the stone chimney at the left; the rest a steel-grey overcast sky with heavy soft clouds, lighter towards "
             "the horizon, a hint of warm orange light from below.",
         plat_far="a low raised round platform of black iron plates with big rivets, short blunt spikes around its side face "
                  "pointing outward (not up), its top pale grey steel.",
         plat_near="a flat round slab of pale grey stone with a ring of iron rivets.",
         light="smoky overcast noon: cool steel-grey light, strong warm orange light from the forge hearth on the left; tough "
               "and heavy but friendly.",
         effects=["sparks flying from the anvil and the hearth's glow (pink dashed oval at the forge): no sparks, only a soft "
                  "warm glow in the hearth", "smoke rising from the chimney (pink dashed box above the chimney top): keep that "
                  "sky plain, no smoke"],
         leave="sparks, smoke, steam, flames, glowing dots, light halos",
         vi_desc="sân lò rèn trên gờ đá núi lửa lúc trưa u ám: lò rèn mái tôn đen đinh tán bên trái xa, ống khói đá cao, đe, giá "
                 "khiên giáo gai; cụm gai sắt cắm nghiêng ở mép phải; trời xám thép"),
    dict(id="c08", kind="m", spots=[8], place="the Illusion Fire Grove", stages="50–59", boss_stage=50, boss="Huyễn Viêm",
         vi="Rừng Lửa Ảo", vi_stages="ải 50 (mini boss Huyễn Viêm) và 51–59",
         shapes=[below("ember", 890, 905), below("ground", 1005, 1012),
                 poly("trunk", (0, CUT), (200, CUT), (190, 600), (200, 1066), (0, 1066)),
                 poly("ember", (200, CUT), (600, CUT), (450, 220), (230, 280)),
                 ell("mark", 0, 830, 186, 1062), ell("ember", 868, 900, 1024, 1096)],
         fx=[("rect", (430, 870, 1010, 990)), ("ell", (0, 830, 186, 1062))],
         scene="a magical grove of strange twisted trees at violet twilight. Smaller twisted trees close the back (tops at about y "
               "890-905) in a soft low mist; the near ground from about y = 1005 is soft violet-red earth with moss and fallen "
               "flame-shaped leaves. A tall twisted tree grows at the left edge up to the top of the image; its crown of big solid "
               "leaves shaped like flames (leaves, not fire) in orange, pink and violet arches over the top-left. Low bushes of the "
               "same flame-shaped leaves stand at the right edge below y = 900.",
         landmark="at the far left (x 0-186, y 830-1062) the twisted roots of the big tree with clusters of round violet crystals "
                  "between them.",
         details="small violet crystals in the moss, curled fallen leaves, round stones, a soft low mist along the back.",
         top="the twisted tree and its flame-shaped leaves at the left; the rest a violet twilight sky, pink low and deep violet "
             "higher, a thin crescent moon and a few stars.",
         plat_far="a low raised round platform of pale violet-grey stone with a carved swirling flame pattern on its short side "
                  "face.",
         plat_near="a flat round slab of pale violet-grey stone with a little moss on its rim.",
         light="magical violet twilight: pink and violet sky, the leaves warm orange-pink at their edges, soft violet shadows; "
               "dreamy, not scary; the ground and the platforms stay light.",
         effects=["will-o'-the-wisp flames drifting between the trees (pink dashed box): no glowing dots, no flames in the air",
                  "the violet crystals pulse (pink dashed oval): draw them clear, no halo"],
         leave="glowing dots, flames in the air, halos, sparkles, mist puffs",
         vi_desc="rừng cây xoắn lạ lúc chạng vạng tím: tán lá hình ngọn lửa cam hồng tím bên trái vắt phía trên, rễ cây có cụm pha lê "
                 "tím bên trái xa, sương mờ phía sau, trăng lưỡi liềm"),
    dict(id="c09", kind="m", spots=[9], place="the Ruby Cave", stages="60–69", boss_stage=60, boss="Hỏa Tinh",
         vi="Hang Hồng Ngọc", vi_stages="ải 60 (mini boss Hỏa Tinh) và 61–69",
         shapes=[below("rock", 950, 930), below("stone", 1004, 1010),
                 poly("rock", (0, 420), (150, 400), (300, 560), (350, 900), (332, 1046), (0, 1062)),
                 ell("mark", 10, 772, 186, 1036), rect("mark", 888, 880, 1024, 1086)],
         fx=[("ell", (10, 772, 186, 1036)), ("rect", (888, 880, 1024, 1086)), ("rect", (420, 200, 1010, 620))],
         scene="a rocky hillside in front of a cave, on a clear night under a big full moon. Dark blue rocky ridges reach the "
               "horizon (y 950 at the left, 930 at the right); a big dark rock hill rises at the left from the ground up to about "
               "y = 400 (its right side ends at about x = 350). The near ground from about y = 1004 is smooth pale grey rock lit "
               "by the moon, with small red crystal pebbles.",
         landmark="the cave mouth in the rock hill at the far left (x 10-186, y 772-1036), dark inside with a soft red light, "
                  "ringed with big clusters of ruby-red crystals; another big ruby cluster at the right edge (x 888-1024, "
                  "y 880-1086).",
         details="small ruby crystals in the rock cracks, loose stones, a few dry thorny shrubs, the faint orange glow of the far "
                 "volcano just above the horizon on the right.",
         top="the top of the rock hill with small ruby crystals at the left; the rest a deep blue starry night sky with a big "
             "round pale-yellow full moon at the upper right and a few small clouds lit by the moon.",
         plat_far="a low raised round platform of dark rock with small ruby crystals around its rim and a short side face, its "
                  "top pale grey.",
         plat_near="a flat round slab of smooth pale grey rock with tiny ruby pebbles on its rim.",
         light="clear moonlit night: deep blue sky and cool blue shadows, silver moonlight on the floor and the platforms, warm red "
               "light from the rubies; the floor and the two platforms stay light.",
         effects=["the ruby clusters pulse with red light and sparkle (pink dashed oval and box): draw the crystals clear and "
                  "bright, no halo, no sparkle stars", "twinkling stars (pink dashed box in the sky): small plain dots only, "
                  "no glow"],
         leave="glow halos, sparkle stars, glowing dots",
         vi_desc="sườn đồi đá trước hang đêm trăng tròn: miệng hang có cụm hồng ngọc to bên trái xa, cụm hồng ngọc ở mép phải, nền "
                 "đá nhạt dưới trăng, trời sao"),
    dict(id="b70", kind="b", spots=[10], place="the Volcano Crater", stages="70", boss="Lân Hỏa",
         vi="Miệng Núi Lửa", vi_stages="ải 70 (boss Lân Hỏa, 3 dạng)",
         shapes=[below("ground", 975, 990), below("stone", 1022, 1036),
                 poly("rock", (0, 975), (0, 720), (260, 420), (400, 190), (620, 190), (760, 420), (1024, 700), (1024, 975)),
                 ell("lava", 420, 160, 600, 230),
                 poly("lava", (380, 232), (410, 240), (260, 520), (120, 800), (95, 795), (230, 510)),
                 poly("lava", (612, 232), (640, 238), (780, 500), (860, 640), (835, 646), (752, 508)),
                 ell("mark", 20, 820, 186, 1000), rect("mark", 880, 870, 1024, 1070)],
         fx=[("ell", (118, 1062, 482, 1160)), ("rect", (420, 100, 620, 260)), ("ell", (20, 820, 186, 1000))],
         scene="the rim of the great volcano at the top of the fire island, at a dramatic crimson dusk. Behind the arena the huge "
               "dark cone of the volcano rises and fills the top part (its peak at about y = 190): its crater at the very top is "
               "full of lava, and two lava streams run down its slopes on the left and the right (flat orange and yellow with "
               "dark crust lines, never reaching the arena). Beyond the far edge of the rim, far ridges and a sea of ash clouds "
               "reach the horizon (y 975-990). The ground from about y = 1022 is old dark basalt flagstones with thin orange cracks, "
               "a little lighter in the middle.",
         landmark="two stone guardian statues of a qilin-like lion-dog on carved pedestals, facing the arena: one at the far left "
                  "(x 20-186, y 820-1000), one at the right edge (x 880-1024, y 870-1070); and the volcano with its lava-filled "
                  "crater behind.",
         details="black rocks and small red crystals along the arena edge, two unlit iron braziers, cracks with thin lava lines, a "
                 "few red prayer flags without writing on poles far behind.",
         top="the huge volcano cone across the top part with its lava-filled crater at the top centre and lava streams on its "
             "slopes; heavy dark-red and violet ash clouds gathering around its peak.",
         plat_far="a grand raised round dais of carved dark basalt: flame and cloud carvings on its side face, a gold ring inlaid "
                  "in its pale stone top, thin lava cracks in its side (never on its top).",
         plat_near="a flat round slab of pale basalt with a thin gold ring.",
         light="the climax of the island: crimson and violet dusk, heavy ash clouds, warm orange light from the lava and a golden "
               "rim on the statues and the dais. Grand and dramatic, still cute, not horror. The game darkens this image for the "
               "boss's later forms and adds falling ash and lightning, so keep it clear, rich and not too dark.",
         effects=["a fire rune circle that lights up on the dais top (pink dashed oval): keep the top plain stone with only the "
                  "gold ring", "lava blobs and smoke bursting from the crater (pink dashed box at the crater): flat lava in the "
                  "crater, no smoke, no flying blobs", "the statues' eyes glow (pink dashed oval at the left statue): plain stone "
                  "eyes", "falling ash and lightning in the later forms: plain clouds, no ash in the air, no lightning"],
         leave="glowing runes, smoke, sparks, flying embers, ash in the air, lightning, glows",
         vi_desc="miệng núi lửa trên đỉnh đảo lúc hoàng hôn đỏ thẫm: núi lửa to phía sau phủ phần trên, miệng đầy dung nham, hai "
                 "dòng dung nham chảy hai bên sườn, hai tượng lân đá hai bên; bệ boss bazan chạm lửa mây, vòng vàng"),
    dict(id="fx", kind="fx", vi="Sheet phần động đảo Hỏa", vi_stages="ải 1–70",
         items=["a falling ash flake: a small soft curled flake of grey ash with a glowing orange edge on one side, thin ink "
                "outline",
                "a lava bubble bursting: a round dome of orange lava splitting open at the top, three or four small yellow-orange "
                "droplets flying up, thin ink outline",
                "a glowing fire rune circle seen at a low angle (a wide flat ellipse): a ring of flame and cloud patterns and small "
                "dots inside a double ring, pale glowing orange",
                "a burst of sparks: a fan of ten or twelve short bright yellow-orange spark streaks spreading up and out from one "
                "point, each with a tiny round tip, no ink outline",
                "a will-o'-the-wisp flame: a small soft flame shaped like a teardrop with a curled tip, pink at the core and "
                "violet at the edge, thin ink outline",
                "a flying blob of lava: a round orange-yellow blob with a dark crust patch and a short tapering trail of lighter "
                "orange behind it, thin ink outline"],
         names=["ash", "lavapop", "firerune", "sparks", "foxfire", "lavablob"],
         vi_desc="6 món: vảy tro rơi, bọt dung nham nổ, vòng phù văn lửa, chùm tia lửa, lửa ma tím, cục dung nham bay"),
]
BY_ID = {a["id"]: a for a in ARENAS}
KIND_VI = {"c": "thường", "m": "chặng có mini boss", "b": "boss", "fx": "phần động"}

# Game dùng nền thế nào: khoá nền game -> (ảnh duyệt, màu phủ hoặc None, phần động). Ải mini boss phủ màu nhẹ và thêm phần động mạnh
# hơn; boss dạng 2, 3 phủ tối đỏ dần, thêm tro rơi, sét. Ảnh có sẵn dùng lại: Islands/Anim anim_smoke_big, anim_smoke_small,
# anim_flame_a, anim_flame_b, anim_embers, anim_sparkle; BattleBG/Anim san_glow, san_mist, san_wisp, san_firefly, san_petal, san_cloud,
# san_bolt.
USES = {
    "hoa_c01": ("c12", None, "tàn lửa trôi trên suối dung nham, sóng nhỏ mép bờ"),
    "hoa_c02": ("c12", None, "như c01"),
    "hoa_c03": ("c34", None, "khói ba lỗ phun, lá cam rơi"),
    "hoa_c04": ("c34", None, "như c03"),
    "hoa_c05": ("c05", None, "lửa cửa lò, khói hương, quầng đèn đá"),
    "hoa_s20": ("c05", "#e0dcec", "lửa lò bùng to, tia lửa, khói dày"),
    "hoa_c06": ("c06", None, "bọt dung nham nổ trong hồ, cánh sen bay"),
    "hoa_s30": ("c06", "#f2dcdc", "cánh sen bay dày, bọt nổ nhiều, quầng hồng ở chùa"),
    "hoa_c07": ("c07", None, "tia lửa ở đe, khói ống khói"),
    "hoa_s40": ("c07", "#dcdfe6", "tia lửa bắn mạnh, khói dày, quầng lò"),
    "hoa_c08": ("c08", None, "lửa ma tím trôi, pha lê sáng"),
    "hoa_s50": ("c08", "#e4d8ee", "lửa ma dày, pha lê bừng, sương"),
    "hoa_c09": ("c09", None, "quầng hồng ngọc, lấp lánh, sao nhấp nháy"),
    "hoa_s60": ("c09", "#d8d4e6", "hồng ngọc bừng sáng, tàn lửa bay"),
    "hoa_s70": ("b70", None, "vòng phù văn lửa trên bệ, khói và cục dung nham ở miệng núi lửa, mắt tượng sáng, tàn lửa"),
    "hoa_s70_2": ("b70", "#d4b4b4", "thêm mây tro trôi, tro rơi"),
    "hoa_s70_3": ("b70", "#9c7884", "thêm tro rơi dày, sét núi lửa kèm chớp màn"),
}


def approved(i):
    return WORK / f"{i}.png"


def needs(a):
    return [] if a["id"] == "c12" else ["c12"]


def ready(a):
    return all(approved(n).exists() for n in needs(a))


# ---------- ảnh mẫu ----------

def map_spots():
    """chỗ địa danh trên bản đồ dài đảo Hỏa (build_zone70_hoa.py): số -> (x, y) px bản đồ ghép"""
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


SLUG = {1: "ben_da_den", 2: "suoi_dung_nham", 3: "rung_than_hong", 4: "suon_nui_khoi", 5: "lo_lua_thien", 6: "chua_lien_hoa",
        7: "lo_ren_gai_thep", 8: "rung_lua_ao", 9: "hang_hong_ngoc", 10: "mieng_nui_lua"}
SPOT_EN = {1: "the wooden pier and the black basalt boulders on the shore", 2: "the arched basalt bridge over the lava river",
           3: "the charred trees with orange leaf crowns", 4: "the grey rock slope with the sulfur vents",
           5: "the dome furnace and the meditation platform", 6: "the lava pool with stone lotus leaves and the red-roofed temple",
           7: "the blacksmith forge", 8: "the trees with flame-shaped leaves", 9: "the cave mouth with the ruby crystals",
           10: "the volcano with its crater and the two guardian statues"}
SPOT_VI = {1: "bến gỗ, đá bazan đen trên bờ", 2: "cầu vòm đá bazan qua sông dung nham", 3: "cây cháy tán lá cam",
           4: "sườn đá xám có lỗ phun lưu huỳnh", 5: "lò vòm đá, bệ thiền", 6: "hồ dung nham lá sen đá, chùa mái đỏ", 7: "lò rèn",
           8: "cây tán hình ngọn lửa", 9: "hang hồng ngọc", 10: "núi lửa, hai tượng lân đá"}


# chỗ thật của địa danh trên bản đồ ghép đảo Hỏa (px; build_zone70_hoa.py SPOTS_REAL, BRIDGE_REAL đo tay 2026-11-05)
SPOT_FIX = {1: (200, 4080), 2: (420, 3742), 3: (830, 3472), 4: (230, 3312), 5: (760, 3110), 6: (260, 2570), 7: (730, 2150),
            8: (285, 1700), 9: (360, 820), 10: (530, 190)}


def make_refs():
    """cắt địa danh khỏi đoạn bản đồ dài đảo Hỏa đã duyệt (512 x 512 quanh chỗ địa danh); đoạn chưa duyệt thì chưa có"""
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
                 "nền trận Bến Đá Đen + Suối Dung Nham đã duyệt (1024 × 1536, nền đặc): lấy nét"),
                (GRID, "the numbered 3 x 2 grid: one object per cell, in number order",
                 "lưới 3 × 2 đánh số (1536 × 1024, nền trắng, ô viền hồng, số hồng ở góc): mỗi ô một món")]
    out = []
    if a["id"] == "c12":
        out.append((STYLE, "an approved battle background of ANOTHER island of this game, in the same tall format: copy its "
                           "RENDERING, perspective, platform size and look, the calm open middle and the plain hatched sky with "
                           "small clouds in the top part; not its content or colours",
                    "nền trận Bờ Rêu + Đồng Hoa Sáng đảo Mộc đã duyệt (1024 × 1536, nền đặc): bờ biển rêu, đồi cỏ, hai gò rêu làm "
                    "bệ, trời xanh gạch chì có mây nhỏ ở phần trên; lấy nét, góc nhìn, cỡ và kiểu bệ"))
        out.append((MAP1, "part 1 of the new map of this Fire island, seen from above: copy its colours and the look of its "
                          "objects (warm red-orange hatched earth, black basalt rocks, charred trees with orange leaf crowns, flat "
                          "orange lava with dark crust lines, the wooden pier, the stone bridge); ignore its layout and its "
                          "top-down view",
                    "đoạn 1 bản đồ dài đảo Hỏa đã duyệt (1024 × 1536, nền đặc, nhìn từ trên): đất đỏ cam gạch chì, đá bazan đen, "
                    "cây cháy tán cam, sông dung nham, cầu đá, bến gỗ; lấy màu và dáng đồ vật"))
    else:
        copy = ("copy its rendering, colours, perspective, platform look and brightness; not its content" if k == "c" else
                "copy its rendering, perspective and platform look; not its content, colours or daylight (this place has its own "
                "light)")
        out.append((approved("c12"), f"the approved battle background of this island (a normal stage): {copy}",
                    "nền trận Bến Đá Đen + Suối Dung Nham đã duyệt (1024 × 1536, nền đặc): lấy nét, góc nhìn, kiểu bệ, độ sáng"))
    crops = [n for n in a["spots"] if crop_of(n)]
    for n in crops:
        sz = size_of(crop_of(n)) or (512, 512)
        out.append((crop_of(n), f"a crop of this island's new map, seen from above, showing {SPOT_EN[n]}: draw the same landmark "
                                f"here, seen from the side, with its colours and shapes",
                    f"mảnh cắt bản đồ dài đảo Hỏa ({sz[0]} × {sz[1]}, nhìn từ trên xuống): {SPOT_VI[n]}"))
    if a["id"] != "c12" and not crops:
        out.append((MAP1, "part of the new map of this Fire island: the look of its objects; ignore its layout",
                    "đoạn 1 bản đồ dài đảo Hỏa (1024 × 1536): lấy dáng đồ vật"))
    if k in ("m", "b"):
        out.append((DAIS, "the island map's boss plate: a raised round platform with a flat top, a visible side face and a ring on "
                          "its top; copy only this idea for the far platform, in the material described below" +
                          (", lower and simpler" if k == "m" else ""),
                    "bệ boss của bản đồ đảo Hỏa (400 × 250, nền trong suốt): đĩa đất đỏ cam dày có mặt bên nâu, vòng vàng trên "
                    "mặt, đá xám viền"))
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


FIRE_CONTRAST = ("The fighters of this island are mostly red and orange: keep the earth a soft, muted red-orange (not saturated "
                 "red), and the two platform tops pale (ash grey, cream or pale stone), so red and orange fighters stand out.")


def rendering_text(a):
    if a["id"] == "c12":
        return ["", "RENDERING: copy image 1's rendering: wobbly dark-brown ink outlines (#2B2118), coloured-pencil hatching on "
                    "cream paper, flat warm colours with light watercolour washes, chunky cute doodle shapes with clear "
                    "silhouettes; the same perspective, the same platform size and look, the same calm open middle and plain "
                    "hatched sky. Ink about 6 px on near things and 3-4 px on far things. Use the colours and the look of the "
                    "objects of image 2 (warm red-orange hatched earth, black basalt rocks, charred trees with orange crowns, flat "
                    "orange lava with dark crust lines): a warm volcanic island, not a green forest. Not 3D, not glossy, no "
                    "realistic rendering, no tiny noisy details.",
                "",
                "CONTRAST: the fighters must stand out, so the background is a little softer and lighter than the map, with "
                "the most detail and contrast on the landmarks and along the left and right edges; the middle stays simple. "
                + FIRE_CONTRAST]
    return ["", "RENDERING: exactly as image 1 (the approved battle background of this island): the same ink, hatching, paper, "
                "perspective, platform size and look. Not 3D, not glossy, no tiny noisy details. The fighters must stand out: most "
                "detail and contrast on the landmark and along the left and right edges; the middle stays simple. " + FIRE_CONTRAST]


def arena_prompt(a, refs):
    k = a["kind"]
    lines = head(refs) + save_block(a)
    if k == "c":
        what = (f"the battle background for the stages at {a['place']} (stages {a['stages']}) of the Fire island, a volcanic "
                f"island, in a vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added "
                f"by the game) fight on it: the enemy on the smaller far platform at the upper left, the player's fighter on the "
                f"bigger near platform at the lower right.")
    elif k == "m":
        what = (f"the battle background for {a['place']} (stages {a['stages']}) of the Fire island, a volcanic island, in a "
                f"vertical mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added by the "
                f"game) fight on it: the enemy on the far raised platform at the upper left, the player's fighter on the bigger "
                f"near platform at the lower right.")
    else:
        what = (f"the battle background for the final boss stage at {a['place']} (stage 70) of the Fire island, a volcanic island, "
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
              f"WHAT THIS IS: a sprite sheet of {len(a['items'])} separate effect objects for the battle backgrounds of the Fire "
              f"island (a volcanic island) of a vertical mobile game. The game cuts the sheet into {len(a['items'])} sprites and "
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
    return f"""# Gói gửi GPT: sàn đấu đảo Hỏa 70 ải (`hoa`)

Sinh bằng `{HERE / 'build_hoa.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè). Nền trận cho 70 ải đảo Hỏa, cùng khuôn đảo Mộc: **tiết kiệm dung lượng, 8 nền thay cho 17 nền của đảo Thủy**, game dùng lại nền, nhưng mỗi nền một nơi, một giờ, một thời tiết riêng:
- **2 nền thường**, mỗi nền cho hai chặng đầu liền nhau: Bến Đá Đen + Suối Dung Nham (ải 1–9, sáng trong), Rừng Than Hồng + Sườn Núi Khói (ải 10–19, chiều hanh).
- **5 nền chặng có mini boss**: Lò Lửa Thiền (chạng vạng xanh), Chùa Liên Hoa (bình minh hồng), Lò Rèn Gai Thép (trưa u ám), Rừng Lửa Ảo (chạng vạng tím), Hang Hồng Ngọc (đêm trăng). Ải mini boss (20, 30, 40, 50, 60) và các ải thường sau nó dùng chung một nền; ải mini boss game phủ màu nhẹ và thêm phần động mạnh hơn. Ải 20 đang để Hồ Lửa đứng tạm, nền không phụ thuộc tướng.
- **1 nền boss ải 70** (Miệng Núi Lửa, hoàng hôn đỏ thẫm). Dạng 2, 3 của Lân Hỏa không vẽ thêm: game phủ tối đỏ dần, thêm mây tro, tro rơi, sét.
- **1 sheet phần động** 3 × 2, chỉ 6 món chưa có: vảy tro rơi, bọt dung nham nổ, vòng phù văn lửa, chùm tia lửa, lửa ma tím, cục dung nham bay. Khói, lửa, tàn lửa, lấp lánh (ảnh phần động bản đồ đảo), quầng sáng, sương, đốm hồn, đom đóm, cánh hoa (cánh sen), mây bão, sét (ảnh sàn đấu đảo Thủy, Mộc) dùng lại.

**Tướng Hỏa phần lớn đỏ, cam:** file prompt dặn đất đỏ cam dịu (không đỏ rực), mặt bệ sáng (xám tro, kem, đá nhạt) để tướng nổi.

**Khổ dọc, vẽ một lượt:** GPT vẽ 1024 × 1536. 880 px dưới (từ nét đứt trắng y {TOP}) là khung sân máy 9:16, phần trên là trời, tán cây, núi lửa dư cho máy dài. Game lấy y {CUT}..1536 phóng về 1080 × 1528.

Ước dung lượng (ASTC 6×6, 1080 × 1528 khoảng 0,7 MB mỗi nền): 8 nền khoảng 5,6 MB như đảo Mộc; sheet phần động thêm khoảng 0,2 MB.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Làm lượt 1 trước (chốt nét đảo Hỏa): GPT lưu xong thì nhắn Claude "duyệt c12 đảo Hỏa"; Claude soi, lưu bản duyệt và dựng file prompt các lượt sau. Nên làm mọi lượt trong cùng một chat để GPT giữ nét.

Ảnh địa danh: bản đồ dài đảo Hỏa đã duyệt đủ 3 đoạn, nên mỗi lượt có ảnh cắt địa danh của nơi đó (`{REFS}`), để địa danh trên nền trận giống bản đồ.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
{chr(10).join(rows)}

Bản duyệt Claude lưu ở `{WORK}\\<mã>.png`, kèm ảnh soi khung `soi_<mã>.png` và bản cao vào game `cao_<mã>.png` (1080 × 1528).

## Game dùng nền thế nào

Như đảo Mộc: `StageView` mượn ảnh theo `use` và phủ `tint` (khoá trong `arena_fx.json`). Phần động từng nền đo trên ảnh đã duyệt khi xuất. Khói và lửa chưa có kiểu trong `ArenaAnim`: thêm khi xuất (dùng ảnh khói, lửa của bản đồ đảo).

| Khoá nền game | Ảnh | Màu phủ | Phần động |
|---|---|---|---|
{chr(10).join(use_rows)}

## Soi trước khi nhắn Claude

- Ảnh dọc 1024 × 1536. Hai bệ đúng chỗ như bố cục (bệ xa trên trái, bệ gần to dưới phải); mặt bệ **trống** và **sáng** hơn đất.
- Mọi thứ trận cần (hai bệ, địa danh, chân trời) nằm dưới nét đứt trắng; phần trên chỉ là trời, tán cây, ống khói, núi lửa nối lên.
- Giữa hai bệ thoáng; ngay sau lưng hai tướng (khung trắng nét đứt) không có vật cao, chỗ sáng, dung nham.
- Góc trên phải và dưới trái của khung sân (gạch chéo xám) chỉ có trời, đất: bảng máu che chỗ đó.
- Đảo núi lửa đỏ cam dịu (lượt 1 không lấy màu xanh lá của ảnh mẫu đảo Mộc), không đỏ rực tới mức tướng đỏ chìm.
- Chặng có mini boss, boss: rõ là nơi đặc biệt (giờ, thời tiết, địa danh to, bệ địch nổi có mặt bên) mà vẫn đủ sáng cho ải thường, dễ thương, không đáng sợ.
- **Không vẽ phần động** file đã dặn chừa (khói, lửa trong lò, tia lửa, tàn lửa bay, bọt dung nham, cánh sen bay, lửa ma, quầng sáng, tro rơi, sét).
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
| Lượt 1 ra xanh lá như đảo Mộc | `Same layout, but this is the warm volcanic Fire island: soft muted red-orange earth, black basalt rocks, charred trees with orange crowns; no green grass.` |
| Đỏ rực, tướng đỏ sẽ chìm | `Same image, but make the earth a softer, muted red-orange and the two platform tops pale ash grey, so red and orange fighters stand out.` |
| Vẽ cả phần động | `Same image, but remove the [smoke / flames / sparks / embers / bubbles / petals / wisps / glow / ash / lightning]; leave that place plain as the file says.` |
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
# Như build_moc.py: bản cao 1080 x 1528 (hoa/cao_<mã>.png, --duyet ghi) lưu Assets/03 Art/BattleBG/battle_hoa_<khoá>.png cho 8 ảnh
# (ART_KEY); khoá dùng chung (USES) ghi "use", "tint", phần động vào arena_fx.json; sheet fx cắt thành BattleBG/Anim/san_<tên>.
# arena_fx.json chỉ thay các khoá hoa_*, giữ khoá đảo khác.
ASSETS = ART.parent / "Assets"
OUT = ASSETS / "03 Art" / "BattleBG"
OUT_FX = OUT / "Anim"
OUT_JSON = OUT / "Resources" / "arena_fx.json"
ART_KEY = {"c12": "hoa_c01", "c34": "hoa_c03", "c05": "hoa_c05", "c06": "hoa_c06", "c07": "hoa_c07", "c08": "hoa_c08",
           "c09": "hoa_c09", "b70": "hoa_s70"}


def fx(k, x, y, s, **kw):
    return dict(k=k, x=x, y=y, s=s, **kw)


# phần động từng khoá, toạ độ ảnh GPT 1024 x 1536 (khung sân là y 656..1536; món ở trên y 656 chỉ máy dài thấy), đo trên ảnh đã duyệt
# 2026-11-05. Không thêm kiểu mới vào ArenaAnim: khói là "wisp" (bay lên, lắc, mờ) với ảnh khói bản đồ đảo; lửa trong lò là "glow"
# (phập phồng) với anim_flame_a; bọt dung nham là "spout" (phồng lên rồi tan, chỗ khác trong vùng); tro rơi là "leaf" với san_ash;
# tàn lửa, tia lửa, lửa ma, cục dung nham là "wisp" với anim_embers, san_sparks, san_foxfire, san_lavablob; cánh sen là "leaf" với
# san_petal (đảo Mộc). c34: khói chỉ ở hai lỗ phun trái (lỗ thứ ba sau chân tướng địch). c08: không thêm sương động (ảnh đã vẽ
# sương; lớp san_mist thành cục mây trắng giữa cảnh hồng tím, bỏ sau khi chụp thử).
SMOKE, SMOKE_BIG, EMBER = "anim_smoke_small", "anim_smoke_big", "anim_embers"
_c01 = [fx("wisp", 630, 1012, 26, w=300, h=16, n=4, img=EMBER), fx("wave", 410, 985, 90, w=360, h=10, n=2),
        fx("sparkle", 965, 1180, 34, w=60, h=50, n=1)]
_c03 = [fx("wisp", 160, 850, 52, w=24, h=8, n=2, img=SMOKE), fx("wisp", 90, 900, 44, w=24, h=8, n=2, img=SMOKE),
        fx("wisp", 70, 640, 22, w=80, h=260, n=3, img=EMBER)]
_c05 = [fx("glow", 140, 960, 220, c="#ffb060"), fx("glow", 140, 985, 90, img="anim_flame_a"),
        fx("wisp", 880, 965, 34, w=20, h=8, n=2, img=SMOKE), fx("wisp", 95, 545, 50, w=20, h=8, n=2, img=SMOKE),
        fx("glow", 805, 965, 60, c="#ffcf80"), fx("glow", 970, 975, 60, c="#ffcf80")]
_c06 = [fx("spout", 160, 995, 40, w=240, h=60, n=2, img="san_lavapop"), fx("leaf", 500, 700, 34, n=3, img="san_petal"),
        fx("leaf", 860, 600, 34, n=2, img="san_petal"), fx("glow", 85, 780, 150, c="#ffd27a"), fx("sparkle", 75, 640, 34, w=60, h=40)]
_c07 = [fx("glow", 75, 860, 140, c="#ffa050"), fx("wisp", 120, 930, 34, w=40, h=20, n=2, img="san_sparks"),
        fx("wisp", 35, 575, 70, w=20, h=10, n=2, img=SMOKE_BIG)]
_c08 = [fx("wisp", 720, 930, 36, w=560, h=100, n=3, img="san_foxfire"), fx("glow", 90, 940, 200, c="#c58cff"),
        fx("glow", 975, 1105, 70, c="#c58cff"), fx("leaf", 300, 330, 34, n=2, img="san_petal")]
_c09 = [fx("glow", 120, 940, 220, c="#ff5a5a"), fx("glow", 950, 980, 180, c="#ff5a5a"), fx("glow", 800, 945, 90, c="#ff9050"),
        fx("sparkle", 110, 740, 36, w=120, h=80, n=2), fx("sparkle", 950, 950, 34, w=100, h=100, n=2),
        fx("sparkle", 560, 300, 20, w=700, h=300, n=3)]
_s70 = [fx("rune", 300, 1108, 360, img="san_firerune"), fx("wisp", 520, 170, 140, w=160, h=20, n=2, img=SMOKE_BIG),
        fx("wisp", 520, 185, 40, w=140, h=20, n=2, img="san_lavablob"), fx("glow", 110, 805, 50, c="#ffcf70"),
        fx("glow", 930, 860, 50, c="#ffcf70"), fx("wisp", 600, 1000, 22, w=700, h=120, n=4, img=EMBER)]
_ash = [fx("leaf", x, y, 28, n=2, img="san_ash") for x, y in ((200, 700), (500, 680), (800, 720), (650, 900))]
FX = {
    "hoa_c01": _c01, "hoa_c02": _c01, "hoa_c03": _c03, "hoa_c04": _c03,
    "hoa_c05": _c05,
    "hoa_s20": [fx("glow", 140, 960, 260, c="#ffb060"), fx("glow", 140, 980, 120, img="anim_flame_a"),
                fx("wisp", 140, 930, 40, w=80, h=30, n=2, img="san_sparks"), fx("wisp", 95, 540, 70, w=20, h=10, n=2, img=SMOKE_BIG)]
               + _c05[2:3] + _c05[4:],
    "hoa_c06": _c06,
    "hoa_s30": [fx("spout", 160, 995, 44, w=240, h=60, n=3, img="san_lavapop"), fx("leaf", 400, 720, 34, n=3, img="san_petal"),
                fx("leaf", 700, 640, 34, n=3, img="san_petal")] + _c06[1:],
    "hoa_c07": _c07,
    "hoa_s40": [fx("glow", 75, 860, 180, c="#ffa050"), fx("wisp", 120, 925, 40, w=50, h=24, n=4, img="san_sparks"),
                fx("wisp", 35, 570, 80, w=24, h=10, n=3, img=SMOKE_BIG)],
    "hoa_c08": _c08,
    "hoa_s50": [fx("wisp", 720, 930, 38, w=640, h=120, n=6, img="san_foxfire"), fx("wisp", 300, 1000, 34, w=300, h=60, n=3,
                img="san_foxfire"), fx("glow", 90, 940, 240, c="#c58cff")] + _c08[2:],
    "hoa_c09": _c09,
    "hoa_s60": _c09 + [fx("wisp", 630, 1000, 24, w=600, h=80, n=4, img=EMBER)],
    "hoa_s70": _s70,
    "hoa_s70_2": _s70 + [fx("cloud", 512, 120, 380, w=1000, h=120, n=3)] + _ash,
    "hoa_s70_3": _s70 + [fx("cloud", 512, 110, 420, w=1000, h=140, n=4), fx("bolt", 420, 680, 220, w=500, h=20)]
                 + _ash + [fx("leaf", x, y, 30, n=2, img="san_ash") for x, y in ((350, 820), (900, 980), (120, 1000))],
}
FX_NAMES = ["ash", "lavapop", "firerune", "sparks", "foxfire", "lavablob"]  # sheet fx 3 x 2


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
    if name not in ("leafrune", "firerune"):
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
    arenas = {k: v for k, v in old.get("arenas", {}).items() if not k.startswith("hoa_")}
    arenas.update(data)
    note = old.get("note", "toạ độ 0..1 theo khung sân 1080 x 928, y từ trên; cỡ theo bề ngang khung")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({"note": note, "arenas": arenas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Xuất {len(imgs)} nền, {len(data)} khoá hoa_* (giữ {len(arenas) - len(data)} khoá đảo khác) vào {out_json}")


# ---------- lượt sửa ----------
# Ảnh đã duyệt tạm nhưng sai một chỗ: file sua_<mã>.txt bảo GPT sửa đúng chỗ đó trên chính ảnh của nó (ảnh mẫu: ảnh đó, ảnh soi khung,
# bố cục). GPT lưu <mã>_2.png cạnh ảnh cũ; --duyet <mã> lấy ảnh mới nhất. Sửa xong thì bỏ mã khỏi FIXES.
# 2026-11-05: c07 lò rèn tràn sau lưng tướng địch, đất đỏ rực; c08, b70 bệ xa vẽ cao hơn chỗ đứng 60–75 px (chân tướng rơi vào mặt bên);
# cả ba đã sửa bằng sua_<mã>.txt, GPT giữ nguyên phần còn lại.
FIXES = {}  # c07, c08, b70 đã sửa và duyệt (2026-11-05)


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
    lines += ["", f"WHAT THIS IS: a correction of image 1, the battle background for {a['place']} of the Fire island in a vertical "
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
                    help="xuất 8 nền, sheet phần động và khoá hoa_* của arena_fx.json vào Assets (hoặc vào THU_MUC để thử)")
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
