// Nút Chiêu / Tuyệt kỹ ở hàng dưới của trận (dựng sẵn hai nút trong prefab Screens/Battle): icon thẻ, tên, giá hoặc "Đã xếp",
// vạch nộ (Tuyệt kỹ), mờ khi chưa dùng được, viền vàng khi sẵn sàng; vừa sẵn sàng thì icon bật lên một nhịp (PopReady).
using System;
using System.Collections;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class InnateButton : MonoBehaviour
    {
        [SerializeField] Image icon, glow;
        [SerializeField] ClickCatcher click;
        [SerializeField] TextMeshProUGUI cardName, cost;
        [SerializeField] RectTransform meterFill; // chỉ Tuyệt kỹ
        [SerializeField] CanvasGroup group;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image iconImg, Image glowImg, ClickCatcher catcher, TextMeshProUGUI nameText, TextMeshProUGUI costText, RectTransform fill, CanvasGroup cg)
        {
            icon = iconImg;
            glow = glowImg;
            click = catcher;
            cardName = nameText;
            cost = costText;
            meterFill = fill;
            group = cg;
        }

        // why: lý do chưa dùng được ("" = dùng được); rage: nộ của tướng (vạch nộ, 100 là đầy)
        public void Bind(CardDef card, Sprite iconSprite, bool used, string why, bool ready, double rage, Action onClick)
        {
            Rect.localScale = Vector3.one;
            click.OnClick = onClick;
            icon.sprite = iconSprite;
            cardName.text = card.name;
            cost.text = used ? "Đã xếp" : CardText.CostText(card);
            if (meterFill) meterFill.anchorMax = new Vector2(Mathf.Min(1, (float)rage / 100f), 1);
            group.alpha = used ? 0.45f : why != "" ? 0.6f : 1;
            glow.gameObject.SetActive(ready);
        }

        Coroutine pop;

        // vừa đủ mana/nộ (GameFeel 6.10 "tạo power-up"): icon bật 0,6 → 1,35 → 1 trong 0,34 giây, xoay lắc nhẹ. Chỉ đụng icon vì
        // BattleView đang phồng xẹp cả nút khi sẵn sàng.
        public void PopReady()
        {
            if (!icon || !isActiveAndEnabled) return;
            if (pop != null) StopCoroutine(pop);
            pop = StartCoroutine(PopIcon(icon.rectTransform));
        }

        static IEnumerator PopIcon(RectTransform rt)
        {
            const float len = 0.34f;
            for (float t = 0; t < len; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / len;
                float s = k < 0.6f ? Mathf.Lerp(0.6f, 1.35f, 1 - Mathf.Pow(1 - k / 0.6f, 3)) : Mathf.Lerp(1.35f, 1, Mathf.SmoothStep(0, 1, (k - 0.6f) / 0.4f));
                rt.localScale = new Vector3(s, s, 1);
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(k * Mathf.PI * 3) * 10 * (1 - k));
                yield return null;
            }
            if (!rt) yield break;
            rt.localScale = Vector3.one;
            rt.localEulerAngles = Vector3.zero;
        }
    }
}
