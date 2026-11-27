// Một ô của Sổ Phép (prefab mục Items/OSoPhep, 20 bản sao đặt sẵn trong Dialogs/SoPhep; menu "PokiClash/Prefab/Hộp thoại và màn/Sổ Phép").
// Màn nền tối, cây toả ra nối bằng đường (người dùng 2026-11-27): ô là đĩa tròn có icon, viền tròn vẽ tay, tên và giá bên dưới (miếng nền
// cùng màu nền sau chữ che đường nối đi ngang). Ô chốt to hơn, viền đôi (SetSize lúc dựng prefab). Trạng thái:
// - chương khoá: đĩa tối, icon chìm, chữ mờ;
// - chưa vẽ, chưa vẽ được: đĩa kem, viền xám tím; vẽ được: viền trắng thở nhẹ, giá vàng;
// - đã vẽ: đĩa và viền màu chương; vẽ đủ ghi "Đã vẽ"; ô nhiều cấp có viên "1/2" ở góc;
// - đang chọn: vòng đứt nét trắng xoay chậm quanh ô.
// Màu đặc, không dùng alpha để pha sáng tối: nền tối trộn theo Linear làm lớp mờ sáng hơn nhiều (memory ui-phu-toi-linear).
// Tiêu đề không dùng chữ đen đậm (người dùng 2026-11-27): tên ô Baloo2 Bold màu kem.
using System;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    // bảng màu màn Sổ Phép nền tối
    public static class SoPhepColors
    {
        public static readonly Color Bg = UI.Theme.Hex("#1d1b2c");
        public static readonly Color Panel = UI.Theme.Hex("#262439");
        public static readonly Color Plate = UI.Theme.Hex("#2c2943"); // băng chương, viên số
        public static readonly Color Dots = UI.Theme.Hex("#3f3b58"); // chấm sao nền
        public static readonly Color Cream = UI.Theme.Hex("#f4ecd8");
        public static readonly Color Soft = UI.Theme.Hex("#d9d3e6"); // chữ mô tả
        public static readonly Color Muted = UI.Theme.Hex("#a7a1bd");
        public static readonly Color Dim = UI.Theme.Hex("#6c6884");
        public static readonly Color Coral = UI.Theme.Hex("#f08a7a");
        public static readonly Color Gold = UI.Theme.Hex("#f7c948");
        public static readonly Color LineOpen = UI.Theme.Hex("#4a4664"); // đường chưa sáng (chương mở)
        public static readonly Color LineLock = UI.Theme.Hex("#2f2c45"); // đường chương khoá
        public static readonly Color DiscOpen = UI.Theme.Hex("#efe6d2");
        public static readonly Color DiscLock = UI.Theme.Hex("#34314a");
        public static readonly Color RingOpen = UI.Theme.Hex("#7a7494");
        public static readonly Color RingLock = UI.Theme.Hex("#403c58");

        // màu chương (viền, đường đã vẽ) và màu sáp nhạt (đĩa đã vẽ)
        static readonly Color[] Ch = { UI.Theme.Hex("#f7c948"), UI.Theme.Hex("#7fd46a"), UI.Theme.Hex("#6fb6f2"), UI.Theme.Hex("#c18af0") };
        static readonly Color[] ChFill = { UI.Theme.Hex("#ffe6a3"), UI.Theme.Hex("#d4f0c6"), UI.Theme.Hex("#d6e8fb"), UI.Theme.Hex("#ecd9f7") };
        public static Color Chapter(int ch) => Ch[Mathf.Clamp(ch, 0, Ch.Length - 1)];
        public static Color ChapterFill(int ch) => ChFill[Mathf.Clamp(ch, 0, ChFill.Length - 1)];
    }

    public sealed class SoPhepTile : MonoBehaviour
    {
        public const float Size = 150, CapSize = 190, LabelW = 236;

        [SerializeField] Image disc, ring, ring2, sel, icon, badge, badgeRing, plate;
        [SerializeField] TextMeshProUGUI title, sub, level;
        [SerializeField] ClickCatcher click;

        bool pulse;
        float phase;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image discImg, Image ringImg, Image ring2Img, Image selImg, Image iconImg, Image badgeImg, Image badgeRingImg, Image plateImg,
            TextMeshProUGUI titleText, TextMeshProUGUI subText, TextMeshProUGUI levelText, ClickCatcher catcher)
        {
            disc = discImg;
            ring = ringImg;
            ring2 = ring2Img;
            sel = selImg;
            icon = iconImg;
            badge = badgeImg;
            badgeRing = badgeRingImg;
            plate = plateImg;
            title = titleText;
            sub = subText;
            level = levelText;
            click = catcher;
        }

        // Đặt cỡ đĩa và vị trí chữ (Editor, lúc dựng prefab): gốc ô (pivot) là tâm đĩa; chữ nằm dưới đĩa. cap: viền đôi.
        public void SetSize(float d, bool cap)
        {
            var rt = Rect;
            float h = d + 100;
            rt.sizeDelta = new Vector2(Mathf.Max(d, LabelW), h);
            rt.pivot = new Vector2(0.5f, 1 - d / 2 / h);
            void At(Graphic g, Vector2 pos, Vector2 size)
            {
                var r = g.rectTransform;
                r.anchorMin = r.anchorMax = new Vector2(0.5f, 1);
                r.pivot = new Vector2(0.5f, 0.5f);
                r.anchoredPosition = pos;
                r.sizeDelta = size;
            }
            var c = new Vector2(0, -d / 2);
            At(sel, c, Vector2.one * d * 1.22f);
            At(disc, c, Vector2.one * d);
            At(ring, c, Vector2.one * d);
            At(ring2, c, Vector2.one * d * 0.84f);
            ring2.gameObject.SetActive(cap);
            At(icon, c, Vector2.one * d * 0.62f);
            var bc = c + new Vector2(d * 0.36f, -d * 0.36f);
            At(badge, bc, new Vector2(74, 42));
            At(badgeRing, bc, new Vector2(74, 42));
            At(level, bc + new Vector2(0, 1), new Vector2(74, 42));
            At(plate, new Vector2(0, -d - 46), new Vector2(LabelW - 6, 76));
            At(title, new Vector2(0, -d - 30), new Vector2(LabelW, 38));
            At(sub, new Vector2(0, -d - 64), new Vector2(LabelW, 30));
        }

        public void Bind(SoPhepNode n, Sprite iconSprite, int lv, int face, bool open, bool canBuy, int cost, bool selected, Action onClick)
        {
            bool owned = lv > 0, maxed = lv >= n.MaxLv;
            var chc = SoPhepColors.Chapter(n.ch);
            disc.color = owned ? SoPhepColors.ChapterFill(n.ch) : open ? SoPhepColors.DiscOpen : SoPhepColors.DiscLock;
            var rc = owned ? chc : !open ? SoPhepColors.RingLock : canBuy ? Color.white : SoPhepColors.RingOpen;
            ring.color = rc;
            ring2.color = Color.Lerp(rc, SoPhepColors.Bg, 0.35f);
            UI.Theme.SetSprite(icon, iconSprite);
            icon.color = open ? Color.white : new Color(0.3f, 0.29f, 0.38f, 0.75f);
            title.text = n.FaceCount > 1 && !n.IsElem ? n.FaceName(face) : n.Name; // ô chọn: mặt đang chọn; ô 5 hệ: tên ô (hệ ở bảng đáy)
            title.color = open ? SoPhepColors.Cream : SoPhepColors.Dim;
            sub.text = maxed ? Loc.T("Đã vẽ") : n.stones > 0 && lv == 0 ? Loc.F("{0} nét · {1} đá", cost, n.stones) : Loc.F("{0} nét", cost);
            sub.color = !open ? SoPhepColors.Dim : maxed ? chc : canBuy ? SoPhepColors.Gold : SoPhepColors.Muted;
            bool multi = n.MaxLv > 1;
            badge.gameObject.SetActive(multi);
            badgeRing.gameObject.SetActive(multi);
            level.gameObject.SetActive(multi);
            level.text = $"{lv}/{n.MaxLv}";
            level.color = open ? SoPhepColors.Cream : SoPhepColors.Dim;
            badgeRing.color = rc;
            sel.gameObject.SetActive(selected);
            pulse = open && canBuy && !maxed;
            if (!pulse) ring.rectTransform.localScale = Vector3.one;
            click.OnClick = onClick;
        }

        void OnEnable() => phase = UnityEngine.Random.Range(0f, 6.28f);

        void Update()
        {
            float t = Time.unscaledTime;
            if (sel.gameObject.activeSelf) sel.rectTransform.localEulerAngles = new Vector3(0, 0, -t * 18);
            // vẽ được: viền thở to nhỏ nhẹ (1,0 ↔ 1,05), lệch pha giữa các ô
            if (pulse) ring.rectTransform.localScale = Vector3.one * (1.025f + 0.025f * Mathf.Sin(t * 3.2f + phase));
        }
    }
}
