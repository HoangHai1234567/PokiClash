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
        public void Bind(StageDef st, bool open, bool cleared, bool current, Vector2 pos, Action onClick) =>
            Bind(st, open, cleared, current, pos, onClick, Size, SizeNow, false);

        // đảo vùng đất: chấm to theo dữ liệu (người dùng dặn chấm phải đủ lớn, 2026-11-18), có số ải
        public void Bind(StageDef st, bool open, bool cleared, bool current, Vector2 pos, Action onClick, float size, float sizeNow, bool number)
        {
            name = "cham_" + st.idx;
            var rt = (RectTransform)transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = pos;
            float hitSize = Mathf.Max(Hit, sizeNow + 30);
            rt.sizeDelta = new Vector2(hitSize, hitSize);
            float s = current ? sizeNow : size;
            dot.Rect.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(s, s));
            dot.SetText(number ? st.idx.ToString() : "");
            if (number)
            {
                // chấm chưa mở màu đá đậm hơn xám nhạt cũ, số mực đậm: nổi trên đường cát (soi M1 2026-11-18)
                if (!open) dot.SetColor(Theme.Hex("#c4b38c"));
                dot.Label.enableAutoSizing = false;
                dot.Label.fontSize = s * 0.44f;
                dot.Label.color = open ? Theme.Ink : Theme.Ink2;
            }
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
