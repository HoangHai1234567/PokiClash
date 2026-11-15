# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 7 đảo Hỏa (id `giap_long`, ải 40 của đảo, "Lò Rèn Gai Thép") sang quỷ lửa cầm đao lớn (mã làm việc quy_dao, rig monster_3655;
người dùng 2026-11-13: "làm tướng thứ 7 đảo hỏa, concept quỷ lửa cầm đao lớn ...", chọn concept C sừng đen, xem rig rồi "đưa tướng này vào game").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (hai dạng) nên golden không đổi (golden chỉ ghi id, không ghi tên). Đổi:
    aola    tướng + cả hai dạng -> quy_dao_1 (mới có một rig; dạng 2 to hơn theo `size` sẵn có 0,92 / 1,1 cho tới khi có dạng riêng)
    tên     Giáp Long -> Viêm Đao (cả hai dạng); danh hiệu "Quỷ lửa vác đại đao"; dòng "Dòng Viêm Đao"
    thẻ     Gai Thép -> Địa Hỏa Trảm (sword -> flame); Thiết Long Xung -> Liên Hoàn Đao (hammer -> sword); Giáp Gai -> Giáp Vai Sắt (helmet giữ)
Tên do Claude đặt, người dùng có thể đổi. Không đè, không xoá thư mục Resources/giap_long_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm. Trả về như cũ: `--ve_cu`.

    py -3 -I ArtGen/Spine/quai/doi_quy_dao.py [--kiem] [--ve_cu]
    py -3 -I ArtGen/Spine/quai/doi_quy_dao.py chep      chép rig/quy_dao_1.atomik + chân dung vào Resources/quy_dao_1/ (thư mục mới)
    py -3 -I ArtGen/Spine/quai/doi_quy_dao.py chep_non  chép inbox/quy_dao_non/rig/quy_dao_non_th.atomik + chân dung vào Resources/quy_dao_non/
    py -3 -I ArtGen/Spine/quai/doi_quy_dao.py dang_1 [--kiem]   dạng 1 -> quy_dao_non "Viêm Đao Nhi" cỡ 0,8
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
ID = "giap_long"
AOLA = ["quy_dao_1"] * 3                                                 # khoá aola theo thứ tự xuất hiện: tướng, dạng 1, dạng 2
AOLA_CU = ["giap_long_1", "giap_long_1", "giap_long_2"]
TEN = ["Viêm Đao"] * 3                                                   # name: tướng, dạng 1, 2
TEN_CU = ["Giáp Long", "Giáp Long Con", "Giáp Long"]
KHAC = [("title", "Gai thép lửa đỏ", "Quỷ lửa vác đại đao"), ("line", "Dòng Giáp Long", "Dòng Viêm Đao")]
THE = {"giap_long_skill": ("Gai Thép", "Địa Hỏa Trảm", "sword", "flame"),
       "giap_long_ult": ("Thiết Long Xung", "Liên Hoàn Đao", "hammer", "sword"),
       "giap_long_pas": ("Giáp Gai", "Giáp Vai Sắt", "helmet", "helmet")}


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
    for ma in ("quy_dao_1",):
        rig = os.path.join(INBOX, ma, "rig")
        d = os.path.join(RES, ma)
        os.makedirs(d, exist_ok=True)
        for nguon, dich in ((f"{ma}.atomik", f"{ma}.atomik"), ("chan_dung.png", f"{ma}_portrait.png")):
            p, q = os.path.join(rig, nguon), os.path.join(d, dich)
            giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
            if not giong:
                shutil.copyfile(p, q)
            print(f"  {os.path.relpath(q, ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(q) // 1024} KB)")


def dang_1():
    """2026-11-14 (người dùng: "làm dạng 1 cho tướng thứ 7 đảo hỏa"): dạng 1 = quỷ lửa con chibi (ArtGen/Spine/quy_dao_non.py, rig
    inbox/quy_dao_non/rig/quy_dao_non_th.atomik đã gộp clip evolve) -> Resources/quy_dao_non, tên "Viêm Đao Nhi" (Claude đặt), cỡ 0,8; dạng 2
    giữ quy_dao_1 cỡ 1,1. Số dạng không đổi nên golden không đổi."""
    sys.path.insert(0, HERE)
    import doi_phap_lua as P
    path = os.path.join(DATA, "Json", "heroes.json")
    t = open(path, "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    P.ID = ID
    a, b = P.khoi_tuong(t)
    blk = t[a:b]
    blk2 = P.dat_dang(blk, nl, [("Viêm Đao Nhi", "quy_dao_non", 0.8), ("Viêm Đao", "quy_dao_1", 1.1)], "quy_dao_non", 0.8)
    doi = blk2 != blk
    print(f"  {os.path.relpath(path, ROOT)}: khối {ID} " + ("đổi dạng 1" if doi else "đã đúng") + (" (chỉ kiểm)" if KIEM and doi else ""))
    if doi and not KIEM:
        open(path, "wb").write((t[:a] + blk2 + t[b:]).encode("utf-8"))


def chep_non():
    rig = os.path.join(INBOX, "quy_dao_non", "rig")
    d = os.path.join(RES, "quy_dao_non")
    os.makedirs(d, exist_ok=True)
    for nguon, dich in (("quy_dao_non_th.atomik", "quy_dao_non.atomik"), ("chan_dung.png", "quy_dao_non_portrait.png")):
        p, q = os.path.join(rig, nguon), os.path.join(d, dich)
        giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
        if not giong:
            shutil.copyfile(p, q)
        print(f"  {os.path.relpath(q, ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(q) // 1024} KB)")


if __name__ == "__main__":
    if "chep_non" in sys.argv:
        chep_non()
    elif "dang_1" in sys.argv:
        dang_1()
    elif "chep" in sys.argv:
        chep()
    else:
        sua(os.path.join(DATA, "Json", "heroes.json"), heroes_json)
        sua(os.path.join(DATA, "Json", "cards.json"), cards_json)
