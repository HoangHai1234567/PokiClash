// Đảo Casino (GD_Claude/29_DaoCasino.md, 2026-11-25): luật chung của đảo. Từng trò ở Core/Casino/*.cs.
// - Đảo mở ở cấp openLevel; mỗi trò mở theo cấp (và số tướng) trong casino.unlocks.
// - Lều may rủi (Blackjack, Roulette, Slot) mở theo lịch sự kiện: vòng lặp tính từ ngày mốc, hoặc ngày cố định. Hết giờ là đóng thật.
// - Cược bằng bi. Bậc cược nhân theo bậc cấp như gói bi (ShopConfig.Band). Trần ván có thưởng mỗi ngày.
// - Hũ bàn: mỗi bi đã cược (quy về bi gốc, thắng hay thua) đổ vào hũ của bàn; sức chứa = jarBets × cược gốc của bậc cao nhất đã dùng từ
//   lần hũ trước; đầy thì trao rương theo bậc đó (bậc cao có mảnh tướng khách mời).
// - Mọi kết quả ngẫu nhiên đi qua Rng có hạt giống; ngày là Afk.Today (giờ máy, 0 giờ địa phương).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class CasinoJar
    {
        public double fill; // bi gốc đã đổ
        public int tier = -1; // bậc cao nhất đã dùng từ lần hũ trước
    }

    public sealed class FishRec
    {
        public int n;
        public double best; // cỡ lớn nhất (cm)
    }

    public sealed class CaughtFish
    {
        public string id;
        public double size;
    }

    public sealed class CasinoState
    {
        public bool intro; // đã xem truyện mở đảo
        public List<string> seen = new List<string>(); // "open:<trò>" đã báo mở, "howto:<trò>" đã xem hướng dẫn, "ev:<sự kiện>#<lần>" đã báo
        public int day = -1; // ngày của các đếm theo ngày
        public Dictionary<string, int> plays = new Dictionary<string, int>(); // lượt có thưởng hôm nay theo trò
        public int betToday, wonToday;
        public double betAll, wonAll;
        public Dictionary<string, CasinoJar> jars = new Dictionary<string, CasinoJar>();
        public int luckyDay = -1; // ngày đã lật Bói sao
        // câu cá
        public int freeBaitUsed, bait, rod = 1;
        public Dictionary<string, FishRec> dex = new Dictionary<string, FishRec>();
        public List<CaughtFish> creel = new List<CaughtFish>(); // cá chưa bán
        public List<string> sets = new List<string>(); // hệ đã nhận quà đủ 6 loài
        public int kingWeek = -1; // tuần đã bắt Cá Vua
        // đua
        public int raceWeek = -1;
        public int[] cupPts = new int[0];
        public int cupClaimed; // bit theo hạng: đã nhận quà tuần
        // chợ đen
        public int mkStamp = -1; // lượt hàng (ngày × số mốc giờ + mốc)
        public int mkRoll; // số lần làm mới trong lượt (đổi hạt giống)
        public int mkRefreshDay = -1, mkRefresh; // lần làm mới đã trả trong ngày
        public List<int> mkBought = new List<int>(); // ô đã mua trong lượt hàng
        public int spareStones; // đá tiềm năng đã đổi từ thẻ thừa hôm nay (trần MarketConfig.stoneDaily)
        // đấu trường ngầm
        public int ugWon; // bit theo bậc: đã thắng hôm nay
        public int ugChampWeek = -1;
        // quán trọ
        public List<string> inn = new List<string>(); // nhiệm vụ hôm nay
        public Dictionary<string, int> innProg = new Dictionary<string, int>();
        public List<string> innClaimed = new List<string>();
        public bool innAll;

        public int Play(string k) => plays.TryGetValue(k, out var n) ? n : 0;

        public CasinoJar Jar(string table) => jars.TryGetValue(table, out var j) ? j : jars[table] = new CasinoJar();

        public static CasinoState Read(Dictionary<string, object> o)
        {
            if (o == null) return null;
            var s = new CasinoState
            {
                intro = J.Bool(o, "intro"), day = J.Int(o, "day", -1), betToday = J.Int(o, "betToday"), wonToday = J.Int(o, "wonToday"),
                betAll = J.Num(o, "betAll"), wonAll = J.Num(o, "wonAll"), luckyDay = J.Int(o, "luckyDay", -1),
                freeBaitUsed = J.Int(o, "freeBait"), bait = J.Int(o, "bait"), rod = Math.Max(1, J.Int(o, "rod", 1)), kingWeek = J.Int(o, "kingWeek", -1),
                raceWeek = J.Int(o, "raceWeek", -1), cupClaimed = J.Int(o, "cupClaimed"),
                mkStamp = J.Int(o, "mkStamp", -1), mkRoll = J.Int(o, "mkRoll"), mkRefreshDay = J.Int(o, "mkRefreshDay", -1), mkRefresh = J.Int(o, "mkRefresh"),
                ugWon = J.Int(o, "ugWon"), ugChampWeek = J.Int(o, "ugChampWeek", -1), innAll = J.Bool(o, "innAll"), spareStones = J.Int(o, "spareStones"),
            };
            foreach (var x in J.Arr(o, "seen")) if (x is string t) s.seen.Add(t);
            foreach (var kv in J.Obj(o, "plays") ?? new Dictionary<string, object>()) if (kv.Value is double n) s.plays[kv.Key] = (int)n;
            foreach (var kv in J.Obj(o, "jars") ?? new Dictionary<string, object>())
            {
                var jo = J.Obj(kv.Value);
                if (jo != null) s.jars[kv.Key] = new CasinoJar { fill = J.Num(jo, "fill"), tier = J.Int(jo, "tier", -1) };
            }
            foreach (var kv in J.Obj(o, "dex") ?? new Dictionary<string, object>())
            {
                var fo = J.Obj(kv.Value);
                if (fo != null) s.dex[kv.Key] = new FishRec { n = J.Int(fo, "n"), best = J.Num(fo, "best") };
            }
            foreach (var x in J.Arr(o, "creel"))
            {
                var c = J.Obj(x);
                if (c != null) s.creel.Add(new CaughtFish { id = J.Str(c, "id"), size = J.Num(c, "size") });
            }
            foreach (var x in J.Arr(o, "sets")) if (x is string t) s.sets.Add(t);
            s.cupPts = J.Arr(o, "cupPts").Select(x => x is double v ? (int)v : 0).ToArray();
            foreach (var x in J.Arr(o, "mkBought")) if (x is double v) s.mkBought.Add((int)v);
            foreach (var x in J.Arr(o, "inn")) if (x is string t) s.inn.Add(t);
            foreach (var kv in J.Obj(o, "innProg") ?? new Dictionary<string, object>()) if (kv.Value is double n) s.innProg[kv.Key] = (int)n;
            foreach (var x in J.Arr(o, "innClaimed")) if (x is string t) s.innClaimed.Add(t);
            return s;
        }

        public Dictionary<string, object> Write() => new Dictionary<string, object>
        {
            ["intro"] = intro, ["seen"] = seen.Cast<object>().ToList(), ["day"] = (double)day,
            ["plays"] = plays.ToDictionary(kv => kv.Key, kv => (object)(double)kv.Value),
            ["betToday"] = (double)betToday, ["wonToday"] = (double)wonToday, ["betAll"] = betAll, ["wonAll"] = wonAll,
            ["jars"] = jars.ToDictionary(kv => kv.Key, kv => (object)new Dictionary<string, object> { ["fill"] = kv.Value.fill, ["tier"] = (double)kv.Value.tier }),
            ["luckyDay"] = (double)luckyDay,
            ["freeBait"] = (double)freeBaitUsed, ["bait"] = (double)bait, ["rod"] = (double)rod,
            ["dex"] = dex.ToDictionary(kv => kv.Key, kv => (object)new Dictionary<string, object> { ["n"] = (double)kv.Value.n, ["best"] = kv.Value.best }),
            ["creel"] = creel.Select(c => (object)new Dictionary<string, object> { ["id"] = c.id, ["size"] = c.size }).ToList(),
            ["sets"] = sets.Cast<object>().ToList(), ["kingWeek"] = (double)kingWeek,
            ["raceWeek"] = (double)raceWeek, ["cupPts"] = cupPts.Select(x => (object)(double)x).ToList(), ["cupClaimed"] = (double)cupClaimed,
            ["mkStamp"] = (double)mkStamp, ["mkRoll"] = (double)mkRoll, ["mkRefreshDay"] = (double)mkRefreshDay, ["mkRefresh"] = (double)mkRefresh,
            ["mkBought"] = mkBought.Select(x => (object)(double)x).ToList(),
            ["ugWon"] = (double)ugWon, ["ugChampWeek"] = (double)ugChampWeek,
            ["inn"] = inn.Cast<object>().ToList(), ["innProg"] = innProg.ToDictionary(kv => kv.Key, kv => (object)(double)kv.Value),
            ["innClaimed"] = innClaimed.Cast<object>().ToList(), ["innAll"] = innAll, ["spareStones"] = (double)spareStones,
        };
    }

    // một lần mở của sự kiện: [startDay, endDay] gồm cả hai đầu (ngày Afk.Today)
    public sealed class CasinoSpan
    {
        public CasinoEvent ev;
        public int occ; // lần mở thứ mấy (vòng lặp); ngày cố định: 0
        public int startDay, endDay;
        public string Key => ev.id + "#" + occ;
    }

    // chế độ một ván ở bàn may rủi: có cược; ván đầu miễn phí (không trả cược, thắng nhận phần lời); ván tập (hết lượt có thưởng)
    public enum TableMode { Paid, Free, Practice }

    public sealed class JarResult
    {
        public bool full;
        public int tier;
        public List<Reward> rewards = new List<Reward>();
    }

    public static class Casino
    {
        public const string Blackjack = "blackjack", Roulette = "roulette", Slot = "slot", Race = "race";
        public const string Fishing = "fishing", Inn = "inn", Booths = "booths", Market = "market", Underground = "underground";
        public const string Bait = "bait";
        public const double Day = 86400000;

        public static CasinoConfig C(GameData d) => d.Cfg.casino;
        public static CasinoState Of(SaveData s) => s.casino ?? (s.casino = new CasinoState());

        // ---------- mở ----------

        public static bool Open(SaveData s, GameData d) => C(d).unlocks.Count > 0 && s.level >= C(d).openLevel;

        public static int OwnedHeroes(SaveData s) => s.heroes.Count(kv => kv.Value.owned);

        // Mở hết lều (không lưu): coi như cả ba lều may rủi đang dựng hôm nay và mục lều đã mở (bỏ mốc cấp). Lịch thật không đổi.
        // Mặc định tắt (test, lõi); App.cs bật lúc mở game khi CHƯA PHÁT HÀNH (người dùng 2026-11-26). Editor/CasinoTestBooths.cs tắt lại khi
        // về Edit mode (Play tắt Reload Domain nên biến tĩnh còn nguyên sau Play) để EditMode test chạy theo lịch thật.
        public static bool TestAllBooths;

        public static bool Unlocked(SaveData s, GameData d, string id)
        {
            if (!Open(s, d)) return false;
            if (TestAllBooths && id == Booths) return true;
            var u = C(d).Unlock(id);
            return u == null || (s.level >= u.level && OwnedHeroes(s) >= u.heroes);
        }

        // chữ điều kiện mở của trò (rỗng nếu đã mở)
        public static string Need(SaveData s, GameData d, string id)
        {
            if (Unlocked(s, d, id)) return "";
            var u = C(d).Unlock(id);
            int lv = u?.level ?? C(d).openLevel;
            if (u != null && u.heroes > 0 && s.level >= lv) return Loc.F("Cần {0} tướng để mở", u.heroes);
            return Loc.F("Mở ở cấp {0}", Math.Max(lv, C(d).openLevel));
        }

        // trò vừa mở mà chưa báo (đánh dấu đã báo khi gọi MarkSeen)
        public static List<string> NewlyOpen(SaveData s, GameData d) =>
            C(d).unlocks.Where(u => Unlocked(s, d, u.id) && !Of(s).seen.Contains("open:" + u.id)).Select(u => u.id).ToList();

        public static void MarkSeen(SaveData s, string key)
        {
            var st = Of(s);
            if (!st.seen.Contains(key)) st.seen.Add(key);
        }

        // ---------- ngày, giờ ----------

        public static int Today(double now) => Afk.Today(now);
        public static int Week(int day) => Shop.Week(day);

        public static double Hour(double now)
        {
            var off = TimeZoneInfo.Local.GetUtcOffset(DateTimeOffset.FromUnixTimeMilliseconds((long)now).UtcDateTime).TotalMinutes;
            double ms = (now + off * 60000) % Day;
            if (ms < 0) ms += Day;
            return ms / 3600000.0;
        }

        public static bool Night(double now)
        {
            double h = Hour(now);
            return h >= 19 || h < 5;
        }

        // sang ngày mới thì xoá các đếm theo ngày (gọi đầu mọi thao tác)
        public static CasinoState Roll(SaveData s, GameData d, double now)
        {
            var st = Of(s);
            int day = Today(now);
            if (st.day == day) return st;
            st.day = day;
            st.plays.Clear();
            st.betToday = st.wonToday = 0;
            st.freeBaitUsed = 0;
            st.ugWon = 0;
            st.spareStones = 0;
            st.inn.Clear();
            st.innProg.Clear();
            st.innClaimed.Clear();
            st.innAll = false;
            PickInn(s, d, day);
            return st;
        }

        // ---------- lượt có thưởng ----------

        public static int Daily(GameData d, string game)
        {
            var c = C(d);
            switch (game)
            {
                case Blackjack: return c.blackjack.daily;
                case Roulette: return c.roulette.daily;
                case Slot: return c.slots.daily;
                case Race: return c.race.daily;
                case Underground: return c.underground.daily;
                default: return int.MaxValue;
            }
        }

        public static int PlaysLeft(SaveData s, GameData d, string game, double now) =>
            Math.Max(0, Daily(d, game) - Roll(s, d, now).Play(game));

        public static void UsePlay(SaveData s, GameData d, string game, double now)
        {
            var st = Roll(s, d, now);
            st.plays[game] = st.Play(game) + 1;
        }

        // ---------- bậc cược ----------

        public static double Band(SaveData s, GameData d) => d.Cfg.shop.Band(s.level);

        public static int Bet(SaveData s, GameData d, CasinoTable t, int tier) =>
            tier < 0 || tier >= t.bets.Length ? 0 : Shop.RoundBalls(t.bets[tier] * Band(s, d));

        public static bool BetOpen(SaveData s, CasinoTable t, int tier) => tier >= 0 && tier < t.betLevel.Length && s.level >= t.betLevel[tier];

        public static int BetLevel(CasinoTable t, int tier) => tier >= 0 && tier < t.betLevel.Length ? t.betLevel[tier] : 0;

        // ---------- bi ----------

        // trả bi cược (false nếu thiếu); ghi thống kê
        public static bool Stake(SaveData s, GameData d, int n, double now)
        {
            if (n <= 0 || s.balls < n) return false;
            var st = Roll(s, d, now);
            s.balls -= n;
            st.betToday += n;
            st.betAll += n;
            return true;
        }

        // trả lại bi cược (hoà, ván tập bị huỷ)
        public static void Refund(SaveData s, GameData d, int n, double now)
        {
            if (n <= 0) return;
            var st = Roll(s, d, now);
            s.balls += n;
            st.betToday -= n;
            st.betAll -= n;
        }

        public static void Win(SaveData s, GameData d, int n, double now)
        {
            if (n <= 0) return;
            var st = Roll(s, d, now);
            s.balls += n;
            st.wonToday += n;
            st.wonAll += n;
        }

        // trả bi không tính là cược (mồi, cần câu, làm mới chợ, mua chợ, lệ phí)
        public static bool Spend(SaveData s, int n)
        {
            if (n < 0 || s.balls < n) return false;
            s.balls -= n;
            return true;
        }

        // ---------- Hũ bàn ----------

        public static double JarCap(CasinoTable t, int tier) => tier < 0 || tier >= t.bets.Length ? 0 : t.jarBets * t.bets[tier];

        // đổ bi đã cược vào hũ; đầy thì trao rương theo bậc cao nhất đã dùng, phần dư giữ lại
        public static JarResult Pour(SaveData s, GameData d, string table, int tier, int amount, double now, Rng rng)
        {
            var t = C(d).Table(table);
            var res = new JarResult();
            if (t == null || amount <= 0) return res;
            var jar = Roll(s, d, now).Jar(table);
            jar.tier = Math.Max(jar.tier, Math.Min(tier, t.bets.Length - 1));
            jar.fill += amount / Math.Max(1e-9, Band(s, d));
            double cap = JarCap(t, jar.tier);
            if (cap <= 0 || jar.fill < cap) return res;
            res.full = true;
            res.tier = jar.tier;
            jar.fill = Math.Min(jar.fill - cap, cap * 0.5);
            if (jar.tier < t.jar.Count) res.rewards = Grant(s, d, t.jar[jar.tier].items, now, rng, GuestOf(d, table, now));
            jar.tier = tier;
            return res;
        }

        public static double JarFrac(SaveData s, GameData d, string table, double now)
        {
            var t = C(d).Table(table);
            var jar = Roll(s, d, now).Jar(table);
            double cap = JarCap(t, Math.Max(0, jar.tier));
            return cap <= 0 ? 0 : Math.Min(1, jar.fill / cap);
        }

        // ---------- sự kiện ----------

        public static int Anchor(GameData d) => Math.Max(0, CasinoConfig.Days(C(d).anchor));

        // lần mở của sự kiện chứa ngày day, hoặc null
        public static CasinoSpan SpanAt(GameData d, CasinoEvent e, int day)
        {
            if (!string.IsNullOrEmpty(e.start))
            {
                int a = CasinoConfig.Days(e.start), b = CasinoConfig.Days(e.end);
                return day >= a && day <= b ? new CasinoSpan { ev = e, occ = 0, startDay = a, endDay = b } : null;
            }
            if (e.period <= 0) return null;
            int rel = day - Anchor(d) - e.offset;
            int occ = (int)Math.Floor(rel / (double)e.period);
            int pos = rel - occ * e.period;
            if (pos >= e.length) return null;
            int start = day - pos;
            return new CasinoSpan { ev = e, occ = occ, startDay = start, endDay = start + e.length - 1 };
        }

        // lần mở kế tiếp bắt đầu sau ngày day (tìm trong 60 ngày)
        public static CasinoSpan NextSpan(GameData d, CasinoEvent e, int day)
        {
            for (int k = 1; k <= 60; k++)
            {
                var sp = SpanAt(d, e, day + k);
                if (sp != null && sp.startDay == day + k) return sp;
            }
            return null;
        }

        // sự kiện đang mở (ngày cố định đè vòng lặp cùng lều)
        public static List<CasinoSpan> Active(GameData d, int day)
        {
            var all = C(d).events.Select(e => SpanAt(d, e, day)).Where(sp => sp != null).ToList();
            var fixedBooths = new HashSet<string>(all.Where(sp => !string.IsNullOrEmpty(sp.ev.start)).Select(sp => sp.ev.booth));
            var res = all.Where(sp => !string.IsNullOrEmpty(sp.ev.start) || !fixedBooths.Contains(sp.ev.booth)).ToList();
            if (TestAllBooths)
                foreach (var booth in new[] { Blackjack, Roulette, Slot })
                {
                    if (res.Any(sp => sp.ev.booth == booth)) continue;
                    var e = C(d).events.FirstOrDefault(x => x.booth == booth);
                    if (e == null) continue;
                    // lần mở kế tiếp của chính sự kiện đó (khách mời trùng lần thật), chỉ kéo dài hôm nay
                    var next = NextSpan(d, e, day);
                    res.Add(new CasinoSpan { ev = e, occ = next?.occ ?? 0, startDay = day, endDay = day });
                }
            return res;
        }

        public static List<CasinoSpan> Active(GameData d, double now) => Active(d, Today(now));

        // n sự kiện sắp mở (chưa mở hôm nay), theo ngày bắt đầu
        public static List<CasinoSpan> Upcoming(GameData d, double now, int n)
        {
            int day = Today(now);
            return C(d).events.Select(e => NextSpan(d, e, day)).Where(sp => sp != null).OrderBy(sp => sp.startDay).Take(n).ToList();
        }

        public static CasinoSpan Booth(GameData d, string booth, double now) => Active(d, now).FirstOrDefault(sp => sp.ev.booth == booth);

        // lều may rủi đang mở cho người chơi này (đã mở mục lều theo cấp, vùng không tắt lều)
        public static bool BoothOpen(SaveData s, GameData d, string booth, double now) =>
            Unlocked(s, d, Booths) && TablesAllowed(d) && Booth(d, booth, now) != null;

        // ---------- vùng, chế độ bàn ----------

        // mã nước 2 chữ của máy (App đặt lúc mở game theo cài đặt vùng; rỗng: không biết, không chặn)
        public static string Region = "";

        // lều may rủi được mở ở vùng này (casino.tablesBlock)
        public static bool TablesAllowed(GameData d) =>
            string.IsNullOrEmpty(Region) || Array.IndexOf(C(d).tablesBlock, Region.Trim().ToUpperInvariant()) < 0;

        // ván đầu ở mỗi bàn may rủi không mất bi (mục 12): chưa chơi ván miễn phí của bàn này
        public static bool FreeFirst(SaveData s, string game) => !Of(s).seen.Contains("free:" + game);

        // chế độ ván kế: ván đầu miễn phí, hết lượt có thưởng thì ván tập (không cược, không thưởng, mục 6 / câu 8), còn lại có cược
        public static TableMode ModeOf(SaveData s, GameData d, string game, double now) =>
            FreeFirst(s, game) ? TableMode.Free : PlaysLeft(s, d, game, now) <= 0 ? TableMode.Practice : TableMode.Paid;

        // ván miễn phí thắng thì nhận phần lời (không hoàn cược vì không trả cược), thua không mất gì
        public static int FreeWin(int payout, int staked) => Math.Max(0, payout - staked);

        // mili giây còn lại tới hết ngày cuối của lần mở
        public static double Left(CasinoSpan sp, double now)
        {
            int day = Today(now);
            double startOfToday = now - Hour(now) * 3600000.0;
            return Math.Max(0, startOfToday + (sp.endDay - day + 1) * Day - now);
        }

        // tướng khách mời: cố định trong dữ liệu, hoặc chọn theo lần mở trong bể Hiếm / Sử thi (như gói tướng tuần)
        public static string Guest(GameData d, CasinoSpan sp)
        {
            if (sp == null) return null;
            if (!string.IsNullOrEmpty(sp.ev.guest)) return sp.ev.guest;
            var pool = d.Heroes.Where(h => !h.minion && (h.rarity == Rarity.Rare || h.rarity == Rarity.Epic)).Select(h => h.id)
                .OrderBy(x => x, StringComparer.Ordinal).ToList();
            if (pool.Count == 0) return null;
            uint seed = 2166136261;
            foreach (char ch in sp.ev.id) seed = (seed ^ ch) * 16777619;
            var rng = new Rng(seed ^ (uint)(sp.occ * 7919 + 13));
            return rng.Pick(pool);
        }

        // khách mời của lều đang mở (mảnh trong Hũ bàn, Sao Vàng, huy hiệu máy quả)
        public static string GuestOf(GameData d, string booth, double now) => Guest(d, Booth(d, booth, now));

        public static double RaceMult(GameData d, double now) => Booth(d, "race_fest", now)?.ev.mult ?? 1;

        // ---------- trao thưởng ----------

        // trao món của đảo; "*guest" lấy khách mời của lều đang mở (không có thì khách mời của sự kiện sắp tới / tướng gánh đội);
        // "*elem:<hệ>" là tướng ngẫu nhiên của hệ đó (ưu tiên tướng đã có); scale: bi nhân bậc cấp
        public static List<Reward> Grant(SaveData s, GameData d, List<CasinoItem> items, double now, Rng rng, string guest = null, bool scale = true)
        {
            var outL = new List<Reward>();
            var shop = new List<ShopItem>();
            foreach (var it in items)
            {
                if (it == null || (it.chance < 1 && !rng.Chance(it.chance))) continue;
                if (it.k == Bait)
                {
                    Of(s).bait += it.n;
                    outL.Add(new Reward { k = RewardKind.Bait, n = it.n, id = Bait });
                    continue;
                }
                var x = it.ToShop();
                if (x.h == "*guest") x.h = guest ?? AnyGuest(d, now) ?? "*carry";
                else if (x.h != null && x.h.StartsWith("*elem:")) x.h = HeroOfElem(s, d, Keys.ToElem(x.h.Substring(6)), rng);
                shop.Add(x);
            }
            if (shop.Count > 0) outL.AddRange(Shop.Grant(s, d, Shop.Resolve(s, d, shop, scale, null), now, rng));
            return outL;
        }

        static string AnyGuest(GameData d, double now)
        {
            var sp = Active(d, now).FirstOrDefault(x => x.ev.booth != "race_fest") ?? Upcoming(d, now, 1).FirstOrDefault();
            return Guest(d, sp);
        }

        // tướng của hệ e: ưu tiên tướng đã có còn lên được sao, rồi tướng chưa có
        public static string HeroOfElem(SaveData s, GameData d, Elem e, Rng rng)
        {
            var all = d.Heroes.Where(h => !h.minion && h.elem == e).ToList();
            var owned = all.Where(h => s.Hero(h.id)?.owned == true && s.Hero(h.id).star < StarTier.MaxStar).ToList();
            var pick = owned.Count > 0 ? owned : all;
            return pick.Count == 0 ? null : rng.Pick(pick).id;
        }

        // ---------- Bói sao ----------

        // hệ may mắn của ngày (cố định theo ngày, ai cũng như nhau)
        public static Elem Lucky(double now)
        {
            var rng = new Rng((uint)(Today(now) * 2654435761u + 97));
            return Elements.All[rng.Int(0, Elements.All.Length - 1)];
        }

        public static bool LuckyFlipped(SaveData s, double now) => Of(s).luckyDay == Today(now);

        public static Elem FlipLucky(SaveData s, double now)
        {
            Of(s).luckyDay = Today(now);
            return Lucky(now);
        }

        // hệ may mắn đang có tác dụng (chỉ khi đã lật hôm nay)
        public static Elem? LuckyActive(SaveData s, double now) => LuckyFlipped(s, now) ? Lucky(now) : (Elem?)null;

        // ---------- quán trọ ----------

        static void PickInn(SaveData s, GameData d, int day)
        {
            var st = Of(s);
            var inn = C(d).inn;
            // việc ở lều lữ khách chỉ ra vào ngày có lều may rủi đang mở (ngày nghỉ của lịch không làm được)
            bool tables = TablesAllowed(d) && Active(d, day).Any(sp => C(d).Table(sp.ev.booth) != null);
            var pool = inn.quests.Where(q => (string.IsNullOrEmpty(q.need) || Unlocked(s, d, q.need)) && (q.kind != "table" || tables)).ToList();
            var rng = new Rng((uint)(day * 40503 + 11));
            while (st.inn.Count < inn.count && pool.Count > 0)
            {
                var q = rng.Pick(pool);
                pool.Remove(q);
                st.inn.Add(q.id);
            }
        }

        public static List<InnQuest> InnToday(SaveData s, GameData d, double now)
        {
            var st = Roll(s, d, now);
            if (st.inn.Count == 0) PickInn(s, d, st.day); // mở quán giữa ngày
            return st.inn.Select(id => C(d).inn.quests.Find(q => q.id == id)).Where(q => q != null).ToList();
        }

        public static int InnProg(SaveData s, string id) => Of(s).innProg.TryGetValue(id, out var n) ? n : 0;

        // ghi tiến độ cho mọi nhiệm vụ hôm nay cùng loại
        public static void Track(SaveData s, GameData d, string kind, int n, double now)
        {
            if (!Open(s, d) || n <= 0) return;
            foreach (var q in InnToday(s, d, now))
                if (q.kind == kind) Of(s).innProg[q.id] = Math.Min(q.n, InnProg(s, q.id) + n);
        }

        public static bool QuestDone(SaveData s, InnQuest q) => InnProg(s, q.id) >= q.n;

        public static List<Reward> ClaimQuest(SaveData s, GameData d, string id, double now, Rng rng)
        {
            var st = Roll(s, d, now);
            var q = InnToday(s, d, now).Find(x => x.id == id);
            if (q == null || !QuestDone(s, q) || st.innClaimed.Contains(id)) return new List<Reward>();
            st.innClaimed.Add(id);
            return Grant(s, d, q.items, now, rng);
        }

        public static bool InnAllReady(SaveData s, GameData d, double now)
        {
            var st = Roll(s, d, now);
            var qs = InnToday(s, d, now);
            return !st.innAll && qs.Count > 0 && qs.All(q => st.innClaimed.Contains(q.id));
        }

        public static List<Reward> ClaimInnAll(SaveData s, GameData d, double now, Rng rng)
        {
            if (!InnAllReady(s, d, now)) return new List<Reward>();
            Of(s).innAll = true;
            return Grant(s, d, C(d).inn.all, now, rng);
        }

        // ---------- chấm đỏ ----------

        // có việc chờ trên đảo: trò mới mở, sự kiện mới chưa xem, nhiệm vụ xong chưa nhận, chưa lật Bói sao, còn mồi miễn phí
        public static bool Alert(SaveData s, GameData d, double now)
        {
            if (!Open(s, d)) return false;
            var st = Roll(s, d, now);
            if (NewlyOpen(s, d).Count > 0) return true;
            if (Unlocked(s, d, Booths) && Active(d, now).Any(sp => !st.seen.Contains("ev:" + sp.Key))) return true;
            if (Unlocked(s, d, Inn) && (InnToday(s, d, now).Any(q => QuestDone(s, q) && !st.innClaimed.Contains(q.id)) || InnAllReady(s, d, now))) return true;
            return false;
        }
    }
}
