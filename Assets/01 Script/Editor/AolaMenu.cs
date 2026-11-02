// Menu đặt thư mục reskin của aola cho Editor và bản dev (lưu trong EditorPrefs của máy này, không vào project).
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class AolaMenu
    {
        [MenuItem("PokiClash/Đặt thư mục aola (bản dev)...", priority = 40)]
        static void SetDir()
        {
            var cur = EditorPrefs.GetString(AolaActor.PrefKey, "");
            var dir = EditorUtility.OpenFolderPanel("Chọn thư mục reskin của aola", cur, "");
            if (string.IsNullOrEmpty(dir)) return;
            EditorPrefs.SetString(AolaActor.PrefKey, dir);
            AolaActor.ForgetDir();
            Debug.Log($"[Aola] Thư mục reskin: {dir}. Hình nạp trong Editor, hoặc bản build có define POKICLASH_DEV.");
        }

        [MenuItem("PokiClash/Tự tìm thư mục aola (bản dev)", priority = 41)]
        static void FindDir()
        {
            EditorPrefs.DeleteKey(AolaActor.PrefKey);
            AolaActor.ForgetDir();
            var dir = AolaActor.FindDir();
            Debug.Log(dir != null ? $"[Aola] Thư mục reskin: {dir}" : "[Aola] Không tìm thấy thư mục reskin (cần <ổ>:/Aola*/.../reskin/<tên>/export/anim.json).");
        }
    }
}
