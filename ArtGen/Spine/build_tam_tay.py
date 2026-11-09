# -*- coding: utf-8 -*-
"""Gói prompt Codex cho Tám Tay vẽ lại (tướng .atomik thứ hai sau Thủy Long, 2026-11-08). Người dùng dặn: tự thiết kế, không bám
aola, chiến, không cute; gen hình trọn con LIỀN một ảnh (không tờ mảnh), rig thẳng từ ảnh đó (thuy_long_lien.py).

Mỗi dạng k (1, 2): luot_1_lien.txt, concept trọn con ở dáng rig được từ một ảnh: tay chân tách thân, vũ khí không vắt qua
người. Dạng 2 đính concept dạng 1 (cùng một con lớn lên). Lưu inbox/tam_tay_<k>/tai_ve/L1_lien.png.

    py -3 -I ArtGen/Spine/build_tam_tay.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, ART, line  # noqa: E402

STYLE_ANCHOR = W(ART, "Heroes", "refs", "style_anchor.png")
THUY_LONG = W(HERE, "inbox", "thuy_long_1", "L1_duyet.png")

COMMON = ("an OCTOPUS WARRIOR, a water-element gunner: a battle-hardened octopus soldier that stands upright on two thick "
          "tentacles like legs. Fierce and tough, NOT cute, NOT chibi, NOT a mascot: a strong bulbous mantle (head) with a "
          "heavy frowning brow ridge, narrow angry amber eyes (#F0A830) with black horizontal-bar pupils, a scar across the "
          "mantle; muscular tentacles. Colours: sandy-gold skin (#E0B04E) with cobalt-blue ring markings (#2F5FB0) along the "
          "tentacles and spots on the mantle, a pale cream underside of the tentacles with suckers (#F3E3BE), dark-cobalt "
          "outline accents. Only SIX tentacles are visible: two legs, two arms, and two short tentacles curling behind; the "
          "rest are tucked away out of sight.")

FORMS = {
    1: {
        "name": "Tám Tay Bong Bóng",
        "vn": "lính bạch tuộc trẻ: mũ nồi đỏ có huy hiệu vỏ sò, dây đeo chéo gắn ba quả bom bong bóng thủy tinh, súng hoả mai vỏ "
              "ốc anh vũ ngắn bắn bong bóng",
        "who": ("FORM 1, a young octopus soldier: lean and wiry. A worn red beret (#C0392B) with a small bronze shell badge, "
                "tilted on the mantle. A brown leather bandolier across the body holding three glass bubble-grenades (pale "
                "aqua #BDEBF0 with a white glint line). WEAPON: a short blunderbuss made from a nautilus shell (cream and "
                "rust-orange stripes #E8D2A6 / #C8693A) with a bronze barrel ring and a flared bronze muzzle."),
        "weapon_pose": ("The arm-tentacle on the viewer's RIGHT holds the nautilus blunderbuss at hip height, the tentacle tip "
                        "wrapped around its grip; the muzzle points forward to the viewer's right and slightly up. The whole "
                        "gun is clear of the body, the legs, the head and the canvas edges, with white space between gun and "
                        "body."),
    },
    2: {
        "name": "Tám Tay Pháo Thủ",
        "vn": "pháo thủ bạch tuộc: to khoẻ, mũ trụ đồng kiểu thợ lặn (lộ mặt, có ống thở cong), giáp vai đồng tán đinh, đai đạn "
              "bong bóng, khẩu pháo vỏ ốc anh vũ lớn có nòng đồng",
        "who": ("FORM 2, the same octopus grown into a heavy bubble-cannon gunner: bigger, broader and more muscular. An open-face "
                "bronze diving helmet (#B8762E with darker bronze #8A5420 rivets) on the mantle, a curved breathing pipe at its "
                "back, a round porthole rim framing the face (the face fully visible, no glass). A riveted bronze shoulder "
                "plate on the arm on the viewer's RIGHT, a wide leather belt with a row of glass bubble shells. WEAPON: a big "
                "hand-cannon made from a large nautilus shell (cream and rust-orange stripes) with a long bronze barrel and "
                "bronze bands, a pale aqua bubble glowing slightly in the muzzle."),
        "weapon_pose": ("The arm-tentacle on the viewer's RIGHT holds the shell cannon under the arm at hip height, braced "
                        "against the side, the barrel pointing forward to the viewer's right and slightly up. The whole cannon "
                        "is clear of the legs, the head and the canvas edges; it may touch the side of the body only where "
                        "it is held."),
    },
}

POSE = """POSE (very important: the picture will be animated as ONE single drawing with a bending 2D skeleton, so the limbs must be readable and must not overlap):
- Three-quarter view turned toward the viewer's RIGHT; the eyes look to the viewer's right with a fierce, ready-to-fight expression. A grounded battle-ready stance, not a big action pose.
- The two leg-tentacles stand wide apart, their curled tips planted flat on the same ground line, slightly bent like knees. Clear white space between the two legs.
- {weapon_pose}
- The arm-tentacle on the viewer's LEFT is held a little away from the body, slightly bent, its tip curled into a tight coil like a fist at hip height, with clear white space between the arm and the body.
- The two short back tentacles curl out behind the body on the viewer's LEFT, their tips clear of the legs and the arm.
- Nothing covers the face."""


def paths(k):
    code = f"tam_tay_{k}"
    out_dir = W(HERE, "gui_gpt", code)
    save_dir = W(HERE, "inbox", code, "tai_ve")
    return code, out_dir, save_dir, W(save_dir, "L1_lien.png")


def luot_1(k):
    f = FORMS[k]
    code, out_dir, save_dir, save = paths(k)
    refs = [(THUY_LONG, "an approved hero of the same game (a dragon warrior), 1024x1536, white background: match EXACTLY its "
                        "hand-drawn line, crayon texture, flat colouring, level of detail and fierce non-cute proportions. "
                        "Do NOT copy its species or design"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style (brown ink pen outline "
                          "+ coloured pencil / wax crayon hatching), nothing of its content"),
            (STYLE_ANCHOR, "an older hero of the same game, 1143x1376; only for the pen line weight and crayon texture. Do NOT "
                           "copy its cute proportions, its shine spots or its shading")]
    for j in range(1, k):
        refs.append((paths(j)[3], f"FORM {j} of this same octopus (approved), 1024x1536, white background: keep the same "
                                  f"species, face, colours and drawing style so the line clearly grows up; the new form is "
                                  f"bigger, tougher and better equipped"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw ONE hero as ONE full-body picture, in a clean animation-ready pose, in the drawing style of image 1 and image 2.

CHARACTER: {COMMON}
{f['who']}

CANVAS AND FRAMING: portrait 1024x1536, pure-white background, NO ground line, no cast shadow. The whole character and its weapon are visible, nothing cut by the edges. The warrior stands centred, about 1150 px tall from the top of the head (or hat) to the planted tentacle tips; the tips rest about 110 px above the bottom edge.

{POSE.format(weapon_pose=f['weapon_pose'])}

{line(7)}

Keep the design clean and readable: no text, no background, no extra props.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


def huong_dan():
    lines = ["# Tám Tay vẽ lại (tướng .atomik, rig từ một ảnh liền)", "",
             "Bạch tuộc chiến binh hệ Nước, pháo thủ bong bóng; tự thiết kế, chiến, không cute (người dùng dặn 2026-11-08). "
             "Claude gọi Codex bằng `ArtGen/Spine/gen.py`; người dùng không phải gửi tay.", ""]
    for k, f in FORMS.items():
        code, out_dir, save_dir, save = paths(k)
        lines += [f"## Dạng {k}: {f['name']}", f"- Thiết kế: {f['vn']}.", f"- File prompt: `{W(out_dir, 'luot_1_lien.txt')}`.",
                  f"- Ảnh mẫu: Thủy Long dạng 1 (nét, tô), bản đồ (nét), tướng cũ (độ dày nét)"
                  + (", concept dạng 1." if k > 1 else "."), f"- Lưu: `{save}`.", ""]
    lines += ["## Kiểm", "- Chiến, không cute; tô phẳng không bóng; tay chân tách thân, không chéo nhau; vũ khí không vắt qua người.",
              "", "## Câu sửa nhanh", "- \"Less cute: narrower angry eyes, heavier brow, smaller eyes, scar.\"",
              "- \"The gun must not cross the body or the legs.\"", "- \"Flat colour only: no shine spots, no shading.\""]
    p = W(HERE, "gui_gpt", "tam_tay_1", "HUONG_DAN.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return p


def main():
    for f in (STYLE_ANCHOR, WORLD_STYLE, THUY_LONG):
        if not os.path.isfile(f):
            sys.exit("thiếu ảnh mẫu: " + f)
    print(luot_1(1))
    if os.path.isfile(paths(1)[3]):
        print(luot_1(2))
    print(huong_dan())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
