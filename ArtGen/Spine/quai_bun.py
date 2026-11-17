# -*- coding: utf-8 -*-
"""Quái bùn / quái đất sét (mã làm việc quai_bun): tướng thứ 8 đảo Thổ (ải 50, suất hiện là ho_kim_cuong), người dùng dặn 2026-11-17.
Con gốc của rig: monster_3668 (game tham khảo, kho SwordxStaff, người dùng chỉ): quái chất nhầy xám lục gù như khỉ đột, đế nhầy loang
dưới đất, hai nắm đấm khối, đầu góc cạnh nhỏ, cái miệng to lòng xanh sáng từ đầu xuống ngực, chùm xúc tu đầu hồng trên lưng và đầu;
tay xa co giãn được (chạy trên path `shou`), đầu biến thành hàm khổng lồ (skill_04), thân xẻ đôi (deform_01). Xương, lưới, chuyển động
gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Lời dặn: "concept quái vật bùn lầy hoặc quái vật đất sét như con gốc"; "các animation bạn tự sáng tạo xoay quanh con gốc và việc co dãn,
biến hình được của nó, xem kĩ rig con gốc và animation của nó"; gen bằng Magnific (dưới 100 credit / ảnh, kể cả ảnh bộ phận; hơn thì hỏi).

    quai_bun.py ca_con        hình cả con gốc khung 0 idle → inbox/quai_bun_1/mau/goc_ca_con.png
    quai_bun.py slot          bảng slot (thứ tự vẽ, ảnh, xương, khung trên ảnh ca_con)
    quai_bun.py concept       file prompt từng hướng → gui_gpt/quai_bun_1/luot_1_concept_<k>.txt + HUONG_DAN.md
    quai_bun.py so_goc        chồng viền con gốc lên từng concept, in IoU → inbox/quai_bun_1/mau/_so_goc.png
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402

CODE = "quai_bun"
tho5.CON[CODE] = ("monster_3668", 8, 50)
_I = os.path.join(HERE, "inbox")

GOC_EN = ("the creature whose skeleton we reuse, idle pose, 1536x1024, white background: a hunched goo monster built like a gorilla, "
          "turned to the right. It is painted in a smooth digital cel style with soft light and dark planes and a glowing mouth: do NOT "
          "copy that painting style, its colours or its details. Use it for the POSE, the BODY PLAN and the CHEST-MOUTH construction only")
GOC_VI = ("Con gốc monster_3668, khung 0 idle, nền trắng 1536×1024: quái nhầy xám lục gù như khỉ đột quay phải, miệng to lòng xanh từ "
          "dưới đầu xuống ngực, hai nắm đấm chống đất, đế nhầy loang trái, chùm xúc tu đầu hồng. Chỉ lấy DÁNG, bố cục chi và cách dựng miệng")
REF_DAT = (os.path.join(_I, "dat_nung_1", "tai_ve", "L1_duyet.png"),
           "an approved hero of our game (a terracotta warrior golem), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen "
           "line, its crayon hatching and its flat colouring of a big earth body. Do NOT copy its design, its sword, its lava or its colours.",
           "Chiến binh đất nung (tướng đảo Hỏa) đã duyệt: lấy nét bút rung, vân sáp, cách tô phẳng thân đất to")
REF_VUON = (os.path.join(_I, "quy_nui_1", "tai_ve", "L1_duyet.png"),
            "an approved hero of our game (a rock ape titan), 1536x1024, white background: match EXACTLY its pen line, its crayon hatching "
            "and how a fierce, determined face is drawn (heavy brow, small eyes with one white dot). Do NOT copy its design, its rock "
            "blocks, its four arms or its colours: our creature is made of SOFT material with rounded blobby masses, not stone blocks.",
            "Vượn núi đá (tướng 5 đảo Thổ) đã duyệt: lấy nét bút, vân sáp và cách vẽ một gương mặt dữ, quả quyết")

CONCEPT = {
    "A": "a hulking MUD MONSTER (a swamp-mud brute) whose body is thick wet mud that can stretch and reshape",
    "B": "a hulking CLAY MONSTER (a living lump of soft potter's clay) whose body can be stretched and re-moulded",
    "C": "a hulking MUD MONSTER wearing a hard CLAY MASK and clay fist-wraps; its body is thick wet mud that can stretch and reshape",
}

PLAN = (
    "BODY PLAN (from image 1, keep it; the new creature is animated with the same skeleton): a huge hunched blob-brute built like a "
    "gorilla made of a soft material, turned to the RIGHT (it attacks towards the right). "
    "(1) BODY: one big heavy rounded mass; the near shoulder is a huge rounded HUMP at the upper LEFT (the highest, widest part of the back), "
    "the back slopes down to the left; a lighter, rounded BELLY in the middle right. "
    "(2) HEAD: small, at the upper RIGHT of the body, sunk low between the shoulders, its snout pointing to the lower right; TWO small "
    "slanted eyes side by side on the upper face, both visible (three-quarter view to the right). "
    "(3) MOUTH (keep this construction exactly): a HUGE mouth opens DOWNWARD from under the head across the chest. The head is the UPPER "
    "jaw, the big round belly under it is the LOWER jaw; a row of teeth along the rim of both jaws; the inside of the mouth is a tall oval "
    "area right of the centre, reaching from just under the eyes down to the middle of the belly. "
    "(4) NEAR ARM (on the LEFT): hangs from the shoulder hump; a huge FIST of thick, blocky, rounded fingers rests on the ground at the lower "
    "left of centre. "
    "(5) FAR ARM (on the RIGHT): a thick rounded upper arm at the right edge behind the head, bending down to a second huge fist of blocky "
    "fingers resting on the ground at the lower right. "
    "(6) BASE: NO legs: the body melts down into a wide, flat, puddle-like base spreading on the ground; its longest tongue reaches far to "
    "the lower LEFT. "
    "(7) STRANDS: about ten thin wobbly strands rise from the back and the head: three from the left part of the back, two from the "
    "shoulder hump, four or five round the top of the head; in our design they become the strands described under DESIGN, at the same "
    "places, about the same length and thickness. "
    "Same size and same place on the canvas as image 1; body, arms, fists and base keep about the same size and thickness.")

MOOD = ("MOOD: a heavy, menacing but likeable earth brute, fierce and determined (a hard frown, ready to smash); not cute-silly, not a "
        "mascot, not horror; mature proportions like image 1 (a small head for the huge body, not chibi).")

DETAIL = ("DETAIL: about as much detail as image 1, not more: big simple rounded masses, each a flat colour, at most one or two inner "
          "lines per piece; only the details listed under DESIGN.")

KHAC = ("It must NOT look like a recolour or a trace of image 1: NO pink, NO glowing cyan mouth, NO cyan crack veins, NO paddle-shaped "
        "tendril tips, NO swept-back pointed helmet crest, NO dragon-like angular head plates.")

HUONG = {
    "A": ("quái BÙN LẦY nâu sô-cô-la",
          "thân bùn ướt nâu sẫm, bụng (hàm dưới) nâu bùn sáng; xúc tu thành GIỌT BÙN dựng (sợi bùn rung, đầu là giọt tròn nặng), vài giọt "
          "văng; đầu bùn u nề, gờ mày bùn dày, mắt vàng hổ phách, hai SỪNG ĐÁ CUỘI ngắn cắm ngửa sau; lòng miệng vàng hổ phách, răng đá "
          "cuội tròn; nắm đấm là đá cuội xám bọc bùn; vài bong bóng bùn trên lưng; đế là vũng bùn",
          ["MATERIAL: thick wet MUD: dark chocolate brown #5E4231 on the faces turned to the viewer, #45301F on the faces turned away; the "
           "belly / lower jaw a lighter muddy brown #8A6646. Three or four small round MUD BUBBLES (little rings) on the back, nothing else.",
           "STRANDS: thick MUD DRIPS standing up from the back and head like stretched dripping mud: each a wobbly strand that ends in a "
           "heavy round DROP (a round blob, not a flat paddle), the drop the same brown; two tiny loose drops flying off near the tips.",
           "HEAD: a heavy lumpy MUD head: a thick overhanging BROW RIDGE of mud, two small fierce eyes in flat amber yellow #F2B33A under it "
           "(dark pupil, one small white dot each), a blunt rounded snout; TWO short blunt grey RIVER-STONE HORNS #A7A397 stuck in the top "
           "of the head, leaning back. No crest.",
           "MOUTH: the inside a flat warm AMBER-OCHRE #E9A63B (one flat colour, a slightly darker #C98426 back wall), a row of rounded "
           "PEBBLE TEETH in pale stone #D6D0C0 along both jaws.",
           "FISTS: each finger a big rounded grey RIVER STONE #9A968B (side faces #77736A) set in mud, mud between the stones.",
           "BASE: a wide wet MUD PUDDLE of the same brown, a few drip blobs on its edge, two small pebbles in it.",
           "NO plants, no moss, no glow."]),
    "B": ("quái ĐẤT SÉT vàng son",
          "thân đất sét sống vàng son, bụng kem; vết ngón cái ấn lõm; xúc tu thành CUỘN SÉT vê tròn (đầu véo dẹt, vài cuộn quăn); đầu nặn "
          "như tượng sét dữ, MÀO VÉO dọc giữa đầu, hai mắt vàng chanh trong hốc sẫm; lòng miệng nâu đỏ sẫm như lòng hũ sét, răng sét véo "
          "nhọn màu kem; nắm đấm sét đầu ngón sẫm, lòng bàn tay kem; đế là vũng sét lỏng",
          ["MATERIAL: soft raw POTTER'S CLAY: warm ochre #C98A55 on the faces turned to the viewer, #A46A3E on the faces turned away; the "
           "belly / lower jaw cream-tan #E4BD8C. Four shallow oval THUMB-PRESS dents and two finger-smear lines on the body, nothing else.",
           "STRANDS: rolled CLAY COILS (like clay snakes rolled between the palms) rising from the back and head, each with a slightly "
           "flattened PINCHED tip, two of them curling at the end; same ochre clay.",
           "HEAD: a sculpted CLAY head like a fierce clay idol: a flat-topped head with a PINCHED RIDGE crest running front-to-back down the "
           "middle (clay pinched between two fingers), a heavy brow, two small fierce eyes in flat lemon yellow #F4D447 set in dark brown "
           "sockets (dark pupil, one small white dot each), a blunt squarish snout.",
           "MOUTH: the inside a flat deep red-brown #7C3626 like the inside of an unglazed clay jar, a row of pinched pointed CLAY TEETH in "
           "cream #F0DAB2 along both jaws.",
           "FISTS: the same clay, the fingertips a darker #8B532E, pale cream palm / knuckle patches #E4BD8C.",
           "BASE: a puddle of wet CLAY SLIP, smooth, the same ochre a little lighter #D49A63, two drips on its edge.",
           "NO plants, no moss, no glow, no fired cracks."]),
    "C": ("quái BÙN đeo MẶT NẠ ĐẤT SÉT trắng ngà",
          "thân bùn nâu xám sẫm; đầu đội MẶT NẠ đất sét trắng ngà (gờ mày khắc, hai lỗ mắt lộ mắt vàng hổ phách, hai vạch sét đỏ son trên "
          "má), hai tai mặt nạ nhọn ngắn; nắm đấm quấn băng sét trắng ngà; xúc tu thành giọt bùn dựng; lòng miệng vàng hổ phách, răng "
          "kem; đế vũng bùn",
          ["MATERIAL: thick wet MUD: dark grey-brown #54463B on the faces turned to the viewer, #3E332B on the faces turned away; the belly / "
           "lower jaw a lighter mud #7B6A58. Three small round mud bubbles on the back, nothing else.",
           "STRANDS: thick MUD DRIPS standing up from the back and head: each a wobbly strand ending in a heavy round DROP, same mud colour.",
           "HEAD: the whole head (the upper jaw) is covered by a hard CLAY MASK in ivory clay #E8D9BC (side faces #C9B796): a carved heavy "
           "brow, TWO eye holes showing two small fierce amber eyes #F2B33A (dark pupil, one small white dot each), two red-ochre clay "
           "stripes #B4553A on each cheek, two short pointed mask ears leaning back. The mask is cracked by ONE small crack only.",
           "MOUTH: the inside a flat warm AMBER-OCHRE #E9A63B (darker #C98426 back wall), a row of blunt cream teeth #F0E2C4 along the mask "
           "rim and along the belly rim.",
           "FISTS: wrapped in bands of the same ivory clay #E8D9BC (two or three bands per fist), mud showing between the bands.",
           "BASE: a wide wet mud puddle, two drip blobs on its edge.",
           "NO skull look (the mask is a carved clay mask, not bones), no plants, no glow."]),
}


def task(k):
    return (f"TASK: DESIGN OUR OWN CHARACTER ON THE POSE OF image 1: {CONCEPT[k]}. Image 1 is the guide for the POSE, the BODY PLAN and "
            "the CHEST-MOUTH construction (the new creature will be animated with the same skeleton): keep its pose, its facing, its size "
            "and place on the canvas, where the head, the body, each arm, each fist, the base and the strands are, and which way they "
            "point. The head, the strands, the surface, the materials and the colours are OUR OWN NEW DESIGN, described below. Every limb "
            "and the head stay joined to the body (no white gaps).")


def concept():
    G = tho5.dat(CODE)
    gui = os.path.join(HERE, "gui_gpt", f"{CODE}_1")
    R = [(os.path.join(G.MAU, "goc_ca_con.png"), GOC_EN, GOC_VI), REF_DAT, REF_VUON]
    hd = ["# Gói gen: quái bùn / quái đất sét (`quai_bun`), tướng 8 đảo Thổ (ải 50)", "",
          "Con gốc của rig: `monster_3668` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept, ba hướng (2026-11-17, gen bằng Magnific GPT 2.6, 1k high, 95 credit / ảnh)", "",
          "Người dùng: \"concept quái vật bùn lầy hoặc quái vật đất sét như con gốc\". Ảnh 1 là mẫu dáng, bố cục chi và cách dựng miệng "
          "ngực (dùng chung bộ xương); đầu, xúc tu, chất liệu, màu là thiết kế mới; ba hướng do Claude đề xuất.", "",
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
              "", task(k), "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in doi] + ["", KHAC, "", DETAIL, "", tho5.style(), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no glow, no aura round the character, no smoke, no speed lines, no "
              "labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: cùng dáng, quay phải, miệng to mở từ dưới đầu xuống ngực (đầu là hàm trên, bụng là hàm dưới), hai mắt nhỏ cạnh nhau, "
           "hai nắm đấm chống đất đúng chỗ ảnh 1, đế loang sang trái, chùm xúc tu đúng chỗ; đầu, xúc tu, chất liệu đổi hẳn; không hồng, "
           "không lòng miệng xanh phát sáng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng; nền trắng tinh.",
           "", "Câu sửa nhanh: \"too many details: simplify\"; \"remove the shading / highlights / glow, flat colour only\"; \"keep the "
           "mouth opening downward from under the head across the chest, as in image 1\"."]
    tho5.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        tho5.ca_con(CODE)
    elif cmd == "slot":
        tho5.slot(CODE)
    elif cmd == "concept":
        concept()
    elif cmd == "so_goc":
        tho5.so_goc(CODE, sys.argv[2] if len(sys.argv) > 2 else "ABC")
    else:
        print(__doc__)
