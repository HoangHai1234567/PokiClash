// Đấu trường ngầm (Hầm đấu, GD_Claude/29_DaoCasino.md mục 6.5): trận thẻ bài thường với đội địch do người thiết kế đặt theo ngày.
// - Đội trong ngày: dates (ghi đè theo ngày yyyy-MM-dd) hoặc rotation[(ngày − mốc) mod số ngày vòng]. Mỗi ngày một đội cho mỗi bậc
//   thường; bậc weekly (Nhà Vô Địch) chỉ chủ nhật, một lần mỗi tuần, dùng đội kế tiếp trong danh sách của ngày (nếu có).
// - Bậc mở theo cấp người chơi; lệ phí trả lúc bấm Đánh (× bậc cấp). Thắng lần đầu trong ngày: winMult × lệ phí + mảnh tướng chủ lực +
//   quà của bậc; thắng lại: rewinMult × lệ phí + rewin; thua: mất lệ phí.
// - Luật ngày áp lên hai đội: atk / hp / def (+p cho tướng hệ elem, rỗng = mọi tướng), picks (số lần chọn mỗi lượt của người chơi),
//   solo (mỗi bên một tướng), buff (đội địch mạnh thêm p).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class UgResult
    {
        public bool won, first;
        public int balls;
        public List<Reward> rewards = new List<Reward>();
    }

    public static class Underground
    {
        static UndergroundConfig C(GameData d) => Casino.C(d).underground;

        public static string Ymd(int day) => new DateTime(1970, 1, 1).AddDays(day).ToString("yyyy-MM-dd", System.Globalization.CultureInfo.InvariantCulture);

        // chủ nhật (ngày 0 = thứ Năm 1/1/1970)
        public static bool Sunday(int day) => ((day % 7) + 7) % 7 == 3;

        public static UgDay DayOf(GameData d, int day)
        {
            var c = C(d);
            string ymd = Ymd(day);
            var fixedDay = c.dates.Find(x => x.date == ymd);
            if (fixedDay != null) return fixedDay;
            if (c.rotation.Count == 0) return null;
            int k = ((day - Casino.Anchor(d)) % c.rotation.Count + c.rotation.Count) % c.rotation.Count;
            return c.rotation[k];
        }

        public static int NormalTiers(GameData d) => C(d).tiers.Count(t => !t.weekly);

        // các bậc hiện hôm nay (bậc weekly chỉ chủ nhật và khi ngày có đủ đội)
        public static List<int> TiersToday(GameData d, double now)
        {
            int day = Casino.Today(now);
            var ud = DayOf(d, day);
            var list = new List<int>();
            int normal = 0;
            for (int i = 0; i < C(d).tiers.Count; i++)
            {
                var t = C(d).tiers[i];
                if (!t.weekly)
                {
                    if (ud != null && normal < ud.entries.Count) list.Add(i);
                    normal++;
                }
                else if (Sunday(day) && ud != null && ud.entries.Count > NormalTiers(d)) list.Add(i);
            }
            return list;
        }

        public static UgEntry Entry(GameData d, int tier, double now) => EntryAt(d, tier, Casino.Today(now));

        // đội của bậc tier trong ngày day (trận đang đánh giữ ngày lúc bấm Đánh, qua 0 giờ vẫn đúng đội)
        public static UgEntry EntryAt(GameData d, int tier, int day)
        {
            var ud = DayOf(d, day);
            if (ud == null || tier < 0 || tier >= C(d).tiers.Count) return null;
            int k = C(d).tiers[tier].weekly ? NormalTiers(d) : C(d).tiers.Take(tier).Count(t => !t.weekly);
            return k < ud.entries.Count ? ud.entries[k] : null;
        }

        // ải giả cho trận (nền, nhạc, độ epic như ải thường): đảo theo hệ tướng chủ lực, bậc từ Vàng trở lên là trận boss
        public static StageDef Stage(GameData d, UgEntry e, int tier)
        {
            string lead = Lead(e);
            var t = C(d).tiers[Math.Max(0, Math.Min(tier, C(d).tiers.Count - 1))];
            var st = new StageDef
            {
                id = 90000 + tier, zone = d.Hero(lead)?.elem ?? Elem.Tho, idx = tier + 1, name = e.Name,
                kind = t.weekly || tier >= 3 ? StageKind.Boss : StageKind.Normal,
            };
            foreach (var m in TeamLimit(e) == 1 ? e.team.Take(1) : e.team)
                st.enemies.Add(new StageEnemy { hero = m.hero, level = Math.Max(1, m.level), boss = st.kind == StageKind.Boss && m.hero == lead });
            return st;
        }

        public static bool TierOpen(SaveData s, GameData d, int tier) =>
            Casino.Unlocked(s, d, Casino.Underground) && tier >= 0 && tier < C(d).tiers.Count && s.level >= C(d).tiers[tier].level;

        public static int Fee(SaveData s, GameData d, int tier) => Shop.RoundBalls(C(d).tiers[tier].fee * Casino.Band(s, d));

        public static bool WonToday(SaveData s, GameData d, int tier, double now)
        {
            var st = Casino.Roll(s, d, now);
            if (C(d).tiers[tier].weekly) return st.ugChampWeek == Casino.Week(Casino.Today(now));
            return (st.ugWon & (1 << tier)) != 0;
        }

        public static string Lead(UgEntry e) => !string.IsNullOrEmpty(e.lead) ? e.lead : e.team.FirstOrDefault()?.hero;

        public static int TeamLimit(UgEntry e) => e?.rule?.kind == "solo" ? 1 : 3;

        // chữ luật ngày
        public static string RuleText(UgRule r)
        {
            if (r == null || string.IsNullOrEmpty(r.kind)) return Loc.T("Luật thường");
            string who = string.IsNullOrEmpty(r.elem) ? Loc.T("mọi tướng") : Loc.F("tướng hệ {0}", Elements.Name(Keys.ToElem(r.elem)));
            int pct = (int)Math.Round(r.p * 100);
            switch (r.kind)
            {
                case "atk": return Loc.F("Công +{0}% cho {1}", pct, who);
                case "hp": return Loc.F("Máu +{0}% cho {1}", pct, who);
                case "def": return Loc.F("Thủ +{0}% cho {1}", pct, who);
                case "picks": return Loc.F("Mỗi lượt chỉ chọn {0} thẻ", r.n);
                case "solo": return Loc.T("Mỗi bên chỉ một tướng");
                case "buff": return Loc.F("Đội ngầm mạnh thêm {0}%", pct);
                default: return r.kind;
            }
        }

        // đội địch (sao, thẻ do người thiết kế đặt), đã áp luật ngày phần của địch
        public static TeamSetup Enemy(GameData d, UgEntry e)
        {
            var t = new TeamSetup { name = e.Name, ai = true };
            var list = TeamLimit(e) == 1 ? e.team.Take(1) : e.team;
            foreach (var m in list)
                t.members.Add(new Member
                {
                    heroId = m.hero, level = Math.Max(1, m.level), star = Math.Max(1, m.star),
                    cardSkill = Math.Max(1, m.card), cardUlt = Math.Max(1, m.card), cardPassive = Math.Max(1, m.card),
                });
            ApplyRule(d, e.rule, t, true);
            return t;
        }

        // áp luật ngày lên một đội (enemy: buff chỉ cho địch; picks chỉ cho người chơi)
        public static void ApplyRule(GameData d, UgRule r, TeamSetup t, bool enemy)
        {
            if (r == null || string.IsNullOrEmpty(r.kind) || t == null) return;
            Elem? el = string.IsNullOrEmpty(r.elem) ? (Elem?)null : Keys.ToElem(r.elem);
            foreach (var m in t.members)
            {
                var h = d.Hero(m.heroId);
                bool hit = h != null && (el == null || h.elem == el.Value);
                StatMods Mods() => m.mods ?? (m.mods = new StatMods());
                switch (r.kind)
                {
                    case "atk": if (hit) Mods().atkPct += r.p; break;
                    case "hp": if (hit) Mods().hpPct += r.p; break;
                    case "def": if (hit) Mods().defPct += r.p; break;
                    case "buff":
                        if (enemy)
                        {
                            Mods().hpPct += r.p;
                            Mods().atkPct += r.p;
                            Mods().defPct += r.p / 2;
                        }
                        break;
                }
            }
            if (!enemy && r.kind == "picks" && r.n > 0)
            {
                t.rules = t.rules ?? new BattleRules();
                t.rules.picks = r.n;
            }
        }

        // trả lệ phí lúc bấm Đánh
        public static bool Pay(SaveData s, GameData d, int tier, double now, out string why)
        {
            why = null;
            if (!TierOpen(s, d, tier)) { why = Loc.F("Mở ở cấp {0}", C(d).tiers[Math.Max(0, Math.Min(tier, C(d).tiers.Count - 1))].level); return false; }
            if (!TiersToday(d, now).Contains(tier)) { why = Loc.T("Hôm nay không có trận này"); return false; }
            if (C(d).tiers[tier].weekly && WonToday(s, d, tier, now)) { why = Loc.T("Tuần này đã thắng Nhà Vô Địch"); return false; }
            if (!Casino.Spend(s, Fee(s, d, tier))) { why = Loc.T("Không đủ bi"); return false; }
            Casino.Roll(s, d, now);
            return true;
        }

        public static UgResult Finish(SaveData s, GameData d, int tier, bool won, double now, Rng rng)
        {
            var res = new UgResult { won = won };
            if (!won) return res;
            var c = C(d);
            var t = c.tiers[tier];
            var e = Entry(d, tier, now);
            var st = Casino.Roll(s, d, now);
            res.first = !WonToday(s, d, tier, now);
            int fee = Fee(s, d, tier);
            Casino.Track(s, d, "ug_win", 1, now);
            if (res.first)
            {
                if (t.weekly) st.ugChampWeek = Casino.Week(Casino.Today(now));
                else st.ugWon |= 1 << tier;
                res.balls = (int)Math.Round(fee * c.winMult);
                s.balls += res.balls;
                var items = new List<CasinoItem>(t.items);
                string lead = e != null ? Lead(e) : null;
                if (t.shards > 0 && lead != null) items.Insert(0, new CasinoItem { k = "shards", n = t.shards, h = lead });
                res.rewards = Casino.Grant(s, d, items, now, rng);
            }
            else
            {
                res.balls = (int)Math.Round(fee * c.rewinMult);
                s.balls += res.balls;
                res.rewards = Casino.Grant(s, d, c.rewin, now, rng);
            }
            return res;
        }
    }
}
