// Cấu hình Nhà (GD_Claude/21_Nha_Home.md, 2026-11-18): khối "home" trong balance.json. Lớp [Serializable], chỉ dùng List và mảng
// phẳng để Unity lưu được trong BalanceConfigAsset. Số là số tạm, đo lại bằng ProgressSim.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // một cấp Nhà chính: cấp người chơi cần, giá, thời gian, tổng chỗ tướng, số đội thợ
    [Serializable]
    public class HomeLevel
    {
        public int player, wood, ore, slots, builders = 1;
        public double minutes;
    }

    // một cấp của công trình: chỗ tướng, hệ số năng suất, giá, thời gian; kho: sức chứa; giếng, cối nước: bán kính, cộng năng suất;
    // suối nước nóng: phần nghỉ được bớt (bonus)
    [Serializable]
    public class HomeBLevel
    {
        public int slots, wood, ore, cap, capOre;
        public double mult = 1, minutes, capH, radius, bonus;
    }

    [Serializable]
    public class HomeBuildingDef
    {
        public string id, name;
        public string Name => Loc.T(name); // tên theo ngôn ngữ
        public string kind; // main, prod (cần tướng), support, tree (Cây bi), deco, road
        public int size; // cạnh chân thoi, ô
        public bool hasElem;
        public Elem elem; // hệ hợp (prod)
        public string output; // prod: balls, wood, ore, fish, stones, bread
        public double rate; // sản lượng gốc mỗi giờ của một tướng
        public string need; // "ore": chỉ đặt trên mạch quặng; "stream": phải sát suối
        public bool irrigable; // ăn cộng năng suất của giếng, cối nước, đất màu
        public int home = 1; // Nhà chính cấp mấy thì mở
        public int[] count = new int[0]; // số tối đa theo cấp Nhà (rỗng: 1; trang trí, đường không giới hạn)
        public List<HomeBLevel> levels = new List<HomeBLevel>();
        public int beauty, wood, ore, balls; // trang trí, đường: điểm đẹp và giá
        public bool reward; // trang trí chỉ có từ thưởng (tượng boss, cúp câu cá)
        public string set; // bộ trang trí theo hệ
    }

    // vòng ô rừng tính từ khoảnh đầu (1, 2, 3): khoá cấp Nhà, cấp người chơi, giá (tăng theo số ô đã mở trong vòng), thời gian, gỗ rơi
    [Serializable]
    public class HomeRing
    {
        public int home, player, wood, woodStep, ore, oreStep, reward, balls; // reward: gỗ; balls: bi để thả máy bi khi dọn xong
        public double minutes;
    }

    // ô rừng có kiểu riêng (mặc định "forest"; "hill": cao nguyên, không mở)
    [Serializable]
    public class HomeLotDef
    {
        public int i, j;
        public string kind;
    }

    // điểm cố định trên lưới: lake, stream, rock (chặn), ore (mạch quặng: chỉ Mỏ), fertile (đất màu)
    [Serializable]
    public class HomeFeature
    {
        public string kind;
        public int gx, gy, w, d;
        public bool Has(int x, int y) => x >= gx && x < gx + w && y >= gy && y < gy + d;
    }

    [Serializable]
    public class HomePlace
    {
        public string b;
        public int gx, gy;
    }

    [Serializable]
    public class HomeGift
    {
        public int wood, ore, balls, evo, stones;
    }

    // loại ô lát (học ô đường, ô nước của Clash of Critters, 2026-11-18): một ô lát = tile x tile ô lưới; block: chặn xây (nước)
    [Serializable]
    public class HomeTileDef
    {
        public string id, name;
        public string Name => Loc.T(name);
        public int wood, ore;
        public bool block;
    }

    [Serializable]
    public class HomeConfig
    {
        public int grid = 72, lot = 12; // đảo 72 x 72 ô, 6 x 6 ô rừng 12 x 12 (người dùng dặn 2026-11-19: đảo to ra cho quái đi khắp nơi)
        public List<HomeLotDef> startLots = new List<HomeLotDef>();
        public int[] maxLots = new int[0]; // tổng ô rừng đã mở tối đa theo cấp Nhà (kể cả khoảnh đầu)
        public List<HomeRing> rings = new List<HomeRing>();
        public List<HomeLotDef> lots = new List<HomeLotDef>();
        public List<HomeFeature> features = new List<HomeFeature>();
        public List<HomeLevel> levels = new List<HomeLevel>();
        public int woodCap = 200, oreCap = 60, breadCap = 20;
        public double orePerStone = 5, evoPerOre = 0.008, fertileBonus = 0.1, restCutMax = 0.75, speedMin = 30;
        public int[] beautyTiers = new int[0];
        public double restPerTier = 0.05;
        public List<HomeGift> beautyGifts = new List<HomeGift>();
        public string fishDeco = "cup_fish";
        public ChestTable fish = new ChestTable { kind = "fish" };
        public List<HomePlace> layout = new List<HomePlace>();
        public List<HomeBuildingDef> buildings = new List<HomeBuildingDef>();
        public int tile = 2; // cạnh ô lát, ô lưới
        public List<HomeTileDef> tiles = new List<HomeTileDef>();
        public List<HomePlace> startTiles = new List<HomePlace>(); // ô lát có sẵn lúc mới (b = loại, gx, gy = toạ độ ô lát)

        public HomeBuildingDef Def(string id) => buildings.Find(b => b.id == id);
        public HomeTileDef Tile(string id) => tiles.Find(t => t.id == id);

        public static HomeConfig Parse(Dictionary<string, object> o, Func<List<object>, List<ChestRoll>> rolls)
        {
            var c = new HomeConfig();
            if (o == null) return c;
            c.grid = J.Int(o, "grid", 72);
            c.lot = J.Int(o, "lot", 12);
            foreach (var x in J.Arr(o, "startLots"))
            {
                var a = J.Arr(x);
                if (a.Count >= 2) c.startLots.Add(new HomeLotDef { i = (int)(double)a[0], j = (int)(double)a[1], kind = "start" });
            }
            c.maxLots = Ints(J.Arr(o, "maxLots"));
            foreach (var x in J.Arr(o, "rings"))
            {
                var r = J.Obj(x);
                c.rings.Add(new HomeRing
                {
                    home = J.Int(r, "home"), player = J.Int(r, "player"), wood = J.Int(r, "wood"), woodStep = J.Int(r, "woodStep"),
                    ore = J.Int(r, "ore"), oreStep = J.Int(r, "oreStep"), minutes = J.Num(r, "minutes"), reward = J.Int(r, "reward"), balls = J.Int(r, "balls"),
                });
            }
            foreach (var x in J.Arr(o, "lots"))
            {
                var l = J.Obj(x);
                c.lots.Add(new HomeLotDef { i = J.Int(l, "i"), j = J.Int(l, "j"), kind = J.Str(l, "kind", "forest") });
            }
            foreach (var x in J.Arr(o, "features"))
            {
                var f = J.Obj(x);
                c.features.Add(new HomeFeature { kind = J.Str(f, "kind"), gx = J.Int(f, "gx"), gy = J.Int(f, "gy"), w = J.Int(f, "w", 1), d = J.Int(f, "d", 1) });
            }
            foreach (var x in J.Arr(o, "levels"))
            {
                var l = J.Obj(x);
                c.levels.Add(new HomeLevel
                {
                    player = J.Int(l, "player"), wood = J.Int(l, "wood"), ore = J.Int(l, "ore"), minutes = J.Num(l, "minutes"),
                    slots = J.Int(l, "slots"), builders = J.Int(l, "builders", 1),
                });
            }
            c.woodCap = J.Int(o, "woodCap", 200);
            c.oreCap = J.Int(o, "oreCap", 60);
            c.breadCap = J.Int(o, "breadCap", 20);
            c.orePerStone = J.Num(o, "orePerStone", 5);
            c.evoPerOre = J.Num(o, "evoPerOre", 0.008);
            c.fertileBonus = J.Num(o, "fertileBonus", 0.1);
            c.restCutMax = J.Num(o, "restCutMax", 0.75);
            c.speedMin = J.Num(o, "speedMin", 30);
            c.beautyTiers = Ints(J.Arr(o, "beautyTiers"));
            c.restPerTier = J.Num(o, "restPerTier", 0.05);
            foreach (var x in J.Arr(o, "beautyGifts"))
            {
                var g = J.Obj(x);
                c.beautyGifts.Add(new HomeGift { wood = J.Int(g, "wood"), ore = J.Int(g, "ore"), balls = J.Int(g, "balls"), evo = J.Int(g, "evo"), stones = J.Int(g, "stones") });
            }
            c.fishDeco = J.Str(o, "fishDeco", "cup_fish");
            c.fish = new ChestTable { kind = "fish", rolls = rolls(J.Arr(o, "fish")) };
            foreach (var x in J.Arr(o, "layout"))
            {
                var p = J.Obj(x);
                c.layout.Add(new HomePlace { b = J.Str(p, "b"), gx = J.Int(p, "gx"), gy = J.Int(p, "gy") });
            }
            foreach (var x in J.Arr(o, "buildings"))
            {
                var b = J.Obj(x);
                var e = J.Str(b, "elem");
                var df = new HomeBuildingDef
                {
                    id = J.Str(b, "id"), name = J.Str(b, "name"), kind = J.Str(b, "kind"), size = J.Int(b, "size", 1),
                    hasElem = e != null, elem = e != null ? Keys.ToElem(e) : Elem.Kim,
                    output = J.Str(b, "output"), rate = J.Num(b, "rate"), need = J.Str(b, "need"), irrigable = J.Bool(b, "irrigable"),
                    home = J.Int(b, "home", 1), count = Ints(J.Arr(b, "count")),
                    beauty = J.Int(b, "beauty"), wood = J.Int(b, "wood"), ore = J.Int(b, "ore"), balls = J.Int(b, "balls"),
                    reward = J.Bool(b, "reward"), set = J.Str(b, "set"),
                };
                foreach (var y in J.Arr(b, "levels"))
                {
                    var l = J.Obj(y);
                    df.levels.Add(new HomeBLevel
                    {
                        slots = J.Int(l, "slots"), mult = J.Num(l, "mult", 1), wood = J.Int(l, "wood"), ore = J.Int(l, "ore"),
                        minutes = J.Num(l, "minutes"), capH = J.Num(l, "capH"), cap = J.Int(l, "cap"), capOre = J.Int(l, "capOre"),
                        radius = J.Num(l, "radius"), bonus = J.Num(l, "bonus"),
                    });
                }
                c.buildings.Add(df);
            }
            c.tile = J.Int(o, "tile", 2);
            foreach (var x in J.Arr(o, "tiles"))
            {
                var t = J.Obj(x);
                c.tiles.Add(new HomeTileDef { id = J.Str(t, "id"), name = J.Str(t, "name"), wood = J.Int(t, "wood"), ore = J.Int(t, "ore"), block = J.Bool(t, "block") });
            }
            foreach (var x in J.Arr(o, "startTiles"))
            {
                var p = J.Obj(x);
                c.startTiles.Add(new HomePlace { b = J.Str(p, "b"), gx = J.Int(p, "gx"), gy = J.Int(p, "gy") });
            }
            return c;
        }

        // lỗi dữ liệu (test và menu nhập dữ liệu gọi): công trình thiếu, bố cục đầu chồng nhau hay ra ngoài khoảnh đầu, mảng theo cấp Nhà thiếu
        public List<string> Validate()
        {
            var err = new List<string>();
            int n = grid / Math.Max(1, lot);
            if (grid % lot != 0) err.Add($"Nhà: lưới {grid} không chia hết ô rừng {lot}");
            if (levels.Count == 0) err.Add("Nhà: thiếu cấp Nhà chính");
            if (maxLots.Length < levels.Count) err.Add("Nhà: maxLots thiếu cấp");
            if (rings.Count < 3) err.Add("Nhà: thiếu vòng ô rừng");
            if (Def("main") == null) err.Add("Nhà: thiếu công trình main");
            if (Def("tree") == null) err.Add("Nhà: thiếu công trình tree (Cây bi)");
            if (beautyGifts.Count < beautyTiers.Length) err.Add("Nhà: thiếu quà mốc điểm đẹp");
            if (Def(fishDeco) == null) err.Add("Nhà: thiếu trang trí " + fishDeco);
            foreach (var b in buildings)
            {
                if (b.size < 1) err.Add($"Nhà: {b.id} cỡ {b.size}");
                if (b.kind == "prod" && (b.output == null || b.levels.Count == 0 || b.rate <= 0)) err.Add($"Nhà: {b.id} thiếu đầu ra, cấp hoặc năng suất");
                if ((b.kind == "prod" || b.kind == "support") && b.count.Length < levels.Count) err.Add($"Nhà: {b.id} count thiếu cấp Nhà");
            }
            var start = new HashSet<int>(startLots.Select(l => l.i * n + l.j));
            var cells = new Dictionary<(int, int), string>();
            foreach (var p in layout)
            {
                var df = Def(p.b);
                if (df == null)
                {
                    err.Add("Nhà: bố cục đầu có công trình lạ " + p.b);
                    continue;
                }
                for (int x = p.gx; x < p.gx + df.size; x++)
                for (int y = p.gy; y < p.gy + df.size; y++)
                {
                    if (!start.Contains(x / lot * n + y / lot)) err.Add($"Nhà: {p.b} ở ({p.gx},{p.gy}) ra ngoài khoảnh đầu");
                    else if (cells.TryGetValue((x, y), out var other)) err.Add($"Nhà: {p.b} chồng {other} ở ({x},{y})");
                    else cells[(x, y)] = p.b;
                    if (features.Any(f => f.Has(x, y) && f.kind != "fertile")) err.Add($"Nhà: {p.b} đè lên điểm cố định ở ({x},{y})");
                }
            }
            if (layout.Count(p => p.b == "main") != 1) err.Add("Nhà: bố cục đầu phải có đúng một Nhà chính");
            foreach (var f in features)
                if (f.gx < 0 || f.gy < 0 || f.gx + f.w > grid || f.gy + f.d > grid) err.Add($"Nhà: điểm {f.kind} ra ngoài lưới");
            if (tile < 1 || grid % tile != 0 || lot % tile != 0) err.Add($"Nhà: ô lát {tile} không chia hết lưới, ô rừng");
            if (tiles.Count == 0) err.Add("Nhà: thiếu loại ô lát");
            foreach (var t in startTiles)
            {
                if (Tile(t.b) == null) err.Add("Nhà: ô lát đầu loại lạ " + t.b);
                for (int x = t.gx * tile; x < (t.gx + 1) * tile; x++)
                for (int y = t.gy * tile; y < (t.gy + 1) * tile; y++)
                    if (cells.ContainsKey((x, y)) || !start.Contains(x / lot * n + y / lot)) err.Add($"Nhà: ô lát đầu ({t.gx},{t.gy}) chồng công trình hoặc ra ngoài khoảnh đầu");
            }
            return err.Distinct().ToList();
        }

        static int[] Ints(List<object> l) => l.Select(x => x is double d ? (int)d : 0).ToArray();
    }
}
