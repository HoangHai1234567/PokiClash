# -*- coding: utf-8 -*-
"""Rồng vây (mã làm việc rong_vay, tướng thứ 8 đảo Thủy): chia nhóm mảnh, cắt mảnh GPT, ghép soi. Animation làm sau.

Mảnh chia MỘT – MỘT theo con gốc monster_3458 (bảng ở inbox/rong_vay_ghichu.md mục 3). Mỗi mảnh do GPT vẽ lại từ concept đã duyệt,
ĐÚNG CHỖ, ĐÚNG CỠ, thành một hình kín có cả phần khuất; mã chỉ tách nền trắng và xếp lớp.

    py -3 -I ArtGen/Spine/rong_vay.py nhom          chia nhóm mảnh không chạm nhau → inbox/rong_vay_1/mau/nhom_<X>.png + nhom.json
    py -3 -I ArtGen/Spine/build_rong_vay.py         → gui_gpt/rong_vay_1/luot_2_nhom_<X>.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rong_vay_1/luot_2_nhom_<X>.txt
    py -3 -I ArtGen/Spine/rong_vay.py cat [X ...]   cắt ảnh tai_ve/N_<X>.png thành mảnh → inbox/rong_vay_1/manh/<tên>.png (cả khung)
    py -3 -I ArtGen/Spine/rong_vay.py ghep          xếp lớp theo thứ tự vẽ, so với concept → inbox/rong_vay_1/rig/ghep.png, so_concept.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CODE = "rong_vay"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
MANH = os.path.join(BASE, "manh")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024

# slot con gốc → tên mảnh của mình (thứ tự vẽ lấy theo slot). Gộp: gờ mày (P_erduo) và mắt mở vào mảnh đầu.
TEN = {
    "P_yuqi16": "vay_16", "P_weiba": "vay_duoi", "P_yuqi13": "vay_13", "P_yuqi12": "vay_12", "P_shenti06": "than_6",
    "P_shenti05": "than_5", "P_chibangL06": "canh_x_mang", "P_chibangL05": "canh_x_song", "P_yuqi11": "vay_11",
    "P_yuqi10": "vay_10", "P_yuqi15": "vay_15", "P_yuqi14": "vay_14", "P_shenti04": "than_4", "P_yuqi08": "vay_08",
    "P_shenti03": "than_3", "P_yuqi09": "vay_09", "P_yuqi07": "vay_07", "P_yuqi06": "vay_06", "P_shenti02": "than_2",
    "P_shenti01": "than_1", "P_tou": "dau", "P_yuqi05": "tai_lon", "P_yuqi04": "sung_s", "P_yuqi03": "sung_t",
    "P_zuiba02": "mo_duoi", "P_zuiba01": "mo_tren", "P_yuqi01": "vay_ma",
    "P_chibangR06": "canh_g_mang", "P_chibangR08": "canh_g_song",
}
GOP = {"P_erduo": "P_tou"}                     # mảnh nhỏ nhập vào mảnh khác
BO = ("P_shenti07", "P_chibangR08_2", "P_chibangR08_3", "P_yanjing01", "P_yanjing02")   # dùng lại ảnh / làm ở bước animation
KE = 16                                         # nới mỗi mảnh từng này px khi xét chạm nhau (hai mảnh cùng nhóm cách nhau >= 2 KE)
TOI_DA = 6                                      # số mảnh tối đa một nhóm


# ---------------------------------------------------------------- nhãn vùng từng mảnh trên CONCEPT đã duyệt
LOAI = {t: ("than" if t.startswith("than") else "dau" if t == "dau" else "sung" if t.startswith("sung") else
            "mo" if t.startswith("mo_") else "mang" if t.endswith("_mang") else "song" if t.endswith("_song") else "vay")
        for t in TEN.values()}
THEM = {"P_yuqi02": "tai_lon", "P_shenti07": "vay_duoi", "P_chibangR08_2": "canh_g_song", "P_chibangR08_3": "canh_x_song", "P_yanjing01": "dau",
        "P_erduo": "dau"}                                       # slot phụ của rig → mảnh của mình (chỉ để bỏ phiếu vùng)
MAU_LOP = {"cham": (58, 74, 178), "kem": (252, 236, 205), "lam": (115, 163, 180), "navy": (45, 55, 138), "den": (41, 40, 46),
           "vang": (247, 162, 63)}        # màu đo trên concept đã duyệt
HOP = {"cham": {"than", "dau", "vay_duoi"}, "kem": {"than", "mang"}, "lam": {"vay", "mang"}, "navy": {"vay", "mang", "song", "dau"},
       "den": {"sung", "mo", "dau"}, "vang": {"dau", "than"}}
RIENG = ("mo_tren", "mo_duoi")     # không vào nhóm tự động: vẽ trên tờ phóng to riêng
EP = []          # ép tay: (x, y, tên mảnh): cả ô mực chứa điểm (x, y) của concept thuộc mảnh đó


def hinh(con):
    """hình của concept: bỏ nền trắng nối mép và giấy trắng khép kín lớn (lòng vòng cuộn); chấm trắng nhỏ (mắt) vẫn là hình."""
    from quai import anh
    trang = con.min(axis=2) > 236
    fg = ~anh.nen_tu_mep(trang)
    n, lab, st, _ = cv2.connectedComponentsWithStats((trang & fg).astype(np.uint8), 8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 400:
            fg[lab == i] = False
    return fg


def hop_le(ten, lop):
    return LOAI[ten] in HOP[lop] or ten in HOP[lop]


def nhan():
    """chia concept thành vùng từng mảnh: ô = cụm liền không phải nét mực; mỗi ô bỏ phiếu theo mặt nạ rig (chỉ mảnh hợp màu ô);
    ô liền nhiều mảnh (thân chàm) chia theo mặt nạ rig. Ra mau/thay/<tên>.png (phần lộ), mau/khuat/<tên>.png (phần khuất), nhan.png."""
    import rong_vay_bo_cuc as B
    from quai import anh
    _, masks, order = B.dung(luu=False)
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    fg = hinh(con)
    sm = cv2.medianBlur(con, 3).astype(int)
    r, g, b = sm[..., 0], sm[..., 1], sm[..., 2]
    toi = fg & (sm.max(axis=2) < 112) & (b - r < 25)          # nét mực nâu và mảng đen than (navy, chàm có b - r lớn nên không dính)
    e6 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    day = cv2.dilate(cv2.morphologyEx(toi.astype(np.uint8), cv2.MORPH_OPEN, e6), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    den = toi & day.astype(bool)                               # mảng đen dày: sừng, mỏ (kể cả viền của chúng)
    ink = cv2.dilate((toi & ~den).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & fg & ~den
    # lớp màu từng điểm (ảnh làm mượt) rồi ô = cụm liền CÙNG LỚP MÀU không phải nét mực: hai bộ phận khác màu không dính nhau
    # dù nét mực giữa chúng bị hở
    keys = list(MAU_LOP)
    pal = np.array([MAU_LOP[k] for k in keys], float)
    sm7 = cv2.medianBlur(con, 7).astype(float)
    lop_all = np.argmin(((sm7[:, :, None, :] - pal[None, None]) ** 2).sum(axis=3), axis=2).astype(np.int32)
    lop_all[den] = keys.index("den")
    lab = np.zeros((H, W), np.int32)
    n = 1
    for k in range(len(keys)):
        nk, lk = cv2.connectedComponents((fg & ~ink & (lop_all == k)).astype(np.uint8), connectivity=8)
        lab[lk > 0] = lk[lk > 0] + n - 1
        n += nk - 1
    # mặt nạ rig theo tên mảnh của mình, kèm thứ tự vẽ
    rig = {}
    for s, m in masks.items():
        t = TEN.get(s) or THEM.get(s)
        if t:
            o = order.get(s, 0) if s in TEN else order.get([k for k, v in TEN.items() if v == t][0], 0)
            if t in rig:
                rig[t] = (rig[t][0] | m, max(rig[t][1], o) if s in TEN else rig[t][1])
            else:
                rig[t] = (m, o)
    names = sorted(rig, key=lambda t: rig[t][1])
    idx = {t: i + 1 for i, t in enumerate(names)}
    own = np.zeros((H, W), np.int32)
    lop_px = np.full((H, W), -1, np.int8)
    flat = lab.ravel()
    order_px = np.argsort(flat, kind="stable")
    cuts = np.r_[0, np.cumsum(np.bincount(flat, minlength=n))]
    cells = []
    for c in range(1, n):
        ii = order_px[cuts[c]:cuts[c + 1]]
        if len(ii) < 25:
            continue
        k = int(lop_all.ravel()[ii[0]])
        lop_px.ravel()[ii] = k
        cells.append((c, ii, k))
    # ứng viên từng điểm: mảnh trên cùng của rig mà hợp màu ô
    cand = np.zeros((H, W), np.int32)
    for t in names:
        m = rig[t][0]
        for k, key in enumerate(keys):
            if hop_le(t, key):
                cand[m & (lop_px == k)] = idx[t]
    for c, ii, k in cells:
        v = cand.ravel()[ii]
        vv = v[v > 0]
        if len(vv) == 0:
            continue
        cnt = np.bincount(vv)
        top = int(np.argmax(cnt))
        if cnt[top] >= 0.7 * len(vv):
            own.ravel()[ii] = top
        else:
            own.ravel()[ii] = v
    for x, y, t in EP:
        own[lab == lab[y, x]] = idx[t]
    # điểm chưa có chủ trong ô: lấy chủ gần nhất cùng lớp màu; rồi nét mực và mẩu vụn: chủ gần nhất bất kỳ
    def gan_nhat(seed_mask, todo):
        src = (~seed_mask).astype(np.uint8)
        _, lb = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        lut = np.zeros(lb.max() + 1, np.int32)
        lut[lb[seed_mask]] = own[seed_mask]
        own[todo] = lut[lb[todo]]

    for k in range(len(keys)):
        seed = (own > 0) & (lop_px == k)
        todo = (own == 0) & (lop_px == k)
        if seed.any() and todo.any():
            gan_nhat(seed, todo)
    todo = fg & (own == 0)
    gan_nhat(own > 0, todo)
    own[~fg] = 0
    # lưu
    for d in ("thay", "khuat"):
        os.makedirs(os.path.join(MAU, d), exist_ok=True)
    rng = np.random.RandomState(7)
    cols = rng.randint(40, 255, (len(names) + 1, 3))
    vis = con.copy()
    F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
    txt = []
    for t in names:
        if t not in LOAI:
            continue
        v = own == idx[t]
        Image.fromarray(v.astype(np.uint8) * 255).save(os.path.join(MAU, "thay", t + ".png"))
        kh = rig[t][0] & fg & ~v
        kh = cv2.morphologyEx(kh.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))).astype(bool)
        Image.fromarray(kh.astype(np.uint8) * 255).save(os.path.join(MAU, "khuat", t + ".png"))
        vis[v] = (0.45 * vis[v] + 0.55 * cols[idx[t]]).astype(np.uint8)
        if v.any():
            ys, xs = np.nonzero(v)
            txt.append((xs.mean(), ys.mean(), t))
        print(f"{t:12s} lộ {int(v.sum()):6d} px, khuất {int(kh.sum()):6d} px")
    edge = cv2.morphologyEx(own.astype(np.uint16), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    vis[edge] = (255, 255, 255)
    im = Image.fromarray(vis)
    d = ImageDraw.Draw(im)
    for x, y, t in txt:
        d.text((x - 18, y - 6), t, fill=(255, 255, 255), font=F, stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(os.path.join(MAU, "nhan.png"))
    Image.fromarray(((ink | (toi & ~den)) * 255).astype(np.uint8)).save(os.path.join(MAU, "_muc.png"))
    sz = np.bincount(lab.ravel())
    print("ô lớn nhất:", sorted(sz[1:].tolist(), reverse=True)[:8])
    print(os.path.join(MAU, "nhan.png"))


HONG = (255, 105, 180)


def vung(t):
    """(phần lộ trên concept, phần khuất) của một mảnh."""
    v = np.asarray(Image.open(os.path.join(MAU, "thay", t + ".png"))) > 127
    k = np.asarray(Image.open(os.path.join(MAU, "khuat", t + ".png"))) > 127
    return v, k


def nhom():
    """chia nhóm mảnh không chạm nhau; tờ hướng dẫn mỗi nhóm = concept đã xoá mọi thứ ngoài các mảnh của nhóm (giữ nguyên chỗ),
    phần khuất của từng mảnh tô HỒNG để GPT vẽ bù."""
    names = [t for t in sorted(set(TEN.values())) if t not in RIENG and os.path.exists(os.path.join(MAU, "thay", t + ".png"))]
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    muc = np.asarray(Image.open(os.path.join(MAU, "_muc.png"))) > 127
    order = {v: i for i, v in enumerate(TEN.values())}          # TEN ghi theo thứ tự vẽ sau → trước? không: lấy từ rig
    import rong_vay_bo_cuc as B
    _, _, od = B.dung(luu=False)
    order = {TEN[s]: od.get(s, 0) for s in TEN}
    V, K, full = {}, {}, {}
    for t in names:
        V[t], K[t] = vung(t)
        nn, lb, st, _ = cv2.connectedComponentsWithStats(V[t].astype(np.uint8), 8)      # bỏ mẩu vụn rời của phần lộ
        for i in range(1, nn):
            if st[i, cv2.CC_STAT_AREA] < 250:
                V[t][lb == i] = False
        full[t] = V[t] | K[t]
    os.makedirs(os.path.join(MAU, "day"), exist_ok=True)
    for t in names:
        Image.fromarray(full[t].astype(np.uint8) * 255).save(os.path.join(MAU, "day", t + ".png"))
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * KE + 1, 2 * KE + 1))
    big = {t: cv2.dilate(full[t].astype(np.uint8), k).astype(bool) for t in names}
    groups = []
    for t in sorted(names, key=lambda t: -int(full[t].sum())):
        for g in groups:
            if len(g) < TOI_DA and not any((big[t] & big[u]).any() for u in g):
                g.append(t)
                break
        else:
            groups.append([t])
    F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    e6 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    out = {}
    for i, g in enumerate(groups):
        X = chr(ord("A") + i)
        im = np.full((H, W, 3), 255, np.uint8)
        info = []
        for t in sorted(g, key=lambda t: order[t]):
            keep = V[t] | (cv2.dilate(V[t].astype(np.uint8), e6).astype(bool) & muc)      # phần lộ + trọn nét mực viền của nó
            pink = K[t] & ~keep
            im[pink] = HONG
            im[keep] = con[keep]
            ys, xs = np.nonzero(full[t])
            info.append({"ten": t, "order": order[t], "tam": [float(xs.mean()), float(ys.mean())],
                         "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                         "lo": int(V[t].sum()), "khuat": int(K[t].sum())})
        Image.fromarray(im).save(os.path.join(MAU, f"nhom_{X}.png"))
        so = Image.fromarray(im)
        d = ImageDraw.Draw(so)
        for q in info:
            d.text((q["tam"][0] - 20, q["tam"][1] - 8), q["ten"], fill=(255, 255, 255), font=F, stroke_width=2, stroke_fill=(0, 0, 0))
        so.save(os.path.join(MAU, f"nhom_{X}_ten.png"))
        out[X] = info
        print(X, [q["ten"] for q in info])
    json.dump(out, open(os.path.join(MAU, "nhom.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


THAN = ["than_1", "than_2", "than_3", "than_4", "than_5"]      # các khúc thân nối nhau lộ ra trên concept: gen LIỀN một ảnh rồi cắt


def nhom_than():
    """tờ hướng dẫn gen CẢ THÂN liền một ảnh (người dùng 2026-11-11: "những khớp nối thì gen cả con ra rồi cắt chứ không gen riêng
    không thì sẽ lệch"): concept đã xoá mọi thứ ngoài năm khúc thân, phần thân bị cánh, vây, đầu che tô hồng → mau/nhom_T.png."""
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    muc = np.asarray(Image.open(os.path.join(MAU, "_muc.png"))) > 127
    e6 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    V = np.zeros((H, W), bool)
    K = np.zeros((H, W), bool)
    for t in THAN:
        v, k = vung(t)
        V |= v
        K |= k
    keep = V | (cv2.dilate(V.astype(np.uint8), e6).astype(bool) & muc)
    pink = K & ~keep
    im = np.full((H, W, 3), 255, np.uint8)
    im[pink] = HONG
    im[keep] = con[keep]
    Image.fromarray(im).save(os.path.join(MAU, "nhom_T.png"))
    print(os.path.join(MAU, "nhom_T.png"), "lộ", int(V.sum()), "px, khuất", int(pink.sum()), "px")


def cat_than(chom=34, mem=10):
    """cắt ảnh cả thân N_T thành năm khúc: dời cả ảnh cho khớp concept, gán mỗi điểm thân cho khúc gần nhất (theo vùng lộ đã tách trên
    concept), mỗi khúc lấy thêm `chom` px sang khúc kề (mép cắt mờ dần `mem` px, KHÔNG có nét mực vì là lát cắt của cùng một ảnh:
    vạch bụng hai khúc trùng nhau từng điểm). Bản gen riêng cũ dời sang manh/_rieng/."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, "N_T")
    if not path:
        print("T chưa có ảnh")
        return
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, "_N_T_doi_co.png")
        im.save(path)
    to = anh.doc_to(path, dien_tich_min=4000, gop_px=20)
    rgba = to.rgba.copy()
    al = np.isin(to.lab, [i for m in to.manh for i in m["ids"]])
    rgba[..., 3] = (rgba[..., 3] * anh.gian(al, 2)).astype(np.uint8)
    # lòng vòng cuộn là giấy trắng khép kín: doc_to giữ nó như một phần của mảnh (đục ra, không thì lòng vòng thành mảng trắng đặc)
    trang = (rgba[..., :3].min(axis=2) > 236) & (rgba[..., 3] > 127)
    nn, lb_, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), 8)
    for i in range(1, nn):
        if st[i, cv2.CC_STAT_AREA] > 400:
            lo = cv2.dilate((lb_ == i).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
            rgba[..., 3][lo] = 0
            print(f"  đục lòng giấy trắng khép kín {int(st[i, cv2.CC_STAT_AREA])} px")
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    Vs = {t: vung(t)[0] for t in THAN}
    Vall = np.zeros((H, W), bool)
    for v in Vs.values():
        Vall |= v
    # dời cả ảnh cho phần lộ khớp màu concept
    s2 = lambda a: cv2.GaussianBlur(cv2.resize(a, (W // 2, H // 2), interpolation=cv2.INTER_AREA), (0, 0), 1.5).astype(np.float32)  # noqa: E731
    c2, p2 = s2(con), s2(rgba[..., :3])
    a2 = cv2.resize(rgba[..., 3], (W // 2, H // 2), interpolation=cv2.INTER_AREA) > 127
    v2 = cv2.resize(Vall.astype(np.uint8), (W // 2, H // 2), interpolation=cv2.INTER_NEAREST).astype(bool)
    R = 14
    ys, xs = np.nonzero(v2)
    y0, y1, x0, x1 = max(R, ys.min()), min(H // 2 - R, ys.max() + 1), max(R, xs.min()), min(W // 2 - R, xs.max() + 1)
    best = None
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            e = np.minimum(1.0, np.abs(p2[y0 - dy:y1 - dy, x0 - dx:x1 - dx] - c2[y0:y1, x0:x1]).sum(axis=2) / 255.0)
            e[~a2[y0 - dy:y1 - dy, x0 - dx:x1 - dx]] = 1.0
            sc = float(e[v2[y0:y1, x0:x1]].mean())
            if best is None or sc < best[0]:
                best = (sc, dx, dy)
            if dx == 0 and dy == 0:
                zero = sc
    sc, dx, dy = best
    if zero - sc < 0.01:
        dx = dy = 0
    DX, DY = 2 * dx, 2 * dy
    out = np.zeros_like(rgba)
    ya, yb, xa, xb = max(0, DY), min(H, H + DY), max(0, DX), min(W, W + DX)
    out[ya:yb, xa:xb] = rgba[ya - DY:yb - DY, xa - DX:xb - DX]
    rgba = out
    al = rgba[..., 3] > 127
    print(f"T {os.path.basename(path)}: dời ({DX:+d}, {DY:+d}) px, lệch màu phần lộ {zero:.3f} → {sc if (dx or dy) else zero:.3f}; "
          f"thân {int(al.sum())} px, concept lộ {int(Vall.sum())} px, lộ mà ảnh trống {int((Vall & ~al).sum())} px")
    # nhãn khúc cho mọi điểm thân: vùng lộ của khúc nào thì thuộc khúc đó; điểm còn lại theo vùng lộ gần nhất
    lab = np.zeros((H, W), np.int32)
    for i, t in enumerate(THAN, 1):
        lab[Vs[t] & al] = i
    seed = lab > 0
    _, lb = cv2.distanceTransformWithLabels((~seed).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lut = np.zeros(lb.max() + 1, np.int32)
    lut[lb[seed]] = lab[seed]
    lab = np.where(al, lut[lb], 0)
    cu = os.path.join(MANH, "_rieng")
    os.makedirs(cu, exist_ok=True)
    os.makedirs(os.path.join(MAU, "day"), exist_ok=True)
    Image.fromarray((lab * 40).astype(np.uint8)).save(os.path.join(MAU, "_than_nhan.png"))      # nhãn khúc (x40) trên ảnh cả thân
    for i, t in enumerate(THAN, 1):
        own = lab == i
        ke = (lab == i - 1) | (lab == i + 1)
        d = cv2.distanceTransform((~own).astype(np.uint8), cv2.DIST_L2, 5)
        f = np.where(own, 1.0, np.where(ke, np.clip((chom - d) / mem, 0.0, 1.0), 0.0))
        A = rgba.copy()
        A[..., 3] = (A[..., 3] * f).astype(np.uint8)
        p = os.path.join(MANH, t + ".png")
        if os.path.exists(p) and not os.path.exists(os.path.join(cu, t + ".png")):
            os.replace(p, os.path.join(cu, t + ".png"))
        if t == "than_5":
            X5 = rgba.copy()
            X5[..., 3] = np.where(own, rgba[..., 3], 0).astype(np.uint8)
            Image.fromarray(X5, "RGBA").save(os.path.join(MAU, "_than_5_X.png"))      # phần của khúc đáy trên ảnh cả thân
            Image.fromarray(A, "RGBA").save(os.path.join(MAU, "_than_5_day.png"))     # + chờm sang vòng cuộn
        if t == "than_5" and os.path.exists(os.path.join(cu, t + ".png")) and not os.path.exists(os.path.join(TAI, "N_U.png")):
            # khúc đáy chui ra sau ngực: ảnh cả thân chỉ vẽ tới mép ngực, nên phần nấp sau ngực lấy từ bản gen riêng cũ (khuất ở
            # dáng nghỉ; không có thì ngực nhích lên là hở)
            O = np.asarray(Image.open(os.path.join(cu, t + ".png")).convert("RGBA"))
            them = (O[..., 3] > 127) & (lab == 2) & (A[..., 3] < 30)
            A[them] = O[them]
            print(f"  {t}: thêm {int(them.sum())} px nấp sau ngực từ bản gen riêng")
        Image.fromarray(A, "RGBA").save(p)
        g = os.path.join(MANH, "_goc", t + ".png")
        if os.path.exists(g):
            os.remove(g)                        # khop() không dời lại các khúc này (đã dời cả ảnh)
        print(f"  {t}: {int(own.sum())} px của khúc + chờm {int(((f > 0.5) & ~own).sum())} px sang khúc kề")


DUOI_J = [(839, 754), (927, 668), (935, 550), (939, 434), (1060, 470), (1165, 495), (1200, 345)]   # sống đuôi trên khung concept
DUOI_R = [78, 66, 56, 48, 40, 31, 23]                                                               # nửa bề dày tại từng khớp
DUOI_KHUC = [("than_5", 0, 1.0), ("than_6", 1.0, 3.45), ("vay_duoi", 3.45, 6.0)]                    # khúc theo vị trí dọc sống (chỉ số khớp)


def _doc_song(pts):
    """vị trí dọc sống đuôi (chỉ số khớp thực, 0..6) của từng điểm: chiếu lên đoạn gần nhất."""
    J = np.array(DUOI_J, float)
    best = np.full(len(pts), 1e9)
    u = np.zeros(len(pts))
    for i in range(len(J) - 1):
        a, b = J[i], J[i + 1]
        d = b - a
        t = np.clip(((pts - a) @ d) / (d @ d), 0, 1)
        dist = np.hypot(*(pts - (a + t[:, None] * d)).T)
        m = dist < best
        best[m] = dist[m]
        u[m] = i + t[m]
    return u, best


def nhom_duoi():
    """tờ hướng dẫn gen PHẦN ĐUÔI liền một ảnh (người dùng 2026-11-11: "phần đuôi đâu, nhìn hướng này ổn áp hơn đó"): khúc đáy lấy
    nguyên từ ảnh cả thân N_T (để khớp với vòng cuộn), mẩu đuôi lộ bên trái cổ và cuống + vây đuôi lấy từ concept; đoạn đuôi nấp sau
    ngực và sau cổ (nối ba thứ đó) tô hồng dọc sống đuôi → mau/nhom_U.png."""
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    muc = np.asarray(Image.open(os.path.join(MAU, "_muc.png"))) > 127
    e6 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    im = np.full((H, W, 3), 255, np.uint8)
    pink = np.zeros((H, W), np.uint8)
    J = np.array(DUOI_J, float)
    for i in range(len(J) - 1):
        n = int(np.hypot(*(J[i + 1] - J[i])) / 3) + 2
        for t in np.linspace(0, 1, n):
            p = J[i] + t * (J[i + 1] - J[i])
            cv2.circle(pink, (int(p[0]), int(p[1])), int(DUOI_R[i] + t * (DUOI_R[i + 1] - DUOI_R[i])), 1, -1)
    pink = pink.astype(bool)
    for t in ("vay_duoi", "than_6"):                       # phần khuất theo mặt nạ rig cũng tô hồng
        pink |= vung(t)[1]
    im[pink] = HONG
    x5 = np.asarray(Image.open(os.path.join(MAU, "_than_5_X.png")).convert("RGBA"))
    k5 = x5[..., 3] > 200
    # bỏ dải sát ngực: ở đó ảnh cả thân có nét viền của NGỰC vắt ngang khúc đáy, giữ lại thì thành một vạch cắt ngang đuôi
    nguc = np.asarray(Image.open(os.path.join(MAU, "_than_nhan.png"))) == 80
    k5 &= ~cv2.dilate(nguc.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (75, 75))).astype(bool)
    nn, lb_, st, _ = cv2.connectedComponentsWithStats(k5.astype(np.uint8), 8)
    if nn > 2:
        k5 = lb_ == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))
    im[k5] = x5[..., :3][k5]
    for t in ("than_6", "vay_duoi"):
        v = vung(t)[0]
        keep = v | (cv2.dilate(v.astype(np.uint8), e6).astype(bool) & muc)
        im[keep] = con[keep]
    Image.fromarray(im).save(os.path.join(MAU, "nhom_U.png"))
    print(os.path.join(MAU, "nhom_U.png"))


def cat_duoi(chom=34, mem=10):
    """cắt ảnh phần đuôi N_U: khúc đáy chỉ lấy thêm đoạn nấp sau ngực (phần lộ giữ bản cắt từ N_T), than_6 và vay_duoi (cuống + vây)
    cắt theo vị trí dọc sống đuôi, chờm `chom` px sang khúc kề."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, "N_U")
    if not path:
        print("U chưa có ảnh")
        return
    to = anh.doc_to(path, dien_tich_min=4000, gop_px=20)
    rgba = to.rgba.copy()
    al = np.isin(to.lab, [i for m in to.manh for i in m["ids"]])
    rgba[..., 3] = (rgba[..., 3] * anh.gian(al, 2)).astype(np.uint8)
    trang = (rgba[..., :3].min(axis=2) > 236) & (rgba[..., 3] > 127)
    nn, lb_, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), 8)
    for i in range(1, nn):
        if st[i, cv2.CC_STAT_AREA] > 400:
            rgba[..., 3][cv2.dilate((lb_ == i).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)] = 0
    al = rgba[..., 3] > 127
    ys, xs = np.nonzero(al)
    u, _ = _doc_song(np.stack([xs, ys], 1).astype(float))
    U = np.full((H, W), -1.0)
    U[ys, xs] = u
    # điểm thuộc vây đuôi (xa sống) vẫn chiếu về đoạn cuối: đúng ý
    cu = os.path.join(MANH, "_rieng")
    os.makedirs(cu, exist_ok=True)
    for t, u0, u1 in DUOI_KHUC:
        own = al & (U >= u0) & (U < u1 + (1e-6 if u1 < 6 else 1))
        d = cv2.distanceTransform((~own).astype(np.uint8), cv2.DIST_L2, 5)
        f = np.where(own, 1.0, np.where(al, np.clip((chom - d) / mem, 0.0, 1.0), 0.0))
        A = rgba.copy()
        A[..., 3] = (A[..., 3] * f).astype(np.uint8)
        p = os.path.join(MANH, t + ".png")
        if t == "than_5":
            B = np.asarray(Image.open(os.path.join(MAU, "_than_5_day.png")).convert("RGBA")).copy()   # bản cắt từ N_T (lộ + chờm vòng cuộn)
            them = (A[..., 3] > 30) & (B[..., 3] < 30)
            B[them] = A[them]
            Image.fromarray(B, "RGBA").save(p)
            print(f"  than_5: giữ bản N_T, thêm {int(them.sum())} px nấp sau ngực từ ảnh phần đuôi")
            continue
        if os.path.exists(p) and not os.path.exists(os.path.join(cu, t + ".png")):
            os.replace(p, os.path.join(cu, t + ".png"))
        Image.fromarray(A, "RGBA").save(p)
        print(f"  {t}: {int(own.sum())} px + chờm {int(((f > 0.5) & ~own).sum())} px")
    for t in ("than_6", "vay_duoi", "than_5"):
        g = os.path.join(MANH, "_goc", t + ".png")
        if os.path.exists(g):
            os.remove(g)
        r = os.path.join(MANH_RIG, t + ".png")
        if os.path.exists(r):
            os.remove(r)


# ---------------------------------------------------------------- mảnh vẽ ĐÚNG KHUNG part của con gốc (y hệt tỉ lệ, hướng)
# người dùng 2026-11-11: "sao không gen theo đó ghép lại rồi đổi pose là được", "gen theo y hệt đúng tỉ lệ luôn, đúng hướng".
# Các mảnh của mình lệch hình part của họ nhiều nhất (đuôi, vây đuôi, lớp sẫm của cánh, vây tai nhỏ còn thiếu) vẽ lại ngay trong khung
# ảnh của part đó: rig dùng nguyên lưới + uv của họ cho các mảnh này (rong_vay_rig.py, PART_GOC).
PART_TO = {"P1": [("P_chibangR08", "song"), ("P_weiba", "vay"), ("P_shenti06", "than"), ("P_chibangL05", "song"), ("P_yuqi02", "vay")]}
PART_Z = 2            # ảnh vùng atlas của họ phóng 2 lần trên tờ (= đúng cỡ thế giới của họ)
PART_MAU = {"than": (52, 64, 143), "bung": (243, 230, 196), "vay": (106, 155, 168), "song": (36, 44, 104)}


def part_goc():
    """ảnh từng part của con gốc, cắt đúng theo lưới (như scan/.../parts): {slot: RGBA cỡ vùng atlas}."""
    import rong_vay_bo_cuc as B
    sys.path.insert(0, os.path.join(HERE, "mo_xe"))
    import to_manh
    root = B.sxs()
    _, imgs = to_manh.nap(os.path.join(root, "web", "assets", "Monster", B.MON), B.MON)
    D = json.load(open(os.path.join(root, "scan", B.MON, "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in D["atts"]:
        if a.get("region") not in imgs or a["slot"] in out:
            continue
        im = imgs[a["region"]].convert("RGBA")
        uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
        m = Image.new("L", (im.width * 4, im.height * 4), 0)
        d = ImageDraw.Draw(m)
        for t in np.array(a["tris"]).reshape(-1, 3):
            d.polygon([tuple(uv[i] * 4) for i in t], fill=255, outline=255)
        A = np.asarray(im).copy()
        A[..., 3] = (A[..., 3].astype(np.float32) * np.asarray(m.resize(im.size, Image.LANCZOS)) / 255.0).astype(np.uint8)
        out[a["slot"]] = Image.fromarray(A, "RGBA")
    return out


def nhom_part(to="P1"):
    """tờ hướng dẫn: mỗi part là một HÌNH BÓNG PHẲNG đúng cỡ, đúng hướng như ảnh part của con gốc (không có nét vẽ, hoa văn, màu của
    họ: chỉ hình bóng làm trơn nhẹ, tô màu của mình), đặt trong ô riêng → mau/part_<tờ>.png + part_<tờ>.json (ô của từng part)."""
    P = part_goc()
    x, y, hh = 40, 60, 0
    im = np.full((H, W, 3), 255, np.uint8)
    khung = {}
    e = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    for slot, loai in PART_TO[to]:
        g = P[slot]
        w, h = g.width * PART_Z, g.height * PART_Z
        if x + w + 40 > W:
            x, y, hh = 40, y + hh + 60, 0
        a = np.asarray(g.resize((w, h), Image.LANCZOS))
        m = a[..., 3] > 100
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, e(4))
        m = cv2.GaussianBlur((cv2.morphologyEx(m, cv2.MORPH_OPEN, e(2)) * 255).astype(np.uint8), (0, 0), 2.0) > 127
        cell = im[y:y + h, x:x + w]
        cell[m] = PART_MAU[loai]
        if loai == "than":
            hsv = cv2.cvtColor(a[..., :3], cv2.COLOR_RGB2HSV)
            pale = cv2.medianBlur(((hsv[..., 2] > 150) & (hsv[..., 1] < 95) & (a[..., 3] > 100)).astype(np.uint8) * 255, 9) > 127
            cell[pale & m] = PART_MAU["bung"]
        cell[m & ~cv2.erode(m.astype(np.uint8), e(3)).astype(bool)] = (43, 33, 24)
        khung[slot] = [x, y, w, h]
        x += w + 50
        hh = max(hh, h)
    os.makedirs(MAU, exist_ok=True)
    Image.fromarray(im).save(os.path.join(MAU, f"part_{to}.png"))
    json.dump(khung, open(os.path.join(MAU, f"part_{to}.json"), "w", encoding="utf-8"), indent=1)
    print(os.path.join(MAU, f"part_{to}.png"), khung)


PART_CON = [("P_chibangR06", "canh_g_mang"), ("P_chibangL06", "canh_x_mang"), ("P_shenti01", "than_1"), ("P_shenti02", "than_2"),
            ("P_shenti03", "than_3"), ("P_shenti04", "than_4"), ("P_shenti05", "than_5"), ("P_tou", "dau"), ("P_erduo", "dau"),
            ("P_zuiba01", "mo_tren"), ("P_zuiba02", "mo_duoi"), ("P_yuqi03", "sung_t"), ("P_yuqi04", "sung_s"), ("P_yuqi05", "tai_lon"),
            ("P_yuqi01", "vay_ma")] + [(f"P_yuqi{i:02d}", f"vay_{i:02d}") for i in range(6, 17)]


def nhom_part_het(kieu="Q"):
    """tờ hướng dẫn cho MỌI part còn lại (P2, P3, ...): mỗi part một ô đúng khung ảnh vùng của nó (phóng 2 lần; part nhỏ phóng 4 lần),
    trong ô là hình bóng part; phần nào mảnh hiện có của mình (manh/, đã nằm đúng chỗ trên khung concept) phủ tới thì NƯỚNG hình đó
    vào (qua lưới của part: chỗ đứng ở dáng gốc → chỗ trong ảnh vùng). Hình mình thò ra ngoài hình bóng thì bị cắt.
    kieu "P" (bản đầu, 2026-11-11): phần còn thiếu tô hồng để GPT vẽ bù → GPT hay bỏ phần hồng, mảnh lệch hình bóng (IoU 0,66–0,87),
    lắp vào lưới thì thân khuyết. kieu "Q" (thay thế): phần thiếu TÔ SẴN bằng màu của chỗ gần nhất, nét mực cũ nằm sát chỗ thiếu bị
    xoá, rồi kẻ viền sẫm đúng mép hình bóng: tờ hướng dẫn là hình bóng KÍN như tờ P1 (P1 ra IoU 0,90–0,96)."""
    import rong_vay_bo_cuc as B
    from quai.soi import _tris
    P = part_goc()
    root = B.sxs()
    D = json.load(open(os.path.join(root, "scan", B.MON, "att_goc.json"), encoding="utf-8"))
    by = {a["slot"]: a for a in D["atts"]}
    atts = [a for a in D["atts"] if a["cur"] and a["type"].endswith("MeshAttachment")]
    Pq = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = Pq[:, 0].min(), Pq[:, 1].min(), Pq[:, 0].max(), Pq[:, 1].max()
    ox = (B.W - (x1 - x0) * B.SC) / 2 - x0 * B.SC
    oy = (B.H + (y1 - y0) * B.SC) / 2 + y0 * B.SC
    e = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    cells = []
    for slot, t in PART_CON:
        g = P[slot]
        z = 4 if max(g.size) * 2 < 280 else 2
        w, h = g.width * z, g.height * z
        a = np.asarray(g.resize((w, h), Image.LANCZOS))
        m = cv2.morphologyEx((a[..., 3] > 100).astype(np.uint8), cv2.MORPH_CLOSE, e(2 * z))
        m = cv2.GaussianBlur((cv2.morphologyEx(m, cv2.MORPH_OPEN, e(z)) * 255).astype(np.uint8), (0, 0), 1.0 * z) > 127
        pm = os.path.join(MANH_RIG, t + ".png")
        src = Image.open(pm if os.path.exists(pm) else os.path.join(MANH, t + ".png")).convert("RGBa")
        at = by[slot]
        uv = np.array(at["uv"], float).reshape(-1, 2) * np.array([w, h])
        xy = np.array(at["xy"], float).reshape(-1, 2)
        can = np.stack([xy[:, 0] * B.SC + ox, oy - xy[:, 1] * B.SC], 1)
        lay = Image.new("RGBa", (w, h), (0, 0, 0, 0))
        _tris(lay, src, uv, can, np.array(at["tris"]).reshape(-1, 3))
        bk = np.asarray(lay.convert("RGBA"))
        co = (bk[..., 3] > 200) & m
        cell = np.full((h, w, 3), 255, np.uint8)
        cell[m] = HONG
        cell[co] = bk[..., :3][co]
        if kieu == "Q":
            s_ = z // 2
            rgb = bk[..., :3]
            muc = co & (rgb.max(axis=2) < 105)
            gan = cv2.dilate((m & ~co).astype(np.uint8), e(11 * s_)).astype(bool)
            tot = co & ~muc & cv2.erode(co.astype(np.uint8), e(2 * s_)).astype(bool)      # màu tô thật, không phải mực hay mép
            giu = co & ~(muc & gan)                                                     # giữ nguyên (kể cả nét bên trong)
            phang = (38, 37, 44) if t.startswith(("sung", "mo_")) else (36, 44, 104) if slot == "P_erduo" else None
            if phang or tot.sum() < 50:                       # sừng, mỏ (đen: lẫn với mực) và mào: một màu phẳng
                cell[m] = phang or PART_MAU["vay"]
            else:
                _, lab = cv2.distanceTransformWithLabels((~tot).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                tra = np.zeros((int(lab.max()) + 1, 3), np.uint8)
                tra[lab[tot]] = rgb[tot]
                lap = tra[lab]
                lap = cv2.medianBlur(lap, 2 * (3 * s_) + 1)
                bu = m & ~giu
                cell[bu] = lap[bu]
            cell[m & ~cv2.erode(m.astype(np.uint8), e(3 * s_)).astype(bool)] = (43, 33, 24)
        cells.append((slot, t, z, w, h, cell, int(co.sum()), int(m.sum())))
    cells.sort(key=lambda c: -c[4])
    sheets, cur, x, y, hh = [], [], 40, 40, 0
    for c in cells:
        w, h = c[3], c[4]
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
    for k, sh in enumerate(sheets, 2):
        im = np.full((H, W, 3), 255, np.uint8)
        khung = {}
        to = f"{kieu}{k}"
        for (slot, t, z, w, h, cell, nco, nm), x, y in sh:
            im[y:y + h, x:x + w] = cell
            khung[slot] = {"x": x, "y": y, "w": w, "h": h, "z": z, "ten": t, "co": nco, "bong": nm}
        Image.fromarray(im).save(os.path.join(MAU, f"part_{to}.png"))
        json.dump(khung, open(os.path.join(MAU, f"part_{to}.json"), "w", encoding="utf-8"), indent=1)
        print(f"{to}:", ", ".join(f"{s}({v['ten']}, x{v['z']}, có {100 * v['co'] // max(1, v['bong'])}%)" for s, v in khung.items()))
    print(len(sheets), "tờ")


def cat_part(to="P1", ep=False):
    """cắt tờ N_<tờ>: mỗi part lấy đúng Ô của nó trên tờ (GPT vẽ đúng chỗ, đúng cỡ nên ô đó chính là khung ảnh vùng của part), tách nền
    trắng → manh/part/<slot>.png cỡ = ảnh vùng atlas của họ × PART_Z (rig tự co)."""
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
    import rong_vay_bo_cuc as B
    HULL = {x["slot"]: (np.array(x["uv"], float).reshape(-1, 2)[:x["hull"]]) for x in
            json.load(open(os.path.join(B.sxs(), "scan", B.MON, "att_goc.json"), encoding="utf-8"))["atts"] if x.get("hull")}
    pso = os.path.join(ra, "_iou.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    for slot, kv in khung.items():
        x, y, w, h = (kv["x"], kv["y"], kv["w"], kv["h"]) if isinstance(kv, dict) else kv
        z = kv["z"] if isinstance(kv, dict) else PART_Z
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
        # GPT hay vẽ thừa ra ngoài hình bóng (búi lông, mép phình): lưới của rig sẽ vẽ cả phần thừa đó → cắt sát hình bóng (nới 3 px)
        sat = cv2.dilate(g.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * 3 * z // 2 + 1,) * 2)).astype(bool)
        cell[..., 3][~sat] = 0
        a &= sat
        cu = SO.get(slot, [0, ""])
        if not ep and cu[1] != to and cu[0] >= iou:
            print(f"  {slot}: IoU {iou:.2f}, giữ bản {cu[1]} (IoU {cu[0]:.2f})")
            continue
        ho = g & ~a
        if to.startswith("Q") and ho.any():
            # tờ Q là hình bóng kín: chỗ GPT vẽ hụt lấy màu của tờ hướng dẫn (bỏ viền máy kẻ: lấy màu tô gần nhất) cho khỏi khuyết
            gc = gd[y:y + h, x:x + w]
            to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105) & (gc.min(axis=2) < 215)
            if to_.any():
                _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                tra[lb[to_]] = gc[to_]
                cell[ho, :3] = tra[lb][ho]
                cell[ho, 3] = 255
        a = cell[..., 3] > 127
        if isinstance(kv, dict) and kv["ten"].startswith("than"):
            # khúc thân: GPT tô nâu xám các gai nhỏ ở mép (chỗ tờ hướng dẫn bị nhoè) → bỏ các mảng nâu xám đó (thân chỉ có chàm, kem, vỏ sò)
            hsv = cv2.cvtColor(cell[..., :3], cv2.COLOR_RGB2HSV)
            bun = a & (hsv[..., 0] >= 4) & (hsv[..., 0] <= 32) & (hsv[..., 2] > 95) & (hsv[..., 2] < 205)
            bun = cv2.morphologyEx(bun.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
            if bun.sum() > 60:
                k9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
                giu_ = cv2.morphologyEx((a & ~cv2.dilate(bun.astype(np.uint8), k9).astype(bool)).astype(np.uint8), cv2.MORPH_OPEN, k9).astype(bool)
                giu_ = cv2.dilate(giu_.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & a
                bo_ = a & ~giu_
                cell[..., 3][~giu_] = 0
                a = giu_
                # mép vừa gọt mất luôn nét viền: kẻ lại nét mực dọc đoạn mép đó
                k7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
                vien = a & ~cv2.erode(a.astype(np.uint8), k7).astype(bool) & cv2.dilate(bo_.astype(np.uint8), k9).astype(bool)
                cell[vien, :3] = (43, 33, 24)
        if isinstance(kv, dict) and kv["ten"].startswith("than"):
            # thân không có màu trắng: mảng trắng giấy lọt trong mảnh (GPT vẽ hụt mép khung) lấy màu tô gần nhất
            trang = a & (cell[..., :3].min(axis=2) > 228)
            okm = a & ~trang & (cell[..., :3].max(axis=2) > 105)
            if trang.any() and okm.any():
                _, lb = cv2.distanceTransformWithLabels((~okm).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                tra[lb[okm]] = cell[..., :3][okm]
                cell[trang, :3] = tra[lb][trang]
        if slot in HULL:
            # lưới của rig ôm sát hình bóng, nét viền của mình dày hơn của họ nên chỗ lưới xén vào thì mất viền (mép thẳng trơ màu):
            # kẻ nét mực dọc phía trong mép lưới ở mọi chỗ có hình
            hm = np.zeros(a.shape, np.uint8)
            cv2.fillPoly(hm, [np.round(HULL[slot] * np.array([w, h])).astype(np.int32)], 1)
            q = 5 * z // 2
            dai = hm.astype(bool) & ~cv2.erode(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * q + 1, 2 * q + 1)), borderValue=0).astype(bool)
            cell[dai & (cell[..., 3] > 127), :3] = (43, 33, 24)
        if slot == "P_weiba" or slot.startswith("P_yuqi"):
            # vây vẽ phình chạm mép khung ảnh vùng thì bị xén thẳng, mất viền: kẻ lại nét mực dọc đoạn mép đó
            bien = np.zeros(a.shape, bool)
            q = 3 * z // 2
            bien[:q], bien[-q:], bien[:, :q], bien[:, -q:] = True, True, True, True
            kin = cell[..., 3] > 127
            cell[bien & kin, :3] = (43, 33, 24)
        SO[slot] = [round(float(iou), 3), to]
        out = Image.fromarray(cell, "RGBA")
        if z != PART_Z:
            out = out.convert("RGBa").resize((w * PART_Z // z, h * PART_Z // z), Image.LANCZOS).convert("RGBA")
        out.save(os.path.join(ra, slot + ".png"))
        print(f"  {slot}: {w} x {h} (x{z}), trùng hình bóng hướng dẫn IoU {iou:.2f}" + (f", bù {int(ho.sum())} px" if to.startswith("Q") else ""))
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)


# các khúc thân kề nhau trên rig (slot của con gốc), theo thứ tự dọc thân; P_shenti07 dùng lại ảnh P_shenti06
NOI_PART = [("P_shenti01", "P_shenti02"), ("P_shenti02", "P_shenti03"), ("P_shenti03", "P_shenti04"), ("P_shenti04", "P_shenti05"),
            ("P_shenti05", "P_shenti06"), ("P_shenti06", "P_shenti07")]
NOI_ANH = {"P_shenti07": "P_shenti06"}


def noi_part(r=5, vanh=9):
    """Người dùng: "bỏ outline những khúc nối nhau đi cho liền mạch". Mảnh vẽ đúng khung part có viền mực kín, nên ở chỗ hai khúc thân
    KỀ NHAU chồng lên nhau, đầu khúc nằm trên in một vạch mực cắt ngang thân. Ở dáng gốc: nét mực trên vành mép của một khúc mà rơi
    SÂU trong khúc kề (cách mép khúc kề hơn r đơn vị) là vạch nối → thay bằng màu tô gần nhất. Nét viền chạy dọc hai bên thân (nằm
    trên mép của cả hai khúc) giữ nguyên. Ra manh/part_noi/<slot>.png (rig ưu tiên dùng)."""
    import rong_vay_bo_cuc as B
    from quai.soi import _tris
    root = B.sxs()
    D = json.load(open(os.path.join(root, "scan", B.MON, "att_goc.json"), encoding="utf-8"))
    by = {a["slot"]: a for a in D["atts"]}
    slots = sorted({x for c in NOI_PART for x in c})
    src_dir, ra = os.path.join(MANH, "part"), os.path.join(MANH, "part_noi")
    os.makedirs(ra, exist_ok=True)
    A = {}
    for sl in slots:
        pth = os.path.join(src_dir, NOI_ANH.get(sl, sl) + ".png")
        if not os.path.exists(pth):
            print("  thiếu", pth)
            return
        im = Image.open(pth).convert("RGBA")
        at = by[sl]
        A[sl] = (im, np.array(at["uv"], float).reshape(-1, 2) * np.array(im.size), np.array(at["xy"], float).reshape(-1, 2),
                 np.array(at["tris"]).reshape(-1, 3))
    P = np.concatenate([v[2] for v in A.values()])
    x0, y1 = P[:, 0].min() - 20, P[:, 1].max() + 20
    cw, ch = int(P[:, 0].max() - x0 + 20), int(y1 - P[:, 1].min() + 20)
    can = lambda xy: np.stack([xy[:, 0] - x0, y1 - xy[:, 1]], 1)          # noqa: E731  thế giới của họ → pixel (1 px = 1 đơn vị)
    e = lambda q: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * q + 1, 2 * q + 1))  # noqa: E731
    phu = {}
    for sl, (im, uv, xy, tris) in A.items():
        lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), can(xy), uv, tris)
        phu[sl] = np.asarray(lay)[..., 3] > 127
    for sl, (im, uv, xy, tris) in A.items():
        ke = [b if a == sl else a for a, b in NOI_PART if sl in (a, b)]
        J = np.zeros((ch, cw), bool)
        for t in ke:
            J |= cv2.erode(phu[t].astype(np.uint8), e(r)).astype(bool)
        jim = Image.fromarray(np.dstack([J * 255] * 4).astype(np.uint8), "RGBa")
        lay = Image.new("RGBa", im.size, (0, 0, 0, 0))
        _tris(lay, jim, uv, can(xy), tris)
        Jt = np.asarray(lay)[..., 3] > 127
        a = np.asarray(im).copy()
        al = a[..., 3] > 127
        rgb = a[..., :3]
        muc = al & (rgb.max(axis=2) < 105)
        vm = al & ~cv2.erode(al.astype(np.uint8), e(vanh)).astype(bool)
        bo = cv2.dilate((vm & muc & Jt).astype(np.uint8), e(2)).astype(bool) & al & Jt & vm
        tot = (cv2.erode(al.astype(np.uint8), e(3)).astype(bool) & ~cv2.dilate(muc.astype(np.uint8), e(4)).astype(bool)
               & (rgb.min(axis=2) < 215))
        # mẩu mực vụn còn sót sát chỗ vừa xoá (đầu nét cụt, không dính vào nét nào khác): xoá nốt
        nc, lab_, st, _ = cv2.connectedComponentsWithStats((muc & ~bo).astype(np.uint8), connectivity=8)
        gan_bo = cv2.dilate(bo.astype(np.uint8), e(6)).astype(bool)
        for i in range(1, nc):
            if st[i, cv2.CC_STAT_AREA] < 450 and (gan_bo & (lab_ == i)).any():
                bo |= lab_ == i
        bo = cv2.dilate(bo.astype(np.uint8), e(1)).astype(bool) & al
        # viền trắng giấy ở mép cắt không có mực (đầu khúc): lấy màu tô gần nhất
        bo |= al & (rgb.min(axis=2) > 218) & ~cv2.erode(al.astype(np.uint8), e(12)).astype(bool)
        if bo.any() and tot.any():
            _, lb = cv2.distanceTransformWithLabels((~tot).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
            tra[lb[tot]] = rgb[tot]
            lap = cv2.medianBlur(tra[lb], 7)
            rgb[bo] = lap[bo]
        Image.fromarray(a, "RGBA").save(os.path.join(ra, sl + ".png"))
        print(f"  {sl}: kề {', '.join(ke)}; xoá {int(bo.sum())} px mực ở chỗ nối")



def so_part(*tos):
    """tờ so từng part đã cắt (manh/part) với hình bóng trên tờ hướng dẫn: ĐỎ = hình bóng mà mảnh không phủ (lắp vào lưới sẽ khuyết),
    XANH LÁ = mảnh vẽ thừa ra ngoài hình bóng. Xem tờ này trước khi lắp rig → mau/so_part.png."""
    tos = tos or sorted({os.path.basename(f)[5:-5] for f in os.listdir(MAU) if f.startswith("part_") and f.endswith(".json")})
    cells = []
    for to in tos:
        K = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        for slot, v in K.items():
            x, y, w, h = v if isinstance(v, list) else (v["x"], v["y"], v["w"], v["h"])
            pm = os.path.join(MANH, "part", slot + ".png")
            if not os.path.exists(pm):
                continue
            g = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a = c[..., 3] > 127
            im = np.full((h, w, 3), 255, np.uint8)
            im[a] = c[..., :3][a]
            im[g & ~a] = (255, 0, 0)
            im[a & ~g] = (im[a & ~g] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
            cv2.putText(im, f"{to} {slot}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cells.append(im)
    Wd, x, y, hh, pos = 1800, 0, 0, 0, []
    for im in cells:
        h, w = im.shape[:2]
        if x + w > Wd:
            x, y, hh = 0, y + hh + 10, 0
        pos.append((x, y))
        x += w + 10
        hh = max(hh, h)
    S = np.full((y + hh, Wd, 3), 230, np.uint8)
    for im, (x, y) in zip(cells, pos):
        S[y:y + im.shape[0], x:x + min(im.shape[1], Wd - x)] = im[:, :Wd - x]
    Image.fromarray(S).save(os.path.join(MAU, "so_part.png"))
    print(os.path.join(MAU, "so_part.png"), len(cells), "part")


def cat(chi=None):
    """cắt ảnh nhóm N_<X>.png (bản mới nhất) thành mảnh: tách nền trắng, gán cụm cho mảnh theo mặt nạ hướng dẫn, lưu cả khung."""
    from quai import anh
    G = json.load(open(os.path.join(MAU, "nhom.json"), encoding="utf-8"))
    os.makedirs(MANH, exist_ok=True)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * KE + 1, 2 * KE + 1))
    for X, parts in G.items():
        if chi and X not in chi:
            continue
        path = anh.to_moi_nhat(TAI, f"N_{X}")
        if not path:
            print(X, "chưa có ảnh")
            continue
        im = Image.open(path).convert("RGB")
        if im.size != (W, H):
            print(X, "cỡ ảnh", im.size, "→ đổi về", (W, H))
            im = im.resize((W, H), Image.LANCZOS)
            path = os.path.join(MAU, f"_N_{X}_doi_co.png")
            im.save(path)
        to = anh.doc_to(path, dien_tich_min=120, gop_px=14)
        gm = {q["ten"]: cv2.dilate((np.asarray(Image.open(os.path.join(MAU, "day", q["ten"] + ".png"))) > 127).astype(np.uint8),
                                   k).astype(bool) for q in parts}
        got = {}
        for m in to.manh:
            comp = np.isin(to.lab, m["ids"])
            ov = {t: int((comp & g).sum()) for t, g in gm.items()}
            t = max(ov, key=ov.get)
            if ov[t] == 0:
                print(f"  {X}: cụm {m['dt']} px ở ({m['x0']},{m['y0']}) không thuộc mảnh nào → bỏ")
                continue
            got.setdefault(t, []).append((ov[t] / m["dt"], m, comp))
        line = []
        for q in parts:
            t = q["ten"]
            if t not in got:
                line.append(f"{t}: THIẾU")
                continue
            comp = np.zeros((H, W), bool)
            for _, m, c in got[t]:
                comp |= c
            rgba = to.rgba.copy()
            rgba[..., 3] = (rgba[..., 3] * anh.gian(comp, 2)).astype(np.uint8)
            Image.fromarray(rgba, "RGBA").save(os.path.join(MANH, t + ".png"))
            g0 = np.asarray(Image.open(os.path.join(MAU, "day", t + ".png"))) > 127
            iou = (comp & g0).sum() / max(1, (comp | g0).sum())
            line.append(f"{t}: {len(got[t])} cụm, {int(comp.sum())} px, IoU hướng dẫn {iou:.2f}")
        print(X, os.path.basename(path), "|", "; ".join(line))


def khop(chi=None):
    """chỉnh chỗ từng mảnh cho trùng concept (GPT hay xê dịch vài chục px): dời cả mảnh sao cho phần lộ khớp màu với concept nhất;
    mảnh khuất hẳn (không có phần lộ) thì co + dời cả mảnh cho vừa vùng khuất. Bản trước khi chỉnh giữ ở manh/_goc/."""
    G = json.load(open(os.path.join(MAU, "nhom.json"), encoding="utf-8"))
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    con_s = cv2.GaussianBlur(cv2.resize(con, (W // 2, H // 2), interpolation=cv2.INTER_AREA), (0, 0), 1.5).astype(np.float32)
    goc = os.path.join(MANH, "_goc")
    os.makedirs(goc, exist_ok=True)
    R = 15                                        # ±30 px ở cỡ thật
    for X, parts in G.items():
        if chi and X not in chi:
            continue
        for q in parts:
            t = q["ten"]
            p = os.path.join(MANH, t + ".png")
            if not os.path.exists(p):
                continue
            g = os.path.join(goc, t + ".png")
            if not os.path.exists(g) or os.path.getmtime(p) > os.path.getmtime(g):
                Image.open(p).save(g)
            im = np.asarray(Image.open(g).convert("RGBA"))
            V, K = vung(t)
            a = im[..., 3] > 127
            if V.sum() < 400:                     # mảnh khuất hẳn: co cho vừa vùng khuất
                ys, xs = np.nonzero(a)
                ky, kx = np.nonzero(K)
                sc = min(1.0, 1.08 * np.sqrt(K.sum() / max(1, a.sum())))
                bb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
                cut = Image.fromarray(im, "RGBA").crop(bb)
                w, h = max(1, int(cut.width * sc)), max(1, int(cut.height * sc))
                cut = cut.resize((w, h), Image.LANCZOS)
                fgc = hinh(con)
                cut0 = Image.fromarray(im, "RGBA").crop(bb)
                best = None
                for f in (1.0, 0.9, 0.8, 0.7):          # dáng nghỉ không được thò ra ngoài hình: thử co thêm, dời quanh tâm vùng khuất
                    w, h = max(1, int(cut0.width * sc * f)), max(1, int(cut0.height * sc * f))
                    c2 = cut0.resize((w, h), Image.LANCZOS)
                    a2 = np.asarray(c2)[..., 3] > 127
                    for dy in range(-24, 25, 4):
                        for dx in range(-24, 25, 4):
                            x, y = int(kx.mean() - w / 2) + dx, int(ky.mean() - h / 2) + dy
                            if x < 0 or y < 0 or x + w > W or y + h > H:
                                continue
                            lo = int((a2 & ~fgc[y:y + h, x:x + w]).sum())
                            key = (lo > 40, lo if lo > 40 else 0, -f, abs(dx) + abs(dy))
                            if best is None or key < best[0]:
                                best = (key, c2, x, y, f, lo)
                _, c2, x, y, f, lo = best
                out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                out.paste(c2, (x, y))
                out.save(p)
                print(f"  {t}: khuất hẳn, co {sc * f:.2f} lần, thò ra ngoài hình {lo} px")
                continue
            ims = cv2.resize(im, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
            rgb = cv2.GaussianBlur(ims[..., :3], (0, 0), 1.5).astype(np.float32)
            al = ims[..., 3] > 127
            Vs = cv2.resize(V.astype(np.uint8), (W // 2, H // 2), interpolation=cv2.INTER_NEAREST).astype(bool)
            ys, xs = np.nonzero(Vs)
            y0, y1, x0, x1 = max(R, ys.min()), min(H // 2 - R, ys.max() + 1), max(R, xs.min()), min(W // 2 - R, xs.max() + 1)
            vv = Vs[y0:y1, x0:x1]
            cc = con_s[y0:y1, x0:x1]
            best = None
            for dy in range(-R, R + 1):
                for dx in range(-R, R + 1):
                    pr = rgb[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
                    pa = al[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
                    e = np.minimum(1.0, np.abs(pr - cc).sum(axis=2) / 255.0)
                    e[~pa] = 1.0
                    sco = float(e[vv].mean())
                    if best is None or sco < best[0] - 1e-6 or (abs(sco - best[0]) <= 1e-6 and abs(dx) + abs(dy) < abs(best[1]) + abs(best[2])):
                        best = (sco, dx, dy)
                    if dx == 0 and dy == 0:
                        zero = sco
            sco, dx, dy = best
            if zero - sco < 0.01:
                dx = dy = 0
            out = np.zeros_like(im)
            DX, DY = 2 * dx, 2 * dy
            ys0, ys1 = max(0, DY), min(H, H + DY)
            xs0, xs1 = max(0, DX), min(W, W + DX)
            out[ys0:ys1, xs0:xs1] = im[ys0 - DY:ys1 - DY, xs0 - DX:xs1 - DX]
            Image.fromarray(out, "RGBA").save(p)
            print(f"  {t}: dời ({DX:+d}, {DY:+d}) px, lệch màu phần lộ {zero:.3f} → {sco if (dx or dy) else zero:.3f}")


def cat_mo():
    """tờ phóng to N_M (mỏ trên, mỏ dưới, mí mắt nhắm, trái → phải): thu về cỡ concept, dò tỉ lệ và chỗ đặt theo khối mỏ và con mắt
    của concept (GPT không giữ đúng tỉ lệ 6 lần)."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, "N_M")
    if not path:
        print("M chưa có ảnh")
        return
    to = anh.doc_to(path, dien_tich_min=2000, gop_px=10)
    ms = sorted(sorted(to.manh, key=lambda m: -m["dt"])[:3], key=lambda m: m["x0"])
    if len(ms) != 3:
        raise SystemExit(f"tờ M có {len(ms)} mảnh, cần 3")
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB")).astype(int)
    fg = hinh(con.astype(np.uint8))
    blob = np.asarray(Image.open(os.path.join(MAU, "thay", "mo_tren.png"))) > 127
    ys, xs = np.nonzero(blob)
    bx0, by0, bx1, by1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    # đường miệng xám trong khối mỏ → nửa trên / nửa dưới
    sang = con.sum(axis=2) / 3
    line = blob & (sang > 62) & (cv2.erode(blob.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0)
    up = np.zeros_like(blob)
    dn = np.zeros_like(blob)
    last = None
    for x in range(bx1 - 1, bx0 - 1, -1):
        col = np.nonzero(line[:, x])[0]
        if len(col):
            last = int(np.median(col))
        if last is None:
            up[:, x] = blob[:, x]
        else:
            up[:last, x] = blob[:last, x]
            dn[last:, x] = blob[last:, x]
    print(f"khối mỏ {bx1 - bx0} x {by1 - by0} px tại ({bx0},{by0}); nửa trên {int(up.sum())} px, nửa dưới {int(dn.sum())} px")
    # con mắt: vùng vàng hổ phách trên đầu
    r, g, b = con[..., 0], con[..., 1], con[..., 2]
    eye = (r > 200) & (g > 120) & (g < 215) & (b < 130)
    eye[:, :1000] = False
    eye[300:, :] = False
    eye = cv2.dilate(eye.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))).astype(bool)   # gồm con ngươi, viền
    ys, xs = np.nonzero(eye)
    ex0, ey0, ex1, ey1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    bg = ~fg

    def manh_rgba(m):
        im = anh.cat_manh(to, m, pad=6)
        return im.crop(im.getbbox())

    def dat(im, sc, x, y):
        w, h = max(1, int(round(im.width * sc))), max(1, int(round(im.height * sc)))
        s = im.resize((w, h), Image.LANCZOS)
        full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        full.paste(s, (int(x), int(y)))
        return full

    def do(im, diem, x_ref, y_ref, duoi):
        """dò tỉ lệ + chỗ quanh mốc: mép phải của mảnh ở x_ref; mép trên (hoặc mép dưới nếu duoi) ở y_ref."""
        best = None
        for sc in np.linspace(1 / 9, 1 / 3.5, 34):
            w, h = max(1, int(round(im.width * sc))), max(1, int(round(im.height * sc)))
            a = np.asarray(im.resize((w, h), Image.LANCZOS))[..., 3] > 127
            for dx in range(-14, 15, 2):
                for dy in range(-14, 15, 2):
                    x = x_ref - w + dx
                    y = y_ref - h + dy if duoi else y_ref + dy
                    if x < 0 or y < 0 or x + w > W or y + h > H:
                        continue
                    sco = diem(a, x, y, w, h)
                    if best is None or sco > best[0]:
                        best = (sco, sc, x, y)
        return best

    def diem_tren(a, x, y, w, h):
        return ((a & up[y:y + h, x:x + w]).sum() / max(1, up.sum()) - 1.0 * (a & dn[y:y + h, x:x + w]).sum() / max(1, dn.sum())
                - 2.0 * (a & bg[y:y + h, x:x + w]).sum() / a.sum())

    def diem_duoi(a, x, y, w, h):
        return (a & dn[y:y + h, x:x + w]).sum() / max(1, dn.sum()) - 2.0 * (a & bg[y:y + h, x:x + w]).sum() / a.sum()

    os.makedirs(MANH, exist_ok=True)
    i_t, i_d, i_m = (manh_rgba(m) for m in ms)
    s1 = do(i_t, diem_tren, bx1, by0, False)
    os.makedirs(os.path.join(MANH, "_goc"), exist_ok=True)
    dat(i_t, s1[1], s1[2], s1[3]).save(os.path.join(MANH, "_goc", "mo_tren_gpt.png"))       # bản GPT (gốc mỏ kéo dài) để dành
    # mỏ trên nằm trên cùng, không có phần khuất: lấy thẳng nửa khối mỏ phía trên đường miệng của concept (dáng nghỉ y như concept)
    tren = up | (cv2.dilate(up.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & blob & ~cv2.erode(dn.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool))
    rg = np.dstack([con.astype(np.uint8), (cv2.GaussianBlur(tren.astype(np.float32), (0, 0), 0.8) * 255).clip(0, 255).astype(np.uint8)])
    Image.fromarray(rg, "RGBA").save(os.path.join(MANH, "mo_tren.png"))
    s2 = do(i_d, diem_duoi, bx1, by1, True)
    dat(i_d, s2[1], s2[2], s2[3]).save(os.path.join(MANH, "mo_duoi.png"))
    sc = (ex1 - ex0) / i_m.width
    cx, cy = (ex0 + ex1) / 2, (ey0 + ey1) / 2
    dat(i_m, sc, cx - i_m.width * sc / 2, cy - i_m.height * sc / 2).save(os.path.join(MANH, "mat_nham.png"))
    print(f"mo_tren: tỉ lệ 1/{1 / s1[1]:.1f}, điểm {s1[0]:.2f}; mo_duoi: tỉ lệ 1/{1 / s2[1]:.1f}, điểm {s2[0]:.2f}; "
          f"mat_nham: tỉ lệ 1/{1 / sc:.1f}, mắt {ex1 - ex0} x {ey1 - ey0} px tại ({ex0},{ey0})")


def cat_s():
    """tờ N_S: dải cạnh cánh (một mảnh nằm ngang, vai bên trái, mút nhọn bên phải) → manh/canh_canh.png (cắt sát, không đặt chỗ:
    rig tự đặt dọc sống cánh)."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, "N_S")
    if not path:
        print("S chưa có ảnh")
        return
    to = anh.doc_to(path, dien_tich_min=1500, gop_px=10)
    m = max(to.manh, key=lambda m: m["dt"])
    im = anh.cat_manh(to, m, pad=6)
    im = im.crop(im.getbbox())
    os.makedirs(MANH, exist_ok=True)
    im.save(os.path.join(MANH, "canh_canh.png"))
    print(f"S {os.path.basename(path)} | canh_canh: {im.width} x {im.height} px ({len(to.manh)} cụm trên tờ)")


def thu_tu():
    """thứ tự vẽ sau → trước: theo slot con gốc; mỏ dưới, mỏ trên ngay trên đầu (như con gốc), mí mắt nhắm không ghép (ẩn mặc định)."""
    G = json.load(open(os.path.join(MAU, "nhom.json"), encoding="utf-8"))
    L = sorted([(q["order"], q["ten"]) for g in G.values() for q in g])
    d = [o for o, t in L if t == "dau"][0]
    return sorted(L + [(d + 0.3, "mo_duoi"), (d + 0.4, "mo_tren")])


MANH_RIG = os.path.join(BASE, "manh_rig")
NOI = [("dau", "than_1")]      # năm khúc thân cắt từ một ảnh cả thân (cat_than) nên không cần làm liền; chỉ còn đầu đè lên cổ


def noi():
    """làm liền các khúc thân chỗ nối nhau (người dùng 2026-11-11: "bỏ outline những khúc nối nhau đi cho liền mạch"). Mảnh GPT là hình
    kín có viền mực quanh cả đầu khúc; khúc vẽ trên đè đầu khúc có viền lên khúc dưới nên thân trông đứt đoạn. Với mỗi cặp khúc kề:
    (1) xoá nét mực ở đầu khúc (nét nằm trong phần khuất của mảnh, lọt sâu trong lòng khúc kia, sát mép mảnh): tô bằng màu thịt gần
    nhất của chính mảnh; viền hai bên sườn giữ nguyên; (2) khúc vẽ TRÊN: phần vẽ bù chờm sang khúc dưới chỉ giữ ~14 px rồi mờ dần,
    để dáng nghỉ lộ đúng hình concept của khúc dưới (chờm 18 px đặc, mờ tới 30 px). Ra manh_rig/<tên>.png (rig đọc ở đây); manh/ giữ nguyên bản GPT."""
    os.makedirs(MANH_RIG, exist_ok=True)
    od = dict((t, o) for o, t in thu_tu())
    names = [t for _, t in thu_tu()] + ["mat_nham"]
    im = {t: np.asarray(Image.open(os.path.join(MANH, t + ".png")).convert("RGBA")).copy() for t in names
          if os.path.exists(os.path.join(MANH, t + ".png"))}
    e = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    al0 = {t: a[..., 3] > 127 for t, a in im.items()}
    V = {}
    for a, b in NOI:
        for t in (a, b):
            if t not in V:
                V[t] = vung(t)[0]

    def xoa_muc(t, n):
        A = im[t]
        rgb = A[..., :3].astype(int)
        al = al0[t]
        muc = al & (rgb.max(axis=2) < 112) & (rgb[..., 2] - rgb[..., 0] < 25)
        khuat = ~cv2.dilate(V[t].astype(np.uint8), e(4)).astype(bool)
        sau = cv2.erode(al0[n].astype(np.uint8), e(8)).astype(bool)
        mep = al & ~cv2.erode(al.astype(np.uint8), e(11)).astype(bool)
        rm = muc & khuat & sau & mep
        if not rm.any():
            return 0
        rm = cv2.dilate(rm.astype(np.uint8), e(2)).astype(bool) & al & khuat & sau      # lấy cả rìa nét mực mờ
        thit = al & ~muc & ~rm & (cv2.erode(al.astype(np.uint8), e(3)) > 0)
        _, lb = cv2.distanceTransformWithLabels((~thit).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        lut = np.zeros((lb.max() + 1, 3), np.uint8)
        lut[lb[thit]] = A[..., :3][thit]
        A[..., :3][rm] = lut[lb[rm]]
        return int(rm.sum())

    def cat_chom(hi, lo):
        A = im[hi]
        al = al0[hi]
        khuat = ~cv2.dilate(V[hi].astype(np.uint8), e(3)).astype(bool)
        Z = al & khuat & cv2.erode(al0[lo].astype(np.uint8), e(2)).astype(bool)
        if not Z.any():
            return 0
        giu = al & ~Z
        d = cv2.distanceTransform((~giu).astype(np.uint8), cv2.DIST_L2, 5)
        f = np.clip(1.0 - (d - 18.0) / 12.0, 0.0, 1.0)          # chờm 18 px đặc rồi mờ dần tới 30 px
        # phần chờm còn lại lấy luôn màu của khúc dưới ở đúng chỗ đó: hai mảnh GPT vẽ bù mỗi cái một kiểu (khúc trên vẽ vạch kem
        # quấn quanh đầu khúc, khúc dưới để chàm) nên để nguyên thì chỗ mờ dần lộ vệt kem nhạt khi cánh nhấc lên
        cung = Z & (im[lo][..., 3] > 200)
        A[..., :3][cung] = im[lo][..., :3][cung]
        a2 = A[..., 3].astype(np.float32)
        a2[Z] *= f[Z]
        A[..., 3] = a2.astype(np.uint8)
        return int((Z & (f < 0.5)).sum())

    for a, b in NOI:
        if a not in im or b not in im:
            continue
        hi, lo = (a, b) if od[a] > od[b] else (b, a)
        r1, r2 = xoa_muc(a, b), xoa_muc(b, a)
        c = cat_chom(hi, lo)
        print(f"  {a} – {b}: xoá nét mực đầu khúc {r1} + {r2} px; {hi} vẽ trên, bớt phần chờm {c} px")
    for t, A in im.items():
        Image.fromarray(A, "RGBA").save(os.path.join(MANH_RIG, t + ".png"))
    print(MANH_RIG)


def ghep():
    """xếp mọi mảnh theo thứ tự vẽ, so với concept: IoU hình bóng, số px concept có mà ghép bị trống, tờ so sánh, tờ từng mảnh."""
    from quai import anh
    os.makedirs(os.path.join(BASE, "rig"), exist_ok=True)
    out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    alpha = np.zeros((H, W), bool)
    co_manh = []
    for _, t in thu_tu():
        p = os.path.join(MANH, t + ".png")
        if not os.path.exists(p):
            print("thiếu mảnh", t)
            continue
        im = Image.open(p).convert("RGBA")
        out.alpha_composite(im)
        alpha |= np.asarray(im)[..., 3] > 127
        co_manh.append((t, im))
    out.convert("RGB").save(os.path.join(BASE, "rig", "ghep.png"))
    con = np.asarray(Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB"))
    fg = hinh(con)
    iou = (fg & alpha).sum() / max(1, (fg | alpha).sum())
    print(f"{len(co_manh)} mảnh; IoU hình bóng với concept {iou:.3f}; concept có mà ghép trống {int((fg & ~alpha).sum())} px; "
          f"ghép thừa ra ngoài concept {int((alpha & ~fg).sum())} px")
    g = np.asarray(out.convert("RGB")).astype(int)
    diff = np.abs(g - con.astype(int)).sum(axis=2)
    vis = np.full((H, W, 3), 255, np.uint8)
    vis[fg & alpha] = (205, 205, 205)
    vis[(diff > 150) & fg & alpha] = (120, 120, 120)
    vis[fg & ~alpha] = (230, 40, 40)
    vis[alpha & ~fg] = (40, 90, 230)
    tam = Image.new("RGB", (W * 3, H), "white")
    tam.paste(Image.fromarray(con), (0, 0))
    tam.paste(out.convert("RGB"), (W, 0))
    tam.paste(Image.fromarray(vis), (W * 2, 0))
    tam.save(os.path.join(BASE, "rig", "so_concept.png"))
    # tờ từng mảnh trên nền xám
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    cells = []
    for t, im in co_manh:
        bb = im.getbbox()
        if bb:
            cells.append((t, im.crop(bb)))
    cw = 380
    rows, x, y, hh = [], 10, 10, 0
    for t, c in cells:
        sc = min(1.0, (cw - 20) / c.width, 330 / c.height)
        c = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.LANCZOS)
        if x + cw > 1900:
            x, y, hh = 10, y + hh + 40, 0
        rows.append((t, c, x, y))
        x += cw
        hh = max(hh, c.height)
    sheet = Image.new("RGB", (1900, y + hh + 50), (140, 140, 140))
    d = ImageDraw.Draw(sheet)
    for t, c, x, y in rows:
        sheet.paste(c, (x, y + 20), c)
        d.text((x, y), t, fill=(255, 255, 255), font=F)
    sheet.save(os.path.join(BASE, "rig", "manh_soi.png"))
    print(os.path.join(BASE, "rig", "so_concept.png"))


def main(a):
    if not a or a[0] == "nhom":
        nhom()
    elif a[0] == "nhan":
        nhan()
    elif a[0] == "nhom_than":
        nhom_than()
    elif a[0] == "cat_than":
        cat_than()
    elif a[0] == "nhom_part":
        nhom_part(*a[1:])
    elif a[0] == "nhom_part_het":
        nhom_part_het()
    elif a[0] == "cat_part":
        cat_part(*a[1:])
    elif a[0] == "noi_part":
        noi_part()
    elif a[0] == "so_part":
        so_part(*a[1:])
    elif a[0] == "nhom_duoi":
        nhom_duoi()
    elif a[0] == "cat_duoi":
        cat_duoi()
    elif a[0] == "cat":
        cat(a[1:] or None)
        khop(a[1:] or None)
        if not a[1:] or "M" in a[1:]:
            cat_mo()
        if not a[1:] or "S" in a[1:]:
            cat_s()
    elif a[0] == "noi":
        noi()
    elif a[0] == "ghep":
        ghep()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
