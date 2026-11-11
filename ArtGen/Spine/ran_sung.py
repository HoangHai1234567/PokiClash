# -*- coding: utf-8 -*-
"""Dòng rắn nước có sừng (mã tạm `ran_sung`, tướng thứ 5 đảo Thủy): RESKIN rig Spine gốc `monster_3247` (người dùng chốt 2026-11-11:
"xóa hết đi mà xây lại, gen y hệt con gốc rồi reskin thôi"). Giữ NGUYÊN xương, lưới, trọng số, thứ tự vẽ, animation của con gốc; chỉ
vẽ lại DA từng mảnh theo thiết kế của mình (GPT vẽ đè lên tờ mảnh gốc, giữ hình bóng từng mảnh). Giống cách dự án vẽ đè lên rig aola.

    py -3 -I ArtGen/Spine/ran_sung.py to 1          tờ mảnh gốc phóng 3 lần cho GPT vẽ lại da -> inbox/ran_sung_1/mau/goc_A.png, goc_B.png
    py -3 -I ArtGen/Spine/ran_sung.py nhan 1        cắt tờ GPT (tai_ve/R01*.png = tờ A, R02*.png = tờ B) -> inbox/ran_sung_1/da/<vùng>.png
    py -3 -I ArtGen/Spine/ran_sung.py lien 1        bỏ nét mực ở chỗ nối giữa các khúc thân cùng màu (liền khối) -> inbox/ran_sung_1/da/_lien/
    py -3 -I ArtGen/Spine/ran_sung.py them          hai clip con gốc không có (cast, skill): viết khoá trên bộ xương gốc, lấy mẫu bằng runtime Spine thật
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ran_sung.py rig 1     nướng rig gốc + da mới -> inbox/ran_sung_1/rig/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ran_sung.py all       dạng 2, rồi dạng 1 gộp bản nhẹ của dạng 2 (clip evolve)
    py -3 -I ArtGen/Spine/ran_sung.py xem 1 <clip> <khung,khung,...>                       soi lớn vài khung

Dữ liệu gốc (đã rút bằng mo_xe, xem skill pokiclash-spine-rig mục 00): <SXS_SCAN>/monster_3247/ gồm rig/ (skel, atlas, png), info.json,
att_goc.json (mọi hình ở dáng gốc: đỉnh, uv, trọng số), mau_khung.json (mọi clip lấy mẫu 30 khung/giây: ma trận thế giới từng xương,
hình đang bật của từng slot). Rig gốc có IK và path constraint; .atomik không có ràng buộc nên NƯỚNG: mọi xương gốc thành con trực
tiếp của `nhun`, mỗi khung khoá thẳng vị trí, góc, tỉ lệ thế giới (trục xương lệch tối đa 3°, bỏ qua).
Ghi chú thiết kế, bảng mảnh: inbox/ran_sung_ghichu.md. Hình và chuyển động gốc là của hãng làm game tham khảo: không đăng công khai.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
CODE = "ran_sung"
GOC = "monster_3247"
GRAY = (150, 150, 150)
FONT = "C:/Windows/Fonts/arial.ttf"
PHONG = 3                      # tờ mảnh cho GPT: mảnh gốc phóng chừng này lần
TI_ANH = 4.0 / 3.0             # ảnh da trong atlas của mình: px ảnh gốc x chừng này (= 1 px mỗi đơn vị xương, atlas gốc xuất tỉ lệ 0,75)
K = 1.0                        # đơn vị xương gốc -> px rig
CHAM = {1: 1.0, 2: 1.1}
KK = {1: 1.0, 2: 1.15}         # dạng 2 to hơn: cả rig phóng chừng này (ảnh da cũng lớn theo để không nhoè)


def dat_dang(k):
    """đặt tỉ lệ rig và cỡ ảnh da theo dạng (gọi đầu mỗi lệnh)."""
    global K, TI_ANH
    K = KK[k]
    TI_ANH = 4.0 / 3.0 * K


# mảnh THÊM của dạng 2 (con gốc không có): một chiếc nanh, một chiếc gai lưng. Trên tờ mảnh là HÌNH GIỮ CHỖ xám nhạt do script vẽ; GPT vẽ
# lại như các mảnh khác (giữ hình bóng). Rig đặt nhiều bản của mỗi mảnh: 2 nanh (một bản lật) bám xương đầu, 5 gai dọc sống cổ.
THEM = {2: {"B": {"X_nanh": (1180, 440), "X_gai": (1320, 430)}}}


def hinh_them(g):
    """hình giữ chỗ của một mảnh thêm, cỡ px ảnh gốc (RGBA): nền xám nhạt, viền sẫm; gai để hở viền ở đáy (đáy khuất dưới cổ)."""
    S = 8
    if g == "X_nanh":
        w, h = 18, 30
        poly = [(2, 2), (16, 2), (15.5, 11), (12, 22), (8, 29), (6, 21), (3, 11)]
        vien = poly + [poly[0]]
    else:
        w, h = 34, 30
        poly = [(2, 29), (4, 17), (9, 2), (17, 11), (26, 20), (32, 29)]
        vien = poly
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(x * S, y * S) for x, y in poly], fill=(205, 205, 205, 255))
    d.line([(x * S, y * S) for x, y in vien], fill=(50, 45, 40, 255), width=2 * S, joint="curve")
    return im.resize((w, h), Image.LANCZOS)


def o_to(k):
    """ô từng mảnh trên hai tờ của dạng k (mảnh gốc + mảnh thêm)."""
    return {t: {**cac, **THEM.get(k, {}).get(t, {})} for t, cac in TO.items()}


def them_vao(k, imgs, mn):
    for cac in THEM.get(k, {}).values():
        for g in cac:
            imgs[g] = hinh_them(g)
            mn[g] = np.asarray(imgs[g])[..., 3] > 128

# tờ mảnh: vùng ảnh gốc -> góc trên trái của ô trên tờ 1536 x 1024 (ảnh phóng PHONG lần)
TO = {
    "A": {"P_shenti01": (40, 40), "P_shenti02": (400, 60), "P_shenti03": (730, 90), "P_bozi": (1140, 80),
          "P_weiba02": (40, 560), "P_weiba01": (600, 590), "P_huoyan": (1000, 530)},
    "B": {"P_face": (40, 50), "P_yanpi": (420, 60), "P_mouth": (800, 80), "P_ear01": (1090, 60), "P_ear02": (1320, 80),
          "P_yanjing01": (80, 460), "P_yanjing02": (300, 460), "P_yanjing03": (480, 470), "P_yanjing04": (650, 470),
          "P_shouji01": (820, 470), "P_shouji02": (980, 470)},
}
BUOC = {"A": "R01", "B": "R02"}
# mảnh đổi thành SỪNG cứng (người dùng: sừng đen, cứng): bám trọn một xương thay vì chuỗi xương mềm của con gốc
# sừng (thay chùm lông mềm của con gốc): CỨNG, cả hình bám trọn một xương, lưới là một ô chữ nhật phủ cả khung ảnh (sừng không phải nằm
# trong đa giác của chùm lông cũ). Khoá theo TÊN SLOT (cùng vùng ảnh P_huoyan, cùng tên hình "P_huoyan" có ở hai slot: dáng đứng bám chuỗi bone12..15, dáng bò
# P_huoyan2 bám chuỗi bone33..36). Sừng đuôi bám đốt thứ hai của chuỗi (đốt cuối mà mảnh chóp đuôi còn bám): gốc sừng đi liền chóp đuôi.
# Hai sừng đầu bám xương đầu (không bám xương tai bone21, bone24: tai gốc vẫy, sừng thì không).
CUNG = {"P_ear01": "bone16", "P_ear02": "bone16", "P_huoyan": "bone13", "P_huoyan2": "bone34"}
VUNG_CUNG = ("P_ear01", "P_ear02", "P_huoyan")
# thứ tự vẽ: hai sừng đầu nằm SAU mặt nạ (gốc sừng khuất sau đỉnh đầu như concept; chùm tai gốc thì đè lên trán), ngay trước gáy
SAU_MAT = ("P_ear02", "P_ear01")
# Sừng đuôi TỰ ĐẶT (dạng 2; dạng 1 người dùng đã duyệt chỗ đặt theo chùm lông cũ + DOI nên giữ): gốc sừng (đầu to, lùi vào một đoạn)
# đặt đúng đầu mút nhọn của mảnh chóp đuôi, trục sừng xoay theo hướng chóp đuôi (+ GOC_SUNG độ). Sừng to hơn chùm lông cũ mà vẫn đặt
# theo khung chùm lông thì gốc sừng lệch khỏi chóp đuôi (lỗi người dùng báo 2026-11-11).
TU_DAT = {2: {"P_huoyan": ("P_weiba01", "P_weiba01"), "P_huoyan2": ("P_weiba04", "P_weiba01")}}   # hình sừng -> (slot, hình) của chóp đuôi đi với nó
LUI_GOC = 0.13                 # gốc sừng lùi vào trong chóp đuôi chừng này lần chiều dài sừng
GOC_SUNG = 30.0                # xoay thêm trục sừng so với hướng chóp đuôi (độ, dương = ngược kim)


def truc_hinh(al):
    """trục dài của một hình (mặt nạ bool): trả (đầu to, đầu nhọn) toạ độ px (x, y)."""
    ys, xs = np.nonzero(al)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    w, v = np.linalg.eigh(np.cov((P - c).T))
    ax = v[:, int(np.argmax(w))]
    t = (P - c) @ ax
    lo, hi = np.percentile(t, 1), np.percentile(t, 99)
    L = hi - lo
    rong = lambda u0, u1: float(np.ptp((P - c)[(t >= u0) & (t <= u1)] @ np.array([-ax[1], ax[0]])) if ((t >= u0) & (t <= u1)).sum() > 3 else 0.0)
    r_lo, r_hi = rong(lo, lo + 0.25 * L), rong(hi - 0.25 * L, hi)
    a_, b_ = c + ax * lo, c + ax * hi
    return (a_, b_) if r_lo >= r_hi else (b_, a_)


# dời ô ảnh sừng (px ảnh gốc, y xuống) so với chỗ chùm lông cũ: (dx, dy)
DOI = {"P_huoyan": (2, -5), "P_huoyan2": (2, -5), "P_ear01": (5, -8), "P_ear02": (0, 0)}
# mảnh KHÔNG viền mực (đĩa con ngươi trượt trên tròng mắt cùng màu): mép hình lẫn nền trắng của tờ thành vành nhạt -> tô lại dải mép bằng
# màu giữa của mảnh; và tròng mắt trên nền mắt (P_yanpi) kéo về đúng màu đó cho đĩa chìm hẳn vào tròng
KHONG_VIEN = ("P_yanjing03", "P_yanjing04")
LAT_NGANG = ("P_ear02",)       # sừng bên phải người xem: GPT hay vẽ cùng chiều cong với sừng trái -> lật ngang trong khung (mũi sừng cong vào trong)


def scan():
    return os.path.join(os.environ.get("SXS_SCAN", r"D:\Ripper\SwordxStaff\scan"), GOC)


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def moi_nhat(thu_muc, goc):
    best, bn = None, -1
    if not os.path.isdir(thu_muc):
        return None
    for f in os.listdir(thu_muc):
        n, e = os.path.splitext(f)
        if e.lower() != ".png" or not (n == goc or n.startswith(goc + "_")):
            continue
        sx = n[len(goc) + 1:]
        i = int(sx) if sx.isdigit() else (1 if n == goc else -1)
        if i > bn:
            best, bn = os.path.join(thu_muc, f), i
    return best


# ---------------------------------------------------------------- dữ liệu gốc
def nap_goc():
    import to_manh
    rig_ = os.path.join(scan(), "rig")
    atlas, imgs = to_manh.nap(rig_, GOC)
    att = json.load(open(os.path.join(scan(), "att_goc.json"), encoding="utf-8"))
    info = json.load(open(os.path.join(scan(), "info.json"), encoding="utf-8"))
    return atlas, imgs, att, info


def uv_cua(a, atlas, im):
    """uv (px ảnh gốc, khung chưa cắt) của từng đỉnh một hình; vùng chữ nhật thì 4 góc BL, UL, UR, BR của phần đã cắt."""
    if a["type"].endswith("MeshAttachment"):
        return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3), a["hull"]
    r = atlas[a["region"]]
    ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
    w, h = (r["bounds"][3], r["bounds"][2]) if r["rotate"] in (90, 270) else (r["bounds"][2], r["bounds"][3])
    return (np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float),
            np.array([[0, 1, 2], [2, 3, 0]]), 4)


def mat_na_vung(att, atlas, imgs):
    """mặt nạ từng vùng ảnh gốc: phần nằm trong đa giác lưới của hình dùng vùng đó (atlas gốc xếp theo đa giác nên khung chữ nhật của
    một vùng lẫn mẩu của vùng khác)."""
    out = {}
    for a in att["atts"]:
        g = a.get("region")
        if g not in imgs or g in out:
            continue
        im = imgs[g]
        uv, tr, hull = uv_cua(a, atlas, im)
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).polygon([tuple(p) for p in uv[:hull].tolist()], fill=255)
        al = np.asarray(im)[..., 3]
        out[g] = (np.asarray(m) > 0) & (al > 20)
    return out


# ---------------------------------------------------------------- tờ mảnh gốc cho GPT
def to(k):
    atlas, imgs, att, info = nap_goc()
    mn = mat_na_vung(att, atlas, imgs)
    them_vao(k, imgs, mn)
    dm = os.path.join(d_inbox(k), "mau")
    os.makedirs(dm, exist_ok=True)
    for ten, cac in o_to(k).items():
        sheet = Image.new("RGB", (1536, 1024), (255, 255, 255))
        o = {}
        for g, (x, y) in cac.items():
            im = np.asarray(imgs[g]).copy()
            im[..., 3] = np.where(mn[g], im[..., 3], 0)
            pil = Image.fromarray(im, "RGBA").resize((imgs[g].width * PHONG, imgs[g].height * PHONG), Image.LANCZOS)
            sheet.paste(pil, (x, y), pil)
            o[g] = [x, y, x + pil.width, y + pil.height]
            if x + pil.width > 1536 - 20 or y + pil.height > 1024 - 20:
                raise SystemExit(f"{g} tràn tờ {ten}")
        sheet.save(os.path.join(dm, f"goc_{ten}.png"))
        json.dump(o, open(os.path.join(dm, f"goc_{ten}.json"), "w", encoding="utf-8"), indent=1)
        print(os.path.join(dm, f"goc_{ten}.png"), len(o), "mảnh")


def nen_trang(a, nguong=236):
    import cv2
    w = (a.min(2) >= nguong).astype(np.uint8)
    n, lab = cv2.connectedComponents(w, connectivity=4)
    mep = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    mep = mep[mep != 0]
    return np.isin(lab, mep) & (w > 0)


def phang_lung(rgba):
    """LÀM PHẲNG lưng một khúc thân (luật tướng: tô phẳng, không bóng). GPT hay tô sẫm, gạch chì đậm ở đầu dưới khúc cổ, khúc ngực:
    (1) nét sẫm như mực nằm SÂU trong hình (xa mép hơn bề rộng viền) không phải viền -> lấy màu lưng sạch gần nhất; (2) vùng lưng tối
    hơn mức giữa -> kéo sáng lên mức giữa, giữ vân sáp. rgba: uint8 cỡ tờ (px tờ). Trả ảnh mới."""
    import cv2
    a = rgba.copy()
    c = a[..., :3].astype(np.float32)
    al = a[..., 3] > 128
    sau = cv2.distanceTransform(al.astype(np.uint8), cv2.DIST_L2, 5)
    mx = c.max(2)
    lung = al & (c[..., 2] > c[..., 0] + 40) & (c[..., 1] < 165)             # lam / chàm (không phải bụng nhạt, đốm bong bóng)
    sach = lung & (mx >= 115)
    if sach.sum() < 200:
        return a
    giua = float(np.median(mx[sach]))
    # (1) nét sẫm sâu trong hình, nằm giữa vùng lưng
    gan_lung = cv2.dilate(sach.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    net = al & (mx < 115) & (sau > 16) & gan_lung
    net = cv2.dilate(net.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    net &= al & (sau > 14)
    ng = sach & ~net & (mx >= 0.9 * giua)
    if net.any() and ng.any():
        _, lab = cv2.distanceTransformWithLabels((~ng).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        lut = np.zeros(lab.max() + 1, np.int64)
        lut[lab[ng]] = np.flatnonzero(ng)
        c[net] = c.reshape(-1, 3)[lut[lab[net]]]
        mx = c.max(2)
    # (2) vùng lưng tối hơn mức giữa (không đụng dải sát viền mực: ở đó là pixel lẫn mực của viền)
    toi = al & (c[..., 2] > c[..., 0] + 40) & (c[..., 1] < 165) & (mx >= 100) & (mx < 0.92 * giua) & (sau > 12)
    he = np.clip(giua * 0.97 / np.maximum(1.0, mx), 1.0, 1.7)
    c[toi] *= he[toi][:, None]
    a[..., :3] = np.clip(c, 0, 255).astype(np.uint8)
    return a


def nhan(k):
    """cắt hai tờ GPT đã vẽ lại da theo ô của tờ mảnh gốc; mỗi mảnh: lấy cụm hình trong ô, dò lệch ±12 px (px tờ) so với mặt nạ mảnh gốc,
    thu về cỡ atlas của mình, lưu inbox/ran_sung_<k>/da/<vùng>.png (cùng khung với ảnh gốc: uv của lưới gốc dùng thẳng)."""
    import cv2
    atlas, imgs, att, info = nap_goc()
    mn = mat_na_vung(att, atlas, imgs)
    them_vao(k, imgs, mn)
    dd = os.path.join(d_inbox(k), "da")
    os.makedirs(dd, exist_ok=True)
    noi_khung, mau_trong = {}, []
    for ten, cac in o_to(k).items():
        pth = moi_nhat(os.path.join(d_inbox(k), "tai_ve"), BUOC[ten])
        if not pth:
            print(f"  tờ {ten}: chưa có ảnh {BUOC[ten]}")
            continue
        g_ = np.array(Image.open(pth).convert("RGB").resize((1536, 1024), Image.LANCZOS)).astype(np.float32)
        hinh = ~nen_trang(g_)
        n, lab, st, _ = cv2.connectedComponentsWithStats(hinh.astype(np.uint8), connectivity=8)
        for vung, (x0, y0) in cac.items():
            w0, h0 = imgs[vung].size
            W3, H3 = w0 * PHONG, h0 * PHONG
            m_goc = cv2.resize(mn[vung].astype(np.uint8), (W3, H3), interpolation=cv2.INTER_NEAREST) > 0
            M0 = np.zeros((1024, 1536), bool)
            M0[y0:y0 + H3, x0:x0 + W3] = m_goc
            ids = [i for i in range(1, n) if st[i, 4] > 60 and (lab == i)[y0:y0 + H3, x0:x0 + W3].sum() > 0.5 * st[i, 4]]
            m = np.isin(lab, ids)
            if not m.any():
                print(f"  {vung}: GPT không vẽ mảnh này, giữ da gốc")
                continue
            best = (-1.0, 0, 0)
            for sy in range(-12, 13, 2):
                for sx in range(-12, 13, 2):
                    sh = np.roll(np.roll(m, sy, 0), sx, 1)
                    iou = (sh & M0).sum() / max(1, (sh | M0).sum())
                    if iou > best[0]:
                        best = (float(iou), sx, sy)
            iou, sx, sy = best
            if vung in VUNG_CUNG:                                              # sừng: hình khác hẳn chùm lông cũ, dò lệch theo hình bóng là vô nghĩa
                sx = sy = 0
                ys, xs = np.nonzero(m)
                tran = [xs.min() < x0, ys.min() < y0, xs.max() >= x0 + W3, ys.max() >= y0 + H3]
                # sừng to hơn chùm lông cũ: NỚI KHUNG ảnh (bội PHONG px tờ = px ảnh gốc), ghi vào da/_noi.json để lúc dựng lưới nới ô chữ nhật theo
                nl, nt = -(-max(0, x0 - xs.min()) // PHONG), -(-max(0, y0 - ys.min()) // PHONG)
                nr, nb = -(-max(0, xs.max() + 1 - x0 - W3) // PHONG), -(-max(0, ys.max() + 1 - y0 - H3) // PHONG)
                if vung in LAT_NGANG:
                    nl = nr = max(nl, nr)                                      # lật ngang quanh giữa khung gốc: nới đều hai bên
                noi_khung[vung] = [int(nl), int(nt), int(nr), int(nb)]
                if any(tran):
                    print(f"    {vung}: sừng to hơn khung mảnh gốc, nới khung (trái, trên, phải, dưới) = {noi_khung[vung]} px ảnh gốc")
            nl, nt, nr, nb = [v * PHONG for v in noi_khung.get(vung, (0, 0, 0, 0))]
            gb = np.roll(np.roll(g_, sy, 0), sx, 1)[y0 - nt:y0 + H3 + nb, x0 - nl:x0 + W3 + nr]
            mb = np.roll(np.roll(m, sy, 0), sx, 1)[y0 - nt:y0 + H3 + nb, x0 - nl:x0 + W3 + nr].copy()
            lo = 0
            if vung not in VUNG_CUNG:
                # LỖ (lỗ mắt của mặt nạ): mảng trắng kín trong hình GPT mà phần lớn nằm ở chỗ mảnh gốc trong suốt -> trong suốt
                ngoai = cv2.dilate(m_goc.astype(np.uint8), np.ones((7, 7), np.uint8)) == 0
                tr_ = ((gb.min(2) >= 236) & mb).astype(np.uint8)
                nn, ll, ss, _ = cv2.connectedComponentsWithStats(tr_, connectivity=4)
                for i in range(1, nn):
                    c = ll == i
                    if ss[i, 4] > 40 and (c & ngoai).sum() > 0.3 * ss[i, 4]:
                        mb &= ~(cv2.dilate(c.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)
                        lo += 1
            al = cv2.GaussianBlur(mb.astype(np.float32), (0, 0), 0.8)
            al = np.where(cv2.erode(mb.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0, 1.0, al)
            if vung not in VUNG_CUNG:
                # hình không tràn khỏi mảnh gốc (lưới gốc chỉ phủ tới đó) và giữ mép mờ của mảnh gốc: nhân với alpha gốc nới 5 px tờ
                a_goc = np.where(mn[vung], np.asarray(imgs[vung])[..., 3], 0).astype(np.uint8)
                a_goc = cv2.resize(a_goc, (W3, H3), interpolation=cv2.INTER_LINEAR)
                a_goc = cv2.dilate(a_goc, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))).astype(np.float32) / 255.0
                al = al * np.clip(a_goc * 1.6, 0, 1)
            if vung in KHONG_VIEN:
                trong = cv2.erode(mb.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
                mau_giua = np.median(gb[trong & (gb[..., 2] < 110) & (gb[..., 0] > 180)], axis=0)       # hổ phách, bỏ con ngươi đen và chấm sáng
                gb = gb.copy()
                gb[~trong] = mau_giua
                mau_trong.append(mau_giua)
            rgba = np.dstack([np.clip(gb, 0, 255), al * 255]).astype(np.uint8)
            if vung in THAN:
                rgba = phang_lung(rgba)
            if lo:
                print(f"    {vung}: {lo} lỗ trong suốt")
            if vung in LAT_NGANG:
                rgba = np.ascontiguousarray(rgba[:, ::-1])
            tw, th = max(2, round((w0 + (nl + nr) / PHONG) * TI_ANH)), max(2, round((h0 + (nt + nb) / PHONG) * TI_ANH))
            Image.fromarray(rgba, "RGBA").resize((tw, th), Image.LANCZOS).save(os.path.join(dd, vung + ".png"))
            print(f"  {vung}: dời ({sx:+d}, {sy:+d}) px tờ, IoU hình bóng với mảnh gốc {iou:.3f}")
    json.dump(noi_khung, open(os.path.join(dd, "_noi.json"), "w", encoding="utf-8"))
    p_yp = os.path.join(dd, "P_yanpi.png")
    if mau_trong and os.path.exists(p_yp):
        a = np.array(Image.open(p_yp).convert("RGBA")).astype(np.float32)
        cam = (a[..., 0] > 180) & (a[..., 2] < 120) & (a[..., 1] > 90) & (a[..., 3] > 0)
        if cam.any():
            a[..., :3][cam] += np.mean(mau_trong, axis=0) - np.median(a[..., :3][cam], axis=0)
            Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").save(p_yp)
    soi_da(k)


def doc_noi(k):
    p = os.path.join(d_inbox(k), "da", "_noi.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def da(k, imgs, mn, lien=True):
    """da từng vùng: bản GPT vẽ lại nếu có (ưu tiên bản đã bỏ nét mực chỗ nối, da/_lien/), không thì da gốc (dựng thử rig trước khi
    có da mới)."""
    from quai import anh
    out, thieu = {}, []
    for g, im in imgs.items():
        p = os.path.join(d_inbox(k), "da", g + ".png")
        p_l = os.path.join(d_inbox(k), "da", "_lien", g + ".png")
        if lien and os.path.exists(p_l) and os.path.exists(p) and os.path.getmtime(p_l) >= os.path.getmtime(p):
            p = p_l
        tw, th = max(2, round(im.width * TI_ANH)), max(2, round(im.height * TI_ANH))
        if os.path.exists(p):
            pil = Image.open(p).convert("RGBA")                              # sừng có thể rộng hơn khung gốc (doc_noi): giữ nguyên cỡ
        else:
            a = np.asarray(im).copy()
            if g in mn:
                a[..., 3] = np.where(mn[g], a[..., 3], 0)
            pil = Image.fromarray(a, "RGBA").resize((tw, th), Image.LANCZOS)
            thieu.append(g)
        out[g] = anh.loang_mau(pil)
    return out, thieu


def soi_da(k):
    atlas, imgs, att, info = nap_goc()
    mn = mat_na_vung(att, atlas, imgs)
    them_vao(k, imgs, mn)
    dd = os.path.join(d_inbox(k), "da")
    ten = [g for g in imgs if os.path.exists(os.path.join(dd, g + ".png"))]
    if not ten:
        return
    f = ImageFont.truetype(FONT, 15)
    CW, CH, cot = 430, 250, 6
    hang = (len(ten) + cot - 1) // cot
    out = Image.new("RGB", (cot * CW, hang * CH), (120, 125, 140))
    dr = ImageDraw.Draw(out)
    for i, g in enumerate(sorted(ten, key=lambda n: -imgs[n].width * imgs[n].height)):
        x0, y0 = (i % cot) * CW, (i // cot) * CH
        a = np.asarray(imgs[g]).copy()
        a[..., 3] = np.where(mn[g], a[..., 3], 0)
        a = Image.fromarray(a, "RGBA")
        b = Image.open(os.path.join(dd, g + ".png")).convert("RGBA")
        s = min(195 / a.width, 180 / a.height, 3.0)
        a2 = a.resize((max(1, int(a.width * s)), max(1, int(a.height * s))), Image.LANCZOS)
        b2 = b.resize(a2.size, Image.LANCZOS)
        out.paste(a2, (x0 + 10, y0 + 40), a2)
        out.paste(b2, (x0 + 220, y0 + 40), b2)
        dr.text((x0 + 8, y0 + 8), f"{g}: gốc | da mới", fill=(255, 255, 255), font=f)
        dr.rectangle([x0, y0, x0 + CW - 1, y0 + CH - 1], outline=(90, 95, 110))
    out.save(os.path.join(dd, "_so_goc.png"))
    print("  ->", os.path.join(dd, "_so_goc.png"))


# ================================================================ RIG: nướng rig gốc
def _quai():
    from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat
    return anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat


def ln(f, keys):
    return float(np.interp(f, [q[0] for q in keys], [q[1] for q in keys]))


def tach_ma_tran(m):
    """ma trận thế giới [a, b, c, d] của xương Spine (trục x = (a, c), trục y = (b, d)) -> (góc độ, sx, sy)."""
    a, b, c, d = m
    sx, sy = math.hypot(a, c), math.hypot(b, d)
    if a * d - b * c < 0:
        sy = -sy
    return math.degrees(math.atan2(c, a)), sx, sy


# ---- mảnh thêm của dạng 2 trên rig (con gốc không có). Toạ độ ghi bằng px ẢNH GỐC của mảnh mà nó bám theo.
NANH = [(51.5, 75.0, False), (74.0, 76.0, True)]      # hai nanh: (x, y) đỉnh nanh trên ảnh mặt nạ P_face (hai gò môi hai bên khấc), lật ngang?
NANH_TO = 1.0
GAI = [(0.13, 1.0), (0.27, 1.05), (0.41, 1.0), (0.55, 0.9), (0.69, 0.78)]   # gai lưng: (chỗ dọc cổ: phần chiều cao ảnh P_shenti01, cỡ)
VONG2 = (1.2, (-16.0, -3.0))                           # vòng thân thứ hai: bản sao khúc vòng cuộn phóng chừng này quanh tâm, dời (đơn vị gốc)


def tren_luoi(uv, tris, V, W, p):
    """điểm ảnh p (px ảnh gốc) trên một lưới -> (affine 3x2 [x, y, 1] @ A = thế giới của tam giác chứa nó, trọng số nội suy tại đó)."""
    A_, B_, C_ = uv[tris[:, 0]], uv[tris[:, 1]], uv[tris[:, 2]]
    v0, v1, v2 = B_ - A_, C_ - A_, np.asarray(p, float)[None] - A_
    d = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    d = np.where(np.abs(d) < 1e-9, 1e-9, d)
    b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / d
    b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / d
    bary = np.stack([1 - b1 - b2, b1, b2], 1)
    t = int(np.argmax(bary.min(1)))
    idx = tris[t]
    Aff = np.linalg.solve(np.c_[uv[idx], np.ones(3)], V[idx])
    w = {}
    for bi, i in zip(np.clip(bary[t], 0, 1), idx):
        for b, x in W[i].items():
            w[b] = w.get(b, 0.0) + float(bi) * x
    top = sorted(w.items(), key=lambda q: -q[1])[:4]
    tot = sum(x for _, x in top) or 1.0
    return Aff, {b: x / tot for b, x in top}


def dung(k, lien=True, nhe=1.0):
    """dựng Sk từ dữ liệu gốc: mọi xương gốc (tên b_<tên gốc>) là con trực tiếp của `nhun`, đặt theo dáng gốc; mọi slot, mọi hình với
    lưới, uv, trọng số của gốc; da là ảnh mới. Trả (sk, info). nhe < 1: bản NHẸ (ảnh thu nhỏ, không có bản còn nét) để gộp vào dạng
    trước cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    atlas, imgs, att, inf = nap_goc()
    mn = mat_na_vung(att, atlas, imgs)
    them_vao(k, imgs, mn)
    das, thieu = da(k, imgs, mn, lien)
    if nhe < 1.0:
        das = {g: im.resize((max(2, round(im.width * nhe)), max(2, round(im.height * nhe))), Image.LANCZOS) for g, im in das.items()}
    ti_a = TI_ANH * nhe                                                      # px ảnh da trên mỗi px ảnh gốc
    noi_k = doc_noi(k)
    if thieu:
        print(f"  CHƯA có da mới cho {len(thieu)} vùng (dùng tạm da gốc): {', '.join(sorted(thieu))}")
    B = att["bones"]
    ten_b = ["b_" + b["name"] for b in B]
    dy = -float(inf["y"])                                                    # đáy hình của con gốc nằm dưới gốc toạ độ: dời lên cho chân ở y = 0
    sk = khung.Sk(f"{CODE}_{k}")
    for g, im in das.items():
        sk.anh(g, im)
    # khúc thân đã bỏ nét mực chỗ nối (bước lien): thêm bản CÒN NÉT để clip đổi sang ở những khung mép đó lộ ra thành viền ngoài
    co_vien = set()
    if lien and nhe >= 1.0:
        for g in THAN:
            p_v, p_l = os.path.join(d_inbox(k), "da", g + ".png"), os.path.join(d_inbox(k), "da", "_lien", g + ".png")
            if g not in thieu and os.path.exists(p_l) and os.path.getmtime(p_l) >= os.path.getmtime(p_v):
                sk.anh(g + "_vien", anh.loang_mau(Image.open(p_v).convert("RGBA")))
                co_vien.add(g)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("nhun", "move")
    goc0 = []
    for b, tn in zip(B, ten_b):
        g, sx, sy = tach_ma_tran([b["a"], b["b"], b["c"], b["d"]])
        goc0.append((b["x"] * K, (b["y"] + dy) * K, g, sx, sy))
        sk.xuong(tn, "nhun", b["x"] * K, (b["y"] + dy) * K, goc=g, dai=float(b["len"]) * K, sx=sx, sy=sy, the_gioi=True)
    # chỗ nhả nước cho VFX: con của xương miệng gốc (bone20), trục x chĩa ra trước
    m20 = B[[b["name"] for b in B].index("bone20")]
    sk.xuong("mieng", "b_bone20", (m20["x"] + 30) * K, (m20["y"] + dy - 26) * K, goc=-15, dai=30, the_gioi=True)
    theo_slot = {}
    for a in att["atts"]:
        if a.get("region") in das:
            theo_slot.setdefault(a["slot"], []).append(a)
    dinh = 0

    def du_lieu(slot, ten_hinh):
        """(uv px ảnh gốc, tam giác, đỉnh thế giới, trọng số) của một hình gốc."""
        a = next(q for q in theo_slot[slot] if q["att"] == ten_hinh)
        uv, tr, hull = uv_cua(a, atlas, imgs[a["region"]])
        V = np.array(a["xy"], float).reshape(-1, 2)
        V = np.stack([V[:, 0] * K, (V[:, 1] + dy) * K], 1)
        W = [{ten_b[i]: float(w) for i, w in ws} for ws in a["w"]] if a.get("w") else [{"b_" + a["bone"]: 1.0}] * len(uv)
        return uv, tr, V, W

    def o_cung(slot, vung, goc, ex, ey, Aff, W_, lat=False):
        """một ô chữ nhật ảnh `vung` thành slot mới: goc = góc trên trái, ex / ey = cạnh ngang / dọc, đều theo px ẢNH GỐC của mảnh nó
        bám (Aff đổi ra thế giới); W_ = trọng số chung cho cả 4 đỉnh (đi theo da chỗ đó)."""
        im = das[vung]
        w, h = im.width, im.height
        pts = np.array([[0, h], [0, 0], [w, 0], [w, h]], float)
        if lat:
            pts[:, 0] = w - pts[:, 0]
        goc, ex, ey = np.asarray(goc, float), np.asarray(ex, float), np.asarray(ey, float)
        V = np.c_[np.array([goc + ey, goc, goc + ex, goc + ex + ey]), np.ones(4)] @ Aff
        sk.slot(slot, max(W_, key=W_.get), slot)
        sk.luoi_gan(slot, vung, luoi.Luoi(pts, np.array([[0, 1, 2], [2, 3, 0]]), 4, 4, w, h, ten=slot), [W_] * 4, the_gioi=V, ten=slot)

    def them_truoc(ten_slot):
        """slot thêm của dạng 2 chèn TRƯỚC (vẽ sau lưng) slot gốc ten_slot."""
        if k != 2:
            return
        if ten_slot == "P_weiba02" and "P_shenti03" in das:                 # vòng thân thứ hai: sau lưng mọi thứ
            uv, tr, V, W = du_lieu("P_shenti03", "P_shenti03")
            c = V.mean(0)
            V2 = c + (V - c) * VONG2[0] + np.array(VONG2[1]) * K
            p_v = os.path.join(d_inbox(k), "da", "P_shenti03.png")
            im = anh.loang_mau(Image.open(p_v).convert("RGBA")) if os.path.exists(p_v) else das["P_shenti03"]
            if nhe < 1.0:
                im = im.resize(das["P_shenti03"].size, Image.LANCZOS)
            sk.anh("P_vong2", im)
            a0 = next(q for q in theo_slot["P_shenti03"] if q["att"] == "P_shenti03")
            _, _, hull = uv_cua(a0, atlas, imgs["P_shenti03"])
            sk.slot("vong2", "b_" + a0["bone"], "vong2")
            sk.luoi_gan("vong2", "P_vong2", luoi.Luoi(uv * ti_a, tr, hull, hull, im.width, im.height, ten="vong2"), W, the_gioi=V2, ten="vong2")
        if ten_slot == "P_shenti01" and "X_gai" in das:                     # gai lưng: sau lưng khúc cổ, đáy gai khuất dưới mép cổ
            uv, tr, V, W = du_lieu("P_shenti01", "P_shenti01")
            m = mn["P_shenti01"]
            ab = __import__("cv2").GaussianBlur(m.astype(np.float32), (0, 0), 3)
            gy_, gx_ = np.gradient(ab)
            gw, gh = imgs["X_gai"].size
            for i, (fr_, to_) in enumerate(GAI):
                y = int(round(fr_ * m.shape[0]))
                xs = np.flatnonzero(m[y])
                if not len(xs):
                    continue
                x = int(xs[0])
                n = -np.array([gx_[y, x], gy_[y, x]])
                n /= max(1e-6, np.linalg.norm(n))
                t = np.array([-n[1], n[0]])
                if t[1] < 0:
                    t = -t                                                  # cạnh trái của ảnh gai (phía mũi gai ngả) hướng về đầu rắn
                pz = np.array([x, y], float) - n * 5.0                       # đáy gai lùi vào trong mép cổ
                Aff, W_ = tren_luoi(uv, tr, V, W, pz)
                o_cung(f"gai_{i + 1}", "X_gai", pz + n * gh * to_ - t * gw * to_ * 0.5, t * gw * to_, -n * gh * to_, Aff, W_)
        if ten_slot == "P_face" and "X_nanh" in das:                        # hai nanh: sau mặt nạ (gốc nanh khuất sau môi trên), trước khối miệng
            uv, tr, V, W = du_lieu("P_face", "P_face")
            Aff, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], V, rcond=None)
            nw, nh = imgs["X_nanh"].size
            for i, (x, y, lat) in enumerate(NANH):
                o_cung(f"nanh_{i + 1}", "X_nanh", (x - nw * NANH_TO * 0.5, y), (nw * NANH_TO, 0), (0, nh * NANH_TO), Aff, {"b_bone16": 1.0}, lat)

    thu_tu = [s for s in inf["slots"] if s["name"] not in SAU_MAT]
    i_gay = next(i for i, s in enumerate(thu_tu) if s["name"] == "P_bozi") + 1
    thu_tu[i_gay:i_gay] = [s for s in inf["slots"] if s["name"] in SAU_MAT]
    for s in thu_tu:
        ds = theo_slot.get(s["name"])
        if not ds:
            continue
        them_truoc(s["name"])
        mac_dinh = next((a["att"] for a in ds if a["cur"]), None)
        sk.slot(s["name"], "b_" + ds[0]["bone"], mac_dinh)
        for a in ds:
            im = das[a["region"]]
            uv, tr, hull = uv_cua(a, atlas, imgs[a["region"]])
            pts = uv * ti_a
            V = np.array(a["xy"], float).reshape(-1, 2)
            V = np.stack([V[:, 0] * K, (V[:, 1] + dy) * K], 1)
            if s["name"] in CUNG:                                            # sừng: cứng, bám trọn một xương, lưới = ô chữ nhật cả khung ảnh
                A_, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], V, rcond=None)      # ảnh gốc (px) -> thế giới ở dáng gốc
                w0, h0 = imgs[a["region"]].size
                nl, nt, nr, nb = noi_k.get(a["region"], (0, 0, 0, 0)) if a["region"] not in thieu else (0, 0, 0, 0)
                uv = np.array([[-nl, h0 + nb], [-nl, -nt], [w0 + nr, -nt], [w0 + nr, h0 + nb]], float)
                tr, hull = np.array([[0, 1, 2], [2, 3, 0]]), 4
                pts = (uv + np.array([nl, nt])) * ti_a
                V = np.c_[uv + np.array(DOI.get(s["name"], (0, 0)), float), np.ones(4)] @ A_
                if s["name"] in TU_DAT.get(k, {}) and a["region"] not in thieu:
                    # gốc sừng vào đầu mút chóp đuôi: đầu mút và hướng của chóp đuôi ở dáng gốc (px ảnh gốc -> thế giới qua lưới của nó)
                    uv_c, tr_c, V_c, W_c = du_lieu(*TU_DAT[k][s["name"]])
                    to_c, nhon_c = truc_hinh(mn["P_weiba01"])
                    Aff_c, _ = tren_luoi(uv_c, tr_c, V_c, W_c, nhon_c + (to_c - nhon_c) * 0.06)
                    mut = np.r_[nhon_c, 1.0] @ Aff_c
                    huong = mut - np.r_[nhon_c + (to_c - nhon_c) * 0.3, 1.0] @ Aff_c
                    g_c = math.atan2(huong[1], huong[0]) + math.radians(GOC_SUNG if huong[0] >= 0 else -GOC_SUNG)   # dáng bò lật ngang: ngóc lên là xoay chiều kia
                    al_s = np.asarray(im)[..., 3] > 128
                    to_s, nhon_s = truc_hinh(al_s)                              # px ảnh da (y xuống)
                    goc_s = to_s + (nhon_s - to_s) * LUI_GOC
                    d_s = nhon_s - to_s
                    g_s = math.atan2(-d_s[1], d_s[0])                           # hướng trục sừng trên ảnh, đổi sang y lên
                    q = g_c - g_s
                    R_ = np.array([[math.cos(q), -math.sin(q)], [math.sin(q), math.cos(q)]])
                    px_ = pts - goc_s                                           # px ảnh da; 1 px ảnh da = 1 đơn vị rig
                    V = (np.stack([px_[:, 0], -px_[:, 1]], 1) / nhe) @ R_.T + mut
                W = [{"b_" + CUNG[s["name"]]: 1.0}] * 4
            elif a.get("w"):
                W = [{ten_b[i]: float(w) for i, w in ws} for ws in a["w"]]
            else:
                W = [{"b_" + a["bone"]: 1.0}] * len(pts)
            L = luoi.Luoi(pts, tr, hull, hull, im.width, im.height, ten=a["att"])
            sk.luoi_gan(s["name"], a["region"], L, W, the_gioi=V, ten=a["att"])
            if a["region"] in co_vien:
                L2 = luoi.Luoi(pts, tr, hull, hull, im.width, im.height, ten=a["att"] + "_vien")
                sk.luoi_gan(s["name"], a["region"] + "_vien", L2, W, the_gioi=V, ten=a["att"] + "_vien")
            dinh += len(pts)
    for ev, mo_ta in (("trung", "đòn thường: cắn trúng đối thủ"), ("phun", "bắt đầu nhả nước (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                      ("chem", "chiêu cuối: một nhát đuôi chém tới (VFX vệt chém bám xương b_bone13)"), ("vao_cho", "xuất hiện: vào tới chỗ")):
        sk.su_kien(ev, mo_ta)
    H = float(inf["height"]) * K
    return sk, {"k": k, "H": H, "ten_b": ten_b, "goc0": goc0, "dy": dy, "dinh": dinh, "thieu": thieu, "co_vien": co_vien,
                "theo": {"vong2": "P_shenti03"} if "vong2" in sk.si else {},
                "slot": [q["name"] for q in sk.slots], "mac_dinh": {q["name"]: q["att"] for q in sk.slots}}


def khung_goc(info, mau, ten):
    """các khung đã lấy mẫu của một clip gốc -> list (dịch mỗi xương: [dx, dy, dgóc, sx, sy] so với dáng gốc; hình từng slot; alpha)."""
    fr = mau[ten]["frames"]
    nb = len(info["ten_b"])
    g0 = info["goc0"]
    out = []
    truoc = [0.0] * nb
    for f in fr:
        dich = []
        for i in range(nb):
            x, y = f["b"][i][0] * K, (f["b"][i][1] + info["dy"]) * K
            g, sx, sy = tach_ma_tran(f["m"][i])
            dg = g - g0[i][2]
            dg -= 360.0 * round((dg - truoc[i]) / 360.0)                     # góc liền mạch qua các khung
            truoc[i] = dg
            dich.append((x - g0[i][0], y - g0[i][1], dg, sx / (g0[i][3] or 1), sy / (g0[i][4] or 1)))
        out.append((dich, f["n"], f["a"]))
    return out


def dat_khung(P, info, slots_goc, kf, bo_qua=(), tt=""):
    """đặt một khung gốc vào Pose. tt: tiền tố tên xương, slot, hình (rig gộp tiến hóa: dạng sau mang tiền tố n_)."""
    dich, hinh, alpha = kf
    for tn, (dx, dy_, dg, sx, sy) in zip(info["ten_b"], dich):
        if tn in bo_qua:
            continue
        if abs(dx) + abs(dy_) > 1e-6:
            P.move(tt + tn, dx, dy_)
        if abs(dg) > 1e-6:
            P.rot(tt + tn, dg)
        if abs(sx - 1) + abs(sy - 1) > 1e-6:
            P.scale(tt + tn, sx, sy)
    for sn, h, a in zip(slots_goc, hinh, alpha):
        if sn not in info["mac_dinh"]:
            continue
        if h != info["mac_dinh"][sn]:
            P.att[tt + sn] = (tt + h) if h else None
        if a < 0.999:
            P.alpha[tt + sn] = a
    for sn, goc in info.get("theo", {}).items():                            # slot thêm ẩn hiện theo slot gốc (vòng thân thứ hai theo khúc vòng cuộn)
        if hinh[slots_goc.index(goc)] is None:
            P.att[tt + sn] = None


def tron_khung(ka, kb, u):
    """trộn hai khung gốc (u = 0: ka, 1: kb): dùng để nối clip (bò vào -> đứng)."""
    da_, ha, aa = ka
    db, hb, ab = kb
    d = [tuple(x + (y - x) * u for x, y in zip(p, q)) for p, q in zip(da_, db)]
    return d, (ha if u < 0.5 else hb), [x + (y - x) * u for x, y in zip(aa, ab)]


def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Clip = hoat.Clip
    mau = json.load(open(os.path.join(scan(), "mau_khung.json"), encoding="utf-8"))
    inf = json.load(open(os.path.join(scan(), "info.json"), encoding="utf-8"))
    slots_goc = [s["name"] for s in inf["slots"]]
    H = info["H"]
    ch = CHAM[k]
    p_them = os.path.join(scan(), "mau_them.json")
    if os.path.exists(p_them):
        mau.update(json.load(open(p_them, encoding="utf-8")))
    KG = {n: khung_goc(info, mau, n) for n in mau}

    def lay(ten, f):
        fr = KG[ten]
        f = max(0.0, min(len(fr) - 1.0, f))
        i = int(math.floor(f))
        if i >= len(fr) - 1 or f - i < 1e-6:
            return fr[min(i, len(fr) - 1)]
        return tron_khung(fr[i], fr[i + 1], f - i)

    def an_het(P, a):
        for s in info["slot"]:
            P.alpha[s] = a * P.alpha.get(s, 1.0)

    def idle_fn(t, P):
        dat_khung(P, info, slots_goc, lay("idle_01", t / ch * 30.0))

    # attack = skill_01 của con gốc (lao cắn, chạm ở khung 15) + cú lao của cả con trên xương move (game đo trên xương này)
    def attack_fn(t, P):
        f = t / ch * 30.0
        dat_khung(P, info, slots_goc, lay("skill_01", f))
        if "vong2" in sk.si:                                                    # thân duỗi ra lao cắn thì không còn vòng thân thêm
            a_v = ln(f, [(0, 1), (13, 1), (13.5, 0), (24.5, 0), (25, 1)])     # đổi nhanh đúng lúc bật ra / thu về (mờ chậm thì thành bóng ma)
            if a_v < 0.999:
                P.alpha["vong2"] = a_v
        P.move("move", 0.42 * H * ln(f, [(0, 0), (13, -0.04), (14, 0.3), (15, 1.0), (17, 1.08), (22, 1.0), (28, 0)]), 0)

    def hit_fn(t, P):
        dat_khung(P, info, slots_goc, lay("hit_01", t / ch * 30.0))

    # die = die_01 của con gốc, giữ khung cuối rồi mờ dần
    N_DIE = len(KG["die_01"]) - 1

    def die_fn(t, P):
        f = t / ch * 30.0
        dat_khung(P, info, slots_goc, lay("die_01", f))
        if f > N_DIE + 2:
            an_het(P, ln(f, [(N_DIE + 2, 1), (N_DIE + 11, 0)]))

    # appear = bò vào bằng run_01 của con gốc (lặp), tới nơi thì hoà về dáng đứng
    N_RUN = len(KG["run_01"]) - 1
    A_TOI = 20

    def appear_fn(t, P):
        f = t / ch * 30.0
        u = ln(f, [(0, 0), (A_TOI - 3, 0), (A_TOI + 5, 1), (40, 1)])
        kr = lay("run_01", f % N_RUN)
        kf = tron_khung(kr, KG["idle_01"][0], u) if u > 0 else kr
        dat_khung(P, info, slots_goc, kf)
        P.move("move", -1.0 * H * ln(f, [(0, 1), (A_TOI, 0), (40, 0)]), 0)
        if f < 2:
            an_het(P, ln(f, [(0, 0), (2, 1)]))

    ra = [Clip("appear", (A_TOI + 6) / 30.0 * ch, appear_fn, ev=[(A_TOI / 30.0 * ch, "vao_cho", "")]),
          Clip("idle", (len(KG["idle_01"]) - 1) / 30.0 * ch, idle_fn, loop=True),
          Clip("attack", (len(KG["skill_01"]) - 1) / 30.0 * ch, attack_fn, ev=[(15 / 30.0 * ch, "trung", "")]),
          Clip("hit", (len(KG["hit_01"]) - 1) / 30.0 * ch, hit_fn),
          Clip("die", (N_DIE + 11) / 30.0 * ch, die_fn)]
    T_CAST, T_SKILL = TEN_THEM[k]
    NHAT, N_SKILL = NHAT_K[k], N_SKILL_K[k]
    info["KG"], info["slots_goc"] = KG, slots_goc
    if T_CAST in KG and T_SKILL in KG:
        # cast: đứng tại chỗ, ngửa lấy hơi, chồm tới há nhẹ miệng nhả nước (tia là việc của lớp VFX, bám xương mieng), giữ tới hết dòng
        def cast_fn(t, P):
            dat_khung(P, info, slots_goc, lay(T_CAST, t / ch * 30.0))

        # skill: lao tới, đuôi quất chém liên tiếp (bảy nhát lên xuống trong nửa giây, nhát cuối bổ mạnh nhất), rồi lùi về
        def skill_fn(t, P):
            f = t / ch * 30.0
            dat_khung(P, info, slots_goc, lay(T_SKILL, f))
            P.move("move", 0.34 * H * ln(f, [(0, 0), (5, -0.05), (10, 1.0), (NHAT[-1][0], 1.0), (NHAT[-1][0] + 4, 0.92), (N_SKILL, 0)]), 0)

        ra += [Clip("cast", N_CAST / 30.0 * ch, cast_fn, ev=[(PHUN / 30.0 * ch, "phun", ""), (HET_PHUN / 30.0 * ch, "het_phun", "")]),
               Clip("skill", N_SKILL / 30.0 * ch, skill_fn, trung=NHAT[0][0] / 30.0 * ch,
                    ev=[(fn_ / 30.0 * ch, "chem", huong) for fn_, huong in NHAT])]
    else:
        print("  CHƯA có cast, skill: chạy `ran_sung.py them` trước")
    # khung mà mép đã bỏ mực lộ ra thành viền ngoài: đổi khúc đó sang bản còn nét (bước lien ghi da/_lien/_lo.json)
    p_lo = os.path.join(d_inbox(k), "da", "_lien", "_lo.json")
    if info.get("co_vien") and os.path.exists(p_lo):
        lo = json.load(open(p_lo, encoding="utf-8"))

        def boc(ds, fn):
            def g(t, P):
                fn(t, P)
                for sn in ds[min(len(ds) - 1, int(round(t * hoat.FPS)))]:
                    h = P.att.get(sn, info["mac_dinh"].get(sn))
                    if h and not h.endswith("_vien") and h + "_vien" in sk.atts.get(sn, {}):
                        P.att[sn] = h + "_vien"
            return g

        for c in ra:
            if any(lo.get(c.ten, [])):
                c.fn = boc(lo[c.ten], c.fn)
    return ra


# ---------------------------------------------------------------- clip tự viết trên BỘ XƯƠNG GỐC (cast: há miệng nhả nước; skill: đuôi chém)
# Con gốc không có hai clip này. Viết khoá trên chính bộ xương gốc (cây xương, IK A1 / A2, path B1 của nó vẫn chạy), nạp vào runtime
# Spine thật bằng extra.json (mo_xe: addExtra), lấy mẫu từng khung như các clip gốc rồi nướng chung một đường. Giá trị khoá = khoá của
# idle_01 ở giây 0 (dáng đứng) + lệch viết ở đây: clip vào và ra đều đúng dáng đứng.
N_CAST, PHUN, HET_PHUN = 50, 14, 42          # khung (30 khung/giây, trước khi nhân CHAM)
# chiêu cuối theo dạng: khung từng nhát đuôi. Dạng 1: bảy nhát; dạng 2 mạnh hơn: mười một nhát, nhịp dồn hai khung một nhát, nhát cuối
# giơ lâu hơn rồi bổ.
NHAT_K = {1: [(12, "xuong"), (15, "len"), (17, "xuong"), (20, "len"), (22, "xuong"), (25, "len"), (27, "xuong")],
          2: [(12, "xuong"), (14, "len"), (16, "xuong"), (18, "len"), (20, "xuong"), (22, "len"), (24, "xuong"), (26, "len"), (28, "xuong"),
              (30, "len"), (34, "xuong")]}
N_SKILL_K = {1: 42, 2: 50}
MANH = {1: 1.0, 2: 1.25}                     # biên độ động tác của cast, skill theo dạng
TEN_THEM = {1: ("cast_moi", "skill_moi"), 2: ("cast_moi_2", "skill_moi_2")}


def noi(f, keys):
    """nội suy khoá [(khung, giá trị, kiểu)]: kiểu "e" êm hai đầu (mặc định), "l" thẳng (cú quất), "o" bật nhanh rồi hãm."""
    if f <= keys[0][0]:
        return np.atleast_1d(np.array(keys[0][1], float))
    for a, b in zip(keys[:-1], keys[1:]):
        if f <= b[0]:
            u = (f - a[0]) / max(1e-9, b[0] - a[0])
            kieu = b[2] if len(b) > 2 else "e"
            u = u if kieu == "l" else (1 - (1 - u) ** 2.2 if kieu == "o" else u * u * (3 - 2 * u))
            return np.atleast_1d(np.array(a[1], float)) * (1 - u) + np.atleast_1d(np.array(b[1], float)) * u
    return np.atleast_1d(np.array(keys[-1][1], float))


def lech_cast(k):
    q = MANH[k]
    rung = lambda f: (1.0 if int(f) % 4 < 2 else -1.0) * float(noi(f, [(PHUN, 0), (PHUN + 2, 1), (HET_PHUN - 2, 1), (HET_PHUN, 0)])[0])
    song = lambda f, pha: float(noi(f, [(0, 0), (8, 1), (HET_PHUN, 1), (N_CAST, 0)])[0]) * math.sin(2 * math.pi * f / 16.0 - pha)
    return {
        # ngửa ra sau lấy hơi (0-11) -> chồm tới, há miệng (11-14) -> giữ nhả, rung nhẹ, trôi lùi dần (14-42) -> ngậm, về (42-50)
        ("bone2", "translate"): lambda f: q * noi(f, [(0, (0, 0)), (8, (-9, -3)), (11, (-10, -4)), (14, (9, 0), "o"), (HET_PHUN, (5, 0)), (N_CAST, (0, 0))]),
        ("bone3", "rotate"): lambda f: q * noi(f, [(0, 0), (8, 9), (11, 10), (14, -10, "o"), (HET_PHUN, -7), (N_CAST, 0)]) - 0.8 * q * rung(f),
        ("bone4", "rotate"): lambda f: q * noi(f, [(0, 0), (8, 5), (11, 6), (14, -6, "o"), (HET_PHUN, -4), (N_CAST, 0)]),
        ("bone5", "rotate"): lambda f: q * noi(f, [(0, 0), (8, -7), (11, -8), (14, 6, "o"), (HET_PHUN, 4), (N_CAST, 0)]),
        ("bone16", "rotate"): lambda f: q * noi(f, [(0, 0), (8, 9), (11, 11), (14, -5, "o"), (HET_PHUN, -3), (N_CAST, 0)]) + 1.2 * q * rung(f),
        ("bone20", "rotate"): lambda f: noi(f, [(0, 0), (11, 0), (14, -11 * q, "o"), (HET_PHUN, -11 * q), (HET_PHUN + 4, 0)]),
        # đuôi hạ xuống né đường tia nước (dáng đứng thì sừng đuôi nằm ngay trước miệng), sừng đuôi vẫn lắc, mỗi đốt trễ thêm một nhịp
        ("bone11", "rotate"): lambda f: noi(f, [(0, 0), (8, 6), (14, -22), (HET_PHUN, -20), (N_CAST, 0)]) + 2.5 * song(f, 0.0),
        ("bone12", "rotate"): lambda f: noi(f, [(0, 0), (9, 4), (15, -16), (HET_PHUN, -15), (N_CAST, 0)]) + 3.0 * song(f, 0.7),
        ("bone13", "rotate"): lambda f: noi(f, [(0, 0), (10, 4), (16, -12), (HET_PHUN, -11), (N_CAST, 0)]) + 4.0 * song(f, 1.4),
    }


def lech_skill(k):
    q = min(MANH[k], 1.12)
    NH, N = NHAT_K[k], N_SKILL_K[k]
    fc = NH[-1][0]                                                            # khung nhát cuối
    U, D = np.array([14.0, 10.0, 8.0]) * q, np.array([-30.0, -24.0, -18.0]) * q   # dáng đuôi giơ lên / chém xuống: lệch của bone11, 12, 13
    khoa = [(0, U * 0), (6, U * 0.6), (10, U)]
    for i, (f, huong) in enumerate(NH):
        cuoi = i == len(NH) - 1
        if cuoi:
            khoa.append((f - 1.5, U * 1.15, "e"))                                # nhát cuối: giơ thêm một nhịp rồi mới bổ
        khoa.append((f, (D * (1.3 if cuoi else 1.0)) if huong == "xuong" else U * 0.9, "l"))
    khoa += [(fc + 4, D * 1.15), (N, U * 0)]
    duoi = lambda f, i, tre: float(noi(f - tre, khoa)[i])
    # thân giật ngược chiều mỗi nhát
    giat = lambda f: sum((1.0 if h == "xuong" else -1.0) * max(0.0, 1.0 - abs(f - kk_) / 1.5) for kk_, h in NH)
    return {
        ("A2", "translate"): lambda f: noi(f, [(0, (0, 0)), (6, (8, 50)), (10, (34, 100)), (fc - 2, (38, 100)), (fc, (40, 66), "l"), (fc + 4, (30, 58)), (N, (0, 0))]),
        ("bone11", "rotate"): lambda f: duoi(f, 0, 0.0),
        ("bone12", "rotate"): lambda f: duoi(f, 1, 0.5),
        ("bone13", "rotate"): lambda f: duoi(f, 2, 1.0),
        ("bone2", "translate"): lambda f: noi(f, [(0, (0, 0)), (6, (-8, -6)), (10, (-4, -2)), (fc, (4, -3)), (fc + 4, (6, -3)), (N, (0, 0))]) + np.array([-3.0 * giat(f), 0.0]),
        ("bone3", "rotate"): lambda f: noi(f, [(0, 0), (6, 12), (10, 8), (12, -6), (fc, -8), (fc + 4, -12), (N, 0)]) + 2.0 * giat(f),
        ("bone4", "rotate"): lambda f: noi(f, [(0, 0), (6, 6), (12, -3), (fc + 4, -5), (N, 0)]),
        ("bone16", "rotate"): lambda f: noi(f, [(0, 0), (6, 8), (12, -4), (fc + 4, -6), (N, 0)]) - 2.5 * giat(f),
        ("bone20", "rotate"): lambda f: noi(f, [(0, 0), (9, 0), (12, -9 * q), (fc + 2, -9 * q), (fc + 7, 0)]),
    }


def them():
    """ghi extra.json (hai clip cast_moi, skill_moi) vào thư mục rig gốc rồi lấy mẫu bằng runtime Spine thật -> mau_them.json."""
    import subprocess
    att = json.load(open(os.path.join(scan(), "att_goc.json"), encoding="utf-8"))
    keys = json.load(open(os.path.join(scan(), "keys.json"), encoding="utf-8"))
    ten = [b["name"] for b in att["bones"]]
    loai = {"RotateTimeline": "rotate", "TranslateTimeline": "translate", "ScaleTimeline": "scale"}
    nen = {(ten[t["boneIndex"]], loai[t["type"]]): np.array(t["f"][1:t["n"]], float) for t in keys["idle_01"]["tls"] if t["type"] in loai}
    ra = []
    for name, n, lech in ((TEN_THEM[1][0], N_CAST, lech_cast(1)), (TEN_THEM[1][1], N_SKILL_K[1], lech_skill(1)),
                          (TEN_THEM[2][0], N_CAST, lech_cast(2)), (TEN_THEM[2][1], N_SKILL_K[2], lech_skill(2))):
        bones = {}
        for (b, kind) in sorted(set(nen) | set(lech)):
            v0 = nen.get((b, kind), np.zeros(1 if kind == "rotate" else 2) if kind != "scale" else np.ones(2))
            ks = []
            for f in range(n + 1):
                d = np.atleast_1d(np.array(lech[(b, kind)](f), float)) if (b, kind) in lech else None
                v = v0 if d is None else (v0 * d if kind == "scale" else v0 + d)
                ks.append([round(f / 30.0, 5)] + [round(float(x), 4) for x in v])
            bones.setdefault(b, {})[kind] = ks
        ra.append({"name": name, "dur": n / 30.0, "bones": bones})
    rig_ = os.path.join(scan(), "rig")
    json.dump(ra, open(os.path.join(rig_, "extra.json"), "w", encoding="utf-8"))
    out = os.path.join(scan(), "mau_them.json")
    cmd = [sys.executable, "-I", os.path.join(HERE, "quai", "khoa.py"), "chrome", "--", sys.executable, "-I",
           os.path.join(HERE, "mo_xe", "chay.py"), "sample", rig_, GOC, out, ",".join(TEN_THEM[1] + TEN_THEM[2]), "30", "extra.json"]
    subprocess.run(cmd, check=True)
    print("->", out)


# ---------------------------------------------------------------- bỏ nét mực ở chỗ NỐI giữa các khúc thân (liền khối)
# Người dùng dặn 2026-11-11: "phần nối giữa các part bỏ viền đen đi tạo cảm giác liền khối". Con gốc viền đen quanh từng khúc nên chỗ
# khúc trước đè lên khúc sau có một nét mực cắt ngang thân. Luật: nét mực trên mép một khúc thân bị BỎ ở đoạn mà suốt clip idle nó nằm
# đè lên một khúc thân khác CÙNG MÀU (lưng lam trên lưng lam, bụng nhạt trên bụng nhạt). Giữ nét ở viền ngoài (sau nó là nền, sừng) và
# ở chỗ đổi màu (bụng nhạt đè lên lưng lam: đó là chỗ thân vòng ra sau, cần nét để thấy lớp).
THAN = ("P_shenti01", "P_shenti02", "P_shenti03", "P_bozi", "P_weiba02", "P_weiba01")
THAN_SAU = THAN + ("P_vong2",)             # vòng thân thêm của dạng 2 cũng là thân: khúc vòng cuộn đè lên nó thì bỏ nét (liền thành một khối)
KHONG_BO = ("P_weiba01", "P_weiba02")      # hai mảnh đuôi: vẫn tính là "thân" cho khúc khác nối vào, nhưng không bỏ nét của chính nó (đuôi vẫy, mép lộ ra luôn)
NGUONG_LO = 0.40               # phần đoạn mép đã bỏ mực lộ ra thành viền ngoài tới chừng này thì khung đó dùng bản còn nét


def lien(k):
    import cv2
    from quai.soi import _tris
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k, lien=False)
    idle = next(c for c in clips(sk, info, k) if c.ten == "idle")
    fr = hoat.nuong(sk, idle)[::3]
    ve = soi.Ve(sk)
    H = info["H"]
    S = 1.5
    x0, y0, x1, y1 = -1.2 * H, -0.15 * H, 1.6 * H, 1.25 * H
    Wc, Hc = int((x1 - x0) * S), int((y1 - y0) * S)
    lop = lambda r: (r > 180)                                                  # lớp màu: True = bụng nhạt, False = lưng lam / đốm
    M = {}
    for g in THAN:
        im = np.asarray(sk.images[g].convert("RGBA")).copy()
        al = (im[..., 3] > 128).astype(np.uint8)
        cs, _ = cv2.findContours(al, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(cs, key=len)[:, 0, :].astype(float)
        ab = cv2.GaussianBlur(al.astype(np.float32), (0, 0), 3)
        gx, gy = cv2.Sobel(ab, cv2.CV_32F, 1, 0, ksize=5), cv2.Sobel(ab, cv2.CV_32F, 0, 1, ksize=5)
        ci = c.astype(int)
        n = -np.stack([gx[ci[:, 1], ci[:, 0]], gy[ci[:, 1], ci[:, 0]]], 1)
        n /= np.maximum(1e-6, np.linalg.norm(n, axis=1, keepdims=True))
        # màu bên trong mép (qua khỏi nét mực): thử sâu dần tới khi hết mực
        trong = np.zeros(len(c), bool)
        co = np.zeros(len(c), bool)
        for sau in (6, 8, 10, 13):
            q = np.clip((c - n * sau).round().astype(int), 0, [im.shape[1] - 1, im.shape[0] - 1])
            px = im[q[:, 1], q[:, 0]]
            ok = (~co) & (px[:, 3] > 200) & (px[:, :3].max(1) >= 100)
            trong[ok] = lop(px[ok, 0])
            co |= ok
        M[g] = {"im": im, "c": c, "n": n, "trong": trong, "co": co, "noi": np.zeros(len(c)), "vien": np.zeros(len(c)), "tri": {}}

    def tam_giac(g, an, uv_px, tris):
        """mỗi mẫu viền: tam giác lưới chứa nó, toạ độ trọng tâm của điểm mép và điểm dò ngoài mép."""
        key = an
        if key in M[g]["tri"]:
            return M[g]["tri"][key]
        m = M[g]
        A, B, C = uv_px[tris[:, 0]], uv_px[tris[:, 1]], uv_px[tris[:, 2]]
        def bary(P):
            v0, v1 = B - A, C - A
            d = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
            d = np.where(np.abs(d) < 1e-9, 1e-9, d)
            v2 = P[:, None, :] - A[None]
            b1 = (v2[..., 0] * v1[:, 1] - v2[..., 1] * v1[:, 0]) / d
            b2 = (v0[:, 0] * v2[..., 1] - v0[:, 1] * v2[..., 0]) / d
            return np.stack([1 - b1 - b2, b1, b2], -1)                          # (N, T, 3)
        bi = bary(m["c"] - m["n"] * 2.0)
        ti = np.argmax(bi.min(-1), 1)
        r = np.arange(len(ti))
        out = (ti, bary(m["c"])[r, ti], bary(m["c"] + m["n"] * 4.0)[r, ti])
        m["tri"][key] = out
        return out

    def phan_tich(P):
        """một khung: với từng hình thân đang vẽ trả (vùng, slot, thấy, cùng) theo mẫu viền: thấy = không bị hình khác đè; cùng = sau
        mép là khúc thân cùng màu (hoặc nét mực của khúc thân dưới)."""
        ra_ = []
        items, _ = ve.skin(P)
        lops = []
        for nm, an, V, uv, tris, a, path, si in items:
            if a < 0.5 or not len(tris):
                lops.append(None)
                continue
            src, ox, oy, sw, sh = ve.src[path]
            D = np.stack([(V[:, 0] - x0) * S, (y1 - V[:, 1]) * S], 1)
            lay = Image.new("RGBa", (Wc, Hc), (0, 0, 0, 0))
            _tris(lay, src, D, uv * np.array([sw, sh]) + np.array([ox, oy]), tris)
            lops.append(np.asarray(lay.convert("RGBA")))
        truoc = [None] * len(items)                                           # hợp các hình vẽ SAU nó (đè lên nó)
        acc = np.zeros((Hc, Wc), bool)
        for i in range(len(items) - 1, -1, -1):
            truoc[i] = acc.copy()
            if lops[i] is not None:
                acc |= lops[i][..., 3] > 128
        mau_sau = np.zeros((Hc, Wc, 3), np.uint8)
        id_sau = np.full((Hc, Wc), -1, int)
        for i, (nm, an, V, uv, tris, a, path, si) in enumerate(items):
            if lops[i] is None:
                continue
            if path in M:
                m = M[path]
                src, ox, oy, sw, sh = ve.src[path]
                ti, b_mep, b_do = tam_giac(path, (nm, an), uv * np.array([sw, sh]), tris)      # cùng tên hình có ở hai slot (dáng đứng, dáng bò), lưới khác nhau
                Vt = V[tris[ti]]                                                # (N, 3, 2)
                def px(b):
                    w = (b[:, :, None] * Vt).sum(1)
                    return (np.clip(((w[:, 0] - x0) * S).round().astype(int), 0, Wc - 1),
                            np.clip(((y1 - w[:, 1]) * S).round().astype(int), 0, Hc - 1))
                mx, my = px(b_mep)
                dx_, dy_ = px(b_do)
                khuat = truoc[i][my, mx] | truoc[i][dy_, dx_]
                ids = id_sau[dy_, dx_]
                la_than = np.array([j >= 0 and items[j][6] in THAN_SAU for j in ids])
                col = mau_sau[dy_, dx_].astype(int)
                # điểm dò rơi đúng nét mực của khúc thân bên dưới: hai nét chạy sát nhau (nét đôi) -> cũng bỏ nét của khúc trên,
                # nét của khúc dưới vẫn còn làm viền
                muc = col.max(1) < 100
                cung = la_than & (muc | ((lop(col[:, 0]) == m["trong"]) & m["co"]))
                ra_.append((path, nm, ~khuat, cung))
            ok = lops[i][..., 3] > 128
            mau_sau[ok] = lops[i][..., :3][ok]
            id_sau[ok] = i
        return ra_

    for P in fr:
        for path, nm, thay, cung in phan_tich(P):
            M[path]["noi"] += thay & cung
            M[path]["vien"] += thay & ~cung

    ra = os.path.join(d_inbox(k), "da", "_lien")
    os.makedirs(ra, exist_ok=True)
    o_soi = []
    for g, m in M.items():
        tot = m["noi"] + m["vien"]
        bo = (tot > 0) & (m["noi"] >= 0.8 * tot)
        if g in KHONG_BO:
            bo[:] = False
        N = len(bo)
        # làm gọn trên vòng mép: lấp khe ngắn, bỏ đoạn vụn
        def chay(b, val, ngan):
            b = b.copy()
            i = 0
            ext = np.concatenate([b, b])
            st = None
            for j in range(2 * N):
                if ext[j] == val and st is None:
                    st = j
                elif ext[j] != val and st is not None:
                    if j - st <= ngan and st < N:
                        for q in range(st, j):
                            b[q % N] = not val
                    st = None
            return b
        bo = chay(bo, False, 6)
        bo = chay(bo, True, 9)
        bo = np.array([bo[(np.arange(-5, 6) + i) % N].any() for i in range(N)])   # nới hai đầu đoạn bỏ: không để lại mẩu mực cụt
        m["bo"] = bo
        im = m["im"]
        Z = np.zeros(im.shape[:2], np.uint8)
        for (x, y) in m["c"][bo].astype(int):
            cv2.circle(Z, (int(x), int(y)), int(round(7 * K)), 255, -1)
        al_ = im[..., 3] > 0
        muc = (im[..., :3].max(2) < 110) & al_                                  # mực: tối cả ba kênh (không thử riêng kênh lam: lưng chàm đậm có lam 143)
        net_mem = (im[..., 0] > 148) & (im[..., 0] < 205) & (im[..., 2] > 190) & al_   # nét lam nhạt GPT vẽ thay viền ở mép mềm
        sau = cv2.distanceTransform((im[..., 3] > 128).astype(np.uint8), cv2.DIST_L2, 5)
        # tô lại CẢ DẢI MÉP (rộng bằng nét mực) trong vùng bỏ bằng màu của LÕI gần nhất (lõi = pixel sạch nằm sâu hơn dải mép): hoa văn
        # bên trong (ranh lưng / bụng, vân sáp) kéo thẳng ra tới mép. Không chọn màu theo "ngữ cảnh": ở góc lưng giáp bụng nó tạo mảng
        # trắng lởm chởm (lỗi đã gặp 2026-11-11).
        dai = sau <= 6.0 * K
        dich = (Z > 0) & (muc | dai | (net_mem & (sau <= 9.0 * K)))
        dich = (cv2.dilate(dich.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & (Z > 0) & al_
        loi = (im[..., 3] > 200) & ~(cv2.dilate(muc.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & ~net_mem & (sau > 7.5 * K)
        moi = im.copy()
        if dich.any() and loi.any():
            _, lab = cv2.distanceTransformWithLabels((~loi).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            lut = np.zeros(lab.max() + 1, np.int64)
            lut[lab[loi]] = np.flatnonzero(loi)
            moi[..., :3][dich] = im[..., :3].reshape(-1, 3)[lut[lab[dich]]]
            mo = cv2.GaussianBlur(moi[..., :3], (0, 0), 1.2)                   # dịu vệt sọc vuông góc mép của kiểu lấy màu gần nhất
            moi[..., :3][dich] = mo[dich]
        Image.fromarray(moi, "RGBA").save(os.path.join(ra, g + ".png"))
        print(f"  {g}: bỏ mực {int(bo.sum())}/{N} điểm mép ({100.0 * bo.sum() / N:.0f}%)")
        s_ = 3
        v = Image.fromarray(im, "RGBA").resize((im.shape[1] * s_, im.shape[0] * s_), Image.LANCZOS)
        nen = Image.new("RGB", v.size, (120, 125, 140))
        nen.paste(v, (0, 0), v)
        dd = ImageDraw.Draw(nen)
        for (x, y), b in zip(m["c"], bo):
            if b:
                dd.ellipse([x * s_ - 3, y * s_ - 3, x * s_ + 3, y * s_ + 3], fill=(255, 40, 40))
        v2 = Image.fromarray(moi, "RGBA").resize(v.size, Image.LANCZOS)
        nen2 = Image.new("RGB", v.size, (120, 125, 140))
        nen2.paste(v2, (0, 0), v2)
        o_soi.append((g, nen, nen2))
    # lượt 2: khung nào của clip nào thì đoạn mép đã bỏ mực LỘ RA thành viền ngoài (lao cắn, bò vào: thân duỗi, khúc không còn đè lên
    # nhau như dáng đứng) -> khung đó slot ấy dùng bản còn nét (<hình>_vien). Ghi da/_lien/_lo.json: {clip: [[slot, ...] mỗi khung]}
    lo = {}
    for c in clips(sk, info, k):
        ds, ti_le = [], {}
        for P in hoat.nuong(sk, c):
            hien = set()
            for path, nm, thay, cung in phan_tich(P):
                b_ = M[path]["bo"] & thay
                lo_ = int((b_ & ~cung).sum())
                ti_le.setdefault(nm, []).append(lo_ / max(1, int(M[path]["bo"].sum())))
                if M[path]["bo"].any() and lo_ >= NGUONG_LO * M[path]["bo"].sum():
                    hien.add(nm)
            ds.append(hien)
        ds = [sorted(ds[max(0, i - 1)] | ds[i] | ds[min(len(ds) - 1, i + 1)]) for i in range(len(ds))]
        lo[c.ten] = ds
        print(f"  {c.ten}: {sum(1 for d in ds if d)}/{len(ds)} khung có khúc dùng bản còn nét; phần mép đã bỏ mực bị lộ, lớn nhất: "
              + ", ".join(f"{n_} {max(v):.2f}" for n_, v in ti_le.items() if max(v) > 0.05))
    json.dump(lo, open(os.path.join(ra, "_lo.json"), "w", encoding="utf-8"))
    Wt = sum(a.width + b.width + 30 for _, a, b in o_soi)
    Ht = max(a.height for _, a, b in o_soi) + 30
    tong = Image.new("RGB", (Wt, Ht), (120, 125, 140))
    dd = ImageDraw.Draw(tong)
    x = 0
    f = ImageFont.truetype(FONT, 16)
    for g, a, b in o_soi:
        dd.text((x + 6, 4), g + ": đỏ = đoạn bỏ mực | sau khi bỏ", fill=(255, 255, 255), font=f)
        tong.paste(a, (x, 30))
        tong.paste(b, (x + a.width + 10, 30))
        x += a.width + b.width + 30
    tong.save(os.path.join(ra, "_soi.png"))
    print("  ->", os.path.join(ra, "_soi.png"))


def nuong_het(sk, cl):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    return {c.ten: hoat.nuong(sk, c) for c in cl}


def rig(k, tien_hoa=None):
    """dựng, nướng, xuất dạng k. tien_hoa = (sk2, info2, idle0 của dạng 2, cao2): gộp bản nhẹ của dạng sau cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    dat_dang(k)
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = nuong_het(sk, cl)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    ve = soi.Ve(sk)
    cao = soi.chieu_cao(ve, fr["idle"][0])
    M, clM, frM, noi_ = sk, cl, fr, {}
    if tien_hoa:
        sk2, info2, idle2, cao2 = tien_hoa
        ti = cao / cao2
        M = tienhoa.gop(sk, sk2)
        KG1, KG2, sg = info["KG"], info2["KG"], info["slots_goc"]
        T1, T2 = TEN_THEM[k][0], TEN_THEM[k + 1][0]

        def gong(t, P):                                                       # dạng cũ: ngửa ra sau gồng (dáng lấy hơi của cast), rung dần
            g = hoat.cv(t, [(0, 0), (0.3, 0.25), (0.6, 1, "out"), (1.3, 1.1)])
            dat_khung(P, info, sg, tron_khung(KG1["idle_01"][0], KG1[T1][11], max(0.0, min(1.0, g))))
            r = hoat.rung(t, 0.45, 1.35, moi=1)
            P.scale("nhun", 1 + 0.03 * g + 0.012 * r, 1 - 0.02 * g - 0.012 * r)
            P.move("nhun", 1.5 * r, 0)

        def gam(t, P, fl):                                                    # dạng sau: chồm tới há miệng gầm (dáng nhả của cast, há thêm)
            dat_khung(P, info2, sg, tron_khung(KG2["idle_01"][0], KG2[T2][20], max(0.0, min(1.0, fl))), tt="n_")
            r = hoat.rung(t, 2.0, 2.4, moi=1)
            P.rot("n_b_bone20", -10 * fl * (1 + 0.1 * r))
            P.scale("n_nhun", 1 + 0.03 * fl, 1 + 0.03 * fl)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=gam)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, idle2, ti)
        noi_["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi_["evolve"])
    tk = xuat.xuat_het(M, clM, ra, f"{CODE}_{k}", f"Rắn sừng dạng {k} (reskin {GOC})", frames=frM, dang=k, so_dang=2, dung_yen=("cast",),
                       lao=("skill",), cao=cao, khop_idle=0, ma_goc=3247, noi_them=noi_)
    print(f"dạng {k}: {len(M.bones)} xương, {info['dinh']} đỉnh; cao {cao:.0f} px rig; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


def tat_ca():
    """dạng 2, rồi dạng 1 gộp bản nhẹ của dạng 2 (clip evolve)."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    rig(2)
    dat_dang(2)
    sk2, info2 = dung(2, nhe=0.55)
    cl2 = clips(sk2, info2, 2)
    idle2 = hoat.nuong(sk2, next(c for c in cl2 if c.ten == "idle"))[0]
    cao2 = soi.chieu_cao(soi.Ve(sk2), idle2)
    rig(1, tien_hoa=(sk2, info2, idle2, cao2))


def xem(k, ten, khung_, phong=1.7):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    cl = {c.ten: c for c in clips(sk, info, k)}
    fr = hoat.nuong(sk, cl[ten])
    ve = soi.Ve(sk)
    H = info["H"]
    box = (-1.1 * H, -0.1 * H, 1.5 * H, 1.15 * H)
    ims = [ve.ve(fr[min(len(fr) - 1, i)], box, phong, bg=GRAY, ss=2).convert("RGB") for i in khung_]
    w, h = ims[0].size
    cot = min(4, len(ims))
    out = Image.new("RGB", (cot * w, ((len(ims) + cot - 1) // cot) * h), GRAY)
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype(FONT, 20)
    for j, (i, im) in enumerate(zip(khung_, ims)):
        out.paste(im, ((j % cot) * w, (j // cot) * h))
        d.text(((j % cot) * w + 8, (j // cot) * h + 6), f"{ten} khung {i}", fill=(255, 255, 255), font=f)
    ra = os.path.join(d_inbox(k), "rig", f"xem_{ten}.png")
    os.makedirs(os.path.dirname(ra), exist_ok=True)
    out.save(ra)
    print(ra, out.size)


if __name__ == "__main__":
    arg = sys.argv[1:]
    if len(arg) > 1 and arg[1].isdigit():
        dat_dang(int(arg[1]))
    if arg[:1] == ["to"]:
        to(int(arg[1]))
    elif arg[:1] == ["nhan"]:
        nhan(int(arg[1]))
    elif arg[:1] == ["them"]:
        them()
    elif arg[:1] == ["lien"]:
        lien(int(arg[1]))
    elif arg[:1] == ["rig"]:
        rig(int(arg[1]))
    elif arg[:1] == ["all"]:
        tat_ca()
    elif arg[:1] == ["xem"]:
        xem(int(arg[1]), arg[2], [int(v) for v in arg[3].split(",")])
    else:
        print(__doc__)
