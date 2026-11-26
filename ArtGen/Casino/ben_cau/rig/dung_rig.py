# Dựng rig cậu thám hiểm câu cá bằng AtomSpine (GD_Claude/32 mục 2). Đọc geo.json (chuan_bi.py, cat_phu.py), sinh atom/ops/01_rig.ops
# rồi chạy `atom do -f` trên project mới (init --force, chạy lại được).
# Toạ độ: ảnh nửa cỡ 512 x 768, gốc mặt đất (256, 709) giữa hai ủng; world = (px - 256, 709 - py), y lên, độ ngược kim.
# Khớp đọc ở tờ gốc cỡ đầy đủ (goc_rig.png 1024 x 1536) cho dễ soi, đổi sang nửa cỡ ở đây.
# Thứ tự vẽ (sau ra trước): cần câu, tay trái, tay phải, thân áo kem, chân, quần, ủng, áo choàng, đầu, chỏm tóc.
# Bản 3 (2026-11-26): tay cứng gắn ngực, không xương tay, không bàn tay (tờ gốc goc_tay_cam.png).
import os, sys, json, math, subprocess

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from atom_cli import CLI, run  # noqa: E402

PROJ = os.path.join(HERE, "atom")
ORDER = ["can_cau", "tay_t", "tay_p", "than", "chan_t", "chan_p", "quan", "ung_t", "ung_p", "ao_choang", "dau",
         "toc_chom"]
geo = json.load(open(os.path.join(HERE, "geo.json")))
CW, CH = geo["canvas"]
OX, OY = geo["origin"]
S = 0.5

# khớp ở tờ gốc cỡ đầy đủ
J = {
    "hip": (512, 1000), "bung": (512, 890), "nguc": (512, 760), "co": (512, 575), "dau": (512, 535), "dau_top": (512, 190),
    "chom": (452, 168), "chom_top": (505, 62),
    "vai_t": (330, 642), "khuyu_t": (262, 760), "co_tay_t": (226, 828), "nam_t_c": (222, 855),
    "vai_p": (692, 650), "khuyu_p": (748, 768), "co_tay_p": (768, 832), "nam_p_c": (752, 856),
    "hang_t": (400, 1060), "goi_t": (382, 1150), "co_chan_t": (350, 1250),
    "hang_p": (612, 1060), "goi_p": (622, 1150), "co_chan_p": (642, 1250),
    "cam": (608, 758),  # điểm cầm cần, trước ngực lệch phải (khuất sau áo choàng)
    "ao1": (512, 610), "ao2": (512, 770), "ao3": (512, 905), "ao_end": (512, 1040),
    "aot1": (418, 610), "aot2": (330, 805), "aot_end": (248, 985),
    "aop1": (606, 610), "aop2": (694, 805), "aop_end": (738, 985),
}


def W(name):
    x, y = J[name]
    return round(x * S - OX, 1), round(OY - y * S, 1)


def seg(a, b):
    (x0, y0), (x1, y1) = W(a), W(b)
    return x0, y0, round(math.degrees(math.atan2(y1 - y0, x1 - x0)), 2), round(math.hypot(x1 - x0, y1 - y0), 1)


def bone(name, parent, a, b=None, rot=None, ln=0):
    if b:
        x, y, r, l = seg(a, b)
    else:
        (x, y), r, l = W(a), rot or 0, ln
    return f"bone.add {name} parent={parent} x={x} y={y} rot={r} len={l} world=true"


def part(name, bone_name, mesh=False, slot=None):
    p = geo["parts"][name]
    s = f"part.add {name} path=images/{name}.png at={p['left']},{p['top']} canvas={CW},{CH} origin={OX},{OY} bone={bone_name}"
    if mesh:
        s += " mesh=true"
    if slot:
        s += f" slot={slot}"
    return s


def main():
    ops = ["project.set name=cau_ca fps=30"]
    # thân
    ops += [
        bone("move", "root", "hip", rot=0, ln=0).replace(f"x={W('hip')[0]} y={W('hip')[1]}", "x=0 y=0"),
        bone("hip", "move", "hip", "bung"),
        bone("bung", "hip", "bung", "nguc"),
        bone("nguc", "bung", "nguc", "co"),
        bone("co", "nguc", "co", "dau"),
        bone("dau", "co", "dau", "dau_top"),
        bone("chom", "dau", "chom", "chom_top"),
        # tay: không có xương (người dùng 2026-11-26: tay không cần animation), hai mảnh cứng gắn ngực
        # chân (IK, ủng gắn đích IK để đứng yên trên đất)
        bone("dui_t", "hip", "hang_t", "goi_t"), bone("ong_t", "dui_t", "goi_t", "co_chan_t"),
        bone("dui_p", "hip", "hang_p", "goi_p"), bone("ong_p", "dui_p", "goi_p", "co_chan_p"),
        bone("ik_chan_t", "move", "co_chan_t", rot=0, ln=0), bone("ik_chan_p", "move", "co_chan_p", rot=0, ln=0),
        # áo choàng: ba chuỗi
        bone("ao1", "nguc", "ao1", "ao2"), bone("ao2", "ao1", "ao2", "ao3"), bone("ao3", "ao2", "ao3", "ao_end"),
        bone("aot1", "nguc", "aot1", "aot2"), bone("aot2", "aot1", "aot2", "aot_end"),
        bone("aop1", "nguc", "aop1", "aop2"), bone("aop2", "aop1", "aop2", "aop_end"),
    ]
    # cần câu (người dùng 2026-11-26: "tay lỗi nhiều, không cần show tay cầm cần"): hai tay cầm cần ở phía trước người, khuất sau áo
    # choàng; cần gắn vào điểm cầm `cam` (con của ngực, trước ngực lệch phải), không gắn bàn tay. Setup: cần dựng đứng, chỗ cầm = 86,3%
    # chiều dài tính từ ngọn.
    rod = geo["extra"]["can_cau"]
    rw, rh = rod["w"], rod["h"]
    grip_r = 0.863 * rh
    gx, gy = J["cam"][0] * S, J["cam"][1] * S  # px nửa cỡ
    left, top = round(gx - rw / 2, 1), round(gy - grip_r, 1)
    wx, wy = round(gx - OX, 1), round(OY - gy, 1)
    seg_len = round(grip_r / 4, 1)
    ops += [
        f"bone.add cam parent=nguc x={wx} y={wy} rot=90 len=0 world=true",
        f"bone.add can1 parent=cam x=0 y=0 rot=0 len={seg_len}",
        f"bone.add can2 parent=can1 x={seg_len} y=0 rot=0 len={seg_len}",
        f"bone.add can3 parent=can2 x={seg_len} y=0 rot=0 len={seg_len}",
        f"bone.add can4 parent=can3 x={seg_len} y=0 rot=0 len={seg_len}",
        f"bone.add dau_can parent=can4 x={seg_len} y=0 rot=0 len=0",
        f"part.add can_cau path=images/can_cau.png at={left},{top} canvas={CW},{CH} origin={OX},{OY} bone=can1 mesh=true",
        "att.weights can_cau can_cau bones=can1,can2,can3,can4",
    ]
    # tay (sau thân), nắm tay
    ops += [
        part("tay_t", "nguc"),
        part("tay_p", "nguc"),
        part("than", "nguc"),
        part("chan_t", "dui_t", mesh=True), "att.weights chan_t chan_t bones=dui_t,ong_t",
        part("chan_p", "dui_p", mesh=True), "att.weights chan_p chan_p bones=dui_p,ong_p",
        part("quan", "hip", mesh=True), "att.weights quan quan bones=hip,dui_t,dui_p",
        part("ung_t", "ik_chan_t"), part("ung_p", "ik_chan_p"),
        part("ao_choang", "nguc", mesh=True),
        "att.weights ao_choang ao_choang bones=nguc,ao1,ao2,ao3,aot1,aot2,aop1,aop2",
        part("dau", "dau"),
        part("toc_chom", "chom"),
        "ik.add chan_t bones=dui_t,ong_t target=ik_chan_t bend=-",
        "ik.add chan_p bones=dui_p,ong_p target=ik_chan_p bend=+",
    ]
    # bàn tay thay, đầu quay: cùng tâm với hình gốc
    def centre(name):
        p = geo["parts"][name]
        return p["left"] + p["w"] / 2, p["top"] + p["h"] / 2
    for slot, alt in (("dau", "dau_quay"),):
        cx, cy = centre(slot)
        e = geo["extra"][alt]
        ops.append(f"part.add {alt}__{slot} path=images/{alt}.png at={round(cx - e['w'] / 2, 1)},{round(cy - e['h'] / 2 - 10, 1)} "
                   f"canvas={CW},{CH} origin={OX},{OY} bone=dau slot={slot}")
    ops += ["slot.set dau att=dau"]
    # thứ tự vẽ sau → trước (đặt lần lượt ra trước cùng)
    for s in ORDER:
        ops.append(f"slot.order {s} to=front")
    os.makedirs(os.path.join(PROJ, "ops"), exist_ok=True)
    path = os.path.join(PROJ, "ops", "01_rig.ops")
    open(path, "w", encoding="utf-8").write("\n".join(ops) + "\n")
    # project mới
    imgs = os.path.join(PROJ, "images")
    keep = sorted(os.listdir(imgs))
    run(CLI + ["init", PROJ, "--name", "cau_ca", "--force"])
    print(run(CLI + ["-p", PROJ, "do", "-f", path]))
    print(run(CLI + ["-p", PROJ, "q", "summary"]))


if __name__ == "__main__":
    main()
