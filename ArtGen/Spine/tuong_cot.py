# -*- coding: utf-8 -*-
"""Tượng đá cổ đại cầm cột đá (mã làm việc tuong_cot): tướng thứ 6 đảo Mộc (ải 30), người dùng dặn 2026-11-17. Con gốc của rig:
monster_3608 (game tham khảo, kho SwordxStaff): golem đá đầu thấp, tay gần nắm đấm khối đá, tay xa nắm một cột đá vác chéo sau lưng,
lõi cầu xanh giữa ngực, không chân (cụm đá lơ lửng dưới ngực). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng
nội bộ, không đăng công khai.

Lời dặn: "concept tượng đá cổ đại cầm 1 cột đá lớn"; "đừng làm quá nhiều chi tiết, vừa phải thôi"; gen bằng Magnific, đưa concept xem
trước; animation Claude tự làm trên rig gốc (độc đáo, lạ, epic) sau khi concept được chọn.

    tuong_cot.py ca_con        hình cả con gốc khung 0 idle → inbox/tuong_cot_1/mau/goc_ca_con.png
    tuong_cot.py concept       file prompt từng hướng → gui_gpt/tuong_cot_1/luot_1_concept_<k>.txt + HUONG_DAN.md
    tuong_cot.py so_goc        chồng viền con gốc lên từng concept, in IoU → inbox/tuong_cot_1/mau/_so_goc.png
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
from tho5_huong import REF  # noqa: E402

CODE = "tuong_cot"
tho5.CON[CODE] = ("monster_3608", 6, 30)
_I = os.path.join(HERE, "inbox")
REF = dict(REF)
REF["quy_nui"] = (
    os.path.join(_I, "quy_nui_1", "tai_ve", "L1_duyet.png"),
    "an approved hero of our game (a mighty rock ape titan), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen line, "
    "its crayon hatching, its flat colouring of big rock masses, and how a fierce, determined stone face is drawn (heavy brow, small "
    "eyes with one white dot, firm mouth). Do NOT copy its design, its four arms or its colours.",
    "Vượn núi đá (tướng 5 đảo Thổ) đã duyệt: lấy nét bút, vân sáp, cách tô khối đá to và một gương mặt đá dữ, quả quyết")

GOC_EN = ("the creature whose skeleton we reuse, idle pose, 1536x1024, white background. It is painted in a smooth digital cel style. Use "
          "it ONLY for the pose and the body plan; do NOT copy its shapes, the outlines of its pieces, its details or its colours")
GOC_VI = "Con gốc monster_3608, khung 0 idle, nền trắng 1536×1024: chỉ lấy DÁNG và chỗ các chi, cột đá vác chéo"

CONCEPT = "an ANCIENT STONE STATUE come to life, a forest-temple guardian, holding a BIG STONE PILLAR as its weapon"

PLAN = (
    "BODY PLAN (from image 1, keep it): a heavy hunched stone giant turned to the RIGHT (it attacks towards the right). "
    "(1) The HEAD sits LOW in the middle of the picture, sunk between the shoulders like a gorilla, just under the pillar, its face "
    "looking to the right. (2) The NEAR ARM is on the LEFT: a big shoulder piece at the upper left, the arm hanging down, a big fist made "
    "of separate blocky stone fingers at the lower left. (3) The FAR ARM reaches to the RIGHT behind the body; its blocky fingers grip "
    "the pillar near the pillar's lower-right end. (4) The PILLAR is a long thick column lying DIAGONALLY across the back: its top end "
    "sticks up at the top middle of the picture (above the head), its lower end is at the right. Same length, thickness and angle as "
    "in image 1. (5) The CORE is a round heart-stone in the middle of the chest, partly covered by chest plates. (6) NO LEGS: under the "
    "chest a loose cluster of floating rock chunks, like in image 1. (7) A few small shards between the near shoulder and the near arm. "
    "The separate finger blocks and the floating rock chunks stay separate like in image 1 (a statue held together by forest magic); "
    "everything else stays joined to the body.")

MOOD = ("MOOD: an ancient guardian statue awakened, heavy, mighty and determined (a stern, fierce frown); not cute-silly, not a mascot, "
        "not scary; mature proportions (not chibi, the head stays small for the body as in image 1).")

DETAIL = ("MODERATE DETAIL (the user asked: not too many details): big simple stone masses, each a flat colour; at most one or two inner "
          "lines per piece; only the details listed under DESIGN.")

HUONG = {
    "A": ("thần giữ đền đá hoa cương, mặt nạ đá nghiêm, lõi ngọc bích",
          "đầu là mũ đá vuông có vành, mặt khắc nghiêm: mày thẳng nặng, hai hốc mắt ngọc lục, miệng một nét thẳng, cằm vuông; vai gần là "
          "khối đá bậc vuông như đầu cột đền; lõi tròn ngọc bích trong khung đá vuông; cột đền tròn có rãnh dọc, đầu và chân cột khối "
          "vuông, hai vòng dây leo; đá xám hoa cương, vài mảng rêu",
          ["HEAD: a carved stone GUARDIAN HEAD with a flat, squarish HELMET (a straight brim over the forehead, flat top). The face is a "
           "stern carved mask turned to the right: a heavy straight brow, TWO deep-set eyes in flat jade green #4FC46E (dark pupil, one "
           "small white dot each), a short straight mouth line, a square chin. No horns, no crest, no pointed plate.",
           "NEAR SHOULDER: a heavy SQUARE stone block with two stepped edges (like the top block of a temple column), not round, no notch "
           "or hole. FAR SHOULDER: a smaller plain square slab.",
           "CORE: a round JADE stone #4DBA6A set in a square stone frame on the chest, one carved leaf line on it; no glow.",
           "SHARDS: a few small flat jade shards #6FD38A.",
           "ARMS AND FISTS: blocky granite, the fingers darker #63665F.",
           "FLOATING ROCKS under the chest: dark granite #5C5F5A, simple angular chunks.",
           "PILLAR: a straight ROUND TEMPLE COLUMN with 4–5 even vertical grooves, a plain square block on its top end and a square base "
           "block on its lower end; two small moss patches #5E9A4A; two green vine bands #4F8A3C wrapped round it near the lower end.",
           "COLOURS: granite grey #A3A39A on the faces turned to the viewer, #7D7F78 on the faces turned away; a few small moss patches "
           "#5E9A4A on the shoulders and head (no more than five patches on the whole body).",
           "NO blue, no round keyhole shoulder, no pointed head plate, no spirals, no sprout, no cracks all over, no runes."]),
    "B": ("tượng vua cổ rễ cây quấn, vương miện tầng, lõi pha lê lá",
          "đầu là mặt vua đá cổ đội vương miện nhọn ba tầng (kiểu tháp đền), mắt xanh lá hẹp dưới mày nặng, mũi bè, môi dày mím; rễ cây "
          "nâu to bò qua vai gần, xuống cánh tay và quấn cột; vai gần là phiến tròn có gờ; lõi cụm ba pha lê lá trong vòng rễ; đá xám "
          "ngả lục; cột đá vuông có một đai khắc gần mỗi đầu, đầu trên hơi vỡ",
          ["HEAD: a carved ANCIENT KING face turned to the right, wearing a tall POINTED CROWN of THREE simple stacked tiers (like a small "
           "temple tower). The face: TWO narrow fierce eyes in flat leaf green #8BD448 (dark pupil, one small white dot each) under a heavy "
           "brow, a wide flat nose, thick lips pressed in a firm line, a broad jaw.",
           "ROOTS: THREE thick brown TREE ROOTS #7A5534 (with a few small leaves #6DBE45) grow over the near shoulder and down the near "
           "arm, and two roots wrap round the pillar. No other plants.",
           "NEAR SHOULDER: a rounded dome-like stone slab with one rim line, a root crawling over it. FAR SHOULDER: a smaller rounded slab.",
           "CORE: a cluster of THREE flat leaf-green crystals #7CCB4E held in a ring of roots on the chest; no glow.",
           "SHARDS: a few small leaf-green crystal shards.",
           "ARMS AND FISTS: weathered stone, the fingers darker #555C50.",
           "FLOATING ROCKS under the chest: dark stone #555C50.",
           "PILLAR: an old SQUARE stone pillar (square cross-section) with ONE simple carved band near each end, its top end slightly "
           "broken; the two roots wrap it near the lower end.",
           "COLOURS: weathered grey-green stone #9DA593 on the faces turned to the viewer, #77806E on the faces turned away.",
           "NO blue, no round keyhole shoulder, no pointed head plate, no vines, no spirals, no sprout, no moss beards, no runes."]),
    "C": ("tượng đầu dài đá bazan (kiểu tượng đảo), mắt khe xanh, cột đá thô",
          "đầu dài nguyên khối: gờ mày nhô, hai khe mắt xanh lá, mũi dài thẳng, miệng mỏng mím, hàm dài, đỉnh bằng; vai gần là tảng đá tròn "
          "trơn; lõi tim pha lê xanh lá; đá bazan xám lam sẫm, vài mảng địa y vàng lục; cột đá thô tròn hơi thuôn như cột đá dựng, hai vòng "
          "dây leo",
          ["HEAD: a LONG MONOLITH HEAD (like the ancient giant stone heads on an island) turned to the right: a long face, a heavy "
           "overhanging brow ridge, TWO narrow eye slits in flat leaf green #9BE05A (one small white dot each), a long straight nose, a "
           "tight thin mouth, a long heavy jaw, a flat top. No helmet, no crown, no pointed plate.",
           "NEAR SHOULDER: a thick round plain BOULDER, one lichen patch. FAR SHOULDER: a smaller plain boulder.",
           "CORE: a round leaf-green crystal heart #7DD35A in the chest stone, plain; no glow.",
           "SHARDS: a few small leaf-green crystal shards.",
           "ARMS AND FISTS: rounded basalt blocks, the fingers darker #3C424B.",
           "FLOATING ROCKS under the chest: dark basalt #3C424B.",
           "PILLAR: a ROUGH-HEWN round stone column of the same basalt, slightly tapered, plain, bound with two green vine bands #4F8A3C "
           "near its lower end.",
           "COLOURS: dark blue-grey basalt #6C7480 on the faces turned to the viewer, #4F5661 on the faces turned away; a few small "
           "yellow-green lichen patches #A9C24A (no more than five on the whole body).",
           "NO blue glow, no round keyhole shoulder, no pointed head plate, no spirals, no sprout, no runes, no cracks all over."]),
}


def task():
    from tho5_huong2 import task2
    return task2(CONCEPT)


def concept():
    G = tho5.dat(CODE)
    gui = os.path.join(HERE, "gui_gpt", f"{CODE}_1")
    R = [(os.path.join(G.MAU, "goc_ca_con.png"), GOC_EN, GOC_VI), REF["golem"], REF["quy_nui"]]
    hd = ["# Gói gen: tượng đá cổ đại cầm cột đá (`tuong_cot`), tướng 6 đảo Mộc (ải 30)", "",
          "Con gốc của rig: `monster_3608` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept, ba hướng (2026-11-17, gen bằng Magnific GPT 2.6)", "",
          "Người dùng: \"concept tượng đá cổ đại cầm 1 cột đá lớn\", \"đừng làm quá nhiều chi tiết, vừa phải thôi\". Ảnh 1 chỉ là mẫu dáng "
          "và chỗ các chi (dùng chung bộ xương); đầu, mặt, vai, lõi, cột là thiết kế mới; ba hướng do Claude đề xuất.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{tho5.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(gui, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {tho5.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {tho5.Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", task(), "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in doi] + ["", DETAIL, "", tho5.style(), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the "
              "same place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no "
              "speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: cùng dáng, cùng hướng (quay phải), cột vác chéo đúng chỗ ảnh 1, nắm tay xa nắm đầu dưới cột; đầu, vai, lõi, cột đổi hẳn "
           "dáng; mắt có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng; chi tiết vừa phải; nền trắng tinh.",
           "", "Câu sửa nhanh: \"too many details: simplify\"; \"remove the shading / highlights / glow, flat colour only\"; \"keep the "
           "pillar at the same place and angle as in image 1\"."]
    tho5.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        tho5.ca_con(CODE)
    elif cmd == "concept":
        concept()
    elif cmd == "so_goc":
        tho5.so_goc(CODE, "ABC")
    else:
        print(__doc__)
