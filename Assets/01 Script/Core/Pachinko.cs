// Máy bi: vật lý thuần (đinh, nấm, mái, đáy V, vách, ô) chép đúng bàn table_01 của máy bi tham khảo (đục ở D:\CrittersRipper,
// báo cáo analysis/PINBALL_REPORT.md): toạ độ, cỡ, vật liệu, trọng lực, cản, kẹp tốc, lực phóng; bi phóng lên làn phải rồi ra
// bàn ở hốc trên phải. Kết quả chọn theo bảng tỉ lệ (cfg.odds) rồi phát một đường bi vật lý thật rơi đúng chỗ đó (Board.odds).
// Vật lý tự viết (không dùng Physics2D) để có hạt giống, chạy được trong EditMode test và mô phỏng.
// Toạ độ máy: x sang phải, y xuống, khung BW × BH; một u của máy tham khảo bằng U đơn vị máy (X(), Y() đổi từ u, y lên, sang máy).
// Bảng thưởng ở cuối file: ô đáy, rương, mốc Huyền thoại, mốc quà, vòng nấm.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum SlotKind { Exp5, Exp10, Exp15, Ball, ChestWood, ChestSilver, ChestGold }
    public enum PegKind { Peg, Bumper, Post, Top }
    public enum SegKind { Wall, Ceiling, Shoulder, Divider, Roof, Floor }

    // vật cản tròn; e: hệ số nảy, f: ma sát (đã trộn với bi như Box2D: nảy lấy max, ma sát lấy căn của tích)
    public struct Peg
    {
        public double x, y, r, e, f;
        public PegKind kind;
    }

    // đoạn thẳng có bề dày (viên con nhộng bán kính r; r = 0 là cạnh mỏng như khung)
    public struct Seg
    {
        public double x1, y1, x2, y2, r, e, f;
        public SegKind kind;
    }

    // ô cảm biến hình chữ nhật w × h quanh (x, y): bi chạm vào là vào (như trigger của máy tham khảo)
    public struct Cup
    {
        public double x, y, r, w, h;
        public SlotKind reward;
    }

    // ô đáy: cảm biến chữ nhật [x0, x1] × [y0, y1]
    public struct Slot
    {
        public double x0, x1, y0, y1;
        public SlotKind reward;
    }

    public sealed class Ball
    {
        public int id;
        public double x, y, vx, vy;
        public int mult;
        public bool alive;
        public double age;
        public double lane = -1, laneV; // quãng đã đi trên làn phóng (âm: đã ra bàn), tốc lúc ra bàn
        public int target = -1; // kết quả đã chọn theo bảng tỉ lệ (-1: vật lý thuần)
    }

    // sự kiện của một bước: chạm đinh (peg) hoặc rơi vào ô / cốc (land)
    public struct PEvent
    {
        public bool land;
        public int peg;
        public double speed;
        public SlotKind reward;
        public int slot; // -1 nếu là cốc
        public bool cup;
        public Ball ball;
    }

    public sealed class Board
    {
        public const double BW = 460, BH = 680;
        public const double U = 78;            // đơn vị máy mỗi u của máy tham khảo
        const double XC = 0.15, YT = 5.27, Y0 = 2; // u ở giữa bề ngang máy; u ở y = Y0 của máy
        public static double X(double u) => BW / 2 + (u - XC) * U;
        public static double Y(double v) => Y0 + (YT - v) * U;

        public const double BallR = 0.081 * U;

        // vật liệu máy tham khảo, trộn với bi (bi: ma sát 0,4, nảy 0): đinh, mái, đáy V nảy 0,8 trơn; nấm đỉnh nảy 0,9 trơn;
        // nấm lớn, khung, vách ô nảy 0,8, ma sát 0,22. Va chậm hơn VRest (tốc pháp tuyến 1 u/giây) thì không nảy.
        public const double ERed = 0.8, ETop = 0.9, EGreen = 0.8, EOrange = 0.8, Fric = 0.22, EBall = 0;
        public const double VRest = 1 * U;
        // config máy tham khảo: gravity 2 (hệ số trọng lực, 2 × 9,81 u/giây²), linerDrag 0, kẹp tốc 4–14 u/giây
        public const double Gravity = 2 * 9.81 * U, Drag = 0, VMin = 4 * U, VMax = 14 * U;
        // lực phóng 650–680 trong một bước vật lý 0,016 giây (khối lượng 1): bi ra hốc với tốc 10,4–10,88 u/giây
        public const double ForceMin = 650, ForceMax = 680, ForceStep = 0.016, LaneSpeed = 22;
        public const int Sub = 6;
        public const double Dt = 1.0 / 60;

        // làn phóng (ngoài khung, mép phải): chân làn, cột dọc, cung quẹo trái, đoạn thẳng vào hốc trên phải của khung
        public const double LaneX = 2.95, LaneY0 = -2.40, LaneArc = 0.35, SpawnX = 1.90, SpawnY = 3.875, LaunchDeg = 180;
        public const double LaneHalf = 0.14; // nửa bề rộng làn (u), chỉ để vẽ

        // khung (EdgeCollider2D 26 điểm, toạ độ cục bộ, cộng FrameOff ra toạ độ thế giới)
        static readonly double[] FrameLocal =
        {
            2.2089016, 3.345851, 1.87046, 3.6171837, 1.7288232, 3.7200484, 1.5218911, 3.8511472, 1.0295405, 4.0875382,
            0.4182581, 4.2168994, -0.11059916, 4.2297378, -0.78265035, 3.981679, -1.31617, 3.6897738, -1.8864664, 3.1892915,
            -2.1675763, 2.7234316, -2.3872023, 2.1623313, -2.4576142, 1.7333742, -2.6003926, -3.9567394, 2.8873246, -3.9442213,
            2.874138, -2.6719983, 2.7744408, 0.75676656, 2.7682333, 0.87337214, 2.7615075, 1.4047263, 2.7017133, 1.7555923,
            2.6676772, 1.8573519, 2.5102212, 2.175478, 2.1901445, 2.6679869, 1.8889656, 2.9717264, 1.9500747, 3.1286397,
            2.1997778, 3.3453755,
        };
        const double FrameDX = -0.18, FrameDY = 0.55;

        // 22 đinh r 0,15 (u)
        static readonly double[] PegsU =
        {
            0, 3.892, -0.9, 3.5, 0.9, 3.5, -1.6, 2.9, 0.012, 2.9, 1.6, 2.9, -0.7, 2.5, 0.7, 2.5, 0, 1.9, -0.61, 1.2, 0.61, 1.2,
            -2, 0.8, 2, 0.8, -1, 0.45, 0, 0.491, 1, 0.45, -1.6, 0, 1.6, 0, -2, -0.55, 2, -0.55, -1.6, -1.2, 1.6, -1.2,
        };

        // vách ô: thân rộng 0,228, đầu tròn ở y −2,01
        static readonly double[] DividerU = { -1.75, -0.572, 0.571, 1.734 };
        public const double DividerTopU = -2.010, DividerHalfU = 0.114;

        // ô đáy (trái sang phải): kẹo ngoài, kẹo + sự kiện, ô khuất (jackpot), kẹo + sự kiện, kẹo ngoài
        public static readonly SlotKind[] SlotLayout = { SlotKind.Exp5, SlotKind.Exp10, SlotKind.ChestGold, SlotKind.Exp10, SlotKind.Exp5 };
        // cảm biến ô (u): tâm x, bề rộng, tâm y, chiều cao
        static readonly double[] SlotU =
        {
            -2.343, 1.024, -2.756, 1.402, -1.165, 1.024, -2.756, 1.402, -0.005, 1.15, -2.756, 1.15,
            1.150, 1.024, -2.756, 1.402, 2.317, 1.024, -2.756, 1.402,
        };
        // cốc thẻ dưới mái (u): tâm, cỡ
        public const double GiftXU = 0.012, GiftYU = -0.832, GiftWU = 0.80, GiftHU = 1.21;
        public const SlotKind GiftReward = SlotKind.ChestSilver;

        public readonly List<Peg> pegs = new List<Peg>();
        public readonly List<Cup> cups = new List<Cup>();
        public readonly List<Slot> slots = new List<Slot>();
        public readonly List<Seg> segs = new List<Seg>();
        public List<Ball> balls = new List<Ball>();
        public readonly int[] ringPeg = { -1, -1 }; // chỉ số hai nấm lớn (trái: trứng, phải: khiên)
        public int topPeg = -1;
        public readonly List<(double x, double y)> lane = new List<(double, double)>(); // đường làn (toạ độ máy), điểm cuối là chỗ bi ra bàn
        readonly List<double> laneAt = new List<double>(); // quãng tích luỹ tới từng điểm làn
        public double LaneLength => laneAt.Count > 0 ? laneAt[laneAt.Count - 1] : 0;
        public Rng rng;
        int nextId = 1;

        public Board(uint seed = 1)
        {
            rng = new Rng(seed);
            Build();
        }

        void AddPeg(double xu, double yu, double ru, PegKind kind, double e, double f) =>
            pegs.Add(new Peg { x = X(xu), y = Y(yu), r = ru * U, kind = kind, e = e, f = f });

        void AddSeg(double x1u, double y1u, double x2u, double y2u, double ru, SegKind kind, double e, double f) =>
            segs.Add(new Seg { x1 = X(x1u), y1 = Y(y1u), x2 = X(x2u), y2 = Y(y2u), r = ru * U, kind = kind, e = e, f = f });

        // BoxCollider2D (tâm, góc quay độ ngược kim đồng hồ, rộng w, dài h theo trục y cục bộ) thành viên con nhộng cùng dài
        void AddBox(double cx, double cy, double deg, double w, double h, bool mirror, SegKind kind, double e, double f)
        {
            double a = deg * Math.PI / 180, ax = -Math.Sin(a), ay = Math.Cos(a);
            if (mirror) ax = -ax;
            double r = w / 2, hl = h / 2 - r;
            AddSeg(cx - ax * hl, cy - ay * hl, cx + ax * hl, cy + ay * hl, r, kind, e, f);
        }

        void Build()
        {
            int n = FrameLocal.Length / 2;
            for (int i = 0; i + 1 < n; i++)
                AddSeg(FrameLocal[2 * i] + FrameDX, FrameLocal[2 * i + 1] + FrameDY, FrameLocal[2 * i + 2] + FrameDX, FrameLocal[2 * i + 3] + FrameDY,
                    0, SegKind.Wall, EOrange, Fric);
            for (int i = 0; i < PegsU.Length; i += 2) AddPeg(PegsU[i], PegsU[i + 1], 0.15, PegKind.Peg, ERed, 0);
            topPeg = pegs.Count;
            AddPeg(-0.033, 4.917, 0.352, PegKind.Top, ETop, 0);
            ringPeg[0] = pegs.Count;
            AddPeg(-1.65, 1.985, 0.55, PegKind.Bumper, EGreen, Fric);
            ringPeg[1] = pegs.Count;
            AddPeg(1.65, 1.985, 0.55, PegKind.Bumper, EGreen, Fric);
            // mái "cánh" hai bên cốc thẻ: mỗi bên hai thanh 0,19 × 0,53
            AddBox(-0.495, -0.052, -69.1, 0.191, 0.535, false, SegKind.Roof, ERed, 0);
            AddBox(-0.828, -0.267, -52.0, 0.191, 0.533, false, SegKind.Roof, ERed, 0);
            AddBox(0.495, -0.053, -69.1, 0.191, 0.535, true, SegKind.Roof, ERed, 0);
            AddBox(0.828, -0.268, -52.0, 0.191, 0.533, true, SegKind.Roof, ERed, 0);
            // đáy chữ V dưới cốc thẻ: hai thanh và ba núm
            AddBox(-0.358, -1.308, -106.7, 0.18, 0.698, false, SegKind.Floor, ERed, 0);
            AddBox(0.372, -1.331, -72.4, 0.18, 0.627, false, SegKind.Floor, ERed, 0);
            AddPeg(0.691, -1.205, 0.092, PegKind.Post, ERed, 0);
            AddPeg(0.012, -1.402, 0.128, PegKind.Post, ERed, 0);
            AddPeg(-0.667, -1.196, 0.096, PegKind.Post, ERed, 0);
            foreach (var x in DividerU) AddSeg(x, DividerTopU, x, -3.33, DividerHalfU, SegKind.Divider, EOrange, Fric);
            for (int i = 0; i < SlotLayout.Length; i++)
            {
                double cx = SlotU[4 * i], w = SlotU[4 * i + 1], cy = SlotU[4 * i + 2], h = SlotU[4 * i + 3];
                slots.Add(new Slot { x0 = X(cx - w / 2), x1 = X(cx + w / 2), y0 = Y(cy + h / 2), y1 = Y(cy - h / 2), reward = SlotLayout[i] });
            }
            cups.Add(new Cup { x = X(GiftXU), y = Y(GiftYU), w = GiftWU * U, h = GiftHU * U, reward = GiftReward });
            BuildLane();
            BuildGrid();
        }

        // lưới tra nhanh: mỗi ô lưới giữ danh sách đinh, đoạn có thể chạm bi ở trong ô (theo thứ tự chỉ số, như duyệt hết)
        const double Cell = 20, Reach = BallR + 4;
        int gw, gh;
        int[][] gridPegs, gridSegs;

        static double RectDist(double x0, double y0, double x1, double y1, double px, double py)
        {
            double dx = Math.Max(Math.Max(x0 - px, 0), px - x1), dy = Math.Max(Math.Max(y0 - py, 0), py - y1);
            return Math.Sqrt(dx * dx + dy * dy);
        }

        void BuildGrid()
        {
            gw = (int)Math.Ceiling(BW / Cell);
            gh = (int)Math.Ceiling(BH / Cell);
            gridPegs = new int[gw * gh][];
            gridSegs = new int[gw * gh][];
            var lp = new List<int>();
            var ls = new List<int>();
            for (int gy = 0; gy < gh; gy++)
                for (int gx = 0; gx < gw; gx++)
                {
                    double x0 = gx * Cell, y0 = gy * Cell, x1 = x0 + Cell, y1 = y0 + Cell;
                    lp.Clear();
                    ls.Clear();
                    for (int i = 0; i < pegs.Count; i++)
                        if (RectDist(x0, y0, x1, y1, pegs[i].x, pegs[i].y) < pegs[i].r + Reach) lp.Add(i);
                    for (int i = 0; i < segs.Count; i++)
                    {
                        var g = segs[i];
                        // khoảng cách đoạn tới ô lưới: lấy mẫu dày dọc đoạn (đủ chính xác vì có dư Reach)
                        double best = double.MaxValue, len = Math.Sqrt((g.x2 - g.x1) * (g.x2 - g.x1) + (g.y2 - g.y1) * (g.y2 - g.y1));
                        int n = Math.Max(1, (int)Math.Ceiling(len / 2));
                        for (int k = 0; k <= n; k++)
                            best = Math.Min(best, RectDist(x0, y0, x1, y1, g.x1 + (g.x2 - g.x1) * k / n, g.y1 + (g.y2 - g.y1) * k / n));
                        if (best < g.r + Reach + 1) ls.Add(i);
                    }
                    gridPegs[gy * gw + gx] = lp.ToArray();
                    gridSegs[gy * gw + gx] = ls.ToArray();
                }
        }

        // làn: cột dọc x = LaneX từ chân làn, cung bán kính LaneArc quẹo trái tới hướng LaunchDeg, đoạn thẳng tới chỗ ra bàn
        void BuildLane()
        {
            lane.Clear();
            laneAt.Clear();
            double phi = LaunchDeg * Math.PI / 180, rho = LaneArc;
            double endX = LaneX - rho + rho * Math.Sin(phi);
            double len = (SpawnX - endX) / Math.Cos(phi);
            double endY = SpawnY - len * Math.Sin(phi);
            double cx = LaneX - rho, cy = endY + rho * Math.Cos(phi);
            var pts = new List<(double, double)> { (LaneX, LaneY0), (LaneX, cy) };
            int steps = 12;
            for (int i = 1; i <= steps; i++)
            {
                double t = (phi - Math.PI / 2) * i / steps; // góc quay từ hướng lên
                pts.Add((cx + rho * Math.Cos(t), cy + rho * Math.Sin(t)));
            }
            pts.Add((SpawnX, SpawnY));
            double at = 0;
            (double x, double y) prev = (0, 0);
            for (int i = 0; i < pts.Count; i++)
            {
                var (xu, yu) = pts[i];
                var q = (X(xu), Y(yu));
                if (i > 0) at += Math.Sqrt((q.Item1 - prev.x) * (q.Item1 - prev.x) + (q.Item2 - prev.y) * (q.Item2 - prev.y));
                if (i > 0 && at - laneAt[laneAt.Count - 1] < 1e-6) continue;
                lane.Add(q);
                laneAt.Add(at);
                prev = q;
            }
        }

        // Bảng tỉ lệ (null: vật lý thuần, lực phóng ngẫu nhiên): xác suất từng kết quả theo thứ tự ô đáy rồi tới cốc. Có bảng thì
        // mỗi lần phóng chọn kết quả theo bảng, rồi tìm một lực phóng mà đường bi thật (cùng vật lý, bi không va bi) rơi đúng chỗ
        // đó: máy tham khảo có bộ ghi và phát lại đường bi, tỉ lệ công bố của nó (cốc thẻ 3,3 %) xa tỉ lệ vật lý thuần của chính bàn
        // ấy (khoảng 20 %). Các lực thử trúng chỗ khác được giữ lại (mỗi kết quả tối đa PoolCap) cho lần sau.
        public double[] odds;
        public const int MaxTries = 400, PoolCap = 48;
        readonly Dictionary<int, Queue<double>> pool = new Dictionary<int, Queue<double>>();
        public int tries, misses; // số lần thử vật lý, số lần phóng không tìm được đường đúng (đếm cho test)

        public int Outcomes => slots.Count + cups.Count;

        // kết quả của một bi: chỉ số ô đáy, hoặc slots.Count + chỉ số cốc
        public int OutcomeOf(PEvent e) => e.cup ? slots.Count + cups.FindIndex(c => c.reward == e.reward) : e.slot;

        // hình học bàn (toạ độ máy) cho script ghép ảnh mặt máy tĩnh ArtGen/Pachinko/ghep_ban.py, ghi ở ArtGen/Pachinko/refs/mat_may.json
        // (menu "PokiClash/Prefab/Máy bi: xuất hình học mặt máy"; test MatMay_AnhGhepKhopHinhHoc báo khi file lệch code)
        public string GeometryJson()
        {
            string F(double v) => v.ToString("0.###", System.Globalization.CultureInfo.InvariantCulture);
            var sb = new System.Text.StringBuilder();
            sb.Append("{\n");
            sb.Append($" \"bw\": {F(BW)}, \"bh\": {F(BH)}, \"u\": {F(U)}, \"ball_r\": {F(BallR)}, \"lane_half\": {F(LaneHalf * U)},\n");
            sb.Append(" \"pegs\": [" + string.Join(", ", pegs.Select(p => $"[{F(p.x)}, {F(p.y)}, {F(p.r)}, \"{p.kind}\"]")) + "],\n");
            sb.Append(" \"segs\": [" + string.Join(", ", segs.Select(g => $"[{F(g.x1)}, {F(g.y1)}, {F(g.x2)}, {F(g.y2)}, {F(g.r)}, \"{g.kind}\"]")) + "],\n");
            sb.Append(" \"cups\": [" + string.Join(", ", cups.Select(c => $"[{F(c.x - c.w / 2)}, {F(c.y - c.h / 2)}, {F(c.x + c.w / 2)}, {F(c.y + c.h / 2)}, \"{Pachinko.Key(c.reward)}\"]")) + "],\n");
            sb.Append(" \"slots\": [" + string.Join(", ", slots.Select(c => $"[{F(c.x0)}, {F(c.y0)}, {F(c.x1)}, {F(c.y1)}, \"{Pachinko.Key(c.reward)}\"]")) + "],\n");
            sb.Append(" \"lane\": [" + string.Join(", ", lane.Select(q => $"[{F(q.x)}, {F(q.y)}]")) + "]\n");
            sb.Append("}\n");
            return sb.ToString();
        }

        // phóng một bi từ chân làn
        public Ball Launch(int mult)
        {
            var (x, y) = lane[0];
            var b = new Ball { id = nextId++, x = x, y = y, mult = mult, alive = true, lane = 0 };
            b.laneV = PickSpeed(out b.target);
            balls.Add(b);
            return b;
        }

        double RandomSpeed() => rng.Range(ForceMin, ForceMax) * ForceStep * U;

        double PickSpeed(out int want)
        {
            want = -1;
            if (odds == null) return RandomSpeed();
            want = PickOutcome();
            if (pool.TryGetValue(want, out var q) && q.Count > 0) return q.Dequeue();
            double v = 0;
            for (int i = 0; i < MaxTries; i++)
            {
                v = RandomSpeed();
                int got = Simulate(v);
                tries++;
                if (got == want) return v;
                if (got < 0) continue;
                if (!pool.TryGetValue(got, out var pq)) pool[got] = pq = new Queue<double>();
                if (pq.Count < PoolCap) pq.Enqueue(v);
            }
            misses++;
            return v;
        }

        // thử trước n đường bi, chỉ khi còn kết quả nào trong bảng chưa có sẵn đủ Reserve đường (gọi rải mỗi khung lúc rảnh, để lúc
        // phóng lấy ngay từ kho, không phải tìm). Trả về true nếu còn thiếu.
        public const int Reserve = 3;
        public bool Warm(int n)
        {
            if (odds == null) return false;
            for (int k = 0; k < n; k++)
            {
                if (!Short()) return false;
                double v = RandomSpeed();
                int got = Simulate(v);
                tries++;
                if (got < 0) continue;
                if (!pool.TryGetValue(got, out var pq)) pool[got] = pq = new Queue<double>();
                if (pq.Count < PoolCap) pq.Enqueue(v);
            }
            return Short();
        }

        bool Short()
        {
            for (int i = 0; i < odds.Length; i++)
                if (odds[i] > 0 && (!pool.TryGetValue(i, out var q) || q.Count < Reserve)) return true;
            return false;
        }

        int PickOutcome()
        {
            double sum = 0;
            foreach (var p in odds) sum += p;
            double r = rng.Next() * sum;
            for (int i = 0; i < odds.Length; i++)
            {
                r -= odds[i];
                if (r < 0) return i;
            }
            return odds.Length - 1;
        }

        // chạy riêng một bi từ chỗ ra làn với tốc v (y như bi thật sau khi rời làn) tới khi rơi; trả về kết quả
        readonly List<PEvent> simEv = new List<PEvent>();
        public int Simulate(double v)
        {
            var b = new Ball { alive = true };
            Exit(b, v);
            const double h = Dt / Sub;
            simEv.Clear();
            while (b.alive)
            {
                Move(b, h, simEv);
                if (simEv.Count > 0)
                {
                    var last = simEv[simEv.Count - 1];
                    if (last.land) return OutcomeOf(last);
                    simEv.Clear();
                }
            }
            return -1;
        }

        // một khung vật lý cố định Dt (bước con Dt / Sub); người gọi tự gom giờ thật thành từng khung
        public List<PEvent> Step()
        {
            var ev = new List<PEvent>();
            const double h = Dt / Sub;
            for (int k = 0; k < Sub; k++)
                foreach (var b in balls)
                {
                    if (!b.alive) continue;
                    if (b.lane >= 0) LaneStep(b, h);
                    else Move(b, h, ev);
                }
            balls.RemoveAll(b => !b.alive);
            return ev;
        }

        // ma sát khi bi chạm vật có ma sát: bớt tốc theo mặt tiếp xúc, tối đa f × xung pháp tuyến (jn) và không quá 1/3 tốc
        // tiếp tuyến (bi tròn đặc lăn được thì ma sát chỉ ăn tới đó)
        static void Rub(Ball b, double nx, double ny, double jn, double f)
        {
            double tx = -ny, ty = nx;
            double vt = b.vx * tx + b.vy * ty;
            double cut = Math.Min(Math.Abs(vt) / 3, f * jn);
            double dv = vt > 0 ? cut : -cut;
            b.vx -= dv * tx;
            b.vy -= dv * ty;
        }

        // bi trên làn (chỉ là đường hình, không va chạm): chạy đều LaneSpeed; hết làn thì ra bàn ở hốc trên phải theo hướng đoạn
        // cuối, tốc bằng tốc phóng
        void LaneStep(Ball b, double h)
        {
            b.lane += LaneSpeed * U * h;
            if (b.lane >= LaneLength)
            {
                Exit(b, b.laneV);
                return;
            }
            int i = 1;
            while (i < laneAt.Count - 1 && laneAt[i] < b.lane) i++;
            double k = (b.lane - laneAt[i - 1]) / (laneAt[i] - laneAt[i - 1]);
            b.x = lane[i - 1].x + (lane[i].x - lane[i - 1].x) * k;
            b.y = lane[i - 1].y + (lane[i].y - lane[i - 1].y) * k;
        }

        // bi rời làn ở hốc trên phải: hướng đoạn cuối của làn, tốc v
        void Exit(Ball b, double v)
        {
            int m = lane.Count - 1;
            double ex = lane[m].x - lane[m - 1].x, ey = lane[m].y - lane[m - 1].y, el = Math.Sqrt(ex * ex + ey * ey);
            b.x = lane[m].x;
            b.y = lane[m].y;
            b.vx = v * ex / el;
            b.vy = v * ey / el;
            b.lane = -1;
            b.age = 0;
        }

        // bi chạm ô chữ nhật (khoảng cách từ tâm bi tới hình chữ nhật nhỏ hơn bán kính)
        static bool Touch(Ball b, double x0, double y0, double x1, double y1)
        {
            double cx = Math.Max(x0, Math.Min(x1, b.x)), cy = Math.Max(y0, Math.Min(y1, b.y));
            double dx = b.x - cx, dy = b.y - cy;
            return dx * dx + dy * dy < BallR * BallR;
        }

        // một bước con của bi đã ra bàn (mỗi bi tính riêng: bi không va bi, nên đường bi chỉ phụ thuộc tốc lúc rời làn)
        void Move(Ball b, double h, List<PEvent> ev)
        {
            const double R = BallR;
            {
                b.age += h;
                b.vy += Gravity * h;
                double damp = 1 / (1 + Drag * h);
                b.vx *= damp;
                b.vy *= damp;
                double sp = Math.Sqrt(b.vx * b.vx + b.vy * b.vy);
                if (sp > VMax)
                {
                    b.vx *= VMax / sp;
                    b.vy *= VMax / sp;
                }
                else if (sp < VMin)
                {
                    if (sp > 1e-9)
                    {
                        b.vx *= VMin / sp;
                        b.vy *= VMin / sp;
                    }
                    else b.vy = VMin;
                }
                b.x += b.vx * h;
                b.y += b.vy * h;
                int gx = Math.Max(0, Math.Min(gw - 1, (int)(b.x / Cell))), gy = Math.Max(0, Math.Min(gh - 1, (int)(b.y / Cell)));
                var cellPegs = gridPegs[gy * gw + gx];
                var cellSegs = gridSegs[gy * gw + gx];
                // đinh, nấm, núm
                foreach (int i in cellPegs)
                {
                    var p = pegs[i];
                    double dx = b.x - p.x, dy = b.y - p.y;
                    double rr = R + p.r;
                    double d2 = dx * dx + dy * dy;
                    if (d2 >= rr * rr || d2 == 0) continue;
                    double d = Math.Sqrt(d2), nx = dx / d, ny = dy / d;
                    b.x = p.x + nx * rr;
                    b.y = p.y + ny * rr;
                    double vn = b.vx * nx + b.vy * ny;
                    if (vn < 0)
                    {
                        double e = -vn > VRest ? p.e : 0;
                        b.vx -= (1 + e) * vn * nx;
                        b.vy -= (1 + e) * vn * ny;
                        if (p.f > 0) Rub(b, nx, ny, (1 + e) * -vn, p.f);
                        if (-vn > 0.5 * U) ev.Add(new PEvent { peg = i, ball = b, speed = -vn });
                    }
                }
                // khung, mái, đáy V, vách ô
                foreach (int si in cellSegs)
                {
                    var sg = segs[si];
                    double ex = sg.x2 - sg.x1, ey = sg.y2 - sg.y1;
                    double len2 = ex * ex + ey * ey;
                    double t = len2 > 0 ? ((b.x - sg.x1) * ex + (b.y - sg.y1) * ey) / len2 : 0;
                    t = Math.Max(0, Math.Min(1, t));
                    double cx = sg.x1 + ex * t, cy = sg.y1 + ey * t;
                    double dx = b.x - cx, dy = b.y - cy;
                    double rr = R + sg.r;
                    double d2 = dx * dx + dy * dy;
                    if (d2 >= rr * rr) continue;
                    double d = Math.Sqrt(d2);
                    double nx, ny;
                    if (d < 1e-9)
                    {
                        // tâm bi nằm đúng trên cạnh: đẩy theo pháp tuyến của đoạn
                        double el = Math.Sqrt(len2);
                        nx = -ey / el;
                        ny = ex / el;
                    }
                    else
                    {
                        nx = dx / d;
                        ny = dy / d;
                    }
                    b.x = cx + nx * rr;
                    b.y = cy + ny * rr;
                    double vn = b.vx * nx + b.vy * ny;
                    if (vn < 0)
                    {
                        double e = -vn > VRest ? sg.e : 0;
                        b.vx -= (1 + e) * vn * nx;
                        b.vy -= (1 + e) * vn * ny;
                        if (sg.f > 0) Rub(b, nx, ny, (1 + e) * -vn, sg.f);
                    }
                }
                // cốc thẻ, rồi ô đáy: chạm cảm biến là vào
                foreach (var c in cups)
                {
                    if (!Touch(b, c.x - c.w / 2, c.y - c.h / 2, c.x + c.w / 2, c.y + c.h / 2)) continue;
                    b.alive = false;
                    ev.Add(new PEvent { land = true, reward = c.reward, slot = -1, cup = true, ball = b });
                    break;
                }
                if (!b.alive) return;
                for (int i = 0; i < slots.Count; i++)
                {
                    var s = slots[i];
                    if (!Touch(b, s.x0, s.y0, s.x1, s.y1)) continue;
                    b.alive = false;
                    ev.Add(new PEvent { land = true, reward = s.reward, slot = i, cup = false, ball = b });
                    break;
                }
                if (!b.alive) return;
                // lọt ra ngoài khung (không nên có) hoặc kẹt quá lâu: tính vào ô gần nhất theo x
                if (b.y > BH || b.x < 0 || b.x > BW || b.age > 30)
                {
                    int best = 0;
                    for (int i = 1; i < slots.Count; i++)
                        if (Math.Abs((slots[i].x0 + slots[i].x1) / 2 - b.x) < Math.Abs((slots[best].x0 + slots[best].x1) / 2 - b.x)) best = i;
                    b.alive = false;
                    ev.Add(new PEvent { land = true, reward = slots[best].reward, slot = best, cup = false, ball = b });
                }
            }
        }
    }

    // ---------- thưởng ----------

    public enum RewardKind { Exp, Balls, Card, Shards, Hero, LegendCopies, Chest, Stones }

    public sealed class Reward
    {
        public RewardKind k;
        public int n;
        public int ups; // số cấp vừa lên (EXP)
        public Progress.CardDrop drop;
        public ShardResult res;
        public string hero;
        public CardSlot slot;
        public SlotKind chest;
    }

    public static class Pachinko
    {
        public static string Key(SlotKind k) =>
            k == SlotKind.Exp5 ? "exp5" : k == SlotKind.Exp10 ? "exp10" : k == SlotKind.Exp15 ? "exp15" : k == SlotKind.Ball ? "ball"
            : k == SlotKind.ChestWood ? "chest_wood" : k == SlotKind.ChestSilver ? "chest_silver" : "chest_gold";

        public static SlotKind FromKey(string s) =>
            s == "exp5" ? SlotKind.Exp5 : s == "exp10" ? SlotKind.Exp10 : s == "exp15" ? SlotKind.Exp15 : s == "ball" ? SlotKind.Ball
            : s == "chest_wood" ? SlotKind.ChestWood : s == "chest_silver" ? SlotKind.ChestSilver : SlotKind.ChestGold;

        public static bool IsChest(SlotKind k) => k == SlotKind.ChestWood || k == SlotKind.ChestSilver || k == SlotKind.ChestGold;
        public static int Exp(SlotKind k) => k == SlotKind.Exp5 ? 5 : k == SlotKind.Exp10 ? 10 : k == SlotKind.Exp15 ? 15 : 0;

        public static string ChestName(SlotKind k) => k == SlotKind.ChestWood ? "Rương Gỗ" : k == SlotKind.ChestSilver ? "Rương Bạc" : "Rương Vàng";

        // ô đáy: thưởng ngay (rương thì đưa vào hàng chờ mở)
        public static Reward SlotReward(SaveData s, BalanceConfig cfg, SlotKind kind, int x)
        {
            int exp = Exp(kind);
            if (exp > 0) return new Reward { k = RewardKind.Exp, n = exp * x, ups = Progress.AddExp(s, exp * x, cfg) };
            if (kind == SlotKind.Ball)
            {
                s.balls += x;
                return new Reward { k = RewardKind.Balls, n = x };
            }
            return new Reward { k = RewardKind.Chest, chest = kind };
        }

        public static List<Reward> OpenChest(SaveData s, GameData d, SlotKind kind, int x, Rng rng) =>
            RollChest(s, d, d.Cfg.Chest(Key(kind)), x, rng);

        // quay một bảng rương (máy bi, rương AFK): một dòng theo trọng số, số lượng × x; thẻ rút riêng từng thẻ theo độ hiếm
        public static List<Reward> RollChest(SaveData s, GameData d, ChestTable table, int x, Rng rng)
        {
            var cfg = d.Cfg;
            var roll = rng.Weighted(table.rolls, r => r.w);
            int n = rng.Int(roll.min, roll.max) * x;
            switch (roll.k)
            {
                case "balls":
                    s.balls += n;
                    return new List<Reward> { new Reward { k = RewardKind.Balls, n = n } };
                case "exp":
                    return new List<Reward> { new Reward { k = RewardKind.Exp, n = n, ups = Progress.AddExp(s, n, cfg) } };
                case "stones":
                    s.potentialStones += n;
                    return new List<Reward> { new Reward { k = RewardKind.Stones, n = n } };
                case "cards":
                {
                    var outL = new List<Reward>();
                    for (int i = 0; i < n; i++)
                    {
                        var r = rng.Weighted(roll.rar, e => e.w).rarity;
                        var drop = Progress.RollCardDrop(s, d, r, rng);
                        if (drop != null)
                        {
                            Progress.GiveCard(s, drop);
                            outL.Add(new Reward { k = RewardKind.Card, drop = drop });
                        }
                    }
                    if (outL.Count > 0) return outL;
                    return new List<Reward> { new Reward { k = RewardKind.Exp, n = 20 * x, ups = Progress.AddExp(s, 20 * x, cfg) } };
                }
                default:
                {
                    var pool = Progress.AfkBossPool(s, d);
                    var cand = pool.Count > 0 ? pool : d.Heroes.Where(h => h.rarity != Rarity.Legend).Select(h => h.id).ToList();
                    return new List<Reward> { new Reward { k = RewardKind.Shards, res = Progress.AddShards(s, d, rng.Pick(cand), n, rng) } };
                }
            }
        }

        // trừ bi khi thả; tới mốc thì chắc chắn ra tướng Huyền thoại lần đầu (đã có tướng thì bản sao thẻ Huyền thoại)
        public static Reward SpendBall(SaveData s, GameData d, int x)
        {
            s.balls -= x;
            s.ballsSpent += x;
            s.stats.dropped++;
            if (!s.legendDone && s.ballsSpent >= d.Cfg.legendMilestone)
            {
                s.legendDone = true;
                string id = d.LegendMilestoneHero;
                if (!s.Hero(id).owned)
                {
                    Progress.UnlockHero(s, id);
                    return new Reward { k = RewardKind.Hero, hero = id };
                }
                var h = d.Hero(id);
                var slot = Progress.Slots.Cast<CardSlot?>().FirstOrDefault(k => d.Card(Progress.CardOf(h, k.Value)).rarity == Rarity.Legend) ?? CardSlot.Ult;
                s.Hero(id).Card(slot).copies += d.Cfg.legendCopies;
                return new Reward { k = RewardKind.LegendCopies, hero = id, slot = slot, n = d.Cfg.legendCopies };
            }
            return null;
        }

        // ---------- mốc quà ----------
        // Sau mốc Huyền thoại, mỗi bi tiêu (theo cược) cộng một nấc vào mốc đang chạy (cfg.gifts, hết thì vòng lại từ đầu).
        // Đủ n thì nhận quà rồi sang mốc kế, phần dư chuyển sang mốc kế. Quà rương trả về để người gọi đưa vào hàng chờ mở
        // (như rương ở ô); bi và EXP cộng ngay.

        public static GiftStep GiftNow(SaveData s, BalanceConfig cfg) => cfg.gifts.Count == 0 ? null : cfg.gifts[s.giftTier % cfg.gifts.Count];

        // mốc thứ i tính từ mốc đang chạy (0 = đang chạy)
        public static GiftStep GiftAt(SaveData s, BalanceConfig cfg, int i) => cfg.gifts.Count == 0 ? null : cfg.gifts[(s.giftTier + i) % cfg.gifts.Count];

        // số bi của lần thả vừa rồi tính vào mốc quà: lần thả vượt mốc Huyền thoại (legend khác null) chỉ tính phần dư
        public static int GiftCredit(SaveData s, BalanceConfig cfg, int x, Reward legend) =>
            legend != null ? Math.Max(0, Math.Min(x, s.ballsSpent - cfg.legendMilestone)) : s.legendDone ? x : 0;

        public static List<Reward> GiftAdd(SaveData s, GameData d, int n)
        {
            var got = new List<Reward>();
            var cfg = d.Cfg;
            if (n <= 0 || cfg.gifts.Count == 0) return got;
            s.gift += n;
            for (var g = GiftNow(s, cfg); g != null && g.n > 0 && s.gift >= g.n; g = GiftNow(s, cfg))
            {
                s.gift -= g.n;
                s.giftTier++;
                got.Add(GiftGive(s, cfg, g));
            }
            return got;
        }

        static Reward GiftGive(SaveData s, BalanceConfig cfg, GiftStep g)
        {
            switch (g.k)
            {
                case "balls":
                    s.balls += g.v;
                    return new Reward { k = RewardKind.Balls, n = g.v };
                case "exp":
                    return new Reward { k = RewardKind.Exp, n = g.v, ups = Progress.AddExp(s, g.v, cfg) };
                default:
                    return new Reward { k = RewardKind.Chest, chest = FromKey(g.k) };
            }
        }

        // ---------- vòng nấm ----------
        // Mỗi nấm lớn có một vòng tiến độ (cfg.rings[i], i = 0 nấm trái, 1 nấm phải): mỗi lần bi chạm cộng mult nấc (cược ×N tính
        // N), đủ n nấc thì ra quà, phần dư giữ cho vòng sau. Rương trả về để người gọi đưa vào hàng chờ mở; bi, EXP cộng ngay.
        public static List<Reward> RingHit(SaveData s, BalanceConfig cfg, int ring, int mult)
        {
            var got = new List<Reward>();
            if (ring < 0 || ring >= cfg.rings.Count || ring >= s.rings.Length) return got;
            var g = cfg.rings[ring];
            if (g.n <= 0) return got;
            s.rings[ring] += Math.Max(1, mult);
            while (s.rings[ring] >= g.n)
            {
                s.rings[ring] -= g.n;
                got.Add(GiftGive(s, cfg, g));
            }
            return got;
        }

        // "Rương Bạc", "+10 bi", "+120 XP"
        public static string GiftName(GiftStep g) =>
            g.k == "balls" ? $"+{g.v} bi" : g.k == "exp" ? $"+{g.v} XP" : ChestName(FromKey(g.k));
    }
}
