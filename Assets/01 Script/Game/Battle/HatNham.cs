// Bộ NHAM THẦN (2026-11-13, golem lõi lửa, suất nham_than đảo Hỏa; rig ArtGen/Spine/golem_lua_rig.py).
// Người dùng: đánh thường "lao đến dùng tay vả từ trên xuống vào đầu đối thủ"; chiêu cuối "nhảy lên co người thành hình tròn, gai lửa dài
// hơn, xoay thật nhanh rồi lao vào đối thủ; bay vào nảy ra dùng code"; "làm vfx riêng đi" (phần hình là đề xuất của Claude).
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc: phát từ đầu clip, biết `lead` = giờ tới lúc chạm) vì hiệu ứng phải chạy TRƯỚC lúc chạm
// (vệt lửa theo quả cầu đang lăn tới). Màu theo Themes["nham_than"] (bảng "lua", mảnh văng đá tro). Chiêu mana vẫn là "phun" (HatLua.Breath).
// - n_cau_lan (chiêu cuối): bụi đá lúc bật nhảy và lúc quả cầu rơi lại đất; VỆT LỬA tuột lại sau quả cầu suốt quãng lăn tới (quỹ đạo chép
//   AolaSticker.Jump nhánh Rams); chạm: chớp nổ lớn + lưỡi lửa toé theo hướng tông + đá tro vỡ văng + vòng lửa dưới chân; quả cầu bật về kéo
//   theo than hồng, khói mỏng; bung người đáp đất: vòng bụi + bụi đá hai bên + bụi trượt.
// - n_nham_va (đòn thường, tướng lao tới): bụi lúc bật khỏi chỗ; bàn tay nện xuống đầu đối thủ: chớp toé nhỏ, tia lửa và dăm đá văng hai
//   bên, bụi dưới chân đối thủ bị ép ra. Nhỏ hơn chiêu mana.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color TroC = C(204, 196, 186), TroC2 = C(174, 165, 154);   // bụi đá tro
        static readonly Color DaTroC = C(178, 167, 154), DaTroC2 = C(146, 134, 120); // dăm đá tro (màu thân golem)

        // quả cầu rời chỗ ở khung trúng của clip skill (hết clip − 1/30 s), chạm đối thủ ở 0,50 s của clip skill_land (golem_lua_rig.py L_HIT)
        public const float CauLanBay = 0.5f + 1f / 30;

        P BuiTro(Vector2 pos, Vector2 vel, float life = 0, float r0 = 4, float r1 = 11, int group = Front)
        {
            var p = Bui(pos, vel, life, r0, r1, group);
            p.col = (p.seed & 4) != 0 ? TroC2 : TroC;
            return p;
        }

        // dăm đá tro: xoay, rơi có trọng lực (máy chưa có ảnh dăm thì dùng mảnh văng của chủ đề)
        void DaTro(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            if (!HasGai)
            {
                Extra(pos, 1, vel.magnitude, group);
                return;
            }
            var q = Shard(pos, vel, life, r, 860, 1.4f, group);
            q.col = (q.seed & 4) != 0 ? DaTroC2 : DaTroC;
        }

        // vòng bụi + bụi đá toé hai bên ở chân (bật nhảy, rơi xuống, đáp đất); sc: cỡ
        void BuiDap(Vector2 feet, float H, float sc, int n)
        {
            Ripple(feet + new Vector2(0, 2), 0.08f * H * sc, 0.62f * H * sc, 0.42f, TroC2);
            for (int i = 0; i < n; i++)
            {
                float sd = (i & 1) == 0 ? -1 : 1;
                BuiTro(feet + new Vector2(sd * U(0.05f, 0.3f) * H * sc, U(-5, 2)), new Vector2(sd * U(130, 300) * sc, -U(10, 80)), U(0.4f, 0.7f), 4,
                    U(9, 15) * Mathf.Sqrt(sc), (i & 2) == 0 ? Back : Front);
            }
        }

        // CẦU LỬA LĂN (chiêu cuối). lead: giây từ đầu clip skill tới lúc quả cầu chạm đối thủ.
        public float NCauLan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(CauLanBay + 0.05f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float tBay = L - CauLanBay, R = 0.42f * casterH;
            // chỗ chạm so với chân (StageView: 86 % quãng tới đối thủ, nhấc 6 % chiều cao đối thủ); y của sân đi XUỐNG
            var den = new Vector2((foeFeet.x - casterFeet.x) * 0.86f, (foeFeet.y - casterFeet.y) * 0.86f - 0.06f * tH);
            // tâm quả cầu lúc lăn tới (u 0..1) và lúc bật về (v 0..1): chép AolaSticker.Jump nhánh Rams
            Vector2 Toi(float u) => casterFeet + den * (u * u * (0.4f + 0.6f * u)) + new Vector2(0, -0.4f * casterH * u * (1 - u) - R);
            Vector2 Ve(float v) => casterFeet + den * (1 - v * v * (3 - 2 * v)) + new Vector2(0, -3.4f * casterH * v * (1 - v) - R);
            float goc = T;

            // lấy đà: bật nhảy (clip skill 0,30 s) rồi quả cầu rơi lại đất (0,95 s): bụi đá
            if (L - 1.2f > 0.02f) At(L - 1.2f, () => BuiDap(casterFeet, casterH, 0.7f, 6));
            if (L - 0.58f > 0.02f)
                At(L - 0.58f, () =>
                {
                    Shake?.Invoke(0.22f);
                    BuiDap(casterFeet, casterH, 1f, 8);
                    for (int i = 0; i < 4; i++)
                        DaTro(casterFeet + new Vector2(U(-0.3f, 0.3f) * casterH, -4), new Vector2(U(-160, 160), -U(180, 320)), U(0.4f, 0.6f), U(3, 4.6f));
                });

            // lăn tới: lưỡi lửa tuột lại phía sau (ngọn chĩa ngược hướng lăn), dày dần theo tốc độ; than hồng và khói mỏng trên đường lăn
            Every(tBay, L, x => 34 + 60 * x, x =>
            {
                float u = Mathf.Clamp01((T - goc - tBay) / CauLanBay);
                var c = Toi(u);
                var hg = Unit(Toi(Mathf.Min(1, u + 0.06f)) - c);
                var ng = new Vector2(-hg.y, hg.x);
                // sinh ngay trong nửa sau quả cầu: vệt dính liền cầu, không hở quãng
                var q = Flame(c - hg * R * U(-0.35f, 0.55f) + ng * R * U(-0.85f, 0.85f), -hg * U(40, 150) + new Vector2(0, -U(20, 80)), U(0.26f, 0.4f),
                    U(8, 11), U(19, 28), "tron", Th.pal, U(0, 1) < 0.65f ? Back : Front, 1.8f, -220, 1.3f, 0.22f, 0.2f);
                Tongue(q, 1, 0.25f);
                q.smokeGroup = Back;
                if (U(0, 1) < 0.3f) Spark(c + new Vector2(0, R * 0.8f), -hg + new Vector2(0, -U(0.2f, 0.8f)), U(220, 380));
            });
            Every(tBay + 0.05f, L, 12, x =>
            {
                float u = Mathf.Clamp01((T - goc - tBay) / CauLanBay);
                Smoke(Toi(u) - new Vector2(dir * R * 0.6f, -R * 0.5f), new Vector2(-dir * U(20, 60), -U(30, 60)), U(0.6f, 0.9f), 6, 17, Back, "fire");
            });

            // chạm: chớp nổ lớn ở mặt trước thân đối thủ, lưỡi lửa toé theo hướng tông, đá tro vỡ văng, vòng lửa dưới chân
            var cham = foeBody + new Vector2(-dir * 0.1f * tH, 0);
            At(L, () =>
            {
                Shake?.Invoke(0.6f);
                Explode(cham, 1.2f, tH);
                Ring(foeFeet + new Vector2(0, 2), 0.45f, 0.18f * tH, 1.05f * tH, Th.ring);
                for (int i = 0; i < 9; i++)
                {
                    float a = (i - 4) * 0.3f + U(-0.1f, 0.1f); // quạt quanh hướng tông, hơi hất lên
                    var d = new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a) - 0.25f);
                    var q = Flame(cham + d * U(6, 14), d * U(300, 520), U(0.3f, 0.46f), 10, U(20, 28), "tron", Th.pal, i % 3 == 0 ? Front : Back, 4.2f,
                        -160, 1.5f, 0.3f);
                    Tongue(q, 1, 0.12f);
                    q.smokeGroup = Back;
                }
                for (int i = 0; i < 8; i++)
                {
                    float a = 6.28f * (i + U(0, 0.8f)) / 8; // rải đều góc
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f);
                    DaTro(cham + d * U(6, 14), d * U(220, 440), U(0.5f, 0.8f), U(3.4f, 5.6f));
                }
                for (int i = 0; i < 8; i++)
                {
                    float a = U(0, 6.28f);
                    Spark(cham, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f), U(280, 480));
                }
            });
            At(L + 0.13f, () =>
            {
                Shake?.Invoke(0.3f);
                Explode(cham + new Vector2(dir * U(4, 20), U(-26, 6)), 0.62f, tH);
            });
            At(L + 0.34f, () =>
            {
                for (int i = 0; i < 5; i++) Smoke(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.1f, 0.5f) * tH), null, 0, 9, 23, Back, "fire");
                for (int i = 0; i < 7; i++) Ash(foeBody + U2(-28, 28));
            });

            // bật về (đứng 0,16 s rồi bay vòng cung 0,42 s): than hồng, vài lưỡi lửa nhỏ và khói mỏng tuột lại
            float tVe = L + 0.16f;
            Every(tVe + 0.02f, tVe + 0.4f, 26, x =>
            {
                float v = Mathf.Clamp01((T - goc - tVe) / 0.42f);
                var c = Ve(v) + U2(-0.5f, 0.5f) * R;
                if (U(0, 1) < 0.45f)
                {
                    var q = Flame(c, new Vector2(dir * U(30, 90), -U(10, 60)), U(0.22f, 0.32f), 6, U(12, 17), "tron", Th.pal, Back, 2, -200, 1.2f, 0.2f, 0.3f);
                    Tongue(q, 1, 0.3f);
                }
                else if (U(0, 1) < 0.6f) Ember(c, null, 0, 9, Back);
                else Smoke(c, null, U(0.5f, 0.8f), 5, 14, Back, "fire", 0.2f);
            });

            // bung người, đáp đất (clip skill_land ~1,57 s), trượt lùi nốt về chỗ: vòng bụi, bụi đá hai bên, dăm đá, bụi trượt phía trước
            float tDap = L - 0.5f + 1.57f;
            var dap = casterFeet + new Vector2(dir * 0.28f * casterH, 0);
            At(tDap, () =>
            {
                Shake?.Invoke(0.26f);
                BuiDap(dap, casterH, 1.1f, 9);
                for (int i = 0; i < 4; i++)
                    DaTro(dap + new Vector2(U(-0.35f, 0.35f) * casterH, -4), new Vector2(U(-180, 180), -U(160, 300)), U(0.4f, 0.6f), U(3, 4.6f));
            });
            Every(tDap + 0.03f, tDap + 0.3f, 22, x =>
                BuiTro(casterFeet + new Vector2(dir * U(0.05f, 0.45f) * (1 - 0.6f * x) * casterH, U(-5, 2)), new Vector2(dir * U(60, 180), -U(10, 50)),
                    U(0.35f, 0.55f), 3.5f, U(7, 11), Back));
            return L;
        }

        // VẢ TỪ TRÊN XUỐNG (đòn đánh thường, tướng lao tới; lead = khung trúng của clip attack)
        public float NNhamVa(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.02f, L - 0.3f);
            // bật khỏi chỗ: bụi đá bắn ra sau
            At(t0, () =>
            {
                Ripple(casterFeet + new Vector2(0, 2), 0.06f * casterH, 0.4f * casterH, 0.35f, TroC2);
                for (int i = 0; i < 5; i++)
                    BuiTro(casterFeet + new Vector2(U(-12, 12), U(-5, 2)), new Vector2(-dir * U(110, 260), -U(20, 80)), U(0.35f, 0.6f), 3.5f, U(8, 12), Back);
            });
            // bàn tay nện xuống đầu đối thủ
            var dau = foeBody + new Vector2(-dir * 0.06f * tH, -0.3f * tH);
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                Explode(dau, 0.4f, tH); // chớp sao gai màu lửa (BurstFlash là chớp nước, lấy bảng màu nước)
                for (int i = 0; i < 6; i++)
                {
                    float sd = (i & 1) == 0 ? -1 : 1; // văng sang hai bên, hơi chúi xuống theo cú nện
                    Spark(dau + new Vector2(sd * U(4, 12), 0), new Vector2(sd * U(0.6f, 1f), U(-0.35f, 0.45f)), U(260, 420));
                }
                for (int i = 0; i < 5; i++)
                {
                    float sd = (i & 1) == 0 ? -1 : 1;
                    DaTro(dau + new Vector2(sd * U(4, 14), U(-4, 6)), new Vector2(sd * U(140, 300), -U(80, 240)), U(0.45f, 0.7f), U(3, 4.8f));
                }
                for (int i = 0; i < 3; i++) // lửa cổ tay toé theo
                {
                    var q = Flame(dau + U2(-8, 8), new Vector2(-dir * U(40, 160), -U(120, 240)), U(0.24f, 0.34f), 6, U(12, 17), "tron", Th.pal, Front, 3,
                        -180, 1.3f, 0.2f, 0.2f);
                    Tongue(q, 1, 0.2f);
                }
                // bụi dưới chân đối thủ bị ép ra hai bên
                Ripple(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.5f * tH, 0.4f, TroC2);
                for (int i = 0; i < 6; i++)
                {
                    float sd = (i & 1) == 0 ? -1 : 1;
                    BuiTro(foeFeet + new Vector2(sd * U(0.1f, 0.3f) * tH, U(-5, 2)), new Vector2(sd * U(120, 260), -U(10, 60)), U(0.4f, 0.65f), 4, U(9, 13),
                        Back);
                }
            });
            return L;
        }
    }
}
