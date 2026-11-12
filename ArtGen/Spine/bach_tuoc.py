# -*- coding: utf-8 -*-
"""Bạch tuộc quái vật (mã làm việc bach_tuoc; con gốc của rig: monster_3616, game tham khảo). Dạng người dùng giao là DẠNG 2.

Cách làm = "reskin theo khung part" (skill pokiclash-spine-rig mục 00, mẫu rong_vay.py): mỗi part của rig gốc một ô đúng khung ảnh
vùng, trong ô là hình bóng kín tô phẳng theo THIẾT KẾ CỦA MÌNH; Codex vẽ lại sạch; rig dùng nguyên xương, lưới, chuyển động của họ.
HƯỚNG: con gốc nhìn sang PHẢI (+x): con mắt nhìn về phía ba xúc tu NGẮN ở bên phải; hai xúc tu to lộ mặt dưới nằm ở bên trái là
phía SAU. KHÔNG lật ngang. (2026-11-12 tôi đoán sai là nó nhìn trái vì các clip quật xúc tu to về bên trái, đã lật cả con; người dùng:
"hướng mắt bạn ngược rồi, trong game mắt hướng cùng với bên xúc tu ngắn".)

    bach_tuoc.py part_goc         ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3616/parts/ (chỉ để xem)
    bach_tuoc.py bo_cuc           sơ đồ bố cục phẳng 1536 × 1024 (đính vào prompt concept) → inbox/bach_tuoc_2/mau/bo_cuc.png
    bach_tuoc.py nhom_part        tờ hướng dẫn theo khung part (Q1, Q2...) → mau/part_<tờ>.png + .json
    bach_tuoc.py cat_part <tờ>    cắt tờ N_<tờ> Codex vẽ → manh/part/<hình>.png, đo IoU
    bach_tuoc.py so_part          tờ so mảnh với hình bóng → mau/so_part.png
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "bach_tuoc"
MON = "monster_3616"
# DẠNG: biến môi trường BT_DANG = 1 | 2 (mặc định 2). Dạng 2 là con bám con gốc (người dùng duyệt 2026-11-12); dạng 1 là CON NON trên
# CÙNG rig, cùng lưới, cùng clip (người dùng 2026-11-12: "làm dạng 1, con non"): da vẽ lại trong cùng khung part, đổi tỉ lệ vài xương.
K = int(os.environ.get("BT_DANG", "2"))
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
MANH = os.path.join(BASE, "manh")
TAI = os.path.join(BASE, "tai_ve")
TAI_CHUNG = os.path.join(HERE, "inbox", f"{CODE}_2", "tai_ve")      # ảnh dùng chung hai dạng: hố đất, bạch tuộc con, xúc tu dài
W, H = 1536, 1024
SC = 0.78                                        # đơn vị rig con gốc → pixel khung concept
Z = 2                                            # ảnh vùng atlas phóng 2 lần = đúng cỡ thế giới của họ
INK = (43, 33, 24)
# bảng màu ĐỀ XUẤT của Claude, chờ duyệt concept. Bản 1 (tím mực + mũ vỏ ốc) bị trả 2026-11-12: "không nhất thiết phải có phần tàu ở
# trên, có thể bỏ; xúc tu cũng có thể làm khác đi", "màu tím này không đẹp, thử phối đúng màu hồng đỏ giống bạch tuộc bình thường".
PAL = dict(da=(212, 92, 78), dom=(176, 62, 58), bung=(247, 228, 210), giac=(236, 170, 150), gai=(138, 44, 48), mat=(244, 200, 74))
# part THÊM của mình (con gốc không có). Toạ độ theo thế giới của con gốc ở dáng gốc (con nhìn về +x), đơn vị của họ.
#   gai: mào gai thịt trên đỉnh đầu (tên, gốc, cao, rộng, hướng độ), vẽ SAU đầu (gốc gai nấp sau vòm đầu), bám da đầu ngay chỗ gốc
# Bản 2 lượt đầu có thêm MẮT XA và PHỄU phụt mực trên má: người dùng trả 2026-11-12 "hướng mặt/mắt sai rồi, xem lại con gốc, chỉ thấy
# 1 bên mắt, không có mồm" → mặt giữ đúng cách dựng của con gốc: nhìn NGHIÊNG, MỘT mắt giữa vòm đầu trong vành hốc mắt tròn, không mồm.
GAI = [("gai_1", (-100.0, 778.0), 190.0, 124.0, 100.0), ("gai_2", (-300.0, 742.0), 150.0, 104.0, 120.0), ("gai_3", (-448.0, 636.0), 112.0, 84.0, 140.0)]
MAT_XA = None
# đốm sẫm trên đầu (x, y, bán trục ngang, dọc) và tâm vết sẹo, theo concept đã duyệt, thế giới của rig (đơn vị con gốc)
DOM_DAU = [(14.0, 695.0, 48.0, 30.0), (132.0, 671.0, 21.0, 19.0), (-287.0, 655.0, 19.0, 17.0), (-379.0, 548.0, 26.0, 24.0),
           (180.0, 564.0, 66.0, 48.0), (290.0, 480.0, 19.0, 21.0), (202.0, 428.0, 26.0, 26.0), (287.0, 373.0, 32.0, 34.0),
           (153.0, 275.0, 34.0, 26.0), (-190.0, 300.0, 22.0, 20.0)]
SEO = (180.0, 564.0)
VANH, BUOU = 96.0, (-80.0, 84.0, 24.0)           # bán kính vành hốc mắt; bướu nhỏ sau – trên mắt (dx, dy, bán kính)
MAY = (-104.0, 128.0, 108.0, 58.0, 1.0)          # gờ mày: đầu sau (dx, dy), đầu trước (dx, dy) so với tâm mắt, hệ số bề dày
MI = (0.55, 0.05)                                # mép mí trên (phần bán kính mắt tính từ tâm lên): mắt mở, mắt lim dim
if K == 1:
    # CON NON (đề xuất của Claude, chờ duyệt concept): hồng san hô NHẠT hơn, đầu to (rig phóng xương đầu), mắt TO tròn gần kín vành,
    # mí và gờ mày nhẹ hơn (vẫn quả quyết, chưa dữ), mào mới nhú HAI gai nhỏ, ít đốm, chưa có sẹo, xúc tu ngắn hơn (rig thu xương gốc)
    PAL = dict(da=(238, 124, 108), dom=(206, 88, 82), bung=(250, 232, 214), giac=(240, 178, 160), gai=(170, 62, 64), mat=(246, 206, 84))
    GAI = [("gai_1", (-110.0, 776.0), 98.0, 96.0, 100.0), ("gai_2", (-300.0, 740.0), 72.0, 78.0, 120.0)]
    DOM_DAU = [(45.0, 723.0, 48.0, 32.0), (-270.0, 670.0, 26.0, 22.0), (-353.0, 558.0, 28.0, 24.0), (244.0, 548.0, 44.0, 34.0),
               (290.0, 390.0, 26.0, 28.0)]            # theo concept dạng 1 đã duyệt (L1_duyet.png)
    SEO = None
    VANH, BUOU = 128.0, (-104.0, 108.0, 22.0)
    MAY = (-92.0, 172.0, 110.0, 128.0, 0.62)
    MI = (0.78, 0.2)


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


def rig_goc():
    return os.path.join(sxs(), "web", "assets", "Monster", MON)


def scan():
    return os.path.join(sxs(), "scan", MON)


def loai(ten):
    return ("xuc_tu" if "shou" in ten else "san_ho" if "shanhu" in ten else "xich" if "suolian" in ten else "vo" if ten == "P_chuanban1"
            else "long_vo" if ten == "P_chuanban2" else "dau" if ten == "P_tou" else "mat")


def BO(ten):
    """part của con gốc KHÔNG dùng (mũ = mảnh thân tàu, mặt trong của nó, san hô trên mũ, xích)."""
    return loai(ten) in ("vo", "long_vo", "san_ho", "xich")


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_C = {}


def nap():
    """(ảnh vùng đã gỡ xoay {tên: RGBA}, att dáng gốc {tên hình: att}, danh sách att theo thứ tự vẽ)."""
    if not _C:
        _, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), "att_goc.json"), encoding="utf-8"))
        atts = [a for a in D["atts"] if a.get("region") in imgs]
        _C.update(imgs=imgs, by={a["att"]: a for a in atts}, atts=sorted(atts, key=lambda a: a["order"]), bones=D["bones"])
    return _C["imgs"], _C["by"], _C["atts"]


def part_goc(ten, z=1):
    """ảnh một part của con gốc cắt đúng theo lưới của nó (ảnh vùng atlas là chữ nhật nên dính mảnh bên cạnh)."""
    imgs, by, _ = nap()
    a = by[ten]
    im = imgs[a["region"]].convert("RGBA")
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    m = Image.new("L", (im.width * 4, im.height * 4), 0)
    d = ImageDraw.Draw(m)
    for t in np.array(a["tris"]).reshape(-1, 3):
        d.polygon([tuple(uv[i] * 4) for i in t], fill=255, outline=255)
    A = np.asarray(im).copy()
    A[..., 3] = (A[..., 3].astype(np.float32) * np.asarray(m.resize(im.size, Image.LANCZOS)) / 255.0).astype(np.uint8)
    out = Image.fromarray(A, "RGBA")
    return out if z == 1 else out.resize((im.width * z, im.height * z), Image.LANCZOS)


def aff(ten, z=Z):
    """affine (bình phương tối thiểu) pixel ô part (phóng z) → thế giới của họ ở dáng gốc: world = [u, v, 1] @ M."""
    imgs, by, _ = nap()
    a = by[ten]
    im = imgs[a["region"]]
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width * z, im.height * z])
    xy = np.array(a["xy"], float).reshape(-1, 2)
    M, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], xy, rcond=None)
    return M


def bong(ten, z=Z):
    """hình bóng KÍN của part (làm trơn nhẹ, không mang nét vẽ của họ), cỡ ảnh vùng × z."""
    a = np.asarray(part_goc(ten, z))
    k = loai(ten)
    m = (a[..., 3] > 100).astype(np.uint8)
    # làm trơn trên ảnh ĐÃ ĐỆM viền trống: chỗ part bị khung ảnh vùng cắt thẳng (phần họ giấu dưới mảnh khác) thì hai góc cắt bo tròn
    # lại thay vì thành mấu nhọn. Đầu bo mạnh hơn: mép phải của vòm đầu bị cắt thẳng ~70 đơn vị, con gốc che bằng xích, của mình lộ ra.
    le = 24 * z
    m = cv2.copyMakeBorder(m, le, le, le, le, cv2.BORDER_CONSTANT, value=0)
    if k != "xich":
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2 * z))
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, el(z))
    m = (cv2.GaussianBlur(m * 255, (0, 0), (13.0 if k == "dau" else 2.5) * z) > 127)[le:-le, le:-le]
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 2:
        m = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return m, a


def thiet_ke(ten, z=Z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Chỉ lấy của con gốc: hình bóng và
    ranh "mặt trên / mặt dưới xúc tu", chỗ đặt giác hút. Trả (RGB nền trắng, mặt nạ)."""
    m, a = bong(ten, z)
    k = loai(ten)
    h, w = m.shape
    im = np.full((h, w, 3), 255, np.uint8)
    rgb = a[..., :3].astype(int)
    al = a[..., 3] > 100
    s = z / 2.0
    pil = None
    if k == "xuc_tu":
        im[m] = PAL["da"]
        hong = cv2.medianBlur(((rgb[..., 0] > rgb[..., 2] + 15) & al).astype(np.uint8) * 255, 2 * int(3 * s) + 1) > 127
        hong = cv2.morphologyEx(hong.astype(np.uint8), cv2.MORPH_OPEN, el(3 * s)).astype(bool) & m
        im[hong] = PAL["bung"]
        ranh = cv2.morphologyEx(hong.astype(np.uint8), cv2.MORPH_GRADIENT, el(1.5 * s)).astype(bool) & m
        giac = hong & (rgb[..., 1] < 150) & (rgb[..., 0] > 150)
        giac = cv2.morphologyEx(giac.astype(np.uint8), cv2.MORPH_OPEN, el(2 * s))
        n, lab, st, cen = cv2.connectedComponentsWithStats(giac, 8)
        pil = Image.fromarray(im)
        d = ImageDraw.Draw(pil)
        for i in range(1, n):
            ar = st[i, cv2.CC_STAT_AREA]
            if not (40 * s * s < ar < 900 * s * s):
                continue
            bw, bh = st[i, cv2.CC_STAT_WIDTH] / 2 + 2 * s, st[i, cv2.CC_STAT_HEIGHT] / 2 + 2 * s
            cx, cy = cen[i]
            d.ellipse([cx - bw, cy - bh, cx + bw, cy + bh], fill=PAL["giac"], outline=INK, width=int(round(3 * s)))
            d.ellipse([cx - bw * 0.3, cy - bh * 0.3, cx + bw * 0.3, cy + bh * 0.3], fill=INK)
        da_ = cv2.erode((m & ~hong).astype(np.uint8), el(20 * s)).astype(bool)
        ys_, xs_ = np.nonzero(da_)
        if len(xs_) > 400:
            rs = np.random.RandomState(sum(ord(ch) for ch in ten) * 7 % 9973)
            dd = []
            for _ in range(200):
                q = rs.randint(len(xs_))
                x, y, r = xs_[q], ys_[q], rs.uniform(9, 15) * s
                if any(np.hypot(x - px, y - py) < 70 * s for px, py in dd):
                    continue
                dd.append((x, y))
                d.ellipse([x - r, y - r * 0.85, x + r, y + r * 0.85], fill=PAL["dom"], outline=INK, width=int(round(2 * s)))
                if len(dd) >= 2:
                    break
        im = np.asarray(pil).copy()
        im[ranh] = INK
    elif k == "dau":
        im[m] = PAL["da"]
        pil = Image.fromarray(im)
        d = ImageDraw.Draw(pil)
        rs = np.random.RandomState(11)
        trong = cv2.erode(m.astype(np.uint8), el(26 * s)).astype(bool)
        ys, xs = np.nonzero(trong)
        F = the_gioi_vao_o(ten, z)
        _, by, _ = nap()
        e1 = np.array(by["P_yanjing1"]["xy"], float).reshape(-1, 2).mean(0)
        mat_o = [F(e1)]
        # đốm sẫm và vết sẹo đặt như concept đã duyệt (L1_duyet.png; đọc toạ độ trên concept rồi đổi về thế giới của rig)
        for (x, y, rx, ry) in DOM_DAU:
            c = F((x, y))
            d.ellipse([c[0] - rx * s, c[1] - ry * s, c[0] + rx * s, c[1] + ry * s], fill=PAL["dom"], outline=INK, width=int(round(3 * s)))
        if SEO:
            # sẹo: một vệt nhạt thuôn nhọn hai đầu, mép răng cưa nhẹ (như concept), không phải thanh thẳng
            a0, a1 = np.array([SEO[0] - 60.0, SEO[1] + 54.0]), np.array([SEO[0] + 58.0, SEO[1] - 58.0])
            v_ = a1 - a0
            nn = np.array([-v_[1], v_[0]]) / np.hypot(*v_)
            ts = np.linspace(0, 1, 15)
            tren = [a0 + v_ * t + nn * (9.0 * math.sin(math.pi * t) + (3.0 if i % 2 else -1.0) * math.sin(math.pi * t)) for i, t in enumerate(ts)]
            duoi = [a0 + v_ * t - nn * (9.0 * math.sin(math.pi * t) + (3.0 if i % 2 else -1.0) * math.sin(math.pi * t)) for i, t in enumerate(ts)][::-1]
            d.polygon([tuple(F(q)) for q in tren + duoi], fill=PAL["bung"])
            d.line([tuple(F(q)) for q in tren + duoi + tren[:1]], fill=INK, width=int(round(4 * s)))
        # vành hốc mắt tròn quanh con mắt (như con gốc: một vòng gồ quanh mắt + một bướu nhỏ phía sau – trên)
        c = F(e1)
        r = VANH * s
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=PAL["da"], outline=INK, width=int(round(3 * s)))
        cb = F((e1[0] + BUOU[0], e1[1] + BUOU[1]))          # bướu nhỏ ở phía sau – trên con mắt
        rb = BUOU[2] * s
        d.ellipse([cb[0] - rb, cb[1] - rb, cb[0] + rb, cb[1] + rb], fill=PAL["da"], outline=INK, width=int(round(3 * s)))
        # gờ mày dữ: MỘT nếp da dày thuôn hai đầu (không vẽ thanh thẳng: GPT chép thành thanh chữ nhật), trên con mắt, dốc xuống về
        # phía trước (con nhìn về +x)
        A_, B_ = np.array([e1[0] + MAY[0], e1[1] + MAY[1]]), np.array([e1[0] + MAY[2], e1[1] + MAY[3]])
        v = B_ - A_
        n_ = np.array([-v[1], v[0]]) / np.hypot(*v)
        if n_[1] < 0:
            n_ = -n_
        tren = [A_ + v * t + n_ * MAY[4] * (30.0 * math.sin(math.pi * t) ** 0.8 + 16.0 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 24)]
        duoi = [A_ + v * t + n_ * MAY[4] * (16.0 * math.sin(math.pi * t) - 14.0 * math.sin(math.pi * t) ** 0.8) for t in np.linspace(1, 0, 24)]
        d.polygon([tuple(F(q)) for q in tren + duoi], fill=PAL["gai"], outline=INK)
        d.line([tuple(F(q)) for q in tren + duoi + tren[:1]], fill=INK, width=int(round(4 * s)))
        im = np.asarray(pil).copy()
        im[~m] = 255
    elif k == "vo":
        im[m] = PAL["vo"]
        dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
        for lv in (0.36, 0.72):
            c = (dt > dt.max() * lv).astype(np.uint8)
            im[cv2.morphologyEx(c, cv2.MORPH_GRADIENT, el(1.5 * s)).astype(bool) & m] = PAL["gan"]
        pil = Image.fromarray(im)
        d = ImageDraw.Draw(pil)
        xs = np.nonzero(m.any(axis=0))[0]
        for f, r in ((0.16, 13), (0.3, 9), (0.47, 15), (0.63, 10), (0.76, 12)):
            x = int(xs[0] + f * (xs[-1] - xs[0]))
            y = int(np.argmax(dt[:, x]))
            if dt[y, x] < 20 * s:
                continue
            r *= s
            d.ellipse([x - r, y - r, x + r, y + r], fill=PAL["ha"], outline=INK, width=int(round(3 * s)))
            d.ellipse([x - r * 0.35, y - r * 0.35, x + r * 0.35, y + r * 0.35], fill=INK)
        im = np.asarray(pil).copy()
    elif k == "mat":
        M = aff(ten, z)
        A = M[:2].T                                  # cột = ảnh của trục u, v trong thế giới
        Ai = np.linalg.inv(A)
        ys, xs = np.nonzero(m)
        c = np.array([xs.mean(), ys.mean()])
        rw = np.sqrt(m.sum() / np.pi)
        ngang = Ai @ np.array([1.0, 0.0])
        ngang /= np.linalg.norm(ngang)                # hướng nằm ngang của thế giới, trong khung ô
        doc = Ai @ np.array([0.0, 1.0])
        doc /= np.linalg.norm(doc)                    # hướng LÊN của thế giới, trong khung ô
        pil = Image.fromarray(im)
        d = ImageDraw.Draw(pil)
        yy, xx = np.mgrid[0:h, 0:w]
        rel = np.stack([xx - c[0], yy - c[1]], -1)
        if ten == "P_yanjing 3":                      # nhắm: mí da + một nét mực dày nằm ngang
            im[m] = PAL["gai"]
            im[m & (np.abs(rel @ doc) < 5 * s) & (np.abs(rel @ ngang) < rw * 0.8)] = INK
        else:
            im[m] = PAL["mat"]
            lech = rw * 0.16                          # con ngươi lệch về phía trước (+x, phía xúc tu ngắn): mắt nhìn theo hướng mặt
            im[m & (np.abs(rel @ doc) < rw * 0.2) & (np.abs(rel @ ngang - lech) < rw * 0.56)] = INK      # con ngươi NGANG
            cham = c + doc * rw * 0.42 + ngang * rw * 0.5
            im[np.hypot(xx - cham[0], yy - cham[1]) < 4.5 * s] = 255
            # mí trên dốc về phía trước (+x): mắt mở đã lườm, lim dim thì mí hạ quá nửa
            t = np.radians(20)
            n_ = doc * np.cos(t) + ngang * np.sin(t)              # pháp tuyến của mép mí
            muc_ = rw * (MI[1] if ten == "P_yanjing2" else MI[0])
            im[m & ((rel @ n_) > muc_)] = PAL["gai"]
            im[m & (np.abs(rel @ n_ - muc_) < 3.5 * s)] = INK
    else:
        im[m] = PAL[k]
    im[m & ~cv2.erode(m.astype(np.uint8), el(5 * s)).astype(bool)] = INK
    im[~m] = 255
    return im, m


def the_gioi_vao_o(ten, z=Z):
    """hàm đổi điểm thế giới (dáng gốc của họ) → pixel trong ô part (× z), theo affine của lưới part."""
    Mi = np.linalg.inv(np.c_[aff(ten, z), [0, 0, 1]])
    return lambda p: (np.r_[np.asarray(p, float), 1.0] @ Mi)[:2]


def anh_gai(cao, rong, z=Z):
    """một gai thịt của mào (thiết kế của mình): mũi nhọn hơi cong, gốc bầu; ảnh dựng đứng (mũi lên trên), gốc ở giữa đáy.
    Trả (RGB, mặt nạ, lề): ảnh cỡ (rong + 2 lề) × (cao + 2 lề) (× z / 2), lề 8."""
    S = 4
    le = 8
    w, h = int((rong + 2 * le) * z / 2), int((cao + 2 * le) * z / 2)
    pil = Image.new("L", (w * S, h * S), 0)
    d = ImageDraw.Draw(pil)
    k = z / 2 * S
    bx, by_ = (rong / 2 + le) * k, (cao + le) * k
    pts = []
    for t in np.linspace(0, 1, 30):                      # sườn trái: từ gốc trái lên mũi (cong lõm nhẹ)
        pts.append((bx - rong / 2 * k * (1 - t) ** 1.5 + 0.10 * rong * k * math.sin(math.pi * t), by_ - cao * k * t))
    for t in np.linspace(1, 0, 30):                      # sườn phải: từ mũi về gốc phải (cong lồi)
        pts.append((bx + rong / 2 * k * (1 - t) ** 0.75 + 0.10 * rong * k * math.sin(math.pi * t), by_ - cao * k * t))
    d.polygon(pts, fill=255)
    m = np.asarray(pil.resize((w, h), Image.LANCZOS)) > 127
    im = np.full((h, w, 3), 255, np.uint8)
    im[m] = PAL["gai"]
    im[m & ~cv2.erode(m.astype(np.uint8), el(5 * z / 2)).astype(bool)] = INK
    return im, m, le


def trong_so_da(ten, p):
    """trọng số xương của da part `ten` ngay tại điểm thế giới p (toạ độ trọng tâm trong tam giác lưới chứa p; ngoài lưới: đỉnh gần
    nhất) → {chỉ số xương: trọng số}. Dùng cho mảnh thêm cứng bám da (gai trên đầu)."""
    _, by, _ = nap()
    a = by[ten]
    Q = np.array(a["xy"], float).reshape(-1, 2)
    p = np.asarray(p, float)
    for t in np.array(a["tris"]).reshape(-1, 3):
        A, B_, C = Q[t]
        v0, v1, v2 = B_ - A, C - A, p - A
        den = v0[0] * v1[1] - v0[1] * v1[0]
        if abs(den) < 1e-9:
            continue
        b1 = (v2[0] * v1[1] - v2[1] * v1[0]) / den
        b2 = (v0[0] * v2[1] - v0[1] * v2[0]) / den
        if b1 >= -1e-6 and b2 >= -1e-6 and b1 + b2 <= 1 + 1e-6:
            out = {}
            for vi, bw in zip(t, (1 - b1 - b2, b1, b2)):
                for k_, w in a["w"][vi]:
                    out[k_] = out.get(k_, 0.0) + bw * w
            return out
    i = int(np.argmin(np.hypot(*(Q - p).T)))
    return {k_: w for k_, w in a["w"][i]}


def khung_T():
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["cur"]])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    cx = W / 2 - (x0 + x1) / 2 * SC                  # không lật: x khung = cx + x·SC
    oy = (H + (y1 - y0) * SC) / 2 + y0 * SC
    return lambda p: np.stack([cx + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


def bo_cuc(luu=True, chi=None):
    """sơ đồ bố cục: các part (thiết kế của mình) đặt đúng chỗ dáng gốc, đúng thứ tự vẽ, lật ngang cho nhìn sang phải; bỏ mũ, san hô,
    xích của con gốc; thêm mào gai (sau đầu) và mắt xa (trên đầu)."""
    imgs, by, atts = nap()
    T = khung_T()
    S2 = 2
    can = [Image.new("RGBA", (W * S2, H * S2), (255, 255, 255, 255))]

    def dan(im, m, V, uv, tris):
        src = Image.fromarray(np.dstack([im, m.astype(np.uint8) * 255]), "RGBA").convert("RGBa")
        lay = Image.new("RGBa", can[0].size, (0, 0, 0, 0))
        _tris(lay, src, T(V) * S2, uv, tris)
        can[0] = Image.alpha_composite(can[0], lay.convert("RGBA"))

    Q4 = np.array([[0, 1, 2], [0, 2, 3]])
    for a in atts:
        if not a["cur"] or BO(a["att"]) or (chi and a["att"] not in chi):
            continue
        if a["att"] == "P_tou":
            for g in GAI:
                im, m, V, uv = o_gai(g[0])
                dan(im, m, V, uv, Q4)
        im, m = thiet_ke(a["att"])
        uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([m.shape[1], m.shape[0]])
        dan(im, m, np.array(a["xy"], float).reshape(-1, 2), uv, np.array(a["tris"]).reshape(-1, 3))
        if a["att"] == "P_yanjing1" and MAT_XA:
            dan(im, m, mat_xa(a), uv, np.array(a["tris"]).reshape(-1, 3))
    out = can[0].convert("RGB").resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        out.save(os.path.join(MAU, "bo_cuc.png"))
        print(os.path.join(MAU, "bo_cuc.png"))
    return out


def mat_xa(a):
    """đỉnh thế giới của mắt xa: mắt gần (att a) lật ngang quanh tâm, thu nhỏ, dời tới MAT_XA."""
    V = np.array(a["xy"], float).reshape(-1, 2)
    c = V.mean(0)
    return np.array(MAT_XA["tam"]) + (V - c) * np.array([-1.0, 1.0]) * MAT_XA["ti"]


def o_gai(ten):
    """một gai của mào: (RGB, mặt nạ, 4 góc thế giới theo thứ tự trên trái, trên phải, dưới phải, dưới trái, uv px tương ứng)."""
    _, goc, cao, rong, huong = next(g for g in GAI if g[0] == ten)
    im, m, le = anh_gai(cao, rong)
    h, w = m.shape
    th = np.radians(huong)
    len_ = np.array([np.cos(th), np.sin(th)])            # hướng mũi gai
    ngang = np.array([np.sin(th), -np.cos(th)])          # sang phải của ảnh
    g0 = np.array(goc) - len_ * 34.0                     # gốc gai chìm 34 đơn vị vào trong vòm đầu
    k = Z / 2.0                                          # px ảnh mỗi đơn vị

    def P(u, v):                                         # pixel ảnh → thế giới
        return g0 + ngang * (u / k - (rong / 2 + le)) + len_ * ((cao + le) - v / k)

    V = np.array([P(0, 0), P(w, 0), P(w, h), P(0, h)])
    uv = np.array([[0, 0], [w, 0], [w, h], [0, h]], float)
    return im, m, V, uv


def anh_part(ten):
    """ảnh của một part cho rig, cỡ ảnh vùng × Z: bản Codex vẽ (manh/part/<hình>.png) nếu đã có, không thì DA TẠM = thiết kế phẳng
    bằng mã (để dựng rig, thử clip trước khi concept được duyệt). Trả (RGBA, True nếu là da tạm)."""
    p = os.path.join(MANH, "part", ten.replace(" ", "") + ".png")
    if os.path.exists(p):
        return Image.open(p).convert("RGBA"), False
    im, m = thiet_ke(ten)
    return Image.fromarray(np.dstack([im, m.astype(np.uint8) * 255]), "RGBA"), True


def cat_ho():
    """tách ảnh hố đất (tai_ve/H01*.png, một ảnh cả hố) thành hai lớp → manh/ho_sau.png (lòng hố + vành sau + hai đầu), manh/ho_truoc.png
    (vành trước: phần đất nằm dưới đường ngang qua tâm lòng hố và ngoài lòng hố), cùng khung đã cắt sát; manh/ho.json ghi elip lòng hố
    (tâm, bán trục, px trong khung đã cắt) để rig đặt mặt nạ cắt. Ảnh chưa có thì vẽ hố tạm bằng mã."""
    from quai import anh
    os.makedirs(MANH, exist_ok=True)
    path = anh.to_moi_nhat(TAI_CHUNG, "H01") if os.path.isdir(TAI_CHUNG) else None
    if path:
        tt = anh.doc_to(path, dien_tich_min=120, gop_px=400)
        rgba = tt.rgba.copy()
        tam = False
    else:
        pil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(pil)
        d.ellipse([78, 330, 1458, 760], fill=(140, 106, 72, 255), outline=INK + (255,), width=6)
        d.ellipse([178, 370, 1358, 670], fill=(35, 28, 25, 255), outline=INK + (255,), width=5)
        rgba = np.asarray(pil).copy()
        tam = True
    al = rgba[..., 3] > 127
    toi = al & (rgba[..., :3].max(axis=2) < 70)
    toi = cv2.morphologyEx(toi.astype(np.uint8), cv2.MORPH_OPEN, el(9))
    n, lab, st, cen = cv2.connectedComponentsWithStats(toi, 8)
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    long_ = cv2.morphologyEx((lab == i).astype(np.uint8), cv2.MORPH_CLOSE, el(15)).astype(bool)
    ys, xs = np.nonzero(long_)
    cx, cy, a_, b_ = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2, (xs.max() - xs.min()) / 2, (ys.max() - ys.min()) / 2
    yy = np.arange(rgba.shape[0])[:, None]
    truoc = al & ~cv2.dilate(long_.astype(np.uint8), el(2)).astype(bool) & (yy > cy)
    # mẩu đất rời nằm dưới tâm cũng thuộc lớp trước; lớp sau = phần còn lại
    # lớp sau CHỜM xuống dưới đường tách 8 px (nằm dưới lớp trước): hai lớp chỉ giáp mép nhau thì lọc ảnh để hở một vạch nền mảnh
    sau = al & (~truoc | (yy <= cy + 8))
    ysa, xsa = np.nonzero(al)
    x0, y0, x1, y1 = xsa.min(), ysa.min(), xsa.max() + 1, ysa.max() + 1
    for ten, m in (("ho_sau", sau), ("ho_truoc", truoc)):
        c = rgba.copy()
        c[..., 3] = np.where(m, c[..., 3], 0)
        Image.fromarray(c[y0:y1, x0:x1], "RGBA").save(os.path.join(MANH, ten + ".png"))
    json.dump({"w": int(x1 - x0), "h": int(y1 - y0), "cx": float(cx - x0), "cy": float(cy - y0), "a": float(a_), "b": float(b_), "tam": tam,
               "nguon": path or ""}, open(os.path.join(MANH, "ho.json"), "w", encoding="utf-8"), indent=1)
    print(f"hố {'TẠM' if tam else os.path.basename(path)}: khung {x1 - x0} x {y1 - y0}, lòng hố tâm ({cx - x0:.0f}, {cy - y0:.0f}) bán trục {a_:.0f} x {b_:.0f}")


def ds_o():
    """các ô của tờ mảnh: (tên file mảnh, tên part gốc, RGB, mặt nạ, z). Mỗi part của rig một ô đúng khung ảnh vùng (× z); gai một ô."""
    _, _, atts = nap()
    out = []
    for a in atts:
        t = a["att"]
        if BO(t):
            continue
        g = part_goc(t)
        z = 4 if max(g.size) * 2 < 300 else 2
        im, m = thiet_ke(t, z)
        out.append((t.replace(" ", ""), t, im, m, z))
    for g in GAI:
        im, m, _, _ = o_gai(g[0])
        out.append((g[0], g[0], im, m, Z))
    return out


def nhom_part():
    """tờ hướng dẫn theo khung part: mỗi ô là hình bóng KÍN của part tô phẳng theo thiết kế của mình, viền sẫm đúng mép → mau/part_Q<k>.png
    + part_Q<k>.json (ô của từng part). Codex vẽ lại sạch, giữ nguyên hình bóng (build_bach_tuoc.py build_parts)."""
    cells = sorted(ds_o(), key=lambda c: -c[3].shape[0])
    sheets, cur, x, y, hh = [], [], 40, 40, 0
    for c in cells:
        h, w = c[3].shape
        if x + w + 40 > W:
            x, y, hh = 40, y + hh + 50, 0
        if y + h + 40 > H:
            sheets.append(cur)
            cur, x, y, hh = [], 40, 40, 0
        cur.append((c, x, y))
        x += w + 50
        hh = max(hh, h)
    if cur:
        sheets.append(cur)
    os.makedirs(MAU, exist_ok=True)
    for f in os.listdir(MAU):
        if f.startswith("part_Q"):
            os.remove(os.path.join(MAU, f))
    for k, sh in enumerate(sheets, 1):
        im = np.full((H, W, 3), 255, np.uint8)
        khung = {}
        for (ten, goc, cim, m, z), x, y in sh:
            h, w = m.shape
            im[y:y + h, x:x + w] = cim
            khung[ten] = {"x": x, "y": y, "w": w, "h": h, "z": z, "goc": goc}
        Image.fromarray(im).save(os.path.join(MAU, f"part_Q{k}.png"))
        json.dump(khung, open(os.path.join(MAU, f"part_Q{k}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"Q{k}:", ", ".join(f"{t} (x{v['z']})" for t, v in khung.items()))
    print(len(sheets), "tờ")


def cat_part(to):
    """cắt tờ N_<tờ> Codex vẽ: mỗi part lấy đúng Ô của nó (ô = khung ảnh vùng của part), tách nền trắng, cắt sát hình bóng (nới 3 px),
    chỗ vẽ hụt lấy màu tờ hướng dẫn, kẻ nét mực dọc phía trong mép lưới → manh/part/<tên>.png cỡ ảnh vùng × Z. Đo IoU với hình bóng,
    ghi manh/part/_iou.json; chỉ ghi đè khi bản mới khít hơn."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, f"N_{to}")
    if not path:
        print(to, "chưa có ảnh")
        return
    khung = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, f"_N_{to}_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=300, gop_px=12)
    gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    _, by, _ = nap()
    pso = os.path.join(ra, "_iou.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    for ten, kv in khung.items():
        x, y, w, h, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + h, x:x + w].min(axis=2) < 236                       # hình bóng trên tờ hướng dẫn
        cell = tt.rgba[y:y + h, x:x + w].copy()
        lab = tt.lab[y:y + h, x:x + w]
        ids = [i for m in tt.manh for i in m["ids"]]
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[g].ravel().tolist()) - {0}:
            if i in ids:
                giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & g).sum() / max(1, (a | g).sum())
        sat = cv2.dilate(g.astype(np.uint8), el(3 * z / 2)).astype(bool)
        cell[..., 3][~sat] = 0
        a &= sat
        cu = SO.get(ten, [0, ""])
        if cu[1] != to and cu[0] >= iou:
            print(f"  {ten}: IoU {iou:.2f}, giữ bản {cu[1]} (IoU {cu[0]:.2f})")
            continue
        ho = g & ~a
        if ho.any():                                                     # chỗ vẽ hụt lấy màu tô gần nhất của tờ hướng dẫn
            gc = gd[y:y + h, x:x + w]
            to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105) & (gc.min(axis=2) < 236)
            if to_.any():
                _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                tra[lb[to_]] = gc[to_]
                cell[ho, :3] = tra[lb][ho]
                cell[ho, 3] = 255
        if kv["goc"] in by:                                              # nét mực dọc phía trong mép lưới (lưới ôm sát hình bóng)
            at = by[kv["goc"]]
            hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
            hm = np.zeros(a.shape, np.uint8)
            cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
            dai = hm.astype(bool) & ~cv2.erode(hm, el(5 * z / 2), borderValue=0).astype(bool)
            cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), to]
        out = Image.fromarray(cell, "RGBA")
        if z != Z:
            out = out.convert("RGBa").resize((w * Z // z, h * Z // z), Image.LANCZOS).convert("RGBA")
        out.save(os.path.join(ra, ten + ".png"))
        print(f"  {ten}: {w} x {h} (x{z}), trùng hình bóng hướng dẫn IoU {iou:.2f}, bù {int(ho.sum())} px")
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)


def cat_con():
    """bạch tuộc con (tai_ve/C01*.png): tách nền trắng, cắt sát → manh/bt_con.png (cao 360 px; rig tự thu nhỏ)."""
    from quai import anh
    path = anh.to_moi_nhat(TAI_CHUNG, "C01")
    if not path:
        print("chưa có C01")
        return
    tt = anh.doc_to(path, dien_tich_min=300, gop_px=60)
    rgba = Image.fromarray(tt.rgba, "RGBA")
    g = rgba.crop(rgba.getbbox())
    pt = os.path.join(MANH, "part", "P_tou.png")
    if os.path.exists(pt):                       # da bạch tuộc con cân về màu da của dạng này (dạng 1 hồng nhạt hơn dạng 2)
        o = np.asarray(g).copy()
        ref = np.asarray(Image.open(pt).convert("RGBA")).astype(int)
        da_ = lambda q: (q[..., 3] > 200) & (q[..., 0] > 190) & (q[..., 1] > 60) & (q[..., 1] < 135) & (q[..., 0] - q[..., 1] > 90)   # noqa: E731
        oi = o.astype(int)
        if da_(ref).sum() > 300 and da_(oi).sum() > 300:
            lech = np.median(ref[..., :3][da_(ref)], axis=0) - np.median(oi[..., :3][da_(oi)], axis=0)
            m = da_(oi)
            o[..., :3][m] = np.clip(oi[..., :3][m] + lech, 0, 255).astype(np.uint8)
            print("  lệch da", lech.round().astype(int).tolist())
            g = Image.fromarray(o, "RGBA")
    g = g.convert("RGBa")
    k = 360.0 / g.height
    g = g.resize((round(g.width * k), 360), Image.LANCZOS).convert("RGBA")
    g.save(os.path.join(MANH, "bt_con.png"))
    print(os.path.join(MANH, "bt_con.png"), g.size, "từ", os.path.basename(path))


def cat_voi():
    """xúc tu dài của appear (tai_ve/V01*.png: duỗi thẳng nằm ngang, gốc bên trái): tách nền trắng, cắt sát, đặt trục giữa hình đúng
    giữa chiều cao ảnh (luoi_dai lấy trục ngang qua giữa), cân màu da và kem về chuẩn của các mảnh thân → manh/voi.png (dài 1100 px)."""
    from quai import anh
    path = anh.to_moi_nhat(TAI_CHUNG, "V01")
    if not path:
        print("chưa có V01")
        return
    tt = anh.doc_to(path, dien_tich_min=300, gop_px=30)
    rgba = Image.fromarray(tt.rgba, "RGBA")
    g = np.asarray(rgba.crop(rgba.getbbox())).copy()
    al = g[..., 3] > 127
    ys = np.nonzero(al[:, : max(8, g.shape[1] // 12)].any(axis=1))[0]      # bề dày ở gốc → trục giữa
    truc = (ys.min() + ys.max()) / 2.0
    tren, duoi = int(round(truc)), g.shape[0] - int(round(truc))
    nua = max(tren, duoi) + 2
    out = np.zeros((2 * nua, g.shape[1], 4), np.uint8)
    out[nua - tren:nua - tren + g.shape[0]] = g
    ref = np.asarray(Image.open(os.path.join(MANH, "part", "P_tou.png")).convert("RGBA")).astype(int)
    r, gg, b = ref[..., 0], ref[..., 1], ref[..., 2]
    chuan = np.median(ref[..., :3][(ref[..., 3] > 200) & (r > 190) & (gg > 60) & (gg < 135) & (r - gg > 90)], axis=0)
    o = out.astype(int)
    da = (o[..., 3] > 200) & (o[..., 0] > 190) & (o[..., 1] > 60) & (o[..., 1] < 135) & (o[..., 0] - o[..., 1] > 90)
    if da.sum() > 300:
        lech = chuan - np.median(o[..., :3][da], axis=0)
        out[..., :3][da] = np.clip(o[..., :3][da] + lech, 0, 255).astype(np.uint8)
        print("  lệch da", lech.round().astype(int).tolist())
    im = Image.fromarray(out, "RGBA").convert("RGBa")
    k = 1100.0 / im.width
    im = im.resize((1100, max(2, round(im.height * k))), Image.LANCZOS).convert("RGBA")
    im.save(os.path.join(MANH, "voi.png"))
    print(os.path.join(MANH, "voi.png"), im.size, "từ", os.path.basename(path))


def can_mau():
    """cân màu da giữa các mảnh: mỗi tờ Codex tô đỏ một sắc hơi khác (ngón này sẫm hơn ngón kia, lắp cạnh nhau thấy lệch tông). Lấy
    trung vị màu DA (đỏ san hô, không phải mực, đốm sẫm, kem) của đầu làm chuẩn; ở từng mảnh xúc tu, cộng độ lệch trung vị vào mọi
    điểm da và điểm kem cũng cân về trung vị kem chung. Ghi đè manh/part/<tên>.png (chạy sau cat_part)."""
    ra = os.path.join(MANH, "part")

    def lop(a):
        rgb = a[..., :3].astype(int)
        al = a[..., 3] > 200
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        da = al & (r > 190) & (g > 60) & (g < 135) & (r - g > 90)                    # đỏ san hô
        kem = al & (r > 225) & (g > 200) & (b > 170)                                 # kem
        return da, kem

    ref = np.asarray(Image.open(os.path.join(ra, "P_tou.png")).convert("RGBA"))
    da0, _ = lop(ref)
    chuan_da = np.median(ref[..., :3][da0], axis=0)
    kems = []
    ten = [f[:-4] for f in sorted(os.listdir(ra)) if f.startswith("P_shou") and f.endswith(".png")]
    A = {t: np.asarray(Image.open(os.path.join(ra, t + ".png")).convert("RGBA")).copy() for t in ten}
    for t in ten:
        _, kem = lop(A[t])
        if kem.sum() > 300:
            kems.append(np.median(A[t][..., :3][kem], axis=0))
    chuan_kem = np.median(np.array(kems), axis=0) if kems else None
    for t in ten:
        a = A[t]
        da, kem = lop(a)
        ghi = []
        for m, chuan in ((da, chuan_da), (kem, chuan_kem)):
            if chuan is None or m.sum() < 300:
                continue
            lech = chuan - np.median(a[..., :3][m], axis=0)
            a[..., :3][m] = np.clip(a[..., :3][m].astype(float) + lech, 0, 255).astype(np.uint8)
            ghi.append(f"{lech.round().astype(int).tolist()}")
        Image.fromarray(a, "RGBA").save(os.path.join(ra, t + ".png"))
        print(f"  {t}: lệch da / kem {', '.join(ghi)}")
    print("chuẩn da", chuan_da.round().tolist(), "kem", None if chuan_kem is None else chuan_kem.round().tolist())


def so_part():
    """tờ so từng part đã cắt (manh/part) với hình bóng trên tờ hướng dẫn: ĐỎ = hình bóng mà mảnh không phủ (lắp vào lưới sẽ khuyết),
    XANH LÁ = mảnh vẽ thừa ra ngoài hình bóng (đã bị cắt sát nên thường không còn) → mau/so_part.png."""
    cells = []
    for f in sorted(os.listdir(MAU)):
        if not (f.startswith("part_Q") and f.endswith(".json")):
            continue
        to = f[5:-5]
        K_ = json.load(open(os.path.join(MAU, f), encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        for ten, v in K_.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm):
                continue
            x, y, w, h = v["x"], v["y"], v["w"], v["h"]
            g = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a = c[..., 3] > 127
            im = np.full((h, w, 3), 150, np.uint8)
            im[a] = c[..., :3][a]
            im[g & ~a] = (255, 0, 0)
            im[a & ~g] = (im[a & ~g] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
            cv2.putText(im, f"{to} {ten}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cells.append(im)
    Wd, x, y, hh, pos = 2000, 0, 0, 0, []
    for im in cells:
        h, w = im.shape[:2]
        if x + w > Wd:
            x, y, hh = 0, y + hh + 10, 0
        pos.append((x, y))
        x += w + 10
        hh = max(hh, h)
    S = np.full((y + hh, Wd, 3), 90, np.uint8)
    for im, (x, y) in zip(cells, pos):
        S[y:y + im.shape[0], x:x + min(im.shape[1], Wd - x)] = im[:, :Wd - x]
    Image.fromarray(S).save(os.path.join(MAU, "so_part.png"))
    print(os.path.join(MAU, "so_part.png"), len(cells), "part")


def xuat_part_goc():
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    _, _, atts = nap()
    for a in atts:
        part_goc(a["att"]).save(os.path.join(ra, f"{a['order']:02d}_{a['att'].replace(' ', '')}.png"))
    print(ra, len(atts), "part")


def main(a):
    if a[:1] == ["part_goc"]:
        xuat_part_goc()
    elif a[:1] == ["bo_cuc"]:
        bo_cuc()
    elif a[:1] == ["cat_ho"]:
        cat_ho()
    elif a[:1] == ["nhom_part"]:
        nhom_part()
    elif a[:1] == ["cat_part"]:
        for t in a[1:]:
            cat_part(t)
    elif a[:1] == ["cat_con"]:
        cat_con()
    elif a[:1] == ["can_mau"]:
        can_mau()
    elif a[:1] == ["cat_voi"]:
        cat_voi()
    elif a[:1] == ["so_part"]:
        so_part()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
