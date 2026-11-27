// Ô mặt một tướng trong màn VS (prefab Items/TranVsMat, dựng bằng menu "PokiClash/Prefab/Trận/Trận: màn VS truyện tranh"): khung giấy viền
// mực tô màu phe, mặt tướng (ảnh mặt vẽ tay HeroArt.Face; chưa có thì chân dung phóng cho đầu lấp ô, HeroArt.FitHead), nhãn BOSS góc trên trái,
// ô tên và cấp đè mép dưới khung. Dựng sẵn ở cỡ Size; màn VS đổi cỡ bằng localScale, lật hình (không lật chữ) cho phe mình.
// Màn VS bản tối (2026-11-27) đặt rig vector của tướng (AolaSticker) vào vùng hình (ArtRect, trong mặt nạ stencil của ô: ảnh rig dùng
// shader viền sticker, không theo RectMask2D) rồi gọi UseRig để ẩn mặt / chân dung.
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
        // vùng hình trong mặt nạ ô (lật ngang cho phe mình) và cỡ của nó (đơn vị ô dựng sẵn)
        public RectTransform ArtRect => art;
        public Vector2 ArtBox => art.rect.size;

        // màn VS bản nhân vật (2026-11-27: "thay vì icon 2 con cho luôn 2 con nhân vật"): bỏ khung ô và mặt nạ, tướng đứng cả thân trong
        // vùng hình (rig đặt sau; trong lúc chờ hoặc không có rig thì chân dung trọn con), ô tên dưới chân, nhãn BOSS giữ nguyên
        public void Body(HeroDef h, int star)
        {
            frame.enabled = false;
            var holder = art.parent;
            var mask = holder ? holder.GetComponent<Mask>() : null;
            if (mask)
            {
                mask.enabled = false;
                var g = holder.GetComponent<Graphic>();
                if (g) g.enabled = false;
            }
            face.gameObject.SetActive(false);
            portrait.gameObject.SetActive(true);
            HeroArt.FitBody(portrait, h, star, art.rect.size, 0.9f);
        }

        // rig đã đặt vào vùng hình: ẩn mặt vẽ tay / chân dung
        public void UseRig(bool on)
        {
            if (!on) return;
            face.gameObject.SetActive(false);
            portrait.gameObject.SetActive(false);
        }

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
