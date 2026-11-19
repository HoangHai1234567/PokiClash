# M0 đảo Thổ kiểu vùng đất (chép từ land_hoa/m0, 2026-11-19) (GD_Claude/18): từ ảnh nền tạm (concept đã xoá thú, cờ) và đường dò (do_duong.py):
#   --xuat : ghi Assets/03 Art/Islands/land_tho.png (phóng 2 lần), land_tho_dist.png (khoảng cách tới bờ cho shader sóng),
#            khối "land" của đảo Thổ trong zones.json (thay khối cũ nếu có)
#   (luôn) : vẽ bo_cuc_m0.png: đường, vùng che quanh bệ, chấm ải đúng cỡ và chỗ thật (cùng cách tính với ZoneScene), khung một màn
# Cách đặt chấm phải khớp ZoneScene.LandLayout (C#): đổi một bên thì đổi bên kia.
import sys, os, json, re, math
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from diem_tho import HABS, RING
try:
    from diem_tho import RING_OF  # bán trục riêng từng bệ (bệ theo môi trường vùng, mỗi bệ một cỡ)
except ImportError:
    RING_OF = {}
try:
    from diem_tho import ROAD_AT  # bệ đứng xa đường: điểm đường làm mốc chia cờ (ảnh nền)
except ImportError:
    ROAD_AT = {}
from vat_dong import cat_vat, anim_items, FRAME_S, sea_mask
import vung
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(HERE, "..", "nen", "nen_boss_1.png")
ART = os.path.join(ROOT, "Assets", "03 Art", "Islands")
# ảnh khoảng cách để trong Baked/: bộ hậu xử lý ảnh bỏ qua, menu "PokiClash/Đảo vùng đất/Dựng" tự đặt cách nhập (tắt sRGB, không nén)
DIST = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Islands")
ZONES = os.path.join(ROOT, "Assets", "02 Data", "Json", "zones.json")
if "--ra" in sys.argv:  # ghi ra thư mục thử (chép zones.json sang trước), không đụng Assets
    out = sys.argv[sys.argv.index("--ra") + 1]
    os.makedirs(out, exist_ok=True)
    if not os.path.exists(os.path.join(out, "zones.json")):
        import shutil
        shutil.copy(ZONES, os.path.join(out, "zones.json"))
    ART = DIST = out
    ZONES = os.path.join(out, "zones.json")

PIP, PIP_NOW, ZIG = 104, 128, 1.35  # cỡ chấm, chấm đang đánh (người dùng dặn đủ lớn); khoảng cách < ZIG·PIP thì so le hai bên đường
PAD = 0                            # lề quanh vòng đá
HERO_H = {3: 360, 4: 480}          # cao khung tướng trên bệ (px khung 1080), thân chiếm 62% (khớp ZoneScene.LandHeroH)
# đắp thêm biển quanh ảnh nền (px ảnh gốc): habitat sát mép trên (đền rồng) kéo xuống được dưới khung thông tin; hai bên trái phải chừa
# chỗ cho vành mây (IslandAnim frame) khỏi đè vách đảo và bảng tên (góp ý 2026-11-18: mây che phần biển lệch tông)
PAD_T, PAD_B, PAD_L, PAD_R = 120, 60, 90, 90
SCALE = 4800 * 1.1 / 1344          # px khung 1080 mỗi px ảnh gốc; phóng 1,1 lần: đường cong nhẹ (người dùng 2026-11-19 "ít path uốn lượn chữ S"), chặng 9 cờ cần thêm chỗ


def pad_sea(im, top, bot, left=0, right=0):
    """thêm biển bốn phía bằng cách đóng chồng các mảng biển sạch 64 px lấy từ chính ảnh, nối vào mép ảnh chỉ ở chỗ biển"""
    a = np.asarray(im).astype(np.float32)
    H, W, _ = a.shape
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    sea = (B > 195) & (G > 165) & (R < 190) & (B - R > 45)
    P = 64
    frac = ndi.uniform_filter(sea.astype(np.float32), P)
    ys, xs = np.nonzero(frac > 0.995)
    ok = (ys > P // 2) & (ys < H - P // 2) & (xs > P // 2) & (xs < W - P // 2)
    ys, xs = ys[ok], xs[ok]
    rng = np.random.default_rng(7)
    oh, ow = H + top + bot, W + left + right
    acc = np.zeros((oh, ow, 3), np.float32)
    wsum = np.zeros((oh, ow), np.float32)
    g = np.exp(-((np.arange(P) - P / 2 + 0.5) ** 2) / (2 * 16.0 ** 2))
    win = np.outer(g, g).astype(np.float32)
    inner = np.zeros((oh, ow), bool)  # vùng ảnh gốc trừ dải nối 24 px: không cần đắp
    inner[top + 24:top + H - 24, left + 24:left + W - 24] = True
    for y0 in range(-P // 2, oh, 22):
        for x0 in range(-P // 2, ow, 22):
            cy0, cx0 = min(max(y0 + P // 2, 0), oh - 1), min(max(x0 + P // 2, 0), ow - 1)
            if inner[cy0, cx0]:
                continue
            i = rng.integers(len(ys))
            cy, cx = ys[i], xs[i]
            patch = a[cy - P // 2:cy + P // 2, cx - P // 2:cx + P // 2]
            ya, xa = max(0, y0), max(0, x0)
            yb, xb = min(oh, y0 + P), min(ow, x0 + P)
            if yb <= ya or xb <= xa:
                continue
            pw = win[ya - y0:yb - y0, xa - x0:xb - x0]
            acc[ya:yb, xa:xb] += patch[ya - y0:yb - y0, xa - x0:xb - x0] * pw[..., None]
            wsum[ya:yb, xa:xb] += pw
    fill = acc / np.maximum(wsum, 1e-6)[..., None]
    out = fill.copy()
    out[top:top + H, left:left + W] = a
    # nối: dải 24 px quanh mép ảnh gốc pha dần sang biển đắp, chỉ ở điểm biển (và chỉ khi phía đó có đắp)
    for k in range(24):
        t = 1 - k / 24
        rows = ([(top + k, k)] if top else []) + ([(top + H - 1 - k, H - 1 - k)] if bot else [])
        for row, sr in rows:
            m = sea[sr]
            seg = out[row, left:left + W]
            seg[m] = seg[m] * (1 - t) + fill[row, left:left + W][m] * t
        cols = ([(left + k, k)] if left else []) + ([(left + W - 1 - k, W - 1 - k)] if right else [])
        for col, sc in cols:
            m = sea[:, sc]
            seg = out[top:top + H, col]
            seg[m] = seg[m] * (1 - t) + fill[top:top + H, col][m] * t
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


# mây, hải âu, thuyền cắt ra thành hình rời (game cho chúng chuyển động), chỗ cũ vá bằng biển; rồi đắp biển trên, dưới
base, cuts = cat_vat(Image.open(SRC).convert("RGB"))
src = pad_sea(base, PAD_T, PAD_B, PAD_L, PAD_R)
W0, H0 = src.size
LW = round(W0 * SCALE)              # bề ngang vùng đất, px khung 1080
LH = round(LW * H0 / W0)
duong = json.load(open(os.path.join(HERE, "duong.json")))
path_n = [((x + PAD_L) / W0, (y + PAD_T) / H0) for x, y in duong["path"]]
habs = [{"stage": st, "at": [round((c[0] + PAD_L) / W0, 4), round((c[1] + PAD_T) / H0, 4)], "size": s, "plate": side,
         "ring": [round(RING_OF.get(st, RING[s])[0] / W0, 4), round(RING_OF.get(st, RING[s])[1] / H0, 4)],
         # bệ đứng xa đường (ROAD_AT trong diem_tho.py): mốc chia cờ là điểm đường ghim tay; khớp LandHab.road (C#)
         **({"road": [round((ROAD_AT[st][0] + PAD_L) / W0, 4), round((ROAD_AT[st][1] + PAD_T) / H0, 4)]} if st in ROAD_AT else {})}
        for k, (st, c, s, side) in enumerate(HABS)]


def inside_any(x, y):
    for h in habs:
        rx, ry = h["ring"][0] * LW + PAD + PIP / 2, h["ring"][1] * LH + PAD + PIP / 2
        if ((x - h["at"][0] * LW) / rx) ** 2 + ((y - h["at"][1] * LH) / ry) ** 2 <= 1:
            return True
    return False


def layout():
    """chỗ các chấm ải (px vùng đất, y xuống), theo đúng cách của ZoneScene.LandLayout"""
    P = np.array([(x * LW, y * LH) for x, y in path_n])
    L = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
    t = np.arange(0, L[-1], 2.0)
    Q = np.stack([np.interp(t, L, P[:, 0]), np.interp(t, L, P[:, 1])], 1)
    free = np.ones(len(t), bool)
    along, span = [], []
    for h in habs:
        cx, cy = h["at"][0] * LW, h["at"][1] * LH
        rx, ry = h["ring"][0] * LW + PAD, h["ring"][1] * LH + PAD
        dx, dy = Q[:, 0] - cx, Q[:, 1] - cy
        body = HERO_H[h["size"]] * 0.62
        free &= ~(((dx / rx) ** 2 + (dy / ry) ** 2 <= 1) | ((abs(dx) < 0.4 * rx) & (dy < 0) & (dy > -body - PAD)))
        # mốc chia cờ: điểm đường gần bệ (road) thay tâm bệ; khớp ZoneSceneLand.LandLayout
        ax, ay = (h["road"][0] * LW, h["road"][1] * LH) if "road" in h else (cx, cy)
        near = np.hypot(Q[:, 0] - ax, Q[:, 1] - ay)
        along.append(t[int(np.argmin(near))])
        # đoạn đường ôm vòng đá: điểm mốc của habitat được trượt trong đoạn này; đường xuyên qua tâm bệ (đảo Mộc) thì giữ ở tâm, không
        # trượt (trượt ra trước bệ thì cờ của chặng sau rơi xuống trước bệ, 2026-11-19); khớp ZoneSceneLand.LandLayout
        span.append(t[near <= max(rx, ry) * 1.6] if near.min() > 0.35 * ry else np.array([t[int(np.argmin(near))]]))
    # chia đều (góp ý 2026-11-18): dời điểm mốc từng habitat trong đoạn đường ôm vòng đá cho khoảng cách chấm hai đoạn kề nhau gần
    # bằng nhau (lặp vài lượt); khớp ZoneScene.LandLayout
    stg = [h["stage"] for h in habs]
    def free_len(a, b):
        return float(np.count_nonzero((t >= a) & (t <= b) & free)) * 2.0
    for _ in range(4):
        for k in range(1, len(habs) - 1):
            cand = span[k] if len(span[k]) else np.array([along[k]])
            n0, n1 = stg[k] - stg[k - 1] - 1, stg[k + 1] - stg[k] - 1
            best, bv = along[k], -1
            for c in cand[::4]:
                if c <= along[k - 1] or c >= along[k + 1]:
                    continue
                v = min(free_len(along[k - 1], c) / max(1, n0), free_len(c, along[k + 1]) / max(1, n1))
                if v > bv:
                    bv, best = v, c
            along[k] = best
    pips = []
    for i in range(len(habs) - 1):
        a, b = habs[i]["stage"], habs[i + 1]["stage"]
        n = b - a - 1
        idx = np.nonzero((t >= along[i]) & (t <= along[i + 1]) & free)[0]
        gap = len(idx) * 2.0 / n
        # cờ ải đặt đúng trên đường (người dùng 2026-11-18: "phải đặt các mốc đúng nằm trên path"), bỏ xếp so le hai bên đường
        for j in range(1, n + 1):
            q = idx[min(len(idx) - 1, int((j - 0.5) * gap / 2.0))]
            x, y = Q[q]
            pips.append((a + j, x, y, gap, False))
    return P, pips, Q, t, along


P, pips, LQ, LT, LALONG = layout()

# ---------- tờ bố cục ----------
S = 0.4
bg = src.resize((round(LW * S), round(LH * S)), Image.LANCZOS)
d = ImageDraw.Draw(bg, "RGBA")
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
fb = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
d.line([(x * S, y * S) for x, y in P], fill=(255, 40, 40, 160), width=3)
for h in habs:
    cx, cy = h["at"][0] * LW * S, h["at"][1] * LH * S
    rx, ry = (h["ring"][0] * LW + PAD) * S, (h["ring"][1] * LH + PAD) * S
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(255, 255, 0, 230), width=3)
    body = HERO_H[h["size"]] * 0.62 * S
    d.rectangle([cx - 0.25 * rx, cy - body, cx + 0.25 * rx, cy], outline=(255, 160, 0, 230), width=2)
    d.text((cx, cy + 4), str(h["stage"]), fill=(120, 0, 0), font=fb, anchor="mt", stroke_width=3, stroke_fill=(255, 255, 255))
for st, x, y, gap, zig in pips:
    r = PIP * S / 2
    d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=(255, 224, 138, 235), outline=(60, 40, 20), width=2)
    d.text((x * S, y * S), str(st), fill=(60, 30, 10), font=f, anchor="mm")
# khung một màn (1080 x 1920, trừ khung trên 260 và dưới 330) quanh ải 1
fx, fy = habs[0]["at"][0] * LW, habs[0]["at"][1] * LH
w, hgt = 1080, 1920 - 260 - 330
d.rectangle([(fx - w / 2) * S, (fy - hgt / 2) * S, (fx + w / 2) * S, (fy + hgt / 2) * S], outline=(255, 255, 255, 255), width=3)
d.text(((fx - w / 2) * S + 6, (fy - hgt / 2) * S + 4), "1 man dien thoai", fill=(255, 255, 255), font=f)
bg.save(os.path.join(HERE, "bo_cuc_m0.png"))
# ---------- chia vùng boss (vung.py): tờ xem trước vung_m0.png ----------
vlabel, vland, vmasks = vung.chia(src, LW, LH, LQ, LT, LALONG, habs, sea_mask)
VS = 0.22
vbg = src.resize((round(LW * VS), round(LH * VS)), Image.LANCZOS)
pal = [(230, 60, 60), (240, 150, 40), (230, 220, 60), (90, 200, 80), (50, 190, 190), (60, 120, 230), (140, 80, 220), (220, 80, 200),
       (150, 110, 70), (90, 90, 90)]
lab_rgb = np.zeros(vlabel.shape + (4,), np.uint8)
for k in range(len(habs)):
    lab_rgb[vlabel == k] = pal[k % len(pal)] + (110,)
edge = (vlabel != np.roll(vlabel, 1, 0)) | (vlabel != np.roll(vlabel, 1, 1))
lab_rgb[edge & (vlabel >= 0)] = (20, 20, 20, 255)
part = vbg.convert('RGBA')
part.alpha_composite(Image.fromarray(lab_rgb).resize(vbg.size, Image.NEAREST))
pd = ImageDraw.Draw(part)
for k, h in enumerate(habs):
    pd.text((h['at'][0] * LW * VS, h['at'][1] * LH * VS), f'V{k}', fill=(255, 255, 255), font=fb, anchor='mm', stroke_width=3,
            stroke_fill=(0, 0, 0))
panels = [('chia vùng', part.convert('RGB'))]
for prog in (0, 23, 45):
    pv = vung.darken(vbg, LW, LH, vmasks, vung.open_count(habs, prog))
    panels.append((f'tiến độ {prog} ải: mở {vung.open_count(habs, prog)} vùng', pv))
pw, ph = vbg.size
sheet = Image.new('RGB', (pw * 2 + 10, (ph + 30) * 2), 'white')
sd = ImageDraw.Draw(sheet)
for i, (nm, im) in enumerate(panels):
    x, y = (i % 2) * (pw + 10), (i // 2) * (ph + 30)
    sheet.paste(im, (x, y + 30))
    sd.text((x + 4, y + 4), nm, fill=(0, 0, 0), font=fb)
sheet.save(os.path.join(HERE, 'vung_m0.png'))
gaps = sorted({(round(g), z) for _, _, _, g, z in pips})
print(f"vùng đất {LW} x {LH}, đường dài {round(np.hypot(*np.diff(P, axis=0).T).sum())} px, {len(pips)} chấm; "
      f"khoảng cách chấm theo chặng (px, so le):", gaps)

# ---------- xuất ----------
if "--xuat" in sys.argv:
    up = src.resize((W0 * 2, H0 * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
    up.save(os.path.join(ART, "land_tho.png"))
    # tấm biển lặp quanh đảo (ZoneScene: land.sea): mảng biển sạch của chính ảnh nền (đã phóng, cùng mật độ điểm ảnh) đóng lên khung
    # 512 px quấn vòng (mép trái nối mép phải, trên nối dưới) cho lặp liền; thay biển lặp cũ của màn đảo (góp ý 2026-11-18)
    ua = np.asarray(up).astype(np.float32)
    us = (ua[..., 2] > 195) & (ua[..., 1] > 165) & (ua[..., 0] < 190) & (ua[..., 2] - ua[..., 0] > 45)
    PT, T = 96, 512
    fr = ndi.uniform_filter(us.astype(np.float32), PT)
    ys, xs = np.nonzero(fr > 0.998)
    ok = (ys > PT // 2) & (ys < ua.shape[0] - PT // 2) & (xs > PT // 2) & (xs < ua.shape[1] - PT // 2)
    ys, xs = ys[ok], xs[ok]
    rng = np.random.default_rng(5)
    acc = np.zeros((T, T, 3), np.float32)
    ws = np.zeros((T, T), np.float32)
    g = np.exp(-((np.arange(PT) - PT / 2 + 0.5) ** 2) / (2 * (PT / 4) ** 2))
    win = np.outer(g, g).astype(np.float32)
    for y0 in range(0, T, PT // 3):
        for x0 in range(0, T, PT // 3):
            i = rng.integers(len(ys))
            patch = ua[ys[i] - PT // 2:ys[i] + PT // 2, xs[i] - PT // 2:xs[i] + PT // 2]
            yy = (np.arange(PT) + y0) % T
            xx = (np.arange(PT) + x0) % T
            acc[np.ix_(yy, xx)] += patch * win[..., None]
            ws[np.ix_(yy, xx)] += win
    tile = Image.fromarray(np.clip(acc / np.maximum(ws, 1e-6)[..., None], 0, 255).astype(np.uint8))
    tile.save(os.path.join(ART, "land_tho_bien.png"))
    # khoảng cách tới bờ (cùng cách make_song.py): kênh R = khoảng cách × 4 (px ảnh gốc, trần 64), G = chỗ được vẽ sóng
    a = np.asarray(src).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    seaish = ndi.binary_closing((B > 195) & (G > 165) & (R < 190) & (B - R > 45), iterations=2)
    lab, n = ndi.label(seaish)
    band = np.zeros_like(seaish)
    band[:15] = band[-15:] = True
    band[:, :15] = band[:, -15:] = True
    cnt = ndi.sum(seaish, lab, range(1, n + 1))
    edge = {i for i in set(np.unique(lab[band & seaish])) - {0} if cnt[i - 1] > 2000}
    sea = ndi.binary_opening(np.isin(lab, list(edge)), iterations=1)
    holes = ndi.binary_fill_holes(sea) & ~sea
    hl, hn = ndi.label(holes)
    sizes = ndi.sum(holes, hl, range(1, hn + 1))
    small = np.isin(hl, [i + 1 for i, s in enumerate(sizes) if s < 30000])
    sfd = sea | small
    M = 24
    bm = np.zeros_like(sea)
    bm[:M] = bm[-M:] = True
    bm[:, :M] = bm[:, -M:] = True
    near = ndi.binary_dilation(sfd, iterations=M)
    sfd = sfd | (bm & near & ~ndi.binary_dilation(~sfd & ~bm, iterations=3))
    dist = ndi.distance_transform_edt(np.pad(sfd, 100, constant_values=True))[100:-100, 100:-100]
    draw = (sea | (sfd & bm)) & ~ndi.binary_dilation(small, iterations=2)
    rg = np.zeros((H0, W0, 3), np.uint8)
    rg[..., 0] = np.clip(dist * 4, 0, 255)
    rg[..., 1] = draw * 255
    os.makedirs(DIST, exist_ok=True)
    Image.fromarray(rg).save(os.path.join(DIST, "land_tho_dist.png"))
    # khối land trong zones.json: chèn sau "world" của đảo tho (sửa tại chỗ, không ghi lại cả file)
    # kéo, zoom ra ngoài ảnh tối đa (trái, phải, trên, dưới; tỉ lệ bề ngang ảnh): vẫn trong vành mây (trên, dưới 5 hàng tới 1,46 bề ngang
    # mây; trái, phải 2 hàng tới 0,38), không lộ khối phủ ngoài
    pan = [round(0.35 * FRAME_S, 4)] * 2 + [round(1.4 * FRAME_S, 4)] * 2
    # vùng boss (vung.py): ảnh trường vùng cho shader phác chì (Baked/Islands, menu Dựng cờ ải, vùng boss đặt cách nhập), mây phủ và
    # khung từng vùng, lưới vùng thô; vùng khoá vẽ phác chì dưới mây phủ (người dùng 2026-11-18)
    MW, MH = LW // vung.DS, LH // vung.DS
    Image.fromarray(vung.truong(vlabel, vland)).save(os.path.join(DIST, "land_tho_vung.png"))
    veggs, vgaps = vung.trung(vlabel, vland, LQ, habs, LW, LH, anim_items(cuts, W0, H0, PAD_T, PAD_L), src, sea_mask)
    vclouds = vung.may(vlabel, vland, len(habs), LW, LH, gaps=vgaps, Q=LQ, habs=habs)
    secs = []
    for k, (al, (x0, y0, x1, y1)) in enumerate(vmasks):
        sec = {"box": [round(x0 / MW, 4), round(y0 / MH, 4), round(x1 / MW, 4), round(y1 / MH, 4)], "clouds": vclouds[k]}
        sec.update(veggs[k])
        secs.append(sec)
    print("easter egg:", [(k, "chest" in e, "note" in e, [t["k"] for t in e.get("tease", [])]) for k, e in enumerate(veggs)])
    gw, gh, gd = vung.luoi(vlabel)
    for k in range(len(habs)):  # mặt nạ đen cũ (đã bỏ)
        old = os.path.join(ART, f"land_tho_vung_{k}.png")
        for f_ in (old, old + ".meta"):
            if os.path.exists(f_):
                os.remove(f_)
    print("vùng boss:", [len(c) for c in vclouds], "đám mây; lưới", gw, "x", gh)
    land = {"art": "land_tho", "sea": "land_tho_bien", "cloud": "land_tho_may_2", "size": [LW, LH], "pip": [PIP, PIP_NOW], "pan": pan,
            "path": [[round(x, 4), round(y, 4)] for x, y in path_n], "habs": habs, "secs": secs,
            "grid": {"w": gw, "h": gh, "d": gd}}
    block = json.dumps(land, ensure_ascii=False, separators=(", ", ": "))
    txt = open(ZONES, encoding="utf-8").read()
    i = txt.index('"id": "tho"')
    j = txt.index('"world"', i)
    k2 = txt.index("]", j) + 1  # hết mảng world
    m = re.match(r'\s*,\s*"land":\s*', txt[k2:])
    if m:
        s0 = k2 + m.end()
        depth, p = 0, s0
        while True:
            ch = txt[p]
            depth += ch == '{'
            depth -= ch == '}'
            p += 1
            if depth == 0:
                break
        txt = txt[:s0] + block + txt[p:]
    else:
        txt = txt[:k2] + ',\n   "land": ' + block + txt[k2:]
    json.loads(txt)
    open(ZONES, "w", encoding="utf-8", newline="").write(txt)
    # hình rời của phần động, sprite mưa, khoá land_tho trong island_anim.json (giữ kiểu xuống dòng, thụt lề như build_zone70.py)
    for name, rgba, c, w, kind, par in cuts:
        rgba.save(os.path.join(ART, name + ".png"))
    anim_dir = os.path.join(ART, "Anim")
    os.makedirs(anim_dir, exist_ok=True)
    rain = Image.new("RGBA", (12, 56), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rain)
    rd.rounded_rectangle([3, 2, 8, 53], radius=3, fill=(70, 120, 170, 230))
    rd.rounded_rectangle([4, 4, 7, 51], radius=2, fill=(214, 238, 255, 255))
    rain.save(os.path.join(anim_dir, "anim_rain.png"))
    # đèn đêm: quầng đèn ấm mềm, chùm đèn hải đăng (gốc ở mép trái giữa ảnh, loe dần, nhạt dần)
    g = 128
    yy, xx = np.mgrid[0:g, 0:g]
    r = np.hypot(xx - g / 2 + 0.5, yy - g / 2 + 0.5) / (g / 2)
    a = np.clip(1 - r, 0, 1) ** 1.8
    glow = np.zeros((g, g, 4), np.uint8)
    glow[..., 0], glow[..., 1], glow[..., 2], glow[..., 3] = 255, 226, 150, (a * 235).astype(np.uint8)
    Image.fromarray(glow).save(os.path.join(anim_dir, "anim_glow.png"))
    bw, bh = 256, 128
    yy, xx = np.mgrid[0:bh, 0:bw]
    u = xx / bw
    half = 0.06 + 0.42 * u
    v = np.abs(yy - bh / 2 + 0.5) / (bh / 2)
    a = np.clip(1 - v / np.maximum(half, 1e-3), 0, 1) ** 1.2 * (1 - u) ** 0.9
    beam = np.zeros((bh, bw, 4), np.uint8)
    beam[..., 0], beam[..., 1], beam[..., 2], beam[..., 3] = 255, 240, 185, (a * 200).astype(np.uint8)
    Image.fromarray(beam).save(os.path.join(anim_dir, "anim_beam.png"))
    anim_path = os.path.join(ART, "island_anim.json")
    if os.path.exists(anim_path):
        raw = open(anim_path, "rb").read()
        nl = "\r\n" if b"\r\n" in raw else "\n"
        anim = json.loads(raw.decode("utf-8"))
        anim["land_tho"] = anim_items(cuts, W0, H0, PAD_T, PAD_L)
        open(anim_path, "w", encoding="utf-8", newline=nl).write(json.dumps(anim, ensure_ascii=False, indent=1))
    print("đã ghi land_tho.png", up.size, ", land_tho_dist.png, khối land trong zones.json,", len(cuts), "hình rời, khoá land_tho")
