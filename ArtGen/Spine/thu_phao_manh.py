# -*- coding: utf-8 -*-
"""Thú giáp pháo (thu_phao, rig monster_3629): MẢNH theo concept C đã duyệt (inbox/thu_phao_1/tai_ve/L1_duyet.png: giáp thép bạc trắng
viền vàng kim, mũ hiệp sĩ khe chữ T mắt vàng, tai giáp dựng, thân pháo hộp bạc gờ vàng, họng tròn vành vàng có cánh, lõi mặt trời vàng, hai
cánh vàng, vảy đuôi viền vàng, vuốt vàng sẫm).

Hai loại tờ (skill pokiclash-spine-rig mục 00; memory bam-con-goc-khung-part; mẫu ky_nguyen_manh.py):
  K1–K6: mảnh GIỮ HÌNH BÓNG gốc (tấm mai, đai sống lưng, bụng, cổ, khối sau gáy, mọi khối chân, khớp, đế, 24 ngón, bốn đốt đuôi, khối tối sau
         đuôi, mặt dưới pháo): tờ = CHÍNH mảnh gốc cắt theo lưới phóng to; GPT đổi da theo concept, giữ hình bóng; NGUYÊN lưới của họ.
  R1, R2: mảnh ĐỔI DÁNG gen "đúng chỗ, đúng cỡ" trên concept (mỗi tờ vài mảnh không chồng nhau): R1 mũ (cả đầu, không tai) + thân pháo hộp;
         R2 họng pháo tròn có cánh, lõi tròn, hai cánh vàng, hai tai giáp + ỐNG NÒNG (khuất ở dáng nghỉ, vẽ ở góc trống; rig gắn cứng vào
         bone97, thò ra khỏi thân pháo khi nòng vươn ở chiêu cuối). Mảnh cứng một xương, ô 4 đỉnh (manh/moi.json, cùng `_mieng`, `_loi`).

    thu_phao_manh.py can        căn concept lên hình con gốc → mau/can.json
    thu_phao_manh.py to         dựng mọi tờ hướng dẫn + file prompt → mau/goc_K*.png, gui_gpt/thu_phao_1/luot_2_*.txt
    thu_phao_manh.py cat [tờ]   cắt ảnh về (K1..K6 / R1 / R2) → manh/<vùng>.png, manh/moi.json, tờ so manh/_so_*.png
Ảnh con gốc, mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import thu_phao as G  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
RES = 2                                   # ảnh mảnh của mình = ảnh vùng của họ × RES (atlas họ 0,5 px / đơn vị → mình 1 px / đơn vị)
GUI = os.path.join(HERE, "gui_gpt", "thu_phao_1")
CON = os.path.join(G.TAI, "L1_duyet.png")
SOI_GIAP = os.path.join(HERE, "inbox", "soi_giap_1", "tai_ve", "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
MUC = "#2E2012"

# màu đo trên concept C (k-means trên hình + trung vị ô 7 × 7)
MAU = dict(bac="#C6C9D1", bac_ben="#9BA0AB", vang="#DFAD46", vang_sam="#90692C", toi="#4C4C50", xam="#84888F", xam_toi="#64656A",
           sang="#F8C44C", sang_nhat="#EFDFA7")


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def mat_na(rgb, nguong=28):
    m = ((255 - rgb.astype(np.int16)).max(2) > nguong).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k.astype(bool)


# ================================================================ căn concept lên rig
def can():
    """tìm phép đồng dạng (tâm khung, tỉ lệ a, dời d) đưa hình con gốc (goc_ca_con) trùng hình bóng concept nhất."""
    g = mat_na(np.asarray(Image.open(os.path.join(G.MAU, "goc_ca_con.png")).convert("RGB")))
    c = mat_na(np.asarray(Image.open(CON).convert("RGB").resize((W, H))))
    k = 4
    gs = cv2.resize(g.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA)
    cs = cv2.resize(c.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA).astype(bool)
    C = np.array([W / 2, H / 2]) / k
    best = (0, 1.0, 0.0, 0.0)

    def thu(a, dx, dy):
        M = np.array([[a, 0, C[0] - a * C[0] + dx / k], [0, a, C[1] - a * C[1] + dy / k]], np.float32)
        w = cv2.warpAffine(gs, M, (W // k, H // k), flags=cv2.INTER_NEAREST).astype(bool)
        return (w & cs).sum() / max(1, (w | cs).sum())
    for a in np.arange(0.90, 1.141, 0.01):
        for dx in range(-48, 49, 4):
            for dy in range(-48, 49, 4):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    _, a0, x0, y0 = best
    for a in np.arange(a0 - 0.01, a0 + 0.0101, 0.0025):
        for dx in range(int(x0) - 4, int(x0) + 5):
            for dy in range(int(y0) - 4, int(y0) + 5):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    v, a, dx, dy = best
    gj = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    out = dict(iou=round(float(v), 4), a=float(a), dx=float(dx), dy=float(dy), s=gj["s"], cx=gj["cx"], cy=gj["cy"])
    json.dump(out, open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print("căn:", out)
    return out


def phep_can():
    """(T: thế giới dáng gốc → px concept, Ti: ngược lại, px concept / đơn vị)."""
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, a, dx, dy = j["s"], j["cx"], j["cy"], j["a"], j["dx"], j["dy"]
    C = np.array([W / 2, H / 2])

    def T(V):
        V = np.asarray(V, float).reshape(-1, 2)
        P = np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
        return C + a * (P - C) + np.array([dx, dy])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([dx, dy]) - C) / a + C
        return np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    return T, Ti, s * a


def _to_so(ims, p):
    w_ = sum(i.width + 10 for i in ims) + 10
    h_ = max(i.height for i in ims) + 20
    o = Image.new("RGB", (w_, h_), (150, 150, 150))
    x = 10
    for i in ims:
        o.paste(i, (x, 10), i)
        x += i.width + 10
    o.save(p)
    print(p)


R_CON = ("the APPROVED picture of OUR character, 1536x1024, white background: an armoured siege beast turned to the right, low on four "
         "short legs like a tortoise, covered in flat SILVER-WHITE knight armour plates with GOLD rims; a knight helm with a T-shaped visor "
         "and two yellow eyes at the lower right, two pointed armour ear guards; four silver tail scales curling down at the rear; on its "
         "back a long boxy silver cannon housing with a gold ridge and a round gold boss, two small gold wings on top, a round gold core with "
         "a sun at its rear end and a thick gold oval muzzle ring with small wings above the head. It gives the design, the colours, the ink "
         "line and the crayon hatching.")

# ================================================================ K: mảnh giữ hình bóng gốc (tờ = mảnh gốc phóng to)
_BAC = f"flat silver {MAU['bac']} on the faces turned to the viewer, darker silver {MAU['bac_ben']} on the side faces"
_VIEN = f"a GOLD rim band {MAU['vang']} (about 14 px wide) along its lower edge"
_KHONG = "NO carved spirals, no meanders, no stone texture (the spirals of image 1 are NOT kept)"


def _mo_ta(r):
    """mô tả tiếng Anh từng mảnh theo loại (tên slot của họ)."""
    if r in ("P_shenti01", "P_shenti02", "P_shenti03", "P_shenti04"):
        return f"a big ARMOUR PLATE of the back shell: {_BAC}, {_VIEN}, 2 small round gold rivets; {_KHONG}."
    if r == "P_shenti":
        return (f"the SPINE RIDGE along the top of the shell (a row of small overlapping segments): every segment flat silver {MAU['bac']}, "
                f"keep each segment line, a thin gold line {MAU['vang']} along the top edge; {_KHONG}.")
    if r in ("P_shenti08", "P_shenti07", "P_shenti09", "P_shenti06", "P_shenti05"):
        return f"DARK UNDER-ARMOUR (belly): flat dark steel {MAU['toi']}, one or two thin plate lines where image 1 has edges; {_KHONG}."
    if r.startswith("P_bozi"):
        return f"a NECK RING segment: flat dark steel {MAU['xam_toi']}, one thin plate line; {_KHONG}."
    if r == "P_tou02":
        return f"the BACK OF THE HELMET (behind the face): {_BAC}, a thin gold rim {MAU['vang']} along its lower edge; {_KHONG}."
    if r in ("P_y_qiantui14", "P_y_houtui14", "P_y_qiantui11", "P_z_qiantui11", "P_y_houtui12", "P_z_houtui09"):
        return f"a dark steel LEG JOINT: flat {MAU['toi']}, ink outline; {_KHONG}."
    if r in ("P_y_qiantui09", "P_z_qiantui13", "P_y_houtui08", "P_z_houtui12"):
        return f"the flat SOLE plate under a foot: flat dark steel {MAU['xam_toi']}; {_KHONG}."
    if r.startswith("P_pao0") and r in ("P_pao04", "P_pao05", "P_pao06", "P_pao07"):
        return f"a curved TAIL SCALE (one segment of the thick tail): {_BAC}, {_VIEN.replace('lower edge', 'lower curved edge')}; {_KHONG}."
    if r == "P_pao08":
        return f"the dark mass behind the tail scales: flat steel grey {MAU['xam_toi']}; {_KHONG}."
    if r == "P_pao03":
        return f"the UNDERSIDE of the cannon housing: flat steel grey {MAU['xam']}, one thin line; {_KHONG}."
    if r in MO_TA_PHAO:
        return MO_TA_PHAO[r]
    if r in NGON:
        return (f"a short thick TOE CLAW: flat dark gold {MAU['vang_sam']}, a lighter gold {MAU['vang']} top face where image 1 shows a top "
                "face; keep its exact outline.")
    return (f"a LEG ARMOUR BLOCK: {_BAC} (keep the face / side lines of image 1), a gold rim {MAU['vang']} along its lower edge if it is a "
            f"big block; {_KHONG}.")


# K7 (người dùng 2026-11-17: "phần súng nhìn 2D quá, bề rộng họng súng không khớp với miệng súng, sửa lại kĩ"): pháo quay về ĐÚNG khung part
# của họ (khối hộp ba phần tư: mặt trên, mặt bên, mặt trước), chỉ đổi da theo concept C. Bản R1/R2 (thân pháo hộp phẳng nhìn ngang, vòng họng
# to rời, ống nòng tự chế) bỏ.
_3D = ("KEEP THE THREE-QUARTER PERSPECTIVE of image 1 exactly: every top face, side face and front face stays where image 1 has it, with "
       f"its edge lines; top faces and faces turned to the viewer flat light silver {MAU['bac']}, side faces darker silver {MAU['bac_ben']}, "
       f"faces turned down / away steel grey {MAU['xam']}")
MO_TA_PHAO = {
    "P_pao01_1": (f"the CANNON HOUSING (the near part of a long box lying along the back, seen in three-quarter view: a long sloping TOP "
                  "FACE on the left, a RAISED BLOCK in the middle with its front face, and a lower floor face on the right): " + _3D + ". "
                  f"A GOLD ridge {MAU['vang']} (about 14 px) along the top front edges of the top face and of the raised block; on the front "
                  f"face of the raised block, instead of the carved spiral, ONE round GOLD-rimmed boss {MAU['vang']} with a silver middle; the "
                  f"wavy left end becomes the plain rounded rear end of the housing (same outline). {_KHONG}."),
    "P_pao01_2": ("the MUZZLE BLOCK at the front of the cannon, seen in three-quarter view: on the left the long BARREL (a box: its side face "
                  "and its lower face, going back into the housing), on the right the FRONT FRAME of the muzzle (a tall block with a rounded "
                  "top) whose front face holds the glowing opening: " + _3D + " for the barrel (the barrel side face darker silver "
                  f"{MAU['bac_ben']}, its lower face steel grey {MAU['xam']}, one thin GOLD band {MAU['vang']} round the barrel just behind the "
                  f"frame). The FRONT FRAME becomes a thick GOLD frame {MAU['vang']} (its thin side faces darker gold {MAU['vang_sam']}), "
                  "keeping its outer outline; the arched opening keeps EXACTLY its place, shape and size and becomes the CANNON MOUTH: a dark "
                  f"bore rim {MAU['toi']} just inside the gold frame, then the glow in TWO flat tones (golden {MAU['sang']} with ONE pale "
                  f"{MAU['sang_nhat']} inner shape), no gradient, no rays. The small tab at the top of the arch becomes a gold keystone. No "
                  f"meander pattern on the frame: plain gold. {_KHONG}."),
    "P_pao02": ("the ROUND CORE at the rear end of the cannon (a thick ring seen in three-quarter view, its thickness showing on the right): "
                f"a GOLD ring {MAU['vang']} (its thickness darker gold {MAU['vang_sam']}), inside it a dark rim and a simple golden SUN "
                f"{MAU['sang']} (a round middle with eight short rays) on a dark gold {MAU['vang_sam']} ground; the two small tabs become two "
                "small gold studs. Flat colours, no glow."),
    "P_pao01_3": f"a tiny edge piece of the cannon housing: flat light silver {MAU['bac']}, ink outline.",
    "P_pao01_4": f"a tiny edge piece of the cannon housing: flat darker silver {MAU['bac_ben']}, ink outline.",
    "P_pao01_5": f"a tiny edge piece of the cannon housing: flat darker silver {MAU['bac_ben']}, ink outline.",
}

NGON = (["P_y_qiantui0%d" % i for i in range(6)] + ["P_y_houtui0%d" % i for i in range(1, 7)] + ["P_z_qiantui0%d" % i for i in range(4, 10)]
        + ["P_z_houtui0%d" % i for i in range(2, 8)])
TO_K = {
    "K1": [[("P_shenti", 1.7), ("P_shenti04", 2.0)],
           [("P_shenti01", 1.8), ("P_shenti02", 1.8), ("P_shenti03", 1.8)]],
    "K2": [[("P_shenti08", 1.6), ("P_shenti07", 1.6)],
           [("P_shenti09", 2.0), ("P_shenti06", 3.0), ("P_shenti05", 3.0), ("P_tou02", 2.4)],
           [("P_bozi02", 2.0), ("P_bozi01", 2.0), ("P_bozi", 2.0)]],
    "K3": [[("P_y_qiantui14", 2.2), ("P_y_qiantui13", 2.2), ("P_y_qiantui12", 2.2), ("P_y_qiantui06", 2.2), ("P_z_qiantui12", 2.2),
            ("P_z_qiantui00", 2.2)],
           [("P_y_qiantui08", 2.2), ("P_y_qiantui07", 2.2), ("P_y_qiantui11", 2.2), ("P_y_qiantui10", 2.2), ("P_z_qiantui10", 2.2),
            ("P_z_qiantui01", 2.2), ("P_z_qiantui02", 2.2)],
           [("P_y_qiantui09", 2.4), ("P_z_qiantui13", 2.4), ("P_z_qiantui11", 2.4)]],
    "K4": [[("P_y_houtui14", 2.6), ("P_y_houtui13", 2.6), ("P_y_houtui11", 2.6), ("P_y_houtui00", 2.6), ("P_z_houtui00", 2.6)],
           [("P_z_houtui11", 2.6), ("P_z_houtui10", 2.6), ("P_y_houtui07", 2.6), ("P_y_houtui09", 2.6), ("P_z_houtui08", 2.6),
            ("P_z_houtui01", 2.6)],
           [("P_y_houtui08", 2.6), ("P_z_houtui12", 2.6), ("P_y_houtui10", 2.6), ("P_y_houtui12", 2.6), ("P_z_houtui09", 2.6)]],
    "K5": [[(r, 4.0) for r in NGON[0:6]], [(r, 4.0) for r in NGON[6:12]], [(r, 4.0) for r in NGON[12:18]], [(r, 4.0) for r in NGON[18:24]]],
    "K6": [[("P_pao08", 2.0), ("P_pao07", 2.2), ("P_pao06", 2.2)],
           [("P_pao05", 2.2), ("P_pao04", 2.2), ("P_pao03", 2.0)]],
    "K7": [[("P_pao01_1", 1.95), ("P_pao01_2", 1.95)],
           [("P_pao02", 2.5), ("P_pao01_3", 5.0), ("P_pao01_4", 5.0), ("P_pao01_5", 5.0)]],
}
VI_K = {"K1": "đai sống lưng + bốn tấm mai (bạc, viền vàng)",
        "K2": "bụng tối, khối tối dưới ngực, khối sau gáy, ba khúc cổ",
        "K3": "các khối chân trước gần + xa, khớp tối, đế",
        "K4": "các khối chân sau gần + xa, khớp tối, đế",
        "K5": "24 ngón (vuốt vàng sẫm)",
        "K6": "bốn vảy đuôi, khối tối sau đuôi, mặt dưới pháo",
        "K7": "PHÁO giữ khối 3D của họ: thân pháo, khối họng (nòng + khung vàng, miệng sáng), lõi vòng vàng mặt trời, ba mẩu viền"}
TA_K = {"K1": "five parts: top row a long ridge of small segments and a plate; bottom row three big shell plates",
        "K2": "nine parts: top row two big dark belly pieces; middle row a dark block, two small dark pieces and the back of a head; "
              "bottom row three neck segments",
        "K3": "sixteen parts of two front legs: armour blocks, dark joints, foot blocks and flat soles",
        "K4": "sixteen parts of two back legs: armour blocks, dark joints, foot blocks and flat soles",
        "K5": "twenty-four small toe claws drawn very big, four rows of six",
        "K6": "six parts: a tall dark mass, four curved tail lumps and the underside of a cannon",
        "K7": "six parts of a box-shaped CANNON seen in three-quarter view: top row the cannon housing and the muzzle block (a long barrel "
              "box with a tall front frame holding a glowing arched opening); bottom row a round core ring and three tiny edge pieces"}


def vung():
    """{slot / vùng: (att, ảnh part cắt theo lưới)} theo dáng gốc (att_goc)."""
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    atts = sorted([a for a in D["atts"] if a.get("region") in imgs], key=lambda a: (not a["cur"], a["order"]))
    out = {}
    for a in atts:
        out.setdefault(a["slot"], (a, G.part_goc(a)))
    for a in atts:
        out.setdefault(a["region"], out.get(a["region"]) or (a, G.part_goc(a)))
    return out


def to_k(ma):
    V = vung()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    o = {}
    cao = []
    for h_ in TO_K[ma]:
        cs = []
        for r, z in h_:
            im = V[r][1]
            big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
            cs.append((r, z, big))
        cao.append((cs, max(c[2].height for c in cs)))
    ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
    y = ke_y
    for cs, hh in cao:
        ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
        assert ke >= 8 and ke_y >= 8, (ma, ke, ke_y)
        x = ke
        for r, z, big in cs:
            y0 = y + (hh - big.height) // 2
            can_.alpha_composite(big, (x, y0))
            o[r] = dict(hop=[x, y0, big.width, big.height], z=z, vung=V[r][0]["region"])
            x += big.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, f"goc_{ma}.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_k(ma, o):
    mau = os.path.join(G.MAU, f"goc_{ma}.png")
    out = os.path.join(G.TAI, f"D_{ma}.png")
    p = os.path.join(GUI, f"luot_2_da_{ma}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: separate parts of a 2D animation puppet (a four-legged "
         f"armoured beast with a cannon on its back), each drawn alone, at the exact size and place to keep: {TA_K[ma]}. They are painted "
         "in a smooth jade-green stone digital style with carved spirals.",
         f"image 2 = {Wp(CON)}: {R_CON} Take from it the colours, the materials and the hand-drawn look. The shapes come from image 1.",
         f"image 3 = {Wp(SOI_GIAP)}: another approved hero of the same game: the hand-drawn ink and crayon style and the flat colouring of "
         "metal plates to match. Do NOT copy its design.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: RESKIN. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
         "(if the new picture were laid over image 1, every part must coincide with the old one), and its main structural lines (the edge "
         "between a front face and a side face). Do NOT merge parts, do NOT add parts, do NOT move parts. Pure white (#FFFFFF) between the "
         "parts.", "",
         f"NEW LOOK (see image 2 for the exact colours and drawing style): forged METAL armour, hand-drawn on paper: a wobbly dark-brown ink "
         f"outline ({MUC}, about 9 px) running all the way round every part exactly on its silhouette, thinner ink lines for the inner lines, "
         "and every area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. The parts of image 1 are jade-green "
         "STONE with carved spirals and soft light and dark planes in a smooth digital style: do NOT copy that stone, those spirals, that "
         "painting style or those colours; no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows: flat colour "
         "only. VERY SIMPLE: no extra details.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {_mo_ta(r)}")
    t += ["", "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."]
    ghi(p, t)
    print(p)
    return p, mau, out


def nen_trang(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def cat_k(ma):
    path = anh.to_moi_nhat(G.TAI, f"D_{ma}")
    if not path:
        print(f"{ma}: chưa gen")
        return
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    print(f"{ma}:", os.path.basename(path))
    o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
    fg = ~nen_trang(A)
    fgG = ~nen_trang(Gd)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    so = []
    for r, d in o.items():
        x, y, cw, ch = d["hop"]
        pad = 14
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
        gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
        sub = lab[y0:y1, x0:x1]
        ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
        m = np.isin(lab, ids)
        m[:y0] = m[y1:] = False
        m[:, :x0] = m[:, x1:] = False
        rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
        mm = m[y:y + ch, x:x + cw]
        al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
        vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
        sang = rgb.min(2).astype(np.float32)
        al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
        im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
        goc = V[r][1]
        tw, th = goc.width * RES, goc.height * RES
        im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        a2 = np.asarray(im2).copy()
        ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
        gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
        a2[..., 3] = np.where(gioi, a2[..., 3], 0)
        a2[..., 3] = np.where(~ag & (a2[..., :3].min(2) > 230), 0, a2[..., 3])
        thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)
        if thieu.any() and (a2[..., 3] >= 128).any():
            co = (a2[..., 3] >= 128).astype(np.uint8)
            _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys_, xs_ = np.nonzero(co)
            bang = np.zeros((lbl.max() + 1, 3), np.uint8)
            bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
            a2[thieu, :3] = bang[lbl[thieu]]
            a2[thieu, 3] = 255
        Image.fromarray(a2, "RGBA").save(os.path.join(MANH, d["vung"] + ".png"))
        b = fgG[y:y + ch, x:x + cw]
        iou = float((mm & b).sum()) / max(1, (mm | b).sum())
        ious[r] = round(iou, 3)
        so.append(Image.fromarray(a2, "RGBA"))
        print(f"  {r:14s} → {d['vung']}.png  IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, f"_so_{ma}.png"))


# ================================================================ R1, R2: mảnh đổi dáng, gen đúng chỗ, đúng cỡ trên concept
# (tên, slot của họ, xương bám, mô tả) ; ống nòng không có trên concept: vẽ ở góc trống, rig đặt bằng mã
R = {"R1": [("mu", "P_tou00", "bone34",
             "the HELMET (the whole head): the silver knight helm with the T-shaped visor slit, the TWO YELLOW EYES in the slit, the small "
             "gold crest ridge on top and its gold rims; complete it into one closed shape down to its lower edge at the neck; WITHOUT the "
             "two tall pointed ear guards (leave them out, close the helm outline where they rose)"),
            ("than_phao", "P_pao01_1", "bone30",
             "the CANNON HOUSING: the long boxy silver gun housing lying along the back, with its raised middle block, the round gold-rimmed "
             "boss on that block and the gold ridge along its top edge; complete it into one closed box: also the parts hidden behind the "
             "muzzle ring, the round core and the two wings (continue the box and its gold ridge naturally; its FRONT END under the ring is "
             "a plain flat end); WITHOUT the muzzle ring, WITHOUT the round core, WITHOUT the two wings")],
     "R2": [("mieng_phao", "P_pao01_2", "bone97",
             "the MUZZLE RING: the thick gold oval ring with the two small gold wings on its sides and the dark bore with the golden glow "
             "inside it; complete the ring all the way round (also its left side that lies against the housing); WITHOUT the housing "
             "behind it"),
            ("loi", "P_pao02", "bone30", "the ROUND CORE: the gold ring with the golden SUN inside it, a complete circle"),
            ("canh_trai", "P_pao00", "bone98", "the LEFT small gold WING standing on the rear of the housing, complete down to its base"),
            ("canh_phai", "P_pao09", "bone30", "the RIGHT small gold WING (behind the raised block), complete down to its base (also the "
                                              "part hidden behind the block)"),
            ("tai_gan", "P_erduo00", "bone36", "the NEAR (left) pointed armour EAR GUARD rising from the helm, complete down to its base"),
            ("tai_xa", "P_erduo01", "bone37", "the FAR (right) pointed armour EAR GUARD, complete down to its base (also the part hidden "
                                             "behind the helm)")]}
NONG_MO_TA = ("In the EMPTY lower-left corner of the sheet (about x = 70 to x = 560, y = 820 to y = 980, where the legs were) draw ONE "
              "extra piece that is hidden in image 1: the INNER CANNON TUBE: a plain straight silver tube lying HORIZONTALLY, about 460 px "
              f"long and 140 px tall, flat silver {MAU['bac']} with a darker {MAU['bac_ben']} lower band and ONE thin gold ring {MAU['vang']} "
              "near its right end; both ends cut STRAIGHT (flat vertical ends), dark-brown ink outline all round")
VI_R = {"R1": "mũ hiệp sĩ (cả đầu, không tai) + thân pháo hộp đủ (không họng, lõi, cánh)",
        "R2": "họng pháo tròn có cánh, lõi mặt trời, hai cánh vàng, hai tai giáp + ống nòng ở góc trống"}
TAM_R = {"R1": {"mu": (1030, 700), "than_phao": (600, 290)},
         "R2": {"mieng_phao": (975, 255), "loi": (455, 435), "canh_trai": (390, 240), "canh_phai": (555, 225), "tai_gan": (915, 560),
                "tai_xa": (1040, 535), "nong": (315, 900)}}


def prompt_r():
    ps = []
    for ma, ds in R.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: {R_CON}",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} pieces listed below, each in the SAME POSITION and at the SAME SIZE as in "
             "image 1 (if your picture were laid over image 1, every piece must sit exactly on its old place). REMOVE everything else "
             "(the body, the shell plates, the legs, the tail and every other piece) and leave pure white there. COMPLETE every piece into "
             "ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were hidden behind other things in "
             "image 1 are drawn too, continuing its shape naturally. The pieces must not touch each other.", "", "THE PIECES:"]
        t += [f"{i}. {mt}." for i, (_, _, _, mt) in enumerate(ds, 1)]
        if ma == "R2":
            t += [f"{len(ds) + 1}. {NONG_MO_TA}."]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, "
              "no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


def tach_manh(rgb, tam):
    """tách các mảnh: lòng tô chia vùng liền; mỗi vùng về mảnh có tâm gần nhất; mọi điểm của hình (cả viền) về mảnh của lòng tô gần nhất."""
    fg = ~nen_trang(rgb.astype(np.int32))
    lum = rgb.astype(np.int32).mean(2)
    trang = rgb.min(2) > 236
    r_, b_ = rgb[..., 0].astype(np.int32), rgb[..., 2].astype(np.int32)
    muc = (lum < 50) | ((lum < 62) & (r_ - b_ > 22))
    long_ = fg & ~muc & ~trang
    long_ = cv2.erode(long_.astype(np.uint8), el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(long_.astype(np.uint8), 8)
    ten = list(tam)
    C = np.array([tam[k] for k in ten], float)
    gan = np.zeros(n, np.int32) - 1
    for i in range(1, n):
        if st[i, 4] < 25:
            continue
        gan[i] = int(np.argmin(np.hypot(*(C - cen[i]).T)))
    hop = (lab > 0) & (gan[lab] >= 0)
    _, lbl = cv2.distanceTransformWithLabels((~hop).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(hop)
    bang = np.full(lbl.max() + 1, -1, np.int32)
    bang[lbl[ys, xs]] = gan[lab[ys, xs]]
    thuoc = bang[lbl]
    return {k: fg & ~trang & (thuoc == j) for j, k in enumerate(ten)}


def _nen_trong(rgb, mm):
    """giấy trắng KHÉP KÍN trong mảnh (lỗ) → trong suốt."""
    trang = (rgb.min(2) > 236) & mm
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), 4)
    lo = np.zeros_like(mm)
    for i in range(1, n):
        if st[i, 4] > 900:
            lo |= lab == i
    return lo


def _x_bone(bn):
    """trục x thế giới (đơn vị) của xương ở khung 0 idle."""
    D = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    b = next(b for b in D["bones"] if b["name"] == bn)
    v = np.array([b["a"], b["c"]], float)
    return v / np.linalg.norm(v)


# mảnh R bỏ (2026-11-17, người dùng chê pháo 2D): pháo dùng tờ K7 theo khung part của họ
BO_R = {"than_phao", "mieng_phao", "loi", "nong"}
CHINH = {}                                 # chỉnh tay sau khi ghép: {tên: dict(dx, dy, s)} px concept
NONG_DAI, NONG_SAU = 470.0, 70.0           # ống nòng: dài (đơn vị), đầu trước lùi sau tâm họng chừng ấy (nấp sau vành)


def cat_r():
    T, Ti, spx = phep_can()
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    os.makedirs(MANH, exist_ok=True)
    for ma, ds in R.items():
        path = anh.to_moi_nhat(G.TAI, f"M_{ma}")
        if not path:
            print(f"{ma}: chưa gen")
            continue
        print(f"{ma}:", os.path.basename(path))
        rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
        ms = tach_manh(rgb, TAM_R[ma])
        ds2 = list(ds) + ([("nong", "nong", "bone97", "")] if ma == "R2" else [])
        for ten, sl, bn, _ in ds2:
            if ten in BO_R:
                moi.pop(ten, None)
                continue
            mm0 = ms.get(ten)
            if mm0 is None or mm0.sum() < 50:
                print(f"  {ten}: KHÔNG thấy mảnh")
                continue
            ys, xs = np.nonzero(mm0)
            pad = 4
            x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W - 1, xs.max() + pad), min(H - 1, ys.max() + pad)
            mm = mm0[y0:y1 + 1, x0:x1 + 1].copy()
            sub = rgb[y0:y1 + 1, x0:x1 + 1]
            mm &= ~_nen_trong(sub, mm)
            al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
            rgba = np.dstack([sub, (al * 255).astype(np.uint8)])
            k = 1.0 / spx * (RES * 0.5)
            out = Image.fromarray(rgba, "RGBA").convert("RGBa")
            out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
            out.save(os.path.join(MANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
            if ten in CHINH:
                c_ = CHINH[ten]
                tam = hop.mean(0)
                hop = tam + (hop - tam) * c_.get("s", 1.0) + np.array([c_.get("dx", 0.0), c_.get("dy", 0.0)])
            if ten == "nong":
                continue                                    # đặt sau khi có họng
            goc4 = Ti(hop)
            moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=goc4.tolist(), to=ma)
            print(f"  {ten:10s} hộp {x0},{y0}–{x1},{y1}  → {ten}.png {out.size}  (thay {sl}, xương {bn})")
            if ten == "mieng_phao":                         # tâm lòng họng: vùng vàng sáng
                s_ = sub.astype(np.int32)
                vang = mm & (s_[..., 0] > 200) & (s_[..., 1] > 150) & (s_[..., 2] < 170)
                vy, vx = np.nonzero(vang)
                c = np.array([vx.mean() + x0, vy.mean() + y0]) if len(vx) > 30 else hop.mean(0)
                moi["_mieng"] = dict(the_gioi=Ti(c)[0].tolist(), px=c.tolist())
                moi["_mieng_cao"] = dict(don_vi=float((y1 - y0) / spx))
                print(f"    tâm họng px {c.round(1)}")
            if ten == "loi":
                c = hop.mean(0)
                moi["_loi"] = dict(the_gioi=Ti(c)[0].tolist(), px=c.tolist())
        # ống nòng: cứng trên bone97, trục theo trục x của bone97, đầu trước nấp sau vành họng, thân chạy lùi vào trong thân pháo
        if ma == "R2" and "nong" not in BO_R and os.path.exists(os.path.join(MANH, "nong.png")) and "_mieng" in moi:
            ax = _x_bone("bone97")
            up = np.array([-ax[1], ax[0]])
            F = np.array(moi["_mieng"]["the_gioi"]) - ax * NONG_SAU
            B = F - ax * NONG_DAI
            im = Image.open(os.path.join(MANH, "nong.png"))
            h_ = 0.5 * moi["_mieng_cao"]["don_vi"]           # nửa chiều cao vành họng: nòng to, đọc rõ khi thò ra
            goc4 = np.array([B + up * h_ / 2, F + up * h_ / 2, F - up * h_ / 2, B - up * h_ / 2])
            moi["nong"] = dict(slot="nong", xuong="bone97", the_gioi=goc4.tolist(), to=ma)
            print(f"  nong       dài {NONG_DAI:.0f}, cao {h_:.0f} đơn vị, trục bone97 {ax.round(3)}")
    json.dump(moi, open(pj, "w"), indent=1)


# ================================================================ hướng dẫn
def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh theo concept C đã duyệt (2026-11-17)", "",
          "Hai loại tờ (Claude tự gen và tự cắt; người dùng không cần làm gì). Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, p, rs, vi in ps:
        gd += [f"### {ten}", "", vi, "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {v} |" for i, (r, v) in enumerate(rs, 1)]
        gd += [""]
    gd += ["Kiểm: hình bóng trùng tờ hướng dẫn; không còn hoa văn xoắn đá; mũ, thân pháo, họng, lõi, cánh, tai đúng chỗ, đúng cỡ như concept, "
           "vẽ đủ phần khuất; ống nòng nằm ngang ở góc trống; tô phẳng; nền trắng. Cắt: `py -3 -I ArtGen/Spine/thu_phao_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    ps = []
    for ma in TO_K:
        o = to_k(ma)
        p, gd, out = prompt_k(ma, o)
        ps.append((f"Tờ mảnh giữ hình bóng {ma}", p, [(gd, f"Mảnh gốc cắt theo lưới, phóng to: {VI_K[ma]}"), (CON, "Concept C"),
                                                     (SOI_GIAP, "Sói giáp sắt: chỉ lấy nét, cách tô kim loại")], f"{VI_K[ma]} → `{Wp(out)}`"))
    for ma, p, out in prompt_r():
        ps.append((f"Tờ mảnh đổi dáng {ma}", p, [(CON, "Concept C đã duyệt")], f"{VI_R[ma]} → `{Wp(out)}`"))
    huong_dan(ps)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ma in TO_K:
            if chi in ("", ma):
                cat_k(ma)
        if chi in ("", "R1", "R2", "R"):
            cat_r()
    else:
        print(__doc__)
