# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 1 đảo Hỏa (id `su_tu_lua`, ải 71 "Bến Đá Đen") sang dòng tiểu quỷ lava (mã làm việc quy_lava, rig monster_3336; người dùng
2026-11-13: "làm tướng đầu tiên của đảo hỏa ... con gốc lấy ref làm dạng 1", rồi dạng 2 hiệp sĩ dung nham, "ok ổn rồi cho vào game đi").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (ba dạng) nên golden không đổi. Đổi:
    aola    tướng + dạng 1 -> quy_lava_1; dạng 2, dạng 3 -> quy_lava_2 (dạng 3 dùng chung rig dạng 2, to hơn theo `size` sẵn có)
    tên     Sư Tử Lửa -> Tiểu Quỷ Lava (dạng 1), Hiệp Sĩ Dung Nham (dạng 2, 3); danh hiệu "Quỷ lửa cầm khiên"; dòng "Dòng Quỷ Lava"
    thẻ     Liên Hoa Hỏa -> Giáo Phun Lửa (torch); Hỏa Dực Phần Thiên -> Giáo Nham Giáng Thế (phoenix -> sword);
            Lửa Thiền -> Khiên Than Hồng (flame -> shield)
Tên do Claude đặt, người dùng có thể đổi. Không đè, không xoá thư mục Resources/su_tu_lua_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm. Trả về như cũ: `--ve_cu`.

    py -3 -I ArtGen/Spine/quai/doi_quy_lava.py [--kiem] [--ve_cu]
    py -3 -I ArtGen/Spine/quai/doi_quy_lava.py chep      chép rig/quy_lava_<k>.atomik + chân dung vào Resources/quy_lava_<k>/ (thư mục mới)
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
INBOX = os.path.join(HERE, "..", "inbox")
KIEM = "--kiem" in sys.argv
VE_CU = "--ve_cu" in sys.argv
ID = "su_tu_lua"
AOLA = ["quy_lava_1", "quy_lava_1", "quy_lava_2", "quy_lava_2"]        # khoá aola theo thứ tự xuất hiện: tướng, dạng 1, dạng 2, dạng 3
AOLA_CU = ["su_tu_lua_1", "su_tu_lua_1", "su_tu_lua_2", "su_tu_lua_3"]
TEN = ["Tiểu Quỷ Lava", "Tiểu Quỷ Lava", "Hiệp Sĩ Dung Nham", "Hiệp Sĩ Dung Nham"]   # name: tướng, dạng 1, 2, 3
TEN_CU = ["Sư Tử Lửa"] * 4
KHAC = [("title", "Bờm lửa nhỏ", "Quỷ lửa cầm khiên"), ("line", "Dòng Sư Tử Lửa", "Dòng Quỷ Lava")]
THE = {"su_tu_lua_skill": ("Liên Hoa Hỏa", "Giáo Phun Lửa", "torch", "torch"),
       "su_tu_lua_ult": ("Hỏa Dực Phần Thiên", "Giáo Nham Giáng Thế", "phoenix", "sword"),
       "su_tu_lua_pas": ("Lửa Thiền", "Khiên Than Hồng", "flame", "shield")}


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


def thay_lan_luot(k, khoa, cu, moi):
    """thay lần lượt từng khoá `khoa` theo thứ tự xuất hiện: giá trị cu[i] -> moi[i]."""
    n = 0
    out, pos = [], 0
    i = 0
    for m in re.finditer(rf'"{khoa}": "([^"]*)"', k):
        out.append(k[pos:m.start()])
        v = m.group(1)
        if i < len(cu) and v == cu[i] and cu[i] != moi[i]:
            out.append(f'"{khoa}": "{moi[i]}"')
            n += 1
        else:
            out.append(m.group(0))
        pos = m.end()
        i += 1
    out.append(k[pos:])
    return "".join(out), n


def heroes_json(t):
    a, b = khoi(t, f'"id": "{ID}"', '"id": "')
    k = t[a:b]
    if VE_CU:
        k, n1 = thay_lan_luot(k, "aola", AOLA, AOLA_CU)
        k, n2 = thay_lan_luot(k, "name", TEN, TEN_CU)
        n3 = 0
        for khoa, cu, m in KHAC:
            n3 += k.count(f'"{khoa}": "{m}"')
            k = k.replace(f'"{khoa}": "{m}"', f'"{khoa}": "{cu}"')
    else:
        k, n1 = thay_lan_luot(k, "aola", AOLA_CU, AOLA)
        k, n2 = thay_lan_luot(k, "name", TEN_CU, TEN)
        n3 = 0
        for khoa, cu, m in KHAC:
            n3 += k.count(f'"{khoa}": "{cu}"')
            k = k.replace(f'"{khoa}": "{cu}"', f'"{khoa}": "{m}"')
    return t[:a] + k + t[b:], n1 + n2 + n3


def cards_json(t):
    n = 0
    for cid, (cu, m, ic0, ic1) in THE.items():
        a, b = khoi(t, f'"id": "{cid}"', '"id": "')
        k = t[a:b]
        if VE_CU:
            k2 = k.replace(f'"name": "{m}"', f'"name": "{cu}"').replace(f'"icon": "{ic1}"', f'"icon": "{ic0}"')
        else:
            k2 = k.replace(f'"name": "{cu}"', f'"name": "{m}"').replace(f'"icon": "{ic0}"', f'"icon": "{ic1}"')
        n += (k2 != k)
        t = t[:a] + k2 + t[b:]
    return t, n


def chep():
    for ma in ("quy_lava_1", "quy_lava_2"):
        rig = os.path.join(INBOX, ma, "rig")
        d = os.path.join(RES, ma)
        os.makedirs(d, exist_ok=True)
        for nguon, dich in ((f"{ma}.atomik", f"{ma}.atomik"), ("chan_dung.png", f"{ma}_portrait.png")):
            p, q = os.path.join(rig, nguon), os.path.join(d, dich)
            giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
            if not giong:
                shutil.copyfile(p, q)
            print(f"  {os.path.relpath(q, ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(q) // 1024} KB)")


if __name__ == "__main__":
    if "chep" in sys.argv:
        chep()
    else:
        sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
        sua(os.path.join(DATA, "Json", "cards.json"), cards_json)
