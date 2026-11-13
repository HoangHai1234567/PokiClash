# -*- coding: utf-8 -*-
"""Đổi suất 9 đảo Mộc (id `moc_tinh`, ải 60 "Hang Pha Lê Lục") sang dòng thú cổ thụ một sừng (mã làm việc giac_moc, rig monster_3804;
người dùng 2026-11-13 duyệt concept hướng A + sừng kiểu 2: "auto mode làm hết đi"). Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, biểu tượng
thẻ, số dạng (hai dạng); đổi TÊN hiển thị và thư mục hình của hai dạng:

    tướng   Mộc Tinh -> Giác Mộc; danh hiệu "Thú cổ thụ một sừng"; dòng "Dòng Giác Mộc"
    dạng    Tiểu Mộc Tinh (moc_tinh_1, 0,92) -> Giác Mộc Non (giac_moc_1, 0,9); Mộc Tinh (moc_tinh_2, 1,1) -> Giác Mộc (giac_moc_2, 1,05)
    thẻ     Gai Pha Lê -> Tia Sừng Hổ Phách; Rừng Pha Lê -> Tim Cổ Thụ Khai Quang; Giáp Pha Lê -> Vỏ Cây Ngàn Năm
Tên do Claude đặt, người dùng có thể đổi. Dạng non CHƯA có hình riêng (người dùng: "dạng non làm sau"): tạm thời `giac_moc_1` dùng cùng
rig với `giac_moc_2`. Thư mục hình cũ `Resources/moc_tinh_1`, `moc_tinh_2` KHÔNG bị đụng (không xoá, không ghi đè).

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại;
prefab tướng do menu "PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Số dạng không đổi và golden không chứa tên, thư mục hình nên
không phải tính lại golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_giac_moc.py [--kiem]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "Assets", "02 Data")
KIEM = "--kiem" in sys.argv
ID = "moc_tinh"

# trong khối tướng: thay nguyên chuỗi (cũ, mới), theo thứ tự
TUONG = [('"name": "Tiểu Mộc Tinh"', '"name": "Giác Mộc Non"'),
         ('"name": "Mộc Tinh"', '"name": "Giác Mộc"'),
         ('"title": "Thú giáp pha lê lục"', '"title": "Thú cổ thụ một sừng"'),
         ('"line": "Dòng Mộc Tinh"', '"line": "Dòng Giác Mộc"'),
         ('"aola": "moc_tinh_1"', '"aola": "giac_moc_1"'),
         ('"aola": "moc_tinh_2"', '"aola": "giac_moc_2"'),
         ('"size": 0.92', '"size": 0.9'),
         ('"size": 1.1\r', '"size": 1.05\r'), ('"size": 1.1\n', '"size": 1.05\n')]
THE = {"moc_tinh_skill": ("Gai Pha Lê", "Tia Sừng Hổ Phách"),
       "moc_tinh_ult": ("Rừng Pha Lê", "Tim Cổ Thụ Khai Quang"),
       "moc_tinh_pas": ("Giáp Pha Lê", "Vỏ Cây Ngàn Năm")}


def khoi(text, dau, cuoi_tu):
    a = text.index(dau)
    b = text.find(cuoi_tu, a + len(dau))
    return a, (len(text) if b < 0 else b)


def sua(path, fn):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    moi, n = fn(text)
    print(f"  {os.path.relpath(path, ROOT)}: {n} chỗ đổi" + (" (chỉ kiểm)" if KIEM and n else ""))
    if n and not KIEM:
        open(path, "wb").write(moi.encode("utf-8"))


def heroes_json(t):
    a, b = khoi(t, f'"id": "{ID}"', '"id": "')
    k, n = t[a:b], 0
    for cu, m in TUONG:
        n += k.count(cu)
        k = k.replace(cu, m)
    return t[:a] + k + t[b:], n


def cards_json(t):
    n = 0
    for cid, (cu, m) in THE.items():
        a, b = khoi(t, f'"id": "{cid}"', '"id": "')
        k = t[a:b]
        k2 = k.replace(f'"name": "{cu}"', f'"name": "{m}"')
        n += (k2 != k)
        t = t[:a] + k2 + t[b:]
    return t, n


if __name__ == "__main__":
    sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
    sua(os.path.join(DATA, "Json", "cards.json"), cards_json)
