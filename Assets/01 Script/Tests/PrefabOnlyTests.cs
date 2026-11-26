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

        // đường dẫn tương đối từ "01 Script" → lý do được phép (miễn cả file)
        static readonly Dictionary<string, string> Exceptions = new Dictionary<string, string>
        {
            // hình aola (session hình tướng làm): diễn viên dựng từ atlas lúc chạy
            ["Game/Heroes/AolaActor.cs"] = "hình aola: dựng diễn viên từ atlas",
            ["Game/Heroes/AolaSticker.cs"] = "hình aola: ghép diễn viên vào sân",
            // bảo mật (Lớp 1): nạp ảnh mã hoá buộc dựng Texture2D/Sprite từ blob lúc chạy, không có bản prefab thay thế
            ["Game/Content/PokiArt.cs"] = "ảnh mã hoá: dựng Texture2D/Sprite từ blob giải mã lúc chạy",
        };

        // miễn một luật trong một file, tối đa số chỗ ghi ở đây: thêm chỗ thứ (max + 1) vẫn bị bắt (người dùng chọn 2026-11-27)
        static readonly (string file, string rule, int max, string why)[] RuleExceptions =
        {
            // component hành vi không có hình, gắn vào đồ có sẵn trong prefab ("có thì lấy, chưa có thì gắn"); UiMotion nằm trên nút ở 68 prefab
            ("UI/Kit/UiMotion.cs", "AddComponent", 1, "hành vi nhún / lún gắn vào nút có sẵn"),
            ("UI/Kit/NumberTicker.cs", "AddComponent", 1, "hành vi chạy số gắn vào chữ có sẵn"),
            ("Game/Battle/CardBend.cs", "AddComponent", 1, "hiệu ứng uốn lưới gắn vào Graphic của lá bài có sẵn"),
            // bản sao material của prefab để đổi thông số shader mỗi khung mà không ghi vào asset gốc
            ("App/Scenes/Casino/FishingPanel.cs", "new Material", 1, "nước Bến câu: phao, gợn, bóng cá đổi mỗi khung"),
            ("App/Scenes/Home/HomeScene.cs", "new Material", 1, "lưới xây Nhà: ô sáng đổi theo chỗ đặt"),
            ("App/Shop/HeroUnlockView.cs", "new Material", 1, "tranh chì mở khoá tướng: hộp, màu nhóm bút"),
            // ảnh vẽ lúc chạy từ dữ liệu, không có bản prefab thay thế
            ("App/Shop/HeroUnlockView.cs", "new Texture2D", 1, "vệt bút màu tô dần lúc chạy"),
        };

        static int Allowed(string file, string rule)
        {
            foreach (var e in RuleExceptions)
                if (e.file == file && e.rule == rule)
                    return e.max;
            return 0;
        }

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
                foreach (var (name, hits) in Hits(rel))
                {
                    int allowed = Allowed(rel, name);
                    if (hits.Count <= allowed) continue;
                    foreach (var h in hits)
                        errors.Add($"{rel}:{h} {name}" + (allowed > 0 ? $" (ngoại lệ cho {allowed} chỗ, đang có {hits.Count})" : ""));
                }
            }
            Assert.IsEmpty(errors, "Mã runtime còn sinh đồ vật (dùng prefab):\n" + string.Join("\n", errors.Take(80)));
        }

        // các dòng vi phạm của một file theo từng luật: "dòng: mã"
        static IEnumerable<(string rule, List<string> hits)> Hits(string rel)
        {
            var lines = StripComments(File.ReadAllText(Path.Combine(Root, rel))).Split('\n');
            foreach (var (name, re) in Rules)
            {
                var hits = new List<string>();
                for (int i = 0; i < lines.Length; i++)
                    if (re.IsMatch(lines[i]))
                        hits.Add($"{i + 1}: {lines[i].Trim()}");
                if (hits.Count > 0) yield return (name, hits);
            }
        }

        [Test]
        public void NgoaiLe_VanConFile()
        {
            var files = new HashSet<string>(RuntimeFiles());
            foreach (var kv in Exceptions)
                Assert.IsTrue(files.Contains(kv.Key), $"Ngoại lệ thừa (file không còn): {kv.Key}");
            foreach (var e in RuleExceptions)
            {
                Assert.IsTrue(files.Contains(e.file), $"Ngoại lệ thừa (file không còn): {e.file}");
                Assert.IsTrue(Rules.Any(r => r.name == e.rule), $"Ngoại lệ ghi sai tên luật: {e.file} / {e.rule}");
                Assert.IsTrue(Hits(e.file).Any(h => h.rule == e.rule), $"Ngoại lệ thừa (file không còn {e.rule}): {e.file}");
            }
        }

        // bộ bài tráo của trận dựng sẵn trong prefab (trước 2026-11-27 DraftDeck tự dựng lúc chạy)
        [Test]
        public void BoBaiTrao_DungSanTrongPrefabTran()
        {
            const string path = "Assets/04 Prefabs/Screens/Battle.prefab";
            var go = UnityEditor.AssetDatabase.LoadAssetAtPath<GameObject>(path);
            Assert.IsTrue(go, "Không thấy " + path);
            var deck = go.GetComponentInChildren<DraftDeck>(true);
            Assert.IsTrue(deck, "Screens/Battle chưa có DraftDeck: chạy menu PokiClash/Prefab/Trận/Bộ bài tráo: lớp + viền độ hiếm");
            Assert.IsTrue(deck.Baked, "DraftDeck trong Screens/Battle thiếu lớp, khung viền hoặc material: chạy lại menu trên");
        }
    }
}
