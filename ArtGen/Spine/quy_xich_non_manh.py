# -*- coding: utf-8 -*-
"""Quỷ xích DẠNG 1 NON: MẢNH theo concept A đã duyệt (inbox/quy_xich_non/tai_ve/L1_duyet.png: quỷ con đội nồi sắt).

Dùng lại hàm của quy_xich_manh.py (tờ thân liền, cắt, tách mảnh đổi dáng), chỉ thay:
  - phép căn concept ↔ thế giới: theo hình bố cục rig non (quy_xich_rig.py bo_cuc → mau/bo_cuc.json, quy_xich_non.py khung →
    bo_cuc_khung.json), tinh chỉnh bằng hình bóng phần THÂN (đầu của bố cục còn mũ + sừng dạng 2, cao hơn nồi);
  - hình bóng từng part ở dáng gốc của rig NON (đầu × 1,25...): đỉnh lưới gốc của họ đưa qua xương đã đổi tỉ lệ;
  - bảng màu, prompt, danh sách mảnh đổi dáng (nồi, hai sừng con, vạt da vai, vòng sắt, móc gỉ).
Mảnh giữ y dạng 2 (cánh, mặt, đuôi, sáu ngón, hai mắt xích) chép từ inbox/quy_xich_1/manh. Ẩn ở rig non: má mũ, ba vây, giáp vai nhỏ, hai
giáp cổ.

    quy_xich_non_manh.py can        → mau/can.json
    quy_xich_non_manh.py to         tờ thân liền + hai tờ mảnh đổi dáng + prompt → gui_gpt/quy_xich_non/luot_2_*.txt; chép mảnh dùng lại
    quy_xich_non_manh.py cat [LIEN|R]
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

os.environ["QX_DANG"] = "non"
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quy_xich as G  # noqa: E402
import quy_xich_manh as M  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = M.W, M.H
BASE1 = G.BASE
BASE = os.path.join(HERE, "inbox", "quy_xich_non")
G.BASE, G.MAU, G.TAI = BASE, os.path.join(BASE, "mau"), os.path.join(BASE, "tai_ve")
M.MANH = os.path.join(BASE, "manh")
M.GUI = os.path.join(HERE, "gui_gpt", "quy_xich_non")
M.CON = os.path.join(G.TAI, "L1_duyet.png")
DANG2 = os.path.join(BASE1, "tai_ve", "L1_duyet.png")
MUC = M.MUC

# màu đo trên concept A non (trung vị ô 7 × 7)
M.MAU = dict(da="#CE452E", quan="#62493D", day="#BC8850", sat="#69666A", vai_da="#865339", gi="#A16443", sung="#EDD2A1",
             vuot="#3A3236", thep="#9FA2A7")
M.BANG = {"P_duzi": ("da", "quan", "day"), "P_xionqiang": ("da",), "P_bozi": ("da",),
          "P_shouR1": ("da",), "P_shouR2": ("da",), "P_shouL1": ("da",), "P_shouL2": ("da",),
          "P_tuiL1": ("da", "vuot"), "P_tuiL2": ("da", "vuot"), "P_tuiR1": ("da", "vuot"), "P_tuiR2": ("da", "vuot")}
DUNG_LAI = ("P_chibang", "P_tou", "P_weiba", "P_shouR31", "P_shouR32", "P_shouR33", "P_shouL31", "P_shouL32", "P_shouL33",
            "W_suolian1", "W_suolian2")
AN = ("P_toukui1", "P_toukui3", "P_jiejing1", "P_jiejing2", "P_jiejing3", "P_jianjiaL", "P_xiongjiaL1", "P_xiongjiaR1")

M.R = {
    "R1": [("noi", "P_toukui2", "bone55",
            "the IRON COOKING POT worn as a helmet: the whole upside-down pot with its rim and the small loop handle on its left side, "
            "complete on its own, WITH the two holes where the horns come out (draw the holes as small dark openings; draw NO horns)"),
           ("vai_da", "P_jianjiaR", "bone26",
            "the LEATHER SHOULDER PAD on the viewer's left shoulder with its little tied strap and knot, complete (the part hidden behind "
            "the arm and the chain is drawn too)"),
           ("vong", "P_suo", "bone40",
            "the small round IRON RING in the middle of the chest where the two chains cross, complete, WITHOUT the chains (its middle "
            "hole stays pure white)"),
           ("moc", "W_wuqi", "bone14b2",
            "the small rusty HOOK WEAPON: the J-shaped iron hook with its rust patches at the top, the collar, the whole thin iron SHAFT "
            "going down (complete where the fist covered it: a straight even shaft) and the small round RING at its lower end, WITHOUT "
            "the fist, WITHOUT the chain")],
    "R2": [("sung_to", "P_jiaoL1", "bone11",
            "the RIGHT HORN: the short stubby ivory horn on the right of the pot, complete down to its round base (the base that was "
            "inside the pot is drawn too, about as long again as the visible part)"),
           ("sung_nho", "P_jiaoR1", "bone11",
            "the LEFT HORN: the short stubby ivory horn on the left of the pot, complete down to its round base (the base that was inside "
            "the pot is drawn too, about as long again as the visible part)")],
}
M.VI_R = {"R1": "nồi sắt (có quai, hai lỗ sừng), vạt da vai, vòng sắt, móc gỉ (lưỡi + khâu + cán đủ + vòng cuối)",
          "R2": "hai sừng con vẽ đủ gốc"}
M.TAM_R = {"R1": {"noi": (780, 320), "vai_da": (600, 540), "vong": (800, 590), "moc": (1090, 620)},   # tâm mảnh trên tờ GPT lượt đầu
           "R2": {"sung_nho": (758, 245), "sung_to": (888, 268)}}
M.THEO_GOC = ()
M.CHINH = {}


# ================================================================ căn: thế giới dáng gốc NON → px concept
def _bo_cuc():
    b = json.load(open(os.path.join(G.MAU, "bo_cuc.json")))
    k = json.load(open(os.path.join(G.MAU, "bo_cuc_khung.json")))
    return b["box"][0], b["box"][3], b["scale"], k["k"], k["ox"], k["oy"]


def can():
    """tinh chỉnh (a, dx, dy) quanh tâm khung để hình bóng THÂN (dưới y 420) của bố cục trùng concept nhất."""
    g = M.mat_na(np.asarray(Image.open(os.path.join(G.MAU, "bo_cuc_khung.png")).convert("RGB")))
    c = M.mat_na(np.asarray(Image.open(M.CON).convert("RGB").resize((W, H))))
    g[:420] = False
    c[:420] = False
    C = np.array([W / 2, H / 2])
    best = (0, 1.0, 0, 0)
    for a in np.arange(0.95, 1.051, 0.01):
        for dx in range(-24, 25, 3):
            for dy in range(-24, 25, 3):
                Mx = np.float32([[a, 0, C[0] - a * C[0] + dx], [0, a, C[1] - a * C[1] + dy]])
                w = cv2.warpAffine(g.astype(np.uint8), Mx, (W, H), flags=cv2.INTER_NEAREST).astype(bool)
                v = (w & c).sum() / max(1, (w | c).sum())
                if v > best[0]:
                    best = (v, a, dx, dy)
    x0, y1, sc, k, ox, oy = _bo_cuc()
    out = dict(iou_than=round(float(best[0]), 4), a=float(best[1]), dx=float(best[2]), dy=float(best[3]), x0=x0, y1=y1, sc=sc, k=k, ox=ox, oy=oy)
    json.dump(out, open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print("căn:", out)


def phep_can():
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    C = np.array([W / 2, H / 2])

    def P0(V):
        V = np.asarray(V, float).reshape(-1, 2)
        return np.stack([j["ox"] + j["k"] * (V[:, 0] - j["x0"]) * j["sc"], j["oy"] + j["k"] * (j["y1"] - V[:, 1]) * j["sc"]], 1)

    def T(V):
        return C + j["a"] * (P0(V) - C) + np.array([j["dx"], j["dy"]])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([j["dx"], j["dy"]]) - C) / j["a"] + C
        return np.stack([j["x0"] + (P[:, 0] - j["ox"]) / (j["k"] * j["sc"]), j["y1"] - (P[:, 1] - j["oy"]) / (j["k"] * j["sc"])], 1)
    return T, Ti, j["k"] * j["sc"] * j["a"]


# ================================================================ hình bóng từng part ở dáng gốc NON
_CK = {}


def lop_goc():
    if "lop" in _CK:
        return _CK["lop"]
    os.environ["QX_MANH"] = os.path.join(BASE1, "manh")     # chỉ cần xương đã đổi tỉ lệ: dựng tạm bằng da dạng 2
    import quy_xich_rig as R
    sk, _ = R.dung()
    Wi = sk.the_gioi()
    T, _, _ = phep_can()
    G._C.pop("att", None)
    _, imgs, atts_idle = G.nap("att_idle0.json")
    hien = [a["slot"] for a in atts_idle if a.get("region")]
    by = {a["slot"]: a for a in R.AG["atts"]}
    lop, top, thu_tu = {}, np.full((H, W), -1, np.int32), []
    for k_, sl in enumerate(hien):
        a = dict(by[sl])
        ws = a.get("w")
        xy = np.array(a["xy"], float).reshape(-1, 2)
        V = []
        for i, p in enumerate(xy):
            lst = [(R.NB[b], w) for b, w in ws[i] if w > 0] if ws else [(a["bone"], 1.0)]
            tong = sum(w for _, w in lst)
            v = np.zeros(2)
            for bn, w in lst:
                bn2 = "move" if bn == "root" else bn
                lp = np.linalg.solve(R.WG[bn], np.array([p[0], p[1], 1.0]))
                v += w / tong * (Wi[bn2] @ lp)[:2]
            V.append(v)
        a["xy"] = np.array(V).ravel().tolist()                 # đỉnh ở dáng gốc non (cat_lien / _the_gioi_o đọc trường này)
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(V)), uv, tr)
        m = np.asarray(lay)[..., 3] > 110
        lop[sl] = (a, m)
        top[m] = k_
        thu_tu.append(sl)
    _CK["lop"] = (lop, top, thu_tu)
    return _CK["lop"]


M.phep_can = phep_can
M.lop_goc = lop_goc


# ================================================================ prompt
def prompt_lien():
    gd = os.path.join(G.MAU, "lien.png")
    out = os.path.join(G.TAI, "N_lien.png")
    p = os.path.join(M.GUI, "luot_2_than_lien.txt")
    C_ = M.MAU
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {M.Wp(M.CON)}: the APPROVED character, 1536x1024, white background: a fat little red demon kid wearing an iron cooking "
         "pot as a helmet, small maroon bat wings, a leather shoulder pad, two chains crossing the bare chest with an iron ring, a rope "
         "belt over dark brown short pants, bare red arms and bare red feet with small dark claws, a thin red devil tail, holding a small "
         "rusty hook on a chain. It gives the design, the colours, the ink line and the crayon hatching.",
         f"image 2 = {M.Wp(gd)}: BODY GUIDE, 1536x1024, white background, assembled by computer from image 1: FIVE separate flat shapes, "
         "each with a dark outline: in the MIDDLE the fat BODY (the bare red chest and huge round bare red belly with a small navel, the "
         "rope belt, the dark brown short pants at the bottom, the red neck at the top); at the LEFT the NEAR ARM (a fat bare red arm "
         "hanging down: upper arm and forearm in one shape); at the RIGHT the FAR ARM (a fat bare red arm bent forward: upper arm, forearm "
         "and the base of the fist in one shape); at the bottom left and bottom right the TWO SHORT LEGS (a stubby bare red leg with a "
         "foot and small dark claws). Some places of image 2 are blurry smears: there the shape was hidden under other parts (the head, "
         "the shoulder pad, the chains, the hands) and the computer only spread the nearest colour.",
         "", f"SAVE: save it as a PNG to {M.Wp(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY every "
         "silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, the five "
         "shapes must coincide). This sheet will be cut by a program into the body parts of a 2D animation puppet.", "",
         "VERY IMPORTANT, EACH SHAPE IS ONE CONTINUOUS SURFACE: draw the dark-brown ink outline ONLY around the OUTSIDE of each of the "
         "five shapes. Inside a shape draw no line where the upper arm meets the forearm, where the chest meets the belly, where the leg "
         "meets the foot; no folds, no creases, no cut lines. Clean up every blurry smear: continue the surrounding design through it.",
         "",
         f"- BODY (middle): flat red skin {C_['da']} over the chest and the round belly, one small navel line on the belly as in image 1; "
         f"the thick twisted ROPE belt ({C_['day']}, a few twist lines) round the waist exactly where image 2 shows it; under it the dark "
         f"brown short pants ({C_['quan']}) down to the bottom of the shape. Where the chains, the ring, the hands and the shoulder pad lay "
         "in image 1 just continue the skin: draw NO chains, NO ring, NO shoulder pad, NO hands on the body.",
         f"- ARMS: plain flat red skin {C_['da']}, no bracers, no fingers, no claws (they are separate parts).",
         f"- LEGS: plain red skin {C_['da']}, the stubby foot at the bottom with two or three small pointed dark claws {C_['vuot']} at its "
         "front edge.",
         f"- OUTLINE: dark-brown ink ({MUC}), about 7 px thick on this canvas, wobbly like a real pen, closed around each shape and lying "
         "just INSIDE its edge.",
         "Draw nothing else: no head, no wings, no horns, no tail, no chains, no hook, no ground.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no darker "
         "side, no highlights, no gradients, no cast shadows. Pure white (#FFFFFF) background; no text, no labels, no frames."]
    M.ghi(p, t)
    print(p)
    return p, gd, out


def prompt_r():
    ps = []
    for ma, ds in M.R.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(M.GUI, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {M.Wp(M.CON)}: the APPROVED picture of OUR character, 1536x1024, white background: a fat little red demon kid "
             "wearing a dented iron cooking pot as a helmet with two short ivory horns poking out, a leather shoulder pad, two chains "
             "crossing the chest with a small iron ring, a rope belt, holding a small rusty hook on a chain.",
             "", f"SAVE: save it as a PNG to {M.Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} pieces listed below, each in the SAME POSITION and at the SAME SIZE as in "
             "image 1 (if your picture were laid over image 1, every piece must sit exactly on its old place). REMOVE everything else "
             "(the body, the face, the arms, the wings, the tail, the chains, the legs and the other pieces) and leave pure white there. "
             "COMPLETE every piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were hidden "
             "behind other things in image 1 are drawn too, continuing its shape naturally. The pieces stay separate from each other (a "
             "little white gap between them is fine, do not merge them).", "",
             "THE PIECES:"]
        t += [f"{i}. {mt}." for i, (_, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, "
              "no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        M.ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


def sua_noi():
    """nồi (manh/noi.png): (1) bỏ LÒNG NỒI tối GPT vẽ dưới vành (nó đè lên mắt: mắt rig non ở y 378–408 px concept, ngay dưới vành):
    mỗi cột cắt mọi điểm thấp hơn điểm sáng thấp nhất của vành 7 px (giữ nét mực dưới vành); (2) lấp hai lỗ sừng (hai sừng đặt SAU nồi
    như sừng phải của con gốc, nhô lên khỏi đỉnh nồi; sừng thật không chui đúng lỗ được vì sừng phải nằm sau mũ)."""
    p_ = os.path.join(M.MANH, "noi.png")
    im = np.asarray(Image.open(p_).convert("RGBA")).copy()
    rgb = im[..., :3].astype(np.int32)
    lum = rgb.mean(2)
    sat = rgb.max(2) - rgb.min(2)
    vanh = (lum > 135) & (sat < 40) & (im[..., 3] > 200)
    h, w = lum.shape
    # dải vành = vùng sáng liền TRẢI RỘNG nhất ở nửa dưới (vân sáp sáng lẻ tẻ trong lòng nồi không tính); mép dưới làm trơn qua 25 cột
    vv = cv2.morphologyEx(vanh.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3)))
    vv[: int(h * 0.45)] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(vv, 8)
    j = 1 + int(np.argmax(st[1:, 2])) if n > 1 else 0
    dai = lab == j
    xs_ = [x for x in range(w) if dai[:, x].any()]
    day = np.array([np.nonzero(dai[:, x])[0].max() for x in xs_], float)
    day = np.array([np.median(day[max(0, i - 12):i + 13]) for i in range(len(day))])
    duoi = np.interp(np.arange(w), xs_, day)
    cat_ = 0
    for x in range(min(xs_), w):                          # quai bên trái (ngoài dải vành, cao hơn vành) không cắt
        y_ = int(round(duoi[x])) + 7
        cat_ += int((im[y_:, x, 3] > 0).sum())
        im[y_:, x, 3] = 0
    d = json.load(open(os.path.join(M.MANH, "moi.json")))["noi"]
    x0, y0 = d["hop"][0], d["hop"][1]
    _, _, spx = phep_can()
    k = (M.RES * 0.5) / spx
    lo = np.zeros((h, w), np.uint8)
    for cx, cy in ((765, 248), (882, 265)):                 # tâm hai lỗ trên tờ M_R1 lượt đầu
        q = (int(round((cx - x0) * k)), int(round((cy - y0) * k)))
        m = np.zeros((h, w), np.uint8)
        cv2.circle(m, q, 17, 1, -1)
        lo |= m & (lum < 95).astype(np.uint8)
    lo = cv2.dilate(lo, M.el(2))
    bgr = cv2.cvtColor(im[..., :3].copy(), cv2.COLOR_RGB2BGR)
    im[..., :3] = cv2.cvtColor(cv2.inpaint(bgr, lo, 6, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
    Image.fromarray(im, "RGBA").save(p_)
    print(f"nồi: cắt lòng nồi {cat_} px, lấp lỗ sừng {int(lo.sum())} px")


def to_het():
    can()
    M.to_lien()
    prompt_lien()
    prompt_r()
    os.makedirs(M.MANH, exist_ok=True)
    for r in DUNG_LAI:
        shutil.copy(os.path.join(BASE1, "manh", r + ".png"), os.path.join(M.MANH, r + ".png"))
    print("chép", len(DUNG_LAI), "mảnh dùng lại từ dạng 2")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        if chi in ("", "LIEN"):
            M.cat_lien()
        if chi in ("", "R"):
            M.cat_r()
            sua_noi()
    else:
        print(__doc__)
