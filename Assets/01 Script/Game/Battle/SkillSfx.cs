// TIẾNG CHIÊU (2026-11-24; người dùng: "tìm sound cho các skill đánh nhau trong game (nổ, tụ tia năng lượng, chém, húc,...)", rồi "bạn tự
// chọn, nếu không hợp thì gen"). Tiếng ở Assets/03 Art/Audio/Sfx/tran_*.ogg (gói CC0 + vài tiếng gen Magnific, nguồn ở ArtGen/Sfx/tran/
// NGUON.md, xuất bằng ArtGen/Sfx/xuat_tieng_tran.py), nạp bằng menu "PokiClash/Âm thanh/Nạp nhạc và tiếng".
// Không rải lệnh phát tiếng vào từng hàm hạt: StageView gọi một chỗ ở các điểm điều phối chiêu (PreFx, UltFx, FireBeam) với mã chiêu và
// giờ tới lúc trúng; bảng dưới chọn TIẾNG RA CHIÊU (phát ngay) và TIẾNG TRÚNG (hẹn đúng giờ trúng) theo chữ trong mã chiêu — các bảng
// FireFx / WaterFx / MocFx / KimFx / ThoFx đặt tên theo động tác (cau = cầu, tia / phun = tia, loc / xoay = lốc, song = sóng, gam = gầm,
// ten / kim / nem / ban = đạn bay, chem / kiem / vuot = chém, huc / dam / dap = húc nện, gai / thach = đá) — rồi tiếng trúng theo hệ.
// Đòn thường không qua đây: AudioService.Hit ("hit" / "hitCrit", nay là tiếng đấm thật). Vào chiêu cuối: "ult" (tụ năng lượng).
using PokiClash.Core;

namespace PokiClash
{
    public static class SkillSfx
    {
        // tiếng trúng mặc định theo hệ
        static string ElemHit(Elem e) =>
            e == Elem.Hoa ? "fx_no_nho" : e == Elem.Thuy ? "fx_nuoc" : e == Elem.Kim ? "fx_kim" : e == Elem.Tho ? "fx_da" : e == Elem.Moc ? "fx_chem2" : "fx_huc";

        // so theo TỪNG CHỮ của mã (tách "_", bỏ số đuôi dạng: "huc2" → "huc"); chữ có "_" (vd. "ho_anh") thì so chuỗi con
        static bool Has(string k, params string[] words)
        {
            var toks = k.Split('_');
            foreach (var w in words)
            {
                if (w.IndexOf('_') >= 0)
                {
                    if (k.Contains(w)) return true;
                    continue;
                }
                foreach (var t in toks)
                    if (t.TrimEnd('0', '1', '2', '3', '4', '5', '6', '7', '8', '9') == w) return true;
            }
            return false;
        }

        // (tiếng lúc ra chiêu, tiếng lúc trúng); null = không phát
        public static (string start, string hit) For(string kind, Elem elem)
        {
            if (string.IsNullOrEmpty(kind)) return (null, null);
            string k = kind.StartsWith("n_") ? kind.Substring(2) : kind;
            if (k.Length == 0 || k == "stay") return (null, ElemHit(elem));
            if (elem == Elem.Thuy) // bộ Thủy (StageView.WaterFx): mã ngắn, gán thẳng
                switch (k)
                {
                    case "tia": return ("fx_tia_nuoc", "fx_nuoc");
                    case "va": return (null, "fx_nuoc_lon");
                    case "cau": return ("fx_bong", "fx_nuoc_lon");
                    case "ngoc":
                    case "muc":
                    case "dan": return ("fx_bong", "fx_nuoc");
                    case "thuong": return ("whoosh", "fx_nuoc");
                    case "loc":
                    case "voi": return ("fx_loc", "fx_nuoc");
                    case "song": return ("fx_song", null);
                    case "mua": return (null, "fx_nuoc");
                    case "xoay": return ("fx_bong", "fx_nuoc_lon");
                    case "lien_dan": return ("fx_bong", "fx_nuoc");
                    case "bong_nay": return ("fx_bong", "fx_nuoc");
                    case "cau_nhot": return ("fx_bong", "fx_nuoc_lon");
                    case "bom": return ("fx_bong", "fx_nuoc_lon");
                    case "cau_xoay": return ("fx_bong", "fx_nuoc_lon");
                    case "mua_giong": return (null, "fx_nuoc_lon");
                    case "song_than": return ("fx_song", "fx_nuoc_lon");
                    case "thuy_xa": return ("fx_tia_nuoc", "fx_nuoc_lon");
                    case "cau_ma": return ("fx_tu", "fx_nuoc_lon");
                    case "xa_chem": return ("fx_chem", "fx_nuoc_lon");
                    case "bao_xoay":
                    case "bao_xoay1": return ("fx_loc", "fx_nuoc");
                    case "loat_cau": return ("fx_bong", "fx_nuoc");
                }
            if (Has(k, "gam")) return ("fx_gam", null);
            if (Has(k, "song")) return ("fx_song", null);
            if (Has(k, "loc", "voi", "xoay")) return ("fx_loc", ElemHit(elem));
            if (k == "phun_nham") return ("fx_da", "fx_no");
            if (Has(k, "phun")) return (elem == Elem.Hoa ? "fx_phun_lua" : "fx_tia_nuoc", ElemHit(elem));
            if (k == "no_lon" || k == "dao_lien") return ("fx_tu", "fx_no_lon");
            if (Has(k, "tia")) return ("fx_nha_tia", ElemHit(elem));
            if (Has(k, "cau")) return ("fx_tu", elem == Elem.Hoa ? "fx_no" : ElemHit(elem));
            if (Has(k, "ban", "dan")) return ("fx_nha_tia", ElemHit(elem));
            if (Has(k, "lua")) return ("fx_lua_bay", "fx_no_nho");
            if (Has(k, "ten", "kim", "thuong", "nem", "la")) return ("whoosh", ElemHit(elem));
            if (Has(k, "chem", "kiem", "vuot", "luoi", "ho_anh", "rut", "dao", "hon")) return ("fx_chem", elem == Elem.Kim ? "fx_kim" : "fx_chem2");
            if (Has(k, "huc", "dam", "dap", "nen", "va", "go", "quat", "dop", "tong", "ngoam", "nhat", "tang", "chan", "lien", "mieng", "an", "danh", "bo", "nga"))
                return ("whoosh", "fx_huc");
            if (Has(k, "nham", "trao")) return (null, "fx_no");
            if (Has(k, "gai", "tru", "re", "thach", "tinh", "da", "dat", "khoang", "roi", "cot", "troi")) return (null, "fx_da");
            if (Has(k, "mua")) return (null, ElemHit(elem));
            return (null, ElemHit(elem));
        }
    }
}
