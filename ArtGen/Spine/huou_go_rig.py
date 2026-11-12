# -*- coding: utf-8 -*-
"""Hươu gỗ DẠNG 2 (hươu cổ dài; tướng thứ 4 đảo Mộc): hình của mình chạy trên ĐÚNG rig của con gốc monster_3504.
Ghi chú: inbox/huou_go_ghichu.md. Cách làm như huou_go_non_rig.py (dạng 1) / xuong_rong_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ, đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move`, `ham` (hàm dưới, con của xương đầu, khớp
  ở chốt bản lề), `mieng` (chỗ bắn tia = giữa hai gạc), `cau` (quả cầu năng lượng cho VFX), `mat_cong` + `cong` (appear).
- MẢNH: 24 part vẽ đúng khung ảnh vùng (HG_DANG=2 huou_go.py cat_part) lắp vào NGUYÊN lưới của họ. BỎ sáu pha lê + ba túm lông ở vai
  của họ (người dùng: rêu và pha lê ra sau lưng) và đầu của họ. Mảnh của mình cắt thẳng từ concept (tờ M_E1, M_E2 "đúng chỗ, đúng
  cỡ"; đặt vào rig bằng phép khớp concept ↔ sơ đồ bố cục): `dau` (đầu không hàm dưới, cứng trên bone7), `ham` (hàm dưới, cứng trên
  xương `ham`), `hong` (lòng miệng sẫm, lưới 4 đỉnh căng giữa hai hàm), `pha_le` (cụm pha lê + rêu, cứng trên xương lưng bone4).
- CHUYỂN ĐỘNG: clip dựng ở tầng điều khiển (huou_go_clip.py), runtime Spine thật nướng ra scan/sample_moi.json → lệch so với dáng gốc
  cho mọi xương; slot lá rơi (P_weiba4..7, mặc định ẩn) hiện theo trường n, a của mẫu. Kênh riêng (kenh_rieng.json): ham → góc xương
  `ham`, cau → xương `cau`, bay → xương `move`, cong → cổng + mặt nạ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/huou_go_rig.py        → inbox/huou_go_2/rig/
    py -3 -I ArtGen/Spine/huou_go_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [luoi]          → rig/soi_<clip>.png (khung lớn nền xám)
    py -3 -I ArtGen/Spine/huou_go_rig.py khop                                              → in phép khớp concept ↔ sơ đồ, mau/_khop.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
os.environ["HG_DANG"] = "2"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import huou_go as HG  # noqa: E402
import huou_go_clip as RC  # noqa: E402

KG = 1.0
NHE = os.environ.get("HG_NHE") == "1"       # bản NHẸ (ảnh nhỏ) của dạng 2, chỉ để gộp vào rig dạng 1 cho clip tiến hóa
D_PX = 0.72 if NHE else 1.15  # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~700 đơn vị)
BO_TEN = ("shadow", "wangge")
BO_PART = ("P_z_jingshi1", "P_z_jingshi", "P_y_jingshi", "P_y_jingshi1", "P_y_jingshi2", "P_y_jingshi3", "P_z_maofa", "P_y_maofa",
           "P_y_maofa1", "P_tou")
CLIPS = [("appear", "hg_appear", False, None), ("idle", "hg_idle", True, None), ("walk", "hg_walk", True, None),
         ("attack", "hg_attack", False, None), ("cast", "hg_cast", False, None), ("skill", "hg_skill", False, None),
         ("hit", "hg_hit", False, None), ("die", "hg_die", False, None)]
VE_NGHI = ("appear", "attack", "cast", "skill", "hit")
MAT_XA = 4000.0
TAN = 0.45
IMPACT = {"attack": (0.06, 0.32, 0.08), "skill": (0.20, 1.0, 0.16, "#eaffd266")}
BO_CAO = ("P_y_jiao", "P_y_jiao1", "P_z_jiao", "P_z_jiao1", "P_toufa", "P_y_er", "P_z_er")
HAM_MO = 34.0                # độ mở hàm dưới khi ham = 1
CONG = os.path.join(HG.HERE, "inbox", "huou_go_1", "manh", "cong")
CONG_CAO = 830.0
# các mốc trên concept (px, L1_duyet.png): chốt bản lề hàm; mút trong của khe miệng ở mõm (cho lòng miệng)
CHOT_PX = (858.0, 470.0)
MOM_PX = (1040.0, 462.0)
# chỉnh tay chỗ đặt mảnh cắt từ concept (đơn vị rig), sau khi soi
LECH = {"dau": (0.0, 0.0), "ham": (0.0, 0.0), "pha_le": (0.0, 0.0)}


def nap_goc():
    scan = HG.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, I, scan


def ti_le_atlas(D):
    _, imgs, _ = HG.nap()
    a = [x for x in D["atts"] if x["att"] == "P_bozi" and x["cur"]][0]
    im = imgs[a["region"]]
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    xy = np.array(a["xy"], float).reshape(-1, 2)
    return float(np.hypot(*(uv.max(0) - uv.min(0))) / np.hypot(*(xy.max(0) - xy.min(0))))


def anh_part(ten, a_tl):
    z = {t: z_ for to, (z_, ds) in HG.TO.items() for t in ds}[ten]
    pth = os.path.join(HG.MANH, "part", ten + ".png")
    if not os.path.exists(pth):
        raise SystemExit("thiếu ảnh part " + pth)
    g = Image.open(pth).convert("RGBA")
    kq = D_PX / (a_tl * z)
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


# ---------------------------------------------------------------- concept ↔ rig
_KH = {}


def khop(ve=False):
    """phép đồng dạng đưa pixel concept (L1_duyet.png) về pixel sơ đồ bố cục (bo_cuc_thu.png, dựng từ rig): p' = tam + (p − tam) × s
    + (tx, ty). Dò s, tx, ty cho hình bóng hai ảnh trùng nhau nhất (GPT vẽ concept to hơn sơ đồ chừng 8%). Trả hàm px concept → rig."""
    if not _KH:
        c = np.asarray(Image.open(os.path.join(HG.TAI, "L1_duyet.png")).convert("RGB"))
        g = np.asarray(Image.open(os.path.join(HG.MAU, "bo_cuc_thu.png")).convert("RGB"))
        mc = (c.min(2) < 236).astype(np.uint8)
        mg = (g.min(2) < 236).astype(np.uint8)
        # chỉ so phần thân dưới + chân + cổ (bờm, gạc, đầu, pha lê vẽ khác sơ đồ): hàng y > 560 của sơ đồ và cột cổ
        H_, W_ = mg.shape
        tam = np.array([W_ / 2, H_ / 2])
        best = (-1, 1.0, 0, 0)
        k4 = 4
        gs = cv2.resize(mg, (W_ // k4, H_ // k4), interpolation=cv2.INTER_AREA)
        for s in np.arange(0.84, 1.021, 0.01):
            M = np.array([[s, 0, tam[0] * (1 - s)], [0, s, tam[1] * (1 - s)]], float)
            cs = cv2.warpAffine(mc, M, (W_, H_), flags=cv2.INTER_NEAREST)
            cs = cv2.resize(cs, (W_ // k4, H_ // k4), interpolation=cv2.INTER_AREA)
            for ty in range(-14, 15, 2):
                for tx in range(-14, 15, 2):
                    sh = np.roll(np.roll(cs, ty, 0), tx, 1)
                    iou = (sh & gs).sum() / max(1, (sh | gs).sum())
                    if iou > best[0]:
                        best = (iou, float(s), tx * k4, ty * k4)
        iou, s, tx, ty = best
        T, sc = HG.khung_T()
        o = T(np.array([0.0, 0.0]))
        _KH.update(s=s, tx=tx, ty=ty, iou=iou, tam=tam, sc=sc, ox=float(o[0]), oy=float(o[1]))
        print(f"khớp concept ↔ sơ đồ: s = {s:.3f}, dời ({tx}, {ty}) px, IoU {iou:.3f}; sơ đồ {sc:.4f} px mỗi đơn vị rig")
        if ve:
            M = np.array([[s, 0, tam[0] * (1 - s) + tx], [0, s, tam[1] * (1 - s) + ty]], float)
            cw = cv2.warpAffine(c, M, (W_, H_), borderValue=(255, 255, 255))
            out = (cw.astype(float) * 0.6 + 255 * 0.4)
            out[cv2.morphologyEx(mg, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(bool)] = (255, 0, 200)
            Image.fromarray(out.astype(np.uint8)).save(os.path.join(HG.MAU, "_khop.png"))
            print(os.path.join(HG.MAU, "_khop.png"))
    k = _KH

    def px_rig(p):
        p = np.asarray(p, float)
        q = k["tam"] + (p - k["tam"]) * k["s"] + np.array([k["tx"], k["ty"]])
        return np.stack([(q[..., 0] - k["ox"]) / k["sc"], (k["oy"] - q[..., 1]) / k["sc"]], -1) * KG

    return px_rig, k["s"] / k["sc"] * KG          # (hàm đổi, đơn vị rig cho mỗi px concept)


def manh_concept():
    """ba mảnh cắt từ hai tờ "đúng chỗ, đúng cỡ" (M_E1: đầu + cụm pha lê; M_E2: hàm dưới) → {tên: (ảnh RGBA cắt sát, x0, y0 px concept)}."""
    out = {}
    for to, ds in (("M_E1", {"dau": (950, 370), "pha_le": (655, 560)}), ("M_E2", {"ham": (945, 490)})):
        path = anh.to_moi_nhat(HG.TAI, to)
        if not path:
            raise SystemExit("thiếu tờ " + to)
        tt = anh.doc_to(path, dien_tich_min=600, gop_px=18)
        for ten, (cx, cy) in ds.items():
            m_ = min(tt.manh, key=lambda m: np.hypot((m["x0"] + m["x1"]) / 2 - cx, (m["y0"] + m["y1"]) / 2 - cy))
            mk = np.isin(tt.lab, m_["ids"])
            ys, xs = np.nonzero(mk)
            x0, x1, y0, y1 = max(0, xs.min() - 4), xs.max() + 5, max(0, ys.min() - 4), ys.max() + 5
            cell = tt.rgba[y0:y1, x0:x1].copy()
            cell[..., 3] = (cell[..., 3] * anh.gian(mk[y0:y1, x0:x1], 2)).astype(np.uint8)
            out[ten] = (Image.fromarray(cell, "RGBA"), int(x0), int(y0))
            print(f"  mảnh concept {ten}: {x1 - x0} x {y1 - y0} px ở ({x0}, {y0}) của {os.path.basename(path)}")
    return out


# xoá nét mực ở chỗ nối (người dùng 2026-11-12: "dạng 1 ở các khớp nối chân, thân bỏ outline đen đi để liền mạch", "phần này vẫn có
# outline, xem cả cho dạng 2"): cặp (mảnh nằm TRÊN, mảnh kề nằm DƯỚI); mọi chỗ hai mảnh thân / chân cùng màu gỗ chồng nhau.
NOI = [("P_z_houzhi1", "P_z_houzhi2"), ("P_z_houzhi", "P_z_houzhi1"), ("P_shenti", "P_z_houzhi"),
       ("P_z_qianzhi1", "P_z_qianzhi"), ("P_bozi", "P_z_qianzhi"), ("P_shenti", "P_z_qianzhi"),
       ("P_y_houzhi1", "P_y_houzhi2"), ("P_y_houzhi", "P_y_houzhi1"), ("P_y_houzhi", "P_shenti", "mo"),
       ("P_bozi", "P_shenti"), ("P_bozi", "P_y_houzhi"), ("P_y_qianzhi1", "P_bozi", "mo"), ("P_y_qianzhi1", "P_shenti", "mo"),
       ("P_y_qianzhi", "P_y_qianzhi1"), ("P_shenti", "P_weiba1")]


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
SAU = 7
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
    px_rig, u_px = khop()
    MC = manh_concept()
    sk = khung.Sk("huou_go_2")
    sk.xuong("root")
    sk.xuong("move", "root")
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_TEN:
            continue
        cha = ten[b["parent"]]
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG, sx=b["sx"], sy=b["sy"])
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    by = {a["slot"]: a for a in D["atts"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_TEN and s["name"] in by]
    bbox = lambda s: (lambda v: (v[:, 0].min(), v[:, 1].min(), v[:, 0].max(), v[:, 1].max()))(np.array(by[s]["xy"], float).reshape(-1, 2) * KG)
    dat_y = min(bbox(s)[1] for s in ("P_y_houzhi2", "P_z_houzhi2", "P_y_qianzhi", "P_z_qianzhi1"))
    # xương hàm dưới: con của xương đầu, đặt ở chốt bản lề (đọc trên concept)
    chot = px_rig(CHOT_PX) + np.array(LECH["ham"])
    lp = np.linalg.solve(Wc["bone7"], np.array([chot[0], chot[1], 1.0]))
    goc7 = float(np.degrees(np.arctan2(Wc["bone7"][1, 0], Wc["bone7"][0, 0])))
    sk.xuong("ham", "bone7", float(lp[0]), float(lp[1]), goc=-goc7)          # trục xương hàm nằm ngang thế giới ở dáng gốc

    def anh_mc(t_):
        g, x0, y0 = MC[t_]
        kq = u_px * D_PX
        im_ = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
        tam = px_rig(np.array([x0 + g.width / 2, y0 + g.height / 2])) + np.array(LECH[t_])
        return anh.loang_mau(im_), tam

    def gan_cung(slot, t_, xg):
        im_, tam = anh_mc(t_)
        sk.anh(t_, im_)
        sk.slot(slot, "move", t_)
        Lq = luoi.luoi_o(im_.width, im_.height, 2, 2, ten=slot)
        sk.luoi_gan(slot, t_, Lq, [{xg: 1.0}] * Lq.n, dat=Dat(float(tam[0]), float(tam[1]), ti=1.0 / D_PX))

    co_cong = os.path.exists(os.path.join(CONG, "cong_sau.png"))
    xc = RC.P_CONG * KG
    sk.xuong("cong", "root", xc, dat_y)
    if co_cong:
        g = Image.open(os.path.join(CONG, "cong_sau.png")).convert("RGBA")
        ti = CONG_CAO * D_PX * 0.7 / g.height          # ảnh cổng lưu nhỏ 0,7 lần rồi phóng (cổng chỉ hiện ~2 s)
        for lop in ("cong_sau", "cong_truoc"):
            c = Image.open(os.path.join(CONG, lop + ".png")).convert("RGBA")
            sk.anh(lop, anh.loang_mau(c.convert("RGBa").resize((max(2, round(c.width * ti)), max(2, round(c.height * ti))), Image.LANCZOS).convert("RGBA")))
        sk.slot("cong_sau", "cong", "cong_sau", an=True)
        sk.manh("cong_sau", "cong_sau", Dat(xc, dat_y - 10, ti=1.0 / (D_PX * 0.7), neo=(0.5, 1.0)))
    sk.xuong("mat_cong", "root", -MAT_XA, 0.0)
    sk.slot("mat_na", "mat_cong")
    tong = [0, 0]
    an_san = []
    theo_att = {by[s_]["att"]: by[s_] for s_ in slots if by[s_]["cur"]}
    IM = {n_: anh_part(n_, a_tl) for n_ in theo_att if n_ not in BO_PART}
    # thân + chân lấy từ TỜ THÂN LIỀN (huou_go.py cat_lien): không còn bước xoá mực ở chỗ nối
    for s in slots:
        a = by[s]
        nguon = a["att"]
        if nguon == "P_tou":                      # đầu của mình: lòng miệng, hàm dưới, đầu (sau → trước)
            mom = px_rig(MOM_PX)
            hong = Image.new("RGBA", (8, 8), (74, 54, 38, 255))
            sk.anh("hong", hong)
            sk.slot("hong", "move", "hong")
            Lh = luoi.Luoi(np.array([[1, 1], [7, 1], [7, 7], [1, 7]], float), np.array([[0, 1, 2], [0, 2, 3]]), 4, 4, 8, 8, ten="hong")
            V = np.array([chot + (0, 16), mom + (-14, 8), mom + (-14, -8), chot + (0, -16)], float)
            sk.luoi_gan("hong", "hong", Lh, [{"bone7": 1.0}, {"bone7": 1.0}, {"ham": 1.0}, {"ham": 1.0}], the_gioi=V)
            gan_cung("ham", "ham", "ham")
            gan_cung("dau", "dau", "bone7")
            continue
        if nguon in BO_PART:
            continue
        an = not a["cur"]
        sk.slot(s, "move", nguon, an=an)
        if an:
            an_san.append(s)
        if nguon not in sk.images:
            sk.anh(nguon, IM[nguon])
        L = gan_nguyen(sk, s, nguon, a, ten, Wc)
        tong[0] += L.n
        tong[1] += len(L.tris)
        if s == "P_shenti":                       # cụm pha lê + rêu trên lưng: ngay trước thân, bám xương lưng
            gan_cung("pha_le", "pha_le", "bone4")
    cuoi = sk.slots[-1]["name"]
    sk.cat("mat_na", cuoi, [(xc - MAT_XA, dat_y - 4000), (xc - MAT_XA + 12000, dat_y - 4000), (xc - MAT_XA + 12000, dat_y + 8000),
                            (xc - MAT_XA, dat_y + 8000)])
    if co_cong:
        sk.slot("cong_truoc", "cong", "cong_truoc", an=True)
        sk.manh("cong_truoc", "cong_truoc", Dat(xc, dat_y - 10, ti=1.0 / (D_PX * 0.7), neo=(0.5, 1.0)))
    lp = np.linalg.solve(Wc["bone7"], np.array([RC.GIUA_SUNG[0] * KG, RC.GIUA_SUNG[1] * KG, 1.0]))
    sk.xuong("mieng", "bone7", float(lp[0]), float(lp[1]))
    sk.xuong("cau", "move", 0.0, 0.0)
    for e, m in (("trung", "khung trúng"), ("tu", "bắt đầu tụ cầu"), ("phun", "bắn tia"), ("het_phun", "hết tia"), ("day", "cầu đầy"),
                 ("nem", "cầu rời mõm"), ("cong_mo", "appear: cổng mở"), ("buoc_ra", "appear: bước ra khỏi cổng"),
                 ("cong_dong", "appear: cổng khép")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác (lưới của họ); mặt đất y = {dat_y:.1f}; ảnh vùng "
          f"của họ {a_tl:.3f} px mỗi đơn vị; cổng: {'có' if co_cong else 'CHƯA có ảnh'}; slot ẩn sẵn {an_san}")
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]], dat_y=dat_y, co_cong=co_cong, an_san=an_san)


def chuyen_dong(sk, info):
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
            A[:, 0] -= 360.0 * round((A[0, 0] if clip == "hg_die" else A[-1, 0]) / 360.0)
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        # độ đậm từng slot của mình: 0 khi slot của họ không có hình, không thì lấy độ đậm slot của họ
        dam = [{SL[j]: (0.0 if n is None else float(F["a"][j])) for j, n in enumerate(F["n"]) if SL[j] in sk.si} for F in fr]
        out[clip] = (float(v["dur"]), res, dam)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    KR = json.load(open(os.path.join(info["scan"], "kenh_rieng.json"), encoding="utf-8"))
    co_cong = info["co_cong"]
    mac_dinh = {sl["name"]: sl["alpha"] for sl in sk.slots}

    def kenh(goc, ten_, tau):
        k = KR[goc][ten_]
        x = min(len(k) - 1, max(0.0, tau) * 30.0)
        i0 = int(x)
        i1 = min(i0 + 1, len(k) - 1)
        w = x - i0
        return (np.array(k[i0], float) * (1 - w) + np.array(k[i1], float) * w)

    def dat_dang(P, goc, tau, lap):
        dur, R, dam = CD[goc]
        n = len(dam)
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
        for s, a in dam[i0].items():
            if abs(a - mac_dinh[s]) > 1e-3:
                P.alpha[s] = a
        h = float(kenh(goc, "ham", tq))
        if h > 1e-3:
            P.rot("ham", -HAM_MO * h)
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
                P.move("mat_cong", MAT_XA * (1.0 - RC.em((t - RC.P_TOI - 0.02) / 0.06)), 0.0)
                if co_cong:
                    for lop in ("cong_sau", "cong_truoc"):
                        P.alpha[lop] = float(np.clip(cg * 4.0, 0.0, 1.0))
                    s = 0.25 + 0.75 * cg
                    P.scale("cong", s * (1.0 + 0.03 * np.sin(2 * np.pi * 1.7 * t)), s)
                if t < 0.02:
                    for sl in sk.slots:
                        if sl["name"] != "mat_na":
                            P.alpha[sl["name"]] = 0.0
            out.append(Clip(ten_, dur, fn, ev=ev, trung=trung))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap) and None), loop=lap, ev=ev, trung=trung))
    return out, dat_dang


def main(a):
    if a and a[0] == "khop":
        khop(ve=True)
        return
    sk, info = dung()
    clips, dat_dang = lam_clip(sk, info)
    ra = os.environ.get("HG_RA") or os.path.join(HG.HERE, "inbox", "huou_go_2", "rig")
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
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
    if a and a[0] == "nhe":                    # HG_NHE=1: ghi bản nhẹ (rig, các khung appear đã khớp về idle, khung 0 idle, chiều cao)
        import pickle
        os.makedirs(ra, exist_ok=True)
        pickle.dump(dict(sk=sk, appear=frames["appear"], idle0=frames["idle"][0], cao=cao, p_ra=RC.P_RA, p_cong=RC.P_CONG * KG),
                    open(os.path.join(ra, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(ra, "_nhe.pkl"))
        return
    xuat.xuat_het(sk, clips, ra, "huou_go_2", "Hươu gỗ (huou_go) dạng 2: hươu cổ dài", frames=frames, dang=2, so_dang=2,
                  dung_yen=("cast", "skill"), ma_goc=None, khop_idle=0, cao=cao, noi_them={}, impact=IMPACT,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, dich_mb=0.6, tran_mb=1.0)


if __name__ == "__main__":
    main(sys.argv[1:])
