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
