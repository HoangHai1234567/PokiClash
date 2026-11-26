# D3 (GD_Claude/31): thêm lá bài Lão Mực cầm ở tay phải vào project rig ĐANG CÓ (không dựng lại cả rig): ảnh lưng bài từ tờ đồ bàn
# (../d3/do_ban/la_lung.png, cat_do_ban.py) thu về cỡ lá trên tay -> ../atom/images/la_bai.png, rồi chạy ../atom/ops/04_la_bai.ops
# (cùng các lệnh dung_rig.py đã có cho lần dựng lại từ đầu). Chạy lại được: đã có slot thì chỉ cập nhật ảnh và chỗ đặt.
# Chạy: py -3 -I them_la_bai.py   rồi   py -3 -I hoat_anh.py   (nướng lại clip, có khoá la_cam)
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dong_co import atom, ATOM  # noqa: E402
from dung_rig import LA_X, LA_Y, LA_ROT  # noqa: E402

CARD_H = 158   # px rig: lá trên tay hơi nhỏ hơn lá nằm trên nỉ (gần Lão Mực hơn bàn người chơi)
src = Image.open(os.path.join(HERE, "..", "d3", "do_ban", "la_lung.png")).convert("RGBA")
w = round(src.width * CARD_H / src.height)
src.resize((w, CARD_H), Image.LANCZOS).save(os.path.join(ATOM, "images", "la_bai.png"))

have = atom("q", "slots", check=False)
L = []
if " la_cam " not in have and not any(ln.split()[1:2] == ["la_cam"] for ln in have.splitlines()):
    L += ["image.add la_bai path=images/la_bai.png",
          "slot.add la_cam bone=tay_pb at=before:ban_tay_trai"]
L.append(f"att.region la_cam la_bai image=la_bai x={LA_X} y={LA_Y} rot={LA_ROT} use=false")
path = os.path.join(ATOM, "ops", "04_la_bai.ops")
open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(atom("do", "-f", path).splitlines()[-1][:200])
print(atom("q", "slots"))
