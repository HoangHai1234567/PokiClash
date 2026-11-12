"""Suất ải 5 đảo Mộc: đổi id và tên dòng Hoa Nhụy (`hoa_nhuy`) thành dòng Mầm Ú (`mam_u`, tinh linh hạt mầm bụng bự), 2026-11-12.

Người dùng dặn "bạn tự sửa tên và id đi" (hình đã thay bằng dòng tinh linh rừng mập, ArtGen/Spine/tinh_linh*.py). Claude đặt:
tướng Mầm Ú, danh hiệu "Tinh linh hạt mầm bụng bự", dòng "Dòng Mầm Ú"; dạng 1 Hạt Ú, dạng 2 Mầm Ú, dạng 3 Hoa Ú; thẻ chiêu mana
Phun Lá (icon leaf), chiêu cuối Húc Bụng (icon fist), bị động Bụng Nảy (icon seed); id thẻ `mam_u_skill/_ult/_pas`, hình
`mam_u_1..3`. Chỉ số, độ hiếm, số và hiệu ứng thẻ, cỡ dạng, chỗ đứng trong danh sách giữ nguyên, nên golden chỉ đổi id.

Sửa tại chỗ, giữ nguyên xuống dòng và thụt lề của từng file; chạy lại không đổi gì thêm.
    py -3 -I ArtGen/Spine/quai/doi_mam_u.py [--kiem]

Đổi: Assets/02 Data/Json/{heroes,cards,stages,balance}.json (saveVersion + 1); Assets/02 Data/Golden/*.json (chỉ id);
Assets/01 Script (IslandGen.cs, StageView.cs, HatNuoc.cs, HatMoc.cs, MocFxTour.cs, SaveData.cs: thêm bước chuyển bản lưu MigrateMamU,
CoreGoldenTests.cs); quai/da_nhan.json; GD_Claude/13, 14.
KHÔNG đổi tên thư mục hình: việc đó làm trong Unity (giữ GUID), xem ArtGen/Spine/inbox/tinh_linh_ghichu.md mục 10.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIEM = "--kiem" in sys.argv
CU, MOI = "hoa_nhuy", "mam_u"
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


def khoi(s, dau, ten):
    """đoạn từ `dau` tới mục "id" kế tiếp (một tướng / một thẻ)."""
    i = s.index(dau)
    j = s.find('"id": "', i + len(dau))
    if j < 0:
        j = len(s)
    return i, j


# ---------------------------------------------------------------- dữ liệu JSON
D = "Assets/02 Data/"
gd = os.path.join(ROOT, D, "Golden")
for f in ["Json/stages.json"] + ["Golden/" + x for x in sorted(os.listdir(gd)) if x.endswith(".json")]:
    s = doc(D + f)
    ghi(D + f, s, s.replace(CU, MOI))

s0 = doc(D + "Json/heroes.json")
s = s0.replace(CU, MOI)
i, j = khoi(s, f'"id": "{MOI}"', "heroes")
blk = s[i:j]
if "Hoa Nhụy" in blk:
    blk = thay(blk, '"name": "Hoa Nhụy"', '"name": "Mầm Ú"', 1, "heroes tên")
    blk = thay(blk, '"Tiên hoa nhụy đỏ"', '"Tinh linh hạt mầm bụng bự"', 1, "heroes danh hiệu")
    blk = thay(blk, '"Dòng Hoa Nhụy"', '"Dòng Mầm Ú"', 1, "heroes dòng")
    blk = thay(blk, '"Thú Ba Lá"', '"Hạt Ú"', 1, "heroes dạng 1")
    blk = thay(blk, '"Thú Búp Hoa"', '"Mầm Ú"', 1, "heroes dạng 2")
    blk = thay(blk, '"Tiên Hoa Nhụy"', '"Hoa Ú"', 1, "heroes dạng 3")
ghi(D + "Json/heroes.json", s0, s[:i] + blk + s[j:])

s0 = doc(D + "Json/cards.json")
s = s0.replace(CU, MOI)
for the, ten_cu, ten_moi, icon_cu, icon_moi in (("skill", "Phấn Hoa", "Phun Lá", "lotus", "leaf"),
                                                ("ult", "Hương Ru Ngủ", "Húc Bụng", "moon", "fist"),
                                                ("pas", "Nhụy Hút Mật", "Bụng Nảy", "lotus", "seed")):
    i, j = khoi(s, f'"id": "{MOI}_{the}"', "cards " + the)
    blk = s[i:j]
    if f'"{ten_cu}"' in blk:
        blk = thay(blk, f'"name": "{ten_cu}"', f'"name": "{ten_moi}"', 1, f"cards {the} tên")
        blk = thay(blk, f'"icon": "{icon_cu}"', f'"icon": "{icon_moi}"', 1, f"cards {the} icon")
    s = s[:i] + blk + s[j:]
ghi(D + "Json/cards.json", s0, s)

# ---------------------------------------------------------------- mã C#
C = "Assets/01 Script/"
s0 = doc(C + "Editor/IslandGen.cs")
ghi(C + "Editor/IslandGen.cs", s0, thay(s0, f'new Intro(5, "{CU}", ', f'new Intro(5, "{MOI}", ', 1, "IslandGen"))

s0 = doc(C + "Game/Battle/StageView.cs")
ghi(C + "Game/Battle/StageView.cs", s0, thay(s0, '{ "hoa_nhuy", ("n_la", ', '{ "mam_u", ("n_la", ', 1, "StageView.MocFx"))

s0 = doc(C + "Game/Battle/HatNuoc.cs")
s = thay(s0, '{ "hoa_nhuy", new WTheme', '{ "mam_u", new WTheme', 1, "HatNuoc.WThemes")
s = s.replace("suất hoa_nhuy;", "dòng Mầm Ú, id mam_u;")
ghi(C + "Game/Battle/HatNuoc.cs", s0, s)

s0 = doc(C + "Game/Battle/HatMoc.cs")
ghi(C + "Game/Battle/HatMoc.cs", s0, s0.replace("tướng tinh linh rừng ở suất hoa_nhuy:", "tướng tinh linh rừng Mầm Ú, id mam_u:"))

s0 = doc(C + "Editor/MocFxTour.cs")
s = thay(s0, 'ThuyFxTour.TryOnly("hoa_nhuy")', 'ThuyFxTour.TryOnly("mam_u")', 1, "MocFxTour")
s = s.replace("hạt lá tinh linh rừng, chiêu mana", "hạt lá Mầm Ú, chiêu mana")
ghi(C + "Editor/MocFxTour.cs", s0, s)

# bước chuyển bản lưu: số phiên bản đọc từ balance.json (phiên khác cũng đổi id tướng cùng ngày, ai chạy trước cũng được)
s0 = doc(C + "Core/SaveData.cs")
if "MigrateMamU" not in s0:
    b0 = doc(D + "Json/balance.json")
    N = int(re.search(r'"saveVersion": (\d+)', b0).group(1))
    m = re.search(r"Migrations =.*?(\[%d\] = \w+,)" % (N - 1), s0, re.S)
    if not m or re.search(r"\[%d\] = " % N, s0):
        raise SystemExit(f"SaveData.Migrations: không thấy bước [{N - 1}] ở cuối hoặc đã có bước [{N}]")
    s = s0[:m.end(1)] + f" [{N}] = MigrateMamU," + s0[m.end(1):]
    a = "        public static void MigrateThuyV5(Dictionary<string, object> o)"
    nl = "\r\n" if "\r\n" in s else "\n"
    moi = nl.join([
        f"        // v{N} -> v{N + 1} (2026-11-12): suất ải 5 đảo Mộc đổi id dòng Hoa Nhụy (hoa_nhuy) thành dòng Mầm Ú (mam_u, tinh linh hạt mầm",
        f"        // bụng bự); bản lưu v{N} đã có hoa_nhuy thì gộp sang mam_u như các bước trên",
        "        public static readonly (string from, string to)[] MamU = { (\"hoa_nhuy\", \"mam_u\") };",
        "",
        "        public static void MigrateMamU(Dictionary<string, object> o)",
        "        {",
        "            GopTuong(o, MamU);",
        "            var st = J.Str(o, \"starter\");",
        "            if (st != null) o[\"starter\"] = Map(MamU, st);",
        "        }",
        "", ""])
    s = thay(s, a, moi + a, 1, "SaveData hàm")
    ghi(C + "Core/SaveData.cs", s0, s)
    ghi(D + "Json/balance.json", b0, thay(b0, f'"saveVersion": {N}', f'"saveVersion": {N + 1}', 1, "balance"))
    t0 = doc(C + "Tests/CoreGoldenTests.cs")
    ghi(C + "Tests/CoreGoldenTests.cs", t0,
        thay(t0, f"Assert.AreEqual({N}, d.Cfg.saveVersion);", f"Assert.AreEqual({N + 1}, d.Cfg.saveVersion);", 1, "CoreGoldenTests"))

# ---------------------------------------------------------------- danh sách đã nhận, tài liệu
Q = "ArtGen/Spine/quai/da_nhan.json"
s0 = doc(Q)
s = s0.replace('"id": "hoa_nhuy"', '"id": "mam_u"')
for k in "123":
    s = s.replace(f'"dich": "hoa_nhuy_{k}"', f'"dich": "mam_u_{k}"')
s = s.replace("Id, tên, danh hiệu, tên dạng, thẻ CHƯA đổi.",
              "Cùng ngày đổi id hoa_nhuy -> mam_u, tên Mầm Ú (Hạt Ú, Mầm Ú, Hoa Ú), thẻ Phun Lá, Húc Bụng, Bụng Nảy (quai/doi_mam_u.py).")
ghi(Q, s0, s)

G = "GD_Claude/13_DanhSachTuong.md"
s0 = doc(G)
m = re.search(r"\| 5 \| `hoa_nhuy` \| Hoa Nhụy \| Tiên hoa nhụy đỏ \| Thường \|[^\n\r]*", s0)
if m:
    moi = ("| 5 | `mam_u` | Mầm Ú | Tinh linh hạt mầm bụng bự | Thường | hình riêng trên rig Spine (2026-11-12, thay dòng Hoa Nhụy "
           "`hoa_nhuy` 593 → 594 → 595): Hạt Ú → Mầm Ú → Hoa Ú | mới, đổi id |")
    ghi(G, s0, s0[:m.start()] + moi + s0[m.end():])
G = "GD_Claude/14_HeThongAi.md"
s0 = doc(G)
ghi(G, s0, s0.replace("| 5 | Đồng Hoa Sáng | Hoa Nhụy |", "| 5 | Đồng Hoa Sáng | Mầm Ú |"))

# ---------------------------------------------------------------- kiểm còn sót
sot = []
for thu_muc in ("Assets/02 Data", "Assets/01 Script"):
    for goc, _, files in os.walk(os.path.join(ROOT, thu_muc)):
        for f in files:
            if not f.endswith((".json", ".cs")):
                continue
            t = open(os.path.join(goc, f), encoding="utf-8-sig", errors="replace").read()
            n = t.count(CU) - (t.count('("hoa_nhuy", "mam_u")') + t.count("(hoa_nhuy)") + t.count("đã có hoa_nhuy")
                               if f == "SaveData.cs" else 0)
            if n > 0:
                sot.append(os.path.relpath(os.path.join(goc, f), ROOT))
print(("SẼ đổi" if KIEM else "đã đổi") + f" {len(da_doi)} file:" if da_doi else "không có gì phải đổi")
for f in da_doi:
    print("  ", f)
if sot and not KIEM:
    print("CÒN id cũ trong:", sot)
