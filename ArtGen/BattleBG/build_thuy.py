# Sàn đấu đảo Thủy 70 ải: dựng bố cục và gói gửi GPT (ArtGen/BattleBG/PROMPTS.md, mục "Đảo Thủy 70 ải").
# - Mỗi chặng (10 địa danh của bản đồ dài) một nền trận thường, cảnh ban ngày, địa danh nhỏ ở xa bên trái.
# - 5 ải mini boss (20–60) và boss ải 70 có nền riêng: gần địa danh hơn, giờ và thời tiết mạnh, bệ địch là bệ nổi; chừa chỗ cho
#   phần động (tia đèn, cầu vồng, sương, bong bóng, xoáy nước, đinh ba, sét…) game cho chuyển động bằng hai sheet hiệu ứng.
# - Boss 70 có 3 bản cùng bố cục (dạng 1, 2, 3 của Lam Quân), game đổi nền lúc chớp sáng tiến hóa.
# Khung: GPT vẽ 1536 x 1024; game lấy khúc giữa 1192 x 1024 (x 172..1364) thu về 1080 x 928 (khung sân của StageView). Hai chỗ
# đứng theo StageView.Pos, cỡ tướng theo StageView.Height (boss x 1,18); hai bảng máu đo trên ảnh chụp màn trận (2026-11-03).
# Ghi: gui_gpt/thuy/ (<nn>_<mã>.txt, bo_cuc_<mã>.png, HUONG_DAN.md), refs/thuy/ (mảnh cắt bản đồ đảo làm ảnh mẫu địa danh).
# Chạy: py -3 -I ArtGen/BattleBG/build_thuy.py
# Duyệt ảnh GPT đã lưu: py -3 -I ArtGen/BattleBG/build_thuy.py --duyet <mã> [ảnh] (mặc định ảnh mới nhất thuy/tai_ve/<mã>*.png):
# lưu thuy/<mã>.png và ảnh soi khung thuy/soi_<mã>.png, rồi dựng lại gói (lượt nào đủ ảnh mẫu thì có file prompt). Lượt cần ảnh
# chưa duyệt thì chưa có file prompt.
import argparse
import math
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/BattleBG
ART = HERE.parent
PACK = HERE / "gui_gpt" / "thuy"
WORK = HERE / "thuy"  # <mã>.png: bản duyệt; soi_<mã>.png: ảnh soi khung
INBOX = WORK / "tai_ve"  # ảnh GPT lưu
REFS = HERE / "refs" / "thuy"
WORLD = ART / "Islands" / "refs" / "world_style.png"
MAP = ART / "Islands" / "zones" / "thuy70" / "zone_thuy70.png"
DAIS = ART.parent / "Assets" / "03 Art" / "Islands" / "be_thuy_boss.png"
GRIDS = {"4x3": ART / "guides" / "G_Sheet4x3.png", "3x2": ART / "guides" / "G_Sheet3x2.png"}

W, H = 1536, 1024
X0, X1 = 172, 1364  # khúc game lấy
G = (X1 - X0) / 1080


def gp(x, y):
    """toạ độ khung sân 1080 x 928 -> ảnh GPT"""
    return X0 + x * G, y * G


FOE, ME = gp(316, 472), gp(784, 836)  # chân địch, chân phe mình (StageView.Pos x 2)
FOE_PLAT = (round(FOE[0]), round(FOE[1] + 5), 400, 116)  # tâm, rộng, cao
FOE_DAIS = (round(FOE[0]), round(FOE[1] + 8), 470, 136, 44)  # tâm mặt trên, rộng, cao, mặt bên
ME_PLAT = (round(ME[0]), round(ME[1] + 7), 540, 160)
FOE_BOX = (391, 121, 651, 521)  # thân tướng địch, cao tới 300 x 1,18 (boss) px khung
ME_BOX = (887, 495, 1187, 923)
PANELS = [(815, 0, 1364, 240), (185, 760, 720, 960)]  # bảng tên, máu: địch trên phải, phe mình dưới trái

INK = (43, 33, 24)
COL = {"sky": (200, 230, 248), "sea": (70, 150, 220), "water": (130, 200, 240), "sand": (246, 228, 176),
       "grass": (178, 222, 170), "rock": (140, 140, 140), "stone": (205, 198, 178), "mark": (222, 222, 222)}
LEGEND = {"sky": "pale blue = sky", "sea": "blue = sea", "water": "light blue = pool, stream, waterfall, lake or shallow water",
          "sand": "pale sand = sandy ground", "grass": "light green = grass, hills or jungle", "rock": "dark grey = rocks and cliffs",
          "stone": "beige grey = flagstones or carved stone", "mark": "light grey with an ink edge = the landmark"}
LEGEND_VI = {"sky": "xanh nhạt là trời", "sea": "xanh là biển", "water": "xanh sáng là hồ, suối, thác, nước nông",
             "sand": "cát nhạt là đất cát", "grass": "xanh lá nhạt là cỏ, đồi, rừng", "rock": "xám sẫm là đá, vách",
             "stone": "be xám là sân đá, đá chạm", "mark": "xám nhạt viền mực là địa danh"}

# mảnh cắt bản đồ dài làm ảnh mẫu địa danh: tâm (cắt 512 x 512) hoặc hộp; câu tả cho GPT, cho người dùng
SPOTS = {
    "bai_bien": ((0, 3700, 1024, 4288), "the beach where the island starts: sandy shore, turquoise sea, giant pastel seashells, palm trees, grey rocks",
                 "khúc đáy bản đồ: bãi cát, biển, vỏ sò hồng to, cọ, đá xám"),
    "vung_san_ho": ((684, 3743), "the coral tide pool", "vũng san hô: hồ nhỏ viền đá, san hô hồng, cam"),
    "cau_go_reu": ((418, 3617), "the mossy wooden bridge over the stream", "cầu gỗ qua suối"),
    "lang_vo_oc": ((348, 3392), "the snail-shell cottages", "ba nhà vỏ ốc cửa gỗ tròn"),
    "hai_dang": ((657, 3131), "the striped lighthouse on its rocks by the bay", "hải đăng sọc đỏ trắng trên mỏm đá cạnh vịnh"),
    "thac_bac": ((318, 2616), "the silver waterfall and its pool", "thác bạc đổ từ vách đá xuống hồ"),
    "ran_ngoc_trai": ((615, 2242), "the giant clam holding a pearl in a coral lagoon", "sò khổng lồ ngậm ngọc trong đầm san hô"),
    "ho_guong": ((407, 1777), "the round mirror lake ringed with stones", "hồ gương tròn viền đá"),
    "den_rua_co": ((372, 936), "the turtle-shell temple and the stone turtle statue", "đền mái mai rùa và tượng rùa đá"),
    "xoay_nuoc": ((512, 200), "the round rocky basin of deep water where the whirlpool spins (the whirlpool itself is added by the game)",
                  "hồ xoáy: hồ tròn nước xanh sẫm viền đá ở đỉnh đảo (xoáy nước, đinh ba là phần động, không có trong ảnh)"),
}


# ---------- các lượt ----------

def below(col, yl, yr):
    return ("below", col, (yl, yr))


def band(col, tl, tr, bl, br):
    return ("band", col, (tl, tr, bl, br))


def ell(col, *box):
    return ("ell", col, box)


def rect(col, *box):
    return ("rect", col, box)


def poly(col, *pts):
    return ("poly", col, pts)


PLAIN = ("text, letters, numbers, signs with writing; creatures, people, birds, fish; any UI, frame or border; "
         "white sticker outlines")

ARENAS = [
    dict(id="c01", kind="c", spot="bai_bien", place="Seashell Beach", vi="Bãi Vỏ Sò", stages="1–4", hz=380,
         shapes=[below("sea", 380, 380), below("sand", 440, 530), ell("mark", 185, 340, 375, 480)],
         scene="a sunny beach at the water's edge. The turquoise sea fills the far part up to the horizon at y = 380, with small "
               "soft wave lines; a thin band of wet sand and a plain wobbly shoreline run from about y = 440 at the left to y = 530 "
               "at the right, just behind the far platform. Below it, warm pale sand covers the whole ground.",
         landmark="a cluster of giant pastel seashells (a big pink scallop, a cream spiral shell, a small blue shell) on the sand at "
                  "the far left, x 185-375, y 340-480, like the shells of image 2.",
         details="a palm tree leaning in from the far left edge and one from the far right edge (mostly inside the cut strips), a "
                 "few small shells, pebbles, beach-grass tufts, a piece of driftwood near the right edge; two or three fluffy "
                 "clouds in the upper-left and middle sky.",
         plat="both are low round mounds of firm sand ringed with small pebbles and tiny shells.",
         light="bright sunny midday, light from the top-left.",
         leave="foam, breaking waves, sparkles on the water (the game adds small foam and ripples along the shoreline)",
         vi_desc="bãi cát mép nước, biển ngọc lam phía xa, cụm vỏ sò khổng lồ bên trái xa"),
    dict(id="b70a", kind="b", spot="xoay_nuoc", place="Trident Whirlpool", vi="Xoáy Nước Đinh Ba, dạng 1 (Lam Quân)", stages="70",
         hz=330, phase=1,
         shapes=[below("sea", 330, 330), below("rock", 500, 520), rect("stone", 172, 110, 300, 520),
                 rect("stone", 1330, 260, 1536, 560)],
         fx=[("ell", (380, 325, 1140, 475)), ("rect", (715, 140, 805, 380))],
         scene="the boss arena: an ancient sunken stone arena on a rocky reef in the open sea. The dark sea fills the far part up "
               "to the horizon at y = 330; broken ancient stone pillars with wave carvings stand at the far left (x 172-300, "
               "y 110-520) and at the far right edge (x 1330-1536, y 260-560); the ground from about y = 510 down is wet dark rock "
               "and old flagstones with seaweed and puddles.",
         landmark="the great whirlpool basin right behind the arena: a wide oval of deep dark-blue water centred at (760, 400), "
                  "about 760 x 150 px, inside the sea (the pink dashed oval of the sketch). Draw it as plain dark water with a "
                  "few faint curved lines and a soft teal light in its centre, NO spiral.",
         details="small rocks and seaweed along the arena edge, a few broken pillar pieces lying on the ground, puddles that "
                 "mirror the sky.",
         plat_far="a grand raised round dais of carved blue-grey stone: wave carvings on its side face, a gold ring inlaid in its "
                  "top, four small broken stone posts around its rim.",
         plat_near="a flat round slab of wet dark rock with seaweed on its rim.",
         light="the climax of the island: deep blue stormy dusk, heavy slate clouds, a cold teal glow rising from the whirlpool's "
               "centre, rim light on the pillars and the dais. Grand and dramatic, still cute, not horror.",
         effects=["the spinning whirlpool in the pink dashed oval: plain dark water there, no spiral, no foam arms",
                  "a golden trident floating and glowing above the whirlpool's centre: keep the pink dashed box x 715-805, "
                  "y 140-380 plain sky and sea, no trident",
                  "big rolling wave crests and waterspouts along the horizon: draw the far sea with only low wave lines",
                  "storm clouds drifting, rain and lightning in the later phases: plain clouds, no rain, no lightning"],
         leave="a whirlpool spiral, a trident, rain, lightning, foam splashes",
         vi_desc="đấu trường đá cổ trên rạn giữa biển, cột đá vỡ hai bên, hồ xoáy sau lưng boss (để trống cho xoáy và đinh ba), "
                 "hoàng hôn bão xanh thẫm"),
    dict(id="b70b", kind="b2", base="b70a", vi="Xoáy Nước Đinh Ba, dạng 2 (Vạn Quân)", stages="70", phase=2,
         change="phase 2, a storm breaks: thick low grey-violet clouds, the sea darker with taller wave lines and white foam "
                "streaks on the far water, rocks and flagstones shiny wet with more puddles, the teal glow in the whirlpool's centre "
                "stronger. A step darker and bluer overall, but the two platform tops stay light enough for the fighters to stand "
                "out.",
         vi_desc="cùng bố cục dạng 1, bão nổi: mây xám tím thấp, biển sẫm sóng cao, đá ướt bóng"),
    dict(id="b70c", kind="b2", base="b70a", vi="Xoáy Nước Đinh Ba, dạng 3 (Hắc Dực Vạn Quân)", stages="70", phase=3,
         change="phase 3, the final form: a stormy night. Indigo-black sky with heavy clouds lit purple from inside, the sea "
                "near-black blue with glowing teal foam lines, faint teal runes glowing on the dais side and on the pillars, a "
                "strong teal glow from the whirlpool's centre. Image 1 is already a dusk, so go darker but never pitch black: the "
                "teal glow and purple lightning-light keep the flagstones, pillars and rocks readable, and the two platform tops "
                "keep a soft lit blue-grey so the fighters still read clearly.",
         vi_desc="cùng bố cục dạng 1, đêm bão: trời chàm đen mây ánh tím, biển đen bọt ngọc lam phát sáng, phù văn trên bệ, cột"),
    dict(id="m20", kind="m", spot="hai_dang", place="Lighthouse Point", vi="Ngọn Hải Đăng, mini boss (Ma Kết)", stages="20", hz=400,
         shapes=[below("sea", 400, 400), below("rock", 470, 500), below("grass", 530, 550), rect("mark", 200, 20, 360, 430),
                 ell("mark", 172, 400, 470, 500), ell("rock", 1290, 430, 1536, 560)],
         fx=[("ell", (230, 15, 330, 115)), ("ell", (180, 410, 340, 520)), ("ell", (1290, 420, 1450, 540))],
         scene="the lighthouse point at sunset with a storm coming. The rough dark-teal sea fills the far part up to the horizon at "
               "y = 400; dark wet rocks line the shore from about y = 470; the near ground is rock and wind-bent grass.",
         landmark="the striped lighthouse of image 2, now big and grand at the far left: the tower x 200-360 from y 20 down to "
                  "y 430, on a heap of dark rocks (x 172-470, y 400-500); its lamp room at the top (x 240-320, y 25-110) glows "
                  "warm yellow.",
         details="dark boulders on the far right edge (x 1290-1536, y 430-560), coils of rope, an old wooden fence, wind-bent "
                 "beach grass, a broken lobster pot.",
         plat_far="a raised round dais of stacked dark-grey stone with a rusty iron ring set in its top and two short iron mooring "
                  "posts at its back rim.",
         plat_near="a flat round slab of wet dark rock.",
         light="a dramatic sunset: a low orange-pink band of sky along the horizon, heavy violet and slate-blue clouds above, warm "
               "rim light on the left side of every rock and of the tower, cool shadows on the right.",
         effects=["a slowly sweeping light beam from the lamp: keep the sky around the lamp plain, no beam",
                  "waves crashing and spraying on the rocks at the lighthouse foot and at the far right edge (pink dashed "
                  "ovals): draw those rocks with only low wave lines, no foam",
                  "rain streaks and passing cloud shadows: no rain"],
         leave="a light beam, rain, foam splashes",
         vi_desc="mỏm hải đăng lúc hoàng hôn trước bão, hải đăng to bên trái, biển xanh sẫm, mây tím"),
    dict(id="m30", kind="m", spot="thac_bac", place="Silver Falls", vi="Thác Bạc, mini boss (Vây Lam)", stages="30", hz=330,
         shapes=[below("grass", 330, 330), poly("rock", (0, 0), (820, 0), (820, 300), (760, 470), (0, 470)),
                 rect("water", 220, 0, 380, 430), rect("water", 690, 40, 760, 430), ell("water", 172, 395, 760, 485)],
         fx=[("rect", (210, 0, 390, 430)), ("rect", (680, 30, 770, 430)), ("ell", (172, 370, 780, 495)),
             ("ell", (880, 250, 1364, 470))],
         scene="inside the waterfall gorge on a misty morning. Tall grey cliffs with moss and ferns close the back from the left "
               "edge to about x = 820; green slopes and palm trees on the right under the sky; the near ground is wet grass and "
               "flat rocks.",
         landmark="the silver waterfall of image 2, now huge: a broad fall pouring down the cliff at x 220-380 from the top edge, "
                  "and a thinner second fall at x 690-760, on the other side of the far fighter; both fall into one wide round "
                  "plunge pool (x 172-760, y 400-480) ringed with wet rocks.",
         details="ferns, moss and dew on the cliff, round bushes and palms on the right slopes, wet stones along the pool.",
         plat_far="a raised round dais of wet grey stone rising from the edge of the pool, moss and tiny ferns on its rim, a pale "
                  "silver ring inlaid in its top.",
         plat_near="a flat round wet stone with moss at its rim.",
         light="a cool fresh morning: soft silver-blue light, a warm sunbeam from the top-left, dew sparkling on the leaves.",
         effects=["moving water streaks over both falls (pink dashed boxes): paint the falls as smooth silver-white water with "
                  "only a few long vertical lines",
                  "mist rolling along the pool (pink dashed oval): no mist, no foam at the foot of the falls",
                  "a rainbow that fades in over the right slopes (pink dashed oval on the right): keep the sky and slopes there "
                  "plain, no rainbow"],
         leave="mist, foam, spray, a rainbow",
         vi_desc="trong khe thác buổi sáng sương, thác bạc lớn và thác nhỏ hai bên bệ địch, hồ chân thác"),
    dict(id="m40", kind="m", spot="ran_ngoc_trai", place="Pearl Reef", vi="Rạn Ngọc Trai, mini boss (Kuba)", stages="40", hz=390,
         shapes=[below("sea", 390, 390), below("water", 440, 450), ell("mark", 172, 250, 470, 480),
                 ell("rock", 1100, 300, 1300, 450)],
         fx=[("ell", (210, 265, 430, 485))],
         scene="the pearl reef at twilight. The sea reaches the horizon at y = 390 under a violet-blue sky with the first stars "
               "and a thin crescent moon around (620, 90); from about y = 445 down, glowing shallow turquoise water over pale "
               "sand, with coral heads and flat sandbars.",
         landmark="the giant clam of image 2, now big at the far left (x 172-470, y 250-480), wide open on a coral rock, holding a "
                  "big shining pearl centred at (320, 375), about 110 px across; tall pink, orange and purple coral branches "
                  "around it.",
         details="a group of tall coral pillars far on the right (x 1100-1300, y 300-450), round sea rocks, seaweed, small shells "
                 "on the sandbars.",
         plat_far="a raised round table of pink coral rock with a ring of small white pearls set around its top.",
         plat_near="a flat round sandbar just above the shallow water, rimmed with small coral pebbles.",
         light="magical twilight: the pearl and the shallow water give a soft cyan-pink glow, everything else cool violet-blue, "
               "the coral rims lit pink.",
         effects=["a pulsing glow around the pearl (pink dashed oval): draw the pearl bright, keep about 60 px around it plain",
                  "bubbles rising from the water and sparkles on it: calm flat water, no bubbles, no sparkle stars"],
         leave="bubbles, sparkle stars, a glow halo",
         vi_desc="rạn ngọc lúc chạng vạng, sò khổng lồ ngậm ngọc to bên trái, nước nông ngọc lam phát sáng"),
    dict(id="m50", kind="m", spot="ho_guong", place="Mirror Lake", vi="Hồ Gương, mini boss (Thương Lam)", stages="50", hz=360,
         shapes=[below("grass", 300, 340), below("water", 360, 360), ell("rock", -60, 880, 330, 1100), ell("mark", 255, 45, 405, 195)],
         fx=[("ell", (330, 600, 710, 800))],
         scene="the mirror lake at night. Dark-blue hills far behind (tops at y 300-360); the perfectly still lake covers the whole "
               "ground from y = 360 to the bottom edge; smooth round stones line the far bank and gather in the bottom-left corner. "
               "The two platforms stand in the water.",
         landmark="the mirror lake of image 2 under a big full moon at the upper left (the light-grey disc of the sketch, centre "
                  "(330, 120), about 150 px across) with a few soft clouds; the water mirrors the moon as a soft column of light "
                  "below it and reflects the stars.",
         details="a few water lilies and reeds near the edges, smooth stones half in the water.",
         plat_far="a raised round dais of pale smooth stone standing in the water, a thin silver ring inlaid in its top.",
         plat_near="a big flat round stone just above the water.",
         light="calm, silvery and magical: deep blue sky with many small stars, cool moonlight from the top-left, pale silver rims "
               "on the stones and platforms.",
         effects=["mirror reflections of the two fighters in the water below each platform (pink dashed oval below the far "
                  "platform, and below the near one): keep the water there smooth and plain",
                  "fireflies, ripple rings and shimmer on the moon's reflection: no glowing dots, no ripple rings"],
         leave="fireflies, ripple rings, reflections of creatures",
         vi_desc="hồ gương ban đêm, trăng tròn to bên trái trên, hai bệ đứng trong nước phẳng như gương"),
    dict(id="m60", kind="m", spot="den_rua_co", place="Old Turtle Temple", vi="Đền Rùa Cổ, mini boss (Huyền Vũ)", stages="60",
         hz=460,
         shapes=[below("grass", 250, 300), below("stone", 460, 460), rect("mark", 172, 40, 600, 460),
                 ell("mark", 1080, 280, 1340, 470)],
         fx=[("rect", (240, 290, 340, 440)), ("ell", (286, 461, 756, 597))],
         scene="the ancient turtle temple at dusk, wrapped in a faint green spirit mist. Tall dark jungle trees with big leaves "
               "frame the sky; the courtyard of carved flagstones fills the ground from its far edge at about y = 460.",
         landmark="the temple of image 2, now big and grand at the far left (x 172-600, y 40-460): a huge dome shaped like a "
                  "turtle shell with hexagon plates, moss and vines, stone columns, wide steps, and a dark arched doorway at "
                  "x 240-340, y 290-440 that glows soft teal from inside; and a giant stone turtle statue at the far right "
                  "(x 1080-1340, y 280-470) with closed eyes.",
         details="stone lanterns, broken low walls, vines, ferns, moss between the flagstones.",
         plat_far="a raised round stone dais carved with a faint hexagon turtle-shell pattern on its top and wave carvings on its "
                  "side face.",
         plat_near="a round circle of flat carved flagstones.",
         light="mysterious dusk: teal and violet sky, the ancient stone grey-green, a soft teal glow from the doorway, cool "
               "shadows.",
         effects=["a glowing rune ring that lights up on the dais top (pink dashed oval): keep the top plain stone with only "
                  "faint carved hexagons",
                  "the doorway glow and the statue's eyes that pulse and open: keep the statue's eyes closed",
                  "rising spirit motes and falling leaves: no glowing dots, no leaves in the air"],
         leave="glowing runes, glowing dots, leaves in the air",
         vi_desc="đền rùa cổ lúc chạng vạng có sương xanh, đền mái mai rùa to bên trái, tượng rùa đá to bên phải"),
    dict(id="fxm", kind="fx", grid="4x3", base="c01", vi="Sheet hiệu ứng mini boss", stages="20–60",
         items=["a long cone of lighthouse light: a narrow rounded end at the left, widening to the right edge of the cell; solid "
                "pale warm yellow with yellow pencil hatching and a thin ink outline only along its two long sides",
                "a half-circle rainbow of five soft pencil-hatched bands, no ink outline",
                "three tall thin wavy streaks of falling white water side by side, with a few short blue ink lines",
                "a soft round puff of white mist with very pale blue hatching and a faint thin outline",
                "a round soft glow: a pale pink-white disc with short rays all around it, no ink",
                "one round water bubble with a white highlight and a thin blue ink outline",
                "a cluster of five small water bubbles of different sizes",
                "a glowing firefly: a small yellow-green dot inside a soft round pale-green halo",
                "a horizontal streak of moonlight on water: short broken white-yellow lines stacked in a narrow band",
                "a flat ripple ring on water seen at a low angle: a wide thin white ellipse with a thin blue ink edge",
                "a glowing teal rune circle seen at a low angle (a wide flat ellipse): a hexagon turtle-shell pattern and small "
                "dots inside a double ring, pale glowing teal",
                "a pale green spirit wisp: a small glowing flame-like curl rising upward"],
         vi_desc="12 món: tia đèn hải đăng, cầu vồng, vệt thác, sương, quầng sáng ngọc, bong bóng, chùm bong bóng, đom đóm, "
                 "vệt trăng trên nước, gợn tròn, vòng phù văn, đốm hồn"),
    dict(id="fxb", kind="fx", grid="3x2", base="b70a", vi="Sheet hiệu ứng boss 70", stages="70",
         items=["a huge whirlpool spiral seen from straight above, perfectly round, about 420 px across: deep blue to teal spiral "
                "arms with white foam lines curling into a dark centre (the game squashes it flat and spins it)",
                "a golden trident standing upright, about 420 px tall: three ornate prongs, a teal gem in its middle, thick ink "
                "outline, pencil shading, no glow",
                "a tall lightning bolt: a zigzag with two small branches, white-yellow core, a pale purple edge, ink outline",
                "a wide dark storm cloud: lumpy top, flat bottom, purple-grey with darker pencil hatching",
                "a tall waterspout: a twisting column of water from a foamy base up to a cloud-like tip, tapered in the middle",
                "a big curling wave crest with white foam, wider than tall"],
         vi_desc="6 món lớn: xoáy nước nhìn từ trên, đinh ba vàng, tia sét, mây bão, vòi rồng nước, ngọn sóng cuộn"),
    dict(id="c02", kind="c", spot="vung_san_ho", place="Coral Pool", vi="Vũng San Hô", stages="5–9", hz=370,
         shapes=[below("sea", 370, 370), below("rock", 405, 425), below("sand", 440, 455), ell("mark", 180, 330, 500, 480),
                 ell("water", 205, 395, 475, 470), ell("water", 1130, 520, 1340, 580), ell("water", 1220, 700, 1430, 760)],
         scene="a rocky shore with tide pools. The far sea reaches the horizon at y = 370 behind a line of low dark-grey rocks "
               "(y 405-440); the ground is warm sand with flat grey rock shelves.",
         landmark="the big coral tide pool of image 2 at the far left (x 180-500, y 330-480): a round pool of clear turquoise water "
                  "ringed with rounded grey rocks, pink and orange coral branches rising from it.",
         details="two small shallow pools on the right side of the ground (light-blue ovals of the sketch), seaweed, barnacled "
                 "rocks, small shells; a tall rock with a palm tree at the far right edge, mostly in the cut strip.",
         plat="both are flat round slabs of pale grey rock, wet and a little darker at the rim, a few barnacles on the rim.",
         light="late-morning sun, light from the top-left.",
         leave="foam, sparkles, ripples",
         vi_desc="bờ đá có vũng nước, vũng san hô lớn bên trái xa, biển phía sau"),
    dict(id="c03", kind="c", spot="cau_go_reu", place="Mossy Bridge", vi="Cầu Gỗ Rêu", stages="10–14", hz=360,
         shapes=[below("grass", 360, 360), band("water", 400, 470, 450, 520), ell("mark", 190, 330, 450, 470)],
         scene="a grassy stream bank. Rolling turquoise-green hills and palm trees far away along the horizon (y = 360). A calm "
               "stream about 50 px wide runs across the whole scene from the left edge (y 400-450) to the right edge "
               "(y 470-520), just behind the far platform; the far platform stands on the near bank.",
         landmark="the mossy wooden bridge of image 2 crossing the stream at the far left (x 190-450, y 330-470): thick wooden "
                  "planks, round posts, moss on the rails, seen from the side at an angle.",
         details="ferns, round bushes and mossy rocks along both banks, a lantern on a wooden post on the far bank at the right, "
                 "grass tufts.",
         plat="both are flat round mossy stone slabs set in the grass.",
         light="sunny afternoon, light from the top-left.",
         leave="foam, ripples, sparkles on the stream (the game adds ripples running along it)",
         vi_desc="bờ suối cỏ, suối chảy ngang sau bệ địch, cầu gỗ rêu bên trái xa"),
    dict(id="c04", kind="c", spot="lang_vo_oc", place="Shell Village", vi="Làng Vỏ Ốc", stages="15–19", hz=370,
         shapes=[below("sand", 370, 370), ell("mark", 180, 220, 400, 470), ell("mark", 690, 310, 810, 420),
                 ell("mark", 1170, 290, 1364, 430)],
         scene="the little square of a seaside village. Palm trees and far cottage roofs along the horizon (y = 370); the ground "
               "is packed warm sand with turquoise grass patches.",
         landmark="the snail-shell cottages of image 2: a big one at the far left (x 180-400, y 220-470), a small one far in the "
                  "middle (x 690-810, y 310-420) and a third one at the right (x 1170-1364, y 290-430), pastel spiral shells with "
                  "round wooden doors and little round windows.",
         details="lanterns on wooden posts, a fishing net hung between two poles, wooden crates, a small rowboat on the sand at the "
                 "right edge, round bushes.",
         plat="both are round plazas of packed light sand edged with a ring of flat round pebbles.",
         light="warm afternoon, light from the top-left.",
         leave="smoke, sparkles",
         vi_desc="quảng trường làng ven biển, nhà vỏ ốc bên trái xa, giữa xa, bên phải"),
    dict(id="c05", kind="c", spot="hai_dang", place="Lighthouse Point", vi="Ngọn Hải Đăng", stages="21–29", hz=390,
         shapes=[below("sea", 390, 390), below("rock", 455, 460), below("grass", 480, 485), rect("mark", 210, 100, 330, 420),
                 ell("mark", 175, 390, 420, 480)],
         scene="a grassy rocky headland by the sea on a fine day. The sea fills the far part up to the horizon at y = 390, with a "
               "small rocky islet far on the right; the land comes up to about y = 470 with a rocky edge.",
         landmark="the striped lighthouse of image 2 on a heap of grey rocks at the far left: the tower x 210-330, y 100-420, the "
                  "rocks x 175-420, y 390-480; seen from the side, medium size.",
         details="grey boulders and round bushes along the cliff edge, beach grass, a wooden fence of three posts, a coil of rope.",
         plat="both are flat round slabs of grey rock with a little moss.",
         light="fine sunny day, light from the top-left.",
         leave="foam, spray, breaking waves, a light beam",
         vi_desc="mỏm đá cỏ ven biển ngày đẹp, hải đăng vừa phải bên trái xa"),
    dict(id="c06", kind="c", spot="thac_bac", place="Silver Falls", vi="Thác Bạc", stages="31–39", hz=330,
         shapes=[below("grass", 330, 330), poly("rock", (0, 60), (172, 100), (560, 300), (560, 470), (0, 470)),
                 rect("water", 210, 110, 330, 420), ell("water", 180, 400, 560, 475), band("water", 455, 470, 480, 500)],
         scene="a lush glen at the foot of tall cliffs. A tall rocky cliff closes the far left (x 172-560, its top from y 100 at "
               "the left down to y 300 at x 560); green hills and palm trees on the right under the sky (above y = 330).",
         landmark="the silver waterfall of image 2 pouring down the cliff at x 210-330 from y 110 into a round pool at its foot "
                  "(x 180-560, y 400-475) ringed with grey rocks.",
         details="ferns, moss, round bushes, wet rocks; a small stream leaves the pool towards the right edge behind the far "
                 "platform.",
         plat="both are flat round wet stones with moss at the rim.",
         light="bright fresh day, light from the top-left.",
         leave="foam, mist, spray at the foot of the fall, a rainbow",
         vi_desc="thung lũng dưới vách đá, thác bạc vừa phải bên trái xa đổ xuống hồ"),
    dict(id="c07", kind="c", spot="ran_ngoc_trai", place="Pearl Reef", vi="Rạn Ngọc Trai", stages="41–49", hz=380,
         shapes=[below("sea", 380, 380), below("water", 430, 440), ell("mark", 185, 320, 420, 470)],
         scene="a shallow lagoon over a coral reef on a sunny day. The sea reaches the horizon at y = 380; from about y = 435 down, "
               "clear shallow turquoise water over pale sand, with coral heads and flat sandbars.",
         landmark="the giant open clam of image 2 holding a big shining pearl, at the far left (x 185-420, y 320-470), on a coral "
                  "rock, pink and orange corals around it.",
         details="coral heads, round sea rocks, seaweed, sandbars with small shells.",
         plat="both are round flat sandbars rising just above the shallow water, rimmed with small coral pebbles.",
         light="bright sunny day, light from the top-left.",
         leave="bubbles, sparkle stars, ripples",
         vi_desc="đầm nước nông trên rạn san hô, sò khổng lồ ngậm ngọc bên trái xa"),
    dict(id="c08", kind="c", spot="ho_guong", place="Mirror Lake", vi="Hồ Gương", stages="51–59", hz=330,
         shapes=[below("grass", 330, 330), band("water", 380, 380, 475, 475)],
         scene="the shore of a perfectly still lake. Soft green hills and a few palm trees far behind (y 330-380); the lake fills "
               "the middle distance from y = 380 to y = 475 like a mirror, reflecting the sky and the hills; smooth round grey "
               "stones line its banks; the near ground is soft turquoise grass.",
         landmark="the mirror lake of image 2: very still pale-blue water with a few long light reflection strokes, ringed by "
                  "smooth rounded stones.",
         details="water lilies near the bank, reeds, smooth stones in the grass, small flowers.",
         plat="both are big flat round smooth stones set in the grass.",
         light="calm clear day, light from the top-left.",
         leave="ripples, sparkle stars",
         vi_desc="bờ hồ gương ngày lặng, hồ phẳng như gương sau bệ địch"),
    dict(id="c09", kind="c", spot="den_rua_co", place="Old Turtle Temple", vi="Đền Rùa Cổ", stages="61–69", hz=450,
         shapes=[below("grass", 300, 330), below("stone", 450, 450), ell("mark", 180, 150, 430, 460),
                 ell("mark", 1150, 300, 1350, 470)],
         scene="the mossy flagstone courtyard of an ancient jungle temple. Tall jungle trees and big leaves behind; the far edge "
               "of the courtyard is at about y = 450.",
         landmark="the old stone temple of image 2 at the far left (x 180-430, y 150-460): a dome shaped like a turtle shell with "
                  "hexagon plates and moss, a dark arched doorway, stone steps; and the stone turtle statue of image 2 at the far "
                  "right (x 1150-1350, y 300-470).",
         details="vines, ferns, stone lanterns, broken low walls, moss between the flagstones.",
         plat="both are round circles of flat carved flagstones.",
         light="warm late afternoon, light from the top-left.",
         leave="glowing runes, leaves in the air",
         vi_desc="sân đá đền cổ trong rừng, đền mái mai rùa bên trái xa, tượng rùa đá bên phải"),
]
BY_ID = {a["id"]: a for a in ARENAS}
KIND_VI = {"c": "thường", "m": "mini boss", "b": "boss", "b2": "boss", "fx": "phần động"}


def approved(i):
    return WORK / f"{i}.png"


def needs(a):
    if a["id"] == "c01":
        return []
    out = ["c01"]
    if a.get("base") and a["base"] != "c01":
        out.append(a["base"])
    return out


def ready(a):
    return all(approved(n).exists() for n in needs(a))


# ---------- ảnh mẫu ----------

def make_refs():
    if not MAP.exists():
        print(f"  ! thiếu bản đồ {MAP}")
        return
    REFS.mkdir(parents=True, exist_ok=True)
    im = Image.open(MAP).convert("RGB")
    for name, (c, _, _) in SPOTS.items():
        if len(c) == 4:
            box = c
        else:
            x0 = min(max(c[0] - 256, 0), im.width - 512)
            y0 = min(max(c[1] - 256, 0), im.height - 512)
            box = (x0, y0, x0 + 512, y0 + 512)
        im.crop(box).save(REFS / f"{name}.png")


def size_of(p):
    try:
        with Image.open(p) as im:
            return im.size
    except OSError:
        return None


def ref_list(a):
    """[(đường dẫn, câu cho GPT, câu cho người dùng)] theo thứ tự ảnh"""
    k = a["kind"]
    bo = PACK / f"bo_cuc_{a.get('base', a['id']) if k == 'b2' else a['id']}.png"
    bo_en = "the layout sketch of the image you draw now: follow it exactly"
    if k == "fx":
        base = a["base"]
        return [(approved(base), "an approved battle background of this game: copy its RENDERING (ink, pencil hatching, colours); "
                                 "ignore its content",
                 f"nền trận {BY_ID[base]['vi']} đã duyệt (1536 × 1024, nền đặc): lấy nét"),
                (GRIDS[a["grid"]], f"the numbered {a['grid'].replace('x', ' x ')} grid: one object per cell, in number order",
                 f"lưới {a['grid'].replace('x', ' × ')} đánh số (1536 × 1024, nền trắng, ô viền hồng, số hồng ở góc): mỗi ô một món")]
    if k == "b2":
        return [(approved(a["base"]), "phase 1 of this boss arena, already approved: redraw this same image",
                 f"nền boss dạng 1 đã duyệt (1536 × 1024, nền đặc): vẽ lại đúng bố cục"),
                (bo, "the layout sketch of this arena (the same for all three phases)",
                 "bố cục nền boss 70 (1536 × 1024) như lượt dạng 1")]
    spot_en, spot_vi = SPOTS[a["spot"]][1], SPOTS[a["spot"]][2]
    sz = size_of(REFS / f"{a['spot']}.png") or (512, 512)
    spot = (REFS / f"{a['spot']}.png",
            f"a crop of this island's map, seen from above, showing {spot_en}: draw the same landmark here, seen from the side, "
            f"with its colours and shapes",
            f"mảnh cắt bản đồ đảo Thủy 70 ải ({sz[0]} × {sz[1]}, nhìn từ trên xuống, đất ngọc lam gạch chì): {spot_vi}")
    if a["id"] == "c01":
        first = (WORLD, "the game's approved hand-drawn world map: copy its RENDERING (wobbly dark-brown ink outlines, "
                        "coloured-pencil hatching on cream paper, chunky cute doodles); ignore its content",
                 "ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền biển xanh đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu; lấy nét, "
                 "không lấy nội dung")
    else:
        copy = ("copy its rendering, colours, perspective, platform look and brightness; not its content" if k == "c" else
                "copy its rendering, perspective and platform look; not its content, colours or daylight (this stage has its own "
                "light)")
        first = (approved("c01"), f"the approved battle background of this island (a normal stage): {copy}",
                 "nền trận Bãi Vỏ Sò đã duyệt (1536 × 1024, nền đặc): lấy nét, góc nhìn, kiểu bệ, độ sáng")
    out = [first, spot]
    if k in ("m", "b"):
        out.append((DAIS, "the island map's boss plate: a raised round dais with a flat top, a visible side face and a ring on "
                          "its top; copy only this idea for the far platform, in the material described below",
                    "bệ boss của bản đồ đảo (400 × 250, nền trong suốt): đĩa cát dày có mặt bên, vòng vàng trên mặt, đá viền"))
    out.append((bo, bo_en, f"bố cục lượt này (1536 × 1024): {sketch_vi(a)}"))
    return out


# ---------- bố cục ----------

def wavy(yl, yr, ph=0.0, amp=6):
    return [(x, yl + (yr - yl) * x / W + amp * math.sin(x / 60 + ph)) for x in range(0, W + 1, 16)]


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


def draw_plat(d, cx, cy, w, h, side=0):
    if side:
        d.ellipse((cx - w / 2, cy - h / 2 + side, cx + w / 2, cy + h / 2 + side), fill=(205, 170, 120), outline=INK, width=6)
        d.rectangle((cx - w / 2, cy, cx + w / 2, cy + side), fill=(205, 170, 120))
        d.line([(cx - w / 2, cy), (cx - w / 2, cy + side)], fill=INK, width=6)
        d.line([(cx + w / 2, cy), (cx + w / 2, cy + side)], fill=INK, width=6)
    d.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(252, 244, 214), outline=INK, width=6)
    if side:
        d.ellipse((cx - w / 2 + 34, cy - h / 2 + 12, cx + w / 2 - 34, cy + h / 2 - 12), outline=(236, 186, 58), width=6)


def overlay_frame(im):
    """bảng máu (gạch chéo xám), dải bị cắt (tối)"""
    for (x0, y0, x1, y1) in PANELS:
        layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        hgt = y1 - y0
        for k in range(-hgt, x1 - x0, 22):
            ld.line([(k, hgt), (k + hgt, 0)], fill=(90, 90, 90, 200), width=4)
        im.alpha_composite(layer, (x0, y0))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rectangle((0, 0, X0, H), fill=(20, 20, 30, 120))
    sd.rectangle((X1, 0, W, H), fill=(20, 20, 30, 120))
    im.alpha_composite(shade)


def draw_sketch(a):
    im = Image.new("RGBA", (W, H), COL["sky"] + (255,))
    d = ImageDraw.Draw(im)
    for i, (kind, col, g) in enumerate(a["shapes"]):
        fill = COL[col]
        if kind == "below":
            line = wavy(g[0], g[1], i)
            d.polygon(line + [(W, H), (0, H)], fill=fill)
            d.line(line, fill=INK, width=4)
        elif kind == "band":
            top, bot = wavy(g[0], g[1], i), wavy(g[2], g[3], i + 1)
            d.polygon(top + bot[::-1], fill=fill)
            d.line(top, fill=INK, width=4)
            d.line(bot, fill=INK, width=4)
        elif kind == "ell":
            d.ellipse(g, fill=fill, outline=INK, width=4)
        elif kind == "rect":
            d.rectangle(g, fill=fill, outline=INK, width=4)
        elif kind == "poly":
            d.polygon(list(g), fill=fill, outline=INK, width=4)
    boss = a["kind"] in ("m", "b")
    if boss:
        cx, cy, w, h, side = FOE_DAIS
        draw_plat(d, cx, cy, w, h, side)
    else:
        draw_plat(d, *FOE_PLAT)
    draw_plat(d, *ME_PLAT)
    for kind, box in a.get("fx", []):
        (dashed_ellipse if kind == "ell" else dashed_rect)(d, box, (240, 40, 200))
    dashed_rect(d, FOE_BOX, (255, 255, 255), 4, 20)
    dashed_rect(d, ME_BOX, (255, 255, 255), 4, 20)
    overlay_frame(im)
    return im.convert("RGB")


def sketch_vi(a):
    if a["kind"] == "b2":
        a = BY_ID[a["base"]]
    cols = []
    for _, c, _ in a["shapes"]:
        if c not in cols:
            cols.append(c)
    parts = [LEGEND_VI["sky"]] + [LEGEND_VI[c] for c in cols if c != "sky"]
    parts.append("hai bầu dục kem viền mực là hai bệ" + (" (bệ địch là bệ nổi có mặt bên và vòng vàng)" if a["kind"] in ("m", "b") else ""))
    if a.get("fx"):
        parts.append("nét đứt hồng là chỗ để trống cho phần động")
    parts += ["khung trắng nét đứt là thân hai tướng", "gạch chéo xám là chỗ bảng máu che", "hai dải tối hai bên bị cắt trên máy"]
    return "; ".join(parts)


def sketch_en(a):
    cols = []
    for _, c, _ in a["shapes"]:
        if c not in cols:
            cols.append(c)
    parts = [LEGEND["sky"]] + [LEGEND[c] for c in cols if c != "sky"]
    parts.append("cream ovals with a thick ink edge = the two platforms" +
                 (" (the far one drawn as a raised dais with a side face and a gold ring)" if a["kind"] in ("m", "b") else ""))
    if a.get("fx"):
        parts.append("pink dashed outlines = places to keep plain for the game's moving effects (see EFFECTS)")
    parts += ["white dashed boxes = the fighters' bodies", "grey diagonal lines = covered by the game's panels",
              "dark side strips = cut off on phones"]
    return "; ".join(parts)


# ---------- file prompt ----------

def head(refs):
    out = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save "
           "it as described under SAVE. Do not reply with text only.", "",
           "REFERENCE IMAGES (open each file from its full path):"]
    for i, (p, en, _) in enumerate(refs):
        sz = size_of(p) if p.exists() else ((W, H) if p.name.startswith("bo_cuc") else None)
        dim = f" ({sz[0]} x {sz[1]})" if sz else ""
        out.append(f"image {i + 1} = {p}{dim}: {en}")
    return out


def save_block(a, w=W, h=H):
    p = INBOX / f"{a['id']}.png"
    return ["", f"SAVE: save the finished image as a {w} x {h} PNG to", str(p),
            f"Create the folder if it is missing. If that file already exists, save it as {a['id']}_2.png, {a['id']}_3.png … in the "
            f"same folder instead. Do not change, move or delete any other file."]


def frame_text(n_sketch):
    fx, fy = FOE_PLAT[0], FOE_PLAT[1]
    return [
        "",
        f"FRAME: phones show only the middle {X1 - X0} x {H} of your {W} x {H} image; the dark strips of the sketch (x < {X0} and "
        f"x > {X1}) are cut off, so just continue the scene into them with nothing important there.",
        "",
        "VIEW: a side three-quarter view like a stage in a picture book: eye level a little above the fighters' heads, looking "
        "slightly down; the ground rises towards the horizon and things get smaller with distance. Not a top-down map.",
        "",
        f"LAYOUT: follow image {n_sketch} exactly. It is only a colour-coded plan: {{legend}}. Do not copy its flat colours, its "
        f"grey diagonal lines, its dashed lines or its dark side strips.",
        "",
        f"FIGHTERS: the far fighter is up to about 390 px tall (white dashed box x {FOE_BOX[0]}-{FOE_BOX[2]}, y {FOE_BOX[1]}-"
        f"{FOE_BOX[3]}), the near one up to about 430 px (box x {ME_BOX[0]}-{ME_BOX[2]}, y {ME_BOX[1]}-{ME_BOX[3]}). Right behind "
        f"their bodies keep only calm sky, water, rock or ground: no tall object, bright spot or busy pattern. Keep the diagonal "
        f"between the two platforms open and calm (flat ground or water, a few small tufts): the fighters lunge across it.",
        "",
        f"PANELS: the game covers the top-right (x {PANELS[0][0]}-{PANELS[0][2]}, y {PANELS[0][1]}-{PANELS[0][3]}) and the "
        f"bottom-left (x {PANELS[1][0]}-{PANELS[1][2]}, y {PANELS[1][1]}-{PANELS[1][3]}) with name-and-health panels (grey "
        f"diagonal lines in the sketch). Draw only plain sky, water or ground there: no landmark, no tree top, no bright spot.",
    ]


def platforms_text(a):
    mx, my, mw, mh = ME_PLAT
    near = (f"the near one centred at ({mx}, {my}), about {mw} x {mh} px, its bottom edge about {H - my - mh // 2} px above the "
            f"image bottom")
    if a["kind"] in ("m", "b"):
        cx, cy, w, h, side = FOE_DAIS
        far = (f"the far one is a raised boss dais: its flat top centred at ({cx}, {cy}), about {w} x {h} px, with a side face "
               f"about {side} px tall below it")
        mat = f"Far dais: {a['plat_far']} Near platform: {a['plat_near']}"
    else:
        cx, cy, w, h = FOE_PLAT
        far = f"the far one centred at ({cx}, {cy}), about {w} x {h} px"
        mat = f"Material: {a['plat']}"
    return ["", f"PLATFORMS: exactly where the sketch has them, same centre and size: {far}; {near}. Their tops are flat, level, "
                f"EMPTY and a little lighter than the ground around them, with a crayon-hatched rim and a soft contact shadow; "
                f"nothing stands on them. {mat}"]


def rendering_text(a):
    if a["id"] == "c01":
        return ["", "RENDERING: copy image 1's rendering: wobbly dark-brown ink outlines (#2B2118), coloured-pencil hatching on "
                    "cream paper, flat warm colours with light watercolour washes, chunky cute doodle shapes with clear "
                    "silhouettes. Ink about 6 px on near things and 3-4 px on far things. Use the colours and the look of the "
                    "objects of image 2 (pale turquoise hatched grass, warm sand, grey rocks, palm trees, pastel shells). Not 3D, "
                    "not glossy, no realistic rendering, no tiny noisy details.",
                "",
                "CONTRAST: the fighters must stand out, so the background is a little softer and lighter than image 2, with the "
                "most detail and contrast on the far landmark and along the left and right edges; the middle stays simple."]
    return ["", "RENDERING: exactly as image 1 (the approved battle background of this island): the same ink, hatching, paper, "
                "perspective, platform size and look. Draw the landmark like image 2 (the same landmark on the "
                "island map, seen from above there; draw it from the side here, much bigger). Not 3D, not glossy, no tiny noisy "
                "details. The fighters must stand out: most detail and contrast on the landmark and along the left and right "
                "edges; the middle stays simple."]


def arena_prompt(a):
    refs = ref_list(a)
    k = a["kind"]
    lines = head(refs) + save_block(a)
    if k == "c":
        what = (f"the battle background for the stages at {a['place']} (stages {a['stages']}) of the Water island, in a vertical "
                f"mobile monster-battle game. Two fighters (cut-out stickers with a white paper border, added by the game) fight "
                f"on it: the enemy on the smaller far platform at the upper left, the player's fighter on the bigger near platform "
                f"at the lower right.")
    else:
        what = (f"the battle background for the {'mini-boss' if k == 'm' else 'final boss'} stage at {a['place']} (stage "
                f"{a['stages']}) of the Water island, in a vertical mobile monster-battle game. Two fighters (cut-out stickers with "
                f"a white paper border, added by the game) fight on it: the boss on the far raised dais at the upper left, the "
                f"player's fighter on the bigger near platform at the lower right.")
    lines += ["", f"WHAT THIS IS: {what}", "", f"Draw a {W} x {H} image."]
    if k == "m":
        lines += ["", "THIS IS A MINI-BOSS STAGE, so it must look special: more dramatic and richer than the normal stages of this "
                      "place, but still cute and cosy, never scary. Closer to the landmark, which is big and grand; a strong time "
                      "of day and weather; richer details along the left and right edges; the far platform is a raised boss dais "
                      "(the idea of image 3, built from the material below)."]
    if k == "b":
        lines += ["", "THIS IS THE ISLAND'S FINAL BOSS STAGE: the most spectacular background of the island, grand, stormy and "
                      "magical, but still cute and cosy, never scary. The boss evolves twice during this battle and the game "
                      "then switches to darker versions of this same image (drawn later from yours), so keep every shape clear "
                      "and simple to redraw. The far platform is a grand raised boss dais (the idea of image 3, built from the "
                      "material below)."]
    lines += rendering_text(a)
    lines += [s.replace("{legend}", sketch_en(a)) for s in frame_text(len(refs))]
    lines += ["", f"SCENE: {a['scene']}", "", f"LANDMARK: {a['landmark']}", "", f"DETAILS: {a['details']}"]
    lines += platforms_text(a)
    lines += ["", f"LIGHT: {a['light']}"]
    if a.get("effects"):
        lines += ["", "EFFECTS: the game animates these on top of your image, so leave their places as described and do NOT draw "
                      "them:"] + [f"- {e};" for e in a["effects"]]
    lines += ["", f"Do not draw: {PLAIN}; {a['leave']}.", "", f"Remember: save the image to {INBOX / (a['id'] + '.png')}"]
    return "\n".join(lines) + "\n"


def phase_prompt(a):
    refs = ref_list(a)
    base = BY_ID[a["base"]]
    lines = head(refs) + save_block(a)
    lines += ["",
              f"WHAT THIS IS: phase {a['phase']} of 3 of the final boss battle background at {base['place']} (stage 70) of the "
              f"Water island, in a vertical mobile monster-battle game. The boss evolves during the battle and the game switches "
              f"from image 1 to your image in a white flash, so both must line up.",
              "",
              f"Redraw image 1 as a {W} x {H} image with every shape in exactly the same place and size: the horizon, the "
              f"pillars, the whirlpool oval, the trident's empty spot, the far dais and the near platform (image 2 is the layout "
              f"they follow). Same rendering: the same ink, pencil hatching and paper. Change only the weather and the light:",
              "",
              f"{a['change']}",
              "",
              "Keep the panel areas (top-right x 815-1364, y 0-240; bottom-left x 185-720, y 760-960) plain, the platform tops "
              "empty, and the places of the game's moving effects plain: the whirlpool oval (plain dark water, no spiral), the "
              "trident's spot (x 715-805, y 140-380), the sky (no lightning) and the air (no rain).",
              "",
              f"Do not draw: {PLAIN}; {base['leave']}.",
              "",
              f"Remember: save the image to {INBOX / (a['id'] + '.png')}"]
    return "\n".join(lines) + "\n"


def fx_prompt(a):
    refs = ref_list(a)
    rows, cols = (3, 4) if a["grid"] == "4x3" else (2, 3)
    cw, ch = W // cols, H // rows
    lines = head(refs) + save_block(a)
    lines += ["",
              f"WHAT THIS IS: a sprite sheet of {len(a['items'])} separate effect objects for the "
              f"{'mini-boss' if a['grid'] == '4x3' else 'final boss'} battle backgrounds of a vertical mobile game. The game cuts "
              f"the sheet into {len(a['items'])} sprites and animates them (moves, spins, fades, scales, makes them see-through), "
              f"so draw each object complete and on its own.",
              "",
              f"Draw a {W} x {H} image with a fully TRANSPARENT background (PNG with alpha), in the rendering of image 1 (same "
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
    return {"fx": fx_prompt, "b2": phase_prompt}.get(a["kind"], arena_prompt)(a)


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
        rows.append(f"| {n}. {a['vi']}; ải {a['stages']}, {KIND_VI[a['kind']]}: {a['vi_desc']} | {file} | {refs} | "
                    f"`{INBOX / (a['id'] + '.png')}` |")
    return f"""# Gói gửi GPT: sàn đấu đảo Thủy 70 ải (`thuy`)

Sinh bằng `{HERE / 'build_thuy.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè). Nền trận cho 70 ải đảo Thủy:
- **9 nền thường**, mỗi chặng một nền theo địa danh của chặng (ải xen giữa dùng nền của chặng mình), cảnh ban ngày, địa danh nhỏ ở xa bên trái.
- **5 nền mini boss** (ải 20, 30, 40, 50, 60): gần địa danh hơn, địa danh to, giờ và thời tiết mạnh (hoàng hôn bão, sương sớm, chạng vạng, đêm trăng, sương hồn), bệ địch là bệ nổi; chừa chỗ cho phần động.
- **Boss ải 70**: 3 bản cùng bố cục theo 3 dạng tiến hóa (hoàng hôn bão, bão nổi, đêm bão), game đổi nền lúc chớp sáng tiến hóa; xoáy nước, đinh ba, sét, mưa, sóng là phần động.
- **2 sheet phần động** (nền trong suốt) cho mini boss và boss.

GPT vẽ 1536 × 1024; game lấy khúc giữa 1192 × 1024 (bỏ 172 px mỗi bên) thu về khung sân 1080 × 928.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Làm lượt 1 trước (chốt nét): GPT lưu xong thì nhắn Claude "duyệt c01"; Claude soi, lưu bản duyệt và dựng file prompt các lượt sau. Lượt 3, 4, 11 cần thêm nền boss dạng 1 (`b70a`) đã duyệt. Nên làm mọi lượt trong cùng một chat để GPT giữ nét.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
{chr(10).join(rows)}

Bản duyệt Claude lưu ở `{WORK}\\<mã>.png`, kèm ảnh soi khung `soi_<mã>.png` (vẽ lại hai chỗ đứng, bảng máu, dải bị cắt lên ảnh để đo).

## Soi trước khi nhắn Claude

- Hai bệ đúng chỗ như bố cục (bệ xa trên trái, bệ gần to dưới phải); mặt bệ **trống**.
- Giữa hai bệ thoáng; ngay sau lưng hai tướng (khung trắng nét đứt) không có vật cao, chỗ sáng.
- Góc trên phải và dưới trái (gạch chéo xám) chỉ có trời, nước, đất: bảng máu che chỗ đó.
- Địa danh giống bản đồ đảo, đúng chỗ (thường ở bên trái xa).
- Mini boss, boss: rõ là ải đặc biệt (giờ, thời tiết, địa danh to, bệ địch nổi có mặt bên) mà vẫn dễ thương, không đáng sợ.
- **Không vẽ phần động** file đã dặn chừa (tia đèn, cầu vồng, sương, bong bóng, quầng sáng, đom đóm, phù văn, xoáy nước, đinh ba, mưa, sét).
- Boss dạng 2, 3: mọi thứ trùng chỗ với dạng 1, chỉ đổi trời và ánh sáng; mặt bệ vẫn đủ sáng để tướng nổi.
- Sheet: nền trong suốt, mỗi món gọn trong ô của mình, không viền lưới, không số.
- Không chữ, số, sinh vật, người, khung viền.

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Bệ lệch chỗ hoặc sai cỡ | `Same image, but put the two platforms exactly where the sketch has them: same centre and size.` |
| Có đồ trên bệ, giữa hai bệ rối | `Same image, but keep both platform tops empty and the ground between the two platforms calm and simple.` |
| Vật cao, chỗ sáng sau lưng tướng | `Same image, but nothing tall or bright right behind the fighters' places (the white dashed boxes of the sketch).` |
| Vẽ đồ ở chỗ bảng máu | `Same image, but only plain sky, water or ground in the top-right and bottom-left areas the sketch crosses with grey lines.` |
| Vẽ cả phần động | `Same image, but remove the [light beam / rainbow / mist / bubbles / glow / rain / lightning / whirlpool spiral / trident]; leave that place plain as the file says.` |
| Mini boss, boss chưa đủ "đã" | `Make it more dramatic and special: a bigger, grander landmark, a stronger sky and light, richer details along the left and right edges. Keep the layout, the platforms and the empty places.` |
| Tối quá, tướng sẽ chìm | `Same image, a little lighter in the middle, and the two platform tops clearly lighter than the ground around them.` |
| Boss dạng 2, 3 lệch dạng 1 | `Redraw it so every shape is exactly where it is in image 1 (horizon, pillars, whirlpool oval, both platforms); change only the weather and the light.` |
| Sheet có nền hoặc món chạm ô | `Same sheet, but a fully transparent background and every object a little smaller, centred inside its own cell, not touching the cell edges; no grid lines, no numbers.` |
| Có chữ, số, sinh vật | `Same image without any text, numbers, creatures or people.` |
| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it in the rendering of image 1: pencil hatching on cream paper, wobbly ink outlines, chunky doodles with clear silhouettes. Keep the same layout.` |
"""


# ---------- soi ----------

def soi(a, im):
    """vẽ lại khung game lên ảnh đã duyệt: dải cắt, bảng máu, chỗ bệ theo code, thân tướng"""
    im = im.convert("RGBA").resize((W, H))
    overlay_frame(im)
    d = ImageDraw.Draw(im)
    if a["kind"] in ("m", "b", "b2"):
        cx, cy, w, h, _ = FOE_DAIS
    else:
        cx, cy, w, h = FOE_PLAT
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
    if sz != (W, H):
        print(f"  ! {src.name} cỡ {sz}, cần {W} x {H}")
    WORK.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, approved(i))
    print(f"Duyệt {i}: {src} -> {approved(i)}")
    if a["kind"] != "fx":
        with Image.open(src) as im:
            soi(a, im).save(WORK / f"soi_{i}.png")
        print(f"  ảnh soi: {WORK / f'soi_{i}.png'}")


def build():
    PACK.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    make_refs()
    for f in PACK.glob("*.txt"):
        f.unlink()
    for a in ARENAS:
        if a["kind"] in ("c", "m", "b"):
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
    print(f"Gói {PACK}: {len(built)} file prompt ({', '.join(built) or 'chưa có'}); "
          f"{len(ARENAS) - len(built)} lượt chờ ảnh duyệt")


# ---------- xuất vào game ----------
# Nền: cắt khúc khung game khỏi ảnh đã duyệt (góc trên trái x0, y0; s px ảnh GPT mỗi px khung), thu về 1080 x 928, lưu
# Assets/03 Art/BattleBG/battle_thuy_<khoá>; nền đã nối trời (troi/<mã>.png, build_troi.py) thì lưu bản cao 1080 x 1528 (StageView
# neo đáy ảnh vào đáy khung). Khoá: c01..c09 theo chặng, s<ải> cho ải mini boss, boss (s70_2, s70_3: dạng 2, 3).
# Sheet fxm cắt thành BattleBG/Anim/san_<tên> (tiền tố riêng: tên trùng ảnh thay thế, vd fx_glow, thì danh mục ảnh đổi
# luôn ảnh đó trong mọi prefab). Phần động và màu trời từng nền ghi BattleBG/Resources/arena_fx.json (toạ độ 0..1
# theo khung, y từ trên; cỡ theo bề ngang khung), ArenaAnim (Unity) đọc.
ASSETS = ART.parent / "Assets"
OUT = ASSETS / "03 Art" / "BattleBG"
OUT_FX = OUT / "Anim"
OUT_JSON = OUT / "Resources" / "arena_fx.json"
FW, FH = 1080, 928
# khúc chung: đo tâm mặt bệ trên các ảnh đã duyệt (GPT đặt bệ gần cao hơn bố cục ~40 px), chân tướng lệch tâm bệ dưới 20 px
CROP = (209, 50, 1.017)
# bệ nổi của mini boss, boss có mặt trên thấp hơn bệ thường ~15 px: khúc riêng cho chân boss vào giữa mặt bệ
CROP_FIX = {i: (215, 65, 1.0075) for i in ("m20", "m30", "m40", "m50", "m60", "b70a", "b70b", "b70c")}
FX_NAMES = ["beam", "rainbow", "fall", "mist", "glow", "bubble", "bubbles", "firefly", "moonlight", "ripple", "rune", "wisp"]
FXB_NAMES = ["whirlpool", "trident", "bolt", "cloud", "spout", "wave"]  # sheet fxb 3 x 2 (boss 70)
KEY = {"b70a": "s70", "b70b": "s70_2", "b70c": "s70_3"}


def art_key(i):
    return KEY.get(i) or ("s" + i[1:] if i.startswith("m") else i)


def fx(k, x, y, s, **kw):
    return dict(k=k, x=x, y=y, s=s, **kw)


# phần động từng nền, toạ độ ảnh GPT 1536 x 1024. area: w, h quanh (x, y) cho món sinh rải rác; n số hạt; c màu; q độ dẹt;
# a góc; t, b mép trên, dưới của thác. Món: sparkle, foam, spray, wave, ripple, glow, beam, rain, fall, mist, rainbow, bubbles,
# firefly, shimmer, rune, wisp, leaf, whirlpool, trident (xem ArenaAnim.cs)
FX = {
    "c01": [fx("foam", 440, 470, 70), fx("foam", 800, 492, 70), fx("foam", 1180, 508, 70),
            fx("sparkle", 860, 418, 40, w=860, h=60, n=3)],
    "c02": [fx("ripple", 1220, 550, 90), fx("ripple", 1285, 708, 90), fx("sparkle", 900, 398, 40, w=600, h=40, n=2),
            fx("foam", 600, 432, 60)],
    "c03": [fx("ripple", 650, 482, 90), fx("ripple", 950, 490, 90), fx("ripple", 1250, 497, 90),
            fx("sparkle", 900, 488, 34, w=800, h=20, n=2)],
    "c04": [fx("sparkle", 870, 362, 36, w=840, h=20, n=3), fx("glow", 1215, 478, 70, c="#ffd98a")],
    "c05": [fx("wave", 950, 415, 100, w=700, h=50, n=2), fx("sparkle", 900, 400, 38, w=700, h=40, n=2), fx("foam", 450, 470, 70)],
    "c06": [fx("fall", 265, 0, 120, t=160, b=440), fx("mist", 265, 452, 130, w=200, h=20, n=2),
            fx("ripple", 800, 505, 80), fx("ripple", 1150, 498, 80)],
    "c07": [fx("sparkle", 950, 575, 44, w=700, h=250, n=3), fx("ripple", 700, 720, 110), fx("ripple", 1200, 620, 110)],
    "c08": [fx("sparkle", 800, 432, 40, w=1000, h=70, n=3), fx("ripple", 850, 450, 120), fx("ripple", 1150, 460, 120)],
    "c09": [fx("leaf", 300, 60, 46), fx("leaf", 1330, 60, 46), fx("glow", 310, 290, 90, c="#6ff5d8"),
            fx("glow", 1100, 440, 60, c="#ffd98a")],
    "m20": [fx("glow", 285, 140, 150, c="#ffd56a"), fx("beam", 285, 140, 720, a=-6),
            fx("wave", 1000, 450, 120, w=600, h=60, n=3), fx("spray", 430, 488, 130), fx("spray", 1250, 545, 130),
            fx("rain", 760, 512, 46, n=36)],
    "m30": [fx("fall", 312, 0, 190, t=0, b=465), fx("fall", 757, 0, 85, t=50, b=455),
            fx("mist", 520, 470, 170, w=560, h=30, n=4), fx("rainbow", 1110, 330, 360),
            fx("sparkle", 320, 455, 40, w=200, h=20, n=2)],
    "m40": [fx("glow", 285, 380, 240, c="#ffe6f0"), fx("bubbles", 930, 690, 34, w=740, h=260, n=6),
            fx("sparkle", 900, 550, 44, w=800, h=300, n=3), fx("ripple", 900, 700, 120)],
    # quầng sáng có tia ngắn: để quanh trăng thì thành mặt trời, quanh xoáy thành vệt lạ, nên m50, b70a không dùng
    "m50": [fx("shimmer", 330, 470, 160), fx("shimmer", 330, 570, 140),
            fx("shimmer", 335, 670, 120), fx("firefly", 1075, 560, 46, w=450, h=280, n=4),
            fx("firefly", 385, 470, 46, w=270, h=100, n=2), fx("ripple", 800, 800, 160, w=1000, h=400, n=3)],
    "m60": [fx("rune", 515, 540, 400), fx("glow", 420, 320, 200, c="#6ff5d8"), fx("wisp", 800, 540, 60, w=1000, h=320, n=5),
            fx("leaf", 180, 80, 46), fx("leaf", 1350, 60, 46)],
    # boss 70 dùng ảnh cỡ lớn của sheet fxb (san_whirlpool, san_trident, san_wave); dạng 2, 3 (bão nổi, đêm bão): cùng chỗ, xoáy quay
    # nhanh dần, mưa, mây bão trôi, vòi rồng ở chân trời; dạng 3 thêm sét
    "b70a": [fx("whirlpool", 790, 445, 780, q=0.15, img="san_whirlpool"), fx("trident", 790, 450, 120, img="san_trident"),
             fx("wave", 780, 345, 150, w=1050, h=30, n=3, img="san_wave")],
    "b70b": [fx("cloud", 768, 130, 380, w=1300, h=140, n=3), fx("spout", 800, 350, 90, w=900, h=10, n=2),
             fx("whirlpool", 790, 445, 780, q=0.15, v=1.4, img="san_whirlpool"), fx("trident", 790, 450, 120, img="san_trident"),
             fx("wave", 780, 345, 160, w=1050, h=30, n=4, img="san_wave"), fx("rain", 760, 512, 50, n=40)],
    "b70c": [fx("cloud", 768, 110, 420, w=1300, h=160, n=4), fx("bolt", 760, 40, 210, w=900, h=20),
             fx("spout", 800, 350, 100, w=900, h=10, n=3),
             fx("whirlpool", 790, 445, 780, q=0.15, v=2, img="san_whirlpool"), fx("trident", 790, 450, 120, img="san_trident"),
             fx("wave", 780, 345, 170, w=1050, h=30, n=4, img="san_wave"), fx("rain", 760, 512, 56, n=54)],
}


def crop_of(i):
    return CROP_FIX.get(i, CROP)


def to_frame(i, item):
    """toạ độ ảnh GPT -> 0..1 theo khung (cỡ theo bề ngang khung)"""
    x0, y0, s = crop_of(i)
    out = dict(item)
    out["x"] = round((item["x"] - x0) / s / FW, 4)
    out["y"] = round((item["y"] - y0) / s / FH, 4)
    for k in ("s", "w"):
        if k in item:
            out[k] = round(item[k] / s / FW, 4)
    for k in ("h", "t", "b"):
        if k in item:
            out[k] = round((item[k] - (y0 if k in ("t", "b") else 0)) / s / FH, 4)
    return out


def frame_of(i):
    x0, y0, s = crop_of(i)
    with Image.open(approved(i)) as im:
        return im.convert("RGB").crop((x0, y0, round(x0 + FW * s), round(y0 + FH * s))).resize((FW, FH), Image.LANCZOS)


# nền vẽ dư trời cho máy dài (build_troi.py --duyet): 1080 x 1528, 928 dòng dưới là khung; có thì xuất bản này
TROI = HERE / "troi"


def art_of(i):
    tall = TROI / f"{i}.png"
    if tall.exists():
        with Image.open(tall) as im:
            return im.convert("RGB")
    return frame_of(i)


def sky_of(im):
    """màu trời phủ phần dôi trên đầu máy dài: trung bình 6 hàng trên cùng"""
    px = im.crop((0, 0, FW, 6)).resize((1, 1), Image.BOX).getpixel((0, 0))
    return "#%02x%02x%02x" % px[:3]


def cut_fx_sheet(i, cols, rows, names):
    OUT_FX.mkdir(parents=True, exist_ok=True)
    with Image.open(approved(i)) as im:
        im = im.convert("RGBA")
        cw, ch = im.width // cols, im.height // rows
        for k, name in enumerate(names):
            cell = im.crop(((k % cols) * cw, (k // cols) * ch, (k % cols + 1) * cw, (k // cols + 1) * ch))
            box = cell.getchannel("A").point(lambda a: 255 if a > 10 else 0).getbbox()
            if not box:
                print(f"  ! {i} ô {k + 1} trống")
                continue
            box = (max(0, box[0] - 4), max(0, box[1] - 4), min(cw, box[2] + 4), min(ch, box[3] + 4))
            cell.crop(box).save(OUT_FX / f"san_{name}.png")
    print(f"  {i}: {len(names)} ảnh -> {OUT_FX}")


def export():
    import json
    OUT.mkdir(parents=True, exist_ok=True)
    data = {}
    for a in ARENAS:
        i = a["id"]
        if a["kind"] == "fx" or not approved(i).exists():
            continue
        im = art_of(i)
        key = "thuy_" + art_key(i)
        im.save(OUT / f"battle_{key}.png")
        data[key] = {"sky": sky_of(im), "fx": [to_frame(i, f) for f in FX.get(i, [])]}
        print(f"  {i} -> battle_{key}.png ({im.width} x {im.height}), trời {data[key]['sky']}, {len(data[key]['fx'])} phần động")
    if approved("fxm").exists():
        cut_fx_sheet("fxm", 4, 3, FX_NAMES)
    if approved("fxb").exists():
        cut_fx_sheet("fxb", 3, 2, FXB_NAMES)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    # chỉ thay khoá thuy_*, giữ khoá đảo khác (đảo Mộc: build_moc.py --xuat)
    old = json.loads(OUT_JSON.read_text(encoding="utf-8")).get("arenas", {}) if OUT_JSON.exists() else {}
    arenas = {k: v for k, v in old.items() if not k.startswith("thuy_")}
    arenas.update(data)
    OUT_JSON.write_text(json.dumps({"note": "build_thuy.py --xuat; toạ độ 0..1 theo khung sân 1080 x 928, y từ trên; cỡ theo bề "
                                            "ngang khung", "arenas": arenas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Xuất {len(data)} nền vào {OUT}, phần động {OUT_JSON}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar=("MA", "ANH"), help="duyệt ảnh GPT của lượt <mã> (mặc định ảnh mới nhất)")
    ap.add_argument("--xuat", action="store_true", help="xuất các nền đã duyệt, sheet phần động và arena_fx.json vào Assets")
    args = ap.parse_args()
    if args.duyet:
        approve(args.duyet[0], args.duyet[1] if len(args.duyet) > 1 else None)
    if args.xuat:
        export()
    else:
        build()
