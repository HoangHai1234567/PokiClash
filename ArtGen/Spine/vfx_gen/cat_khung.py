# Cắt tờ khung VFX gen (GPT 2.6 qua Magnific, 1536 x 1024, lưới 6 x 4 = 24 khung) thành từng khung, xem thử, ước dung lượng.
#   py -3 -I ArtGen/Spine/vfx_gen/cat_khung.py            (mọi hiệu ứng)
#   py -3 -I ArtGen/Spine/vfx_gen/cat_khung.py no khoi    (vài hiệu ứng)
# Nguồn: trong/<tên>.png (đã tách nền bằng Magnific remove_background, RGBA) hoặc tho/<tên>.png nền tối (tách theo độ sáng để giữ quầng
# mềm của lửa). Mọi khung một hiệu ứng cắt cùng một hộp (hộp gộp) để điểm neo (chân / tâm) đứng yên khi chạy.
# Ra: khung/<tên>/<tên>_NN.png, xem/<tên>.gif (trên nền cát và nền tối, 24 khung/giây), xem/index.html, khung/ds.json.
import os, sys, json, glob, colorsys
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
COLS, ROWS = 6, 4
FPS = 24

# tên: (nguồn, nhãn, neo, ghi chú). neo: 'chan' = đáy giữa (đứng trên đất), 'tam' = tâm (bay / trúng)
FX = {
    'no':         ('trong', 'Nổ',                      'chan', 'phồng, chớp sao, nấm, nguội, khói nâu, mảnh khuyết'),
    'nuoc_toe':   ('trong', 'Nước toé',                'chan', 'vương miện nước, sụp thành giọt'),
    'song_nuoc':  ('trong', 'Sóng nước',               'chan', 'sóng dâng, cuộn, đổ, vỡ bọt'),
    'trung_nuoc': ('trong', 'Nước trúng đích',         'tam',  'tia từ trái, toé ngược lại'),
    'cau_nuoc':   ('trong', 'Cầu nước (lặp)',          'tam',  'cầu nước có dải bọt xoay'),
    'lua_lap':    ('toi',   'Lửa cháy (lặp)',          'chan', 'cụm lưỡi lửa liếm lên'),
    'cau_lua':    ('toi',   'Cầu lửa bay (lặp)',       'tam',  'bay sang phải, đuôi lửa sau'),
    'trung_lua':  ('toi',   'Lửa trúng đích',          'tam',  'chớp sao, lưỡi lửa, tàn, khói'),
    'nham':       ('trong', 'Dung nham phun',          'chan', 'nứt, phun dòng dẻo, đổ thành vũng, nguội'),
    'khoi_nong':  ('trong:khoi', 'Khói nóng (sau nổ)', 'chan', 'khói nâu có mảng cam'),
    'khoi':       ('trong:khoi', 'Khói',               'chan', 'bản khói nâu xám (bỏ mảng cam)'),
    'loc':        ('trong', 'Lốc năng lượng (lặp)',    'chan', 'xanh lá ngọc, lõi sáng'),
    'gai_la':     ('trong:gai_la2', 'Gai lá đâm lên',  'chan', 'nứt, phóng lên, giữ, gãy rụng lá'),
    'gai_bang':   ('trong:gai_sat', 'Gai tinh thể (băng)', 'chan', 'bản gốc GPT: lam nhạt'),
    'gai_sat':    ('trong:gai_sat', 'Gai sắt đâm lên', 'chan', 'bản gốc đổi màu xám thép'),
    # lốc xoáy (người dùng 2026-11-19 chê vòi rồng mảng cũ "màu hơi trầm và chưa hợp"): lặp, chân giữa đáy
    'loc_nuoc':   ('trong', 'Lốc nước (lặp)',          'chan', 'vòi rồng nước xoắn, bọt trắng'),
    'loc_lua':    ('trong', 'Lốc lửa (lặp)',           'chan', 'lốc xoáy lửa, lưỡi lửa xoắn'),
    'loc_cat':    ('trong', 'Lốc cát (lặp)',           'chan', 'lốc cát / bụi xoắn'),
    # cầu lửa mới (người dùng 2026-11-19 chê cầu lửa Hỏa Quy "tĩnh"): cầu tụ phập phồng lửa cuộn; cầu bay lửa cuộn đuôi dài
    'cau_tu':     ('trong', 'Cầu lửa đang tụ (lặp)',   'tam',  'lõi phập phồng, lưỡi lửa cuộn quanh'),
    'cau_bay':    ('trong', 'Cầu lửa bay mới (lặp)',   'tam',  'bay sang phải, lửa cuộn, đuôi dài'),
    # lốc TRÙM (người dùng 2026-11-19: "lốc xoáy làm to lên cho che hết tướng địch"; lốc phễu thon ở gốc nên hở chân): cột xoáy dày
    'loc_nuoc_bao': ('trong', 'Lốc nước trùm (lặp)',   'chan', 'cột xoáy dày, gốc gần rộng bằng miệng'),
    'loc_lua_bao':  ('trong', 'Lốc lửa trùm (lặp)',    'chan', 'cột xoáy lửa dày'),
    'loc_cat_bao':  ('trong', 'Lốc cát trùm (lặp)',    'chan', 'cột xoáy cát dày'),
    # tia vẽ sẵn (người dùng 2026-11-19: "các tia năng lượng/nước như này nhìn vẫn chưa đã"): đoạn thân tia (trôi, chồng nhau), đầu nòng, va chạm
    'tia_moc_doan':   ('trong', 'Tia lá: đoạn thân (lặp)',   'tam', 'đoạn năng lượng xanh chảy sang phải, dây leo xoắn, lá phong'),
    'tia_moc_nong':   ('trong', 'Tia lá: đầu nòng (lặp)',    'tam', 'cầu năng lượng xoáy, tia lóe'),
    'tia_moc_trung':  ('trong', 'Tia lá: va chạm (lặp)',     'tam', 'tia tới từ trái, toé ngược, lá bay'),
    'tia_nuoc_doan':  ('trong', 'Tia nước: đoạn thân (lặp)', 'tam', 'đoạn nước chảy sang phải, sợi bọt xoắn'),
    'tia_nuoc_trung': ('trong', 'Tia nước: va chạm (lặp)',   'tam', 'tia tới từ trái, vương miện nước toé ngược'),
    'tia_lua_doan':   ('trong', 'Tia lửa: đoạn thân (lặp)',  'tam', 'đoạn lửa chảy sang phải, sợi lửa xoắn'),
    'tia_lua_nong':   ('trong', 'Tia lửa: đầu nòng (lặp)',   'tam', 'cầu lửa xoáy, tia lóe'),
    'tia_lua_trung':  ('trong', 'Tia lửa: va chạm (lặp)',    'tam', 'tia tới từ trái, lửa toé ngược'),
    'tia_vang_doan':  ('trong', 'Tia vàng: đoạn thân (lặp)', 'tam', 'đoạn năng lượng Mặt Trời, dải xoắn, sao'),
    'tia_vang_nong':  ('trong', 'Tia vàng: đầu nòng (lặp)',  'tam', 'cầu Mặt Trời, tia lóe'),
    'tia_vang_trung': ('trong', 'Tia vàng: va chạm (lặp)',   'tam', 'tia tới từ trái, năng lượng vàng toé ngược'),
    # góp ý từng tướng (2026-11-19): lông lá găm (Linh Điểu), cây quật nện đất (Long Vuốt), vệt chém không gian (Voọc Tướng),
    # bông toé trắng lúc trúng (mọi tướng), sét đánh (chiêu cuối Hải Long)
    'long_la':     ('trong', 'Lông lá găm bay (lặp)',     'tam',  'lông lá nhọn bay sang phải, vệt lá xoáy'),
    'quat_dat':    ('trong', 'Cây quật nện đất',          'chan', 'thân dây leo nện, đất nứt, đá đất văng, lá bung, bụi'),
    'chem_kg':     ('trong', 'Vệt chém không gian',       'tam',  'vệt chém chéo xé không gian, 2 vệt phụ, vỡ mảnh'),
    'trung_trang': ('trong', 'Bông toé trắng lúc trúng',  'tam',  'chớp sao trắng, tia nhọn, giọt trắng văng'),
    'set_danh':    ('trong', 'Sét đánh',                  'chan', 'sét từ trời xuống đất, toé tia điện'),
}


def load(name, src):
    kind, _, file = src.partition(':')
    file = file or name
    if kind == 'toi':
        im = np.asarray(Image.open(os.path.join(HERE, 'tho', file + '.png')).convert('RGB')).astype(np.float32)
        h, w, _ = im.shape
        corners = np.concatenate([im[:24, :24].reshape(-1, 3), im[:24, -24:].reshape(-1, 3),
                                  im[-24:, :24].reshape(-1, 3), im[-24:, -24:].reshape(-1, 3)])
        bg = np.median(corners, axis=0)
        d = np.clip(im - bg, 0, None)
        a = np.max(d / np.maximum(255 - bg, 1), axis=2)
        a = np.clip((a - 0.03) / 0.97, 0, 1)                 # bỏ nhiễu nền
        col = bg + d / np.maximum(a[..., None], 1e-3)
        col = np.clip(col, 0, 255)
        out = np.dstack([col, a * 255]).astype(np.uint8)
        return out
    return decheck(file)


def _fit(xs, ys, hi):
    best = (0, None)
    for s in range(6, 49):
        st = max(1, s // 8)
        for py in range(0, s, st):
            for px in range(0, s, st):
                p = (((xs + px) // s + (ys + py) // s) % 2) == 0
                m = (p == hi).mean()
                sc = max(m, 1 - m)
                if sc > best[0]: best = (sc, (s, px, py, m >= 0.5))
    return best


def fit_checker(raw, bgmask):
    """nền ô cờ giả GPT vẽ: tìm cỡ ô, pha, hai màu từ vùng nền (alpha tách nền = 0). GPT vẽ ô cờ không đều trên cả tờ, nên khớp
    riêng từng ô lưới (6 x 4); ô nào khớp kém (< 0,9) thì không tách ô cờ ở đó (mask = False)."""
    lum = raw.mean(2)
    ys, xs = np.nonzero(bgmask)
    if len(xs) < 1000: return None
    L = lum[ys, xs]
    lo_, hi_ = np.percentile(L, 10), np.percentile(L, 90)
    if hi_ - lo_ < 8: return None   # nền trơn (trắng), không có ô cờ
    thr = (lo_ + hi_) / 2
    H, W = lum.shape
    cw, ch = W // COLS, H // ROWS
    pat = np.zeros((H, W), bool); valid = np.zeros((H, W), bool)
    yy, xx = np.indices((ch, cw))
    rng = np.random.default_rng(0)
    scores, sizes = [], []
    for r in range(ROWS):
        for c in range(COLS):
            sub = bgmask[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw]
            sy, sx = np.nonzero(sub)
            if len(sx) < 600: scores.append(0); continue
            sel = rng.choice(len(sx), min(8000, len(sx)), replace=False)
            sy, sx = sy[sel], sx[sel]
            hi = lum[sy + r * ch, sx + c * cw] > thr
            sc, (s, px, py, same) = _fit(sx, sy, hi)
            scores.append(sc)
            if sc < 0.9: continue
            sizes.append(s)
            p = (((xx + px) // s + (yy + py) // s) % 2) == 0
            pat[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] = p if same else ~p
            valid[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] = True
    if not valid.any(): return None
    hiM = (lum > thr) & bgmask
    loM = (lum <= thr) & bgmask
    c1 = np.median(raw[hiM], axis=0); c2 = np.median(raw[loM], axis=0)
    return (int(np.median(sizes)), pat, valid, c1, c2, float(np.mean([s for s in scores if s > 0])),
            sum(1 for s in scores if s >= 0.9))


def decheck(file):
    """Tách màu thật của mảng trong mờ đã bị GPT trộn với ô cờ giả: c = a*s + (1-a)*k. Trong cửa sổ cạnh nhau, chênh trung bình
    giữa ô sáng và ô tối = (1-a)(k1-k2) -> ra a, rồi s. Alpha cuối = alpha tách nền (Magnific) x a."""
    cache = os.path.join(HERE, 'trong', file + '_sach.png')
    src_t = os.path.join(HERE, 'trong', file + '.png')
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(src_t):
        return np.asarray(Image.open(cache).convert('RGBA')).copy()
    mat = np.asarray(Image.open(src_t).convert('RGBA')).astype(np.float32)
    raw_p = os.path.join(HERE, 'tho', file + '.png')
    raw = np.asarray(Image.open(raw_p).convert('RGB')).astype(np.float32) if os.path.exists(raw_p) else None
    am = mat[..., 3] / 255
    fit = fit_checker(raw, am < 0.02) if raw is not None and raw.shape[:2] == am.shape else None
    if fit is None:
        out = mat.astype(np.uint8)
    else:
        from scipy.ndimage import uniform_filter
        s, pat, valid, c1, c2, sc, nok = fit
        print('  ô cờ ~%dpx, khớp TB %.2f, %d/24 ô tách được, màu %s / %s' % (s, sc, nok, c1.astype(int), c2.astype(int)))
        inside = ((am > 0.5) & valid).astype(np.float32)
        P1 = inside * pat; P2 = inside * (~pat)
        dk = c1 - c2
        t = np.zeros(am.shape, np.float32); have = np.zeros(am.shape, bool)
        for win in (2 * s + 1, 4 * s + 1, 8 * s + 1):
            n1 = uniform_filter(P1, win); n2 = uniform_filter(P2, win)
            ok = (n1 > 0.08) & (n2 > 0.08) & ~have
            if not ok.any(): continue
            D = np.zeros(am.shape, np.float32)
            for ch in range(3):
                m1 = uniform_filter(raw[..., ch] * P1, win) / np.maximum(n1, 1e-6)
                m2 = uniform_filter(raw[..., ch] * P2, win) / np.maximum(n2, 1e-6)
                D += (m1 - m2) * dk[ch]
            tt = np.clip(D / float(dk @ dk), 0, 1)
            t[ok] = tt[ok]; have |= ok
        t = np.where(t < 0.08, 0, t)               # nhiễu nhỏ trong vùng đặc: coi như đặc
        mx, mn = raw.max(2), raw.min(2)
        sat = (mx - mn) / np.maximum(mx, 1)
        t = np.where(sat > 0.45, 0, t)             # lửa, nước đậm màu: luôn đặc (khói mới trong mờ)
        t = np.where(valid, t, 0)
        a = 1 - t
        k = np.where(pat[..., None], c1, c2)
        col = (raw - t[..., None] * k) / np.maximum(a[..., None], 0.06)
        col = np.clip(col, 0, 255)
        # vệt ô cờ còn sót trong vùng trong mờ: làm mượt màu (khói vốn mềm)
        from scipy.ndimage import gaussian_filter
        tm = (t > 0).astype(np.float32)
        den = gaussian_filter(tm, 3)
        sm = np.dstack([gaussian_filter(col[..., ch] * tm, 3) for ch in range(3)]) / np.maximum(den[..., None], 1e-4)
        col = np.where((t > 0)[..., None], sm, raw)
        alpha = am * a
        out = np.dstack([col, alpha * 255]).astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(cache)
    return out.copy()


def recolor(arr, name):
    """khoi: bỏ mảng cam; gai_sat: lam băng -> xám thép"""
    if name not in ('khoi', 'gai_sat'): return arr
    rgb = arr[..., :3].astype(np.float32) / 255
    mx, mn = rgb.max(2), rgb.min(2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    if name == 'khoi':
        # khói nâu xám: giữ sáng tối, hạ bão hoà, mảng cam sáng thành nâu nhạt
        tgt = np.array([0.56, 0.50, 0.47])  # nâu xám
        lum = 0.30 * rgb[..., 0] + 0.55 * rgb[..., 1] + 0.15 * rgb[..., 2]
        lum = np.clip((lum - 0.25) * 0.75 + 0.48, 0, 1)
        out = tgt[None, None, :] * (lum[..., None] / 0.5)
        out = out * 0.85 + rgb * 0.15
    else:
        lum = 0.30 * rgb[..., 0] + 0.55 * rgb[..., 1] + 0.15 * rgb[..., 2]
        steel = np.stack([lum * 0.97, lum * 1.0, lum * 1.05], 2)
        out = steel * 0.82 + rgb * 0.18
    arr = arr.copy()
    arr[..., :3] = (np.clip(out, 0, 1) * 255).astype(np.uint8)
    return arr


M = 64  # lề thêm quanh ô: GPT hay vẽ khung lấn sang ô bên


def cells(arr):
    """Tách theo mảng liền: mỗi mảng về ô chứa trọng tâm của nó (khung lấn ô bên vẫn đủ hình). Mảng dính hai khung (phần
    nằm ngoài ô chính > 15%) thì cắt theo đường lưới. Trả khung có lề M quanh ô."""
    from scipy import ndimage
    h, w = arr.shape[:2]
    cw, ch = w // COLS, h // ROWS
    a = arr[..., 3]
    lab, n = ndimage.label(a > 10, structure=np.ones((3, 3)))
    frames = [np.zeros((ch + 2 * M, cw + 2 * M, 4), np.uint8) for _ in range(COLS * ROWS)]
    objs = ndimage.find_objects(lab)
    ys_all, xs_all = np.indices((h, w))
    split = 0
    for k, sl in enumerate(objs, 1):
        if sl is None: continue
        sub = lab[sl] == k
        yy, xx = np.nonzero(sub)
        yy = yy + sl[0].start; xx = xx + sl[1].start
        wt = a[yy, xx].astype(np.float64) + 1
        cy, cx = np.average(yy, weights=wt), np.average(xx, weights=wt)
        ci = min(COLS - 1, int(cx // cw)); ri = min(ROWS - 1, int(cy // ch))
        cell_of = np.minimum(xx // cw, COLS - 1) + COLS * np.minimum(yy // ch, ROWS - 1)
        own = ci + COLS * ri
        if (cell_of != own).mean() > 0.15 and len(xx) > 400:
            split += 1
            tgt = cell_of                      # mảng dính hai khung: cắt theo lưới
        else:
            tgt = np.full_like(cell_of, own)
        for idx in np.unique(tgt):
            m = tgt == idx
            r, c = divmod(int(idx), COLS)
            fy = yy[m] - r * ch + M; fx = xx[m] - c * cw + M
            ok = (fy >= 0) & (fy < ch + 2 * M) & (fx >= 0) & (fx < cw + 2 * M)
            frames[idx][fy[ok], fx[ok]] = arr[yy[m][ok], xx[m][ok]]
    if split: print('  mảng dính hai khung, cắt theo lưới:', split)
    return frames, cw + 2 * M, ch + 2 * M


def bbox(a, thr=8):
    ys, xs = np.where(a[..., 3] > thr)
    if len(xs) == 0: return None
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def process(name):
    src, label, anchor, note = FX[name]
    arr = recolor(load(name, src), name)
    fr, cw, ch = cells(arr)
    # mép ô có hình chạm (khung lấn ô bên cạnh) thì báo
    bleed = []
    for i, f in enumerate(fr):
        a = f[..., 3]
        edge = max(a[:, :2].max(), a[:, -2:].max(), a[:2, :].max(), a[-2:, :].max())
        if edge > 60: bleed.append(i)
    boxes = [bbox(f) for f in fr]
    bs = [b for b in boxes if b]
    x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs); x1 = max(b[2] for b in bs); y1 = max(b[3] for b in bs)
    pad = 2
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(cw, x1 + pad), min(ch, y1 + pad)
    # giữ đối xứng quanh trục giữa ô với neo chân / tâm, để điểm neo nằm giữa ảnh
    cx = cw / 2
    half = max(cx - x0, x1 - cx)
    x0, x1 = int(max(0, cx - half)), int(min(cw, cx + half))
    if anchor == 'tam':
        cy = ch / 2
        hv = max(cy - y0, y1 - cy)
        y0, y1 = int(max(0, cy - hv)), int(min(ch, cy + hv))
    out_dir = os.path.join(HERE, 'khung', name)
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, '*.png')): os.remove(f)
    imgs = []
    for i, f in enumerate(fr):
        im = Image.fromarray(f[y0:y1, x0:x1], 'RGBA')
        im.save(os.path.join(out_dir, '%s_%02d.png' % (name, i)), optimize=True)
        imgs.append(im)
    W, H = x1 - x0, y1 - y0
    # neo: tỉ lệ trong ảnh (Unity pivot). chân = đáy hình thật (dòng có hình thấp nhất)
    py_ = 0.5 if anchor == 'tam' else max(0.0, (y1 - max(b[3] for b in bs)) / H)
    # GIF xem thử: nền cát (sân đấu) bên trái, nền tối bên phải
    sand, dark = (214, 190, 140), (40, 44, 52)
    sc = 1.0
    gif = []
    for im in imgs:
        g = Image.new('RGB', (W * 2 + 12, H), (255, 255, 255))
        for k, bgc in enumerate((sand, dark)):
            tile = Image.new('RGB', (W, H), bgc)
            tile.paste(im, (0, 0), im)
            g.paste(tile, (k * (W + 12), 0))
        gif.append(g.convert('P', palette=Image.ADAPTIVE, colors=255))
    os.makedirs(os.path.join(HERE, 'xem'), exist_ok=True)
    gif[0].save(os.path.join(HERE, 'xem', name + '.gif'), save_all=True, append_images=gif[1:], duration=int(1000 / FPS),
                loop=0, disposal=2)
    png_kb = sum(os.path.getsize(p) for p in glob.glob(os.path.join(out_dir, '*.png'))) / 1024
    # ước bộ nhớ trong game: hộp chặt từng khung, ASTC 6x6 = 3.56 bit / điểm ảnh
    tight = sum(((b[2] - b[0] + 4) * (b[3] - b[1] + 4)) if b else 0 for b in boxes)
    astc_kb = tight * 3.56 / 8 / 1024
    info = {'name': name, 'label': label, 'anchor': anchor, 'note': note, 'frames': len(fr), 'w': int(W), 'h': int(H),
            'pivot': [0.5, round(float(py_), 3)], 'png_kb': int(png_kb), 'astc_kb': int(astc_kb), 'bleed': [int(b) for b in bleed]}
    print(name, W, 'x', H, 'png %d KB' % png_kb, 'ASTC~%d KB' % astc_kb, 'lấn ô:' if bleed else '', bleed or '')
    return info


def page(infos):
    rows = []
    for e in infos:
        rows.append(f"""<section><h2>{e['label']} <small>{e['name']} · {e['frames']} khung · {e['w']}×{e['h']} · ASTC ~{e['astc_kb']} KB</small></h2>
<p>{e['note']}</p><img src="{e['name']}.gif" alt="{e['label']}"></section>""")
    html = """<!doctype html><html lang="vi"><meta charset="utf-8"><title>VFX gen 24 khung</title>
<style>body{margin:0;padding:16px;background:#1e2128;color:#e8e4dc;font:15px system-ui,sans-serif}
h1{font-size:20px}h2{font-size:17px;margin:18px 0 4px}small{color:#9aa0aa;font-weight:400}p{margin:0 0 6px;color:#c9c3b8}
section{background:#2a2e36;border-radius:8px;padding:10px 14px;margin-bottom:12px}img{max-width:100%;image-rendering:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:12px}</style>
<h1>VFX gen 24 khung (24 khung/giây), trái: nền cát sân đấu, phải: nền tối</h1><div class="grid">""" + '\n'.join(rows) + '</div></html>'
    open(os.path.join(HERE, 'xem', 'index.html'), 'w', encoding='utf-8').write(html)


def main():
    names = sys.argv[1:] or list(FX)
    infos = []
    old = {}
    ds = os.path.join(HERE, 'khung', 'ds.json')
    if os.path.exists(ds):
        old = {e['name']: e for e in json.load(open(ds, encoding='utf-8'))}
    for n in names:
        try:
            old[n] = process(n)
        except FileNotFoundError as ex:
            print('thiếu nguồn', n, ex)
    infos = [old[n] for n in FX if n in old]
    os.makedirs(os.path.join(HERE, 'khung'), exist_ok=True)
    json.dump(infos, open(ds, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    page(infos)
    print('tổng ASTC ~%d KB' % sum(e['astc_kb'] for e in infos))


if __name__ == '__main__':
    main()
