# Đưa hình lều Đêm Bài (D3, GD_Claude/31) vào Unity: Assets/03 Art/Casino/Leu/ và rig Lão Mực vào Assets/03 Art/Casino/Dealer/.
# - bj_nen.jpg: nền lều cả ảnh (1144 x 2048, nhập 2048: ArtPostprocessor coi /Casino/Leu/ là ảnh lớn);
# - bj_ban.png: lớp bàn (mép bàn sau + khay chip + nỉ) cắt từ hàng BAN_TOP xuống đáy, cùng bề ngang; menu dựng scene đặt nó lệch
#   xuống BAN_TOP px ảnh so với nền (ghi trong leu_bai.json);
# - bài, cỗ bài, chip: cắt từ tờ đồ bàn (cat_do_ban.py), thu về khoảng 2 lần cỡ hiện trên màn;
# - lao_muc.bytes: bản sao atom/export/lao_muc.atomik (đuôi .bytes để AtomikImporter của tướng không nhận; nạp bằng AtomikFile.Load
#   như rương máy bi).
# Chạy: py -3 -I dua_vao_unity.py
import json, os, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LEU = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "Leu")
DEALER = os.path.join(PROJECT, "Assets", "03 Art", "Casino", "Dealer")
os.makedirs(LEU, exist_ok=True)
os.makedirs(DEALER, exist_ok=True)

info = json.load(open(os.path.join(HERE, "tach_lop.json")))
BAN_TOP = 840   # trên hàng này lớp bàn trong suốt hết (mép khay cao nhất 849 - 2,5)
nen = Image.open(os.path.join(HERE, "nen_leu_bai.jpg")).convert("RGB")
nen.save(os.path.join(LEU, "bj_nen.jpg"), quality=92)
ban = Image.open(os.path.join(HERE, "ban_leu_bai.png")).convert("RGBA")
ban.crop((0, BAN_TOP, ban.width, ban.height)).save(os.path.join(LEU, "bj_ban.png"))

# bề cao đích (px ảnh) ~ 2 lần cỡ hiện: lá bài hiện cao ~150, chip ~64, cỗ bài ~130
SIZE = {"la_lung": 300, "la_mat": 300, "co_bai": 260, "chip_do": 128, "chip_vang": 128, "chip_xanh": 128, "chip_la": 128,
        "chong_do": 156, "chong_xanh": 156, "chong_la": 156, "chong_vang": 156}   # chồng chip 4 màu theo bậc cược (doi_mau_chip.py)
for n, hgt in SIZE.items():
    im = Image.open(os.path.join(HERE, "do_ban", n + ".png")).convert("RGBA")
    w = round(im.width * hgt / im.height)
    im.resize((w, hgt), Image.LANCZOS).save(os.path.join(LEU, "bj_" + n + ".png"))

json.dump({"nen": list(nen.size), "ban_top": BAN_TOP, "rim_center_y": info["rim_center_y"], "tray": info["tray"]},
          open(os.path.join(LEU, "leu_bai.json"), "w"), indent=1)
shutil.copyfile(os.path.join(HERE, "..", "atom", "export", "lao_muc.atomik"), os.path.join(DEALER, "lao_muc.bytes"))
print("xong:", LEU, DEALER)
