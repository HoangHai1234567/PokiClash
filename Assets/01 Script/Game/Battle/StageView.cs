// Sân đấu (chép Web/src/view/battle/stage.ts): nền theo hệ đảo (đảo có bộ sàn đấu thì theo ải, kèm phần động ArenaAnim), hai tướng dạng sticker, chữ tượng thanh, số sát thương, rung màn.
// Địch đứng trên trái, phe mình dưới phải (lật ngang). Toạ độ theo khung web 540 × 464, nhân 2 sang UI (1080 × 928).
// Tướng: prefab Items/TranTuong, hình là AolaSticker (Editor lúc Play, bản dev); không có aola thì ô trống (hình giữ chỗ vẽ tay
// đã bỏ 2026-11-02), Body vẫn chạy clip giả (lao tới 35% quãng đường) làm chỗ neo.
// Nằm trong prefab màn hình Screens/Battle; hiệu ứng (chữ nổi, tượng thanh, vòng, tia) là prefab mục, dùng xong thì tắt để dùng lại.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed class ClipHandle
    {
        public bool hit, done;
    }

    public sealed partial class StageView : MonoBehaviour // phần trình diễn (chết, ra sân, hồi sinh, boss tiến hóa): StageViewShow.cs
    {
        public const float SW = 540, SH = 464, K = 2;
        public static readonly Vector2[] Pos = { new Vector2(392, 418), new Vector2(158, 236) }; // phe mình, địch
        static readonly float[] Height = { 176, 150 };
        // cast: clip ngắn của chiêu bắn tia (tướng aola có khai, AolaSticker.Beam)
        public const string Idle = "idle", Hit = "hit", Attack = "attack", Skill = "skill", Cast = "cast";

        static readonly string[] WordsHit = { "BỐP!", "CHÁT!", "BỤP!", "HỰ!", "BINH!" };
        static readonly string[] WordsBig = { "ẦM!!", "RẦM!!", "OÀNH!!" };

        public float speed = 1; // nhịp sân ngoài lúc ra đòn: giây sân mỗi giây thật (BattleController đặt); animation tướng không theo
        public float fast = 1;  // công cụ thử chạy nhanh gấp fast, cả lúc ra đòn (BattleController.FastForward)
        [SerializeField] Image sky, bg, flashImg;
        [SerializeField] RectTransform root, actorLayer, fxLayer, plateLayer;
        [SerializeField] StageActor actorPrefab;
        [SerializeField] StageFx textFx, burstFx, ringFx, sparkFx;
        [SerializeField] StageFx beamFx; // tia nước của chiêu bắn (Items/TiaNuoc, menu "PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn")
        [SerializeField] StageFx imageFx; // ảnh hiệu ứng rời, đổi ảnh lúc dùng (Items/AnhHieuUng, cùng menu)
        [SerializeField] Sprite beamSplash, beamDrops, beamRipple, beamSparkle; // nổ nước, giọt, vòng sóng, lấp lánh (Assets/03 Art/Fx)
        // tia riêng của 3 boss cuối đảo Thủy (người dùng dặn 2026-11-07): ảnh thân tia theo tên (anim.json "cast.tia": tia_bang,
        // tia_xoay, tia_trieu) và hiệu ứng phụ của từng kiểu (mảnh băng, vòng xoáy, vòng sóng âm); cùng menu gán
        [SerializeField] Sprite[] beamStyles;
        [SerializeField] Sprite beamShard, beamVortex, beamSoundRing;
        // hạt chồng lớp phẳng (HatLua, bộ Hỏa 2026-11-10): prefab Items/HatLua, ba lớp chứa (đất, sau tướng, trước tướng) và ảnh hạt
        // Assets/03 Art/Fx/Hat; gán bằng menu "PokiClash/Prefab/Sàn đấu: hạt lửa"
        [SerializeField] Image hatPrefab;
        [SerializeField] RectTransform hatFloor, hatBack, hatFront;
        [SerializeField] Sprite[] hatSprites;
        HatLua hat;
        int nuocTarget = 1; // phe bị trúng của lần PlayNuoc gần nhất (cho NuocPulse, DanhTrung)

        // một nhịp trúng phụ của chiêu đang chạy (tia dội, cú phụ): con bị trúng chớp trắng và giật lùi theo k (0..1)
        void FoePulse(float k)
        {
            var v = actors[nuocTarget];
            if (v != null)
            {
                v.flash = Mathf.Max(v.flash, 0.05f + 0.09f * k);
                NhunTrung(v, 0.03f + 0.045f * k, 0.42f + 0.38f * k);
            }
            Bump(nuocTarget, 2f + 3.5f * k);
        }

        // GAME JUICE lúc trúng đòn (người dùng 2026-11-19: "khi tướng bị ăn đòn thêm splash trắng và hơi nhún nhẹ (không phải anim nhún mà là
        // nhún bằng code, animation chạy bình thường)"): bóp cả gốc tướng (bè ngang, lùn xuống rồi nảy lại, tắt dần ~0,25 s) và một bông toé
        // trắng vẽ sẵn (khung "trung_trang") ở thân, lệch về phía kẻ đánh. Nhịp dội liên tục (tia, sóng) không phát bông quá 7 lần / giây.
        void NhunTrung(Actor a, float bienDo, float coToe)
        {
            if (a == null || a.dead > 0) return;
            float now = Time.unscaledTime;
            float conLai = a.nhunA * Mathf.Exp(-(now - a.nhunLuc) / 0.085f);
            a.nhunA = Mathf.Max(conLai, bienDo);
            a.nhunLuc = now;
            var hat = Hat;
            if (hat == null || coToe <= 0 || now - a.toeLuc < 0.14f) return;
            a.toeLuc = now;
            var than = Body(a.side);
            var veKeDanh = (Pos[1 - a.side] - Pos[a.side]).normalized;
            var cho = than + veKeDanh * (0.16f * a.H) + new Vector2(UnityEngine.Random.Range(-0.08f, 0.08f), UnityEngine.Random.Range(-0.1f, 0.05f)) * a.H;
            hat.Fb("trung_trang", cho, coToe * a.H, HatLua.Front, 60, 1.7f, UnityEngine.Random.Range(-35f, 35f), UnityEngine.Random.value < 0.5f);
        }

        HatLua Hat
        {
            get
            {
                if (hat == null && hatPrefab && hatFloor && hatBack && hatFront)
                    hat = new HatLua(hatPrefab, hatFloor, hatBack, hatFront, hatSprites)
                    {
                        Shake = v => trauma = Mathf.Min(1, trauma + v),
                        FlashScreen = c => Flash(c),
                        NegScreen = d => Neg(d),
                        // mỗi nhịp tia nước dội vào thân (HatNuoc.NTia, 0,24 s một nhịp): con bị trúng chớp trắng và giật lùi theo nhịp
                        // (người dùng 2026-11-18: tia phải có va chạm với địch, không chỉ giật một lần lúc chạm)
                        NuocPulse = k => FoePulse(k),
                        DanhTrung = (p, k) => FoePulse(k), // nhịp trúng của chiêu Mộc (tia, luồng lá, sóng âm, nổ cầu; HatMoc.cs)
                        HoaTrung = (p, k) => FoePulse(k), // nhịp trúng của chiêu Hỏa không qua PlayNuoc (tia mắt, phun, tên, dung nham, nổ lớn)
                    };
                return hat != null && hat.Ready ? hat : null;
            }
        }

        // chiêu mana và chiêu cuối theo dòng tướng hệ Hỏa (thử 2026-11-10; công thức ở skill pokiclash-fx-congthuc). Tướng Hỏa không
        // có trong bảng: chiêu mana là cầu lửa, chiêu cuối giữ nguyên clip.
        static readonly Dictionary<string, (string mana, string ult)> FireFx = new Dictionary<string, (string, string)>
        {
            { "hoa_nhan", ("tia_mat", "quyen_xoay") }, { "nham_than", ("phun", "n_cau_lan") }, { "kim_su", ("ten", "no_lon") },
            { "su_tu_lua", ("cau", "phun_nham") }, // Tiểu Quỷ Lava (2026-11-18): cầu lửa; chiêu cuối dung nham phun dưới chân đối thủ (trước chưa có dòng, chiêu cuối không có hạt nào)
            { "hong_lien", ("n_kim_phap", "n_cau_phap") }, // suất này nay là pháp sư lửa (Viêm Sư, 2026-11-14; HatPhap.cs, đi đường "n_"): kim lửa quanh đầu trượng rồi phóng; chiêu cuối cầu lửa của rig phình to, mốc ban_cau cầu hạt lao tới đối thủ (trước: "kim", "loc_xoay")
            { "giap_long", ("dat_trao", "no_lon") }, // suất này nay là quỷ lửa cầm đao (Viêm Đao, 2026-11-13): chiêu mana bổ đao cắm đất, dung nham trào dưới chân địch; chiêu cuối lao tới liên hoàn chém, nổ lớn ở nhát bổ kết (trước: "phun", "phun_nham")
            { "huyen_viem", ("n_dat_dam", "no_lon") }, // suất này nay là Viêm Dũng, chiến binh đất nung lõi dung nham (2026-11-14; HatDat.cs, đi đường "n_"): lao tới đâm rồi chém liên hoàn, dung nham trào ở nhát bổ kết; chiêu cuối năm kiếm của rig bay tới, nổ lớn (trước: "kim", "loc_xoay")
            { "hoa_tinh", ("n_ho_gam", "n_ho_anh") }, // suất này nay là Bạch Viêm Hổ (2026-11-14; HatHo.cs, đi đường "n_"): gầm tạo sóng xung kích + sóng nhiệt; chiêu cuối tan biến, màn âm bản, lướt chém để lại sẹo lửa rồi nổ (trước: "cau", "no_lon")
            { "lan_hoa", ("n_nui_cau", "n_nui_ten") }, // suất này nay là Hỏa Sơn Long, khủng long núi lửa (2026-11-15; HatNuiLua.cs, đi đường "n_"): há mồm tụ cầu lửa rồi bắn; chiêu cuối bẻ các ống núi lửa, bắn đạn tầm nhiệt
            { "nguu_quyen", ("n_cau_rua", "n_cau_sung") }, // suất này nay là rùa golem lửa (Hỏa Quy, 2026-11-13; HatRua.cs, đi đường "n_" để cầu tụ TRƯỚC khung nhả): tụ cầu lửa ở mõm rồi bắn; chiêu cuối lửa trên lưng bị hút vào cầu lửa trên mũi sừng, hất sừng phóng cầu
        };

        // chiêu cuối hệ Hỏa theo từng DẠNG (đè lên FireFx): Hỏa Quy dạng 1 (rùa non) chỉ có ba ngọn lửa và sừng mầm ngắn nên dùng bản nhẹ
        static readonly Dictionary<string, string[]> HoaUltDang = new Dictionary<string, string[]>
        {
            { "nguu_quyen", new[] { "n_cau_sung1", "n_cau_sung" } },
            { "hong_lien", new[] { "n_cau_phap1", "n_cau_phap" } }, // Viêm Đồng (dạng 1): trượng ngắn, cầu lửa nhỏ và ở chỗ khác dạng 2
            { "hoa_tinh", new[] { "n_ho_anh1", "n_ho_anh" } }, // Viêm Hổ Nhi (dạng 1): 6 lượt lướt thay vì 12
            { "lan_hoa", new[] { "n_nui_ten1", "n_nui_ten2", "n_nui_ten" } }, // Hỏa Sơn Nhi (dạng 1): 8 phát; Hỏa Sơn Thú (dạng 2): 12 phát; Hỏa Sơn Long: 16 phát
        };

        // bộ Thủy (2026-11-10, HatNuoc.cs): chiêu mana theo dòng tướng, chiêu cuối theo từng DẠNG, chọn cho khớp động tác clip CHIÊU
        // của dạng đó (beasts_cfg._REDESIGN): đạn xoay quanh người rồi phóng = thương nước, xoáy nhốt = vòi rồng, gọi mưa / vật rơi =
        // mưa rào, sóng lan trên đất = sóng thần, trồi lên dưới chân = xoáy nước rồi mạch phun, phun dòng = tia nước, loạt đạn = bong
        // bóng, lao tới (trượt, húc, liên hoàn) = cú va nước lúc chạm. Mã bắt đầu bằng "n_". Tướng Thủy không có trong bảng: tia cũ.
        static readonly Dictionary<string, (string mana, string[] ult)> WaterFx = new Dictionary<string, (string, string[])>
        {
            // lô 10 tướng mới đảo Thủy (2026-11-11): theo chiêu cast / skill từng dạng trong ArtGen/Spine/inbox/tm0*_ghichu.md (chiêu mana
            // một mã cho cả dòng: hai dạng khác kiểu thì lấy kiểu dạng 1). Bảng nháp cho bước VFX riêng, chưa xem trong trận
            { "ti_tach", ("n_tia", new[] { "n_va", "n_va" }) },                // há miệng bắn tia nước; chiêu cuối nhảy đè: nước toé lúc chạm
            { "thach_giai", ("n_tia", new[] { "n_cau", "n_cau" }) },           // suất này nay là dòng ếch xanh (2026-11-11): há miệng bắn tia nước; chiêu cuối ợ ra cầu nước
            { "ca_den", ("n_tia", new[] { "n_tia", "n_tia" }) },              // Vòi Nước (há miệng bắn tia); Thủy Pháo (dậm chân gầm, tia to hơn) ở cả hai dạng
            { "ha_ba", ("n_ngoc", new[] { "n_va", "n_va" }) },                 // suất này nay là dòng sò đột biến (2026-11-11): phồng lên phụt viên ngọc trai; chiêu cuối lè lưỡi lao tới quật: nước toé lúc chạm
            { "so_ngoc", ("n_muc", new[] { "n_va", "n_va" }) },                // suất này nay là dòng bạch tuộc quái vật (2026-11-12): phồng người phụt một quả bóng mực đen; chiêu cuối gọi bạch tuộc con (nằm trong rig, xương fly*) bò tới nhảy bổ vào địch: mực toé lúc chạm
            { "giong_bao", ("n_tia", new[] { "n_thuong", "n_thuong" }) },      // suất này nay là dòng pháp sư nước (2026-11-11): chĩa gậy bắn tia; chiêu cuối giơ gậy gọi kim nước, dậm gậy thì kim phóng đi
            { "lien_kinh", ("n_va", new[] { "n_tia", "n_tia" }) },             // suất này nay là dòng cá voi biến dị (2026-11-11): chiêu mana xoay người quật đuôi (nước toé lúc chạm); chiêu cuối há to phun luồng nước
            { "uyen_xa", ("n_tia", new[] { "n_va", "n_va" }) },                // suất này nay là dòng rắn nước có sừng (2026-11-11): há nhẹ miệng bắn tia nước; chiêu cuối lao tới, đuôi sừng quất chém liên tiếp: nước toé lúc chạm (vệt chém riêng chưa làm)
            { "han_ngac", ("n_loc", new[] { "n_song", "n_mua" }) },            // suất này nay là dòng rồng vây (2026-11-12): quạt cánh tạo lốc xoáy nước lướt tới địch; chiêu cuối chưa chốt, giữ sóng / mưa
            { "hai_long", ("n_tia", new[] { "n_song", "n_xoay", "n_voi" }) },  // phun nước từ các đầu; chiêu gầm ba dạng mạnh dần
        };

        // đòn đánh thường của tướng Thủy đứng yên bắn (rig khai "stay" cho clip attack): mã hạt nước của viên đạn. Tướng không có
        // trong bảng: không vẽ đạn (chỉ có hiệu ứng trúng ở đối thủ).
        static readonly Dictionary<string, string> WaterAtk = new Dictionary<string, string>
        {
            { "giong_bao", "n_dan" }, // pháp sư nước: chĩa gậy bắn một viên nước từ cầu nước đầu gậy
        };

        // đòn đánh thường của tướng Mộc có hiệu ứng riêng. Mã nào HatLua.AtkLao nhận thì phát cả khi tướng LAO tới (không cần rig khai "stay").
        static readonly Dictionary<string, string> MocAtk = new Dictionary<string, string>
        {
            { "phong_linh", "n_hat_nga" }, // Lâm Tượng (HatVoi.cs): bụi lúc chân sau đạp, lá tuột lại lúc bay, nện + hất ngà
            { "thanh_long", "n_rong_dam" }, // suất này nay là rồng trúc bốn cánh, boss cuối đảo Mộc (2026-11-13, HatRong.cs): dậm hai chân trước, địa chấn chạy tới, sét giáng vào đầu đối thủ
            { "moc_tinh", "n_giac_dam" }, // suất này nay là Giác Mộc, thú cổ thụ một sừng (2026-11-13, HatGiac.cs): co chân trước dậm xuống, đất nứt chạy tới đối thủ
            { "gio_loc", "n_mo_dam" }, // Linh Điểu (HatChim.cs): lao tới đâm mỏ: bụi bật, gió và lá tuột lại, chớp toé chỗ mỏ chạm
        };

        // bộ Mộc (2026-11-12, HatMoc.cs; mã cũng bắt đầu bằng "n_" nên đi chung đường với bộ Thủy): chiêu mana, chiêu cuối theo dạng.
        // Tướng Mộc không có trong bảng: như cũ (hiệu ứng trong clip hoặc tia cũ).
        static readonly Dictionary<string, (string mana, string[] ult)> MocFx = new Dictionary<string, (string, string[])>
        {
            { "mam_u", ("n_la", new[] { "n_la_va", "n_la_va", "n_la_va" }) }, // tinh linh rừng mập: há mồm phun lá; chiêu cuối phình bụng lao tới húc: lá vỡ tung lúc chạm
            { "tien_la", ("n_gai", new[] { "n_gai_va", "n_gai_va" }) }, // Cầu Gai: gồng, gai trồi từ đất tới chân đối thủ; chiêu cuối quả cầu gai xoay tông vào: gai gãy văng
            { "gac_da", ("n_da_va", new[] { "n_cau_la", "n_cau_la" }) }, // Gạc Đá (HatDa.cs): hai tảng tay bay tới nện, đá vụn văng; chiêu cuối tụ cầu năng lượng (gió, lá bị hút vào) rồi ném
            { "phong_linh", ("n_voi_phun", new[] { "n_dam_rung1", "n_dam_rung" }) }, // Lâm Tượng (HatVoi.cs): vòi phụt hạt cây + lá; chiêu cuối dậm chân, sóng đất, rễ và cột lá trồi
            { "bom_la", ("n_cau_tia", new[] { "n_cau_mom1", "n_cau_mom" }) }, // Lộc Phong (HatLoc.cs): tụ cầu nhỏ giữa hai gạc rồi bắn tia; chiêu cuối dựng người há mồm tụ cầu to rồi gật đầu nện
            { "gio_loc", ("n_la_gam", new[] { "n_thach_roi1", "n_thach_roi" }) }, // Linh Điểu (HatChim.cs): quạt cánh, lá cánh bay găm vào đối thủ rồi về cánh (lá là mảnh của rig, xương fly_*); chiêu cuối gọi tảng đá rơi từ trời xuống đầu đối thủ (dạng 1 tảng nhỏ hơn). 2026-11-17 suất bị Cổ Vương đè nhầm, trả lại 2026-11-19
            { "long_vuot", ("n_gai_va", new[] { "n_la_va", "n_la_va" }) }, // suất này nay là dòng người cây đầm lầy (2026-11-12): giơ tay gọi dây gai quật rồi trói (dây gai là mảnh của rig, xương far): gai gãy văng lúc quật trúng; chiêu cuối tụ quả cầu dây leo (mảnh của rig) rồi nhảy tới nện: lá vỡ tung lúc chạm
            { "thanh_long", ("n_rong_gam", new[] { "n_rong_van", "n_rong_van", "n_rong_van" }) }, // rồng trúc bốn cánh (HatRong.cs): gầm, các đợt sóng âm lao tới, rung màn; chiêu cuối Vạn Diệp: kén cánh bung, bão lá chém, rừng măng trúc đâm lên, sét kết liễu
            { "moc_tinh", ("n_giac_tia", new[] { "n_giac_tim", "n_giac_tim" }) }, // Giác Mộc (HatGiac.cs): ngẩng lên tụ cầu ở đỉnh sừng rồi cúi xuống bắn tia; chiêu cuối mở vỏ ngực, quả tim rực sáng bắn tia lớn
            { "tho_hoang", ("n_kiem_rut", new[] { "n_kiem_ao" }) }, // suất này nay là Voọc Tướng, voọc kiếm sĩ giáp lá (2026-11-12, HatKiem.cs): cúi giữ thế lướt tới rồi rút kiếm chém (rig khai lunge cho cast); chiêu cuối biến mất, bốn ảo ảnh (mảnh của rig, xương far) chém để lại sẹo, tra kiếm thì các vết nổ lại
        };

        // đòn đánh thường của tướng Hỏa có hiệu ứng riêng (mã "n_" đi đường PlayNuoc, phát từ đầu clip; HatLua.AtkLao nhận thì phát cả khi lao tới)
        static readonly Dictionary<string, string> HoaAtk = new Dictionary<string, string>
        {
            { "nham_than", "n_nham_va" }, // golem lõi lửa (HatNham.cs): lao tới vả từ trên xuống đầu: chớp toé, tia lửa, dăm đá tro, bụi bị ép ra
            { "hoa_tinh", "n_ho_va" }, // Bạch Viêm Hổ (HatHo.cs): lao tới vả, ba vệt vuốt lửa
            { "lan_hoa", "n_nui_huc" }, // Hỏa Sơn Long (HatNuiLua.cs): lao tới húc, dăm đá bazan và giọt dung nham văng
        };

        // bộ Kim (2026-11-16; mã "n_" đi chung đường PlayNuoc): chiêu mana VÀ chiêu cuối theo từng DẠNG (dạng 1, 2 khác số tinh thể).
        // Tướng Kim không có trong bảng: như cũ (hiệu ứng trong clip hoặc tia cũ).
        static readonly Dictionary<string, (string[] mana, string[] ult)> KimFx = new Dictionary<string, (string[], string[])>
        {
            { "bo_cap", (new[] { "n_sat_ban1", "n_sat_ban2" }, new[] { "n_sat_dap1", "n_sat_dap" }) }, // suất này nay là Thiết Tinh, tinh linh tinh thể sắt (HatSat.cs): tinh thể của rig xếp vòng cung trên đầu rồi lần lượt găm vào đối thủ (8 / 10 viên); chiêu cuối nhảy dập: vòng cột tinh thể trồi quanh đối thủ
            { "bo_ngua", (new[] { "n_khoang_ban1", "n_khoang_ban2" }, new[] { "n_khoang_dao1", "n_khoang_dao" }) }, // suất này nay là Thiết Khoáng, tinh linh quặng sắt chui đất (2026-11-16, rig quang_sat_<k>, HatKhoang.cs): hai tay quặng (dạng 2 thêm năm gai) bay găm vào đối thủ (mảnh của rig, xương fly_*, game lái): mỗi mảnh găm một cú nổ dăm quặng; chiêu cuối đất toé lúc cắm hố, đất hất sau gò chạy ngầm (rig khai lunge), đất nổ lúc trồi, húc từ dưới: chớp + vòng cột tinh thể (dạng 2 trồi húc hai lần)
            { "doc_giac", (new[] { "n_giao_nem1", "n_giao_nem" }, new[] { "n_kim_sat1", "n_kim_sat" }) }, // suất này nay là Thiết Vệ, chiến binh sắt khiên giáo (2026-11-16, HatGiao.cs): ném giáo (cây giáo là mảnh của rig, xương fly_0, game lái) rồi giáo mọc lại trong tay; chiêu cuối giơ giáo gọi kim sắt thành vòng cung trên đầu, dậm giáo xuống đất, kim lao găm vào đối thủ (7 / 11 kim)
            { "phi_thuong", (new[] { "n_cua_quat" }, new[] { "n_cua_lien" }) }, // suất này nay là Thiết Cưa, tinh linh đuôi máy cưa (2026-11-16, HatCua.cs): rig tự lao tới quật đuôi cưa (tia lửa cưa toé lúc trúng, không bắn tia nữa); chiêu cuối giật dây ba lần (khói, máy nổ), hút khí vào đĩa cưa, ghì cưa 11 nhát tia lửa
            { "tam_kiem", (new[] { "n_hon_goi1", "n_hon_goi" }, new[] { "n_hon_kiem1", "n_hon_kiem" }) }, // suất này nay là Vong Kỵ, kỵ sĩ cổ đại bị nguyền (2026-11-16, rig ky_nguyen_<k>, HatHon.cs): giơ kiếm lên trời gọi hồn đồng đội (hình mũ hồn xanh) lao tới đánh (3 / 5 hồn); chiêu cuối tay vuốt dọc lưỡi, phần vá hồn hiện theo tay (mặt nạ cắt của rig), khí hồn hút vào mép vá, giơ kiếm aura bùng, bổ: vệt lửa hồn theo mũi kiếm, nổ hồn lớn
            { "khien_bac", (new[] { "n_xich_nem1", "n_xich_nem" }, new[] { "n_xich_lua1", "n_xich_lua" }) }, // suất này nay là Quỷ Xích, quỷ béo móc xích (2026-11-16, HatXich.cs): quay xích qua đầu, ném móc (móc + xích là mảnh của rig, xương fly_*, game lái) găm rồi giật về; chiêu cuối xích bốc lửa quay để lại vệt lửa + khói, ném trói đối thủ (vòng xích), cột lửa rất to thiêu
            { "chien_than", (new[] { "n_soi_nem1", "n_soi_nem" }, new[] { "n_soi_huc1", "n_soi_huc" }) }, // suất này nay là Sói Giáp, sói chiến binh khiên búa (2026-11-16, rig soi_giap_<k>, HatSoi.cs): ném búa xoáy (búa là mảnh của rig, xương fly_0, game lái) trúng rồi bay về tay; chiêu cuối che khiên tụ gió, lao xé gió (rig khai lunge), húc
            { "thiet_phu", (new[] { "n_robot_cau1", "n_robot_cau" }, new[] { "n_robot_ten1", "n_robot_ten" }) }, // suất này nay là Thần Cơ, robot hủy diệt cổ đại (2026-11-16, rig robot_co_<k>, HatRobot.cs): hai tay giơ cao xoay lòng bàn tay tụ cầu năng lượng to rồi ném xuống đầu đối thủ, nổ rất lớn; chiêu cuối mở giáp ngực, 7 tên lửa tầm nhiệt bay đường cong ngẫu nhiên lao vào đối thủ, nổ lớn
            { "kim_nghe", (new[] { "n_vua_tia1", "n_vua_tia" }, new[] { "n_vua_nhat1", "n_vua_nhat" }) }, // suất này nay là Nhật Vương, vua robot quyền trượng Mặt Trời (2026-11-17, rig vua_may_<k>, HatVua.cs): ba hành tinh xếp cột trên đầu đối thủ, Mặt Trời lên đỉnh, tia giáng xuống, nổ mặt trời; chiêu cuối bay lên, nhật thực (màn tối), ba thiên thạch nện, cú cuối rất lớn
            { "ung_thep", (new[] { "n_phao_mua1", "n_phao_mua" }, new[] { "n_phao_cau1", "n_phao_cau" }) }, // suất này nay là Pháo Giáp, thú giáp pháo (2026-11-17, rig thu_phao_<k>, HatPhao.cs): nòng chĩa trời bắn liền 5 quả lên khỏi màn, trên đầu đối thủ mỗi quả tách thành 2 / 3 tên lửa nhỏ homing lao xuống; chiêu cuối gồng tụ cầu năng lượng rất lớn ở họng pháo, bắn, nổ lớn, giật điện
        };

        // đòn đánh thường của tướng Kim có hiệu ứng riêng (HatLua.AtkLao nhận thì phát cả khi lao tới)
        static readonly Dictionary<string, string> KimAtk = new Dictionary<string, string>
        {
            { "bo_cap", "n_sat_tong" }, // Thiết Tinh (HatSat.cs): lao tới tông, chớp + tia bạc + dăm tinh thể
            { "bo_ngua", "n_khoang_huc" }, // Thiết Khoáng (HatKhoang.cs): lao tới húc: chớp, dăm quặng, bụi; dạng 2 húc rồi lộn giáng xuống (khung trúng ở nhát giáng): sóng đất, đất toé
            { "doc_giac", "n_giao_dam" }, // Thiết Vệ (HatGiao.cs): lao tới đâm giáo: chớp sắt, tia bạc theo hướng đâm, dăm thép
            { "phi_thuong", "n_cua_huc" }, // Thiết Cưa (HatCua.cs): lao tới húc: chớp sắt, tia lửa, dăm thép, bụi
            { "tam_kiem", "n_hon_chem" }, // Vong Kỵ (HatHon.cs): lao tới, vung kiếm qua đầu bổ: vệt chém lửa hồn, chớp hồn, lưỡi lửa toé, mảnh giáp rỉ
            { "khien_bac", "n_xich_go" }, // Quỷ Xích (HatXich.cs): bay tới gõ móc lên đầu đối thủ: chớp sắt, tia, dăm thép, bụi lúc móc đập xuống
            { "chien_than", "n_soi_go" }, // Sói Giáp (HatSoi.cs): lao tới, búa bổ từ trên đầu xuống nện: vệt búa, chớp sắt, tia, dăm thép, sóng đất, bụi, sỏi
        };

        // bộ Thổ (2026-11-17; HatTho.cs, mã "n_" đi chung đường PlayNuoc): tướng đầu đảo Thổ vẽ lại trên rig Sword x Staff; chiêu mana, chiêu
        // cuối và đòn thường theo từng DẠNG (dạng 1, 2 là hai rig khác nhau: quai/doi_tho5_dang2.py). Tướng Thổ không có trong bảng: như cũ.
        static readonly Dictionary<string, (string[] mana, string[] ult)> ThoFx = new Dictionary<string, (string[], string[])>
        {
            { "thach_nhan", (new[] { "n_giap_soi", "n_giap_soi2" }, new[] { "n_giap_mua", "n_giap_mua2" }) }, // Thạch Giáp Nhi (rig cong_da_1) / Thạch Giáp (cong_da_2): lắc mai, sỏi / ba cụm pha lê của rig bay găm; chiêu cuối pha lê vọt lên trời, mưa pha lê hổ phách (dạng 2 dày hơn, mảnh to hơn)
            { "lung_vuong", (new[] { "n_tich_phien", "n_tich_phien2" }, new[] { "n_tich_loc", "n_tich_loc2" }) }, // Sa Tích Nhi (than_lan_cat_1) / Sa Tích (than_lan_cat_2): ba / năm phiến đất nung bay găm rồi về lắp; chiêu cuối dậm (dạng 2 đập hai lần), lốc cát trùm đối thủ
            { "cao_da", (new[] { "n_thiem_phun", "n_thiem_phun2" }, new[] { "n_thiem_lan", "n_thiem_bo2" }) }, // Tê Thiềm Nhi (thu_da_1) / Tê Thiềm (thu_da_2): há hàm hút đá, phun tảng đá; chiêu cuối cuộn tròn lăn nện / nhảy tới bổ khối pha lê (cả hai rig khai lunge cho skill)
            { "ho_khoan", (new[] { "n_long_luoi1", "n_long_luoi" }, new[] { "n_long_cot1", "n_long_cot" }) }, // Sa Long Nhi (rong_cat_non) / Sa Long (rong_cat_1): hai / ba lưỡi cát trăng khuyết; chiêu cuối nện đất, vết nứt, hai / ba cột sa thạch
            { "phu_van", (new[] { "n_vien_chan" }, new[] { "n_vien_tang" }) }, // Sơn Viên (rig quy_nui_1, cả hai dạng): nện đất, sóng chấn gai đá; chiêu cuối tụ tảng đá khổng lồ trên tay phụ, bốn tay ném
            { "hat_de", (new[] { "n_re_troi" }, new[] { "n_tru_giang1", "n_tru_giang" }) }, // suất này nay là Cổ Vương, tượng vua cổ rễ quấn cầm cột (2026-11-17, tướng 6 đảo Thổ; ghép nhầm vào gio_loc đảo Mộc, chuyển về đây 2026-11-19; HatCoVuong.cs, màu WThemes "hat_de"): cắm cột / nện tay, rễ trồi dọc đất tới đối thủ rồi quấn; chiêu cuối cột (mảnh của rig, xương fly_cot) giáng xuống đối thủ: dạng 1 cột nhỏ, dạng 2 cột khổng lồ rồi bay về tay
            { "rua_nui", (new[] { "n_trung_gai" }, new[] { "n_trung_mieng" }) }, // Sa Trùng (rig sau_dat_1, ải 40; dạng 1 tạm cùng rig): giáng đầu, ba gai đá đầu ngạnh; chiêu cuối lặn, gò đất chạy ngầm, trồi ngoạm
            { "ho_kim_cuong", (new[] { "n_bun_troi" }, new[] { "n_bun_ngoam" }) }, // suất này nay là Bùn Ngoạm, quái bùn (2026-11-17, rig quai_bun_1, ải 50, HatBun.cs): cắm tay xuống bùn, nắm đấm bùn khổng lồ của rig trồi dưới đối thủ; chiêu cuối lao ngoạm NUỐT đối thủ (StageViewNuot.cs giấu nó), thành quả bóng, 22 gai đâm xuyên, NHỔ nó bay về chỗ. Một dạng (thêm dạng 1 thì thêm mã vào mảng)
            { "cu_phu", (new[] { "n_thach_xoay1", "n_thach_xoay" }, new[] { "n_thach_cau1", "n_thach_cau" }) }, // suất này nay là Thiên Thạch Thú (HatThach.cs): Thiên Thạch Thú Non (rig tinh_hach_non, ba thiên thạch, quả cầu nhỏ) / Thiên Thạch Thú (tinh_hach_1, năm thiên thạch)
            { "giap_nham", (new[] { "n_tinh_gai1", "n_tinh_gai" }, new[] { "n_tinh_hang1", "n_tinh_hang" }) }, // suất này nay là Thổ Tinh, final boss ải 70 (HatThoTinh.cs): Tiểu Thổ Tinh (rig thach_de_non, sáu mảnh vỏ) / Thổ Tinh (thach_de_1, mười lưỡi trăng): gầm, mảnh lưng lần lượt phóng; chiêu cuối thiên thạch bọc đối thủ, ép co (StageViewThoTinh.cs), mặt trời, tia nhiệt, nổ nấm
        };

        // đòn đánh thường của tướng Thổ theo DẠNG (HatLua.AtkLao nhận thì phát cả khi lao tới)
        static readonly Dictionary<string, string[]> ThoAtk = new Dictionary<string, string[]>
        {
            { "thach_nhan", new[] { "n_giap_huc", "n_giap_huc2" } }, // Thạch Giáp: lao húc đầu: chớp, dăm đá, bụi (dạng 2 nặng hơn, vòng bụi)
            { "lung_vuong", new[] { "n_tich_dop", "n_tich_dop2" } }, // Sa Tích: chồm đớp: vết cắn hai cung kem, dăm cát
            { "cao_da", new[] { "n_thiem_giang", "n_thiem_dam2" } }, // Tê Thiềm: chồm giáng sừng / lao đâm mũi khối pha lê
            { "ho_khoan", new[] { "n_long_vuot1", "n_long_vuot" } }, // Sa Long: lao chém vuốt: ba vệt vuốt, dăm cát (dạng 1 nhẹ hơn)
            { "phu_van", new[] { "n_vien_dam" } }, // Sơn Viên: lao tới liên hoàn ba đấm, cú cuối có vòng bụi
            { "hat_de", new[] { "n_vuong_huc", "n_tru_dap" } }, // Cổ Vương Nhi / Cổ Vương (HatCoVuong.cs): lao húc chóp vương miện / lao tới đập cột xuống đầu đối thủ
            { "rua_nui", new[] { "n_trung_dop" } }, // Sa Trùng: đớp nghiền: vết cắn lớn, dăm đá, hai nhịp nghiến
            { "ho_kim_cuong", new[] { "n_bun_danh" } }, // Bùn Ngoạm (rig khai stay + far): tay bùn co giãn tới đấm đối thủ: giọt bùn rơi theo tay, toé bùn
            { "cu_phu", new[] { "n_thach_vo" } }, // Thiên Thạch Thú (HatThach.cs; phiên assets-3c)
            { "giap_nham", new[] { "n_tinh_nen1", "n_tinh_nen" } }, // Tiểu Thổ Tinh / Thổ Tinh (HatThoTinh.cs, rig khai lunge): nhảy lao tới nện hai nắm đấm: sao kem, dăm, nứt đất, đối thủ bẹp (StageViewThoTinh.cs)
        };

        // đòn đánh thường theo DẠNG (bảng đo trên rig mỗi dạng một khác): ưu tiên hơn các bảng trên
        static readonly Dictionary<string, string[]> AtkDang = new Dictionary<string, string[]>
        {
            { "thiet_phu", new[] { "n_robot_ban1", "n_robot_ban" } }, // Thần Cơ (HatRobot.cs): đứng giơ tay phải tụ cầu năng lượng ở ổ nắm đấm rồi bắn, tay giật lùi
            { "ung_thep", new[] { "n_phao_ban1", "n_phao_ban" } }, // Pháo Giáp (HatPhao.cs): đứng nâng nòng bắn một quả đạn sắt vòng cung, nổ lửa
            { "kim_nghe", new[] { "n_vua_an1", "n_vua_an" } }, // Nhật Vương (HatVua.cs): "Nhật Ấn", đứng vụt trượng nện đất, đường lửa chạy tới đối thủ, ấn + cột năng lượng
        };

        // form: dạng đang ra trận (0 là dạng đầu); chỉ tướng có trong AtkDang chọn theo dạng
        public static string FireAtk(HeroDef h, int form = 0) =>
            h != null && AtkDang.TryGetValue(h.id, out var ad) && ad.Length > 0 ? ad[Mathf.Clamp(form, 0, ad.Length - 1)] :
            h == null ? null : h.elem == Elem.Thuy && WaterAtk.TryGetValue(h.id, out var k) ? k : h.elem == Elem.Moc && MocAtk.TryGetValue(h.id, out var m) ? m :
            h.elem == Elem.Hoa && HoaAtk.TryGetValue(h.id, out var f) ? f : h.elem == Elem.Kim && KimAtk.TryGetValue(h.id, out var g) ? g :
            h.elem == Elem.Tho && ThoAtk.TryGetValue(h.id, out var o) && o.Length > 0 ? o[Mathf.Clamp(form, 0, o.Length - 1)] : null;

        // form: dạng đang ra trận (0 là dạng đầu); chỉ bộ Kim chọn chiêu mana theo dạng
        public static string FireMana(HeroDef h, int form = 0)
        {
            if (h == null) return null;
            if (h.elem == Elem.Hoa) return FireFx.TryGetValue(h.id, out var f) ? f.mana : "cau";
            if (h.elem == Elem.Moc) return MocFx.TryGetValue(h.id, out var m) ? m.mana : null;
            if (h.elem == Elem.Kim) return KimFx.TryGetValue(h.id, out var k) && k.mana.Length > 0 ? k.mana[Mathf.Clamp(form, 0, k.mana.Length - 1)] : null;
            if (h.elem == Elem.Tho) return ThoFx.TryGetValue(h.id, out var o) && o.mana.Length > 0 ? o.mana[Mathf.Clamp(form, 0, o.mana.Length - 1)] : null;
            return h.elem == Elem.Thuy && WaterFx.TryGetValue(h.id, out var w) ? w.mana : null;
        }

        // form: dạng đang ra trận (0 là dạng đầu); chỉ bộ Thủy chọn chiêu cuối theo dạng
        public static string FireUlt(HeroDef h, int form = 0)
        {
            if (h == null) return null;
            if (h.elem == Elem.Hoa)
                return HoaUltDang.TryGetValue(h.id, out var hd) ? hd[Mathf.Clamp(form, 0, hd.Length - 1)] : FireFx.TryGetValue(h.id, out var f) ? f.ult : null;
            if (h.elem == Elem.Thuy && WaterFx.TryGetValue(h.id, out var w) && w.ult.Length > 0)
                return w.ult[Mathf.Clamp(form, 0, w.ult.Length - 1)];
            if (h.elem == Elem.Moc && MocFx.TryGetValue(h.id, out var m) && m.ult.Length > 0)
                return m.ult[Mathf.Clamp(form, 0, m.ult.Length - 1)];
            if (h.elem == Elem.Kim && KimFx.TryGetValue(h.id, out var k) && k.ult.Length > 0)
                return k.ult[Mathf.Clamp(form, 0, k.ult.Length - 1)];
            if (h.elem == Elem.Tho && ThoFx.TryGetValue(h.id, out var o) && o.ult.Length > 0) return o.ult[Mathf.Clamp(form, 0, o.ult.Length - 1)];
            return null;
        }

        // chỗ bắn của tướng so với chân (đơn vị sân) và cỡ tia: dạng có clip bắn thì theo anim.json; không thì từ trước ngực
        Vector2 Muzzle(Actor a, int side, out float scale)
        {
            if (a.aola != null && a.aola.Beam(out var m, out scale)) return m;
            int other = side == 0 ? 1 : 0;
            var dir = Pos[other].x < Pos[side].x ? -1f : 1f;
            scale = a.forms <= 1 ? 1f : 0.7f + 0.7f * a.form / (a.forms - 1f);
            if (a.boss) scale *= 1.2f;
            return new Vector2(dir * a.H * 0.3f, -a.H * 0.5f);
        }

        // chiêu nước: phát ngay lúc clip bắn / clip CHIÊU BẮT ĐẦU, pha tụ nước chạy trong lúc tướng lấy đà và nước nhả đúng khung
        // trúng của clip; tướng giữ dáng nhả tới khi dòng nước, mưa, vòi rồng gần xong (người dùng 2026-11-10: animation khớp hiệu ứng)
        void PreFx(Actor a, int side, string clip)
        {
            a.fxHitAt = -1;
            if (clip == Attack)
            {
                AtkFx(a, side);
                return;
            }
            if (clip != Cast && clip != Skill) return;
            bool ult = clip == Skill;
            string kind = ult ? FireUlt(a.hero, a.form) : FireMana(a.hero, a.form);
            if (!HatLua.IsNuoc(kind) || HatLua.NuocAtHit(kind)) return;
            var h = Hat;
            if (h == null || !h.HasWater) return;
            int other = side == 0 ? 1 : 0;
            var victim = actors[other];
            float tH = victim != null ? victim.H : Height[other];
            float len = a.aola != null ? a.aola.Duration(clip) : ClipLen(clip);
            float lead = a.aola != null ? a.aola.HitTime(clip) : len * HitAt(clip);
            h.UseTheme(a.hero.id);
            nuocTarget = other;
            float t = h.PlayNuoc(kind, ult, Pos[side], a.H, Pos[side] + Muzzle(a, side, out _), Pos[other], Body(other), tH, lead);
            a.fxHitAt = Clock + t;
            a.holdAt = lead;
            a.holdUntil = Clock + lead + HatLua.HoldNuoc(kind, ult);
            skillHold = Mathf.Max(skillHold, t + 1.2f);
        }

        // đòn đánh thường bắn đạn nước (tướng đứng yên bắn): phát lúc clip bắt đầu; đạn rời chỗ nhả HatLua.DanTravel giây trước khung
        // trúng của clip nên chạm đối thủ đúng khung trúng (cảm giác trúng và số sát thương giữ nguyên chỗ)
        void AtkFx(Actor a, int side)
        {
            string kind = FireAtk(a.hero, a.form);
            if (kind == null || a.aola == null || (!a.aola.Stays(Attack) && !HatLua.AtkLao(kind))) return;
            var h = Hat;
            if (h == null || !h.HasWater) return;
            int other = side == 0 ? 1 : 0;
            var victim = actors[other];
            float tH = victim != null ? victim.H : Height[other];
            h.UseTheme(a.hero.id);
            nuocTarget = other;
            h.PlayNuoc(kind, false, Pos[side], a.H, Pos[side] + Muzzle(a, side, out _), Pos[other], Body(other), tH, a.aola.HitTime(Attack));
        }

        // chiêu cuối hệ Hỏa: gọi lúc trúng của clip CHIÊU; trả thời gian tới lúc hiệu ứng chạm đối thủ (giây sân), 0 nếu không có
        public float UltFx(int side)
        {
            var a = actors[side];
            string kind = a != null ? FireUlt(a.hero, a.form) : null;
            var h = Hat;
            if (kind == null || h == null) return 0;
            int other = side == 0 ? 1 : 0;
            var victim = actors[other];
            float tH = victim != null ? victim.H : Height[other];
            var feet = Pos[other];
            h.UseTheme(a.hero.id);
            if (HatLua.IsNuoc(kind))
            {
                if (HatLua.NuocAtHit(kind)) // chiêu lao tới: nước toé lúc chạm
                {
                    if (!h.HasWater) return 0;
                    nuocTarget = other;
                    h.PlayNuoc(kind, true, Pos[side], a.H, Pos[side], feet, Body(other), tH, 0);
                    skillHold = Mathf.Max(skillHold, 1.2f);
                    return 0;
                }
                float left = a.fxHitAt < 0 ? 0 : Mathf.Max(0, a.fxHitAt - Clock); // đã phát từ đầu clip (PreFx)
                a.fxHitAt = -1;
                return left;
            }
            nuocTarget = other;
            float t = h.PlayUlt(kind, feet, Body(other), tH, Mathf.Sign(Pos[side].x - feet.x));
            skillHold = Mathf.Max(skillHold, t + 0.8f);
            return t;
        }

        // chiêu mana hệ Hỏa thay tia nước; trả thời gian tới lúc trúng, âm nếu không làm
        float FireBeam(Actor a, int side, Vector2 from, Vector2 to)
        {
            string kind = FireMana(a.hero, a.form);
            if (HatLua.IsNuoc(kind)) // đã phát từ đầu clip (PreFx); chưa phát được (thiếu lớp hạt) thì bắn tia cũ
            {
                // chiêu mana KHÔNG có đạn (đòn do mảnh của rig quật: dây gai của người cây; hoặc tướng tự quật): hạt toé ở đối thủ đúng
                // khung trúng, như nhánh chiêu cuối trong UltFx. Trước 2026-11-12 nhánh này thiếu: PreFx bỏ qua mã "lúc chạm" nên
                // fxHitAt = -1, rơi xuống dưới và bắn tia cũ từ tay tướng sang đối thủ.
                if (HatLua.NuocAtHit(kind))
                {
                    var hh = Hat;
                    if (hh == null || !hh.HasWater) return -1;
                    int o = side == 0 ? 1 : 0;
                    var v = actors[o];
                    hh.UseTheme(a.hero.id);
                    nuocTarget = o;
                    hh.PlayNuoc(kind, false, Pos[side], a.H, Pos[side], Pos[o], Body(o), v != null ? v.H : Height[o], 0);
                    return 0;
                }
                if (a.fxHitAt < 0) return -1;
                float left = Mathf.Max(0, a.fxHitAt - Clock);
                a.fxHitAt = -1;
                return left;
            }
            var h = Hat;
            if (kind == null || h == null) return -1;
            int other = side == 0 ? 1 : 0;
            var victim = actors[other];
            float tH = victim != null ? victim.H : Height[other];
            h.UseTheme(a.hero.id);
            nuocTarget = other;
            float t = h.PlayMana(kind, Pos[side], a.H, from, Pos[other], to, tH);
            // người dùng dặn 2026-11-10: tướng đứng phun cho hết luồng lửa mới về đứng; kim, cầu cũng giữ dáng tới lúc phóng
            a.holdAt = a.t;
            a.holdUntil = Clock + HatLua.HoldOf(kind);
            skillHold = Mathf.Max(skillHold, t + 0.6f);
            return t;
        }
        public RectTransform PlateLayer => plateLayer;
        float flashT = -1, flashLife = 0.35f;
        float negT = -1, negLife;
        Material negMat;
        Color flashColor;
        // cảm giác trúng (skill pokiclash-hero-fx): clip .atomik khai impact* thì lúc trúng sân khựng, màn rung kiểu trauma, con bị
        // đánh bật lùi kèm nghiêng. Tướng không khai thì Hurt tự thêm mức tối thiểu (khựng ngắn, bật lùi nhẹ) theo độ mạnh của cú.
        float freeze, trauma;
        const float FreezeSlow = 0.06f, RecoilLen = 0.38f, TraumaDecay = 1.3f, TraumaX = 12, TraumaY = 8;
        // Đẩy màn có hướng (GameFeel mục 5 "camera bump"; 2026-11-16 thay rung ngẫu nhiên mỗi khung của đòn thường): cả sân dời theo
        // hướng cú đánh (từ kẻ đánh tới con bị trúng) rồi hồi mũ theo giờ thật (×0,85 mỗi khung 60 hình/giây ≈ λ 9,75/s).
        Vector2 bump;
        const float BumpDecay = 9.75f;
        float lastHurt = -9; // giờ thật của cú trúng trước: hai cú liền nhau trong 0,2 giây thì cú sau khựng một nửa

        // Độ "epic" của trận 0..1 (người dùng 2026-11-16: "tướng sau, độ khó cao hơn thì hiệu ứng combat, feeling càng phải epic hơn"):
        // BattleController đặt theo ải (ải sau trên đảo, đảo sau, bậc huy hiệu, tầng hang). Ải đầu gọn nhẹ, ải cuối khựng lâu hơn,
        // đẩy màn xa hơn, có rung, hạt nhiều và nhanh hơn, số to hơn, rung tay mạnh hơn.
        public float Epic;

        // độ mạnh cảm giác của một cú do tướng phe attacker gây ra: độ epic của trận + boss + dạng tiến hóa đang hiện, chặn 0..1
        public float Power(int attacker)
        {
            var a = attacker >= 0 && attacker < 2 ? actors[attacker] : null;
            float p = Epic;
            if (a != null)
            {
                if (a.boss) p += 0.25f;
                p += 0.1f * a.form;
            }
            return Mathf.Clamp01(p);
        }

        // đẩy màn theo hướng từ tướng phe kia tới tướng phe side, amount đơn vị sân (cú lớn không bị cú nhỏ cắt)
        public void Bump(int side, float amount)
        {
            var dir = (P(Pos[side]) - P(Pos[1 - side])).normalized;
            var v = dir * amount;
            if (v.sqrMagnitude > bump.sqrMagnitude) bump = v;
        }

        // cộng rung kiểu trauma (chặn ở 1)
        public void AddTrauma(float v) => trauma = Mathf.Min(1, trauma + v);

        // khựng sân s giây thật (lấy max, không cộng dồn, tối đa 0,2 giây)
        public void Freeze(float s) => freeze = Mathf.Max(freeze, Mathf.Min(0.2f, s));
        readonly Actor[] actors = new Actor[2];
        readonly List<Fx> fx = new List<Fx>();
        readonly Dictionary<StageFx, List<StageFx>> idle = new Dictionary<StageFx, List<StageFx>>(); // prefab → bản sao đang tắt

        sealed class Actor
        {
            public int side;
            public HeroDef hero;
            public bool boss;
            public StageActor view;
            public RectTransform rt, body, shadow, statusRt;
            public Image bodyImg, flashImg, emblem;
            public AolaSticker aola; // bản dev
            public string clip = Idle;
            public float t, flash, dead, enter = 9, exit, hop;
            public float holdAt, holdUntil; // chiêu phun: giữ dáng ở khung phun (giờ clip holdAt) tới giờ sân holdUntil rồi mới về đứng
            public float fxHitAt = -1; // chiêu nước phát từ đầu clip: giờ sân lúc nước trúng đối thủ (âm: không có)
            public float impactAt = -1; // cảm giác trúng dời tới giờ sân này (chiêu nước còn bay)
            public string impactClip;
            public float recoil = -1, push; // bật lùi do cú trúng có impact: giây sân đã qua (-1 = không), quãng theo chiều cao
            public float nhunLuc = -9, nhunA, toeLuc = -9; // nhún bằng code + bông toé trắng lúc trúng đòn (game juice 2026-11-19): giờ thật, biên độ
            public bool loop = true;
            public ClipHandle handle;
            public Action onHit;
            public bool hitFired = true;
            public List<(StatusId, int)> statuses = new List<(StatusId, int)>();
            public readonly List<RectTransform> statusIcons = new List<RectTransform>();
            public double size = 1; // cỡ của dạng đang hiện (theo sao)
            public int form, forms = 1; // dạng đang hiện trong dòng tiến hóa và số dạng (cỡ tia của chiêu bắn)
            public float H => Height[side] * (float)size * (boss ? 1.18f : 1);
        }

        sealed class Fx
        {
            public StageFx item, prefab;
            public RectTransform rt;
            public CanvasGroup cg;
            public float t, life;
            public Action<Fx, float> update; // (fx, k = t/life)
            public int side = -1;
            public float lift, size;
            public Vector2 basePos;
        }

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image skyImg, RectTransform shakeRoot, Image bgImg, RectTransform actorsRt, RectTransform fxRt, RectTransform platesRt,
            Image flash, StageActor actor, StageFx text, StageFx burst, StageFx ring, StageFx spark)
        {
            sky = skyImg;
            root = shakeRoot;
            bg = bgImg;
            actorLayer = actorsRt;
            fxLayer = fxRt;
            plateLayer = platesRt;
            flashImg = flash;
            actorPrefab = actor;
            textFx = text;
            burstFx = burst;
            ringFx = ring;
            sparkFx = spark;
        }

        // nền theo đảo: màu trời trên cùng phủ cả phần dôi (máy dài), rồi ảnh nền trận (FitBg: ảnh vẽ dư trời thì chìa lên phần dôi).
        // Đảo có bộ sàn đấu (ArtGen/BattleBG/build_thuy.py) thì theo ải: ải mini boss, boss "battle_<đảo>_s<ải>", rồi chặng
        // "battle_<đảo>_c<chặng>"; không có thì nền hệ. Sàn đấu có phần động (ArenaAnim) và màu trời riêng. stage null (thử thách huy
        // hiệu, hang): nền hệ.
        public void Init(ZoneDef zone, StageDef stage = null)
        {
            this.zone = zone;
            this.stage = stage;
            arenaArt = null;
            ApplyArena(1);
            flashImg.gameObject.SetActive(false);
            ResetShow(); // nền tối, pha trình diễn còn sót của trận trước (StageViewShow.cs)
        }

        // boss tiến hóa: nền dạng sau ("…_s70_2", "…_s70_3") nếu có
        public void SetPhase(int phase) => ApplyArena(phase);

        [SerializeField] ArenaAnim arena; // lớp "PhanDong" ngay trên ảnh nền (menu "PokiClash/Prefab/Sàn đấu: lớp phần động")
        ZoneDef zone;
        StageDef stage;
        string arenaArt;

        static string ArenaArt(ZoneDef zone, StageDef st, int phase)
        {
            string z = "battle_" + Keys.Of(zone.id);
            if (st == null || !App.Art) return z;
            string s = $"{z}_s{st.idx}";
            if (phase > 1 && HasArena($"{s}_{phase}")) return $"{s}_{phase}";
            if (HasArena(s)) return s;
            string c = $"{z}_c{st.chapter + 1:00}";
            return HasArena(c) ? c : z;
        }

        // nền có ảnh riêng, hoặc mượn ảnh nền khác: đảo Mộc dùng chung nền (ArtGen/BattleBG/build_moc.py), khoá trong arena_fx.json có
        // "use" (khoá nền có ảnh) và "tint" (màu phủ ảnh: ải mini boss, boss dạng 2, 3)
        static bool HasArena(string name) => App.Art.HasArt(name) || ArenaAnim.Use(name.Substring("battle_".Length)) != null;

        void ApplyArena(int phase)
        {
            string name = ArenaArt(zone, stage, phase);
            if (name == arenaArt) return;
            arenaArt = name;
            string key = name.Substring("battle_".Length);
            string use = ArenaAnim.Use(key);
            var art = App.Art ? App.Art.Get(use != null ? "battle_" + use : name) : null;
            Theme.SetSprite(bg, art);
            string tint = ArenaAnim.Tint(key);
            bg.color = art ? (tint != null ? Theme.Hex(tint) : Color.white) : Theme.Hex(zone.skyBottom);
            sky.color = Theme.Hex(ArenaAnim.Sky(key) ?? zone.skyTop);
            if (arena) arena.Bind(key);
            fitRoom = -1;
            FitBg();
        }

        // Máy dài hơn 9:16 thì vùng sân cao thêm phía trên khung 1080 × 928 (9:20 thêm 480, 21:9 thêm 600). Ảnh nền rộng 1080, cao theo
        // ảnh, đáy ảnh trùng đáy khung: ảnh cũ cao đúng 928 thì như trước (phần dôi là màu trời); ảnh vẽ dư trời (ArtGen/BattleBG/
        // build_troi.py, 1080 × 1528) thì phần trên chìa lên phủ phần dôi, máy thấp hơn cắt bớt từ trên (Image Filled, không méo).
        // Toạ độ tướng, phần động, bảng vẫn theo khung. Chớp sáng phủ cả vùng sân. Chừa thêm ShakePad cho mép trên khỏi hở lúc rung
        // (phần chừa nằm dưới thanh trên, thanh trên vẽ sau vùng sân).
        const float ShakePad = 16;
        float fitRoom = -1;

        void FitBg()
        {
            var area = transform.parent as RectTransform; // Vung san
            float room = (area ? area.rect.height : SH * K) + ShakePad;
            if (Mathf.Approximately(room, fitRoom)) return;
            fitRoom = room;
            float w = SW * K;
            var s = bg.sprite;
            float h = s ? w * s.rect.height / s.rect.width : SH * K;
            var rt = bg.rectTransform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0);
            rt.anchoredPosition = Vector2.zero;
            rt.sizeDelta = new Vector2(w, h);
            bg.type = Image.Type.Filled;
            bg.fillMethod = Image.FillMethod.Vertical;
            bg.fillOrigin = (int)Image.OriginVertical.Bottom;
            bg.fillAmount = Mathf.Min(1, room / h);
            var fr = flashImg.rectTransform;
            fr.anchorMin = Vector2.zero;
            fr.anchorMax = new Vector2(1, 0);
            fr.pivot = new Vector2(0.5f, 0);
            fr.anchoredPosition = Vector2.zero;
            fr.sizeDelta = new Vector2(0, Mathf.Max(room, SH * K));
        }

        // toạ độ web (gốc trên trái, y xuống) -> anchoredPosition trong khung sân (gốc trên trái)
        public static Vector2 P(float x, float y) => new Vector2(x * K, -y * K);
        public static Vector2 P(Vector2 p) => P(p.x, p.y);

        // ---------- tướng ----------

        // star: sao của tướng trên sân, chọn dạng trong dòng tiến hóa (hình và cỡ)
        public void SetActor(int side, HeroDef hero, bool boss, bool entering, int star = 1)
        {
            if (actors[side] != null)
            {
                actors[side].aola?.Destroy();
                Destroy(actors[side].rt.gameObject);
            }
            var form = App.Data.Cfg.FormOf(hero, star);
            var a = new Actor { side = side, hero = hero, size = form.size, boss = boss, enter = entering ? 0 : 9, t = Random.value * 2 };
            a.form = hero.FormIndex(App.Data.Cfg.formStars, star);
            a.forms = Mathf.Max(1, hero.forms.Length);
            var v = Ui.Spawn(actorPrefab, actorLayer);
            v.name = "tuong_" + side;
            a.view = v;
            a.rt = v.Rect;
            // bóng dưới chân
            a.shadow = v.Shadow.rectTransform;
            a.shadow.sizeDelta = new Vector2(92 * (float)a.size * (side == 0 ? 1.15f : 1) * K, 22 * (float)a.size * K);
            a.shadow.anchoredPosition = new Vector2(0, 2 * K);

            float h = a.H * K;
            a.aola = AolaSticker.TryCreate(a.rt, hero, form.aola, h, side == 0);
            v.Body.gameObject.SetActive(a.aola == null);
            if (a.aola == null)
            {
                // không có hình aola (bản build, tướng chưa xuất): ô trống. Hình giữ chỗ vẽ tay đã bỏ (2026-11-02); Body vẫn
                // là chỗ neo cho chuyển động, chỉ tắt ảnh.
                var body = v.Body;
                body.sizeDelta = new Vector2(h * HeroArt.W / HeroArt.H, h);
                body.localScale = new Vector3(side == 0 ? -1 : 1, 1, 1);
                a.body = body;
                a.bodyImg = v.BodyImg;
                a.emblem = v.Emblem;
                a.flashImg = v.Flash;
                a.bodyImg.enabled = a.emblem.enabled = a.flashImg.enabled = false;
            }
            else
            {
                a.body = a.aola.Rect;
                // ảnh aola nằm ngay trên bóng, dưới dấu trạng thái (như thứ tự dựng cũ)
                a.aola.Rect.SetSiblingIndex(v.Shadow.transform.GetSiblingIndex() + 1);
            }
            a.statusRt = v.Status;
            a.statusRt.anchoredPosition = new Vector2(0, h + 8 * K);
            v.HideStatuses();
            actors[side] = a;
            Place(a);
        }

        public float Retreat(int side)
        {
            var a = actors[side];
            if (a == null || a.dead > 0) return 0; // tướng đã gục (clip chết xong là trống): không cần lùi
            a.exit = 0.0001f;
            return RetreatLen; // giây animation; BattlePlayer chờ bằng WaitRetreat
        }

        public void SetStatuses(int side, List<(StatusId, int)> st)
        {
            var a = actors[side];
            if (a == null) return;
            bool same = a.statuses.Count == st.Count;
            for (int i = 0; same && i < st.Count; i++) same = a.statuses[i].Item1 == st[i].Item1;
            a.statuses = new List<(StatusId, int)>(st);
            if (!same) BuildStatusIcons(a);
        }

        // chạy clip; onHit gọi lúc trúng đòn; handle.done khi clip xong
        public ClipHandle Play(int side, string clip, Action onHit = null)
        {
            var a = actors[side];
            var h = new ClipHandle();
            if (a == null || a.dead > 0)
            {
                onHit?.Invoke();
                h.hit = true;
                StartCoroutine(DoneAfter(h, 0.3f));
                return h;
            }
            if (a.handle != null)
            {
                a.handle.hit = a.handle.done = true;
            }
            if (clip == Skill && arena) arena.Flare(); // sàn đấu bừng sáng theo chiêu, Tuyệt kỹ
            if (clip != Idle && clip != Hit) a.rt.SetAsLastSibling(); // con đang ra đòn nằm trên con kia
            a.clip = clip;
            a.t = 0;
            a.loop = false;
            a.onHit = onHit;
            a.hitFired = onHit == null;
            a.handle = h;
            PreFx(a, side, clip);
            if (onHit == null) h.hit = true;
            return h;
        }

        System.Collections.IEnumerator DoneAfter(ClipHandle h, float s)
        {
            yield return Wait(s);
            h.done = true;
        }

        // chờ s giây sân (theo nhịp lúc đó: đang ra đòn thì chậm cùng sân); sân tắt thì thôi chờ
        public System.Collections.IEnumerator Wait(float s)
        {
            float end = Clock + s;
            while (this && isActiveAndEnabled && Clock < end) yield return null;
        }

        // trúng đòn: chớp, đẩy màn có hướng, khựng ngắn, bật lùi (mức theo skill pokiclash-hero-fx mục 4, nhân theo Power của kẻ đánh).
        // dot: sát thương theo lượt (bỏng): chỉ chớp, đẩy nhẹ, không khựng, không bật lùi.
        public void Hurt(int side, bool big = false, bool dot = false)
        {
            var a = actors[side];
            if (a == null || a.dead > 0) return;
            a.flash = 0.16f;
            float pw = Power(1 - side);
            if (dot) NhunTrung(a, 0.03f, 0);
            else NhunTrung(a, big ? Mathf.Lerp(0.085f, 0.12f, pw) : Mathf.Lerp(0.055f, 0.08f, pw), big ? 0.95f : 0.7f);
            if (dot) Bump(side, 2.5f);
            else
            {
                Bump(side, big ? Mathf.Lerp(6.5f, 12, pw) : Mathf.Lerp(3.5f, 7, pw));
                // rung chỉ cho cú lớn; đòn thường chỉ rung khi trận đã khó (ải đầu chỉ đẩy màn)
                AddTrauma(big ? Mathf.Lerp(0.28f, 0.55f, pw) : 0.26f * pw * pw);
                float stop = big ? Mathf.Lerp(0.07f, 0.13f, pw) : Mathf.Lerp(0.035f, 0.07f, pw);
                if (Time.unscaledTime - lastHurt < 0.2f) stop *= 0.5f;
                lastHurt = Time.unscaledTime;
                Freeze(stop);
                // bật lùi tối thiểu khi rig không khai (đang bật lùi theo impact của rig thì giữ)
                if (a.recoil < 0)
                {
                    a.recoil = 0;
                    a.push = big ? Mathf.Lerp(0.08f, 0.14f, pw) : Mathf.Lerp(0.035f, 0.075f, pw);
                }
            }
            if ((a.clip == Idle || a.clip == Hit) && !Entering(a)) // đang diễn clip ra sân: chỉ chớp, bật lùi, không cắt clip
            {
                a.clip = Hit;
                a.t = 0;
                a.loop = false;
            }
        }

        // cú hạ gục (gọi ngay sau Hurt của cú đó): khựng dài hơn, rung, đẩy màn xa; last = con cuối của phe đó (hết trận) thì gần đứng
        // hình 0,2 giây, rung mạnh và chớp kem nhạt (GameFeel mục 6.15: dừng ngắn cho sự kiện cuối)
        public void KoHit(int side, bool last)
        {
            float pw = Power(1 - side);
            Freeze(last ? 0.2f : Mathf.Lerp(0.1f, 0.16f, pw));
            AddTrauma(last ? Mathf.Lerp(0.6f, 0.95f, pw) : Mathf.Lerp(0.3f, 0.55f, pw));
            Bump(side, last ? Mathf.Lerp(12, 18, pw) : Mathf.Lerp(8, 12, pw));
            if (last) Flash("#fff6c838");
        }

        public void Dodge(int side)
        {
            if (actors[side] != null) actors[side].hop = 0.0001f;
        }

        public void Die(int side)
        {
            if (actors[side] != null) actors[side].dead = 0.0001f;
        }

        public Vector2 Head(int side)
        {
            var p = Pos[side];
            float hh = actors[side] != null ? Height[side] * (float)actors[side].size : Height[side];
            return new Vector2(p.x, p.y - hh * 0.85f);
        }

        public Vector2 Body(int side)
        {
            var p = Pos[side];
            float hh = actors[side] != null ? Height[side] * (float)actors[side].size : Height[side];
            return new Vector2(p.x, p.y - hh * 0.45f);
        }

        // ---------- clip của hình giữ chỗ ----------

        static float ClipLen(string clip) => clip == Attack ? 0.8f : clip == Skill ? 0.9f : clip == Hit ? 0.36f :
            clip == Cast ? AolaSticker.CastLen : 1.2f;
        static float HitAt(string clip) => clip == Skill ? 0.55f : clip == Cast ? 0.5f : 0.6f;

        // ---------- hiệu ứng ----------

        // lấy một bản sao đang tắt của prefab (thiếu thì sinh), đặt lên trên cùng lớp hiệu ứng
        StageFx Take(StageFx prefab)
        {
            if (!idle.TryGetValue(prefab, out var list)) idle[prefab] = list = new List<StageFx>();
            StageFx f = null;
            while (list.Count > 0 && !f)
            {
                f = list[list.Count - 1];
                list.RemoveAt(list.Count - 1);
            }
            if (f) f.gameObject.SetActive(true);
            else f = Ui.Spawn(prefab, fxLayer);
            f.transform.SetAsLastSibling();
            return f;
        }

        void Release(Fx f)
        {
            if (!f.item) return;
            f.item.gameObject.SetActive(false);
            idle[f.prefab].Add(f.item);
        }

        Fx AddFx(StageFx item, StageFx prefab, float life, Action<Fx, float> update)
        {
            var f = new Fx { item = item, prefab = prefab, rt = item.Rect, life = life, update = update, cg = item.Group };
            f.cg.alpha = 1;
            f.cg.blocksRaycasts = false;
            f.basePos = f.rt.anchoredPosition;
            fx.Add(f);
            update(f, 0);
            return f;
        }

        StageFx FxText(string text, Color color, float size)
        {
            var f = Take(textFx);
            var t = f.Label;
            t.text = text;
            t.color = color;
            t.fontSize = size * K;
            t.rectTransform.sizeDelta = new Vector2(900, size * K * 1.4f);
            return f;
        }

        // dòng tin: chữ mới hiện ở chỗ cũ, chữ trước bị đẩy lên một dòng
        public void Text(int side, string text, Color color, float size = 26, float dy = 0)
        {
            var h = Head(side);
            foreach (var f in fx)
                if (f.side == side)
                    f.lift += size + 6;
            float sx = side == 1 ? Mathf.Min(h.x, 200) : Mathf.Max(h.x, 330);
            var item = FxText(text, color, size);
            var rt = item.Rect;
            rt.anchoredPosition = P(sx, h.y + dy + 20);
            float rot = (Random.value - 0.5f) * 0.08f * Mathf.Rad2Deg;
            rt.localEulerAngles = new Vector3(0, 0, -rot);
            var fxi = AddFx(item, textFx, 1.25f, (f, k) =>
            {
                float pop = k < 0.15f ? 0.5f + k / 0.15f * 0.7f : k < 0.25f ? 1.2f - (k - 0.15f) / 0.1f * 0.2f : 1;
                f.cg.alpha = k > 0.7f ? 1 - (k - 0.7f) / 0.3f : 1;
                f.rt.localScale = new Vector3(pop, pop, 1);
                f.rt.anchoredPosition = f.basePos + new Vector2(0, (18 * f.t + f.lift) * K);
            });
            fxi.side = side;
            fxi.size = size;
        }

        public void Text(int side, string text, string hex, float size = 26) => Text(side, text, Theme.Hex(hex), size);

        // số sát thương/hồi máu. Bật ra xa phía kẻ đánh (GameFeel mục 5 "bounce có hướng": chuyển động kể nguyên nhân) theo cung rồi
        // trôi lên; cú lớn bật từ nhỏ lên đỉnh cao hơn (0,3 → 1,45 → 1,1) và lắc ngang lúc đỉnh. Cỡ số nhỉnh theo Power của kẻ đánh.
        public void Number(int side, double n, Color color, bool big = false)
        {
            var b = Body(side);
            float pw = Power(1 - side);
            float size = (big ? 46 : 34) * (1 + 0.22f * pw);
            var item = FxText(NumFmt.Short(n), color, size); // số gọn: 93.5k (người dùng dặn 2026-11-17)
            var rt = item.Rect;
            var stack = NumberStack(side); // số liền nhau trên cùng một con: so le trái phải, nâng dần, không đè nhau
            rt.anchoredPosition = P(b.x + (Random.value - 0.5f) * 24 + stack.x, b.y - 10 - stack.y);
            rt.localEulerAngles = new Vector3(0, 0, (Random.value - 0.5f) * 0.3f * Mathf.Rad2Deg);
            // hướng bật: từ kẻ đánh tới con bị trúng (toạ độ UI), lệch ngẫu nhiên nhẹ
            var away = (P(Pos[side]) - P(Pos[1 - side])).normalized;
            float kick = (big ? 46 : 30) * (1 + 0.4f * pw) * Random.Range(0.85f, 1.15f);
            AddFx(item, textFx, 1f, (f, k) =>
            {
                float pop = big
                    ? (k < 0.12f ? Mathf.Lerp(0.3f, 1.45f, Out01(k / 0.12f)) : k < 0.24f ? Mathf.Lerp(1.45f, 1.1f, (k - 0.12f) / 0.12f) : 1.1f)
                    : (k < 0.15f ? 0.5f + k / 0.15f * 0.7f : k < 0.25f ? 1.2f - (k - 0.15f) / 0.1f * 0.2f : 1);
                f.cg.alpha = k > 0.7f ? 1 - (k - 0.7f) / 0.3f : 1;
                f.rt.localScale = new Vector3(pop, pop, 1);
                // bật ngang ra xa trong 0,25 giây đầu (ease-out), cộng trôi lên như cũ
                float out01 = Out01(Mathf.Min(1, f.t / 0.25f));
                var off = new Vector2(away.x * kick * out01 * K, 70 * f.t * K + Mathf.Max(0, away.y) * kick * 0.5f * out01 * K);
                if (big && k > 0.1f && k < 0.3f) off.x += Mathf.Sin(f.t * 90) * 3 * K * (0.3f - k) / 0.2f;
                f.rt.anchoredPosition = f.basePos + off;
            });
        }

        static float Out01(float k) => 1 - (1 - k) * (1 - k) * (1 - k);

        public void Burst(int side, bool big, string word = null)
        {
            var b = Body(side);
            var words = big ? WordsBig : WordsHit;
            word ??= Loc.T(words[Random.Range(0, words.Length)]);
            var item = Take(burstFx);
            item.Image.color = big ? Theme.Hex("#ffd24a") : Theme.Hex("#fff6c8");
            var rt = item.Rect;
            rt.sizeDelta = new Vector2(160 * K, 112 * K);
            rt.anchoredPosition = P(b.x + (Random.value - 0.5f) * 30, b.y - 20);
            rt.localEulerAngles = new Vector3(0, 0, (Random.value - 0.5f) * 0.5f * Mathf.Rad2Deg);
            item.Label.text = word;
            // trận càng khó, kẻ đánh càng mạnh: chữ to hơn, tia văng nhiều và xa hơn, cú lớn có vòng sóng (Power)
            float pw = Power(1 - side);
            float sz = (big ? 1.35f : 1) * (1 + 0.15f * pw);
            AddFx(item, burstFx, 0.6f, (f, k) =>
            {
                float pop = k < 0.2f ? 0.3f + k / 0.2f * 0.9f : 1.2f - Mathf.Min(0.2f, (k - 0.2f) * 0.5f);
                f.cg.alpha = k > 0.75f ? 1 - (k - 0.75f) / 0.25f : 1;
                f.rt.localScale = new Vector3(pop * sz, pop * sz, 1);
            });
            int n = Mathf.RoundToInt(big ? Mathf.Lerp(12, 20, pw) : Mathf.Lerp(7, 12, pw));
            Spark(side, big ? Theme.Hex("#ffd24a") : Color.white, n, 1 + 0.45f * pw + (big ? 0.2f : 0));
            if (big && pw >= 0.3f || pw >= 0.75f) Ring(side, big ? Theme.Hex("#ffd24a") : Theme.Hex("#fff6c8"));
        }

        public void Ring(int side, Color color)
        {
            var b = Body(side);
            var item = Take(ringFx);
            item.Image.color = color;
            var rt = item.Rect;
            rt.anchoredPosition = P(b);
            AddFx(item, ringFx, 0.6f, (f, k) =>
            {
                f.cg.alpha = 1 - k;
                f.rt.sizeDelta = new Vector2(140 * (0.3f + k) * K, 84 * (0.3f + k) * K);
            });
        }

        public void Ring(int side, string hex) => Ring(side, Theme.Hex(hex));

        // clip đang chạy của tướng side (menu thử chụp lúc ra đòn)
        public string ClipOf(int side) => actors[side] == null ? Idle : actors[side].dead > 0 ? Game.AolaActor.Die :
            Entering(actors[side]) ? Game.AolaActor.Appear : actors[side].loop ? Idle : actors[side].clip; // chết, ra sân: clip đang hiện thật

        // Lúc ra đòn cả sân chậm lại cho rõ animation (người dùng 2026-11-04, thay cách chỉ kéo chậm clip chiêu của 2026-11-03): tướng đang
        // chạy clip đánh, chiêu bắn (động tác bắn, tia bay, tan) hay clip CHIÊU (tuyệt kỹ, chiêu mana của boss làm riêng) thì chữ nổi, hiệu
        // ứng, rung và chờ của BattlePlayer (Wait) chạy ×1 cho khớp tướng. Vào nhịp chậm ngay lúc clip bắt đầu, ra lại nhịp sân mượt trong
        // SlowEase giây thật. Animation của tướng (đứng, đánh, trúng đòn, chiêu) luôn chạy tốc độ gốc, không theo nhịp sân (người dùng
        // 2026-11-09: chỉ tăng nhịp trận, tốc độ animation về gốc; trước đó clip đánh ×1,3, lúc đứng và trúng đòn ×3).
        const float AttackPace = 1f, SkillPace = 1f, SlowEase = 0.1f;
        float slow = 1;  // hệ số đang nhân vào nhịp sân (1: nhịp thường)
        float skillHold; // giây sân còn giữ nhịp chiêu sau clip bắn (tia còn bay, tan)
        public float Clock { get; private set; } // giây sân đã chạy

        // Chiêu mana bắn tia (người dùng 2026-11-03): mặc định của mọi tướng, quái thường, phần lớn mini boss; số ít boss làm riêng
        // khai "mana": "clip" trong anim.json (AolaSticker.ManaUsesClip) thì phát clip CHIÊU như cũ.

        public bool CanBeam(int side) => beamFx && actors[side] != null && !(actors[side].aola?.ManaUsesClip ?? false);

        // Tia từ chỗ bắn của side tới thân đối thủ (người dùng 2026-11-03: to, có hoạt cảnh, tan cho đẹp):
        // - phóng: nổ nước nhỏ và lấp lánh ở chỗ bắn;
        // - bay: thân tia vươn ra (đầu bọt dẫn trước), gợn sóng liên tục, lõi sáng mảnh hơn bên trong, giọt nước văng dọc đường;
        // - trúng (lúc đầu tia tới nơi): nổ nước lớn, giọt văng, vòng sóng loang dưới chân đối thủ, lấp lánh, rung sân nhẹ;
        // - tan: đuôi tia rút dần về phía đối thủ (nước chảy hết vào chỗ trúng), mảnh dần rồi mờ.
        // Chỗ bắn và cỡ tia: dạng có clip bắn thì theo anim.json (AolaSticker.Beam); không thì từ trước ngực, cỡ to dần theo dạng trong
        // dòng (một dạng: vừa), boss to hơn. Ảnh nước dùng chung; tướng hệ khác tạm nhuộm màu hệ tới khi có ảnh riêng.
        // Trả về thời gian tới nơi (giây sân).
        public float Beam(int side)
        {
            var a = actors[side];
            if (!beamFx || a == null) return 0;
            int other = side == 0 ? 1 : 0;
            var m = Muzzle(a, side, out float scale);
            var from = Pos[side] + m;
            var to = Body(other);
            float fire = FireBeam(a, side, from, to);
            if (fire >= 0) return fire;
            var d = to - from;
            float len = d.magnitude, ang = Mathf.Atan2(d.y, d.x);
            var nrm = len > 0 ? new Vector2(-d.y, d.x) / len : Vector2.up; // pháp tuyến (web)
            var tint = a.hero.elem == Elem.Thuy ? Color.white : Color.Lerp(Color.white, Theme.Of(a.hero.elem), 0.75f);
            float flipY = d.x < 0 ? -1 : 1; // bắn sang trái thì lật dọc để vệt sáng vẫn ở trên
            // bề dày tia (đơn vị web): dạng đầu (cỡ 0.7) 84, to dần chậm hơn cỡ (dạng cuối cỡ 1.4 khoảng 127, quái một dạng 104)
            float h = 84 * Mathf.Pow(scale / 0.7f, 0.6f);
            // cỡ hiệu ứng phụ (nổ, giọt, lấp lánh): to dần còn chậm hơn, để không che thân tướng bắn
            float g = Mathf.Pow(scale / 0.7f, 0.4f);
            // tia riêng (3 boss cuối đảo Thủy): ảnh thân tia khác, giữ lâu hơn, thêm hiệu ứng phụ theo kiểu
            string style = a.aola != null ? a.aola.BeamStyle : null;
            Sprite styleArt = null;
            if (!string.IsNullOrEmpty(style) && beamStyles != null)
                foreach (var s in beamStyles)
                    if (s && s.name == style)
                    {
                        styleArt = s;
                        break;
                    }
            var bodyArt = styleArt ? styleArt : (beamFx.Image ? beamFx.Image.sprite : null);
            if (styleArt) tint = Color.white;
            const float grow = 0.2f, shrink = 0.22f;
            float hold = styleArt ? 0.45f : 0.3f, life = grow + hold + shrink;
            // tia xoắn vẽ vòng xoắn kín cả bề dày ảnh, tia triều đã có vòng sóng âm đi kèm: không làm dày thêm, để dạng cuối
            // không che thân tướng bắn (soi tour 2026-11-07)
            if (styleArt) h *= style == "tia_xoay" ? 0.85f : style == "tia_trieu" ? 1f : 1.15f;
            skillHold = Mathf.Max(skillHold, life);

            // thân tia và lõi sáng: vẽ đoạn [đuôi, đầu] của đường bắn, đầu vươn ra nhanh, đuôi rút về đối thủ lúc tan
            for (int layer = 0; layer < 2; layer++)
            {
                bool core = layer == 1;
                var item = Take(beamFx);
                if (item.Image)
                {
                    // bản sao lấy từ hàng chờ có thể còn ảnh tia riêng của lần trước: luôn gán lại
                    if (bodyArt && item.Image.sprite != bodyArt) Theme.SetSprite(item.Image, bodyArt);
                    item.Image.color = core ? Color.Lerp(tint, Color.white, 0.7f) : tint;
                }
                item.Rect.pivot = new Vector2(0, 0.5f);
                float thick = core ? 0.42f : 1f, phase = core ? 1.7f : 0f;
                AddFx(item, beamFx, life, (f, k) =>
                {
                    float t = k * life;
                    float head = Mathf.Min(1, t / grow);
                    head = 1 - (1 - head) * (1 - head) * (1 - head);
                    float tail = Mathf.Clamp01((t - grow - hold) / shrink);
                    tail *= tail;
                    var p0 = from + d * tail;
                    float wob = 1 + 0.12f * Mathf.Sin(t * 38 + phase) + 0.06f * Mathf.Sin(t * 71 + phase);
                    f.rt.anchoredPosition = P(p0);
                    f.rt.sizeDelta = new Vector2(Mathf.Max(1, len * (head - tail)) * K, h * thick * wob * (1 - 0.6f * tail) * K);
                    f.rt.localEulerAngles = new Vector3(0, 0, -ang * Mathf.Rad2Deg + Mathf.Sin(t * 23 + phase) * 1.5f);
                    f.rt.localScale = new Vector3(1, flipY, 1);
                    f.cg.alpha = (core ? 0.6f : 1f) * (tail > 0.6f ? (1 - tail) / 0.4f : 1);
                });
            }

            // phóng: nổ nước nhỏ, lấp lánh ở chỗ bắn (nhỏ hơn đầu tướng)
            Pop(beamSplash, from, 64 * g, tint, 0, 0.3f, 0.4f, 1.1f, Random.value * 360);
            Pop(beamSparkle, from - nrm * 30 * g, 34 * g, Color.white, 0.03f, 0.3f, 0.3f, 1.2f, 0);
            // bay: giọt nước văng ra hai bên khi đầu tia đi qua (từ quá nửa đường, xa thân tướng bắn)
            for (int i = 0; i < 4; i++)
            {
                float u = 0.4f + 0.13f * i;
                float side2 = i % 2 == 0 ? 1 : -1;
                var at = from + d * u + nrm * side2 * h * 0.35f;
                var fly = nrm * side2 * 50 * g * (0.7f + Random.value * 0.5f) + d.normalized * 20 * g;
                float delay = grow * (1 - Mathf.Pow(1 - u, 1f / 3f));
                Drift(beamDrops, at, fly, 30 * g, tint, delay, 0.45f, Random.value * 360);
            }
            if (styleArt) StyleBeamFx(style, from, d, nrm, h, g, grow, hold);
            var victim = actors[other];
            StartCoroutine(BeamHit(other, to, victim != null ? victim.H : Height[other], g, tint, grow));
            if (styleArt) StartCoroutine(StyleBeamHit(style, other, to, victim != null ? victim.H : Height[other], g, grow));
            return grow;
        }

        // hiệu ứng phụ dọc đường tia của kiểu tia riêng: tia băng văng mảnh băng, tia xoắn có vòng xoáy quay dọc thân,
        // tia triều có vòng sóng âm chuông đồng nở lần lượt
        void StyleBeamFx(string style, Vector2 from, Vector2 d, Vector2 nrm, float h, float g, float grow, float hold)
        {
            switch (style)
            {
                case "tia_bang":
                    for (int i = 0; i < 8; i++)
                    {
                        float u = 0.25f + 0.09f * i;
                        float s2 = i % 2 == 0 ? 1 : -1;
                        var at = from + d * u + nrm * s2 * h * 0.4f;
                        var fly = nrm * s2 * 70 * g * (0.6f + Random.value * 0.6f) + d.normalized * 30 * g;
                        Drift(beamShard, at, fly, 40 * g, Color.white, grow * u, 0.55f, Random.value * 360);
                    }
                    break;
                case "tia_xoay":
                    // vòng đầu cách chỗ bắn một khúc, cỡ bằng bề dày tia: không trùm đầu tướng bắn ở dạng cuối
                    for (int i = 0; i < 5; i++)
                    {
                        float u = 0.35f + 0.14f * i;
                        Spin(beamVortex, from + d * u, h, Color.white, grow * u, hold + 0.1f, i % 2 == 0 ? 540 : -540);
                    }
                    break;
                case "tia_trieu":
                    // vòng theo g (to chậm hơn bề dày tia), bắt đầu từ quá nửa đường để không trùm tướng bắn
                    for (int i = 0; i < 3; i++)
                    {
                        float u = 0.42f + 0.18f * i;
                        Pop(beamSoundRing, from + d * u, 110 * g, Color.white, grow * u + 0.06f * i, 0.42f, 0.3f, 1.3f, 0);
                    }
                    AddTrauma(0.15f); // sóng âm: rung đều, không có hướng
                    break;
            }
        }

        // lúc trúng của kiểu tia riêng: thêm một nhịp riêng cho đặc biệt (chùm mảnh băng, vòng xoáy lớn, vòng sóng âm kép)
        System.Collections.IEnumerator StyleBeamHit(string style, int target, Vector2 at, float tH, float g, float after)
        {
            yield return Wait(after);
            float e = tH * Mathf.Lerp(1, g, 0.5f);
            switch (style)
            {
                case "tia_bang":
                    for (int i = 0; i < 6; i++)
                    {
                        float ang = i / 6f * Mathf.PI * 2 + Random.value * 0.5f;
                        Drift(beamShard, at, new Vector2(Mathf.Cos(ang), Mathf.Sin(ang) - 0.3f) * e * 0.9f, e * 0.28f, Color.white,
                            0.02f * i, 0.5f, Random.value * 360);
                    }
                    break;
                case "tia_xoay": // nhỏ hơn thân con bị trúng (Spin nở tới 1,1 lần cỡ)
                    Spin(beamVortex, at, e * 0.8f, Color.white, 0, 0.55f, 720);
                    break;
                case "tia_trieu": // vòng kép, vòng lớn nở tới khoảng 1,1 lần thân rồi mờ, vòng trong nhỏ hơn thân
                    Pop(beamSoundRing, at, e * 0.85f, Color.white, 0, 0.45f, 0.3f, 1.3f, 0);
                    Pop(beamSoundRing, at, e * 0.55f, Color.white, 0.12f, 0.4f, 0.3f, 1.3f, 0);
                    Bump(target, 9);
                    AddTrauma(0.25f);
                    break;
            }
        }

        // ảnh hiệu ứng nở rồi quay đều (spin độ mỗi lần sống), mờ ở cuối, sau delay giây sân
        void Spin(Sprite s, Vector2 at, float size, Color tint, float delay, float life, float spin)
        {
            if (!imageFx || !s) return;
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, s);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = P(at);
            float aspect = s.rect.height / Mathf.Max(1, s.rect.width);
            float rot0 = Random.value * 360;
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, e = 1 - (1 - u) * (1 - u);
                float sc = 0.4f + 0.7f * e;
                f.rt.sizeDelta = new Vector2(size * sc, size * sc * aspect) * K;
                f.rt.localEulerAngles = new Vector3(0, 0, -(rot0 + spin * u));
                f.cg.alpha = u < 0.6f ? 1 : (1 - u) / 0.4f;
            });
        }

        // trúng: nổ nước, giọt văng, vòng sóng dưới chân, lấp lánh, rung sân nhẹ; cỡ theo thân con bị trúng (tH),
        // nhỏ hơn thân để vẫn thấy nó bị trúng, nhỉnh dần theo dạng của con bắn (g)
        System.Collections.IEnumerator BeamHit(int target, Vector2 at, float tH, float g, Color tint, float after)
        {
            yield return Wait(after);
            float e = tH * Mathf.Lerp(1, g, 0.5f);
            Pop(beamSplash, at, e * 0.75f, tint, 0, 0.4f, 0.35f, 1.25f, Random.value * 360);
            Pop(beamSplash, at, e * 0.45f, Color.Lerp(tint, Color.white, 0.6f), 0.05f, 0.32f, 0.3f, 1.15f, Random.value * 360);
            for (int i = 0; i < 3; i++)
            {
                float a = Random.value * Mathf.PI * 2;
                Drift(beamDrops, at, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f) * e * 0.7f, e * 0.2f, tint, 0.02f * i, 0.45f, Random.value * 360);
            }
            Ripple(Pos[target], e * 1.1f, tint, 0.03f, 0.5f);
            Pop(beamSparkle, at + new Vector2(e * 0.4f, -e * 0.35f), e * 0.22f, Color.white, 0.08f, 0.3f, 0.3f, 1.2f, 0);
            Pop(beamSparkle, at + new Vector2(-e * 0.4f, -e * 0.15f), e * 0.16f, Color.white, 0.14f, 0.3f, 0.3f, 1.2f, 0);
            Spark(target, Theme.Hex("#cfe9ff"));
            Bump(target, 6);
        }

        // ảnh hiệu ứng của chiêu bắn nở ra từ s0 tới s1 rồi mờ (cỡ theo bề rộng ảnh, giữ tỉ lệ), sau delay giây sân
        void Pop(Sprite s, Vector2 at, float size, Color tint, float delay, float life, float s0, float s1, float rot)
        {
            if (!imageFx || !s) return;
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, s);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = P(at);
            float aspect = s.rect.height / Mathf.Max(1, s.rect.width);
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, e = 1 - (1 - u) * (1 - u);
                float sc = s0 + (s1 - s0) * e;
                f.rt.sizeDelta = new Vector2(size * sc, size * sc * aspect) * K;
                f.rt.localEulerAngles = new Vector3(0, 0, -(rot + 25 * u));
                f.cg.alpha = u < 0.55f ? 1 : (1 - u) / 0.45f;
            });
        }

        // ảnh hiệu ứng bay theo vận tốc (đơn vị web mỗi lần sống), rơi xuống, xoay, mờ dần, sau delay giây
        void Drift(Sprite s, Vector2 at, Vector2 fly, float size, Color tint, float delay, float life, float rot)
        {
            if (!imageFx || !s) return;
            float fall = 160 * life; // quãng rơi theo thời gian sống
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, s);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            float aspect = s.rect.height / Mathf.Max(1, s.rect.width);
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life;
                var p = at + fly * u + new Vector2(0, fall * u * u); // rơi
                f.rt.anchoredPosition = P(p);
                float sc = 0.6f + 0.5f * u;
                f.rt.sizeDelta = new Vector2(size * sc, size * sc * aspect) * K;
                f.rt.localEulerAngles = new Vector3(0, 0, -(rot + 120 * u));
                f.cg.alpha = u < 0.6f ? 1 : (1 - u) / 0.4f;
            });
        }

        // vòng sóng loang dưới chân: dẹt, nở rộng, mờ dần
        void Ripple(Vector2 feet, float width, Color tint, float delay, float life)
        {
            if (!imageFx || !beamRipple) return;
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, beamRipple);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = P(feet);
            rt.localEulerAngles = Vector3.zero;
            float aspect = beamRipple.rect.height / Mathf.Max(1, beamRipple.rect.width);
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, e = 1 - (1 - u) * (1 - u);
                float sc = 0.4f + 0.9f * e;
                f.rt.sizeDelta = new Vector2(width * sc, width * sc * aspect) * K;
                f.cg.alpha = u < 0.4f ? 1 : (1 - u) / 0.6f;
            });
        }

        // tia văng từ thân con bị trúng: n tia, speed nhân tốc. "Bắn rồi khựng" (skill pokiclash-hero-fx mục 6): tốc đầu cao, cản mũ,
        // vệt dài theo tốc độ rồi co lại, nên tia vụt ra rồi dừng thay vì trôi đều.
        public void Spark(int side, Color color, int n = 9, float speed = 1)
        {
            var b = Body(side);
            for (int i = 0; i < n; i++)
            {
                float a = Random.value * Mathf.PI * 2, v = (340 + Random.value * 380) * speed, s = 6 + Random.value * 8;
                const float drag = 6f;
                var item = Take(sparkFx);
                item.Image.color = color;
                var rt = item.Rect;
                rt.sizeDelta = new Vector2((s + 6) * K, 6 * K);
                rt.localEulerAngles = new Vector3(0, 0, -a * Mathf.Rad2Deg);
                rt.anchoredPosition = P(b);
                AddFx(item, sparkFx, 0.45f, (f, k) =>
                {
                    f.cg.alpha = k < 0.6f ? 1 : 1 - (k - 0.6f) / 0.4f;
                    float d = v * (1 - Mathf.Exp(-drag * f.t)) / drag;
                    float vel = v * Mathf.Exp(-drag * f.t);
                    // dài theo tốc độ (tối đa 2,4 lần), mảnh dần
                    float len = (s + 6) * Mathf.Clamp(vel / 300f, 0.5f, 2.4f);
                    f.rt.sizeDelta = new Vector2(len * K, 6 * (1 - 0.5f * k) * K);
                    f.rt.anchoredPosition = f.basePos + new Vector2(Mathf.Cos(a) * d, -Mathf.Sin(a) * d) * K;
                });
            }
        }

        // màn chơi ÂM BẢN trong dur giây (chiêu cuối Bạch Viêm Hổ): lớp chớp phủ sân tạm đổi sang vật liệu đảo màu (Resources/UIInvert, shader
        // PokiClash/UIInvert); trong lúc đó các cú chớp màu bị bỏ qua
        public void Neg(float dur)
        {
            if (!negMat) negMat = Resources.Load<Material>("UIInvert");
            if (!negMat) return;
            negLife = Mathf.Max(0.1f, dur);
            negT = 0;
            flashT = -1;
            flashImg.material = negMat;
            flashImg.color = new Color(1, 1, 1, 0);
            flashImg.gameObject.SetActive(true);
        }

        public void Flash(Color color)
        {
            if (negT >= 0) return;
            flashColor = color;
            flashT = 0;
            flashImg.gameObject.SetActive(true);
        }

        public void Flash(string hex = "#ffffff") => Flash(Theme.Hex(hex));

        // ---------- trạng thái trên đầu ----------

        // nhóm dấu dựng sẵn trong prefab tướng: bật nhóm có trong danh sách, xếp theo thứ tự trạng thái
        void BuildStatusIcons(Actor a)
        {
            a.view.HideStatuses();
            a.statusIcons.Clear();
            foreach (var (id, _) in a.statuses)
            {
                var g = a.view.Group(id);
                if (g) // prefab chưa có nhóm dấu (độc trước khi chạy menu dựng): giữ chỗ trống cho khớp thứ tự
                {
                    g.gameObject.SetActive(true);
                    g.SetAsLastSibling();
                }
                a.statusIcons.Add(g);
            }
        }

        void UpdateStatusIcons(Actor a)
        {
            float t = Time.unscaledTime;
            a.statusRt.gameObject.SetActive(a.dead <= 0 && !Entering(a) && a.statuses.Count > 0); // đang ra sân: dấu hiện khi clip xong
            for (int k = 0; k < a.statusIcons.Count && k < a.statuses.Count; k++)
            {
                var g = a.statusIcons[k];
                if (!g) continue;
                var id = a.statuses[k].Item1;
                if (id == StatusId.Poison) // bọt độc nổi lên rồi vỡ, lệch pha
                    for (int i = 0; i < g.childCount; i++)
                    {
                        float u = (t * 0.9f + i * 0.37f) % 1f;
                        var ch = (RectTransform)g.GetChild(i);
                        ch.anchoredPosition = new Vector2(-24 + i * 24 + Mathf.Sin(t * 3 + i) * 4, -36 - u * 26) * K;
                        float s = 0.7f + 0.4f * Mathf.Sin(u * Mathf.PI);
                        ch.localScale = new Vector3(s, s, 1);
                    }
                else if (id == StatusId.Stun)
                    for (int i = 0; i < g.childCount; i++)
                    {
                        float ang = t * 3 + i * Mathf.PI * 2 / 3;
                        ((RectTransform)g.GetChild(i)).anchoredPosition = new Vector2(Mathf.Cos(ang) * 30, Mathf.Sin(ang) * 8) * K;
                    }
                else if (id == StatusId.Burn)
                    for (int i = 0; i < g.childCount; i++)
                        ((RectTransform)g.GetChild(i)).anchoredPosition = new Vector2(-26 + i * 26, -30 - Mathf.Sin(t * 8 + i) * 3) * K;
                else if (id == StatusId.Regen)
                    ((RectTransform)g.GetChild(0)).anchoredPosition = new Vector2(34, -20 + (t * 30) % 30) * K;
                else if (id == StatusId.Evade)
                {
                    var img = g.GetChild(0).GetComponent<Image>();
                    var c = img.color;
                    c.a = 0.5f + Mathf.Sin(t * 6) * 0.2f;
                    img.color = c;
                    ((RectTransform)g.GetChild(0)).anchoredPosition = new Vector2(0, -80 * K);
                }
            }
        }

        void OnDestroy()
        {
            foreach (var a in actors) a?.aola?.Destroy();
        }

        // ---------- cập nhật ----------

        void Update()
        {
            FitBg(); // xoay màn, đổi khung Game view
            float raw = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            // đang ra đòn: sân về nhịp của clip chậm nhất đang chạy (không nhanh hơn nhịp thường)
            float pace = skillHold > 0 ? SkillPace : float.MaxValue;
            foreach (var a in actors)
            {
                if (a == null || a.loop) continue;
                if (a.clip == Attack) pace = Mathf.Min(pace, AttackPace);
                else if (a.clip == Cast || a.clip == Skill) pace = Mathf.Min(pace, SkillPace);
            }
            float goal = Mathf.Min(1, pace / Mathf.Max(0.1f, speed));
            slow = goal < slow ? goal : Mathf.MoveTowards(slow, goal, raw / SlowEase);
            float dt = raw * speed * slow * fast;
            float adt = raw * fast; // giờ animation của tướng (clip, lúc đứng): tốc độ gốc, chỉ công cụ thử mới tua nhanh
            if (freeze > 0) // khựng lúc trúng: sân gần như đứng trong giây thật đã khai
            {
                freeze -= raw;
                dt *= FreezeSlow;
                adt *= FreezeSlow;
            }
            Clock += dt;
            skillHold = Mathf.Max(0, skillHold - dt);
            foreach (var a in actors)
            {
                if (a == null) continue;
                a.t += adt;
                if (!a.loop && (a.clip == Cast || a.clip == Skill) && a.holdUntil > Clock && a.t > a.holdAt &&
                    !(a.aola != null && a.aola.SelfHold(a.clip))) a.t = a.holdAt; // giữ dáng phun, dáng nhả (rig tự giữ chiêu thì để clip chạy)
                if (a.impactAt >= 0 && Clock >= a.impactAt)
                {
                    a.impactAt = -1;
                    Impact(a, a.impactClip);
                }
                a.flash = Mathf.Max(0, a.flash - dt);
                if (a.enter < 9)
                {
                    float e0 = a.enter;
                    // ra sân, chết, rút lui chạy theo giờ animation (tốc độ gốc như mọi clip của tướng), không theo nhịp sân ×3 (2026-11-17)
                    a.enter += adt;
                    // clip ra sân của rig khai sự kiện chạm đất ("cham_dat", "dap_dat"...) hoặc gầm: rung màn đúng lúc; hình rơi xuống thì
                    // rung nhẹ, bụi lúc chạm đất (StageViewShow.EnterBeats)
                    EnterBeats(a, e0);
                    RaSanFx(a, e0); // rig có hạt ra sân riêng (Bùn Ngoạm: cục đất chạm đất, bung; StageViewNuot.cs)
                }
                if (a.exit > 0) a.exit += adt;
                if (a.hop > 0) a.hop = a.hop > 0.5f ? 0 : a.hop + dt;
                if (a.dead > 0 && NuotPha(a, out _, out _) == 0) // đang bị nuốt / nhổ (StageViewNuot.cs): clip chết chờ tới khi đáp
                {
                    float d0 = a.dead;
                    a.dead += adt;
                    DieBeats(a, d0); // thân chạm đất trong clip chết: thịch nhẹ, bụi; gần hết clip: vài hạt màu hệ bay lên
                }
                if (a.recoil >= 0) a.recoil = a.recoil + dt > RecoilLen ? -1 : a.recoil + dt;
                if (!a.loop)
                {
                    float len = a.aola != null ? a.aola.Duration(a.clip) : ClipLen(a.clip);
                    float hitT = a.aola != null ? a.aola.HitTime(a.clip) : len * HitAt(a.clip);
                    if (!a.hitFired && a.t >= hitT)
                    {
                        a.hitFired = true;
                        // chiêu nước nhả ở khung này nhưng còn bay tới đối thủ: khựng, rung, bật lùi dời tới lúc nước trúng
                        if (a.fxHitAt > Clock + 0.03f)
                        {
                            a.impactAt = a.fxHitAt;
                            a.impactClip = a.clip;
                        }
                        else Impact(a);
                        a.onHit?.Invoke();
                        if (a.handle != null) a.handle.hit = true;
                    }
                    if (a.t >= len)
                    {
                        if (!a.hitFired)
                        {
                            a.hitFired = true;
                            Impact(a);
                            a.onHit?.Invoke();
                        }
                        a.clip = Idle;
                        a.t = 0;
                        a.loop = true;
                        if (a.handle != null)
                        {
                            a.handle.hit = a.handle.done = true;
                            a.handle = null;
                        }
                    }
                }
                Place(a);
                UpdateStatusIcons(a);
            }
            // đẩy màn có hướng: giữ nguyên lúc khựng (khoảnh khắc chạm đứng hình), hồi mũ theo giờ thật sau đó
            if (freeze <= 0) bump *= Mathf.Exp(-BumpDecay * raw);
            if (bump.sqrMagnitude < 0.01f) bump = Vector2.zero;
            var jolt = bump;
            if (trauma > 0) // rung trauma (Eiserloh): lệch = tối đa × trauma², sóng sin lệch tần số (mượt), giảm theo giờ thật
            {
                trauma = Mathf.Max(0, trauma - raw * TraumaDecay);
                float q = trauma * trauma, n = Time.unscaledTime * 30;
                jolt += new Vector2((Mathf.Sin(n * 1.7f) + Mathf.Sin(n * 2.3f + 1.3f)) * 0.5f * TraumaX * q,
                    (Mathf.Sin(n * 1.1f + 0.7f) + Mathf.Sin(n * 2.9f)) * 0.5f * TraumaY * q);
            }
            var off = jolt * K;
            root.anchoredPosition = off;
            // đẩy, rung làm lộ mép sân: phóng nhẹ quanh gốc của lớp rung vừa đủ phủ kín mép (kiêm "zoom punch" của GameFeel, tối đa 8%)
            var rr = root.rect;
            var pv = root.pivot;
            float need = 0;
            if (off.x > 0) need = Mathf.Max(need, off.x / Mathf.Max(1, rr.width * pv.x));
            else if (off.x < 0) need = Mathf.Max(need, -off.x / Mathf.Max(1, rr.width * (1 - pv.x)));
            if (off.y > 0) need = Mathf.Max(need, off.y / Mathf.Max(1, rr.height * pv.y));
            else if (off.y < 0) need = Mathf.Max(need, -off.y / Mathf.Max(1, rr.height * (1 - pv.y)));
            float zs = 1 + Mathf.Min(0.08f, need * 1.05f);
            root.localScale = new Vector3(zs, zs, 1);

            hat?.Update(dt);
            for (int i = fx.Count - 1; i >= 0; i--)
            {
                var f = fx[i];
                f.t += dt;
                if (f.t >= f.life || f.rt == null)
                {
                    Release(f);
                    fx.RemoveAt(i);
                    continue;
                }
                f.update(f, f.t / f.life);
            }

            if (negT >= 0)
            {
                negT += dt;
                if (negT >= negLife)
                {
                    negT = -1;
                    flashImg.material = null;
                    if (flashT < 0) flashImg.gameObject.SetActive(false);
                }
                else flashImg.color = new Color(1, 1, 1, Mathf.Min(1, negT / 0.03f) * Mathf.Min(1, (negLife - negT) / 0.04f)); // vào, ra gọn: pha nửa chừng là một màn xám
            }
            else if (flashT >= 0)
            {
                flashT += dt;
                float k = flashT / flashLife;
                if (k >= 1)
                {
                    flashT = -1;
                    flashImg.gameObject.SetActive(false);
                }
                else flashImg.color = new Color(flashColor.r, flashColor.g, flashColor.b, (1 - k) * 0.7f * flashColor.a); // hex 8 số: chớp nhạt
            }
        }

        // cú trúng của clip có khai impact (AolaSticker.Impact): khựng sân (tối đa 0,2 giây thật), cộng trauma rung, đẩy lùi đối thủ
        // Rung màn ở chiêu cuối của MỌI tướng (người dùng 2026-11-12: "thêm shake cam vào chiêu cuối của tất cả các tướng"): tướng
        // không khai impact (hình aola, hình giữ chỗ, rig cũ) hoặc khai rung nhẹ vẫn rung ít nhất UltShake lúc chiêu cuối trúng;
        // tướng không khai gì thì thêm một nhịp khựng ngắn UltStop cho cú rung có lực.
        const float UltShake = 0.62f, UltStop = 0.06f;

        void Impact(Actor a, string clip = null)
        {
            string c = clip ?? a.clip;
            float stop = 0, tr = 0, push = 0;
            string flash = null;
            bool has = a.aola != null && a.aola.Impact(c, out stop, out tr, out push, out flash);
            // chiêu cuối: mức tối thiểu tăng theo độ khó trận và kẻ đánh (boss, dạng sau) (người dùng 2026-11-16: tướng sau epic hơn);
            // số rig tự khai giữ nguyên, chỉ nâng mức sàn
            float pw = Power(a.side);
            if (c == Skill)
            {
                if (!has) stop = Mathf.Lerp(UltStop, 0.14f, pw);
                else stop = Mathf.Max(stop, Mathf.Lerp(0, 0.12f, pw));
                tr = Mathf.Max(tr, Mathf.Lerp(UltShake, 0.9f, pw));
                Bump(1 - a.side, Mathf.Lerp(8, 16, pw));
            }
            else if (!has) return;
            freeze = Mathf.Max(freeze, Mathf.Min(0.2f, stop));
            trauma = Mathf.Min(1, trauma + tr);
            if (!string.IsNullOrEmpty(flash)) Flash(flash);
            var d = actors[a.side == 0 ? 1 : 0];
            if (d != null && d.dead <= 0 && push > 0)
            {
                d.recoil = 0;
                d.push = push;
            }
        }

        void Place(Actor a)
        {
            var p = Pos[a.side];
            float x = p.x, y = p.y;
            // rig có clip ra sân / chết (lô quái Thủy 2026-11-11) thì clip tự diễn, sân không rơi, không xoay, không mờ thay
            bool rigEnter = a.aola != null && a.aola.HasClip(Game.AolaActor.Appear) && a.enter < a.aola.Duration(Game.AolaActor.Appear);
            bool rigDie = a.dead > 0 && a.aola != null && a.aola.HasClip(Game.AolaActor.Die);
            // ra sân: rơi từ trên xuống, nảy nhẹ
            if (a.enter < EnterFall && !rigEnter)
            {
                float k = Mathf.Max(0, a.enter) / EnterFall;
                y -= (1 - k) * (1 - k) * 260;
            }
            float alpha = 1;
            if (a.exit > 0) // rút lui (đổi tướng): nhún lên rồi lướt ra mép sân nhanh dần, mờ dần
            {
                float k = Mathf.Min(1, a.exit / RetreatLen);
                alpha = 1 - k * k;
                x += (a.side == 0 ? 1 : -1) * k * k * 320;
                y -= Mathf.Sin(k * Mathf.PI) * 16;
            }
            if (a.hop > 0) y -= Mathf.Sin(a.hop / 0.5f * Mathf.PI) * 40;
            float rot = 0;
            if (a.dead > 0 && !rigDie) // hình không có clip chết: khựng một nhịp, ngã nghiêng nhanh dần, chìm, mờ hết
            {
                float k = Mathf.Clamp01((a.dead - 0.1f) / (DieFade - 0.1f));
                float fall = k * k;
                alpha = 1 - k;
                rot = (a.side == 0 ? 1 : -1) * fall * 1.1f;
                y += fall * 14;
            }
            // bị Bùn Ngoạm nuốt (pha 1: ẩn hẳn) hoặc đang bị nhổ bay về chỗ (pha 2), StageViewNuot.cs
            int nuot = NuotPha(a, out var nk, out float ntf);
            if (nuot != 2) NhoXong(a);
            a.rt.gameObject.SetActive(a.dead <= DieLen(a) + 0.1f && nuot != 1);

            // quãng lao: nắn chuyển động của clip đánh tới đối thủ (aola), hình giữ chỗ thì tự nhún tới 35%
            float ox = 0, oy = 0;
            var other = Pos[a.side == 0 ? 1 : 0];
            float tx = (other.x - p.x) * 0.72f, ty = (other.y - p.y) * 0.72f;
            bool lunged = false;
            // chiêu cuối của tướng aola chỉ lao khi clip có khai (AolaSticker.Lunge); không khai thì đứng tại chỗ như trước
            if (!a.loop && (a.clip == Attack || a.clip == Skill))
            {
                // chiêu cuối nhảy đè (rig có "skill_land"): bay theo cung lên đầu đối thủ, đè, rồi bật về (AolaSticker.Jump; y lên)
                var foe = actors[a.side == 0 ? 1 : 0];
                float foeH = foe != null ? foe.H : Height[a.side == 0 ? 1 : 0];
                // chiêu cuối tông thẳng (AolaSticker.Rams, Cầu Gai): chỗ đáp ngang thân đối thủ, dừng sát trước nó (86 % quãng)
                var jumpTo = a.aola != null && a.aola.Rams
                    ? new Vector2((other.x - p.x) * 0.86f, (p.y - other.y) * 0.86f + foeH * 0.06f)
                    : new Vector2(other.x - p.x, p.y - other.y + foeH * 0.62f);
                if (a.aola != null && a.aola.Jump(a.clip, a.t, jumpTo, a.H, out var jo))
                {
                    ox = jo.x;
                    oy = -jo.y;
                    lunged = true;
                }
                else if (a.aola != null && a.aola.Lunge(a.clip, a.t, tx, ty, out var o))
                {
                    ox = o.x;
                    oy = o.y;
                    lunged = true;
                }
                else if ((a.clip == Attack || a.aola == null) && (a.aola == null || !a.aola.Stays(a.clip)))
                {
                    // đòn bắn xa (rig khai far/stay) đứng một chỗ: không nhún tới (người dùng 2026-11-09)
                    float len = a.aola != null ? a.aola.Duration(a.clip) : ClipLen(a.clip);
                    float hitT = a.aola != null ? a.aola.HitTime(a.clip) : len * HitAt(a.clip);
                    float u = Mathf.Min(1, a.t / Mathf.Max(0.01f, hitT));
                    float back = a.t > hitT ? Mathf.Min(1, (a.t - hitT) / Mathf.Max(0.01f, len - hitT)) : 0;
                    float lunge = Mathf.Sin(u * Mathf.PI * 0.5f) * (1 - back) * (a.clip == Skill ? 0.12f : 0.35f);
                    ox = tx * lunge;
                    oy = ty * lunge;
                }
            }
            // chiêu mana LƯỚT TỚI chém (Voọc Tướng 2026-11-12: "cúi xuống hold, rút kiếm chém, trong lúc hold có thể move tới đối thủ"): rig
            // khai "lunge" cho clip cast VÀ mã hiệu ứng thuộc HatLua.CastLao thì quãng lướt của clip được nắn tới 72 % quãng tới đối thủ như
            // đòn đánh thường. Rig khác khai lunge cho cast (Liên Kình) không đổi cho tới khi mã hiệu ứng của nó được thêm vào CastLao.
            if (!a.loop && a.clip == Cast && a.aola != null && HatLua.CastLao(FireMana(a.hero, a.form)) && a.aola.Lunge(a.clip, a.t, tx, ty, out var co))
            {
                ox = co.x;
                oy = co.y;
                lunged = true;
            }
            // chiêu bắn của tướng không có clip bắn: nhún nhẹ về phía đối thủ lúc phóng tia
            if (!a.loop && a.clip == Cast && (a.aola == null || !a.aola.HasCast))
            {
                float k = Mathf.Clamp01(a.t / AolaSticker.CastLen);
                float nudge = Mathf.Sin(k * Mathf.PI) * 0.06f;
                ox = tx * nudge;
                oy = ty * nudge;
            }
            if (a.recoil >= 0) // bật lùi (Impact): ra xa đối thủ trong 15% đầu, về chỗ êm; nghiêng ra sau; lúc khựng rung ngang tại chỗ
            {
                float u = a.recoil / RecoilLen, v = Mathf.Clamp01((u - 0.15f) / 0.85f);
                float f = u < 0.15f ? Mathf.Sin(u / 0.15f * Mathf.PI * 0.5f) : 1 - v * v * (3 - 2 * v);
                var away = new Vector2(p.x - other.x, p.y - other.y).normalized * (f * a.push * a.H);
                ox += away.x;
                oy += away.y;
                rot += (a.side == 0 ? 1 : -1) * 0.09f * f;
                if (freeze > 0) ox += Mathf.Sin(Time.unscaledTime * 95) * 0.015f * a.H;
            }
            if (nuot == 2) NhoDat(a, nk, ntf, x, y, ref ox, ref oy, ref rot); // bị nhổ: bay theo cung từ miệng kẻ đánh về chỗ, nảy
            TinhDat(a, ref ox, ref oy, ref alpha); // bị Thổ Tinh đánh: co vào vỏ đá, bẹp, giật theo lưỡi trăng (StageViewThoTinh.cs)
            a.rt.anchoredPosition = P(x + ox, y + oy);
            // nhún bằng code lúc trúng đòn (NhunTrung): dao động tắt dần, gốc ở chân; animation của rig chạy bình thường bên trong
            float tn = Time.unscaledTime - a.nhunLuc, nh = tn < 0.4f ? a.nhunA * Mathf.Exp(-tn / 0.085f) * Mathf.Cos(tn * 37f) : 0;
            a.rt.localScale = new Vector3(1 + nh, 1 - 0.9f * nh, 1);
            a.rt.localEulerAngles = new Vector3(0, 0, -rot * Mathf.Rad2Deg);

            if (a.aola != null)
            {
                // đòn bắn từ xa (không lao) của aola: đạn bay và vụ nổ vẽ về thân đối thủ (AolaSticker.Far)
                bool far = !a.loop && !lunged && (a.clip == Attack || a.clip == Skill || a.clip == Cast); // Cast: Gạc Đá bắn hai tảng tay (xương fly_*); AolaSticker.Far tự bỏ qua clip không khai far
                a.aola.Far(a.loop ? Idle : a.clip, far ? Body(a.side == 0 ? 1 : 0) - new Vector2(x + ox, y + oy) : (Vector2?)null);
                if (nuot == 2) a.aola.Show(Hit, ntf, false, alpha, false, a.flash); // đang bay khi bị nhổ: dáng trúng đòn (gục thì chết sau khi đáp)
                else if (rigDie) a.aola.Show(Game.AolaActor.Die, a.dead, false, alpha, false, a.flash); // flash: thân trắng dần lúc boss tiến hóa
                else if (rigEnter && a.loop) a.aola.Show(Game.AolaActor.Appear, a.enter, false, alpha, false, a.flash);
                else a.aola.Show(a.loop ? Idle : a.clip, a.t, a.loop, alpha, a.dead > 0, a.flash);
            }
            else
            {
                // nhịp thở lúc đứng, giật lùi lúc trúng đòn
                float sy = 1, sx = 1;
                if (a.clip == Idle) sy = 1 + Mathf.Sin(a.t * 4.2f) * 0.025f;
                if (a.clip == Hit) sx = 1 - Mathf.Sin(a.t / 0.36f * Mathf.PI) * 0.08f;
                a.body.localScale = new Vector3((a.side == 0 ? -1 : 1) * sx, sy, 1);
                if (a.clip == Hit) a.body.anchoredPosition = new Vector2((a.side == 0 ? 1 : -1) * Mathf.Sin(a.t / 0.36f * Mathf.PI) * 10 * K, 0);
                else a.body.anchoredPosition = Vector2.zero;
                var gray = a.dead > 0 ? new Color(0.62f, 0.6f, 0.58f, alpha) : new Color(1, 1, 1, alpha);
                a.bodyImg.color = gray;
                a.emblem.color = gray;
                a.flashImg.color = new Color(1, 1, 1, Mathf.Min(1, a.flash * 5) * 0.65f * alpha);
            }
            var sc = a.view.Shadow;
            sc.color = new Color(Theme.Ink.r, Theme.Ink.g, Theme.Ink.b, 0.35f * alpha);
            // bóng đứng yên ở chân khi lao
            a.shadow.anchoredPosition = new Vector2(-ox * K, (y + oy - p.y - 2) * K);
        }
    }
}
