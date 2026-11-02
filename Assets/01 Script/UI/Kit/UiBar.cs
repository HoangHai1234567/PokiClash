// Thanh máu (có khiên phía phải và vệt vàng lùi chậm), mana, nộ (đầy thì phát sáng), EXP, mảnh. Chép .bar của bản web.
// Prefab Assets/04 Prefabs/Kit/Thanh: loại thanh chọn trong Inspector (màu phần đầy đổi theo).
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiBar : MonoBehaviour
    {
        public enum Kind { Hp, Mana, Rage, Exp, Shard }

        [SerializeField] Kind kind;
        [SerializeField] RectTransform area, main, ghost, shield;
        [SerializeField] Image mainImg;
        [SerializeField] TextMeshProUGUI label;

        float target, ghostValue, shown, shieldTarget;
        float ghostDelay;
        bool full;

        public static Color ColorOf(Kind k) =>
            k == Kind.Mana ? Theme.Mana : k == Kind.Rage ? Theme.Rage : k == Kind.Exp ? Theme.Exp : k == Kind.Shard ? Theme.Hex("#7ee0d0") : Theme.Hp;

        public Kind Type => kind;
        public TextMeshProUGUI Label => label;

        // Dùng khi nướng prefab (Editor): gắn các phần đã dựng.
        public void Setup(Kind k, RectTransform areaRt, RectTransform mainRt, RectTransform ghostRt, RectTransform shieldRt, TextMeshProUGUI text)
        {
            kind = k;
            area = areaRt;
            main = mainRt;
            ghost = ghostRt;
            shield = shieldRt;
            mainImg = main.GetComponent<Image>();
            label = text;
        }

        public void SetKind(Kind k)
        {
            kind = k;
            if (mainImg) mainImg.color = ColorOf(k);
        }

#if UNITY_EDITOR
        void OnValidate()
        {
            if (mainImg) mainImg.color = ColorOf(kind);
        }
#endif

        float Width => area.rect.width;

        // v/max: giá trị; shieldV: khiên (cùng đơn vị máu); text: chữ thay cho "v/max"
        public void Set(float v, float max, float shieldV = 0, string text = null, bool instant = false)
        {
            float p = Mathf.Clamp01(v / Mathf.Max(1, max));
            if (p < target) ghostDelay = 0.35f; // mất máu: vệt vàng đứng lại một chút rồi lùi
            target = p;
            shieldTarget = Mathf.Clamp01(shieldV / Mathf.Max(1, max));
            if (instant)
            {
                shown = ghostValue = p;
                Apply();
            }
            if (label) label.text = text ?? $"{Mathf.RoundToInt(v)}/{Mathf.RoundToInt(max)}";
            full = v >= max;
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            // nảy nhẹ như cubic-bezier(0.3, 1.4, 0.6, 1) của web
            shown = Mathf.Lerp(shown, target, 1 - Mathf.Exp(-dt * 14));
            if (ghostDelay > 0) ghostDelay -= dt;
            else ghostValue = ghostValue > shown ? Mathf.MoveTowards(ghostValue, shown, dt * 0.9f) : shown;
            Apply();
            if (kind == Kind.Rage)
            {
                float glow = full ? 0.5f + 0.5f * Mathf.Sin(Time.unscaledTime * Mathf.PI / 0.6f) : 0;
                mainImg.color = Color.Lerp(Theme.Rage, Theme.Hex("#ffd36a"), glow * 0.55f);
            }
        }

        void Apply()
        {
            float w = Width;
            main.sizeDelta = new Vector2(w * shown, 0);
            ghost.sizeDelta = new Vector2(w * Mathf.Max(ghostValue, shown), 0);
            shield.sizeDelta = new Vector2(w * shieldTarget, 0);
        }
    }
}
