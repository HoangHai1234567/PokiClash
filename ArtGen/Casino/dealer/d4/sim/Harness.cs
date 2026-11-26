// Đo mô phỏng viên bi Vòng Xoay ngoài Unity: py -3 -I chay.py [stats | dump <ô> <hạt giống>]
using System;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;

static class Harness
{
    static int Main(string[] args)
    {
        CultureInfo.DefaultThreadCurrentCulture = CultureInfo.InvariantCulture;
        string what = args.Length > 0 ? args[0] : "stats";
        if (what == "dump")
        {
            int pocket = args.Length > 1 ? int.Parse(args[1]) : 7;
            uint seed = args.Length > 2 ? uint.Parse(args[2]) : 1;
            var rng = new Rng(seed);
            double rot0 = rng.Range(0, Math.PI * 2);
            var tr = RouletteBall.Plan(RouletteWheel.SlotOf(pocket), rot0, RouletteBall.OmegaSpin, rng);
            var sb = new StringBuilder();
            sb.Append("{\"slot\":" + tr.slot + ",\"pocket\":" + pocket + ",\"duration\":" + tr.duration.ToString("0.###") + ",\"drop\":" + tr.dropTime.ToString("0.###") +
                      ",\"tries\":" + tr.tries + ",\"dt\":" + RlTrack.Dt.ToString("0.######") + ",\"rest\":[" + tr.restAngle.ToString("0.#####") + "," + tr.restR.ToString("0.####") + "],\"pts\":[");
            int n = tr.count + 240;   // thêm 2 giây bi nằm trong ô đi theo mâm
            for (int i = 0; i < n; i++)
            {
                tr.Sample(i * RlTrack.Dt, out float x, out float y, out float z);
                sb.Append((i > 0 ? "," : "") + "[" + x.ToString("0.####") + "," + y.ToString("0.####") + "," + z.ToString("0.####") + "," + tr.Rotor(i * RlTrack.Dt).ToString("0.####") + "]");
            }
            sb.Append("],\"hits\":[");
            sb.Append(string.Join(",", tr.hits.Select(h => "[" + h.t.ToString("0.###") + "," + (int)h.kind + "," + h.power.ToString("0.##") + "]")));
            sb.Append("]}");
            File.WriteAllText("track.json", sb.ToString());
            Console.WriteLine($"ô {pocket} vị trí {tr.slot}: {tr.duration:0.00}s, rời vách {tr.dropTime:0.00}s, {tr.laps10 / 10.0} vòng, {tr.diamondHits} mấu, {tr.hops} nảy, {tr.fretHits} va vách, vào ô {tr.capture:0.00}s, lệch pha {tr.shift} ô, {tr.tries} lần thử");
            return 0;
        }
        // thống kê: mô phỏng tự do (không chọn ô) để xem phân bố, thời lượng; rồi Plan cho mọi ô
        {
            var rng = new Rng(77);
            int n = 4000, ok = 0;
            var slots = new int[26];
            double cap = 0, dur = 0, durMin = 99, durMax = 0, drop = 0, laps = 0, frets = 0, dia = 0;
            int nice = 0, fails = 0;
            var fh = new int[30];
            var sw = System.Diagnostics.Stopwatch.StartNew();
            for (int i = 0; i < n; i++)
            {
                var tr = RouletteBall.Simulate(rng.Range(0, Math.PI * 2), RouletteBall.OmegaSpin, -rng.Range(RouletteBall.BallMin, RouletteBall.BallMax), unchecked((uint)(i * 2654435761u + 1)), null);
                if (tr == null) { if (fails++ < 12) Console.WriteLine("  không yên: " + RouletteBall.LastFail); continue; }
                ok++;
                fh[Math.Min(29, tr.hops)]++; cap += tr.capture;
                slots[tr.slot]++;
                dur += tr.duration; durMin = Math.Min(durMin, tr.duration); durMax = Math.Max(durMax, tr.duration);
                drop += tr.dropTime; laps += tr.laps10 / 10.0; frets += tr.fretHits; dia += tr.diamondHits;
                if (RouletteBall.Nice(tr)) nice++;
            }
            sw.Stop();
            Console.WriteLine($"tự do: {ok}/{n} nằm yên, {sw.ElapsedMilliseconds / (double)n:0.00} ms / cú; thời lượng tb {dur / ok:0.00}s ({durMin:0.0}..{durMax:0.0}), rời vách tb {drop / ok:0.00}s, vào ô tb {cap / ok:0.00}s, {laps / ok:0.0} vòng, {dia / ok:0.0} mấu, {frets / ok:0.0} vách; nhịp đẹp {nice * 100.0 / ok:0.0}%");
            Console.WriteLine("số lần va vách: " + string.Join(" ", fh));
            Console.WriteLine("phân bố vị trí: " + string.Join(" ", slots) + "  (đều = " + ok / 26 + ")");
        }
        {
            var rng = new Rng(2026);
            int maxTries = 0; long sum = 0; int cnt = 0, bad = 0, forced = 0;
            double dmin = 99, dmax = 0, dsum = 0;
            var sw = System.Diagnostics.Stopwatch.StartNew();
            for (int rep = 0; rep < 40; rep++)
                for (int pocket = 0; pocket < 26; pocket++)
                {
                    double rot0 = rng.Range(0, Math.PI * 2);
                    double om = RouletteBall.OmegaSpin * rng.Range(0.92, 1.08);
                    var tr = RouletteBall.Plan(RouletteWheel.SlotOf(pocket), rot0, om, rng);
                    cnt++;
                    if (tr == null || RouletteWheel.PocketAt(tr.slot) != pocket) { bad++; continue; }
                    if (tr.tries > 4000) forced++;
                    maxTries = Math.Max(maxTries, tr.tries); sum += tr.tries;
                    dmin = Math.Min(dmin, tr.duration); dmax = Math.Max(dmax, tr.duration); dsum += tr.duration;
                    tr.Sample(tr.duration - 1e-4f, out float ax, out float ay, out _);
                    tr.Sample(tr.duration + 1e-4f, out float bx, out float by, out _);
                    if (Math.Abs(ax - bx) + Math.Abs(ay - by) > 0.01) { bad++; Console.WriteLine($"giật cuối: {ax},{ay} -> {bx},{by}"); }
                }
            sw.Stop();
            Console.WriteLine($"Plan: {cnt} cú, sai {bad}, ép {forced}; số lần thử tb {sum / (double)cnt:0.0}, nhiều nhất {maxTries}; {sw.ElapsedMilliseconds / (double)cnt:0.0} ms / cú; thời lượng {dmin:0.0}..{dmax:0.0}, tb {dsum / cnt:0.00}s");
        }
        for (int p = 0; p < 26; p++)
            if (RouletteWheel.PocketAt(RouletteWheel.SlotOf(p)) != p) { Console.WriteLine("LOI xếp ô " + p); return 1; }
        Console.WriteLine("xếp ô: " + string.Join(" ", Enumerable.Range(0, 26).Select(s => RouletteWheel.PocketAt(s))));
        return 0;
    }
}
