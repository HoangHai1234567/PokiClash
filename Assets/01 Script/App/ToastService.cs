// Thông báo ngắn ở phía trên: bật ra, đứng khoảng 2,2 giây rồi mờ dần và trôi lên (tổng khoảng 2,7 giây).
// Mỗi thông báo là một bản sao prefab Assets/04 Prefabs/Dialogs/ThongBao.
using System.Collections;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class ToastService : MonoBehaviour
    {
        public const float Life = 2.7f;

        [SerializeField] UiToast toastPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiToast prefab) => toastPrefab = prefab;

        public void Show(string text, Sprite icon = null)
        {
            var t = Ui.Spawn(toastPrefab, transform);
            t.name = "thong_bao";
            t.Set(text, icon);
            StartCoroutine(Run(t));
        }

        IEnumerator Run(UiToast toast)
        {
            var rt = toast.Rect;
            var cg = toast.Group;
            for (float t = 0; t < 0.3f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.3f;
                float s = k < 0.6f ? Mathf.Lerp(0.3f, 1.12f, k / 0.6f) : Mathf.Lerp(1.12f, 1, (k - 0.6f) / 0.4f);
                rt.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            rt.localScale = Vector3.one;
            yield return new WaitForSecondsRealtime(Life - 0.3f - 0.4f);
            for (float t = 0; t < 0.4f; t += Time.unscaledDeltaTime)
            {
                cg.alpha = 1 - t / 0.4f;
                rt.localPosition += new Vector3(0, Time.unscaledDeltaTime * 35, 0);
                yield return null;
            }
            Destroy(rt.gameObject);
        }
    }
}
