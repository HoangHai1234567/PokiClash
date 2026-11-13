# -*- coding: utf-8 -*-
"""Giác Mộc NON (suất 9 đảo Mộc, id moc_tinh, dạng 1; người dùng 2026-11-13 duyệt concept A "nụ sừng": inbox/giac_moc_non/tai_ve/L1_nu.png).
Dựng THẲNG trên .atomik dạng lớn (Resources/giac_moc_2/giac_moc_2.atomik: cùng xương, lưới, clip; máy C không có dữ liệu quét con gốc):
- tỉ lệ xương: inbox/giac_moc_non/mau/ti_le.json (như bố cục gửi GPT);
- đầu liền nụ sừng: cắt từ concept, ô cứng trên xương đầu bone65 (thay mảnh `dau`);
- bốn lá mào: cắt từ concept, ô cứng trên bốn xương MỚI `la_1..4` (con của bone65, gốc ở gốc lá), thay mảnh P_toufa5/2/4/3; khoá xoay đung
  đưa tự viết (rig gốc để mào trên chuỗi cổ: lúc cúi đầu gốc lá lệch tới ~200 px so với đầu, lộ mép cắt);
- mọi mảnh khác: tô màu lại theo nhóm (lá lục sẫm → lục non, thân sáng ấm hơn), giữ vân chì sáp;
- xương `mieng` (chỗ tụ cầu, game.muzzle) dời về đỉnh nụ sừng;
- clip `evolve`: gộp dạng lớn bản nhẹ (atlas × 0,5).
Ra inbox/giac_moc_non/rig/ (giac_moc_non.atomik, chan_dung.png, xem.html, khung soi). Xương, lưới, chuyển động gốc là của nhà phát hành
game tham khảo; hình là của mình. Dùng nội bộ.

    py -3 -I ArtGen/Spine/giac_moc_non.py
"""
import json
import os
import shutil
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402
from cat_concept import cat  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
BASE = os.path.join(HERE, "inbox", "giac_moc_non")
RA = os.path.join(BASE, "rig")
TEN = "giac_moc_non"
SRC = os.path.join(RES, "giac_moc_2", "giac_moc_2.atomik")
CONCEPT = os.path.join(BASE, "tai_ve", "L1_nu.png")
KHUNG = (-560, -60, 900, 1330)                  # khung của bo_cuc.png (atomik_bocuc.py --khung)
SIZE_A, SIZE_B = 0.9, 1.05                       # cỡ dạng 1, 2 trong heroes.json
DPX = 0.85                                       # px atlas / đơn vị rig cho mảnh cắt từ concept

# đa giác khung đầu trên canvas concept (px); các vùng kín nằm >= 70 % trong khung thuộc về đầu
DAU_POLY = np.array([(670, 330), (750, 315), (830, 310), (920, 315), (970, 295), (980, 230), (1020, 200), (1075, 220), (1060, 380),
                     (1055, 480), (1062, 560), (1042, 600), (990, 606), (900, 598), (840, 587), (780, 553), (740, 525), (700, 500), (670, 410)])
NU_SUNG = (1058, 236)                            # đỉnh nụ sừng trên concept: xương mieng
# lá mào: (slot cũ, tâm lá trên concept để chọn thành phần lục, gốc lá trên concept, pha đung đưa)
LA = [("P_toufa5", (693, 269), (742, 335), 0.00),
      ("P_toufa2", (789, 239), (792, 322), 0.27),
      ("P_toufa4", (884, 262), (880, 318), 0.55),
      ("P_toufa3", (783, 310), (786, 336), 0.80)]
# đổi màu theo nhóm slot (màu atlas cũ → màu concept)
NHOM = {
    ("B_beimao", "P_beifa", "P_toufa", "B_tou"): [
        ("#2F793B", "#7CBA44"), ("#348545", "#86C246"), ("#32843B", "#86C246"), ("#2E6930", "#5E9A3A"), ("#449447", "#8CC64C"),
        ("#83B940", "#A6D460"), ("#89C444", "#A8D664"), ("#74A237", "#96C452"), ("#52862F", "#6AA640"), ("#B3D95F", "#C4E57A")],
    ("P_shenti", "TH_", "TQ_", "P_tuimao", "P_tuijiao", "P_bei_", "B_bozi_1", "P_bozi", "P_tou2"): [
        ("#A36C3D", "#B07240"), ("#AC7647", "#B67A47"), ("#AD7545", "#B67A47"), ("#966538", "#A66C3C"), ("#96653A", "#A66C3C"),
        ("#815434", "#6E4224"), ("#805635", "#6E4224"), ("#75A734", "#88BA38"), ("#5A7A2A", "#6A9A34")],
    ("B_bozi_A", "B_bozi_B", "B_bozi_C", "B_bozi_D", "B_bozi_E", "B_bozi_F"): [
        ("#357D3B", "#4B9544"), ("#81A736", "#88BA38"), ("#87BD44", "#8CC64C"), ("#5E9337", "#5E9A3A")],
}


def dung():
    J, img, ver = A.load(SRC)
    JB, imgB, _ = A.load(SRC)
    hB = JB["game"]["height"]
    A.scale_bones(J, json.load(open(os.path.join(BASE, "mau", "ti_le.json"), encoding="utf-8")))
    S = J["slots"]
    B = A.bi(J)
    # ---- màu
    for pre, pairs in NHOM.items():
        ais = [i for i, a in enumerate(J["atts"]) if S[a["slot"]]["name"].startswith(pre)]
        img = A.recolor(img, A.att_masks(J, img, ais), pairs)
    # ---- cắt từ concept
    rgb = np.asarray(Image.open(CONCEPT).convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    green = (hsv[..., 0] > 30) & (hsv[..., 0] < 90) & (hsv[..., 1] > 50) & (rgb.min(2) < 238)
    dau, m_dau = cat(rgb, DAU_POLY, ti=0.7, loai=green)
    to_rig, to_px, z = A.canvas_map(KHUNG, rgb.shape[1], rgb.shape[0])
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    ims, quads = [], []                          # (att names, bone, góc theo xương)

    def o_cung(rgba, bone, att_names, bao=None):
        im = Image.fromarray(rgba, "RGBA")
        bb = bao or im.getbbox()
        crop = im.crop(bb)
        w = max(2, round((bb[2] - bb[0]) * z * DPX))
        h = max(2, round((bb[3] - bb[1]) * z * DPX))
        ims.append(crop.resize((w, h), Image.LANCZOS))
        corners = to_rig([(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])])
        quads.append((att_names, bone, A.bone_local(P, bone, corners)))

    o_cung(dau, B["bone65"], ["dau"])
    # lá: thành phần lục quanh tâm, + nét mực ôm; phần lấn xuống dưới đầu tô thêm màu lá (không hở khi lá đung đưa)
    n, lab = cv2.connectedComponents(green.astype(np.uint8), connectivity=8)
    ink = rgb.min(2) < 90
    for slot, tam, goc, pha in LA:
        comp = lab == lab[tam[1], tam[0]]
        near = cv2.dilate(comp.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))).astype(bool)
        m = comp | (near & ink & ~m_dau)
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)).astype(bool)
        ext = cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(bool) & m_dau & ~m
        col = np.median(rgb[comp], axis=0).astype(np.uint8)
        px = rgb.copy()
        px[ext] = col
        mm = m | ext
        a = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 1.0)
        rgba = np.dstack([px, (np.clip((a - 0.25) / 0.5, 0, 1) * 255).astype(np.uint8)])
        q = to_rig([goc])[0]
        lp = A.bone_local(P, B["bone65"], [q])[0]
        bnew = A.add_bone(J, f"la_{len(quads)}", B["bone65"], lp[0], lp[1])
        P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
        o_cung(rgba, bnew, [slot])
        A.sway(J, bnew, amp=4.5, chu_ky=1.7 + 0.2 * pha, pha=pha)
    img, boxes = A.add_regions(J, img, ims)
    H2, W2 = img.shape[:2]
    for (names, bone, loc), box in zip(quads, boxes):
        for ai, a in enumerate(J["atts"]):
            if a["name"] in names:
                A.set_quad(J, H2, W2, ai, box, bone, loc)
    # ---- xương mieng về đỉnh nụ sừng (chỗ tụ cầu của chiêu mana)
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    mi = B["mieng"]
    par = J["bones"][mi]["parent"]
    lp = A.bone_local(P, par, to_rig([NU_SUNG]))[0]
    J["bones"][mi]["x"], J["bones"][mi]["y"] = float(lp[0]), float(lp[1])
    # ---- khối game
    g = dict(J["game"])
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    g["height"] = round(float(A.bounds(P)[3]), 2)
    ci = A.clip(J, "cast")
    tc = g["hitTimes"][g["hitClips"].index("cast")] if "cast" in g["hitClips"] else 0.0
    P.at(ci, tc)
    g["muzzle"] = [round(float(v), 2) for v in P.bone_pt(mi)]
    J["game"] = g
    J["rigName"] = TEN
    # ---- tiến hóa
    k_B = SIZE_B / SIZE_A * g["height"] / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=B["bone"])
    print(f"cao dạng 1 {g['height']:.0f} (dạng 2 {hB:.0f}); dạng 2 trong rig gộp × {k_B:.3f}; muzzle {g['muzzle']}")
    return J, img, ver


def main():
    J, img, ver = dung()
    os.makedirs(RA, exist_ok=True)
    p = os.path.join(RA, TEN + ".atomik")
    n, nj, npng = A.save(p, J, img, ver)
    print(f"{p}: {n // 1024} KB (JSON {nj // 1024} KB, PNG {npng // 1024} KB), {len(J['bones'])} xương, {len(J['slots'])} slot, "
          f"atlas {img.shape[1]}x{img.shape[0]}, clip {[a['name'] for a in J['anims']]}")
    # chân dung 512 (khung 0 idle, cả con, nền trong suốt)
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    b = A.bounds(P)
    side = max(b[2] - b[0], b[3] - b[1]) * 1.12
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    im = A.render(J, img, P, (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2), 1024 / side, ss=1).resize((512, 512), Image.LANCZOS)
    im.save(os.path.join(RA, "chan_dung.png"))
    # trang xem
    shutil.copyfile(os.path.join(HERE, "mo_xe", "atomik_xem.py"), os.path.join(RA, "_atomik_xem.py")) if False else None
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "atomik_xem.py"), ROOT, RA, p, "Giác Mộc Non (dạng 1, suất 9 đảo Mộc)"])


if __name__ == "__main__":
    main()
