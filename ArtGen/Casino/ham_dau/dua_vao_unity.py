# Đưa nền scene Hầm đấu (GD_Claude/29 mục 6.5, bản sàn đấu có Lão Mực 2026-11-26) vào Unity: Assets/03 Art/Casino/HamDau/.
# Chạy tach_lop.py trước (tách cổng sắt, khán giả; ra nen_ham_dau_2k_dong.jpg và lop/).
# - hd_nen.jpg: nền dùng trong game (nen_ham_dau_2k_dong.jpg: lòng cổng không còn song, khán giả trong nền chỉ còn mảng tối;
#   1144 x 2048; ArtPostprocessor nhập 2048);
# - hd_quay.png: lớp quầy nhà cái cắt từ mép trên quầy (nét mực trên dải nỉ xanh) xuống, đè lên thân dưới của Lão Mực;
# - hd_cong_song.png + hd_cong_mat_na.png: song sắt và mặt nạ lòng vòm (song trượt lên, vòm che);
# - hd_kg_duoi_<i>.png, hd_kg_xa_<i>.png: khán giả hàng đầu / trên khán đài (nhún);
# - ham_dau.json: số đo trên ảnh 2k (px, gốc trên trái); ham_dau_lop.txt: mỗi dòng "tên x0 y0 x1 y1" cho menu dựng scene đọc.
# Số đo quầy, biển lấy bằng tay trên ảnh có thước. Chạy: py -3 -I dua_vao_unity.py
import json, os, shutil
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "HamDau")
os.makedirs(OUT, exist_ok=True)

M = {
    "size": [1144, 2048],
    "rim_y": 693,                     # mép trên quầy (hàng đầu của nét mực trên dải nỉ): thân Lão Mực dưới hàng này bị quầy che
    "opening": [407, 330, 730, 693],  # lòng quầy màu kem (x0, y0, x1, y1): chỗ Lão Mực đứng
    "cover": [330, 693, 814, 940],    # lớp quầy cắt ra (x0, y0, x1, y1)
    "sign": [392, 835, 748, 928],     # biển gỗ trống: ghi tên bậc
    "pit": [0, 1150, 1144, 1700],     # sàn cát (khung bao elip, gần đúng)
    "bottom_color": "#302338",        # màu đáy ảnh (bóng khán giả): tô phần màn dài hơn ảnh
}

src = Image.open(os.path.join(HERE, "nen_ham_dau_2k_dong.jpg")).convert("RGB")
assert list(src.size) == M["size"], src.size
src.save(os.path.join(OUT, "hd_nen.jpg"), quality=92)

x0, y0, x1, y1 = M["cover"]
c = np.asarray(src.crop((x0, y0, x1, y1)).convert("RGBA")).copy()
c[0, :, 3] = 128  # hàng đầu nửa trong: mép mềm, không lộ đường cắt
Image.fromarray(c, "RGBA").save(os.path.join(OUT, "hd_quay.png"))

lop = json.load(open(os.path.join(HERE, "lop", "lop.json")))["pieces"]
lines = []
for name, box in lop.items():
    shutil.copyfile(os.path.join(HERE, "lop", name + ".png"), os.path.join(OUT, "hd_" + name + ".png"))
    lines.append("hd_%s %d %d %d %d" % (name, *box))
open(os.path.join(OUT, "ham_dau_lop.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
M["layers"] = lop
json.dump(M, open(os.path.join(OUT, "ham_dau.json"), "w"), indent=1)
print("xong:", OUT, sorted(os.listdir(OUT)))
