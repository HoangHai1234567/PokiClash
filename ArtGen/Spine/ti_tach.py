# -*- coding: utf-8 -*-
"""Dòng Tí Tách (giọt nước dáng vòm, làm lại 2026-11-11): cắt mảnh từ concept đã duyệt, cắt tờ nét mặt GPT.

    py -3 -I ArtGen/Spine/ti_tach.py cat 1|2     cắt concept dạng k -> inbox/ti_tach_<k>/manh/ (than, mat_mo, ma, giot_<i>, manh.json, _soi.png)
    py -3 -I ArtGen/Spine/ti_tach.py mat         cắt tờ nét mặt M01 (dùng chung hai dạng) -> inbox/ti_tach_1/mat/ (+ _soi.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ti_tach.py rig 1|2   dựng rig một dạng (không có evolve) -> inbox/ti_tach_<k>/rig/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ti_tach.py all       dạng 2 rồi dạng 1 gộp dạng 2 (clip evolve)

Cách cắt (khớp concept 100 %): thân = cụm lớn nhất sau khi loang nền trắng từ mép; mặt (hai mắt, hai vệt má) tách theo màu rồi
XOÁ khỏi thân bằng cách chép vân sáp từ vùng thân sạch bên cạnh (không nhờ GPT vẽ lại thân: GPT vẽ lại thì lệch dáng). Giọt con là
các cụm rời còn lại. Toạ độ trong manh.json là pixel concept (1536 x 1024, y xuống).
Ghi chú thiết kế, mổ xẻ con gốc: inbox/ti_tach_ghichu.md.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ti_tach"
GRAY = (150, 150, 150)


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def concept(k):
    return os.path.join(d_inbox(k), "tai_ve", "L1_duyet.png")


def moi_nhat(thu_muc, goc):
    """ảnh mới nhất của một bước: M01.png, M01_2.png, M01_3.png..."""
    best, bn = None, -1
    for f in os.listdir(thu_muc):
        n, e = os.path.splitext(f)
        if e.lower() != ".png" or not (n == goc or n.startswith(goc + "_")):
            continue
        s = n[len(goc) + 1:]
        i = int(s) if s.isdigit() else (1 if n == goc else -1)
        if i > bn:
            best, bn = os.path.join(thu_muc, f), i
    return best


def nen_trang(a, nguong=236):
    """mặt nạ nền: vùng sáng nối mép ảnh."""
    w = (a.min(2) >= nguong).astype(np.uint8)
    n, lab = cv2.connectedComponents(w, connectivity=4)
    mep = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    mep = mep[mep != 0] if not w[0, 0] else mep
    bg = np.isin(lab, mep) & (w > 0)
    return bg


def cum(mask, min_dt=300):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    out = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= min_dt:
            x, y, w, h, dt = st[i]
            out.append({"m": lab == i, "x0": int(x), "y0": int(y), "x1": int(x + w), "y1": int(y + h), "dt": int(dt)})
    return out


def lap_lo(m):
    """lấp lỗ kín của một mặt nạ."""
    pad = np.pad((~m).astype(np.uint8), 1, constant_values=1)
    n, lab = cv2.connectedComponents(pad, connectivity=4)
    return m | ((pad[1:-1, 1:-1] > 0) & (lab[1:-1, 1:-1] != lab[0, 0]))


def gian(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(m.astype(np.uint8), k) > 0


def co(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.erode(m.astype(np.uint8), k) > 0


def luu(a, alpha, box, path):
    x0, y0, x1, y1 = box
    rgba = np.dstack([a[y0:y1, x0:x1].astype(np.uint8), (np.clip(alpha[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(path)


def hop(m, le=3):
    ys, xs = np.nonzero(m)
    return [max(0, int(xs.min()) - le), max(0, int(ys.min()) - le), min(m.shape[1], int(xs.max()) + 1 + le),
            min(m.shape[0], int(ys.max()) + 1 + le)]


def chep_van(a, vung, sach, than_trong):
    """Xoá một cụm của mặt: chép vân sáp từ vùng thân sạch gần nhất (dịch cả mảng một véc-tơ), mép hoà 5 px."""
    can = gian(vung, 14)
    ys, xs = np.nonzero(can)
    h, w = vung.shape
    ung = []
    for dx in range(-520, 521, 10):
        for dy in range(-260, 261, 10):
            if abs(dx) < 30 and abs(dy) < 30:
                continue
            y2, x2 = ys + dy, xs + dx
            if y2.min() < 0 or x2.min() < 0 or y2.max() >= h or x2.max() >= w:
                continue
            if sach[y2, x2].mean() > 0.997:
                ung.append((dx * dx + 4 * dy * dy, dx, dy))     # ưu tiên dịch ngang (vân sáp chạy chéo đều, dịch dọc đổi tông ít)
    if not ung:
        raise SystemExit("không tìm được vùng thân sạch để chép vân")
    _, dx, dy = min(ung)
    m = cv2.GaussianBlur(gian(vung, 7).astype(np.float32), (0, 0), 2.5)[..., None]
    src = np.roll(a, (-dy, -dx), axis=(0, 1))
    return a * (1 - m) + src * m, (dx, dy)


def cat(k):
    src = concept(k)
    if not os.path.exists(src):
        raise SystemExit("chưa có " + src)
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    bg = nen_trang(a)
    cs = sorted(cum(~bg), key=lambda c: -c["dt"])
    than_c, giot = cs[0], sorted(cs[1:], key=lambda c: c["x0"])
    than = lap_lo(than_c["m"])
    ra = os.path.join(d_inbox(k), "manh")
    os.makedirs(ra, exist_ok=True)
    info = {"concept": os.path.basename(src), "cỡ": [a.shape[1], a.shape[0]], "manh": {}}

    # mặt: viền mắt lam đậm (G thấp), lòng mắt (lỗ trong viền), vệt má (G vừa, B cao)
    trong = co(than, 10)
    vien = (G < 125) & (B > 80) & (B - R > 55) & trong
    mat_c = sorted(cum(vien, 600), key=lambda c: -c["dt"])[:2]
    mat_c.sort(key=lambda c: c["x0"])                         # trái = mắt gần (to), phải = mắt xa
    mat = np.zeros_like(than)
    for c in mat_c:
        mat |= lap_lo(gian(c["m"], 1))
    ma_ung = (G < 196) & (R < 110) & (B > 195) & trong & ~gian(mat, 3)
    y_mat = min(c["y0"] for c in mat_c)
    ma_ung[:y_mat] = False
    ma_c = sorted(cum(ma_ung, 500), key=lambda c: -c["dt"])[:2]
    ma_c.sort(key=lambda c: c["x0"])
    ma = np.zeros_like(than)
    for c in ma_c:
        ma |= c["m"]

    # thân trơn: xoá từng cụm mặt bằng vân sáp chép từ chỗ sạch
    dom = cv2.morphologyEx(((R > 135) & (G > 222) & trong).astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0   # đốm bong bóng
    sach = co(than, 14) & ~gian(mat, 10) & ~gian(ma, 12) & ~gian(dom, 6) & (G > 185)
    tron, dich = a.copy(), []
    for c in mat_c:
        tron, d = chep_van(tron, lap_lo(gian(c["m"], 1)), sach, trong)
        dich.append(d)
    for c in ma_c:
        tron, d = chep_van(tron, c["m"], sach, trong)
        dich.append(d)
    al_than = cv2.GaussianBlur(than.astype(np.float32), (0, 0), 0.7)
    al_than = np.where(co(than, 2), 1.0, al_than)
    box = hop(than)
    luu(tron, al_than, box, os.path.join(ra, "than.png"))
    info["manh"]["than"] = box

    # mắt mở (cặp): viền + lòng; mép ngoài mềm theo G
    al_mat = np.where(mat, 1.0, 0.0)
    ngoai = gian(mat, 3) & ~mat
    al_mat = np.where(ngoai, np.clip((205 - G) / 80, 0, 1), al_mat)
    box = hop(gian(mat, 3))
    luu(a, al_mat, box, os.path.join(ra, "mat_mo.png"))
    info["manh"]["mat_mo"] = box
    info["mat"] = [{"x0": c["x0"], "y0": c["y0"], "x1": c["x1"], "y1": c["y1"]} for c in mat_c]

    # vệt má (cặp): độ đậm mềm theo G
    al_ma = np.where(gian(ma, 6), np.clip((208 - G) / 36, 0, 1), 0.0) * (R < 120) * (B > 180)
    box = hop(al_ma > 0.05)
    luu(a, al_ma, box, os.path.join(ra, "ma.png"))
    info["manh"]["ma"] = box

    # giọt con
    for i, c in enumerate(giot, 1):
        m = lap_lo(c["m"])
        al = np.where(co(m, 2), 1.0, cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7))
        box = hop(m)
        luu(a, al, box, os.path.join(ra, f"giot_{i}.png"))
        info["manh"][f"giot_{i}"] = box
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # tờ soi: (1) thân trơn + giọt trên nền xám, (2) ghép lại đủ mặt, (3) concept, (4) chỗ khác nhau giữa (2) và (3)
    H, Wd = a.shape[:2]

    def nen():
        return Image.new("RGBA", (Wd, H), GRAY + (255,))

    def dan(im, ten):
        p = Image.open(os.path.join(ra, ten + ".png"))
        x0, y0 = info["manh"][ten][:2]
        im.alpha_composite(p, (x0, y0))

    t1 = nen()
    for ten in info["manh"]:
        if ten == "than" or ten.startswith("giot"):
            dan(t1, ten)
    t2 = nen()
    for ten in ["than", "ma", "mat_mo"] + [n for n in info["manh"] if n.startswith("giot")]:
        dan(t2, ten)
    t3 = nen()
    al_all = np.where(bg, 0, 255).astype(np.uint8)
    t3.alpha_composite(Image.fromarray(np.dstack([a.astype(np.uint8), al_all]), "RGBA"))
    d = np.abs(np.array(t2.convert("RGB")).astype(int) - np.array(t3.convert("RGB")).astype(int)).max(2)
    t4 = Image.fromarray(np.dstack([np.clip(d * 4, 0, 255)] * 3).astype(np.uint8)).convert("RGBA")
    t5 = nen()                                                    # mặt rời đặt lệch sang trái 160 px: thấy thân sạch bên dưới
    dan(t5, "than")
    for ten in ("ma", "mat_mo"):
        p = Image.open(os.path.join(ra, ten + ".png"))
        x0, y0 = info["manh"][ten][:2]
        t5.alpha_composite(p, (x0 - 220, y0 - 30))
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    to = Image.new("RGBA", (Wd * 3 // 2, H), (60, 60, 60, 255))
    o = [(t1, "1. thân đã xoá mặt + giọt con"), (t5, "2. mặt trượt trái 220 px (thân bên dưới phải sạch)"),
         (t2, "3. ghép lại"), (t3, "4. concept"), (t4, "5. khác nhau giữa 3 và 4 (x4)")]
    to = Image.new("RGBA", (Wd // 2 * 3, H // 2 * 2), (60, 60, 60, 255))
    for i, (im, chu) in enumerate(o):
        s = im.resize((Wd // 2, H // 2), Image.LANCZOS)
        ImageDraw.Draw(s).text((12, 8), chu, fill=(255, 255, 255, 255), font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22))
        to.alpha_composite(s, ((i % 3) * (Wd // 2), (i // 3) * (H // 2)))
    to.convert("RGB").save(os.path.join(ra, "_soi.png"))
    print(f"dạng {k}: thân {info['manh']['than']}, mắt {[(c['x1'] - c['x0'], c['y1'] - c['y0']) for c in mat_c]}, "
          f"má {len(ma_c)}, giọt {len(giot)}; dịch vân {dich}; khác concept tối đa {int(d.max())}, "
          f"{int((d > 24).sum())} px lệch > 24 -> {os.path.join(ra, '_soi.png')}")


# ---------------------------------------------------------------- tờ nét mặt GPT (M01): 3 x 2 ô 512
O_MAT = [["mat_nhan", "mat_xoay", "mat_cuoi"], ["mat_chop", "mieng_nho", "mieng_to"]]


def cat_mat():
    thu = os.path.join(d_inbox(1), "tai_ve")
    src = moi_nhat(thu, "M01")
    if not src:
        raise SystemExit("chưa có tờ M01 trong " + thu)
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    H, Wd = a.shape[:2]
    bg = nen_trang(a, 232)
    ra = os.path.join(d_inbox(1), "mat")
    os.makedirs(ra, exist_ok=True)
    info = {"to": os.path.basename(src), "manh": {}}
    R = a[..., 0]
    # nét lam trên trắng: độ đậm mềm theo R (lam đậm R ~ 10, trắng 255); lòng kín (mắt xoáy, miệng) đặc
    al = np.where(bg, np.clip((238 - R) / 150, 0, 1), 1.0)
    al = np.where(bg & ~gian(~bg, 2), 0.0, al)
    for r, hang in enumerate(O_MAT):
        for c, ten in enumerate(hang):
            x0, y0, x1, y1 = c * Wd // 3, r * H // 2, (c + 1) * Wd // 3, (r + 1) * H // 2
            m = np.zeros_like(bg)
            m[y0:y1, x0:x1] = ~bg[y0:y1, x0:x1]
            cc = [q for q in cum(m, 120)]
            if not cc:
                print("  thiếu", ten)
                continue
            mm = np.zeros_like(bg)
            for q in cc:
                mm |= q["m"]
            box = hop(mm, 4)
            # màu: bỏ lẫn trắng ở mép (unpremultiply với nền trắng)
            aa = np.clip(al, 0.02, 1)[..., None]
            col = np.clip((a - (1 - aa) * 255) / aa, 0, 255)
            luu(col, al * gian(mm, 3), box, os.path.join(ra, ten + ".png"))
            info["manh"][ten] = {"hop": box, "cum": [[q["x0"], q["y0"], q["x1"], q["y1"]] for q in sorted(cc, key=lambda q: q["x0"])]}
    json.dump(info, open(os.path.join(ra, "mat.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # tờ soi: từng nét mặt đặt lên thân trơn dạng 1 (đúng chỗ mắt concept), kèm mắt mở
    mj = json.load(open(os.path.join(d_inbox(1), "manh", "manh.json"), encoding="utf-8"))
    tx0, ty0, tx1, ty1 = mj["manh"]["than"]
    than = Image.open(os.path.join(d_inbox(1), "manh", "than.png"))
    ma = Image.open(os.path.join(d_inbox(1), "manh", "ma.png"))
    mo = Image.open(os.path.join(d_inbox(1), "manh", "mat_mo.png"))
    e = mj["mat"]
    cxm = (e[0]["x0"] + e[1]["x1"]) / 2
    cym = (e[0]["y0"] + e[0]["y1"]) / 2
    cmx, cmy = (e[0]["x1"] + e[1]["x0"]) / 2 + 12, mj["manh"]["ma"][3] + 48          # chỗ miệng: giữa hai mắt, dưới vệt má

    def canh(mat=None, mieng=None, ti_mieng=1.0):
        im = Image.new("RGBA", (tx1 - tx0 + 40, ty1 - ty0 + 40), GRAY + (255,))
        im.alpha_composite(than, (20, 20))
        im.alpha_composite(ma, (mj["manh"]["ma"][0] - tx0 + 20, mj["manh"]["ma"][1] - ty0 + 20))
        if mat is None:
            im.alpha_composite(mo, (mj["manh"]["mat_mo"][0] - tx0 + 20, mj["manh"]["mat_mo"][1] - ty0 + 20))
        else:
            p = Image.open(os.path.join(ra, mat + ".png"))
            ti = (e[1]["x1"] - e[0]["x0"]) / p.width          # cặp nét mặt co cho vừa bề ngang cặp mắt concept
            p = p.resize((max(1, int(p.width * ti)), max(1, int(p.height * ti))), Image.LANCZOS)
            im.alpha_composite(p, (int(cxm - p.width / 2) - tx0 + 20, int(cym - p.height / 2) - ty0 + 20))
        if mieng:
            p = Image.open(os.path.join(ra, mieng + ".png"))
            if ti_mieng != 1.0:
                p = p.resize((max(1, int(p.width * ti_mieng)), max(1, int(p.height * ti_mieng))), Image.LANCZOS)
            im.alpha_composite(p, (int(cmx - p.width / 2) - tx0 + 20, int(cmy - p.height / 2) - ty0 + 20))
        return im

    o = [(canh(), "mắt mở (concept)"), (canh("mat_nhan"), "mat_nhan  > <"), (canh("mat_xoay"), "mat_xoay"),
         (canh("mat_cuoi"), "mat_cuoi  ^ ^"), (canh("mat_chop"), "mat_chop"), (canh(None, "mieng_nho", 0.55), "mắt mở + mieng_nho"),
         (canh("mat_nhan", "mieng_to", 0.55), "mat_nhan + mieng_to"), (canh(None, "mieng_to", 0.55), "mắt mở + mieng_to")]
    w1, h1 = o[0][0].size
    s = 0.55
    cw, ch = int(w1 * s), int(h1 * s)
    to = Image.new("RGBA", (cw * 4, ch * 2), (60, 60, 60, 255))
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    for i, (im, chu) in enumerate(o):
        q = im.resize((cw, ch), Image.LANCZOS)
        ImageDraw.Draw(q).text((10, 6), chu, fill=(255, 255, 255, 255), font=f)
        to.alpha_composite(q, ((i % 4) * cw, (i // 4) * ch))
    to.convert("RGB").save(os.path.join(ra, "_soi.png"))
    print("tờ nét mặt:", {k: v["hop"] for k, v in info["manh"].items()}, "->", os.path.join(ra, "_soi.png"))


# ================================================================ RIG (thư viện quai) ================================================================
# Cấu trúc học từ con gốc monster_3203 (ghi chú inbox/ti_tach_ghichu.md mục 2):
#   root -> move (game dời: lao, nhảy) -> lon (tâm thân: rơi lúc xuất hiện) -> day (ở đất: nén giãn, nghiêng, dời = bone2 của gốc)
#        -> than (khối trên: lắc, phình = bone3) -> dinh (đỉnh vòm, lò xo: thạch rung) -> can0, can1 (cần đỡ giọt, lò xo) -> cum -> g<i>
#                                                -> mat (mặt: trượt = bone7) -> mom (miệng: co giãn), mieng (chỗ và hướng nhả)
# Thân là MỘT lưới dày, trọng số theo chiều cao (day / than / dinh), nên không có khớp nào để hở. Mặt là lớp dán đổi hình.
SC = 0.5                      # pixel concept -> pixel rig
REF_W, REF_H = 226.0, 168.0   # cỡ thân con gốc (đơn vị rig của nó): đổi độ dời của khoá gốc sang cỡ thân mình
CHAM = {1: 1.0, 2: 1.12}      # dạng 2 nặng hơn: mọi clip chậm lại chừng này
CAO_HIEU = {1: 1.0, 2: 1.0}   # game quy mọi dạng về cùng chiều cao rồi nhân size trong heroes.json (0,92 / 1,1): không khai lệch ở đây
TI_MIENG = 0.55               # miệng trên tờ GPT to hơn cần: co lại (so với cỡ concept dạng 1)


def _quai():
    sys.path.insert(0, HERE)
    from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat
    return anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat


def ln(f, keys):
    """nội suy thẳng theo khung (như phần lớn khoá của con gốc)."""
    return float(np.interp(f, [k[0] for k in keys], [k[1] for k in keys]))


def spl(f, keys, chu_ky=None):
    """đường cong trơn qua các khoá (Hermite, tiếp tuyến trung bình hai bên) cho khoá bezier của con gốc; chu_ky: khép vòng."""
    xs, vs = [float(k[0]) for k in keys], [float(k[1]) for k in keys]
    if chu_ky:
        f = f % chu_ky
        xs = [xs[-1] - chu_ky] + xs + [xs[0] + chu_ky, xs[1] + chu_ky]
        vs = [vs[-1]] + vs + [vs[0], vs[1]]
    else:
        f = min(max(f, xs[0]), xs[-1])
        xs = [xs[0] - 1] + xs + [xs[-1] + 1]
        vs = [vs[0]] + vs + [vs[-1]]
    i = 1
    while i < len(xs) - 3 and f > xs[i + 1]:
        i += 1

    def m(j):
        return 0.5 * ((vs[j + 1] - vs[j]) / (xs[j + 1] - xs[j]) + (vs[j] - vs[j - 1]) / (xs[j] - xs[j - 1]))

    h = xs[i + 1] - xs[i]
    u = (f - xs[i]) / h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * vs[i] + (u ** 3 - 2 * u ** 2 + u) * h * m(i) + (-2 * u ** 3 + 3 * u ** 2) * vs[i + 1]
            + (u ** 3 - u ** 2) * h * m(i + 1))


def dung(k):
    """dựng rig dạng k: trả (sk, info)."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Dat = khung.Dat
    dm = os.path.join(d_inbox(k), "manh")
    dmat = os.path.join(d_inbox(1), "mat")
    mj = json.load(open(os.path.join(dm, "manh.json"), encoding="utf-8"))
    m1 = json.load(open(os.path.join(d_inbox(1), "manh", "manh.json"), encoding="utf-8"))
    b = mj["manh"]["than"]
    ox, oy = (b[0] + b[2]) / 2, b[3] - 4.0

    def R(x, y):
        return ((x - ox) * SC, (oy - y) * SC)

    def tam(box):
        return R((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)

    def nap(path, ti=SC):
        im = Image.open(path).convert("RGBA")
        im = im.resize((max(2, round(im.width * ti)), max(2, round(im.height * ti))), Image.LANCZOS)
        return anh.loang_mau(im)

    Wb, Hb = (b[2] - b[0] - 6) * SC, (b[3] - b[1] - 7) * SC
    e = mj["mat"]
    span = e[1]["x1"] - e[0]["x0"]
    span1 = m1["mat"][1]["x1"] - m1["mat"][0]["x0"]
    fc = R((e[0]["x0"] + e[1]["x1"]) / 2, (e[0]["y0"] + e[0]["y1"] + e[1]["y0"] + e[1]["y1"]) / 4)
    cao_mat = (e[0]["y1"] - e[0]["y0"]) * SC
    mc = R((e[0]["x1"] + e[1]["x0"]) / 2 + 12 * span / span1, mj["manh"]["ma"][3] + 48 * span / span1)
    giot = sorted([n for n in mj["manh"] if n.startswith("giot_")], key=lambda n: int(n.split("_")[1]))
    gc = np.array([tam(mj["manh"][n]) for n in giot])
    gr = np.array([(mj["manh"][n][2] - mj["manh"][n][0] - 6) * SC / 2 for n in giot])
    C = (gc * (gr ** 2)[:, None]).sum(0) / (gr ** 2).sum()                    # tâm cụm giọt (theo diện tích)

    sk = khung.Sk(f"{CODE}_{k}")
    sk.anh("than", nap(os.path.join(dm, "than.png")))
    sk.anh("ma", nap(os.path.join(dm, "ma.png")))
    sk.anh("mat_mo", nap(os.path.join(dm, "mat_mo.png")))
    fj = json.load(open(os.path.join(dmat, "mat.json"), encoding="utf-8"))
    for n in ("mat_nhan", "mat_xoay", "mat_cuoi", "mat_chop"):
        w0 = fj["manh"][n]["hop"][2] - fj["manh"][n]["hop"][0]
        sk.anh(n, nap(os.path.join(dmat, n + ".png"), SC * span / w0))
    for n in ("mieng_nho", "mieng_to"):
        sk.anh(n, nap(os.path.join(dmat, n + ".png"), SC * TI_MIENG * span / span1))
    for n in giot:
        sk.anh(n, nap(os.path.join(dm, n + ".png")))

    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("lon", "move", 0, Hb * 0.5)
    sk.xuong("day", "lon", 0, 0, the_gioi=True)
    sk.xuong("than", "day", 0, Hb * 0.42, the_gioi=True)
    sk.xuong("dinh", "than", 0, Hb * 0.45, goc=90, dai=Hb * 0.5, the_gioi=True)
    sk.xuong("mat", "than", *fc, the_gioi=True)
    sk.xuong("mom", "mat", *mc, the_gioi=True)
    sk.xuong("mieng", "mat", mc[0] + 4, mc[1], goc=0, dai=40, the_gioi=True)   # chỗ nhả cho VFX: trục x chĩa hướng nhả
    Jb = np.array([C[0] * 0.5, Hb * 0.9])
    can = sk.chuoi("can", "dinh", [Jb, (Jb + C) / 2, C])
    sk.xuong("cum", can[-1], *C, the_gioi=True)
    gb = []
    for i, n in enumerate(giot):
        gb.append(sk.xuong(f"g{i + 1}", "cum", *gc[i], the_gioi=True) or f"g{i + 1}")
    gb = [f"g{i + 1}" for i in range(len(giot))]

    sk.slot("than", "day", "than")
    sk.slot("ma", "mat", "ma")
    sk.slot("mat", "mat", "mat_mo")
    sk.slot("mieng", "mom", None)
    for i, n in enumerate(giot):
        sk.slot(n, gb[i], n)

    # thân: một lưới dày đều; trọng số theo chiều cao (Bernstein bậc hai: đáy bám day, giữa bám than, đỉnh bám dinh)
    im = sk.images["than"]
    H = float(max(gc[:, 1] + gr))                                             # chiều cao cả con (tới đỉnh giọt cao nhất)
    Lt = luoi.luoi_vung(im, buoc_vien=0.015 * H, buoc_trong=0.02 * H, ten=f"than {k}")
    dat_than = Dat(*tam(b))
    V = dat_than.ra(Lt.pts, im.width, im.height)
    Wt = []
    for x, y in V:
        u = min(1.0, max(0.0, y / Hb))
        d = {"day": (1 - u) ** 2, "than": 2 * u * (1 - u), "dinh": u * u}
        d = {q: w for q, w in d.items() if w > 0.004}
        s = sum(d.values())
        Wt.append({q: w / s for q, w in d.items()})
    sk.luoi_gan("than", "than", Lt, Wt, dat=dat_than)
    sk.manh("ma", "ma", Dat(*tam(mj["manh"]["ma"])))
    sk.manh("mat", "mat_mo", Dat(*tam(mj["manh"]["mat_mo"])))
    for n in ("mat_nhan", "mat_xoay", "mat_cuoi"):
        sk.manh("mat", n, Dat(*fc), ten=n)
    sk.manh("mat", "mat_chop", Dat(fc[0], fc[1] - 0.16 * cao_mat), ten="mat_chop")   # mí khép nằm ở nửa dưới con mắt
    for n in ("mieng_nho", "mieng_to"):
        sk.manh("mieng", n, Dat(*mc), ten=n)
    for i, n in enumerate(giot):
        sk.manh(n, n, Dat(*gc[i]))
    for ev, mo in (("trung", "đòn húc chạm đối thủ"), ("phun", "bắt đầu nhả nước (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                   ("bat", "chiêu cuối: rời đất, code bắt đầu cung nhảy"), ("cham_dat", "chiêu cuối: chạm đất / đầu đối thủ")):
        sk.su_kien(ev, mo)
    info = {"k": k, "Wb": Wb, "Hb": Hb, "H": H, "can": can, "gb": gb, "giot": giot, "gc": gc, "gr": gr, "C": C, "fc": fc, "mc": mc,
            "dinh_luoi": Lt.n, "ho": getattr(Lt, "ho", None)}
    return sk, info


def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Clip, LoXo, rung = hoat.Clip, hoat.LoXo, hoat.rung
    Wb, Hb, H, can, gb = info["Wb"], info["Hb"], info["H"], info["can"], info["gb"]
    KX, KY = Wb / REF_W, Hb / REF_H
    ch = CHAM[k]
    F = 30.0 / ch                                                             # khung (của bản thiết kế) mỗi giây
    slots = [s["name"] for s in sk.slots]
    gl = [(sk.bones[sk.bi[g]]["x"], sk.bones[sk.bi[g]]["y"]) for g in gb]      # chỗ từng giọt trong hệ xương cum
    A0 = sk.W0[can[-1]][:2, :2]

    def tg_cum(dx, dy):
        """độ dời thế giới -> độ dời trong hệ cha của xương cum (dáng gốc)."""
        v = np.linalg.solve(A0, np.array([dx, dy], float))
        return float(v[0]), float(v[1])

    def mem():
        if len(gb) > 2:                                                       # vương miện rộng: cần cứng hơn, kẻo giọt hai đầu quệt vào vòm
            return [LoXo(["dinh"], k=[240], damp=0.42, maxang=9), LoXo(can, k=[330, 270], damp=0.6, maxang=7)]
        return [LoXo(["dinh"], k=[240], damp=0.42, maxang=9), LoXo(can, k=[170, 120], damp=0.4, maxang=30)]

    def giot_quay(P, pha):
        """giọt con lúc nghỉ: dạng 1 cả cụm quay quanh tâm (giọt giữ thẳng), dạng 2 nhấp nhô lượn sóng. pha tính bằng vòng."""
        a = 2 * math.pi * pha
        if len(gb) <= 2:
            c, sn = math.cos(-a), math.sin(-a)                                # quay thuận kim; dời từng giọt quanh tâm cụm (giọt giữ thẳng)
            for g, (lx, ly) in zip(gb, gl):
                P.move(g, c * lx - sn * ly - lx, sn * lx + c * ly - ly)
            P.move("cum", *tg_cum(0, 0.05 * H * (1 - math.cos(a)) / 2))       # nhấc cụm lên khi giọt nhỏ vòng xuống dưới
        else:
            for i, g in enumerate(gb):
                ph = 1.1 * i
                v = 0.022 * H * (math.sin(a * 2 - ph) - math.sin(-ph))
                m = 0.012 * H                                                 # xuống tối đa chừng này: giọt không chạm vòm
                P.move(g, *tg_cum(0, v if v >= 0 else -m * math.tanh(-v / m)))
            P.rot(can[0], 1.5 * math.sin(a))

    def mat(P, ten):
        if ten != "mat_mo":
            P.att["mat"] = ten

    def an_het(P, a):
        for s in slots:
            P.alpha[s] = a

    # ---------------- idle: 2 vòng idle_01 của con gốc (40 khung mỗi vòng), vòng hai có chớp mắt
    def idle_fn(t, P):
        fa = t * F
        f = fa % 40
        P.scale("day", spl(f, [(0, 1), (5, .963), (8, .926), (10, .913), (16, 1.07), (21, .966), (25, 1), (35, .913)], 40),
                spl(f, [(0, 1), (5, 1.02), (8, 1.05), (10, 1.06), (16, .894), (21, 1.04), (25, 1), (35, 1.06)], 40))
        P.move("than", KX * ln(f, [(0, 0), (8, 0), (16, 22.3), (35, -5.13), (40, 0)]),
               KY * ln(f, [(0, 0), (2, -10.4), (5, 16.7), (8, 0), (40, 0)]))
        P.scale("than", 1, ln(f, [(0, 1), (2, 1.13), (5, .859), (8, 1), (40, 1)]))
        P.move("mat", KX * spl(f, [(0, 0), (6, -35.9), (23, -26.4), (35, -2.88)], 40), KY * spl(f, [(0, 0), (6, 0), (23, 7.78), (35, 0)], 40))
        giot_quay(P, fa / 40.0)
        if 52 <= fa < 55.5:
            mat(P, "mat_chop")

    # ---------------- appear: rơi từ trên xuống, bẹp, nảy (nửa sau hit_02 của con gốc)
    def appear_fn(t, P):
        f = t * F
        an_het(P, ln(f, [(0, 0), (2, 1)]))
        P.move("lon", 0, 2.7 * Hb * (1 - min(1.0, f / 7.0) ** 2))
        P.scale("day", ln(f, [(0, .78), (7, .74), (8.5, 1.5), (10, 1.42), (12, .93), (14, 1.08), (17, .96), (20, 1.03), (23, 1)]),
                ln(f, [(0, 1.28), (7, 1.36), (8.5, .6), (10, .66), (12, 1.1), (14, .9), (17, 1.06), (20, .98), (23, 1)]))
        P.move("day", 0, KY * ln(f, [(0, 0), (10, 0), (12, 26), (14, 0), (17, 6), (20, 0)]))
        P.move("than", 0, KY * ln(f, [(0, 0), (7, 12), (8.5, -26), (11, 14), (14, -5), (18, 0)]))
        mat(P, "mat_nhan" if f < 10 else ("mat_cuoi" if f < 18 else "mat_mo"))

    # ---------------- attack: húc đầu (skill_01 của con gốc; cú lao 3 khung nằm trên xương move để sân kéo tới đối thủ)
    def attack_fn(t, P):
        f = t * F
        P.rot("day", ln(f, [(0, 0), (9, -.33), (12, 1.5), (16, 1.5), (19, 7.22), (22, 0)]))
        P.scale("day", ln(f, [(0, 1), (9, .513), (12, 1.3), (16, 1.3), (17, .787), (19, .82), (22, .806), (24, 1.08), (27, .896), (30, 1.1), (32, 1)]),
                ln(f, [(0, 1), (9, 1.74), (12, .666), (16, .666), (17, 1.61), (19, .926), (22, 1.21), (24, .677), (27, 1), (30, .92), (32, 1)]))
        P.move("day", 0.7 * KX * ln(f, [(0, 0), (19, 0), (22, -19.4), (24, -19.4), (27, -5.66), (30, 0)]),
               KY * ln(f, [(0, 0), (16, 0), (17, 2.5), (19, 60.9), (22, 0), (24, 0), (27, 24.3), (30, 0)]))
        P.move("move", 0.42 * H * ln(f, [(0, 0), (9, 0), (10, .22), (11, .6), (12, 1), (16, 1), (17, .915), (19, .745), (22, 0)]), 0)
        P.rot("than", ln(f, [(0, 0), (3, 1.69), (9, 5.43), (12, -23.5), (16, -23.5), (19, -3.3), (22, 0)]))
        P.move("than", KX * ln(f, [(0, 0), (3, -74.3), (9, -54.3), (12, 105), (14, 44.9), (16, 41.8), (19, -25.6), (22, 0)]),
               KY * ln(f, [(0, 0), (3, 29), (9, -35.1), (12, -25), (14, -21.9), (16, -21.7), (19, 43.8), (22, 0)]))
        P.scale("than", ln(f, [(0, 1), (3, 1.45), (9, 1.41), (12, 1.35), (16, 1), (32, 1)]), ln(f, [(0, 1), (3, .88), (9, .731), (12, 1), (16, 1.18), (22, 1)]))
        if 9 <= f < 19.5:
            mat(P, "mat_nhan")

    # ---------------- cast: co lại + cao lên, há miệng bắn nước, bắn xong mới ngậm
    # Dòng nước của game (HatNuoc.NTia) nhả đúng lúc `phun` và chảy 0,88 s thật: miệng phải há suốt quãng đó rồi mới ngậm, nên
    # đoạn giữ tính bằng GIÂY (không co theo CHAM). E = khung thiết kế lúc hết nhả; các khoá sau đó dời theo d.
    NHA = 0.94
    E = 13.5 + NHA * F
    d = E - 28

    def cast_fn(t, P):
        f = t * F
        r = rung(t, 13.5 / F, E / F)
        P.scale("day", spl(f, [(0, 1), (5, 1.1), (9, .93), (13, .8), (15, .84), (E, .84), (32 + d, 1.08), (35.5 + d, .97), (40 + d, 1)]),
                spl(f, [(0, 1), (5, .88), (9, 1.1), (13, 1.27), (15, 1.2), (E, 1.2), (32 + d, .92), (35.5 + d, 1.03), (40 + d, 1)]))
        P.rot("day", spl(f, [(0, 0), (9, 0), (13, -2), (15, 4), (E, 3.2), (32 + d, -1), (36 + d, 0), (40 + d, 0)]))
        P.move("than", KX * (spl(f, [(0, 0), (9, 0), (12.5, 4), (14, -9), (15, -10), (E, -8), (32 + d, 2), (36 + d, 0), (40 + d, 0)]) + 1.5 * r), 0)
        P.move("mat", KX * spl(f, [(0, 0), (9, -6), (13, -3), (E, -3), (33 + d, 0), (40 + d, 0)]), 0)
        # miệng: chấm nhỏ hiện ra sớm (lúc nước đang tụ trước miệng), lớn dần, há to đúng lúc nhả; hết nước mới co lại rồi biến
        if 5 <= f < 11:
            P.att["mieng"] = "mieng_nho"
            g = ln(f, [(5, .3), (8, .8), (11, 1.15)])
            P.scale("mom", g, g)
        elif 11 <= f < E + 2:
            P.att["mieng"] = "mieng_to"
            g = ln(f, [(11, .5), (13, 1.08), (14.5, 1), (E, 1), (E + 2, .5)]) * (1 + 0.035 * r)
            P.scale("mom", g * (1 + 0.02 * r), g)
        elif E + 2 <= f < E + 4.5:
            P.att["mieng"] = "mieng_nho"
            g = ln(f, [(E + 2, 1.1), (E + 4.5, .3)])
            P.scale("mom", g, g)
        if 2 <= f < 6:
            mat(P, "mat_chop")
        elif 11 <= f < E + 3:
            mat(P, "mat_nhan")

    # ---------------- skill: phình to, nhún, bật lên (nửa đầu skill_02); kết thúc ở dáng đang bay, code nhấc lên theo cung
    G = 1.27                                                                  # độ phình
    BAY = (0.88, 1.14)                                                        # dáng đang bay: cuối skill = đầu skill_land

    def skill_fn(t, P):
        f = t * F
        g = spl(f, [(0, 1), (4, 1.13), (7, 1.08), (11, 1.31), (14, G), (36, G)])
        r = rung(t, 4 / F, 13 / F)
        P.scale("day", g * ln(f, [(0, 1), (14, 1), (20, 1.14), (22, 1.2), (24, .7), (25, .6), (28, .8), (32, .92), (36, BAY[0])]) * (1 + 0.012 * r),
                g * ln(f, [(0, 1), (14, 1), (20, .74), (22, .66), (24, 1.42), (25, 1.62), (28, 1.24), (32, 1.1), (36, BAY[1])]) * (1 - 0.012 * r))
        P.move("than", 0, KY * ln(f, [(0, 0), (14, 0), (22, -22), (25, 20), (28, 0), (36, 0)]))
        P.scale("than", 1, ln(f, [(0, 1), (14, 1), (22, .95), (25, 1.15), (28, 1), (36, 1)]))
        if 6 <= f < 9:
            mat(P, "mat_chop")
        elif f >= 17:
            mat(P, "mat_nhan")

    # ---------------- skill_land: rơi xuống, bẹp nặng, nảy thấp, xẹp về cỡ thường (nửa sau skill_02, nặng hơn)
    def land_fn(t, P):
        f = t * F
        g = spl(f, [(0, G), (8, G), (14, 1.1), (20, 1), (26, 1)])
        P.scale("day", g * ln(f, [(0, BAY[0]), (3, .8), (4, 1.2), (5, 1.62), (8, 1.55), (11, .93), (14, 1.1), (17, .97), (21, 1.02), (26, 1)]),
                g * ln(f, [(0, BAY[1]), (3, 1.26), (4, .8), (5, .5), (8, .55), (11, 1.1), (14, .9), (17, 1.04), (21, .99), (26, 1)]))
        P.move("day", 0, KY * ln(f, [(0, 0), (8, 0), (11, 14), (14, 0), (26, 0)]))
        P.move("than", 0, KY * ln(f, [(0, 0), (3, 10), (5, -34), (8, -24), (11, 16), (14, -6), (18, 0), (26, 0)]))
        if f < 10:
            mat(P, "mat_nhan")

    # ---------------- hit: hit_01 của con gốc (lùi 1 khung để khung 0 là dáng nghỉ); mặt không trượt ra ngoài thân
    def hit_fn(t, P):
        f = t * F
        P.rot("day", ln(f, [(0, 0), (1, 26), (3, 3.9), (5, 12.7), (8, -.63), (10, -6.39), (12, -2.6), (16, 0)]))
        P.move("day", KX * ln(f, [(0, 0), (1, 20), (3, -53.1), (5, -21.6), (8, -15.2), (10, 0), (16, 0)]),
               KY * ln(f, [(0, 0), (5, 1.5), (8, 0), (10, 16.1), (12, 1.79), (16, 0)]))
        P.scale("day", ln(f, [(0, 1), (1, .56), (3, .52), (5, .46), (8, 1.04), (10, 1), (12, .955), (16, 1)]),
                ln(f, [(0, 1), (1, 1.5), (3, .6), (5, 1.12), (8, .739), (10, 1), (12, 1.08), (16, 1)]))
        P.rot("than", ln(f, [(0, 0), (1, 0), (3, 17.2), (5, 3.46), (8, -12.1), (10, 0), (16, 0)]))
        P.move("than", KX * ln(f, [(0, 0), (1, 0), (3, -65), (5, -23.6), (10, 0), (13, -.5), (16, 0)]),
               KY * ln(f, [(0, 0), (1, 0), (3, 152), (5, 57.4), (10, 0), (13, 13.2), (16, 0)]))
        P.scale("than", ln(f, [(0, 1), (1, 1), (3, 2.2), (5, 2.0), (8, 1.46), (13, .969), (16, 1)]),
                ln(f, [(0, 1), (1, 1), (3, 1.83), (5, 1.39), (8, 1.53), (13, 1.22), (16, 1)]))
        P.move("mat", KX * ln(f, [(0, 0), (1, -70), (3, -40), (10, 5), (16, 0)]), KY * ln(f, [(0, 0), (1, 0), (3, -20), (10, 0), (16, 0)]))
        if 0.5 <= f < 10.5:
            mat(P, "mat_nhan")

    # ---------------- die: die_01 của con gốc (lùi 2 khung), chảy xẹp thành vũng rồi tan
    def die_fn(t, P):
        f = t * F
        P.rot("day", ln(f, [(0, 0), (2, 16.3), (5, -2.56), (9, -8), (12, .848), (32, 2.34), (44, 2.34)]))
        P.move("day", KX * ln(f, [(0, 0), (2, -97.3), (5, 0), (44, 0)]), KY * ln(f, [(0, 0), (2, 17.3), (5, 0), (44, 0)]))
        P.scale("day", ln(f, [(0, 1), (2, .969), (5, .799), (9, 1.55), (12, 1), (32, 1), (44, 1.14)]),
                ln(f, [(0, 1), (2, 1.01), (5, 1.31), (9, .625), (12, 1), (32, 1.11), (44, .86)]))
        P.rot("than", ln(f, [(0, 0), (2, -3.72), (5, 23.3), (12, 0), (44, 0)]))
        P.move("than", KX * ln(f, [(0, 0), (2, 33.8), (5, -4.07), (12, 0), (32, -4.06), (44, -4.06)]),
               KY * ln(f, [(0, 0), (2, -53.3), (5, 45.8), (12, 0), (32, -99.2), (44, -110)]))
        P.scale("than", ln(f, [(0, 1), (2, 1.46), (5, 1), (12, 1), (32, 1.62), (44, 1.74)]), ln(f, [(0, 1), (2, 1.36), (5, 1), (44, 1)]))
        P.move("mat", KX * ln(f, [(0, 0), (2, -70), (5, 0), (12, 0), (32, .976), (44, 1)]), KY * ln(f, [(0, 0), (12, 0), (32, 38.7), (44, 42)]))
        sxm = ln(f, [(0, 1), (2, 1.46), (5, 1), (12, 1), (32, 1.62), (44, 1.74)])
        P.scale("mat", 1 / sxm ** 0.75, 1)
        mat(P, "mat_nhan")
        if f > 32:
            an_het(P, ln(f, [(32, 1), (43, 0), (44, 0)]))

    return [Clip("appear", 24 / F, appear_fn, mem=mem()),
            Clip("idle", 80 / F, idle_fn, loop=True, mem=mem()),
            Clip("attack", 32 / F, attack_fn, ev=[(12 / F, "trung", "")], mem=mem()),
            Clip("cast", (40 + d) / F, cast_fn, ev=[(13.5 / F, "phun", ""), (E / F, "het_phun", "")], mem=mem()),
            Clip("skill", 36 / F, skill_fn, ev=[(25 / F, "bat", "")], trung=25 / F, mem=mem()),
            Clip("skill_land", 26 / F, land_fn, ev=[(4.5 / F, "cham_dat", "")], trung=4.5 / F, mem=mem()),
            Clip("hit", 16 / F, hit_fn, mem=mem()),
            Clip("die", 44 / F, die_fn, mem=mem())]


def ngoai_than(sk, ve, P, s=0.5, le=4.0):
    """diện tích (px rig vuông) của mặt, má, miệng nằm ngoài thân (thân co vào `le` px: không đè nét mực viền); kèm hướng đẩy vào."""
    W = sk.the_gioi(P)
    items, _ = ve.skin(P, W)
    than = next((it for it in items if it[0] == "than"), None)
    mat_ = [it for it in items if it[0] in ("ma", "mat", "mieng") and it[5] > 0.02]
    if than is None or not mat_ or than[5] < 0.02:
        return 0.0, None, W
    V = than[2]
    allv = np.vstack([V] + [it[2] for it in mat_])
    x0, y1 = allv[:, 0].min() - 8, allv[:, 1].max() + 8
    wc, hc = int((allv[:, 0].max() + 8 - x0) * s) + 2, int((y1 - allv[:, 1].min() + 8) * s) + 2

    def tf(Q):
        return np.stack([(Q[:, 0] - x0) * s, (y1 - Q[:, 1]) * s], 1)

    body = np.zeros((hc, wc), np.uint8)
    D = np.round(tf(V) * 8).astype(np.int32)
    cv2.fillPoly(body, [D[t] for t in than[4]], 1, shift=3)
    r = max(1, int(round(le * s)))
    body_in = cv2.erode(body, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
    out = np.zeros((hc, wc), bool)
    for nm, an, Vq, uv, tris, a, path, si in mat_:
        im = sk.images[path]
        al = np.ascontiguousarray(np.asarray(im)[..., 3])
        src = np.float32([[0, 0], [im.width, 0], [0, im.height]])
        dq = tf(Vq)
        M = cv2.getAffineTransform(src, np.float32([dq[0], dq[1], dq[3]]))
        m = cv2.warpAffine(al, M, (wc, hc), flags=cv2.INTER_LINEAR) > 110
        out |= m & (body_in == 0)
    n = int(out.sum())
    if not n:
        return 0.0, None, W
    ys, xs = np.nonzero(out)
    by, bx = np.nonzero(body_in) if body_in.any() else np.nonzero(body)
    if not len(bx):
        return n / (s * s), None, W
    d = np.array([bx.mean() - xs.mean(), -(by.mean() - ys.mean())])        # hướng đẩy (thế giới, y lên): từ chỗ thò ra về tâm thân
    nn = float(np.hypot(*d))
    return n / (s * s), (d / nn if nn > 1e-6 else None), W


def ep_mat(sk, frames, ten=""):
    """ép mặt (mắt, má, miệng) nằm trong thân ở mọi khung: đẩy xương mat về tâm thân từng bước; vẫn thò thì co mặt lại.
    Sau đó làm trơn độ chỉnh theo thời gian để mặt không giật. Trả (số khung phải chỉnh, diện tích thò ra nhiều nhất trước, sau)."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    ve = soi.Ve(sk)
    n = len(frames)
    adj = np.zeros((n, 3))                                                    # dx, dy (hệ cha của mat), log tỉ lệ
    truoc = 0.0
    for i, P in enumerate(frames):
        c0, d, W = ngoai_than(sk, ve, P)
        truoc = max(truoc, c0)
        if c0 <= 0:
            continue
        Q = P.copy()
        dx = dy = 0.0
        sc = 1.0
        for it in range(90):
            c, d, W = ngoai_than(sk, ve, Q)
            if c <= 0 or d is None:
                break
            if it % 12 == 11 and sc > 0.45:                                   # đẩy mãi chưa lọt: thân lúc này hẹp hơn mặt -> co mặt
                sc *= 0.9
            st = np.linalg.solve(W["than"][:2, :2], d * 2.5)
            dx, dy = dx + st[0], dy + st[1]
            Q = P.copy()
            Q.move("mat", dx, dy)
            Q.scale("mat", sc, sc)
        adj[i] = (dx, dy, math.log(sc))
    if np.abs(adj).sum() > 0:
        k = np.array([1, 2, 3, 2, 1], float) / 9
        sm = np.stack([np.convolve(np.pad(adj[:, j], 2, mode="edge"), k, mode="valid") for j in range(3)], 1)
        fin = np.where(np.abs(sm) > np.abs(adj), sm, adj)                     # không chỉnh ÍT hơn mức cần, chỉ thêm đoạn vào/ra êm
        for i, P in enumerate(frames):
            if np.abs(fin[i]).sum() > 1e-6:
                P.move("mat", float(fin[i, 0]), float(fin[i, 1]))
                e = math.exp(float(fin[i, 2]))
                P.scale("mat", e, e)
    sau = max((ngoai_than(sk, ve, P)[0] for P in frames), default=0.0)
    so = int((np.abs(adj).sum(1) > 0).sum())
    print(f"  ép mặt {ten}: {so}/{n} khung phải chỉnh; thò ra nhiều nhất {truoc:.0f} px2 -> {sau:.0f} px2")
    return so, truoc, sau


def nuong_het(sk, cl):
    """nướng mọi clip; clip kết thúc ở dáng nghỉ thì hoà phần lò xo còn dư về khung 0 idle (skill kết thúc trên không: để nguyên)."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    for c in cl:
        if not c.loop and c.ten not in ("die", "evolve", "skill"):
            hoat.khop_cuoi(fr[c.ten], fr["idle"][0], 0.2)
    for c in cl:
        ep_mat(sk, fr[c.ten], c.ten)
    return fr


def to_nhay(sk, fr, ra, info):
    """tờ xem thử chiêu cuối: skill + cung nhảy giả (thay cho code của game) + skill_land, đặt trên một dải."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    H = info["H"]
    a, b = fr["skill"], fr["skill_land"]
    i0 = next(i for i in range(len(a)) if i / 30.0 >= 25 / 30.0 * CHAM[info["k"]])     # khung `bat`
    seq = [P.copy() for P in a[:i0]]
    bay = [P.copy() for P in a[i0:]] + [a[-1].copy() for _ in range(6)] + [b[0].copy(), b[1].copy(), b[2].copy(), b[3].copy()]
    n = len(bay)
    for j, P in enumerate(bay):
        u = j / (n - 1.0)
        P.move("move", 1.5 * H * u, 1.6 * H * 4 * u * (1 - u))
    dat = [P.copy() for P in b[4:]]
    for P in dat:
        P.move("move", 1.5 * H, 0)
    seq += bay + dat
    ve = soi.Ve(sk)
    pick = [0, 8, 12, 17, 21, 23, i0, i0 + 3, i0 + 8, i0 + 13, i0 + n - 3, i0 + n, i0 + n + 1, i0 + n + 3, i0 + n + 7, i0 + n + 12, len(seq) - 1]
    pick = [min(len(seq) - 1, p) for p in pick]
    box = (-0.75 * H, -0.08 * H, 2.4 * H, 2.75 * H)
    s = 0.42
    tiles = [ve.ve(seq[p], box, s, bg=(150, 150, 150), ss=2) for p in pick]
    w, h = tiles[0].size
    cot = 6
    to = Image.new("RGB", (w * cot, h * ((len(tiles) + cot - 1) // cot)), (60, 60, 60))
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    for i, (p, im) in enumerate(zip(pick, tiles)):
        im = im.convert("RGB")
        ImageDraw.Draw(im).text((8, 6), f"khung {p}  ({p / 30.0:.2f} s)", fill=(255, 255, 255), font=f)
        to.paste(im, ((i % cot) * w, (i // cot) * h))
    to.save(ra)
    return ra


def rig(k, tien_hoa=None):
    """dựng, nướng, xuất dạng k vào inbox/ti_tach_<k>/rig/. tien_hoa = (sk2, info2, fr2, cl2): gộp dạng sau cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = nuong_het(sk, cl)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    ve = soi.Ve(sk)
    h_that = soi.chieu_cao(ve, fr["idle"][0])
    cao = h_that * CAO_HIEU[k]
    ten = f"{CODE}_{k}"
    noi = {}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        h2 = soi.chieu_cao(soi.Ve(sk2), fr2["idle"][0]) * CAO_HIEU[2]
        ti = cao / h2
        M = tienhoa.gop(sk, sk2)
        Hb = info["Hb"]

        def gong(t, P):                                                       # dạng cũ phình dần, rung, mắt nhắm chặt
            g = hoat.cv(t, [(0, 1), (0.3, 0.92), (0.6, 1.12, "out"), (1.0, 1.3), (1.3, 1.42)])
            r = hoat.rung(t, 0.45, 1.3)
            P.scale("day", g * (1 + 0.02 * r), g * (1 - 0.02 * r))
            if t > 0.25:
                P.att["mat"] = "mat_nhan"

        def bung(t, P, fl):                                                   # dạng sau hiện ra: nảy bẹp một nhịp, mắt cười
            sq = hoat.cv(t, [(0, 0), (1.5, 0), (1.75, 1, "out"), (2.0, -0.45, "io"), (2.25, 0.2, "io"), (2.45, 0, "io"), (2.8, 0)])
            P.scale("n_day", 1 + 0.22 * sq, 1 - 0.2 * sq)
            if 1.5 < t < 2.3:
                P.att["n_mat"] = "n_mat_cuoi"

        memM = cl[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=bung, mem=memM)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
    tk = xuat.xuat_het(M, clM, ra, ten, f"Tí Tách dạng {k}", frames=frM, dang=k, so_dang=2, dung_yen=("cast", "skill", "skill_land"),
                       cao=cao, khop_idle=0, noi_them=noi,
                       tol={"rotate": 0.08, "translate": 0.15, "scale": 0.001},
                       can=[("can_mieng_cast", "cast", 0.9, "mom", 0.2 * info["H"]),
                            ("can_huc", "attack", 12 / 30.0 * CHAM[k], "than", 0.6 * info["H"]),
                            ("can_bep", "skill_land", 6 / 30.0 * CHAM[k], "than", 0.7 * info["H"])])
    to_nhay(sk, fr, os.path.join(ra, "xem_nhay.png"), info)
    print(f"dạng {k}: thân {info['dinh_luoi']} đỉnh, cao thật {h_that:.0f} px rig, game.height {cao:.0f}; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["cat"]:
        for k in ([int(a[1])] if len(a) > 1 else [1, 2]):
            cat(k)
    elif a[:1] == ["mat"]:
        cat_mat()
    elif a[:1] == ["rig"]:
        rig(int(a[1]))
    elif a[:1] == ["all"]:
        r2 = rig(2)
        rig(1, tien_hoa=r2)
    else:
        print(__doc__)
