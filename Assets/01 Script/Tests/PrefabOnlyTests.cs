// Chặn sinh đồ vật lúc chạy (change convert-to-prefabs): quét mã runtime (mọi thư mục trừ Editor, Tests, BanThu), không được dựng
// GameObject, component, sprite, texture, material, âm thanh hay gọi hàm dựng giao diện. Ngoại lệ ghi kèm lý do.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEngine;

namespace PokiClash.Tests
{
    public class PrefabOnlyTests
    {
        static readonly (string name, Regex re)[] Rules =
        {
            ("new GameObject", new Regex(@"\bnew\s+GameObject\s*\(")),
            ("AddComponent", new Regex(@"\bAddComponent\s*[<(]")),
            ("Sprite.Create", new Regex(@"\bSprite\.Create\s*\(")),
            ("new Texture2D", new Regex(@"\bnew\s+Texture2D\s*\(")),
            ("new Material", new Regex(@"\bnew\s+Material\s*\(")),
            ("AudioClip.Create", new Regex(@"\bAudioClip\.Create\s*\(")),
            ("hàm dựng Ui.*", new Regex(@"\bUi\.(Rect|Img|Text|Title|Panel|Button|Bar|Chip|ElemTag|Stars|Tape|Stamp|Hint|Paper|Dim)\s*\(")),
            ("SceneKit", new Regex(@"\bSceneKit\.")),
            (".Layout(...)", new Regex(@"\.Layout\s*\(")),
        };

        // đường dẫn tương đối từ "01 Script" → lý do được phép
        static readonly Dictionary<string, string> Exceptions = new Dictionary<string, string>
        {
            // hình aola (session hình tướng làm): diễn viên dựng từ atlas lúc chạy
            ["Game/Heroes/AolaActor.cs"] = "hình aola: dựng diễn viên từ atlas",
            ["Game/Heroes/AolaSticker.cs"] = "hình aola: ghép diễn viên vào sân",
        };

        static string Root => Path.Combine(Application.dataPath, "01 Script");

        static IEnumerable<string> RuntimeFiles() =>
            Directory.GetFiles(Root, "*.cs", SearchOption.AllDirectories)
                .Select(p => p.Substring(Root.Length + 1).Replace('\\', '/'))
                .Where(r => !r.StartsWith("Editor/") && !r.StartsWith("Tests/") && !r.StartsWith("BanThu/"));

        // bỏ chú thích // và /* */ để chữ trong ghi chú không bị bắt
        static string StripComments(string src)
        {
            src = Regex.Replace(src, @"/\*.*?\*/", m => new string('\n', m.Value.Count(c => c == '\n')), RegexOptions.Singleline);
            return Regex.Replace(src, @"//[^\n]*", "");
        }

        [Test]
        public void MaRuntime_KhongSinhDoVat()
        {
            var errors = new List<string>();
            foreach (var rel in RuntimeFiles())
            {
                if (Exceptions.ContainsKey(rel)) continue;
                var lines = StripComments(File.ReadAllText(Path.Combine(Root, rel))).Split('\n');
                for (int i = 0; i < lines.Length; i++)
                    foreach (var (name, re) in Rules)
                        if (re.IsMatch(lines[i]))
                            errors.Add($"{rel}:{i + 1} {name}: {lines[i].Trim()}");
            }
            Assert.IsEmpty(errors, "Mã runtime còn sinh đồ vật (dùng prefab):\n" + string.Join("\n", errors.Take(80)));
        }

        [Test]
        public void NgoaiLe_VanConFile()
        {
            var files = new HashSet<string>(RuntimeFiles());
            foreach (var kv in Exceptions)
                Assert.IsTrue(files.Contains(kv.Key), $"Ngoại lệ thừa (file không còn): {kv.Key}");
        }
    }
}
