# Đưa hình lều Vòng Xoay (D4, GD_Claude/31) vào Unity: Assets/03 Art/Casino/Leu/rl_* và rig Lão Mực vào Assets/03 Art/Casino/Dealer/.
# - rl_nen.jpg: nền lều cả ảnh (1144 x 2048, nhập 2048: ArtImporter coi /Casino/Leu/rl_nen, rl_ban là ảnh lớn);
# - rl_ban.png: lớp bàn (thanh gỗ mép bàn + khay chip + nỉ) cắt từ hàng BAN_TOP xuống đáy, cùng bề ngang;
# - rl_chao.png, rl_vanh_truoc.png, rl_mam.png, rl_truc.png, rl_bi.png: bánh xe vẽ bằng mã (ve_banh_xe.py, thư mục ra/);
# - rl_banh_xe.json: cỡ và tâm các hình bánh xe (menu dựng scene ghi cứng theo đây, đổi hình thì soát lại CasinoTablesMenu);
# - lao_muc.bytes: bản sao ../atom/export/lao_muc.atomik (26 clip, có rl_invite, rl_no_more, rl_spin, rl_watch, rl_point).
# Chip dùng lại bj_chip_* / bj_chong_* của lều Đêm Bài.
# Chạy: py -3 -I dua_vao_unity.py [--khong-rig]
import json, os, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LEU = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "Leu")
DEALER = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "Dealer")
os.makedirs(LEU, exist_ok=True)

BAN_TOP = 680   # trên hàng này lớp bàn trong suốt hết (mép thanh gỗ cao nhất 684 − 3)
Image.open(os.path.join(HERE, "nen_leu_xoay.jpg")).convert("RGB").save(os.path.join(LEU, "rl_nen.jpg"), quality=92)
ban = Image.open(os.path.join(HERE, "ban_leu_xoay.png")).convert("RGBA")
ban.crop((0, BAN_TOP, ban.width, ban.height)).save(os.path.join(LEU, "rl_ban.png"))
for n in ("rl_chao.png", "rl_vanh_truoc.png", "rl_mam.png", "rl_truc.png", "rl_bi.png"):
    shutil.copyfile(os.path.join(HERE, "ra", n), os.path.join(LEU, n))
info = json.load(open(os.path.join(HERE, "ra", "banh_xe.json")))
info["ban_top"] = BAN_TOP
json.dump(info, open(os.path.join(LEU, "rl_banh_xe.json"), "w"), indent=1)
if "--khong-rig" not in sys.argv:
    shutil.copyfile(os.path.join(HERE, "..", "atom", "export", "lao_muc.atomik"), os.path.join(DEALER, "lao_muc.bytes"))
print("xong:", LEU, info["chao"], info["mam"], info["truc"], info["bi"])
