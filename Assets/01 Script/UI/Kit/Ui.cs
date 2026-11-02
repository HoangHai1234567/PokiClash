// Tiện ích giao diện lúc chạy: sinh bản sao prefab (Ui.Spawn), đặt RectTransform theo neo (Place, Stretch).
// Mọi giao diện là prefab làm sẵn trong Assets/04 Prefabs (change convert-to-prefabs); code chạy không dựng gì.
// Cỡ theo khung 1080 × 1920 (gấp đôi số px của bản web).
using UnityEngine;

namespace PokiClash.UI
{
    public enum BtnColor { Red, Green, Blue, Orange, Purple, Yellow, Paper, Custom }
    public enum BtnSize { Big, Normal, Small, Tiny, Round }
    public enum FontKind { Title, Bold, Body }

    public static class Ui
    {
        // Sinh bản sao prefab dưới parent, giữ toạ độ cục bộ của prefab. Ngoài Play (Editor) bản sao giữ liên kết prefab.
        public static T Spawn<T>(T prefab, Transform parent) where T : Component
        {
#if UNITY_EDITOR
            if (!Application.isPlaying)
            {
                var go = (GameObject)UnityEditor.PrefabUtility.InstantiatePrefab(prefab.gameObject, parent);
                return go.GetComponent<T>();
            }
#endif
            return Object.Instantiate(prefab, parent, false);
        }

        public static RectTransform Stretch(this RectTransform rt, float left = 0, float top = 0, float right = 0, float bottom = 0)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = new Vector2(left, bottom);
            rt.offsetMax = new Vector2(-right, -top);
            return rt;
        }

        // đặt theo điểm neo (0..1), toạ độ lệch và cỡ
        public static RectTransform Place(this RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size, Vector2? pivot = null)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = pivot ?? anchor;
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
            return rt;
        }
    }
}
