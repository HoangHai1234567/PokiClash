# -*- coding: utf-8 -*-
"""Robot hủy diệt cổ đại (robot_co, rig monster_3613): MẢNH theo concept C đã duyệt (inbox/robot_co_1/tai_ve/L1_duyet.png: sắt cổ gỉ sét, mũ
vòm một vây, mặt nạ vuông hàm lưới, mỗi vai hai ống xả, giáp tán đinh, dải da, mắt hổ phách).

Hai loại mảnh (skill pokiclash-spine-rig mục 00, 23; memory reskin-theo-part-goc). Con này gồm các tấm giáp rời có viền kín (như con gốc),
không có bề mặt nối liền nên không cần tờ thân liền.
  K1..K4: mảnh giữ HÌNH BÓNG GỐC (tờ = chính mảnh gốc cắt theo lưới, phóng to; GPT đổi da theo concept): giáp vai lớp sau + mép + giáp cổ |
          hai giáp ngực, lõi tên lửa (đủ đạn / ống rỗng), hai cẳng tay | hai chân, ngón chân, bốn dải vải | 12 đốt ngón tay.
  R1..R3: mảnh ĐỔI DÁNG, mảnh cứng một xương, gen "đúng chỗ, đúng cỡ" trên concept: thân (mũ vòm + vây, mặt trơn có MẮT, cổ, thân dưới;
          tờ hướng dẫn hình bóng vì phần lớn bị che) | mặt nạ (lỗ tròn quanh mắt), giáp vai trước trái / phải | cụm ống xả trái / phải (thay
          cụm sừng + bắp tay của họ). Toạ độ concept → thế giới dáng gốc qua phép căn.

    robot_co_manh.py can        căn concept lên hình con gốc (phép đồng dạng khớp hình bóng nhất) → mau/can.json
    robot_co_manh.py to         dựng mọi tờ hướng dẫn + file prompt → mau/goc_K*.png, mau/huong_than.png, gui_gpt/robot_co_1/luot_2_*.txt
    robot_co_manh.py cat [K|R]  cắt ảnh về → manh/<vùng>.png, manh/moi.json (mảnh đổi dáng), tờ so manh/_so_*.png
Ảnh con gốc, mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import robot_co as G  # noqa: E402
from quai.soi import _tris  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
RES = 2                                   # ảnh mảnh của mình = ảnh vùng của họ × RES (atlas họ 0,5 px / đơn vị → mình 1 px / đơn vị)
GUI = os.path.join(HERE, "gui_gpt", "robot_co_1")
CON = os.path.join(G.TAI, "L1_duyet.png")
SOI_GIAP = os.path.join(HERE, "inbox", "soi_giap_1", "tai_ve", "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
INK = (43, 33, 24)
MUC = "#2B2118"

# màu đo trên concept C (trung vị ô 7 × 7)
MAU = dict(giap="#6A6D72", giap_sang="#8E9196", giap_toi="#4A4C51", ri="#B15A2E", sat_toi="#3B3A3D", da="#70462F", dinh="#A3A6AB",
           mat="#E8A33F")
MO_TA_CON = ("a heavy ancient war robot seen from the front, made of gunmetal iron with flat rust patches: a dome helmet with one tall "
             "flat fin, a square visor with ONE round amber eye and a grille of slots under it, two short exhaust pipes on each shoulder, "
             "big riveted shoulder pads, two riveted chest plates meeting round a small amber light, dark brown leather straps at the "
             "waist, huge riveted barrel forearms with amber-ringed fist sockets, three thick dark fingers on each hand resting on the "
             "ground, short dark legs with an iron spike on top")


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
    for a in np.arange(1.00, 1.221, 0.01):                 # GPT vẽ concept C to hơn con gốc ~13 %
        for dx in range(-120, 121, 6):
            for dy in range(-120, 121, 6):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    _, a0, x0, y0 = best
    for a in np.arange(a0 - 0.01, a0 + 0.0101, 0.0025):
        for dx in range(int(x0) - 6, int(x0) + 7, 2):
            for dy in range(int(y0) - 6, int(y0) + 7, 2):
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


_CK = {}


def lop_goc():
    """{slot: (att, mặt nạ bool trên khung concept)} các hình đang bật ở khung 0 idle, theo thứ tự vẽ; + bản đồ slot trên cùng."""
    if "lop" in _CK:
        return _CK["lop"]
    T, _, _ = phep_can()
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    lop = {}
    top = np.full((H, W), -1, np.int32)
    for k, a in enumerate(atts):
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        m = np.asarray(lay)[..., 3] > 110
        lop[a["slot"]] = (a, m)
        top[m] = k
    _CK["lop"] = (lop, top, [a["slot"] for a in atts])
    return _CK["lop"]


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


# ================================================================ K: mảnh giữ hình bóng gốc (tờ = mảnh gốc phóng to)
TO_K = {
    "K1": [[("P_shouR1_4", 2.4), ("P_shouR1_2", 2.4), ("P_jianjiaR", 2.4), ("P_jianjiaL", 2.4), ("P_shouL1_3", 2.4)]],
    "K2": [[("P_xiongjiaR", 2.3), ("P_xiongjiaL", 2.3), ("P_wuqi1", 2.3), ("P_wuqi2", 2.3)],
           [("P_shouR2_1", 2.3), ("P_shouL2_1", 2.3)]],
    "K3": [[("P_shouR2_2", 2.2), ("P_shouR2_22", 2.2), ("P_shouL2_22", 2.2), ("P_shouL2_2", 2.2)],
           [("P_butiao4", 2.2), ("P_butiao1", 2.2), ("P_butiao2", 2.2), ("P_butiao3", 2.2)]],
    "K4": [[(f"P_shouR3_{i}{j}", 4.0) for i in (1, 2, 3) for j in ("a", "b")],
           [(f"P_shouL3_{i}{j}", 4.0) for i in (1, 2, 3) for j in ("a", "b")]],
    # người dùng 2026-11-16: "walk tay phải đung đưa bị lỗi": khối bắp tay phải hình do GPT vẽ (cụm ống xả R3) ngắn hơn bắp tay gốc → hở giữa
    # vai và cẳng tay khi tay vung; ống xả quay theo bắp tay. Bắp tay phải làm lại theo HÌNH BÓNG GỐC (bỏ sừng), ống xả tách ra gắn xương vai.
    "K5": [[("P_shouL1_2", 3.2)]],
    # người dùng 2026-11-16 "tay vẫn lỗi": bắp tay máy ống lồng (ống bọc + cần pít-tông) tay phải hình; hình bóng tự dựng (TU_CHE)
    "K6": [[("tay_may_ong", 2.6), ("tay_may_can", 2.6)]],
}
# hình bóng tự dựng (không có trong rig của họ), cỡ 0,5 px / đơn vị như ảnh vùng của họ: (rộng, dài) đơn vị rig. Khớp robot_co_rig.them_tay_may:
# ống bọc 150 × (0,78 L + 40), cần 96 × (0,60 L + 34), L = 282 (vai → khuỷu tay phải hình ở dáng gốc)
L_TAY = 282.1
TU_CHE = {"tay_may_ong": (150.0, 0.78 * L_TAY + 40.0), "tay_may_can": (96.0, 0.60 * L_TAY + 34.0)}
# mở hình bóng (bỏ mũi nhọn): mũi gai trên đỉnh lớp sau giáp vai trái của họ (giáp vai trước của mình tròn, không gai)
MO = {"P_shouR1_4": 13}
# bỏ SỪNG khỏi cụm sừng + bắp tay của họ (cụm tím sẫm chạm mép trên ảnh vùng), giữ khối bắp tay + nón dưới
BO_SUNG = ("P_shouL1_2",)
VI_K = {"K6": "bắp tay máy tay phải hình: ống bọc thép (hai đai đinh) + cần pít-tông sắt sẫm (hình bóng tự dựng)",
        "K5": "khối bắp tay phải hình (hình bóng gốc, bỏ sừng): sắt sẫm, tấm giáp thép, hai gai",
        "K1": "giáp vai lớp sau trái / phải, mép giáp vai trái, hai giáp cổ nhỏ",
        "K2": "hai giáp ngực, lõi tên lửa (đủ đạn + ống rỗng), hai cẳng tay",
        "K3": "hai chân, hai cặp ngón chân, bốn dải vải → dải da",
        "K4": "12 đốt ngón tay (ba ngón mỗi tay, mỗi ngón hai đốt)"}
TOM_K = {"K1": "five armour parts: the inner (back) face of the left shoulder pad, a thin edge strip of it, two small collar plates, the "
               "inner (back) face of the right shoulder pad",
         "K2": "top row: the left chest plate, the right chest plate, the missile pod full of missiles, the same missile pod empty; bottom "
               "row: the left forearm and the right forearm (huge round barrel shells, each ending in a round fist socket)",
         "K3": "top row: the left leg, two small toes of the left foot, two small toes of the right foot, the right leg; bottom row: four "
               "cloth strips that hang from the waist (the middle one wide)",
         "K4": "twelve finger segments drawn very big: top row the six segments of the left hand, bottom row the six segments of the right "
               "hand",
         "K5": "ONE part drawn big: the right UPPER-ARM BLOCK (a rounded armoured block that links the shoulder to the forearm, with two small "
               "cones at its lower end)",
         "K6": "TWO plain light grey shapes drawn big, both standing upright: on the left a thick rounded-end cylinder (the SLEEVE of a "
               "robot's telescopic upper arm), on the right a narrower rounded-end rod (the PISTON that slides out of that sleeve)"}
_M = MAU
MO_TA_K = {
    "P_shouR1_4": f"the INNER (back) FACE of the LEFT SHOULDER PAD (seen when the pad swings open): dark gunmetal {_M['giap_toi']}, a light "
                  f"gunmetal {_M['giap_sang']} rim along its curved outer edge, two round rivets {_M['dinh']}; plain otherwise.",
    "P_shouR1_2": f"a THIN EDGE STRIP of the left shoulder pad (its side face): light gunmetal {_M['giap_sang']}, plain.",
    "P_jianjiaR": f"a SMALL COLLAR PLATE at the left side of the neck (mostly hidden): dark gunmetal {_M['giap_toi']}, one rim line.",
    "P_jianjiaL": f"a SMALL COLLAR PLATE at the right side of the neck: dark gunmetal {_M['giap_toi']}, one rim line.",
    "P_shouL1_3": f"the INNER (back) FACE of the RIGHT SHOULDER PAD: dark gunmetal {_M['giap_toi']}, a light gunmetal {_M['giap_sang']} rim "
                  f"along its curved outer edge, two round rivets {_M['dinh']}.",
    "P_xiongjiaR": f"the LEFT CHEST PLATE (a thick curved plate; its inner end, on the right, is cut in a half circle round the chest "
                   f"light): gunmetal {_M['giap']} with one or two flat rust patches {_M['ri']}, a raised rim of light gunmetal "
                   f"{_M['giap_sang']} along its inner curved edge, three big round rivets {_M['dinh']} in a row; the dark part along the "
                   f"half-circle cut very dark iron {_M['sat_toi']}. Remove the engraved pattern of image 1.",
    "P_xiongjiaL": "the RIGHT CHEST PLATE: the same design as the left chest plate, mirrored (its inner end, on the left, cut in a half "
                   "circle).",
    "P_wuqi1": f"the MISSILE POD seen from the front: a dark iron {_M['sat_toi']} hexagon frame with SEVEN round tubes (one in the middle, "
               f"six around it), each tube holding the nose of a missile: an amber {_M['mat']} round tip inside a thin gunmetal ring. "
               "Keep the seven tubes exactly where they are.",
    "P_wuqi2": f"the SAME MISSILE POD after firing: the same dark iron hexagon frame and the same seven tubes at the same places, but every "
               f"tube EMPTY: a round very dark hole {_M['sat_toi']} with a thin gunmetal {_M['giap']} ring (no amber).",
    "P_shouR2_1": f"the LEFT FOREARM (a huge round barrel-shaped shell; its round end at the lower right is the FIST SOCKET): gunmetal "
                  f"{_M['giap']} with two flat rust patches {_M['ri']} and TWO RIVETED BANDS round it (light gunmetal {_M['giap_sang']} "
                  f"bands with round rivets {_M['dinh']}); the socket: a very dark iron {_M['sat_toi']} disc with an amber {_M['mat']} ring "
                  "in it; the small pointed cone at its top left becomes a short dark iron spike.",
    "P_shouL2_1": "the RIGHT FOREARM: the same design as the left forearm (its fist socket at the lower left, amber ring, two riveted "
                  "bands, rust patches; the small cone at its top right a short dark iron spike).",
    "P_shouR2_2": f"the LEFT LEG (a short thick upright cylinder): very dark iron {_M['sat_toi']}, with a gunmetal {_M['giap']} armour plate "
                  f"wrapped round its outer (left) side (light rim line, two rivets); the red cone on its top becomes a short conical "
                  "dark iron SPIKE.",
    "P_shouR2_22": f"TWO SMALL ROUND TOES of the left foot: very dark iron {_M['sat_toi']}.",
    "P_shouL2_22": f"TWO SMALL ROUND TOES of the right foot: very dark iron {_M['sat_toi']}.",
    "P_shouL2_2": "the RIGHT LEG: the same design as the left leg (the gunmetal plate on its outer, right side; a short dark iron spike on "
                  "its top).",
    "P_butiao4": f"a narrow LEATHER STRAP hanging down: flat dark brown leather {_M['da']}, one round iron rivet {_M['dinh']} near its top, "
                 "its lower end torn. Remove the golden circuit lines of image 1.",
    "P_butiao1": "another narrow LEATHER STRAP: the same.",
    "P_butiao2": f"the wide middle LEATHER APRON: flat dark brown leather {_M['da']} divided into three straps by two thin ink lines, a row of "
                 f"three round iron rivets {_M['dinh']} along its top, its lower end torn. Remove the golden circuit lines of image 1.",
    "P_butiao3": "another narrow LEATHER STRAP: the same as the first narrow strap.",
}
MO_TA_K["P_shouL1_2"] = (f"the RIGHT UPPER-ARM BLOCK (it links the right shoulder to the forearm): very dark iron {_M['sat_toi']}; the big pale "
                         f"sand-coloured plate on it becomes a gunmetal {_M['giap']} armour plate with a light gunmetal {_M['giap_sang']} rim "
                         f"line, two round rivets {_M['dinh']} and one flat rust patch {_M['ri']}; the two red cones at its lower end become "
                         "two short conical dark iron SPIKES. The top edge is a clean closed rounded edge (nothing sticks out of it).")
MO_TA_K["tay_may_ong"] = (f"the upper-arm SLEEVE: an upright thick metal CYLINDER seen from the side, gunmetal {_M['giap']} with one flat rust "
                          f"patch {_M['ri']}, TWO riveted BANDS (light gunmetal {_M['giap_sang']} with small round rivets {_M['dinh']}) going "
                          "across it, one near the top end and one near the bottom end, both ends rounded; keep the silhouette exactly.")
MO_TA_K["tay_may_can"] = (f"the PISTON ROD: an upright narrower metal rod, very dark iron {_M['sat_toi']}, one thin light gunmetal "
                          f"{_M['giap_sang']} ring going across it near its middle, a thin light steel line along its length, both ends "
                          "rounded; keep the silhouette exactly.")
for i in (1, 2, 3):
    for j in ("a", "b"):
        MO_TA_K[f"P_shouR3_{i}{j}"] = (f"a FINGER SEGMENT (a short thick rounded block): very dark iron {_M['sat_toi']}, one small light "
                                       f"gunmetal {_M['giap_sang']} band line; keep its silhouette.")
        MO_TA_K[f"P_shouL3_{i}{j}"] = "a FINGER SEGMENT: the same."


def vung():
    """{slot hoặc vùng: (att, ảnh part cắt theo lưới)} theo dáng gốc (att_goc)."""
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    AG = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in AG["atts"]:                                  # cả hình không bật mặc định (lõi ống rỗng P_wuqi2): nap() chỉ giữ hình đang bật
        if a.get("region") not in imgs:
            continue
        out.setdefault(a["region"], (a, G.part_goc(a)))
        out.setdefault(a["slot"], (a, G.part_goc(a)))
    for ten, (rong, dai) in TU_CHE.items():               # hình bóng tự dựng: ống bo tròn hai đầu, xám nhạt, viền sẫm (0,5 px / đơn vị)
        w_, h_ = int(round(rong * 0.5)), int(round(dai * 0.5))
        ss = 4
        im = Image.new("RGBA", (w_ * ss, h_ * ss), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle([2 * ss, 2 * ss, w_ * ss - 2 * ss, h_ * ss - 2 * ss], radius=int(w_ * ss * 0.34),
                                             fill=(196, 198, 202, 255), outline=(60, 50, 40, 255), width=2 * ss)
        out[ten] = ({"region": ten}, im.resize((w_, h_), Image.LANCZOS))
    return out


def _mo(im, r):
    """gọt hình bóng: bỏ mũi nhọn (phép mở, MO) hoặc bỏ sừng (BO_SUNG: cụm tím sẫm chạm mép trên), giữ phần liền lớn nhất."""
    if r not in MO and r not in BO_SUNG:
        return im
    A = np.asarray(im).copy()
    m = (A[..., 3] > 60).astype(np.uint8)
    if r in MO:
        mo = cv2.morphologyEx(m, cv2.MORPH_OPEN, el(MO[r]))
        mo = cv2.dilate(mo, el(1)) & m
    else:
        B = A.astype(int)
        lum = B[..., :3].mean(2)
        tim = (m > 0) & (lum > 40) & (lum < 115) & (B[..., 2] >= B[..., 0] - 2) & (B[..., 2] > B[..., 1])
        tim = cv2.erode(tim.astype(np.uint8), el(1))
        n, lab, st, _ = cv2.connectedComponentsWithStats(tim, 8)
        sung = np.zeros_like(m)
        for i in range(1, n):
            if st[i, 1] <= 8 and st[i, 4] > 200:                  # chạm mép trên ảnh vùng = sừng
                sung |= (lab == i).astype(np.uint8)
        sung = cv2.dilate(sung, el(4))                             # cả viền mực của sừng
        mo = m & (1 - sung)
        n, lab, st, _ = cv2.connectedComponentsWithStats(mo, 8)
        if n > 1:
            mo = (lab == 1 + int(np.argmax(st[1:, 4]))).astype(np.uint8)
        mo = cv2.morphologyEx(mo, cv2.MORPH_OPEN, el(2))
    A[..., 3] = (A[..., 3] * mo).astype(np.uint8)
    return Image.fromarray(A, "RGBA")


def to_k(ten):
    V = vung()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    o = {}
    cao = []
    for h_ in TO_K[ten]:
        cs = []
        for r, z in h_:
            im = _mo(V[r][1], r)
            big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
            cs.append((r, z, big))
        cao.append((cs, max(c[2].height for c in cs)))
    ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
    y = ke_y
    for cs, hh in cao:
        ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
        assert ke > 12 and ke_y > 12, (ten, ke, ke_y)
        x = ke
        for r, z, big in cs:
            y0 = y + (hh - big.height) // 2
            can_.alpha_composite(big, (x, y0))
            o[r] = dict(hop=[x, y0, big.width, big.height], z=z, vung=V[r][0]["region"])
            x += big.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, f"goc_{ten}.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_k(ten, o):
    mau = os.path.join(G.MAU, f"goc_{ten}.png")
    out = os.path.join(G.TAI, f"D_{ten}.png")
    p = os.path.join(GUI, f"luot_2_da_{ten}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: {TOM_K[ten]} of a 2D animation puppet (a big ancient robot), "
         "each drawn alone, at the exact size and place to keep. They are painted in a smooth digital style with sand-gold, brown and "
         "purple colours, weathering stains and red gems.",
         f"image 2 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: {MO_TA_CON}. Take from it the "
         "colours, the materials and the hand-drawn look (wobbly brown ink line, crayon hatching, flat colour). The shapes come from "
         "image 1.",
         f"image 3 = {Wp(SOI_GIAP)}: another approved hero of the same game: the hand-drawn ink and crayon style to match. Do NOT copy "
         "its design.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ten}_2.png, D_{ten}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: RESKIN. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
         "(if the new picture were laid over image 1, every part must coincide with the old one). Do NOT merge parts, do NOT add parts, "
         "do NOT move parts. Pure white (#FFFFFF) between the parts.", "",
         f"NEW LOOK (see image 2 for the exact colours and drawing style): hand-drawn on paper: a wobbly dark-brown ink outline ({MUC}, "
         "about 9 px) running all the way round every part exactly on its silhouette, thinner ink lines for the inner lines, and every "
         "area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. Do NOT copy the painting style of image 1 "
         "(no sand-gold, no purple, no stains, no engraved patterns, no red gems); no shading, no highlights, no white shine streaks, no "
         "gradients, no glow, no shadows: flat colour only. VERY SIMPLE: no extra details.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {MO_TA_K[r]}")
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


def cat_k(ten):
    path = anh.to_moi_nhat(G.TAI, f"D_{ten}")
    if not path:
        print(f"{ten}: chưa gen")
        return
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    print(f"{ten}:", os.path.basename(path))
    o = json.load(open(os.path.join(G.MAU, f"goc_{ten}.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ten}.png")).convert("RGB")).astype(np.int32)
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
        goc = _mo(V[r][1], r)
        tw, th = goc.width * RES, goc.height * RES
        im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        a2 = np.asarray(im2).copy()
        ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
        gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
        a2[..., 3] = np.where(gioi, a2[..., 3], 0)
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
        print(f"  {r:12s} → {d['vung']}.png  IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, f"_so_{ten}.png"))


# ================================================================ R: mảnh đổi dáng, gen đúng chỗ, đúng cỡ trên concept
# mỗi mảnh: (tên, slot của họ mà nó thay, xương bám, tả tiếng Anh)
R = {
    "R1": [("than", "P_shenti", "bone4",
            "the BODY of the robot, filling EXACTLY the light grey shape of image 2 (same outline, same place): at the top the rounded DOME "
            f"HELMET with its tall flat FIN (gunmetal {MAU['giap']}, light gunmetal fin, the rust patches of image 1), complete; under the "
            f"dome the FACE AREA: plain very dark iron {MAU['sat_toi']} with the ONE round EYE exactly where the eye is in image 1 (flat "
            f"amber {MAU['mat']} inside its ink outline, one small white dot, a thin dark ring round it); the short NECK with its row of "
            f"small round holes; under the neck the upper chest as a plain gunmetal COLLAR plate (it is hidden behind the two chest plates "
            f"in image 1: draw it plain, one rim line, no rivets); then the big ROUND LOWER BODY in very dark iron {MAU['sat_toi']} with the "
            "two pale grey curved plates on its sides as in image 1, going down to the rounded bottom of the grey shape (hidden behind "
            "the leather straps in image 1: continue the dark body). WITHOUT the square visor (face plate) and its grille, WITHOUT the "
            "chest plates, the shoulder pads, the pipes, the arms, the hands, the straps and the legs")],
    "R2": [("mat_na", "P_tou1", "bone39",
            f"the FACE PLATE: the square light gunmetal {MAU['giap_sang']} VISOR on the front of the head with its grille of slots under "
            "the eye, complete; where the eye is, the visor has a round HOLE: leave the inside of the eye ring PURE WHITE (the eye is on "
            "another part and shows through the hole); keep the dark ink ring round the hole"),
           ("vai_trai", "P_shouR1_1", "bone38",
            "the BIG LEFT SHOULDER PAD (the rounded riveted gunmetal plate on the viewer's left, with its rust patches, its light rim and "
            "its row of round rivets), complete: the parts hidden behind the pipes are drawn too; WITHOUT the pipes, WITHOUT the small "
            "spikes under it"),
           ("vai_phai", "P_shouL1_1", "rotate_02",
            "the BIG RIGHT SHOULDER PAD (the rounded riveted gunmetal plate on the viewer's right), complete: the parts hidden behind the "
            "pipes are drawn too; WITHOUT the pipes, WITHOUT the small spikes under it")],
    "R3": [("ong_trai", "P_shouR1_3", "bone28",
            f"the LEFT SHOULDER UNIT: the TWO short EXHAUST PIPES on the viewer's left shoulder (dark iron {MAU['sat_toi']} tubes, the "
            "taller one behind, the shorter one in front, each with a thick ring round its open top and a dark inside), complete down to "
            f"their base, AND under them the UPPER-ARM BLOCK that is hidden behind the left shoulder pad in image 1: draw it complete as a "
            f"plain rounded very dark iron block (about as wide as the shoulder pad, going down to just under the pad), with the two short "
            "dark iron SPIKES that stick out under the shoulder pad at its lower left. One single closed piece"),
           ("ong_phai", "P_shouL1_2", "rotate_01",
            "the RIGHT SHOULDER UNIT: the TWO short EXHAUST PIPES on the viewer's right shoulder, complete down to their base, AND under "
            "them the plain rounded very dark iron UPPER-ARM BLOCK hidden behind the right shoulder pad (draw it complete, going down to "
            "just under the pad), with the two short dark iron SPIKES that stick out under the right shoulder pad. One single closed "
            "piece")],
}
VI_R = {"R1": "thân: mũ vòm + vây, mặt trơn có MẮT hổ phách, cổ lỗ tròn, cổ áo (khuất sau giáp ngực), thân dưới tròn sẫm (theo hình bóng tờ 2)",
        "R2": "mặt nạ vuông hàm lưới (lỗ tròn quanh mắt), giáp vai trước trái, giáp vai trước phải",
        "R3": "cụm ống xả trái, cụm ống xả phải (mỗi cụm: hai ống + khối bắp tay sẫm khuất sau giáp vai + hai gai dưới vai)"}


def huong_than():
    """tờ hướng dẫn hình bóng THÂN (khung concept): hình bóng thân của họ bỏ chỏm chữ T (phần trên cổ) ∪ khối đầu của concept (mũ vòm, vây,
    mặt nạ). Xám nhạt, viền sẫm. → mau/huong_than.png"""
    lop, _, _ = lop_goc()
    m_than = lop["P_shenti"][1].copy()
    m_mat = lop["P_tou1"][1]
    ys, xs = np.nonzero(m_mat)
    y_cat = int(np.percentile(ys, 70))                    # bỏ chỏm chữ T: phần thân của họ cao hơn 70 % chiều cao mặt nạ của họ
    m_than[:y_cat] = False
    Cn = np.asarray(Image.open(CON).convert("RGB").resize((W, H), Image.LANCZOS))
    cm = mat_na(Cn)
    # khối đầu của concept: trong hộp giữa hai cụm ống xả, phía trên mép trên hai giáp ngực
    hop = np.zeros((H, W), bool)
    hop[30:345, 605:935] = True
    dau = cm & hop
    n, lab, st, _ = cv2.connectedComponentsWithStats(dau.astype(np.uint8), 8)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, 4]))
        dau = lab == k
    m = cv2.morphologyEx((m_than | dau).astype(np.uint8), cv2.MORPH_CLOSE, el(9)).astype(bool)
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m2 = np.zeros((H, W), np.uint8)
    cv2.drawContours(m2, cs, -1, 1, -1)
    g = np.full((H, W, 3), 255, np.uint8)
    g[m2.astype(bool)] = (214, 214, 214)
    cv2.drawContours(g, cs, -1, INK, 6)
    p = os.path.join(G.MAU, "huong_than.png")
    Image.fromarray(g).save(p)
    np.save(os.path.join(G.MAU, "huong_than.npy"), m2.astype(bool))
    print(p, f"cắt chỏm ở y {y_cat}")
    return p


def prompt_r():
    ps = []
    for ma, ds in R.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: {MO_TA_CON}."]
        if ma == "R1":
            t.append(f"image 2 = {Wp(os.path.join(G.MAU, 'huong_than.png'))}: SHAPE GUIDE, 1536x1024, white background: ONE light grey "
                     "shape with a dark outline, laid on the same canvas as image 1: the exact outline and place of the robot's BODY part "
                     "(the dome helmet and fin at the top, the neck, the collar and the big round lower body that are mostly hidden behind "
                     "other parts in image 1).")
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              f"TASK: redraw image 1 with ONLY the {len(ds)} piece{'s' if len(ds) > 1 else ''} listed below, each in the SAME POSITION and "
              "at the SAME SIZE as in image 1 (if your picture were laid over image 1, every piece must sit exactly on its old place). "
              "REMOVE everything else and leave pure white there. COMPLETE every piece into ONE CLOSED SHAPE with the ink outline all the "
              "way round: the parts of a piece that were hidden behind other things in image 1 are drawn too, continuing its shape "
              "naturally." + (" The pieces stay separate from each other (a little white gap between them is fine, do not merge them)."
                              if len(ds) > 1 else ""), "",
              "THE PIECE" + ("S:" if len(ds) > 1 else ":")]
        t += [f"{i}. {mt}." for i, (_, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, "
              "no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


def tam_r():
    """tâm từng mảnh R trên khung concept = tâm part gốc mà nó thay (sau phép căn)."""
    lop, _, _ = lop_goc()
    out = {}
    for ma, ds in R.items():
        out[ma] = {}
        for ten, sl, _, _ in ds:
            ys, xs = np.nonzero(lop[sl][1])
            out[ma][ten] = (float(xs.mean()), float(ys.mean()))
    return out


def tach_manh(rgb, tam):
    """tách các mảnh chạm viền nhau: lòng tô (không mực, không trắng) chia vùng liền; mỗi vùng về mảnh có tâm gần nhất; mọi điểm của hình
    (cả viền) về mảnh của lòng tô gần nhất. Trắng khép kín trong hình = lỗ (trong suốt). → {tên: mặt nạ bool}."""
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
    out = {}
    for j, k in enumerate(ten):
        out[k] = fg & ~trang & (thuoc == j)
    return out


def tim_mat(rgba):
    """tâm + bán kính con mắt hổ phách trên ảnh thân (px ảnh)."""
    A = rgba.astype(np.int32)
    r_, g_, b_ = A[..., 0], A[..., 1], A[..., 2]
    m = (r_ > 190) & (g_ > 120) & (g_ < 200) & (b_ < 110) & (A[..., 3] > 128)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n < 2:
        return None
    k = 1 + int(np.argmax(st[1:, 4]))
    return float(cen[k][0]), float(cen[k][1]), float(np.sqrt(st[k, 4] / np.pi))


def cat_r():
    """mỗi tờ M_R*: tách mảnh, ghi manh/<tên>.png + moi.json (slot thay, xương, 4 góc thế giới dáng gốc; thân: chỗ + bán kính mắt)."""
    T, Ti, spx = phep_can()
    TAM = tam_r()
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    os.makedirs(MANH, exist_ok=True)
    so = []
    for ma, ds in R.items():
        path = anh.to_moi_nhat(G.TAI, f"M_{ma}")
        if not path:
            print(f"{ma}: chưa gen")
            continue
        print(f"{ma}:", os.path.basename(path))
        rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
        ms = tach_manh(rgb, TAM[ma]) if len(ds) > 1 else {ds[0][0]: (~nen_trang(rgb.astype(np.int32))) & ~(rgb.min(2) > 236)}
        for ten, sl, bn, _ in ds:
            mm0 = ms.get(ten)
            if mm0 is None or mm0.sum() < 50:
                print(f"  {ten}: KHÔNG thấy mảnh")
                continue
            # giữ cụm lớn nhất (+ các cụm sát nó): bỏ vụn rời
            n, lab, st, _ = cv2.connectedComponentsWithStats(mm0.astype(np.uint8), 8)
            k0 = 1 + int(np.argmax(st[1:, 4]))
            gan_ = cv2.dilate((lab == k0).astype(np.uint8), el(6)).astype(bool)
            giu = [i for i in range(1, n) if i == k0 or (gan_ & (lab == i)).any() or st[i, 4] > 0.15 * st[k0, 4]]
            mm0 = np.isin(lab, giu)
            ys, xs = np.nonzero(mm0)
            pad = 4
            x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W - 1, xs.max() + pad), min(H - 1, ys.max() + pad)
            mm = mm0[y0:y1 + 1, x0:x1 + 1]
            al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
            rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], (al * 255).astype(np.uint8)])
            k = 1.0 / spx * (RES * 0.5)             # px tờ → px ảnh mảnh của mình (1 px / đơn vị rig)
            out = Image.fromarray(rgba, "RGBA").convert("RGBa")
            out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
            out.save(os.path.join(MANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
            goc4 = Ti(hop)
            moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=goc4.tolist(), to=ma)
            if ten == "than":
                e = tim_mat(rgba)
                if e:
                    c = Ti([[x0 + e[0], y0 + e[1]]])[0]
                    moi[ten]["mat"] = dict(the_gioi=c.tolist(), r=e[2] / spx)
                    print(f"  mắt: tâm thế giới {c[0]:.0f},{c[1]:.0f}, bán kính {e[2] / spx:.1f} đơn vị")
                if os.path.exists(os.path.join(G.MAU, "huong_than.npy")):
                    gd = np.load(os.path.join(G.MAU, "huong_than.npy"))
                    phu = (mm0 & gd).sum() / max(1, gd.sum())
                    thua = (mm0 & ~gd).sum() / max(1, mm0.sum())
                    print(f"  phủ hình bóng thân {phu:.1%}, vẽ ngoài hình bóng {thua:.1%}")
            so.append(out)
            print(f"  {ten:9s} hộp {x0},{y0}–{x1},{y1}  → {ten}.png {out.size}  (thay {sl}, xương {bn})")
    json.dump(moi, open(pj, "w"), indent=1)
    if so:
        _to_so(so, os.path.join(MANH, "_so_R.png"))


# ================================================================ tách ống xả khỏi khối bắp tay (người dùng 2026-11-16: walk tay phải lỗi)
# tâm từng phần trên tờ M_R3 (px tờ 1536 × 1024): ống sau, ống trước, khối bắp tay
TAM_ONG = {"trai": {"o1": (510, 230), "o2": (440, 300), "khoi": (460, 480)},
           "phai": {"o1": (1040, 230), "o2": (1090, 310), "khoi": (1065, 480)}}
XUONG_ONG = {"trai": "bone27", "phai": "bone8"}             # xương vai (cha của bắp tay): ống không quay theo bắp tay


def tach_ong():
    """M_R3 → ống xả (mảnh riêng có đế tròn kín viền, gắn xương vai, vẽ sau thân) + khối bắp tay trái (thay P_shouR1_3). Bắp tay phải dùng
    tờ K5 (hình bóng gốc bỏ sừng) nên bỏ mảnh đổi dáng của slot P_shouL1_2."""
    T, Ti, spx = phep_can()
    path = anh.to_moi_nhat(G.TAI, "M_R3")
    rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj))
    k = 1.0 / spx * (RES * 0.5)
    ink = np.array(INK, np.uint8)
    sat = np.array([0x3B, 0x3A, 0x3D], np.uint8)
    for ben, tam in TAM_ONG.items():
        nua = np.zeros((H, W), bool)                          # chỉ nửa tờ của cụm này (tờ có hai cụm)
        if ben == "trai":
            nua[:, :W // 2] = True
        else:
            nua[:, W // 2:] = True
        ms = {kk: v & nua for kk, v in tach_manh(rgb, tam).items()}
        ong = ms["o1"] | ms["o2"]
        khoi = ms["khoi"]

        def luu(mm, ten, nen=None):
            ys, xs = np.nonzero(mm if nen is None else (mm | nen))
            x0, y0, x1, y1 = xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5
            A = np.zeros((H, W, 4), np.uint8)
            if nen is not None:
                A[nen] = np.r_[sat, 255]
                vien = nen & ~cv2.erode(nen.astype(np.uint8), el(3)).astype(bool)
                A[vien] = np.r_[ink, 255]
            al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
            A[..., :3] = np.where(mm[..., None], rgb, A[..., :3])
            A[..., 3] = np.maximum(A[..., 3], (al * 255).astype(np.uint8))
            im = Image.fromarray(A[y0:y1, x0:x1], "RGBA").convert("RGBa")
            im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS).convert("RGBA")
            im.save(os.path.join(MANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float)
            return Ti(hop).tolist(), [int(x0), int(y0), int(x1), int(y1)]
        # đế ống: elip sắt sẫm viền mực ngay dưới chân hai ống (bị ống đè), để lúc giáp vai / bắp tay dịch ra không lộ ống cụt
        ys, xs = np.nonzero(ong)
        day = []
        for nm in ("o1", "o2"):
            yy, xx = np.nonzero(ms[nm])
            day.append((xx.mean(), yy.max()))
        cx = float(np.mean([d[0] for d in day]))
        cy = float(max(d[1] for d in day)) - 18
        nen = np.zeros((H, W), np.uint8)
        cv2.ellipse(nen, (int(cx), int(cy)), (int((xs.max() - xs.min()) / 2 + 8), 34), 0, 0, 360, 1, -1)
        nen = nen.astype(bool) & ~ong
        # đế elip sẫm trông như BÓNG ĐỔ dưới ống (luật hình tướng: không bóng) và chân ống đã có viền mực kín theo nét mép khối → bỏ đế
        tg, hop = luu(ong, f"ong_xa_{ben}")
        moi[f"ong_xa_{ben}"] = dict(slot=None, them_truoc="P_shouL1_2", xuong=XUONG_ONG[ben], hop=hop, the_gioi=tg, to="R3")
        print(f"  ống xả {ben}: hộp {hop} → ong_xa_{ben}.png, xương {XUONG_ONG[ben]}")
        if ben == "trai":
            tg, hop = luu(khoi, "khoi_trai")
            moi["khoi_trai"] = dict(slot="P_shouR1_3", xuong="bone28", hop=hop, the_gioi=tg, to="R3")
            print(f"  khối bắp tay trái: hộp {hop} → khoi_trai.png (thay P_shouR1_3)")
    moi.pop("ong_trai", None)
    moi.pop("ong_phai", None)                                # bắp tay phải: tờ K5 trên lưới gốc của P_shouL1_2
    json.dump(moi, open(pj, "w"), indent=1)


# ================================================================ hướng dẫn
def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh theo concept C đã duyệt (2026-11-16)", "",
          "Hai loại tờ (Claude tự gen và tự cắt; người dùng không cần làm gì). Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, p, rs, vi in ps:
        gd += [f"### {ten}", "", vi, "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {v} |" for i, (r, v) in enumerate(rs, 1)]
        gd += [""]
    gd += ["Kiểm: hình bóng trùng tờ hướng dẫn; mảnh đổi dáng đúng chỗ, đúng cỡ như concept, vẽ đủ phần khuất; mặt nạ có lỗ tròn trắng ở chỗ "
           "mắt; tô phẳng; nền trắng. Cắt: `py -3 -I ArtGen/Spine/robot_co_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    ps = []
    for ten in TO_K:
        o = to_k(ten)
        p, gd, out = prompt_k(ten, o)
        ps.append((f"Tờ mảnh giữ hình bóng {ten}", p, [(gd, f"Mảnh gốc cắt theo lưới, phóng to: {VI_K[ten]}"), (CON, "Concept C"),
                                                     (SOI_GIAP, "Sói giáp sắt: chỉ lấy nét")], f"{VI_K[ten]} → `{Wp(out)}`"))
    hth = huong_than()
    for ma, p, out in prompt_r():
        rs = [(CON, "Concept C đã duyệt")] + ([(hth, "Hình bóng thân (xám nhạt): thân của họ bỏ chỏm chữ T + khối đầu của concept")]
                                              if ma == "R1" else [])
        ps.append((f"Tờ mảnh đổi dáng {ma}", p, rs, f"{VI_R[ma]} → `{Wp(out)}`"))
    huong_dan(ps)
    return ps


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        if len(sys.argv) > 2:                               # chỉ dựng một tờ K: robot_co_manh.py to K5
            prompt_k(sys.argv[2], to_k(sys.argv[2]))
        else:
            to_het()
    elif cmd == "tach_ong":
        tach_ong()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ten in TO_K:
            if chi in ("", "K", ten):
                cat_k(ten)
        if chi in ("", "R"):
            cat_r()
    else:
        print(__doc__)
