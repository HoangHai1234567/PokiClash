// Dựng đội cho trận, chép memberOf / playerTeam / enemyTeam của Web/src/core/progression.ts.
using System.Collections.Generic;

namespace PokiClash.Core
{
    public static class Teams
    {
        // d: dữ liệu để biết hệ của tướng (phần cộng huy hiệu); null thì dùng GameData.Current
        public static Member MemberOf(SaveData s, string hero, GameData d = null)
        {
            var p = s.Hero(hero);
            d = d ?? GameData.Current;
            var h = d?.Hero(hero);
            return new Member
            {
                heroId = hero, level = s.level, star = p.star,
                cardSkill = p.skill.lv, cardUlt = p.ult.lv, cardPassive = p.passive.lv,
                mods = h != null ? Potential.Mods(s, d, h) : null, // huy hiệu + tiềm năng
                start = h != null ? Potential.Start(s, d, hero) : null,
                partner = hero == s.starter,
            };
        }

        public static TeamSetup Player(SaveData s, IEnumerable<string> team = null, GameData d = null)
        {
            var t = new TeamSetup { name = "Đội bạn", ai = false };
            foreach (var h in team ?? s.team)
            {
                var p = s.Hero(h);
                if (p != null && p.owned) t.members.Add(MemberOf(s, h, d));
            }
            return t;
        }

        // sao của địch theo cấp (chép enemyTeam của Web/src/core/progression.ts); cũng chọn dạng của địch trong dòng tiến hóa
        public static int EnemyStar(int level) => 1 + level / 6;

        // sao để chọn hình (dạng) của địch ngoài trận: như EnemyStar, riêng boss tiến hóa vào trận ở dạng 1 (chép enemyFormStar)
        public static int EnemyFormStar(StageEnemy e) => e.evo ? 1 : EnemyStar(e.level);

        // sao ứng với dạng thứ form của dòng (dạng 1 là sao 1, dạng sau ở mốc formStars)
        public static int FormStar(BalanceConfig cfg, int form) => form <= 0 ? 1 : cfg.formStars[System.Math.Min(form, cfg.formStars.Length) - 1];

        // sao để vẽ tướng đang trên sân: boss tiến hóa theo dạng trong trận, còn lại theo sao
        public static int LookStar(BalanceConfig cfg, Fighter f) => f.evo ? FormStar(cfg, f.form) : f.star;

        // tướng chính của ải (đứng trên nút ải ở màn đảo; chép stageLead): boss, không có thì địch cấp cao nhất, bằng cấp thì độ hiếm
        // cao hơn
        public static StageEnemy StageLead(StageDef st, GameData d)
        {
            int Score(StageEnemy e) => (e.boss ? 1000 : 0) + e.level * 10 + (int)d.Hero(e.hero).rarity;
            var best = st.enemies[0];
            foreach (var e in st.enemies)
                if (Score(e) > Score(best)) best = e;
            return best;
        }

        // d: để biết lính và độ hiếm (phần cộng của địch, Islands.EnemyMods)
        public static TeamSetup Enemy(StageDef st, GameData d)
        {
            var t = new TeamSetup { name = st.name, ai = true };
            foreach (var e in st.enemies)
                t.members.Add(new Member
                {
                    heroId = e.hero, level = e.level, boss = e.boss, evo = e.evo, star = EnemyStar(e.level),
                    cardSkill = 1 + e.level / 5, cardUlt = 1 + e.level / 6, cardPassive = 1 + e.level / 6,
                    mods = Islands.EnemyMods(d, e, st.tag != StageTag.None),
                });
            return t;
        }
    }
}
