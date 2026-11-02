// Co RectTransform vào Screen.safeArea (tai thỏ, thanh điều hướng). Đặt trên một khung phủ kín canvas.
using UnityEngine;

namespace PokiClash
{
    [RequireComponent(typeof(RectTransform))]
    public sealed class SafeArea : MonoBehaviour
    {
        Rect last;
        Vector2Int lastScreen;

        // dùng để thử trong Editor: vùng an toàn giả (tỉ lệ 0..1), Rect rỗng = tắt
        public static Rect Simulated;

        void OnEnable() => Apply(true);

        void Update() => Apply(false);

        void Apply(bool force)
        {
            var safe = Simulated.width > 0
                ? new Rect(Simulated.x * Screen.width, Simulated.y * Screen.height, Simulated.width * Screen.width, Simulated.height * Screen.height)
                : Screen.safeArea;
            var screen = new Vector2Int(Screen.width, Screen.height);
            if (!force && safe == last && screen == lastScreen) return;
            last = safe;
            lastScreen = screen;
            if (screen.x <= 0 || screen.y <= 0) return;
            var rt = (RectTransform)transform;
            rt.anchorMin = new Vector2(safe.xMin / screen.x, safe.yMin / screen.y);
            rt.anchorMax = new Vector2(safe.xMax / screen.x, safe.yMax / screen.y);
            rt.offsetMin = rt.offsetMax = Vector2.zero;
        }
    }
}
