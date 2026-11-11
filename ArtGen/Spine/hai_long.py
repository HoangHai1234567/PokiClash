"""Hải Long Ngũ Đầu (dạng 3 của dòng Hải Long, boss cuối đảo Thủy): cắt mảnh từ bảy tờ GPT, dựng rig Spine 4.2 (JSON + atlas + PNG),
7 clip tên game (appear, idle, attack, cast = phun nước, skill = gầm, hit, die) và clip `aura` (nước dưới chân, lặp riêng, phát chồng
lên mọi clip: AtomikPose.Overlay). Gói prompt: build_hai_long.py. Cách dựng, trọng số lưới và các luật nhịp học từ bài mổ xẻ
.claude/skills/skill-petclash/mo_xe_quai_nhieu_dau.md (mục 3b, 6b, 9); cách làm: skill pokiclash-spine-rig mục 20.
Bản 4 (2026-11-11, lô 10 tướng mới đảo Thủy, đặc tả ArtGen/Spine/quai/DAC_TA_LO_THUY.md): lưới dày, mịn, gần đều cạnh (cổ 3 cột mỗi
đốt × 7 hàng, đầu 14×10, sóng 8×8, dải nước 4 hàng, vòng thân 13×8), hàm dưới là lưới hai xương như con gốc (họng theo đầu, cằm theo
hàm), nước tách thành clip `aura`. KHÔNG tự chép .atomik sang Assets (Claude điều phối làm bước vào game).
  - mỗi khung chỉ cho vị trí, góc, độ há của từng ĐẦU; cổ 14 đốt giải theo đường cong từ chỗ trồi tới gáy, phần thừa trượt thẳng
    xuống dưới nước (mặt nạ cắt che); thêm sóng uốn chạy dọc cổ (đầu không xê dịch);
  - mọi dải lưới (cổ, râu, đuôi, lưỡi) chia trọng số kiểu B-spline bậc hai: không đỉnh nào bám cứng một đốt nên thân cong trơn;
  - râu 6 đốt và lưỡi 5 đốt mô phỏng dây mềm rồi nướng (rope); bờm trễ theo đầu; vòng thân là lưới 5 điểm điều khiển lệch pha;
  - thịt trong miệng đi theo hàm dưới (há theo hàm), chỉ một màng ở khoé miệng nối lên đầu; mí mắt dò cho phủ
    kín con mắt (chớp, nhắm lúc trúng đòn, chết);
  - nước nền: 23 cuộn sóng × 2 bản sao lệch nửa chu kỳ, mỗi cuộn là lưới bám chuỗi 4 đốt trên sống lưng sóng: dâng tại chỗ, mào
    tự cuộn lại, trôi nhẹ, tan (không trượt ngang); dải mặt nước và dải gợn sóng uốn theo 8 xương; nước phản ứng: đầu trồi, bổ,
    chìm thì toé đúng chỗ;
  - tia, đạn, vụ nổ của chiêu KHÔNG nằm trong rig (việc của VFX): rig để lại xương mieng_<đầu> và sự kiện phun / het_phun / can /
    gam / het_gam / troi / roi_nuoc.

    py -3 -I hai_long.py cat         cắt inbox/hai_long/tai_ve/M01..M07.png thành inbox/hai_long/manh/<tên>.png
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I hai_long.py rig
                                     dựng inbox/hai_long/rig/hai_long.json|.atlas|.png, xem.html (trang xem một file, aura chạy
                                     track 1), hai_long.atomik + hai_long_game.json (định dạng của game; KHÔNG chép vào Assets)
Soi (tờ khung có aura, lưới, so sánh, chân dung): hai_long_soi.py. Mảnh chưa có thì dùng hình giữ chỗ.
"""
import json
import math
import zlib
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "inbox", "hai_long")
TAI = os.path.join(INBOX, "tai_ve")
MANH = os.path.join(INBOX, "manh")
RIG = os.path.join(INBOX, "rig")
NAME = "hai_long"
SC = 0.8      # tỉ lệ mảnh trong atlas so với tờ GPT (đơn vị rig = pixel atlas)
FPS = 30
TW = 1.6      # chu kỳ băng chuyền sóng (giây)
CLIPY = 112   # mép dưới của mặt nạ cắt (mặt nước)
PALETTE = True                                                        # lưu atlas dạng bảng 256 màu
UNUSED = {"tuft", "jet_k", "jet_n", "burst", "flare", "streak_a", "streak_b", "streak_c"}  # tia nước, vụ nổ: để dành cho VFX, không vào rig                                                     # mảnh có trên tờ nhưng rig không dùng
PSC = {"tongue_k": 0.62, "tongue_n": 0.62, "drop_a": 0.4, "drop_b": 0.4, "drop_c": 0.4, "mouth": 0.6, "mound": 0.8}  # mảnh lưu nhỏ hơn trong atlas

# ---------------------------------------------------------------- 1. cắt mảnh
# tên mảnh: (tờ, cỡ giữ chỗ trên tờ GPT, màu giữ chỗ)
PIECES = {
    "head_k": ("M01", (430, 330), (47, 167, 155)), "jaw_k": ("M01", (330, 120), (242, 217, 160)), "mouth": ("M01", (240, 170), (184, 64, 90)),
    "head_n": ("M01", (380, 280), (47, 167, 155)), "jaw_n": ("M01", (290, 105), (242, 217, 160)),
    "whisker": ("M01", (360, 60), (244, 238, 220)), "tuft": ("M01", (200, 130), (224, 86, 60)),
    "neck_k": ("M02", (1380, 190), (47, 167, 155)), "neck_n": ("M02", (1380, 140), (47, 167, 155)),
    "coil": ("M02", (520, 300), (47, 167, 155)), "tail": ("M02", (520, 190), (47, 167, 155)),
    "wave_a": ("M03", (400, 400), (58, 150, 226)), "wave_b": ("M03", (430, 360), (58, 150, 226)), "wave_c": ("M03", (400, 300), (58, 150, 226)),
    "wave_d": ("M03", (260, 230), (58, 150, 226)), "wave_e": ("M03", (440, 170), (58, 150, 226)), "foam": ("M03", (300, 220), (244, 252, 255)),
    "band": ("M04", (1400, 230), (58, 150, 226)), "mound": ("M04", (820, 250), (30, 104, 190)), "crown": ("M04", (480, 300), (140, 208, 246)),
    "drop_a": ("M04", (60, 90), (58, 150, 226)), "drop_b": ("M04", (50, 70), (58, 150, 226)), "drop_c": ("M04", (36, 50), (58, 150, 226)),
    "ring": ("M04", (520, 130), (58, 150, 226)),
    "jet_k": ("M05", (1380, 170), (58, 150, 226)), "jet_n": ("M05", (1380, 105), (58, 150, 226)),
    "burst": ("M05", (470, 400), (58, 150, 226)), "flare": ("M05", (230, 260), (58, 150, 226)),
    "streak_a": ("M05", (170, 60), (58, 150, 226)), "streak_b": ("M05", (130, 50), (58, 150, 226)), "streak_c": ("M05", (95, 40), (58, 150, 226)),
    "lid_k": ("M05", (120, 78), (47, 167, 155)), "lid_n": ("M05", (100, 64), (47, 167, 155)),
    "tongue_k": ("M06", (320, 64), (226, 124, 146)), "tongue_n": ("M06", (260, 52), (226, 124, 146)),
    "sweep": ("M07", (1000, 200), (58, 150, 226)), "curl_s1": ("M07", (180, 190), (58, 150, 226)),
    "tend_a": ("M07", (130, 400), (58, 150, 226)), "tend_b": ("M07", (170, 320), (58, 150, 226)),
    "curl_s2": ("M07", (230, 230), (58, 150, 226)), "curl_s3": ("M07", (150, 150), (58, 150, 226)),
    "ripple": ("M07", (1300, 120), (140, 208, 246)),
}


def sheet_path(sc):
    """ảnh GPT mới nhất của một bước (M01.png, M01_2.png ...)."""
    import glob
    fs = sorted(glob.glob(os.path.join(TAI, sc + "*.png")), key=os.path.getmtime)
    return fs[-1] if fs else None


def components(path, min_area=900):
    """các mảnh rời trên nền trắng: trả [(x0, y0, x1, y1, mask)] và ảnh RGBA cả tờ (nền trong suốt, mép mềm)."""
    rgb = np.asarray(Image.open(path).convert("RGB"))
    h, w = rgb.shape[:2]
    light = (rgb.min(axis=2) > 236).astype(np.uint8)
    ff = np.zeros((h + 2, w + 2), np.uint8)
    bg = light.copy()
    for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if bg[y, x] == 1:
            cv2.floodFill(bg, ff, (x, y), 2)
    fg = (bg != 2).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
    big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= min_area]
    out = []
    for i in big:
        x, y, ww, hh = st[i, 0], st[i, 1], st[i, 2], st[i, 3]
        out.append([x, y, x + ww, y + hh, lab == i])
    # mẩu nhỏ sát mảnh lớn (< 40 px) nhập vào mảnh đó
    for i in range(1, n):
        if i in big or st[i, cv2.CC_STAT_AREA] < 30:
            continue
        x, y, ww, hh = st[i, 0], st[i, 1], st[i, 2], st[i, 3]
        best, bd = None, 40
        for o in out:
            dx = max(o[0] - (x + ww), x - o[2], 0)
            dy = max(o[1] - (y + hh), y - o[3], 0)
            if max(dx, dy) < bd:
                best, bd = o, max(dx, dy)
        if best is not None:
            best[4] = best[4] | (lab == i)
            best[0], best[1], best[2], best[3] = min(best[0], x), min(best[1], y), max(best[2], x + ww), max(best[3], y + hh)
    alpha = cv2.GaussianBlur(cv2.erode(fg, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.1)
    rgba = np.dstack([rgb, (np.clip(alpha * 1.25, 0, 1) * 255).astype(np.uint8)])
    return out, rgba


def assign(sc, comps, w, h):
    """gán tên cho các mảnh của một tờ theo bố cục đã dặn GPT."""
    cx = lambda c: (c[0] + c[2]) / 2
    cy = lambda c: (c[1] + c[3]) / 2
    area = lambda c: int(c[4].sum())
    names = {}
    if sc == "M01":
        grid = [["head_k", "jaw_k", "mouth"], ["head_n", "jaw_n", None]]
        last = []
        for c in comps:
            col, row = min(2, int(cx(c) / (w / 3))), min(1, int(cy(c) / (h / 2)))
            nm = grid[row][col]
            if nm is None:
                last.append(c)
            elif nm not in names or area(c) > area(names[nm]):
                names[nm] = c
        last.sort(key=cy)
        if len(last) >= 2:
            names["whisker"], names["tuft"] = last[0], last[-1]
        elif last:
            names["whisker"] = last[0]
    elif sc == "M02":
        rows = sorted(comps, key=cy)
        wide = sorted([c for c in comps if c[2] - c[0] > 0.6 * w], key=cy)
        if len(wide) >= 2:
            names["neck_k"], names["neck_n"] = wide[0], wide[1]
        rest = sorted([c for c in rows if all(c is not x for x in wide)], key=cx)
        if len(rest) >= 2:
            names["coil"], names["tail"] = rest[0], rest[-1]
    elif sc == "M03":
        grid = [["wave_a", "wave_b", "wave_c"], ["wave_d", "wave_e", "foam"]]
        for c in comps:
            nm = grid[min(1, int(cy(c) / (h / 2)))][min(2, int(cx(c) / (w / 3)))]
            if nm not in names or area(c) > area(names[nm]):
                names[nm] = c
    elif sc == "M04":
        top = [c for c in comps if cy(c) < h * 0.33]
        mid = sorted([c for c in comps if h * 0.33 <= cy(c) < h * 0.7], key=cx)
        bot = [c for c in comps if cy(c) >= h * 0.7]
        if top:
            names["band"] = max(top, key=area)
        if len(mid) >= 2:  # hai mảnh lớn nhất hàng giữa (quanh vương miện nước còn mấy giọt lẻ: bỏ)
            two = sorted(sorted(mid, key=area, reverse=True)[:2], key=cx)
            names["mound"], names["crown"] = two[0], two[1]
        if bot:
            ring = max(bot, key=lambda c: c[2] - c[0])
            names["ring"] = ring
            drops = sorted([c for c in bot if c is not ring], key=area, reverse=True)
            for nm, c in zip(("drop_a", "drop_b", "drop_c"), drops):
                names[nm] = c
    elif sc == "M05":
        wide = sorted([c for c in comps if c[2] - c[0] > 0.6 * w], key=cy)
        if len(wide) >= 2:
            names["jet_k"], names["jet_n"] = wide[0], wide[1]
        rest = [c for c in comps if all(c is not x for x in wide) and cy(c) > h * 0.5]
        col = lambda a, b: [c for c in rest if w * a <= cx(c) < w * b]
        if col(0, 0.33):
            names["burst"] = max(col(0, 0.33), key=area)
        if col(0.33, 0.58):
            names["flare"] = max(col(0.33, 0.58), key=area)
        for nm, c in zip(("streak_a", "streak_b", "streak_c"), sorted(sorted(col(0.58, 0.80), key=area, reverse=True)[:3], key=cy)):
            names[nm] = c
        for nm, c in zip(("lid_k", "lid_n"), sorted(sorted(col(0.80, 1.01), key=area, reverse=True)[:2], key=cy)):
            names[nm] = c
    elif sc == "M06":
        for nm, c in zip(("tongue_k", "tongue_n"), sorted(sorted(comps, key=area, reverse=True)[:2], key=cy)):
            names[nm] = c
    elif sc == "M07":
        top = sorted([c for c in comps if cy(c) < h * 0.31], key=lambda c: c[2] - c[0], reverse=True)
        mid = sorted(sorted([c for c in comps if h * 0.31 <= cy(c) < h * 0.76], key=area, reverse=True)[:4], key=cx)
        bot = [c for c in comps if cy(c) >= h * 0.76]
        if len(top) >= 2:
            names["sweep"], names["curl_s1"] = top[0], top[1]
        for nm, c in zip(("tend_a", "tend_b", "curl_s2", "curl_s3"), mid):
            names[nm] = c
        if bot:
            names["ripple"] = max(bot, key=lambda c: c[2] - c[0])
    return names


def cat():
    os.makedirs(MANH, exist_ok=True)
    for sc in ("M01", "M02", "M03", "M04", "M05", "M06", "M07"):
        p = sheet_path(sc)
        if not p:
            print(sc, ": chưa có ảnh")
            continue
        comps, rgba = components(p)
        h, w = rgba.shape[:2]
        names = assign(sc, comps, w, h)
        want = [k for k, v in PIECES.items() if v[0] == sc]
        print(sc, os.path.basename(p), f"{len(comps)} mảnh rời ->", ", ".join(f"{k} {names[k][2] - names[k][0]}x{names[k][3] - names[k][1]}" for k in want if k in names),
              "| THIẾU: " + ", ".join(k for k in want if k not in names) if any(k not in names for k in want) else "")
        for nm, c in names.items():
            x0, y0, x1, y1, m = c
            pad = 4
            x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
            im = rgba[y0:y1, x0:x1].copy()
            keep = cv2.dilate(m[y0:y1, x0:x1].astype(np.uint8), np.ones((5, 5), np.uint8))
            im[..., 3] = (im[..., 3] * keep).astype(np.uint8)
            if nm == "ring":  # lòng vòng sóng là giấy trắng khép kín: đục thành trong suốt
                hh, ww = im.shape[:2]
                lightc = (im[..., :3].min(axis=2) > 236).astype(np.uint8)
                if lightc[hh // 2, ww // 2]:
                    ffm = np.zeros((hh + 2, ww + 2), np.uint8)
                    cv2.floodFill(lightc, ffm, (ww // 2, hh // 2), 2)
                    hole = cv2.dilate((lightc == 2).astype(np.uint8), np.ones((3, 3), np.uint8))
                    soft = cv2.GaussianBlur((1 - hole).astype(np.float32), (0, 0), 1.1)
                    im[..., 3] = (im[..., 3] * np.clip(soft * 1.2 - 0.1, 0, 1)).astype(np.uint8)
            Image.fromarray(im, "RGBA").save(os.path.join(MANH, nm + ".png"))
    # tờ soi: mọi mảnh trên nền xám
    ims = [(k, Image.open(os.path.join(MANH, k + ".png"))) for k in PIECES if os.path.exists(os.path.join(MANH, k + ".png"))]
    if ims:
        W_ = 1800
        x = y = 10
        row = 0
        sheet = Image.new("RGB", (W_, 2600), (120, 124, 132))
        d = ImageDraw.Draw(sheet)
        for k, im in ims:
            im = im.copy()
            im.thumbnail((560, 300))
            if x + im.width + 10 > W_:
                x, y, row = 10, y + row + 26, 0
            sheet.paste(im, (x, y + 16), im)
            d.text((x, y), k, fill=(255, 255, 255))
            x += im.width + 14
            row = max(row, im.height + 16)
        sheet.crop((0, 0, W_, y + row + 20)).save(os.path.join(MANH, "_soi.png"))


def placeholder(nm):
    _, (w, h), col = PIECES[nm]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink = (43, 33, 24, 255)
    if nm.startswith("neck"):
        d.rounded_rectangle([2, 22, w - 3, h - 3], radius=h // 2 - 12, fill=col + (255,), outline=ink, width=6)
        d.rectangle([60, h - 50, w - 60, h - 9], fill=(242, 217, 160, 255))
        for x in range(60, w - 60, 80):
            d.polygon([(x, 26), (x + 30, 2), (x + 60, 26)], fill=(224, 86, 60, 255), outline=ink)
            d.line([(x, h - 50), (x, h - 9)], fill=ink, width=3)
    elif nm == "ring":
        d.ellipse([2, 2, w - 3, h - 3], outline=col + (255,), width=22)
    elif nm.startswith("drop"):
        d.polygon([(w / 2, 2), (w - 3, h * 0.65), (w / 2, h - 3), (3, h * 0.65)], fill=col + (255,), outline=ink)
    elif nm.startswith("wave") or nm in ("crown", "foam"):
        d.pieslice([2, 2, w - 3, 2 * h - 6], 180, 360, fill=col + (255,), outline=ink, width=6)
        d.ellipse([w * 0.55, 8, w * 0.95, h * 0.45], fill=(244, 252, 255, 255), outline=ink, width=5)
    elif nm.startswith("head"):
        d.rounded_rectangle([2, h * 0.35, w - 3, h - 3], radius=40, fill=col + (255,), outline=ink, width=6)
        d.polygon([(w * 0.2, h * 0.4), (w * 0.25, 4), (w * 0.38, h * 0.38)], fill=(233, 184, 74, 255), outline=ink)
        d.ellipse([w * 0.6, h * 0.5, w * 0.7, h * 0.65], fill=(240, 160, 48, 255), outline=ink, width=3)
    else:
        d.rounded_rectangle([2, 2, w - 3, h - 3], radius=min(w, h) // 3, fill=col + (255,), outline=ink, width=6)
    return im


def bleed(im, it=6):
    """màu của điểm trong suốt lấy theo mép hình gần nhất (lọc tuyến tính không kéo viền trắng vào)."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3].copy(), a[..., 3:] / 255.0
    w = (al > 0.02).astype(np.float32)
    cur = rgb * w
    for _ in range(it):
        num = cv2.blur(cur, (5, 5))
        den = cv2.blur(w, (5, 5))
        den = den[..., None] if den.ndim == 2 else den
        fill = num / np.maximum(den, 1e-4)
        grow = (den > 1e-3).astype(np.float32)
        cur = cur * w + fill * (1 - w) * grow
        w = np.maximum(w, grow)
    out = np.where(al > 0.02, rgb, cur)
    return Image.fromarray(np.dstack([out, a[..., 3:]]).clip(0, 255).astype(np.uint8), "RGBA")


def load_pieces():
    out, fake = {}, []
    for nm in PIECES:
        if nm in UNUSED:
            continue
        p = os.path.join(MANH, nm + ".png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
        else:
            im = placeholder(nm)
            fake.append(nm)
        bb = im.getbbox()
        im = im.crop(bb)
        k = SC * PSC.get(nm, 1.0)
        im = im.resize((max(2, round(im.width * k)), max(2, round(im.height * k))), Image.LANCZOS)
        out[nm] = bleed(im)
    if fake:
        print("mảnh giữ chỗ:", ", ".join(fake))
    return out


# ---------------------------------------------------------------- 2. khung xương
class Sk:
    def __init__(self):
        self.bones, self.bi, self.slots, self.atts, self.anims = [], {}, [], {}, {}

    def bone(self, name, parent=None, x=0.0, y=0.0, rot=0.0, length=0.0, sx=1.0, sy=1.0):
        b = {"name": name}
        if parent:
            b["parent"] = parent
        for k, v, d in (("length", length, 0), ("x", x, 0), ("y", y, 0), ("rotation", rot, 0), ("scaleX", sx, 1), ("scaleY", sy, 1)):
            if abs(v - d) > 1e-6:
                b[k] = round(float(v), 2)
        self.bi[name] = len(self.bones)
        self.bones.append(b)
        return name

    def slot(self, name, bone, att=None, alpha=1.0):
        s = {"name": name, "bone": bone}
        if att:
            s["attachment"] = att
        if alpha < 1:
            s["color"] = "ffffff%02x" % int(alpha * 255)
        self.slots.append(s)
        return name

    def region(self, slot, piece, im, x, y, rot=0.0, sx=1.0, sy=1.0, name=None):
        a = {"path": piece, "x": round(x, 2), "y": round(y, 2), "width": im.width, "height": im.height}
        if rot:
            a["rotation"] = round(rot, 2)
        if sx != 1:
            a["scaleX"] = sx
        if sy != 1:
            a["scaleY"] = sy
        self.atts.setdefault(slot, {})[name or piece] = a

    def mesh(self, slot, piece, im, pts, tris, weights, bind, name=None):
        """pts: [(px, py)] điểm trên ảnh mảnh; weights: mỗi đỉnh [(xương, w)]; bind: toạ độ lúc gắn của từng đỉnh (X, Y) và
        của từng xương {xương: (ox, oy, độ)}."""
        P, BW = bind
        uvs, vs = [], []
        for (px, py), ws, (X, Y) in zip(pts, weights, P):
            uvs += [round(px / im.width, 5), round(py / im.height, 5)]
            ws = [(b, w) for b, w in ws if w > 0.004]
            tot = sum(w for _, w in ws)
            vs.append(len(ws))
            for b, w in ws:
                ox, oy, r = BW[b][:3]
                bsc = BW[b][3] if len(BW[b]) > 3 else 1.0
                c, s = math.cos(math.radians(-r)), math.sin(math.radians(-r))
                dx, dy = (X - ox) / bsc, (Y - oy) / bsc
                vs += [self.bi[b], round(dx * c - dy * s, 2), round(dx * s + dy * c, 2), round(w / tot, 4)]
        self.atts.setdefault(slot, {})[name or piece] = {"type": "mesh", "path": piece, "uvs": uvs, "triangles": [int(i) for t in tris for i in t],
                                                         "vertices": vs, "hull": len(pts), "width": im.width, "height": im.height}

    def clip(self, slot, end, poly):
        self.atts.setdefault(slot, {})["cat"] = {"type": "clipping", "end": end, "vertexCount": len(poly), "vertices": [round(v, 1) for p in poly for v in p],
                                                 "color": "ce3a3aff"}


STRIP_PER = 3   # số cột lưới mỗi đốt của dải (bản 3: 2)
STRIP_ROWS = 7  # số hàng tối đa của dải (tự giảm cho dải mỏng để tam giác gần đều cạnh)


def strip_mesh(im, n_bones, per=STRIP_PER, margin=3, rows=None):
    """lưới dải dọc theo chiều ngang của mảnh (cổ, râu, đuôi, lưỡi): mỗi cột `rows` đỉnh từ mép trên tới mép dưới của hình, cột
    cách đều theo x (per cột mỗi đốt). rows tự chọn cho ô lưới gần vuông (tam giác gần đều cạnh), tối đa STRIP_ROWS, tối thiểu 3;
    đường chéo so le từng ô (dải uốn hai chiều đều mượt). Trả pts, tris, trục y (đường thẳng giữa dải), và x của từng cột."""
    al = np.asarray(im)[..., 3] > 16
    w, h = im.width, im.height
    ncol = n_bones * per + 1
    xs = np.linspace(0, w, ncol)
    tops, bots = [], []
    for x in xs:
        x0, x1 = int(max(0, x - w / ncol * 0.6)), int(min(w, x + w / ncol * 0.6 + 1))
        rr = np.flatnonzero(al[:, x0:x1].any(axis=1))
        tops.append(rr[0] if len(rr) else np.nan)
        bots.append(rr[-1] if len(rr) else np.nan)
    tops, bots = np.array(tops, float), np.array(bots, float)
    ok = ~np.isnan(tops)
    tops[~ok] = np.interp(np.flatnonzero(~ok), np.flatnonzero(ok), tops[ok])
    bots[~ok] = np.interp(np.flatnonzero(~ok), np.flatnonzero(ok), bots[ok])
    tops, bots = np.clip(tops - margin, 0, h), np.clip(bots + margin, 0, h)
    axis = float(np.median((tops + bots) / 2))
    if rows is None:
        thick = float(np.median(bots - tops))
        rows = int(min(STRIP_ROWS, max(3, round(thick / (w / (ncol - 1))) + 1)))
    pts, tris = [], []
    for i, x in enumerate(xs):
        for r in range(rows):
            f = r / (rows - 1)
            pts.append((x, tops[i] + (bots[i] - tops[i]) * f))
        if i:
            a = (i - 1) * rows
            for r in range(rows - 1):
                p0, p1, q0, q1 = a + r, a + r + 1, a + rows + r, a + rows + r + 1   # cột trước (p), cột này (q); trên (0), dưới (1)
                if (i + r) % 2 == 0:
                    tris += [(p0, q0, q1), (p0, q1, p1)]
                else:
                    tris += [(p0, q0, p1), (q0, q1, p1)]
    return pts, tris, axis, xs


def chain_weights(X, seg, n):
    """trọng số của một điểm ở hoành độ X trên dải n đốt dài seg, kiểu B-spline bậc hai: giữa đốt 0,75 đốt đó + 0,125 mỗi đốt kề,
    ở khớp 0,5 / 0,5. Không đỉnh nào bám cứng một đốt nên dải lưới uốn thành đường cong trơn; bám 100% ở giữa đốt (cách cũ) thì
    mỗi khớp là một chỗ gập. Rig mẫu chia đúng kiểu này (0,70 / 0,15 / 0,15 ở giữa đốt, 0,5 / 0,5 ở khớp)."""
    f = X / seg
    out = {}
    for j in range(int(math.floor(f - 1.5)), int(math.floor(f + 1.5)) + 2):
        t = abs(f - (j + 0.5))
        w = 0.75 - t * t if t <= 0.5 else (0.5 * (1.5 - t) ** 2 if t < 1.5 else 0.0)
        if w > 1e-4:
            jj = min(n - 1, max(0, j))
            out[jj] = out.get(jj, 0.0) + w
    return sorted(out.items())


def ease(u, kind):
    u = min(1.0, max(0.0, u))
    if kind == "io":
        return u * u * (3 - 2 * u)
    if kind == "out":
        return 1 - (1 - u) ** 3
    if kind == "in":
        return u ** 3
    if kind == "back":
        c1, c3 = 1.70158, 2.70158
        return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2
    if kind == "hold":
        return 0.0 if u < 1 else 1.0
    return u


class Track:
    """khoá (t, giá trị, kiểu êm của đoạn TỚI khoá đó); giá trị là số hoặc bộ số."""

    def __init__(self, keys):
        self.k = [(float(t), np.atleast_1d(np.array(v, float)), e) for t, v, e in keys]

    def __call__(self, t):
        k = self.k
        if t <= k[0][0]:
            return k[0][1]
        for (t0, v0, _), (t1, v1, e) in zip(k[:-1], k[1:]):
            if t <= t1:
                return v0 + (v1 - v0) * ease((t - t0) / max(1e-6, t1 - t0), e)
        return k[-1][1]


def rdp(ts, vs, tol):
    """lược khoá Ramer-Douglas-Peucker trên chuỗi (t, vector)."""
    vs = np.asarray(vs, float)
    if vs.ndim == 1:
        vs = vs[:, None]
    keep = np.zeros(len(ts), bool)
    keep[0] = keep[-1] = True
    st = [(0, len(ts) - 1)]
    while st:
        a, b = st.pop()
        if b <= a + 1:
            continue
        t = (np.asarray(ts[a + 1:b]) - ts[a]) / (ts[b] - ts[a])
        lin = vs[a] + (vs[b] - vs[a]) * t[:, None]
        err = np.abs(vs[a + 1:b] - lin).max(axis=1)
        i = int(err.argmax())
        if err[i] > tol:
            keep[a + 1 + i] = True
            st += [(a, a + 1 + i), (a + 1 + i, b)]
    return np.flatnonzero(keep)


def neck_joints(E, dirE, H, psi, seg, n, ka=0.52, kb=0.42, C2=None, wave=None, rest=None):
    """khớp J0..Jn của cổ n đốt dài seg: đường cong Bezier từ chỗ trồi E (hướng dirE) tới gáy H (psi = hướng cổ đi tới gáy), phần thừa của cổ
    trượt thẳng xuống dưới E. Lần ngược từ đầu, mỗi bước đúng một đốt. C2: điểm điều khiển gần đầu (cho đà trễ).
    rest: đường tâm cổ lúc nghỉ (danh sách điểm E → gáy, trích từ mặt nạ concept, vòng 2 lô Thủy): thay Bezier bằng đường này, kéo
    mềm theo đầu (điểm càng gần gáy dời theo đầu càng nhiều: hệ số t^1,5), sóng uốn vẫn cộng thêm."""
    E, H = np.array(E, float), np.array(H, float)
    uE = np.array([math.cos(math.radians(dirE)), math.sin(math.radians(dirE))])
    uH = np.array([math.cos(math.radians(psi)), math.sin(math.radians(psi))])
    d = float(np.hypot(*(H - E)))
    t = np.linspace(0, 1, 160)[:, None]
    if rest is not None:
        R = np.asarray(rest, float)
        dl = np.hypot(*np.diff(R, axis=0).T)
        cum = np.concatenate([[0.0], np.cumsum(dl)])
        u = t[:, 0] * cum[-1]
        base = np.stack([np.interp(u, cum, R[:, 0]), np.interp(u, cum, R[:, 1])], axis=1)
        curve = base + (H - R[-1]) * (t ** 1.5) + (E - R[0]) * ((1 - t) ** 1.5)
    else:
        P1 = E + uE * d * ka
        P2 = np.array(C2, float) if C2 is not None else H - uH * d * kb
        curve = (1 - t) ** 3 * E + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * H
    if wave:  # (biên độ, pha): sóng ngang chạy dọc đoạn cổ nổi, tắt ở hai đầu (chỗ trồi và gáy) nên đầu không bị xê dịch
        amp, phs = wave
        dC = np.gradient(curve, axis=0)
        nrm = np.stack([-dC[:, 1], dC[:, 0]], axis=1)
        nrm /= np.maximum(1e-6, np.hypot(nrm[:, 0], nrm[:, 1]))[:, None]
        tt = t[:, 0]
        curve = curve + nrm * (amp * np.sin(math.pi * tt) * np.sin(2 * math.pi * WAVE_K * tt + phs))[:, None]
    L = seg * n
    below = E - uE * np.linspace(L, 0, 80, endpoint=False)[:, None]
    line = np.vstack([below, curve])  # từ đáy lên tới đầu
    J = [H.copy()]
    i = len(line) - 1
    for _ in range(n):
        p = J[-1]
        while i > 0 and np.hypot(*(line[i - 1] - p)) < seg:
            i -= 1
        if i == 0:
            q = p - uE * seg
        else:
            a, b = line[i], line[i - 1]  # |a - p| < seg <= |b - p|
            lo, hi = 0.0, 1.0
            for _ in range(18):
                m = (lo + hi) / 2
                if np.hypot(*(a + (b - a) * m - p)) < seg:
                    lo = m
                else:
                    hi = m
            q = a + (b - a) * lo
        J.append(q)
    return np.array(J[::-1])


def follow(target, tau, dt, pre):
    """bám trễ bậc nhất của chuỗi điểm target (mảng theo khung); pre: số khung chạy đà (clip lặp)."""
    k = 1 - math.exp(-dt / tau)
    c = target[0].copy()
    n = len(target)
    for i in range(pre):
        c = c + (target[(i - pre) % n] - c) * k
    out = []
    for i in range(n):
        c = c + (target[i] - c) * k
        out.append(c.copy())
    return np.array(out)


def rope(anchor, ang0, rest, seg, loop, k0=0.20, k1=0.035, zeta=0.5, wind=None, sub=4, lim=(20.0, 32.0)):
    """dây mềm N đốt (râu): mô phỏng kiểu Verlet 'đốt sau đi theo đốt trước' rồi nướng ra góc xoay từng đốt.
    anchor[n, 2]: gốc dây theo khung (toạ độ thế giới); ang0[n]: góc thế giới của xương cha (độ); rest[N]: góc nghỉ của từng đốt
    so với đốt trước (độ); seg: dài mỗi đốt. Mỗi đốt là một lò xo kéo về dáng nghỉ SO VỚI ĐỐT TRƯỚC (cứng k0 ở gốc -> k1 ở ngọn,
    tần số riêng ~ sqrt(k) * FPS * sub rad/s), giảm chấn zeta, có gió wind(giây, đốt) -> gia tốc. Vì lò xo tính theo đốt trước
    nên cú giật của đầu chạy dọc sợi râu thành sóng. loop: clip lặp thì chạy đà hai vòng cho khớp vòng.
    Trả góc lệch [n, N] (độ) so với dáng nghỉ."""
    n, N = len(anchor), len(rest)
    dt = 1.0 / FPS / sub
    ks = np.linspace(k0, k1, N)
    keep = 1 - 2 * zeta * np.sqrt(ks)
    lims = np.linspace(lim[0], lim[1], N)  # mỗi khớp chỉ gập tối đa chừng này so với dáng nghỉ (nén mềm bằng tanh): râu cong đều, không gãy

    def rest_pts(a, ang):
        pts, th = [np.array(a, float)], ang
        for i in range(N):
            th += rest[i]
            pts.append(pts[-1] + seg * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))]))
        return np.array(pts)

    st = {"p": rest_pts(anchor[0], ang0[0])}
    st["prev"] = st["p"].copy()

    def step(a, ang, tsec):
        pp, prev = st["p"], st["prev"]
        new = pp.copy()
        new[0] = a
        thp = ang
        for i in range(1, N + 1):
            q = pp[i] + (pp[i] - prev[i]) * keep[i - 1]
            if wind is not None:
                q = q + wind(tsec, i) * dt * dt
            r = math.radians(thp + rest[i - 1])
            tgt = new[i - 1] + seg * np.array([math.cos(r), math.sin(r)])
            q = q + (tgt - q) * ks[i - 1]
            d = q - new[i - 1]
            base = thp + rest[i - 1]
            o = ((math.degrees(math.atan2(d[1], d[0])) - base) + 180) % 360 - 180
            thp = base + lims[i - 1] * math.tanh(o / lims[i - 1])
            new[i] = new[i - 1] + seg * np.array([math.cos(math.radians(thp)), math.sin(math.radians(thp))])
        st["prev"], st["p"] = pp, new

    def frame(f, f0):
        for k in range(1, sub + 1):
            u = k / sub
            step(anchor[f0] + (anchor[f] - anchor[f0]) * u, ang0[f0] + (ang0[f] - ang0[f0]) * u, (f0 + (f - f0) * u) / FPS)

    if loop:
        for _ in range(2):
            for f in range(1, n):
                frame(f, f - 1)
    else:
        for _ in range(12):
            frame(0, 0)
    out = np.zeros((n, N))
    for f in range(n):
        if f:
            frame(f, f - 1)
        pts = st["p"]
        thp = ang0[f]
        for i in range(N):
            d = pts[i + 1] - pts[i]
            a = math.degrees(math.atan2(d[1], d[0]))
            out[f, i] = ((a - thp - rest[i]) + 180) % 360 - 180
            thp = a
    return out


# ---------------------------------------------------------------- 4. dựng rig
# đầu: tên, loại cổ/đầu, cỡ, chỗ trồi (x), hướng trồi, đầu lúc nghỉ (x, y, góc), biên độ đung đưa (x, y, góc), pha
# arr: cổ đi tới gáy theo hướng (góc đầu + arr): cổ vào đầu từ phía dưới sau như concept, bờm che chỗ nối
HEADS = [
    dict(id="a", kind="n", size=0.90, ex=-120, dirE=122, H=(-430, 700), psi=6, arr=70, sway=(34, 22, 5), ph=0.35),
    dict(id="c", kind="n", size=0.90, ex=110, dirE=100, H=(250, 575), psi=-13, arr=52, sway=(30, 26, 5), ph=0.80),
    dict(id="b", kind="n", size=0.82, ex=-215, dirE=152, H=(-500, 400), psi=-6, arr=84, sway=(28, 18, 6), ph=0.10),
    dict(id="d", kind="n", size=0.82, ex=225, dirE=84, H=(380, 330), psi=-19, arr=38, sway=(32, 16, 6), ph=0.55),
    dict(id="k", kind="k", size=1.00, ex=0, dirE=74, H=(-60, 810), psi=-4, arr=64, sway=(26, 20, 4), ph=0.0),
]
NB = 14  # số đốt mỗi cổ
WB = 6   # số đốt mỗi sợi râu
WREST = 5.0    # độ cong nghỉ giữa hai đốt râu
WIND = 2600.0  # gió phất râu (gia tốc ở ngọn, đơn vị rig / giây²)
WAVE_A = 22.0  # biên độ sóng uốn chạy dọc cổ (đơn vị rig, ở giữa cổ)
WAVE_K = 1.15  # số bước sóng trên đoạn cổ nổi
TB = 6   # số đốt chóp đuôi
MUZZLE = (0.42, -0.085)               # xương miệng: chỗ nhả (theo bề rộng ảnh đầu, hệ xương đầu)
LB = 5   # số đốt lưỡi
TONGUE_AT = (0.20, -0.06)   # gốc lưỡi trong hàm dưới (theo bề rộng, bề cao ảnh hàm; hệ xương hàm, y lên)
TONGUE_ROT = 6.0            # lưỡi nằm hơi chếch lên so với trục hàm
TONGUE_G = 30000.0          # trọng lực kéo lưỡi rũ (gia tốc, đơn vị rig / giây²)
JROT = -3.0                           # tia nước lệch so với trục đầu (độ)
LID_DX, LID_DY = 0.02, 0.06           # dịch mí so với tâm con ngươi (theo cỡ mí)
LID_ROT = -16.0                       # mí mắt nghiêng theo mắt
TGT = (1150.0, 400.0)                 # chỗ năm tia nước chụm lại (chỗ đối thủ đứng, đơn vị rig)
# chỗ gắn trên từng mảnh, theo tỉ lệ khung mảnh (x từ trái, y từ trên): gáy của đầu, bản lề của hàm, gốc râu...
ANCHOR = {"head_k": (0.45, 0.74), "head_n": (0.44, 0.72), "jaw_k": (0.10, 0.22), "jaw_n": (0.11, 0.24)}
# trong khung đầu (gốc ở gáy, trục x theo mõm): bản lề hàm, tâm lòng miệng, gốc râu trên / dưới; theo bề rộng mảnh đầu
HEAD_GEO = {"jaw": (0.07, 0.042), "mouth": (0.28, -0.075), "wh_f": (0.485, -0.004), "wh_b": (0.43, -0.014)}
HEAD_GEO_K = {}    # theo loại đầu ("k"/"n") nếu dạng khác cần (tm10: bản lề hàm dò theo concept); thiếu thì HEAD_GEO
JAW_SC = 0.86      # hàm dưới vẽ dài hơn mõm trên một chút: thu lại cho răng dưới nằm trong môi trên
JAW_SC_K = {}      # theo loại đầu (tm10: tỉ lệ hàm dò theo concept)
WHISK_ROT = {"b": -128.0, "f": -104.0}   # góc gốc râu sau / trước (dạng 3: râu rủ xuống sau mõm; dạng 1, 2: chĩa ra trước)
WHISK_SC = {"b": 0.62, "f": 0.74}        # cỡ sợi râu sau / trước (dạng 1, 2: râu cụt ngắn)
JAW_CLOSE = {}                           # theo loại đầu: góc khép thêm cho hàm lúc nghỉ (độ; dạng 1, 2 mảnh hàm vẽ há sẵn)
BREATHE = (5.0, 3.0)                     # miệng hé lúc idle: trung bình, biên độ (độ); dạng 1, 2 hé ít hơn
MANE = {"k": (0.38, 0.66, 0.34), "n": (0.40, 0.62, 0.20)}  # gốc bờm (x, y theo ảnh đầu), mép trên của vùng bờm (trên đó là sừng)
NECK_THICK = {"k": 1.0, "n": 1.18}  # cổ nhỏ vẽ hơi mảnh so với đầu: nới bề dày lúc gắn lưới

NC = 4  # số đốt chuỗi xương của mỗi cuộn sóng
# sống lưng của từng hình sóng: đường từ chân sóng, dọc lưng sóng lên mào rồi vào tới đầu móc cuộn (toạ độ theo ảnh, 0..1, y xuống).
# Chuỗi NC đốt nằm trên đường này; xoay các đốt cùng chiều uốn của đường thì mào cuộn chặt lại, ngược chiều thì duỗi ra.
SPINES = {
    "wave_a": [(0.25, 0.97), (0.14, 0.62), (0.25, 0.30), (0.50, 0.12), (0.80, 0.18), (0.88, 0.38), (0.76, 0.52)],
    "wave_b": [(0.70, 0.97), (0.92, 0.65), (0.85, 0.32), (0.60, 0.12), (0.30, 0.20), (0.16, 0.42), (0.28, 0.58)],
    "wave_c": [(0.15, 0.92), (0.06, 0.60), (0.20, 0.28), (0.42, 0.12), (0.62, 0.22), (0.62, 0.42)],
    "wave_d": [(0.30, 0.95), (0.10, 0.65), (0.20, 0.32), (0.48, 0.10), (0.82, 0.16), (0.95, 0.36), (0.80, 0.52)],
    "wave_e": [(0.08, 0.85), (0.30, 0.60), (0.55, 0.52), (0.75, 0.30), (0.90, 0.25), (0.90, 0.45)],
    "sweep": [(0.02, 0.80), (0.30, 0.78), (0.55, 0.55), (0.75, 0.30), (0.90, 0.20), (0.97, 0.45), (0.92, 0.62)],
    "curl_s1": [(0.35, 0.97), (0.10, 0.60), (0.25, 0.22), (0.60, 0.10), (0.90, 0.30), (0.80, 0.55)],
    "tend_a": [(0.45, 0.98), (0.30, 0.65), (0.32, 0.35), (0.50, 0.10), (0.80, 0.08), (0.92, 0.22), (0.72, 0.30)],
    "tend_b": [(0.35, 0.97), (0.10, 0.60), (0.30, 0.25), (0.60, 0.08), (0.92, 0.20), (0.85, 0.38)],
    "curl_s2": [(0.35, 0.97), (0.06, 0.60), (0.22, 0.22), (0.60, 0.08), (0.92, 0.28), (0.75, 0.52)],
    "curl_s3": [(0.35, 0.97), (0.08, 0.60), (0.25, 0.25), (0.60, 0.10), (0.90, 0.30), (0.75, 0.55)],
    "foam": [(0.5, 0.95), (0.5, 0.7), (0.5, 0.45), (0.5, 0.2)],
}
# cuộn sóng: mảnh, lớp, x chân sóng, y chân sóng, cỡ, pha, lật; tuỳ chọn: dx (trôi ngang cả đời sóng), kc (độ cuộn), rise (độ dâng theo
# chiều cao), a (độ đậm). Học rig mẫu: sóng KHÔNG trượt ngang; mỗi cuộn dâng lên tại chỗ, mào tự cuộn lại, trôi nhẹ rồi tan.
WAVES = [
    dict(p="wave_b", lane="back", x=-560, y=62, s=1.00, ph=0.00, flip=False),
    dict(p="tend_a", lane="back", x=-340, y=78, s=1.08, ph=0.55, flip=True, kc=0.8),
    dict(p="wave_c", lane="back", x=-190, y=84, s=0.90, ph=0.25, flip=False),
    dict(p="tend_b", lane="back", x=40, y=86, s=1.02, ph=0.80, flip=False, kc=0.8),
    dict(p="tend_a", lane="back", x=300, y=80, s=1.00, ph=0.10, flip=False, kc=0.8),
    dict(p="wave_a", lane="back", x=470, y=62, s=1.00, ph=0.45, flip=False),
    dict(p="curl_s2", lane="mid", x=-250, y=70, s=0.90, ph=0.65, flip=True),
    dict(p="tend_b", lane="mid", x=-60, y=72, s=0.80, ph=0.30, flip=True, kc=0.8),
    dict(p="wave_a", lane="mid", x=110, y=60, s=0.62, ph=0.90, flip=False),
    dict(p="curl_s2", lane="mid", x=330, y=66, s=0.85, ph=0.15, flip=False),
    dict(p="wave_c", lane="front", x=-560, y=14, s=0.72, ph=0.30, flip=True),
    dict(p="curl_s1", lane="front", x=-480, y=18, s=0.90, ph=0.70, flip=False),
    dict(p="wave_d", lane="front", x=-290, y=8, s=0.90, ph=0.05, flip=True),
    dict(p="curl_s3", lane="front", x=-215, y=22, s=0.95, ph=0.50, flip=False),
    dict(p="curl_s2", lane="front", x=-20, y=4, s=0.70, ph=0.85, flip=True),
    dict(p="curl_s1", lane="front", x=130, y=16, s=0.85, ph=0.40, flip=True),
    dict(p="wave_d", lane="front", x=200, y=8, s=0.85, ph=0.20, flip=False),
    dict(p="curl_s3", lane="front", x=395, y=20, s=0.90, ph=0.60, flip=True),
    dict(p="wave_c", lane="front", x=505, y=14, s=0.70, ph=0.95, flip=False),
    dict(p="foam", lane="front", x=-250, y=16, s=0.60, ph=0.90, flip=False, kc=0.0, rise=0.3),
    dict(p="foam", lane="front", x=300, y=14, s=0.55, ph=0.35, flip=True, kc=0.0, rise=0.3),
    dict(p="sweep", lane="sweep", x=-650, y=6, s=0.86, ph=0.20, flip=False, kc=0.5, rise=0.12, dx=30),
    dict(p="sweep", lane="sweep", x=660, y=8, s=0.72, ph=0.70, flip=True, kc=0.5, rise=0.12, dx=30),
]
NRB = 8  # số xương dọc mỗi dải nước (dải mặt nước, dải gợn sóng): xương nhấp nhô lệch pha -> dải uốn sóng mềm
N_CROWN, N_DROP, N_RING = 6, 20, 3
WAVE_G = 8    # lưới mỗi cuộn sóng: WAVE_G × WAVE_G ô (bản 3: 5)
HEAD_G = (14, 10)   # lưới đầu (cột, hàng; bản 3: 9 × 6)
COIL_G = (13, 8)    # lưới vòng thân (bản 3: 8 × 5)
MOUTH_G = (7, 4)    # lưới lòng miệng (bản 3: 5 × 3)
JAW_G = (9, 4)      # lưới hàm dưới (bản 3: mảnh cứng). Hai xương như con gốc (xiae): họng sát bản lề theo đầu, cằm và mõm theo hàm
RIB_ROWS, RIB_PER = 4, 3   # dải nước: hàng và cột mỗi xương (bản 3: 3 hàng, 2 cột)


def grid_tris(nx, ny):
    """tam giác của lưới (nx + 1) × (ny + 1) đỉnh xếp theo hàng, đường chéo so le."""
    tris = []
    for r in range(ny):
        for c in range(nx):
            a = r * (nx + 1) + c
            if (r + c) % 2 == 0:
                tris += [(a, a + 1, a + nx + 2), (a, a + nx + 2, a + nx + 1)]
            else:
                tris += [(a, a + 1, a + nx + 1), (a + 1, a + nx + 2, a + nx + 1)]
    return tris


_LID = {}


def fit_lid(kind, hp, lp):
    """chỗ đặt mí mắt trên ảnh đầu: (tâm x, tâm y theo pixel ảnh đầu, góc độ, tỉ lệ). Con mắt = cụm cam trong vùng mặt, lấy bao lồi
    (gồm cả đồng tử, chấm sáng) rồi nới 5 px cho hết viền mực. Dò góc, tỉ lệ, độ lệch sao cho mí phủ KÍN con mắt, ít lòi ra ngoài
    hình đầu nhất, và nhỏ nhất có thể. Đặt theo 'tâm con ngươi × hệ số' (cách cũ) thì hở một khe cam ở mép."""
    if kind in _LID:
        return _LID[kind]
    ha = np.asarray(hp).astype(int)
    H_, W_ = ha.shape[:2]
    org = ((ha[..., 3] > 128) & (ha[..., 0] > 200) & (ha[..., 1] > 110) & (ha[..., 1] < 200) & (ha[..., 2] < 110)).astype(np.uint8)
    ne, lab, st_, cen = cv2.connectedComponentsWithStats(org, 8)
    cand = [i for i in range(1, ne) if 0.56 * W_ < cen[i][0] < 0.86 * W_ and 0.38 * H_ < cen[i][1] < 0.82 * H_]
    if not cand:
        _LID[kind] = (0.7 * W_, 0.6 * H_, LID_ROT, 0.5)
        return _LID[kind]
    ie = max(cand, key=lambda i: st_[i, cv2.CC_STAT_AREA])
    # mống mắt có hai sắc (cam đậm, vàng nhạt): lấy cả vùng màu ấm liền với cụm cam, giới hạn trong ô quanh mắt (không dính sừng vàng)
    warm = ((ha[..., 3] > 128) & (ha[..., 0] > 185) & (ha[..., 0] - ha[..., 2] > 55)).astype(np.uint8)
    x0e, y0e, we, he = st_[ie, 0], st_[ie, 1], st_[ie, 2], st_[ie, 3]
    box = np.zeros_like(warm)
    box[max(0, y0e - he):y0e + 2 * he, max(0, x0e - we):x0e + 2 * we] = 1
    nw, labw = cv2.connectedComponents(warm & box, connectivity=8)
    yo, xo = np.nonzero(lab == ie)           # một điểm chắc chắn thuộc cụm cam (tâm cụm có thể rơi vào đồng tử đen)
    ys, xs = np.nonzero(labw == labw[yo[0], xo[0]])
    brow = ((ha[..., 3] > 128) & (ha[..., 1] > 212) & (ha[..., 2] > 185) & (ha[..., 0] < 236)).astype(np.uint8)  # gờ mày xanh nhạt: mí đừng đè lên
    hull = cv2.convexHull(np.stack([xs, ys], axis=1).astype(np.int32))
    eye = np.zeros((H_, W_), np.uint8)
    cv2.fillConvexPoly(eye, hull, 1)
    eye = cv2.dilate(eye, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    need = int(eye.sum())
    head = (ha[..., 3] > 128).astype(np.uint8)
    la = (np.asarray(lp)[..., 3] > 150).astype(np.uint8)
    la = cv2.erode(la, np.ones((3, 3), np.uint8))  # phần đặc của mí (bỏ mép mờ)
    ex, ey = float(xs.mean()), float(ys.mean())
    ew = float(xs.max() - xs.min() + 11)
    best = None
    for rot in range(-34, 9, 4):
        for sc in np.arange(1.25, 2.61, 0.15) * ew / lp.width:
            for dx in range(-12, 13, 3):
                for dy in range(-12, 13, 3):
                    M = cv2.getRotationMatrix2D((lp.width / 2, lp.height / 2), rot, sc)  # góc dương = ngược kim trên màn hình
                    M[0, 2] += ex + dx - lp.width / 2
                    M[1, 2] += ey + dy - lp.height / 2
                    m = cv2.warpAffine(la, M, (W_, H_), flags=cv2.INTER_NEAREST)
                    miss = need - int((m & eye).sum())
                    out = int((m & (1 - head)).sum())
                    cost = miss * 40 + out * 6 + int((m & brow).sum()) * 1.5 + int(m.sum()) * 0.05
                    if best is None or cost < best[0]:
                        best = (cost, ex + dx, ey + dy, rot, sc, miss, out)
    print(f"mí mắt {kind}: tâm ({best[1]:.0f}, {best[2]:.0f}) góc {best[3]} tỉ lệ {best[4]:.2f}; còn hở {best[5]} px / {need}, lòi ngoài đầu {best[6]} px")
    _LID[kind] = (best[1], best[2], float(best[3]), float(best[4]))
    return _LID[kind]


def build_rig(pc):
    sk = Sk()
    sk.bone("root")
    sk.bone("nuoc", "root")      # nhóm nước: clip chính co giãn (nở ra lúc xuất hiện, tan lúc chết)
    sk.bone("song", "nuoc")      # cha của mọi cuộn sóng: clip chính ép dẹt lúc nước lặng (calm); mọi chuyển động sóng nằm ở clip aura
    sk.bone("than", "root")      # nhóm thân
    info = {"heads": {}, "waves": [], "ribbons": [], "pieces": pc}

    # --- nước sau (không bị cắt) ---
    sk.bone("mound", "nuoc", 0, 28)
    sk.slot("mound", "mound", "mound")
    sk.region("mound", "mound", pc["mound"], 0, pc["mound"].height * 1.5 / 2, 0, 2.15, 1.5)

    def wave_inst(i, cfg, copy):
        nm = f"w{i}{'ab'[copy]}"
        im = pc[cfg["p"]]
        sp = np.array(SPINES[cfg["p"]], float) * (im.width, im.height)
        sp = np.stack([sp[:, 0] - sp[0, 0], im.height - sp[:, 1]], axis=1)   # hệ gốc sóng: gốc ở chân sống lưng, y lên
        dl = np.hypot(*np.diff(sp, axis=0).T)
        cum = np.concatenate([[0], np.cumsum(dl)])
        dense_t = np.linspace(0, cum[-1], 81)
        dense = np.stack([np.interp(dense_t, cum, sp[:, 0]), np.interp(dense_t, cum, sp[:, 1])], axis=1)
        J = dense[:: 80 // NC]                                             # NC + 1 khớp cách đều theo độ dài
        ang = [math.degrees(math.atan2(J[k + 1][1] - J[k][1], J[k + 1][0] - J[k][0])) for k in range(NC)]
        turn = sum(((ang[k + 1] - ang[k] + 180) % 360) - 180 for k in range(NC - 1))
        sense = 1.0 if turn >= 0 else -1.0
        sk.bone(nm, "song", cfg["x"], cfg["y"], 0, 0, (-1 if cfg["flip"] else 1) * cfg["s"], cfg["s"])
        cn = [f"{nm}{k}" for k in range(NC)]
        for k in range(NC):
            if k == 0:
                sk.bone(cn[0], nm, J[0][0], J[0][1], ang[0], cum[-1] / NC)
            else:
                sk.bone(cn[k], cn[k - 1], cum[-1] / NC, 0, ang[k] - ang[k - 1], cum[-1] / NC)
        # slot sóng hiện sẵn (alpha 1): đời sóng (mờ vào, mờ ra) khoá trong clip aura; runtime Overlay NHÂN độ đậm nên mặc định phải là 1
        sk.slot(nm, nm, cfg["p"])
        g = WAVE_G
        size = max(im.width, im.height)
        pts, wts, P = [], [], []
        for r in range(g + 1):
            for c in range(g + 1):
                px, py = im.width * c / g, im.height * r / g
                X, Y = px - sp[0, 0] - 0.0, im.height - py
                X = px - np.array(SPINES[cfg["p"]][0][0]) * im.width
                d2 = (dense[:, 0] - X) ** 2 + (dense[:, 1] - Y) ** 2
                kmin = int(np.argmin(d2))
                near = math.exp(-(math.sqrt(d2[kmin]) / (0.30 * size)) ** 2)   # điểm xa sống lưng (ngọn sóng phụ, chân sóng) bám gốc
                f = kmin / 80 * NC
                ws = [(cn[b], w * near) for b, w in chain_weights(f, 1.0, NC)] + [(nm, 1 - near)]
                pts.append((px, py))
                P.append((X, Y))
                wts.append(ws)
        tris = grid_tris(g, g)
        bind = {cn[k]: (J[k][0], J[k][1], ang[k]) for k in range(NC)}
        bind[nm] = (0, 0, 0)
        sk.mesh(nm, cfg["p"], im, pts, tris, wts, (P, bind))
        info["waves"].append(dict(cfg, bone=nm, ph=(cfg["ph"] + 0.5 * copy) % 1.0, sense=sense, h=im.height))

    def ribbon(slot, bone, piece, sx, sy, y0=0.0):
        """dải nước dài: lưới 3 hàng bám NRB xương xếp dọc dải (trọng số B-spline theo x); hàng đáy bám xương gốc (đáy đứng yên),
        hàng mào bám hẳn chuỗi: khoá các xương nhấp nhô lệch pha thì mào dải uốn thành sóng chạy."""
        im = pc[piece]
        W_ = im.width * abs(sx)
        seg = W_ / NRB
        rn = [f"{bone}_{i}" for i in range(NRB)]
        for i in range(NRB):
            sk.bone(rn[i], bone, -W_ / 2 + (i + 0.5) * seg, 0)
        cols = RIB_PER * NRB + 1
        pts, P, wts = [], [], []
        for r in range(RIB_ROWS):
            for c in range(cols):
                px, py = im.width * c / (cols - 1), im.height * r / (RIB_ROWS - 1)
                X, Y = (px - im.width / 2) * sx, (im.height - py) * sy + y0
                k = (1.0 - r / (RIB_ROWS - 1)) ** 1.6     # hàng mào bám hẳn chuỗi, hàng đáy bám gốc (đáy đứng yên)
                pts.append((px, py))
                P.append((X, Y))
                wts.append([(rn[b], w * k) for b, w in chain_weights(X + W_ / 2, seg, NRB)] + [(bone, 1 - k)])
        tris = grid_tris(cols - 1, RIB_ROWS - 1)
        bind = {rn[i]: (-W_ / 2 + (i + 0.5) * seg, 0, 0) for i in range(NRB)}
        bind[bone] = (0, 0, 0)
        sk.mesh(slot, piece, im, pts, tris, wts, (P, bind))
        info["ribbons"].append(bone)

    def lane(name):
        for i, cfg in enumerate(WAVES):
            if cfg["lane"] == name:
                for copy in (0, 1):
                    wave_inst(i, cfg, copy)

    lane("back")
    # --- mặt nạ cắt: mọi thứ của thân dưới mặt nước bị che ---
    sk.slot("cat", "root", "cat")
    # --- vòng thân và chóp đuôi ---
    # vòng thân: một lưới, 5 điểm điều khiển dọc vòm; khoá lệch pha nhau nên chỗ phồng chạy dọc thân (thân như đang trườn)
    cim, csc = pc["coil"], 0.82
    cw, chh = cim.width * csc, cim.height * csc
    sk.bone("coil", "than", -500, 70)
    info["coil"] = []
    for i, a in enumerate((172, 130, 90, 50, 8)):
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        sk.bone(f"coil{i}", "coil", ux * cw * 0.36, -34 + uy * chh * 0.72)
        info["coil"].append((f"coil{i}", ux, uy, ux * cw * 0.36, -34 + uy * chh * 0.72))
    sk.slot("coil", "coil", "coil")
    gx_, gy_ = COIL_G
    cpts, cP, cwts = [], [], []
    for r in range(gy_ + 1):
        for cc in range(gx_ + 1):
            px, py = cim.width * cc / gx_, cim.height * r / gy_
            X, Y = (px - cim.width / 2) * csc, (cim.height - py) * csc - 34
            ws = [(nm, math.exp(-((X - bx) ** 2 + (Y - by) ** 2) / (cw * 0.26) ** 2)) for nm, _, _, bx, by in info["coil"]]
            cpts.append((px, py))
            cP.append((X, Y))
            cwts.append(ws + [("coil", 0.18)])
    ctris = grid_tris(gx_, gy_)
    cbind = {nm: (bx, by, 0) for nm, _, _, bx, by in info["coil"]}
    cbind["coil"] = (0, 0, 0)
    sk.mesh("coil", "coil", cim, cpts, ctris, cwts, (cP, cbind))
    # chóp đuôi: dải lưới TB đốt, quẫy thành sóng lớn dần ra vây
    tim, tsc = pc["tail"], 0.8
    tseg = tim.width * tsc / TB
    tr0 = math.radians(56)
    tnames = ["tail"] + [f"tail{i}" for i in range(1, TB)]
    sk.bone("tail", "than", 500 - 60 * math.cos(tr0), 60 - 60 * math.sin(tr0), 56, tseg)
    for i in range(1, TB):
        sk.bone(tnames[i], tnames[i - 1], tseg, 0, 0, tseg)
    sk.slot("tail", "tail", "tail")
    tpts, ttris, taxis, _ = strip_mesh(tim, TB)
    tP = [(px * tsc, (taxis - py) * tsc) for px, py in tpts]
    twts = [[(tnames[b], w) for b, w in chain_weights(px * tsc, tseg, TB)] for px, _ in tpts]
    sk.mesh("tail", "tail", tim, tpts, ttris, twts, (tP, {tnames[i]: (i * tseg, 0, 0) for i in range(TB)}))

    def head(h, with_mid=False):
        hid, kind = h["id"], h["kind"]
        neck, hp, jp = pc["neck_" + kind], pc["head_" + kind], pc["jaw_" + kind]
        sz = h["size"]
        seg = neck.width / NB
        E = (h["ex"], CLIPY - 14)
        J = neck_joints(E, h["dirE"], h["H"], h["psi"] + h["arr"], seg * sz, NB, ka=h.get("ka", 0.52), kb=h.get("kb", 0.42), rest=h.get("rest"))
        th = [math.degrees(math.atan2(*(J[i + 1] - J[i])[::-1])) for i in range(NB)]
        names = []
        for i in range(NB):
            nm = f"n{hid}{i}"
            if i == 0:
                sk.bone(nm, "than", J[0][0], J[0][1], th[0], seg, sz, sz)
            else:
                sk.bone(nm, names[-1], seg, 0, th[i] - th[i - 1], seg)
            names.append(nm)
        hb = sk.bone("h" + hid, names[-1], seg, 0, h["psi"] - th[-1], hp.width * 0.8)
        ax, ay = ANCHOR["head_" + kind]
        hw = hp.width
        GEO = HEAD_GEO_K.get(kind, HEAD_GEO)
        JAW_SC = JAW_SC_K.get(kind, globals()["JAW_SC"])
        gx, gy = GEO["jaw"]
        jb = sk.bone("j" + hid, hb, gx * hw, gy * hw, 0, jp.width * 0.8, JAW_SC, JAW_SC)
        # bờm: hai đốt chĩa ra sau gáy
        mxf, myf, ytop = MANE[kind]
        ML = hp.width * 0.19
        bx0, by0 = (mxf - ax) * hp.width, (ay - myf) * hp.height
        sk.bone(f"b{hid}0", hb, bx0, by0, 180, ML)
        sk.bone(f"b{hid}1", f"b{hid}0", ML, 0, 0, ML)
        # râu: sau (xa) và trước (gần), mỗi sợi 3 đốt
        wp = pc["whisker"]
        wseg = wp.width / WB
        whinfo = {}
        for tag, (wx, wy), rot0, wsz in (("b", GEO["wh_b"], WHISK_ROT["b"], WHISK_SC["b"]), ("f", GEO["wh_f"], WHISK_ROT["f"], WHISK_SC["f"])):
            prev = hb
            wsc = wsz * (0.9 if kind == "n" else 1.0)
            whinfo[tag] = (wx * hw, wy * hw, rot0, wsc)
            for i in range(WB):
                nm = f"r{hid}{tag}{i}"
                if i == 0:
                    sk.bone(nm, prev, wx * hw, wy * hw, rot0, wseg, wsc, wsc)
                else:
                    sk.bone(nm, prev, wseg, 0, WREST, wseg)
                prev = nm
        # slot sau -> trước: râu sau, cổ, lòng miệng, hàm, đầu, râu trước
        def whisker_slot(tag):
            sl = sk.slot(f"r{hid}{tag}", f"r{hid}{tag}0", "whisker")
            pts, tris, axis, xs = strip_mesh(wp, WB)
            P = [(px, axis - py) for px, py in pts]
            wts = [[(f"r{hid}{tag}{b}", w) for b, w in chain_weights(px, wseg, WB)] for px, _ in pts]
            sk.mesh(sl, "whisker", wp, pts, tris, wts, (P, {f"r{hid}{tag}{i}": (i * wseg, 0, 0) for i in range(WB)}))

        whisker_slot("b")
        sl = sk.slot("c" + hid, names[0], "neck_" + kind)
        pts, tris, axis, xs = strip_mesh(neck, NB)
        P = [(px, (axis - py) * NECK_THICK[kind] * h.get("thick", 1.0)) for px, py in pts]
        wts = [[(names[b], w) for b, w in chain_weights(px, seg, NB)] for px, _ in pts]
        sk.mesh(sl, "neck_" + kind, neck, pts, tris, wts, (P, {names[i]: (i * seg, 0, 0) for i in range(NB)}))
        mp = pc["mouth"]
        mx, my = GEO["mouth"]
        sk.slot("m" + hid, hb, "mouth")
        mc, mr = MOUTH_G
        mx0, mx1 = gx * hw - 0.03 * hw, 0.40 * hw
        mpts, mP, mW = [], [], []
        # thịt trong miệng ĐI THEO HÀM DƯỚI (người dùng dặn 2026-11-10): hàng dưới bám hàm 100%; hàng trên chỉ bám đầu ở sát bản lề
        # (màng khoé miệng), ra phía mõm thì theo hàm luôn và mỏng dần. Phần nào ở lại với đầu mà thò ra khỏi hàm trên sẽ trông như
        # cái lưỡi thứ hai. Hai bảng dưới là hàm theo vị trí dọc miệng (0 = bản lề, 1 = mõm), nội suy cho lưới dày hơn.
        m_ytop = (-0.015, -0.022, -0.036, -0.050, -0.064)
        m_qtop = (0.0, 0.35, 0.80, 1.0, 1.0)
        fu5 = np.linspace(0, 1, 5)
        for r in range(mr):
            for cc in range(mc):
                fu = cc / (mc - 1)
                X = mx0 + (mx1 - mx0) * fu
                yt, yb = float(np.interp(fu, fu5, m_ytop)) * hw, -0.112 * hw
                k = r / (mr - 1)
                mpts.append(((0.10 + 0.87 * fu) * mp.width, (0.03 + 0.94 * k) * mp.height))   # lấy cả viền mực mép trên, mép dưới, mép trước
                mP.append((X, yt + (yb - yt) * k))
                q = float(np.interp(fu, fu5, m_qtop))
                wj = q + (1.0 - q) * k
                mW.append([(hb, 1.0 - wj), (jb, wj)])
        mtris = grid_tris(mc - 1, mr - 1)
        sk.mesh("m" + hid, "mouth", mp, mpts, mtris, mW, (mP, {hb: (0, 0, 0), jb: (gx * hw, gy * hw, 0, JAW_SC)}))
        # xương miệng: chỗ và hướng nhả của đầu này (VFX của game bám vào đây; tia, đạn không vẽ trong rig)
        jx0, jy0 = MUZZLE[0] * hw, MUZZLE[1] * hw
        sk.bone("mieng_" + hid, hb, jx0, jy0, JROT, 60)
        jx, jy = ANCHOR["jaw_" + kind]
        sk.slot("j" + hid, jb, "jaw_" + kind)
        # hàm dưới: lưới hai xương như con gốc (mục 3b): vùng họng sát bản lề (góc sau trên của mảnh) bám xương đầu, cằm và mõm bám
        # xương hàm, giữa chia dần. Há miệng thì da họng giãn ra, bản lề không hở; mảnh cứng (bản 3) thì khe bản lề lộ góc nhọn.
        jgx, jgy = JAW_G
        jpts, jP, jW = [], [], []
        for r in range(jgy + 1):
            for cc in range(jgx + 1):
                u, v = cc / jgx, r / jgy                         # u: 0 = đuôi hàm (bản lề), 1 = mõm; v: 0 = mép trên (nướu), 1 = cằm
                px, py = jp.width * u, jp.height * v
                X, Y = (px - jx * jp.width) / JAW_SC, (jy * jp.height - py) / JAW_SC   # hệ xương hàm (tỉ lệ 0,86: chia cho tỉ lệ)
                wh = ease((0.34 - u) / 0.26, "io") * (1.0 - 0.45 * v)   # họng (sau, trên) theo đầu; càng xuống cằm, càng ra mõm càng theo hàm
                wh = min(0.88, wh)
                jpts.append((px, py))
                jP.append((X, Y))
                jW.append([(hb, wh), (jb, 1.0 - wh)])
        jtris = grid_tris(jgx, jgy)
        sk.mesh("j" + hid, "jaw_" + kind, jp, jpts, jtris, jW, (jP, {jb: (0, 0, 0), hb: (-gx * hw / JAW_SC, -gy * hw / JAW_SC, 0, 1.0 / JAW_SC)}))
        lim_ = pc["tongue_" + kind]
        lseg = lim_.width / LB
        lx0, ly0 = TONGUE_AT[0] * jp.width, TONGUE_AT[1] * jp.height
        ln = [f"l{hid}{i}" for i in range(LB)]
        sk.bone(ln[0], jb, lx0, ly0, TONGUE_ROT, lseg)
        for i in range(1, LB):
            sk.bone(ln[i], ln[i - 1], lseg, 0, 0, lseg)
        sk.slot("l" + hid, ln[0], "tongue_" + kind, alpha=0.0)
        lpts, ltris, laxis, _ = strip_mesh(lim_, LB)
        lP = [(px, laxis - py) for px, py in lpts]
        lwts = [[(ln[b], w) for b, w in chain_weights(px, lseg, LB)] for px, _ in lpts]
        sk.mesh("l" + hid, "tongue_" + kind, lim_, lpts, ltris, lwts, (lP, {ln[i]: (i * lseg, 0, 0) for i in range(LB)}))
        sk.slot("h" + hid, hb, "head_" + kind)
        gx_, gy_ = HEAD_G
        hpts, hP, hw_ = [], [], []
        for r in range(gy_ + 1):
            for cc in range(gx_ + 1):
                px, py = hp.width * cc / gx_, hp.height * r / gy_
                u, v = cc / gx_, r / gy_
                m = ease((mxf - u) / 0.16, "io") * ease((v - ytop + 0.06) / 0.12, "io")
                tip = ease((mxf - 0.14 - u) / 0.16, "io")
                hpts.append((px, py))
                hP.append((px - ax * hp.width, ay * hp.height - py))
                hw_.append([(hb, 1 - m), (f"b{hid}0", m * (1 - tip)), (f"b{hid}1", m * tip)])
        htris = grid_tris(gx_, gy_)
        sk.mesh("h" + hid, "head_" + kind, hp, hpts, htris, hw_,
                (hP, {hb: (0, 0, 0), f"b{hid}0": (bx0, by0, 180), f"b{hid}1": (bx0 - ML, by0, 180)}))
        # mí mắt: dò chỗ đặt phủ kín con mắt (fit_lid); mặc định ẩn (chớp, nhắm bằng alpha slot)
        lp = pc["lid_" + kind]
        lcx, lcy, lrot, lsc = fit_lid(kind, hp, lp)
        sk.slot("e" + hid, hb, "lid_" + kind, alpha=0.0)
        sk.region("e" + hid, "lid_" + kind, lp, lcx - ax * hp.width, ay * hp.height - lcy, lrot, lsc, lsc)
        whisker_slot("f")
        info["heads"][hid] = dict(h, seg=seg * sz, E=E, th=th, J0=J[0], names=names, hw=hw, last="r%sf" % hid, wh=whinfo, wseg=wseg,
                                  tongue=dict(x=lx0, y=ly0, seg=lseg, jx=gx * hw, jy=gy * hw),
                                  jet=dict(x=jx0, y=jy0))

    for h in HEADS[:2]:
        head(h)
    lane("mid")
    for h in HEADS[2:]:
        head(h)
    last_body = sk.slots[-1]["name"]
    sk.clip("cat", last_body, [(-2400, CLIPY), (2400, CLIPY), (2400, 3200), (-2400, 3200)])

    # --- nước trước (không bị cắt) ---
    sk.bone("band", "nuoc", 0, -6)
    sk.bone("band2", "nuoc", 40, 22)
    sk.slot("band2", "band2", "band")
    ribbon("band2", "band2", "band", -1.28, 1.0)
    lane("front")
    lane("sweep")
    sk.slot("band", "band", "band")
    ribbon("band", "band", "band", 1.2, 0.92)
    sk.bone("ripple", "nuoc", 10, -44)
    sk.slot("ripple", "ripple", "ripple")
    ribbon("ripple", "ripple", "ripple", 1.22, 1.0)
    for i in range(N_RING):
        sk.bone(f"rg{i}", "nuoc", 0, 60)
        sk.slot(f"rg{i}", f"rg{i}", "ring", alpha=0.0)
        sk.region(f"rg{i}", "ring", pc["ring"], 0, 0)
    for i in range(N_CROWN):
        sk.bone(f"cr{i}", "nuoc", 0, 60)
        sk.slot(f"cr{i}", f"cr{i}", "crown", alpha=0.0)
        sk.region(f"cr{i}", "crown", pc["crown"], 0, pc["crown"].height / 2 - 12)
    for i in range(N_DROP):
        d = ("drop_a", "drop_b", "drop_c")[i % 3]
        sk.bone(f"dr{i}", "nuoc", 0, 0)
        sk.slot(f"dr{i}", f"dr{i}", d, alpha=0.0)
        sk.region(f"dr{i}", d, pc[d], 0, 0)
    return sk, info


# ---------------------------------------------------------------- 5. clip
class Clip:
    def __init__(self, name, dur, info, loop=False):
        self.name, self.dur, self.info, self.loop = name, dur, info, loop
        self.n = int(round(dur * FPS)) + 1
        self.ts = np.arange(self.n) / FPS
        self.bones, self.slots = {}, {}
        self.fx = []  # (t, x, y, cỡ, loại)
        self.events = []  # (t, tên, chuỗi): mốc cho VFX và âm thanh của game

    def key(self, bone, kind, ts, vs, tol):
        ts, vs = np.asarray(ts, float), np.asarray(vs, float)
        idx = rdp(ts, vs, tol)
        self.bones.setdefault(bone, {})[kind] = [(float(ts[i]), vs[i]) for i in idx]

    def raw(self, bone, kind, keys):
        self.bones.setdefault(bone, {})[kind] = [(float(t), np.atleast_1d(np.array(v, float))) for t, v in keys]

    def alpha(self, slot, keys):
        self.slots.setdefault(slot, {})["alpha"] = [(float(t), float(v)) for t, v in keys]


def idle_sway(h, t, amp=1.0):
    ax, ay, aa = h["sway"]
    w = 2 * math.pi / (2 * TW)
    p = 2 * math.pi * h["ph"]
    # trừ giá trị tại t = 0: giây 0 idle đúng dáng gốc (bóng dáng khung 0 = concept, IoU đo được; 2026-11-11), vòng lặp vẫn kín vì hằng
    return np.array([ax * (math.sin(w * t + p) - math.sin(p)) * amp, ay * (math.sin(2 * w * t + p * 1.7) - math.sin(p * 1.7)) * amp,
                     aa * (math.sin(w * t + p + 1.1) - math.sin(p + 1.1)) * amp, 0.0])


def animate_heads(clip, tracks, sway=None, base=None, tongue=None):
    """tracks[id](t) -> (dx, dy, dgóc, hàm há độ) so với dáng nghỉ; sway(t) 0..1: phần đung đưa idle cộng thêm;
    base[id](t) -> độ chìm thêm của chỗ trồi (không dùng), trả vị trí thế giới của đầu theo khung (cho hiệu ứng nước)."""
    info = clip.info
    out = {}
    dt = 1.0 / FPS
    off = 0.0 if clip.loop else clip.dur
    tp = clip.ts - off
    for h in HEADS:
        hid = h["id"]
        H = info["heads"][hid]
        seg, E = H["seg"], H["E"]
        tr = tracks.get(hid)
        vals, sws = [], []
        for t in clip.ts:
            v = np.array(tr(t), float) if tr else np.zeros(4)
            if len(v) < 4:
                v = np.concatenate([v, np.zeros(4 - len(v))])
            sw = 1.0 if sway is None else sway(t)
            vals.append(v + idle_sway(h, t - off, sw))
            sws.append(sw)
        vals = np.array(vals)
        Hp = np.array(h["H"], float) + vals[:, :2]
        psi = h["psi"] + vals[:, 2]
        d = np.hypot(*(Hp - np.array(E)).T)
        pa = psi + h["arr"]
        uH = np.stack([np.cos(np.radians(pa)), np.sin(np.radians(pa))], axis=1)
        C2 = follow(Hp - uH * (d * h.get("kb", 0.42))[:, None], 0.085, dt, clip.n if clip.loop else 0)
        th_all, J0 = [], []
        for i in range(clip.n):
            # sóng dọc cổ nhân bao sin²(πt/D): giây 0 và cuối mỗi clip cổ đúng đường tâm concept (khung 0 idle = dáng gốc, 2026-11-11)
            wv = (WAVE_A * h["size"] * (0.4 + 0.6 * sws[i]) * math.sin(math.pi * clip.ts[i] / clip.dur) ** 2,
                  2 * math.pi * tp[i] / (2 * TW) + h["ph"] * 6.28 + 0.8)
            J = neck_joints(E, h["dirE"], Hp[i], pa[i], seg, NB, C2=C2[i], wave=wv, ka=h.get("ka", 0.52), rest=h.get("rest"))
            th_all.append([math.atan2(*(J[k + 1] - J[k])[::-1]) for k in range(NB)])
            J0.append(J[0])
        th_all = np.degrees(np.unwrap(np.array(th_all), axis=0))
        # không cho góc nhảy vòng so với dáng gốc
        th0 = np.array(H["th"])
        th_all += np.round((th0 - th_all[0]) / 360.0) * 360.0
        J0 = np.array(J0)
        names = H["names"]
        clip.key(names[0], "translate", clip.ts, J0 - np.array(H["J0"]), 0.6)
        clip.key(names[0], "rotate", clip.ts, th_all[:, 0] - th0[0], 0.25)
        for k in range(1, NB):
            rel = (th_all[:, k] - th_all[:, k - 1]) - (th0[k] - th0[k - 1])
            clip.key(names[k], "rotate", clip.ts, rel, 0.25)
        hrel = (psi - th_all[:, -1]) - (h["psi"] - th0[-1])
        clip.key("h" + hid, "rotate", clip.ts, hrel, 0.25)
        breathe = BREATHE[0] + BREATHE[1] * np.sin(2 * math.pi * tp / (2 * TW) + h["ph"] * 6.28)  # miệng hé, thở
        clip.key("j" + hid, "rotate", clip.ts, -(vals[:, 3] + breathe) + JAW_CLOSE.get(h["kind"], 0.0), 0.4)
        if tongue and hid in tongue:  # tongue[hid] = giờ thè lưỡi: lưỡi tuồn ra rồi rũ theo trọng lực, lắc theo đầu
            T = H["tongue"]
            jr = psi - (vals[:, 3] + breathe)
            c0, s0 = np.cos(np.radians(psi)), np.sin(np.radians(psi))
            jo = Hp + np.stack([c0 * T["jx"] - s0 * T["jy"], s0 * T["jx"] + c0 * T["jy"]], axis=1) * h["size"]
            c1, s1 = np.cos(np.radians(jr)), np.sin(np.radians(jr))
            anc = jo + np.stack([c1 * T["x"] - s1 * T["y"], s1 * T["x"] + c1 * T["y"]], axis=1) * h["size"] * JAW_SC_K.get(h["kind"], JAW_SC)
            offs = rope(anc, jr, [TONGUE_ROT] + [0.0] * (LB - 1), T["seg"] * h["size"] * JAW_SC_K.get(h["kind"], JAW_SC), clip.loop, k0=0.10, k1=0.03, zeta=0.55,
                        wind=lambda tsec, i: np.array([0.0, -TONGUE_G]), lim=(38.0, 55.0))
            for k in range(LB):
                clip.key(f"l{hid}{k}", "rotate", clip.ts, offs[:, k], 0.4)
            t_on = tongue[hid]
            clip.alpha("l" + hid, [(0, 0.0), (max(0.0, t_on - 0.034), 0.0), (t_on, 1.0), (clip.dur, 1.0)])
            clip.raw(f"l{hid}0", "scale", [(0, (0.25, 1)), (t_on, (0.25, 1)), (t_on + 0.16, (1.06, 1)), (t_on + 0.26, (1, 1))])
        # râu: trễ theo góc đầu và theo vận tốc dọc của đầu
        vy = np.gradient(Hp[:, 1], dt)
        vx = np.gradient(Hp[:, 0], dt)
        if not clip.loop:
            vy[0] = vx[0] = 0.0  # clip không lặp bắt đầu từ dáng đứng: râu, bờm chưa lệch ở khung đầu
        cs_, sn_ = np.cos(np.radians(psi)), np.sin(np.radians(psi))
        for tag in ("b", "f"):
            lx, ly, rot0, wsc = H["wh"][tag]
            anc = Hp + np.stack([cs_ * lx - sn_ * ly, sn_ * lx + cs_ * ly], axis=1) * h["size"]
            ph0 = h["ph"] * 6.28 + (1.3 if tag == "b" else 0.0)
            wind = lambda tsec, i, ph0=ph0: np.array([WIND * (i / WB) ** 1.5 * math.sin(2 * math.pi * (tsec - off) / TW + ph0 - i * 0.6), 0.0])
            offs = rope(anc, psi, [rot0] + [WREST] * (WB - 1), H["wseg"] * wsc * h["size"], clip.loop, wind=wind)
            # nối clip không giật ở ngọn râu: clip lặp (idle, nướng trước) ghi dáng râu khung 0; clip không lặp hoà 0,3 s cuối về đó
            # (đo trên đỉnh lưới: trước đó lệch 18–34 px ở ngọn râu; bài học DAC_TA mục 5)
            key0 = (hid, tag)
            if clip.loop:
                info.setdefault("rope0", {})[key0] = offs[0].copy()
            elif key0 in info.get("rope0", {}):
                nb = min(clip.n - 1, int(round(0.3 * FPS)))
                tgt = info["rope0"][key0]
                for i in range(nb):
                    w_ = ease((i + 1) / nb, "io")
                    f = clip.n - nb + i
                    offs[f] = offs[f] * (1 - w_) + tgt * w_
            for k in range(WB):
                clip.key(f"r{hid}{tag}{k}", "rotate", clip.ts, offs[:, k], 0.4)
        for k in range(2):
            lag = follow(np.stack([psi, vy, vx], axis=1), 0.09 + 0.07 * k, dt, clip.n if clip.loop else 0)
            r = (lag[:, 0] - psi) * (0.55 + 0.35 * k) + lag[:, 1] * 0.007 * (1 + 0.6 * k)
            r += (2.2 + 1.8 * k) * np.sin(2 * math.pi * tp / (TW / 2) + h["ph"] * 6.28 - k * 1.1)
            clip.key(f"b{hid}{k}", "rotate", clip.ts, np.clip(r, -18, 18), 0.4)
        out[hid] = dict(H=Hp, psi=psi, J0=J0)
    return out


def animate_aura(clip):
    """clip lặp `aura` (dài 2·TW): mọi chuyển động tuần hoàn của nước và của phần thân nằm trong nước: băng chuyền sóng (mỗi cuộn
    dâng tại chỗ, mào tự cuộn, trôi nhẹ, mờ vào mờ ra; hai bản sao lệch nửa chu kỳ), mảng nền phập phồng, ba dải nước uốn sóng chạy,
    vòng thân phồng chạy dọc vòm, đuôi quẫy. Runtime phủ clip này lên mọi clip chính theo đồng hồ chung (AtomikPose.Overlay: xoay,
    dời cộng; tỉ lệ, độ đậm nhân), nên nước liền qua mọi lần đổi clip và khoá nước chỉ lưu một lần (con gốc chép vào cả 18 clip:
    hơn nửa số khoá). Clip chính chỉ khoá phần phụ thuộc clip (animate_water): nước nở / tan, lặng, thân chìm."""
    info = clip.info
    D = clip.dur
    US = (0.0, 0.16, 0.5, 0.8, 0.96, 0.999)
    CURL = (-0.55, -0.30, 0.25, 0.60, 0.95, 1.0)   # độ cuộn của mào theo đời sóng: mới sinh còn duỗi, càng về sau càng cuộn chặt
    AJ = (8.0, 18.0, 26.0, 20.0)                   # góc mỗi đốt khi cuộn hết cỡ (lớn nhất ở gần mào)
    for wv in info["waves"]:
        b, ph, s_ = wv["bone"], wv["ph"], wv["s"]
        kc, rise, dx = wv.get("kc", 1.0), wv.get("rise", 1.0), wv.get("dx", 46.0)
        hh = wv["h"]
        tr, scl, al = [], [], []
        rots = [[] for _ in range(NC)]
        k0 = int(math.floor(-ph)) - 1
        for cyc in range(k0, int(math.ceil(D / TW)) + 2):
            for u, cu in zip(US, CURL):
                t = (cyc + ph + u) * TW  # giữ cả khoá ngoài [0, D]: _close cần chúng để nội suy đúng hai mép clip
                g = 0.6 + 0.4 * ease(u / 0.45, "out")
                tr.append((t, ((-1 if wv["flip"] else 1) * dx * (u - 0.3), -0.24 * hh * s_ * rise * (1 - ease(u / 0.5, "out")) + 0.03 * hh * s_ * u)))
                if u in (0.0, 0.5, 0.8, 0.999):
                    scl.append((t, (g, g)))
                al.append((t, ease(u / 0.16, "io") * (1 - ease((u - 0.8) / 0.16, "io")) * wv.get("a", 1.0)))
                if u in (0.0, 0.5, 0.8, 0.999):
                    for k in range(NC):
                        rots[k].append((t, wv["sense"] * AJ[k] * cu * kc))
        clip.raw(b, "translate", _close(tr, D, ph, None))
        clip.raw(b, "scale", _close(scl, D, ph, None))
        if kc:
            for k in range(NC):
                clip.raw(f"{b}{k}", "rotate", _close(rots[k], D, ph, None))
        clip.alpha(b, _close([(t, np.array([v])) for t, v in al], D, ph, None, scalar=True))
    # mảng nước nền và dải mặt nước: phập phồng, trôi ngang chậm
    ts = clip.ts
    tp = ts
    w = 2 * math.pi / TW
    clip.key("mound", "scale", ts, np.stack([1 + 0.025 * np.sin(w * tp), 1 + 0.05 * np.sin(w * tp + 1.2)], axis=1), 0.004)
    clip.key("band", "translate", ts, np.stack([16 * np.sin(w * tp * 0.5), 5 * np.sin(w * tp + 0.6)], axis=1), 0.5)
    clip.key("band2", "translate", ts, np.stack([-22 * np.sin(w * tp * 0.5 + 0.8), 6 * np.sin(w * tp + 2.2)], axis=1), 0.5)
    clip.key("ripple", "translate", ts, np.stack([12 * np.sin(w * tp * 0.5 + 2.0), 3 * np.sin(w * tp + 1.0)], axis=1), 0.5)
    for bone, amp, kph, dirn in (("band", 10.0, 0.0, 1), ("band2", 8.0, 1.7, -1), ("ripple", 7.0, 0.9, 1)):
        for i in range(NRB):  # xương dọc dải nhấp nhô lệch pha 0,8 rad: sóng chạy dọc mào dải
            clip.key(f"{bone}_{i}", "translate", ts, np.stack([3 * np.cos(w * tp - dirn * i * 0.8 + kph), amp * np.sin(w * tp - dirn * i * 0.8 + kph)], axis=1), 0.3)
    # vòng thân, đuôi: nhân bao sin²(πt/D) để giây 0 (và D) đúng dáng gốc (bóng dáng khung 0 = concept, 2026-11-11); vòng lặp vẫn kín
    env = np.sin(np.pi * ts / D) ** 2
    clip.key("coil", "translate", ts, np.stack([4 * np.sin(w * tp * 0.5), 9 * np.sin(w * tp * 0.5 + 0.5)], axis=1) * env[:, None], 0.5)
    clip.key("coil", "rotate", ts, 2.2 * np.sin(w * tp * 0.5 + 1.0) * env, 0.2)
    for i, (nm, ux, uy, _, _) in enumerate(info["coil"]):  # chỗ phồng chạy từ chân trái vòm sang chân phải, mỗi điểm trễ 0,9 rad
        rad = 11 * np.sin(w * tp * 0.5 - i * 0.9) * env
        tan = 6 * np.cos(w * tp * 0.5 - i * 0.9) * env
        clip.key(nm, "translate", ts, np.stack([ux * rad - uy * tan, uy * rad + ux * tan], axis=1), 0.3)
    clip.key("tail", "rotate", ts, 6 * np.sin(w * tp * 0.5 + 2.0) * env, 0.3)
    for i in range(1, TB):  # sóng quẫy chạy ra chóp, biên độ lớn dần
        clip.key(f"tail{i}", "rotate", ts, (1.5 + 1.7 * i) * np.sin(w * tp - i * 0.75 + 2.0) * env, 0.25)
    clip.key("tail", "translate", ts, np.stack([0 * tp, 8 * np.sin(w * tp * 0.5 + 2.6) * env], axis=1), 0.5)


def animate_water(clip, grow=None, calm=None, sink=None):
    """phần nước phụ thuộc clip chính (cộng / nhân lên clip aura): grow(t): tỉ lệ cả vùng nước (xương `nuoc`); calm(t): 1 = sóng bình
    thường, 0 = sóng lặng (ép dẹt xương `song` và làm mờ mọi slot sóng; runtime nhân với độ đậm của aura); sink(t): vòng thân, đuôi
    chìm xuống dưới mặt nước (đơn vị rig; dời cộng thêm vào dao động của aura)."""
    ts = clip.ts
    if grow:
        g = np.array([grow(t) for t in ts])
        clip.key("nuoc", "scale", ts, np.stack([g, np.maximum(0.02, g)], axis=1), 0.004)
    if calm:
        c = np.clip(np.array([calm(t) for t in ts]), 0.0, 1.0)
        clip.key("song", "scale", ts, np.stack([1 + 0 * c, 0.55 + 0.45 * c], axis=1), 0.004)
        idx = rdp(ts, c, 0.01)
        if any(c[i] < 0.995 for i in idx):
            for wv in clip.info["waves"]:
                clip.alpha(wv["bone"], [(float(ts[i]), float(c[i])) for i in idx])
    if sink:
        dn = np.array([sink(t) for t in ts])
        clip.key("coil", "translate", ts, np.stack([0 * dn, -dn * 0.8], axis=1), 0.5)
        clip.key("tail", "translate", ts, np.stack([-dn * 0.5, -dn * 1.3], axis=1), 0.5)


def _close(keys, D, ph, _, scalar=False):
    """sắp khoá theo giờ, thêm khoá đúng t = 0 và t = D (nội suy tuyến tính từ hai khoá kề, kể cả ngoài khoảng)."""
    keys = sorted(keys, key=lambda k: k[0])
    ts = np.array([k[0] for k in keys])
    vs = np.array([np.atleast_1d(k[1]) for k in keys], float)
    out = []
    for t_edge in (0.0, D):
        if not np.any(np.abs(ts - t_edge) < 1e-4):
            v = np.array([np.interp(t_edge, ts, vs[:, c]) for c in range(vs.shape[1])])
            out.append((t_edge, v))
    allk = sorted(list(zip(ts, vs)) + out, key=lambda k: k[0])
    return [(float(t), (float(v[0]) if scalar else v)) for t, v in allk if -1e-6 <= t <= D + 1e-6]


def animate_fx(clip):
    """vương miện nước, giọt, vòng sóng theo danh sách clip.fx = [(t, x, y, cỡ, loại)]; loại: 'toe' (trồi / bổ), 'vong'."""
    rng = np.random.RandomState(zlib.crc32(clip.name.encode()) % 10000)
    pc = clip.info["pieces"]
    cr = {i: [] for i in range(N_CROWN)}
    dr = {i: [] for i in range(N_DROP)}
    rg = {i: [] for i in range(N_RING)}
    free_c, free_d, free_r = [0.0] * N_CROWN, [0.0] * N_DROP, [0.0] * N_RING

    def take(free, t, life):
        i = min(range(len(free)), key=lambda k: free[k])
        if free[i] > t + 1e-6:
            return None
        free[i] = t + life + 0.05
        return i

    for t, x, y, size, kind in sorted(clip.fx):
        if kind in ("toe", "toe_nho", "giot"):
            i = take(free_c, t, 0.62) if kind != "giot" else None
            if i is not None:
                s = size
                cr[i] += [("T", t - 0.001, x, y), ("S", t, 0.55 * s, 0.05 * s, 0), ("A", t, 0.0), ("A", t + 0.04, 1.0), ("S", t + 0.10, 1.05 * s, 1.18 * s, 0),
                          ("S", t + 0.20, 1.0 * s, 1.0 * s, 0), ("A", t + 0.36, 1.0), ("S", t + 0.6, 1.18 * s, 0.25 * s, 0), ("A", t + 0.6, 0.0)]
            nd = {"toe": 5, "toe_nho": 3, "giot": 4}[kind]
            for _ in range(nd):
                j = take(free_d, t, 0.75)
                if j is None:
                    break
                a = math.radians(rng.uniform(40, 140) if kind != "giot" else rng.uniform(-5, 115))
                v = rng.uniform(520, 900) * (0.6 + 0.4 * size)
                life = rng.uniform(0.5, 0.72)
                if kind != "giot":
                    life = min(life, max(0.16, v * math.sin(a) / 1500 - 0.02))
                ks = []
                for q in np.linspace(0, 1, 6):
                    tt = q * life
                    ks.append(("T", t + tt, x + math.cos(a) * v * tt, y + 30 + math.sin(a) * v * tt - 1500 * tt * tt))
                    ang = math.degrees(math.atan2(math.sin(a) * v - 3000 * tt, math.cos(a) * v)) - 90
                    ks.append(("R", t + tt, ang))
                sc = rng.uniform(0.7, 1.15) * (0.7 + 0.3 * size)
                dr[j] += ks + [("S", t, sc, sc, 0), ("A", t - 0.001, 0.0), ("A", t + 0.03, 1.0), ("A", t + life - 0.12, 1.0), ("A", t + life, 0.0)]
        if kind in ("toe", "vong"):
            i = take(free_r, t, 0.7)
            if i is not None:
                s = size
                rg[i] += [("T", t - 0.001, x, y - 8), ("S", t, 0.25 * s, 0.25 * s, 0), ("A", t, 0.0), ("A", t + 0.05, 0.9), ("S", t + 0.65, 1.25 * s, 1.25 * s, 0),
                          ("A", t + 0.4, 0.8), ("A", t + 0.65, 0.0)]

    def put(prefix, pool, home):
        for i, ks in pool.items():
            if not ks:
                continue
            b = f"{prefix}{i}"
            T = sorted([(k[1], (k[2] - home[0], k[3] - home[1])) for k in ks if k[0] == "T"], key=lambda k: k[0])
            S = sorted([(k[1], (k[2], k[3])) for k in ks if k[0] == "S"], key=lambda k: k[0])
            R = sorted([(k[1], k[2]) for k in ks if k[0] == "R"], key=lambda k: k[0])
            A = sorted([(k[1], k[2]) for k in ks if k[0] == "A"], key=lambda k: k[0])
            fix = lambda L: [(max(0.0, min(clip.dur, t)), v) for t, v in L]
            if T:
                clip.raw(b, "translate", fix(T))
            if S:
                clip.raw(b, "scale", fix(S))
            if R:
                clip.raw(b, "rotate", fix(R))
            clip.alpha(b, [(0.0, 0.0)] + fix(A) if A[0][0] > 0 else fix(A))

    put("cr", cr, (0, 60))
    put("dr", dr, (0, 0))
    put("rg", rg, (0, 60))


WY = CLIPY + 6  # độ cao mặt nước cho hiệu ứng


def K(*keys):
    return Track(keys)


def lids(clip, sched):
    """nhắm mắt: sched = {đầu: [(từ, tới), ...]} (giây); bật tắt mảng mí bằng alpha slot, 1 khung chuyển."""
    for hid, spans in sched.items():
        ks = [(0.0, 1.0 if spans and spans[0][0] <= 0 else 0.0)]
        for t0, t1 in spans:
            if t0 > 0:
                ks += [(max(0.0, t0 - 0.034), 0.0), (t0, 1.0)]
            ks.append((min(clip.dur, t1), 1.0))
            if t1 < clip.dur - 0.05:
                ks.append((t1 + 0.034, 0.0))
        clip.alpha("e" + hid, ks)


def clip_aura(info):
    c = Clip("aura", 2 * TW, info, loop=True)
    animate_aura(c)
    return c


def clip_idle(info):
    c = Clip("idle", 2 * TW, info, loop=True)
    # điểm phá nhịp: mỗi vòng mỗi đầu táp miệng một cái (0,45 s) ở giờ riêng, kèm gật nhẹ; con gốc dùng cú thè lưỡi 0,4 s cho việc này
    z = (0, 0, 0, 0)
    acc = {}
    for h in HEADS:
        ta = 0.3 + ((h["ph"] * 2.7 + 0.75) % 1.0) * 2.2
        acc[h["id"]] = K((0, z, "lin"), (ta, z, "lin"), (ta + 0.10, (6, -4, -3, 15), "out"), (ta + 0.20, (0, 2, 1, 2), "in"), (ta + 0.30, (4, -2, -2, 10), "out"),
                         (ta + 0.45, z, "io"), (2 * TW, z, "lin"))
    animate_heads(c, acc)
    blink = {}
    for h in HEADS:  # mỗi đầu chớp một lần mỗi vòng, lệch giờ nhau; thủ lĩnh chớp đôi
        t = 0.4 + ((h["ph"] * 2.7 + 0.3) % 1.0) * 2.3
        blink[h["id"]] = [(t, t + 0.11)] + ([(t + 0.28, t + 0.38)] if h["id"] == "k" else [])
    lids(c, blink)
    animate_water(c)
    animate_fx(c)
    return c


def clip_xuat_hien(info):
    """mặt nước phẳng lặng, một vòng sóng loang, vũng nước nở ra; bốn đầu vọt lên lần lượt từ hai bên vào giữa, mỗi đầu toé một
    vương miện nước; đầu thủ lĩnh trồi lên sau cùng, chậm và cao; cả năm đầu gầm rồi về dáng đứng."""
    D = 3 * TW
    c = Clip("appear", D, info)
    rise = {"d": 1.05, "b": 1.25, "c": 1.50, "a": 1.72, "k": 2.35}
    tr = {}
    for h in HEADS:
        hid, t0 = h["id"], rise[h["id"]]
        Hx, Hy = h["H"]
        E = info["heads"][hid]["E"]
        under = (E[0] - Hx - 60 * math.cos(math.radians(h["dirE"])), (E[1] - 520) - Hy, 90 - h["psi"] - 20, 0)  # đầu nằm dưới mặt nước, chúc lên
        top = (0.25 * (E[0] - Hx), 90 if hid != "k" else 120, 22, 34)                                            # vọt quá đà, há miệng
        if hid == "k":
            tr[hid] = K((0, under, "lin"), (t0, under, "lin"), (t0 + 0.55, top, "out"), (t0 + 0.95, (0, -20, -6, 8), "io"), (3.75, (-30, 26, 10, 46), "io"),
                        (4.25, (-30, 26, 10, 46), "lin"), (D, (0, 0, 0, 0), "io"))
        else:
            tr[hid] = K((0, under, "lin"), (t0, under, "lin"), (t0 + 0.22, top, "out"), (t0 + 0.6, (0, -14, -5, 6), "io"), (t0 + 0.9, (0, 0, 0, 0), "io"),
                        (3.55, (0, 0, 0, 0), "lin"), (3.85, (-34, 18, 12, 40), "out"), (4.25, (-34, 18, 12, 40), "lin"), (D, (0, 0, 0, 0), "io"))
        c.fx.append((t0 + 0.02, E[0], WY, 1.0 if hid != "k" else 1.35, "toe"))
        c.events.append((t0, "troi", hid))
    c.fx += [(0.15, 0, WY - 30, 0.7, "vong"), (0.55, 0, WY - 30, 1.1, "vong")]
    lids(c, {hid: [(0, t0 + (0.45 if hid != "k" else 0.8))] for hid, t0 in rise.items()})
    animate_heads(c, tr, sway=lambda t: ease((t - 3.2) / 1.4, "io"))
    c.raw("than", "translate", [(0, (0, -500)), (0.7, (0, -500)), (1.0, (0, 0))])
    animate_water(c, grow=lambda t: ease(t / 0.95, "back"), calm=lambda t: ease((t - 0.2) / 0.9, "io"),
                  sink=lambda t: 330 * (1 - ease((t - 1.9) / 0.8, "back")))
    animate_fx(c)
    return c


def clip_tan_cong(info):
    """hai đầu bên phải cắn liên tiếp một-hai: đầu thấp (d) rụt về rồi phóng ra cắn ở 0,45 s, đầu giữa (c) bổ chéo xuống ở 0,68 s;
    thủ lĩnh chồm theo gầm; hai đầu trái ngả ra sau lấy thăng bằng."""
    D = TW
    c = Clip("attack", D, info)
    z = (0, 0, 0, 0)
    tr = {
        "d": K((0, z, "lin"), (0.30, (-150, 40, 16, 4), "io"), (0.38, (-160, 44, 18, 30), "lin"), (0.45, (330, -30, -4, 44), "in"), (0.50, (345, -34, -6, 0), "lin"),
               (0.62, (330, -28, -4, 0), "lin"), (1.05, (-20, 8, 2, 0), "io"), (D, z, "io")),
        "c": K((0, z, "lin"), (0.48, (-130, 90, 22, 6), "io"), (0.60, (-140, 96, 24, 34), "lin"), (0.68, (300, -150, -22, 46), "in"), (0.73, (312, -160, -24, 0), "lin"),
               (0.86, (300, -150, -22, 0), "lin"), (1.25, (-16, 10, 3, 0), "io"), (D, z, "io")),
        "k": K((0, z, "lin"), (0.40, (-60, 30, 10, 10), "io"), (0.62, (90, -10, -8, 36), "out"), (0.95, (80, -6, -6, 30), "lin"), (1.35, (-8, 4, 1, 0), "io"), (D, z, "io")),
        "a": K((0, z, "lin"), (0.45, (-60, 20, 12, 0), "io"), (0.75, (40, 10, -4, 14), "out"), (1.3, z, "io"), (D, z, "lin")),
        "b": K((0, z, "lin"), (0.40, (-50, -10, 10, 0), "io"), (0.70, (30, 14, -5, 12), "out"), (1.25, z, "io"), (D, z, "lin")),
    }
    c.fx += [(0.30, info["heads"]["d"]["E"][0] + 30, WY, 0.55, "toe_nho"), (0.47, info["heads"]["d"]["E"][0] + 120, WY, 0.8, "toe_nho"),
             (0.70, info["heads"]["c"]["E"][0] + 150, WY, 0.9, "toe")]
    c.events += [(0.45, "can", "d"), (0.68, "can", "c")]
    for hid, th_ in (("d", 0.45), ("c", 0.68)):
        c.raw("h" + hid, "scale", [(0, (1, 1)), (th_ - 0.07, (1, 1)), (th_, (1.15, 0.92)), (th_ + 0.07, (0.96, 1.04)), (th_ + 0.2, (1, 1)), (D, (1, 1))])
    animate_heads(c, tr, sway=lambda t: 1 - ease(t / 0.25, "io") * (1 - ease((t - 1.1) / 0.5, "io")))
    animate_water(c)
    animate_fx(c)
    return c


def clip_chieu(info):
    """ngũ long phún thủy: năm đầu ngửa ra sau hít hơi (nước dồn lại, sóng thấp xuống), rồi đồng loạt vươn về phía trước xoè như
    nan quạt, há hết miệng, giữ và rung trong lúc phun (tia nước do lớp hạt của game vẽ); nước dưới chân dâng trào; thu về."""
    D = 2 * TW
    c = Clip("skill", D, info)
    z = (0, 0, 0, 0)
    fan = {"a": (250, 60, 18, 0.00), "b": (300, -30, 2, 0.05), "k": (230, -90, -8, 0.10), "c": (240, -70, -6, 0.04), "d": (250, -10, 6, 0.08)}
    back = {"a": (-90, 60, 26), "b": (-80, 40, 24), "k": (-120, 70, 22), "c": (-150, 80, 26), "d": (-170, 70, 30)}
    tr = {}
    T0, T1, T2 = 1.15, 1.32, 2.35
    for h in HEADS:
        hid = h["id"]
        fx_, fy_, fa_, dl = fan[hid]
        bx, by, ba = back[hid]
        shake = []
        for i, t in enumerate(np.arange(T1 + 0.1 + dl, T2, 2.0 / FPS)):
            s = 1 if i % 2 == 0 else -1
            shake.append((float(t), (fx_ + 6 * s, fy_ + 4 * s, fa_ + 1.6 * s, 50 + 3 * s), "lin"))
        tr[hid] = Track([(0, z, "lin"), (0.5, (bx * 0.6, by * 0.6, ba * 0.6, 8), "io"), (T0 + dl, (bx, by, ba, 22), "io"),
                         (T1 + dl, (fx_, fy_, fa_, 52), "in")] + shake + [(T2 + 0.05, (fx_, fy_, fa_, 30), "lin"), (D - 0.15, z, "io"), (D, z, "lin")])
        c.fx.append((T1 + dl, info["heads"][hid]["E"][0] + 60, WY, 0.8, "toe_nho"))
    c.events += [(T1, "gam", ""), (T2, "het_gam", "")]
    c.fx += [(T1, 0, WY - 30, 1.5, "vong"), (T1 + 0.3, 120, WY, 1.0, "toe"), (T1 + 0.65, -80, WY, 0.9, "toe_nho"), (T1 + 0.9, 220, WY, 0.9, "toe_nho")]
    animate_heads(c, tr, sway=lambda t: 1 - ease(t / 0.4, "io") * (1 - ease((t - 2.6) / 0.5, "io")))
    animate_water(c, grow=lambda t: 1 - 0.16 * ease(t / T0, "io") * (1 - ease((t - T0) / 0.2, "out")) + 0.14 * ease((t - T1) / 0.15, "out") * (1 - ease((t - T2) / 0.6, "io")),
                  calm=lambda t: 1 - 0.5 * ease(t / T0, "io") * (1 - ease((t - T0) / 0.25, "io")))
    animate_fx(c)
    return c


def clip_chieu_phun(info):
    """ngũ long thủy pháo (chỉ phần thân; tia nước là VFX của game, bám xương mieng_<đầu>, bật theo sự kiện 'phun', tắt theo
    'het_phun'): năm đầu rụt về, cúi nén như lò xo (ngậm miệng, nước dưới chân dâng); thủ lĩnh phóng tới há miệng, bốn đầu kia nối
    theo cách nhau 0,06 s, mọi đầu chĩa đúng vào điểm TGT; giữ 1,1 s: đầu bị sức phun đẩy giật lùi rồi gồng rung (hai dáng đổi nhau
    mỗi 2 khung); hết phun thì thở ra rũ xuống rồi về dáng đứng."""
    D = 2 * TW
    c = Clip("cast", D, info)
    z = (0, 0, 0, 0)
    delay = {"k": 0.0, "c": 0.06, "d": 0.12, "a": 0.18, "b": 0.24}
    gather = {"k": (-150, -70, -16), "c": (-170, -40, -14), "d": (-190, 10, -10), "a": (-110, -60, -14), "b": (-120, -10, -10)}
    fire = {"k": (120, -40), "c": (110, -30), "d": (100, 10), "a": (140, 0), "b": (150, 30)}
    F0, E = 1.0, 2.30
    tr = {}
    ts = c.ts
    for h in HEADS:
        hid, sz = h["id"], h["size"]
        jt = info["heads"][hid]["jet"]
        F = F0 + delay[hid]
        gx, gy, ga = gather[hid]
        fx_, fy_ = fire[hid]
        Hf = np.array(h["H"], float) + (fx_, fy_)
        psi_f = h["psi"]
        for _ in range(4):  # góc đầu sao cho tia trúng đích (chỗ miệng phụ thuộc góc đầu nên lặp)
            r = math.radians(psi_f)
            m = Hf + sz * np.array([math.cos(r) * jt["x"] - math.sin(r) * jt["y"], math.sin(r) * jt["x"] + math.cos(r) * jt["y"]])
            psi_f = math.degrees(math.atan2(TGT[1] - m[1], TGT[0] - m[0])) - JROT
        da = psi_f - h["psi"]
        ux, uy = math.cos(math.radians(psi_f)), math.sin(math.radians(psi_f))
        if hid == "k":  # chỗ bắn tia của thủ lĩnh lúc phun (game.muzzle, hệ rig): xương mieng_k ở khung F
            info["muzzle"] = (float(m[0]), float(m[1]))
            info["cast_fire"] = F
        keys = [(0, z, "lin"), (0.45, (gx * 0.7, gy * 0.7, ga * 0.7, -3), "io"), (0.80, (gx, gy, ga, -6), "io"), (F - 0.07, (gx - 12, gy - 6, ga - 2, -6), "lin"),
                (F, (fx_ + 26 * ux, fy_ + 26 * uy, da, 52), "in"), (F + 0.10, (fx_ - 34 * ux, fy_ - 34 * uy, da + 3, 50), "out"), (F + 0.30, (fx_, fy_, da, 50), "io")]
        for i, t in enumerate(np.arange(F + 0.30 + 2.0 / FPS, E - 0.02, 2.0 / FPS)):
            sg = 1 if i % 2 == 0 else -1
            keys.append((float(t), (fx_ - 5 * uy * sg, fy_ + 5 * ux * sg, da + 1.2 * sg, 50 + 3 * sg), "lin"))
        keys += [(E, (fx_, fy_, da, 46), "lin"), (E + 0.22, (fx_ - 24, fy_ - 26, da - 7, 4), "io"), (D - 0.12, z, "io"), (D, z, "lin")]
        tr[hid] = Track(keys)
        c.raw("h" + hid, "scale", [(0, (1, 1)), (F - 0.07, (1, 1)), (F, (1.13, 0.93)), (F + 0.10, (0.97, 1.03)), (F + 0.3, (1, 1)), (D, (1, 1))])
        c.events.append((F, "phun", hid))
        c.fx.append((F - 0.02, info["heads"][hid]["E"][0] + 40, WY, 0.7, "toe_nho"))
    c.events.append((E, "het_phun", ""))
    c.fx += [(F0 - 0.02, 0, WY - 30, 1.4, "vong"), (F0 + 0.03, 120, WY, 0.9, "toe_nho"), (F0 + 0.4, 300, WY - 4, 0.7, "toe_nho"), (F0 + 0.8, 180, WY - 4, 0.6, "toe_nho"),
             (E + 0.2, 0, WY - 30, 1.0, "vong")]
    animate_heads(c, tr, sway=lambda t: 1 - ease(t / 0.35, "io") * (1 - ease((t - 2.65) / 0.5, "io")))
    animate_water(c, grow=lambda t: 1 + 0.09 * ease((t - 0.2) / 0.6, "io") * (1 - ease((t - F0) / 0.12, "out")) + 0.06 * ease((t - F0) / 0.1, "out") * (1 - ease((t - E) / 0.5, "io")),
                  calm=lambda t: 1 - 0.4 * ease(t / 0.8, "io") * (1 - ease((t - F0) / 0.2, "io")))
    animate_fx(c)
    return c


def clip_trung_don(info):
    """bị đánh từ bên phải: cả năm đầu giật bật về trái trong hai khung, miệng há, rồi hồi về lệch nhau có nẩy quá đà; nước toé."""
    D = 0.8
    c = Clip("hit", D, info)
    z = (0, 0, 0, 0)
    amt = {"a": (-70, 26, 16, 0.00), "b": (-60, 20, 14, 0.03), "k": (-110, 30, 18, 0.0), "c": (-150, 46, 24, 0.02), "d": (-170, 50, 28, 0.04)}
    tr = {}
    for hid, (dx, dy, da, dl) in amt.items():
        tr[hid] = K((0, z, "lin"), (0.07, (dx, dy, da, 28), "out"), (0.16 + dl, (dx * 0.9, dy * 0.8, da * 0.9, 24), "lin"), (0.48 + dl * 2, (16, -8, -4, 0), "io"),
                    (0.66 + dl, (-4, 2, 1, 0), "io"), (D, z, "io"))
    c.fx += [(0.03, 150, WY, 0.9, "toe"), (0.10, -40, WY, 0.6, "toe_nho")]
    lids(c, {hid: [(0.03, 0.30 + dl * 3)] for hid, (_, _, _, dl) in amt.items()})
    animate_heads(c, tr, sway=lambda t: ease((t - 0.3) / 0.5, "io"))
    animate_water(c)
    animate_fx(c)
    return c


def clip_chet(info):
    """trúng đòn chí mạng: cả năm đầu giật bật, nhắm nghiền mắt; rồi từng đầu lả đi (đầu thấp trước, thủ lĩnh sau cùng): ngửa ra sau,
    mõm chổng lên trời, hàm trễ xuống, lưỡi thè ra rũ lủng lẳng, lắc lư yếu ớt nửa giây; cổ hết lực, đầu đổ ngửa ra sau đập xuống
    nước (toé nước đúng chỗ rơi), nổi lộn ngược một nhịp (cằm chổng lên, lưỡi vắt ra) rồi chìm; sóng lặng dần, vũng nước tan."""
    D = 2.5 * TW
    c = Clip("die", D, info)
    z = (0, 0, 0, 0)
    t1 = {"d": 0.30, "c": 0.42, "b": 0.54, "a": 0.66, "k": 0.85}   # lúc lả đi, ngửa ra, lè lưỡi
    land = {"a": -500, "b": -600, "k": -310, "c": -120, "d": 60}    # chỗ đầu đổ xuống (x)
    tr, tongue = {}, {}
    for h in HEADS:
        hid = h["id"]
        Hx, Hy = h["H"]
        ta, big = t1[hid], hid == "k"
        tf = ta + (0.80 if big else 0.62)   # hết lực, bắt đầu đổ
        tl = tf + (0.42 if big else 0.34)   # chạm nước
        back = (-90, 70, 70, 42) if big else (-70, 50, 62, 40)   # ngửa: lùi, nhô lên, mõm chổng lên
        wob1 = (back[0] - 22, back[1] - 14, back[2] + 9, 46)
        wob2 = (back[0] + 8, back[1] - 34, back[2] + 2, 38)
        af = 152 - h["psi"]                 # nằm ngửa trên nước: đầu lộn ngược, mõm chĩa sang trái
        lx = land[hid]
        hitp = (lx - Hx, WY + 62 - Hy, af, 30)
        flo = (lx - 16 - Hx, WY + 50 - Hy, af + 6, 36)
        sunk = (lx - 44 - Hx, WY - 420 - Hy, af + 22, 20)
        tr[hid] = K((0, z, "lin"), (0.07, (-46, 22, 14, 26), "out"), (0.18, (-36, 14, 9, 16), "lin"), (ta, (-30, 6, 6, 10), "io"),
                    (ta + 0.16, back, "out"), (ta + 0.38, wob1, "io"), (tf, wob2, "io"),
                    (tl, hitp, "in"), (tl + 0.09, (hitp[0], hitp[1] - 18, af + 3, 34), "out"), (tl + 0.28, (hitp[0] - 6, hitp[1] + 6, af + 2, 36), "io"),
                    (tl + 0.55, flo, "io"), (tl + 1.2, sunk, "in"), (D, sunk, "lin"))
        tongue[hid] = ta + 0.06
        c.fx += [(tl, lx - 60, WY, 1.4 if big else 1.0, "toe"), (tl + 0.5, lx - 20, WY - 30, 0.8, "vong")]
        c.events.append((tl, "roi_nuoc", hid))
    c.fx += [(0.03, 120, WY, 0.9, "toe_nho"), (3.1, 0, WY - 30, 1.2, "vong")]
    lids(c, {h["id"]: [(0.04, D)] for h in HEADS})
    c.raw("than", "translate", [(0, (0, 0)), (3.25, (0, 0)), (3.65, (0, -500))])
    animate_heads(c, tr, sway=lambda t: 1 - ease(t / 0.12, "io"), tongue=tongue)
    animate_water(c, grow=lambda t: (1 - 0.3 * ease((t - 2.7) / 0.7, "io")) * (1 - ease((t - 3.5) / 0.46, "in")),
                  calm=lambda t: 1 - 0.85 * ease((t - 2.5) / 1.0, "io"),
                  sink=lambda t: 330 * ease((t - 2.2) / 1.0, "io"))
    animate_fx(c)
    return c


CLIPS = [clip_idle, clip_xuat_hien, clip_tan_cong, clip_chieu_phun, clip_chieu, clip_trung_don, clip_chet, clip_aura]  # idle nướng trước: dáng râu khung 0


# ---------------------------------------------------------------- 6. xuất
def pack(pc, padding=3):
    items = sorted(pc.items(), key=lambda kv: (-kv[1].height, -kv[1].width))
    area = sum((im.width + padding) * (im.height + padding) for _, im in items)
    widest = max(im.width for _, im in items) + 2 * padding
    W = max(widest, int(math.sqrt(area * 1.12)))
    W = (W + 7) // 8 * 8
    place, shelves = {}, []
    y = padding
    for name, im in items:
        for sh in shelves:
            if sh[1] + im.width + padding <= W and im.height <= sh[2]:
                place[name] = (sh[1], sh[0])
                sh[1] += im.width + padding
                break
        else:
            shelves.append([y, padding + im.width + padding, im.height])
            place[name] = (padding, y)
            y += im.height + padding
    H = (y + 7) // 8 * 8
    sheet = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for name, (x, yy) in place.items():
        sheet.paste(pc[name], (x, yy))
    return sheet, place


def _root_group(sk, name):
    """xương gốc nhóm (con trực tiếp của root) chứa xương này: 'than', 'nuoc' hoặc chính nó."""
    while True:
        b = sk.bones[sk.bi[name]]
        p = b.get("parent")
        if p is None or p == "root":
            return name
        name = p


def export(sk, clips, pc):
    os.makedirs(RIG, exist_ok=True)
    sheet, place = pack(pc)
    if PALETTE:
        sheet.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG).save(os.path.join(RIG, NAME + ".png"), optimize=True)
    else:
        sheet.save(os.path.join(RIG, NAME + ".png"), optimize=True)
    lines = [NAME + ".png", f"size:{sheet.width},{sheet.height}", "filter:Linear,Linear", "pma:false"]
    for name, (x, y) in place.items():
        lines += [name, f"bounds:{x},{y},{pc[name].width},{pc[name].height}"]
    open(os.path.join(RIG, NAME + ".atlas"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    anims = {}
    r2 = lambda v: round(float(v), 2)
    for c in clips:
        A = {"bones": {}, "slots": {}}
        for b, tl in c.bones.items():
            o = {}
            for kind, keys in tl.items():
                if kind == "rotate":
                    ks = [{"time": round(t, 4), "value": r2(np.atleast_1d(v)[0])} for t, v in keys]
                    if all(abs(k["value"]) < 0.02 for k in ks):
                        continue
                elif kind == "translate":
                    ks = [{"time": round(t, 4), "x": r2(v[0]), "y": r2(v[1])} for t, v in keys]
                    if all(abs(k["x"]) < 0.02 and abs(k["y"]) < 0.02 for k in ks):
                        continue
                else:
                    ks = [{"time": round(t, 4), "x": round(float(v[0]), 3), "y": round(float(v[1]), 3)} for t, v in keys]
                    if all(abs(k["x"] - 1) < 0.002 and abs(k["y"] - 1) < 0.002 for k in ks):
                        continue
                for k in ks:
                    if k["time"] == 0:
                        del k["time"]
                o[kind] = ks
            if o:
                A["bones"][b] = o
        for s, tl in c.slots.items():
            ks = [{"time": round(t, 4), "value": round(v, 3)} for t, v in tl["alpha"]]
            for k in ks:
                if k["time"] == 0:
                    del k["time"]
            A["slots"][s] = {"alpha": ks}
        if c.events:
            A["events"] = [{"time": round(t, 4), "name": n, "string": st} for t, n, st in sorted(c.events)]
        anims[c.name] = A
    data = {"skeleton": {"spine": "4.2.28", "x": -760, "y": -20, "width": 1500, "height": 1150, "images": "", "audio": ""},
            "bones": sk.bones, "slots": sk.slots, "events": {n: {} for n in EVENTS}, "skins": [{"name": "default", "attachments": sk.atts}], "animations": anims}
    p = os.path.join(RIG, NAME + ".json")
    open(p, "w", encoding="utf-8").write(json.dumps(data, separators=(",", ":")))
    per_clip = {}
    for cn, a in anims.items():
        per_clip[cn] = sum(len(ks) for k_, part in a.items() if k_ != "events" for tl in part.values() for ks in (tl.values() if isinstance(tl, dict) else [tl]))
    nk = sum(per_clip.values())
    nv = sum(len(a.get("uvs", [])) // 2 for s in sk.atts.values() for a in s.values())
    nt = sum(len(a.get("triangles", [])) // 3 for s in sk.atts.values() for a in s.values())
    nmesh = sum(1 for s in sk.atts.values() for a in s.values() if a.get("type") == "mesh")
    js, pg = os.path.getsize(p), os.path.getsize(os.path.join(RIG, NAME + ".png"))
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {nmesh} lưới, {nv} đỉnh, {nt} tam giác, {len(anims)} clip, {nk} khoá; atlas {sheet.width}x{sheet.height}")
    print(f"dung lượng: json {js / 1e6:.2f} MB + png {pg / 1e6:.2f} MB = {(js + pg) / 1e6:.2f} MB")
    for c in clips:
        print(f"   {c.name}: {c.dur:.2f} s, {per_clip[c.name]} khoá")
    stat = {"bones": len(sk.bones), "slots": len(sk.slots), "meshes": nmesh, "verts": nv, "tris": nt, "clips": len(anims), "keys": nk,
            "keys_per_clip": per_clip, "json": js, "png": pg, "atlas": [sheet.width, sheet.height],
            "durs": {c.name: c.dur for c in clips},
            "bones_body": sum(1 for b in sk.bones if _root_group(sk, b["name"]) == "than"),
            "bones_water": sum(1 for b in sk.bones if _root_group(sk, b["name"]) == "nuoc")}
    json.dump(stat, open(os.path.join(RIG, "stat.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return (f"{len(sk.bones)} xương · {len(sk.slots)} slot · {nv} đỉnh / {nt} tam giác · {len(anims)} clip · {nk} khoá · "
            f"json {js / 1e6:.2f} MB + atlas {pg / 1e6:.2f} MB = {(js + pg) / 1e6:.2f} MB")


EVENTS = {"troi": "đầu trồi khỏi mặt nước", "can": "khung cắn trúng", "gam": "bắt đầu gầm", "het_gam": "hết gầm", "phun": "đầu này bắt đầu phun (VFX tia nước bám xương mieng_<đầu>)",
          "het_phun": "hết phun", "roi_nuoc": "đầu đập xuống nước"}
LABELS = {"appear": "1 Xuất hiện", "idle": "2 Đứng", "attack": "3 Tấn công", "cast": "4 Chiêu phun nước", "skill": "5 Chiêu gầm",
          "hit": "6 Trúng đòn", "die": "7 Chết", "aura": "nước (aura, track 1)"}


def viewer(clips, stat):
    """trang xem tự đủ rig/xem.html: nhúng JSON, atlas, ảnh vào một file, mở bằng cách bấm đúp (không cần server).
    Runtime spine-player.js nằm ở rig/lib (chép từ ArtGen/Spine/lib)."""
    import base64
    import shutil
    tpl = open(os.path.join(HERE, "xem_spine_mau.html"), encoding="utf-8").read()
    b64 = lambda ext: base64.b64encode(open(os.path.join(RIG, NAME + ext), "rb").read()).decode()
    js = open(os.path.join(RIG, NAME + ".json"), encoding="utf-8").read().replace("</", "<\\/")
    names = [c.name for c in clips if c.name != "aura"]
    rp = {"__TITLE__": "Hải Long Ngũ Đầu", "__NAME__": NAME, "__IDLE__": "idle", "__DIE__": "die", "__INFO__": stat,
          "__CLIPS__": json.dumps([[n, LABELS.get(n, n)] for n in names], ensure_ascii=False),
          "__SEQ__": json.dumps(["appear", "idle", "attack", "idle", "cast", "idle", "skill", "idle", "hit", "idle", "die"]),
          "__VIEWS__": json.dumps({}),
          "__VIEW__": json.dumps([-20, 470, 1900, 1500]), "__ATLAS__": b64(".atlas"), "__PNG__": b64(".png"), "__JSON__": js}
    for k, v in rp.items():
        tpl = tpl.replace(k, v)
    # nước là clip `aura` phát chồng trên track 1, trộn kiểu cộng (như AtomikPose.Overlay: xoay, dời cộng; tỉ lệ, độ đậm theo lệch so với
    # dáng gốc). Trang mẫu dùng chung không biết aura nên chèn sau khi dựng AnimationState.
    hook = "state = new spine.AnimationState(asd);"
    assert hook in tpl, "trang mẫu đổi: không thấy chỗ chèn aura"
    tpl = tpl.replace(hook, hook + "\n  if (sd.findAnimation(\"aura\")) { const ae = state.setAnimation(1, \"aura\", true); "
                                   "ae.mixBlend = (spine.MixBlend && spine.MixBlend.add !== undefined) ? spine.MixBlend.add : 3; }", 1)
    # trộn cộng của Spine cộng dồn vào dáng hiện tại mỗi khung: phải về dáng gốc trước mỗi apply (như AtomikPose.Sample), không thì
    # sóng phình to dần (lỗi đã gặp 2026-11-11)
    hook2 = "  state.apply(skeleton);"
    assert hook2 in tpl, "trang mẫu đổi: không thấy state.apply"
    tpl = tpl.replace(hook2, "  skeleton.setToSetupPose();\n" + hook2, 1)
    os.makedirs(os.path.join(RIG, "lib"), exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "lib", "spine-player.js"), os.path.join(RIG, "lib", "spine-player.js"))
    open(os.path.join(RIG, "xem.html"), "w", encoding="utf-8").write(tpl)
    print("trang xem:", os.path.join(RIG, "xem.html"))


def game_info(info, clips):
    """khối `game` của .atomik (AtomikGame trong Unity): boss đứng tại chỗ (không lao), chỗ bắn tia = xương mieng_k lúc phun. Chiều cao
    dáng đứng đo từ khung đầu idle: đỉnh gạc thủ lĩnh tới đáy nước (xấp xỉ theo dáng gốc: H của thủ lĩnh + nửa ảnh đầu)."""
    hk = info["heads"]["k"]
    hp = info["pieces"]["head_k"]
    top = hk["H"][1] + hp.height * 0.75          # gạc vươn trên gáy
    bottom = -60.0                               # đáy dải gợn sóng (ripple ở y = -44, cao ~ 100 ở tỉ lệ 1,22 → mép dưới ≈ -60 + ...)
    height = top - bottom
    durs = {c.name: c.dur for c in clips}
    mz = info.get("muzzle", (0.0, 0.0))
    return {"fps": FPS, "height": round(height, 2),
            "hitClips": ["attack", "cast", "skill"], "hitTimes": [0.45, round(info.get("cast_fire", 1.0), 3), 1.32],
            "lunge": [], "stay": ["attack", "cast", "skill"], "far": [],
            "muzzle": [round(mz[0], 2), round(mz[1], 2)], "beam": 1.6, "beamStyle": "",
            "move": "root", "shadow": "",
            "impactClips": ["attack", "skill"], "impactStop": [0.08, 0.2], "impactShake": [0.45, 0.95], "impactPush": [0.1, 0.22],
            "impactFlash": ["", "#d8f4ff66"],
            "_durs": {k: round(v, 3) for k, v in durs.items()}}


def to_atomik(game):
    """xuất rig/hai_long.atomik (định dạng của game, bản 3: mặt nạ cắt, sự kiện, slot ẩn mặc định; clip aura) và hai_long_game.json.
    KHÔNG chép vào Assets (đặc tả lô Thủy mục 5: Claude điều phối làm bước vào game)."""
    if HERE not in sys.path:   # chạy bằng -I thì thư mục script không nằm trong sys.path
        sys.path.insert(0, HERE)
    import atomik
    gp = os.path.join(RIG, NAME + "_game.json")
    gm = {k: v for k, v in game.items() if not k.startswith("_")}
    json.dump(game, open(gp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = os.path.join(RIG, NAME + ".atomik")
    atomik.convert(os.path.join(RIG, NAME + ".json"), os.path.join(RIG, NAME + ".atlas"), out, NAME, game=gm)
    print(f"{out}: {os.path.getsize(out) / 1e6:.2f} MB (không chép vào Assets)")


def rig():
    pc = load_pieces()
    sk, info = build_rig(pc)
    clips = [f(info) for f in CLIPS]
    stat = export(sk, clips, pc)
    viewer(clips, stat)
    to_atomik(game_info(info, clips))


def viewer_only():
    """dựng lại rig/xem.html từ JSON và stat.json đã có (không nướng lại)."""
    st = json.load(open(os.path.join(RIG, "stat.json"), encoding="utf-8"))
    J = json.load(open(os.path.join(RIG, NAME + ".json"), encoding="utf-8"))

    class _C:
        def __init__(self, n):
            self.name = n
    stat = (f"{st['bones']} xương · {st['slots']} slot · {st['verts']} đỉnh / {st['tris']} tam giác · {st['clips']} clip · {st['keys']} khoá · "
            f"json {st['json'] / 1e6:.2f} MB + atlas {st['png'] / 1e6:.2f} MB = {(st['json'] + st['png']) / 1e6:.2f} MB")
    viewer([_C(n) for n in J["animations"]], stat)


def atomik_only():
    """chỉ xuất lại .atomik + _game.json từ rig/hai_long.json đã có (nướng mỗi clip cast để lấy chỗ bắn tia)."""
    pc = load_pieces()
    sk, info = build_rig(pc)
    clips = [clip_chieu_phun(info)]
    durs = json.load(open(os.path.join(RIG, "stat.json"), encoding="utf-8"))["durs"]
    g = game_info(info, clips)
    g["_durs"] = {k: round(v, 3) for k, v in durs.items()}
    to_atomik(g)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "rig"
    if cmd == "cat":
        cat()
    elif cmd == "atomik":
        atomik_only()
    elif cmd == "xem":
        viewer_only()
    else:
        rig()
