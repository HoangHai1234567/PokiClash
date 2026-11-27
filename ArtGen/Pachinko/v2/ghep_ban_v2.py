# Mặt bàn máy bi bản 3 (GD_Claude/23; người dùng 2026-11-20: "đường ống bắn lên nhìn không khớp gì cả, đục kĩ con Clash of Critters
# và làm lại", "giảm bớt texture kiểu chì", "làm thật nét và thật đẹp, nặng cũng được").
# Ghép như ArtGen/Pachinko/ghep_ban.py (cùng hình học va chạm refs/mat_may.json, cùng tờ bộ phận), khác:
# - ngoài vòm trong suốt (thân máy vòm đỏ nằm sau bàn);
# - nền mặt chơi: tranh trời tô phẳng tai_ve/magnific/nen_mat_choi_v2.png (Magnific GPT 2.6 2k);
# - ô đáy tô phẳng (không gạch chéo), cọc vách gỗ phẳng; bộ phận vẽ tay làm phẳng vân chì (lọc giữ nét mực);
# - viền vòm là ống vàng tô phẳng (như vòng ống cam quanh mặt chơi của máy tham khảo);
# - ống phóng như máy tham khảo: rãnh tối hẹp, mũi tên kem chỉ lên, ống vàng hai bên; canvas nới EXT đơn vị bên phải cho ống ngoài
#   (Unity kéo ảnh tĩnh ra ngoài khung bàn đúng EXT, menu "Máy bi: bố cục bản 2" đọc refs/mat_v2.json);
# - chỗ ống chui vào mặt chơi ghi ra refs/mat_v2.json (sao băng che chỗ nối, như máy tham khảo).
# Ra Assets/03 Art/Baked/Machine/may_tinh_v2.png ((460 + EXT) x 680 đơn vị × OUTK) và v2/refs/mat_v2.json.
# Chạy: py -3 -I ArtGen/Pachinko/v2/ghep_ban_v2.py [--soi out.png]
import importlib.util
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PK = HERE.parent
spec = importlib.util.spec_from_file_location("pk_build", PK / "build.py")
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

GEOM = PK / "refs" / "mat_may.json"
PARTS = PK / "tai_ve" / "bo_phan.png"
BG = PK / "tai_ve" / "magnific" / "nen_mat_choi_v2.png"
# bản casino (người dùng 2026-11-20 chọn casino_B.png, "thêm 1 chút nhẹ kiểu tô chì, 1 chút thôi"): tờ bộ phận 4x3 mới (đinh vàng,
# phỉnh, cột vàng, cốc, thanh vàng, ngọc, thẻ bài), nền tím lưới vàng có mây; ô đáy là thẻ bài; vân chì nhẹ phủ cả bàn. --v3: bản cũ.
CASINO_DIR = PK / "tai_ve" / "casino"
CASINO = (CASINO_DIR / "bo_phan_casino.png").exists() and "--v3" not in sys.argv
if CASINO:
    PARTS = CASINO_DIR / "bo_phan_casino.png"
    BG = CASINO_DIR / "nen_mat_choi_casino_phang.png"
GRAIN = 0.02  # độ đậm vân chì phủ thêm (tỉ lệ sáng tối; người dùng: "1 chút thôi")
OUT = PK.parent.parent / "Assets" / "03 Art" / "Baked" / "Machine" / "may_tinh_v2.png"
INFO = HERE / "refs" / "mat_v2.json"
RAISE = 48
EXT = 10  # đơn vị máy thêm bên phải cho ống ngoài của làn
SS, OUTK = 2, 2.5  # ra 2,5 px mỗi đơn vị (máy 1440 px gần 1:1)

INK = (43, 33, 24, 255)
GOLD = (246, 180, 62)
GOLD_HI = (255, 218, 120)
WOOD = (214, 140, 82)
LANE_DARK = (58, 40, 84)
CHEVRON = (255, 241, 201)
SLOT_COLOR = dict(pk.SLOT_COLOR)
SLOT_DARK = (42, 17, 60)  # lòng thẻ ô số (casino): tím than, sẫm hơn hẳn nền mặt chơi (108, 20, 101) để số sáng nổi lên
TUBE = 5.0  # bề dày ống vàng (đơn vị)
INKW = 1.6


def flatten(im):
    """Làm phẳng vân chì của hình vẽ tay mà giữ nét mực: lọc giữ cạnh trên phần màu, trả lại nét mực sẫm như cũ."""
    a = np.array(im.convert("RGBA"))
    rgb = a[:, :, :3]
    sm = cv2.edgePreservingFilter(np.ascontiguousarray(rgb[:, :, ::-1]), flags=cv2.RECURS_FILTER, sigma_s=40, sigma_r=0.35)[:, :, ::-1]
    sm = cv2.bilateralFilter(np.ascontiguousarray(sm), 9, 40, 9)
    ink = rgb.max(2) < 95
    out = sm.copy()
    out[ink] = rgb[ink]
    a[:, :, :3] = out
    return Image.fromarray(a, "RGBA")


def ring_flat(size=256, inner=0.8):
    """Vòng tiến độ quanh nấm lớn (pk_vong_nam), như ring_sprite của ghep_ban.py nhưng dải trắng tô phẳng (game tô màu phần đầy)."""
    ss = 4
    n = size * ss
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = n / 2
    ro, ri, ink = c - 2 * ss, (c - 2 * ss) * inner, 3.2 * ss
    d.ellipse([c - ro, c - ro, c + ro, c + ro], fill=INK)
    d.ellipse([c - ro + ink, c - ro + ink, c + ro - ink, c + ro - ink], fill=(255, 255, 255, 255))
    d.ellipse([c - ri, c - ri, c + ri, c + ri], fill=INK)
    d.ellipse([c - ri + ink, c - ri + ink, c + ri - ink, c + ri - ink], fill=(0, 0, 0, 0))
    return im.resize((size, size), Image.LANCZOS)


def plate_flat(size=192):
    """Đĩa kem lót sau hình quà giữa nấm lớn (pk_dia_nam), tô phẳng."""
    ss = 4
    n = size * ss
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, r, ink = n / 2, n / 2 - 2 * ss, 3.4 * ss
    d.ellipse([c - r, c - r, c + r, c + r], fill=INK)
    d.ellipse([c - r + ink, c - r + ink, c + r - ink, c + r - ink], fill=(255, 246, 224, 255))
    return im.resize((size, size), Image.LANCZOS)


def flat_lattice(src, dst):
    """Nền mặt chơi casino: tranh gen có quầng mờ quanh lưới vàng (trông nhoè); ô tím tô lại một màu phẳng nhưng giữ vân chì nhỏ
    (chi tiết tần số cao), lưới vàng, sao lấp lánh, mây đáy và nét mực giữ nguyên."""
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    r, b = a[..., 0], a[..., 2]
    gold = np.clip((r - b - 70) / 70, 0, 1)
    cloud = a.min(2) > 150
    ink = a.max(2) < 90
    protect = cv2.dilate((cloud | ink).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) > 0
    deep = (gold == 0) & ~protect & (a.sum(2) < 330)
    purple = np.median(a[deep], axis=0)
    low = cv2.GaussianBlur(a, (0, 0), 3)
    flatv = purple[None, None, :] + (a - low) * 0.7
    t = gold[..., None]
    out = np.where(protect[..., None], a, flatv * (1 - t) + a * t)
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB").save(dst)
    print("nền lưới casino: tím phẳng", purple.round().tolist())


def cut_any(src, cols, rows):
    """Như pk.cut_cells(split=True) nhưng nhận tờ mọi cỡ (tờ casino 2k 3072 x 2048)."""
    im = Image.open(src).convert("RGBA")
    a0 = np.array(im)
    a0[:, :, 3][a0[:, :, 3] >= 250] = 255
    # nền tách chưa sạch (độ đục 1–63 rải khắp tờ): chỉ giữ độ đục quanh vật (đục > 128, nới 4 px cho mép khử răng cưa)
    core = (a0[:, :, 3] > 128).astype(np.uint8)
    near = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
    a0[:, :, 3][~near] = 0
    im = Image.fromarray(a0, "RGBA")
    cw, ch = im.width / cols, im.height / rows
    out = []
    for r in range(rows):
        for c in range(cols):
            cell = im.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch)))
            a = np.array(cell)[..., 3] > 8
            y0, y1 = pk.main_run(a.sum(1))
            x0, x1 = pk.main_run(a[y0:y1].sum(0))
            out.append(cell.crop((x0, y0, x1, y1)))
    return out


def pencil_grain(h, w, seed=7):
    """Vân chì nhẹ: nhiễu kéo thành nét chéo ngắn (như chì màu tô xiên), trung bình 0, độ lệch 1."""
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((h, w)).astype(np.float32)
    k = np.fliplr(np.eye(9, dtype=np.float32)) / 9
    s = cv2.filter2D(n, -1, k)
    s = cv2.GaussianBlur(s, (0, 0), 0.6)
    return np.clip(s / (s.std() + 1e-6), -2.5, 2.5)


def tall_card(spr, w, h):
    """Thẻ bài cao co theo bề ngang ô, giữ nguyên đầu và đáy thẻ (góc kim cương), kéo dãn khúc giữa cho đủ cao."""
    s = w / spr.width
    top = spr.crop((0, 0, spr.width, int(spr.height * 0.3)))
    bot = spr.crop((0, int(spr.height * 0.7), spr.width, spr.height))
    mid = spr.crop((0, int(spr.height * 0.3), spr.width, int(spr.height * 0.7)))
    th, bh = max(1, round(top.height * s)), max(1, round(bot.height * s))
    mh = max(1, round(h) - th - bh)
    out = Image.new("RGBA", (round(w), th + mh + bh), (0, 0, 0, 0))
    out.paste(top.resize((round(w), th), Image.LANCZOS), (0, 0))
    out.paste(mid.resize((round(w), mh), Image.LANCZOS), (0, th))
    out.paste(bot.resize((round(w), bh), Image.LANCZOS), (0, th + mh))
    return out


def dark_card(spr, rgb=SLOT_DARK):
    """Thẻ ô số tối (người dùng 2026-11-27: "các số phần thưởng còn nhỏ không nổi bật, sửa lại cho nền các ô tối màu hơn"): lòng kem
    của thẻ (mảng kem liền lớn nhất) tô lại màu sẫm, giữ viền vàng, góc kim cương, nét mực; mép khử răng cưa giữa kem và mực nội suy
    theo độ sáng từ mực tới màu sẫm cho khỏi viền sáng."""
    a = np.array(spr.convert("RGBA")).astype(np.float32)
    r, b = a[..., 0], a[..., 2]
    cream = (a[..., :3].min(2) > 170) & (r - b < 70)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cream.astype(np.uint8), connectivity=4)
    if n < 2:
        return spr
    core = lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    zone = cv2.dilate(core.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
    zone &= (r - b) < 90  # không lan sang viền vàng (vàng: đỏ trừ lam rất lớn)
    lum = a[..., :3].mean(2)
    ref = float(np.median(lum[core]))
    ink = np.array(INK[:3], np.float32)
    t = np.clip((lum - 45) / (ref - 45), 0, 1)[..., None]
    col = ink * (1 - t) + np.array(rgb, np.float32) * t + ((lum - ref) * 0.25 * t[..., 0])[..., None]
    a[..., :3] = np.where(zone[..., None], col, a[..., :3])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def square_pad(im, fill_frac):
    """Đặt hình vào ô vuông, hình chiếm fill_frac bề rộng ô (nấm: ảnh chừa viền vài đơn vị quanh vật va chạm)."""
    side = round(max(im.size) / fill_frac)
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
    return out


def smooth_poly(pts, iters=4, sharp_deg=40):
    """Làm tròn vòm (người dùng 2026-11-20: "đường vòm gấp khúc quá, làm tròn vào"): cắt góc Chaikin trên đa giác kín, giữ nguyên
    đỉnh gắt (rẽ quá sharp_deg: hai góc đáy, mỏ hắt ở miệng ống). Chỉ đổi hình vẽ; vách va chạm giữ đúng đa giác của Board."""
    pts = [tuple(p) for p in pts]
    if pts[0] == pts[-1]:
        pts = pts[:-1]

    def sharp_flags(ps):
        n = len(ps)
        out = []
        for i in range(n):
            ax, ay = ps[i - 1]
            bx, by = ps[i]
            cx, cy = ps[(i + 1) % n]
            a1 = math.atan2(by - ay, bx - ax)
            a2 = math.atan2(cy - by, cx - bx)
            turn = abs((math.degrees(a2 - a1) + 180) % 360 - 180)
            out.append(turn > sharp_deg)
        return out
    keep = sharp_flags(pts)
    for _ in range(iters):
        n = len(pts)
        new, nk = [], []
        for i in range(n):
            p0, p1 = pts[i], pts[(i + 1) % n]
            if keep[i]:
                new.append(p0)
                nk.append(True)
            q = (p0[0] * 0.75 + p1[0] * 0.25, p0[1] * 0.75 + p1[1] * 0.25)
            r = (p0[0] * 0.25 + p1[0] * 0.75, p0[1] * 0.25 + p1[1] * 0.75)
            new += [q, r]
            nk += [False, False]
        pts, keep = new, nk
    return pts


def main():
    g = json.loads(GEOM.read_text(encoding="utf-8"))
    BW, BH, U = int(g["bw"]), int(g["bh"]), g["u"]
    K = SS * OUTK
    if CASINO:
        src_bg = CASINO_DIR / "nen_mat_choi_casino.png"
        if not BG.exists() or BG.stat().st_mtime < src_bg.stat().st_mtime:
            flat_lattice(src_bg, BG)
        cells = cut_any(PARTS, 4, 3)
        peg, chip, chip_lit, post, cup, roof, ruby, ruby_lit, peg_lit, card, card_gold, _stud = cells
        bump = ruby  # núm đáy V cũng là ngọc: MachineBoard cho núm đáy V và nấm đỉnh chung hình sáng pk_u_loi_sang
    else:
        parts = [flatten(p) for p in pk.cut_cells(PARTS, 4, 3, split=True)]
        peg, _bumper, bump, post, cup, roof, _floor, _cloud, _ball, shoulder, _rail, _plate = parts
    W = BW + EXT
    img = Image.new("RGBA", (round(W * K), round(BH * K)), (0, 0, 0, 0))

    def P(x, y):
        return (x * K, y * K)

    def put(spr, cx, cy, w, h=None, angle=0):
        h = h if h is not None else w * spr.height / spr.width
        im = spr.resize((max(1, round(w * K)), max(1, round(h * K))), Image.LANCZOS)
        if angle:
            im = im.rotate(-angle, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(im, (round(cx * K - im.width / 2), round(cy * K - im.height / 2)))

    def plank(spr, x1, y1, x2, y2, thick, extra):
        length = math.hypot(x2 - x1, y2 - y1) + 2 * extra
        im = pk.three_slice(spr, length * K, thick * K)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        im = im.rotate(-ang, resample=Image.BICUBIC, expand=True)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        img.alpha_composite(im, (round(cx * K - im.width / 2), round(cy * K - im.height / 2)))

    def paste_masked(layer, mask):
        clipped = Image.new("RGBA", img.size, (0, 0, 0, 0))
        clipped.paste(layer, (0, 0), mask)
        img.alpha_composite(clipped)

    def flat(rgb, a=255):
        return Image.new("RGBA", img.size, tuple(rgb) + (a,))

    walls = [s for s in g["segs"] if s[5] == "Wall"]
    poly = smooth_poly([(walls[0][0], walls[0][1])] + [(s[2], s[3]) for s in walls])
    poly = poly + [poly[0]]
    inside = Image.new("L", img.size, 0)
    ImageDraw.Draw(inside).polygon([P(x, y) for x, y in poly], fill=255)
    outside = Image.eval(inside, lambda v: 255 - v)

    # 1. nền mặt chơi: tranh trời tô phẳng, đáy tranh ở đáy máy (mây ló trên hàng ô)
    xs = [x for x, _ in poly]
    bx0, bx1, by0 = min(xs), max(xs), min(y for _, y in poly)
    if BG.exists():
        bw, bh = (bx1 - bx0) * K, (BH - by0) * K
        bg = Image.open(BG).convert("RGBA")
        s = max(bw / bg.width, bh / bg.height)
        bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        lift = round(RAISE * K)
        top = round(BH * K - bg.height - lift)
        layer.paste(bg, (round(bx0 * K + (bw - bg.width) / 2), top))
        if lift > 0:
            strip = bg.crop((0, bg.height - 2, bg.width, bg.height)).resize((bg.width, lift + 2))
            layer.paste(strip, (round(bx0 * K + (bw - bg.width) / 2), top + bg.height - 2))
        paste_masked(layer, inside)
    else:
        paste_masked(flat((190, 232, 250)), inside)

    # 2. ô đáy: casino là thẻ bài viền vàng, lòng tím than (ô rương: thẻ vàng tia kem) như casino_B; bản cũ phủ màu phẳng nửa trong
    card_num = dark_card(card) if CASINO else None
    for x0, y0, x1, y1, kind in (g["slots"] if CASINO else []):
        cw_ = x1 - x0 - 3
        cimg = tall_card(card_gold if kind.startswith("chest") else card_num, cw_ * K, (BH - y0 + 6) * K)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        layer.alpha_composite(cimg, (round((x0 + 1.5) * K), round((y0 + 1) * K)))
        paste_masked(layer, inside)
    for x0, y0, x1, y1, kind in ([] if CASINO else g["slots"]):
        box = Image.new("L", img.size, 0)
        ImageDraw.Draw(box).rectangle([P(x0, y0), P(x1, BH)], fill=255)
        mask = Image.fromarray(np.minimum(np.array(box), np.array(inside)))
        paste_masked(flat(SLOT_COLOR[kind], 150), mask)
    if not CASINO:
        slot_top = min(s[1] for s in g["slots"])
        ln = Image.new("L", img.size, 0)
        ImageDraw.Draw(ln).line([P(0, slot_top), P(BW, slot_top)], fill=70, width=round(K))
        paste_masked(flat(INK[:3]), Image.fromarray(np.minimum(np.array(ln), np.array(inside))))

    # 3. viền vòm: ống vàng tô phẳng ngoài cạnh va chạm (dải sáng giữa ống), mực hai mép
    T = 7
    o = np.array(outside)
    lane0, lw0 = g["lane"], g["lane_half"]
    # khe giữa vách phải của vòm và làn (ngoài vòm, trên đoạn dọc của làn): lấp vàng cho vòm và ống liền một gờ như máy tham khảo
    ins_np = np.array(inside) > 0
    fill_np = np.zeros(ins_np.shape, np.uint8)
    xl = int(lane0[0][0] * K)
    # x tâm làn theo từng hàng (đoạn uốn, đoạn chéo vào vòm): lấp cả khe tam giác giữa vòm và chỗ ống bắt đầu uốn
    lane_x_row = {}
    for i in range(1, len(lane0)):
        (ax, ay), (bx2, by2) = lane0[i - 1], lane0[i]
        nn = max(1, int(math.hypot(bx2 - ax, by2 - ay) * K))
        for kk in range(nn + 1):
            px, py = (ax + (bx2 - ax) * kk / nn) * K, (ay + (by2 - ay) * kk / nn) * K
            lane_x_row[int(py)] = max(lane_x_row.get(int(py), 0), int(px))
    y_start = int(min(lane_x_row)) if lane_x_row else int(lane0[1][1] * K)
    for yy in range(y_start, ins_np.shape[0]):
        xr = min(xl, lane_x_row.get(yy, xl))
        r = np.where(ins_np[yy, : xr])[0]  # vách phải của vòm xiên: lấp theo từng hàng
        if len(r):
            fill_np[yy, r.max(): xr] = 255
    paste_masked(flat(GOLD), Image.fromarray(np.minimum(fill_np, o)))

    def band(width):
        m = Image.new("L", img.size, 0)
        ImageDraw.Draw(m).line([P(x, y) for x, y in poly], fill=255, width=round(width * K), joint="curve")
        return Image.fromarray(np.minimum(np.array(m), o))
    paste_masked(flat(INK[:3]), band(2 * T + 3))
    paste_masked(flat(GOLD), band(2 * T))
    paste_masked(flat(GOLD_HI), band(T * 0.9))
    ImageDraw.Draw(img).line([P(x, y) for x, y in poly], fill=INK, width=round(INKW * K), joint="curve")

    # 4. ống phóng: rãnh tối, ống vàng hai bên, mực các mép; mũi tên kem chỉ lên trên đoạn dọc
    lane = g["lane"]
    lw = g["lane_half"]
    d = ImageDraw.Draw(img)
    # tô theo khoảng cách tới đường tâm làn (lớp ống song song tuyệt đối, đầu tròn, không gai ở chỗ uốn); chân làn kéo dài thêm
    # một bán kính làm bệ phóng tròn
    x0, y0 = lane[0]
    center = Image.new("L", img.size, 0)
    cl = [P(x0, y0 + lw * 0.9)] + [P(x, y) for x, y in lane]
    ImageDraw.Draw(center).line(cl, fill=255, width=1)
    dist = cv2.distanceTransform((np.array(center) == 0).astype(np.uint8), cv2.DIST_L2, 5) / K
    lay = np.zeros((img.height, img.width, 4), np.uint8)
    r1, r2, r3, r4 = lw, lw + INKW, lw + INKW + TUBE, lw + 2 * INKW + TUBE
    for lo, hi, col in ((0, r1, LANE_DARK), (r1, r2, INK[:3]), (r2, r3, GOLD), (r3, r4, INK[:3])):
        m = (dist >= lo) & (dist < hi)
        lay[m, :3] = col
        lay[m, 3] = 255
    hi_m = (dist >= r2 + TUBE * 0.3) & (dist < r2 + TUBE * 0.7)
    lay[hi_m, :3] = GOLD_HI
    img.alpha_composite(Image.fromarray(lay, "RGBA"))
    # mũi tên: như máy tham khảo, nhỏ, sát nhau (ghep_ban cũ cách 24 đơn vị)
    vx, top = lane[0][0], lane[1][1]
    chev = []
    yy = y0 - 18
    while yy > top + 14:
        cw, ch = lw * 0.62, lw * 0.5
        tri = [P(vx, yy - ch), P(vx + cw, yy + ch * 0.6), P(vx + cw * 0.45, yy + ch * 0.6), P(vx, yy - ch * 0.15),
               P(vx - cw * 0.45, yy + ch * 0.6), P(vx - cw, yy + ch * 0.6)]
        d.polygon(tri, fill=CHEVRON + (255,))
        chev.append([round(vx, 2), round(yy, 2)])
        yy -= 24

    # 5. vách ô: thân gỗ phẳng đúng bề rộng hộp va chạm, núm vẽ tay đè nắp tròn
    knob_h = post.width
    tops = [s for s in g["segs"] if s[5] == "Divider"]
    caps = [p for p in g["pegs"] if p[3] == "Cap"]
    top_img = post.crop((0, 0, post.width, knob_h))
    stick = post.crop((0, knob_h, post.width, post.height))
    for x1, y1, x2, y2, r, _ in tops:
        wdt = 2 * r
        s = wdt / post.width
        cap = min(caps, key=lambda p: abs(p[0] - x1)) if caps else None
        if not cap:
            ytop = min(y1, y2) - r
            stick_len = BH - (ytop + knob_h * s) + 1
            put(stick, x1, ytop + knob_h * s + stick_len / 2 - 0.5, post.width * s * 0.9, stick_len)
            put(top_img, x1, ytop + knob_h * s / 2, wdt, knob_h * s)
            continue
        cx, cy, cr = cap[0], cap[1], cap[2]
        yb = cy + cr * 0.4
        bar = Image.new("L", img.size, 0)
        ImageDraw.Draw(bar).rectangle([P(x1 - r, yb), P(x1 + r, BH)], fill=255)
        paste_masked(flat(GOLD if CASINO else WOOD), bar)
        dd = ImageDraw.Draw(img)
        if CASINO:
            dd.rectangle([P(x1 - r * 0.15, yb), P(x1 + r * 0.35, BH)], fill=GOLD_HI)
        for ex in (x1 - r + 0.8, x1 + r - 0.8):
            dd.line([P(ex, yb), P(ex, BH)], fill=INK, width=round(INKW * K))
        kw = 2 * cr * 1.08 if CASINO else 2 * cr * post.width / 57
        put(top_img, cx, cy, kw, kw * knob_h / post.width)

    # 6. cốc dưới mái, mái hai cánh, đáy V và núm, đinh
    for cx0, cy0, cx1, cy1, _ in g["cups"]:
        cw = (cx1 - cx0) * 0.86
        put(cup, (cx0 + cx1) / 2, cy0 + (cy1 - cy0) * 0.6, cw, cw * cup.height / cup.width)
    for x1, y1, x2, y2, r, kind in g["segs"]:
        if kind in ("Roof", "Floor"):
            spr = roof if x2 > x1 else roof.transpose(Image.FLIP_LEFT_RIGHT)
            plank(spr, x1, y1, x2, y2, 2 * r, 0)
    for x, y, r, kind in g["pegs"]:
        if kind == "Post":
            put(bump, x, y, 2 * r + 1.5)
    for x, y, r, kind in g["pegs"]:
        if kind == "Peg":
            put(peg, x, y, 2 * r + 2)

    out = img.resize((round(W * OUTK), round(BH * OUTK)), Image.LANCZOS)
    if CASINO and GRAIN > 0:
        # vân chì nhẹ phủ cả bàn (ống vàng, làn, vách vẽ phẳng bằng code thành cùng chất tay với tranh gen)
        oa = np.array(out).astype(np.float32)
        gr = pencil_grain(oa.shape[0], oa.shape[1])
        oa[..., :3] = np.clip(oa[..., :3] * (1 + GRAIN * gr[..., None]), 0, 255)
        out = Image.fromarray(oa.astype(np.uint8), "RGBA")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)

    # chỗ ống chui vào mặt chơi: điểm đầu tiên trên làn (đi từ chân lên) nằm trong vòm
    ins = np.array(inside) > 0
    total = sum(math.hypot(lane[i][0] - lane[i - 1][0], lane[i][1] - lane[i - 1][1]) for i in range(1, len(lane)))
    entry = lane[-1]
    acc, step = 0.0, 1.0
    found = False
    for i in range(1, len(lane)):
        (ax, ay), (bx, by) = lane[i - 1], lane[i]
        seg = math.hypot(bx - ax, by - ay)
        n = max(1, int(seg / step))
        for k in range(n + 1):
            x, y = ax + (bx - ax) * k / n, ay + (by - ay) * k / n
            px, py = int(x * K), int(y * K)
            if 0 <= py < ins.shape[0] and 0 <= px < ins.shape[1] and ins[py, px] and y < lane[1][1] + 40:
                entry = (x, y)
                found = True
                break
        if found:
            break
    info = {"ext": EXT, "outk": OUTK, "bw": BW, "bh": BH, "lane_half": lw, "tube": TUBE, "chevrons": chev, "entry": [round(entry[0], 2), round(entry[1], 2)],
            "lane_top": round(lane[1][1], 2), "lane_x": round(lane[0][0], 2)}
    INFO.write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    # vòng tiến độ, đĩa lót của nấm lớn: bản tô phẳng (bỏ gạch chéo), cùng hình với bản ghep_ban.py
    # casino: vòng mảnh hơn (chỉ đè vành vàng của phỉnh, chừa dải trắng đỏ), nấm là phỉnh, nấm đỉnh là ngọc, đinh sáng vàng
    pk.save_game(ring_flat(inner=0.9 if CASINO else 0.8), "pk_vong_nam")
    pk.save_game(plate_flat(), "pk_dia_nam")
    if CASINO:
        fit = lambda im, side: im.resize((side, side), Image.LANCZOS)
        pk.save_game(fit(square_pad(chip, 42.9 / 44.9), 256), "pk_bumper")
        pk.save_game(fit(square_pad(chip_lit, 42.9 / 44.9), 256), "pk_bumper_sang")
        pk.save_game(fit(square_pad(ruby, 27.3 / 28.3), 192), "pk_nam_dinh")
        pk.save_game(fit(square_pad(ruby_lit, 1.0), 192), "pk_u_loi_sang")
        pk.save_game(fit(square_pad(peg_lit, 1.0), 64), "pk_dinh_sang")
    print(f"mặt bàn v3: {OUT.name} {out.width}x{out.height}, {len(chev)} mũi tên, chỗ ống vào vòm {info['entry']}")

    if "--soi" in sys.argv:
        dst = Path(sys.argv[sys.argv.index("--soi") + 1])
        soi = Image.new("RGBA", out.size, (232, 96, 74, 255))
        soi.alpha_composite(out)
        sd = ImageDraw.Draw(soi)
        k = OUTK
        for x, y, r, kind in g["pegs"]:
            sd.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], outline=(0, 160, 255, 255), width=2)
        for x1, y1, x2, y2, r, kind in g["segs"]:
            sd.line([x1 * k, y1 * k, x2 * k, y2 * k], fill=(0, 160, 255, 255), width=max(2, round(2 * r * k)) if r else 2)
        ex, ey = info["entry"]
        sd.ellipse([(ex - 4) * k, (ey - 4) * k, (ex + 4) * k, (ey + 4) * k], outline=(255, 0, 255, 255), width=3)
        soi.convert("RGB").save(dst)
        print("ảnh soi", dst)


if __name__ == "__main__":
    main()
