# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 6 đảo Hỏa (id `hong_lien`, ải 30 của đảo, "Chùa Liên Hoa") sang pháp sư lửa (mã làm việc phap_lua, rig monster_3481;
người dùng 2026-11-13 chốt concept G, 2026-11-14: "suất 6 cho vào game rồi làm thêm dạng 1").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). SỐ DẠNG 3 → 2 (như các suất Hỏa khác đã đổi hình) nên golden roster phải tính
lại trong Unity. Đổi:
    tên     Hồng Liên -> Viêm Sư; danh hiệu "Pháp sư gọi cầu lửa"; dòng "Dòng Viêm Sư"
    dạng    [Đốm Hồng, Phi Viêm, Hồng Liên] (hong_lien_1..3) -> hai dạng. Chưa có rig dạng 1: cả hai trỏ phap_lua_1 (cỡ 0,92 / 1,1).
            Có rig dạng 1 thì chạy `dang_1`: dạng 1 "Viêm Đồng" -> phap_lua_non (cỡ CO_NON)
    thẻ     Cánh Sen Lửa -> Hỏa Châm (lotus -> flame); Hồng Liên Nghiệp Hỏa -> Đại Hỏa Cầu (phoenix -> sun);
            Lông Vũ Lửa -> Thân Khói (feather -> ghost); thẻ boss Niết Bàn Hỏa -> Nhen Lại Lửa Tàn (phoenix -> torch)
Tên do Claude đặt, người dùng có thể đổi. Không đè, không xoá thư mục Resources/hong_lien_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_phap_lua.py [--kiem]
    py -3 -I ArtGen/Spine/quai/doi_phap_lua.py chep            chép rig/phap_lua_1.atomik + chân dung vào Resources/phap_lua_1/ (thư mục mới)
    py -3 -I ArtGen/Spine/quai/doi_phap_lua.py dang_1 [--kiem] dạng 1 -> phap_lua_non (sau khi có Resources/phap_lua_non)
    py -3 -I ArtGen/Spine/quai/doi_phap_lua.py chep_non <thư mục rig dạng 1>   chép <thư mục>/phap_lua_non.atomik + chan_dung.png vào Resources/phap_lua_non/
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
ID = "hong_lien"
TEN, TEN_NON = "Viêm Sư", "Viêm Đồng"
CO_NON = 0.8
KHAC = [("name", "Hồng Liên", TEN), ("title", "Cánh lửa sen đỏ", "Pháp sư gọi cầu lửa"), ("line", "Dòng Hồng Liên", "Dòng Viêm Sư")]
THE = {"hong_lien_skill": ("Cánh Sen Lửa", "Hỏa Châm", "lotus", "flame"),
       "hong_lien_ult": ("Hồng Liên Nghiệp Hỏa", "Đại Hỏa Cầu", "phoenix", "sun"),
       "hong_lien_pas": ("Lông Vũ Lửa", "Thân Khói", "feather", "ghost"),
       "hong_lien_boss": ("Niết Bàn Hỏa", "Nhen Lại Lửa Tàn", "phoenix", "torch")}


def khoi_tuong(t):
    """(a, b): khối { ... } của tướng ID trong heroes.json."""
    k0 = t.index(f'"id": "{ID}"')
    a = t.rindex("{", 0, k0)
    d, i = 0, a
    while True:
        if t[i] == "{":
            d += 1
        elif t[i] == "}":
            d -= 1
            if d == 0:
                return a, i + 1
        i += 1


def dat_dang(blk, nl, dang, aola0, size0):
    """thay mảng forms bằng `dang` [(tên, aola, cỡ)], aola / size chung của tướng = dạng 1."""
    f0 = blk.index('"forms": [')
    f1 = blk.index("]", f0) + 1
    ind = "    "
    muc = [f'{ind}{{{nl}{ind} "name": "{n}",{nl}{ind} "aola": "{a}",{nl}{ind} "size": {s}{nl}{ind}}}' for n, a, s in dang]
    blk = blk[:f0] + '"forms": [' + nl + ("," + nl).join(muc) + nl + "   ]" + blk[f1:]
    dau = blk[:blk.index('"forms": [')]
    dau2 = re.sub(r'"aola": "[^"]*"', f'"aola": "{aola0}"', dau, count=1)
    dau2 = re.sub(r'"size": [0-9.]+', f'"size": {size0}', dau2, count=1)
    return dau2 + blk[len(dau):]


def heroes(dang):
    path = os.path.join(DATA, "Json", "heroes.json")
    t = open(path, "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    a, b = khoi_tuong(t)
    blk = t[a:b]
    dau = blk[:blk.index('"forms": [')]
    dau2 = dau
    for khoa, cu, m in KHAC:
        dau2 = dau2.replace(f'"{khoa}": "{cu}"', f'"{khoa}": "{m}"')
    blk2 = dat_dang(dau2 + blk[len(dau):], nl, dang, dang[0][1], dang[0][2])
    doi = blk2 != blk
    print(f"  {os.path.relpath(path, ROOT)}: khối {ID} " + ("đổi" if doi else "đã đúng") + (" (chỉ kiểm)" if KIEM and doi else ""))
    if doi and not KIEM:
        open(path, "wb").write((t[:a] + blk2 + t[b:]).encode("utf-8"))


def cards():
    path = os.path.join(DATA, "Json", "cards.json")
    t = open(path, "rb").read().decode("utf-8")
    n = 0
    for cid, (cu, m, ic0, ic1) in THE.items():
        a = t.index(f'"id": "{cid}"')
        b = t.find('"id": "', a + 10)
        b = len(t) if b < 0 else b
        k = t[a:b]
        k2 = k.replace(f'"name": "{cu}"', f'"name": "{m}"', 1).replace(f'"icon": "{ic0}"', f'"icon": "{ic1}"', 1)
        n += (k2 != k)
        t = t[:a] + k2 + t[b:]
    print(f"  {os.path.relpath(path, ROOT)}: {n} thẻ đổi" + (" (chỉ kiểm)" if KIEM and n else ""))
    if n and not KIEM:
        open(path, "wb").write(t.encode("utf-8"))


def chep(ma, rig, ten_atomik):
    d = os.path.join(RES, ma)
    os.makedirs(d, exist_ok=True)
    for nguon, dich in ((ten_atomik, f"{ma}.atomik"), ("chan_dung.png", f"{ma}_portrait.png")):
        p, q = os.path.join(rig, nguon), os.path.join(d, dich)
        giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
        if not giong:
            shutil.copyfile(p, q)
        print(f"  {os.path.relpath(q, ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(q) // 1024} KB)")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        chep("phap_lua_1", os.path.join(INBOX, "phap_lua_1", "rig"), "phap_lua_1.atomik")
    elif a[:1] == ["chep_non"]:
        chep("phap_lua_non", os.path.abspath(a[1]), "phap_lua_non.atomik")
    elif a[:1] == ["dang_1"]:
        heroes([(TEN_NON, "phap_lua_non", CO_NON), (TEN, "phap_lua_1", 1.1)])
    else:
        heroes([(TEN, "phap_lua_1", 0.92), (TEN, "phap_lua_1", 1.1)])
        cards()
