# D3 phần hai (GD_Claude/31): thêm vào project rig ĐANG CÓ (không dựng lại cả rig)
#   * 7 lá bài xoè `xao_1..7` (xương con của root, slot vẽ trên ống tay, dưới bàn tay; hình lưng bài la_bai) cho clip shuffle;
#   * 2 giọt mồ hôi `mo_hoi_1..2` (xương con của head ở hai thái dương, slot vẽ trên mắt, dưới lưỡi trai) cho clip deal_self_tense.
# Giọt mồ hôi vẽ bằng mã: giọt nước tô phẳng xanh nhạt, viền nâu sẫm (nét như ảnh mẫu), không điểm sáng, không bóng (luật hình).
# Cùng các lệnh dung_rig.py đã có cho lần dựng lại từ đầu. Chạy lại được (đã có thì bỏ qua phần thêm).
# Chạy: py -3 -I them_d3b.py   rồi   py -3 -I hoat_anh.py
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dong_co import atom, ATOM  # noqa: E402
from dung_rig import XAO_N, MO_HOI  # noqa: E402


def draw_drop(path, w=34, h=48, k=4):
    W, H = w * k, h * k
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = W * 0.40
    cx, cy = W / 2, H - r - 3 * k
    # cung tròn phía dưới (toạ độ ảnh: y xuống), hai đầu vuốt lên thành đỉnh nhọn
    tip = (cx, 3 * k)
    shape = [tip]
    for i in range(0, 181, 3):          # cung dưới từ phải sang trái
        a = math.radians(-20 + i * (220 / 180))
        shape.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    shape.append(tip)
    ink = (59, 40, 30, 255)
    d.polygon(shape, fill=(150, 205, 236, 255))
    d.line(shape, fill=ink, width=int(2.6 * k), joint="curve")
    # vân chì nhẹ (chỉ là vân, không mảng sáng tối)
    rnd = random.Random(7)
    tex = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tex)
    for _ in range(40):
        x = rnd.uniform(0, W)
        y = rnd.uniform(0, H)
        td.line([(x, y), (x + 9 * k, y - 5 * k)], fill=(120, 180, 220, 70), width=k)
    mask = im.split()[3].point(lambda v: 255 if v > 200 else 0)
    im.paste(Image.alpha_composite(im, tex), (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.line(shape, fill=ink, width=int(2.6 * k), joint="curve")
    im = im.resize((w, h), Image.LANCZOS)
    im.save(path)


draw_drop(os.path.join(ATOM, "images", "mo_hoi.png"))
have_b = atom("q", "bones", "--limit", "500", check=False)
have_s = atom("q", "slots", check=False)
names_b = {ln.split()[0] for ln in have_b.splitlines() if ln.strip()}
names_s = {ln.split()[1] for ln in have_s.splitlines() if len(ln.split()) > 1}
L = []
for i in range(1, XAO_N + 1):
    if f"xao_{i}" not in names_b:
        L.append(f"bone.add xao_{i} parent=root x=0 y=0 rot=0 len=20")
for i, (x, y) in enumerate(MO_HOI, 1):
    if f"mo_hoi_{i}" not in names_b:
        L.append(f"bone.add mo_hoi_{i} parent=head x={x} y={y} rot=0 len=20 world=true")
if "mo_hoi" not in atom("q", "images", check=False):
    L.append("image.add mo_hoi path=images/mo_hoi.png")
for i in range(1, XAO_N + 1):
    if f"xao_{i}" not in names_s:
        L.append(f"slot.add xao_{i} bone=xao_{i} at=before:ban_tay_trai")
    L.append(f"att.region xao_{i} la_xao image=la_bai x=0 y=0 rot=0 use=false")
for i in range(1, len(MO_HOI) + 1):
    if f"mo_hoi_{i}" not in names_s:
        L.append(f"slot.add mo_hoi_{i} bone=mo_hoi_{i} at=before:luoi_trai")
    L.append(f"att.region mo_hoi_{i} mo_hoi image=mo_hoi x=0 y=0 rot=0 use=false")
path = os.path.join(ATOM, "ops", "05_xao_mo_hoi.ops")
open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(atom("do", "-f", path).splitlines()[-1][:200])
print(atom("q", "slots"))
