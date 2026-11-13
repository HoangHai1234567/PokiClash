# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 5 đảo Hỏa (id `nguu_quyen`, ải 90 = ải 20 của đảo, "Lò Lửa Thiền") sang rùa golem lửa (mã làm việc rua_lua, rig monster_3425;
người dùng 2026-11-13: "làm tướng thứ 5 đảo hỏa, concept rùa golem lửa ...", duyệt concept A, xem rig rồi "ok ổn cho vào game đi").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (ba dạng) nên golden không đổi (golden chỉ ghi id, không ghi tên). Đổi:
    aola    tướng + cả ba dạng -> rua_lua_1 (mới có một rig; dạng 2, 3 to dần theo `size` sẵn có 0,9 / 1,02 / 1,14 cho tới khi có dạng sau)
    tên     Ngưu Quyền -> Hỏa Quy (cả ba dạng); danh hiệu "Rùa đá cõng lửa"; dòng "Dòng Hỏa Quy"
    thẻ     Song Quyền Lửa -> Hỏa Cầu (fist -> flame); Ngưu Ma Liên Quyền -> Sừng Tụ Hỏa Cầu (fist2 -> sun);
            Máu Đấu Sĩ -> Mai Nung Đỏ (rage giữ)
Tên do Claude đặt, người dùng có thể đổi. Không đè, không xoá thư mục Resources/nguu_quyen_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm. Trả về như cũ: `--ve_cu`.

    py -3 -I ArtGen/Spine/quai/doi_rua_lua.py [--kiem] [--ve_cu]
    py -3 -I ArtGen/Spine/quai/doi_rua_lua.py chep      chép rig/rua_lua_1.atomik + chân dung vào Resources/rua_lua_1/ (thư mục mới)
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
ID = "nguu_quyen"
AOLA = ["rua_lua_1"] * 4                                                 # khoá aola theo thứ tự xuất hiện: tướng, dạng 1, dạng 2, dạng 3
AOLA_CU = ["nguu_quyen_1", "nguu_quyen_1", "nguu_quyen_2", "nguu_quyen_3"]
TEN = ["Hỏa Quy"] * 4                                                    # name: tướng, dạng 1, 2, 3
TEN_CU = ["Ngưu Quyền", "Nghé Lửa", "Ngưu Lãng Tử", "Ngưu Quyền"]
KHAC = [("title", "Quyền thủ mây lửa", "Rùa đá cõng lửa"), ("line", "Dòng Ngưu Quyền", "Dòng Hỏa Quy")]
THE = {"nguu_quyen_skill": ("Song Quyền Lửa", "Hỏa Cầu", "fist", "flame"),
       "nguu_quyen_ult": ("Ngưu Ma Liên Quyền", "Sừng Tụ Hỏa Cầu", "fist2", "sun"),
       "nguu_quyen_pas": ("Máu Đấu Sĩ", "Mai Nung Đỏ", "rage", "rage")}


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
    for ma in ("rua_lua_1",):
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
