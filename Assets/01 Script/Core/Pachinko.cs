// Máy bi: vật lý thuần (đinh, nấm bật, cốc hứng, ô đáy) và bảng thưởng, chép Web/src/core/pachinko.ts.
// Vật lý tự viết (không dùng Physics2D) để giữ tỉ lệ đã đo, có hạt giống, chạy được trong EditMode test.
// Math.hypot chép đúng cách tính của V8 (tổng Kahan sau khi chia cho giá trị lớn nhất) để số khớp bản web.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum SlotKind { Exp5, Exp10, Exp15, Ball, ChestWood, ChestSilver, ChestGold }
    public enum PegKind { Peg, Bumper, Post }

    public struct Peg
    {
        public double x, y, r;
        public PegKind kind;
    }

    public struct Seg
    {
        public double x1, y1, x2, y2;
    }

    public struct Cup
    {
        public double x, y, r;
        public SlotKind reward;
    }

    public struct Slot
    {
        public double x0, x1;
        public SlotKind reward;
    }

    public sealed class Ball
    {
        public int id;
        public double x, y, vx, vy;
        public int mult;
        public bool alive;
        public double age;
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
        public const double BW = 460, BH = 680, BallR = 9, DropY = 46;
        public const double Left = 14, Right = BW - 14, SlotTop = 572, Floor = BH - 30;
        public const double Swing = 150; // máng thả đung đưa quanh giữa, biên độ này
        public static readonly SlotKind[] SlotLayout =
        {
            SlotKind.ChestWood, SlotKind.Exp15, SlotKind.Exp5, SlotKind.Ball, SlotKind.Exp10, SlotKind.Ball, SlotKind.Exp5, SlotKind.Exp15, SlotKind.ChestWood,
        };
        // ô mép (rương gỗ) hẹp, ô giữa rộng
        public static readonly double[] SlotW = { 22, 50, 66, 30, 96, 30, 66, 50, 22 };

        public readonly List<Peg> pegs = new List<Peg>();
        public readonly List<Cup> cups = new List<Cup>();
        public readonly List<Slot> slots = new List<Slot>();
        public readonly List<Seg> segs = new List<Seg>();
        public List<Ball> balls = new List<Ball>();
        public Rng rng;
        int nextId = 1;
        public double gravity = 1150;

        public readonly double[] slotW; // độ rộng 9 ô đáy (mặc định SlotW; cửa sổ Cân bằng thử độ rộng khác)

        public Board(uint seed = 1, double[] widths = null)
        {
            rng = new Rng(seed);
            slotW = widths ?? SlotW;
            Build();
        }

        void Build()
        {
            for (int i = 0; i < 10; i++)
            {
                double y = 120 + i * 42;
                bool odd = i % 2 == 1;
                int n = odd ? 8 : 9;
                // khe giữa tường và đinh mép phải rộng hơn bi (18), không thì bi kẹt
                const double gap = 46.25;
                for (int j = 0; j < n; j++)
                {
                    double x = (odd ? 45 + gap / 2 : 45) + j * gap;
                    if (i == 3 && (j == 1 || j == 6) || i == 6 && j == 4)
                    {
                        pegs.Add(new Peg { x = x, y = y, r = 15, kind = PegKind.Bumper });
                        continue;
                    }
                    if (i == 7 && (j == 1 || j == 6))
                    {
                        cups.Add(new Cup { x = x, y = y + 6, r = 3.5, reward = SlotKind.ChestSilver });
                        continue;
                    }
                    if (i == 4 && j == 4)
                    {
                        cups.Add(new Cup { x = x, y = y + 6, r = 3, reward = SlotKind.ChestGold });
                        continue;
                    }
                    pegs.Add(new Peg { x = x, y = y, r = 5, kind = PegKind.Peg });
                }
                // u lồi trên tường ở hàng lẻ: bi trượt dọc tường bị đẩy vào trong
                if (odd)
                {
                    pegs.Add(new Peg { x = Left, y = y, r = 10, kind = PegKind.Post });
                    pegs.Add(new Peg { x = Right, y = y, r = 10, kind = PegKind.Post });
                }
            }
            var xs = new List<double> { Left };
            foreach (var w in slotW) xs.Add(xs[xs.Count - 1] + w);
            for (int i = 0; i < SlotLayout.Length; i++) slots.Add(new Slot { x0 = xs[i], x1 = xs[i + 1], reward = SlotLayout[i] });
            segs.Add(new Seg { x1 = Left, y1 = 0, x2 = Left, y2 = BH });
            segs.Add(new Seg { x1 = Right, y1 = 0, x2 = Right, y2 = BH });
            // vai nghiêng hai bên trên cùng: bi thả sát mép trượt vào giữa
            segs.Add(new Seg { x1 = Left, y1 = 70, x2 = Left + 40, y2 = 104 });
            segs.Add(new Seg { x1 = Right, y1 = 70, x2 = Right - 40, y2 = 104 });
            for (int i = 1; i < SlotLayout.Length; i++)
            {
                double x = xs[i];
                segs.Add(new Seg { x1 = x, y1 = SlotTop, x2 = x, y2 = BH });
                pegs.Add(new Peg { x = x, y = SlotTop, r = 3.5, kind = PegKind.Post });
            }
        }

        public Ball Drop(double x, int mult)
        {
            var b = new Ball
            {
                id = nextId++, x = Math.Max(Left + BallR + 2, Math.Min(Right - BallR - 2, x)), y = DropY,
                vx = rng.Range(-20, 20), vy = 60, mult = mult, alive = true,
            };
            balls.Add(b);
            return b;
        }

        public List<PEvent> Step(double dt)
        {
            var ev = new List<PEvent>();
            const int sub = 4;
            double h = dt / sub;
            for (int k = 0; k < sub; k++) Substep(h, ev);
            balls.RemoveAll(b => !b.alive);
            return ev;
        }

        // Math.hypot(x, y) của V8
        public static double Hypot(double a, double b)
        {
            a = Math.Abs(a);
            b = Math.Abs(b);
            double max = Math.Max(a, b);
            if (double.IsInfinity(max)) return double.PositiveInfinity;
            if (double.IsNaN(a) || double.IsNaN(b)) return double.NaN;
            if (max == 0) return 0;
            // hai vòng của V8 viết thẳng ra (không cấp phát mảng: hàm này chạy mỗi bi mỗi bước con)
            double sum = 0, comp = 0;
            double n = a / max;
            double summand = n * n - comp;
            double pre = sum + summand;
            comp = pre - sum - summand;
            sum = pre;
            n = b / max;
            summand = n * n - comp;
            pre = sum + summand;
            sum = pre;
            return Math.Sqrt(sum) * max;
        }

        void Substep(double h, List<PEvent> ev)
        {
            const double R = BallR;
            foreach (var b in balls)
            {
                if (!b.alive) continue;
                b.age += h;
                b.vy += gravity * h;
                double sp = Hypot(b.vx, b.vy);
                if (sp > 950)
                {
                    b.vx *= 950 / sp;
                    b.vy *= 950 / sp;
                }
                b.x += b.vx * h;
                b.y += b.vy * h;
                // đinh và nấm
                for (int i = 0; i < pegs.Count; i++)
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
                        double e = p.kind == PegKind.Bumper ? 0.75 : 0.5;
                        b.vx -= (1 + e) * vn * nx;
                        b.vy -= (1 + e) * vn * ny;
                        // một chút lệch ngẫu nhiên, để không lần nào giống lần nào
                        double j = rng.Range(-0.18, 0.18);
                        double c = Math.Cos(j), s = Math.Sin(j);
                        double vx = b.vx * c - b.vy * s, vy = b.vx * s + b.vy * c;
                        b.vx = vx * 0.985;
                        b.vy = vy * 0.985;
                        if (-vn > 60) ev.Add(new PEvent { peg = i, ball = b, speed = -vn });
                    }
                }
                // tường, vách ô
                foreach (var sg in segs)
                {
                    double ex = sg.x2 - sg.x1, ey = sg.y2 - sg.y1;
                    double len2 = ex * ex + ey * ey;
                    double t = ((b.x - sg.x1) * ex + (b.y - sg.y1) * ey) / len2;
                    t = Math.Max(0, Math.Min(1, t));
                    double cx = sg.x1 + ex * t, cy = sg.y1 + ey * t;
                    double dx = b.x - cx, dy = b.y - cy;
                    double d2 = dx * dx + dy * dy;
                    if (d2 >= R * R) continue;
                    double d = Math.Sqrt(d2);
                    if (d == 0) d = 0.001;
                    double nx = dx / d, ny = dy / d;
                    b.x = cx + nx * R;
                    b.y = cy + ny * R;
                    double vn = b.vx * nx + b.vy * ny;
                    if (vn < 0)
                    {
                        b.vx -= 1.4 * vn * nx;
                        b.vy -= 1.4 * vn * ny;
                    }
                }
                // cốc hứng giữa máy
                foreach (var c in cups)
                {
                    double dx = b.x - c.x, dy = b.y - c.y;
                    if (b.vy > 0 && dx * dx + dy * dy < c.r * c.r)
                    {
                        b.alive = false;
                        ev.Add(new PEvent { land = true, reward = c.reward, slot = -1, cup = true, ball = b });
                        break;
                    }
                }
                if (!b.alive) continue;
                // chạm đáy
                if (b.y > Floor)
                {
                    int i = slots.FindIndex(s => b.x >= s.x0 && b.x < s.x1);
                    int slot = i < 0 ? (b.x < BW / 2 ? 0 : slots.Count - 1) : i;
                    b.alive = false;
                    ev.Add(new PEvent { land = true, reward = slots[slot].reward, slot = slot, cup = false, ball = b });
                }
                // kẹt quá lâu thì tính rơi thẳng
                if (b.age > 14 && b.alive) b.vy += 400;
            }
            // bi va bi
            var bs = balls;
            for (int i = 0; i < bs.Count; i++)
            {
                var a = bs[i];
                if (!a.alive) continue;
                for (int j = i + 1; j < bs.Count; j++)
                {
                    var c = bs[j];
                    if (!c.alive) continue;
                    double dx = c.x - a.x, dy = c.y - a.y;
                    double d2 = dx * dx + dy * dy;
                    if (d2 >= 4 * R * R || d2 == 0) continue;
                    double d = Math.Sqrt(d2), nx = dx / d, ny = dy / d;
                    double push = (2 * R - d) / 2;
                    a.x -= nx * push;
                    a.y -= ny * push;
                    c.x += nx * push;
                    c.y += ny * push;
                    double rv = (c.vx - a.vx) * nx + (c.vy - a.vy) * ny;
                    if (rv < 0)
                    {
                        double imp = -(1 + 0.6) * rv / 2;
                        a.vx -= imp * nx;
                        a.vy -= imp * ny;
                        c.vx += imp * nx;
                        c.vy += imp * ny;
                    }
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
    }
}
