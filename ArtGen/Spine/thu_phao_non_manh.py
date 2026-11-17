# -*- coding: utf-8 -*-
"""Thú giáp pháo non (dạng 1, thu_phao_non): MẢNH theo concept đã duyệt inbox/thu_phao_non/tai_ve/L1_duyet.png (= L2_1_2: bản A thân giáp bạc
nhẹ, đầu kiểu 1b mũ hiệp sĩ non khép, khe chữ T, mắt vàng xếch, chỏm vàng ngắn, tai giáp nhọn ngắn). Dùng lại hàm của thu_phao_manh.py.

  CHUYỂN DA N (K1 mai, K2 bụng + cổ + sau gáy, K3 chân trước, K4 chân sau): tờ = mảnh DẠNG 2 đã xong đặt đúng ô tờ K của nó; GPT tô lại cho
       dạng non (cùng bạc + vàng, BỎ đinh tán, viền vàng mảnh một nửa), giữ hình bóng; cắt bằng `thu_phao_manh.cat_k` (hình bóng gốc).
  DÙNG LẠI dạng 2: K5 (24 ngón), K6 (vảy đuôi, khối tối, mặt dưới pháo), K7 (pháo khối 3D, lõi), hai cánh vàng (moi.json "he": "lon":
       toạ độ thế giới dạng 2 → rig gắn theo hệ không đổi tỉ lệ, co cùng pháo).
  R (gen đúng chỗ, đúng cỡ trên concept dạng 1): mũ (cả đầu, thay P_tou00 trên bone34), tai gần (P_erduo00 bone36), tai xa (P_erduo01 bone37);
       toạ độ thế giới DẠNG 1 (rig non) qua bố cục → không ghi "he".

    thu_phao_non_manh.py can       căn concept dạng 1 lên khung bố cục → inbox/thu_phao_non/mau/can.json
    thu_phao_non_manh.py chep      chép mảnh dạng 2 dùng lại → inbox/thu_phao_non/manh/ (+ moi.json hai cánh)
    thu_phao_non_manh.py to        tờ chuyển da + prompt → mau/da2_K*.png, gui_gpt/thu_phao_non/luot_2_*.txt
    thu_phao_non_manh.py cat [tờ]  cắt (K1..K4 / R) → inbox/thu_phao_non/manh/
"""
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import thu_phao as G  # noqa: E402
import thu_phao_manh as M  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
NON = os.path.join(HERE, "inbox", "thu_phao_non")
NMAU, NTAI, NMANH = os.path.join(NON, "mau"), os.path.join(NON, "tai_ve"), os.path.join(NON, "manh")
GUI = os.path.join(HERE, "gui_gpt", "thu_phao_non")
CON = os.path.join(NTAI, "L1_duyet.png")
MANH2 = os.path.join(G.BASE, "manh")
CHUYEN = ["K1", "K2", "K3", "K4"]
DUNG_LAI_K = ["K5", "K6", "K7"]
DUNG_LAI_R = ["canh_trai", "canh_phai"]
MUC = M.MUC
MAU = M.MAU


def Wp(p):
    return os.path.normpath(p)


# ================================================================ căn concept dạng 1 ↔ thế giới rig non (qua bố cục)
def can():
    g = M.mat_na(np.asarray(Image.open(os.path.join(NMAU, "bo_cuc_khung.png")).convert("RGB")))
    c = M.mat_na(np.asarray(Image.open(CON).convert("RGB").resize((W, H))))
    import cv2
    k = 4
    gs = cv2.resize(g.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA)
    cs = cv2.resize(c.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA).astype(bool)
    C = np.array([W / 2, H / 2]) / k
    best = (0, 1.0, 0.0, 0.0)

    def thu(a, dx, dy):
        Mx = np.array([[a, 0, C[0] - a * C[0] + dx / k], [0, a, C[1] - a * C[1] + dy / k]], np.float32)
        w = cv2.warpAffine(gs, Mx, (W // k, H // k), flags=cv2.INTER_NEAREST).astype(bool)
        return (w & cs).sum() / max(1, (w | cs).sum())
    for a in np.arange(0.94, 1.081, 0.01):
        for dx in range(-32, 33, 4):
            for dy in range(-32, 33, 4):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    v, a, dx, dy = best
    out = dict(iou=round(float(v), 4), a=float(a), dx=float(dx), dy=float(dy))
    json.dump(out, open(os.path.join(NMAU, "can.json"), "w"), indent=1)
    print("căn:", out)


def phep_can():
    """(T: thế giới rig non → px concept dạng 1, Ti: ngược lại, px / đơn vị)."""
    bc = json.load(open(os.path.join(NMAU, "bo_cuc.json")))
    kh = json.load(open(os.path.join(NMAU, "bo_cuc_khung.json")))
    cj = json.load(open(os.path.join(NMAU, "can.json")))
    x0, y0, x1, y1 = bc["box"]
    sc, k, ox, oy = bc["scale"], kh["k"], kh["ox"], kh["oy"]
    a, dx, dy = cj["a"], cj["dx"], cj["dy"]
    C = np.array([W / 2, H / 2])

    def T(V):
        V = np.asarray(V, float).reshape(-1, 2)
        P = np.stack([(V[:, 0] - x0) * sc * k + ox, (y1 - V[:, 1]) * sc * k + oy], 1)
        return C + a * (P - C) + np.array([dx, dy])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([dx, dy]) - C) / a + C
        return np.stack([(P[:, 0] - ox) / (sc * k) + x0, y1 - (P[:, 1] - oy) / (sc * k)], 1)
    return T, Ti, sc * k * a


# ================================================================ dùng lại mảnh dạng 2
def chep():
    os.makedirs(NMANH, exist_ok=True)
    n = 0
    for ma in DUNG_LAI_K:
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        for r, d in o.items():
            shutil.copy2(os.path.join(MANH2, d["vung"] + ".png"), os.path.join(NMANH, d["vung"] + ".png"))
            n += 1
    m2 = json.load(open(os.path.join(MANH2, "moi.json")))
    pm = os.path.join(NMANH, "moi.json")
    moi = json.load(open(pm)) if os.path.exists(pm) else {}
    for ten in DUNG_LAI_R:
        shutil.copy2(os.path.join(MANH2, ten + ".png"), os.path.join(NMANH, ten + ".png"))
        moi[ten] = dict(m2[ten], he="lon")
        n += 1
    json.dump(moi, open(pm, "w"), indent=1)
    print(f"chép {n} mảnh dạng 2 → {NMANH}")


# ================================================================ chuyển da (tờ = mảnh dạng 2 đặt đúng ô tờ K)
R_CON = ("the APPROVED YOUNG FIRST FORM of our character, 1536x1024, white background: a young armoured cannon beast turned to the right "
         "in LIGHT silver armour with THIN gold trims and NO rivets, a round silver knight helm with a T-shaped visor and two yellow eyes, "
         "short gold crest, short pointed ear guards, a three-quarter box cannon on its back. It gives the colours, the trims and the "
         "hand-drawn look.")


def _mo_ta_non(r):
    t = M._mo_ta(r)
    t = t.replace(", 2 small round gold rivets", "").replace("(about 14 px wide)", "(THIN: about 7 px wide)")
    return t + " YOUNG FORM: no rivets at all, gold trims thin."


def to_n(ma):
    o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for r, d in o.items():
        x, y, cw, ch = d["hop"]
        im = Image.open(os.path.join(MANH2, d["vung"] + ".png")).convert("RGBA")
        im = im.convert("RGBa").resize((cw, ch), Image.LANCZOS).convert("RGBA")
        can_.alpha_composite(im, (x, y))
    os.makedirs(NMAU, exist_ok=True)
    p = os.path.join(NMAU, f"da2_{ma}.png")
    can_.convert("RGB").save(p)
    out = os.path.join(NTAI, f"D_{ma}.png")
    pp = os.path.join(GUI, f"luot_2_da_{ma}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(p)}: the PARTS SHEET, 1536x1024, white background: separate parts of a 2D animation puppet (a four-legged armoured "
         f"beast with a cannon on its back), each drawn alone at the exact size and place to keep: {M.TA_K[ma]}. They are already drawn in "
         "our hand-drawn style for the FINAL form (silver plates, thick gold trims, round rivets).",
         f"image 2 = {Wp(CON)}: {R_CON}",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: RESKIN FOR THE YOUNG FORM. Redraw the SAME sheet with every part repainted as described below, so that the parts can be put "
         "back on the same puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation, its place on "
         "the sheet (if the new picture were laid over image 1, every part must coincide with the old one) and its structural lines (the "
         "edge between a front face and a side face). Keep the same flat colours (silver faces, darker silver side faces, dark steel, dark "
         "gold claws). CHANGE ONLY: REMOVE EVERY RIVET (no round dots on any plate) and make every GOLD TRIM about HALF AS WIDE as in image 1 "
         "(a thin band, about 7 px). Do NOT merge, add or move parts. Pure white (#FFFFFF) between the parts.", "",
         f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 9 px) round every part, thin ink lines for inner "
         "lines, every area ONE flat colour with visible crayon hatching. No shading, no highlights, no gradients, no glow, no shadows.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {_mo_ta_non(r)}")
    t += ["", "Plain pure-white background (#FFFFFF), no labels, no numbers, no frame, nothing added."]
    M.ghi(pp, t)
    print(pp)


# ================================================================ R: mũ + hai tai, đúng chỗ, đúng cỡ trên concept dạng 1
# Tờ R1 (mũ + hai tai) Codex vẽ đúng mũ nhưng hai tai bè ra hai bên hông, thấp: chỉ lấy MŨ từ R1 (tâm tai đặt đúng chỗ tai trên tờ đó để chỏm vàng
# về mũ); hai tai gen riêng tờ R2 (chỉ hai tai, không mũ: khỏi chồng, khỏi gán nhầm)
R = {"R1": [("mu", "P_tou00", "bone34",
             "the HELMET (the whole head): the round silver knight helm with the T-shaped visor slit, the TWO YELLOW EYES with their dark "
             "pupils, white dots and brows, the short gold crest on top and the gold rims; complete it into one closed shape down to its lower "
             "edge; WITHOUT the two pointed ear guards (leave them out, close the helm outline where they rose)"),
            ("tai_gan", "P_erduo00", "bone36", "the NEAR (left) short pointed armour EAR GUARD, complete down to its base"),
            ("tai_xa", "P_erduo01", "bone37", "the FAR (right) short pointed armour EAR GUARD, complete down to its base")],
     "R2": [("tai_gan", "P_erduo00", "bone36",
             "the NEAR (LEFT) pointed armour EAR GUARD: it rises from the UPPER LEFT of the round helm (around x = 820 to 925, y = 525 to 650 "
             "in image 1), pointing UP and slightly back to the upper left, silver with a gold rim on its outer edge; draw it in EXACTLY that "
             "place, size and direction, and CONTINUE its lower end about 50 px further DOWN-RIGHT into where the helm was (that part is "
             "hidden behind the helm in image 1), ending in a plain rounded base"),
            ("tai_xa", "P_erduo01", "bone37",
             "the FAR (RIGHT) pointed armour EAR GUARD: it rises from the UPPER RIGHT of the round helm (around x = 1075 to 1165, y = 510 to "
             "650 in image 1), pointing UP and slightly back, silver with a gold rim on its outer edge; draw it in EXACTLY that place, size "
             "and direction, and CONTINUE its lower end about 50 px further DOWN-LEFT into where the helm was, ending in a plain rounded "
             "base")]}
LAY = {"R1": ("mu",), "R2": ("tai_gan", "tai_xa")}                 # mảnh lấy từ mỗi tờ
TAM_R = {"R1": {"mu": (1030, 730), "tai_gan": (795, 680), "tai_xa": (1165, 650)},
         "R2": {"tai_gan": (868, 590), "tai_xa": (1117, 585)}}


def prompt_r():
    for ma, ds in R.items():
        out = os.path.join(NTAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ma}.txt")
        bo = ("the helmet, the body, the shell, the legs, the tail, the cannon" if ma == "R2" else
              "the body, the shell, the legs, the tail, the cannon")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CON)}: {R_CON}",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} pieces listed below, each in the SAME POSITION and at the SAME SIZE as in image 1 "
             f"(if your picture were laid over image 1, every piece must sit exactly on its old place). REMOVE everything else ({bo}) and "
             "leave pure white there. COMPLETE every piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece "
             "that were hidden behind other things in image 1 are drawn too, continuing its shape naturally. The pieces must not touch each "
             "other.", "", "THE PIECES:"]
        t += [f"{i}. {mt}." for i, (_, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, no "
              "gradients, no glow, no shadows.", "", "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no "
              "labels, no frame."]
        M.ghi(p, t)
        print(p)


def cat_r(chi=""):
    import cv2
    T, Ti, spx = phep_can()
    pm = os.path.join(NMANH, "moi.json")
    moi = json.load(open(pm)) if os.path.exists(pm) else {}
    for ma, ds in R.items():
        if chi not in ("", "R", ma):
            continue
        path = anh.to_moi_nhat(NTAI, f"M_{ma}")
        if not path:
            print(f"{ma}: chưa gen")
            continue
        print(f"{ma}:", os.path.basename(path))
        rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
        ms = M.tach_manh(rgb, TAM_R[ma])
        for ten, sl, bn, _ in ds:
            if ten not in LAY[ma]:
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
            mm &= ~M._nen_trong(sub, mm)
            al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
            rgba = np.dstack([sub, (al * 255).astype(np.uint8)])
            k = 1.0 / spx * (M.RES * 0.5)
            out = Image.fromarray(rgba, "RGBA").convert("RGBa")
            out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
            out.save(os.path.join(NMANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
            moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=Ti(hop).tolist(), to=ma)
            print(f"  {ten:8s} hộp {x0},{y0}–{x1},{y1} → {ten}.png {out.size} (thay {sl}, xương {bn})")
    json.dump(moi, open(pm, "w"), indent=1)


def cat_n(ma):
    """cắt tờ chuyển da bằng thu_phao_manh.cat_k: đọc tai_ve dạng 1, ghi manh dạng 1 (hình bóng = mảnh gốc của họ)."""
    M.MANH = NMANH
    tai_cu = G.TAI
    G.TAI = NTAI
    try:
        M.cat_k(ma)
    finally:
        G.TAI = tai_cu


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "chep":
        chep()
    elif cmd == "to":
        for ma in CHUYEN:
            to_n(ma)
        prompt_r()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ma in CHUYEN:
            if chi in ("", ma):
                cat_n(ma)
        if chi in ("", "R", "R1", "R2"):
            cat_r(chi)
    else:
        print(__doc__)
