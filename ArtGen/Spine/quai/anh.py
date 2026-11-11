# -*- coding: utf-8 -*-
"""Ảnh cho thư viện quai: cắt mảnh từ tờ GPT, mặt nạ, loang màu, hình giữ chỗ. Chỉ cần numpy + Pillow (không cần cv2).

    to = anh.doc_to("inbox/tm01_1/tai_ve/M01.png")            # mảnh rời trên nền trắng
    ten = anh.gan_theo_o(to, [["dau", "ham", "mieng"], ["than", None, "duoi"]])
    anh.luu_manh(to, ten, "inbox/tm01_1/manh", duc={"vong": "tam"})
    pc = anh.nap_manh("inbox/tm01_1/manh", GIU_CHO, ti_le=0.8)  # mảnh đã cắt (thiếu thì hình giữ chỗ), co theo tỉ lệ atlas, loang màu
"""
import glob
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

INK = (43, 33, 24)
FONT = "C:/Windows/Fonts/arial.ttf"


def font(size=14):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------- mặt nạ
def gian(m, r=1, tron=False):
    """giãn mặt nạ bool r px (ô vuông, hoặc đĩa nếu tron)."""
    m = np.asarray(m, bool)
    if r <= 0:
        return m.copy()
    H, W = m.shape
    if tron:
        p = np.pad(m, r)
        o = np.zeros_like(m)
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r + r:
                    o |= p[r + dy:r + dy + H, r + dx:r + dx + W]
        return o
    p = np.pad(m, ((0, 0), (r, r)))
    o = np.zeros_like(m)
    for d in range(2 * r + 1):
        o |= p[:, d:d + W]
    p = np.pad(o, ((r, r), (0, 0)))
    o2 = np.zeros_like(m)
    for d in range(2 * r + 1):
        o2 |= p[d:d + H, :]
    return o2


def co(m, r=1, tron=False):
    """co mặt nạ bool r px."""
    return ~gian(~np.asarray(m, bool), r, tron)


def mo_mo(m, r=1):
    """mở (co rồi giãn): bỏ sợi mảnh, chấm lẻ."""
    return gian(co(m, r), r)


def _taps(a, k, axis):
    r = len(k) // 2
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r, r)
    p = np.pad(a, pad, mode="edge")
    n = a.shape[axis]
    o = np.zeros_like(a)
    for i, w in enumerate(k):
        sl = [slice(None)] * a.ndim
        sl[axis] = slice(i, i + n)
        o += w * p[tuple(sl)]
    return o


def lam_mo(a, sigma):
    """làm mờ Gauss (mảng float, 2 hoặc 3 chiều)."""
    a = np.asarray(a, np.float32)
    if sigma <= 0:
        return a.copy()
    r = max(1, int(3 * sigma + 0.5))
    x = np.arange(-r, r + 1)
    k = np.exp(-x * x / (2.0 * sigma * sigma))
    k = (k / k.sum()).astype(np.float32)
    return _taps(_taps(a, k, 0), k, 1)


def lam_mo_hop(a, r):
    """trung bình ô (2r+1)x(2r+1)."""
    a = np.asarray(a, np.float32)
    k = np.full(2 * r + 1, 1.0 / (2 * r + 1), np.float32)
    return _taps(_taps(a, k, 0), k, 1)


def thanh_phan(m):
    """các cụm liền 8 hướng của mặt nạ bool. Trả (lab int32 HxW: 0 nền, 1..n), [dict(i, x0, y0, x1, y1, dt)] (x1, y1 không gồm).
    Ghép theo đoạn chạy từng hàng (union-find), nhanh cả với tờ 1536x1024 mà không cần cv2."""
    m = np.asarray(m, bool)
    H, W = m.shape
    d = np.diff(np.pad(m.astype(np.int8), ((0, 0), (1, 1))), axis=1)
    sr, sc = np.nonzero(d == 1)
    er, ec = np.nonzero(d == -1)
    n = len(sr)
    lab = np.zeros((H, W), np.int32)
    if n == 0:
        return lab, []
    rp = np.searchsorted(sr, np.arange(H + 1)).tolist()
    scl, ecl = sc.tolist(), ec.tolist()
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for y in range(1, H):
        i, i1, j, j1 = rp[y - 1], rp[y], rp[y], rp[y + 1]
        while i < i1 and j < j1:
            if scl[j] <= ecl[i] and scl[i] <= ecl[j]:
                a, b = find(i), find(j)
                if a != b:
                    if a < b:
                        par[b] = a
                    else:
                        par[a] = b
            if ecl[i] < ecl[j]:
                i += 1
            else:
                j += 1
    ids, out = {}, []
    srl = sr.tolist()
    for k in range(n):
        r = find(k)
        if r not in ids:
            ids[r] = len(ids) + 1
            out.append({"i": ids[r], "x0": W, "y0": H, "x1": 0, "y1": 0, "dt": 0})
        li = ids[r]
        y, a, b = srl[k], scl[k], ecl[k]
        lab[y, a:b] = li
        c = out[li - 1]
        c["dt"] += b - a
        c["x0"] = min(c["x0"], a)
        c["x1"] = max(c["x1"], b)
        c["y0"] = min(c["y0"], y)
        c["y1"] = max(c["y1"], y + 1)
    return lab, out


def nen_tu_mep(sang):
    """phần 'sáng' nối được ra mép ảnh (nền giấy)."""
    lab, _ = thanh_phan(sang)
    b = set(np.unique(lab[0]).tolist()) | set(np.unique(lab[-1]).tolist()) | set(np.unique(lab[:, 0]).tolist()) | set(np.unique(lab[:, -1]).tolist())
    b.discard(0)
    return np.isin(lab, list(b)) if b else np.zeros(sang.shape, bool)


def lap_lo(m, toi_da=None):
    """lấp lỗ (vùng không thuộc m mà không chạm mép); toi_da: chỉ lấp lỗ có diện tích <= toi_da px."""
    m = np.asarray(m, bool)
    lab, cs = thanh_phan(~m)
    H, W = m.shape
    out = m.copy()
    edge = set(np.unique(lab[0]).tolist()) | set(np.unique(lab[-1]).tolist()) | set(np.unique(lab[:, 0]).tolist()) | set(np.unique(lab[:, -1]).tolist())
    fill = [c["i"] for c in cs if c["i"] not in edge and (toi_da is None or c["dt"] <= toi_da)]
    if fill:
        out |= np.isin(lab, fill)
    return out


def bao_loi(pts):
    """bao lồi (chuỗi đơn điệu): pts (N, 2) -> (K, 2) ngược chiều kim đồng hồ theo toạ độ ảnh."""
    P = sorted(set(map(tuple, np.asarray(pts, float).tolist())))
    if len(P) < 3:
        return np.array(P, float)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return np.array(lo[:-1] + hi[:-1], float)


def to_da_giac(shape, poly, val=True):
    """mặt nạ bool cỡ shape (H, W) tô đa giác poly [(x, y)...] toạ độ ảnh."""
    H, W = shape
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(map(float, p)) for p in poly], fill=255)
    return np.asarray(im) > 127 if val else np.asarray(im) <= 127


# ---------------------------------------------------------------- cắt tờ GPT
class To:
    """một tờ GPT đã tách: rgba (nền trong suốt, mép mềm), lab (nhãn cụm), manh [dict(i, x0, y0, x1, y1, dt, ids)]."""

    def __init__(self, path, rgba, lab, manh):
        self.path, self.rgba, self.lab, self.manh = path, rgba, lab, manh
        self.h, self.w = rgba.shape[:2]


def to_moi_nhat(thu_muc, buoc):
    """ảnh GPT mới nhất của một bước (M01.png, M01_2.png ...)."""
    fs = sorted(glob.glob(os.path.join(thu_muc, buoc + "*.png")), key=os.path.getmtime)
    return fs[-1] if fs else None


def doc_to(path, nguong_sang=236, dien_tich_min=900, gop_px=40):
    """tách các mảnh rời trên nền trắng: loang nền sáng từ mép (giấy trắng khép kín bên trong mảnh như tròng mắt, răng vẫn giữ),
    bỏ sợi mảnh 1 px, tách cụm liền, mẩu nhỏ cách mảnh lớn dưới gop_px thì nhập vào mảnh đó. Mép alpha mềm (co 1 px, mờ 1,1)."""
    rgb = np.asarray(Image.open(path).convert("RGB"))
    bg = nen_tu_mep(rgb.min(axis=2) > nguong_sang)
    fg = mo_mo(~bg, 1)
    lab, cs = thanh_phan(fg)
    big = [dict(c, ids=[c["i"]]) for c in cs if c["dt"] >= dien_tich_min]
    for c in cs:
        if c["dt"] >= dien_tich_min or c["dt"] < 30:
            continue
        best, bd = None, gop_px
        for o in big:
            dx = max(o["x0"] - c["x1"], c["x0"] - o["x1"], 0)
            dy = max(o["y0"] - c["y1"], c["y0"] - o["y1"], 0)
            if max(dx, dy) < bd:
                best, bd = o, max(dx, dy)
        if best is not None:
            best["ids"].append(c["i"])
            best["dt"] += c["dt"]
            for k, f in (("x0", min), ("y0", min), ("x1", max), ("y1", max)):
                best[k] = f(best[k], c[k])
    alpha = lam_mo(co(fg, 1).astype(np.float32), 1.1)
    rgba = np.dstack([rgb, (np.clip(alpha * 1.25, 0, 1) * 255).astype(np.uint8)])
    return To(path, rgba, lab, big)


def gan_theo_o(to, luoi, giu_lon=True):
    """gán tên theo ô lưới đã dặn GPT: luoi = [[tên hàng 1 ...], [hàng 2 ...]] (None = bỏ). Mỗi ô giữ mảnh lớn nhất
    (giu_lon) và trả {tên: mảnh}; in mảnh thừa."""
    R = len(luoi)
    out, thua = {}, []
    for m in to.manh:
        cx, cy = (m["x0"] + m["x1"]) / 2, (m["y0"] + m["y1"]) / 2
        r = min(R - 1, int(cy / (to.h / R)))
        row = luoi[r]
        c = min(len(row) - 1, int(cx / (to.w / len(row))))
        nm = row[c]
        if nm is None:
            thua.append(m)
            continue
        if nm in out:
            if giu_lon and m["dt"] > out[nm]["dt"]:
                thua.append(out[nm])
                out[nm] = m
            else:
                thua.append(m)
        else:
            out[nm] = m
    if thua:
        print(f"  {os.path.basename(to.path)}: {len(thua)} mảnh không gán: " + ", ".join(f"({m['x0']},{m['y0']}) {m['x1'] - m['x0']}x{m['y1'] - m['y0']}" for m in thua[:8]))
    return out


def gan_theo_thu_tu(manh, ten, khoa="x"):
    """gán tên theo thứ tự (khoa: 'x' trái → phải, 'y' trên → dưới, 'dt' lớn → nhỏ) cho danh sách mảnh."""
    f = {"x": lambda m: (m["x0"] + m["x1"]) / 2, "y": lambda m: (m["y0"] + m["y1"]) / 2, "dt": lambda m: -m["dt"]}[khoa]
    return {t: m for t, m in zip(ten, sorted(manh, key=f)) if t}


def duc_long(im, diem=None, tu_dong=0, nguong=236):
    """đục giấy trắng khép kín bên trong mảnh thành trong suốt (lòng vòng sóng, khe giữa càng...).
    diem: [(fx, fy)] theo tỉ lệ khung mảnh, hoặc "tam" (tâm khung); tu_dong: đục mọi vùng trắng kín có diện tích >= số này mà
    phẳng như giấy (độ lệch màu < 3; tròng mắt, răng vẽ có vân thì giữ)."""
    a = np.asarray(im).copy()
    hh, ww = a.shape[:2]
    light = a[..., :3].min(axis=2) > nguong
    lab, cs = thanh_phan(light & (a[..., 3] > 0))
    edge = set(np.unique(lab[0]).tolist()) | set(np.unique(lab[-1]).tolist()) | set(np.unique(lab[:, 0]).tolist()) | set(np.unique(lab[:, -1]).tolist())
    pick = set()
    if diem == "tam":
        diem = [(0.5, 0.5)]
    for fx, fy in diem or []:
        x, y = int(fx * (ww - 1)), int(fy * (hh - 1))
        if lab[y, x]:
            pick.add(int(lab[y, x]))
    if tu_dong:
        for c in cs:
            if c["i"] in edge or c["dt"] < tu_dong:
                continue
            px = a[..., :3][lab == c["i"]].astype(np.float32)
            if px.std(axis=0).max() < 3.0:
                pick.add(c["i"])
    if not pick:
        return Image.fromarray(a, "RGBA")
    hole = gian(np.isin(lab, list(pick)), 1)
    soft = lam_mo((~hole).astype(np.float32), 1.1)
    a[..., 3] = (a[..., 3] * np.clip(soft * 1.2 - 0.1, 0, 1)).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def cat_manh(to, m, pad=4):
    """ảnh RGBA của một mảnh (chỉ cụm của nó, mép giãn 2 px để giữ viền mờ)."""
    x0, y0 = max(0, m["x0"] - pad), max(0, m["y0"] - pad)
    x1, y1 = min(to.w, m["x1"] + pad), min(to.h, m["y1"] + pad)
    im = to.rgba[y0:y1, x0:x1].copy()
    keep = gian(np.isin(to.lab[y0:y1, x0:x1], m["ids"]), 2)
    im[..., 3] = (im[..., 3] * keep).astype(np.uint8)
    return Image.fromarray(im, "RGBA")


def luu_manh(to, ten, thu_muc, duc=None, pad=4):
    """lưu từng mảnh <tên>.png; duc = {tên: diem | "tam" | ("tu_dong", diện tích)} để đục lòng giấy trắng khép kín."""
    os.makedirs(thu_muc, exist_ok=True)
    out = {}
    for nm, m in ten.items():
        im = cat_manh(to, m, pad)
        if duc and nm in duc:
            d = duc[nm]
            im = duc_long(im, tu_dong=d[1]) if isinstance(d, tuple) and d and d[0] == "tu_dong" else duc_long(im, diem=d)
        im.save(os.path.join(thu_muc, nm + ".png"))
        out[nm] = im
    print(f"  {os.path.basename(to.path)}: " + ", ".join(f"{k} {v.width}x{v.height}" for k, v in out.items()))
    return out


def to_soi(thu_muc, ten, ra=None, rong=1800):
    """tờ soi mọi mảnh trên nền xám (_soi.png)."""
    ims = [(k, Image.open(os.path.join(thu_muc, k + ".png"))) for k in ten if os.path.exists(os.path.join(thu_muc, k + ".png"))]
    if not ims:
        return None
    x = y = 10
    row = 0
    sheet = Image.new("RGB", (rong, 4000), (120, 124, 132))
    d = ImageDraw.Draw(sheet)
    f = font(13)
    for k, im in ims:
        im = im.copy()
        im.thumbnail((560, 320))
        if x + im.width + 10 > rong:
            x, y, row = 10, y + row + 26, 0
        sheet.paste(im, (x, y + 16), im)
        d.text((x, y), f"{k} {im.width}x{im.height}", fill=(255, 255, 255), font=f)
        x += im.width + 14
        row = max(row, im.height + 16)
    ra = ra or os.path.join(thu_muc, "_soi.png")
    sheet.crop((0, 0, rong, y + row + 20)).save(ra)
    return ra


# ---------------------------------------------------------------- loang màu, nạp mảnh
def loang_mau(im, lan=6):
    """màu của điểm trong suốt lấy theo mép hình gần nhất (lọc tuyến tính trong atlas không kéo viền trắng vào)."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3].copy(), a[..., 3]
    w = (al > 5).astype(np.float32)
    cur = rgb * w[..., None]
    for _ in range(lan):
        num = lam_mo_hop(cur, 2)
        den = lam_mo_hop(w, 2)
        fill = num / np.maximum(den, 1e-4)[..., None]
        grow = (den > 1e-3).astype(np.float32)
        cur = cur * w[..., None] + fill * ((1 - w) * grow)[..., None]
        w = np.maximum(w, grow)
    out = np.where((al > 5)[..., None], rgb, cur)
    return Image.fromarray(np.dstack([out, a[..., 3:]]).clip(0, 255).astype(np.uint8), "RGBA")


def _but_chi(d, box, col, rng, n=30):
    """vân chì nhạt cho hình giữ chỗ (để thử bảng 256 màu)."""
    x0, y0, x1, y1 = box
    dk = tuple(max(0, c - 22) for c in col)
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        L = rng.uniform(6, 18)
        d.line([(x, y), (x + L, y - L * 0.6)], fill=dk + (255,), width=1)


def gia(hinh, w, h, mau=(86, 160, 214), vien=5, hat=0):
    """hình giữ chỗ khi chưa có ảnh GPT (dựng rig song song lúc chờ gen). hinh: 'tron' (elip), 'bo' (chữ nhật bo góc), 'dai'
    (dải thuôn: đuôi, râu, cổ), 'giot', 'mat' (tròng trắng + con ngươi), 'mi' (mí: nửa elip màu da), 'ham' (hàm dưới có răng),
    'mieng' (lòng miệng đỏ hồng), 'chan' (chân thuôn có bàn), 'luoi' (lưỡi). Viền mực nâu, tô phẳng, vân chì nhạt."""
    rng = np.random.RandomState(hat or (w * 31 + h))
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink = INK + (255,)
    col = tuple(mau) + (255,)
    v = vien
    if hinh == "tron":
        d.ellipse([v, v, w - 1 - v, h - 1 - v], fill=col, outline=ink, width=v)
        _but_chi(d, (w * 0.25, h * 0.25, w * 0.7, h * 0.7), mau, rng)
        d.ellipse([v, v, w - 1 - v, h - 1 - v], outline=ink, width=v)
    elif hinh == "bo":
        d.rounded_rectangle([v, v, w - 1 - v, h - 1 - v], radius=min(w, h) // 3, fill=col, outline=ink, width=v)
    elif hinh in ("dai", "luoi"):
        pts = []
        for i in range(41):
            u = i / 40
            hw = (h / 2 - v) * (1.0 - 0.75 * u ** 1.4)
            pts.append((v + u * (w - 2 * v), h / 2 - hw))
        pts += [(x, h - y) for x, y in reversed(pts)]
        d.polygon(pts, fill=col, outline=ink, width=v)
        if hinh == "dai":
            for i in range(1, 8):  # vạch ngang để thấy lưới uốn
                x = v + (w - 2 * v) * i / 8
                hw = (h / 2 - v) * (1.0 - 0.75 * (i / 8) ** 1.4)
                d.line([(x, h / 2 - hw * 0.8), (x, h / 2 + hw * 0.8)], fill=tuple(max(0, c - 40) for c in mau) + (255,), width=3)
        else:
            d.line([(w * 0.1, h / 2), (w * 0.85, h / 2)], fill=tuple(max(0, c - 50) for c in mau) + (255,), width=2)
    elif hinh == "ong":  # ống hai chỏm tròn (tay, xúc tu ngắn dày), vạch ngang để thấy lưới uốn
        r = (h - 2 * v) / 2
        d.rounded_rectangle([v, v, w - 1 - v, h - 1 - v], radius=int(r), fill=col, outline=ink, width=v)
        dk = tuple(max(0, c - 40) for c in mau) + (255,)
        for i in range(1, 6):
            x = r + v + (w - 2 * r - 2 * v) * i / 6
            d.line([(x, v + 4), (x, h - v - 5)], fill=dk, width=3)
    elif hinh == "giot":
        d.polygon([(w / 2, v), (w - v, h * 0.65), (w / 2, h - v), (v, h * 0.65)], fill=col, outline=ink)
    elif hinh == "mat":
        d.ellipse([v, v, w - 1 - v, h - 1 - v], fill=(250, 246, 236, 255), outline=ink, width=v)
        r = min(w, h) * 0.26
        d.ellipse([w * 0.58 - r, h * 0.52 - r, w * 0.58 + r, h * 0.52 + r], fill=(240, 150, 40, 255), outline=ink, width=2)
        r2 = r * 0.5
        d.ellipse([w * 0.6 - r2, h * 0.52 - r2, w * 0.6 + r2, h * 0.52 + r2], fill=INK + (255,))
        d.ellipse([w * 0.53, h * 0.36, w * 0.53 + r * 0.45, h * 0.36 + r * 0.45], fill=(255, 255, 255, 255))
    elif hinh == "mi":
        d.ellipse([v, v, w - 1 - v, h - 1 - v], fill=col, outline=ink, width=v)
        d.arc([w * 0.15, h * 0.2, w * 0.85, h * 0.8], 20, 160, fill=ink, width=3)
    elif hinh == "ham":
        d.rounded_rectangle([v, v, w - 1 - v, h - 1 - v], radius=h // 2 - 2, fill=col, outline=ink, width=v)
        for x in np.linspace(w * 0.4, w * 0.9, 4):
            d.polygon([(x, v + 2), (x + w * 0.05, v + 2), (x + w * 0.025, v + h * 0.35)], fill=(250, 248, 240, 255), outline=ink)
    elif hinh == "mieng":
        d.rounded_rectangle([v, v, w - 1 - v, h - 1 - v], radius=min(w, h) // 3, fill=(184, 64, 90, 255), outline=ink, width=v)
        d.ellipse([w * 0.3, h * 0.45, w * 0.8, h * 0.85], fill=(226, 124, 146, 255))
    elif hinh == "chan":
        d.rounded_rectangle([w * 0.18, v, w * 0.82, h * 0.86], radius=int(w * 0.3), fill=col, outline=ink, width=v)
        d.ellipse([v, h * 0.7, w - 1 - v, h - 1 - v], fill=col, outline=ink, width=v)
        for x in (0.3, 0.5, 0.7):
            d.line([(w * x, h * 0.84), (w * x, h * 0.95)], fill=ink, width=2)
    else:
        d.rectangle([v, v, w - 1 - v, h - 1 - v], fill=col, outline=ink, width=v)
    return im


def nap_manh(thu_muc, giu_cho, ti_le=1.0, ti_le_rieng=None, loang=True):
    """nạp mảnh đã cắt: giu_cho = {tên: (hình, w, h, màu)} (cỡ theo tờ GPT; thiếu ảnh thì vẽ hình giữ chỗ). Cắt sát, co theo
    ti_le (đơn vị rig = pixel atlas) và ti_le_rieng[tên], loang màu ra vùng trong suốt. Trả {tên: PIL RGBA}."""
    out, fake = {}, []
    for nm, spec in giu_cho.items():
        p = os.path.join(thu_muc, nm + ".png") if thu_muc else None
        if p and os.path.exists(p):
            im = Image.open(p).convert("RGBA")
        else:
            hinh, w, h, mau = spec
            im = gia(hinh, w, h, mau)
            fake.append(nm)
        bb = im.getbbox()
        if bb:
            im = im.crop(bb)
        k = ti_le * (ti_le_rieng or {}).get(nm, 1.0)
        if abs(k - 1) > 1e-6:
            im = im.resize((max(2, round(im.width * k)), max(2, round(im.height * k))), Image.LANCZOS)
        out[nm] = loang_mau(im) if loang else im
    if fake:
        print("  mảnh giữ chỗ:", ", ".join(fake))
    return out
