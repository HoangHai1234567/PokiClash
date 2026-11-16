# -*- coding: utf-8 -*-
"""Sói giáp sắt DẠNG 1 (soi_giap_non): sói con chibi trên CÙNG rig với dạng 2 (monster_3428), tỉ lệ đổi ở rig (soi_giap_rig.py SG_DANG=non).
Người dùng 2026-11-16: "làm dạng 1", chọn chung rig 3428 + "ít giáp, màu nhạt" (Claude gen vài hướng để chọn).

    soi_giap_non.py khung      hình bố cục (mau/bo_cuc.png, dựng bằng da dạng 2 ở tỉ lệ non) đặt giữa khung 1536 × 1024 → mau/bo_cuc_khung.png
    soi_giap_non.py concept    ba file prompt concept → gui_gpt/soi_giap_non/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    soi_giap_non.py so         chồng viền bố cục lên từng concept, in độ khớp → mau/_so_bo_cuc.png
Hình con gốc không đính cho GPT (bố cục đã là hình của mình)."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soi_giap_da as D  # noqa: E402

W, H = 1536, 1024
BASE = os.path.join(HERE, "inbox", "soi_giap_non")
MAU, TAI = os.path.join(BASE, "mau"), os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "soi_giap_non")
DANG2 = os.path.join(HERE, "inbox", "soi_giap_1", "tai_ve", "L1_duyet.png")
HO_CON = os.path.join(HERE, "inbox", "hoa_ho_non", "tai_ve", "L1_duyet.png")
Wp, ghi = D.Wp, D.ghi
CAO = 820.0


def khung():
    im = Image.open(os.path.join(MAU, "bo_cuc.png")).convert("RGB")
    k = CAO / im.height
    w, h = round(im.width * k), round(im.height * k)
    can = Image.new("RGB", (W, H), "white")
    ox, oy = (W - w) // 2, (H - h) // 2
    can.paste(im.resize((w, h), Image.LANCZOS), (ox, oy))
    p = os.path.join(MAU, "bo_cuc_khung.png")
    can.save(p)
    json.dump(dict(k=k, ox=ox, oy=oy), open(p[:-4] + ".json", "w"), indent=1)        # px khung = (px bố cục · k + ox, · k + oy)
    print(p, (w, h))


MO_TA = (
    "THE LAYOUT (image 1, built from our rig, keep it): a young WOLF CUB warrior standing on two short legs in a low ready crouch, its body "
    "turned three-quarters to the viewer's RIGHT, its BIG HEAD (about 40 % of its height) low and pushed forward, ONE eye showing, the muzzle "
    "pointing right; two pointed ears; a helmet on its head; a shoulder pad on the near (left) shoulder; a chest and belly; a belt with a long "
    "cloth flap; the near arm (left) hanging down with its fist gripping a HAMMER whose head rests low at the lower left and whose handle "
    "sticks up to the left; the far arm (right) reaching forward, its paw in front of a SHIELD standing on the right; a small tail tip at the "
    "left behind the hips. Keep the SAME pose, the SAME place and size of every part (head, shoulder pad, arms, legs, hammer, shield), so the "
    "picture still fits the same rig.")
CHUNG = [
    "MAKE IT A CUB (chibi, first form): a chubby, round, compact little body (round tummy, soft fluffy fur, short thick arms and legs, small "
    "round paws), a big round head; the shaggy mane behind the head becomes a SMALL fluffy ruff (much smaller than in image 1, it must not "
    "make a hump on the back); the eye BIG and round, determined and brave, a short frowning brow, the mouth closed with one tiny fang. Cute "
    "but ready to fight; not a baby, not a mascot.",
    "LIGHT ARMOUR, LIGHTER COLOURS than the grown-up form of image 2 (image 2 is the same wolf AFTER it evolves: charcoal fur, full blackened "
    "iron armour with brass): the cub wears little armour, mostly leather and plain iron, and its fur is lighter. No breastplate, no back "
    "plate behind the head, no spikes except where listed.",
]
HUONG = {
    "A": ("sói con xám tro, đồ da + sắt thô",
          "lông xám tro nhạt, mõm kem; mũ sắt tròn nhỏ quai da; giáp vai da tròn; áo gi lê da một khoá; quấn da cẳng tay; đai thừng; khiên gỗ "
          "dáng tám cạnh (tiền thân khiên dạng 2) viền sắt bốn đinh; búa sắt đầu khối nhỏ cán gỗ, không mỏ; mắt hổ phách",
          ["FUR: light ash grey #9C98A2 on the head, back, arms, legs and tail; the muzzle, cheeks, chest fluff, inner ears, paws and tail tip "
           "pale cream #E9E3E6. EYE: amber #F2B33D with a dark pupil and a tiny white dot.",
           "HELMET: a small ROUND raw-iron cap #8E949C (a plain dome) with a dark brown leather chin strap, the ears poking out at its sides. No "
           "fins, no horns.",
           "SHOULDER PAD: one small round brown leather pad #7A5338 with two stitch lines (no metal, no spikes).",
           "CHEST: a brown leather vest #7A5338 over the fluffy pale chest, closed by one small iron buckle; a leather strap round the neck.",
           "FOREARMS: brown leather wraps. BELT: a rope belt with a knot; the cloth flap shorter, faded brown #8A6A4E.",
           "SHIELD: a WOODEN shield of vertical planks #B07D4E in the same eight-sided shape as the grown-up shield (corners cut off), with a "
           "plain iron rim #6E747F and four round iron studs; smaller than image 2's shield (the size of image 1).",
           "HAMMER: a small plain iron hammer #7E848E: a squared block head with no spike, a wooden handle #9A6B43 with a leather grip."]),
    "B": ("sói con xám xanh, mũ da + sắt",
          "lông xám xanh nhạt, mõm kem; mũ da nâu có lỗ tai, đai sắt quanh trán; giáp vai một tấm sắt nhỏ; ngực để lông xù, chỉ có dây đai da chéo; "
          "bao tay da; khiên tròn gỗ viền sắt núm sắt; búa gỗ (vồ) hai đai sắt; mắt cam",
          ["FUR: light blue-grey #8C93A2 on the head, back, arms, legs and tail; the muzzle, cheeks, chest fluff, inner ears, paws and tail tip "
           "pale cream #E8E6EA. EYE: orange #F08A3A with a dark pupil and a tiny white dot.",
           "HELMET: a brown LEATHER cap #84593B that hugs the top of the head, with holes for the two ears and one plain iron band #8E949C round "
           "the forehead. No fins, no horns.",
           "SHOULDER PAD: one small plain iron plate #8E949C with a rounded edge, held by a leather strap.",
           "CHEST: no vest: the fluffy pale chest shows, crossed by one brown leather strap from the shoulder.",
           "FOREARMS: brown leather bracers. BELT: a leather belt with a small iron buckle; the cloth flap shorter, brown #7A5A44.",
           "SHIELD: a ROUND wooden shield #B4834F with a plain iron rim #6E747F and one round iron boss in its middle (the size of image 1's "
           "shield, standing upright on the right).",
           "HAMMER: a wooden MALLET: a fat wooden barrel head #A87444 with two iron bands #7E848E, a wooden handle."]),
    "C": ("sói con xám bạc + than, giáp thép mỏng + đồng (dạng 2 thu nhỏ)",
          "lông xám bạc, lưng và gáy than (gợi dạng 2); mũ sắt đỉnh bằng nhỏ có hai mầm vây ngắn, vành đồng; giáp vai vòm nhỏ MỘT gai cụt; áo da "
          "có một tấm thép nhỏ trên ngực + đinh đồng; khiên gỗ tám cạnh viền thép đinh đồng; búa đầu khối nhỏ có u mỏ; mắt cam",
          ["FUR: silver grey #A9A5AD on the arms, legs and belly, charcoal grey #5E5A62 on the back of the head, the ruff and the tail; the "
           "muzzle, cheeks, chest fluff, inner ears, paws and tail tip pale cream #ECE7EA. EYE: orange #F08A3A with a dark pupil and a tiny "
           "white dot.",
           "HELMET: a small FLAT-TOPPED steel cap #858B95 with a thin brass #D4A451 brim and two very short stubby fins on top (just buds). The "
           "ears poke out at its sides.",
           "SHOULDER PAD: a small steel dome #858B95 with a thin brass rim and ONE short blunt spike.",
           "CHEST: a brown leather vest #7A5338 with one small steel plate on the chest and one brass stud; a leather strap round the neck.",
           "FOREARMS: brown leather wraps with one thin brass band. BELT: a leather belt with a brass buckle; the cloth flap shorter, brown.",
           "SHIELD: a WOODEN eight-sided shield #A9784A (corners cut off, like a small version of the grown-up shield) with a steel rim #6E747F "
           "and four brass studs.",
           "HAMMER: a small steel hammer #7E848E: a squared block head with a tiny blunt bump on its top (a beak not grown yet), a wooden handle "
           "with a brass ring."]),
}
STYLE = (
    "DRAWING STYLE (very important): exactly the hand-drawn look of images 2 and 3: a wobbly dark-brown ink outline (#2B2118, about 7 px) "
    "all the way round every piece, a few thinner inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon "
    "hatching. No shading, no highlights, no gradients, no glow, no shadows. SIMPLE: few details, nothing beyond what is listed.")


def prompt():
    bc = os.path.join(MAU, "bo_cuc_khung.png")
    R = [(bc, "the LAYOUT of the cub, 1536x1024, white background, built from our animation rig with the grown-up wolf's skin at the cub's "
              "proportions (big head, short limbs, small shield and hammer). It gives the POSE and the PLACE and SIZE of every part. Its "
              "look (charcoal fur, blackened iron, brass, big shaggy mane, horned helmet) is NOT the cub's look.",
          "Hình bố cục (1536 × 1024, nền trắng): rig ở tỉ lệ dạng non, da dạng 2. Cho dáng, chỗ, cỡ từng mảnh; KHÔNG phải màu, chất liệu của dạng 1"),
         (DANG2, "the approved GROWN-UP form of the same wolf (what the cub becomes), 1536x1024: match its drawing style; keep the family "
                 "look (wolf face, orange eye, shield, hammer) but NOT its heavy armour or dark colours.",
          "Concept dạng 2 đã duyệt: nét vẽ, nét nhận dòng"),
         (HO_CON, "an approved first-form CUB of another hero (a tiger cub), 1536x1024: see how a cub is drawn: chubby round body, big round "
                  "eye, short thick legs, cute but brave. Do NOT copy its design or colours.",
          "Hổ con (dạng 1 hổ lửa) đã duyệt: cách vẽ thú con chibi")]
    hd = ["# Gói GPT: sói giáp sắt dạng 1 (soi_giap_non): sói con chibi", "",
          "Cùng rig với dạng 2 (monster_3428), tỉ lệ đổi ở rig. Người dùng chọn \"ít giáp, màu nhạt\"; ba hướng để chọn.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: draw ONE picture of OUR character's FIRST FORM: a wolf cub warrior, on the layout of image 1.", "", MO_TA, ""] + CHUNG + [
              "", "DESIGN (this direction):"] + [f"- {d}" for d in doi] + ["", STYLE, "",
              "Both arms, both legs and the tail stay attached to the body; the near fist really grips the hammer handle; the shield stands "
              "behind the far paw.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the cub at the same place and size "
              "as in image 1. No sparkles, no glow, no speed lines, no labels, no frame."]
        ghi(p, t)
        print(p)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): gửi GPT `{Wp(p)}`; ảnh lưu `{Wp(out)}`."]
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng và chỗ từng mảnh như ảnh 1; đầu to, thân tròn mũm mĩm, chân tay ngắn, bờm nhỏ (không bướu); mắt to quả quyết; ít giáp, "
           "màu nhạt hơn dạng 2; tay gần nắm cán búa, khiên sau bàn tay xa; tô phẳng, không bóng; nền trắng."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


def so(ks="ABC"):
    import cv2
    g = D._mat_na(os.path.join(MAU, "bo_cuc_khung.png"))
    cs, _ = cv2.findContours(g.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    o = []
    for k in ks:
        p = os.path.join(TAI, f"L1_{k}.png")
        if not os.path.exists(p):
            continue
        m = D._mat_na(p)
        iou = (m & g).sum() / max(1, (m | g).sum())
        im = np.asarray(Image.open(p).convert("RGB").resize((W, H))).copy()
        cv2.drawContours(im, cs, -1, (230, 30, 30), 3)
        cv2.putText(im, f"{k}  IoU {iou:.3f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (230, 30, 30), 4)
        o.append(Image.fromarray(im).resize((W // 2, H // 2), Image.LANCZOS))
        print(k, f"IoU {iou:.3f}")
    if o:
        c = Image.new("RGB", (W // 2 * len(o), H // 2), "white")
        for i, im in enumerate(o):
            c.paste(im, (i * W // 2, 0))
        c.save(os.path.join(MAU, "_so_bo_cuc.png"))


# ================================================================ MẢNH dạng 1 (concept A đã duyệt: tai_ve/L1_duyet.png)
# Thân / tay / chân: tờ liền như dạng 2 (cùng hình bóng khung part) nhưng màu A, áo gi lê da, quấn da cẳng tay, bờm co còn chỏm lông (CO_BOM).
# Mảnh viền riêng (đuôi, ngón, dây, quai, vạt): đổi màu mảnh dạng 2 bằng mã. Mảnh đổi dáng (mũ, búa, khiên, đầu mắt to, giáp vai da, hai tai):
# gen đúng chỗ trên concept A.
CONCEPT = os.path.join(TAI, "L1_duyet.png")
MANH = os.path.join(BASE, "manh")
MANH2 = os.path.join(HERE, "inbox", "soi_giap_1", "manh")
PAL = dict(long=(173, 154, 158), long_nhat=(241, 229, 221), gang=(149, 89, 59), gang_toi=(120, 70, 46), dong=(111, 67, 42),
           da=(149, 89, 59), vat=(143, 107, 60), vuot=(58, 52, 56), mat=(225, 161, 68))
HX = {k: "#%02X%02X%02X" % v for k, v in PAL.items()}
SAT, GO = "#97999C", "#BB7D4B"


def _sm():
    """soi_giap_manh trỏ sang thư mục + bảng màu dạng 1."""
    import soi_giap as G
    import soi_giap_manh as SM
    G.MAU, G.TAI = MAU, TAI
    SM.MANH = MANH
    SM.MAU = dict(PAL)
    SM.CO_BOM = 0.62
    return G, SM


MOI = {
    "M1": [("mu", f"THE HELMET on the cub's head: the small round raw-iron cap {SAT} (a plain dome) with its brim; draw it COMPLETE as ONE closed "
                  "shape (the parts hidden behind the ears drawn too), WITHOUT the leather chin strap, NO ears, NO face, NO fur.",
            "mũ sắt tròn (không quai, không tai)"),
           ("bua", f"THE WHOLE HAMMER at the lower left: the small iron block head {SAT} and the wooden handle {GO} with its leather grip, going "
                   "up to the left; draw it COMPLETE as ONE closed shape, the part of the handle hidden behind the paw drawn too (straight, same "
                   "width), NO paw, NO fingers.",
            "cả cây búa (vẽ đủ đoạn cán nấp sau bàn tay)"),
           ("khien", f"THE SHIELD on the right: the eight-sided wooden shield of vertical planks {GO} with its iron rim and four iron studs; draw "
                     "it COMPLETE as ONE closed shape, the part hidden behind the paw drawn too, NO paw.",
            "khiên gỗ tám cạnh (vẽ đủ phần nấp sau bàn tay)")],
    "M2": [("dau", "THE HEAD of the cub WITHOUT its helmet and WITHOUT its two ears: the big round head with its grey fur, the cream face and "
                   "muzzle with the black nose, the big amber eye with its frowning brow, the closed mouth with the tiny fang, the spiky cream "
                   "cheek ruff on the left, and the dark brown leather chin strap across the face; where the helmet covered the top of the "
                   "head, draw the top of the head as plain grey fur (a round skull); where the ears were, plain fur. ONE closed shape.",
            "đầu (không mũ, không tai; đỉnh đầu vẽ lông)"),
           ("vai", f"THE SMALL LEATHER SHOULDER PAD on the left shoulder (brown leather {HX['da']} with its stitch); draw it COMPLETE as ONE "
                   "closed shape, its lower part hidden behind the arm drawn too, NO arm, NO fur.",
            "giáp vai da (vẽ đủ phần nấp)")],
    "M3": [("tai_gan", f"THE NEAR EAR (the bigger pointed ear on the LEFT of the helmet): grey fur {HX['long']} outside, cream "
                       f"{HX['long_nhat']} inside; draw it COMPLETE as ONE closed shape, its base hidden under the helmet drawn too, ending in a "
                       "rounded base. NO helmet.",
            "tai gần"),
           ("tai_xa", f"THE FAR EAR (the smaller pointed ear on the RIGHT of the helmet): grey fur {HX['long']} outside, cream "
                      f"{HX['long_nhat']} inside; draw it COMPLETE as ONE closed shape, its base hidden behind the helmet drawn too, ending "
                      "in a rounded base. NO helmet.",
            "tai xa")],
}
VUNG = {"mu": (690, 210, 1030, 420), "bua": (380, 540, 660, 850), "khien": (890, 400, 1130, 820), "dau": (660, 240, 1050, 590),
        "vai": (520, 420, 680, 560), "tai_gan": (700, 210, 820, 340), "tai_xa": (940, 220, 1050, 340)}


def prompt_manh():
    G, SM = _sm()
    SM.to_lien()
    gl = os.path.join(MAU, "lien.png")
    r1 = ("the APPROVED picture of OUR cub (first form), 1536x1024, white background: a chubby ash-grey wolf cub with a cream face and paws, a big "
          "amber eye, a small round iron cap with a leather chin strap, a brown leather vest with an iron buckle, a small stitched leather "
          "shoulder pad, leather wraps on the forearms, a rope belt, a short faded brown cloth flap, a small iron hammer with a wooden handle "
          "and an eight-sided wooden shield with an iron rim. Take from it the design, the colours and the hand-drawn look.")
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh dạng 1 (concept A đã duyệt 2026-11-16)", ""]
    out = os.path.join(TAI, "N_lien.png")
    p = os.path.join(GUI, "luot_2_lien.txt")
    t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {r1}",
         f"image 2 = {Wp(gl)}: BODY GUIDE, 1536x1024, white background, drawn by computer: FIVE flat silhouettes of the cub's body parts WITHOUT "
         "the head, the helmet, the shoulder pad, the straps, the belt, the cloth flap, the shield and the hammer. Top row: the NEAR ARM (furry "
         "upper arm, forearm wrapped in leather, cream paw closed in a fist), the TORSO (the furry hips at the bottom, the chest with the brown "
         "leather vest, a small fluffy ruff at the top right where the neck is), the FAR ARM (furry upper arm, leather-wrapped forearm, cream "
         "paw). Bottom row: the NEAR LEG and the FAR LEG (furry thigh and shin, a cream paw with dark claws). Grey = fur, cream = paws, brown "
         "= leather. It gives the exact silhouettes, sizes and positions.", "",
         f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY every "
         "silhouette of image 2 (same outline, size, position). This sheet will be cut by a program into the body parts of a 2D animation rig.",
         "", "VERY IMPORTANT, ONE CONTINUOUS SURFACE PER SHAPE: draw the dark-brown ink outline ONLY around the OUTSIDE of each shape and along "
         "the edges of the leather pieces. INSIDE the fur draw NO outline at all (no line where the upper arm meets the shoulder, between the "
         "thigh and the shin, between the ruff and the chest, between the hips and the chest).", "",
         f"- FUR: soft ash grey {HX['long']} with loose crayon hatching and a few short fluffy tufts on the outer edges.",
         f"- PAWS: cream {HX['long_nhat']}; the near paw is a closed fist; the feet have short dark claws at the toe tips.",
         f"- VEST (on the torso, where image 2 shows brown): brown leather {HX['da']} with one small iron buckle {SAT} in its middle and one "
         f"stitch line; the fluffy cream {HX['long_nhat']} chest fur shows above its collar.",
         f"- FOREARMS: wrapped in brown leather strips {HX['da']} (a few diagonal wrap lines).",
         "- OUTLINE: dark-brown ink (#2B2118), about 7 px, wobbly, closed around each shape, just inside its edge.",
         "Draw nothing else. FLAT COLOUR, NO LIGHT, NO SHADOW. Pure white (#FFFFFF) background; no text, no labels, no frames."]
    ghi(p, t)
    print(p)
    gd += [f"- Tờ liền: gửi GPT `{Wp(p)}` → `{Wp(out)}`"]
    for ma, ds in MOI.items():
        out = os.path.join(TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_moi_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {r1}", "",
             f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 keeping ONLY the piece(s) listed below, each in the SAME POSITION, at the SAME SIZE and the SAME ANGLE as "
             "in image 1 (laid over image 1 they must coincide); REMOVE everything else: pure white there. COMPLETE each kept piece into ONE "
             "closed shape with a dark-brown ink outline all the way round, drawing the parts that are hidden in image 1 as described:", ""]
        t += [f"- {en}" for _, en, _ in ds]
        t += ["", "Same drawing style and colours as image 1: wobbly dark-brown ink outline (about 7 px), flat colours with crayon hatching, no "
              "shading, no highlights, no glow. Pure-white background, nothing else on the canvas, no labels."]
        ghi(p, t)
        print(p)
        gd += [f"- Lượt `{ma}` (" + "; ".join(vi for _, _, vi in ds) + f"): gửi GPT `{Wp(p)}` → `{Wp(out)}`"]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_mau():
    """mảnh viền riêng của dạng 2 → dạng 1 bằng ĐỔI MÀU (không gen): lông than → xám tro, xám nhạt → kem; da giữ; đồng → sắt."""
    os.makedirs(MANH, exist_ok=True)
    cu = {"long": (82, 78, 83), "long_nhat": (196, 189, 194), "dong": (212, 164, 81), "gang": (75, 79, 88)}
    moi = {"long": PAL["long"], "long_nhat": PAL["long_nhat"], "dong": (151, 153, 156), "gang": (151, 153, 156)}
    for r in ("P_weiba", "P_shouL31", "P_shouR32", "P_diaozhui3", "P_xianglian1", "P_shouR12", "W_dunpai6", "W_dunpai4", "P_yaodai"):
        A = np.asarray(Image.open(os.path.join(MANH2, r + ".png")).convert("RGBA")).astype(np.float32)
        rgb = A[..., :3]
        d = np.stack([np.linalg.norm(rgb - np.array(c, np.float32), axis=-1) for c in cu.values()], -1)
        k = d.argmin(-1)
        dmin = d.min(-1)
        out = rgb.copy()
        for i, (ten, c0) in enumerate(cu.items()):
            m = (k == i) & (dmin < 46)
            out[m] = rgb[m] - np.array(c0, np.float32) + np.array(moi[ten], np.float32)     # giữ vân sáp: dời màu
        if r == "P_diaozhui3":                                         # nút thừng vàng như đai thừng của concept A
            lum = rgb.mean(-1)
            m = (A[..., 3] > 40) & (lum > 60)
            out[m] = rgb[m] - rgb[m].mean(0) + np.array([216, 176, 106], np.float32)
        A[..., :3] = np.clip(out, 0, 255)
        Image.fromarray(A.astype(np.uint8), "RGBA").save(os.path.join(MANH, r + ".png"))
        print(" đổi màu", r)


# mốc đọc tay (px khung 1536 × 1024): bố cục rig ↔ concept A (mũi, bàn chân gần, bàn chân xa, nắm tay gần, bàn tay xa)
MOC_BC = [(985, 532), (575, 840), (880, 835), (490, 640), (945, 650)]
MOC_CC = [(985, 503), (590, 850), (860, 850), (500, 660), (945, 660)]
# dời riêng từng mảnh (px concept) cho khớp bộ phận nó bám trên rig: đầu + mũ + tai theo mũi, búa theo nắm tay, khiên theo bàn tay xa;
# "neo2": đặt tâm mảnh vào tâm mảnh cùng tên của dạng 2 (giáp vai: vai rig cao hơn vai concept ~190 px)
DOI = {"dau": (0, 29), "mu": (0, 29), "tai_gan": (0, 29), "tai_xa": (0, 29), "bua": (-5, -11), "khien": (5, -1), "vai": "neo2"}


def khop():
    """concept A px → thế giới rig dạng non (khung 0 idle, đã đổi tỉ lệ), ghi mau/khop_concept.json theo dạng của soi_giap_manh.concept_ra_the_gioi
    (gx = (P − d) / k; X = (gx − W/2) / s + cx; Y = −(gy − H/2) / s + cy)."""
    L, C = np.array(MOC_BC, float), np.array(MOC_CC, float)
    lm, cm = L.mean(0), C.mean(0)
    sc_ = float(((C - cm) * (L - lm)).sum() / ((L - lm) ** 2).sum())
    t = cm - sc_ * lm                                                  # concept = sc_ · bố cục + t
    bc = json.load(open(os.path.join(MAU, "bo_cuc.json")))
    kh = json.load(open(os.path.join(MAU, "bo_cuc_khung.json")))
    x0, _, _, y1 = bc["box"]
    s = kh["k"] * bc["scale"]                                          # px khung mỗi đơn vị rig
    out = dict(k=sc_, dx=float(t[0]), dy=float(t[1]), s=s, cx=x0 + (W / 2 - kh["ox"]) / s, cy=y1 - (H / 2 - kh["oy"]) / s, doi=DOI)
    json.dump(out, open(os.path.join(MAU, "khop_concept.json"), "w"), indent=1)
    sai = np.hypot(*((sc_ * L + t) - C).T)
    print(f"concept = bố cục × {sc_:.3f} + ({t[0]:.1f}, {t[1]:.1f}); sai mốc {np.round(sai).astype(int).tolist()} px")


Z_DAU, HA_K = 2.0, 1.45          # tờ biến thể đầu: phóng ảnh đầu 2 lần; ô há miệng cao gấp HA_K (chừa chỗ hàm há xuống)


def to_dau():
    """tờ hướng dẫn hai biến thể của ĐẦU dạng 1 (manh/dau.png): ô 1 nhắm mắt (trúng đòn, chết), ô 2 há miệng gầm (appear, tiến hóa)."""
    d = Image.open(os.path.join(MANH, "dau.png")).convert("RGBA")
    big = d.resize((round(d.width * Z_DAU), round(d.height * Z_DAU)), Image.LANCZOS)
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    ke = (W - 2 * big.width) // 3
    y0 = (H - round(big.height * HA_K)) // 2
    o = {"nham": [ke, y0, big.width, big.height], "ha": [2 * ke + big.width, y0, big.width, round(big.height * HA_K)]}
    can.alpha_composite(big, tuple(o["nham"][:2]))
    can.alpha_composite(big, tuple(o["ha"][:2]))
    from PIL import ImageDraw
    x, y, w, h = o["ha"]
    ImageDraw.Draw(can).rectangle([x - 2, y - 2, x + w + 2, y + h + 2], outline=(205, 205, 205), width=2)
    p = os.path.join(MAU, "dau_bien_the.png")
    can.convert("RGB").save(p)
    json.dump(dict(o=o, z=Z_DAU), open(p[:-4] + ".json", "w"), indent=1)
    out = os.path.join(TAI, "D_dau.png")
    pp = os.path.join(GUI, "luot_3_dau.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(p)}: a sheet of TWO copies of our wolf cub's HEAD (big amber eye, cream face, grey fur, leather chin strap, no helmet), "
         "1536x1024, white background: the left copy alone, the right copy at the top of a taller box with empty space under it.",
         f"image 2 = {Wp(CONCEPT)}: the approved cub, for the colours and the hand-drawn look.", "",
         f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as D_dau_2.png, D_dau_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: redraw the SAME sheet, keeping each head at exactly the same place, size and angle (laid over image 1 the heads must coincide), "
         "changing ONLY what is listed:",
         f"1. (left, about x = {o['nham'][0]} to {o['nham'][0] + o['nham'][2]}, y = {o['nham'][1]} to {o['nham'][1] + o['nham'][3]}) THE SAME "
         "HEAD WITH THE EYE SQUEEZED SHUT: where the big amber eye is, draw a thick dark-brown ink '>' shape (the eye pinched shut in pain), "
         "the brow pulled down, a small frown; everything else (the outline, the fur, the muzzle, the nose, the strap, the mouth) identical.",
         f"2. (right, about x = {o['ha'][0]} to {o['ha'][0] + o['ha'][2]}, y = {o['ha'][1]} to {o['ha'][1] + o['ha'][3]}) THE SAME HEAD "
         "ROARING: keep the top of the head, the eye (wide open, fierce), the nose and the strap exactly as they are; the LOWER JAW drops wide "
         "open, hinged at the back of the cheek: a big open mouth with a dark red inside #5A2228, a pink tongue #B5525A, two small white fangs "
         "on top and two on the lower jaw; the lower jaw cream with grey fur under it, reaching down into the empty part of the box. A brave "
         "little battle howl.", "",
         "Same style: wobbly dark-brown ink outline, flat colours with crayon hatching, no shading, no highlights. Pure-white background, no "
         "labels, no frame lines."]
    ghi(pp, t)
    print(pp)


def cat_dau():
    """cắt tờ biến thể đầu → manh/dau_nham.png (cùng cỡ dau.png) + manh/dau_ha.png (+ dau_ha.json: dời góc trên trái so với dau, px ảnh)."""
    import cv2
    import soi_giap_manh as SM
    p = SM._moi_nhat.__wrapped__(TAI, "D_dau") if hasattr(SM._moi_nhat, "__wrapped__") else None
    fs = sorted([f for f in os.listdir(TAI) if f.startswith("D_dau") and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(TAI, f)))
    if not fs:
        print("tờ đầu: chưa gen")
        return
    A = np.asarray(Image.open(os.path.join(TAI, fs[-1])).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    J = json.load(open(os.path.join(MAU, "dau_bien_the.json")))
    z = J["z"]
    fg = ~SM.nen(A)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    d0 = Image.open(os.path.join(MANH, "dau.png"))
    for ten, (x, y, w, h) in J["o"].items():
        pad = 16
        ids = [i for i in range(1, n) if st[i, 4] > 200 and x - pad <= st[i, 0] + st[i, 2] / 2 <= x + w + pad and y - pad <= st[i, 1] + st[i, 3] / 2 <= y + h + pad]
        m = np.isin(lab, ids)
        ys, xs = np.nonzero(m)
        bx0, by0 = min(x, xs.min()), min(y, ys.min())
        bx1, by1 = max(x + w, xs.max() + 1), max(y + h if ten == "nham" else y, ys.max() + 1)
        rgb = A[by0:by1, bx0:bx1].astype(np.uint8)
        al = cv2.GaussianBlur(m[by0:by1, bx0:bx1].astype(np.float32), (0, 0), 0.8)
        im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
        im = im.convert("RGBa").resize((max(1, round(im.width / z)), max(1, round(im.height / z))), Image.LANCZOS).convert("RGBA")
        im.save(os.path.join(MANH, f"dau_{ten}.png"))
        json.dump(dict(dx=(bx0 - x) / z, dy=(by0 - y) / z, w=im.width, h=im.height, w0=d0.width, h0=d0.height),
                  open(os.path.join(MANH, f"dau_{ten}.json"), "w"), indent=1)
        print(f"  dau_{ten}: {im.size}, dời {(bx0 - x) / z:.1f}, {(by0 - y) / z:.1f} px so với đầu thường")


def cat():
    G, SM = _sm()
    V = SM.goc_tat_ca()
    os.makedirs(MANH, exist_ok=True)
    SM.cat_lien(V)
    SM.MOI, SM.VUNG = MOI, VUNG
    SM.cat_moi()
    to_mau()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "khung":
        khung()
    elif cmd == "concept":
        prompt()
    elif cmd == "so":
        so(*(sys.argv[2:3] or ["ABC"]))
    elif cmd == "manh":
        prompt_manh()
    elif cmd == "cat":
        cat()
    elif cmd == "khop":
        khop()
    elif cmd == "dau":
        to_dau()
    elif cmd == "cat_dau":
        cat_dau()
    else:
        print(__doc__)
