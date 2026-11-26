# Vẽ viền mực cho máy quả "Háu Ăn" SAU khi animation đã chốt (luật rig của dự án: gen không viền -> rig -> clip -> viền sau cùng).
# Viền là nét bút nâu sẫm hơi rung, vẽ bằng `paint.stroke` vào lớp `vien` của từng ảnh mảnh trong Paint của AtomSpine (sửa lại được
# trong Studio), rồi flatten. Chỉ vẽ ở mép NHÌN THẤY:
#   than        viền ngoài + ranh giữa các mảng màu (khung cuộn, vành đèn, bảng hai bên, cản dưới)
#   mieng_*     viền ngoài (vành môi)                    mat_*      đã có vành mắt, không vẽ thêm
#   may_t / _p  viền ngoài, trừ đầu chờm qua giữa (hai nửa chồng nhau ở đó)
#   sao         viền ngoài                               lo_xo      dây lò xo vốn sẫm, không viền
#   can         viền ngoài, trừ đoạn đuôi khuất sau thân  giay_*     viền ngoài
#   chan_*      hai mép dọc ống (hai đầu ống khuất trong thân và trong cổ giày)
#   den_*       vành từng bóng đèn (lớp đèn sáng phủ lên vành của thân)
# Ảnh sạch (chưa viền) giữ ở ../atom/images_khong_vien/ (chụp lần đầu chạy); mỗi lần chạy trả ảnh sạch rồi vẽ lại từ đầu.
# chuan_bi.py chạy lại thì xoá thư mục đó + các .ora rồi chạy lại script này.
# Chạy: py -3 -I ve_vien.py --xem   (chỉ dựng ảnh xem thử soi/vien_xem.png, không đụng project)
#       py -3 -I ve_vien.py         (vẽ vào project AtomSpine)
import glob, json, math, os, shutil, subprocess, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
IMG = os.path.join(ATOM, "images")
CLEAN = os.path.join(ATOM, "images_khong_vien")
sys.path.insert(0, HERE)
from atom_cli import CLI  # noqa: E402
geo = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))
P = geo["parts"]
INK = "2B2118FF"
W_OUT, W_IN, W_SMALL = 6, 4, 5      # px ảnh: viền ngoài thân, ranh trong thân, mảnh nhỏ (máy hiện ở tỉ lệ ~0,9)
rng = np.random.default_rng(7)


def load(name):
    src = os.path.join(CLEAN if os.path.isdir(CLEAN) and os.path.exists(os.path.join(CLEAN, name + ".png")) else IMG, name + ".png")
    return np.asarray(Image.open(src).convert("RGBA")).astype(np.float32)


def wobble(pts, closed, step=7.0, amp=0.8):
    """Lấy mẫu lại đường gấp khúc mỗi `step` px và cho rung nhẹ theo pháp tuyến (nét bút tay)."""
    pts = np.asarray(pts, np.float32)
    if closed:
        pts = np.vstack([pts, pts[:1]])
    seg = np.hypot(*(pts[1:] - pts[:-1]).T)
    L = float(seg.sum())
    if L < step * 2:
        return [tuple(p) for p in pts]
    n = max(4, int(L / step))
    acc = np.concatenate([[0], np.cumsum(seg)])
    out = []
    ph = rng.uniform(0, 6.28, 3)
    for i in range(n + (0 if closed else 1)):
        s = L * i / n
        k = min(len(seg) - 1, int(np.searchsorted(acc, s, side="right") - 1))
        f = (s - acc[k]) / max(seg[k], 1e-6)
        p = pts[k] + (pts[k + 1] - pts[k]) * f
        d = pts[k + 1] - pts[k]
        nrm = np.array([-d[1], d[0]]) / max(np.hypot(*d), 1e-6)
        w = amp * (0.6 * math.sin(s / 23.0 + ph[0]) + 0.4 * math.sin(s / 9.0 + ph[1]) + 0.3 * math.sin(s / 61.0 + ph[2]))
        out.append((float(p[0] + nrm[0] * w), float(p[1] + nrm[1] * w)))
    if closed:
        out.append(out[0])
    return out


def contours(mask, min_len=40):
    cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        if cv2.arcLength(c, True) < min_len:
            continue
        c = cv2.approxPolyDP(c, 1.0, True)[:, 0, :].astype(np.float32)
        if len(c) >= 3:
            out.append(c)
    return out


def split_keep(poly, keep):
    """Cắt đường khép kín thành các đoạn chỉ gồm điểm keep(x, y) == True."""
    runs, cur = [], []
    for p in poly:
        if keep(p[0], p[1]):
            cur.append(p)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def body_regions(a):
    """Bản đồ nhãn mảng màu của thân (ảnh đã làm mờ cho mất vân chì): k-means 6 màu, bỏ mẩu nhỏ, mọi điểm của thân có đúng một nhãn
    (điểm của mẩu bị bỏ nhập vào mảng gần nhất) nên mỗi ranh chỉ là MỘT đường."""
    al = a[..., 3] > 128
    rgb = cv2.medianBlur(a[..., :3].astype(np.uint8), 11)
    rgb = cv2.bilateralFilter(rgb, 9, 60, 9)
    px = rgb[al].astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0)
    cv2.setRNGSeed(3)
    _, lab, cen = cv2.kmeans(px, 6, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    L = np.full(al.shape, -1, np.int32)
    L[al] = lab[:, 0]
    Lf = np.full(al.shape, -1, np.int32)
    el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    for k in range(len(cen)):
        m = cv2.morphologyEx((L == k).astype(np.uint8), cv2.MORPH_OPEN, el)
        n, cc, st, _ = cv2.connectedComponentsWithStats(m, 8)
        for i in range(1, n):
            if st[i, 4] >= 260:
                Lf[(cc == i) & (Lf < 0)] = k
    k3 = np.ones((3, 3), np.uint8)
    for _ in range(60):                     # điểm chưa có nhãn nhận nhãn của mảng gần nhất
        todo = al & (Lf < 0)
        if not todo.any():
            break
        for k in range(len(cen)):
            grow = cv2.dilate((Lf == k).astype(np.uint8), k3) > 0
            Lf[grow & todo & (Lf < 0)] = k
    return Lf, len(cen)


def strokes_for(name):
    """Danh sách (điểm, bề dày) của viền cho ảnh `name` (toạ độ px ảnh mảnh)."""
    a = load(name)
    al = a[..., 3]
    h, w = al.shape
    mask = al > 128
    left, top = P.get(name, {}).get("left", 0), P.get(name, {}).get("top", 0)
    S = []
    if name == "lo_xo" or name.startswith("mat_"):
        return S
    if name == "than":
        for c in contours(mask):
            S.append((wobble(c, True), W_OUT))
        Lf, nk = body_regions(a)
        inner = cv2.erode(mask.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0   # ranh trong: bỏ phần trùng viền ngoài
        big = cv2.dilate(Lf.astype(np.float32), np.ones((5, 5), np.uint8))          # nhãn lớn nhất trong ô 5 x 5

        def keep_in(k):
            # mỗi ranh chỉ vẽ một lần: mảng k vẽ đoạn giáp mảng có nhãn lớn hơn
            return lambda x, y: inner[min(h - 1, int(y)), min(w - 1, int(x))] and big[min(h - 1, int(y)), min(w - 1, int(x))] > k
        for k in range(nk):
            for c in contours(Lf == k, 60):
                idx = next((i for i, q in enumerate(c) if not keep_in(k)(q[0], q[1])), 0)
                c2 = np.vstack([c[idx:], c[:idx]])
                for run in split_keep(c2, keep_in(k)):
                    if len(run) >= 4:
                        S.append((wobble(run, False, amp=0.6), W_IN))
        return S
    if name.startswith("den_"):
        for c in contours(mask, 30):
            S.append((wobble(c, True, step=5, amp=0.4), W_IN))
        return S
    keep = None
    if name in ("may_t", "may_p"):
        xc = geo["may"]["xc"] - left
        keep = (lambda x, y: x < xc - 4) if name == "may_t" else (lambda x, y: x > xc + 4)
    elif name == "can":
        ycut = 745 + 26 - top          # dưới trục cần 26 px là khuất sau thân / bệ cần
        keep = lambda x, y: y < ycut
    elif name.startswith("chan_"):
        r = geo["leg_w"] / 2
        keep = lambda x, y: r * 0.9 < y < h - r * 0.9
    for c in contours(mask):
        if keep is None:
            S.append((wobble(c, True), W_SMALL))
        else:
            # xoay điểm đầu về chỗ bị loại để mỗi đoạn giữ được liền mạch
            idx = next((i for i, p in enumerate(c) if not keep(p[0], p[1])), 0)
            c2 = np.vstack([c[idx:], c[:idx]])
            for run in split_keep(c2, keep):
                S.append((wobble(run, False), W_SMALL))
    return S


def names():
    return sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(IMG, "*.png")))


def preview():
    from ghep_thu import geo as g2  # noqa: F401
    tiles = []
    for n in names():
        a = load(n)
        im = Image.fromarray(a.astype(np.uint8))
        big = Image.new("RGBA", (im.width + 12, im.height + 12), (0, 0, 0, 0))
        big.alpha_composite(im, (6, 6))
        d = ImageDraw.Draw(big)
        for pts, wd in strokes_for(n):
            d.line([(x + 6, y + 6) for x, y in pts], fill=(43, 33, 24, 255), width=wd, joint="curve")
        tiles.append((n, big))
    os.makedirs(os.path.join(HERE, "soi", "vien"), exist_ok=True)
    for n, t in tiles:
        t.save(os.path.join(HERE, "soi", "vien", n + ".png"))
    # ghép cả con (dáng nghỉ) trên nền kem
    cv = Image.new("RGBA", (1024 + 12, 1536 + 12), (243, 233, 214, 255))
    T = dict(tiles)

    def put(n, left=None, top=None):
        cv.alpha_composite(T[n], (int(P[n]["left"] if left is None else left), int(P[n]["top"] if top is None else top)))
    for n in ("can", "lo_xo", "sao", "chan_t", "chan_p", "giay_t", "giay_p", "than"):
        put(n)
    m = T["mieng_01"]
    put("mieng_01", geo["mieng"]["cx"] - (m.width - 12) / 2, geo["mieng"]["top"])
    e = T["mat_01"]
    put("mat_01", geo["mat"]["cx"] - (e.width - 12) / 2, geo["mat"]["cy"] - (e.height - 12) / 2)
    put("may_t")
    put("may_p")
    cv.convert("RGB").save(os.path.join(HERE, "soi", "vien_xem.png"))
    print("xem:", os.path.join(HERE, "soi", "vien_xem.png"))


def atom(*args, check=True):
    r = subprocess.run(CLI + list(args) + ["-p", ATOM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        print(out[-1500:])
        raise SystemExit(f"atom {' '.join(args[:2])} lỗi")
    return out


def apply():
    ns = names()
    if not os.path.isdir(CLEAN):
        os.makedirs(CLEAN)
        for n in ns:
            shutil.copy(os.path.join(IMG, n + ".png"), os.path.join(CLEAN, n + ".png"))
    for n in ns:      # trả ảnh sạch, bỏ tài liệu lớp cũ
        shutil.copy(os.path.join(CLEAN, n + ".png"), os.path.join(IMG, n + ".png"))
        ora = os.path.join(IMG, n + ".ora")
        if os.path.exists(ora):
            os.remove(ora)
    L = []
    total = 0
    for n in ns:
        S = strokes_for(n)
        if not S:
            continue
        L.append(f"paint.open {n}")
        L.append(f"paint.layer add {n} name=vien")
        for pts, wd in S:
            L.append(f"paint.stroke {n} layer=vien pts=" + ",".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" size={wd} color={INK} hard=1 cap=round")
            total += 1
        L.append(f"paint.flatten {n}")
    path = os.path.join(ATOM, "ops", "20_vien.ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(atom("paint", "-f", path)[-300:], "|", total, "nét")


if __name__ == "__main__":
    if "--xem" in sys.argv:
        preview()
    else:
        apply()
