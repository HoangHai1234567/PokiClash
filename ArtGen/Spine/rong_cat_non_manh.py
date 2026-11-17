# -*- coding: utf-8 -*-
"""Sa Long DẠNG 1 (dạng non; mã rong_cat_non, rig monster_3529; ghi chú inbox/rong_cat_non_ghichu.md): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ".

Concept duyệt (tai_ve/L1_duyet.png = L1_A, Magnific; người dùng 2026-11-17: "duyệt rồi mà làm ngay đi") đã vẽ theo dáng rig 3529: bàn chân,
hông, đầu, đuôi trùng chỗ con gốc (chỉ khác: chùm gai mào và gai lưng lớn của họ thành hai sừng ngắn + vài phiến sa thạch nhỏ). Không cần
concept nắn: các tờ mảnh cắt thẳng trên concept duyệt.

Mảnh (tên ảnh → slot / xương của họ, xem rong_cat_non_rig.SLOT):
    than            thân + cổ + ngực bụng kem (gộp shenti_1, shenti_2, bozi_1)          T1
    dau             đầu + hai sừng đá + phiến má + sừng mũi hổ phách, KHÔNG mắt        T2 (cứng trên xương đầu bone6)
    duoi            đuôi + vằn + ba phiến nhỏ trên đuôi                                 T2 (weiba_2)
    chan_gan        chân sau gần (trái) + vuốt                                          T3 (tui_1..3 + zhuazi_4..6)
    tay_xa          chân trước xa (phải) + vuốt                                         T3 (shou_4..6 + zhuazi_10..12)
    tay_gan         chân trước gần (giữa trái, trước bụng) + vuốt                       T4 (shou_1..3 + zhuazi_1..3)
    pa / pc         phiến lưng to sau cổ / phiến nhỏ ở hông                             T4 (xương riêng)
    chan_xa         chân sau xa (giữa, nửa khuất) + vuốt                                T5 (tui_4..6 + zhuazi_7..9)
    pb              phiến lưng giữa                                                     T5
    mat / mat_nham  mắt mở (cắt thẳng) / mắt nhắm (dựng từ mặt nạ mắt)

    rong_cat_non_manh.py prompt       năm tờ mảnh → gui_gpt/rong_cat_non/luot_2_T1..T5.txt
    rong_cat_non_manh.py cat [tờ]     cắt tờ (tai_ve/M_<tờ>.png) → manh/<tên>.png + manh/dat.json
    rong_cat_non_manh.py mat          mắt mở cắt thẳng từ concept + mắt nhắm dựng từ mặt nạ → manh/mat*.png
    rong_cat_non_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5_dang2 as D2  # noqa: E402

G = D2.dat_non("rong_cat")
W, H = 1536, 1024
DUYET = os.path.join(G.TAI, "L1_duyet.png")
NAN = DUYET
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "rong_cat_non")


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


# tâm dự kiến (px concept) để gán cụm cắt ra đúng tên
TAM = {"than": (760, 620), "dau": (950, 400), "duoi": (420, 640), "chan_gan": (530, 770), "tay_xa": (990, 760), "tay_gan": (765, 770),
       "pa": (757, 520), "pc": (562, 640), "chan_xa": (820, 800), "pb": (657, 580), "dau_tren": (950, 380), "ham": (975, 515)}
VIEN = ("complete it into ONE CLOSED SHAPE with the dark-brown ink outline all the way round; where it is hidden behind another part in "
        "image 1, draw the hidden portion as it would continue (same colours, same flat crayon colouring)")
NHOM = {
    "T1": [("than", "the BODY: the neck (dark brown, from under the back of the head at about (780-900, 450) down to the shoulders), the torso "
            "from the shoulders (about x 900) to the hips (about x 560), the dusty brown back and sides and the cream throat, chest and belly "
            "running from under the jaw at about (900, 540) down the front of the chest to the belly at about (650-880, 740)",
            "draw it WITHOUT the head, WITHOUT the back plates, WITHOUT any leg and WITHOUT the tail: the top of the neck, hidden behind the "
            "head, continues as a plain rounded brown neck end; the back under the plates continues as plain brown skin with a smooth rounded "
            "outline; where the four legs cover the body, continue the brown sides and the cream belly; at the hips, where the tail starts, "
            "close it with a rounded edge (the tail is not drawn); the shoulders and hips are rounded where the legs join")],
    "T2": [("dau", "the HEAD: the brown head with its two short cream stone horns on top (tips at about (790, 245) and (885, 210)), the "
            "striped cream-and-ochre plate on the back of the head / cheek at about (735-880, 330-450), the snout ending at the right at about "
            "x 1140 with the small amber crystal nose horn at about (1080-1140, 375-460), the zigzag mouth line with small teeth, the cream "
            "lower jaw down to about y 560",
            "draw it WITHOUT the eye: where the yellow eye is (about (985-1035, 405-445)), plain brown face skin with the heavy brow line "
            "kept above it. Its back and bottom, hidden behind the neck, continue as a rounded back of the head and a rounded throat line "
            "(the neck is not drawn)"),
           ("duoi", "the TAIL at the left: from the hips at about x 600 going left and curving UP to the rounded tip at about (295, 550), "
            "brown with its ochre-and-dark stripes, the cream underside, and the TWO small striped cream plates standing on top of it at "
            "about (420-495, 605-655) and (335-395, 560-605) (the plate at the hips at about (525-600, 612-668) is NOT part of the tail: "
            "leave it out)",
            "complete its root, hidden behind the hips and the near back leg, as a thick rounded tail base reaching right to about x 640")],
    "T3": [("chan_gan", "the NEAR BACK LEG at the lower left: the brown thigh at the hip (about (500-640, 640-760)), the shin going down-left "
            "and the foot with its dark-brown claws at about (440-585, 835-895)",
            "complete its top, hidden behind the tail and the belly, as a rounded thigh"),
           ("tay_xa", "the FAR FRONT LEG at the right: from the right side of the chest at about (880-950, 640) going down-right to the foot "
            "with its dark-brown claws at about (995-1120, 820-895)", "complete its top, hidden behind the chest, as a rounded shoulder")],
    "T4": [("tay_gan", "the NEAR FRONT LEG (the leg in front of the belly, left of the middle): from the shoulder at about (760-860, 640) "
            "down to the foot with its dark-brown claws at about (715-835, 845-905)",
            "complete its top, hidden behind the chest, as a rounded shoulder"),
           ("pa", "the BIG striped back plate just behind the neck: about x 705-815, y 482-560, cream with ochre bands", VIEN),
           ("pc", "the SMALL striped back plate at the hips: about x 525-600, y 612-668, cream with ochre bands", VIEN)],
    # người dùng 2026-11-17 (xem.html, dáng gầm): "sao bạn không tách hàm ra để há mồm được": đầu không hàm dưới + hàm dưới riêng
    "T6": [("dau_tren", "the HEAD WITHOUT ITS LOWER JAW: the two short cream stone horns, the striped cream-and-ochre cheek plate on the back of "
            "the head (about (735-880, 330-450)), the brown face and snout ending at the right at about x 1140, the small amber crystal nose "
            "horn (about (1080-1140, 375-460)), the brow line, and the cream UPPER LIP running from the mouth corner at about (878, 452) to "
            "the snout at about (1088, 517) with its small pointed teeth pointing DOWN along the zigzag mouth line; the brown back of the "
            "head and cheek behind the mouth corner down to about y 560",
            "draw it WITHOUT the eye (plain brown face skin where the yellow eye is, the brow line kept) and WITHOUT the lower jaw: "
            "everything below the zigzag line of the upper teeth (the cream lower jaw and the chin) is removed, so the lower edge of the "
            "head in front of the mouth corner IS the row of upper teeth (outlined in ink); no red or pink flesh, no tongue, no gums under "
            "the upper teeth; behind the mouth corner, the back of the head and cheek end in a rounded throat line (the neck is not drawn)")],
    "T7": [("ham", "the LOWER JAW ONLY, in exactly the place of the lower jaw in image 1 (below the zigzag mouth line): the cream lower jaw "
            "from the mouth corner at about (878, 465) to the chin at about (1080, 545), its bottom edge down to about y 560, with a row of "
            "small cream teeth pointing UP along its top edge exactly where the zigzag line is, and ON TOP of the jaw, just inside those "
            "teeth, a NARROW dark red-brown (#7A2E26) band of the mouth floor (about 16 px tall) following the jaw",
            "the back end of the jaw at the mouth corner is a rounded end (it turns there, hidden behind the cheek); nothing else of the "
            "head: no upper teeth, no face, no horns, no eye")],
    "T5": [("chan_xa", "the FAR BACK LEG (half hidden, between the near front leg and the far front leg): the brown leg and the foot with its "
            "dark-brown claws at about (760-890, 730-880)", "complete its hidden upper part, behind the belly and the near front leg, as a "
            "rounded thigh reaching up to about y 690"),
           ("pb", "the MIDDLE striped back plate: about x 608-708, y 545-612, cream with ochre bands", VIEN)],
}
ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a young sandstone drake walking on four legs, turned to the "
        "right: a brown head with two short cream stone horns, a striped cream cheek plate, a fierce yellow slit-pupil eye, a small amber "
        "crystal nose horn, a zigzag mouth with small teeth, a dark brown neck, dusty brown skin, a cream throat, chest and belly, three "
        "striped cream plates along the back, a long striped tail curling up at the left with small plates, four legs with dark-brown "
        "claws. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")


def prompt_manh():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ trên concept duyệt (2026-11-17, agent dạng 1)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(NAN)}`: concept duyệt (1536 × 1024, nền trắng). Mỗi tờ vài mảnh không chạm nhau, đúng chỗ, đúng "
          "cỡ, vẽ đủ phần bị che. Mắt Claude cắt thẳng từ concept, mắt nhắm dựng từ mặt nạ mắt. Gen: `py -3 -I ArtGen/Spine/gen_magnific.py "
          "<file>` (95 credit / tờ).", ""]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(NAN)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap (at least 20 px) "
             "between the kept parts: where two kept parts would touch, shorten the hidden portion rather than letting them touch.",
             "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(x for x, _, _ in ds)}): chỉ gửi đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (`rong_cat_non_manh.py ghep`); phần bị che vẽ đủ, viền kín; đầu không còn mắt; nền "
           "trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ================================================================ cắt, mắt, ghép (như than_lan_cat_2_manh)
def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


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


def khu_vien(rgb, mm, r=2):
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def luu_manh(A, m, ten, DATJ, nguon):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=nguon)
    return x0, y0, x1, y1


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd)) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    os.makedirs(MANH, exist_ok=True)
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w"), indent=1)


def cat(chi=None):
    DATJ = nap_dat()
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        slots = [x for x, _, _ in ds]
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = [i for i in range(1, n) if st[i, 4] > 30]
        gan = {x: [] for x in slots}
        for i in cum:
            c = cen[i]
            best = min(slots, key=lambda x: np.hypot(c[0] - TAM[x][0], c[1] - TAM[x][1]))
            d = np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1])
            if d < 260 or st[i, 4] > 20000:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {st[i, 4]} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for x, ids in gan.items():
            if not ids:
                print(f"  {x:10s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, np.isin(lab, ids), x, DATJ, os.path.basename(src))
            big = max(ids, key=lambda i: st[i, 4])
            print(f"  {x:10s} hộp {b}, {len(ids)} cụm (to nhất {st[big, 4]} px, tâm {cen[big][0]:.0f},{cen[big][1]:.0f})")
    ghi_dat(DATJ)


MAT_HOP = (965, 392, 1050, 458)


def mat():
    """mắt mở cắt thẳng từ concept (bao lồi vùng vàng + con ngươi + chấm sáng, nới 5 px lấy vành mực); mắt nhắm dựng từ cùng mặt nạ: tô màu
    da mặt + một nét mực cong xuống ngang giữa (mí khép)."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(NAN).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = A[y0:y1, x0:x1]
    vang = (sub[..., 0] > 205) & (sub[..., 1] > 150) & (sub[..., 2] < 110) & (sub[..., 0] - sub[..., 2] > 120)
    vang = cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_CLOSE, el(10))
    n, lab, st, _ = cv2.connectedComponentsWithStats(vang, 8)
    ids = [i for i in range(1, n) if st[i, 4] > 80]
    m = np.zeros_like(vang)
    hulls = []
    for i in ids:
        ys, xs = np.nonzero(lab == i)
        hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        cv2.fillPoly(m, [hull], 1)
        hulls.append(hull.reshape(-1, 2) + np.array([x0, y0]))
    m = cv2.dilate(m, el(5)).astype(bool)
    full = np.zeros((H, W), bool)
    full[y0:y1, x0:x1] = m
    print("mat", luu_manh(A, full, "mat", DATJ, "L1_duyet.png (cắt thẳng)"), f"{len(ids)} cụm vàng")
    hx0, hy0, hx1, hy1 = DATJ["mat"]["hop"]
    im = np.asarray(Image.open(os.path.join(MANH, "mat.png")).convert("RGBA")).copy()
    # da mặt: trung vị điểm nâu quanh mắt trong concept
    vung = A[max(0, hy0 - 10):hy1 + 10, max(0, hx0 - 10):hx1 + 10].reshape(-1, 3)
    nau = vung[(vung[:, 0] > 120) & (vung[:, 0] < 200) & (vung[:, 2] < 110) & (vung[:, 0] - vung[:, 2] > 40) & (vung[:, 1] < 150)]
    da = np.median(nau, 0).astype(np.uint8) if len(nau) > 20 else np.array([150, 104, 70], np.uint8)
    al = im[..., 3] > 0
    trong = cv2.erode(al.astype(np.uint8), el(5)).astype(bool)
    im[trong, :3] = da
    can = Image.fromarray(im, "RGBA")
    d = ImageDraw.Draw(can)
    for hull in hulls:
        hx = hull[:, 0] - hx0
        hy = hull[:, 1] - hy0
        xa, xb, ym = hx.min() + 2, hx.max() - 2, (hy.min() + hy.max()) / 2
        pts = [(xa + (xb - xa) * u, ym + 0.22 * (hy.max() - hy.min()) * np.sin(np.pi * u)) for u in np.linspace(0, 1, 12)]
        d.line(pts, fill=(43, 33, 24, 255), width=6, joint="curve")
    can.save(os.path.join(MANH, "mat_nham.png"))
    DATJ["mat_nham"] = dict(hop=DATJ["mat"]["hop"], nguon=f"dựng từ mặt nạ mắt (tô da {da.tolist()} + mí)")
    ghi_dat(DATJ)


THU_TU = ["tay_xa", "chan_xa", "duoi", "than", "pc", "pb", "pa", "chan_gan", "tay_gan", "ham", "dau_tren", "mat"]


def ghep():
    DATJ = nap_dat()
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for x in THU_TU:
        if x not in DATJ:
            thieu.append(x)
            continue
        x0, y0, _, _ = DATJ[x]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, x + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(NAN).convert("RGB").resize((W, H))).astype(np.int32)
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
    pp = os.path.join(MANH, "_ghep.png")
    out.save(pp)
    can.convert("RGB").save(os.path.join(MANH, "_ghep_to.png"))
    print(pp, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")




def noi_vai(ten="tay_xa", L=80):
    """mảnh chân GPT cắt thẳng ở đầu trên (không viền, đầu bị khuất sau thân trong concept): nối dài theo trục chân một khúc L px có đầu
    tròn, tô bằng vân lấy từ giữa chân, viền mực hai bên + đầu tròn; mép hở cũ không có viền nên liền màu. Giữ bản gốc ở <ten>_goc.png."""
    DATJ = nap_dat()
    if f"{ten}_goc" not in DATJ:
        Image.open(os.path.join(MANH, ten + ".png")).save(os.path.join(MANH, ten + "_goc.png"))
        DATJ[f"{ten}_goc"] = dict(DATJ[ten])
    im = np.asarray(Image.open(os.path.join(MANH, ten + "_goc.png")).convert("RGBA")).copy()
    x0, y0, x1, y1 = DATJ[f"{ten}_goc"]["hop"]
    a = im[..., 3] > 128
    h, w = a.shape
    ys, xs = np.nonzero(a)
    # mép hở = điểm biên của mặt nạ KHÔNG có mực (sáng) ở nửa trên
    bien = a & ~cv2.erode(a.astype(np.uint8), el(1)).astype(bool)
    sang = im[..., :3].astype(np.int32).mean(2) > 95                 # không phải mực (mực ~ 33, da nâu ~ 140)
    ho = bien & sang & (np.arange(h)[:, None] < 0.4 * h)
    hy, hx = np.nonzero(ho)
    if len(hx) < 5:
        print(ten, "không thấy mép hở")
        return
    P = np.stack([hx, hy], 1).astype(float)
    c = P.mean(0)
    u, s, vt = np.linalg.svd(P - c)
    e = vt[0]
    t = (P - c) @ e
    A, B = c + e * t.min(), c + e * t.max()
    chan = np.stack([xs, ys], 1)[ys > 0.7 * h].mean(0)
    d = (A + B) / 2 - chan
    d /= np.linalg.norm(d)
    r = np.linalg.norm(B - A) / 2
    pad = int(L + r + 12)
    H2, W2 = h + 2 * pad, w + 2 * pad
    o = np.array([pad, pad], float)
    A2, B2 = A + o, B + o
    pts = [A2, B2, B2 + d * L, A2 + d * L]
    can = np.zeros((H2, W2, 4), np.uint8)
    poly = np.zeros((H2, W2), np.uint8)
    cv2.fillPoly(poly, [np.round(pts).astype(np.int32)], 1)
    cv2.circle(poly, tuple(np.round((A2 + B2) / 2 + d * L).astype(int)), int(round(r)), 1, -1)
    # vân: ô 40 × 40 nằm trọn trong chân, không dính mực (dò lưới), lát kín
    lum = im[..., :3].astype(np.int32).mean(2)
    o_v = None
    for yy in range(0, h - 40, 6):
        for xx in range(0, w - 40, 6):
            if (im[yy:yy + 40, xx:xx + 40, 3] > 250).all() and lum[yy:yy + 40, xx:xx + 40].min() > 95:
                o_v = im[yy:yy + 40, xx:xx + 40, :3]
                break
        if o_v is not None:
            break
    if o_v is None:
        o_v = np.tile(np.median(im[a & sang][:, :3], 0).astype(np.uint8), (40, 40, 1))
    lat = np.tile(o_v, (H2 // 40 + 1, W2 // 40 + 1, 1))[:H2, :W2]
    trong = poly.astype(bool)
    can[trong, :3] = lat[trong]
    can[trong, 3] = 255
    vien = cv2.dilate(poly, el(7)).astype(bool) & ~cv2.erode(poly, el(0)).astype(bool)
    gy2, gx2 = np.mgrid[0:H2, 0:W2]                                               # không kẻ viền đè lên mảnh gốc, nhất là dọc mép hở
    ab2 = B2 - A2
    tt2 = np.clip(((gx2 - A2[0]) * ab2[0] + (gy2 - A2[1]) * ab2[1]) / max(1e-6, ab2 @ ab2), 0.0, 1.0)
    dd2 = np.hypot(gx2 - (A2[0] + tt2 * ab2[0]), gy2 - (A2[1] + tt2 * ab2[1]))
    vien &= ~np.pad(im[..., 3] > 0, pad) & ~((dd2 < 6) & (tt2 > 0.08) & (tt2 < 0.92))
    can[vien, :3] = (43, 33, 24)
    can[vien, 3] = 255
    goc = np.zeros((H2, W2, 4), np.uint8)
    goc[pad:pad + h, pad:pad + w] = im
    gy, gx = np.mgrid[0:h, 0:w]                                                   # mép hở cũ (đoạn A–B) hơi sẫm: tô lại bằng vân
    ab = B - A
    tt = np.clip(((gx - A[0]) * ab[0] + (gy - A[1]) * ab[1]) / max(1e-6, ab @ ab), 0.06, 0.94)
    dd = np.hypot(gx - (A[0] + tt * ab[0]), gy - (A[1] + tt * ab[1]))
    xoa = np.pad((dd < 7) & (im[..., 3] > 0), pad)
    goc[xoa, :3] = lat[xoa]
    out = Image.fromarray(can, "RGBA")
    out.alpha_composite(Image.fromarray(goc, "RGBA"))
    arr = np.asarray(out)
    ys2, xs2 = np.nonzero(arr[..., 3] > 0)
    arr = arr[ys2.min():ys2.max() + 1, xs2.min():xs2.max() + 1]
    Image.fromarray(arr, "RGBA").save(os.path.join(MANH, ten + ".png"))
    nx0, ny0 = x0 - pad + int(xs2.min()), y0 - pad + int(ys2.min())
    DATJ[ten] = dict(hop=[nx0, ny0, nx0 + arr.shape[1], ny0 + arr.shape[0]], nguon=DATJ[f"{ten}_goc"]["nguon"] + f" (nối vai {L} px)")
    ghi_dat(DATJ)
    print(ten, "nối vai", DATJ[ten]["hop"], "hướng", np.round(d, 2), "mép hở", np.round(A), np.round(B))





def _bo_vien_noi(ten, vung, DATJ, fg, dist, mo_rong, mo_mat, sau=10.0):
    """xoá viền mực ở mép mảnh `ten` nằm SÂU trong hình bóng con vật (dist > 10 px tới nền concept) trong `vung` (hàm (X, Y) toạ độ concept →
    bool), chỉ nét giáp da nâu (không giáp mảng kem: phiến má, sừng, răng giữ viền); tô lại bằng màu da lân cận (inpaint). Rồi nới da mảnh
    ra `mo_rong` px trong vùng đó (chỉ trong hình bóng, sâu > 8 px), alpha mờ dần theo khoảng cách (mo_mat: lũy thừa)."""
    goc_ten = f"{ten}_truoc_noi"
    if goc_ten not in DATJ:
        Image.open(os.path.join(MANH, ten + ".png")).save(os.path.join(MANH, goc_ten + ".png"))
        DATJ[goc_ten] = dict(DATJ[ten])
    im = np.asarray(Image.open(os.path.join(MANH, goc_ten + ".png")).convert("RGBA")).copy()
    x0, y0, x1, y1 = DATJ[goc_ten]["hop"]
    pad = mo_rong + 4
    h, w = im.shape[:2]
    H2, W2 = h + 2 * pad, w + 2 * pad
    big = np.zeros((H2, W2, 4), np.uint8)
    big[pad:pad + h, pad:pad + w] = im
    gx0, gy0 = x0 - pad, y0 - pad
    yy, xx = np.mgrid[0:H2, 0:W2]
    GX, GY = xx + gx0, yy + gy0
    trong = (GX >= 0) & (GX < W) & (GY >= 0) & (GY < H)
    fgl = np.zeros((H2, W2), bool)
    dl = np.zeros((H2, W2), np.float32)
    fgl[trong] = fg[GY[trong], GX[trong]]
    dl[trong] = dist[GY[trong], GX[trong]]
    vz = vung(GX, GY)
    m = big[..., 3] > 128
    rgb = big[..., :3].copy()
    lum = rgb.astype(np.int32).mean(2)
    nau = m & (lum > 85) & (lum < 185) & ((rgb[..., 0].astype(int) - rgb[..., 2].astype(int)) > 30)
    kem = m & (lum >= 185)
    d_nau = cv2.distanceTransform((~nau).astype(np.uint8), cv2.DIST_L2, 5)
    d_kem = cv2.distanceTransform((~kem).astype(np.uint8), cv2.DIST_L2, 5)
    bien = m & ~cv2.erode(m.astype(np.uint8), el(9)).astype(bool)
    xoa = bien & (lum < 115) & vz & (dl > sau) & (d_nau < 12) & (d_kem > 9)
    xoa = cv2.dilate(xoa.astype(np.uint8), el(1)).astype(bool) & m
    d_ra = cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5)
    E = (~m) & (d_ra <= mo_rong) & vz & fgl & (dl > 8)
    # mực còn sát vùng nới (trong mảnh, trong vùng, không giáp kem) cũng bỏ, kẻo thành vệt giữa da cũ và da nới
    muc_sat = m & (lum < 115) & vz & (d_kem > 9) & cv2.dilate(E.astype(np.uint8), el(12)).astype(bool)
    xoa |= muc_sat
    # tô lại: chỉ lấy màu từ DA trong mảnh (ngoài mảnh trong suốt có RGB đen; mực cũng không làm nguồn)
    chua_biet = (~m) | xoa
    lap = cv2.inpaint(rgb, chua_biet.astype(np.uint8), 7, cv2.INPAINT_TELEA)
    big[xoa, :3] = lap[xoa]
    big[xoa, 3] = 255
    if E.any():
        big[E, :3] = lap[E]
        a = np.clip(1.0 - d_ra / float(mo_rong), 0, 1) ** mo_mat
        big[E, 3] = np.maximum(big[E, 3], (255 * a[E]).astype(np.uint8))
    ys, xs = np.nonzero(big[..., 3] > 0)
    big = big[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(big, "RGBA").save(os.path.join(MANH, ten + ".png"))
    nx0, ny0 = gx0 + int(xs.min()), gy0 + int(ys.min())
    DATJ[ten] = dict(hop=[nx0, ny0, nx0 + big.shape[1], ny0 + big.shape[0]], nguon=DATJ[goc_ten]["nguon"] + f" (bỏ viền nối, nới {mo_rong} px)")
    print(ten, "bỏ viền", int(xoa.sum()), "px, nới", int(E.sum()), "px →", DATJ[ten]["hop"])


def noi_co():
    """người dùng 2026-11-17: "thân vẫn bị hở giữa thân và đầu, bỏ outline đoạn nối thân và đầu đi". Chỗ nối cổ–đầu thành da LIỀN: bỏ viền
    mép dưới / sau mảnh đầu nằm trên cổ (sau góc miệng, dưới phiến má) + nới da đầu xuống phủ cổ 30 px mờ dần; bỏ viền mép trên cổ nằm dưới
    đầu + nới cổ lên dưới đầu 34 px (đủ phủ khe khi đầu ngẩng / cúi)."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(NAN).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = ~nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_CLOSE, el(6)).astype(bool)
    dist = cv2.distanceTransform(fg.astype(np.uint8), cv2.DIST_L2, 5)
    _bo_vien_noi("dau_tren", lambda X, Y: (X < 905) & (Y > 395), DATJ, fg, dist, 30, 1.6)
    _bo_vien_noi("than", lambda X, Y: (X > 735) & (X < 965) & (Y < 520), DATJ, fg, dist, 34, 0.6, sau=-1.0)   # mép trên cổ khuất sau đầu: bỏ hết viền
    ghi_dat(DATJ)





def _goc_cua(ten, DATJ):
    """bản gốc (trước mọi lần bỏ viền) của mảnh: <ten>_truoc_noi.png nếu có, không thì lưu bản hiện tại làm gốc."""
    g = f"{ten}_truoc_noi"
    if g not in DATJ:
        Image.open(os.path.join(MANH, ten + ".png")).save(os.path.join(MANH, g + ".png"))
        DATJ[g] = dict(DATJ[ten])
    return np.asarray(Image.open(os.path.join(MANH, g + ".png")).convert("RGBA")).copy(), DATJ[g]["hop"]


def noi_theo_concept(ten, DATJ, A, fg, dist, mo=12.0, vung=None, sach=None, mat_trong=False, nguong_muc=110):
    """chuẩn là concept duyệt: ở MÉP mảnh nằm trong hình bóng con vật (sâu > 6 px) mà concept KHÔNG có nét mực ở đó (trong 5 px) — tức mép
    là phần GPT vẽ thêm cho chỗ khuất (đỉnh vai, đùi, gáy, gốc đuôi) — thì xoá viền, tô da (chỉ lấy màu từ da trong mảnh) và làm MỜ mép đó
    vào trong `mo` px để hoà vào lớp dưới như da liền. Mép trùng nét concept (đường bao ngoài, viền phiến, răng) giữ nguyên.
    vung: hàm (X, Y) → bool giới hạn chỗ xét; sach: hàm (X, Y) → bool chỗ bỏ HẾT viền (khuất sau mảnh khác, vd đỉnh cổ dưới đầu)."""
    im, (x0, y0, x1, y1) = _goc_cua(ten, DATJ)
    h, w = im.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    GX, GY = xx + x0, yy + y0
    ok = (GX >= 0) & (GX < W) & (GY >= 0) & (GY < H)
    lumC = A.mean(2)
    mucC = cv2.dilate((lumC < nguong_muc).astype(np.uint8), el(5)).astype(bool)
    cm = np.zeros((h, w), bool)
    dl = np.zeros((h, w), np.float32)
    cm[ok] = mucC[GY[ok], GX[ok]]
    dl[ok] = dist[GY[ok], GX[ok]]
    vz = vung(GX, GY) if vung else np.ones((h, w), bool)
    m = im[..., 3] > 128
    rgb = im[..., :3].copy()
    lum = rgb.astype(np.int32).mean(2)
    bien = m & ~cv2.erode(m.astype(np.uint8), el(9)).astype(bool)
    from scipy import ndimage
    if mat_trong:
        # mép "quay vào trong": nhìn ra ngoài mảnh 6–12 px, concept ở đó là thân con vật sâu > 10 px (không phải nền, không phải nét bao)
        # → mép nằm đè lên bộ phận khác: viền là viền nối, bỏ. Mép quay ra nền (đường bao ngoài) giữ nguyên.
        ring = cv2.dilate(m.astype(np.uint8), el(12)).astype(bool) & ~cv2.dilate(m.astype(np.uint8), el(6)).astype(bool)
        dl_ngoai = np.zeros((h, w), np.float32)
        dl_ngoai[ok] = dist[GY[ok], GX[ok]]
        _, (ry, rx) = ndimage.distance_transform_edt(~ring, return_indices=True)
        trong = cv2.blur((dl_ngoai[ry, rx] > 10).astype(np.float32), (9, 9)) > 0.5
        xoa = bien & (lum < 120) & vz & trong & ~cm
        xoa = cv2.morphologyEx(xoa.astype(np.uint8), cv2.MORPH_CLOSE, el(10)).astype(bool) & bien & (lum < 120) & vz & trong
    else:
        trong = dl > 8
        xoa = bien & (lum < 120) & vz & (dl > 6) & ~cm
        # liền mạch: các khúc giữ lại ngắn kẹp giữa những khúc xoá (gần nét bộ phận khác trong concept) cũng xoá, kẻo viền còn lổn nhổn
        xoa = cv2.morphologyEx(xoa.astype(np.uint8), cv2.MORPH_CLOSE, el(10)).astype(bool) & bien & (lum < 120) & vz & (dl > 4)
    if sach:
        xoa |= bien & (lum < 120) & sach(GX, GY) & (dl > 8)          # giữ đường bao ngoài (họng, gáy) dù trong vùng khuất
    # nở theo vệt tối liền (viền GPT dày 10–12 px, dày hơn dải biên): tới hết điểm khử răng cưa phía trong, kẻo còn chỉ nâu mảnh
    toi_l = (lum < 128) & m
    for _ in range(6):
        xoa = xoa | (cv2.dilate(xoa.astype(np.uint8), el(1)).astype(bool) & toi_l)
    xoa = cv2.dilate(xoa.astype(np.uint8), el(1)).astype(bool) & m
    # sợi mực mảnh còn sót sát chỗ xoá (mép khử răng cưa, chỗ chuyển giữ / bỏ): mảnh hơn 4 px thì bỏ nốt, kẻo thành chỉ đen
    con = bien & (lum < 128) & ~xoa & m
    day = cv2.dilate(cv2.erode(con.astype(np.uint8), el(2)), el(3)).astype(bool)
    xoa |= con & ~day & cv2.dilate(xoa.astype(np.uint8), el(5)).astype(bool)
    for _ in range(4):                                                   # nở lại qua vệt tối liền sau bước trên
        xoa = xoa | (cv2.dilate(xoa.astype(np.uint8), el(1)).astype(bool) & toi_l)
    # tô: chép điểm DA gần nhất phía trong (cách mép > 10 px, không thuộc vùng xoá) — giữ vân sáp, không nhoè thành vòng như inpaint
    d_mep = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    # nguồn: da thật, cách mọi điểm tối (viền, khử răng cưa của viền: lum < 118) ≥ 4 px — kẻo chép điểm nửa mực thành vòng nâu sẫm
    toi = cv2.dilate((lum < 118).astype(np.uint8), el(4)).astype(bool)
    nguon = m & ~xoa & (d_mep > 8) & ~toi
    if nguon.any():
        _, (iy, ix) = ndimage.distance_transform_edt(~nguon, return_indices=True)
        # chép VÂN: lấy điểm sâu thêm 12 px theo hướng vào trong (từ điểm cần tô tới điểm da gần nhất) — giữ nét sáp chéo, không ra mảng
        # trơn / vệt toả tia như chép điểm gần nhất
        vy, vx = (iy - yy).astype(np.float32), (ix - xx).astype(np.float32)
        nn = np.maximum(np.hypot(vy, vx), 1e-3)
        sy = np.clip(np.round(iy + 12.0 * vy / nn).astype(int), 0, h - 1)
        sx = np.clip(np.round(ix + 12.0 * vx / nn).astype(int), 0, w - 1)
        hop_le = nguon[sy, sx]
        sy = np.where(hop_le, sy, iy)
        sx = np.where(hop_le, sx, ix)
        lap = rgb[sy, sx]
    else:
        lap = cv2.inpaint(rgb, ((~m) | xoa).astype(np.uint8), 7, cv2.INPAINT_TELEA)
    # độ sáng vùng tô theo da quanh đó (trung bình cục bộ 10 px của da nâu không sát mực): chép điểm gần nhất hay vớ phải da sáng
    # sát viền (GPT tô sáng mép trong viền) thành mảng loang sáng
    nau_l = ((lap[..., 0].astype(int) - lap[..., 2].astype(int)) > 30) & (lap.astype(np.int32).mean(2) < 190)
    ref = m & ~xoa & ~toi & ((rgb[..., 0].astype(int) - rgb[..., 2].astype(int)) > 30) & (lum > 85) & (lum < 190)
    if ref.sum() > 200 and (xoa & nau_l).any():
        def _tb(arr, msk):
            S = cv2.GaussianBlur(arr * msk[..., None], (0, 0), 10)
            N = cv2.GaussianBlur(msk.astype(np.float32), (0, 0), 10)[..., None]
            return S / np.maximum(N, 1e-3), N[..., 0]
        lapf = lap.astype(np.float32)
        tb_ref, n_ref = _tb(rgb.astype(np.float32), ref.astype(np.float32))
        tb_lap, n_lap = _tb(lapf, (xoa & nau_l).astype(np.float32))
        # chỉ chỉnh nơi có đủ da tham chiếu quanh đó (không thì trung bình rỗng ≈ 0 kéo màu tô thành đen)
        tin = np.clip((n_ref - 0.03) / 0.10, 0, 1) * (n_lap > 0.02)
        q = xoa & nau_l
        lapf[q] = lapf[q] + tin[q][:, None] * (tb_ref[q] - tb_lap[q])
        lap = np.clip(lapf, 0, 255).astype(np.uint8)
    im[xoa, :3] = lap[xoa]
    # đầu mút viền GIỮ LẠI sát chỗ xoá: vuốt nhạt dần sang da trong 12 px, kẻo đứt cụt thành bậc / mẩu lổn nhổn
    if xoa.any():
        dx = cv2.distanceTransform((~xoa).astype(np.uint8), cv2.DIST_L2, 5)
        giu = m & ~xoa & (lum < 128) & (dx < 12.0) & bien & trong     # chỉ đầu mút nằm TRONG thân; đường bao ngoài không vuốt nhạt
        if giu.any():
            t = (1.0 - dx / 12.0)[giu][:, None]
            im[giu, :3] = np.clip(im[giu, :3].astype(np.float32) * (1 - t) + lap[giu].astype(np.float32) * t, 0, 255).astype(np.uint8)
    # vòng mép bán trong suốt (khu_vien làm tối) quanh chỗ xoá: cắt hẳn (alpha 0), kẻo thành chỉ mảnh
    gan_xoa = cv2.dilate(xoa.astype(np.uint8), el(4)).astype(bool)
    gan_xoa8 = cv2.dilate(xoa.astype(np.uint8), el(8)).astype(bool)
    im[(~m) & gan_xoa8, 3] = 0
    # điểm nửa trong suốt mà sẫm (bóng mờ đen ở đầu mút viền giữ lại) sát chỗ xoá: tô màu da, kẻo thành vệt đen loang
    loang = m & gan_xoa8 & (im[..., 3] < 235) & (im[..., :3].astype(np.int32).mean(2) < 100)
    im[loang, :3] = lap[loang]
    vanh = m & (d_mep <= 3.5) & gan_xoa & (lap.astype(np.int32).mean(2) < 180)
    im[vanh, :3] = lap[vanh]
    # khớp màu da với concept (GPT tô mảnh chân hơi sáng hơn thân): nhân từng kênh theo trung vị da trùng chỗ
    nauP = m & (lum > 85) & (lum < 185) & ((rgb[..., 0].astype(int) - rgb[..., 2].astype(int)) > 30)
    Cl = np.zeros((h, w, 3), np.float32)
    Cl[ok] = A[GY[ok], GX[ok]]
    lC = Cl.mean(2)
    nauC = (lC > 85) & (lC < 185) & ((Cl[..., 0] - Cl[..., 2]) > 30)
    chung = nauP & nauC & (dl > 8)
    if chung.sum() > 400:
        k = np.median(Cl[chung], 0) / np.maximum(1.0, np.median(im[..., :3][chung].astype(np.float32), 0))
        k = np.clip(k, 0.8, 1.25)
        sua = (im[..., 3] > 0) & ((im[..., :3].astype(np.int32).mean(2) > 85)) & ((im[..., 0].astype(int) - im[..., 2].astype(int)) > 30) &               (im[..., :3].astype(np.int32).mean(2) < 190)
        im[sua, :3] = np.clip(im[sua, :3].astype(np.float32) * k, 0, 255).astype(np.uint8)
    # mép "nối" = điểm biên mặt nạ thuộc vùng vừa xoá viền; mờ dần vào trong mo px tính từ mép nối
    bien1 = m & ~cv2.erode(m.astype(np.uint8), el(1)).astype(bool)
    mep_noi = bien1 & cv2.dilate(xoa.astype(np.uint8), el(2)).astype(bool)
    if mep_noi.any():
        d = cv2.distanceTransform((~mep_noi).astype(np.uint8), cv2.DIST_L2, 5)
        # điểm sẫm (đầu mút viền giữ lại) trong dải mờ: tô da trước khi mờ, kẻo mờ ra thành vệt đen loang
        sam = m & (d < mo) & (im[..., :3].astype(np.int32).mean(2) < 110)
        im[sam, :3] = lap[sam]
        f = np.clip(d / mo, 0.0, 1.0)
        f = f * f * (3 - 2 * f)
        a = im[..., 3].astype(np.float32) * np.where(m, f, 1.0)
        im[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
    Image.fromarray(im, "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=DATJ[f"{ten}_truoc_noi"]["nguon"] + f" (bỏ viền nối theo concept, mờ {mo:.0f} px)")
    print(f"{ten}: bỏ {int(xoa.sum())} px viền nối, mép nối {int(mep_noi.sum())} px")


def cat_hong(DATJ, y_het=738.0, x_het=600.0):
    """đùi chân sau gần (vẽ TRƯỚC thân) lồi ra sau đường hông của thân ~10–30 px và che mất nét hông: concept có MỘT nét hông chạy
    từ phiến lưng xuống chân (đuôi mọc từ sau hông). Ở vùng hông (trên y_het, trước x_het) cắt đùi ngay trong dải viền sau của thân
    để nét hông của thân lộ ra, đùi chỉ phủ phần da bên trong. Dưới y_het đùi giữ nguyên (mép sau cẳng chân là đường bao)."""
    g = np.array(Image.open(os.path.join(MANH, "chan_gan.png")).convert("RGBA"))
    gx0, gy0 = DATJ["chan_gan"]["hop"][:2]
    t = np.array(Image.open(os.path.join(MANH, "than.png")).convert("RGBA"))
    tx0, ty0 = DATJ["than"]["hop"][:2]
    h, w = g.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    GX, GY = xx + gx0, yy + gy0
    tx, ty = GX - tx0, GY - ty0
    ok = (tx >= 0) & (tx < t.shape[1]) & (ty >= 0) & (ty < t.shape[0])
    T = np.zeros((h, w, 4), np.uint8)
    T[ok] = t[ty[ok], tx[ok]]
    tb = T[..., 3] > 128
    tl = T[..., :3].astype(np.int32).mean(2)
    d_in = cv2.distanceTransform(tb.astype(np.uint8), cv2.DIST_L2, 5)
    vien = tb & (tl < 118) & (d_in < 16)
    vien = cv2.dilate(vien.astype(np.uint8), el(1)).astype(bool)
    trong = tb & ~vien & (d_in > 4)
    vung = (GY < y_het) & (GX < x_het)
    bo = vung & ~trong & (g[..., 3] > 0)
    # mép cắt mềm 1,5 px; hai đầu vùng (gần y_het, x_het) hoà dần 6 px cho khỏi thành bậc
    d = cv2.distanceTransform((~bo).astype(np.uint8), cv2.DIST_L2, 5)
    f = np.clip(d / 1.5, 0, 1)
    ra = np.clip((y_het - GY) / 6.0, 0, 1) * np.clip((x_het - GX) / 6.0, 0, 1)
    f = 1.0 - (1.0 - f) * ra
    g[..., 3] = (g[..., 3].astype(np.float32) * f).astype(np.uint8)
    Image.fromarray(g, "RGBA").save(os.path.join(MANH, "chan_gan.png"))
    print(f"chan_gan: cắt {int(bo.sum())} px lồi qua nét hông của thân")


def noi_da():
    """người dùng 2026-11-17: "bỏ outline đoạn nối thân và đầu đi", "làm kĩ vào để không phải sửa đi sửa lại nhiều". Mọi chỗ nối hai mảnh
    của cùng khối da thành da liền theo concept: gáy đầu → cổ, đỉnh vai chân trước gần, đùi chân sau gần, đỉnh hai chân xa, gốc đuôi; đỉnh cổ
    (khuất sau đầu) bỏ hết viền. Thay cho noi_co (bản nới da mờ làm nhoè gáy, phủ lên phiến lưng)."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(NAN).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = cv2.morphologyEx((~nen(A)).astype(np.uint8), cv2.MORPH_CLOSE, el(6)).astype(bool)
    dist = cv2.distanceTransform(fg.astype(np.uint8), cv2.DIST_L2, 5)
    # mép nối gần như ĐỤC (mờ 5–8 px): màu đã khớp nên không thấy đường nối; mờ rộng thì khi chi quay ra khỏi thân lộ lớp dưới thành vệt nhoè
    # gáy / đáy đầu đè lên cổ: bỏ HẾT viền (người dùng: "bỏ outline đoạn nối thân và đầu"), trừ mép dưới phiến mang tai (x < 790)
    # mép đáy gáy quay vào cổ (concept ở ngoài mép là thân) bỏ viền; mép trái gáy quay ra nền (đường bao lưng cổ) giữ. Nét concept tính
    # là mực khi lum < 62: mảng bóng nâu sẫm ở gáy concept (lum 95–112, mép 70–82) không phải nét viền
    noi_theo_concept("dau_tren", DATJ, A, fg, dist, 8.0, vung=lambda X, Y: (X < 852) & (Y > 455), mat_trong=True, nguong_muc=62)
    # đầu mút viền đáy gáy còn sót thành gai nhọn chĩa ra sau ở góc phiến má (x 846–867) + vài điểm kem khử răng cưa: tô da (chép da
    # gáy cách 14 px về phía sau), góc phiến má giữ nguyên như concept
    g = np.array(Image.open(os.path.join(MANH, "dau_tren.png")).convert("RGBA"))
    x0_, y0_ = DATJ["dau_tren"]["hop"][:2]
    L = g[..., :3].astype(np.int32).mean(2)
    for yy_ in range(486 - y0_, 507 - y0_):
        for xx_ in range(846 - x0_, 873 - x0_):
            X_, Y_ = xx_ + x0_, yy_ + y0_
            if g[yy_, xx_, 3] < 10:
                continue
            gai = X_ <= 867 and L[yy_, xx_] < 128
            kem = X_ <= 872 and Y_ >= 494 and L[yy_, xx_] > 165
            if gai or kem:
                g[yy_, xx_, :3] = g[yy_, xx_ - 14, :3] if g[yy_, xx_ - 14, 3] > 200 else (150, 96, 64)
    Image.fromarray(g, "RGBA").save(os.path.join(MANH, "dau_tren.png"))
    # thân: chỉ đỉnh cổ khuất sau đầu (bỏ hết viền) và mép sau ở gốc đuôi; KHÔNG đụng mép lưng dưới phiến (làm mờ ở đó lọt nền trắng)
    # mép sau ở hông (gốc đuôi) GIỮ viền: concept có nét hông đè lên gốc đuôi (đuôi mọc từ sau hông); xoá thì thành mảng nâu lổn nhổn
    # đỉnh cổ: chỉ bỏ viền ở mép QUAY VÀO đầu (ngoài mép, concept là đầu / hàm); mép quay ra nền (nét lưng cổ sau gáy, mép trước họng
    # dưới hàm, x > 925: lúc nghỉ khuất sau hàm, khi đầu ngẩng / đi thì lộ) giữ — bỏ cả (bản "sach" cũ) thì họng lú ra dưới hàm thành
    # mép kem răng cưa không viền
    noi_theo_concept("than", DATJ, A, fg, dist, 6.0, vung=lambda X, Y: (X > 740) & (X < 925) & (Y < 540), mat_trong=True,
                     nguong_muc=62)
    noi_theo_concept("tay_gan", DATJ, A, fg, dist, 5.0)
    # đùi chân sau gần: bỏ cung đỉnh đùi (đè lên thân), GIỮ mép sau đùi đè lên gốc đuôi (concept có nét đó)
    noi_theo_concept("chan_gan", DATJ, A, fg, dist, 5.0, vung=lambda X, Y: (X > 548))
    cat_hong(DATJ)
    # mảnh nằm SAU thân (đuôi, hai chân xa): đỉnh / gốc vốn khuất dưới thân; xoá viền + làm mờ ở đó chỉ sinh lỗ nền khi lộ ra (soi walk,
    # attack): giữ nguyên bản (khi lộ ra ngoài thân, viền GPT là đường bao đúng)
    for ten in ("tay_xa", "chan_xa", "duoi"):
        g = f"{ten}_truoc_noi"
        if g in DATJ:
            Image.open(os.path.join(MANH, g + ".png")).save(os.path.join(MANH, ten + ".png"))
            DATJ[ten] = dict(DATJ[g])
            print(f"{ten}: giữ nguyên bản (mảnh sau thân)")
    # chân trước xa: phần nới vai (noi_vai) cao tới y 589 — khi cổ hạ theo đầu (walk) đỉnh vai lú lên trên nét lưng cổ thành cục có
    # viền. Đỉnh vai luôn khuất sau ngực: mờ dần về 0 ở trên y 636 (đục từ y 658), vẫn dư ~10 px so với mảnh gốc (y 660)
    g = np.array(Image.open(os.path.join(MANH, "tay_xa.png")).convert("RGBA"))
    x0_, y0_ = DATJ["tay_xa"]["hop"][:2]
    GYv = np.arange(g.shape[0])[:, None] + y0_
    f = np.clip((GYv - 636.0) / 22.0, 0, 1)
    f = f * f * (3 - 2 * f)
    g[..., 3] = (g[..., 3].astype(np.float32) * f).astype(np.uint8)
    Image.fromarray(g, "RGBA").save(os.path.join(MANH, "tay_xa.png"))
    print("tay_xa: mờ đỉnh vai trên y 636")
    ghi_dat(DATJ)



if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "mat":
        mat()
    elif cmd == "ghep":
        ghep()
    elif cmd == "prompt":
        prompt_manh()
    elif cmd == "noi_da":
        noi_da()
    elif cmd == "noi_co":
        noi_co()
    elif cmd == "vai":
        noi_vai(*(sys.argv[2:3] or ["tay_xa"]))
    else:
        print(__doc__)
