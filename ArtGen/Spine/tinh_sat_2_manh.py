# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt DẠNG 2 (tinh_sat_2, rig monster_3347): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png = L1_A,
người dùng chọn 2026-11-16: mặt kem + mày, giáp thép lam, cằm bạc lam, tinh thể bay oải hương). Concept vẽ đúng khung hình cả con gốc ở khung 0
idle (mau/goc_ca_con.json), nên mỗi mảnh cắt ra là đặt thẳng vào thế giới rig ở dáng idle 0 rồi gắn lên xương của mảnh cũ (như dạng 1,
tinh_sat_manh.py).

Khác dạng 1: nhóm gen chia TỰ ĐỘNG theo hình bóng ĐỦ của từng mảnh (cả phần khuất; tinh_sat_2_da.mat_na) để các mảnh trong một nhóm không chồng
nhau; mỗi nhóm kèm ảnh 2 = TỜ DÁNG (hình bóng đủ của từng mảnh giữ lại, xám) để GPT biết phần khuất kéo tới đâu.

    tinh_sat_2_manh.py nhom        chia nhóm → mau/nhom.json + tờ dáng mau/dang_<nhóm>.png
    tinh_sat_2_manh.py prompt      file prompt từng nhóm → gui_gpt/tinh_sat_2/luot_2_<nhóm>.txt (+ HUONG_DAN.md)
    tinh_sat_2_manh.py cat [nhóm]  cắt tai_ve/M_<nhóm>.png → inbox/tinh_sat_2/manh/<vùng>.png + manh/dat.json
    tinh_sat_2_manh.py ghep        ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tinh_sat_2 as G  # noqa: E402
import tinh_sat_2_da as DA  # noqa: E402

W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = DA.GUI
PNHOM = os.path.join(G.MAU, "nhom.json")

# mỗi mảnh: (mô tả tiếng Anh, cách vẽ phần khuất)
MO_TA = {
    "P_lian_1": ("the C-shaped SHELL of chunky blue-steel crystal plates wrapped round the face",
                 "complete it into ONE continuous C-shaped band with its full outline, following the grey shape of image 2: also draw the "
                 "parts hidden behind the crown spikes on top, behind the two chin crystals at the lower left and behind the floating "
                 "shards at the left, with the same plates and facet lines. The face window inside the C stays EMPTY WHITE (no face, no "
                 "eyes, no brows)"),
    "P_lian": ("the FACE: the cream face window between the shell plates",
               "draw it as ONE complete plain cream (#F7F4EC) rounded disc filling the whole grey shape of image 2 (most of it is hidden "
               "behind the shell in image 1: draw it whole), with its full outline, WITHOUT eyes, brows or any marks"),
    "P_maozi": ("the CROWN of three sharp blue-steel crystal spikes on top", "complete the part of the left spike hidden behind the "
                                                                               "floating shard, so the crown has its full outline"),
    "P_zui": ("the two CHIN crystals (pale silver-cyan) in front of the lower face", "fully visible; keep them as one piece"),
    "P_tui_R2": ("the UPPER part of the LEFT leg (the leg at the viewer's left): a rounded blue-steel crystal lump",
                 "it is almost completely hidden behind the chin crystals in image 1: draw it whole, filling the grey shape of image 2, "
                 "with its full outline"),
    "P_tui_R1": ("the LEFT FOOT (viewer's left): a faceted blue-steel crystal foot at the bottom left",
                 "its top is hidden behind the body: complete it into a closed faceted foot as in the grey shape of image 2"),
    "P_tui_L2": ("the UPPER part of the RIGHT leg (the leg at the viewer's right): a rounded blue-steel crystal lump",
                 "it is almost completely hidden in image 1: draw it whole, filling the grey shape of image 2, with its full outline"),
    "P_tui_L1": ("the RIGHT FOOT (viewer's right): a faceted blue-steel crystal foot at the bottom right",
                 "its top is hidden behind the body: complete it into a closed faceted foot as in the grey shape of image 2"),
    "P_bc_01": ("the long lavender FLOATING SHARD at the left, pointing out to the left", "fully visible"),
    "P_bc_02": ("the slim lavender FLOATING SHARD at the upper left, pointing up and to the left", "fully visible"),
    "P_bc_03": ("the long slim lavender FLOATING SHARD at the upper right, slanting like a halo above the head", "fully visible"),
    "P_bc_04": ("the lavender FLOATING SHARD at the right, pointing to the right", "its inner (left) end is hidden behind the shell: "
                                                                                     "continue it and close it as in the grey shape of image 2"),
    "P_bc_05": ("the small lavender FLOATING SHARD at the lower right, pointing down and to the right",
                "its inner (upper left) end is hidden behind the shell: continue it and close it as in the grey shape of image 2"),
}
# mắt: mở (concept), nhắm chặt `> <` (P_biyan: trúng đòn, chết, chiêu), chớp (P_biyan2: idle)
MAT = {
    "F1": ("P_yanjing", "the two EYES WITH THEIR BROWS exactly as in image 1 (golden-yellow eyes with the dark-navy rim and the tiny light "
                        "dot, the two thick slanted navy brows)"),
    "F2": ("P_biyan", "the two eyes TIGHTLY CLOSED, drawn as a bold '>' mark (left eye) and a bold '<' mark (right eye) in dark navy "
                      "#2C2A5C, each in the same place and about the same size as the eye it replaces, with the two thick slanted navy BROWS "
                      "kept above them exactly as in image 1"),
    "F3": ("P_biyan2", "the two eyes CLOSED IN A BLINK, each drawn as one thick gently curved dark-navy #2C2A5C line (curving down) along "
                       "the lower edge of the eye it replaces, the same width as that eye, with the two thick slanted navy BROWS kept above "
                       "them exactly as in image 1"),
}
ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: an armoured iron-crystal spirit seen from the front, turned "
        "slightly to the viewer's right: a cream face window with determined golden eyes under thick slanted navy brows, a C-shaped shell "
        "of chunky blue-steel crystal plates round the face, a crown of three sharp blue-steel crystal spikes on top, two pale silver-cyan "
        "chin crystals, two stubby blue-steel legs, five slim lavender crystal shards floating around. Hand-drawn: wobbly dark-brown ink "
        "line, crayon hatching, flat colours.")


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


def mat_na():
    p = os.path.join(G.MAU, "_mat_na.npz")
    if os.path.exists(p):
        z = np.load(p)
        return {k: z[k] for k in z.files}
    M = DA.mat_na()
    np.savez_compressed(p, **M)
    return M


def nhom():
    """chia nhóm tham lam: mảnh to trước; một mảnh vào nhóm đầu tiên mà hình bóng đủ (nới 16 px) không chạm mảnh nào trong nhóm; tối đa 4."""
    M = mat_na()
    nd = {k: cv2.dilate(v.astype(np.uint8), DA.el(16)).astype(bool) for k, v in M.items()}
    ds = sorted([k for k in M if k in MO_TA], key=lambda k: -M[k].sum())
    G_ = []
    for k in ds:
        for g in G_:
            if len(g) < 4 and not any((nd[k] & nd[q]).any() for q in g):
                g.append(k)
                break
        else:
            G_.append([k])
    NH = {f"M{i + 1}": g for i, g in enumerate(G_)}
    json.dump(NH, open(PNHOM, "w"), indent=1)
    for nh, g in NH.items():
        can = np.full((H, W, 3), 255, np.uint8)
        for k in g:
            m = M[k]
            can[m] = (214, 214, 214)
            can[m & ~cv2.erode(m.astype(np.uint8), DA.el(2)).astype(bool)] = (90, 90, 90)
        Image.fromarray(can).save(os.path.join(G.MAU, f"dang_{nh}.png"))
        print(nh, g)
    return NH


def prompt():
    NH = json.load(open(PNHOM))
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-16; người dùng chọn A = `L1_duyet.png`)", "",
          f"Ảnh mẫu 1 = `{Wp(CONCEPT)}`: concept A đã chọn (1536 × 1024, nền trắng). Ảnh mẫu 2 (nhóm M) = tờ dáng `mau/dang_<nhóm>.png`: hình "
          "bóng ĐỦ (cả phần bị che) của từng mảnh giữ lại, tô xám, đúng chỗ. Mỗi lượt chỉ giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ "
          "đủ phần bị che. Nhóm F chỉ vẽ mắt + mày (mở, nhắm chặt, chớp).", ""]
    for nh, ds in NH.items():
        out, save = luu(f"M_{nh}")
        dang = os.path.join(G.MAU, f"dang_{nh}.png")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}",
             f"image 2 = {Wp(dang)}: SHAPE GUIDE, 1536x1024, white background, made by computer: the FULL shape of each part to keep (grey "
             "with a thin dark edge), including the portions hidden behind other parts in image 1, at exactly the same place. Use it only to "
             "know where each part's hidden portion ends; take the look, colours and lines from image 1.", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue (its full shape is the grey "
             "shape of image 2), in the same style, colours and flat crayon colouring. Same wobbly ink line, same colours, same crayon "
             "hatching, same completely flat colouring as image 1 (no shading, no highlights). Do not move, resize, rotate or redesign "
             "anything. Keep a clear white gap between the kept parts.", "", "KEEP:"]
        t += [f"{i}. {MO_TA[s][0]}: {MO_TA[s][1]}." for i, s in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(ds)}): ảnh mẫu 2 = `{Wp(dang)}`; chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    for nh, (slot, mt) in MAT.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: draw ONLY the character's eyes and brows, in exactly the SAME POSITION and at the SAME SIZE as in image 1"
             + (", unchanged" if nh == "F1" else ", but CHANGED as follows") + f": {mt}. REMOVE everything else (face, shell, crown, chin, "
             "legs, shards: pure white). Same wobbly hand-drawn line, flat colours, crayon texture as image 1.", "",
             "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({slot}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `tinh_sat_2_manh.py ghep`); phần bị che vẽ đủ theo tờ dáng, "
           "viền kín; lòng chữ C của vỏ để trắng; nền trắng tinh."]
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
    fs = sorted([f for f in os.listdir(G.TAI) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def luu_manh(A, m, ten, DAT, src):
    import dat_nung_da as DN
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8)
    mm = m[y0:y1, x0:x1]
    rgb = DN.khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), DA.el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DAT[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=os.path.basename(src))
    return x0, y0, x1, y1


def cat(chi=None):
    os.makedirs(MANH, exist_ok=True)
    pd = os.path.join(MANH, "dat.json")
    DAT = json.load(open(pd)) if os.path.exists(pd) else {}
    M = mat_na()
    NH = json.load(open(PNHOM))
    viec = dict(NH)
    viec.update({nh: [slot] for nh, (slot, _) in MAT.items()})
    for nh, slots in viec.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        trang = A.min(2) > 236
        print(f"{nh} ({os.path.basename(src)}):")
        if nh in MAT:                                                  # mắt: lấy mọi nét quanh chỗ mắt + mày
            hop = M["P_yanjing"]
            vung = cv2.dilate(hop.astype(np.uint8), DA.el(70)).astype(bool)
            m = fg & vung & ~trang
            m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, DA.el(2)).astype(bool) & fg
            if not m.any():
                print("  KHÔNG THẤY NÉT")
                continue
            b = luu_manh(A, m, slots[0], DAT, src)
            print(f"  {slots[0]:10s} hộp {b}")
            continue
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        nd = {s: cv2.dilate(M[s].astype(np.uint8), DA.el(25)).astype(bool) for s in slots}
        gan = {s: np.zeros((H, W), bool) for s in slots}
        for i in range(1, n):
            if st[i, 4] < 30:
                continue
            c = lab == i
            ov = {s: (c & nd[s]).sum() for s in slots}
            s = max(ov, key=ov.get)
            if ov[s] < 0.3 * st[i, 4]:
                x, y, w, h, a = st[i]
                print(f"  bỏ cụm ({x + w / 2:.0f}, {y + h / 2:.0f}), {a} px")
                continue
            gan[s] |= c
        for s, m in gan.items():
            if not m.any():
                print(f"  {s:10s} KHÔNG THẤY MẢNH")
                continue
            m = m & ~(trang & ~cv2.dilate(M[s].astype(np.uint8), DA.el(6)).astype(bool))   # giấy trắng ngoài hình bóng (lòng chữ C) = nền
            b = luu_manh(A, m, s, DAT, src)
            mm = M[s]
            iou = (m & mm).sum() / max(1, (m | mm).sum())
            print(f"  {s:10s} hộp {b} | khớp hình bóng đủ {iou:.2f}")
    json.dump(DAT, open(pd, "w"), indent=1)


def ghep():
    """ghép mảnh theo thứ tự vẽ của rig (mắt mở) lên nền trắng; đặt cạnh concept; IoU hình bóng."""
    DAT = json.load(open(os.path.join(MANH, "dat.json")))
    I = json.load(open(os.path.join(G.scan(), "info.json"), encoding="utf-8"))
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in [q["name"] for q in I["slots"] if q["name"] not in ("shadow", "P_tui_R1_2", "P_tui_L1_1")]:
        if s not in DAT:
            thieu.append(s)
            continue
        x0, y0, _, _ = DAT[s]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    lech = np.abs(C - Gp).sum(2) > 90
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[(a & b) & lech] = (240, 170, 60)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    can.convert("RGB").save(os.path.join(MANH, "_ghep_to.png"))
    print(p, f"IoU hình bóng {iou:.3f}; điểm lệch màu {(lech & a & b).sum() / max(1, (a & b).sum()) * 100:.1f} %",
          ("thiếu: " + ", ".join(thieu)) if thieu else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "nhom":
        nhom()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
