# -*- coding: utf-8 -*-
"""Gói prompt Codex cho Rồng Giọt (dạng 1 mới của dòng Giọt Sương, thay Giọt Nước aola thuy_7), làm theo cách A của
skill pokiclash-spine-rig: GPT vẽ hình trọn con ở dáng dễ rig, rồi tờ mảnh (đầu khớp tròn thừa ra) để dựng xương .atomik.

Lượt 1: concept trọn con, dáng dễ rig (thiết kế mới, không có ảnh thiết kế; người dùng chọn "rồng con giọt nước" 2026-11-07).
Lượt 2: hai tờ mảnh (đầu, thân). Chỉ sinh khi đã có inbox/rong_giot/L1_duyet.png (Claude chép ảnh lượt 1 đã duyệt về).

    py -3 -I ArtGen/Spine/build_rong_giot.py
Đường dẫn tính từ chỗ đặt file này, không ghi cứng ổ đĩa.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, PARTS_EXAMPLE, ART, line  # noqa: E402

CODE = "rong_giot"
STYLE_ANCHOR = W(ART, "Heroes", "refs", "style_anchor.png")
STYLE_SHEET = W(ART, "Heroes", "refs", "style", "style_sheet.png")
ADULT = W(ART, "..", "Assets", "03 Art", "Heroes", "Resources", "thuy_9", "thuy_9_portrait.png")

WHO = ("a BABY WATER DRAGON, the first form of a line that later grows into a water dragon. Chubby and compact, a big head "
       "(about 45% of its whole height), short thick limbs, readable when small. "
       "HEAD: shaped like a big round water drop; the pointed tip of the drop rises from the top-back of the head and curls "
       "backward as a small water-curl CREST. Two short rounded pale-aqua (#BFEFF2) horn nubs just above the brows. Two "
       "fin-shaped EARS pointing sideways and slightly back, pale aqua (#9FE3F0) with three darker-blue (#2F7FD0) spines. "
       "FACE: big round blue eyes (#2E7BD6) with one small white catchlight dot each, eyebrows lowered and slanted down "
       "toward the nose (determined, ready to fight), a confident small smile showing one little white fang. "
       "SKIN: sky blue (#5BB8F0) with a few darker-blue (#2F7FD0) rounded stripe markings on the top of the head, the back "
       "and the top of the tail. BELLY: a cream-white (#FFF6DC) belly plate of horizontal segments from the chin to the "
       "crotch. "
       "WINGS: two small fin-like back wings, one sticking out behind each shoulder: pale aqua (#9FE3F0) membrane with "
       "darker-blue (#2F7FD0) bones and a scalloped edge. "
       "ARMS: short and thick, each ending in a round fist with three tiny cream claws. "
       "LEGS: short and stubby, round feet with three cream claws each. "
       "TAIL: thick at the root, ending in a fin shaped like a water drop, pale aqua with a darker-blue edge. "
       "WEAPON: a short sword held in the fist on the viewer's RIGHT: pale steel blade (#DCE6EE) with a blue groove, a gold "
       "(#F2B33D) crossguard shaped like a scallop shell, a dark-blue wrapped grip and a round gold pommel.")

POSE = """POSE (very important, the drawing will be cut into pieces for a 2D cut-out skeleton animation, like a paper puppet):
- Three-quarter view turned toward the viewer's RIGHT; the face looks to the viewer's right with a determined, ready-to-fight expression. A calm ready stance, not an action pose.
- Feet planted apart, both feet flat on the same ground line, knees only slightly bent. The two legs do not overlap: a clear gap is visible between them.
- Both arms are held a little away from the body so that clear white space separates each arm and each fist from the belly, the head and the legs. Elbows only slightly bent.
- The arm on the viewer's LEFT hangs down and slightly outward, ending in a closed fist at hip height.
- The arm on the viewer's RIGHT also hangs down and slightly outward; its fist grips the sword at hip height. The sword points down and forward to the viewer's right at about 45 degrees. The whole blade is clear of the legs, the body and the edges of the canvas.
- The tail sits behind the body on the viewer's LEFT; only its root is hidden behind the hip. Its drop-shaped fin is clear of the fist and the arm, with white space in between.
- The two back wings stick out behind the shoulders, one on each side, both clearly visible above the arms (not touching the arms or the ears).
- The two fin ears stick out sideways from the head, fully visible. The crest curls up from the top-back of the head, fully visible.
- Nothing covers the face."""

ANATOMY = """ANATOMY TO KEEP READABLE (each piece must be a clear shape with its own outline):
- each arm = a short blue upper arm + a round fist, with an outline where the fist starts (a wrist line);
- each leg = a short blue thigh + a round foot, with an outline where the foot starts (an ankle line);
- the head (face + horn nubs), the crest, each ear, each wing, the torso with its belly plate, the tail and the sword are each a clearly outlined shape."""


def luot_1(out_dir, save_dir):
    save = W(save_dir, "L1_full.png")
    t = f"""IMAGES (attached in this order; open each from its path):
image 1 = {STYLE_ANCHOR}: an approved hero of the same game (a blue water-drop knight), 1143x1376, white background; learn ONLY its pen line weight, its crayon texture and its level of detail. Do NOT copy its design, and do NOT copy its shine spots or its darker shading (they are against the rules below).
image 2 = {WORLD_STYLE}: the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen outline + coloured pencil / wax crayon hatching), nothing of its content.
image 3 = {STYLE_SHEET}: a sheet of 8 creature heroes from another source, 1536x1024; learn ONLY the design language (chunky compact bodies, big heads, big eyes, simple shapes, few details). Never copy any of these creatures and never copy their glossy rendering.
image 4 = {ADULT}: the grown-up dragon form of this same line, 512x512; echo its colour family (sky blue, pale aqua, cream claws) so the baby clearly belongs to it. Do NOT copy its shape: the baby is a new, chubby, bipedal design.

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_full_2.png, L1_full_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE new creature hero as ONE full-body picture, in a clean "puppet-ready" pose, in the drawing style of image 2 and image 1.

CHARACTER: {WHO}

PERSONALITY: a pet-like fighting creature with a "ready to battle" look: cute but brave and confident; not a cheerful mascot, not scary.

CANVAS AND FRAMING: portrait 1024x1536, pure-white background. The whole character is visible, nothing cut by the edges. It stands centred, about 1250 px tall from the top of the crest to the soles of the feet; the soles rest on one level ground line about 100 px above the bottom edge.

{POSE}

{ANATOMY}

{line(7)}

Keep the design simple: no extra accessories, no cape, no armour, no text.
"""
    p = W(out_dir, "luot_1_tong.txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    return p, save


COMMON_PIECES = """PIECE RULES (for every piece):
- Draw each piece COMPLETE, including the parts that were hidden behind other pieces in image 1.
- Wherever a piece joins another piece (the JOINT end), continue it about 30 px past the joint with a rounded end, as if it slides under the neighbour piece. Draw the outline around that rounded end too. This hidden overlap keeps the puppet from showing gaps when the joint bends.
- Keep the size, the angle and the direction each piece has in image 1 (same scale as image 1). Do not rotate, mirror or straighten pieces.
- Leave at least 60 px of pure white between any two pieces; pieces never touch or overlap each other.
- Each piece only once. No shadows under the pieces, no text, no numbers, no labels, no frame, no guide lines."""


def luot_2(out_dir, save_dir, full):
    save_a = W(save_dir, "L2a_head_pieces.png")
    save_b = W(save_dir, "L2b_body_pieces.png")
    t = f"""IMAGES (attached in this order; open each from its path):
image 1 = {full}: the hero in its puppet-ready pose, 1024x1536, white background. THIS is the drawing to cut up.
image 2 = {WORLD_STYLE}: the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style.
image 3 = {PARTS_EXAMPLE}: an example of a creature cut into separate puppet pieces laid out on white (glossy vector creatures from another source); learn ONLY the idea of "pieces laid out apart", never its designs or its glossy look.

This turn makes TWO pictures, one after the other. Both cut the hero of image 1 into the separate pieces of a 2D cut-out (paper puppet) skeleton animation. Same character, same colours, same drawing style as image 1.

{COMMON_PIECES}

{line(7)}

==================== STEP A: head pieces ====================
SAVE (step A): save it as a PNG to {save_a}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)

CANVAS: landscape 1536x1024, pure white.
PIECES, laid out in two rows:
Row 1 (top), left to right:
 A1. HEAD: the face with its two horn nubs, exactly as in image 1, but WITHOUT the crest and WITHOUT the two ears. Where the ears and the crest were attached, draw the plain blue head surface with its stripe markings (closed outline). The bottom of the head (where the neck joins the body) is completed as a smooth rounded chin.
 A2. HEAD, EYES CLOSED: an exact copy of A1, same size and shape; the only change is that both eyes are closed (a curved, determined closed-eye line under the same lowered brows). Used for blinking.
 A3. HEAD, SHOUTING: an exact copy of A1, same size and outline; the only change is the face: eyes wide open and fierce under the lowered brows, mouth wide open in a battle cry showing the little fang (inside of the mouth dark red, small pink tongue). Used when it strikes.
Row 2 (bottom), left to right:
 A4. CREST: the water-curl crest from the top-back of the head; its bottom end (joint) extended as a rounded stub that would tuck into the head.
 A5. EAR on the viewer's LEFT: the fin ear as in image 1; its root end (joint, toward the head) extended as a rounded stub.
 A6. EAR on the viewer's RIGHT: the fin ear as in image 1; its root end (joint, toward the head) extended as a rounded stub.

==================== STEP B: body pieces ====================
SAVE (step B): save it as a PNG to {save_b}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)

CANVAS: landscape 1536x1024, pure white.
PIECES, laid out in three rows:
Row 1 (top), left to right:
 B1. WING on the viewer's LEFT: the whole fin wing; its root end (joint, toward the shoulder) extended as a rounded stub.
 B2. TORSO: the blue body with its cream belly plate, from the neck to the hips. Complete it where the head, arms, legs, wings and tail covered it: the top (neck) is a rounded end that would tuck under the head; the shoulders are rounded; the bottom includes the hips and the crotch, rounded.
 B3. WING on the viewer's RIGHT: same rules as B1.
 B4. TAIL: the whole tail with its drop-shaped fin; its root end (joint, toward the hip) extended as a rounded stub.
 B5. SWORD: the whole sword, including the part of the grip hidden by the fist in image 1; same angle as in image 1.
Row 2 (middle), left to right:
 B6. UPPER ARM on the viewer's LEFT: the short blue arm from the shoulder to the wrist; both ends rounded joints (shoulder end tucks into the torso, wrist end tucks into the fist).
 B7. FIST on the viewer's LEFT: the round fist with its three cream claws; its wrist end (joint) a rounded edge.
 B8. UPPER ARM on the viewer's RIGHT: same rules as B6.
 B9. FIST on the viewer's RIGHT: the fist that holds the sword, drawn closed around an EMPTY grip (no sword in this piece; the sword is B5), so the fingers wrap a gap where the grip will go.
Row 3 (bottom), left to right:
 B10. THIGH on the viewer's LEFT: the short blue leg from the hip to the ankle; top end a rounded joint that tucks under the torso, bottom end a rounded joint that tucks into the foot.
 B11. FOOT on the viewer's LEFT: the round foot with its three cream claws and flat sole; its top (ankle joint) a rounded edge.
 B12. THIGH on the viewer's RIGHT: same rules as B10.
 B13. FOOT on the viewer's RIGHT: same rules as B11.

Check before saving each step: the right number of pieces (6 in step A, 13 in step B), none touching, every piece complete with a closed outline, flat colours, white background.
"""
    p = W(out_dir, "luot_2_tach_manh.txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    return p, save_a, save_b


def huong_dan(out_dir, save_dir, p1, s1, p2):
    l2 = (f"- File prompt: `{p2}`\n" if p2 else "- Chưa có: Claude dựng file này sau khi duyệt ảnh lượt 1.\n")
    t = f"""# Rồng Giọt (dạng 1 mới của dòng Giọt Sương, định dạng .atomik)

Thay Giọt Nước (`thuy_7`, hình aola) bằng tướng vẽ mới, rig xương riêng, xuất `.atomik` (người dùng chọn 2026-11-07).
Claude gọi Codex bằng `ArtGen/Heroes/tools/gen_codex.py`; người dùng không phải gửi tay.

## Lượt 1: concept trọn con, dáng dễ rig
- File prompt: `{p1}`
- Ảnh mẫu Codex mở:
  - image 1 `{STYLE_ANCHOR}`: Giọt Sương dạng 1 đã duyệt, 1143x1376, nền trắng (chỉ lấy nét bút, vân chì sáp, độ chi tiết).
  - image 2 `{WORLD_STYLE}`: bản đồ vẽ tay 1024x1536, nền biển xanh (chỉ lấy nét mực nâu và tô chì sáp).
  - image 3 `{STYLE_SHEET}`: tờ 8 tướng aola, 1536x1024 (chỉ học cách thiết kế gọn, mắt to).
  - image 4 `{ADULT}`: Sương Long (dạng 3 của dòng), 512x512, nền trắng (chỉ lấy họ màu).
- Lưu: `{s1}`
- Kiểm: đủ người, không cắt mép; tay tách thân, chân không chéo; kiếm, đuôi, cánh không chạm tay; tô phẳng, không bóng, không điểm sáng (trừ chấm mắt); mặt quả quyết.
- Câu sửa nhanh: "Arms must not touch the body." / "Flat colour only: no shine spots, no shading, no shadow under the feet." / "Wings must not touch the arms or the ears."

## Lượt 2: tách mảnh (2 ảnh)
{l2}- Bước A `L2a_head_pieces.png`: đầu, đầu nhắm mắt, đầu hét, mào, 2 tai (6 mảnh). Bước B `L2b_body_pieces.png`: 2 cánh, thân, đuôi, kiếm, 2 cánh tay, 2 nắm tay, 2 đùi, 2 bàn chân (13 mảnh). Cùng thư mục `{save_dir}`.
- Kiểm: đủ 6 và 13 mảnh, không mảnh nào chạm nhau, chỗ khớp có đầu tròn thừa ra.

## Sau đó
Claude cắt mảnh, khớp vào ảnh lượt 1, dựng xương, làm animation (đứng, trúng đòn, đánh, bắn tia, chiêu cuối, tiến hóa) với hiệu ứng nước sẵn có của dòng Giọt Sương, xuất `.atomik`, nối vào game.
"""
    p = W(out_dir, "HUONG_DAN.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    return p


def main():
    out_dir = W(HERE, "gui_gpt", CODE)
    save_dir = W(HERE, "inbox", CODE, "tai_ve")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    for f in (STYLE_ANCHOR, WORLD_STYLE, STYLE_SHEET, ADULT, PARTS_EXAMPLE):
        if not os.path.isfile(f):
            sys.exit("thiếu ảnh mẫu: " + f)
    p1, s1 = luot_1(out_dir, save_dir)
    full = W(HERE, "inbox", CODE, "L1_duyet.png")
    p2 = luot_2(out_dir, save_dir, full)[0] if os.path.isfile(full) else None
    hd = huong_dan(out_dir, save_dir, p1, s1, p2)
    for p in (p1, p2, hd):
        if p:
            print(p)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
