// Tiến trình so với bản web (golden): chỉ số 11 tướng × cấp 1/10/20/30 × sao 1/3/5 × boss, chuỗi thẻ rơi từ rương,
// chuỗi mảnh tướng; và luật nâng thẻ, tiến hóa, đội hình.
// progression.json (chỉ số 5 tướng khởi đầu, Võ Sư): tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md).
using System.Collections.Generic;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class ProgressionTests
    {
        static Dictionary<string, object> golden;
        static Dictionary<string, object> G => golden ??= J.Obj(MiniJson.Parse(TestData.Read("Golden/progression.json")));

        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        [Test]
        public void ChiSoTuong_KhopBanWeb()
        {
            var d = TestData.Load();
            int n = 0;
            foreach (var x in J.Arr(G, "stats"))
            {
                var o = J.Obj(x);
                var st = HeroStats.Compute(d.Cfg, d.Hero(J.Str(o, "id")), J.Int(o, "lv"), J.Int(o, "st"), J.Bool(o, "boss"));
                string at = $"{J.Str(o, "id")} cấp {J.Int(o, "lv")} sao {J.Int(o, "st")} boss {J.Bool(o, "boss")}";
                Assert.AreEqual(J.Num(o, "hp"), st.hp, at + " máu");
                Assert.AreEqual(J.Num(o, "atk"), st.atk, at + " công");
                Assert.AreEqual(J.Num(o, "def"), st.def, at + " thủ");
                Assert.AreEqual(J.Num(o, "spd"), st.spd, at + " tốc");
                n++;
            }
            Assert.AreEqual(d.Heroes.Count * 4 * 3 * 2, n);
        }

        [Test]
        public void ModsCongThemPhanTram()
        {
            var d = TestData.Load();
            var h = d.Hero("lam_quan");
            var a = HeroStats.Compute(d.Cfg, h, 10, 1);
            var b = HeroStats.Compute(d.Cfg, h, 10, 1, false, new StatMods { atkPct = 0.1, spd = 3 });
            Assert.AreEqual(a.hp, b.hp);
            Assert.AreEqual(Js.Round(a.atk * 1.1), b.atk, 1);
            Assert.AreEqual(a.spd + 3, b.spd);
            // Bọ Cạp Đồng (Hiếm) mạnh hơn Bu Lông (Thường) cùng cấp, cùng sao
            var c = HeroStats.Compute(d.Cfg, d.Hero("bu_long"), 10, 1);
            var v = HeroStats.Compute(d.Cfg, d.Hero("bo_cap"), 10, 1);
            Assert.Greater(v.hp + v.atk + v.def, c.hp + c.atk + c.def);
        }

        [Test]
        public void TheRoiTuRuong_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "vo_su", "ca_ngua", "phap_luan", "ca_sa" }) s.Hero(id).owned = true;
            var r = new Rng(77);
            var want = J.Arr(G, "drops");
            for (int i = 0; i < want.Count; i++)
            {
                var drop = Progress.RollCardDrop(s, d, (Rarity)r.Int(0, 4), r);
                var w = J.Arr(want[i]);
                if (want[i] == null)
                {
                    Assert.IsNull(drop, $"lần {i}");
                    continue;
                }
                Assert.IsNotNull(drop, $"lần {i}");
                Assert.AreEqual((string)w[0], drop.hero, $"lần {i}: tướng");
                Assert.AreEqual((string)w[1], SlotKey[(int)drop.slot], $"lần {i}: ô");
                Assert.AreEqual((string)w[2], drop.card, $"lần {i}: thẻ");
                Assert.AreEqual((string)w[3], Keys.Of(drop.rarity), $"lần {i}: độ hiếm");
            }
        }

        [Test]
        public void TheRoi_LuiDoHiem_KhongCoThiNull()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0); // chỉ có Giọt Sương: bộ thẻ tạm chép của Tiểu Y là thường/khá/hiếm...
            var drop = Progress.RollCardDrop(s, d, Rarity.Legend, new Rng(1));
            Assert.IsNotNull(drop);
            Assert.AreEqual("giot_suong", drop.hero);
            s.Hero("giot_suong").owned = false;
            Assert.IsNull(Progress.RollCardDrop(s, d, Rarity.Epic, new Rng(1)), "không có tướng nào: null (đổi thành EXP)");
        }

        [Test]
        public void ManhTuong_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var r = new Rng(5);
            foreach (var x in J.Arr(G, "shards"))
            {
                var w = J.Arr(x);
                string hero = d.Heroes[r.Int(0, d.Heroes.Count - 1)].id;
                int n = r.Int(1, 6);
                var res = Progress.AddShards(s, d, hero, n, r);
                Assert.AreEqual((string)w[0], hero);
                Assert.AreEqual((double)w[1], n);
                Assert.AreEqual((bool)w[2], res.unlocked, hero + " mở");
                Assert.AreEqual((double)w[3], res.converted, hero + " đổi thành bản sao");
            }
            foreach (var x in J.Arr(G, "shardEnd"))
            {
                var w = J.Arr(x);
                var p = s.Hero((string)w[0]);
                Assert.AreEqual((bool)w[1], p.owned, (string)w[0]);
                Assert.AreEqual((double)w[2], p.shards, (string)w[0]);
                Assert.AreEqual((double)w[3], p.skill.copies);
                Assert.AreEqual((double)w[4], p.ult.copies);
                Assert.AreEqual((double)w[5], p.passive.copies);
            }
        }

        [Test]
        public void NangThe_TieuBanSao_CapToiDaGiuBanSao()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            Progress.UnlockHero(s, "vo_su");
            var c = s.Hero("vo_su").skill;
            Assert.IsFalse(Progress.CanUpCard(s, cfg, "vo_su", CardSlot.Skill));
            c.copies = 2;
            Assert.IsTrue(Progress.UpCard(s, cfg, "vo_su", CardSlot.Skill));
            Assert.AreEqual(2, c.lv);
            Assert.AreEqual(0, c.copies);
            // Thiết Quyền cấp 2: mô tả theo số thật
            Assert.AreEqual("Gây 138% Công sát thương. +12 nộ.", CardText.Text(d.Card(d.Hero("vo_su").skill), 2, cfg.cardLvStep));
            c.copies = 100;
            while (Progress.UpCard(s, cfg, "vo_su", CardSlot.Skill)) { }
            Assert.AreEqual(5, c.lv);
            Assert.AreEqual(100 - 4 - 8 - 15, c.copies, "cấp tối đa: bản sao còn lại được giữ");
            Assert.AreEqual(int.MaxValue, Progress.CardReq(cfg, 5));
        }

        [Test]
        public void TienHoa_CanTongCapTheVaCapNguoiChoi()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            var p = s.Hero("giot_suong");
            // sao 2: tổng cấp thẻ 5, cấp người chơi 2
            p.skill.lv = 3;
            s.level = 1;
            Assert.IsFalse(Progress.CanEvolve(s, cfg, "giot_suong"), "thiếu cấp người chơi");
            s.level = 2;
            Assert.IsTrue(Progress.Evolve(s, cfg, "giot_suong"));
            Assert.AreEqual(2, p.star);
            // sao 3: tổng 8, cấp 5 — đủ thẻ mà thiếu cấp
            p.ult.lv = 4;
            s.level = 4;
            var need = Progress.StarNeed(cfg, 3);
            Assert.AreEqual((8, 5), need);
            Assert.AreEqual(8, Progress.CardSum(s, "giot_suong"));
            Assert.IsFalse(Progress.CanEvolve(s, cfg, "giot_suong"));
            Assert.AreEqual(0, Progress.HeroAlerts(s, d));
            s.level = 5;
            Assert.AreEqual(1, Progress.HeroAlerts(s, d), "một việc chờ: tiến hóa");
        }

        [Test]
        public void LenCap_GiuExpThua_VaQuaHaiCap()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            int need = Progress.ExpToNext(1, d.Cfg) + Progress.ExpToNext(2, d.Cfg);
            int ups = Progress.AddExp(s, need + 7, d.Cfg);
            Assert.AreEqual(2, ups);
            Assert.AreEqual(3, s.level);
            Assert.AreEqual(7, s.exp);
        }
    }
}
