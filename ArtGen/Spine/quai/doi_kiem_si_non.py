# -*- coding: utf-8 -*-
"""Suất 8 đảo Mộc (id `tho_hoang`, Voọc Tướng) từ MỘT dạng thành HAI dạng (người dùng 2026-11-13: "ok xuất ra rồi cho vào game"):

    dạng 1  Voọc Non   (tho_hoang_1, 0,92) = khỉ con khăn trán, kiếm cùn trong vỏ gỗ (rig inbox/kiem_si_non/rig, có clip evolve)
    dạng 2  Voọc Tướng (tho_hoang_2, 1,1)  = dạng lớn xuất lại là dạng 2/2 (inbox/kiem_si_non/rig_lon/kiem_si_1.atomik)

Tên "Voọc Non" do Claude đặt tạm, người dùng có thể đổi. Cỡ theo lệ dòng hai dạng (0,92 / 1,1).

Sửa nguồn `Assets/02 Data/Json/heroes.json` (forms, aola, size của tướng) và `stages.json` (ải 260, boss của suất: thêm "evo": true, đúng như
menu "Đảo 70 ải: sinh lại" ra khi tướng có > 1 dạng). Chép `.atomik` + chân dung vào `Assets/03 Art/Heroes/Resources/tho_hoang_<k>/`
(ghi đè nội dung tho_hoang_1, giữ .meta). Sau đó trong Unity: Nhập dữ liệu, Gắn dạng .atomik vào prefab tướng, tính lại golden
(roster: số dạng; sim, islands: ải 260 tiến hóa). Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_kiem_si_non.py [--kiem]
"""
import filecmp
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
ROOT = os.path.normpath(os.path.join(SPINE, "..", ".."))
JSON = os.path.join(ROOT, "Assets", "02 Data", "Json")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
KIEM = "--kiem" in sys.argv
ID = "tho_hoang"

FORMS_CU = '''   "size": 1,
   "forms": [
    {
     "name": "Voọc Tướng",
     "aola": "tho_hoang_1",
     "size": 1
    }
   ]'''
FORMS_MOI = '''   "size": 0.92,
   "forms": [
    {
     "name": "Voọc Non",
     "aola": "tho_hoang_1",
     "size": 0.92
    },
    {
     "name": "Voọc Tướng",
     "aola": "tho_hoang_2",
     "size": 1.1
    }
   ]'''
EVO_CU = '''     "hero": "tho_hoang",
     "level": 142,
     "boss": true,
     "buff": 1,'''
EVO_MOI = '''     "hero": "tho_hoang",
     "level": 142,
     "boss": true,
     "evo": true,
     "buff": 1,'''

CHEP = [  # (nguồn, đích)
    ("inbox/kiem_si_non/rig/kiem_si_non.atomik", "tho_hoang_1/tho_hoang_1.atomik"),
    ("inbox/kiem_si_non/rig/chan_dung.png", "tho_hoang_1/tho_hoang_1_portrait.png"),
    ("inbox/kiem_si_non/rig_lon/kiem_si_1.atomik", "tho_hoang_2/tho_hoang_2.atomik"),
    ("inbox/kiem_si_non/rig_lon/chan_dung.png", "tho_hoang_2/tho_hoang_2_portrait.png"),
]


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


def thay_trong_khoi(dau, cuoi, cu, moi):
    def fn(t):
        nl = "\r\n" if "\r\n" in t else "\n"
        c, m = cu.replace("\n", nl), moi.replace("\n", nl)
        a, b = khoi(t, dau, cuoi)
        k = t[a:b]
        if m in k:
            return t, 0
        if c not in k:
            raise SystemExit(f"không thấy đoạn cần đổi sau {dau!r}")
        return t[:a] + k.replace(c, m, 1) + t[b:], 1
    return fn


def main():
    sua(os.path.join(JSON, "heroes.json"), thay_trong_khoi(f'"id": "{ID}"', '"id": "', FORMS_CU, FORMS_MOI))
    sua(os.path.join(JSON, "stages.json"), thay_trong_khoi('"id": 260,', '"id": 261,', EVO_CU, EVO_MOI))
    for src, dst in CHEP:
        s, d = os.path.join(SPINE, src), os.path.join(RES, dst)
        if not os.path.isfile(s):
            raise SystemExit(f"thiếu {s} (dựng: kiem_si_non.py rig / lon2)")
        same = os.path.isfile(d) and filecmp.cmp(s, d, shallow=False)
        print(f"  {dst}: {'giống, bỏ qua' if same else 'chép' + (' (chỉ kiểm)' if KIEM else '')} ({os.path.getsize(s) // 1024} KB)")
        if not same and not KIEM:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)


if __name__ == "__main__":
    main()
