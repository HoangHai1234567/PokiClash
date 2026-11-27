// Nút tạm dừng trên thanh trận (Screens/Battle, BattleView.p.pauseBtn; người dùng báo 2026-11-27 "nút pause nhìn mờ và xấu"): nút tròn kit
// bị kéo thành bầu dục 84 x 104, icon hai vạch ruột kem nằm trên nền giấy kem nên chỉ còn nét viền mảnh, lại bị kéo giãn theo nút.
// Menu "PokiClash/Prefab/Trận/Trận: nút tạm dừng tròn, vạch mực đặc" (hoặc cờ Temp/tran_nut_dung_build.flag) đặt nút tròn đều Size x Size,
// icon giữa nút giữ tỉ lệ, tô màu mực (ruột kem nhân màu mực thành vạch đặc). Chạy lại nhiều lần ra như nhau.
using System.IO;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class BattlePauseButtonMenu
    {
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
        const float Size = 84, IconSize = 44;

        [MenuItem("PokiClash/Prefab/Trận/Trận: nút tạm dừng tròn, vạch mực đặc", priority = 66)]
        public static void Build()
        {
            var root = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var view = root.GetComponentInChildren<BattleView>(true);
                var btn = view ? (SketchButton)new SerializedObject(view).FindProperty("p.pauseBtn").objectReferenceValue : null;
                if (!btn)
                {
                    Debug.LogError("[Trận] Battle.prefab không có nút tạm dừng (BattleView.p.pauseBtn)");
                    return;
                }
                var rt = btn.Rect;
                rt.sizeDelta = new Vector2(Size, Size);
                if (btn.TryGetComponent<LayoutElement>(out var le))
                {
                    le.preferredWidth = le.minWidth = Size;
                    le.preferredHeight = le.minHeight = Size;
                }
                var icon = btn.transform.Find("icon");
                if (icon && icon.TryGetComponent<Image>(out var img))
                {
                    var irt = img.rectTransform;
                    irt.anchorMin = irt.anchorMax = irt.pivot = new Vector2(0.5f, 0.5f);
                    irt.anchoredPosition = Vector2.zero;
                    irt.sizeDelta = new Vector2(IconSize, IconSize);
                    img.preserveAspect = true;
                    img.color = Theme.Ink;
                }
                else Debug.LogWarning("[Trận] nút tạm dừng không có con \"icon\": chỉ sửa cỡ nút");
                PrefabUtility.SaveAsPrefabAsset(root, BattlePath);
                Debug.Log($"[Trận] Đã sửa nút tạm dừng ở {BattlePath}: tròn {Size} x {Size}, icon {IconSize} màu mực, giữ tỉ lệ.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var flag = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/tran_nut_dung_build.flag"));
            if (!File.Exists(flag)) return;
            File.Delete(flag);
            Build();
        }
    }
}
