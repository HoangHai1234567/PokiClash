// Tiếng tổng hợp kiểu đồ chơi ("bụp", "keng", "soạt"), chép công thức của Web/src/view/sfx.ts (WebAudio)
// thành mẫu PCM để Unity làm AudioClip. Không có file âm thanh nào.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public enum Wave { Sine, Triangle, Square, Sawtooth }

    public static class SfxSynth
    {
        public const int Rate = 44100;

        abstract class Part
        {
            public double Delay;
            public abstract double End { get; }
            public abstract void Mix(float[] buf, Random rnd);
        }

        sealed class Tone : Part
        {
            public double Freq, Dur, Vol, Slide;
            public Wave Type;
            public override double End => Delay + Dur + 0.02;

            public override void Mix(float[] buf, Random rnd)
            {
                int start = (int)(Delay * Rate);
                int len = (int)((Dur + 0.02) * Rate);
                double f1 = Math.Max(30, Freq + Slide);
                double phase = 0;
                for (int i = 0; i < len && start + i < buf.Length; i++)
                {
                    double t = (double)i / Rate;
                    // tần số trượt theo hàm mũ trong dur giây
                    double f = Slide != 0 && t < Dur ? Freq * Math.Pow(f1 / Freq, t / Dur) : Slide != 0 ? f1 : Freq;
                    phase += f / Rate;
                    phase -= Math.Floor(phase);
                    double s;
                    switch (Type)
                    {
                        case Wave.Triangle: s = 1 - 4 * Math.Abs(phase - 0.5); break;
                        case Wave.Square: s = phase < 0.5 ? 1 : -1; break;
                        case Wave.Sawtooth: s = 2 * phase - 1; break;
                        default: s = Math.Sin(phase * 2 * Math.PI); break;
                    }
                    // bao: 0,0001 -> vol trong 10 ms rồi -> 0,0001 lúc hết dur (mũ)
                    double g;
                    if (t < 0.01) g = 0.0001 * Math.Pow(Vol / 0.0001, t / 0.01);
                    else if (t < Dur) g = Vol * Math.Pow(0.0001 / Vol, (t - 0.01) / Math.Max(0.001, Dur - 0.01));
                    else g = 0;
                    buf[start + i] += (float)(s * g);
                }
            }
        }

        sealed class Noise : Part
        {
            public double Dur, Vol, Freq, Q;
            public override double End => Delay + Dur;

            public override void Mix(float[] buf, Random rnd)
            {
                int start = (int)(Delay * Rate);
                int len = (int)(Dur * Rate);
                // lọc dải thông (biquad, đỉnh 0 dB như BiquadFilterNode 'bandpass')
                double w0 = 2 * Math.PI * Freq / Rate, alpha = Math.Sin(w0) / (2 * Q), a0 = 1 + alpha;
                double b0 = alpha / a0, b2 = -alpha / a0, a1 = -2 * Math.Cos(w0) / a0, a2 = (1 - alpha) / a0;
                double x1 = 0, x2 = 0, y1 = 0, y2 = 0;
                for (int i = 0; i < len && start + i < buf.Length; i++)
                {
                    double x = (rnd.NextDouble() * 2 - 1) * (1 - (double)i / len);
                    double y = b0 * x + b2 * x2 - a1 * y1 - a2 * y2;
                    x2 = x1; x1 = x; y2 = y1; y1 = y;
                    buf[start + i] += (float)(y * Vol);
                }
            }
        }

        static Part T(double freq, double dur, Wave type = Wave.Sine, double vol = 0.12, double slide = 0, double delay = 0) =>
            new Tone { Freq = freq, Dur = dur, Type = type, Vol = vol, Slide = slide, Delay = delay };

        static Part N(double dur, double vol = 0.1, double freq = 1200, double q = 0.8, double delay = 0) =>
            new Noise { Dur = dur, Vol = vol, Freq = freq, Q = q, Delay = delay };

        static IEnumerable<Part> Seq(double[] freqs, double dur, Wave type, double vol, double start, double step)
        {
            for (int i = 0; i < freqs.Length; i++) yield return T(freqs[i], dur, type, vol, 0, start + i * step);
        }

        static List<Part> L(params object[] parts)
        {
            var l = new List<Part>();
            foreach (var p in parts)
                if (p is Part one) l.Add(one);
                else if (p is IEnumerable<Part> many) l.AddRange(many);
            return l;
        }

        // Tên tiếng giống bản web; "peg" là tiếng chạm đinh gốc 1100 Hz (AudioService đổi cao độ và giới hạn nhịp).
        static readonly Dictionary<string, Func<List<Part>>> Recipes = new Dictionary<string, Func<List<Part>>>
        {
            ["click"] = () => L(T(660, 0.07, Wave.Triangle, 0.08, 200)),
            ["pick"] = () => L(N(0.12, 0.12, 2400, 1.2), T(520, 0.08, Wave.Triangle, 0.05, 300)),
            ["deal"] = () => L(N(0.08, 0.06, 3200, 1.5)),
            ["card"] = () => L(T(440, 0.09, Wave.Square, 0.04, 220), N(0.06, 0.05, 1800)),
            ["hit"] = () => L(N(0.18, 0.22, 500, 0.7), T(140, 0.18, Wave.Sine, 0.22, -80)),
            ["hitCrit"] = () => L(N(0.18, 0.32, 500, 0.7), T(180, 0.18, Wave.Sine, 0.22, -80)),
            ["whoosh"] = () => L(N(0.25, 0.1, 900, 0.5)),
            ["heal"] = () => L(T(660, 0.12, Wave.Sine, 0.07), T(880, 0.16, Wave.Sine, 0.07, 0, 0.08)),
            ["buff"] = () => L(T(500, 0.08, Wave.Triangle, 0.06, 300), T(750, 0.1, Wave.Triangle, 0.06, 300, 0.07)),
            ["debuff"] = () => L(T(400, 0.2, Wave.Sawtooth, 0.04, -200)),
            ["shield"] = () => L(T(300, 0.15, Wave.Square, 0.04, 200), N(0.1, 0.05, 4000)),
            ["miss"] = () => L(T(900, 0.15, Wave.Sine, 0.05, -500)),
            ["coin"] = () => L(T(988, 0.07, Wave.Square, 0.05), T(1319, 0.14, Wave.Square, 0.05, 0, 0.06)),
            ["peg"] = () => L(T(1100, 0.04, Wave.Triangle, 0.06)),
            ["land"] = () => L(T(330, 0.12, Wave.Triangle, 0.08, -100)),
            ["chest"] = () => L(N(0.2, 0.12, 700), Seq(new double[] { 523, 659, 784, 1047 }, 0.18, Wave.Triangle, 0.07, 0.12, 0.07)),
            ["level"] = () => L(Seq(new double[] { 523, 659, 784, 1047, 1319 }, 0.22, Wave.Square, 0.05, 0, 0.09)),
            ["win"] = () => L(Seq(new double[] { 392, 523, 659, 784, 1047 }, 0.25, Wave.Triangle, 0.08, 0, 0.11)),
            ["lose"] = () => L(Seq(new double[] { 392, 349, 311, 262 }, 0.3, Wave.Triangle, 0.07, 0, 0.16)),
            ["ult"] = () => L(N(0.5, 0.18, 300, 0.5), T(110, 0.6, Wave.Sawtooth, 0.08, 220)),
            ["swap"] = () => L(N(0.15, 0.08, 1500), T(380, 0.12, Wave.Triangle, 0.06, 380)),
            ["error"] = () => L(T(160, 0.15, Wave.Square, 0.05)),
            ["stamp"] = () => L(N(0.12, 0.3, 300, 0.6), T(90, 0.2, Wave.Sine, 0.25, -40)),
        };

        public static IEnumerable<string> Names => Recipes.Keys;

        public static float[] Render(string name, int seed = 7)
        {
            if (!Recipes.TryGetValue(name, out var recipe)) return new float[0];
            var parts = recipe();
            double end = 0;
            foreach (var p in parts) end = Math.Max(end, p.End);
            var buf = new float[(int)Math.Ceiling(end * Rate) + 1];
            var rnd = new Random(seed);
            foreach (var p in parts) p.Mix(buf, rnd);
            for (int i = 0; i < buf.Length; i++) buf[i] = Math.Max(-1f, Math.Min(1f, buf[i]));
            return buf;
        }
    }
}
