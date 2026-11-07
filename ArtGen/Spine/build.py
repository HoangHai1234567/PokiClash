# -*- coding: utf-8 -*-
"""Sinh gói prompt GPT cho thử nghiệm rig Spine (repo spine-animation-ai).

Lượt 1: hình trọn con, dáng đứng dễ rig.
Lượt 2: tách mảnh (2 ảnh: nhóm đầu, nhóm thân). Chỉ sinh khi đã có ảnh lượt 1.

Chạy:  py -3 -I ArtGen/Spine/build.py giot_suong
Đường dẫn tính từ chỗ đặt file này, không ghi cứng ổ đĩa.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))


def W(*p):
    return os.path.normpath(os.path.join(*p))


WORLD_STYLE = W(ART, "Islands", "refs", "world_style.png")
PARTS_EXAMPLE = W(ART, "Heroes", "refs", "style", "parts_example.png")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, "
        "they do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the "
        "figure, on the ground or on the background), no white highlights or shine spots, no gloss, no glow, no rim light, "
        "no gradients, no 3D look. The only white allowed is one small catchlight dot in each eye. A darker tone appears "
        "only where the design itself has a darker colour.")


def line(px):
    return ("LINE AND COLOUR: the game's hand-drawn look of the style image, NOT the glossy look of the design image: drawn "
            "by hand on paper with a dark-brown ink pen (#2B2118), an outline about " + str(px) + " px thick on this canvas, "
            "the same weight on every edge, slightly wobbly like a real pen; every area coloured with coloured pencils and "
            "wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the "
            "outline. Clean and appealing, neither a crude scribble nor overly detailed.\n" + FLAT + "\n"
            "Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or "
            "sticker outline around the figure or its pieces (the game adds that itself). No text, no labels, no frame.")


HEROES = {
    "giot_suong": {
        "ten": "Giọt Sương (dạng 1)",
        "design": W(ART, "Heroes", "inbox", "giot_suong_1", "concept_duyet.png"),
        "design_note": ("the approved design of this hero: a small blue water-drop creature knight, about 1143x1376, white "
                        "background; glossy rendering that must NOT be copied"),
        "who": ("a small, chunky, blue water-drop creature knight: big round blue head with a confident, determined face "
                "(big blue eyes with lowered brows, small smile with one little fang); a round silver-grey helmet with a "
                "gold diamond gem on the forehead; a white-and-grey wing with blue tips on each side of the helmet; a "
                "blue water swirl plume rising from the top of the helmet; a short blue body with a silver-grey chest "
                "plate ending in a point at the belly; short blue arms ending in silver-grey glove fists; short blue legs "
                "in silver-grey boots; a big blue curled water tail behind; a short sword (gold crossguard and grip, "
                "pale steel blade)"),
    },
}


def luot_1(code, h, out_dir, save_dir):
    save = W(save_dir, "L1_full.png")
    t = f"""IMAGES (attached in this order; open each from its path):
image 1 = {h['design']}: {h['design_note']}.
image 2 = {WORLD_STYLE}: the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen outline + coloured pencil / wax crayon hatching), nothing of its content.

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_full_2.png, L1_full_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw the hero of image 1 as ONE full-body picture that will later be cut into pieces for a 2D cut-out skeleton (bone) animation, like a paper puppet. Same character, same design and colours as image 1; a new, clean "puppet-ready" pose; the drawing style of image 2.

CHARACTER (keep from image 1): {h['who']}.

CANVAS AND FRAMING: portrait 1024x1536, pure-white background. The whole character is visible, nothing cut by the edges. It stands centred, about 1300 px tall from the tip of the plume to the soles of the boots; the boot soles rest on one level ground line about 90 px above the bottom edge.

POSE (very important, this is what makes the cut-out rig work):
- Three-quarter view turned toward the viewer's RIGHT, like image 1; the face looks to the viewer's right with a determined, ready-to-fight expression. A calm ready stance, not an action pose.
- Feet planted apart, both boots flat on the same ground line, knees only slightly bent. The two legs do not overlap each other: a gap of white (or body colour) is visible between them.
- Both arms are held a little away from the body so that clear white space separates each arm and each fist from the torso, the head and the legs. Elbows only slightly bent.
- The arm on the viewer's LEFT hangs down and slightly outward, ending in a closed fist at hip height.
- The arm on the viewer's RIGHT also hangs down and slightly outward; its fist grips the sword at hip height. The sword points down and forward to the viewer's right at about 45 degrees. The whole blade is clear of the legs, the body and the edges of the canvas.
- The tail sits behind the body on the viewer's LEFT; only its root is hidden behind the hip. Its curl is clear of the fist and the arm with white space in between.
- The two helmet wings stick out sideways, one on each side of the helmet, fully visible. The plume rises straight up from the top of the helmet, fully visible.
- Nothing covers the face.

ANATOMY TO KEEP READABLE (each piece must be a clear shape with its own outline):
- each arm = a short blue upper arm + a silver-grey glove fist, with an outline where the glove starts;
- each leg = a short blue thigh + a silver-grey boot, with an outline where the boot starts;
- the head (face + helmet), the plume, each wing, the torso with its chest plate, the tail and the sword are each a clearly outlined shape.

{line(7)}

Do not change the design: no new accessories, no cape, no extra details, no different colours.
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


def luot_2(code, h, out_dir, save_dir, full):
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
SAVE: save step A as a PNG to {save_a}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)

CANVAS: landscape 1536x1024, pure white.
PIECES, laid out in two rows:
Row 1 (top), left to right:
 A1. HEAD: the face and the round helmet with its gold gem, exactly as in image 1, but WITHOUT the plume and WITHOUT the two wings. Where the wings and the plume were attached, draw the plain helmet surface (closed outline). The bottom of the head (where the neck joins the body) is completed as a smooth rounded chin.
 A2. HEAD, EYES CLOSED: an exact copy of A1, same size and shape, the only change is that both eyes are closed (a curved, determined closed-eye line under the same brows). Used for blinking.
Row 2 (bottom), left to right:
 A3. PLUME: the blue water swirl from the top of the helmet; its bottom end (joint) extended as a rounded stub that would tuck into the helmet.
 A4. WING on the viewer's LEFT: as in image 1; its root end (joint, toward the helmet) extended as a rounded stub.
 A5. WING on the viewer's RIGHT: as in image 1; its root end (joint, toward the helmet) extended as a rounded stub.

==================== STEP B: body pieces ====================
SAVE: save step B as a PNG to {save_b}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)

CANVAS: landscape 1536x1024, pure white.
PIECES, laid out in three rows:
Row 1 (top), left to right:
 B1. TORSO: the blue body with its silver-grey chest plate, from the neck to the hips. Complete it where the head, arms, legs and tail covered it: the top (neck) is a rounded end that would tuck under the head; the shoulders are rounded; the bottom includes the hips and the crotch, rounded.
 B2. TAIL: the whole blue curled water tail; its root end (joint, toward the hip) extended as a rounded stub.
 B3. SWORD: the whole sword, including the part of the grip hidden by the fist in image 1; same angle as in image 1.
Row 2 (middle), left to right:
 B4. UPPER ARM on the viewer's LEFT: the short blue arm from the shoulder to the wrist; both ends rounded joints (shoulder end tucks into the torso, wrist end tucks into the glove).
 B5. FIST on the viewer's LEFT: the silver-grey glove fist; its wrist end (joint) a rounded opening edge.
 B6. UPPER ARM on the viewer's RIGHT: same rules as B4.
 B7. FIST on the viewer's RIGHT: the silver-grey glove fist that holds the sword, drawn closed around an EMPTY grip (no sword in this piece; the sword is B3), so the fingers wrap a gap where the grip will go.
Row 3 (bottom), left to right:
 B8. THIGH on the viewer's LEFT: the short blue leg from the hip to the boot; top end a rounded joint that tucks under the torso, bottom end a rounded joint that tucks into the boot.
 B9. BOOT on the viewer's LEFT: the silver-grey boot with its sole; its top (joint) a rounded opening edge.
 B10. THIGH on the viewer's RIGHT: same rules as B8.
 B11. BOOT on the viewer's RIGHT: same rules as B9.

Check before saving each step: the right number of pieces (5 in step A, 11 in step B), none touching, every piece complete with a closed outline, flat colours, white background.
"""
    p = W(out_dir, "luot_2_tach_manh.txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    return p, save_a, save_b


def huong_dan(code, h, out_dir, save_dir, p1, s1, p2):
    l2 = (f"- File prompt: `{p2}`\n" if p2 else
          "- Chưa có: Claude dựng file này sau khi duyệt ảnh lượt 1.\n")
    t = f"""# Thử rig Spine: {h['ten']}

Mục đích: xem bộ công cụ `spine-animation-ai` rig xương và làm animation từ hình GPT vẽ được tới đâu.
Đây là thử nghiệm riêng, không thay quy trình vẽ đè lên rig aola.

## Lượt 1: hình trọn con, dáng đứng dễ rig
- File prompt (gửi GPT đúng đường dẫn này): `{p1}`
- Ảnh mẫu GPT sẽ mở:
  - image 1 `{h['design']}`: Giọt Sương bản đã duyệt, 1143x1376, nền trắng, đứng nghiêng sang phải, tay phải cầm kiếm, có bóng loáng (chỉ lấy thiết kế).
  - image 2 `{WORLD_STYLE}`: bản đồ vẽ tay 1024x1536, nền biển xanh (chỉ lấy nét mực nâu và tô chì sáp).
- GPT lưu ảnh vào: `{s1}`
- Kiểm:
  - đủ người, không bị cắt mép; ảnh dọc 1024x1536; nền trắng;
  - hai tay tách khỏi thân (có khoảng trắng), hai chân không chéo nhau, kiếm và đuôi không đè lên tay, chân;
  - tô phẳng, không bóng loáng, không bóng đổ dưới chân; viền nâu đều.
- Câu sửa nhanh:
  - "Arms must not touch the body: leave clear white space between each arm and the torso."
  - "Flat colour only: no shine spots, no shading, no shadow under the feet."
  - "Keep the whole sword blade clear of the legs."

## Lượt 2: tách mảnh (2 ảnh)
{l2}- Bước A lưu `L2a_head_pieces.png` (đầu, đầu nhắm mắt, mào, 2 cánh), bước B lưu `L2b_body_pieces.png` (thân, đuôi, kiếm, 2 cánh tay, 2 nắm tay, 2 đùi, 2 ủng), cùng thư mục `{save_dir}`.
- Kiểm: đủ 5 và 11 mảnh, không mảnh nào chạm nhau, chỗ khớp có đầu tròn thừa ra.

## Sau đó
Claude cắt mảnh, khớp vị trí với ảnh lượt 1, dựng xương Spine 4.2, làm animation (đứng thở, đánh, trúng đòn, chiêu) và mở trang xem thử.
"""
    p = W(out_dir, "HUONG_DAN.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    return p


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else "giot_suong"
    h = HEROES[code]
    out_dir = W(HERE, "gui_gpt", code)
    save_dir = W(HERE, "inbox", code, "tai_ve")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    for f in (h["design"], WORLD_STYLE, PARTS_EXAMPLE):
        if not os.path.isfile(f):
            sys.exit("thiếu ảnh mẫu: " + f)
    p1, s1 = luot_1(code, h, out_dir, save_dir)
    full = W(HERE, "inbox", code, "L1_duyet.png")  # Claude chép ảnh lượt 1 đã duyệt về đây
    p2 = None
    if os.path.isfile(full):
        p2, _, _ = luot_2(code, h, out_dir, save_dir, full)
    hd = huong_dan(code, h, out_dir, save_dir, p1, s1, p2)
    print(p1)
    if p2:
        print(p2)
    print(hd)


if __name__ == "__main__":
    main()
