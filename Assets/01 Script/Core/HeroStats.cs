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
    }
}
