# -*- coding: utf-8 -*-
"""Đổi tên suất 5 đảo Mộc (id `phong_linh`, ải 20) sang dòng ma mút rừng (mã làm việc voi_rung; người dùng 2026-11-12: "Vào game
ngay", "Dùng tên tôi đề xuất"). Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ; chỉ đổi TÊN hiển thị và biểu tượng thẻ:

    tướng   Phong Linh -> Lâm Tượng; danh hiệu "Ma mút cõng rừng"; dòng "Dòng Lâm Tượng"
    dạng    Tiểu Phong Linh -> Tượng Mầm; Phong Linh Tướng -> Lâm Tượng
    thẻ     Nanh Gió -> Vòi Phun (leaf); Phong Mộc Sứ -> Dậm Rừng (crack); Nhanh Nhẹn -> Áo Lá Dày (shield)

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại
(thêm `--asset` để sửa thẳng hai asset khi không chạy được menu). Chạy lại không đổi gì thêm. Golden và test không chứa tên hiển thị.

    py -3 -I ArtGen/Spine/quai/doi_ten_lam_tuong.py [--kiem] [--asset]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "Assets", "02 Data")
KIEM = "--kiem" in sys.argv
ID = "phong_linh"

TEN = [("Phong Linh", "Lâm Tượng"), ("Linh tướng gió lá", "Ma mút cõng rừng"), ("Dòng Phong Linh", "Dòng Lâm Tượng"),
       ("Tiểu Phong Linh", "Tượng Mầm"), ("Phong Linh Tướng", "Lâm Tượng")]
THE = {"phong_linh_skill": ("Nanh Gió", "Vòi Phun", "fang", "leaf"),
       "phong_linh_ult": ("Phong Mộc Sứ", "Dậm Rừng", "wind", "crack"),
       "phong_linh_pas": ("Nhanh Nhẹn", "Áo Lá Dày", "feather", "shield")}


def yaml_u(s):
    """chuỗi kiểu Unity YAML: có ký tự ngoài ASCII thì đặt trong ngoặc kép, viết \\xHH (dưới 256) hoặc \\uXXXX."""
    if all(ord(ch) < 128 for ch in s):
        return s
    return '"' + "".join(ch if ord(ch) < 128 else (f"\\x{ord(ch):02X}" if ord(ch) < 256 else f"\\u{ord(ch):04X}") for ch in s) + '"'


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
    for cu, m in sorted(TEN, key=lambda x: -len(x[0])):
        c = k.count('"' + cu + '"')
        k = k.replace('"' + cu + '"', '"' + m + '"')
        n += c
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


def hero_db(t):
    dau = f"  - id: {ID}\n" if f"  - id: {ID}\n" in t else f"  - id: {ID}\r\n"
    a, b = khoi(t, dau, "\n  - id: ")
    k, n = t[a:b], 0
    for cu, m in sorted(TEN, key=lambda x: -len(x[0])):
        c = k.count(yaml_u(cu))
        k = k.replace(yaml_u(cu), yaml_u(m))
        n += c
    return t[:a] + k + t[b:], n


def card_db(t):
    n = 0
    for cid, (cu, m, ic0, ic1) in THE.items():
        dau = f"  - id: {cid}\n" if f"  - id: {cid}\n" in t else f"  - id: {cid}\r\n"
        a, b = khoi(t, dau, "\n  - id: ")
        k = t[a:b]
        k2 = k.replace("name: " + yaml_u(cu), "name: " + yaml_u(m), 1).replace("icon: " + ic0, "icon: " + ic1, 1)
        n += (k2 != k)
        t = t[:a] + k2 + t[b:]
    return t, n


if __name__ == "__main__":
    sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
    sua(os.path.join(DATA, "Json", "cards.json"), cards_json)
    if "--asset" in sys.argv:
        sua(os.path.join(DATA, "HeroDb.asset"), hero_db)
        sua(os.path.join(DATA, "CardDb.asset"), card_db)
