// Ô mặt một địch ở góc trên trái sân (prefab Items/TranMatDich, hàng BattleView.p.foeRow): người chơi thấy trận có mấy địch, còn
// mấy con. Đang ra sân: nền vàng, to hơn; đã gục: chân dung tô sẫm đặc, nền giấy sẫm, dấu X đỏ. Chân dung vừa trọn con trong ô
// (HeroArt.FitBody, hộp hình đo sẵn PortraitBoxes; người dùng báo 2026-11-27 bản cắt đầu phóng to "mờ và xấu", ô gục xám trong mờ).
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

        static readonly Color Idle = Theme.Hex("#fbf4e2"), Active = Theme.Hex("#ffe9a0"), Dead = Theme.Hex("#b8ab98");
        static readonly Color DeadTint = Theme.Hex("#5e5045"); // hình tướng gục: sẫm đặc (bản cũ xám trong mờ 50% nhìn bẩn)
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
                HeroArt.FitBody(portrait, hero, star, ((RectTransform)portrait.Rect.parent).rect.size);
                shown = hero;
                shownStar = star;
            }
            bg.color = dead ? Dead : active ? Active : Idle;
            portraitImg.color = dead ? DeadTint : Color.white;
            cross.SetActive(dead);
            Rect.localScale = Vector3.one * (active && !dead ? 1.12f : 1f);
        }
    }
}
