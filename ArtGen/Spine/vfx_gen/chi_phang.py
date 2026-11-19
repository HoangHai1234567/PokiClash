# Đổi khung VFX gen (khung/<tên>/) sang style game: TÔ PHẲNG + VÂN CHÌ, bỏ bóng ánh sáng (người dùng 2026-11-19: "các fx mới gen đẹp
# nhưng texture chưa hợp với style game, kiểu chì vẽ, bỏ bóng ánh sáng đi").
#   py -3 -I ArtGen/Spine/vfx_gen/chi_phang.py            (mọi hiệu ứng)
#   py -3 -I ArtGen/Spine/vfx_gen/chi_phang.py no khoi    (vài hiệu ứng)
# Mỗi khung:
#  1. phân họ màu theo sắc / bão hoà / sáng (lửa, vỏ nham, sáng, còn lại), rồi về MÀU ĐÍCH gần nhất trong họ (Lab, hạ trọng số độ
#     sáng): bảng màu không có màu "sáng" / "tối" nên mảng sáng bầu dục, đáy tối, chuyển màu, quầng đều gộp về màu nền của vùng;
#  2. điểm "sáng" (vệt bóng, chấm sáng): mảng lớn thì giữ làm lõi kem (lửa) / bọt trắng (nước), mảng nhỏ / mảnh lấy màu vùng bao quanh;
#  3. mép vùng làm mượt (lọc gauss trên từng nhãn) + khử răng cưa; lửa bỏ quầng mềm (alpha làm mượt rồi cắt ngưỡng 0,62);
#     khói giữ alpha (tan dần) nhưng làm mượt để hết loang;
#  4. khói / tinh thể / lá: nét chì trong (sẫm hơn màu nền) theo mép khối của bản gen, để còn ra cụm múi, mặt cạnh mà không cần bóng;
#  5. phủ vân chì màu gạch chéo -38 độ (như hạt hat_* và tranh bản đồ), cố định theo khung (không nhấp nháy).
# Ra: khung_chi/<tên>/<tên>_NN.png, xem/chi_<tên>.gif, xem/chi.html (trái: bản gen, phải: bản chì phẳng).
import os, sys, json, glob, math
import numpy as np
import cv2
from PIL import Image, ImageDraw
from scipy import ndimage

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 24


def C(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# bảng lửa "hoa" của game (HatLua.Pal): đỏ tươi, cam, vàng, kem
RED, ORA, YEL, CRE = C('E8452E'), C('FFA43A'), C('FFD94A'), C('FFF6D6')
SMOKE = C('8C7C74')       # khói nâu xám một tông
WATER, FOAM = C('2F95E6'), C('F4FBFF')
# nước nhiều gam lam như bản gen (người dùng 2026-11-19: "thêm các gam màu xanh nữa vào cho giống với bản gốc, để 1 màu không thì hơi
# nhạt nhẽo"): 4 mảng phẳng theo thứ tự lam đậm (đỉnh, lưng) -> lam -> xanh trời -> ngọc lam (chân), không chuyển màu
WATER4 = [C('1D5FD2'), C('2F8FE8'), C('35BFEA'), C('45DFD0')]
SAND4 = [C('F8E6BA'), C('F2C677'), C('E2A75E'), C('BF8850')]
WATER4B = [C('2B78E6'), C('3D9FF2'), C('4FCBF2'), C('5FE6D8')]  # lốc nước: bản sáng hơn WATER4 một nấc   # lốc cát: kem, vàng cát, nâu nhạt, nâu cát (mảng phẳng)
DIRT = C('B39672')
LEAF, WOOD = C('72BE3E'), C('8A6440')
STEEL, ICE = C('A3ABBA'), C('8FC6E2')
CRUST = C('7A3A2A')
FIRE4 = [RED, ORA, YEL, CRE]
FIRE5 = [RED, C('F0702A'), ORA, YEL, CRE]   # thêm đỏ cam của game (vòng, tàn lửa) cho lốc lửa nhiều dải

# fam: họ -> bảng đích. Họ: fire (đỏ cam vàng đậm màu), crust (nâu đỏ sẫm), light (gần trắng), other (còn lại)
# light_keep: màu giữ cho mảng sáng LỚN (None = mọi điểm sáng lấy màu vùng quanh); lines: nét chì trong cho họ nào
FX = {
    'no':        dict(fam={'fire': [RED, ORA, YEL], 'crust': [SMOKE], 'other': [SMOKE]}, light_keep=None, lines=('other', 'crust')),
    'trung_lua': dict(fam={'fire': FIRE4, 'crust': [RED], 'other': [SMOKE]}, light_keep=CRE, lines=(), light_s=0.45, light_v=0.8),
    'lua_lap':   dict(fam={'fire': FIRE4, 'crust': [RED], 'other': [RED]}, light_keep=CRE, lines=(), light_s=0.4),
    'cau_lua':   dict(fam={'fire': FIRE4, 'crust': [RED], 'other': [RED]}, light_keep=CRE, lines=(), light_s=0.4),
    'nham':      dict(fam={'fire': [RED, ORA, YEL], 'crust': [CRUST], 'other': [SMOKE]}, light_keep=YEL, lines=('other',)),
    'khoi':      dict(fam={'fire': [SMOKE], 'crust': [SMOKE], 'other': [SMOKE]}, light_keep=None, lines=('other', 'crust', 'fire'),
                      edge_src='khoi_nong'),
    'nuoc_toe':  dict(fam={'other': WATER4}, light_keep=FOAM, lines=(), lw=1.0, smooth=2.2, light_open=1, light_min=28),
    'song_nuoc': dict(fam={'other': WATER4}, light_keep=FOAM, lines=(), lw=1.0, smooth=2.2, light_open=1, light_min=28),
    'trung_nuoc': dict(fam={'other': WATER4}, light_keep=FOAM, lines=(), lw=1.0, smooth=2.2, light_open=1, light_min=28),
    'cau_nuoc':  dict(fam={'other': WATER4}, light_keep=FOAM, lines=(), lw=1.0, smooth=2.2, light_open=1, light_min=28),
    'loc':       dict(fam={'other': [C('1F7A5A'), C('A6E04A'), C('3CCFC0'), C('8A74C8')]}, light_keep=None, lines=()),
    'gai_la':    dict(fam={'other': [LEAF, WOOD, DIRT], 'fire': [LEAF, WOOD, DIRT], 'crust': [WOOD]}, light_keep=None, lines=('other',)),
    'gai_bang':  dict(fam={'other': [ICE]}, light_keep=C('DCEFF7'), light_low=0.72, lines=('other',), line_k=0.42, canny=(45, 110), min_len=24),
    'gai_sat':   dict(fam={'other': [STEEL]}, light_keep=C('DEDCD6'), light_low=0.72, lines=('other',), line_k=0.42, canny=(45, 110), min_len=24),
    # lốc: người dùng chê bản mảng cũ "màu hơi trầm": giữ độ sáng khi gán màu (lw 1), bảng sáng hơn, vân chì nhạt hơn (tex_k)
    'loc_nuoc':  dict(auto_k=6, fam={'other': WATER4B}, light_keep=FOAM, lines=(), lw=1.0, smooth=1.8, light_open=1, light_min=18,
                      light_s=0.26, light_v=0.8, tex_k=0.65, hard_alpha=True),
    'loc_lua':   dict(auto_k=5, fam={'fire': FIRE5, 'crust': [RED], 'other': [ORA]}, light_keep=CRE, lines=(), light_s=0.4, lw=1.0, tex_k=0.65),
    'loc_cat':   dict(auto_k=5, fam={'other': SAND4, 'fire': SAND4, 'crust': SAND4}, light_keep=C('FFF4D8'), lines=(), lw=1.0, smooth=1.8,
                      light_s=0.22, light_v=0.88, light_open=1, light_min=24, tex_k=0.6, hard_alpha=True),
    'cau_tu':    dict(auto_k=5, fam={'fire': FIRE5}, light_keep=CRE, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'cau_bay':   dict(auto_k=5, fam={'fire': FIRE5}, light_keep=CRE, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'loc_nuoc_bao': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.65, hard_alpha=True),
    'loc_lua_bao':  dict(auto_k=5, fam={'fire': FIRE5}, lines=(), lw=1.0, tex_k=0.65, hard_alpha=True),
    'loc_cat_bao':  dict(auto_k=5, fam={'other': SAND4}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_moc_doan':   dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_moc_nong':   dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_moc_trung':  dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_nuoc_doan':  dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_nuoc_trung': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_lua_doan': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_lua_nong': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_lua_trung': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_vang_doan': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_vang_nong': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'tia_vang_trung': dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'long_la':     dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'quat_dat':    dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.6, hard_alpha=True),
    'chem_kg':     dict(auto_k=6, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.5, hard_alpha=True),
    'trung_trang': dict(auto_k=3, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.35, hard_alpha=True),
    'set_danh':    dict(auto_k=5, fam={'other': WATER4B}, lines=(), lw=1.0, tex_k=0.45, hard_alpha=True),
}
FAMS = ['fire', 'crust', 'other']


def to_lab(rgb):
    return cv2.cvtColor(rgb.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)


def hatch_tex(h, w, seed=5, ss=3):
    """vân chì màu: nét gạch chéo -38 độ dày ~2 px, cách ~5 px, đậm nhạt khác nhau, hơi rung; thêm vài nét sáng và hạt giấy.
    Trả hệ số nhân 0..~1.05 cỡ (h, w)."""
    rng = np.random.RandomState(seed)
    H, W = h * ss, w * ss
    im = Image.new('L', (W, H), 255)
    d = ImageDraw.Draw(im)
    a = math.radians(-38)
    ca, sa = math.cos(a), math.sin(a)
    span = int(math.hypot(W, H)) + 40
    step = 5.2 * ss
    k = -span
    while k < span:
        off0 = k + rng.uniform(-0.3, 0.3) * step
        # nét đứt thành đoạn dài ngắn như chì tô tay
        t = -span
        while t < span:
            ln = rng.uniform(40, 160) * ss
            pts = []
            for j in range(7):
                tt = t + ln * j / 6
                off = off0 + rng.uniform(-0.5, 0.5) * ss
                pts.append((W / 2 + off * -sa + tt * ca, H / 2 + off * ca + tt * sa))
            dark = rng.uniform(0.70, 0.88)
            d.line(pts, fill=int(255 * dark), width=int(round(rng.uniform(1.5, 2.6) * ss)), joint='curve')
            t += ln + rng.uniform(2, 14) * ss
        k += step * rng.uniform(0.85, 1.15)
    v = np.asarray(im.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
    grain = ndimage.gaussian_filter(rng.normal(0, 1, (h, w)), 0.7)
    v = v + 0.025 * grain
    return np.clip(v, 0.5, 1.05)


def hsv(rgb):
    x = rgb.astype(np.float32) / 255
    mx, mn = x.max(-1), x.min(-1)
    S = np.where(mx > 1e-4, (mx - mn) / np.maximum(mx, 1e-4), 0)
    hsv_ = cv2.cvtColor(rgb.astype(np.uint8).reshape(-1, 1, 3), cv2.COLOR_RGB2HSV_FULL).reshape(rgb.shape)
    Hd = hsv_[..., 0].astype(np.float32) * 360 / 255
    return Hd, S, mx


def flatten(arr, cfg, tex, edge_rgb=None):
    h, w = arr.shape[:2]
    a = arr[..., 3].astype(np.float32) / 255
    rgb = arr[..., :3]
    vis = a > 0.04
    Hd, S, V = hsv(rgb)
    warm = (Hd <= 62) | (Hd >= 335)
    light = (S < cfg.get('light_s', 0.2)) & (V > cfg.get('light_v', 0.86))
    if cfg.get('no_light'): light = np.zeros_like(light)   # bảng tự lấy đã có màu sáng (bọt, kem) như bản gốc: giữ nguyên
    fam = np.full((h, w), 2, np.int32)                       # other
    fam[warm & (S > 0.42) & (V > 0.55)] = 0                    # fire
    fam[warm & (S > 0.28) & (V <= 0.55)] = 1                   # crust
    famcfg = cfg['fam']
    # bảng nhãn chung: mọi màu đích của mọi họ (+ màu giữ cho mảng sáng)
    tg, tfam = [], []
    for fi, f in enumerate(FAMS):
        for c in famcfg.get(f, famcfg.get('other')):
            tg.append(c); tfam.append(fi)
    keep = cfg['light_keep']
    if keep is not None:
        tg.append(keep); tfam.append(-1)
    tg = np.array(tg, np.float32); tfam = np.array(tfam)
    lab = to_lab(rgb).reshape(h, w, 3)
    tlab = to_lab(tg)
    wgt = np.array([cfg.get('lw', 0.35), 1.0, 1.0], np.float32)
    dist = (((lab[:, :, None, :] - tlab[None, None]) * wgt) ** 2).sum(-1)
    # chỉ cho chọn màu đích cùng họ
    allow = tfam[None, None, :] == fam[..., None]
    dist = np.where(allow, dist, 1e12)
    lbl = dist.argmin(-1)
    # điểm sáng: mảng lớn, dày -> màu giữ; còn lại -> lấy nhãn gần nhất không sáng
    li = light & vis
    if keep is not None:
        big = ndimage.binary_opening(li, iterations=cfg.get('light_open', 2))
        cc, n = ndimage.label(big)
        if n:
            sz = ndimage.sum(np.ones_like(cc), cc, index=np.arange(1, n + 1))
            big = np.isin(cc, 1 + np.nonzero(sz >= cfg.get('light_min', 120))[0])
        big = ndimage.binary_dilation(big, iterations=2) & li
        if cfg.get('light_low'):            # chỉ giữ bụi sáng ở phần dưới khung (vệt bóng trên thân tinh thể lấy màu thân)
            big[:int(cfg['light_low'] * h)] = False
        lbl[big] = len(tg) - 1
        fill = li & ~big
    else:
        fill = li
    src = vis & ~fill
    if fill.any() and src.any():
        _, (iy, ix) = ndimage.distance_transform_edt(~src, return_indices=True)
        lbl[fill] = lbl[iy[fill], ix[fill]]
    K = len(tg)
    # mép mượt: gauss trên từng nhãn rồi lấy lớn nhất; khử răng cưa bằng trộn nhẹ quanh mép
    oh = np.stack([((lbl == k) & vis).astype(np.float32) for k in range(K)], -1)
    sm = np.stack([ndimage.gaussian_filter(oh[..., k], cfg.get('smooth', 1.3)) for k in range(K)], -1)
    lbl = sm.argmax(-1)
    oh = np.stack([(lbl == k).astype(np.float32) for k in range(K)], -1)
    aa = np.stack([ndimage.gaussian_filter(oh[..., k], 0.6) for k in range(K)], -1)
    col = (aa[..., :, None] * tg[None, None]).sum(2) / np.maximum(aa.sum(-1, keepdims=True), 1e-4)
    # alpha: lửa bỏ quầng; còn lại làm mượt (hết loang của bản tách nền)
    is_fire = (tfam[lbl] == 0) | (tfam[lbl] == -1) & (keep == CRE)
    if cfg.get('hard_alpha'): is_fire = np.ones_like(is_fire)   # dải mảnh (lốc): mép rõ, không để mờ thành trong suốt
    a_s = ndimage.gaussian_filter(a, 1.2)
    hard = np.clip((a_s - 0.62) / 0.06, 0, 1)
    soft = ndimage.gaussian_filter(a, 2.2)
    soft = np.where(a > 0.04, soft, 0)
    edge_a = np.clip((a_s - 0.3) / 0.12, 0, 1)                # mép rõ cho khối không phải lửa
    alpha = np.where(is_fire, hard, np.minimum(edge_a, np.clip(soft / 0.78, 0, 1)))
    # nét chì trong theo mép khối của bản gen (khói, tinh thể, lá)
    lines_f = [FAMS.index(f) for f in cfg['lines']]
    if lines_f:
        g = cv2.cvtColor((edge_rgb if edge_rgb is not None else rgb).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        g = cv2.GaussianBlur(g, (0, 0), 1.4)
        e = cv2.Canny(g, *cfg.get('canny', (22, 60))) > 0
        region = np.isin(tfam[lbl], lines_f) & (alpha > 0.5)
        region = ndimage.binary_erosion(region, iterations=3)   # không vẽ ở mép ngoài (không viền)
        e &= region
        cc, n = ndimage.label(e, structure=np.ones((3, 3)))
        if n:
            sz = ndimage.sum(np.ones_like(cc), cc, index=np.arange(1, n + 1))
            e = np.isin(cc, 1 + np.nonzero(sz >= cfg.get('min_len', 14))[0])
        line = np.clip(ndimage.gaussian_filter(e.astype(np.float32), 0.75) * 2.2, 0, 1)
        col = col * (1 - cfg.get('line_k', 0.30) * line[..., None])
    tk = cfg.get('tex_k', 1.0)
    col = np.clip(col * (1 - tk * (1 - tex))[..., None], 0, 255)
    alpha[~vis] = 0
    return np.dstack([col, alpha * 255]).astype(np.uint8)


def auto_palette(files, k):
    """bảng màu phẳng lấy từ chính bản gen: k-means (Lab) trên điểm đặc của vài khung -> k màu đại diện (giữ dải tươi của bản gốc)"""
    px = []
    for f in files[::max(1, len(files) // 6)]:
        a = np.asarray(Image.open(f).convert('RGBA'))
        m = a[..., 3] > 200
        px.append(a[m][:, :3])
    px = np.concatenate(px)
    px = px[np.random.default_rng(1).choice(len(px), min(60000, len(px)), replace=False)]
    lab = to_lab(px)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.5)
    _, lb, cen = cv2.kmeans(lab.astype(np.float32), k, None, crit, 6, cv2.KMEANS_PP_CENTERS)
    rgb = cv2.cvtColor(cen.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_LAB2RGB).reshape(-1, 3)
    return [tuple(int(v) for v in c) for c in rgb]


def process(name):
    cfg = FX[name]
    if cfg.get('auto_k'):
        fs = sorted(glob.glob(os.path.join(HERE, 'khung', name, name + '_*.png')))
        pal = auto_palette(fs, cfg['auto_k'])
        print('  bảng tự lấy:', ['#%02X%02X%02X' % c for c in pal])
        cfg = dict(cfg, fam={'fire': pal, 'crust': pal, 'other': pal}, light_keep=None, smooth=0.9, no_light=True)
    files = sorted(glob.glob(os.path.join(HERE, 'khung', name, name + '_*.png')))
    if not files:
        print('thiếu khung', name); return None
    out_dir = os.path.join(HERE, 'khung_chi', name)
    os.makedirs(out_dir, exist_ok=True)
    first = Image.open(files[0])
    tex = hatch_tex(first.height, first.width)
    outs, srcs = [], []
    for f in files:
        arr = np.asarray(Image.open(f).convert('RGBA'))
        er = None
        if cfg.get('edge_src'):
            ef = os.path.join(HERE, 'khung', cfg['edge_src'], os.path.basename(f).replace(name, cfg['edge_src'], 1))
            if os.path.exists(ef): er = np.asarray(Image.open(ef).convert('RGB'))
        o = flatten(arr, cfg, tex, er)
        im = Image.fromarray(o, 'RGBA')
        im.save(os.path.join(out_dir, os.path.basename(f)), optimize=True)
        outs.append(im); srcs.append(Image.fromarray(arr, 'RGBA'))
    W, H = first.size
    sand = (214, 190, 140)
    frames = []
    for s, o in zip(srcs, outs):
        g = Image.new('RGB', (W * 2 + 12, H), (255, 255, 255))
        for k, im in enumerate((s, o)):
            tile = Image.new('RGB', (W, H), sand)
            tile.paste(im, (0, 0), im)
            g.paste(tile, (k * (W + 12), 0))
        frames.append(g.convert('P', palette=Image.ADAPTIVE, colors=255))
    frames[0].save(os.path.join(HERE, 'xem', 'chi_%s.gif' % name), save_all=True, append_images=frames[1:],
                   duration=int(1000 / FPS), loop=0, disposal=2)
    print(name, 'xong', len(files), 'khung')
    return name


def page():
    ds = json.load(open(os.path.join(HERE, 'khung', 'ds.json'), encoding='utf-8'))
    rows = []
    for e in ds:
        if e['name'] not in FX or not os.path.exists(os.path.join(HERE, 'xem', 'chi_%s.gif' % e['name'])): continue
        rows.append(f"<section><h2>{e['label']} <small>{e['name']}</small></h2><img src=\"chi_{e['name']}.gif\"></section>")
    html = """<!doctype html><html lang="vi"><meta charset="utf-8"><title>VFX chì phẳng</title>
<style>body{margin:0;padding:16px;background:#1e2128;color:#e8e4dc;font:15px system-ui,sans-serif}h1{font-size:20px}
h2{font-size:17px;margin:4px 0}small{color:#9aa0aa;font-weight:400}section{background:#2a2e36;border-radius:8px;padding:10px 14px}
img{max-width:100%}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:12px}</style>
<h1>VFX: trái bản gen, phải bản tô phẳng + vân chì (bỏ bóng ánh sáng), 24 khung/giây trên nền cát</h1><div class="grid">""" + \
        '\n'.join(rows) + '</div></html>'
    open(os.path.join(HERE, 'xem', 'chi.html'), 'w', encoding='utf-8').write(html)


def main():
    names = sys.argv[1:] or list(FX)
    for n in names: process(n)
    page()


if __name__ == '__main__':
    main()
