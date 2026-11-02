// Màn mây vẽ tay khi chuyển scene: hai khối mây từ hai bên khép vào giữa (0,38 giây), đổi scene khi đã che kín,
// rồi tách ra (0,38 giây). Trong lúc chuyển chặn mọi thao tác chạm. Nằm trong prefab App (Canvas phu/Nen/May).
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CloudCover : MonoBehaviour
    {
        public const float Duration = 0.38f;

        [SerializeField] RectTransform left, right;
        [SerializeField] Image blocker;
        public bool Closed { get; private set; }

        RectTransform Root => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform leftHalf, RectTransform rightHalf, Image block)
        {
            left = leftHalf;
            right = rightHalf;
            blocker = block;
            SetT(0);
            Block(false);
        }

        public void Block(bool on)
        {
            blocker.raycastTarget = on;
            blocker.gameObject.SetActive(on);
        }

        // t = 0 mở hẳn, 1 che kín
        void SetT(float t)
        {
            var size = Root.rect.size;
            if (size.x <= 0) size = new Vector2(PokiCanvas.RefW, PokiCanvas.RefH);
            var cloud = new Vector2(size.x * 0.95f, size.y * 1.15f);
            left.sizeDelta = right.sizeDelta = cloud;
            float off = -cloud.x * (1 - t);
            left.anchoredPosition = new Vector2(off, 0);
            right.anchoredPosition = new Vector2(-off, 0); // nửa phải lật ngang: dịch ngược dấu
            left.gameObject.SetActive(t > 0.001f);
            right.gameObject.SetActive(t > 0.001f);
            // phồng nhẹ khi khép
            float puff = 1 + 0.04f * Mathf.Sin(t * Mathf.PI);
            left.localScale = new Vector3(puff, puff, 1);
            right.localScale = new Vector3(-puff, puff, 1);
        }

        public IEnumerator Close()
        {
            Block(true);
            if (Closed) yield break;
            for (float t = 0; t < Duration; t += Time.unscaledDeltaTime)
            {
                float k = t / Duration;
                SetT(k * k * (3 - 2 * k));
                yield return null;
            }
            SetT(1);
            Closed = true;
        }

        public IEnumerator Open()
        {
            for (float t = 0; t < Duration; t += Time.unscaledDeltaTime)
            {
                float k = t / Duration;
                SetT(1 - k * k * (3 - 2 * k));
                yield return null;
            }
            SetT(0);
            Closed = false;
            Block(false);
        }

        // che ngay (lúc khởi động, trước scene đầu tiên)
        public void CloseNow()
        {
            Block(true);
            SetT(1);
            Closed = true;
        }
    }
}
