# -*- coding: utf-8 -*-
"""Thú giáp pháo (thu_phao, rig monster_3629): concept THEO CON GỐC (thú bốn chân thấp như rùa, quay phải, giáp khối, đuôi cuộn lên lưng
thành khẩu pháo chĩa tới trước trên đầu), đổi đầu, tai, họng pháo, lõi, tay cầm, đốt đuôi và chất liệu, màu (giáp kim loại).

    thu_phao_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/thu_phao_1/mau/goc_ca_con.png (+ .json: khung từng part)
    thu_phao_da.py concept    ba file prompt concept (ba hướng) → gui_gpt/thu_phao_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    thu_phao_da.py so_goc     chồng viền hình bóng con gốc lên từng concept, in IoU → inbox/thu_phao_1/mau/_so_goc.png
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import thu_phao as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "thu_phao_1")
SOI_GIAP = os.path.join(HERE, "inbox", "soi_giap_1", "tai_ve", "L1_duyet.png")
PHAP_LUA = os.path.join(HERE, "inbox", "robot_co_1", "tai_ve", "L1_duyet.png")  # robot cổ (tướng 7 đảo Kim)
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def khung_ca_con(atts, cao=800.0):
    """phép đổi toạ độ rig → ảnh 1536 × 1024: cả con cao ~cao px, đặt giữa khung."""
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024; ghi khung bao từng part trên ảnh."""
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    s, cx, cy, T = khung_ca_con(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    hop = {}
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)
        lay = lay.convert("RGBA")
        al = np.asarray(lay)[..., 3] > 60
        if al.any():
            ys, xs = np.nonzero(al)
            hop[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
        can.alpha_composite(lay)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")
    for k, v in hop.items():
        print(k, v)


from thu_phao_huong import MO_TA_CON, HUONG, STYLE_ANH1, R_VI, R_SOI, R_PHAP, TASK, MOOD  # noqa: E402


STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) for the "
    "few inner lines (plate edges, metal bands, the toes), and every area filled with ONE flat colour with visible coloured-pencil / "
    f"wax-crayon hatching. {STYLE_ANH1}: no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows, no gloss, no "
    "sparkles: flat colour only. A different tone appears only where a different face (front face / side face) or material is listed. "
    "VERY SIMPLE DESIGN, FEW DETAILS: no extra rivets, engravings, scratches, cracks, dents, skulls, badges or patterns beyond what is "
    "listed; the glowing colour ONLY inside the round core, the muzzle and the eyes.")


def prompt_concept():
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau,) + R_VI, (SOI_GIAP,) + R_SOI, (PHAP_LUA,) + R_PHAP]
    hd = ["# Gói GPT: thú giáp pháo (thu_phao), tướng 9 đảo Kim", "",
          "Con gốc của rig: `monster_3629` (thú đá lục bốn chân, pháo khối trên lưng; game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ "
          "dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng (2026-11-17)", "",
          "Người dùng: \"quái thú mặc kín giáp, đuôi là 1 khẩu pháo to\". Ba file, mỗi file một hướng; giữ dáng (bốn chân thấp như rùa, quay "
          "phải, đuôi cuộn lên lưng thành pháo chĩa tới trước trên đầu), chỗ và cỡ từng mảnh của con gốc (để lắp lên đúng xương), đổi dáng "
          "các mảnh nhận diện (đầu, tai, họng pháo, lõi tròn, tay cầm, đốt đuôi) và đổi chất liệu từ đá sang kim loại, đổi màu.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["", TASK, "", MO_TA_CON, "", "CHANGE:"] + [f"- {d}" for d in doi] + ["", STYLE, "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no speed "
              "lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng (bốn chân đứng đất, quay phải, đầu nhỏ thấp ở dưới bên phải, pháo vắt trên lưng, họng pháo ở trên đầu chĩa "
           "phải), đúng chỗ và cỡ từng mảnh như ảnh 1 (chồng lên phải trùng, trừ đầu, tai, họng pháo đổi dáng); bốn đốt đuôi cuộn xuống "
           "ở sau; giáp kim loại, không còn hoa văn xoắn đá; mắt có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng "
           "sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the shading / highlights / glow, flat colour only\"; \"keep every piece at the same place and size as "
           "in image 1\"; \"no stone spirals, metal plates only\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


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


def so_goc(ks="ABC"):
    """chồng viền hình bóng con gốc (đỏ) lên từng concept, in độ khớp IoU → mau/_so_goc.png."""
    import cv2
    g = _mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
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
        c.save(os.path.join(G.MAU, "_so_goc.png"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "so_goc":
        so_goc(*(sys.argv[2:3] or ["ABC"]))
    elif cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)
