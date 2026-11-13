# -*- coding: utf-8 -*-
"""Đưa dạng non mới vào game (người dùng 2026-11-13 duyệt concept: suất 9 hướng A "nụ sừng", suất 10 dạng 1 và 2):

    suất 9  moc_tinh   dạng 1 Giác Mộc Non  : Resources/giac_moc_1 ← inbox/giac_moc_non/rig/giac_moc_non.atomik (trước: bản sao giac_moc_2)
    suất 10 thanh_long dạng 1 Thanh Long Con: Resources/moc_vuong_d1 ← inbox/thanh_long_non/rig_d1/thanh_long_d1.atomik
                       dạng 2 Thanh Long    : Resources/moc_vuong_d2 ← inbox/thanh_long_non/rig_d2/thanh_long_d2.atomik
                       dạng 3 Lôi Thanh Long: moc_vuong_1 (giữ)

Số dạng không đổi (2 và 3), tên dạng giữ; golden không chứa thư mục hình nên không đổi. Sửa `heroes.json` (aola của dạng 1, 2 Thanh Long)
và `Tests/RosterTests.cs` (assert thư mục ba dạng). Sau đó trong Unity: Nhập dữ liệu, "Gắn dạng .atomik vào prefab tướng".
Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_dang_non_9_10.py [--kiem]
"""
import filecmp
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
ROOT = os.path.normpath(os.path.join(SPINE, "..", ".."))
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
KIEM = "--kiem" in sys.argv

CHEP = [("inbox/giac_moc_non/rig/giac_moc_non.atomik", "giac_moc_1/giac_moc_1.atomik"),
        ("inbox/giac_moc_non/rig/chan_dung.png", "giac_moc_1/giac_moc_1_portrait.png"),
        ("inbox/thanh_long_non/rig_d1/thanh_long_d1.atomik", "moc_vuong_d1/moc_vuong_d1.atomik"),
        ("inbox/thanh_long_non/rig_d1/chan_dung.png", "moc_vuong_d1/moc_vuong_d1_portrait.png"),
        ("inbox/thanh_long_non/rig_d2/thanh_long_d2.atomik", "moc_vuong_d2/moc_vuong_d2.atomik"),
        ("inbox/thanh_long_non/rig_d2/chan_dung.png", "moc_vuong_d2/moc_vuong_d2_portrait.png")]

HEROES_CU = '''     "name": "Thanh Long Con",
     "aola": "moc_vuong_1",'''
HEROES_MOI = '''     "name": "Thanh Long Con",
     "aola": "moc_vuong_d1",'''
HEROES_CU2 = '''     "name": "Thanh Long",
     "aola": "moc_vuong_1",'''
HEROES_MOI2 = '''     "name": "Thanh Long",
     "aola": "moc_vuong_d2",'''
TOP_CU = '''   "aola": "moc_vuong_1",
   "elem": "moc",
   "rarity": "legend",'''
TOP_MOI = '''   "aola": "moc_vuong_d1",
   "elem": "moc",
   "rarity": "legend",'''
TEST_CU = '''            // 2026-11-13: hình của suất này nay là rồng trúc bốn cánh (boss cuối đảo Mộc, rig ArtGen/Spine/moc_vuong_rig.py); rig mới mới có
            // một dạng nên cả ba dạng tạm trỏ chung moc_vuong_1 (thư mục thanh_long_* cũ còn nguyên; quai/doi_moc_vuong.py --ve_cu trả lại)
            Assert.AreEqual(new[] { "moc_vuong_1", "moc_vuong_1", "moc_vuong_1" }, System.Array.ConvertAll(d.Hero("thanh_long").forms, f => f.aola));'''
TEST_MOI = '''            // 2026-11-13: hình của suất này nay là rồng trúc bốn cánh (boss cuối đảo Mộc, rig ArtGen/Spine/moc_vuong_rig.py); dạng 1 rồng con,
            // dạng 2 rồng thiếu niên dựng trên cùng rig (ArtGen/Spine/thanh_long_non.py; thư mục thanh_long_* cũ còn nguyên)
            Assert.AreEqual(new[] { "moc_vuong_d1", "moc_vuong_d2", "moc_vuong_1" }, System.Array.ConvertAll(d.Hero("thanh_long").forms, f => f.aola));'''


def sua(path, pairs, khoi=None):
    t = open(path, "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    a, b = 0, len(t)
    if khoi:
        a = t.index(khoi[0])
        b = t.find(khoi[1], a + len(khoi[0]))
        b = len(t) if b < 0 else b
    k, n = t[a:b], 0
    for cu, moi in pairs:
        cu, moi = cu.replace("\n", nl), moi.replace("\n", nl)
        if moi in k:
            continue
        if cu not in k:
            raise SystemExit(f"{os.path.basename(path)}: không thấy đoạn cần đổi: {cu[:60]!r}")
        k = k.replace(cu, moi, 1)
        n += 1
    print(f"  {os.path.relpath(path, ROOT)}: {n} chỗ đổi" + (" (chỉ kiểm)" if KIEM and n else ""))
    if n and not KIEM:
        open(path, "wb").write((t[:a] + k + t[b:]).encode("utf-8"))


def main():
    sua(os.path.join(ROOT, "Assets", "02 Data", "Json", "heroes.json"), [(TOP_CU, TOP_MOI), (HEROES_CU, HEROES_MOI), (HEROES_CU2, HEROES_MOI2)],
        khoi=('"id": "thanh_long"', '"id": "'))
    sua(os.path.join(ROOT, "Assets", "01 Script", "Tests", "RosterTests.cs"), [(TEST_CU, TEST_MOI)])
    for src, dst in CHEP:
        s, d = os.path.join(SPINE, src), os.path.join(RES, dst)
        if not os.path.isfile(s):
            raise SystemExit(f"thiếu {s} (chạy giac_moc_non.py / thanh_long_non.py)")
        same = os.path.isfile(d) and filecmp.cmp(s, d, shallow=False)
        print(f"  {dst}: {'giống, bỏ qua' if same else 'chép' + (' (chỉ kiểm)' if KIEM else '')} ({os.path.getsize(s) // 1024} KB)")
        if not same and not KIEM:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)


if __name__ == "__main__":
    main()
