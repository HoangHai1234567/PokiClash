# -*- coding: utf-8 -*-
"""Tê Thiềm DẠNG 2 (thu_da_2; tướng 3 đảo Thổ, ải 10; rig monster_3526 = dạng tiến hoá của 3525 trong game gốc): MẢNH "đúng chỗ, đúng cỡ".
Concept duyệt `inbox/thu_da_2/tai_ve/L1_duyet.png` (= L1_A; người dùng 2026-11-17 "ok concept 3 con kia ổn rồi làm đi"): cóc tê giác da đất
nung, sừng đá kem dài trên mõm, hàm kem răng tù, mắt hổ phách, rất nhiều cụm pha lê hổ phách trên lưng, vai, đuôi, khuỷu; đai da ba tấm đá.

Concept đứng bốn chân kiểu cóc còn rig 3526 thì lom khom: tay gần chống đất có bàn ba ngón, tay xa ôm một KHỐI GAI LỚN (`wuqi_*`, "vũ khí")
vắt qua lưng, một lưỡi dài chéo trước thân xuống đất; IoU concept / con gốc chỉ 0,555. Nên làm hai bước (skill pokiclash-spine-rig mục 00):
  C0  CONCEPT TRÊN RIG: vẽ lại đúng con đã duyệt theo ĐÚNG dáng, chỗ, cỡ từng mảnh của con gốc (ảnh 1 = hình con gốc khung 0 idle); khối gai
      thành cụm lăng trụ pha lê hổ phách (mỗi gai một lăng trụ, cùng chỗ, cùng góc), tay gần thành chân trước đất nung vuốt kem, tay xa thành
      vai đất nung ôm cụm pha lê. Lúc rig vung "vũ khí" trông như vung khối pha lê trên lưng (Claude chính dặn giữ cách đó).
  T1..T5  từng nhóm mảnh không chồng nhau, chép từ C0 đúng chỗ đúng cỡ, vẽ đủ phần bị che (nhóm theo mặt nạ part gốc, `mau/mat_na_part.npz`):
      T1 THÂN LIỀN (thân, eo, cổ trước, bướu cổ sau, đầu, hai hàm; đai da vẽ liền trên eo; không mắt, sừng, chi, đuôi, pha lê)
      T2 chân trước gần (vai + cẳng + bàn + ba ngón vuốt), vai xa, đuôi
      T3 lưỡi pha lê dài wuqi_01 + wuqi_011, wuqi_11, gai lưng shenti_02, gai đầu to_02, gai gối zuoqigai
      T4 wuqi_02, wuqi_05, wuqi_06, wuqi_010, wuqi_012, SỪNG jiao_01, gai vai youdabi_02, gai gối youqigai
      T5 wuqi_03, wuqi_04, gai shenti_03, chân sau xa, chân sau gần
  mắt cắt thẳng từ C0; lòng miệng + lưỡi vẽ bằng mã.

    thu_da2_manh.py c0          file prompt C0 → gui_gpt/thu_da_2/luot_2_C0.txt (+ HUONG_DAN.md)
    thu_da2_manh.py can         phép căn C0 → con gốc (IoU hình bóng) → mau/can.json
    thu_da2_manh.py prompt      file prompt T1..T5 (ảnh mẫu = C0) → gui_gpt/thu_da_2/luot_2_<tờ>.txt
    thu_da2_manh.py cat [tờ]    cắt ảnh về → manh/<slot>.png + manh/dat.json
    thu_da2_manh.py mat         mắt cắt từ C0; mắt nhắm vẽ bằng mã
    thu_da2_manh.py ghep        ghép mọi mảnh theo thứ tự vẽ cạnh C0 → manh/_ghep.png + IoU
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
import tho5  # noqa: E402
import tho5_dang2 as D2  # noqa: E402

G = D2.dat2("thu_da")
W, H = 1536, 1024
DUYET = os.path.join(G.TAI, "L1_duyet.png")
C0 = os.path.join(G.TAI, "C0.png")
GOC = os.path.join(G.MAU, "goc_ca_con.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "thu_da_2")
MUC = (43, 33, 24)


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


def style():
    return tho5.style().replace("(images 2 and 3)", "(images 2 and 3)")


# ---------------------------------------------------------------- C0: concept trên rig
GOC_C0 = ("the ORIGINAL CREATURE of the skeleton (a game reference), 1536x1024, white background: a hunched heavy rock beast turned to the "
          "RIGHT. Use it as the EXACT LAYOUT: the outline, the pose and the place, size and angle of EVERY piece (head, jaw, horn, body, neck, "
          "each arm and leg, the hand and its three fingers, the tail, every spike) must stay the same. It is painted in a smooth digital cel "
          "style with soft light and dark planes and gradients: do NOT copy that painting style, its colours, its flame shapes or its face.")
DUYET_EN = ("our APPROVED design of this character (1536x1024, white background): a stocky TOAD-RHINO with warm terracotta skin, a big cream "
            "lower jaw with blunt teeth, a long cream stone horn on the snout, a small angry amber eye under a heavy brow, a cream belly, a "
            "dark hide belt with three flat stone plates, and MANY clusters of AMBER CRYSTAL prisms on the back, shoulders, elbows and tail. "
            "Take from it the LOOK only (species, face, colours, materials, crystals, line); NOT its pose.")
C0_BAN_DO = [
    "BODY, NECK AND SHOULDER HUMP (the big dark rock masses in the middle of image 1, from the shoulders down to the waist): the TOAD-RHINO "
    "body of image 2: warm terracotta skin #B8663E with two or three flat darker #8A4A2C patches; where image 1 shows the pale grey belly "
    "under the chest, a cream belly #EADCBD. Same outline as image 1 (rounded, not jagged rock).",
    "WAIST: around the waist, where image 1 has a few small dark pieces at the hip, the dark hide BELT #5A3424 of image 2 with three flat "
    "grey stone plates #A79A8A.",
    "HEAD (upper right, the dark head with orange flame spikes in image 1): the wide toad-rhino head of image 2 in the SAME place and size: "
    "terracotta, a heavy angry brow, ONE small amber eye #F5C04A (dark pupil, one small white dot) exactly where the yellow eye of image 1 "
    "is, a rounded snout at the right; no flame spikes (the head outline becomes smooth and rounded).",
    "JAW AND MOUTH: the big cream lower JAW #EADCBD with a row of blunt teeth exactly where the pale jaw of image 1 is; the mouth slightly "
    "open as in image 1, a dark red-brown mouth inside with a pink tongue where image 1 shows the red tongue.",
    "HORN: the tall orange horn on top of the head in image 1 becomes the long thick cream STONE HORN #EADCBD of image 2, same place, same "
    "size, same angle (pointing up).",
    "THE SMALL ORANGE SPIKE at the right side of the head, the spike on the near shoulder, the spikes on the back of the body, the knee "
    "spikes: each becomes a small AMBER CRYSTAL prism #F0AA32 (straight edges, sharp point, one lighter flat facet #FFD27A), same place, "
    "size and angle.",
    "THE BIG SPIKY CLUB (the cluster of long orange spikes at the upper left, held by the far arm, and the LONG BLADE that crosses "
    "diagonally in front of the body down to the ground): a big CLUSTER OF AMBER CRYSTALS: EVERY spike of image 1 becomes ONE long straight "
    "amber crystal prism #F0AA32 with a sharp point and one lighter flat facet #FFD27A, at the same place, size and angle as that spike "
    "(the longest one runs diagonally in front of the body down to the ground, exactly like the long blade of image 1).",
    "FAR ARM (the dark rock arm at the upper left of the body that holds the club): a thick terracotta shoulder and arm, same place and "
    "size, gripping the base of the crystal cluster.",
    "NEAR FRONT LEG (the big dark rock upper arm and forearm at the right, with the hand and its THREE fingers planted on the ground at the "
    "lower right): the thick terracotta FRONT LEG of image 2, same place, size and bend; the hand becomes a broad foot and the three fingers "
    "become three short terracotta toes, each tipped with a CREAM CLAW #EFE2C4 (exactly where the three finger tips of image 1 are).",
    "HIND LEGS (the two short dark rock legs at the bottom middle and bottom left): thick terracotta legs with cream claws, same places.",
    "TAIL (the long dark tail lying at the lower left): a thick terracotta tail with two small amber crystals, same place and length.",
]


def c0():
    out, save = luu("C0")
    p = os.path.join(GUI, "luot_2_C0.txt")
    R = [(GOC, GOC_C0, "Con gốc 3526 khung 0 idle: BỐ CỤC chuẩn (dáng, chỗ, cỡ, góc từng mảnh)"),
         (DUYET, DUYET_EN, "Concept dạng 2 đã duyệt (L1_A): lấy hình dáng, màu, chất liệu")]
    from tho5_huong import REF
    R += [REF["rua"]]
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
    t += [""] + save + ["",
          "TASK: REDRAW OUR CHARACTER (image 2) IN EXACTLY THE POSE AND PIECE LAYOUT OF image 1. The new picture will be cut into pieces and "
          "put on the skeleton of image 1, so if it were laid over image 1 every piece must coincide with the matching piece of image 1 "
          "(same outline, same place, same size, same angle). Only the DESIGN changes: each piece of image 1 is redrawn as the matching part "
          "of our toad-rhino of image 2, as listed below. Every limb, the tail, the head and the arm holding the crystals stay joined to the "
          "body (no white gaps).", "", "PIECE BY PIECE:"] + [f"- {d}" for d in C0_BAN_DO]
    t += ["", style().replace("(images 2 and 3)", "(images 2 and 3)"), "",
          "MOOD: the grown-up, battle-ready form of our hero: a determined, fierce face; cute but tough; not scary.", "",
          "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at EXACTLY the same "
          "place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura, no smoke, no speed lines, no labels, no frame."]
    ghi(p, t)
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n") if os.path.exists(hd) else ""
    gd = ["", "## Lượt 2: concept trên rig rồi mảnh đúng chỗ, đúng cỡ (2026-11-17, agent dạng 2 Tê Thiềm)", "",
          "Concept duyệt đứng bốn chân còn rig 3526 lom khom ôm khối gai: trước hết vẽ lại con đã duyệt theo đúng bố cục từng mảnh của con gốc "
          "(C0), rồi các tờ mảnh T1..T5 chép từ C0.", "", "| Ảnh mẫu C0 | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", f"- **C0**: chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`.",
           "  Kiểm: chồng lên con gốc thì từng mảnh trùng chỗ; mặt, màu cóc tê giác như concept; khối gai thành cụm lăng trụ hổ phách; tay gần "
           "thành chân trước vuốt kem; mọi chi dính thân; tô phẳng, nền trắng."]
    ghi(hd, ((cu + "\n") if cu else "").split("\n") + gd)
    print(p)


# ---------------------------------------------------------------- căn C0 lên con gốc (C0 vẽ đúng chỗ: thường gần như đồng nhất)
def mat_na(p):
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H))).astype(np.int16)
    m = ((255 - a).max(2) > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k


def can():
    """C0 → khung con gốc: co a quanh tâm + dời (dx, dy), chọn theo IoU hình bóng (C0 vẽ đúng chỗ nên a ≈ 1)."""
    g = mat_na(GOC)
    c = mat_na(C0)
    best = None
    for a in np.arange(0.94, 1.065, 0.01):
        M = np.float32([[a, 0, 768 * (1 - a)], [0, a, 512 * (1 - a)]])
        cw = cv2.warpAffine(c, M, (W, H), flags=cv2.INTER_NEAREST)
        for dy in range(-30, 31, 3):
            for dx in range(-30, 31, 3):
                cs = np.roll(np.roll(cw, dy, 0), dx, 1)
                iou = (cs & g).sum() / max(1, (cs | g).sum())
                if best is None or iou > best[0]:
                    best = (float(iou), float(a), int(dx), int(dy))
    iou, a, dx, dy = best
    c_ = mat_na(DUYET)
    iou0 = (c_ & g).sum() / max(1, (c_ | g).sum())
    json.dump(dict(a=a, dx=dx, dy=dy, iou=iou), open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print(f"căn C0: a {a:.2f}, dời ({dx}, {dy}) px, IoU hình bóng {iou:.3f} (concept duyệt chưa căn: {iou0:.3f})")


def phep_can():
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    return j["a"], j["dx"], j["dy"]


def tf():
    """px C0 → px khung con gốc → thế giới rig."""
    a, dx, dy = phep_can()
    jj = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = jj["s"], jj["cx"], jj["cy"]
    c2g = lambda P: np.stack([a * (P[:, 0] - W / 2) + W / 2 + dx, a * (P[:, 1] - H / 2) + H / 2 + dy], 1)
    g2c = lambda Q: np.stack([(Q[:, 0] - W / 2 - dx) / a + W / 2, (Q[:, 1] - H / 2 - dy) / a + H / 2], 1)
    g2w = lambda Q: np.stack([cx + (Q[:, 0] - W / 2) / s, cy - (Q[:, 1] - H / 2) / s], 1)
    w2g = lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
    return dict(a=a, s=s, c2w=lambda P: g2w(c2g(P)), c2g=c2g, g2c=g2c, w2g=w2g)


def mat_part():
    """mặt nạ từng part gốc (idle 0) trong px C0 (qua phép căn ngược)."""
    z = np.load(os.path.join(G.MAU, "mat_na_part.npz"))
    a, dx, dy = phep_can()
    M = np.float32([[1 / a, 0, (-W / 2 - dx) / a + W / 2], [0, 1 / a, (-H / 2 - dy) / a + H / 2]])
    return {k: cv2.warpAffine(z[k].astype(np.uint8), M, (W, H), flags=cv2.INTER_NEAREST).astype(bool) for k in z.files}


# ---------------------------------------------------------------- nhóm mảnh (tờ gen từ C0)
CHAN_TRUOC = ["youdabi_01", "youxiaobi", "shouzhang", "shouzhi_01", "shouzhitou_01", "shouzhi_02", "shouzhitou_02", "shouzhi_03",
              "shouzhitou_03"]
THAN = ["shenti_01", "yao", "bozi_01", "bozi_02", "to_01", "xiaba_01", "xiaba_02"]
NHOM = {
    "T1": [("than", THAN, "the WHOLE BODY, NECK AND HEAD as ONE piece: the terracotta body with its cream belly and the dark hide belt with "
            "its three stone plates on the waist, the shoulder hump and the neck, the head with its heavy brow, the cream lower jaw with its "
            "blunt teeth and the dark open mouth with the pink tongue",
            "KEEP ONLY these three amber crystals that grow out of the body itself, exactly as they are: the big one on top of the back "
            "centred at about x = 800, y = 290; the one on top of the head centred at about x = 987, y = 360; the one at the left side of the "
            "head centred at about x = 873, y = 493. Draw it WITHOUT the eye (where the eye was: plain terracotta skin under the brow), "
            "WITHOUT the cream stone horn on the snout and WITHOUT the amber crystal behind that horn (where they stood: the head and snout "
            "continue as plain rounded terracotta), WITHOUT every other amber crystal (where crystals stood or crossed in front: the body "
            "continues as plain terracotta / cream body), WITHOUT the four legs, the far arm and the tail (where they cover the body: the "
            "body, belly and belt continue as plain rounded shapes). One closed shape with the ink outline all round")],
    "T2": [("chan_truoc", CHAN_TRUOC, "the NEAR FRONT LEG (at the right): the big shoulder, the forearm, the broad foot and its three toes "
            "with cream claws, WITH its two small amber crystals (on the forearm and at the elbow)", "complete its top, hidden behind the head and "
            "the body, as a rounded shoulder"),
           ("zuodabi", ["zuodabi"], "the FAR ARM at the upper left of the body (the terracotta shoulder and arm that grips the crystals)",
            "complete the part hidden behind the crystals and the body as a rounded arm; WITHOUT the crystals it holds"),
           ("weiba", ["weiba"], "the TAIL lying at the lower left, WITH its two small amber crystals", "complete the part hidden "
            "behind the legs and crystals as the tail continuing")],
    "T3": [("wuqi_01", ["wuqi_01"], "the LONGEST amber crystal: the long one that runs diagonally in front of the body down to the ground",
            "complete it as one straight prism from its base to its sharp tip"),
           ("wuqi_11", ["wuqi_11"], None, None), ("shenti_02", ["shenti_02"], None, None),
           ("to_02", ["to_02"], "the cream STONE HORN on the snout (pointing up)", "complete its base, hidden in the head, as a rounded base"),
           ("zuoqigai", ["zuoqigai"], "the small amber crystal on the knee of the NEAR hind leg, centred at about x = 886, y = 791",
            "complete its base as the prism continuing")],
    "T4": [("wuqi_02", ["wuqi_02"], None, None), ("wuqi_05", ["wuqi_05"], None, None), ("wuqi_06", ["wuqi_06"], None, None),
           ("wuqi_010", ["wuqi_010"], None, None), ("wuqi_012", ["wuqi_012"], None, None),
           ("jiao_01", ["jiao_01"], "the amber crystal on top of the head at the right, standing just behind the cream horn of the snout",
            "complete the part hidden behind the cream horn as the prism continuing down into the head"),
           ("youqigai", ["youqigai"], "the small amber crystal on the knee of the FAR hind leg (bottom left), centred at about x = 606, y = 811",
            "complete its base as the prism continuing")],
    "T5": [("wuqi_03", ["wuqi_03"], None, None), ("wuqi_04", ["wuqi_04"], None, None), ("shenti_03", ["shenti_03"], "a small amber crystal growing from the back, centred at about x = 667, y = 478, mostly hidden "
            "behind the big crystals in image 1", "draw it COMPLETE as one small prism pointing up-left, about 70 px long"),
           ("chan_sau_xa", ["zuodatui", "zuoxiaotui"], "the FAR HIND LEG (bottom left, behind): thigh, lower leg and foot with cream claws",
            "complete the parts hidden behind the long crystal, the tail and the belly as the leg continuing"),
           ("chan_sau_gan", ["youdatui", "youxiaotui"], "the NEAR HIND LEG (bottom middle): thigh, lower leg and foot with cream claws",
            "complete the part hidden behind the belly and belt as a rounded thigh; WITHOUT the knee crystal")],
}


def mo_ta_pha_le(slot, Mp):
    """mô tả một tinh thể theo chỗ, dài, hướng mũi (px C0, theo mặt nạ part gốc: C0 vẽ đúng chỗ)."""
    ys, xs = np.nonzero(Mp[slot])
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    w, v = np.linalg.eigh(np.cov((P - c).T))
    ax = v[:, 1]
    t = (P - c) @ ax
    L = float(np.ptp(t))
    # mũi = đầu hẹp hơn (bề ngang ở 15 % hai đầu)
    nrm = np.array([-ax[1], ax[0]])
    rong = lambda sel: float(np.ptp((P[sel] - c) @ nrm)) if sel.sum() > 3 else 0.0
    a_ = rong(t > t.max() - 0.15 * L)
    b_ = rong(t < t.min() + 0.15 * L)
    mui = ax if a_ < b_ else -ax
    huong = ("up" if mui[1] < -0.38 else ("down" if mui[1] > 0.38 else "")) + ("-" if abs(mui[1]) > 0.38 and abs(mui[0]) > 0.38 else "") +             ("left" if mui[0] < -0.38 else ("right" if mui[0] > 0.38 else ""))
    return (f"the amber crystal prism centred at about x = {c[0]:.0f}, y = {c[1]:.0f}, about {L:.0f} px long, its sharp tip pointing {huong}",
            "complete its base, hidden behind other pieces, as the prism continuing")


def prompt():
    Mp = mat_part()
    ANH1 = (f"the picture of our character (1536x1024, white background): a toad-rhino with terracotta skin, a cream jaw, a cream stone horn, "
            "an amber eye, a dark belt with stone plates, a big cluster of amber crystal prisms held over its back by the far arm with one long "
            "crystal crossing diagonally in front of the body, smaller crystals on the shoulder, back, knees and head. Hand-drawn: wobbly "
            "dark-brown ink line, crayon hatching, flat colours.")
    STY = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
           "shading, no highlights, no glow, no shadows).")
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().rstrip("\n").split("\n")
    gd = ["", f"Tờ mảnh (ảnh mẫu duy nhất = `{Wp(C0)}`): mỗi tờ giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị che."]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(C0)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION, at exactly the SAME SIZE and "
             "ANGLE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything "
             "else (leave pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the "
             "way around it: where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same "
             "style, colours and flat crayon colouring. " + STY + " Do not move, resize, rotate or redesign anything. Keep a clear white gap "
             "between the kept parts.", "", "KEEP:"]
        for i, (ten, slots, mt, kh) in enumerate(ds, 1):
            if mt is None:
                mt, kh = mo_ta_pha_le(slots[0], Mp)
            t.append(f"{i}. {mt}: {kh}.")
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(x[0] for x in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với C0 (`thu_da2_manh.py ghep`); phần bị che vẽ đủ, viền kín; T1 không còn mắt, sừng, chi, "
           "đuôi, pha lê; nền trắng tinh."]
    if not any("Tờ mảnh (ảnh mẫu duy nhất" in x for x in cu):
        ghi(hd, cu + gd)


# ---------------------------------------------------------------- cắt
def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


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


def khu_vien(rgb, mm, r=2):
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def luu_manh(A, m, ten, DATJ, nguon, alpha_them=None):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    if alpha_them is not None:
        al = al * alpha_them[y0:y1, x0:x1]
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=nguon)       # (cắt lại thì phải chạy lại `nan`)
    return x0, y0, x1, y1


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd)) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    os.makedirs(MANH, exist_ok=True)
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w"), indent=1)


THU_TU_GOC = None


def thu_tu_goc():
    global THU_TU_GOC
    if THU_TU_GOC is None:
        _, _, atts = G.nap("att_idle0.json")
        THU_TU_GOC = {a["slot"]: a["order"] for a in atts}
    return THU_TU_GOC


def chia_theo_part(A, m, slots, DATJ, nguon, Mp, CHONG=22.0, nhan=None, mo=None):
    """chia khối liền m thành slot theo part gốc gần nhất (khoảng cách tới mặt nạ part gốc, 0 nếu ở trong). Mỗi slot lấy thêm dải CHONG px;
    ở dải chồng, slot vẽ SAU (thứ tự của họ) mờ dần về mép cắt, slot vẽ TRƯỚC giữ đặc (khỏi thủng). nhan: {slot: mặt nạ ép} (vd hàm = vùng
    kem) ưu tiên trước khi chia khoảng cách."""
    ord_ = thu_tu_goc()
    D = {s: cv2.distanceTransform((~Mp[s]).astype(np.uint8), cv2.DIST_L2, 5) for s in slots}
    if nhan:
        for s, mk in nhan.items():
            D[s] = np.where(mk, 0.0, D[s] + 40.0)
            for s2 in slots:
                if s2 != s:
                    D[s2] = np.where(mk, D[s2] + 60.0, D[s2])
    St = np.stack([D[s] for s in slots])
    dmin = St.min(0)
    amin = St.argmin(0)
    od = np.array([ord_.get(s, 0) for s in slots])
    for k, s in enumerate(slots):
        vung = m & (D[s] <= dmin + CHONG)
        if not vung.any():
            print(f"  {s}: rỗng")
            continue
        sau = od[amin] < ord_.get(s, 0)
        f = np.where((D[s] > dmin) & sau, np.clip(1.0 - (D[s] - dmin) / CHONG, 0, 1), 1.0).astype(np.float32)
        if mo is not None:
            f = f * mo
        b = luu_manh(A, vung, s, DATJ, nguon, alpha_them=f)
        print(f"  {s:14s} hộp {b}")


DAU_HAT = (1000, 520)                             # điểm giữa mặt (px C0): loang vùng đầu chặn bởi nét mực
HAM_ROI = (893, 575, 1130, 705)                   # vùng hàm dưới + răng + lòng miệng ngay dưới đầu


def loang(A, hat):
    muc = (A.mean(2) < 105).astype(np.uint8)
    ff = (1 - muc).astype(np.uint8)
    msk = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(ff, msk, hat, 2)
    return ff == 2


def chia_than(A, m, DATJ, nguon, Mp):
    """khối thân liền T1 → ĐẦU (to_01: vùng loang từ giữa mặt chặn bởi nét mực, lấp lỗ, kèm viền mực và pha lê sát đầu), HÀM DƯỚI
    (xiaba_01: dải kem hàm, răng nhô lên, lòng miệng ngay dưới đầu; thịt trong miệng thuộc hàm dưới), còn lại chia shenti_01 / yao /
    bozi_01 / bozi_02 theo part gốc gần nhất. Thân lấn 24 px xuống dưới đầu và hàm, tô màu điểm thân gần nhất (khỏi lộ nét đôi, khỏi hở khi
    đầu / hàm chuyển động). xiaba_02 (hàng răng trên của họ, nằm trên xương hàm) để trống."""
    muc = A.mean(2) < 105
    dau = loang(A, DAU_HAT)
    dau = cv2.morphologyEx(dau.astype(np.uint8), cv2.MORPH_CLOSE, el(6)).astype(bool)
    cs, _ = cv2.findContours(dau.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    dau = cv2.drawContours(np.zeros((H, W), np.uint8), cs, -1, 1, -1).astype(bool)          # lấp lỗ (nét mày, nếp trong mặt)
    r, g, b = A[..., 0], A[..., 1], A[..., 2]
    amber = (r > 200) & (g > 110) & (g < 230) & (b < 135) & (r - b > 95)
    n, lab, st, _ = cv2.connectedComponentsWithStats((amber & m).astype(np.uint8), 4)
    gan_dau = cv2.dilate(dau.astype(np.uint8), el(8)).astype(bool)
    pl = np.isin(lab, [i for i in range(1, n) if (lab[gan_dau] == i).any() and st[i, 4] > 80])
    dau_full = (cv2.dilate((dau | pl).astype(np.uint8), el(10)).astype(bool) & m)     # cả viền mực đầu (~8 px), khỏi sót vệt mực bên thân
    # hàm dưới: các vùng không mực trong ROI dưới đầu
    x0, y0, x1, y1 = HAM_ROI
    roi = np.zeros((H, W), bool)
    roi[y0:y1, x0:x1] = True
    ung = m & roi & ~dau_full & ~muc
    n2, lab2, st2, cen2 = cv2.connectedComponentsWithStats(ung.astype(np.uint8), 4)
    giu = [i for i in range(1, n2) if st2[i, 4] > 40 and cen2[i][0] > 905]
    ham = np.isin(lab2, giu)
    ham_full = cv2.dilate(ham.astype(np.uint8), el(8)).astype(bool) & m & ~dau
    dau_full &= ~ham
    than = m & ~dau_full & ~ham_full
    # đáy đầu khuyết hình răng (răng thuộc hàm dưới, vẽ SAU đầu): lấp khuyết bằng màu da đầu (môi trên), viền đầu khép kín bao lồi theo đáy
    khuyet = cv2.morphologyEx(dau_full.astype(np.uint8), cv2.MORPH_CLOSE, el(22)).astype(bool) & ~dau_full & m
    A = A.copy()
    if khuyet.any():
        da = dau_full & ~muc & ~amber
        d2, lab4 = cv2.distanceTransformWithLabels((~da).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        zy2, zx2 = np.nonzero(da)
        k2 = np.clip(lab4[khuyet] - 1, 0, len(zy2) - 1)
        mau = np.median(A[zy2[k2], zx2[k2]], 0).astype(int)
        A[khuyet] = mau
        dau_full |= khuyet
    # thân lấn dưới đầu / hàm, màu điểm thân (không mực) gần nhất
    nguon_mau = than & ~muc
    d, lab3 = cv2.distanceTransformWithLabels((~nguon_mau).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(nguon_mau)
    d_ngoai = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    lan = (dau_full | ham_full) & (d <= 24) & (d_ngoai > 10)
    # tô phần lấn bằng inpaint từ điểm thân (không lấy màu đầu, hàm, mực): mịn, không sọc
    che = (~nguon_mau).astype(np.uint8) * 255                       # nguồn inpaint chỉ là điểm thân không mực
    B = cv2.inpaint(A.astype(np.uint8), che, 9, cv2.INPAINT_TELEA).astype(np.int32)
    B = np.where(lan[..., None], B, A)
    print("  to_01         hộp", luu_manh(A, dau_full, "to_01", DATJ, nguon))
    print("  xiaba_01      hộp", luu_manh(A, ham_full, "xiaba_01", DATJ, nguon))
    DATJ.pop("xiaba_02", None)
    t6 = moi_nhat("M_T6")
    if t6:                                                       # thân KHÔNG đầu, cổ vẽ đủ chỗ đầu che (tờ T6): khỏi vá, khỏi lộ vệt khi đầu ngửa
        A6 = np.asarray(Image.open(t6).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        m6 = ~nen(A6)
        n6, lab6, st6, _ = cv2.connectedComponentsWithStats(m6.astype(np.uint8), 8)
        k6 = 1 + int(np.argmax(st6[1:, 4]))
        cs6, _ = cv2.findContours((lab6 == k6).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        m6 = cv2.drawContours(np.zeros((H, W), np.uint8), cs6, -1, 1, -1).astype(bool)
        print(f"  thân từ {os.path.basename(t6)} (không đầu)")
        chia_theo_part(A6, m6, ["shenti_01", "yao", "bozi_01", "bozi_02"], DATJ, os.path.basename(t6), Mp)
        return
    mo = np.ones((H, W), np.float32)
    mo[lan] = np.clip((24.0 - d[lan]) / 16.0, 0.0, 1.0)            # phần lấn mờ dần về mép: mép (bị tô viền) không lộ khi đầu / hàm lệch
    chia_theo_part(B, than | lan, ["shenti_01", "yao", "bozi_01", "bozi_02"], DATJ, nguon, Mp, mo=mo)


def kem_mask(A, m):
    rgb = A.astype(np.float32)
    kem = (rgb[..., 0] > 205) & (rgb[..., 1] > 180) & (rgb[..., 2] > 130) & (rgb[..., 0] - rgb[..., 2] < 100)
    kem = cv2.morphologyEx((kem & m).astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)
    return kem


def cat(chi=None):
    DATJ = nap_dat()
    Mp = mat_part()
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        # gán cụm cho mảnh có phủ (mặt nạ part gốc gộp) lớn nhất, hoà thì gần tâm nhất
        vung = {ten: np.any(np.stack([Mp[s] for s in slots]), 0) for ten, slots, _, _ in ds}
        tam = {ten: np.array(np.nonzero(v)[::-1]).mean(1) for ten, v in vung.items()}
        gan = {ten: [] for ten in vung}
        for i in range(1, n):
            if st[i, 4] <= 30:
                continue
            ci = lab == i
            phu = {ten: int((ci & v).sum()) for ten, v in vung.items()}
            best = max(phu, key=phu.get)
            if phu[best] < 0.15 * st[i, 4]:
                best = min(tam, key=lambda t: np.hypot(*(cen[i] - tam[t])))
                if np.hypot(*(cen[i] - tam[best])) > 140:
                    print(f"  {nh}: bỏ cụm ({cen[i][0]:.0f}, {cen[i][1]:.0f}) {st[i, 4]} px")
                    continue
            gan[best].append(i)
        print(f"{nh} ({os.path.basename(src)}):")
        for ten, slots, _, _ in ds:
            ids = gan[ten]
            if not ids:
                print(f"  {ten:14s} KHÔNG THẤY")
                continue
            m = np.isin(lab, ids)
            cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            m = cv2.drawContours(np.zeros((H, W), np.uint8), cs, -1, 1, -1).astype(bool)
            iou = (m & vung[ten]).sum() / max(1, (m | vung[ten]).sum())
            print(f"  [{ten}] IoU với part gốc {iou:.2f}")
            if len(slots) == 1:
                b = luu_manh(A, m, slots[0], DATJ, os.path.basename(src))
                print(f"  {slots[0]:14s} hộp {b}")
            elif ten == "than":
                chia_than(A, m, DATJ, os.path.basename(src), Mp)
            else:
                chia_theo_part(A, m, slots, DATJ, os.path.basename(src), Mp)
    ghi_dat(DATJ)


# ---------------------------------------------------------------- cụm pha lê (khối "vũ khí") cắt từ C0
GAI_PHU = {"wuqi_010": ("M_T4", "all45"), "wuqi_11": ("M_T3", "all46"), "wuqi_012": (None, "all46")}
CUM_SLOT = "wuqi_01"                              # cụm chính (mọi pha lê trên all19) vẽ ở slot trước nhất của họ
LAP_SLOT = "wuqi_02"                              # lớp lấp chỗ gai phụ che cụm: slot all19 vẽ trước gai phụ (họ: thứ tự 38 < 44..46 < 47)


def cum_pha_le():
    """Tờ T3–T5 GPT chọn sai pha lê theo toạ độ, nên cụm pha lê lấy thẳng từ C0 (đúng y bố cục đã căn): mặt pha lê = cụm điểm hổ phách tách
    nhau bởi nét mực; mỗi mặt gán cho mảnh pha lê gốc phủ nó nhiều nhất. Mặt thuộc ba gai phụ (xương all45 / all46, xoay riêng trong đòn
    đánh, lúc vào sân) thành mảnh riêng (thêm bản vẽ đủ của tờ T3 / T4 nếu có); còn lại (all19 + gai lưng shenti_02/03 lẫn trong cụm) thành
    MỘT mảnh `wuqi_01` vẽ trước nhất của khối: lúc đứng y hệt C0, chỗ gai phụ lộ ra là lỗ trên mảnh cụm (gai phụ vẽ sau nó lấp vào).
    Pha lê liền trên thân, đầu (đã có trong mảnh T1), trên chân trước, đuôi (T2) không lấy."""
    DATJ = nap_dat()
    Mp = mat_part()
    A = np.asarray(Image.open(C0).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    r, g, b = A[..., 0], A[..., 1], A[..., 2]
    amber = (r > 200) & (g > 110) & (g < 230) & (b < 135) & (r - b > 95)
    muc = A.mean(2) < 110
    # mặt pha lê đã có trong mảnh T1 / T2 (pha lê liền thân, đầu, chân trước, đuôi) và pha lê đầu, gối (T3, T4): loại
    da_co = np.zeros((H, W), bool)
    for s in ("shenti_01", "to_01", "bozi_02", "bozi_01", "yao", "youdabi_01", "youxiaobi", "shouzhang", "weiba", "zuodabi"):
        if s in DATJ:
            x0, y0, _, _ = DATJ[s]["hop"]
            q = np.asarray(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA")).astype(np.int32)
            hp = (q[..., 3] > 128) & (q[..., 0] > 200) & (q[..., 1] > 110) & (q[..., 1] < 230) & (q[..., 2] < 135) & (q[..., 0] - q[..., 2] > 95)
            da_co[y0:y0 + hp.shape[0], x0:x0 + hp.shape[1]] |= hp          # chỉ điểm HỔ PHÁCH của mảnh (pha lê liền thân / chi)
    vu_khi = ["wuqi_01", "wuqi_02", "wuqi_03", "wuqi_04", "wuqi_05", "wuqi_06", "wuqi_010", "wuqi_11", "wuqi_012", "shenti_02", "shenti_03"]
    vung_vk = cv2.dilate(np.any(np.stack([Mp[s] for s in vu_khi]), 0).astype(np.uint8), el(25)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(amber.astype(np.uint8), 4)
    gan = np.full((H, W), -1, np.int32)
    ten = ["cum"] + list(GAI_PHU)
    for i in range(1, n):
        if st[i, 4] < 25:
            continue
        ci = lab == i
        if not (ci & vung_vk).any() or (ci & da_co).sum() > 0.5 * st[i, 4]:
            continue
        phu = {s: int((ci & Mp[s]).sum()) for s in vu_khi}
        best = max(phu, key=phu.get)
        if phu[best] == 0:
            continue
        gan[ci] = ten.index(best) if best in GAI_PHU else 0
    # nét mực quanh các mặt: gán cho mặt gần nhất (trong 7 px), chỉ nét mực thật (tối) và không thuộc thân / đầu đã cắt
    co = gan >= 0
    d, lab2 = cv2.distanceTransformWithLabels((~co).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(co)
    vien = muc & ~co & (d <= 7)
    k = np.clip(lab2[vien] - 1, 0, len(zy) - 1)
    gan2 = gan.copy()
    gan2[vien] = gan[zy[k], zx[k]]
    cum = gan2 == 0
    phu = gan2 > 0
    dong = cv2.morphologyEx(cum.astype(np.uint8), cv2.MORPH_CLOSE, el(14))
    csd, _ = cv2.findContours(dong, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    trong_cum = cv2.drawContours(np.zeros((H, W), np.uint8), csd, -1, 1, -1).astype(bool)
    lap = phu & trong_cum                                        # chỗ gai phụ che cụm, chỉ phần nằm TRONG hình bóng kín của cụm
    if lap.sum() < 800:                                          # lỗ quá nhỏ: không cần lớp lấp (mẩu vụn còn gây nét lơ lửng)
        lap[:] = False
        DATJ.pop(LAP_SLOT, None)
    if lap.any():                                                # LỚP LẤP riêng (slot LAP_SLOT trên all19, vẽ SAU gai phụ): đứng yên gai phụ
        nguon = cum & ~muc                                       # che nó, gai phụ xoay đi thì nó lộ ra thay cho lỗ trên mảnh cụm
        che = (~nguon).astype(np.uint8) * 255
        A_l = cv2.inpaint(A.astype(np.uint8), che, 7, cv2.INPAINT_TELEA).astype(np.int32)
        ml = cv2.dilate(lap.astype(np.uint8), el(3)).astype(bool)
        print(f"  {LAP_SLOT:10s} (lớp lấp dưới gai phụ, {int(lap.sum())} px) hộp", luu_manh(A_l, ml, LAP_SLOT, DATJ, "C0.png (inpaint chỗ gai phụ che cụm)"))
    for j, s in enumerate(ten):
        m = gan2 == j
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(2)).astype(bool)
        if not m.any():
            print(f"  {s}: rỗng")
            continue
        n4, lab4, st4, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)       # bỏ mẩu rời (nét mực lẻ) không liền khối
        lon = st4[1:, 4].max()
        m = np.isin(lab4, [q for q in range(1, n4) if st4[q, 4] >= max(150, 0.04 * lon)])
        ra = CUM_SLOT if s == "cum" else s
        Bm, mm = A.copy(), m
        if s in GAI_PHU and GAI_PHU[s][0]:                      # gai phụ: hợp thêm bản vẽ đủ của tờ (cùng chỗ) để khi xoay không cụt
            src = moi_nhat(GAI_PHU[s][0])
            if src:
                Ts = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
                fg = ~nen(Ts)
                n3, lab3, st3, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
                ids = [q for q in range(1, n3) if st3[q, 4] > 200 and ((lab3 == q) & m).sum() > 0.3 * min(st3[q, 4], m.sum())]
                if ids:
                    them = np.isin(lab3, ids) & ~m
                    Bm = np.where(them[..., None], Ts, A)
                    mm = m | them
                    print(f"  {s}: thêm {int(them.sum())} px phần bị che từ {os.path.basename(src)}")
        bx = luu_manh(Bm, mm, ra, DATJ, "C0.png (cụm pha lê)" if s == "cum" else "C0.png + tờ")
        print(f"  {ra:10s} hộp {bx}")
    ghi_dat(DATJ)


# ---------------------------------------------------------------- nắn chân sau về đúng chân rig
NAN = {"zuodatui": 42, "zuoxiaotui": 42, "youqigai": 42, "youdatui": 9, "youxiaotui": 9, "zuoqigai": 9}   # px C0, đo ở tâm bàn chân (đáy trùng)


def nan_chan():
    """C0 đặt hai chân sau lệch trái so với chân rig (chân xa 42 px, chân gần 9 px; pha lê gối theo chân): dời hộp mảnh (giữ hộp gốc ở hop0)."""
    DATJ = nap_dat()
    for s, dx in NAN.items():
        if s not in DATJ:
            continue
        h0 = DATJ[s].get("hop0", DATJ[s]["hop"])
        DATJ[s]["hop0"] = h0
        DATJ[s]["hop"] = [h0[0] + dx, h0[1], h0[2] + dx, h0[3]]
        print(f"  {s}: dời {dx} px")
    ghi_dat(DATJ)


# ---------------------------------------------------------------- mắt (cắt từ C0), lưỡi (vẽ bằng mã)
def mat():
    DATJ = nap_dat()
    Mp = mat_part()
    A = np.asarray(Image.open(C0).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    gan = cv2.dilate(np.any(np.stack([Mp["yanjing_01"], Mp["yanjing_02"]]), 0).astype(np.uint8), el(30)).astype(bool)
    vang = (A[..., 0] > 200) & (A[..., 1] > 140) & (A[..., 2] < 150) & (A[..., 0] - A[..., 2] > 70) & gan
    toi = (A.mean(2) < 95) & gan
    sang = (A.min(2) > 200) & gan
    mk = (vang | toi | sang).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mk, 8)
    nv, labv, stv, _ = cv2.connectedComponentsWithStats(vang.astype(np.uint8), 8)
    if nv < 2:
        print("không thấy tròng vàng quanh chỗ mắt")
        return
    kv = 1 + int(np.argmax(stv[1:, 4]))
    # mắt = tròng vàng + vành mực + chấm sáng dính tròng; nét mày dày dính vào thì cắt bằng vòng tròn ôm tròng
    ys, xs = np.nonzero(labv == kv)
    cx_, cy_ = xs.mean(), ys.mean()
    r = 0.5 * max(np.ptp(xs), np.ptp(ys)) + 9
    yy, xx = np.mgrid[0:H, 0:W]
    tron = (xx - cx_) ** 2 + (yy - cy_) ** 2 <= r * r
    k = int(np.bincount(lab[labv == kv]).argmax())
    tr = ((lab == k) & tron).astype(np.uint8)
    cs, _ = cv2.findContours(tr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    kin = cv2.drawContours(np.zeros_like(tr), cs, -1, 1, -1).astype(bool)
    print("yanjing_02", luu_manh(A, kin, "yanjing_02", DATJ, "C0.png (cắt thẳng)"))
    # mắt nhắm (slot thêm mat_nham trên xương mắt): lòng mắt màu da đầu, một nét mực cong võng (mí khép) + nét mí trên
    vung = cv2.dilate(kin.astype(np.uint8), el(8)).astype(bool) & ~cv2.dilate(kin.astype(np.uint8), el(3)).astype(bool)
    da = np.median(A[vung & (A.mean(2) > 100) & (A.min(2) < 230)], 0).astype(int)
    B = A.copy()
    B[kin] = da
    im = Image.fromarray(B.astype(np.uint8))
    d = ImageDraw.Draw(im)
    ys, xs = np.nonzero(kin)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    top = [(x, ys[xs == x].min()) for x in range(x0, x1 + 1) if (xs == x).any()]
    d.line([(x, y + 3) for x, y in top], fill=MUC, width=7, joint="curve")
    khep = [(x, y0 + 0.55 * (y1 - y0) + 0.18 * (y1 - y0) * np.sin(np.pi * (x - x0) / max(1, x1 - x0))) for x in range(x0 + 3, x1 - 2)]
    d.line(khep, fill=MUC, width=5, joint="curve")
    B = np.asarray(im).astype(np.int32)
    print("mat_nham", luu_manh(B, kin, "mat_nham", DATJ, "vẽ bằng mã từ yanjing_02"), "màu da", da)
    ghi_dat(DATJ)


def luoi_ve():
    """lòng miệng + lưỡi (slot shetou, như đạo cụ T5 của dạng 1 nhưng vẽ bằng mã): khối tròn dẹt nâu đỏ rất sẫm, lưỡi hồng phẳng nằm nửa dưới
    (đầu lưỡi tròn quay phải), viền mực quanh khối. Vẽ ở 420 × 190 px; rig đặt lại vào chỗ giữa hai hàm (dat_lai) nên hộp px không dùng."""
    DATJ = nap_dat()
    w, h = 420, 190
    can_ = Image.new("RGB", (w + 20, h + 20), (255, 255, 255))
    d = ImageDraw.Draw(can_)
    d.ellipse((10, 10, 10 + w, 10 + h), fill=(74, 35, 32))
    d.ellipse((60, 10 + 0.48 * h, 10 + 0.92 * w, 10 + 1.02 * h), fill=(217, 120, 122))
    d.arc((60, 10 + 0.48 * h, 10 + 0.92 * w, 10 + 1.02 * h), 180, 360, fill=MUC, width=4)
    d.line([(0.40 * w, 10 + 0.62 * h), (0.70 * w, 10 + 0.66 * h)], fill=(176, 84, 88), width=4)
    ngoai = Image.new("L", can_.size, 0)
    ImageDraw.Draw(ngoai).ellipse((10, 10, 10 + w, 10 + h), fill=255)
    can_.paste((255, 255, 255), mask=Image.eval(ngoai, lambda v: 255 - v))       # lưỡi không lòi ra ngoài lòng miệng
    d.ellipse((10, 10, 10 + w, 10 + h), outline=MUC, width=7)
    A = np.full((H, W, 3), 255, np.int32)
    x0, y0 = 50, 50
    A[y0:y0 + h + 20, x0:x0 + w + 20] = np.asarray(can_).astype(np.int32)
    m = np.zeros((H, W), bool)
    yy, xx = np.mgrid[0:h + 20, 0:w + 20]
    trong = ((xx - (10 + w / 2)) / (w / 2 + 3.5)) ** 2 + ((yy - (10 + h / 2)) / (h / 2 + 3.5)) ** 2 <= 1.0
    m[y0:y0 + h + 20, x0:x0 + w + 20] = trong
    m &= ~((A == 255).all(2))
    print("shetou", luu_manh(A, m, "shetou", DATJ, "vẽ bằng mã (lòng miệng + lưỡi)"))
    ghi_dat(DATJ)


# ---------------------------------------------------------------- ghép soi
def ghep():
    DATJ = nap_dat()
    _, _, atts = G.nap("att_idle0.json")
    thu_tu = [a["slot"] for a in sorted(atts, key=lambda a: a["order"])]
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in thu_tu:
        if s not in DATJ:
            thieu.append(s)
            continue
        x0, y0, _, _ = DATJ[s]["hop"]
        can_.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
        if s == "yanjing_02" and "mat_nham" in DATJ:
            pass
    C = np.asarray(Image.open(C0).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can_.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can_.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    can_.convert("RGB").save(os.path.join(MANH, "_ghep_to.png"))
    print(p, f"IoU hình bóng với C0 {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "c0":
        c0()
    elif cmd == "can":
        can()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "mat":
        mat()
    elif cmd == "cum":
        cum_pha_le()
    elif cmd == "nan":
        nan_chan()
    elif cmd == "luoi":
        luoi_ve()
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
