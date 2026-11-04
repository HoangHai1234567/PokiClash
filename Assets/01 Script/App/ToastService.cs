// Thông báo ngắn ở phía trên: bật ra, đứng khoảng 2,2 giây rồi mờ dần và trôi lên (tổng khoảng 2,7 giây).
// Mỗi thông báo là một bản sao prefab Assets/04 Prefabs/Dialogs/ThongBao.
// Chống dồn (người dùng dặn 2026-11-04, bấm liên tục ở máy bi, bảng chặng): thông báo cùng nội dung đang hiện thì không sinh thêm,
// thông báo cũ nảy lại và đứng lại từ đầu; hiện tối đa MaxShown thông báo, thông báo mới đẩy thông báo cũ nhất mờ đi ngay.
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class ToastService : MonoBehaviour
    {
        public const float Life = 2.7f;
        public const int MaxShown = 3;
        const float PopT = 0.3f, FadeT = 0.4f;

        [SerializeField] UiToast toastPrefab;

        // một thông báo đang hiện: bump = vừa gọi lại cùng nội dung; leaving = đang mờ đi
        sealed class Entry
        {
            public UiToast toast;
            public string text;
            public bool bump, leaving;
        }

        readonly List<Entry> live = new List<Entry>();

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiToast prefab) => toastPrefab = prefab;

        public void Show(string text, Sprite icon = null)
        {
            var same = live.Find(e => !e.leaving && e.text == text);
            if (same != null)
            {
                same.bump = true;
                return;
            }
            foreach (var old in live.Where(e => !e.leaving).Take(Mathf.Max(0, live.Count(e => !e.leaving) - MaxShown + 1)).ToList())
                old.leaving = true;
            var t = Ui.Spawn(toastPrefab, transform);
            t.name = "thong_bao";
            t.Set(text, icon);
            var entry = new Entry { toast = t, text = text };
            live.Add(entry);
            StartCoroutine(Run(entry));
        }

        IEnumerator Run(Entry e)
        {
            var rt = e.toast.Rect;
            var cg = e.toast.Group;
            yield return Pop(rt, 0.3f);
            float held = 0;
            while (!e.leaving && held < Life - PopT - FadeT)
            {
                if (e.bump)
                {
                    e.bump = false;
                    held = 0;
                    yield return Pop(rt, 0.85f);
                    continue;
                }
                held += Time.unscaledDeltaTime;
                yield return null;
            }
            e.leaving = true;
            for (float t = 0; t < FadeT; t += Time.unscaledDeltaTime)
            {
                cg.alpha = 1 - t / FadeT;
                rt.localPosition += new Vector3(0, Time.unscaledDeltaTime * 35, 0);
                yield return null;
            }
            live.Remove(e);
            Destroy(rt.gameObject);
        }

        // nảy: phóng từ cỡ from lên 1,12 rồi về 1
        static IEnumerator Pop(RectTransform rt, float from)
        {
            for (float t = 0; t < PopT; t += Time.unscaledDeltaTime)
            {
                float k = t / PopT;
                float s = k < 0.6f ? Mathf.Lerp(from, 1.12f, k / 0.6f) : Mathf.Lerp(1.12f, 1, (k - 0.6f) / 0.4f);
                rt.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            rt.localScale = Vector3.one;
        }
    }
}
