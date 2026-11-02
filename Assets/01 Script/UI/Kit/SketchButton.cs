// Nút vẽ tay: nhấn thì lún xuống (bóng thu lại, thân dịch phải xuống như web .btn:active), thả thì bật lên, kêu "click".
// Prefab theo cỡ ở Assets/04 Prefabs/Kit (Nut_To, Nut_Vua, Nut_Nho, Nut_Ti, Nut_Tron). Màu chọn bằng trường Màu trong Inspector:
// đổi là nền, màu chữ và viền chữ đổi theo (Tuỳ chỉnh: giữ màu nền đang đặt trên Image).
using System;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class SketchButton : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IPointerClickHandler, IPointerExitHandler
    {
        public static Action<string> Sound; // AudioService gắn vào: Sound("click")

        [SerializeField] Image bg;
        [SerializeField] TextMeshProUGUI label;
        [SerializeField] bool round;
        [SerializeField] Sprite normal, pressed;
        [Tooltip("Màu nền theo vai trò; Tuỳ chỉnh thì giữ màu đang đặt trên Image")]
        [SerializeField] BtnColor color = BtnColor.Yellow;
        [SerializeField] Material labelOutlined, labelPlain; // chữ trắng viền mực / chữ mực không viền
        [SerializeField] Color baseColor = Color.white;

        bool down, interactable = true;
        Action onClick;

        public TextMeshProUGUI Label => label;
        public RectTransform Rect => (RectTransform)transform;
        public string ClickSound = "click";

        public static Color Fill(BtnColor c)
        {
            switch (c)
            {
                case BtnColor.Red: return Theme.Red;
                case BtnColor.Green: return Theme.Green;
                case BtnColor.Blue: return Theme.Blue;
                case BtnColor.Orange: return Theme.Orange;
                case BtnColor.Purple: return Theme.Purple;
                case BtnColor.Paper: return Theme.Paper;
                default: return Theme.Yellow;
            }
        }

        public static bool DarkLabel(BtnColor c) => c == BtnColor.Paper || c == BtnColor.Yellow;

        // Dùng khi nướng prefab (Editor): gắn các phần đã dựng.
        public void Setup(Image image, TextMeshProUGUI text, bool isRound, Sprite normalSprite, Sprite pressedSprite, Material outlined, Material plain)
        {
            bg = image;
            label = text;
            round = isRound;
            normal = normalSprite;
            pressed = pressedSprite;
            labelOutlined = outlined;
            labelPlain = plain;
            baseColor = bg.color;
        }

        // Đổi màu theo vai trò (nền, màu chữ, viền chữ).
        public void SetRole(BtnColor c)
        {
            color = c;
            ApplyRole();
        }

        void ApplyRole()
        {
            if (!bg) return;
            if (color != BtnColor.Custom) baseColor = Fill(color);
            bg.color = interactable ? baseColor : Dimmed(baseColor);
            if (!label || color == BtnColor.Custom) return;
            bool dark = DarkLabel(color);
            label.color = dark ? Theme.Ink : Color.white;
            var m = dark ? labelPlain : labelOutlined;
            if (m) label.fontSharedMaterial = m;
        }

#if UNITY_EDITOR
        void OnValidate() => ApplyRole();
#endif

        public void SetText(string s) => label.text = s.ToUpperInvariant();

        // Bề rộng theo chữ như Ui.Button tự rộng (nướng với width < 0): gọi sau SetText khi chữ đổi lúc chạy.
        public void FitWidth()
        {
            float h = Rect.sizeDelta.y;
            float w = round ? h : Mathf.Max(h * 1.6f, label.text.Length * label.fontSizeMax * 0.62f + 80);
            Rect.sizeDelta = new Vector2(w, h);
            var le = GetComponent<LayoutElement>();
            if (le) le.preferredWidth = w;
        }

        public void SetOnClick(Action click) => onClick = click;

        // công cụ thử bấm hộ (như người chơi chạm)
        public void SimulateClick() => OnPointerClick(null);

        static Color Dimmed(Color c) => Color.Lerp(c, Theme.Paper3, 0.75f) * new Color(1, 1, 1, 0.75f);

        public bool Interactable
        {
            get => interactable;
            set
            {
                interactable = value;
                bg.color = value ? baseColor : Dimmed(baseColor);
                if (label) label.alpha = value ? 1 : 0.6f;
            }
        }

        // màu nền riêng (không theo vai trò)
        public void SetColor(Color c)
        {
            color = BtnColor.Custom;
            baseColor = c;
            if (interactable) bg.color = c;
        }

        public void OnPointerDown(PointerEventData e)
        {
            if (!interactable) return;
            down = true;
            bg.sprite = pressed;
            // thân dịch theo bóng: 4 px sang phải, 6 px xuống
            if (label) label.rectTransform.anchoredPosition += new Vector2(4, -6);
        }

        void Release()
        {
            if (!down) return;
            down = false;
            bg.sprite = normal;
            if (label) label.rectTransform.anchoredPosition -= new Vector2(4, -6);
        }

        public void OnPointerUp(PointerEventData e) => Release();

        public void OnPointerExit(PointerEventData e) => Release();

        public void OnPointerClick(PointerEventData e)
        {
            if (!interactable)
            {
                Sound?.Invoke("error");
                return;
            }
            if (!string.IsNullOrEmpty(ClickSound)) Sound?.Invoke(ClickSound);
            onClick?.Invoke();
        }
    }
}
