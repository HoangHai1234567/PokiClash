# -*- coding: utf-8 -*-
"""Gói prompt Codex cho 10 dòng tướng đảo Mộc vẽ lại thành tướng .atomik (2026-11-08 tối).

Người dùng dặn: concept dựa trên tướng đã có (concept đã duyệt của từng dạng, ArtGen/Heroes/inbox/<id>_<k>/concept_duyet.png);
gen MỘT con hoàn chỉnh trước, rig xương, SAU ĐÓ mới gen thêm bộ phận phục vụ animation (build_parts.py: ảnh "lớp dưới" vẽ đủ
phần bị che, đúng chỗ, đúng cỡ). Animation đơn giản kiểu Clash of Critters như đảo Thủy (beast.py).

Mỗi dạng: gui_gpt/<id>_<k>/luot_1_lien.txt -> inbox/<id>_<k>/tai_ve/L1_lien.png (1536x1024).

    py -3 -I ArtGen/Spine/build_moc.py [id ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, ART, line  # noqa: E402
from build_beasts import POSES  # noqa: E402

OLD = W(ART, "Heroes", "inbox")
POSE_REF = {"quad": "lam_quan_1", "biped": "canh_cut_1", "bird": "mi_nhi_1", "blob": "tieu_y_1", "hover": "thuong_lam_1",
            "seagoat": "ma_ket_1", "crab": "kuba_1", "dragon": "thuong_lam_1", "turtle": "huyen_vu_1"}

POSES = dict(POSES)
POSES["blob"] = ("- Stands on its short legs (or its round bottom), feet flat on one level ground line (no ground drawn), a grounded "
                 "ready-to-fight stance.\n- Small arms, leaves, fins or ears are held a little away from the body with white space "
                 "between them and the body where possible.")
POSES["humanoid"] = ("- Stands upright on its two legs, both feet flat on one level ground line (no ground drawn), feet a little "
                     "apart with a white gap between the legs, a grounded ready-to-fight stance.\n- Both arms are held a little away "
                     "from the body with white space between each arm and the body; any held item is fully clear of the head and "
                     "body; wings (if any) spread behind, clear of the head.")
POSES["hover"] = ("- It FLOATS in the air a little above the ground (no ground drawn): about 90 px of white space between its lowest "
                  "point and the ground line, as if hovering, in a ready-to-fight stance.\n- Wings (if any) spread up and back, "
                  "clear of the head; the long tail curves behind and below on the viewer's LEFT, clear of the body where possible; "
                  "small limbs held away from the body. A small cloud or wind swirl under it is allowed only if it is part of the "
                  "design in image 1.")

# id -> ải, kiểu dáng mỗi dạng, ghi chú riêng
LINES = {
    "tien_la": {"order": 1, "kind": {1: "blob", 2: "humanoid", 3: "humanoid"},
                "note": {3: "Its leaf wings spread behind its back, clear of the head."}},
    "hoa_nhuy": {"order": 5, "kind": {1: "blob", 2: "blob", 3: "humanoid"}, "note": {}},
    "de_hoa": {"order": 10, "kind": {1: "quad", 2: "quad", 3: "quad"}, "note": {}},
    "bom_la": {"order": 15, "kind": {1: "quad", 2: "quad"}, "note": {}},
    "phong_linh": {"order": 20, "kind": {1: "bird", 2: "bird"},
                   "note": {1: "Its two leaf-propeller seeds stay held out to the sides like small wings.",
                            2: "Its ring of bamboo and wind ribbons stays behind its head, clear of the face."}},
    "gio_loc": {"order": 30, "kind": {1: "hover", 2: "hover", 3: "hover"}, "note": {}},
    "long_vuot": {"order": 40, "kind": {1: "quad", 2: "humanoid"},
                  "note": {1: "Crouched on four legs, wings half open behind.", 2: "Wings spread behind, clear of the head."}},
    "tho_hoang": {"order": 50, "kind": {1: "humanoid"},
                  "note": {1: "Keep its big wooden shield-wheel and bamboo charms, but place them clear of the body: the wheel "
                              "behind on the viewer's LEFT, the charms floating at the sides."}},
    "moc_tinh": {"order": 60, "kind": {1: "quad", 2: "quad"}, "note": {}},
    "thanh_long": {"order": 70, "kind": {1: "hover", 2: "hover", 3: "hover"},
                   "note": {1: "Its clouds are filled with a pale blue-grey crayon colour (#DDE9EE), never left as white paper; its "
                               "white whiskers and white mane are a pale cream crayon colour (#F4EEDC).",
                            2: "Its clouds are filled with a pale blue-grey crayon colour (#DDE9EE), never left as white paper; its "
                               "white whiskers and white mane are a pale cream crayon colour (#F4EEDC).",
                            3: "A long serpent dragon: its body makes ONE big S-curve above the cloud, head at the right, no knots "
                               "or loops through itself, the tail at the left. Its storm clouds are filled with grey and pale "
                               "blue-grey crayon colours, never left as white paper; its white mane, whiskers and tail tuft are "
                               "a pale cream crayon colour (#F4EEDC) with closed outlines, never white paper."}},
}


def code(hid, k):
    return f"{hid}_{k}"


def paths(hid, k):
    c = code(hid, k)
    return c, W(HERE, "gui_gpt", c), W(HERE, "inbox", c, "tai_ve"), W(HERE, "inbox", c, "tai_ve", "L1_lien.png")


def luot_1(hid, k):
    ln = LINES[hid]
    kind = ln["kind"][k]
    c, out_dir, save_dir, save = paths(hid, k)
    design = W(OLD, c, "concept_duyet.png")
    pose_ref = W(HERE, "inbox", POSE_REF[kind] if kind in POSE_REF else "canh_cut_1", "tai_ve", "L1_lien.png")
    refs = [(design, "the APPROVED DESIGN of this hero (form %d), white background: redraw EXACTLY this creature: same species, "
                     "body shape, proportions, face, colours, markings, leaves, flowers and accessories" % k),
            (pose_ref, "another hero of the same game redrawn the way we need, 1536x1024: copy ONLY its framing, pose logic "
                       "(three-quarter side view facing right, limbs separated) and its hand-drawn line and flat crayon colouring. "
                       "Do NOT copy its species or design"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style, nothing of its content")]
    if k > 1:
        prev = W(HERE, "inbox", code(hid, k - 1), "L1_duyet.png")  # ảnh Claude chọn (gen lại), không thì ảnh gen đầu
        if not os.path.isfile(prev):
            prev = W(HERE, "inbox", code(hid, k - 1), "tai_ve", "L1_lien.png")
        if os.path.isfile(prev):
            refs.append((prev, f"FORM {k - 1} of this same line already redrawn this way (1536x1024): keep the same drawing style, "
                               f"line weight and colour treatment"))
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    boss = ""
    if ln["order"] >= 30:
        boss = "\nThis line belongs to one of the island's bosses: keep every refined detail of the approved design, draw it beautifully."
    note = ln["note"].get(k, "")
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_lien_2.png, L1_lien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw the hero of image 1 as ONE full-body picture in a clean animation-ready pose (it will be animated as one drawing with a simple 2D skeleton). Same creature and design as image 1; a new pose; the hand-drawn style of images 2 and 3.{boss}

CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature is visible, nothing cut by the edges, at least 60 px of white margin all round. It is centred, about 720 px tall from the top of its head (ears, horns, leaves or crest included) to its lowest point; its lowest point is about 120 px above the bottom edge.

POSE (very important: body parts must be readable and must not overlap):
- Side three-quarter view turned toward the viewer's RIGHT; the head is at the right, the eyes look to the viewer's right with a determined, ready-to-fight expression (as in image 1).
{POSES[kind]}
- Nothing covers the face. Ears, horns, leaves and crest do not cross each other.{(chr(10) + '- ' + note) if note else ''}

{line(7).replace("of the style image, NOT the glossy look of the design image", "of images 1 and 2")}

Keep the design clean: no text, no background, no extra props, no effects around the creature.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


def huong_dan():
    lines = ["# Đảo Mộc: tướng .atomik vẽ lại theo concept đã duyệt (rig từ một ảnh liền, rồi gen bộ phận)", "",
             "Người dùng dặn 2026-11-08: concept dựa trên tướng đã có; gen một con hoàn chỉnh, rig xương, rồi mới gen thêm bộ phận "
             "phục vụ animation (build_parts.py). Claude gọi Codex bằng `ArtGen/Spine/gen.py`.", ""]
    for hid, ln in LINES.items():
        lines.append(f"## {hid} (ải {ln['order']})")
        for k in ln["kind"]:
            c, out_dir, save_dir, save = paths(hid, k)
            lines += [f"- Dạng {k}: file prompt `{W(out_dir, 'luot_1_lien.txt')}`; ảnh mẫu: concept đã duyệt `{W(OLD, c, 'concept_duyet.png')}`"
                      f" (thiết kế), một tướng đảo Thủy đã vẽ lại (dáng, nét), bản đồ (nét); lưu `{save}`."]
        lines.append("")
    lines += ["## Kiểm", "- Đúng thiết kế concept đã duyệt; nhìn nghiêng 3/4 sang phải; chân tay tách thân; tô phẳng không bóng.", "",
              "## Câu sửa nhanh", "- \"Keep the exact design of image 1, only change the pose.\"",
              "- \"Flat colour only: no shine spots, no shading, no glow.\""]
    p = W(HERE, "gui_gpt", "HUONG_DAN_moc.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return p


def main(ids):
    for hid in ids or list(LINES):
        for k in LINES[hid]["kind"]:
            if not os.path.isfile(W(OLD, code(hid, k), "concept_duyet.png")):
                print("thiếu concept đã duyệt:", code(hid, k))
                continue
            print(luot_1(hid, k))
    print(huong_dan())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
