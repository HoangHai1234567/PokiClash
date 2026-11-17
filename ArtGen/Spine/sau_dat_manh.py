# -*- coding: utf-8 -*-
"""Sâu đất khổng lồ (sau_dat, tướng 7 đảo Thổ, rig monster_3643): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" từ concept đã duyệt (tai_ve/L1_duyet.png = L1_A,
người dùng chọn 2026-11-17: sâu cát, đầu húc ba vòng giáp sa thạch, miệng tròn vòng răng, thân vòng đốt vàng cát).

Concept lệch tỉ lệ con gốc (IoU 0,675) nên làm hai bước như rong_cat_manh.py:
  1. BỐ CỤC (L2_bocuc): GPT vẽ lại con của mình ĐÚNG dáng, chỗ, cỡ từng part của con gốc (ảnh 1 = con gốc, ảnh 2 = concept).
  2. NHÓM MẢNH (M_N*): mỗi lượt vài khối không chồng nhau, đúng chỗ, đúng cỡ trên bố cục, vẽ đủ phần khuất; thân giun (P_bozi_01..10)
     gen LIỀN một khối rồi cắt theo vùng part của họ.
Gen qua Magnific (GPT 2.6, 1k high, 95 credit / ảnh; người dùng: dưới 100 credit / ảnh, quá thì hỏi).

    sau_dat_manh.py bocuc        file prompt bố cục → gui_gpt/sau_dat_1/luot_2_bocuc.txt
    sau_dat_manh.py so_bocuc     chồng bao từng part gốc lên bố cục, IoU hình bóng → mau/_so_bocuc.png
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sau_dat  # noqa: E402,F401  (đăng ký mã sau_dat trong tho5.CON)
import tho5  # noqa: E402
from quai.soi import _tris  # noqa: E402

G = tho5.dat("sau_dat")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
GOC = os.path.join(G.MAU, "goc_ca_con.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "sau_dat_1")
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def el(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, f"{ten}.png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


STYLE = (f"DRAWING STYLE (very important): exactly the hand-drawn style of image 2: a wobbly dark-brown INK outline ({MUC}, about 7 px) "
         "running all the way round every piece, thinner ink lines (about 4 px) for the few inner lines (ring grooves, plate edges, rock "
         "strata, teeth), every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. Image 1 is painted in a smooth "
         "digital cel style with soft shading: do NOT copy that painting style, its colours, its cell pattern, its blue crystals or its "
         "purple petals. No shading, no highlights, no gradients, no glow, no shadows: flat colour only.")

COLORS = ("COLOURS (from image 2): worm body rings sand-ochre #D3A866 with thin darker grooves #9C7444, belly side cream sand #EAD7AE; head "
          "armour rings and lower jaw sandstone #C99A57 with #9E7442 on the faces turned away; crest plates #D9B677 with a flat ochre band "
          "#BF8443; teeth and tusks cream #F1E6CB; inside of the mouth terracotta red #A2412E; eye amber #F6C443 with a black slit pupil; "
          "feelers dark brown #4E3726 with amber #EFA330 barbs; slabs in flat strata bands of cream #EAD7AE, ochre #C99A57 and rust "
          "#A85F3A; earth chunks dark brown #5A4030 (side faces #3F2D22) with one thin amber crack #EFA330; tendrils dusty rose #C98B78 "
          "with darker rings #A86E5E; sand mound #E2C48C, rocks #C99A57 / #9E7442, small amber crystals #EFA330.")

BOCUC = (
    "TASK: draw OUR character of image 2 (the approved design: a colossal SANDWORM bursting out of the ground: a sand-ochre ring-segmented "
    "worm body, a blunt armoured ram-like head with three sandstone armour rings and a wide round mouth full of rings of small cream teeth, "
    "a fierce narrow amber eye, broad fan-shaped sandstone crest plates, ten long dark-brown whip feelers with amber barbs, tall slabs of "
    "layered sandstone strata behind, dark earth chunks with amber cracks in front, dusty-rose earthworm-like tendrils, a sand mound with "
    "rocks and amber crystals) in EXACTLY the POSE, the LAYOUT and the SIZE of the creature in image 1: every piece at the same place, the "
    "same size, the same angle and with the same overlaps as the matching piece of image 1 (if the new picture were laid over image 1, "
    "each piece must sit on its old place). Image 1 is ONLY a pose and layout guide; the LOOK, colours and details come from image 2.",
    "PIECE BY PIECE (positions on the 1536x1024 canvas as in image 1; left/right as seen by the viewer):\n"
    "- RUBBLE at the bottom, where image 1 has its blue crystals: a low SAND MOUND with sandstone rocks and a few small flat amber crystals: "
    "the biggest cluster at the bottom left (x 416-721, y 752-911), a smaller cluster at the bottom middle (x 693-859, y 810-908), a low "
    "cluster at the bottom right (x 857-1030, y 844-905).\n"
    "- GROUND SHARDS: where image 1 has the two small dark claw-like roots lying flat on the ground (far bottom left x 439-811, bottom "
    "right x 827-1081, y 750-908), two LOW FLAT dark-brown rock shards lying on the ground, pointing outwards.\n"
    "- SLABS BEHIND: where image 1 has its five tall purple petals, FIVE tall upturned SLABS of layered sandstone strata (flat horizontal "
    "bands of cream, ochre and rust), jagged pointed tops, at the same places, sizes and lean as the petals: the biggest one at the middle "
    "left leaning right (x 612-896, y 293-829); a narrow one left of it (x 541-666, y 386-801); one at the far left leaning left (x 464-652, "
    "y 425-819); a big one at the centre right (x 766-1014, y 342-833); one at the lower right leaning far to the right, its tip pointing to "
    "the upper right (x 764-1104, y 508-869).\n"
    "- DARK EARTH CHUNKS: where image 1 has its four dark curved plates, four angular dark-brown EARTH CHUNKS, each with one thin amber "
    "crack: one BEHIND the body at the left (x 453-666, y 544-830); one in front at the lower left (x 578-751, y 591-858); one in front in "
    "the middle (x 663-953, y 668-880); one lying in front at the lower right (x 762-1058, y 760-898).\n"
    "- WORM BODY: the thick worm body rising in a gentle S-curve out of the middle of the rubble up to the head (x 666-943, y 439-879), made "
    "of sand-ochre RING SEGMENTS with thin darker grooves, the cream belly side facing the viewer; at the top it goes into the back of the "
    "head.\n"
    "- HEAD (upper right, x 841-1040, y 450-656), pointing RIGHT and slightly DOWN, ONE eye visible: the blunt armoured ram head of image 2 "
    "with its sandstone ARMOUR RINGS (the upper head piece), at its right end the WIDE ROUND MOUTH slightly open with rings of small cream "
    "teeth and a terracotta-red inside; a separate thick armoured LOWER JAW under it; where image 1 has the small dark spikes at the chin "
    "and under the snout, the TWO short cream TUSKS of the lower jaw pointing up and forward; where image 1 has its narrow eye slit, the "
    "fierce narrow amber EYE (black slit pupil, one small white dot) under a heavy stone brow ridge; where image 1 has the tall pointed horn "
    "above the eye, a SHORT blunt sandstone brow horn. The head may be up to about 15 % bigger than the head of image 1 but stays centred "
    "on the same place.\n"
    "- CREST: where image 1 has the four long backswept blades on top of the head (x 674-990, y 306-547), FOUR broad rounded FAN-SHAPED "
    "sandstone plates stacked like a collar, each with a flat ochre band along its edge, sweeping back and up toward the upper left, about "
    "the same places and lengths as the blades but ROUNDED fan shapes, not blades.\n"
    "- FEELERS: TEN long thin dark-brown whip FEELERS, each ending in a small amber diamond-shaped barb, exactly where image 1 has its ten "
    "dark tentacles (same roots at the back of the head, same curves, same lengths, same thickness), fanning up and to the right.\n"
    "- TENDRILS: where image 1 has its pale curved horn-like tendrils (eleven round the body and the rubble, three from the back of the head "
    "pointing left), dusty-rose RINGED earthworm-like tendrils at the same places, with the same curves, lengths and thickness.",
)


def p_bocuc():
    out, save = luu("L2_bocuc")
    R1 = (f"image 1 = {Wp(GOC)}: the REFERENCE creature (a pale serpent-dragon rising out of a cocoon of purple petals, dark tentacles on its "
          "head, blue crystals at the bottom, in a smooth digital cel style). Use it ONLY for the pose, the layout and the size of every "
          "piece; do NOT copy its look, its colours, its petals, its crystals or its painting style.")
    R2 = (f"image 2 = {Wp(CONCEPT)}: our APPROVED character design (hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours). "
          "Copy its look, materials, colours and drawing style exactly.")
    t = ["IMAGES (attached in this order; open each from its path):", R1, R2, ""] + save + ["", BOCUC[0], "", BOCUC[1], "", COLORS, "",
         STYLE, "", "MOOD: a colossal, ancient, menacing worm, fierce like a boss monster; stylised and clean, no gore, no slime. The head, "
         "the crest, the feelers and the tendrils joined to the body or the ground (no white gaps). No new pieces beyond the list.", "",
         "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow, the character at the same place "
         "and size as in image 1. No sparkles, no glow, no dust cloud, no labels, no frame."]
    p = os.path.join(GUI, "luot_2_bocuc.txt")
    ghi(p, t)
    print(p)


# ---------------------------------------------------------------- tiện ích hình
def nen(A):
    """mặt nạ nền: trắng nối mép tờ (lấp kín lỗ trong hình)."""
    m = ((255 - A.astype(np.int16)).max(2) > 28).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2))
    f = m.copy()
    msk = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(f, msk, (0, 0), 128)
    return f == 128


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(ten) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def doc(p):
    return np.asarray(Image.open(p).convert("RGB").resize((W, H)))


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    return s, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


_MN = {}


def mat_na_part():
    """mặt nạ (px khung concept) từng part gốc ở khung 0 idle (tô theo lưới của họ) + thứ tự vẽ."""
    if _MN:
        return _MN
    _, imgs, atts = G.nap("att_idle0.json")
    _, to_px = tf()
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), to_px(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        _MN[a["slot"]] = (np.asarray(lay.convert("RGBA"))[..., 3] > 60, a["order"])
    return _MN


def so_bocuc():
    src = moi_nhat("L2_bocuc")
    A = doc(src)
    g = ~nen(doc(GOC))
    m = ~nen(A)
    iou = (g & m).sum() / max(1, (g | m).sum())
    MN = mat_na_part()
    im = Image.fromarray(A.astype(np.uint8))
    d = ImageDraw.Draw(im)
    for k, (s, (mm, _)) in enumerate(sorted(MN.items(), key=lambda q: q[1][1])):
        cs, _ = cv2.findContours(mm.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = [(230, 40, 40), (40, 120, 230), (30, 160, 60), (200, 0, 200)][k % 4]
        for cc in cs:
            pts = [tuple(p) for p in cc.reshape(-1, 2)]
            if len(pts) > 2:
                d.line(pts + [pts[0]], fill=c, width=1)
    d.text((20, 20), f"IoU hinh bong voi con goc {iou:.3f}", fill=(230, 30, 30))
    p = os.path.join(G.MAU, "_so_bocuc.png")
    im.save(p)
    print(os.path.basename(src), f"IoU {iou:.3f}", p)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "bocuc":
        p_bocuc()
    elif a[0] == "so_bocuc":
        so_bocuc()
