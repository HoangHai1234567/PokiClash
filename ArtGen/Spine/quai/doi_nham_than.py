"""Suất ải 15 đảo Hỏa (Sườn Núi Khói): dòng Nham Thần (`nham_than`) đổi HÌNH thành golem lõi lửa (mã làm việc golem_lua), 2026-11-13.

Người dùng chốt: "cho vào game"; GIỮ id `nham_than` và tên Nham Thần; dòng còn 2 dạng (trước là 3). Không đổi id nên không cần bước chuyển
bản lưu (sao cao tự dừng ở dạng cuối: HeroDef.FormIndex), không đổi saveVersion.
- heroes.json, khối nham_than: forms 3 → 2: dạng 1 "Nham Con" (`nham_than_1`, cỡ 0,92; tạm dùng rig golem cho tới khi có dạng 1 thật),
  dạng 2 "Nham Thần" (`nham_than_2`, cỡ 1,1; rig golem_lua_1); size chung 0,92. Danh hiệu, chỉ số, độ hiếm, số mảnh giữ nguyên.
- cards.json: tên thẻ chiêu cuối "Biển Dung Nham" → "Cầu Lửa Lăn" (chiêu mới: co thành quả cầu lửa, lăn tông vào đối thủ rồi bật về; tên
  do Claude đặt). Số, hiệu ứng, biểu tượng giữ nguyên. "Phun Nham" (chiêu mana: há mồm phun lửa) và "Thân Nham" giữ.
- StageView.FireFx: nham_than ("nham", "thien_thach") → ("phun", "no_lon"): phun lửa từ họng (xương `mieng`), nổ lớn lúc quả cầu tông.

Sửa tại chỗ, giữ nguyên xuống dòng và thụt lề; chạy lại không đổi gì thêm.
    py -3 -I ArtGen/Spine/quai/doi_nham_than.py [--kiem]
Sau đó trong Unity: chép rig vào Resources/nham_than_1, 2, xoá nham_than_3, refresh, Nhập dữ liệu, Gắn dạng .atomik, golden (roster: số dạng
3 → 2), EditMode. Ghi chú: ArtGen/Spine/inbox/golem_lua_ghichu.md mục 6.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIEM = "--kiem" in sys.argv
da_doi = []


def doc(rel):
    return open(os.path.join(ROOT, rel), "r", encoding="utf-8", newline="").read()


def ghi(rel, cu, moi):
    if cu == moi:
        return
    da_doi.append(rel)
    if not KIEM:
        open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="").write(moi)


def thay(s, a, b, ten):
    if a not in s:
        if b in s:
            return s
        raise SystemExit(f"{ten}: không thấy đoạn cần thay")
    if s.count(a) != 1:
        raise SystemExit(f"{ten}: đoạn cần thay xuất hiện {s.count(a)} lần")
    return s.replace(a, b)


def khoi(s, id_):
    """(đầu, cuối) của khối JSON object chứa "id": "<id_>" (đếm ngoặc từ dấu { mở gần nhất trước nó)."""
    k = s.index(f'"id": "{id_}"')
    a = s.rindex("{", 0, k)
    d, i = 0, a
    while True:
        c = s[i]
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return a, i + 1
        i += 1


NL = "\r\n" if "\r\n" in doc("Assets/02 Data/Json/heroes.json") else "\n"

# heroes.json
rel = "Assets/02 Data/Json/heroes.json"
s0 = doc(rel)
a, b = khoi(s0, "nham_than")
blk = s0[a:b]
cu_forms = blk[blk.index('"forms": ['):blk.index("]", blk.index('"forms": [')) + 1]
ind = "    "
moi_forms = ('"forms": [' + NL +
             f'{ind}{{{NL}{ind} "name": "Nham Con",{NL}{ind} "aola": "nham_than_1",{NL}{ind} "size": 0.92{NL}{ind}}},{NL}'
             f'{ind}{{{NL}{ind} "name": "Nham Thần",{NL}{ind} "aola": "nham_than_2",{NL}{ind} "size": 1.1{NL}{ind}}}{NL}   ]')
blk2 = blk.replace(cu_forms, moi_forms)
blk2 = blk2.replace('"size": 0.9,', '"size": 0.92,', 1)
ghi(rel, s0, s0[:a] + blk2 + s0[b:])

# cards.json
rel = "Assets/02 Data/Json/cards.json"
s0 = doc(rel)
a, b = khoi(s0, "nham_than_ult")
blk = s0[a:b]
ghi(rel, s0, s0[:a] + thay(blk, '"name": "Biển Dung Nham"', '"name": "Cầu Lửa Lăn"', "cards nham_than_ult") + s0[b:])

# StageView.cs
rel = "Assets/01 Script/Game/Battle/StageView.cs"
s0 = doc(rel)
ghi(rel, s0, thay(s0, '{ "nham_than", ("nham", "thien_thach") }', '{ "nham_than", ("phun", "no_lon") }', "StageView FireFx"))

print(("CHẠY THỬ, sẽ đổi: " if KIEM else "đã đổi: ") + (", ".join(da_doi) if da_doi else "không có gì (đã đổi từ trước)"))
