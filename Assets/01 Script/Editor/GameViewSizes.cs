// Khung Game view để soi bố cục: 1080×1920 (9:16), 1080×2400 (9:20, máy dài), 1536×2048 (3:4, máy tính bảng).
// Dùng API nội bộ của Unity qua reflection; lỗi thì chỉ cảnh báo.
using System;
using System.Reflection;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class GameViewSizes
    {
        public static readonly Vector2Int[] Frames = { new Vector2Int(1080, 1920), new Vector2Int(1080, 2400), new Vector2Int(1536, 2048) };

        [MenuItem("PokiClash/Game view/1080×1920 (9:16)", priority = 200)]
        static void Size916() => Select(1080, 1920);

        [MenuItem("PokiClash/Game view/1080×2400 (máy dài)", priority = 201)]
        static void Size920() => Select(1080, 2400);

        [MenuItem("PokiClash/Game view/1536×2048 (máy tính bảng)", priority = 202)]
        static void Size34() => Select(1536, 2048);

        // Thêm cả 3 khung vào danh sách (không chọn).
        public static void EnsureAll()
        {
            foreach (var f in Frames) Find(f.x, f.y, true);
        }

        static object Group(out Type gt)
        {
            var asm = typeof(Editor).Assembly;
            var sizesType = asm.GetType("UnityEditor.GameViewSizes");
            var instance = typeof(ScriptableSingleton<>).MakeGenericType(sizesType).GetProperty("instance").GetValue(null);
            var groupType = (GameViewSizeGroupType)sizesType.GetProperty("currentGroupType").GetValue(instance);
            var group = sizesType.GetMethod("GetGroup").Invoke(instance, new object[] { (int)groupType });
            gt = group.GetType();
            return group;
        }

        static int Find(int w, int h, bool add)
        {
            try
            {
                var group = Group(out var gt);
                int count = (int)gt.GetMethod("GetTotalCount").Invoke(group, null);
                for (int i = 0; i < count; i++)
                {
                    var size = gt.GetMethod("GetGameViewSize").Invoke(group, new object[] { i });
                    var st = size.GetType();
                    if ((int)st.GetProperty("width").GetValue(size) == w && (int)st.GetProperty("height").GetValue(size) == h &&
                        st.GetProperty("sizeType").GetValue(size).ToString() == "FixedResolution")
                        return i;
                }
                if (!add) return -1;
                var asm = typeof(Editor).Assembly;
                var sizeType = asm.GetType("UnityEditor.GameViewSize");
                var kind = asm.GetType("UnityEditor.GameViewSizeType");
                var ctor = sizeType.GetConstructor(new[] { kind, typeof(int), typeof(int), typeof(string) });
                var newSize = ctor.Invoke(new[] { Enum.Parse(kind, "FixedResolution"), w, h, $"PokiClash {w}x{h}" });
                gt.GetMethod("AddCustomSize").Invoke(group, new[] { newSize });
                return count;
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[PokiClash] Không thêm được khung Game view {w}x{h}: {e.Message}");
                return -1;
            }
        }

        public static bool Select(int w, int h)
        {
            int index = Find(w, h, true);
            if (index < 0) return false;
            try
            {
                var gameViewType = typeof(Editor).Assembly.GetType("UnityEditor.GameView");
                var view = EditorWindow.GetWindow(gameViewType);
                gameViewType.GetMethod("SizeSelectionCallback", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
                    .Invoke(view, new object[] { index, null });
                return true;
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[PokiClash] Không chọn được khung Game view {w}x{h}: {e.Message}");
                return false;
            }
        }
    }
}
