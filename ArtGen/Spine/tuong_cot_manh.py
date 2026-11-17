# -*- coding: utf-8 -*-
"""Tượng vua cổ rễ quấn (tuong_cot, tướng 6 đảo Mộc, rig monster_3608): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png
= hướng B, người dùng chọn 2026-11-17). Concept to hơn con gốc ~14 %: căn bằng co k + dời (mau/can.json) rồi mỗi mảnh đặt theo chỗ của
nó trên concept và gắn vào xương / nhóm lưới gốc tương ứng (tuong_cot_rig.py).

    tuong_cot_manh.py can          căn concept lên hình con gốc (co + dời, IoU) → mau/can.json
    tuong_cot_manh.py tren         vẽ viền từng part gốc (tô theo nhóm) chồng lên concept → mau/_rig_tren_concept.png
    tuong_cot_manh.py prompt       file prompt từng nhóm → gui_gpt/tuong_cot_1/luot_2_<nhóm>.txt (+ nối HUONG_DAN.md)
    tuong_cot_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    tuong_cot_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
import quy_nui_manh as Q  # noqa: E402

tho5.CON["tuong_cot"] = ("monster_3608", 6, 30)
G = tho5.dat("tuong_cot")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "tuong_cot_1")
Q.G, Q.CONCEPT, Q.MANH, Q.GUI = G, CONCEPT, MANH, GUI

# nhóm part gốc (để tô màu khi soi); khoá = tên nhóm
NHOM_GOC = {
    "vai_gan": ["P_jianjiaR01", "P_jianjiaR02", "P_jianjiaR03", "P_jianjiaR04", "P_jianjiaR05"],
    "tay_gan": ["P_shoubiR01", "P_shoubiR02"],
    "nam_gan": ["P_shouR01"] + [f"P_shouzhiR0{i}" for i in range(1, 9)],
    "vai_xa": ["P_jianjiaL01", "P_jianjiaL02", "P_jianjiaL03", "P_jianjiaL04", "P_jianjiaL05"],
    "tay_xa": ["P_shoubiL01", "P_shoubiL02", "P_shoubiL03", "P_shoubiL04"],
    "nam_xa": ["P_shouL01"] + [f"P_shouL0{i}" for i in range(2, 10)],
    "dau": ["P_tou"], "lung": ["P_beijia"], "cot": ["P_wuqi"],
    "loi": ["P_jiejingqiu", "P_qiu"], "nguc": ["P_xiongjia01", "P_xiongjia02", "P_xiongjia03", "P_shikuai01"],
    "da": [f"P_shitou0{i}" for i in range(1, 9)], "pha_le": [f"P_jiejing0{i}" for i in range(1, 7)],
    "day": ["P_tengwan01", "P_tengwan02"],
}
MAU_NHOM = {"vai_gan": (230, 40, 40), "tay_gan": (240, 140, 0), "nam_gan": (200, 0, 160), "vai_xa": (0, 120, 255), "tay_xa": (0, 180, 200),
            "nam_xa": (120, 0, 255), "dau": (0, 0, 0), "lung": (120, 80, 0), "cot": (0, 150, 0), "loi": (255, 0, 0), "nguc": (255, 120, 180),
            "da": (90, 90, 90), "pha_le": (0, 220, 120), "day": (160, 160, 0)}


# ---------------------------------------------------------------- mảnh của mình (khung px trên concept 1536 × 1024)
# Bên theo NGƯỜI XEM. Con quay phải; tay GẦN ở nửa trái tranh (slot *R* của họ), tay XA nắm cột ở bên phải (slot *L*).
#   cot      cột vuông + hai rễ quấn + lá            ← P_wuqi (bone54, con của lòng bàn tay xa bone21)
#   da_k     đá lơ lửng dưới ngực                    ← P_shitou01..08 (bone31..38), gán theo tâm gần nhất
#   dau      đầu vua cổ + vương miện ba tầng          ← P_tou (bone4)
#   tay_gan  cánh tay gần (đá xếp) + đoạn rễ + 2 lá   ← P_shoubiR01 + R02 (bone7, bone59 đứng yên theo bone7)
#   vai_gan  vai gần (phiến vòm có gờ) + đoạn rễ + lá ← P_jianjiaR01..05 (bone17, bone30)
#   than     ngực (khối đá quanh lõi) + vòng rễ ôm lõi ← P_xiongjia01..03, P_shikuai01, P_tengwan01 (bone55..58, bone3)
#   nam_xa   các khối ngón tay xa trên mép cột        ← P_shouL04/06/08 (vẽ trước cột), bám bone21
#   lung     khối đá sau đầu (lưng)                   ← P_beijia (bone39)
#   nam_gan  nắm tay gần (một khối: lòng + ngón)      ← P_shouR01 + ngón (bone8)
#   pha_le_k hai mảnh pha lê lá giữa vai và tay gần   ← P_jiejing02/03 (bone50, bone49); 01, 04..06 mượn ảnh
#   vai_xa   phiến vai xa (sau cột)                   ← P_jianjiaL01..05
#   loi      cụm ba pha lê lá (lõi)                   ← P_jiejingqiu (bone3)
#   tay_xa   cánh tay xa + mu bàn tay (khuất sau cột: vẽ ở góc trống, đặt theo khung part gốc) ← P_shoubiL01..04 + P_shouL01
# BỎ: P_qiu (viên tròn nhỏ ở cổ), P_tengwan02 (dây leo lưng: rễ trên cột đã vẽ liền vào cột).
TAM = {"cot": (870, 430), "dau": (755, 450), "tay_gan": (380, 660), "vai_gan": (490, 400), "than": (710, 680), "nam_xa": (1095, 520),
       "lung": (640, 430), "nam_gan": (410, 840), "vai_xa": (965, 380), "loi": (705, 615), "tay_xa": (1340, 200)}

NHOM = {
    "Q1": [("cot", "the big SQUARE STONE PILLAR lying diagonally across the picture (its broken top end with the stepped carved band at the "
            "upper middle, around x 550-760, y 60-250; its lower end with the stepped carved band at the lower right, around x 1000-1190, "
            "y 560-800), INCLUDING the two brown tree roots wrapped round it (the upper root around x 600-840, y 180-330 and the lower "
            "root around x 880-1060, y 360-600) and their small green leaves",
            "draw the WHOLE pillar as one straight square column from end to end: the parts hidden behind the head, behind the round "
            "shoulder slab and behind the dark finger blocks continue straight with the same width and the same edges; the two roots stay "
            "wrapped round it exactly where they are"),
           ("da", "the FLOATING dark-grey ROCK CHUNKS under the chest (the loose angular stones around x 470-870, y 690-960)",
            "draw each rock as its own small closed angular stone with a clear white gap between rocks; do not merge them")],
    "Q2": [("dau", "the HEAD: the carved ancient king face (narrow green eyes, heavy brow, wide flat nose, firm thick lips, broad jaw) with "
            "the tall pointed crown of three stacked tiers on top (around x 650-860, y 285-600)",
            "complete its back and its bottom (hidden by nothing else) as the same carved stone; keep the face and the crown exactly"),
           ("tay_gan", "the NEAR ARM on the left: the column of grey stone blocks from under the shoulder down to just above the dark fist "
            "(around x 285-475, y 500-830), INCLUDING the brown root running down along it and its two green leaves at its left side",
            "complete its top (under the shoulder slab) and its bottom (above the fist) as rounded stone ends; the root stays on it exactly "
            "where it is")],
    "Q3": [("vai_gan", "the NEAR SHOULDER: the big rounded dome-like stone slab with its rim at the upper left (around x 330-665, "
            "y 330-525), INCLUDING the brown root crawling over it and the green leaves sticking out at its top and its left",
            "complete it into one closed rounded slab (its bottom edge hidden behind the arm continues as the same stone)"),
           ("than", "the CHEST: the mass of grey stone blocks around the heart in the middle of the body (around x 540-880, y 540-800), "
            "INCLUDING the brown root ring that holds the heart crystals, but WITHOUT the three green crystals",
            "complete it as one closed chunk of stacked stones: where the green crystals were, draw the stone and the root ring continuing "
            "behind them (a slightly darker stone hollow in the middle of the ring); its top hidden behind the head continues as stone"),
           ("nam_xa", "the dark FINGER BLOCKS of the far hand gripping the pillar near its lower-right end (around x 1035-1150, y 465-575)",
            "keep only these few dark finger blocks exactly as they are, each completed into its own closed blocky shape")],
    "Q4": [("lung", "the BACK STONES behind the head: the grey and dark-grey stone blocks between the near shoulder slab and the head "
            "(around x 560-720, y 290-570)", "complete them as one closed chunk of stacked stones (the parts hidden by the head, the "
            "shoulder slab and the pillar continue as the same stones)"),
           ("nam_gan", "the dark NEAR FIST at the lower left: the fist made of dark-grey blocky stone fingers and knuckles (around "
            "x 305-525, y 735-915)", "complete its top (hidden under the arm) as a dark stone wrist block; keep it as ONE closed fist shape"),
           ("pha_le", "the TWO small green CRYSTAL SHARDS floating between the near shoulder and the near arm (around x 445-505, y 530-625)",
            "each shard its own closed shape"),
           ("vai_xa", "the FAR SHOULDER: the rounded grey stone slab behind the pillar at the right of the head (around x 915-1015, "
            "y 320-435)", "complete it into one closed rounded slab about 190 px wide and 170 px tall: the part hidden behind the pillar "
            "continues down and to the left as the same slab")],
    "Q5": [("loi", "the HEART: the cluster of THREE flat leaf-green crystals in the middle of the chest (around x 645-765, y 550-675)",
            "keep only the three crystals together as one closed cluster shape, exactly as they are (no root, no stones)"),
           ("tay_xa", "a NEW piece that is hidden in image 1: the FAR ARM of the statue (it is behind the pillar). Draw it in the EMPTY "
            "top-right corner of the canvas (x 1180-1500, y 40-330), NOT at its hidden place",
            "draw it as one closed piece about 270 px wide and 230 px tall: a thick weathered grey-green stone upper-arm block "
            "(#77806E, the side-face tone, because it is the far side) going down-right into a dark-grey stone forearm and the back of a "
            "dark stone hand (#555C50) at its lower right end, no fingers, no roots, same ink line and crayon hatching as the near arm")],
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: an ancient stone KING STATUE come to life, hunched and turned "
        "to the right, holding a big square stone pillar diagonally across its back with its far hand; a carved king face with narrow "
        "green eyes under a tall pointed crown of three tiers; a big rounded near shoulder slab; a near arm of stacked stones ending in a "
        "dark blocky fist; thick brown tree roots with small green leaves crawling over the shoulder, the arm and the pillar; a cluster "
        "of three green crystals held by a root ring in the chest; floating dark rock chunks instead of legs. Hand-drawn: wobbly "
        "dark-brown ink line, crayon hatching, flat colours.")
STYLE = Q.STYLE


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-17; người dùng chọn B = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{tho5.Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): tượng vua cổ rễ quấn cầm cột vuông. "
          "Mỗi nhóm chỉ giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị che. Gen bằng Magnific (GPT 2.6).", ""]
    for nh, ds in NHOM.items():
        out, save = Q.luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {tho5.Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "CANVAS: landscape 1536x1024, the same frame as image 1.", "",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap between the "
             "kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        Q.ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `tuong_cot_manh.py ghep`); phần bị che vẽ đủ, viền kín; "
           "nền trắng tinh."]
    Q.ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
NHIEU = {"da": (650, 40000), "pha_le": (None, 2500)}      # mảnh nhiều cụm giữ riêng từng cụm: (y tối thiểu, diện tích tối đa)


def cat(chi=None):
    DATJ = Q.nap_dat()
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = Q.moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A, lab, cum = Q._cum(src)
        print(f"{nh} ({os.path.basename(src)}): {len(cum)} cụm")
        slots = [s for s, _, _ in ds]
        rieng = {s: [] for s in slots if s in NHIEU}
        gan = {s: [] for s in slots if s not in NHIEU}
        for i, a, c, st in cum:
            done = False
            for s in rieng:
                ymin, amax = NHIEU[s]
                if (ymin is None or c[1] > ymin) and a < amax and (s != "pha_le" or np.hypot(c[0] - 475, c[1] - 575) < 120):
                    rieng[s].append((i, a, c))
                    done = True
                    break
            if done or not gan:
                if not done:
                    print(f"  bỏ cụm ({c[0]:.0f}, {c[1]:.0f}) {a} px")
                continue
            best = min(gan, key=lambda s: np.hypot(c[0] - TAM[s][0], c[1] - TAM[s][1]))
            gan[best].append(i)
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:9s} KHÔNG THẤY MẢNH")
                continue
            b = Q.luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            print(f"  {s:9s} hộp {b}, {len(ids)} cụm")
        for s, ds_ in rieng.items():
            for k in [k for k in list(DATJ) if k.startswith(s + "_")]:
                del DATJ[k]
            ds_.sort(key=lambda x: (x[2][0], x[2][1]))
            for k, (i, a, c) in enumerate(ds_, 1):
                b = Q.luu_manh(A, lab == i, f"{s}_{k}", DATJ, os.path.basename(src))
                print(f"  {s}_{k:<6d} hộp {b}, {a} px")
    Q.ghi_dat(DATJ)


def phu_goc(slots):
    """khung bao (px concept) của các part gốc ở khung 0 idle."""
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    _, _, atts = G.nap("att_idle0.json")
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["slot"] in slots])
    P = goc_sang_concept(np.stack([W / 2 + (P[:, 0] - cx) * s, H / 2 - (P[:, 1] - cy) * s], 1))
    return P.min(0), P.max(0)


def dat_tay_xa():
    """cánh tay xa GPT vẽ ở góc trống: co đều cho vừa khung bao các part tay xa của con gốc (bắp tay, cẳng tay, mu bàn tay), đặt giữa."""
    DATJ = Q.nap_dat()
    p0, p1 = phu_goc(["P_shoubiL01", "P_shoubiL02", "P_shoubiL03", "P_shoubiL04", "P_shouL01"])
    im = Image.open(os.path.join(MANH, "tay_xa.png")).convert("RGBA")
    k = min((p1[0] - p0[0]) / im.width, (p1[1] - p0[1]) / im.height)
    im2 = im.convert("RGBa").resize((round(im.width * k), round(im.height * k)), Image.LANCZOS).convert("RGBA")
    c = (p0 + p1) / 2
    x0, y0 = int(round(c[0] - im2.width / 2)), int(round(c[1] - im2.height / 2))
    im2.save(os.path.join(MANH, "tay_xa.png"))
    DATJ["tay_xa"] = dict(hop=[x0, y0, x0 + im2.width, y0 + im2.height], nguon=DATJ.get("tay_xa", {}).get("nguon", ""), co=float(k))
    Q.ghi_dat(DATJ)
    print("tay_xa", DATJ["tay_xa"])


def hong(ten="hong", vung_=(490, 790, 425, 590)):
    """khối đá lót giữa cánh tay gần và ngực (concept có, không nhóm nào vẽ; chỗ viên đá số 1 của con gốc): cắt THẲNG từ concept phần chưa
    mảnh nào phủ ở vùng đó, nới 22 px trong hình, trừ chỗ pha lê + đá lơ lửng (chúng bay riêng), lấp lỗ bằng màu đá sẫm của chính nó,
    kẻ lại viền mực dọc mép mới. Vẽ sau cùng (dưới mọi mảnh)."""
    DATJ = Q.nap_dat()
    C = np.asarray(Image.open(CONCEPT).convert("RGB")).astype(np.int32)
    fg = ~Q.nen(C)

    def phu(keys):
        m = np.zeros((H, W), bool)
        for k in keys:
            x0, y0, _, _ = DATJ[k]["hop"]
            a = np.asarray(Image.open(os.path.join(MANH, k + ".png")))[..., 3] > 40
            m[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] |= a
        return m
    cov = phu([k for k in DATJ if k != ten and not k.startswith("hong")] + [k for k in DATJ if k.startswith("hong") and k != ten])
    trong = fg & ~cov
    vung = np.zeros((H, W), bool)
    vung[vung_[0]:vung_[1], vung_[2]:vung_[3]] = True
    trong = cv2.morphologyEx((trong & vung).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
    m = (cv2.dilate(trong.astype(np.uint8), el_(22)) > 0) & fg & vung
    bay = cv2.dilate(phu([k for k in DATJ if k.startswith(("pha_le_", "da_"))]).astype(np.uint8), el_(2)) > 0
    m &= ~bay
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    m = lab == (1 + int(np.argmax(st[1:, 4])))
    lo = m.copy()                                                    # lấp lỗ
    ff = (~m).astype(np.uint8)
    cv2.floodFill(ff, None, (0, 0), 0)
    m |= ff > 0
    rgb = C.astype(np.uint8).copy()
    lum = rgb.mean(2)
    da = m & lo & (lum > 70) & (lum < 160)
    mau = np.median(rgb[da], axis=0).astype(np.uint8)
    rgb[m & ~lo] = mau
    muc = np.median(rgb[m & (lum < 45)], axis=0).astype(np.uint8)
    dist = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    rgb[m & (dist <= 6)] = muc
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    al = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)
    out = np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)])[y0:y1, x0:x1]
    Image.fromarray(out, "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon="cắt từ concept")
    Q.ghi_dat(DATJ)
    print(ten, DATJ[ten])


def el_(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


THU_TU = ["tay_xa", "hong_x", "vai_xa", "hong", "than", "da_*", "cot", "nam_xa", "lung", "dau", "loi", "pha_le_*", "vai_gan", "nam_gan", "tay_gan"]


def thu_tu(DATJ):
    out = []
    for s in THU_TU:
        if s.endswith("*"):
            out += sorted([k for k in DATJ if k.startswith(s[:-1])], key=lambda k: int(k.split("_")[-1]))
        elif s in DATJ:
            out.append(s)
    return out


def ghep():
    DATJ = Q.nap_dat()
    Q.THU_TU = [s for s in thu_tu(DATJ) if s != "tay_xa"]
    Q.ghep()


def can_j():
    return json.load(open(os.path.join(G.MAU, "can.json")))


def goc_sang_concept(P):
    """px khung ca_con của con gốc → px concept (nghịch phép căn)."""
    c = can_j()
    return np.stack([(P[:, 0] - c["tx"]) / c["k"], (P[:, 1] - c["ty"]) / c["k"]], 1)


def tren():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    _, imgs, atts = G.nap("att_idle0.json")
    nhom_cua = {sl: k for k, v in NHOM_GOC.items() for sl in v}
    base = Image.open(CONCEPT).convert("RGB").resize((W, H))
    base = Image.blend(Image.new("RGB", (W, H), "white"), base, 0.55)
    d = ImageDraw.Draw(base)
    f = ImageFont.truetype("arial.ttf", 13)
    for a in atts:
        if not a.get("region"):
            continue
        V = np.array(a["xy"], float).reshape(-1, 2)
        P = np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
        P = goc_sang_concept(P)
        uv, tr = G.luoi(a)
        m = Image.new("L", (W, H), 0)
        dm = ImageDraw.Draw(m)
        for t in tr:
            dm.polygon([tuple(P[i]) for i in t], fill=255)
        M = np.asarray(m) > 0
        cs, _ = cv2.findContours(M.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        col = MAU_NHOM.get(nhom_cua.get(a["slot"]), (255, 0, 0))
        for c in cs:
            d.line([tuple(p[0]) for p in c] + [tuple(c[0][0])], fill=col, width=2)
        ys, xs = np.nonzero(M)
        if len(xs):
            d.text((xs.mean() - 8, ys.mean() - 6), str(a["order"]), fill=col, font=f)
    p = os.path.join(G.MAU, "_rig_tren_concept.png")
    base.save(p)
    print(p)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        Q.can()
    elif cmd == "tren":
        tren()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    elif cmd == "hong":
        hong()
        hong("hong_x", (630, 770, 855, 985))
    elif cmd == "tay_xa":
        dat_tay_xa()
    else:
        print(__doc__)
