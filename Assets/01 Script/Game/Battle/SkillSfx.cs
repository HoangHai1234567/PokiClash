// TIẾNG CHIÊU. Bản đầu 2026-11-24 (người dùng: "tìm sound cho các skill đánh nhau trong game (nổ, tụ tia năng lượng, chém, húc,...)", rồi "bạn
// tự chọn, nếu không hợp thì gen"): đoán tiếng theo CHỮ trong mã chiêu. Bản 2 2026-11-28 (người dùng: "quét kĩ lại phần combat và chiêu của
// từng tướng chưa có sound, có những sound đặc thù như tiếng hét, lốc, cầu lửa, va chạm, tiếng nước bắn, tiếng đất, tiếng tia laser từ mặt
// trời đâm xuống, thiên thạch va chạm, tiếng nổ"): BẢNG RIÊNG từng mã chiêu / đòn thường có hiệu ứng (StageView.FireFx / WaterFx / MocFx /
// KimFx / ThoFx / ...Atk), viết theo mô tả từng chiêu; luật đoán theo chữ chỉ còn là dự phòng cho mã chưa có trong bảng.
// Tiếng ở Assets/03 Art/Audio/Sfx/tran_*.ogg (gói CC0 + tiếng gen Magnific; nguồn ArtGen/Sfx/tran/NGUON.md; xuất bằng ArtGen/Sfx/
// xuat_tieng_tran.py và xuat_tieng_chieu.py), nạp bằng menu "PokiClash/Âm thanh/Nạp nhạc và tiếng".
// Không rải lệnh phát tiếng vào từng hàm hạt: StageView gọi một chỗ (StageViewTieng.cs) ở các điểm điều phối chiêu (PreFx, AtkFx, UltFx,
// FireBeam) với mã chiêu và giờ tới lúc trúng; các mốc trong bảng hẹn theo giờ sân (HatLua.At). Chiêu nhiều phát (đạn, thiên thạch, tên lửa,
// nhát chém liên hoàn) nghe từng cú nhờ "rep": mỗi cú rung màn (HatLua.Shake) / nhịp trúng (NuocPulse, DanhTrung, HoaTrung) sau lúc trúng
// phát một tiếng, cách nhau ≥ 0,1 s.
//
// CÚ PHÁP một dòng bảng (các mục cách nhau dấu cách):
//   tiếng@f      phát ở phần f của thời gian tới lúc trúng (0 = lúc gọi, 1 = lúc trúng); mã đi đường "n_" có mốc rig co theo giờ trúng
//                nên phần f đúng với mốc của clip (vd. thiên thạch thứ nhất của Nhật Vương ở 2,82 / 3,2 = 0,88)
//   tiếng+s      s giây sau lúc trúng          tiếng-s   s giây TRƯỚC lúc trúng (tiếng có đà: rít rơi, tia giáng — đỉnh nằm ở cuối đà)
//   rep:tiếng    mỗi cú trúng phụ sau lúc trúng     cast:tiếng  mỗi cú rung TRƯỚC lúc trúng (dậm, bắn pháo)
//   big:tiếng    cú rung mạnh (≥ bigmin) sau lúc trúng, một lần (nổ kết)   min:x  ngưỡng rung tính là cú trúng (mặc định 0,05)
//   bigmin:x     (mặc định 0,45)   win:s  sau lúc trúng còn nghe cú trúng phụ thêm s giây (mặc định 2)
// "whoosh" là tiếng vụt tổng hợp sẵn (BakedArt), các tiếng khác là khoá fx_* trong AudioImportMenu.
// Khoá bảng: mã bỏ "n_"; tra lần lượt "<id tướng>:<mã>", "<hệ>:<mã>", "<mã>", rồi mã bỏ số đuôi ("n_vua_tia1" → "vua_tia").
using System.Collections.Generic;
using System.Globalization;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash
{
    public static class SkillSfx
    {
        public struct Mark
        {
            public string snd;
            public int mode; // 0: phần của thời gian tới lúc trúng; 1: giây sau lúc trúng; 2: giây trước lúc trúng
            public float v;
        }

        public sealed class Cue
        {
            public readonly List<Mark> marks = new List<Mark>();
            public string rep, cast, big;
            public float min = 0.05f, bigMin = 0.45f, win = 2f;
        }

        // giờ (giây sân tính từ lúc gọi) của một mốc khi còn tHit giây tới lúc trúng
        public static float When(Mark m, float tHit) =>
            m.mode == 0 ? m.v * tHit : m.mode == 1 ? tHit + m.v : Mathf.Max(0, tHit - m.v);

        static readonly Dictionary<string, string> Bang = new Dictionary<string, string>
        {
            // ---------------------------------------------------------------- THỦY (WaterFx, WaterAtk)
            ["thuy:tia"] = "fx_tu@0 fx_tia_nuoc@.75 fx_nuoc_lon@1",                 // Thủy Pháo: dậm chân gầm, tia nước to
            ["thuy:va"] = "fx_nuoc_lon@1 fx_huc@1",                                  // lao tới / nhảy đè / quật đuôi: nước toé lúc chạm
            ["thuy:cau"] = "fx_bong@0 fx_nuoc_lon@1",
            ["thuy:dan"] = "fx_bong@0 fx_nuoc@1",                                    // đạn nước (đòn thường pháp sư nước)
            ["thuy:thuong"] = "whoosh@0 fx_nuoc@1",
            ["thuy:loc"] = "fx_loc@0 fx_nuoc@1 rep:fx_nuoc",                         // lốc xoáy nước lướt tới
            ["thuy:voi"] = "fx_gam@0 fx_loc@.35 fx_nuoc_lon@1 rep:fx_nuoc",          // Hải Long gầm: vòi rồng
            ["thuy:song"] = "fx_gam@0 fx_song@.5 fx_nuoc_lon@1",                     // Hải Long gầm: sóng thần
            ["thuy:mua"] = "fx_mua@.3 fx_nuoc@1 rep:fx_nuoc",
            ["thuy:xoay"] = "fx_gam@0 fx_loc@.4 fx_nuoc_lon@1 rep:fx_nuoc",          // Hải Long gầm: xoáy nước rồi mạch phun
            ["ngoc"] = "fx_bong@0 fx_nuoc_lon@1",                                    // sò phụt ngọc trai
            ["muc"] = "fx_bong@0 fx_bun@1 fx_nuoc@1",                                // bạch tuộc phụt bóng mực: toé nhớt
            ["lien_dan"] = "fx_bong@0 fx_nuoc@1 rep:fx_nuoc",                        // 5 viên đạn nước liên tiếp
            ["bong_nay"] = "fx_bong@0 fx_nuoc@1 rep:fx_bong",                        // 3 bong bóng nảy
            ["cau_nhot"] = "fx_bong@0 fx_nuoc_lon@1 rep:fx_nuoc_lon",               // cầu nước bọc đối thủ rồi vỡ
            ["bom"] = "fx_bong@0 fx_no_nho@1 fx_nuoc_lon@1",                         // bom nước bay vồng nổ cột nước
            ["cau_xoay"] = "fx_tu@0 fx_loc@.6 fx_nuoc_lon@1",                        // cầu xoáy từ đầu trượng
            ["mua_giong"] = "fx_loc@0 fx_mua@.35 fx_set@1 fx_nuoc_lon@1 rep:fx_nuoc big:fx_set win:3", // mây giông, mưa trút, thác dội, sét
            ["song_than"] = "fx_song@0 fx_nuoc_lon@1",
            ["cau_ma"] = "fx_tu@0 fx_phep@.5 fx_nuoc_lon@1 fx_no@1",                 // cầu ma thủy hiện ở thân đối thủ rồi nổ
            ["thuy_xa"] = "fx_tia_nuoc@0 fx_dop@1 fx_nuoc_lon@1",                    // rắn nước trườn tới ngoạm
            ["xa_chem"] = "fx_chem@0 fx_nuoc_lon@1 rep:fx_chem2",                    // ba nhát chém nước
            ["bao_xoay"] = "fx_loc@0 fx_gio@.5 fx_nuoc_lon@1 rep:fx_pha_le",        // siêu bão xoáy, mảnh băng bay vòng
            ["loat_cau"] = "fx_bong@0 fx_nuoc@1 rep:fx_nuoc",
            ["loat_tia"] = "fx_tu@0 fx_tia_nuoc@.8 fx_nuoc_lon@1 rep:fx_nha_tia",   // mỗi đầu rồng bắn một tia laser nước

            // ---------------------------------------------------------------- HỎA (FireFx, HoaUltDang, HoaAtk)
            ["hoa:cau"] = "fx_tu@0 fx_lua_bay@.6 fx_no@1",                           // cầu lửa mặc định
            ["tia_mat"] = "fx_nha_tia@0 fx_phun_lua@0 fx_no@1",                      // tia lửa từ con ngươi / mũi giáo
            ["quyen_xoay"] = "fx_loc@0 fx_lua_bay@0 fx_no_nho@1 rep:fx_no_nho big:fx_no", // lửa xoáy + chuỗi nổ theo nhịp đấm
            ["phun"] = "fx_phun_lua@0 fx_no_nho@1",
            ["cau_lan"] = "fx_lua_bay@0 fx_dong_dat@.4 fx_no@1 fx_huc@1",            // cuộn thành cầu lửa lăn tông
            ["ten"] = "whoosh@0 fx_no_nho@1 rep:fx_no_nho",                          // ba mũi tên lửa
            ["no_lon"] = "fx_tu@0 whoosh@.5 fx_no_lon@1 rep:fx_no",                  // kiếm bay tới / nổ lớn, nổ phụ
            ["phun_nham"] = "fx_dong_dat@0 fx_nham@1 fx_no@1 rep:fx_nham",          // dung nham phun dưới chân đối thủ
            ["kim_phap"] = "fx_lua_bay@0 whoosh@.7 fx_no_nho@1 rep:fx_no_nho",       // kim lửa quanh trượng rồi phóng
            ["cau_phap"] = "fx_tu@0 fx_lua_bay@.7 fx_no_lon@1",                      // cầu lửa phình to lao tới, nổ lớn
            ["dat_trao"] = "fx_huc@0 fx_dong_dat@0 fx_nham@1 fx_no_nho@1",           // bổ đao cắm đất, dung nham trào
            ["dao_lien"] = "fx_het@0 fx_chem@.6 fx_chem2@1 rep:fx_chem big:fx_no_lon", // lao tới chém liên hoàn, nổ lớn ở nhát bổ
            ["dat_dam"] = "fx_het@0 fx_chem2@1 rep:fx_chem big:fx_nham",             // đâm, chém liên hoàn, dung nham trào ở nhát kết
            ["ho_gam"] = "fx_gam_thu@0 fx_song_am@.45 fx_phun_lua@.6 fx_no_nho@1",   // hổ gầm: sóng xung kích + sóng nhiệt
            ["ho_anh"] = "fx_bien_mat@0 fx_chem@1 rep:fx_chem big:fx_no_lon win:3",  // tan biến, lướt chém nhiều lượt, sẹo lửa nổ
            ["nui_cau"] = "fx_tu@0 fx_lua_bay@.75 fx_no@1",                          // há mồm tụ cầu lửa rồi bắn
            ["nui_ten"] = "fx_dong_dat@0 fx_ten_lua@.3 fx_ten_lua@.55 fx_no_nho@1 rep:fx_no_nho big:fx_no win:3", // đạn tầm nhiệt từ ống núi lửa
            ["cau_rua"] = "fx_tu@0 fx_lua_bay@.75 fx_no@1",                          // rùa tụ cầu lửa ở mõm rồi bắn
            ["cau_sung"] = "fx_tu@0 fx_lua_bay@.8 fx_no_lon@1",                      // lửa trên lưng hút vào cầu trên sừng, phóng
            ["nham_va"] = "fx_da_vo@1 fx_no_nho@1",                                  // đòn thường: vả từ trên xuống, dăm đá tro
            ["ho_va"] = "fx_chem2@1 fx_no_nho@1",                                    // đòn thường: vả, ba vệt vuốt lửa
            ["nui_huc"] = "fx_da_vo@1 fx_nham@1",                                    // đòn thường: húc, dăm bazan, giọt dung nham

            // ---------------------------------------------------------------- MỘC (MocFx, MocAtk)
            ["la"] = "fx_la@0 fx_chem2@1 rep:fx_la",                                 // phun lá
            ["la_va"] = "fx_huc@1 fx_la@1",                                          // húc: lá vỡ tung lúc chạm
            ["gai"] = "fx_dong_dat@0 fx_da_vo@1 rep:fx_da_vo",                       // gai trồi từ đất tới chân đối thủ
            ["gai_va"] = "whoosh@0 fx_huc@1 fx_da_vo@1",                             // quả cầu gai xoay tông vào
            ["long_vuot:gai_va"] = "fx_la@0 fx_roi@1 rep:fx_roi",                    // người cây: dây gai quật rồi trói
            ["da_va"] = "whoosh@0 fx_da_lon@1 rep:fx_da_vo",                         // hai tảng tay bay tới nện
            ["cau_la"] = "fx_tu@0 fx_gio@.4 fx_no_nho@1 fx_la@1",                    // tụ cầu gió + lá rồi ném
            ["voi_phun"] = "fx_gio@0 fx_la@.3 fx_chem2@1 rep:fx_la",                 // vòi phụt hạt cây + lá
            ["dam_rung"] = "cast:fx_da_lon fx_dong_dat@.2 fx_da_vo@1 fx_la@1 rep:fx_da_vo", // dậm chân, sóng đất, rễ và cột lá trồi
            ["cau_tia"] = "fx_tu@0 fx_nha_tia@.85 fx_la@1",                          // tụ cầu giữa hai gạc rồi bắn tia
            ["cau_mom"] = "fx_tu@0 fx_no@1 fx_huc@1",                                // tụ cầu to trước mõm, gật đầu nện
            ["la_gam"] = "fx_gio@0 fx_la@.4 fx_chem2@1 rep:fx_chem2",                // quạt cánh, lá cánh GĂM vào đối thủ (không phải "gầm")
            ["thach_roi"] = "fx_gio@0 fx_thien_thach_roi-0.72 fx_da_lon@1 fx_dong_dat@1", // gọi tảng đá rơi từ trời
            ["rong_gam"] = "fx_gam@0 fx_song_am@.5 fx_huc@1 rep:fx_huc",             // rồng trúc gầm: các đợt sóng âm
            ["rong_van"] = "fx_gio@0 fx_la@.3 fx_chem2@1 rep:fx_chem2 big:fx_set bigmin:0.4 win:3.5", // Vạn Diệp: bão lá chém, măng đâm, sét kết
            ["giac_tia"] = "fx_tu@0 fx_nha_tia@.85 fx_no_nho@1",                     // tụ cầu ở đỉnh sừng, cúi đầu bắn tia
            ["giac_tim"] = "fx_tu@0 fx_nha_tia@.9 fx_no_lon@1",                      // mở ngực, tim bắn tia lớn
            ["kiem_rut"] = "fx_gio@0 fx_chem@.8 fx_chem2@1 rep:fx_chem2",            // lướt tới rút kiếm chém, bổ nhát hai
            ["kiem_ao"] = "fx_bien_mat@0 fx_chem@1 rep:fx_chem big:fx_no win:3",     // biến mất, ảo ảnh chém, tra kiếm vết nổ lại
            ["hat_nga"] = "fx_huc@1 fx_la@1",                                        // đòn thường voi: nện + hất ngà
            ["rong_dam"] = "fx_dong_dat@0 fx_set@1",                                 // đòn thường rồng: dậm, địa chấn, sét giáng
            ["giac_dam"] = "fx_dong_dat@0 fx_da_vo@1",                               // đòn thường: dậm, đất nứt chạy tới
            ["mo_dam"] = "fx_chem2@1",                                               // đòn thường chim: lao tới đâm mỏ

            // ---------------------------------------------------------------- KIM (KimFx, KimAtk, AtkDang)
            ["sat_ban"] = "fx_phep@0 fx_pha_le@1 rep:fx_pha_le big:fx_kim",          // tinh thể sắt lần lượt găm
            ["sat_dap"] = "fx_da_lon@1 fx_pha_le@1 rep:fx_pha_le",                   // nhảy dập, vòng cột tinh thể trồi rồi vỡ
            ["khoang_ban"] = "whoosh@.5 fx_da_vo@1 rep:fx_da_vo",                    // tay quặng bay găm, nổ dăm quặng
            ["khoang_dao"] = "fx_dong_dat@0 fx_da_lon@1 fx_huc@1 rep:fx_pha_le",     // ĐÀO đất chạy ngầm, trồi húc (không phải "đao")
            ["giao_nem"] = "fx_chem@.5 fx_kim@1 fx_no_nho@1",                        // ném giáo, giáo găm nổ
            ["kim_sat"] = "fx_phep@0 cast:fx_bua fx_kim@1 rep:fx_kim",               // gọi kim sắt, dậm giáo, kim lao găm
            ["cua_quat"] = "fx_cua@.45 fx_kim@1",                                    // lao tới quật đuôi cưa máy
            ["cua_lien"] = "fx_may_no@0 fx_cua@.75 fx_kim@1 fx_cua+0.6 rep:fx_kim win:3", // giật dây máy nổ, ghì cưa nhiều nhát
            ["hon_goi"] = "fx_hon@0 fx_hon@.6 fx_chem2@1 rep:fx_chem2",              // gọi hồn đồng đội lao tới đánh
            ["hon_kiem"] = "fx_hon@0 fx_tu@.4 fx_chem@.9 fx_no_lon@1",               // vá kiếm bằng hồn, bổ, nổ hồn lớn
            ["xich_nem"] = "fx_xich@0 fx_xich@.6 fx_kim@1 fx_xich+0.3",              // quay xích, ném móc găm, giật về
            ["xich_lua"] = "fx_xich@0 fx_lua_bay@.3 fx_xich@.8 fx_phun_lua@1 fx_no@1 rep:fx_no_nho win:3", // xích lửa, trói, cột lửa
            ["soi_nem"] = "whoosh@.5 fx_bua@1 whoosh+0.3",                           // ném búa xoáy, trúng, bay về tay
            ["soi_huc"] = "fx_het@0 fx_gio@.45 fx_huc@1 fx_bua@1",                   // che khiên tụ gió, lao xé gió, húc
            ["robot_cau"] = "fx_tu@0 fx_dien@.6 fx_no_nam@1",                        // cầu năng lượng to ném xuống, nổ rất lớn
            ["robot_ten"] = "fx_ten_lua@.2 fx_ten_lua@.4 fx_no@1 rep:fx_no_nho big:fx_no_lon win:3", // 7 tên lửa tầm nhiệt
            ["phao_mua"] = "cast:fx_phao fx_ten_lua@.6 fx_no_nho@1 rep:fx_no_nho big:fx_no win:3",    // 5 quả lên trời, tách tên lửa nhỏ
            ["phao_cau"] = "fx_tu@0 fx_phao@.95 fx_no_lon@1 fx_dien+0.2",            // gồng tụ cầu ở họng pháo, bắn, giật điện
            ["vua_tia"] = "fx_tu@0 fx_phep@.4 fx_tia_troi-0.88 fx_no+0.08",          // hành tinh xếp cột, tia Mặt Trời giáng xuống
            // nhật thực (2,0 / 3,2), ba thiên thạch nện ở 2,82 / 2,96 / 3,2 giây rig (lead 3,2): cú cuối nổ rất lớn
            ["vua_nhat"] = "fx_gio@0 fx_tu@.3 fx_phep@.62 fx_thien_thach_roi@.66 fx_thien_thach@.88 fx_thien_thach@.925 fx_no_nam@1",
            ["sat_tong"] = "fx_pha_le@1 fx_huc@1",                                   // đòn thường: tông, dăm tinh thể
            ["khoang_huc"] = "fx_huc@1 fx_da_vo@1 rep:fx_da_lon",                    // đòn thường: húc (dạng 2 lộn giáng)
            ["giao_dam"] = "fx_kim@1 fx_chem2@1",                                    // đòn thường: đâm giáo
            ["cua_huc"] = "fx_cua@.4 fx_kim@1",                                      // đòn thường: húc, tia lửa cưa
            ["hon_chem"] = "fx_hon@.5 fx_chem2@1",                                   // đòn thường: bổ kiếm, vệt lửa hồn
            ["xich_go"] = "fx_xich@.4 fx_bua@1",                                     // đòn thường: gõ móc xích lên đầu
            ["soi_go"] = "fx_bua@1 fx_da_vo@1",                                      // đòn thường: búa bổ nện
            ["robot_ban"] = "fx_tu@0 fx_nha_tia@.85 fx_no_nho@1",                    // đòn thường: tụ cầu ở nắm đấm rồi bắn
            ["phao_ban"] = "cast:fx_phao fx_no@1",                                   // đòn thường: bắn đạn sắt vòng cung, nổ lửa
            ["vua_an"] = "cast:fx_da_lon fx_lua_bay@.6 fx_no@1",                     // đòn thường: nện trượng, đường lửa, ấn nổ

            // ---------------------------------------------------------------- THỔ (ThoFx, ThoAtk)
            ["giap_soi"] = "whoosh@.6 fx_da_vo@1 rep:fx_da_vo",                      // sỏi găm
            ["giap_soi2"] = "whoosh@.6 fx_pha_le@1 rep:fx_pha_le",                   // cụm pha lê găm
            ["giap_mua"] = "fx_phep@0 fx_pha_le@1 rep:fx_pha_le win:2.5",            // mưa pha lê hổ phách
            ["tich_phien"] = "whoosh@.5 fx_da_vo@1 rep:fx_da_vo",                    // phiến đất nung bay găm
            ["tich_loc"] = "cast:fx_da_lon fx_loc@.3 fx_da_vo@1 rep:fx_da_vo",       // dậm, lốc cát trùm đối thủ
            ["thiem_phun"] = "fx_gio@0 whoosh@.8 fx_da_lon@1",                       // há hàm hút đá, phun tảng đá
            ["thiem_phun2"] = "fx_gam_thu@0 whoosh@.8 fx_da_lon@1",                  // ngả gầm, phun tảng đá lớn
            ["thiem_lan"] = "fx_dong_dat@0 fx_da_lon@1 fx_huc@1",                    // cuộn tròn lăn nện
            ["thiem_bo2"] = "fx_het@0 whoosh@.6 fx_da_lon@1 fx_pha_le@1 rep:fx_pha_le", // nhảy bổ khối pha lê, cột pha lê
            ["long_luoi"] = "fx_gio@0 fx_chem@.6 fx_chem2@1 rep:fx_chem2",           // lưỡi cát trăng khuyết
            ["long_cot"] = "cast:fx_da_lon fx_dong_dat@.3 fx_da_vo@1 rep:fx_da_lon", // nện đất, cột sa thạch trồi từng nhịp
            ["vien_chan"] = "cast:fx_da_lon fx_dong_dat@.4 fx_da_vo@1 rep:fx_da_vo", // nện đất, sóng chấn gai đá
            ["vien_tang"] = "fx_het@0 fx_dong_dat@.2 whoosh@.85 fx_da_lon@1 fx_no@1", // tụ tảng đá khổng lồ, bốn tay ném
            ["re_troi"] = "cast:fx_da_lon fx_dong_dat@.3 fx_da_vo@1 fx_roi+0.15",    // rễ trồi dọc đất tới đối thủ rồi quấn
            ["tru_giang"] = "fx_la@0 fx_gio@.5 fx_da_lon@1 fx_dong_dat@1 rep:fx_da_vo", // cột khổng lồ giáng xuống, rễ trồi
            ["trung_gai"] = "cast:fx_da_lon fx_da_vo@1 rep:fx_da_vo",                // giáng đầu, gai đá trồi
            ["trung_mieng"] = "fx_da_vo@0 fx_dong_dat@.2 fx_da_lon@1 fx_dop@1",      // lặn, chạy ngầm, trồi ngoạm
            ["bun_troi"] = "fx_bun@0 fx_dong_dat@.3 fx_bun@1 fx_huc@1",              // nắm đấm bùn khổng lồ trồi
            ["bun_ngoam"] = "fx_dop@1 fx_nuot+0.3 rep:fx_da_vo big:fx_bun win:4",    // ngoạm nuốt, gai đâm, nhổ
            ["tinh_gai"] = "fx_gam@0 whoosh@.7 fx_da_vo@1 rep:fx_da_vo",             // Thổ Tinh gầm, lưỡi trăng lưng phóng
            // Thổ Tinh: thiên thạch bay (0,36 / 3,48 giây rig), bám (1,0), ép (2,15), tia nhiệt (3,40), nổ nấm (3,48 = lúc trúng)
            ["tinh_hang"] = "fx_gio@.1 fx_da_lon@.29 fx_dong_dat@.62 fx_tia_troi-0.96 fx_no_nam@1",
            ["thach_xoay"] = "fx_gio@.2 fx_lua_bay@.8 fx_thien_thach@1 rep:fx_da_vo", // thiên thạch quay nhanh rồi lao vào đối thủ
            ["thach_cau"] = "fx_gio@.2 fx_thien_thach_roi-0.72 fx_thien_thach@1 fx_no_nam@1", // cuộn thành thiên thạch lao xuống, nổ rất lớn
            ["giap_huc"] = "fx_huc@1 fx_da_vo@1",                                    // đòn thường: húc đầu
            ["giap_huc2"] = "fx_huc@1 fx_da_lon@1",
            ["tich_dop"] = "fx_dop@1",                                               // đòn thường: chồm đớp
            ["tich_dop2"] = "fx_dop@1 fx_huc@1",
            ["thiem_giang"] = "fx_huc@1 fx_da_vo@1",                                 // đòn thường: giáng sừng
            ["thiem_dam2"] = "fx_pha_le@1 fx_huc@1",                                 // đòn thường: đâm mũi khối pha lê
            ["tho:long_vuot"] = "fx_chem2@1",                                        // đòn thường Sa Long: chém vuốt
            ["vien_dam"] = "fx_huc@1 rep:fx_huc",                                    // đòn thường: liên hoàn ba đấm
            ["vuong_huc"] = "fx_huc@1 fx_da_vo@1",
            ["tru_dap"] = "fx_da_lon@1",                                             // đòn thường: đập cột xuống đầu
            ["trung_dop"] = "fx_dop@1 rep:fx_dop",                                   // đòn thường: đớp nghiền hai nhịp
            ["bun_danh"] = "fx_bun@1 fx_huc@1",                                      // đòn thường: tay bùn đấm
            ["thach_vo"] = "fx_da_vo@1 fx_huc@1",
            ["tinh_nen"] = "fx_da_lon@1 fx_dong_dat@1",                              // đòn thường: nhảy nện hai nắm đấm
        };

        static readonly Dictionary<string, Cue> cache = new Dictionary<string, Cue>();

        // null = không phát gì
        public static Cue Get(string kind, Elem elem, string heroId)
        {
            if (string.IsNullOrEmpty(kind)) return null;
            string k = kind.StartsWith("n_") ? kind.Substring(2) : kind;
            if (k.Length == 0) return null;
            string e = elem.ToString().ToLowerInvariant();
            string bare = k.TrimEnd('0', '1', '2', '3', '4', '5', '6', '7', '8', '9');
            string key = null;
            foreach (var c in new[] { heroId + ":" + k, e + ":" + k, k, heroId + ":" + bare, e + ":" + bare, bare })
                if (Bang.ContainsKey(c))
                {
                    key = c;
                    break;
                }
            string cacheKey = key ?? ("?" + e + ":" + k);
            if (cache.TryGetValue(cacheKey, out var cue)) return cue;
            cue = key != null ? Parse(Bang[key]) : Guess(k, elem);
            cache[cacheKey] = cue;
            return cue;
        }

        static Cue Parse(string s)
        {
            var c = new Cue();
            foreach (var tok in s.Split(' '))
            {
                if (tok.Length == 0) continue;
                int colon = tok.IndexOf(':');
                if (colon > 0)
                {
                    string name = tok.Substring(0, colon), val = tok.Substring(colon + 1);
                    switch (name)
                    {
                        case "rep": c.rep = val; break;
                        case "cast": c.cast = val; break;
                        case "big": c.big = val; break;
                        case "min": c.min = F(val); break;
                        case "bigmin": c.bigMin = F(val); break;
                        case "win": c.win = F(val); break;
                    }
                    continue;
                }
                int p = tok.IndexOfAny(new[] { '@', '+', '-' });
                if (p <= 0)
                {
                    c.marks.Add(new Mark { snd = tok, mode = 0, v = 1 });
                    continue;
                }
                char op = tok[p];
                c.marks.Add(new Mark { snd = tok.Substring(0, p), mode = op == '@' ? 0 : op == '+' ? 1 : 2, v = F(tok.Substring(p + 1)) });
            }
            return c;
        }

        static float F(string v) => float.TryParse(v, NumberStyles.Float, CultureInfo.InvariantCulture, out var f) ? f : 0;

        // ------------------------------------------------ DỰ PHÒNG: mã chưa có trong bảng → đoán theo chữ (luật bản 2026-11-24)

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

        static Cue Guess(string k, Elem elem)
        {
            var (start, hit) = GuessPair(k, elem);
            var c = new Cue();
            if (start != null) c.marks.Add(new Mark { snd = start, mode = 0, v = 0 });
            if (hit != null) c.marks.Add(new Mark { snd = hit, mode = 0, v = 1 });
            return c;
        }

        static (string start, string hit) GuessPair(string k, Elem elem)
        {
            if (k == "stay") return (null, ElemHit(elem));
            if (Has(k, "gam")) return ("fx_gam", null);
            if (Has(k, "song")) return ("fx_song", null);
            if (Has(k, "loc", "voi", "xoay")) return ("fx_loc", ElemHit(elem));
            if (Has(k, "phun")) return (elem == Elem.Hoa ? "fx_phun_lua" : "fx_tia_nuoc", ElemHit(elem));
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
            return (null, ElemHit(elem));
        }
    }
}
