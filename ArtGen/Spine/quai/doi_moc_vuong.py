# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 10 đảo Mộc (id `thanh_long`, boss ải 70) sang rồng trúc bốn cánh (mã làm việc moc_vuong, rig monster_3709; người dùng
2026-11-13: "làm tướng cuối cùng ở đảo mộc, final boss", chốt concept bản tối + sừng măng rồi bật auto mode).

Giữ nguyên id, TÊN (Thanh Long: rồng xanh phương Đông hệ Mộc, vẫn đúng với rồng trúc), danh hiệu, chỉ số, thẻ, số dạng (ba dạng) nên
không golden nào đổi. Chỉ đổi khoá `aola` của tướng và của ba dạng: thanh_long_1 / _2 / _3 → moc_vuong_1 (rig mới mới có MỘT dạng; dạng
non làm sau nếu người dùng muốn, lúc đó trỏ lại từng dạng). KHÔNG đè, không xoá thư mục Resources/thanh_long_* cũ.

Sửa `Assets/02 Data/Json/heroes.json` (nguồn). HeroDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi "PokiClash/Tướng/Gắn
dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm. Trả về như cũ: `--ve_cu`.

    py -3 -I ArtGen/Spine/quai/doi_moc_vuong.py [--kiem] [--ve_cu]
    py -3 -I ArtGen/Spine/quai/doi_moc_vuong.py chep      chép rig/moc_vuong_1.atomik + chân dung vào Resources/moc_vuong_1/ (thư mục mới)
"""
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "Assets", "02 Data")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
RIG = os.path.join(HERE, "..", "inbox", "moc_vuong_1", "rig")
KIEM = "--kiem" in sys.argv
VE_CU = "--ve_cu" in sys.argv
ID, MOI = "thanh_long", "moc_vuong_1"


def heroes_json(t):
    a = t.index(f'"id": "{ID}"')
    b = t.find('"id": "', a + 10)
    b = len(t) if b < 0 else b
    k = t[a:b]
    if VE_CU:
        dem = iter([1, 1, 2, 3])                      # khoá aola của tướng (= dạng 1) rồi ba dạng theo thứ tự
        k2 = re.sub(rf'"aola": "{MOI}"', lambda m: f'"aola": "{ID}_{next(dem)}"', k)
    else:
        k2 = re.sub(rf'"aola": "{ID}_\d"', f'"aola": "{MOI}"', k)
    n = sum(1 for x, y in zip(re.findall(r'"aola": "[^"]+"', k), re.findall(r'"aola": "[^"]+"', k2)) if x != y)
    return t[:a] + k2 + t[b:], n


def sua(path, fn):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    moi, n = fn(text)
    print(f"  {os.path.relpath(path, ROOT)}: {n} chỗ đổi" + (" (chỉ kiểm)" if KIEM and n else ""))
    if n and not KIEM:
        open(path, "wb").write(moi.encode("utf-8"))


def chep():
    d = os.path.join(RES, MOI)
    os.makedirs(d, exist_ok=True)
    for nguon, dich in ((f"{MOI}.atomik", f"{MOI}.atomik"), ("chan_dung.png", f"{MOI}_portrait.png")):
        p, q = os.path.join(RIG, nguon), os.path.join(d, dich)
        giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
        if not giong:
            shutil.copyfile(p, q)
        print(f"  {os.path.relpath(q, ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(q) // 1024} KB)")


if __name__ == "__main__":
    if "chep" in sys.argv:
        chep()
    else:
        sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
