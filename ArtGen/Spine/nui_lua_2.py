# -*- coding: utf-8 -*-
"""Khủng long núi lửa DẠNG 2 (con thiếu niên; mã nui_lua_2, suất lan_hoa = tướng thứ 10 đảo Hỏa).

Người dùng 2026-11-15: "con này cần có dạng 2 nữa, làm dạng 2 đi". Dòng có ba dạng: 1 = con non chibi (nui_lua_non), 2 = thiếu niên (file
này), 3 = boss hai sừng (nui_lua_1). Theo luật tiến hoá của dự án: chỉ dạng 1 chibi; dạng 2 hết chibi, mắt sắc, thế đánh, nhưng chưa bằng
dạng cuối. Làm như dạng 1 bản chibi (nui_lua_non.py): tỉ lệ đổi trên rig → hình bố cục → concept → người dùng chọn → mảnh cắt từ concept.

    nui_lua_2.py bo_cuc     hình bố cục từ rig với tỉ lệ dạng 2 → inbox/nui_lua_2/mau/bo_cuc_chibi.png
    nui_lua_2.py concept    prompt concept gui_gpt/nui_lua_2/luot_0_concept_<A|B>.txt (+ HUONG_DAN_concept.md)
    nui_lua_2.py manh_prompt   sáu tờ mảnh "đúng chỗ, đúng cỡ" từ concept đã chọn: gui_gpt/nui_lua_2/luot_1_manh_<tờ>.txt
  Cắt và lắp: NL_MA=nui_lua_2 nui_lua_chibi.py cat; rig: NL_MA=nui_lua_2 NL_DANG=chibi py -3 -I nui_lua_rig.py → inbox/nui_lua_2/rig/
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# tỉ lệ dạng 2 (giữa dạng 1 và dạng 3): đầu to hơn dạng lớn một chút và ngẩng vừa phải, chân ngắn bớt, sáu ống + núi lửa chính, sừng ngắn
TI_LE = dict(NL_MA="nui_lua_2", NL_KDAU="1.22", NL_CO="26", NL_CHAN="0.9", NL_KONG="0.82", NL_KLUNG="0.92", NL_ONG="09,10,02,14,13,03",
             NL_SUNG="0.6")
for k_, v_ in TI_LE.items():
    os.environ.setdefault(k_, v_)
import nui_lua_non as N  # noqa: E402

N.BASE = os.path.join(HERE, "inbox", "nui_lua_2")
N.TAI, N.MAU = os.path.join(N.BASE, "tai_ve"), os.path.join(N.BASE, "mau")
N.GUI = os.path.join(HERE, "gui_gpt", "nui_lua_2")
Wp, ghi, FLAT = N.Wp, N.ghi, N.FLAT


def concept():
    lon = os.path.join(N.LON, "tai_ve", "L1_duyet.png")
    non = os.path.join(HERE, "inbox", "nui_lua_non", "tai_ve", "L1_duyet.png")
    bc = os.path.join(N.MAU, "bo_cuc_chibi.png")
    net = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
    for f in (lon, non, bc, net):
        if not os.path.exists(f):
            raise SystemExit("thiếu ảnh mẫu " + f)
    os.makedirs(N.TAI, exist_ok=True)
    huong = {
        "A": ("nghiêng về dạng lớn",
              "Lean toward the ADULT (image 1): chunky FACETED boulders with a few facet lines, a lean and fierce look, a narrow angry "
              "eye; like a young bull that already wants to fight."),
        "B": ("nghiêng về dạng 1",
              "Lean a little toward the HATCHLING (image 2): rounder boulders with fewer lines and a slightly bigger eye, but clearly "
              "older, bigger and tougher than the hatchling; brave and cocky."),
    }
    hd = ["# Khủng long núi lửa dạng 2 (thiếu niên, nui_lua_2): concept\n",
          "Người dùng 2026-11-15: \"con này cần có dạng 2 nữa, làm dạng 2 đi\". Hai hướng concept là đề xuất của Claude, chọn một rồi Claude "
          "mới làm mảnh.\n",
          "## Ảnh mẫu (cả hai file dùng chung, theo thứ tự)",
          f"1. `{Wp(lon)}` — concept dạng 3 (boss hai sừng) đã duyệt, 1536x1024, nền trắng: lấy loài, màu, nét vẽ, đích tiến hoá.",
          f"2. `{Wp(non)}` — concept dạng 1 (con non chibi) đã duyệt, 1536x1024, nền trắng: điểm xuất phát của dòng.",
          f"3. `{Wp(bc)}` — hình bố cục máy dựng từ rig, 1536x1024, nền trắng: cùng con đó ở tỉ lệ thiếu niên (đầu ngẩng vừa, sáu ống + một "
          "núi lửa giữa lưng, hai sừng ngắn); thô, còn chi tiết của dạng lớn; chỉ để lấy dáng và tỉ lệ.",
          f"4. `{Wp(net)}` — ảnh mốc nét vẽ tay của game (bản đồ vẽ bút mực, tô chì màu).\n"]
    for ma, (vi, cau) in huong.items():
        out = os.path.join(N.TAI, f"L1_{ma}.png")
        txt = f"""IMAGES (attached in this order; open each from its path):
image 1 = {Wp(lon)}: the ADULT, final form (stage 3), already approved, 1536x1024, white background: a huge four-legged VOLCANO DINOSAUR of charcoal-black basalt facing right, with two great ivory ram horns, an ivory lower jaw with saw teeth, and a back that carries a main crater mountain and a crowd of tiered crater towers. It gives the species, the colours, the drawing style and where the evolution ends.
image 2 = {Wp(non)}: the HATCHLING (stage 1), already approved, 1536x1024, white background: the same species as a chibi baby: a huge round head with one big yellow eye, two tiny horn buds, an ivory lower jaw, one plump volcano and three little cones on its back, four short pillar legs. It shows where the evolution starts.
image 3 = {Wp(bc)}: PROPORTION AND POSE GUIDE for the form to draw, 1536x1024, white background, assembled by computer from the animation rig: the same animal as a JUVENILE: the head held half-way up at the right, medium legs, ONE volcano in the middle of the back and six crater towers, two short horns. It is crude and still carries the adult's details. Use it ONLY for the pose, the proportions and where each body part sits on the canvas.
image 4 = {Wp(net)}: the hand-drawn look of the whole set: ink pen on paper, filled with coloured pencil and wax crayon.

SAVE: save it as a PNG to {Wp(out)}
If a file with that name already exists, save as L1_{ma}_2.png, L1_{ma}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw the JUVENILE (stage 2, the middle form) of this volcano dinosaur: clearly the same animal as images 1 and 2, half-way between them. One single creature, whole body, landscape 1536x1024, pure-white background (#FFFFFF), side view facing RIGHT, standing on all four legs in a battle-ready stance. {cau}

PROPORTIONS (no longer chibi): the head is about one third of the creature's length, held forward and a little lowered, ready to ram. The body is sturdy and low. Four thick pillar legs of medium length. No tail. It must read as a young fighter: bigger, heavier and fiercer than the hatchling, but smaller and simpler than the adult.

MATERIAL: boulders of charcoal basalt (#6A5868 purple-grey, as the rock of images 1 and 2), big simple shapes with two or three facet or crack lines each. Fewer pieces than the adult, more than the hatchling.

HEAD AND FACE: three-quarter side view facing right, ONE eye visible. The upper head is a heavy boulder with a clear overhanging BROW ridge. The eye is medium-sized (much smaller than the hatchling's): golden-yellow iris (#FAD646), a dark slit-like oval pupil, ONE tiny light dot, a slanted upper eyelid: an angry, determined look (not scary, not cute-smiling). The LOWER JAW is a separate piece of warm ivory bone (#E4CEA4), longer than the hatchling's, with FOUR or FIVE pointed teeth along its upper edge; a few small rock teeth hang from the upper lip; the mouth is slightly open and flat lava orange (#F07828) shows inside. TWO ivory HORNS grow from the brow and curve forward and up: clearly real horns now, about half as long as the adult's, each with two ring grooves near the base.

BACK (a growing volcano range): in the middle of the back ONE steep VOLCANO of near-black basalt (#36323C), taller than the head, with an open crater on top: a thick orange (#F07828) lip, a golden-yellow (#FACC50) lava pool seen slightly from above, and one forked stream of flat orange lava running down its front. Around it FIVE or SIX crater towers of charcoal basalt of different heights: each is two or three stacked rock rings with a flat orange seam between the rings, an orange lip with drips and a yellow pool; the two tallest stand behind the volcano at the left, the others fan out to the left and to the right behind the head. Fewer and shorter towers than the adult.

BODY AND LEGS: the flank is three or four chunky boulders overlapping like armour; in the gaps between them slivers of flat orange lava show. TWO small ivory bone thorns on the flank boulders. Each leg is a thick pillar of charcoal basalt built from two stacked blocks; the two front feet end in THREE ivory claws; the two hind feet are dipped in lava: an orange band with a zigzag upper edge at the bottom.

NOT ON THIS FORM: no tail, no wings, no smoke, no flames in the air, no sparks, no armour, no jewellery; not the adult's huge horns, not the hatchling's huge round eye.

KEEP IT EASY TO ANIMATE: all four legs clearly visible and separate from each other, placed as in image 3 (do not hide a leg behind the body or the head). The head does not cover the volcano. The lower jaw is a clearly separate piece from the upper head. The volcano and every tower are separate shapes with their own complete outline.

LINE AND COLOUR: exactly the hand-drawn look of images 1, 2 and 4: ONE wobbly dark-brown ink pen outline (#2B2118), about 6 px thick around the creature and around each body part, about 3 px for inner details; every area filled with visible loose diagonal coloured-pencil / wax-crayon hatching kept inside the lines. Drawn carefully and cleanly, not scribbled, not glossy, not digital-looking.

{FLAT}

Pure white background. No ground, no ground shadow, no text, no labels, no numbers, no frame, no white sticker border around the creature. Leave a white margin of at least 60 px on every side.
"""
        p = os.path.join(N.GUI, f"luot_0_concept_{ma}.txt")
        ghi(p, txt)
        hd += [f"## Hướng {ma} ({vi})", f"- File prompt: `{Wp(p)}`", f"- GPT lưu vào: `{Wp(out)}` (trùng tên thì `_2`, `_3`).\n"]
        print(p)
    hd += ["## Cách kiểm",
           "- Một con khủng long đá thiếu niên, nhìn ngang quay phải, đứng bốn chân, thế sẵn sàng húc; đầu khoảng một phần ba chiều dài.",
           "- Rõ là cùng loài với dạng 1 và dạng 3, nằm giữa hai dạng: mắt vừa, vẻ dữ; hai sừng thật nhưng ngắn; hàm dưới ngà rời có răng nhọn.",
           "- Lưng: một núi lửa có miệng + năm sáu tháp ống xếp tầng; ít và thấp hơn dạng 3. Không khói, không lửa.",
           "- Tô phẳng, không bóng, không phát sáng, không điểm sáng (trừ một chấm trong mắt).\n",
           "## Câu sửa nhanh",
           "- Còn chibi quá: \"Make the head smaller and the eye smaller and narrower; longer legs; more facets.\"",
           "- Giống dạng lớn quá: \"Fewer and shorter towers, shorter horns, simpler boulders.\"",
           "- Chân bị che: \"Show all four legs clearly, separate from each other, as in image 3.\""]
    ghi(os.path.join(N.GUI, "HUONG_DAN_concept.md"), "\n".join(hd) + "\n")


# ---------------------------------------------------------------- mảnh của dạng 2: gen "đúng chỗ, đúng cỡ" từ concept đã chọn (A, 2026-11-15)
N.DUYET = os.path.join(N.TAI, "L1_duyet.png")
N.TIEU_DE = "Khủng long núi lửa dạng 2 (thiếu niên, nui_lua_2)"
N.MO_TA = ("Concept đã chọn (A, người dùng 2026-11-15)", "khủng long đá thiếu niên đứng bốn chân quay phải, mắt vàng hẹp, hai sừng ngà ngắn, "
           "hàm dưới ngà răng nhọn; lưng có một núi lửa sẫm và năm tháp ống xếp tầng")
N.TEN_TO = "luot_1_manh"
N.CON_NON = ("a JUVENILE VOLCANO DINOSAUR facing right, made of chunky faceted purple-grey boulders: a heavy head with one narrow yellow "
             "eye, two short ivory horns and an ivory lower jaw with pointed teeth; on its back one dark volcano with an orange lip and "
             "five tiered crater towers; four thick pillar legs (the two hind feet dipped in orange lava, the two front feet with ivory "
             "claws)")
N.TO_C = {
    "DAU": ("đầu (cả hàm dưới, hai sừng, mắt, răng)",
            "ONLY THE HEAD: the whole head with the two ivory horns, the brow ridge, the yellow eye, the teeth, the orange inside of the "
            "mouth and the ivory LOWER JAW (about x = 835 to 1380, y = 385 to 805). REMOVE the body, the legs, the volcano and all five "
            "crater towers (also the small tower that stands on top of the head). COMPLETE the head into ONE CLOSED SHAPE: where the "
            "body and the tower touched it, continue the head's own rounded outline. Do not change the face."),
    "THAN": ("thân (tảng hông + tảng vai + hai khe dung nham), không đầu, chân, núi lửa, ống",
             "ONLY THE BODY: the big HIP boulder with its ivory thorn (about x = 230 to 550, y = 425 to 720), the big SHOULDER boulder "
             "with its ivory thorn (about x = 540 to 860, y = 470 to 760) and the orange lava showing between and beside them (about "
             "x = 470 to 560, y = 590 to 700 and about x = 810 to 900, y = 630 to 720), as ONE CLOSED group in the same place. REMOVE the "
             "head with its jaw and horns, the dark volcano, all five crater towers and all four legs. COMPLETE the body where those "
             "parts covered it or joined it: the shoulder boulder continues to the right as a faceted boulder to about x = 960 (under "
             "where the head was); the top edges of both boulders are complete outlines (where the towers and the volcano stood); the "
             "underside is ONE smooth belly line at about y = 770 with NO leg stumps and no gaps. Keep the thorns, the crack lines and "
             "the lava exactly."),
    "CHAN": ("bốn chân rời nhau + tháp ống phía trước",
             "ONLY FIVE THINGS, as FIVE SEPARATE closed shapes, each in the same position and at the same size as in image 1: leg 1 = the "
             "hind leg at the far left (about x = 160 to 360, y = 620 to 915) with its orange seam ring and the orange zigzag lava band "
             "at the bottom; leg 2 = the hind leg right of it (about x = 405 to 595, y = 700 to 900), also with a seam ring and a lava "
             "band; leg 3 = the front leg in the middle with a seam ring and three ivory claws (about x = 625 to 920, y = 665 to 945); "
             "leg 4 = the front leg at the right under the head, with ivory claws (about x = 930 to 1205, y = 740 to 930); and the FRONT "
             "CRATER TOWER (the small cone at about x = 445 to 640, y = 340 to 490, with its orange lip, drips, yellow pool and orange "
             "seam ring). REMOVE the body, the head, the dark volcano and the four other towers. COMPLETE every leg: where the body or "
             "the head covered its top, extend the leg upward by about 70 px and close it with a ROUNDED top end, like a thick pillar; "
             "keep the seam rings, the lava bands and the claws exactly. COMPLETE the tower: extend its base downward by about 50 px "
             "(to about y = 540) and close it with a rounded bottom. The five shapes must NOT touch each other: keep clear white space "
             "between them."),
    "NUI": ("núi lửa chính",
            "ONLY THE BIG DARK VOLCANO in the middle of the back (about x = 560 to 940, y = 100 to 560): the near-black cone with its thick "
            "orange lip, the yellow lava pool and the forked orange lava running down its front. REMOVE the head, the body, the legs and "
            "all five crater towers. COMPLETE the volcano into ONE CLOSED SHAPE: where the towers, the body and the head covered its "
            "lower part, continue its two sloping sides straight down and close it with a wide rounded base at about y = 640; the hidden "
            "areas are plain near-black rock with one or two crack lines. Do not change the lip, the pool or the lava."),
    "ONG1": ("hai tháp ống: trái cùng và phải (sau núi lửa)",
             "ONLY TWO THINGS, as TWO SEPARATE closed shapes in the same positions and at the same sizes as in image 1: (a) the TALLEST "
             "crater tower at the far left (about x = 245 to 440, y = 75 to 470), three stacked rock rings with orange seams: complete "
             "its hidden base by extending it about 60 px further down (to about y = 530) and close it with a rounded bottom; where the "
             "next tower covered its right edge, complete its own outline; (b) the crater tower at the RIGHT of the volcano (about "
             "x = 935 to 1090, y = 200 to 350): complete it where the volcano and the other tower covered it: continue its sides down to "
             "about y = 440 and close it with a rounded bottom, with one more rock ring and an orange seam. Keep their orange lips, "
             "drips, yellow pools and seam rings exactly. REMOVE everything else: the head, the body, the legs, the dark volcano and the "
             "three other towers."),
    "ONG2": ("hai tháp ống: thứ hai từ trái và phải cùng (trên đầu)",
             "ONLY TWO THINGS, as TWO SEPARATE closed shapes in the same positions and at the same sizes as in image 1: (a) the SECOND "
             "crater tower from the left (about x = 405 to 600, y = 135 to 420), two stacked rock rings with an orange seam: complete it "
             "where the volcano, the tall left tower and the body covered it: complete its own outline on both sides, extend it down to "
             "about y = 500 and close it with a rounded bottom; (b) the RIGHTMOST crater tower, the small one above the head (about "
             "x = 1075 to 1225, y = 290 to 420): complete its hidden base by extending it about 60 px further down (to about y = 480) "
             "and close it with a rounded bottom. Keep their orange lips, drips, yellow pools and seam rings exactly. REMOVE everything "
             "else: the head, the body, the legs, the dark volcano and the three other towers."),
}


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    if lenh == "bo_cuc":
        N.bo_cuc()
    elif lenh == "concept":
        concept()
    elif lenh == "manh_prompt":
        N.manh_prompt()
    else:
        print(__doc__)
