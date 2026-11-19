// Đền Huy Hiệu so với golden badges.json: đội địch của mọi trận thử thách (cấp, tướng, boss, cường hóa, hạt giống), chỉ số có phần cộng
// huy hiệu, 5 trận đánh thật bậc Đồng hệ Thủy, một đoạn tiến độ (mở đền, thắng, lên bậc, rương).
// Thêm: thua không mất tiến độ, phần cộng theo bậc cao nhất không cộng dồn, không có huy hiệu thì không có mods; sao từng trận, đánh lại
// lấy sao, mốc sao, bản lưu cũ thắng nhiều hơn số trận mới; đặc tính hệ và phần cộng cả đội.
// badges.json (chỉ số Võ Sư): tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md);
// số hiệp 5 trận thật tính lại cùng ngày khi Chiêu đổi sang ra đòn ngay lúc bấm, và 2026-11-04 khi đổi luật rút thẻ.
// 2026-11-16: bỏ 31 tướng cũ không còn suất đảo, tướng mẫu đổi sang tướng thay cùng hệ (SaveCodec.BoTuongCu); golden tính lại bằng
// menu "PokiClash/Thử/Tính lại golden theo tướng mẫu của test" (GoldenFixtureMenu).
// 2026-11-17 (tăng dày nội dung, GD_Claude/20_TangDayNoiDung.md): 10 bậc, số trận 5/5/6/6/8/8/8/10/10/12, cấp địch +14 mỗi bậc, địch
// quy về sức tướng Khá; "stages" dựng lại đủ mọi trận bằng menu "Tính lại golden theo danh sách tướng" (IslandGenMenu), "stats",
// "steps" bằng GoldenFixtureMenu, "fights" bằng IslandGenMenu.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class BadgeTests
    {
        static Dictionary<string, object> G => J.Obj(MiniJson.Parse(TestData.Read("Golden/badges.json")));

        [Test]
        public void DoiDichMoiTran_KhopGolden()
        {
            var d = TestData.Load();
            int n = 0;
            foreach (var x in J.Arr(G, "stages"))
            {
                var o = J.Obj(x);
                var z = Keys.ToElem(J.Str(o, "zone"));
                int tier = J.Int(o, "tier"), i = J.Int(o, "i");
                var st = Badges.Stage(d, z, tier, i);
                string at = $"{J.Str(o, "zone")} bậc {tier} trận {i}";
                Assert.AreEqual(J.Int(o, "id"), st.id, at);
                Assert.AreEqual((uint)J.Num(o, "seed"), Badges.Seed(d, z, tier, i), at);
                Assert.AreEqual(J.Str(o, "kind"), st.kind == StageKind.Boss ? "boss" : "mini", at);
                var we = J.Arr(o, "enemies");
                Assert.AreEqual(we.Count, st.enemies.Count, at);
                for (int k = 0; k < we.Count; k++)
                {
                    var e = J.Arr(we[k]);
                    Assert.AreEqual((string)e[0], st.enemies[k].hero, at);
                    Assert.AreEqual((double)e[1], st.enemies[k].level, at);
                    Assert.AreEqual((bool)e[2], st.enemies[k].boss, at);
                    if (e.Count > 3) Assert.AreEqual((double)e[3], st.enemies[k].buff, 1e-9, at + " cường hóa");
                }
                n++;
            }
            Assert.AreEqual(Elements.All.Length * Badges.FightsTotal(d.Cfg), n, "golden có đủ mọi trận của 5 dãy");
        }

        // đội 5 trận đánh thật bậc Đồng hệ Thủy (IslandGenMenu.HeroGoldens tính lại "fights" bằng đúng đội và bản lưu này)
        static readonly string[] FightTeam = { "ti_tach", "so_ngoc", "giap_long" };

        static SaveData StatSave(GameData d)
        {
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "cao_da", "tien_la", "so_ngoc", "giap_long" }) s.Hero(id).owned = true;
            s.badges[(int)Elem.Thuy].tier = 2;
            s.badges[(int)Elem.Hoa].tier = 5;
            return s;
        }

        [Test]
        public void ChiSoCoHuyHieu_VaTranThat_KhopGolden()
        {
            var d = TestData.Load();
            var s = StatSave(d);
            foreach (var x in J.Arr(G, "stats"))
            {
                var o = J.Obj(x);
                var h = d.Hero(J.Str(o, "hero"));
                var m = Teams.MemberOf(s, h.id, d);
                Assert.AreEqual(J.Get(o, "mods") == null, m.mods == null, h.id + " có phần cộng");
                var st = HeroStats.Compute(d.Cfg, h, 9, 2, false, m.mods);
                var w = J.Obj(o, "stats");
                Assert.AreEqual(J.Num(w, "hp"), st.hp, h.id);
                Assert.AreEqual(J.Num(w, "atk"), st.atk, h.id);
                Assert.AreEqual(J.Num(w, "def"), st.def, h.id);
                Assert.AreEqual(J.Num(w, "spd"), st.spd, h.id);
            }
            s.level = 9;
            // đội có tướng khởi đầu (tướng đồng hành): Tí Tách từ 2026-11-11. Số hiệp, bên thắng tính lại bằng menu "PokiClash/Thử/Tính lại
            // golden theo danh sách tướng" (đối thủ đền hệ Thủy chọn theo danh sách tướng Thủy, thêm 10 tướng là đổi)
            s.team = new List<string>(FightTeam);
            foreach (var x in J.Arr(G, "fights"))
            {
                var o = J.Obj(x);
                int i = J.Int(o, "i");
                var stage = TestData.AtLevel(Badges.Stage(d, Elem.Thuy, 1, i), J.Int(o, "foeLevel"));
                var team = Teams.Player(s, null, d);
                team.ai = true;
                var b = Battle.Create(d, team, Teams.Enemy(stage, d), Badges.Seed(d, Elem.Thuy, 1, i), 9, System.Math.Max(9, stage.enemies[0].level));
                BattleSim.Run(b);
                Assert.AreEqual(J.Int(o, "winner"), b.winner, $"trận {i} bên thắng");
                Assert.AreEqual(J.Int(o, "round"), b.round, $"trận {i} số hiệp");
            }
        }

        [Test]
        public void TienDo_MoDen_LenBac_Ruong_KhopGolden()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0, TestData.OldStarter); // bản lưu mẫu của golden (TestData.OldStarter)
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.zones[(int)Elem.Kim] = Islands.MiniAt(Elem.Kim); // qua mini boss đầu đảo Kim (ải 4 khi còn 8 ải, ải 20 từ 2026-11-05)
            var rng = new Rng(31);
            var steps = J.Arr(G, "steps");
            var first = J.Obj(steps[0]);
            Assert.AreEqual(J.Bool(first, "temple"), Badges.TempleOpen(s));
            var zones = d.Zones.Select(z => z.id).ToList();
            var lines = J.Arr(first, "lines");
            for (int k = 0; k < zones.Count; k++) Assert.AreEqual((bool)lines[k], Badges.LineOpen(s, zones[k]), Keys.Of(zones[k]));
            for (int k = 1; k < steps.Count; k++)
            {
                var o = J.Obj(steps[k]);
                var z = Keys.ToElem(J.Str(o, "zone"));
                var r = Badges.Win(s, d, z, rng);
                string at = $"bước {k}";
                Assert.AreEqual(J.Int(o, "gain"), r?.balls ?? 0, at + " bi thưởng");
                Assert.AreEqual(J.Int(o, "tierDone"), r?.tierDone ?? 0, at);
                var wr = J.Arr(o, "rewards");
                Assert.AreEqual(wr.Count, r?.rewards.Count ?? 0, at + " số thưởng rương");
                for (int q = 0; q < wr.Count; q++)
                {
                    var e = J.Arr(wr[q]);
                    if ((string)e[0] == "card") Assert.AreEqual((string)e[2], r.rewards[q].drop.card, at);
                    else Assert.AreEqual((double)e[1], r.rewards[q].n, at);
                }
                var cur = J.Obj(o, "cur");
                var mine = Badges.Current(s, d.Cfg, z);
                Assert.AreEqual(cur == null, mine == null, at + " trận đang đánh");
                if (cur != null)
                {
                    Assert.AreEqual(J.Int(cur, "tier"), mine.Value.tier, at);
                    Assert.AreEqual(J.Int(cur, "i"), mine.Value.i, at);
                }
                Assert.AreEqual(J.Int(o, "balls"), s.balls, at + " tổng bi");
                var wb = J.Obj(J.Obj(o, "badges"), J.Str(o, "zone"));
                Assert.AreEqual(J.Int(wb, "tier"), s.badges[(int)z].tier, at + " bậc");
                Assert.AreEqual(J.Int(wb, "won"), s.badges[(int)z].won, at + " đã thắng");
                Assert.AreEqual(J.Int(o, "level"), s.level, at + " cấp");
                Assert.AreEqual(J.Int(o, "exp"), s.exp, at + " exp");
            }
        }

        [Test]
        public void ThuaKhongMatTienDo_PhanCongKhongCongDon_LuuDocLai()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            Assert.IsNull(Teams.MemberOf(s, "ti_tach", d).mods, "chưa có huy hiệu thì không có phần cộng");
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.badges[(int)Elem.Thuy].won = 3;
            // thua: không gọi Win, trận đang đánh vẫn là 4
            Assert.AreEqual((1, 4), Badges.Current(s, cfg, Elem.Thuy).Value);
            s.badges[(int)Elem.Thuy].tier = 3;
            var m = Badges.Mods(s, cfg, Elem.Thuy);
            Assert.AreEqual(cfg.badges.bonus[2], m.hpPct, 1e-12, "bậc Vàng chỉ lấy phần cộng của bậc Vàng, không cộng dồn các bậc dưới");
            var h = d.Hero("ti_tach");
            var plain = HeroStats.Compute(cfg, h, 5, 1);
            var boosted = HeroStats.Compute(cfg, h, 5, 1, false, Teams.MemberOf(s, "ti_tach", d).mods);
            Assert.AreEqual(plain.hp * (1 + cfg.badges.bonus[2]), boosted.hp, 1.0);
            Assert.IsNull(Teams.MemberOf(s, "cao_da", d).mods, "hệ khác không được cộng");
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var back));
            Assert.AreEqual(3, back.badges[(int)Elem.Thuy].tier);
            Assert.AreEqual(3, back.badges[(int)Elem.Thuy].won);
        }

        [Test]
        public void SaoTungTran_DanhLai_MocSao_BanLuuCu()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var rng = new Rng(5);
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = Islands.MiniAt(Elem.Thuy);
            Assert.AreEqual(0, Badges.FightIndex(cfg, 1, 1));
            Assert.AreEqual(cfg.badges.counts[0], Badges.FightIndex(cfg, 2, 1));

            var r = Badges.Win(s, d, Elem.Thuy, 1, 1, 3, rng);
            Assert.AreEqual(cfg.badges.ballsBase + cfg.badges.ballsPerTier, r.balls);
            Assert.AreEqual(3, Badges.Stars(s, cfg, Elem.Thuy, 1, 1));
            Badges.Win(s, d, Elem.Thuy, 1, 2, 1, rng);
            int balls = s.balls;
            r = Badges.Win(s, d, Elem.Thuy, 1, 2, 2, rng);
            Assert.IsTrue(r.replay, "trận đã thắng là đánh lại");
            Assert.AreEqual(balls, s.balls, "đánh lại không có bi");
            Assert.AreEqual(2, Badges.Stars(s, cfg, Elem.Thuy, 1, 2), "đánh lại được nhiều sao hơn thì ghi");
            Badges.Win(s, d, Elem.Thuy, 1, 2, 1, rng);
            Assert.AreEqual(2, Badges.Stars(s, cfg, Elem.Thuy, 1, 2), "giữ sao cao nhất");
            Assert.IsNull(Badges.Win(s, d, Elem.Thuy, 1, 4, 3, rng), "trận chưa tới thì không thắng được");
            Badges.Win(s, d, Elem.Thuy, 1, 3, 1, rng);
            Badges.Win(s, d, Elem.Thuy, 1, 4, 1, rng);
            int evo = s.evoStones;
            r = Badges.Win(s, d, Elem.Thuy, 1, 5, 1, rng);
            Assert.AreEqual(1, r.tierDone);
            Assert.AreEqual(evo + cfg.badges.evo[0], s.evoStones, "xong bậc có đá tiến hóa");
            Assert.AreEqual(3 + 2 + 1 + 1 + 1, Badges.TierStars(s, cfg, Elem.Thuy, 1));

            // bản lưu trước 2026-11-17: bậc 3 có 10 trận, đã thắng 9; nay bậc 3 ít trận hơn: đang ở trận cuối, trận đã thắng tính 1 sao
            var o = SaveData.New(d, 0);
            o.zones[(int)Elem.Hoa] = Islands.Size(Elem.Hoa);
            o.badges[(int)Elem.Hoa].tier = 2;
            o.badges[(int)Elem.Hoa].won = 9;
            int n3 = Badges.Count(cfg, 3);
            Assert.AreEqual((3, n3), Badges.Current(o, cfg, Elem.Hoa).Value);
            Assert.AreEqual(1, Badges.Stars(o, cfg, Elem.Hoa, 1, 3));
            Assert.AreEqual(cfg.badges.counts[0] + cfg.badges.counts[1] + n3 - 1, Badges.LineStars(o, cfg, Elem.Hoa));
            Assert.AreEqual(3, Badges.Win(o, d, Elem.Hoa, 3, n3, 2, rng).tierDone);

            // mốc sao: mỗi giftEvery sao cả đền là một mốc, nhận ngay khi đủ
            var g = SaveData.New(d, 0);
            g.zones[(int)Elem.Kim] = Islands.Size(Elem.Kim);
            int got = 0, stars = 0;
            for (int t = 1; stars < cfg.badges.giftEvery; t++)
                for (int i = 1; i <= Badges.Count(cfg, t) && stars < cfg.badges.giftEvery; i++)
                {
                    got += Badges.Win(g, d, Elem.Kim, t, i, 3, rng).gifts.Count;
                    stars += 3;
                }
            Assert.AreEqual(1, got, "đủ giftEvery sao: một mốc");
            Assert.AreEqual(1, g.badgeGifts);
            Assert.AreEqual(Badges.MaxStars(cfg) / cfg.badges.giftEvery, Badges.GiftsTotal(cfg));

            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var back));
            Assert.AreEqual(s.badges[(int)Elem.Thuy].stars, back.badges[(int)Elem.Thuy].stars, "sao từng trận giữ khi lưu");
        }

        [Test]
        public void SaoCuaTran_DieuKien()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            s.level = 120;
            s.team = new List<string> { "ti_tach" };
            var stage = Badges.Stage(d, Elem.Hoa, 1, 1);
            var team = Teams.Player(s, null, d);
            team.ai = true;
            var b = Battle.Create(d, team, Teams.Enemy(stage, d), 7, 120, 120);
            BattleSim.Run(b);
            var (win, safe, fast) = Badges.StarChecks(cfg, b);
            Assert.AreEqual(b.winner == 0, win);
            Assert.AreEqual(win && !b.sides[0].fighters[0].dead, safe);
            Assert.AreEqual(win && b.round <= Badges.StarRounds(cfg, 1), fast);
            Assert.AreEqual(win ? 1 + (safe ? 1 : 0) + (fast ? 1 : 0) : 0, Badges.Grade(cfg, b));
            Assert.AreEqual(cfg.badges.starRounds * 3, Badges.StarRounds(cfg, 3), "sao 3 tính theo số địch");
        }

        [Test]
        public void DacTinhHe_PhanCongCaDoi()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            Assert.IsNull(Badges.Trait(s, cfg, Elem.Thuy), "chưa có huy hiệu thì chưa có đặc tính");
            int t1 = cfg.badges.traitTiers[0];
            s.badges[(int)Elem.Thuy].tier = t1 - 1;
            Assert.IsNull(Badges.Trait(s, cfg, Elem.Thuy));
            s.badges[(int)Elem.Thuy].tier = t1;
            var tr = Badges.Trait(s, cfg, Elem.Thuy);
            Assert.AreEqual(Potential.FromKey(cfg.badges.traitKind[(int)Elem.Thuy]), tr.Value.k);
            Assert.AreEqual(cfg.badges.traitValue[(int)Elem.Thuy * cfg.badges.traitTiers.Length], tr.Value.v, 1e-12);

            // đặc tính Thủy (khiên) vào trận qua BattleStart cho tướng Thủy, không cho tướng hệ khác
            Assert.AreEqual(PotKind.Shield, tr.Value.k, "Thủy: khiên đầu trận");
            s.Hero("cao_da").owned = true;
            var st = Potential.Start(s, d, "ti_tach");
            Assert.AreEqual(tr.Value.v, st.shield, 1e-12);
            Assert.IsNull(Potential.Start(s, d, "cao_da"), "tướng Thổ không có đặc tính Thủy");
            var b = Battle.Create(d, Teams.Player(s, new List<string> { "ti_tach" }, d), Teams.Enemy(Badges.Stage(d, Elem.Hoa, 1, 1), d), 3);
            var f = b.sides[0].fighters[0];
            Assert.AreEqual(Js.Round(f.maxHp * tr.Value.v), f.shield, "khiên đầu trận");

            // phần cộng cả đội: cộng theo bậc của từng dãy, áp cho mọi hệ
            for (int e = 0; e < 5; e++) s.badges[e].tier = Badges.MaxTier(cfg);
            double team = cfg.badges.teamBonus[Badges.MaxTier(cfg) - 1] * 5;
            Assert.AreEqual(team, Badges.TeamBonus(s, cfg), 1e-12);
            Assert.AreEqual(Badges.Bonus(cfg, Badges.MaxTier(cfg)) + team, Teams.MemberOf(s, "cao_da", d).mods.hpPct, 1e-12);
            Assert.IsNull(Badges.Current(s, cfg, Elem.Thuy), "xong bậc cuối thì không còn trận");
        }
    }
}
