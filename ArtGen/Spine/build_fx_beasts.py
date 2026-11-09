# -*- coding: utf-8 -*-
"""Tờ hiệu ứng riêng cho từng dòng thú đảo Thủy (beast.py), 2026-11-08. Người dùng dặn: animation đơn giản, hiệu ứng bù vào
là chính, càng gần boss cuối hiệu ứng càng đẹp; tham khảo cách làm của pixelfx (đà, khựng, hạt văng có biến thiên) nhưng hình là
ảnh vẽ tay tô phẳng theo luật game (không glow, không gradient).

Mỗi tờ: ảnh 1536x1024 chia lưới vô hình 3 cột x 2 hàng (ô 512x512), mỗi ô một hình hiệu ứng nằm trọn trong ô. Cắt theo ô
(--cat) ra inbox/fx/<id>_<tên>.png (nền trong, cắt sát).

    py -3 -I ArtGen/Spine/build_fx_beasts.py [id ...]          sinh file prompt gui_gpt/fx_<id>/luot_1_lien.txt
    py -3 -I ArtGen/Spine/build_fx_beasts.py --cat [id ...]    cắt tờ đã gen
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, ART, FLAT  # noqa: E402

REF = W(ART, "Heroes", "inbox", "giot_suong_fx", "tai_ve")
OUT = W(HERE, "inbox", "fx")

# id -> [(tên, mô tả tiếng Anh)] đúng 6 ô theo thứ tự: hàng trên trái -> phải, rồi hàng dưới
SHEETS = {
    "tieu_y": [
        ("claw", "three parallel curved water claw-slash streaks (a paw swipe made of water), slanting down to the right, foam edges, a few drops"),
        ("orb", "a round water bubble orb with a small spiral current inside and three tiny bubbles around it"),
        ("tornado", "a small upright water tornado (a narrow twisting water spout), wide at the top, thin at the bottom, foam rings and flying drops"),
        ("burst", "a round splash burst of water seen from the front: a ring of water petals with foam, drops flying outward"),
        ("foam", "a small cluster of white foam bubbles with a blue outline, like sea foam"),
        ("curl", "a single curling ocean wave crest with white foam, moving to the right"),
    ],
    "canh_cut": [
        ("smash", "an ice impact burst: a star-shaped burst of pale blue ice chunks and frost flakes radiating from the centre"),
        ("orb", "a round frosty ice orb with a snowflake pattern inside and small ice crystals orbiting it"),
        ("block", "a big cracked block of clear blue ice falling, with frost on its edges"),
        ("shards", "a spray of seven sharp pale-blue ice shards flying to the right in a fan"),
        ("flake", "one simple six-pointed snowflake"),
        ("fish", "a small frozen fish encased in a cube of ice, cartoon style"),
    ],
    "mi_nhi": [
        ("notes", "a cluster of three musical notes made of flowing water, with small drops, floating to the right"),
        ("sound", "three curved sound-wave arcs (crescents) of pale aqua water, opening to the right, getting bigger outward"),
        ("ribbon", "a long swirling ribbon of water forming a loose spiral, with foam tips"),
        ("pearl", "a round pearl orb with a soft pink rim inside a ring of tiny water drops"),
        ("feather", "a single lavender-blue feather with a turquoise tip"),
        ("note", "one small musical note made of water"),
    ],
    "ma_ket": [
        ("ram", "a curved double shock-wave of water shaped like two spiral ram horns hitting forward to the right, foam edges"),
        ("orb", "a round sea-foam orb, aqua water with white foam curls swirling around it"),
        ("tide", "a tall tidal wave rising up and curling forward to the right, its foam crest shaped like a ram's spiral horn"),
        ("burst", "a round splash burst of water with foam, drops flying outward"),
        ("bubble", "a small group of three round bubbles with blue outlines"),
        ("shell", "a small spiral seashell, cream and coral, silver rim"),
    ],
    "vay_lam": [
        ("bite", "a big biting jaw made of water: two curved rows of white shark teeth closing (upper and lower arcs) with splashing foam"),
        ("fin", "a shark fin cutting through a low wave, leaving a foam trail to the left, moving to the right"),
        ("geyser", "a tall upright water geyser with a pair of water shark jaws opening at its top"),
        ("burst", "a round splash burst of deep blue water with foam, drops flying outward"),
        ("drop", "one single blue water droplet"),
        ("tooth", "one white triangular shark tooth with a blue outline"),
    ],
    "kuba": [
        ("smash", "a crystal impact burst: aquamarine and white faceted crystal shards exploding outward from the centre"),
        ("orb", "a round aquamarine crystal orb with facets, small crystal chips orbiting it"),
        ("spikes", "a cluster of big pointed aquamarine crystals erupting upward from the ground, with rock chips flying"),
        ("shards", "a spray of seven small faceted crystal shards flying to the right in a fan"),
        ("gem", "one small faceted diamond gem, ice-white with aquamarine facets"),
        ("shield", "a round hexagon-pattern crystal shield, pale aqua, seen from the front"),
    ],
    "thuong_lam": [
        ("breath", "a cone of frost breath blowing to the right: icy wind streaks, snowflakes and ice crystals, wide at the right end"),
        ("orb", "a round ice orb with crystal spikes, a snowflake core"),
        ("icicles", "a burst of big icicles erupting upward from the ground in a ring, pale blue crystal ice"),
        ("nova", "a flat ring of frost and ice crystals spreading on the ground, seen in perspective (a wide ellipse)"),
        ("flake", "one ornate six-pointed snowflake"),
        ("shard", "one sharp ice shard crystal"),
    ],
    "huyen_vu": [
        ("slam", "a heavy shock-wave splash: a wide crescent of water bursting outward to both sides from a ground impact, rocks and foam"),
        ("orb", "a round jade-green orb with a golden hexagon rune pattern and swirling water around it"),
        ("serpent", "a huge water serpent (a sea snake made of water) rising up and striking forward to the right, mouth open, foam mane"),
        ("runes", "a flat golden rune circle with a hexagon turtle-shell pattern, seen in perspective on the ground (a wide ellipse), jade and gold"),
        ("spark", "one small four-pointed jade-green sparkle star"),
        ("wave", "a big dark-blue tidal wave with a white foam crest, curling forward to the right"),
    ],
    "lam_quan": [
        ("toll", "three concentric bronze-gold sound shock rings (a bell toll), seen in perspective as ellipses, with small music-note sparks"),
        ("orb", "a small bronze temple bell glowing with swirling water around it, coral-red tassel"),
        ("bell", "a huge ornate bronze temple bell with wave reliefs and a coral-red rope on top, seen from the side, falling down"),
        ("whirl", "a flat whirlpool of deep blue water spiralling, seen in perspective on the ground (a wide ellipse), foam spiral arms"),
        ("note", "one small golden music-note spark"),
        ("trident", "a big curling wave rising forward to the right with a golden trident shape inside its foam crest"),
    ],
    # tờ thứ hai cho dạng cuối của hai boss cuối đảo (ải 60, 70): hiệu ứng lớn, đẹp nhất
    "huyen_vu_b": [
        ("barrier", "a big half-dome shield made of jade hexagon tiles (a turtle-shell pattern) with a golden rim, seen from the front"),
        ("serpent", "a giant water serpent coiling up in a spiral and rising, mouth open, golden eyes, white foam mane"),
        ("pillar", "a pillar of black-jade stone with golden runes erupting from the ground, water splashing around its base"),
        ("tsunami", "a huge wide dark-blue tidal wave wall with a curling white foam crest, moving to the right"),
        ("orb", "a black-jade orb wrapped in a thin golden rune ring, small water swirls around it"),
        ("rain", "a cluster of falling water drops mixed with small jade-green sparkles"),
    ],
    "lam_quan_b": [
        ("shock", "a huge golden-bronze shockwave ring cracking the ground, seen in perspective as a wide ellipse, rock chips and water splashes flying"),
        ("toll", "a vertical fan of big bronze-gold sound-wave arcs expanding to the right, with three tiny bells among them"),
        ("spout", "a tall twisting whirlpool water column with a golden trident rising out of its top"),
        ("dragon", "a lion-dragon head made of water, roaring and charging to the right, foam mane flowing back"),
        ("feathers", "a swirling burst of black feathers with indigo tips"),
        ("halo", "a ring of small golden bells and golden sparkles, like a charm halo"),
    ],
    # đảo Mộc (2026-11-08 tối): lá, hoa, dây leo, gió, pha lê lục; sét vẽ vàng phẳng (không glow)
    "tien_la": [
        ("slash", "a crescent slash made of sharp green leaves flying to the right"),
        ("orb", "a round green seed orb with a small leaf swirl around it"),
        ("storm", "an upright whirl of green leaves spinning like a small tornado"),
        ("burst", "a round burst of green leaves flying outward from the centre"),
        ("leaf", "one single green leaf"),
        ("seed", "one small golden round seed pod with a short stem"),
    ],
    "hoa_nhuy": [
        ("petals", "a crescent stream of red and white flower petals flying to the right"),
        ("orb", "a round yellow pollen orb surrounded by red petals"),
        ("bloom", "a giant red-and-white flower bursting open upward from the ground, with leaves at its base"),
        ("burst", "a round burst of red petals and yellow pollen dots"),
        ("petal", "one single red flower petal"),
        ("pollen", "a small cluster of yellow pollen dots and tiny sparkles"),
    ],
    "de_hoa": [
        ("ram", "a curved shock-wave shaped like two wooden antler branches hitting forward to the right, with small yellow flowers"),
        ("orb", "a round wreath orb of yellow flowers and green leaves"),
        ("roots", "a burst of brown wooden roots and branches erupting upward from the ground, little leaves on them"),
        ("burst", "a round burst of yellow flowers and green leaves"),
        ("flower", "one small yellow five-petal flower"),
        ("chip", "one small brown wood chip"),
    ],
    "bom_la": [
        ("claw", "three parallel curved claw-slash streaks made of green leaves, slanting down to the right"),
        ("orb", "a round brown pinecone orb with green fern leaves around it"),
        ("vines", "a cluster of green vines whipping upward from the ground, curling at the tips, with leaves"),
        ("burst", "a round burst of green fern leaves"),
        ("cone", "one small brown pinecone"),
        ("fern", "one single green fern leaf"),
    ],
    "phong_linh": [
        ("gust", "a crescent gust of pale green wind streaks with small leaves, blowing to the right"),
        ("orb", "a spinning maple-seed propeller orb: two winged seeds circling a pale green wind ball"),
        ("whirl", "an upright whirlwind of pale green wind with leaves caught in it"),
        ("ring", "a flat ring of wind swirls seen in perspective on the ground (a wide ellipse)"),
        ("seed", "one maple seed with its single wing"),
        ("feather", "one single green owl feather"),
    ],
    "gio_loc": [
        ("blade", "a sharp crescent wind blade of pale teal air with white swirl lines, flying to the right"),
        ("orb", "a round teal wind orb with a white spiral symbol inside, small air swirls around it"),
        ("tornado", "a big upright teal tornado, wide at the top, with white swirl lines and leaves"),
        ("ring", "a flat ring of teal wind seen in perspective on the ground (a wide ellipse) with leaves"),
        ("swirl", "one small white-and-teal wind swirl"),
        ("wing", "one translucent-looking green dragonfly wing piece, flat pale green with dark green veins"),
    ],
    "long_vuot": [
        ("claw", "three parallel curved red claw-slash streaks with small green leaves, slanting down to the right"),
        ("orb", "a round amber orb with a leaf pattern inside and little leaves around it"),
        ("thorns", "a burst of thorny green vines and red thorns erupting upward from the ground"),
        ("burst", "a round burst of green leaves and small red thorns"),
        ("acorn", "one small orange-brown acorn"),
        ("talon", "one curved red claw tip"),
    ],
    "tho_hoang": [
        ("slash", "a long crescent slash made of jade-green bamboo leaves, flying to the right"),
        ("orb", "a round jade-green bamboo charm orb with a golden ring and small bamboo leaves around it"),
        ("spikes", "a ring of sharp jade bamboo stalks erupting upward from the ground"),
        ("burst", "a round burst of jade bamboo leaves and golden sparks"),
        ("leaf", "one single bamboo leaf"),
        ("wheel", "a round wooden shield-wheel with green carvings, seen from the front"),
    ],
    "moc_tinh": [
        ("claw", "three parallel curved claw-slash streaks made of bright green crystal, slanting down to the right"),
        ("orb", "a round faceted bright green crystal orb with small crystal chips orbiting it"),
        ("spikes", "a cluster of big pointed bright green crystals erupting upward from the ground with rock chips"),
        ("burst", "a round burst of bright green crystal shards"),
        ("gem", "one small faceted bright green gem"),
        ("leaf", "one leaf-shaped green crystal"),
    ],
    "thanh_long": [
        ("claw", "three parallel curved jade-green dragon claw streaks with small leaves, slanting down to the right"),
        ("orb", "a round jade pearl orb with a flat yellow zig-zag lightning ring around it"),
        ("dragon", "a long green dragon made of wind and leaves rising upward in an S-curve, mouth open"),
        ("strike", "a flat yellow lightning strike hitting the ground with a burst of green leaves at its base"),
        ("bolt", "one small flat yellow zig-zag lightning bolt"),
        ("cloud", "one small round grey-and-white cloud swirl"),
    ],
    "thanh_long_b": [
        ("storm", "a big storm cloud ring seen in perspective on the ground (a wide ellipse) with flat yellow lightning bolts"),
        ("roar", "a vertical fan of big jade-green wind arcs expanding to the right, with leaves"),
        ("pillar", "a tall twisting pillar of green wind and leaves with a flat yellow lightning bolt down its centre"),
        ("head", "a green dragon head made of wind and leaves, roaring and charging to the right, white whiskers flowing back"),
        ("leaves", "a swirling burst of green and golden leaves"),
        ("halo", "a ring of small jade pearls and flat yellow sparkles, like a halo"),
    ],
}


def paths(hid):
    out_dir = W(HERE, "gui_gpt", "fx_" + hid)
    save_dir = W(HERE, "inbox", "fx", hid, "tai_ve")
    return out_dir, save_dir, W(save_dir, "sheet.png")


def luot_1(hid):
    out_dir, save_dir, save = paths(hid)
    items = SHEETS[hid]
    refs = [(W(REF, "FX03.png"), "an approved effect of the same game (a water splash burst), 1024x1024: match EXACTLY its hand-drawn "
                                 "line, crayon texture and flat colouring"),
            (W(REF, "FX07.png"), "another approved effect of the same game (a wave), 1024x1024: same style reference"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style, nothing of its content")]
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    cells = ["top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right"]
    lst = "\n".join(f"{j + 1}. {cells[j]} cell: {d}." for j, (_n, d) in enumerate(items))
    boss = ""
    if hid.split("_b")[0] in ("kuba", "huyen_vu", "lam_quan", "thuong_lam", "gio_loc", "tho_hoang", "thanh_long") or hid.endswith("_b"):
        boss = ("\nThese effects belong to one of the island's last bosses: make them especially rich and beautiful (more "
                "layered shapes, elegant curls and details), still flat-coloured and readable.")
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as sheet_2.png, sheet_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw a SHEET OF SIX SEPARATE GAME EFFECT SPRITES in the hand-drawn style of images 1 and 2.

LAYOUT (very important, the sheet is cut automatically): landscape 1536x1024, pure-white background, divided into an invisible grid of 3 columns x 2 rows of 512x512 cells. Draw exactly ONE effect in each cell, centred, filling about 75% of the cell, every part (drops and sparks included) at least 40 px inside its cell: nothing crosses into a neighbouring cell. No grid lines, no numbers, no labels.
{lst}{boss}

STYLE: drawn by hand on paper with a dark-brown ink pen (#2B2118) outline about 6 px thick, slightly wobbly; coloured with coloured pencils and wax crayons, visible diagonal hatching. Colours exactly as described for each effect (water blue and aqua with white foam; ice pale blue and white; leaves and vines green; flowers as stated; crystals as stated; lightning flat yellow with a dark outline, never glowing).
{FLAT}
Plain pure-white background (#FFFFFF), no creature, no character, no text.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


def cat(hid):
    """cắt tờ theo ô 3x2: nền trắng nối mép thành trong suốt (giữ trắng bên trong như bọt), cắt sát, lưu inbox/fx/<id>_<tên>.png."""
    import numpy as np
    from PIL import Image
    sys.path.insert(0, HERE)
    import rig as riglib
    _o, save_dir, save = paths(hid)
    cands = sorted([f for f in os.listdir(save_dir) if f.lower().endswith(".png")],
                   key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
    if not cands:
        print("chưa có tờ:", hid)
        return
    im = Image.open(os.path.join(save_dir, cands[-1])).convert("RGB")
    im = im.resize((1536, 1024), Image.LANCZOS) if im.size != (1536, 1024) else im
    a = np.array(im)
    for j, (name, _d) in enumerate(SHEETS[hid]):
        cx, cy = (j % 3) * 512, (j // 3) * 512
        cell = a[cy + 6:cy + 506, cx + 6:cx + 506]
        m = riglib.fg_mask(cell)
        if not m.any():
            print("  ô trống:", name)
            continue
        rgba = riglib.to_rgba(cell, m)
        ys, xs = np.nonzero(m)
        out = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, f"{hid}_{name}.png")
        out.save(p, optimize=True)
        print(" ", p, out.size)


def main(argv):
    if argv and argv[0] == "--cat":
        for hid in argv[1:] or list(SHEETS):
            cat(hid)
        return
    for hid in argv or list(SHEETS):
        print(luot_1(hid))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
