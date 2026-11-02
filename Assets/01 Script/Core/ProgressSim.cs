// Mô phỏng tiến độ: N ngày theo các kiểu người chơi (chăm, vừa, ít). Mỗi lần vào game:
//   1. nhận AFK (×2 nếu xem quảng cáo), mở rương AFK tới giờ (và "Mở ngay" nếu xem quảng cáo);
//   2. đánh ải kế tiếp của đảo gợi ý; tỉ lệ thắng = máy tự chơi (đội và cấp thật lúc đó) + mức "người giỏi hơn máy";
//      ải kế quá khó (< 30%) thì đánh lại ải đã qua nhiều bi nhất mà gần chắc thắng;
//   3. thả hết bi (ô rơi theo tỉ lệ đo của máy, ×1), mở rương máy bi; 4. nâng thẻ, tiến hóa khi đủ;
//   5. rời game thì bật tăng tốc AFK (nếu xem quảng cáo).
// Có trang trại (thu hoạch, đổi ca, tự xếp mỗi lần vào). Huy hiệu và tiềm năng chưa mô phỏng (cần chơi tay).
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
        public int[] zoneLevelDay = new int[5]; // ngày đạt cấp đề nghị thấp nhất của đảo, -1 = chưa
        public int battles, wins, replays, ballsDropped, ballsFromStages, ballsFromTrees, ballsFromFarm, afkChests, cardUps, evolves;
    }

    public static class ProgressSim
    {
        const double H = 3600000;

        // giá trị khởi điểm (design.md, câu hỏi còn mở)
        public static PlayerProfile[] DefaultProfiles() => new[]
        {
            new PlayerProfile { name = "Chăm", sessions = 6, battles = 5, ads = true },
            new PlayerProfile { name = "Vừa", sessions = 3, battles = 3, ads = true },
            new PlayerProfile { name = "Ít", sessions = 1, battles = 2, ads = false },
        };

        // cache: tỉ lệ thắng của máy theo (ải, cấp, đội); dùng chung giữa các kiểu người chơi để chạy nhanh
        public static ProgressReport Run(GameData d, PlayerProfile p, int days = 30, uint seed = 1, int simN = 8,
            Dictionary<string, double> cache = null, Action<int> onDay = null)
        {
            cache = cache ?? new Dictionary<string, double>();
            var s = SaveData.New(d, 0);
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
                if (rep.zoneLevelDay[i] < 0 && s.level >= z.levelMin) rep.zoneLevelDay[i] = day;
            }
        }

        static void Session(GameData d, SaveData s, PlayerProfile p, ProgressReport rep, Rng rng, int day, double now, int simN, Dictionary<string, double> cache)
        {
            // 1. cây bi (hái ×2 khi xem quảng cáo, 3 lần mỗi ngày), AFK (mảnh, rương)
            int ripe = Trees.Stock(s, d.Cfg, now);
            int tm = p.ads && ripe > 0 && AdGate.Use(s, d.Cfg, day, AdGate.TreeDouble) ? 2 : 1;
            rep.ballsFromTrees += Trees.Harvest(s, d.Cfg, now, tm);
            Afk.Claim(s, d, now, 1, rng);
            while (Afk.OpenChest(s, d, now, rng) != null) rep.afkChests++;
            if (p.ads)
                while (s.afk.chests.Count > 0 && AdGate.Use(s, d.Cfg, day, AdGate.AfkChestOpen))
                    if (Afk.OpenChest(s, d, now, rng, true) != null) rep.afkChests++;

            // 1b. trang trại: thu hoạch, rút tướng hết sức, tự xếp
            if (Farm.Open(s, d.Cfg))
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
                var team = BestTeam(s, d);
                if (team.Count == 0) break;
                var zone = Progress.RecommendedZone(s, d);
                var target = Progress.NextStage(s, d, zone.id);
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

            // 3. thả hết bi ở ×1: ô rơi theo tỉ lệ đo của máy
            var kinds = (SlotKind[])Enum.GetValues(typeof(SlotKind));
            int guard = 0;
            while (s.balls >= 1 && guard++ < 100000)
            {
                Pachinko.SpendBall(s, d, 1);
                rep.ballsDropped++;
                var k = rng.Weighted(kinds, x => d.Cfg.Rate(Pachinko.Key(x)));
                if (Pachinko.SlotReward(s, d.Cfg, k, 1).k == RewardKind.Chest) Pachinko.OpenChest(s, d, k, 1, rng);
            }

            // 4. nâng thẻ, tiến hóa
            foreach (var h in d.Heroes)
            {
                if (!s.Hero(h.id).owned) continue;
                foreach (var slot in Progress.Slots)
                    while (Progress.UpCard(s, d.Cfg, h.id, slot)) rep.cardUps++;
                while (Progress.Evolve(s, d.Cfg, h.id)) rep.evolves++;
            }

            // 5. tăng tốc AFK trước khi rời game
            if (p.ads && !Afk.Boosting(s, now) && !Afk.Pending(s, d.Cfg, now).full && AdGate.Use(s, d.Cfg, day, AdGate.AfkBoost)) Afk.Boost(s, d.Cfg, now);
        }

        // 3 tướng mạnh nhất đang có: sao, độ hiếm, tổng cấp thẻ
        static List<string> BestTeam(SaveData s, GameData d)
        {
            var team = d.Heroes.Where(h => s.Hero(h.id).owned)
                .OrderByDescending(h => s.Hero(h.id).star).ThenByDescending(h => (int)h.rarity)
                .ThenByDescending(h => Progress.CardSum(s, h.id)).ThenBy(h => d.Heroes.IndexOf(h))
                .Take(3).Select(h => h.id).ToList();
            s.team = team;
            return team;
        }

        static double WinChance(GameData d, SaveData s, StageDef st, List<string> team, PlayerProfile p, int simN, Dictionary<string, double> cache)
        {
            var key = $"{st.id}|{s.level}|" + string.Join(",", team.Select(h =>
            {
                var hp = s.Hero(h);
                return $"{h}:{hp.star}:{hp.skill.lv}{hp.ult.lv}{hp.passive.lv}";
            }));
            if (!cache.TryGetValue(key, out var bot))
            {
                bot = Sim.Stage(d, s, st, simN, 1000, team).WinRate;
                cache[key] = bot;
            }
            return Math.Min(1, bot + p.skill);
        }
    }
}
