# -*- coding: utf-8 -*-
"""Chim lá DẠNG 1 (chim non, hướng A "kem" người dùng chọn 2026-11-12): CHUYỂN DA từ dạng lớn trên cùng rig monster_3630
(skill pokiclash-spine-rig mục 00 "DẠNG KHÁC trên CÙNG rig gốc"). Rig: CL_DANG=non chim_la_rig.py.

- doi_mau: mọi ảnh part ĐÃ XONG của dạng lớn (inbox/chim_la_1/manh/part) → màu chim non, giữ nguyên hình bóng, nét mực, vân sáp
  (mỗi điểm cộng độ lệch màu của lớp màu gần nó nhất, pha mềm giữa các lớp; mực, trắng, hồng giữ nguyên) → inbox/chim_la_non/manh/part.
- to_dau: tờ hướng dẫn riêng cho cái ĐẦU mới (mắt to tròn, mũ lục nhạt) đúng khung part + ô nụ hoa → prompt luot_2_dau.txt.
- cat_dau: cắt tờ N_dau*.png → P_tou_01.png, nu.png.

    chim_la_non.py doi_mau | to_dau | cat_dau
"""
import glob
import json
import os
import re
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chim_la as CL  # noqa: E402
import chim_la_manh as M  # noqa: E402

LON = os.path.join(HERE, "inbox", "chim_la_1", "manh", "part")
BASE = os.path.join(HERE, "inbox", "chim_la_non")
RA = os.path.join(BASE, "manh", "part")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
PK = os.path.join(HERE, "gui_gpt", "chim_la_non")
W, H = 1536, 1024
INK = CL.INK
h = CL._h
# lớp màu dạng lớn → màu chim non (hướng A); None = giữ nguyên
DOI = [(h("#F4EFDC"), h("#F7EFCB")), (h("#7E9E7A"), h("#A8C690")), (h("#4C9A52"), h("#7FC25A")), (h("#93C663"), h("#B8DC72")),
       (h("#2A6A3A"), h("#3C8C46")), (h("#2F7646"), h("#4FA052")), (h("#1F5634"), h("#34783E")), (h("#7A5638"), h("#9A6E48")),
       (h("#9A968A"), h("#A8A498")), (h("#66625A"), h("#8A867C")), (h("#6FAE4B"), h("#7FBE58")), (h("#EE8A3E"), h("#F2A04A")),
       (h("#4A3A30"), h("#6A4A36")), (INK, None), ((255, 255, 255), None), (h("#F2A6BC"), None), (h("#EE86A6"), None)]
PAL = dict(long=h("#F7EFCB"), sage=h("#A8C690"), cam=h("#F2A04A"), nu=h("#F2A6BC"), nu_dam=h("#E07C9C"), la_nhat=h("#B8DC72"),
           canh=h("#9A6E48"), trang=(255, 255, 255))


def doi_mau_anh(im):
    A = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb = A[..., :3]
    C = np.array([c for c, _ in DOI], np.float32)
    D = np.array([(np.array(n, np.float32) - np.array(c, np.float32)) if n is not None else np.zeros(3, np.float32) for c, n in DOI])
    d2 = ((rgb[..., None, :] - C[None, None]) ** 2).sum(-1)                  # (h, w, số lớp)
    w = np.exp(-(d2 - d2.min(-1, keepdims=True)) / (2 * 26.0 ** 2))
    w /= w.sum(-1, keepdims=True)
    out = np.clip(rgb + (w[..., None] * D[None, None]).sum(-2), 0, 255)
    return Image.fromarray(np.dstack([out, A[..., 3:]]).astype(np.uint8), "RGBA")


def doi_mau():
    os.makedirs(RA, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(os.path.join(LON, "*.png"))):
        ten = os.path.basename(f)
        if ten in ("P_tou_01.png",):               # đầu gen mới (cat_dau); chưa có thì tạm dùng bản đổi màu
            if os.path.exists(os.path.join(RA, ten)) and os.path.exists(os.path.join(RA, "_dau_moi")):
                continue
        doi_mau_anh(Image.open(f)).save(os.path.join(RA, ten))
        n += 1
    for f in ("_z.json", "_iou.json"):
        if os.path.exists(os.path.join(LON, f)):
            shutil.copy(os.path.join(LON, f), os.path.join(RA, f))
    print(RA, n, "ảnh đã đổi màu")


# ---------------------------------------------------------------- đầu mới + nụ hoa
Z_DAU = 5.0
NU = (170, 210)


def o_dau():
    """đầu chim non trong đúng khung part P_tou_01 × Z_DAU: mũ lục nhạt, mặt kem, MẮT TO TRÒN, nét mày ngắn quả quyết."""
    z = Z_DAU
    m = M.bong("P_tou_01", z)
    hh, ww = m.shape
    im = np.full((hh, ww, 3), 255, np.uint8)
    im[m] = PAL["sage"]
    MA_UV = [(0.64, 0.46), (0.74, 0.26), (0.90, 0.20), (1.0, 0.36), (1.0, 0.82), (0.80, 0.84), (0.72, 1.0), (0.40, 1.0), (0.44, 0.76), (0.56, 0.64)]
    mk = np.zeros((hh, ww), np.uint8)
    cv2.fillPoly(mk, [np.int32([(u * ww, v * hh) for u, v in MA_UV])], 1)
    im[m & mk.astype(bool)] = PAL["long"]
    a = M.by()["P_tou_01"]
    e = M.by()["P_yanjing_01"]
    pe = M.uv_cua(a, np.array(e["xy"], float).reshape(-1, 2).mean(0)) * np.array([ww, hh])
    cx, cy = int(pe[0] - 1.0 * z), int(pe[1] + 0.6 * z)
    r = int(8.6 * z)
    cv2.circle(im, (cx, cy), r, PAL["cam"], -1, cv2.LINE_AA)
    cv2.circle(im, (cx, cy), r, INK, max(2, int(1.4 * z)), cv2.LINE_AA)
    cv2.circle(im, (cx + int(0.8 * z), cy + int(0.3 * z)), int(4.9 * z), INK, -1, cv2.LINE_AA)
    cv2.circle(im, (cx - int(0.8 * z), cy - int(2.0 * z)), max(2, int(1.3 * z)), PAL["trang"], -1, cv2.LINE_AA)
    cv2.line(im, (cx - int(8.5 * z), cy - int(12.5 * z)), (cx + int(7.5 * z), cy - int(8.6 * z)), INK, max(3, int(2.4 * z)), cv2.LINE_AA)
    vien = 8.0 * M.a_tl() * z
    im[m & ~cv2.erode(m.astype(np.uint8), CL.el(vien)).astype(bool)] = INK
    im[~m] = 255
    return im, m, (cx, cy, r)


def o_nu():
    w, hh = NU
    im = np.full((hh, w, 3), 255, np.uint8)
    cx = w // 2
    # nụ: giọt nước nhọn đầu, hai lá đài ở gốc
    P = np.array([(cx, 16), (cx + 46, 92), (cx + 34, 150), (cx, 172), (cx - 34, 150), (cx - 46, 92)], np.int32)
    hull = cv2.convexHull(P)
    mk = np.zeros((hh, w), np.uint8)
    cv2.fillPoly(mk, [hull], 1)
    mk = cv2.GaussianBlur(mk * 255, (0, 0), 9) > 110
    im[mk] = PAL["nu"]
    im[mk & ~cv2.erode(mk.astype(np.uint8), CL.el(8)).astype(bool)] = INK
    for sg in (-1, 1):
        Q = np.array([(cx, 196), (cx + sg * 40, 150), (cx + sg * 30, 112), (cx + sg * 6, 150)], np.int32)
        cv2.fillPoly(im, [Q], PAL["la_nhat"], cv2.LINE_AA)
        cv2.polylines(im, [Q], True, INK, 7, cv2.LINE_AA)
    return im, im.min(axis=2) < 236


def to_dau():
    os.makedirs(MAU, exist_ok=True)
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    im = np.full((H, W, 3), 255, np.uint8)
    dau, m, mat = o_dau()
    hh, ww = m.shape
    x0, y0 = 60, 60
    im[y0:y0 + hh, x0:x0 + ww] = dau
    nu, _ = o_nu()
    nx, ny = x0 + ww + 120, 100
    im[ny:ny + NU[1], nx:nx + NU[0]] = nu
    Image.fromarray(im).save(os.path.join(MAU, "part_dau.png"))
    json.dump({"P_tou_01": {"x": x0, "y": y0, "w": ww, "h": hh, "z": Z_DAU}, "nu": {"x": nx, "y": ny, "w": NU[0], "h": NU[1], "z": 1.0},
               "mat": [x0 + mat[0], y0 + mat[1], mat[2]]}, open(os.path.join(MAU, "part_dau.json"), "w"), indent=1)
    duyet = os.path.join(TAI, "L1_duyet.png")
    gd = os.path.join(MAU, "part_dau.png")
    out = os.path.join(TAI, "N_dau.png")
    p = os.path.join(PK, "luot_2_dau.txt")
    N = os.path.normpath
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {N(duyet)}: the APPROVED young creature, 1536x1024, white background: a plump cream-coloured fledgling forest bird "
         "with a light sage-green feather hood, a big round orange eye with a determined little frown, a short orange beak, two leaves "
         "standing in a V on its head, small wings made of leaves with thin brown branches carrying pink buds. It gives the design of "
         "the head, the colours, the wobbly dark-brown ink line and the crayon hatching.",
         f"image 2 = {N(gd)}: PART GUIDE, 1536x1024, white background, drawn by computer: two separate flat shapes with dark outlines: "
         "the big one is the bird's HEAD alone (no beak, no crest leaves), the small one at the right is a flower BUD. It gives the "
         "exact silhouette, size, orientation and place of each shape.",
         "", f"SAVE: save it as a PNG to {N(out)}",
         "If a file with that name already exists, save as N_dau_2.png, N_dau_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY the "
         "silhouette of both shapes: the same outline, the same size, the same orientation, the same place on the sheet (if your "
         "picture were laid over image 2, the shapes must coincide). A program will cut each shape out of its place and wrap it onto an "
         "animation mesh, so do not move, rotate, mirror or resize them, and draw nothing else. Exactly 2 shapes.", "",
         f"- THE HEAD (centre at about x = {x0 + ww // 2}, y = {y0 + hh // 2}; {ww} x {hh} px): the fledgling's head in profile, facing "
         "RIGHT, drawn WITHOUT its beak and WITHOUT the two crest leaves (separate parts). The back of the head (the left end) breaks "
         "into three or four soft pointed feather tufts. A light sage-green HOOD (#A8C690) covers the crown and the back of the head; "
         "the FACE (front, cheek and throat) is soft cream (#F7EFCB); the border between them is a soft zigzag feather edge drawn as a "
         f"thin ink line. ONE eye exactly where image 2 has it (centre at about x = {x0 + mat[0]}, y = {y0 + mat[1]}, about "
         f"{2 * mat[2]} px wide): BIG and ROUND, soft-orange iris (#F2A04A), a big round dark pupil, one tiny white dot, a clean ink "
         "rim; above it a SHORT dark brow stroke slanting down toward the front (right): a determined little frown, brave, not angry "
         "and not sad. The right end of the head, where the beak will be attached, is plain rounded cream. Same face as on image 1.",
         f"- THE BUD (centre at about x = {nx + NU[0] // 2}, y = {ny + NU[1] // 2}; {NU[0]} x {NU[1]} px): one closed flower bud, pointed "
         "at the top, soft pink (#F2A6BC) with one or two thin darker-pink petal lines, held at its base by two tiny light-green "
         "(#B8DC72) sepals.", "",
         "OUTLINE: each shape has its own CLOSED dark-brown ink outline (#2B2118) all the way around, lying just INSIDE the edge of the "
         "silhouette of image 2, about 20 px thick on the head and about 8 px on the bud, slightly wobbly like a real pen. Inner detail "
         "lines (feather lines) are thin darker pencil lines, not ink.",
         "COLOUR: flat colours as listed; coloured pencil and wax crayon, the strokes visible as loose diagonal hatching inside the "
         "outline, as on image 1.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
         "highlights (except the one tiny dot in the eye), no gradients, no cast shadows, no glow. Pure white (#FFFFFF) background "
         "between the shapes; no text, no labels, no frames."]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    hd = os.path.join(PK, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n") if os.path.exists(hd) else ""
    them = ["", "## Lượt 2: đầu mới + nụ hoa (hướng A đã duyệt 2026-11-12)", "",
            "Mọi mảnh khác của dạng 1 là ảnh mảnh dạng lớn ĐỔI MÀU bằng mã (`py -3 -I ArtGen/Spine/chim_la_non.py doi_mau`); chỉ cái đầu "
            "(mắt to tròn) và nụ hoa phải vẽ mới.", "",
            f"**Chỉ gửi GPT đường dẫn:** `{N(p)}`. Ảnh lưu vào `{N(out)}` (trùng tên thì `_2`, `_3`…).", "",
            "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
            f"| 1 | `{N(duyet)}` | Concept chim non đã duyệt (1536 × 1024, nền trắng): chim non lông kem, mũ lục nhạt, mắt cam to tròn, mào "
            "hai lá chữ V. Lấy thiết kế cái đầu, màu, nét, vân sáp |",
            f"| 2 | `{N(gd)}` | Tờ hướng dẫn (1536 × 1024, nền trắng): hình phẳng cái đầu (không mỏ, không mào) viền sẫm, mắt tròn cam vẽ "
            "sẵn đúng chỗ; bên phải một nụ hoa hồng nhỏ |", "",
            "Kiểm: hình bóng đầu trùng tờ hướng dẫn, một mắt to tròn đúng chỗ có nét mày, mũ lục nhạt + mặt kem, viền kín; nụ hồng có hai lá "
            "đài; nền trắng. Claude cắt bằng `py -3 -I ArtGen/Spine/chim_la_non.py cat_dau`."]
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(them) + "\n")
    print(gd)
    print(p)


def cat_dau():
    from quai import anh
    fs = [f for f in glob.glob(os.path.join(TAI, "N_dau*.png")) if re.fullmatch(r"N_dau(_\d+)?\.png", os.path.basename(f))]
    if not fs:
        raise SystemExit("chưa có N_dau.png")
    path = max(fs, key=os.path.getmtime)
    K = json.load(open(os.path.join(MAU, "part_dau.json")))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, "_N_dau_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=120, gop_px=10)
    gd = np.asarray(Image.open(os.path.join(MAU, "part_dau.png")).convert("RGB"))
    os.makedirs(RA, exist_ok=True)
    for ten in ("P_tou_01", "nu"):
        kv = K[ten]
        x, y, w, hh, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + hh, x:x + w].min(axis=2) < 236
        d = 14 if ten == "nu" else 0
        x0, y0, x1, y1 = max(0, x - d), max(0, y - d), min(W, x + w + d), min(H, y + hh + d)
        cell = tt.rgba[y0:y1, x0:x1].copy()
        lab = tt.lab[y0:y1, x0:x1]
        gg = np.zeros(lab.shape, bool)
        gg[y - y0:y - y0 + hh, x - x0:x - x0 + w] = g
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[gg].ravel().tolist()) - {0}:
            giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & gg).sum() / max(1, (a | gg).sum())
        if ten == "P_tou_01":
            sat = cv2.dilate(g.astype(np.uint8), CL.el(0.75 * z)).astype(bool)
            cell[..., 3][~sat] = 0
            a &= sat
            ho = g & ~a
            if ho.any():
                gc = gd[y:y + hh, x:x + w]
                to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105)
                _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                tra[lb[to_]] = gc[to_]
                cell[ho, :3] = tra[lb][ho]
                cell[ho, 3] = 255
                vanh = g & ~cv2.erode(g.astype(np.uint8), CL.el(3.0 * z)).astype(bool)
                cell[ho & vanh, :3] = INK
            at = M.by()[ten]
            hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, hh])
            hm = np.zeros(a.shape, np.uint8)
            cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
            dai = hm.astype(bool) & ~cv2.erode(hm, CL.el(1.0 * z), borderValue=0).astype(bool)
            cell[dai & (cell[..., 3] > 127), :3] = INK
        Image.fromarray(cell, "RGBA").save(os.path.join(RA, ten + ".png"))
        print(f"  {ten}: {cell.shape[1]} x {cell.shape[0]}, IoU {iou:.2f}")
    pz = os.path.join(RA, "_z.json")
    zs = json.load(open(pz)) if os.path.exists(pz) else {}
    zs["P_tou_01"] = Z_DAU
    json.dump(zs, open(pz, "w"), indent=0)
    json.dump({"mat": [K["mat"][0] - K["P_tou_01"]["x"], K["mat"][1] - K["P_tou_01"]["y"], K["mat"][2]], "w": K["P_tou_01"]["w"]},
              open(os.path.join(RA, "_mat.json"), "w"))
    open(os.path.join(RA, "_dau_moi"), "w").write(os.path.basename(path))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["doi_mau"]:
        doi_mau()
    elif a[:1] == ["to_dau"]:
        to_dau()
    elif a[:1] == ["cat_dau"]:
        cat_dau()
    else:
        print(__doc__)
