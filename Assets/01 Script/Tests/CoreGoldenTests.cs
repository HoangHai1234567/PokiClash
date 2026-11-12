// Đối chiếu phần lõi với bản web: số ngẫu nhiên, mô tả thẻ, số lượng dữ liệu.
// Golden xuất bằng `npx tsx scripts/export_golden.ts` (thư mục Web), dữ liệu bằng `npx tsx scripts/export_data.ts`.
// Từ 2026-11-03 làm ở Unity: thẻ của 5 tướng khởi đầu trong cardtext.json sửa bên Unity (GD_Claude/15_TuongKhoiDau.md);
// 2026-11-04 thêm mô tả 12 thẻ chung mới.
using System.Collections.Generic;
using System.IO;
using NUnit.Framework;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Tests
{
    public static class TestData
    {
        public static string DataDir => Path.Combine(Application.dataPath, "02 Data");
        public static string Read(string rel) => File.ReadAllText(Path.Combine(DataDir, rel));

        // tướng khởi đầu hệ Thủy trước lô tướng mới 2026-11-11 (Giọt Sương, tên Thủy Long; giờ là Tí Tách). Các golden xuất với bản lưu
        // mặc định cũ (rương, trang trại, tiềm năng, tiến độ đền) không phụ thuộc tướng khởi đầu nào: test dựng bản lưu "người chơi
        // đã chọn Giọt Sương" bằng SaveData.New(d, 0, OldStarter) để giữ nguyên golden đó
        public const string OldStarter = "giot_suong";

        static GameData cached;

        public static GameData Load() => cached ??= GameData.FromJson(
            Read("Json/heroes.json"), Read("Json/cards.json"), Read("Json/zones.json"), Read("Json/stages.json"), Read("Json/balance.json"));

        // bản sao của ải với mọi địch ở cấp lv: các trận so với bản web giữ đúng cấp địch lúc xuất golden (thang cấp đã đổi sau đó,
        // 5 đảo song song từ 2026-11-05), để vẫn so cơ chế trận mà không phụ thuộc cấp của dữ liệu ải hiện tại
        public static StageDef AtLevel(StageDef st, int lv)
        {
            var c = new StageDef { id = st.id, zone = st.zone, idx = st.idx, name = st.name, kind = st.kind, tag = st.tag, chapter = st.chapter, drops = st.drops };
            foreach (var e in st.enemies) c.enemies.Add(new StageEnemy { hero = e.hero, level = lv, boss = e.boss, evo = e.evo, buff = e.buff });
            return c;
        }
    }

    public class CoreGoldenTests
    {
        [Test]
        public void Rng_KhopBanWeb()
        {
            var root = J.Obj(MiniJson.Parse(TestData.Read("Golden/rng.json")));
            var seeds = J.Arr(root, "seeds");
            Assert.AreEqual(3, seeds.Count);
            foreach (var x in seeds)
            {
                var o = J.Obj(x);
                uint seed = (uint)J.Num(o, "seed");
                var r = new Rng(seed);
                var next = J.Arr(o, "next");
                Assert.AreEqual(1000, next.Count);
                for (int i = 0; i < next.Count; i++)
                    Assert.AreEqual((double)next[i], r.Next(), 0.0, $"hạt giống {seed}, số thứ {i}");
                var r2 = new Rng(seed);
                var ints = J.Arr(o, "ints");
                for (int i = 0; i < ints.Count; i++)
                    Assert.AreEqual((int)(double)ints[i], r2.Int(0, 9), $"hạt giống {seed}, int thứ {i}");
            }
        }

        [Test]
        public void CardText_KhopBanWeb()
        {
            var d = TestData.Load();
            var root = J.Obj(MiniJson.Parse(TestData.Read("Golden/cardtext.json")));
            var cards = J.Arr(root, "cards");
            Assert.AreEqual(d.Pool.Count + d.Innate.Count + d.MinionCards.Count + d.Traits.Count, cards.Count); // kể cả bị động boss
            var fails = new List<string>();
            foreach (var x in cards)
            {
                var o = J.Obj(x);
                var c = d.Card(J.Str(o, "id"));
                Assert.IsNotNull(c, J.Str(o, "id"));
                void Check(string what, string want, string got)
                {
                    if (want != got) fails.Add($"{c.id} {what}:\n  web:   {want}\n  unity: {got}");
                }
                Check("lv1", J.Str(o, "lv1"), CardText.Text(c, 1, d.Cfg.cardLvStep));
                Check("lv5", J.Str(o, "lv5"), CardText.Text(c, 5, d.Cfg.cardLvStep));
                Check("cost", J.Str(o, "cost"), CardText.CostText(c));
            }
            Assert.IsEmpty(fails, string.Join("\n", fails));
        }

        [Test]
        public void DuLieu_DuSoLuong_VaToaDoTrong01()
        {
            var d = TestData.Load();
            var err = d.Validate();
            Assert.IsEmpty(err, string.Join("\n", err));
            Assert.AreEqual(88, d.Heroes.Count);
            Assert.AreEqual(35, d.Pool.Count); // 23 của bản web, thêm 12 ở Unity (2026-11-04)
            Assert.AreEqual(265, d.Innate.Count); // 88 tướng × 3 + thẻ Tiến Hóa của boss
            Assert.AreEqual(30, d.Minions.Count);
            Assert.AreEqual(90, d.MinionCards.Count);
            Assert.AreEqual(5, d.Zones.Count);
            Assert.AreEqual(350, d.Stages.Count); // 5 đảo, mỗi đảo 70 ải
            Assert.AreEqual(Elem.Thuy, d.Zones[0].id, "đảo đầu tiên là Thủy");
            Assert.AreEqual(5, d.Cfg.picks);
            Assert.AreEqual(9, d.Cfg.saveVersion); // v5: chọn 1 trong 5 tướng khởi đầu (2026-11-03); v6: tướng cũ đảo Thủy chuyển sang 10 tướng mới (2026-11-11)
        }

        [Test]
        public void JsRound_GiongMathRound()
        {
            Assert.AreEqual(3, Js.Round(2.5));
            Assert.AreEqual(-2, Js.Round(-2.5));
            Assert.AreEqual(0, Js.Round(0.49999999999999994));
            Assert.AreEqual(1, Js.Round(0.5));
            Assert.AreEqual("1,5", Js.Num(1.5).Replace('.', ','));
            Assert.AreEqual("24", Js.Num(24));
        }

        [Test]
        public void NguHanh_Khac()
        {
            Assert.AreEqual(1.5, Elements.Mult(Elem.Thuy, Elem.Hoa));
            Assert.AreEqual(0.75, Elements.Mult(Elem.Hoa, Elem.Thuy));
            Assert.AreEqual(1.0, Elements.Mult(Elem.Kim, Elem.Thuy));
        }

        [Test]
        public void MiniJson_GhiRoiDocLai()
        {
            var o = new Dictionary<string, object> { ["a"] = 1, ["b"] = "Đảo \"Thủy\"\n", ["c"] = new List<object> { 1.25, true, null } };
            var back = J.Obj(MiniJson.Parse(MiniJson.Write(o)));
            Assert.AreEqual(1.0, back["a"]);
            Assert.AreEqual("Đảo \"Thủy\"\n", back["b"]);
            Assert.AreEqual(1.25, J.Arr(back, "c")[0]);
        }
    }
}
