# -*- coding: utf-8 -*-
"""Vua robot (vua_may, rig monster_3637): ảnh mẫu cho concept lượt 1.

    vua_may_da.py ca_con    hình cả con gốc ở khung 0 idle trên nền trắng → inbox/vua_may_1/mau/goc_ca_con.png (+ .json khung từng part)
    vua_may_da.py bo_cuc    SƠ ĐỒ BỐ CỤC: thân con gốc nâng lên DY, bỏ hai chân xích, vẽ hai CHÂN ROBOT (khối phẳng) và BỐN CÁNH lơ lửng
                            (quạt lưỡi xám) đúng chỗ dự kiến lắp xương → mau/bo_cuc.png (+ .json: phép đổi toạ độ, chỗ khớp chân, gốc cánh)
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vua_may as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
MUC = (43, 33, 24)
DY = 150.0  # nâng cả thân lên (đơn vị rig) để có chỗ cho chân robot đi lại
BO = ("jiao_l_03", "jiao_r_3")  # hai chân xích của họ: bỏ

# CHÂN (đơn vị rig, SAU khi nâng thân; y = 0 là mặt đất). gan = chân phía người xem (bên TRÁI hình, vẽ trước khối hông),
# xa = bên PHẢI hình (vẽ sau khối hông, sau thân). hong = khớp háng, goi = khớp gối, co = cổ chân, ban = (gót x, mũi x, cao bàn)
CHAN = {
    "xa": dict(hong=(150, 262), goi=(250, 160), co=(262, 74), ban=(130, 410, 92), day=(170, 150)),
    "gan": dict(hong=(-140, 258), goi=(-250, 158), co=(-262, 74), ban=(-420, -120, 96), day=(176, 156)),
}
# CÁNH: gốc (đơn vị rig sau khi nâng), góc mép trước (độ, 0 = sang phải, ngược kim), dài, chiều quạt (+1 ngược kim), số lưỡi,
# thứ tự: sau thân (mọi cánh đều sau thân; cánh xa vẽ trước cánh gần vì nằm sau hơn? không: cả bốn sau thân, cánh xa vẽ trước = nằm dưới)
CANH = {
    "tren_xa": dict(goc=(60, 980), huong=58, dai=600, quat=-1, luoi=6),
    "duoi_xa": dict(goc=(150, 800), huong=-8, dai=440, quat=-1, luoi=5),
    "tren_gan": dict(goc=(-200, 930), huong=128, dai=680, quat=+1, luoi=6),
    "duoi_gan": dict(goc=(-260, 760), huong=192, dai=500, quat=+1, luoi=5),
}
THU_TU_CANH = ["tren_xa", "duoi_xa", "tren_gan", "duoi_gan"]  # vẽ trước → sau (đều nằm sau thân)


def Wp(p):
    return os.path.normpath(p)


def _atts():
    _, imgs, atts = G.nap("att_idle0.json")
    return imgs, [a for a in atts if a.get("region")]


def _khung(P, cao=820.0, rong=1300.0):
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), rong / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (np.asarray(V, float)[..., 0] - cx) * s,
                                             H / 2 - (np.asarray(V, float)[..., 1] - cy) * s], -1))


def _ve_parts(can, atts, T, S, dy=0.0, bo=()):
    hop = {}
    for a in atts:
        if a["slot"] in bo:
            continue
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        V = np.array(a["xy"], float).reshape(-1, 2) + [0, dy]
        lay = Image.new("RGBa", can.size, (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(V) * S, uv, tr)
        lay = lay.convert("RGBA")
        al = np.asarray(lay)[..., 3] > 60
        if al.any():
            ys, xs = np.nonzero(al)
            hop[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
        can.alpha_composite(lay)
    return hop


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024."""
    imgs, atts = _atts()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    s, cx, cy, T = _khung(P, 800.0, 1250.0)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    hop = _ve_parts(can, atts, T, S)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")


def _tron(c, r, n=40):
    return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def _doan(a, b, w0, w1=None):
    """hình thang dọc đoạn a → b, bề ngang w0 ở a, w1 ở b."""
    w1 = w0 if w1 is None else w1
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    n = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-9)
    return [tuple(a + n * w0 / 2), tuple(b + n * w1 / 2), tuple(b - n * w1 / 2), tuple(a - n * w0 / 2)]


def chan_hinh(c):
    """các khối của một chân (đơn vị rig): đùi, gối, ống, bàn; trả [(tên, đa giác, màu)] vẽ sau → trước."""
    vang, sam, khop = (233, 196, 112), (196, 150, 72), (92, 80, 60)
    hx, hy = c["hong"]
    gx, gy = c["goi"]
    ox, oy = c["co"]
    g, m, cao = c["ban"]
    dd, do = c["day"]
    ra = [("khop_hong", _tron((hx, hy), 64), khop),
          ("dui", _doan((hx, hy), (gx, gy), dd, dd * 0.8), vang),
          ("ong", _doan((gx, gy - 10), (ox, oy + 6), do * 0.95, do * 1.2), sam),
          ("khop_co", _tron((ox, oy + 12), 44), khop),
          ("ban", [(g, 0), (g, cao * 0.7), (g + (m - g) * 0.22, cao), (g + (m - g) * 0.7, cao), (m, cao * 0.5), (m + 26, 0)], vang),
          ("goi", _tron((gx, gy), 70), sam)]
    return ra


def _long(p0, a, l, w):
    """một chiếc lông kim loại: gốc hẹp, thân rộng đều, mũi tròn vát (đơn vị rig)."""
    d = np.array([math.cos(a), math.sin(a)])
    n = np.array([-d[1], d[0]])
    p0 = np.array(p0, float)
    pts = [p0 + n * w * 0.30, p0 + d * l * 0.18 + n * w * 0.5, p0 + d * l * 0.80 + n * w * 0.5, p0 + d * l * 0.96 + n * w * 0.25,
           p0 + d * l, p0 + d * l * 0.90 - n * w * 0.5, p0 + d * l * 0.18 - n * w * 0.5, p0 - n * w * 0.30]
    return [tuple(p) for p in pts]


def canh_luoi(c):
    """một cánh như cánh chim (đơn vị rig): tay cánh đi từ gốc ra tới cổ cánh; các lông kim loại chồng mép nhau treo dọc tay cánh,
    lông ngoài cùng dài nhất chĩa gần theo tay cánh, lông vào trong ngắn dần và chúc dần xuống. Trả [(đa giác, màu)] vẽ sau → trước."""
    gx, gy = c["goc"]
    a0, L, q, n = math.radians(c["huong"]), c["dai"], c["quat"], c["luoi"]
    d = np.array([math.cos(a0), math.sin(a0)])
    G0 = np.array([gx, gy], float)
    co = G0 + d * L * 0.55  # cổ cánh
    ra = []
    for k in range(n):
        t = k / max(1, n - 1)  # 0 = lông ngoài cùng, 1 = trong cùng
        diem = co + (G0 - co) * (t * 0.8)
        a = a0 + q * math.radians(8 + 104 * t)
        l = L * (0.78 - 0.40 * t)
        ra.append((_long(diem, a, l, L * 0.15), (214, 219, 226)))
    ra.reverse()  # lông trong cùng vẽ trước, lông ngoài cùng trên cùng
    ra.append((_doan(G0, co, L * 0.12, L * 0.085), (170, 176, 186)))
    ra.append((_tron(co, L * 0.06), (150, 156, 168)))
    ra.append((_tron(G0, L * 0.085), (120, 160, 220)))
    return ra


def bo_cuc():
    imgs, atts = _atts()
    P = [np.array(a["xy"], float).reshape(-1, 2) + [0, DY] for a in atts if a["slot"] not in BO]
    for c in CHAN.values():
        P.append(np.array([(c["ban"][0], 0), (c["ban"][1] + 20, 0), c["hong"]], float))
    for c in CANH.values():
        for poly, _ in canh_luoi(c):
            P.append(np.array(poly, float))
    P = np.concatenate(P)
    s, cx, cy, T = _khung(P, 900.0, 1380.0)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))

    def ve(polys, nen=None):
        lay = Image.new("RGBA", can.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for poly, mau in polys:
            pts = [tuple(p) for p in (T(np.array(poly, float)) * S)]
            d.polygon(pts, fill=mau + (255,), outline=MUC + (255,))
            d.line(pts + [pts[0]], fill=MUC + (255,), width=int(7 * S * s / 0.75 * 0.5) or 6, joint="curve")
        can.alpha_composite(lay)

    # 1. bốn cánh (sau mọi thứ)
    for k in THU_TU_CANH:
        ve(canh_luoi(CANH[k]))
    # 2. chân xa (sau thân)
    ve([(p, m) for _, p, m in chan_hinh(CHAN["xa"])])
    # 3. thân con gốc nâng lên (đúng thứ tự vẽ của họ), chân gần chen sau khối hông (thứ tự 29) như chân xích gần của họ
    truoc = [a for a in atts if a["order"] <= 29 or str(a["order"]) <= "29"]
    i_hong = next(i for i, a in enumerate(atts) if a["slot"] == "xiabanshen_02")
    hop = _ve_parts(can, atts[:i_hong + 1], T, S, DY, BO)
    ve([(p, m) for _, p, m in chan_hinh(CHAN["gan"])])
    hop.update(_ve_parts(can, atts[i_hong + 1:], T, S, DY, BO))
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "bo_cuc.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, DY=DY, chan=CHAN, canh=CANH, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")


GUI = os.path.join(HERE, "gui_gpt", "vua_may_1")
ROBOT_CO = os.path.join(HERE, "inbox", "robot_co_1", "tai_ve", "L1_duyet.png")  # robot cổ (tướng 7 đảo Kim)
VONG_KY = os.path.join(HERE, "inbox", "ky_nguyen_1", "tai_ve", "L1_duyet.png")  # Vong Kỵ (tướng 8 đảo Kim)
MUC_HEX = "#2B2118"


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def prompt_concept():
    from vua_may_huong import MO_TA_CON, HUONG, STYLE_ANH1, R_VI, R_ROBOT, R_VUA, TASK, DETAIL, MOOD
    style = (f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly "
             f"dark-brown INK outline ({MUC_HEX}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink "
             "lines (about 4 px) for the inner lines (plate edges, trims, engravings, feather quills, fingers), and every area filled with "
             f"ONE flat colour with visible coloured-pencil / wax-crayon hatching. {STYLE_ANH1}: no shading, no highlights, no white shine "
             "streaks, no gradients, no glow, no shadows, no gloss, no sparkles: flat colour only. A different tone appears only where a "
             "different face (front face / side face) or material is listed.")
    mau = os.path.join(G.MAU, "bo_cuc.png")
    R = [(mau,) + R_VI, (ROBOT_CO,) + R_ROBOT, (VONG_KY,) + R_VUA]
    hd = ["# Gói GPT: vua robot (vua_may), tướng 10 / final boss đảo Kim", "",
          "Con gốc của rig: `monster_3637` (vua robot vàng ngồi trên bệ hai chân xích; game tham khảo). Ảnh mẫu 1 dựng từ hình con gốc: chỉ "
          "dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept, ba hướng (2026-11-17)", "",
          "Người dùng: \"concept vua robot như hình nhưng làm thêm nhiều chi tiết hơn nữa, đổi chân máy thành chân robot đi lại, thêm 4 cánh "
          "máy móc robot ở sau lưng lơ lửng\"; \"có thể làm thành cánh thiên thần lông vũ cũng được, cánh màu đen hoặc trắng\". Ba file, mỗi "
          "file một hướng; giữ dáng và chỗ, cỡ từng mảnh thân của con gốc (để lắp lên đúng xương của họ), thân nâng lên 150 đơn vị cho có chỗ "
          "hai chân robot; chân và bốn cánh là mảnh mới, đặt đúng chỗ khối giữ chỗ trên ảnh 1.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["", TASK, "", MO_TA_CON, "", "CHANGE:"] + [f"- {d}" for d in doi] + ["", DETAIL, "", style, "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1 (wings included, nothing cut by the frame). No sparkles, no glints, no dust, no glow, no aura "
              "round the character, no smoke, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}): {vi2}. Chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng (quay phải, đứng hai chân robot chạm đất, bốn cánh lơ lửng SAU lưng có khe hở với thân), đúng chỗ và cỡ từng mảnh "
           "thân như ảnh 1 (chồng lên phải trùng, trừ vương miện, mặt, râu đổi dáng); quyền trượng dựng đứng chạm đất, đầu bánh răng + hai "
           "vòng lơ lửng trên ngọc; bánh răng phối cảnh ở khuỷu và eo; nhiều chi tiết hơn con gốc nhưng vẫn tô phẳng: nét bút mực rung, vân "
           "sáp, không bóng, không quầng sáng; mắt có chấm trắng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the shading / highlights / glow, flat colour only\"; \"keep every body piece at the same place and size "
           "as in image 1\"; \"the four wings must float behind the back with a clear gap, not attached\"; \"both feet flat on the ground\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        ca_con()
    elif cmd == "bo_cuc":
        bo_cuc()
    elif cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)


def _mat_na(p):
    """mặt nạ hình (khác nền trắng), lấp kín lỗ."""
    import cv2
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H)), np.int16)
    m = ((255 - a).max(2) > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k.astype(bool)


def so_bo_cuc(ks="ABC"):
    """chồng viền hình bóng sơ đồ bố cục (đỏ) lên từng concept, in IoU cả hình → mau/_so_bo_cuc.png."""
    import cv2
    g = _mat_na(os.path.join(G.MAU, "bo_cuc.png"))
    cs, _ = cv2.findContours(g.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    o = []
    for k in ks:
        p = os.path.join(G.TAI, f"L1_{k}.png")
        if not os.path.exists(p):
            continue
        m = _mat_na(p)
        iou = (m & g).sum() / max(1, (m | g).sum())
        im = np.asarray(Image.open(p).convert("RGB").resize((W, H))).copy()
        cv2.drawContours(im, cs, -1, (230, 30, 30), 3)
        cv2.putText(im, f"{k}  IoU {iou:.3f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (230, 30, 30), 4)
        o.append(Image.fromarray(im).resize((W // 2, H // 2), Image.LANCZOS))
        print(k, f"IoU {iou:.3f}")
    if o:
        c = Image.new("RGB", (W // 2 * len(o), H // 2), "white")
        for i, im in enumerate(o):
            c.paste(im, (i * W // 2, 0))
        c.save(os.path.join(G.MAU, "_so_bo_cuc.png"))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "so_bo_cuc":
    so_bo_cuc(*(sys.argv[2:3] or ["ABC"]))


# ---------------------------------------------------------------- lượt 2: cánh hoàng gia nhiều tầng + vòng hoa văn sau lưng
# Người dùng 2026-11-17 (xem ba concept lượt 1, chưa chọn): "cánh nhìn chưa epic, nhiều lớp hơn, hoàng gia hơn, làm thêm 1 vòng tròn hoa văn
# ánh sáng đằng sau nữa". Sửa trên từng bản lượt 1 (giữ nguyên thân), chỉ đổi bốn cánh và thêm vòng.
CANH2 = {
    "A": ("cánh máy: tầng lông phủ men xanh hoàng gia, tầng giữa + tầng ngoài thép trắng viền vàng, tay cánh vàng chạm hoa văn; vòng mặt trời "
          "vàng nhạt răng bánh răng",
          "four floating MECHANICAL wings of royal splendour: the WING ARM becomes a thick ornate GOLD frame with engraved scrollwork, rivets, a "
          "round blue jewel at the wrist and a bigger blue jewel in a gold sun-rosette at the root; THREE overlapping tiers of separate metal "
          "feather plates hang from it: an inner tier of short rounded COVERT plates in royal blue enamel #2F5FC4 with gold rims, a middle "
          "tier of medium plates in white steel #E4E8EE with gold rims, and an outer tier of very long pointed PRIMARY plates in white steel "
          "with a gold rim and a gold tip, each with one engraved line",
          "a big flat ROYAL SUN HALO: an outer ring with gear teeth all round, a band of small engraved sun rays, an inner ring of round blue "
          "jewels and a thin inner circle, in pale gold #F3D98A and cream #FFF4D2 with a few royal blue #3E8EE8 jewels"),
    "B": ("cánh lông vũ trắng: ba tầng lông (phủ nhỏ, giữa, lông dài ngọn vàng), tay cánh bạc chạm vàng; vòng hào quang trắng ngà hoa văn "
          "nguyệt quế",
          "four floating ANGEL wings of royal splendour: the WING ARM becomes an ornate SILVER frame with gold filigree and a pearl at the wrist "
          "and at the root; THREE overlapping tiers of real soft WHITE feathers #F7F7F4 hang from it: an inner tier of small rounded COVERT "
          "feathers with gold edges, a middle tier of medium feathers, and an outer tier of very long PRIMARY feathers with pale gold tips "
          "#EBD9A0, each feather with one simple quill line",
          "a big flat ROYAL HALO: an outer ring of small laurel leaves, a band of short straight light rays, an inner ring of pearls and a "
          "thin inner circle, in pale gold #F1DC9C and ivory #FFF8E6"),
    "C": ("cánh lông vũ đen: ba tầng lông (phủ tím mận viền vàng, giữa đen, lông dài đen ngọn vàng), tay cánh vàng đen ngọc đỏ; vòng hào quang "
          "vàng nhạt + tím, răng nhọn, ngọc đỏ",
          "four floating BLACK wings of royal splendour: the WING ARM becomes an ornate black-and-gold frame with engraved scrollwork and a "
          "round red jewel at the wrist and a bigger red jewel in a gold rosette at the root; THREE overlapping tiers of soft feathers hang "
          "from it: an inner tier of small rounded COVERT feathers in dark plum #4A2E5C with gold edges, a middle tier of medium black "
          "feathers #2A2B33, and an outer tier of very long black PRIMARY feathers with a thin gold tip #D7A848, each with one quill line",
          "a big flat ROYAL HALO: an outer ring of short sharp pointed spikes, a band of engraved rays, an inner ring of round red jewels and a "
          "thin inner circle, in pale gold #EED48A and soft violet #B9A3E0 with a few red #D8343A jewels"),
}


def prompt_canh2():
    from vua_may_huong import R_ROBOT
    hd = ["", "## Lượt 2: cánh hoàng gia nhiều tầng + vòng hoa văn sau lưng (2026-11-17)", "",
          "Người dùng: \"cánh nhìn chưa epic, nhiều lớp hơn, hoàng gia hơn, làm thêm 1 vòng tròn hoa văn ánh sáng đằng sau nữa\" (chưa chọn "
          "A/B/C). Mỗi file sửa trên bản lượt 1 cùng chữ cái (ảnh mẫu 1): giữ nguyên thân, chỉ đổi bốn cánh (ba tầng lông, tay cánh chạm hoa "
          "văn, ngọc), thêm vòng hào quang hoa văn sau lưng tô phẳng màu sáng (không quầng sáng, theo luật nét của game).", ""]
    for k, (vi, canh, vong) in CANH2.items():
        mau = os.path.join(G.TAI, f"L1_{k}.png")
        out, save = luu(f"L2_{k}")
        p = os.path.join(GUI, f"luot_2_canh_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(mau)}: OUR approved draft of the robot king (our own character), 1536x1024, white background. Redraw THIS "
             "picture.",
             f"image 2 = {Wp(ROBOT_CO)}: {R_ROBOT[0]}", ""] + save + ["",
             "TASK: EDIT image 1. Keep the robot king EXACTLY as he is and change only the four wings, and add a halo behind him.", "",
             "KEEP IDENTICAL (same place, same size, same shapes, same colours, same line style as image 1; if the new picture were laid over "
             "image 1, everything listed here must match): the crown, the face, the eyes, the beard, the nose, the body armour, the chest "
             "grille, the shoulders, the cape, the sash, both arms and hands, the scepter with its orb, its floating gear head and the two "
             "rings, the hip, both legs and feet, the pose, the white background.", "",
             "CHANGE:",
             f"- WINGS: {canh}. The wings are BIGGER and grander than in image 1 (about 15 % longer), with the same four places and directions "
             "as in image 1 (two big upper wings rising up and outward like a V behind the crown, two smaller lower wings spreading sideways), "
             "still FLOATING behind the back with a small clear gap between the back and each wing root, all four BEHIND the body. Every "
             "feather / plate is a separate piece with its own ink outline; the tiers overlap neatly like a real bird wing (coverts over the "
             "middle tier, middle tier over the long primaries).",
             f"- HALO (new): behind everything (behind the wings and the body), centred behind the upper back and the head, {vong}. It is a "
             "flat ornate ring, about as wide as the span between the two shoulders plus a half, its centre behind the neck; drawn like "
             "everything else: ink outlines, flat colour, crayon texture. It shows the idea of light only by its pale colours and its ray "
             "shapes: NO glow, NO soft halo, NO gradient, NO light beams, NO sparkles.", "",
             f"DRAWING STYLE: exactly the style of image 1 (wobbly dark-brown ink outline {MUC_HEX}, flat colours with crayon hatching, no "
             "shading, no highlights, no glow, no gradients, no shadows).", "",
             "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), the character at the same place and size as in image 1, wings "
             "and halo fully inside the frame. No ground line, no cast shadow, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **{k}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    ph = os.path.join(GUI, "HUONG_DAN.md")
    old = open(ph, encoding="utf-8").read()
    if "## Lượt 2" not in old:
        open(ph, "a", encoding="utf-8", newline="\n").write("\n".join(hd) + "\n")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "canh2":
    prompt_canh2()


# ---------------------------------------------------------------- lượt 3: giảm chi tiết thân + quyền trượng hệ mặt trời
# Người dùng 2026-11-17 (xem lượt 2, chưa chọn): "nhìn ổn nhưng làm ít hoa văn và giảm bớt chi tiết trên người tướng lại, ngoài ra đổi các
# miếng bánh răng trên quyền trượng thành hình các hành tinh như mặt trời (là cục gắn với quyền trượng), sao hỏa, trái đất, sao thủy".
# Ba mảnh lơ lửng của họ (fazhang_05 bánh răng to, fazhang_04 / fazhang_03 hai vòng) → Trái Đất / Sao Hỏa / Sao Thủy; ngọc fazhang_06 → Mặt Trời.
MAU_L3 = {
    "A": "vàng + men trắng, cánh máy xanh trắng, vòng mặt trời",
    "B": "vàng + bạc, cánh lông trắng, vòng nguyệt quế",
    "C": "thép đen + vàng, cánh lông đen tím, vòng răng nhọn",
}


def prompt_l3():
    from vua_may_huong import R_ROBOT
    hd = ["", "## Lượt 3: giảm chi tiết thân + quyền trượng hệ mặt trời (2026-11-17)", "",
          "Người dùng: \"nhìn ổn nhưng làm ít hoa văn và giảm bớt chi tiết trên người tướng lại, ngoài ra đổi các miếng bánh răng trên quyền "
          "trượng thành hình các hành tinh như mặt trời (là cục gắn với quyền trượng), sao hỏa, trái đất, sao thủy\". Sửa trên bản lượt 2 cùng "
          "chữ cái: thân bớt đinh tán, bỏ hình khắc, mảng lớn trơn; cánh, vòng giữ cấu trúc, bớt hoa văn; ngọc đầu trượng → Mặt Trời, bánh răng "
          "lơ lửng → Trái Đất, hai vòng → Sao Hỏa, Sao Thủy.", ""]
    for k, vi in MAU_L3.items():
        mau = os.path.join(G.TAI, f"L2_{k}.png")
        out, save = luu(f"L3_{k}")
        p = os.path.join(GUI, f"luot_3_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(mau)}: OUR approved draft of the robot king (our own character) with four wings and a halo, 1536x1024, white "
             "background. Redraw THIS picture.",
             f"image 2 = {Wp(ROBOT_CO)}: {R_ROBOT[0]} Look at how CLEAN and SIMPLE its metal surfaces are.", ""] + save + ["",
             "TASK: EDIT image 1: make the robot king SIMPLER and CLEANER, and turn the scepter head into a little SOLAR SYSTEM. Everything else "
             "stays as in image 1.", "",
             "KEEP IDENTICAL (same place, same size, same silhouette, same colours as image 1): the pose, the crown, the face (eyes, beard, "
             "nose), the outline of every armour piece, the cape, the sash, the arms and hands, the hip, the legs and feet, the scepter shaft "
             "and its tower-shaped top, the four wings (same places, sizes, colours and the same three tiers of feathers), the halo behind (same "
             "place, size and colours), the white background.", "",
             "CHANGE 1, FEWER DETAILS ON THE BODY (very important): the armour becomes big CLEAN flat areas of colour: remove almost all rivets "
             "(at most 2 or 3 small rivets on a big piece, none on small pieces), remove the engraved sun and gear emblems on the shoulders, "
             "forearms, chest and legs, remove extra plate lines and trims (keep only ONE simple trim along the rim of each big armour piece); "
             "the cape keeps its border and only 2 or 3 big simple gear shapes; the sash keeps its one emblem; the leg joints are simple round "
             "joints. The wings keep their three tiers but the wing arms lose their scrollwork (a plain frame with one jewel at the wrist and "
             "one at the root); the halo keeps its shape but with fewer small patterns (about half).",
             "CHANGE 2, THE SCEPTER HEAD BECOMES THE SOLAR SYSTEM: (a) the round orb fixed on top of the scepter's tower top becomes the SUN: a "
             "slightly bigger ball, flat warm yellow #FFC93C with an orange #FF9A3D ring of short wavy flame points all round its edge (flat "
             "shapes, no glow); (b) the big floating gear above it becomes the EARTH: a round planet, the biggest of the three floating ones, "
             "flat ocean blue #3E8EE8 with a few simple flat green #5BB55A continents and one or two small white cloud shapes; (c) the upper "
             "floating ring becomes MARS: a smaller round planet, flat rusty red #D2553A with two or three darker #A33A28 round craters; (d) "
             "the lower floating ring becomes MERCURY: the smallest round planet, flat grey #A7A3A0 with a few darker grey #7F7B78 small "
             "craters. The three planets float in the same places as the gear and the two rings in image 1, near each other above and around "
             "the Sun, each with its own ink outline; no orbit lines, no stars, no glow.", "",
             f"DRAWING STYLE: exactly the style of image 1 (wobbly dark-brown ink outline {MUC_HEX}, flat colours with crayon hatching, no "
             "shading, no highlights, no glow, no gradients, no shadows).", "",
             "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), the character at the same place and size as in image 1, wings and "
             "halo fully inside the frame. No ground line, no cast shadow, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **{k}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    ph = os.path.join(GUI, "HUONG_DAN.md")
    if "## Lượt 3" not in open(ph, encoding="utf-8").read():
        open(ph, "a", encoding="utf-8", newline="\n").write("\n".join(hd) + "\n")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "l3":
    prompt_l3()
