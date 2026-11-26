# Sinh file prompt concept máy quả (lều Hội Máy Quả, đảo Casino). Chạy: py -3 -I build_concept.py
# Ra: concept/luot_1_huong_A.txt, _B.txt, _C.txt (mỗi hướng một tờ 3:2: hình chính + 3 dáng động).
# Đường dẫn ảnh mẫu tính từ chỗ đặt script (hai máy khác ổ đĩa).
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(os.path.dirname(HERE))  # .../ArtGen
OUT = os.path.join(HERE, "concept")
os.makedirs(OUT, exist_ok=True)

REF_DEALER = os.path.join(ART, "Casino", "dealer", "huong_A_dealer_co_dien.png")
REF_TENT = os.path.join(ART, "Casino", "dealer", "d4", "nen_leu_xoay_1k.png")
REF_WORLD = os.path.join(ART, "Islands", "refs", "world_style.png")

HEAD = """REFERENCE IMAGES (open them in this order)
image 1 = {dealer}: the dealer character of the same carnival island (a black ink fellow with yellow eyes). It fixes the DRAWING TECHNIQUE and the cartoon family: flat colour areas filled with visible coloured-pencil / wax-crayon diagonal hatching, dark brown slightly wobbly ink outlines, cream paper, no lighting at all. The new machine must look like it lives in the same cartoon as him. Do not draw him.
image 2 = {tent}: a tent interior of the same island. Same technique; shows the props family and palette of the island (striped canvas, gold fringe, paper lanterns, chips, barrels, chests).
image 3 = {world}: the world map of the same game. Third reference for the hand-drawn pen-and-crayon look on paper.

SAVE
Save the finished picture as {save} (if that name exists, add _2, _3 ...). Do not edit, move or delete any other file.

CANVAS
One landscape sheet, aspect ratio 3:2, plain warm cream paper background (flat, empty, no frame, no vignette).

WHAT IT IS
A character-design sheet for an ORIGINAL LIVING SLOT MACHINE (a three-reel fruit machine) that stands in a travelling carnival tent of a pet-collecting game. It is drawn in the spirit of early-1930s rubber-hose cartoons, where objects are alive: chunky, soft, bouncy, a body that can squash and stretch like rubber. It is a brand-new design: do not copy any existing cartoon character or any real machine brand.
"""

BODY_COMMON = """
PARTS EVERY VERSION HAS
- REEL WINDOW: one large flat upright rectangle in the middle of the body, about 55 % of the body width, with a thick brass frame. Behind it three vertical cream reel strips side by side separated by two thin brass bars; each strip shows three symbols stacked, so 9 symbols in a 3 x 3 grid. The symbols are simple chunky icons, one per cell: a red flame gem, a blue water-drop gem, a green leaf gem, a grey metal-ingot gem, a brown rock gem, a glass marble, a gold star, a small treasure chest, a crown badge.
- LEVER: on the viewer's right side of the body, a pull lever with a fat red ball knob on a slightly curved springy shaft, pointing up.
- PAYOUT TRAY at the bottom front, holding a few glass marbles (flat colours).
- The machine is seen STRAIGHT FROM THE FRONT, upright, no perspective, no three-quarter turn: the reel window is a true rectangle.

LAYOUT OF THE SHEET
- Left 60 % of the sheet: ONE BIG main drawing of the machine, whole body, standing upright in its neutral idle pose, front view.
- Right 40 % of the sheet: three small action sketches of the same machine stacked top to bottom, each clearly a different silhouette:
  1. SQUASH: pressed down short and wide, bulging at the sides, as if crouching before a hop; the top ornament and the lever knob lag upward.
  2. LEAN: the whole body bent in one smooth banana curve to the viewer's left, the lever and the top ornament whipping the other way, the reel symbols drawn as vertical speed streaks (reels spinning).
  3. JACKPOT: jumping in the air, stretched tall and thin, base lifted off the ground, lever flung up, marbles and little stars bursting out of the tray and the top, short crayon tick marks around it for the rattle.
- No labels, no arrows, no captions.

RULES (strict)
- Flat colours only: every area one even colour with crayon hatching as texture. NO lighting: no shadows, no cast shadow or ground shadow under the machine, no glow or halo around bulbs, no gradients, no white shiny highlights on metal or glass (brass is flat ochre-gold, glass is flat pale blue).
- Dark brown ink outlines, slightly wobbly, same weight as image 1.
- NO text, letters, numbers or digits anywhere: no words on the marquee, no "7", no price tags. Marquee decoration is shapes only (stars, dots, diamonds).
- Simple and bold: big readable shapes, few details, nothing fiddly. Cute and cheeky, never scary.
- Do not draw any background scene, user interface, frame or logo.
"""

DIRS = {
    "A": ("huong_A_chuong_vang.png", """
THIS VERSION: "THE GOLDEN BELL" (an object with NO face)
- No eyes, no mouth, no arms, no legs. It is alive only through the way its body bounces, bends and wobbles.
- Shape: a classic upright one-armed-bandit cabinet turned soft and chubby: a pear / bottle silhouette, round belly at the reel window, a narrower neck, a flared base that sits on four small ball feet.
- Colours: wine-red body, cream panels, ochre-gold trim (the same wine red and gold as the dealer's waistcoat in image 1).
- Top: an arched marquee crown with a row of round bulbs (flat yellow), and on the very top ONE BIG GOLD BELL sitting on a short coil spring (it wobbles and rings).
- A small scalloped red-and-cream striped awning with a fringe of gold tassels hangs over the reel window (the tassels swing).
- Two short brass whistle pipes stick out of the shoulders.
- Payout tray: a wide brass scoop.
"""),
    "B": ("huong_B_hau_an.png", """
THIS VERSION: "THE GREEDY ONE" (a machine with a FACE and two legs)
- Shape: a round-shouldered chubby cabinet like a fat little fellow: a dome head-marquee on top, a belly with the reel window, and two short rubber-hose legs (plain curved tubes, no knees) ending in fat round brown shoes with cream cuffs.
- Colours: turquoise-teal body, cream panels, tomato-red and ochre-gold trim.
- FACE: in the dome on top, two BIG oval cartoon eyes of the 1930s kind (white ovals, black pupils with a small wedge cut out), with the dome rim acting as cheeky eyebrows. The PAYOUT TRAY is its mouth: a wide grinning lower jaw with a row of chunky square cream teeth, one tooth gold; the marbles lie in the mouth like sweets.
- On top of the dome a small gold star on a coil-spring antenna (it wobbles).
- A row of round bulbs (flat yellow) around the dome like a hat band.
- No arms: the lever on the viewer's right is its only "arm".
- Expression: cocky, greedy, pleased with itself; in the JACKPOT sketch its eyes pop wide and the mouth-tray drops open spilling marbles.
"""),
    "C": ("huong_C_hu_bi.png", """
THIS VERSION: "THE MARBLE JAR" (an object with NO face, on three spring legs)
- No eyes, no mouth, no arms.
- Shape: squat and round like a pot-belly stove or a fat barrel, wider than tall in the body, with gold hoops around it. It stands on three short coil-spring legs with round brass feet (the springs compress and stretch).
- Colours: emerald-green body, cream panels, ochre-gold hoops and trim, a few plum-purple accents.
- Top: a BIG round glass globe jar, about half as wide as the body, filled with many coloured glass marbles (this is the jackpot jar), closed by a gold lid with a tiny pennant flag on top. The marbles rattle inside.
- On the viewer's left shoulder: a brass gramophone horn, opening pointing up and outward (prizes shoot out of it).
- Payout tray: a small half-round brass dish under the reel window.
- In the JACKPOT sketch the jar lid pops off and marbles fountain out of the jar and the horn.
"""),
}


def main():
    for k, (png, part) in DIRS.items():
        save = os.path.join(OUT, png)
        txt = HEAD.format(dealer=REF_DEALER, tent=REF_TENT, world=REF_WORLD, save=save) + part + BODY_COMMON
        p = os.path.join(OUT, "luot_1_huong_%s.txt" % k)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        print(p, len(txt))


if __name__ == "__main__":
    main()
