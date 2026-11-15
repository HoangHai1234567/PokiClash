# -*- coding: utf-8 -*-
"""Hỏa Quy DẠNG 1 VẼ RIÊNG (rùa non chibi; hướng `ve` của rua_lua_non, suất nguu_quyen đảo Hỏa).

Người dùng 2026-11-13: "E cũng được nhưng sẽ phải gen lại bằng gpt cho chi bi hơn"; 2026-11-14 xem hai concept, bảo "làm đi" (theo đề
xuất B của Claude) → inbox/rua_lua_non/tai_ve/L1_tron_hon.png = L1_duyet.png. Cùng xương, cùng clip với dạng 2 (rua_lua_rig.py,
RL_NON=ve); mảnh gen "đúng chỗ, đúng cỡ" từ concept non như dạng 2 (rua_lua_manh.py), khung concept ↔ rig khớp bằng mốc tay (KHOP_VE).

    rua_lua_non_ve.py luoi            concept + lưới toạ độ → inbox/rua_lua_non/mau/_luoi_duyet.png (đọc mốc)
    rua_lua_non_ve.py chong           viền part của rig gốc chồng lên concept theo KHOP_VE → mau/_rig_tren_concept.png
    rua_lua_non_ve.py build           → gui_gpt/rua_lua_non/luot_2_manh_<A..D>.txt (+ HUONG_DAN.md mục lượt 2)
    rua_lua_non_ve.py lam             cắt tờ M_<A..D>.png → inbox/rua_lua_non/manh_ve/ (ảnh mảnh + dat.json + _so_ghep.png + _to.png)
    rua_lua_non_ve.py tho             viền thô từng mảnh đã cắt chồng lên concept → mau/_tho_tren_concept.png (chỉnh CHINH)
Rig: RL_NON=ve py -3 -I rua_lua_rig.py → inbox/rua_lua_non/rig_ve/; tiến hóa: RL_NON=ve RL_CO=<cỡ> py -3 -I rua_lua_non_th.py
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.join(HERE, "inbox", "rua_lua_non")
TAI = os.path.join(BASE, "tai_ve")
MAU = os.path.join(BASE, "mau")
MANH = os.path.join(BASE, "manh_ve")
DUYET = os.path.join(TAI, "L1_duyet.png")
PK = os.path.join(HERE, "gui_gpt", "rua_lua_non")
MANH2 = os.path.join(HERE, "inbox", "rua_lua_1", "manh")

# khung concept non (px, y xuống) ↔ thế giới con gốc dáng idle giây 0: px = ox + s·X, py = oy − s·Y. Mốc tay: mép ngoài + đáy bốn chân,
# mũi đuôi, đỉnh và mép trái mai. Thân con non gần đúng tỉ lệ rig (bằng 0,94 khung dạng 2), chỉ đầu to hẳn (mảnh cứng trên xương đầu).
KHOP_VE = (1.075, 722.0, 903.0)
MIENG_VE = (1165, 805)        # trước mõm trên concept non (chỗ tụ cầu lửa của chiêu mana)

# mảnh: (tờ, tâm ước chừng trên tờ để cắt, slot gốc, kiểu đặt, mô tả) như rua_lua_manh.P. Ba đùi khuất + đùi trước gần lấy lại mảnh dạng 2
# (kiểu "r": rig đặt theo khung part gốc, không phụ thuộc concept).
P = {
    # ---- tờ A
    "mai": ("A", (690, 550), "p_ke", "c",
            "THE SHELL: the big domed slate blue-grey stone shell with its seam lines (in image 1 its visible part is about x = 388 to "
            "x = 1000, y = 345 to y = 748). Draw the WHOLE shell as ONE closed, SOLID dome-shaped piece, like half of a big round "
            "pebble, with NOTHING missing. TOP EDGE: one smooth dome line that continues under the flame and under the stone columns "
            "(highest point about y = 345 near x = 700). RIGHT END: hidden behind the horn and the big face mask; continue it as a "
            "rounded end reaching about x = 1010 between y = 520 and y = 700. LEFT END: a simple rounded end at about x = 388, "
            "y = 640 (no hook, no curl, no lip). LOWER EDGE (very important): ONE continuous line that bulges gently DOWNWARD all "
            "the way, from the left end at about (392, 650) through about (480, 705), (600, 740) and (760, 748) to about (900, 740), "
            "then up to the right end. In image 1 the legs and the head stand IN FRONT of the shell and cover part of this lower "
            "edge: the shell continues BEHIND them. Do NOT cut an arch, a notch, a bite or any opening out of the shell; there is "
            "no concave part anywhere on its outline. Keep the same few seam lines as in image 1 and continue them over the newly "
            "drawn parts. Remove the columns, the flame, both horns, the head, every leg, the tail and the belly plate."),
    "ong_truoc_xa": ("A", (1100, 850), "p_xiaotui02", "c",
                     "THE FAR FRONT LEG BLOCK: the short pillar leg at the far right with its small orange crystal on its upper right "
                     "(visible about x = 1050 to x = 1237, y = 770 to y = 937, plus a low strip under the jaw from x = 945). Its left "
                     "side is hidden behind the jaw and the face mask: complete it as ONE short rounded pillar block like the other "
                     "legs, about x = 945 to x = 1237, with a rounded top at about y = 755, flat bottom at about y = 935. Keep the "
                     "crystal. Only this leg block."),
    "hong": ("A", (170, 880), None, "r",
             "THE INSIDE OF THE MOUTH (not visible in image 1; it is seen when the jaw opens; draw it in the empty BOTTOM-LEFT corner, "
             "centred at about x = 170, y = 880): ONE rounded bean-shaped cavity about 170 px wide and 130 px tall, a flat orange "
             "(#F7902A) area with a yellow (#FFD45A) centre and a red-orange (#E0441F) rim, dark-brown ink outline, same crayon "
             "hatching; no teeth, no tongue."),
    # ---- tờ B
    "bung": ("B", (690, 770), "p_xiongqiang", "k",
             "THE BELLY PLATE: the lighter blue-grey plate under the shell (visible between the legs and under the shell rim, about "
             "x = 400 to x = 900, y = 690 to y = 835). Complete it as ONE long flat stone plate from about x = 385 to x = 1000: its "
             "bottom edge as in image 1 (about y = 832), its two ends rounded, its top edge (hidden under the shell) rounded, at "
             "about y = 672."),
    "cot_gan": ("B", (568, 500), "p_kuangshi01", "c",
                "THE COLUMN CLUSTER: the group of three short dark navy-charcoal hexagonal stone columns standing on the shell (about "
                "x = 470 to x = 667, y = 400 to y = 600), drawn as ONE piece (keep the ink lines between the columns). They are fully "
                "visible in image 1; close the bottom of the cluster with the ink outline where the columns stand on the shell."),
    "lua_cao": ("B", (765, 285), None, "k",
                "THE FLAME: the single flame on top of the shell (about x = 663 to x = 868, y = 123 to y = 438), with its three nested "
                "colour zones. It is fully visible in image 1: one complete piece, its rounded base closed with the ink outline. Do "
                "NOT draw any small separate floating flame bits next to it."),
    "sung_gan": ("B", (935, 500), "p_jiao01", "c",
                 "THE NEAR HORN BUD: the thick short ivory horn on the side of the head (about x = 843 to x = 1032, y = 378 to "
                 "y = 613): its broad lobed base and the short curve up to the tip. It is fully visible in image 1 (it lies in front "
                 "of the face mask and the shell): one complete piece with its outline all the way around."),
    "sung_xa": ("B", (1165, 540), "p_jiao01_2", "k",
                "THE FAR HORN BUD: the tiny ivory horn nub at the top right, behind the face mask (visible about x = 1148 to x = 1192, "
                "y = 485 to y = 560), whole and pointed. Complete its BASE, hidden behind the mask: a thick rounded base that "
                "continues down-left to about x = 1118, y = 612."),
    # ---- tờ C
    "mat_so": ("C", (1010, 680), "p_lian", "c",
               "THE FACE MASK: the big ivory skull-like stone mask (visible about x = 790 to x = 1227, y = 485 to y = 862) with its "
               "crack seam, its dark angular eye socket with the yellow eye and dark pupil, and its zigzag lower edge. Its upper-left "
               "part is hidden under the base of the horn bud: complete it there as a smooth rounded forehead / cheek (the outline "
               "runs from about (850, 600) up to about (1000, 500)). Remove both horns and the jaw."),
    "ong_truoc_gan": ("C", (598, 830), "p_xiaotui01", "c",
                      "THE NEAR FRONT LEG BLOCK: the short pillar leg in the foreground (about x = 495 to x = 702, y = 722 to y = 937) "
                      "with its seam lines and its two small orange crystals (a bigger one at its top left, a smaller one beside it). "
                      "It is fully visible in image 1: one complete piece, crystals included."),
    "duoi": ("C", (350, 710), "p_weiba", "c",
             "THE TAIL: the short stone tail at the far left with its two small curved ivory spikes on its upper edge (visible about "
             "x = 298 to x = 400, y = 630 to y = 790). Most of it is hidden behind the near hind leg and under the shell: complete it "
             "as ONE thick short tapering stone tail, its tip at the left exactly as in image 1, its thick rounded root continuing "
             "to the right to about x = 455 (between about y = 680 and y = 800). Keep the two spikes."),
    # ---- tờ D
    "ham": ("D", (1010, 815), "p_xiaba", "c",
            "THE LOWER JAW: the ivory jaw block under the face mask (visible about x = 880 to x = 1140, y = 765 to y = 897). Its top "
            "is hidden behind the zigzag lower edge of the mask: complete it upward as one block with a flat top at about y = 728 "
            "and rounded corners, from about x = 885 to x = 1135. Only the jaw: not the mask, not the leg next to it."),
    "ong_sau_gan": ("D", (425, 820), "p_xiaotui04", "c",
                    "THE NEAR HIND LEG BLOCK: the short pillar leg at the left (about x = 350 to x = 503, y = 728 to y = 913) with its "
                    "seam lines. Its right edge is slightly hidden behind the next leg: complete it as one rounded pillar block, "
                    "right edge at about x = 508."),
    "ong_sau_xa": ("D", (775, 840), "p_xiaotui03", "c",
                   "THE FAR HIND LEG BLOCK: the short pillar leg seen under the belly between the near front leg and the head "
                   "(visible about x = 700 to x = 852, y = 835 to y = 913). Complete it as a rounded pillar block like the other "
                   "legs, about x = 695 to x = 852, with a rounded top at about y = 762 (hidden behind the belly)."),
}
TO = sorted({v[0] for v in P.values()})
MO_TA_EN = ("the BABY form of a fire tortoise golem, chibi, facing right: a round domed slate blue-grey stone shell with a cluster of "
            "three short dark stone columns and ONE flame on top, a lighter belly plate, four short pillar legs (small orange crystals "
            "on the two front ones), a short tail with two ivory spikes at the left, and at the front right a very big ivory "
            "skull-like face mask with one yellow eye, a jaw block under it, a thick short horn bud on the near side and a tiny horn "
            "nub behind the mask.")
MO_TA_VI = ("rùa golem lửa NON chibi (concept dạng 1 đã chốt): mai vòm tròn xám lam có cụm ba cột đá lùn và MỘT ngọn lửa, bụng xám nhạt, bốn "
            "chân trụ lùn (pha lê cam ở hai chân trước), đuôi ngắn hai gai ngà, mặt sọ ngà rất to một mắt vàng, hàm, sừng mầm gần mập, "
            "mầm sừng xa tí hon sau mặt")
# thứ tự vẽ sau → trước (như rua_lua_manh.THU_TU, một ngọn lửa, không cột đá xa)
THU_TU = ["dui_sau_xa", "ong_sau_xa", "duoi", "dui_truoc_xa", "ong_truoc_xa", "bung", "dui_sau_gan", "ong_sau_gan", "dui_truoc_gan",
          "mai", "sung_xa", "lua_cao", "cot_gan", "hong", "ham", "mat_so", "mat_tat", "sung_gan", "ong_truoc_gan"]
DUI = ["dui_sau_xa", "dui_truoc_xa", "dui_sau_gan", "dui_truoc_gan"]
# chỉnh tay (dời x, dời y, tỉ lệ [, tỉ lệ dọc]) cho mảnh Codex vẽ lệch concept (đọc trên mau/_tho_tren_concept.png)
# bung: Codex vẽ tấm bụng rộng hơn mai (x 370–1035) và thấp hơn concept ~18 px: lúc appear chỉ còn mai + bụng thì bụng thò ra hai bên như
# cái đĩa → co ngang 0,86, co dọc 0,90, dời lên 12 px (nấp gọn dưới vành mai, đáy ngang đáy chân lúc mai nằm sát đất)
CHINH = {"bung": (0, -12, 0.86, 0.90)}
# rua_lua_rig.giam_dau: đầu rất to nên bớt độ xoay thực của đầu ở các clip quật đầu (hit, die, húc); riêng dáng chĩa sừng của chiêu cuối
# (skill_02) giữ 0,8 để cú HẤT SỪNG phóng cầu còn rõ
DAU_GIAM = {"*": 0.45, "skill_02": 0.8}
LICH = {"chan_truoc_xa": 1.06}  # appear: mai con non ngắn, chân trước xa mọc ra ngoài mép mai → cho mọc sát lúc đầu thò ra (đầu che)


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luoi():
    im = Image.open(DUYET).convert("RGB")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for x in range(0, im.width, 50):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if x % 100 == 0 else (255, 170, 170), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=f)
    for y in range(0, im.height, 50):
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255) if y % 100 == 0 else (170, 170, 255), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(0, 0, 200), font=f)
    os.makedirs(MAU, exist_ok=True)
    p = os.path.join(MAU, "_luoi_duyet.png")
    im.save(p)
    print(p)


def chong(ten="_rig_tren_concept.png"):
    """khung bao từng part của rig gốc (dáng idle giây 0) chồng lên concept non mờ theo KHOP_VE."""
    os.environ.setdefault("SXS", "D:/RefAnimation/SwordxStaff")
    import rua_lua as G
    A0 = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    s, ox, oy = KHOP_VE
    C = Image.open(DUYET).convert("RGB")
    im = Image.blend(C, Image.new("RGB", C.size, (255, 255, 255)), 0.45)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    mau = [(220, 0, 0), (0, 120, 220), (0, 150, 0), (200, 0, 200), (220, 120, 0), (0, 160, 160)]
    for i, a in enumerate(x for x in A0["atts"] if x["cur"]):
        Pt = np.array(a["xy"], float).reshape(-1, 2)
        px = np.c_[ox + s * Pt[:, 0], oy - s * Pt[:, 1]]
        hull = a.get("hull") or len(px)
        pts = [tuple(q) for q in px[:hull]]
        c = mau[i % len(mau)]
        d.line(pts + [pts[0]], fill=c, width=2)
        d.text((px[:, 0].mean() - 20, px[:, 1].mean() - 6), a["slot"].replace("p_", ""), fill=c, font=f)
    d.line([(0, oy), (C.width, oy)], fill=(120, 120, 120), width=1)
    p = os.path.join(MAU, ten)
    im.save(p)
    print(p)


def _M():
    """rua_lua_manh với bảng mảnh, thư mục, concept của dạng non (dùng lại cat_to, lam)."""
    os.environ.setdefault("SXS", "D:/RefAnimation/SwordxStaff")
    import rua_lua_manh as M
    M.P, M.TO, M.MANH, M.DUYET, M.CHINH, M.THU_TU, M.DOI, M.MAI_CAT, M.MAI_O = P, TO, MANH, DUYET, CHINH, THU_TU, {}, None, None

    def moi_nhat(ma):
        c = [f for f in os.listdir(TAI) if f == f"M_{ma}.png" or (f.startswith(f"M_{ma}_") and f.endswith(".png"))]
        if not c:
            return None
        c.sort(key=lambda f: (0 if f == f"M_{ma}.png" else int(f[len(f"M_{ma}_"):-4])))
        return os.path.join(TAI, c[-1])
    M.moi_nhat = moi_nhat
    return M


def build():
    os.environ.setdefault("SXS", "D:/RefAnimation/SwordxStaff")
    import rua_lua_manh as M
    if not os.path.exists(DUYET):
        raise SystemExit("chưa có concept duyệt " + DUYET)
    os.makedirs(PK, exist_ok=True)
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-14, concept chốt `L1_tron_hon.png` → `L1_duyet.png`)", "",
          "Mỗi file vẽ lại concept non đã chốt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất, bỏ hết thứ khác (nền trắng). "
          "Lòng miệng vẽ ở góc trống. Ảnh mẫu duy nhất của mọi file:", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{os.path.normpath(DUYET)}` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): {MO_TA_VI} |", ""]
    for ma in TO:
        ten = [k for k, v in P.items() if v[0] == ma]
        out = os.path.join(TAI, f"M_{ma}.png")
        p = os.path.join(PK, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {os.path.normpath(DUYET)}: the APPROVED picture of the creature, 1536x1024, white background: " + MO_TA_EN,
             "", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "", M.MANH_CHUNG, "", "KEEP:"]
        t += [f"{i}. {P[k][4]}" for i, k in enumerate(ten, 1)]
        t += ["", f"Exactly {len(ten)} separate parts on the canvas, nothing else.", "", M.FLAT, M.BG]
        ghi(p, t)
        print(p)
        gd += [f"- **`{ma}`** ({', '.join(ten)}): chỉ gửi GPT `{os.path.normpath(p)}`; ảnh lưu vào `{os.path.normpath(out)}`."]
    gd += ["", "Kiểm từng ảnh: đúng các mảnh đã kê, trùng chỗ concept, viền mực kín, không chạm nhau, phần khuất vẽ đủ, nền trắng, "
           "không bóng. Claude cắt bằng `rua_lua_non_ve.py lam`."]
    hd = os.path.join(PK, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    ghi(hd, [cu] + gd)


def lam():
    """cắt các tờ đã gen (rua_lua_manh.lam với bảng của dạng non), thêm bốn đùi khuất của dạng 2, ghi mốc khung, mõm, mũi sừng."""
    import shutil
    M = _M()
    M.lam()
    pd = os.path.join(MANH, "dat.json")
    D = json.load(open(pd, encoding="utf-8"))
    D2 = json.load(open(os.path.join(MANH2, "dat.json"), encoding="utf-8"))
    for t in DUI:                                  # mảnh kiểu "r": rig đặt theo khung part gốc, toạ độ `goc` không dùng
        shutil.copyfile(os.path.join(MANH2, t + ".png"), os.path.join(MANH, t + ".png"))
        D[t] = dict(D2[t])
    co = set(D) - {"_thu_tu"}
    tt = []
    for t in THU_TU:
        if t in co:
            tt.append(t)
            if t + "_nguoi" in co:
                tt.append(t + "_nguoi")
    D["_thu_tu"] = tt
    D["_khop"] = list(KHOP_VE)
    D["_mieng"] = list(MIENG_VE)
    D["_dau_giam"] = DAU_GIAM
    if "duoi" in D:                                # đuôi lùn của con non bám lưới 3 xương của đuôi gốc thì gập mép giữa hai gai lúc quẫy
        D["duoi"]["deu"] = {"bone24": 0.5, "bone25": 0.5}
    D["_lich"] = LICH
    if "sung_gan" in D:                            # mũi sừng mầm: điểm cao nhất của mảnh sừng gần, lùi vào 6 px
        a = np.asarray(Image.open(os.path.join(MANH, "sung_gan.png")))[..., 3] > 128
        ys, xs = np.nonzero(a)
        k = int(np.argmin(ys))
        g = D["sung_gan"]["goc"]
        D["_sung_mui"] = [int(g[0] + xs[ys == ys[k]].mean()), int(g[1] + ys[k] + 6)]
    json.dump(D, open(pd, "w", encoding="utf-8"), indent=1)
    print("thứ tự:", tt)
    print("mũi sừng", D.get("_sung_mui"), "mõm", D["_mieng"], "khớp", D["_khop"])


def tho():
    """viền thô từng mảnh đã cắt (đúng chỗ dat.json) chồng lên concept mờ: xem mảnh nào Codex vẽ lệch."""
    import cv2
    D = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    C = Image.open(DUYET).convert("RGB")
    im = np.asarray(Image.blend(C, Image.new("RGB", C.size, (255, 255, 255)), 0.5)).copy()
    mau = [(220, 0, 0), (0, 120, 220), (0, 150, 0), (200, 0, 200), (220, 120, 0), (0, 160, 160)]
    for i, t in enumerate(D["_thu_tu"]):
        d = D[t]
        if d.get("kieu") == "r" or t.endswith("_nguoi") or t == "mat_tat":
            continue
        a = (np.asarray(Image.open(os.path.join(MANH, t + ".png")))[..., 3] > 128).astype(np.uint8)
        cs, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        gx, gy = d["goc"]
        for c in cs:
            cv2.polylines(im, [c + np.array([[gx, gy]])], True, mau[i % len(mau)], 2)
        cv2.putText(im, t, (gx + 4, gy + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, mau[i % len(mau)], 1, cv2.LINE_AA)
    p = os.path.join(MAU, "_tho_tren_concept.png")
    Image.fromarray(im).save(p)
    print(p)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd in ("luoi", "chong", "build", "lam", "tho"):
        globals()[cmd]()
    else:
        print(__doc__)
