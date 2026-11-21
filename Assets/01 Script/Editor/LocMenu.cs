// Menu PokiClash/Ngôn ngữ (2026-11-21): chọn ngôn ngữ cho Play trong Editor, ghi chuỗi chưa dịch gặp lúc chạy, kiểm bảng dịch.
// Ngôn ngữ lưu ở PlayerPrefs "PokiClash.Lang" như nút Ngôn ngữ ở Sổ tay; đang Play thì đổi ngay (App.SetLanguage).
// Bảng dịch: Assets/Resources/Loc/<mã>/*.json. Kiểm bảng = LocTests (đủ bản dịch cho chuỗi trong code, prefab, dữ liệu).
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class LocMenu
    {
        const string Root = "PokiClash/Ngôn ngữ/";

        [MenuItem(Root + "Tiếng Việt", priority = 1)]
        static void UseVi() => Use(Loc.Vi);

        [MenuItem(Root + "English", priority = 2)]
        static void UseEn() => Use(Loc.En);

        [MenuItem(Root + "Tiếng Việt", true)]
        static bool CheckVi()
        {
            Menu.SetChecked(Root + "Tiếng Việt", Current() == Loc.Vi);
            return true;
        }

        [MenuItem(Root + "English", true)]
        static bool CheckEn()
        {
            Menu.SetChecked(Root + "English", Current() == Loc.En);
            return true;
        }

        static string Current()
        {
            var s = PlayerPrefs.GetString(LocService.PrefKey, "");
            return string.IsNullOrEmpty(s) ? Loc.Vi : s;
        }

        static void Use(string lang)
        {
            if (Application.isPlaying && App.I) App.SetLanguage(lang);
            else
            {
                PlayerPrefs.SetString(LocService.PrefKey, lang);
                PlayerPrefs.Save();
            }
            Debug.Log($"[Loc] Ngôn ngữ: {lang}" + (Application.isPlaying ? "" : " (áp dụng ở lần Play tới)"));
        }

        // Ghi chú bút chì ở vùng boss là ảnh có chữ (Islands/Co/trung_ghi_*): bản dịch trung_ghi_*_<mã> vẽ bằng ArtGen/Islands/ve_trung_en.py.
        // Thêm các ảnh đó vào ZoneScene.eggArt của Screens/Zone (giữ nguyên ảnh đang có). "Đảo vùng đất/Dựng cờ ải, vùng boss" cũng gom.
        [MenuItem(Root + "Gắn ghi chú tiếng Anh vào màn đảo", priority = 10)]
        static void AddNoteArt()
        {
            const string zonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
            var add = AssetDatabase.FindAssets("trung_ghi t:Sprite", new[] { "Assets/03 Art/Islands/Co" })
                .Select(g => AssetDatabase.LoadAssetAtPath<Sprite>(AssetDatabase.GUIDToAssetPath(g)))
                .Where(sp => sp && sp.name.StartsWith("trung_ghi") && sp.name.EndsWith("_" + Loc.En)).ToList();
            var zone = PrefabUtility.LoadPrefabContents(zonePath);
            try
            {
                var scene = zone.GetComponentInChildren<ZoneScene>(true);
                var so = new SerializedObject(scene);
                var ea = so.FindProperty("eggArt");
                var have = new System.Collections.Generic.HashSet<Object>();
                for (int i = 0; i < ea.arraySize; i++) have.Add(ea.GetArrayElementAtIndex(i).objectReferenceValue);
                int n = 0;
                foreach (var sp in add)
                {
                    if (have.Contains(sp)) continue;
                    ea.arraySize++;
                    ea.GetArrayElementAtIndex(ea.arraySize - 1).objectReferenceValue = sp;
                    n++;
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                if (n > 0) PrefabUtility.SaveAsPrefabAsset(zone, zonePath);
                Debug.Log($"[Loc] Gắn {n} ghi chú tiếng Anh vào Screens/Zone (tìm thấy {add.Count})");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(zone);
            }
        }

        [MenuItem(Root + "Ghi chuỗi chưa dịch gặp lúc chạy", priority = 20)]
        static void DumpMissing()
        {
            var path = Path.GetFullPath("Temp/loc_missing.txt");
            File.WriteAllLines(path, LocService.Missing.OrderBy(x => x));
            Debug.Log($"[Loc] {LocService.Missing.Count} chuỗi chưa dịch → {path}");
            EditorUtility.RevealInFinder(path);
        }
    }
}
