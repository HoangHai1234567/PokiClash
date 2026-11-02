// Một nút ải trên đảo (prefab Assets/04 Prefabs/Items/NutAi, biến thể nút tròn của kit): số ải, màu theo trạng thái và kiểu ải,
// biểu tượng boss / mini boss, khoá và mờ khi chưa mở, dấu qua, nhịp phồng ở ải đang đánh. Mọi phần có sẵn, Bind bật tắt.
using System;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneNode : MonoBehaviour
    {
        [SerializeField] SketchButton button;
        [SerializeField] Image kind, lockIcon, check;
        [SerializeField] CanvasGroup group;
        [SerializeField] Pulse pulse;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(SketchButton btn, Image kindIcon, Image lockImg, Image checkImg, CanvasGroup cg, Pulse pulseFx)
        {
            button = btn;
            kind = kindIcon;
            lockIcon = lockImg;
            check = checkImg;
            group = cg;
            pulse = pulseFx;
        }

        public static float Size(StageKind k) => k == StageKind.Boss ? 172 : k == StageKind.Mini ? 144 : 116;

        public static Color Fill(StageDef st, bool open, bool cleared) =>
            !open ? Theme.Hex("#d9d2c2") : cleared ? Theme.Hex("#c9eab8") : st.kind == StageKind.Boss ? Theme.Hex("#ffb3a3")
            : st.kind == StageKind.Mini ? Theme.Hex("#ffd9a0") : Theme.Hex("#fff3c4");

        // p: toạ độ trong khung ảnh đảo (gốc trên trái); kindIcon: biểu tượng boss / vương miện của ải đặc biệt
        public void Bind(StageDef st, bool open, bool cleared, bool current, Vector2 p, Sprite kindIcon, Action onClick)
        {
            float size = Size(st.kind);
            name = "ai_" + st.idx;
            button.SetText(open ? st.idx.ToString() : "");
            button.SetColor(Fill(st, open, cleared));
            button.Label.color = Theme.Ink;
            button.Label.fontSizeMax = st.kind == StageKind.Normal ? 48 : 30;
            button.SetOnClick(onClick);
            button.ClickSound = open ? "click" : "error";
            var rt = Rect;
            rt.sizeDelta = new Vector2(size, rt.sizeDelta.y); // cao theo nút tròn của kit như Ui.Button cũ
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = p;

            bool special = st.kind != StageKind.Normal && open;
            kind.gameObject.SetActive(special);
            if (special)
            {
                kind.sprite = kindIcon;
                kind.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(-3, 14), new Vector2(size * 0.5f, size * 0.5f), new Vector2(0.5f, 1));
            }
            button.Label.rectTransform.Stretch(8, special ? size * 0.35f : 4, 14, 14);

            lockIcon.gameObject.SetActive(!open);
            lockIcon.rectTransform.sizeDelta = new Vector2(size * 0.45f, size * 0.45f);
            group.alpha = open ? 1 : 0.85f;
            check.gameObject.SetActive(cleared);
            pulse.enabled = current;
        }
    }
}
