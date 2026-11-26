# Dựng rig máy quả "Háu Ăn" trong AtomSpine. Đọc ../atom/geo.json (chuan_bi.py), sinh ../atom/ops/*.ops rồi chạy `atom do -f`.
# Toạ độ: px ảnh L1 (1024 x 1536) -> thế giới AtomSpine: x = px − 498, y = 1446 − py (y lên, gốc ở mặt đất giữa hai chân).
#
# Xương:
#   root > move > hip > tam > dau            ba khối thân chồng nhau: cản dưới (hip), tấm khung cuộn (tam), vòm đầu (dau);
#                                            nén giãn bằng DỜI khối trên dọc trục khối dưới, nghiêng bằng xoay ở hai chỗ nối
#   hip_d, tam_d, dau_d                      "xương da" (con của từng khối, cùng chỗ): lưới thân bám vào đây, phình / bẹp bằng tỉ lệ
#                                            mà không lây sang khối trên
#   tam_d > cuon                             mốc tâm ô cuộn (game vẽ hình cuộn theo ma trận xương này; trục x sang phải, y lên)
#   hip_d > mieng     dau_d > mat, may_t, may_p      miệng (6 hình), mắt (8 hình), hai nửa dải mày (xoay quanh đầu ngoài)
#   tam > can1 > can2 > can3 > num           cần gạt 3 đốt + núm (bàn tay Lão Mực bám xương num)
#   dau > lx1 > lx2 > lx3 > sao              lò xo ăng ten 3 đốt + ngôi sao
#   root > chan_t1..4, giay_t (và _p)        ống chân 4 đốt + giày: đặt theo toạ độ thế giới lúc nướng clip (chân ống cao su,
#                                            giày ghim đất)
# Mảnh (sau -> trước): can, lo_xo, sao, chan_t, chan_p, giay_t, giay_p, than (một lưới), den_a_d, den_a_h, den_b_d, den_b_h (đèn
#   sáng, mặc định ẩn), mieng, mat, may_t, may_p.
# Trọng số do script này tính: thân theo chiều cao (ba khối, hai dải hoà); ống chân, cần, lò xo chia kiểu B-spline bậc hai.
# Chạy: py -3 -I dung_rig.py   (dựng lại từ đầu; clip viết lại bằng hoat_anh.py)
#       py -3 -I dung_rig.py --luoi   (chỉ dựng lại lưới + trọng số từ ảnh hiện có, sau ve_vien.py; giữ xương, slot, clip)
import json, math, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
sys.path.insert(0, HERE)
from atom_cli import CLI  # noqa: E402
geo = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))
OX, OY = geo["origin"]
P = geo["parts"]

# ---- mốc (px ảnh) ----
Y_BOT, Y_HT, Y_TD = 1147, 960, 560           # đáy thân, chỗ nối hông - tấm, chỗ nối tấm - đầu
REEL_C = ((geo["reel"]["cols"][0][0] + geo["reel"]["cols"][2][1]) / 2, (geo["reel"]["top"] + geo["reel"]["bot"]) / 2)
MAT = (geo["mat"]["cx"], geo["mat"]["cy"])
MIENG = (geo["mieng"]["cx"], geo["mieng"]["top"])
MAY = {"t": (348, 392), "p": (664, 392)}     # đầu ngoài của mỗi nửa dải mày (trục xoay)
NUM = (geo["num"]["cx"], geo["num"]["cy"])
CAN_PIVOT_Y = 745
CAN_LO = geo["can_duoi"]
_f = (CAN_LO[1] - CAN_PIVOT_Y) / (CAN_LO[1] - NUM[1])
CAN_PIVOT = (CAN_LO[0] + (NUM[0] - CAN_LO[0]) * _f, CAN_PIVOT_Y)
LX = [(511, 300), (511, 255), (511, 210), (511, 168)]   # gốc lò xo (khuất sau bóng đèn đỉnh) ... chân ngôi sao
LEG_X = geo["leg_x"]
SOCKET_Y, ANKLE_Y = geo["socket_y"], geo["ankle_y"]
NLEG = 4
MOUTHS, EYES = 6, 8
DEN = ["den_a_d", "den_a_h", "den_b_d", "den_b_h"]


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
    L = ["project.set name=may_qua fps=30", "bone.add move parent=root x=0 y=0"]

    def add(name, parent, p, rot, ln):
        x, y = w(*p)
        L.append(f"bone.add {name} parent={parent} x={x:.1f} y={y:.1f} rot={rot:.2f} len={ln:.1f} world=true")

    cx = OX
    add("hip", "move", (cx, Y_BOT), 90, Y_BOT - Y_HT)
    add("hip_d", "hip", (cx, Y_BOT), 90, 60)
    add("tam", "hip", (cx, Y_HT), 90, Y_HT - Y_TD)
    add("tam_d", "tam", (cx, Y_HT), 90, 60)
    add("cuon", "tam_d", REEL_C, 0, 40)
    add("dau", "tam", (cx, Y_TD), 90, 325)
    add("dau_d", "dau", (cx, Y_TD), 90, 60)
    add("mat", "dau_d", MAT, 0, 40)
    add("may_t", "dau_d", MAY["t"], 0, 60)
    add("may_p", "dau_d", MAY["p"], 180, 60)
    add("mieng", "hip_d", MIENG, 0, 40)
    a = ang(CAN_PIVOT, NUM)
    seg = dist(CAN_PIVOT, NUM) / 3
    par = "tam"
    for k in range(3):
        p = (CAN_PIVOT[0] + (NUM[0] - CAN_PIVOT[0]) * k / 3, CAN_PIVOT[1] + (NUM[1] - CAN_PIVOT[1]) * k / 3)
        add(f"can{k + 1}", par, p, a, seg)
        par = f"can{k + 1}"
    add("num", par, NUM, a, 30)
    par = "dau"
    for k in range(3):
        add(f"lx{k + 1}", par, LX[k], 90, dist(LX[k], LX[k + 1]))
        par = f"lx{k + 1}"
    add("sao", par, LX[3], 90, 60)
    seg = (ANKLE_Y - SOCKET_Y) / NLEG
    for s in ("t", "p"):
        par = "root"
        for k in range(NLEG):
            add(f"chan_{s}{k + 1}", par, (LEG_X[s], SOCKET_Y + seg * k), -90, seg)
            par = f"chan_{s}{k + 1}"
        add(f"giay_{s}", "root", (LEG_X[s], ANKLE_Y), 0, 60)
    return L


def parts_ops():
    L = []
    cv = f"canvas=1024,1536 origin={OX},{OY}"

    def pa(name, bone, slot=None, left=None, top=None):
        L.append(f"part.add {name} path=images/{name}.png at={left if left is not None else P[name]['left']},"
                 f"{top if top is not None else P[name]['top']} {cv} bone={bone}" + (f" slot={slot}" if slot else ""))

    pa("can", "can1")
    pa("lo_xo", "lx1")
    pa("sao", "sao")
    for s in ("t", "p"):
        pa(f"chan_{s}", f"chan_{s}1")
    for s in ("t", "p"):
        pa(f"giay_{s}", f"giay_{s}")
    pa("than", "hip_d")
    for n in DEN:
        pa(n, "dau_d" if n.endswith("_d") else "hip_d")
    for i in range(1, MOUTHS + 1):
        n = f"mieng_{i:02d}"
        pa(n, "mieng", slot="mieng", left=round(MIENG[0] - P[n]["w"] / 2), top=round(MIENG[1]))
    for i in range(1, EYES + 1):
        n = f"mat_{i:02d}"
        pa(n, "mat", slot="mat", left=round(MAT[0] - P[n]["w"] / 2), top=round(MAT[1] - P[n]["h"] / 2))
    pa("may_t", "may_t")
    pa("may_p", "may_p")
    L.append("att.mesh than than from=than edge=18 inner=34 maxVerts=1300")
    L.append("att.mesh can can from=can edge=10 inner=16")
    L.append("att.mesh lo_xo lo_xo from=lo_xo edge=8 inner=12")
    for s in ("t", "p"):
        L.append(f"att.mesh chan_{s} chan_{s} from=chan_{s} edge=10 inner=14")
    L.append("slot.set mat att=mat_01")
    L.append("slot.set mieng att=mieng_01")
    for n in DEN:
        L.append(f"slot.set {n} color=FFFFFF00")   # đèn sáng ẩn sẵn; clip bật bằng alpha
    return L


# ---------------- trọng số ----------------
def sstep(a, b, v):
    t = max(0.0, min(1.0, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)


def bspline(u, n, last_full=False):
    """Trọng số B-spline bậc hai trên chuỗi n đốt tại tham số u (đơn vị đốt). Kẹp ở hai đầu. last_full: đốt cuối là đầu mút
    không có độ dài: tới u = n − 1 thì bám trọn nó."""
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


BLEND_HT = (975, 1015)   # dải hoà tấm -> hông (dưới thanh dưới của khung cuộn)
BLEND_TD = (500, 560)    # dải hoà đầu -> tấm (trên thanh trên của khung cuộn)


def w_body(x, y):
    if y >= BLEND_HT[1]:
        return {"hip_d": 1.0}
    if y >= BLEND_HT[0]:
        f = sstep(BLEND_HT[0], BLEND_HT[1], y)
        return {"tam_d": 1 - f, "hip_d": f}
    if y >= BLEND_TD[1]:
        return {"tam_d": 1.0}
    if y >= BLEND_TD[0]:
        f = sstep(BLEND_TD[0], BLEND_TD[1], y)
        return {"dau_d": 1 - f, "tam_d": f}
    return {"dau_d": 1.0}


def w_leg(x, y, s):
    seg = (ANKLE_Y - SOCKET_Y) / NLEG
    ws = bspline((y - SOCKET_Y) / seg, NLEG)
    return {f"chan_{s}{k + 1}": v for k, v in ws.items()}


def w_lever(x, y):
    if dist((x, y), NUM) < geo["num"]["r"] + 8:
        return {"num": 1.0}
    L3 = dist(CAN_PIVOT, NUM)
    ex, ey = (NUM[0] - CAN_PIVOT[0]) / L3, (NUM[1] - CAN_PIVOT[1]) / L3
    u = ((x - CAN_PIVOT[0]) * ex + (y - CAN_PIVOT[1]) * ey) / (L3 / 3)
    names = ["can1", "can2", "can3", "num"]
    return {names[k]: v for k, v in bspline(u, 4, last_full=True).items()}


def w_spring(x, y):
    u = (LX[0][1] - y) / (LX[0][1] - LX[1][1])
    names = ["lx1", "lx2", "lx3", "sao"]
    return {names[k]: v for k, v in bspline(u, 4, last_full=True).items()}


def weights_ops(slot, name, bind, pts, fn):
    """Ops đặt trọng số: bám cứng `bind`, rồi từng bước set (đỉnh, xương, w) gom theo (bước, xương, w)."""
    L = [f"att.bind {slot} {name} bone={bind}"]
    steps = {}
    worst = 0
    for i, (x, y) in enumerate(pts):
        ws = fn(x, y)
        tot = sum(ws.values())
        ws = {b: round(v / tot * 40) / 40 for b, v in ws.items()}
        ws = {b: v for b, v in ws.items() if v > 0}
        tot = sum(ws.values())
        order = sorted(((b, v / tot) for b, v in ws.items()), key=lambda kv: -kv[1])[:4]
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


def setup_px(slot):
    """Đỉnh lưới của mảnh `slot` ở dáng gốc, đổi về px ảnh (lưới chưa có trọng số: verts nằm trong hệ xương của slot)."""
    proj = json.load(open(os.path.join(ATOM, "atomspine.json"), encoding="utf-8"))   # chỉ ĐỌC để lấy toạ độ đỉnh
    sl = next(s for s in proj["slots"] if s["name"] == slot)
    att = None
    for sk in proj["skins"]:
        for a in sk["atts"]:
            if a.get("slot") == slot and a.get("name") == slot:
                att = a
    verts = att["verts"]
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


def run(name, ops):
    path = os.path.join(ATOM, "ops", name + ".ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(ops) + "\n")
    out = atom("do", "-f", path)
    print(name, "|", out.splitlines()[-1][:160])


MESHES = (("than", "hip_d", w_body, "edge=18 inner=34 maxVerts=1300"), ("chan_t", "chan_t1", lambda x, y: w_leg(x, y, "t"), "edge=10 inner=14"),
          ("chan_p", "chan_p1", lambda x, y: w_leg(x, y, "p"), "edge=10 inner=14"), ("can", "can1", w_lever, "edge=10 inner=16"),
          ("lo_xo", "lx1", w_spring, "edge=8 inner=12"))


def remesh():
    """Dựng lại lưới + trọng số của các mảnh lưới từ ảnh hiện có (sau khi ve_vien.py vẽ viền: mép lưới phải ôm cả nét mực).
    Xương, slot, clip giữ nguyên."""
    cv = f"canvas=1024,1536 origin={OX},{OY}"
    L = []
    for slot, bind, fn, opt in MESHES:
        L.append(f"part.add {slot} path=images/{slot}.png at={P[slot]['left']},{P[slot]['top']} {cv} bone={bind}")
        L.append(f"att.mesh {slot} {slot} from={slot} {opt}")
    run("04_luoi_lai", L)
    L = []
    for slot, bind, fn, opt in MESHES:
        pts = setup_px(slot)
        ops, worst = weights_ops(slot, slot, bind, pts, fn)
        print(f"  {slot}: {len(pts)} đỉnh, tối đa {worst} xương / đỉnh")
        L += ops
    run("03_trong_so", L)
    print(atom("q", "summary"))


def main():
    if "--luoi" in sys.argv:
        remesh()
        return
    for f in ("atomspine.json",):
        p = os.path.join(ATOM, f)
        if os.path.exists(p):
            os.remove(p)
    atom("init", ATOM, "--name", "may_qua", "--force", check=False)
    os.makedirs(os.path.join(ATOM, "ops"), exist_ok=True)
    run("01_xuong", bones_ops())
    run("02_manh", parts_ops())
    L = []
    for slot, bind, fn in (("than", "hip_d", w_body), ("chan_t", "chan_t1", lambda x, y: w_leg(x, y, "t")),
                           ("chan_p", "chan_p1", lambda x, y: w_leg(x, y, "p")), ("can", "can1", w_lever), ("lo_xo", "lx1", w_spring)):
        pts = setup_px(slot)
        ops, worst = weights_ops(slot, slot, bind, pts, fn)
        print(f"  {slot}: {len(pts)} đỉnh, {len(ops)} ops, tối đa {worst} xương / đỉnh")
        L += ops
    run("03_trong_so", L)
    print(atom("q", "summary"))
    print(atom("lint", check=False)[-600:])


if __name__ == "__main__":
    main()
