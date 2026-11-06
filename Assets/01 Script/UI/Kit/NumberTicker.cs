// Số đếm chạy rồi nảy (bộ UI Sa Bàn): đặt số mới thì chữ chạy từ số đang hiện tới số mới trong 0,6 giây, xong thì phần tử cha
// (chip) nảy nhẹ. Lần đặt đầu hiện thẳng. NumberTicker.Set(chữ, số, cách in) tự gắn component vào chữ.
using System;
using TMPro;
using UnityEngine;

namespace PokiClash.UI
{
    public sealed class NumberTicker : MonoBehaviour
    {
        const float Len = 0.6f;
        TextMeshProUGUI text;
        Func<long, string> fmt;
        long from, to, shown;
        float t = -1;
        bool init;

        public static void Set(TextMeshProUGUI tmp, long value, Func<long, string> format)
        {
            if (!tmp) return;
            var nt = tmp.TryGetComponent<NumberTicker>(out var x) ? x : tmp.gameObject.AddComponent<NumberTicker>();
            nt.Go(tmp, value, format);
        }

        void Go(TextMeshProUGUI tmp, long v, Func<long, string> format)
        {
            text = tmp;
            fmt = format ?? (n => n.ToString());
            if (!init || !isActiveAndEnabled)
            {
                init = true;
                shown = from = to = v;
                t = -1;
                text.text = fmt(v);
                return;
            }
            if (v == to) return;
            from = shown;
            to = v;
            t = 0;
        }

        void Update()
        {
            if (t < 0) return;
            t += Mathf.Min(0.05f, Time.unscaledDeltaTime);
            float k = Mathf.Min(1, t / Len);
            shown = (long)Math.Round(from + (to - from) * (1 - Math.Pow(1 - k, 3)));
            text.text = fmt(shown);
            if (k >= 1)
            {
                t = -1;
                var target = transform.parent ? transform.parent : transform;
                UiMotion.Of(target).Punch(0.6f);
            }
        }

        void OnDisable()
        {
            // tắt giữa chừng: hiện thẳng số cuối
            if (t >= 0 && text)
            {
                t = -1;
                shown = to;
                text.text = fmt(to);
            }
        }
    }
}
