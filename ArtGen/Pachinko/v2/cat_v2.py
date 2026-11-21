# Cắt các tờ màn máy bi bản 2 (tai_ve/*_v2.png, Magnific GPT 2.6, PROMPTS_V2.md) thành ảnh game + số đo.
# Ra Assets/03 Art/Pachinko/:
#   pk_than_may_v2.png (thân máy vòm đỏ, đặt theo bo_cuc_v2.json: vùng khối máy REG), pk_bang_so_v2.png, pk_so_0..9, pk_so_cong,
#   pk_so_nhan, pk_push_{thuong,lun,het,lon} (chung đế, cùng khung), pk_v2_{cuoc,cuoc_khoa,khay,dem,lien,lien_bat},
#   fx2_* (12 hình sáng), pk_nen_phong.png (nền phòng);
# Assets/03 Art/Baked/Machine/may_tinh_v2.png: mặt bàn tĩnh, phần cam ngoài dải gỗ viền vòm thành trong suốt (thân máy mới nằm sau
#   bàn, hiện ra quanh vòm); dải gỗ, làn phóng giữ nguyên;
# v2/refs/v2_do.json: chỗ bóng đèn thân máy (px khối máy), bóng bảng số (tỉ lệ ảnh), màn tối bảng số, lõi bóng trong ảnh sáng.
# Chạy: py -3 -I ArtGen/Pachinko/v2/cat_v2.py [--xem out.png] (ảnh ghép thử toàn màn theo bố cục, không đụng Unity)
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(PK, "..", ".."))
IN = os.path.join(PK, "tai_ve")
ART = os.path.join(ROOT, "Assets", "03 Art", "Pachinko")
BAKED = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Machine")
LAY = json.load(open(os.path.join(HERE, "refs", "bo_cuc_v2.json"), encoding="utf-8"))
SURROUND = [(252, 116, 84), (236, 92, 64)]  # cam ngoài vòm + gạch chéo (ghep_ban.py)
# bản casino (người dùng 2026-11-20 chọn casino_B.png, "thêm 1 chút nhẹ kiểu tô chì"): tờ ở tai_ve/casino/, thân máy vẽ trên vùng
# rộng hơn (cột hai bên, bệ sau hàng nút, refs/bo_cuc_casino.json). --v3: cắt lại bản 3 (vòm đỏ gỗ) như cũ.
CASINO = os.path.exists(os.path.join(IN, "casino", "than_may_casino.png")) and "--v3" not in sys.argv
CASINO_LAY = json.load(open(os.path.join(HERE, "refs", "bo_cuc_casino.json"), encoding="utf-8")) if CASINO else None
SRC = {"than_may_v2.png": "casino/than_may_casino.png", "bang_so_v2.png": "casino/bang_so_casino.png",
       "nut_push_v2.png": "casino/nut_push_casino.png", "mon_v2.png": "casino/mon_casino.png",
       "nen_phong_v2.png": "casino/nen_phong_casino.png"} if CASINO else {}


def cab_region():
    return CASINO_LAY["region"] if CASINO else LAY["cab_canvas"]["region"]


def load(name):
    im = Image.open(os.path.join(IN, SRC.get(name, name))).convert("RGBA")
    a = np.array(im)
    a[:, :, 3][a[:, :, 3] >= 250] = 255  # GPT 2.6 trả độ đục tối đa 254
    return Image.fromarray(a, "RGBA")


def trim(im, pad=6):
    a = np.array(im)[:, :, 3]
    ys, xs = np.where(a > 8)
    if not len(xs):
        return im, (0, 0, 0, 0)
    box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + 1 + pad), min(im.height, ys.max() + 1 + pad))
    return im.crop(box), box


def cells(im, cols, rows):
    w, h = im.width / cols, im.height / rows
    return [im.crop((round(c * w), round(r * h), round((c + 1) * w), round((r + 1) * h))) for r in range(rows) for c in range(cols)]


def fit_max(im, side):
    s = min(1.0, side / max(im.size))
    return im if s >= 1 else im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def bulbs_in(im, area=(60, 900)):
    """Bóng đèn tắt vẽ tay: chấm kem sáng (không phải trắng thuần của cửa sổ), gần tròn."""
    a = np.array(im).astype(int)
    r, g, b, al = a[:, :, 0], a[:, :, 1], a[:, :, 2], a[:, :, 3]
    cream = (r > 225) & (g > 200) & (b > 120) & (b < 232) & (al > 240) & ((r - b) > 22)
    m = cream.astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, ar = st[i]
        if not (area[0] <= ar <= area[1]):
            continue
        if not (0.6 <= w / max(h, 1) <= 1.65):
            continue
        if ar / float(w * h) < 0.45:
            continue
        out.append((float(cen[i][0]), float(cen[i][1]), float(math.sqrt(ar / math.pi))))
    return out


def save(im, name, folder=ART):
    os.makedirs(folder, exist_ok=True)
    im.save(os.path.join(folder, name + ".png"))
    return name


def cabinet(do):
    im = load("than_may_v2.png")
    reg = cab_region()
    sc = im.width / (reg[2] - reg[0])
    k = im.width / 1024  # tờ 1k: 1, tờ 2k: 2 (ngưỡng đo theo tỉ lệ)
    found = bulbs_in(im, (120 * k * k, 900 * k * k))
    rail0 = LAY["cab"]["rail"][0]
    frame, rail = [], []
    for x, y, r in found:
        bx, by, br = reg[0] + x / sc, reg[1] + y / sc, r / sc
        (rail if by > rail0 - 6 else frame).append([round(bx, 1), round(by, 1), round(br, 1)])
    # thứ tự chạy: chân cột trái lên, qua vòm, xuống chân cột phải (góc quanh một điểm dưới mọi bóng)
    frame.sort(key=lambda p: -math.atan2(1500 - p[1], p[0] - 540))
    rail.sort(key=lambda p: p[0])
    # cửa sổ trắng nằm dưới bàn, nhưng lộ ra ở chỗ mặt bàn v2 trong suốt (dải cạnh làn phóng, góc ống làn): tô đỏ khung, gạch chéo
    # như cam ngoài vòm của mặt bàn cũ, lấn 2 px qua mép trắng cho khỏi viền sáng
    a = np.array(im).astype(int)
    # cửa sổ = vùng không phải khung (khung: đục và không trắng) chứa tâm ảnh; GPT có khi xoá nền lan vào giữa cửa sổ (mảng mờ),
    # nên lấy cả phần trắng lẫn phần trong suốt bên trong khung
    frameish = ((a[:, :, 3] > 200) & ~(a[:, :, :3].min(2) > 228)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - frameish, 4)
    c0 = lab[a.shape[0] // 2, a.shape[1] // 2]
    win = (lab == c0).astype(np.uint8) if c0 > 0 else np.zeros_like(frameish)
    win = cv2.dilate(win, np.ones((int(5 * k) | 1, int(5 * k) | 1), np.uint8)) > 0
    red = np.array([240, 74, 52])
    if CASINO:
        # đỏ ruby của dải vòm (trung vị các điểm đỏ đục)
        rr = (a[:, :, 0] > 140) & (a[:, :, 1] < 60) & (a[:, :, 2] < 80) & (a[:, :, 3] > 250)
        red = np.median(a[:, :, :3][rr], axis=0).astype(int)
    fill = np.zeros_like(a[:, :, :3]) + red
    a[:, :, :3][win] = fill[win]
    a[:, :, 3][win] = 255
    # bỏ ngôi sao giữa huy hiệu vòm: nấm đỉnh của bàn (vật va chạm thật, Board "Top") nằm đúng chỗ đó, thành viên ngọc giữa hai cuộn
    # xanh (như concept 1). Vùng sao (vàng + viền mực quanh nó) tô lại đỏ dải vòm có gạch chéo; giữ viền mực trên của vòm.
    cx = a.shape[1] // 2
    box = (slice(int(60 * k), int(220 * k)), slice(cx - int(110 * k), cx + int(110 * k)))
    sub = a[box]
    yellow = ((sub[:, :, 0] > 200) & (sub[:, :, 1] > 160) & (sub[:, :, 2] < 120) & (sub[:, :, 3] > 200)).astype(np.uint8)
    if yellow.sum() > 200 * k * k and not CASINO:
        n, lab, st, _ = cv2.connectedComponentsWithStats(yellow, 8)
        star = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
        d = int(17 * k) | 1
        star = cv2.dilate(star, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d, d))) > 0
        # viền trên của vòm: 10 px tính từ mép đục trên cùng của từng cột
        al = sub[:, :, 3] > 40
        top = np.argmax(al, axis=0)
        rows = np.arange(sub.shape[0])[:, None]
        keep_edge = rows < top[None, :] + 10 * k
        teal = (sub[:, :, 1] > 150) & (sub[:, :, 2] > 140) & (sub[:, :, 0] < 150)
        m = star & ~keep_edge & ~teal & al
        f = np.zeros_like(sub[:, :, :3]) + np.array([250, 86, 62])
        yy2, xx2 = np.mgrid[0:sub.shape[0], 0:sub.shape[1]]
        f[((xx2 + yy2) % 7) < 2] = [238, 70, 50]
        sub[:, :, :3][m] = f[m]
        a[box] = sub
    im = Image.fromarray(a.astype(np.uint8), "RGBA")
    # thu trước bằng LANCZOS về 1,33 lần cỡ hiện (900 px khối máy): máy 1440 px gần 1:1, máy 1080 thu nhẹ, khỏi răng cưa
    ow = round(1.333 * (reg[2] - reg[0]))
    save(im.resize((ow, round(ow * im.height / im.width)), Image.LANCZOS), "pk_than_may_v2")
    do["cabinet"] = {"rect": [reg[0], reg[1], reg[2] - reg[0], reg[3] - reg[1]], "bulbs": frame, "rail": rail}
    print(f"thân máy: {len(frame)} bóng khung, {len(rail)} bóng gờ đế, r ~{np.median([b[2] for b in frame + rail]):.1f} px khối")


def board_face():
    g = json.load(open(os.path.join(PK, "refs", "mat_may.json"), encoding="utf-8"))
    src = Image.open(os.path.join(BAKED, "may_tinh.png")).convert("RGBA")
    k = src.width / g["bw"]
    walls = [s for s in g["segs"] if s[5] == "Wall"]
    poly = [(walls[0][0] * k, walls[0][1] * k)] + [(s[2] * k, s[3] * k) for s in walls]
    inside = Image.new("L", src.size, 0)
    ImageDraw.Draw(inside).polygon(poly, fill=255)
    ins = np.array(inside) > 0
    # dải gỗ + mực: tới (2T+3)/2 = 8,5 đơn vị ngoài đường tường (ghep_ban.py bước 4), thêm 1 đơn vị cho khử răng cưa
    line = Image.new("L", src.size, 0)
    ImageDraw.Draw(line).line(poly, fill=255, width=1)
    dist = cv2.distanceTransform((np.array(line) == 0).astype(np.uint8), cv2.DIST_L2, 5)
    band = dist <= 9.5 * k
    a = np.array(src).astype(float)
    dcol = np.min([np.abs(a[:, :, :3] - np.array(c)).sum(2) for c in SURROUND], axis=0)
    # mức "cam": 0 ở màu cam, 1 khi khác hẳn
    keep = np.clip((dcol - 45) / 70, 0, 1)
    out_zone = ~ins & ~band
    alpha = a[:, :, 3] / 255
    alpha[out_zone] = alpha[out_zone] * keep[out_zone]
    a[:, :, 3] = np.round(alpha * 255)
    img = Image.fromarray(a.astype(np.uint8), "RGBA")
    save(img, "may_tinh_v2", BAKED)
    print("mặt bàn v2: cam ngoài vòm thành trong suốt", f"{int((alpha < 0.05).sum())} px")


def scoreboard(do):
    im, _ = trim(load("bang_so_v2.png"), 4)
    im = fit_max(im, 1024)
    a = np.array(im).astype(int)
    dark = ((a[:, :, 0] < 140) & (a[:, :, 1] < 80) & (a[:, :, 2] < 130) & (a[:, :, 2] - a[:, :, 1] > 8) & (a[:, :, 3] > 240)).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(dark, 8)
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h, _ = st[i]
    W, H = im.size
    uv = [round(x / W, 4), round(y / H, 4), round((x + w) / W, 4), round((y + h) / H, 4)]
    found = bulbs_in(im, (40, 1200))
    cx, cy = W / 2, H / 2
    found.sort(key=lambda p: math.atan2(p[1] - cy, (p[0] - cx) * H / W))  # vòng theo chiều kim đồng hồ từ bên trái
    save(im, "pk_bang_so_v2")
    do["score"] = {"size": [W, H], "screen_uv": uv, "bulbs": [[round(p[0] / W, 4), round(p[1] / H, 4), round(p[2] / H, 4)] for p in found]}
    print(f"bảng số: {W}x{H}, màn {uv}, {len(found)} bóng")


def digits():
    # Tách theo thành phần liền trên cả tờ (2026-11-22): GPT vẽ chữ số tràn qua lưới 6x2 đều (số 0 rộng tới x 282 trong ô 256),
    # cắt theo lưới làm 9/12 hình mất mép trái/phải. 12 hình trên tờ không dính nhau; bỏ đốm nhỏ theo diện tích, xếp theo hàng
    # (y tâm) rồi theo x để ứng đúng tên 0-9, cộng, nhân.
    im = load("chu_so_v2.png")
    a = np.array(im)
    m = (a[:, :, 3] > 8).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    big = [i for i in range(1, n) if st[i][cv2.CC_STAT_AREA] > 2000 * (im.width / 1536) ** 2]
    names = [f"pk_so_{i}" for i in range(10)] + ["pk_so_cong", "pk_so_nhan"]
    assert len(big) == len(names), f"tờ chữ số: thấy {len(big)} hình liền, cần {len(names)}"
    mid = im.height / 2
    big.sort(key=lambda i: (st[i][1] + st[i][3] / 2 > mid, st[i][0]))
    cs, boxes = [], []
    for i in big:
        x, y, w, h, _ = st[i]
        c = a.copy()
        c[:, :, 3][lab != i] = 0
        cs.append(Image.fromarray(c, "RGBA"))
        boxes.append((x, y, x + w, y + h))
    # cao chung = chữ số cao nhất; mỗi chữ số canh theo đáy của chính nó. Hai hàng ô trên tờ GPT vẽ chữ ở độ cao khác nhau:
    # lấy trên / dưới chung cả tờ làm 6-9 nằm cao hơn 0-5 khoảng 40 / 168 (số lệch, người dùng 2026-11-21).
    # Dấu cộng / nhân canh giữa khung. crop ngoài ảnh thì PIL độn trong suốt, nên mọi hình cùng tỉ lệ phóng.
    hh = max(b[3] - b[1] for b in boxes[:10])
    for c, b, n in zip(cs, boxes, names):
        t0, t1 = b[3] - hh, b[3]
        if n in ("pk_so_cong", "pk_so_nhan"):
            mid = (b[1] + b[3]) / 2
            t0, t1 = round(mid - hh / 2), round(mid + hh / 2)
        g = c.crop((b[0] - 6, t0 - 6, b[2] + 6, t1 + 6))
        s = 168 / g.height
        save(g.resize((max(1, round(g.width * s)), 168), Image.LANCZOS), n)
    print("chữ số: 12 hình cao 168")


def push(do):
    im = load("nut_push_v2.png")
    cs = cells(im, 2, 2)
    names = ["pk_push_thuong", "pk_push_lun", "pk_push_het", "pk_push_lon"]
    info = []
    for c in cs:
        a = np.array(c)[:, :, 3] > 20
        ys, xs = np.where(a)
        bot = ys.max()
        row = np.where(a[bot - int((bot - ys.min()) * 0.12)])[0]  # hàng gần đáy: bề ngang đế
        info.append((c, xs.min(), ys.min(), xs.max(), bot, (row.min() + row.max()) / 2, row.max() - row.min()))
    base_w = info[0][6]
    outs = []
    for c, x0, y0, x1, bot, bcx, bw in info:
        s = base_w / bw
        cc = c.resize((round(c.width * s), round(c.height * s)), Image.LANCZOS)
        outs.append((cc, bcx * s, bot * s, x0 * s, y0 * s, x1 * s))
    # khung chung: đáy đế thẳng hàng, tâm đế thẳng hàng
    left = max(o[1] - o[3] for o in outs) + 6
    right = max(o[5] - o[1] for o in outs) + 6
    up = max(o[2] - o[4] for o in outs) + 6
    W, H = round(left + right), round(up + 8)
    for (cc, bcx, bot, *_), n in zip(outs, names):
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(cc, (round(left - bcx), round(up - bot)))
        save(fit_max(canvas, 640), n)
    do["push"] = {"size": [W, H]}
    print(f"nút PUSH: 4 trạng thái, khung {W}x{H}")


def items():
    im = load("mon_v2.png")
    names = ["pk_v2_cuoc", "pk_v2_cuoc_khoa", "pk_v2_khay", "pk_v2_dem", "pk_v2_lien", "pk_v2_lien_bat"]
    for c, n in zip(cells(im, 3, 2), names):
        save(fit_max(trim(c, 6)[0], 512), n)
    print("6 món")


def fx(do):
    im = load("fx_sang_v2.png")
    names = ["fx2_den_vang", "fx2_den_hong", "fx2_den_trang", "fx2_quang", "fx2_sao4", "fx2_loe8", "fx2_quat", "fx2_xu", "fx2_giay",
             "fx2_vet", "fx2_vong", "fx2_sao5"]
    cores = {}
    # tờ vẽ trên nền đen, quầng bị giữ gần như đục và sẫm màu khi tách nền: gỡ nền đen (ghép lên đen rồi lấy độ sáng làm độ đục,
    # màu chia độ sáng), quầng mờ dần về trong suốt, lõi sáng giữ nguyên; nét mực sẫm cũng mờ đi (hình sáng không cần viền)
    a = np.array(im).astype(float)
    comp = a[:, :, :3] * (a[:, :, 3:4] / 255)
    m = comp.max(2)
    al = np.clip((m - 6) / 249, 0, 1)
    rgb = np.where(m[..., None] > 0, comp * 255 / np.maximum(m[..., None], 1), 0)
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8), "RGBA")
    for c, n in zip(cells(im, 4, 3), names):
        t, _ = trim(c, 4)
        a = np.array(t)[:, :, 3]
        # bóng đèn: lõi sáng (gần đục) so với cả hình (có quầng), để đặt lõi trùng bóng vẽ trên thân máy
        if n.startswith("fx2_den"):
            ys, xs = np.where(a > 225)
            cores[n] = round(float(max(xs.max() - xs.min(), ys.max() - ys.min())) / max(t.size), 3)
        # bóng đèn hiện chỉ 28–46 px (khung 1080): lưu sẵn 72 px cho khỏi răng cưa (ảnh không mipmap)
        save(fit_max(t, 72 if n.startswith("fx2_den") else 256), n)
    do["fx_core"] = cores
    print("12 hình sáng", cores)


def shooting_star(do):
    """Sao băng che chỗ ống phóng chui vào mặt chơi (như máy tham khảo): ghi tâm ngôi sao trong ảnh và bề ngang ngôi sao."""
    path = os.path.join(IN, "sao_bang_v2.png")
    if not os.path.exists(path):
        return
    t, _ = trim(load("sao_bang_v2.png"), 6)
    t = fit_max(t, 512)
    a = np.array(t).astype(int)
    # ngôi sao: mảng vàng lớn nhất ở nửa trên trái
    yel = ((a[:, :, 0] > 220) & (a[:, :, 1] > 150) & (a[:, :, 2] < 120) & (a[:, :, 3] > 200)).astype(np.uint8)
    yel[a.shape[0] // 2:, :] = 0
    yel[:, a.shape[1] // 2:] = 0
    n, lab, st, cen = cv2.connectedComponentsWithStats(yel, 8)
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h, _ = st[i]
    W, H = t.size
    save(t, "pk_sao_bang")
    do["sao"] = {"size": [W, H], "anchor": [round((x + w / 2) / W, 4), round((y + h / 2) / H, 4)], "star_w": round(max(w, h) / W, 4)}
    print("sao băng", do["sao"])


def chevron_glow():
    """Mũi tên sáng phủ lên mũi tên kem của ống phóng (mũi tên leo sáng như máy tham khảo): cùng hình mũi tên của ghep_ban_v2,
    lõi vàng kem, quầng mềm; gỡ sẵn kiểu nền đen (màu đủ sáng, độ đục theo quầng)."""
    s = 16  # px mỗi đơn vị máy
    lw = 10.92
    cw, ch = lw * 0.62, lw * 0.5
    W, H = int(cw * 2 * s * 2.2), int(ch * 1.6 * s * 3.0)
    cx, cy = W / 2, H / 2 + ch * 0.2 * s
    tri = [(cx, cy - ch * s), (cx + cw * s, cy + ch * 0.6 * s), (cx + cw * 0.45 * s, cy + ch * 0.6 * s), (cx, cy - ch * 0.15 * s),
           (cx - cw * 0.45 * s, cy + ch * 0.6 * s), (cx - cw * s, cy + ch * 0.6 * s)]
    core = Image.new("L", (W, H), 0)
    ImageDraw.Draw(core).polygon(tri, fill=255)
    c = cv2.GaussianBlur(np.array(core).astype(float) / 255, (0, 0), 1.2)
    # quầng rộng (phủ cả bề ngang rãnh) + lõi vàng cam rực: vẽ cộng sáng trên rãnh tối (như mũi tên tím HDR của máy tham khảo)
    glow = cv2.GaussianBlur(c, (0, 0), W * 0.16)
    glow = glow / max(glow.max(), 1e-6)
    al = np.clip(np.maximum(c, glow * 0.85), 0, 1)
    col = np.zeros((H, W, 3))
    t = np.clip(c[..., None], 0, 1)
    col[:] = np.array([255, 160, 40]) * (1 - t) + np.array([255, 236, 150]) * t
    img = Image.fromarray(np.dstack([col, al * 255]).astype(np.uint8), "RGBA")
    save(fit_max(img, 96), "fx2_mui_ten")  # hiện khoảng 50 px: thu sẵn cho khỏi răng cưa (ảnh không mipmap)
    return W, H


def room():
    im = Image.open(os.path.join(IN, SRC.get("nen_phong_v2.png", "nen_phong_v2.png"))).convert("RGB")
    fit_max(im, 2400).save(os.path.join(ART, "pk_nen_phong.png"))  # phủ 1080 x 1920–2340, máy 1440 gần 1:1
    print("nền phòng", im.size)


def preview(path):
    """Ghép thử màn 1080 x 1920 theo bố cục (khối máy 1080 x 1530 giữa vùng nội dung 1770, đỉnh nội dung ở 150)."""
    W, H = 1080, 1920
    top = 150 + (1770 - 1530) / 2  # đỉnh khối máy trên màn
    scr = Image.new("RGBA", (W, H))
    bg = Image.open(os.path.join(ART, "pk_nen_phong.png")).convert("RGBA")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
    scr.alpha_composite(bg, ((W - bg.width) // 2, (H - bg.height) // 2))

    def put(name, rect, folder=ART):
        im = Image.open(os.path.join(folder, name + ".png")).convert("RGBA")
        x0, y0, x1, y1 = rect
        im = im.resize((max(1, round(x1 - x0)), max(1, round(y1 - y0))), Image.LANCZOS)
        scr.alpha_composite(im, (round(x0), round(y0 + top)))

    reg = cab_region()
    put("pk_than_may_v2", reg)
    mv = json.load(open(os.path.join(HERE, "refs", "mat_v2.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "refs", "mat_v2.json")) else {"ext": 0}
    bd = LAY["board"]
    ku = (bd[2] - bd[0]) / 460  # px khối máy mỗi đơn vị máy
    put("may_tinh_v2", [bd[0], bd[1], bd[2] + mv["ext"] * ku, bd[3]], BAKED)
    do0 = json.load(open(os.path.join(HERE, "refs", "v2_do.json"), encoding="utf-8"))
    if "sao" in do0 and "entry" in mv:
        sa = do0["sao"]
        ex, ey = bd[0] + mv["entry"][0] * ku, bd[1] + mv["entry"][1] * ku
        # như MachineV2Menu: ngôi sao rộng 64 đơn vị, nghiêng 15° theo chiều kim đồng hồ quanh tâm sao; sao nhỏ lật gương bên trái
        def star(cx, cy, scale, flip):
            w = 64 * ku / sa["star_w"] * scale
            h = w * sa["size"][1] / sa["size"][0]
            im = Image.open(os.path.join(ART, "pk_sao_bang.png")).convert("RGBA").resize((round(w), round(h)), Image.LANCZOS)
            ax, ay = sa["anchor"][0] * w, sa["anchor"][1] * h
            if flip:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
                ax = w - ax
            pad = round(max(w, h))
            big = Image.new("RGBA", (round(w) + 2 * pad, round(h) + 2 * pad))
            big.alpha_composite(im, (pad, pad))
            big = big.rotate(15 if flip else -15, center=(pad + ax, pad + ay), resample=Image.BICUBIC)
            scr.alpha_composite(big, (round(cx - ax - pad), round(cy - ay - pad + top)))
        star(ex, ey, 1, False)
        star(bd[0] + (mv["bw"] - mv["entry"][0] - 22) * ku, bd[1] + (mv["entry"][1] - 6) * ku, 0.62, True)
    sb = LAY["score"]
    put("pk_bang_so_v2", sb)
    do = json.load(open(os.path.join(HERE, "refs", "v2_do.json"), encoding="utf-8"))
    uv = do["score"]["screen_uv"]
    sx0, sy0 = sb[0] + uv[0] * (sb[2] - sb[0]), sb[1] + uv[1] * (sb[3] - sb[1])
    sx1, sy1 = sb[0] + uv[2] * (sb[2] - sb[0]), sb[1] + uv[3] * (sb[3] - sb[1])
    dh = (sy1 - sy0) * 0.78
    x = (sx0 + sx1) / 2 - 1.5 * dh * 0.62
    for ch in "523":
        g = Image.open(os.path.join(ART, f"pk_so_{ch}.png"))
        w = dh * g.width / g.height
        put(f"pk_so_{ch}", [x, (sy0 + sy1) / 2 - dh / 2, x + w, (sy0 + sy1) / 2 + dh / 2])
        x += w * 0.92
    # bóng sáng xen kẽ trên vòm
    lit = Image.open(os.path.join(ART, "fx2_den_vang.png")).convert("RGBA")
    core = do["fx_core"]["fx2_den_vang"]
    for i, (bx, by, br) in enumerate(do["cabinet"]["bulbs"] + do["cabinet"]["rail"]):
        if i % 2:
            continue
        d = 2 * br / core
        put("fx2_den_vang", [bx - d / 2, by - d / 2, bx + d / 2, by + d / 2])
    for i, (u, v, r) in enumerate(do["score"]["bulbs"]):
        if i % 2:
            continue
        bx, by = sb[0] + u * (sb[2] - sb[0]), sb[1] + v * (sb[3] - sb[1])
        d = 2 * r * (sb[3] - sb[1]) / core
        put("fx2_den_vang", [bx - d / 2, by - d / 2, bx + d / 2, by + d / 2])
    pw = LAY["push"]
    put("pk_push_thuong", pw)
    put("pk_v2_cuoc", LAY["bet"])
    put("pk_v2_khay", LAY["tray"])
    put("pk_v2_lien", LAY["auto"])
    put("pk_v2_dem", LAY["counter"])
    scr.convert("RGB").save(path)
    print("ảnh ghép thử:", path)


def main():
    do = {}
    cabinet(do)
    if "--mat-cu" in sys.argv:
        board_face()  # bản 2: mặt bàn cũ bỏ góc cam; bản 3 dùng ghep_ban_v2.py
    scoreboard(do)
    digits()
    push(do)
    items()
    fx(do)
    shooting_star(do)
    chevron_glow()
    room()
    # cho Unity (JsonUtility không đọc mảng lồng): bóng thân máy thành một vòng liền (khung từ chân cột trái qua vòm xuống chân cột
    # phải, rồi gờ đế từ phải sang trái), phẳng x, y, r; lõi bóng của ảnh sáng vàng
    loop = do["cabinet"]["bulbs"] + do["cabinet"]["rail"][::-1]
    do["unity"] = {"rect": do["cabinet"]["rect"], "bulbs": [v for b in loop for v in b], "core": do["fx_core"]["fx2_den_vang"]}
    with open(os.path.join(HERE, "refs", "v2_do.json"), "w", encoding="utf-8") as f:
        json.dump(do, f, ensure_ascii=False, indent=1)
    if "--xem" in sys.argv:
        preview(sys.argv[sys.argv.index("--xem") + 1])


if __name__ == "__main__":
    main()
