// Bỏ khỏi bản build những thứ chắc chắn không dùng (bộ build PokiBuild, người dùng 2026-11-21). Mọi thứ trong thư mục Resources đều
// vào bản build dù không ai gọi tới, nên trước build dời tạm các thư mục thừa ra ngoài Resources (AssetDatabase.MoveAsset: giữ
// GUID, .meta đi theo, không nhập lại) rồi dời về ngay sau build. Build hỏng hay Editor tắt giữa chừng thì lần nạp code kế tiếp tự
// dời về theo sổ ghi Library/PokiBuild/doi_tam.txt.
// Hiện bỏ: thư mục dạng tướng trong Heroes/Resources (có <dạng>/<dạng>.asset kiểu AolaAnim) khi đủ cả ba điều kiện:
//  1. tên không còn trong heroes.json, cả tướng lẫn lính (AolaImport.StaleForms);
//  2. không file nào của nó nằm trong cây phụ thuộc của scene trong build và của asset Resources khác (prefab tướng trỏ tới thì nó
//     vẫn vào bản build qua tham chiếu, dời cũng vô ích);
//  3. tên không xuất hiện trong code chạy (Resources.Load theo chuỗi, như HatHon nạp "ky_nguyen_2/...").
// Lần đầu (2026-11-21): 27 dạng cũ của các suất đã đổi tướng (bo_cap_*, hong_lien_*, huyen_viem_*, lan_hoa_*, tam_kiem_*...).
// Thêm (2026-11-23): thư mục cố định trong UnusedDirs (phông mẫu LiberationSans của TextMesh Pro, ~1 MB: phông mặc định của TMP đã là
// Pangolin, game không gọi phông theo tên), cùng hai điều kiện 2 và 3 ở trên.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class BuildExclude
    {
        public sealed class Item
        {
            public string path; // thư mục asset (Assets/...)
            public string why;
        }

        const string Hold = "Assets/_PokiBuildTam";
        static string Journal => Path.GetFullPath(Path.Combine(Application.dataPath, "../Library/PokiBuild/doi_tam.txt"));

        // thư mục trong Resources chắc không dùng (tên thư mục phải khác mọi thư mục dạng tướng: cùng chỗ tạm dời Hold); chữ để soát code
        static readonly (string dir, string word, string why)[] UnusedDirs =
        {
            ("Assets/TextMesh Pro/Resources/Fonts & Materials", "LiberationSans", "phông mẫu LiberationSans của TextMesh Pro"),
        };

        // Danh sách sẽ bỏ, không dời gì. scenes: scene sẽ vào bản build.
        public static List<Item> Plan(IEnumerable<string> scenes)
        {
            var res = new List<Item>();
            var cands = new List<string>();
            var why = new Dictionary<string, (string word, string why)>();
            foreach (var name in AolaImport.StaleForms())
            {
                string dir = AolaImport.ResDir + "/" + name;
                if (!AssetDatabase.LoadAssetAtPath<AolaAnim>($"{dir}/{name}.asset")) continue;
                cands.Add(dir);
                why[dir] = (name, "dạng tướng không còn tướng/lính nào dùng");
            }
            foreach (var u in UnusedDirs)
            {
                if (!AssetDatabase.IsValidFolder(u.dir)) continue;
                cands.Add(u.dir);
                why[u.dir] = (u.word, u.why);
            }
            if (cands.Count == 0) return res;

            // gốc của cây phụ thuộc: scene trong build + mọi asset trong thư mục Resources (trừ Editor) không thuộc thư mục ứng viên
            var prefixes = cands.Select(c => c + "/").ToArray();
            var roots = new List<string>(scenes);
            foreach (var p in AssetDatabase.GetAllAssetPaths())
            {
                if (!p.StartsWith("Assets/") || !p.Contains("/Resources/") || p.Contains("/Editor/")) continue;
                if (prefixes.Any(p.StartsWith) || AssetDatabase.IsValidFolder(p)) continue;
                roots.Add(p);
            }
            var used = new HashSet<string>(AssetDatabase.GetDependencies(roots.ToArray(), true));
            string code = RuntimeCode();
            foreach (var dir in cands)
            {
                var (name, reason) = why[dir];
                var files = AssetDatabase.FindAssets("", new[] { dir }).Select(AssetDatabase.GUIDToAssetPath);
                string hit = files.FirstOrDefault(used.Contains);
                if (hit != null)
                {
                    Debug.Log($"[Build] Giữ {dir}: {hit} vẫn được trỏ tới.");
                    continue;
                }
                if (code.Contains("\"" + name) || code.Contains(name + "\""))
                {
                    Debug.Log($"[Build] Giữ {dir}: code chạy có nhắc \"{name}\".");
                    continue;
                }
                res.Add(new Item { path = dir, why = reason });
            }
            return res;
        }

        // nội dung mọi file .cs chạy trong game (bỏ thư mục Editor)
        static string RuntimeCode()
        {
            var sb = new StringBuilder();
            foreach (var f in Directory.EnumerateFiles(Application.dataPath, "*.cs", SearchOption.AllDirectories))
            {
                var rel = f.Replace('\\', '/');
                if (rel.Contains("/Editor/")) continue;
                sb.Append(File.ReadAllText(f));
            }
            return sb.ToString();
        }

        // Dời các thư mục ra ngoài Resources. Ghi sổ trước mỗi lần dời để dời về được cả khi Editor tắt giữa chừng.
        public static void Apply(List<Item> items)
        {
            Restore(); // còn sót từ lần build trước
            if (items == null || items.Count == 0) return;
            Directory.CreateDirectory(Path.GetDirectoryName(Journal));
            if (!AssetDatabase.IsValidFolder(Hold)) AssetDatabase.CreateFolder("Assets", Path.GetFileName(Hold));
            var lines = new List<string>();
            foreach (var it in items)
            {
                string dst = Hold + "/" + Path.GetFileName(it.path);
                lines.Add(it.path + "\t" + dst);
                File.WriteAllLines(Journal, lines);
                string err = AssetDatabase.MoveAsset(it.path, dst);
                if (string.IsNullOrEmpty(err)) continue;
                Debug.LogWarning($"[Build] Không dời được {it.path}: {err} (vẫn vào bản build)");
                lines.RemoveAt(lines.Count - 1);
                File.WriteAllLines(Journal, lines);
            }
            Debug.Log($"[Build] Tạm dời {lines.Count} thư mục ra ngoài Resources (dời về sau build).");
        }

        // Dời về chỗ cũ theo sổ ghi. Gọi sau build và khi nạp code.
        public static void Restore()
        {
            if (!File.Exists(Journal)) return;
            int back = 0, bad = 0;
            foreach (var line in File.ReadAllLines(Journal))
            {
                var p = line.Split('\t');
                if (p.Length != 2) continue;
                if (!AssetDatabase.IsValidFolder(p[1])) continue; // chưa kịp dời
                if (AssetDatabase.IsValidFolder(p[0]))
                {
                    Debug.LogError($"[Build] {p[0]} và {p[1]} cùng có: không dời về, xem tay.");
                    bad++;
                    continue;
                }
                string err = AssetDatabase.MoveAsset(p[1], p[0]);
                if (string.IsNullOrEmpty(err)) back++;
                else
                {
                    Debug.LogError($"[Build] Không dời về được {p[1]} → {p[0]}: {err}");
                    bad++;
                }
            }
            if (bad > 0) return; // giữ sổ để lần sau thử lại
            File.Delete(Journal);
            if (AssetDatabase.IsValidFolder(Hold) && !Directory.EnumerateFileSystemEntries(Hold).Any()) AssetDatabase.DeleteAsset(Hold);
            if (back > 0) Debug.Log($"[Build] Đã dời về {back} thư mục vào Resources.");
        }

        [InitializeOnLoadMethod]
        static void OnLoad() => EditorApplication.delayCall += () =>
        {
            if (!BuildPipeline.isBuildingPlayer) Restore();
        };
    }
}
