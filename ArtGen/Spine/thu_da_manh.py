# -*- coding: utf-8 -*-
"""Cóc tê giác pha lê (thu_da, tướng 3 đảo Thổ, ải 10; rig monster_3525): MẢNH "đúng chỗ, đúng cỡ" gen từ concept đã duyệt
(tai_ve/L1_duyet.png = L1_D, người dùng chọn 2026-11-17: cóc tê giác da đất nung, sừng đá kem trên mõm, hàm kem năm răng tù, ba cụm pha lê
hổ phách trên lưng, hai mảng nâu sẫm trên lưng, chân mập vuốt kem).

Concept "gần giống" (tỉ lệ khác con gốc) nên trước hết CĂN cả concept lên hình con gốc bằng một phép co + dời chung (`can`: IoU hình bóng
lớn nhất, chân chạm đất như con gốc). Mọi mảnh cắt ở px concept rồi qua phép căn đó mới vào thế giới rig.

Mảnh (skill pokiclash-spine-rig mục 00 "gen liền rồi cắt"; memory khop-noi-gen-lien):
  T1  THÂN LIỀN một ảnh (thân + đầu + hàm + ngực + bụng, KHÔNG mắt, sừng, chân, pha lê) → cắt theo vùng: lớp KEM (hàm, ngực, bụng) chia cho
      mt1 / chest1 / chest3 / body1; lớp ĐẤT NUNG chia cho head1 / 1chest / hip1 (vùng = hình part gốc gần nhất, chồng mép 14 đơn vị, mép
      cắt của mảnh vẽ trước... xem chia_vung). face21 / face1 / mt2 / beijiao2 / eyes3..5 bỏ (ẩn).
  T2  BA CHÂN liền từng chân (gần sau lleg1/2, gần trước lhand3/1/2, xa trước rhand2/1/3) → cắt theo vùng từng khúc. Chân xa sau (rleg1/2)
      không thấy trên concept: dùng lại ảnh chân gần sau, tối đi 14 %.
  T3  pha lê A2 (to nhất, cụm vai), B1, C1 + SỪNG mũi;   T4  pha lê A1, A3, B2, C2 (mỗi tờ các mảnh không chồng nhau).
      Pha lê → slot gai của họ: A2 beijiao4, A1 hair1, A3 jiao3 (con của đầu); B1 beijiao3, B2 jiao1, C1 beijiao1, C2 jiao2 (con của lưng).
  T5  hai đạo cụ: QUẢ CẦU (cóc cuộn tròn thành tảng đá, cụm pha lê chĩa ra) cho slot xz; LÒNG MIỆNG + lưỡi cho slot shetou.
  mắt: cắt thẳng từ concept (eyes2); mắt nhắm (eyes1) vẽ bằng mã (mí đất nung + nét mực cong).

    thu_da_manh.py can          tìm phép căn concept → con gốc → mau/can.json
    thu_da_manh.py prompt       file prompt T1..T5 → gui_gpt/thu_da_1/luot_2_<tờ>.txt (+ nối HUONG_DAN.md)
    thu_da_manh.py cat [tờ]     cắt ảnh về (tai_ve/M_<tờ>.png) → manh/<slot>.png + manh/dat.json (hộp px concept)
    thu_da_manh.py mat          mắt mở cắt từ concept + mắt nhắm vẽ bằng mã
    thu_da_manh.py ghep         ghép mọi mảnh (qua phép căn) theo thứ tự vẽ cạnh concept và con gốc → manh/_ghep.png + IoU
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

G = tho5.dat("thu_da")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "thu_da_1")
MUC = (43, 33, 24)

# ---------------------------------------------------------------- nhóm gen
TAM = {  # tâm dự kiến (px concept) của từng mảnh / khối, để gán cụm cắt ra cho đúng tên
    "than": (760, 560), "lleg": (440, 780), "lhand": (705, 770), "rhand": (1050, 815),
    "A2": (825, 180), "B1": (550, 300), "C1": (380, 460), "sung": (1110, 370),
    "A1": (725, 255), "A3": (952, 235), "B2": (505, 370), "C2": (350, 512),
    "xz": (768, 300), "shetou": (768, 800),
}
NHOM = {
    "T1": [("than", "the WHOLE BODY AND HEAD as ONE piece: the terracotta head with its heavy brow, the big cream lower JAW with its five "
            "blunt teeth, the cream chest and belly, the terracotta back and flank with the two dark brown patches",
            "draw it WITHOUT the eye (where the eye was: plain terracotta skin, keep the heavy angry brow line above it), WITHOUT the horn "
            "on the snout (where it was: the snout continues as a plain rounded terracotta snout tip), WITHOUT the amber crystals (where "
            "they stood: the back continues as a plain rounded terracotta back), WITHOUT the four legs (where the legs cover the body: the "
            "flank and the cream belly continue as a plain rounded body). One closed shape with the ink outline all round")],
    "T2": [("lleg", "the NEAR BACK LEG (lower left): thigh, lower leg and the foot with two cream claws",
            "complete its top, hidden in the body, as a rounded thigh"),
           ("lhand", "the NEAR FRONT LEG (the big one in the bottom middle): shoulder, lower leg and the foot with three cream claws",
            "complete its top, hidden in the body, as a rounded shoulder"),
           ("rhand", "the FAR FRONT LEG (lower right): upper leg, lower leg and the foot with three cream claws",
            "complete its top, hidden behind the cream chest, as a rounded upper leg")],
    "T3": [("A2", "the TALLEST amber crystal (the big middle one of the cluster above the shoulders)",
            "complete its bottom, hidden in the back, as the crystal prism continuing down"),
           ("B1", "the upper-left crystal of the middle cluster on the back", "complete its bottom as the prism continuing down"),
           ("C1", "the upper crystal of the small cluster at the rear (left)", "complete its bottom as the prism continuing down"),
           ("sung", "the cream stone HORN on the snout", "complete its base, hidden in the snout, as a rounded base")],
    "T4": [("A1", "the LEFT crystal of the big cluster above the shoulders", "complete its bottom as the prism continuing down, and the part "
            "hidden behind the tallest crystal"),
           ("A3", "the RIGHT crystal of the big cluster above the shoulders", "complete its bottom and the part hidden behind the tallest "
            "crystal"),
           ("B2", "the LOWER crystal of the middle cluster on the back", "complete its bottom and the part hidden behind the other crystal"),
           ("C2", "the LOWER crystal of the small cluster at the rear (left)", "complete its bottom and the part hidden behind the other "
            "crystal")],
}
# cụm pha lê → slot gai của họ
PHA_LE = {"A2": "beijiao4", "A1": "hair1", "A3": "jiao3", "B1": "beijiao3", "B2": "jiao1", "C1": "beijiao1", "C2": "jiao2"}
# chia khối liền thành slot của họ
CHIA = {
    "than_lung": {"tat": ["1chest", "hip1"]},
    "than_bung": {"tat": ["chest3", "chest1", "body1"]},
    "lleg": {"tat": ["lleg1", "lleg2"]},
    "lhand": {"tat": ["lhand3", "lhand1", "lhand2"]},
    "rhand": {"tat": ["rhand2", "rhand1", "rhand3"]},
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a stocky TOAD-RHINO turned to the right, standing on four "
        "thick legs: terracotta skin, a big cream lower jaw with five blunt teeth, a cream chest and belly, a heavy angry brow over one "
        "small yellow eye, a cream stone horn on the snout, two dark brown patches on the back, three clusters of amber crystals along "
        "the back, cream claws. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")
DAO_CU = [
    ("xz", "a BALL, alone in the UPPER half of the canvas (centre about x = 768, y = 290): the same toad-rhino CURLED UP into a round "
     "BOULDER about 400 px wide and 380 px tall, seen from the side: only its terracotta back and flank show, rounded into a near circle, "
     "with the two dark brown patches and its three clusters of amber crystals sticking OUTWARD from the ball (one cluster on top, one "
     "on the upper left, one small on the lower left); the cream stone horn sticks out on the right side; the head, legs, jaw and eye are "
     "tucked away and NOT visible (a closed ball). No motion lines, no dust."),
    ("shetou", "the INSIDE OF AN OPEN MOUTH, alone in the LOWER half of the canvas (centre about x = 768, y = 790): a wide flat rounded "
     "shape about 420 px wide and 190 px tall: a flat very dark red-brown #4A2320 mouth cavity with a flat pink tongue #D9787A lying in its "
     "lower half (the tongue's rounded tip to the right), the ink outline all round. Nothing else."),
]


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


# ---------------------------------------------------------------- căn concept lên con gốc
def mat_na(p):
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H))).astype(np.int16)
    m = ((255 - a).max(2) > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k


def can():
    """phép căn concept → khung con gốc: co a quanh tâm khung + dời (dx, dy); chọn a, dx theo IoU hình bóng, dy để đáy chân trùng đáy chân
    con gốc."""
    g = mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
    c = mat_na(CONCEPT)
    best = None
    for a in np.arange(0.84, 0.94, 0.01):
        M = np.float32([[a, 0, 768 * (1 - a)], [0, a, 512 * (1 - a)]])
        cw = cv2.warpAffine(c, M, (W, H), flags=cv2.INTER_NEAREST)
        gy = np.nonzero(g)[0].max()
        cy_ = np.nonzero(cw)[0].max()
        dy = int(gy - cy_)
        for dx in range(-60, 61, 3):
            cs = np.roll(np.roll(cw, dy, 0), dx, 1)
            iou = (cs & g).sum() / max(1, (cs | g).sum())
            if best is None or iou > best[0]:
                best = (float(iou), float(a), int(dx), int(dy))
    iou, a, dx, dy = best
    json.dump(dict(a=a, dx=dx, dy=dy, iou=iou), open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print(f"căn: a {a:.2f}, dời ({dx}, {dy}) px, IoU hình bóng {iou:.3f}")


def phep_can():
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    return j["a"], j["dx"], j["dy"]


def tf():
    """px concept → px khung con gốc → thế giới rig."""
    a, dx, dy = phep_can()
    jj = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = jj["s"], jj["cx"], jj["cy"]
    c2g = lambda P: np.stack([a * (P[:, 0] - W / 2) + W / 2 + dx, a * (P[:, 1] - H / 2) + H / 2 + dy], 1)
    g2w = lambda Q: np.stack([cx + (Q[:, 0] - W / 2) / s, cy - (Q[:, 1] - H / 2) / s], 1)
    w2g = lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
    return dict(a=a, s=s, c2w=lambda P: g2w(c2g(P)), c2g=c2g, w2g=w2g)


# ---------------------------------------------------------------- prompt
def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-17; người dùng chọn D = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): cóc tê giác da đất nung, hàm kem năm răng, "
          "sừng đá kem, ba cụm pha lê hổ phách, bốn chân mập vuốt kem. T1–T4 giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị "
          "che; T5 vẽ hai đạo cụ cùng nét (quả cầu cuộn tròn, lòng miệng). Mắt Claude cắt thẳng từ concept.", ""]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap between the "
             "kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    out, save = luu("M_T5")
    p = os.path.join(GUI, "luot_2_T5.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(CONCEPT)}: {ANH1} Use it for the character's look and the drawing style.", ""] + save + ["",
         "TASK: draw TWO separate props for the animation of this character, in exactly the hand-drawn style of image 1 (wobbly dark-brown "
         "ink outline about 7 px all the way round each prop, flat colours with visible coloured-pencil / wax-crayon hatching, no shading, "
         "no highlights, no shadows, no glow). VERY SIMPLE, FEW DETAILS. Keep a wide white gap between the two props.", ""]
    t += [f"{i}. {d}" for i, (_, d) in enumerate(DAO_CU, 1)]
    t += ["", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no frame."]
    ghi(p, t)
    gd += [f"- **T5** (xz, shetou): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
    print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `thu_da_manh.py ghep`); phần bị che vẽ đủ, viền kín; thân "
           "không còn mắt, sừng, chân, pha lê; quả cầu kín không lộ mặt chân; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
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


def luu_manh(A, m, ten, DATJ, nguon, alpha_them=None, toi=0.0):
    """m: mặt nạ (H × W) của mảnh; alpha_them (H × W, 0..1): nhân thêm vào alpha (mép cắt mờ dần); toi: làm tối (chân xa)."""
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    if toi:
        rgb = (rgb.astype(np.float32) * (1 - toi)).astype(np.uint8)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    if alpha_them is not None:
        al = al * alpha_them[y0:y1, x0:x1]
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


def hull_goc():
    """hình (đa giác bao lồi) từng part gốc ở idle 0, px concept (qua phép căn ngược)."""
    T = tf()
    a, dx, dy = phep_can()
    g2c = lambda Q: np.stack([(Q[:, 0] - W / 2 - dx) / a + W / 2, (Q[:, 1] - H / 2 - dy) / a + H / 2], 1)
    _, imgs, atts = G.nap("att_idle0.json")
    out = {}
    for at in atts:
        P = g2c(T["w2g"](np.array(at["xy"], float).reshape(-1, 2)))
        out[at["slot"]] = cv2.convexHull(P.astype(np.float32)).reshape(-1, 2)
    return out


THU_TU_GOC = None


def thu_tu_goc():
    global THU_TU_GOC
    if THU_TU_GOC is None:
        _, _, atts = G.nap("att_idle0.json")
        THU_TU_GOC = {a["slot"]: a["order"] for a in atts}
    return THU_TU_GOC


def chia_vung(A, m, ten_khoi, DATJ, nguon, HG):
    """chia một khối liền (mặt nạ m) thành mảnh từng slot của họ: mỗi điểm thuộc slot có hình part gốc gần nhất (khoảng cách tới đa giác,
    0 nếu ở trong); mỗi slot lấy thêm dải CHONG px quanh vùng của nó. Ở dải chồng, mảnh vẽ SAU (thứ tự của họ) mờ dần về mép cắt, mảnh vẽ
    TRƯỚC giữ đặc (khỏi thủng). Khối thân chia hai lớp màu trước (kem / đất nung) rồi mới chia vùng trong lớp."""
    CHONG = 26.0
    ord_ = thu_tu_goc()
    ys, xs = np.nonzero(m)
    lop = {k: v for k, v in CHIA[ten_khoi].items()}
    # phân lớp màu
    if "kem" in lop:
        rgb = A.astype(np.float32)
        kem = (rgb[..., 0] > 200) & (rgb[..., 1] > 170) & (rgb[..., 2] > 115) & (rgb[..., 0] - rgb[..., 2] < 110)
        kem = cv2.morphologyEx((kem & m).astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)
        n, lab, st, _ = cv2.connectedComponentsWithStats(kem.astype(np.uint8), 8)
        kem = np.isin(lab, [i for i in range(1, n) if st[i, 4] > 1500])
        # nét mực theo lớp gần nhất: lớp kem nới 6 px ăn luôn nét mực viền của nó
        kem_n = cv2.dilate(kem.astype(np.uint8), el(6)).astype(bool) & m
        dat = m & ~kem_n
        dat_n = cv2.dilate(dat.astype(np.uint8), el(6)).astype(bool) & m
        mats_lop = {"kem": kem_n, "dat": dat_n}
    else:
        mats_lop = {list(lop)[0]: m}
    pts = np.stack([xs, ys], 1).astype(np.float32)
    for ln, slots in lop.items():
        ml = mats_lop[ln]
        D = {}
        for s in slots:
            poly = HG[s].reshape(-1, 1, 2).astype(np.float32)
            d = np.zeros((H, W), np.float32)
            dd = np.array([max(0.0, -cv2.pointPolygonTest(poly, (float(x), float(y)), True)) for x, y in pts], np.float32)
            d[ys, xs] = dd
            D[s] = d
        dmin = np.min(np.stack([D[s] for s in slots]), 0)
        amin = np.argmin(np.stack([D[s] for s in slots]), 0)
        for k, s in enumerate(slots):
            vung = ml & (D[s] <= dmin + CHONG)
            if not vung.any():
                print(f"  {s}: rỗng")
                continue
            # mép cắt mờ: nếu slot này vẽ SAU slot sở hữu điểm đó thì mờ dần qua dải chồng
            chu = np.array(slots)[amin]
            sau = np.vectorize(lambda o: ord_.get(o, 0))(chu) < ord_.get(s, 0)
            f = np.where((D[s] > dmin) & sau, np.clip(1.0 - (D[s] - dmin) / CHONG, 0, 1), 1.0).astype(np.float32)
            b = luu_manh(A, vung, s, DATJ, nguon, alpha_them=f)
            print(f"  {s:8s} hộp {b}")


def chia_chan(A, m, ten_khoi, DATJ, nguon, HG):
    """chân liền → khúc của họ theo DẢI DỌC: ranh giới giữa hai khúc kề = giữa đoạn chồng (theo chiều dọc) của hai part gốc, tính theo tỉ lệ
    chiều cao cả chân gốc rồi áp lên chiều cao chân của mình (concept lệch chỗ so với rig nên chia theo hình part gốc cắt sai bàn chân).
    Mỗi khúc lấy thêm dải chồng CHONG px; ở dải chồng, khúc vẽ SAU mờ dần về mép cắt."""
    CHONG = 22.0
    ord_ = thu_tu_goc()
    slots = CHIA[ten_khoi]["tat"]
    yr = {s: (float(HG[s][:, 1].min()), float(HG[s][:, 1].max())) for s in slots}
    seq = sorted(slots, key=lambda s: (yr[s][0] + yr[s][1]) / 2)             # trên → dưới
    g0, g1 = min(v[0] for v in yr.values()), max(v[1] for v in yr.values())
    ranh = []
    for a_, b_ in zip(seq, seq[1:]):
        lo, hi = yr[b_][0], yr[a_][1]                                       # đoạn chồng: đầu khúc dưới → cuối khúc trên
        ranh.append(((lo + hi) / 2 - g0) / (g1 - g0))
    ys, xs = np.nonzero(m)
    m0, m1 = ys.min(), ys.max()
    bien = [m0 - 1e6] + [m0 + r * (m1 - m0) for r in ranh] + [m1 + 1e6]
    yy = np.broadcast_to(np.arange(H)[:, None], (H, W)).astype(np.float32)
    D = {s: np.maximum(0.0, np.maximum(bien[i] - yy, yy - bien[i + 1])) for i, s in enumerate(seq)}
    dmin = np.minimum.reduce([D[s] for s in seq])
    amin = np.argmin(np.stack([D[s] for s in seq]), 0)
    for i, s in enumerate(seq):
        vung = m & (D[s] <= dmin + CHONG)
        chu = np.array(seq)[amin]
        sau = np.vectorize(lambda o: ord_.get(o, 0))(chu) < ord_.get(s, 0)
        f = np.where((D[s] > dmin) & sau, np.clip(1.0 - (D[s] - dmin) / CHONG, 0, 1), 1.0).astype(np.float32)
        b = luu_manh(A, vung, s, DATJ, nguon, alpha_them=f)
        print(f"  {s:8s} hộp {b}")


def gan_muc(A, m, nhom):
    """nhom: {tên: mặt nạ điểm màu}; trả {tên: mặt nạ} sau khi chia mọi điểm mực (và điểm lẻ) trong m cho nhóm màu gần nhất."""
    co = np.zeros((H, W), np.int32)
    ten = list(nhom)
    for k, t in enumerate(ten, 1):
        co[nhom[t]] = k
    src = (co == 0).astype(np.uint8)
    _, lab = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(src == 0)                                      # điểm "không" theo thứ tự quét = nhãn 1..N
    gan = co[zy, zx]
    near = np.zeros((H, W), np.int32)
    ok = lab > 0
    near[ok] = gan[np.clip(lab[ok] - 1, 0, len(gan) - 1)]
    near[co > 0] = co[co > 0]
    return {t: m & (near == k) for k, t in enumerate(ten, 1)}, near


def chia_than(A, m, DATJ, nguon, HG):
    """khối thân liền T1 → cụm màu khép kín bởi nét mực: ĐẦU (head1), HÀM + răng (mt1), BỤNG kem (chia body1 / chest1 / chest3 theo vùng),
    LƯNG đất nung + mảng nâu (chia 1chest / hip1 theo vùng; lấn 20 px vào dưới đầu, màu lấy điểm lưng gần nhất, khỏi hở khi đầu xoay)."""
    lum = A.mean(2)
    muc = lum < 95
    trang = A.min(2) > 236
    hinh = m & ~muc & ~trang
    n, lab, st, cen = cv2.connectedComponentsWithStats(hinh.astype(np.uint8), 4)
    rgb = A.astype(np.float32)
    dau = ham = bung = None
    rang, lung = [], []
    for i in range(1, n):
        if st[i, 4] < 40:
            continue
        c = rgb[lab == i].mean(0)
        kem = c[0] > 225 and c[1] > 195 and c[2] > 130
        cx_, cy_ = cen[i]
        if kem:
            if st[i, 4] > 20000:
                if cy_ < 690 and (ham is None or st[i, 4] > st[ham, 4] or cy_ < cen[ham][1]):
                    if ham is not None and cen[ham][1] > cy_:
                        bung = ham if bung is None else bung
                    ham = i if (ham is None or cy_ < cen[ham][1]) else ham
                else:
                    bung = i if bung is None or st[i, 4] > st[bung, 4] else bung
            else:
                rang.append(i)
        elif st[i, 4] > 20000 and cx_ > 780 and cy_ < 560 and (dau is None or cx_ > cen[dau][0]):
            if dau is not None:
                lung.append(dau)
            dau = i
        else:
            lung.append(i)
    print(f"  cụm: đầu {dau}, hàm {ham}, bụng {bung}, răng {len(rang)}, lưng {len(lung)}")
    nhom = {"dau": lab == dau, "ham": np.isin(lab, [ham] + rang), "bung": lab == bung, "lung": np.isin(lab, lung)}
    M, near = gan_muc(A, m, nhom)
    # nét mực chỗ đầu giáp lưng thuộc ĐẦU (mảnh vẽ trước): khi đầu xoay, lưng không lộ vạch mực đôi
    gan_dau = cv2.dilate(nhom["dau"].astype(np.uint8), el(9)).astype(bool)
    chuyen = M["lung"] & muc & gan_dau
    M["lung"] &= ~chuyen
    M["dau"] |= chuyen
    B = A.copy()
    # lưng lấn vào dưới đầu: điểm đầu cách lưng ≤ 22 px và cách mép ngoài khối > 12 px (khỏi thò ra ngoài hình đầu), tô màu điểm lưng gần nhất
    lung_mau = nhom["lung"] & ~muc
    d, lab2 = cv2.distanceTransformWithLabels((~lung_mau).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(lung_mau)
    d_ngoai = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    lan = (M["dau"] & (d <= 22) & (d_ngoai > 12)) | (M["ham"] & (d <= 28) & (d_ngoai > 12))   # lấn dưới đầu và dưới góc sau của hàm
    k = np.clip(lab2[lan] - 1, 0, len(zy) - 1)
    B[lan] = A[zy[k], zx[k]]
    M_lung = M["lung"] | lan
    b = luu_manh(A, M["dau"], "head1", DATJ, nguon)
    print(f"  head1    hộp {b}")
    b = luu_manh(A, M["ham"], "mt1", DATJ, nguon)
    print(f"  mt1      hộp {b}")
    chia_vung(B, M_lung, "than_lung", DATJ, nguon, HG)
    chia_vung(A, M["bung"], "than_bung", DATJ, nguon, HG)


def cat(chi=None):
    DATJ = nap_dat()
    HG = hull_goc()
    for nh, ds in list(NHOM.items()) + [("T5", [(s, "", "") for s, _ in DAO_CU])]:
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        names = [s for s, _, _ in ds]
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        gan = {s: [] for s in names}
        for i in range(1, n):
            if st[i, 4] <= 30:
                continue
            c = cen[i]
            best = min(names, key=lambda s: np.hypot(c[0] - TAM[s][0], c[1] - TAM[s][1]))
            if np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1]) < 300 or st[i, 4] > 20000:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ({c[0]:.0f}, {c[1]:.0f}) {st[i, 4]} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:8s} KHÔNG THẤY")
                continue
            m = np.isin(lab, ids)
            cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            m = cv2.drawContours(np.zeros((H, W), np.uint8), cs, -1, 1, -1).astype(bool)   # lấp lỗ giấy trắng khép kín trong mảnh
            if s == "than":
                chia_than(A, m, DATJ, os.path.basename(src), HG)
            elif s in CHIA:
                chia_chan(A, m, s, DATJ, os.path.basename(src), HG)
                if s == "lleg":                                # chân xa sau: dùng lại chân gần sau, tối đi, DỜI tới chỗ chân xa của họ
                    c_l = np.concatenate([HG["lleg1"], HG["lleg2"]]).mean(0)
                    c_r = np.concatenate([HG["rleg1"], HG["rleg2"]]).mean(0)
                    dx_, dy_ = int(round(c_r[0] - c_l[0])), int(round(c_r[1] - c_l[1]))
                    for a_, b_ in (("lleg1", "rleg1"), ("lleg2", "rleg2")):
                        im = Image.open(os.path.join(MANH, a_ + ".png")).convert("RGBA")
                        q = np.asarray(im).astype(np.float32)
                        q[..., :3] *= 0.86
                        Image.fromarray(q.astype(np.uint8), "RGBA").save(os.path.join(MANH, b_ + ".png"))
                        h_ = DATJ[a_]["hop"]
                        DATJ[b_] = dict(hop=[h_[0] + dx_, h_[1] + dy_, h_[2] + dx_, h_[3] + dy_], dung_lai=a_,
                                        nguon=DATJ[a_]["nguon"] + f" (dùng lại {a_}, tối 14 %, dời {dx_}, {dy_} px)")
                    print(f"  rleg1/2  dùng lại lleg, dời ({dx_}, {dy_}) px")
            else:
                ten = PHA_LE.get(s, s)
                b = luu_manh(A, m, ten, DATJ, os.path.basename(src))
                print(f"  {s:8s} → {ten:9s} hộp {b}")
    ghi_dat(DATJ)


# ---------------------------------------------------------------- mắt
MAT_HOP = (840, 388, 1030, 495)                                          # hộp quanh mắt (px concept)


def mat():
    """mắt mở cắt thẳng từ concept (tròng vàng + con ngươi + vành mực, KHÔNG lấy nét mày) → eyes2; mắt nhắm vẽ bằng mã → eyes1: mí đất nung
    phủ đúng chỗ mắt + một nét mực cong (giữa võng xuống)."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = A[y0:y1, x0:x1]
    vang = (sub[..., 0] > 200) & (sub[..., 1] > 140) & (sub[..., 2] < 150) & (sub[..., 0] - sub[..., 2] > 70)
    toi = sub.mean(2) < 95
    sang = sub.min(2) > 200
    # mắt = vùng vàng + nét mực + chấm sáng nối liền với tròng vàng (nét mày tách rời nên bị loại), rồi lấp lỗ
    mat_ = (vang | toi | sang).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mat_, 8)
    nv, labv, stv, _ = cv2.connectedComponentsWithStats(vang.astype(np.uint8), 8)
    kv = 1 + int(np.argmax(stv[1:, 4]))
    k = int(np.bincount(lab[labv == kv]).argmax())
    tr = (lab == k).astype(np.uint8)
    cs, _ = cv2.findContours(tr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    kin = cv2.drawContours(np.zeros_like(tr), cs, -1, 1, -1)
    vanh = cv2.dilate(kin, el(1)).astype(bool)
    full = np.zeros((H, W), bool)
    full[y0:y1, x0:x1] = vanh
    print("eyes2", luu_manh(A, full, "eyes2", DATJ, "L1_duyet.png (cắt thẳng)"))
    # mắt nhắm: giữ nét mí trên dày (nét mực phía trên lòng mắt), lòng mắt (tròng + con ngươi) tô màu da đầu, đáy lòng mắt kẻ một nét mực
    # (mí khép); nét viền dưới cũ cũng thành da.
    vung = (cv2.dilate(full.astype(np.uint8), el(6)) & ~cv2.dilate(full.astype(np.uint8), el(3))).astype(bool)
    da = np.median(A[vung & (A.mean(2) > 100)], 0).astype(int)
    DH = DATJ.get("head1")
    if DH:                                                              # màu da lấy từ mảnh đầu (tờ T1) cho mí trùng màu đầu trong rig
        hd = np.asarray(Image.open(os.path.join(MANH, "head1.png")).convert("RGBA")).astype(np.int32)
        hx0, hy0 = DH["hop"][:2]
        ys_, xs_ = np.nonzero(vung)
        ok = (ys_ - hy0 >= 0) & (ys_ - hy0 < hd.shape[0]) & (xs_ - hx0 >= 0) & (xs_ - hx0 < hd.shape[1])
        q = hd[ys_[ok] - hy0, xs_[ok] - hx0]
        q = q[(q[:, 3] > 200) & (q[:, :3].mean(1) > 100)]
        if len(q) > 50:
            da = np.median(q[:, :3], 0).astype(int)
    # vẽ mới trên khuôn mắt: cả khuôn tô màu da; nét MÍ TRÊN dày chạy theo mép trên khuôn (từ đuôi trái tới móc phải); nét MÍ KHÉP cong
    # võng xuống ở khoảng 55 % chiều cao khuôn.
    ys_f, xs_f = np.nonzero(full)
    top, bot = {}, {}
    for x in range(xs_f.min(), xs_f.max() + 1):
        c = ys_f[xs_f == x]
        if len(c):
            top[x], bot[x] = c.min(), c.max()
    B = A.copy()
    B[full] = da
    can_ = Image.fromarray(B.astype(np.uint8))
    d = ImageDraw.Draw(can_)
    xs_k = sorted(top)
    d.line([(x, top[x] + 5) for x in xs_k], fill=MUC, width=10, joint="curve")
    x_a, x_b = xs_k[0] + int(0.18 * len(xs_k)), xs_k[-1] - int(0.12 * len(xs_k))
    khep = [(x, top[x] + 5 + 0.55 * (bot[x] - top[x] - 5)) for x in xs_k if x_a <= x <= x_b]
    d.line(khep, fill=MUC, width=6, joint="curve")
    B = np.asarray(can_).astype(np.int32)
    m_nham = full
    print("eyes1", luu_manh(B, m_nham, "eyes1", DATJ, "vẽ bằng mã từ eyes2 (mí trên giữ, lòng mắt thành da, nét mực mí khép)"),
          "màu da", da)
    ghi_dat(DATJ)


# ---------------------------------------------------------------- ghép soi
THU_TU = ["beijiao3", "beijiao1", "rhand3", "rhand2", "rhand1", "rleg2", "rleg1", "chest3", "jiao3", "1chest", "jiao2", "hip1", "jiao1",
          "beijiao4", "head1", "mt1", "chest1", "body1", "lleg2", "lleg1", "lhand3", "hair1", "eyes2", "lhand2", "lhand1", "sung"]


def ghep():
    """ghép mảnh (px concept) theo thứ tự vẽ của họ; tờ: concept | ghép | so (đỏ = concept có mà ghép thiếu, xanh = thừa)."""
    DATJ = nap_dat()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in THU_TU:
        if s not in DATJ or DATJ[s].get("dung_lai"):
            if s not in DATJ:
                thieu.append(s)
            continue
        x0, y0, _, _ = DATJ[s]["hop"]
        can_.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(np.int32)
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
    print(p, f"IoU hình bóng với concept {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "mat":
        mat()
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
