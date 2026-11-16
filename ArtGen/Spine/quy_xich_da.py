# -*- coding: utf-8 -*-
"""Quỷ xích (quy_xich, rig monster_3408): concept THEO CON GỐC (quỷ béo cánh dơi, mũ giáp, móc neo nối xích), đổi sang quỷ béo MẶC GIÁP sắt.

    quy_xich_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/quy_xich_1/mau/goc_ca_con.png (+ .json: khung từng part)
    quy_xich_da.py concept    ba file prompt concept (ba hướng) → gui_gpt/quy_xich_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quy_xich as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "quy_xich_1")
CHIEN_SAT = os.path.join(HERE, "inbox", "chien_sat_1", "tai_ve", "L1_duyet.png")
QUY_DAO = os.path.join(HERE, "inbox", "quy_dao_1", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def khung_ca_con(atts, cao=800.0):
    """phép đổi toạ độ rig → ảnh 1536 × 1024: cả con cao ~cao px, đặt giữa khung."""
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024; ghi khung bao từng part trên ảnh."""
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    s, cx, cy, T = khung_ca_con(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    hop = {}
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)
        lay = lay.convert("RGBA")
        al = np.asarray(lay)[..., 3] > 60
        if al.any():
            ys, xs = np.nonzero(al)
            hop[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
        can.alpha_composite(lay)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")
    for k, v in hop.items():
        print(k, v)


MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: a big FAT round-bellied little demon seen from the front, turned slightly to the viewer's RIGHT, sitting "
    "low on two very short stubby legs): "
    "the HEAD in the upper middle-right: a round face turned three-quarters to the viewer's right; two narrow slanted angry eyes (the right "
    "eye close to the right edge of the face); a small wavy frowning mouth with one tiny fang at its right corner; no nose. "
    "A HELMET on the head: it covers the top of the head and comes down both sides of the face as cheek guards (a big guard down the left "
    "side, a small one on the right side), its front band sits just above the eyes. "
    "TWO HORNS come up through the top of the helmet: a short one on the left, a big one on the right. "
    "THREE SPIKES in a row stick up from the back behind the head (to the viewer's left of the head). "
    "SHOULDERS: a big shoulder pad on the viewer's LEFT shoulder with one big spike sticking up from it; a small shoulder pad on the right "
    "shoulder, half hidden behind the head. "
    "TWO BAT WINGS behind the shoulders: the left wing spreads up and out to the upper left, the right wing spreads to the right behind "
    "the weapon arm. "
    "BODY: a huge round pot belly (with a navel) fills the middle and the bottom of the picture; dark pants round the lower belly and the "
    "hips. "
    "CHEST CHAINS: two chains cross the chest in an X, from the shoulders down to the sides of the belly, with a round fastener where they "
    "cross in the middle of the chest. "
    "LEFT ARM (viewer's left): a big fat arm hanging down along the left side of the belly, its hand with three short claws near the hip. "
    "RIGHT ARM (viewer's right): a fat arm bent forward, its hand with three thick fingers wrapped round the SHAFT of the HOOK WEAPON, "
    "holding it upright on the right. "
    "THE HOOK WEAPON: a big hook blade at the top, above a collar, a short thin iron shaft going down through the fist, a ring at the lower "
    "end of the shaft; from that ring a CHAIN of big iron links hangs down and runs along the ground to the left, behind the right leg. "
    "LEGS: two very short dark stubby legs under the belly. "
    "TAIL: a thin devil tail with an arrow-head tip, lying on the ground at the far left.")

# ba hướng (Claude đề xuất, chờ người dùng chọn). Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("quỷ đỏ, giáp gang sẫm",
          "da đỏ gạch; mũ ĐỔI DÁNG thành mũ chảo tròn có sống giữa + hàng đinh tán ở vành; hai sừng thành sừng bò ngà cong tới trước; ba gai "
          "lưng thành ba vây sắt tam giác; giáp vai hai lớp tròn + một gai nón sắt; THÊM giáp bụng tròn ôm bụng phệ + đai sắt; ổ khoá đồng "
          "thành ổ khoá sắt to; lưỡi móc thành móc treo thịt một lưỡi cong có ngạnh; mắt vàng",
          ["SKIN (face, arms, the tail): flat brick red #B8473A; the claws and fingers dark charcoal #3A3236.",
           "EYES: the same two narrow slanted angry eyes, flat yellow #F2C14E inside the ink outline (no glow, no pupils). The mouth keeps its "
           "wavy frown and its one tiny ivory fang #EFE6D2.",
           "ARMOUR colours (everything made of metal below): dark gunmetal iron #565B66 on the main faces, darker iron #3F434C on the faces "
           "turned away, light steel #9AA1AC only on rims where listed.",
           "HELMET: a NEW SHAPE: a round iron KETTLE HELMET: a smooth dome with ONE raised ridge running from front to back over its top, a "
           "flat brim band just above the eyes with four small round rivets in a row, and two rounded iron cheek plates down the sides of "
           "the face (big on the left, small on the right). No vent slits, no visor bars.",
           "HORNS: a NEW SHAPE: two thick BULL HORNS of pale ivory #E9DDBF with three thin ink ring lines near their base, both coming out "
           "through the sides of the dome and curving forward and up to a sharp point; the right horn bigger than the left. Not pink, not "
           "a crescent.",
           "BACK SPIKES: the three spikes become three flat triangular IRON FINS (dark iron, one ridge line each), same row, same sizes.",
           "LEFT SHOULDER PAD: a rounded iron pauldron made of TWO overlapping curved plates with a light steel rim, and ONE short pointed "
           "conical iron spike sticking up from it (no crystal). The right shoulder pad: one rounded iron plate.",
           "BELLY ARMOUR (new, it makes him an armoured demon): a big rounded iron BELLY PLATE that covers the chest and the round pot belly "
           "following its round shape exactly, with two curved lines across its lower part (overlapping plates) and a thick iron BELT band "
           "at its lower edge; the pants under it stay dark charcoal #2E2A2E. No navel showing. The two chest chains still run over it.",
           "CHEST CHAINS and the HOOK CHAIN: plain steel links #9AA1AC with the inside of each link dark. The round fastener where the chest "
           "chains cross becomes a big iron PADLOCK (a rounded body with a keyhole, its shackle up), dark iron with a light steel rim.",
           "FOREARMS: a plain iron bracer band round each wrist. LEGS: short iron greaves, dark iron.",
           "WINGS: the same bat-wing shape and size; flat dark maroon membrane #5C2A2E, the wing bones charcoal #3A3236.",
           "TAIL: brick red with an iron arrow-head tip.",
           "THE HOOK: a NEW SHAPE in the same place and the same size as the old blade: a heavy iron MEAT HOOK: one thick round hook that "
           "rises from the collar, curves over to the left and comes down to a sharp point with one small barb; the inner edge of the curve "
           "light steel #B5BCC6, the rest #8D95A2; the collar a plain dark iron ring (no crystal); the shaft and the end ring iron."]),
    "B": ("quỷ xanh than, giáp thép + đồng thau",
          "da xanh than xám; mũ ĐỔI DÁNG thành mũ thép có chóp nhọn + vành đồng thau; hai sừng dài thẳng chĩa xiên ra hai bên, đầu bịt đồng; "
          "ba gai lưng thành ba chóp thép đầu đồng; giáp vai vòm tròn viền đồng một đinh to, không gai; THÊM giáp ngực thép + đai bụng thép "
          "khoá đồng (bụng lộ); ổ khoá thành vòng khoá đồng; lưỡi móc thành móc liềm cong to; mắt cam",
          ["SKIN (face, arms, belly, the tail): flat slate blue-grey #5E6B86; the belly the same colour (one flat colour, no lighter patch); "
           "the claws and fingers dark navy #2F3446.",
           "EYES: the same two narrow slanted angry eyes, flat orange #F08A3A inside the ink outline (no glow, no pupils). The mouth keeps its "
           "wavy frown and its one tiny ivory fang #EFE6D2.",
           "ARMOUR colours: steel #A7AEB9 on the main faces, darker steel #727A88 on the faces turned away, a thin BRASS trim #C99A3E only "
           "where listed.",
           "HELMET: a NEW SHAPE: a steel helmet with a tall pointed SPIKE on its top (like a spiked cap), a brass band round its brim just "
           "above the eyes, and two steel cheek plates with brass edges down the sides of the face (big on the left, small on the right). "
           "No vent slits, no visor bars.",
           "HORNS: a NEW SHAPE: two long nearly straight HORNS, black #2C2A30, coming out of the sides of the helmet and pointing out "
           "diagonally up and away from the head (one to the upper left, one to the upper right, the right one longer), each with a small "
           "brass cap on its tip. Not pink, not curved like a crescent.",
           "BACK SPIKES: the three spikes become three steel CONES with brass tips, same row, same sizes.",
           "LEFT SHOULDER PAD: a big ROUND steel dome pauldron with a brass rim and one big round brass rivet in its middle; NO spike on it. "
           "The right shoulder pad: a small steel dome with a brass rim.",
           "CHEST ARMOUR (new, it makes him an armoured demon): a steel BREASTPLATE covering the upper chest under the head (down to about "
           "the height of the chain crossing); below it the round pot belly stays bare skin with its navel; a wide steel BELT plate with a "
           "square brass buckle round the bottom of the belly over the dark navy pants #2B2F3D.",
           "CHEST CHAINS and the HOOK CHAIN: plain steel links #A7AEB9 with the inside of each link dark. The round fastener where the chest "
           "chains cross becomes a plain round BRASS RING #C99A3E.",
           "FOREARMS: a steel bracer with a brass edge on each wrist. LEGS: short steel greaves.",
           "WINGS: the same bat-wing shape and size; flat dark navy membrane #2F3446, the wing bones black #2C2A30.",
           "TAIL: slate blue-grey with a steel arrow-head tip.",
           "THE HOOK: a NEW SHAPE in the same place and the same size as the old blade: a big curved SICKLE HOOK: one wide curved blade that "
           "rises from the collar and sweeps over to the left and down to a long sharp point, its sharpened inner edge a light steel strip "
           "#C9CED6, the rest steel #8D95A2; the collar a brass ring #C99A3E (no crystal); the shaft and the end ring steel."]),
    "C": ("quỷ xanh rêu, giáp đồng đỏ kiểu đai thùng",
          "da xanh rêu sẫm; mũ ĐỔI DÁNG thành mũ xô đỉnh bằng có gờ mày + ba đinh tán; hai sừng cong ngược ra sau như cái móc; ba gai lưng "
          "thành ba móc sắt cong; giáp vai vuông đồng đỏ + gai móc; THÊM giáp bụng kiểu thùng: ba đai đồng ôm quanh bụng phệ; ổ khoá thành "
          "vòng đồng; lưỡi móc thành móc cẩu công nghiệp dày; mắt vàng chanh",
          ["SKIN (face, arms, belly, the tail): flat dark moss green #4F6B4A; the claws and fingers dark charcoal #2E2B2C.",
           "EYES: the same two narrow slanted angry eyes, flat lemon yellow #E8E05A inside the ink outline (no glow, no pupils). The mouth "
           "keeps its wavy frown and its one tiny ivory fang #EFE6D2.",
           "ARMOUR colours: COPPER #B3683F on the main faces, darker copper #84492E on the faces turned away, dark iron #4A4B52 where listed.",
           "HELMET: a NEW SHAPE: a copper BUCKET HELMET with a FLAT TOP, straight sides and a thick horizontal brow ridge just above the "
           "eyes with three round rivets on it, and two square copper cheek plates down the sides of the face (big on the left, small on "
           "the right). No vent slits, no visor bars.",
           "HORNS: a NEW SHAPE: two dark iron #4A4B52 horns that come out of the top corners of the helmet, rise a little and then CURL BACK "
           "and down like hooks (each ends in a downward point behind its base); the right one bigger. Not pink.",
           "BACK SPIKES: the three spikes become three curved dark iron HOOKS pointing back, same row, same sizes.",
           "LEFT SHOULDER PAD: a big square-cornered copper pauldron with a dark iron rim and ONE curved hook-shaped iron spike sticking up "
           "from it (no crystal). The right shoulder pad: a small square copper plate.",
           "BELLY ARMOUR (new, it makes him an armoured demon): BARREL ARMOUR: THREE wide copper HOOP BANDS go round the round pot belly "
           "(one under the chest, one across the middle, one at the bottom over the dark pants), following its round shape; the skin shows "
           "between the bands; no navel showing. The pants dark charcoal #2E2B2C.",
           "CHEST CHAINS and the HOOK CHAIN: dark iron links #6B6E77 with the inside of each link darker. The round fastener where the chest "
           "chains cross becomes a plain round COPPER RING.",
           "FOREARMS: a copper bracer on each wrist. LEGS: short dark iron greaves.",
           "WINGS: the same bat-wing shape and size; flat dark olive membrane #3C4A36, the wing bones charcoal #2E2B2C.",
           "TAIL: moss green with a dark iron arrow-head tip.",
           "THE HOOK: a NEW SHAPE in the same place and the same size as the old blade: a heavy industrial CRANE HOOK: a thick C-shaped hook "
           "(fat at its bottom curve, thinner towards its sharp upturned tip, opening to the left), dark iron #5A5C64 with its flat front "
           "face lighter #8A8D96; the collar a copper ring (no crystal); the shaft and the end ring dark iron."]),
}

STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) for the "
    "few inner lines (plate edges, the eyes, the mouth, the chain links), and every area filled with ONE flat colour with visible "
    "coloured-pencil / wax-crayon hatching. Image 1 is painted in a smooth digital cel style with soft light and dark planes, a pink flush "
    "on the chin and glowing red eyes: do NOT copy that painting style or its purple and pink colours: no shading, no highlights, no white "
    "shine streaks, no gradients, no blush, no glow, no shadows, no gloss, no sparkles: flat colour only. A different tone appears only "
    "where a different face (front face / side face) or material is listed. VERY SIMPLE DESIGN, FEW DETAILS: no extra rivets, engravings, "
    "scratches, cracks, dents, skulls, badges, flames or patterns beyond what is listed.")


def prompt_concept():
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, "the REFERENCE character, 1536x1024, white background: a big fat purple demon with bat wings, a dark iron half-helmet with "
               "pink horns, red crystal spikes on its back and on its left shoulder pad, two chains crossing its chest with a bronze lock, "
               "a thin devil tail, holding upright on the right a crescent hook blade on a short shaft with a chain hanging from it. It is "
               "painted in a smooth digital cel style. Keep its POSE, its PIECES and their PLACES; change its LOOK and the shapes listed.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): quỷ béo tím cánh dơi, mũ giáp sẫm sừng hồng, gai tinh thể đỏ ở lưng và giáp vai "
          "trái, xích chéo ngực có ổ khoá đồng, đuôi mũi tên, tay phải cầm dựng lưỡi móc hình lưỡi liềm trên cán ngắn, xích thõng xuống đất. "
          "Giữ dáng và từng mảnh, đổi hình"),
         (CHIEN_SAT, "an approved hero of our game from the same metal island (a chubby armoured knight), 1536x1024, white background: match "
                     "EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring of metal "
                     "plates (front faces and darker side faces). Do NOT copy its design or colours.",
          "Chiến binh sắt (tướng 2 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô giáp phẳng (mặt trước + mặt bên sẫm)"),
         (QUY_DAO, "another approved hero of our game (an armoured demon with a big blade), 1536x1024, white background: see how a sturdy "
                   "armoured demon body, its dark iron armour and its horns are drawn flat. Do NOT copy its design, its flames or its "
                   "colours.",
          "Quỷ đao (tướng đảo Hỏa) đã duyệt: xem cách vẽ thân quỷ chắc nịch, giáp sắt sẫm, sừng tô phẳng")]
    hd = ["# Gói GPT: quỷ xích (quy_xich), tướng 5 đảo Kim", "",
          "Con gốc của rig: `monster_3408` (quỷ béo tím cánh dơi, móc nối xích; game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong "
          "máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng (2026-11-16)", "",
          "Người dùng: \"concept quỷ béo mặc giáp, vũ khí là móc liền gắn với xích sắt\". Ba file, mỗi file một hướng; giữ dáng đứng, chỗ và cỡ "
          "từng mảnh của con gốc (để lắp lên đúng xương), đổi hẳn dáng các mảnh nhận diện (mũ, sừng, gai lưng, giáp vai, lưỡi móc) và thêm "
          "giáp ở thân để khỏi giống con gốc.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: REDESIGN ON THE SAME POSE. Redraw the demon of image 1 as ONE picture of OUR OWN character, a FAT ARMOURED DEMON with "
              "a hook on an iron chain: the SAME pose, with EVERY piece in the same place, at the same size and with the same overlaps (if "
              "the new picture were laid over image 1, every piece must sit on its old place), but with the NEW shapes, new materials, new "
              "colours and our hand-drawn drawing style described below. Do not add pieces other than the armour listed, do not remove, "
              "merge or move pieces.", "",
              MO_TA_CON, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a grumpy, tough, determined fat demon warrior ready to fight (a game hero), not a cute mascot, not scary. Both arms, "
              "both legs, both wings and the tail must stay attached to the body exactly as in image 1; the fist really grips the shaft.",
              "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no fire, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng chỗ và cỡ từng mảnh như ảnh 1 (chồng lên phải trùng, trừ mũ, sừng, gai, lưỡi móc đổi dáng); mặt nghiêng phải, "
           "hai mắt xếch, miệng cau một răng nanh; tay phải nắm cán móc, xích thõng xuống đất sang trái; hai cánh, hai chân, đuôi dính thân; "
           "nét bút mực rung, vân sáp, tô phẳng, không bóng, không má hồng, mắt không phát sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the shading / highlights, flat colour only\"; \"keep every piece at the same place and size as in image "
           "1\"; \"the fist must grip the hook shaft\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


def _mat_na(p):
    """mặt nạ hình (khác nền trắng), lấp kín lỗ."""
    import cv2
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H)), np.int16)
    m = ((255 - a).max(2) > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k.astype(bool)


def so_goc(ks="ABC"):
    """chồng viền hình bóng con gốc (đỏ) lên từng concept, in độ khớp IoU → mau/_so_goc.png."""
    import cv2
    g = _mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
    cs, _ = cv2.findContours(g.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    o = []
    for k in ks:
        p = os.path.join(G.TAI, f"L1_{k}.png")
        if not os.path.exists(p):
            continue
        m = _mat_na(p)
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
        c.save(os.path.join(G.MAU, "_so_goc.png"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "so_goc":
        so_goc(*(sys.argv[2:3] or ["ABC"]))
    elif cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)
