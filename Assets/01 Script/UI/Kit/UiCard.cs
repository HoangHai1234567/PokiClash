// Thẻ bài vẽ tay (chép cardEl của bản web): dải màu độ hiếm trên đầu, băng keo theo loại thẻ, tên viền mực, ô hình tròn,
// mô tả theo cấp thẻ, dòng độ hiếm, nhãn giá (mana xanh, nộ cam), khoá, vệt sáng chạy cho thẻ Huyền thoại.
// Prefab Assets/04 Prefabs/Kit/The (320 × 464) và TheMini (200 × 292), web 160 × 232 và 100 × 146. Bind gán thẻ.
using System;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiCard : MonoBehaviour, IPointerClickHandler
    {
        public static readonly Vector2 NormalSize = new Vector2(320, 464);
        public static readonly Vector2 MiniSize = new Vector2(200, 292);

        [Serializable]
        public struct Parts
        {
            public Image frame, band, tape, art, icon, cost, shine, lockPanel;
            public TextMeshProUGUI name, desc, rarity, costText, lockText;
            public RectMask2D mask;
        }

        [SerializeField] bool mini;
        [SerializeField] Parts p;

        public CardDef Card { get; private set; }
        public bool Mini => mini;
        Action onClick;
        float shineT;

        // Dùng khi nướng prefab (Editor).
        public void Setup(bool isMini, Parts parts)
        {
            mini = isMini;
            p = parts;
        }

        // Tạo thẻ từ prefab kit. icon: hình của thẻ (ArtLibrary.Icon(card.icon)); null thì dùng chấm mực.
        public static UiCard Create(Transform parent, CardDef c, int lv, bool mini, Sprite icon, string locked = null, Action onClick = null, bool showKind = false)
        {
            var card = Ui.Spawn(mini ? Theme.Prefabs.cardMini : Theme.Prefabs.card, parent);
            card.Bind(c, lv, icon, locked, onClick, showKind);
            return card;
        }

        public void Bind(CardDef c, int lv, Sprite icon, string locked = null, Action click = null, bool showKind = false)
        {
            Card = c;
            onClick = click;
            name = "the_" + c.id;
            float k = mini ? 0.625f : 1f;
            var rc = Theme.Of(c.rarity);

            p.frame.raycastTarget = click != null;
            p.frame.color = string.IsNullOrEmpty(locked) ? Theme.CardFill : Color.Lerp(Theme.CardFill, Theme.Paper3, 0.6f);
            p.band.color = rc;
            p.tape.color = c.kind == CardKind.Ult ? Theme.TapePink : c.kind == CardKind.Skill ? Theme.TapeBlue : c.kind == CardKind.Passive ? Theme.TapeGreen : Theme.TapeYellow;
            p.name.text = c.name;
            p.name.color = Color.white;
            p.art.color = new Color(rc.r, rc.g, rc.b, 0.35f);
            Theme.SetSprite(p.icon, icon != null ? icon : Sketch.InkDot);
            p.icon.color = icon != null ? Color.white : Theme.Ink3;
            p.desc.text = CardText.Text(c, lv);
            p.desc.color = Theme.Ink;
            string rar = (showKind || c.kind != CardKind.Pool ? Elements.KindName(c.kind) + " · " : "") + Elements.RarityName(c.rarity) + (lv > 1 ? $" · cấp {lv}" : "");
            p.rarity.text = "<color=#" + ColorUtility.ToHtmlStringRGB(rc) + ">•</color> " + rar.ToUpperInvariant();
            p.rarity.color = Theme.Ink2;

            p.cost.gameObject.SetActive(c.HasCost);
            if (c.HasCost)
            {
                p.cost.color = c.costRage > 0 ? Theme.Rage : Theme.Mana;
                p.costText.text = CardText.CostText(c);
                p.costText.color = Color.white;
                float w = p.costText.GetPreferredValues().x + 28;
                p.cost.rectTransform.sizeDelta = new Vector2(w, 52 * k);
            }

            bool legend = c.rarity == Rarity.Legend;
            p.shine.gameObject.SetActive(legend);
            p.shine.color = new Color(1, 1, 1, 0.45f);
            p.mask.enabled = legend;

            bool isLocked = !string.IsNullOrEmpty(locked);
            if (isLocked)
                foreach (var g in new Graphic[] { p.band, p.tape, p.name, p.art, p.icon, p.desc, p.rarity, p.cost, p.costText, p.shine })
                    g.color = new Color(g.color.r * 0.6f + 0.25f, g.color.g * 0.6f + 0.25f, g.color.b * 0.6f + 0.25f, g.color.a * 0.65f);
            p.lockPanel.gameObject.SetActive(isLocked);
            if (isLocked) p.lockText.text = locked;
        }

        void Update()
        {
            if (!p.shine || !p.shine.gameObject.activeSelf) return;
            // vệt sáng chạy chéo mỗi 2,4 giây
            shineT = (shineT + Time.unscaledDeltaTime / 2.4f) % 1f;
            float w = ((RectTransform)transform).rect.width;
            p.shine.rectTransform.anchoredPosition = new Vector2(Mathf.Lerp(-w * 0.4f, w * 1.4f, shineT), 0);
        }

        public void OnPointerClick(PointerEventData e)
        {
            if (onClick == null) return;
            SketchButton.Sound?.Invoke("pick");
            onClick();
        }
    }
}
