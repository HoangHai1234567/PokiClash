// Canvas chuẩn của game: tham chiếu 1080 × 1920. Màn dài hơn 9:16 khớp chiều rộng (phần dôi dồn cho nền);
// màn rộng hơn (máy tính bảng 3:4) khớp chiều cao, nội dung giữ khung 1080 ở giữa, hai bên để nền.
// Cây: Canvas → Nen (phủ kín) + An toan (theo Screen.safeArea) → Khung (rộng 1080, cao theo vùng an toàn).
// Prefab Assets/04 Prefabs/Kit/CanvasManHinh. Camera ở Boot (khác scene) nên gắn lúc Awake, không kéo thả được.
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PokiCanvas : MonoBehaviour
    {
        public const float RefW = 1080, RefH = 1920;

        // camera vẽ mọi canvas (trong App ở Boot): canvas Screen Space - Camera để hình tướng (MeshRenderer) xen được giữa nền và UI
        public static Camera UiCamera;
        public const float PlaneDistance = 100;

        [SerializeField] Canvas canvas;
        [SerializeField] CanvasScaler scaler;
        [SerializeField] RectTransform bg, safe, frame;

        public Canvas Canvas => canvas;
        public RectTransform Root => (RectTransform)transform;
        public RectTransform Bg => bg; // phủ kín màn (kể cả tai thỏ, hai bên máy tính bảng)
        public RectTransform Safe => safe; // vùng an toàn
        public RectTransform Frame => frame; // khung nội dung rộng 1080 trong vùng an toàn

        Vector2Int lastSize;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Canvas c, CanvasScaler s, RectTransform bgRt, RectTransform safeRt, RectTransform frameRt)
        {
            canvas = c;
            scaler = s;
            bg = bgRt;
            safe = safeRt;
            frame = frameRt;
        }

        void Awake() => Attach();

        // gắn camera UI (App gọi lại sau khi có camera)
        public void Attach()
        {
            if (UiCamera)
            {
                canvas.renderMode = RenderMode.ScreenSpaceCamera;
                canvas.worldCamera = UiCamera;
                canvas.planeDistance = PlaneDistance;
            }
            else canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            lastSize = default;
            Update();
        }

        void Update()
        {
            var size = new Vector2Int(Screen.width, Screen.height);
            if (size == lastSize || scaler == null) return;
            lastSize = size;
            float aspect = (float)size.x / Mathf.Max(1, size.y);
            scaler.matchWidthOrHeight = aspect > RefW / RefH + 0.001f ? 1f : 0f;
        }
    }
}
