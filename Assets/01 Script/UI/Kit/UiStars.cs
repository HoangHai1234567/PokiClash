// Hàng sao (có / chưa có). Prefab Assets/04 Prefabs/Kit/Sao: 5 sao cỡ 36, xếp ngang.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiStars : MonoBehaviour
    {
        [SerializeField] Image[] stars;
        [SerializeField] HorizontalLayoutGroup row;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image[] images, HorizontalLayoutGroup layout)
        {
            stars = images;
            row = layout;
        }

        // n sao vàng trên tổng max (max không quá số sao của prefab)
        public void Set(int n, int max)
        {
            for (int i = 0; i < stars.Length; i++)
            {
                stars[i].gameObject.SetActive(i < max);
                stars[i].color = i < n ? Theme.Yellow : Theme.Paper3;
            }
            Rect.sizeDelta = new Vector2(Mathf.Min(max, stars.Length) * Size * 0.9f, Size);
        }

        float Size => stars.Length > 0 ? stars[0].rectTransform.sizeDelta.x : 36;

        public void SetSize(float size)
        {
            row.spacing = -size * 0.12f;
            foreach (var s in stars) s.rectTransform.sizeDelta = new Vector2(size, size);
        }
    }
}
