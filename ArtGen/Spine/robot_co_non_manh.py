# -*- coding: utf-8 -*-
"""Robot cổ DẠNG 1 NON: MẢNH theo concept A đã duyệt (inbox/robot_co_non/tai_ve/L1_duyet.png: robot con thép mới, đầu vòm to, mỗi vai một ống
xả, giáp vai tròn hai đinh, vải bố vàng nhạt).

Dùng lại hàm của robot_co_manh.py (tờ, cắt, tách mảnh đổi dáng), chỉ thay:
  - phép căn concept ↔ thế giới: theo hình bố cục rig non (robot_co_rig.py bo_cuc → mau/bo_cuc.json, robot_co_non.py khung → bo_cuc_khung.json),
    khớp bằng hình bóng phần dưới cổ (đầu concept cố ý to hơn bố cục);
  - hình bóng từng part ở dáng gốc của rig NON (lấy thẳng từ rig: đỉnh lưới qua xương đã đổi tỉ lệ);
  - CHUYỂN DA (skill "DẠNG KHÁC trên CÙNG rig gốc", bước 4): tờ = mảnh ĐÃ XONG của dạng 2 (inbox/robot_co_1/manh) xếp vào ô, GPT tô lại sang
    thép sáng, bỏ gỉ, bớt đinh, dải da → vải bố; giữ hình bóng. Ngón tay giữ y dạng 2 (sắt sẫm như nhau).
  - Mảnh đổi dáng gen "đúng chỗ, đúng cỡ" trên concept: thân (đầu vòm to + mẩu vây, mặt trơn có mắt, cổ, cổ áo, thân dưới; kèm tờ hình bóng),
    mặt nạ (lỗ tròn quanh mắt), ống xả đơn trái / phải.

    robot_co_non_manh.py can        → mau/can.json
    robot_co_non_manh.py to         mọi tờ + prompt → gui_gpt/robot_co_non/luot_2_*.txt
    robot_co_non_manh.py cat [N1|N2|N3|N4|R]
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

os.environ["RC_DANG"] = "non"
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import robot_co as G  # noqa: E402
import robot_co_rig as RIG  # noqa: E402  (nạp TRƯỚC khi đổi G.BASE: rig tính đường dẫn da dạng 2 từ G.BASE)
import robot_co_manh as M  # noqa: E402
import robot_co_so as SO  # noqa: E402

W, H = M.W, M.H
BASE1 = G.BASE
MANH2 = os.path.join(BASE1, "manh")
BASE = os.path.join(HERE, "inbox", "robot_co_non")
G.BASE, G.MAU, G.TAI = BASE, os.path.join(BASE, "mau"), os.path.join(BASE, "tai_ve")
M.MANH = os.path.join(BASE, "manh")
M.GUI = os.path.join(HERE, "gui_gpt", "robot_co_non")
M.CON = os.path.join(G.TAI, "L1_duyet.png")
DANG2 = os.path.join(BASE1, "tai_ve", "L1_duyet.png")
M.MO, M.BO_SUNG, M.TU_CHE = {}, (), {}
MUC = M.MUC

# màu đo trên concept A non
MAU = dict(thep="#A9AEB6", thep_sang="#C9CDD3", sat="#4A4B50", vai="#CDB98A", dinh="#D9DCE0", mat="#E8A33F")
M.MAU = dict(M.MAU, giap=MAU["thep"], giap_sang=MAU["thep_sang"], giap_toi="#8E939B", sat_toi=MAU["sat"], dinh=MAU["dinh"])
M.MO_TA_CON = ("a small young robot seen from the front, made of bright NEW light steel with no rust: a big round dome head with a short "
               "rounded stub on top, a square visor with ONE round amber eye and three grille slots under it, one short exhaust pipe on "
               "each shoulder, small rounded shoulder pads with two rivets, two chest plates meeting round a small amber light, a pale "
               "khaki canvas apron at the waist, huge round barrel forearms with amber-ringed fist sockets, three thick dark fingers on "
               "each hand resting on the ground, short dark legs")

# ---------------------------------------------------------------- CHUYỂN DA: tờ = mảnh dạng 2 đã xong
TO_N = {
    "N1": [[("vai_trai", 2.0), ("vai_phai", 2.0), ("P_shouR1_4", 2.0), ("P_shouL1_3", 2.0)],
           [("P_shouR1_2", 2.0), ("P_jianjiaR", 2.0), ("P_jianjiaL", 2.0)]],
    "N2": [[("P_xiongjiaR", 2.3), ("P_xiongjiaL", 2.3), ("P_wuqi1", 2.3), ("P_wuqi2", 2.3)],
           [("P_shouR2_1", 2.3), ("P_shouL2_1", 2.3)]],
    "N3": [[("P_shouR2_2", 2.2), ("P_shouR2_22", 2.2), ("P_shouL2_22", 2.2), ("P_shouL2_2", 2.2)],
           [("P_butiao4", 2.2), ("P_butiao1", 2.2), ("P_butiao2", 2.2), ("P_butiao3", 2.2)]],
    "N4": [[("P_shouL1_2", 2.2), ("khoi_trai", 2.2), ("tay_may_ong", 2.2), ("tay_may_can", 2.2)]],
}
NGON = [f"P_shou{s}3_{i}{j}" for s in ("R", "L") for i in (1, 2, 3) for j in ("a", "b")]      # giữ y dạng 2
TOM_N = {"N1": "seven armour parts: top row the front of the left shoulder pad, the front of the right shoulder pad, the inner (back) face "
               "of the left pad, the inner face of the right pad; bottom row a thin edge strip of the left pad and two small collar plates",
         "N2": "top row the left chest plate, the right chest plate, the missile pod full of missiles, the same pod empty; bottom row the left "
               "forearm and the right forearm (huge round barrel shells, each ending in a round fist socket)",
         "N3": "top row the left leg, two small toes, two small toes, the right leg; bottom row four strips that hang from the waist (the third "
               "one wide)",
         "N4": "four arm parts: the right upper-arm block, the left upper-arm block, the sleeve of the telescopic right upper arm, the piston "
               "rod that slides out of that sleeve"}
_THEP = (f"bright NEW light steel {MAU['thep']} instead of the dark gunmetal, light steel {MAU['thep_sang']} instead of the light "
         f"gunmetal rims and bands, rivets light {MAU['dinh']}; very dark iron parts become dark iron {MAU['sat']}; REMOVE every rust patch")
MO_TA_N = {
    "vai_trai": f"the FRONT of the LEFT SHOULDER PAD: {_THEP}; keep only TWO round rivets (near its lower rim).",
    "vai_phai": f"the FRONT of the RIGHT SHOULDER PAD: {_THEP}; keep only TWO round rivets.",
    "P_shouR1_4": f"the INNER (back) FACE of the left shoulder pad: a slightly darker steel #8E939B, light steel rim, no rivets.",
    "P_shouL1_3": f"the INNER (back) FACE of the right shoulder pad: steel #8E939B, light steel rim, no rivets.",
    "P_shouR1_2": f"a thin edge strip of the left pad: light steel {MAU['thep_sang']}.",
    "P_jianjiaR": "a small collar plate: steel #8E939B, one rim line.",
    "P_jianjiaL": "a small collar plate: steel #8E939B, one rim line.",
    "P_xiongjiaR": f"the LEFT CHEST PLATE: {_THEP}; keep only TWO rivets; the dark part along the half-circle cut dark iron {MAU['sat']}.",
    "P_xiongjiaL": f"the RIGHT CHEST PLATE: {_THEP}; keep only TWO rivets.",
    "P_wuqi1": f"the MISSILE POD full of missiles: keep it as it is (dark iron frame {MAU['sat']}, seven amber tips {MAU['mat']} in thin steel "
               "rings).",
    "P_wuqi2": f"the SAME POD empty: keep it as it is (seven empty dark holes in thin steel rings).",
    "P_shouR2_1": f"the LEFT FOREARM: {_THEP}; ONE plain light steel band instead of the two riveted bands (no rivets); the fist socket dark "
                  f"iron with its amber ring; the small spike at its top becomes a small rounded steel cap.",
    "P_shouL2_1": "the RIGHT FOREARM: the same as the left forearm.",
    "P_shouR2_2": f"the LEFT LEG: dark iron {MAU['sat']} with a light steel {MAU['thep']} plate on its outer side (one rivet); the spike on its "
                  "top becomes a small rounded dark iron cap.",
    "P_shouR2_22": f"two small toes: dark iron {MAU['sat']}.",
    "P_shouL2_22": f"two small toes: dark iron {MAU['sat']}.",
    "P_shouL2_2": "the RIGHT LEG: the same as the left leg.",
    "P_butiao4": f"a narrow strip of pale KHAKI CANVAS cloth {MAU['vai']} with a dashed stitched line along its edges, its lower end cut "
                 "straight with a small point (not torn); no rivet, no leather.",
    "P_butiao1": "another narrow khaki canvas strip: the same.",
    "P_butiao2": f"the wide middle strip: pale khaki canvas {MAU['vai']} with two dashed stitched lines dividing it in three, its lower end "
                 "cut into a point (not torn); no rivets.",
    "P_butiao3": "another narrow khaki canvas strip: the same.",
    "P_shouL1_2": f"the RIGHT UPPER-ARM BLOCK: dark iron {MAU['sat']}; its steel plate light steel {MAU['thep']} with a light rim, no rust, "
                  "no rivets; the two small spikes at its lower end become two small rounded caps.",
    "khoi_trai": f"the LEFT UPPER-ARM BLOCK: dark iron {MAU['sat']}; the two small spikes at its lower left become two small rounded caps.",
    "tay_may_ong": f"the upper-arm SLEEVE: {_THEP}; one plain light steel band near each end, no rivets.",
    "tay_may_can": f"the PISTON ROD: dark iron {MAU['sat']} with one thin light steel ring near its middle.",
}


def vung_non():
    """mảnh dạng 2 đã xong (1 px / đơn vị) thu về 0,5 px / đơn vị (cỡ 'ảnh vùng' cho to_k / cat_k)."""
    out = {}
    for h_ in TO_N.values():
        for hang_ in h_:
            for r, _ in hang_:
                im = Image.open(os.path.join(MANH2, r + ".png")).convert("RGBA")
                im2 = im.convert("RGBa").resize((max(2, im.width // 2), max(2, im.height // 2)), Image.LANCZOS).convert("RGBA")
                out[r] = ({"region": r}, im2)
    return out


M.vung = vung_non
M.TO_K = TO_N
M.TOM_K = TOM_N
M.MO_TA_K = MO_TA_N
M.VI_K = {"N1": "giáp vai trước / sau, mép giáp vai, hai giáp cổ", "N2": "hai giáp ngực, lõi tên lửa (đủ + rỗng), hai cẳng tay",
          "N3": "hai chân, ngón chân, bốn dải vải bố", "N4": "khối bắp tay phải / trái, ống bọc + cần pít-tông tay máy"}


def prompt_n(ten, o):
    mau = os.path.join(G.MAU, f"goc_{ten}.png")
    out = os.path.join(G.TAI, f"D_{ten}.png")
    p = os.path.join(M.GUI, f"luot_2_da_{ten}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {M.Wp(mau)}: the PARTS SHEET, 1536x1024, white background: {TOM_N[ten]} of a 2D animation puppet (a robot), each drawn "
         "alone at the exact size and place to keep. They are already drawn in our hand-drawn style, with the rusty dark gunmetal colours "
         "of the robot's FINAL form.",
         f"image 2 = {M.Wp(M.CON)}: the APPROVED picture of the robot's YOUNG form: {M.MO_TA_CON}. Take from it the new colours and "
         "materials.",
         "", f"SAVE: save it as a PNG to {M.Wp(out)}",
         f"If a file with that name already exists, save as D_{ten}_2.png, D_{ten}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: RECOLOUR. Redraw the SAME sheet with every part REPAINTED in the colours of image 2 as described below. For EVERY part keep "
         "exactly its silhouette (the same outline), its size, its orientation and its place on the sheet (if the new picture were laid "
         "over image 1, every part must coincide with the old one), and its main structural lines. Do NOT merge, add or move parts. Pure "
         "white (#FFFFFF) between the parts.", "",
         f"STYLE: the same hand-drawn style as image 1: wobbly dark-brown ink outline ({MUC}, about 9 px) round every part, thinner ink lines "
         "inside, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, no highlights, no gradients, no "
         "glow, no shadows. VERY SIMPLE: fewer details than image 1.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {MO_TA_N[r]}")
    t += ["", "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."]
    M.ghi(p, t)
    print(p)
    return p, mau, out


# ---------------------------------------------------------------- phép căn concept non ↔ thế giới rig non
def can():
    """concept → khung bố cục: tỉ lệ + dời, khớp bằng hình bóng phần dưới cổ (y khung > 330)."""
    bc = os.path.join(G.MAU, "bo_cuc_khung.png")
    g = M.mat_na(np.asarray(Image.open(bc).convert("RGB")))
    m = M.mat_na(np.asarray(Image.open(M.CON).convert("RGB").resize((W, H))))
    g2 = g.copy()
    g2[:330] = False
    m2 = m.copy()
    m2[:330] = False                                         # cùng ngưỡng xấp xỉ: tinh chỉnh bằng vòng lặp
    iou, a, tx, ty = SO.khop(m2, g2)
    json.dump(dict(iou=round(float(iou), 4), a=float(a), tx=float(tx), ty=float(ty)), open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print(f"căn (dưới cổ): a {a:.3f}, dời {tx:.1f},{ty:.1f}, IoU {iou:.3f}")


def phep_can():
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    b = json.load(open(os.path.join(G.MAU, "bo_cuc.json")))
    kj = json.load(open(os.path.join(G.MAU, "bo_cuc_khung.json")))
    x0, y0, x1, y1 = b["box"]
    sc, k, ox, oy = b["scale"], kj["k"], kj["ox"], kj["oy"]
    a, tx, ty = j["a"], j["tx"], j["ty"]

    def T(V):
        V = np.asarray(V, float).reshape(-1, 2)
        Pk = np.stack([(V[:, 0] - x0) * sc * k + ox, (y1 - V[:, 1]) * sc * k + oy], 1)
        return (Pk - np.array([tx, ty])) / a

    def Ti(P):
        P = np.asarray(P, float).reshape(-1, 2) * a + np.array([tx, ty])
        return np.stack([(P[:, 0] - ox) / (sc * k) + x0, y1 - (P[:, 1] - oy) / (sc * k)], 1)
    return T, Ti, sc * k / a


_CK = {}


def lop_goc():
    """{slot: (None, mặt nạ bool trên khung concept)} các hình đang bật ở dáng gốc của rig NON (dựng rig bằng da dạng 2)."""
    if "lop" in _CK:
        return _CK["lop"]
    from PIL import ImageDraw
    T, _, _ = phep_can()
    cu = RIG.MANH
    RIG.MANH = MANH2                                         # dựng rig non bằng TRỌN da + moi.json dạng 2 (đúng hình bố cục)
    try:
        sk, _ = RIG.dung()
    finally:
        RIG.MANH = cu
    from quai.soi import _tris
    lop = {}
    for sl in sk.slots:
        if sl["alpha"] <= 0 or not sl.get("att"):
            continue
        sp = sk.atts[sl["name"]].get(sl["att"])
        if sp is None:
            continue
        # hình bóng THẬT (alpha ảnh qua lưới), không phải ô lưới: mảnh cứng là ô chữ nhật
        imp = sk.images[sp["path"]].convert("RGBa")
        uv = np.asarray(sp["uv"], float) * np.array([imp.width, imp.height])
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, imp, T(sp["V"]), uv, np.asarray(sp["tris"], int))
        lop[sl["name"]] = (None, np.asarray(lay)[..., 3] > 110)
    _CK["lop"] = (lop, None, list(lop))
    return _CK["lop"]


M.phep_can = phep_can
M.lop_goc = lop_goc


def huong_than():
    """hình bóng THÂN non: thân của rig non bỏ chỏm (phần trên 70 % mặt nạ) ∪ khối đầu concept A (hộp x 575–995, y 50–395)."""
    lop, _, _ = lop_goc()
    m_than = lop["P_shenti"][1].copy()
    ys, xs = np.nonzero(lop["P_tou1"][1])
    m_than[:int(np.percentile(ys, 70))] = False
    Cn = np.asarray(Image.open(M.CON).convert("RGB").resize((W, H), Image.LANCZOS))
    cm = M.mat_na(Cn)
    hop = np.zeros((H, W), bool)
    hop[50:395, 575:995] = True
    dau = cm & hop
    n, lab, st, _ = cv2.connectedComponentsWithStats(dau.astype(np.uint8), 8)
    if n > 1:
        dau = lab == 1 + int(np.argmax(st[1:, 4]))
    m = cv2.morphologyEx((m_than | dau).astype(np.uint8), cv2.MORPH_CLOSE, M.el(9)).astype(bool)
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m2 = np.zeros((H, W), np.uint8)
    cv2.drawContours(m2, cs, -1, 1, -1)
    g = np.full((H, W, 3), 255, np.uint8)
    g[m2.astype(bool)] = (214, 214, 214)
    cv2.drawContours(g, cs, -1, M.INK, 6)
    p = os.path.join(G.MAU, "huong_than.png")
    Image.fromarray(g).save(p)
    np.save(os.path.join(G.MAU, "huong_than.npy"), m2.astype(bool))
    print(p)
    return p


M.huong_than = huong_than

M.R = {
    "R1": [("than", "P_shenti", "bone4",
            "the BODY of the young robot, filling EXACTLY the light grey shape of image 2 (same outline, same place): at the top the BIG "
            f"round DOME HEAD in bright light steel {MAU['thep']} with its short rounded STUB on top, complete; on the front of the dome the "
            f"FACE AREA: plain dark iron {MAU['sat']} with the ONE round EYE exactly where the eye is in image 1 (flat amber {MAU['mat']} inside "
            f"its ink outline, one small white dot, a thin dark ring round it); the short NECK with its row of small round holes; under the "
            f"neck a plain light steel COLLAR plate (hidden behind the chest plates in image 1: draw it plain, one rim line); then the ROUND "
            f"LOWER BODY in dark iron {MAU['sat']} with the two pale grey curved plates on its sides, going down to the rounded bottom of the "
            "grey shape (hidden behind the apron in image 1: continue the dark body). WITHOUT the square visor and its grille slots, WITHOUT "
            "the chest plates, the shoulder pads, the pipes, the arms, the hands, the apron and the legs")],
    "R2": [("mat_na", "P_tou1", "bone39",
            f"the FACE PLATE: the square light steel {MAU['thep_sang']} VISOR on the front of the head with its three grille slots under "
            "the eye, complete; where the eye is, the visor has a round HOLE: leave the inside of the eye ring PURE WHITE (the eye is on "
            "another part and shows through); keep the dark ink ring round the hole"),
           ("ong_xa_trai", None, "bone27",
            "the short EXHAUST PIPE on the viewer's LEFT shoulder: the stubby light steel tube with its thick rim and dark inside, complete "
            "down to its round base (the part hidden behind the shoulder pad is drawn too)"),
           ("ong_xa_phai", None, "bone8",
            "the short EXHAUST PIPE on the viewer's RIGHT shoulder: the same kind of stubby light steel tube, complete down to its round "
            "base")],
}
M.VI_R = {"R1": "thân: đầu vòm to + mẩu vây, mặt trơn có MẮT, cổ lỗ tròn, cổ áo, thân dưới tròn sẫm (theo hình bóng tờ 2)",
          "R2": "mặt nạ vuông ba khe (lỗ tròn quanh mắt), ống xả đơn trái, ống xả đơn phải"}
TAM_R2 = {"mat_na": (778, 300), "ong_xa_trai": (512, 350), "ong_xa_phai": (1035, 350)}


def tam_r():
    lop, _, _ = lop_goc()
    ys, xs = np.nonzero(lop["P_shenti"][1])
    return {"R1": {"than": (float(xs.mean()), float(ys.mean()))}, "R2": dict(TAM_R2)}


M.tam_r = tam_r


def chuan_bi_moi():
    """moi.json của dạng non = của dạng 2 (giáp vai trước, khối bắp tay trái: hình bóng giữ, ảnh chuyển da cùng tên) trừ các mảnh gen lại."""
    os.makedirs(M.MANH, exist_ok=True)
    pj = os.path.join(M.MANH, "moi.json")
    if os.path.exists(pj):
        return
    moi = json.load(open(os.path.join(MANH2, "moi.json")))
    for k in ("than", "mat_na", "ong_xa_trai", "ong_xa_phai"):
        moi.pop(k, None)
    json.dump(moi, open(pj, "w"), indent=1)


def sua_moi_ong():
    """ống xả gen mới (đúng cỡ concept non): mảnh THÊM trên xương vai, không co thêm."""
    pj = os.path.join(M.MANH, "moi.json")
    moi = json.load(open(pj))
    for k in ("ong_xa_trai", "ong_xa_phai"):
        if k in moi:
            moi[k].update(slot=None, them_truoc="P_shouL1_2", co=1.0)
    json.dump(moi, open(pj, "w"), indent=1)


def chep_ngon():
    import shutil
    os.makedirs(M.MANH, exist_ok=True)
    for r in NGON:
        shutil.copy(os.path.join(MANH2, r + ".png"), os.path.join(M.MANH, r + ".png"))


def doi_mau(A, vai=False):
    """CHUYỂN DA BẰNG MÃ (2026-11-16 16:2x Codex hết hạn mức tới 19:01): đổi bảng màu mảnh dạng 2 sang thép sáng của concept A non, giữ vân
    sáp + nét mực (ánh xạ độ sáng đơn điệu). Mực nâu, hổ phách giữ; gỉ cam → thép chính; da nâu → vải bố khaki (vai=True); xám trung tính: độ
    sáng nguồn [59 sắt sẫm, 75 thép tối, 108 thép, 145 viền, 165 đinh] → đích [75, 146, 174, 203, 219], nhuộm sắc lam nhẹ của thép concept."""
    B = A[..., :3].astype(np.float32)
    r_, g_, b_ = B[..., 0], B[..., 1], B[..., 2]
    lum = B.mean(2)
    muc = (lum < 52) | ((lum < 66) & (r_ - b_ > 14))
    ho_phach = (r_ > 170) & (g_ > 105) & (g_ < 200) & (b_ < 120)
    if vai:                                                           # dải da: mọi điểm ngả nâu / cam (kể cả sáng như gỉ) là da
        da = (r_ - b_ > 15) & ~ho_phach & ~muc
        gi = np.zeros_like(da)
    else:
        gi = (r_ - b_ > 14) & (r_ > g_ + 4) & ~ho_phach & ~muc          # cả đốm gỉ nhạt (ngả hồng) ở mép mảng gỉ
        da = (r_ - b_ > 18) & (lum > 50) & (lum < 125) & ~gi & ~ho_phach & ~muc
    xam = ~muc & ~ho_phach & ~gi & ~da
    out = B.copy()
    l_dich = np.interp(lum, [59, 75, 108, 145, 165, 255], [75, 146, 174, 203, 219, 255])
    sac = np.array([0.965, 0.99, 1.045], np.float32)                 # sắc lam nhẹ của thép #A9AEB6
    out[xam] = (l_dich[xam, None] * sac)
    # gỉ: thép chính, giữ dao động sáng tối của vân (lệch so với trung bình vùng)
    tb = cv2.GaussianBlur(lum, (0, 0), 6)
    out[gi] = ((174 + 0.8 * (lum - tb))[gi, None] * sac)
    if vai:
        kh = np.array([0xCD, 0xB9, 0x8A], np.float32)
        out[da] = kh * (1 + 0.006 * (lum - tb))[da, None]
    else:
        out[da] = (l_dich[da, None] * sac)
    A2 = A.copy()
    A2[..., :3] = np.clip(out, 0, 255).astype(np.uint8)
    return A2


def doi_mau_het():
    os.makedirs(M.MANH, exist_ok=True)
    so = []
    for h_ in TO_N.values():
        for hang_ in h_:
            for r, _ in hang_:
                A = np.asarray(Image.open(os.path.join(MANH2, r + ".png")).convert("RGBA"))
                A2 = doi_mau(A, vai=r.startswith("P_butiao"))
                im = Image.fromarray(A2, "RGBA")
                im.save(os.path.join(M.MANH, r + ".png"))
                so.append(im)
                print("  đổi màu", r)
    M._to_so(so, os.path.join(M.MANH, "_so_doi_mau.png"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    chep_ngon()
    chuan_bi_moi()
    for ten in TO_N:
        prompt_n(ten, M.to_k(ten))
    huong_than()
    M.prompt_r()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "doi_mau":
        doi_mau_het()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ten in TO_N:
            if chi in ("", ten):
                M.cat_k(ten)
        if chi in ("", "R"):
            chuan_bi_moi()
            M.cat_r()
            sua_moi_ong()
    else:
        print(__doc__)
