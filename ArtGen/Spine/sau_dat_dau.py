# -*- coding: utf-8 -*-
"""Sâu đất (sau_dat): CỤM ĐẦU cắt THẲNG từ concept đã duyệt (cách lai, skill pokiclash-spine-rig mục 21), thay bốn lượt GPT "đúng chỗ"
(K1–K4) vẽ lệch concept: chỉ một vòng giáp chữ C thay hai vòng, vành đầu hẹp mất má, ngà dịch trái ~60 px → hở đầu, hàm lệch (người dùng
2026-11-17: "rig đầu ghép lỗi bị hở rồi", "vẫn lỗi").

Mảng kín giữa nét mực trên concept (số vùng đọc ở mau/_vung_dau.png) → nhóm:
    dau   (P_shange)  hai vòng giáp sau đầu, vành đầu, má, gờ mày, mắt, răng trên; lòng miệng khoét trong
    ham   (P_xiae_01) thân hàm dưới, răng dưới (hốc ngà nằm trong thân hàm)
    nanh1 / nanh2 (P_jiao_07 / 09) hai ngà, vẽ TRƯỚC đầu, cùng xương hàm
Mực: chia cho nhóm gần nhất trong 7 px (mực đường môi cho cả đầu lẫn hàm). Chỗ bị che lấy từ mảnh GPT: hàm dưới phần đầu và ngà che → mảnh
`ham` của K2 (đuôi hàm vẽ đủ); đầu dưới chỗ ngà che → màu má phẳng. Lòng miệng: đĩa K3 (`mieng`) nằm sau, co giãn theo hàm.
Mảnh cũ của K1, K2, K4 giữ ở manh/cung/<tên>_k.png; `vong`, `may`, `mat` gộp vào `dau` (rig ẩn P_jiao_04, P_jiao_08, P_jiao_05).

    sau_dat_dau.py         → manh/cung/{dau,ham,nanh1,nanh2}.png + dat.json + mau/_dau_lien.png (tờ soi)
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
import sau_dat  # noqa: E402,F401
import tho5  # noqa: E402

G = tho5.dat("sau_dat")
W, H = 1536, 1024
CUNG = os.path.join(G.BASE, "manh", "cung")
X0, Y0, X1, Y1 = 720, 330, 1080, 680               # khung vùng đầu trên concept
DAU = {89, 134, 225, 231, 159, 215, 234, 226, 228, 229, 230, 232, 233, 235, 236, 238, 240, 241}
HAM = {250, 276, 248, 260, 264, 275, 284, 292, 294}
NGA = {"nanh1": {251}, "nanh2": {287}}
DO = {239, 247, 252, 280}                           # lòng miệng (khoét)
SLOT = {"dau": "P_shange", "ham": "P_xiae_01", "nanh1": "P_jiao_07", "nanh2": "P_jiao_09"}


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def doc_manh(k, path=None):
    """mảnh GPT cũ (đặt ở hộp trên concept) → RGBA cỡ cả tờ."""
    DAT = json.load(open(os.path.join(CUNG, "dat.json"), encoding="utf-8"))
    im = Image.open(path or os.path.join(CUNG, k + ".png")).convert("RGBA")
    out = np.zeros((H, W, 4), np.uint8)
    x0, y0 = DAT[k]["hop"][:2]
    a = np.asarray(im)
    out[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
    return out


def main():
    A = np.asarray(Image.open(os.path.join(G.TAI, "L1_duyet.png")).convert("RGB").resize((W, H)))
    sub = A[Y0:Y1, X0:X1].astype(int)
    toi = sub.mean(2) < 95
    trang = sub.min(2) > 236
    _, lab = cv2.connectedComponents((~toi & ~trang).astype(np.uint8), connectivity=4)
    nhom = {"dau": DAU, "ham": HAM, **NGA}
    vung = {k: np.isin(lab, list(v)) for k, v in nhom.items()}
    do = np.isin(lab, list(DO))
    khac = (lab > 0) & ~do & ~np.logical_or.reduce(list(vung.values()))
    # mực → nhóm gần nhất (trong 7 px); mực đường môi cho cả đầu và hàm
    d = {k: cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5) for k, m in vung.items()}
    dkhac = cv2.distanceTransform((~khac).astype(np.uint8), cv2.DIST_L2, 5)
    dmin = np.minimum.reduce(list(d.values()))
    mk = {}
    for k, m in vung.items():
        muc = toi & (d[k] < 7) & (d[k] <= dmin + (3 if k in ("dau", "ham") else 0.5))
        mm = m | muc
        # lỗ nhỏ kín (chấm sáng mắt, mẩu giữa răng): lấp; lòng miệng đỏ thì không
        f = mm.astype(np.uint8).copy()
        msk = np.zeros((f.shape[0] + 2, f.shape[1] + 2), np.uint8)
        cv2.floodFill(f, msk, (0, 0), 2)
        lo = (f == 0)
        n, ll, st, _ = cv2.connectedComponentsWithStats(lo.astype(np.uint8), 4)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] < 80 and not (do & (ll == i)).any():
                mm |= ll == i
        mk[k] = mm
    full = {k: np.zeros((H, W), bool) for k in mk}
    for k, m in mk.items():
        full[k][Y0:Y1, X0:X1] = m

    def rgba(m):
        out = np.zeros((H, W, 4), np.uint8)
        out[m, :3] = A[m]
        out[m, 3] = 255
        return out

    imgs = {k: rgba(full[k]) for k in full}
    # bản K cũ giữ lại một lần
    for k in ("dau", "ham", "nanh1", "nanh2"):
        p, pk = os.path.join(CUNG, k + ".png"), os.path.join(CUNG, k + "_k.png")
        if os.path.exists(p) and not os.path.exists(pk):
            shutil.copy(p, pk)
    DAT = json.load(open(os.path.join(CUNG, "dat.json"), encoding="utf-8"))
    for k in ("dau", "ham", "nanh1", "nanh2"):
        if k + "_k" not in DAT and k in DAT:
            DAT[k + "_k"] = dict(DAT[k])
    json.dump(DAT, open(os.path.join(CUNG, "dat.json"), "w", encoding="utf-8"), indent=1)
    # chỗ bị che: hàm dưới đầu / dưới ngà → mảnh hàm K2 (đuôi hàm vẽ đủ)
    k2 = doc_manh("ham_k", os.path.join(CUNG, "ham_k.png"))
    che_ham = cv2.dilate((full["dau"] | full["nanh1"] | full["nanh2"]).astype(np.uint8), el(3)).astype(bool)
    bu = che_ham & (k2[..., 3] > 128) & ~full["ham"]
    imgs["ham"][bu] = k2[bu]
    # đầu dưới chỗ ngà che → màu má phẳng (vùng 234), chỉ trong bao lồi của đầu
    hull = cv2.convexHull(np.argwhere(full["dau"])[:, ::-1].astype(np.int32))
    hm = np.zeros((H, W), np.uint8)
    cv2.fillPoly(hm, [hull], 1)
    ma = np.median(A[Y0:Y1, X0:X1][lab == 234], 0).astype(np.uint8)
    # chỉ tô phần thuộc MÁ (gần vùng má 234 hơn lòng miệng / răng): bản đầu tô lấn vào lòng miệng → mảng vàng đất lọt trong miệng khi há
    mieng_rang = np.pad(do | np.isin(lab, [226, 228, 229, 230, 232, 233, 235, 236, 238, 240, 241, 248, 260, 264, 275, 284, 292, 294]),
                        ((Y0, H - Y1), (X0, W - X1)))
    d_ma = cv2.distanceTransform((~np.pad(lab == 234, ((Y0, H - Y1), (X0, W - X1)))).astype(np.uint8), cv2.DIST_L2, 5)
    d_mr = cv2.distanceTransform((~mieng_rang).astype(np.uint8), cv2.DIST_L2, 5)
    for k in ("nanh1", "nanh2"):
        bd = cv2.dilate(full[k].astype(np.uint8), el(2)).astype(bool) & hm.astype(bool) & ~full["dau"]
        bd &= ~np.pad(do, ((Y0, H - Y1), (X0, W - X1))) & (d_ma < d_mr)
        imgs["dau"][bd, :3] = ma
        imgs["dau"][bd, 3] = 255
    # lưu: cắt sát, mép mềm 1 px
    for k, im in imgs.items():
        a = im[..., 3].astype(np.float32)
        a = cv2.GaussianBlur(a, (0, 0), 0.6)
        ys, xs = np.nonzero(a > 8)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        out = im[y0:y1, x0:x1].copy()
        out[..., 3] = np.clip(a[y0:y1, x0:x1], 0, 255).astype(np.uint8)
        Image.fromarray(out, "RGBA").save(os.path.join(CUNG, k + ".png"))
        DAT[k] = {"slot": SLOT[k], "hop": [int(x0), int(y0), int(x1), int(y1)], "nguon": "L1_duyet.png (cắt thẳng) + mảnh GPT cho chỗ che",
                  "phu": 1.0}
        print(k, "→", SLOT[k], f"hộp {x0},{y0}–{x1},{y1}")
    json.dump(DAT, open(os.path.join(CUNG, "dat.json"), "w", encoding="utf-8"), indent=1)
    # tờ soi: concept | ghép lại (lòng miệng K3 sau cùng) | từng mảnh trên nền xám
    k3 = doc_manh("mieng")
    ghep = np.full((H, W, 4), 255, np.uint8)
    ghep[..., 3] = 255
    G2 = Image.fromarray(ghep, "RGBA")
    for k in ("mieng", "ham", "dau", "nanh1", "nanh2"):
        G2.alpha_composite(Image.fromarray(k3 if k == "mieng" else imgs[k], "RGBA"))
    con = Image.fromarray(A).convert("RGBA")
    o = Image.new("RGB", (560 * 3, 480), (150, 150, 150))
    o.paste(con.crop((560, 220, 1120, 700)).convert("RGB"), (0, 0))
    o.paste(G2.crop((560, 220, 1120, 700)).convert("RGB"), (560, 0))
    tach = Image.new("RGBA", (W, H), (150, 150, 150, 255))
    for k, dx, dy in (("ham", 0, 70), ("dau", -10, -30), ("nanh1", -60, 60), ("nanh2", 40, 70)):
        tach.alpha_composite(Image.fromarray(np.roll(np.roll(imgs[k], dy, 0), dx, 1), "RGBA"))
    o.paste(tach.crop((560, 220, 1120, 700)).convert("RGB"), (1120, 0))
    p = os.path.join(G.MAU, "_dau_lien.png")
    o.save(p)
    print(p)


if __name__ == "__main__":
    main()
