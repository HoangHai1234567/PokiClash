// Hải Long: LOẠT THỦY TIA (2026-11-25, người dùng xem hộp chi tiết tướng: "chiêu mana con này nhìn yếu quá, làm nó bắn thành nhiều laser
// beam đi"). Thay Loạt thủy cầu (NLoatCau, HatNuocChieu.cs — giữ nguyên hàm): mỗi đầu bắn một tia kiểu Water Laser (NLaser, HatNuocGoi.cs)
// đúng lúc đầu đó vươn ra trong clip cast (mốc miệng từng đầu, giờ vươn: HlDau* / HlGio* / HlMz* đo trên .atomik, dùng chung với
// NLoatCau). Dạng 1 một đầu bắn ba tia toả (giữa dày nhất), dạng 2 ba đầu, dạng 3 năm đầu. Các tia hội tụ vào thân đối thủ ở những điểm
// lệch nhau, so le giờ bắn và giờ tắt (không cùng bật cùng tắt); tia đầu chính dày, các đầu phụ mảnh hơn. Không có bộ nước shader thì về
// tia nước cũ. Trả giờ tia đầu tiên chạm.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // giữ dáng nhả sau giờ trúng (StageView: bảng giữ của mã "n_loat_tia"): đầu chót vươn trễ 0,25 s + tia sống ~0,7 s
        public const float LoatTiaGiu = 0.95f;

        public float NLoatTia(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1, H = Mathf.Max(1, casterH);
            float mzX = (mouth.x - casterFeet.x) * dir / H, mzY = (casterFeet.y - mouth.y) / H;
            int dang = mzX < 0.31f ? 3 : mzY > 0.6f ? 2 : 1;
            var dau = dang == 3 ? HlDau3 : dang == 2 ? HlDau2 : HlDau1;
            var gio = dang == 3 ? HlGio3 : dang == 2 ? HlGio2 : HlGio1;
            var mz = dang == 3 ? HlMz3 : dang == 2 ? HlMz2 : HlMz1;
            float k = Mathf.Max(0.3f, lead) / 1.0f;
            float dayChinh = Mathf.Clamp(0.15f * casterH, 18, 34), dayPhu = Mathf.Clamp(0.105f * casterH, 12, 24);
            // (miệng, giờ vươn, lệch điểm trúng theo thân đối thủ (phần tH), dày)
            var tia = new List<(Vector2 g, float t0, Vector2 lech, float day)>();
            if (dau.Length == 1)
            {
                var g = LechRig(mouth, casterFeet, casterH, foeFeet, dau[0], mz);
                tia.Add((g, gio[0] * k, new Vector2(0, -0.05f), dayChinh * 1.15f));
                tia.Add((g, gio[0] * k + 0.08f, new Vector2(0.06f, -0.3f), dayPhu));
                tia.Add((g, gio[0] * k + 0.15f, new Vector2(-0.04f, 0.18f), dayPhu));
            }
            else
            {
                float[] ly = { -0.05f, -0.3f, 0.16f, -0.18f, 0.06f };
                for (int i = 0; i < dau.Length; i++)
                    tia.Add((LechRig(mouth, casterFeet, casterH, foeFeet, dau[i], mz), gio[i] * k, new Vector2(U(-0.06f, 0.06f), ly[i % ly.Length]),
                        i == 0 ? dayChinh : dayPhu));
            }
            float tHit0 = float.MaxValue;
            for (int i = 0; i < tia.Count; i++)
            {
                var (g, t0, lech, day) = tia[i];
                bool chinh = i == 0;
                var hit = foeBody + new Vector2(-dir * 0.1f * tH + lech.x * tH, lech.y * tH);
                float dai = (hit - g).magnitude;
                float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f); // như NTiaKhung / TiaFb
                float tTu = Mathf.Max(0.05f, t0 - 0.06f);            // tia phóng theo cú vươn của đầu
                float tBan = (chinh ? 0.72f : 0.55f) + 0.04f * i;     // tắt so le
                tHit0 = Mathf.Min(tHit0, tTu + tVuon);
                var gg = g;
                var hh = hit;
                NLaser(() => gg, () => hh, day, tTu, tBan, Front, chinh ? 1f : 0.75f, chinh ? 1f : 0.7f, casterFeet.y, foeFeet.y);
                AtW(tTu, () => Shake?.Invoke(chinh ? 0.28f : 0.14f));
                AtW(tTu + tVuon, () => NuocPulse?.Invoke(chinh ? 0.6f : 0.35f));
            }
            return tHit0;
        }
    }
}
