// Chỉ số tướng, một nguồn cho trận và màn Tướng (chép heroStats của Web/src/core/battle.ts).
//   m    = sức theo độ hiếm × (1 + lvStep·(cấp − 1)) × (1 + starStep·(sao − 1))
//   Máu  = hpBase  × √(máu gốc / tb) × m (× bossHp)
//   Công = atkBase × √(max(công, công phép) / tb) × m (× bossAtk)
//   Thủ  = defBase × √(tb(thủ, thủ phép) / tb) × m
//   Tốc  = tốc gốc + cấp
// tb là trung bình (công, thủ, máu) của chính tướng. mods: phần cộng của side meta (huy hiệu, đá tiềm năng), mặc định không có.
using System;

namespace PokiClash.Core
{
    public sealed class StatMods
    {
        public double hpPct, atkPct, defPct; // cộng phần trăm (0,05 = +5%)
        public double spd; // cộng thẳng
        public bool IsEmpty => hpPct == 0 && atkPct == 0 && defPct == 0 && spd == 0;
    }

    public struct Stats
    {
        public double hp, atk, def, spd;
    }

    public static class HeroStats
    {
        static readonly double[] RarityPower = { 1, 1.1, 1.22, 1.36, 1.5 };

        public static double PowerOf(Rarity r) => RarityPower[(int)r];

        public static Stats Compute(BalanceConfig cfg, HeroDef h, int level, int star, bool boss = false, StatMods mods = null)
        {
            double atkP = h.stats[0], defP = h.stats[1], matk = h.stats[2], mdef = h.stats[3], hpS = h.stats[4], spd = h.stats[5];
            double a = Math.Max(atkP, matk), d = (defP + mdef) / 2, mean = (a + d + hpS) / 3;
            double m = RarityPower[(int)h.rarity] * (1 + cfg.lvStep * (level - 1)) * (1 + cfg.starStep * (star - 1));
            double hp = cfg.hpBase * Math.Sqrt(hpS / mean) * m * (boss ? cfg.bossHp : 1);
            double atk = cfg.atkBase * Math.Sqrt(a / mean) * m * (boss ? cfg.bossAtk : 1);
            double def = cfg.defBase * Math.Sqrt(d / mean) * m;
            // nhân thêm chỉ khi có mods, để số không mods khớp từng bit với bản web
            if (mods != null && !mods.IsEmpty)
            {
                hp *= 1 + mods.hpPct;
                atk *= 1 + mods.atkPct;
                def *= 1 + mods.defPct;
                spd += mods.spd;
            }
            return new Stats { hp = Js.Round(hp), atk = Js.Round(atk), def = Js.Round(def), spd = spd + level };
        }

        // Lực chiến (chỉ để hiện, trận không dùng): 2·√(máu hiệu dụng × Công), máu hiệu dụng = Máu × (defK + Thủ) / defK
        // (sát thương nhận × defK / (defK + Thủ)). Tăng gần đúng tỉ lệ với m: tướng thường cấp 1 khoảng 800.
        public static int Power(BalanceConfig cfg, Stats s) =>
            (int)Math.Round(2 * Math.Sqrt(s.hp * (cfg.defK + s.def) / cfg.defK * s.atk));

        // chỉ số một tướng khi vào trận (khớp Battle.MakeFighter), để hiện ở hộp Chuẩn bị trận; tướng tiến hóa trong trận thì theo
        // dạng form của dòng (máu, Công nhân hệ số của dạng, Battle.EvoMult)
        public static Stats InBattle(BalanceConfig cfg, HeroDef h, Member m, int form = 0)
        {
            var s = Compute(cfg, h, m.level, m.star, m.boss, m.mods);
            if (!m.evo) return s;
            var k = Battle.EvoMult(cfg, Math.Max(1, h.forms.Length), form);
            s.hp = Js.Round(s.hp * k.hp);
            s.atk = Js.Round(s.atk * k.atk);
            return s;
        }

        // lực chiến của một tướng trong đội (cấp, sao, boss, phần cộng); boss tiến hóa gánh máu cả dòng (cfg.bossEvoHp)
        public static int Power(BalanceConfig cfg, HeroDef h, Member m)
        {
            var s = Compute(cfg, h, m.level, m.star, m.boss, m.mods);
            if (m.evo) s.hp *= cfg.bossEvoHp;
            return Power(cfg, s);
        }
    }

    public static class TeamPower
    {
        public static int Of(BalanceConfig cfg, GameData d, TeamSetup t)
        {
            int sum = 0;
            foreach (var m in t.members) sum += HeroStats.Power(cfg, d.Hero(m.heroId), m);
            return sum;
        }

        // 12345 -> "12.345" (dấu chấm ngăn nghìn như tiếng Việt)
        public static string Text(int v) => v.ToString("#,0", System.Globalization.CultureInfo.InvariantCulture).Replace(',', '.');
    }
}
