# -*- coding: utf-8 -*-
"""Đổi suất 8 đảo Mộc (id `tho_hoang`, ải 50) sang dòng voọc kiếm sĩ giáp lá (mã làm việc kiem_si; người dùng 2026-11-12: "rất tốt, cho
vào game"). Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, số dạng (một dạng); đổi TÊN hiển thị và biểu tượng thẻ:

    tướng   Thỏ Hoàng -> Voọc Tướng; danh hiệu "Kiếm khách giáp lá"; dòng "Dòng Voọc Tướng"
    dạng    Thỏ Hoàng (tho_hoang_1, 1) -> Voọc Tướng (tho_hoang_1, 1)
    thẻ     Hoàng Quyền -> Bạt Kiếm Trảm (sword); Hoàng Cực Thiên Chưởng -> Ảo Ảnh Loạn Trảm (wind); Khí Hoàng Gia -> Tĩnh Tâm Kiếm (helmet)
    bị động boss  Hoàng Giáp Hộ Thân -> Giáp Lá Hộ Thân (shield)
Tên do Claude đặt, người dùng có thể đổi.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại.
Số dạng không đổi và golden không chứa tên nên không phải tính lại golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_kiem_si.py [--kiem]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "Assets", "02 Data")
KIEM = "--kiem" in sys.argv
ID = "tho_hoang"

# trong khối tướng: (khoá, cũ, mới); "name" có ở cả tướng lẫn dạng nên thay mọi chỗ
TEN = [("name", "Thỏ Hoàng", "Voọc Tướng"), ("title", "Chiến giáp hoàng cực", "Kiếm khách giáp lá"), ("line", "Dòng Thỏ Hoàng", "Dòng Voọc Tướng")]
THE = {"tho_hoang_skill": ("Hoàng Quyền", "Bạt Kiếm Trảm", "fist", "sword"),
       "tho_hoang_ult": ("Hoàng Cực Thiên Chưởng", "Ảo Ảnh Loạn Trảm", "crown", "wind"),
       "tho_hoang_pas": ("Khí Hoàng Gia", "Tĩnh Tâm Kiếm", "crown", "helmet"),
       "tho_hoang_boss": ("Hoàng Giáp Hộ Thân", "Giáp Lá Hộ Thân", "crown", "shield")}


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
    for khoa, cu, m in TEN:
        n += k.count(f'"{khoa}": "{cu}"')
        k = k.replace(f'"{khoa}": "{cu}"', f'"{khoa}": "{m}"')
    return t[:a] + k + t[b:], n


def cards_json(t):
    n = 0
    for cid, (cu, m, ic0, ic1) in THE.items():
        a, b = khoi(t, f'"id": "{cid}"', '"id": "')
        k = t[a:b]
        k2 = k.replace(f'"name": "{cu}"', f'"name": "{m}"').replace(f'"icon": "{ic0}"', f'"icon": "{ic1}"')
        n += (k2 != k)
        t = t[:a] + k2 + t[b:]
    return t, n


if __name__ == "__main__":
    sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
    sua(os.path.join(DATA, "Json", "cards.json"), cards_json)
