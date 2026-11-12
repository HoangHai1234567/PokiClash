# -*- coding: utf-8 -*-
"""Đổi suất 6 đảo Mộc (id `gio_loc`, ải 30) sang dòng chim bảo hộ rừng (mã làm việc chim_la; người dùng 2026-11-12: "ok 2 dạng ổn,
ghép vào game đi"). Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ; đổi TÊN hiển thị, biểu tượng thẻ và SỐ DẠNG (ba dạng → hai dạng):

    tướng   Gió Lốc -> Linh Điểu; danh hiệu "Chim thần giữ rừng"; dòng "Dòng Linh Điểu"
    dạng    Gió Con / Gió Cuộn / Gió Lốc (0,9 / 1,02 / 1,14) -> Điểu Nhi (gio_loc_1, 0,92) / Linh Điểu (gio_loc_2, 1,1)
    thẻ     Lưỡi Gió -> Lông Lá Găm (leaf); Bão Xé Mây -> Thiên Thạch Giáng (rock); Thân Gió -> Cánh Lá Nhẹ (wing)
    bị động boss "Gió Cuốn" giữ (gió từ cánh).
Tên do Claude đặt, người dùng có thể đổi.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại.
Số dạng đổi nên golden phải tính lại bằng menu (xem ArtGen/Spine/inbox/chim_la_ghichu.md mục 8). Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_linh_dieu.py [--kiem]
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "Assets", "02 Data")
KIEM = "--kiem" in sys.argv
ID = "gio_loc"

TEN = [("name", "Gió Lốc", "Linh Điểu"), ("title", "Rồng gió xé mây", "Chim thần giữ rừng"), ("line", "Dòng Gió Lốc", "Dòng Linh Điểu")]
DANG = [("Điểu Nhi", "gio_loc_1", 0.92), ("Linh Điểu", "gio_loc_2", 1.1)]
THE = {"gio_loc_skill": ("Lưỡi Gió", "Lông Lá Găm", "wind", "leaf"),
       "gio_loc_ult": ("Bão Xé Mây", "Thiên Thạch Giáng", "wind", "rock"),
       "gio_loc_pas": ("Thân Gió", "Cánh Lá Nhẹ", "feather", "wing")}


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
    nl = "\r\n" if "\r\n" in t else "\n"
    a, b = khoi(t, f'"id": "{ID}"', '"id": "')
    k, n = t[a:b], 0
    f = k.index('"forms"')
    dau, than = k[:f], k[f:]
    for khoa, cu, m in TEN:
        c = dau.count(f'"{khoa}": "{cu}"')
        dau = dau.replace(f'"{khoa}": "{cu}"', f'"{khoa}": "{m}"')
        n += c
    size = re.search(r'"size": ([0-9.]+)', dau)
    if float(size.group(1)) != DANG[0][2]:
        dau = dau[:size.start(1)] + str(DANG[0][2]) + dau[size.end(1):]
        n += 1
    cuoi = than.index("]") + 1
    moi = '"forms": [' + nl + ("," + nl).join(
        f'    {{{nl}     "name": "{ten}",{nl}     "aola": "{aola}",{nl}     "size": {co}{nl}    }}' for ten, aola, co in DANG) + nl + "   ]"
    if than[:cuoi] != moi:
        than = moi + than[cuoi:]
        n += 1
    return t[:a] + dau + than + t[b:], n


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
