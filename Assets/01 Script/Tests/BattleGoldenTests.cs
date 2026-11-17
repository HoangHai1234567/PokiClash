// Đối chiếu luật trận với bản web: 200 trận cố định hạt giống (máy chơi cả hai bên, bên 0 chọn tướng thay qua hộp),
// 12 trận so từng sự kiện kèm ảnh chụp, 200 trận so kết quả, chuỗi loại sự kiện và ảnh chụp cuối.
// Golden xuất bằng `npx tsx scripts/export_golden.ts` (thư mục Web).
// battles.json, battle_events.json: tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md),
// rồi lần nữa cùng ngày khi Chiêu đổi sang ra đòn ngay lúc bấm (không vào hàng thẻ); lần nữa 2026-11-04 khi đổi luật rút thẻ
// (35 thẻ chung, thẻ đã chọn không ra lại trong lượt). 2026-11-17: 75 thẻ chung, cơ chế mới, boss tiến hóa khi gục: phải tính lại
// battles.json, battle_events.json (Claude chính tính khi gom).
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

        // boss có thẻ Tiến Hóa: vào trận ở dạng 1 (máu bossEvoHp·1/(1+…+n)·bossEvoEarly máu boss), mỗi lần tiến hóa lên đúng một dạng,
        // dạng mới vào trận đầy máu (máu tối đa tăng). Luật 2026-11-17: dạng chưa cuối tiến hóa khi về 0 máu (trước: dưới 25% máu);
        // chuỗi sự kiện: đòn đưa máu về 0 → Passive boss_evo (ảnh chụp dạng cũ, máu 0, chưa gục) → Evolve
        [Test]
        public void BossTienHoa_TuDang1LenDangCuoi()
        {
            var d = TestData.Load();
            var card = d.Card(Battle.BossEvoCard);
            Assert.AreEqual("Khi gục, nếu còn dạng sau: tiến hóa, dạng sau vào trận đầy máu, máu và Công tăng.", CardText.Text(card, 1, d.Cfg.cardLvStep));
            Assert.AreEqual(0.75, d.Cfg.bossEvoEarly, "máu các dạng chưa cuối ×0,75 cho tổng máu phải đánh như luật cũ");
            var st = d.Stages.Find(x => x.zone == Elem.Thuy && x.kind == StageKind.Boss);
            Assert.AreEqual(1, st.enemies.Count, "ải boss chỉ có boss");
            Assert.IsTrue(st.enemies[0].evo);
            var hero = d.Hero(st.enemies[0].hero);
            Assert.AreEqual(3, hero.forms.Length);
            var mods = Teams.Enemy(st, d).members[0].mods; // đảo 70 ải: boss cuối quy về độ hiếm Khá, máu ×0,7
            var full = HeroStats.Compute(d.Cfg, hero, st.enemies[0].level, Teams.EnemyStar(st.enemies[0].level), true, mods);
            // đội mạnh hơn hẳn để chắc đánh tới dạng cuối
            var p = new TeamSetup { name = "Bạn", ai = true };
            int lv = st.enemies[0].level; // ngang cấp boss (thang 200)
            // sao tối đa của thang đang dùng (thang 1..20 từ 2026-11-17; trước 5)
            foreach (var id in new[] { "han_ngac", "ca_sa", "giap_long" })
                p.members.Add(new Member { heroId = id, level = lv, star = d.Cfg.maxStar, cardSkill = 5, cardUlt = 5, cardPassive = 5 });
            var log = new List<BattleEvent>();
            var b = Battle.Create(d, p, Teams.Enemy(st, d), 11);
            Assert.AreEqual(0, b.ActiveOf(1).form);
            Assert.AreEqual(Js.Round(full.hp * 0.1875), b.ActiveOf(1).maxHp, "dạng 1: 0,75 × 1/6 của 1,5 lần máu boss");
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
                // dạng cũ gục: ảnh chụp của Passive và của sự kiện trước đó còn dạng cũ, máu 0, chưa dead
                var old = log[k - 1].snap.f[1][0];
                Assert.AreEqual(0, old.hp, "dạng cũ về 0 máu rồi mới tiến hóa");
                Assert.IsFalse(old.dead);
                Assert.AreEqual(0, log[k - 2].snap.f[1][0].hp, $"sự kiện trước Passive ({log[k - 2].TypeKey}) đưa máu về 0");
                Assert.IsFalse(log.GetRange(0, k).Exists(e => e.t == EvType.Death && e.side == 1), "boss không có sự kiện gục trước khi tiến hóa");
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
            p.members.Add(new Member { heroId = "thach_giai", level = 5, star = 1 });
            p.members.Add(new Member { heroId = "vo_su", level = 5, star = 1 });
            var e = new TeamSetup { name = "Địch", ai = true };
            e.members.Add(new Member { heroId = "nguu_quyen", level = 3, star = 1 });
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

        // luật rút thẻ (người dùng dặn 2026-11-04): thẻ đã chọn không ra lại trong lượt, trừ thẻ có cờ repeat; sang lượt sau thì ra lại được
        [Test]
        public void TheDaChon_KhongRaLaiTrongLuot_TruTheLapLai()
        {
            var d = TestData.Load();
            Assert.IsTrue(d.Card("nem_da").repeat, "Ném Đá ra lại được");
            Assert.IsFalse(d.Card("cuong_no").repeat, "Cuồng Nộ mỗi lượt một lần");
            var p = new TeamSetup { name = "Bạn", ai = false };
            p.members.Add(new Member { heroId = "vo_su", level = 5, star = 1 });
            var e = new TeamSetup { name = "Địch", ai = true };
            e.members.Add(new Member { heroId = "nguu_quyen", level = 3, star = 1 });
            int repeatSeen = 0, onceNextTurn = 0;
            for (uint seed = 1; seed <= 200; seed++)
            {
                var b = Battle.Create(d, p, e, seed, 10, 10);
                b.StartBattle();
                while (b.phase == Phase.Picking)
                {
                    Assert.AreEqual(3, b.turn.offer.Distinct().Count(), "3 thẻ khác nhau");
                    foreach (var id in b.turn.offer)
                    {
                        Assert.LessOrEqual(d.Card(id).unlock, 10, id);
                        if (!b.turn.queue.Exists(q => q.card == id)) continue;
                        Assert.IsTrue(d.Card(id).repeat, $"hạt giống {seed}: {id} đã chọn mà ra lại");
                        repeatSeen++;
                    }
                    // ưu tiên thẻ một lần để hàng thẻ có nhiều thẻ bị loại
                    int i = b.turn.offer.FindIndex(id => !d.Card(id).repeat);
                    b.Pick(i < 0 ? 0 : i);
                }
                var once = b.turn.queue.Select(q => q.card).Where(id => !d.Card(id).repeat).ToList();
                b.Execute();
                // máy đánh lượt địch, về lại lượt chọn của người chơi
                for (int guard = 0; guard < 50 && b.phase != Phase.Over && !(b.phase == Phase.Picking && b.turn.side == 0); guard++)
                {
                    if (b.phase == Phase.Picking)
                    {
                        BattleAi.Turn(b);
                        b.Execute();
                    }
                    else if (b.phase == Phase.ForceSwap) b.ForceSwap(b.AiForcedChoice(b.turn.side));
                    else b.Advance();
                }
                if (b.phase == Phase.Picking && b.turn.offer.Exists(once.Contains)) onceNextTurn++;
            }
            Assert.Greater(repeatSeen, 0, "thẻ có cờ repeat vẫn ra lại trong lượt");
            Assert.Greater(onceNextTurn, 0, "lượt sau thẻ một lần ra lại được");
        }

        // Chiêu ra đòn ngay lúc bấm (người dùng 2026-11-03): không vào hàng thẻ, không tốn lần chọn, rồi chọn tiếp;
        // chiêu hạ tướng đối thủ thì hết lúc chọn, thẻ đã xếp chạy (không đánh thường) rồi hết lượt
        [Test]
        public void Chieu_RaDonNgay_RoiChonTiep()
        {
            var d = TestData.Load();
            var p = new TeamSetup { name = "Bạn", ai = false };
            p.members.Add(new Member { heroId = "ti_tach", level = 5, star = 1 });
            var e = new TeamSetup { name = "Địch", ai = true };
            e.members.Add(new Member { heroId = "nguu_quyen", level = 3, star = 1 });
            e.members.Add(new Member { heroId = "nguu_quyen", level = 3, star = 1 });

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

        // ---------- 75 thẻ chung, cơ chế mới (2026-11-17) ----------

        // mỗi thẻ một tác dụng (không trùng cây hiệu ứng), mở rải trên thang cấp 1–200, mô tả tự sinh không rỗng
        [Test]
        public void TheChung_75The_KhongTrungTacDung_RaiTheoCap()
        {
            var d = TestData.Load();
            Assert.AreEqual(75, d.Pool.Count);
            var dup = d.Pool.GroupBy(c => c.effectsJson).Where(g => g.Count() > 1).Select(g => string.Join("/", g.Select(c => c.id))).ToList();
            Assert.IsEmpty(dup, "thẻ trùng tác dụng: " + string.Join(", ", dup));
            foreach (var (lo, hi) in new[] { (1, 10), (11, 40), (41, 80), (81, 120), (121, 160), (161, 200) })
                Assert.IsTrue(d.Pool.Exists(c => c.unlock >= lo && c.unlock <= hi), $"có thẻ mở ở cấp {lo}–{hi}");
            foreach (var c in d.Pool) Assert.Greater(CardText.Text(c, 1, d.Cfg.cardLvStep).Length, 5, c.id);
        }

        static Battle Duel(GameData d, int foes = 1)
        {
            var p = new TeamSetup { name = "Bạn", ai = false };
            p.members.Add(new Member { heroId = "vo_su", level = 30, star = 1 });
            var e = new TeamSetup { name = "Địch", ai = true };
            for (int i = 0; i < foes; i++) e.members.Add(new Member { heroId = "nguu_quyen", level = 30, star = 1 });
            var b = Battle.Create(d, p, e, 5, 200, 200);
            b.StartBattle();
            return b;
        }

        // xếp sẵn hàng thẻ của người chơi rồi chạy lượt
        static List<BattleEvent> RunQueue(Battle b, params string[] cards)
        {
            b.turn.queue.Clear();
            foreach (var c in cards) b.turn.queue.Add(new QueueItem { card = c, lv = 1 });
            b.turn.picksLeft = 0;
            b.turn.offer.Clear();
            b.phase = Phase.Ready;
            return b.Execute();
        }

        // độc: cộng dồn lớp (chặn 5), mỗi lớp theo Công kẻ tẩm, chạy đầu lượt của tướng trúng độc; kích nổ gây ngay phần còn lại;
        // tướng trúng độc gục thì độc lan sang tướng ra thay
        [Test]
        public void Doc_CongDon_KichNo_LanKhiGuc()
        {
            var d = TestData.Load();
            var b = Duel(d);
            var foe = b.ActiveOf(1);
            RunQueue(b, "kim_doc", "kim_doc", "van_doc", "kim_doc");
            var p = foe.statuses.Find(x => x.id == StatusId.Poison);
            double per = b.PoisonPerStack(b.ActiveOf(0), foe, 0.15);
            Assert.AreEqual(5, p.stacks, "chặn ở 5 lớp");
            Assert.AreEqual(4, p.left, "số lượt dài nhất (Vạn Độc 4 lượt)");
            Assert.AreEqual(5 * per, p.v);
            var evs = b.Advance();
            var dot = evs.Find(x => x.t == EvType.Dmg && x.dmgKind == DmgKind.Poison);
            Assert.AreEqual(Js.Round(5 * per), dot.amount, "độc chạy đầu lượt của địch");
            Assert.AreEqual(5, dot.snap.f[1][0].stk[0], "ảnh chụp ghi số lớp độc");
            var side1 = (List<object>)((List<object>)BattleEvent.SnapDict(dot.snap)["f"])[1];
            var st0 = (List<object>)((List<object>)((Dictionary<string, object>)side1[0])["st"])[0];
            Assert.AreEqual(3, st0.Count, "JSON ảnh chụp: [\"poison\", lượt, lớp]");

            b = Duel(d);
            foe = b.ActiveOf(1);
            evs = RunQueue(b, "kim_doc", "kim_doc", "boc_doc");
            per = b.PoisonPerStack(b.ActiveOf(0), foe, 0.15);
            var det = evs.FindAll(x => x.t == EvType.Dmg && x.dmgKind == DmgKind.Poison);
            Assert.AreEqual(1, det.Count);
            Assert.AreEqual(Js.Round(2 * per * 3 * 1.5), det[0].amount, "Bộc Độc: 150% của 2 lớp × 3 lượt còn lại");
            Assert.IsFalse(foe.Has(StatusId.Poison));

            b = Duel(d, 2);
            var f0 = b.ActiveOf(1);
            RunQueue(b, "kim_doc", "kim_doc");
            f0.hp = 1;
            f0.shield = 0;
            RunQueue(b, "nem_da");
            Assert.IsTrue(f0.dead);
            evs = b.Advance();
            var f1 = b.ActiveOf(1);
            Assert.AreNotSame(f0, f1);
            Assert.IsTrue(f1.statuses.Exists(x => x.id == StatusId.Poison && x.stacks == 2), "độc lan sang tướng ra thay");
            Assert.IsTrue(evs.Exists(x => x.t == EvType.Status && x.status == StatusId.Poison && x.side == 1));
        }

        // phản đòn (hạ gục được kẻ đánh), kết liễu (boss nhận ×2), combo theo nhóm thẻ, cường hóa thẻ kế tiếp, chặn hồi máu, đập khiên
        [Test]
        public void PhanDon_KetLieu_Combo_CuongHoa_ChanHoi_DapKhien()
        {
            var d = TestData.Load();
            // phản đòn: mỗi đòn trúng phản 30% (cả phần khiên đỡ)
            var b = Duel(d);
            RunQueue(b, "gai_nhon");
            var evs = b.Advance();
            evs.AddRange(BattleAi.Turn(b));
            evs.AddRange(b.Execute());
            var hits = evs.FindAll(x => x.t == EvType.Dmg && x.from == 1 && x.to == 0 && !x.dodged && x.dmgKind != DmgKind.Burn && x.dmgKind != DmgKind.Poison);
            var th = evs.FindAll(x => x.t == EvType.Dmg && x.dmgKind == DmgKind.Thorns);
            Assert.AreEqual(hits.Count, th.Count, "mỗi đòn trúng một lần phản");
            Assert.AreEqual(Js.Round((hits[0].toHp + hits[0].blocked) * 0.3), th[0].amount);
            // phản đòn hạ gục kẻ đánh giữa lượt: thẻ sau thôi chạy
            b = Duel(d);
            var me = b.ActiveOf(0);
            b.ActiveOf(1).buffs.Add(new Buff { stat = Stat.Thorns, v = 5, left = 99, until = Until.End });
            me.hp = 5;
            evs = RunQueue(b, "nem_da", "mai_vuot");
            Assert.IsTrue(me.dead);
            Assert.IsFalse(evs.Exists(x => x.t == EvType.Card && x.card == "mai_vuot"));
            Assert.AreEqual(1, b.winner);

            // kết liễu: địch thường dưới 15% gục ngay; boss nhận sát thương ×2, không gục ngay
            b = Duel(d);
            var foe = b.ActiveOf(1);
            foe.hp = System.Math.Floor(foe.maxHp * 0.14);
            RunQueue(b, "ket_lieu");
            Assert.IsTrue(foe.dead);

            // combo: Chuỗi Đòn đếm thẻ đánh khác trong hàng (2 Ném Đá), không đếm Mài Vuốt
            b = Duel(d);
            evs = RunQueue(b, "chuoi_don", "nem_da", "nem_da", "mai_vuot");
            Assert.AreEqual(4, evs.Count(x => x.t == EvType.Dmg && x.to == 1 && x.dmgKind == DmgKind.Card), "gốc + combo + 2 Ném Đá");
            b = Duel(d);
            me = b.ActiveOf(0);
            evs = RunQueue(b, "tuong_thanh", "thu_the", "mai_rua", "gai_nhon");
            Assert.AreEqual(Js.Round(me.maxHp * 0.15), evs.FindAll(x => x.t == EvType.Shield)[1].amount, "Tường Thành: 3 thẻ thủ khác × 5%");

            // cường hóa: thẻ kế tiếp mạnh thêm 50%, dùng một lần
            b = Duel(d);
            evs = RunQueue(b, "tich_luc", "mai_vuot", "mai_vuot");
            var atk = evs.FindAll(x => x.t == EvType.Buff && x.stat == Stat.Atk);
            Assert.AreEqual(0.38, atk[0].v, 1e-9);
            Assert.AreEqual(0.25, atk[1].v, 1e-9);

            // chặn hồi: Cắt Mạch làm địch không hồi được máu
            b = Duel(d);
            RunQueue(b, "cat_mach");
            Assert.AreEqual(-1, Battle.BuffSum(b.ActiveOf(1), Stat.HealTaken));

            // đập khiên: tiêu hết khiên, sát thương bằng số khiên
            b = Duel(d);
            me = b.ActiveOf(0);
            evs = RunQueue(b, "thu_the", "thu_the", "dap_khien");
            Assert.AreEqual(0, me.shield);
            Assert.AreEqual(Js.Round(me.maxHp * 0.34), evs.Find(x => x.t == EvType.Dmg && x.to == 1 && x.dmgKind == DmgKind.Card).amount);
        }
    }
}
