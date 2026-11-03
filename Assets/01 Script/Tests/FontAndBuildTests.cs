// Phông TMP đủ mọi dấu tiếng Việt; Build Settings đúng thứ tự; không có hình aola trong Assets; dữ liệu asset khớp JSON.
using System.IO;
using System.Linq;
using NUnit.Framework;
using PokiClash.EditorTools;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEditor;

namespace PokiClash.Tests
{
    public class FontAndBuildTests
    {
        [Test]
        public void PhongTMP_DuDauTiengViet()
        {
            var ui = AssetDatabase.LoadAssetAtPath<UiAssets>("Assets/02 Data/UiAssets.asset");
            Assert.IsNotNull(ui, "chưa chạy PokiClash/Cài đặt/2. Dựng tất cả");
            foreach (var f in new[] { ui.title, ui.bold, ui.body })
            {
                Assert.IsNotNull(f);
                // atlas lệch cỡ thì thêm chữ sẽ ghi tràn bộ nhớ và làm Unity crash: dừng ở đây (FontAtlasGuard)
                var bad = FontAtlasGuard.Problems(f);
                Assert.IsEmpty(bad, string.Join("\n", bad));
                bool ok = f.HasCharacters(ProjectSetup.VietSample, out var missing, false, true);
                Assert.IsTrue(ok, $"{f.name} thiếu: {(missing == null ? "" : new string(missing.Select(c => (char)c).ToArray()))}");
            }
        }

        [Test]
        public void BuildSettings_BootDauTien_KhongCoBanThu()
        {
            var scenes = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => Path.GetFileNameWithoutExtension(s.path)).ToList();
            Assert.AreEqual(SceneIds.Boot, scenes[0]);
            foreach (var n in SceneIds.Features) Assert.Contains(n, scenes);
            Assert.IsFalse(scenes.Contains("BanThu"));
        }

        [Test]
        public void KhongCoHinhAolaTrongAssets()
        {
            var errors = PreBuildCheck.Scan(out _);
            Assert.IsEmpty(errors, string.Join("\n", errors));
        }

        [Test]
        public void CongCuDev_BocKin_KhongVaoBanPhatHanh()
        {
            Assert.IsTrue(Directory.GetFiles(PreBuildCheck.DevDir, "*.cs").Length >= 2, "có công cụ dev trong App/Dev");
            var errors = PreBuildCheck.DevGuards();
            Assert.IsEmpty(errors, string.Join("\n", errors));
        }

        [Test]
        public void AssetDuLieu_KhopJson()
        {
            var heroes = AssetDatabase.LoadAssetAtPath<HeroDb>("Assets/02 Data/HeroDb.asset");
            var cards = AssetDatabase.LoadAssetAtPath<CardDb>("Assets/02 Data/CardDb.asset");
            var zones = AssetDatabase.LoadAssetAtPath<ZoneDb>("Assets/02 Data/ZoneDb.asset");
            var bal = AssetDatabase.LoadAssetAtPath<BalanceConfigAsset>("Assets/02 Data/BalanceConfig.asset");
            Assert.IsNotNull(heroes);
            var d = GameDb.Build(heroes, cards, zones, bal);
            Assert.IsEmpty(d.Validate());
            var json = TestData.Load();
            for (int i = 0; i < json.Pool.Count; i++)
                Assert.AreEqual(json.Pool[i].effectsJson, d.Pool[i].effectsJson, json.Pool[i].id);
            Assert.AreEqual(json.Zones[2].nodes[5].x, d.Zones[2].nodes[5].x);
            Assert.AreEqual(json.Cfg.cardLvStep, d.Cfg.cardLvStep);
            // cấu hình side meta phải qua được lưu ScriptableObject (không dùng kiểu Unity không lưu: mảng lồng, nullable...)
            var a = d.Cfg;
            var j = json.Cfg;
            Assert.AreEqual(j.chests.Count, a.chests.Count, "bảng rương máy bi");
            Assert.AreEqual(j.Chest("chest_gold").rolls.Count, a.Chest("chest_gold").rolls.Count);
            Assert.AreEqual(j.rates.Count, a.rates.Count, "tỉ lệ đo của máy bi");
            Assert.AreEqual(j.afk.chest.rolls.Count, a.afk.chest.rolls.Count, "rương AFK");
            Assert.AreEqual(j.simTeams.Count, a.simTeams.Count, "đội mẫu theo đảo");
            CollectionAssert.AreEqual(j.badges.counts, a.badges.counts, "huy hiệu");
            CollectionAssert.AreEqual(j.potential.values, a.potential.values, "bảng dòng tiềm năng");
            CollectionAssert.AreEqual(j.potential.caps, a.potential.caps, "trần tiềm năng");
            CollectionAssert.AreEqual(j.cave.weekday, a.cave.weekday, "hệ boss Hang theo thứ");
            Assert.AreEqual(j.cave.tiers.Count, a.cave.tiers.Count, "tầng Hang");
            Assert.AreEqual(0.16, a.potential.Val((int)PokiClash.Core.PotKind.Atk, 4), 1e-12);
            Assert.AreEqual(PokiClash.Core.Elem.Kim, a.cave.Weekday(1));
            Assert.AreEqual(j.farm.spots.Count, a.farm.spots.Count, "chỗ làm trang trại");
            CollectionAssert.AreEqual(j.farm.spotLevels, a.farm.spotLevels, "cấp mở chỗ trang trại");
            Assert.AreEqual(j.farm.@base, a.farm.@base, "năng suất gốc trang trại");
        }
    }
}
