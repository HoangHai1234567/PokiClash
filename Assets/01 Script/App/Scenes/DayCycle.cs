// Giờ trong game theo giờ máy (người dùng dặn 2026-11-18: các đảo và sảnh lấy thời gian sáng, tối): độ đêm, độ hoàng hôn, độ nắng,
// màu nhuộm cảnh. DayNight (lớp phủ trên ảnh đảo) đọc mỗi khung. Override: ép giờ để thử (menu PokiClash/Thử/Giờ trong game…).
//   đêm: 20h–4h30 đủ tối; chạng vạng 17h30→20h tối dần, 4h30→6h30 sáng dần
//   hoàng hôn, bình minh: ấm nhất quanh 18h20 và 6h
//   nắng (tia nắng): 7h→10h mạnh dần, 15h→17h30 yếu dần
using System;
using UnityEngine;

namespace PokiClash
{
    public static class DayCycle
    {
        public static float? Override;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)] // Play không reload domain
        static void ResetStatics() => Override = null;

        public static float Hour => Override ?? (float)DateTime.Now.TimeOfDay.TotalHours;

        static float Ramp(float x, float a, float b) => Mathf.SmoothStep(0, 1, Mathf.InverseLerp(a, b, x));

        public static float Night(float h) => h < 12 ? 1 - Ramp(h, 4.5f, 6.5f) : Ramp(h, 17.5f, 20f);

        public static float Dusk(float h)
        {
            float Bell(float c, float w) => Mathf.Exp(-(h - c) * (h - c) / (2 * w * w));
            return Mathf.Max(Bell(6f, 0.8f), Bell(18.3f, 0.9f));
        }

        public static float Sun(float h) => h < 12 ? Ramp(h, 7f, 10f) : 1 - Ramp(h, 15f, 17.5f);

        // đêm: đảo chỉ ngả xanh nhẹ cho còn nhìn rõ; biển tối thêm (SeaNight, càng xa bờ càng tối) nên đảo nổi sáng giữa biển đêm
        // (người dùng 2026-11-18: "tối xung quanh thôi, đảo phải phát sáng, tối quá không nhìn được gì")
        static readonly Color NightTint = new Color(0.66f, 0.72f, 0.93f), DuskTint = new Color(1f, 0.76f, 0.68f);
        public static readonly Color SeaNight = new Color(0.56f, 0.62f, 0.84f);

        // mây xỉn màu khi chiều tối (nhân thêm trên màu cảnh; đảo vẫn sáng): chiều ngả xám tím, đêm tối hơn đảo
        public static Color CloudTint(float h)
        {
            var c = Color.Lerp(Color.white, new Color(0.80f, 0.77f, 0.82f), Dusk(h));
            return Color.Lerp(c, new Color(0.58f, 0.62f, 0.78f), Night(h));
        }

        // màu nhân lên cảnh (trắng = giữ nguyên)
        public static Color Tint(float h)
        {
            var c = Color.Lerp(Color.white, DuskTint, Dusk(h) * 0.75f);
            return Color.Lerp(c, NightTint, Night(h));
        }
    }
}
