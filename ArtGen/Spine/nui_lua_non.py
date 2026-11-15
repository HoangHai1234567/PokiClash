# -*- coding: utf-8 -*-
"""Khủng long núi lửa DẠNG 1 (con non, bản CHIBI; mã nui_lua_non, suất lan_hoa = tướng thứ 10 đảo Hỏa).

Người dùng 2026-11-14: "Ok làm dạng 1 đi" (sau khi xem rig dạng lớn bản "sừng"). Làm như hổ con bản chibi (hoa_ho_non.py mục CHIBI; bản
ghép từ da dạng lớn + đầu phóng to của hổ đã bị chê "xấu quá, gen lại chibi hơn", nên con này đi thẳng đường chibi):
tỉ lệ đổi ngay trên rig (nui_lua_rig.py, NL_DANG=non: đầu to và ngẩng lên, chân ngắn, bốn ống núi lửa ngắn + miệng núi lửa chính) → hình bố
cục → concept → người dùng chọn → mới làm mảnh.

    nui_lua_non.py bo_cuc    hình bố cục từ rig với tỉ lệ chibi → inbox/nui_lua_non/mau/bo_cuc_chibi.png
    nui_lua_non.py concept   prompt concept gui_gpt/nui_lua_non/luot_0_concept_<A|B>.txt (+ HUONG_DAN_concept.md)
    nui_lua_non.py manh_prompt  năm tờ mảnh "đúng chỗ, đúng cỡ" từ concept đã chọn: gui_gpt/nui_lua_non/luot_1_chibi_<tờ>.txt
  Cắt và lắp: nui_lua_chibi.py; rig: NL_DANG=chibi py -3 -I nui_lua_rig.py → inbox/nui_lua_non/rig/
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.join(HERE, "inbox", "nui_lua_non")
TAI = os.path.join(BASE, "tai_ve")
MAU = os.path.join(BASE, "mau")
GUI = os.path.join(HERE, "gui_gpt", "nui_lua_non")
LON = os.path.join(HERE, "inbox", "nui_lua_1")
W, H = 1536, 1024
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no darker side, no "
        "cast shadow, no shadow under the feet, no white highlights or shine spots (except ONE tiny light dot in the eye), NO GLOW around "
        "the lava (lava is just a flat bright colour with an ink outline), NO GRADIENTS (two colours always meet at a clean inked edge), no "
        "3D look.")


def Wp(p):
    return os.path.normpath(p)


def ghi(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(s)


def bo_cuc():
    """hình bố cục 1536x1024 nền trắng: dáng đứng khung 0 idle của rig với tỉ lệ chibi, da của dạng lớn, không khói (chỉ để lấy dáng, tỉ lệ)."""
    os.environ["NL_DANG"] = "non"
    import nui_lua_rig as R
    sk, info = R.dung()
    ve0 = R.soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    P0 = R.hoat.nuong(sk, clips[1])[0]
    for b, *_ in info["khoi"]:
        P0.alpha[b] = 0.0
    b = ve0.bao(P0)
    sc = min((W * 0.74) / (b[2] - b[0]), (H * 0.80) / (b[3] - b[1]))
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    box = (cx - W / 2 / sc, cy - H / 2 / sc, cx + W / 2 / sc, cy + H / 2 / sc)
    im = ve0.ve(P0, box, sc, bg=(255, 255, 255), ss=2).convert("RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(MAU, exist_ok=True)
    p = os.path.join(MAU, "bo_cuc_chibi.png")
    im.save(p)
    json.dump(dict(sc=sc, box=box, chibi=dict(NL_KDAU=R.K_DAU, NL_CO=R.G_CO, NL_CHAN=R.K_CHAN, NL_KONG=R.K_ONG, NL_KLUNG=R.K_LUNG,
                                               ong=R.ONG_NON)), open(os.path.join(MAU, "bo_cuc_chibi.json"), "w"))
    print(p, f"{sc:.3f} px / đơn vị; khung", [round(v) for v in b])


def concept():
    lon = os.path.join(LON, "tai_ve", "L1_duyet.png")
    bc = os.path.join(MAU, "bo_cuc_chibi.png")
    chibi = os.path.join(HERE, "inbox", "hoa_ho_non", "tai_ve", "L1_duyet.png")
    net = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
    for f in (lon, bc, chibi, net):
        if not os.path.exists(f):
            raise SystemExit("thiếu ảnh mẫu " + f)
    os.makedirs(TAI, exist_ok=True)
    huong = {
        "A": ("theo bố cục",
              "Follow image 2 closely: the same proportions and the same placement of the head, the body, the four legs, the big volcano and "
              "the small cones on the canvas."),
        "B": ("tròn hơn",
              "Follow the pose and placement of image 2, but push it ROUNDER and even more chibi: the body is one plump round boulder, the "
              "four legs are very short stubs (each still clearly visible and separate), the head is a little bigger and rounder than in "
              "image 2, the eye is larger, the big volcano on the back is shorter and fatter, like a little pudding."),
    }
    hd = ["# Khủng long núi lửa dạng 1 bản CHIBI (nui_lua_non): concept\n",
          "Người dùng 2026-11-14: \"Ok làm dạng 1 đi\". Hai hướng concept là đề xuất của Claude, chọn một rồi Claude mới làm mảnh.\n",
          "## Ảnh mẫu (cả hai file dùng chung, theo thứ tự)",
          f"1. `{Wp(lon)}` — concept dạng LỚN đã duyệt (bản sừng), 1536x1024, nền trắng: khủng long đá đen hai sừng ngà, lưng là núi lửa; lấy "
          "loài, màu, nét vẽ.",
          f"2. `{Wp(bc)}` — hình bố cục máy dựng từ rig, 1536x1024, nền trắng: cùng con đó với đầu to ngẩng lên, chân ngắn, chỉ còn một núi "
          "lửa lớn và bốn ống nhỏ; thô, còn chi tiết của dạng lớn; chỉ để lấy dáng và tỉ lệ.",
          f"3. `{Wp(chibi)}` — dạng 1 chibi đã duyệt của tướng khác (hổ con), nền trắng: lấy MỨC chibi và độ đơn giản.",
          f"4. `{Wp(net)}` — ảnh mốc nét vẽ tay của game (bản đồ vẽ bút mực, tô chì màu).\n"]
    for ma, (vi, cau) in huong.items():
        out = os.path.join(TAI, f"L1_{ma}.png")
        txt = f"""IMAGES (attached in this order; open each from its path):
image 1 = {Wp(lon)}: the ADULT creature, already approved, 1536x1024, white background: a huge four-legged VOLCANO DINOSAUR of charcoal-black basalt facing right, with two great ivory ram horns, an ivory lower jaw, and a back that carries a main crater mountain and a crowd of tiered crater towers. It gives the species, the colours and the drawing style (wobbly dark-brown ink line, loose crayon hatching, flat colours).
image 2 = {Wp(bc)}: PROPORTION AND POSE GUIDE, 1536x1024, white background, assembled by computer from the animation rig: the same animal as a baby: a big head held up at the right, short legs, ONE big volcano in the middle of the back and only four small cones. It is crude and still carries the adult's details (a blocky head, too many rocks and lines). Use it ONLY for the pose, the proportions and where each body part sits on the canvas.
image 3 = {Wp(chibi)}: an approved CHIBI baby form of a different creature from the same set (a tiger cub), white background. It shows the level of chibi wanted: huge simple head, small body, few details, bold clean shapes. Do not copy that creature.
image 4 = {Wp(net)}: the hand-drawn look of the whole set: ink pen on paper, filled with coloured pencil and wax crayon.

SAVE: save it as a PNG to {Wp(out)}
If a file with that name already exists, save as L1_{ma}_2.png, L1_{ma}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw the HATCHLING (the baby form) of the volcano dinosaur of image 1 as a cute CHIBI creature. One single creature, whole body, landscape 1536x1024, pure-white background (#FFFFFF), side view facing RIGHT, standing on all four legs. {cau}

PROPORTIONS: the head is huge and rounded, almost half of the creature's total length. The body is small, low and plump. Four short, thick, stubby pillar legs. No tail.

MATERIAL: the whole animal is made of smooth, ROUNDED boulders of charcoal basalt (#6A5868 purple-grey, as the rock of image 1), like river pebbles: big simple shapes with only one or two short crack lines each. Far fewer pieces than the adult.

HEAD AND FACE: seen in three-quarter side view facing right, so ONE big eye is visible. The upper head is one big rounded boulder with a soft bump of a brow. The eye is big and round: dark ink rim, golden-yellow iris (#FAD646), a large dark pupil (a tall oval), ONE tiny light dot. A short firm upper eyelid gives a brave, determined look (cute but ready to fight, not sleepy, not scary). The LOWER JAW is a separate piece of warm ivory bone (#E4CEA4), short and rounded like a little shovel, with THREE small rounded baby teeth along its upper edge; the mouth is slightly open and flat lava orange (#F07828) shows inside. On the brow, above and in front of the eye, TWO tiny ivory HORN BUDS: short blunt cones pointing forward and up, each with one ring line (they will grow into the adult's great horns).

BACK (a baby volcano): in the middle of the back ONE small plump VOLCANO of near-black basalt (#36323C), about as tall as the head, with an open crater on top: a thick orange (#F07828) lip, a golden-yellow (#FACC50) lava pool seen slightly from above, and ONE short forked dribble of flat orange lava running down its front. Around it only THREE little crater cones of charcoal basalt, stubby like thimbles, each with ONE orange seam ring, an orange lip with two or three drips and a yellow pool: one behind the volcano at the left, one in front of it, one small one peeking out behind the head. No other chimneys.

BODY AND LEGS: the flank is two or three plump rounded boulders; in ONE gap between them a sliver of flat orange lava shows. ONE small ivory bone thorn on the hip boulder. Each leg is one short thick pillar of charcoal basalt; the two front feet end in THREE small rounded ivory claws; the two hind feet are dipped in lava: an orange band with a zigzag upper edge at the bottom.

NOT ON THE HATCHLING: no long horns, no tail, no wings, no smoke, no flames in the air, no sparks, no long teeth, no armour, no jewellery.

KEEP IT EASY TO ANIMATE: all four legs clearly visible and separate from each other, placed as in image 2 (do not hide a leg behind the body or the head). The head does not cover the volcano; the cones do not cover the face. The lower jaw is a clearly separate piece from the upper head. Every cone and the volcano are separate shapes with their own complete outline.

LINE AND COLOUR: exactly the hand-drawn look of images 1 and 4: ONE wobbly dark-brown ink pen outline (#2B2118), about 7 px thick around the creature and around each body part, about 4 px for inner details; every area filled with visible loose diagonal coloured-pencil / wax-crayon hatching kept inside the lines. Drawn carefully and cleanly, not scribbled, not glossy, not digital-looking.

{FLAT}

Pure white background. No ground, no ground shadow, no text, no labels, no numbers, no frame, no white sticker border around the creature. Leave a white margin of at least 60 px on every side.
"""
        p = os.path.join(GUI, f"luot_0_concept_{ma}.txt")
        ghi(p, txt)
        hd += [f"## Hướng {ma} ({vi})", f"- File prompt: `{Wp(p)}`", f"- GPT lưu vào: `{Wp(out)}` (trùng tên thì `_2`, `_3`).\n"]
        print(p)
    hd += ["## Cách kiểm",
           "- Một con khủng long đá con, nhìn ngang quay phải, đứng bốn chân, đầu to gần nửa chiều dài, bốn chân đều thấy rõ.",
           "- Một mắt to tròn màu vàng, vẻ quả quyết; hàm dưới ngà rời khỏi đầu trên, ba răng sữa tròn; hai nụ sừng ngà nhỏ trên trán.",
           "- Lưng: MỘT núi lửa nhỏ mập có miệng (vành cam, lòng vàng, một dòng dung nham ngắn) + ba ống nhỏ; không khói, không lửa.",
           "- Tô phẳng, không bóng, không phát sáng, không điểm sáng (trừ một chấm trong mắt).\n",
           "## Câu sửa nhanh",
           "- Chưa đủ chibi: \"Make the head bigger and rounder and the legs shorter; fewer rocks, fewer lines.\"",
           "- Chân bị che: \"Show all four legs clearly, separate from each other, as in image 2.\"",
           "- Có khói / lửa / phát sáng: \"Remove all smoke, flames and glow; lava is flat orange with an ink outline.\""]
    ghi(os.path.join(GUI, "HUONG_DAN_concept.md"), "\n".join(hd) + "\n")


# ---------------------------------------------------------------- mảnh của bản CHIBI: gen "đúng chỗ, đúng cỡ" từ concept đã chọn (A)
DUYET = os.path.join(TAI, "L1_duyet.png")
CON_NON = ("a chibi baby VOLCANO DINOSAUR facing right, made of rounded purple-grey boulders: a huge round head with one big yellow eye, two "
           "tiny ivory horn buds and an ivory lower jaw; on its back one plump dark volcano with an orange lip and three little crater "
           "cones; four short pillar legs (the two hind feet dipped in orange lava, the two front feet with ivory claws)")
TO_C = {
    "THAN": ("thân (hai tảng hông và vai + khe dung nham), không đầu, chân, núi lửa, ống",
             "ONLY THE BODY: the big round HIP boulder with its ivory thorn (about x = 225 to 520, y = 500 to 790), the orange lava gap "
             "(about x = 490 to 545, y = 620 to 790) and the big SHOULDER boulder (about x = 530 to 900, y = 510 to 790), as ONE CLOSED "
             "group in the same place. REMOVE the head with its jaw, the dark volcano, all three crater cones and all four legs. COMPLETE "
             "the body where those parts covered it or joined it: the shoulder boulder continues to the right as a rounded boulder to "
             "about x = 940 (under where the head was); the top edges of both boulders are complete rounded outlines (where the cones "
             "and the volcano stood); the underside is ONE smooth rounded belly line at about y = 800 with NO leg stumps and no gaps. "
             "Keep the thorn, the crack lines and the lava gap exactly."),
    "CHAN": ("bốn chân rời nhau + ống núi lửa phía trước",
             "ONLY FIVE THINGS, as FIVE SEPARATE closed shapes, each in the same position and at the same size as in image 1: leg 1 = the "
             "hind leg at the far left with the orange zigzag lava band (about x = 235 to 415, y = 760 to 925); leg 2 = the smaller "
             "lava-banded leg right of it (about x = 460 to 610, y = 780 to 915); leg 3 = the front leg in the middle with three ivory "
             "claws (about x = 630 to 865, y = 740 to 940); leg 4 = the front leg at the right with ivory claws (about x = 880 to 1115, "
             "y = 760 to 925); and the FRONT CRATER CONE (the little volcano cone at about x = 415 to 635, y = 365 to 540, with its orange "
             "lip, drips, yellow pool and orange seam ring). REMOVE the body, the head, the dark volcano and the two other cones. "
             "COMPLETE every leg: where the body or the head covered its top, extend the leg upward by about 70 px and close it with a "
             "ROUNDED top end, like a short plump pillar; keep the lava bands and the claws exactly. COMPLETE the cone: extend its base "
             "downward by about 50 px (to about y = 590) and close it with a rounded bottom. The five shapes must NOT touch each other: "
             "keep clear white space between them."),
    "NUI": ("núi lửa chính",
            "ONLY THE BIG DARK VOLCANO in the middle of the back (about x = 450 to 830, y = 85 to 520): the near-black cone with its thick "
            "orange lip, the yellow lava pool and the orange lava running down its front. REMOVE the head, the body, the legs and all "
            "three small crater cones. COMPLETE the volcano into ONE CLOSED SHAPE: where the cones, the body and the head covered its "
            "lower part, continue its two sloping sides straight down and close it with a wide rounded base at about y = 600; the hidden "
            "areas are plain near-black rock with one or two crack lines. Do not change the lip, the pool or the lava."),
    "ONG": ("hai ống nhỏ (trái, phải)",
            "ONLY TWO THINGS, as TWO SEPARATE closed shapes in the same positions and at the same sizes as in image 1: (a) the LEFT crater "
            "cone (about x = 290 to 445, y = 245 to 500): complete its hidden base by extending it about 60 px further down (to about "
            "y = 560) and close it with a rounded bottom; (b) the RIGHT crater cone behind the head (about x = 815 to 965, y = 155 to "
            "290): complete it where the head covered it: continue its sides down to about y = 370 and close it with a rounded bottom, "
            "with one orange seam ring like the other cones. Keep their orange lips, drips, yellow pools and seam rings exactly. REMOVE "
            "the head, the body, the legs, the dark volcano and the front cone."),
    "DAU": ("đầu (cả hàm dưới, hai nụ sừng, mắt, răng)",
            "ONLY THE HEAD: the whole big round head with the two ivory horn buds, the brow line, the big yellow eye, the upper teeth, the "
            "orange inside of the mouth and the ivory LOWER JAW (about x = 705 to 1315, y = 225 to 770). REMOVE the body, the legs, the "
            "volcano and the cones. COMPLETE the head into ONE CLOSED SHAPE: where the body touched it at the lower left, continue the "
            "head's own rounded outline. Do not change the face."),
}


TIEU_DE = "Khủng long núi lửa dạng 1 bản CHIBI (nui_lua_non)"
MO_TA = ("Concept đã chọn (A, người dùng 2026-11-14)", "khủng long đá con chibi đứng bốn chân quay phải, đầu to một mắt vàng, hai nụ sừng ngà, "
         "hàm dưới ngà; lưng có một núi lửa sẫm và ba ống nhỏ")
TEN_TO = "luot_1_chibi"


def manh_prompt():
    cd = "x".join(str(v) for v in Image.open(DUYET).size)
    hd = [f"# {TIEU_DE}: lượt mảnh\n",
          f"{MO_TA[0]}: `{Wp(DUYET)}`, {cd}, nền trắng: {MO_TA[1]}. Mỗi tờ GPT vẽ lại MỘT phần của "
          "concept, đúng chỗ, đúng cỡ, bỏ hết phần khác và vẽ bù phần bị che thành hình kín.\n"]
    for ma, (vi, cau) in TO_C.items():
        out = os.path.join(TAI, f"C_{ma}.png")
        txt = f"""IMAGES (attached in this order; open each from its path):
image 1 = {Wp(DUYET)}: the APPROVED creature, {cd}, white background: {CON_NON}. Coordinates below are pixels on this image, x from the left, y from the top.

SAVE: save it as a PNG to {Wp(out)}
If a file with that name already exists, save as C_{ma}_2.png, C_{ma}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw image 1 with {cau}

SAME POSITION, SAME SIZE: landscape 1536x1024; if your picture were laid over image 1, every part you keep must coincide with the same part there. Do not move, scale, rotate or re-pose anything. A program will cut this picture by position and assemble the pieces.

LINE AND COLOUR: exactly the look of image 1: the same wobbly dark-brown ink pen outline (#2B2118), about 7 px thick, closed all the way around each shape, about 4 px for inner details; the same colours; the same loose diagonal crayon / coloured-pencil hatching inside every area.

{FLAT}

Pure white (#FFFFFF) background everywhere else: no ground, no shadow, no smoke, no text, no labels, no numbers, no frame, no white sticker border.
"""
        p_ = os.path.join(GUI, f"{TEN_TO}_{ma}.txt")
        ghi(p_, txt)
        hd += [f"## Tờ {ma}: {vi}", f"- File prompt: `{Wp(p_)}`", "- Ảnh mẫu: concept ở trên.", f"- GPT lưu vào: `{Wp(out)}` (trùng tên thì `_2`, `_3`).\n"]
        print(p_)
    hd += ["## Cách kiểm", "- Chồng lên concept thì phần giữ lại trùng chỗ, trùng cỡ; mỗi hình có viền mực kín; nền trắng tinh.",
           "- Tờ CHAN: bốn chân và một ống rời nhau, đỉnh chân bo tròn. Tờ THAN: bụng trơn không mẩu chân. Tô phẳng, không bóng.\n",
           "## Câu sửa nhanh", "- Lệch chỗ: \"Keep exactly the position and size of image 1.\"",
           "- Hình chưa kín: \"Close the ink outline all the way around every shape.\"",
           "- Hai hình chạm nhau: \"Keep clear white space between the separate shapes.\""]
    ghi(os.path.join(GUI, "HUONG_DAN_manh_chibi.md"), "\n".join(hd) + "\n")


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    if lenh == "bo_cuc":
        bo_cuc()
    elif lenh == "concept":
        concept()
    elif lenh == "manh_prompt":
        manh_prompt()
    else:
        print(__doc__)
