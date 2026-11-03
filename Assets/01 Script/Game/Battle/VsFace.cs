// Ô mặt một tướng trong màn VS (prefab Items/TranVsMat, dựng bằng menu "PokiClash/Prefab/Trận: màn VS truyện tranh"): khung giấy viền
// mực tô màu phe, mặt tướng (ảnh mặt vẽ tay HeroArt.Face; chưa có thì chân dung phóng cho đầu lấp ô, HeroArt.FitHead), nhãn BOSS góc trên trái,
// ô tên và cấp đè mép dưới khung. Dựng sẵn ở cỡ Size; màn VS đổi cỡ bằng localScale, lật hình (không lật chữ) cho phe mình.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class VsFace : MonoBehaviour
    {
        public const float Size = 300;

        [SerializeField] Image frame, face;
        [SerializeField] RectTransform art; // chứa mặt và chân dung (lật ngang cho phe mình)
        [SerializeField] HeroPortrait portrait;
        [SerializeField] GameObject boss;
        [SerializeField] TextMeshProUGUI label;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image frameImg, RectTransform artRt, Image faceImg, HeroPortrait por, GameObject bossTag, TextMeshProUGUI labelText)
        {
            frame = frameImg;
            art = artRt;
            face = faceImg;
            portrait = por;
            boss = bossTag;
            label = labelText;
        }

        // star: sao để chọn dạng (HeroArt.FormOf); tint: màu lòng khung theo phe
        public void Bind(HeroDef h, string heroName, int star, int level, bool isBoss, bool mirror, Color tint)
        {
            name = "vs_mat_" + h.id;
            frame.color = tint;
            var s = HeroArt.Face(h, star);
            face.gameObject.SetActive(s);
            portrait.gameObject.SetActive(!s);
            if (s) Theme.SetSprite(face, s);
            else HeroArt.FitHead(portrait, h, star, art.rect.size);
            art.localScale = new Vector3(mirror ? -1 : 1, 1, 1);
            boss.SetActive(isBoss);
            label.text = $"{heroName} <size=72%><color=#8a7560>Lv{level}</color></size>";
        }
    }
}
