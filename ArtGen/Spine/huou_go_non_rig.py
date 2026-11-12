# -*- coding: utf-8 -*-
"""Hươu gỗ DẠNG 1 (khúc gỗ non; tướng thứ 4 đảo Mộc): hình của mình chạy trên ĐÚNG rig của con gốc monster_3304.
Ghi chú: inbox/huou_go_ghichu.md. Cách làm như xuong_rong_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ (trừ xương bóng), đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move` (game đo cú lao; cung
  bay của đòn thường và quãng đi vào của appear), `mieng` (chỗ bắn tia = giữa hai cành gạc), `cau` (chỗ và cỡ quả cầu năng lượng cho
  VFX), `mat_cong` (mặt nạ cắt ở mặt cổng), `cong` (cánh cổng rừng, nếu đã có ảnh).
- MẢNH: mỗi part một ảnh vẽ đúng khung ảnh vùng của part (HG_DANG=1 huou_go.py cat_part), lắp vào NGUYÊN lưới của họ. Mảnh thêm của
  mình: `mat_xa` (ụ mắt xa có mắt, bám xương ụ mắt xa bone39), `pha_le` (nụ pha lê trên mông, bám xương mông), `mieng_ha` (hình thứ
  hai của slot mồm: mồm há, bám xương mồm bone24).
- CHUYỂN ĐỘNG: clip dựng ở tầng điều khiển của rig gốc (huou_go_non_clip.py), runtime Spine thật nướng ra scan/sample_moi.json (biến
  đổi riêng đã áp: IK chân đã thành FK) → lệch so với dáng gốc cho mọi xương. Kênh riêng (kenh_rieng.json): ham → đổi hình mồm, cau
  → xương `cau`, bay → xương `move`, cong → cổng + mặt nạ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/huou_go_non_rig.py        → inbox/huou_go_1/rig/
    py -3 -I ArtGen/Spine/huou_go_non_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [luoi]          → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
os.environ["HG_DANG"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi, tienhoa  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import huou_go as HG  # noqa: E402
import huou_go_non_clip as RC  # noqa: E402

K = 1
KG = 1.0                     # đơn vị rig con gốc → đơn vị rig của mình
D_PX = 1.8                   # pixel ảnh atlas cho mỗi đơn vị rig
BO_TEN = ("shadow",)
CLIPS = [("appear", "hn_appear", False, None), ("idle", "hn_idle", True, None), ("walk", "hn_walk", True, None),
         ("attack", "hn_attack", False, None), ("cast", "hn_cast", False, None), ("skill", "hn_skill", False, None),
         ("hit", "hn_hit", False, None), ("die", "hn_die", False, None)]
VE_NGHI = ("appear", "attack", "cast", "skill", "hit")            # clip hết ở dáng nghỉ: hoà 0,2 s cuối về khung 0 idle
MAT_XA = 3000.0              # mặt nạ cổng nằm xa chừng này ngoài clip appear (không cắt gì)
TAN = 0.45                   # die: giữ dáng cuối rồi mờ dần chừng này giây
IMPACT = {"attack": (0.05, 0.24, 0.06), "skill": (0.14, 0.75, 0.12)}       # khựng giây, rung, bật lùi × chiều cao
BO_CAO = ("JiaoL_01", "JiaoL_02", "JiaoL_03", "JiaoL_04", "JiaoR_01", "JiaoR_02", "JiaoR_03")       # chiều cao game đo trên khúc gỗ
# mảnh thêm: (bề rộng thế giới, slot đứng ngay SAU slot nào của họ, xương bám)
# mat_xa (ụ mắt xa có tròng) ĐÃ BỎ: người dùng 2026-11-12 "bạn xem con gốc mắt bên kia không thấy tròng mắt đâu, chỉ thấy mắt nó lồi ra
# thôi" → bên phải chỉ còn ụ gỗ YanL_01 của rig (nấp sau khúc gỗ, lồi ra mép phải), đúng như con gốc
THEM = {"pha_le": (44.0, "P_shenti", "bone")}
MIENG_HA = 76.0              # bề rộng thế giới của mồm há
CONG = os.path.join(HG.HERE, "inbox", "huou_go_1", "manh", "cong")          # cong_sau.png, cong_truoc.png (huou_go.py cat_cong)
CONG_CAO = 400.0             # chiều cao cánh cổng (đơn vị rig) ở dạng 1


def nap_goc():
    scan = HG.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, I, scan


def ti_le_atlas(D):
    """pixel ảnh vùng atlas của họ cho mỗi đơn vị rig (đo trên khúc gỗ)."""
    _, imgs, _ = HG.nap()
    a = [x for x in D["atts"] if x["att"] == "P_tou" and x["cur"]][0]
    im = imgs[a["region"]]
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    xy = np.array(a["xy"], float).reshape(-1, 2)
    return float(np.hypot(*(uv.max(0) - uv.min(0))) / np.hypot(*(xy.max(0) - xy.min(0))))


def anh_part(ten, a_tl):
    """ảnh part của mình (cỡ ô trên tờ = ảnh vùng × z) → cỡ atlas (D_PX px mỗi đơn vị rig)."""
    z = {t: z_ for to, (z_, ds) in HG.TO.items() for t in ds}[ten]
    pth = os.path.join(HG.MANH, "part", ten + ".png")
    if not os.path.exists(pth):
        raise SystemExit("thiếu ảnh part " + pth)
    g = Image.open(pth).convert("RGBA")
    kq = D_PX / (a_tl * z)
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


def cat_sat(path, le=3):
    g = Image.open(path).convert("RGBA")
    bb = g.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
    return g.crop((max(0, bb[0] - le), max(0, bb[1] - le), min(g.width, bb[2] + le), min(g.height, bb[3] + le)))


def anh_them(ten, rong):
    """ảnh ô thêm, cắt sát, co về bề rộng thế giới `rong`."""
    c = cat_sat(os.path.join(HG.MANH, "part", ten + ".png"))
    w = max(2, round(rong * D_PX))
    return anh.loang_mau(c.convert("RGBa").resize((w, max(2, round(c.height * w / c.width))), Image.LANCZOS).convert("RGBA"))


def mat_xa_anh(a_tl):
    """mắt bên PHẢI (ụ mắt xa) dựng từ chính hai mảnh của mắt trái cho GIỐNG nhau (người dùng 2026-11-12: "mắt bên phải dạng 1 nhìn
    không giống mắt bên trái"; bản đầu là một vành bầu dục dẹt vẽ riêng): ụ gỗ = YanR_02 lật ngang, ép hẹp 0,78 (nhìn chếch); tròng
    = YanR_01 xoay 180° (chấm kem xuống dưới – ra ngoài: hai mắt nhìn hai hướng), ép hẹp 0,66, lồi qua mép phải của ụ như bên trái."""
    u = anh_part("YanR_02", a_tl).transpose(Image.FLIP_LEFT_RIGHT)
    u = u.resize((max(2, round(u.width * 0.78)), u.height), Image.LANCZOS)
    tr = anh_part("YanR_01", a_tl).rotate(180)
    tr = tr.resize((max(2, round(tr.width * 0.66)), tr.height), Image.LANCZOS)
    lo = round(tr.width * 0.30)                   # tròng thò ra ngoài mép ụ chừng này
    W_, H_ = u.width + lo, max(u.height, tr.height)
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    im.alpha_composite(u, (0, (H_ - u.height) // 2))
    im.alpha_composite(tr, (W_ - tr.width, (H_ - tr.height) // 2))
    return anh.loang_mau(im)


# xoá nét mực ở chỗ nối (người dùng 2026-11-12, chuyển tiếp qua phiên Gạc Đá: "dạng 1 ở các khớp nối chân, thân bỏ outline đen đi
# để liền mạch"): cặp (mảnh nằm TRÊN, mảnh kề nằm DƯỚI). Nét mực trên vành mép của mảnh trên mà ở dáng gốc rơi sâu trong mảnh dưới thì
# thay bằng màu tô gần nhất.
# khúc chân dưới đè khúc trên, hai mép gần trùng nhau: sâu 7 px, không thì mép ngoài của khúc dưới mất viền (viền khúc trên nấp dưới nó)
NOI = [("P_tuiR_H_2", "P_tuiR_H_1"), ("P_tuiL_H_2", "P_tuiL_H_1"), ("P_tuiR_Q_2", "P_tuiR_Q_1"), ("P_tuiL_Q_2", "P_tuiL_Q_1"),
       ("P_tuiR_Q_1", "P_tou", "mo"), ("P_tuiL_Q_1", "P_tou", "mo"),
       ("P_shenti", "P_tuiR_H_1"), ("P_shenti", "P_tuiL_H_1"), ("P_tou", "P_tuiL_H_1"), ("P_tou", "P_tuiR_H_1"),
       # ranh mông – khúc gỗ: bản đầu tôi giữ nét (concept có) → người dùng 2026-11-12 (chuyển tiếp lần 3, kèm ảnh cận): "phần này vẫn
       # có outline, xem cả cho dạng 2" → bỏ luôn; mọi chỗ hai mảnh THÂN / CHÂN cùng màu gỗ chồng nhau đều không để nét mực
       # sâu 9 px: chỉ xoá mép TRÁI khúc gỗ (nằm sâu trong mông); mép ĐÁY khúc gỗ chạy trùng mép đáy mông nên xoá sẽ nham nhở
       ("P_tou", "P_shenti")]


def _tg(att, w, h):
    return (np.array(att["uv"], float).reshape(-1, 2) * np.array([w, h]), np.array(att["xy"], float).reshape(-1, 2) * KG,
            np.array(att["tris"]).reshape(-1, 3))


def _bary(P, a, b, c):
    v0, v1, v2 = b - a, c - a, P - a
    den = v0[0] * v1[1] - v0[1] * v1[0]
    den = den if abs(den) > 1e-9 else 1e-9
    b1 = (v2[:, 0] * v1[1] - v2[:, 1] * v1[0]) / den
    b2 = (v0[0] * v2[:, 1] - v0[1] * v2[:, 0]) / den
    return 1 - b1 - b2, b1, b2


# độ sâu (px ảnh atlas) tính từ viền ngoài của khối hợp hai mảnh mà nét mực mới bị xoá. Xoá là NƯỚNG theo dáng gốc; lúc cử động
# khúc chân trượt ra khỏi thân vài đơn vị, xoá nông quá (5 px) thì lộ một đoạn mép không viền ngay dưới mép thân
SAU = 11
_TG = {}


def _tg_px(im, att):
    k = (id(im), att["slot"])
    if k not in _TG:
        _TG[k] = (im, the_gioi_px(im, att))       # giữ im để id không bị dùng lại
    return _TG[k][1]


def xoa_muc_noi(imA, attA, imB, attB, vanh=7, sau=5, mo=False):
    """trả ảnh A đã xoá nét mực ở vành mép (rộng `vanh` px) tại những điểm NẰM HẲN BÊN TRONG khối hợp A ∪ B ở dáng gốc (cách viền
    ngoài của khối hợp hơn `sau` px ảnh atlas). Điểm vành nằm sát viền ngoài của khối hợp (mép A giáp nền, hoặc giáp một mảnh KHÁC
    không phải B, ví dụ chân gần đè lên chân xa) giữ nguyên nét. (Bản đầu xét "nằm sâu trong B": khúc chân dưới mất viền hai bên ở
    chỗ mép nó gần trùng mép khúc trên, đáy khúc gỗ nham nhở chỗ trùng đáy mông: người dùng "vẫn bị lỗi nhỏ ở gần chân".)"""
    A = np.asarray(imA).copy()
    al = A[..., 3] > 127
    rgb = A[..., :3].astype(int)
    muc = al & (rgb.max(axis=2) < 100)
    k = np.ones((2 * vanh + 1, 2 * vanh + 1), np.uint8)
    xet = (A[..., 3] > 8) & ~cv2.erode(al.astype(np.uint8), k).astype(bool)
    WA, WB = _tg_px(imA, attA), _tg_px(imB, attB)
    okA, okB = ~np.isnan(WA[..., 0]), ~np.isnan(WB[..., 0])
    mA, mB = okA & al, okB & (np.asarray(imB)[..., 3] > 127)
    if not mA.any() or not mB.any():
        return imA, 0
    P = np.concatenate([WA[mA], WB[mB]])
    o = P.min(axis=0) - 16
    kt = np.ceil((P.max(axis=0) + 16 - o) * D_PX).astype(int)
    U = np.zeros((kt[1], kt[0]), np.uint8)
    for W_, m_ in ((WA, mA), (WB, mB)):
        ij = np.round((W_[m_] - o) * D_PX).astype(int)
        U[ij[:, 1], ij[:, 0]] = 1
    U = cv2.morphologyEx(U, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    trong_khoi = cv2.erode(U, np.ones((2 * sau + 1, 2 * sau + 1), np.uint8)).astype(bool)
    GB = np.zeros_like(U)
    ij = np.round((WB[mB] - o) * D_PX).astype(int)
    GB[ij[:, 1], ij[:, 0]] = 1
    GB = cv2.dilate(cv2.morphologyEx(GB, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), np.ones((5, 5), np.uint8)).astype(bool)
    cand = xet & okA
    ys, xs = np.nonzero(cand)
    if not len(ys):
        return imA, 0
    ij = np.clip(np.round((WA[ys, xs] - o) * D_PX).astype(int), 0, [kt[0] - 1, kt[1] - 1])
    trong = trong_khoi[ij[:, 1], ij[:, 0]] & GB[ij[:, 1], ij[:, 0]]            # trong khối hợp VÀ chạm tới B (chỗ hai mảnh chồng nhau)
    if not trong.any():
        return imA, 0
    tot = (cv2.erode(al.astype(np.uint8), k).astype(bool) & ~cv2.dilate(muc.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
           & (rgb.max(axis=2) > 200))
    if not tot.any():
        return imA, 0
    _, lb = cv2.distanceTransformWithLabels((~tot).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
    tra[lb[tot]] = A[..., :3][tot]
    da = np.zeros(al.shape, np.uint8)
    da[ys[trong], xs[trong]] = 1
    da = cv2.morphologyEx(da, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) & xet.astype(np.uint8)
    yy, xx = np.nonzero(da)
    A[yy, xx, :3] = tra[lb[yy, xx]]
    # điểm trong suốt / ngoài lưới sát chỗ đã xoá cũng về màu gỗ (lọc tuyến tính kéo màu của chúng vào thành vệt mảnh)
    quanh = cv2.dilate(da, np.ones((5, 5), np.uint8)).astype(bool) & ((A[..., 3] <= 127) | (xet & ~okA))
    A[quanh, :3] = tra[lb][quanh]
    # chỗ nối nằm SÂU trong khối: cho mép mảnh ĐẶC hẳn và nới ra 5 px (màu gỗ). Mép mềm nửa trong suốt gỗ-đè-gỗ vẫn hiện thành quầng
    # sáng theo mép mảnh ở trang xem Spine (người dùng 2026-11-12: "phần chân bị lem nhem khá nhiều"); đặc tới ngoài mép lưới thì
    # cạnh nhìn thấy là cạnh lưới, hai bên cùng màu gỗ
    khoi2 = cv2.erode(U, np.ones((2 * (sau + 5) + 1, 2 * (sau + 5) + 1), np.uint8)).astype(bool)
    sau2 = trong & khoi2[ij[:, 1], ij[:, 0]]
    if sau2.any():
        d2 = np.zeros(al.shape, np.uint8)
        d2[ys[sau2], xs[sau2]] = 1
        noi = cv2.dilate(d2, np.ones((11, 11), np.uint8)).astype(bool) & (A[..., 3] < 255)
        A[noi, :3] = tra[lb][noi]
        A[noi, 3] = 255
    if mo:
        # mảnh A vẽ TRƯỚC thân có đốm: phần A nằm rất sâu trong B cho mờ dần tới trong suốt, để đốm của thân hiện xuyên qua thay vì bị
        # khối gỗ không viền của A che cụt (nhìn như đốm bị xén)
        sauB = cv2.erode(GB.astype(np.uint8), np.ones((2 * (sau + 8) + 1, 2 * (sau + 8) + 1), np.uint8)) & khoi2.astype(np.uint8)
        kc = cv2.distanceTransform(sauB, cv2.DIST_L2, 5)
        f = np.clip(1.0 - kc / 12.0, 0.0, 1.0)
        yy2, xx2 = np.nonzero(okA & (A[..., 3] > 0))
        ij2 = np.clip(np.round((WA[yy2, xx2] - o) * D_PX).astype(int), 0, [kt[0] - 1, kt[1] - 1])
        A[yy2, xx2, 3] = (A[yy2, xx2, 3] * f[ij2[:, 1], ij2[:, 0]]).astype(np.uint8)
    return Image.fromarray(A, "RGBA"), int(len(yy))


def the_gioi_px(im, att):
    """toạ độ thế giới (dáng gốc) của từng pixel ảnh part qua lưới của nó: mảng (cao, rộng, 2), NaN ngoài lưới."""
    U, V, T = _tg(att, im.width, im.height)
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    P = np.c_[xs.ravel() + 0.5, ys.ravel() + 0.5]
    Wd = np.full((len(P), 2), np.nan)
    for t in T:
        b0, b1, b2 = _bary(P, U[t[0]], U[t[1]], U[t[2]])
        ok = (b0 >= -0.05) & (b1 >= -0.05) & (b2 >= -0.05) & np.isnan(Wd[:, 0])
        Wd[ok] = b0[ok, None] * V[t[0]] + b1[ok, None] * V[t[1]] + b2[ok, None] * V[t[2]]
    return Wd.reshape(im.height, im.width, 2)


def got_mong(im_mong, att_mong, im_go, att_go, chom=5.0):
    """mông nằm DƯỚI khúc gỗ: (1) cắt phần mông nằm bên phải mép trái khúc gỗ quá `chom` đơn vị (phần đó khuất, nhưng viền đáy của nó
    thò ra dưới đáy khúc gỗ thành một vệt lông tơ đen: người dùng 2026-11-12 "vẫn bị lỗi nhỏ ở gần chân"); (2) bỏ mảng vỏ sẫm trên
    mông (nó bị mép khúc gỗ cắt đôi, mà chỗ nối giờ không còn nét nên trông như bị xén)."""
    A = np.asarray(im_mong).copy()
    al = A[..., 3] > 127
    Wm = the_gioi_px(im_mong, att_mong)
    G = np.asarray(im_go)
    Wg = the_gioi_px(im_go, att_go)
    og = (G[..., 3] > 127) & ~np.isnan(Wg[..., 0])
    gy = np.round(Wg[..., 1][og]).astype(int)
    gx = Wg[..., 0][og]
    y0 = int(gy.min())
    mep = np.full(int(gy.max()) - y0 + 1, np.inf)
    np.minimum.at(mep, gy - y0, gx)                # mép TRÁI khúc gỗ theo từng hàng y thế giới
    mep = np.minimum.accumulate(np.where(np.isfinite(mep), mep, np.inf)[::-1])[::-1] if False else mep
    day = float(np.nanmin(mep[:6])) if np.isfinite(mep[:6]).any() else float(np.nanmin(mep[np.isfinite(mep)]))
    yi = np.clip(np.round(np.nan_to_num(Wm[..., 1], nan=y0)).astype(int) - y0, 0, len(mep) - 1)
    xl = np.where(np.nan_to_num(Wm[..., 1], nan=y0) < y0 + 3, day, mep[yi])       # dưới đáy khúc gỗ: lấy mép ở góc đáy
    xl = np.where(np.isfinite(xl), xl, day)
    cat = (A[..., 3] > 0) & ~np.isnan(Wm[..., 0]) & (Wm[..., 0] > xl + chom)
    A[cat, 3] = 0
    rgb = A[..., :3].astype(int)
    trong = cv2.erode(al.astype(np.uint8), np.ones((17, 17), np.uint8)).astype(bool)
    go = trong & (rgb.max(axis=2) > 200)
    vo = trong & (rgb.max(axis=2) <= 200)
    vo = cv2.dilate(vo.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & trong
    if go.any() and vo.any():
        _, lb = cv2.distanceTransformWithLabels((~(go & ~vo)).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
        tra[lb[go & ~vo]] = A[..., :3][go & ~vo]
        A[vo, :3] = tra[lb][vo]
    return Image.fromarray(A, "RGBA"), int(cat.sum()), int(vo.sum())


def giu_vien_ngoai(IM, goc_im, by, ds, day=4):
    """sau khi xoá mực chỗ nối: nét mực GỐC nào nằm trên VIỀN NGOÀI của cả khối (hợp các mảnh thân + chân ở dáng gốc) thì trả lại.
    (Khúc chân trên nằm gần trọn trong thân: xoá theo từng cặp làm mất luôn đoạn viền chân ngay dưới mép thân.)"""
    W_ = {n: the_gioi_px(IM[n], by[n]) for n in ds}
    P = np.concatenate([W_[n][~np.isnan(W_[n][..., 0])] for n in ds])
    o = P.min(axis=0) - 12
    kt = np.ceil((P.max(axis=0) + 12 - o) * D_PX).astype(int)
    U = np.zeros((kt[1], kt[0]), np.uint8)
    chi = {}
    for n in ds:
        w = W_[n]
        ok = ~np.isnan(w[..., 0])
        ij = np.zeros(w.shape[:2] + (2,), int)
        ij[ok] = np.round((w[ok] - o) * D_PX).astype(int)
        chi[n] = (ok, ij)
        m = ok & (np.asarray(IM[n])[..., 3] > 127)
        U[ij[m][:, 1], ij[m][:, 0]] = 1
    U = cv2.morphologyEx(U, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    bien = U.astype(bool) & ~cv2.erode(U, np.ones((2 * day + 1, 2 * day + 1), np.uint8)).astype(bool)
    tra = 0
    for n in ds:
        G = np.asarray(goc_im[n])
        A = np.asarray(IM[n]).copy()
        ok, ij = chi[n]
        muc = ok & (G[..., 3] > 127) & (G[..., :3].max(axis=2) < 110) & (np.abs(A[..., :3].astype(int) - G[..., :3]).sum(axis=2) > 30)
        muc &= bien[ij[..., 1], ij[..., 0]]
        muc = cv2.dilate(muc.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & (G[..., 3] > 0)
        A[muc, :3] = G[..., :3][muc]
        IM[n] = Image.fromarray(A, "RGBA")
        tra += int(muc.sum())
    return tra


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc, hinh=None):
    """slot dùng NGUYÊN lưới của con gốc (đỉnh, tam giác, uv, trọng số) với ảnh của mình đã nằm đúng khung ảnh vùng của part đó."""
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2) * KG
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V, ten=hinh)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh or anh_ten]["verts"] = rows
    return L


def dung():
    D, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    a_tl = ti_le_atlas(D)
    sk = khung.Sk("huou_go_1")
    sk.xuong("root")
    sk.xuong("move", "root")
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_TEN:
            continue
        cha = ten[b["parent"]]
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG, sx=b["sx"], sy=b["sy"])
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    by = {a["slot"]: a for a in D["atts"] if a["cur"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_TEN and s["name"] in by]
    bbox = lambda s: (lambda v: (v[:, 0].min(), v[:, 1].min(), v[:, 0].max(), v[:, 1].max()))(np.array(by[s]["xy"], float).reshape(-1, 2) * KG)
    dat_y = min(bbox(s)[1] for s in ("P_tuiL_H_2", "P_tuiR_H_2", "P_tuiL_Q_2", "P_tuiR_Q_2"))
    co_cong = os.path.exists(os.path.join(CONG, "cong_sau.png"))
    xc = RC.P_CONG * KG
    sk.xuong("cong", "root", xc, dat_y)
    if co_cong:                                   # lớp sau của cổng: sau mọi thứ, không bị mặt nạ cắt
        g = Image.open(os.path.join(CONG, "cong_sau.png")).convert("RGBA")
        ti = CONG_CAO * D_PX / g.height
        for lop in ("cong_sau", "cong_truoc"):
            c = Image.open(os.path.join(CONG, lop + ".png")).convert("RGBA")
            sk.anh(lop, anh.loang_mau(c.convert("RGBa").resize((max(2, round(c.width * ti)), max(2, round(c.height * ti))), Image.LANCZOS).convert("RGBA")))
        sk.slot("cong_sau", "cong", "cong_sau", an=True)
        sk.manh("cong_sau", "cong_sau", Dat(xc, dat_y - 6, ti=1.0 / D_PX, neo=(0.5, 1.0)))
    # mặt nạ cắt ở mặt cổng: bám xương `mat_cong` đặt XA về bên trái (không cắt gì); chỉ clip appear kéo nó về đúng mặt cổng
    sk.xuong("mat_cong", "root", -MAT_XA, 0.0)
    sk.slot("mat_na", "mat_cong")
    tong = [0, 0]
    IM = {by[s]["att"]: anh_part(by[s]["att"], a_tl) for s in slots}
    # thân + chân lấy từ TỜ THÂN LIỀN (huou_go.py cat_lien): hai mảnh chồng nhau mang cùng điểm ảnh, chỗ nối không có nét, nên KHÔNG
    # còn bước xoá mực (xoa_muc_noi, got_mong: ba bản vá bị người dùng trả "lem nhem"; hàm còn để lại phía trên, không gọi)
    for s in slots:
        a = by[s]
        nguon = a["att"]
        sk.slot(s, "move", nguon)
        sk.anh(nguon, IM[nguon])
        L = gan_nguyen(sk, s, nguon, a, ten, Wc)
        tong[0] += L.n
        tong[1] += len(L.tris)
        if s == "zuiba":                          # hình thứ hai của slot mồm: mồm há (ô cứng bám xương mồm)
            sk.anh("mieng_ha", anh_them("mieng_ha", MIENG_HA))
            x0, y0, x1, y1 = bbox("zuiba")
            im_ = sk.images["mieng_ha"]           # slot mồm nằm trên xương move: gắn bằng lưới 4 đỉnh bám trọn xương mồm
            Lm = luoi.luoi_o(im_.width, im_.height, 2, 2, ten="mieng_ha")
            sk.luoi_gan("zuiba", "mieng_ha", Lm, [{"bone24": 1.0}] * Lm.n, dat=Dat((x0 + x1) / 2, (y0 + y1) / 2 - 2, ti=1.0 / D_PX),
                        ten="mieng_ha")
        for t_, (rong, sau, xg) in THEM.items():
            if sau != s:
                continue
            sk.anh(t_, mat_xa_anh(a_tl) if t_ == "mat_xa" else anh_them(t_, rong))
            sk.slot(t_, xg, t_)
            if t_ == "mat_xa":                    # ụ mắt xa: tâm ụ nằm ngay trong mép phải khúc gỗ, tròng lồi ra ngoài mép
                x0, y0, x1, y1 = bbox("YanL_01")
                px = float(np.array(by["P_tou"]["xy"], float).reshape(-1, 2)[:, 0].max()) * KG
                d = Dat(px + 5.0, (y0 + y1) / 2 + 1.0, ti=1.0 / D_PX)
            else:                                 # nụ pha lê: đứng trên đỉnh mông, lệch về phía đuôi
                x0, y0, x1, y1 = bbox("P_shenti")
                d = Dat(x0 + (x1 - x0) * 0.40, y1 - 9.0, ti=1.0 / D_PX, neo=(0.5, 0.94))
            sk.manh(t_, t_, d, xuong=xg)
    cuoi = sk.slots[-1]["name"]
    Pall = np.concatenate([np.array(by[s]["xy"], float).reshape(-1, 2) for s in slots]) * KG
    # nửa mặt phẳng bên PHẢI mặt cổng (toạ độ lúc mặt nạ còn ở xa: x lùi MAT_XA)
    sk.cat("mat_na", cuoi, [(xc - MAT_XA, dat_y - 3000), (xc - MAT_XA + 9000, dat_y - 3000), (xc - MAT_XA + 9000, dat_y + 5000),
                            (xc - MAT_XA, dat_y + 5000)])
    if co_cong:                                   # nửa vành cổng phía gần: trước mọi thứ
        sk.slot("cong_truoc", "cong", "cong_truoc", an=True)
        sk.manh("cong_truoc", "cong_truoc", Dat(xc, dat_y - 6, ti=1.0 / D_PX, neo=(0.5, 1.0)))
    # chỗ bắn tia: giữa hai cành gạc (chỗ cầu mana), con của khúc gỗ; xương cầu năng lượng: con của move
    lp = np.linalg.solve(Wc["bone13"], np.array([RC.GIUA_SUNG[0] * KG, RC.GIUA_SUNG[1] * KG, 1.0]))
    sk.xuong("mieng", "bone13", float(lp[0]), float(lp[1]))
    sk.xuong("cau", "move", 0.0, 0.0)
    for e, m in (("trung", "khung trúng"), ("tu", "bắt đầu tụ cầu"), ("phun", "bắn tia"), ("het_phun", "hết tia"), ("day", "cầu đầy"),
                 ("nem", "cầu rời mồm"), ("cong_mo", "appear: cổng mở"), ("buoc_ra", "appear: bước ra khỏi cổng"),
                 ("cong_dong", "appear: cổng khép")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; mặt đất y = {dat_y:.1f}; ảnh vùng của họ "
          f"{a_tl:.3f} px mỗi đơn vị; cổng: {'có' if co_cong else 'CHƯA có ảnh'}")
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]], dat_y=dat_y, co_cong=co_cong)


def chuyen_dong(sk, info):
    """clip đã lấy mẫu → {clip: (dài, {xương: mảng (số khung, 5) = xoay độ, dời x, y, tỉ lệ x, y nhân}, ẩn [khung][slot])}."""
    S = json.load(open(os.path.join(info["scan"], "sample_moi.json"), encoding="utf-8"))
    IB, ten, SL = info["IB"], info["ten"], info["slots"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i in ids:
            b0 = IB[i]
            A = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                           F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round((A[0, 0] if clip == "hn_die" else A[-1, 0]) / 360.0)
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        an = [{SL[j] for j, n in enumerate(F["n"]) if n is None and SL[j] in sk.si} for F in fr]
        out[clip] = (float(v["dur"]), res, an)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    KR = json.load(open(os.path.join(info["scan"], "kenh_rieng.json"), encoding="utf-8"))
    co_cong = info["co_cong"]

    def kenh(goc, ten_, tau):
        k = KR[goc][ten_]
        x = min(len(k) - 1, max(0.0, tau) * 30.0)
        i0 = int(x)
        i1 = min(i0 + 1, len(k) - 1)
        w = x - i0
        return (np.array(k[i0], float) * (1 - w) + np.array(k[i1], float) * w)

    def dat_dang(P, goc, tau, lap):
        dur, R, an = CD[goc]
        n = len(an)
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * 30.0
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        for s in an[i0]:
            P.alpha[s] = 0.0
        P.att["zuiba"] = "mieng_ha" if float(kenh(goc, "ham", tq)) > 0.5 else "zuiba"
        bx, by_ = kenh(goc, "bay", tq)
        if abs(bx) > 1e-4 or abs(by_) > 1e-4:
            P.move("move", float(bx) * KG, float(by_) * KG)
        r, cx, cy = kenh(goc, "cau", tq)
        P.move("cau", float(cx) * KG, float(cy) * KG)
        P.scale("cau", max(0.01, float(r) * KG / 100.0))
        return float(kenh(goc, "cong", tq))

    out = []
    for ten_, goc, lap, trung in CLIPS:
        dur = CD[goc][0]
        ev = RC.SU_KIEN.get(goc, [])
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in sk.slots:
                    if sl["name"] not in ("mat_na", "cong_sau", "cong_truoc"):
                        P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])
            out.append(Clip(ten_, dur + TAN, fn, ev=ev))
        elif ten_ == "appear":
            def fn(t, P, goc=goc, dur=dur):
                cg = dat_dang(P, goc, t, False)
                # mặt nạ về đúng mặt cổng suốt lúc bước ra; con đã qua hẳn (P_TOI) thì đưa mặt nạ ra xa lại
                P.move("mat_cong", MAT_XA * (1.0 - RC.em((t - RC.P_TOI - 0.02) / 0.06)), 0.0)
                if co_cong:
                    for lop in ("cong_sau", "cong_truoc"):
                        P.alpha[lop] = float(np.clip(cg * 4.0, 0.0, 1.0))
                    s = 0.25 + 0.75 * cg
                    P.scale("cong", s * (1.0 + 0.03 * np.sin(2 * np.pi * 1.7 * t)), s)
                if t < 0.02:                    # khung đầu trống hẳn
                    for sl in sk.slots:
                        if sl["name"] != "mat_na":
                            P.alpha[sl["name"]] = 0.0
            out.append(Clip(ten_, dur, fn, ev=ev, trung=trung))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap) and None), loop=lap, ev=ev, trung=trung))
    return out, dat_dang


# ---------------------------------------------------------------- TIẾN HÓA (người dùng 2026-11-12: "làm clip tiến hóa đi"; ý là ĐỀ XUẤT
# của Claude đã nêu trước: dạng 1 chạy vào cổng rừng, dạng 2 bước ra từ chính cổng đó)
E_MO, E_QUAY, E_VAO, E_HET, E_RA = 0.35, 0.30, 0.52, 1.15, 1.30      # cổng mở xong; bắt đầu quay đầu; bắt đầu chạy; khuất hẳn; dạng 2 bước ra


def tien_hoa(sk, info, dat_dang, cao):
    """rig dạng 1 gộp BẢN NHẸ của dạng 2 (huou_go_rig.py nhe, tiến trình riêng vì hai rig đọc cấu hình theo dạng lúc nạp mô-đun) + clip
    evolve. Cổng rừng của DẠNG 2 mở phía sau (0 → 0,35); dạng 1 quay đầu (lật ngang quanh xương move 0,30 → 0,46), chạy nước kiệu vào
    cổng, phần đã qua mặt cổng bị mặt nạ của dạng 1 giấu (khuất hẳn lúc 1,15); 1,30: dạng 2 bước ra bằng đúng clip appear của nó (từ
    mốc bước ra), cổng khép, khung cuối = khung 0 idle dạng 2."""
    import pickle
    import subprocess
    subprocess.run([sys.executable, "-I", os.path.join(HG.HERE, "huou_go_rig.py"), "nhe"], env=dict(os.environ, HG_NHE="1"), check=True,
                   stdout=subprocess.DEVNULL)
    N2 = pickle.load(open(os.path.join(HG.HERE, "inbox", "huou_go_2", "rig", "_nhe.pkl"), "rb"))
    sk2, ap2, idle2 = N2["sk"], N2["appear"], N2["idle0"]
    ti = cao / N2["cao"]
    M = tienhoa.gop(sk, sk2)
    alphaB = M.info.get("alpha_B", {})
    slotA = {s_["name"]: s_["alpha"] for s_ in sk.slots}
    x_cong = N2["p_cong"] * ti                    # mặt cổng của dạng 2 trong rig gộp
    xc1 = RC.P_CONG * KG
    dur = E_RA + (len(ap2) - 1) / 30.0 - N2["p_ra"]

    def fn(t, P):
        # ---- dạng 2 (xương n_*): cổng mở, giữ mở, rồi bước ra
        tau = N2["p_ra"] * min(1.0, t / E_MO) if t < E_RA else N2["p_ra"] + (t - E_RA)
        F = ap2[min(len(ap2) - 1, int(round(tau * 30)))]
        Q = tienhoa.doi_ten_pose(F, "n_")
        P.t.update({k: list(v) for k, v in Q.t.items()})
        P.att.update(Q.att)
        for sl, a0 in alphaB.items():
            P.alpha[sl] = Q.alpha.get(sl, a0)
        P.scale("evo", ti)
        # ---- dạng 1: nghỉ → quay đầu → chạy vào cổng
        Pa = khung.Pose()
        dat_dang(Pa, "hn_idle", t, True)
        Pb = khung.Pose()
        dat_dang(Pb, "hn_walk", max(0.0, t - E_VAO + 0.1), True)
        w = hoat.ease((t - (E_VAO - 0.12)) / 0.16)
        for b_ in set(Pa.t) | set(Pb.t):
            va, vb = Pa.t.get(b_, [0, 0, 0, 1, 1]), Pb.t.get(b_, [0, 0, 0, 1, 1])
            P.t[b_] = [va[q] * (1 - w) + vb[q] * w for q in range(5)]
        P.att.update(Pa.att)
        lat = 1.0 - 2.0 * hoat.ease((t - E_QUAY) / 0.16)              # 1 → −1: quay đầu về phía cổng
        lat = (1 if lat >= 0 else -1) * max(0.14, abs(lat))
        di = hoat.cv(t, [(0, 0), (E_VAO, 0), (E_HET, 1, "in")])
        P.scale("move", lat, 1.0 + 0.06 * (1 - abs(lat)))
        P.move("move", (x_cong - 190.0 * KG) * di, 0.0)
        P.move("mat_cong", MAT_XA + (x_cong - xc1), 0.0)                # mặt nạ dạng 1 về đúng mặt cổng của dạng 2
        an = t >= E_HET
        for sl, a0 in slotA.items():
            if sl != "mat_na":
                P.alpha[sl] = 0.0 if (an or sl in ("cong_sau", "cong_truoc")) else Pa.alpha.get(sl, a0)

    ev = Clip("evolve", dur, fn, ev=[(0.0, "cong_mo", ""), (E_VAO, "chay_vao", ""), (E_RA, "doi_dang", ""), (E_RA + 1.2, "cong_dong", "")])
    for e_, m_ in (("chay_vao", "tiến hóa: dạng cũ chạy vào cổng"), ("doi_dang", "tiến hóa: dạng mới bước ra")):
        M.su_kien(e_, m_)
    _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
    return M, ev, s_ev + f" (dạng sau co {ti:.3f} trong rig gộp; clip {dur:.2f} s)"


def main(a):
    sk, info = dung()
    clips, dat_dang = lam_clip(sk, info)
    ra = os.environ.get("HG_RA") or os.path.join(HG.HERE, "inbox", "huou_go_1", "rig")
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ] [luoi]: khung lớn nền xám → rig/soi_<clip>.png
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        for an_ in [x for x in os.environ.get("HG_AN", "").split(",") if x]:        # gỡ lỗi: ẩn vài slot để xem lớp dưới
            for P in Ps:
                P.alpha[an_] = 0.0
        sc = float(a[3]) if len(a) > 3 else 1.0
        kw = dict(luoi=True, mau_luoi=(10, 10, 10, 90)) if len(a) > 4 else {}
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2, **kw).convert("RGB") for P in Ps]
        cot = min(len(ims), 4)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in VE_NGHI:
            frames[c.ten] = [P.copy() for P in frames[c.ten]]
            hoat.khop_cuoi(frames[c.ten], frames["idle"][0], 0.2)
    cao = soi.chieu_cao(soi.Ve(sk), frames["idle"][0], BO_CAO)
    M, noi_them = sk, {}
    if os.path.exists(os.path.join(HG.HERE, "inbox", "huou_go_2", "manh", "part", "P_bozi.png")) and not os.environ.get("HG_KHONG_TH"):
        M, ev, s_ev = tien_hoa(sk, info, dat_dang, cao)
        clips = clips + [ev]
        frames["evolve"] = hoat.nuong(M, ev)
        noi_them["evolve"] = s_ev
        print("  evolve:", s_ev)
    xuat.xuat_het(M, clips, ra, "huou_go_1", "Hươu gỗ (huou_go) dạng 1: khúc gỗ non", frames=frames, dang=1, so_dang=2,
                  dung_yen=("cast", "skill"), ma_goc=None, khop_idle=0, cao=cao, noi_them=noi_them, impact=IMPACT,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, dich_mb=0.6, tran_mb=1.0)


if __name__ == "__main__":
    main(sys.argv[1:])
