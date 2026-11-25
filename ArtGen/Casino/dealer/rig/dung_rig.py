# Dựng rig Lão Mực trong AtomSpine (GD_Claude/31 mốc D2, bản 2). Đọc ../atom/geo.json (chuan_bi.py), sinh ../atom/ops/*.ops rồi
# chạy `atom do -f`. Toạ độ: px ảnh L1 (1024 x 1536) -> thế giới AtomSpine: x = px − 512, y = 1460 − py (y lên, gốc giữa hai chân).
#
# Xương (65):
#   root > move > hip > bung > nguc > vai > neck > head          sống lưng 4 đốt: thân uốn chữ C / S, nén giãn bằng DỜI đốt
#   hip_d, bung_d, nguc_d, vai_d                                 "xương da" (con của từng đốt sống, cùng chỗ): lưới thân bám vào
#                                                                đây, phình / bẹp bằng tỉ lệ mà KHÔNG lây sang tay, đầu
#   head > chom1 > chom2 > chom3, mai, luoi > luoi2, mat, mieng  chỏm tóc 3 đốt, tóc mai, lưỡi trai 2 đốt (vành phất), mặt
#   vai > no > no_t, no_p                                        nơ + hai cánh nơ
#   vai > tay_t1..8 > tay_tb (bàn tay)                           ống tay 8 đốt; giãn dài bằng dời đốt con dọc trục cha
#   tay_t1d..9d                                                  xương da của ống tay (thon lại khi giãn: tỉ lệ ngang)
#   hip > dui_t > ong_t > ban_t (và _p)                          chân (bàn chân ghim đất bằng IK tính lúc nướng clip)
# Mảnh (sau -> trước): than (một lưới), mieng, mat, luoi_trai (lưới 2 xương), tay_trai, tay_phai (ống lưới), nit_trai, nit_phai
#   (nịt cứng trên đốt 4), no (lưới 3 xương, che gốc tay), ban_tay_trai, ban_tay_phai (12 hình mỗi bên; bên phải lật ngang).
# Trọng số do script này tính (không dùng tự động): dọc mỗi chuỗi chia kiểu B-spline bậc hai (giữa đốt 0,75 + 0,125 hai bên, ở
# khớp 0,5 / 0,5), không đỉnh nào bám cứng một đốt nên không gập ở khớp; đặt bằng chuỗi `att.weight ... mode=set`.
# Chạy: py -3 -I dung_rig.py   (dựng lại từ đầu; clip viết lại bằng hoat_anh.py)
import json, math, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
CLI = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
geo = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))
OX, OY = geo["origin"]
J = geo["J"]
P = geo["parts"]
NSEG = 8
NHAND = geo.get("n_hand", 10)   # 11 = bàn tay mở dựng đứng, 12 = nắm tay dựng nghiêng (nhìn từ phía mu, ngón cái ở trên)
SPINE = ["hip", "bung", "nguc", "vai"]
SPINE_Y = [J["hong"][1], J["bung"][1], J["nguc"][1], J["vai"][1], J["co"][1]]  # 1000, 900, 790, 680, 575


def w(px, py):
    return px - OX, OY - py


def ang(a, b):
    return math.degrees(math.atan2(-(b[1] - a[1]), b[0] - a[0]))


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def atom(*args, check=True):
    r = subprocess.run(CLI + list(args) + ["-p", ATOM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        print(out[-1500:])
        raise SystemExit(f"atom {' '.join(args[:2])} lỗi")
    return out


def bones_ops():
    L = []

    def add(name, parent, p, rot, ln):
        x, y = w(*p)
        L.append(f"bone.add {name} parent={parent} x={x:.1f} y={y:.1f} rot={rot:.2f} len={ln:.1f} world=true")

    L.append("project.set name=lao_muc fps=30")
    L.append("bone.add move parent=root x=0 y=0")
    add("hip", "move", J["hong"], 90, SPINE_Y[0] - SPINE_Y[1])
    add("bung", "hip", J["bung"], 90, SPINE_Y[1] - SPINE_Y[2])
    add("nguc", "bung", J["nguc"], 90, SPINE_Y[2] - SPINE_Y[3])
    add("vai", "nguc", J["vai"], 90, SPINE_Y[3] - SPINE_Y[4])
    for b, key in (("hip", "hong"), ("bung", "bung"), ("nguc", "nguc"), ("vai", "vai")):
        add(b + "_d", b, J[key], 90, 60)
    add("neck", "vai", J["co"], 90, 27)
    add("head", "neck", J["dau"], 90, J["dau"][1] - J["dinh_dau"][1])
    add("chom1", "head", J["chom1"], ang(J["chom1"], J["chom2"]), dist(J["chom1"], J["chom2"]))
    add("chom2", "chom1", J["chom2"], ang(J["chom2"], J["chom3"]), dist(J["chom2"], J["chom3"]))
    add("chom3", "chom2", J["chom3"], ang(J["chom3"], J["chom4"]), dist(J["chom3"], J["chom4"]))
    add("mai", "head", J["mai1"], ang(J["mai1"], J["mai2"]), dist(J["mai1"], J["mai2"]))
    add("luoi", "head", J["luoi"], ang(J["luoi"], J["luoi2"]), dist(J["luoi"], J["luoi2"]))
    add("luoi2", "luoi", J["luoi2"], ang(J["luoi2"], J["luoi3"]), dist(J["luoi2"], J["luoi3"]))
    add("mat", "head", J["mat"], 0, 40)
    add("mieng", "head", J["mieng"], 0, 40)
    add("no", "vai", J["no"], 0, 20)
    add("no_t", "no", J["no_t"], ang(J["no_t"], J["no_t2"]), dist(J["no_t"], J["no_t2"]))
    add("no_p", "no", J["no_p"], ang(J["no_p"], J["no_p2"]), dist(J["no_p"], J["no_p2"]))
    for s, n in (("t", "trai"), ("p", "phai")):
        add(f"dui_{s}", "hip", J[f"dui_{n}"], ang(J[f"dui_{n}"], J[f"goi_{n}"]), dist(J[f"dui_{n}"], J[f"goi_{n}"]))
        add(f"ong_{s}", f"dui_{s}", J[f"goi_{n}"], ang(J[f"goi_{n}"], J[f"co_chan_{n}"]), dist(J[f"goi_{n}"], J[f"co_chan_{n}"]))
        add(f"ban_{s}", f"ong_{s}", J[f"co_chan_{n}"], ang(J[f"co_chan_{n}"], J[f"ban_chan_{n}"]), 70)
        S, E = J[f"vai_{n}"], J[f"co_tay_{n}"]
        a = ang(S, E)
        seg = dist(S, E) / NSEG
        parent = "vai"
        for k in range(NSEG):
            p = (S[0] + (E[0] - S[0]) * k / NSEG, S[1] + (E[1] - S[1]) * k / NSEG)
            add(f"tay_{s}{k + 1}", parent, p, a, seg)
            add(f"tay_{s}{k + 1}d", f"tay_{s}{k + 1}", p, a, seg)
            parent = f"tay_{s}{k + 1}"
        add(f"tay_{s}9d", parent, E, a, 10)
        add(f"tay_{s}b", parent, E, a, 60)
    return L


def parts_ops():
    L = []
    cv = f"canvas=1024,1536 origin={OX},{OY}"

    def pa(name, bone, slot=None, left=None, top=None):
        L.append(f"part.add {name} path=images/{name}.png at={left if left is not None else P[name]['left']},"
                 f"{top if top is not None else P[name]['top']} {cv} bone={bone}" + (f" slot={slot}" if slot else ""))

    pa("than", "hip_d")
    for kind, bone in (("mat", "mat"), ("mieng", "mieng")):
        cx, cy = J[kind]
        for i in range(1, 11):
            n = f"{kind}_{i:02d}"
            pa(n, bone, slot=kind, left=round(cx - P[n]["w"] / 2), top=round(cy - P[n]["h"] / 2))
    pa("luoi_trai", "luoi")
    pa("tay_trai", "tay_t1d")
    pa("tay_phai", "tay_p1d")
    # nịt tay áo: đặt lại cho tâm nịt nằm trên trục ống tay mới (ống mới lệch trục ảnh gốc vài độ), giữ góc so với ống
    for s, n in (("t", "trai"), ("p", "phai")):
        S, E = J[f"vai_{n}"], J[f"co_tay_{n}"]
        L_arm = dist(S, E)
        ex, ey = (E[0] - S[0]) / L_arm, (E[1] - S[1]) / L_arm
        g = P[f"nit_{n}"]
        tx, ty = g["tam"]
        u = (tx - S[0]) * ex + (ty - S[1]) * ey             # chỗ nịt dọc ống (px)
        k = min(NSEG - 1, int(u / (L_arm / NSEG)))            # đốt mang nịt
        # trục tay ảnh gốc (đo): trái x = −0,576 y + c ; phải x = 0,569 y + c
        slope = -0.576 if s == "t" else 0.569
        th_o = math.degrees(math.atan2(-1.0, slope))         # góc trục gốc (y lên), chĩa xuống
        # tâm ảnh so với tâm nịt, đổi sang hệ trục gốc (dọc, ngang) rồi đặt vào hệ đốt
        icx, icy = g["left"] + g["w"] / 2, g["top"] + g["h"] / 2
        dx, dy = icx - tx, -(icy - ty)                       # y lên
        c, s_ = math.cos(math.radians(-th_o)), math.sin(math.radians(-th_o))
        lx, ly = c * dx - s_ * dy, s_ * dx + c * dy
        bx = u - k * (L_arm / NSEG) + lx
        L.append(f"image.add nit_{n} path=images/nit_{n}.png")
        L.append(f"slot.add nit_{n} bone=tay_{s}{k + 1}d")
        L.append(f"att.region nit_{n} nit_{n} image=nit_{n} x={bx:.1f} y={ly:.1f} rot={-th_o:.2f}")
    pa("no", "no")
    for i in range(1, NHAND + 1):
        L.append(f"image.add tay_{i:02d} path=images/tay_{i:02d}.png")
    for s, n, flip in (("t", "trai", False), ("p", "phai", True)):
        slot = f"ban_tay_{n}"
        L.append(f"slot.add {slot} bone=tay_{s}b")
        for i in range(1, NHAND + 1):
            nm = f"tay_{i:02d}"
            g = P[nm]
            dx, dy = g["huong"]
            vx, vy = g["goc"][0] - g["w"] / 2, g["goc"][1] - g["h"] / 2
            if flip:
                dx, vx = -dx, -vx
            phi = math.atan2(-dy, dx)
            rot = -phi
            ux, uy = vx, -vy
            c, s_ = math.cos(rot), math.sin(rot)
            rx, ry = c * ux - s_ * uy, s_ * ux + c * uy
            x, y = -rx - 8, -ry  # lùi 8 px cho cổ tay đen chồng lên đầu ống tay
            sx = -1 if flip else 1
            L.append(f"att.region {slot} {nm}_{s} image={nm} x={x:.1f} y={y:.1f} rot={math.degrees(rot):.2f} sx={sx}"
                     + (" use=true" if i == 1 else " use=false"))
    L.append("att.mesh than than from=than edge=16 inner=30 maxVerts=1500")
    for n in ("trai", "phai"):
        L.append(f"att.mesh tay_{n} tay_{n} from=tay_{n} edge=9 inner=13")
    L.append("att.mesh no no from=no edge=10 inner=18")
    L.append("att.mesh luoi_trai luoi_trai from=luoi_trai edge=16 inner=30")
    # miệng vẽ DƯỚI mắt: lúc sốc (hàm rớt, mắt lồi) hai thứ chờm nhau thì mắt đè lên phần vòm miệng tối, không bị miệng cắt
    for sl in ("mieng", "mat", "luoi_trai", "tay_trai", "tay_phai", "nit_trai", "nit_phai", "no", "ban_tay_trai", "ban_tay_phai"):
        L.append(f"slot.order {sl} to=front")
    L.append("slot.set mat att=mat_02")
    L.append("slot.set mieng att=mieng_01")
    return L


# ---------------- trọng số ----------------
def sstep(a, b, v):
    t = max(0.0, min(1.0, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)


def bspline(u, n, last_full=False):
    """Trọng số B-spline bậc hai trên chuỗi n đốt tại tham số u (đơn vị đốt, 0..n). Trả {chỉ số đốt: w}. Kẹp ở hai đầu.
    last_full: đốt cuối (n−1) là 'đầu mút' không có độ dài (cổ tay): tới u = n−1 thì bám trọn nó."""
    u = max(0.0, min(float(n - (1 if last_full else 0)), u))
    i = min(n - 1, int(math.floor(u)))
    f = u - i
    if last_full and i >= n - 2:
        if i >= n - 1:
            return {n - 1: 1.0}
        w0, w2 = (1 - f) ** 2 / 2, f * f
        ws = {i - 1: w0, i: 1 - w0 - w2, i + 1: w2}
    else:
        ws = {i - 1: (1 - f) ** 2 / 2, i: 0.5 + f - f * f, i + 1: f * f / 2}
    out = {}
    for k, v in ws.items():
        k = max(0, min(n - 1, k))
        out[k] = out.get(k, 0.0) + v
    return {k: v for k, v in out.items() if v > 1e-4}


def proj_chain(p, pts):
    """Chiếu điểm lên đường gấp khúc pts; trả tham số (chỉ số đoạn + phần lẻ, cho phép < 0 ở đầu và > n ở cuối) và khoảng cách."""
    best = (1e18, 0.0)
    n = len(pts) - 1
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2
        lo = -1.0 if i == 0 else 0.0
        hi = 2.0 if i == n - 1 else 1.0
        t = max(lo, min(hi, t))
        q = (a[0] + dx * t, a[1] + dy * t)
        d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
        if d < best[0]:
            best = (d, i + t)
    return best[1], math.sqrt(best[0])


def w_body(x, y):
    """Trọng số một đỉnh lưới thân tại px ảnh (x, y)."""
    HCx, HCy, HR = geo["dau_tron"]
    out = {}

    def add(b, v):
        if v > 1e-4:
            out[b] = out.get(b, 0.0) + v

    if y < 600 and not (y > 535 and abs(x - 512) > 120):
        # ----- đầu, tóc -----
        w_head_zone = 1.0 - sstep(540, 596, y)           # cổ: pha dần sang đốt vai
        r = math.hypot(x - HCx, y - HCy)
        hw = {}
        outside = r - (HR - 6)
        if outside > 0 and y < 300 and x < 610:
            # chỏm tóc: chuỗi chom1..3, gốc là đầu
            pts = [J["chom1"], J["chom2"], J["chom3"], J["chom4"]]
            u, _ = proj_chain((x, y), pts)
            ws = bspline(u + 1.0, 4)                      # chỉ số 0 = đầu, 1..3 = chom1..3
            names = ["head", "chom1", "chom2", "chom3"]
            # độ "thuộc chỏm" tính theo độ cao trên mép đai lưỡi trai (đai chạy chéo từ (305, 250) tới (645, 160)): gốc chỏm
            # và phần đỉnh đầu bên phải dưới móc xoăn vẫn theo đầu, không thì chúng vung theo ngọn chỏm thành một cái gai
            band_y = 250.0 - 0.265 * (x - 305.0)
            k_in = sstep(4.0, 62.0, band_y - y)
            for k, v in ws.items():
                hw[names[k]] = hw.get(names[k], 0) + v * k_in
            hw["head"] = hw.get("head", 0) + (1 - k_in)
        elif outside > 0 and x < 345 and y >= 300:
            a, b = J["mai1"], J["mai2"]
            L = dist(a, b)
            f = ((x - a[0]) * (b[0] - a[0]) + (y - a[1]) * (b[1] - a[1])) / (L * L)
            wm = sstep(-0.45, 0.55, f)
            hw["mai"] = wm
            hw["head"] = 1 - wm
        else:
            hw["head"] = 1.0
        for b, v in hw.items():
            add(b, v * w_head_zone)
        rest = 1.0 - w_head_zone
        if rest > 1e-4:
            add("vai_d", rest)
        return out
    # ----- thân + chân -----
    side = "t" if x < 512 else "p"
    m_leg = sstep(1004, 1078, y) * sstep(38, 72, abs(x - 512))
    if y > 1090:
        m_leg = 1.0
    if m_leg > 1e-4:
        yk, ya = J["goi_trai"][1], J["co_chan_trai"][1]   # 1170, 1320
        if y < yk - 45:
            lw = {"dui": 1.0}
        elif y < yk + 45:
            f = sstep(yk - 45, yk + 45, y)
            lw = {"dui": 1 - f, "ong": f}
        elif y < ya - 22:
            lw = {"ong": 1.0}
        elif y < ya + 14:
            f = sstep(ya - 22, ya + 14, y)
            lw = {"ong": 1 - f, "ban": f}
        else:
            lw = {"ban": 1.0}
        for b, v in lw.items():
            add(f"{b}_{side}", v * m_leg)
    m_torso = 1.0 - m_leg
    if m_torso > 1e-4:
        ys = SPINE_Y
        if y >= ys[0]:
            ws = {0: 1.0}
        else:
            i = 0
            while i < 3 and y < ys[i + 1]:
                i += 1
            f = (ys[i] - y) / (ys[i] - ys[i + 1])
            ws = bspline(i + min(1.0, f), 4)
        for k, v in ws.items():
            add(SPINE[k] + "_d", v * m_torso)
    return out


def w_arm(x, y, s, n):
    S, E = J[f"vai_{n}"], J[f"co_tay_{n}"]
    L_arm = dist(S, E)
    ex, ey = (E[0] - S[0]) / L_arm, (E[1] - S[1]) / L_arm
    u = ((x - S[0]) * ex + (y - S[1]) * ey) / (L_arm / NSEG)
    ws = bspline(u, NSEG + 1, last_full=True)
    return {f"tay_{s}{k + 1}d": v for k, v in ws.items()}


def w_bow(x, y):
    cx = J["no"][0]
    d = x - cx
    wt = sstep(8, 46, -d)
    wp = sstep(8, 46, d)
    out = {"no": 1 - wt - wp}
    if wt > 1e-4:
        out["no_t"] = wt
    if wp > 1e-4:
        out["no_p"] = wp
    return {k: v for k, v in out.items() if v > 1e-4}


def w_visor(x, y):
    f = sstep(J["luoi2"][0] - 70, J["luoi2"][0] + 60, x)
    return {k: v for k, v in (("luoi", 1 - f), ("luoi2", f)) if v > 1e-4}


def mesh_points(slot, name):
    """Toạ độ px ảnh của các đỉnh lưới (dáng gốc)."""
    j = json.loads(atom("q", f"att {slot} {name} full", "--json"))
    a = j.get("att") or j.get("full") or j
    if "verts" not in a:
        for v in j.values():
            if isinstance(v, dict) and "verts" in v:
                a = v
                break
    verts = a["verts"]
    bone = json.loads(atom("q", "slot " + slot, "--json"))
    return a, verts, bone


def weights_ops(slot, name, bind, pts, fn):
    """Ops đặt trọng số: bám cứng `bind`, rồi từng bước set (đỉnh, xương, w) gom theo (bước, xương, w)."""
    L = [f"att.bind {slot} {name} bone={bind}"]
    steps = {}
    worst = 0
    for i, (x, y) in enumerate(pts):
        ws = fn(x, y)
        tot = sum(ws.values())
        ws = {b: round(v / tot * 40) / 40 for b, v in ws.items()}   # lượng tử 0,025
        ws = {b: v for b, v in ws.items() if v > 0}
        tot = sum(ws.values())
        ws = {b: v / tot for b, v in ws.items()}
        order = sorted(ws.items(), key=lambda kv: -kv[1])[:4]
        tot = sum(v for _, v in order)
        order = [(b, v / tot) for b, v in order]
        worst = max(worst, len(order))
        acc = 0.0
        for k, (b, v) in enumerate(order):
            acc += v
            val = 1.0 if k == 0 else v / acc
            if k == 0 and b == bind:
                continue
            steps.setdefault((k, b, round(val, 4)), []).append(i)
    for (k, b, val), idx in sorted(steps.items(), key=lambda kv: kv[0][0]):
        for c in range(0, len(idx), 120):
            L.append(f"att.weight {slot} {name} bone={b} w={val} i={','.join(map(str, idx[c:c + 120]))} mode=set")
    return L, worst


def run(name, ops):
    path = os.path.join(ATOM, "ops", name + ".ops")
    open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
    out = atom("do", "-f", path)
    print(name, "|", out.splitlines()[-1][:160])


def main():
    atom("init", ATOM, "--name", "lao_muc", "--force", check=False)
    os.makedirs(os.path.join(ATOM, "ops"), exist_ok=True)
    run("01_xuong", bones_ops())
    run("02_manh", parts_ops())
    # đỉnh lưới (thế giới, dáng gốc) -> px ảnh
    L = []
    for slot, bind, fn in (("than", "hip_d", w_body), ("tay_trai", "tay_t1d", lambda x, y: w_arm(x, y, "t", "trai")),
                           ("tay_phai", "tay_p1d", lambda x, y: w_arm(x, y, "p", "phai")), ("no", "no", w_bow),
                           ("luoi_trai", "luoi", w_visor)):
        pts = setup_px(slot)
        ops, worst = weights_ops(slot, slot, bind, pts, fn)
        print(f"  {slot}: {len(pts)} đỉnh, {len(ops)} ops, tối đa {worst} xương / đỉnh")
        L += ops
    run("03_trong_so", L)
    print(atom("q", "summary"))
    print(atom("lint", check=False)[-600:])


def setup_px(slot):
    """Đỉnh lưới của mảnh `slot` ở dáng gốc, đổi về px ảnh. Lưới chưa có trọng số: verts nằm trong hệ xương của slot."""
    proj = json.load(open(os.path.join(ATOM, "atomspine.json"), encoding="utf-8"))   # chỉ ĐỌC để lấy toạ độ đỉnh
    sl = next(s for s in proj["slots"] if s["name"] == slot)
    att = None
    for sk in proj["skins"]:
        for a in sk["atts"]:
            if a.get("slot") == slot and a.get("name") == slot:
                att = a
    verts = att["verts"]
    # ma trận thế giới dáng gốc của xương slot
    bones = {b["name"]: b for b in proj["bones"]}

    def world(name):
        b = bones[name]
        r = math.radians(b["rot"])
        c, s = math.cos(r), math.sin(r)
        m = (c * b.get("sx", 1), -s * b.get("sy", 1), b["x"], s * b.get("sx", 1), c * b.get("sy", 1), b["y"])
        if b["parent"] is None:
            return m
        p = world(b["parent"])
        return (p[0] * m[0] + p[1] * m[3], p[0] * m[1] + p[1] * m[4], p[0] * m[2] + p[1] * m[5] + p[2],
                p[3] * m[0] + p[4] * m[3], p[3] * m[1] + p[4] * m[4], p[3] * m[2] + p[4] * m[5] + p[5])

    m = world(sl["bone"])
    pts = []
    for i in range(0, len(verts), 2):
        x, y = verts[i], verts[i + 1]
        wx, wy = m[0] * x + m[1] * y + m[2], m[3] * x + m[4] * y + m[5]
        pts.append((wx + OX, OY - wy))
    return pts


if __name__ == "__main__":
    main()
