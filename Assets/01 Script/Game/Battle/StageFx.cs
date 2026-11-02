// Một hiệu ứng trên sân đấu: chữ nổi (Items/TranChuNoi), ngôi sao tượng thanh (Items/TranTuongThanh), vòng (Items/TranVong),
// tia văng (Items/TranTia). StageView giữ hàng chờ theo loại: hết thời gian thì tắt, lần sau bật lại dùng tiếp.
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class StageFx : MonoBehaviour
    {
        [SerializeField] CanvasGroup group;
        [SerializeField] Image image; // không có ở chữ nổi
        [SerializeField] TextMeshProUGUI label; // không có ở vòng, tia

        public RectTransform Rect => (RectTransform)transform;
        public CanvasGroup Group => group;
        public Image Image => image;
        public TextMeshProUGUI Label => label;

        // Dùng khi nướng prefab (Editor).
        public void Setup(CanvasGroup cg, Image img, TextMeshProUGUI text)
        {
            group = cg;
            image = img;
            label = text;
        }
    }
}
