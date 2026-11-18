// Cờ ải xen giữa trên đường của đảo vùng đất (prefab Assets/04 Prefabs/Items/CoAi, menu "PokiClash/Đảo vùng đất/Dựng cờ ải (CoAi)"),
// thay chấm tròn có số (góp ý 2026-11-18: "chia đều các ô ải ra, không cần phải hiện số, các ô này phải làm nổi bật để người chơi dễ
// thấy", "có thể đổi sang dạng cờ cũng được"). Ô đá dưới chân, cán gỗ, vải đuôi én phấp phới bằng 6 khung ảnh
// (Assets/03 Art/Islands/Co, vẽ bằng ArtGen/Islands/land_thuy/m0/ve_co.py). Vải và ô nhuộm theo trạng thái: chưa mở xanh đậm,
// đã qua vàng, đang đánh đỏ cam to hơn, phồng nhịp, bay nhanh. Gốc prefab đặt ở chân cờ (zoom phóng bù quanh chân), vùng chạm phủ
// cả cờ. Chạm mở hộp chuẩn bị trận.
using System;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class LandFlag : MonoBehaviour
    {
        // khớp ve_co.py: hình vẽ ở cỡ cờ 104 (land.pip), 2 điểm ảnh mỗi đơn vị bản đồ; đỉnh vải dưới núm 132 đơn vị trên chân;
        // chỗ gắn vải (góc trên trái, theo tỉ lệ ảnh vải); chân cán (mũi nhọn, theo tỉ lệ ảnh cán)
        public const float RefSize = 104, PxPerUnit = 2, ClothTop = 132, PoleSink = 6;
        static readonly Vector2 ClothPivot = new Vector2(0.0892f, 0.8051f), PolePivot = new Vector2(0.5f, 0.0427f);
        // chân cờ trong khung gốc (tỉ lệ từ trái, từ dưới; vải bay sang phải nên vùng chạm lệch phải) và cỡ vùng chạm theo cỡ cờ
        const float FootX = 0.3f, FootY = 0.14f, HitW = 1.6f, HitH = 1.75f;
        public static readonly Color Locked = Theme.Hex("#4d72b8"), Cleared = Theme.Hex("#f4bf3a"), Current = Theme.Hex("#ff4d3a");

        [SerializeField] ClickCatcher hit;
        [SerializeField] RectTransform body;
        [SerializeField] Image stone, cloth, pole;
        [SerializeField] Pulse pulse;
        [SerializeField] Sprite[] wave;

        float fps, fpsOpen, phase;
        Color look;
        bool isCurrent;
        public const float PopTime = 0.38f;
        int shown = -1;

        public RectTransform Rect => (RectTransform)transform;
        public Vector2 Foot { get; private set; } // chỗ chân cờ trên khung ảnh (gốc trên trái, y âm xuống)
        public int Idx { get; private set; }      // số ải (vùng boss của cờ)

        // Dùng khi dựng prefab (Editor).
        public void Setup(ClickCatcher hitArea, RectTransform bodyRect, Image stoneImg, Image clothImg, Image poleImg, Pulse bodyPulse, Sprite[] frames)
        {
            hit = hitArea;
            body = bodyRect;
            stone = stoneImg;
            cloth = clothImg;
            pole = poleImg;
            pulse = bodyPulse;
            wave = frames;
        }

        // foot: chân cờ trên khung ảnh đảo; size, sizeNow: cỡ cờ thường / cờ ải đang đánh (land.pip, land.pipNow); locked: cờ ở vùng
        // boss chưa mở (cờ nét chưa tô màu như bản phác chì của vùng, vải đứng yên; mây phủ nằm trên)
        public void Bind(StageDef st, bool open, bool cleared, bool current, Vector2 foot, Action onClick, float size, float sizeNow,
            bool locked = false)
        {
            name = "co_" + st.idx;
            Idx = st.idx;
            Foot = foot;
            float s = current ? sizeNow : size, k = s / RefSize / PxPerUnit;
            var rt = Rect;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(FootX, FootY);
            rt.anchoredPosition = foot;
            rt.sizeDelta = new Vector2(s * HitW, s * HitH);
            rt.localScale = Vector3.one;

            body.anchorMin = body.anchorMax = rt.pivot; // các mảnh tính từ chân cờ
            body.sizeDelta = Vector2.zero;
            body.anchoredPosition = Vector2.zero;
            body.localScale = Vector3.one;
            Place(stone, new Vector2(0.5f, 0.5f), Vector2.zero, k);
            Place(pole, PolePivot, new Vector2(0, -PoleSink * s / RefSize), k);
            Place(cloth, ClothPivot, new Vector2(0, (ClothTop - PoleSink) * s / RefSize), k); // ClothTop tính từ mũi cán

            look = cleared ? Cleared : current ? Current : Locked;
            isCurrent = current;
            fpsOpen = current ? 9 : cleared ? 6 : 4; // đang đánh bay nhanh, đã qua phấp phới vừa, chưa mở lững lờ; mỗi cờ lệch nhịp
            SetLocked(locked);
            phase = st.idx * 1.7f;
            shown = -1;
            pulse.enabled = current;
            hit.OnClick = () =>
            {
                SketchButton.Sound?.Invoke("click");
                onClick();
            };
            Update();
        }

        // vùng boss khoá: cờ chưa mọc (ẩn); mở: màu theo trạng thái (người dùng 2026-11-18: "cờ khi mọc lên tween từng cái một")
        public void SetLocked(bool locked)
        {
            cloth.color = look;
            stone.color = Color.Lerp(Color.white, look, 0.45f);
            pole.color = Color.white;
            fps = fpsOpen;
            shown = -1;
            gameObject.SetActive(!locked);
            if (!locked) Update();
        }

        // mọc lên sau delay giây: từ chân cờ nảy cao lên, quá đà rồi về (vùng boss vừa mở, từng cờ một theo đường)
        public void PopIn(float delay)
        {
            SetLocked(false);
            pulse.enabled = false; // Pulse lấy cỡ gốc lúc bật: bật lại khi đã mọc xong
            body.localScale = new Vector3(1, 0, 1);
            StartCoroutine(Pop(delay));
        }

        System.Collections.IEnumerator Pop(float delay)
        {
            if (delay > 0) yield return new WaitForSecondsRealtime(delay);
            SketchButton.Sound?.Invoke("pick");
            for (float t = 0; t < PopTime; t += Time.unscaledDeltaTime)
            {
                float u = t / PopTime;
                float y = 1 + Mathf.Sin(u * Mathf.PI) * 0.22f * (1 - u) + (Mathf.SmoothStep(0, 1, Mathf.Min(1, u * 1.8f)) - 1);
                float x = 1 - Mathf.Sin(u * Mathf.PI * 2) * 0.08f * (1 - u);
                body.localScale = new Vector3(x, Mathf.Max(0, y), 1);
                yield return null;
            }
            body.localScale = Vector3.one;
            pulse.enabled = isCurrent;
        }

        static void Place(Image img, Vector2 pivot, Vector2 at, float k)
        {
            var r = img.rectTransform;
            r.anchorMin = r.anchorMax = new Vector2(0.5f, 0.5f);
            r.pivot = pivot;
            r.anchoredPosition = at;
            r.sizeDelta = img.sprite ? img.sprite.rect.size * k : Vector2.zero;
            img.raycastTarget = false;
        }

        void Update()
        {
            if (wave == null || wave.Length == 0) return;
            int f = (int)Mathf.Repeat(Time.unscaledTime * fps + phase, wave.Length);
            if (f == shown) return;
            shown = f;
            cloth.sprite = wave[f];
        }
    }
}
