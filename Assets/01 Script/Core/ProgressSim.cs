// Mô phỏng tiến độ: N ngày theo các kiểu người chơi (chăm, vừa, ít). Mỗi lần vào game:
//   1. nhận AFK (×2 nếu xem quảng cáo), mở rương AFK tới giờ (và "Mở ngay" nếu xem quảng cáo); đặt đội AFK ở ải rơi mảnh của tướng
//      chủ lực khi nó đang thiếu mảnh lên sao (2026-11-17: mảnh dồn để lên sao, người chơi chọn "AFK ải này"), còn lại để AFK tự chọn
//      ải xa nhất có rơi mảnh (gom mảnh mở khoá tướng mới);
//   2. đánh ải kế tiếp của đảo gợi ý (đảo có ải kế cấp thấp nhất); tỉ lệ thắng = máy tự chơi (đội và cấp thật lúc đó) + mức "người giỏi hơn máy";
//      ải kế quá khó (< 30%) thì đánh lại ải đã qua nhiều bi nhất mà gần chắc thắng;
//   3. thả hết bi (ô rơi theo tỉ lệ đo của máy, ×1), mở rương máy bi và rương mốc quà, nhận rương mốc đảo;
//   4. nâng thẻ, lên sao bằng mảnh, tiến hóa bằng đá (đá dồn cho tướng mạnh nhất trước: người chơi nuôi đội chủ lực);
//   5. rời game thì bật tăng tốc AFK (nếu xem quảng cáo).
// Có trang trại (thu hoạch, đổi ca, tự xếp mỗi lần vào). Huy hiệu và tiềm năng chưa mô phỏng (cần chơi tay); đá tiến hóa của Đền Huy
// Hiệu và Hang Tiềm Năng cộng gần đúng theo cấp (SideEvo).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class PlayerProfile
    {
        public string name;
        public int sessions; // lần vào game mỗi ngày (rải đều 8 giờ – 23 giờ)
        public int battles; // trận mỗi lần
        public bool ads; // có xem quảng cáo thưởng không
        public double skill = 0.15; // người giỏi hơn máy bao nhiêu (cộng vào tỉ lệ thắng)

        public PlayerProfile Copy() => (PlayerProfile)MemberwiseClone();
    }

    public sealed class ProgressReport
    {
        public PlayerProfile profile;
        public int days;
        public int[] level; // cấp cuối mỗi ngày, [0] = lúc mới chơi
        public int[] cleared; // tổng số ải đã qua cuối mỗi ngày
        public int[] zoneDay = new int[5]; // ngày chinh phục từng đảo (theo Elem), -1 = chưa
        public int[] zoneLevelDay = new int[5]; // ngày đạt cấp boss cuối đảo (levelMax; đảo song song đều bắt đầu từ cấp 1), -1 = chưa
        public int battles, wins, replays, ballsDropped, ballsFromStages, ballsFromTrees, ballsFromFarm, afkChests, cardUps, evolves;
        public int starUps, evoStones, evoSide; // lần lên sao bằng mảnh; tổng đá tiến hóa kiếm được (evolves: lần tiến hóa sang bậc sau),
                                                 // trong đó đá của Đền Huy Hiệu, Hang Tiềm Năng (SideEvo)
    }

    public static class ProgressSim
    {
        // Sổ Phép (2026-11-24): người chơi ảo vẽ theo đường gợi ý sau khi tiến hóa (tiến hóa được ưu tiên đá). Tắt để so nhịp có / không sổ
        public static bool SoPhepOn = true;

        const double H = 3600000;

        // giá trị khởi điểm (design.md, câu hỏi còn mở)
        public static PlayerProfile[] DefaultProfiles() => new[]
        {
            new PlayerProfile { name = "Chăm", sessions = 6, battles = 5, ads = true },
            new PlayerProfile { name = "Vừa", sessions = 3, battles = 3, ads = true },
            new PlayerProfile { name = "Ít", sessions = 1, battles = 2, ads = false },
        };

        // cache: tỉ lệ thắng của máy theo (ải, cấp, đội); dùng chung giữa các kiểu người chơi để chạy nhanh
        // starter: tướng khởi đầu đã chọn (null = tướng đầu danh sách)
        public static ProgressReport Run(GameData d, PlayerProfile p, int days = 30, uint seed = 1, int simN = 8,
            Dictionary<string, double> cache = null, Action<int> onDay = null, string starter = null, Action<int, SaveData> onDaySave = null)
        {
            cache = cache ?? new Dictionary<string, double>();
            var s = starter != null ? SaveData.New(d, 0, starter) : SaveData.New(d, 0);
            s.intro = true;
            var rng = new Rng(seed);
            var rep = new ProgressReport { profile = p, days = days, level = new int[days + 1], cleared = new int[days + 1] };
            for (int z = 0; z < 5; z++) rep.zoneDay[z] = rep.zoneLevelDay[z] = -1;
            Mark(d, s, rep, 0);
            for (int day = 0; day < days; day++)
            {
                for (int k = 0; k < p.sessions; k++)
                {
                    double now = (day * 24 + 8 + 15.0 * (k + 0.5) / p.sessions) * H;
                    Session(d, s, p, rep, rng, day, now, simN, cache);
                }
                Mark(d, s, rep, day + 1);
                onDay?.Invoke(day + 1);
                onDaySave?.Invoke(day + 1, s);
            }
            return rep;
        }

        static void Mark(GameData d, SaveData s, ProgressReport rep, int day)
        {
            rep.level[day] = s.level;
            rep.cleared[day] = Progress.TotalCleared(s);
            foreach (var z in d.Zones)
            {
                int i = (int)z.id;
                if (rep.zoneDay[i] < 0 && Progress.ZoneDone(s, z.id)) rep.zoneDay[i] = day;
                if (rep.zoneLevelDay[i] < 0 && s.level >= z.levelMax) rep.zoneLevelDay[i] = day;
            }
        }

        static void Session(GameData d, SaveData s, PlayerProfile p, ProgressReport rep, Rng rng, int day, double now, int simN, Dictionary<string, double> cache)
        {
            int stones0 = s.evoStones;
            // 1. cây bi (hái ×2 khi xem quảng cáo, 3 lần mỗi ngày), AFK (mảnh, rương)
            int ripe = Trees.Stock(s, d.Cfg, now);
            int tm = p.ads && ripe > 0 && AdGate.Use(s, d.Cfg, day, AdGate.TreeDouble) ? 2 : 1;
            rep.ballsFromTrees += Trees.Harvest(s, d.Cfg, now, tm);
            Afk.Claim(s, d, now, 1, rng);
            var afkAt = AfkTarget(s, d);
            if (afkAt == null)
            {
                int keep = s.afk.stage;
                s.afk.stage = 0;
                afkAt = Afk.Stage(s, d); // ải AFK tự chọn
                s.afk.stage = keep;
            }
            if (afkAt != null && afkAt.id != s.afk.stage) Afk.SetStage(s, d, afkAt.id, now, rng);
            while (Afk.OpenChest(s, d, now, rng) != null) rep.afkChests++;
            if (p.ads)
                while (s.afk.chests.Count > 0 && AdGate.Use(s, d.Cfg, day, AdGate.AfkChestOpen))
                    if (Afk.OpenChest(s, d, now, rng, true) != null) rep.afkChests++;

            // 1b. trang trại: thu hoạch, rút tướng hết sức, tự xếp. Nhà thay trang trại (mô phỏng vẫn dùng mô hình trang trại cũ cho bi
            // của ruộng vườn, gần đúng), mở cùng Nhà (Home.Open: sau ải thứ 2 từ 2026-11-24)
            if (Home.Open(s, d.Cfg))
            {
                rep.ballsFromFarm += Farm.Harvest(s, d, now);
                var f = Farm.Of(s, d.Cfg, now);
                for (int i = 0; i < f.spots.Count; i++)
                    if (f.spots[i].hero != null && f.spots[i].energy <= 0) Farm.Remove(s, d, now, i);
                Farm.Auto(s, d, now);
            }

            // 2. đánh ải
            for (int b = 0; b < p.battles; b++)
            {
                var zone = Progress.RecommendedZone(s, d);
                var target = Progress.NextStage(s, d, zone.id);
                var team = BestTeam(s, d, target);
                if (team.Count == 0) break;
                double pw = target != null ? WinChance(d, s, target, team, p, simN, cache) : 0;
                if (target == null || pw < 0.3)
                {
                    var farm = d.Stages.Where(st => Progress.StageCleared(s, st))
                        .OrderByDescending(st => Progress.StageBalls(d, st, false)).ThenByDescending(st => st.id)
                        .FirstOrDefault(st => WinChance(d, s, st, team, p, simN, cache) >= 0.7);
                    if (farm != null)
                    {
                        target = farm;
                        pw = WinChance(d, s, farm, team, p, simN, cache);
                        rep.replays++;
                    }
                }
                if (target == null) break;
                rep.battles++;
                s.stats.battles++;
                if (rng.Chance(pw))
                {
                    rep.wins++;
                    s.stats.wins++;
                    rep.ballsFromStages += Progress.WinStage(s, d, target.id, rng).balls;
                }
            }

            // 3. thả hết bi ở ×1: ô rơi theo bảng tỉ lệ của máy; mỗi bi chạm mỗi nấm trung bình ringHits lần (cộng dồn phần lẻ)
            var kinds = (SlotKind[])Enum.GetValues(typeof(SlotKind));
            var hitAcc = new double[d.Cfg.ringHits.Length];
            int guard = 0;
            while (s.balls >= 1 && guard++ < 100000)
            {
                var legend = Pachinko.SpendBall(s, d, 1);
                foreach (var g in Pachinko.GiftAdd(s, d, Pachinko.GiftCredit(s, d.Cfg, 1, legend)))
                    if (g.k == RewardKind.Chest) Pachinko.OpenChest(s, d, g.chest, 1, rng);
                rep.ballsDropped++;
                var k = rng.Weighted(kinds, x => d.Cfg.Rate(Pachinko.Key(x)));
                if (Pachinko.SlotReward(s, d.Cfg, k, 1).k == RewardKind.Chest) Pachinko.OpenChest(s, d, k, 1, rng);
                for (int i = 0; i < hitAcc.Length; i++)
                {
                    hitAcc[i] += d.Cfg.ringHits[i];
                    for (; hitAcc[i] >= 1; hitAcc[i]--)
                        foreach (var g in Pachinko.RingHit(s, d.Cfg, i, 1))
                            if (g.k == RewardKind.Chest) Pachinko.OpenChest(s, d, g.chest, 1, rng);
                }
            }

            // 3b. rương mốc đảo; đá của side meta tới cấp hiện tại (Đền, Hang chưa mô phỏng trận: cộng gần đúng theo cấp)
            foreach (var z in Elements.All)
                while (Progress.ClaimZoneChest(s, d, z, rng) != null) { }
            int side = SideEvo(s.level) - rep.evoSide;
            if (side > 0)
            {
                s.evoStones += side;
                rep.evoSide += side;
            }

            // 4. nâng thẻ, lên sao (mảnh của từng tướng), tiến hóa (đá dùng chung: tướng mạnh nhất trước, mỗi lần một bậc rồi xếp lại)
            foreach (var h in d.Heroes)
            {
                if (!s.Hero(h.id).owned) continue;
                foreach (var slot in Progress.Slots)
                    while (Progress.UpCard(s, d.Cfg, h.id, slot)) rep.cardUps++;
                while (Progress.StarUp(s, d, h.id)) rep.starUps++;
            }
            rep.evoStones += s.evoStones - stones0;
            // tướng mạnh hơn đang chờ tiến hóa, đủ cấp mà thiếu đá thì để dành đá cho nó, không tiêu cho tướng yếu hơn
            for (bool more = true; more;)
            {
                more = false;
                foreach (var h in d.Heroes.Where(x => s.Hero(x.id).owned).OrderByDescending(x => Strength(d, s, x)))
                {
                    if (Progress.Evolve(s, d, h.id))
                    {
                        rep.evolves++;
                        while (Progress.StarUp(s, d, h.id)) rep.starUps++;
                        more = true;
                        break;
                    }
                    if (Progress.NextStep(s, d, h.id) == Progress.StarStep.Evolve && s.level >= Progress.EvolveCost(s, d, h.id).level) break;
                }
            }

            // 4b. Sổ Phép: vẽ theo đường gợi ý bằng nét đang có (đá còn lại sau tiến hóa)
            if (SoPhepOn) SoPhep.AutoBuy(s, d.Cfg);

            // 5. tăng tốc AFK trước khi rời game
            if (p.ads && !Afk.Boosting(s, now) && !Afk.Pending(s, d.Cfg, now).full && AdGate.Use(s, d.Cfg, day, AdGate.AfkBoost)) Afk.Boost(s, d.Cfg, now);
        }

        // ải AFK cho mảnh: tướng chủ lực (sao cao nhất, rồi mạnh nhất, có ải đã qua rơi mảnh của nó, không tính quà) nếu nó đang thiếu
        // mảnh để lên sao kế; ải có tỉ lệ rơi của nó cao nhất trong bể AFK của ải (ải tướng: chỉ nó), bằng nhau thì ải sau. Không thì null
        static StageDef AfkTarget(SaveData s, GameData d)
        {
            foreach (var h in d.Heroes.Where(x => s.Hero(x.id).owned && s.Hero(x.id).star < StarTier.MaxStar)
                         .OrderByDescending(x => s.Hero(x.id).star).ThenByDescending(x => Strength(d, s, x)))
            {
                StageDef best = null;
                double bw = 0;
                foreach (var st in d.Stages.Where(x => Progress.StageCleared(s, x)))
                {
                    var pool = Afk.Pool(st);
                    double sum = pool.Sum(x => x.chance), w = pool.Where(x => x.hero == h.id).Sum(x => x.chance);
                    if (w <= 0) continue;
                    if (w / sum >= bw) { bw = w / sum; best = st; }
                }
                if (best == null) continue;
                var g = Progress.ShardGoal(s, d, h.id);
                return g.need > 0 && g.have < g.need ? best : null;
            }
            return null;
        }

        // đá tiến hóa của side meta gom được tới cấp level, gần đúng (agent B, 2026-11-17; không mô phỏng trận Đền, Hang):
        // - Đền Huy Hiệu 10 bậc × 5 dãy, rương bậc 0/0/1/1/1/1/2/2/2/3 đá (65), mốc sao đền khoảng 20 đá rải đều bậc 3–10; bậc 3 có địch từ
        //   cấp ~94, coi mỗi bậc sau cao hơn 15 cấp (bậc 10 ở cấp ~199);
        // - Hang Tiềm Năng thưởng lần đầu khoảng 9 đá: 3 đá mỗi tầng 3 (cấp 62), 5 (cấp 98), 7 (cấp 134).
        static readonly int[] TempleChest = { 0, 0, 1, 1, 1, 1, 2, 2, 2, 3 };

        public static int SideEvo(int level)
        {
            double n = 0;
            for (int t = 0; t < TempleChest.Length; t++)
            {
                int at = t < 2 ? 0 : 94 + (t - 2) * 15;
                if (t >= 2 && level >= at) n += 5 * TempleChest[t] + 20.0 / 8;
            }
            foreach (int lv in new[] { 62, 98, 134 })
                if (level >= lv) n += 3;
            return (int)n;
        }

        // sức của tướng để xếp đội và dồn đá: lực chiến (cấp, sao, độ hiếm, phần cộng) nhân √(cấp thẻ trung bình)
        static double Strength(GameData d, SaveData s, HeroDef h) =>
            HeroStats.Power(d.Cfg, h, Teams.MemberOf(s, h.id, d)) * Math.Sqrt(Progress.CardSum(s, h.id) / 3.0);

        // đội theo số ô đã mở (Progress.TeamSlots): sức của tướng nhân lợi thế hệ với tướng chính của ải (√(hệ số gây / hệ số nhận));
        // sao lệch nhiều theo bậc (2026-11-17) nên không xếp tướng khắc hệ 1 sao lên trước tướng chủ lực đã tiến hóa
        static List<string> BestTeam(SaveData s, GameData d, StageDef target)
        {
            var foe = target != null ? d.Hero(Teams.StageLead(target, d).hero).elem : (Elem?)null;
            double Edge(HeroDef h) => foe is Elem e
                ? Math.Sqrt(Elements.Mult(h.elem, e, h.id == s.starter, false) / Elements.Mult(e, h.elem, false, h.id == s.starter))
                : 1;
            var team = d.Heroes.Where(h => s.Hero(h.id).owned)
                .OrderByDescending(h => Strength(d, s, h) * Edge(h)).ThenBy(h => d.Heroes.IndexOf(h))
                .Take(Progress.TeamSlots(s)).Select(h => h.id).ToList();
            s.team = team;
            return team;
        }

        static double WinChance(GameData d, SaveData s, StageDef st, List<string> team, PlayerProfile p, int simN, Dictionary<string, double> cache)
        {
            var key = $"{st.id}|{s.level}|{s.starter}|" + string.Join(",", team.Select(h =>
            {
                var hp = s.Hero(h);
                return $"{h}:{hp.star}:{hp.skill.lv}{hp.ult.lv}{hp.passive.lv}";
            })) + "|" + SoPhep.Key(s);
            if (!cache.TryGetValue(key, out var bot))
            {
                bot = Sim.Stage(d, s, st, simN, 1000, team).WinRate;
                cache[key] = bot;
            }
            return Math.Min(1, bot + p.skill);
        }
    }
}
