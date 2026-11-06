// Nét bung khi nhấn (bộ UI Sa Bàn): 5 gạch mực ngắn toả ra từ chỗ chạm rồi tan trong 0,38 giây. Prefab Assets/04 Prefabs/Kit/NetBung
// (menu "PokiClash/Prefab/Bộ UI Sa Bàn: hiệu ứng, nút sticker, chỉ khâu"), UiKit.burst trỏ tới. SketchButton gọi At khi nhả nút.
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash.UI
{
    public sealed class InkBurst : MonoBehaviour
    {
        const float Len = 0.38f;
        [SerializeField] CanvasGroup group;
        float t;

        // Dùng khi nướng prefab (Editor).
        public void Setup(CanvasGroup g) => group = g;

        // đặt nét bung tại chỗ chạm, trên cùng canvas gốc của phần tử được nhấn
        public static void At(Component from, PointerEventData e)
        {
            var prefab = Theme.Prefabs ? Theme.Prefabs.burst : null;
            if (!prefab || e == null || !from) return;
            var canvas = from.GetComponentInParent<Canvas>();
            if (!canvas) return;
            canvas = canvas.rootCanvas;
            var root = (RectTransform)canvas.transform;
            var cam = canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(root, e.position, cam, out var lp)) return;
            var b = Instantiate(prefab, root, false);
            var rt = (RectTransform)b.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = lp;
            rt.localEulerAngles = new Vector3(0, 0, Random.value * 72);
            rt.SetAsLastSibling();
        }

        void Update()
        {
            t += Mathf.Min(0.05f, Time.unscaledDeltaTime);
            float k = t / Len;
            if (k >= 1)
            {
                Destroy(gameObject);
                return;
            }
            float s = Mathf.Lerp(0.5f, 1.25f, 1 - Mathf.Pow(1 - k, 3));
            transform.localScale = new Vector3(s, s, 1);
            if (group) group.alpha = 1 - k;
        }
    }
}
