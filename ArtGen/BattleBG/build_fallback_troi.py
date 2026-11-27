# Nối trời cho nền trận thay thế (người dùng 2026-11-27: "có 1 số đảo phần ảnh trong màn combat chưa gen lại cho full lên trên nên
# bị trống"). Đảo Thổ, Kim chưa có bộ sàn đấu nên mọi trận dùng ảnh thay thế Assets/03 Art/Fallback/battle_<hệ>.png (code vẽ của
# bản web, Web/scripts/export_fallback.mjs, 1080 x 928); trận không theo ải (thử thách huy hiệu, hang) của mọi đảo cũng dùng. Máy dài
# hơn 9:16 thì phần trên vùng sân chỉ còn màu trời trơn, thấy rõ mép ảnh.
# Ảnh này là hình vẽ bằng code (trời chuyển màu, vệt màu nước trắng mờ, mây, mặt trời nét rough.js) nên nối bằng code, không cho GPT
# vẽ (GPT vẽ lại kiểu chì màu, lệch kiểu với phần dưới). Ra 1080 x 1528 như bản cao của các bộ sàn đấu (600 trời thêm + khung 928;
# StageView.FitBg neo đáy ảnh vào đáy khung), 928 dòng dưới giữ nguyên từng điểm ảnh:
# - trời: dải chuyển màu của web (sky[0] ở y 0, sky[1] ở 75 % khung) kéo dài lên trên theo đúng độ dốc (EXTRAP);
# - vệt màu nước: vệt cũ bị mép trên cắt thì soi gương qua mép rồi nhạt dần trong MIRROR dòng (liền mép, không gãy độ sáng), cộng
#   vệt mới cùng kiểu web (trắng 0,35 ở tâm, tắt ở bán kính) nằm hẳn trong phần thêm;
# - mây: chép 2 đám mây của chính ảnh (lật, đổi cỡ) lên phần thêm; mặt trời giữ chỗ cũ.
# Ảnh gốc 928 cất ở ArtGen/BattleBG/fallback_goc/ (lần đầu chạy); chạy lại thì đọc bản gốc. Xuất lại ảnh thay thế từ web
# (export_fallback.mjs) thì chạy lại script này. Ảnh soi: fallback_goc/soi_<hệ>.png (vạch chỗ máy 9:16, 2960 x 1440, 20:9, 21:9).
# Chạy: py -3 -I ArtGen/BattleBG/build_fallback_troi.py [hệ ...]
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/BattleBG
ROOT = HERE.parent.parent
FALLBACK = ROOT / "Assets" / "03 Art" / "Fallback"
GOC = HERE / "fallback_goc"

W, H = 1080, 928
EXTRA = 600
FULL = H + EXTRA
GRAD_END = 0.75 * H  # web: addColorStop(0.75, sky[1]) trên khung 464 x2
EXTRAP = 0.6  # độ dốc chuyển màu kéo lên (1 = đúng độ dốc web; nhỏ hơn cho đỉnh khỏi gắt)
MIRROR = 240  # vệt cũ soi gương qua mép trên rồi tắt trong ngần này dòng (bán kính vệt web tối đa 220)
SKY_ROWS = 520  # dải trời của ảnh cũ (đỉnh đồi thấp nhất ~ y 416)
SHOWS = [(0, "9:16"), (300, "2960x1440"), (480, "20:9"), (600, "21:9")]

# màu trời web (Web/src/core/data/stages.ts), vị trí mây web (x2) để nhận đám mây; mây chép: (mây nguồn, lật, cỡ, tâm x, tâm y theo
# bản cuối 1528)
SKY = {"thuy": ("#bfe6f5", "#f4f1dc"), "hoa": ("#f7c9a8", "#fbe9d0"), "kim": ("#d6dee8", "#f1efe6"),
       "moc": ("#cfeec0", "#f4f1dc"), "tho": ("#f6dfae", "#fbf0d8")}
CLOUDS = {"lon": (600, 140), "trai": (120, 240), "phai": (840, 300)}
COPIES = [("lon", True, 0.85, 300, 300), ("phai", False, 1.1, 820, 440)]
SEED = {"thuy": 11, "hoa": 12, "kim": 13, "moc": 14, "tho": 15}


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32)


def grad(z, ys):
    """màu trời web ở các dòng ys (theo khung cũ, âm là phần thêm phía trên)"""
    s0, s1 = (hexrgb(c) for c in SKY[z])
    t = np.clip(ys / GRAD_END, 0, 1)
    t = np.where(ys < 0, ys / GRAD_END * EXTRAP, t)
    return np.clip(s0[None] + (s1 - s0)[None] * t[:, None], 0, 255)  # (n, 3)


def source(z):
    GOC.mkdir(parents=True, exist_ok=True)
    keep = GOC / f"battle_{z}.png"
    cur = FALLBACK / f"battle_{z}.png"
    if not keep.exists():
        with Image.open(cur) as im:
            if im.size != (W, H):
                sys.exit(f"{cur} cỡ {im.size}, chưa có bản gốc {keep}")
        shutil.copy2(cur, keep)
    with Image.open(keep) as im:
        return np.asarray(im.convert("RGB"), dtype=np.float32)


def objects(o, g):
    """mặt nạ vật vẽ nét (mây, mặt trời, đồi) trong dải trời: nét mực tối hơn trời nhiều, lấp kín phần trong nét"""
    lum = o[:SKY_ROWS].mean(axis=2)
    ink = lum < g[:SKY_ROWS].mean(axis=1)[:, None] - 45
    ink = ndimage.binary_dilation(ink, iterations=2)
    filled = ndimage.binary_fill_holes(ink)
    return ndimage.binary_dilation(filled, iterations=1)


def alpha_of(o, g, obj):
    """độ phủ trắng của vệt màu nước: o = g (1 - a) + 255 a; chỗ có vật thì nội suy từ trời quanh đó"""
    room = np.maximum(255 - g[:SKY_ROWS], 1)[:, None, :]
    wch = room / room.sum(axis=2, keepdims=True)
    a = np.clip(((o[:SKY_ROWS] - g[:SKY_ROWS, None, :]) / room * wch).sum(axis=2), 0, 1)
    m = (~obj).astype(np.float32)
    for sig in (6, 16, 40):  # chuẩn hoá tích chập: lấp chỗ vật bằng trời quanh đó
        num = ndimage.gaussian_filter(a * m, sig)
        den = ndimage.gaussian_filter(m, sig)
        fill = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0)
        a = np.where(m > 0, a, fill)
        m = np.maximum(m, (den > 0.05).astype(np.float32))
    return a


def blobs(rng, n):
    """vệt mới kiểu web nằm hẳn trong phần thêm: độ phủ (EXTRA, W)"""
    a = np.zeros((EXTRA, W), dtype=np.float32)
    yy, xx = np.mgrid[0:EXTRA, 0:W].astype(np.float32)
    for _ in range(n):
        r = rng.uniform(60, 220)
        cx = rng.uniform(0, W)
        cy = rng.uniform(-r * 0.5, EXTRA - r)  # đáy vệt không chạm mép cũ
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        ab = np.clip(1 - d / r, 0, 1) * 0.35
        a = a + ab * (1 - a)
    return a


def cloud_patch(o, obj, name):
    """đám mây gần chỗ web vẽ: (ảnh RGBA cắt sát, tâm)"""
    lab, n = ndimage.label(obj)
    cx, cy = CLOUDS[name]
    best = None
    for k in range(1, n + 1):
        ys, xs = np.nonzero(lab == k)
        if ys.min() > 380 or len(ys) < 400 or xs.max() - xs.min() > 400:  # bỏ đồi, nét vụn
            continue
        d = (xs.mean() - cx) ** 2 + (ys.mean() - cy) ** 2
        if best is None or d < best[0]:
            best = (d, k)
    if best is None or best[0] > 80 ** 2:
        sys.exit(f"không tìm thấy đám mây {name}")
    ys, xs = np.nonzero(lab == best[1])
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    mask = ndimage.gaussian_filter((lab[y0:y1, x0:x1] == best[1]).astype(np.float32), 0.7)
    rgba = np.dstack([o[y0:y1, x0:x1], mask * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def extend(z):
    o = source(z)
    ys_old = np.arange(H, dtype=np.float32)
    g_old = grad(z, ys_old)
    obj = objects(o, g_old)
    a_old = alpha_of(o, g_old, obj)
    rng = np.random.default_rng(SEED[z])
    # phần thêm: dòng r (0..EXTRA-1) ứng với y = r - EXTRA của khung cũ
    ys_new = np.arange(EXTRA, dtype=np.float32) - EXTRA
    g_new = grad(z, ys_new)
    d = -ys_new - 1  # khoảng cách tới mép cũ
    fade = np.clip(1 - d / MIRROR, 0, 1)
    fade = fade * fade * (3 - 2 * fade)
    mir = np.zeros((EXTRA, W), dtype=np.float32)
    rows = d < MIRROR
    mir[rows] = a_old[d[rows].astype(int)] * fade[rows, None]
    a_blob = blobs(rng, 19)
    a = mir + a_blob * (1 - mir)
    top = g_new[:, None, :] * (1 - a[..., None]) + 255 * a[..., None]
    top = np.clip(top + rng.uniform(-0.5, 0.5, top.shape), 0, 255)
    out = np.empty((FULL, W, 3), dtype=np.float32)
    out[:EXTRA] = top
    out[EXTRA:] = o
    res = Image.fromarray(np.round(out).astype(np.uint8), "RGB")
    for name, flip, s, cx, cy in COPIES:
        p = cloud_patch(o, obj, name)
        if flip:
            p = p.transpose(Image.FLIP_LEFT_RIGHT)
        p = p.resize((round(p.width * s), round(p.height * s)), Image.LANCZOS)
        res.paste(p, (round(cx - p.width / 2), round(cy - p.height / 2)), p)
    # giữ nguyên từng điểm ảnh khung cũ
    res.paste(Image.fromarray(o.astype(np.uint8), "RGB"), (0, EXTRA))
    return res


def soi(im):
    marked = im.copy()
    d = ImageDraw.Draw(marked)
    for extra, label in SHOWS:
        y = EXTRA - extra
        d.line([(0, y), (W, y)], fill=(255, 0, 255), width=4)
        d.rectangle((8, y + 6, 8 + 9 * len(label) + 12, y + 30), fill=(255, 0, 255))
        d.text((14, y + 10), label, fill="white")
    out = Image.new("RGB", (W * 2 + 20, FULL), "white")
    out.paste(im, (0, 0))
    out.paste(marked, (W + 20, 0))
    return out


if __name__ == "__main__":
    zones = sys.argv[1:] or list(SKY)
    for z in zones:
        im = extend(z)
        im.save(FALLBACK / f"battle_{z}.png", optimize=True)
        soi(im).save(GOC / f"soi_{z}.png")
        print(f"  {z}: {FALLBACK / f'battle_{z}.png'} ({im.width} x {im.height}), soi {GOC / f'soi_{z}.png'}")
