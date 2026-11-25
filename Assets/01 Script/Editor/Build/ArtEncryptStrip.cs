// Lớp 1 (cách B) — bước build: sinh blob mã hoá cho ảnh hero rồi DỜI ảnh gốc ra ngoài Resources để bản ship không mang ảnh thô
// (AssetStudio không rip được). Viết theo đúng khuôn BuildExclude (journal + tự khôi phục khi Editor tắt ngang). An toàn:
//  - MẶC ĐỊNH TẮT (EditorPrefs): chỉ chạy khi bật qua menu, sau khi "Thử mã hoá toàn bộ ảnh hero" ĐẠT.
//  - verify blob giải ra khớp TRƯỚC khi dời ảnh gốc; ảnh nào lỗi thì BỎ QUA (giữ ảnh thô, PokiArt tự lùi về Resources.Load).
//  - ảnh nào còn bị prefab/scene tham chiếu bằng GUID thì BỎ QUA (dời sẽ vỡ tham chiếu); chỉ dời ảnh nạp thuần bằng chuỗi.
// PokiBuild gọi StripForBuild (trong try) và Restore (trong finally) cho bản phát hành.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Security;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    [InitializeOnLoad]
    public static class ArtEncryptStrip
    {
        const string Pref = "PokiClash.ArtEncryptOnBuild";
        const string EncFolder = ArtEncryptBuild.HeroRes + "/enc";
        const string Hold = "Assets/_PokiArtTam";
        static string Journal => Path.GetFullPath(Path.Combine(Application.dataPath, "../Library/PokiBuild/art_enc.txt"));

        public static bool Enabled
        {
            get => EditorPrefs.GetBool(Pref, false);
            set => EditorPrefs.SetBool(Pref, value);
        }

        [MenuItem("PokiClash/Bảo mật/Mã hoá ảnh hero khi build (bật tắt)", priority = 210)]
        static void Toggle()
        {
            Enabled = !Enabled;
            Debug.Log("[Bảo mật] Mã hoá ảnh hero khi build: " + (Enabled ? "BẬT" : "TẮT"));
        }

        [MenuItem("PokiClash/Bảo mật/Mã hoá ảnh hero khi build (bật tắt)", validate = true)]
        static bool ToggleCheck() { Menu.SetChecked("PokiClash/Bảo mật/Mã hoá ảnh hero khi build (bật tắt)", Enabled); return true; }

        // Sinh blob + dời ảnh gốc. scenes = scene sẽ vào bản build (để kiểm tham chiếu GUID). Gọi trong try của build.
        public static void StripForBuild(IEnumerable<string> scenes)
        {
            Restore(); // dọn sót từ lần trước
            if (!Enabled) return;
            var targets = ArtEncryptBuild.Collect();
            if (targets.Count == 0) return;

            // tập asset còn được tham chiếu bằng GUID (scene build + asset Resources khác, trừ chính các ảnh đích): không dời
            var targetPaths = new HashSet<string>(targets.Select(t => t.path));
            var roots = new List<string>(scenes);
            foreach (var p in AssetDatabase.GetAllAssetPaths())
            {
                if (!p.StartsWith("Assets/") || !p.Contains("/Resources/") || p.Contains("/Editor/")) continue;
                if (targetPaths.Contains(p) || AssetDatabase.IsValidFolder(p)) continue;
                roots.Add(p);
            }
            var used = new HashSet<string>(AssetDatabase.GetDependencies(roots.ToArray(), true));
            var toProcess = targets.Where(t => !used.Contains(t.path)).ToList();
            int skipRef = targets.Count - toProcess.Count;

            Directory.CreateDirectory(Path.GetDirectoryName(Journal));
            if (!AssetDatabase.IsValidFolder(Hold)) AssetDatabase.CreateFolder("Assets", Path.GetFileName(Hold));
            var lines = new List<string>();
            int done = 0, skipErr = 0;

            var prev = ArtEncryptBuild.SetReadable(toProcess, true); // bật readable theo đợt (nhẹ hơn toggle từng ảnh)
            try
            {
                try
                {
                    AssetDatabase.StartAssetEditing();
                    foreach (var t in toProcess)
                    {
                        byte[] enc = ArtEncryptBuild.EncodeReadable(t, out _, out _, out string err);
                        if (enc == null) { skipErr++; Debug.LogWarning($"[Bảo mật] Bỏ qua {t.key}: {err}"); continue; }
                        // verify giải ra được + đúng gói trước khi dời ảnh gốc
                        var plain = PokiCrypt.TryDecrypt(enc, "texture");
                        if (plain == null || TexBlob.Unpack(plain) == null)
                        {
                            skipErr++; Debug.LogWarning($"[Bảo mật] Bỏ qua {t.key}: blob không giải lại được."); continue;
                        }

                        string blobPath = EncFolder + "/" + t.key + ".bytes";
                        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(Path.Combine(Application.dataPath, "..", blobPath))));
                        File.WriteAllBytes(Path.GetFullPath(Path.Combine(Application.dataPath, "..", blobPath)), enc);

                        string held = Hold + "/" + t.key.Replace('/', '~') + Path.GetExtension(t.path);
                        lines.Add(t.path + "\t" + held + "\t" + blobPath);
                    }
                }
                finally { AssetDatabase.StopAssetEditing(); AssetDatabase.Refresh(); }
            }
            finally { ArtEncryptBuild.RestoreReadable(prev); } // trả readable TRƯỚC khi dời ảnh gốc

            // dời ảnh gốc (ghi journal trước mỗi lần dời để khôi phục được cả khi tắt ngang)
            var moved = new List<string>();
            foreach (var line in lines)
            {
                var parts = line.Split('\t');
                moved.Add(line);
                File.WriteAllLines(Journal, moved);
                string errMove = AssetDatabase.MoveAsset(parts[0], parts[1]);
                if (!string.IsNullOrEmpty(errMove))
                {
                    Debug.LogWarning($"[Bảo mật] Không dời được {parts[0]}: {errMove} (ảnh thô vẫn vào build).");
                    moved.RemoveAt(moved.Count - 1);
                    File.WriteAllLines(Journal, moved);
                    // xoá blob thừa của ảnh không dời được (tránh trùng): để nguyên cũng được vì PokiArt ưu tiên blob; nhưng ảnh gốc còn -> giữ nhất quán, xoá blob
                    try { File.Delete(Path.GetFullPath(Path.Combine(Application.dataPath, "..", parts[2]))); } catch { }
                    continue;
                }
                done++;
            }
            Debug.Log($"[Bảo mật] Mã hoá ảnh hero: dời {done} ảnh gốc ra ngoài build, giữ {skipRef} (còn bị tham chiếu), bỏ {skipErr} (lỗi). Trả lại sau build.");
        }

        // Trả ảnh gốc về chỗ cũ, xoá blob. Gọi sau build và khi nạp code (nếu build tắt ngang).
        public static void Restore()
        {
            if (!File.Exists(Journal)) return;
            int back = 0, bad = 0;
            var remain = new List<string>();
            foreach (var line in File.ReadAllLines(Journal))
            {
                var p = line.Split('\t');
                if (p.Length != 3) continue;
                try { File.Delete(Path.GetFullPath(Path.Combine(Application.dataPath, "..", p[2]))); } catch { }
                try { File.Delete(Path.GetFullPath(Path.Combine(Application.dataPath, "..", p[2] + ".meta"))); } catch { }
                if (!AssetDatabase.IsValidFolder(Path.GetDirectoryName(p[1])) && !File.Exists(Path.GetFullPath(Path.Combine(Application.dataPath, "..", p[1]))))
                    continue; // chưa kịp dời
                string err = AssetDatabase.MoveAsset(p[1], p[0]);
                if (string.IsNullOrEmpty(err)) back++;
                else { Debug.LogError($"[Bảo mật] Không trả lại được {p[1]} -> {p[0]}: {err}"); bad++; remain.Add(line); }
            }
            AssetDatabase.Refresh();
            // dọn thư mục enc + hold nếu rỗng
            TryDeleteIfEmpty(EncFolder);
            TryDeleteIfEmpty(Hold);
            if (bad > 0) { File.WriteAllLines(Journal, remain); return; }
            File.Delete(Journal);
            if (back > 0) Debug.Log($"[Bảo mật] Đã trả lại {back} ảnh hero gốc vào Resources.");
        }

        static void TryDeleteIfEmpty(string folder)
        {
            if (!AssetDatabase.IsValidFolder(folder)) return;
            string full = Path.GetFullPath(Path.Combine(Application.dataPath, "..", folder));
            if (Directory.Exists(full) && !Directory.EnumerateFileSystemEntries(full).Any())
                AssetDatabase.DeleteAsset(folder);
        }

        static ArtEncryptStrip() => EditorApplication.delayCall += () =>
        {
            if (!BuildPipeline.isBuildingPlayer) Restore();
        };
    }
}
