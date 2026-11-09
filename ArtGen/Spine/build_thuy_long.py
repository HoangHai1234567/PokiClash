# -*- coding: utf-8 -*-
"""Gói prompt Codex cho Thủy Long (dòng Giọt Sương vẽ lại cả 3 dạng, rig xương riêng .atomik, người dùng chọn 2026-11-08):
long chiến binh đứng hai chân, chiến, không cute, không bám aola.

Mỗi dạng k (1, 2, 3):
- luot_1_tong.txt: concept trọn con ở dáng dễ rig. Dạng 2, 3 đính concept đã duyệt của dạng trước (cùng một con lớn lên).
  Chỉ dựng khi dạng trước đã có L1_duyet.png.
- luot_2_tach_manh.txt: ba tờ mảnh (A đầu, B tay chân, C thân, đuôi, vũ khí, đồ vải). Chỉ dựng khi dạng đó có L1_duyet.png.
Tay, chân vẽ liền cả chi (vai tới cổ tay, hông tới cổ chân): bộ rig uốn khuỷu, gối bằng lưới có trọng số, không cắt khớp.

    py -3 -I ArtGen/Spine/build_thuy_long.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, PARTS_EXAMPLE, ART, line  # noqa: E402

STYLE_ANCHOR = W(ART, "Heroes", "refs", "style_anchor.png")
STYLE_SHEET = W(ART, "Heroes", "refs", "style", "style_sheet.png")

COMMON = ("a WATER DRAGON WARRIOR: a bipedal dragon fighter standing on two legs, fierce and battle-hardened, intimidating but "
          "heroic. NOT cute, NOT chibi, NOT a mascot: the head is only about a quarter of the total height, athletic body, "
          "long strong limbs. Dragon head with a strong snout and a powerful jaw, narrow amber-gold eyes (#F0A830) with black "
          "slit pupils under heavy, angry brow ridges, sharp white fangs. Colours: deep sea-blue scales (#2A5FA8) with dark "
          "navy stripes (#1B355E), teal fins and crest (#2BA39A) with darker teal spines (#1D7A73), pale aqua belly plates "
          "(#BFE9E4), cream-white claws and horns (#EFE6CF).")

FORMS = {
    1: {
        "name": "Long Binh",
        "vn": "lính rồng trẻ: gầy rắn, sừng ngắn vuốt ngược, mào vây ở gáy, vây má, giáp da (đệm vai, bao cổ tay, đai), dải vải "
              "thắt lưng xanh mòng két, đuôi vừa có vây chót, giáo ngắn mũi lá thép, tua xanh",
        "who": ("FORM 1, a young dragon soldier: lean and wiry. Two short horns swept back. A teal fin crest that runs from the "
                "top of the head down the back of the head. A small teal fin on each cheek. Leather armour: one brown leather "
                "shoulder pad on the shoulder of the arm on the viewer's RIGHT, brown leather bracers on both forearms, a wide "
                "brown leather belt with a bronze buckle; a dark-teal cloth sash hangs from the front of the belt to the knees. "
                "A medium tail with a teal fin at its tip. WEAPON: a short spear (about as long as the warrior is tall): dark "
                "wood shaft, steel leaf-shaped spearhead, a teal tassel under the spearhead."),
        "weapon": "spear",
        "weapon_pose": ("The arm on the viewer's RIGHT holds the spear in front of the body at hip height; the spear is held "
                        "diagonally, the spearhead up and forward (to the viewer's right) at about 50 degrees, the butt down and "
                        "back. The whole spear is clear of the head, the legs and the canvas edges."),
        "shoulder": "the brown leather shoulder pad of the arm on the viewer's RIGHT",
        "cloth": "the dark-teal cloth sash that hangs from the front of the belt",
        "crest": "the teal fin crest from the top and back of the head",
        "cape": None,
    },
    2: {
        "name": "Long Kỵ Sĩ",
        "vn": "kỵ sĩ rồng: cao, cơ bắp, sừng dài cong ra sau, mào vây lớn, giáp ngực vảy thép viền đồng, giáp vai thép lớn, găng, "
              "ống chân thép, vạt áo xanh mòng két, đuôi dài hai vây, kiếm lưỡi nước cong",
        "who": ("FORM 2, the same dragon grown into a dragon knight: taller and muscular. Longer horns curving back. A larger teal "
                "fin crest down the back of the head and neck. Armour: a steel-blue (#6E8AA6) chest plate made of overlapping "
                "scale plates with a bronze (#C08A3E) rim, a large steel shoulder plate on the shoulder of the arm on the viewer's "
                "RIGHT, steel gauntlets and steel shin guards, a teal cloth tabard hanging from the belt in front to the knees. "
                "A long tail with two teal fins. WEAPON: a long slightly curved sword whose blade is made of flowing water "
                "(pale aqua #BDEBF0 with a darker teal edge and a white foam crest along the back of the blade), steel guard "
                "and a dark grip."),
        "weapon": "water sword",
        "weapon_pose": ("The arm on the viewer's RIGHT holds the sword in front at hip height, the blade pointing down and "
                        "forward to the viewer's right at about 45 degrees. The whole sword is clear of the legs, the body and "
                        "the canvas edges."),
        "shoulder": "the large steel shoulder plate of the arm on the viewer's RIGHT",
        "cloth": "the teal cloth tabard that hangs from the front of the belt",
        "crest": "the teal fin crest from the top and back of the head and neck",
        "cape": None,
    },
    3: {
        "name": "Long Tướng",
        "vn": "long tướng: to lớn, sừng lớn cong có vòng đồng, bờm vây dọc đầu và cổ, sẹo ngang một mắt, giáp thép sẫm viền đồng khắc "
              "sóng, hai giáp vai, áo choàng xanh mòng két rách gấu có hoa văn sóng trắng, đuôi dài khoẻ, đại đao lưỡi sóng",
        "who": ("FORM 3, the same dragon as a dragon warlord: powerful, broad and tall. Large curved cream horns with bronze "
                "rings. A mane of teal fins along the back of the head and the neck. A pale scar across the eye on the viewer's "
                "LEFT. Heavy dark steel armour (#4A5866) with bronze trims (#C08A3E) engraved with wave patterns, a big shoulder "
                "plate on each shoulder, armoured forearms and shins. A long deep-teal cape (#1F6F6A) with a ragged hem and a "
                "white wave pattern near the hem hangs from the shoulders behind the body. A long powerful tail with a fin. "
                "WEAPON: a huge glaive (a long pole weapon with a big curved blade shaped like a breaking wave, steel blade with "
                "a teal edge, dark pole with bronze rings)."),
        "weapon": "glaive",
        "weapon_pose": ("The arm on the viewer's RIGHT holds the glaive in front of the body at hip height; the glaive is held "
                        "diagonally, the blade up and forward (to the viewer's right) at about 55 degrees, the butt of the pole "
                        "down and back near the back foot. The whole glaive is clear of the head and the canvas edges."),
        "shoulder": "the big shoulder plate of the arm on the viewer's RIGHT",
        "cloth": "the armoured skirt flap (tasset) that hangs from the front of the belt",
        "crest": "the mane of teal fins along the back of the head and the neck",
        "cape": "the long deep-teal cape that hangs behind the body from the shoulders",
    },
}

POSE = """POSE (very important, the drawing will be cut into pieces for a 2D skeleton animation with bending limbs):
- Three-quarter view turned toward the viewer's RIGHT; the head and eyes look to the viewer's right with a fierce, ready-to-fight expression. A grounded battle-ready stance, not a big action pose.
- Feet planted wide apart, both feet flat on the same ground line, knees slightly bent. The two legs do not overlap: a clear gap between them.
- {weapon_pose}
- The arm on the viewer's LEFT is held a little away from the body, slightly bent, ending in a clenched fist at hip height, with clear white space between the arm and the body.
- The tail comes out behind the hips on the viewer's LEFT and curves down and back; its tip is clear of the legs and the arm.
- The crest / mane and the horns are fully visible. Nothing covers the face.{cape_line}"""

ANATOMY = """ANATOMY TO KEEP READABLE (each piece must be a clear shape with its own outline):
- each arm = one continuous arm from the shoulder to the wrist (upper arm and forearm, slightly bent at the elbow) + a separate-looking hand / fist with an outline at the wrist;
- each leg = one continuous leg from the hip to the ankle (thigh and shin, slightly bent at the knee) + a clawed foot with an outline at the ankle;
- the head, the crest / mane, the torso with its armour, the tail, the weapon, the shoulder armour and the hanging cloth are each a clearly outlined shape."""


def paths(k):
    code = f"thuy_long_{k}"
    out_dir = W(HERE, "gui_gpt", code)
    save_dir = W(HERE, "inbox", code, "tai_ve")
    return code, out_dir, save_dir, W(HERE, "inbox", code, "L1_duyet.png")


def luot_1(k):
    f = FORMS[k]
    code, out_dir, save_dir, _ = paths(k)
    save = W(save_dir, "L1_full.png")
    refs = [(STYLE_ANCHOR, "an approved hero of the same game, 1143x1376, white background; learn ONLY its pen line weight, "
                           "its crayon texture and its level of detail. Do NOT copy its design, its cute proportions, its shine "
                           "spots or its darker shading"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen outline + "
                          "coloured pencil / wax crayon hatching), nothing of its content"),
            (STYLE_SHEET, "a sheet of 8 creature heroes from another source, 1536x1024; learn ONLY how simple, readable shapes are "
                          "designed. Never copy any of these creatures and never copy their glossy rendering")]
    for j in range(1, k):
        prev = paths(j)[3]
        refs.append((prev, f"FORM {j} of this same dragon (approved), 1024x1536, white background: keep the same species, face, "
                           f"colours and drawing style so the line clearly grows up; the new form is bigger and more armoured"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    cape_line = ("\n- The cape hangs behind the body from both shoulders and flows down behind the back leg and the tail, its "
                 "outline clear; it does not cover the arms or the front leg.") if f["cape"] else ""
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_full_2.png, L1_full_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE hero as ONE full-body picture, in a clean "puppet-ready" pose, in the drawing style of image 2 and image 1.

CHARACTER: {COMMON}
{f['who']}

CANVAS AND FRAMING: portrait 1024x1536, pure-white background. The whole character and its weapon are visible, nothing cut by the edges. The warrior stands centred, about 1150 px tall from the top of the horns / crest to the soles of the feet; the soles rest on one level ground line about 110 px above the bottom edge.

{POSE.format(weapon_pose=f['weapon_pose'], cape_line=cape_line)}

{ANATOMY}

{line(7)}

Keep the design clean and readable: no text, no background, no extra props.
"""
    p = W(out_dir, "luot_1_tong.txt")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p, save


LIEN_POSE = {  # vẽ lại concept đã duyệt ở dáng rig được từ một ảnh liền (2026-11-08: người dùng bảo gen liền, bỏ tờ mảnh)
    3: ("The arm on the viewer's RIGHT holds the glaive UPRIGHT beside the body on the viewer's right: the fist is at "
        "belly height, a little to the right of the body; the pole stands almost vertical (leaning only about 10 degrees, the "
        "top toward the viewer's right), its butt end just above the ground to the right of the front foot, the big wave blade "
        "high up to the right of the head, NOT overlapping the head, the horns or the mane. The ENTIRE glaive stays to the "
        "right of the body: it never crosses the torso, the belt, the legs, the cape or the other arm; clear white space "
        "between the pole and the front leg."),
}


def luot_1_lien(k):
    """concept đã duyệt vẽ lại ở dáng rig được từ một ảnh liền (vũ khí không vắt qua người)."""
    f = FORMS[k]
    code, out_dir, save_dir, full = paths(k)
    save = W(save_dir, "L1_lien.png")
    refs = [(full, f"FORM {k} of this dragon, the APPROVED design, 1024x1536, white background: redraw THIS exact character "
                   f"(same face, scar, horns, mane, armour pieces and patterns, cape, tail, colours, proportions, line and "
                   f"crayon texture); only the pose of the weapon arm and the weapon changes"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen outline + "
                          "coloured pencil / wax crayon hatching), nothing of its content")]
    for j in range(1, k):
        refs.append((paths(j)[3], f"FORM {j} of the same dragon (approved), 1024x1536: only for consistency of the species"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    cape_line = ("\n- The cape hangs behind the body from both shoulders and flows down behind the legs and the tail, its "
                 "outline clear; it does not cover the arms or the front leg.") if f["cape"] else ""
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw the hero of image 1 as ONE full-body picture in a new, animation-ready pose. The picture will be animated as a single drawing with a bending 2D skeleton, so the weapon must not cross the body.

CHARACTER: {COMMON}
{f['who']}

CANVAS AND FRAMING: portrait 1024x1536, pure-white background, NO ground line, no cast shadow. The whole character and its weapon are visible, nothing cut by the edges. The warrior stands centred, about 1150 px tall from the top of the horns to the soles of the feet; the soles rest about 110 px above the bottom edge.

{POSE.format(weapon_pose=LIEN_POSE[k], cape_line=cape_line)}

{line(7)}

Keep the design clean and readable: no text, no background, no extra props.
"""
    p = W(out_dir, "luot_1_lien.txt")
    os.makedirs(save_dir, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p, save


COMMON_PIECES = """PIECE RULES (for every piece):
- Draw each piece COMPLETE, including the parts that were hidden behind other pieces in image 1.
- Wherever a piece joins another piece (the JOINT end), continue it about 30 px past the joint with a rounded end, as if it slides under the neighbour piece. Draw the outline around that rounded end too. This hidden overlap keeps the puppet from showing gaps when the joint bends.
- Keep the size, the angle, the bend and the direction each piece has in image 1 (same scale as image 1). Do not rotate, mirror or straighten pieces.
- Leave at least 60 px of pure white between any two pieces; pieces never touch or overlap each other.
- Each piece only once. No shadows under the pieces, no text, no numbers, no labels, no frame, no guide lines."""


def luot_2(k):
    f = FORMS[k]
    code, out_dir, save_dir, full = paths(k)
    sa, sb, sc = (W(save_dir, n) for n in ("L2a_head.png", "L2b_limbs.png", "L2c_body.png"))
    cape = f["cape"]
    c_rows = ("Row 1 (top), left to right: C1 TORSO, C2 TAIL, C3 CAPE.\nRow 2 (bottom), left to right: C4 WEAPON, C5 SHOULDER ARMOUR, "
              "C6 CLOTH." if cape else
              "Row 1 (top), left to right: C1 TORSO, C2 TAIL.\nRow 2 (bottom), left to right: C3 WEAPON, C4 SHOULDER ARMOUR, C5 CLOTH.")
    n_c = 6 if cape else 5
    cape_piece = (f"\n C3. CAPE: {cape}, the whole cape alone, as it hangs in image 1, completed where the body covered it; its top "
                  f"edge (joint, at the shoulders) straight and slightly thickened.") if cape else ""
    w_i, s_i, c_i = ("C4", "C5", "C6") if cape else ("C3", "C4", "C5")
    t = f"""IMAGES (attached in this order; open each from its path):
image 1 = {full}: the hero in its puppet-ready pose, 1024x1536, white background. THIS is the drawing to cut up.
image 2 = {WORLD_STYLE}: the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style.
image 3 = {PARTS_EXAMPLE}: an example of a creature cut into separate puppet pieces laid out on white (glossy vector creatures from another source); learn ONLY the idea of "pieces laid out apart", never its designs or its glossy look.

This turn makes THREE pictures, one after the other (steps A, B, C). They cut the hero of image 1 into the separate pieces of a 2D skeleton animation with bending limbs. Same character, same colours, same drawing style as image 1.

{COMMON_PIECES}

{line(7)}

==================== STEP A: head pieces ====================
SAVE (step A): save it as a PNG to {sa}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)
CANVAS: landscape 1536x1024, pure white. Four pieces in one row, left to right:
 A1. HEAD: the head with its horns, exactly as in image 1, but WITHOUT {f['crest']}. Where the crest was attached, draw the plain head surface (closed outline). The neck end at the bottom is a rounded stub that would tuck into the torso.
 A2. HEAD, EYES CLOSED: an exact copy of A1, same size and outline; the only change is that both eyes are closed (fierce closed-eye lines under the same heavy brows). Used for blinking.
 A3. HEAD, ROARING: an exact copy of A1, same size and outline of the skull and horns; the jaw is opened wide in a battle roar showing the fangs (inside of the mouth dark red, tongue darker pink), eyes wide and furious.
 A4. CREST: {f['crest']}, alone; its root end (joint, toward the head) extended as a rounded stub.

==================== STEP B: limb pieces ====================
SAVE (step B): save it as a PNG to {sb}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)
CANVAS: landscape 1536x1024, pure white. Eight pieces in two rows:
Row 1 (top), left to right:
 B1. ARM, viewer's LEFT: the whole arm from the shoulder to the wrist in ONE piece (upper arm + forearm, with the same slight elbow bend and the same armour as in image 1); the shoulder end and the wrist end are rounded joints.
 B2. FIST, viewer's LEFT: the clenched fist with its claws; its wrist end a rounded joint.
 B3. ARM, viewer's RIGHT: the whole arm from the shoulder to the wrist in ONE piece, same rules as B1, without the shoulder armour (that is a separate piece).
 B4. HAND, viewer's RIGHT: the hand that holds the weapon, drawn closed around an EMPTY grip (no weapon in this piece), so the fingers wrap a gap where the weapon's grip will go.
Row 2 (bottom), left to right:
 B5. LEG, viewer's LEFT: the whole leg from the hip to the ankle in ONE piece (thigh + shin, same slight knee bend and armour as image 1); hip end and ankle end rounded joints.
 B6. FOOT, viewer's LEFT: the clawed foot with a flat sole; its ankle end a rounded joint.
 B7. LEG, viewer's RIGHT: same rules as B5.
 B8. FOOT, viewer's RIGHT: same rules as B6.

==================== STEP C: body pieces ====================
SAVE (step C): save it as a PNG to {sc}
(if the name exists, add _2, _3 ... ; do not edit, move or delete any other file)
CANVAS: landscape 1536x1024, pure white. {n_c} pieces in two rows:
{c_rows}
 C1. TORSO: the body with its armour and belt, from the neck to the hips, WITHOUT the head, the arms, the legs, the tail, the shoulder armour, the hanging cloth{', the cape' if cape else ''}. Complete it where those covered it: the neck end is a rounded stub that tucks under the head, the shoulders are rounded, the bottom includes the hips, rounded.
 C2. TAIL: the whole tail with its fin(s); its root end (joint, toward the hips) extended as a rounded stub.{cape_piece}
 {w_i}. WEAPON: the whole {f['weapon']}, including the part of the grip hidden by the hand in image 1; same angle as in image 1.
 {s_i}. SHOULDER ARMOUR: {f['shoulder']}, alone.
 {c_i}. CLOTH: {f['cloth']}, alone, as it hangs in image 1; its top edge (joint, at the belt) straight.

Check before saving each step: the right number of pieces (4 in A, 8 in B, {n_c} in C), none touching, every piece complete with a closed outline, flat colours, white background.
"""
    p = W(out_dir, "luot_2_tach_manh.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


def huong_dan(done):
    lines = ["# Thủy Long: dòng Giọt Sương vẽ lại cả 3 dạng (rig xương riêng .atomik)", "",
             "Long chiến binh đứng hai chân, chiến, không cute (người dùng chọn 2026-11-08). Claude gọi Codex bằng "
             "`ArtGen/Spine/gen.py` (khoá chung với các lô tướng); người dùng không phải gửi tay.", ""]
    for k, f in FORMS.items():
        code, out_dir, save_dir, full = paths(k)
        lines += [f"## Dạng {k}: {f['name']}", f"- Thiết kế: {f['vn']}.",
                  f"- Lượt 1 (concept dáng dễ rig): `{W(out_dir, 'luot_1_tong.txt')}`, lưu `{W(save_dir, 'L1_full.png')}`; "
                  f"bản duyệt chép về `{full}`."]
        lines.append(f"- Lượt 2 (3 tờ mảnh: đầu 4 mảnh, tay chân 8 mảnh, thân {'6' if f['cape'] else '5'} mảnh): "
                     + (f"`{W(out_dir, 'luot_2_tach_manh.txt')}`" if k in done else "chưa dựng (chờ duyệt lượt 1)") + ".")
        lines.append("")
    lines += ["## Kiểm", "- Concept: chiến, không cute (đầu khoảng 1/4 chiều cao), tô phẳng không bóng, tay tách thân, chân không chéo, "
              "vũ khí, đuôi, áo choàng không che tay chân trước.",
              "- Mảnh: đủ số mảnh, không chạm nhau, tay và chân liền cả chi, chỗ khớp có đầu tròn thừa ra.", "",
              "## Câu sửa nhanh", "- \"Less cute: smaller head (a quarter of the height), longer limbs, narrower angry eyes.\"",
              "- \"Flat colour only: no shine spots, no shading, no shadow under the feet.\"",
              "- \"Arms must not touch the body; the weapon must not cross the legs.\""]
    p = W(HERE, "gui_gpt", "thuy_long_1", "HUONG_DAN.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return p


def main():
    for f in (STYLE_ANCHOR, WORLD_STYLE, STYLE_SHEET, PARTS_EXAMPLE):
        if not os.path.isfile(f):
            sys.exit("thiếu ảnh mẫu: " + f)
    done = []
    for k in FORMS:
        if k > 1 and not os.path.isfile(paths(k - 1)[3]):
            break
        print(luot_1(k)[0])
        if os.path.isfile(paths(k)[3]):
            print(luot_2(k))
            done.append(k)
    print(huong_dan(done))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
