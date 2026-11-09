# -*- coding: utf-8 -*-
"""Thanh Long dạng 2, 3 vẽ lại cho "chiến" (người dùng dặn 2026-11-09): chibi chỉ ở dạng 1; dạng sau tỉ lệ rồng trưởng thành
(đầu nhỏ so với thân, mắt xếch đồng tử dọc, nanh, móng giương), thân rắn dài uốn chữ S để rig chuỗi xương sống.
KHÔNG vẽ mây: mây cắt riêng từ concept cũ, game cho bay vòng quanh rồng (beasts_cfg "orbit").

Mỗi dạng: gui_gpt/thanh_long_<k>/luot_1_chien.txt -> inbox/thanh_long_<k>/tai_ve/L1_chien.png (1536x1024).

    py -3 -I ArtGen/Spine/build_thanh_long_chien.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/thanh_long_2/luot_1_chien.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, line  # noqa: E402

INBOX = W(HERE, "inbox")

# giữ nhận diện của dòng (màu, bờm, sừng, mào ngọc) nhưng đổi tỉ lệ và thần thái
WHO = {
    2: ("a young-adult EASTERN (Chinese) AZURE DRAGON, a fierce battle beast, no longer a baby: a long serpentine body "
        "(about four times longer than it is tall) with four strong short legs; a SMALL head compared with the body (the head "
        "is only about a quarter of the figure's height); a longer snout; narrowed, slanted golden eyes with thin dark "
        "slit pupils under heavy angry brows; the mouth open in a snarl showing sharp white fangs; turquoise-teal scales "
        "(same colour as image 3), a pale-yellow segmented belly running from the chin to the tail; a cream (#F4EEDC) "
        "mane swept back like wind-blown flames; two sharp orange antlers, each with two tines; the same small jade-green "
        "shell crest on the brow as image 3; two long cream whiskers streaming back from the snout; a row of small "
        "pointed teal fins along the spine; each foot has four sharp orange-tipped claws spread wide; a cream flame-like "
        "tuft at the tail tip"),
    3: ("a full-grown EASTERN (Chinese) STORM DRAGON, the island's final boss, powerful and fearsome but not horrific: "
        "an even longer, more muscular serpentine body (about four and a half times longer than it is tall) with four "
        "strong legs; a SMALL head compared with the body (about a quarter of the figure's height); a long snout with a "
        "strong jaw; narrowed, slanted yellow eyes with thin dark slit pupils under heavy angry brows; the mouth open in a "
        "battle roar showing sharp white fangs; deep turquoise-teal scales (same colour as image 3), a pale-yellow "
        "segmented belly; a big cream (#F4EEDC) mane swept back like wind-blown flames; two large orange antlers with three "
        "sharp tines each; the jade-green shell crest of image 3, a little larger, on the brow; two long cream whiskers "
        "streaming back; a row of big golden-yellow blade-shaped fins along the whole spine (as in image 3); each foot has "
        "four big sharp orange-tipped claws spread wide; a cream flame-like tuft at the tail tip; two or three small flat "
        "yellow zig-zag lightning marks painted ON its body (near the elbows and the tail), drawn flat with the ink outline, "
        "nothing floating around it"),
}

POSE = ("POSE (very important: it will be animated with a chain of bones along the spine, so body parts must be readable and "
        "must not overlap):\n"
        "- Side three-quarter view facing the viewer's RIGHT; the head is at the right, raised a little and thrust forward, "
        "glaring to the viewer's right, ready to strike.\n"
        "- It FLOATS in the air (no ground drawn): its long body makes ONE smooth horizontal S-shaped wave from the head at "
        "the right to the tail at the left: neck curving down to the chest, the middle of the body arching UP, the hips "
        "dipping down, then the tail sweeping up and curling down at the far left. No knots, no loops through itself, the "
        "body never crosses itself, the tail does not cross the body.\n"
        "- The four legs hang below the body, clearly separated from it and from each other, with white space between them; "
        "the front leg nearer to the viewer reaches forward with its claws spread, the others bent, claws spread.\n"
        "- The mane and the whiskers stream back over the neck and shoulders only; they do not cover the face, the legs or "
        "the middle of the body. The antlers do not cross each other.\n"
        "- NO clouds, no wind swirls, no lightning or anything else around the dragon: only the dragon itself.")


def luot_1(k):
    c = f"thanh_long_{k}"
    out_dir, save_dir = W(HERE, "gui_gpt", c), W(INBOX, c, "tai_ve")
    save = W(save_dir, "L1_chien.png")
    cur = W(INBOX, c, "L1_duyet.png")
    if not os.path.isfile(cur):
        cur = W(INBOX, c, "tai_ve", "L1_lien.png")
    refs = [
        (W(INBOX, "thanh_long_1", "L1_duyet.png"), "FORM 1 of this same dragon line (the cute baby form, 1536x1024): keep its "
         "drawing style, line weight and flat crayon colouring exactly; its colours carry over, but its baby proportions "
         "(huge head, big round eyes, smile) must NOT be copied"),
        (W(INBOX, "giap_long_2", "tai_ve", "L1_lien.png"), "another hero of the same game (a fierce armoured fire lizard), "
         "1536x1024: copy ONLY its attitude and adult proportions (small head, slanted angry eyes, fangs, sharp claws, "
         "ready-to-fight body language) and its hand-drawn line; do NOT copy its species, colours or armour"),
        (cur, f"the CURRENT form {k} of this dragon, 1536x1024: keep its colours and identity details (mane, antlers, crest, "
              f"belly{', golden spine fins, lightning marks' if k == 3 else ''}); it looks too cute and chibi, which is exactly what "
              f"must change; ignore its clouds"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style, nothing of its content"),
    ]
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_chien_2.png, L1_chien_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw form {k} of this dragon line again as ONE full-body picture, redesigned to look battle-ready and fierce. The user said: "the evolved forms are not fierce enough, only form 1 is chibi". Keep the identity of images 1 and 3 (colours, mane, antlers, crest), but NOT the chibi proportions.

WHO: {WHO[k]}.
Still a creature of a cute-but-tough monster-collecting game: clean, appealing shapes, a confident warrior look; not a realistic or horror dragon, no blood, no gore.

CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole dragon is visible, nothing cut by the edges, at least 60 px of white margin all round. About 1300 px from the tail tip to the snout, about 640 px from the top of the mane or antlers to the lowest claw; the lowest claw is about 150 px above the bottom edge.

{POSE}

{line(7).replace("of the style image, NOT the glossy look of the design image", "of images 1 and 2")}

Keep the design clean: no text, no background, no extra props, no effects around the dragon.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_chien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


# Lượt 2 dạng 3 (người dùng 2026-11-09: "dạng 2 và 3 chưa khác nhau lắm"): đổi cả màu, giáp, đồ và DÁNG (chồm dựng thay vì nằm
# ngang) để nhìn bóng dáng đã biết là con khác, mạnh hơn hẳn; dáng dựng còn hẹp hơn nên vừa sân.
WHO3B = ("the FINAL evolution of this dragon line, a full-grown EASTERN THUNDER DRAGON KING, the island's final boss: it must look "
         "clearly DIFFERENT from and much more powerful than form 2 (image 2) at a glance: bigger, heavier, a thick muscular "
         "serpentine body; DEEP AZURE-BLUE scales (much darker and bluer than the turquoise of form 2, about #1C7FB0) with the "
         "pale-yellow segmented belly; GOLDEN ARMOUR: a golden forehead plate framing the jade-green shell crest, golden plates on the "
         "shoulders, elbows and along the top of the tail; a row of big golden-yellow blade fins along the whole spine; a HUGE mane "
         "that is white at the root and pale lemon-yellow at the tips, swept back and up like a storm; two VERY LARGE golden antlers "
         "with four sharp tines each; long whiskers shaped like zig-zag lightning bolts (pale yellow, flat colour, ink outline); "
         "narrowed yellow eyes with thin dark slit pupils under heavy angry brows; the mouth wide open in a thunderous roar showing "
         "sharp white fangs; big claws with golden tips; the near front claw holds out a round pale-yellow THUNDER PEARL with a small "
         "zig-zag mark on it; the tail ends in a golden lightning-bolt-shaped blade instead of a fur tuft; a few flat yellow zig-zag "
         "lightning marks painted on its body")

POSE3B = ("POSE (very important: it will be animated with a chain of bones along the spine, so body parts must be readable and "
          "must not overlap):\n"
          "- Side three-quarter view facing the viewer's RIGHT.\n"
          "- It REARS UP in the air (no ground drawn), a different silhouette from form 2: the front half of its body rises in a "
          "tall S-curve so the head is HIGH at the upper right, chest thrust forward, roaring down toward the right; the back half "
          "of the body sweeps down and lies in one loose curve along the bottom toward the left; the tail lifts at the far left with "
          "its lightning blade. No knots, no loops through itself, the body never crosses itself, the tail does not cross the body.\n"
          "- The four legs are clearly separated from the body and from each other, with white space between them: the near front "
          "leg is raised forward holding the thunder pearl out to the right (the pearl clear of the face), the far front leg is "
          "raised with claws spread, the hind legs are bent below the lower body, claws spread.\n"
          "- The mane and the whiskers stream back and up behind the head; they do not cover the face, the legs or the middle of "
          "the body. The antlers do not cross each other.\n"
          "- NO clouds, no wind swirls, no loose lightning or anything else floating around the dragon: only the dragon itself.")


def luot_1_b3():
    c = "thanh_long_3"
    out_dir, save_dir = W(HERE, "gui_gpt", c), W(INBOX, c, "tai_ve")
    save = W(save_dir, "L1_chien_b.png")
    refs = [
        (W(INBOX, "thanh_long_1", "L1_duyet.png"), "FORM 1 of this same dragon line (the cute baby form, 1536x1024): keep its "
         "drawing style, line weight and flat crayon colouring exactly; NOT its baby proportions"),
        (W(INBOX, "thanh_long_2", "tai_ve", "L1_chien.png"), "FORM 2 of this same line (1536x1024): the final form must look clearly "
         "different and stronger than this one: different colours (deeper blue), golden armour, bigger antlers and mane, a rearing "
         "pose instead of this horizontal one; keep only its adult proportions, its fierce face and its drawing style"),
        (W(INBOX, "giap_long_2", "tai_ve", "L1_lien.png"), "another hero of the same game (a fierce armoured fire lizard), "
         "1536x1024: copy ONLY its attitude and how it draws golden armour plates on a beast, and its hand-drawn line; do NOT copy "
         "its species or colours"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style, nothing of its content"),
    ]
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_chien_b_2.png, L1_chien_b_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw the FINAL form (form 3) of this dragon line as ONE full-body picture. The user said: "forms 2 and 3 do not look different enough". The final form must be recognisable as the same azure dragon line (jade crest, cream-white mane, golden spine fins, pale-yellow belly) but different at first glance: new colours, golden armour, bigger antlers, a thunder pearl, and a rearing pose.

WHO: {WHO3B}.
Still a creature of a cute-but-tough monster-collecting game: clean, appealing shapes, a majestic warrior look; not a realistic or horror dragon, no blood, no gore.

CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole dragon is visible, nothing cut by the edges, at least 60 px of white margin all round. About 1150 px from the tail tip to the front claws, about 820 px from the antler tips to the lowest claw; the lowest point is about 90 px above the bottom edge.

{POSE3B}

{line(7).replace("of the style image, NOT the glossy look of the design image", "of images 1 and 2")}

Keep the design clean: no text, no background, no extra props, no effects around the dragon.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_chien_b.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


def main():
    if "b3" in sys.argv[1:]:
        print(luot_1_b3())
        return
    for k in (2, 3):
        print(luot_1(k))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
