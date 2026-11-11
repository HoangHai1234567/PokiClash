# -*- coding: utf-8 -*-
"""Đổi tên suất 7 đảo Thủy (id `lien_kinh`, ải 40) sang dòng cá voi biến dị (người dùng 2026-11-11: "tên tùy bạn quyết").
Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ; chỉ đổi TÊN hiển thị và biểu tượng thẻ:

    tướng   Liên Kình -> Thôn Kình (cá voi nuốt chửng); danh hiệu "Cá voi vô diện đuôi đá"; dòng "Dòng Thôn Kình"
    dạng    Kình Nụ -> Kình Nhi; Liên Kình -> Thôn Kình
    thẻ     Bong Bóng Sen -> Quật Đuôi Đá (rock); Nụ Bung -> Thôn Hải Pháo (wave); Sen Thiêng -> Nuốt Đòn (fang)
    bị động boss  Sen Hộ Thể -> Da Đá Hộ Thể (rock)

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn) và, vì Unity không mở để chạy menu "PokiClash/Nhập dữ liệu", sửa luôn đúng
các dòng tên / biểu tượng đó trong `HeroDb.asset`, `CardDb.asset` (chuỗi YAML của Unity: ký tự ngoài ASCII viết \\xHH hoặc \\uXXXX).
Chạy lại không đổi gì thêm. Golden và test không chứa tên hiển thị.

    py -3 -I ArtGen/Spine/quai/doi_ten_thon_kinh.py [--kiem]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "Assets", "02 Data")
KIEM = "--kiem" in sys.argv

TEN = [("Liên Kình", "Thôn Kình"), ("Kình ngư cõng sen thiêng", "Cá voi vô diện đuôi đá"), ("Dòng Liên Kình", "Dòng Thôn Kình"),
       ("Kình Nụ", "Kình Nhi")]
THE = {"lien_kinh_skill": ("Bong Bóng Sen", "Quật Đuôi Đá", "bubble", "rock"),
       "lien_kinh_ult": ("Nụ Bung", "Thôn Hải Pháo", "lotus", "wave"),
       "lien_kinh_pas": ("Sen Thiêng", "Nuốt Đòn", "lotus", "fang"),
       "lien_kinh_boss": ("Sen Hộ Thể", "Da Đá Hộ Thể", "lotus", "rock")}


def yaml_u(s):
    """chuỗi kiểu Unity YAML: có ký tự ngoài ASCII thì đặt trong ngoặc kép, viết \\xHH (dưới 256) hoặc \\uXXXX."""
    if all(ord(ch) < 128 for ch in s):
        return s
    return '"' + "".join(ch if ord(ch) < 128 else (f"\\x{ord(ch):02X}" if ord(ch) < 256 else f"\\u{ord(ch):04X}") for ch in s) + '"'


def khoi(text, dau, cuoi_tu):
    """đoạn văn bản từ chỗ `dau` tới ngay trước lần gặp `cuoi_tu` kế tiếp: (bắt đầu, kết thúc)."""
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
    a, b = khoi(t, '"id": "lien_kinh"', '"id": "')
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
    a, b = khoi(t, "  - id: lien_kinh\n", "\n  - id: ") if "  - id: lien_kinh\n" in t else khoi(t, "  - id: lien_kinh\r\n", "\n  - id: ")
    k, n = t[a:b], 0
    for cu, m in sorted(TEN, key=lambda x: -len(x[0])):
        c = k.count(yaml_u(cu))
        k = k.replace(yaml_u(cu), yaml_u(m))
        n += c
    return t[:a] + k + t[b:], n


def card_db(t):
    n = 0
    for cid, (cu, m, ic0, ic1) in THE.items():
        a, b = khoi(t, f"  - id: {cid}\n", "\n  - id: ") if f"  - id: {cid}\n" in t else khoi(t, f"  - id: {cid}\r\n", "\n  - id: ")
        k = t[a:b]
        k2 = k.replace("name: " + yaml_u(cu), "name: " + yaml_u(m), 1).replace("icon: " + ic0, "icon: " + ic1, 1)
        n += (k2 != k)
        t = t[:a] + k2 + t[b:]
    return t, n


if __name__ == "__main__":
    sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
    sua(os.path.join(DATA, "Json", "cards.json"), cards_json)
    sua(os.path.join(DATA, "HeroDb.asset"), hero_db)
    sua(os.path.join(DATA, "CardDb.asset"), card_db)
