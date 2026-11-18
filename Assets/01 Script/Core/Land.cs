// Đảo kiểu vùng đất (GD_Claude/18_DaoVungDat_Habitat.md, 2026-11-18): một đảo rộng kéo hai chiều, mỗi ải tướng một habitat (bệ
// tròn) đặt cố định trên ảnh nền, một đường duy nhất đi qua từng habitat theo thứ tự ải. Ải xen giữa là chấm trên đường, ZoneScene
// tự rải theo đường (LandLayout). Toạ độ theo tỉ lệ 0..1 của ảnh nền (y từ trên). Khối "land" trong zones.json do
// ArtGen/Islands/land_thuy/m0/build_land.py ghi; đảo không có khối này thì màn đảo chạy kiểu cũ.
// Vùng boss (secs, người dùng 2026-11-18: đánh xong boss thì mở vùng sau, vùng chưa mở tối đen, tướng đứng im): vùng k ứng với
// habitat k (đoạn đường từ boss k-1 tới boss k cộng bệ boss k), mở khi đã qua ải của boss k-1; chia bằng m0/vung.py. Vùng khoá vẽ
// phác chì dưới mây phủ, mở thì mây tan, bút chì tô màu (người dùng 2026-11-18: "kết hợp cả A và B, mây tan ra, có bút chì vào tô màu").
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    [Serializable]
    public class LandHab
    {
        public int stage;     // số ải (idx) của ải tướng đứng ở habitat này
        public Pt at;         // tâm bệ (chỗ tướng đứng), tỉ lệ ảnh nền
        public int size = 3;  // 3: habitat thường, 4: habitat to (mini boss, boss)
        public int plate = 1; // bảng tên bên phải (1) hay trái (-1)
        public Pt ring;       // bán trục ngang, dọc của vòng đá, tỉ lệ ảnh nền (chấm ải không đè lên)
    }

    // số vùng boss đã diễn cảnh mở (mây tan, bút chì tô) của từng đảo, lưu trong SaveData.extra["landShown"] (không thêm trường vào bản
    // lưu): vùng đã mở mà chưa diễn thì vào đảo diễn, kể cả vùng 0 lần đầu vào đảo (người dùng 2026-11-18: "lần đầu tiên vào mỗi đảo sẽ
    // có đoạn mở section đầu tiên … mỗi khi unlock section đều bắt người chơi phải xem")
    public static class LandShown
    {
        const string Key = "landShown";

        public static int Get(SaveData s, Elem e)
        {
            if (s?.extra == null || !s.extra.TryGetValue(Key, out var o) || !(o is Dictionary<string, object> d)) return 0;
            return d.TryGetValue(e.ToString().ToLowerInvariant(), out var v) && v != null ? Convert.ToInt32(v) : 0;
        }

        // chỉ đổi trong bộ nhớ: lần lưu kế tiếp ghi xuống (gọi Save ở đây làm màn đang mở dựng lại)
        public static void Set(SaveData s, Elem e, int n)
        {
            if (s?.extra == null) return;
            if (!s.extra.TryGetValue(Key, out var o) || !(o is Dictionary<string, object> d))
            {
                d = new Dictionary<string, object>();
                s.extra[Key] = d;
            }
            d[e.ToString().ToLowerInvariant()] = (double)Math.Max(0, n);
        }
    }

    // cờ đánh dấu theo vùng của từng đảo (bit k = vùng k) trong SaveData.extra: landGift (rương bí ẩn đã nhận), landPoke (đã hắt xì nhận
    // quà chọc mây); chỉ đổi trong bộ nhớ, người gọi tự lưu
    public static class LandBits
    {
        public static bool Has(SaveData s, string key, Elem e, int k) => (Get(s, key, e) & (1 << k)) != 0;

        public static int Get(SaveData s, string key, Elem e)
        {
            if (s?.extra == null || !s.extra.TryGetValue(key, out var o) || !(o is Dictionary<string, object> d)) return 0;
            return d.TryGetValue(e.ToString().ToLowerInvariant(), out var v) && v != null ? Convert.ToInt32(v) : 0;
        }

        public static void Add(SaveData s, string key, Elem e, int k)
        {
            if (s?.extra == null) return;
            if (!s.extra.TryGetValue(key, out var o) || !(o is Dictionary<string, object> d))
            {
                d = new Dictionary<string, object>();
                s.extra[key] = d;
            }
            d[e.ToString().ToLowerInvariant()] = (double)(Get(s, key, e) | (1 << k));
        }
    }

    // easter egg vùng khoá: hiệu ứng rò qua mây (k: dom_dom, den_bien, bong_bong, chim, set, phun_nuoc, phat_sang, tuyet, xoay)
    [Serializable]
    public class LandTease
    {
        public string k;
        public double x, y, s; // tâm, cỡ (tỉ lệ vùng đất; s theo bề ngang)
    }

    [Serializable]
    public class LandSec
    {
        public double x0, y0, x1, y1; // khung vùng, tỉ lệ vùng đất (y từ trên)
        // mây phủ khi vùng chưa mở, mỗi đám 4 số: x, y (tâm, tỉ lệ vùng đất), w (bề ngang, tỉ lệ bề ngang vùng đất), lật (0/1)
        public List<double> clouds = new List<double>();
        // easter egg khi vùng còn khoá (người dùng 2026-11-18): rương bí ẩn (bi khi mở vùng; cx < 0: không có), ghi chú bút chì
        // (ảnh, tâm, bề ngang), hiệu ứng rò qua mây
        public double cx = -1, cy = -1;
        public int gift;
        public string note;
        public double nx, ny, nw;
        public List<LandTease> tease = new List<LandTease>();
    }

    [Serializable]
    public class LandDef
    {
        public string art;           // ảnh nền (Assets/03 Art/Islands)
        public string sea;           // tấm biển lặp quanh đảo, cắt từ nét biển của ảnh nền (rỗng: biển của màn đảo)
        public string cloud;         // hình mây phủ vùng boss chưa mở (một hình cho mọi đám, gộp lệnh vẽ)
        public double w, h;          // cỡ vùng đất, px khung 1080
        public double pip, pipNow;   // cỡ chấm ải xen giữa, chấm ải đang đánh (px khung 1080)
        public List<Pt> path = new List<Pt>(); // tâm con đường từ bến tới habitat cuối
        // giới hạn kéo, zoom ra ngoài ảnh (trái, phải, trên, dưới; tỉ lệ bề ngang ảnh): vẫn trong vành mây, không lộ khối phủ ngoài
        public List<double> pan = new List<double>();
        public List<LandHab> habs = new List<LandHab>();
        public List<LandSec> secs = new List<LandSec>(); // theo thứ tự habs; rỗng: không chia vùng (mọi chỗ đủ màu)
        // lưới vùng thô (ẩn hiệu ứng, đèn trong vùng khoá): gw × gh ô phủ cả vùng đất, mỗi ô một ký tự '0'..'9' (vùng) hoặc '.' (biển)
        public int gw, gh;
        public string grid = "";

        // vùng ở chỗ (fx, fy) tỉ lệ vùng đất (y từ trên); -1: biển hay không có lưới
        public int SectionAt(double fx, double fy)
        {
            if (gw <= 0 || gh <= 0 || grid.Length < gw * gh) return -1;
            int i = (int)Math.Floor(fx * gw), j = (int)Math.Floor(fy * gh);
            if (i < 0 || j < 0 || i >= gw || j >= gh) return -1;
            char c = grid[j * gw + i];
            return c >= '0' && c <= '9' ? c - '0' : -1;
        }

        // số vùng đã mở với prog ải đã qua: vùng 0 luôn mở, vùng k mở khi đã qua ải boss k-1
        public int OpenSections(int prog)
        {
            int n = 1;
            for (int k = 0; k + 1 < habs.Count; k++)
                if (prog >= habs[k].stage) n++;
            return n;
        }

        // vùng của ải idx: ải tướng là vùng của habitat đó, ải xen giữa là vùng của habitat kế tiếp
        public int SectionOf(int idx)
        {
            for (int k = 0; k < habs.Count; k++)
                if (idx <= habs[k].stage) return k;
            return habs.Count - 1;
        }

        public bool Has => habs != null && habs.Count > 0 && path != null && path.Count > 1 && w > 0 && h > 0;

        static Pt P(object v)
        {
            var a = J.Arr(v);
            return a.Count >= 2 ? new Pt(Convert.ToDouble(a[0]), Convert.ToDouble(a[1])) : default;
        }

        public static LandDef Parse(Dictionary<string, object> o)
        {
            var l = new LandDef();
            if (o == null) return l;
            l.art = J.Str(o, "art");
            l.sea = J.Str(o, "sea");
            l.cloud = J.Str(o, "cloud");
            var size = J.Arr(o, "size");
            if (size.Count >= 2)
            {
                l.w = Convert.ToDouble(size[0]);
                l.h = Convert.ToDouble(size[1]);
            }
            var pip = J.Arr(o, "pip");
            l.pip = pip.Count > 0 ? Convert.ToDouble(pip[0]) : 72;
            l.pipNow = pip.Count > 1 ? Convert.ToDouble(pip[1]) : l.pip * 1.25;
            foreach (var p in J.Arr(o, "path")) l.path.Add(P(p));
            foreach (var v in J.Arr(o, "pan")) l.pan.Add(Convert.ToDouble(v));
            foreach (var x in J.Arr(o, "habs"))
            {
                var h = J.Obj(x);
                if (h == null) continue;
                l.habs.Add(new LandHab
                {
                    stage = J.Int(h, "stage"),
                    at = P(J.Get(h, "at")),
                    size = J.Int(h, "size", 3),
                    plate = J.Int(h, "plate", 1) >= 0 ? 1 : -1,
                    ring = P(J.Get(h, "ring")),
                });
            }
            foreach (var x in J.Arr(o, "secs"))
            {
                var c = J.Obj(x);
                if (c == null) continue;
                var b = J.Arr(c, "box");
                var sec = new LandSec
                {
                    x0 = b.Count > 3 ? Convert.ToDouble(b[0]) : 0, y0 = b.Count > 3 ? Convert.ToDouble(b[1]) : 0,
                    x1 = b.Count > 3 ? Convert.ToDouble(b[2]) : 0, y1 = b.Count > 3 ? Convert.ToDouble(b[3]) : 0,
                };
                var ch = J.Arr(c, "chest");
                if (ch.Count >= 2)
                {
                    sec.cx = Convert.ToDouble(ch[0]);
                    sec.cy = Convert.ToDouble(ch[1]);
                    sec.gift = J.Int(c, "gift");
                }
                var nt = J.Obj(c, "note");
                if (nt != null)
                {
                    sec.note = J.Str(nt, "a");
                    sec.nx = J.Num(nt, "x");
                    sec.ny = J.Num(nt, "y");
                    sec.nw = J.Num(nt, "w");
                }
                foreach (var tz in J.Arr(c, "tease"))
                {
                    var t = J.Obj(tz);
                    if (t != null) sec.tease.Add(new LandTease { k = J.Str(t, "k"), x = J.Num(t, "x"), y = J.Num(t, "y"), s = J.Num(t, "s") });
                }
                foreach (var cl in J.Arr(c, "clouds"))
                {
                    var q = J.Arr(cl);
                    if (q.Count < 4) continue;
                    for (int i = 0; i < 4; i++) sec.clouds.Add(Convert.ToDouble(q[i]));
                }
                l.secs.Add(sec);
            }
            var g = J.Obj(o, "grid");
            if (g != null)
            {
                l.gw = J.Int(g, "w");
                l.gh = J.Int(g, "h");
                l.grid = J.Str(g, "d") ?? "";
            }
            return l;
        }

        // lỗi dữ liệu (GameData.Validate): mỗi ải tướng đúng một habitat theo thứ tự ải, toạ độ trong ảnh, đủ điểm đường
        public IEnumerable<string> Check(string zone, IList<int> heroStages)
        {
            if (!Has) yield break;
            static bool In01(Pt p) => p.x >= 0 && p.x <= 1 && p.y >= 0 && p.y <= 1;
            if (string.IsNullOrEmpty(art)) yield return $"{zone}: vùng đất thiếu ảnh nền";
            if (path.Any(p => !In01(p))) yield return $"{zone}: vùng đất có điểm đường ngoài 0–1";
            var st = habs.Select(x => x.stage).ToList();
            if (!st.SequenceEqual(heroStages))
                yield return $"{zone}: habitat ({string.Join(", ", st)}) phải khớp đúng thứ tự ải tướng ({string.Join(", ", heroStages)})";
            foreach (var x in habs)
            {
                if (!In01(x.at)) yield return $"{zone}: habitat ải {x.stage} có tâm {x.at} ngoài 0–1";
                if (x.size != 3 && x.size != 4) yield return $"{zone}: habitat ải {x.stage} cỡ {x.size} (chỉ 3 hoặc 4)";
                if (x.ring.x <= 0 || x.ring.y <= 0) yield return $"{zone}: habitat ải {x.stage} thiếu cỡ vòng đá";
            }
            if (secs.Count > 0 && secs.Count != habs.Count) yield return $"{zone}: vùng đất có {secs.Count} vùng boss, phải bằng số habitat {habs.Count}";
            for (int k = 0; k < secs.Count; k++)
            {
                var c = secs[k];
                if (c.clouds.Count == 0) yield return $"{zone}: vùng boss {k} không có mây phủ";
                if (!(c.x0 >= 0 && c.y0 >= 0 && c.x1 <= 1 && c.y1 <= 1 && c.x1 > c.x0 && c.y1 > c.y0)) yield return $"{zone}: vùng boss {k} có khung sai";
            }
            if (secs.Count > 0 && (gw <= 0 || gh <= 0 || grid.Length != gw * gh)) yield return $"{zone}: lưới vùng {gw} x {gh} không khớp {grid.Length} ô";
            if (pip <= 0 || pipNow < pip) yield return $"{zone}: cỡ chấm ải vùng đất ({pip}, {pipNow}) không hợp lệ";
        }
    }
}
