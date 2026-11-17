# -*- coding: utf-8 -*-
"""Rồng giáp sa thạch (rong_cat, tướng 4 đảo Thổ, ải 15, rig monster_3424): MẢNH theo concept D đã duyệt (tai_ve/L1_duyet.png: da nâu bụi,
giáp sa thạch kem vạch son trên vai, cẳng tay gần và sống lưng, hai sừng đá dài vuốt ra sau, sừng mũi pha lê hổ phách, mắt vàng, vuốt nâu sẫm).

Concept "gần giống" lệch tỉ lệ con gốc (IoU 0,71) nên làm hai bước:
  1. BỐ CỤC (L2_bocuc): GPT vẽ lại con của mình (thiết kế concept D) ĐÚNG dáng, chỗ, cỡ từng mảnh của con gốc ở khung 0 idle (ảnh 1 = hình
     con gốc chỉ để lấy dáng; ảnh 2 = concept). Ảnh này là "concept trên rig": mọi mảnh sau cắt theo nó.
  2. NHÓM MẢNH (M_<nhóm>): mỗi lượt giữ vài mảnh KHÔNG chồng nhau của bố cục, đúng chỗ, đúng cỡ, vẽ đủ phần khuất (ảnh 2 = bố cục có viền đỏ
     quanh các mảnh cần giữ). Mặt liền màu (thân + đuôi + chân sau gần; chân sau xa; tay xa; tay gần) gen LIỀN một khối rồi cắt theo vùng part
     của họ (skill pokiclash-spine-rig mục 00, "gen liền rồi cắt").

    rong_cat_manh.py bocuc         file prompt bố cục → gui_gpt/rong_cat_1/luot_2_bocuc.txt
    rong_cat_manh.py so_bocuc      IoU + viền part gốc chồng lên bố cục → mau/_so_bocuc.png
    rong_cat_manh.py nhom          tờ viền + file prompt từng nhóm → mau/_vien_<nhóm>.png, gui_gpt/rong_cat_1/luot_2_<nhóm>.txt
    rong_cat_manh.py cat [nhóm]    cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<slot>.png + manh/dat.json (hộp px trên khung concept)
    rong_cat_manh.py ghep          ghép mọi mảnh theo thứ tự vẽ idle cạnh bố cục → manh/_ghep.png + IoU
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
from quai.soi import _tris  # noqa: E402

G = tho5.dat("rong_cat")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
GOC = os.path.join(G.MAU, "goc_ca_con.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "rong_cat_1")
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


STYLE = (f"DRAWING STYLE (very important): exactly the hand-drawn style of image 2: a wobbly dark-brown INK outline ({MUC}, about 7 px) "
         "running all the way round every piece, thinner ink lines (about 4 px) for the few inner lines (plate edges, the jaw line, toes), "
         "every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. Image 1 is painted in a smooth digital cel style "
         "with soft shading: do NOT copy that painting style, its colours, its pebbly skin texture or its dark rock shards. No shading, no "
         "highlights, no gradients, no glow, no shadows: flat colour only.")

# ---------------------------------------------------------------- 1. bố cục
BOCUC = (
    "TASK: draw OUR character of image 2 (the approved design: an armoured desert drake with dusty-brown hide, thick rounded cream "
    "SANDSTONE ARMOUR SLABS with flat ochre bands on the shoulders, on the near forearm and along the spine down the tail, two long "
    "backswept cream stone horns, one amber crystal nose horn, a fierce yellow eye, big dark-brown talons) in EXACTLY the POSE, the "
    "LAYOUT and the SIZE of the creature in image 1: every body part at the same place, the same size, the same angle and with the same "
    "overlaps as in image 1 (if the new picture were laid over image 1, each body part must sit on its old place). Image 1 is ONLY a pose "
    "and layout guide; the LOOK, colours and details come from image 2.",
    "PIECE BY PIECE (positions as in image 1; left/right as seen by the viewer):\n"
    "- HEAD (right, low, pointing to the lower right) with a separate heavy LOWER JAW under it (a zigzag row of small teeth along the "
    "closed mouth), ONE narrow angry yellow eye with a black slit pupil and one small white dot, a heavy dark-brown rock-plated brow; "
    "on the snout, where image 1 has its big red horn, ONE flat straight-edged AMBER CRYSTAL nose horn; where image 1 has the two small "
    "red horns behind it, two small blunt dark-brown horn bumps.\n"
    "- Behind the head, where image 1 has a fan of six blade spines, only TWO long thick backswept cream STONE HORNS (from the back of "
    "the head, sweeping up and back to the upper left, the upper one the longest), no other spines.\n"
    "- On the shoulders and the back, where image 1 has dark angular rock shards (three over the shoulders at the top middle, three on "
    "the back left of the middle), rounded cream SANDSTONE ARMOUR SLABS with one flat ochre band each, about the same places and sizes, "
    "tilted back like the shards; on the tail, where image 1 has two small dark scales, two small sandstone slabs.\n"
    "- BODY: a hunched muscular dusty-brown body (the chest and shoulders in the middle, the hips at the left), cream belly underneath.\n"
    "- NEAR FRONT LEG (middle left, in front of the body): the upper arm from the shoulder down to the left, and the very big FOREARM "
    "plate of image 1 (from its rounded top end above the elbow down to the wrist) covered by a thick cream sandstone armour slab with "
    "ochre bands; at its lower end THREE long curved dark-brown TALONS on the ground (bottom middle).\n"
    "- FAR FRONT LEG (right, behind the head): upper arm and forearm in darker dusty brown, THREE long curved dark-brown talons on the "
    "ground at the far right.\n"
    "- NEAR BACK LEG (left): thigh, shin and foot with dark-brown claws, dusty brown with one ochre stripe on the thigh.\n"
    "- FAR BACK LEG (middle, partly behind): thigh, shin and foot in a slightly darker dusty brown, dark claws.\n"
    "- TAIL: a long tapering tail at the far left, dusty brown with a few flat ochre stripes, cream underside.",
)
COLORS = ("COLOURS (from image 2): hide dusty brown #8E6E52 with a darker #6E533D on the parts turned away and on the far limbs; belly and "
          "throat cream #E8D7B0; armour slabs and the long horns cream #E3CC98 with flat ochre bands #BF8443; nose horn amber #F0A62E with "
          "one lighter flat facet; talons and claws dark brown #3E2F24; eye yellow #F7C43A.")


def p_bocuc():
    out, save = luu("L2_bocuc")
    R1 = (f"image 1 = {Wp(GOC)}: the REFERENCE creature (a beige spiny drake crouching to pounce, turned to the right, in a smooth digital "
          "cel style). Use it ONLY for the pose, the layout and the size of every body part; do NOT copy its look, its colours, its spines, "
          "its rock shards or its painting style.")
    R2 = (f"image 2 = {Wp(CONCEPT)}: our APPROVED character design (hand-drawn: wobbly dark-brown ink line, crayon hatching, flat "
          "colours). Copy its look, materials, colours and drawing style exactly.")
    t = ["IMAGES (attached in this order; open each from its path):", R1, R2, ""] + save + ["", BOCUC[0], "", BOCUC[1], "", COLORS, "",
         STYLE, "", "Mood: a fierce predator drake crouched to pounce, head low, eye narrowed, talons ready; powerful but appealing, a game "
         "hero, not horror. Every limb, the tail and the head joined to the body (no white gaps). No new pieces beyond the list.", "",
         "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow, the character at the same place "
         "and size as in image 1. No sparkles, no glow, no dust, no labels, no frame."]
    p = os.path.join(GUI, "luot_2_bocuc.txt")
    ghi(p, t)
    print(p)


# ---------------------------------------------------------------- tiện ích hình
def nen(A):
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H:
            bg |= lab == i
    return bg


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def doc(p):
    return np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)


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
    im = Image.fromarray(A.astype(np.uint8))
    d = ImageDraw.Draw(im)
    _, imgs, atts = G.nap("att_idle0.json")
    _, to_px = tf()
    for k, a in enumerate(atts):
        P = to_px(np.array(a["xy"], float).reshape(-1, 2))
        h = cv2.convexHull(P.astype(np.float32)).reshape(-1, 2)
        c = [(230, 40, 40), (40, 120, 230), (30, 160, 60), (200, 0, 200)][k % 4]
        d.line([tuple(p) for p in h] + [tuple(h[0])], fill=c, width=2)
        mm = P.mean(0)
        d.text((mm[0] - 14, mm[1] - 6), a["slot"].replace("P_", ""), fill=c)
    d.text((20, 20), f"IoU hình bóng với con gốc {iou:.3f}", fill=(230, 30, 30))
    p = os.path.join(G.MAU, "_so_bocuc.png")
    im.save(p)
    print(os.path.basename(src), f"IoU {iou:.3f}", p)


# ---------------------------------------------------------------- 2. nhóm mảnh
# khối: tên → (các slot của họ mà khối phủ, vùng dự kiến = hợp mặt nạ các part gốc này, mô tả tiếng Anh, cách vẽ phần khuất)
KHOI = {
    "than": (["P_shenti01", "P_shenti02", "P_weiba"], None,
             "the BODY as ONE continuous shape: the hunched dusty-brown body (chest and shoulders in the middle, hips at the left), the long "
             "TAIL at the far left and the NEAR BACK LEG (left: thigh, shin and foot with its dark claws), all joined as one surface",
             "NO ink line where the back leg or the tail joins the body. Remove the head, the jaw, the horns, every armour slab, both front "
             "legs and the far back leg; where they covered the body, the body continues as plain dusty-brown hide with the same few ochre "
             "stripes and the cream belly (the back under the armour slabs, the chest and shoulder under the near front leg); the neck "
             "continues up and to the right to where the head was and ends there in a rounded neck end"),
    "chan_xa": (["P_datui02", "P_xiaotui02", "P_jiao02"], None,
                "the FAR BACK LEG (middle, partly behind the body): thigh, shin and foot with its dark claws as ONE continuous shape",
                "no ink line between thigh, shin and foot; its top, hidden behind the body, completed as a rounded thigh"),
    "tay_xa": (["P_shoubi02", "P_shouzhang02"], None,
               "the FAR FRONT LEG (right, behind the head): upper arm and forearm as ONE continuous shape, WITHOUT its three talons",
               "no ink line at the elbow; its upper end, hidden behind the head and body, completed as a rounded shoulder; its lower end, "
               "where the talons grow, a rounded paw"),
    "tay_gan": (["P_shoubi01", "P_shouzhang01"], None,
                "the NEAR FRONT LEG (middle left): the upper arm and the very big armoured FOREARM with its thick cream sandstone armour slab "
                "and ochre bands, as ONE shape, WITHOUT its three talons",
                "its shoulder end, hidden under the shoulder, completed as a rounded joint; its lower end, where the talons grow, a rounded "
                "paw"),
    "dau": (["P_tou"], None,
            "the HEAD (right, low) WITHOUT the lower jaw, WITHOUT the eye, WITHOUT any horn",
            "where the eye was, plain hide under the heavy dark brow; where the horns stand, plain hide; the back of the head, hidden behind "
            "the horns and the neck, completed as a rounded skull; its lower edge is the upper jaw with its zigzag row of upper teeth"),
    "ham": (["P_xiaba"], None, "the LOWER JAW (under the head) alone",
            "its back end, hidden under the head, completed as a rounded hinge; the zigzag row of lower teeth along its top edge"),
    "sung_tren": (["P_qi09"], ["P_qi09", "P_qi10", "P_qi11"], "the UPPER long backswept cream stone HORN (the longest one)",
                  "its root, hidden in the back of the head, completed as a rounded base"),
    "sung_duoi": (["P_qi08"], ["P_qi08", "P_qi01"], "the LOWER long backswept cream stone HORN",
                  "its root, hidden in the back of the head, completed as a rounded base"),
    "sung_mui": (["P_jian03"], None, "the AMBER CRYSTAL nose horn", "its base, hidden in the snout, completed as a straight flat base"),
    "u1": (["P_jian01"], None, "the SMALL dark-brown horn bump nearer the back of the head", "complete its base"),
    "u2": (["P_jian02"], None, "the SMALL dark-brown horn bump nearer the snout", "complete its base"),
    "mat": (["P_yanjing01"], None, "the yellow EYE with its black slit pupil and the dark rock-plated brow right above it",
            "complete it as one closed shape (the eye and the brow ledge)"),
}
# giáp lưng, vảy đuôi: theo VÙNG trên bố cục (GPT vẽ giáp khác chỗ, khác cỡ đá của họ: tô theo mặt nạ part gốc thì lệch). Mỗi tấm gán cho một
# slot đá / vảy của họ có xương hợp chỗ (con của ngực / hông / đuôi); P_shitou01, P_shitou02 (đá trên vai phải, chỗ đó bố cục là hai sừng) bỏ.
# Số vùng đọc trên mau/_vung_bocuc.png (rong_cat_manh.py vung).
VUNG_BC = {"giap0": [30], "giap03": [24], "giap06": [50], "giap05": [44], "vay02": [57], "vay01": [68, 72],
           "sung_tren": [4], "sung_duoi": [9], "sung_mui": [58]}
for _k, _s in (("giap0", "P_shitou0"), ("giap03", "P_shitou03"), ("giap06", "P_shitou06"), ("giap05", "P_shitou05")):
    KHOI[_k] = ([_s], None, None, "complete it into one closed rounded slab: its lower end, hidden in the body, rounded too")
for _k, _s in (("vay01", "P_linpian01"), ("vay02", "P_linpian02")):
    KHOI[_k] = ([_s], None, None, "complete it into one closed small slab (or slabs)")
for _s in ("P_zhuazi01", "P_zhuazi02", "P_zhuazi03", "P_zhuazi04", "P_zhuazi05", "P_zhuazi06"):
    KHOI["vuot" + _s[-2:]] = ([_s], None, None, "complete its root, hidden in the paw, as a rounded base")
for _k in ("u1", "u2", "mat"):                     # u1, u2: hai u sừng nhỏ vẽ liền vào đầu; mắt cắt thẳng từ bố cục (không bị che)
    KHOI.pop(_k, None)
# chân sau gần gen RIÊNG (N6): ở N1 nó dính liền thân, cắt theo hình bóng gốc thì ống chân nằm trong mảnh đuôi (đung đưa sai khi bước)
KHOI["chan_gan"] = (["P_datui01", "P_xiaotui01", "P_jiao01"], None,
                    "the NEAR BACK LEG (left, in front of the body): thigh, shin and foot with its dark claws as ONE continuous shape",
                    "no ink line between thigh, shin and foot; its top (the hip, hidden in the body) completed as a big rounded thigh top")
VUNG_BC["chan_gan"] = [92, 67]
KHOI["dau"] = (["P_tou"], None, "the HEAD (right, low) WITHOUT the lower jaw, WITHOUT the eye, WITHOUT the amber nose horn, WITHOUT the two "
               "long horns, but WITH its two small dark-brown horn bumps on top",
               "where the eye was, plain hide under the heavy dark brow; under the nose horn, plain hide; the back of the head, hidden behind "
               "the long horns and the neck, completed as a rounded skull; its lower edge is the upper jaw with its zigzag row of upper teeth")

# tên vị trí cho mô tả các khối nhỏ (đọc trên _goc_vien.png)
VI_TRI = {"giap0": "the big armour slab at the top LEFT of the back", "giap03": "the armour slab at the TOP of the back (right of the "
          "big one, left of the long horns)", "giap06": "the armour slab in the MIDDLE of the back, just above the big striped forearm "
          "slab", "giap05": "the armour slab on the LEFT end of the back (behind the big striped forearm slab)",
          "vay01": "the TWO small slabs on the tail", "vay02": "the small slab on the tail base, near the hips",
          "vuot01": "the near front talon in the MIDDLE (the longest of the three bottom-middle talons)",
          "vuot03": "the LEFT talon of the three bottom-middle talons", "vuot04": "the RIGHT (shortest) talon of the three bottom-middle talons",
          "vuot02": "the middle talon of the three talons at the far RIGHT", "vuot05": "the RIGHTMOST talon at the far right",
          "vuot06": "the LEFT talon of the three talons at the far right"}


_VL = {}


def vung_bocuc():
    """nhãn vùng (mặt kín giữa các nét mực) của bố cục: mau/_vung_lab.npy (rong_cat_manh.py vung)."""
    if "lab" not in _VL:
        _VL["lab"] = np.load(os.path.join(G.MAU, "_vung_lab.npy"))
    return _VL["lab"]


def mat_na_khoi(k):
    if k in VUNG_BC:
        lab = vung_bocuc()
        m = np.isin(lab, VUNG_BC[k])
        return cv2.dilate(m.astype(np.uint8), el(7)).astype(bool)
    MN = mat_na_part()
    slots, vung, _, _ = KHOI[k]
    m = np.zeros((H, W), bool)
    for s in (vung or slots):
        m |= MN[s][0]
    return m


def chia_nhom():
    """xếp các khối vào nhóm sao cho trong một nhóm không khối nào chạm khối nào (mặt nạ nới 9 px). Khối to xếp trước."""
    ks = sorted(KHOI, key=lambda k: -mat_na_khoi(k).sum())
    gian = {k: cv2.dilate(mat_na_khoi(k).astype(np.uint8), el(9)).astype(bool) for k in ks}
    nhom = []
    for k in ks:
        for g in nhom:
            if all(not (gian[k] & gian[o]).any() for o in g):
                g.append(k)
                break
        else:
            nhom.append([k])
    return {f"N{i + 1}": g for i, g in enumerate(nhom)}


def mo_ta(k):
    _, _, mt, kh = KHOI[k]
    if mt is None:
        if k.startswith("giap"):
            mt = VI_TRI[k] + " (a rounded cream sandstone slab with one flat ochre band)"
        elif k.startswith("vay"):
            mt = VI_TRI[k] + " (a small rounded cream sandstone slab with an ochre band)"
        else:
            mt = VI_TRI[k] + " (a long curved dark-brown talon)"
    return mt, kh


# nhóm đặt tay (chia_nhom tự động xếp tấm giáp chung nhóm với thân vì mặt nạ thân gốc nhỏ hơn thân đã vẽ đủ phần khuất dưới giáp)
NHOM_TAY = {"N1": ["vuot02"], "N7": ["than"], "N6": ["chan_gan"],          # N7 = N1 vẽ lại bỏ chân sau gần (luot_2_N7.txt viết tay)
            "N2": ["tay_gan", "tay_xa", "vay01"],
            "N3": ["dau", "chan_xa", "giap0", "vay02", "vuot03", "vuot05", "vuot06"],
            "N4": ["sung_duoi", "ham", "giap06", "vuot01"],
            "N5": ["giap03", "sung_tren", "sung_mui", "vuot04", "giap05"]}


def p_nhom():
    src = moi_nhat("L2_bocuc")
    if not src:
        sys.exit("chưa có L2_bocuc")
    NH = NHOM_TAY
    assert sorted(k for g in NH.values() for k in g) == sorted(KHOI), sorted(set(KHOI) ^ {k for g in NH.values() for k in g})
    json.dump(NH, open(os.path.join(G.MAU, "nhom.json"), "w"), indent=1)
    A = doc(src)
    for nh, ks in NH.items():
        if nh == "N7":
            continue
        # tờ viền: bố cục mờ, khối cần giữ đậm + viền đỏ quanh vùng dự kiến
        m = np.zeros((H, W), bool)
        for k in ks:
            m |= mat_na_khoi(k)
        m2 = cv2.dilate(m.astype(np.uint8), el(14)).astype(bool)
        B = (A * 0.35 + 255 * 0.65).astype(np.uint8)
        B[m2] = A[m2]
        vien = cv2.dilate(m2.astype(np.uint8), el(3)).astype(bool) & ~m2
        B[vien] = (230, 30, 30)
        pv = os.path.join(G.MAU, f"_vien_{nh}.png")
        Image.fromarray(B).save(pv)
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(src)}: the APPROVED picture of our character (an armoured sandstone drake, hand-drawn: wobbly dark-brown ink "
             "line, crayon hatching, flat colours).",
             f"image 2 = {Wp(pv)}: the same picture with the parts to KEEP shown in full colour inside RED outlines; everything faded is to "
             "be removed.", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP (the parts inside the red outlines of image 2), each in exactly the "
             "SAME POSITION and at exactly the SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must "
             "coincide with image 1). REMOVE everything else (pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the "
             "dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, draw the hidden "
             "portion as it would continue, in the same style, colours and flat crayon colouring. Same wobbly dark-brown ink line (about 7 "
             "px), same colours, completely flat colouring as image 1 (no shading, no highlights, no glow, no shadows). Do not move, resize, "
             "rotate or redesign anything. Do NOT draw the red outlines. Keep a clear white gap between the kept parts.", "", "KEEP:"]
        for i, k in enumerate(ks, 1):
            mt, kh = mo_ta(k)
            t.append(f"{i}. {mt}: {kh}.")
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        print(p, ks)


# ---------------------------------------------------------------- 3. cắt
def khu_vien(rgb, mm, r=2):
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def luu_manh(A, m, ten, DATJ, nguon, al_ngoai=None):
    """lưu mảnh: m = mặt nạ hình; al_ngoai (tuỳ chọn) = alpha 0..1 nhân thêm (mép cắt mờ dần của khối liền)."""
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    if al_ngoai is not None:
        al = al * al_ngoai[y0:y1, x0:x1]
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=nguon)
    return x0, y0, x1, y1


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd)) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    os.makedirs(MANH, exist_ok=True)
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w"), indent=1)


LE = 26          # khối liền: mỗi slot lấn sang slot kề LE px
MO = 10          # mép cắt mờ dần MO px


UU_TIEN = {"than": ["P_shenti01", "P_shenti02", "P_weiba"]}     # mặt liền: thân / đuôi nhận hết điểm trong hình bóng gốc của chúng (chân
                                                                # chỉ lấy phần LÒI ra ngoài thân + lấn LE px): sọc đuôi, bụng kem không dính
                                                                # vào ống chân mà đong đưa theo bước chân


def chia_lien(fg, slots, uu=()):
    """chia hình khối liền (fg) cho các slot: điểm thuộc slot vẽ TRÊN CÙNG có mặt nạ gốc chứa nó; không slot nào chứa thì slot gần nhất.
    Trả {slot: (mặt nạ lấn LE px, alpha mép cắt)}."""
    MN = mat_na_part()
    order = sorted(slots, key=lambda s: MN[s][1])
    lab = np.full((H, W), -1, np.int32)
    for i, s in enumerate(order):                                  # vẽ sau đè lên
        lab[MN[s][0] & fg] = i
    for s in uu:                                                   # slot ưu tiên nhận lại điểm trong hình bóng gốc của nó
        lab[MN[s][0] & fg] = order.index(s)
    con = fg & (lab < 0)
    if con.any():
        best = np.full((H, W), 1e9, np.float32)
        for i, s in enumerate(order):
            d = cv2.distanceTransform((~MN[s][0]).astype(np.uint8), cv2.DIST_L2, 5)
            sel = con & (d < best)
            lab[sel] = i
            best = np.where(sel, d, best)
    out = {}
    for i, s in enumerate(order):
        vung = (lab == i)
        if not vung.any():
            out[s] = None
            continue
        d = cv2.distanceTransform((~vung).astype(np.uint8), cv2.DIST_L2, 5)
        m = fg & (d <= LE)
        al = np.clip((LE + 0.5 - d) / MO, 0, 1)
        al[vung] = 1.0
        out[s] = (m, al)
    return out


def cat(chi=None):
    NH = json.load(open(os.path.join(G.MAU, "nhom.json")))
    DATJ = nap_dat()
    for nh, ks in NH.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A = doc(src)
        fg = ~nen(A)
        fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1)).astype(bool)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        # khoảng cách tới vùng dự kiến của từng khối
        dk = {k: cv2.distanceTransform((~mat_na_khoi(k)).astype(np.uint8), cv2.DIST_L2, 5) for k in ks}
        gan = {k: np.zeros((H, W), bool) for k in ks}
        print(f"{nh} ({os.path.basename(src)}):")
        for i in range(1, n):
            if st[i, 4] < 40:
                continue
            mi = lab == i
            # cụm phủ nhiều khối (GPT để dính): chia theo khối gần nhất từng điểm
            dd = np.stack([dk[k][mi] for k in ks], 0)
            j = dd.argmin(0)
            if dd.min(0).mean() > 120:
                print(f"  bỏ cụm ở ({cen[i][0]:.0f}, {cen[i][1]:.0f}), {st[i, 4]} px")
                continue
            ys, xs = np.nonzero(mi)
            for q, k in enumerate(ks):
                sel = j == q
                if sel.any():
                    gan[k][ys[sel], xs[sel]] = True
        for k in ks:
            m = gan[k]
            if m.sum() < 60:
                print(f"  {k:10s} KHÔNG THẤY MẢNH")
                continue
            # lấp lỗ (giấy trắng khép kín) chỉ ở khối lớn (mắt có chấm trắng thì giữ)
            slots = KHOI[k][0]
            if k == "tay_gan":
                cat_tay_gan(A, m, DATJ, os.path.basename(src))
                continue
            if k == "than" and "M_N1" in os.path.basename(src):    # (bản cũ) ống chân sau gần dính trong N1: bỏ, chân lấy ở N6
                m = m & ~cv2.dilate((vung_bocuc() == 92).astype(np.uint8), el(10)).astype(bool)
                n2, lab2, st2, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
                m = lab2 == 1 + int(np.argmax(st2[1:, 4]))           # bỏ mẩu vuốt / ống chân vụn còn sót
            if len(slots) == 1:
                b = luu_manh(A, m, slots[0], DATJ, os.path.basename(src))
                print(f"  {k:10s} → {slots[0]:14s} hộp {b}")
            else:
                ph = chia_lien(m, slots, UU_TIEN.get(k, ()))
                for s, v in ph.items():
                    if v is None:
                        print(f"  {k:10s} → {s:14s} KHÔNG CÓ VÙNG")
                        continue
                    b = luu_manh(A, v[0], s, DATJ, os.path.basename(src) + " (khối liền)", al_ngoai=v[1])
                    print(f"  {k:10s} → {s:14s} hộp {b}")
    ghi_dat(DATJ)
    if not chi or {"N3", "N6"} & set(chi):                         # chân sau: luôn tô lại trên part gốc (đè mảnh GPT vừa cắt)
        chan_goc()


def cat_tay_gan(A, m, DATJ, nguon):
    """tay gần: tấm giáp cẳng (kem / son, viền kín riêng) → P_shouzhang01; phần nâu bên PHẢI khuỷu (vai → khuỷu) → P_shoubi01. Phần nâu
    bên trái tấm giáp (GPT vẽ cánh tay dài quá khuỷu gốc, nấp sau giáp lưng) bỏ: để nó trong tấm cẳng thì xoay theo cẳng thành cục nâu lòi ra."""
    rgb = A.astype(np.int32)
    kem = m & (rgb[..., 0] > 200) & (rgb[..., 1] > 110) & (rgb[..., 2] < 190)          # kem (247, 200, 128) + son (216, 131, 51); nâu da (181, 116, 76) loại
    n, lab, st, _ = cv2.connectedComponentsWithStats(kem.astype(np.uint8), 8)
    k = 1 + int(np.argmax(st[1:, 4]))
    tam = cv2.morphologyEx((lab == k).astype(np.uint8), cv2.MORPH_CLOSE, el(9))
    cs, _ = cv2.findContours(tam, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    tam = cv2.drawContours(np.zeros_like(tam), cs, -1, 1, -1)
    tam = cv2.dilate(tam, el(7)).astype(bool) & m                     # + viền mực của tấm
    print("  tay_gan    → P_shouzhang01  hộp", luu_manh(A, tam, "P_shouzhang01", DATJ, nguon + " (tấm cẳng)"))
    _, to_px = tf()
    W0 = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    b20 = next(b for b in W0["bones"] if b["name"] == "bone20")
    khuyu = to_px(np.array([[b20["x"], b20["y"]]]))[0]
    nau = m & ~tam
    nau = cv2.morphologyEx(nau.astype(np.uint8), cv2.MORPH_OPEN, el(7)).astype(bool)     # bỏ dải viền mảnh còn sót quanh tấm cẳng
    yy, xx = np.mgrid[0:H, 0:W]
    nau &= xx > khuyu[0] - 10
    n, lab, st, _ = cv2.connectedComponentsWithStats(nau.astype(np.uint8), 8)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, 4]))
        nau = lab == k
        # phần nâu nấp dưới tấm cẳng: lấn vào trong tấm 20 px cho khuỷu kín khi cẳng xoay
        lan = cv2.dilate(nau.astype(np.uint8), el(20)).astype(bool) & tam & ~cv2.erode(tam.astype(np.uint8), el(40)).astype(bool)
        A2 = A.copy()
        mau = np.median(A[nau & ~cv2.dilate((~nau).astype(np.uint8), el(8)).astype(bool)], 0)
        A2[lan] = mau
        print("  tay_gan    → P_shoubi01     hộp", luu_manh(A2, nau | lan, "P_shoubi01", DATJ, nguon + " (cánh tay, phải khuỷu)"))


# ---------------------------------------------------------------- chân sau: tô lại TRÊN hình bóng part gốc (không theo mảnh GPT)
CHAN = {"gan": (["P_datui01", "P_xiaotui01", "P_jiao01"], "M_N6"), "xa": (["P_datui02", "P_xiaotui02", "P_jiao02"], "M_N3")}


def _vat_lieu(src, tam):
    """màu da (trung vị) + mẫu vân sáp (độ lệch độ sáng 96 × 96) lấy trong mảng da nâu quanh `tam` của ảnh GPT."""
    A = doc(src)
    lum = A.mean(2)
    nau = (A[..., 0] > 120) & (A[..., 0] < 215) & (A[..., 2] < 120) & (A[..., 0] - A[..., 2] > 60)
    nau &= ~cv2.dilate((lum < 80).astype(np.uint8), el(5)).astype(bool)
    yy, xx = np.nonzero(nau)
    d = np.hypot(xx - tam[0], yy - tam[1])
    sel = d < np.percentile(d, 30)
    mau = np.median(A[yy[sel], xx[sel]], 0)
    # mẫu vân: ô 96 × 96 nằm trọn trong da nâu của THÂN (M_N1, mảng nâu lớn nhất) cho mọi chân cùng một kiểu vân
    B = doc(moi_nhat("M_N1"))
    lb = B.mean(2)
    nb = (B[..., 0] > 120) & (B[..., 0] < 215) & (B[..., 2] < 120) & (B[..., 0] - B[..., 2] > 60)
    best = None
    for y0 in range(0, H - 96, 16):
        for x0 in range(0, W - 96, 16):
            if nb[y0:y0 + 96, x0:x0 + 96].mean() > 0.995:
                best = (x0, y0)
                break
        if best:
            break
    x0, y0 = best
    patch = lb[y0:y0 + 96, x0:x0 + 96]
    return mau, (patch - patch.mean()) / max(1.0, patch.mean())


def _mat_na_manh(DATJ, slots):
    """hợp hình (alpha > 0,5) của các mảnh đã cắt, đặt đúng hộp trên khung concept."""
    m = np.zeros((H, W), bool)
    for s_ in slots:
        if s_ not in DATJ:
            continue
        x0, y0, x1, y1 = DATJ[s_]["hop"]
        a = np.asarray(Image.open(os.path.join(MANH, s_ + ".png")).convert("RGBA"))[..., 3] > 128
        m[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] |= a[:H - y0, :W - x0]
    return m


def chan_goc():
    """chân sau gần / xa: hình bóng ĐÚNG part gốc ở khung 0 idle (các khúc chồng nhau đúng như người vẽ gốc dựng, gập mạnh không hở như mảnh
    GPT), tô lại theo thiết kế: da nâu (màu + vân sáp của THÂN GPT cho chân gần liền một bề mặt với thân), vuốt nâu sẫm.
    MỘT BỀ MẶT (người dùng chê "bụng bị lỗi": đùi gốc có mép trên răng cưa, viền kín từng khúc vẽ đè lên thân thành vết rách): mép nào của một khúc
    nằm TRONG mảnh vẽ dưới nó (thân với chân gần; khúc dưới với khúc trên) thì KHÔNG kẻ mực và mờ dần 12 px, chỉ mép lộ ra ngoài mới có viền.
    Chân xa sẫm hơn."""
    DATJ = nap_dat()
    _, to_px = tf()
    _, imgs, atts = G.nap("att_idle0.json")
    by = {a["slot"]: a for a in atts}
    MUC_RGB = np.array([43, 33, 24])
    VUOT = np.array([70, 50, 38])
    than = _mat_na_manh(DATJ, ["P_shenti01", "P_shenti02", "P_weiba"])
    B = doc(moi_nhat("M_N7"))
    nau_than = than & (B[..., 0] > 120) & (B[..., 2] < 120) & (B[..., 0] - B[..., 2] > 60) & (B.mean(2) > 90)
    mau_than = np.median(B[nau_than], 0)
    for ben, (slots, src_ten) in CHAN.items():
        src = moi_nhat(src_ten)
        hop_all = np.concatenate([np.argwhere(mat_na_part()[s][0]) for s in slots])
        tam = hop_all.mean(0)[::-1]
        _, van = _vat_lieu(src, tam)
        mau = mau_than * (0.86 if ben == "xa" else 1.0)
        # hình bóng từng khúc ở khung 0 idle
        HB = {}
        for s in slots:
            a = by[s]
            im = G.part_goc(a)
            uv, tr = G.luoi(a)
            lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
            _tris(lay, im.convert("RGBa"), to_px(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
            L = np.asarray(lay.convert("RGBA")).astype(np.int32)
            m = cv2.morphologyEx((L[..., 3] > 110).astype(np.uint8), cv2.MORPH_CLOSE, el(3)).astype(bool)
            m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, el(4)).astype(bool)          # gọt răng cưa nhỏ ở mép
            HB[s] = (m, L)
        thu_tu = sorted(slots, key=lambda q: mat_na_part()[q][1])                              # vẽ trước → sau
        for s in slots:
            m, L = HB[s]
            lum = L[..., :3].mean(2)
            duoi = np.zeros((H, W), bool)                                                      # các mảnh vẽ DƯỚI khúc này
            for q in thu_tu[:thu_tu.index(s)]:
                duoi |= HB[q][0]
            # chân gần nay vẽ DƯỚI thân (rong_cat_rig.thu_tu_slot): đỉnh đùi luôn nấp sau hông, mọi mép khúc có viền kín (mép mờ dần bị lộ ra
            # khi chân bước / lao thành vệt nhoè); thân không còn tính là mảnh dưới
            trong = np.zeros((H, W), bool)
            vuot = m & (lum >= 40) & (lum < 92)
            if not s.startswith("P_jiao"):
                vuot[:] = False
            else:
                n, lab, st, cen = cv2.connectedComponentsWithStats(vuot.astype(np.uint8), 8)
                ys = np.nonzero(m)[0]
                ymid = (ys.min() + ys.max()) / 2
                keep = [i for i in range(1, n) if st[i, 4] > 60 and cen[i][1] > ymid]
                vuot = cv2.morphologyEx(np.isin(lab, keep).astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)
            vt = np.tile(van, (H // 96 + 1, W // 96 + 1))[:H, :W]
            da = np.clip(mau[None, None, :] * (1 + 0.9 * vt[..., None]), 0, 255)
            cvu = np.clip(VUOT[None, None, :] * (1 + 0.9 * vt[..., None]), 0, 255)
            rgb = np.where(vuot[..., None], cvu, da)
            vien = m & ~cv2.erode(m.astype(np.uint8), el(6)).astype(bool)
            vien_lo = vien & ~trong                                                            # chỉ mép lộ ra ngoài mới kẻ mực
            vien_vuot = vuot & ~cv2.erode(vuot.astype(np.uint8), el(2)).astype(bool)
            rgb[vien_lo | vien_vuot] = MUC_RGB
            # alpha: mép nằm trong mảnh dưới mờ dần 12 px (khoảng cách tới mép hình); mép lộ giữ đặc
            dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
            al = np.where(trong, np.clip(dt / 12.0, 0, 1), 1.0)
            print(s, luu_manh(rgb.astype(np.int32), m, s, DATJ, f"tô lại trên part gốc, một bề mặt ({os.path.basename(src)}: vân)",
                              al_ngoai=al))
    ghi_dat(DATJ)

def ghep(bg="bocuc"):
    """ghép mảnh theo thứ tự vẽ idle lên nền trắng, đặt cạnh bố cục; IoU hình bóng."""
    DATJ = nap_dat()
    MN = mat_na_part()
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in sorted(MN, key=lambda s: MN[s][1]):
        if s not in DATJ:
            thieu.append(s)
            continue
        x0, y0, _, _ = DATJ[s]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = doc(moi_nhat("L2_bocuc"))
    Gp = np.asarray(can.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    can.convert("RGB").save(os.path.join(MANH, "_ghep_to.png"))
    print(p, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


def mat():
    """mắt mở cắt thẳng từ bố cục (không bị mảnh nào che): tròng vàng (vùng 61) + con ngươi, chấm sáng + vành mực quanh → manh/P_yanjing01."""
    DATJ = nap_dat()
    A = doc(moi_nhat("L2_bocuc"))
    lab = vung_bocuc()
    m = lab == 61
    ys, xs = np.nonzero(m)
    hop = np.zeros((H, W), bool)
    hop[ys.min() - 14:ys.max() + 15, xs.min() - 14:xs.max() + 15] = True
    toi = (A.mean(2) < 90) & hop
    k = cv2.dilate(m.astype(np.uint8), el(9)).astype(bool) & (toi | m)
    k |= cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(6)).astype(bool)
    cs, _ = cv2.findContours(cv2.morphologyEx(k.astype(np.uint8), cv2.MORPH_CLOSE, el(3)), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    kin = cv2.drawContours(np.zeros((H, W), np.uint8), cs, -1, 1, -1).astype(bool) & cv2.dilate(m.astype(np.uint8), el(10)).astype(bool)
    print("P_yanjing01", luu_manh(A, kin, "P_yanjing01", DATJ, os.path.basename(moi_nhat("L2_bocuc")) + " (cắt thẳng)"))
    ghi_dat(DATJ)


def mat_nham():
    """mắt nhắm (hit, block của họ đổi hình mắt) dựng từ mảnh mắt của mình: tròng vàng tô màu da quanh nó, kẻ một nét mực cong (mí khép)
    dọc giữa tròng → manh/mat_nham.png (cùng hộp với P_yanjing01)."""
    DATJ = nap_dat()
    im = np.asarray(Image.open(os.path.join(MANH, "P_yanjing01.png")).convert("RGBA")).copy()
    rgb = im[..., :3].astype(np.int32)
    al = im[..., 3] > 128
    vang = al & (rgb[..., 0] > 180) & (rgb[..., 1] > 140) & (rgb[..., 2] < 140)          # tròng vàng
    con = al & (rgb.max(2) < 70) & cv2.dilate(vang.astype(np.uint8), el(6)).astype(bool)  # con ngươi + vành mực quanh tròng
    trong = cv2.morphologyEx((vang | con).astype(np.uint8), cv2.MORPH_CLOSE, el(4))
    cs, _ = cv2.findContours(trong, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    trong = cv2.drawContours(np.zeros_like(trong), cs, -1, 1, -1).astype(bool)          # lấp cả chấm sáng trắng trong tròng
    if trong.sum() < 20:
        print("mắt nhắm: không thấy tròng vàng")
        return
    # màu da đầu lấy ngay trên bố cục (vùng đầu, mặt kín 51); cả mảnh tô màu da (mắt khép mất hẳn tròng và vành), chỉ còn nét mí
    lab = vung_bocuc()
    Abc = doc(moi_nhat("L2_bocuc"))
    mau = np.median(Abc[lab == 51], 0)
    out = im.copy()
    out[al, :3] = mau.astype(np.uint8)
    out[..., 3] = np.where(al, 255, out[..., 3])
    ys, xs = np.nonzero(trong)
    pil = Image.fromarray(out, "RGBA")
    d = ImageDraw.Draw(pil)
    x0, x1 = xs.min(), xs.max()
    yc = (ys.min() + ys.max()) / 2
    pts = [(x, yc + 0.18 * (ys.max() - ys.min()) * math.sin(math.pi * (x - x0) / max(1, x1 - x0))) for x in range(x0, x1 + 1, 2)]
    d.line(pts, fill=(43, 33, 24, 255), width=max(3, int(round(0.012 * W / 4))))
    pil.save(os.path.join(MANH, "mat_nham.png"))
    DATJ["mat_nham"] = dict(DATJ["P_yanjing01"], nguon="dựng từ P_yanjing01")
    ghi_dat(DATJ)
    print("mat_nham", DATJ["mat_nham"]["hop"])


def goc():
    """bộ mảnh TẠM bằng da gốc (chỉ để chạy thử rig trong máy khi chưa có mảnh của mình): mỗi part của họ vẽ đúng chỗ khung 0 idle trên
    khung concept → manh_goc/<slot>.png + dat.json; mắt nhắm lấy hình phụ của họ."""
    ra = os.path.join(G.BASE, "manh_goc")
    os.makedirs(ra, exist_ok=True)
    _, to_px = tf()
    DATJ = {}
    _, imgs, atts = G.nap("att_idle0.json")

    def ve(a, ten):
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), to_px(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        lay = lay.convert("RGBA")
        bb = lay.getbbox()
        lay.crop(bb).save(os.path.join(ra, ten + ".png"))
        DATJ[ten] = dict(hop=[bb[0], bb[1], bb[2], bb[3]], nguon="da gốc")

    for a in atts:
        ve(a, a["slot"])
    # mắt nhắm: hình P_yanjing01 của họ (ở dáng idle 0 thay cho hình mở)
    D0 = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    a = next(x for x in D0["atts"] if x["slot"] == "P_yanjing01")
    b = dict(a)
    b["region"] = "P_yanjing01"
    try:
        ve(b, "mat_nham")
    except Exception as e:                                   # noqa: BLE001
        print("mắt nhắm:", e)
    json.dump(DATJ, open(os.path.join(ra, "dat.json"), "w"), indent=1)
    print(ra, len(DATJ))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "goc":
        goc()
    elif cmd == "bocuc":
        p_bocuc()
    elif cmd == "so_bocuc":
        so_bocuc()
    elif cmd == "chia":
        for k, v in chia_nhom().items():
            print(k, v)
    elif cmd == "nhom":
        p_nhom()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    elif cmd == "mat_nham":
        mat_nham()
    elif cmd == "mat":
        mat()
        mat_nham()
    elif cmd == "chan_goc":
        chan_goc()
    else:
        print(__doc__)
