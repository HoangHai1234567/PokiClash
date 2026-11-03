// Chấm ải xen giữa trên đường mòn của đảo 70 ải (prefab Assets/04 Prefabs/Items/ChamAi, dựng bằng menu
// "PokiClash/Prefab/Đảo 70 ải (ChamAi, DongChang, BangChang)"): nút tròn kit nhỏ (vàng: đã qua, cam: đang đánh, xám: chưa mở),
// vùng chạm rộng hơn chấm, nhịp ở ải đang đánh. Chạm mở bảng chặng.
using System;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class ZonePip : MonoBehaviour
    {
        // cỡ chấm, chấm ải đang đánh, vùng chạm (người dùng 2026-11-03: chấm to hơn, 22/34/64 cũ nhỏ quá)
        public const float Size = 32, SizeNow = 46, Hit = 76;

        [SerializeField] SketchButton dot;
        [SerializeField] ClickCatcher hit;
        [SerializeField] Pulse pulse;

        // Dùng khi dựng prefab (Editor).
        public void Setup(SketchButton dotButton, ClickCatcher hitArea, Pulse dotPulse)
        {
            dot = dotButton;
            hit = hitArea;
            pulse = dotPulse;
        }

        // pos: chỗ ải trong khung ảnh đảo (gốc trên trái)
        public void Bind(StageDef st, bool open, bool cleared, bool current, Vector2 pos, Action onClick)
        {
            name = "cham_" + st.idx;
            var rt = (RectTransform)transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = pos;
            rt.sizeDelta = new Vector2(Hit, Hit);
            float s = current ? SizeNow : Size;
            dot.Rect.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(s, s));
            dot.SetText("");
            dot.SetColor(cleared ? Theme.Hex("#ffe08a") : current ? Theme.Hex("#ff8a6a") : Theme.Hex("#d9d2c2"));
            pulse.enabled = current;
            dot.transform.localScale = Vector3.one;
            hit.OnClick = () =>
            {
                SketchButton.Sound?.Invoke("click");
                onClick();
            };
        }
    }
}
