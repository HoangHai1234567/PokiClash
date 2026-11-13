# -*- coding: utf-8 -*-
"""Quỷ lửa bắn cung (cung_lua, tướng thứ 3 đảo Hỏa): RESKIN đúng nghĩa trên con gốc monster_3357 (skill pokiclash-spine-rig mục 23).

Người dùng 2026-11-13 (sau hai bản rig tự chia mảnh bị chê): "xấu quá, xóa hết đi làm lại từ đầu, xem con gốc tách như nào thì mình tách và
gen như thế". → Mỗi mảnh của con gốc một mảnh của mình, vẽ trên CHÍNH khung ảnh vùng của mảnh đó; tờ hướng dẫn là các mảnh GỐC (cắt theo
lưới, phóng to) để GPT thấy cấu trúc thật của từng mảnh (bản trước chỉ đưa hình bóng trơn → GPT tô thành cục). GPT chỉ đổi da: giáp cháy
đen, lửa, khe sáng; giữ hình bóng và các đường cấu trúc. Ảnh con gốc chỉ nằm trong máy và gửi GPT làm mẫu, không đăng công khai.

    cung_lua_da.py to       tờ mảnh gốc + file prompt → inbox/cung_lua_1/mau/goc_<A|B>.png (+ .json), gui_gpt/cung_lua_1/luot_1_da_<A|B>.txt, HUONG_DAN.md
    cung_lua_da.py cat      cắt tờ D_A / D_B đã gen → inbox/cung_lua_1/manh/<vùng>.png (cỡ ảnh vùng × RES) + _so_<A|B>.png, _iou.json
"""
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
import cung_lua as G  # noqa: E402

W, H = 1536, 1024
RES = 2                      # ảnh mảnh của mình = ảnh vùng của họ × RES
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "cung_lua_1")
CONCEPT = os.path.join(G.MAU, "concept_A.png")
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
SUNG_NOI = 0.62              # vòm sau mũ (to_01): nới khung lên trên theo bề cao vùng cho HAI SỪNG (mảnh vẫn là một, bám xương đầu như họ)
SAM = (52, 42, 44)
INK = (43, 33, 24)

# tờ → các hàng [(vùng, phóng)]
TO = {
    "A": [[("tofa", 2.6), ("to_02", 2.6), ("to_01", 2.6)], [("gongjian_01", 2.5), ("jian", 2.6), ("jiandai", 2.6)]],
    "B": [[("xiong", 3.0), ("yao", 3.0), ("zuoxiaobi", 3.0), ("youxiaobi", 3.0), ("zuojianjia", 3.0), ("youjianjia", 3.0)],
          [("zuodabi", 3.0), ("youdabi", 3.0), ("pigu", 3.0), ("zuodatui", 3.0), ("youdatui", 3.0), ("zuojiao", 3.0), ("youjiao", 3.0)],
          [("zuoshou_01", 5.0), ("zuoshou_02", 5.0), ("youshou_01", 5.0), ("youshou_02", 5.0)]],
}


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vung():
    """{vùng: (hình đầu tiên dùng vùng đó, ảnh part cắt theo lưới)}."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_goc.json")
    out = {}
    for a in atts:
        if a["region"] not in out:
            out[a["region"]] = (a, G.part_goc(a))
    return out


def sung(g, n, rong, cong):
    g, n = np.array(g, float), np.array(n, float)
    ts = np.linspace(0, 1, 40)
    d = n - g
    L = np.linalg.norm(d)
    pp = np.array([-d[1], d[0]]) / L
    sp = g[None] + d[None] * ts[:, None] + pp[None] * (cong * np.sin(ts * math.pi))[:, None]
    wd = rong * 0.5 * (1 - ts) ** 0.85
    dx, dy = np.gradient(sp[:, 0]), np.gradient(sp[:, 1])
    nn = np.hypot(dx, dy) + 1e-6
    A = np.stack([sp[:, 0] - dy / nn * wd, sp[:, 1] + dx / nn * wd], 1)
    B = np.stack([sp[:, 0] + dy / nn * wd, sp[:, 1] - dx / nn * wd], 1)
    return np.concatenate([A, B[::-1]], 0)


def to():
    V = vung()
    os.makedirs(G.MAU, exist_ok=True)
    os.makedirs(GUI, exist_ok=True)
    os.makedirs(G.TAI, exist_ok=True)
    O = {}
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = []
            for r, z in h_:
                im = V[r][1]
                noi = int(round(im.height * SUNG_NOI)) if r == "to_01" else 0
                cs.append((r, z, im, noi, int(round(im.width * z)), int(round((im.height + noi) * z))))
            cao.append((cs, max(c[5] for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[4] for c in cs)) // (len(cs) + 1)
            x = ke
            for r, z, im, noi, cw, ch in cs:
                y0 = y + (hh - ch) // 2
                big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
                if noi:                               # hai sừng mọc từ đỉnh vòm sau mũ (vẽ bằng mã, tô phẳng)
                    hw, hh_ = big.width, big.height
                    nz = int(round(noi * z))
                    m = np.zeros((ch, cw), np.uint8)
                    for bx, ex, ey, rong, cong in ((0.30, 0.10, -0.52, 0.30, 0.14), (0.70, 0.95, -0.46, 0.27, -0.13)):
                        P = sung((bx * hw, nz + 0.20 * hh_), (ex * hw, nz + ey * hh_), rong * hw, cong * hw)
                        cv2.fillPoly(m, [P.astype(np.int32)], 1)
                    m = cv2.GaussianBlur(m * 255, (0, 0), 2.0) > 127
                    a = np.zeros((ch, cw, 4), np.uint8)
                    a[m] = SAM + (255,)
                    a[m & ~cv2.erode(m.astype(np.uint8), el(4)).astype(bool)] = INK + (255,)
                    can.alpha_composite(Image.fromarray(a, "RGBA"), (x, y0))
                    can.alpha_composite(big, (x, y0 + nz))
                else:
                    can.alpha_composite(big, (x, y0))
                o[r] = dict(hop=[x, y0, cw, ch], z=z, noi=noi)
                x += cw + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    prompt(O)


def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of the separate body PARTS of a 2D animation puppet (an armoured knight archer), each part drawn "
    "alone on white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
    "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet (if the "
    "new picture were laid over image 1, every part must coincide with the old one), and its main structural lines (plate edges, bands, "
    "folds, the visor openings). Do NOT merge parts, do NOT add parts, do NOT move parts. Pure white (#FFFFFF) between the parts.")
STYLE = (
    "NEW LOOK (the same for all parts; see image 2, the approved picture of OUR character, for the exact colours and drawing style): a "
    "BURNING KNIGHT in CHARRED armour. Hand-drawn on paper: a wobbly dark-brown ink outline (#2B2118, about {px} px) running all the way "
    "round every part exactly on its silhouette, thinner ink lines for the inner structural lines, and every area filled with ONE flat "
    "colour with visible coloured-pencil / wax-crayon hatching. Colours: armour plates charred brown-black (#644A44); the darker parts "
    "(under-suit, joints, bands, the dome) darker charred black (#342A2C); fire red-orange (#DE4022) / orange (#F88C28) / yellow "
    "(#FFD254); gold (#E8B24A) only where listed. The parts of image 1 are painted in a smooth digital cel style with blue-grey armour, "
    "gold trims, a red letter emblem and light / dark shading bands: do NOT copy that painting style, those colours, the gold trims or "
    "the emblem; no shading, no highlights, no gradients, no glow, no shadows: flat colour only.")
BG = ("Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added.")

MO_TA = {
    "A": [
        ("tofa", "THE HELMET PLUME → A FLAME: the same sweeping plume silhouette (wide round top, long curve, thin hooked tip at the bottom) "
                 "repainted as ONE flame with three flat colour zones following the shape: red-orange (#DE4022) along the outer edge, orange "
                 "(#F88C28), and a big yellow (#FFD254) zone inside, the zone borders wavy like flame tongues. Its edge stays on the silhouette."),
        ("to_02", "THE HELMET FRONT (the visor plate, wider at the sides): charred brown-black plate; the visor openings (three tall slots and a "
                  "narrow fourth one at the right edge) stay exactly where they are and are filled with glowing flat yellow (#FFD254) with an "
                  "ink outline; the band along the top and left rim (gold in image 1) becomes a plain darker charred band (#342A2C)."),
        ("to_01", "THE BACK DOME OF THE HELMET WITH TWO HORNS: the round dome (lower part of this piece) plain darker charred black (#342A2C) "
                  "with its small knob on top; the two curved horns rising from its top (flat dark shapes in image 1) are part of the same "
                  "piece: smooth dark charred horns (#342A2C), thick at the base, sharp at the tip, each with two thin ring grooves near "
                  "its base. One closed shape: dome and horns together."),
        ("gongjian_01", "THE BOW (two curved limbs joined at the grip, each ending in a broad pointed fin, with a sharp fin on its back): the "
                        "same silhouette, charred black horn (#342A2C); keep the line where the two limbs meet at the grip; add ONE thin crack "
                        "of fire (orange #F88C28 with a yellow centre) running along the middle of each limb."),
        ("jian", "THE ARROW (a short thick shaft with a big head pointing to the lower right): shaft darker charred black (#342A2C); the big "
                 "arrowhead gold (#E8B24A) with one ink line down its middle."),
        ("jiandai", "THE QUIVER (a tilted box with three arrow ends sticking out of its top left): the box charred brown-black with its darker "
                    "band on the left side (#342A2C); the three arrow ends gold (#E8B24A)."),
    ],
    "B": [
        ("xiong", "CHEST PLATE: charred brown-black; the two bands (gold in image 1) become darker charred bands (#342A2C); the red letter "
                  "emblem is REMOVED and replaced by ONE natural crack of fire in the same place (a single slightly curved line, thicker in the "
                  "middle, tapering at both ends, orange #F88C28 with a yellow #FFD254 centre)."),
        ("yao", "WAIST SKIRT (pointed armour flaps): charred brown-black flaps; the trims (gold in image 1) become darker charred lines."),
        ("zuoxiaobi", "BIG NEAR GAUNTLET (the egg-shaped plate with cracks): charred brown-black; its branching cracks stay where they are and "
                      "become cracks of fire (orange #F88C28 with a yellow #FFD254 centre)."),
        ("youxiaobi", "FAR FOREARM GUARD: charred brown-black, keep its plate edge line."),
        ("zuojianjia", "NEAR SHOULDER PAD (pointed plate): charred brown-black; its lower trim becomes a darker charred band."),
        ("youjianjia", "FAR SHOULDER PAD: the same."),
        ("zuodabi", "NEAR UPPER ARM: darker charred black (#342A2C), plain."),
        ("youdabi", "FAR UPPER ARM: darker charred black, plain."),
        ("pigu", "HIP PIECE: darker charred black, plain."),
        ("zuodatui", "NEAR THIGH: darker charred black, plain."),
        ("youdatui", "FAR THIGH: darker charred black, plain."),
        ("zuojiao", "NEAR BOOT: charred brown-black armour boot, keep its plate lines."),
        ("youjiao", "FAR BOOT: the same."),
        ("zuoshou_01", "NEAR HAND, main piece (bottom row, drawn very big): a darker charred black gauntlet fist (#342A2C); keep the lines "
                       "between its fingers."),
        ("zuoshou_02", "NEAR HAND, small front piece: the same darker charred black."),
        ("youshou_01", "FAR HAND, main piece: the same gauntlet fist; keep the finger lines."),
        ("youshou_02", "FAR HAND, small piece: the same."),
    ],
}
VI = {"A": "ngọn lửa (chùm lông mũ), mặt nạ mũ, vòm sau mũ + hai sừng, cây cung, mũi tên, ống tên",
      "B": "giáp ngực, váy giáp, bao tay gần, cẳng tay xa, hai tấm vai, hai bắp tay, hông, hai đùi, hai ủng, bốn mảnh bàn tay"}


def prompt(O):
    gd = ["# Gói gửi GPT: `cung_lua` (quỷ lửa bắn cung, tướng thứ 3 đảo Hỏa, tên chưa đặt)", "",
          "Làm lại từ đầu 2026-11-13 theo lời người dùng: \"xem con gốc tách như nào thì mình tách và gen như thế\". Reskin trên con gốc "
          "`monster_3357`: mỗi tờ là các mảnh GỐC cắt ra từ rig (phóng to), GPT vẽ lại da từng mảnh đúng chỗ, đúng cỡ, đúng hình bóng. "
          "Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai. Ghi chú: `ArtGen/Spine/inbox/cung_lua_ghichu.md`.", ""]
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out = os.path.join(G.TAI, f"D_{ma}.png")
        p = os.path.join(GUI, f"luot_1_da_{ma}.txt")
        R = [(mau, "the PARTS SHEET, 1536x1024, white background: the separate body parts of the puppet, each drawn alone, at the exact "
                   "size and place to keep. " + ("Six parts: top row a big helmet plume, the helmet front plate with visor slots, the round "
                                                  "back dome of the helmet with two dark horns above it; bottom row a big bow, a short arrow, a "
                                                  "quiver." if ma == "A" else
                                                  "Seventeen parts: top row six armour pieces (chest plate, waist skirt, big cracked gauntlet, "
                                                  "forearm guard, two shoulder pads); middle row seven small pieces (two upper arms, hip, two "
                                                  "thighs, two boots); bottom row the four pieces of the two hands, drawn very big."),
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng 2,5–5 lần: {VI[ma]}. Hình cel số màu lam xám, viền vàng"),
             (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: a chibi burning knight archer in charred "
                       "brown-black armour with a big helmet with glowing yellow visor slits, two dark horns, a flame as helmet plume and "
                       "cracks of fire on the chest and the gauntlet. Take from it ONLY the colours, the materials and the hand-drawn look "
                       "(wobbly brown ink line, crayon hatching, flat colour). Do NOT copy its shapes or its pose: the shapes come from image 1.",
              "Concept đã duyệt của mình (bản A, 1536 × 1024, nền trắng): chỉ lấy màu, chất liệu, nét vẽ tay"),
             (KIEM_SI, "an approved hero of the same game, 1536x1024: the hand-drawn ink and crayon style to match. Do NOT copy its design.",
              "Voọc Tướng đã duyệt: chỉ lấy nét vẽ")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "", CHUNG, "", STYLE.format(px="6" if ma == "A" else "6 (about 9 on the four big hand pieces of the bottom row)"),
              "", "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        t += [f"{i}. ({cho(o, r)}) {mt}" for i, (r, mt) in enumerate(MO_TA[ma], 1)]
        t += ["", BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        print(p)
        gd += [f"## Tờ `{ma}`: {VI[ma]}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/cung_lua_1/luot_1_da_{ma}.txt`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["## Kiểm", "",
           "- Mỗi mảnh nằm ĐÚNG chỗ, đúng cỡ, đúng hình bóng mảnh gốc (chồng lên tờ mảnh gốc phải trùng); đủ số mảnh, không dính nhau.",
           "- Da mới: giáp cháy nâu đen, mảng sẫm, lửa ba màu phẳng, khe mũ vàng sáng; không còn lam xám, viền vàng, chữ S đỏ; không bóng, không quầng sáng.",
           "- Nét bút nâu rung, vân sáp; nền trắng tinh.", "",
           "Cắt: `py -3 -I ArtGen/Spine/cung_lua_da.py cat` (in độ khớp hình bóng từng mảnh).", "",
           "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Mảnh lệch chỗ / đổi cỡ | `Every part must stay at exactly the same place and size as in image 1; lay your picture over image 1 and check.` |",
           "| Còn màu lam, viền vàng, chữ S | `Remove every blue-grey colour, gold trim and the red letter emblem: charred brown-black armour only.` |",
           "| Tô khối, có bóng | `Flat colour only: no shading bands, no highlights, no gradients.` |"]
    open(os.path.join(GUI, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")


def nen(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def cat():
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    ious = {}
    for ma in TO:
        fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(f"D_{ma}") and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
        if not fs:
            print(f"tờ {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(os.path.join(G.TAI, fs[-1])).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg = ~nen(A)
        fgG = Gd.min(2) < 238
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
            # ảnh RGBA đúng khung ô
            rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
            mm = m[y:y + ch, x:x + cw]
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
            sang = rgb.min(2).astype(np.float32)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            # về cỡ ảnh vùng × RES; giữ trong hình bóng gốc nới 3 px (phần sừng nới thêm thì để nguyên)
            goc = V[r][1]
            noi = d["noi"]
            tw, th = goc.width * RES, (goc.height + noi) * RES
            im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
            a2 = np.asarray(im2).copy()
            ag = np.asarray(goc.resize((goc.width * RES, goc.height * RES), Image.LANCZOS))[..., 3] > 60
            gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
            gh = np.ones((th, tw), bool)
            gh[noi * RES:] = gioi
            if noi:
                gh[noi * RES:noi * RES + int(0.30 * goc.height * RES)] = True       # chỗ gốc sừng chờm lên vòm
            a2[..., 3] = np.where(gh, a2[..., 3], 0)
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            a = mm
            b = fgG[y:y + ch, x:x + cw]
            iou = float((a & b).sum()) / max(1, (a | b).sum())
            ious[r] = round(iou, 3)
            vis = np.full((ch, cw, 3), 255, np.uint8)
            vis[a & b] = (170, 170, 170)
            vis[b & ~a] = (230, 60, 60)
            vis[a & ~b] = (60, 190, 60)
            so.append((Image.fromarray(vis), Image.fromarray(a2, "RGBA")))
            print(f"  {r:12s} IoU {iou:.3f}")
        w_ = sum(max(s[0].width, s[1].width) + 10 for s in so)
        hh = max(s[0].height for s in so)
        h2 = max(s[1].height for s in so)
        out = Image.new("RGB", (w_ + 10, hh + h2 + 30), (150, 150, 150))
        xx = 10
        for vis, kh in so:
            out.paste(vis, (xx, 10))
            out.paste(kh, (xx, hh + 20), kh)
            xx += max(vis.width, kh.width) + 10
        out.save(os.path.join(MANH, f"_so_{ma}.png"))
        print(os.path.join(MANH, f"_so_{ma}.png"))
    json.dump(ious, open(os.path.join(MANH, "_iou.json"), "w"), indent=1)
    # dây cung: mảnh của họ là một sợi đỏ mảnh → đổi màu bằng mã (cam lửa, giữ viền sẫm)
    goc = V["gongjian_02"][1]
    g = np.asarray(goc.resize((goc.width * RES, goc.height * RES), Image.LANCZOS)).copy()
    sang = g[..., :3].max(2)
    g[..., :3] = np.where((sang > 110)[..., None], np.array([248, 140, 40], np.uint8), np.array(INK, np.uint8))
    Image.fromarray(g, "RGBA").save(os.path.join(MANH, "gongjian_02.png"))
    print("  gongjian_02  đổi màu bằng mã")


if __name__ == "__main__":
    if sys.argv[1:2] == ["to"]:
        to()
    elif sys.argv[1:2] == ["cat"]:
        cat()
    elif sys.argv[1:2] not in (["ten_lua"], ["ten_lua_cat"]):
        print(__doc__)


# ---------------------------------------------------------------- mũi tên lửa năng lượng của chiêu cuối (mảnh rời, không có ở con gốc)
# người dùng 2026-11-13: "mũi tên cuối trong chiêu cuối nên là 1 mũi tên lửa năng lực rực cháy, khác với mũi tên thường"
TL_NOCK, TL_Y = 340, 512            # chỗ đuôi tên tì dây (x) và trục mũi tên (y) trên tờ 1536 × 1024, ghi trong prompt


def ten_lua_to():
    da = os.path.join(G.TAI, "D_A.png")
    out = os.path.join(G.TAI, "T_LUA.png")
    p = os.path.join(GUI, "luot_2_ten_lua.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(da)}: a sheet of parts of OUR character (a burning knight archer), 1536x1024, white background: a flame plume (top "
         "left), helmet pieces, a black bow with cracks of fire, a short dark arrow with a gold head, a quiver. Use it ONLY for the drawing "
         "style: the wobbly dark-brown ink outline, the crayon hatching, and the way the FLAME is drawn as flat nested colour zones. The new "
         "arrow must look clearly DIFFERENT from the plain dark arrow of this sheet.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as T_LUA_2.png, T_LUA_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: draw ONE object alone on a pure-white 1536x1024 canvas: a BLAZING FIRE-ENERGY ARROW, the charged final shot of the burning "
         "knight archer. It lies exactly HORIZONTAL, pointing to the RIGHT, its axis on the line y = 512; the whole object from about x = 150 "
         "to x = 1390 and from about y = 350 to y = 675.", "",
         "DESIGN: the whole arrow is made of fire and energy, not of wood or metal:",
         "- SHAFT: a straight bar of pure bright energy along y = 512, from x = 340 to about x = 1120, about 34 px thick: pale yellow-white "
         "(#FFF2B0) with a yellow (#FFD254) edge.",
         "- ARROWHEAD (about x = 1100 to x = 1390, about 180 px tall): a big, sharp, leaf-shaped blade of fire, its tip exactly at "
         "(1390, 512): pale yellow-white (#FFF2B0) core, then yellow (#FFD254), orange (#F88C28) and a red-orange (#DE4022) outer rim; its "
         "two rear barbs sweep back like flame tongues.",
         "- FLAMES ALONG THE SHAFT: five or six big flame tongues grow from the shaft, alternating above and below it, all streaming "
         "BACKWARD (to the left), small near the head and bigger toward the back; each tongue red-orange outside, orange, yellow near the "
         "shaft.",
         "- TAIL (about x = 150 to x = 340): instead of feathers, a big flaring tail of fire with three long tongues streaming back to the "
         "left, the middle one longest. The tail meets the shaft at x = 340 (that point sits on the bowstring).",
         "", "STYLE: hand-drawn like image 1: ONE closed shape with a wobbly dark-brown ink outline (#2B2118, about 6 px) all the way round "
         "the outer silhouette; inside, flat colour zones with visible crayon hatching, the zone borders wavy like flames (thin red-orange "
         "lines allowed between zones, no black lines inside). Bold, simple, readable shapes.",
         "FLAT COLOUR ONLY: the arrow looks blazing because its flat colours are bright and its shapes are flames; NO glow, NO halo, NO "
         "gradients, NO blur, NO sparks or embers flying off, no shadow, no detached pieces.", "",
         BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2: mũi tên lửa")[0].rstrip("\n")
    gd = [cu, "", "## Lượt 2: mũi tên lửa năng lượng của chiêu cuối (2026-11-13)", "",
          "Người dùng: \"mũi tên cuối trong chiêu cuối nên là 1 mũi tên lửa năng lực rực cháy, khác với mũi tên thường\". Mảnh rời (con gốc không có).", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(da)}` | Tờ mảnh đã reskin của mình (1536 × 1024, nền trắng): ngọn lửa ba màu phẳng, mũ, cung, mũi tên thường thân sẫm đầu vàng, ống tên. Chỉ lấy nét vẽ và cách vẽ lửa |",
          "", "Kiểm: một mũi tên toàn lửa nằm ngang chĩa phải, trục y = 512, đuôi tì dây ở x = 340, mũi ở (1390, 512); một hình kín viền mực; tô phẳng, "
          "không quầng sáng, không tàn lửa rời. Cắt: `py -3 -I ArtGen/Spine/cung_lua_da.py ten_lua_cat`."]
    open(hd, "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)


def ten_lua_cat():
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith("T_LUA") and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    A = np.asarray(Image.open(os.path.join(G.TAI, fs[-1])).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = ~nen(A)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    i = 1 + int(np.argmax(st[1:, 4]))
    m = lab == i
    x0, y0, w, h = st[i, :4]
    rgb = A[y0:y0 + h, x0:x0 + w].astype(np.uint8)
    mm = m[y0:y0 + h, x0:x0 + w]
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, "ten_lua.png"))
    ys, xs = np.nonzero(mm)
    mui = [int(xs.max()), int(round(ys[xs == xs.max()].mean()))]
    meta = dict(nock=[int(TL_NOCK - x0), mui[1]], mui=mui,          # trục mũi tên lấy theo chỗ mũi thật (GPT vẽ lệch trục vài px)
                co=[int(w), int(h)], nguon=fs[-1])
    json.dump(meta, open(os.path.join(MANH, "ten_lua.json"), "w"), indent=1)
    print("ten_lua", (w, h), meta)


if __name__ == "__main__" and sys.argv[1:2] == ["ten_lua"]:
    ten_lua_to()
if __name__ == "__main__" and sys.argv[1:2] == ["ten_lua_cat"]:
    ten_lua_cat()
