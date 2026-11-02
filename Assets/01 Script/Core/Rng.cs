// Bộ số ngẫu nhiên có hạt giống (mulberry32), chép đúng phép bit của Web/src/core/rng.ts:
// cùng hạt giống thì cùng chuỗi số với bản web (Math.imul -> nhân int có tràn, >>> -> uint).
using System;
using System.Collections.Generic;
using System.Globalization;

namespace PokiClash.Core
{
    public sealed class Rng
    {
        public uint S;

        public Rng(uint seed)
        {
            S = seed == 0 ? 1u : seed;
        }

        public double Next()
        {
            unchecked
            {
                S += 0x6d2b79f5u;
                int t = (int)S;
                t = (t ^ (int)((uint)t >> 15)) * (t | 1);
                t ^= t + (t ^ (int)((uint)t >> 7)) * (t | 61);
                return (uint)(t ^ (int)((uint)t >> 14)) / 4294967296.0;
            }
        }

        public double Range(double a, double b) => a + (b - a) * Next();

        public int Int(int a, int b) => a + (int)Math.Floor(Next() * (b - a + 1));

        public bool Chance(double p) => Next() < p;

        public T Pick<T>(IReadOnlyList<T> arr) => arr[(int)Math.Floor(Next() * arr.Count)];

        public T Weighted<T>(IReadOnlyList<T> items, Func<T, double> weight)
        {
            double total = 0;
            foreach (var it in items) total += Math.Max(0, weight(it));
            double r = Next() * total;
            foreach (var it in items)
            {
                r -= Math.Max(0, weight(it));
                if (r < 0) return it;
            }
            return items[items.Count - 1];
        }

        static readonly Random Sys = new Random();
        public static uint RandomSeed() => unchecked((uint)Sys.Next(int.MinValue, int.MaxValue));
    }

    // Phép toán cho khớp JavaScript.
    public static class Js
    {
        // Math.round của JS: làm tròn .5 lên phía +vô cùng (khác Math.Round của C#).
        public static double Round(double x)
        {
            if (double.IsNaN(x) || double.IsInfinity(x)) return x;
            double f = Math.Floor(x);
            return x - f >= 0.5 ? f + 1 : f;
        }

        public static int RoundInt(double x) => (int)Round(x);

        // String(number) của JS cho số thường gặp (không dạng mũ).
        public static string Num(double x)
        {
            if (x == Math.Floor(x) && Math.Abs(x) < 1e15) return ((long)x).ToString(CultureInfo.InvariantCulture);
            return x.ToString("R", CultureInfo.InvariantCulture);
        }
    }
}
