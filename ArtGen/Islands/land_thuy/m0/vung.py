# Chia đảo vùng đất thành từng vùng boss (người dùng 2026-11-18: "phân section cho đảo, đánh xong 1 boss thì unlock section sau, chưa
# unlock thì có màu tối đen hẳn và tướng không play animation").
# - Vùng k = đoạn đường từ boss k-1 (không tính) tới boss k cộng bệ boss k; vùng 0 = bến và bệ ải 1. Vùng k mở khi đã qua ải của
#   boss k-1 (ZoneSceneLand: LandSections).
# - Ranh giới: mỗi chỗ trên đất thuộc vùng có đoạn đường (hay vòng đá bệ) gần nó nhất (biến đổi khoảng cách tới hạt giống). Đất =
#   mọi thứ không phải biển ngoài khơi (sông, hồ trong đảo tính là đất để tối liền một mảng).
# - Mặt nạ mỗi vùng (khung bao dùng cho camera, tâm mây tản): nới 2 ô rồi làm mềm, cắt theo khung bao, độ phân giải 1/DS đơn vị bản đồ.
# - Vẽ vùng khoá (người dùng 2026-11-18: "kết hợp cả A và B, mây tan ra, có bút chì vào tô màu section mới"; trước đó phủ đen bị chê):
#   truong(): ảnh trường vùng RG cho shader phác chì (R = chỉ số vùng × 25 làm mềm, biển lấy theo đất gần nhất; G = đất làm mềm);
#   may(): chỗ đặt mây phủ từng vùng (tâm mây trong vùng, cách vùng khác đủ xa, mây gần ranh nhỏ lại); luoi(): lưới vùng thô cho code
#   (ẩn hiệu ứng, đèn trong vùng khoá).
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

DS = 8          # đơn vị bản đồ mỗi ô mặt nạ
GROW, SOFT = 2, 2.2
PULL = 0.32     # khoảng cách tới tâm bệ boss tính bằng PULL lần (kéo vùng quanh bệ về boss của nó)


def chia(src, LW, LH, Q, t, along, habs, sea_mask):
    """trả (label (MH, MW) chỉ số vùng, -1 ngoài đất; land bool; [(alpha uint8, (x0, y0, x1, y1) ô mặt nạ)])"""
    MW, MH = LW // DS, LH // DS
    a = np.asarray(src.resize((MW, MH), Image.LANCZOS)).astype(np.float32)
    sea = sea_mask(a)
    # biển ngoài khơi: phần biển chạm mép ảnh; đất = phần còn lại, đóng cửa sông rồi lấp lỗ
    lab, _ = ndi.label(sea)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    open_sea = np.isin(lab, edge[edge > 0])
    land = ~open_sea
    land = ndi.binary_closing(land, iterations=4)
    land = ndi.binary_fill_holes(land)
    land = ndi.binary_opening(land, iterations=2)
    # bỏ mảnh vụn (đá ngoài khơi giữ nếu đủ lớn)
    lab2, n2 = ndi.label(land)
    if n2:
        sizes = ndi.sum(land, lab2, range(1, n2 + 1))
        land = np.isin(lab2, [i + 1 for i, s in enumerate(sizes) if s >= 40])

    # hạt giống: điểm đường theo đoạn, vòng đá bệ
    seed = np.zeros((MH, MW), np.int16)  # 0: không, k+1: vùng k
    K = len(habs)
    for i in range(len(t)):
        k = int(np.searchsorted(np.asarray(along), t[i], side="left"))  # t <= along[k] → vùng k
        k = min(k, K - 1)
        x, y = int(Q[i][0] / DS), int(Q[i][1] / DS)
        if 0 <= x < MW and 0 <= y < MH:
            seed[y, x] = k + 1
    yy, xx = np.mgrid[0:MH, 0:MW]
    for k, h in enumerate(habs):
        cx, cy = h["at"][0] * LW / DS, h["at"][1] * LH / DS
        rx, ry = h["ring"][0] * LW / DS * 1.25, h["ring"][1] * LH / DS * 1.25
        seed[((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1] = k + 1
    # khoảng cách tới đường của từng vùng, so với khoảng cách tới tâm bệ boss nhân PULL (< 1: quanh bệ thuộc vùng của bệ dù đường vùng
    # khác đi sát hơn, cảnh riêng của boss không bị cắt sang vùng sau)
    best = np.full((MH, MW), np.inf, np.float32)
    label = np.full((MH, MW), -1, np.int16)
    for k, h in enumerate(habs):
        dk = ndi.distance_transform_edt(seed != k + 1).astype(np.float32)
        cx, cy = h["at"][0] * LW / DS, h["at"][1] * LH / DS
        dk = np.minimum(dk, np.hypot(xx - cx, (yy - cy) * 1.6) * PULL)
        better = dk < best
        best[better] = dk[better]
        label[better] = k
    label[~land] = -1

    masks = []
    for k in range(K):
        m = label == k
        m = ndi.binary_dilation(m, iterations=GROW) & ndi.binary_dilation(land, iterations=GROW)
        al = ndi.gaussian_filter(m.astype(np.float32), SOFT)
        al = np.clip(al * 1.15, 0, 1)
        ys, xs = np.nonzero(al > 0.01)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        masks.append(((al[y0:y1, x0:x1] * 255).astype(np.uint8), (int(x0), int(y0), int(x1), int(y1))))
    return label, land, masks


FIELD_SOFT = 2.6   # làm mềm trường vùng (ô 1/DS): mép phác / màu mềm khoảng 20 đơn vị bản đồ
GRID = 8           # lưới thô: mỗi ô GRID ô mặt nạ (64 đơn vị bản đồ)


def truong(label, land):
    """ảnh RGBA (MH, MW): R = chỉ số vùng × 25 làm mềm, G = đất làm mềm, B = 0, A = 255"""
    _, (iy, ix) = ndi.distance_transform_edt(label < 0, return_indices=True)
    lab = label[iy, ix].astype(np.float32)
    v = ndi.gaussian_filter(lab, FIELD_SOFT)
    g = ndi.gaussian_filter(land.astype(np.float32), 1.0)
    out = np.zeros(label.shape + (4,), np.uint8)
    out[..., 0] = np.clip(np.round(v * 25), 0, 255)
    out[..., 1] = np.clip(np.round(g * 255), 0, 255)
    out[..., 3] = 255
    return out


def may(label, land, K, LW, LH, seed=11, gaps=None):
    """mây phủ từng vùng: [[x, y, w, lật] ...] theo tỉ lệ vùng đất (x, w theo bề ngang; y theo bề cao); gaps[k]: [(x, y, r) ...]
    (đơn vị bản đồ) khe chừa trống để thấy rương, ghi chú, xoáy nước bên dưới"""
    rng = np.random.default_rng(seed)
    near_land = ndi.binary_dilation(land, iterations=3)
    out = []
    step = 13  # ô mặt nạ (~105 đơn vị bản đồ); người dùng 2026-11-18: "cho mây che nhiều lên" (trước 24)
    MH, MW = label.shape
    for k in range(K):
        own = label == k
        other = (label >= 0) & (label != k)
        d = ndi.distance_transform_edt(~other)  # khoảng cách tới đất vùng khác (ô)
        reach = ndi.binary_dilation(own, iterations=3) & near_land
        ys, xs = np.nonzero(own)
        res = []
        if len(xs):
            for y in range(ys.min() - step // 2, ys.max() + step, step):
                for x in range(xs.min() - step // 2, xs.max() + step, step):
                    jx, jy = int(x + rng.uniform(-6, 6)), int(y + rng.uniform(-5, 5))
                    if not (0 <= jx < MW and 0 <= jy < MH) or not reach[jy, jx] or d[jy, jx] < 2.0:
                        continue
                    w = float(np.clip(d[jy, jx] * DS * 2.6, 260, 520) * rng.uniform(0.88, 1.12))
                    # mây bẹt (cao ~ nửa ngang): chừa khe theo elip quanh món cần lộ
                    if gaps and any(((jx * DS - gx) / (0.45 * w + gr)) ** 2 + ((jy * DS - gy) / (0.24 * w + gr)) ** 2 < 1
                                    for gx, gy, gr in gaps[k]):
                        continue
                    res.append([round(jx * DS / LW, 4), round(jy * DS / LH, 4), round(w / LW, 4), int(rng.random() < 0.5)])
        res.sort(key=lambda c: c[1])
        out.append(res)
    return out


# easter egg vùng khoá (người dùng 2026-11-18: "làm 1 vài easter egg cho các zone khi bị khóa", "làm cả 6"): hiệu ứng rò qua mây của
# từng vùng (đảo Thủy), ghi chú bút chì, rương bí ẩn (bi thưởng khi mở vùng). Mắt boss, boss ló đầu, chọc mây do game tự đặt theo bệ.
TEASE = {1: "dom_dom", 2: "den_bien", 3: "bong_bong", 4: "chim", 5: "set", 6: "phun_nuoc", 7: "phat_sang", 8: "tuyet", 9: "xoay"}


def gift(k):
    return 6 + 2 * k  # bi trong rương bí ẩn của vùng k (8–24)


def trung(label, land, Q, habs, LW, LH, anim, src=None, sea_mask=None):
    """trả (eggs[k]: {chest, gift, note, tease}, gaps[k]: [(x, y, r) đơn vị bản đồ])"""
    MH, MW = label.shape
    K = len(habs)
    path = np.zeros((MH, MW), bool)
    for x, y in Q:
        i, j = int(x / DS), int(y / DS)
        if 0 <= i < MW and 0 <= j < MH:
            path[j, i] = True
    dpath = ndi.distance_transform_edt(~path)
    inner = ndi.binary_erosion(land, iterations=3)
    dcoast = ndi.distance_transform_edt(land)  # khoảng cách tới biển ngoài khơi (ô)
    water = np.zeros_like(land)
    if src is not None and sea_mask is not None:  # sông, hồ trong đảo: rương không đặt trên nước
        a = np.asarray(src.resize((MW, MH), Image.LANCZOS)).astype(np.float32)
        water = ndi.binary_dilation(sea_mask(a), iterations=2)
    lights = anim.get("lights", [])
    swirl = next((it for it in anim.get("items", []) if it["k"] == "swirl"), None)
    eggs, gaps = [], []
    for k in range(K):
        e, g = {}, []
        own = label == k
        dother = ndi.distance_transform_edt(~((label >= 0) & ~own))
        hx, hy = habs[k]["at"][0] * LW, habs[k]["at"][1] * LH
        if k >= 1:
            # rương: sâu trong đất (không ra mỏm đá ngoài khơi, không trên nước), cách đường vừa phải, xa vùng khác và bệ boss
            dhab = np.hypot(np.arange(MW)[None, :] * DS - hx, np.arange(MH)[:, None] * DS - hy)
            ok = own & (dcoast >= 7) & ~water & (dhab > 260) & (dpath >= 9) & (dother >= 4)
            score = np.where(ok, np.minimum(dcoast, 16) * 1.5 + np.minimum(dother, 14) - np.maximum(dpath - 30, 0) * 0.6, -1)
            j, i = np.unravel_index(int(np.argmax(score)), score.shape)
            if score[j, i] > 0:
                e["chest"] = [round(i * DS / LW, 4), round(j * DS / LH, 4)]
                e["gift"] = gift(k)
                g.append((i * DS, j * DS, 90))
            # ghi chú: ở mép giáp vùng trước (chỗ người chơi đang đứng nhìn sang), không đè đường
            dprev = ndi.distance_transform_edt(label != k - 1)
            band = own & inner & (dprev > 4) & (dprev < 14) & (dpath > 7)
            ys, xs = np.nonzero(band)
            if len(xs):
                cx, cy = xs.mean(), ys.mean()
                m = int(np.argmin(np.hypot(xs - cx, ys - cy)))
                nx, ny = xs[m], ys[m]
                # ghi chú vẽ trên lớp mây (đọc được), không cần khe mây
                e["note"] = {"a": f"trung_ghi_{k}", "x": round(nx * DS / LW, 4), "y": round(ny * DS / LH, 4), "w": round(380 / LW, 4)}
        kind = TEASE.get(k)
        if kind:
            ys, xs = np.nonzero(own)
            cx, cy = (xs.mean() * DS, ys.mean() * DS) if len(xs) else (hx, hy)
            t = []
            if kind == "den_bien":
                b = next((l for l in lights if l["k"] == "beam"), None)
                if b:
                    t.append({"k": kind, "x": b["x"], "y": b["y"], "s": round(b["s"] * 1.4, 4)})
            elif kind == "phat_sang":
                for l in lights:
                    if l["k"] == "glow" and 0 <= int(l["y"] * LH / DS) < MH and 0 <= int(l["x"] * LW / DS) < MW                             and label[int(l["y"] * LH / DS), int(l["x"] * LW / DS)] == k:
                        t.append({"k": kind, "x": l["x"], "y": l["y"], "s": round(l["s"] * 4.5, 4)})
            elif kind == "xoay" and swirl:
                t.append({"k": kind, "x": swirl["x"], "y": swirl["y"], "s": swirl["s"]})
                g.append((swirl["x"] * LW, swirl["y"] * LH, swirl["s"] * LW * 0.55))
            elif kind in ("set", "phun_nuoc", "bong_bong"):
                t.append({"k": kind, "x": round(hx / LW, 4), "y": round((hy - 120) / LH, 4), "s": round(420 / LW, 4)})
            else:  # dom_dom, chim, tuyet: rải trên cả vùng
                bw = (xs.max() - xs.min()) * DS if len(xs) else 600
                t.append({"k": kind, "x": round(cx / LW, 4), "y": round(cy / LH, 4), "s": round(min(bw, 1100) / LW, 4)})
            if t:
                e["tease"] = t
        eggs.append(e)
        gaps.append(g)
    return eggs, gaps


def luoi(label):
    """lưới vùng thô: (gw, gh, chuỗi: '0'..'9' vùng, '.' biển), mỗi ô lấy nhãn nhiều nhất"""
    MH, MW = label.shape
    gw, gh = MW // GRID, MH // GRID
    rows = []
    for j in range(gh):
        row = []
        for i in range(gw):
            blk = label[j * GRID:(j + 1) * GRID, i * GRID:(i + 1) * GRID].ravel()
            blk = blk[blk >= 0]
            row.append('.' if len(blk) < GRID * GRID // 4 else str(int(np.bincount(blk).argmax())))
        rows.append(''.join(row))
    return gw, gh, ''.join(rows)


def open_count(habs, prog):
    """số vùng đã mở: vùng 0 luôn mở, vùng k mở khi đã qua ải boss k-1"""
    return 1 + sum(1 for h in habs[:-1] if prog >= h["stage"])


def darken(img, LW, LH, masks, opened, dark=0.86):
    """ảnh xem trước: phủ tối các vùng chưa mở lên ảnh (cỡ bất kỳ, cùng khung vùng đất)"""
    W, H = img.size
    acc = np.zeros((LH // DS, LW // DS), np.float32)
    for k, (al, (x0, y0, x1, y1)) in enumerate(masks):
        if k < opened:
            continue
        region = acc[y0:y1, x0:x1]
        a = al.astype(np.float32) / 255
        acc[y0:y1, x0:x1] = region + a * (1 - region)
    m = np.asarray(Image.fromarray((acc * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)).astype(np.float32) / 255
    out = np.asarray(img.convert("RGB")).astype(np.float32) * (1 - dark * m[..., None])
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))
