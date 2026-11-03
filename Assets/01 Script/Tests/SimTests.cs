// Công cụ cân bằng: bảng 102 ải × 5 mức cấp của Unity phải ra đúng từng ô như npm run sim -- battle (golden sim.json),
// mô phỏng máy bi ra tỉ lệ khớp bảng đo của web, mô phỏng tiến độ chạy được và có thứ tự hợp lý giữa các kiểu người chơi.
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class SimTests
    {
        [Test]
        public void BangAi_KhopTungO_VoiBanWeb()
        {
            var d = TestData.Load();
            var g = J.Obj(MiniJson.Parse(TestData.Read("Golden/sim.json")));
            int n = J.Int(g, "n");
            int cells = 0;
            foreach (var zx in J.Arr(g, "zones"))
            {
                var zo = J.Obj(zx);
                var zone = d.Zone(Keys.ToElem(J.Str(zo, "zone")));
                var levels = Sim.Levels(zone);
                CollectionAssert.AreEqual(J.Arr(zo, "levels").Select(x => (int)(double)x).ToArray(), levels, zone.name + " mức cấp");
                var tm = d.Cfg.SimTeamOf(zone.id);
                foreach (var sx in J.Arr(zo, "stages"))
                {
                    var so = J.Obj(sx);
                    var st = d.Stage(J.Int(so, "id"));
                    var wc = J.Arr(so, "cells");
                    for (int i = 0; i < levels.Length; i++)
                    {
                        var s = Sim.Setup(d, tm.team, levels[i], tm.star, tm.card);
                        var c = Sim.Stage(d, s, st, n);
                        var w = J.Obj(wc[i]);
                        string at = $"{zone.name} ải {st.idx} cấp {levels[i]}";
                        Assert.AreEqual(J.Int(w, "win"), c.win, at + " số trận thắng");
                        Assert.AreEqual(J.Num(w, "rounds"), c.rounds, at + " tổng số hiệp");
                        cells++;
                    }
                }
            }
            Assert.AreEqual(d.Stages.Count * 5, cells);
        }

        [Test]
        public void MayBi_TiLeKhopBangDo_BiHoanDuoiNuaBi()
        {
            var d = TestData.Load();
            var r = Sim.Machine(d, chestOpens: 2000);
            foreach (var kv in r.count)
                Assert.AreEqual(d.Cfg.Rate(Pachinko.Key(kv.Key)), r.Rate(kv.Key), 0.01, Pachinko.Key(kv.Key));
            Assert.Less(r.backPerBall, 0.5);
            Assert.Greater(r.expPerBall, 5);
            TestContext.WriteLine($"Mỗi bi ×1: {r.expPerBall:0.00} EXP, hoàn {r.backPerBall:0.000} bi, {r.cardsPerBall:0.000} thẻ");
        }

        [Test]
        public void TienDo_10Ngay_ChamNhanhHonIt_ChayLaiGiongNhau()
        {
            var d = TestData.Load();
            var ps = ProgressSim.DefaultProfiles();
            var cache = new System.Collections.Generic.Dictionary<string, double>();
            var cham = ProgressSim.Run(d, ps[0], 10, 1, 4, cache);
            var it = ProgressSim.Run(d, ps[2], 10, 1, 4, cache);
            var again = ProgressSim.Run(d, ps[2], 10, 1, 4, cache);
            Assert.Greater(cham.level[10], 1);
            Assert.GreaterOrEqual(cham.level[10], it.level[10]);
            Assert.GreaterOrEqual(cham.cleared[10], it.cleared[10]);
            CollectionAssert.AreEqual(it.level, again.level, "cùng hạt giống thì cùng kết quả");
            TestContext.WriteLine($"Ngày 10: chăm cấp {cham.level[10]} ({cham.cleared[10]} ải), ít cấp {it.level[10]} ({it.cleared[10]} ải)");
        }
    }
}
