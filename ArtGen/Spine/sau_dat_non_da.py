# -*- coding: utf-8 -*-
"""Sa Trùng Nhi (sau_dat_non, dạng 1): DA theo concept B đã duyệt (người dùng 2026-11-17 chọn "B": giun non hồng đất, đầu vỏ kem, mắt hổ
phách to, miệng tròn răng sữa, hai nụ ngà, ba râu nâu nhạt đầu hạt hổ phách). Cùng rig, lưới, clip với dạng 2 (sau_dat_rig.py SD_DANG=non).

- ĐẦU (sọ, hàm, hai nụ ngà, ba tấm mào) CẮT THẲNG từ concept B theo vùng kín giữa nét mực (số vùng ở mau/_vung_dau.png), như dạng 2
  (sau_dat_dau.py). Concept B vẽ trên bố cục rig dạng 1 (khung 0 idle) nên mỗi mảnh đầu của dạng 2 ứng với một chỗ trên B qua chính lưới
  của nó (`khop`: đỉnh lưới ở px khung concept dạng 2 ↔ px B, sai ≤ 0,3 px, riêng hàm 5 px vì vành mềm). Mảnh mới được NẮN NGƯỢC về khung
  concept dạng 2 → rig gắn y như dạng 2 (dat.json, gan_theo_goc, vanh_mem không đổi).
- Lòng miệng: đĩa của dạng 2 đổi sang màu đất nung của B.
- THÂN (P_bozi_*, ảnh lót thân N_L) và RÂU (A_chuxu_*): ĐỔI MÀU BẰNG MÃ trên ảnh đã xong của dạng 2 (giữ từng nét, hình bóng, mọi bước
  dọn chỗ nối): thân cát → hồng giun, bụng kem → kem hồng; râu nâu sẫm → nâu nhạt, dải hổ phách dưới khấc → thân râu (chỉ còn hạt ở ngọn).
- Tua, phiến, tảng, gò cát: B giữ như dạng 2 → rig dùng lại ảnh dạng 2.

    sau_dat_non_da.py khop     (dựng rig dạng 1 bằng da dạng 2) cặp đỉnh mảnh đầu → mau/_khop_dau.npz
    sau_dat_non_da.py dau      → inbox/sau_dat_non/manh/cung/*.png + dat.json, tờ soi mau/_dau_B.png
    sau_dat_non_da.py than     → manh/part/P_bozi_*.png + tai_ve/N_L.png
    sau_dat_non_da.py rau      → manh/part/A_chuxu_*.png
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W, H = 1536, 1024
LON = os.path.join(HERE, "inbox", "sau_dat_1")
NON = os.path.join(HERE, "inbox", "sau_dat_non")
MAU, TAI = os.path.join(NON, "mau"), os.path.join(NON, "tai_ve")
CUNG2, CUNG = os.path.join(LON, "manh", "cung"), os.path.join(NON, "manh", "cung")
PART2, PART = os.path.join(LON, "manh", "part"), os.path.join(NON, "manh", "part")
DUYET = os.path.join(TAI, "L1_duyet.png")
X0, Y0 = 640, 230                                   # góc khung vùng đầu trên B (mau/_vung_dau.npy)
NHOM = {"dau": {221, 255, 286, 396, 422, 424, 440, 441, 469, 479, 499},     # vòng giáp, mặt, gờ mày, mắt, răng trên
        "ham": {534, 514, 521, 543, 567, 588, 590, 594},                    # vành dưới mặt, răng dưới
        "nanh1": {579}, "nanh2": {596},                                     # hai nụ ngà (vẽ trước đầu, cùng xương hàm)
        "maoA": {89}, "maoB": {211}, "maoC": {334}}                         # ba tấm mào kem
SLOT = {"dau": "P_shange", "ham": "P_xiae_01", "nanh1": "P_jiao_07", "nanh2": "P_jiao_09", "maoA": "P_jiao_03", "maoB": "P_jiao_02",
        "maoC": "P_jiao_01", "mieng": "P_xiae_02"}
TRUOC = {"maoC": ("maoB", "maoA", "dau"), "maoB": ("maoA", "dau"), "maoA": ("dau",)}     # mảnh vẽ đè lên tấm mào
DO_MAU = np.array([189, 74, 37])                    # lòng miệng B


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


# ---------------------------------------------------------------- khớp
def khop():
    os.environ["SD_DANG"] = "non"
    os.environ["SD_DA2"] = "1"
    import sau_dat_rig as R
    from quai import hoat, soi
    sk, info = R.dung()
    clips = R.lam_clip(sk, info)
    P = hoat.nuong(sk, clips[1])[0]
    j = json.load(open(os.path.join(MAU, "bocuc.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    DAT = json.load(open(os.path.join(CUNG2, "dat.json"), encoding="utf-8"))
    out = {}
    for nm, an, V, uv, tris, a, path, si in soi.Ve(sk).skin(P)[0]:
        if nm not in R.CUNG_SLOT:
            continue
        k = R.CUNG_SLOT[nm]
        g = Image.open(os.path.join(CUNG2, k + ".png"))
        C = uv * np.array([g.width, g.height]) + np.array(DAT[k]["hop"][:2])
        Bp = np.stack([(V[:, 0] - cx) * s + 768, -(V[:, 1] - cy) * s + 512], 1)
        out[k + "_C"], out[k + "_B"] = C, Bp
    np.savez_compressed(os.path.join(MAU, "_khop_dau.npz"), **out)
    print("đã lưu", sorted({k[:-2] for k in out}))


def nan_nguoc(k, img_B, pad=12):
    """ảnh RGBA cỡ B (px bố cục dạng 1) → ảnh trong khung concept dạng 2 qua lưới của mảnh k. Trả (ảnh, (x0, y0))."""
    from scipy.interpolate import LinearNDInterpolator
    Z = np.load(os.path.join(MAU, "_khop_dau.npz"))
    C, Bp = Z[k + "_C"], Z[k + "_B"]
    A = np.hstack([Bp, np.ones((len(Bp), 1))])
    Minv, *_ = np.linalg.lstsq(A, C, rcond=None)                    # B → C (để ước hộp)
    Ac = np.hstack([C, np.ones((len(C), 1))])
    Mf, *_ = np.linalg.lstsq(Ac, Bp, rcond=None)                    # C → B (ngoài lưới)
    ys, xs = np.nonzero(img_B[..., 3] > 0)
    goc = np.array([[xs.min(), ys.min(), 1], [xs.max(), ys.min(), 1], [xs.min(), ys.max(), 1], [xs.max(), ys.max(), 1]], float) @ Minv
    x0, y0 = np.floor(goc.min(0)).astype(int) - pad
    x1, y1 = np.ceil(goc.max(0)).astype(int) + pad
    gx, gy = np.meshgrid(np.arange(x0, x1, dtype=float), np.arange(y0, y1, dtype=float))
    q = np.stack([gx.ravel(), gy.ravel()], 1)
    f = LinearNDInterpolator(C, Bp)
    b = f(q)
    ngoai = np.isnan(b[:, 0])
    b[ngoai] = np.hstack([q[ngoai], np.ones((ngoai.sum(), 1))]) @ Mf
    mx = b[:, 0].reshape(gx.shape).astype(np.float32)
    my = b[:, 1].reshape(gx.shape).astype(np.float32)
    src = img_B.astype(np.float32)
    src[..., :3] *= src[..., 3:4] / 255.0
    o = cv2.remap(src, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    al = o[..., 3:4]
    o[..., :3] = np.where(al > 1, o[..., :3] * 255.0 / np.maximum(al, 1), 0)
    return np.clip(o, 0, 255).astype(np.uint8), (int(x0), int(y0))


# ---------------------------------------------------------------- đầu
def dau():
    A = np.asarray(Image.open(DUYET).convert("RGB").resize((W, H)))
    lab = np.load(os.path.join(MAU, "_vung_dau.npy"))
    h, w = lab.shape
    sub = A[Y0:Y0 + h, X0:X0 + w].astype(int)
    toi = sub.mean(2) < 95
    n = int(lab.max()) + 1
    area = np.bincount(lab.ravel(), minlength=n)
    med = np.zeros((n, 3))
    for i in range(1, n):
        if area[i]:
            med[i] = np.median(sub[lab == i], 0)
    # lòng miệng: vùng màu đất nung quanh miệng (kể cả mẩu vụn giữa nét gạch)
    Z = np.load(os.path.join(MAU, "_khop_dau.npz"))
    hm = Z["mieng_B"]
    mx0, my0, mx1, my1 = hm[:, 0].min() - X0, hm[:, 1].min() - Y0, hm[:, 0].max() - X0, hm[:, 1].max() - Y0
    ys, xs = np.indices(lab.shape)
    trong_dia = (xs >= mx0) & (xs <= mx1) & (ys >= my0) & (ys <= my1)
    do_id = [i for i in range(1, n) if area[i] and np.abs(med[i] - DO_MAU).max() < 55 and (trong_dia & (lab == i)).any()]
    do = np.isin(lab, do_id)
    vung = {k: np.isin(lab, list(v)) for k, v in NHOM.items()}
    d = {k: cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5) for k, m in vung.items()}
    dmin = np.minimum.reduce(list(d.values()))
    mk = {}
    for k, m in vung.items():
        # tấm mào: giữ TRỌN nét mực ở mép chung với mảnh đè lên (mảnh kín viền; lúc mào đung đưa tách khỏi đầu vẫn có viền)
        muc = toi & (d[k] < 7) & ((d[k] <= dmin + (3 if k in ("dau", "ham") else 0.5)) | k.startswith("mao"))
        mm = m | muc
        f = mm.astype(np.uint8).copy()
        msk = np.zeros((f.shape[0] + 2, f.shape[1] + 2), np.uint8)
        cv2.floodFill(f, msk, (0, 0), 2)
        nl, ll, st, _ = cv2.connectedComponentsWithStats((f == 0).astype(np.uint8), 4)
        for i in range(1, nl):                      # lỗ kín (con ngươi, chấm sáng mắt, khe giữa răng): lấp; lòng miệng thì không
            if not (do & (ll == i)).any():
                mm |= ll == i
        mk[k] = mm
    imgs = {}
    for k, m in mk.items():
        o = np.zeros((h, w, 4), np.uint8)
        o[m, :3] = sub[m]
        o[m, 3] = 255
        imgs[k] = o
    # (bỏ 2026-11-17) tấm mào độn màu phẳng phần nấp sau mảnh đè: lúc ngửa đầu lộ mảng kem không viền
    for k, tr in ():
        che = np.logical_or.reduce([mk[t] for t in tr])
        bu = cv2.dilate(mk[k].astype(np.uint8), el(22)).astype(bool) & che & ~mk[k]
        c = np.median(sub[vung[k]], 0).astype(np.uint8)
        imgs[k][bu, :3] = c
        imgs[k][bu, 3] = 255
    # sọ dưới chỗ nụ ngà che (lộ ra khi há): màu mặt phẳng, chỉ phần gần da mặt hơn miệng / răng / hàm
    hull = cv2.convexHull(np.argwhere(mk["dau"])[:, ::-1].astype(np.int32))
    hu = np.zeros((h, w), np.uint8)
    cv2.fillPoly(hu, [hull], 1)
    da = np.isin(lab, [221, 286])
    khac = do | mk["ham"] | np.isin(lab, [422, 424, 440, 441, 469, 479, 499])
    d_da = cv2.distanceTransform((~da).astype(np.uint8), cv2.DIST_L2, 5)
    d_kh = cv2.distanceTransform((~khac).astype(np.uint8), cv2.DIST_L2, 5)
    mat = np.median(sub[lab == 286], 0).astype(np.uint8)
    for k in ("nanh1", "nanh2"):
        bd = cv2.dilate(mk[k].astype(np.uint8), el(2)).astype(bool) & hu.astype(bool) & ~mk["dau"] & ~do & (d_da < d_kh)
        imgs["dau"][bd, :3] = mat
        imgs["dau"][bd, 3] = 255
    os.makedirs(CUNG, exist_ok=True)
    DAT = json.load(open(os.path.join(CUNG2, "dat.json"), encoding="utf-8"))
    full = {}
    for k, im in imgs.items():
        F = np.zeros((H, W, 4), np.uint8)
        F[Y0:Y0 + h, X0:X0 + w] = im
        a = cv2.GaussianBlur(F[..., 3].astype(np.float32), (0, 0), 0.6)
        F[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
        full[k] = F
        o, (ox, oy) = nan_nguoc(k, F)
        ys_, xs_ = np.nonzero(o[..., 3] > 8)
        a0, b0, a1, b1 = xs_.min(), ys_.min(), xs_.max() + 1, ys_.max() + 1
        Image.fromarray(o[b0:b1, a0:a1], "RGBA").save(os.path.join(CUNG, k + ".png"))
        DAT[k] = {"slot": SLOT[k], "hop": [int(ox + a0), int(oy + b0), int(ox + a1), int(oy + b1)],
                  "nguon": "sau_dat_non/tai_ve/L1_duyet.png (concept B, cắt thẳng, nắn về khung concept dạng 2)", "phu": 1.0}
        print(k, "→", SLOT[k], "hộp", DAT[k]["hop"])
    # lòng miệng: đĩa dạng 2 đổi sang đất nung của B, XÉN trong hình bóng đầu B (mõm B nhỏ hơn: đĩa cũ lòi ra ngoài mõm)
    g = np.asarray(Image.open(os.path.join(CUNG2, "mieng.png")).convert("RGBA")).copy()
    rgb = g[..., :3].astype(np.float32)
    do2 = (g[..., 3] > 0) & (rgb[..., 0] > rgb[..., 1] + 40) & (rgb.mean(2) > 60)
    rgb[do2] += DO_MAU - np.median(rgb[do2], 0)
    g[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    dau_B = np.zeros((H, W, 4), np.uint8)
    hb = np.zeros((h, w), bool)
    for k in ("dau", "ham", "nanh1", "nanh2"):
        hb |= mk[k]
    from scipy import ndimage as nd
    hb = nd.binary_fill_holes(hb | do)                  # nét gạch sẫm trong lòng miệng không thuộc vùng nào: lấp
    hb = cv2.erode(hb.astype(np.uint8), el(3)).astype(bool)
    dau_B[Y0:Y0 + h, X0:X0 + w][hb] = 255
    cl, (cx0, cy0) = nan_nguoc("mieng", dau_B, pad=40)
    mx_, my_ = DAT["mieng"]["hop"][:2]
    o_ = np.zeros(g.shape[:2], np.float32)
    ys_, xs_ = np.indices(g.shape[:2])
    yy, xx = ys_ + my_ - cy0, xs_ + mx_ - cx0
    ok = (yy >= 0) & (xx >= 0) & (yy < cl.shape[0]) & (xx < cl.shape[1])
    o_[ok] = cl[yy[ok], xx[ok], 3] / 255.0
    g[..., 3] = (g[..., 3] * o_).astype(np.uint8)
    Image.fromarray(g, "RGBA").save(os.path.join(CUNG, "mieng.png"))
    print("lòng miệng giữ", f"{(g[..., 3] > 127).sum()} điểm (xén ngoài đầu B)")
    for k in ("mat", "may", "vong"):                 # rig ẩn các slot này nhưng còn đọc hộp mắt (tâm vành mềm)
        if os.path.exists(os.path.join(CUNG2, k + ".png")):
            shutil.copy(os.path.join(CUNG2, k + ".png"), os.path.join(CUNG, k + ".png"))
    json.dump(DAT, open(os.path.join(CUNG, "dat.json"), "w", encoding="utf-8"), indent=1)
    # tờ soi: B | ghép lại trên khung B (lòng miệng đất nung sau cùng) | tách rời
    ghep = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    dia = np.zeros((H, W, 4), np.uint8)
    hmask = np.zeros((H, W), np.uint8)
    cv2.fillPoly(hmask, [cv2.convexHull(hm.astype(np.int32))], 1)
    dia[hmask.astype(bool)] = (*DO_MAU, 255)
    ghep.alpha_composite(Image.fromarray(dia, "RGBA"))
    for k in ("maoC", "maoB", "maoA", "ham", "dau", "nanh1", "nanh2"):
        ghep.alpha_composite(Image.fromarray(full[k], "RGBA"))
    tach = Image.new("RGBA", (W, H), (150, 150, 150, 255))
    for k, dx, dy in (("maoC", -40, -10), ("maoB", -30, -40), ("maoA", 0, -50), ("ham", 0, 60), ("dau", 0, 0), ("nanh1", -30, 90),
                      ("nanh2", 30, 90)):
        tach.alpha_composite(Image.fromarray(np.roll(np.roll(full[k], dy, 0), dx, 1), "RGBA"))
    box = (600, 200, 1130, 680)
    o = Image.new("RGB", (530 * 3, 480), (150, 150, 150))
    o.paste(Image.fromarray(A).crop(box), (0, 0))
    o.paste(ghep.crop(box).convert("RGB"), (530, 0))
    o.paste(tach.crop(box).convert("RGB"), (1060, 0))
    o.save(os.path.join(MAU, "_dau_B.png"))
    print("lòng miệng:", len(do_id), "vùng; tờ soi", os.path.join(MAU, "_dau_B.png"))


# ---------------------------------------------------------------- đổi màu
def doi_mau(rgba, cap, giu_toi=95):
    """cap: [(màu nguồn, màu đích)]; điểm chưa phải mực (trung bình ≥ giu_toi) gán lớp nguồn gần nhất rồi dời theo độ lệch lớp (giữ vân
    sáp). Trả bản mới."""
    a = rgba.copy()
    rgb = a[..., :3].astype(np.float32)
    src = np.array([c for c, _ in cap], np.float32)
    dst = np.array([c for _, c in cap], np.float32)
    m = (a[..., 3] > 0) & (rgb.mean(2) >= giu_toi)
    lop = ((rgb[m][:, None, :] - src[None]) ** 2).sum(-1).argmin(1)
    rgb[m] += (dst - src)[lop]
    a[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return a


THAN = [((240, 211, 156), (247, 205, 180)),        # bụng kem → kem hồng
        ((228, 175, 97), (229, 160, 130)),          # thân cát → hồng giun
        ((219, 156, 77), (218, 146, 116)),          # mảng sẫm (giáp sau đầu) → hồng sẫm
        ((168, 121, 73), (178, 114, 88))]           # vạch vòng đốt


def than():
    os.makedirs(PART, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    for i in range(1, 11):
        t = f"P_bozi_{i:02d}"
        a = np.asarray(Image.open(os.path.join(PART2, t + ".png")).convert("RGBA"))
        Image.fromarray(doi_mau(a, THAN, 110), "RGBA").save(os.path.join(PART, t + ".png"))
    from quai import anh
    p = anh.to_moi_nhat(os.path.join(LON, "tai_ve"), "N_L")
    a = np.asarray(Image.open(p).convert("RGBA"))
    a2 = doi_mau(a, THAN, 110)
    trang = a[..., :3].min(2) > 236                 # nền giấy giữ trắng (doc_to tách nền theo trắng)
    a2[trang] = a[trang]
    Image.fromarray(a2[..., :3]).save(os.path.join(TAI, "N_L.png"))
    print("thân: 10 part + N_L từ", os.path.basename(p))


RAU = [((43, 33, 24), (43, 33, 24)), ((93, 58, 33), (148, 97, 56)), ((120, 83, 55), (170, 122, 80)), ((245, 172, 52), (248, 163, 32))]


def rau():
    os.makedirs(PART, exist_ok=True)
    for k in ("01", "02", "03", "04", "05", "06", "07"):
        t = f"A_chuxu_{k}"
        a = np.asarray(Image.open(os.path.join(PART2, t + ".png")).convert("RGBA")).copy()
        rgb = a[..., :3].astype(np.float32)
        # khấc dưới hạt ngọn: hàng hẹp nhất của hình trong đoạn đầu (ngọn ở trên)
        rong = (a[..., 3] > 127).sum(1)
        top = int(np.argmax(rong > 0))
        mo = top + int(np.argmax(rong[top: top + 60]))              # hàng rộng nhất của hạt ngọn (hình thoi)
        doan = rong[mo: mo + 50]
        khac = mo + int(np.argmin(doan))
        if doan.min() > 0.8 * rong[mo]:                             # ngọn tròn, không khấc (ảnh 05): cả dải thành thân râu
            khac = top
        src = np.array([c for c, _ in RAU], np.float32)
        lop = ((rgb[..., None, :] - src[None, None]) ** 2).sum(-1).argmin(-1)
        hp = (a[..., 3] > 0) & (lop == len(RAU) - 1)                 # lớp hổ phách (kể cả điểm mép sẫm)
        duoi = np.zeros_like(hp)
        duoi[khac:] = True
        b = doi_mau(a, RAU, 0)
        # dải hổ phách dưới khấc → thân râu (nâu nhạt), giữ vân
        rr = rgb[hp & duoi]
        if len(rr):
            b[..., :3][hp & duoi] = np.clip(rr - np.median(rr, 0) + np.array([158, 108, 64]), 0, 255).astype(np.uint8)
        # vạch sẫm lẻ trong thân râu (mép cũ giữa dải hổ phách và thân): thành màu thân, nét viền dọc mép giữ
        trong = cv2.erode((a[..., 3] > 127).astype(np.uint8), np.ones((15, 15), np.uint8)).astype(bool)
        sam = trong & (b[..., :3].astype(int).mean(2) < 120)
        sam[:khac + 4] = False
        if sam.any():
            ok_ = trong & ~sam
            ok_[:khac + 4] = False
            _, lb = cv2.distanceTransformWithLabels((~ok_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
            tra[lb[ok_]] = b[..., :3][ok_]
            b[..., :3][sam] = tra[lb[sam]]
        Image.fromarray(b, "RGBA").save(os.path.join(PART, t + ".png"))
        print(t, "khấc ở hàng", khac, "/", a.shape[0], "(trên cùng", top, ")")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "khop":
        khop()
    elif a[0] == "dau":
        dau()
    elif a[0] == "than":
        than()
    elif a[0] == "rau":
        rau()
