// KHUNG VẼ SẴN cho bộ Mộc (2026-11-19). Người dùng duyệt bộ 24 khung (HatFlip.cs): "ổn hơn rồi đấy, cho vào game đi", và chê "gai lá,
// gai sắt đâm lên xấu", "khói rải rác, chưa cụm, chưa mềm". File này gom ba cách dùng khung trong các chiêu Mộc:
//   MocGaiFb  : gai lá đâm lên (gai_la) có pha GIỮ kéo dài được, đỉnh phóng rơi đúng giờ hẹn (giờ trúng cũ không đổi);
//   MocLocFb  : lốc năng lượng (loc) lặp quanh con đang gồng, nở êm lúc hiện, mờ dần lúc tắt;
//   MocKhoiFb : cụm khói nhuộm ra bụi đất (khoi), MocBuiHaiBen: hai cụm hai bên cú dậm / nện (thay 3–6 cụm BuiCum cũ).
// Hàm nào cũng trả null / false khi chưa nhập ảnh, để hàm gọi rơi về hạt cũ. Chỉ chiêu Mộc gọi; đồ dùng chung với hệ khác (BuiCum, Bui, Spike,
// Shard, ThachNo, CungDat, VetDat, GatherLa…) giữ nguyên.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // khung khói nâu xám (#8C7C74) nhân màu ra bụi đất ấm: nhân màu chỉ làm tối đi, nên bụi đậm hơn cụm be cũ một chút
        static readonly Color MocBuiFbC = new Color(1f, 0.925f, 0.8f);

        // mốc khung của gai_la (đo hộp hình từng khung): 0–3 nứt đất, 4–8 phóng lên (khung 8 gần đủ cao), 9–16 giữ lắc nhẹ, 17–23 gãy rụng lá
        const float MocGaiFbDinh = 8, MocGaiFbGiu = 16;

        // GAI LÁ ĐÂM LÊN bằng khung vẽ sẵn. feet: đáy giữa cụm gai trên đất; h: khung cao (đơn vị sân, gai cao nhất ~0,95 h, rộng ~1 h);
        // dinh: sau bao nhiêu giây kể từ lúc gọi thì gai phóng lên gần đủ cao (đặt trùng giờ trúng cũ); giu: giây giữ ở đỉnh trước khi gãy
        // (ít nhất bằng nhịp khung tự nhiên); start: khung bắt đầu (0 có khung nứt đất; gọi muộn quá thì tự bỏ bớt khung đầu cho kịp đỉnh).
        // Cuối đời mờ dần 0,08 s (khung cuối còn ụ đất nhỏ, không tắt phụt). Trả false khi chưa nhập ảnh.
        bool MocGaiFb(Vector2 feet, float h, float dinh, float giu = 0, int group = Back, float layer = 35, bool flip = false, float speed = 1.35f,
            float start = 2.5f, Color? tint = null, float alpha = 1)
        {
            var art = FbArt("gai_la");
            if (art == null) return false;
            var d = Fbs["gai_la"];
            float fps = d.fps * Mathf.Max(0.1f, speed);
            float t0 = dinh - (MocGaiFbDinh - start) / fps; // giờ bắt đầu chạy khung (so với lúc gọi)
            float s = start;
            if (t0 < 0)
            {
                s = Mathf.Min(MocGaiFbDinh - 0.5f, start - t0 * fps);
                t0 = 0;
            }
            float tLen = (MocGaiFbDinh - s) / fps, tGiu = Mathf.Max((MocGaiFbGiu - MocGaiFbDinh) / fps, giu), tGay = (d.n - 1 - MocGaiFbGiu) / fps;
            var col = tint ?? Color.white;
            var p = new P { pos = feet, group = group, life = tLen + tGiu + tGay + 0.08f };
            p.draw = (q, k, buf) =>
            {
                float t = q.age, f;
                if (t < tLen) f = s + t * fps;
                else if (t < tLen + tGiu) f = MocGaiFbDinh + (MocGaiFbGiu - MocGaiFbDinh) * (t - tLen) / tGiu;
                else f = MocGaiFbGiu + (t - tLen - tGiu) * fps;
                DrawFb(buf, art, d, f, q.pos, h, q.group, layer, 0, flip, col, alpha * Mathf.Clamp01((q.life - t) / 0.08f));
            };
            if (t0 <= 0.001f) Add(p);
            else At(t0, () => Add(p));
            return true;
        }

        // VÒNG GAI LÁ quanh chân đối thủ. Người dùng xem trong game 2026-11-19: "có vài vụ nổ layer nằm dưới địch nên không thấy rõ" (gai phần
        // lớn ở SAU lưng nên bị thân che). Nay lớp TRƯỚC có hai cụm to hai bên (lệch ±0,62–0,64 tH, cao 0,78–0,84 tH × truoc, đứng chếch trước
        // chân) và, nếu biết phía con ra chiêu (phia ±1; 0 thì bỏ), một cụm vừa chếch trước chân phía đó (±0,4 tH, 0,6 tH, đứng thấp hơn nữa
        // trên màn nên vẽ đè lên hai cụm kia). Không cụm nào cao đứng ngay trước mặt. Lớp SAU: các cụm cao làm nền, đủ cao để ló lên trên vai.
        // sau: (lệch ngang, cao, trễ đỉnh) theo tH; dinh: giờ đỉnh phóng (so với lúc gọi); giu: giây giữ của cụm đầu (cụm trễ giữ bớt đi).
        void MocVongGai(Vector2 foeFeet, float tH, float dinh, float giu, float phia, (float x, float h, float tre)[] sau, float truoc = 1,
            float start = 4.5f)
        {
            for (int i = 0; i < sau.Length; i++)
            {
                var (ox, hh, tre) = sau[i];
                MocGaiFb(foeFeet + new Vector2(ox * tH, -3 - 2 * (i & 1)), hh * tH, dinh + tre, giu - tre, Front, 35 + 0.01f * i, (i & 1) == 0, 1.35f, start);
            }
            MocGaiFb(foeFeet + new Vector2(-0.64f * tH, 8), 0.84f * truoc * tH, dinh + 0.03f, giu - 0.03f, Front, 35.2f, false, 1.35f, start);
            MocGaiFb(foeFeet + new Vector2(0.62f * tH, 9), 0.78f * truoc * tH, dinh + 0.06f, giu - 0.06f, Front, 35.21f, true, 1.35f, start);
            if (phia != 0)
                MocGaiFb(foeFeet + new Vector2(phia * 0.4f * tH, 14), 0.6f * truoc * tH, dinh + 0.09f, giu - 0.09f, Front, 35.22f, phia > 0, 1.35f, start);
        }

        // LỐC NĂNG LƯỢNG lặp (loc) quanh con đang gồng: neo ở chân, nở từ 40 % trong 0,18 s và hiện dần (không bật phụt), lặp tới hết life
        // rồi mờ dần 0,2 s. Đặt ở Back, lớp thấp: con ra chiêu và lá cuốn vẽ đè lên.
        P MocLocFb(Vector2 feet, float h, float life, int group = Back, float layer = 16, float alpha = 0.9f, bool flip = false)
        {
            var art = FbArt("loc");
            if (art == null) return null;
            var d = Fbs["loc"];
            float ph = U(0, d.n);
            var p = new P { pos = feet, group = group, life = Mathf.Max(0.12f, life) };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float g = 0.4f + 0.6f * EaseOut(Mathf.Min(1, t / 0.18f));
                float a = alpha * Mathf.Min(1, t / 0.1f) * Mathf.Clamp01((q.life - t) / 0.2f);
                DrawFb(buf, art, d, ph + t * d.fps, q.pos, h * g, q.group, layer, 0, flip, Color.white, a);
            };
            return Add(p);
        }

        // LỐC KHÍ (2026-11-25, người dùng chọn lốc "Khí" của gói Game VFX - Tornado Collection cho chiêu cuối rồng trúc). Khung chụp tách nền
        // từ prefab FX_AirTornado_Loop (Editor/VfxPackShots.cs → ArtGen/XemVfx/vfx_loc/xuat_loc_khi.py), ba bộ cùng khung cắt, cùng neo chân:
        // loc_khi_moc (mọc 0,5 s) → loc_khi_lap (thân, lặp liền) → loc_khi_tan (tắt phát hạt, tan tự nhiên); đổi đoạn hoà mờ 0,14 s.
        // path(t): chân lốc theo giây kể từ lúc gọi; tTan: giây bắt đầu tan; trum(t) 0..1: lốc đang trùm đối thủ → lớp SAU đặc + lớp TRƯỚC mờ
        // một nửa (đối thủ thấy trong lốc); không trùm: một lớp TRƯỚC. Trả null khi chưa nhập đủ ba bộ khung.
        public const float LocKhiMoc = 0.5f;
        // khung lốc trắng xám (cộng sáng của gói đã tách nền): nhân màu lục ngọc cho hợp hệ Mộc và NỔI trên nền sân cát sáng (bản đầu nhân lục
        // rất nhạt 0,84 / 0,98 / 0,88: chụp trong trận lốc gần như tan vào nền)
        static readonly Color MocKhiTint = new Color(0.62f, 0.9f, 0.72f);
        // dáng khung lốc khí (đo ở xuat_loc_khi.py): phần đặc cao ~0,72 khung trên neo; lá quay quanh thân: cao 0,66, bán kính 0,11 → 0,29 khung
        public const float LocKhiDinh = 0.72f;
        bool HasLocKhi => HasFb("loc_khi_moc") && HasFb("loc_khi_lap") && HasFb("loc_khi_tan");

        // khung cao lớn nhất để phần đặc của lốc đứng ở chân feetY không vượt mép trên sân (y 24)
        static float LocKhiCaoMax(float feetY) => Mathf.Max(40, (feetY - 24) / LocKhiDinh);

        P MocLocKhi(System.Func<float, Vector2> path, float h, float tTan, System.Func<float, float> trum, Color? tint = null, float alpha = 1,
            float layer = 30) => MocLocKhi(path, _ => h, 1, tTan, trum, t => trum(t) > 0.001f ? Back : Front, tint, alpha, layer);

        // hFn(t): khung cao theo giây (lốc gần rồng to, bay xa nhỏ dần theo chiều sâu); sx: giãn ngang (lốc béo hơn mà không cao thêm);
        // lop(t): lớp chính, vẽ đặc (null = TRƯỚC); trum(t) > 0 thêm lớp còn lại mờ 0,5 × trum (lốc ở lớp SAU trùm đối thủ: đối thủ vẫn thấy trong
        // lốc). Lốc chạy vòng quanh đối thủ: nửa trước vòng ở lớp TRƯỚC, nửa sau ở lớp SAU
        P MocLocKhi(System.Func<float, Vector2> path, System.Func<float, float> hFn, float sx, float tTan, System.Func<float, float> trum,
            System.Func<float, int> lop, Color? tint = null, float alpha = 1, float layer = 30)
        {
            var aM = FbArt("loc_khi_moc");
            var aL = FbArt("loc_khi_lap");
            var aT = FbArt("loc_khi_tan");
            if (aM == null || aL == null || aT == null) return null;
            var dM = Fbs["loc_khi_moc"];
            var dL = Fbs["loc_khi_lap"];
            var dT = Fbs["loc_khi_tan"];
            float tMoc = dM.n / dM.fps;
            tTan = Mathf.Max(tTan, tMoc);
            const float X = 0.14f;
            var col = tint ?? Color.white;
            var p = new P { pos = path(0), group = Front, life = tTan + dT.n / dT.fps };
            p.upd = (q, dt, s) => q.pos = path(q.age);
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float tr = Mathf.Clamp01(trum(t));
                float aEnd = alpha * Mathf.Clamp01((q.life - t) / 0.12f);
                float h = hFn(t);
                int g = lop != null ? lop(t) : Front;
                void Ve(Sprite[] art, FbDef d, float f, float a)
                {
                    a *= aEnd;
                    if (a < 0.02f) return;
                    DrawFb(buf, art, d, f, q.pos, h, g, layer, 0, false, col, a, sx);
                    if (tr > 0.001f) DrawFb(buf, art, d, f, q.pos, h, g == Front ? Back : Front, layer, 0, false, col, a * 0.5f * tr, sx); // trùm: thêm lớp kia mờ một nửa
                }
                float fl = (t - (tMoc - X)) * dL.fps; // khung của đoạn lặp (bắt đầu chạy từ lúc hoà với đoạn mọc)
                if (t < tMoc)
                {
                    float w = Mathf.Clamp01((t - (tMoc - X)) / X);
                    Ve(aM, dM, t * dM.fps, 1 - w);
                    if (w > 0) Ve(aL, dL, fl, w);
                }
                else if (t < tTan) Ve(aL, dL, fl, 1);
                else
                {
                    float w = Mathf.Clamp01((t - tTan) / X);
                    if (w < 1) Ve(aL, dL, fl, 1 - w);
                    Ve(aT, dT, (t - tTan) * dT.fps, w);
                }
            };
            return Add(p);
        }

        // LÁ QUAY QUANH LỐC: n lá bám thân lốc (chân theo path, giây kể từ lúc gọi chiêu), mỗi lá một độ cao (rải đều 12–86 % thân lốc cao hThan),
        // bán kính nở theo cao như phễu (rDay ở chân → rDinh ở đỉnh), góc chạy nhanh lệch tốc; lúc sinh cuốn từ ngoài vào trong 0,3 s. Nửa trước
        // quỹ đạo (thấp hơn trên màn) ở lớp TRƯỚC, nửa sau ở lớp SAU. tNo: lá NỔ TUNG văng ra theo hướng bán kính (chếch lên), rơi, tắt dần.
        void LaQuanhLoc(System.Func<float, Vector2> path, float hThan, float rDay, float rDinh, int n, float t0, float tNo, float sc = 1) =>
            LaQuanhLoc(path, _ => hThan / 0.66f, 1, n, t0, tNo, sc, rDay / hThan * 0.66f, rDinh / hThan * 0.66f);

        // hFn(t): khung cao của lốc theo giây chiêu (cùng gốc giờ với path), sx: giãn ngang của lốc; lá bám thân theo dáng khung lốc khí
        void LaQuanhLoc(System.Func<float, Vector2> path, System.Func<float, float> hFn, float sx, int n, float t0, float tNo, float sc = 1,
            float kDay = 0.11f, float kDinh = 0.29f, float laTo = 1)
        {
            var la = new System.Collections.Generic.List<P>(n);
            for (int i = 0; i < n; i++)
            {
                int j = i;
                float tSinh = t0 + 0.025f * i;
                if (tSinh >= tNo - 0.05f) break;
                At(tSinh, () =>
                {
                    float hf = 0.12f + 0.74f * (j + U(0.1f, 0.9f)) / n;
                    var q = Leaf(path(tSinh), Vector2.zero, tNo - tSinh + 2f, U(5.5f, 8.5f) * laTo, 0, 0, Front);
                    q.hgt = hf;
                    q.r0 = kDay + (kDinh - kDay) * (hf * hf * 0.6f + hf * 0.4f); // bán kính theo phần khung cao, nở nhanh dần lên đỉnh
                    q.R0 = U(0, 6.28f);                               // góc đầu
                    q.R1 = U(6.5f, 9.5f) * ((j % 5 == 4) ? 0.8f : 1); // tốc góc (rad/giây)
                    q.wd = tSinh;
                    q.upd = (z, dt, s) =>
                    {
                        float tt = z.wd + z.age;
                        float hh = hFn(tt);
                        float a = z.R0 + z.R1 * z.age;
                        float cuon = 1 + 0.7f * (1 - Mathf.Clamp01(z.age / 0.3f)); // cuốn từ ngoài vào
                        float c = Mathf.Cos(a), sn = Mathf.Sin(a), r = z.r0 * hh;
                        z.pos = path(tt) + new Vector2(c * r * sx * cuon, -z.hgt * 0.66f * hh + sn * r * 0.3f * cuon + Mathf.Sin(z.ph + z.age * 6) * 3);
                        z.group = sn > 0 ? Front : Back;
                        z.vel = Vector2.zero;
                        z.r1 = r * sx;                                 // bán kính đang thấy (dùng lúc nổ)
                    };
                    la.Add(q);
                });
            }
            At(tNo, () =>
            {
                foreach (var z in la)
                {
                    if (z.dead) continue;
                    float a = z.R0 + z.R1 * z.age;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.45f - 0.4f).normalized;
                    z.upd = null;
                    z.vel = d * U(380, 720) * sc + new Vector2(-Mathf.Sin(a), Mathf.Cos(a) * 0.3f) * z.R1 * z.r1 * 0.6f; // bung ra + quán tính quay
                    z.acc = new Vector2(0, 620);
                    z.drag = 2.2f;
                    z.life = z.age + U(0.55f, 0.9f);
                }
            });
        }

        // CỤM BỤI bằng khung khói: đáy cụm chạm đất ở feet, r ~ bán kính cụm BuiCum cũ (khung cao 2,4 r: ở khung to nhất cụm rộng ~2,3 r);
        // start: bỏ các khung cụm còn bé (cú dậm: cụm to ngay); vel: trôi theo hướng bị hất, hãm dần. Khung tự phồng, bay lên, tan thành mảnh.
        P MocKhoiFb(Vector2 feet, float r, Vector2 vel = default, int group = Back, float start = 4, float speed = 1.35f, float alpha = 0.92f,
            Color? tint = null)
        {
            var p = Fb("khoi", feet, 2.4f * r, group, 30, speed, 0, U(0, 1) < 0.5f, tint ?? MocBuiFbC, alpha, -1, start);
            if (p == null) return null;
            p.vel = vel;
            p.drag = 2.6f;
            return p;
        }

        // hai cụm bụi hai bên điểm feet, trôi ra ngoài (thay 3–6 cụm BuiCum của cú dậm / nện); giua: thêm một cụm nhỏ ở giữa, sau lưng.
        // false khi chưa nhập khung (hàm gọi chạy hạt cũ)
        bool MocBuiHaiBen(Vector2 feet, float r, float lech, float v, bool giua = false, int group = Back)
        {
            if (!HasFb("khoi")) return false;
            for (int i = 0; i < 2; i++)
            {
                float sd = i == 0 ? -1 : 1;
                MocKhoiFb(feet + new Vector2(sd * U(0.7f, 1.1f) * lech, U(-3, 2)), r * U(0.95f, 1.15f), new Vector2(sd * v * U(0.8f, 1.2f), -U(10, 30)), group,
                    U(3.5f, 5f));
            }
            if (giua) MocKhoiFb(feet + new Vector2(U(-0.2f, 0.2f) * lech, -U(3, 6)), r * 0.85f, new Vector2(U(-20, 20), -U(20, 40)), group, U(4, 5.5f));
            return true;
        }
    }
}
