// Bản lưu: ghi rồi đọc lại, file tạm sót, bản cũ v1 và file hỏng (giữ .bak, báo người chơi).
using System.IO;
using NUnit.Framework;
using PokiClash.Core;
using PokiClash.Game;

namespace PokiClash.Tests
{
    public class SaveTests
    {
        string dir;

        [SetUp]
        public void SetUp()
        {
            dir = Path.Combine(Path.GetTempPath(), "pokiclash_save_test_" + System.Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(dir);
        }

        [TearDown]
        public void TearDown()
        {
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
        }

        [Test]
        public void NguoiChoiMoi_DungTrangThaiDau()
        {
            var svc = new SaveService(TestData.Load(), dir);
            Assert.IsTrue(svc.Load());
            Assert.IsTrue(svc.IsNew);
            var s = svc.Data;
            Assert.AreEqual(1, s.level);
            Assert.AreEqual(10, s.balls);
            // chưa chọn tướng khởi đầu: chưa có tướng nào, sảnh mở hộp chọn (15_TuongKhoiDau.md)
            Assert.IsNull(s.starter);
            Assert.IsEmpty(s.team);
            Assert.IsFalse(s.Hero("giot_suong").owned);
            Assert.IsFalse(s.Hero("ca_sa").owned);
            Assert.AreEqual(0, s.zones[(int)Elem.Thuy]);
            Assert.IsTrue(File.Exists(Path.Combine(dir, $"save_v{TestData.Load().Cfg.saveVersion}.json")));
        }

        [Test]
        public void GhiRoiDocLai_GiuNguyen()
        {
            var d = TestData.Load();
            var svc = new SaveService(d, dir);
            svc.Load();
            svc.Data.ChooseStarter("giot_suong");
            svc.Data.level = 7;
            svc.Data.balls = 123;
            svc.Data.zones[(int)Elem.Hoa] = 3;
            svc.Data.clears[12] = 2;
            svc.Data.Hero("vo_su").owned = true;
            svc.Data.Hero("vo_su").skill.lv = 3;
            svc.Data.team.Add("vo_su");
            svc.Data.settings.speed = 2;
            svc.Data.settings.boil = false;
            svc.Data.extra["homestead"] = new System.Collections.Generic.Dictionary<string, object> { ["thuy"] = 1.0 };
            svc.Data.chests.Add(new PendingChest { kind = "chest_gold", x = 3 });
            svc.Data.chests.Add(new PendingChest { kind = "chest_wood", x = 1 });
            svc.Save();

            var again = new SaveService(d, dir);
            Assert.IsTrue(again.Load());
            Assert.IsFalse(again.IsNew);
            var s = again.Data;
            Assert.AreEqual(7, s.level);
            Assert.AreEqual(123, s.balls);
            Assert.AreEqual(3, s.zones[(int)Elem.Hoa]);
            Assert.AreEqual(2, s.clears[12]);
            Assert.AreEqual(3, s.Hero("vo_su").skill.lv);
            Assert.AreEqual(new[] { "giot_suong", "vo_su" }, s.team.ToArray());
            Assert.AreEqual(2, s.settings.speed);
            Assert.IsFalse(s.settings.boil);
            Assert.IsTrue(s.extra.ContainsKey("homestead"), "khoá lạ được giữ nguyên");
            Assert.AreEqual(2, s.chests.Count, "rương máy bi chờ mở");
            Assert.AreEqual("chest_gold", s.chests[0].kind);
            Assert.AreEqual(3, s.chests[0].x);
            Assert.IsFalse(s.extra.ContainsKey("chests"));
            Assert.AreEqual("giot_suong", s.starter, "tướng khởi đầu đã chọn");
        }

        [Test]
        public void FileTamSot_DuocDungLai()
        {
            var d = TestData.Load();
            var svc = new SaveService(d, dir);
            svc.Load();
            svc.Data.balls = 77;
            svc.Save();
            // giả lập tắt ngang: bản chính đã xoá, bản tạm chưa kịp đổi tên
            File.Move(svc.FilePath, svc.FilePath + ".tmp");

            var again = new SaveService(d, dir);
            Assert.IsTrue(again.Load());
            Assert.AreEqual(77, again.Data.balls);
            Assert.IsTrue(File.Exists(again.FilePath));
        }

        [Test]
        public void BanCuV1_GiuBak_VaBao()
        {
            File.WriteAllText(Path.Combine(dir, "save_v1.json"), "{\"v\":1,\"level\":9,\"chapter\":3}");
            var svc = new SaveService(TestData.Load(), dir);
            Assert.IsFalse(svc.Load());
            Assert.AreEqual("Dữ liệu bản thử cũ không dùng được, sẽ bắt đầu lại.", svc.Notice);
            Assert.IsTrue(File.Exists(Path.Combine(dir, "save_v1.bak")));
            svc.CreateNew();
            Assert.AreEqual(1, svc.Data.level);
        }

        [Test]
        public void BanLuuV2_DiChuyenLenBanMoi()
        {
            // file save_v2.json của bản trước: đọc, chạy bước v2 -> v3 (lượt quảng cáo dồn về ads), ghi file mới, giữ file cũ thành .bak
            File.WriteAllText(Path.Combine(dir, "save_v2.json"),
                "{\"v\":2,\"level\":5,\"balls\":77,\"afk\":{\"lastTick\":0,\"adDay\":20500,\"adOpen\":3,\"adBoost\":0}}");
            var d = TestData.Load();
            var svc = new SaveService(d, dir);
            Assert.IsTrue(svc.Load());
            Assert.IsFalse(svc.IsNew);
            Assert.AreEqual(5, svc.Data.level);
            Assert.AreEqual(77, svc.Data.balls);
            Assert.AreEqual(3, svc.Data.ads.used[AdGate.AfkChestOpen]);
            Assert.IsTrue(File.Exists(Path.Combine(dir, $"save_v{d.Cfg.saveVersion}.json")));
            Assert.IsTrue(File.Exists(Path.Combine(dir, "save_v2.bak")));
        }

        [Test]
        public void FileHong_GiuBak_VaBao()
        {
            int v = TestData.Load().Cfg.saveVersion;
            File.WriteAllText(Path.Combine(dir, $"save_v{v}.json"), "{\"v\":" + v + ",\"level\":");
            var svc = new SaveService(TestData.Load(), dir);
            Assert.IsFalse(svc.Load());
            Assert.IsNotNull(svc.Notice);
            Assert.IsTrue(File.Exists(Path.Combine(dir, $"save_v{v}.bak")));
        }

        [Test]
        public void Sfx_SinhDuMauChoMoiTieng()
        {
            foreach (var name in SfxSynth.Names)
            {
                var buf = SfxSynth.Render(name);
                Assert.Greater(buf.Length, 100, name);
                float peak = 0;
                foreach (var x in buf) peak = System.Math.Max(peak, System.Math.Abs(x));
                Assert.Greater(peak, 0.005f, name + " không có tiếng");
                Assert.LessOrEqual(peak, 1f, name);
            }
        }
    }
}
