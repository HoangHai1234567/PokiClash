# -*- coding: utf-8 -*-
"""Năm tướng đầu đảo Thổ (ải 1, 5, 10, 15, 20) trên rig game tham khảo (kho SwordxStaff), Claude chọn 2026-11-17, người dùng duyệt:
con sau trông chiến hơn con trước. Concept do Claude đề xuất (người dùng: "lên concept reskin đi, animation tôi mô tả sau").
Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

    tho5.py ca_con <mã|all>      hình cả con gốc ở khung 0 idle, nền trắng 1536 × 1024 → inbox/<mã>_1/mau/goc_ca_con.png (+ .json)
    tho5.py slot <mã>            in bảng slot (thứ tự vẽ, ảnh, xương, khung trên ảnh ca_con)
    tho5.py concept <mã|all>     file prompt concept từng hướng → gui_gpt/<mã>_1/luot_1_concept_<k>.txt + HUONG_DAN.md
    tho5.py so_goc <mã>          chồng viền hình bóng con gốc lên từng concept, in IoU → inbox/<mã>_1/mau/_so_goc.png
    tho5.py xem                  trang so cả 5 con (con gốc + các hướng) → inbox/tho5_xem_concept.html
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, HH = 1536, 1024
# mã làm việc → (con gốc, suất, ải)
CON = {
    "cong_da": ("monster_3378", 1, 1),
    "than_lan_cat": ("monster_3257", 2, 5),
    "thu_da": ("monster_3525", 3, 10),
    "rong_cat": ("monster_3424", 4, 15),
    "quy_nui": ("monster_3612", 5, 20),
}


_LUOI_GOC = H.luoi


def luoi_sua(a):
    """như hoa_ho.luoi nhưng KHÔNG đổi rộng / cao với hình region xoay 90° trong atlas: atlas Spine 4 ghi bounds theo cỡ CHƯA xoay và
    to_manh.nap đã gỡ xoay ảnh, nên đổi chỗ w, h làm mảnh bẹp (mắt monster_3257 thành một khe dẹt, 2026-11-17)."""
    if "uv" in a:
        return _LUOI_GOC(a)
    atlas, imgs, _ = H.nap(H._C.get("att"))
    im = imgs[a["region"]]
    r = atlas[a["region"]]
    ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
    w, h = r["bounds"][2], r["bounds"][3]
    return (np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float),
            np.array([[0, 1, 2], [2, 3, 0]]))


def dat(code):
    mon = CON[code][0]
    base = os.path.join(HERE, "inbox", f"{code}_1")
    H.CODE, H.MON, H.BASE = code, mon, base
    H.MAU, H.TAI = os.path.join(base, "mau"), os.path.join(base, "tai_ve")
    H.NHOM = []
    H._C.clear()
    H.luoi = luoi_sua
    return H


def khung_ca_con(atts, cao=800.0):
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, HH / 2 - (V[:, 1] - cy) * s], 1))


def ca_con(code):
    G = dat(code)
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    s, cx, cy, T = khung_ca_con(atts)
    S = 2
    can = Image.new("RGBA", (W * S, HH * S), (255, 255, 255, 255))
    hop = {}
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, HH * S), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)
        lay = lay.convert("RGBA")
        al = np.asarray(lay)[..., 3] > 60
        if al.any():
            ys, xs = np.nonzero(al)
            hop[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
        can.alpha_composite(lay)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, HH), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")


def slot(code):
    G = dat(code)
    _, imgs, atts = G.nap("att_idle0.json")
    D = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    bn = [b["name"] for b in D["bones"]]
    hop = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))["hop"]
    for a in atts:
        print(f'{a["order"]:3d} {a["slot"]:22s} {a["region"]:28s} {G.xuong_bam(a, bn)[:40]:40s} {hop.get(a["slot"])}')


MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def style():
    from tho5_huong import STYLE_ANH1
    return (
        f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown "
        f"INK outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) "
        "for the few inner lines (rock facets, plate edges, toes), and every area filled with ONE flat colour with visible coloured-pencil "
        f"/ wax-crayon hatching. {STYLE_ANH1}: no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows, no "
        "gloss, no sparkles: flat colour only. A different tone appears only where a different face (front face / side face) or material "
        "is listed. VERY SIMPLE DESIGN, FEW DETAILS: no extra cracks, carvings, runes, scratches, spots, pebbles, moss, skulls, badges or "
        "patterns beyond what is listed.")


def prompt_concept(code):
    from tho5_huong import CON as HG, REF
    G = dat(code)
    c = HG[code]
    mon, suat, ai = CON[code]
    gui = os.path.join(HERE, "gui_gpt", f"{code}_1")
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, c["goc_en"], c["goc_vi"])] + [REF[k] for k in c["refs"]]
    hd = [f"# Gói GPT: {c['ten']} (`{code}`), tướng {suat} đảo Thổ (ải {ai})", "",
          f"Con gốc của rig: `{mon}` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, hai hướng (2026-11-17)", "",
          "Người dùng: \"lên concept reskin\" cho năm tướng đầu đảo Thổ (con sau trông chiến hơn con trước). Claude đề xuất hai hướng; giữ "
          "dáng, chỗ và cỡ từng mảnh của con gốc (để lắp lên đúng xương), đổi dáng các mảnh nhận diện, đổi chất liệu và màu sang hệ đất.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in c["huong"].items():
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(gui, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", c["task"], "", c["mo_ta"], "", "CHANGE:"] + [f"- {d}" for d in doi] + ["", style(), "", c["mood"], "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no speed "
              "lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "", f"Kiểm: {c['kiem']}; nét bút mực rung, vân sáp, tô phẳng, "
           "không bóng, không quầng sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the shading / highlights / glow, flat colour only\"; \"keep every piece at the same place and size as "
           "in image 1\"; \"every limb joined to the body, no white gap\"."]
    ghi(os.path.join(gui, "HUONG_DAN.md"), hd)


def prompt_concept2(code):
    """lượt 2 (người dùng trả lượt 1 vì giống con gốc quá): concept tự thiết kế, ảnh 1 chỉ là mẫu dáng → luot_1_concept_<C|D>.txt."""
    from tho5_huong import CON as HG, REF
    from tho5_huong2 import HUONG2, task2, goc2
    G = dat(code)
    c, c2 = HG[code], HUONG2[code]
    mon, suat, ai = CON[code]
    gui = os.path.join(HERE, "gui_gpt", f"{code}_1")
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, goc2(c["goc_en"]), c["goc_vi"].replace("Giữ dáng và từng mảnh, đổi hình", "Chỉ lấy DÁNG và chỗ các chi"))]
    R += [REF[k] for k in c2["refs"]]
    hd = [f"# Gói GPT: {c['ten']} (`{code}`), tướng {suat} đảo Thổ (ải {ai})", "",
          f"Con gốc của rig: `{mon}` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1, hướng C và D: concept tự thiết kế, chỉ gần giống con gốc (2026-11-17)", "",
          "Người dùng trả hai hướng A, B: \"ảnh bạn gen ra bị giống con gốc quá, tự lên concept gần giống thôi\". Ảnh 1 chỉ còn là mẫu dáng và "
          "chỗ các chi (để dùng chung bộ xương); đầu, mặt, mảnh lưng, sừng, diềm, mào là thiết kế mới; thân và chân giữ cỡ gần như cũ.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in c2["huong"].items():
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(gui, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", task2(c2["concept"]), "", c2["plan"], "", "DESIGN:"] + [f"- {d}" for d in doi] + ["", style(), "", c2["mood"], "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no speed "
              "lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: cùng dáng, cùng hướng, cùng chỗ các chi như ảnh 1 nhưng nhìn ra con KHÁC (đầu, mặt, mảnh lưng đổi hẳn); mọi chi dính thân; mắt "
           "có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"it still looks like image 1: change the head and the back pieces more\"; \"remove the shading / highlights / "
           "glow, flat colour only\"; \"every limb joined to the body, no white gap\"."]
    ghi(os.path.join(gui, "HUONG_DAN.md"), hd)


def _mat_na(p):
    """mặt nạ hình (khác nền trắng), lấp kín lỗ (loang nền từ mép)."""
    from PIL import ImageDraw, ImageFilter
    a = np.asarray(Image.open(p).convert("RGB").resize((W, HH)), np.int16)
    m = Image.fromarray((((255 - a).max(2) > 28) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    f = m.copy()
    ImageDraw.floodfill(f, (0, 0), 128)
    return np.asarray(f) != 128


def so_goc(code, ks="AB"):
    from PIL import ImageDraw, ImageFilter, ImageFont
    G = dat(code)
    g = _mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
    gi = Image.fromarray((g * 255).astype(np.uint8))
    vien = np.asarray(gi.filter(ImageFilter.MaxFilter(5))) ^ np.asarray(gi.filter(ImageFilter.MinFilter(3)))
    o = []
    font = ImageFont.truetype("arial.ttf", 56)
    for k in ks:
        p = os.path.join(G.TAI, f"L1_{k}.png")
        if not os.path.exists(p):
            continue
        m = _mat_na(p)
        iou = (m & g).sum() / max(1, (m | g).sum())
        im = np.asarray(Image.open(p).convert("RGB").resize((W, HH))).copy()
        im[vien > 0] = (230, 30, 30)
        im = Image.fromarray(im)
        ImageDraw.Draw(im).text((30, 30), f"{k}  IoU {iou:.3f}", fill=(230, 30, 30), font=font)
        o.append(im.resize((W // 2, HH // 2), Image.LANCZOS))
        print(code, k, f"IoU {iou:.3f}")
    if o:
        c = Image.new("RGB", (W // 2 * len(o), HH // 2), "white")
        for i, im in enumerate(o):
            c.paste(im, (i * W // 2, 0))
        c.save(os.path.join(G.MAU, "_so_goc.png"))


def xem():
    """trang so cả 5 con: mỗi hàng con gốc + các hướng, dùng đường dẫn tương đối từ inbox/."""
    from tho5_huong import CON as HG
    from tho5_huong2 import HUONG2
    rows = []
    for code, (mon, suat, ai) in CON.items():
        c = HG[code]
        cells = [f'<figure><img src="{code}_1/mau/goc_ca_con.png"><figcaption>Con gốc {mon}</figcaption></figure>']
        for k, (vi, _, _) in HUONG2[code]["huong"].items():
            for f in sorted(os.listdir(os.path.join(HERE, "inbox", f"{code}_1", "tai_ve"))) if os.path.isdir(
                    os.path.join(HERE, "inbox", f"{code}_1", "tai_ve")) else []:
                if f.startswith(f"L1_{k}") and f.endswith(".png"):
                    cells.append(f'<figure><img src="{code}_1/tai_ve/{f}"><figcaption>{f[:-4]}: {vi}</figcaption></figure>')
        rows.append(f"<h2>{suat}. {c['ten']} (ải {ai}, <code>{code}</code>)</h2><div class=r>{''.join(cells)}</div>")
    html = ("<!doctype html><meta charset=utf-8><title>Thổ: concept 5 tướng đầu</title><style>body{font:15px sans-serif;margin:16px;"
            "background:#f4f1ea}h2{margin:22px 0 6px}.r{display:flex;gap:10px;flex-wrap:wrap}figure{margin:0;background:#fff;padding:6px;"
            "border:1px solid #ddd}img{width:440px;display:block}figcaption{padding-top:4px;max-width:440px}</style>"
            "<h1>Đảo Thổ: concept năm tướng đầu (con sau chiến hơn con trước)</h1>" + "".join(rows))
    p = os.path.join(HERE, "inbox", "tho5_xem_concept.html")
    open(p, "w", encoding="utf-8").write(html)
    print(p)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    arg = sys.argv[2] if len(sys.argv) > 2 else "all"
    codes = list(CON) if arg == "all" else [arg]
    if cmd == "ca_con":
        for c in codes:
            ca_con(c)
    elif cmd == "slot":
        for c in codes:
            print("==", c, CON[c][0])
            slot(c)
    elif cmd == "concept":
        for c in codes:
            prompt_concept(c)
    elif cmd == "concept2":
        for c in codes:
            prompt_concept2(c)
    elif cmd == "so_goc":
        for c in codes:
            so_goc(c, sys.argv[3] if len(sys.argv) > 3 else "AB")
    elif cmd == "xem":
        xem()
    else:
        print(__doc__)
