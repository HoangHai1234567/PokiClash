# Dựng rig Lão Mực trong AtomSpine (GD_Claude/31 mốc D2). Đọc ../atom/geo.json (chuan_bi.py), sinh ../atom/ops/rig.ops rồi chạy
# `atom do -f`. Toạ độ: px ảnh L1 (1024 x 1536) -> thế giới AtomSpine: x = px − 512, y = 1460 − py (y lên, gốc giữa hai chân).
# Xương: root > move > hip > chest > neck > head (> chom1 > chom2, luoi, mat, mieng); hai chuỗi tay 8 đốt từ chest (tay_t1..8,
# tay_p1..8) + bàn tay (tay_tb, tay_pb); hai chân dui > ong > ban. Mảnh: than (một lưới, trọng số theo thân / đầu / chân),
# luoi_trai (cứng, xương luoi), tay_trai / tay_phai (dải lưới, trọng số dọc chuỗi), mat (10 hình), mieng (10 hình),
# ban_tay_trai / ban_tay_phai (10 hình mỗi bên; bên phải là ảnh lật ngang).
# Chạy: py -3 -I dung_rig.py [--rebuild]   (--rebuild: xoá atomspine.json cũ, dựng lại từ đầu)
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


def w(px, py):
    return px - OX, OY - py


def ang(a, b):
    return math.degrees(math.atan2(-(b[1] - a[1]), b[0] - a[0]))


def atom(*args, check=True):
    r = subprocess.run(CLI + list(args) + ["-p", ATOM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        print(out)
        raise SystemExit(f"atom {' '.join(args[:2])} lỗi")
    return out


def bones_ops():
    L = []
    add = lambda name, parent, px, py, rot, ln: L.append(
        f"bone.add {name} parent={parent} x={w(px, py)[0]:.1f} y={w(px, py)[1]:.1f} rot={rot:.2f} len={ln:.1f} world=true")
    L.append("project.set name=lao_muc fps=30")
    L.append("bone.add move parent=root x=0 y=0")
    add("hip", "move", *J["hong"], 90, 240)
    add("chest", "hip", *J["nguc"], 90, 180)
    add("neck", "chest", *J["co"], 90, 15)
    add("head", "neck", *J["dau"], 90, 330)
    add("chom1", "head", *J["chom1"], ang(J["chom1"], J["chom2"]), 95)
    add("chom2", "chom1", *J["chom2"], ang(J["chom2"], J["chom3"]), 55)
    add("luoi", "head", *J["luoi_trai"], 0, 120)
    add("mat", "head", *J["mat"], 0, 40)
    add("mieng", "head", *J["mieng"], 0, 40)
    for s, n in (("t", "trai"), ("p", "phai")):
        add(f"dui_{s}", "hip", *J[f"dui_{n}"], ang(J[f"dui_{n}"], J[f"goi_{n}"]), 140)
        add(f"ong_{s}", f"dui_{s}", *J[f"goi_{n}"], ang(J[f"goi_{n}"], J[f"co_chan_{n}"]), 150)
        add(f"ban_{s}", f"ong_{s}", *J[f"co_chan_{n}"], ang(J[f"co_chan_{n}"], J[f"ban_chan_{n}"]), 70)
        # chuỗi tay: 8 đốt đều từ vai tới cổ tay
        S, E = J[f"vai_{n}"], J[f"co_tay_{n}"]
        a = ang(S, E)
        seg = math.hypot(E[0] - S[0], E[1] - S[1]) / NSEG
        parent = "chest"
        for k in range(NSEG):
            px = S[0] + (E[0] - S[0]) * k / NSEG
            py = S[1] + (E[1] - S[1]) * k / NSEG
            add(f"tay_{s}{k + 1}", parent, px, py, a, seg)
            parent = f"tay_{s}{k + 1}"
        add(f"tay_{s}b", parent, *E, a, 60)
    return L


def parts_ops():
    L = []
    cv = f"canvas=1024,1536 origin={OX},{OY}"
    pa = lambda name, bone, mesh=False, slot=None, left=None, top=None: L.append(
        f"part.add {name} path=images/{name}.png at={left if left is not None else P[name]['left']},{top if top is not None else P[name]['top']} "
        f"{cv} bone={bone}" + (f" slot={slot}" if slot else "") + (" mesh=true" if mesh else ""))
    pa("than", "hip")
    # mắt, miệng: tâm ở mốc mắt / miệng
    for kind, slot, bone in (("mat", "mat", "mat"), ("mieng", "mieng", "mieng")):
        cx, cy = J[kind]
        for i in range(1, 11):
            n = f"{kind}_{i:02d}"
            pa(n, bone, slot=slot, left=round(cx - P[n]["w"] / 2), top=round(cy - P[n]["h"] / 2))
    pa("luoi_trai", "luoi")
    pa("tay_trai", "tay_t1")
    pa("tay_phai", "tay_p1")
    # bàn tay: att.region trong hệ xương bàn tay; gốc cổ tay của ảnh đặt ở gốc xương, hướng ảnh theo trục xương
    for i in range(1, 11):
        L.append(f"image.add tay_{i:02d} path=images/tay_{i:02d}.png")
    for s, n, flip in (("t", "trai", False), ("p", "phai", True)):
        slot = f"ban_tay_{n}"
        L.append(f"slot.add {slot} bone=tay_{s}b")
        for i in range(1, 11):
            nm = f"tay_{i:02d}"
            g = P[nm]
            dx, dy = g["huong"]
            vx, vy = g["goc"][0] - g["w"] / 2, g["goc"][1] - g["h"] / 2  # gốc so với tâm, ảnh y xuống
            if flip:
                dx, vx = -dx, -vx
            phi = math.atan2(-dy, dx)  # hướng ảnh (y lên)
            rot = -phi
            # vectơ gốc trong hệ y lên, quay theo rot
            ux, uy = vx, -vy
            c, s_ = math.cos(rot), math.sin(rot)
            rx, ry = c * ux - s_ * uy, s_ * ux + c * uy
            x, y = -rx - 6, -ry  # lùi 6 px cho cổ tay đen chồng lên đầu dải tay
            sx = -1 if flip else 1
            L.append(f"att.region {slot} {nm}_{s} image={nm} x={x:.1f} y={y:.1f} rot={math.degrees(rot):.2f} sx={sx}"
                     + (" use=true" if i == 1 else " use=false"))
    return L


def weights_ops():
    L = []
    L.append("att.mesh than than from=than edge=18 inner=34 maxVerts=1400")
    L.append("att.weights than than bones=hip,chest,neck,head,chom1,chom2,dui_t,ong_t,ban_t,dui_p,ong_p,ban_p mode=geodesic")
    for s, n in (("t", "trai"), ("p", "phai")):
        L.append(f"att.mesh tay_{n} tay_{n} from=tay_{n} edge=8 inner=10")
        L.append(f"att.weights tay_{n} tay_{n} bones=" + ",".join(f"tay_{s}{k}" for k in range(1, NSEG + 1)) + " mode=geodesic")
    # thứ tự vẽ (sau -> trước): thân, mắt, miệng, lưỡi trai, tay, bàn tay
    for sl in ("mat", "mieng", "luoi_trai", "tay_trai", "tay_phai", "ban_tay_trai", "ban_tay_phai"):
        L.append(f"slot.order {sl} to=front")
    L.append("slot.set mat att=mat_02")
    L.append("slot.set mieng att=mieng_01")
    return L


def main():
    if "--rebuild" in sys.argv:
        j = os.path.join(ATOM, "atomspine.json")
        if os.path.exists(j):
            os.remove(j)
        atom("init", ATOM, "--name", "lao_muc", "--force", check=False)
    os.makedirs(os.path.join(ATOM, "ops"), exist_ok=True)
    for name, ops in (("01_xuong", bones_ops()), ("02_manh", parts_ops()), ("03_trong_so", weights_ops())):
        path = os.path.join(ATOM, "ops", name + ".ops")
        open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
        print(name, atom("do", "-f", path).splitlines()[-1] if True else "")
    print(atom("q", "summary"))


if __name__ == "__main__":
    main()
