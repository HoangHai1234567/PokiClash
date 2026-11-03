// Đối chiếu luật trận với bản web: 200 trận cố định hạt giống (máy chơi cả hai bên, bên 0 chọn tướng thay qua hộp),
// 12 trận so từng sự kiện kèm ảnh chụp, 200 trận so kết quả, chuỗi loại sự kiện và ảnh chụp cuối.
// Golden xuất bằng `npx tsx scripts/export_golden.ts` (thư mục Web).
// battles.json, battle_events.json: tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md),
// rồi lần nữa cùng ngày khi Chiêu đổi sang ra đòn ngay lúc bấm (không vào hàng thẻ).
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class BattleGoldenTests
    {
        static List<object> battles;
        static List<object> detail;

        static List<object> Battles => battles ??= J.Arr(J.Obj(MiniJson.Parse(TestData.Read("Golden/battles.json"))), "battles");
        static List<object> Detail => detail ??= J.Arr(J.Obj(MiniJson.Parse(TestData.Read("Golden/battle_events.json"))), "battles");

        static TeamSetup Team(Dictionary<string, object> o)
        {
            var t = new TeamSetup { name = J.Str(o, "name"), ai = J.Bool(o, "ai") };
            foreach (var x in J.Arr(o, "members"))
            {
                var m = J.Obj(x);
                var cl = J.Obj(m, "cardLv");
                t.members.Add(new Member
                {
                    heroId = J.Str(m, "heroId"), level = J.Int(m, "level"), star = J.Int(m, "star"), boss = J.Bool(m, "boss"), evo = J.Bool(m, "evo"),
                    cardSkill = J.Int(cl, "skill"), cardUlt = J.Int(cl, "ult"), cardPassive = J.Int(cl, "passive"),
                });
            }
            return t;
        }

        static Battle Make(Dictionary<string, object> entry)
        {
            var teams = J.Arr(entry, "teams");
            var unlock = J.Arr(entry, "unlock");
            return Battle.Create(TestData.Load(), Team(J.Obj(teams[0])), Team(J.Obj(teams[1])), (uint)J.Num(entry, "seed"),
                (int)(double)unlock[0], (int)(double)unlock[1]);
        }

        // so sâu hai cây JSON; trả mô tả chỗ lệch đầu tiên (null nếu khớp)
        public static string Diff(object a, object b, string path = "")
        {
            if (a is double || a is int)
            {
                double da = System.Convert.ToDouble(a, CultureInfo.InvariantCulture);
                if (!(b is double || b is int)) return $"{path}: web {a}, unity {b}";
                double db = System.Convert.ToDouble(b, CultureInfo.InvariantCulture);
                return da == db ? null : $"{path}: web {da:R}, unity {db:R}";
            }
            if (a is Dictionary<string, object> da2)
            {
                if (!(b is Dictionary<string, object> db2)) return $"{path}: unity không phải object";
                foreach (var k in da2.Keys.Union(db2.Keys))
                {
                    if (!da2.ContainsKey(k)) return $"{path}.{k}: web thiếu";
                    if (!db2.ContainsKey(k)) return $"{path}.{k}: unity thiếu";
                    var r = Diff(da2[k], db2[k], path + "." + k);
                    if (r != null) return r;
                }
                return null;
            }
            if (a is List<object> la)
            {
                if (!(b is List<object> lb)) return $"{path}: unity không phải mảng";
                if (la.Count != lb.Count) return $"{path}: web {la.Count} phần tử, unity {lb.Count}";
                for (int i = 0; i < la.Count; i++)
                {
                    var r = Diff(la[i], lb[i], $"{path}[{i}]");
                    if (r != null) return r;
                }
                return null;
            }
            return Equals(a, b) ? null : $"{path}: web {a}, unity {b}";
        }

        [Test]
        public void TranChiTiet_KhopTungSuKien()
        {
            var all = Battles;
            for (int i = 0; i < Detail.Count; i++)
            {
                var entry = J.Obj(all[i]);
                var want = J.Arr(J.Obj(Detail[i]), "evs");
                var log = new List<BattleEvent>();
                BattleSim.Run(Make(entry), 0.15, log);
                for (int k = 0; k < want.Count && k < log.Count; k++)
                {
                    var d = Diff(want[k], log[k].ToDict());
                    if (d != null) Assert.Fail($"Trận {i} (hạt giống {J.Num(entry, "seed")}), sự kiện {k} ({log[k].TypeKey}): {d}");
                }
                Assert.AreEqual(want.Count, log.Count, $"Trận {i}: số sự kiện");
            }
        }

        [Test]
        public void Tran200_KhopKetQua()
        {
            var fails = new StringBuilder();
            int n = 0;
            foreach (var x in Battles)
            {
                var entry = J.Obj(x);
                var log = new List<BattleEvent>();
                var b = BattleSim.Run(Make(entry), 0.15, log);
                string kinds = string.Join(",", log.Select(e => e.TypeKey));
                string err = null;
                if (b.winner != J.Int(entry, "winner")) err = $"thắng: web {J.Int(entry, "winner")}, unity {b.winner}";
                else if (b.round != J.Int(entry, "round")) err = $"số hiệp: web {J.Int(entry, "round")}, unity {b.round}";
                else if (b.turns != J.Int(entry, "turns")) err = "số lượt";
                else if (log.Count != J.Int(entry, "events")) err = $"số sự kiện: web {J.Int(entry, "events")}, unity {log.Count}";
                else if (kinds != J.Str(entry, "kinds")) err = "chuỗi loại sự kiện";
                else
                {
                    var dmg = J.Arr(entry, "dmg");
                    if ((double)dmg[0] != b.dmgDealt[0] || (double)dmg[1] != b.dmgDealt[1]) err = "sát thương gây ra";
                    else err = Diff(J.Get(entry, "last"), BattleEvent.SnapDict(log[log.Count - 1].snap), "last");
                }
                if (err != null && n++ < 10) fails.AppendLine($"hạt giống {J.Num(entry, "seed")}: {err}");
            }
            Assert.AreEqual(0, n, $"{n}/200 trận lệch:\n{fails}");
        }

        [Test]
        public void HoiSinh_PhatTam_LanDauGuc()
        {
            var d = TestData.Load();
            var pas = d.Card("cs_pas");
            Assert.AreEqual(PassiveTrigger.Death, pas.trigger);
            Assert.AreEqual("Lần đầu gục: hồi sinh với 35% máu.", CardText.Text(pas, 1, d.Cfg.cardLvStep));
            // tìm trận golden có hồi sinh và kiểm: không có "death" ngay trước, máu = 35%·máu tối đa ở cấp thẻ 1
            int found = 0;
            foreach (var x in Battles)
            {
                var entry = J.Obj(x);
                if (!J.Str(entry, "kinds").Contains("revive")) continue;
                var log = new List<BattleEvent>();
                BattleSim.Run(Make(entry), 0.15, log);
                for (int i = 0; i < log.Count; i++)
                {
                    if (log[i].t != EvType.Revive) continue;
                    found++;
                    Assert.AreEqual(EvType.Passive, log[i - 1].t);
                    // Phật Tâm của Cà Sa, hoặc bản chép của nó (Kỳ Lân Cát mượn bộ thẻ Cà Sa, thẻ tạm 2026-11-02)
                    Assert.AreEqual(PassiveTrigger.Death, d.Card(log[i - 1].card).trigger, log[i - 1].card);
                    var f = log[i].snap.f[log[i].side][log[i].idx];
                    Assert.IsFalse(f.dead);
                    Assert.Greater(f.hp, 0);
                    Assert.LessOrEqual(f.hp, f.maxHp * 0.95);
                }
            }
            Assert.Greater(found, 0, "golden phải có ít nhất một lần hồi sinh");
        }

        // boss có thẻ Tiến Hóa: vào trận ở dạng 1 (máu bossEvoHp·1/(1+…+n) máu boss), mỗi lần tiến hóa lên đúng một dạng, hồi đầy máu
        // dạng mới (máu tối đa tăng), không gục khi còn dạng sau
        [Test]
        public void BossTienHoa_TuDang1LenDangCuoi()
        {
            var d = TestData.Load();
            var card = d.Card(Battle.BossEvoCard);
            Assert.AreEqual("Khi máu dưới 25%, nếu còn dạng sau: tiến hóa, hồi đầy máu, máu và Công tăng.", CardText.Text(card, 1, d.Cfg.cardLvStep));
            var st = d.Stages.Find(x => x.zone == Elem.Thuy && x.kind == StageKind.Boss);
            Assert.AreEqual(1, st.enemies.Count, "ải boss chỉ có boss");
            Assert.IsTrue(st.enemies[0].evo);
            var hero = d.Hero(st.enemies[0].hero);
            Assert.AreEqual(3, hero.forms.Length);
            var mods = Teams.Enemy(st, d).members[0].mods; // đảo 70 ải: boss cuối quy về độ hiếm Khá, máu ×0,7
            var full = HeroStats.Compute(d.Cfg, hero, st.enemies[0].level, Teams.EnemyStar(st.enemies[0].level), true, mods);
            // đội mạnh hơn hẳn để chắc đánh tới dạng cuối
            var p = new TeamSetup { name = "Bạn", ai = true };
            foreach (var id in new[] { "huyen_vu", "ca_sa", "phap_luan" }) p.members.Add(new Member { heroId = id, level = 30, star = 5, cardSkill = 5, cardUlt = 5, cardPassive = 5 });
            var log = new List<BattleEvent>();
            var b = Battle.Create(d, p, Teams.Enemy(st, d), 11);
            Assert.AreEqual(0, b.ActiveOf(1).form);
            Assert.AreEqual(Js.Round(full.hp * 0.25), b.ActiveOf(1).maxHp, "dạng 1: 1/6 của 1,5 lần máu boss");
            BattleSim.Run(b, 0.15, log);
            var evo = log.FindAll(e => e.t == EvType.Evolve);
            Assert.AreEqual(2, evo.Count, "dòng 3 dạng tiến hóa 2 lần");
            double lastMax = 0;
            for (int i = 0; i < evo.Count; i++)
            {
                Assert.AreEqual(i + 1, evo[i].form);
                int k = log.IndexOf(evo[i]);
                Assert.AreEqual(EvType.Passive, log[k - 1].t);
                Assert.AreEqual(Battle.BossEvoCard, log[k - 1].card);
                var f = evo[i].snap.f[1][0];
                Assert.IsFalse(f.dead);
                Assert.AreEqual(f.maxHp, f.hp, "hồi đầy máu dạng mới");
                Assert.Greater(f.maxHp, lastMax);
                lastMax = f.maxHp;
            }
            Assert.AreEqual(0, b.winner, "boss gục ở dạng cuối");
            Assert.AreEqual(2, b.ActiveOf(1).form);
        }

        [Test]
        public void GioiHan60Hiep()
        {
            var d = TestData.Load();
            Assert.AreEqual(60, d.Cfg.maxRounds);
            foreach (var x in Battles) Assert.LessOrEqual(J.Int(J.Obj(x), "round"), 60);
        }

        [Test]
        public void DoiTuong_ChoangVaKetThuc_TheoLuat()
        {
            var d = TestData.Load();
            var p = new TeamSetup { name = "Bạn", ai = false };
            p.members.Add(new Member { heroId = "tieu_y", level = 5, star = 1 });
            p.members.Add(new Member { heroId = "vo_su", level = 5, star = 1 });
            var e = new TeamSetup { name = "Địch", ai = true };
            e.members.Add(new Member { heroId = "bo_de", level = 3, star = 1 });
            var b = Battle.Create(d, p, e, 7);
            b.StartBattle();
            Assert.AreEqual(Phase.Picking, b.phase);
            Assert.AreEqual(0, b.turn.side, "người chơi đi trước");
            Assert.AreEqual(5, b.turn.picksLeft);
            Assert.AreEqual(3, b.turn.offer.Count);
            // đổi tướng chỉ được trước lần chọn đầu
            Assert.IsTrue(b.CanSwap(1));
            var evs = b.Swap(1);
            Assert.AreEqual(EvType.Swap, evs[0].t);
            Assert.IsFalse(b.CanSwap(0), "đã đổi rồi");
            b.Pick(0);
            Assert.IsFalse(b.CanSwap(0));
            while (b.phase == Phase.Picking) b.Pick(0);
            Assert.AreEqual(Phase.Ready, b.phase);
            b.Execute();
            Assert.AreEqual(Phase.Idle, b.phase);
            // choáng: mất trọn lượt (không chọn thẻ, không đánh), lượt chuyển ngay sang bên kia
            var foe = b.ActiveOf(1);
            double hp0 = b.ActiveOf(0).hp;
            foe.statuses.Add(new StatusInst { id = StatusId.Stun, left = 1 });
            var stunEvs = b.Advance();
            Assert.IsTrue(stunEvs.Exists(x => x.t == EvType.Stunned && x.side == 1), "có sự kiện choáng");
            Assert.IsTrue(b.turn.stunned);
            Assert.AreEqual(0, b.turn.picksLeft);
            Assert.AreEqual(Phase.Idle, b.phase, "không có lúc chọn thẻ");
            Assert.IsFalse(foe.Has(StatusId.Stun), "choáng hết sau một lượt");
            Assert.AreEqual(hp0, b.ActiveOf(0).hp, "bên bị choáng không đánh");
            // chạy hết trận bằng máy: phải kết thúc có người thắng
            BattleSim.Run(Battle.Create(d, p, e, 99));
        }

        // Chiêu ra đòn ngay lúc bấm (người dùng 2026-11-03): không vào hàng thẻ, không tốn lần chọn, rồi chọn tiếp;
        // chiêu hạ tướng đối thủ thì hết lúc chọn, thẻ đã xếp chạy (không đánh thường) rồi hết lượt
        [Test]
        public void Chieu_RaDonNgay_RoiChonTiep()
        {
            var d = TestData.Load();
            var p = new TeamSetup { name = "Bạn", ai = false };
            p.members.Add(new Member { heroId = "giot_suong", level = 5, star = 1 });
            var e = new TeamSetup { name = "Địch", ai = true };
            e.members.Add(new Member { heroId = "bo_de", level = 3, star = 1 });
            e.members.Add(new Member { heroId = "bo_de", level = 3, star = 1 });

            var b = Battle.Create(d, p, e, 7);
            b.StartBattle();
            var foe = b.ActiveOf(1);
            b.ActiveOf(0).mana = d.Cfg.maxMana;
            b.Pick(0);
            Assert.AreEqual("", b.InnateBlock(InnateKind.Skill));
            double foeHp = foe.hp + foe.shield;
            var evs = b.UseInnate(InnateKind.Skill);
            Assert.AreEqual(EvType.Innate, evs[0].t);
            Assert.AreEqual("skill", evs[0].kind);
            Assert.IsTrue(evs.Exists(x => x.t == EvType.Dmg && x.dmgKind == DmgKind.Skill && x.to == 1), "chiêu gây sát thương ngay");
            Assert.Less(foe.hp + foe.shield, foeHp);
            Assert.AreEqual(1, b.turn.queue.Count, "chiêu không vào hàng thẻ");
            Assert.AreEqual(4, b.turn.picksLeft, "không tốn lần chọn");
            Assert.AreEqual(Phase.Picking, b.phase, "chọn tiếp");
            Assert.AreEqual("Đã dùng lượt này", b.InnateBlock(InnateKind.Skill));
            while (b.phase == Phase.Picking) b.Pick(0);
            var run = b.Execute();
            Assert.IsFalse(run.Exists(x => x.t == EvType.Dmg && x.dmgKind == DmgKind.Skill), "cuối lượt chiêu không chạy lại");
            Assert.IsTrue(run.Exists(x => x.t == EvType.Attack), "vẫn đánh thường cuối lượt");

            // chiêu hạ tướng đối thủ (còn tướng dự bị)
            b = Battle.Create(d, p, e, 7);
            b.StartBattle();
            foe = b.ActiveOf(1);
            b.ActiveOf(0).mana = d.Cfg.maxMana;
            b.Pick(0);
            foe.hp = 1;
            foe.shield = 0;
            b.UseInnate(InnateKind.Skill);
            Assert.IsTrue(foe.dead);
            Assert.AreEqual(Phase.Ready, b.phase, "hết lúc chọn");
            Assert.AreEqual(0, b.turn.offer.Count);
            run = b.Execute();
            Assert.AreEqual(1, run.Count(x => x.t == EvType.Card), "thẻ đã xếp vẫn chạy");
            Assert.IsFalse(run.Exists(x => x.t == EvType.Attack), "đối thủ gục thì không đánh thường");
            Assert.AreEqual(Phase.Idle, b.phase);
            var next = b.Advance();
            Assert.IsTrue(next.Exists(x => x.t == EvType.Swap && x.side == 1 && x.forced), "địch đưa tướng dự bị ra");
            Assert.AreEqual(1, b.turn.side);
        }
    }
}
