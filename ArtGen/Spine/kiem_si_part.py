# -*- coding: utf-8 -*-
"""Kiếm sĩ rừng: mảnh vẽ ĐÚNG KHUNG part của rig gốc monster_3620.

Tờ P (THÂN; người dùng 2026-11-12: "trúng đòn lỗi bị hở ở giữa, giáp tay phải lệch hẳn khỏi tay... mổ xẻ kĩ con gốc và xem mọi part của nó...
phần body tôi nghĩ nên gen đầy đủ không bị hở"): hai nửa cánh cứng to (P_keR, P_keL) + khối ngực (P_shenti2) + gù lưng (P_ke) + gáy (P_tou2)
+ bụng (P_shenti1) + hai bắp tay (P_shouR1, P_shouL1) + hai khuỷu.

Tờ Q (BÀN TAY; người dùng: "phần bàn tay không ôm vào kiếm, bạn xem con gốc nó làm thế nào sửa lại đi", rồi "lỗi nặng" với bản bàn tay hai mảnh
tự chế): tám part bàn tay của họ (mỗi tay một khối lòng bàn tay + ba ngón, xếp trước / sau thanh kiếm, mỗi ngón một xương). Vẽ lại đúng khung
từng part để tay ôm kiếm y như con gốc ở mọi dáng.

Mỗi part một ô đúng khung ảnh vùng của họ, trong ô là HÌNH BÓNG KÍN của part tô phẳng màu của mình, Codex vẽ lại sạch giữ nguyên hình bóng.

    kiem_si_part.py to [P|Q]     tờ hướng dẫn + file prompt → inbox/kiem_si_1/mau/khung_part[_Q].png (+ .json), gui_gpt/kiem_si_1/luot_*.txt
    kiem_si_part.py cat [P|Q]    cắt tờ M_P / M_Q đã gen → inbox/kiem_si_1/manh/kp_<tên>.png (đúng khung ảnh vùng) + _so_part[_Q].png
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
import kiem_si as KS  # noqa: E402
import kiem_si_manh as KM  # noqa: E402
import build_kiem_si as BK  # noqa: E402

W, H = 1536, 1024
INK = (43, 33, 24)
# (slot của họ, tên của mình, chất liệu, phóng so với px ảnh vùng)
TO = {
    "P": dict(part=[("P_keR", "ao", "la", 1.6), ("P_keL", "lung", "long", 1.6), ("P_shenti2", "than", "long", 1.6),
                    ("P_shouR1", "bap_g", "long", 1.6), ("P_shouL1", "bap_x", "long", 1.6),
                    ("P_ke", "gu", "long", 1.6), ("P_shenti1", "bung", "long", 1.6), ("P_tou2", "co", "long", 1.6),
                    ("P_shouR2_2", "khuyu_g", "long", 2.6), ("P_shouL2_2", "khuyu_x", "long", 2.6)],
              hang=[5, 5], duoi="", prompt="luot_3_khung_part.txt"),
    "Q": dict(part=[("P_shouR3_2", "r32", "da", 4.6), ("P_shouR3_1", "r31", "da", 4.6), ("P_shouR3_3", "r33", "da", 4.6),
                    ("P_shouR3_4", "r34", "da", 4.6),
                    ("P_shouL3_4", "l34", "da", 4.6), ("P_shouL3_1", "l31", "da", 4.6), ("P_shouL3_2", "l32", "da", 4.6),
                    ("P_shouL3_3", "l33", "da", 4.6)],
              hang=[4, 4], duoi="_Q", prompt="luot_5_khung_tay.txt"),
}


def mau_giua(ten):
    """màu tô thuần của một mảnh đã cắt (trung vị các điểm đặc, bỏ mực và điểm sáng)."""
    a = np.asarray(Image.open(os.path.join(KM.MANH, ten + ".png")).convert("RGBA")).astype(int)
    m = (a[..., 3] > 250) & (a[..., :3].sum(2) > 150) & (a[..., :3].min(2) < 200)
    px = a[m][:, :3]
    sang = px.sum(1)
    px = px[(sang > np.percentile(sang, 35)) & (sang < np.percentile(sang, 85))]
    return tuple(int(v) for v in np.median(px, 0))


def bong(a):
    """hình bóng kín (bool, cỡ ảnh vùng) của một part của họ."""
    al = np.asarray(KS.part_goc(a))[..., 3] > 90
    m = cv2.morphologyEx(al.astype(np.uint8), cv2.MORPH_CLOSE, KS.el(3))
    return m.astype(bool)


def aff_uv(a):
    """affine (2 × 3): toạ độ ảnh vùng (px) → thế giới khung 0 idle của họ (bình phương tối thiểu trên các đỉnh lưới)."""
    uv, _ = KS.luoi(a)
    xy = np.array(a["xy"], float).reshape(-1, 2)
    A = np.c_[uv, np.ones(len(uv))]
    M, *_ = np.linalg.lstsq(A, xy, rcond=None)
    sai = float(np.abs(A @ M - xy).max())
    return M.T, sai


def to(ma="P"):
    C = TO[ma]
    mau_p = os.path.join(KS.MAU, f"khung_part{C['duoi']}.png")
    _, imgs, atts = KS.nap()
    by = {a["slot"]: a for a in atts}
    MAUS = dict(long=mau_giua("than"), la=mau_giua("ao"), da=mau_giua("nam_x"))
    print("màu:", MAUS)
    can = np.full((H, W, 3), 255, np.uint8)
    o, y = {}, 26
    k = 0
    for n in C["hang"]:
        ds = C["part"][k:k + n]
        k += n
        cs = [(int(round(imgs[by[s]["region"]].width * z)), int(round(imgs[by[s]["region"]].height * z))) for s, _, _, z in ds]
        tong = sum(c[0] for c in cs)
        ke = (W - tong) // (n + 1)
        x = ke
        hh = max(c[1] for c in cs)
        for (s, ten, chat, z), (cw, ch) in zip(ds, cs):
            a = by[s]
            b0 = np.pad(bong(a), 8, mode="edge")     # đệm lặp mép trước khi làm trơn: chỗ hình bóng chạm khung ảnh vùng không bị khoét lõm
            m = cv2.resize(b0.astype(np.uint8) * 255, (int(round(b0.shape[1] * z)), int(round(b0.shape[0] * z))), interpolation=cv2.INTER_LINEAR)
            m = cv2.GaussianBlur(m, (0, 0), 2.0 if z < 3 else 5.0) > 127
            oy_, ox_ = (m.shape[0] - ch) // 2, (m.shape[1] - cw) // 2
            m = m[oy_:oy_ + ch, ox_:ox_ + cw]
            y0 = y + (hh - ch) // 2
            sub = can[y0:y0 + ch, x:x + cw]
            sub[m] = MAUS[chat]
            if chat == "la":                         # gân các lá: toả từ đầu trên (theo thế giới) của mảnh ra mép tròn
                M, _ = aff_uv(a)
                ys, xs = np.nonzero(m)
                P = np.c_[xs / z, ys / z, np.ones(len(xs))] @ M.T            # thế giới của từng điểm bóng
                goc = np.array([xs[np.argmax(P[:, 1])], ys[np.argmax(P[:, 1])]], float)
                vien = m & ~cv2.erode(m.astype(np.uint8), KS.el(2)).astype(bool)
                vy, vx = np.nonzero(vien)
                ang = np.arctan2(vy - goc[1], vx - goc[0])
                d = np.hypot(vx - goc[0], vy - goc[1])
                xa = d > 0.55 * d.max()
                for q in np.linspace(np.percentile(ang[xa], 6), np.percentile(ang[xa], 94), 6):
                    i = np.argmin(np.abs(ang - q) + (~xa) * 9.0)
                    p1 = goc + (np.array([vx[i], vy[i]], float) - goc) * 0.93
                    cv2.line(sub, (int(goc[0]), int(goc[1])), (int(p1[0]), int(p1[1])), (24, 70, 44), 4, cv2.LINE_AA)
            net = 5 if z < 3 else 8
            mp = np.pad(m, 12)                       # viền mực kín cả ở đoạn hình bóng bị khung ảnh vùng cắt thẳng
            sub[(mp & ~cv2.erode(mp.astype(np.uint8), KS.el(net)).astype(bool))[12:-12, 12:-12]] = INK
            o[ten] = dict(slot=s, hop=[x, y0, cw, ch], z=z, chat=chat)
            x += cw + ke
        y += hh + 46
    os.makedirs(KS.MAU, exist_ok=True)
    Image.fromarray(can).save(mau_p)
    json.dump(o, open(mau_p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(mau_p)
    duyet = os.path.join(KS.TAI, "L1_duyet.png")
    out = os.path.join(KS.TAI, f"M_{ma}.png")
    p = os.path.join(BK.pk(), C["prompt"])

    def cho(ten):
        x, y_, cw, ch = o[ten]["hop"]
        return f"about x = {x} to x = {x + cw}, y = {y_} to y = {y_ + ch}"

    dau = ["", f"SAVE: save it as a PNG to {BK.Wp(out)}",
           f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or delete "
           "any other file.", ""]
    giu = ("TASK: redraw image 1 CLEANLY in the hand-drawn style of image 2. Keep EVERY silhouette exactly: the same outline, the same "
           "size, the same orientation, the same place on the sheet (if the new picture were laid over image 1, every shape must coincide "
           "with its silhouette). Each part is ONE COMPLETE CLOSED SHAPE with the dark-brown ink outline running all the way round, "
           "exactly on the edge of its silhouette. The parts do not touch; pure white between them. Nothing else on the sheet.")
    if ma == "P":
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {BK.Wp(mau_p)}: a PARTS GUIDE SHEET, 1536x1024, white background, made by computer: TEN flat silhouettes of body parts "
             "of a creature for a 2D animation rig, each a closed shape filled with one flat colour and a dark outline. Nine of them are dark "
             "charcoal-brown (FUR parts); one, the first of the top row, is dark green with a few darker lines (a LEAF CAPE part). The "
             "silhouettes are exact: their outline, size, orientation and position on the sheet must be kept.",
             f"image 2 = {BK.Wp(duyet)}: the APPROVED picture of the creature these parts belong to, 1536x1024, white background: {BK.CON}. "
             "It gives the wobbly dark-brown ink line and its thickness, the crayon hatching, the exact look of the shaggy charcoal fur (see "
             "the fur of its arms and body) and of the dark-green leaf cape behind it. Do NOT copy its pose or its parts: only its style."]
        t += dau + [giu.replace("ink outline running", "ink outline (about 6 px) running"), "",
                    "- THE NINE CHARCOAL PARTS are pieces of the creature's FUR-covered body (back, chest, neck, belly, upper arms, elbows): fill "
                    "each one completely with the flat charcoal-brown fur colour of image 2 with its crayon hatching, and a few short curved fur "
                    "ticks inside (thin darker pencil strokes, three to eight per part depending on its size). Along the outline draw the fur as "
                    "small, low, rounded-pointed tufts that stay ON the silhouette edge: the tufts may dent the outline inward a little but must "
                    "NOT stick out beyond the silhouette and must not change its overall shape. No face, no eyes, no hands, no armour, no other "
                    "colour on these parts.",
                    f"- THE GREEN PART (first of the top row, {cho('ao')}) is the creature's RAIN CAPE OF LEAVES: fill the whole silhouette with "
                    "five or six big overlapping dark-green leaves like the cape in image 2. The darker lines in the guide are the centre veins "
                    "of the leaves: all leaves grow from the point where those lines meet and fan out toward the rounded edge, their pointed "
                    "tips forming a gently scalloped (not deeply cut) rounded edge that stays ON the silhouette edge. Each leaf has its centre "
                    "vein and a few side veins; ink outline between the leaves. The straight edge of the silhouette stays straight.", "",
                    "Do not add anything: no shadows, no glow, no labels, no extra pieces.", "", BK.FLAT3]
    else:
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {BK.Wp(mau_p)}: a PARTS GUIDE SHEET, 1536x1024, white background, made by computer: EIGHT flat tan silhouettes, each "
             "a closed shape filled with one flat skin colour and a dark outline, drawn very big. They are the separate pieces of the "
             "creature's two HANDS for a 2D animation rig: in each row the FIRST, biggest shape is the PALM BLOCK of a hand (the chunky back "
             "of the hand), and the other three, smaller, tapering shapes are single FINGERS (each one a fat finger seen from the side, its "
             "wide end is the knuckle, its narrow end is the fingertip). The silhouettes are exact: their outline, size, orientation and "
             "position on the sheet must be kept.",
             f"image 2 = {BK.Wp(duyet)}: the APPROVED picture of the creature these parts belong to, 1536x1024, white background: {BK.CON}. "
             "It gives the wobbly dark-brown ink line, the crayon hatching and the exact flat tan skin colour of its bare monkey hands. Do "
             "NOT copy its pose or its hands: only its style and skin colour."]
        t += dau + [giu.replace("ink outline running", "ink outline (about 9 px on this sheet, because the parts are drawn big) running"), "",
                    "- Fill every part completely with the flat tan skin colour of the hands in image 2, with its crayon hatching.",
                    "- THE TWO PALM BLOCKS (first shape of each row): the back of a chunky monkey hand: plain skin with ONE or TWO short curved "
                    "crease lines (thin darker pencil strokes), nothing else.",
                    "- THE SIX FINGERS: each one fat finger: plain skin with ONE short crease line across it near its middle (a knuckle fold). "
                    "Where the silhouette's narrow end is sharply pointed, round the very tip a little (a blunt fingertip, not a claw), without "
                    "changing the rest of the outline. No nails, no claws, no fur.", "",
                    "Do not add anything: no shadows, no glow, no labels, no extra pieces, no sword.", "", BK.FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    print(p)


def cat(ma="P"):
    C = TO[ma]
    mau_p = os.path.join(KS.MAU, f"khung_part{C['duoi']}.png")
    o = json.load(open(mau_p[:-4] + ".json", encoding="utf-8"))
    A = KM.doc(KM.moi_nhat(ma))
    G = KM.doc(mau_p)
    bg = KM.nen(A, 10 ** 9)
    bgG = G.min(2) > 238
    so = []
    for ten, d in o.items():
        x, y, cw, ch = d["hop"]
        pad = 10
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
        m = ~bg[y0:y1, x0:x1]
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        if n > 1:                                    # chỉ lấy cụm lớn nhất trong ô (mẩu của ô bên cạnh thì bỏ)
            m = lab == (1 + int(np.argmax(st[1:, 4])))
        full = np.zeros(bg.shape, bool)
        full[y0:y1, x0:x1] = m
        if d["z"] >= 3:                              # part vẽ to (bàn tay, phóng 4,6 lần) rồi thu ~0,24 lần lúc lắp: nét 9 px chỉ còn ~2 px,
            muc = (A.max(2) < 120) & full            # mảnh hơn nét của cả con → nở vùng mực 6 px về mỗi phía trước khi cắt
            muc = cv2.dilate(muc.astype(np.uint8), KS.el(6)).astype(bool)
            A = A.copy()
            A[muc] = INK
            full = full | muc
        im, goc = KM.manh_rgba(A, full)
        khung = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))                    # đặt lại vào ĐÚNG khung ô (= khung ảnh vùng của họ)
        khung.paste(im, (goc[0] - x, goc[1] - y), im)
        khung.save(os.path.join(KM.MANH, f"kp_{ten}.png"))
        a = np.asarray(khung)[..., 3] > 120
        b = ~bgG[y:y + ch, x:x + cw]
        iou = float((a & b).sum()) / max(1, (a | b).sum())
        vis = np.full((ch, cw, 3), 255, np.uint8)
        vis[a & b] = (170, 170, 170)
        vis[b & ~a] = (230, 60, 60)                  # đỏ: hình bóng mà mảnh không phủ
        vis[a & ~b] = (60, 190, 60)                  # lục: vẽ thừa ra ngoài
        so.append((ten, iou, Image.fromarray(vis), khung))
        print(f"  {ten:8s} IoU {iou:.3f}  ({cw} × {ch})")
    w_ = sum(max(s[2].width, 120) + 10 for s in so)
    hh = max(s[2].height for s in so)
    out = Image.new("RGB", (w_ + 10, hh * 2 + 30), (150, 150, 150))
    x = 10
    for ten, iou, vis, kh in so:
        out.paste(vis, (x, 10))
        out.paste(kh, (x, hh + 20), kh)
        x += max(vis.width, 120) + 10
    out.save(os.path.join(KM.MANH, f"_so_part{C['duoi']}.png"))
    print(os.path.join(KM.MANH, f"_so_part{C['duoi']}.png"))


if __name__ == "__main__":
    if sys.argv[1:2] == ["to"]:
        to(*sys.argv[2:3])
    elif sys.argv[1:2] == ["cat"]:
        cat(*sys.argv[2:3])
    else:
        print(__doc__)
