# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt (tinh_sat): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png = L3_1, người dùng chọn 2026-11-15:
mày quả quyết, miệng một răng nanh, tinh thể dài nhọn hơn, má sao bạc). Concept vẽ đúng khung hình cả con gốc ở khung 0 idle (mau/goc_ca_con.json:
tỉ lệ s px / đơn vị, tâm cx, cy), nên mỗi mảnh cắt ra là đặt thẳng vào thế giới rig ở dáng idle 0 rồi gắn lên xương của mảnh cũ.

    tinh_sat_manh.py khung        viền mọi part gốc (khung 0 idle) chồng lên concept → mau/_goc_tren_concept.png (kiểm khớp khung)
    tinh_sat_manh.py prompt       file prompt từng nhóm (mảnh không chồng nhau trên concept) → gui_gpt/tinh_sat_1/luot_3_<nhóm>.txt
    tinh_sat_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → inbox/tinh_sat_1/manh/<slot>.png + manh/dat.json (hộp trên concept)
    tinh_sat_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ trên nền trắng cạnh concept → manh/_ghep.png + IoU hình bóng
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tinh_sat as G  # noqa: E402
import tinh_sat_da as DA  # noqa: E402

W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = DA.GUI
MUC = "#2B2118"

# nhóm gen: các mảnh trong một nhóm KHÔNG chồng nhau trên concept. Mỗi mảnh: (slot, mô tả tiếng Anh, cách vẽ phần khuất)
NHOM = {
    "M1": [("bin2", "the LONG WING CRYSTAL at the left", "its inner (right) end is hidden behind the body: continue its facets and close it "
                                                          "with a pointed or flat faceted end"),
           ("bin6", "the LONG WING CRYSTAL at the right", "its inner (left) end is hidden behind the body: continue it and close it"),
           ("tail3", "the LONG POINTED TAIL CRYSTAL at the bottom right", "fully visible"),
           ("youjiao", "the little RIGHT FOOT under the body (the one at the right)", "its top is hidden under the body: complete it into a "
                                                                                      "small rounded closed foot shape"),
           ("zuojiao", "the little LEFT FOOT under the body (the one at the left)", "its top is hidden under the body: complete it into a "
                                                                                    "small rounded closed foot shape")],
    "M2": [("body", "the round cream BODY", "the parts of it covered by the head crystals, the wings, the hands and the face must be "
                                            "drawn: a complete smooth round chubby body with its full outline, plain cream, WITHOUT any face, "
                                            "eyes, brows, mouth or cheek marks, and without the little hand bumps"),
           ("tail2", "the TINY TAIL CRYSTAL below the body (left of the long tail crystal)", "fully visible")],
    "M3": [("bin3", "the BIG CRYSTAL on the upper LEFT of the head", "its lower end is hidden behind the middle crystal and touches the "
                                                                     "body: complete it with its full closed outline"),
           ("bin9", "the BIG CRYSTAL on the upper RIGHT of the head", "its lower end is hidden: complete it with its full closed outline"),
           ("bin7", "the SMALL PALE CRYSTAL under the left wing", "its inner end is hidden behind the body: complete it"),
           ("bin8", "the SMALL PALE CRYSTAL under the right wing", "its inner end is hidden behind the body and the right wing: complete it")],
    "M4": [("bin1", "the MIDDLE CRYSTAL on top of the head", "its lower end is hidden in the body outline: complete it with its full outline"),
           ("weitail1", "the SMALL TAIL CRYSTAL right under the body, between the feet", "its top is hidden behind the body: complete it")],
    # M4 lần đầu Codex vẽ lại hai bàn chân thay cho hai tay: tay gen riêng, có toạ độ
    "M5": [("zuoshou", "the little LEFT ARM NUB: the small rounded mitten-like bump that hangs on the LOWER LEFT side of the body, at about "
                       "x = 600 to x = 695, y = 570 to y = 670 (its inner side is marked in image 1 by a short curved stroke inside the body)",
            "draw it as ONE small separate rounded cream nub (about 90 px wide, 95 px tall) with its own complete ink outline all the way "
            "round, the same place and size"),
           ("youshou", "the little RIGHT ARM NUB: the small rounded mitten-like bump on the LOWER RIGHT side of the body, at about x = 968 to "
                       "x = 1040, y = 592 to y = 666 (marked in image 1 by a short curved stroke inside the body)",
            "draw it as ONE small separate rounded cream nub (about 70 px wide, 72 px tall) with its own complete ink outline all the way "
            "round, the same place and size")],
    "F1": [("eyes", "the two EYES WITH THEIR BROWS (golden-yellow eyes with dark navy ring and light dot, the two thick slanted navy brows)",
            "fully visible"),
           ("mt", "the MOUTH (the small closed smile with the tiny white fang)", "fully visible"),
           ("bin5", "the small four-pointed silver STAR on the LEFT cheek", "fully visible"),
           ("bin4", "the small four-pointed silver STAR on the RIGHT cheek", "fully visible")],
}
# cụm thừa Codex vẽ thêm (tâm cụm trên concept px): bỏ khi cắt
BO_CUM = {"M4": [(705, 712), (907, 712)]}
# hình mắt phụ (mắt nhắm, choáng): vẽ đúng chỗ đôi mắt + mày của concept
PHU = {
    "F2": ("biyan", "the two eyes TIGHTLY CLOSED, drawn as a bold '>' mark (left eye) and a bold '<' mark (right eye) in dark navy, each in the "
                    "same place and about the same size as the eye it replaces, with the two thick slanted navy BROWS kept above them"),
    "F3": ("yun", "the two eyes DIZZY, each drawn as a bold dark-navy SPIRAL in the same place and about the same size as the eye it "
                  "replaces, with the two brows kept above them but tilted up in the middle (a dazed look)"),
}


def Wp(p):
    return os.path.normpath(p)


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    to_px = lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
    to_rig = lambda P: np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    return s, to_px, to_rig


def hop_goc():
    """hộp (concept px) của từng part gốc ở khung 0 idle."""
    _, imgs, atts = G.nap("att_idle0.json")
    _, to_px, _ = tf()
    out = {}
    for a in atts:
        P = to_px(np.array(a["xy"], float).reshape(-1, 2))
        out[a["slot"]] = [float(P[:, 0].min()), float(P[:, 1].min()), float(P[:, 0].max()), float(P[:, 1].max())]
    return out


def khung():
    im = Image.open(CONCEPT).convert("RGB")
    d = ImageDraw.Draw(im)
    _, imgs, atts = G.nap("att_idle0.json")
    _, to_px, _ = tf()
    from hoa_ho import luoi
    for a in atts:
        P = to_px(np.array(a["xy"], float).reshape(-1, 2))
        _, tr = luoi(a)
        for t in tr:
            for i, j in ((0, 1), (1, 2), (2, 0)):
                pass
        # viền ngoài: bao lồi của các đỉnh
        h = cv2.convexHull(P.astype(np.float32)).reshape(-1, 2)
        d.line([tuple(p) for p in h] + [tuple(h[0])], fill=(230, 40, 40), width=2)
        c = P.mean(0)
        d.text((c[0] - 10, c[1] - 6), a["slot"], fill=(200, 0, 0))
    p = os.path.join(G.MAU, "_goc_tren_concept.png")
    im.save(p)
    print(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a round chubby cream spirit with determined golden eyes under "
        "thick slanted brows, a small smile with one fang, silver star marks on the cheeks, nine floating pointed blue-steel faceted "
        "crystals around it (three on the head, two long wing crystals at the sides, two small pale ones under them) and a tail of three "
        "lavender-steel crystals below. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3")[0].rstrip("\n")
    gd = ["", "## Lượt 3: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-15; người dùng chọn phương án 1 của lượt sửa nhẹ = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): thân kem, mày xếch, miệng một răng nanh, má sao bạc, "
          "9 tinh thể thép lam nhọn + đuôi 3 tinh thể. Mỗi lượt chỉ giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị che.", ""]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_3_{nh}.txt")
        t = [f"IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. Same wobbly ink line, same colours, same crayon hatching, same completely flat colouring as image 1. "
             "Do not move, resize, rotate or redesign anything. Keep a clear white gap between the kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    for nh, (slot, mt) in PHU.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_3_{nh}.txt")
        t = [f"IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: draw ONLY the character's eyes and brows, in exactly the SAME POSITION and at the SAME SIZE as in image 1, but CHANGED as "
             f"follows: {mt}. REMOVE everything else (body, mouth, cheeks, crystals: pure white). Same wobbly hand-drawn line, flat colours, "
             "crayon texture as image 1.", "", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({slot}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `tinh_sat_manh.py ghep`); phần bị che vẽ đủ, viền kín; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
def nen(A):
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H:
            bg |= lab == i
    return bg


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(ten) and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def cat(chi=None):
    os.makedirs(MANH, exist_ok=True)
    pd = os.path.join(MANH, "dat.json")
    DAT = json.load(open(pd)) if os.path.exists(pd) else {}
    HG = hop_goc()
    viec = {nh: [s for s, _, _ in ds] for nh, ds in NHOM.items()}
    viec.update({nh: [slot] for nh, (slot, _) in PHU.items()})
    for nh, slots in viec.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        # giấy trắng KHÉP KÍN lớn trong mảnh (lòng giữa hai chân, khe) vẫn là nền nếu nó không nằm trong hộp part nào
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = [i for i in range(1, n) if st[i, 4] > 30]
        # mắt phụ: hộp của mắt gốc; còn lại: hộp part gốc
        gan = {s: [] for s in slots}
        for i in cum:
            x, y, w, h, a = st[i]
            c = (x + w / 2, y + h / 2)
            if any(np.hypot(c[0] - bx, c[1] - by) < 30 for bx, by in BO_CUM.get(nh, [])):
                print(f"  {nh}: bỏ cụm thừa ở ({c[0]:.0f}, {c[1]:.0f})")
                continue
            best, bd = None, 1e9
            for s in slots:
                hb = HG["eyes" if s in ("biyan", "yun") else s]
                cx_, cy_ = (hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2
                # khoảng cách từ tâm cụm tới hộp (0 nếu nằm trong), cộng chút theo tâm
                dx = max(hb[0] - c[0], 0, c[0] - hb[2])
                dy = max(hb[1] - c[1], 0, c[1] - hb[3])
                dd = np.hypot(dx, dy) + 0.15 * np.hypot(c[0] - cx_, c[1] - cy_)
                if dd < bd:
                    best, bd = s, dd
            if bd < 160:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {a} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:9s} KHÔNG THẤY MẢNH")
                continue
            m = np.isin(lab, ids)
            ys, xs = np.nonzero(m)
            x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
            rgb = A[y0:y1, x0:x1].astype(np.uint8)
            mm = m[y0:y1, x0:x1]
            import dat_nung_da as DN
            rgb = DN.khu_vien(rgb, mm)
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), DA.el(2)).astype(bool)
            sang = rgb.min(2).astype(np.float32)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
            Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, s + ".png"))
            DAT[s] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=os.path.basename(src))
            hb = HG["eyes" if s in ("biyan", "yun") else s]
            print(f"  {s:9s} hộp ({x0}, {y0}, {x1}, {y1}) | part gốc ({hb[0]:.0f}, {hb[1]:.0f}, {hb[2]:.0f}, {hb[3]:.0f}), {len(ids)} cụm")
    json.dump(DAT, open(pd, "w"), indent=1)


def ghep():
    """ghép mảnh theo thứ tự vẽ của rig (eyes = mắt mở) lên nền trắng; đặt cạnh concept; IoU hình bóng."""
    DAT = json.load(open(os.path.join(MANH, "dat.json")))
    I = json.load(open(os.path.join(G.scan(), "info.json"), encoding="utf-8"))
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in [q["name"] for q in I["slots"] if q["name"] != "shadow"]:
        if s not in DAT:
            thieu.append(s)
            continue
        x0, y0, _, _ = DAT[s]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    print(p, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "khung":
        khung()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
