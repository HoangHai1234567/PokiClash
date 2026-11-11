"""Cách LAI cho dạng 1, 2 dòng Hải Long (chuẩn 2026-11-11): đầu, hàm, râu, cổ, đuôi, vòng thân CẮT THẲNG TỪ CONCEPT theo mặt nạ +
hình học đã dò (khop.json); mọi điểm thân còn lại gán cho mảnh gần nhất (nhãn gần nhất, như thuy_long_lien.py) nên bóng dáng khung 0
trùng concept. Lớp dưới (cổ) mọc thêm GROW px dưới lớp trên (đầu, cổ trước) và dưới mặt nước, vẽ bù bằng inpaint. Cổ uốn bằng chuỗi
xương n<hid>* sẵn có (đường tâm Dijkstra) với trọng số B-spline chiếu lên chuỗi, lưới vùng dày của chính hình concept
(quai.luoi.luoi_vung, bước theo chiều cao con). Phần dưới mặt nước vẫn là dải cổ GPT (slot c<hid>) nằm DƯỚI cổ concept (slot cc<hid>),
mặt nạ cắt + sóng che chỗ nối. Hàm dưới: vùng hàm concept (dáng gốc hé), xoay quanh bản lề; lòng miệng = mảng hồng phẳng đúng vùng
hàm, bám đầu (hé thì lộ). Hình nước dùng chung với dạng 3.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm10_lai.py cat 2     cắt -> inbox/tm10_2/manh_lai/*.png + lai.json + _soi.png
    (tm10.py rig <k> tự gọi apply_lai khi có lai.json)
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import hai_long as HL  # noqa: E402
import hai_long_soi as S  # noqa: E402
import tm10_khop as KH  # noqa: E402
from quai import luoi as QL  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
GROW = 44            # lớp dưới mọc thêm dưới lớp trên (px concept; đích ≥ 30, lấy 44 để đầu ngửa 40° chưa lộ mép cắt)
FLESH = (176, 58, 84)   # màu lòng miệng (hồng sẫm, phẳng)
K5 = np.ones((5, 5), np.uint8)


def paths(k):
    inbox = os.path.join(HERE, "inbox", f"tm10_{k}")
    return inbox, os.path.join(inbox, "tai_ve", "L1_duyet.png"), os.path.join(inbox, "manh"), os.path.join(inbox, "manh_lai"), os.path.join(inbox, "rig", "khop.json")


def kdisk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def warp_alpha(piece_path, cx, cy, ang, sc, shape):
    """mặt nạ (bool, cỡ concept) của mảnh GPT đặt theo kết quả dò (tâm, góc, tỉ lệ)."""
    im = Image.open(piece_path).convert("RGBA")
    im = im.crop(im.getbbox())
    a = (np.asarray(im)[..., 3] > 100).astype(np.uint8)
    M = cv2.getRotationMatrix2D((im.width / 2, im.height / 2), ang, sc)
    M[0, 2] += cx - im.width / 2
    M[1, 2] += cy - im.height / 2
    return cv2.warpAffine(a, M, (shape[1], shape[0]), flags=cv2.INTER_NEAREST) > 0


def biggest(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 2:
        return m
    return lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))


def crop_piece(rgb, region, grow=None, fill_rgb=None):
    """cắt vùng region (bool) khỏi ảnh concept thành RGBA. grow (bool): pixel mọc thêm, vẽ bù bằng inpaint từ màu vùng (fill_rgb: tô
    phẳng thay inpaint). Trả (PIL RGBA, (x0, y0)) hoặc (None, ...)."""
    reg = region if grow is None else (region | grow)
    ys, xs = np.nonzero(reg)
    if not len(xs):
        return None, (0, 0)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    sub = rgb[y0:y1, x0:x1].copy()
    m = reg[y0:y1, x0:x1]
    if grow is not None:
        g = grow[y0:y1, x0:x1] & ~region[y0:y1, x0:x1]
        if g.any():
            if fill_rgb is not None:
                sub[g] = fill_rgb
            else:
                # điểm mọc thêm lấy màu của điểm vùng gần nhất (kéo dài nét mực, vân sáp ra ngoài); inpaint TELEA nhoè thành vệt bẩn
                r0 = region[y0:y1, x0:x1]
                # lấy màu từ trong hình (cách mép 8 px, bỏ điểm mực sẫm): không kéo viền mực ra, không thành mảng sẫm dưới hàm (lỗi đã gặp)
                ink = cv2.cvtColor(sub, cv2.COLOR_RGB2HSV)[..., 2] < 110
                r_in = cv2.erode(r0.astype(np.uint8), kdisk(8)).astype(bool) & ~ink
                if r_in.sum() > 50:
                    r0 = r_in
                _, lbl = cv2.distanceTransformWithLabels((~r0).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                ry_, rx_ = np.nonzero(r0)
                src_idx = np.zeros(int(lbl.max()) + 1, np.int64)
                src_idx[lbl[ry_, rx_]] = ry_ * r0.shape[1] + rx_
                flat = sub.reshape(-1, 3)
                gy_, gx_ = np.nonzero(g)
                sub[gy_, gx_] = flat[src_idx[lbl[gy_, gx_]]]
                sub = cv2.GaussianBlur(sub, (0, 0), 1.2) * g[..., None] + sub * (~g)[..., None]
                sub = sub.astype(np.uint8)
    al = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)
    rgba = np.dstack([sub, (np.clip(al * 1.25, 0, 1) * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), (int(x0), int(y0))


def pca_axis(mask):
    ys, xs = np.nonzero(mask)
    pts = np.stack([xs, ys], axis=1).astype(float)
    c = pts.mean(axis=0)
    _, _, vt = np.linalg.svd(pts - c, full_matrices=False)
    ax = vt[0]
    proj = (pts - c) @ ax
    return c, ax, float(proj.min()), float(proj.max())


def nearest_fill(labels, body):
    """điểm thân chưa có nhãn -> nhãn của hạt giống gần nhất (distanceTransformWithLabels)."""
    seed = labels > 0
    todo = body & ~seed
    if not todo.any() or not seed.any():
        return labels
    inv = (~seed).astype(np.uint8)
    _, lbl = cv2.distanceTransformWithLabels(inv, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(seed)
    mp = np.zeros(int(lbl.max()) + 1, np.int32)
    mp[lbl[ys, xs]] = labels[ys, xs]
    out = labels.copy()
    out[todo] = mp[lbl[todo]]
    return out


def cat(k):
    inbox, con_p, manh, out_dir, kp = paths(k)
    os.makedirs(out_dir, exist_ok=True)
    kh = json.load(open(kp, encoding="utf-8"))
    X0, yw, f = kh["X0"], kh["y_water"], kh["f"]
    con = Image.open(con_p).convert("RGB")
    rgb = np.asarray(con)
    body, water = KH.concept_masks(con)
    body = body & ~water
    cls = KH.lab(con)
    cream = cls[..., 2] > 0
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(int)
    H_, W_ = body.shape
    yy, xx = np.mgrid[0:H_, 0:W_]
    toC = lambda p: (p[0] / f + X0, yw - (p[1] - HL.CLIPY) / f)
    order = ["a", "d", "k"] if k == 2 else ["k"]        # thứ tự vẽ cổ: sau -> trước (hai_long: HEADS[:2] sau, HEADS[2:] trước)
    meta = dict(X0=X0, y_water=yw, f=f, pieces={}, heads={}, order=order)
    # ---- hạt giống
    corridors, heads_full = {}, {}
    for hid, h in kh["heads"].items():
        rh = kh["rig_heads"][hid]
        tr = [toC(p) for p in rh["rest"]]
        m = np.zeros(body.shape, np.uint8)
        th = int(round(rh.get("th_px") or 60))
        cv2.polylines(m, [np.int32(np.round(tr)).reshape(-1, 1, 2)], False, 1, thickness=max(30, int(th * 1.05)))
        corridors[hid] = (m > 0) & body
        heads_full[hid] = cv2.dilate(warp_alpha(os.path.join(manh, h["piece"] + ".png"), h["cx"], h["cy"], h["ang"], h["sc"], body.shape).astype(np.uint8),
                                     kdisk(9)).astype(bool) & body
    LBL = {}          # tên mảnh -> nhãn số
    labels = np.zeros(body.shape, np.int32)

    def seed(name, m):
        LBL[name] = len(LBL) + 1
        labels[m & (labels == 0)] = LBL[name]
        return m

    parts = {}         # tên -> dict(kind, hid, ...)
    for hid, h in kh["heads"].items():
        hf = heads_full[hid]
        gx, gy, w = h["gx"], h["gy"], h["w_px"]
        neck_below = corridors[hid] & (yy > gy + 0.10 * w)    # họng ngay dưới gáy vẫn là đầu (xoay theo đầu); cổ mọc thêm 32 px dưới đó
        # vùng đầu ứng viên = khung bao của mảnh đầu GPT nới xuống 0,22 w (mảnh GPT không có hàm dưới nên hàm, họng concept nằm ngoài hf)
        ys_, xs_ = np.nonzero(hf)
        box = np.zeros(body.shape, bool)
        box[int(ys_.min()):int(min(H_, ys_.max() + 0.22 * w)), int(max(0, xs_.min() - 4)):int(min(W_, xs_.max() + 0.05 * w))] = True
        head = (hf | box) & body & ~neck_below
        for h2 in kh["heads"]:
            if h2 != hid:
                head &= ~heads_full[h2] & ~corridors[h2]
        # hàm dưới: khe miệng = cụm hồng (lòng miệng) ở nửa trước đầu; đường chia = giữa khe theo từng cột, kéo thẳng ra mõm; bản lề =
        # mép sau của khe; sau bản lề đường chia chúc xuống 30° (cằm, họng theo hàm, má theo đầu)
        tipx = float(xx[head].max()) if head.any() else gx + w
        pink = (hsv[..., 2] > 120) & (hsv[..., 1] > 60) & ((hsv[..., 0] <= 16) | (hsv[..., 0] >= 170)) & head & (xx > gx + 0.22 * w) & (yy > gy - 0.02 * w)
        pink = cv2.morphologyEx(pink.astype(np.uint8), cv2.MORPH_CLOSE, kdisk(4)).astype(bool)
        if pink.any():
            pink = biggest(pink)
            cols = np.flatnonzero(pink.any(axis=0))
            hx = float(cols.min())
            mid = np.full(W_, np.nan)
            for cx_ in cols:
                rr = np.flatnonzero(pink[:, cx_])
                mid[cx_] = (rr.min() + rr.max()) / 2
            mid[cols.min():cols.max() + 1] = np.interp(np.arange(cols.min(), cols.max() + 1), cols, mid[cols])
            hy = float(mid[int(hx)])
            x_ar = np.arange(W_)
            line = np.where(x_ar < hx, hy + (hx - x_ar) * math.tan(math.radians(30)), np.where(x_ar <= cols.max(), mid, mid[cols.max()]))
            line = np.nan_to_num(line, nan=hy)
            jaw = head & (yy > line[None, :]) & (xx > hx - 0.22 * w) & (yy < hy + 0.3 * w)
        else:
            hx, hy = gx + 0.12 * w, gy + 0.02 * w
            line_y = hy + (xx - hx) / max(1.0, tipx - hx) * (-0.04 * w)
            jaw = head & (yy > line_y) & (xx > hx - 0.02 * w) & (yy < hy + 0.28 * w)
        jaw = cv2.morphologyEx(jaw.astype(np.uint8), cv2.MORPH_OPEN, K5).astype(bool)
        jaw = biggest(jaw) if jaw.any() else jaw
        # râu: sợi kem MỎNG, DÀI (dây) gần mõm, ngoài mảnh đầu GPT, ngoài hàm, ngoài mọi cổ (bụng cổ cũng màu kem: lỗi đã gặp);
        # vệt kem dính liền mép môi là môi, ở lại với đầu / hàm
        win = np.zeros(body.shape, bool)
        win[int(max(0, hy - 0.35 * w)):int(min(H_, hy + 0.45 * w)), int(max(0, tipx - 0.35 * w)):int(min(W_, tipx + 0.6 * w))] = True
        wm = cream & win & body & ~jaw
        for h2 in kh["heads"]:
            wm &= ~heads_full[h2] & ~corridors[h2]
        n, lab, st, cen = cv2.connectedComponentsWithStats(wm.astype(np.uint8), 8)
        comps = []
        for i in range(1, n):
            ar = st[i, cv2.CC_STAT_AREA]
            if ar < 80:
                continue
            c, ax, pmin, pmax = pca_axis(lab == i)
            ln = pmax - pmin
            if ln < 0.08 * w or ar / max(1.0, ln) > 0.07 * w:    # phải dài và mảnh
                continue
            comps.append((ar, i))
        comps = sorted(comps, reverse=True)[:2]
        tags = []
        for _, i in comps:
            reg = cv2.dilate((lab == i).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & body & ~hf
            c, ax, pmin, pmax = pca_axis(reg)
            p0, p1 = c + ax * pmin, c + ax * pmax
            root, tip = (p0, p1) if np.hypot(p0[0] - tipx, p0[1] - hy) < np.hypot(p1[0] - tipx, p1[1] - hy) else (p1, p0)
            tags.append((cen[i][1], reg, root, tip))
        tags.sort(key=lambda t: t[0])
        whisk_all = np.zeros(body.shape, bool)
        for (_, reg, root, tip), tag in zip(tags, ("f", "b") if len(tags) == 2 else ("f",)):
            nm = f"lai_whisk_{hid}{tag}"
            seed(nm, reg)
            whisk_all |= reg
            parts[nm] = dict(kind="whisker", hid=hid, tag=tag, root=[float(root[0]), float(root[1])], tip=[float(tip[0]), float(tip[1])])
        head_only = head & ~jaw & ~whisk_all
        seed(f"lai_head_{hid}", head_only)
        parts[f"lai_head_{hid}"] = dict(kind="head", hid=hid, hole=jaw)
        if jaw.any():
            seed(f"lai_jaw_{hid}", jaw)
            parts[f"lai_jaw_{hid}"] = dict(kind="jaw", hid=hid, hinge=[float(hx), float(hy)])
        meta["heads"][hid] = dict(tipx=tipx, hx=float(hx), hy=float(hy), pink=int(pink.sum()))
    for hid in order:
        reg = corridors[hid]
        for h2 in kh["heads"]:
            reg = reg & ~heads_full[h2]
        seed(f"lai_neck_{hid}", reg)
        parts[f"lai_neck_{hid}"] = dict(kind="neck", hid=hid)
    for pname in ("tail", "coil"):
        p = kh.get("parts", {}).get(pname)
        if not p or (pname == "coil" and k == 1):
            continue
        m = warp_alpha(os.path.join(manh, pname + ".png"), p["cx"], p["cy"], p["ang"], p["sc"], body.shape)
        m = cv2.dilate(m.astype(np.uint8), kdisk(7)).astype(bool) & body & (labels == 0)
        if not m.any():
            continue
        m = biggest(m)
        seed(f"lai_{pname}", m)
        parts[f"lai_{pname}"] = dict(kind=pname)
    # ---- điểm thân còn lại -> nhãn gần nhất (bóng dáng khung 0 = concept); mẩu rời < 1500 px của đầu/hàm/cổ gán lại cho mảnh kề.
    # Dải 70 px trên mặt nước không gán thêm: bọt sóng, nét mực sóng lẫn vào mặt nạ thân sẽ thành vệt treo dưới cổ khi cổ nhấc (lỗi đã gặp)
    body_fill = body & ~((yy > yw - 70) & (labels == 0))
    labels = nearest_fill(labels, body_fill)
    for nm, p in parts.items():
        if p["kind"] in ("head", "jaw", "neck", "tail", "coil"):
            m = labels == LBL[nm]
            n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
            if n > 2:
                big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
                for i in range(1, n):
                    if i != big and st[i, cv2.CC_STAT_AREA] < 1500:
                        labels[lab == i] = 0
    labels = nearest_fill(labels, body_fill)
    labels[yy > yw + 30] = 0          # dưới mặt nước 30 px trở xuống: mặt nạ cắt che, không cần cắt (viền sóng lẫn vào thân)
    regions = {nm: labels == LBL[nm] for nm in parts}
    for nm, p in parts.items():      # râu là dây mỏng: phần thân gán nhầm (cách trục sợi > 14 px) trả về đầu
        if p["kind"] == "whisker":
            c, ax, _, _ = pca_axis(regions[nm])
            nrm = np.array([-ax[1], ax[0]])
            d = np.abs((np.stack([xx, yy], -1) - c) @ nrm)
            bad = regions[nm] & (d > 14)
            regions[nm] &= ~bad
            regions[f"lai_head_{p['hid']}"] |= bad
    # ---- cắt từng mảnh (lớp dưới mọc thêm dưới lớp trên và dưới mặt nước)
    layer_above = {}
    # lớp trên để cổ mọc thêm: đầu + râu, KHÔNG gồm hàm dưới (hàm há ra thì phần cổ mọc dưới hàm lộ thành mảng lạ dưới cằm: lỗi đã gặp;
    # khe há đã có lòng miệng bám đầu che)
    allheads = np.zeros(body.shape, bool)
    for nm, p in parts.items():
        if p["kind"] in ("head", "whisker"):
            allheads |= regions[nm]
    for i, hid in enumerate(order):
        above = allheads.copy()
        for h2 in order[i + 1:]:
            above |= regions[f"lai_neck_{h2}"]
        layer_above[f"lai_neck_{hid}"] = above | water
    for pname in ("lai_tail", "lai_coil"):
        if pname in parts:
            layer_above[pname] = water | allheads
    body_top = int(np.nonzero(body.any(axis=1))[0].min())
    meta["height_rig"] = round(HL.CLIPY + (yw - body_top) * f, 1)
    for nm, p in parts.items():
        reg = regions[nm]
        if not reg.any():
            continue
        grow = None
        if nm in layer_above:
            grow = cv2.dilate(reg.astype(np.uint8), kdisk(GROW)).astype(bool) & layer_above[nm] & ~reg
            if p["kind"] == "neck":   # cổ chỉ mọc TRONG hành lang của mình (+4 px): nối tiếp hình cổ vào sọ, không thành dải rộng dưới cả đầu
                grow &= cv2.dilate(corridors[p["hid"]].astype(np.uint8), kdisk(4)).astype(bool)
                # dưới đầu chỉ mọc tới ngang gáy + 0,1 w (dưới sọ), không mọc dưới cằm / mõm: hàm há thì phần mọc dưới cằm lộ thành mảng
                # màu lạ (lỗi đã gặp); chỗ nối gáy vẫn kín khi đầu xoay
                hh = kh["heads"][p["hid"]]
                grow &= ~(allheads & (yy > hh["gy"] + 0.10 * hh["w_px"]))
        if p["kind"] == "jaw":
            # hàm to hơn lỗ 1 px (viền không hở); KHÔNG mọc thêm lên đầu: hàm vẽ trên lòng miệng, dải mọc thêm lộ thành vệt sẫm khi há
            reg = cv2.dilate(reg.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & body
            grow = None
        im, org = crop_piece(rgb, reg, grow=grow)
        im.save(os.path.join(out_dir, nm + ".png"))
        meta["pieces"][nm] = dict(org=org, w=im.width, h=im.height, **{k2: v for k2, v in p.items() if k2 != "hole"})
        if p["kind"] == "head" and p["hole"].any():
            # lòng miệng: mảng hồng phẳng đúng vùng hàm (nới 3 px lên đầu để không hở khe khi há)
            hx_, hy_ = parts[f"lai_jaw_{p['hid']}"]["hinge"]
            w_ = kh["heads"][p["hid"]]["w_px"]
            hole = cv2.dilate(p["hole"].astype(np.uint8), kdisk(3)).astype(bool) & (regions[nm] | p["hole"])
            hole &= (xx > hx_ - 0.03 * w_) & (yy < hy_ + 0.26 * w_)     # khe miệng + cằm (vệt râu dưới cằm không tô hồng); hụt thì há lộ cổ sau lỗ hàm
            ys, xs = np.nonzero(hole)
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            sub = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
            sub[..., :3] = FLESH
            sub[..., 3] = hole[y0:y1, x0:x1] * 255
            Image.fromarray(sub, "RGBA").save(os.path.join(out_dir, f"lai_mouth_{p['hid']}.png"))
            meta["pieces"][f"lai_mouth_{p['hid']}"] = dict(org=(int(x0), int(y0)), w=int(x1 - x0), h=int(y1 - y0), kind="mouth", hid=p["hid"])
        if p["kind"] in ("tail", "coil"):
            c, ax, pmin, pmax = pca_axis(regions[nm])
            if ax[0] < 0:
                ax, pmin, pmax = -ax, -pmax, -pmin
            meta["pieces"][nm].update(base=[float(c[0] + ax[0] * pmin), float(c[1] + ax[1] * pmin)],
                                      tip=[float(c[0] + ax[0] * pmax), float(c[1] + ax[1] * pmax)])
    cover = np.zeros(body.shape, bool)
    for nm in regions:
        cover |= regions[nm]
    miss = body & ~cover & (yy <= yw - 70)
    meta["phu"] = round(1 - miss.sum() / max(1, body.sum()), 4)
    json.dump(meta, open(os.path.join(out_dir, "lai.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # tờ soi: nhãn màu trên concept + từng mảnh
    pal = np.random.RandomState(3).randint(60, 255, (len(LBL) + 1, 3)).astype(np.uint8)
    lab_im = rgb.copy()
    mk = labels > 0
    lab_im[mk] = (0.45 * rgb[mk] + 0.55 * pal[labels[mk]]).astype(np.uint8)
    lab_im[miss] = (255, 0, 255)
    sheet = Image.new("RGB", (1800, 2600), (120, 124, 132))
    d = ImageDraw.Draw(sheet)
    L = Image.fromarray(lab_im)
    L.thumbnail((1780, 700))
    sheet.paste(L, (10, 20))
    d.text((10, 4), f"nhãn mảnh trên concept (tím = thân không mảnh nào nhận, phủ {meta['phu']:.3f})", fill=(255, 255, 255))
    x, y, row = 10, L.height + 40, 0
    for nm in sorted(meta["pieces"]):
        im = Image.open(os.path.join(out_dir, nm + ".png"))
        im.thumbnail((440, 280))
        if x + im.width + 10 > 1800:
            x, y, row = 10, y + row + 26, 0
        sheet.paste(im, (x, y + 16), im)
        d.text((x, y), nm, fill=(255, 255, 255))
        x += im.width + 14
        row = max(row, im.height + 16)
    sheet.crop((0, 0, 1800, min(2600, y + row + 20))).save(os.path.join(out_dir, "_soi.png"))
    print(f"{out_dir}: {len(meta['pieces'])} mảnh, phủ thân {meta['phu']:.3f}, đỉnh thân rig y={meta['height_rig']}")
    return meta


# ---------------------------------------------------------------- gắn vào rig (sau build_rig_form, trước nướng clip)
def _world(sk):
    return S.world_bones({"bones": sk.bones})


def _inv(Wb, p):
    """toạ độ thế giới -> cục bộ của xương (W = (wx, wy, a, b, c, d))."""
    wx, wy, a, b, c, d = Wb
    det = a * d - b * c
    x, y = p[0] - wx, p[1] - wy
    return ((d * x - b * y) / det, (-c * x + a * y) / det)


def _bind(Wb):
    wx, wy, a, b, c, d = Wb
    return (wx, wy, math.degrees(math.atan2(c, a)), math.hypot(a, c))


def _rot(Wb):
    return math.degrees(math.atan2(Wb[4], Wb[2]))


def _scl(Wb):
    return math.hypot(Wb[2], Wb[4])


def _set_att(sk, slot, name):
    for s in sk.slots:
        if s["name"] == slot:
            s["attachment"] = name


def _mesh(sk, slot, name, im, P_fn, weights_fn, binds, pc, H_rig):
    """lưới vùng dày (bước theo chiều cao con) trên ảnh mảnh im; P_fn(px, py) -> thế giới; weights_fn(P) -> [(xương, w)]."""
    L = QL.luoi_vung(im, buoc_theo_cao=H_rig, in_tk=False)
    pts = [(float(p[0]), float(p[1])) for p in L.pts]
    P = [P_fn(px, py) for px, py in pts]
    wts = [weights_fn(p) for p in P]
    tris = [tuple(int(v) for v in t) for t in L.tris]
    pc[name] = im
    sk.atts[slot] = {}
    sk.mesh(slot, name, im, pts, tris, wts, (P, binds), name=name)
    sk.atts[slot][name]["hull"] = int(L.nh)
    _set_att(sk, slot, name)
    return len(pts), len(tris)


def chain_proj_weights(J, n):
    """trọng số B-spline theo tham số dọc chuỗi: chiếu điểm thế giới lên đường gấp khúc khớp J (n+1 điểm)."""
    J = np.asarray(J, float)
    segs = J[1:] - J[:-1]
    L2 = np.maximum(1e-6, (segs ** 2).sum(axis=1))
    Ls = np.sqrt(L2)
    cum = np.concatenate([[0.0], np.cumsum(Ls)])
    seg = float(cum[-1] / n)

    def fn(p):
        p = np.asarray(p, float)
        best = None
        for i in range(len(segs)):
            t = float(np.clip(((p - J[i]) @ segs[i]) / L2[i], 0, 1))
            q = J[i] + segs[i] * t
            d = float(np.hypot(*(p - q)))
            if best is None or d < best[0]:
                best = (d, cum[i] + t * Ls[i])
        return HL.chain_weights(best[1], seg, n)
    return fn


def pieces_of(lai_dir):
    return sorted(json.load(open(os.path.join(lai_dir, "lai.json"), encoding="utf-8"))["pieces"])


def load_piece(lai_dir, nm):
    """ảnh mảnh cắt, phóng về tỉ lệ rig (f của dạng) và bleed màu mép; dùng cả khi gộp rig dạng sau (merge_next)."""
    f = json.load(open(os.path.join(lai_dir, "lai.json"), encoding="utf-8"))["f"]
    im = Image.open(os.path.join(lai_dir, nm + ".png")).convert("RGBA")
    im = im.resize((max(2, round(im.width * f)), max(2, round(im.height * f))), Image.LANCZOS)
    return HL.bleed(im)


def apply_lai(sk, pc, info, k, C):
    inbox, con_p, manh, out_dir, kp = paths(k)
    meta = json.load(open(os.path.join(out_dir, "lai.json"), encoding="utf-8"))
    X0, yw, f = meta["X0"], meta["y_water"], meta["f"]
    toR = lambda x, y: ((x - X0) * f, HL.CLIPY + (yw - y) * f)
    H_rig = float(meta["height_rig"])
    W = _world(sk)
    tot = [0, 0]

    def load(nm):
        return load_piece(out_dir, nm)

    def P_of(nm):
        ox, oy = meta["pieces"][nm]["org"]
        rx, ry = toR(ox, oy)
        return lambda px, py: (rx + px, ry - py)

    def add(slot, nm, im, wfn, binds):
        nv, nt = _mesh(sk, slot, nm, im, P_of(nm), wfn, binds, pc, H_rig)
        tot[0] += nv
        tot[1] += nt

    for hid in info["heads"]:
        Hh = info["heads"][hid]
        kind = Hh["kind"]
        hb, jb = "h" + hid, "j" + hid
        # ---- đầu: bám xương đầu; bờm (sau gáy, trên) chia dần cho hai đốt bờm b<hid>0/1 để vẫn phất
        nm = f"lai_head_{hid}"
        if nm in meta["pieces"]:
            im = load(nm)
            b0n, b1n = f"b{hid}0", f"b{hid}1"
            bx0 = sk.bones[sk.bi[b0n]].get("x", 0.0)
            ML = sk.bones[sk.bi[b0n]].get("length", 40.0)
            hw = Hh["hw"]

            def wh_(p, hb=hb, bx0=bx0, ML=ML, hw=hw, b0n=b0n, b1n=b1n, Wh=W[hb]):
                lx, ly = _inv(Wh, p)
                m = HL.ease((bx0 - lx) / (0.18 * hw), "io") * HL.ease((ly + 0.05 * hw) / (0.14 * hw), "io")
                tip = HL.ease((bx0 - ML - lx) / (0.18 * hw), "io")
                return [(hb, 1 - m), (b0n, m * (1 - tip)), (b1n, m * tip)]
            add(hb, nm, im, wh_, {hb: _bind(W[hb]), b0n: _bind(W[b0n]), b1n: _bind(W[b1n])})
            # mí mắt dò lại trên đầu concept
            lid = pc["lid_" + kind]
            HL._LID.pop(kind, None)
            lcx, lcy, lrot, lsc = HL.fit_lid(kind, im, lid)
            ox, oy = meta["pieces"][nm]["org"]
            rx, ry = toR(ox, oy)
            lx, ly = _inv(W[hb], (rx + lcx, ry - lcy))
            sk.atts["e" + hid] = {}
            sk.region("e" + hid, "lid_" + kind, lid, lx, ly, lrot - _rot(W[hb]), lsc / _scl(W[hb]), lsc / _scl(W[hb]))
            # xương miệng ở mõm concept
            mh = meta["heads"][hid]
            mx, my = _inv(W[hb], toR(mh["tipx"] - 8, mh["hy"] - 6))
            bm = sk.bones[sk.bi["mieng_" + hid]]
            bm["x"], bm["y"] = round(mx, 2), round(my, 2)
        # ---- xương hàm dời tới bản lề concept TRƯỚC (lòng miệng, hàm đều bind theo W[jb] mới; bind theo W cũ rồi dời xương thì lưới bị kéo lệch)
        nm = f"lai_jaw_{hid}"
        if nm in meta["pieces"]:
            hx, hy = meta["pieces"][nm]["hinge"]
            jl = _inv(W[hb], toR(hx, hy))
            bj = sk.bones[sk.bi[jb]]
            bj["x"], bj["y"] = round(jl[0], 2), round(jl[1], 2)
            bj["scaleX"] = bj["scaleY"] = 1.0
            bj["rotation"] = 0.0
            W = _world(sk)
        # ---- lòng miệng: mảng hồng đúng vùng hàm, bám đầu (hàng dưới theo hàm 0,55 để không lòi dưới cằm)
        nm = f"lai_mouth_{hid}"
        if nm in meta["pieces"]:
            im = load(nm)
            pm = meta["pieces"][nm]
            oy_top = toR(0, pm["org"][1])[1]
            hgt = pm["h"] * f

            def wm_(p, hb=hb, jb=jb, top=oy_top, hgt=hgt):
                v = min(1.0, max(0.0, (top - p[1]) / max(1.0, hgt)))
                wj = 0.55 * v * v
                return [(hb, 1 - wj), (jb, wj)]
            add("m" + hid, nm, im, wm_, {hb: _bind(W[hb]), jb: _bind(W[jb])})
        # ---- hàm: vùng hàm concept, xương hàm dời tới bản lề (tỉ lệ 1), họng sát bản lề theo đầu
        nm = f"lai_jaw_{hid}"
        if nm in meta["pieces"]:
            im = load(nm)
            hx, hy = meta["pieces"][nm]["hinge"]
            hr = toR(hx, hy)
            jlen = im.width

            def wj_(p, hr=hr, jlen=jlen, hb=hb, jb=jb):
                d = math.hypot(p[0] - hr[0], p[1] - hr[1])
                wh = min(0.85, 0.9 * max(0.0, 1 - d / (0.33 * jlen)))
                return [(hb, wh), (jb, 1 - wh)]
            add(jb, nm, im, wj_, {hb: _bind(W[hb]), jb: _bind(W[jb])})
            ln0 = sk.bones[sk.bi[f"l{hid}0"]]       # lưỡi: gốc ở giữa hàm concept
            ln0["x"], ln0["y"] = round(jlen * 0.45 / _scl(W[jb]), 2), round(-im.height * 0.35 / _scl(W[jb]), 2)
        # ---- cổ: lưới vùng trên hình cắt, trọng số chiếu lên chuỗi n<hid>*; dải GPT (slot c<hid>) ở dưới làm đoạn chìm
        nm = f"lai_neck_{hid}"
        if nm in meta["pieces"]:
            im = load(nm)
            names = Hh["names"]
            J = [W[n][:2] for n in names]
            segW = math.hypot(J[1][0] - J[0][0], J[1][1] - J[0][1])
            a_, c_ = W[names[-1]][2], W[names[-1]][4]
            h_ = math.hypot(a_, c_)
            J.append((J[-1][0] + a_ / h_ * segW, J[-1][1] + c_ / h_ * segW))
            wraw = chain_proj_weights(J, HL.NB)
            wfn = lambda p, wraw=wraw, names=names: [(names[i], w) for i, w in wraw(p)]
            slot = "cc" + hid
            sn = [s["name"] for s in sk.slots]
            if slot not in sn:
                sk.slots.insert(sn.index("c" + hid) + 1, {"name": slot, "bone": names[0], "attachment": nm})
            add(slot, nm, im, wfn, {n: _bind(W[n]) for n in names})
            # dải cổ GPT (slot c<hid>, nằm dưới cổ concept) chỉ giữ 55 % phía chân (đoạn chìm + nối): phần gần đầu lộ ra thành mảng
            # sẫm dưới hàm khi há miệng / đầu ngửa (lỗi đã gặp). Lưới dải như hai_long.head(): hệ dọc chuỗi, bind (i·seg, 0, 0).
            neck = pc["neck_" + kind]
            nmc = "neck_" + kind + "_c"
            cw = int(neck.width * 0.55)
            if nmc not in pc:
                pc[nmc] = neck.crop((0, 0, cw, neck.height))
            segp = neck.width / HL.NB
            pts, tris, axis, _ = HL.strip_mesh(pc[nmc], max(2, round(HL.NB * 0.55)))
            Pc = [(px, (axis - py) * HL.NECK_THICK[kind] * Hh.get("thick", 1.0)) for px, py in pts]
            wc = [[(names[b], w) for b, w in HL.chain_weights(px, segp, HL.NB)] for px, _ in pts]
            sk.atts["c" + hid] = {}
            sk.mesh("c" + hid, nmc, pc[nmc], pts, tris, wc, (Pc, {names[i]: (i * segp, 0, 0) for i in range(HL.NB)}))
            _set_att(sk, "c" + hid, nmc)
        # ---- râu: chuỗi r<hid><tag>* đặt dọc trục sợi concept, dây mềm của hai_long chạy trên đó
        for tag in ("f", "b"):
            nm = f"lai_whisk_{hid}{tag}"
            slot = f"r{hid}{tag}"
            if nm not in meta["pieces"]:
                for s in sk.slots:
                    if s["name"] == slot:
                        s.pop("attachment", None)
                continue
            im = load(nm)
            pm = meta["pieces"][nm]
            root, tip = toR(*pm["root"]), toR(*pm["tip"])
            L_ = math.hypot(tip[0] - root[0], tip[1] - root[1])
            ang = math.degrees(math.atan2(tip[1] - root[1], tip[0] - root[0]))
            rn = [f"r{hid}{tag}{i}" for i in range(HL.WB)]
            rl = _inv(W[hb], root)
            b0 = sk.bones[sk.bi[rn[0]]]
            b0["x"], b0["y"], b0["rotation"] = round(rl[0], 2), round(rl[1], 2), round(ang - _rot(W[hb]), 2)
            b0["scaleX"] = b0["scaleY"] = 1.0
            wseg = L_ / HL.WB / _scl(W[hb])
            b0["length"] = round(wseg, 2)
            for i in range(1, HL.WB):
                bi_ = sk.bones[sk.bi[rn[i]]]
                bi_["x"], bi_["rotation"], bi_["length"] = round(wseg, 2), 0.0, round(wseg, 2)
                bi_.pop("y", None)
            W = _world(sk)
            Jw = [W[n][:2] for n in rn] + [tip]
            wraw = chain_proj_weights(Jw, HL.WB)
            wfn = lambda p, wraw=wraw, rn=rn: [(rn[i], w) for i, w in wraw(p)]
            add(slot, nm, im, wfn, {n: _bind(W[n]) for n in rn})
            # dây mềm (rope) của hai_long: gốc, góc nghỉ, dài đốt theo sợi mới
            Hh["wh"][tag] = (rl[0], rl[1], ang - _rot(W[hb]), (L_ / HL.WB) / max(1e-6, Hh["wseg"] * Hh["size"]))
    # ---- đuôi: chuỗi tail* dọc trục mảnh cắt (gốc = đầu trong, ngọn = vây)
    nm = "lai_tail"
    if nm in meta["pieces"]:
        im = load(nm)
        pm = meta["pieces"][nm]
        base, tip = toR(*pm["base"]), toR(*pm["tip"])
        L_ = math.hypot(tip[0] - base[0], tip[1] - base[1])
        ang = math.degrees(math.atan2(tip[1] - base[1], tip[0] - base[0]))
        tn = ["tail"] + [f"tail{i}" for i in range(1, HL.TB)]
        bt = sk.bones[sk.bi["tail"]]
        bl = _inv(W["than"], base)
        bt["x"], bt["y"], bt["rotation"] = round(bl[0], 2), round(bl[1], 2), round(ang - _rot(W["than"]), 2)
        bt["scaleX"] = bt["scaleY"] = 1.0
        tseg = L_ / HL.TB / _scl(W["than"])
        bt["length"] = round(tseg, 2)
        for i in range(1, HL.TB):
            bi_ = sk.bones[sk.bi[tn[i]]]
            bi_["x"], bi_["rotation"], bi_["length"] = round(tseg, 2), 0.0, round(tseg, 2)
        W = _world(sk)
        Jt = [W[n][:2] for n in tn] + [tip]
        wraw = chain_proj_weights(Jt, HL.TB)
        wfn = lambda p, wraw=wraw, tn=tn: [(tn[i], w) for i, w in wraw(p)]
        add("tail", nm, im, wfn, {n: _bind(W[n]) for n in tn})
    # ---- vòng thân: lưới vùng, trọng số Gauss về 5 điểm điều khiển coil0..4 (như hai_long) để chỗ phồng chạy dọc thân
    nm = "lai_coil"
    if nm in meta["pieces"] and not C.get("no_coil") and "coil" in sk.bi:
        im = load(nm)
        pm = meta["pieces"][nm]
        rx, ry = toR(*pm["org"])
        cx, cy = rx + im.width / 2, ry - im.height / 2
        bc = sk.bones[sk.bi["coil"]]
        cl = _inv(W["than"], (cx, cy))
        bc["x"], bc["y"], bc["rotation"] = round(cl[0], 2), round(cl[1], 2), 0.0
        bc["scaleX"] = bc["scaleY"] = 1.0
        cw = im.width
        for i, a in enumerate((172, 130, 90, 50, 8)):   # điểm điều khiển dọc vòm, theo cỡ vòng thân mới
            ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
            b = sk.bones[sk.bi[f"coil{i}"]]
            b["x"], b["y"] = round(ux * cw * 0.36, 2), round(-im.height * 0.5 + uy * im.height * 0.72, 2)
        W = _world(sk)
        cn = [f"coil{i}" for i in range(5)]

        def wc_(p, W=W, cn=cn, cw=cw):
            ws = [(n, math.exp(-((p[0] - W[n][0]) ** 2 + (p[1] - W[n][1]) ** 2) / (cw * 0.26) ** 2)) for n in cn]
            return ws + [("coil", 0.18)]
        add("coil", nm, im, wc_, {n: _bind(W[n]) for n in cn + ["coil"]})
    print(f"lai: {tot[0]} đỉnh, {tot[1]} tam giác lưới vùng từ hình concept (bước viền {0.015 * H_rig:.1f}, trong {0.02 * H_rig:.1f} px)")
    return meta


if __name__ == "__main__":
    cat(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
