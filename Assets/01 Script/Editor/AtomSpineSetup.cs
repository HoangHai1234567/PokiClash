// Gói Unity của AtomSpine (com.atomspine.runtime, GD_Claude/23_MayBi_TraiNghiem.md): dự án đã có bộ nhập .atomik riêng
// (Editor/AtomikImporter.cs), Unity chỉ cho một ScriptedImporter mỗi đuôi, nên phải bật define ATOMSPINE_DISABLE_IMPORTER cho mọi nền
// tảng build trước khi gói vào dự án. Rig của gói (rương máy bi) nạp lúc chạy từ .bytes bằng AtomSpine.AtomikFile.Load.
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class AtomSpineSetup
    {
        const string Define = "ATOMSPINE_DISABLE_IMPORTER";
        static readonly NamedBuildTarget[] Targets = { NamedBuildTarget.Standalone, NamedBuildTarget.Android, NamedBuildTarget.iOS };

        [MenuItem("PokiClash/Cài đặt/AtomSpine: bật define tắt importer của gói", priority = 300)]
        public static void AddDefine()
        {
            foreach (var t in Targets)
            {
                var cur = PlayerSettings.GetScriptingDefineSymbols(t);
                var list = cur.Split(';').Select(s => s.Trim()).Where(s => s.Length > 0).ToList();
                if (list.Contains(Define)) continue;
                list.Add(Define);
                PlayerSettings.SetScriptingDefineSymbols(t, string.Join(";", list));
            }
            AssetDatabase.SaveAssets(); // ghi ProjectSettings.asset ngay (không thì chỉ nằm trong bộ nhớ tới khi thoát Unity)
            Debug.Log("[AtomSpine] Define " + Define + ": " + string.Join(", ", Targets.Select(t => t.TargetName + "=" + PlayerSettings.GetScriptingDefineSymbols(t))));
        }
    }
}
