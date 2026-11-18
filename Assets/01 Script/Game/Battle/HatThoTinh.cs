// THỔ TINH (suất giap_nham, ải 70 đảo Thổ, final boss; 2026-11-18): hành tinh đá có hai nắm đấm mặt trăng, mười lưỡi trăng trên lưng, vệ tinh
// bay quanh. Rig thach_de_1 (ArtGen/Spine/thach_de_rig.py trên monster_3802; ghi chú ArtGen/Spine/inbox/thach_de_ghichu.md mục 3f).
// DẠNG 1 "Tiểu Thổ Tinh" (2026-11-18): rig thach_de_non (cùng script, cờ TH_DANG=non; ghi chú ArtGen/Spine/inbox/thach_de_non_ghichu.md): lõi
// bọc vỏ đá trăng nứt, SÁU mảnh vỏ vỡ trên lưng thay mười lưỡi trăng, ba vệ tinh, cao 572 (dạng 2: 800); cùng nhịp clip, chiêu mana phóng sáu
// mảnh vỏ (lưỡi 9, 7, 5, 4, 2, 0; ban 0,98 + 0,08 j). Mã dạng 1 thêm đuôi "1" (n_tinh_nen1, n_tinh_gai1, n_tinh_hang1), dùng bộ số TtD1
// (dạng 2: TtD2); dạng 1 nhẹ hơn (muc 0,8: rung, chớp, độ lớn nổ).
// Làm lại trong game đúng bản xem trước người dùng đã duyệt ArtGen/Spine/thach_de_fx.py (GIF inbox/thach_de_1/fx/): cùng nhịp, cùng phần tử.
// Đi đường "n_" như bộ Thổ (HatTho.cs, HatThach.cs): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip); mốc dưới đây là giây của rig, co
// theo k = lead / giờ trúng của rig (lead chỉ lệch vì làm tròn khung 25/giây thì giữ k = 1 để mảnh bay hiện đúng lúc rig ẩn nó). Điểm bám đo
// bằng ArtGen/Spine/thach_de_do_hat.py (TH_DANG=non cho dạng 1; đơn vị chiều cao tướng; x về phía đối thủ, y lên; gốc = chân). Số px của bản
// xem trước: phần quanh tướng mình tính theo tướng cao 172,5 (1,15 × 150), phần quanh đối thủ theo đối thủ cao 150.
// Hình: đá trăng tím oải hương có hố như mảnh rig, viền mực #2B2118, tô phẳng; lửa mặt trời cam → kem; không glow, không gradient. Thân khối lớn
// (lưỡi trăng / mảnh vỏ, đuôi thiên thạch, mặt trời, tia nhiệt, mây nấm) là mảng liền (HatMang). Mây nấm phủ lên đối thủ nên cả khối trong
// 0,82: hợp các cụm tròn thành MỘT đường viền ngoài (mỗi cụm rời một mảng), viền mực nằm ngoài mảng màu, không lớp nào chồng lớp nào.
// - n_tinh_nen  đánh thường "Thiên Chuỳ" (rig khai lunge, trúng 0,68): bụi bật lúc nhảy (0,22); nện hai nắm đấm: sao kem, dăm, bụi, vòng bụi,
//   hai vết nứt dưới chân đối thủ, rung, chớp nhẹ; đối thủ bẹp (StageViewThoTinh.cs).
// - n_tinh_gai  chiêu mana "Nguyệt Nhận" (đứng): gầm (cung sóng kem từ miệng 0,32 → 0,92), đất rung, vụn ở đế mảnh khi bứt ra; rig ẨN từng
//   mảnh đúng sự kiện ban, lớp này vẽ mảnh (mảng theo đường viền ảnh luoi_1 / non_vo_1) bay 0,20 s từ đúng khung ảnh lúc ẩn tới giữa thân đối
//   thủ, mũi xoay theo đường bay thật, bóng mờ + vệt bụi, cắm rồi vỡ; mỗi mảnh một cú trúng nhẹ (đối thủ giật, nháy: StageViewThoTinh.cs),
//   mảnh cuối nặng hơn. Trả giờ mảnh đầu cắm.
// - n_tinh_hang chiêu cuối "Hằng Tinh Diệt" (đứng, 4,70 s, trúng 3,48): sỏi nổi lên dưới chân khi bay lên; 45 thiên thạch / đá trăng (đuôi lửa
//   45 %, còn lại đuôi bụi mảnh không viền) lao từ trên trời / phía xa tướng mình tới bám thành vỏ cầu quanh giữa thân đối thủ (nửa sau vẽ sau
//   nó); ép 2,15 → 2,83: vỏ co còn 44 %, run, bụi dăm phì ra, đối thủ co theo (StageViewThoTinh.cs, hai dạng chung); mặt trời đĩa phẳng bốn
//   lớp + vành lưỡi lửa quay trên đầu đối thủ (3,05); tia nhiệt (3,40); NỔ 3,48: chớp vừa, rung mạnh, vỏ đá văng tứ tung (nảy một lần rồi
//   nằm, mờ dần), cầu lửa, vành bụi, mây nấm dựng hình (cột + mũ vòm + cuộn mép, lửa → than → xám, tan dần); đáp đất 4,15.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // ---------- màu (không dùng biến tĩnh của file khác lúc khởi tạo) ----------
        static readonly Color TtMat = C(226, 206, 218), TtHo = C(172, 148, 174);                             // đá trăng của rig: mặt, hố / mặt bên
        static readonly Color TtDa = C(207, 200, 214), TtDa2 = C(157, 149, 171), TtDa3 = C(179, 171, 192);    // dăm đá trăng
        static readonly Color TtBui3 = C(238, 208, 160), TtBui4 = C(252, 238, 208);                          // đuôi bụi, vành bụi (tươi, 2026-11-18)
        static readonly Color TtHoi = C(255, 238, 212);                                                       // hơi nóng
        static readonly Color[] TtLua = { C(234, 96, 40), C(248, 158, 52), C(252, 214, 92), C(255, 244, 206) }; // mặt trời, tia, đuôi lửa
        static readonly Color[] TtNamC =                                                                     // mây nấm theo tuổi: lửa → than → xám
            { C(252, 214, 92), C(248, 158, 52), C(168, 86, 50), C(112, 98, 94), C(160, 156, 152), C(204, 200, 196), C(152, 148, 146) };
        static readonly Color[] TtDamC = { C(207, 200, 214), C(157, 149, 171), C(179, 171, 192), C(118, 104, 90), C(150, 136, 118), C(184, 170, 150) };
        // cầu lửa vụ nổ: bốn lớp từ ngoài vào lõi (đỏ cam, cam, vàng, kem); lớp ngoài nguội dần thành than
        static readonly Color[] TtLuaC = { C(230, 82, 36), C(246, 140, 44), C(252, 204, 78), C(255, 244, 210) };
        static readonly Color TtThan = C(58, 48, 46);

        // ---------- nhịp (giây rig, hai dạng chung) ----------
        const float TtCaoXem = 172.5f;                                     // tướng mình cao chừng này trong bản xem trước
        const float TtAtTu = 0.22f, TtAtTr = 0.68f;                        // đánh thường: rời đất, nện (= trúng)
        const float TtCaTr = 1.1787f;                                       // cast: giờ trúng khai trong rig (game.hitTimes, hai dạng như nhau)
        const float TtGam0 = 0.32f, TtGam1 = 0.92f, TtTach0 = 0.30f, TtTachCach = 0.024f, TtBan0 = 0.98f, TtBay = 0.20f;
        const float TtSkBay0 = 0.36f, TtSkHut = 1.00f, TtSkEp0 = 2.15f, TtSkEp2 = 2.83f, TtSkGoi = 3.05f, TtSkTia = 3.40f, TtSkNo = 3.48f,
            TtSkDat = 4.15f;

        // ---------- bộ số theo DẠNG (đo bằng ArtGen/Spine/thach_de_do_hat.py, 2026-11-18) ----------
        // nam1 / nam2: hai nắm đấm (bone96, bone102) so với xương move ở khung trúng đòn thường (sân nắn đỉnh cú lao vào 72 % quãng tới đối thủ);
        // mieng: bản lề hàm (xương ham) ở cast từ 0,30 bước 0,05; miengLech: bản lề → miệng (bản xem trước dạng 2: 14 px tới trước, 4 px xuống;
        // dạng 1 nhân đầu net 1,27 và đổi sang chiều cao 572); mảnh bay chiêu mana theo THỨ TỰ PHÓNG: idx (số lưỡi), tach (đế lúc bứt, giây
        // 0,32 + 0,024 idx), ban / goc / cao / rong (tâm, góc trục đáy → đỉnh ảnh độ ngược kim y lên, cao, rộng của khung ảnh lúc rig ẩn nó; rig
        // chĩa về đích mặc định 1,25 / 0,42 chiều cao chứ không phải đối thủ thật nên mảnh VFX xoay dần sang đường bay thật); banCach: giãn cách
        // phóng; trai / phai: đường viền ảnh mảnh (u theo bề rộng ảnh, phải +; v từ mép dưới 0 tới mép trên 1), mép trái và mép phải từ trên
        // xuống; ho: hố (u, v, bán kính theo chiều cao); matBen: bề rộng mặt bên sẫm dọc mép phải; vo: mảnh vỏ (mặt bên chạy tới tận đáy);
        // muc: độ mạnh rung, chớp, nổ.
        sealed class TtDang
        {
            public Vector2 nam1, nam2, miengLech;
            public Vector2[] mieng, tach, ban, trai, phai;
            public int[] idx;
            public float[] goc, cao, rong;
            public Vector3[] ho;
            public float banCach, matBen, muc;
            public bool vo;
        }

        static readonly Vector2[] TtMiengD2 =
        {
            new Vector2(0.153f, 0.405f), new Vector2(0.159f, 0.404f), new Vector2(0.169f, 0.383f), new Vector2(0.164f, 0.398f),
            new Vector2(0.164f, 0.397f), new Vector2(0.170f, 0.380f), new Vector2(0.165f, 0.395f), new Vector2(0.170f, 0.378f),
            new Vector2(0.170f, 0.377f), new Vector2(0.166f, 0.391f), new Vector2(0.171f, 0.375f), new Vector2(0.166f, 0.390f),
            new Vector2(0.166f, 0.389f), new Vector2(0.169f, 0.375f),
        };

        // dạng 2 Thổ Tinh (thach_de_1, cao 800,2): mười lưỡi trăng, hình luoi_1
        static readonly TtDang TtD2 = new TtDang
        {
            nam1 = new Vector2(0.155f, 0.098f), nam2 = new Vector2(0.407f, 0.126f),
            mieng = TtMiengD2, miengLech = new Vector2(0.081f, -0.023f),
            idx = new[] { 9, 8, 7, 6, 5, 4, 3, 2, 1, 0 },
            tach = new[]
            {
                new Vector2(0.230f, 0.601f), new Vector2(0.170f, 0.659f), new Vector2(0.088f, 0.695f), new Vector2(0.027f, 0.711f), new Vector2(-0.034f, 0.709f),
                new Vector2(-0.088f, 0.694f), new Vector2(-0.137f, 0.670f), new Vector2(-0.202f, 0.631f), new Vector2(-0.248f, 0.591f), new Vector2(-0.278f, 0.533f),
            },
            ban = new[]
            {
                new Vector2(0.475f, 0.579f), new Vector2(0.421f, 0.663f), new Vector2(0.395f, 0.775f), new Vector2(0.281f, 0.802f), new Vector2(0.183f, 0.873f),
                new Vector2(0.058f, 0.834f), new Vector2(-0.081f, 0.843f), new Vector2(-0.171f, 0.747f), new Vector2(-0.297f, 0.691f), new Vector2(-0.321f, 0.571f),
            },
            goc = new[] { -11.6f, -16.3f, -22.5f, -21.5f, -23.0f, -19.2f, -17.6f, -13.0f, -9.9f, -5.5f },
            cao = new[] { 0.137f, 0.174f, 0.213f, 0.250f, 0.274f, 0.257f, 0.229f, 0.195f, 0.162f, 0.131f },
            rong = new[] { 0.103f, 0.119f, 0.131f, 0.153f, 0.161f, 0.157f, 0.141f, 0.127f, 0.115f, 0.098f },
            banCach = 0.062f,
            trai = new[]
            {
                new Vector2(0.434f, 0.986f), new Vector2(0.018f, 0.898f), new Vector2(-0.167f, 0.808f), new Vector2(-0.289f, 0.721f), new Vector2(-0.373f, 0.634f),
                new Vector2(-0.434f, 0.544f), new Vector2(-0.465f, 0.456f), new Vector2(-0.478f, 0.366f), new Vector2(-0.469f, 0.279f), new Vector2(-0.430f, 0.192f),
                new Vector2(-0.360f, 0.102f), new Vector2(-0.075f, 0.014f),
            },
            phai = new[]
            {
                new Vector2(0.469f, 0.986f), new Vector2(0.325f, 0.898f), new Vector2(0.224f, 0.808f), new Vector2(0.162f, 0.721f), new Vector2(0.127f, 0.634f),
                new Vector2(0.123f, 0.544f), new Vector2(0.154f, 0.456f), new Vector2(0.219f, 0.366f), new Vector2(0.338f, 0.279f), new Vector2(0.382f, 0.192f),
                new Vector2(0.329f, 0.102f), new Vector2(0.105f, 0.014f),
            },
            ho = new[] { new Vector3(-0.232f, 0.523f, 0.041f), new Vector3(-0.154f, 0.306f, 0.073f), new Vector3(0.118f, 0.181f, 0.028f) },
            matBen = 0.15f, vo = false, muc = 1f,
        };

        // dạng 1 Tiểu Thổ Tinh (thach_de_non, cao 571,9): sáu mảnh vỏ vỡ (lưỡi 5→non_vo_1, 4→vo_2, 7→vo_3, 2→vo_4, 9→vo_5, 0→vo_6), hình non_vo_1
        // giãn theo khung từng mảnh
        static readonly TtDang TtD1 = new TtDang
        {
            nam1 = new Vector2(0.135f, 0.120f), nam2 = new Vector2(0.390f, 0.148f),
            mieng = new[]
            {
                new Vector2(0.201f, 0.393f), new Vector2(0.214f, 0.394f), new Vector2(0.217f, 0.365f), new Vector2(0.218f, 0.386f),
                new Vector2(0.218f, 0.384f), new Vector2(0.216f, 0.361f), new Vector2(0.218f, 0.381f), new Vector2(0.215f, 0.358f),
                new Vector2(0.215f, 0.356f), new Vector2(0.217f, 0.376f), new Vector2(0.214f, 0.353f), new Vector2(0.216f, 0.374f),
                new Vector2(0.216f, 0.373f), new Vector2(0.212f, 0.354f),
            },
            miengLech = new Vector2(0.144f, -0.041f),
            idx = new[] { 9, 7, 5, 4, 2, 0 },
            tach = new[]
            {
                new Vector2(0.234f, 0.658f), new Vector2(0.087f, 0.755f), new Vector2(-0.039f, 0.770f), new Vector2(-0.095f, 0.754f), new Vector2(-0.214f, 0.689f),
                new Vector2(-0.295f, 0.592f),
            },
            ban = new[]
            {
                new Vector2(0.468f, 0.637f), new Vector2(0.367f, 0.848f), new Vector2(0.147f, 0.947f), new Vector2(0.015f, 0.912f), new Vector2(-0.215f, 0.822f),
                new Vector2(-0.360f, 0.639f),
            },
            goc = new[] { -15.5f, -25.9f, -25.5f, -21.7f, -15.3f, -7.8f },
            cao = new[] { 0.096f, 0.149f, 0.192f, 0.181f, 0.136f, 0.091f },
            rong = new[] { 0.084f, 0.123f, 0.120f, 0.132f, 0.115f, 0.094f },
            banCach = 0.08f,
            trai = new[]
            {
                new Vector2(0.406f, 0.986f), new Vector2(0.133f, 0.937f), new Vector2(-0.022f, 0.889f), new Vector2(-0.096f, 0.840f), new Vector2(-0.124f, 0.792f),
                new Vector2(-0.153f, 0.743f), new Vector2(-0.271f, 0.694f), new Vector2(-0.357f, 0.646f), new Vector2(-0.373f, 0.597f), new Vector2(-0.386f, 0.549f),
                new Vector2(-0.427f, 0.500f), new Vector2(-0.463f, 0.451f), new Vector2(-0.471f, 0.403f), new Vector2(-0.451f, 0.354f), new Vector2(-0.427f, 0.306f),
                new Vector2(-0.422f, 0.257f), new Vector2(-0.431f, 0.208f), new Vector2(-0.431f, 0.160f), new Vector2(-0.431f, 0.111f), new Vector2(-0.427f, 0.063f),
                new Vector2(-0.402f, 0.014f),
            },
            phai = new[]
            {
                new Vector2(0.422f, 0.986f), new Vector2(0.410f, 0.937f), new Vector2(0.378f, 0.889f), new Vector2(0.349f, 0.840f), new Vector2(0.333f, 0.792f),
                new Vector2(0.324f, 0.743f), new Vector2(0.324f, 0.694f), new Vector2(0.402f, 0.646f), new Vector2(0.480f, 0.597f), new Vector2(0.451f, 0.549f),
                new Vector2(0.422f, 0.500f), new Vector2(0.402f, 0.451f), new Vector2(0.386f, 0.403f), new Vector2(0.373f, 0.354f), new Vector2(0.373f, 0.306f),
                new Vector2(0.382f, 0.257f), new Vector2(0.394f, 0.208f), new Vector2(0.414f, 0.160f), new Vector2(0.435f, 0.111f), new Vector2(0.459f, 0.063f),
                new Vector2(0.361f, 0.014f),
            },
            ho = new[] { new Vector3(-0.018f, 0.527f, 0.051f), new Vector3(-0.120f, 0.256f, 0.097f) },
            matBen = 0.16f, vo = true, muc = 0.8f,
        };

        // mây nấm (bản xem trước): mũ vòm 9 cụm, 4 cụm cuộn dưới mép mũ (lần bề rộng, bề cao mũ)
        static readonly Vector2[] TtNamMu =
        {
            new Vector2(-1f, 0f), new Vector2(-0.62f, -0.42f), new Vector2(-0.2f, -0.62f), new Vector2(0.22f, -0.6f), new Vector2(0.64f, -0.4f),
            new Vector2(1f, 0.02f), new Vector2(-0.4f, -0.15f), new Vector2(0f, -0.25f), new Vector2(0.42f, -0.12f),
        };
        static readonly Vector2[] TtNamCuon = { new Vector2(-1.12f, 0.38f), new Vector2(-0.6f, 0.42f), new Vector2(0.6f, 0.42f), new Vector2(1.14f, 0.36f) };

        // một hòn của vỏ đá chiêu cuối: chỗ bám trên đĩa đơn vị (khung bản xem trước), sâu z (< 0: nửa sau, vẽ sau đối thủ), chỗ xuất phát (sân)
        sealed class TtDaVo
        {
            public Vector2 u, tu;
            public float z, sz, ang, bay, gio;
            public int seed;
            public bool lua, vun;
        }

        readonly List<Vector3> ttHop = new List<Vector3>(24);   // cụm tròn của mây nấm (x, y, bán kính)
        readonly int[] ttNhom = new int[32];
        readonly Vector2[] ttCs = new Vector2[7];
        readonly float[] ttHw = new float[7];

        // ---------- toán ----------
        // độ lệch đo trong khung bản xem trước (đối thủ ở BÊN TRÁI tướng mình) → khung sân theo phía thật
        static Vector2 TtLat(Vector2 v, float dir) => new Vector2(-dir * v.x, v.y);

        // hệ số giờ: lead lệch giờ trúng của rig chỉ vì làm tròn khung thì giữ đúng giờ rig
        static float TtK(float lead, float tr) => Mathf.Abs(lead - tr) < 0.05f ? 1 : Mathf.Max(0.05f, lead) / tr;

        static float TtIo(float u)
        {
            u = Mathf.Clamp01(u);
            return u * u * (3 - 2 * u);
        }

        static float TtIn(float u)
        {
            u = Mathf.Clamp01(u);
            return u * u * u;
        }

        static float TtBao(float t, float t0, float t1, float vao, float ra) => TtIo((t - t0) / vao) * (1 - TtIo((t - (t1 - ra)) / ra));

        // độ lệch (x phải, y xuống) xoay theo góc ảnh (độ, ngược kim như Image)
        static Vector2 TtXoay(Vector2 v, float angDeg)
        {
            float a = angDeg * Mathf.Deg2Rad, c = Mathf.Cos(a), s = Mathf.Sin(a);
            return new Vector2(v.x * c + v.y * s, -v.x * s + v.y * c);
        }

        // ---------- trạng thái đối thủ do sân đọc (StageViewThoTinh.cs) ----------

        // mã kind là chiêu `goc` của Thổ Tinh ở dạng nào: 2 (kind == goc), 1 (kind == goc + "1"), 0 không phải
        public static int TinhDang(string kind, string goc) =>
            kind == null ? 0 : kind == goc ? 2 : kind.Length == goc.Length + 1 && kind[goc.Length] == '1' && kind.StartsWith(goc) ? 1 : 0;

        // vỏ đá quanh đối thủ: bán kính / bán kính lúc mới bọc ở giây rig t của clip skill (co 56 % khi ép, run nhẹ tới lúc nổ)
        static float TtVo(float t)
        {
            float u = TtIo((t - TtSkEp0) / (TtSkEp2 - TtSkEp0));
            float rr = t > TtSkEp0 && t < TtSkNo ? 0.012f * Mathf.Sin(t * 2 * Mathf.PI * 15) : 0;
            return 1 - 0.56f * u + rr;
        }

        // cỡ đối thủ (quanh giữa thân) ở giây t của clip skill Thổ Tinh (hai dạng): co theo vỏ đá từ lúc ép (bản xem trước nhảy ngay xuống 0,92;
        // ở đây vào êm trong 0,08 s), bật về 1 đúng lúc nổ
        public static float TinhCoDoiThu(float t) =>
            t < TtSkEp0 || t >= TtSkNo ? 1 : TtVo(t) * Mathf.Lerp(1, 0.92f, TtIo((t - TtSkEp0) / 0.08f));

        // độ hiện của đối thủ theo giờ clip chiêu cuối của Thổ Tinh: ẩn trong cầu lửa từ lúc nổ, rồi hiện MỜ DẦN sau làn khói đen (người dùng
        // 2026-11-18: "hiện tướng đằng sau khói đen mờ mờ cho mượt chứ không hiện tướng luôn")
        public const float TinhHien0 = TtSkNo + 0.45f, TinhHien1 = TtSkNo + 1.25f;
        public static float TinhHienDoiThu(float t) => t < TtSkNo ? 1 : t < TinhHien0 ? 0 : TtIo((t - TinhHien0) / (TinhHien1 - TinhHien0));

        // cầu lửa: bốn khối hợp tròn lồng nhau (vòng 9 cụm + cụm giữa, mép phập phồng), phình bật 0,16 s rồi bốc lên; lõi kem, vàng co lại trước
        // (lộ lớp cam, đỏ), lớp ngoài nguội thành than rồi nhạt hẳn (khói đen và mây nấm nối tiếp); chỉ lớp ngoài có viền mực
        readonly List<Vector3> ttCau = new List<Vector3>(12);
        void TtCauLua(Vector2 c0, float R1, float sc)
        {
            var p = new P { pos = c0, life = 1.05f, group = Front, sz = R1, ph = U(0, 6.28f) };
            p.draw = (q, k, buf) =>
            {
                float t = q.age, R = q.sz * EaseOut(Mathf.Min(1, t / 0.16f)) * (1 + 0.12f * t);
                var c = q.pos + new Vector2(0, -45 * sc * Mathf.Pow(t, 1.3f));
                float aInk = 1 - SmoothStep(0.55f, 0.9f, t), aFill = 1 - SmoothStep(0.75f, 1.05f, t);
                if (aFill < 0.03f || R < 1) return;
                for (int lop = 0; lop < 4; lop++)
                {
                    float co = lop == 0 ? 1 : lop == 1 ? 0.8f * (1 - 0.6f * SmoothStep(0.35f, 0.85f, t))
                        : lop == 2 ? 0.58f * (1 - SmoothStep(0.25f, 0.7f, t)) : 0.36f * (1 - SmoothStep(0.18f, 0.55f, t));
                    float r = R * co;
                    if (r < 1.5f) continue;
                    ttCau.Clear();
                    for (int i = 0; i < 12; i++)                                 // 12 múi to nhỏ không đều: mép lồi lõm như cụm lửa nổ
                    {
                        float h1 = Mathf.Repeat(Mathf.Sin(i * 12.9898f + q.ph) * 43758.55f, 1f), h2 = Mathf.Repeat(Mathf.Sin(i * 78.233f + q.ph) * 12543.1f, 1f);
                        float a = q.ph + i * 0.5236f + 0.18f * Mathf.Sin(t * 6 + i), ro = r * (0.42f + 0.22f * h1);
                        float rc = r * (0.3f + 0.26f * h2) * (1 + 0.14f * Mathf.Sin(i * 1.7f + t * 10 + lop));
                        ttCau.Add(new Vector3(c.x + ro * Mathf.Cos(a), c.y + ro * 0.9f * Mathf.Sin(a), rc));
                    }
                    ttCau.Add(new Vector3(c.x, c.y, 0.62f * r));
                    var col = lop == 0 ? Color.Lerp(TtLuaC[0], TtThan, SmoothStep(0.4f, 0.9f, t)) : TtLuaC[lop];
                    TtVeHop(Front, 38.5f + 0.1f * lop, ttCau, col, aFill, lop == 0 ? aInk : 0);
                }
            };
            Add(p);
        }

        // đối thủ bẹp khi hai nắm đấm nện (u: giây kể từ khung trúng của đòn thường): bẹp ngay (1,14 × 0,80), nảy cao (0,94 × 1,06), về
        public static bool TinhBep(float u, out float sx, out float sy)
        {
            sx = sy = 1;
            if (u < 0 || u > 0.26f) return false;
            Vector2 a = new Vector2(1.14f, 0.80f), b = new Vector2(0.94f, 1.06f), s;
            if (u < 0.09f) s = a;
            else if (u < 0.16f) s = Vector2.Lerp(a, b, TtIo((u - 0.09f) / 0.07f));
            else s = Vector2.Lerp(b, Vector2.one, TtIo((u - 0.16f) / 0.10f));
            sx = s.x;
            sy = s.y;
            return true;
        }

        // mảnh bay gần nhất đã cắm (chiêu mana Thổ Tinh, dang1: dạng 1) ở giây t của clip cast; lead: giờ trúng game dùng. since: giây từ lúc cắm
        public static bool TinhLuoiCam(bool dang1, float t, float lead, out float since, out bool cuoi)
        {
            since = 0;
            cuoi = false;
            var d = dang1 ? TtD1 : TtD2;
            float k = TtK(lead, TtCaTr);
            int nn = d.idx.Length;
            for (int n = nn - 1; n >= 0; n--)
            {
                float th = (TtBan0 + d.banCach * n + TtBay) * k;
                if (t < th) continue;
                since = t - th;
                cuoi = n == nn - 1;
                return since < 0.2f;
            }
            return false;
        }

        // ---------- vật liệu ----------

        // đá trăng như vệ tinh / nắm đấm của rig: khối tròn méo viền mực, mặt bên sẫm (xoay theo hòn đá), hai hố; vun: mảnh vụn dẹt. r: bán kính
        void TtVeDa(List<Item> buf, int g, float layer, Vector2 pos, float r, float ang, int seed, float a, bool vun)
        {
            if (r < 0.8f || a < 0.03f) return;
            int si = seed & 3;
            float st = vun ? 1.35f : 1f, ink = Mathf.Min(4.2f, 2f + r * 0.06f);
            Put(buf, g, layer, S("solid_" + si), Ink, pos, 2 * r + ink, (2 * r * st + ink) / (2 * r + ink), ang, a);
            Put(buf, g, layer + 0.01f, S("blob_" + si), TtHo, pos, 2 * r, st, ang, a);
            Put(buf, g, layer + 0.02f, S("blob_" + si), TtMat, pos + TtXoay(new Vector2(-0.1f * st, -0.1f) * r, ang), 1.8f * r, st, ang, a);
            if (r < 6) return;
            for (int j = 0; j < 2; j++)
            {
                var o = j == 0 ? new Vector2(-0.32f * st, -0.22f) : new Vector2(0.22f * st, 0.2f);
                float rc = (j == 0 ? 0.2f : 0.26f) * r;
                var c = pos + TtXoay(o * r, ang);
                if (r >= 10) Put(buf, g, layer + 0.03f + j * 0.002f, S("solid_" + ((si + j + 1) & 3)), Ink, c, 2 * rc + 1.6f, 1, ang + 40 * j, a);
                Put(buf, g, layer + 0.031f + j * 0.002f, S("blob_" + ((si + j + 1) & 3)), TtHo, c, 2 * rc, 1, ang + 40 * j, a);
            }
        }

        // hòn đá trăng văng: rơi có trọng lực, chạm đất nảy một lần rồi nằm, mờ ở 28 % cuối
        void TtDaVang(Vector2 pos, Vector2 vel, float r, float life, float ground, int group, float ang0, bool vun, int seed)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, acc = new Vector2(0, 900), ground = ground, bounce = 0.35f, spin = U(-9, 9), drag = 0.3f,
                group = group, sz = r, ph = ang0, seed = seed, crust = vun
            };
            p.draw = (q, k, buf) => TtVeDa(buf, q.group, 46, q.pos, q.sz, q.ph + q.ang * Mathf.Rad2Deg, q.seed, 1 - Mathf.Max(0, k - 0.72f) / 0.28f, q.crust);
            Add(p);
        }

        // sao chớp kem viền mực (mảng 10 đỉnh như bản xem trước), 0,12 s
        void TtSao(Vector2 c, float r)
        {
            var p = new P { pos = c, life = 0.12f, group = Front, sz = r, ang = U(0, 6.28f) };
            p.draw = (q, k, buf) =>
            {
                float rr = q.sz * (0.85f + 0.3f * EaseOut(k / 0.5f));
                int s0 = mp.Count;
                for (int j = 0; j < 10; j++)
                {
                    float a = q.ang + j * Mathf.PI / 5, rj = (j & 1) == 0 ? rr : rr * 0.42f;
                    mp.Add(q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rj);
                }
                MSolid(Front, 60, s0, 10, ToKem, 1, 2.2f);
            };
            Add(p);
        }

        // dải cung elip (bán trục ea theo f, eb theo n) từ −52° tới 52° quanh f, nằm giữa hai độ lệch o0 < o1 so với elip
        void TtCung(Vector2 c, Vector2 f, Vector2 n, float ea, float eb, float o0, float o1, Color col, float al)
        {
            const int N = 9;
            int a0 = mp.Count;
            for (int i = 0; i < N; i++)
            {
                float ph = (-52 + 104f * i / (N - 1)) * Mathf.Deg2Rad;
                mp.Add(c + f * ((ea + o1) * Mathf.Cos(ph)) + n * ((eb + o1) * Mathf.Sin(ph)));
            }
            int b0 = mp.Count;
            for (int i = 0; i < N; i++)
            {
                float ph = (-52 + 104f * i / (N - 1)) * Mathf.Deg2Rad;
                mp.Add(c + f * ((ea + o0) * Mathf.Cos(ph)) + n * ((eb + o0) * Mathf.Sin(ph)));
            }
            MRibbon(Front, 58, a0, b0, N, col, al);
        }

        // một cung sóng gầm: phình từ miệng về phía trước (f), tan dần. Ảnh kr_songam (dải cung lồi +x) nếu đã nhập; không thì mảng liền hình
        // lưỡi liềm THON hai đầu (dày giữa, nhọn mũi), một viền mực ngoài (người dùng 2026-11-18: "sóng âm chưa đẹp": bỏ dải đều hai viền như ống)
        void TtSongGam(Vector2 m, Vector2 f, float s)
        {
            var p = new P { pos = m, life = 0.42f, group = Front, aim = f, sz = s, seed = rng.Next(4) };
            p.draw = (q, k, buf) =>
            {
                float r = (22 + 135 * EaseOut(k)) * q.sz, a = Mathf.Pow(1 - k, 1.2f);
                if (a < 0.03f) return;
                var ff = q.aim;
                var n = new Vector2(-ff.y, ff.x);
                var c = q.pos + ff * (0.2f * r);
                var sp = S("kr_songam_" + q.seed);
                if (sp != null)
                {
                    float ang = VelAng(ff), w = 0.55f * r, h = 2 * r;
                    Put(buf, Front, 58, SK("kr_songams_" + q.seed, "kr_songam_" + q.seed), Ink, c + ff * (0.45f * r), h + 4, (w + 4) / (h + 4), ang, a);
                    Put(buf, Front, 58.1f, sp, ToKem, c + ff * (0.45f * r), h, w / h, ang, a);
                    return;
                }
                const int N = 11;
                float bw = (6.5f - 3f * k) * q.sz, ea = 0.62f * r;
                int s0 = mp.Count;
                for (int i = 0; i < N; i++)
                {
                    float u = i / (N - 1f), ph = (-56 + 112 * u) * Mathf.Deg2Rad, t = Mathf.Sin(Mathf.PI * u);
                    mp.Add(c + ff * ((ea + bw * t) * Mathf.Cos(ph)) + n * ((r + bw * t) * Mathf.Sin(ph)));
                }
                for (int i = N - 2; i >= 1; i--)
                {
                    float u = i / (N - 1f), ph = (-56 + 112 * u) * Mathf.Deg2Rad, t = Mathf.Sin(Mathf.PI * u);
                    mp.Add(c + ff * ((ea - bw * t) * Mathf.Cos(ph)) + n * ((r - bw * t) * Mathf.Sin(ph)));
                }
                MSolid(Front, 58, s0, mp.Count - s0, ToKem, a, 2f);
            };
            Add(p);
        }

        // mảnh bay (lưỡi trăng dạng 2 / mảnh vỏ dạng 1; mảng theo đường viền ảnh của dạng): c = tâm khung ảnh trên sân, d = hướng đáy → đỉnh ảnh
        // (sân), dir: phía đối thủ (ảnh lật khi đối thủ ở bên trái), h / w: cao / rộng khung ảnh. full: viền mực + mặt bên sẫm + hố; không full:
        // bóng mờ một màu (không lớp nào chồng nên mờ được)
        void TtVeManh(TtDang dg, List<Item> buf, float layer, Vector2 c, Vector2 d, float dir, float h, float w, float al, bool full)
        {
            if (al < 0.03f) return;
            var side = new Vector2(-d.y, d.x) * dir;
            Vector2 L(Vector2 uv) => c + d * ((uv.y - 0.5f) * h) + side * (uv.x * w);
            var tr = dg.trai;
            var ph = dg.phai;
            int s0 = mp.Count;
            for (int i = 0; i < tr.Length; i++) mp.Add(L(tr[i]));
            for (int i = ph.Length - 1; i >= 1; i--) mp.Add(L(ph[i]));
            int n = mp.Count - s0;
            if (!full)
            {
                MFill(Front, layer, s0, n, TtMat, al, true);
                return;
            }
            MSolid(Front, layer, s0, n, TtMat, al, 2.2f);
            int s1 = mp.Count;                                                  // mặt bên sẫm dọc mép phải (lõm của lưỡi / mép vỡ của vỏ)
            for (int i = 0; i < ph.Length; i++) mp.Add(L(ph[i]));
            for (int i = ph.Length - 2; i >= 1; i--)
            {
                var uv = ph[i];
                float b = dg.vo ? Mathf.Clamp01((0.99f - uv.y) / 0.12f) : Mathf.Max(0, Mathf.Sin(Mathf.PI * (uv.y - 0.06f) / 0.92f));
                mp.Add(L(new Vector2(uv.x - dg.matBen * b, uv.y)));
            }
            MFill(Front, layer + 0.002f, s1, mp.Count - s1, TtHo, al, false);
            for (int j = 0; j < dg.ho.Length; j++)                              // hố
            {
                var ho = dg.ho[j];
                var hp = L(new Vector2(ho.x, ho.y));
                float r = ho.z * h;
                Put(buf, Front, 47.5f + j * 0.01f, S("solid_" + j), Ink, hp, 2 * r + 2, 1, 0, al);
                Put(buf, Front, 47.505f + j * 0.01f, S("blob_" + j), TtHo, hp, 2 * r, 1, 0, al);
            }
        }

        // đuôi thiên thạch: dải liền thon dần theo đường bay (tu → b, phần quãng f^1.6), lửa: mực + cam đỏ + vàng + kem, mép gợn; bụi: be + kem
        // be mờ 0,8, không viền. Ngắn lại khi sắp bám
        void TtDuoi(Vector2 tu, Vector2 b, float f, float sz, bool lua, float t)
        {
            float dai = (lua ? 0.22f : 0.32f) * (1 - 0.6f * Mathf.Max(0, f - 0.8f) / 0.2f);
            for (int i = 0; i < 7; i++) ttCs[i] = tu + (b - tu) * Mathf.Pow(Mathf.Max(0, f - dai * i / 6), 1.6f);
            if ((ttCs[0] - ttCs[6]).magnitude <= 6) return;
            float w0 = sz * (lua ? 0.36f : 0.24f);
            int nl = lua ? 4 : 2;
            for (int lop = 0; lop < nl; lop++)
            {
                float kw;
                Color col;
                float al = 1, them = 0;
                int pha;
                if (lua)
                {
                    kw = lop <= 1 ? 1 : lop == 2 ? 0.76f : 0.46f;                   // lõi kem rộng (người dùng 2026-11-18: "màu tươi hơn")
                    col = lop == 0 ? Ink : TtLua[lop == 1 ? 1 : lop == 2 ? 2 : 3];
                    them = lop == 0 ? 2.2f : 0;
                    pha = Mathf.Max(0, lop - 1);
                }
                else
                {
                    kw = lop == 0 ? 1 : 0.55f;
                    col = lop == 0 ? TtBui3 : TtBui4;
                    al = 0.8f;
                    pha = lop;
                }
                for (int i = 0; i < 7; i++)
                {
                    float gon = lua ? 1 + 0.28f * Mathf.Sin(i * 1.9f + t * 38 + pha) : 1;
                    ttHw[i] = w0 * kw * Mathf.Pow(1 - i / 6f, 0.8f) * gon + them;
                }
                int a0 = mp.Count;
                for (int i = 0; i < 7; i++)
                {
                    var dv = ttCs[Mathf.Max(0, i - 1)] - ttCs[Mathf.Min(6, i + 1)];
                    var nn = new Vector2(-dv.y, dv.x) / Mathf.Max(1e-3f, dv.magnitude);
                    mp.Add(ttCs[i] + nn * ttHw[i]);
                }
                int b0 = mp.Count;
                for (int i = 0; i < 7; i++)
                {
                    var dv = ttCs[Mathf.Max(0, i - 1)] - ttCs[Mathf.Min(6, i + 1)];
                    var nn = new Vector2(-dv.y, dv.x) / Mathf.Max(1e-3f, dv.magnitude);
                    mp.Add(ttCs[i] - nn * ttHw[i]);
                }
                MRibbon(Front, 48 + lop * 0.01f, a0, b0, 7, col, al);
            }
        }

        // sỏi trăng nổi lên dưới chân lúc tướng bay lên: trôi lên chậm, xoay, hiện nhanh rồi nhạt dần
        void TtSoiNoi(Vector2 p0, float s)
        {
            var p = new P
            {
                pos = p0, vel = new Vector2(U(-10, 10), U(-90, -50)) * s, life = U(0.9f, 1.4f), drag = 0.8f, spin = U(-3, 3),
                group = U(0, 1) < 0.5f ? Back : Front, sz = 0.47f * U(6, 11) * s, seed = rng.Next(4), ph = U(0, 360)
            };
            p.draw = (q, k, buf) => TtVeDa(buf, q.group, 44, q.pos, q.sz, q.ph + q.ang * Mathf.Rad2Deg, q.seed, Mathf.Min(1, Mathf.Min(k * 6, (1 - k) * 3)), true);
            Add(p);
        }

        // hơi nóng bốc lên quanh mặt trời: hai nét lượn mảnh màu kem, uốn liên tục, hiện dần rồi nhạt dần
        void TtHoiNong(Vector2 p0, float h)
        {
            var p = new P { pos = p0, vel = new Vector2(U(-6, 6), -U(45, 75)), life = U(1.1f, 1.5f), drag = 0.3f, group = Back, ph = U(0, 24), sz = h, wd = U(6, 9) };
            p.draw = (q, k, buf) =>
            {
                float a = Mathf.Min(1, Mathf.Min(k / 0.25f, (1 - k) / 0.35f)) * 0.75f;
                if (a < 0.03f) return;
                float hh = q.sz * (0.85f + 0.3f * k);
                for (int i = 0; i < 2; i++)
                {
                    var o = q.pos + new Vector2((i - 0.5f) * q.wd, i * 5);
                    const int N = 7;
                    int a0 = mp.Count;
                    for (int j = 0; j < N; j++)
                    {
                        float y = (j / (N - 1f) - 0.5f) * hh;
                        mp.Add(o + new Vector2(Mathf.Sin(y * 0.35f + q.age * 8 + q.ph + i) * 2.2f - 0.8f, y));
                    }
                    int b0 = mp.Count;
                    for (int j = 0; j < N; j++)
                    {
                        float y = (j / (N - 1f) - 0.5f) * hh;
                        mp.Add(o + new Vector2(Mathf.Sin(y * 0.35f + q.age * 8 + q.ph + i) * 2.2f + 0.8f, y));
                    }
                    MRibbon(Back, 39, a0, b0, N, TtHoi, a);
                }
            };
            Add(p);
        }

        // ---------- hợp các hình tròn (mây nấm) ----------

        int TtGoc(int x)
        {
            while (ttNhom[x] != x) x = ttNhom[x] = ttNhom[ttNhom[x]];
            return x;
        }

        void TtCungTron(Vector3 c, float th, float span, float buoc)
        {
            buoc = Mathf.Clamp(5f / Mathf.Max(0.5f, c.z), buoc, 1.2f);          // dây cung ~5 đơn vị sân: cụm nhỏ ít điểm
            int m = Mathf.Max(1, Mathf.CeilToInt(span / buoc));
            for (int q = 0; q < m; q++)
            {
                float a = th + span * q / m;
                mp.Add(new Vector2(c.x + c.z * Mathf.Cos(a), c.y + c.z * Mathf.Sin(a)));
            }
        }

        // đường viền ngoài của một cụm tròn chạm nhau (gốc nhóm goc): bắt đầu ở đỉnh cao nhất (chắc nằm trên viền ngoài), đi theo chiều tăng góc
        // trên đường tròn đang đi tới chỗ đi vào đường tròn khác của cụm thì chuyển sang nó, tới khi về chỗ đầu. Lỗ bên trong bị lấp. Thêm điểm
        // vào mp, trả số điểm (0: không dựng được)
        int TtVien(List<Vector3> cs, int goc, float buoc)
        {
            const float Tau = 2 * Mathf.PI;
            int n = cs.Count, s = -1;
            for (int i = 0; i < n; i++)
                if (cs[i].z > 0.5f && TtGoc(i) == goc && (s < 0 || cs[i].y - cs[i].z < cs[s].y - cs[s].z)) s = i;
            if (s < 0) return 0;
            int s0 = mp.Count, ci = s;
            float th = -Mathf.PI / 2, th0 = th;
            for (int lap = 0; lap < 96; lap++)
            {
                var c = cs[ci];
                float best = float.MaxValue;
                int bj = -1;
                for (int j = 0; j < n; j++)
                {
                    if (j == ci || cs[j].z <= 0.5f || TtGoc(j) != goc) continue;
                    var cj = cs[j];
                    float dx = cj.x - c.x, dy = cj.y - c.y, d = Mathf.Sqrt(dx * dx + dy * dy);
                    if (d >= c.z + cj.z || d <= Mathf.Abs(c.z - cj.z)) continue;
                    float cosd = (d * d + c.z * c.z - cj.z * cj.z) / (2 * d * c.z);
                    float e = Mathf.Atan2(dy, dx) - Mathf.Acos(Mathf.Clamp(cosd, -1, 1)); // đi theo chiều tăng góc thì vào đường tròn j ở đây
                    float dd = Mathf.Repeat(e - th, Tau);
                    if (dd < 1e-4f) dd += Tau;
                    if (dd < best)
                    {
                        best = dd;
                        bj = j;
                    }
                }
                if (ci == s && lap > 0)
                {
                    float rem = Mathf.Repeat(th0 - th, Tau);
                    if (rem <= best)
                    {
                        TtCungTron(c, th, rem, buoc);
                        return mp.Count - s0;
                    }
                }
                if (bj < 0)
                {
                    if (ci == s && lap == 0)
                    {
                        TtCungTron(c, th, Tau, buoc);
                        return mp.Count - s0;
                    }
                    break;
                }
                TtCungTron(c, th, best, buoc);
                float te = th + best;
                var cn = cs[bj];
                th = Mathf.Atan2(c.y + c.z * Mathf.Sin(te) - cn.y, c.x + c.z * Mathf.Cos(te) - cn.x);
                ci = bj;
            }
            mp.RemoveRange(s0, mp.Count - s0);
            return 0;
        }

        // vẽ hợp các hình tròn cs (x, y, bán kính): mỗi cụm chạm nhau một mảng liền có viền mực ngoài; aFill: độ đậm cả khối, aInk: viền
        void TtVeHop(int g, float layer, List<Vector3> cs, Color col, float aFill, float aInk)
        {
            int n = Mathf.Min(cs.Count, ttNhom.Length);
            for (int i = 0; i < n; i++) ttNhom[i] = i;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++)
                {
                    if (cs[i].z <= 0.5f || cs[j].z <= 0.5f) continue;
                    float dx = cs[j].x - cs[i].x, dy = cs[j].y - cs[i].y;
                    float rs = cs[i].z + cs[j].z;
                    if (dx * dx + dy * dy >= rs * rs) continue;
                    int a = TtGoc(i), b = TtGoc(j);
                    if (a != b) ttNhom[Mathf.Max(a, b)] = Mathf.Min(a, b);
                }
            for (int i = 0; i < n; i++)
            {
                if (cs[i].z <= 0.5f || TtGoc(i) != i) continue;
                int s0 = mp.Count, m = TtVien(cs, i, 0.22f);
                if (m < 3) continue;
                if (aInk > 0.03f) MBand(g, layer, MGrow(s0, m, 2.4f), s0, m, Ink, aFill * aInk, true);
                MFill(g, layer + 0.001f, s0, m, col, aFill, aInk < 0.5f);
            }
        }

        // mây nấm dựng hình (bản xem trước ve_nam): cột 5 cụm từ chỗ nổ lên tới mũ, mũ vòm 9 cụm, 4 cụm cuộn dưới mép; bốc lên, nở rồi co, màu
        // lửa → khói lửa → than → xám theo tuổi; cả khối trong 0,82 (phủ lên đối thủ), viền nhạt trước, rồi cả khối nhạt dần (không vụt tắt)
        void TtNam(Vector2 c0, float s)
        {
            var p = new P { pos = c0, life = 2.2f, group = Front, sz = s };
            p.draw = (q, k, buf) =>
            {
                float t = q.age, sc = q.sz;
                float aFill = 1 - SmoothStep(1.5f, 2.15f, t), aInk = 1 - SmoothStep(1.3f, 1.9f, t);
                if (aFill < 0.03f) return;
                float len = EaseOut(Mathf.Min(1, t / 0.55f));
                float yMu = q.pos.y - (14 + 64 * len + 5 * t) * sc;
                float no = EaseOut(Mathf.Min(1, t / 0.6f)) * (1 + 0.1f * t);
                float tan = 1 - 0.55f * SmoothStep(1.1f, 2.1f, t);
                float Wm = 70 * no * sc, Hm = 34 * no * sc;
                ttHop.Clear();
                for (int i = 0; i < 5; i++)
                {
                    float f = (i + 0.5f) / 5;
                    ttHop.Add(new Vector3(q.pos.x + 4 * sc * Mathf.Sin(t * 5 + i), q.pos.y + (yMu + Hm * 0.3f - q.pos.y) * f, (19 + 5 * (1 - f)) * no * sc * tan));
                }
                foreach (var o in TtNamCuon) ttHop.Add(new Vector3(q.pos.x + o.x * Wm, yMu + o.y * Hm, 13 * no * sc * tan));
                for (int j = 0; j < TtNamMu.Length; j++)
                    ttHop.Add(new Vector3(q.pos.x + TtNamMu[j].x * Wm, yMu + TtNamMu[j].y * Hm, (19 + 4 * ((j * 7) % 3)) * no * sc * tan));
                var col = Ramp(TtNamC, Mathf.Pow(Mathf.Min(1, Mathf.Max(0, t - 0.28f) / 1.7f), 0.8f));
                TtVeHop(Front, 40, ttHop, col, 0.82f * aFill, aInk);
            };
            Add(p);
        }

        // ================= ĐÁNH THƯỜNG "Thiên Chuỳ": nhảy lên, lao tới, nện hai nắm đấm mặt trăng xuống người đối thủ =================
        public float NTinhNen(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            TtNen(TtD2, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        // dạng 1 (Tiểu Thổ Tinh): nắm đấm nhỏ hơn, nhẹ hơn
        public float NTinhNen1(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            TtNen(TtD1, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        float TtNen(TtDang dg, Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), k = TtK(L, TtAtTr), dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float sC = casterH / TtCaoXem, sc = tH / 150f, m = dg.muc;
            // rời đất: vòng bụi, bụi hai bên chân
            At(TtAtTu * k + 0.04f, () =>
            {
                ToVong(casterFeet, 80 * sC, 0.45f);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(casterFeet + new Vector2(d * 28 * sC, -2), new Vector2(d * 80, -25) * sC, 16 * sC, 3);
            });
            // nện: hai nắm đấm ở đỉnh cú lao (72 % quãng) + chỗ đo trên rig
            At(L, () =>
            {
                var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f);
                Vector2 a = ToSan(toi, casterH, dir, dg.nam1), b = ToSan(toi, casterH, dir, dg.nam2);
                var dat = new Vector2(0.5f * (a.x + b.x), foeFeet.y + 4 * sc);
                ToNo(foeBody + TtLat(new Vector2(4, 10), dir) * sc, foeFeet.y, tH, 1.6f * m, TtDa, TtDa2, new Vector2(dir * 0.4f, 1));
                ToVong(dat, 120 * sc * (0.8f + 0.2f * m), 0.55f);
                ToHo(dat, 44 * sc * (0.8f + 0.2f * m));
                for (int d = -1; d <= 1; d += 2)
                {
                    ToNut(dat, dat + new Vector2(d * 70 * (0.8f + 0.2f * m), U(-8, 10)) * sc, 0.16f, sc);
                    ToCum(dat + new Vector2(d * 30, -4) * sc, new Vector2(d * 110, -30) * sc, 18 * sc, 4);
                }
                for (int f = 0; f < 2; f++)
                {
                    var p = f == 0 ? a : b;
                    for (int j = 0; j < 2; j++)
                        ToSoiCum(p, new Vector2(U(-220, 220), U(-300, -140)) * sc, U(3.4f, 4.8f) * sc, TtDa, TtDa2, foeFeet.y + U(-4, 10) * sc, (j & 1) == 0 ? Front : Back);
                }
                Shake?.Invoke(0.3f * m);                                        // rig khai thêm impactShake 0,23
                FlashScreen?.Invoke(new Color(1, 0.965f, 0.84f, 0.25f * m));
            });
            return L;
        }

        // ================= CHIÊU MANA "Nguyệt Nhận": gầm, lưỡi trăng (dạng 1: mảnh vỏ) bứt khỏi lưng, lần lượt phóng vào đối thủ =================
        public float NTinhGai(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            TtGai(TtD2, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        // dạng 1 (Tiểu Thổ Tinh): sáu mảnh vỏ vỡ, giãn cách 0,08 s
        public float NTinhGai1(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            TtGai(TtD1, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        float TtGai(TtDang dg, Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float k = TtK(lead, TtCaTr), dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float sC = casterH / TtCaoXem, tGoi = T;
            // sóng gầm: cung kem phình ra từ miệng, hướng giữa phía trước và đối thủ
            Every(TtGam0 * k, TtGam1 * k, 9, x =>
            {
                float tr = (T - tGoi) / k;
                var mo = ToSan(casterFeet, casterH, dir, ToDiem(dg.mieng, 0.30f, 0.05f, tr) + dg.miengLech);
                var f = Unit(Vector2.Lerp(new Vector2(dir, 0), Unit(foeBody - mo), 0.5f));
                TtSongGam(mo, f, sC);
            });
            // đất rung: sỏi nảy, bụi dưới chân
            Every(TtGam0 * k, 0.95f * k, 14 * dg.muc, x =>
            {
                var p = casterFeet + new Vector2(-dir * U(-90, 70) * sC, U(-4, 6));
                ToSoi(p, new Vector2(U(-30, 30), U(-150, -80)) * sC, U(2f, 3.4f) * sC, U(0, 1) < 0.5f ? TtDa : TtDa2, p.y);
                if (U(0, 1) < 0.45f) ToBui(p, new Vector2(U(-30, 30), -24) * sC, 0.55f, 8 * sC, 16 * sC, Back, false);
            });
            At(TtGam0 * k, () => Shake?.Invoke(0.25f * dg.muc));
            int nn = dg.idx.Length;
            // mảnh bứt khỏi vành: vụn + bụi ở đế
            for (int n = 0; n < nn; n++)
            {
                var tach = dg.tach[n];
                At((TtTach0 + TtTachCach * dg.idx[n] + 0.02f) * k, () =>
                {
                    var p = ToSan(casterFeet, casterH, dir, tach);
                    for (int j = 0; j < 2; j++)
                        ToSoi(p, new Vector2(U(-90, 90), U(-140, -40)) * sC, U(2.5f, 4) * sC, TtDa2, casterFeet.y + U(-2, 8), 0, (j & 1) == 0 ? Front : Back);
                    ToBui(p, new Vector2(U(-20, 20), -30) * sC, 0.45f, 5 * sC, 12 * sC, Back);
                });
            }
            // phóng: theo thứ tự của rig (mảnh phía trước trước), đúng lúc rig ẩn
            for (int n = 0; n < nn; n++)
            {
                int ni = n;
                At((TtBan0 + dg.banCach * n) * k, () => TtManhBay(dg, ni, ni == nn - 1, casterFeet, casterH, dir, foeFeet, foeBody, tH, TtBay * k));
            }
            return (TtBan0 + TtBay) * k;
        }

        // một mảnh bay (thứ n theo thứ tự phóng): từ đúng khung ảnh lúc rig ẩn nó, đường f^1.5 cong nhẹ tới giữa thân đối thủ trong `bay` giây;
        // trục ảnh xoay từ hướng lúc rời sang hướng bay thật trong 1/4 quãng đầu; ba bóng mờ phía sau, vệt bụi; tới nơi CẮM (lún vào 18 %),
        // 0,08 s sau tan, vỡ
        void TtManhBay(TtDang dg, int n, bool cuoi, Vector2 casterFeet, float casterH, float dir, Vector2 foeFeet, Vector2 foeBody, float tH, float bay)
        {
            float sc = tH / 150f, h = dg.cao[n] * casterH, w = dg.rong[n] * casterH, m = dg.muc;
            float g = dg.goc[n] * Mathf.Deg2Rad;
            var d0 = new Vector2(dir * Mathf.Cos(g), -Mathf.Sin(g));
            var a0 = ToSan(casterFeet, casterH, dir, dg.ban[n]);
            var b0 = foeBody + new Vector2(U(-12, 12), U(-16, 14)) * sc;
            var ab = b0 - a0;
            var nrm = new Vector2(-ab.y, ab.x) / Mathf.Max(1, ab.magnitude);
            float vong = U(-14, 14) * sc, g0 = Mathf.Atan2(d0.y, d0.x) * Mathf.Rad2Deg;
            Vector2 Vi(float f) => a0 + ab * Mathf.Pow(Mathf.Max(0, f), 1.5f) + nrm * (vong * Mathf.Sin(Mathf.PI * Mathf.Clamp01(f)));
            Vector2 Mui(float f)
            {
                var hv = f < 0.04f ? Vi(0.04f) - a0 : Vi(f) - Vi(f - 0.04f);
                float g1 = Mathf.Atan2(hv.y, hv.x) * Mathf.Rad2Deg;
                float a = (g0 + Mathf.DeltaAngle(g0, g1) * TtIo(f / 0.25f)) * Mathf.Deg2Rad;
                return new Vector2(Mathf.Cos(a), Mathf.Sin(a));
            }
            var p = new P { pos = a0, life = bay + 0.12f, group = Front };
            p.draw = (q, k, buf) =>
            {
                float f = Mathf.Min(1, q.age / bay);
                if (f < 1)
                {
                    for (int j = 3; j >= 1; j--)                                 // bóng mờ phía sau (vệt tốc độ)
                    {
                        float fj = f - 0.11f * j;
                        if (fj > 0) TtVeManh(dg, buf, 46 + 0.01f * (3 - j), Vi(fj), Mui(fj), dir, h, w, j == 1 ? 0.42f : j == 2 ? 0.24f : 0.12f, false);
                    }
                    TtVeManh(dg, buf, 48, Vi(f), Mui(f), dir, h, w, 1, true);
                }
                else
                {
                    var u = Unit(ab);
                    TtVeManh(dg, buf, 48, b0 - u * (h * 0.18f), u, dir, h, w, 1 - Mathf.Max(0, (q.age - bay - 0.08f) / 0.04f), true);
                }
            };
            p.upd = (q, dt, s) =>                                                  // vệt bụi liền theo quãng mảnh vừa bay (KR5), cụm đứng tại chỗ
            {
                if (q.age >= bay) return;
                float f = q.age / bay, buoc = 8 * sc;
                var vi = Vi(f);
                q.R0 += (vi - q.home).magnitude;
                q.home = vi;
                if (q.R0 < buoc || f < 0.03f) return;
                q.R0 -= buoc;
                var c = s.ToBui(vi - Mui(f) * (0.3f * h), new Vector2(s.U(-12, 12), -s.U(10, 26)) * sc, s.U(0.32f, 0.42f), 4 * sc, s.U(7, 10) * sc, Front, false);
                c.col = TtBui4;
            };
            p.home = a0;
            Add(p);
            At(bay, () =>
            {
                Shake?.Invoke((cuoi ? 0.35f : 0.1f) * m);
                TtSao(b0, 14 * sc * (cuoi ? 1.6f : 1) * (0.85f + 0.15f * m));
                ToVongVa(b0, (cuoi ? 0.5f : 0.36f) * tH);
                ToBong(b0, ab, (cuoi ? 0.5f : 0.38f) * tH, TtMat);
                At(0.10f, () =>
                {
                    for (int j = 0; j < 3; j++)
                        TtDaVang(b0, new Vector2(U(-160, 160), U(-220, -60)) * sc, 0.5f * h * U(0.18f, 0.28f), 0.7f, foeFeet.y + U(-4, 8) * sc, Front, U(0, 360),
                            true, rng.Next(4));
                    ToSoiCum(b0, new Vector2(-Mathf.Sign(ab.x) * U(60, 160), U(-220, -120)) * sc, U(3f, 4f) * sc, TtDa, TtDa2, foeFeet.y + U(-4, 8) * sc);
                    ToCum(b0, new Vector2(U(-30, 30), -30) * sc, 11 * sc * (cuoi ? 1.4f : 1), cuoi ? 4 : 3, Back);
                });
            });
        }

        // ================= CHIÊU CUỐI "Hằng Tinh Diệt" =================
        public float NTinhHang(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            TtHang(TtD2, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        // dạng 1 (Tiểu Thổ Tinh): cùng nhịp, nổ / rung / chớp nhẹ hơn
        public float NTinhHang1(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            TtHang(TtD1, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        float TtHang(TtDang dg, Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = TtK(L, TtSkNo), dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float sC = casterH / TtCaoXem, sc = tH / 150f, tGoi = T, tNoAbs = T + L, RS0 = 0.62f * tH, m = dg.muc, mo = 0.8f + 0.2f * m;
            var C0 = foeBody;
            float Tr() => (T - tGoi) / k;
            Vector2 ChoBam(TtDaVo d, float tr)                                   // chỗ bám của hòn d: vỏ xoay chậm, co khi ép
            {
                float a = 0.25f * (tr - TtSkHut), cs = Mathf.Cos(a), sn = Mathf.Sin(a);
                var v = new Vector2(d.u.x * cs - d.u.y * sn, (d.u.x * sn + d.u.y * cs) * 0.96f);
                return C0 + TtLat(v, dir) * (RS0 * TtVo(tr));
            }

            // 1. bay lên: vòng bụi, bụi hai bên; sỏi trăng nổi lên dưới chân theo
            At(TtSkBay0 * k, () =>
            {
                ToVong(casterFeet, 90 * sC, 0.6f);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(casterFeet + new Vector2(d * 26 * sC, -2), new Vector2(d * 70, -30) * sC, 17 * sC, 3);
            });
            Every(TtSkBay0 * k, TtSkEp0 * k, 9, x => TtSoiNoi(casterFeet + new Vector2(-dir * U(-80, 60) * sC, U(-2, 6)), sC));

            // 2. 45 thiên thạch / đá trăng: vành trước (14), nửa sau (9), lấp mặt trước (22); lao từ trời / phía xa tướng mình tới chỗ bám
            var da = new List<TtDaVo>(45);
            for (int j = 0; j < 14; j++)
            {
                float a = 2 * Mathf.PI * j / 14 + U(-0.12f, 0.12f);
                da.Add(new TtDaVo { u = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(0.86f, 1f), z = U(-0.1f, 0.25f) });
            }
            for (int j = 0; j < 9; j++)
            {
                float a = 2 * Mathf.PI * (j + 0.5f) / 9;
                da.Add(new TtDaVo { u = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(0.55f, 0.8f), z = -0.8f });
            }
            for (int j = 0; j < 22; j++)
            {
                float r = Mathf.Sqrt((j + 0.5f) / 22) * 0.82f, a = j * 2.39996f + U(-0.2f, 0.2f);
                da.Add(new TtDaVo { u = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * r, z = Mathf.Sqrt(Mathf.Max(0, 1 - r * r)) });
            }
            for (int j = 0; j < da.Count; j++)
            {
                var d = da[j];
                int ten = j % 7 == 0 ? 8 : rng.Next(9);                           // 0..4 vệ tinh tròn, 5..7 mảnh vụn, 8 mặt trăng nhỏ
                d.vun = ten >= 5 && ten <= 7;
                d.sz = (d.vun ? U(22, 32) : U(26, 38)) * (d.z > 0.5f ? 1.15f : 1) * sc;
                d.ang = U(0, 360);
                d.seed = rng.Next(4);
                d.lua = U(0, 1) < 0.45f;
                d.bay = U(0.34f, 0.5f);
                float goc = (U(0, 1) < 0.8f ? U(-165, -35) : U(160, 195)) * Mathf.Deg2Rad;  // trên trời, hoặc phía bên kia đối thủ: không cắt qua tướng mình
                d.tu = C0 + TtLat(new Vector2(Mathf.Cos(goc), Mathf.Sin(goc)) * U(300, 380), dir);
                d.gio = Mathf.Lerp(TtSkHut, TtSkEp0 - 0.05f, j / (da.Count - 1f));
            }
            foreach (var d0 in da)
            {
                var d = d0;
                At(d.gio * k, () =>
                {
                    var p = new P { pos = d.tu, life = d.bay * k, group = Front };
                    p.draw = (q, kk, buf) =>
                    {
                        float f = Mathf.Min(1, q.age / q.life), tr = Tr();
                        var b = ChoBam(d, tr);
                        TtDuoi(d.tu, b, f, d.sz, d.lua, tr);
                        var pos = d.tu + (b - d.tu) * Mathf.Pow(f, 1.6f);
                        TtVeDa(buf, Front, 50, pos, 0.47f * 1.1f * d.sz, d.ang - dir * 200 * f, d.seed, 1, d.vun);
                    };
                    p.onDeath = (q, s) =>                                        // bám: bụi, dăm, rung khẽ; thành một hòn của vỏ tới lúc nổ
                    {
                        var b = ChoBam(d, Tr());
                        var bb = ToBui(b, new Vector2(U(-20, 20), -15) * sc, 0.42f, 6 * sc, 13 * sc, d.z >= 0 ? Front : Back, false);
                        bb.col = TtBui4;
                        if (U(0, 1) < 0.5f) ToSoi(b, new Vector2(U(-120, 120), U(-150, -40)) * sc, U(1.8f, 3f) * sc, TtDa2, foeFeet.y + U(-4, 8) * sc);
                        Shake?.Invoke(0.03f * m);
                        float con = tNoAbs - T;
                        if (con <= 0) return;
                        var v = new P { pos = b, life = con, group = d.z >= 0 ? Front : Back };
                        v.draw = (z, kk, buf) =>
                        {
                            float tr = Tr();
                            TtVeDa(buf, z.group, 44 + (int)(4 * (d.z + 1)), ChoBam(d, tr), 0.47f * d.sz * Mathf.Pow(TtVo(tr), 0.55f),
                                d.ang - dir * 10 * (tr - TtSkHut), d.seed, 1, d.vun);
                        };
                        Add(v);
                    };
                    Add(p);
                });
            }

            // 3. ép: bụi, dăm phì ra ở mép vỏ khi vỏ co lại
            At((TtSkEp0 + 0.05f) * k, () => Shake?.Invoke(0.2f * m));
            Every((TtSkEp0 + 0.05f) * k, (TtSkEp2 + 0.15f) * k, 18, x =>
            {
                float a = U(0, 6.28f);
                var u = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                var p = C0 + u * (RS0 * TtVo(Tr()) * 0.95f);
                var b = ToBui(p, u * U(40, 90) * sc, 0.5f, 7 * sc, 15 * sc, u.y < -0.2f ? Back : Front, false);
                b.col = TtBui4;
                if (U(0, 1) < 0.5f) ToSoi(p, (u * U(80, 160) + new Vector2(0, -60)) * sc, U(1.8f, 3f) * sc, TtDa2, foeFeet.y + U(-4, 8) * sc);
            });

            // 4. mặt trời trên đầu đối thủ (dưới mép sân): hiện bật ra, co lấy đà rồi phình khi bắn, tắt sau nổ
            float rSun0 = 25 * sc * mo;
            var sun = new Vector2(C0.x - dir * 6 * sc, Mathf.Max(C0.y - 0.71f * tH, 18 + 1.75f * rSun0));
            float RSun(float tr)
            {
                float u = (tr - TtSkGoi) / 0.28f;
                float a = EaseOut(u) * (1 + 0.12f * Mathf.Sin(Mathf.PI * Mathf.Clamp01(u)));
                a *= 1 - 0.10f * TtBao(tr, TtSkTia - 0.2f, TtSkTia, 0.15f, 0.02f) + 0.18f * TtBao(tr, TtSkTia, TtSkTia + 0.32f, 0.04f, 0.2f);
                a *= 1 - TtIn((tr - (TtSkNo + 0.35f)) / 0.35f);
                return rSun0 * Mathf.Max(0, a);
            }
            At(TtSkGoi * k, () =>
            {
                Shake?.Invoke(0.15f * m);
                var p = new P { pos = sun, life = (TtSkNo + 0.72f - TtSkGoi) * k, group = Back };
                p.draw = (q, kk, buf) => TtMatTroi(q.pos, RSun(Tr()), Tr(), dir);
                Add(p);
            });
            Every((TtSkGoi + 0.1f) * k, (TtSkNo + 0.4f) * k, 5, x => TtHoiNong(sun + new Vector2(U(-30, 30), 20) * sc, 30 * sc));

            // 5. tia nhiệt từ đáy mặt trời xuống quả cầu đá; lửa toé ở chỗ tia đập vào vỏ
            At(TtSkTia * k, () =>
            {
                Shake?.Invoke(0.35f * m);
                var p = new P { pos = sun, life = 0.5f * k, group = Front };
                p.draw = (q, kk, buf) =>
                {
                    float tr = Tr();
                    TtTia(sun, C0 + new Vector2(0, -RS0 * TtVo(tr) * 0.85f), sc * mo, tr, RSun(tr));   // chân tia đặt đúng mặt trên vỏ đá
                };
                Add(p);
            });
            // chỗ tia đập vào vỏ: BÔNG va chạm toé lên + vòng va chạm nhấp liên tục, lưỡi lửa nhỏ liếm ra hai bên (tia không cụt lủn giữa không trung)
            Every((TtSkTia + 0.02f) * k, TtSkNo * k, 40, x =>
            {
                float a = U(-Mathf.PI * 0.95f, -Mathf.PI * 0.05f);
                var q = Flame(C0 + new Vector2(U(-14, 14) * sc, -RS0 * TtVo(Tr()) * 0.85f), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(140, 240) * sc, U(0.2f, 0.32f),
                    5 * sc, 11 * sc, "tron", "lua", Front, 1.8f, -120, 1.2f, 0.25f, 0.05f);
                Tongue(q, 1, 0.3f);
            });
            for (int j = 0; j < 3; j++)
                At((TtSkTia + 0.01f + 0.035f * j) * k, () =>
                {
                    var cham = C0 + new Vector2(0, -RS0 * TtVo(Tr()) * 0.85f);
                    ToBong(cham, new Vector2(0, 1), (0.5f - 0.08f * j) * tH * mo, TtLua[2], Front, 0.14f);
                    ToVongVa(cham, 0.5f * tH * mo, 0.18f, 0.4f);
                });

            // 6. NỔ (người dùng 2026-11-18: "khi tia năng lượng bắn xuống phải nổ thật epic, sau đó nổ xong có khói đen tỏa ra thì hiện tướng đằng
            // sau khói đen mờ mờ cho mượt"): chớp + rung HAI nhịp, sao chớp lớn, CẦU LỬA nhiều lớp (hợp tròn: đỏ cam / cam / vàng / kem) phình
            // 0,16 s rồi bốc lên, nguội thành than; cột lửa vọt theo tia; hai vòng sóng đứng, sóng sát đất + vành bụi; vỏ đá, dăm, lửa, tia lửa văng;
            // năm vết nứt toả; ba tiếng nổ phụ; KHÓI ĐEN dày toả ra phủ chỗ đối thủ (lớp trước) rồi tan dần bay lên; mây nấm. Đối thủ ẩn trong cầu
            // lửa rồi hiện mờ dần sau khói (TinhHienDoiThu, StageViewThoTinh)
            At(L, () =>
            {
                FlashScreen?.Invoke(new Color(1, 0.965f, 0.84f, 0.5f * m));
                Shake?.Invoke(0.6f * m);                                        // rig khai impactShake 0,47 + sàn chiêu cuối của sân
                float tr = Tr();
                foreach (var d in da)
                {
                    var b = ChoBam(d, tr);
                    var u = Unit(b - C0 + new Vector2(0, -6 * sc));
                    var v = u * U(240, 520) * sc * mo + new Vector2(0, -U(140, 300)) * sc;
                    TtDaVang(b, v, 0.47f * 0.62f * d.sz, U(1.4f, 1.8f), foeFeet.y + U(-6, 60) * sc, d.z >= 0 ? Front : Back, d.ang, d.vun, d.seed);
                }
                // dăm theo CHÙM lệch cỡ (người dùng 2026-11-18: hạt lẻ to, đơn lẻ), lưỡi lửa nhỏ văng xa, tia lửa nửa trên
                int nDam = Mathf.RoundToInt(6 * m), nLua = Mathf.RoundToInt(12 * m), nTia = Mathf.RoundToInt(14 * m);
                for (int i = 0; i < nDam; i++)
                {
                    float a = -Mathf.PI * ((i + 0.5f) / nDam) + U(-0.2f, 0.2f);
                    ToSoiCum(C0 + U2(-14, 14) * sc, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(300, 520) * sc * mo, U(3.6f, 5.4f) * sc, TtDamC[rng.Next(TtDamC.Length)],
                        TtDa3, foeFeet.y + U(-6, 60) * sc, (i & 1) == 0 ? Front : Back);
                }
                for (int i = 0; i < nLua; i++)                                   // lưỡi lửa văng xa, đuôi khói
                {
                    float a = U(0, 6.28f);
                    var q = Flame(C0 + U2(-14, 14) * sc, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f) * U(140, 320) * sc * mo, U(0.28f, 0.42f), 7 * sc * mo,
                        16 * sc * mo, "tron", "lua", Front, 2.2f, -160, 1.3f, 0.4f, 0.1f);
                    Tongue(q, 1, 0.2f);
                }
                for (int i = 0; i < nTia; i++)                                   // tia lửa toả đều nửa trên
                {
                    float a = -Mathf.PI * ((i + U(0.1f, 0.9f)) / nTia);
                    Spark(C0, new Vector2(Mathf.Cos(a), Mathf.Sin(a)), U(380, 720) * sc * mo, U(0.35f, 0.6f), 10 * sc, 600, Front);
                }
                ToChop(C0, 0.75f * tH * mo, Front, 0.12f);                       // sao chớp kem lớn, giữ 2 khung rồi co
                TtCauLua(C0, 0.6f * tH * mo, sc);
                TtNam(C0, sc * (0.75f + 0.3f * m));
                // sóng: cung dẹt KHÔNG viền trên đất (sóng sát đất + vành bụi), vòng đứng mảnh không viền (vòng có viền mực thành vòng đen dày)
                ToVong(new Vector2(C0.x, foeFeet.y), 260 * sc * mo, 0.6f);
                At(0.1f, () => ToVong(new Vector2(C0.x, foeFeet.y), 190 * sc * mo, 0.7f));
                ToVongVa(C0, 150 * sc * mo, 0.3f, 0.95f);
                ToHo(foeFeet, 0.55f * tH * mo, 1.1f);
                for (int j = 0; j < 5; j++)                                      // nứt đất toả dưới chân đối thủ
                {
                    float a = (j - 2) * 0.55f + U(-0.15f, 0.15f) + (j % 2 == 0 ? 0 : Mathf.PI);
                    var dn = new Vector2(Mathf.Cos(a), 0.32f * Mathf.Sin(a));
                    ToNut(foeFeet + dn * 10 * sc, foeFeet + dn * U(70, 130) * sc * mo, 0.18f, sc);
                }
                for (int j = 0; j < 4; j++)                                      // bụi lan sát đất: bốn cụm nhiều múi, tách dần
                {
                    float d = (j & 1) == 1 ? -1 : 1;
                    ToCum(new Vector2(C0.x + d * U(20, 50) * sc, foeFeet.y - 6 * sc), new Vector2(d * U(140, 260), -18) * sc * mo, 26 * sc * mo, 3, j < 2 ? Front : Back,
                        U(0.9f, 1.2f));
                }
            });
            Every(L, L + 0.32f, 36, x =>                                         // cột lửa vọt lên theo tia: lưỡi lửa vuốt lên (không cầu tròn)
            {
                var q = Flame(C0 + new Vector2(U(-12, 12), -U(0, 24)) * sc, new Vector2(U(-40, 40), -U(380, 620)) * sc * mo, U(0.3f, 0.45f), 8 * sc,
                    17 * sc * mo, "tron", "lua", Front, 1.6f, -200, 1.4f, 0.25f, 0.08f);
                Tongue(q, 1, 0.6f);
            });
            At(L + 0.08f, () => ToVongVa(C0, 210 * sc * mo, 0.4f, 0.95f));                                       // sóng đứng thứ hai (mảnh)
            At(L + 0.12f, () => FlashScreen?.Invoke(new Color(1, 0.93f, 0.78f, 0.22f * m)));                         // chớp nhịp hai
            At(L + 0.22f, () => Shake?.Invoke(0.35f * m));                                                            // rung nhịp hai
            for (int j = 0; j < 3; j++)                                          // ba tiếng nổ phụ quanh cầu lửa
            {
                float tj = L + 0.12f + 0.11f * j;
                At(tj, () =>
                {
                    float a = U(0, 6.28f);
                    var p = C0 + new Vector2(Mathf.Cos(a), 0.7f * Mathf.Sin(a)) * U(0.35f, 0.6f) * tH * mo;
                    ToChop(p, 0.34f * tH * mo, Front, 0.12f);
                    for (int i = 0; i < 4; i++)
                        Tongue(Flame(p, U2(-120, 120) * sc + new Vector2(0, -80 * sc), U(0.25f, 0.36f), 6 * sc, 13 * sc * mo, "tron", "lua", Front, 2, -160, 1.3f, 0.4f, 0.05f),
                            1, 0.25f);
                    Shake?.Invoke(0.12f * m);
                });
            }
            // KHÓI ĐEN: cụm to bay toả ra (phần lớn lớp trước, phủ chỗ đối thủ), cụm thấp lan ngang sát đất; tan dần bay lên, không vụt tắt
            // khói than cụm nhiều múi (đỉnh nhạt, đáy đậm), một số cụm to tách đôi ba giữa đời; ít hạt hơn mà to, hoà thành một khối liền
            Every(L + 0.1f, L + 0.62f, 40 * m, x =>
            {
                float a = -Mathf.PI * U(-0.15f, 1.15f);
                var u = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                ToKhoi(C0 + u * U(0, 0.3f) * tH, u * U(50, 150) * sc * mo + new Vector2(0, -U(10, 50) * sc), U(1.7f, 2.3f), 20 * sc,
                    U(46, 66) * sc * mo, U(0, 1) < 0.75f ? Front : Back, U(0, 1) < 0.3f);
            });
            Every(L + 0.15f, L + 0.5f, 16 * m, x =>
            {
                float d = U(0, 1) < 0.5f ? -1 : 1;
                ToKhoi(new Vector2(C0.x + d * U(0, 40) * sc, foeFeet.y - U(10, 30) * sc), new Vector2(d * U(120, 220), -U(10, 40)) * sc * mo,
                    U(1.4f, 1.9f), 16 * sc, U(36, 50) * sc * mo, Front, false);
            });

            // 7. đáp đất
            At(TtSkDat * k, () =>
            {
                ToVong(casterFeet, 110 * sC, 0.55f);
                ToHo(casterFeet, 40 * sC, 0.8f);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(casterFeet + new Vector2(d * 36 * sC, -2), new Vector2(d * 120, -25) * sC, 18 * sC, 4);
                Shake?.Invoke(0.45f * m);
            });
            return L;
        }

        // mặt trời: đĩa phẳng bốn lớp (cam đỏ, cam, vàng, kem) viền mực + 12 lưỡi lửa tam giác dài ngắn xen kẽ, phập phồng, quay
        void TtMatTroi(Vector2 c, float r, float t, float dir)
        {
            if (r < 1) return;
            float rot = t * 1.4f;
            for (int j = 0; j < 12; j++)
            {
                float a = rot + 2 * Mathf.PI * j / 12, lg = r * (0.55f + 0.18f * (j % 2) + 0.08f * Mathf.Sin(t * 9 + j * 1.7f));
                const float w = 0.22f;
                int s0 = mp.Count;
                mp.Add(c + TtLat(new Vector2(Mathf.Cos(a - w), Mathf.Sin(a - w)) * (0.85f * r), dir));
                mp.Add(c + TtLat(new Vector2(Mathf.Cos(a + 0.1f), Mathf.Sin(a + 0.1f)) * (r + lg), dir));
                mp.Add(c + TtLat(new Vector2(Mathf.Cos(a + w), Mathf.Sin(a + w)) * (0.85f * r), dir));
                MSolid(Back, 20 + j * 0.001f, s0, 3, TtLua[(j & 1) == 1 ? 1 : 0], 1, 2.2f);
            }
            for (int lop = 0; lop < 4; lop++)
            {
                float rr = r * (lop == 0 ? 1 : lop == 1 ? 0.8f : lop == 2 ? 0.58f : 0.34f);
                int s0 = mp.Count;
                for (int i = 0; i < 27; i++)
                {
                    float a = 2 * Mathf.PI * i / 27;
                    mp.Add(c + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rr);
                }
                if (lop == 0) MSolid(Back, 22, s0, 27, TtLua[0], 1, 2.6f);
                else MFill(Back, 22 + lop * 0.01f, s0, 27, TtLua[lop], 1, false);
            }
        }

        // tia nhiệt: mảng liền từ đáy mặt trời xuống MẶT VỎ ĐÁ, bốn lớp mép gợn, LÕI KEM RỘNG (người dùng 2026-11-18: "tia beam bắn xuống nhìn màu
        // hơi tối"): ngoài cam, vàng, kem rộng; chân tia LOE thành bông chạm (rộng 1,7 lần ở 12 % cuối) ôm lên mặt vỏ, không cụt ngang; bật mở
        // 0,06 s, giữ, rồi RÚT từ trên xuống (đuôi tia đuổi xuống chân, 0,16 s) thay vì thu hẹp cả cột
        void TtTia(Vector2 sun, Vector2 dich, float sc, float t, float rSun)
        {
            float mo = EaseOut((t - TtSkTia) / 0.06f), rut = TtIo((t - (TtSkTia + 0.32f)) / 0.16f);
            float w = 50 * sc * mo * (1 - 0.35f * rut);
            if (t < TtSkTia || w < 1 || rut >= 0.98f) return;
            float y0 = sun.y + rSun * 0.6f, y1 = dich.y;
            if (y1 - y0 < 4) return;
            y0 += (y1 - y0) * 0.9f * rut;
            const int N = 14;
            for (int lop = 0; lop < 4; lop++)
            {
                float kw = lop == 0 ? 1 : lop == 1 ? 0.8f : lop == 2 ? 0.62f : 0.42f;
                int s0 = mp.Count;
                for (int pass = 0; pass < 2; pass++)
                    for (int i = 0; i < N; i++)
                    {
                        int ii = pass == 0 ? i : N - 1 - i;
                        float f = ii / (N - 1f), yy = y0 + (y1 - y0) * f;
                        float g = 1 + 0.09f * Mathf.Sin(yy * 0.13f + t * 40 + lop) + 0.05f * Mathf.Sin(yy * 0.31f - t * 27);
                        float loe = 1 + 0.2f * f + 0.7f * SmoothStep(0.86f, 1, f);  // chân tia loe ra ôm mặt vỏ
                        float hw = w * kw / 2 * g * loe, xc = sun.x + (dich.x - sun.x) * f;
                        mp.Add(new Vector2(pass == 0 ? xc - hw : xc + hw, yy));
                    }
                if (lop == 0) MSolid(Front, 70, s0, 2 * N, TtLua[1], 1, 2.6f);
                else MFill(Front, 70 + lop * 0.01f, s0, 2 * N, lop == 1 ? TtLua[2] : lop == 2 ? Color.Lerp(TtLua[2], TtLua[3], 0.5f) : TtLua[3], 1, false);
            }
        }
    }
}
