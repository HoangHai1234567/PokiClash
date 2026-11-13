"""Suất ải 5 đảo Hỏa: đổi dòng Khổng Lồ Lửa (`khong_lo`, ba dạng) thành dòng Hỏa Nhãn (`hoa_nhan`, mắt lửa bọc giáp, hai dạng), 2026-11-13.

Người dùng chốt: "thay vào game đi"; đổi id mới; tên Hỏa Nhãn (Claude đề xuất, người dùng chọn). Chỉ số, thẻ theo Khổng Lồ Lửa (như Gạc Đá).
id `hoa_nhan`, tên Hỏa Nhãn, danh hiệu "Mắt lửa giáp nham", dòng "Dòng Hỏa Nhãn"; dạng 1 Nhãn Than (`hoa_nhan_1`, cỡ 0,92), dạng 2 Hỏa Nhãn
(`hoa_nhan_2`, cỡ 1,1); thẻ `hoa_nhan_skill` Hỏa Nhãn Xạ (chiêu mana: tia lửa từ con ngươi), `hoa_nhan_ult` Quyền Chong Chóng (chiêu
cuối: hai nắm tay quay quanh thân rồi lao vào đập liên tục), `hoa_nhan_pas` Giáp Nham. Tên thẻ do Claude đặt. Độ hiếm, sáu chỉ số, số
mảnh, số và hiệu ứng thẻ, biểu tượng, chỗ đứng trong danh sách giữ nguyên của Khổng Lồ Lửa.

Sửa tại chỗ, giữ nguyên xuống dòng và thụt lề của từng file; chạy lại không đổi gì thêm (mẫu: doi_gac_da.py).
    py -3 -I ArtGen/Spine/quai/doi_hoa_nhan.py [--kiem]

Đổi: Assets/02 Data/Json/{heroes,cards,stages,balance}.json (saveVersion +1, đội mẫu); mọi Assets/02 Data/Golden/*.json có id cũ (chỉ
đổi id; golden phụ thuộc số dạng phải tính lại bằng menu trong Unity); Assets/01 Script (IslandGen.cs, HatLua.cs, StageView.cs,
HoaFxTour.cs; SaveData.cs: bước chuyển bản lưu; CoreGoldenTests.cs); quai/da_nhan.json. Sau đó trong Unity: xem
ArtGen/Spine/inbox/mat_lua_ghichu.md mục 7.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIEM = "--kiem" in sys.argv
CU, MOI = "khong_lo", "hoa_nhan"
da_doi = []
DOI_ID = re.compile(r"(?<![a-z_])khong_lo(?![a-z])")        # khong_lo, khong_lo_1, khong_lo_skill...; không đụng chuỗi dài hơn chứa nó


def doc(rel):
    return open(os.path.join(ROOT, rel), "r", encoding="utf-8", newline="").read()


def ghi(rel, cu, moi):
    if cu == moi:
        return
    da_doi.append(rel)
    if not KIEM:
        open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="").write(moi)


def thay(s, a, b, so=None, ten=""):
    """thay a bằng b; so = số lần phải có (None: bao nhiêu cũng được). Đã thay rồi (không còn a, đã có b) thì bỏ qua."""
    n = s.count(a)
    if n == 0 and (b in s):
        return s
    if so is not None and n != so:
        raise SystemExit(f"{ten}: cần {so} chỗ '{a}', thấy {n}")
    return s.replace(a, b)


def doi_id(s):
    return DOI_ID.sub(MOI, s)


# ---------------------------------------------------------------- dữ liệu JSON
D = "Assets/02 Data/"
s0 = doc(D + "Json/stages.json")
ghi(D + "Json/stages.json", s0, doi_id(s0))
for f in sorted(os.listdir(os.path.join(ROOT, D, "Golden"))):
    if f.endswith(".json"):
        s0 = doc(D + "Golden/" + f)
        if f == "roster.json" and '"migrate"' in s0:      # phần "migrate" là đầu ra của RIÊNG bước v3: giữ nguyên
            i = s0.index('"migrate"')
            ghi(D + "Golden/" + f, s0, doi_id(s0[:i]) + s0[i:])
        else:
            ghi(D + "Golden/" + f, s0, doi_id(s0))

s0 = doc(D + "Json/heroes.json")
s = doi_id(s0)
nl = "\r\n" if "\r\n" in s else "\n"
i = s.index(f'"id": "{MOI}"')
k = s.index('"id": "', i + 10)
blk = s[i:k]
if "Khổng Lồ" in blk:
    blk = thay(blk, '"name": "Khổng Lồ Lửa"', '"name": "Hỏa Nhãn"', 2, "heroes tên")      # tên tướng + tên dạng 3 (thay lại ở forms)
    blk = thay(blk, '"Sừng lửa thân than"', '"Mắt lửa giáp nham"', 1, "heroes danh hiệu")
    blk = thay(blk, '"Dòng Khổng Lồ Lửa"', '"Dòng Hỏa Nhãn"', 1, "heroes dòng")
    m = re.search(r'"size": 0\.9,(\s*)"forms"', blk)
    if not m:
        raise SystemExit("heroes cỡ: không thấy \"size\": 0.9 trước forms")
    blk = blk[:m.start()] + '"size": 0.92,' + m.group(1) + '"forms"' + blk[m.end():]
    a = blk.index('"forms": [')
    b = blk.index("]", a)
    ind = re.search(r'\n([ \t]*)"forms"', blk).group(1)             # thụt lề của khoá forms
    forms = nl.join(['"forms": [',
                     ind + " {", ind + '  "name": "Nhãn Than",', ind + '  "aola": "hoa_nhan_1",', ind + '  "size": 0.92', ind + " },",
                     ind + " {", ind + '  "name": "Hỏa Nhãn",', ind + '  "aola": "hoa_nhan_2",', ind + '  "size": 1.1', ind + " }",
                     ind])
    blk = blk[:a] + forms + blk[b:]
ghi(D + "Json/heroes.json", s0, s[:i] + blk + s[k:])

s0 = doc(D + "Json/cards.json")
s = doi_id(s0)
for the, cu_, moi_ in (("hoa_nhan_skill", "Đấm Than", "Hỏa Nhãn Xạ"), ("hoa_nhan_ult", "Núi Lửa Giáng", "Quyền Chong Chóng"),
                       ("hoa_nhan_pas", "Da Than", "Giáp Nham")):
    i = s.index(f'"id": "{the}"')
    k = s.index('"id": "', i + 10)
    blk = s[i:k]
    if f'"name": "{moi_}"' not in blk:
        blk = thay(blk, f'"name": "{cu_}"', f'"name": "{moi_}"', 1, "cards " + the)
    s = s[:i] + blk + s[k:]
ghi(D + "Json/cards.json", s0, s)

s0 = doc(D + "Json/balance.json")
N = int(re.search(r'"saveVersion":\s*(\d+)', s0).group(1))          # phiên bản bản lưu hiện tại; nâng ở phần SaveData bên dưới
ghi(D + "Json/balance.json", s0, doi_id(s0))                       # đội mẫu (simTeams)

# ---------------------------------------------------------------- mã C#
C = "Assets/01 Script/"
s0 = doc(C + "Editor/IslandGen.cs")
ghi(C + "Editor/IslandGen.cs", s0, thay(s0, f'new Intro(5, "{CU}", ', f'new Intro(5, "{MOI}", ', 1, "IslandGen"))
for rel in ("Game/Battle/HatLua.cs", "Game/Battle/StageView.cs", "Editor/HoaFxTour.cs"):        # bảng màu, hiệu ứng trận, tour thử
    s0 = doc(C + rel)
    ghi(C + rel, s0, doi_id(s0))

# bước chuyển bản lưu: KHÔNG ghi cứng số phiên bản: đọc saveVersion hiện tại N, thêm bước [N] = MigrateHoaNhan, nâng lên N + 1.
s0 = doc(C + "Core/SaveData.cs")
s = s0
if "MigrateHoaNhan" not in s:
    m = re.search(r"(Migrations\s*=\s*new Dictionary<int, Action<Dictionary<string, object>>>\s*\{)(.*?)(\r?\n\s*\};)", s, re.S)
    if not m:
        raise SystemExit("SaveData: không thấy bảng Migrations")
    buoc = [int(x) for x in re.findall(r"\[(\d+)\]\s*=", m.group(2))]
    if N in buoc:
        raise SystemExit(f"SaveData: đã có bước [{N}] mà saveVersion vẫn {N}: phiên khác đang sửa dở, dừng")
    s = s[:m.end(2)].rstrip(" ") + f" [{N}] = MigrateHoaNhan," + s[m.end(2):]
    a = "        public static void MigrateThuyV5(Dictionary<string, object> o)"
    nl = "\r\n" if "\r\n" in s else "\n"
    moi = nl.join([
        f"        // v{N} -> v{N + 1} (2026-11-13): suất ải 5 đảo Hỏa đổi dòng Khổng Lồ Lửa (khong_lo) thành dòng Hỏa Nhãn (hoa_nhan, mắt lửa",
        f"        // bọc giáp, hai dạng); bản lưu v{N} đã có khong_lo thì gộp sang hoa_nhan (sở hữu, mảnh, sao, cấp thẻ, tiềm năng, đội, tướng khởi đầu)",
        "        public static readonly (string from, string to)[] HoaNhanMap = { (\"khong_lo\", \"hoa_nhan\") };",
        "",
        "        public static void MigrateHoaNhan(Dictionary<string, object> o)",
        "        {",
        "            GopTuong(o, HoaNhanMap);",
        "            var st = J.Str(o, \"starter\");",
        "            if (st != null) o[\"starter\"] = Map(HoaNhanMap, st);",
        "        }",
        "", ""])
    s = thay(s, a, moi + a, 1, "SaveData hàm")
    ghi(C + "Core/SaveData.cs", s0, s)
    b0 = doc(D + "Json/balance.json")
    b1 = doi_id(b0)
    ghi(D + "Json/balance.json", b0, thay(b1, f'"saveVersion": {N}', f'"saveVersion": {N + 1}', 1, "balance"))
    t0 = doc(C + "Tests/CoreGoldenTests.cs")
    ghi(C + "Tests/CoreGoldenTests.cs", t0, thay(t0, f"Assert.AreEqual({N}, d.Cfg.saveVersion);", f"Assert.AreEqual({N + 1}, d.Cfg.saveVersion);", 1,
                                                 "CoreGoldenTests"))
    print(f"bước chuyển bản lưu: [{N}] = MigrateHoaNhan, saveVersion {N} -> {N + 1}")

# ---------------------------------------------------------------- danh sách rig đã nhận (vao_game.py chép vào Resources)
Q = "ArtGen/Spine/quai/"
s0 = doc(Q + "da_nhan.json")
if '"id": "hoa_nhan"' not in s0:
    nl = "\r\n" if "\r\n" in s0 else "\n"
    i = s0.rindex("]")                                       # cuối mảng "nhan"
    j = s0.rindex("}", 0, i)
    moi = ("," + nl + '    {"id": "hoa_nhan", "dang": [{"nguon": "ArtGen/Spine/inbox/mat_lua_1/rig", "atomik": "mat_lua_1.atomik", '
           '"dich": "hoa_nhan_1"}, {"nguon": "ArtGen/Spine/inbox/mat_lua_2/rig", "atomik": "mat_lua_2.atomik", "dich": "hoa_nhan_2"}]}')
    ghi(Q + "da_nhan.json", s0, s0[:j + 1] + moi + s0[j + 1:])

# ---------------------------------------------------------------- kiểm còn sót
sot = []
for goc, _, files in os.walk(os.path.join(ROOT, "Assets", "02 Data")):
    for f in files:
        t = open(os.path.join(goc, f), encoding="utf-8-sig", errors="replace").read() if f.endswith(".json") else ""
        if f == "roster.json" and '"migrate"' in t:
            t = t[:t.index('"migrate"')]
        if DOI_ID.search(t):
            sot.append(os.path.relpath(os.path.join(goc, f), ROOT))
print(("SẼ đổi" if KIEM else "đã đổi") + f" {len(da_doi)} file:" if da_doi else "không có gì phải đổi")
for f in da_doi:
    print("  ", f)
if sot and not KIEM:
    print("CÒN id cũ trong:", sot)
