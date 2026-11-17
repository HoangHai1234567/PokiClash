# -*- coding: utf-8 -*-
"""Đưa 5 tướng Thổ (2026-11-17) vào mã game: chép HatTho.cs, thêm mã "n_" vào HatNuoc.PlayNuoc, HatVoi.AtkLao, bảng ThoFx / ThoAtk +
nhánh Elem.Tho trong StageView. Sửa TỪNG CHỖ (các phiên khác cũng sửa các file này), chạy lại không đổi thêm.
Đợt 2 (dạng 2 Thạch Giáp / Sa Tích / Tê Thiềm + dạng 1 Sa Long, rig riêng mỗi dạng): thêm case n_*2 / n_long_*1, AtkLao, và đổi ThoFx /
ThoAtk sang bảng THEO DẠNG (như KimFx / AtkDang); khối bảng cũ một-mã-mỗi-tướng trong StageView được thay bằng bản mới.

    py -3 -I ArtGen/Spine/quai/tho5_game/vao_game.py [--kiem] [--khong-sv]   sửa thẳng Assets (--khong-sv: chừa StageView)
    py -3 -I ArtGen/Spine/quai/tho5_game/vao_game.py --ra <thư mục>   ghi bản đã sửa ra thư mục khác (để biên dịch thử)
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
BAT = os.path.join(ROOT, "Assets", "01 Script", "Game", "Battle")
KIEM = "--kiem" in sys.argv
RA = sys.argv[sys.argv.index("--ra") + 1] if "--ra" in sys.argv else None

CASES = '''                case "n_giap_huc": return NGiapHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thạch Giáp (HatTho.cs), đòn thường: lao húc đầu, dăm đá
                case "n_giap_soi": return NGiapSoi(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thạch Giáp: lắc mai, ba viên sỏi (mảnh của rig) găm
                case "n_giap_mua": return NGiapMua(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thạch Giáp: chiêu cuối pha lê vọt lên trời, mưa pha lê hổ phách
                case "n_tich_dop": return NTichDop(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Tích (HatTho.cs), đòn thường: chồm đớp, vết cắn
                case "n_tich_phien": return NTichPhien(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Tích: ba phiến áo choàng đất nung (mảnh của rig) găm
                case "n_tich_loc": return NTichLoc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Tích: chiêu cuối dậm đất, lốc cát trùm đối thủ
                case "n_thiem_giang": return NThiemGiang(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm (HatTho.cs), đòn thường: chồm giáng sừng
                case "n_thiem_phun": return NThiemPhun(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm: há hàm hút đá, phun tảng đá
                case "n_thiem_lan": return NThiemLan(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm: chiêu cuối cuộn tròn lăn nện (rig khai lunge)
                case "n_long_vuot": return NLongVuot(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long (HatTho.cs), đòn thường: lao chém vuốt
                case "n_long_luoi": return NLongLuoi(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long: ba lưỡi cát trăng khuyết
                case "n_long_cot": return NLongCot(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long: chiêu cuối nện đất, cột sa thạch trồi ba nhịp
                case "n_vien_dam": return NVienDam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sơn Viên (HatTho.cs), đòn thường: liên hoàn ba đấm
                case "n_vien_chan": return NVienChan(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sơn Viên: nện đất, sóng chấn gai đá
                case "n_vien_tang": return NVienTang(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sơn Viên: chiêu cuối tụ tảng đá khổng lồ, bốn tay ném
'''
CASES2 = '''                case "n_giap_huc2": return NGiapHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thạch Giáp dạng 2 (HatTho.cs): lao húc nặng
                case "n_giap_soi2": return NGiapSoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thạch Giáp dạng 2: ba cụm pha lê của rig găm
                case "n_giap_mua2": return NGiapMua(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thạch Giáp dạng 2: mưa pha lê dày, mảnh to
                case "n_tich_dop2": return NTichDop(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Sa Tích dạng 2: chồm đớp nặng
                case "n_tich_phien2": return NTichPhien(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Sa Tích dạng 2: năm phiến mũ trùm găm
                case "n_tich_loc2": return NTichLoc(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Sa Tích dạng 2: đập đất hai lần, lốc cát lớn
                case "n_thiem_dam2": return NThiemDam2(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm dạng 2: lao đâm mũi khối pha lê
                case "n_thiem_phun2": return NThiemPhun(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Tê Thiềm dạng 2: ngả gầm, phun tảng đá lớn
                case "n_thiem_bo2": return NThiemBo2(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm dạng 2: nhảy tới bổ khối pha lê, cột pha lê
                case "n_long_vuot1": return NLongVuot(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.75f); // Sa Long dạng 1 (rồng non): vồ chém nhẹ
                case "n_long_luoi1": return NLongLuoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Sa Long dạng 1: hai lưỡi cát nhỏ
                case "n_long_cot1": return NLongCot1(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long dạng 1: nện đất, hai cột sa thạch
'''
MOC_CASE = '                default: return NVa(foeBody, foeFeet, tH);'

ATK_CU = 'kind == "n_soi_go";'
ATK_MOI = ('kind == "n_soi_go" ||\n            kind == "n_giap_huc" || kind == "n_tich_dop" || kind == "n_thiem_giang" || kind == "n_long_vuot" || kind == "n_vien_dam"; '
           '// bộ Thổ (HatTho.cs)')

BANG = '''        // bộ Thổ (2026-11-17; HatTho.cs, mã "n_" đi chung đường PlayNuoc): năm tướng đầu đảo Thổ vẽ lại trên rig Sword x Staff, mỗi tướng
        // một rig cho mọi dạng nên chiêu không đổi theo dạng. Tướng Thổ không có trong bảng: như cũ (tia cũ).
        static readonly Dictionary<string, (string mana, string ult)> ThoFx = new Dictionary<string, (string, string)>
        {
            { "thach_nhan", ("n_giap_soi", "n_giap_mua") }, // suất này nay là Thạch Giáp, tatu mai đá hổ phách (rig cong_da_1): lắc mai, ba viên sỏi của rig bay găm; chiêu cuối rụt mai gồng, pha lê vọt lên trời, mưa pha lê hổ phách, mảnh to cắm xuống
            { "lung_vuong", ("n_tich_phien", "n_tich_loc") }, // suất này nay là Sa Tích, thằn lằn áo choàng phiến đất nung (rig than_lan_cat_1): ba phiến áo choàng bay găm rồi về lắp; chiêu cuối dậm đất, lốc cát trùm đối thủ
            { "cao_da", ("n_thiem_phun", "n_thiem_lan") }, // suất này nay là Tê Thiềm, cóc tê giác đất nung (rig thu_da_1): há hàm hút đá, phun tảng đá; chiêu cuối cuộn tròn lăn nện (rig khai lunge cho skill)
            { "ho_khoan", ("n_long_luoi", "n_long_cot") }, // suất này nay là Sa Long, rồng giáp sa thạch (rig rong_cat_1): ba nhát vuốt phóng ba lưỡi cát trăng khuyết; chiêu cuối nện đất, vết nứt, cột sa thạch trồi ba nhịp
            { "phu_van", ("n_vien_chan", "n_vien_tang") }, // suất này nay là Sơn Viên, vượn núi đá bốn tay (rig quy_nui_1): nện đất, sóng chấn gai đá; chiêu cuối tụ tảng đá khổng lồ trên tay phụ, bốn tay ném
        };

        // đòn đánh thường của tướng Thổ có hiệu ứng riêng (HatLua.AtkLao nhận thì phát cả khi lao tới)
        static readonly Dictionary<string, string> ThoAtk = new Dictionary<string, string>
        {
            { "thach_nhan", "n_giap_huc" }, // Thạch Giáp: lao húc đầu: chớp, dăm đá, bụi
            { "lung_vuong", "n_tich_dop" }, // Sa Tích: chồm đớp: vết cắn hai cung kem, dăm cát
            { "cao_da", "n_thiem_giang" }, // Tê Thiềm: chồm giáng sừng: vòng bụi, dăm đá
            { "ho_khoan", "n_long_vuot" }, // Sa Long: lao chém vuốt: ba vệt vuốt, dăm cát
            { "phu_van", "n_vien_dam" }, // Sơn Viên: lao tới liên hoàn ba đấm, cú cuối có vòng bụi
        };

'''
BANG_DAU = '        // bộ Thổ (2026-11-17; HatTho.cs'
BANG2 = '''        // bộ Thổ (2026-11-17; HatTho.cs, mã "n_" đi chung đường PlayNuoc): tướng đầu đảo Thổ vẽ lại trên rig Sword x Staff; chiêu mana, chiêu
        // cuối và đòn thường theo từng DẠNG (dạng 1, 2 là hai rig khác nhau: quai/doi_tho5_dang2.py). Tướng Thổ không có trong bảng: như cũ.
        static readonly Dictionary<string, (string[] mana, string[] ult)> ThoFx = new Dictionary<string, (string[], string[])>
        {
            { "thach_nhan", (new[] { "n_giap_soi", "n_giap_soi2" }, new[] { "n_giap_mua", "n_giap_mua2" }) }, // Thạch Giáp Nhi (rig cong_da_1) / Thạch Giáp (cong_da_2): lắc mai, sỏi / ba cụm pha lê của rig bay găm; chiêu cuối pha lê vọt lên trời, mưa pha lê hổ phách (dạng 2 dày hơn, mảnh to hơn)
            { "lung_vuong", (new[] { "n_tich_phien", "n_tich_phien2" }, new[] { "n_tich_loc", "n_tich_loc2" }) }, // Sa Tích Nhi (than_lan_cat_1) / Sa Tích (than_lan_cat_2): ba / năm phiến đất nung bay găm rồi về lắp; chiêu cuối dậm (dạng 2 đập hai lần), lốc cát trùm đối thủ
            { "cao_da", (new[] { "n_thiem_phun", "n_thiem_phun2" }, new[] { "n_thiem_lan", "n_thiem_bo2" }) }, // Tê Thiềm Nhi (thu_da_1) / Tê Thiềm (thu_da_2): há hàm hút đá, phun tảng đá; chiêu cuối cuộn tròn lăn nện / nhảy tới bổ khối pha lê (cả hai rig khai lunge cho skill)
            { "ho_khoan", (new[] { "n_long_luoi1", "n_long_luoi" }, new[] { "n_long_cot1", "n_long_cot" }) }, // Sa Long Nhi (rong_cat_non) / Sa Long (rong_cat_1): hai / ba lưỡi cát trăng khuyết; chiêu cuối nện đất, vết nứt, hai / ba cột sa thạch
            { "phu_van", (new[] { "n_vien_chan" }, new[] { "n_vien_tang" }) }, // Sơn Viên (rig quy_nui_1, cả hai dạng): nện đất, sóng chấn gai đá; chiêu cuối tụ tảng đá khổng lồ trên tay phụ, bốn tay ném
        };

        // đòn đánh thường của tướng Thổ theo DẠNG (HatLua.AtkLao nhận thì phát cả khi lao tới)
        static readonly Dictionary<string, string[]> ThoAtk = new Dictionary<string, string[]>
        {
            { "thach_nhan", new[] { "n_giap_huc", "n_giap_huc2" } }, // Thạch Giáp: lao húc đầu: chớp, dăm đá, bụi (dạng 2 nặng hơn, vòng bụi)
            { "lung_vuong", new[] { "n_tich_dop", "n_tich_dop2" } }, // Sa Tích: chồm đớp: vết cắn hai cung kem, dăm cát
            { "cao_da", new[] { "n_thiem_giang", "n_thiem_dam2" } }, // Tê Thiềm: chồm giáng sừng / lao đâm mũi khối pha lê
            { "ho_khoan", new[] { "n_long_vuot1", "n_long_vuot" } }, // Sa Long: lao chém vuốt: ba vệt vuốt, dăm cát (dạng 1 nhẹ hơn)
            { "phu_van", new[] { "n_vien_dam" } }, // Sơn Viên: lao tới liên hoàn ba đấm, cú cuối có vòng bụi
        };

'''
# nhánh Elem.Tho: bản một-mã (đợt 1) → bản theo dạng (đợt 2)
SUA_SV2 = [
    ('            h.elem == Elem.Tho && ThoAtk.TryGetValue(h.id, out var o) ? o : null;',
     '            h.elem == Elem.Tho && ThoAtk.TryGetValue(h.id, out var o) && o.Length > 0 ? o[Mathf.Clamp(form, 0, o.Length - 1)] : null;'),
    ('            if (h.elem == Elem.Tho) return ThoFx.TryGetValue(h.id, out var o) ? o.mana : null;',
     '            if (h.elem == Elem.Tho) return ThoFx.TryGetValue(h.id, out var o) && o.mana.Length > 0 ? o.mana[Mathf.Clamp(form, 0, o.mana.Length - 1)] : null;'),
    ('            if (h.elem == Elem.Tho && ThoFx.TryGetValue(h.id, out var o)) return o.ult;',
     '            if (h.elem == Elem.Tho && ThoFx.TryGetValue(h.id, out var o) && o.ult.Length > 0) return o.ult[Mathf.Clamp(form, 0, o.ult.Length - 1)];'),
]
ATK2_CU = 'kind == "n_vien_dam"; // bộ Thổ (HatTho.cs)'
ATK2_MOI = ('kind == "n_vien_dam" ||\n            kind == "n_giap_huc2" || kind == "n_tich_dop2" || kind == "n_thiem_dam2" || kind == "n_long_vuot1"; '
            '// bộ Thổ (HatTho.cs; dạng 2, dạng 1 Sa Long)')
MOC_BANG = '        // đòn đánh thường theo DẠNG (bảng đo trên rig mỗi dạng một khác): ưu tiên hơn các bảng trên'

SUA_SV = [
    # FireAtk
    ('h.elem == Elem.Hoa && HoaAtk.TryGetValue(h.id, out var f) ? f : h.elem == Elem.Kim && KimAtk.TryGetValue(h.id, out var g) ? g : null;',
     'h.elem == Elem.Hoa && HoaAtk.TryGetValue(h.id, out var f) ? f : h.elem == Elem.Kim && KimAtk.TryGetValue(h.id, out var g) ? g :\n'
     '            h.elem == Elem.Tho && ThoAtk.TryGetValue(h.id, out var o) ? o : null;'),
    # FireMana
    ('            if (h.elem == Elem.Kim) return KimFx.TryGetValue(h.id, out var k) && k.mana.Length > 0 ? k.mana[Mathf.Clamp(form, 0, k.mana.Length - 1)] : null;\n',
     '            if (h.elem == Elem.Kim) return KimFx.TryGetValue(h.id, out var k) && k.mana.Length > 0 ? k.mana[Mathf.Clamp(form, 0, k.mana.Length - 1)] : null;\n'
     '            if (h.elem == Elem.Tho) return ThoFx.TryGetValue(h.id, out var o) ? o.mana : null;\n'),
    # FireUlt
    ('            if (h.elem == Elem.Kim && KimFx.TryGetValue(h.id, out var k) && k.ult.Length > 0)\n                return k.ult[Mathf.Clamp(form, 0, k.ult.Length - 1)];\n',
     '            if (h.elem == Elem.Kim && KimFx.TryGetValue(h.id, out var k) && k.ult.Length > 0)\n                return k.ult[Mathf.Clamp(form, 0, k.ult.Length - 1)];\n'
     '            if (h.elem == Elem.Tho && ThoFx.TryGetValue(h.id, out var o)) return o.ult;\n'),
]


def doc(p):
    return open(p, "rb").read().decode("utf-8")


def ghi(ten, cu, moi):
    doi = cu != moi
    print(f"  {ten}: " + ("đổi" if doi else "đã đúng") + (" (chỉ kiểm)" if KIEM and doi else ""))
    if not doi or KIEM:
        return
    q = os.path.join(RA or BAT, ten)
    open(q, "wb").write(moi.encode("utf-8"))


def lam():
    if RA:
        os.makedirs(RA, exist_ok=True)
    # HatTho.cs
    src = doc(os.path.join(HERE, "HatTho.cs"))
    q = os.path.join(BAT, "HatTho.cs")
    ghi("HatTho.cs", doc(q) if os.path.exists(q) and not RA else "", src.replace("\n", "\r\n") if "\r\n" in doc(os.path.join(BAT, "HatKhoang.cs")) else src)
    # HatNuoc.cs
    t = doc(os.path.join(BAT, "HatNuoc.cs"))
    nl = "\r\n" if "\r\n" in t else "\n"
    m = t
    if '"n_giap_huc"' not in m:
        assert MOC_CASE in m, "HatNuoc: không thấy default của PlayNuoc"
        m = m.replace(MOC_CASE, CASES.replace("\n", nl) + MOC_CASE, 1)
    if '"n_giap_huc2"' not in m:
        m = m.replace(MOC_CASE, CASES2.replace("\n", nl) + MOC_CASE, 1)
    ghi("HatNuoc.cs", t, m)
    # HatVoi.cs
    t = doc(os.path.join(BAT, "HatVoi.cs"))
    nl = "\r\n" if "\r\n" in t else "\n"
    m = t
    if '"n_giap_huc"' not in m:
        assert m.count(ATK_CU) == 1, "HatVoi: AtkLao đã đổi dạng"
        m = m.replace(ATK_CU, ATK_MOI.replace("\n", nl), 1)
    if '"n_giap_huc2"' not in m:
        assert m.count(ATK2_CU) == 1, "HatVoi: AtkLao Thổ đã đổi dạng"
        m = m.replace(ATK2_CU, ATK2_MOI.replace("\n", nl), 1)
    ghi("HatVoi.cs", t, m)
    # StageView.cs (phiên khác hay sửa: --khong-sv để chừa lại, đọc lại file ngay lúc chèn)
    if "--khong-sv" in sys.argv:
        print("  StageView.cs: chừa lại (--khong-sv)")
        return
    t = doc(os.path.join(BAT, "StageView.cs"))
    nl = "\r\n" if "\r\n" in t else "\n"
    m = t
    if "ThoFx" not in m:
        assert MOC_BANG in m, "StageView: không thấy bảng AtkDang"
        m = m.replace(MOC_BANG, BANG.replace("\n", nl) + MOC_BANG, 1)
        for a, b in SUA_SV:
            a2, b2 = a.replace("\n", nl), b.replace("\n", nl)
            assert m.count(a2) == 1, "StageView: " + a[:70]
            m = m.replace(a2, b2, 1)
    if "(string mana, string ult)> ThoFx" in m:                # đợt 1 → đợt 2: bảng theo dạng
        a0 = m.index(BANG_DAU)
        a1 = m.index(MOC_BANG)
        assert a0 < a1, "StageView: khối bảng Thổ không nằm ngay trên AtkDang"
        m = m[:a0] + BANG2.replace("\n", nl) + m[a1:]
        for a, b in SUA_SV2:
            assert m.count(a) == 1, "StageView: " + a[:70]
            m = m.replace(a, b, 1)
    ghi("StageView.cs", t, m)


if __name__ == "__main__":
    lam()
