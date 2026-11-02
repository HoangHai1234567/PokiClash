// Màn VS đầu trận (dựng sẵn, tắt, trong lớp phủ của prefab Screens/Battle): nền tối, tên ải, đội địch, chữ VS, đội bạn.
// BattleController bật lên, gán tên ải và chân dung hai đội, chạy hoạt cảnh rồi tắt.
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class BattleIntro : MonoBehaviour
    {
        [SerializeField] CanvasGroup group;
        [SerializeField] TextMeshProUGUI title, vs;
        [SerializeField] RectTransform mine, foe; // hàng chân dung đội bạn, đội địch

        public CanvasGroup Group => group;
        public TextMeshProUGUI Title => title;
        public TextMeshProUGUI Vs => vs;
        public RectTransform Row(int side) => side == 0 ? mine : foe;

        // Dùng khi nướng prefab (Editor).
        public void Setup(CanvasGroup cg, TextMeshProUGUI titleText, TextMeshProUGUI vsText, RectTransform myRow, RectTransform foeRow)
        {
            group = cg;
            title = titleText;
            vs = vsText;
            mine = myRow;
            foe = foeRow;
        }
    }
}
