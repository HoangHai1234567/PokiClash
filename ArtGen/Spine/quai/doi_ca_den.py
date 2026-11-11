"""Suất ải 10 đảo Thủy: đổi dòng Nòng Xoáy (`nong_xoay`, nòng nọc) thành dòng Hải Đăng (`ca_den`, cá đèn lồng), 2026-11-11.

Người dùng chốt: dòng Hải Đăng, dạng 1 Lồng Đèn, dạng 2 Hải Đăng; thẻ chiêu mana Vòi Nước, chiêu cuối Thủy Pháo; id nội bộ đổi
sang `ca_den` (thẻ `ca_den_skill/_ult/_pas`, hình `ca_den_1`, `ca_den_2`). Chỉ số, độ hiếm, số và hiệu ứng thẻ, tên bị động
(Vụng San Hô), chỗ đứng trong danh sách giữ nguyên, nên golden chỉ đổi id (golden không chứa tên tướng, tên thẻ).

Sửa tại chỗ, giữ nguyên xuống dòng và thụt lề của từng file; chạy lại không đổi gì thêm.
    py -3 -I ArtGen/Spine/quai/doi_ca_den.py [--kiem]

Đổi: Assets/02 Data/Json/{heroes,cards,stages}.json; Assets/02 Data/Golden/{roster,zones,islands,cardtext,badges,potential,
progression}.json; Assets/01 Script (IslandGen.cs, StageView.cs, HatNuoc.cs, SaveData.cs: bước chuyển bản lưu v6 -> v7,
CoreGoldenTests.cs); balance.json (saveVersion 7); quai/{tuong_moi_thuy,golden_thuy,vao_game}.py, da_nhan.json.
Sau đó trong Unity: xem ArtGen/Spine/inbox/ca_den_ghichu.md mục 7.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIEM = "--kiem" in sys.argv
CU, MOI = "nong_xoay", "ca_den"
da_doi = []


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


# ---------------------------------------------------------------- dữ liệu JSON
D = "Assets/02 Data/"
for f in ("Json/stages.json", "Golden/roster.json", "Golden/zones.json", "Golden/islands.json", "Golden/cardtext.json",
          "Golden/badges.json", "Golden/potential.json", "Golden/progression.json"):
    s = doc(D + f)
    ghi(D + f, s, s.replace(CU, MOI))

s0 = doc(D + "Json/heroes.json")
s = s0.replace(CU, MOI)
i = s.index(f'"id": "{MOI}"')
j = s.index('"id": "', i + 10)
k = s.index('"id": "', j + 10) if False else j
blk = s[i:k]
if "Nòng" in blk or "Ếch Lốc" in blk:
    blk = thay(blk, '"Dòng Nòng Xoáy"', '"Dòng Hải Đăng"', 1, "heroes line")
    blk = thay(blk, '"Nòng nọc mắt bão"', '"Cá đèn lồng vực sâu"', 1, "heroes title")
    if blk.count('"Nòng Xoáy"') != 2:
        raise SystemExit(f"heroes: cần 2 chỗ tên 'Nòng Xoáy' (tướng, dạng 1), thấy {blk.count(chr(34) + 'Nòng Xoáy' + chr(34))}")
    blk = blk.replace('"Nòng Xoáy"', '"Hải Đăng"', 1)          # tên tướng (đứng trước mảng forms)
    blk = blk.replace('"Nòng Xoáy"', '"Lồng Đèn"', 1)          # tên dạng 1
    blk = thay(blk, '"Ếch Lốc"', '"Hải Đăng"', 1, "heroes dạng 2")
ghi(D + "Json/heroes.json", s0, s[:i] + blk + s[k:])

s0 = doc(D + "Json/cards.json")
s = s0.replace(CU, MOI)
s = thay(s, '"Đuôi Xoáy"', '"Vòi Nước"', 1, "cards skill")
s = thay(s, '"Xoáy Bong Bóng"', '"Thủy Pháo"', 1, "cards ult")
ghi(D + "Json/cards.json", s0, s)

s0 = doc(D + "Json/balance.json")
ghi(D + "Json/balance.json", s0, thay(s0, '"saveVersion": 6', '"saveVersion": 7', 1, "balance"))

# ---------------------------------------------------------------- mã C#
C = "Assets/01 Script/"
s0 = doc(C + "Editor/IslandGen.cs")
ghi(C + "Editor/IslandGen.cs", s0, thay(s0, f'new Intro(10, "{CU}", ', f'new Intro(10, "{MOI}", ', 1, "IslandGen"))

s0 = doc(C + "Game/Battle/StageView.cs")
m = re.search(r'            \{ "nong_xoay", \("n_bong", new\[\] \{ "n_xoay", "n_voi" \}\) \},[^\n]*', s0)
if m:
    s = s0[:m.start()] + ('            { "ca_den", ("n_tia", new[] { "n_tia", "n_tia" }) },              '
                          '// Vòi Nước (há miệng bắn tia); Thủy Pháo (dậm chân gầm, tia to hơn) ở cả hai dạng') + s0[m.end():]
    ghi(C + "Game/Battle/StageView.cs", s0, s)
elif '{ "ca_den", ("n_tia"' not in s0:
    raise SystemExit("StageView.WaterFx: không thấy dòng nong_xoay")

s0 = doc(C + "Game/Battle/HatNuoc.cs")
m = re.search(r'            \{ "nong_xoay", new WTheme \{ w = WPal\([^\n]*\) \} \},', s0)
if m:
    s = s0[:m.start()] + ('            { "ca_den", new WTheme { w = WPal(C(52, 66, 143), C(76, 95, 196), C(155, 168, 242)) } },'
                          '   // chàm của cá đèn lồng') + s0[m.end():]
    ghi(C + "Game/Battle/HatNuoc.cs", s0, s)
elif '{ "ca_den", new WTheme' not in s0:
    raise SystemExit("HatNuoc.WThemes: không thấy dòng nong_xoay")

s0 = doc(C + "Core/SaveData.cs")
s = thay(s0, '("canh_cut", "nong_xoay")', '("canh_cut", "ca_den")', 1, "SaveData ThuyV6")
if "MigrateCaDenV6" not in s:
    s = thay(s, "[4] = MigrateStarterV4, [5] = MigrateThuyV5,", "[4] = MigrateStarterV4, [5] = MigrateThuyV5, [6] = MigrateCaDenV6,", 1,
             "SaveData Migrations")
    a = "        public static void MigrateThuyV5(Dictionary<string, object> o)"
    nl = "\r\n" if "\r\n" in s else "\n"
    moi = nl.join([
        "        // v6 -> v7 (2026-11-11): suất ải 10 đảo Thủy đổi dòng Nòng Xoáy (nong_xoay) thành dòng Hải Đăng (ca_den, cá đèn lồng);",
        "        // bản lưu v6 đã có nong_xoay thì gộp sang ca_den như bước trên (sở hữu, mảnh, sao, cấp thẻ, tiềm năng, đội, tướng khởi đầu)",
        "        public static readonly (string from, string to)[] CaDenV7 = { (\"nong_xoay\", \"ca_den\") };",
        "",
        "        public static void MigrateCaDenV6(Dictionary<string, object> o)",
        "        {",
        "            GopTuong(o, CaDenV7);",
        "            var st = J.Str(o, \"starter\");",
        "            if (st != null) o[\"starter\"] = Map(CaDenV7, st);",
        "        }",
        "", ""])
    s = thay(s, a, moi + a, 1, "SaveData hàm")
ghi(C + "Core/SaveData.cs", s0, s)

s0 = doc(C + "Tests/CoreGoldenTests.cs")
s = thay(s0, "Assert.AreEqual(6, d.Cfg.saveVersion);", "Assert.AreEqual(7, d.Cfg.saveVersion);", 1, "CoreGoldenTests")
ghi(C + "Tests/CoreGoldenTests.cs", s0, s)

# ---------------------------------------------------------------- script, danh sách đã nhận
Q = "ArtGen/Spine/quai/"
s0 = doc(Q + "tuong_moi_thuy.py")
m = re.search(r'    dict\(id="nong_xoay", old="canh_cut", at=10,.*?pas=\("Vụng San Hô", "drop"\)\),', s0, re.S)
if m:
    nl = "\r\n" if "\r\n" in s0 else "\n"
    moi = nl.join([
        '    dict(id="ca_den", old="canh_cut", at=10, name="Hải Đăng", title="Cá đèn lồng vực sâu", line="Dòng Hải Đăng",   # 2026-11-11: thay Nòng Xoáy',
        '         forms=[("Lồng Đèn", 0.92), ("Hải Đăng", 1.1)],',
        '         skill=("Vòi Nước", "wave"), ult=("Thủy Pháo", "bubble"), pas=("Vụng San Hô", "drop")),'])
    ghi(Q + "tuong_moi_thuy.py", s0, s0[:m.start()] + moi + s0[m.end():])
s0 = doc(Q + "golden_thuy.py")
ghi(Q + "golden_thuy.py", s0, thay(s0, '"canh_cut": "nong_xoay"', '"canh_cut": "ca_den"', 1, "golden_thuy"))
s0 = doc(Q + "vao_game.py")
ghi(Q + "vao_game.py", s0, thay(s0, '"thach_giai", "nong_xoay", "ha_ba"', '"thach_giai", "ca_den", "ha_ba"', 1, "vao_game LO"))
s0 = doc(Q + "da_nhan.json")
m = re.search(r'\{\s*"id":\s*"nong_xoay".*?\]\s*\}', s0, re.S)
if m:
    moi = ('{"id": "ca_den", "dang": [{"nguon": "ArtGen/Spine/inbox/ca_den_1/rig", "atomik": "ca_den_1.atomik", "dich": "ca_den_1"}, '
           '{"nguon": "ArtGen/Spine/inbox/ca_den_2/rig", "atomik": "ca_den_2.atomik", "dich": "ca_den_2"}]}')
    ghi(Q + "da_nhan.json", s0, s0[:m.start()] + moi + s0[m.end():])
elif '"id": "ca_den"' not in s0:
    raise SystemExit("da_nhan.json: không thấy dòng nong_xoay")

# ---------------------------------------------------------------- kiểm còn sót
sot = []
for goc, _, files in os.walk(os.path.join(ROOT, "Assets", "02 Data")):
    for f in files:
        if f.endswith(".json") and CU in open(os.path.join(goc, f), encoding="utf-8-sig", errors="replace").read():
            sot.append(os.path.relpath(os.path.join(goc, f), ROOT))
print(("SẼ đổi" if KIEM else "đã đổi") + f" {len(da_doi)} file:" if da_doi else "không có gì phải đổi")
for f in da_doi:
    print("  ", f)
if sot and not KIEM:
    print("CÒN id cũ trong:", sot)
