// Gói tải sau (GD_Claude/27_TaiNoiDungSau.md): soát sau khi gán gói (menu PokiClash/Tải sau/Gán gói). Bỏ qua khi cơ chế đang tắt (Gỡ gói).
//  - tướng ngoài dòng khởi đầu: prefab không trỏ thẳng hình, mỗi dạng có AolaAnim trong Heroes/Forms và nằm đúng nhóm noi_dung_<hệ>;
//  - dòng khởi đầu: trỏ thẳng, hình ở Resources (bản cài);
//  - chân dung mọi dạng vẫn ở Resources/<dạng>/<dạng>_portrait.png;
//  - không gì trong bản cài (scene trong build, mọi asset trong Resources) phụ thuộc asset của gói: phụ thuộc thì asset bị kéo vào bản
//    cài, gói vô ích;
//  - mục ArtLibrary thuộc gói: không trỏ Sprite, có địa chỉ đúng tên trong nhóm của hệ.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using NUnit.Framework;
using PokiClash.EditorTools;
using PokiClash.Game;
using UnityEditor;
using UnityEditor.AddressableAssets;
using UnityEditor.AddressableAssets.Settings;
using UnityEngine;

namespace PokiClash.Tests
{
    public class ContentPackTests
    {
        static AddressableAssetSettings Settings
        {
            get
            {
                if (!ContentPackSetup.Enabled) Assert.Ignore("Gói tải sau đang tắt (Gỡ gói)");
                var s = AddressableAssetSettingsDefaultObject.Settings;
                Assert.IsNotNull(s, "chưa có Addressables (chạy PokiClash/Tải sau/Gán gói)");
                return s;
            }
        }

        static string Pack(AddressableAssetSettings s, string path)
        {
            var e = s.FindAssetEntry(AssetDatabase.AssetPathToGUID(path));
            if (e == null) return null;
            string g = e.parentGroup ? e.parentGroup.Name : "";
            return g.StartsWith("noi_dung_") ? g.Substring("noi_dung_".Length) : null;
        }

        [Test]
        public void HeroFormsInRightPack()
        {
            var s = Settings;
            int packed = 0, starters = 0;
            foreach (var h in ContentPackSetup.Heroes())
            {
                string pp = $"Assets/04 Prefabs/Heroes/{h.id}.prefab";
                var actor = AssetDatabase.LoadAssetAtPath<AolaActor>(pp);
                if (!actor) continue;
                if (h.starter)
                {
                    starters++;
                    Assert.IsTrue(string.IsNullOrEmpty(actor.Pack), $"{h.id}: tướng khởi đầu phải ở bản cài");
                    for (int i = 0; i < h.forms.Count; i++)
                    {
                        var a = actor.Form(i);
                        Assert.IsTrue(a, $"{h.id} dạng {h.forms[i]}: chưa trỏ AolaAnim");
                        Assert.IsTrue(AssetDatabase.GetAssetPath(a).Contains("/Resources/"), $"{h.id} dạng {h.forms[i]}: hình không ở Resources");
                    }
                    continue;
                }
                packed++;
                Assert.AreEqual(h.elem, actor.Pack, $"{h.id}: sai gói");
                Assert.AreEqual(h.forms.Count, actor.FormCount, $"{h.id}: số dạng");
                var so = new SerializedObject(actor);
                var forms = so.FindProperty("forms");
                for (int i = 0; i < forms.arraySize; i++)
                    Assert.IsNull(forms.GetArrayElementAtIndex(i).objectReferenceValue, $"{h.id}: còn trỏ thẳng dạng {i} (kéo hình vào bản cài)");
                for (int i = 0; i < h.forms.Count; i++)
                {
                    string form = h.forms[i];
                    Assert.AreEqual(form, actor.FormKey(i), $"{h.id}: tên dạng {i}");
                    string path = $"{ContentPackSetup.FormsDir}/{form}/{form}.asset";
                    if (!File.Exists(path)) continue; // dạng chưa nhập hình
                    Assert.AreEqual(h.elem, Pack(s, path), $"{form}: AolaAnim không ở nhóm noi_dung_{h.elem}");
                    Assert.AreEqual(form, s.FindAssetEntry(AssetDatabase.AssetPathToGUID(path)).address, $"{form}: địa chỉ");
                }
            }
            TestContext.WriteLine($"{packed} tướng trong gói, {starters} tướng khởi đầu ở bản cài");
            Assert.Greater(packed, 0);
        }

        [Test]
        public void PortraitsStayInResources()
        {
            foreach (var h in ContentPackSetup.Heroes())
                foreach (var form in h.forms)
                {
                    if (!File.Exists($"{ContentPackSetup.FormsDir}/{form}/{form}.asset") && !File.Exists($"Assets/03 Art/Heroes/Resources/{form}/{form}.asset")) continue;
                    Assert.IsTrue(File.Exists($"Assets/03 Art/Heroes/Resources/{form}/{form}_portrait.png"), $"{form}: chân dung không ở Resources");
                }
        }

        [Test]
        public void BaseDoesNotDependOnPacks()
        {
            var s = Settings;
            var pack = new Dictionary<string, string>();
            foreach (var g in s.groups)
            {
                if (!g || !g.Name.StartsWith("noi_dung_")) continue;
                foreach (var e in g.entries) pack[e.AssetPath] = g.Name;
            }
            Assert.Greater(pack.Count, 0, "các gói đang rỗng");
            var roots = EditorBuildSettings.scenes.Where(x => x.enabled).Select(x => x.path).ToList();
            roots.AddRange(AssetDatabase.GetAllAssetPaths().Where(p => p.StartsWith("Assets/") && p.Contains("/Resources/") && !p.Contains("/Editor/")
                                                                    && !AssetDatabase.IsValidFolder(p)));
            var bad = new List<string>();
            foreach (var r in roots)
                foreach (var d in AssetDatabase.GetDependencies(r, true))
                    if (pack.TryGetValue(d, out var g)) bad.Add($"{r} → {d} ({g})");
            Assert.IsEmpty(bad.Distinct().Take(30).ToList(), "bản cài phụ thuộc asset của gói");
        }

        [Test]
        public void ArtPackEntriesAddressable()
        {
            var s = Settings;
            var lib = AssetDatabase.LoadAssetAtPath<ArtLibrary>("Assets/02 Data/ArtLibrary.asset");
            Assert.IsNotNull(lib);
            int n = 0;
            foreach (var e in lib.art.Where(e => !string.IsNullOrEmpty(e.pack)))
            {
                n++;
                Assert.IsNull(e.sprite, $"{e.name}: mục của gói còn trỏ thẳng Sprite");
                var entry = s.groups.Where(g => g && g.Name == ContentPacks.PackName(e.pack)).SelectMany(g => g.entries).FirstOrDefault(x => x.address == e.name);
                Assert.IsNotNull(entry, $"{e.name}: không có trong nhóm {ContentPacks.PackName(e.pack)}");
            }
            TestContext.WriteLine($"{n} ảnh trong gói");
            Assert.Greater(n, 0);
        }
    }
}
