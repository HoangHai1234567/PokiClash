# -*- coding: utf-8 -*-
"""DẠNG 2 của ba tướng đầu đảo Thổ (2026-11-17). Người dùng: "làm thêm dạng 2 cho 3 con đầu đi"; chọn rig (tờ ứng viên
inbox/tho5_dang2_ung_vien.png): Thạch Giáp (tatu, dạng 1 rig 3378) → monster_3528; Sa Tích (thằn lằn, 3257) → monster_3530; Tê Thiềm
(cóc tê giác, 3525) → monster_3526 (dạng tiến hoá của 3525 trong game gốc, có clip evolution_01). Thư mục làm việc inbox/<mã>_2/.
Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Concept dạng 2: GIỮ NHẬN DIỆN dạng 1 đã duyệt (ảnh 2 = L1_duyet.png: loài, mặt, màu, chất liệu, mảnh nhận diện) nhưng là con TIẾN HOÁ trên
thân mới của rig dạng 2 (ảnh 1 chỉ là mẫu dáng và bố cục chi): to hơn, chiến hơn, mảnh nhận diện lớn và nhiều hơn; không vẽ lại con gốc.

    tho5_dang2.py ca_con <mã|all>    hình cả con gốc dạng 2 khung 0 idle → inbox/<mã>_2/mau/goc_ca_con.png (+ .json)
    tho5_dang2.py slot <mã>          bảng slot của rig dạng 2
    tho5_dang2.py concept <mã|all>   file prompt → gui_gpt/<mã>_2/luot_1_concept.txt + HUONG_DAN.md
    tho5_dang2.py so_goc <mã> [AB]   chồng viền hình bóng con gốc lên concept, in IoU → inbox/<mã>_2/mau/_so_goc.png
    tho5_dang2.py non_ca_con / non_slot / non_concept / non_so_goc <mã>   DẠNG NHỎ (bảng NON, thư mục inbox/<mã>_non/)
    tho5_dang2.py sua <mã>           lượt sửa (bảng SUA): vẽ lại một concept, chỉ đổi phần được dặn → gui_gpt/<mã>_2/<luot>
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5 as T  # noqa: E402

CON2 = {
    "cong_da": ("monster_3528", "Thạch Giáp"),
    "than_lan_cat": ("monster_3530", "Sa Tích"),
    "thu_da": ("monster_3526", "Tê Thiềm"),
}


def dat2(code):
    mon = CON2[code][0]
    H = T.H
    base = os.path.join(HERE, "inbox", f"{code}_2")
    H.CODE, H.MON, H.BASE = code, mon, base
    H.MAU, H.TAI = os.path.join(base, "mau"), os.path.join(base, "tai_ve")
    H.NHOM = []
    H._C.clear()
    H.luoi = T.luoi_sua
    return H


def _voi_dat2(fn, code, *a):
    cu = T.dat
    T.dat = dat2
    try:
        return fn(code, *a)
    finally:
        T.dat = cu


# ---------------------------------------------------------------- mô tả concept dạng 2
GOC_EN = {
    "cong_da": ("the original creature of the skeleton (a game reference), 1536x1024, white background: a big pile of large crystal "
                "blocks carried on FOUR straight crystal legs, a small body and face peeking out under the front of the pile, a curled tail "
                "under the left side"),
    "than_lan_cat": ("the original creature of the skeleton (a game reference), 1536x1024, white background: a big spiky lizard sitting "
                     "upright and squat on its haunches, facing right, a big head with a crest of long spikes, both front arms hanging in "
                     "front of the round belly, rows of big leaf-shaped spikes down its sides and arms, a short tail at the left"),
    "thu_da": ("the original creature of the skeleton (a game reference), 1536x1024, white background: a heavy rock beast standing on four "
               "short legs, facing right, a big head with a huge lower jaw, its back, shoulders and tail covered with large jagged spikes "
               "pointing up and back"),
}
GOC_VI = {
    "cong_da": "Con gốc 3528 khung 0 idle: đống khối pha lê to trên bốn chân pha lê, thân và mặt nhỏ ló dưới mép trước, đuôi xoắn bên trái",
    "than_lan_cat": "Con gốc 3530 khung 0 idle: thằn lằn gai ngồi xổm thẳng lưng, đầu to mào gai dài, hai tay trước bụng tròn, hàng gai lá dọc thân",
    "thu_da": "Con gốc 3526 khung 0 idle: thú đá bốn chân đứng, đầu to hàm dưới lớn, lưng vai đuôi phủ gai lớn chĩa lên ra sau",
}
DANG1_EN = ("our APPROVED FIRST FORM of this hero (1536x1024, white background): the new design must be the SAME CHARACTER grown up: keep "
            "its species, its face, its colours, its materials and its signature pieces described below. Do NOT copy its pose or its body "
            "plan: those come from image 1.")

D2 = {}
D2["cong_da"] = dict(
    concept="the GROWN-UP, battle-hardened form of our armadillo hero (image 2): a big ARMADILLO that has grown a MOUNTAIN of rock on its back",
    plan=("BODY PLAN (from image 1): three-quarter view turned a little to the RIGHT; a huge load on the back that fills most of the picture "
          "(wider and taller than the body), the creature's head and face peeking out under the FRONT (right) edge of the load, FOUR straight "
          "pillar legs standing under it (two in front, two behind), a curled tail hanging under the left side, a tiny two-leaf sprout "
          "on the very top of the load."),
    design=[
        "THE ARMADILLO (from image 2, grown up): the same sandy ochre #D2A066 hide, cream #F0DDB4 face and belly, the same short pointed "
        "snout with the round dark-brown nose, the small rounded ears, the determined eyes (white, dark-brown pupils, one small white dot "
        "each) under thick angry brow strokes; older and tougher: a firmer frown. Only the head, the front of the "
        "body and the tail show under the load; the tail is the armadillo tail with dark #9A6B3C rings, curled where the tail of image 1 is.",
        "THE LOAD: the armadillo STONE SHELL of image 2 grown into a big rocky MOUND: several large overlapping curved stone plates "
        "#BFB29B with darker #998D77 rims (armadillo-shell bands, not crystal blocks), with THREE big broken-open geode holes from which "
        "big flat AMBER crystal clusters #F2B33D stand up (the biggest cluster on top, the size of the head).",
        "THE LEGS: the four legs of image 1 become four STONE PILLAR legs (about as long and thick as the legs of image 1, stacked rounded rock, grey-beige #BFB29B with one darker "
        "band #998D77 near the bottom, three tiny cream claws at the foot), each joined to the underside of the shell.",
        "THE SPROUT: the tiny two-leaf sprout on top becomes a small amber crystal shard #F2B33D.",
        "NO pale lilac crystal blocks, no purple body, no crystal legs.",
    ],
    kiem="cùng dáng, cùng chỗ bốn chân, đuôi, mặt như ảnh 1; mặt, màu tatu như ảnh 2 (vàng đất, kem, mũi nâu); mai đá nhiều tấm + 3 cụm hổ phách",
)
D2["than_lan_cat"] = dict(
    concept="the GROWN-UP, battle-hardened form of our desert lizard hero (image 2): a big ARMOURED LIZARD KNIGHT wearing a mantle of clay plates",
    plan=("BODY PLAN (from image 1): the lizard sits upright and squat on its haunches, three-quarter view turned to the RIGHT; a big head at "
          "the upper right with a tall crest of long pieces rising behind it, the two front arms hanging in front of a round belly, the "
          "thick back legs folded at the bottom, rows of big pieces down the sides of the body and on the arms, a short tail at the left."),
    design=[
        "THE LIZARD (from image 2, grown up): the same short blunt wedge-shaped head with the heavy ROCK-PLATED BROW, the fierce yellow eye "
        "#F2C640 (black slit pupil, one small white dot; the far eye just peeking), the jaw with two small fangs at the corner, now a "
        "little bigger; the same dusty khaki-ochre #B9A06A skin with a cream #EEDDB0 throat and belly; blunt dark-brown claws.",
        "THE CREST: instead of the spikes of image 1, a tall raised HOOD of overlapping terracotta CLAY PLATES #B5603A with cream rims "
        "#EAD3A6 rising behind the head (the signature mantle of image 2, bigger and taller, jagged top edge).",
        "THE SIDE AND ARM PIECES: every big piece on the sides, shoulders and arms of image 1 becomes a flat terracotta CLAY PLATE #B5603A "
        "with a cream rim #EAD3A6 (overlapping like armour scales, rounded or blunt-pointed tips), so the whole lizard wears an armour of "
        "clay plates; the tail ringed with terracotta plates.",
        "NO green, no yellow spikes, no leaf shapes.",
    ],
    kiem="cùng dáng ngồi, cùng chỗ đầu, tay, chân, đuôi như ảnh 1; đầu nêm mày giáp, mắt vàng, da khaki như ảnh 2; mũ trùm + giáp phiến đất nung",
)
D2["thu_da"] = dict(
    concept="the GROWN-UP, battle-hardened form of our toad-rhino hero (image 2): a huge TOAD-RHINO bristling with amber crystals",
    plan=("BODY PLAN (from image 1): a heavy four-legged beast standing square, three-quarter view turned to the RIGHT, a big head at the "
          "right with a huge lower jaw, big pieces covering the back, the shoulders and the tail and pointing up and back, four short thick "
          "legs."),
    design=[
        "THE TOAD-RHINO (from image 2, grown up): the same wide toad-like head with ONE thick blunt STONE HORN on the snout (cream #EADCBD, "
        "now longer and sharper), the wide mouth with blunt teeth, the small angry amber eyes #F5C04A (dark pupil, one small white dot) "
        "under a heavy brow; the same warm terracotta #B8663E hide with cream #EADCBD jaw, chest and belly, a few flat darker #8A4A2C "
        "patches; thick legs with short cream claws.",
        "THE CRYSTALS: every big spike of image 1 becomes a cluster of AMBER CRYSTALS #F0AA32 (straight prisms with sharp points, one lighter "
        "flat facet #FFD27A each): big clusters over the shoulders and along the back, smaller ones on the tail and the elbows, the "
        "signature crystals of image 2 grown big and many.",
        "THE BELT: the band round the waist of image 1 becomes a plain dark hide belt #5A3424 with three flat stone plates.",
        "NO flame shapes, no lava, no orange fire spikes, no glow.",
    ],
    kiem="cùng dáng, cùng chỗ đầu, hàm, chân, đuôi như ảnh 1; sừng mõm, da đất nung, mắt hổ phách như ảnh 2; gai lửa đổi thành cụm pha lê hổ phách",
)


def task_d2(concept):
    return (f"TASK: DESIGN THE EVOLVED FORM of our hero: {concept}. Image 1 is ONLY a guide for the POSE and the BODY PLAN (the new form will "
            "be animated with the skeleton of image 1): keep its pose, its facing, its size and place on the canvas, and roughly where the "
            "head, the body, each limb, the tail and the big pieces are and which way they point; the body and the legs keep about the same "
            "size and thickness. Image 2 gives the CHARACTER: the species, the face, the colours, the materials and the signature pieces "
            "of our first form, grown bigger, older and more battle-ready. The result must read at a glance as the SAME hero as image 2, "
            "evolved, and must NOT look like a recolour or a trace of image 1. Every limb, the tail and the head stay joined to the body "
            "(no white gaps between a limb and the body).")


MOOD = ("MOOD: a cute but BATTLE-READY pet creature in the style of a creature-collecting game (chunky, big eyes, few details), clearly "
        "stronger and more imposing than its first form: a determined, fierce face, a ready-to-fight stance; not scary, not a smiling "
        "mascot.")


def prompt(code):
    from tho5_huong import REF, CON as HG
    G = dat2(code)
    mon, ten = CON2[code]
    c = D2[code]
    gui = os.path.join(HERE, "gui_gpt", f"{code}_2")
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    d1 = os.path.join(HERE, "inbox", f"{code}_1", "tai_ve", "L1_duyet.png")
    R = [(mau, GOC_EN[code] + ". It is painted in a smooth digital cel style. Use it ONLY for the pose and the body plan; do NOT copy its "
          "shapes, its face, the outlines of its pieces, its details or its colours.", GOC_VI[code] + " (chỉ lấy DÁNG và chỗ các chi)"),
         (d1, DANG1_EN, f"Dạng 1 {ten} đã duyệt (L1_duyet.png): giữ loài, mặt, màu, chất liệu, mảnh nhận diện")]
    R += [REF[k] for k in HG[code]["refs"]]
    out = os.path.join(G.TAI, "L1_A.png")
    p = os.path.join(gui, "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {T.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {T.Wp(out)}",
          "If a file with that name already exists, save as L1_A_2.png, L1_A_3.png ... in the same folder. Do not edit, move or delete any "
          "other file.", "", task_d2(c["concept"]), "", c["plan"], "", "DESIGN:"] + [f"- {d}" for d in c["design"]]
    t += ["", T.style().replace("(images 2 and 3)", f"(images 2 to {len(R)})"), "", MOOD, "",
          "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
          "place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no speed lines, "
          "no labels, no frame."]
    T.ghi(p, t)
    hd = [f"# Gói GPT: {ten} dạng 2 (`{code}_2`), rig `{mon}`", "",
          f"Con gốc của rig: `{mon}` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept dạng 2 (2026-11-17)", "",
          "Người dùng: \"làm thêm dạng 2 cho 3 con đầu\", chọn rig này. Concept giữ nhận diện dạng 1 đã duyệt (ảnh 2), đặt lên thân và dáng của "
          "rig dạng 2 (ảnh 1), to hơn, chiến hơn.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{T.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += ["", f"- Chỉ gửi GPT đường dẫn `{T.Wp(p)}`; ảnh lưu vào `{T.Wp(out)}` (trùng tên thì `_2`, `_3`…). Bản được chọn chép thành "
           "`L1_duyet.png` cùng thư mục.", "",
           f"Kiểm: {c['kiem']}; mọi chi dính thân; mắt có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng; nền "
           "trắng tinh.", "",
           "Câu sửa nhanh: \"it must be the same hero as image 2: same face and colours\"; \"keep the pose and the legs of image 1\"; "
           "\"remove the shading / highlights / glow, flat colour only\"; \"every limb joined to the body, no white gap\"."]
    T.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)
    print(p)
    return p, out


# ---------------------------------------------------------------- lượt sửa: vẽ lại một concept, chỉ đổi phần được dặn
SUA = {
    # người dùng 2026-11-17 (L1_A): "con đầu tiên chân dài quá nhìn hơi dị, sửa lại"
    "cong_da": dict(
        nguon="L1_A.png", ra="L1_B.png", luot="luot_2_sua_chan.txt",
        vi="Thạch Giáp dạng 2 lượt 1 (L1_A): đúng ý trừ bốn chân trụ đá quá dài",
        doi=[
            "THE LEGS ARE TOO LONG: make them SHORT, THICK and STUMPY. The four legs become short sturdy ARMADILLO legs like the legs of "
            "image 3 but thicker (the same sandy ochre #D2A066 hide as the face, three small cream claws on each foot), not stone pillars.",
            "To hide the length, the bottom edge of the stone mound now hangs down LOW all round like a skirt of big curved stone plates "
            "(the same plates and colours as now), down to about the middle of the old legs, so only the lower half of each leg shows below "
            "it. The creature reads as a heavy, low, wide armadillo carrying a mountain, NOT a creature on stilts.",
            "The FEET stay exactly where they are now (same ground line, same four places, two in front and two behind), and the face, the "
            "head, the tail and the top of the mound stay where they are now.",
            "Everything else stays EXACTLY as in image 1: the face, the colours, the shell plates, the three amber crystal clusters, the "
            "small amber shard on top, the curled ringed tail.",
        ],
        kiem="chân ngắn mập màu da tatu, mép mai buông thấp che nửa trên chân; bàn chân, mặt, đuôi, đỉnh mai giữ chỗ cũ; phần còn lại y như L1_A",
    ),
}


def prompt_sua(code):
    from tho5_huong import REF, CON as HG
    G = dat2(code)
    s = SUA[code]
    mon, ten = CON2[code]
    gui = os.path.join(HERE, "gui_gpt", f"{code}_2")
    nguon = os.path.join(G.TAI, s["nguon"])
    R = [(nguon, "our concept of this hero that we want to FIX (1536x1024, white background): redraw THIS image, keep everything that is not "
          "listed under CHANGE exactly the same (design, colours, line, place and size on the canvas).", s["vi"]),
         (os.path.join(G.MAU, "goc_ca_con.png"), GOC_EN[code] + ". Use it ONLY to see where the feet, the face and the tail must stay; do "
          "NOT copy its shapes, its painting style or its colours.", GOC_VI[code] + " (chỉ để giữ chỗ bàn chân, mặt, đuôi)"),
         (os.path.join(HERE, "inbox", f"{code}_1", "tai_ve", "L1_duyet.png"), "our approved FIRST FORM of this hero: look at its short, stubby "
          "legs and feet.", f"Dạng 1 {ten} đã duyệt: xem chân ngắn mập")]
    R += [REF[k] for k in HG[code]["refs"][:1]]
    out = os.path.join(G.TAI, s["ra"])
    p = os.path.join(gui, s["luot"])
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {T.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {T.Wp(out)}",
          f"If a file with that name already exists, save as {s['ra'][:-4]}_2.png, {s['ra'][:-4]}_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: REDRAW image 1 with only the change below.", "", "CHANGE:"] + [f"- {d}" for d in s["doi"]]
    t += ["", T.style().replace("(images 2 and 3)", "(images 1, 3 and 4)").replace("Image 1 is painted", "Image 2 is painted"), "", MOOD, "",
          "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same place "
          "and size as in image 1. No sparkles, no glints, no dust, no glow, no aura, no smoke, no speed lines, no labels, no frame."]
    T.ghi(p, t)
    hd = open(os.path.join(gui, "HUONG_DAN.md"), encoding="utf-8").read().rstrip("\n").split("\n")
    if s["luot"] not in "\n".join(hd):
        hd += ["", f"## Lượt sửa: {s['vi']}", "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        hd += [f"| {i} | `{T.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        hd += ["", f"- Chỉ gửi GPT đường dẫn `{T.Wp(p)}`; ảnh lưu vào `{T.Wp(out)}`.", f"- Kiểm: {s['kiem']}."]
        T.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)
    print(p)
    return p


# ---------------------------------------------------------------- DẠNG NHỎ (dạng 1 trước tiến hoá) cho tướng mà bản hiện có là dạng cuối
# Người dùng 2026-11-17: "làm thử dạng 1 của tướng thứ 4 đảo thổ" (gen qua Magnific, trần < 100 credit / ảnh); chọn rig monster_3529 (thằn
# lằn rồng bốn chân, dáng chồm tới gần 3424). Bản hiện có (rig rong_cat_1 trên 3424) thành dạng 2. Thư mục inbox/<mã>_non/.
NON = {
    "rong_cat": dict(
        mon="monster_3529", ten="Sa Long",
        goc_en=("the original creature of the skeleton (a game reference), 1536x1024, white background: a lean young four-legged spiky "
                "lizard-drake in mid-stride, facing right, its head raised at the right with a crest of long spikes, spikes along its back, "
                "a long spiky tail stretched out to the left"),
        goc_vi="Con gốc 3529 khung 0 idle: thằn lằn rồng non bốn chân đang bước, đầu ngẩng bên phải mào gai dài, gai dọc lưng, đuôi dài có gai bên trái",
        concept="the YOUNG FIRST FORM of our sandstone drake hero (image 2): a small, lean, quick young drake that will one day grow into image 2",
        plan=("BODY PLAN (from image 1): a lean four-legged young drake in three-quarter view turned to the RIGHT, walking in mid-stride, its "
              "head raised at the right, a row of pieces along the back, four slim legs (the near ones in front), a long tail stretched out "
              "to the left with pieces along it."),
        design=[
            "THE DRAKE (from image 2, but YOUNG): the same species and colours: dusty brown hide #8E6E52 (darker #6E533D on the faces turned "
            "away), cream belly and throat #E8D7B0, a few flat ochre #C4964F stripes on the tail, dark brown talons #3E2F24; a narrow "
            "determined eye (yellow iris #F7C43A, black slit pupil, one small white dot); a SMALL stubby AMBER crystal nose horn #F0A62E "
            "(the start of the big horn of image 2).",
            "THE HORNS: two SHORT backswept stone horns #E3CC98 on the back of the head (young versions of the long horns of image 2) instead "
            "of the long spikes of image 1.",
            "THE BACK AND TAIL PIECES: every spike of image 1 along the back and the tail becomes a small rounded SANDSTONE PLATE #E3CC98 with "
            "one flat ochre band #BF8443 (young, smaller versions of the armour plates of image 2), fewer and smaller than in image 2.",
            "Younger and smaller-looking than image 2: a bigger head for its body, slimmer limbs, smaller armour; still fierce, ready to fight.",
            "NO green, no yellow lightning spikes.",
        ],
        kiem="cùng dáng bước, cùng chỗ đầu, chân, đuôi như ảnh 1; màu nâu bụi, mắt vàng, sừng mũi hổ phách nhỏ, hai sừng đá ngắn, phiến sa thạch nhỏ",
    ),
}


def dat_non(code):
    c = NON[code]
    H = T.H
    base = os.path.join(HERE, "inbox", f"{code}_non")
    H.CODE, H.MON, H.BASE = code, c["mon"], base
    H.MAU, H.TAI = os.path.join(base, "mau"), os.path.join(base, "tai_ve")
    H.NHOM = []
    H._C.clear()
    H.luoi = T.luoi_sua
    return H


def task_non(concept):
    return (f"TASK: DESIGN THE YOUNG FIRST FORM of our hero: {concept}. Image 1 is ONLY a guide for the POSE and the BODY PLAN (the new form "
            "will be animated with the skeleton of image 1): keep its pose, its facing, its size and place on the canvas, and roughly where "
            "the head, the body, each limb, the tail and the pieces are and which way they point; the body and the legs keep about the same "
            "size and thickness. Image 2 is our FINAL form of this hero: the young form must clearly be the SAME species with the same face, "
            "colours and materials, smaller and less armoured. The result must NOT look like a recolour or a trace of image 1. Every limb, "
            "the tail and the head stay joined to the body (no white gaps between a limb and the body).")


def prompt_non(code):
    from tho5_huong import REF, CON as HG
    c = NON[code]
    G = dat_non(code)
    gui = os.path.join(HERE, "gui_gpt", f"{code}_non")
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    d2 = os.path.join(HERE, "inbox", f"{code}_1", "tai_ve", "L1_duyet.png")
    R = [(mau, c["goc_en"] + ". It is painted in a smooth digital cel style. Use it ONLY for the pose and the body plan; do NOT copy its "
          "shapes, its face, the outlines of its pieces, its details or its colours.", c["goc_vi"] + " (chỉ lấy DÁNG và chỗ các chi)"),
         (d2, "our APPROVED FINAL FORM of this hero (1536x1024, white background): the young form must be the SAME CHARACTER, younger: keep "
          "its species, its face, its colours and its materials, with smaller horns and armour. Do NOT copy its pose or its body plan: those "
          "come from image 1.", f"{c['ten']} dạng cuối đã duyệt (L1_duyet.png): giữ loài, mặt, màu, chất liệu")]
    R += [REF[k] for k in HG[code]["refs"]]
    out = os.path.join(G.TAI, "L1_A.png")
    p = os.path.join(gui, "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {T.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {T.Wp(out)}",
          "If a file with that name already exists, save as L1_A_2.png, L1_A_3.png ... in the same folder. Do not edit, move or delete any "
          "other file.", "", task_non(c["concept"]), "", c["plan"], "", "DESIGN:"] + [f"- {d}" for d in c["design"]]
    t += ["", T.style().replace("(images 2 and 3)", f"(images 2 to {len(R)})"), "",
          "MOOD: a cute but BATTLE-READY young pet creature in the style of a creature-collecting game (chunky, big eyes, few details): a "
          "determined, fierce little face, a ready-to-fight stance; not scary, not a smiling mascot.", "",
          "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
          "place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no speed lines, "
          "no labels, no frame."]
    T.ghi(p, t)
    hd = [f"# Gói GPT: {c['ten']} DẠNG 1 (dạng nhỏ, `{code}_non`), rig `{c['mon']}`", "",
          f"Con gốc của rig: `{c['mon']}` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept dạng nhỏ (2026-11-17)", "",
          "Người dùng: \"làm thử dạng 1 của tướng thứ 4 đảo thổ\" (gen qua Magnific, trần < 100 credit / ảnh), chọn rig này. Bản hiện có "
          f"(`{code}_1`) thành dạng 2.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{T.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += ["", f"- Gen: `py -3 -I ArtGen/Spine/gen_magnific.py {T.Wp(p)}` (95 credit, 1k high) hoặc gửi GPT đường dẫn đó; ảnh lưu vào "
           f"`{T.Wp(out)}`. Bản được chọn chép thành `L1_duyet.png`.", "", f"Kiểm: {c['kiem']}; mọi chi dính thân; mắt có chấm trắng; nét bút "
           "mực rung, vân sáp, tô phẳng, không bóng; nền trắng tinh."]
    T.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)
    print(p)
    return p


def _voi_dat_non(fn, code, *a):
    cu = T.dat
    T.dat = dat_non
    try:
        return fn(code, *a)
    finally:
        T.dat = cu


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd.startswith("non_"):                                  # non_ca_con / non_slot / non_concept / non_so_goc <mã>
        code = sys.argv[2]
        {"non_ca_con": lambda: _voi_dat_non(T.ca_con, code), "non_slot": lambda: _voi_dat_non(T.slot, code),
         "non_concept": lambda: prompt_non(code), "non_so_goc": lambda: _voi_dat_non(T.so_goc, code, sys.argv[3] if len(sys.argv) > 3 else "A")}[cmd]()
        sys.exit(0)
    arg = sys.argv[2] if len(sys.argv) > 2 else "all"
    codes = list(CON2) if arg == "all" else [arg]
    if cmd == "ca_con":
        for c in codes:
            _voi_dat2(T.ca_con, c)
    elif cmd == "slot":
        for c in codes:
            print("==", c, CON2[c][0])
            _voi_dat2(T.slot, c)
    elif cmd == "concept":
        for c in codes:
            prompt(c)
    elif cmd == "so_goc":
        for c in codes:
            _voi_dat2(T.so_goc, c, sys.argv[3] if len(sys.argv) > 3 else "A")
    elif cmd == "sua":
        for c in codes:
            prompt_sua(c)
    else:
        print(__doc__)
