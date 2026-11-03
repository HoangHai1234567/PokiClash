// Menu đặt thư mục reskin của AolaRipper, nguồn của menu PokiClash/Tướng/Nhập hình tướng aola (lưu trong EditorPrefs của máy
// này, không vào project).
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class AolaMenu
    {
        [MenuItem("PokiClash/Đặt thư mục aola...", priority = 40)]
        static void SetDir()
        {
            var cur = EditorPrefs.GetString(AolaImport.PrefKey, "");
            var dir = EditorUtility.OpenFolderPanel("Chọn thư mục reskin của aola", cur, "");
            if (string.IsNullOrEmpty(dir)) return;
            EditorPrefs.SetString(AolaImport.PrefKey, dir);
            AolaImport.ForgetDir();
            Debug.Log($"[Aola] Thư mục reskin: {dir}. Nhập hình vào project: menu PokiClash/Tướng/Nhập hình tướng aola thành prefab.");
        }

        [MenuItem("PokiClash/Tự tìm thư mục aola", priority = 41)]
        static void FindDir()
        {
            EditorPrefs.DeleteKey(AolaImport.PrefKey);
            AolaImport.ForgetDir();
            var dir = AolaImport.FindDir();
            Debug.Log(dir != null ? $"[Aola] Thư mục reskin: {dir}" : "[Aola] Không tìm thấy thư mục reskin (cần Aola*/.../reskin/<tên>/export/anim.json cạnh thư mục project hoặc ở gốc ổ đĩa).");
        }
    }
}
