// Băng rôn giữa sân của trận (prefab Assets/04 Prefabs/Items/TranBangRon): "Hiệp N" trên giấy, tên tuyệt kỹ trên nền đỏ.
// BattleView giữ hàng chờ: chạy xong thì tắt, lần sau dùng lại.
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleBanner : MonoBehaviour
    {
        [SerializeField] Image bg;
        [SerializeField] TextMeshProUGUI title, sub;
        [SerializeField] CanvasGroup group;
        [SerializeField] Material titleRound, titleUlt; // chữ viền 0,28 (hiệp) và 0,32 (tuyệt kỹ)

        public RectTransform Rect => (RectTransform)transform;
        public CanvasGroup Group => group;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, TextMeshProUGUI titleText, TextMeshProUGUI subText, CanvasGroup cg, Material roundMat, Material ultMat)
        {
            bg = bgImg;
            title = titleText;
            sub = subText;
            group = cg;
            titleRound = roundMat;
            titleUlt = ultMat;
        }

        public void Bind(string titleText, string subText, bool ult)
        {
            name = "bang_ron";
            bg.color = ult ? Theme.Red : Theme.Paper;
            title.text = titleText;
            title.fontSize = ult ? 80 : 68;
            if (ult ? titleUlt : titleRound) title.fontSharedMaterial = ult ? titleUlt : titleRound;
            sub.text = subText;
            sub.color = ult ? Color.white : Theme.Ink;
            group.alpha = 1;
            group.blocksRaycasts = false;
            var rt = Rect;
            rt.anchorMin = new Vector2(0, 1);
            rt.anchorMax = new Vector2(1, 1);
            rt.pivot = new Vector2(0.5f, 1);
            rt.offsetMin = new Vector2(-40, -640);
            rt.offsetMax = new Vector2(40, -460);
            rt.localEulerAngles = Vector3.zero;
        }
    }
}
