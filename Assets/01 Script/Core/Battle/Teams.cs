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

        public static TeamSetup Enemy(StageDef st)
        {
            var t = new TeamSetup { name = st.name, ai = true };
            foreach (var e in st.enemies)
                t.members.Add(new Member
                {
                    heroId = e.hero, level = e.level, boss = e.boss, star = EnemyStar(e.level),
                    cardSkill = 1 + e.level / 5, cardUlt = 1 + e.level / 6, cardPassive = 1 + e.level / 6,
                });
            return t;
        }
    }
}
