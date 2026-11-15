# -*- coding: utf-8 -*-
"""Viêm Sư DẠNG 1 (pháp sư lửa con chibi "Viêm Đồng", mã làm việc phap_lua_non; suất hong_lien = tướng thứ 6 đảo Hỏa).

Người dùng 2026-11-14: "suất 6 cho vào game rồi làm thêm dạng 1". Concept (phiên chính chọn hướng A): inbox/phap_lua_non/tai_ve/L1_duyet.png.
Rig = phap_lua_rig.py với PL_NON=1: CÙNG xương, CÙNG 9 clip, cùng sự kiện với dạng 2; khác ở mảnh và dáng gốc vài xương:
- khung concept → thế giới rig: X = (x − CX) · TI + XR, Y = (CY − y) · TI + YR (mốc: cổ = gốc xương đầu bone6). Cả thân hạ xuống DY_THAN
  (dáng gốc của bone2 và của xương trượng thả rời bone102) cho váy lửa sát đất: con non thấp hơn dạng 2 nhiều.
- mũ trùm (`dau`, ảnh cứng trên bone6), váy lửa (`lua_ao`) và thân (`ao`: cổ áo choàng + áo đỏ + dây vàng, một mảnh; trọng số theo các đốt
  xương đuôi áo của họ), đuôi áo choàng (`vai_duoi`, bám lưới pifeng_02 của họ), hai búi tóc (`toc_tren`, `toc_phai`: mảnh cứng trên hai
  xương mới là con của xương đầu, đung đưa trong aura), trượng ngắn (`truong`, ảnh cứng trên bone56 / bone102): gen "đúng chỗ, đúng cỡ" từ
  concept non (4 tờ), cắt theo cụm liền.
- hai bàn tay (cổ tay khói + đốt ngón / vuốt), bàn tay thứ hai trên `far`, cầu lửa + tim + lưỡi lửa + khói: dùng lại mảnh dạng 2 (tay giữ
  cỡ, dời gốc tay cho khớp concept; cầu lửa co theo bán kính cầu mới).
- dây bện, hai gai sao của dạng 2 (`shenti`, `zhuangshi_*`) bỏ: dây vàng vẽ liền vào thân.

    py -3 -I ArtGen/Spine/phap_lua_non.py prompt          4 file prompt gui_gpt/phap_lua_non/luot_2_manh_<tờ>.txt (+ HUONG_DAN.md)
    py -3 -I ArtGen/Spine/phap_lua_non.py cat             cắt tai_ve/M_<tờ>.png → inbox/phap_lua_non/manh/ + dat_moi.json (chép cả mảnh dùng lại của dạng 2)
    PL_NON=1 py -3 -I ArtGen/Spine/phap_lua_rig.py        dựng → inbox/phap_lua_non/rig_d1/
    py -3 -I ArtGen/Spine/phap_lua_non.py so              khung 0 idle cạnh concept → rig_d1/so_concept.png + IoU
    py -3 -I ArtGen/Spine/phap_lua_non.py th              gộp clip evolve (dạng 2 bản nhẹ) → inbox/phap_lua_non/rig/phap_lua_non.atomik + chan_dung.png
                                                          (cần SXS như bước rig: chân dung dựng lại từ rig)
    py -3 -I ArtGen/Spine/phap_lua_non.py do              số đo cho HatPhap.cs (đầu trượng ở cast, tâm + cỡ cầu ở skill)
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo (monster_3481): dùng nội bộ, không đăng công khai. Hình là của mình.
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
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
BASE = os.path.join(HERE, "inbox", "phap_lua_non")
TAI = os.path.join(BASE, "tai_ve")
MANH = os.path.join(BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "phap_lua_non")
MANH2 = os.path.join(HERE, "inbox", "phap_lua_1", "manh")
CONCEPT = os.path.join(TAI, "L1_duyet.png")
W, H = 1536, 1024

# ---- khung concept ↔ rig (mốc tay): cổ (chỗ cằm mũ trùm gặp cổ áo) ↔ gốc xương đầu bone6 đã hạ DY_THAN
TI = 0.80                       # đơn vị rig cho mỗi px concept (gần tỉ lệ concept dạng 2: 0,81)
CX, CY = 812.0, 640.0           # cổ trên concept (px)
XR, YR0 = 51.0, 436.0           # gốc bone6 ở dáng gốc dạng 2
DY_THAN = -170.0                # hạ cả thân: váy lửa của con non chạm sát đất
YR = YR0 + DY_THAN

# dáng gốc các xương (cha trước con; dời theo THẾ GIỚI). Tay: mảnh dạng 2 to lên TAY lần (con chibi tay to; nét mực cũng khớp concept)
TAY_TR, TAY_V = 1.0, 1.0        # cỡ bàn tay trượng / bàn tay vuốt so với dạng 2 (đo trên concept: nắm tay ~100 px, vuốt ~190 px)
XUONG = {
    "bone2": {"dy": DY_THAN},
    "bone42": {"dx": -29.0, "dy": 114.0},           # gốc tay trượng: đưa nắm tay tới chỗ nắm tay trên concept
    "bone45": {"s": TAY_TR},                        # bàn tay trượng (cổ tay khói + bốn ngón)
    "bone7": {"dx": 16.0, "dy": -20.0},             # gốc tay vuốt
    "bone10": {"s": TAY_V},                         # bàn tay vuốt (cổ tay khói + mười đốt vuốt)
    # xương trượng thả rời: cùng tỉ lệ thế giới với xương trượng trong tay (con của bone45) và cùng độ dời với bàn tay trượng (hạ thân +
    # dời tay), để lúc buông / chụp trượng (đổi từ bone56 sang bone102) trượng không nhảy chỗ
    "bone102": {"dx": -29.0, "dy": DY_THAN + 114.0, "s": TAY_TR},
    "bone103": {"s": TAY_V},                        # bàn tay thứ hai (trên far, hiện ra chỗ đối thủ)
}
AN = ["shenti", "zhuangshi_01", "zhuangshi_02", "pifeng_02", "pifeng_01", "pifeng_03", "maofa_01"]
LOP = {"pifeng_03": ["lua_ao", "vai_duoi", "ao"], "maofa_01": ["toc_tren", "toc_phai"]}
CAU = dict(tam=(440.0, 466.0), r=76.0)       # tâm, bán kính quả cầu lửa trong móc trượng trên concept (px)
DUNG_LAI = (["cau", "tim"] + [f"lua_{k}" for k in range(4)] + [f"khoi_{k}" for k in range(3)] + ["shouzhangL_01", "shouzhangR_01"] +
            [f"shouzhiL_{k:02d}" for k in range(1, 11)] + [f"shouzhiR_{k:02d}" for k in range(1, 5)])


def Wp(p):
    return os.path.normpath(p)


def tg(x, y):
    """px concept → thế giới rig."""
    return (x - CX) * TI + XR, (CY - y) * TI + YR


def px(X, Y):
    return (X - XR) / TI + CX, CY - (Y - YR) / TI


# ---------------------------------------------------------------- prompt 4 tờ mảnh
TO = {
    "dau_lua": dict(
        vi="chỉ còn mũ trùm (trên) và váy lửa (dưới), mỗi thứ vẽ đủ phần khuất",
        en=("KEEP ONLY TWO THINGS, each redrawn COMPLETE:\n"
            "(1) THE HOOD: the big charcoal hood with its short pointed tip at the upper left, its broad gold hem around the dark "
            "face opening, the flat darkness inside with the two burning eyes, the yellow diamond gem on the brow, and the two "
            "lappets hanging down at the sides of the opening. Complete it into ONE closed shape with an ink outline all the way "
            "round: where the staff head, the fireball or its flames covered the left edge of the hood, finish that edge as the "
            "simple rounded hood; the two lappets end in soft rounded points at about y = 650; between the lappets the dark face "
            "opening closes in a rounded chin at about y = 630.\n"
            "(2) THE SKIRT OF FLAMES under the robe: all the little flame tongues below the red robe. Complete it into ONE closed "
            "flame shape with an ink outline all the way round: the tongues join in one body of fire that continues UPWARD behind "
            "where the robe was, up to about y = 730, with a simple rounded top (red-orange outside, orange, yellow inside: the "
            "same three flat colours); where the staff shaft crossed the flames, fill in the flames.\n"
            "The two things do not touch each other. Do NOT draw the cream hair tufts, the cape, the robe, the cord, the staff or "
            "the hands.")),
    "than": dict(
        vi="chỉ còn thân: cổ áo choàng than viền vàng + áo đỏ + dây vàng, một mảnh liền, vẽ đủ phần bị mũ, tay, trượng che",
        en=("KEEP ONLY THE LITTLE BODY, redrawn COMPLETE as ONE closed shape with an ink outline all the way round: the small "
            "charcoal collar-cape with its pale gold hem lying over the shoulders, the short crimson robe under it with its wavy "
            "lower edge, and the pale gold braided cord running down the middle of the collar and the robe. WITHOUT the long "
            "pointed tail of the cape (cut the cape off in a simple rounded left end at about x = 650, y = 710: the tail is drawn "
            "separately). At the top the collar closes in a simple rounded neck at about y = 615, between about x = 740 and x = 880 "
            "(it was hidden under the chin and the lappets of the hood): fill in plain flat charcoal there. Everywhere the hood, "
            "the staff, the staff hand or the wrist puff covered the body, fill in the plain flat colour of that part (charcoal "
            "#3C353B for the collar, crimson #A32E22 for the robe) and continue the gold hem line smoothly. Keep the wavy lower "
            "edge of the robe exactly where it is. Do NOT draw the flames under the robe, the hood, the hair, the staff or the "
            "hands.")),
    "toc_duoi": dict(
        vi="chỉ còn hai búi tóc khói ngà (trên đỉnh mũ, bên phải mũ) và cái đuôi áo choàng nhọn bên trái, mỗi thứ vẽ đủ phần khuất",
        en=("KEEP ONLY THREE SMALL THINGS, each redrawn COMPLETE as its own closed shape with an ink outline all the way round:\n"
            "(1) THE TOP HAIR TUFT: the pale ash-cream crescent tuft that peeks out above the hood at the upper left. Continue it "
            "DOWNWARD behind where the hood was, as one soft rounded lobe reaching down to about y = 300 (that part will be hidden "
            "behind the hood).\n"
            "(2) THE RIGHT HAIR TUFT: the pale ash-cream tuft peeking out at the right side of the hood. Continue it to the LEFT "
            "behind where the hood was, as one soft rounded lobe reaching to about x = 960 (hidden behind the hood).\n"
            "(3) THE TAIL OF THE CAPE: the narrow charcoal pointed tail with its gold hem that sweeps out to the lower left. "
            "Continue it to the RIGHT and UP behind where the collar and the staff hand were, as one simple tapering band reaching "
            "to about x = 740, y = 680 (hidden behind the collar); keep the gold hem line along its lower edge.\n"
            "The three things do not touch each other. Do NOT draw the hood, the collar, the robe, the staff or the hands.")),
    "truong": dict(
        vi="chỉ còn cây trượng (khung trượng than đen), KHÔNG có cầu lửa, không lửa, không bàn tay; vẽ đủ phần bị tay và cầu lửa che",
        en=("KEEP ONLY THE STAFF, redrawn COMPLETE as ONE closed shape with an ink outline all the way round: the charcoal-black "
            "staff with its open claw-shaped crook at the top, its straight shaft and its zigzag lower end. REMOVE the ball of fire "
            "and its flames: the inside of the crook is EMPTY (pure white shows through the crook where the ball was), and finish "
            "the inner edges of the crook prongs cleanly. REMOVE the hand: where the fist and the wrist puff covered the shaft, "
            "draw the plain straight shaft through. Flat charcoal black (#2F2A30) with at most one thin slightly lighter inner "
            "line along the shaft. Do NOT draw the fireball, any flame, the hand, the hood or anything else.")),
}
STYLE = ("STYLE: exactly as image 1: the same colours, the same wobbly dark-brown ink outline (#2B2118, about 6 px on this canvas), flat "
         "colours with visible crayon hatching; NO shading, NO shadows, NO highlights, NO glow, NO gradients. Do not add anything that is "
         "not listed (no sparks, no smoke).")
BG = "Plain pure-white background (#FFFFFF), no paper grain outside the pieces, no labels, no numbers, no frame, nothing added."


def prompt():
    os.makedirs(GUI, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    gd = ["", "## Lượt 2: mảnh, gen đúng chỗ đúng cỡ từ concept dạng 1 (2026-11-14)", "",
          f"Concept chốt: `{Wp(CONCEPT)}` (hướng A, phiên chính chọn). Mỗi tờ vẽ lại concept, chỉ giữ một vài mảnh ĐÚNG CHỖ, ĐÚNG CỠ và vẽ đủ "
          "phần khuất. Cắt: `py -3 -I ArtGen/Spine/phap_lua_non.py cat`. Tay, cầu lửa, lưỡi lửa, khói dùng lại mảnh dạng 2.", ""]
    for ten, d in TO.items():
        out = os.path.join(TAI, f"M_{ten}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ten}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: the approved picture of OUR character, 1536x1024, white background: a small chibi fire-mage "
             "spirit: a very big charcoal hood with a gold hem, a dark face opening with two burning eyes and a yellow gem on the "
             "brow; two small pale cream hair tufts behind the hood (one above it at the upper left, one at its right side); a small "
             "charcoal collar-cape with a gold hem and a pointed tail sweeping to the lower left; a short crimson robe with a gold "
             "braided cord; a skirt of small flames under the robe instead of legs; at the left a short black staff with a "
             "claw-shaped crook holding a ball of fire, gripped by a small black fist with a pale cream wrist puff; at the right a "
             "floating black clawed hand with a pale cream wrist puff.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ten}_2.png, M_{ten}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 on the same 1536x1024 pure-white canvas, keeping ONLY the piece(s) named below, in EXACTLY THE SAME "
             "POSITION and at EXACTLY THE SAME SIZE as in image 1 (if the new picture were laid over image 1, the visible parts of the "
             "piece must coincide), and REMOVE everything else (pure white). The piece will be cut out and animated on a 2D skeleton, "
             "so the parts of it that were hidden behind other things must be drawn too. Coordinates are pixels on the 1536x1024 "
             "canvas (x from the left, y from the top).", "",
             d["en"], "", STYLE, "", BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        print(p)
        gd += [f"### `{ten}`: {d['vi']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(CONCEPT)}` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): pháp sư lửa con mũ trùm to, mắt lửa, hai búi tóc "
               "khói ngà, cổ áo choàng than viền vàng có đuôi nhọn, áo đỏ dây vàng, váy lửa, trượng ngắn có cầu lửa, hai bàn tay vuốt |", ""]
    gd += ["Kiểm: mảnh nằm đúng chỗ concept (chồng lên phải trùng phần lộ), mỗi mảnh một hình kín viền mực, phần khuất đã vẽ đủ, không dính thứ "
           "khác; trượng không còn cầu lửa và bàn tay."]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2: mảnh")[0].rstrip("\n") if os.path.exists(hd) else ""
    open(hd, "w", encoding="utf-8", newline="\n").write("\n".join([cu] + gd) + "\n")


# ---------------------------------------------------------------- cắt
def moi_nhat(tien_to):
    fs = [f for f in os.listdir(TAI) if f.startswith(tien_to) and f.endswith(".png") and (f[len(tien_to)] in "._")]
    fs = [f for f in fs if f[len(tien_to):] == ".png" or f[len(tien_to) + 1:-4].isdigit()]
    return os.path.join(TAI, sorted(fs, key=lambda f: os.path.getmtime(os.path.join(TAI, f)))[-1]) if fs else None


def cum(ten_anh, min_px=1500):
    """các cụm liền của tờ M_<tên> (ảnh RGBA đã cắt + góc trên trái trên khung concept), trái → phải theo tâm."""
    import cv2
    f = moi_nhat(f"M_{ten_anh}")
    if not f:
        print(f"  M_{ten_anh}: chưa gen")
        return []
    A = np.asarray(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = (A.min(2) < 236) | ((A.max(2) - A.min(2)) > 26)
    k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, k3).astype(bool)
    # lấp lỗ kín bên trong (vùng trắng không thông ra nền) TRỪ khi nó rộng: lòng móc trượng phải giữ trong suốt
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    out = []
    for i in sorted([i for i in range(1, n) if st[i, 4] > min_px], key=lambda i: cen[i][0]):
        m = lab == i
        k15 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (29, 29))
        for j in range(1, n):
            if j != i and st[j, 4] <= min_px and (cv2.dilate(m.astype(np.uint8), k15).astype(bool) & (lab == j)).any():
                m |= lab == j
        ys, xs = np.nonzero(m)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        mm = m[y0:y1, x0:x1]
        pad = np.pad(~mm, 1, constant_values=True)
        nl, ll, sl, _ = cv2.connectedComponentsWithStats(pad.astype(np.uint8), 4)
        ngoai = ll[0, 0]                              # vùng trắng thông ra nền
        dien = mm.sum()
        for j in range(1, nl):
            if j != ngoai and sl[j, 4] < 0.04 * dien:  # lỗ kín nhỏ (chấm sáng trong mắt, khe hở nét) thì lấp; lỗ lớn (lòng móc trượng) giữ
                mm = mm | (ll[1:-1, 1:-1] == j)
        al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
        rgb = A[y0:y1, x0:x1].astype(np.uint8)
        vien = mm & ~cv2.erode(mm.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))).astype(bool)
        al = np.where(vien, np.minimum(al, np.clip((250.0 - rgb.min(2).astype(np.float32)) / 70.0, 0, 1)), al)
        out.append((Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA"), int(x0), int(y0),
                    (float(cen[i][0]), float(cen[i][1]))))
    print(f"  M_{ten_anh} ({os.path.basename(f)}): {len(out)} cụm " + ", ".join(f"{im.size} ở ({x}, {y})" for im, x, y, _ in out))
    return out


def cat():
    os.makedirs(MANH, exist_ok=True)
    moi = {}

    def ghi(ten, c, **them):
        im, x0, y0, _ = c
        im.save(os.path.join(MANH, ten + ".png"))
        X, Y = tg(x0, y0)
        moi[ten] = dict(anh=ten, goc=[round(X, 2), round(Y, 2)], ti=TI, px=1.25, **them)

    c = sorted(cum("dau_lua"), key=lambda q: q[3][1])          # trên → dưới
    if len(c) >= 2:
        ghi("dau", c[0])
        ghi("lua_ao", c[1], kieu="xuong", sigma=54.0)
    c = cum("than")
    if c:
        ghi("ao", max(c, key=lambda q: q[0].width * q[0].height), kieu="xuong", sigma=62.0)
    c = cum("toc_duoi")
    if len(c) >= 3:
        duoi = max(c, key=lambda q: q[3][1])                   # thấp nhất: đuôi áo choàng
        con = sorted([q for q in c if q is not duoi], key=lambda q: q[3][0])
        ghi("vai_duoi", duoi, kieu="goc", theo="pifeng_02")
        # hai búi tóc: KHÔNG bám lưới tóc của họ (búi nằm xa ngoài lưới đó: lúc chết, lúc vụt trượng xương tóc quật mạnh, búi văng rời khỏi
        # mũ). Mảnh cứng trên xương mới là con của xương đầu, gốc xoay ở chỗ búi chui vào sau mũ; aura cho đung đưa nhẹ
        ghi("toc_tren", con[0], kieu="cung", xuong="toc_tren_x", cha="bone6", truc=[round(v, 1) for v in tg(690, 285)], lac=3.5, chu_ky=2.0, pha=0.0)
        ghi("toc_phai", con[-1], kieu="cung", xuong="toc_phai_x", cha="bone6", truc=[round(v, 1) for v in tg(965, 430)], lac=4.5, chu_ky=4.0 / 3, pha=1.1)
    c = cum("truong")
    if c:
        t = max(c, key=lambda q: q[0].width * q[0].height)
        t[0].save(os.path.join(MANH, "truong.png"))
        X, Y = tg(t[1], t[2])
        moi["_truong"] = dict(anh="truong", goc=[round(X, 2), round(Y, 2)], ti=TI, tam=[CAU["tam"][0] - t[1], CAU["tam"][1] - t[2]],
                              R=round(CAU["r"] * TI, 2))
    for r in DUNG_LAI:                                         # mảnh dùng lại của dạng 2 (cỡ theo xương / bán kính cầu)
        shutil.copyfile(os.path.join(MANH2, r + ".png"), os.path.join(MANH, r + ".png"))
    moi["_xuong"] = XUONG
    moi["_an"] = AN
    moi["_lop"] = {k: [x for x in v if x in moi] for k, v in LOP.items()}      # tờ chưa gen thì mảnh đó tạm vắng (dựng thử từng phần)
    if "_truong" not in moi:
        shutil.copyfile(os.path.join(MANH2, "wuqi.png"), os.path.join(MANH, "wuqi.png"))       # tạm: trượng dạng 2
    moi["_top"] = TOP
    moi["_tr_lech"] = TR_LECH
    moi["_die_nang"] = DIE_NANG
    json.dump(moi, open(os.path.join(MANH, "dat_moi.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(os.path.join(MANH, "dat_moi.json"), [k for k in moi])


TOP = [40.0, 930.0]             # chỗ cầu lửa bay lên ở chiêu cuối (thế giới rig)
# trượng thả rời dời thêm (thế giới) trong lúc rời tay: chiêu cuối cho lơ lửng bên trái mũ trùm (không thì che mặt: mũ to, thân thấp);
# lúc chết cho rơi xuống tận đất (dáng gốc của bone102 cao hơn thân 114 theo bàn tay)
TR_LECH = {"skill": [-460.0, -20.0], "die": [29.0, 273.0]}
DIE_NANG = 275.0                # lúc chết: dáng nằm của họ (cho thân cao, đầu nhỏ) làm mũ trùm to chìm ~300 dưới đất → nâng thân dần lúc rơi


# ---------------------------------------------------------------- so concept
def rig_mod():
    os.environ["PL_NON"] = "1"
    import contextlib
    import io
    import phap_lua_rig as R
    with contextlib.redirect_stdout(io.StringIO()):
        sk, info = R.dung()
        clips = R.lam_clip(sk, info)
    return R, sk, info, clips


def so(khung=None):
    """khung 0 idle (không khói) trên đúng khung concept: concept | rig | lệch (đỏ: concept có mà rig thiếu; xanh: rig thừa) + viền rig trên concept."""
    import cv2
    from quai import hoat, soi
    R, sk, info, clips = rig_mod()
    P = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
    for i in range(R.N_KHOI):
        P.alpha[f"khoi_{i}"] = P.alpha[f"khoi_{i}_t"] = 0.0
    x0, y1 = tg(0, 0)
    x1, y0 = tg(W, H)
    im = soi.Ve(sk).ve(P, (x0, y0, x1, y1), 1.0 / TI, bg=(255, 255, 255), ss=2).convert("RGB").resize((W, H), Image.LANCZOS)
    cc = Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS)
    ma, mb = np.asarray(im).min(2) < 225, np.asarray(cc).min(2) < 225
    vis = np.full((H, W, 3), 255, np.uint8)
    vis[ma & mb] = (170, 170, 170)
    vis[mb & ~ma] = (230, 60, 60)
    vis[ma & ~mb] = (60, 190, 60)
    ed = cv2.Canny(cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY), 80, 160) > 0
    ov = (np.asarray(cc).astype(np.float32) * 0.55 + 255 * 0.45).astype(np.uint8)
    ov[cv2.dilate(ed.astype(np.uint8), np.ones((2, 2), np.uint8)) > 0] = (230, 30, 30)
    out = Image.new("RGB", (W * 2, H * 2), (255, 255, 255))
    out.paste(cc, (0, 0))
    out.paste(im, (W, 0))
    out.paste(Image.fromarray(vis), (0, H))
    out.paste(Image.fromarray(ov), (W, H))
    pth = os.path.join(R.RA, "so_concept.png")
    os.makedirs(R.RA, exist_ok=True)
    out.save(pth)
    print(pth, f"IoU hình bóng {float((ma & mb).sum()) / max(1, (ma | mb).sum()):.3f}")
    W0 = sk.the_gioi(P)
    for b in ("bone6", "bone42", "bone45", "bone56", "bone7", "bone10", "bone21", "cau_goc", "bone61", "bone25"):
        print(f"  {b}: thế giới {W0[b][:2, 2].round(1)} = px concept {np.round(px(*W0[b][:2, 2]), 0)}")


# ---------------------------------------------------------------- gộp tiến hóa
def th():
    import atomik_dang as A
    ra_d1 = os.path.join(BASE, "rig_d1")
    ra = os.path.join(BASE, "rig")
    os.makedirs(ra, exist_ok=True)
    J, img, ver = A.load(os.path.join(ra_d1, "phap_lua_non.atomik"))
    JB, imgB, _ = A.load(os.path.join(HERE, "inbox", "phap_lua_1", "rig", "phap_lua_1.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1 or s["name"].startswith("khoi_")}
    # dung lượng: dạng 2 trong rig gộp chỉ diễn idle. Hình của các slot ẩn suốt idle (bản _t, trượng thả rời, bàn tay thứ hai, khói: khói chỉ
    # chạy trong clip aura của dạng 2, rig gộp không có) thay bằng một tam giác rỗng: bớt lưới và trọng số không bao giờ vẽ
    idB = JB["anims"][A.clip(JB, "idle")]
    hien = {i for i in range(len(JB["slots"])) if i not in an_B}
    for x in idB.get("sa") or []:
        if x["slot"] not in hien and JB["slots"][x["slot"]]["name"].startswith("khoi_") is False and max(x["keys"][1::7]) > 0.01:
            hien.add(x["slot"])
            an_B.discard(x["slot"])
    can = {JB["slots"][i].get("att", -1) for i in hien}
    for x in idB.get("sk") or []:
        if x["slot"] in hien:
            can |= set(x["atts"])
    bo = 0
    for i, a in enumerate(JB["atts"]):
        if i not in can and a["slot"] not in hien:
            a["uvs"], a["tris"], a["wInfo"] = [0, 0, 0, 0, 0, 0], [0, 1, 2], [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1]
            bo += 1
    print(f"dạng 2 trong rig gộp: {len(hien)} slot hiện ở idle, {bo} / {len(JB['atts'])} hình không vẽ thay bằng tam giác rỗng")
    nA_s, nA_b = len(J["slots"]), len(J["bones"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = SIZE_B / SIZE_A * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, nhe=NHE, than_A=A.bi(J)["bone4"])
    ev = J["anims"][-1]
    for tl in ev["tls"]:                             # dạng 1 mờ hẳn từ 1,35 s: khoá idle của nó sau 1,5 s không ai thấy, bỏ (dung lượng)
        if tl["bone"] < nA_b:
            S = 7 if tl["type"] == 0 else 12
            kk = tl["keys"]
            m = len(kk) // S
            giu = [i for i in range(m) if kk[i * S] <= 1.5]
            if giu and len(giu) < m:
                giu.append(giu[-1] + 1)
                tl["keys"] = [v for i in giu for v in kk[i * S:(i + 1) * S]]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(ra, "phap_lua_non.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; dạng 2 trong rig gộp × {k_B:.3f}; {n} slot ẩn giữ ẩn trong evolve; {kq}")
    chan_dung()
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    ims = [A.render(J, img, A.Pose(J).at(ci, t), box, 0.45, bg=(150, 150, 150)).convert("RGB") for t in ts]
    cot = 6
    out = Image.new("RGB", (cot * ims[0].width, ((len(ims) + cot - 1) // cot) * ims[0].height), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    out.save(os.path.join(ra, "khung_evolve.png"))
    print(os.path.join(ra, "khung_evolve.png"), out.size)


NHE = 0.40                      # atlas dạng 2 trong rig gộp thu còn chừng này (chỉ hiện 2 giây cuối clip evolve)
def chan_dung():
    """chân dung 512 của dạng 1: khung 0 idle, CÓ cầu lửa, lưỡi lửa, hai búi tóc (bản của xuat.xuat_het bỏ mọi slot mà clip aura đụng tới nên
    mất cầu lửa và tóc); chỉ bỏ khói."""
    from quai import hoat, soi
    R, sk, info, clips = rig_mod()
    P = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
    for i in range(R.N_KHOI):
        P.alpha[f"khoi_{i}"] = P.alpha[f"khoi_{i}_t"] = 0.0
    os.makedirs(os.path.join(BASE, "rig"), exist_ok=True)
    print(soi.chan_dung(soi.Ve(sk), P, os.path.join(BASE, "rig", "chan_dung.png")))


SIZE_A, SIZE_B = 0.8, 1.1       # cỡ dạng 1, dạng 2 trong heroes.json (khối hong_lien; quai/doi_phap_lua.py CO_NON)


# ---------------------------------------------------------------- số đo cho HatPhap.cs
def do():
    import atomik_dang as A
    J, img, _ = A.load(os.path.join(BASE, "rig", "phap_lua_non.atomik"))
    B = A.bi(J)
    Hh = J["game"]["height"]

    def pt(clip, t, bone):
        P = A.Pose(J).at(A.clip(J, clip), t)
        p = P.bone_pt(B[bone])
        w = P.w[B[bone]]
        return round(p[0] / Hh, 3), round(p[1] / Hh, 3), round(float(np.hypot(w[0], w[2])), 2)
    print(f"chiều cao khai {Hh:.1f}; hitTimes {J['game']['hitTimes']}")
    print("cast, đầu trượng (mieng):", {t: pt("cast", t, "mieng")[:2] for t in (0.16, 0.3, 0.5, 0.8)})
    print("skill, tâm cầu (mieng) + tỉ lệ:", {t: pt("skill", t, "mieng") for t in (0.66, 1.05, 2.05, 2.20, 2.25)})
    Rw = json.load(open(os.path.join(MANH, "dat_moi.json"), encoding="utf-8"))["_truong"]["R"]
    print(f"bán kính gốc của cầu: {Rw} đơn vị = {Rw / Hh:.3f} chiều cao khai")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c in ("prompt", "cat", "so", "th", "do", "chan_dung"):
        globals()[c]()
    else:
        print(__doc__)
