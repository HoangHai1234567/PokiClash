// Chặn crash của TMP: phông động mà vùng xếp chữ (free/used glyph rects) hoặc ảnh atlas vượt cỡ atlas khai báo thì
// FontEngine ghi tràn bộ nhớ khi thêm chữ, Unity crash (lúc chạy test phông, hoặc sau đó khi vẽ lại giao diện). Đã gặp
// 2026-11-02: sửa tay m_AtlasWidth/Height của Pangolin 2048 → 1024 mà vùng xếp chữ còn 2047.
// Mỗi lần Editor nạp code: soát mọi TMP_FontAsset trong Assets/03 Art/Fonts; phông động bị lệch thì xoá dữ liệu atlas
// (ClearFontAssetData) để TMP dựng lại đúng cỡ khi cần chữ. Test phông gọi Problems trước khi thêm chữ.
using System.Collections.Generic;
using TMPro;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    [InitializeOnLoad]
    public static class FontAtlasGuard
    {
        const string FontDir = "Assets/03 Art/Fonts";

        static FontAtlasGuard() => EditorApplication.delayCall += () => FixAll();

        // Mô tả chỗ lệch của phông (rỗng là ổn).
        public static List<string> Problems(TMP_FontAsset f)
        {
            var errors = new List<string>();
            if (!f || f.atlasPopulationMode != AtlasPopulationMode.Dynamic) return errors;
            int w = f.atlasWidth, h = f.atlasHeight;
            var so = new SerializedObject(f); // danh sách vùng xếp chữ của TMP không mở ra ngoài
            void Check(string prop, string what)
            {
                var arr = so.FindProperty(prop);
                if (arr == null || !arr.isArray) return;
                for (int i = 0; i < arr.arraySize; i++)
                {
                    var e = arr.GetArrayElementAtIndex(i);
                    int x = e.FindPropertyRelative("m_X").intValue, y = e.FindPropertyRelative("m_Y").intValue;
                    int rw = e.FindPropertyRelative("m_Width").intValue, rh = e.FindPropertyRelative("m_Height").intValue;
                    if (x < 0 || y < 0 || x + rw > w || y + rh > h)
                    {
                        errors.Add($"{f.name}: {what} ({x}, {y}, {rw}x{rh}) vượt atlas {w}x{h}");
                        return;
                    }
                }
            }
            Check("m_FreeGlyphRects", "vùng trống xếp chữ");
            Check("m_UsedGlyphRects", "chữ đã xếp");
            if (f.atlasTextures != null)
                foreach (var t in f.atlasTextures)
                    if (t && t.width > 1 && (t.width != w || t.height != h))
                        errors.Add($"{f.name}: ảnh atlas {t.width}x{t.height} khác cỡ khai báo {w}x{h}");
            return errors;
        }

        // Sửa mọi phông động bị lệch; trả số phông đã sửa.
        public static int FixAll()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return 0;
            int fixedCount = 0;
            foreach (var guid in AssetDatabase.FindAssets("t:TMP_FontAsset", new[] { FontDir }))
            {
                var f = AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(AssetDatabase.GUIDToAssetPath(guid));
                var errors = Problems(f);
                if (errors.Count == 0) continue;
                Debug.LogWarning("[Phông] " + string.Join("; ", errors) + ". Xoá dữ liệu atlas để TMP dựng lại đúng cỡ (tránh crash).");
                f.ClearFontAssetData(true);
                EditorUtility.SetDirty(f);
                fixedCount++;
            }
            if (fixedCount > 0) AssetDatabase.SaveAssets();
            return fixedCount;
        }
    }
}
