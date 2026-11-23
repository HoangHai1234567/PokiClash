// Đa ngôn ngữ (2026-11-21): luật tra của Loc, bảng tiếng Anh đọc được và khớp chỗ điền, đủ bản dịch cho mọi chuỗi tiếng Việt
// người chơi thấy (Loc.T / Loc.F trong code, chữ TMP trong prefab, tên trong dữ liệu), mô tả thẻ tiếng Anh không sót chữ Việt.
// Thiếu bản dịch: thêm vào Assets/Resources/Loc/en/*.json (khoá là chính chuỗi tiếng Việt).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using NUnit.Framework;
using PokiClash.Core;
using PokiClash.Game;
using TMPro;
using UnityEditor;
using UnityEngine;

namespace PokiClash.Tests
{
    public class LocTests
    {
        static Dictionary<string, string> en;
        static Dictionary<string, string> En => en ??= LocService.Load(Loc.En);

        [TearDown]
        public void Back() => Loc.UseVi();

        [Test]
        public void Loc_TraChuoi()
        {
            Loc.Use(Loc.En, new Dictionary<string, string> { ["Cấp"] = "Level", ["Ruộng Bậc Thang"] = "Terraced Fields", ["Ải {0} · {1}"] = "{1} · Stage {0}" });
            Assert.AreEqual("Level", Loc.T("Cấp"));
            Assert.AreEqual(" Level ", Loc.T(" Cấp "), "giữ khoảng trắng hai đầu");
            Assert.AreEqual("Terraced Fields 3", Loc.T("Ruộng Bậc Thang 3"), "số đuôi");
            Assert.AreEqual("Đảo lạ", Loc.T("Đảo lạ"), "thiếu thì giữ tiếng Việt");
            Assert.AreEqual("Fire · Stage 2", Loc.F("Ải {0} · {1}", 2, "Fire"), "đổi thứ tự chỗ điền");
            Loc.UseVi();
            Assert.AreEqual("Cấp", Loc.T("Cấp"));
            Assert.IsTrue(Loc.LooksVi("Đảo"));
            Assert.IsFalse(Loc.LooksVi("Island 3"));
        }

        static readonly Regex Ph = new Regex(@"(?<!\{)\{(\d+)(?:,[^}:]*)?(?::[^}]*)?\}(?!\})");

        [Test]
        public void BangTiengAnh_DocDuoc_KhopChoDien()
        {
            Assert.Greater(En.Count, 500, "bảng tiếng Anh trống hoặc không đọc được");
            var bad = new List<string>();
            foreach (var kv in En)
            {
                var a = Ph.Matches(kv.Key).Cast<Match>().Select(m => m.Groups[1].Value).OrderBy(x => x);
                var b = Ph.Matches(kv.Value).Cast<Match>().Select(m => m.Groups[1].Value).OrderBy(x => x);
                if (!a.SequenceEqual(b)) bad.Add($"{kv.Key} => {kv.Value}");
                if (Loc.LooksVi(kv.Value)) bad.Add($"còn chữ Việt: {kv.Key} => {kv.Value}");
            }
            Assert.IsEmpty(bad, string.Join("\n", bad.Take(30)));
        }

        // ---------- đủ bản dịch ----------

        static void Need(string vi, string where, List<string> miss)
        {
            if (string.IsNullOrEmpty(vi) || !Loc.LooksVi(vi)) return;
            if (!Loc.Find(vi, out _)) miss.Add($"{where}: {vi}");
        }

        static string Unescape(string s)
        {
            var sb = new StringBuilder();
            for (int i = 0; i < s.Length; i++)
            {
                char c = s[i];
                if (c != '\\' || i + 1 >= s.Length)
                {
                    sb.Append(c);
                    continue;
                }
                char n = s[++i];
                switch (n)
                {
                    case 'n': sb.Append('\n'); break;
                    case 't': sb.Append('\t'); break;
                    case 'r': sb.Append('\r'); break;
                    case 'u':
                        sb.Append((char)System.Convert.ToInt32(s.Substring(i + 1, 4), 16));
                        i += 4;
                        break;
                    default: sb.Append(n); break;
                }
            }
            return sb.ToString();
        }

        [Test]
        public void DuBanDich_ChuoiTrongCode()
        {
            Loc.Use(Loc.En, En);
            var miss = new List<string>();
            var call = new Regex(@"Loc\.(?:T|F)\(\s*""((?:[^""\\]|\\.)*)""");
            string root = Path.Combine(Application.dataPath, "01 Script");
            foreach (var f in Directory.GetFiles(root, "*.cs", SearchOption.AllDirectories))
            {
                var rel = f.Substring(root.Length + 1).Replace('\\', '/');
                if (rel.StartsWith("Editor/") || rel.StartsWith("Tests/") || rel.StartsWith("BanThu/")) continue;
                var src = File.ReadAllText(f);
                foreach (Match m in call.Matches(src))
                    Need(Unescape(m.Groups[1].Value), rel, miss);
            }
            // chữ dịch ở chỗ dùng (mảng tĩnh, hằng): đi qua hàm trả tên
            foreach (Elem e in System.Enum.GetValues(typeof(Elem))) Need(Elements.NameVi(e), "Elements", miss);
            foreach (Rarity r in System.Enum.GetValues(typeof(Rarity))) Need(Elements.RarityNameVi(r), "Elements", miss);
            foreach (CardKind k in System.Enum.GetValues(typeof(CardKind))) Need(Elements.KindNameVi(k), "Elements", miss);
            Assert.AreEqual("Metal", Elements.Name(Elem.Kim), "tên hệ Kim (không dấu) phải dịch");
            Assert.IsEmpty(miss, $"{miss.Count} chuỗi chưa dịch:\n" + string.Join("\n", miss.Take(40)));
        }

        [Test]
        public void DuBanDich_ChuTrongPrefab()
        {
            Loc.Use(Loc.En, En);
            var miss = new List<string>();
            foreach (var guid in AssetDatabase.FindAssets("t:Prefab", new[] { "Assets/04 Prefabs" }))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var go = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                if (!go) continue;
                foreach (var t in go.GetComponentsInChildren<TMP_Text>(true))
                    Need(t.text, path.Substring("Assets/04 Prefabs/".Length) + "/" + t.name, miss);
            }
            Assert.IsEmpty(miss, $"{miss.Count} chữ prefab chưa dịch:\n" + string.Join("\n", miss.Take(40)));
        }

        [Test]
        public void DuBanDich_TenTrongDuLieu()
        {
            Loc.Use(Loc.En, En);
            var d = TestData.Load();
            var miss = new List<string>();
            foreach (var h in d.Heroes.Concat(d.Minions))
            {
                Need(h.name, "tướng " + h.id, miss);
                Need(h.title, "danh hiệu " + h.id, miss);
                Need(h.line, "dòng " + h.id, miss);
                foreach (var f in h.forms) Need(f.name, "dạng " + h.id, miss);
            }
            foreach (var c in d.Pool.Concat(d.Innate).Concat(d.MinionCards).Concat(d.Traits))
            {
                Need(c.name, "thẻ " + c.id, miss);
                Need(c.flavor, "lời thẻ " + c.id, miss);
            }
            foreach (var z in d.Zones)
            {
                Need(z.name, "đảo " + z.id, miss);
                Need(z.sub, "đảo " + z.id, miss);
            }
            foreach (var s in d.Stages) Need(s.name, "ải " + s.id, miss);
            var cfg = d.Cfg;
            foreach (var t in cfg.cave.tiers) Need(t.name, "tầng Hang", miss);
            foreach (var t in cfg.badges.tiers) Need(t, "bậc huy hiệu", miss);
            foreach (var p in cfg.ads.products)
            {
                Need(p.name, "gói " + p.id, miss);
                Need(p.desc, "gói " + p.id, miss);
            }
            // cửa hàng (GD_Claude/26): gói, trứng, mẫu ưu đãi, thẻ, chuỗi
            foreach (var p in cfg.shop.packs)
            {
                Need(p.name, "gói cửa hàng " + p.id, miss);
                if (!string.IsNullOrEmpty(p.desc)) Need(p.desc, "gói cửa hàng " + p.id, miss);
            }
            foreach (var e in cfg.shop.eggs) Need(e.name, "trứng " + e.tier, miss);
            foreach (var o in cfg.shop.offers) Need(o.name, "ưu đãi " + o.id, miss);
            foreach (var c in cfg.shop.cards) Need(c.name, "thẻ " + c.id, miss);
            foreach (var c in cfg.shop.chains) Need(c.name, "chuỗi " + c.id, miss);
            Assert.IsEmpty(miss, $"{miss.Count} tên chưa dịch:\n" + string.Join("\n", miss.Take(40)));
        }

        [Test]
        public void MoTaThe_TiengAnh_KhongSotChuViet()
        {
            var d = TestData.Load();
            Loc.Use(Loc.En, En);
            var bad = new List<string>();
            foreach (var c in d.Pool.Concat(d.Innate).Concat(d.MinionCards).Concat(d.Traits))
            {
                foreach (int lv in new[] { 1, 5 })
                {
                    var t = CardText.Text(c, lv, d.Cfg.cardLvStep);
                    if (Loc.LooksVi(t) || (c.Effects.Count > 0 && t.Trim('.').Length == 0)) bad.Add($"{c.id} cấp {lv}: {t}");
                }
                var note = CardText.Note(c);
                if (Loc.LooksVi(note)) bad.Add($"{c.id} luật: {note}");
            }
            Assert.IsEmpty(bad, string.Join("\n", bad.Take(30)));
        }
    }
}
