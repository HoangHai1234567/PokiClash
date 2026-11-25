// Bản lưu trong Editor: game lưu ở file persistentDataPath/save_v{n}.json, không ở PlayerPrefs (PlayerPrefs chỉ giữ ngôn ngữ, lọc màn
// Tướng), nên "Edit/Clear All PlayerPrefs" không đưa game về đầu (người dùng hỏi 2026-11-23).
// - "PokiClash/Bản lưu/Chơi lại từ đầu": dời mọi save_v*.json (cả .tmp; bản phiên bản cũ cũng dời, không thì game di chuyển nó lên) vào
//   thư mục bak_<giờ> cạnh đó, xoá PlayerPrefs. Đang Play thì dừng trước (App ghi bản lưu lúc thoát), dời xong vào Play lại: cốt
//   truyện, chọn tướng, hướng dẫn chạy như người mới. Không xoá gì: lấy lại bản cũ thì chép file trong bak_<giờ> về chỗ cũ khi không Play.
// - "PokiClash/Bản lưu/Mở thư mục bản lưu".
using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    [InitializeOnLoad]
    public static class SaveMenu
    {
        const string PendingKey = "PokiClash.SaveMenu.Restart";

        static SaveMenu()
        {
            EditorApplication.playModeStateChanged -= OnPlayMode;
            EditorApplication.playModeStateChanged += OnPlayMode;
        }

        static string Dir => Application.persistentDataPath;

        [MenuItem("PokiClash/Bản lưu/Chơi lại từ đầu (dời bản lưu, xoá PlayerPrefs)", priority = 160)]
        static void Restart()
        {
            var files = SaveFiles();
            string list = files.Length == 0 ? "(chưa có file lưu)" : string.Join("\n", files.Select(Path.GetFileName));
            if (!EditorUtility.DisplayDialog("Chơi lại từ đầu",
                    $"Dời bản lưu sang thư mục bak_<giờ> trong\n{Dir}\nvà xoá PlayerPrefs?\n\n{list}" +
                    (EditorApplication.isPlaying ? "\n\nĐang Play: dừng, dời xong rồi vào Play lại." : ""),
                    "Chơi lại", "Thôi"))
                return;
            if (EditorApplication.isPlaying)
            {
                // App ghi bản lưu lúc thoát Play: dời sau khi đã về Edit
                SessionState.SetBool(PendingKey, true);
                EditorApplication.isPlaying = false;
                return;
            }
            Clear();
        }

        [MenuItem("PokiClash/Bản lưu/Mở thư mục bản lưu", priority = 161)]
        static void Open()
        {
            Directory.CreateDirectory(Dir);
            Application.OpenURL("file:///" + Dir.Replace('\\', '/'));
        }

        static void OnPlayMode(PlayModeStateChange st)
        {
            if (st != PlayModeStateChange.EnteredEditMode || !SessionState.GetBool(PendingKey, false)) return;
            SessionState.EraseBool(PendingKey);
            Clear();
            EditorApplication.delayCall += () => EditorApplication.isPlaying = true;
        }

        static string[] SaveFiles() =>
            Directory.Exists(Dir)
                ? Directory.GetFiles(Dir, "save_v*.json").Concat(Directory.GetFiles(Dir, "save_v*.json.tmp")).OrderBy(p => p).ToArray()
                : new string[0];

        static void Clear()
        {
            var files = SaveFiles();
            string bak = null;
            if (files.Length > 0)
            {
                bak = Path.Combine(Dir, "bak_" + DateTime.Now.ToString("yyyyMMdd_HHmmss"));
                Directory.CreateDirectory(bak);
                foreach (var f in files) File.Move(f, Path.Combine(bak, Path.GetFileName(f)));
            }
            PlayerPrefs.DeleteAll();
            PlayerPrefs.Save();
            Debug.Log(bak != null
                ? $"[Bản lưu] Đã dời {files.Length} file sang {bak} và xoá PlayerPrefs. Lấy lại: chép file về {Dir} khi không Play."
                : "[Bản lưu] Không có file lưu; đã xoá PlayerPrefs.");
        }
    }
}
