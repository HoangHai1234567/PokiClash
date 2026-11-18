// Nhà (GD_Claude/21_Nha_Home.md, 2026-11-18), thay Trang trại. Đảo lưới thoi 48 x 48 ô (isometric 2:1 như Clash of Critters), chia
// 6 x 6 ô rừng 8 x 8 ô; khoảnh đầu 2 x 2 ô rừng đã dọn. Người chơi đặt công trình tự do trên ô đã mở, dọn ô rừng kề đất đã mở theo cấp
// Nhà chính và cấp người chơi, giao tướng vào công trình làm ra đồ (luật sức làm, nghỉ, năng suất lấy từ Trang trại: Farm.Hours,
// Farm.RestMin, farm.rarityPower / starStep / match / capHours / boostMult), đặt trang trí lấy điểm đẹp.
// - Đầu ra: bi (ruộng, vườn), gỗ (xưởng gỗ), quặng và ít đá tiến hóa (mỏ), câu cá (bi, thẻ, cúp), đá tiềm năng (lò rèn, ăn quặng trong
//   kho), bánh (bếp: cho tướng đang nghỉ ăn thì hết nghỉ ngay).
// - Bi không phình: số tướng ở công trình ra bi (ruộng, vườn, ao) theo đường chỗ của Trang trại cũ (Farm.SpotsOpen); tổng chỗ tướng theo
//   cấp Nhà chính.
// - Xây, nâng cấp, dọn rừng tốn thời gian và một đội thợ; xong thì tự xong ở lần tính kế. Trang trí đặt ngay.
// - Đồng hồ theo đoạn như Trang trại: giờ máy lùi thì bỏ qua đoạn đó.
// - Bản lưu cũ: lần đầu mở Nhà (Of) gộp Trang trại sang (bi tích về túi, tướng đang làm sang công trình cùng việc, nghỉ giữ nguyên) và
//   đặt Cây bi đã mở vào nhà; Trees vẫn tính bi của cây.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class HomeSlot
    {
        public string hero; // null = trống
        public double energy; // giờ làm còn lại của ca
        public double stock; // đồ tích (số thực)
    }

    public sealed class HomeBuilding
    {
        public int id;
        public string def;
        public int gx, gy; // ô góc trên của chân thoi (gx đi xuống phải, gy đi xuống trái trên màn)
        public int level = 1;
        public bool flip; // lật ngang (chỉ hình)
        public int job; // 0 không, 1 đang xây, 2 đang nâng cấp
        public double until; // xong việc lúc (ms)
        public double acc; // Mỏ: phần lẻ đá tiến hóa
        public int tree = -1; // Cây bi thứ mấy (chỉ số trong TreeState.stock)
        public List<HomeSlot> slots = new List<HomeSlot>();
    }

    public sealed class HomeState
    {
        public double lastTick, boostUntil;
        public int nextId = 1;
        public double wood, ore;
        public int bread;
        public uint seed = 1; // câu cá
        public int beautyGifts; // số mốc điểm đẹp đã nhận
        public List<int> lots = new List<int>(); // ô rừng đã mở (i * 6 + j)
        public Dictionary<int, double> clearing = new Dictionary<int, double>(); // ô rừng đang dọn → xong lúc (ms)
        public List<HomeBuilding> buildings = new List<HomeBuilding>();
        public Dictionary<string, double> rest = new Dictionary<string, double>(); // tướng → hết nghỉ lúc (ms)
        public Dictionary<string, int> bag = new Dictionary<string, int>(); // trang trí đang cất
        public Dictionary<int, string> tiles = new Dictionary<int, string>(); // ô lát (tx * cạnh + ty) → loại; không có = cỏ
        public List<int> cleared = new List<int>(); // ô rừng vừa dọn xong, màn Nhà chưa báo thưởng (không lưu)
    }

    public enum HomeErr
    {
        Ok, NotFound, OutOfMap, Locked, Blocked, Overlap, NeedOre, NeedStream, HomeLevel, PlayerLevel, Count, Cost, Builder, Busy,
        MaxLevel, NotAdjacent, Slot, HeroBusy, TotalSlots, BallSlots,
    }

    public sealed class HomeYield
    {
        public int balls, wood, ore, evo, stones, bread;
        public List<Reward> other = new List<Reward>(); // câu cá: thẻ, kinh nghiệm
        public List<string> deco = new List<string>(); // câu cá: cúp
        public bool Any => balls + wood + ore + evo + stones + bread > 0 || other.Count > 0 || deco.Count > 0;
    }

    public static class Home
    {
        const double H = 3600000, M = 60000;

        // ---------- tra cứu ----------

        public static bool Open(SaveData s, BalanceConfig cfg) => Farm.Open(s, cfg);
        public static HomeBuildingDef Def(BalanceConfig cfg, string id) => cfg.home.Def(id);
        public static int LotsPerSide(HomeConfig c) => c.grid / c.lot;
        public static int LotIndex(HomeConfig c, int i, int j) => i * LotsPerSide(c) + j;
        public static (int i, int j) LotIJ(HomeConfig c, int lot) => (lot / LotsPerSide(c), lot % LotsPerSide(c));
        public static int LotOfCell(HomeConfig c, int gx, int gy) => LotIndex(c, gx / c.lot, gy / c.lot);
        public static bool InMap(HomeConfig c, int gx, int gy) => gx >= 0 && gy >= 0 && gx < c.grid && gy < c.grid;
        public static string LotKind(HomeConfig c, int lot)
        {
            var (i, j) = LotIJ(c, lot);
            return c.lots.Find(l => l.i == i && l.j == j)?.kind ?? "forest";
        }

        // vòng tính từ khoảnh đầu: khoảng cách Chebyshev nhỏ nhất tới một ô rừng của khoảnh đầu (0 là khoảnh đầu)
        public static int Ring(HomeConfig c, int lot)
        {
            var (i, j) = LotIJ(c, lot);
            return c.startLots.Count == 0 ? 0 : c.startLots.Min(s => Math.Max(Math.Abs(s.i - i), Math.Abs(s.j - j)));
        }

        public static bool IsDeco(HomeBuildingDef df) => df.kind == "deco" || df.kind == "road";
        public static bool IsBallOut(HomeBuildingDef df) => df.kind == "prod" && (df.output == "balls" || df.output == "fish");
        public static HomeBLevel Lv(HomeBuildingDef df, int level) =>
            df.levels.Count == 0 ? null : df.levels[Math.Max(0, Math.Min(df.levels.Count - 1, level - 1))];
        public static int MaxLevel(BalanceConfig cfg, HomeBuildingDef df) => df.kind == "main" ? cfg.home.levels.Count : df.levels.Count;
        public static int SlotsOf(HomeBuildingDef df, int level) => df.kind == "prod" ? Lv(df, level)?.slots ?? 0 : 0;

        public static HomeBuilding Find(HomeState h, int id) => h.buildings.Find(b => b.id == id);
        public static HomeBuilding Main(HomeState h) => h.buildings.Find(b => b.def == "main");
        public static int Level(HomeState h) => Main(h)?.level ?? 1;
        public static HomeLevel HomeLv(HomeConfig c, int level) => c.levels[Math.Max(0, Math.Min(c.levels.Count - 1, level - 1))];
        public static int Builders(HomeState h, HomeConfig c) => HomeLv(c, Level(h)).builders;
        public static int Busy(HomeState h) => h.buildings.Count(b => b.job != 0) + h.clearing.Count;
        public static int MaxCount(HomeBuildingDef df, int homeLevel) =>
            IsDeco(df) ? int.MaxValue : df.count == null || df.count.Length == 0 ? 1 : df.count[Math.Max(0, Math.Min(df.count.Length - 1, homeLevel - 1))];
        public static int CountOf(HomeState h, string def) => h.buildings.Count(b => b.def == def);
        public static int MaxLots(HomeConfig c, int homeLevel) =>
            c.maxLots.Length == 0 ? int.MaxValue : c.maxLots[Math.Max(0, Math.Min(c.maxLots.Length - 1, homeLevel - 1))];

        public static double WoodCap(HomeState h, BalanceConfig cfg) =>
            cfg.home.woodCap + h.buildings.Where(b => b.def == "storage" && b.job != 1).Sum(b => Lv(Def(cfg, b.def), b.level)?.cap ?? 0);
        public static double OreCap(HomeState h, BalanceConfig cfg) =>
            cfg.home.oreCap + h.buildings.Where(b => b.def == "storage" && b.job != 1).Sum(b => Lv(Def(cfg, b.def), b.level)?.capOre ?? 0);

        public static int TotalSlots(HomeState h, HomeConfig c) => HomeLv(c, Level(h)).slots;
        public static int BallSlots(SaveData s, BalanceConfig cfg) => Farm.SpotsOpen(cfg, s.level);
        public static int UsedSlots(HomeState h) => h.buildings.Sum(b => b.slots.Count(sl => sl.hero != null));
        public static int UsedBallSlots(HomeState h, BalanceConfig cfg) =>
            h.buildings.Where(b => IsBallOut(Def(cfg, b.def))).Sum(b => b.slots.Count(sl => sl.hero != null));

        // ---------- tạo, gộp bản cũ ----------

        public static HomeState Fresh(GameData d, double now)
        {
            var c = d.Cfg.home;
            var h = new HomeState { lastTick = now };
            foreach (var l in c.startLots) h.lots.Add(LotIndex(c, l.i, l.j));
            foreach (var p in c.layout) Add(d.Cfg, h, p.b, p.gx, p.gy);
            foreach (var t in c.startTiles) h.tiles[TileIndex(c, t.gx, t.gy)] = t.b;
            return h;
        }

        public static HomeState Of(SaveData s, GameData d, double now)
        {
            if (s.home != null) return s.home;
            s.home = Fresh(d, now);
            FromFarm(s, d, now);
            SyncTrees(s, d);
            return s.home;
        }

        static HomeBuilding Add(BalanceConfig cfg, HomeState h, string def, int gx, int gy)
        {
            var b = new HomeBuilding { id = h.nextId++, def = def, gx = gx, gy = gy };
            Fit(cfg, b);
            h.buildings.Add(b);
            return b;
        }

        // đủ số ô tướng theo cấp (lên cấp thì thêm ô trống)
        static void Fit(BalanceConfig cfg, HomeBuilding b)
        {
            int n = SlotsOf(Def(cfg, b.def), b.level);
            while (b.slots.Count < n) b.slots.Add(new HomeSlot());
        }

        // khu của Trang trại cũ → công trình cùng việc (Farm spots kind)
        public static readonly Dictionary<string, string> FarmKind = new Dictionary<string, string>
        {
            ["duck"] = "pond", ["veg"] = "field", ["orchard"] = "orchard", ["bakery"] = "kitchen", ["smithy"] = "forge",
        };

        static void FromFarm(SaveData s, GameData d, double now)
        {
            var f = s.farm;
            if (f == null) return;
            Farm.Harvest(s, d, now); // bi đang tích của trang trại về túi
            var h = s.home;
            for (int i = 0; i < f.spots.Count && i < d.Cfg.farm.spots.Count; i++)
            {
                var sp = f.spots[i];
                if (sp.hero == null) continue;
                string def = FarmKind.TryGetValue(d.Cfg.farm.spots[i].kind ?? "", out var k) ? k : "field";
                var b = h.buildings.FirstOrDefault(x => x.def == def && x.slots.Any(sl => sl.hero == null));
                if (b == null)
                {
                    var pos = FindSpot(s, d, def);
                    if (pos == null) continue;
                    b = Add(d.Cfg, h, def, pos.Value.gx, pos.Value.gy); // công trình có sẵn từ Trang trại: không tính giá, cấp Nhà, số tối đa
                }
                var slot = b.slots.First(sl => sl.hero == null);
                slot.hero = sp.hero;
                slot.energy = sp.energy;
            }
            foreach (var kv in f.rest) h.rest[kv.Key] = kv.Value;
            h.boostUntil = f.boostUntil;
            s.farm = null;
        }

        // Cây bi đã mở (Trees.Open) mà chưa có chỗ trong nhà: đặt vào ô trống gần Nhà chính
        public static void SyncTrees(SaveData s, GameData d)
        {
            var h = s.home;
            int n = Trees.Open(s, d.Cfg);
            for (int i = 0; i < n; i++)
            {
                if (h.buildings.Any(b => b.def == "tree" && b.tree == i)) continue;
                var pos = FindSpot(s, d, "tree");
                if (pos == null) break;
                Add(d.Cfg, h, "tree", pos.Value.gx, pos.Value.gy).tree = i;
            }
        }

        // ---------- ô lưới, đặt chỗ ----------

        public static HomeFeature FeatureAt(HomeConfig c, int gx, int gy) => c.features.Find(f => f.Has(gx, gy) && f.kind != "fertile");
        static bool Blocks(HomeFeature f) => f != null && (f.kind == "lake" || f.kind == "stream" || f.kind == "rock");
        public static bool LotOpenAt(HomeState h, HomeConfig c, int gx, int gy) => h.lots.Contains(LotOfCell(c, gx, gy));

        public static HomeBuilding At(HomeState h, BalanceConfig cfg, int gx, int gy, int ignore = -1) =>
            h.buildings.Find(b => b.id != ignore && Covers(cfg, b, gx, gy));

        static bool Covers(BalanceConfig cfg, HomeBuilding b, int gx, int gy)
        {
            int n = Def(cfg, b.def).size;
            return gx >= b.gx && gx < b.gx + n && gy >= b.gy && gy < b.gy + n;
        }

        // đặt công trình def với ô góc (gx, gy) được không (ignore: công trình đang dời)
        public static HomeErr CanPlace(SaveData s, GameData d, string def, int gx, int gy, int ignore = -1)
        {
            var c = d.Cfg.home;
            var h = s.home;
            var df = Def(d.Cfg, def);
            if (df == null) return HomeErr.NotFound;
            int n = df.size;
            if (gx < 0 || gy < 0 || gx + n > c.grid || gy + n > c.grid) return HomeErr.OutOfMap;
            for (int x = gx; x < gx + n; x++)
            for (int y = gy; y < gy + n; y++)
            {
                if (!LotOpenAt(h, c, x, y)) return HomeErr.Locked;
                var f = FeatureAt(c, x, y);
                if (Blocks(f)) return HomeErr.Blocked;
                bool ore = f != null && f.kind == "ore";
                if (df.need == "ore" && !ore) return HomeErr.NeedOre;
                if (df.need != "ore" && ore) return HomeErr.Blocked; // mạch quặng để dành cho Mỏ
                if (TileBlocks(h, c, x, y)) return HomeErr.Blocked; // ô lát nước
                if (At(h, d.Cfg, x, y, ignore) != null) return HomeErr.Overlap;
            }
            if (df.need == "stream" && !NextToStream(c, gx, gy, n)) return HomeErr.NeedStream;
            return HomeErr.Ok;
        }

        static bool NextToStream(HomeConfig c, int gx, int gy, int n)
        {
            for (int x = gx - 1; x <= gx + n; x++)
            for (int y = gy - 1; y <= gy + n; y++)
            {
                bool inside = x >= gx && x < gx + n && y >= gy && y < gy + n;
                if (!inside && FeatureAt(c, x, y)?.kind == "stream") return true;
            }
            return false;
        }

        // ô trống gần Nhà chính đặt được def (vòng vuông nở dần)
        public static (int gx, int gy)? FindSpot(SaveData s, GameData d, string def, int ignore = -1)
        {
            var c = d.Cfg.home;
            var m = Main(s.home);
            int cx = m != null ? m.gx + Def(d.Cfg, "main").size / 2 : c.grid / 2;
            int cy = m != null ? m.gy + Def(d.Cfg, "main").size / 2 : c.grid / 2;
            for (int r = 0; r < c.grid; r++)
            for (int x = cx - r; x <= cx + r; x++)
            for (int y = cy - r; y <= cy + r; y++)
            {
                if (Math.Max(Math.Abs(x - cx), Math.Abs(y - cy)) != r) continue;
                if (CanPlace(s, d, def, x, y, ignore) == HomeErr.Ok) return (x, y);
            }
            return null;
        }

        // ---------- ô lát: đất, cát, đường đá, nước (học Clash of Critters) ----------
        // Một ô lát = tile x tile ô lưới, thẳng hàng với lưới (tx = gx / tile). Lát trên ô rừng đã mở, không lát lên hồ, suối, mạch quặng,
        // không lát dưới công trình, trang trí. Nước chặn xây. Xoá về cỏ thì không hoàn giá. Mép ô do lớp vẽ tự dựng theo TileMask.

        public static int TilesPerSide(HomeConfig c) => c.grid / Math.Max(1, c.tile);
        public static int TileIndex(HomeConfig c, int tx, int ty) => tx * TilesPerSide(c) + ty;

        public static string TileAt(HomeState h, HomeConfig c, int tx, int ty)
        {
            int n = TilesPerSide(c);
            if (tx < 0 || ty < 0 || tx >= n || ty >= n) return null;
            return h.tiles.TryGetValue(TileIndex(c, tx, ty), out var t) ? t : null;
        }

        static bool TileBlocks(HomeState h, HomeConfig c, int gx, int gy)
        {
            var id = TileAt(h, c, gx / c.tile, gy / c.tile);
            return id != null && (c.Tile(id)?.block ?? false);
        }

        // id null hoặc "grass": xoá về cỏ
        public static HomeErr CanPaint(SaveData s, GameData d, int tx, int ty, string id)
        {
            var c = d.Cfg.home;
            var h = s.home;
            int n = TilesPerSide(c);
            if (tx < 0 || ty < 0 || tx >= n || ty >= n) return HomeErr.OutOfMap;
            bool erase = id == null || id == "grass";
            var def = erase ? null : c.Tile(id);
            if (!erase && def == null) return HomeErr.NotFound;
            if (TileAt(h, c, tx, ty) == (erase ? null : id)) return HomeErr.Busy; // đã là loại này
            for (int x = tx * c.tile; x < (tx + 1) * c.tile; x++)
            for (int y = ty * c.tile; y < (ty + 1) * c.tile; y++)
            {
                if (!LotOpenAt(h, c, x, y)) return HomeErr.Locked;
                var f = FeatureAt(c, x, y);
                if (f != null) return HomeErr.Blocked;
                if (At(h, d.Cfg, x, y) != null) return HomeErr.Overlap;
            }
            // đổi ô không mất tài nguyên (như Clash of Critters, người dùng dặn 2026-11-18): giá ô cũ được hoàn khi lát đè hoặc xoá
            var old = c.Tile(TileAt(h, c, tx, ty) ?? "");
            if (!erase && (h.wood + (old?.wood ?? 0) < def.wood || h.ore + (old?.ore ?? 0) < def.ore)) return HomeErr.Cost;
            return HomeErr.Ok;
        }

        // lát ô: hoàn giá ô cũ (nếu có) rồi trả giá ô mới; xoá về cỏ thì hoàn đủ
        public static HomeErr Paint(SaveData s, GameData d, int tx, int ty, string id)
        {
            var e = CanPaint(s, d, tx, ty, id);
            if (e != HomeErr.Ok) return e;
            var c = d.Cfg.home;
            var h = s.home;
            int k = TileIndex(c, tx, ty);
            var old = h.tiles.TryGetValue(k, out var oid) ? c.Tile(oid) : null;
            if (old != null)
            {
                h.wood += old.wood;
                h.ore += old.ore;
            }
            if (id == null || id == "grass")
            {
                h.tiles.Remove(k);
                return HomeErr.Ok;
            }
            var def = c.Tile(id);
            Pay(s, def.wood, def.ore, 0);
            h.tiles[k] = id;
            return HomeErr.Ok;
        }

        // 8 bit ô hàng xóm cùng loại (để vẽ mép): bit 0..3 = +tx, +ty, -tx, -ty (cạnh); bit 4..7 = (+tx,+ty), (-tx,+ty), (-tx,-ty), (+tx,-ty)
        // (góc). Trên màn: +tx là xuống phải, +ty là xuống trái (theo lưới thoi).
        public static readonly (int dx, int dy)[] Around = { (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1) };

        public static int TileMask(HomeState h, HomeConfig c, int tx, int ty)
        {
            var id = TileAt(h, c, tx, ty);
            if (id == null) return 0;
            int m = 0;
            for (int k = 0; k < Around.Length; k++)
                if (TileAt(h, c, tx + Around[k].dx, ty + Around[k].dy) == id) m |= 1 << k;
            return m;
        }

        // ---------- xây, dời, cất, nâng cấp ----------

        static bool Afford(SaveData s, int wood, int ore, int balls) => s.home.wood >= wood && s.home.ore >= ore && s.balls >= balls;

        static void Pay(SaveData s, int wood, int ore, int balls)
        {
            s.home.wood -= wood;
            s.home.ore -= ore;
            s.balls -= balls;
        }

        // giá xây mới: công trình lấy cấp 1, trang trí lấy giá riêng
        public static (int wood, int ore, int balls, double minutes) BuildCost(HomeBuildingDef df)
        {
            if (IsDeco(df)) return (df.wood, df.ore, df.balls, 0);
            var l = Lv(df, 1);
            return l == null ? (0, 0, 0, 0) : (l.wood, l.ore, 0, l.minutes);
        }

        public static HomeErr CanBuild(SaveData s, GameData d, string def)
        {
            var h = s.home;
            var df = Def(d.Cfg, def);
            if (df == null || df.kind == "main" || df.kind == "tree") return HomeErr.NotFound;
            bool fromBag = h.bag.TryGetValue(def, out var nb) && nb > 0;
            if (IsDeco(df))
            {
                if (df.reward && !fromBag) return HomeErr.Locked;
            }
            else
            {
                if (Level(h) < df.home) return HomeErr.HomeLevel;
                if (CountOf(h, def) >= MaxCount(df, Level(h))) return HomeErr.Count;
            }
            var (w, o, bl, min) = BuildCost(df);
            if (!fromBag && !Afford(s, w, o, bl)) return HomeErr.Cost;
            if (min > 0 && Busy(h) >= Builders(h, d.Cfg.home)) return HomeErr.Builder;
            return HomeErr.Ok;
        }

        public static HomeErr Build(SaveData s, GameData d, double now, string def, int gx, int gy) => Build(s, d, now, def, gx, gy, out _);

        public static HomeErr Build(SaveData s, GameData d, double now, string def, int gx, int gy, out HomeBuilding built)
        {
            built = null;
            Tick(s, d, now);
            var h = s.home;
            var e = CanBuild(s, d, def);
            if (e != HomeErr.Ok) return e;
            e = CanPlace(s, d, def, gx, gy);
            if (e != HomeErr.Ok) return e;
            var df = Def(d.Cfg, def);
            if (h.bag.TryGetValue(def, out var nb) && nb > 0)
            {
                if (nb == 1) h.bag.Remove(def);
                else h.bag[def] = nb - 1;
            }
            else
            {
                var (w, o, bl, _) = BuildCost(df);
                Pay(s, w, o, bl);
            }
            built = Add(d.Cfg, h, def, gx, gy);
            double min = BuildCost(df).minutes;
            if (min > 0)
            {
                built.job = 1;
                built.until = now + min * M;
            }
            return HomeErr.Ok;
        }

        public static HomeErr Move(SaveData s, GameData d, int id, int gx, int gy)
        {
            var b = Find(s.home, id);
            if (b == null) return HomeErr.NotFound;
            var e = CanPlace(s, d, b.def, gx, gy, b.id);
            if (e != HomeErr.Ok) return e;
            b.gx = gx;
            b.gy = gy;
            return HomeErr.Ok;
        }

        // cất trang trí, đường vào túi (công trình không cất)
        public static bool Store(SaveData s, GameData d, int id)
        {
            var h = s.home;
            var b = Find(h, id);
            if (b == null || !IsDeco(Def(d.Cfg, b.def))) return false;
            h.buildings.Remove(b);
            Bag(h, b.def, 1);
            return true;
        }

        public static void Bag(HomeState h, string def, int n) => h.bag[def] = (h.bag.TryGetValue(def, out var k) ? k : 0) + n;

        // giá và thời gian lên cấp sau; null nếu đã tối đa
        public static (int wood, int ore, double minutes, int player)? UpgradeCost(BalanceConfig cfg, HomeBuilding b)
        {
            var df = Def(cfg, b.def);
            int next = b.level + 1;
            if (df.kind == "main")
            {
                if (next > cfg.home.levels.Count) return null;
                var l = cfg.home.levels[next - 1];
                return (l.wood, l.ore, l.minutes, l.player);
            }
            if (IsDeco(df) || df.kind == "tree" || next > df.levels.Count) return null;
            var bl = df.levels[next - 1];
            return (bl.wood, bl.ore, bl.minutes, 0);
        }

        public static HomeErr CanUpgrade(SaveData s, GameData d, int id)
        {
            var h = s.home;
            var b = Find(h, id);
            if (b == null) return HomeErr.NotFound;
            if (b.job != 0) return HomeErr.Busy;
            var cost = UpgradeCost(d.Cfg, b);
            if (cost == null) return HomeErr.MaxLevel;
            var (w, o, _, player) = cost.Value;
            if (b.def == "main") { if (s.level < player) return HomeErr.PlayerLevel; }
            else if (b.level + 1 > Level(h)) return HomeErr.HomeLevel; // công trình không vượt cấp Nhà chính
            if (!Afford(s, w, o, 0)) return HomeErr.Cost;
            if (Busy(h) >= Builders(h, d.Cfg.home)) return HomeErr.Builder;
            return HomeErr.Ok;
        }

        public static HomeErr Upgrade(SaveData s, GameData d, double now, int id)
        {
            Tick(s, d, now);
            var e = CanUpgrade(s, d, id);
            if (e != HomeErr.Ok) return e;
            var b = Find(s.home, id);
            var (w, o, min, _) = UpgradeCost(d.Cfg, b).Value;
            Pay(s, w, o, 0);
            b.job = 2;
            b.until = now + min * M;
            if (min <= 0) Finish(d.Cfg, b);
            return HomeErr.Ok;
        }

        static void Finish(BalanceConfig cfg, HomeBuilding b)
        {
            if (b.job == 2) b.level++;
            b.job = 0;
            b.until = 0;
            Fit(cfg, b);
        }

        // ---------- ô rừng ----------

        public static bool Adjacent(HomeState h, HomeConfig c, int lot)
        {
            var (i, j) = LotIJ(c, lot);
            int n = LotsPerSide(c);
            foreach (var (di, dj) in new[] { (1, 0), (-1, 0), (0, 1), (0, -1) })
            {
                int a = i + di, b = j + dj;
                if (a >= 0 && b >= 0 && a < n && b < n && h.lots.Contains(LotIndex(c, a, b))) return true;
            }
            return false;
        }

        public static HomeRing RingOf(HomeConfig c, int lot)
        {
            int r = Ring(c, lot);
            return r <= 0 || c.rings.Count == 0 ? null : c.rings[Math.Min(c.rings.Count - 1, r - 1)];
        }

        // giá dọn: gốc của vòng + bước × số ô đã mở (hoặc đang dọn) trong cùng vòng
        public static (int wood, int ore, double minutes) ClearCost(HomeState h, HomeConfig c, int lot)
        {
            var r = RingOf(c, lot);
            if (r == null) return (0, 0, 0);
            int ring = Ring(c, lot);
            int done = h.lots.Concat(h.clearing.Keys).Count(l => Ring(c, l) == ring);
            return (r.wood + r.woodStep * done, r.ore + r.oreStep * done, r.minutes);
        }

        public static HomeErr CanClear(SaveData s, GameData d, int lot)
        {
            var c = d.Cfg.home;
            var h = s.home;
            int n = LotsPerSide(c);
            if (lot < 0 || lot >= n * n) return HomeErr.NotFound;
            if (h.lots.Contains(lot) || h.clearing.ContainsKey(lot)) return HomeErr.Busy;
            if (LotKind(c, lot) == "hill") return HomeErr.Locked;
            if (!Adjacent(h, c, lot)) return HomeErr.NotAdjacent;
            var r = RingOf(c, lot);
            if (r == null) return HomeErr.Locked;
            if (Level(h) < r.home) return HomeErr.HomeLevel;
            if (s.level < r.player) return HomeErr.PlayerLevel;
            if (h.lots.Count + h.clearing.Count >= MaxLots(c, Level(h))) return HomeErr.Count;
            var (w, o, _) = ClearCost(h, c, lot);
            if (!Afford(s, w, o, 0)) return HomeErr.Cost;
            if (Busy(h) >= Builders(h, c)) return HomeErr.Builder;
            return HomeErr.Ok;
        }

        public static HomeErr ClearLot(SaveData s, GameData d, double now, int lot)
        {
            Tick(s, d, now);
            var e = CanClear(s, d, lot);
            if (e != HomeErr.Ok) return e;
            var (w, o, min) = ClearCost(s.home, d.Cfg.home, lot);
            Pay(s, w, o, 0);
            s.home.clearing[lot] = now + min * M;
            if (min <= 0) FinishJobs(s, d, now);
            return HomeErr.Ok;
        }

        // rút thời gian việc của công trình (id) hoặc ô rừng đang dọn (lot) đi speedMin phút, sau khi xem quảng cáo home_speed
        public static bool SpeedUp(SaveData s, GameData d, double now, int id, int lot = -1)
        {
            Tick(s, d, now);
            var h = s.home;
            double cut = d.Cfg.home.speedMin * M;
            var b = id >= 0 ? Find(h, id) : null;
            if (b != null && b.job != 0) b.until -= cut;
            else if (lot >= 0 && h.clearing.ContainsKey(lot)) h.clearing[lot] -= cut;
            else return false;
            FinishJobs(s, d, now);
            return true;
        }

        static void FinishJobs(SaveData s, GameData d, double now)
        {
            var h = s.home;
            var c = d.Cfg.home;
            foreach (var b in h.buildings)
                if (b.job != 0 && b.until <= now) Finish(d.Cfg, b);
            foreach (var lot in h.clearing.Where(kv => kv.Value <= now).Select(kv => kv.Key).ToList())
            {
                h.clearing.Remove(lot);
                h.lots.Add(lot);
                var ring = RingOf(c, lot);
                h.wood = Math.Min(Math.Max(h.wood, WoodCap(h, d.Cfg)), h.wood + (ring?.reward ?? 0));
                s.balls += ring?.balls ?? 0; // dọn rừng được bi để thả (người dùng dặn 2026-11-18)
                h.cleared.Add(lot);
            }
        }

        // ---------- năng suất, đồng hồ ----------

        public static double CapHours(BalanceConfig cfg, HomeBuildingDef df, int level)
        {
            var l = Lv(df, level);
            return l != null && l.capH > 0 ? l.capH : cfg.farm.capHours;
        }

        // khoảng ô trống giữa hai chân thoi theo một trục
        static int Gap(int a0, int an, int b0, int bn) => Math.Max(0, Math.Max(b0 - (a0 + an), a0 - (b0 + bn)));

        // cộng năng suất của giếng, cối nước (lấy cái lớn nhất, không cộng dồn)
        public static double Irrigation(HomeState h, BalanceConfig cfg, HomeBuilding b)
        {
            var df = Def(cfg, b.def);
            if (!df.irrigable) return 0;
            double best = 0;
            foreach (var w in h.buildings)
            {
                if ((w.def != "well" && w.def != "waterwheel") || w.job == 1) continue;
                var wd = Def(cfg, w.def);
                var l = Lv(wd, w.level);
                if (l == null) continue;
                int dist = Math.Max(Gap(b.gx, df.size, w.gx, wd.size), Gap(b.gy, df.size, w.gy, wd.size));
                if (dist <= l.radius) best = Math.Max(best, l.bonus);
            }
            return best;
        }

        // đất màu: chân thoi nằm trọn trong vùng fertile
        public static double Fertile(HomeConfig c, HomeBuildingDef df, HomeBuilding b) =>
            df.irrigable && c.features.Any(f => f.kind == "fertile" && f.Has(b.gx, b.gy) && f.Has(b.gx + df.size - 1, b.gy + df.size - 1)) ? c.fertileBonus : 0;

        // sản lượng mỗi giờ của tướng hero ở công trình b
        public static double Rate(SaveData s, GameData d, string hero, HomeBuilding b)
        {
            var df = Def(d.Cfg, b.def);
            var fc = d.Cfg.farm;
            var hd = d.Hero(hero);
            if (df.kind != "prod" || hd == null) return 0;
            double r = df.rate * fc.rarityPower[(int)hd.rarity] * (1 + fc.starStep * (StarTier.Legacy(s.Hero(hero).star) - 1));
            if (df.hasElem && hd.elem == df.elem) r *= fc.match;
            r *= Lv(df, b.level)?.mult ?? 1;
            if (df.irrigable && s.home != null) r *= 1 + Irrigation(s.home, d.Cfg, b) + Fertile(d.Cfg.home, df, b);
            return r;
        }

        public static double Hours(SaveData s, GameData d, string hero) => Farm.Hours(s, d, hero);

        // phần nghỉ được bớt: suối nước nóng (cấp cao nhất đang có) + bậc điểm đẹp, tối đa restCutMax
        public static double RestCut(HomeState h, BalanceConfig cfg)
        {
            double spring = h.buildings.Where(b => b.def == "hotspring" && b.job != 1).Select(b => Lv(Def(cfg, b.def), b.level)?.bonus ?? 0).DefaultIfEmpty(0).Max();
            return Math.Min(cfg.home.restCutMax, spring + BeautyTier(h, cfg) * cfg.home.restPerTier);
        }

        public static double RestMin(SaveData s, GameData d, string hero) =>
            Farm.RestMin(s, d, hero) * (1 - (s.home != null ? RestCut(s.home, d.Cfg) : 0));

        // tính tới now; false nếu giờ máy bị lùi (bỏ qua đoạn đó)
        public static bool Tick(SaveData s, GameData d, double now)
        {
            var h = Of(s, d, now);
            var c = d.Cfg.home;
            if (now < h.lastTick)
            {
                h.lastTick = now;
                return false;
            }
            double dt = (now - h.lastTick) / H;
            double oreLeft = h.ore;
            foreach (var b in h.buildings)
            {
                var df = Def(d.Cfg, b.def);
                if (df.kind != "prod" || b.job == 1) continue;
                double capH = CapHours(d.Cfg, df, b.level);
                foreach (var sl in b.slots)
                {
                    if (sl.hero == null || sl.energy <= 0) continue;
                    double work = Math.Min(dt, sl.energy);
                    double boosted = Math.Max(0, Math.Min(h.lastTick + work * H, h.boostUntil) - h.lastTick) / H;
                    double rate = Rate(s, d, sl.hero, b);
                    double add = rate * (work + boosted * (d.Cfg.farm.boostMult - 1));
                    if (df.output == "stones") add = Math.Min(add, Math.Max(0, oreLeft) / c.orePerStone); // lò rèn ăn quặng trong kho
                    double before = sl.stock;
                    sl.stock = Math.Min(Math.Max(before, rate * capH), before + add);
                    double got = sl.stock - before;
                    if (df.output == "stones") oreLeft -= got * c.orePerStone;
                    if (df.output == "ore") b.acc += got * c.evoPerOre;
                    sl.energy -= work;
                }
            }
            h.ore = Math.Max(0, oreLeft);
            FinishJobs(s, d, now);
            foreach (var k in h.rest.Where(kv => kv.Value <= now).Select(kv => kv.Key).ToList()) h.rest.Remove(k);
            h.lastTick = now;
            SyncTrees(s, d);
            return true;
        }

        // ---------- tướng ----------

        public static (int id, int slot) Working(HomeState h, string hero)
        {
            foreach (var b in h.buildings)
                for (int i = 0; i < b.slots.Count; i++)
                    if (b.slots[i].hero == hero) return (b.id, i);
            return (-1, -1);
        }

        public static double RestLeft(HomeState h, string hero, double now) => Math.Max(0, (h.rest.TryGetValue(hero, out var t) ? t : 0) - now);

        public static bool Free(SaveData s, HomeState h, string hero, double now) =>
            s.Hero(hero) != null && s.Hero(hero).owned && Working(h, hero).id < 0 && RestLeft(h, hero, now) <= 0;

        public static HomeErr CanPlaceHero(SaveData s, GameData d, double now, int id, int slot, string hero)
        {
            var h = s.home;
            var b = Find(h, id);
            if (b == null) return HomeErr.NotFound;
            var df = Def(d.Cfg, b.def);
            if (df.kind != "prod" || b.job == 1) return HomeErr.Busy;
            if (slot < 0 || slot >= b.slots.Count || b.slots[slot].hero != null) return HomeErr.Slot;
            if (!Free(s, h, hero, now)) return HomeErr.HeroBusy;
            if (UsedSlots(h) >= TotalSlots(h, d.Cfg.home)) return HomeErr.TotalSlots;
            if (IsBallOut(df) && UsedBallSlots(h, d.Cfg) >= BallSlots(s, d.Cfg)) return HomeErr.BallSlots;
            return HomeErr.Ok;
        }

        public static HomeErr Place(SaveData s, GameData d, double now, int id, int slot, string hero)
        {
            Tick(s, d, now);
            var e = CanPlaceHero(s, d, now, id, slot, hero);
            if (e != HomeErr.Ok) return e;
            var sl = Find(s.home, id).slots[slot];
            sl.hero = hero;
            sl.energy = Hours(s, d, hero);
            return HomeErr.Ok;
        }

        // rút tướng: tướng nghỉ theo công thức (rút giữa ca vẫn nghỉ đủ); đồ tích vẫn ở ô
        public static bool Remove(SaveData s, GameData d, double now, int id, int slot)
        {
            Tick(s, d, now);
            var b = Find(s.home, id);
            if (b == null || slot < 0 || slot >= b.slots.Count || b.slots[slot].hero == null) return false;
            var sl = b.slots[slot];
            s.home.rest[sl.hero] = now + RestMin(s, d, sl.hero) * M;
            sl.hero = null;
            sl.energy = 0;
            return true;
        }

        // cho tướng đang nghỉ ăn một cái bánh: hết nghỉ ngay
        public static HomeErr Feed(SaveData s, GameData d, double now, string hero)
        {
            Tick(s, d, now);
            var h = s.home;
            if (RestLeft(h, hero, now) <= 0) return HomeErr.Slot;
            if (h.bread <= 0) return HomeErr.Cost;
            h.bread--;
            h.rest.Remove(hero);
            return HomeErr.Ok;
        }

        // tự xếp: duyệt ô trống theo thứ tự công trình (bi trước), mỗi ô lấy tướng rảnh có năng suất cao nhất ở đó
        public static List<(int id, int slot, string hero)> Auto(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            var h = s.home;
            var placed = new List<(int, int, string)>();
            string[] order = { "balls", "fish", "wood", "ore", "stones", "bread" };
            foreach (var b in h.buildings.Where(x => Def(d.Cfg, x.def).kind == "prod").OrderBy(x => Array.IndexOf(order, Def(d.Cfg, x.def).output)).ThenBy(x => x.id))
                for (int i = 0; i < b.slots.Count; i++)
                {
                    if (b.slots[i].hero != null) continue;
                    string best = null;
                    double br = 0;
                    foreach (var hd in d.Heroes)
                    {
                        if (CanPlaceHero(s, d, now, b.id, i, hd.id) != HomeErr.Ok) continue;
                        double r = Rate(s, d, hd.id, b);
                        if (best == null || r > br)
                        {
                            best = hd.id;
                            br = r;
                        }
                    }
                    if (best == null) continue;
                    Place(s, d, now, b.id, i, best);
                    placed.Add((b.id, i, best));
                }
            return placed;
        }

        // ---------- thu hoạch ----------

        public static HomeYield Harvest(SaveData s, GameData d, double now, int id)
        {
            Tick(s, d, now);
            var y = new HomeYield();
            var b = Find(s.home, id);
            if (b != null) Collect(s, d, b, y);
            return y;
        }

        public static HomeYield HarvestAll(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            var y = new HomeYield();
            foreach (var b in s.home.buildings) Collect(s, d, b, y);
            return y;
        }

        // đồ đang tích (phần nguyên) của công trình b
        public static int Stock(HomeBuilding b) => b.slots.Sum(sl => (int)Math.Floor(sl.stock + 1e-9));

        static void Collect(SaveData s, GameData d, HomeBuilding b, HomeYield y)
        {
            var df = Def(d.Cfg, b.def);
            if (df.kind != "prod") return;
            var h = s.home;
            foreach (var sl in b.slots)
            {
                int n = (int)Math.Floor(sl.stock + 1e-9);
                if (df.output == "wood") n = Math.Min(n, (int)Math.Floor(WoodCap(h, d.Cfg) - h.wood));
                else if (df.output == "ore") n = Math.Min(n, (int)Math.Floor(OreCap(h, d.Cfg) - h.ore));
                else if (df.output == "bread") n = Math.Min(n, d.Cfg.home.breadCap - h.bread);
                if (n <= 0) continue;
                sl.stock -= n;
                switch (df.output)
                {
                    case "balls":
                        s.balls += n;
                        y.balls += n;
                        break;
                    case "wood":
                        h.wood += n;
                        y.wood += n;
                        break;
                    case "ore":
                        h.ore += n;
                        y.ore += n;
                        break;
                    case "stones":
                        s.potentialStones += n;
                        y.stones += n;
                        break;
                    case "bread":
                        h.bread += n;
                        y.bread += n;
                        break;
                    case "fish":
                        Fish(s, d, n, y);
                        break;
                }
            }
            if (df.output == "ore" && b.acc >= 1)
            {
                int e = (int)Math.Floor(b.acc);
                b.acc -= e;
                s.evoStones += e;
                y.evo += e;
            }
        }

        // mỗi lần câu quay bảng fish: bi, thẻ (Pachinko.RollChest), hoặc cúp câu cá vào túi trang trí
        static void Fish(SaveData s, GameData d, int n, HomeYield y)
        {
            var h = s.home;
            var t = d.Cfg.home.fish;
            if (t.rolls.Count == 0) return;
            var rng = new Rng(h.seed);
            for (int i = 0; i < n; i++)
            {
                var roll = rng.Weighted(t.rolls, r => r.w);
                if (roll.k == "deco")
                {
                    Bag(h, d.Cfg.home.fishDeco, 1);
                    y.deco.Add(d.Cfg.home.fishDeco);
                    continue;
                }
                var one = new ChestTable { kind = "fish", rolls = new List<ChestRoll> { roll } };
                foreach (var r in Pachinko.RollChest(s, d, one, 1, rng))
                    if (r.k == RewardKind.Balls) y.balls += r.n;
                    else y.other.Add(r);
            }
            h.seed = rng.S;
        }

        // ×2 năng suất trong farm.boostH giờ (quảng cáo farm_boost); không chồng khi đang tăng
        public static bool Boosting(HomeState h, double now) => h.boostUntil > now;

        public static bool Boost(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            var h = s.home;
            if (h.boostUntil > now) return false;
            h.boostUntil = now + d.Cfg.farm.boostH * H;
            return true;
        }

        // ---------- trang trí, điểm đẹp ----------

        public static int Beauty(HomeState h, BalanceConfig cfg) => h.buildings.Sum(b => Def(cfg, b.def)?.beauty ?? 0);
        public static int BeautyTier(HomeState h, BalanceConfig cfg) => cfg.home.beautyTiers.Count(t => Beauty(h, cfg) >= t);

        // nhận quà mốc điểm đẹp kế tiếp (null nếu chưa tới mốc)
        public static HomeGift ClaimBeauty(SaveData s, GameData d)
        {
            var h = s.home;
            var c = d.Cfg.home;
            if (h.beautyGifts >= BeautyTier(h, d.Cfg) || h.beautyGifts >= c.beautyGifts.Count) return null;
            var g = c.beautyGifts[h.beautyGifts++];
            h.wood = Math.Max(h.wood, Math.Min(WoodCap(h, d.Cfg), h.wood + g.wood));
            h.ore = Math.Max(h.ore, Math.Min(OreCap(h, d.Cfg), h.ore + g.ore));
            s.balls += g.balls;
            s.evoStones += g.evo;
            s.potentialStones += g.stones;
            return g;
        }

        // ---------- chấm báo, thử ----------

        // chấm báo ở sảnh: vừa mở mà chưa vào; tướng hết sức; kho đồ của một ô đầy
        public static bool Alert(SaveData s, GameData d, double now)
        {
            if (!Open(s, d.Cfg)) return false;
            if (s.home == null) return true;
            Tick(s, d, now);
            foreach (var b in s.home.buildings)
            {
                var df = Def(d.Cfg, b.def);
                if (df.kind != "prod") continue;
                double capH = CapHours(d.Cfg, df, b.level);
                foreach (var sl in b.slots)
                    if (sl.hero != null && (sl.energy <= 0 || sl.stock >= Rate(s, d, sl.hero, b) * capH - 1e-9)) return true;
            }
            return false;
        }

        // bảng thử: giả như đã trôi qua ms
        public static void Travel(SaveData s, double ms)
        {
            var h = s.home;
            if (h == null) return;
            h.lastTick -= ms;
            if (h.boostUntil != 0) h.boostUntil -= ms;
            foreach (var k in h.rest.Keys.ToList()) h.rest[k] -= ms;
            foreach (var k in h.clearing.Keys.ToList()) h.clearing[k] -= ms;
            foreach (var b in h.buildings)
                if (b.job != 0) b.until -= ms;
        }
    }
}
