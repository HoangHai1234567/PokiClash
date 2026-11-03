// Ô chân dung đồng đội ở hàng dưới của trận (prefab Assets/04 Prefabs/Items/TranDongDoi): khung, chân dung, thanh máu nhỏ,
// nhãn "ĐANG ĐÁNH" khi đang ra sân, xám mờ kèm dấu X đỏ khi đã gục (như mặt địch, FoeFace). Chạm để đổi tướng.
using System;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class TeamSlot : MonoBehaviour
    {
        [SerializeField] Image bg;
        [SerializeField] ClickCatcher click;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] RectTransform hpFill;
        [SerializeField] GameObject activeTag;
        [SerializeField] CanvasGroup group;
        [SerializeField] Image[] tinted; // ảnh con (trừ khung), trả về màu gốc trước khi làm xám
        [SerializeField] Color[] baseColors;
        [SerializeField] GameObject cross; // dấu X đỏ khi gục (menu "PokiClash/Prefab/Trận: mặt địch góc trên, dấu X tướng gục")

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor): ghi màu gốc của mọi ảnh con.
        public void Setup(Image bgImg, ClickCatcher catcher, HeroPortrait por, RectTransform fill, GameObject tag, CanvasGroup cg)
        {
            bg = bgImg;
            click = catcher;
            portrait = por;
            hpFill = fill;
            activeTag = tag;
            group = cg;
            var imgs = new System.Collections.Generic.List<Image>();
            foreach (var g in GetComponentsInChildren<Image>(true))
                if (g != bg)
                    imgs.Add(g);
            tinted = imgs.ToArray();
            baseColors = new Color[tinted.Length];
            for (int i = 0; i < tinted.Length; i++) baseColors[i] = tinted[i].color;
        }

        public void Bind(Fighter f, int index, bool active, Action onClick)
        {
            name = "dong_doi_" + index;
            Rect.localEulerAngles = Vector3.zero;
            bg.color = active ? Theme.Hex("#ffe9a0") : Theme.Hex("#e9f6e0");
            click.OnClick = onClick;
            for (int i = 0; i < tinted.Length; i++) tinted[i].color = baseColors[i];
            portrait.Bind(f.hero, 108, false, f.star);
            hpFill.anchorMax = new Vector2((float)Math.Max(0, f.hp / f.maxHp), 1);
            activeTag.SetActive(active);
            group.alpha = f.dead ? 0.5f : 1;
            if (cross) cross.SetActive(false); // tắt trước khi làm xám, dấu X giữ màu đỏ
            if (f.dead)
                foreach (var g in GetComponentsInChildren<Image>())
                    g.color = new Color(0.6f, 0.6f, 0.6f, g.color.a);
            if (cross) cross.SetActive(f.dead);
        }
    }
}
