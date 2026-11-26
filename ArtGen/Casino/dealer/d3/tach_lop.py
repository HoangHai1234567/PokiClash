# Tách nền lều Đêm Bài (nen_leu_bai_2k.jpg: Magnific GPT 2.6 1k high rồi phóng classic 2k) thành hai lớp cho scene có dealer
# (GD_Claude/31 mục 3): nền (cả ảnh, Lão Mực đứng trước) và bàn (mép bàn sau + khay chip + nỉ, đè lên hông Lão Mực).
# Đường cắt bám nét mực trên cùng của vành bàn / khay (đo tay, bảng TOP), cắt cao hơn 2,5 px để giữ nét.
# Ra: nen_leu_bai.jpg (đổi tên cho gọn), ban_leu_bai.png (RGBA, đúng cỡ ảnh nền, phần trên trong suốt), tach_lop_xem.png, tach_lop.json
# (y mép bàn từng cột ở giữa, khung khay chip, tính theo pixel ảnh 2k).
import json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(HERE, "nen_leu_bai_2k.jpg")).convert("RGB")
W, H = src.size
# Mép trên của nét mực vành bàn / khay chip, đo bằng hồ sơ độ sáng từng cột trên ảnh 2k (dò tự động bắt nhầm nét rương, cột lều).
TOP = [(0, 943), (100, 920), (200, 908), (280, 902), (296, 903), (343, 849), (805, 849), (848, 912), (950, 912), (1050, 929),
       (1144, 950)]
xs = np.array([p[0] for p in TOP], float)
ys = np.array([p[1] for p in TOP], float)
top = np.interp(np.arange(W), xs, ys)
cut = top - 2.5
yy = np.arange(H)[:, None]
alpha = np.clip(yy - cut[None, :] + 0.5, 0, 1)   # mép mềm nửa pixel
rgba = np.dstack([np.asarray(src), (alpha * 255).astype(np.uint8)])
Image.fromarray(rgba, "RGBA").save(os.path.join(HERE, "ban_leu_bai.png"))
src.save(os.path.join(HERE, "nen_leu_bai.jpg"), quality=92)

# xem: đường cắt tô hồng trên ảnh thu nhỏ
pv = src.copy()
d = ImageDraw.Draw(pv)
d.line([(x, float(cut[x])) for x in range(0, W, 2)], fill=(255, 0, 255), width=3)
pv.crop((0, int(cut.min()) - 260, W, int(cut.max()) + 200)).save(os.path.join(HERE, "tach_lop_xem.png"))
info = {"size": [W, H], "rim_center_y": float(top[W // 2]), "rim_left_y": float(top[5]), "rim_right_y": float(top[W - 5]),
        "tray": {"x0": 343, "x1": 805, "top": 849, "foot_x0": 296, "foot_x1": 848}}
json.dump(info, open(os.path.join(HERE, "tach_lop.json"), "w"), indent=1)
print(info)
