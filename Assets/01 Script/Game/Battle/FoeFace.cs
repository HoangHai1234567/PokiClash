// Ô mặt một địch ở góc trên trái sân (prefab Items/TranMatDich, hàng BattleView.p.foeRow): người chơi thấy trận có mấy địch, còn
// mấy con. Đang ra sân: nền vàng, to hơn; đã gục: chân dung xám mờ, dấu X đỏ. Chân dung phóng cho đầu lấp ô như màn VS
// (HeroArt.FitHead, hộp hình đo sẵn PortraitBoxes).
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FoeFace : MonoBehaviour
    {
        [SerializeField] Image bg, portraitImg;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] GameObject cross;

        static readonly Color Idle = Theme.Hex("#fbf4e2"), Active = Theme.Hex("#ffe9a0"), Dead = Theme.Hex("#cfc6b8");
        HeroDef shown;
        int shownStar = -1;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, HeroPortrait por, Image porImg, GameObject crossMark)
        {
            bg = bgImg;
            portrait = por;
            portraitImg = porImg;
            cross = crossMark;
        }

        // star: sao để vẽ (boss tiến hóa theo dạng đang hiện)
        public void Bind(HeroDef hero, int star, int index, bool active, bool dead)
        {
            name = "mat_dich_" + index;
            if (hero != shown || star != shownStar)
            {
                HeroArt.FitHead(portrait, hero, star, ((RectTransform)portrait.Rect.parent).rect.size);
                shown = hero;
                shownStar = star;
            }
            bg.color = dead ? Dead : active ? Active : Idle;
            portraitImg.color = dead ? new Color(0.55f, 0.55f, 0.55f, 0.5f) : Color.white;
            cross.SetActive(dead);
            Rect.localScale = Vector3.one * (active && !dead ? 1.12f : 1f);
        }
    }
}
