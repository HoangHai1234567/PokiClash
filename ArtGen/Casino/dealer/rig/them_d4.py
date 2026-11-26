# D4 (GD_Claude/31, lều Vòng Xoay): thêm vào project rig ĐANG CÓ (không dựng lại cả rig) viên bi roulette Lão Mực kẹp ở tay phải:
# slot `la_bi` trên xương tay_pb (tên bắt đầu `la_` nên DealerRig tự xếp vào lớp trước), vẽ ngay dưới hai bàn tay nên ngón cái +
# ngón trỏ của hình kẹp (tay_05) che một phần viên bi. Hình vẽ bằng mã: bi trắng ngà tô phẳng, viền nâu sẫm, vân chì nhẹ; không
# điểm sáng, không bóng (luật hình). Bật tắt bằng p["ball"] của động cơ (dong_co.py), mặc định tắt ở mọi clip cũ.
# Cùng các lệnh dung_rig.py đã có cho lần dựng lại từ đầu. Chạy lại được (đã có slot thì chỉ cập nhật ảnh và chỗ đặt).
# Chạy: py -3 -I them_d4.py   rồi   py -3 -I hoat_anh.py rl_invite rl_no_more rl_spin rl_watch rl_point
import os, random, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dong_co import atom, ATOM  # noqa: E402
from dung_rig import BI_X, BI_Y  # noqa: E402

BI_D = 34   # đường kính viên bi (px rig)


def draw_ball(path, d_px=BI_D, k=6):
    pad = 3
    n = (d_px + pad * 2) * k
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink = (59, 40, 30, 255)
    box = [pad * k, pad * k, n - pad * k, n - pad * k]
    d.ellipse(box, fill=(253, 248, 236, 255))
    # vân chì nhẹ (chỉ là vân, không mảng sáng tối)
    rnd = random.Random(11)
    tex = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    td = ImageDraw.Draw(tex)
    for _ in range(26):
        x = rnd.uniform(0, n)
        y = rnd.uniform(0, n)
        td.line([(x, y), (x + 7 * k, y - 4 * k)], fill=(226, 212, 186, 90), width=k)
    mask = im.split()[3].point(lambda v: 255 if v > 200 else 0)
    im.paste(Image.alpha_composite(im, tex), (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.ellipse(box, outline=ink, width=int(2.6 * k))
    im.resize((d_px + pad * 2, d_px + pad * 2), Image.LANCZOS).save(path)


draw_ball(os.path.join(ATOM, "images", "bi.png"))
have_s = atom("q", "slots", check=False)
names_s = {ln.split()[1] for ln in have_s.splitlines() if len(ln.split()) > 1}
L = []
if "bi " not in atom("q", "images", "--limit", "200", check=False) and not any(
        ln.split()[:1] == ["bi"] for ln in atom("q", "images", "--limit", "200", check=False).splitlines()):
    L.append("image.add bi path=images/bi.png")
if "la_bi" not in names_s:
    L.append("slot.add la_bi bone=tay_pb at=before:ban_tay_trai")
L.append(f"att.region la_bi bi image=bi x={BI_X} y={BI_Y} rot=0 use=false")
path = os.path.join(ATOM, "ops", "06_bi.ops")
open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(atom("do", "-f", path).splitlines()[-1][:200])
print(atom("q", "slots"))
