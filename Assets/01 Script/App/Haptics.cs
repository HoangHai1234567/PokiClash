// Rung chia bậc theo giá trị thật (máy bi): chạm đinh nhẹ nhất và bị chặn nhịp, bi rơi ô thường hai nhịp nhẹ, rương mạnh
// dần theo loại, rương vàng dồn nhịp rồi chốt một cú. Mỗi bậc có khoảng chặn riêng để bi va liên tục không rung tê tay.
// Android 8+ (API 26): VibrationEffect dạng sóng có biên độ. Android cũ và iOS chỉ có Handheld.Vibrate (một cú dài cố định)
// nên chỉ dùng cho bậc rương vàng. Bật tắt bằng nút "Rung" trong Sổ tay (settings.haptics, App.ApplySettings).
using UnityEngine;

namespace PokiClash
{
    public enum Haptic { Peg, Drop, LandSmall, LandWood, LandSilver, LandGold, OpenWood, OpenSilver, OpenGold, LevelUp }

    public static class Haptics
    {
        public static bool Enabled = true;

        // mỗi bậc: các nhịp (bắt đầu ms, dài ms, biên độ 1–255); giá trị khởi điểm, chỉnh được
        static readonly (int at, int ms, int amp)[][] Patterns =
        {
            new[] { (0, 8, 40) }, // Peg
            new[] { (0, 10, 70) }, // Drop
            new[] { (0, 10, 60), (23, 12, 110) }, // LandSmall: ô EXP, +1 bi
            new[] { (0, 12, 80), (35, 14, 140), (85, 18, 220) }, // LandWood
            new[] { (0, 14, 110), (40, 16, 180), (90, 22, 255) }, // LandSilver
            new[] { (0, 60, 40), (80, 60, 90), (160, 60, 150), (260, 40, 255) }, // LandGold
            new[] { (0, 18, 150) }, // OpenWood
            new[] { (0, 15, 90), (480, 25, 230) }, // OpenSilver
            new[] { (0, 100, 40), (110, 90, 75), (210, 120, 120), (350, 20, 170), (600, 35, 255) }, // OpenGold
            new[] { (150, 20, 110), (550, 40, 255) }, // LevelUp
        };
        // khoảng chặn tối thiểu giữa hai lần cùng bậc (giây)
        static readonly float[] Gap = { 0.1f, 0.05f, 0.06f, 0.08f, 0.08f, 0.2f, 0.2f, 0.2f, 0.2f, 0.3f };
        static readonly float[] last = new float[Gap.Length];

        public static void Play(Haptic h)
        {
            if (!Enabled) return;
            int i = (int)h;
            float now = Time.unscaledTime;
            if (now - last[i] < Gap[i] && last[i] > 0) return;
            last[i] = now;
#if UNITY_ANDROID && !UNITY_EDITOR
            Android(Patterns[i], h == Haptic.LandGold || h == Haptic.OpenGold);
#elif UNITY_IOS && !UNITY_EDITOR
            if (h == Haptic.LandGold || h == Haptic.OpenGold) Handheld.Vibrate();
#endif
        }

#if UNITY_ANDROID && !UNITY_EDITOR
        static AndroidJavaObject vibrator;
        static int sdk = -1;

        static void Android((int at, int ms, int amp)[] pat, bool strong)
        {
            try
            {
                if (sdk < 0)
                {
                    using (var ver = new AndroidJavaClass("android.os.Build$VERSION")) sdk = ver.GetStatic<int>("SDK_INT");
                    using (var up = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))
                    using (var act = up.GetStatic<AndroidJavaObject>("currentActivity"))
                        vibrator = act.Call<AndroidJavaObject>("getSystemService", "vibrator");
                }
                if (vibrator == null || !vibrator.Call<bool>("hasVibrator")) return;
                if (sdk < 26)
                {
                    // máy cũ không chỉnh được biên độ: chỉ rung ở bậc mạnh nhất
                    if (strong) Handheld.Vibrate();
                    return;
                }
                // sóng: (nghỉ, rung) lần lượt, biên độ 0 khi nghỉ
                var timings = new long[pat.Length * 2];
                var amps = new int[pat.Length * 2];
                int cursor = 0;
                for (int k = 0; k < pat.Length; k++)
                {
                    timings[k * 2] = Mathf.Max(0, pat[k].at - cursor);
                    amps[k * 2] = 0;
                    timings[k * 2 + 1] = pat[k].ms;
                    amps[k * 2 + 1] = Mathf.Clamp(pat[k].amp, 1, 255);
                    cursor = pat[k].at + pat[k].ms;
                }
                using (var ve = new AndroidJavaClass("android.os.VibrationEffect"))
                using (var effect = ve.CallStatic<AndroidJavaObject>("createWaveform", timings, amps, -1))
                    vibrator.Call("vibrate", effect);
            }
            catch (System.Exception)
            {
                // máy không hỗ trợ: bỏ qua rung
            }
        }
#endif
    }
}
