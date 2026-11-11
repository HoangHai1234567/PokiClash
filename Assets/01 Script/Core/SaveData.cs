// Bản lưu của người chơi, chép cấu trúc SaveData của Web/src/core/progression.ts (SAVE_VERSION = 2).
// Khoá JSON giữ đúng tên bên web. Khoá lạ (side meta về sau) được giữ nguyên khi đọc rồi ghi lại.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum CardSlot { Skill, Ult, Passive }

    public sealed class CardProg
    {
        public int lv = 1;
        public int copies;
    }

    public sealed class HeroProg
    {
        public bool owned;
        public int shards;
        public int star = 1;
        public CardProg skill = new CardProg();
        public CardProg ult = new CardProg();
        public CardProg passive = new CardProg();

        public PotLine[] potential = new PotLine[4]; // 4 ô tiềm năng (null = trống)
        public PotLine[] potentialNew; // kết quả khai phá đang chờ chọn giữ mới / giữ cũ

        public CardProg Card(CardSlot s) => s == CardSlot.Skill ? skill : s == CardSlot.Ult ? ult : passive;
    }

    public sealed class Settings
    {
        public bool boil = true; // công tắc "Nét vẽ rung" đã bỏ 2026-11-06; giữ trường để đọc bản lưu cũ, không còn dùng
        public bool sound = true;
        public bool hints = true; // bong bóng gợi ý trong trận
        public bool haptics = true; // rung (máy bi, mở rương, lên cấp)
    }

    public sealed class SaveStats
    {
        public int battles;
        public int wins;
        public int dropped;
    }

    // đồng hồ AFK theo đoạn (xem Afk.cs); mốc giờ là mili giây kể từ 1970, số thực như bản web
    public sealed class AfkState
    {
        public double hours; // giờ AFK hiệu dụng đã dồn, tối đa afkCapH, về 0 khi nhận
        public double lastTick; // lần tính gần nhất
        public double boostUntil; // hết tăng tốc ×2
        public double chestAcc; // giờ hiệu dụng dồn cho rương AFK tiếp theo
        public List<double> chests = new List<double>(); // lúc từng rương AFK vào khay
        public double chainAt; // rương đầu khay đếm giờ mở từ max(lúc vào khay, chainAt)
        public int stage; // ải người chơi chọn cho đội AFK (id ải), 0: chưa chọn (Afk.Stage tự lấy ải xa nhất có rơi mảnh)
    }

    // Đền Huy Hiệu: bậc cao nhất đã có (0..5) và số trận đã thắng trong bậc đang đánh
    public sealed class BadgeProg
    {
        public int tier;
        public int won;
    }

    public sealed class SaveData
    {
        public int v;
        public int level = 1;
        public int exp;
        public int balls;
        public int ballsSpent;
        public bool legendDone;
        public int gift, giftTier; // mốc quà máy bi: bi đã tiêu vào mốc đang chạy, số mốc đã nhận
        public int[] rings = new int[2]; // vòng nấm máy bi (trái, phải): số nấc đã có
        public Dictionary<string, HeroProg> heroes = new Dictionary<string, HeroProg>(); // theo thứ tự tướng trong dữ liệu
        public List<string> team = new List<string>();
        public int[] zones = new int[5]; // số ải đã qua trong từng đảo, chỉ số theo Elem
        public int[] zoneChests = new int[5]; // số rương mốc đã nhận trong từng đảo
        public SortedDictionary<int, int> clears = new SortedDictionary<int, int>(); // số lần qua mỗi ải
        public long afkSince; // lần nhận AFK gần nhất, mili giây kể từ 1970 (giống Date.now())
        public AfkState afk = new AfkState();
        public int potentialStones; // đá tiềm năng
        public CaveDay cave; // Hang Tiềm Năng: lượt trong ngày
        public FarmState farm; // trang trại (null = chưa dùng)
        public AdState ads; // lượt quảng cáo đã dùng trong ngày theo chỗ đặt
        public TreeState trees; // cây bi (null = chưa tính lần nào)
        public Entitlements ent; // quyền lợi gói đã mua
        public BadgeProg[] badges = { new BadgeProg(), new BadgeProg(), new BadgeProg(), new BadgeProg(), new BadgeProg() }; // chỉ số theo Elem
        public Settings settings = new Settings();
        public SaveStats stats = new SaveStats();
        public bool intro;
        public string starter; // tướng khởi đầu đã chọn (tướng đồng hành); null = chưa chọn, sảnh mở hộp chọn tướng
        public List<PendingChest> chests = new List<PendingChest>(); // rương máy bi đang chờ mở (giữ khi rời máy)
        public Dictionary<string, object> extra = new Dictionary<string, object>(); // khoá chưa biết, giữ nguyên

        public HeroProg Hero(string id) => heroes.TryGetValue(id, out var h) ? h : null;

        // người chơi mới đã chọn tướng khởi đầu đầu danh sách (Tí Tách từ 2026-11-11, trước là Giọt Sương): cho test và máy tự chơi
        public static SaveData New(GameData data, long now) => New(data, now, data.Starters.FirstOrDefault());

        // người chơi mới; starter null = chưa chọn (game mở hộp chọn tướng ở sảnh)
        public static SaveData New(GameData data, long now, string starter)
        {
            var s = new SaveData { v = data.Cfg.saveVersion, balls = 10, afkSince = now };
            s.afk.lastTick = now;
            foreach (var h in data.Heroes) s.heroes[h.id] = new HeroProg();
            if (starter != null) s.ChooseStarter(starter);
            return s;
        }

        // chọn tướng khởi đầu: có tướng đó, đội chỉ có tướng đó
        public void ChooseStarter(string id)
        {
            starter = id;
            Hero(id).owned = true;
            team.Clear();
            team.Add(id);
        }

        // Tướng mới thêm vào dữ liệu sau khi đã lưu: bổ sung (giống bản web).
        public void FillMissingHeroes(GameData data)
        {
            foreach (var h in data.Heroes)
                if (!heroes.ContainsKey(h.id)) heroes[h.id] = new HeroProg { owned = h.id == starter };
        }
    }

    public sealed class PendingChest
    {
        public string kind; // chest_wood, chest_silver, chest_gold
        public int x; // mức cược lúc bi rơi vào
    }

    public enum LoadStatus { Ok, Migrated, Outdated, Corrupt }

    public static class SaveCodec
    {
        static readonly string[] ElemKeys = { "kim", "moc", "thuy", "hoa", "tho" }; // theo thứ tự Elem

        // Bước di chuyển: từ phiên bản n lên n+1, sửa thẳng trên cây JSON. v1 -> v2 đổi hẳn cấu trúc đảo (không có bước).
        public static readonly Dictionary<int, Action<Dictionary<string, object>>> Migrations =
            new Dictionary<int, Action<Dictionary<string, object>>>
            {
                [2] = MigrateAdsV2, [3] = MigrateRosterV3, [4] = MigrateStarterV4, [5] = MigrateThuyV5, [6] = MigrateCaDenV6,
            };

        // v5 -> v6 (lô 10 tướng mới đảo Thủy, 2026-11-11, người dùng chọn "chuyển tướng cũ sang tướng mới"): tướng cũ cùng suất đảo
        // gộp vào tướng mới (sở hữu, mảnh, sao, cấp thẻ, tiềm năng) rồi bỏ khỏi bản lưu; đội, trang trại, tướng khởi đầu đổi id theo.
        // Tướng mới phần lớn chỉ 2 dạng: sao cao vẫn đọc được, dạng dừng ở dạng cuối (HeroDef.FormIndex).
        public static readonly (string from, string to)[] ThuyV6 =
        {
            ("giot_suong", "ti_tach"), ("tieu_y", "thach_giai"), ("canh_cut", "ca_den"), ("mi_nhi", "ha_ba"),
            ("ma_ket", "so_ngoc"), ("vay_lam", "giong_bao"), ("kuba", "lien_kinh"), ("thuong_lam", "uyen_xa"),
            ("huyen_vu", "han_ngac"), ("lam_quan", "hai_long"),
        };

        // v6 -> v7 (2026-11-11): suất ải 10 đảo Thủy đổi dòng Nòng Xoáy (nong_xoay) thành dòng Hải Đăng (ca_den, cá đèn lồng);
        // bản lưu v6 đã có nong_xoay thì gộp sang ca_den như bước trên (sở hữu, mảnh, sao, cấp thẻ, tiềm năng, đội, tướng khởi đầu)
        public static readonly (string from, string to)[] CaDenV7 = { ("nong_xoay", "ca_den") };

        public static void MigrateCaDenV6(Dictionary<string, object> o)
        {
            GopTuong(o, CaDenV7);
            var st = J.Str(o, "starter");
            if (st != null) o["starter"] = Map(CaDenV7, st);
        }

        public static void MigrateThuyV5(Dictionary<string, object> o)
        {
            GopTuong(o, ThuyV6);
            var st = J.Str(o, "starter");
            if (st != null) o["starter"] = Map(ThuyV6, st);
        }

        // v4 -> v5 (chọn 1 trong 5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md): bản lưu cũ coi như đã chọn Giọt Sương (tướng khởi
        // đầu duy nhất trước đó); không có Giọt Sương thì tướng đầu tiên đã có; không có tướng nào thì để trống (sảnh mở hộp chọn)
        public static void MigrateStarterV4(Dictionary<string, object> o)
        {
            var hs = J.Obj(o, "heroes");
            if (hs == null) return;
            string pick = J.Bool(J.Obj(hs, "giot_suong"), "owned") ? "giot_suong" : null;
            if (pick == null)
                foreach (var kv in hs)
                    if (J.Bool(J.Obj(kv.Value), "owned"))
                    {
                        pick = kv.Key;
                        break;
                    }
            if (pick != null) o["starter"] = pick;
        }

        // v3 -> v4 (chép migrateRosterV3 ở Web/src/core/progression.ts, 40 tướng 2026-11-02): tướng cũ thành dạng của tướng khác
        // (gộp) hoặc bị bỏ khỏi danh sách (đổi sang tướng thay)
        public static readonly (string from, string to)[] RosterV4 =
        {
            ("y_trach", "tieu_y"), ("van_quan", "lam_quan"), ("hac_duc", "lam_quan"), ("gia_bi", "nu_hoa"), ("su_gia", "de_hoa"),
        };

        static string Map((string from, string to)[] map, string id)
        {
            foreach (var (from, to) in map)
                if (from == id) return to;
            return id;
        }

        static bool AnyLine(object pot)
        {
            foreach (var x in J.Arr(pot))
                if (x != null) return true;
            return false;
        }

        // Gộp tiến trình: có tướng nếu một trong hai có, cộng mảnh và bản sao, lấy sao và cấp thẻ cao hơn, giữ tiềm năng của bên đã
        // có dòng. Đội, chỗ trang trại, giờ nghỉ đổi id theo; tướng trùng trong đội hoặc trên hai chỗ trang trại thì giữ chỗ đầu.
        // Thứ tự khoá như JS (xoá rồi thêm thì khoá mới ở cuối): dựng lại danh sách tướng, không sửa Dictionary tại chỗ.
        public static void MigrateRosterV3(Dictionary<string, object> o) => GopTuong(o, RosterV4);

        // Gộp tướng theo bảng (from → to), dùng cho v3 -> v4 và v5 -> v6
        static void GopTuong(Dictionary<string, object> o, (string from, string to)[] map)
        {
            string MapV4(string id) => Map(map, id);
            var hs = J.Obj(o, "heroes");
            if (hs != null)
            {
                var order = new List<KeyValuePair<string, object>>(hs);
                int Find(string k) => order.FindIndex(kv => kv.Key == k);
                foreach (var (from, to) in map)
                {
                    int ia = Find(from);
                    if (ia < 0) continue;
                    var a = J.Obj(order[ia].Value);
                    order.RemoveAt(ia);
                    int ib = Find(to);
                    if (ib < 0)
                    {
                        order.Add(new KeyValuePair<string, object>(to, a));
                        continue;
                    }
                    var b = J.Obj(order[ib].Value);
                    b["owned"] = J.Bool(b, "owned") || J.Bool(a, "owned");
                    b["shards"] = (double)(J.Int(b, "shards") + J.Int(a, "shards"));
                    b["star"] = (double)Math.Max(J.Int(b, "star"), J.Int(a, "star"));
                    var bc = J.Obj(b, "cards");
                    var ac = J.Obj(a, "cards");
                    if (bc == null && ac != null) b["cards"] = ac;
                    if (bc != null && ac != null)
                    foreach (var k in new[] { "skill", "ult", "passive" })
                    {
                        var x = J.Obj(bc, k);
                        var y = J.Obj(ac, k);
                        if (x == null || y == null)
                        {
                            if (x == null && y != null) bc[k] = y;
                            continue;
                        }
                        x["lv"] = (double)Math.Max(J.Int(x, "lv"), J.Int(y, "lv"));
                        x["copies"] = (double)(J.Int(x, "copies") + J.Int(y, "copies"));
                    }
                    if (!AnyLine(J.Get(b, "potential")) && AnyLine(J.Get(a, "potential"))) b["potential"] = a["potential"];
                }
                var nh = new Dictionary<string, object>();
                foreach (var kv in order) nh[kv.Key] = kv.Value;
                o["heroes"] = nh;
            }

            var team = new List<object>();
            foreach (var t in J.Arr(o, "team"))
            {
                var id = MapV4(t as string);
                if (!team.Contains(id)) team.Add(id);
            }
            o["team"] = team;

            var fm = J.Obj(o, "farm");
            if (fm == null) return;
            var seen = new HashSet<string>();
            foreach (var x in J.Arr(fm, "spots"))
            {
                var sp = J.Obj(x);
                var h = J.Str(sp, "hero");
                if (h != null)
                {
                    h = MapV4(h);
                    sp["hero"] = h;
                }
                if (h != null && seen.Contains(h))
                {
                    sp["hero"] = null;
                    sp["energy"] = 0.0;
                }
                else if (h != null) seen.Add(h);
            }
            var rest = new Dictionary<string, object>();
            var r0 = J.Obj(fm, "rest");
            if (r0 != null)
                foreach (var kv in r0)
                {
                    var id = MapV4(kv.Key);
                    double v = Convert.ToDouble(kv.Value);
                    rest[id] = rest.TryGetValue(id, out var p) ? Math.Max((double)p, v) : v;
                }
            fm["rest"] = rest;
        }

        // v2 -> v3 (chép migrateAdsV2 ở Web/src/core/ads.ts): bộ đếm quảng cáo riêng của AFK, trang trại, hang dồn về ads,
        // chỉ giữ số của ngày mới nhất
        public static void MigrateAdsV2(Dictionary<string, object> o)
        {
            var af = J.Obj(o, "afk") ?? new Dictionary<string, object>();
            var fm = J.Obj(o, "farm") ?? new Dictionary<string, object>();
            var cv = J.Obj(o, "cave") ?? new Dictionary<string, object>();
            bool caveAd = J.Bool(cv, "ad");
            int day = Math.Max(Math.Max(J.Int(af, "adDay"), J.Int(fm, "adDay")), caveAd ? J.Int(cv, "day") : 0);
            if (day > 0)
            {
                var used = new Dictionary<string, object>();
                if (J.Int(af, "adDay") == day && J.Int(af, "adOpen") > 0) used["afk_chest_open"] = (double)J.Int(af, "adOpen");
                if (J.Int(af, "adDay") == day && J.Int(af, "adBoost") > 0) used["afk_boost"] = (double)J.Int(af, "adBoost");
                if (J.Int(fm, "adDay") == day && J.Int(fm, "adCount") > 0) used["farm_boost"] = (double)J.Int(fm, "adCount");
                if (caveAd && J.Int(cv, "day") == day) used["cave_extra"] = 1.0;
                o["ads"] = new Dictionary<string, object> { ["day"] = (double)day, ["used"] = used };
            }
            af.Remove("adDay");
            af.Remove("adOpen");
            af.Remove("adBoost");
            fm.Remove("adDay");
            fm.Remove("adCount");
            cv.Remove("ad");
        }

        static readonly HashSet<string> Known = new HashSet<string>
        {
            "v", "level", "exp", "balls", "ballsSpent", "legendDone", "gift", "giftTier", "rings", "heroes", "team", "zones", "zoneChests", "clears",
            "afkSince", "afk", "badges", "potentialStones", "cave", "farm", "trees", "ads", "ent", "settings", "stats", "intro", "starter", "chests",
        };

        public static int VersionOf(string json)
        {
            try
            {
                return J.Int(J.Obj(MiniJson.Parse(json)), "v", -1);
            }
            catch (FormatException)
            {
                return -1;
            }
        }

        // Đọc bản lưu. Phiên bản cũ hơn mà có đủ bước di chuyển thì chạy; không thì trả Outdated (người gọi báo rồi làm mới).
        public static LoadStatus Read(string json, GameData data, out SaveData save)
        {
            save = null;
            Dictionary<string, object> o;
            try
            {
                o = J.Obj(MiniJson.Parse(json));
            }
            catch (Exception)
            {
                return LoadStatus.Corrupt;
            }
            if (o == null || !(J.Get(o, "v") is double)) return LoadStatus.Corrupt;

            int want = data.Cfg.saveVersion;
            int v = J.Int(o, "v");
            bool migrated = false;
            if (v > want) return LoadStatus.Outdated; // bản lưu của game mới hơn: không đọc bừa
            while (v < want)
            {
                if (!Migrations.TryGetValue(v, out var step)) return LoadStatus.Outdated;
                step(o);
                v++;
                o["v"] = (double)v;
                migrated = true;
            }

            try
            {
                save = FromTree(o);
            }
            catch (Exception)
            {
                save = null;
                return LoadStatus.Corrupt;
            }
            save.FillMissingHeroes(data);
            return migrated ? LoadStatus.Migrated : LoadStatus.Ok;
        }

        static SaveData FromTree(Dictionary<string, object> o)
        {
            var s = new SaveData
            {
                v = J.Int(o, "v"),
                level = J.Int(o, "level", 1),
                exp = J.Int(o, "exp"),
                balls = J.Int(o, "balls"),
                ballsSpent = J.Int(o, "ballsSpent"),
                legendDone = J.Bool(o, "legendDone"),
                gift = J.Int(o, "gift"),
                giftTier = J.Int(o, "giftTier"),
                afkSince = (long)J.Num(o, "afkSince"),
                intro = J.Bool(o, "intro"),
                starter = J.Str(o, "starter"),
            };
            var heroes = J.Obj(o, "heroes");
            if (heroes != null)
                foreach (var kv in heroes)
                {
                    var h = J.Obj(kv.Value);
                    var cards = J.Obj(h, "cards");
                    s.heroes[kv.Key] = new HeroProg
                    {
                        owned = J.Bool(h, "owned"),
                        shards = J.Int(h, "shards"),
                        star = J.Int(h, "star", 1),
                        skill = Card(J.Obj(cards, "skill")),
                        ult = Card(J.Obj(cards, "ult")),
                        passive = Card(J.Obj(cards, "passive")),
                        potential = ReadLines(J.Get(h, "potential")) ?? new PotLine[4],
                        potentialNew = ReadLines(J.Get(h, "potentialNew")),
                    };
                }
            foreach (var t in J.Arr(o, "team")) if (t is string id) s.team.Add(id);
            var rings = J.Arr(o, "rings");
            for (int i = 0; i < s.rings.Length && i < rings.Count; i++) s.rings[i] = (int)(double)rings[i];
            var zones = J.Obj(o, "zones");
            var chests = J.Obj(o, "zoneChests");
            for (int i = 0; i < 5; i++)
            {
                s.zones[i] = J.Int(zones, ElemKeys[i]);
                s.zoneChests[i] = J.Int(chests, ElemKeys[i]);
            }
            var clears = J.Obj(o, "clears");
            if (clears != null)
                foreach (var kv in clears)
                    if (int.TryParse(kv.Key, out var id) && kv.Value is double n) s.clears[id] = (int)n;
            var st = J.Obj(o, "settings");
            if (st != null)
            {
                s.settings.boil = J.Bool(st, "boil", true);
                s.settings.sound = J.Bool(st, "sound", true);
                s.settings.hints = J.Bool(st, "hints", true);
                s.settings.haptics = J.Bool(st, "haptics", true);
            }
            var stats = J.Obj(o, "stats");
            s.stats.battles = J.Int(stats, "battles");
            s.stats.wins = J.Int(stats, "wins");
            s.stats.dropped = J.Int(stats, "dropped");
            s.potentialStones = J.Int(o, "potentialStones");
            var cv = J.Obj(o, "cave");
            if (cv != null)
                s.cave = new CaveDay
                {
                    day = J.Int(cv, "day"), wins = J.Int(cv, "wins"),
                    pick = J.Str(cv, "pick") is string pk ? Keys.ToElem(pk) : (Elem?)null,
                };
            var fo = J.Obj(o, "farm");
            if (fo != null)
            {
                s.farm = new FarmState
                {
                    lastTick = J.Num(fo, "lastTick"), boostUntil = J.Num(fo, "boostUntil"),
                };
                foreach (var x in J.Arr(fo, "spots"))
                {
                    var sp = J.Obj(x);
                    s.farm.spots.Add(new FarmSpot { hero = J.Str(sp, "hero"), energy = J.Num(sp, "energy"), stock = J.Num(sp, "stock") });
                }
                var rest = J.Obj(fo, "rest");
                if (rest != null)
                    foreach (var kv in rest)
                        if (kv.Value is double ms) s.farm.rest[kv.Key] = ms;
            }
            var tro = J.Obj(o, "trees");
            if (tro != null)
            {
                s.trees = new TreeState { lastTick = J.Num(tro, "lastTick") };
                foreach (var x in J.Arr(tro, "stock")) if (x is double v) s.trees.stock.Add(v);
            }
            var ao = J.Obj(o, "ads");
            if (ao != null)
            {
                s.ads = new AdState { day = J.Int(ao, "day") };
                foreach (var kv in J.Obj(ao, "used") ?? new Dictionary<string, object>())
                    if (kv.Value is double n) s.ads.used[kv.Key] = (int)n;
            }
            var eo = J.Obj(o, "ent");
            if (eo != null) s.ent = new Entitlements { passUntil = J.Num(eo, "passUntil"), noAds = J.Bool(eo, "noAds") };
            var bd = J.Obj(o, "badges");
            for (int i = 0; i < 5; i++)
            {
                var b = J.Obj(bd, ElemKeys[i]);
                s.badges[i].tier = J.Int(b, "tier");
                s.badges[i].won = J.Int(b, "won");
            }
            var af = J.Obj(o, "afk");
            if (af == null) s.afk.lastTick = s.afkSince; // bản lưu trước mốc AFK: tính tiếp từ lần nhận trước
            else
            {
                s.afk.hours = J.Num(af, "hours");
                s.afk.lastTick = J.Num(af, "lastTick", s.afkSince);
                s.afk.boostUntil = J.Num(af, "boostUntil");
                s.afk.chestAcc = J.Num(af, "chestAcc");
                foreach (var t in J.Arr(af, "chests")) if (t is double ms) s.afk.chests.Add(ms);
                s.afk.chainAt = J.Num(af, "chainAt");
                s.afk.stage = J.Int(af, "stage");
            }
            foreach (var x in J.Arr(o, "chests"))
            {
                var c = J.Obj(x);
                if (c != null) s.chests.Add(new PendingChest { kind = J.Str(c, "kind"), x = J.Int(c, "x", 1) });
            }
            foreach (var kv in o) if (!Known.Contains(kv.Key)) s.extra[kv.Key] = kv.Value;
            return s;
        }

        static PotLine[] ReadLines(object v)
        {
            if (!(v is List<object> arr)) return null;
            var lines = new PotLine[4];
            for (int i = 0; i < 4 && i < arr.Count; i++)
                if (J.Obj(arr[i]) is Dictionary<string, object> x) lines[i] = new PotLine { k = Potential.FromKey(J.Str(x, "k")), r = J.Int(x, "r") };
            return lines;
        }

        static object WriteLines(PotLine[] lines) =>
            lines.Select(x => x == null ? null : (object)new Dictionary<string, object> { ["k"] = Potential.Key(x.k), ["r"] = x.r }).ToList();

        static CardProg Card(Dictionary<string, object> o) =>
            new CardProg { lv = Math.Max(1, J.Int(o, "lv", 1)), copies = J.Int(o, "copies") };

        static Dictionary<string, object> Card(CardProg c) =>
            new Dictionary<string, object> { ["lv"] = c.lv, ["copies"] = c.copies };

        public static string Write(SaveData s, bool pretty = false)
        {
            var heroes = new Dictionary<string, object>();
            foreach (var kv in s.heroes)
                heroes[kv.Key] = new Dictionary<string, object>
                {
                    ["owned"] = kv.Value.owned,
                    ["shards"] = kv.Value.shards,
                    ["star"] = kv.Value.star,
                    ["cards"] = new Dictionary<string, object>
                    {
                        ["skill"] = Card(kv.Value.skill), ["ult"] = Card(kv.Value.ult), ["passive"] = Card(kv.Value.passive),
                    },
                    ["potential"] = WriteLines(kv.Value.potential),
                };
            foreach (var kv in s.heroes)
                if (kv.Value.potentialNew != null) ((Dictionary<string, object>)heroes[kv.Key])["potentialNew"] = WriteLines(kv.Value.potentialNew);
            var zones = new Dictionary<string, object>();
            var chests = new Dictionary<string, object>();
            for (int i = 0; i < 5; i++)
            {
                zones[ElemKeys[i]] = s.zones[i];
                chests[ElemKeys[i]] = s.zoneChests[i];
            }
            var clears = new Dictionary<string, object>();
            foreach (var kv in s.clears) clears[kv.Key.ToString()] = kv.Value;
            var o = new Dictionary<string, object>
            {
                ["v"] = s.v,
                ["level"] = s.level,
                ["exp"] = s.exp,
                ["balls"] = s.balls,
                ["ballsSpent"] = s.ballsSpent,
                ["legendDone"] = s.legendDone,
                ["gift"] = s.gift,
                ["giftTier"] = s.giftTier,
                ["rings"] = s.rings.Select(x => (object)x).ToList(),
                ["heroes"] = heroes,
                ["team"] = s.team.Cast<object>().ToList(),
                ["zones"] = zones,
                ["zoneChests"] = chests,
                ["clears"] = clears,
                ["afkSince"] = s.afkSince,
                ["potentialStones"] = s.potentialStones,
                ["badges"] = Enumerable.Range(0, 5).ToDictionary(i => ElemKeys[i], i => (object)new Dictionary<string, object>
                {
                    ["tier"] = s.badges[i].tier, ["won"] = s.badges[i].won,
                }),
                ["afk"] = new Dictionary<string, object>
                {
                    ["hours"] = s.afk.hours, ["lastTick"] = s.afk.lastTick, ["boostUntil"] = s.afk.boostUntil, ["chestAcc"] = s.afk.chestAcc,
                    ["chests"] = s.afk.chests.Cast<object>().ToList(), ["chainAt"] = s.afk.chainAt, ["stage"] = s.afk.stage,
                },
                ["settings"] = new Dictionary<string, object>
                {
                    ["boil"] = s.settings.boil, ["sound"] = s.settings.sound, ["hints"] = s.settings.hints,
                    ["haptics"] = s.settings.haptics,
                },
                ["stats"] = new Dictionary<string, object>
                {
                    ["battles"] = s.stats.battles, ["wins"] = s.stats.wins, ["dropped"] = s.stats.dropped,
                },
                ["intro"] = s.intro,
            };
            if (s.starter != null) o["starter"] = s.starter;
            if (s.trees != null)
                o["trees"] = new Dictionary<string, object> { ["lastTick"] = s.trees.lastTick, ["stock"] = s.trees.stock.Cast<object>().ToList() };
            if (s.ads != null)
                o["ads"] = new Dictionary<string, object> { ["day"] = s.ads.day, ["used"] = s.ads.used.ToDictionary(kv => kv.Key, kv => (object)kv.Value) };
            if (s.ent != null)
                o["ent"] = new Dictionary<string, object> { ["passUntil"] = s.ent.passUntil, ["noAds"] = s.ent.noAds };
            if (s.farm != null)
                o["farm"] = new Dictionary<string, object>
                {
                    ["lastTick"] = s.farm.lastTick, ["boostUntil"] = s.farm.boostUntil,
                    ["spots"] = s.farm.spots.Select(sp => (object)new Dictionary<string, object>
                    {
                        ["hero"] = sp.hero, ["energy"] = sp.energy, ["stock"] = sp.stock,
                    }).ToList(),
                    ["rest"] = s.farm.rest.ToDictionary(kv => kv.Key, kv => (object)kv.Value),
                };
            if (s.cave != null)
                o["cave"] = new Dictionary<string, object>
                {
                    ["day"] = s.cave.day, ["wins"] = s.cave.wins, ["pick"] = s.cave.pick is Elem pe ? Keys.Of(pe) : null,
                };
            if (s.chests.Count > 0)
                o["chests"] = s.chests.Select(c => (object)new Dictionary<string, object> { ["kind"] = c.kind, ["x"] = c.x }).ToList();
            foreach (var kv in s.extra) if (!o.ContainsKey(kv.Key)) o[kv.Key] = kv.Value;
            return MiniJson.Write(o, pretty);
        }
    }
}
