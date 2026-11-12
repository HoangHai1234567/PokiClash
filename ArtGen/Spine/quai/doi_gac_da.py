"""Suất ải 10 đảo Mộc: đổi dòng Dê Hoa (`de_hoa`, ba dạng) thành dòng Gạc Đá (`gac_da`, tượng đá cổ giữ rừng, hai dạng), 2026-11-12.

Người dùng chốt: "thay vào, thay tên id luôn cho phù hợp"; tên "bạn tự đặt"; hai dạng; chỉ số và thẻ theo Dê Hoa.
Claude đặt: id `gac_da`, tên Gạc Đá, danh hiệu "Tượng cổ giữ rừng", dòng "Dòng Gạc Đá"; dạng 1 Mầm Đá (`gac_da_1`, cỡ 0,92), dạng 2
Gạc Đá (`gac_da_2`, cỡ 1,1); thẻ `gac_da_skill` Quyền Đá Bay (chiêu mana: bắn hai tảng tay), `gac_da_ult` Cầu Tim Rừng (chiêu cuối: tụ
cầu năng lượng rồi ném), `gac_da_pas` Da Đá Rêu. Độ hiếm, sáu chỉ số, số mảnh, số và hiệu ứng thẻ, biểu tượng, chỗ đứng trong danh
sách giữ nguyên của Dê Hoa.

Sửa tại chỗ, giữ nguyên xuống dòng và thụt lề của từng file; chạy lại không đổi gì thêm (mẫu: doi_ca_den.py).
    py -3 -I ArtGen/Spine/quai/doi_gac_da.py [--kiem]

Đổi: Assets/02 Data/Json/{heroes,cards,stages,balance}.json (saveVersion 8, đội mẫu); mọi Assets/02 Data/Golden/*.json có id cũ (chỉ
đổi id; golden phụ thuộc số dạng phải tính lại bằng menu trong Unity); Assets/01 Script (IslandGen.cs; SaveData.cs: bước chuyển bản
lưu v7 -> v8; CoreGoldenTests.cs); quai/da_nhan.json. Sau đó trong Unity: xem ArtGen/Spine/inbox/tuong_da_ghichu.md.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIEM = "--kiem" in sys.argv
CU, MOI = "de_hoa", "gac_da"
da_doi = []
DOI_ID = re.compile(r"(?<![a-z_])de_hoa(?![a-z])")          # de_hoa, de_hoa_1, de_hoa_skill...; không đụng chuỗi dài hơn chứa nó


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
        if f == "roster.json" and '"migrate"' in s0:      # phần "migrate" là đầu ra của RIÊNG bước v3 (su_gia → de_hoa): giữ id cũ
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
if "Dê" in blk:
    blk = thay(blk, '"name": "Dê Hoa"', '"name": "Gạc Đá"', 1, "heroes tên")
    blk = thay(blk, '"Sừng gỗ vương miện hoa"', '"Tượng cổ giữ rừng"', 1, "heroes danh hiệu")
    blk = thay(blk, '"Dòng Dê Hoa"', '"Dòng Gạc Đá"', 1, "heroes dòng")
    blk = thay(blk, '"size": 0.9,' + nl + '   "forms"', '"size": 0.92,' + nl + '   "forms"', 1, "heroes cỡ")
    a = blk.index('"forms": [')
    b = blk.index("]", a)
    forms = nl.join(['"forms": [',
                     "    {", '     "name": "Mầm Đá",', '     "aola": "gac_da_1",', '     "size": 0.92', "    },",
                     "    {", '     "name": "Gạc Đá",', '     "aola": "gac_da_2",', '     "size": 1.1', "    }",
                     "   "])
    blk = blk[:a] + forms + blk[b:]
ghi(D + "Json/heroes.json", s0, s[:i] + blk + s[k:])

s0 = doc(D + "Json/cards.json")
s = doi_id(s0)
for the, cu_, moi_ in (("gac_da_skill", "Húc Sừng", "Quyền Đá Bay"), ("gac_da_ult", "Xung Phong Sừng Chiến", "Cầu Tim Rừng"),
                       ("gac_da_pas", "Lông Dày", "Da Đá Rêu")):
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
ghi(C + "Editor/IslandGen.cs", s0, thay(s0, f'new Intro(10, "{CU}", ', f'new Intro(10, "{MOI}", ', 1, "IslandGen"))

# bước chuyển bản lưu: KHÔNG ghi cứng số phiên bản (phiên khác cũng đang đổi id tướng Mộc, vd. doi_mam_u.py): đọc saveVersion hiện tại N,
# thêm bước [N] = MigrateGacDa, nâng lên N + 1. Đã có MigrateGacDa thì bỏ qua cả ba chỗ.
s0 = doc(C + "Core/SaveData.cs")
s = s0
if "MigrateGacDa" not in s:
    m = re.search(r"(Migrations\s*=\s*new Dictionary<int, Action<Dictionary<string, object>>>\s*\{)(.*?)(\r?\n\s*\};)", s, re.S)
    if not m:
        raise SystemExit("SaveData: không thấy bảng Migrations")
    buoc = [int(x) for x in re.findall(r"\[(\d+)\]\s*=", m.group(2))]
    if N in buoc:
        raise SystemExit(f"SaveData: đã có bước [{N}] mà saveVersion vẫn {N}: phiên khác đang sửa dở, dừng")
    s = s[:m.end(2)].rstrip(" ") + f" [{N}] = MigrateGacDa," + s[m.end(2):]
    a = "        public static void MigrateThuyV5(Dictionary<string, object> o)"
    nl = "\r\n" if "\r\n" in s else "\n"
    moi = nl.join([
        f"        // v{N} -> v{N + 1} (2026-11-12): suất ải 10 đảo Mộc đổi dòng Dê Hoa (de_hoa) thành dòng Gạc Đá (gac_da, tượng đá cổ giữ rừng, hai",
        f"        // dạng); bản lưu v{N} đã có de_hoa thì gộp sang gac_da (sở hữu, mảnh, sao, cấp thẻ, tiềm năng, đội, tướng khởi đầu)",
        "        public static readonly (string from, string to)[] GacDaMap = { (\"de_hoa\", \"gac_da\") };",
        "",
        "        public static void MigrateGacDa(Dictionary<string, object> o)",
        "        {",
        "            GopTuong(o, GacDaMap);",
        "            var st = J.Str(o, \"starter\");",
        "            if (st != null) o[\"starter\"] = Map(GacDaMap, st);",
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
    print(f"bước chuyển bản lưu: [{N}] = MigrateGacDa, saveVersion {N} -> {N + 1}")

# ---------------------------------------------------------------- danh sách rig đã nhận (vao_game.py chép vào Resources)
Q = "ArtGen/Spine/quai/"
s0 = doc(Q + "da_nhan.json")
if '"id": "gac_da"' not in s0:
    nl = "\r\n" if "\r\n" in s0 else "\n"
    i = s0.rindex("]")                                       # cuối mảng "nhan"
    j = s0.rindex("}", 0, i)
    moi = ("," + nl + '    {"id": "gac_da", "dang": [{"nguon": "ArtGen/Spine/inbox/tuong_da_1/rig", "atomik": "tuong_da_1.atomik", '
           '"dich": "gac_da_1"}, {"nguon": "ArtGen/Spine/inbox/tuong_da_2/rig", "atomik": "tuong_da_2.atomik", "dich": "gac_da_2"}]}')
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
